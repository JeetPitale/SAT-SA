"""
Unsupervised Anomaly Detection Layer for SAT-SA.
Uses Isolation Forest across aggregated entity-level behavioral features with feature-contribution explainability.
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from sat_sa.detectors.base import BaseDetector, SupervisoryFinding


class UnsupervisedEntityAnomalyDetector:
    """
    Computes cross-dimensional behavioral outlier scores using Isolation Forest
    and calculates feature deviation contributions for supervisory explainability.
    """

    def __init__(self, contamination: float = 0.20, random_state: int = 42):
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100,
        )

    def _extract_entity_features(self, lake) -> Tuple[pd.DataFrame, List[str]]:
        """Extracts comprehensive feature vectors for every CSE."""
        query = """
            SELECT 
                a.cse_id,
                count(distinct a.alert_id) as total_alerts,
                count(distinct a.asset_id) as active_assets,
                count(distinct a.category) as category_count,
                count(distinct a.analyst_id) as active_analysts,
                sum(case when a.severity = 'CRITICAL' then 1 else 0 end) * 1.0 / count(distinct a.alert_id) as crit_ratio,
                sum(case when a.false_positive_flag then 1 else 0 end) * 1.0 / count(distinct a.alert_id) as fp_ratio,
                median(case when a.closed_at is not null then (epoch(a.closed_at) - epoch(a.created_at))/60.0 else null end) as mttr_median_min,
                sum(case when a.severity in ('CRITICAL','HIGH') and (epoch(a.closed_at) - epoch(a.created_at)) < 180 then 1 else 0 end) * 1.0 / 
                    nullif(sum(case when a.severity in ('CRITICAL','HIGH') then 1 else 0 end), 0) as fast_close_crit_ratio
            FROM alerts a
            GROUP BY a.cse_id
        """
        df = lake.query_df(query)
        if df.empty:
            return pd.DataFrame(), []

        df = df.fillna(0.0)
        feature_cols = [c for c in df.columns if c != "cse_id"]
        return df, feature_cols

    def run_all(self, lake) -> Dict[str, Optional[SupervisoryFinding]]:
        """Fits model across all CSEs and returns findings for flagged entities."""
        df, feature_cols = self._extract_entity_features(lake)
        if len(df) < 4:
            return {}

        X = df[feature_cols].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        self.model.fit(X_scaled)
        scores = -self.model.score_samples(X_scaled)  # higher = more anomalous
        preds = self.model.predict(X_scaled)  # -1 = anomaly

        # Population means & std for explainability
        pop_means = X.mean(axis=0)
        pop_stds = X.std(axis=0) + 1e-6

        findings_map: Dict[str, Optional[SupervisoryFinding]] = {}

        for idx, row in df.iterrows():
            cse_id = row["cse_id"]
            is_anomaly = (preds[idx] == -1)
            raw_score = float(scores[idx])
            # Normalize anomaly score to [0, 100]
            norm_score = max(0.0, min(100.0, (raw_score - 0.4) * 200.0))

            if is_anomaly:
                # Calculate top feature deviations
                deviations = {}
                for f_idx, col in enumerate(feature_cols):
                    val = float(X[idx, f_idx])
                    z = (val - pop_means[f_idx]) / pop_stds[f_idx]
                    deviations[col] = round(float(z), 2)

                # Sort by absolute z-score
                sorted_devs = dict(sorted(deviations.items(), key=lambda item: abs(item[1]), reverse=True)[:4])

                findings_map[cse_id] = SupervisoryFinding(
                    finding_id=f"FND-{cse_id}-UNSUP01",
                    cse_id=cse_id,
                    detector_code="UNSUP-01",
                    detector_name="Multi-Dimensional Behavioral Outlier (Isolation Forest)",
                    paradigm="UNSUPERVISED",
                    capability_area="Cyber Resilience",
                    severity="HIGH" if norm_score > 70.0 else "MEDIUM",
                    anomaly_score=round(norm_score, 1),
                    evidence={
                        "raw_anomaly_score": round(raw_score, 4),
                        "top_deviating_features_z_scores": sorted_devs,
                    },
                    peer_baseline={
                        "population_feature_means": {
                            col: round(float(pop_means[f_idx]), 2) for f_idx, col in enumerate(feature_cols)
                        }
                    },
                    feature_contributions=sorted_devs,
                    supervisory_recommendation=(
                        f"Isolation Forest identified {cse_id} as a behavioral outlier across dimensions: "
                        f"{', '.join(sorted_devs.keys())}. Conduct cross-control audit."
                    ),
                )
            else:
                findings_map[cse_id] = None

        return findings_map

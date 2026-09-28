"""
8-Capability Area Scoring and Entity Risk Aggregation for SAT-SA.
Produces transparent, defensible composite risk scores with confidence intervals.
"""

from typing import Dict, List, Any, Optional, Tuple
import json
import numpy as np
import pandas as pd

from sat_sa.config import CAPABILITY_AREAS, CAPABILITY_WEIGHTS
from sat_sa.detectors.base import SupervisoryFinding
from sat_sa.detectors import (
    FastClosureDetector,
    TemplateNotesDetector,
    PreSLAGoodhartDetector,
    AnalystConcentrationDetector,
    MetricDiscrepancyDetector,
    SilentAssetsDetector,
    MissingCategoriesDetector,
    OrphanAlertsDetector,
    NightShiftSilenceDetector,
    UnsupervisedEntityAnomalyDetector,
)
from sat_sa.analytics.peer_benchmarking import PeerBenchmarkingEngine


class ScoringEngine:
    """
    Executes all detectors, maps findings to the 8 NCIIPC capability areas,
    and calculates composite entity risk scores.
    """

    def __init__(self):
        self.detectors = [
            FastClosureDetector(),
            TemplateNotesDetector(),
            PreSLAGoodhartDetector(),
            AnalystConcentrationDetector(),
            MetricDiscrepancyDetector(),
            SilentAssetsDetector(),
            MissingCategoriesDetector(),
            OrphanAlertsDetector(),
            NightShiftSilenceDetector(),
        ]
        self.unsup_detector = UnsupervisedEntityAnomalyDetector()
        self.peer_engine = PeerBenchmarkingEngine()

    def evaluate_all_entities(self, lake) -> Tuple[pd.DataFrame, Dict[str, List[SupervisoryFinding]]]:
        """
        Runs comprehensive analysis across all CSEs in the lake.
        Returns: (scores_df, findings_by_cse)
        """
        cse_ids = lake.get_cse_ids()
        peer_df = self.peer_engine.get_peer_groups(lake)
        peer_map = dict(zip(peer_df["cse_id"], peer_df["peer_group_id"])) if not peer_df.empty else {}

        # 1. Run Unsupervised Layer
        unsup_findings = self.unsup_detector.run_all(lake)

        all_findings_by_cse: Dict[str, List[SupervisoryFinding]] = {c: [] for c in cse_ids}
        entity_rows: List[Dict[str, Any]] = []

        # 2. Run Deterministic & Statistical Detectors for each CSE
        for cse_id in cse_ids:
            p_group = peer_map.get(cse_id, "GENERAL")
            cse_findings: List[SupervisoryFinding] = []

            for det in self.detectors:
                try:
                    fnds = det.run(lake, cse_id=cse_id, peer_group_id=p_group)
                    cse_findings.extend(fnds)
                except Exception as e:
                    print(f"Error running detector {det.code} on {cse_id}: {e}")

            # Append unsupervised finding if exists
            unsup_f = unsup_findings.get(cse_id)
            if unsup_f:
                cse_findings.append(unsup_f)

            all_findings_by_cse[cse_id] = cse_findings

            # 3. Calculate 8 Capability Sub-Scores [0 to 100]
            sub_scores: Dict[str, float] = {cap: 0.0 for cap in CAPABILITY_AREAS}
            for f in cse_findings:
                cap = f.capability_area
                # Finding penalty weighted by severity
                severity_mult = 1.0 if f.severity == "CRITICAL" else (0.75 if f.severity == "HIGH" else 0.45)
                sub_scores[cap] = min(100.0, sub_scores.get(cap, 0.0) + (f.anomaly_score * severity_mult))

            # Base baseline noise score (clean SOCs have ~8-15 baseline score)
            for cap in sub_scores:
                sub_scores[cap] = round(max(5.0, sub_scores[cap]), 1)

            # 4. Composite Entity Risk Score
            composite_score = sum(sub_scores[cap] * CAPABILITY_WEIGHTS.get(cap, 0.1) for cap in CAPABILITY_AREAS)
            composite_score = min(100.0, max(0.0, composite_score))

            # 5. Uncertainty / Confidence Band estimation (based on asset & alert sample volume)
            alert_vol_res = lake.query_df(f"SELECT count(*) as c FROM alerts WHERE cse_id = '{cse_id}'")
            alert_vol = int(alert_vol_res["c"].values[0]) if not alert_vol_res.empty else 0
            # Higher volume = smaller confidence margin (error band)
            margin = max(2.5, min(18.0, 45.0 / np.sqrt(max(10, alert_vol / 20.0))))

            entity_rows.append({
                "cse_id": cse_id,
                "peer_group_id": p_group,
                "total_findings": len(cse_findings),
                "critical_findings": sum(1 for f in cse_findings if f.severity == "CRITICAL"),
                "high_findings": sum(1 for f in cse_findings if f.severity == "HIGH"),
                "risk_score": round(composite_score, 1),
                "score_lower_bound": round(max(0.0, composite_score - margin), 1),
                "score_upper_bound": round(min(100.0, composite_score + margin), 1),
                "supervisory_status": "URGENT_INSPECTION" if composite_score >= 50.0 else ("MONITOR" if composite_score >= 25.0 else "SATISFACTORY"),
                **{f"score_{cap.lower().replace(' ', '_').replace('&', 'and')}": sub_scores[cap] for cap in CAPABILITY_AREAS},
            })

        default_cols = [
            "cse_id", "peer_group_id", "total_findings", "critical_findings",
            "high_findings", "risk_score", "score_lower_bound", "score_upper_bound",
            "supervisory_status", "rank"
        ] + [f"score_{cap.lower().replace(' ', '_').replace('&', 'and')}" for cap in CAPABILITY_AREAS]

        if not entity_rows:
            scores_df = pd.DataFrame(columns=default_cols)
        else:
            scores_df = pd.DataFrame(entity_rows)
            scores_df = scores_df.sort_values(by="risk_score", ascending=False).reset_index(drop=True)
            scores_df["rank"] = range(1, len(scores_df) + 1)


        # Persist to disk for instant UI rendering
        try:
            lake.write_table("scores", scores_df)
            findings_json_path = lake.lake_dir / "findings.json"
            serializable_findings = {
                cse: [f.to_dict() for f in f_list]
                for cse, f_list in all_findings_by_cse.items()
            }
            with open(findings_json_path, "w", encoding="utf-8") as fp:
                json.dump(serializable_findings, fp, indent=2)
        except Exception as e:
            print(f"Warning persisting scores: {e}")

        return scores_df, all_findings_by_cse

    def load_cached_evaluation(self, lake) -> Tuple[Optional[pd.DataFrame], Optional[Dict[str, List[SupervisoryFinding]]]]:
        """Loads precomputed evaluation from disk if available."""
        findings_json_path = lake.lake_dir / "findings.json"
        if not (lake.table_exists("scores") and findings_json_path.exists()):
            return None, None
        try:
            scores_df = lake.query_df("SELECT * FROM scores ORDER BY rank")
            with open(findings_json_path, "r", encoding="utf-8") as fp:
                raw_findings = json.load(fp)
            findings_map = {
                cse: [SupervisoryFinding(**f) for f in f_list]
                for cse, f_list in raw_findings.items()
            }
            return scores_df, findings_map
        except Exception:
            return None, None

"""
Negative-Space Detectors (NS-01 to NS-09) for SAT-SA.
Detects operational blind spots through expectation models: what SHOULD exist but is absent.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from scipy.stats import entropy

from sat_sa.detectors.base import BaseDetector, SupervisoryFinding
from sat_sa.config import DETECTOR_CONFIG


class SilentAssetsDetector(BaseDetector):
    """NS-01: Critical CII assets with zero alert telemetry over observation period."""

    def __init__(self):
        super().__init__(
            code="NS-01",
            name="Silent Critical CII Assets",
            capability_area="Threat Detection",
            paradigm="NEGATIVE_SPACE",
        )

    def run(self, lake, cse_id: str, peer_group_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> List[SupervisoryFinding]:
        query = f"""
            SELECT a.asset_id, a.asset_type, a.criticality_tier, count(alt.alert_id) as alert_count
            FROM assets a
            LEFT JOIN alerts alt ON a.asset_id = alt.asset_id
            WHERE a.cse_id = '{cse_id}'
            GROUP BY a.asset_id, a.asset_type, a.criticality_tier
        """
        df = lake.query_df(query)
        if df.empty:
            return []

        # Find silent Tier 1 Core CII assets
        silent_t1 = df[(df["criticality_tier"] == "TIER_1_CORE_CII") & (df["alert_count"] == 0)]
        total_t1 = df[df["criticality_tier"] == "TIER_1_CORE_CII"]
        
        # Peer rate on Tier 1
        peer_query = """
            SELECT median(alert_count) as peer_median_t1_alerts
            FROM (
                SELECT a.asset_id, count(alt.alert_id) as alert_count
                FROM assets a
                LEFT JOIN alerts alt ON a.asset_id = alt.asset_id
                WHERE a.criticality_tier = 'TIER_1_CORE_CII'
                GROUP BY a.asset_id
            )
        """
        peer_res = lake.query_df(peer_query)
        peer_t1_median = float(peer_res["peer_median_t1_alerts"].values[0]) if not peer_res.empty and peer_res["peer_median_t1_alerts"].values[0] is not None else 12.0

        findings = []
        if len(silent_t1) > 0:
            silent_ratio = len(silent_t1) / max(1, len(total_t1))
            severity = "CRITICAL" if len(silent_t1) >= 2 else "HIGH"
            score = min(100.0, silent_ratio * 120.0 + len(silent_t1) * 20.0)

            findings.append(SupervisoryFinding(
                finding_id=f"FND-{cse_id}-NS01",
                cse_id=cse_id,
                detector_code=self.code,
                detector_name=self.name,
                paradigm=self.paradigm,
                capability_area=self.capability_area,
                severity=severity,
                anomaly_score=round(score, 1),
                evidence={
                    "silent_tier1_count": len(silent_t1),
                    "total_tier1_count": len(total_t1),
                    "silent_tier1_asset_ids": silent_t1["asset_id"].tolist(),
                    "silent_asset_types": silent_t1["asset_type"].tolist(),
                },
                peer_baseline={
                    "peer_median_alerts_per_t1_asset": round(peer_t1_median, 1),
                    "peer_expected_silent_t1_count": 0,
                },
                supervisory_recommendation=(
                    f"{len(silent_t1)} Core CII (Tier 1) assets have ZERO alert telemetry in the audit window. "
                    "Audit SIEM connector health, endpoint agent installation, and syslog forwarding configurations for these assets."
                ),
            ))
        return findings


class MissingCategoriesDetector(BaseDetector):
    """NS-02: Missing alert categories / KL divergence against peer expectation."""

    def __init__(self):
        super().__init__(
            code="NS-02",
            name="Missing Core Alert Categories",
            capability_area="Threat Detection",
            paradigm="NEGATIVE_SPACE",
        )

    def run(self, lake, cse_id: str, peer_group_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> List[SupervisoryFinding]:
        # Entity category distribution
        entity_df = lake.query_df(f"""
            SELECT category, count(*) as cat_count
            FROM alerts
            WHERE cse_id = '{cse_id}'
            GROUP BY category
        """)

        # Peer category distribution
        peer_df = lake.query_df("""
            SELECT category, count(*) as cat_count
            FROM alerts
            GROUP BY category
        """)
        if peer_df.empty or entity_df.empty:
            return []

        all_cats = set(peer_df["category"].unique())
        peer_total = float(peer_df["cat_count"].sum())
        peer_dist = {r["category"]: r["cat_count"] / peer_total for _, r in peer_df.iterrows()}

        entity_total = float(entity_df["cat_count"].sum())
        entity_dist = {r["category"]: r["cat_count"] / entity_total for _, r in entity_df.iterrows()}

        # Identify missing categories that are common in peer baseline (> 5% of peer alerts)
        missing_critical_cats = [
            cat for cat, freq in peer_dist.items()
            if freq >= 0.05 and entity_dist.get(cat, 0.0) == 0.0
        ]

        # Compute KL Divergence (with Laplace smoothing)
        eps = 1e-5
        p = np.array([entity_dist.get(c, 0.0) + eps for c in all_cats])
        q = np.array([peer_dist.get(c, 0.0) + eps for c in all_cats])
        p /= p.sum()
        q /= q.sum()
        kl_div = float(entropy(p, q))

        findings = []
        if len(missing_critical_cats) > 0 or kl_div > 1.2:
            severity = "HIGH" if len(missing_critical_cats) >= 2 else "MEDIUM"
            score = min(100.0, len(missing_critical_cats) * 35.0 + kl_div * 15.0)

            findings.append(SupervisoryFinding(
                finding_id=f"FND-{cse_id}-NS02",
                cse_id=cse_id,
                detector_code=self.code,
                detector_name=self.name,
                paradigm=self.paradigm,
                capability_area=self.capability_area,
                severity=severity,
                anomaly_score=round(score, 1),
                evidence={
                    "missing_categories": missing_critical_cats,
                    "kl_divergence": round(kl_div, 3),
                    "entity_category_count": len(entity_df),
                    "peer_category_count": len(all_cats),
                },
                peer_baseline={
                    "peer_expected_category_coverage": 12,
                    "peer_expected_share_for_missing": {
                        c: f"{round(peer_dist[c]*100, 1)}%" for c in missing_critical_cats
                    },
                },
                supervisory_recommendation=(
                    f"Entity has 0 alerts in key categories: {', '.join(missing_critical_cats)} (KL divergence = {round(kl_div,2)}). "
                    "Indicates rule degradation, disabled SIEM use-cases, or unmonitored log sources."
                ),
            ))
        return findings


class OrphanAlertsDetector(BaseDetector):
    """NS-04: High and Critical alerts with no case investigation created."""

    def __init__(self):
        super().__init__(
            code="NS-04",
            name="Orphan Critical Alerts (No Case)",
            capability_area="Investigation",
            paradigm="NEGATIVE_SPACE",
        )

    def run(self, lake, cse_id: str, peer_group_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> List[SupervisoryFinding]:
        query = f"""
            SELECT alt.alert_id, alt.severity, alt.rule_name, c.case_id
            FROM alerts alt
            LEFT JOIN cases c ON alt.alert_id = c.alert_id
            WHERE alt.cse_id = '{cse_id}'
              AND alt.severity IN ('HIGH', 'CRITICAL')
        """
        df = lake.query_df(query)
        if df.empty:
            return []

        orphan_df = df[df["case_id"].isnull()]
        orphan_ratio = len(orphan_df) / max(1, len(df))

        findings = []
        if orphan_ratio > 0.25 and len(orphan_df) >= 5:
            severity = "HIGH" if orphan_ratio > 0.50 else "MEDIUM"
            findings.append(SupervisoryFinding(
                finding_id=f"FND-{cse_id}-NS04",
                cse_id=cse_id,
                detector_code=self.code,
                detector_name=self.name,
                paradigm=self.paradigm,
                capability_area=self.capability_area,
                severity=severity,
                anomaly_score=round(min(100.0, orphan_ratio * 120.0), 1),
                evidence={
                    "orphan_critical_high_count": len(orphan_df),
                    "total_critical_high_count": len(df),
                    "orphan_ratio": round(orphan_ratio, 3),
                    "sample_orphan_alert_ids": orphan_df["alert_id"].head(10).tolist(),
                },
                peer_baseline={
                    "peer_expected_orphan_rate": "< 0.05",
                },
                supervisory_recommendation=(
                    f"{len(orphan_df)} High/Critical alerts ({round(orphan_ratio*100, 1)}%) were closed without opening an investigation case. "
                    "Review why critical alerts bypassed case management workflows."
                ),
            ))
        return findings


class NightShiftSilenceDetector(BaseDetector):
    """NS-07: Time-series operational silence during night shifts (00:00 - 08:00)."""

    def __init__(self):
        super().__init__(
            code="NS-07",
            name="Night-Shift Operational Silence",
            capability_area="Security Operations",
            paradigm="NEGATIVE_SPACE",
        )

    def run(self, lake, cse_id: str, peer_group_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> List[SupervisoryFinding]:
        query = f"""
            SELECT hour(created_at) as alert_hour, count(*) as count
            FROM alerts
            WHERE cse_id = '{cse_id}'
            GROUP BY hour(created_at)
        """
        df = lake.query_df(query)
        if df.empty:
            return []

        hours_dict = {int(r["alert_hour"]): r["count"] for _, r in df.iterrows()}
        night_alerts = sum(hours_dict.get(h, 0) for h in range(0, 8))
        total_alerts = sum(hours_dict.values())
        night_ratio = night_alerts / max(1, total_alerts)

        findings = []
        # Expected ~25% of alerts occur between 00:00 and 08:00 (1/3 of day)
        if night_ratio < 0.05 and total_alerts > 50:
            findings.append(SupervisoryFinding(
                finding_id=f"FND-{cse_id}-NS07",
                cse_id=cse_id,
                detector_code=self.code,
                detector_name=self.name,
                paradigm=self.paradigm,
                capability_area=self.capability_area,
                severity="MEDIUM",
                anomaly_score=round(min(100.0, (0.25 - night_ratio) * 350.0), 1),
                evidence={
                    "night_alerts_count": night_alerts,
                    "total_alerts_count": total_alerts,
                    "night_ratio": round(night_ratio, 3),
                },
                peer_baseline={
                    "peer_expected_night_ratio": "~0.25",
                },
                supervisory_recommendation=(
                    f"Only {round(night_ratio*100, 1)}% of alerts occurred during night hours (00:00–08:00). "
                    "Verify actual 24/7 SOC staffing presence and telemetry ingestion continuity."
                ),
            ))
        return findings

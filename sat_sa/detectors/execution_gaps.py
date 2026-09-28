"""
Execution-Gap Detectors (EG-01 to EG-11) for SAT-SA.
Surfaces behavioral evidence where operational execution contradicts effective SOC claims.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from datetime import datetime

from sat_sa.detectors.base import BaseDetector, SupervisoryFinding
from sat_sa.detectors.template_similarity import TemplateNoteAnalyzer
from sat_sa.config import DETECTOR_CONFIG


class FastClosureDetector(BaseDetector):
    """EG-01: Critical/High alerts closed unusually fast (< 180 seconds)."""

    def __init__(self):
        super().__init__(
            code="EG-01",
            name="Fast-Closure on Critical Alerts",
            capability_area="Investigation",
            paradigm="EXECUTION_GAP",
        )

    def run(self, lake, cse_id: str, peer_group_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> List[SupervisoryFinding]:
        cfg = config or DETECTOR_CONFIG
        crit_thresh = cfg.get("eg01_fast_close_critical_seconds", 180.0)
        
        query = f"""
            SELECT alert_id, severity, rule_name, analyst_id,
                   epoch(closed_at) - epoch(created_at) as duration_seconds
            FROM alerts
            WHERE cse_id = '{cse_id}'
              AND severity IN ('CRITICAL', 'HIGH')
              AND closed_at IS NOT NULL
        """
        df = lake.query_df(query)
        if df.empty:
            return []

        fast_alerts = df[df["duration_seconds"] < crit_thresh]
        fast_ratio = len(fast_alerts) / max(1, len(df))

        # Query peer median for baseline
        peer_query = f"""
            SELECT median(epoch(closed_at) - epoch(created_at)) as peer_median_sec
            FROM alerts
            WHERE severity IN ('CRITICAL', 'HIGH')
              AND closed_at IS NOT NULL
        """
        peer_res = lake.query_df(peer_query)
        peer_median = float(peer_res["peer_median_sec"].values[0]) if not peer_res.empty and peer_res["peer_median_sec"].values[0] is not None else 1800.0

        findings = []
        if fast_ratio > 0.15 or len(fast_alerts) >= 5:
            severity = "CRITICAL" if fast_ratio > 0.40 else "HIGH"
            score = min(100.0, fast_ratio * 150.0)
            
            findings.append(SupervisoryFinding(
                finding_id=f"FND-{cse_id}-EG01",
                cse_id=cse_id,
                detector_code=self.code,
                detector_name=self.name,
                paradigm=self.paradigm,
                capability_area=self.capability_area,
                severity=severity,
                anomaly_score=round(score, 1),
                evidence={
                    "fast_closed_count": len(fast_alerts),
                    "total_crit_high_count": len(df),
                    "fast_closed_ratio": round(fast_ratio, 3),
                    "sample_alert_ids": fast_alerts["alert_id"].head(10).tolist(),
                    "median_duration_seconds": round(float(df["duration_seconds"].median()), 1),
                },
                peer_baseline={
                    "peer_median_duration_seconds": round(peer_median, 1),
                    "peer_expected_fast_close_rate": "< 0.05",
                },
                supervisory_recommendation=(
                    f"Sample and audit the {len(fast_alerts)} High/Critical alerts closed in under {crit_thresh}s. "
                    "Verify if automated playbooks were authorized or if triage was rubber-stamped without forensic review."
                ),
            ))
        return findings


class TemplateNotesDetector(BaseDetector):
    """EG-04: Template-driven boilerplate closure notes (MinHash / LSH)."""

    def __init__(self):
        super().__init__(
            code="EG-04",
            name="Template-Driven Boilerplate Notes",
            capability_area="Operational Discipline",
            paradigm="EXECUTION_GAP",
        )
        self.analyzer = TemplateNoteAnalyzer()

    def run(self, lake, cse_id: str, peer_group_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> List[SupervisoryFinding]:
        cases_df = lake.query_df(f"SELECT case_id, analyst_id, closure_note FROM cases WHERE cse_id = '{cse_id}'")
        analysis = self.analyzer.analyze_cases(cases_df)

        findings = []
        if analysis["duplicate_ratio"] > 0.25 and analysis["total_clustered_cases"] >= 6:
            severity = "HIGH" if analysis["duplicate_ratio"] > 0.60 else "MEDIUM"
            score = min(100.0, analysis["duplicate_ratio"] * 120.0)

            findings.append(SupervisoryFinding(
                finding_id=f"FND-{cse_id}-EG04",
                cse_id=cse_id,
                detector_code=self.code,
                detector_name=self.name,
                paradigm=self.paradigm,
                capability_area=self.capability_area,
                severity=severity,
                anomaly_score=round(score, 1),
                evidence={
                    "duplicate_ratio": analysis["duplicate_ratio"],
                    "total_clustered_cases": analysis["total_clustered_cases"],
                    "cluster_count": analysis["cluster_count"],
                    "sample_boilerplate": analysis["sample_boilerplate"],
                },
                peer_baseline={
                    "peer_median_duplicate_ratio": 0.08,
                    "peer_acceptable_threshold": "< 0.20",
                },
                supervisory_recommendation=(
                    f"{round(analysis['duplicate_ratio']*100, 1)}% of cases exhibit copy-paste boilerplate notes. "
                    "Interview lead analysts to verify whether investigations follow standard operating procedures or superficial logging."
                ),
            ))
        return findings


class PreSLAGoodhartDetector(BaseDetector):
    """EG-06: Pre-SLA Goodhart deadline gaming (clustering right before 60-min deadline)."""

    def __init__(self):
        super().__init__(
            code="EG-06",
            name="Pre-SLA Metric Gaming",
            capability_area="Operational Discipline",
            paradigm="EXECUTION_GAP",
        )

    def run(self, lake, cse_id: str, peer_group_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> List[SupervisoryFinding]:
        query = f"""
            SELECT alert_id,
                   (epoch(closed_at) - epoch(created_at)) / 60.0 as duration_minutes
            FROM alerts
            WHERE cse_id = '{cse_id}' AND closed_at IS NOT NULL
        """
        df = lake.query_df(query)
        if len(df) < 20:
            return []

        # Check concentration between 50 and 60 minutes
        pre_sla = df[(df["duration_minutes"] >= 50.0) & (df["duration_minutes"] <= 60.0)]
        ratio = len(pre_sla) / max(1, len(df))

        findings = []
        if ratio > 0.35:
            severity = "HIGH" if ratio > 0.60 else "MEDIUM"
            findings.append(SupervisoryFinding(
                finding_id=f"FND-{cse_id}-EG06",
                cse_id=cse_id,
                detector_code=self.code,
                detector_name=self.name,
                paradigm=self.paradigm,
                capability_area=self.capability_area,
                severity=severity,
                anomaly_score=round(min(100.0, ratio * 130.0), 1),
                evidence={
                    "pre_sla_closures": len(pre_sla),
                    "total_closures": len(df),
                    "pre_sla_ratio": round(ratio, 3),
                    "sample_alert_ids": pre_sla["alert_id"].head(10).tolist(),
                },
                peer_baseline={
                    "peer_expected_ratio_50_60min": 0.05,
                    "anomaly_lift": round(ratio / 0.05, 1),
                },
                supervisory_recommendation=(
                    f"Abnormal concentration of alert closures ({round(ratio*100, 1)}%) in the 50-60 min window. "
                    "Indicates artificial batch closure to meet SLA KPIs without genuine investigation depth."
                ),
            ))
        return findings


class AnalystConcentrationDetector(BaseDetector):
    """EG-09: Analyst workload Gini concentration."""

    def __init__(self):
        super().__init__(
            code="EG-09",
            name="Analyst Workload Concentration",
            capability_area="Security Operations",
            paradigm="EXECUTION_GAP",
        )

    def _gini(self, array: np.ndarray) -> float:
        array = np.sort(array)
        index = np.arange(1, array.shape[0] + 1)
        n = array.shape[0]
        return float((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array) + 1e-8))

    def run(self, lake, cse_id: str, peer_group_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> List[SupervisoryFinding]:
        query = f"""
            SELECT analyst_id, count(*) as alert_count
            FROM alerts
            WHERE cse_id = '{cse_id}' AND analyst_id IS NOT NULL
            GROUP BY analyst_id
        """
        df = lake.query_df(query)
        if len(df) < 2:
            return []

        counts = df["alert_count"].values.astype(float)
        gini = self._gini(counts)
        top_analyst = df.sort_values(by="alert_count", ascending=False).iloc[0]
        top_ratio = top_analyst["alert_count"] / float(counts.sum())

        findings = []
        if gini > 0.65 or top_ratio > 0.70:
            severity = "HIGH" if top_ratio > 0.80 else "MEDIUM"
            findings.append(SupervisoryFinding(
                finding_id=f"FND-{cse_id}-EG09",
                cse_id=cse_id,
                detector_code=self.code,
                detector_name=self.name,
                paradigm=self.paradigm,
                capability_area=self.capability_area,
                severity=severity,
                anomaly_score=round(min(100.0, gini * 110.0), 1),
                evidence={
                    "gini_coefficient": round(gini, 3),
                    "top_analyst_id": str(top_analyst["analyst_id"]),
                    "top_analyst_share": round(top_ratio, 3),
                    "total_analysts": len(df),
                },
                peer_baseline={
                    "peer_median_gini": 0.28,
                    "peer_acceptable_gini": "< 0.50",
                },
                supervisory_recommendation=(
                    f"Analyst {top_analyst['analyst_id']} closed {round(top_ratio*100, 1)}% of all entity alerts (Gini={round(gini,2)}). "
                    "Suggests single-point-of-failure risk, shift fatigue, or automated credential sharing."
                ),
            ))
        return findings


class MetricDiscrepancyDetector(BaseDetector):
    """EG-11: Claim-vs-Evidence metric reconciliation."""

    def __init__(self):
        super().__init__(
            code="EG-11",
            name="Claim-vs-Evidence Metric Discrepancy",
            capability_area="Governance & Oversight",
            paradigm="EXECUTION_GAP",
        )

    def run(self, lake, cse_id: str, peer_group_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> List[SupervisoryFinding]:
        self_metric = lake.query_df(f"SELECT * FROM self_assessed_metrics WHERE cse_id = '{cse_id}'")
        if self_metric.empty:
            return []

        rep_row = self_metric.iloc[0]
        rep_mttr = float(rep_row["reported_mttr_minutes"])

        obs_res = lake.query_df(f"""
            SELECT median((epoch(closed_at) - epoch(created_at)) / 60.0) as obs_mttr
            FROM alerts
            WHERE cse_id = '{cse_id}' AND closed_at IS NOT NULL
        """)
        if obs_res.empty or obs_res["obs_mttr"].values[0] is None:
            return []

        obs_mttr = float(obs_res["obs_mttr"].values[0])
        gap = abs(obs_mttr - rep_mttr)
        ratio = obs_mttr / max(0.1, rep_mttr)

        findings = []
        if ratio > 2.5 and gap > 20.0:
            findings.append(SupervisoryFinding(
                finding_id=f"FND-{cse_id}-EG11",
                cse_id=cse_id,
                detector_code=self.code,
                detector_name=self.name,
                paradigm=self.paradigm,
                capability_area=self.capability_area,
                severity="HIGH",
                anomaly_score=round(min(100.0, ratio * 25.0), 1),
                evidence={
                    "reported_mttr_minutes": round(rep_mttr, 1),
                    "observed_mttr_minutes": round(obs_mttr, 1),
                    "discrepancy_factor": round(ratio, 1),
                    "absolute_gap_minutes": round(gap, 1),
                },
                peer_baseline={
                    "peer_median_mttr_minutes": 35.0,
                    "acceptable_discrepancy_margin": "± 20%",
                },
                supervisory_recommendation=(
                    f"Self-assessed MTTR is {round(rep_mttr,1)} min, whereas actual observed telemetry MTTR is {round(obs_mttr,1)} min "
                    f"({round(ratio,1)}x discrepancy). Request formal justification for supervisory reporting inaccuracies."
                ),
            ))
        return findings

"""
Data Quality Completeness Gate & Schema Validation for SAT-SA.
Evaluates data completeness, null-rates, timestamp sanity, and referential integrity.
Missing or corrupted data itself surfaces as a supervisory finding.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np


class DataQualityGate:
    """
    Validates submission completeness and integrity across all canonical tables.
    """

    def evaluate_cse_data_quality(
        self,
        cse_id: str,
        alerts_df: pd.DataFrame,
        cases_df: pd.DataFrame,
        escalations_df: pd.DataFrame,
        assets_df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Runs comprehensive data quality checks and returns a quality report + score [0-100].
        """
        checks: List[Dict[str, Any]] = []
        penalties = 0.0

        # Filter for CSE
        c_alerts = alerts_df[alerts_df["cse_id"] == cse_id] if not alerts_df.empty else pd.DataFrame()
        c_cases = cases_df[cases_df["cse_id"] == cse_id] if not cases_df.empty else pd.DataFrame()
        c_escalations = escalations_df[escalations_df["cse_id"] == cse_id] if not escalations_df.empty else pd.DataFrame()
        c_assets = assets_df[assets_df["cse_id"] == cse_id] if not assets_df.empty else pd.DataFrame()

        # Check 1: Record volume presence
        if len(c_alerts) == 0:
            checks.append({"check": "Alert Volume", "status": "FAIL", "msg": "Zero alert records submitted"})
            penalties += 40.0
        else:
            checks.append({"check": "Alert Volume", "status": "PASS", "msg": f"{len(c_alerts)} alerts submitted"})

        if len(c_assets) == 0:
            checks.append({"check": "Asset Inventory", "status": "FAIL", "msg": "Zero assets declared in inventory"})
            penalties += 25.0
        else:
            checks.append({"check": "Asset Inventory", "status": "PASS", "msg": f"{len(c_assets)} assets registered"})

        # Check 2: Null rate on critical fields
        if not c_alerts.empty:
            critical_nulls = c_alerts[["alert_id", "created_at", "severity", "category", "asset_id"]].isnull().sum().sum()
            if critical_nulls > 0:
                checks.append({"check": "Alert Mandatory Fields", "status": "WARN", "msg": f"{critical_nulls} null mandatory values detected"})
                penalties += min(15.0, critical_nulls * 0.5)
            else:
                checks.append({"check": "Alert Mandatory Fields", "status": "PASS", "msg": "100% mandatory fields populated"})

            # Check 3: Timestamp consistency (closed_at >= created_at)
            time_anomalies = (pd.to_datetime(c_alerts["closed_at"]) < pd.to_datetime(c_alerts["created_at"])).sum()
            if time_anomalies > 0:
                checks.append({"check": "Timestamp Sanity", "status": "FAIL", "msg": f"{time_anomalies} records have closed_at before created_at!"})
                penalties += min(20.0, time_anomalies * 2.0)
            else:
                checks.append({"check": "Timestamp Sanity", "status": "PASS", "msg": "Chronological timeline valid"})

        # Check 4: Referential integrity (case alert_id exists in alerts)
        if not c_cases.empty and not c_alerts.empty:
            valid_alert_ids = set(c_alerts["alert_id"])
            orphan_case_alerts = c_cases[c_cases["alert_id"].notnull() & ~c_cases["alert_id"].isin(valid_alert_ids)]
            if len(orphan_case_alerts) > 0:
                checks.append({"check": "Case-Alert Foreign Key", "status": "WARN", "msg": f"{len(orphan_case_alerts)} cases reference non-existent alerts"})
                penalties += min(15.0, len(orphan_case_alerts) * 1.0)
            else:
                checks.append({"check": "Case-Alert Foreign Key", "status": "PASS", "msg": "Referential integrity intact"})

        # Check 5: Asset foreign key in alerts
        if not c_alerts.empty and not c_assets.empty:
            valid_asset_ids = set(c_assets["asset_id"])
            unregistered_assets = c_alerts[~c_alerts["asset_id"].isin(valid_asset_ids)]
            if len(unregistered_assets) > 0:
                checks.append({"check": "Alert Asset Registry", "status": "WARN", "msg": f"{len(unregistered_assets)} alerts on undeclared shadow assets"})
                penalties += min(15.0, len(unregistered_assets) * 0.2)
            else:
                checks.append({"check": "Alert Asset Registry", "status": "PASS", "msg": "All alert assets exist in inventory"})

        quality_score = max(0.0, min(100.0, 100.0 - penalties))

        return {
            "cse_id": cse_id,
            "data_quality_score": round(quality_score, 1),
            "status": "APPROVED" if quality_score >= 80.0 else ("CONDITIONAL" if quality_score >= 50.0 else "REJECTED"),
            "checks": checks,
            "metrics": {
                "alert_count": len(c_alerts),
                "case_count": len(c_cases),
                "escalation_count": len(c_escalations),
                "asset_count": len(c_assets),
            },
        }

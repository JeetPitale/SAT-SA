"""
Realistic Multi-Entity Synthetic SOC Generator & Fault-Injection Engine for SAT-SA.
Generates full audit-ready datasets across critical sectors with ground-truth operational faults.
"""

import random
import uuid
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Tuple, Any, Optional

from sat_sa.config import SECTORS
from sat_sa.generator.taxonomy import (
    ALERT_CATEGORIES,
    RULES_CATALOGUE,
    ASSET_TIERS,
    ASSET_TYPES,
    LEGITIMATE_NOTE_TEMPLATES,
    BOILERPLATE_RUBBER_STAMP_NOTES,
)


class SyntheticSOCGenerator:
    """
    Generates multi-CSE SOC datasets with realistic baseline distributions and
    controlled injection of operational anomalies (Execution Gaps & Negative Space).
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)

    def generate_all(
        self,
        num_cses: int = 16,
        days: int = 60,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, pd.DataFrame]:
        """Generates all 6 canonical tables plus ground truth faults."""
        if end_date is None:
            end_date = datetime(2026, 9, 20, 18, 0, 0, tzinfo=timezone.utc)
        start_date = end_date - timedelta(days=days)

        cse_profiles = self._create_cse_profiles(num_cses)
        all_assets: List[Dict[str, Any]] = []
        all_analysts: List[Dict[str, Any]] = []
        all_alerts: List[Dict[str, Any]] = []
        all_cases: List[Dict[str, Any]] = []
        all_escalations: List[Dict[str, Any]] = []
        all_self_assessed: List[Dict[str, Any]] = []
        all_ground_truths: List[Dict[str, Any]] = []

        # 1. Create Assets & Analysts for each CSE
        for profile in cse_profiles:
            cse_id = profile["cse_id"]
            assets = self._generate_assets(profile, start_date, end_date)
            analysts = self._generate_analysts(profile, start_date)
            all_assets.extend(assets)
            all_analysts.extend(analysts)

        # 2. Plan Fault Injections
        fault_plan = self._assign_fault_plans(cse_profiles)

        # 3. Generate Alerts, Cases, Escalations per CSE according to fault plan
        for profile in cse_profiles:
            cse_id = profile["cse_id"]
            cse_assets = [a for a in all_assets if a["cse_id"] == cse_id]
            cse_analysts = [a for a in all_analysts if a["cse_id"] == cse_id]
            cse_faults = fault_plan.get(cse_id, [])

            alerts, cases, escalations, self_metric, gt_records = self._generate_cse_telemetry(
                profile, cse_assets, cse_analysts, cse_faults, start_date, end_date
            )

            all_alerts.extend(alerts)
            all_cases.extend(cases)
            all_escalations.extend(escalations)
            all_self_assessed.append(self_metric)
            all_ground_truths.extend(gt_records)

        return {
            "assets": pd.DataFrame(all_assets),
            "analysts": pd.DataFrame(all_analysts),
            "alerts": pd.DataFrame(all_alerts),
            "cases": pd.DataFrame(all_cases),
            "escalations": pd.DataFrame(all_escalations),
            "self_assessed_metrics": pd.DataFrame(all_self_assessed),
            "ground_truth_faults": pd.DataFrame(all_ground_truths) if all_ground_truths else pd.DataFrame(columns=["cse_id", "fault_category", "fault_code", "description", "injected_at", "strength"]),
        }

    def _create_cse_profiles(self, num_cses: int) -> List[Dict[str, Any]]:
        profiles = []
        sectors_cycle = SECTORS * 3
        sizes = ["SMALL", "MEDIUM", "LARGE"]
        
        for i in range(1, num_cses + 1):
            sector = sectors_cycle[i - 1]
            size = sizes[(i - 1) % len(sizes)]
            asset_count = 45 if size == "SMALL" else (120 if size == "MEDIUM" else 280)
            analyst_count = 4 if size == "SMALL" else (9 if size == "MEDIUM" else 18)
            
            profiles.append({
                "cse_id": f"CSE-{i:03d}",
                "cse_name": f"{sector.split()[0]}-National-Entity-{i}",
                "sector": sector,
                "size_category": size,
                "asset_count": asset_count,
                "analyst_count": analyst_count,
            })
        return profiles

    def _assign_fault_plans(self, profiles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Assigns distinct fault archetypes to select entities to form the ground-truth benchmark.
        Entity 1 to 5: Clean / Healthy benchmark CSEs
        Entity 6 to 14: Distinct Execution Gap & Negative Space faults
        Entity 15 to 16: Multi-fault composite systemic failures
        """
        plan = {}
        # CSE-001 to CSE-005 are clean control group
        for i in range(1, 6):
            plan[f"CSE-{i:03d}"] = []

        # CSE-006: EG-01 Fast Closure on Criticals
        plan["CSE-006"] = [{
            "code": "EG_01_FAST_CLOSE",
            "category": "EXECUTION_GAP",
            "desc": "Critical & High alerts closed in < 90 seconds without investigation",
            "strength": 0.85,
        }]

        # CSE-007: EG-04 Template / Rubber-Stamp Closure Notes
        plan["CSE-007"] = [{
            "code": "EG_04_TEMPLATE_NOTES",
            "category": "EXECUTION_GAP",
            "desc": "High copy-paste boilerplate notes across analysts with >90% text similarity",
            "strength": 0.90,
        }]

        # CSE-008: EG-06 Pre-SLA Goodhart Deadline Gaming
        plan["CSE-008"] = [{
            "code": "EG_06_PRE_SLA_GAMING",
            "category": "EXECUTION_GAP",
            "desc": "80% of alert closures clustered within 5 minutes before the 60-min SLA timer",
            "strength": 0.80,
        }]

        # CSE-009: EG-09 Analyst Workload Concentration (Gini)
        plan["CSE-009"] = [{
            "code": "EG_09_ANALYST_CONCENTRATION",
            "category": "EXECUTION_GAP",
            "desc": "Single analyst handles 88% of all alert closures while others remain idle",
            "strength": 0.88,
        }]

        # CSE-010: EG-11 Metric Gap (Reported vs Observed)
        plan["CSE-010"] = [{
            "code": "EG_11_METRIC_DISCREPANCY",
            "category": "EXECUTION_GAP",
            "desc": "Self-assessment reports 15 min MTTR and 99% coverage, actual observed is 170 min",
            "strength": 0.75,
        }]

        # CSE-011: NS-01 Silent Critical CII Assets
        plan["CSE-011"] = [{
            "code": "NS_01_SILENT_ASSET",
            "category": "NEGATIVE_SPACE",
            "desc": "Core Tier 1 SCADA / Domain Controller assets show zero telemetry for >30 days",
            "strength": 0.90,
        }]

        # CSE-012: NS-02 Missing Entire Alert Categories
        plan["CSE-012"] = [{
            "code": "NS_02_MISSING_CATEGORY",
            "category": "NEGATIVE_SPACE",
            "desc": "Authentication Anomaly and Privilege Escalation categories have 0 alerts",
            "strength": 0.95,
        }]

        # CSE-013: NS-04 Orphan Critical Alerts (No Case Investigation)
        plan["CSE-013"] = [{
            "code": "NS_04_ORPHAN_ALERTS",
            "category": "NEGATIVE_SPACE",
            "desc": "High and Critical severity alerts closed without linking to an investigation case",
            "strength": 0.70,
        }]

        # CSE-014: NS-07 Night-Shift Operational Blackout
        plan["CSE-014"] = [{
            "code": "NS_07_NIGHT_SILENCE",
            "category": "NEGATIVE_SPACE",
            "desc": "Complete silence / zero alert processing between 00:00 and 08:00 despite 24/7 claim",
            "strength": 0.85,
        }]

        # CSE-015: Composite - Fast Close + Silent Assets (Severely Compromised SOC)
        plan["CSE-015"] = [
            {"code": "EG_01_FAST_CLOSE", "category": "EXECUTION_GAP", "desc": "Fast closure on criticals", "strength": 0.90},
            {"code": "NS_01_SILENT_ASSET", "category": "NEGATIVE_SPACE", "desc": "Silent core CII assets", "strength": 0.85},
            {"code": "EG_04_TEMPLATE_NOTES", "category": "EXECUTION_GAP", "desc": "Template notes", "strength": 0.75},
        ]

        # CSE-016: Composite - Pre-SLA Gaming + Missing Categories + Metric Gap
        plan["CSE-016"] = [
            {"code": "EG_06_PRE_SLA_GAMING", "category": "EXECUTION_GAP", "desc": "Pre-SLA gaming", "strength": 0.80},
            {"code": "NS_02_MISSING_CATEGORY", "category": "NEGATIVE_SPACE", "desc": "Missing categories", "strength": 0.90},
            {"code": "EG_11_METRIC_DISCREPANCY", "category": "EXECUTION_GAP", "desc": "Metric falsification", "strength": 0.80},
        ]

        return plan

    def _generate_assets(
        self, profile: Dict[str, Any], start_date: datetime, end_date: datetime
    ) -> List[Dict[str, Any]]:
        assets = []
        cse_id = profile["cse_id"]
        count = profile["asset_count"]
        sector = profile["sector"]

        for i in range(1, count + 1):
            asset_type = ASSET_TYPES[(i - 1) % len(ASSET_TYPES)]
            # Tier assignment: first 15% Tier 1, next 35% Tier 2, rest Tier 3
            if i <= max(2, int(count * 0.15)):
                tier = "TIER_1_CORE_CII"
            elif i <= int(count * 0.50):
                tier = "TIER_2_OPERATIONAL"
            else:
                tier = "TIER_3_SUPPORT"

            env = "PROD_OT" if ("SCADA" in asset_type or "PLC" in asset_type or "Historian" in asset_type) else "PROD_IT"
            first_seen = start_date - timedelta(days=random.randint(100, 400))
            last_seen = end_date - timedelta(hours=random.randint(0, 12))

            assets.append({
                "asset_id": f"{cse_id}-AST-{i:04d}",
                "cse_id": cse_id,
                "asset_type": asset_type,
                "criticality_tier": tier,
                "sector": sector,
                "environment": env,
                "first_seen": first_seen,
                "last_seen_in_telemetry": last_seen,
            })
        return assets

    def _generate_analysts(
        self, profile: Dict[str, Any], start_date: datetime
    ) -> List[Dict[str, Any]]:
        analysts = []
        cse_id = profile["cse_id"]
        count = profile["analyst_count"]
        names = ["Aarav", "Aditi", "Rohan", "Priya", "Vikram", "Neha", "Sanjay", "Ananya", "Rahul", "Pooja", "Karan", "Sneha"]

        for i in range(1, count + 1):
            name = f"{names[(i - 1) % len(names)]} {chr(65 + (i % 26))}."
            shift = "DAY_SHIFT" if i % 3 == 1 else ("NIGHT_SHIFT" if i % 3 == 2 else "ROTATIONAL")
            role = "IR_LEAD" if i == 1 else ("T2_INVESTIGATOR" if i <= 3 else "T1_TRIAGE")
            join_date = start_date - timedelta(days=random.randint(180, 800))

            analysts.append({
                "analyst_id": f"{cse_id}-ANA-{i:02d}",
                "cse_id": cse_id,
                "analyst_name": name,
                "shift": shift,
                "role": role,
                "join_date": join_date,
            })
        return analysts

    def _generate_cse_telemetry(
        self,
        profile: Dict[str, Any],
        assets: List[Dict[str, Any]],
        analysts: List[Dict[str, Any]],
        faults: List[Dict[str, Any]],
        start_date: datetime,
        end_date: datetime,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], List[Dict[str, Any]]]:
        cse_id = profile["cse_id"]
        fault_codes = {f["code"]: f for f in faults}

        # Calculate base alert volume: ~1.8 alerts per asset per day on average
        base_daily_rate = profile["asset_count"] * 1.5
        total_expected_alerts = int(base_daily_rate * ((end_date - start_date).days))

        alerts: List[Dict[str, Any]] = []
        cases: List[Dict[str, Any]] = []
        escalations: List[Dict[str, Any]] = []
        gt_records: List[Dict[str, Any]] = []

        # Identify silent assets if NS_01 is active
        silent_asset_ids = set()
        if "NS_01_SILENT_ASSET" in fault_codes:
            # Pick 2-4 Tier 1 Core CII assets
            tier1 = [a["asset_id"] for a in assets if a["criticality_tier"] == "TIER_1_CORE_CII"]
            silent_asset_ids = set(random.sample(tier1, min(len(tier1), 3)))
            gt_records.append({
                "cse_id": cse_id,
                "fault_code": "NS_01_SILENT_ASSET",
                "fault_category": "NEGATIVE_SPACE",
                "description": fault_codes["NS_01_SILENT_ASSET"]["desc"],
                "severity_strength": fault_codes["NS_01_SILENT_ASSET"]["strength"],
                "affected_asset_ids": list(silent_asset_ids),
                "affected_alert_ids": [],
                "affected_analyst_ids": [],
            })

        # Identify excluded categories if NS_02 is active
        excluded_categories = set()
        if "NS_02_MISSING_CATEGORY" in fault_codes:
            excluded_categories = {"Authentication Anomaly", "Privileged Account Abuse"}
            gt_records.append({
                "cse_id": cse_id,
                "fault_code": "NS_02_MISSING_CATEGORY",
                "fault_category": "NEGATIVE_SPACE",
                "description": fault_codes["NS_02_MISSING_CATEGORY"]["desc"],
                "severity_strength": fault_codes["NS_02_MISSING_CATEGORY"]["strength"],
                "affected_asset_ids": [],
                "affected_alert_ids": [],
                "affected_analyst_ids": [],
            })

        # Fault tracking lists
        fast_closed_alert_ids = []
        template_case_ids = []
        pre_sla_alert_ids = []
        orphan_alert_ids = []
        bulk_alert_ids = []

        primary_analyst_id = analysts[0]["analyst_id"]

        # Generate alerts across time window
        current_time = start_date
        total_seconds = int((end_date - start_date).total_seconds())

        for idx in range(1, total_expected_alerts + 1):
            # Diurnal & weekly arrival distribution
            sec_offset = random.randint(0, total_seconds)
            alert_time = start_date + timedelta(seconds=sec_offset)

            # Check if night silence fault applies
            if "NS_07_NIGHT_SILENCE" in fault_codes:
                hour = alert_time.hour
                if 0 <= hour < 8 and random.random() < 0.90:
                    continue  # suppress alerts during night shift

            # Select asset (excluding silent assets if fault active)
            candidate_assets = [a for a in assets if a["asset_id"] not in silent_asset_ids]
            if not candidate_assets:
                candidate_assets = assets
            asset = random.choice(candidate_assets)

            # Select rule / category (excluding categories if fault active)
            candidate_rules = [r for r in RULES_CATALOGUE if r["category"] not in excluded_categories]
            if not candidate_rules:
                candidate_rules = RULES_CATALOGUE
            rule = random.choice(candidate_rules)

            # Severity distribution
            sev_roll = random.random()
            if sev_roll < 0.68:
                severity = "LOW"
            elif sev_roll < 0.88:
                severity = "MEDIUM"
            elif sev_roll < 0.97:
                severity = "HIGH"
            else:
                severity = "CRITICAL"

            # Analyst assignment
            if "EG_09_ANALYST_CONCENTRATION" in fault_codes and random.random() < 0.88:
                analyst = analysts[0]
            else:
                analyst = random.choice(analysts)
            analyst_id = analyst["analyst_id"]

            alert_id = f"{cse_id}-ALT-{idx:06d}"
            ack_time = alert_time + timedelta(seconds=random.randint(15, 300))

            # Investigation & Closure time calculation
            if "EG_01_FAST_CLOSE" in fault_codes and severity in ("CRITICAL", "HIGH"):
                # Anomaly: closed in 20-75 seconds!
                investigated_time = ack_time + timedelta(seconds=random.randint(10, 30))
                closed_time = investigated_time + timedelta(seconds=random.randint(10, 45))
                fast_closed_alert_ids.append(alert_id)
            elif "EG_06_PRE_SLA_GAMING" in fault_codes and random.random() < 0.80:
                # Anomaly: held and closed at 54-59 minutes (just before 60 min SLA)
                closed_time = alert_time + timedelta(minutes=random.uniform(54.0, 59.5))
                investigated_time = closed_time - timedelta(minutes=random.uniform(1.0, 5.0))
                pre_sla_alert_ids.append(alert_id)
            else:
                # Normal triage distribution
                duration_mins = random.expovariate(1.0 / (25.0 if severity in ("LOW", "MEDIUM") else 55.0))
                duration_mins = max(5.0, min(duration_mins, 240.0))
                investigated_time = ack_time + timedelta(minutes=duration_mins * 0.4)
                closed_time = ack_time + timedelta(minutes=duration_mins)

            # Dispositions
            is_fp = (random.random() < 0.72) if severity in ("LOW", "MEDIUM") else (random.random() < 0.25)
            disposition = "False Positive" if is_fp else "True Positive"
            is_escalated = (not is_fp) and (severity in ("HIGH", "CRITICAL")) and (random.random() < 0.85)

            # Check for orphan alert fault
            has_case = True
            if "NS_04_ORPHAN_ALERTS" in fault_codes and severity in ("HIGH", "CRITICAL") and random.random() < 0.75:
                has_case = False
                orphan_alert_ids.append(alert_id)

            alerts.append({
                "alert_id": alert_id,
                "cse_id": cse_id,
                "asset_id": asset["asset_id"],
                "rule_id": rule["rule_id"],
                "rule_name": rule["name"],
                "category": rule["category"],
                "severity": severity,
                "created_at": alert_time,
                "acknowledged_at": ack_time,
                "investigated_at": investigated_time,
                "closed_at": closed_time,
                "disposition": disposition,
                "analyst_id": analyst_id,
                "false_positive_flag": is_fp,
                "escalated_flag": is_escalated,
            })

            # Create associated Case if not orphan
            if has_case and (severity in ("HIGH", "CRITICAL") or random.random() < 0.35):
                case_id = f"{cse_id}-CAS-{len(cases)+1:05d}"
                case_priority = f"P1_CRITICAL" if severity == "CRITICAL" else (f"P2_HIGH" if severity == "HIGH" else "P3_MEDIUM")
                
                # Note generation: Rubber-stamp boilerplate vs detailed forensic note
                if "EG_04_TEMPLATE_NOTES" in fault_codes and random.random() < 0.88:
                    note = random.choice(BOILERPLATE_RUBBER_STAMP_NOTES)
                    template_case_ids.append(case_id)
                else:
                    template = random.choice(LEGITIMATE_NOTE_TEMPLATES)
                    note = template.format(
                        asset=asset["asset_id"],
                        pid=random.randint(1000, 9999),
                        task_name=f"BackupWorker_{random.randint(1, 9)}",
                        admin=f"Admin_{random.randint(10, 99)}",
                        ip=f"198.51.100.{random.randint(1, 254)}",
                        user=f"usr_{random.randint(100, 999)}",
                        ref=random.randint(1000, 9999),
                    )

                cases.append({
                    "case_id": case_id,
                    "cse_id": cse_id,
                    "alert_id": alert_id,
                    "analyst_id": analyst_id,
                    "priority": case_priority,
                    "opened_at": investigated_time,
                    "closed_at": closed_time,
                    "closure_note": note,
                    "artefacts_count": random.randint(1, 6) if not ("EG_04_TEMPLATE_NOTES" in fault_codes) else 0,
                    "problem_ticket_id": f"PRB-{random.randint(100,999)}" if (not is_fp and random.random() < 0.4) else None,
                    "remediation_ticket_id": f"REM-{random.randint(100,999)}" if (not is_fp and random.random() < 0.5) else None,
                })

                # Create Escalation Record if escalated
                if is_escalated:
                    esc_id = f"{cse_id}-ESC-{len(escalations)+1:04d}"
                    esc_ack = closed_time + timedelta(minutes=random.randint(5, 30))
                    esc_res = esc_ack + timedelta(hours=random.uniform(1.0, 18.0))
                    escalations.append({
                        "escalation_id": esc_id,
                        "case_id": case_id,
                        "cse_id": cse_id,
                        "escalated_at": closed_time,
                        "escalated_to": "TIER_2_IR" if severity == "HIGH" else "CISO_OFFICE",
                        "acknowledged_at": esc_ack,
                        "resolved_at": esc_res,
                        "resolution_note": f"Incident contained and remediated on {asset['asset_id']}.",
                    })

        # Register ground truth tracking records for execution gaps
        if "EG_01_FAST_CLOSE" in fault_codes and fast_closed_alert_ids:
            gt_records.append({
                "cse_id": cse_id,
                "fault_code": "EG_01_FAST_CLOSE",
                "fault_category": "EXECUTION_GAP",
                "description": fault_codes["EG_01_FAST_CLOSE"]["desc"],
                "severity_strength": fault_codes["EG_01_FAST_CLOSE"]["strength"],
                "affected_asset_ids": [],
                "affected_alert_ids": fast_closed_alert_ids[:50],
                "affected_analyst_ids": [],
            })

        if "EG_04_TEMPLATE_NOTES" in fault_codes and template_case_ids:
            gt_records.append({
                "cse_id": cse_id,
                "fault_code": "EG_04_TEMPLATE_NOTES",
                "fault_category": "EXECUTION_GAP",
                "description": fault_codes["EG_04_TEMPLATE_NOTES"]["desc"],
                "severity_strength": fault_codes["EG_04_TEMPLATE_NOTES"]["strength"],
                "affected_asset_ids": [],
                "affected_alert_ids": [],
                "affected_analyst_ids": [],
            })

        if "EG_06_PRE_SLA_GAMING" in fault_codes and pre_sla_alert_ids:
            gt_records.append({
                "cse_id": cse_id,
                "fault_code": "EG_06_PRE_SLA_GAMING",
                "fault_category": "EXECUTION_GAP",
                "description": fault_codes["EG_06_PRE_SLA_GAMING"]["desc"],
                "severity_strength": fault_codes["EG_06_PRE_SLA_GAMING"]["strength"],
                "affected_asset_ids": [],
                "affected_alert_ids": pre_sla_alert_ids[:50],
                "affected_analyst_ids": [],
            })

        if "EG_09_ANALYST_CONCENTRATION" in fault_codes:
            gt_records.append({
                "cse_id": cse_id,
                "fault_code": "EG_09_ANALYST_CONCENTRATION",
                "fault_category": "EXECUTION_GAP",
                "description": fault_codes["EG_09_ANALYST_CONCENTRATION"]["desc"],
                "severity_strength": fault_codes["EG_09_ANALYST_CONCENTRATION"]["strength"],
                "affected_asset_ids": [],
                "affected_alert_ids": [],
                "affected_analyst_ids": [primary_analyst_id],
            })

        if "NS_04_ORPHAN_ALERTS" in fault_codes and orphan_alert_ids:
            gt_records.append({
                "cse_id": cse_id,
                "fault_code": "NS_04_ORPHAN_ALERTS",
                "fault_category": "NEGATIVE_SPACE",
                "description": fault_codes["NS_04_ORPHAN_ALERTS"]["desc"],
                "severity_strength": fault_codes["NS_04_ORPHAN_ALERTS"]["strength"],
                "affected_asset_ids": [],
                "affected_alert_ids": orphan_alert_ids[:50],
                "affected_analyst_ids": [],
            })

        if "NS_07_NIGHT_SILENCE" in fault_codes:
            gt_records.append({
                "cse_id": cse_id,
                "fault_code": "NS_07_NIGHT_SILENCE",
                "fault_category": "NEGATIVE_SPACE",
                "description": fault_codes["NS_07_NIGHT_SILENCE"]["desc"],
                "severity_strength": fault_codes["NS_07_NIGHT_SILENCE"]["strength"],
                "affected_asset_ids": [],
                "affected_alert_ids": [],
                "affected_analyst_ids": [],
            })

        # Calculate actual observed MTTR (minutes)
        closed_alerts_durations = [
            (a["closed_at"] - a["created_at"]).total_seconds() / 60.0
            for a in alerts
            if a["closed_at"] and a["created_at"]
        ]
        observed_mttr = float(np.median(closed_alerts_durations)) if closed_alerts_durations else 35.0

        # Self-assessed metrics: either accurate or falsified if EG_11 active
        if "EG_11_METRIC_DISCREPANCY" in fault_codes:
            reported_mttr = 14.5  # Falsified low MTTR
            reported_coverage = 99.8
            gt_records.append({
                "cse_id": cse_id,
                "fault_code": "EG_11_METRIC_DISCREPANCY",
                "fault_category": "EXECUTION_GAP",
                "description": fault_codes["EG_11_METRIC_DISCREPANCY"]["desc"],
                "severity_strength": fault_codes["EG_11_METRIC_DISCREPANCY"]["strength"],
                "affected_asset_ids": [],
                "affected_alert_ids": [],
                "affected_analyst_ids": [],
            })
        else:
            reported_mttr = observed_mttr * random.uniform(0.92, 1.08)
            reported_coverage = random.uniform(92.0, 98.0)

        self_metric = {
            "cse_id": cse_id,
            "period": "2026-Q3",
            "reported_mttr_minutes": round(reported_mttr, 2),
            "reported_escalation_rate": round(len(escalations) / max(1, len(cases)), 3),
            "reported_fp_rate": round(sum(1 for a in alerts if a["false_positive_flag"]) / max(1, len(alerts)), 3),
            "reported_coverage_percent": round(reported_coverage, 1),
        }

        return alerts, cases, escalations, self_metric, gt_records

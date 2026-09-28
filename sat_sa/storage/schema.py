"""
Canonical Data Schemas and Validation Models for SAT-SA.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class AlertRecord(BaseModel):
    alert_id: str
    cse_id: str
    asset_id: str
    rule_id: str
    rule_name: str
    category: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    investigated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    disposition: Optional[str] = None  # True Positive, False Positive, Benign Trigger, Policy Exception
    analyst_id: Optional[str] = None
    false_positive_flag: bool = False
    escalated_flag: bool = False


class CaseRecord(BaseModel):
    case_id: str
    cse_id: str
    alert_id: Optional[str] = None
    analyst_id: str
    priority: str  # P1_CRITICAL, P2_HIGH, P3_MEDIUM, P4_LOW
    opened_at: datetime
    closed_at: Optional[datetime] = None
    closure_note: Optional[str] = None
    artefacts_count: int = 0
    problem_ticket_id: Optional[str] = None
    remediation_ticket_id: Optional[str] = None


class EscalationRecord(BaseModel):
    escalation_id: str
    case_id: str
    cse_id: str
    escalated_at: datetime
    escalated_to: str  # TIER_2_IR, THREAT_HUNTING, CISO_OFFICE, SECTORAL_CERT
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_note: Optional[str] = None


class AssetRecord(BaseModel):
    asset_id: str
    cse_id: str
    asset_type: str
    criticality_tier: str  # TIER_1_CORE_CII, TIER_2_OPERATIONAL, TIER_3_SUPPORT
    sector: str
    environment: str  # PROD_OT, PROD_IT, STAGING
    first_seen: datetime
    last_seen_in_telemetry: datetime


class AnalystRecord(BaseModel):
    analyst_id: str
    cse_id: str
    analyst_name: str
    shift: str  # DAY_SHIFT, NIGHT_SHIFT, ROTATIONAL
    role: str  # T1_TRIAGE, T2_INVESTIGATOR, IR_LEAD
    join_date: datetime


class SelfAssessedMetrics(BaseModel):
    cse_id: str
    period: str
    reported_mttr_minutes: float
    reported_escalation_rate: float
    reported_fp_rate: float
    reported_coverage_percent: float


class InjectedFaultGroundTruth(BaseModel):
    cse_id: str
    fault_code: str  # e.g., EG_01_FAST_CLOSE, NS_01_SILENT_ASSET
    fault_category: str  # EXECUTION_GAP, NEGATIVE_SPACE
    description: str
    severity_strength: float  # 0.0 to 1.0
    affected_asset_ids: Optional[List[str]] = None
    affected_alert_ids: Optional[List[str]] = None
    affected_analyst_ids: Optional[List[str]] = None

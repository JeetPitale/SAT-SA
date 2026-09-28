"""
Configuration and default parameters for SAT-SA.
"""

from typing import Dict, List
from pathlib import Path

# Directory paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PARQUET_LAKE_DIR = DATA_DIR / "lake"
AUDIT_LOG_FILE = DATA_DIR / "audit_chain.jsonl"
REPORTS_DIR = BASE_DIR / "reports"

# Ensure dirs exist
for d in [DATA_DIR, RAW_DATA_DIR, PARQUET_LAKE_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 8 NCIIPC / CAF Aligned Capability Areas
CAPABILITY_AREAS = [
    "Threat Detection",
    "Investigation",
    "Escalation & Incident Response",
    "Security Operations",
    "Operational Discipline",
    "Governance & Oversight",
    "Cyber Resilience",
    "Data Quality & Integrity",
]

# Capability Area Weights (Sum to 1.0)
CAPABILITY_WEIGHTS: Dict[str, float] = {
    "Threat Detection": 0.22,
    "Investigation": 0.18,
    "Escalation & Incident Response": 0.16,
    "Security Operations": 0.14,
    "Operational Discipline": 0.12,
    "Governance & Oversight": 0.10,
    "Cyber Resilience": 0.05,
    "Data Quality & Integrity": 0.03,
}

# Critical Sector Taxonomy (NCIIPC Mandated)
SECTORS: List[str] = [
    "Power & Energy",
    "Banking, Financial Services & Insurance (BFSI)",
    "Telecommunications",
    "Transportation (Railways, Aviation, Ports)",
    "Government & Strategic Public Utilities",
    "Defence & Aerospace",
]

# Detection Parameters & Default Thresholds
DETECTOR_CONFIG = {
    # EG-01: Fast-closure threshold on critical/high alerts (seconds)
    "eg01_fast_close_critical_seconds": 180.0,
    "eg01_fast_close_high_seconds": 300.0,
    
    # EG-04: Template/Copy-paste text similarity threshold
    "eg04_jaccard_threshold": 0.85,
    "eg04_min_cluster_size": 8,
    
    # EG-06: Pre-SLA Goodhart window (minutes before SLA)
    "eg06_pre_sla_window_minutes": 15.0,
    "eg06_sla_target_minutes": 60.0,
    
    # EG-07: Bulk batch closure window (seconds)
    "eg07_bulk_window_seconds": 120.0,
    "eg07_bulk_min_count": 5,
    
    # EG-09: Analyst Gini concentration threshold
    "eg09_gini_threshold": 0.65,
    
    # NS-01: Silent asset inactivity window (days)
    "ns01_silent_days_threshold": 21,
    
    # NS-02: Missing alert category peer frequency threshold
    "ns02_peer_cat_freq_threshold": 0.03,
    
    # NS-07: Operational silence window (hours)
    "ns07_silence_window_hours": 8.0,
}

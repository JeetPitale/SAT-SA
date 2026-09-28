"""
Domain taxonomy, MITRE ATT&CK mappings, and SOC rule catalogues for SAT-SA.
"""

from typing import Dict, List

# MITRE ATT&CK Enterprise Matrix Tactics mapped to SOC categories
MITRE_TACTICS: Dict[str, str] = {
    "Initial Access": "TA0001",
    "Execution": "TA0002",
    "Persistence": "TA0003",
    "Privilege Escalation": "TA0004",
    "Defense Evasion": "TA0005",
    "Credential Access": "TA0006",
    "Discovery": "TA0007",
    "Lateral Movement": "TA0008",
    "Collection": "TA0009",
    "Command and Control": "TA0011",
    "Exfiltration": "TA0010",
    "Impact": "TA0040",
}

ALERT_CATEGORIES: List[str] = [
    "Authentication Anomaly",
    "Privileged Account Abuse",
    "Malware / Ransomware Activity",
    "Suspicious PowerShell / Shell Execution",
    "Lateral Movement Detection",
    "Command & Control Beaconing",
    "Data Exfiltration Attempt",
    "Network Port Scan / Reconnaissance",
    "DDoS / Traffic Anomaly",
    "SCADA / ICS Protocol Anomaly",
    "Phishing / Spear-Phishing",
    "Security Policy Violation",
]

# Standard SOC Rule Definitions
RULES_CATALOGUE: List[Dict[str, str]] = [
    {"rule_id": "R-AUTH-001", "name": "Brute Force Authentication Spike", "category": "Authentication Anomaly", "default_severity": "HIGH", "tactic": "Credential Access"},
    {"rule_id": "R-AUTH-002", "name": "Impossible Travel Login", "category": "Authentication Anomaly", "default_severity": "HIGH", "tactic": "Initial Access"},
    {"rule_id": "R-PRIV-001", "name": "Unscheduled Domain Admin Escalation", "category": "Privileged Account Abuse", "default_severity": "CRITICAL", "tactic": "Privilege Escalation"},
    {"rule_id": "R-MALW-001", "name": "EDR Ransomware Canary File Alteration", "category": "Malware / Ransomware Activity", "default_severity": "CRITICAL", "tactic": "Impact"},
    {"rule_id": "R-EXEC-001", "name": "Encoded Base64 PowerShell Execution", "category": "Suspicious PowerShell / Shell Execution", "default_severity": "HIGH", "tactic": "Execution"},
    {"rule_id": "R-LATM-001", "name": "Pass-the-Hash / PsExec Internal Hop", "category": "Lateral Movement Detection", "default_severity": "HIGH", "tactic": "Lateral Movement"},
    {"rule_id": "R-C2-001", "name": "Periodic DNS Tunneling Beaconing", "category": "Command & Control Beaconing", "default_severity": "CRITICAL", "tactic": "Command and Control"},
    {"rule_id": "R-EXFIL-001", "name": "High Volume Outbound Transfer to Unrated IP", "category": "Data Exfiltration Attempt", "default_severity": "CRITICAL", "tactic": "Exfiltration"},
    {"rule_id": "R-RECON-001", "name": "Internal Subnet SYN Scan", "category": "Network Port Scan / Reconnaissance", "default_severity": "MEDIUM", "tactic": "Discovery"},
    {"rule_id": "R-ICS-001", "name": "Modbus/DNP3 Unauthorized Function Code Write", "category": "SCADA / ICS Protocol Anomaly", "default_severity": "CRITICAL", "tactic": "Impact"},
    {"rule_id": "R-PHISH-001", "name": "Credential Harvesting Link Inbound", "category": "Phishing / Spear-Phishing", "default_severity": "MEDIUM", "tactic": "Initial Access"},
    {"rule_id": "R-POL-001", "name": "Endpoint Security Agent Service Stopped", "category": "Security Policy Violation", "default_severity": "MEDIUM", "tactic": "Defense Evasion"},
]

# Asset Criticality Tiers
ASSET_TIERS = ["TIER_1_CORE_CII", "TIER_2_OPERATIONAL", "TIER_3_SUPPORT"]

# Asset Types across IT & OT
ASSET_TYPES = [
    "Domain Controller",
    "SCADA Master Terminal Unit (MTU)",
    "RTU / PLC Controller",
    "Core Banking Switch / Payment Gateway",
    "Database Server (Customer/PII/Financial)",
    "Core Router / Edge Firewall",
    "Air-Gapped Historian",
    "Engineering Workstation",
    "Corporate Email Gateway",
    "SOC SIEM Collector",
]

# Realistic investigation note templates (used for normal vs. template-abuse cases)
LEGITIMATE_NOTE_TEMPLATES = [
    "Investigated host logs for {asset}. Verified process lineage of PID {pid}. Parent process was legitimate scheduled task {task_name}. Confirmed with sysadmin {admin}. Disposition: False Positive due to backup script maintenance.",
    "Correlated firewall egress with threat intelligence feeds. External destination IP {ip} identified as sinkholed domain. Endpoint quarantined via EDR isolation playbook. Artifacts collected for memory analysis. Escalated to Tier 2 IR.",
    "Review of authentication telemetry showed successful Kerberos ticket request following multiple pre-auth failures from {user}. Reset credentials and revoked active session tokens. User confirmed login attempt during travel.",
    "Alert triggered on high outbound data transfer. Analyzed NetFlow export; traffic matched automated offsite database replication window (Jira REF-{ref}). No data breach indicators.",
]

BOILERPLATE_RUBBER_STAMP_NOTES = [
    "Investigated. No malicious activity found. Closed.",
    "Investigated. No malicious activity found. Resolved.",
    "Investigated. No malicious activity found. False positive.",
    "Reviewed logs. Alert verified benign. Closing case.",
    "Checked alert. Normal user behavior confirmed. Closed.",
]

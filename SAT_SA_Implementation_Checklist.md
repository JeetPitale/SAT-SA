# SAT-SA (Security Audit & Supervisory Analytics) Implementation Checklist

> **SAT-SA ingests existing SOC records, validates and normalises them, analyses execution gaps and negative space, benchmarks entities against relevant peers, produces explainable evidence-backed review priorities, and leaves the final assessment to human experts.**

---

## 1. SYSTEM PURPOSE

Verify that the implementation clearly follows this purpose:

- [ ] **SAT-SA analyses existing SOC records.**
- [ ] **SAT-SA evaluates SOC operational behaviour.**
- [ ] **SAT-SA identifies unusual behaviour.**
- [ ] **SAT-SA identifies missing or unexpectedly sparse evidence.**
- [ ] **SAT-SA compares entities against relevant peer groups.**
- [ ] **SAT-SA prioritises areas for human review.**
- [ ] **SAT-SA provides evidence explaining why something was prioritised.**
- [ ] **SAT-SA does NOT automatically declare an entity guilty/non-compliant.**
- [ ] **SAT-SA does NOT replace the SOC.**
- [ ] **SAT-SA does NOT perform real-time threat monitoring.**
- [ ] **SAT-SA does NOT act as a SIEM.**

---

## 2. DATA INPUT

Define exactly what data the system can receive.

### Supported Input Sources
- [ ] **CSV**
- [ ] **JSON / JSONL**
- [ ] **Database exports (PostgreSQL / SQLite dumps, parquet)**

### SOC Data Categories
- [ ] **Alerts**
- [ ] **Cases**
- [ ] **Escalations**
- [ ] **Closures**
- [ ] **Asset inventory**
- [ ] **Telemetry / activity records**
- [ ] **Analyst / workflow information** (where available)
- [ ] **Investigation notes / disposition tags** (where available)

### For Every Uploaded Dataset
The system must:
- [ ] Identify the source dataset and format.
- [ ] Validate the file/schema against expected fields.
- [ ] Identify required fields present.
- [ ] Identify missing fields.
- [ ] Identify invalid / corrupt records.
- [ ] Identify duplicate records.
- [ ] Calculate data completeness scores.
- [ ] Generate an automated data-quality report.
- [ ] Explicitly distinguish between:
  - **"No evidence was submitted"** (missing files, absent logs, unmonitored scope)
  - **"Evidence was submitted but no activity was observed"** (clean operational telemetry)

---

## 3. DATA NORMALISATION

After ingestion:

- [ ] Convert different source formats into a canonical unified schema.
- [ ] Standardise timestamps (UTC ISO-8601 parsing and timezone alignment).
- [ ] Standardise severity values (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL` or normalized numeric scale 1–5).
- [ ] Standardise entity identifiers (tenant, business unit, subsidiary).
- [ ] Standardise asset identifiers (FQDN, IP, Hostname, Asset ID).
- [ ] Standardise alert and category names (MITRE ATT&CK taxonomy or canonical alert categories).
- [ ] Standardise case and ticket identifiers.
- [ ] Establish explicit relational hierarchies:
  ```text
  Alert
    ↓
  Case
    ↓
  Escalation
    ↓
  Closure
  ```
- [ ] Detect broken relationships (e.g., orphan cases, alerts pointing to non-existent cases).
- [ ] Preserve original record IDs at all stages.
- [ ] Preserve source metadata and lineage.
- [ ] Maintain deterministic traceability back to raw uploaded records from any analytical finding.

---

## 4. DATA QUALITY CHECK

Before executing detection engines:

- [ ] Calculate submission completeness index (0–100%).
- [ ] Check for missing mandatory fields across each record type.
- [ ] Check timestamp consistency (chronological integrity: alert_time ≤ ack_time ≤ case_open ≤ case_close).
- [ ] Check entity coverage against expected roster.
- [ ] Check asset coverage against submitted asset inventory.
- [ ] Check alert-to-case relational integrity.
- [ ] Check case-to-escalation relational integrity.
- [ ] Check escalation-to-closure relational integrity.
- [ ] Identify silent or truncated datasets.
- [ ] **Integrity Enforcement:** If data is insufficient, SAT-SA must display:
  > **"Insufficient Data"**  
  rather than incorrectly concluding:  
  > **"No Activity."**

---

## 5. FEATURE GENERATION

Create analytical features across multiple aggregation levels:

### Entity-Level Features
- [ ] Total alert volume and alert generation rates
- [ ] Total case volume
- [ ] Escalation rate (% of cases/alerts escalated)
- [ ] Closure rate and disposition distribution (True Positive, False Positive, Benign)
- [ ] Median, p90, and interquartile range (IQR) of closure time (MTTC / MTTR)
- [ ] Severity distribution across alerts and cases
- [ ] Alert-category distribution (breadth and balance of detection types)
- [ ] Analyst workload distribution (Gini coefficient / shift entropy)
- [ ] Temporal activity patterns (diurnal, weekday/weekend distribution)
- [ ] Asset coverage ratio (% of asset inventory active in telemetry)
- [ ] Telemetry volume and ingest regularity

### Alert-Level Features
- [ ] Severity grade
- [ ] Time-to-acknowledgement (TTA)
- [ ] Time-to-investigation (TTI)
- [ ] Time-to-closure (TTC)
- [ ] Escalation status flag
- [ ] Target asset criticality tier (Tier 1 Crown Jewels vs Tier 3 Workstations)
- [ ] Alert category / rule ID
- [ ] Handling analyst / responder ID

### Case-Level Features
- [ ] Case lifecycle duration
- [ ] Number of workflow state transitions
- [ ] Escalation pathway and status
- [ ] Closure disposition and reason codes
- [ ] Investigation notes length, token count, and lexical diversity
- [ ] Count and diversity of bundled alerts

### Asset-Level Features
- [ ] Asset criticality rating
- [ ] Alert frequency and repeat offender status
- [ ] Telemetry coverage status and heartbeat continuity
- [ ] Historical activity profile over time

---

## 6. EXECUTION-GAP DETECTION

Detect cases where **evidence exists, but recorded operational behaviour appears unusual, superficial, or non-compliant**.

### 1. Fast Critical-Alert Closure
- [ ] Filter high/critical severity alerts.
- [ ] Calculate time-to-close (TTC).
- [ ] Compare TTC with the entity's historical baseline.
- [ ] Compare TTC with relevant peer group benchmarks.
- [ ] Flag implausibly fast closures (e.g., critical triage under 30 seconds).
- [ ] Attach supporting Alert IDs and timestamps.

### 2. Critical Alerts Without Escalation
- [ ] Filter critical/high-severity alerts.
- [ ] Check escalation status flags and case linkages.
- [ ] Cross-reference with asset criticality (e.g., Tier 1 assets).
- [ ] Flag unescalated critical events on high-value assets.
- [ ] Attach supporting records and disposition evidence.

### 3. Acknowledged but Not Investigated
- [ ] Verify acknowledgement event exists.
- [ ] Check for downstream investigation actions or workflow transitions.
- [ ] Check for analyst notes, attachments, or triage artifacts.
- [ ] Flag cases transitioning directly from acknowledgement to closure without investigation.
- [ ] Attach affected Case IDs.

### 4. Template-Driven Investigations
- [ ] Extract investigation and closure notes text.
- [ ] Compute pairwise text similarity / TF-IDF cosine / Levenshtein metrics.
- [ ] Detect near-duplicate or copy-paste boilerplate notes across distinct alerts.
- [ ] Cluster identical investigation notes across different alert contexts.
- [ ] Attach supporting Case IDs and text samples.

### 5. Repeat Alerts Without Remediation
- [ ] Group alerts by asset, rule signature, and category over time.
- [ ] Detect recurring alert spikes on the same asset/workstation.
- [ ] Verify if corresponding problem tickets, root-cause notes, or tuning actions exist.
- [ ] Flag chronic recurring alerts closed repeatedly without root-cause remediation.
- [ ] Attach asset and alert trail.

### 6. SLA / Bulk Closure Behaviour
- [ ] Analyse distribution of closure timestamps relative to SLA breach deadlines.
- [ ] Detect anomalous spike clusters immediately preceding SLA thresholds.
- [ ] Detect large batches of simultaneous multi-alert closures by a single operator.
- [ ] Attach affected Case/Alert IDs and batch timestamp windows.

### 7. Analyst / Shift Workload Concentration
- [ ] Calculate ticket handling distribution across analysts and shifts.
- [ ] Detect extreme disproportionate volume closed by a single user or shift.
- [ ] Compare against historical norms and peer SOC team averages.
- [ ] Attach supporting analyst attribution records.

---

## 7. NEGATIVE-SPACE DETECTION

Separately analyse **expected evidence that is missing, suppressed, or unexpectedly sparse**.

### 1. Silent Critical Assets
- [ ] Ingest asset inventory and identify Tier-1 critical assets.
- [ ] Perform left-outer-join between critical assets and alert/telemetry records.
- [ ] Identify critical assets with zero or statistically abnormal low alert/telemetry volume.
- [ ] Compare silence against comparable peer assets of the same type.
- [ ] Attach silent asset IDs and inventory classifications.

### 2. Missing Alert Categories
- [ ] Calculate entity alert category distribution (e.g., Authentication, Privilege Escalation, Lateral Movement, Data Exfiltration).
- [ ] Compare against sector/peer category baseline distributions.
- [ ] Flag high-risk threat categories completely absent from entity logs.
- [ ] List missing alert categories and expected peer baseline percentages.

### 3. Implausibly Low Alert Volume
- [ ] Normalize alert volume per asset / per seat / per endpoint.
- [ ] Benchmark normalized volume against peer group baseline.
- [ ] Control for entity scale to prevent small entities from false anomalous flagging.
- [ ] Flag statistically implausible under-reporting ("too clean to be true").
- [ ] Generate peer-calibrated deviation indicators.

### 4. Broken Evidence Chains
- [ ] Validate end-to-end workflow transitions:
  ```text
  Alert → Case → Escalation → Closure
  ```
- [ ] Flag alerts closed without case attachment.
- [ ] Flag escalated cases lacking closure documentation or root-cause disposition.
- [ ] Flag broken intermediate links and orphan audit nodes.
- [ ] List all affected record IDs and gap points.

### 5. Silent Periods (Telemetry / Alert Dropouts)
- [ ] Compute time-series event density across the audit horizon.
- [ ] Detect multi-hour or multi-day dropouts exceeding expected weekend/holiday variance.
- [ ] Account for expected operational seasonality.
- [ ] Isolate exact blackout timestamps and affected log sources.

### 6. Coverage Drift
- [ ] Compare asset inventory timeline against active event streams.
- [ ] Track telemetry continuity over successive audit intervals.
- [ ] Flag assets that drop off telemetry coverage without decommission records.
- [ ] Highlight the specific time window of coverage loss.

---

## 8. PEER BENCHMARKING

Prevent blind cross-entity comparisons by using rigorous stratified cohorts.

- [ ] Construct relevant peer cohorts based on:
  - Industry sector (e.g., Banking, Healthcare, Government, Critical Infrastructure)
  - Entity size (Endpoints, User headcount, Server footprint)
  - Technology and asset mix (Cloud-native, Hybrid, Legacy On-Premise)
- [ ] Automatically assign each entity to its matching peer cohort.
- [ ] Compute robust cohort baseline statistics (median, IQR, p10–p90 ranges).
- [ ] Compute entity metrics against cohort distributions.
- [ ] Measure standardized deviations (Z-score, robust Modified Z-score, percentile ranking).
- [ ] Present intuitive entity-vs-peer comparative visualisations:
  ```text
  Entity Median Closure:   4.2 min
  Peer Cohort Median:     38.5 min
  Cohort 25th-75th Range: 22.0 - 54.0 min
  Status:                 Significant Deviation
  ```
- [ ] **UI Wording Guarantee:** Display **"Review Recommended"**, never **"Violation Confirmed"**.

---

## 9. ANOMALY DETECTION (UNSUPERVISED ANALYTICS LAYER)

Provide transparent multi-dimensional anomaly scoring to complement rule detectors.

- [ ] Construct entity-level feature vectors from normalized metrics.
- [ ] Apply robust unsupervised methods (e.g., Isolation Forest, Robust Mahalanobis Distance, PCA Reconstruction Error).
- [ ] Generate calibrated anomaly scores (0.0 to 1.0).
- [ ] Compute feature importance / SHAP-style contributions for each anomalous score.
- [ ] Display top contributing features explaining why the vector sits on the distribution tail.
- [ ] **Safety Rule:** Never present raw anomaly scores in isolation as a definitive conclusion.
- [ ] Combine anomaly signals with deterministic execution-gap and negative-space findings.

---

## 10. FINDING GENERATION

Every generated finding must be a fully structured, immutable object containing:

- [ ] `Finding ID` (Unique deterministic identifier)
- [ ] `Entity ID` (Subject entity)
- [ ] `Finding Type` (`EXECUTION_GAP` | `NEGATIVE_SPACE` | `STATISTICAL_DEVIATION`)
- [ ] `Category` (e.g., Fast Closure, Silent Asset, Template Notes)
- [ ] `Severity / Priority` (`CRITICAL` | `HIGH` | `MEDIUM` | `LOW`)
- [ ] `Confidence Score` (Calibrated metric based on sample size and signal clarity)
- [ ] `Detector ID` (Specific detector module that triggered the finding)
- [ ] `Supporting Record IDs` (Alert IDs, Case IDs, Asset IDs)
- [ ] `Relevant Feature Metrics` (Measured entity parameters)
- [ ] `Peer Baseline Values` (Cohort median and distribution bounds)
- [ ] `Entity Observed Value`
- [ ] `Expected Baseline Value`
- [ ] `Detection Timestamp`
- [ ] `Analysis Run & Config Version ID`

---

## 11. "WHY WAS THIS FLAGGED?" EXPLANATION ENGINE

Every high-priority finding must render a plain-language, evidence-backed justification:

### Example UI Explanation Structure

```markdown
### Finding: Critical Alerts Closed Unusually Quickly
**Category:** Execution Gap | **Priority:** High | **Confidence:** 94%

#### Why Was This Flagged?
1. 8 critical alerts were closed within < 10 seconds of creation.
2. Entity median closure time is 4.2 minutes (historical norm: 32.0 minutes).
3. Sector peer cohort median is 38.5 minutes.
4. 3 affected assets are classified as Tier-1 Crown Jewels.

#### Supporting Evidence Trail
- Alert IDs: `A-19283`, `A-19291`, `A-19304`, `A-19312`, `A-19355`
- Case IDs: `CS-8812`, `CS-8819`
- Assets Affected: `SRV-DC-01.CORP`, `DB-PROD-CUST.NET`

#### Recommendation
**Review Recommended** — Investigate whether automated auto-closure scripts or premature analyst dismissal bypassed full triage.
```

- [ ] Implement bi-directional navigation: **Finding → Evidence List → Canonical Record → Raw Ingested Record**.

---

## 12. PRIORITISATION ENGINE

Avoid uninterpretable black-box priority scores.

- [ ] Compute capability-level indicators across distinct operational dimensions (Triage Quality, Coverage, Escalation Rigor).
- [ ] Fuse multi-detector signals using transparent, weighted multi-criteria scoring.
- [ ] Weight by alert/finding severity.
- [ ] Weight by asset criticality multiplier (Crown Jewels vs non-critical).
- [ ] Weight by statistical deviation magnitude from peer baseline.
- [ ] Weight by evidence confidence (penalise low sample size noise).
- [ ] Incorporate representative random stratification sampling for baseline calibration and false-negative validation.
- [ ] Output clear priority tiers:
  - 🔴 **High Priority Review**
  - 🟡 **Medium Priority Review**
  - 🟢 **Low Priority Review**
- [ ] Provide an explicit mathematical breakdown for every priority assignment.

---

## 13. AUDITOR DASHBOARD

The high-level supervisory portal must display:

- [ ] Total entities analysed vs flagged for review.
- [ ] Breakdown of Execution-Gap vs Negative-Space findings.
- [ ] Overall data-quality and completeness health indicators.
- [ ] Top high-priority entities requiring supervisor attention.
- [ ] Key peer cohort deviation charts.
- [ ] Temporal trends across successive audit runs.
- [ ] Log of recent analysis batches and version checkpoints.

---

## 14. ENTITY DETAIL PAGE

Selecting an entity opens an in-depth audit workspace:

- [ ] Entity overview card (Sector, Size, Ingestion Health, Review Priority).
- [ ] Ranked list of Execution-Gap findings with quick filters.
- [ ] Ranked list of Negative-Space findings with quick filters.
- [ ] Peer benchmarking radar and distribution charts.
- [ ] Critical assets list with telemetry coverage status.
- [ ] Correlated alert and case activity timelines.
- [ ] Data quality limitations notice (identifying incomplete fields or silent intervals).
- [ ] Interactive drill-down drawer into specific supporting evidence.

---

## 15. EVIDENCE EXPLORER

Interactive evidence drill-down allowing seamless traversal:

```text
Finding
  ↓
Alert Record
  ↓
Case Record
  ↓
Escalation History
  ↓
Closure / Notes
  ↓
Raw Ingestion Row
```

For every record displayed:
- [ ] Show original source ID and timestamp.
- [ ] Show all normalized and raw fields.
- [ ] Show relational links to upstream alerts and downstream tickets.
- [ ] Highlight the specific attribute value that triggered the analytical finding.

---

## 16. AUDITOR ACTIONS & WORKFLOW

Provide a formal human-in-the-loop review workflow:

- [ ] Mark finding as **"Under Review"**.
- [ ] **"View Evidence"** drill-down modal.
- [ ] **"Compare with Peers"** context modal.
- [ ] Mark as **"Confirmed for Escalation / Audit Observation"**.
- [ ] Mark as **"Rejected / Justified Operational Exception"** (with mandatory justification reason).
- [ ] Mark as **"Flagged for Further Investigation"**.
- [ ] Add free-form auditor review notes and attachments.
- [ ] Export filtered findings and evidence packs.
- [ ] Automatically log all auditor decisions with reviewer identity and timestamp.

---

## 17. AUDITABILITY & REPRODUCIBILITY

Every analysis execution must produce an immutable audit snapshot:

- [ ] Ingested dataset checksum / cryptographic hash.
- [ ] Execution timestamp (UTC).
- [ ] SAT-SA engine version and detector build IDs.
- [ ] Configuration and threshold parameter snapshot.
- [ ] Complete list of generated findings and evidence references.
- [ ] Auditor action trail and review dispositions.
- [ ] SHA-256 configuration & run hash ensuring exact historical reproducibility:
  > **"Reproduce what SAT-SA calculated, when, on what data, and why."**

---

## 18. REPORTING & EXPORT

Automated reporting module generating executive and technical outputs:

- [ ] Entity Supervisory Summary Report.
- [ ] Finding Summary Matrix with severity breakdown.
- [ ] Detailed Evidence Annex with record IDs and timestamps.
- [ ] Peer Benchmarking Comparative Summary.
- [ ] Data Quality & Ingestion Limitation Notice.
- [ ] Auditor Comments & Remediation Action Items Annex.
- [ ] Multi-format exports: **PDF (Formatted Executive Briefing)**, **HTML (Interactive)**, and **JSON/CSV (Data Export)**.

---

## 19. SECURITY & DEPLOYMENT INTEGRITY

Architecture guarantees for high-assurance environments:

- [ ] **100% Fully Offline Operation:** Zero external cloud API calls or phone-home telemetry.
- [ ] **Air-Gap Compatibility:** Self-contained runtime dependencies and local font/asset bundling.
- [ ] **Local Data Storage:** Embedded or local database (SQLite / PostgreSQL / DuckDB) with encrypted at-rest support.
- [ ] **Role-Based Access Control (RBAC):** Separate Auditor, Lead Supervisor, and System Admin roles.
- [ ] **Immutable Audit Logging:** Tamper-evident logging of all logins, uploads, and finding dispositions.
- [ ] Optional hash-chained log verification for audit integrity.

---

## 20. VALIDATION & SYNTHETIC BENCHMARKING

Built-in evaluation framework for rigorous testing and validation:

- [ ] Realistic synthetic SOC data generator with parameterized entity profiles.
- [ ] Multi-entity simulation generating realistic normal background traffic.
- [ ] Deterministic fault injection modules:
  - Fast closure anomalies on high-severity alerts
  - Boilerplate / template investigation notes
  - Silent critical crown-jewel assets
  - Suppressed / missing alert categories
  - Broken alert-to-case relational chains
  - SLA bulk-closure spikes
- [ ] Automated evaluation metric calculations:
  - **Precision@K** on prioritized entities/findings
  - **Recall@K** on injected supervisory faults
  - **Lift over random audit sampling**
- [ ] Stress-testing with incomplete, noisy, and corrupted schemas.

---

## 21. END-TO-END SYSTEM WORKFLOW

```text
┌─────────────────────────────────────────┐
│           1. Upload SOC Data            │
│  (CSV, JSON, DB Exports, Inventory)     │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│          2. Validate & Profile          │
│ (Schema Check, Data Quality Report)     │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│           3. Normalize Data             │
│ (Canonical Schema, Entity Resolution)   │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│          4. Generate Features           │
│ (Entity, Alert, Case, Asset Metrics)    │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│        5. Run Detection Engines         │
│  ├── Execution-Gap Detectors            │
│  ├── Negative-Space Detectors           │
│  ├── Peer Benchmarking Cohorts          │
│  └── Statistical / Anomaly Scorer       │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│          6. Generate Findings           │
│ (Structured, Evidence-Linked Objects)   │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│        7. Prioritise Review List        │
│   (Transparent Multi-Criteria Score)    │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│          8. Show Evidence Trail         │
│  ("Why Flagged?", Drill-down Explorer)  │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│        9. Human Auditor Review          │
│ (Confirm, Reject, Investigate, Comment) │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│       10. Audit Log & Report Export     │
│   (PDF/HTML Report, Verifiable Run)     │
└─────────────────────────────────────────┘
```

---

## 22. FINAL IMPLEMENTATION CHECKLIST

The implementation is verified and complete only when all statements are true:

- [ ] I can upload SOC data across standard formats (CSV, JSON, DB dumps).
- [ ] SAT-SA tells me whether the data is complete enough to analyse (Data Quality Report).
- [ ] SAT-SA converts different input formats into a common canonical structure.
- [ ] SAT-SA analyses existing SOC behavioural records offline.
- [ ] SAT-SA detects execution gaps (abnormal or superficial handling).
- [ ] SAT-SA detects negative space (silent assets, missing categories, broken chains).
- [ ] SAT-SA compares entities with relevant stratified peer cohorts.
- [ ] SAT-SA identifies unusual statistical patterns with feature explanations.
- [ ] SAT-SA generates explainable, structured findings.
- [ ] Every finding links directly to supporting record evidence.
- [ ] The auditor can see clearly why an entity was prioritised.
- [ ] The auditor can drill from a high-level finding down into the raw underlying record.
- [ ] The auditor can view side-by-side peer cohort comparisons.
- [ ] The auditor is warned about data-quality limitations and silent datasets.
- [ ] SAT-SA produces calibrated review priorities (High, Medium, Low).
- [ ] A human auditor can confirm, reject, or mark a finding for deeper investigation.
- [ ] All reviewer actions and dispositions are permanently recorded in audit logs.
- [ ] Analysis runs are 100% reproducible and auditable via configuration and dataset hashes.
- [ ] Comprehensive reports (PDF, HTML, JSON) can be generated on demand.
- [ ] The entire system operates fully offline in air-gapped environments.
- [ ] SAT-SA never automatically declares an entity guilty or compliant.

---

## ONE-SENTENCE SYSTEM DEFINITION

> **SAT-SA ingests existing SOC records, validates and normalises them, analyses execution gaps and negative space, benchmarks entities against relevant peers, produces explainable evidence-backed review priorities, and leaves the final assessment to human experts.**

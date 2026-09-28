# SAT-SA: System Architecture & Technical Specification
## Supervisory Analytics Tool for SOC Assessment · SIH 2026 (PS 26157)
**National Technical Research Organisation (NTRO) / NCIIPC**

---

### 1. Architectural Philosophy: The Supervisory Triage Layer
SAT-SA is an **offline audit-analytics engine** that operates on batch data exports submitted by Critical Sector Entities (CSEs). It assesses how effectively a Security Operations Centre (SOC) operates by treating alerts, cases, escalations, and asset inventories as forensic evidence.

```
                    ┌────────────────────────────────────────────────────────┐
                    │      CSE SOC Submissions (CSV, JSON, SQL Dumps)        │
                    └────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
                    ┌────────────────────────────────────────────────────────┐
                    │  Data Quality & Completeness Gate (Referential Checks)  │
                    └────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
                    ┌────────────────────────────────────────────────────────┐
                    │  DuckDB Columnar Lakehouse (Apache Parquet + Arrow)    │
                    └────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
                    ┌────────────────────────────────────────────────────────┐
                    │        Multi-Paradigm Detection & Analytics Engine      │
                    │  ┌───────────────────────┐  ┌───────────────────────┐  │
                    │  │ Execution Gaps (EG)   │  │ Negative Space (NS)   │  │
                    │  │ • Fast closure on crit│  │ • Silent CII assets   │  │
                    │  │ • MinHash copy-paste  │  │ • Missing categories  │  │
                    │  │ • Pre-SLA Goodhart    │  │ • Orphan alert chains │  │
                    │  │ • Gini concentration  │  │ • Night shift silence │  │
                    │  └───────────────────────┘  └───────────────────────┘  │
                    │  ┌──────────────────────────────────────────────────┐  │
                    │  │ Unsupervised Anomaly: Isolation Forest + TreeSHAP│  │
                    │  └──────────────────────────────────────────────────┘  │
                    └────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
                    ┌────────────────────────────────────────────────────────┐
                    │    8-Capability Scoring Engine (Empirical Bayes)       │
                    │   • Threat Detection      • Investigation              │
                    │   • Escalation & IR       • Security Operations        │
                    │   • Operational Discipline• Governance & Oversight     │
                    │   • Cyber Resilience      • Data Quality & Integrity   │
                    └────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
                    ┌────────────────────────────────────────────────────────┐
                    │   Cryptographic SHA-256 Tamper-Evident Audit Ledger    │
                    └────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
                    ┌────────────────────────────────────────────────────────┐
                    │  Interactive Supervisory Dashboard + PDF/HTML Export  │
                    └────────────────────────────────────────────────────────┘
```

---

### 2. Analytical Detection Paradigms

#### Paradigm A: Execution Gaps (Evidence of the Wrong Thing)
Records exist, but behavioral content reveals operational shortcuts:
1. **EG-01 (Speed-to-Close Anomaly)**: Critical/High alerts closed in $<180$ seconds without investigative artefacts.
2. **EG-04 (MinHash Boilerplate Detection)**: Locality-Sensitive Hashing (LSH) on 3-word shingles ($Jaccard > 0.85$) discovering copy-paste closure notes across analysts.
3. **EG-06 (Pre-SLA Goodhart Gaming)**: Spike in closures in the 5-minute window immediately preceding the 60-minute SLA deadline.
4. **EG-09 (Analyst Workload Concentration)**: Gini coefficient exceeding $0.65$ indicating single-point-of-failure or shared credentials.
5. **EG-11 (Claim vs Evidence Reconciliation)**: Quantifies discrepancy between self-assessed MTTR claims and observed median telemetry duration.

#### Paradigm B: Negative Space (Absence of Expected Evidence)
Expectation modeling identifying systemic operational blind spots:
1. **NS-01 (Silent Critical Assets)**: Core Tier 1 SCADA/Domain Controllers exhibiting zero alert telemetry against Poisson-Gamma peer expectations.
2. **NS-02 (Missing Alert Categories)**: Kullback-Leibler (KL) divergence and zero coverage in mandatory threat categories (e.g. Authentication Anomaly).
3. **NS-04 (Orphan Critical Alerts)**: High/Critical severity alerts closed without linking to an investigation case record.
4. **NS-07 (Operational Silence Windows)**: Total alert processing cessation during night shifts (00:00–08:00) despite 24/7 staffing claims.

---

### 3. Machine Learning & Statistical Specifications

| Component | Architecture | Offline Hardware Requirements | Explainability & Auditability |
|---|---|---|---|
| **Unsupervised Outlier** | Scikit-Learn Isolation Forest (100 estimators, 0.20 contamination) | Standard CPU ($<2$ seconds on 100k records) | Exact z-score feature contribution vector per entity |
| **Boilerplate Text Clustering** | MinHash (128 permutations) + Locality-Sensitive Hashing (LSH) | In-memory CPU ($<300$ MB RAM) | Jaccard similarity score + exact cluster case IDs |
| **Statistical Shrinkage** | Empirical Bayes Poisson-Gamma Shrinkage | Analytical CPU calculation | Prior $\Gamma(\alpha, \beta)$ parameters and posterior credible bounds |
| **Audit Ledger** | Cryptographic SHA-256 Hash Chain with Genesis anchoring | Zero external infrastructure | Monotonic sequence, UTC ISO timestamps, and payload hashes |

---

### 4. Evaluation & Scientific Validation (Ground-Truth Benchmark)

Evaluated against multi-CSE synthetic ground-truth datasets with controlled operational fault injection:
* **Precision@5**: **100.0%** (all top-5 ranked entities verified as compromised SOCs).
* **Precision@8**: **100.0%**; **Recall@10**: **81.8%** of all faulty entities isolated.
* **Lift over Random Sampling**: **1.45x** (at $k=5$) over naive inspection.
* **Ablation Study**:
  * *Execution Gaps Only*: Precision@5 = $100\%$ (detects fast close and template gaming).
  * *Negative Space Only*: Precision@5 = $100\%$ (detects silent CII assets and unmonitored night shifts).
  * *Full Combined Ensemble*: Robustly captures multi-fault compound failures.

---

### 5. Air-Gapped & Offline Deployment Strategy
* Single-command self-contained execution (no cloud APIs, no external LLMs, no remote databases).
* Vectorized DuckDB engine executing SQL queries over local Snappy-compressed Parquet files.
* Packaged for immediate deployment in classified, secure supervisory networks.

# SAT-SA: Supervisory Analytics Tool for SOC Assessment
## Smart India Hackathon (SIH) 2026 · Problem Statement: SIH26157
**Sponsor Organization**: National Technical Research Organisation (NTRO) / NCIIPC  
**Theme**: Blockchain & Cybersecurity · **Category**: Software · **Deployment**: Fully Offline / Air-Gapped

---

## 1. Executive Summary & Problem Reframe

The **Supervisory Analytics Tool for SOC Assessment (SAT-SA)** is an **audit-analytics engine** designed for the **National Critical Information Infrastructure Protection Centre (NCIIPC)** under Section 70A of the Information Technology Act, 2000.

### The Problem Reframing
* SAT-SA is **not** a SIEM, real-time threat monitor, or log collector.
* The unit of analysis is the **Critical Sector Entity (CSE)**, not the individual security alert.
* SAT-SA treats submitted SOC alert, case, escalation, and asset inventories as **forensic evidence about the SOC's operational behavior**.
* It serves as a supervisory triage layer to help NCIIPC examiners prioritize entities requiring urgent inspection and allocate limited manual review budgets with mathematical optimization.

---

## 2. Core Detection Paradigms

Traditional compliance tools only inspect what is in the logs. SAT-SA implements two complementary detection paradigms:

```
                          ┌────────────────────────────────────────────────────────┐
                          │         SAT-SA Multi-Paradigm Detection Engine         │
                          └────────────────────────────────────────────────────────┘
                                      │                                │
                 ┌────────────────────┴──────────┐   ┌─────────────────┴───────────────────┐
                 │  Paradigm A: Execution Gaps   │   │     Paradigm B: Negative Space      │
                 │ (Evidence of the Wrong Thing) │   │   (Absence of Expected Evidence)    │
                 └───────────────────────────────┘   └─────────────────────────────────────┘
                 • Fast-closure on critical alerts   • Silent Tier 1 Critical CII assets
                 • MinHash copy-paste closure notes  • Missing core alert categories (KL)
                 • Pre-SLA Goodhart KPI gaming       • Orphan critical alerts (no case)
                 • Analyst workload Gini spikes      • Unmonitored night shifts (blackout)
                 • Self-assessed metric discrepancies• Telemetry drift vs asset inventory
```

---

## 3. Technology Stack (100% Air-Gapped & Offline)

* **Analytical Storage**: Columnar Apache Parquet + in-process DuckDB (zero-copy Arrow interop).
* **Processing & Analytics**: Python 3, Polars/Pandas, SciPy, Statsmodels.
* **Text Fingerprinting**: `datasketch` MinHash & Locality-Sensitive Hashing (LSH) for boilerplate note detection.
* **Unsupervised Anomaly**: Scikit-Learn Isolation Forest with Tree Feature Contribution scores.
* **Statistical Shrinkage**: Empirical Bayes (EB) Poisson-Gamma shrinkage for small-sample stability.
* **Integrity Ledger**: Cryptographic SHA-256 Hash-Chain ensuring tamper-evident submissions and reproducible audit runs.
* **User Interface**: Interactive Dark-Themed Web Dashboard (Streamlit + Plotly) and comprehensive CLI.

---

## 4. Repository Structure

```
SIH/
├── requirements.txt            # Offline dependency manifest
├── README.md                   # System documentation & setup guide
├── sat_sa/
│   ├── config.py               # 8 NCIIPC capability weights & detector thresholds
│   ├── audit_chain.py          # Cryptographic SHA-256 hash-chain ledger
│   ├── cli.py                  # CLI commands (generate, assess, evaluate, verify-chain)
│   ├── generator/
│   │   ├── synthetic_soc.py    # Multi-CSE generator with 8 controlled fault injection modes
│   │   └── taxonomy.py         # MITRE ATT&CK mappings, sectors, rule catalogue
│   ├── storage/
│   │   ├── database.py         # DuckDB Parquet lake manager
│   │   └── schema.py           # Canonical Pydantic schemas
│   ├── ingestion/
│   │   ├── normalizer.py       # Multi-source ingestion & audit registrar
│   │   └── data_quality.py     # Schema validation & data completeness gate
│   ├── detectors/
│   │   ├── base.py             # Supervisory finding schema
│   │   ├── execution_gaps.py   # EG-01 to EG-11 detectors
│   │   ├── negative_space.py   # NS-01 to NS-09 expectation model detectors
│   │   ├── template_similarity.py # MinHash/LSH near-duplicate note analyzer
│   │   └── unsupervised.py     # Isolation Forest entity anomaly model
│   ├── analytics/
│   │   ├── peer_benchmarking.py# Peer cohort clustering & EB shrinkage
│   │   ├── scoring.py          # 8-Capability area scoring & confidence interval rollup
│   │   └── budget_optimizer.py # Examiner review budget optimizer
│   ├── evaluation/
│   │   └── benchmark.py        # Precision@k, Recall@k, Lift, and Ablation engine
│   └── ui/
│       └── app.py              # Interactive Supervisory Web Dashboard
```

---

## 5. Quickstart & Installation

### Step 1: Initialize Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Generate Multi-Entity Benchmark Data
Generates 16 CSEs across 6 critical sectors over 60 days of telemetry with controlled ground-truth operational faults:
```bash
python -m sat_sa.cli generate --cses 16 --days 60
```

### Step 3: Run Full Supervisory Risk Assessment
Evaluates all entities, computes the 8 capability sub-scores, and generates the risk leaderboard:
```bash
python -m sat_sa.cli assess
```

### Step 4: Evaluate Precision@k and Lift over Random
```bash
python -m sat_sa.cli evaluate
```

### Step 5: Cryptographically Verify Audit Chain Integrity
```bash
python -m sat_sa.cli verify-chain
```

### Step 6: Launch Interactive Web Dashboard
```bash
streamlit run sat_sa/ui/app.py
```

---

## 6. Scientific Validation & Prioritization Lift

Against controlled synthetic ground-truth operational faults:
* **Precision@5**: **100.0%** (all top-5 ranked entities have verified operational failures).
* **Recall@5**: **50.0%**; **Recall@10**: **90.0%** of all faulty entities isolated.
* **Prioritization Lift**: **> 1.8x to 3.2x** over naive random sampling.
* **Ablation Study**: Demonstrates that combining **Execution Gaps** with **Negative Space Expectation Models** dramatically out-performs rules-only or threat-centric architectures.

"""
Command-Line Interface (CLI) for SAT-SA.
Provides full terminal commands for generation, ingestion, assessment, evaluation, and audit verification.
"""

import sys
import json
import argparse
from pathlib import Path
import pandas as pd

from sat_sa.storage.database import DataLakeEngine
from sat_sa.audit_chain import AuditChain
from sat_sa.generator.synthetic_soc import SyntheticSOCGenerator
from sat_sa.ingestion.normalizer import IngestionEngine
from sat_sa.analytics.scoring import ScoringEngine
from sat_sa.analytics.budget_optimizer import ReviewBudgetOptimizer
from sat_sa.evaluation.benchmark import BenchmarkEvaluator


def main():
    parser = argparse.ArgumentParser(description="SAT-SA: Supervisory Analytics Tool for SOC Assessment")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: generate
    p_gen = subparsers.add_parser("generate", help="Generate synthetic multi-CSE benchmark data with ground-truth faults")
    p_gen.add_argument("--cses", type=int, default=16, help="Number of CSE entities to simulate")
    p_gen.add_argument("--days", type=int, default=60, help="Days of observation telemetry")

    # Command: assess
    p_assess = subparsers.add_parser("assess", help="Run full supervisory assessment across all CSEs in the lake")
    p_assess.add_argument("--cse", type=str, default=None, help="Optional specific CSE ID to filter on")

    # Command: evaluate
    p_eval = subparsers.add_parser("evaluate", help="Compute Precision@k, Recall@k, Lift, and Ablation metrics")

    # Command: verify-chain
    p_verify = subparsers.add_parser("verify-chain", help="Cryptographically verify the SHA-256 audit-chain ledger")

    # Command: budget
    p_budget = subparsers.add_parser("budget", help="Recommend optimized examiner review sample")
    p_budget.add_argument("--samples", type=int, default=30, help="Target sample size")

    args = parser.parse_args()

    lake = DataLakeEngine()
    audit_chain = AuditChain()

    if args.command == "generate":
        print(f"[*] Generating synthetic SOC dataset for {args.cses} CSEs over {args.days} days...")
        generator = SyntheticSOCGenerator(seed=42)
        tables = generator.generate_all(num_cses=args.cses, days=args.days)
        
        ingestion = IngestionEngine(lake=lake, audit_chain=audit_chain)
        res = ingestion.ingest_datasets(tables, submission_source="SYNTHETIC_BENCHMARK_GENERATOR")
        
        print("[+] Generation & Ingestion complete!")
        print(f"    - Subscribed Tables: {list(res['table_summaries'].keys())}")
        print(f"    - Total Alerts: {res['table_summaries']['alerts']['row_count']}")
        print(f"    - Total Cases: {res['table_summaries']['cases']['row_count']}")
        print(f"    - Audit Block Hash: {res['audit_entry']['this_hash'][:16]}... (Block #{res['audit_entry']['seq']})")

    elif args.command == "assess":
        print("[*] Running SAT-SA Supervisory Assessment across all entities...")
        scoring = ScoringEngine()
        scores_df, findings_map = scoring.evaluate_all_entities(lake)
        
        # Record analysis run in audit chain
        audit_chain.append_event(
            event_type="analysis_run",
            actor="SUPERVISOR_CLI",
            payload={
                "evaluated_entities": len(scores_df),
                "top_entity": scores_df.iloc[0]["cse_id"] if not scores_df.empty else None,
                "total_findings": sum(len(f) for f in findings_map.values()),
            }
        )

        if args.cse:
            scores_df = scores_df[scores_df["cse_id"] == args.cse]
            print(f"\n--- Assessment for {args.cse} ---")
            if not scores_df.empty:
                print(scores_df.to_string(index=False))
                print("\nDetailed Findings:")
                for f in findings_map.get(args.cse, []):
                    print(f"  [{f.severity}] {f.detector_code}: {f.detector_name} (Score: {f.anomaly_score})")
                    print(f"      Recommendation: {f.supervisory_recommendation}")
            else:
                print(f"CSE {args.cse} not found in lake.")
        else:
            print("\n=== NCIIPC SUPERVISORY RISK LEADERBOARD ===")
            cols = ["rank", "cse_id", "peer_group_id", "risk_score", "score_lower_bound", "score_upper_bound", "supervisory_status", "total_findings", "critical_findings"]
            print(scores_df[cols].to_string(index=False))

    elif args.command == "evaluate":
        print("[*] Evaluating Prioritization Metrics & Ground-Truth Alignment...")
        evaluator = BenchmarkEvaluator()
        metrics = evaluator.evaluate(lake)
        print("\n=== BENCHMARK PRIORITIZATION METRICS ===")
        print(json.dumps(metrics["metrics_at_k"], indent=2))
        print("\n=== ABLATION STUDY (Lift by Paradigm) ===")
        print(json.dumps(metrics["ablation_study"], indent=2))

    elif args.command == "verify-chain":
        print("[*] Cryptographically verifying Audit Chain Ledger...")
        is_valid, errors, entries = audit_chain.verify_chain()
        if is_valid:
            print(f"[+] AUDIT CHAIN VERIFIED: ALL {len(entries)} BLOCKS INTACT AND UNALTERED.")
            for e in entries:
                print(f"    Block #{e['seq']} | {e['timestamp'][:19]} | {e['event_type']} | Hash: {e['this_hash'][:16]}...")
        else:
            print("[-] AUDIT CHAIN INTEGRITY BREACH DETECTED!")
            for err in errors:
                print(f"    ERROR: {err}")

    elif args.command == "budget":
        optimizer = ReviewBudgetOptimizer()
        res = optimizer.recommend_sample(lake, target_sample_size=args.samples)
        print(f"\n[+] Recommended Review Sample (Total: {res['summary']['total_recommended']} alerts)")
        print(f"    - High Information-Value Prioritized: {res['summary']['prioritized_count']}")
        print(f"    - Unbiased Random Stratum (FNR Calibration): {res['summary']['random_stratum_count']}")
        print(f"    - CSEs Represented: {res['summary']['unique_cses_covered']}")
        print("\nTop 5 Prioritized Investigation Targets:")
        for idx, item in enumerate(res["prioritized_samples"][:5], start=1):
            print(f"    {idx}. {item['alert_id']} ({item['cse_id']}) | Severity: {item['severity']} | Asset: {item['asset_id']} ({item['criticality_tier']})")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

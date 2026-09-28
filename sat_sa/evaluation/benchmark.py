"""
Benchmark Validation & Evaluation Suite for SAT-SA.
Evaluates Precision@k, Recall@k, Lift over random sampling, and performs component ablation studies.
"""

from typing import Dict, List, Any, Tuple, Optional
import pandas as pd
import numpy as np

from sat_sa.analytics.scoring import ScoringEngine


class BenchmarkEvaluator:
    """
    Evaluates prioritization precision, recall, and lift against injected ground-truth faults.
    """

    def __init__(self, scoring_engine: Optional[ScoringEngine] = None):
        self.scoring_engine = scoring_engine or ScoringEngine()

    def evaluate(self, lake, k_values: List[int] = [3, 5, 8, 10]) -> Dict[str, Any]:
        """
        Runs scoring and evaluates ranking performance against ground truth faults.
        """
        scores_df, findings_map = self.scoring_engine.evaluate_all_entities(lake)
        gt_df = lake.query_df("SELECT DISTINCT cse_id, fault_category, fault_code FROM ground_truth_faults")

        faulty_cse_ids = set(gt_df["cse_id"].unique()) if not gt_df.empty else set()
        total_cses = len(scores_df)
        total_faulty = len(faulty_cse_ids)
        base_rate = total_faulty / max(1, total_cses)

        metrics_by_k = {}
        for k in k_values:
            top_k_cses = set(scores_df.head(k)["cse_id"])
            true_positives = len(top_k_cses.intersection(faulty_cse_ids))

            precision_k = true_positives / max(1, k)
            recall_k = true_positives / max(1, total_faulty)
            lift_k = precision_k / max(1e-4, base_rate)

            metrics_by_k[f"k={k}"] = {
                "k": k,
                "precision_at_k": round(precision_k, 3),
                "recall_at_k": round(recall_k, 3),
                "lift_over_random": round(lift_k, 2),
                "true_positives_found": true_positives,
            }

        # Ablation study: compare Execution Gaps vs Negative Space vs Combined
        ablation_results = self._run_ablation(scores_df, findings_map, faulty_cse_ids, k=5)

        return {
            "summary": {
                "total_entities_evaluated": total_cses,
                "total_faulty_entities_ground_truth": total_faulty,
                "base_rate_random_sampling": round(base_rate, 3),
            },
            "metrics_at_k": metrics_by_k,
            "ablation_study": ablation_results,
            "ranked_entities": scores_df[["rank", "cse_id", "risk_score", "supervisory_status", "total_findings"]].to_dict(orient="records"),
        }

    def _run_ablation(
        self,
        scores_df: pd.DataFrame,
        findings_map: Dict[str, List[Any]],
        faulty_cses: set,
        k: int = 5,
    ) -> Dict[str, Any]:
        """
        Measures lift provided by each paradigm layer.
        """
        # Execution Gaps only
        eg_scores = {}
        # Negative Space only
        ns_scores = {}

        for cse_id, f_list in findings_map.items():
            eg_scores[cse_id] = sum(f.anomaly_score for f in f_list if f.paradigm == "EXECUTION_GAP")
            ns_scores[cse_id] = sum(f.anomaly_score for f in f_list if f.paradigm == "NEGATIVE_SPACE")

        sorted_eg = sorted(eg_scores.keys(), key=lambda x: eg_scores[x], reverse=True)[:k]
        sorted_ns = sorted(ns_scores.keys(), key=lambda x: ns_scores[x], reverse=True)[:k]
        sorted_combined = scores_df.head(k)["cse_id"].tolist()

        return {
            "execution_gaps_only": {
                "precision_at_5": round(len(set(sorted_eg).intersection(faulty_cses)) / k, 2),
                "faults_detected": len(set(sorted_eg).intersection(faulty_cses)),
            },
            "negative_space_only": {
                "precision_at_5": round(len(set(sorted_ns).intersection(faulty_cses)) / k, 2),
                "faults_detected": len(set(sorted_ns).intersection(faulty_cses)),
            },
            "full_combined_ensemble": {
                "precision_at_5": round(len(set(sorted_combined).intersection(faulty_cses)) / k, 2),
                "faults_detected": len(set(sorted_combined).intersection(faulty_cses)),
            },
        }

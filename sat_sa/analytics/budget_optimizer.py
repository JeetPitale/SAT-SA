"""
Review Budget Capacity Optimizer for SAT-SA.
Optimizes manual supervisory review time by selecting high-value investigation candidates
plus a 10% stratified random stratum for unbiased False Negative Rate (FNR) calibration.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np


class ReviewBudgetOptimizer:
    """
    Allocates examiner review time to maximize discovered operational vulnerabilities.
    """

    def recommend_sample(
        self,
        lake,
        target_sample_size: int = 30,
        random_stratum_ratio: float = 0.10,
    ) -> Dict[str, Any]:
        """
        Selects target_sample_size alerts / cases:
          - (1 - random_stratum_ratio) prioritized by multi-detector fire count & asset tier
          - random_stratum_ratio sampled uniformly at random across all CSEs
        """
        # Load alerts with asset criticality
        query = """
            SELECT 
                alt.alert_id,
                alt.cse_id,
                alt.asset_id,
                ast.criticality_tier,
                alt.severity,
                alt.rule_name,
                alt.category,
                alt.created_at,
                alt.closed_at,
                alt.disposition,
                alt.analyst_id
            FROM alerts alt
            LEFT JOIN assets ast ON alt.asset_id = ast.asset_id
        """
        alerts_df = lake.query_df(query)
        if alerts_df.empty:
            return {"prioritized_samples": [], "random_samples": [], "summary": {}}

        # Calculate Priority Heuristic Score for each alert
        # High score = High/Critical severity + Core CII asset + extreme fast/slow closure
        def calc_priority(row):
            score = 0.0
            if row["severity"] == "CRITICAL":
                score += 50.0
            elif row["severity"] == "HIGH":
                score += 30.0

            if row["criticality_tier"] == "TIER_1_CORE_CII":
                score += 40.0
            elif row["criticality_tier"] == "TIER_2_OPERATIONAL":
                score += 20.0

            if pd.notnull(row["closed_at"]) and pd.notnull(row["created_at"]):
                dur = (pd.to_datetime(row["closed_at"]) - pd.to_datetime(row["created_at"])).total_seconds()
                if dur < 180:  # Fast close anomaly
                    score += 45.0
                elif dur > 3600 * 8:  # Stale close anomaly
                    score += 25.0
            return score

        alerts_df["priority_weight"] = alerts_df.apply(calc_priority, axis=1)

        # Allocate counts
        n_random = max(2, int(target_sample_size * random_stratum_ratio))
        n_prioritized = target_sample_size - n_random

        # Prioritized subset
        prioritized_df = alerts_df.sort_values(by="priority_weight", ascending=False).head(n_prioritized)

        # Random stratum (excluding already chosen)
        remaining_df = alerts_df[~alerts_df["alert_id"].isin(prioritized_df["alert_id"])]
        random_df = remaining_df.sample(n=min(n_random, len(remaining_df)), random_state=42)

        return {
            "prioritized_samples": prioritized_df.to_dict(orient="records"),
            "random_samples": random_df.to_dict(orient="records"),
            "summary": {
                "total_recommended": len(prioritized_df) + len(random_df),
                "prioritized_count": len(prioritized_df),
                "random_stratum_count": len(random_df),
                "unique_cses_covered": len(set(prioritized_df["cse_id"]).union(set(random_df["cse_id"]))),
            },
        }

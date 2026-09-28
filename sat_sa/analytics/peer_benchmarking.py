"""
Peer Group Benchmarking & Empirical Bayes (EB) Shrinkage for SAT-SA.
Ensures small entities with low sample counts are stabilized and not ranked on random noise.
"""

from typing import Dict, List, Any, Tuple
import numpy as np
import pandas as pd


class PeerBenchmarkingEngine:
    """
    Groups CSEs into sector and size-aligned peer cohorts and applies Empirical Bayes shrinkage.
    """

    def get_peer_groups(self, lake) -> pd.DataFrame:
        """
        Creates peer cohorts based on sector and asset count size bins.
        """
        query = """
            SELECT 
                cse_id, 
                sector,
                count(distinct asset_id) as asset_count,
                case 
                    when count(distinct asset_id) < 80 then 'SMALL'
                    when count(distinct asset_id) < 200 then 'MEDIUM'
                    else 'LARGE'
                end as size_bin
            FROM assets
            GROUP BY cse_id, sector
        """
        df = lake.query_df(query)
        if df.empty:
            return pd.DataFrame()

        df["peer_group_id"] = df["sector"] + "_" + df["size_bin"]
        return df

    def apply_poisson_gamma_shrinkage(
        self,
        observed_counts: np.ndarray,
        exposure_days: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Empirical Bayes Poisson-Gamma Shrinkage:
          Prior: lambda ~ Gamma(alpha, beta) estimated from peer group moments
          Posterior Mean: (observed_count + alpha) / (exposure_days + beta)
          Returns: (shrunk_rates, variance_estimates)
        """
        raw_rates = observed_counts / np.maximum(exposure_days, 1.0)
        mu = float(np.mean(raw_rates))
        var = float(np.var(raw_rates)) + 1e-6

        # Method of moments
        alpha = max(0.1, (mu ** 2) / var)
        beta = max(0.1, mu / var)

        shrunk_rates = (observed_counts + alpha) / (exposure_days + beta)
        shrunk_variance = (observed_counts + alpha) / ((exposure_days + beta) ** 2)

        return shrunk_rates, shrunk_variance

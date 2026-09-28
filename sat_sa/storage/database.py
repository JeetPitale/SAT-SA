"""
DuckDB Database & Parquet Data Lake Storage Engine for SAT-SA.
Supports zero-copy Arrow memory transfers and fast vectorised SQL queries.
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
import duckdb
import pandas as pd
from sat_sa.config import PARQUET_LAKE_DIR


class DataLakeEngine:
    """
    Manages columnar Parquet datasets and executes zero-overhead analytical queries via DuckDB.
    """

    def __init__(self, lake_dir: Path = PARQUET_LAKE_DIR):
        self.lake_dir = lake_dir
        self.lake_dir.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(database=":memory:")
        self._register_views()

    def _register_views(self):
        """Registers views over parquet files in the lake for instant SQL query access."""
        tables = [
            "alerts",
            "cases",
            "escalations",
            "assets",
            "analysts",
            "self_assessed_metrics",
            "ground_truth_faults",
            "scores",
        ]
        for tbl in tables:
            parquet_path = self.lake_dir / f"{tbl}.parquet"
            if parquet_path.exists():
                # Escape path properly for duckdb
                path_str = str(parquet_path).replace("'", "''")
                try:
                    self.conn.execute(
                        f"CREATE OR REPLACE VIEW {tbl} AS SELECT * FROM read_parquet('{path_str}')"
                    )
                except Exception:
                    pass

    def write_table(self, table_name: str, df: pd.DataFrame):
        """Writes a pandas DataFrame to Parquet and updates the DuckDB view."""
        parquet_path = self.lake_dir / f"{table_name}.parquet"
        df.to_parquet(parquet_path, index=False, engine="pyarrow", compression="snappy")
        self._register_views()

    def query_df(self, query: str, params: Optional[List[Any]] = None) -> pd.DataFrame:
        """Executes an arbitrary SQL query and returns a pandas DataFrame."""
        self._register_views()
        if params:
            return self.conn.execute(query, params).df()
        return self.conn.execute(query).df()

    def table_exists(self, table_name: str) -> bool:
        parquet_path = self.lake_dir / f"{table_name}.parquet"
        return parquet_path.exists()

    def get_cse_ids(self) -> List[str]:
        for tbl in ["assets", "alerts", "cases", "self_assessed_metrics"]:
            if self.table_exists(tbl):
                try:
                    res = self.query_df(f"SELECT DISTINCT cse_id FROM {tbl} WHERE cse_id IS NOT NULL ORDER BY cse_id")
                    if isinstance(res, pd.DataFrame) and "cse_id" in res.columns and not res.empty:
                        return [str(x) for x in res["cse_id"].dropna().tolist()]
                except Exception:
                    pass
        return []


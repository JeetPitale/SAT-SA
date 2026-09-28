"""
Ingestion and Normalization Pipeline for SAT-SA.
Ingests multi-source data dumps, generates cryptographic submission receipts,
validates quality, and stages into the DuckDB columnar data lake.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd

from sat_sa.storage.database import DataLakeEngine
from sat_sa.audit_chain import AuditChain
from sat_sa.ingestion.data_quality import DataQualityGate


class IngestionEngine:
    """
    Ingests SOC telemetry tables, applies data quality gates, and registers audit-chain entries.
    """

    def __init__(self, lake: Optional[DataLakeEngine] = None, audit_chain: Optional[AuditChain] = None):
        self.lake = lake or DataLakeEngine()
        self.audit_chain = audit_chain or AuditChain()
        self.quality_gate = DataQualityGate()

    def ingest_datasets(
        self,
        tables: Dict[str, pd.DataFrame],
        submission_source: str = "SYNTHETIC_GENERATOR",
        actor: str = "NCIIPC_INGEST_PIPELINE",
    ) -> Dict[str, Any]:
        """
        Stores datasets in the lake and records a cryptographic submission event.
        """
        table_summaries = {}
        for name, df in tables.items():
            self.lake.write_table(name, df)
            table_summaries[name] = {
                "row_count": len(df),
                "columns": list(df.columns),
            }

        # Run Data Quality checks across all unique CSEs
        quality_reports = {}
        alerts_df = tables.get("alerts", pd.DataFrame())
        cases_df = tables.get("cases", pd.DataFrame())
        escalations_df = tables.get("escalations", pd.DataFrame())
        assets_df = tables.get("assets", pd.DataFrame())

        cse_ids = sorted(list(set(assets_df["cse_id"].unique()) if not assets_df.empty else []))
        for cse_id in cse_ids:
            q_res = self.quality_gate.evaluate_cse_data_quality(
                cse_id, alerts_df, cases_df, escalations_df, assets_df
            )
            quality_reports[cse_id] = q_res

        # Append submission to cryptographic audit chain
        chain_entry = self.audit_chain.append_event(
            event_type="submission",
            actor=actor,
            payload={
                "source": submission_source,
                "tables": table_summaries,
                "cse_count": len(cse_ids),
                "cse_ids": cse_ids,
            },
        )

        return {
            "status": "SUCCESS",
            "audit_entry": chain_entry,
            "table_summaries": table_summaries,
            "quality_reports": quality_reports,
        }

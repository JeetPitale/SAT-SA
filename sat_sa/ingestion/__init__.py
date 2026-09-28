"""
Ingestion and data normalization package for SAT-SA.
"""

from sat_sa.ingestion.normalizer import IngestionEngine
from sat_sa.ingestion.data_quality import DataQualityGate

__all__ = ["IngestionEngine", "DataQualityGate"]

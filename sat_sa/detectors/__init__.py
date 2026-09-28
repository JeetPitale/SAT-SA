"""
Detectors package for SAT-SA.
"""

from sat_sa.detectors.base import BaseDetector, SupervisoryFinding
from sat_sa.detectors.execution_gaps import (
    FastClosureDetector,
    TemplateNotesDetector,
    PreSLAGoodhartDetector,
    AnalystConcentrationDetector,
    MetricDiscrepancyDetector,
)
from sat_sa.detectors.negative_space import (
    SilentAssetsDetector,
    MissingCategoriesDetector,
    OrphanAlertsDetector,
    NightShiftSilenceDetector,
)
from sat_sa.detectors.unsupervised import UnsupervisedEntityAnomalyDetector

__all__ = [
    "BaseDetector",
    "SupervisoryFinding",
    "FastClosureDetector",
    "TemplateNotesDetector",
    "PreSLAGoodhartDetector",
    "AnalystConcentrationDetector",
    "MetricDiscrepancyDetector",
    "SilentAssetsDetector",
    "MissingCategoriesDetector",
    "OrphanAlertsDetector",
    "NightShiftSilenceDetector",
    "UnsupervisedEntityAnomalyDetector",
]

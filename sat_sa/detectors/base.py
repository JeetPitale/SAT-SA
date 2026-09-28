"""
Base Detector and Finding Schema for SAT-SA.
Every finding carries complete evidence IDs, peer baselines, and supervisory recommendations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import hashlib
import json
import pandas as pd
from pydantic import BaseModel, Field


class SupervisoryFinding(BaseModel):
    """
    Standardized, auditable finding payload delivered to NCIIPC supervisors.
    """
    finding_id: str
    cse_id: str
    detector_code: str
    detector_name: str
    paradigm: str  # EXECUTION_GAP, NEGATIVE_SPACE, UNSUPERVISED
    capability_area: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    anomaly_score: float  # 0.0 to 100.0
    evidence: Dict[str, Any]
    peer_baseline: Dict[str, Any]
    feature_contributions: Optional[Dict[str, float]] = None
    supervisory_recommendation: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class BaseDetector(ABC):
    """Abstract base class for all operational audit detectors."""

    def __init__(self, code: str, name: str, capability_area: str, paradigm: str):
        self.code = code
        self.name = name
        self.capability_area = capability_area
        self.paradigm = paradigm

    @abstractmethod
    def run(
        self,
        lake_conn,
        cse_id: str,
        peer_group_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> List[SupervisoryFinding]:
        """Executes detection logic for a given CSE and returns supervisory findings."""
        pass

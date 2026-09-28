"""
MinHash & TF-IDF Template Note / Boilerplate Investigation Detector (EG-04).
Detects copy-pasted and near-duplicate closure notes across SOC analysts and cases.
"""

import re
from typing import List, Dict, Any, Tuple
from datasketch import MinHash, MinHashLSH
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class TemplateNoteAnalyzer:
    """
    Identifies high-frequency duplicate / near-duplicate closure text using MinHash LSH and TF-IDF.
    """

    def __init__(self, jaccard_threshold: float = 0.85, num_perm: int = 128):
        self.jaccard_threshold = jaccard_threshold
        self.num_perm = num_perm

    def _shingle(self, text: str, k: int = 3) -> set:
        clean = re.sub(r"[^\w\s]", "", text.lower()).strip()
        tokens = clean.split()
        if len(tokens) < k:
            return {clean}
        return {" ".join(tokens[i : i + k]) for i in range(len(tokens) - k + 1)}

    def analyze_cases(self, cases_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyzes case closure notes for a CSE and returns template clustering metrics.
        """
        if cases_df.empty or "closure_note" not in cases_df.columns:
            return {"duplicate_ratio": 0.0, "clusters": [], "sample_boilerplate": []}

        valid_cases = cases_df[cases_df["closure_note"].notnull() & (cases_df["closure_note"].str.len() > 5)]
        if len(valid_cases) < 5:
            return {"duplicate_ratio": 0.0, "clusters": [], "sample_boilerplate": []}

        lsh = MinHashLSH(threshold=self.jaccard_threshold, num_perm=self.num_perm)
        minhashes = {}

        for _, row in valid_cases.iterrows():
            cid = str(row["case_id"])
            shingles = self._shingle(str(row["closure_note"]))
            m = MinHash(num_perm=self.num_perm)
            for s in shingles:
                m.update(s.encode("utf8"))
            minhashes[cid] = m
            try:
                lsh.insert(cid, m)
            except ValueError:
                pass

        # Find clusters of duplicate notes
        visited = set()
        clusters: List[List[str]] = []
        for cid, m in minhashes.items():
            if cid in visited:
                continue
            neighbors = lsh.query(m)
            if len(neighbors) > 3:
                for n in neighbors:
                    visited.add(n)
                clusters.append(neighbors)

        total_in_clusters = sum(len(c) for c in clusters)
        duplicate_ratio = total_in_clusters / max(1, len(valid_cases))

        # Extract sample duplicate text
        sample_boilerplate = []
        for c in clusters[:3]:
            sample_note = valid_cases[valid_cases["case_id"] == c[0]]["closure_note"].values[0]
            sample_boilerplate.append({
                "cluster_size": len(c),
                "case_ids_sample": c[:5],
                "note_text": sample_note,
            })

        return {
            "duplicate_ratio": round(duplicate_ratio, 3),
            "total_cases_analyzed": len(valid_cases),
            "total_clustered_cases": total_in_clusters,
            "cluster_count": len(clusters),
            "sample_boilerplate": sample_boilerplate,
        }

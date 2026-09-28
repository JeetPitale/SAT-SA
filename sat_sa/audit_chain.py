"""
Tamper-Evident Audit Chain Ledger for SAT-SA.
Implements a cryptographic SHA-256 hash-chain linking all data submissions,
analysis runs, configuration states, and supervisor findings.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from sat_sa.config import AUDIT_LOG_FILE


class AuditChain:
    """
    Cryptographic hash-chain ledger ensuring audit integrity and non-repudiation.
    Each entry contains:
      - seq: strictly monotonic integer
      - timestamp: ISO 8601 UTC
      - event_type: submission | analysis_run | finding_review | config_change
      - actor: supervisor ID or system identifier
      - payload_hash: SHA-256 of the event specific payload
      - config_hash: SHA-256 of the active rule/weight configuration
      - prev_hash: SHA-256 of the prior block
      - this_hash: SHA-256 of (seq + timestamp + event_type + payload_hash + config_hash + prev_hash)
    """

    def __init__(self, log_path: Path = AUDIT_LOG_FILE):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def _get_last_entry(self) -> Optional[Dict[str, Any]]:
        if not self.log_path.exists() or self.log_path.stat().st_size == 0:
            return None
        last_line = ""
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    last_line = line
        if last_line:
            try:
                return json.loads(last_line)
            except Exception:
                return None
        return None

    def append_event(
        self,
        event_type: str,
        actor: str,
        payload: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Appends a new immutable entry to the cryptographic audit chain."""
        last_entry = self._get_last_entry()
        seq = (last_entry["seq"] + 1) if last_entry else 1
        prev_hash = last_entry["this_hash"] if last_entry else "0" * 64

        payload_serialized = json.dumps(payload, sort_keys=True, default=str)
        payload_hash = hashlib.sha256(payload_serialized.encode("utf-8")).hexdigest()

        config_serialized = json.dumps(config or {}, sort_keys=True, default=str)
        config_hash = hashlib.sha256(config_serialized.encode("utf-8")).hexdigest()

        timestamp = datetime.now(timezone.utc).isoformat()

        entry_data = {
            "seq": seq,
            "timestamp": timestamp,
            "event_type": event_type,
            "actor": actor,
            "payload_hash": payload_hash,
            "config_hash": config_hash,
            "prev_hash": prev_hash,
            "payload_summary": {
                k: (v if not isinstance(v, (list, dict)) or len(str(v)) < 100 else f"[{type(v).__name__} length={len(v)}]")
                for k, v in payload.items()
            },
        }

        # Calculate this_hash strictly on canonical representation
        hash_seed = f"{seq}|{timestamp}|{event_type}|{actor}|{payload_hash}|{config_hash}|{prev_hash}"
        entry_data["this_hash"] = hashlib.sha256(hash_seed.encode("utf-8")).hexdigest()

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry_data) + "\n")

        return entry_data

    def verify_chain(self) -> Tuple[bool, List[str], List[Dict[str, Any]]]:
        """
        Validates the complete hash-chain from Genesis block to head.
        Returns: (is_valid, error_list, all_entries)
        """
        if not self.log_path.exists() or self.log_path.stat().st_size == 0:
            return True, ["Chain is empty (no entries yet)."], []

        entries: List[Dict[str, Any]] = []
        errors: List[str] = []

        with open(self.log_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    entries.append(entry)
                except Exception as e:
                    errors.append(f"Line {line_no}: Malformed JSON - {str(e)}")

        if errors:
            return False, errors, entries

        expected_prev_hash = "0" * 64
        for idx, entry in enumerate(entries):
            seq = entry.get("seq")
            if seq != idx + 1:
                errors.append(f"Entry #{idx+1}: Sequence mismatch (expected {idx+1}, got {seq})")

            if entry.get("prev_hash") != expected_prev_hash:
                errors.append(
                    f"Entry #{seq}: Broken hash link! prev_hash '{entry.get('prev_hash')[:12]}...' "
                    f"does not match expected '{expected_prev_hash[:12]}...'"
                )

            # Re-verify this_hash calculation
            hash_seed = (
                f"{entry['seq']}|{entry['timestamp']}|{entry['event_type']}|"
                f"{entry['actor']}|{entry['payload_hash']}|{entry['config_hash']}|{entry['prev_hash']}"
            )
            recalculated = hashlib.sha256(hash_seed.encode("utf-8")).hexdigest()
            if entry.get("this_hash") != recalculated:
                errors.append(
                    f"Entry #{seq}: Invalid block hash signature! Tampering detected in block data."
                )

            expected_prev_hash = entry.get("this_hash", "")

        is_valid = len(errors) == 0
        return is_valid, errors, entries

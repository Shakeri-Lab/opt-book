"""Central verification for content-addressed harness wheels and claim records.

Chapter harness wheels remain immutable mathematical artifacts. This module is
book-build infrastructure: it removes repeated path, hashing, and JSON
orchestration from learner-visible code without weakening any verification.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def _payload_sha256(payload: dict[str, Any]) -> str:
    clean = dict(payload)
    clean.pop("payload_sha256", None)
    encoded = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


@dataclass(frozen=True)
class HarnessPin:
    """A verified, activated chapter harness wheel."""

    harness_ref: str
    wheel_path: Path
    wheel_sha256: str
    manifest: dict[str, Any]


def activate_harness(harness_ref: str, expected_sha256: str) -> HarnessPin:
    """Verify and activate one vendored chapter wheel."""

    manifest_path = ROOT / "artifacts" / "harness" / harness_ref / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    wheel_path = manifest_path.parent / manifest["wheel"]
    observed = sha256(wheel_path.read_bytes()).hexdigest()
    if observed != expected_sha256 or observed != manifest["wheel_sha256"]:
        raise AssertionError(f"{harness_ref}: wheel digest mismatch")
    if manifest["harness_ref"] != harness_ref:
        raise AssertionError(f"{harness_ref}: manifest identity mismatch")
    resolved = str(wheel_path.resolve())
    if resolved not in sys.path:
        sys.path.insert(0, resolved)
    return HarnessPin(harness_ref, wheel_path, observed, manifest)


def verify_claim(
    claim_id: str,
    *,
    expected_harness: HarnessPin | None = None,
) -> dict[str, Any]:
    """Load a registered JSON claim and verify identity and payload digest."""

    contract = json.loads((ROOT / "contracts" / "claims.yml").read_text())
    registered = {
        item["claim_id"]: item
        for item in contract["claims"]
        if str(item["evidence"]).endswith(".json")
    }
    if claim_id not in registered:
        raise KeyError(f"{claim_id}: no registered JSON evidence")
    evidence_path = ROOT / registered[claim_id]["evidence"]
    artifact = json.loads(evidence_path.read_text())
    if artifact.get("claim_id") != claim_id:
        raise AssertionError(f"{claim_id}: artifact identity mismatch")
    if artifact.get("payload_sha256") != _payload_sha256(artifact):
        raise AssertionError(f"{claim_id}: payload digest mismatch")
    if expected_harness is not None:
        if artifact.get("harness_ref") != expected_harness.harness_ref:
            raise AssertionError(f"{claim_id}: harness reference mismatch")
        if artifact.get("harness_wheel_sha256") != expected_harness.wheel_sha256:
            raise AssertionError(f"{claim_id}: harness wheel mismatch")
    return artifact

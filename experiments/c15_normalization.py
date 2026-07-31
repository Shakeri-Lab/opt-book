"""Verify the C15 invariance and arithmetic witness."""
from hashlib import sha256
import json
from pathlib import Path
import sys
import numpy as np
from _evidence_verify import verify_claim

root = Path(__file__).resolve().parents[1]; mp = root / "artifacts/harness/ch-15/manifest.json"
manifest = json.loads(mp.read_text()); wheel = mp.parent / manifest["wheel"]; digest = sha256(wheel.read_bytes()).hexdigest(); assert digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))
from trainable_harness import centered_normalize, rms_normalize, normalization_jacobian, raw_and_centered_variance
x = np.array([-2., -1., 1., 2.]); shifted = x + 10; raw, centered = raw_and_centered_variance(np.array([9998, 9999, 10001, 10002]))
record = {"schema_version": 1, "claim_id": "c15-invariance-001", "phenomenon_id": "c15-invariance-choice", "chapter": "c15", "provenance_class": "a", "hypothesis": "Centering and RMS-only normalization impose different invariances, and centered arithmetic avoids raw-moment cancellation.", "hardware_claim_boundary": "Deterministic small-vector calculation; epsilon-zero Jacobian excludes degenerate states.", "harness_ref": "ch-15", "harness_wheel_sha256": digest, "result": {"centered_shift_deviation": float(np.max(abs(centered_normalize(x) - centered_normalize(shifted)))), "rms_shift_deviation": float(np.max(abs(rms_normalize(x) - rms_normalize(shifted)))), "centered_jacobian_rank": int(np.linalg.matrix_rank(normalization_jacobian(x, centered=True), tol=1e-10)), "rms_jacobian_rank": int(np.linalg.matrix_rank(normalization_jacobian(x, centered=False), tol=1e-10)), "float32_raw_variance": raw, "float32_centered_variance": centered}}
verify_claim("c15-invariance-001.json", record, absolute_tolerance=1e-12)

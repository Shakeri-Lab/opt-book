"""Verify the C17 matrix-norm and polar witness."""
from hashlib import sha256
import json
from pathlib import Path
import sys
import numpy as np
from _evidence_verify import verify_claim

root = Path(__file__).resolve().parents[1]; mp = root / "artifacts/harness/ch-17/manifest.json"
manifest = json.loads(mp.read_text()); wheel = mp.parent / manifest["wheel"]; digest = sha256(wheel.read_bytes()).hexdigest(); assert digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))
from trainable_harness import newton_schulz_polar, norm_steepest_directions, polar_factor
g = np.zeros((6, 4)); g[:4, :] = np.diag([9., 3., 1., .2]); polar = polar_factor(g); approximation, residuals = newton_schulz_polar(g, 12)
record = {"schema_version": 1, "claim_id": "c17-update-norm-001", "phenomenon_id": "c17-norm-chooses-update", "chapter": "c17", "provenance_class": "a", "hypothesis": "Changing the update norm changes the steepest matrix direction.", "hardware_claim_boundary": "Deterministic matrix calculation; no optimizer throughput or end-task efficiency claim.", "harness_ref": "ch-17", "harness_wheel_sha256": digest, "result": {"gradient_singular_values": np.linalg.svd(g, compute_uv=False).tolist(), "polar_singular_values": np.linalg.svd(polar, compute_uv=False).tolist(), "newton_schulz_residuals": residuals.tolist(), "approximation_error": float(np.linalg.norm(approximation - polar, "fro")), "inner_products": {name: float(np.sum(g * direction)) for name, direction in norm_steepest_directions(g).items()}}}
verify_claim("c17-update-norm-001.json", record, absolute_tolerance=1e-12)

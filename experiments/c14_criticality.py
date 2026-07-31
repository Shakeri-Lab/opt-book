"""Verify the C14 moment-versus-spectrum witness."""
from hashlib import sha256
import json
from pathlib import Path
import sys
import numpy as np
from _evidence_verify import verify_claim

root = Path(__file__).resolve().parents[1]; mp = root / "artifacts/harness/ch-14/manifest.json"
manifest = json.loads(mp.read_text()); wheel = mp.parent / manifest["wheel"]; digest = sha256(wheel.read_bytes()).hexdigest(); assert digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))
from trainable_harness import deep_linear_product, relu_variance_trace
rng = np.random.default_rng(6214); n = 24; depth = 12
gaussian = [rng.normal(size=(n, n)) / np.sqrt(n) for _ in range(depth)]
orthogonal = [np.linalg.qr(rng.normal(size=(n, n)))[0] for _ in range(depth)]
sg = np.linalg.svd(deep_linear_product(gaussian), compute_uv=False); so = np.linalg.svd(deep_linear_product(orthogonal), compute_uv=False)
record = {"schema_version": 1, "claim_id": "c14-criticality-001", "phenomenon_id": "c14-average-criticality", "chapter": "c14", "provenance_class": "a", "hypothesis": "Average variance preservation does not control every singular direction.", "hardware_claim_boundary": "Seeded CPU linear-algebra witness; not a theorem about finite nonlinear networks.", "harness_ref": "ch-14", "harness_wheel_sha256": digest, "result": {"relu_final_variance": {str(c): float(relu_variance_trace(1, c, 20)[-1]) for c in (1., 2., 3.)}, "gaussian_product": {"mean_squared_singular_value": float(np.mean(sg**2)), "minimum": float(sg[-1]), "maximum": float(sg[0])}, "orthogonal_product": {"mean_squared_singular_value": float(np.mean(so**2)), "minimum": float(so[-1]), "maximum": float(so[0])}, "seed": 6214, "width": n, "depth": depth}}
verify_claim("c14-criticality-001.json", record, absolute_tolerance=1e-10)

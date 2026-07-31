"""Verify the C14 finite-width gated Jacobian product."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np

from _evidence_verify import verify_claim


root = Path(__file__).resolve().parents[1]
manifest_path = root / "artifacts/harness/ch-14/manifest.json"
manifest = json.loads(manifest_path.read_text())
wheel = manifest_path.parent / manifest["wheel"]
digest = sha256(wheel.read_bytes()).hexdigest()
assert digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))
from trainable_harness import deep_linear_product

seed = int(sha256(b"c14-gated-product").hexdigest()[:8], 16)
rng = np.random.default_rng(seed)
width, depth = 24, 12
state = rng.normal(size=width)
factors, active = [], []
for _ in range(depth):
    weights = rng.normal(size=(width, width)) * np.sqrt(2 / width)
    preactivation = weights @ state
    gate = (preactivation > 0).astype(float)
    active.append(int(gate.sum()))
    factors.append(gate[:, None] * weights)
    state = np.maximum(preactivation, 0)

singular_values = np.linalg.svd(
    deep_linear_product(factors), compute_uv=False
)
record = {
    "schema_version": 1,
    "claim_id": "c14-gated-product-001",
    "phenomenon_id": "c14-average-criticality",
    "chapter": "c14",
    "provenance_class": "a",
    "hypothesis": "ReLU gates bend the deep-linear isometry control by inserting data-dependent rank loss and anisotropy even at variance-critical weight scale.",
    "hardware_claim_boundary": "One seeded finite-width CPU witness; not a distributional theorem for trained Jacobians.",
    "harness_ref": "ch-14",
    "harness_wheel_sha256": digest,
    "result": {
        "seed": seed,
        "width": width,
        "depth": depth,
        "weight_variance": 2 / width,
        "active_coordinates_by_layer": active,
        "jacobian_rank_tolerance_1e-10": int(
            np.sum(singular_values > 1e-10)
        ),
        "mean_squared_singular_value": float(np.mean(singular_values**2)),
        "maximum_singular_value": float(singular_values[0]),
        "minimum_singular_value": float(singular_values[-1]),
        "singular_values": singular_values.tolist(),
    },
}
verify_claim("c14-gated-product-001.json", record, absolute_tolerance=1e-12)

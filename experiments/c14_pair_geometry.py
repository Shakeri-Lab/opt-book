"""Verify the C14 critical-ReLU pair-geometry witness."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np

from _evidence_verify import verify_claim


root = Path(__file__).resolve().parents[1]
manifest_path = root / "artifacts/harness/ch-14-r2/manifest.json"
manifest = json.loads(manifest_path.read_text())
wheel = manifest_path.parent / manifest["wheel"]
digest = sha256(wheel.read_bytes()).hexdigest()
assert digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))
from trainable_harness import relu_correlation_trace

seed = int(sha256(b"c14-pair-geometry-r2").hexdigest()[:8], 16)
rng = np.random.default_rng(seed)
initial_correlation, width, depth, trials = 0.5, 128, 64, 2048
check_depths = (1, 4, 16, 64)
wide_trace = relu_correlation_trace(initial_correlation, depth)

correlations = np.full(trials, initial_correlation)
finite_summary = {}
for layer in range(1, depth + 1):
    first = rng.normal(size=(trials, width))
    auxiliary = rng.normal(size=(trials, width))
    second = (
        correlations[:, None] * first
        + np.sqrt(np.maximum(0.0, 1.0 - correlations**2))[:, None]
        * auxiliary
    )
    first = np.maximum(first, 0.0)
    second = np.maximum(second, 0.0)
    correlations = np.sum(first * second, axis=1) / (
        np.linalg.norm(first, axis=1) * np.linalg.norm(second, axis=1)
    )
    if layer in check_depths:
        finite_summary[str(layer)] = {
            "mean": float(np.mean(correlations)),
            "median": float(np.median(correlations)),
            "quantile_10": float(np.quantile(correlations, 0.1)),
            "quantile_90": float(np.quantile(correlations, 0.9)),
        }

record = {
    "schema_version": 1,
    "claim_id": "c14-pair-geometry-001",
    "phenomenon_id": "c14-average-criticality",
    "chapter": "c14",
    "provenance_class": "a",
    "hypothesis": (
        "Critical zero-bias ReLU propagation can preserve each input's "
        "second moment while normalized pair separation decays with depth."
    ),
    "hardware_claim_boundary": (
        "Laptop-CPU wide-limit control plus seeded finite-width Gaussian-layer "
        "simulation; not a claim about trained representations."
    ),
    "harness_ref": "ch-14-r2",
    "harness_wheel_sha256": digest,
    "result": {
        "seed": seed,
        "initial_correlation": initial_correlation,
        "width": width,
        "depth": depth,
        "trials": trials,
        "wide_correlation": {
            str(layer): float(wide_trace[layer]) for layer in check_depths
        },
        "wide_final_angle_radians": float(np.arccos(wide_trace[-1])),
        "finite_width_correlation": finite_summary,
    },
}
verify_claim("c14-pair-geometry-001.json", record, absolute_tolerance=1e-10)

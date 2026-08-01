"""Verify the C14 exact depth-to-width fluctuation control."""

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
from trainable_harness import relu_moment_fluctuation_variance

seed = int(sha256(b"c14-depth-width-r2").hexdigest()[:8], 16)
rng = np.random.default_rng(seed)
widths = (32, 128, 512)
ratios = (1 / 32, 1 / 16, 1 / 8)
trials = 200_000
points = []
for width in widths:
    for ratio in ratios:
        depth = round(ratio * width)
        moment_ratios = np.ones(trials)
        for _ in range(depth):
            active = rng.binomial(width, 0.5, size=trials)
            squared_sum = np.zeros(trials)
            nonzero = active > 0
            squared_sum[nonzero] = rng.chisquare(active[nonzero])
            moment_ratios *= 2.0 * squared_sum / width
        points.append(
            {
                "width": width,
                "depth": depth,
                "depth_over_width": ratio,
                "sample_mean": float(np.mean(moment_ratios)),
                "sample_variance": float(np.var(moment_ratios)),
                "exact_variance": relu_moment_fluctuation_variance(
                    width, depth
                ),
            }
        )

record = {
    "schema_version": 1,
    "claim_id": "c14-depth-width-001",
    "phenomenon_id": "c14-average-criticality",
    "chapter": "c14",
    "provenance_class": "a",
    "hypothesis": (
        "At critical zero-bias ReLU scale, finite-width moment fluctuations "
        "are controlled by depth over width only in a declared perturbative "
        "regime."
    ),
    "hardware_claim_boundary": (
        "Exact finite-width Gaussian model calculation plus seeded CPU Monte "
        "Carlo; not a trained-network width prescription."
    ),
    "harness_ref": "ch-14-r2",
    "harness_wheel_sha256": digest,
    "result": {
        "seed": seed,
        "trials": trials,
        "variance_denominator": trials,
        "points": points,
    },
}
verify_claim("c14-depth-width-001.json", record, absolute_tolerance=1e-10)

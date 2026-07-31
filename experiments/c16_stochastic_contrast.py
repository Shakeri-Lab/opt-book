"""Verify the C16 additive-noise contrast."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np

from _evidence_verify import verify_claim


root = Path(__file__).resolve().parents[1]
manifest_path = root / "artifacts/harness/ch-16/manifest.json"
manifest = json.loads(manifest_path.read_text())
wheel = manifest_path.parent / manifest["wheel"]
digest = sha256(wheel.read_bytes()).hexdigest()
assert digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))
from trainable_harness import valley_loss_gradient_hessian

seed = int(sha256(b"c16-stochastic-contrast").hexdigest()[:8], 16)
rng = np.random.default_rng(seed)
state = np.zeros(2)
step_size, noise_sd, steps = 0.2, 0.01, 350
losses, top_curvatures = [], []
for _ in range(steps + 1):
    loss, gradient, hessian = valley_loss_gradient_hessian(state)
    losses.append(loss)
    top_curvatures.append(float(np.linalg.eigvalsh(hessian)[-1]))
    state -= step_size * (
        gradient + rng.normal(scale=noise_sd, size=2)
    )

losses = np.asarray(losses)
top_curvatures = np.asarray(top_curvatures)
crossings = np.flatnonzero(top_curvatures > 2 / step_size)
record = {
    "schema_version": 1,
    "claim_id": "c16-stochastic-contrast-001",
    "phenomenon_id": "c16-moving-boundary",
    "chapter": "c16",
    "provenance_class": "a",
    "hypothesis": "Small additive gradient noise preserves the moving-curvature crossing in the toy valley while shifting its timing and increasing loss nonmonotonicity.",
    "hardware_claim_boundary": "One seeded additive-noise CPU contrast; not a theorem about mini-batch edge-of-stability behavior.",
    "harness_ref": "ch-16",
    "harness_wheel_sha256": digest,
    "result": {
        "seed": seed,
        "step_size": step_size,
        "gradient_noise_sd_per_coordinate": noise_sd,
        "steps": steps,
        "first_crossing_step": int(crossings[0]),
        "number_loss_increases": int(np.sum(np.diff(losses) > 0)),
        "final_loss": float(losses[-1]),
        "maximum_top_curvature": float(top_curvatures.max()),
        "final_state": state.tolist(),
    },
}
verify_claim("c16-stochastic-contrast-001.json", record, absolute_tolerance=1e-12)

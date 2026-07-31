"""Verify the C17 weight-versus-update spectrum trace."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np

from _evidence_verify import verify_claim


root = Path(__file__).resolve().parents[1]
manifest_path = root / "artifacts/harness/ch-17/manifest.json"
manifest = json.loads(manifest_path.read_text())
wheel = manifest_path.parent / manifest["wheel"]
digest = sha256(wheel.read_bytes()).hexdigest()
assert digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))
from trainable_harness import polar_factor

seed = int(sha256(b"c17-weight-update-spectrum").hexdigest()[:8], 16)
rng = np.random.default_rng(seed)
target = rng.normal(size=(6, 4))
initial_a = 0.2 * rng.normal(size=(6, 4))
initial_b = 0.2 * rng.normal(size=(4, 4))
step_size, steps = 0.08, 20
by_rule = {}
for rule in ("frobenius", "polar"):
    factor_a, factor_b = initial_a.copy(), initial_b.copy()
    update_spectra, weight_spectra = [], []
    initial_loss = float(0.5 * np.mean((factor_a @ factor_b - target) ** 2))
    for _ in range(steps):
        residual = factor_a @ factor_b - target
        gradient_a = residual @ factor_b.T / residual.size
        gradient_b = factor_a.T @ residual / residual.size
        if rule == "frobenius":
            direction_a = -gradient_a / np.linalg.norm(gradient_a, "fro")
            direction_b = -gradient_b / np.linalg.norm(gradient_b, "fro")
        else:
            direction_a = -polar_factor(gradient_a)
            direction_b = -polar_factor(gradient_b)
        update_spectra.append(
            np.linalg.svd(step_size * direction_a, compute_uv=False)
        )
        weight_spectra.append(
            np.linalg.svd(factor_a, compute_uv=False)
        )
        factor_a += step_size * direction_a
        factor_b += step_size * direction_b

    update_spectra = np.asarray(update_spectra)
    weight_spectra = np.asarray(weight_spectra)
    by_rule[rule] = {
        "initial_loss": initial_loss,
        "loss_after_20": float(
            0.5 * np.mean((factor_a @ factor_b - target) ** 2)
        ),
        "update_singular_values_step_0": update_spectra[0].tolist(),
        "update_singular_values_step_19": update_spectra[-1].tolist(),
        "weight_singular_values_step_0": weight_spectra[0].tolist(),
        "weight_singular_values_step_19": weight_spectra[-1].tolist(),
        "maximum_update_singular_spread_over_trace": float(
            np.max(update_spectra.max(axis=1) - update_spectra.min(axis=1))
        ),
        "maximum_weight_singular_spread_over_trace": float(
            np.max(weight_spectra.max(axis=1) - weight_spectra.min(axis=1))
        ),
    }

record = {
    "schema_version": 1,
    "claim_id": "c17-weight-update-spectrum-001",
    "phenomenon_id": "c17-norm-chooses-update",
    "chapter": "c17",
    "provenance_class": "a",
    "hypothesis": "A polar update has an isometric update spectrum while the factor it changes retains a non-isometric, evolving weight spectrum.",
    "hardware_claim_boundary": "Seeded twenty-step factorized least-squares CPU control with matched initialization and external step scale; not an optimizer ranking.",
    "harness_ref": "ch-17",
    "harness_wheel_sha256": digest,
    "result": {
        "seed": seed,
        "step_size": step_size,
        "steps": steps,
        "factor_shapes": {"A": [6, 4], "B": [4, 4]},
        "routed_parameters": ["A", "B"],
        "excluded_parameter_example": "bias vector",
        "by_rule": by_rule,
    },
}
verify_claim(
    "c17-weight-update-spectrum-001.json",
    record,
    absolute_tolerance=1e-12,
)

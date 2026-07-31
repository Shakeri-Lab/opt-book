"""Verify the Coda incident diagnosis without rewriting its artifact."""

from hashlib import sha256
import json
from pathlib import Path

import numpy as np

from _evidence_verify import verify_claim


root = Path(__file__).resolve().parents[1]
manifest_path = root / "artifacts/harness/ch-17/manifest.json"
manifest = json.loads(manifest_path.read_text())
wheel = manifest_path.parent / manifest["wheel"]
digest = sha256(wheel.read_bytes()).hexdigest()
assert digest == manifest["wheel_sha256"]


def incident_trace(dtype: type[np.floating]) -> dict[str, object]:
    seed = int(
        sha256(b"coda-one-spike-four-suspects").hexdigest()[:8], 16
    )
    rng = np.random.default_rng(seed)
    sample_count, input_dimension, output_dimension = 256, 6, 4
    inputs = rng.normal(size=(sample_count, input_dimension)).astype(dtype)
    target_matrix = rng.normal(
        size=(input_dimension, output_dimension)
    ).astype(dtype)
    targets = (
        inputs @ target_matrix
        + dtype(0.05)
        * rng.normal(size=(sample_count, output_dimension)).astype(dtype)
    ).astype(dtype)
    weights = np.zeros((input_dimension, output_dimension), dtype=dtype)
    batch_size, step_size, steps, incident = 32, dtype(0.12), 120, 60
    permutation = np.random.default_rng(seed + 1).permutation(sample_count)
    hessian = (inputs.T @ inputs / dtype(sample_count)).astype(dtype)
    top_curvature = float(
        np.linalg.eigvalsh(hessian.astype(float))[-1]
    )

    losses, discrepancies, shift_shares = [], [], []
    directional_curvatures, update_spectra, weight_spectra = [], [], []
    batch_means, batch_variances, magnitudes = [], [], []
    for step in range(steps):
        residual = inputs @ weights - targets
        full_gradient = inputs.T @ residual / dtype(sample_count)
        losses.append(
            float(
                dtype(0.5)
                * np.sum(residual**2, dtype=dtype)
                / dtype(sample_count)
            )
        )
        start = (step * batch_size) % sample_count
        indices = permutation[start : start + batch_size]
        batch_inputs = inputs[indices]
        clean_targets = targets[indices]
        actual_targets = clean_targets.copy()
        if step == incident:
            sign = np.sign(
                np.arange(output_dimension, dtype=float)[None, :] - 1.5
            ).astype(dtype)
            actual_targets += dtype(8) * sign

        clean_gradient = (
            batch_inputs.T @ (batch_inputs @ weights - clean_targets)
            / dtype(batch_size)
        )
        actual_gradient = (
            batch_inputs.T @ (batch_inputs @ weights - actual_targets)
            / dtype(batch_size)
        )
        discrepancy = float(
            np.sum((actual_gradient - full_gradient) ** 2, dtype=dtype)
        )
        gradient_scale = max(
            float(np.sum(full_gradient**2, dtype=dtype)),
            np.finfo(dtype).tiny,
        )
        discrepancies.append(discrepancy / gradient_scale)
        shift_shares.append(
            float(
                np.sum(
                    (actual_gradient - clean_gradient) ** 2,
                    dtype=dtype,
                )
            )
            / max(discrepancy, np.finfo(dtype).tiny)
        )

        update = (-step_size * actual_gradient).astype(dtype)
        update_spectra.append(
            np.linalg.svd(update.astype(float), compute_uv=False)
        )
        weight_spectra.append(
            np.linalg.svd(weights.astype(float), compute_uv=False)
        )
        directional_curvatures.append(
            float(
                np.sum(update * (hessian @ update), dtype=dtype)
                / np.sum(update**2, dtype=dtype)
            )
        )
        magnitudes.append(
            max(
                float(np.max(np.abs(weights))),
                float(np.max(np.abs(update))),
            )
        )
        batch_means.append(batch_inputs.mean(axis=0, dtype=dtype).astype(float))
        batch_variances.append(
            batch_inputs.var(axis=0, dtype=dtype).astype(float)
        )
        weights = (weights + update).astype(dtype)

    residual = inputs @ weights - targets
    losses.append(
        float(
            dtype(0.5)
            * np.sum(residual**2, dtype=dtype)
            / dtype(sample_count)
        )
    )
    return {
        "seed": seed,
        "losses": np.asarray(losses),
        "discrepancies": np.asarray(discrepancies),
        "shift_shares": np.asarray(shift_shares),
        "directional_curvatures": np.asarray(directional_curvatures),
        "update_spectra": np.asarray(update_spectra),
        "weight_spectra": np.asarray(weight_spectra),
        "batch_means": np.asarray(batch_means),
        "batch_variances": np.asarray(batch_variances),
        "maximum_magnitude": max(magnitudes),
        "top_curvature": top_curvature,
    }


float64 = incident_trace(np.float64)
float32 = incident_trace(np.float32)
incident = 60
loss64 = float64["losses"]
loss32 = float32["losses"]
maximum_magnitude = float64["maximum_magnitude"]
record = {
    "schema_version": 1,
    "claim_id": "coda-incident-001",
    "phenomenon_id": "coda-one-spike-four-suspects",
    "chapter": "coda",
    "provenance_class": "a",
    "hypothesis": "A full diagnostic panel can distinguish an engineered estimator-target failure from precision, curvature, and normalization-state rivals.",
    "hardware_claim_boundary": "Seeded laptop-CPU linear-regression incident in float64 with a paired float32 control; no accelerator or large-model claim.",
    "harness_ref": "ch-17",
    "harness_wheel_sha256": digest,
    "result": {
        "seed": float64["seed"],
        "steps": 120,
        "incident_step": incident,
        "batch_size": 32,
        "step_size": 0.12,
        "loss_before_incident": float(loss64[incident]),
        "loss_after_incident": float(loss64[incident + 1]),
        "loss_spike_factor": float(
            loss64[incident + 1] / loss64[incident]
        ),
        "precision_control": {
            "maximum_relative_loss_deviation_float32_vs_float64": float(
                np.max(
                    np.abs(loss32 - loss64)
                    / np.maximum(loss64, 1e-30)
                )
            ),
            "maximum_state_or_update_magnitude": maximum_magnitude,
            "float32_spacing_at_that_scale": float(
                np.spacing(np.float32(maximum_magnitude))
            ),
        },
        "regime_control": {
            "realized_gradient_discrepancy_ratio": float(
                float64["discrepancies"][incident]
            ),
            "fraction_of_discrepancy_from_engineered_target_shift": float(
                float64["shift_shares"][incident]
            ),
        },
        "curvature_control": {
            "top_curvature": float64["top_curvature"],
            "step_times_top_curvature": 0.12 * float64["top_curvature"],
            "incident_directional_curvature": float(
                float64["directional_curvatures"][incident]
            ),
            "step_times_directional_curvature": 0.12
            * float(float64["directional_curvatures"][incident]),
        },
        "spectrum_control": {
            "leading_update_singular_value_ratio_to_previous_step": float(
                float64["update_spectra"][incident, 0]
                / float64["update_spectra"][incident - 1, 0]
            ),
            "incident_update_singular_values": float64[
                "update_spectra"
            ][incident].tolist(),
            "incident_weight_singular_values": float64[
                "weight_spectra"
            ][incident].tolist(),
        },
        "normalization_state_control": {
            "maximum_mean_difference_from_same_batch_previous_cycle": float(
                np.max(
                    np.abs(
                        float64["batch_means"][incident]
                        - float64["batch_means"][incident - 8]
                    )
                )
            ),
            "maximum_variance_difference_from_same_batch_previous_cycle": float(
                np.max(
                    np.abs(
                        float64["batch_variances"][incident]
                        - float64["batch_variances"][incident - 8]
                    )
                )
            ),
        },
        "final_loss": float(loss64[-1]),
    },
}
verify_claim("coda-incident-001.json", record, absolute_tolerance=1e-8)

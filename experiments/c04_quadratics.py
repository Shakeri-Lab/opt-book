"""Generate the class-(a) claim artifacts for C04."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np

from _evidence_verify import verify_claim


ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "artifacts" / "claims"
MANIFEST = ROOT / "artifacts" / "harness" / "ch-04" / "manifest.json"


def verify_generated_claim(filename: str, payload: dict[str, Any]) -> None:
    verify_claim(filename, payload, absolute_tolerance=1e-12)

manifest = json.loads(MANIFEST.read_text())
wheel = MANIFEST.parent / manifest["wheel"]
wheel_digest = sha256(wheel.read_bytes()).hexdigest()
assert wheel_digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))

from trainable_harness import (  # noqa: E402
    classify_mode_factors,
    observation_ledger,
    quadratic_spectrum,
    quadratic_trace,
    scalar_noisy_quadratic_trials,
)


def base_record(
    *,
    claim_id: str,
    hypothesis: str,
    result: dict[str, Any],
    seed: int | None,
) -> dict[str, Any]:
    environment = observation_ledger(
        seed=seed if seed is not None else 0,
        dtype=np.float64,
    )
    environment["seed_role"] = "not applicable" if seed is None else "Monte Carlo"
    return {
        "schema_version": 1,
        "claim_id": claim_id,
        "phenomenon_id": "c04-many-clocks",
        "chapter": "c04",
        "provenance_class": "a",
        "hypothesis": hypothesis,
        "environment": environment,
        "harness_ref": manifest["harness_ref"],
        "harness_wheel_sha256": wheel_digest,
        "hardware_claim_boundary": (
            "Laptop-CPU model calculation; iteration counts are not wall-clock "
            "or accelerator-performance claims."
        ),
        "result": result,
    }


def main() -> None:
    hessian = np.diag([1.0, 100.0])
    initial_error = np.array([1.0, 1.0])
    step_size = 0.019
    steps = 400
    trace = quadratic_trace(
        hessian,
        initial_error,
        step_size=step_size,
        steps=steps,
    )
    factors, labels = classify_mode_factors(
        trace.eigenvalues,
        step_size=step_size,
    )
    tolerance = 1e-3
    iterations_to_tolerance = [
        int(np.ceil(np.log(tolerance) / np.log(abs(factor))))
        for factor in factors
    ]
    closed_form = factors[None, :] ** np.arange(steps + 1)[:, None]
    assert np.allclose(trace.mode_coordinates, closed_form)
    mode_claim = base_record(
        claim_id="c04-mode-dynamics-001",
        hypothesis=(
            "A single gradient step on an ill-conditioned quadratic makes the "
            "sharp mode alternate while the flat mode controls the wait."
        ),
        result={
            "hessian_diagonal": np.diag(hessian).tolist(),
            "initial_error": initial_error.tolist(),
            "step_size": step_size,
            "steps": steps,
            "mode_factors": factors.tolist(),
            "mode_labels": list(labels),
            "absolute_tolerance": tolerance,
            "iterations_to_tolerance_by_mode": iterations_to_tolerance,
            "final_mode_coordinates": trace.mode_coordinates[-1].tolist(),
            "spectrum": quadratic_spectrum(hessian),
        },
        seed=None,
    )
    verify_generated_claim("c04-mode-dynamics-001.json", mode_claim)

    compressed_preconditioner = np.diag([1.0, 1 / 25])
    raw = quadratic_trace(
        hessian,
        initial_error,
        step_size=step_size,
        steps=30,
    )
    compressed = quadratic_trace(
        hessian,
        initial_error,
        step_size=0.4,
        steps=30,
        preconditioner=compressed_preconditioner,
    )
    transformed_eigenvalues = np.linalg.eigvalsh(
        compressed_preconditioner @ hessian
    )
    assert np.allclose(transformed_eigenvalues, [1.0, 4.0])
    preconditioner_claim = base_record(
        claim_id="c04-preconditioner-001",
        hypothesis=(
            "A positive diagonal change of scale that compresses the effective "
            "spectrum from condition number 100 to 4 shortens the slow-mode wait."
        ),
        result={
            "raw": {
                "step_size": step_size,
                "steps": 30,
                "final_error_norm": raw.final_error_norm,
            },
            "preconditioned": {
                "preconditioner_diagonal": np.diag(
                    compressed_preconditioner
                ).tolist(),
                "effective_eigenvalues": transformed_eigenvalues.tolist(),
                "effective_condition_number": float(
                    transformed_eigenvalues[-1] / transformed_eigenvalues[0]
                ),
                "step_size": 0.4,
                "steps": 30,
                "final_error_norm": compressed.final_error_norm,
            },
        },
        seed=None,
    )
    verify_generated_claim("c04-preconditioner-001.json", preconditioner_claim)

    noisy = scalar_noisy_quadratic_trials(
        curvature=1.0,
        step_size=0.1,
        noise_standard_deviation=1.0,
        initial_error=3.0,
        steps=120,
        trials=20_000,
        seed=6213,
    )
    factor = 1.0 - noisy.step_size * noisy.curvature
    finite_step_prediction = (
        factor ** (2 * 120) * noisy.initial_error**2
        + noisy.stationary_second_moment * (1.0 - factor ** (2 * 120))
    )
    assert (
        abs(noisy.endpoint_mean_squared_error - finite_step_prediction)
        < 4 * noisy.endpoint_standard_error
    )
    noise_claim = base_record(
        claim_id="c04-noise-floor-001",
        hypothesis=(
            "A stable scalar quadratic driven by independent mean-zero gradient "
            "noise approaches the exact second-moment floor of its AR(1) recurrence."
        ),
        result={
            "curvature": noisy.curvature,
            "step_size": noisy.step_size,
            "noise_standard_deviation": noisy.noise_standard_deviation,
            "initial_error": noisy.initial_error,
            "steps": 120,
            "trials": noisy.trials,
            "seed": noisy.seed,
            "estimator": "mean endpoint squared error",
            "reduction_axis": "independent trials",
            "denominator": noisy.trials,
            "stationary_second_moment": noisy.stationary_second_moment,
            "finite_step_second_moment": finite_step_prediction,
            "endpoint_mean_squared_error": noisy.endpoint_mean_squared_error,
            "endpoint_standard_error": noisy.endpoint_standard_error,
            "normal_95_percent_interval": [
                noisy.endpoint_mean_squared_error
                - 1.96 * noisy.endpoint_standard_error,
                noisy.endpoint_mean_squared_error
                + 1.96 * noisy.endpoint_standard_error,
            ],
        },
        seed=noisy.seed,
    )
    verify_generated_claim("c04-noise-floor-001.json", noise_claim)

    for claim_id in (
        "c04-mode-dynamics-001",
        "c04-preconditioner-001",
        "c04-noise-floor-001",
    ):
        print(f"verified {claim_id}.json")


if __name__ == "__main__":
    main()

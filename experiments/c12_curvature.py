"""Re-execute the deterministic curvature witnesses registered for C12."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import platform
import sys
from typing import Any

import numpy as np

from _evidence_verify import verify_claim


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts" / "harness" / "ch-12" / "manifest.json"

manifest = json.loads(MANIFEST.read_text())
wheel = MANIFEST.parent / manifest["wheel"]
wheel_digest = sha256(wheel.read_bytes()).hexdigest()
assert wheel_digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))

from trainable_harness import (  # noqa: E402
    bernoulli_curvature_matrices,
    bernoulli_hessian_vector_product,
    dominant_symmetric_eigenpair,
    observation_ledger,
)


def matrix_record(matrix: np.ndarray) -> list[list[float]]:
    return [[float(value) for value in row] for row in matrix]


def curvature_record(matrices) -> dict[str, Any]:
    return {
        "hessian": matrix_record(matrices.hessian),
        "generalized_gauss_newton": matrix_record(
            matrices.generalized_gauss_newton
        ),
        "model_fisher": matrix_record(matrices.model_fisher),
        "empirical_fisher": matrix_record(matrices.empirical_fisher),
        "model_curvature": matrix_record(matrices.model_curvature),
        "hessian_eigenvalues": np.linalg.eigvalsh(matrices.hessian).tolist(),
        "ggn_eigenvalues": np.linalg.eigvalsh(
            matrices.generalized_gauss_newton
        ).tolist(),
        "empirical_fisher_eigenvalues": np.linalg.eigvalsh(
            matrices.empirical_fisher
        ).tolist(),
    }


def build_records() -> tuple[dict[str, Any], dict[str, Any]]:
    inputs = np.array([-2.0, -1.0, 1.0, 2.0])
    labels = np.array([0.0, 0.0, 1.0, 1.0])
    parameters = np.array([0.5, 0.0])
    affine = bernoulli_curvature_matrices(
        parameters,
        inputs,
        labels,
        nonlinear_first_parameter=False,
    )
    composed = bernoulli_curvature_matrices(
        parameters,
        inputs,
        labels,
        nonlinear_first_parameter=True,
    )
    scalar = bernoulli_curvature_matrices(
        parameters,
        np.array([1.0]),
        np.array([1.0]),
        nonlinear_first_parameter=True,
    )
    environment = observation_ledger(seed=6212, dtype=np.float64)
    environment["machine"] = platform.machine()
    curvature = {
        "schema_version": 1,
        "claim_id": "c12-curvature-choice-001",
        "phenomenon_id": "c12-curvature-choice",
        "chapter": "c12",
        "provenance_class": "a",
        "hypothesis": (
            "An affine Bernoulli logit makes the realized Hessian equal GGN, "
            "while composing the same loss with a curved parameter map can "
            "make the Hessian indefinite; observed-label score outer products "
            "need not equal the model Fisher in either case."
        ),
        "environment": environment,
        "harness_ref": manifest["harness_ref"],
        "harness_wheel_sha256": wheel_digest,
        "hardware_claim_boundary": (
            "Deterministic laptop-CPU float64 calculation; no timing or "
            "accelerator-performance conclusion."
        ),
        "result": {
            "inputs": inputs.tolist(),
            "labels": labels.tolist(),
            "parameters": parameters.tolist(),
            "opening_single_observation": {
                "input": 1.0,
                "label": 1.0,
                "probability": float(1.0 / (1.0 + np.exp(-0.25))),
                "hessian_parameter_coordinate": float(scalar.hessian[0, 0]),
                "generalized_gauss_newton_parameter_coordinate": float(
                    scalar.generalized_gauss_newton[0, 0]
                ),
                "model_fisher_parameter_coordinate": float(
                    scalar.model_fisher[0, 0]
                ),
                "empirical_fisher_parameter_coordinate": float(
                    scalar.empirical_fisher[0, 0]
                ),
                "model_curvature_parameter_coordinate": float(
                    scalar.model_curvature[0, 0]
                ),
            },
            "affine_logit": curvature_record(affine),
            "composed_logit": curvature_record(composed),
        },
    }

    vector = np.array([0.3, -0.7])
    dense_product = composed.hessian @ vector
    operator = lambda candidate: bernoulli_hessian_vector_product(
        parameters,
        inputs,
        labels,
        candidate,
        nonlinear_first_parameter=True,
    )
    operator_product = operator(vector)
    estimate = dominant_symmetric_eigenpair(
        operator,
        2,
        iterations=24,
        seed=6212,
    )
    hvp = {
        "schema_version": 1,
        "claim_id": "c12-hvp-001",
        "phenomenon_id": "c12-curvature-choice",
        "chapter": "c12",
        "provenance_class": "a",
        "hypothesis": (
            "The analytic Hessian-vector program matches dense multiplication "
            "and recovers the signed dominant-magnitude eigenvalue without "
            "materializing the matrix in the iteration."
        ),
        "environment": environment,
        "harness_ref": manifest["harness_ref"],
        "harness_wheel_sha256": wheel_digest,
        "hardware_claim_boundary": (
            "Two-dimensional operator witness; algebraic access pattern is "
            "not a measured wall-clock or memory-throughput result."
        ),
        "result": {
            "vector": vector.tolist(),
            "dense_product": dense_product.tolist(),
            "operator_product": operator_product.tolist(),
            "maximum_product_deviation": float(
                np.max(np.abs(dense_product - operator_product))
            ),
            "dense_eigenvalues": np.linalg.eigvalsh(composed.hessian).tolist(),
            "iterations": 24,
            "seed": 6212,
            "dominant_magnitude_eigenvalue_estimate": estimate.eigenvalue,
            "residual_norm": estimate.residual_norm,
            "rayleigh_trace": list(estimate.rayleigh_trace),
        },
    }
    return curvature, hvp


def main() -> None:
    curvature, hvp = build_records()
    verify_claim(
        "c12-curvature-choice-001.json",
        curvature,
        absolute_tolerance=1e-12,
    )
    verify_claim("c12-hvp-001.json", hvp, absolute_tolerance=1e-12)


if __name__ == "__main__":
    main()

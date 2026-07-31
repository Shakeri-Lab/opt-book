"""Generate the class-(a) claim artifacts for C07."""

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
MANIFEST = ROOT / "artifacts" / "harness" / "ch-07" / "manifest.json"


def verify_generated_claim(filename: str, payload: dict[str, Any]) -> None:
    verify_claim(filename, payload, absolute_tolerance=1e-12)

manifest = json.loads(MANIFEST.read_text())
wheel = MANIFEST.parent / manifest["wheel"]
wheel_digest = sha256(wheel.read_bytes()).hexdigest()
assert wheel_digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))

from trainable_harness import (  # noqa: E402
    circle_covering_radius,
    circle_epsilon_net,
    observation_ledger,
    operator_net_certificate,
    operator_net_estimate,
    sphere_cover_log_upper,
    uniform_subgaussian_threshold,
)


def base_record(
    *,
    claim_id: str,
    hypothesis: str,
    result: dict[str, Any],
) -> dict[str, Any]:
    environment = observation_ledger(seed=0, dtype=np.float64)
    environment["seed_role"] = "not applicable; deterministic calculation"
    return {
        "schema_version": 1,
        "claim_id": claim_id,
        "phenomenon_id": "c07-finite-price",
        "chapter": "c07",
        "provenance_class": "a",
        "hypothesis": hypothesis,
        "environment": environment,
        "harness_ref": manifest["harness_ref"],
        "harness_wheel_sha256": wheel_digest,
        "hardware_claim_boundary": (
            "Laptop-CPU geometry calculation; no accelerator throughput "
            "or low-precision format claim."
        ),
        "result": result,
    }


def main() -> None:
    angle = 0.37
    rotation = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    matrix = rotation @ np.diag([6.0, 1.0]) @ rotation.T
    exact_norm = float(np.linalg.norm(matrix, ord=2))
    coordinate_probes = np.eye(2)
    coordinate_maximum = operator_net_estimate(matrix, coordinate_probes)
    resolutions = (0.5, 0.25, 0.125, 0.0625)
    records = {}
    for epsilon in resolutions:
        net = circle_epsilon_net(epsilon)
        radius = circle_covering_radius(net)
        estimate = operator_net_estimate(matrix, net)
        declared_certificate = operator_net_certificate(estimate, epsilon)
        exact_radius_certificate = operator_net_certificate(estimate, radius)
        assert estimate <= exact_norm + 1e-12
        assert declared_certificate >= exact_norm
        assert exact_radius_certificate >= exact_norm
        records[str(epsilon)] = {
            "net_points": int(net.shape[0]),
            "actual_covering_radius": radius,
            "sampled_maximum": estimate,
            "declared_radius_certificate": declared_certificate,
            "exact_radius_certificate": exact_radius_certificate,
            "relative_sample_gap": (exact_norm - estimate) / exact_norm,
        }

    hidden_direction = base_record(
        claim_id="c07-hidden-direction-001",
        hypothesis=(
            "A finite probe set can miss a data-dependent extremal direction, "
            "while a verified epsilon-net turns its sampled maximum into a "
            "deterministic operator-norm certificate."
        ),
        result={
            "matrix": matrix.tolist(),
            "right_singular_rotation_radians": angle,
            "singular_values": [6.0, 1.0],
            "exact_operator_norm": exact_norm,
            "coordinate_probe_maximum": coordinate_maximum,
            "coordinate_probe_gap": exact_norm - coordinate_maximum,
            "epsilon_net_records": records,
            "certificate_formula": "sampled_maximum / (1 - epsilon)",
        },
    )
    verify_generated_claim("c07-hidden-direction-001.json", hidden_direction)

    dimensions = (8, 32, 128, 512)
    epsilon = 0.25
    delta = 0.01
    budget_records = {}
    for dimension in dimensions:
        log_cover = sphere_cover_log_upper(dimension, epsilon)
        subgaussian_threshold = uniform_subgaussian_threshold(log_cover, delta)
        chebyshev_log10_threshold = (
            0.5 * (log_cover + np.log(1.0 / delta)) / np.log(10.0)
        )
        budget_records[str(dimension)] = {
            "log_cover_upper": log_cover,
            "log10_cover_upper": log_cover / np.log(10.0),
            "subgaussian_anchor_threshold": subgaussian_threshold,
            "chebyshev_anchor_threshold_log10": float(
                chebyshev_log10_threshold
            ),
        }

    tail_budget = base_record(
        claim_id="c07-tail-budget-001",
        hypothesis=(
            "An exponential-size Euclidean cover remains affordable under a "
            "sub-Gaussian fixed-anchor tail because the threshold pays only "
            "the logarithm of the cover, whereas a second-moment tail requires "
            "an exponentially large threshold."
        ),
        result={
            "dimensions": list(dimensions),
            "epsilon": epsilon,
            "failure_probability": delta,
            "cover_upper_formula": "(1 + 2/epsilon)^dimension",
            "subgaussian_tail_model": "2 exp(-t^2/2)",
            "chebyshev_tail_model": "1/t^2",
            "records": budget_records,
            "interpolation_term_per_unit_lipschitz": epsilon,
            "boundary": (
                "The comparison prices two declared tail envelopes; it does "
                "not prove that either envelope holds for a new random object."
            ),
        },
    )
    verify_generated_claim("c07-tail-budget-001.json", tail_budget)

    for claim_id in ("c07-hidden-direction-001", "c07-tail-budget-001"):
        print(f"verified {claim_id}.json")


if __name__ == "__main__":
    main()

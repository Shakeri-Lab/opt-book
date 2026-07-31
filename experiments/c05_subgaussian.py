"""Generate the class-(a) claim artifacts for C05."""

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
MANIFEST = ROOT / "artifacts" / "harness" / "ch-05" / "manifest.json"


def verify_generated_claim(filename: str, payload: dict[str, Any]) -> None:
    verify_claim(filename, payload, absolute_tolerance=1e-12)

manifest = json.loads(MANIFEST.read_text())
wheel = MANIFEST.parent / manifest["wheel"]
wheel_digest = sha256(wheel.read_bytes()).hexdigest()
assert wheel_digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))

from trainable_harness import (  # noqa: E402
    empirical_tail_profile,
    moment_growth_profile,
    observation_ledger,
    rademacher_projection_trials,
    standard_normal_maxima,
    subgaussian_max_threshold,
)


def base_record(
    *,
    claim_id: str,
    hypothesis: str,
    result: dict[str, Any],
    seed: int,
) -> dict[str, Any]:
    environment = observation_ledger(seed=seed, dtype=np.float64)
    environment["seed_role"] = "independent named streams"
    return {
        "schema_version": 1,
        "claim_id": claim_id,
        "phenomenon_id": "c05-simultaneous-safe-zone",
        "chapter": "c05",
        "provenance_class": "a",
        "hypothesis": hypothesis,
        "environment": environment,
        "harness_ref": manifest["harness_ref"],
        "harness_wheel_sha256": wheel_digest,
        "hardware_claim_boundary": (
            "Laptop-CPU probability witness; no accelerator throughput claim."
        ),
        "result": result,
    }


def main() -> None:
    counts = (100, 1_000, 10_000, 100_000, 1_000_000)
    seed = 6214
    delta = 0.01
    maxima = standard_normal_maxima(counts, seed=seed)
    thresholds = {
        count: subgaussian_max_threshold(count, delta)
        for count in counts
    }
    assert all(maxima[count] < thresholds[count] for count in counts)
    simultaneous = base_record(
        claim_id="c05-simultaneous-control-001",
        hypothesis=(
            "The largest magnitude among many standard-normal coordinates grows "
            "on the square-root-log scale captured by simultaneous sub-Gaussian control."
        ),
        result={
            "distribution": "independent standard normal coordinates",
            "counts": list(counts),
            "seed": seed,
            "stream_policy": "one SeedSequence child per count",
            "single_seeded_witness_maxima": {
                str(count): maxima[count] for count in counts
            },
            "failure_probability": delta,
            "union_bound_thresholds": {
                str(count): thresholds[count] for count in counts
            },
            "billion_coordinate_model_threshold": subgaussian_max_threshold(
                1_000_000_000,
                delta,
            ),
            "boundary": (
                "The billion-coordinate value is a model calculation from the "
                "bound, not a generated billion-coordinate sample."
            ),
        },
        seed=seed,
    )
    verify_generated_claim("c05-simultaneous-control-001.json", simultaneous)

    widths = (16, 64, 256, 1024)
    trials = 20_000
    base_seed = 6215
    records = {}
    for index, width in enumerate(widths):
        stream_seed = base_seed + index
        coefficients = np.ones(width, dtype=np.float64) / np.sqrt(width)
        samples = rademacher_projection_trials(
            coefficients,
            trials=trials,
            seed=stream_seed,
        )
        mean = float(samples.mean())
        standard_deviation = float(samples.std(ddof=1))
        tail_probability = empirical_tail_profile(samples, [2.0])[2.0]
        records[str(width)] = {
            "seed": stream_seed,
            "coefficient_l2_norm": float(np.linalg.norm(coefficients)),
            "sample_mean": mean,
            "standard_error_of_mean": standard_deviation / np.sqrt(trials),
            "sample_standard_deviation": standard_deviation,
            "approximate_standard_error_of_standard_deviation": (
                standard_deviation / np.sqrt(2 * (trials - 1))
            ),
            "empirical_two_sided_tail_at_2": tail_probability,
            "binomial_standard_error_of_tail": float(
                np.sqrt(
                    tail_probability
                    * (1.0 - tail_probability)
                    / trials
                )
            ),
            "moment_growth_l2_over_sqrt2": moment_growth_profile(
                samples,
                [2],
            )[2],
        }
        assert abs(mean) < 4 * records[str(width)]["standard_error_of_mean"]
        assert abs(standard_deviation - 1.0) < 0.04

    projections = base_record(
        claim_id="c05-projection-scale-001",
        hypothesis=(
            "Rademacher projections with coefficient norm one retain order-one "
            "scale as width grows."
        ),
        result={
            "distribution": "independent Rademacher signs",
            "widths": list(widths),
            "trials_per_width": trials,
            "estimator_contract": {
                "mean": "arithmetic mean over independent trials",
                "variance_denominator": trials - 1,
                "tail_denominator": trials,
                "tail_event": "absolute projection at least 2",
            },
            "records": records,
            "subgaussian_tail_upper_bound_at_2": float(
                2.0 * np.exp(-2.0)
            ),
        },
        seed=base_seed,
    )
    verify_generated_claim("c05-projection-scale-001.json", projections)

    for claim_id in (
        "c05-simultaneous-control-001",
        "c05-projection-scale-001",
    ):
        print(f"verified {claim_id}.json")


if __name__ == "__main__":
    main()

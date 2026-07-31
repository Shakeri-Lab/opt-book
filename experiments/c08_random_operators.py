"""Generate the class-(a) claim artifacts for C08."""

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
MANIFEST = ROOT / "artifacts" / "harness" / "ch-08" / "manifest.json"


def verify_generated_claim(filename: str, payload: dict[str, Any]) -> None:
    verify_claim(filename, payload, absolute_tolerance=1e-12)

manifest = json.loads(MANIFEST.read_text())
wheel = MANIFEST.parent / manifest["wheel"]
wheel_digest = sha256(wheel.read_bytes()).hexdigest()
assert wheel_digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))

from trainable_harness import (  # noqa: E402
    gaussian_singular_value_trials,
    matrix_spectrum_summary,
    observation_ledger,
    power_iteration_spectral_norm,
)


def base_record(
    *,
    claim_id: str,
    hypothesis: str,
    result: dict[str, Any],
    seed: int,
) -> dict[str, Any]:
    environment = observation_ledger(seed=seed, dtype=np.float64)
    environment["seed_role"] = "matrix generation or iteration initialization"
    return {
        "schema_version": 1,
        "claim_id": claim_id,
        "phenomenon_id": "c08-one-average-two-edges",
        "chapter": "c08",
        "provenance_class": "a",
        "hypothesis": hypothesis,
        "environment": environment,
        "harness_ref": manifest["harness_ref"],
        "harness_wheel_sha256": wheel_digest,
        "hardware_claim_boundary": (
            "Laptop-CPU float64 linear-algebra study; no CPU timing is "
            "presented as accelerator performance and no singular value is "
            "identified with low-precision underflow."
        ),
        "result": result,
    }


def quantiles(values: np.ndarray) -> dict[str, float]:
    return {
        "q05": float(np.quantile(values, 0.05)),
        "median": float(np.median(values)),
        "q95": float(np.quantile(values, 0.95)),
    }


def main() -> None:
    dimension = 64
    matrix_seed = 6224
    matrix_rng = np.random.default_rng(matrix_seed)
    matrix = matrix_rng.standard_normal((dimension, dimension)) / np.sqrt(dimension)
    summary = matrix_spectrum_summary(matrix)
    _, singular_values, right_vectors_t = np.linalg.svd(matrix, full_matrices=False)
    fixed_direction = np.zeros(dimension)
    fixed_direction[0] = 1.0
    fixed_stretch = float(np.linalg.norm(matrix @ fixed_direction))
    top_stretch = float(np.linalg.norm(matrix @ right_vectors_t[0]))
    bottom_stretch = float(np.linalg.norm(matrix @ right_vectors_t[-1]))
    assert np.isclose(top_stretch, summary.sigma_max)
    assert np.isclose(bottom_stretch, summary.sigma_min)
    assert np.allclose(singular_values, np.asarray(summary.singular_values))

    average_edges = base_record(
        claim_id="c08-average-edges-001",
        hypothesis=(
            "A scaled Gaussian matrix can preserve a fixed direction and the "
            "average squared stretch near one while its data-dependent "
            "singular directions realize widely separated edges."
        ),
        result={
            "shape": [dimension, dimension],
            "entry_distribution": "N(0, 1/rows)",
            "matrix_seed": matrix_seed,
            "fixed_direction": "first coordinate vector, declared before matrix",
            "fixed_direction_stretch": fixed_stretch,
            "mean_squared_stretch": summary.mean_squared_stretch,
            "sigma_max": summary.sigma_max,
            "sigma_min": summary.sigma_min,
            "condition_number": summary.condition_number,
            "top_singular_direction_stretch": top_stretch,
            "bottom_singular_direction_stretch": bottom_stretch,
            "square_gaussian_lower_benchmark": 0.0,
        },
        seed=matrix_seed,
    )
    verify_generated_claim("c08-average-edges-001.json", average_edges)

    columns = 64
    trials = 160
    rows_grid = (64, 128, 256)
    ensemble_records = {}
    for index, rows in enumerate(rows_grid):
        seed = 6225 + index
        samples = gaussian_singular_value_trials(
            rows,
            columns,
            trials=trials,
            seed=seed,
        )
        ratio = columns / rows
        ensemble_records[str(rows)] = {
            "rows": rows,
            "columns": columns,
            "trials": trials,
            "seed": seed,
            "aspect_ratio_columns_over_rows": ratio,
            "gaussian_lower_benchmark": 1.0 - np.sqrt(ratio),
            "gaussian_upper_benchmark": 1.0 + np.sqrt(ratio),
            "sigma_min": quantiles(samples["sigma_min"]),
            "sigma_max": quantiles(samples["sigma_max"]),
            "fixed_direction_stretch": quantiles(
                samples["fixed_direction_stretch"]
            ),
            "mean_squared_stretch": quantiles(
                samples["mean_squared_stretch"]
            ),
        }

    aspect_ratio = base_record(
        claim_id="c08-aspect-ratio-001",
        hypothesis=(
            "For finite scaled Gaussian matrices with a fixed input width, "
            "increasing the row-to-column aspect ratio opens a positive lower "
            "edge while the fixed-direction and Frobenius averages remain "
            "centered near one."
        ),
        result={
            "entry_distribution": "N(0, 1/rows)",
            "rows_grid": list(rows_grid),
            "columns": columns,
            "trials_per_shape": trials,
            "estimator": "5th, 50th, and 95th empirical quantiles",
            "reduction_axis": "independent matrix trials",
            "records": ensemble_records,
            "boundary": (
                "Benchmark curves are Gaussian edge locations, not a "
                "Marchenko--Pastur empirical-density theorem or calibrated "
                "finite-size confidence interval."
            ),
        },
        seed=6225,
    )
    verify_generated_claim("c08-aspect-ratio-001.json", aspect_ratio)

    iterations = 25
    iteration_seed = 6228
    trace = power_iteration_spectral_norm(
        matrix,
        iterations=iterations,
        seed=iteration_seed,
    )
    estimates = np.asarray(trace.estimates)
    relative_error = np.abs(estimates - summary.sigma_max) / summary.sigma_max
    assert relative_error[-1] < relative_error[0]
    power_iteration = base_record(
        claim_id="c08-power-iteration-001",
        hypothesis=(
            "Power iteration converges toward the largest singular value on "
            "this seeded control but contains no estimate of the lower edge."
        ),
        result={
            "matrix_claim": "c08-average-edges-001",
            "matrix_seed": matrix_seed,
            "iteration_seed": iteration_seed,
            "iterations": iterations,
            "exact_sigma_max": summary.sigma_max,
            "exact_sigma_min": summary.sigma_min,
            "estimates": list(trace.estimates),
            "relative_errors": relative_error.tolist(),
            "reported_edge": "largest only",
            "unreported_edge": "smallest",
        },
        seed=iteration_seed,
    )
    verify_generated_claim("c08-power-iteration-001.json", power_iteration)

    for claim_id in (
        "c08-average-edges-001",
        "c08-aspect-ratio-001",
        "c08-power-iteration-001",
    ):
        print(f"verified {claim_id}.json")


if __name__ == "__main__":
    main()

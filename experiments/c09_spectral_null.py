"""Generate the class-(a) claim artifacts for C09."""

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
MANIFEST = ROOT / "artifacts" / "harness" / "ch-09" / "manifest.json"


def verify_generated_claim(filename: str, payload: dict[str, Any]) -> None:
    verify_claim(filename, payload, absolute_tolerance=1e-12)

manifest = json.loads(MANIFEST.read_text())
wheel = MANIFEST.parent / manifest["wheel"]
wheel_digest = sha256(wheel.read_bytes()).hexdigest()
assert wheel_digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))

from trainable_harness import (  # noqa: E402
    covariance_eigenvalues,
    empirical_upper_threshold,
    gaussian_covariance_trials,
    marchenko_pastur_support,
    observation_ledger,
)


def base_record(
    *,
    claim_id: str,
    hypothesis: str,
    result: dict[str, Any],
    seed: int,
) -> dict[str, Any]:
    environment = observation_ledger(seed=seed, dtype=np.float64)
    environment["seed_role"] = "data generation or finite-null calibration"
    return {
        "schema_version": 1,
        "claim_id": claim_id,
        "phenomenon_id": "c09-bulk-not-verdict",
        "chapter": "c09",
        "provenance_class": "a",
        "hypothesis": hypothesis,
        "environment": environment,
        "harness_ref": manifest["harness_ref"],
        "harness_wheel_sha256": wheel_digest,
        "hardware_claim_boundary": (
            "Laptop-CPU float64 eigendecomposition study; no CPU timing is "
            "presented as accelerator performance, and no trained matrix or "
            "Hessian is assigned a Wishart null."
        ),
        "result": result,
    }


def quantiles(values: np.ndarray) -> dict[str, float]:
    return {
        "q05": float(np.quantile(values, 0.05, method="linear")),
        "median": float(np.quantile(values, 0.50, method="linear")),
        "q95": float(np.quantile(values, 0.95, method="linear")),
    }


def main() -> None:
    sample_count = 128
    feature_count = 64
    aspect_ratio = feature_count / sample_count
    support = marchenko_pastur_support(aspect_ratio)

    witness_seed_rule = "first 32 bits of SHA-256('c09-bulk-not-verdict')"
    witness_seed = int(
        sha256(b"c09-bulk-not-verdict").hexdigest()[:8],
        16,
    )
    witness_rng = np.random.default_rng(witness_seed)
    witness_data = witness_rng.standard_normal((sample_count, feature_count))
    witness_eigenvalues = covariance_eigenvalues(witness_data)
    assert witness_eigenvalues[-1] > support.lambda_plus

    bulk_shape = base_record(
        claim_id="c09-bulk-shape-001",
        hypothesis=(
            "A finite pure-noise covariance spectrum can follow the "
            "Marchenko--Pastur bulk shape while its largest eigenvalue crosses "
            "the asymptotic upper support edge."
        ),
        result={
            "sample_orientation": "rows are observations; columns are coordinates",
            "sample_count": sample_count,
            "feature_count": feature_count,
            "aspect_ratio_features_over_samples": aspect_ratio,
            "estimator": "X.T @ X / sample_count",
            "population_mean": "known zero",
            "centering": False,
            "denominator": sample_count,
            "entry_distribution": "independent N(0,1)",
            "witness_seed": witness_seed,
            "witness_seed_rule": witness_seed_rule,
            "eigenvalues_ascending": witness_eigenvalues.tolist(),
            "mean_eigenvalue": float(np.mean(witness_eigenvalues)),
            "lambda_min": float(witness_eigenvalues[0]),
            "lambda_max": float(witness_eigenvalues[-1]),
            "mp_lambda_minus": support.lambda_minus,
            "mp_lambda_plus": support.lambda_plus,
            "mp_zero_atom": support.zero_atom,
            "crosses_asymptotic_upper_edge": bool(
                witness_eigenvalues[-1] > support.lambda_plus
            ),
            "boundary": (
                "The overlay is a finite witness against an asymptotic law, "
                "not a goodness-of-fit test for the full null model."
            ),
        },
        seed=witness_seed,
    )
    verify_generated_claim("c09-bulk-shape-001.json", bulk_shape)

    null_trials = 2000
    null_seed = 6291
    false_positive_rate = 0.05
    null = gaussian_covariance_trials(
        sample_count,
        feature_count,
        trials=null_trials,
        seed=null_seed,
    )
    null_max = null["lambda_max"]
    finite_threshold = empirical_upper_threshold(
        null_max,
        false_positive_rate=false_positive_rate,
    )
    asymptotic_crossing_rate = float(np.mean(null_max > support.lambda_plus))
    repeated_looks = 20
    independent_look_probability = float(
        1.0 - (1.0 - asymptotic_crossing_rate) ** repeated_looks
    )
    finite_threshold_independent_look_probability = float(
        1.0 - (1.0 - false_positive_rate) ** repeated_looks
    )

    finite_null = base_record(
        claim_id="c09-finite-null-001",
        hypothesis=(
            "Crossing the asymptotic Marchenko--Pastur upper edge is routine "
            "at this finite shape, while an independently calibrated finite "
            "upper-tail threshold does not reject the opening pure-noise witness."
        ),
        result={
            "sample_count": sample_count,
            "feature_count": feature_count,
            "trials": null_trials,
            "null_seed": null_seed,
            "null_model": "independent N(0,1) entries with known zero mean",
            "statistic": "largest eigenvalue of X.T @ X / sample_count",
            "asymptotic_upper_edge": support.lambda_plus,
            "asymptotic_edge_crossings": int(
                np.count_nonzero(null_max > support.lambda_plus)
            ),
            "asymptotic_edge_crossing_rate": asymptotic_crossing_rate,
            "null_quantiles": quantiles(null_max),
            "false_positive_rate": false_positive_rate,
            "finite_upper_threshold": finite_threshold,
            "quantile_method": "NumPy linear empirical quantile",
            "witness_claim": "c09-bulk-shape-001",
            "witness_seed": witness_seed,
            "witness_seed_rule": witness_seed_rule,
            "witness_lambda_max": float(witness_eigenvalues[-1]),
            "witness_crosses_asymptotic_edge": True,
            "witness_crosses_finite_threshold": bool(
                witness_eigenvalues[-1] > finite_threshold
            ),
            "independent_looks": repeated_looks,
            "probability_at_least_one_asymptotic_edge_crossing_under_independence": (
                independent_look_probability
            ),
            "probability_at_least_one_finite_threshold_crossing_under_independence": (
                finite_threshold_independent_look_probability
            ),
            "boundary": (
                "The empirical threshold is calibrated only for the declared "
                "Gaussian shape and estimator; changing centering, denominator, "
                "dependence, tails, or the number of inspected statistics "
                "changes the null contract."
            ),
        },
        seed=null_seed,
    )
    verify_generated_claim("c09-finite-null-001.json", finite_null)

    spike_models = (
        ("null", 1.0, null_seed),
        ("subcritical", 1.5, 6292),
        ("supercritical", 2.5, 6293),
    )
    spike_records: dict[str, Any] = {}
    separation_threshold = 1.0 + np.sqrt(aspect_ratio)
    for label, population_spike, seed in spike_models:
        trials = (
            null
            if population_spike == 1.0
            else gaussian_covariance_trials(
                sample_count,
                feature_count,
                trials=null_trials,
                seed=seed,
                population_spike=population_spike,
            )
        )
        maxima = trials["lambda_max"]
        asymptotic_location = (
            support.lambda_plus
            if population_spike <= separation_threshold
            else population_spike
            * (1.0 + aspect_ratio / (population_spike - 1.0))
        )
        spike_records[label] = {
            "population_spike": population_spike,
            "seed": seed,
            "trials": null_trials,
            "asymptotic_separation_threshold": separation_threshold,
            "asymptotic_sample_location": asymptotic_location,
            "lambda_max_quantiles": quantiles(maxima),
            "fraction_above_finite_null_threshold": float(
                np.mean(maxima > finite_threshold)
            ),
        }

    spike_threshold = base_record(
        claim_id="c09-spike-threshold-001",
        hypothesis=(
            "At aspect ratio one half, a genuine rank-one population spike "
            "below 1+sqrt(gamma) remains largely absorbed by the finite null, "
            "whereas a supercritical spike separates in most trials."
        ),
        result={
            "sample_count": sample_count,
            "feature_count": feature_count,
            "aspect_ratio_features_over_samples": aspect_ratio,
            "trials_per_model": null_trials,
            "model": (
                "Gaussian rows with population covariance "
                "diag(beta,1,...,1)"
            ),
            "finite_null_threshold": finite_threshold,
            "false_positive_rate": false_positive_rate,
            "records": spike_records,
            "boundary": (
                "These are finite ensembles for a declared rank-one spiked "
                "Gaussian model; the Baik--Silverstein locations are "
                "asymptotic benchmarks, not finite exact thresholds."
            ),
        },
        seed=6292,
    )
    verify_generated_claim("c09-spike-threshold-001.json", spike_threshold)

    for claim_id in (
        "c09-bulk-shape-001",
        "c09-finite-null-001",
        "c09-spike-threshold-001",
    ):
        print(f"verified {claim_id}.json")


if __name__ == "__main__":
    main()

"""Generate the class-(a) claim artifacts for C06."""

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
MANIFEST = ROOT / "artifacts" / "harness" / "ch-06" / "manifest.json"


def verify_generated_claim(filename: str, payload: dict[str, Any]) -> None:
    verify_claim(filename, payload, absolute_tolerance=1e-12)

manifest = json.loads(MANIFEST.read_text())
wheel = MANIFEST.parent / manifest["wheel"]
wheel_digest = sha256(wheel.read_bytes()).hexdigest()
assert wheel_digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))

from trainable_harness import (  # noqa: E402
    bernstein_two_regime_rate,
    centered_chi_square_log_mgf,
    centered_chi_square_sum_trials,
    centered_chi_square_sum_upper_tail,
    centered_chi_square_upper_tail,
    centered_pareto_clip_bias,
    observation_ledger,
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
        "phenomenon_id": "c06-square-two-regimes",
        "chapter": "c06",
        "provenance_class": "a",
        "hypothesis": hypothesis,
        "environment": environment,
        "harness_ref": manifest["harness_ref"],
        "harness_wheel_sha256": wheel_digest,
        "hardware_claim_boundary": (
            "Laptop-CPU probability calculation; no accelerator throughput "
            "or low-precision range claim."
        ),
        "result": result,
    }


def main() -> None:
    mgf_parameters = (0.1, 0.25, 0.4, 0.49)
    tail_thresholds = (1.0, 2.0, 4.0, 8.0, 16.0, 32.0)
    log_mgf = centered_chi_square_log_mgf(mgf_parameters)
    exact_tail = centered_chi_square_upper_tail(tail_thresholds)
    variance_matched_candidate = {
        threshold: float(np.exp(-(threshold**2) / 4.0))
        for threshold in tail_thresholds
    }
    violations = [
        threshold
        for threshold in tail_thresholds
        if exact_tail[threshold] > variance_matched_candidate[threshold]
    ]
    assert violations and violations[0] == 4.0
    square_break = base_record(
        claim_id="c06-square-break-001",
        hypothesis=(
            "Centering and squaring a standard normal destroys every global "
            "quadratic MGF envelope even though its upper tail remains exponential."
        ),
        result={
            "variable": "X = Z^2 - 1 for Z standard normal",
            "variance": 2.0,
            "log_mgf_formula": "-lambda - 0.5*log(1-2*lambda)",
            "finite_mgf_domain": "lambda < 0.5",
            "log_mgf_values": {
                str(parameter): log_mgf[parameter]
                for parameter in mgf_parameters
            },
            "upper_tail_thresholds": list(tail_thresholds),
            "exact_upper_tail_probabilities": {
                str(threshold): exact_tail[threshold]
                for threshold in tail_thresholds
            },
            "variance_matched_quadratic_candidate": {
                str(threshold): variance_matched_candidate[threshold]
                for threshold in tail_thresholds
            },
            "first_recorded_candidate_violation": violations[0],
            "standard_normal_psi2_norm": float(np.sqrt(8.0 / 3.0)),
            "standard_normal_square_psi1_norm": 8.0 / 3.0,
        },
        seed=None,
    )
    verify_generated_claim("c06-square-break-001.json", square_break)

    terms = 16
    trials = 500_000
    seed = 6219
    thresholds = (2.0, 4.0, 6.0, 8.0, 12.0, 16.0, 20.0, 24.0, 32.0, 40.0)
    samples = centered_chi_square_sum_trials(
        terms,
        trials=trials,
        seed=seed,
    )
    exact_sum_tail = centered_chi_square_sum_upper_tail(terms, thresholds)
    empirical_records = {}
    for threshold in thresholds:
        exceedances = int(np.count_nonzero(samples >= threshold))
        probability = exceedances / trials
        standard_error = float(
            np.sqrt(probability * (1.0 - probability) / trials)
        )
        empirical_records[str(threshold)] = {
            "exceedances": exceedances,
            "denominator": trials,
            "probability": probability,
            "binomial_standard_error": standard_error,
            "exact_probability": exact_sum_tail[threshold],
        }
        assert (
            abs(probability - exact_sum_tail[threshold])
            <= 4.0 * standard_error + 1.0 / trials
        )

    exact_chernoff = {
        threshold: float(
            np.exp(-threshold / 2.0)
            * (1.0 + threshold / terms) ** (terms / 2.0)
        )
        for threshold in thresholds
    }
    smooth_bernstein = {
        threshold: float(
            np.exp(-(threshold**2) / (4.0 * (terms + threshold)))
        )
        for threshold in thresholds
    }
    piecewise_rate = bernstein_two_regime_rate(
        thresholds,
        quadratic_scale=4.0 * terms,
        linear_scale=4.0,
    )
    two_regimes = base_record(
        claim_id="c06-two-regimes-001",
        hypothesis=(
            "A sum of centered Gaussian squares has collective quadratic-rate "
            "deviations near its mean and linear-rate control after the MGF "
            "constraint becomes active."
        ),
        result={
            "variable": "sum of 16 independent (Z_i^2 - 1)",
            "terms": terms,
            "trials": trials,
            "seed": seed,
            "stream_policy": "one declared NumPy generator, chunked generation",
            "estimator": "upper-tail exceedance proportion",
            "reduction_axis": "independent trials",
            "thresholds": list(thresholds),
            "transition_scale": float(terms),
            "empirical_records": empirical_records,
            "exact_chi_square_chernoff_upper_bounds": {
                str(threshold): exact_chernoff[threshold]
                for threshold in thresholds
            },
            "explicit_bernstein_upper_bounds": {
                str(threshold): smooth_bernstein[threshold]
                for threshold in thresholds
            },
            "piecewise_bernstein_rate": {
                str(threshold): piecewise_rate[threshold]
                for threshold in thresholds
            },
        },
        seed=seed,
    )
    verify_generated_claim("c06-two-regimes-001.json", two_regimes)

    pareto_shape = 1.5
    pareto_scale = 1.0
    clip_thresholds = (2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0)
    clipping_bias = centered_pareto_clip_bias(
        pareto_shape,
        clip_thresholds,
        scale=pareto_scale,
    )
    assert all(value < 0 for value in clipping_bias.values())
    clipping = base_record(
        claim_id="c06-clipping-bias-001",
        hypothesis=(
            "Clipping makes a heavy-tailed variable bounded but changes its "
            "mean; the concentration repair and estimator bias are distinct."
        ),
        result={
            "variable": "X = Y - E[Y], Y Pareto(shape=1.5, scale=1)",
            "pareto_shape": pareto_shape,
            "pareto_scale": pareto_scale,
            "original_mean": 0.0,
            "original_variance": "infinite",
            "positive_mgf": "infinite for every lambda > 0",
            "symmetric_clip_thresholds": list(clip_thresholds),
            "exact_clipped_mean_bias": {
                str(threshold): clipping_bias[threshold]
                for threshold in clip_thresholds
            },
            "bias_formula": "-2/sqrt(C+3)",
            "centered_clipped_proxy_variance_upper_bound": {
                str(threshold): threshold**2
                for threshold in clip_thresholds
            },
            "boundary": (
                "The centered clipped variable is sub-Gaussian by boundedness, "
                "but it estimates a clipped target unless the bias is handled."
            ),
        },
        seed=None,
    )
    verify_generated_claim("c06-clipping-bias-001.json", clipping)

    for claim_id in (
        "c06-square-break-001",
        "c06-two-regimes-001",
        "c06-clipping-bias-001",
    ):
        print(f"verified {claim_id}.json")


if __name__ == "__main__":
    main()

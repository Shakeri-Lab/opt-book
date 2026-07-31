"""Re-execute the class-(a) covariance witness registered for C10."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CLAIM = ROOT / "artifacts" / "claims" / "c10-effective-samples-001.json"
MANIFEST = ROOT / "artifacts" / "harness" / "ch-10" / "manifest.json"

claim = json.loads(CLAIM.read_text())
manifest = json.loads(MANIFEST.read_text())
wheel = MANIFEST.parent / manifest["wheel"]
wheel_digest = sha256(wheel.read_bytes()).hexdigest()
assert wheel_digest == manifest["wheel_sha256"]
assert wheel_digest == claim["harness_wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))

from trainable_harness import (  # noqa: E402
    effective_rank_psd,
    gaussian_covariance_error_trials,
)


def main() -> None:
    result = claim["result"]
    dimension = int(result["dimension"])
    spectra = {
        "isotropic": np.ones(dimension),
        "decaying": 0.82 ** np.arange(dimension),
    }
    maximum_deviation = 0.0

    for name, eigenvalues in spectra.items():
        summary = effective_rank_psd(np.diag(eigenvalues))
        expected = result["population_models"][name]
        assert summary.algebraic_rank == expected["algebraic_rank"]
        maximum_deviation = max(
            maximum_deviation,
            abs(summary.effective_rank - expected["effective_rank"]),
            abs(summary.operator_norm - expected["operator_norm"]),
            abs(summary.trace - expected["trace"]),
        )

    base_seed = int(
        sha256(claim["phenomenon_id"].encode()).hexdigest()[:8],
        16,
    )
    trials = int(result["trials_per_model_per_sample_count"])
    for samples in result["sample_counts"]:
        seed = (base_seed + int(samples)) % (2**32)
        expected_record = result["quantiles"][str(samples)]
        assert seed == expected_record["seed"]
        for name, eigenvalues in spectra.items():
            errors = gaussian_covariance_error_trials(
                eigenvalues,
                int(samples),
                trials=trials,
                seed=seed,
            )["relative_operator_error"]
            observed = np.quantile(errors, [0.1, 0.5, 0.9])
            expected = np.array(
                [
                    expected_record[name]["q10"],
                    expected_record[name]["median"],
                    expected_record[name]["q90"],
                ]
            )
            maximum_deviation = max(
                maximum_deviation,
                float(np.max(np.abs(observed - expected))),
            )

    if maximum_deviation > 1e-12:
        raise AssertionError(
            f"C10 evidence deviation {maximum_deviation:.17g} exceeds 1e-12"
        )
    if maximum_deviation == 0.0:
        print("c10 evidence: exact match")
    else:
        print(f"c10 evidence: max_abs_deviation={maximum_deviation:.3e}")


if __name__ == "__main__":
    main()

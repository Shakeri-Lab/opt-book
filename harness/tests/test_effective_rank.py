from __future__ import annotations

import numpy as np

from trainable_harness import (
    effective_rank_psd,
    gaussian_covariance_error_trials,
    stable_rank,
)


def test_effective_and_stable_rank_keep_their_distinct_contracts() -> None:
    covariance = np.diag([1.0, 0.5, 0.25])
    summary = effective_rank_psd(covariance)
    assert summary.algebraic_rank == 3
    assert summary.effective_rank == 1.75

    factor = np.diag([1.0, np.sqrt(0.5), 0.5])
    assert np.isclose(stable_rank(factor), summary.effective_rank)
    assert not np.isclose(stable_rank(covariance), summary.effective_rank)


def test_effective_rank_rejects_indefinite_and_zero_matrices() -> None:
    with np.testing.assert_raises(ValueError):
        effective_rank_psd([[1.0, 0.0], [0.0, -0.1]])
    with np.testing.assert_raises(ValueError):
        effective_rank_psd(np.zeros((2, 2)))


def test_covariance_error_trials_are_reproducible_and_shape_sensitive() -> None:
    isotropic = gaussian_covariance_error_trials(
        np.ones(16), 32, trials=100, seed=6210
    )
    repeated = gaussian_covariance_error_trials(
        np.ones(16), 32, trials=100, seed=6210
    )
    decaying = gaussian_covariance_error_trials(
        0.7 ** np.arange(16), 32, trials=100, seed=6210
    )
    for key in isotropic:
        assert np.array_equal(isotropic[key], repeated[key])
    assert np.median(decaying["relative_operator_error"]) < np.median(
        isotropic["relative_operator_error"]
    )

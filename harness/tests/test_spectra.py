from __future__ import annotations

import numpy as np

from trainable_harness import (
    covariance_eigenvalues,
    empirical_upper_threshold,
    gaussian_covariance_trials,
    gaussian_singular_value_trials,
    marchenko_pastur_density,
    marchenko_pastur_support,
    matrix_spectrum_summary,
    power_iteration_spectral_norm,
    sample_covariance,
)


def test_spectrum_summary_matches_declared_diagonal_map() -> None:
    matrix = np.diag([5.0, 2.0, 0.5])
    summary = matrix_spectrum_summary(matrix)
    assert summary.singular_values == (5.0, 2.0, 0.5)
    assert summary.sigma_max == 5.0
    assert summary.sigma_min == 0.5
    assert summary.condition_number == 10.0
    assert np.isclose(summary.mean_squared_stretch, 9.75)


def test_gaussian_trials_are_reproducible_and_isotropic_on_average() -> None:
    first = gaussian_singular_value_trials(32, 8, trials=1000, seed=6222)
    second = gaussian_singular_value_trials(32, 8, trials=1000, seed=6222)
    for key in first:
        assert np.array_equal(first[key], second[key])
    assert abs(float(np.mean(first["mean_squared_stretch"])) - 1.0) < 0.02
    assert abs(
        float(np.mean(first["fixed_direction_stretch"] ** 2)) - 1.0
    ) < 0.03


def test_power_iteration_converges_to_upper_edge_only() -> None:
    matrix = np.diag([5.0, 2.0, 0.5])
    result = power_iteration_spectral_norm(matrix, iterations=12, seed=6223)
    assert abs(result.estimates[-1] - 5.0) < 1e-8
    assert result.estimates[-1] > result.estimates[0]
    assert len(result.vector) == 3


def test_sample_covariance_declares_centering_and_denominator() -> None:
    samples = np.array([[1.0, 2.0], [3.0, 0.0], [5.0, 4.0]])
    second_moment = sample_covariance(samples)
    assert np.allclose(second_moment, samples.T @ samples / 3)

    centered = samples - np.mean(samples, axis=0, keepdims=True)
    unbiased = sample_covariance(
        samples,
        center=True,
        denominator="unbiased",
    )
    assert np.allclose(unbiased, centered.T @ centered / 2)
    assert np.allclose(
        covariance_eigenvalues(
            samples,
            center=True,
            denominator="unbiased",
        ),
        np.linalg.eigvalsh(unbiased),
    )


def test_unbiased_denominator_requires_centering() -> None:
    with np.testing.assert_raises(ValueError):
        sample_covariance([[1.0], [2.0]], denominator="unbiased")


def test_marchenko_pastur_support_and_density_contract() -> None:
    support = marchenko_pastur_support(0.5)
    assert np.isclose(support.lambda_minus, (1.0 - np.sqrt(0.5)) ** 2)
    assert np.isclose(support.lambda_plus, (1.0 + np.sqrt(0.5)) ** 2)
    assert support.zero_atom == 0.0

    wide = marchenko_pastur_support(2.0)
    assert wide.zero_atom == 0.5
    grid = np.linspace(0.0, wide.lambda_plus + 0.1, 40_000)
    density = marchenko_pastur_density(grid, 2.0)
    assert np.all(density >= 0.0)
    assert np.isclose(np.trapezoid(density, grid), 0.5, atol=2e-3)


def test_gaussian_covariance_trials_are_reproducible_and_spike_sensitive() -> None:
    null_first = gaussian_covariance_trials(
        48,
        16,
        trials=300,
        seed=6290,
    )
    null_second = gaussian_covariance_trials(
        48,
        16,
        trials=300,
        seed=6290,
    )
    spiked = gaussian_covariance_trials(
        48,
        16,
        trials=300,
        seed=6291,
        population_spike=3.0,
    )
    for key in null_first:
        assert np.array_equal(null_first[key], null_second[key])
    assert np.median(spiked["lambda_max"]) > np.median(null_first["lambda_max"])


def test_empirical_upper_threshold_uses_declared_tail_probability() -> None:
    null = np.arange(1.0, 101.0)
    threshold = empirical_upper_threshold(
        null,
        false_positive_rate=0.05,
    )
    assert threshold == np.quantile(null, 0.95, method="linear")

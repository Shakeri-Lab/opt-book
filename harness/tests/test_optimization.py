from __future__ import annotations

import numpy as np

from trainable_harness import (
    classify_mode_factors,
    quadratic_spectrum,
    quadratic_trace,
    scalar_noisy_quadratic_trials,
)


def test_quadratic_modes_follow_closed_form() -> None:
    hessian = np.diag([1.0, 100.0])
    trace = quadratic_trace(
        hessian,
        [1.0, 1.0],
        step_size=0.019,
        steps=40,
    )
    factors = np.array([0.981, -0.9])
    expected = factors[None, :] ** np.arange(41)[:, None]
    assert np.allclose(trace.mode_coordinates, expected)
    assert np.all(np.diff(trace.objectives) < 0)


def test_mode_classification_marks_stability_regimes() -> None:
    factors, labels = classify_mode_factors(
        [1.0, 100.0, 120.0],
        step_size=0.019,
    )
    assert np.allclose(factors, [0.981, -0.9, -1.28])
    assert labels == ("monotone", "oscillatory", "divergent")


def test_optimal_constant_step_balances_endpoint_modes() -> None:
    spectrum = quadratic_spectrum(np.diag([1.0, 100.0]))
    assert spectrum["condition_number"] == 100.0
    assert np.isclose(spectrum["optimal_constant_step"], 2 / 101)
    assert np.isclose(
        spectrum["optimal_worst_mode_contraction"],
        99 / 101,
    )


def test_preconditioner_compresses_conditioning() -> None:
    hessian = np.diag([1.0, 100.0])
    raw = quadratic_trace(
        hessian,
        [1.0, 1.0],
        step_size=0.019,
        steps=30,
    )
    compressed = quadratic_trace(
        hessian,
        [1.0, 1.0],
        step_size=0.4,
        steps=30,
        preconditioner=np.diag([1.0, 1 / 25]),
    )
    assert compressed.final_error_norm < 1e-6
    assert raw.final_error_norm > 0.5


def test_noisy_quadratic_matches_stationary_second_moment() -> None:
    summary = scalar_noisy_quadratic_trials(
        curvature=1.0,
        step_size=0.1,
        noise_standard_deviation=1.0,
        initial_error=3.0,
        steps=120,
        trials=20_000,
        seed=6213,
    )
    assert (
        abs(
            summary.endpoint_mean_squared_error
            - summary.stationary_second_moment
        )
        < 4 * summary.endpoint_standard_error
    )

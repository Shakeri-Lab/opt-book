from __future__ import annotations

import numpy as np

from trainable_harness import (
    bernstein_two_regime_rate,
    centered_chi_square_log_mgf,
    centered_chi_square_sum_trials,
    centered_chi_square_sum_upper_tail,
    centered_chi_square_upper_tail,
    centered_pareto_clip_bias,
)


def test_centered_chi_square_mgf_and_tail_match_closed_forms() -> None:
    log_mgf = centered_chi_square_log_mgf([0.1, 0.25])
    assert np.isclose(log_mgf[0.25], -0.25 - 0.5 * np.log(0.5))
    tails = centered_chi_square_upper_tail([0.0, 1.0])
    assert np.isclose(tails[0.0], 0.31731050786291415)
    assert np.isclose(tails[1.0], 0.15729920705028513)


def test_even_chi_square_sum_tail_matches_exponential_case() -> None:
    tails = centered_chi_square_sum_upper_tail(2, [0.0, 2.0])
    assert np.isclose(tails[0.0], np.exp(-1.0))
    assert np.isclose(tails[2.0], np.exp(-2.0))


def test_centered_chi_square_trials_are_reproducible() -> None:
    first = centered_chi_square_sum_trials(8, trials=1000, seed=6219)
    second = centered_chi_square_sum_trials(8, trials=1000, seed=6219)
    assert np.array_equal(first, second)
    assert abs(float(first.mean())) < 0.3


def test_bernstein_rate_switches_at_declared_scale() -> None:
    rates = bernstein_two_regime_rate(
        [2.0, 8.0, 32.0],
        quadratic_scale=64.0,
        linear_scale=4.0,
    )
    assert rates == {2.0: 0.0625, 8.0: 1.0, 32.0: 8.0}


def test_centered_pareto_clipping_bias_is_exact_and_monotone() -> None:
    bias = centered_pareto_clip_bias(1.5, [2.0, 8.0, 32.0])
    assert np.isclose(bias[2.0], -2.0 / np.sqrt(5.0))
    assert bias[2.0] < bias[8.0] < bias[32.0] < 0.0

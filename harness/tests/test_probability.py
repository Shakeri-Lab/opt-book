from __future__ import annotations

import numpy as np

from trainable_harness import (
    empirical_tail_profile,
    moment_growth_profile,
    rademacher_projection_trials,
    standard_normal_maxima,
    subgaussian_max_threshold,
)


def test_subgaussian_max_threshold_matches_union_bound() -> None:
    threshold = subgaussian_max_threshold(
        1_000_000,
        0.01,
        proxy_scale=1.0,
    )
    assert np.isclose(2_000_000 * np.exp(-(threshold**2) / 2), 0.01)


def test_seeded_gaussian_maxima_are_reproducible() -> None:
    counts = [100, 1_000, 10_000]
    first = standard_normal_maxima(counts, seed=6214)
    second = standard_normal_maxima(counts, seed=6214)
    assert first == second
    assert set(first) == set(counts)


def test_normalized_rademacher_projection_preserves_scale() -> None:
    width = 256
    samples = rademacher_projection_trials(
        np.ones(width) / np.sqrt(width),
        trials=20_000,
        seed=6215,
    )
    standard_error = float(samples.std(ddof=1) / np.sqrt(samples.size))
    assert abs(float(samples.mean())) < 4 * standard_error
    assert abs(float(samples.var(ddof=1)) - 1.0) < 0.04


def test_empirical_tail_and_moment_profiles_declare_denominators() -> None:
    samples = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    tails = empirical_tail_profile(samples, [1.0, 2.0])
    moments = moment_growth_profile(samples, [1, 2])
    assert tails == {1.0: 0.8, 2.0: 0.4}
    assert moments[1] == 1.2
    assert np.isclose(moments[2], np.sqrt(2) / np.sqrt(2))

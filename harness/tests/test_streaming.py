from __future__ import annotations

import numpy as np

from trainable_harness import (
    comparison_audit,
    merge_moments,
    naive_moments,
    stable_online_moments,
)


def test_welford_matches_float64_reference_on_centered_values() -> None:
    values = np.array([-2.0, -1.0, 0.0, 1.0, 2.0], dtype=np.float32)
    state = stable_online_moments(values, dtype=np.float32)
    assert state.count == 5
    assert np.isclose(state.mean, 0.0)
    assert np.isclose(state.population_variance, 2.0)


def test_pairwise_merge_recovers_between_group_variance() -> None:
    left = stable_online_moments([0.0, 0.0], dtype=np.float64)
    right = stable_online_moments([10.0, 10.0], dtype=np.float64)
    merged = merge_moments(left, right)
    assert merged.count == 4
    assert np.isclose(merged.mean, 5.0)
    assert np.isclose(merged.population_variance, 25.0)


def test_merge_with_empty_state_is_identity() -> None:
    empty = stable_online_moments([], dtype=np.float32)
    state = stable_online_moments([1.0, 2.0, 3.0], dtype=np.float32)
    assert merge_moments(empty, state) == state
    assert merge_moments(state, empty) == state


def test_dtype_mismatch_is_rejected() -> None:
    left = stable_online_moments([1.0], dtype=np.float32)
    right = stable_online_moments([1.0], dtype=np.float64)
    try:
        merge_moments(left, right)
    except ValueError as error:
        assert "dtype mismatch" in str(error)
    else:
        raise AssertionError("dtype mismatch should fail")


def test_seeded_crash_exposes_negative_naive_variance() -> None:
    rng = np.random.default_rng(6210)
    values = (20_000.0 + rng.normal(size=200_000)).astype(np.float32)
    audit = comparison_audit(values, dtype=np.float32)
    assert audit["naive"]["population_variance"] < 0.0
    assert audit["two_pass"]["relative_error"] < 1e-5
    assert audit["welford"]["relative_error"] < 0.005


def test_naive_result_records_the_declared_dtype() -> None:
    state = naive_moments([1.0, 2.0, 3.0], dtype=np.float32)
    assert state.dtype == "float32"
    assert state.method == "naive"

import numpy as np

from trainable_harness import (
    relu_correlation_trace,
    relu_moment_fluctuation_variance,
)


def test_relu_pair_geometry_loses_finite_separation() -> None:
    trace = relu_correlation_trace(0.5, 64)
    assert trace[0] == 0.5
    assert np.all(np.diff(trace) > 0)
    assert trace[-1] > 0.99
    assert relu_correlation_trace(1.0, 3).tolist() == [1.0] * 4


def test_relu_moment_fluctuation_control() -> None:
    width, depth = 64, 8
    expected = (1.0 + 5.0 / width) ** depth - 1.0
    assert np.isclose(
        relu_moment_fluctuation_variance(width, depth), expected
    )
    assert relu_moment_fluctuation_variance(width, 0) == 0.0


def test_criticality_argument_validation() -> None:
    for correlation in (-1.01, 1.01):
        with np.testing.assert_raises(ValueError):
            relu_correlation_trace(correlation, 1)
    with np.testing.assert_raises(ValueError):
        relu_moment_fluctuation_variance(0, 1)

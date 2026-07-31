import numpy as np

from trainable_harness import deep_linear_product, mean_squared_singular_value, relu_variance_trace


def test_relu_critical_scale() -> None:
    np.testing.assert_allclose(relu_variance_trace(1.0, 2.0, 8), 1.0)
    assert relu_variance_trace(1.0, 1.0, 8)[-1] < 0.01
    assert relu_variance_trace(1.0, 3.0, 8)[-1] > 20.0


def test_average_does_not_determine_edges() -> None:
    matrix = np.diag([np.sqrt(2.0), 0.0])
    assert np.isclose(mean_squared_singular_value(matrix), 1.0)
    assert np.linalg.svd(matrix, compute_uv=False)[-1] == 0.0
    np.testing.assert_allclose(deep_linear_product([np.eye(2), matrix]), matrix)

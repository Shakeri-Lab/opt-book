import numpy as np

from trainable_harness import centered_normalize, normalization_jacobian, raw_and_centered_variance, rms_normalize


def test_centered_and_rms_have_different_invariances() -> None:
    x = np.array([-2.0, -1.0, 1.0, 2.0])
    np.testing.assert_allclose(centered_normalize(x), centered_normalize(x + 10.0))
    assert not np.allclose(rms_normalize(x), rms_normalize(x + 10.0))


def test_jacobian_nullspaces_and_variance() -> None:
    x = np.array([-2.0, -1.0, 1.0, 2.0])
    assert np.linalg.matrix_rank(normalization_jacobian(x, centered=True), tol=1e-10) == 2
    assert np.linalg.matrix_rank(normalization_jacobian(x, centered=False), tol=1e-10) == 3
    raw, centered = raw_and_centered_variance(np.array([9998, 9999, 10001, 10002]))
    assert raw == 0.0
    assert centered == 2.5

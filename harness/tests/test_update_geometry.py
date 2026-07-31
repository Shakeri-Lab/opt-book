import numpy as np

from trainable_harness import newton_schulz_polar, norm_steepest_directions, polar_factor


def test_matrix_norm_duality_and_polar_iteration() -> None:
    matrix = np.diag([9.0, 2.0, 0.5])
    directions = norm_steepest_directions(matrix)
    assert np.isclose(np.linalg.norm(directions["frobenius"], "fro"), 1.0)
    assert np.isclose(np.linalg.norm(directions["operator"], 2), 1.0)
    assert np.isclose(np.linalg.norm(directions["nuclear"], "nuc"), 1.0)
    approximate, residuals = newton_schulz_polar(matrix, 12)
    np.testing.assert_allclose(approximate, polar_factor(matrix), atol=1e-10)
    assert residuals[-1] < residuals[0]


def test_polar_equivariance() -> None:
    rng = np.random.default_rng(6210)
    matrix = rng.normal(size=(6, 4))
    q, _ = np.linalg.qr(rng.normal(size=(6, 6)))
    r, _ = np.linalg.qr(rng.normal(size=(4, 4)))
    np.testing.assert_allclose(polar_factor(q @ matrix @ r), q @ polar_factor(matrix) @ r)

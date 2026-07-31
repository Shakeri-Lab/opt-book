import numpy as np

from trainable_harness import (
    bernoulli_curvature_matrices,
    bernoulli_hessian_vector_product,
    dominant_symmetric_eigenpair,
)


def test_affine_logit_hessian_matches_ggn_and_model_fisher() -> None:
    inputs = np.array([-2.0, -1.0, 1.0, 2.0])
    labels = np.array([0.0, 0.0, 1.0, 1.0])
    matrices = bernoulli_curvature_matrices(
        np.array([0.5, 0.0]),
        inputs,
        labels,
        nonlinear_first_parameter=False,
    )
    np.testing.assert_allclose(matrices.hessian, matrices.generalized_gauss_newton)
    np.testing.assert_allclose(matrices.generalized_gauss_newton, matrices.model_fisher)
    assert not np.allclose(matrices.empirical_fisher, matrices.model_fisher)


def test_composed_logit_has_negative_realized_curvature() -> None:
    inputs = np.array([-2.0, -1.0, 1.0, 2.0])
    labels = np.array([0.0, 0.0, 1.0, 1.0])
    parameters = np.array([0.5, 0.0])
    matrices = bernoulli_curvature_matrices(
        parameters,
        inputs,
        labels,
        nonlinear_first_parameter=True,
    )
    assert np.linalg.eigvalsh(matrices.hessian)[0] < 0.0
    assert np.linalg.eigvalsh(matrices.generalized_gauss_newton)[0] >= 0.0
    vector = np.array([0.3, -0.7])
    product = bernoulli_hessian_vector_product(
        parameters,
        inputs,
        labels,
        vector,
        nonlinear_first_parameter=True,
    )
    np.testing.assert_allclose(product, matrices.hessian @ vector)


def test_operator_iteration_recovers_dominant_magnitude_eigenpair() -> None:
    matrix = np.array([[-1.2, 0.1], [0.1, 0.25]])
    expected = np.linalg.eigvalsh(matrix)
    result = dominant_symmetric_eigenpair(
        lambda vector: matrix @ vector,
        2,
        iterations=24,
        seed=6210,
    )
    assert abs(result.eigenvalue - expected[0]) < 1e-12
    assert result.residual_norm < 1e-12

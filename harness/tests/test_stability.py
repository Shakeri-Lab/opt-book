import numpy as np

from trainable_harness import moving_curvature_trace, valley_loss_gradient_hessian


def test_hessian_matches_finite_difference() -> None:
    state = np.array([0.7, 0.3])
    _, _, hessian = valley_loss_gradient_hessian(state)
    eps = 1e-6
    columns = []
    for basis in np.eye(2):
        gp = valley_loss_gradient_hessian(state + eps * basis)[1]
        gm = valley_loss_gradient_hessian(state - eps * basis)[1]
        columns.append((gp - gm) / (2 * eps))
    np.testing.assert_allclose(hessian, np.column_stack(columns), atol=1e-9)


def test_boundary_moves_during_descent() -> None:
    trace = moving_curvature_trace(np.zeros(2), 0.2, 350)
    assert trace.top_curvatures[0] < 10.0
    assert np.max(trace.top_curvatures) > 10.0
    assert np.any(np.diff(trace.losses) > 0.0)

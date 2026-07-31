import numpy as np

from trainable_harness import (
    conditional_safe_step,
    scalar_quadratic_regime,
    two_point_clipping_audit,
)


def test_same_mean_gradient_different_regimes() -> None:
    low = scalar_quadratic_regime(1.0, 0.5, 0.25)
    high = scalar_quadratic_regime(1.0, 0.5, 4.0)
    assert low.expected_next_loss == 0.15625
    assert high.expected_next_loss == 0.625
    assert conditional_safe_step(1.0, 0.25, 1.0) == 1.6
    assert conditional_safe_step(1.0, 4.0, 1.0) == 0.4


def test_clipping_changes_the_estimator() -> None:
    audit = two_point_clipping_audit(
        np.array([-9.0, 19.0 / 9.0]), np.array([0.1, 0.9]), 2.0
    )
    assert np.isclose(audit["mean"], 1.0)
    assert np.isclose(audit["clipped_mean"], 1.6)
    assert audit["clipped_variance"] < audit["variance"]

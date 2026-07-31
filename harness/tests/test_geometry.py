from __future__ import annotations

import numpy as np

from trainable_harness import (
    circle_covering_radius,
    circle_epsilon_net,
    operator_net_certificate,
    operator_net_estimate,
    sphere_cover_log_upper,
    uniform_subgaussian_threshold,
)


def test_circle_net_respects_declared_covering_radius() -> None:
    for epsilon in (0.8, 0.4, 0.2):
        net = circle_epsilon_net(epsilon)
        assert circle_covering_radius(net) <= epsilon + 1e-12
        assert np.allclose(np.linalg.norm(net, axis=1), 1.0)


def test_operator_net_certificate_covers_exact_norm() -> None:
    angle = 0.37
    rotation = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    matrix = rotation @ np.diag([6.0, 1.0]) @ rotation.T
    epsilon = 0.35
    net = circle_epsilon_net(epsilon)
    actual_radius = circle_covering_radius(net)
    estimate = operator_net_estimate(matrix, net)
    certificate = operator_net_certificate(estimate, actual_radius)
    assert estimate <= np.linalg.norm(matrix, ord=2)
    assert certificate >= np.linalg.norm(matrix, ord=2)


def test_cover_log_and_tail_threshold_match_declared_formulas() -> None:
    dimension = 40
    epsilon = 0.25
    delta = 0.01
    log_cover = sphere_cover_log_upper(dimension, epsilon)
    threshold = uniform_subgaussian_threshold(log_cover, delta)
    assert np.isclose(log_cover, dimension * np.log(1 + 2 / epsilon))
    assert np.isclose(
        2 * np.exp(log_cover - threshold**2 / 2),
        delta,
    )

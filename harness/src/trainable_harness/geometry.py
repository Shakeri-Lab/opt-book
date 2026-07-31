"""Finite-cover diagnostics introduced with C07."""

from __future__ import annotations

from collections.abc import Iterable
from math import asin, ceil, log, log1p, pi, sin, sqrt

import numpy as np


def circle_epsilon_net(epsilon: float) -> np.ndarray:
    """Return equally spaced unit vectors whose chord covering radius is at most epsilon."""

    if not 0 < epsilon < 2:
        raise ValueError("epsilon must lie in (0, 2)")
    points = ceil(pi / (2.0 * asin(epsilon / 2.0)))
    angles = 2.0 * pi * np.arange(points, dtype=np.float64) / points
    return np.column_stack((np.cos(angles), np.sin(angles)))


def circle_covering_radius(net: Iterable[Iterable[float]]) -> float:
    """Return the exact Euclidean covering radius of ordered points on the unit circle."""

    points = np.asarray(tuple(tuple(row) for row in net), dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 2 or points.shape[0] < 1:
        raise ValueError("net must be a nonempty collection of two-dimensional points")
    norms = np.linalg.norm(points, axis=1)
    if not np.allclose(norms, 1.0, atol=1e-12, rtol=1e-12):
        raise ValueError("every net point must have unit Euclidean norm")
    angles = np.sort(np.mod(np.arctan2(points[:, 1], points[:, 0]), 2.0 * pi))
    gaps = np.diff(np.concatenate((angles, angles[:1] + 2.0 * pi)))
    return float(2.0 * sin(float(np.max(gaps)) / 4.0))


def operator_net_estimate(
    matrix: Iterable[Iterable[float]],
    net: Iterable[Iterable[float]],
) -> float:
    """Return the largest Euclidean stretch observed on declared unit net points."""

    resolved_matrix = np.asarray(tuple(tuple(row) for row in matrix), dtype=np.float64)
    points = np.asarray(tuple(tuple(row) for row in net), dtype=np.float64)
    if resolved_matrix.ndim != 2 or min(resolved_matrix.shape) < 1:
        raise ValueError("matrix must be nonempty and two-dimensional")
    if (
        points.ndim != 2
        or points.shape[0] < 1
        or points.shape[1] != resolved_matrix.shape[1]
    ):
        raise ValueError("net points must match the matrix input dimension")
    if not np.allclose(np.linalg.norm(points, axis=1), 1.0, atol=1e-12, rtol=1e-12):
        raise ValueError("every net point must have unit Euclidean norm")
    stretches = np.linalg.norm(points @ resolved_matrix.T, axis=1)
    return float(np.max(stretches))


def operator_net_certificate(net_maximum: float, epsilon: float) -> float:
    """Return the standard epsilon-net upper certificate for an operator norm."""

    if net_maximum < 0:
        raise ValueError("net_maximum must be nonnegative")
    if not 0 < epsilon < 1:
        raise ValueError("epsilon must lie in (0, 1)")
    return float(net_maximum / (1.0 - epsilon))


def sphere_cover_log_upper(dimension: int, epsilon: float) -> float:
    """Return ``log((1 + 2/epsilon)**dimension)`` without forming the cover."""

    if dimension < 1:
        raise ValueError("dimension must be positive")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    return float(dimension * log1p(2.0 / epsilon))


def uniform_subgaussian_threshold(
    log_cover: float,
    failure_probability: float,
    *,
    proxy_scale: float = 1.0,
) -> float:
    """Return the anchor threshold for a two-sided sub-Gaussian cover union bound."""

    if log_cover < 0:
        raise ValueError("log_cover must be nonnegative")
    if not 0 < failure_probability < 1:
        raise ValueError("failure_probability must lie in (0, 1)")
    if proxy_scale <= 0:
        raise ValueError("proxy_scale must be positive")
    return float(
        proxy_scale
        * sqrt(2.0 * (log(2.0 / failure_probability) + log_cover))
    )

"""Coordinate-wise normalization diagnostics."""

from __future__ import annotations

import numpy as np


def centered_normalize(vector: np.ndarray, epsilon: float = 0.0) -> np.ndarray:
    """Center coordinates, then divide by their root mean square."""
    x = np.asarray(vector, dtype=float)
    centered = x - x.mean()
    scale = np.sqrt(np.mean(centered**2) + epsilon)
    if scale == 0:
        raise ValueError("centered scale is zero")
    return centered / scale


def rms_normalize(vector: np.ndarray, epsilon: float = 0.0) -> np.ndarray:
    """Divide coordinates by their uncentered root mean square."""
    x = np.asarray(vector, dtype=float)
    scale = np.sqrt(np.mean(x**2) + epsilon)
    if scale == 0:
        raise ValueError("root mean square is zero")
    return x / scale


def normalization_jacobian(vector: np.ndarray, *, centered: bool) -> np.ndarray:
    """Exact zero-epsilon Jacobian away from degenerate states."""
    x = np.asarray(vector, dtype=float)
    d = x.size
    projector = np.eye(d) - np.ones((d, d)) / d if centered else np.eye(d)
    state = projector @ x
    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("normalization Jacobian is singular at this state")
    direction = state / norm
    return np.sqrt(d) / norm * (projector - np.outer(direction, direction))


def raw_and_centered_variance(vector: np.ndarray, dtype: np.dtype = np.float32) -> tuple[float, float]:
    """Compare raw-moment and centered variance in a declared dtype."""
    x = np.asarray(vector, dtype=dtype)
    raw = np.mean(x * x, dtype=dtype) - np.mean(x, dtype=dtype) ** 2
    centered = np.mean((x - np.mean(x, dtype=dtype)) ** 2, dtype=dtype)
    return float(raw), float(centered)

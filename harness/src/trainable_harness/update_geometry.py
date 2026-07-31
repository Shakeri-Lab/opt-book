"""Matrix-norm update geometry and polar-factor approximations."""

from __future__ import annotations

import numpy as np


def polar_factor(matrix: np.ndarray) -> np.ndarray:
    """Return the rectangular polar factor U V^T from a thin SVD."""
    u, _, vt = np.linalg.svd(np.asarray(matrix, dtype=float), full_matrices=False)
    return u @ vt


def norm_steepest_directions(matrix: np.ndarray) -> dict[str, np.ndarray]:
    """Unit-ball steepest directions for Frobenius, operator, and nuclear norms."""
    g = np.asarray(matrix, dtype=float)
    u, _, vt = np.linalg.svd(g, full_matrices=False)
    frobenius = -g / np.linalg.norm(g, "fro")
    operator = -(u @ vt)
    nuclear = -np.outer(u[:, 0], vt[0, :])
    return {"frobenius": frobenius, "operator": operator, "nuclear": nuclear}


def newton_schulz_polar(matrix: np.ndarray, steps: int) -> tuple[np.ndarray, np.ndarray]:
    """Approximate a polar factor after Frobenius scaling; return residual history."""
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    x = np.asarray(matrix, dtype=float) / np.linalg.norm(matrix, "fro")
    residuals = [np.linalg.norm(x.T @ x - np.eye(x.shape[1]), "fro")]
    for _ in range(steps):
        x = 1.5 * x - 0.5 * x @ (x.T @ x)
        residuals.append(np.linalg.norm(x.T @ x - np.eye(x.shape[1]), "fro"))
    return x, np.asarray(residuals)

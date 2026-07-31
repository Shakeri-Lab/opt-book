"""Signal propagation and Jacobian-spectrum diagnostics."""

from __future__ import annotations

import numpy as np


def relu_variance_trace(initial_variance: float, weight_scale: float, depth: int) -> np.ndarray:
    """Wide-model ReLU second-moment recursion q <- scale*q/2."""
    if initial_variance < 0 or weight_scale < 0 or depth < 0:
        raise ValueError("variance, scale, and depth must be nonnegative")
    trace = np.empty(depth + 1, dtype=float)
    trace[0] = initial_variance
    for layer in range(depth):
        trace[layer + 1] = 0.5 * weight_scale * trace[layer]
    return trace


def deep_linear_product(matrices: list[np.ndarray]) -> np.ndarray:
    """Compose square matrices in forward layer order."""
    if not matrices:
        raise ValueError("at least one matrix is required")
    product = np.eye(np.asarray(matrices[0]).shape[1])
    for matrix in matrices:
        array = np.asarray(matrix, dtype=float)
        if array.ndim != 2 or array.shape[1] != product.shape[0]:
            raise ValueError("incompatible matrix chain")
        product = array @ product
    return product


def mean_squared_singular_value(matrix: np.ndarray) -> float:
    """Return tr(J^T J)/input_dimension."""
    array = np.asarray(matrix, dtype=float)
    if array.ndim != 2 or array.shape[1] == 0:
        raise ValueError("matrix must have a nonempty input dimension")
    return float(np.sum(array * array) / array.shape[1])

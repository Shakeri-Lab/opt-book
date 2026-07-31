"""Small curvature operators for the C12 diagnostic witnesses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class CurvatureMatrices:
    """Four named curvature objects and the Hessian term omitted by GGN."""

    hessian: np.ndarray
    generalized_gauss_newton: np.ndarray
    model_fisher: np.ndarray
    empirical_fisher: np.ndarray
    model_curvature: np.ndarray


@dataclass(frozen=True)
class EigenpairEstimate:
    """Dominant-magnitude eigenpair estimate from matrix-vector products."""

    eigenvalue: float
    eigenvector: np.ndarray
    residual_norm: float
    rayleigh_trace: tuple[float, ...]


def _sigmoid(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64)
    result = np.empty_like(values)
    positive = values >= 0
    result[positive] = 1.0 / (1.0 + np.exp(-values[positive]))
    exponent = np.exp(values[~positive])
    result[~positive] = exponent / (1.0 + exponent)
    return result


def bernoulli_curvature_matrices(
    parameters: np.ndarray,
    inputs: np.ndarray,
    labels: np.ndarray,
    *,
    nonlinear_first_parameter: bool,
) -> CurvatureMatrices:
    """Curvatures for mean Bernoulli NLL with z=a^2 x+b or z=ax+b."""
    parameters = np.asarray(parameters, dtype=np.float64)
    inputs = np.asarray(inputs, dtype=np.float64)
    labels = np.asarray(labels, dtype=np.float64)
    if parameters.shape != (2,):
        raise ValueError("parameters must have shape (2,)")
    if inputs.ndim != 1 or labels.shape != inputs.shape or inputs.size == 0:
        raise ValueError("inputs and labels must be same-length nonempty vectors")
    if np.any((labels < 0.0) | (labels > 1.0)):
        raise ValueError("Bernoulli labels must lie in [0, 1]")

    first, intercept = parameters
    if nonlinear_first_parameter:
        logits = first**2 * inputs + intercept
        jacobian = np.column_stack((2.0 * first * inputs, np.ones_like(inputs)))
        logit_hessians = np.zeros((inputs.size, 2, 2), dtype=np.float64)
        logit_hessians[:, 0, 0] = 2.0 * inputs
    else:
        logits = first * inputs + intercept
        jacobian = np.column_stack((inputs, np.ones_like(inputs)))
        logit_hessians = np.zeros((inputs.size, 2, 2), dtype=np.float64)

    probabilities = _sigmoid(logits)
    output_curvature = probabilities * (1.0 - probabilities)
    residuals = probabilities - labels
    ggn = np.einsum(
        "i,ij,ik->jk",
        output_curvature,
        jacobian,
        jacobian,
    ) / inputs.size
    model_curvature = np.einsum(
        "i,ijk->jk",
        residuals,
        logit_hessians,
    ) / inputs.size
    per_example_gradients = residuals[:, None] * jacobian
    empirical_fisher = (
        per_example_gradients.T @ per_example_gradients / inputs.size
    )
    return CurvatureMatrices(
        hessian=ggn + model_curvature,
        generalized_gauss_newton=ggn,
        model_fisher=ggn.copy(),
        empirical_fisher=empirical_fisher,
        model_curvature=model_curvature,
    )


def bernoulli_hessian_vector_product(
    parameters: np.ndarray,
    inputs: np.ndarray,
    labels: np.ndarray,
    vector: np.ndarray,
    *,
    nonlinear_first_parameter: bool,
) -> np.ndarray:
    """Apply the realized Hessian without constructing its dense matrix."""
    parameters = np.asarray(parameters, dtype=np.float64)
    inputs = np.asarray(inputs, dtype=np.float64)
    labels = np.asarray(labels, dtype=np.float64)
    vector = np.asarray(vector, dtype=np.float64)
    if parameters.shape != (2,) or vector.shape != (2,):
        raise ValueError("parameters and vector must have shape (2,)")

    first, intercept = parameters
    if nonlinear_first_parameter:
        logits = first**2 * inputs + intercept
        jacobian = np.column_stack((2.0 * first * inputs, np.ones_like(inputs)))
        model_action = np.column_stack(
            (2.0 * inputs * vector[0], np.zeros_like(inputs))
        )
    else:
        logits = first * inputs + intercept
        jacobian = np.column_stack((inputs, np.ones_like(inputs)))
        model_action = np.zeros((inputs.size, 2), dtype=np.float64)
    probabilities = _sigmoid(logits)
    residuals = probabilities - labels
    output_curvature = probabilities * (1.0 - probabilities)
    return np.mean(
        output_curvature[:, None]
        * jacobian
        * (jacobian @ vector)[:, None]
        + residuals[:, None] * model_action,
        axis=0,
    )


def dominant_symmetric_eigenpair(
    matvec: Callable[[np.ndarray], np.ndarray],
    dimension: int,
    *,
    iterations: int,
    seed: int,
) -> EigenpairEstimate:
    """Estimate the largest-magnitude eigenpair of a symmetric operator."""
    if dimension < 1 or iterations < 1:
        raise ValueError("dimension and iterations must be positive")
    rng = np.random.default_rng(seed)
    vector = rng.normal(size=dimension)
    vector /= np.linalg.norm(vector)
    trace: list[float] = []
    for _ in range(iterations):
        action = np.asarray(matvec(vector), dtype=np.float64)
        if action.shape != (dimension,):
            raise ValueError("matvec returned the wrong shape")
        norm = np.linalg.norm(action)
        if norm == 0.0:
            raise ValueError("power iteration encountered a zero action")
        vector = action / norm
        trace.append(float(vector @ np.asarray(matvec(vector), dtype=np.float64)))
    action = np.asarray(matvec(vector), dtype=np.float64)
    eigenvalue = float(vector @ action)
    return EigenpairEstimate(
        eigenvalue=eigenvalue,
        eigenvector=vector,
        residual_norm=float(np.linalg.norm(action - eigenvalue * vector)),
        rayleigh_trace=tuple(trace),
    )

"""Quadratic control experiments introduced with C04."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class QuadraticTrace:
    """Iterates and exact diagnostics for a centered positive-definite quadratic."""

    hessian: np.ndarray
    initial_error: np.ndarray
    step_size: float
    preconditioner: np.ndarray
    iterates: np.ndarray
    objectives: np.ndarray
    eigenvalues: np.ndarray
    mode_coordinates: np.ndarray
    mode_factors: np.ndarray

    @property
    def final_error_norm(self) -> float:
        return float(np.linalg.norm(self.iterates[-1]))


@dataclass(frozen=True)
class NoisyQuadraticSummary:
    """Monte Carlo second moments for a scalar noisy quadratic recurrence."""

    curvature: float
    step_size: float
    noise_standard_deviation: float
    initial_error: float
    trials: int
    seed: int
    mean_squared_error: np.ndarray
    endpoint_squared_errors: np.ndarray

    @property
    def stationary_second_moment(self) -> float:
        numerator = self.step_size * self.noise_standard_deviation**2
        denominator = self.curvature * (
            2.0 - self.step_size * self.curvature
        )
        return numerator / denominator

    @property
    def endpoint_mean_squared_error(self) -> float:
        return float(self.mean_squared_error[-1])

    @property
    def endpoint_standard_error(self) -> float:
        return float(
            self.endpoint_squared_errors.std(ddof=1) / np.sqrt(self.trials)
        )


def _symmetric_positive_definite(matrix: np.ndarray) -> np.ndarray:
    resolved = np.asarray(matrix, dtype=np.float64)
    if resolved.ndim != 2 or resolved.shape[0] != resolved.shape[1]:
        raise ValueError("hessian must be a square matrix")
    if not np.allclose(resolved, resolved.T):
        raise ValueError("hessian must be symmetric")
    if np.linalg.eigvalsh(resolved).min() <= 0:
        raise ValueError("hessian must be positive definite")
    return resolved


def quadratic_spectrum(hessian: np.ndarray) -> dict[str, float]:
    """Return the exact spectral control fields for a positive-definite Hessian."""

    resolved = _symmetric_positive_definite(hessian)
    eigenvalues = np.linalg.eigvalsh(resolved)
    smallest = float(eigenvalues[0])
    largest = float(eigenvalues[-1])
    condition_number = largest / smallest
    optimal_step = 2.0 / (largest + smallest)
    optimal_contraction = (condition_number - 1.0) / (
        condition_number + 1.0
    )
    return {
        "smallest_eigenvalue": smallest,
        "largest_eigenvalue": largest,
        "condition_number": condition_number,
        "largest_stable_step": 2.0 / largest,
        "optimal_constant_step": optimal_step,
        "optimal_worst_mode_contraction": optimal_contraction,
    }


def classify_mode_factors(
    eigenvalues: Iterable[float], *, step_size: float
) -> tuple[np.ndarray, tuple[str, ...]]:
    """Return scalar mode factors and their monotone/oscillatory behavior."""

    values = np.asarray(tuple(eigenvalues), dtype=np.float64)
    if values.ndim != 1 or values.size == 0 or np.any(values <= 0):
        raise ValueError("eigenvalues must be a nonempty positive sequence")
    if step_size <= 0:
        raise ValueError("step_size must be positive")
    factors = 1.0 - float(step_size) * values
    labels = []
    for factor in factors:
        if factor == 0:
            labels.append("annihilated")
        elif 0 < factor < 1:
            labels.append("monotone")
        elif -1 < factor < 0:
            labels.append("oscillatory")
        elif abs(factor) == 1:
            labels.append("boundary")
        else:
            labels.append("divergent")
    return factors, tuple(labels)


def quadratic_trace(
    hessian: np.ndarray,
    initial_error: Iterable[float],
    *,
    step_size: float,
    steps: int,
    preconditioner: np.ndarray | None = None,
) -> QuadraticTrace:
    """Run exact gradient steps on ``0.5 * e.T @ H @ e``."""

    resolved = _symmetric_positive_definite(hessian)
    error = np.asarray(tuple(initial_error), dtype=np.float64)
    dimension = resolved.shape[0]
    if error.shape != (dimension,):
        raise ValueError(f"initial_error must have shape ({dimension},)")
    if step_size <= 0 or steps < 0:
        raise ValueError("step_size must be positive and steps nonnegative")
    if preconditioner is None:
        transform = np.eye(dimension)
    else:
        transform = _symmetric_positive_definite(preconditioner)

    eigenvalues, eigenvectors = np.linalg.eigh(resolved)
    factors = 1.0 - float(step_size) * eigenvalues
    iterates = np.empty((steps + 1, dimension), dtype=np.float64)
    objectives = np.empty(steps + 1, dtype=np.float64)
    iterates[0] = error
    objectives[0] = 0.5 * error @ resolved @ error
    for index in range(1, steps + 1):
        error = error - float(step_size) * transform @ (resolved @ error)
        iterates[index] = error
        objectives[index] = 0.5 * error @ resolved @ error

    return QuadraticTrace(
        hessian=resolved,
        initial_error=iterates[0].copy(),
        step_size=float(step_size),
        preconditioner=transform,
        iterates=iterates,
        objectives=objectives,
        eigenvalues=eigenvalues,
        mode_coordinates=iterates @ eigenvectors,
        mode_factors=factors,
    )


def scalar_noisy_quadratic_trials(
    *,
    curvature: float,
    step_size: float,
    noise_standard_deviation: float,
    initial_error: float,
    steps: int,
    trials: int,
    seed: int,
) -> NoisyQuadraticSummary:
    """Simulate ``e[t+1] = (1-alpha*lambda)e[t] - alpha*noise[t]``."""

    if curvature <= 0 or step_size <= 0:
        raise ValueError("curvature and step_size must be positive")
    if step_size * curvature >= 2:
        raise ValueError("the scalar recurrence must be strictly stable")
    if noise_standard_deviation < 0 or steps < 0 or trials < 2:
        raise ValueError("invalid noise, step, or trial contract")

    rng = np.random.default_rng(seed)
    states = np.full(trials, initial_error, dtype=np.float64)
    mean_squared_error = np.empty(steps + 1, dtype=np.float64)
    mean_squared_error[0] = float(np.mean(states**2))
    factor = 1.0 - float(step_size) * float(curvature)
    for index in range(1, steps + 1):
        noise = rng.normal(0.0, noise_standard_deviation, size=trials)
        states = factor * states - float(step_size) * noise
        mean_squared_error[index] = float(np.mean(states**2))

    return NoisyQuadraticSummary(
        curvature=float(curvature),
        step_size=float(step_size),
        noise_standard_deviation=float(noise_standard_deviation),
        initial_error=float(initial_error),
        trials=int(trials),
        seed=int(seed),
        mean_squared_error=mean_squared_error,
        endpoint_squared_errors=states**2,
    )

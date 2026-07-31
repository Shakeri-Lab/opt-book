"""Conditional stochastic-gradient diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class QuadraticRegime:
    """One-step conditional diagnostic for a scalar quadratic."""

    expected_next_loss: float
    deterministic_next_loss: float
    noise_penalty: float
    noise_to_signal: float


def scalar_quadratic_regime(
    state: float,
    step_size: float,
    noise_variance: float,
    *,
    curvature: float = 1.0,
) -> QuadraticRegime:
    """Return the exact one-step expectation for an unbiased noisy gradient."""
    if curvature <= 0 or noise_variance < 0:
        raise ValueError("curvature must be positive and variance nonnegative")
    gradient = curvature * state
    deterministic_next = state - step_size * gradient
    deterministic_loss = 0.5 * curvature * deterministic_next**2
    noise_penalty = 0.5 * curvature * step_size**2 * noise_variance
    signal = gradient**2
    ratio = float("inf") if signal == 0 and noise_variance else noise_variance / signal
    return QuadraticRegime(
        expected_next_loss=deterministic_loss + noise_penalty,
        deterministic_next_loss=deterministic_loss,
        noise_penalty=noise_penalty,
        noise_to_signal=ratio,
    )


def conditional_safe_step(
    gradient_norm: float,
    noise_variance: float,
    smoothness: float,
) -> float:
    """Largest strict-descent threshold from the conditional descent lemma."""
    if smoothness <= 0 or noise_variance < 0 or gradient_norm < 0:
        raise ValueError("invalid smoothness, variance, or gradient norm")
    signal = gradient_norm**2
    if signal == 0:
        return 0.0
    return (2.0 / smoothness) / (1.0 + noise_variance / signal)


def two_point_clipping_audit(
    values: np.ndarray,
    probabilities: np.ndarray,
    threshold: float,
) -> dict[str, float]:
    """Compare population moments before and after symmetric clipping."""
    x = np.asarray(values, dtype=float)
    p = np.asarray(probabilities, dtype=float)
    if x.shape != p.shape or x.ndim != 1:
        raise ValueError("values and probabilities must be matching vectors")
    if threshold <= 0 or np.any(p < 0) or not np.isclose(p.sum(), 1.0):
        raise ValueError("invalid threshold or probabilities")
    clipped = np.clip(x, -threshold, threshold)
    mean = float(p @ x)
    clipped_mean = float(p @ clipped)
    variance = float(p @ (x - mean) ** 2)
    clipped_variance = float(p @ (clipped - clipped_mean) ** 2)
    return {
        "mean": mean,
        "clipped_mean": clipped_mean,
        "bias": clipped_mean - mean,
        "variance": variance,
        "clipped_variance": clipped_variance,
    }

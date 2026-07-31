"""Sub-Gaussian diagnostics introduced with C05."""

from __future__ import annotations

from collections.abc import Iterable
from math import erfc, exp, factorial, sqrt

import numpy as np


def subgaussian_max_threshold(
    count: int,
    failure_probability: float,
    *,
    proxy_scale: float = 1.0,
) -> float:
    """Return the union-bound threshold for ``count`` sub-Gaussian variables."""

    if count < 1:
        raise ValueError("count must be positive")
    if not 0 < failure_probability < 1:
        raise ValueError("failure_probability must lie in (0, 1)")
    if proxy_scale <= 0:
        raise ValueError("proxy_scale must be positive")
    return float(
        proxy_scale
        * np.sqrt(2.0 * np.log(2.0 * count / failure_probability))
    )


def standard_normal_maxima(
    counts: Iterable[int],
    *,
    seed: int,
) -> dict[int, float]:
    """Draw one independent standard-normal vector for each requested count."""

    resolved = tuple(int(count) for count in counts)
    if not resolved or any(count < 1 for count in resolved):
        raise ValueError("counts must be a nonempty positive sequence")
    streams = np.random.SeedSequence(seed).spawn(len(resolved))
    maxima = {}
    for count, stream in zip(resolved, streams, strict=True):
        rng = np.random.default_rng(stream)
        maxima[count] = float(np.max(np.abs(rng.standard_normal(count))))
    return maxima


def rademacher_projection_trials(
    coefficients: Iterable[float],
    *,
    trials: int,
    seed: int,
    chunk_size: int = 2048,
) -> np.ndarray:
    """Sample sums ``sum_j coefficients[j] * epsilon[j]`` with signs ±1."""

    weights = np.asarray(tuple(coefficients), dtype=np.float64)
    if weights.ndim != 1 or weights.size == 0:
        raise ValueError("coefficients must be a nonempty one-dimensional sequence")
    if trials < 1 or chunk_size < 1:
        raise ValueError("trials and chunk_size must be positive")
    rng = np.random.default_rng(seed)
    samples = np.empty(trials, dtype=np.float64)
    for start in range(0, trials, chunk_size):
        stop = min(start + chunk_size, trials)
        bits = rng.integers(
            0,
            2,
            size=(stop - start, weights.size),
            dtype=np.int8,
        )
        signs = 2 * bits - 1
        samples[start:stop] = signs @ weights
    return samples


def empirical_tail_profile(
    samples: Iterable[float],
    thresholds: Iterable[float],
) -> dict[float, float]:
    """Estimate two-sided tail probabilities with denominator ``len(samples)``."""

    values = np.asarray(tuple(samples), dtype=np.float64)
    levels = np.asarray(tuple(thresholds), dtype=np.float64)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("samples must be a nonempty one-dimensional sequence")
    if levels.ndim != 1 or levels.size == 0 or np.any(levels < 0):
        raise ValueError("thresholds must be a nonempty nonnegative sequence")
    magnitudes = np.abs(values)
    return {
        float(level): float(np.mean(magnitudes >= level))
        for level in levels
    }


def moment_growth_profile(
    samples: Iterable[float],
    orders: Iterable[int],
) -> dict[int, float]:
    """Estimate ``||X||_p / sqrt(p)`` for declared positive moment orders."""

    values = np.asarray(tuple(samples), dtype=np.float64)
    resolved_orders = tuple(int(order) for order in orders)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("samples must be a nonempty one-dimensional sequence")
    if not resolved_orders or any(order < 1 for order in resolved_orders):
        raise ValueError("orders must be a nonempty positive sequence")
    magnitudes = np.abs(values)
    return {
        order: float(np.mean(magnitudes**order) ** (1.0 / order) / np.sqrt(order))
        for order in resolved_orders
    }


def centered_chi_square_log_mgf(
    parameters: Iterable[float],
) -> dict[float, float]:
    """Evaluate ``log E exp(lambda * (Z**2 - 1))`` for ``lambda < 1/2``."""

    values = np.asarray(tuple(parameters), dtype=np.float64)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("parameters must be a nonempty one-dimensional sequence")
    if np.any(values >= 0.5):
        raise ValueError("the centered chi-square MGF is finite only below 1/2")
    log_mgf = -values - 0.5 * np.log1p(-2.0 * values)
    return {
        float(parameter): float(result)
        for parameter, result in zip(values, log_mgf, strict=True)
    }


def centered_chi_square_upper_tail(
    thresholds: Iterable[float],
) -> dict[float, float]:
    """Return exact ``P(Z**2 - 1 >= t)`` for a standard normal ``Z``."""

    levels = np.asarray(tuple(thresholds), dtype=np.float64)
    if levels.ndim != 1 or levels.size == 0 or np.any(levels < -1.0):
        raise ValueError("thresholds must be a nonempty sequence bounded below by -1")
    return {
        float(level): float(erfc(sqrt((float(level) + 1.0) / 2.0)))
        for level in levels
    }


def centered_chi_square_sum_upper_tail(
    terms: int,
    thresholds: Iterable[float],
) -> dict[float, float]:
    """Return exact upper tails for ``sum_i (Z_i**2 - 1)`` with even ``terms``."""

    if terms < 2 or terms % 2:
        raise ValueError("terms must be a positive even integer")
    levels = np.asarray(tuple(thresholds), dtype=np.float64)
    if levels.ndim != 1 or levels.size == 0 or np.any(levels < -terms):
        raise ValueError(
            "thresholds must be a nonempty sequence bounded below by -terms"
        )

    order = terms // 2
    probabilities = {}
    for level in levels:
        half_argument = (terms + float(level)) / 2.0
        series = sum(
            half_argument**index / factorial(index)
            for index in range(order)
        )
        probabilities[float(level)] = float(exp(-half_argument) * series)
    return probabilities


def centered_chi_square_sum_trials(
    terms: int,
    *,
    trials: int,
    seed: int,
    chunk_size: int = 4096,
) -> np.ndarray:
    """Sample independent centered chi-square sums without materializing all draws."""

    if terms < 1 or trials < 1 or chunk_size < 1:
        raise ValueError("terms, trials, and chunk_size must be positive")
    rng = np.random.default_rng(seed)
    samples = np.empty(trials, dtype=np.float64)
    for start in range(0, trials, chunk_size):
        stop = min(start + chunk_size, trials)
        normals = rng.standard_normal((stop - start, terms))
        samples[start:stop] = np.sum(normals * normals - 1.0, axis=1)
    return samples


def bernstein_two_regime_rate(
    thresholds: Iterable[float],
    *,
    quadratic_scale: float,
    linear_scale: float,
) -> dict[float, float]:
    """Return ``min(t**2 / quadratic_scale, t / linear_scale)``."""

    levels = np.asarray(tuple(thresholds), dtype=np.float64)
    if levels.ndim != 1 or levels.size == 0 or np.any(levels < 0):
        raise ValueError("thresholds must be a nonempty nonnegative sequence")
    if quadratic_scale <= 0 or linear_scale <= 0:
        raise ValueError("quadratic_scale and linear_scale must be positive")
    rates = np.minimum(
        levels * levels / quadratic_scale,
        levels / linear_scale,
    )
    return {
        float(level): float(rate)
        for level, rate in zip(levels, rates, strict=True)
    }


def centered_pareto_clip_bias(
    shape: float,
    thresholds: Iterable[float],
    *,
    scale: float = 1.0,
) -> dict[float, float]:
    """Return exact mean bias after symmetric clipping of a centered Pareto variable."""

    if shape <= 1 or scale <= 0:
        raise ValueError("shape must exceed one and scale must be positive")
    levels = np.asarray(tuple(thresholds), dtype=np.float64)
    lower_extent = scale / (shape - 1.0)
    if (
        levels.ndim != 1
        or levels.size == 0
        or np.any(levels < lower_extent)
    ):
        raise ValueError(
            "thresholds must be nonempty and at least the centered lower extent"
        )
    mean = shape * scale / (shape - 1.0)
    return {
        float(level): float(
            -(scale**shape)
            * (mean + float(level)) ** (1.0 - shape)
            / (shape - 1.0)
        )
        for level in levels
    }

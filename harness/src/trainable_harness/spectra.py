"""Random-operator diagnostics introduced with C08."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SpectrumSummary:
    """Exact small-matrix singular-value diagnostics."""

    rows: int
    columns: int
    singular_values: tuple[float, ...]
    sigma_max: float
    sigma_min: float
    frobenius_norm: float
    condition_number: float
    mean_squared_stretch: float


@dataclass(frozen=True)
class PowerIterationResult:
    """One-sided spectral-norm estimates and the final input direction."""

    estimates: tuple[float, ...]
    vector: tuple[float, ...]


@dataclass(frozen=True)
class MarchenkoPasturSupport:
    """Support and zero-atom contract for an n-by-n sample covariance ESD."""

    aspect_ratio: float
    variance: float
    lambda_minus: float
    lambda_plus: float
    zero_atom: float


def _matrix(values: Iterable[Iterable[float]]) -> np.ndarray:
    resolved = np.asarray(tuple(tuple(row) for row in values), dtype=np.float64)
    if resolved.ndim != 2 or min(resolved.shape) < 1:
        raise ValueError("matrix must be nonempty and two-dimensional")
    if resolved.shape[0] < resolved.shape[1]:
        raise ValueError("the declared input-space lower edge requires rows >= columns")
    return resolved


def matrix_spectrum_summary(
    matrix: Iterable[Iterable[float]],
) -> SpectrumSummary:
    """Return an exact SVD summary for a square or tall real matrix."""

    resolved = _matrix(matrix)
    singular_values = np.linalg.svd(resolved, compute_uv=False)
    largest = float(singular_values[0])
    smallest = float(singular_values[-1])
    frobenius = float(np.linalg.norm(resolved, ord="fro"))
    condition = float(np.inf if smallest == 0.0 else largest / smallest)
    return SpectrumSummary(
        rows=int(resolved.shape[0]),
        columns=int(resolved.shape[1]),
        singular_values=tuple(float(value) for value in singular_values),
        sigma_max=largest,
        sigma_min=smallest,
        frobenius_norm=frobenius,
        condition_number=condition,
        mean_squared_stretch=float(frobenius**2 / resolved.shape[1]),
    )


def gaussian_singular_value_trials(
    rows: int,
    columns: int,
    *,
    trials: int,
    seed: int,
    scaled: bool = True,
) -> dict[str, np.ndarray]:
    """Sample Gaussian matrices and return exact edge and fixed-direction diagnostics."""

    if rows < columns or columns < 1:
        raise ValueError("dimensions must satisfy rows >= columns >= 1")
    if trials < 1:
        raise ValueError("trials must be positive")
    rng = np.random.default_rng(seed)
    normalizer = np.sqrt(rows) if scaled else 1.0
    largest = np.empty(trials, dtype=np.float64)
    smallest = np.empty(trials, dtype=np.float64)
    mean_squared = np.empty(trials, dtype=np.float64)
    fixed_stretch = np.empty(trials, dtype=np.float64)
    for index in range(trials):
        matrix = rng.standard_normal((rows, columns)) / normalizer
        singular_values = np.linalg.svd(matrix, compute_uv=False)
        largest[index] = singular_values[0]
        smallest[index] = singular_values[-1]
        mean_squared[index] = np.sum(matrix * matrix) / columns
        fixed_stretch[index] = np.linalg.norm(matrix[:, 0])
    return {
        "sigma_max": largest,
        "sigma_min": smallest,
        "mean_squared_stretch": mean_squared,
        "fixed_direction_stretch": fixed_stretch,
    }


def power_iteration_spectral_norm(
    matrix: Iterable[Iterable[float]],
    *,
    iterations: int,
    seed: int,
) -> PowerIterationResult:
    """Estimate only the largest singular value through power iteration on A.T @ A."""

    resolved = _matrix(matrix)
    if iterations < 1:
        raise ValueError("iterations must be positive")
    rng = np.random.default_rng(seed)
    vector = rng.standard_normal(resolved.shape[1])
    vector /= np.linalg.norm(vector)
    estimates = []
    for _ in range(iterations):
        image = resolved @ vector
        estimates.append(float(np.linalg.norm(image)))
        pullback = resolved.T @ image
        norm = float(np.linalg.norm(pullback))
        if norm == 0.0:
            raise ValueError("power iteration is undefined for the zero map")
        vector = pullback / norm
    return PowerIterationResult(
        estimates=tuple(estimates),
        vector=tuple(float(value) for value in vector),
    )


def _sample_matrix(values: Iterable[Iterable[float]]) -> np.ndarray:
    resolved = np.asarray(tuple(tuple(row) for row in values), dtype=np.float64)
    if resolved.ndim != 2 or min(resolved.shape) < 1:
        raise ValueError("samples must be a nonempty two-dimensional array")
    if not np.all(np.isfinite(resolved)):
        raise ValueError("samples must be finite")
    return resolved


def sample_covariance(
    samples: Iterable[Iterable[float]],
    *,
    center: bool = False,
    denominator: str = "samples",
) -> np.ndarray:
    """Return a covariance or second-moment matrix under an explicit estimator contract.

    Rows are observations and columns are coordinates. With ``center=False``,
    the population mean is treated as known zero and the denominator must be
    the sample count. With ``center=True``, ``denominator='unbiased'`` selects
    the sample-count-minus-one convention.
    """

    resolved = _sample_matrix(samples)
    count = resolved.shape[0]
    if denominator not in {"samples", "unbiased"}:
        raise ValueError("denominator must be 'samples' or 'unbiased'")
    if denominator == "unbiased" and not center:
        raise ValueError("the unbiased denominator requires sample centering")
    if center:
        resolved = resolved - np.mean(resolved, axis=0, keepdims=True)
    divisor = count if denominator == "samples" else count - 1
    if divisor <= 0:
        raise ValueError("the declared denominator must be positive")
    return (resolved.T @ resolved) / divisor


def covariance_eigenvalues(
    samples: Iterable[Iterable[float]],
    *,
    center: bool = False,
    denominator: str = "samples",
) -> np.ndarray:
    """Return ascending eigenvalues under the same explicit covariance contract."""

    covariance = sample_covariance(
        samples,
        center=center,
        denominator=denominator,
    )
    return np.linalg.eigvalsh(covariance)


def marchenko_pastur_support(
    aspect_ratio: float,
    *,
    variance: float = 1.0,
) -> MarchenkoPasturSupport:
    """Return the asymptotic support for gamma = features / samples."""

    gamma = float(aspect_ratio)
    scale = float(variance)
    if not np.isfinite(gamma) or gamma <= 0.0:
        raise ValueError("aspect_ratio must be finite and positive")
    if not np.isfinite(scale) or scale <= 0.0:
        raise ValueError("variance must be finite and positive")
    root = np.sqrt(gamma)
    return MarchenkoPasturSupport(
        aspect_ratio=gamma,
        variance=scale,
        lambda_minus=float(scale * (1.0 - root) ** 2),
        lambda_plus=float(scale * (1.0 + root) ** 2),
        zero_atom=float(max(0.0, 1.0 - 1.0 / gamma)),
    )


def marchenko_pastur_density(
    points: Iterable[float],
    aspect_ratio: float,
    *,
    variance: float = 1.0,
) -> np.ndarray:
    """Evaluate the continuous part of the Marchenko--Pastur density."""

    support = marchenko_pastur_support(
        aspect_ratio,
        variance=variance,
    )
    resolved = np.asarray(tuple(points), dtype=np.float64)
    if resolved.ndim != 1:
        raise ValueError("points must be one-dimensional")
    density = np.zeros_like(resolved)
    interior = (
        (resolved > support.lambda_minus)
        & (resolved < support.lambda_plus)
        & (resolved > 0.0)
    )
    numerator = np.sqrt(
        (support.lambda_plus - resolved[interior])
        * (resolved[interior] - support.lambda_minus)
    )
    density[interior] = numerator / (
        2.0
        * np.pi
        * support.aspect_ratio
        * support.variance
        * resolved[interior]
    )
    return density


def gaussian_covariance_trials(
    samples: int,
    features: int,
    *,
    trials: int,
    seed: int,
    population_spike: float = 1.0,
) -> dict[str, np.ndarray]:
    """Return exact covariance-spectrum summaries for a rank-one Gaussian model."""

    if samples < 1 or features < 1 or trials < 1:
        raise ValueError("samples, features, and trials must be positive")
    spike = float(population_spike)
    if not np.isfinite(spike) or spike <= 0.0:
        raise ValueError("population_spike must be finite and positive")
    rng = np.random.default_rng(seed)
    smallest = np.empty(trials, dtype=np.float64)
    largest = np.empty(trials, dtype=np.float64)
    mean = np.empty(trials, dtype=np.float64)
    for index in range(trials):
        data = rng.standard_normal((samples, features))
        data[:, 0] *= np.sqrt(spike)
        eigenvalues = covariance_eigenvalues(data)
        smallest[index] = eigenvalues[0]
        largest[index] = eigenvalues[-1]
        mean[index] = np.mean(eigenvalues)
    return {
        "lambda_min": smallest,
        "lambda_max": largest,
        "mean_eigenvalue": mean,
    }


def empirical_upper_threshold(
    null_statistics: Iterable[float],
    *,
    false_positive_rate: float,
) -> float:
    """Return a declared linear empirical upper quantile for a null statistic."""

    resolved = np.asarray(tuple(null_statistics), dtype=np.float64)
    alpha = float(false_positive_rate)
    if resolved.ndim != 1 or resolved.size < 2:
        raise ValueError("null_statistics must contain at least two values")
    if not np.all(np.isfinite(resolved)):
        raise ValueError("null_statistics must be finite")
    if not 0.0 < alpha < 1.0:
        raise ValueError("false_positive_rate must lie strictly between zero and one")
    return float(np.quantile(resolved, 1.0 - alpha, method="linear"))

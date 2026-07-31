"""Stable and mergeable moment calculations for C02."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import platform
import sys
from typing import Any, Iterable

import numpy as np


@dataclass(frozen=True)
class MomentState:
    """State for a count, mean, and centered sum of squares."""

    count: int
    mean: float
    m2: float
    dtype: str
    method: str

    @property
    def population_variance(self) -> float:
        """Return M2/n, or NaN for an empty state."""

        if self.count == 0:
            return float("nan")
        return self.m2 / self.count

    @property
    def sample_variance(self) -> float:
        """Return M2/(n-1), or NaN when fewer than two values exist."""

        if self.count < 2:
            return float("nan")
        return self.m2 / (self.count - 1)

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable state record."""

        record = asdict(self)
        record["population_variance"] = self.population_variance
        record["sample_variance"] = self.sample_variance
        return record


def observation_ledger(*, seed: int, dtype: Any, device: str = "cpu") -> dict[str, Any]:
    """Record the environment fields that make a local witness interpretable."""

    resolved = np.dtype(dtype)
    return {
        "seed": int(seed),
        "device": device,
        "dtype": resolved.name,
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "numpy": np.__version__,
        "platform": platform.platform(),
        "byteorder": sys.byteorder,
    }


def _as_1d(values: Iterable[float], dtype: Any) -> tuple[np.ndarray, np.dtype]:
    resolved = np.dtype(dtype)
    array = np.asarray(values, dtype=resolved)
    if array.ndim != 1:
        raise ValueError(f"expected a one-dimensional stream, got shape {array.shape}")
    return array, resolved


def naive_moments(values: Iterable[float], *, dtype: Any = np.float32) -> MomentState:
    """Compute moments through E[X^2] - E[X]^2 in the declared dtype."""

    array, resolved = _as_1d(values, dtype)
    count = int(array.size)
    if count == 0:
        return MomentState(0, float("nan"), float("nan"), resolved.name, "naive")

    scalar = resolved.type
    n_value = scalar(count)
    total = np.sum(array, dtype=resolved)
    squares = np.multiply(array, array, dtype=resolved)
    total_squares = np.sum(squares, dtype=resolved)
    mean = scalar(total / n_value)
    variance = scalar(total_squares / n_value - mean * mean)
    m2 = scalar(variance * n_value)
    return MomentState(count, float(mean), float(m2), resolved.name, "naive")


def stable_online_moments(
    values: Iterable[float], *, dtype: Any = np.float32
) -> MomentState:
    """Compute Welford's centered state in one pass and bounded memory."""

    array, resolved = _as_1d(values, dtype)
    scalar = resolved.type
    count = 0
    mean = scalar(0)
    m2 = scalar(0)

    for value in array:
        count += 1
        delta = scalar(value - mean)
        mean = scalar(mean + delta / scalar(count))
        delta_after = scalar(value - mean)
        m2 = scalar(m2 + delta * delta_after)

    if count == 0:
        return MomentState(0, float("nan"), float("nan"), resolved.name, "welford")
    return MomentState(count, float(mean), float(m2), resolved.name, "welford")


def merge_moments(left: MomentState, right: MomentState) -> MomentState:
    """Merge two disjoint centered states with the pairwise correction."""

    if left.dtype != right.dtype:
        raise ValueError(f"dtype mismatch: {left.dtype!r} != {right.dtype!r}")
    if left.count == 0:
        return right
    if right.count == 0:
        return left

    resolved = np.dtype(left.dtype)
    scalar = resolved.type
    total_count = left.count + right.count
    delta = scalar(right.mean - left.mean)
    mean = scalar(left.mean + delta * scalar(right.count) / scalar(total_count))
    correction = scalar(
        delta
        * delta
        * scalar(left.count)
        * scalar(right.count)
        / scalar(total_count)
    )
    m2 = scalar(left.m2 + right.m2 + correction)
    return MomentState(total_count, float(mean), float(m2), resolved.name, "merged")


def comparison_audit(
    values: Iterable[float], *, dtype: Any = np.float32
) -> dict[str, Any]:
    """Compare naïve, two-pass, and online variance on the represented inputs."""

    array, resolved = _as_1d(values, dtype)
    if array.size == 0:
        raise ValueError("comparison audit requires at least one value")

    naive = naive_moments(array, dtype=resolved)
    online = stable_online_moments(array, dtype=resolved)
    mean = np.mean(array, dtype=resolved)
    centered = np.subtract(array, mean, dtype=resolved)
    two_pass_variance = float(
        np.mean(np.multiply(centered, centered, dtype=resolved), dtype=resolved)
    )
    reference_variance = float(np.var(array.astype(np.float64), dtype=np.float64))

    def error(value: float) -> float:
        return abs(value - reference_variance) / reference_variance

    return {
        "count": int(array.size),
        "dtype": resolved.name,
        "reference": {
            "dtype": "float64",
            "population_variance": reference_variance,
            "input_contract": "same represented inputs promoted to float64",
        },
        "naive": {
            **naive.as_dict(),
            "relative_error": error(naive.population_variance),
        },
        "two_pass": {
            "population_variance": two_pass_variance,
            "relative_error": error(two_pass_variance),
        },
        "welford": {
            **online.as_dict(),
            "relative_error": error(online.population_variance),
        },
    }

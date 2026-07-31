"""Finite-grid diagnostics introduced with C03."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

import numpy as np


@dataclass(frozen=True)
class UpdateTrace:
    """Exact requested and stored trajectories for a repeated scalar update."""

    initial: float
    increment: float
    steps: int
    dtype: str
    exact: np.ndarray
    stored: np.ndarray

    @property
    def final(self) -> float:
        return float(self.stored[-1])

    @property
    def exact_final(self) -> float:
        return float(self.exact[-1])

    @property
    def changed_steps(self) -> int:
        return int(np.count_nonzero(np.diff(self.stored)))


@dataclass(frozen=True)
class QuantizationResult:
    """Dequantized values and the explicit symmetric scale contract."""

    values: np.ndarray
    dequantized: np.ndarray
    integer_codes: np.ndarray
    scales: np.ndarray
    bits: int
    block_size: int

    @property
    def absolute_error(self) -> np.ndarray:
        return np.abs(self.dequantized - self.values)


def float_contract(dtype: Any) -> dict[str, float | int | str]:
    """Return the range and resolution fields for one NumPy binary format."""

    resolved = np.dtype(dtype)
    if resolved.kind != "f":
        raise TypeError(f"expected a floating dtype, got {resolved.name}")
    info = np.finfo(resolved)
    scalar = resolved.type
    smallest_subnormal = np.nextafter(scalar(0), scalar(1), dtype=resolved)
    return {
        "dtype": resolved.name,
        "bits": int(info.bits),
        "significand_bits": int(info.nmant + 1),
        "fraction_bits": int(info.nmant),
        "exponent_bits": int(info.iexp),
        "epsilon": float(info.eps),
        "unit_roundoff": float(info.eps / 2),
        "smallest_normal": float(info.tiny),
        "smallest_subnormal": float(smallest_subnormal),
        "largest_finite": float(info.max),
    }


def local_spacing(value: float, *, dtype: Any) -> float:
    """Return the absolute gap from the represented value to its next neighbor."""

    resolved = np.dtype(dtype)
    scalar = resolved.type
    represented = scalar(value)
    if not np.isfinite(represented):
        raise ValueError("local spacing requires a finite represented value")
    return float(abs(np.spacing(represented)))


def repeated_update(
    initial: float,
    increment: float,
    steps: int,
    *,
    dtype: Any,
) -> UpdateTrace:
    """Round a scalar back to ``dtype`` after every requested update."""

    if steps < 0:
        raise ValueError("steps must be nonnegative")
    resolved = np.dtype(dtype)
    scalar = resolved.type
    stored = np.empty(steps + 1, dtype=resolved)
    exact = np.empty(steps + 1, dtype=np.float64)
    stored[0] = scalar(initial)
    exact[0] = float(initial)
    for index in range(1, steps + 1):
        exact[index] = exact[index - 1] + float(increment)
        stored[index] = scalar(float(stored[index - 1]) + float(increment))
    return UpdateTrace(
        initial=float(initial),
        increment=float(increment),
        steps=int(steps),
        dtype=resolved.name,
        exact=exact,
        stored=stored,
    )


def _stochastic_round(
    values: np.ndarray, *, dtype: np.dtype, rng: np.random.Generator
) -> np.ndarray:
    """Round real values to adjacent points with distance-proportional odds."""

    nearest = values.astype(dtype)
    nearest_wide = nearest.astype(np.float64)
    lower = np.where(
        nearest_wide <= values,
        nearest_wide,
        np.nextafter(nearest, dtype.type(-np.inf), dtype=dtype).astype(np.float64),
    )
    upper = np.where(
        nearest_wide >= values,
        nearest_wide,
        np.nextafter(nearest, dtype.type(np.inf), dtype=dtype).astype(np.float64),
    )
    width = upper - lower
    probability_up = np.divide(
        values - lower,
        width,
        out=np.zeros_like(values, dtype=np.float64),
        where=width > 0,
    )
    rounded = np.where(rng.random(values.shape) < probability_up, upper, lower)
    return rounded.astype(dtype)


def stochastic_update_trials(
    initial: float,
    increment: float,
    steps: int,
    trials: int,
    *,
    dtype: Any,
    seed: int,
) -> np.ndarray:
    """Return endpoints from repeated updates with stochastic adjacent rounding."""

    if steps < 0 or trials < 1:
        raise ValueError("steps must be nonnegative and trials must be positive")
    resolved = np.dtype(dtype)
    rng = np.random.default_rng(seed)
    states = np.full(trials, initial, dtype=resolved)
    for _ in range(steps):
        requested = states.astype(np.float64) + float(increment)
        states = _stochastic_round(requested, dtype=resolved, rng=rng)
    return states


def symmetric_quantize(
    values: Iterable[float],
    *,
    bits: int,
    block_size: int | None = None,
) -> QuantizationResult:
    """Quantize with one symmetric scale per declared contiguous block."""

    if bits < 2:
        raise ValueError("bits must be at least two")
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 1 or array.size == 0:
        raise ValueError("values must be a nonempty one-dimensional array")
    if block_size is None:
        block_size = int(array.size)
    if block_size < 1:
        raise ValueError("block_size must be positive")

    qmax = 2 ** (bits - 1) - 1
    codes = np.empty(array.size, dtype=np.int64)
    dequantized = np.empty_like(array)
    scales = []
    for start in range(0, array.size, block_size):
        stop = min(start + block_size, array.size)
        block = array[start:stop]
        maximum = float(np.max(np.abs(block)))
        scale = maximum / qmax if maximum else 1.0
        block_codes = np.clip(np.rint(block / scale), -qmax, qmax).astype(np.int64)
        codes[start:stop] = block_codes
        dequantized[start:stop] = block_codes * scale
        scales.append(scale)
    return QuantizationResult(
        values=array,
        dequantized=dequantized,
        integer_codes=codes,
        scales=np.asarray(scales),
        bits=int(bits),
        block_size=int(block_size),
    )

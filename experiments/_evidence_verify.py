"""Compare regenerated evidence with a committed claim without rewriting it."""

from __future__ import annotations

import json
import math
from numbers import Real
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "artifacts" / "claims"
IGNORED_TOP_LEVEL_FIELDS = {"environment", "payload_sha256"}


def _compare(
    observed: Any,
    expected: Any,
    *,
    path: str,
    absolute_tolerance: float,
    deviations: list[tuple[float, str]],
) -> None:
    if isinstance(expected, dict):
        if not isinstance(observed, dict):
            raise AssertionError(f"{path}: expected an object")
        expected_keys = set(expected)
        observed_keys = set(observed)
        if path == "$":
            expected_keys -= IGNORED_TOP_LEVEL_FIELDS
            observed_keys -= IGNORED_TOP_LEVEL_FIELDS
        if observed_keys != expected_keys:
            raise AssertionError(
                f"{path}: key mismatch; observed={sorted(observed_keys)}, "
                f"expected={sorted(expected_keys)}"
            )
        for key in sorted(expected_keys):
            _compare(
                observed[key],
                expected[key],
                path=f"{path}.{key}",
                absolute_tolerance=absolute_tolerance,
                deviations=deviations,
            )
        return

    if isinstance(expected, list):
        if not isinstance(observed, (list, tuple)):
            raise AssertionError(f"{path}: expected a sequence")
        if len(observed) != len(expected):
            raise AssertionError(
                f"{path}: length mismatch {len(observed)} != {len(expected)}"
            )
        for index, (observed_item, expected_item) in enumerate(
            zip(observed, expected, strict=True)
        ):
            _compare(
                observed_item,
                expected_item,
                path=f"{path}[{index}]",
                absolute_tolerance=absolute_tolerance,
                deviations=deviations,
            )
        return

    numeric_pair = (
        isinstance(expected, Real)
        and not isinstance(expected, bool)
        and isinstance(observed, Real)
        and not isinstance(observed, bool)
    )
    if numeric_pair and (isinstance(expected, float) or isinstance(observed, float)):
        observed_float = float(observed)
        expected_float = float(expected)
        if math.isnan(observed_float) and math.isnan(expected_float):
            return
        deviation = abs(observed_float - expected_float)
        deviations.append((deviation, path))
        if deviation > absolute_tolerance:
            raise AssertionError(
                f"{path}: absolute deviation {deviation:.17g} exceeds "
                f"declared tolerance {absolute_tolerance:.17g}; "
                f"observed={observed_float:.17g}, expected={expected_float:.17g}"
            )
        return

    if observed != expected:
        raise AssertionError(f"{path}: observed={observed!r}, expected={expected!r}")


def verify_claim(
    filename: str,
    observed: dict[str, Any],
    *,
    absolute_tolerance: float,
) -> None:
    """Verify a regenerated payload; environment metadata is informational."""
    expected = json.loads((CLAIMS / filename).read_text())
    deviations: list[tuple[float, str]] = []
    _compare(
        observed,
        expected,
        path="$",
        absolute_tolerance=absolute_tolerance,
        deviations=deviations,
    )
    maximum, maximum_path = max(deviations, default=(0.0, "$"))
    if maximum == 0.0:
        print(f"{filename}: exact match")
    else:
        print(
            f"{filename}: max_abs_deviation={maximum:.3e} "
            f"at {maximum_path} (gate={absolute_tolerance:.1e})"
        )

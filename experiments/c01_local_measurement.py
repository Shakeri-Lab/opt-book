"""Re-run the C01 local timing protocol without rewriting its observation."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = json.loads(
    (ROOT / "artifacts/claims/c01-local-measurement-001.json").read_text()
)


def median_seconds(operation, *, warmups: int, repetitions: int) -> float:
    for _ in range(warmups):
        operation()
    samples = []
    for _ in range(repetitions):
        start = time.perf_counter_ns()
        operation()
        samples.append((time.perf_counter_ns() - start) * 1e-9)
    return float(np.median(samples))


copy_rates = {}
for mib in (16, 64, 128):
    count = mib * 1024 * 1024 // 4
    source = np.arange(count, dtype=np.float32)
    destination = np.empty_like(source)
    elapsed = median_seconds(
        lambda: np.copyto(destination, source),
        warmups=5,
        repetitions=15,
    )
    copy_rates[str(mib)] = 8 * count / elapsed / 1e9

matmul_rates = {}
for order in (256, 512, 1024):
    seed = int(
        sha256(f"c01-matmul-{order}".encode()).hexdigest()[:8], 16
    )
    rng = np.random.default_rng(seed)
    left = rng.normal(size=(order, order)).astype(np.float32)
    right = rng.normal(size=(order, order)).astype(np.float32)
    elapsed = median_seconds(
        lambda: left @ right,
        warmups=3,
        repetitions=10,
    )
    matmul_rates[str(order)] = 2 * order**3 / elapsed / 1e9

# Timing is device- and library-specific. The artifact is a pinned observation;
# this executable re-runs the protocol and verifies positivity plus the
# artifact's own count/rate arithmetic without imposing a cross-device speed
# threshold.
ratios = []
for family, observed in (
    ("copy_by_mib", copy_rates),
    ("matmul_by_order", matmul_rates),
):
    rate_field = (
        "achieved_gbyte_per_second"
        if family == "copy_by_mib"
        else "achieved_gflop_per_second"
    )
    for key, value in observed.items():
        reference = EXPECTED["result"][family][key][rate_field]
        ratios.append(value / reference)
        assert np.isfinite(value) and value > 0

for mib, record in EXPECTED["result"]["copy_by_mib"].items():
    count = int(mib) * 1024 * 1024 // 4
    derived = 8 * count / record["median_seconds"] / 1e9
    assert np.isclose(derived, record["achieved_gbyte_per_second"])
for order, record in EXPECTED["result"]["matmul_by_order"].items():
    derived = 2 * int(order) ** 3 / record["median_seconds"] / 1e9
    assert np.isclose(derived, record["achieved_gflop_per_second"])

assert copy_rates["64"] > 0
assert matmul_rates["512"] > 0
print(
    "c01-local-measurement-001.json: protocol re-executed; "
    f"device-scoped rate ratios={min(ratios):.3g}..{max(ratios):.3g}"
)

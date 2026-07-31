"""Generate the class-(a) claim artifacts for C02."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any

import numpy as np

from _evidence_verify import verify_claim

from trainable_harness import (
    comparison_audit,
    merge_moments,
    observation_ledger,
    stable_online_moments,
)


ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "artifacts" / "claims"
MANIFEST = ROOT / "artifacts" / "harness" / "ch-02" / "manifest.json"


def verify_generated_claim(filename: str, payload: dict[str, Any]) -> None:
    verify_claim(filename, payload, absolute_tolerance=0.0)


def left_fold(states):
    state = states[0]
    for next_state in states[1:]:
        state = merge_moments(state, next_state)
    return state


def balanced_fold(states):
    level = list(states)
    while len(level) > 1:
        level = [
            merge_moments(level[index], level[index + 1])
            if index + 1 < len(level)
            else level[index]
            for index in range(0, len(level), 2)
        ]
    return level[0]


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    wheel = MANIFEST.parent / manifest["wheel"]
    wheel_digest = sha256(wheel.read_bytes()).hexdigest()
    assert wheel_digest == manifest["wheel_sha256"]

    seed = 6210
    rng = np.random.default_rng(seed)
    values = (20_000.0 + rng.normal(size=200_000)).astype(np.float32)
    audit = comparison_audit(values, dtype=np.float32)
    assert audit["naive"]["population_variance"] < 0.0
    raw_second_moment = np.mean(values * values, dtype=np.float32)
    mean_square = np.mean(values, dtype=np.float32) ** np.float32(2)
    local_spacing = np.spacing(mean_square)
    cancellation_scale = (
        np.finfo(np.float32).eps
        / 2
        * (20_000 / audit["reference"]["population_variance"] ** 0.5) ** 2
    )

    environment = observation_ledger(seed=seed, dtype=np.float32)
    environment["machine"] = platform.machine()
    crash = {
        "schema_version": 1,
        "claim_id": "c02-variance-crash-001",
        "phenomenon_id": "c02-negative-variance",
        "chapter": "c02",
        "provenance_class": "a",
        "hypothesis": (
            "Adding a large common offset will corrupt the FP32 raw-moment "
            "variance before centered methods on the same represented inputs."
        ),
        "data_roles": {
            "development": "seeded deterministic witness",
            "sealed_endpoint": None,
        },
        "input": {
            "distribution": "offset + standard normal",
            "offset": 20000.0,
            "count": 200000,
            "seed": seed,
            "represented_dtype": "float32",
        },
        "estimator": {
            "target": "population variance of the represented FP32 values",
            "denominator": "n",
            "reduction_axis": "all 200000 scalar observations",
            "reference": "same represented inputs promoted to float64",
        },
        "environment": environment,
        "harness_ref": manifest["harness_ref"],
        "harness_wheel_sha256": wheel_digest,
        "result": {
            **audit,
            "rounding_grid": {
                "raw_second_moment": float(raw_second_moment),
                "mean_square": float(mean_square),
                "local_spacing": float(local_spacing),
                "naive_variance_in_local_ulps": (
                    audit["naive"]["population_variance"] / float(local_spacing)
                ),
                "diagnostic_scale_model": float(cancellation_scale),
            },
        },
    }
    verify_generated_claim("c02-variance-crash-001.json", crash)

    order_seed = 6211
    order_rng = np.random.default_rng(order_seed)
    order_values = (20_000.0 + order_rng.normal(size=131_072)).astype(np.float32)
    blocks = [
        stable_online_moments(block, dtype=np.float32)
        for block in np.array_split(order_values, 128)
    ]
    orders = {
        "left": left_fold(blocks),
        "right": left_fold(list(reversed(blocks))),
        "balanced": balanced_fold(blocks),
        "sequential": stable_online_moments(order_values, dtype=np.float32),
    }
    reference = float(np.var(order_values.astype(np.float64)))
    reduction = {
        "schema_version": 1,
        "claim_id": "c02-reduction-order-001",
        "phenomenon_id": "c02-negative-variance",
        "chapter": "c02",
        "provenance_class": "a",
        "hypothesis": (
            "Valid exact-arithmetic merge orders need not be bitwise identical "
            "when the same partial states are merged in FP32."
        ),
        "input": {
            "distribution": "offset + standard normal",
            "offset": 20000.0,
            "count": 131072,
            "seed": order_seed,
            "represented_dtype": "float32",
            "blocks": 128,
        },
        "estimator": {
            "target": "population variance of the represented FP32 values",
            "denominator": "n",
            "reference": "same represented inputs promoted to float64",
        },
        "environment": observation_ledger(seed=order_seed, dtype=np.float32),
        "harness_ref": manifest["harness_ref"],
        "harness_wheel_sha256": wheel_digest,
        "result": {
            "reference": reference,
            "orders": {
                name: {
                    "population_variance": state.population_variance,
                    "absolute_error": abs(state.population_variance - reference),
                }
                for name, state in orders.items()
            },
        },
    }
    verify_generated_claim("c02-reduction-order-001.json", reduction)

    print("verified c02-variance-crash-001.json")
    print("verified c02-reduction-order-001.json")


if __name__ == "__main__":
    main()

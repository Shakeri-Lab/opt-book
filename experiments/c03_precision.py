"""Generate the class-(a)/(b) claim artifacts for C03."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

import numpy as np

from trainable_harness import (
    float_contract,
    local_spacing,
    observation_ledger,
    repeated_update,
    stochastic_update_trials,
    symmetric_quantize,
)


ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "artifacts" / "claims"
MANIFEST = ROOT / "artifacts" / "harness" / "ch-03" / "manifest.json"


def payload_digest(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def write_claim(filename: str, payload: dict[str, Any]) -> None:
    payload["payload_sha256"] = payload_digest(payload)
    target = CLAIMS / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def base_record(
    *,
    claim_id: str,
    provenance_class: str,
    hypothesis: str,
    result: dict[str, Any],
    manifest: dict[str, Any],
    wheel_digest: str,
    seed: int | None,
) -> dict[str, Any]:
    environment = observation_ledger(
        seed=seed if seed is not None else 0,
        dtype=np.float16,
    )
    environment["seed_role"] = "not applicable" if seed is None else "simulation"
    return {
        "schema_version": 1,
        "claim_id": claim_id,
        "phenomenon_id": "c03-vanishing-update",
        "chapter": "c03",
        "provenance_class": provenance_class,
        "hypothesis": hypothesis,
        "environment": environment,
        "harness_ref": manifest["harness_ref"],
        "harness_wheel_sha256": wheel_digest,
        "hardware_claim_boundary": (
            "CPU simulation of a declared numerical contract; no accelerator "
            "timing or throughput conclusion."
        ),
        "result": result,
    }


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    wheel = MANIFEST.parent / manifest["wheel"]
    wheel_digest = sha256(wheel.read_bytes()).hexdigest()
    assert wheel_digest == manifest["wheel_sha256"]

    initial, increment, steps = 1024.0, 0.25, 400
    trace = repeated_update(initial, increment, steps, dtype=np.float16)
    spacing = local_spacing(initial, dtype=np.float16)
    stagnation = base_record(
        claim_id="c03-update-stagnation-001",
        provenance_class="b",
        hypothesis=(
            "Rounding an increment smaller than half the local FP16 spacing "
            "back to FP16 after each step will make the stored trajectory stall."
        ),
        result={
            "initial": initial,
            "requested_increment": increment,
            "steps": steps,
            "local_spacing": spacing,
            "half_spacing": spacing / 2,
            "exact_endpoint": trace.exact_final,
            "stored_endpoint": trace.final,
            "changed_steps": trace.changed_steps,
        },
        manifest=manifest,
        wheel_digest=wheel_digest,
        seed=None,
    )
    write_claim("c03-update-stagnation-001.json", stagnation)

    envelopes = {
        name: float_contract(dtype)
        for name, dtype in (("float16", np.float16), ("float32", np.float32))
    }
    envelope = base_record(
        claim_id="c03-format-envelope-001",
        provenance_class="a",
        hypothesis=(
            "Binary formats with different exponent and significand allocations "
            "have measurably different range and local resolution."
        ),
        result=envelopes,
        manifest=manifest,
        wheel_digest=wheel_digest,
        seed=None,
    )
    write_claim("c03-format-envelope-001.json", envelope)

    values = np.array([0.1, 0.2, 0.3, 100.0])
    global_result = symmetric_quantize(values, bits=8)
    blocked_result = symmetric_quantize(values, bits=8, block_size=3)
    grid = base_record(
        claim_id="c03-grid-collapse-001",
        provenance_class="b",
        hypothesis=(
            "A single outlier-selected symmetric scale erases small coordinates "
            "that survive when resolution is allocated by declared blocks."
        ),
        result={
            "values": values.tolist(),
            "bits": 8,
            "global": {
                "block_size": global_result.block_size,
                "scales": global_result.scales.tolist(),
                "integer_codes": global_result.integer_codes.tolist(),
                "dequantized": global_result.dequantized.tolist(),
            },
            "blocked": {
                "block_size": blocked_result.block_size,
                "scales": blocked_result.scales.tolist(),
                "integer_codes": blocked_result.integer_codes.tolist(),
                "dequantized": blocked_result.dequantized.tolist(),
            },
        },
        manifest=manifest,
        wheel_digest=wheel_digest,
        seed=None,
    )
    write_claim("c03-grid-collapse-001.json", grid)

    seed, trials = 6212, 20_000
    endpoints = stochastic_update_trials(
        initial,
        increment,
        steps,
        trials,
        dtype=np.float16,
        seed=seed,
    ).astype(np.float64)
    mean = float(endpoints.mean())
    standard_deviation = float(endpoints.std(ddof=1))
    standard_error = standard_deviation / np.sqrt(trials)
    stochastic = base_record(
        claim_id="c03-stochastic-rounding-001",
        provenance_class="b",
        hypothesis=(
            "Distance-proportional adjacent rounding removes the deterministic "
            "endpoint bias of repeated sub-grid updates in expectation."
        ),
        result={
            "initial": initial,
            "requested_increment": increment,
            "steps": steps,
            "trials": trials,
            "seed": seed,
            "exact_endpoint": initial + steps * increment,
            "endpoint_mean": mean,
            "endpoint_standard_deviation": standard_deviation,
            "endpoint_standard_error": standard_error,
            "normal_95_percent_interval_for_mean": [
                mean - 1.96 * standard_error,
                mean + 1.96 * standard_error,
            ],
            "endpoint_minimum": float(endpoints.min()),
            "endpoint_maximum": float(endpoints.max()),
        },
        manifest=manifest,
        wheel_digest=wheel_digest,
        seed=seed,
    )
    write_claim("c03-stochastic-rounding-001.json", stochastic)

    for claim_id in (
        "c03-update-stagnation-001",
        "c03-format-envelope-001",
        "c03-grid-collapse-001",
        "c03-stochastic-rounding-001",
    ):
        print(f"wrote {claim_id}.json")


if __name__ == "__main__":
    main()

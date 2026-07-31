"""Re-execute the deterministic fan-out and checkpoint witnesses for C11."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "artifacts" / "claims"
MANIFEST = ROOT / "artifacts" / "harness" / "ch-11" / "manifest.json"

manifest = json.loads(MANIFEST.read_text())
wheel = MANIFEST.parent / manifest["wheel"]
wheel_digest = sha256(wheel.read_bytes()).hexdigest()
assert wheel_digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))

from trainable_harness import (  # noqa: E402
    TapeNode,
    reverse_accumulate,
    uniform_checkpoint_cost,
)


def overwrite_shared_node(
    nodes: list[TapeNode],
    shared_index: int,
    reverse_order: tuple[int, ...],
) -> np.ndarray:
    cotangents = np.zeros(len(nodes), dtype=np.float64)
    cotangents[-1] = 1.0
    for node_index in reverse_order:
        incoming = cotangents[node_index]
        for parent_index, local_derivative in nodes[node_index].parents:
            contribution = incoming * local_derivative
            if parent_index == shared_index:
                cotangents[parent_index] = contribution
            else:
                cotangents[parent_index] += contribution
    return cotangents


def main() -> None:
    fanout = json.loads((CLAIMS / "c11-fanout-001.json").read_text())
    checkpoint = json.loads((CLAIMS / "c11-checkpoint-001.json").read_text())
    assert fanout["harness_wheel_sha256"] == wheel_digest
    assert checkpoint["harness_wheel_sha256"] == wheel_digest

    x, y = 2.0, 3.0
    tape = [
        TapeNode(x),
        TapeNode(y),
        TapeNode(x * y, ((0, y), (1, x))),
        TapeNode(x * y + x, ((2, 1.0), (0, 1.0))),
        TapeNode(x * y * y, ((2, y), (1, x * y))),
        TapeNode(
            (x * y + x) * (x * y * y),
            ((3, x * y * y), (4, x * y + x)),
        ),
    ]
    correct = reverse_accumulate(tape)
    overwrite = overwrite_shared_node(
        tape,
        shared_index=2,
        reverse_order=(5, 3, 4, 2, 1, 0),
    )
    expected_fanout = fanout["result"]
    assert [node.value for node in tape] == expected_fanout["node_values"]
    assert correct.tolist() == expected_fanout["cotangents"]
    assert correct[:2].tolist() == [
        expected_fanout["correct_leaf_gradients"]["x"],
        expected_fanout["correct_leaf_gradients"]["y"],
    ]
    assert overwrite[:2].tolist() == [
        expected_fanout["last-writer-overwrite_leaf_gradients"]["x"],
        expected_fanout["last-writer-overwrite_leaf_gradients"]["y"],
    ]

    expected_checkpoint = checkpoint["result"]
    observed_records = []
    for block_size in (1, 2, 4, 8, 16, 32, 64):
        cost = uniform_checkpoint_cost(64, block_size)
        observed_records.append(
            {
                "backward_evaluations": cost.backward_evaluations,
                "base_forward_evaluations": cost.base_forward_evaluations,
                "block_size": cost.block_size,
                "checkpoint_count": len(cost.checkpoint_indices),
                "peak_state_units": cost.peak_state_units,
                "recomputed_forward_evaluations": (
                    cost.recomputed_forward_evaluations
                ),
                "total_local_evaluations": cost.total_local_evaluations,
            }
        )
    assert observed_records == expected_checkpoint["records"]
    assert min(
        observed_records,
        key=lambda record: record["peak_state_units"],
    )["block_size"] == expected_checkpoint[
        "minimizing_block_size_among_all_integer_choices"
    ]
    print("c11 evidence: exact match")


if __name__ == "__main__":
    main()

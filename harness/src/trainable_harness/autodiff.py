"""Reverse accumulation and checkpoint bookkeeping introduced with C11."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class TapeNode:
    """A scalar tape node with parent indices and evaluated local derivatives."""

    value: float
    parents: tuple[tuple[int, float], ...] = ()


@dataclass(frozen=True)
class CheckpointCost:
    """Exact state and operation counts for a uniform chain checkpoint model."""

    depth: int
    block_size: int
    checkpoint_indices: tuple[int, ...]
    peak_state_units: int
    base_forward_evaluations: int
    recomputed_forward_evaluations: int
    backward_evaluations: int
    total_local_evaluations: int


def reverse_accumulate(
    tape: Iterable[TapeNode],
    *,
    output_index: int = -1,
    output_cotangent: float = 1.0,
) -> np.ndarray:
    """Accumulate scalar cotangents once in reverse topological order."""

    nodes = tuple(tape)
    if not nodes:
        raise ValueError("tape must be nonempty")
    resolved_output = output_index if output_index >= 0 else len(nodes) + output_index
    if not 0 <= resolved_output < len(nodes):
        raise IndexError("output_index is outside the tape")
    for node_index, node in enumerate(nodes):
        if not np.isfinite(node.value):
            raise ValueError("tape values must be finite")
        for parent_index, local_derivative in node.parents:
            if not 0 <= parent_index < node_index:
                raise ValueError("parents must precede their child in topological order")
            if not np.isfinite(local_derivative):
                raise ValueError("local derivatives must be finite")

    cotangents = np.zeros(len(nodes), dtype=np.float64)
    cotangents[resolved_output] = float(output_cotangent)
    for node_index in range(resolved_output, -1, -1):
        incoming = cotangents[node_index]
        for parent_index, local_derivative in nodes[node_index].parents:
            cotangents[parent_index] += incoming * local_derivative
    return cotangents


def uniform_checkpoint_cost(depth: int, block_size: int) -> CheckpointCost:
    """Count a store-checkpoints-then-recompute-blocks schedule for a chain."""

    if depth < 1:
        raise ValueError("depth must be positive")
    if not 1 <= block_size <= depth:
        raise ValueError("block_size must lie between one and depth")

    checkpoints = list(range(0, depth + 1, block_size))
    if checkpoints[-1] != depth:
        checkpoints.append(depth)
    segment_lengths = np.diff(checkpoints)
    peak_states = len(checkpoints) + int(np.max(segment_lengths)) - 1
    recomputed = int(np.sum(segment_lengths - 1))
    total = depth + recomputed + depth
    return CheckpointCost(
        depth=depth,
        block_size=block_size,
        checkpoint_indices=tuple(int(index) for index in checkpoints),
        peak_state_units=peak_states,
        base_forward_evaluations=depth,
        recomputed_forward_evaluations=recomputed,
        backward_evaluations=depth,
        total_local_evaluations=total,
    )

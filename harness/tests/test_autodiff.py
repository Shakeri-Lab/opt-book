from __future__ import annotations

import numpy as np

from trainable_harness import (
    TapeNode,
    reverse_accumulate,
    uniform_checkpoint_cost,
)


def test_reverse_accumulation_sums_fanout_paths() -> None:
    x, y = 2.0, 3.0
    a = x * y
    b = a + x
    c = a * y
    loss = b * c
    tape = (
        TapeNode(x),
        TapeNode(y),
        TapeNode(a, ((0, y), (1, x))),
        TapeNode(b, ((2, 1.0), (0, 1.0))),
        TapeNode(c, ((2, y), (1, a))),
        TapeNode(loss, ((3, c), (4, b))),
    )
    gradients = reverse_accumulate(tape)
    assert loss == 144.0
    assert np.array_equal(gradients[:2], np.array([144.0, 132.0]))
    assert gradients[2] == 42.0


def test_uniform_checkpoint_cost_has_exact_extremes_and_sqrt_witness() -> None:
    store_all = uniform_checkpoint_cost(64, 1)
    square_root = uniform_checkpoint_cost(64, 8)
    assert store_all.peak_state_units == 65
    assert store_all.recomputed_forward_evaluations == 0
    assert store_all.total_local_evaluations == 128
    assert square_root.checkpoint_indices == tuple(range(0, 65, 8))
    assert square_root.peak_state_units == 16
    assert square_root.recomputed_forward_evaluations == 56
    assert square_root.total_local_evaluations == 184


def test_reverse_accumulation_requires_topological_parents() -> None:
    with np.testing.assert_raises(ValueError):
        reverse_accumulate((TapeNode(1.0, ((0, 1.0),)),))

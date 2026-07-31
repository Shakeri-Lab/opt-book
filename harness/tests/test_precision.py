from __future__ import annotations

import numpy as np

from trainable_harness import (
    float_contract,
    local_spacing,
    repeated_update,
    stochastic_update_trials,
    symmetric_quantize,
)


def test_float16_contract_and_local_spacing() -> None:
    contract = float_contract(np.float16)
    assert contract["significand_bits"] == 11
    assert contract["unit_roundoff"] == 2**-11
    assert contract["smallest_normal"] == 2**-14
    assert local_spacing(1024.0, dtype=np.float16) == 1.0


def test_deterministic_subgrid_update_stagnates() -> None:
    trace = repeated_update(1024.0, 0.25, 400, dtype=np.float16)
    assert trace.final == 1024.0
    assert trace.exact_final == 1124.0
    assert trace.changed_steps == 0


def test_stochastic_update_is_unbiased_at_the_endpoint() -> None:
    endpoints = stochastic_update_trials(
        1024.0,
        0.25,
        400,
        20_000,
        dtype=np.float16,
        seed=6212,
    )
    endpoints_wide = endpoints.astype(np.float64)
    standard_error = float(endpoints_wide.std(ddof=1) / np.sqrt(endpoints.size))
    assert abs(float(endpoints_wide.mean()) - 1124.0) < 4 * standard_error


def test_global_scale_collapses_small_coordinates() -> None:
    values = np.array([0.1, 0.2, 0.3, 100.0])
    global_result = symmetric_quantize(values, bits=8)
    blocked_result = symmetric_quantize(values, bits=8, block_size=3)
    assert np.all(global_result.integer_codes[:3] == 0)
    assert np.all(blocked_result.integer_codes[:3] != 0)
    assert blocked_result.absolute_error[:3].max() < 0.002


def test_quantizer_rejects_invalid_contract() -> None:
    for kwargs in ({"bits": 1}, {"bits": 8, "block_size": 0}):
        try:
            symmetric_quantize([1.0], **kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid contract should fail: {kwargs}")

"""Verify the exact C01 two-resource model."""
from _evidence_verify import verify_claim

record = {
    "schema_version": 1, "claim_id": "c01-roofline-001", "phenomenon_id": "c01-count-not-cost", "chapter": "c01", "provenance_class": "a",
    "hypothesis": "Operation count alone does not determine a resource ceiling.",
    "hardware_claim_boundary": "Exact byte/flop model only; no wall-clock or accelerator claim.",
    "result": {"machine_balance_flop_per_byte": 20.0, "vector_affine_intensity": 2 / 8, "gemm_n": 512, "gemm_intensity": 512 / 6, "vector_ceiling_fraction": (2 / 8) / 20, "gemm_compute_bound_under_model": 512 / 6 > 20},
}
verify_claim("c01-roofline-001.json", record, absolute_tolerance=0.0)

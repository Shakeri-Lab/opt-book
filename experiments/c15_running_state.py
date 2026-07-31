"""Verify the C15 train/evaluation statistic discrepancy."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np

from _evidence_verify import verify_claim


root = Path(__file__).resolve().parents[1]
manifest_path = root / "artifacts/harness/ch-15/manifest.json"
manifest = json.loads(manifest_path.read_text())
wheel = manifest_path.parent / manifest["wheel"]
digest = sha256(wheel.read_bytes()).hexdigest()
assert digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))
from trainable_harness import merge_moments, stable_online_moments

seed = int(sha256(b"c15-running-state").hexdigest()[:8], 16)
rng = np.random.default_rng(seed)
batches = rng.normal(4, 2, size=(8, 32))
evaluation = rng.normal(4, 2, size=32)
states = [stable_online_moments(batch, dtype=np.float64) for batch in batches]
merged = states[0]
trace = [merged]
for state in states[1:]:
    merged = merge_moments(merged, state)
    trace.append(merged)

direct = stable_online_moments(batches.ravel(), dtype=np.float64)
evaluation_state = stable_online_moments(evaluation, dtype=np.float64)
epsilon = 1e-5
train_mode = (evaluation - evaluation_state.mean) / np.sqrt(
    evaluation_state.population_variance + epsilon
)
evaluation_mode = (evaluation - merged.mean) / np.sqrt(
    merged.population_variance + epsilon
)

record = {
    "schema_version": 1,
    "claim_id": "c15-running-state-001",
    "phenomenon_id": "c15-invariance-choice",
    "chapter": "c15",
    "provenance_class": "a",
    "hypothesis": "Train-mode batch statistics and evaluation-mode running statistics can disagree under one unchanged population because they are different finite estimators.",
    "hardware_claim_boundary": "Seeded float64 CPU estimator witness with one scalar coordinate; not a claim about distribution shift or a particular library update rule.",
    "harness_ref": "ch-15",
    "harness_wheel_sha256": digest,
    "result": {
        "seed": seed,
        "batch_count": 8,
        "batch_size": 32,
        "population_mean": 4.0,
        "population_sd": 2.0,
        "epsilon": epsilon,
        "running_state": merged.as_dict(),
        "evaluation_batch_state": evaluation_state.as_dict(),
        "merge_vs_single_pass": {
            "mean_difference": merged.mean - direct.mean,
            "m2_difference": merged.m2 - direct.m2,
        },
        "normalized_discrepancy": {
            "maximum_absolute": float(
                np.max(np.abs(train_mode - evaluation_mode))
            ),
            "train_mode_mean": float(np.mean(train_mode)),
            "train_mode_variance": float(np.var(train_mode)),
            "eval_mode_mean": float(np.mean(evaluation_mode)),
            "eval_mode_variance": float(np.var(evaluation_mode)),
        },
        "running_mean_by_batch": [state.mean for state in trace],
        "running_variance_by_batch": [
            state.population_variance for state in trace
        ],
    },
}
verify_claim("c15-running-state-001.json", record, absolute_tolerance=1e-12)

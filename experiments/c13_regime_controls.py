"""Verify the C13 regime, batch, momentum, and Pareto controls."""

from hashlib import sha256
import json
from pathlib import Path
import sys

import numpy as np

from _evidence_verify import verify_claim


root = Path(__file__).resolve().parents[1]
manifest_path = root / "artifacts/harness/ch-13/manifest.json"
manifest = json.loads(manifest_path.read_text())
wheel = manifest_path.parent / manifest["wheel"]
digest = sha256(wheel.read_bytes()).hexdigest()
assert digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))

from trainable_harness import centered_pareto_clip_bias


def derived_seed(label: str) -> int:
    return int(sha256(label.encode()).hexdigest()[:8], 16)


online_seed = derived_seed("c13-online-regime")
rng = np.random.default_rng(online_seed)
state, step_size, noise_sd, batch_size, steps = 1.0, 0.12, 0.8, 16, 80
chi, losses = [], []
for _ in range(steps):
    gradients = state + rng.normal(scale=noise_sd, size=batch_size)
    losses.append(0.5 * state**2)
    chi.append(
        float(
            gradients.var(ddof=1)
            / batch_size
            / max(state**2, 1e-30)
        )
    )
    state -= step_size * float(gradients.mean())
first_crossing = int(np.flatnonzero(np.asarray(chi) >= 1)[0])

batch_sizes = [1, 4, 16, 64]
trials = 20_000
streams = np.random.SeedSequence(
    derived_seed("c13-batch-scaling")
).spawn(len(batch_sizes))
batch_scaling = {}
for size, stream in zip(batch_sizes, streams, strict=True):
    means = np.random.default_rng(stream).normal(
        scale=noise_sd, size=(trials, size)
    ).mean(axis=1)
    batch_scaling[str(size)] = {
        "observed_variance": float(means.var(ddof=1)),
        "theory_variance": noise_sd**2 / size,
    }

beta, momentum_step, forcing_sd = 0.9, 0.5, 0.2
curvatures = np.array([0.01, 1.0])
replicates = 20_000
momentum_rng = np.random.default_rng(derived_seed("c13-momentum-noise"))
plain = np.ones((replicates, 2))
momentum = plain.copy()
velocity = np.zeros_like(momentum)
for _ in range(500):
    forcing = momentum_rng.normal(scale=forcing_sd, size=plain.shape)
    plain -= momentum_step * (curvatures * plain + forcing)
    velocity = beta * velocity + curvatures * momentum + forcing
    momentum -= momentum_step * velocity


def deterministic_loss(memory: float) -> float:
    state = np.ones(2)
    velocity = np.zeros(2)
    for _ in range(80):
        velocity = memory * velocity + curvatures * state
        state -= momentum_step * velocity
    return float(0.5 * np.sum(curvatures * state**2))


def characteristic_radius(memory: float, curvature: float) -> float:
    roots = np.roots(
        [1.0, -(1 + memory - momentum_step * curvature), memory]
    )
    return float(np.max(np.abs(roots)))


pareto_bias = centered_pareto_clip_bias(1.5, [2.0, 4.0, 16.0, 64.0])
record = {
    "schema_version": 1,
    "claim_id": "c13-regime-controls-001",
    "phenomenon_id": "c13-mean-not-regime",
    "chapter": "c13",
    "provenance_class": "a",
    "hypothesis": "A fixed stochastic quadratic crosses into a noise-dominated regime; batch averaging, momentum memory, and clipping change different parts of the estimator contract.",
    "hardware_claim_boundary": "Seeded low-dimensional CPU controls under declared additive-noise and Pareto models; not a workload-level optimizer ranking.",
    "harness_ref": "ch-13",
    "harness_wheel_sha256": digest,
    "result": {
        "online_crossing": {
            "seed": online_seed,
            "step_size": step_size,
            "per_example_noise_sd": noise_sd,
            "batch_size": batch_size,
            "steps": steps,
            "first_chi_at_least_one": first_crossing,
            "initial_chi_estimate": chi[0],
            "loss_at_crossing": losses[first_crossing],
            "final_state": state,
        },
        "batch_scaling": {
            "trials": trials,
            "per_example_variance": noise_sd**2,
            "by_batch_size": batch_scaling,
        },
        "momentum_control": {
            "step_size": momentum_step,
            "curvatures": curvatures.tolist(),
            "beta": beta,
            "exact_stability_upper_step_for_top_mode": 2 * (1 + beta),
            "characteristic_radius_by_mode": {
                "no_momentum": [
                    characteristic_radius(0.0, value)
                    for value in curvatures
                ],
                "momentum": [
                    characteristic_radius(beta, value)
                    for value in curvatures
                ],
            },
            "deterministic_loss_after_80": {
                "no_momentum": deterministic_loss(0.0),
                "momentum": deterministic_loss(beta),
            },
            "stochastic_mean_loss_after_500": {
                "no_momentum": float(
                    np.mean(0.5 * np.sum(curvatures * plain**2, axis=1))
                ),
                "momentum": float(
                    np.mean(0.5 * np.sum(curvatures * momentum**2, axis=1))
                ),
            },
        },
        "infinite_variance_clipping": {
            "pareto_shape": 1.5,
            "finite_mean": True,
            "finite_variance": False,
            "exact_bias_by_threshold": {
                str(key): value for key, value in pareto_bias.items()
            },
        },
    },
}
verify_claim("c13-regime-controls-001.json", record, absolute_tolerance=1e-12)

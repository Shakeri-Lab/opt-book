"""Pure layout helper for the Coda's six-instrument incident panel."""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np


def incident_figure(result: dict[str, Any]):
    """Render the registered incident result without hiding its controls."""

    precision = result["precision_control"]
    regime = result["regime_control"]
    curvature = result["curvature_control"]
    spectrum = result["spectrum_control"]
    normalizer = result["normalization_state_control"]

    fig, axes = plt.subplots(2, 3, figsize=(10.0, 6.2))
    axes[0, 0].bar(
        ["before", "after"],
        [result["loss_before_incident"], result["loss_after_incident"]],
        color=["#232D4B", "#9C2F2F"],
    )
    axes[0, 0].set(yscale="log", ylabel="full-data loss", title="symptom")
    axes[0, 1].bar(
        ["loss deviation", "ulp / magnitude"],
        [
            precision["maximum_relative_loss_deviation_float32_vs_float64"],
            precision["float32_spacing_at_that_scale"]
            / precision["maximum_state_or_update_magnitude"],
        ],
        color=["#232D4B", "#2E7D32"],
    )
    axes[0, 1].set(yscale="log", title="precision control")
    axes[0, 2].bar(
        ["gradient\ndiscrepancy", "target-shift\nfraction"],
        [
            regime["realized_gradient_discrepancy_ratio"],
            regime["fraction_of_discrepancy_from_engineered_target_shift"],
        ],
        color=["#9C2F2F", "#E57200"],
    )
    axes[0, 2].set(yscale="log", title="estimator control")
    axes[1, 0].bar(
        [r"$\alpha\lambda_{\max}$", "directional"],
        [
            curvature["step_times_top_curvature"],
            curvature["step_times_directional_curvature"],
        ],
        color=["#232D4B", "#2E7D32"],
    )
    axes[1, 0].axhline(2, color="#9C2F2F", linestyle="--")
    axes[1, 0].set(ylim=(0, 2.2), title="curvature control")
    locations = np.arange(4)
    axes[1, 1].bar(
        locations - 0.18,
        spectrum["incident_update_singular_values"],
        width=0.36,
        color="#9C2F2F",
        label="update",
    )
    axes[1, 1].bar(
        locations + 0.18,
        spectrum["incident_weight_singular_values"],
        width=0.36,
        color="#232D4B",
        label="weights",
    )
    axes[1, 1].set(yscale="log", title="incident spectra")
    axes[1, 1].legend(frameon=False)
    axes[1, 2].bar(
        ["mean", "variance"],
        [
            normalizer["maximum_mean_difference_from_same_batch_previous_cycle"],
            normalizer[
                "maximum_variance_difference_from_same_batch_previous_cycle"
            ],
        ],
        color=["#232D4B", "#2E7D32"],
    )
    axes[1, 2].set(ylim=(0, 1), title="repeated input state")
    for axis in axes.flat:
        axis.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    return fig

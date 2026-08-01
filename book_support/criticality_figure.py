"""Pure plotting layout for the C14 pair-geometry and width controls."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


def plot_pair_width_controls(
    pair_trace: np.ndarray,
    pair_claim: dict[str, Any],
    width_claim: dict[str, Any],
    exact_variance: Callable[[int, int], float],
):
    """Plot deterministic controls and registered finite-width checks."""
    pair_depths = np.array([1, 4, 16, 64])
    pair_rows = pair_claim["result"]["finite_width_correlation"]
    pair_means = np.array([
        pair_rows[str(depth)]["mean"] for depth in pair_depths
    ])
    pair_low = np.array([
        pair_rows[str(depth)]["quantile_10"] for depth in pair_depths
    ])
    pair_high = np.array([
        pair_rows[str(depth)]["quantile_90"] for depth in pair_depths
    ])
    points = width_claim["result"]["points"]
    ratio_grid = np.linspace(0.0, 0.25, 161)
    widths = (32, 128, 512)

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.6))
    axes[0].plot(pair_trace, color="#232D4B", label="wide-model map")
    axes[0].errorbar(
        pair_depths,
        pair_means,
        yerr=[pair_means - pair_low, pair_high - pair_means],
        fmt="o",
        color="#E57200",
        capsize=3,
        label="finite width: mean, 10--90%",
    )
    axes[0].set(
        xlabel="depth",
        ylabel="normalized correlation",
        ylim=(0.45, 1.01),
    )
    axes[0].legend(frameon=False)

    for width in widths:
        values = [
            exact_variance(width, round(ratio * width))
            for ratio in ratio_grid
        ]
        axes[1].plot(ratio_grid, values, label=fr"exact, $n={width}$")
    axes[1].plot(
        ratio_grid,
        np.expm1(5 * ratio_grid),
        "--",
        color="#9C2F2F",
        label=r"$e^{5r}-1$",
    )
    axes[1].plot(
        ratio_grid,
        5 * ratio_grid,
        ":",
        color="#6B6B6B",
        label=r"$5r$",
    )
    for width in widths:
        rows = [row for row in points if row["width"] == width]
        axes[1].scatter(
            [row["depth_over_width"] for row in rows],
            [row["sample_variance"] for row in rows],
            s=18,
        )
    axes[1].set(
        xlabel=r"depth over width, $L/n$",
        ylabel=r"variance of $q_L/q_0$",
    )
    axes[1].legend(frameon=False, fontsize=7)
    for axis in axes:
        axis.grid(alpha=0.2)
    fig.tight_layout()
    return fig

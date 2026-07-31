"""Moving-curvature gradient-descent witnesses."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class StabilityTrace:
    states: np.ndarray
    losses: np.ndarray
    top_curvatures: np.ndarray
    directional_curvatures: np.ndarray


def valley_loss_gradient_hessian(state: np.ndarray, *, attraction: float = 0.1, target: float = 3.0) -> tuple[float, np.ndarray, np.ndarray]:
    """Evaluate .5(y-x^2)^2 + .5*attraction*(x-target)^2."""
    x, y = np.asarray(state, dtype=float)
    residual = y - x**2
    loss = 0.5 * residual**2 + 0.5 * attraction * (x - target) ** 2
    gradient = np.array([-2.0 * x * residual + attraction * (x - target), residual])
    hessian = np.array([[6.0 * x**2 - 2.0 * y + attraction, -2.0 * x], [-2.0 * x, 1.0]])
    return float(loss), gradient, hessian


def moving_curvature_trace(initial: np.ndarray, step_size: float, steps: int) -> StabilityTrace:
    """Run full-batch descent and record top and gradient-direction curvature."""
    state = np.asarray(initial, dtype=float).copy()
    states, losses, tops, directions = [], [], [], []
    for _ in range(steps + 1):
        loss, gradient, hessian = valley_loss_gradient_hessian(state)
        states.append(state.copy())
        losses.append(loss)
        tops.append(float(np.linalg.eigvalsh(hessian)[-1]))
        norm = np.linalg.norm(gradient)
        directions.append(float(gradient @ hessian @ gradient / norm**2) if norm else np.nan)
        state = state - step_size * gradient
    return StabilityTrace(np.array(states), np.array(losses), np.array(tops), np.array(directions))

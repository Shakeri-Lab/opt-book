"""Audit the prerequisite route, searchable topics, and cumulative exercises."""

from __future__ import annotations

from _audit_utils import ROOT, fail_if


def main() -> None:
    errors: list[str] = []
    index = (ROOT / "index.qmd").read_text()
    on_ramp = (ROOT / "chapters" / "on-ramp.qmd").read_text()
    beyond = (ROOT / "chapters" / "beyond-this-volume.qmd").read_text()
    incident = (ROOT / "chapters" / "appendices" / "incident-card.qmd").read_text()

    for phrase in (
        "does not require a prior deep-learning course",
        "The 20–30 minute diagnostic",
        "The minimal route through *Making It Learnable*",
        "One minimal training loop",
        "You are ready for Chapter 1 when",
    ):
        if phrase not in on_ramp:
            errors.append(f"on-ramp missing {phrase!r}")
    if not (ROOT / "notebooks" / "on-ramp-training-loop.ipynb").exists():
        errors.append("on-ramp training-loop notebook is missing")

    for phrase in (
        "The route at a glance",
        "Exercise navigation",
        "Deep-Learning--Making-It-Trainable.pdf",
        "Deep-Learning--Making-It-Trainable-Screen.pdf",
    ):
        if phrase not in index:
            errors.append(f"index missing reader route {phrase!r}")

    searchable = {
        "chapters/act1/07-epsilon-nets.qmd": "Epsilon-Nets",
        "chapters/act1/09-marchenko-pastur.qmd": "Marchenko–Pastur",
        "chapters/act2/12-curvature.qmd": "Generalized Gauss–Newton",
        "chapters/act2/16-edge-of-stability.qmd": "Edge-of-Stability",
    }
    for relative, term in searchable.items():
        heading = next(
            (line for line in (ROOT / relative).read_text().splitlines()
             if line.startswith("# ")),
            "",
        )
        if term not in heading:
            errors.append(f"{relative}: searchable title omits {term}")

    for heading in (
        "Similarity-weighted aggregation and kernel geometry",
        "IO-aware exact algorithms",
        "Parallel recurrence and associativity",
        "Lazy and feature-learning regimes",
    ):
        if f"## {heading}" not in beyond:
            errors.append(f"Beyond This Volume missing {heading!r}")

    for heading in (
        "Act 0 — execution contract",
        "Act I — geometric locator",
        "Act II — causal incident",
        "Incident B is deliberately unrevealed",
    ):
        if heading not in incident:
            errors.append(f"Incident Card missing {heading!r}")
    for relative in (
        "chapters/act0/04-quadratic-modes.qmd",
        "chapters/act1/10-effective-rank.qmd",
        "chapters/act2/17-update-geometry.qmd",
    ):
        if "Act checkpoint" not in (ROOT / relative).read_text():
            errors.append(f"{relative}: cumulative Act checkpoint is missing")

    fail_if(errors)
    print("reader routes and cumulative exercises: pass")


if __name__ == "__main__":
    main()

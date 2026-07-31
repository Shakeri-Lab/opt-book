"""Require numbered Plan to Code parity for learner-visible Python cells."""

from __future__ import annotations

import re

from _audit_utils import ROOT, fail_if


CELL = re.compile(r"```\{python\}(.*?)```", flags=re.DOTALL)


def main() -> None:
    errors = []
    audited = 0
    for path in sorted((ROOT / "chapters").rglob("*.qmd")):
        text = path.read_text()
        for index, match in enumerate(CELL.finditer(text), start=1):
            code = match.group(1)
            if re.search(r"#\|\s+include:\s*false", code):
                continue
            audited += 1
            before = text[: match.start()]
            open_at = before.rfind(":::: {.plan-code}")
            close_before = before.rfind("::::")
            if open_at < 0 or close_before > open_at:
                errors.append(f"{path}: Python cell {index} is outside a plan-code panel")
                continue
            panel_prefix = before[open_at:]
            plan_match = re.search(
                r":::\s+\{\.plan\}(.*?):::", panel_prefix, flags=re.DOTALL
            )
            if not plan_match:
                errors.append(f"{path}: Python cell {index} has no plan")
                continue
            steps = re.findall(r"(?m)^\d+\.\s+", plan_match.group(1))
            markers = {int(value) for value in re.findall(r"# \[(\d+)\]", code)}
            expected = set(range(1, len(steps) + 1))
            if not steps:
                errors.append(f"{path}: Python cell {index} has an empty plan")
            elif not expected.issubset(markers):
                errors.append(
                    f"{path}: Python cell {index} markers {sorted(markers)} "
                    f"do not cover steps {sorted(expected)}"
                )
    if audited == 0:
        errors.append("no learner-visible Python cells were audited")
    fail_if(errors)
    print(f"Plan to Code: pass ({audited} cells)")


if __name__ == "__main__":
    main()

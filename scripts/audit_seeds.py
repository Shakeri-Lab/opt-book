"""Require every literal random seed to be registered deliberately."""

from __future__ import annotations

import re

from _audit_utils import ROOT, fail_if, read_yaml


def main() -> None:
    contract = read_yaml(ROOT / "contracts" / "seeds.yml")
    registered = {item["value"]: item for item in contract["literal_seeds"]}
    observed: dict[int, list[str]] = {}
    paths = [
        *sorted((ROOT / "chapters").rglob("*.qmd")),
        *sorted((ROOT / "experiments").glob("*.py")),
    ]
    for path in paths:
        for number, line in enumerate(path.read_text().splitlines(), start=1):
            if "seed" not in line.lower():
                continue
            values = [int(value) for value in re.findall(r"\b6[0-9]{3}\b", line)]
            if re.search(r"\bseed\s*=\s*0\b", line):
                values.append(0)
            for value in values:
                observed.setdefault(value, []).append(
                    f"{path.relative_to(ROOT)}:{number}"
                )

    errors = []
    for value, locations in sorted(observed.items()):
        if value not in registered:
            errors.append(f"literal seed {value} is unregistered at {locations}")
    for value, entry in registered.items():
        if value not in observed:
            errors.append(f"registered literal seed {value} has no source use")
        if len(entry.get("uses", [])) > 1 and not entry.get("reuse"):
            errors.append(f"literal seed {value} has multiple uses without reuse policy")

    fail_if(errors)
    print(f"seed registry: pass ({len(observed)} literal seeds)")


if __name__ == "__main__":
    main()

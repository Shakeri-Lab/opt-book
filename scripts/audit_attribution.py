"""Audit artifact citations and reader-visible theorem provenance."""

from __future__ import annotations

import re

from _audit_utils import ROOT, fail_if, read_yaml


BIB_ENTRY = re.compile(r"(?m)^@\w+\{([^,]+),")


def chapter_path(chapter: str):
    number = int(chapter.removeprefix("c"))
    matches = list((ROOT / "chapters").glob(f"act*/{number:02d}-*.qmd"))
    return matches[0] if len(matches) == 1 else None


def sources_section(text: str) -> str:
    match = re.search(
        r"(?ms)^## Sources and further reading(?:\s+\{[^\n]+\})?\s*$"
        r"(.*?)(?=^## Exercises(?:\s+\{[^\n]+\})?\s*$|\Z)",
        text,
    )
    return match.group(1) if match else ""


def rosetta_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or line.startswith("|:"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0] != "Primitive in this book":
            rows.append(cells)
    return rows


def main() -> None:
    errors = []
    bib_keys = BIB_ENTRY.findall((ROOT / "references.bib").read_text())
    duplicates = sorted({key for key in bib_keys if bib_keys.count(key) > 1})
    if duplicates:
        errors.append(f"duplicate bibliography keys: {duplicates}")
    bib = set(bib_keys)

    rosetta = (ROOT / "chapters" / "appendices" / "rosetta.qmd").read_text()
    rows = rosetta_rows(rosetta)
    citation_contract = read_yaml(
        ROOT / "contracts" / "rosetta-citations.yml"
    )["artifacts"]
    for artifact in citation_contract:
        name = artifact["name"]
        key = artifact["citation"]
        if key not in bib:
            errors.append(f"Rosetta artifact {name}: missing bibliography key {key}")
            continue
        matching = [row for row in rows if name in row[1]]
        if len(matching) != 1:
            errors.append(
                f"Rosetta artifact {name}: expected one standard-name row, "
                f"found {len(matching)}"
            )
        elif f"@{key}" not in " | ".join(matching[0]):
            errors.append(f"Rosetta artifact {name}: row must cite @{key}")

    theorem_contract = read_yaml(ROOT / "contracts" / "theorems.yml")
    for theorem in theorem_contract["theorems"]:
        path = chapter_path(theorem["chapter"])
        if path is None:
            errors.append(
                f"{theorem['id']}: cannot resolve chapter {theorem['chapter']}"
            )
            continue
        sources = sources_section(path.read_text())
        if not sources:
            errors.append(f"{theorem['id']}: cannot resolve reader Sources section")
            continue
        for key in theorem["source"].split(";"):
            if key in bib and f"@{key}" not in sources:
                errors.append(
                    f"{theorem['id']}: bibliographic source @{key} is absent "
                    f"from {path}'s Sources section"
                )

    fail_if(errors)
    print(
        "attribution contracts: pass "
        f"({len(citation_contract)} Rosetta artifacts; "
        f"{len(theorem_contract['theorems'])} theorems)"
    )


if __name__ == "__main__":
    main()

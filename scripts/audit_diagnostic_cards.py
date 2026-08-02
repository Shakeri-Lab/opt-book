"""Lock the two diagnostic-card schemas to every public manifestation."""

from __future__ import annotations

import re

from _audit_utils import ROOT, fail_if, read_yaml


def numbered_bold_list(text: str) -> list[str]:
    return re.findall(r"(?m)^\d+\. \*\*([^:*]+):\*\*", text)


def numbered_table(text: str) -> list[str]:
    rows = re.findall(r"(?m)^\| \*\*(\d+)\. ([^*|]+)\*\* \|", text)
    numbers = [int(number) for number, _field in rows]
    if numbers != list(range(1, len(rows) + 1)):
        return []
    return [field.strip() for _number, field in rows]


def main() -> None:
    contract = read_yaml(ROOT / "contracts" / "diagnostic-cards.yml")
    incident = contract["incident_card"]["fields"]
    autopsy = contract["paper_autopsy"]["fields"]
    errors: list[str] = []

    c17 = (ROOT / "chapters" / "act2" / "17-update-geometry.qmd").read_text()
    c17_autopsy = c17.split("one-page autopsy:", 1)[1].split(
        "This combines the course's Spring 2026 optimizer card", 1
    )[0]
    if numbered_bold_list(c17_autopsy) != autopsy:
        errors.append("C17 Paper Autopsy fields disagree with the card covenant")

    protocol = (ROOT / "docs" / "PAPER-AUTOPSY-PROTOCOL.md").read_text()
    protocol_fields = re.findall(r"(?m)^### \d+\. (.+)$", protocol)
    if protocol_fields != autopsy:
        errors.append("Paper Autopsy Protocol fields disagree with C17")

    fixed_order = re.search(
        r"keep this fixed order: \*\*(.*?)\.\*\*",
        c17,
        flags=re.DOTALL,
    )
    c17_incident = (
        [re.sub(r"\s+", " ", field).strip() for field in fixed_order.group(1).split("→")]
        if fixed_order
        else []
    )
    if c17_incident != incident:
        errors.append("C17 Incident Card order disagrees with the card covenant")

    coda = numbered_table((ROOT / "chapters" / "coda.qmd").read_text())
    if coda != incident:
        errors.append("Coda completed report disagrees with the Incident Card")

    appendix = numbered_table(
        (ROOT / "chapters" / "appendices" / "incident-card.qmd").read_text()
    )
    if appendix != incident:
        errors.append("blank Incident Card disagrees with the card covenant")

    fail_if(errors)
    print("diagnostic cards: pass (two schemas; three Incident Card manifestations)")


if __name__ == "__main__":
    main()

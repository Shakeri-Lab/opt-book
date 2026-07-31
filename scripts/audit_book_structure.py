"""Audit mechanically promised chapter and book apparatus."""

from __future__ import annotations

import re

from _audit_utils import ROOT, public_qmd_files, front_matter, read_yaml, fail_if


def main() -> None:
    promises = read_yaml(ROOT / "contracts" / "promises.yml")["promises"]
    errors = []
    for promise in promises:
        owner = ROOT / promise["owner"]
        if promise["status"] == "active" and not owner.exists():
            errors.append(f"{promise['id']}: missing owner {owner}")

    canonical = (
        "The HTML edition is canonical; the PDF is a derived, "
        "content-equivalent print conversion."
    )
    public_text = "\n".join(path.read_text() for path in public_qmd_files())
    normalized_public = re.sub(r"\s+", " ", public_text)
    if normalized_public.count(canonical) != 1:
        errors.append("canonical-edition statement must appear exactly once")

    index_text = (ROOT / "index.qmd").read_text()
    if not re.search(
        r"(?m)^# Deep Learning: Making It Trainable \{\.unnumbered\}\s*$",
        index_text,
    ):
        errors.append("index.qmd must use an explicitly unnumbered main heading")

    unnumbered_units = {
        ROOT / "chapters" / "coda.qmd": "coda",
        ROOT / "chapters" / "provenance.qmd": "provenance-note",
    }
    for path, stable_id in unnumbered_units.items():
        text = path.read_text()
        if re.search(r"(?m)^title:", text):
            errors.append(
                f"{path}: unnumbered unit must not create a second YAML title"
            )
        if not re.search(
            rf"(?m)^# .+ \{{\.unnumbered #{re.escape(stable_id)}\}}\s*$",
            text,
        ):
            errors.append(f"{path}: missing stable unnumbered unit heading")

    theorem_contract = read_yaml(ROOT / "contracts" / "theorems.yml")
    required_theorem_fields = theorem_contract["required_fields"]
    registered_theorems = {
        theorem["id"]: theorem for theorem in theorem_contract["theorems"]
    }
    for theorem_id, theorem in registered_theorems.items():
        missing = [
            field for field in required_theorem_fields if not theorem.get(field)
        ]
        if missing:
            errors.append(f"{theorem_id}: theorem ledger missing {missing}")

    for path in sorted((ROOT / "chapters").glob("act*/[0-9][0-9]-*.qmd")):
        text = path.read_text()
        metadata = front_matter(text)
        chapter_match = re.match(r"(\d{2})-", path.name)
        if not chapter_match:
            errors.append(f"{path}: numbered chapter filename lacks two-digit prefix")
        else:
            chapter_number = int(chapter_match.group(1))
            if metadata.get("number-offset") != chapter_number - 1:
                errors.append(
                    f"{path}: number-offset must be {chapter_number - 1} "
                    f"to reserve C{chapter_number:02d}"
                )
            stable_heading = re.compile(
                rf"(?m)^# .+ \{{#c{chapter_number:02d}\}}\s*$"
            )
            if not stable_heading.search(text):
                errors.append(
                    f"{path}: main heading must declare stable ID "
                    f"c{chapter_number:02d}"
                )
        if not metadata.get("phenomenon_id"):
            errors.append(f"{path}: missing opening phenomenon metadata")
        lenses = metadata.get("lenses", {})
        if set(lenses) != {"geometric", "dynamic", "algorithmic"}:
            errors.append(f"{path}: incomplete three-lens metadata")
        elif (
            sum(role == "primary" for role in lenses.values()) != 1
            or any(
                role not in {"primary", "supporting", "quiet"}
                for role in lenses.values()
            )
        ):
            errors.append(f"{path}: invalid three-lens roles {lenses!r}")
        else:
            visible_ledger = (
                f"Geometric {lenses['geometric']} · "
                f"Dynamic {lenses['dynamic']} · "
                f"Algorithmic {lenses['algorithmic']}"
            )
            if visible_ledger not in text:
                errors.append(f"{path}: visible lens ledger disagrees with metadata")
        for required in (
            "Check yourself",
            "## Okay, so —",
            "## Sources and further reading",
            "## Exercises",
            "**(Pencil.)",
            "**(Code.)",
            "**(Audit.)",
        ):
            if required not in text:
                errors.append(f"{path}: missing {required!r}")
        theorem_starts = re.findall(
            r"::: \{#(thm-[^\s}]+)([^}\n]*)\}",
            text,
        )
        for theorem_id, attributes in theorem_starts:
            if "phenomenon_id=" not in attributes:
                errors.append(f"{path}: theorem lacks phenomenon_id: {theorem_id}")
            theorem = registered_theorems.get(theorem_id)
            if theorem is None:
                errors.append(f"{path}: unregistered theorem {theorem_id}")
            elif theorem["phenomenon_explained"] != metadata.get("phenomenon_id"):
                errors.append(
                    f"{path}: {theorem_id} phenomenon disagrees with chapter"
                )

    public_theorem_ids = set()
    for path in (ROOT / "chapters").rglob("*.qmd"):
        public_theorem_ids.update(
            re.findall(r"::: \{#(thm-[^\s}]+)", path.read_text())
        )
    unused_theorems = set(registered_theorems) - public_theorem_ids
    if unused_theorems:
        errors.append(f"theorem ledger has no public statement: {sorted(unused_theorems)}")

    for promise in promises:
        if (
            promise["status"] != "active"
            or "source" not in promise
            or "owner" not in promise
        ):
            continue
        owner = ROOT / promise["owner"]
        if not owner.exists():
            continue
        owner_text = owner.read_text()
        owner_metadata = front_matter(owner_text)
        fulfilled = owner_metadata.get("fulfills", [])
        if promise["id"] not in fulfilled:
            errors.append(f"{promise['id']}: owner does not declare fulfillment")
        evidence = promise.get("fulfillment_evidence", {})
        evidence_claims = evidence.get("claim_ids", [])
        prose_flag = evidence.get("prose_flag")
        if not evidence_claims and not prose_flag:
            errors.append(
                f"{promise['id']}: fulfillment has neither claim evidence "
                "nor a declared prose flag"
            )
        owner_claims = set(owner_metadata.get("claim_ids", []))
        missing_claims = set(evidence_claims) - owner_claims
        if missing_claims:
            errors.append(
                f"{promise['id']}: evidence claims are absent from owner "
                f"metadata: {sorted(missing_claims)}"
            )
        if prose_flag and f"#{prose_flag}" not in owner_text:
            errors.append(
                f"{promise['id']}: missing prose fulfillment flag {prose_flag}"
            )

    fail_if(errors)
    print("book structure and promises: pass")


if __name__ == "__main__":
    main()

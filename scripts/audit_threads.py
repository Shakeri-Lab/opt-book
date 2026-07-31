"""Validate registered thread seeds and seed-aware act coverage."""

from __future__ import annotations

from _audit_utils import ROOT, front_matter, read_yaml, fail_if


def main() -> None:
    contract = read_yaml(ROOT / "contracts" / "threads.yml")
    chapter_contract = contract["chapters"]
    errors = []

    for chapter_id, expected in chapter_contract.items():
        matches = list((ROOT / "chapters").rglob(f"*{chapter_id[1:]}*.qmd"))
        if len(matches) != 1:
            errors.append(f"{chapter_id}: expected exactly one manuscript, found {matches}")
            continue
        metadata = front_matter(matches[0].read_text())
        declared = metadata.get("threads", {})
        if declared != expected["threads"]:
            errors.append(
                f"{chapter_id}: manuscript threads {declared!r} != contract "
                f"{expected['threads']!r}"
            )

    for thread in contract["threads"]:
        seed = thread["seed_chapter"]
        role = chapter_contract.get(seed, {}).get("threads", {}).get(thread["id"])
        if seed in chapter_contract and role != "seed":
            errors.append(f"{thread['id']}: registered seed {seed} does not declare seed")

    fail_if(errors)
    print("threads: pass (pre-seed acts exempt)")


if __name__ == "__main__":
    main()

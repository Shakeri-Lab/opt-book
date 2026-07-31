"""Context-aware debranding audit with golden fixtures."""

from __future__ import annotations

from pathlib import Path
import re

from _audit_utils import ROOT, public_qmd_files, prose_only, read_yaml, fail_if


CONTRACT = read_yaml(ROOT / "contracts" / "branding-vocabulary.yml")


def violations(text: str) -> list[tuple[str, str]]:
    found = []
    for rule in CONTRACT["rules"]:
        term_pattern = re.compile(
            rf"(?<![A-Za-z0-9_]){re.escape(rule['term'])}(?![A-Za-z0-9_])",
            flags=re.IGNORECASE,
        )
        context_pattern = re.compile(rule["context_regex"], flags=re.IGNORECASE)
        for match in term_pattern.finditer(text):
            window = text[max(0, match.start() - 90) : match.end() + 90]
            if context_pattern.search(window):
                found.append((rule["term"], match.group()))
    return found


def main() -> None:
    allowed = (ROOT / "tests" / "fixtures" / "branding-allowed.txt").read_text()
    fixture_errors = violations(allowed)
    if fixture_errors:
        raise SystemExit(f"golden allowed sentences triggered: {fixture_errors}")

    rejected = (ROOT / "tests" / "fixtures" / "branding-violations.txt").read_text()
    rejected_terms = {term for term, _ in violations(rejected)}
    expected = {"attention", "He", "Transformer", "Adam"}
    if not expected.issubset(rejected_terms):
        raise SystemExit(
            f"golden violations did not trigger expected rules: {expected - rejected_terms}"
        )

    errors = []
    for path in public_qmd_files():
        if path.name == "rosetta.qmd":
            continue
        prose = prose_only(path.read_text())
        for scope in ("brand-bridge", "paper-audit", "search-aliases"):
            prose = re.sub(
                rf"(?ms)^::: \{{\.{scope}\}}\s*$.*?^:::\s*$",
                "",
                prose,
            )
        for term, occurrence in violations(prose):
            errors.append(f"{path}: unsanctioned branded context {occurrence!r} ({term})")
    fail_if(errors)
    print("branding: pass")


if __name__ == "__main__":
    main()

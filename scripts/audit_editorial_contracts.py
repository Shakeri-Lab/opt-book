"""Audit prediction, self-check, exercise-floor, and palette contracts."""

from __future__ import annotations

import re

from _audit_utils import ROOT, fail_if


ALLOWED_HEX = {
    value.upper()
    for value in (
        "#232D4B",
        "#9C2F2F",
        "#2E7D32",
        "#E57200",
        "#5379AA",
        "#6B6B6B",
    )
}
PREDICTION = re.compile(
    r'::: \{\.callout-important title="Prediction"\}\s*(.*?)\s*:::',
    flags=re.DOTALL,
)
AUTOPSY_FIELDS = (
    "Claim",
    "Mathematical object",
    "Resolution of the theory",
    "Dynamic regime",
    "Evidence culture and interface",
    "Estimator and comparison contract",
    "Numerical and hardware contract",
    "Assumption stress test",
    "Discriminating control",
    "Transfer verdict",
)


def main() -> None:
    errors = []
    chapter_paths = sorted((ROOT / "chapters").glob("act*/[0-9][0-9]-*.qmd"))
    for path in chapter_paths:
        text = path.read_text()
        predictions = PREDICTION.findall(text)
        if len(predictions) != 1:
            errors.append(f"{path}: expected one Prediction box")
        else:
            body = predictions[0]
            if "?" not in body:
                errors.append(f"{path}: Prediction must pose a live question")
            if re.search(r"(?i)\b(?:yes|no)[:.]|the answer is", body):
                errors.append(f"{path}: Prediction contains its own answer")

        check_start = text.find("Check yourself")
        recap_start = text.find("## Okay, so —", check_start)
        if check_start < 0 or recap_start < 0:
            errors.append(f"{path}: cannot locate Check yourself contract")
        elif "?" not in text[check_start:recap_start]:
            errors.append(f"{path}: Check yourself must contain questions")

        sources_start = text.find("## Sources and further reading", recap_start)
        unresolved = re.search(
            r"- \*\*Unresolved:\*\*\s*(.*?)(?=\n\n## Sources and further reading)",
            text[recap_start:],
            flags=re.DOTALL,
        )
        if unresolved is None:
            errors.append(f"{path}: cannot locate Unresolved recap entry")
        else:
            unresolved_text = re.sub(r"\s+", " ", unresolved.group(1)).strip()
            if not unresolved_text.endswith("?"):
                errors.append(f"{path}: Unresolved recap must end as a question")
        if sources_start < 0:
            errors.append(f"{path}: cannot locate Sources section")
        else:
            exercise_start_for_sources = text.find("## Exercises", sources_start)
            sources_text = text[sources_start:exercise_start_for_sources]
            if sources_text.count("**Reading order.**") != 1:
                errors.append(
                    f"{path}: Sources must contain one reading-order sentence"
                )

        exercise_start = text.find("## Exercises")
        if exercise_start < 0:
            errors.append(f"{path}: cannot locate Exercises")
        else:
            exercise_text = text[exercise_start:]
            count = len(re.findall(r"(?m)^\d+\. \*\*\((?:Pencil|Code|Audit)\.\)", exercise_text))
            if count < 5:
                errors.append(f"{path}: exercise floor is five, found {count}")
            audits = re.findall(
                r"(?ms)^\d+\. \*\*\(Audit\.\) Paper audit:.*?"
                r"(?=^\d+\. \*\*\(|\Z)",
                exercise_text,
            )
            for audit in audits:
                normalized_audit = re.sub(r"\s+", " ", audit)
                if "all ten fields" in normalized_audit:
                    continue
                selected = [
                    field for field in AUTOPSY_FIELDS if field in normalized_audit
                ]
                if not 4 <= len(selected) <= 6:
                    errors.append(
                        f"{path}: Paper audit must name four to six exact "
                        f"Protocol fields, found {selected}"
                    )

        colors = {value.upper() for value in re.findall(r"#[0-9A-Fa-f]{6}", text)}
        unapproved = colors - ALLOWED_HEX
        if unapproved:
            errors.append(f"{path}: unapproved figure colors {sorted(unapproved)}")

    coda = (ROOT / "chapters" / "coda.qmd").read_text()
    if "#| fig-cap:" in coda or "Figure Coda.1" not in coda:
        errors.append("Coda incident panel must use the Coda.1 caption namespace")
    for sigil in ("NS ·", "RS ·", "LG ·", "SG ·"):
        if sigil not in coda:
            errors.append(f"Coda must harvest public thread sigil {sigil}")
    if (
        "That is what it means to make a training run diagnosable — and "
        "therefore\ntrainable."
        not in coda
    ):
        errors.append("Coda must end on the unhedged title callback")

    card = (ROOT / "chapters" / "appendices" / "incident-card.qmd").read_text()
    for field in (
        "1. Symptom",
        "2. Prediction",
        "3. Contract",
        "4. Precision control",
        "5. Curvature control",
        "6. Estimator control",
        "7. Spectrum locator",
        "8. State control",
        "9. Verdict",
        "10. Corrective control",
    ):
        if field not in card:
            errors.append(f"Incident Card missing field {field}")

    fail_if(errors)
    print(f"editorial contracts: pass ({len(chapter_paths)} chapters)")


if __name__ == "__main__":
    main()

"""Audit prediction, self-check, exercise-floor, and palette contracts."""

from __future__ import annotations

import re

from _audit_utils import ROOT, fail_if


ALLOWED_HEX = {
    "#232D4B",
    "#9C2F2F",
    "#2E7D32",
    "#E57200",
    "#5379AA",
    "#6B6B6B",
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

    fail_if(errors)
    print(f"editorial contracts: pass ({len(chapter_paths)} chapters)")


if __name__ == "__main__":
    main()

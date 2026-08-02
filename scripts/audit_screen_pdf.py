"""Audit the continuous screen PDF against the print edition."""

from __future__ import annotations

from pathlib import Path
import re

from pypdf import PdfReader

from _audit_utils import ROOT, fail_if, read_yaml


PRINT = ROOT / "_book" / "Deep-Learning--Making-It-Trainable.pdf"
SCREEN = ROOT / "_book" / "Deep-Learning--Making-It-Trainable-Screen.pdf"


def main() -> None:
    errors = []
    if not PRINT.exists():
        errors.append(f"missing print PDF {PRINT}")
    if not SCREEN.exists():
        errors.append(f"missing screen PDF {SCREEN}")
    fail_if(errors)

    print_pages = len(PdfReader(str(PRINT)).pages)
    screen_reader = PdfReader(str(SCREEN))
    screen_pages = len(screen_reader.pages)
    if screen_pages >= print_pages:
        errors.append(
            f"screen PDF has {screen_pages} pages; print has {print_pages}"
        )
    extracted = [(page.extract_text() or "").strip() for page in screen_reader.pages]
    rights = read_yaml(ROOT / "contracts" / "release.yml")["rights_statement"]
    if rights not in re.sub(r"\s+", " ", " ".join(extracted)):
        errors.append("screen PDF text layer omits the release rights statement")
    blank_runs = []
    blank_pages = []
    run_start = None
    for number, page_text in enumerate(extracted, start=1):
        if not page_text and run_start is None:
            run_start = number
            blank_pages.append(number)
        elif not page_text:
            blank_pages.append(number)
        elif page_text and run_start is not None:
            blank_runs.append((run_start, number - 1))
            run_start = None
    if run_start is not None:
        blank_runs.append((run_start, len(extracted)))
    if blank_pages:
        errors.append(f"screen PDF contains blank pages {blank_pages}")
    fail_if(errors)
    print(
        f"screen PDF: pass ({screen_pages} pages versus {print_pages} print pages)"
    )


if __name__ == "__main__":
    main()

"""Reject slide, classroom, and local-source residue in public prose."""

from __future__ import annotations

import re

from _audit_utils import public_qmd_files, prose_only, fail_if


PATTERNS = [
    r"\bas the slide shows\b",
    r"\bon this slide\b",
    r"\bnext slide\b",
    r"\bin lecture\b",
    r"\bthe lecture\b",
    r"\bthis lecture\b",
    r"\bin class\b",
    r"\bour class\b",
    r"\btoday we\b",
    r"\bnext week\b",
    r"\blast week\b",
    r"\bas I showed\b",
    r"\bas I said\b",
    r"\bon the board\b",
    r"\bpause here\b",
    r"\bthe seed's\b",
    r"\\(?:pause|only|uncover|onslide|visible|frametitle)\b",
    r"\\begin\{frame\}",
    r"/Users/",
    r"my_lectures/",
    r"old/DS6210_Book/",
]


def main() -> None:
    errors = []
    for path in public_qmd_files():
        prose = prose_only(path.read_text())
        for pattern in PATTERNS:
            match = re.search(pattern, prose, flags=re.IGNORECASE)
            if match:
                line = prose.count("\n", 0, match.start()) + 1
                errors.append(f"{path}: residue {match.group()!r} near prose line {line}")
    fail_if(errors)
    print("public voice: pass")


if __name__ == "__main__":
    main()

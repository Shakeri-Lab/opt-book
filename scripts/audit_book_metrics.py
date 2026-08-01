"""Emit or audit one reproducible chapter word-count and PDF-span ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from pypdf import PdfReader

from _audit_utils import ROOT, prose_only


PDF = ROOT / "_book" / "Deep-Learning--Making-It-Trainable.pdf"
LEDGER = ROOT / "artifacts" / "book-metrics.json"


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def source_record(path: Path) -> dict[str, object]:
    text = path.read_text()
    title_match = re.search(r"(?m)^# (.+?) \{#c(\d{2})\}\s*$", text)
    if title_match is None:
        raise SystemExit(f"cannot read stable chapter heading from {path}")
    prose = prose_only(text)
    words = re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", prose)
    return {
        "unit": f"C{title_match.group(2)}",
        "title": title_match.group(1),
        "source": str(path.relative_to(ROOT)),
        "source_noncode_words_excluding_sources": len(words),
    }


def first_body_heading_page(pages: list[str], heading: str) -> int:
    target = normalized(heading)
    matches = [
        index
        for index, page in enumerate(pages, start=1)
        if index > 10 and normalized(page).startswith(target)
    ]
    if not matches:
        raise SystemExit(f"cannot locate PDF heading {heading!r}")
    return matches[0]


def metrics() -> dict[str, object]:
    if not PDF.exists():
        raise SystemExit(f"missing rendered PDF {PDF}")
    reader = PdfReader(str(PDF))
    pages = [(page.extract_text() or "") for page in reader.pages]
    chapter_paths = sorted(
        (ROOT / "chapters").glob("act*/[0-9][0-9]-*.qmd"),
        key=lambda path: int(path.name[:2]),
    )
    chapters = [source_record(path) for path in chapter_paths]
    for record in chapters:
        number = int(str(record["unit"])[1:])
        record["pdf_physical_start"] = first_body_heading_page(
            pages, f"{number}. {record['title']}"
        )

    coda_start = first_body_heading_page(pages, "One Spike, Four Suspects")
    for index, record in enumerate(chapters):
        next_start = (
            chapters[index + 1]["pdf_physical_start"]
            if index + 1 < len(chapters)
            else coda_start
        )
        record["pdf_physical_end"] = int(next_start) - 1
        record["pdf_span_pages"] = (
            int(record["pdf_physical_end"])
            - int(record["pdf_physical_start"])
            + 1
        )

    beyond_start = first_body_heading_page(pages, "Beyond This Volume")
    provenance_start = first_body_heading_page(
        pages, "Provenance and Acknowledgements"
    )
    return {
        "schema_version": 1,
        "counting_contract": (
            "source prose after front-matter and fenced-code removal, with "
            "Sources and further reading excluded; PDF physical spans end "
            "immediately before the next numbered chapter or Coda; the Coda "
            "ends immediately before Beyond This Volume"
        ),
        "pdf_total_pages": len(pages),
        "chapters": chapters,
        "coda": {
            "pdf_physical_start": coda_start,
            "pdf_physical_end": beyond_start - 1,
            "pdf_span_pages": beyond_start - coda_start,
        },
        "beyond_this_volume": {
            "pdf_physical_start": beyond_start,
            "pdf_physical_end": provenance_start - 1,
            "pdf_span_pages": provenance_start - beyond_start,
        },
        "provenance_note_pdf_physical_start": provenance_start,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--print",
        action="store_true",
        dest="print_only",
        help="print the current ledger instead of comparing it",
    )
    args = parser.parse_args()
    current = metrics()
    if args.print_only:
        print(json.dumps(current, indent=2))
        return
    if not LEDGER.exists():
        raise SystemExit(f"missing committed metrics ledger {LEDGER}")
    expected = json.loads(LEDGER.read_text())
    if current != expected:
        raise SystemExit(
            "book metrics changed; inspect the rendered diff and update "
            "artifacts/book-metrics.json deliberately"
        )
    print(
        f"book metrics: pass ({len(current['chapters'])} chapters, "
        f"{current['pdf_total_pages']} PDF pages)"
    )


if __name__ == "__main__":
    main()

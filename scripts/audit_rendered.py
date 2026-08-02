"""Audit rendered HTML/PDF structure, extraction, alt text, and fallback state."""

from __future__ import annotations

from pathlib import Path
import json
import re
import subprocess

from bs4 import BeautifulSoup
from pypdf import PdfReader

from _audit_utils import (
    ROOT,
    fail_if,
    front_matter,
    prose_only,
    public_qmd_files,
    read_yaml,
)


PDF = ROOT / "_book" / "Deep-Learning--Making-It-Trainable.pdf"


def numbered_chapters() -> list[tuple[Path, Path, str, str]]:
    chapters = []
    for source in sorted(
        (ROOT / "chapters").glob("act*/[0-9][0-9]-*.qmd"),
        key=lambda path: int(path.name[:2]),
    ):
        number = str(int(source.name[:2]))
        body = source.read_text()
        heading = re.search(r"(?m)^# (.+?) \{#c\d{2}\}\s*$", body)
        if heading is None:
            continue
        html = ROOT / "_book" / source.relative_to(ROOT).with_suffix(".html")
        chapters.append((source, html, number, heading.group(1)))
    return chapters


def source_vocabulary() -> set[str]:
    text = "\n".join(prose_only(path.read_text()) for path in public_qmd_files())
    return {word.lower() for word in re.findall(r"[A-Za-z]{3,}", text)}


def main() -> None:
    errors = []
    html_files = sorted((ROOT / "_book").rglob("*.html"))
    source_refs: set[str] = set()
    for source in public_qmd_files():
        source_refs.update(
            re.findall(r"@((?:fig|eq|thm|exr)-[A-Za-z0-9_-]+)", source.read_text())
        )
    rendered_fragment_links: set[str] = set()
    if not html_files:
        errors.append("no rendered HTML files")
    for path in html_files:
        soup = BeautifulSoup(path.read_text(errors="replace"), "html.parser")
        rendered_fragment_links.update(
            href.rsplit("#", 1)[1]
            for tag in soup.find_all("a", href=True)
            if "#" in (href := tag.get("href", ""))
        )
        for image in soup.find_all("img"):
            if image.get("role") == "presentation":
                continue
            alt = (image.get("alt") or "").strip()
            if len(alt.split()) < 5:
                errors.append(f"{path}: weak or missing alt text for {image.get('src')}")
        text = soup.get_text(" ")
        if "??" in text or re.search(r"@(?:fig|eq|thm|exr)-", text):
            errors.append(f"{path}: unresolved cross-reference marker")
        for output in soup.select(".cell-output pre"):
            for line_number, line in enumerate(
                output.get_text().splitlines(), start=1
            ):
                if len(line) > 92:
                    errors.append(
                        f"{path}: code output line {line_number} is "
                        f"{len(line)} characters (limit 92)"
                    )
    for reference in sorted(source_refs - rendered_fragment_links):
        errors.append(f"rendered HTML has no link for source reference @{reference}")

    for result_path in sorted(
        (ROOT / "_freeze").rglob("execute-results/*.json")
    ):
        frozen = json.loads(result_path.read_text())
        markdown = frozen.get("result", {}).get("markdown", "")
        if "cell-output-error" in markdown or "Traceback (most recent call last)" in markdown:
            errors.append(f"{result_path}: frozen execution contains an error")

    chapter_records = numbered_chapters()
    for _source, path, expected, _title in chapter_records:
        if not path.exists():
            errors.append(f"missing numbered chapter HTML {path}")
            continue
        soup = BeautifulSoup(path.read_text(), "html.parser")
        title = soup.select_one("h1.title .chapter-number")
        if title is None or title.get_text(strip=True) != expected:
            errors.append(f"{path}: rendered chapter number is not {expected}")
        wrong_prefix = str(int(expected) - 1)
        if soup.select_one(
            f'h2[data-number^="{wrong_prefix}."], '
            f'span.header-section-number:-soup-contains("{wrong_prefix}.")'
        ):
            errors.append(f"{path}: stale sequential prefix {wrong_prefix} survives")

    index_html = ROOT / "_book" / "index.html"
    if index_html.exists():
        index_soup = BeautifulSoup(index_html.read_text(), "html.parser")
        home_links = [
            link
            for link in index_soup.find_all("a", href=True)
            if link["href"] in {"./index.html", "index.html"}
        ]
        if any(link.select_one(".chapter-number") for link in home_links):
            errors.append("introduction is numbered in rendered HTML navigation")

    for relative in (
        "chapters/on-ramp.html",
        "chapters/coda.html",
        "chapters/beyond-this-volume.html",
        "chapters/provenance.html",
    ):
        path = ROOT / "_book" / relative
        if not path.exists():
            errors.append(f"missing unnumbered unit HTML {path}")
            continue
        soup = BeautifulSoup(path.read_text(), "html.parser")
        if soup.select_one("h1.title .chapter-number, .breadcrumb .chapter-number"):
            errors.append(f"{path}: unnumbered unit acquired a chapter number")
        if soup.select_one(".header-section-number"):
            errors.append(f"{path}: unnumbered unit acquired section numbering")

    search_path = ROOT / "_book" / "search.json"
    if search_path.exists():
        search = json.loads(search_path.read_text())
        expected_search = {
            str(source.relative_to(ROOT).with_suffix(".html")): expected
            for source, _html, expected, _title in chapter_records
        }
        for href, expected in expected_search.items():
            matches = [item for item in search if item.get("href") == href]
            if not matches or not matches[0].get("title", "").startswith(
                f"{expected}\u00a0"
            ):
                errors.append(f"search index has stale chapter number for {href}")

    if not PDF.exists():
        errors.append(f"missing PDF {PDF}")
        fail_if(errors)

    extracted = subprocess.check_output(
        ["pdftotext", "-enc", "UTF-8", str(PDF), "-"]
    ).decode("utf-8", errors="replace")
    rights = read_yaml(ROOT / "contracts" / "release.yml")["rights_statement"]
    if rights not in re.sub(r"\s+", " ", extracted):
        errors.append("PDF text layer omits the release rights statement")
    if "\x00" in extracted or "\ufffd" in extracted:
        errors.append("PDF extraction contains NUL or U+FFFD")
    if "??" in extracted or re.search(r"@(?:fig|eq|thm|exr)-", extracted):
        errors.append("PDF contains unresolved cross-reference marker")
    for _source, _html, number, title in chapter_records:
        expected = f"{number}. {title}"
        if expected not in extracted:
            errors.append(f"PDF stable chapter numbering missing {expected!r}")
    if "1. One Pass, Two Failures" in extracted:
        errors.append("PDF renumbered C02 into the reserved C01 slot")
    if "18. One Spike, Four Suspects" in extracted:
        errors.append("PDF numbered the Coda as Chapter 18")
    if "19. Provenance and Acknowledgements" in extracted:
        errors.append("PDF numbered the provenance note as Chapter 19")
    for forbidden in (
        "Part I. Act 0",
        "Part II. Act I",
        "Part III. Act II",
        "I. Act 0",
        "II. Act I",
        "III. Act II",
        "Figure 17.3",
        "18. Beyond This Volume",
    ):
        if forbidden in extracted:
            errors.append(f"PDF retained forbidden production label {forbidden!r}")

    vocabulary = source_vocabulary()
    for page_number, page in enumerate(extracted.split("\f"), start=1):
        words = re.findall(r"[A-Za-z]{3,}", page)
        if len(words) < 25:
            continue
        recognized = [word.lower() in vocabulary for word in words]
        ratio = sum(recognized) / len(recognized)
        longest = 0
        current = 0
        for known in recognized:
            current = 0 if known else current + 1
            longest = max(longest, current)
        if ratio < 0.45 and longest >= 8:
            errors.append(
                f"PDF page {page_number}: suspicious word ratio {ratio:.2f}, "
                f"unknown run {longest}"
            )

    reader = PdfReader(str(PDF))
    root = reader.trailer["/Root"]
    if "/StructTreeRoot" not in root:
        fixture = ROOT / "tests" / "fixtures" / "tagged-pdf.md"
        if not fixture.exists():
            errors.append("PDF is untagged and no D24 fallback fixture exists")
        else:
            print("ACCESSIBILITY FALLBACK: PDF is untagged; D24 fixture retained")

    log_path = ROOT / "tmp" / "pdfs" / "book-build.log"
    if log_path.exists():
        log = log_path.read_text(errors="replace")
        if "Missing character" in log:
            errors.append("LuaLaTeX log contains Missing character")

    fail_if(errors)
    print("rendered HTML/PDF: pass")


if __name__ == "__main__":
    main()

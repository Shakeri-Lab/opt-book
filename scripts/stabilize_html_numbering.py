"""Align rendered HTML labels with stable C-numbers while chapters are sparse."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_book"


def chapter_paths() -> list[str]:
    paths = [
        path
        for path in (ROOT / "chapters").glob("act*/[0-9][0-9]-*.qmd")
        if re.match(r"\d{2}-", path.name)
    ]
    paths.sort(key=lambda path: int(path.name[:2]))
    return [str(path.relative_to(ROOT)) for path in paths]


def numbering_map() -> dict[str, tuple[int, int]]:
    mapping: dict[str, tuple[int, int]] = {}
    for actual, source in enumerate(chapter_paths(), start=1):
        match = re.search(r"/(\d{2})-([^/]+)\.qmd$", source)
        if match is None:
            continue
        desired = int(match.group(1))
        output = str(Path(source).with_suffix(".html"))
        mapping[output] = (actual, desired)
    return mapping


def _map_chapter_span(match: re.Match[str], lookup: dict[int, int]) -> str:
    actual = int(match.group(2))
    desired = lookup.get(actual, actual)
    return f"{match.group(1)}{desired}{match.group(3)}"


def renumber_html(
    text: str,
    *,
    current: tuple[int, int] | None,
    lookup: dict[int, int],
) -> str:
    text = re.sub(
        r'(<span class="chapter-number">)(\d+)(</span>)',
        lambda match: _map_chapter_span(match, lookup),
        text,
    )
    if current is None:
        return text

    actual, desired = current
    if actual == desired:
        return text
    actual_text = str(actual)
    desired_text = str(desired)

    substitutions = (
        (
            rf'(<title>){actual_text}(&nbsp;)',
            rf"\g<1>{desired_text}\g<2>",
        ),
        (
            rf'(data-number="){actual_text}(?=\.|")',
            rf"\g<1>{desired_text}",
        ),
        (
            rf'(<span class="header-section-number">){actual_text}(?=\.)',
            rf"\g<1>{desired_text}",
        ),
        (
            rf'(\\tag\{{){actual_text}(?=\.)',
            rf"\g<1>{desired_text}",
        ),
        (
            rf'((?:Figure&nbsp;|Theorem )){actual_text}(?=\.)',
            rf"\g<1>{desired_text}",
        ),
    )
    for pattern, replacement in substitutions:
        text = re.sub(pattern, replacement, text)

    def xref(match: re.Match[str]) -> str:
        number = int(match.group(2))
        return (
            match.group(1)
            + str(lookup.get(number, number))
            + match.group(3)
        )

    return re.sub(
        r'(<a [^>]*class="quarto-xref"[^>]*>.*?<span>)(\d+)(\.)',
        xref,
        text,
    )


def _renumber_search_string(value: str, actual: int, desired: int) -> str:
    if actual == desired:
        return value
    actual_text = str(actual)
    desired_text = str(desired)
    value = re.sub(
        rf"^{actual_text}(?=(?:\u00a0|&nbsp;|\.))",
        desired_text,
        value,
    )
    value = re.sub(
        rf"(?m)^{actual_text}(?=\.\d+(?:\.\d+)?\s)",
        desired_text,
        value,
    )
    value = re.sub(
        rf"(\\tag\{{){actual_text}(?=\.)",
        rf"\g<1>{desired_text}",
        value,
    )
    value = re.sub(
        rf"((?:Equation|Figure|Theorem)(?:\u00a0|&nbsp;)){actual_text}(?=\.)",
        rf"\g<1>{desired_text}",
        value,
    )
    value = re.sub(
        rf"(<span class=['\"]chapter-number['\"]>){actual_text}(</span>)",
        rf"\g<1>{desired_text}\g<2>",
        value,
    )
    return value


def renumber_search_item(
    item: dict[str, Any],
    mapping: dict[str, tuple[int, int]],
) -> dict[str, Any]:
    href = item.get("href", "").split("#", 1)[0]
    current = mapping.get(href)
    if current is None:
        return item
    actual, desired = current
    for key in ("title", "section", "text"):
        if isinstance(item.get(key), str):
            item[key] = _renumber_search_string(item[key], actual, desired)
    if isinstance(item.get("crumbs"), list):
        item["crumbs"] = [
            _renumber_search_string(value, actual, desired)
            if isinstance(value, str)
            else value
            for value in item["crumbs"]
        ]
    return item


def main() -> None:
    mapping = numbering_map()
    lookup = {actual: desired for actual, desired in mapping.values()}
    if not mapping or all(actual == desired for actual, desired in mapping.values()):
        print("stable chapter numbering: native sequence already matches C-numbers")
        return

    html_files = sorted(OUTPUT.rglob("*.html")) if OUTPUT.exists() else []
    for path in html_files:
        relative = str(path.relative_to(OUTPUT))
        original = path.read_text()
        revised = renumber_html(
            original,
            current=mapping.get(relative),
            lookup=lookup,
        )
        if revised != original:
            path.write_text(revised)

    search_path = OUTPUT / "search.json"
    if search_path.exists():
        items = json.loads(search_path.read_text())
        items = [renumber_search_item(item, mapping) for item in items]
        search_path.write_text(json.dumps(items, ensure_ascii=False))

    summary = ", ".join(
        f"C{desired:02d}→{desired}"
        for _source, (_actual, desired) in mapping.items()
    )
    print(f"stable chapter numbering: pass ({summary})")


if __name__ == "__main__":
    main()

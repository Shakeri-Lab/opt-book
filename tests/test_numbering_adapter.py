from __future__ import annotations

from scripts.stabilize_html_numbering import renumber_html, renumber_search_item


def test_html_numbering_maps_navigation_and_current_chapter() -> None:
    html = """
    <title>1&nbsp; One Pass</title>
    <a href="02.html"><span class="chapter-number">1</span></a>
    <span class="header-section-number">1.2</span>
    <span class="math display">\\tag{1.3}</span>
    <figcaption>Figure&nbsp;1.1: witness</figcaption>
    <a class="quarto-xref" href="#eq"><span>1.3</span></a>
    """
    revised = renumber_html(html, current=(1, 2), lookup={1: 2, 2: 3})
    assert "<title>2&nbsp; One Pass</title>" in revised
    assert '<span class="chapter-number">2</span>' in revised
    assert '<span class="header-section-number">2.2</span>' in revised
    assert "\\tag{2.3}" in revised
    assert "Figure&nbsp;2.1" in revised
    assert "<span>2.3</span>" in revised


def test_search_numbering_does_not_change_semantic_chapter_reference() -> None:
    item = {
        "href": "chapters/act0/03-precision-contract.html#loss",
        "title": "2\u00a0 The Grid",
        "section": "2.4 Two losses",
        "text": "2.4 Two losses\nChapter 2 separated two failures. Equation\u00a02.3.",
        "crumbs": ["<span class='chapter-number'>2</span>"],
    }
    revised = renumber_search_item(
        item,
        {"chapters/act0/03-precision-contract.html": (2, 3)},
    )
    assert revised["title"].startswith("3\u00a0")
    assert revised["section"].startswith("3.4")
    assert revised["text"].startswith("3.4")
    assert "Chapter 2 separated" in revised["text"]
    assert "Equation\u00a03.3" in revised["text"]
    assert "chapter-number'>3</span>" in revised["crumbs"][0]

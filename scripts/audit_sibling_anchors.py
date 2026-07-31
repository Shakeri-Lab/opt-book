"""Audit the cross-book public-anchor contract, optionally over the network."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import re
from urllib.parse import urldefrag
from urllib.request import Request, urlopen

from _audit_utils import ROOT, read_yaml, fail_if


URL_PATTERN = re.compile(
    r"https://shakeri-lab\.github\.io/dl-book/[^\s)>]+#[A-Za-z0-9_.:-]+"
)


class IdCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name == "id" and value:
                self.ids.add(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--network", action="store_true")
    arguments = parser.parse_args()

    contract = read_yaml(ROOT / "contracts" / "sibling-anchors.yml")
    declared = {item["url"] for item in contract["anchors"]}
    errors: list[str] = []
    observed: set[str] = set()
    for root in (ROOT / "chapters", ROOT / "docs"):
        for path in sorted(root.rglob("*.qmd")) + sorted(root.rglob("*.md")):
            observed.update(URL_PATTERN.findall(path.read_text()))
    undeclared = observed - declared
    if undeclared:
        errors.append(f"undeclared sibling anchors: {sorted(undeclared)}")

    if arguments.network:
        for url in sorted(declared):
            page_url, fragment = urldefrag(url)
            try:
                request = Request(page_url, headers={"User-Agent": "opt-book-anchor-audit/1"})
                with urlopen(request, timeout=30) as response:
                    body = response.read().decode("utf-8", errors="replace")
                collector = IdCollector()
                collector.feed(body)
                if fragment not in collector.ids:
                    errors.append(f"missing fragment #{fragment} at {page_url}")
            except Exception as error:  # pragma: no cover - scheduled network path
                errors.append(f"could not verify {url}: {error}")

    fail_if(errors)
    mode = "network and declaration" if arguments.network else "declaration"
    print(f"sibling anchors ({mode}): pass")


if __name__ == "__main__":
    main()

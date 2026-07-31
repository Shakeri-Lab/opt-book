"""Shared helpers for repository audits."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parents[1]


def public_qmd_files() -> list[Path]:
    return [ROOT / "index.qmd", *sorted((ROOT / "chapters").rglob("*.qmd"))]


def read_yaml(path: Path) -> Any:
    if path.suffix == ".json":
        return json.loads(path.read_text())
    return yaml.safe_load(path.read_text())


def front_matter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    return yaml.safe_load(text[4:end]) or {}


def strip_front_matter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    return text[end + 5 :] if end >= 0 else text


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def strip_sources(text: str) -> str:
    return re.sub(
        r"(?ms)^## Sources and further reading(?:\s+\{[^\n]+\})?\s*$.*?(?=^## |\Z)",
        "",
        text,
    )


def prose_only(text: str) -> str:
    return strip_sources(strip_fenced_code(strip_front_matter(text)))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def payload_sha256(payload: dict[str, Any]) -> str:
    clean = dict(payload)
    clean.pop("payload_sha256", None)
    encoded = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def fail_if(errors: Iterable[str]) -> None:
    collected = list(errors)
    if collected:
        raise SystemExit("\n".join(f"ERROR: {item}" for item in collected))

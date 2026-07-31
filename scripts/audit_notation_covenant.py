"""Check the notation source of truth against both rendering paths."""

from __future__ import annotations

from _audit_utils import ROOT, read_yaml, fail_if


def main() -> None:
    covenant = read_yaml(ROOT / "contracts" / "notation-covenant.yml")
    pdf = (ROOT / "tex" / "macros.tex").read_text()
    html = (ROOT / "mathjax-config.html").read_text()
    appendix = (ROOT / "chapters" / "appendices" / "notation.qmd").read_text()
    errors = []

    ids = [entry["id"] for entry in covenant["core"] + covenant["extensions"]]
    if len(ids) != len(set(ids)):
        errors.append("notation IDs are not unique")

    for entry in covenant["core"]:
        macro = entry.get("macro")
        if not macro:
            continue
        bare = macro.lstrip("\\")
        if f"\\newcommand{{\\{bare}}}" not in pdf and f"\\DeclareMathOperator*{{\\{bare}}}" not in pdf:
            errors.append(f"PDF macro missing for {macro}")
        if f"{bare}:" not in html and f"{bare}:" not in html.replace('"', ""):
            errors.append(f"HTML macro missing for {macro}")

    for entry in covenant["extensions"]:
        if entry["latex"] not in appendix:
            errors.append(f"notation appendix missing {entry['id']}: {entry['latex']}")

    fail_if(errors)
    print("notation covenant: pass")


if __name__ == "__main__":
    main()

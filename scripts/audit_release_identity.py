"""Keep source citation metadata and annotated book tags in lockstep."""

from __future__ import annotations

import re
import subprocess
import tomllib

from _audit_utils import ROOT, fail_if, read_yaml


def git(*arguments: str) -> str:
    return subprocess.check_output(
        ["git", *arguments], cwd=ROOT, text=True
    ).strip()


def main() -> None:
    release = read_yaml(ROOT / "contracts" / "release.yml")
    cff = read_yaml(ROOT / "CITATION.cff")
    quarto = read_yaml(ROOT / "_quarto.yml")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())
    index = (ROOT / "index.qmd").read_text()
    changelog = (ROOT / "CHANGELOG.md").read_text()
    errors: list[str] = []

    version = str(release["book_version"])
    display = str(release["display_version"])
    date = str(release["release_date"])
    tag = release["tag"]
    if str(cff.get("version")) != version:
        errors.append("CITATION.cff version disagrees with release contract")
    if str(cff.get("date-released")) != date:
        errors.append("CITATION.cff date disagrees with release contract")
    if project["project"]["version"] != version:
        errors.append("pyproject.toml version disagrees with release contract")
    if str(quarto["book"]["date"]) != date:
        errors.append("Quarto publication date disagrees with release contract")
    if not re.search(rf"Public draft\s+{re.escape(display)}\.", index):
        errors.append("suggested citation disagrees with release display version")
    if release["rights_statement"] not in index:
        errors.append("colophon omits the release rights statement")
    if f"## {version} —" not in changelog:
        errors.append("CHANGELOG omits the current release")

    existing = git("tag", "--list", tag)
    if not existing:
        dirty = git("status", "--porcelain")
        if not dirty:
            errors.append(f"clean release source has no {tag} annotated tag")
        else:
            print(f"PRE-RELEASE: {tag} will be required when the source is committed")
    else:
        if git("cat-file", "-t", tag) != "tag":
            errors.append(f"{tag} is not an annotated tag")
        latest = git(
            "for-each-ref",
            "--sort=-version:refname",
            "--count=1",
            "--format=%(refname:short)",
            "refs/tags/book-v*",
        )
        if latest != tag:
            errors.append(f"release contract names {tag}, latest book tag is {latest}")
        tagged_cff = read_yaml_text(git("show", f"{tag}:CITATION.cff"))
        if str(tagged_cff.get("version")) != version:
            errors.append(f"{tag} does not contain citation version {version}")
        message = git("for-each-ref", "--format=%(contents)", f"refs/tags/{tag}")
        if release["citation"] not in re.sub(r"\s+", " ", message):
            errors.append(f"{tag} message omits the canonical citation")
        for filename in (
            "Deep-Learning--Making-It-Trainable.pdf",
            "Deep-Learning--Making-It-Trainable-Screen.pdf",
        ):
            if not re.search(
                rf"{re.escape(filename)} SHA-256: [0-9a-f]{{64}}", message
            ):
                errors.append(f"{tag} message omits the digest for {filename}")

    fail_if(errors)
    print(f"release identity: pass ({tag}; citation {display})")


def read_yaml_text(text: str) -> dict:
    import yaml

    return yaml.safe_load(text)


if __name__ == "__main__":
    main()

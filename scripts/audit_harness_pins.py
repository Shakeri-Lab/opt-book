"""Validate chapter harness metadata, wheel digests, and publication state."""

from __future__ import annotations

import hashlib
import re
import subprocess

from _audit_utils import ROOT, file_sha256, front_matter, read_yaml, fail_if


def ignored_by_git(path) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=False,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(f"git check-ignore failed for {path}")
    return result.returncode == 0


def git_output(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = result.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout


def tagged_source_errors(source: dict) -> list[str]:
    errors = []
    commit = source.get("commit")
    tag = source.get("annotated_tag")
    if not isinstance(commit, str) or not isinstance(tag, str):
        return ["tagged source requires commit and annotated_tag strings"]
    try:
        if git_output("cat-file", "-t", tag).decode().strip() != "tag":
            errors.append(f"{tag}: source identity is not an annotated tag")
        target = git_output("rev-parse", f"{tag}^{{}}").decode().strip()
        if target != commit:
            errors.append(f"{tag}: resolves to {target}, expected {commit}")
    except RuntimeError as exc:
        return [str(exc)]

    for key, expected in source.items():
        if not key.endswith("_sha256"):
            continue
        stem = key.removesuffix("_sha256")
        if stem == "pyproject":
            repo_path = "harness/pyproject.toml"
        elif stem == "init":
            repo_path = "harness/src/trainable_harness/__init__.py"
        else:
            repo_path = f"harness/src/trainable_harness/{stem}.py"
        try:
            source_bytes = git_output("show", f"{commit}:{repo_path}")
            actual = hashlib.sha256(source_bytes).hexdigest()
        except RuntimeError as exc:
            errors.append(str(exc))
            continue
        if actual != expected:
            errors.append(
                f"{tag}: {repo_path} digest {actual} does not match manifest {expected}"
            )
    return errors


def validate_source_identity(
    harness_ref: str,
    source: dict,
    errors: list[str],
    tagged: set[str],
    content_addressed: set[str],
) -> None:
    status = source.get("status")
    identity_contract = source.get("identity_contract")
    if status == "content-addressed-rolling-draft":
        content_addressed.add(harness_ref)
        if identity_contract != "wheel-sha256-under-d34":
            errors.append(f"{harness_ref}: invalid historical identity contract")
        if (
            source.get("commit") is not None
            or source.get("annotated_tag") is not None
        ):
            errors.append(
                f"{harness_ref}: D34 forbids backfilled historical source identity"
            )
    elif status == "tagged-source":
        tagged.add(harness_ref)
        if identity_contract != "annotated-source-tag-under-d34":
            errors.append(f"{harness_ref}: invalid tagged identity contract")
        errors.extend(f"{harness_ref}: {item}" for item in tagged_source_errors(source))
    else:
        errors.append(f"{harness_ref}: unknown D34 source status {status!r}")


def main() -> None:
    errors = []
    tagged = set()
    content_addressed = set()
    for path in sorted((ROOT / "chapters").rglob("*.qmd")):
        text = path.read_text()
        metadata = front_matter(text)
        harness_ref = metadata.get("harness-ref")
        if not harness_ref:
            continue
        manifest_path = ROOT / "artifacts" / "harness" / harness_ref / "manifest.json"
        if not manifest_path.exists():
            errors.append(f"{path}: missing {manifest_path}")
            continue
        if ignored_by_git(manifest_path):
            errors.append(f"{path}: manifest is ignored by Git: {manifest_path}")
        manifest = read_yaml(manifest_path)
        wheel = manifest_path.parent / manifest["wheel"]
        if not wheel.exists():
            errors.append(f"{path}: missing wheel {wheel}")
            continue
        if ignored_by_git(wheel):
            errors.append(f"{path}: vendored wheel is ignored by Git: {wheel}")
        digest = file_sha256(wheel)
        expected = metadata.get("harness-wheel-sha256")
        if digest != expected or digest != manifest["wheel_sha256"]:
            errors.append(f"{path}: wheel digest mismatch")
        if manifest["harness_ref"] != harness_ref:
            errors.append(f"{path}: harness-ref disagrees with manifest")
        activation = re.search(
            rf'activate_harness\(\s*"{re.escape(harness_ref)}",\s*'
            rf'"{re.escape(expected)}"',
            text,
        )
        if activation is None:
            errors.append(
                f"{path}: centralized harness activation does not carry "
                "the exact chapter digest"
            )
    manifest_paths = (ROOT / "artifacts" / "harness").glob("*/manifest.json")
    for manifest_path in sorted(manifest_paths):
        manifest = read_yaml(manifest_path)
        wheel = manifest_path.parent / manifest["wheel"]
        if not wheel.exists():
            errors.append(f"{manifest['harness_ref']}: missing wheel {wheel}")
        elif file_sha256(wheel) != manifest["wheel_sha256"]:
            errors.append(f"{manifest['harness_ref']}: manifest wheel digest mismatch")
        validate_source_identity(
            manifest["harness_ref"],
            manifest["source"],
            errors,
            tagged,
            content_addressed,
        )

    fail_if(errors)
    print(
        "harness pins: pass "
        f"({len(content_addressed)} historical SHA identities; "
        f"{len(tagged)} annotated source identity)"
    )


if __name__ == "__main__":
    main()

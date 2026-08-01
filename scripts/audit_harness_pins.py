"""Validate chapter harness metadata, wheel digests, and publication state."""

from __future__ import annotations

import subprocess
import re

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


def main() -> None:
    errors = []
    pending = []
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
        if manifest["source"]["commit"] is None or manifest["source"]["annotated_tag"] is None:
            pending.append(f"{harness_ref}: source commit/tag pending publication authority")

    fail_if(errors)
    print("harness pins: pass")
    for message in pending:
        print(f"PUBLICATION BLOCKER: {message}")


if __name__ == "__main__":
    main()

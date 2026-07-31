"""Validate claim contracts, artifacts, and payload digests."""

from __future__ import annotations

from _audit_utils import ROOT, front_matter, payload_sha256, read_yaml, fail_if


def main() -> None:
    contract = read_yaml(ROOT / "contracts" / "claims.yml")
    claims = {item["claim_id"]: item for item in contract["claims"]}
    errors = []

    for path in sorted((ROOT / "chapters").rglob("*.qmd")):
        metadata = front_matter(path.read_text())
        for claim_id in metadata.get("claim_ids", []):
            if claim_id not in claims:
                errors.append(f"{path}: undeclared claim {claim_id}")

    for claim_id, claim in claims.items():
        evidence = ROOT / claim["evidence"]
        if not evidence.exists():
            errors.append(f"{claim_id}: missing evidence {evidence}")
            continue
        if evidence.suffix != ".json":
            continue
        artifact = read_yaml(evidence)
        for field in (
            "claim_id",
            "phenomenon_id",
            "chapter",
            "provenance_class",
            "hypothesis",
            "result",
            "payload_sha256",
        ):
            if field not in artifact:
                errors.append(f"{claim_id}: artifact missing {field}")
        if artifact.get("claim_id") != claim_id:
            errors.append(f"{claim_id}: artifact ID mismatch")
        if artifact.get("payload_sha256") != payload_sha256(artifact):
            errors.append(f"{claim_id}: payload digest mismatch")

    fail_if(errors)
    print("claims: pass")


if __name__ == "__main__":
    main()

"""Run the deterministic source and contract audits."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
AUDITS = [
    "audit_public_voice.py",
    "audit_branding.py",
    "audit_threads.py",
    "audit_notation_covenant.py",
    "audit_seeds.py",
    "audit_plan_code.py",
    "audit_editorial_contracts.py",
    "audit_diagnostic_cards.py",
    "audit_harness_pins.py",
    "audit_claims.py",
    "audit_sibling_anchors.py",
    "audit_reader_routes.py",
    "audit_book_structure.py",
    "audit_release_identity.py",
]


def main() -> None:
    for audit in AUDITS:
        print(f"\n== {audit} ==", flush=True)
        subprocess.run([sys.executable, str(ROOT / "scripts" / audit)], check=True)
    print("\nfast audits: pass")


if __name__ == "__main__":
    main()

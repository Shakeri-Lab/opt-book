"""Verify the C13 conditional-regime witness."""
from hashlib import sha256
import json
from pathlib import Path
import sys
import numpy as np
from _evidence_verify import verify_claim

root = Path(__file__).resolve().parents[1]; mp = root / "artifacts/harness/ch-13/manifest.json"
manifest = json.loads(mp.read_text()); wheel = mp.parent / manifest["wheel"]; digest = sha256(wheel.read_bytes()).hexdigest(); assert digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))
from trainable_harness import scalar_quadratic_regime, two_point_clipping_audit

record = {"schema_version": 1, "claim_id": "c13-regime-001", "phenomenon_id": "c13-mean-not-regime", "chapter": "c13", "provenance_class": "a", "hypothesis": "Unbiased estimators with the same conditional mean can imply opposite one-step behavior.", "hardware_claim_boundary": "Exact scalar expectation; no claim about a particular workload.", "harness_ref": "ch-13", "harness_wheel_sha256": digest, "result": {"low_noise": scalar_quadratic_regime(1, .5, .25).__dict__, "high_noise": scalar_quadratic_regime(1, .5, 4).__dict__, "clip": two_point_clipping_audit(np.array([-9., 19/9]), np.array([.1, .9]), 2.)}}
verify_claim("c13-regime-001.json", record, absolute_tolerance=0.0)

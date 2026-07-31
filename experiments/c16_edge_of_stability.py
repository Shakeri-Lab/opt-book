"""Verify the C16 moving-curvature trajectory."""
from hashlib import sha256
import json
from pathlib import Path
import sys
import numpy as np
from _evidence_verify import verify_claim

root = Path(__file__).resolve().parents[1]; mp = root / "artifacts/harness/ch-16/manifest.json"
manifest = json.loads(mp.read_text()); wheel = mp.parent / manifest["wheel"]; digest = sha256(wheel.read_bytes()).hexdigest(); assert digest == manifest["wheel_sha256"]
sys.path.insert(0, str(wheel.resolve()))
from trainable_harness import moving_curvature_trace
trace = moving_curvature_trace(np.zeros(2), .2, 350)
record = {"schema_version": 1, "claim_id": "c16-moving-boundary-001", "phenomenon_id": "c16-moving-boundary", "chapter": "c16", "provenance_class": "a", "hypothesis": "A trajectory can begin below the fixed quadratic boundary and later enter a nonmonotone moving-curvature regime.", "hardware_claim_boundary": "Laptop-CPU two-parameter witness; not a scale claim about deep networks.", "harness_ref": "ch-16", "harness_wheel_sha256": digest, "result": {"step_size": .2, "threshold": 10., "first_crossing_step": int(np.argmax(trace.top_curvatures > 10)), "initial_top_curvature": float(trace.top_curvatures[0]), "maximum_top_curvature": float(trace.top_curvatures.max()), "number_loss_increases": int(np.sum(np.diff(trace.losses) > 0)), "final_loss": float(trace.losses[-1])}}
verify_claim("c16-moving-boundary-001.json", record, absolute_tolerance=1e-12)

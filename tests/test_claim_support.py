from __future__ import annotations

from book_support.claims import activate_harness, verify_claim
from book_support.incident_panel import incident_figure


def test_claim_verifier_checks_registered_payload() -> None:
    claim = verify_claim("c01-roofline-001")
    assert claim["phenomenon_id"] == "c01-count-not-cost"


def test_harness_activation_and_claim_agree() -> None:
    pin = activate_harness(
        "ch-13",
        "3204162cec10360dc6beea83cd1fae19c790772b61a20004a496942ffbc9aacf",
    )
    claim = verify_claim("c13-regime-001", expected_harness=pin)
    assert claim["result"]["high_noise"]["expected_next_loss"] == 0.625


def test_incident_panel_has_six_instruments() -> None:
    claim = verify_claim("coda-incident-001")
    figure = incident_figure(claim["result"])
    assert len(figure.axes) == 6

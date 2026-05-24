"""Smoke tests for meok-eu-aia-art-9-rms-mcp."""
import sys, os, inspect, traceback
os.environ.setdefault("MEOK_HMAC_SECRET", "test-only-secret")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    start_rms,
    identify_risk,
    map_mitigation,
    log_post_market_observation,
    iterate_rms,
    validate_rms_completeness,
    list_iteration_steps,
    sign_rms_chain,
    _RMS_DOCS,
    _risk_score,
)


def test_risk_score_thresholds():
    assert _risk_score(5, 5) == "critical"
    assert _risk_score(4, 3) == "high"
    assert _risk_score(3, 2) == "medium"
    assert _risk_score(1, 1) == "low"


def test_start_rms_basic():
    _RMS_DOCS.clear()
    r = start_rms("Test System", "1.0.0", "Acme Ltd")
    assert r["rms_id"].startswith("RMS_")
    assert r["rms"]["iteration_number"] == 1


def test_identify_risk_basic():
    _RMS_DOCS.clear()
    rms = start_rms("X", "1.0.0", "Acme")
    r = identify_risk(rms["rms_id"], "Biased hiring recommendations", "discrimination_bias", 4, 4)
    assert r["risk_id"].startswith("R_")
    assert r["risk_score"] == "high"


def test_identify_risk_unknown_category():
    _RMS_DOCS.clear()
    rms = start_rms("X", "1.0.0", "Acme")
    r = identify_risk(rms["rms_id"], "x", "bogus_category", 3, 3)
    assert "error" in r


def test_identify_risk_invalid_severity():
    _RMS_DOCS.clear()
    rms = start_rms("X", "1.0.0", "Acme")
    r = identify_risk(rms["rms_id"], "x", "fundamental_rights", 9, 3)
    assert "error" in r


def test_map_mitigation_reduces_risk():
    _RMS_DOCS.clear()
    rms = start_rms("X", "1.0.0", "Acme")
    risk = identify_risk(rms["rms_id"], "x", "discrimination_bias", 5, 5)
    m = map_mitigation(rms["rms_id"], risk["risk_id"], "Quarterly bias audit", 2, 2)
    assert m["residual_risk_score"] == "low"
    assert m["accepted"] is True


def test_map_mitigation_residual_critical_not_accepted():
    _RMS_DOCS.clear()
    rms = start_rms("X", "1.0.0", "Acme")
    risk = identify_risk(rms["rms_id"], "x", "safety_physical", 5, 5)
    m = map_mitigation(rms["rms_id"], risk["risk_id"], "Weak mitigation", 5, 5)
    assert m["residual_risk_score"] == "critical"
    assert m["accepted"] is False


def test_log_post_market_observation():
    _RMS_DOCS.clear()
    rms = start_rms("X", "1.0.0", "Acme")
    r = log_post_market_observation(rms["rms_id"], "User reported false positive", "user_report")
    assert r["observation_id"].startswith("OBS_")


def test_iterate_rms_increments():
    _RMS_DOCS.clear()
    rms = start_rms("X", "1.0.0", "Acme")
    r = iterate_rms(rms["rms_id"])
    assert r["new_iteration_number"] == 2


def test_validate_flags_no_risks():
    _RMS_DOCS.clear()
    rms = start_rms("X", "1.0.0", "Acme")
    v = validate_rms_completeness(rms["rms_id"])
    assert v["complete"] is False
    assert any("no risks identified" in i for i in v["issues"])


def test_validate_complete_after_mitigation():
    _RMS_DOCS.clear()
    rms = start_rms("X", "1.0.0", "Acme")
    for cat in ["discrimination_bias", "data_protection", "safety_physical", "human_oversight_failure"]:
        risk = identify_risk(rms["rms_id"], f"risk-{cat}", cat, 3, 3)
        map_mitigation(rms["rms_id"], risk["risk_id"], "mitigation", 2, 2)
    v = validate_rms_completeness(rms["rms_id"])
    assert v["complete"] is True


def test_list_iteration_steps():
    r = list_iteration_steps()
    assert len(r["iteration_steps"]) == 4
    assert "fundamental_rights" in r["risk_categories"]


def test_sign_rms_chain():
    _RMS_DOCS.clear()
    rms = start_rms("X", "1.0.0", "Acme")
    r = sign_rms_chain(rms["rms_id"])
    assert r["attestation_id"].startswith("RMS_ATT_")


if __name__ == "__main__":
    g = dict(globals())
    fns = [v for k, v in g.items() if k.startswith("test_") and inspect.isfunction(v)]
    p = f = 0
    for fn in fns:
        try:
            fn(); print(f"OK {fn.__name__}"); p += 1
        except Exception as e:
            print(f"X  {fn.__name__}: {type(e).__name__}: {e}"); traceback.print_exc(); f += 1
    print(f"\n{p} passed, {f} failed")

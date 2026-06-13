#!/usr/bin/env python3
"""
MEOK EU AI Act Article 9 Risk Management System MCP
=====================================================

By MEOK AI Labs · https://meok.ai · MIT
<!-- mcp-name: io.github.CSOAI-ORG/meok-eu-aia-art-9-rms-mcp -->

WHAT THIS DOES
--------------
EU AI Act Article 9 requires providers of high-risk AI systems to establish,
implement, document, and maintain a **Risk Management System (RMS)** —
continuous iterative process across the entire system lifecycle.

Article 9(2) defines the 4 mandatory iterations:
  (a) identification + analysis of known + reasonably foreseeable risks
  (b) estimation + evaluation of risks during intended use + misuse
  (c) evaluation of other risks based on post-market monitoring data
  (d) adoption of appropriate, targeted risk-management measures

This MCP auto-generates a structured RMS document, validates completeness,
maps risks to mitigation measures, and signs the RMS for the Annex IV
technical documentation bundle.

Provider-side companion to:
  - meok-eu-ai-act-art-13-ifu-mcp (Article 13 IFU)
  - ai-bom-mcp (Annex IV technical documentation)
  - bias-detection-mcp (Article 10 data governance)
  - meok-eu-ai-act-art-26-fria-mcp (deployer FRIA)

TOOLS
-----
- start_rms(system_name, system_version, risk_categories)
- identify_risk(rms_id, risk_description, severity, likelihood, category)
- map_mitigation(rms_id, risk_id, mitigation_action, residual_severity)
- log_post_market_observation(rms_id, observation, source)
- iterate_rms(rms_id, iteration_number, new_data): rerun the loop
- validate_rms_completeness(rms_id): pre-audit check
- sign_rms_chain(rms_id, signer_role): HMAC-signed attestation

PRICING
-------
Free MIT self-host · £29/mo Starter · Governance Substrate £499/mo · £1,500/mo Enterprise.
"""

from __future__ import annotations
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timezone
from typing import Optional
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("meok-eu-aia-art-9-rms")
_HMAC_SECRET = os.environ.get("MEOK_HMAC_SECRET", "")
_RMS_DOCS: dict[str, dict] = {}


SPEC = "EU AI Act Article 9 (Regulation (EU) 2024/1689)"

# Article 9(2) iteration steps
ITERATION_STEPS = [
    ("a_identification", "Identification + analysis of known + reasonably foreseeable risks"),
    ("b_estimation_evaluation", "Estimation + evaluation of risks during intended use + misuse"),
    ("c_post_market_evaluation", "Evaluation of other risks based on post-market monitoring data"),
    ("d_mitigation_measures", "Adoption of appropriate, targeted risk-management measures"),
]

# Common risk categories per Annex III
RISK_CATEGORIES = [
    "fundamental_rights",
    "discrimination_bias",
    "safety_physical",
    "safety_psychological",
    "fraud_misuse",
    "data_protection",
    "operational_reliability",
    "interpretability_transparency",
    "human_oversight_failure",
    "environmental_impact",
    "economic_harm",
    "supply_chain",
]


def _sign(payload: dict) -> str:
    if not _HMAC_SECRET:
        return "unsigned-no-key-configured"
    return hmac.new(_HMAC_SECRET.encode(), json.dumps(payload, sort_keys=True).encode(), hashlib.sha256).hexdigest()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def _risk_score(severity: int, likelihood: int) -> str:
    """Convert severity (1-5) × likelihood (1-5) into qualitative score."""
    s = severity * likelihood
    if s >= 20: return "critical"
    if s >= 12: return "high"
    if s >= 6:  return "medium"
    return "low"


# ──────────────────────────────────────────────────────────────────────
# Tools
# ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def start_rms(
    system_name: str,
    system_version: str,
    provider_legal_name: str,
    risk_categories: Optional[list[str]] = None,
) -> dict:
    """
    Initialise a new Article 9 Risk Management System document.

    Args:
        system_name: Name of the high-risk AI system.
        system_version: Semver.
        provider_legal_name: Legal entity name of the provider.
        risk_categories: Categories of risk in scope (defaults to all).

    Returns:
        {rms_id, rms, next_step}
    """
    rms_id = f"RMS_{int(time.time())}_{os.urandom(4).hex()}"
    rms = {
        "rms_id": rms_id,
        "spec": SPEC,
        "system_name": system_name,
        "system_version": system_version,
        "provider_legal_name": provider_legal_name,
        "risk_categories_in_scope": risk_categories or RISK_CATEGORIES,
        "iteration_number": 1,
        "risks": [],
        "mitigations": [],
        "post_market_observations": [],
        "iterations_log": [
            {"iteration": 1, "started_at": _ts(), "trigger": "initial_design_phase"}
        ],
        "created_at": _ts(),
        "status": "active",
    }
    _RMS_DOCS[rms_id] = rms
    return {
        "rms_id": rms_id,
        "rms": rms,
        "next_step": f"Call identify_risk(rms_id='{rms_id}', ...) for each risk you can foresee.",
    }


@mcp.tool()
def identify_risk(
    rms_id: str,
    risk_description: str,
    category: str,
    severity: int,
    likelihood: int,
    affected_parties: Optional[list[str]] = None,
) -> dict:
    """
    Add an identified risk to the RMS (Article 9(2)(a)).

    Args:
        rms_id: From start_rms().
        risk_description: Free-text description of the risk.
        category: One of the catalogued RISK_CATEGORIES.
        severity: 1-5 (negligible → catastrophic).
        likelihood: 1-5 (rare → almost certain).
        affected_parties: List of affected groups.

    Returns:
        {risk_id, risk_score, next_step}
    """
    if rms_id not in _RMS_DOCS:
        return {"error": "unknown_rms"}
    if not 1 <= severity <= 5 or not 1 <= likelihood <= 5:
        return {"error": "severity + likelihood must be 1-5"}
    if category not in RISK_CATEGORIES:
        return {"error": f"category must be one of {RISK_CATEGORIES}"}

    risk_id = f"R_{int(time.time())}_{os.urandom(3).hex()}"
    risk = {
        "risk_id": risk_id,
        "description": risk_description,
        "category": category,
        "severity": severity,
        "likelihood": likelihood,
        "risk_score": _risk_score(severity, likelihood),
        "affected_parties": affected_parties or [],
        "identified_at": _ts(),
        "status": "open",
    }
    _RMS_DOCS[rms_id]["risks"].append(risk)
    return {
        "risk_id": risk_id,
        "risk_score": risk["risk_score"],
        "next_step": f"Call map_mitigation(rms_id='{rms_id}', risk_id='{risk_id}', mitigation_action='...') to bring score below threshold.",
    }


@mcp.tool()
def map_mitigation(
    rms_id: str,
    risk_id: str,
    mitigation_action: str,
    residual_severity: int,
    residual_likelihood: int,
    owner: Optional[str] = None,
) -> dict:
    """
    Map a mitigation to an identified risk (Article 9(2)(d)).

    Args:
        rms_id: From start_rms().
        risk_id: From identify_risk().
        mitigation_action: Description of the mitigation.
        residual_severity: 1-5 severity after mitigation.
        residual_likelihood: 1-5 likelihood after mitigation.
        owner: Person/team responsible for the mitigation.

    Returns:
        {mitigation_id, residual_risk_score, accepted}
    """
    if rms_id not in _RMS_DOCS:
        return {"error": "unknown_rms"}
    rms = _RMS_DOCS[rms_id]
    risk = next((r for r in rms["risks"] if r["risk_id"] == risk_id), None)
    if not risk:
        return {"error": "unknown_risk"}

    mitigation_id = f"M_{int(time.time())}_{os.urandom(3).hex()}"
    mitigation = {
        "mitigation_id": mitigation_id,
        "risk_id": risk_id,
        "action": mitigation_action,
        "residual_severity": residual_severity,
        "residual_likelihood": residual_likelihood,
        "residual_risk_score": _risk_score(residual_severity, residual_likelihood),
        "owner": owner or "<unassigned>",
        "applied_at": _ts(),
    }
    rms["mitigations"].append(mitigation)
    risk["status"] = "mitigated"
    risk["mitigation_id"] = mitigation_id

    # Accepted if residual is low/medium; otherwise needs further mitigation
    accepted = mitigation["residual_risk_score"] in ("low", "medium")
    return {
        "mitigation_id": mitigation_id,
        "residual_risk_score": mitigation["residual_risk_score"],
        "accepted": accepted,
        "next_step": (
            "Risk accepted. Continue to next identified risk."
            if accepted
            else "Residual still high/critical — call map_mitigation again with a stronger action."
        ),
    }


@mcp.tool()
def log_post_market_observation(
    rms_id: str,
    observation: str,
    source: str,
    severity_change: Optional[int] = None,
) -> dict:
    """
    Log a post-market observation per Article 9(2)(c) + Article 72.

    Args:
        rms_id: From start_rms().
        observation: What was observed in the field.
        source: Source of the observation (user_report, monitoring_metric, incident_relay, etc.).
        severity_change: Optional severity delta (-2 to +2).

    Returns:
        {observation_id, queued_for_next_iteration}
    """
    if rms_id not in _RMS_DOCS:
        return {"error": "unknown_rms"}
    obs_id = f"OBS_{int(time.time())}_{os.urandom(3).hex()}"
    obs = {
        "observation_id": obs_id,
        "observation": observation,
        "source": source,
        "severity_change": severity_change,
        "logged_at": _ts(),
    }
    _RMS_DOCS[rms_id]["post_market_observations"].append(obs)
    return {
        "observation_id": obs_id,
        "queued_for_next_iteration": True,
        "next_step": f"Call iterate_rms(rms_id='{rms_id}') when ready to fold observations into the next iteration.",
    }


@mcp.tool()
def iterate_rms(rms_id: str, trigger: str = "post_market_review") -> dict:
    """
    Re-run the Article 9 loop with new data (iteration tracking).

    Args:
        rms_id: From start_rms().
        trigger: Why this iteration runs.

    Returns:
        {new_iteration_number, prior_risks_count, observations_to_review}
    """
    if rms_id not in _RMS_DOCS:
        return {"error": "unknown_rms"}
    rms = _RMS_DOCS[rms_id]
    rms["iteration_number"] += 1
    rms["iterations_log"].append({
        "iteration": rms["iteration_number"],
        "started_at": _ts(),
        "trigger": trigger,
    })
    return {
        "new_iteration_number": rms["iteration_number"],
        "prior_risks_count": len(rms["risks"]),
        "observations_to_review": len(rms["post_market_observations"]),
        "next_step": "Re-run identify_risk() for any new risks; map_mitigation() for any residual high/critical risks.",
    }


@mcp.tool()
def validate_rms_completeness(rms_id: str) -> dict:
    """
    Pre-audit check of the RMS — Article 9 completeness.

    Args:
        rms_id: From start_rms().

    Returns:
        {complete, score_0_100, issues, recommendations}
    """
    if rms_id not in _RMS_DOCS:
        return {"error": "unknown_rms"}
    rms = _RMS_DOCS[rms_id]
    issues = []
    recs = []

    if not rms["risks"]:
        issues.append("no risks identified — Art 9(2)(a) requires foreseeable-risk inventory")
    unmitigated = [r for r in rms["risks"] if r["status"] != "mitigated"]
    if unmitigated:
        issues.append(f"{len(unmitigated)} risks have no mitigation mapped — Art 9(2)(d) requires measures for every identified risk")
    critical_residuals = [m for m in rms["mitigations"] if m["residual_risk_score"] == "critical"]
    if critical_residuals:
        issues.append(f"{len(critical_residuals)} mitigations leave residual risk at CRITICAL — system may not be placed on market")
    if rms["iteration_number"] < 2 and rms["post_market_observations"]:
        recs.append("Post-market observations logged but no second iteration run — call iterate_rms()")
    if len(rms["risks"]) < 3:
        recs.append("Only a handful of risks identified — most production systems should have 10-30 catalogued")

    base = 100
    base -= 10 * len(issues)
    base -= 3 * len(recs)
    score = max(0, base)

    return {
        "complete": len(issues) == 0,
        "score_0_100": score,
        "issues": issues,
        "recommendations": recs,
        "risks_count": len(rms["risks"]),
        "mitigations_count": len(rms["mitigations"]),
        "iterations": rms["iteration_number"],
    }


@mcp.tool()
def list_iteration_steps() -> dict:
    """Return the 4 Article 9(2) iteration steps."""
    return {
        "spec": SPEC,
        "iteration_steps": [{"key": k, "description": d} for k, d in ITERATION_STEPS],
        "risk_categories": RISK_CATEGORIES,
    }


@mcp.tool()
def sign_rms_chain(rms_id: str, signer_role: str = "provider_chief_risk_officer") -> dict:
    """HMAC-sign the RMS for the Annex IV technical documentation bundle."""
    if rms_id not in _RMS_DOCS:
        return {"error": "unknown_rms"}
    rms = _RMS_DOCS[rms_id]
    att_id = f"RMS_ATT_{int(time.time())}_{os.urandom(4).hex()}"
    sealed = {
        "attestation_id": att_id,
        "spec": SPEC,
        "signer_role": signer_role,
        "rms_doc": rms,
        "sealed_at": _ts(),
        "issuer": "MEOK AI Labs (CSOAI LTD)",
    }
    sig = _sign(sealed)
    return {
        "attestation_id": att_id,
        "signature": sig,
        "sealed_at": sealed["sealed_at"],
        "verify_url": f"https://meok-attestation-api.vercel.app/verify/{att_id}",
        "retention_hint": "Retain for system lifetime + 6 years (Art 18). Mandatory part of the Annex IV technical documentation bundle.",
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()


# ── MEOK monetization layer (Stripe upgrade · PAYG · pricing) ──────────
# Free tier is zero-config. Upgrade to Pro (unlimited) or pay-as-you-go per call.
import os as _meok_os
MEOK_STRIPE_UPGRADE = "https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t"  # Pro (unlimited)
MEOK_PAYG_KEY = _meok_os.environ.get("MEOK_PAYG_KEY", "")  # set to enable PAYG (x402 / ~GBP0.05 per call)
MEOK_PRICING = "https://meok.ai/pricing"


def meok_upsell(tier: str = "free") -> dict:
    """Monetization options for free-tier callers: Pro upgrade, PAYG, or pricing page."""
    if tier != "free":
        return {}
    return {"upgrade_url": MEOK_STRIPE_UPGRADE,
            "payg_enabled": bool(MEOK_PAYG_KEY),
            "pricing": MEOK_PRICING}

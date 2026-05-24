# MEOK EU AI Act Article 9 RMS Generator MCP

> ## 🧱 Part of the MEOK Governance Substrate (£499/mo) + Enterprise (£1,500/mo)
> See [meok.ai/governance](https://meok.ai/governance).

# Generate + iterate Risk Management Systems per Article 9 — provider-side

<!-- mcp-name: io.github.CSOAI-ORG/meok-eu-aia-art-9-rms-mcp -->

[![PyPI](https://img.shields.io/pypi/v/meok-eu-aia-art-9-rms-mcp)](https://pypi.org/project/meok-eu-aia-art-9-rms-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## What this does

**EU AI Act Article 9** requires providers of high-risk AI systems to establish + maintain a **Risk Management System (RMS)** as a continuous iterative process across the entire system lifecycle. **Article 9(2)** defines 4 mandatory iteration steps.

This MCP generates structured RMS docs, maps risks to mitigations, logs post-market observations, runs lifecycle iterations, and signs everything for the **Annex IV technical documentation bundle** (which DG-CNECT requires on every audit).

Completes the **provider-side compliance triple**:
- `meok-eu-aia-art-9-rms-mcp` — this MCP (Risk Management System)
- `meok-eu-ai-act-art-13-ifu-mcp` — Instructions for Use
- `ai-bom-mcp` — Annex IV technical documentation

## Tools

| Tool | Purpose |
|---|---|
| `start_rms(system_name, system_version, provider_legal_name, risk_categories?)` | Initialise RMS |
| `identify_risk(rms_id, description, category, severity, likelihood, affected_parties?)` | Add risk (Art 9(2)(a)) |
| `map_mitigation(rms_id, risk_id, mitigation_action, residual_severity, residual_likelihood, owner?)` | Mitigate (Art 9(2)(d)) |
| `log_post_market_observation(rms_id, observation, source, severity_change?)` | Art 9(2)(c) |
| `iterate_rms(rms_id, trigger?)` | Re-run the loop |
| `validate_rms_completeness(rms_id)` | Pre-audit check |
| `list_iteration_steps()` | The 4 Art 9(2) steps + 12 risk categories |
| `sign_rms_chain(rms_id, signer_role)` | HMAC-signed attestation |

## Article 9(2) — 4 mandatory steps

(a) identification + analysis · (b) estimation + evaluation · (c) post-market evaluation · (d) targeted mitigation measures.

## 12 risk categories catalogued

`fundamental_rights` · `discrimination_bias` · `safety_physical` · `safety_psychological` · `fraud_misuse` · `data_protection` · `operational_reliability` · `interpretability_transparency` · `human_oversight_failure` · `environmental_impact` · `economic_harm` · `supply_chain`

## Sister MCPs

- `meok-eu-ai-act-art-13-ifu-mcp` — Article 13 IFU (provider side)
- `meok-eu-ai-act-art-26-fria-mcp` — Article 26(9) FRIA (deployer side)
- `ai-bom-mcp` — Annex IV technical documentation
- `bias-detection-mcp` — Article 10 data governance
- `agent-incident-relay-mcp` — Article 73 5-clock broadcaster (feeds post-market observations)

Full catalogue: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

## Pricing

| Option | Price |
|---|---|
| Self-host MIT | £0 |
| Universal PAYG | £29/mo + £0.0002/call |
| Governance Substrate | £499/mo |
| **Enterprise (custom risk taxonomy)** | **£1,500/mo** |
| Defence | £4,990/mo |

Buy: https://meok.ai/governance

## Wire it up — full stack

See [meok.ai/mcp-stack](https://meok.ai/mcp-stack).

## Licence

MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677).

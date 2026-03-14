# ABUSE RESPONSE PLAYBOOK — World Transparency Graph (WTG)

Policy-Version: v1.0.0  
Effective-Date: 2026-02-28  
Owner: WTG Governance Team

## Non-contractual operational guidance

This playbook is internal operational guidance.  
It does not create contractual duties, guaranteed outcomes, or third-party rights.

## Incident severity matrix

- Severity 1 (Critical): active abuse with high harm potential (doxxing/extortion/automation abuse at scale).
- Severity 2 (High): repeated policy violations or targeted misuse.
- Severity 3 (Medium): isolated violations, low immediate harm.
- Severity 4 (Low): suspicious behavior needing monitoring only.

## Triage and response actions

Minimum triage steps:

1. Capture incident metadata and timestamps.
2. Classify severity.
3. Preserve relevant logs and evidence.
4. Apply proportional controls (rate-limit, temporary block, access suspension).

Response controls:

- Request throttling.
- Key/token rotation where applicable.
- Repository and endpoint restrictions.
- Formal incident note in governance logs.

All controls are applied on a best-effort basis, proportional to observed risk and legal constraints.

## Escalation path and evidence retention

Escalation route:

1. Maintainer triage.
2. Governance/legal review for high-impact cases.
3. External escalation only when legally required.

Evidence retention:

- Retain incident evidence for the minimum period needed for response, legal obligations, and auditability.
- Keep evidence access restricted to authorized maintainers.

Related policy documents:

- [ETHICS.md](ETHICS.md)
- [TERMS.md](TERMS.md)
- [PRIVACY.md](PRIVACY.md)

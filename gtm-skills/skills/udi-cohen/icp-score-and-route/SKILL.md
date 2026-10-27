---
name: icp-score-and-route
title: ICP score and route
description: |
  Score any lead or account against your ICP criteria, verify key contacts via
  Lusha, and return a routing recommendation — AE, SDR, or nurture — with a
  confidence level and the specific data points that drove the decision. Runs
  on a single lead or across a full list in one pass. Requires a Lusha
  connection.
category: RevOps
tags: [RevOps, ICP]
---

Score any lead or account against a defined ICP. Verify key
contacts via Lusha. Return a routing recommendation with
transparent reasoning — no black-box grades, no unexplained
decisions.

## Input

The user will provide via $ARGUMENTS:

- Lead or account list (required) — one or more company names,
  domains, or Lusha company IDs.
- ICP criteria (required) — the scoring dimensions to use.
  Examples:
  - Industry: SaaS, FinTech, Healthcare
  - Employee count: 200–2,000
  - Geography: North America, EMEA
  - Funding stage: Series A–C
  - Tech stack: Salesforce, HubSpot, Outreach
  - Buying signals: intent on your category, score 60+
  If ICP criteria are not supplied, ask once. If declined,
  use general B2B SaaS ICP defaults and state that assumption.
- Routing thresholds (optional) — what score maps to which
  route. Default:
  - 80–100: AE
  - 50–79: SDR
  - Below 50: nurture
  Accept custom thresholds if supplied.

## Workflow

1. Anchor on the ICP.
   Read the ICP criteria and routing thresholds from $ARGUMENTS.
   Restate them at the top of the output so the reader knows
   exactly what the scoring was based on. If defaults were used,
   flag them clearly.

2. Resolve accounts via Lusha.
   For each lead or account:
   - If a Lusha company ID is supplied, use it directly.
   - Otherwise resolve via companies_search using the name
     or domain.
   - Flag any accounts that could not be resolved and skip them.

3. Pull data in parallel.
   For each resolved account, run these calls concurrently:
   - Firmographics: industry, employee count, revenue range,
     HQ geography, funding stage.
   - Tech stack signals: technologies in use relevant to ICP.
   - Buying signals: intent topics, signal score 60+.
   - Key contacts: most senior contact in the primary buying
     function. Verify email and direct dial via Lusha.

4. Score against ICP criteria.
   For each scoring dimension, return one of:
   - Met — data confirms the criterion is satisfied
   - Missed — data confirms the criterion is not satisfied
   - Uncertain — data is insufficient to confirm either way

   Calculate an overall ICP score (0–100) based on the
   weighted criteria. Weight buying signals and firmographic
   fit highest. Tech stack and geography as secondary signals.

   Show the score breakdown — not just the total. Every
   dimension visible, every gap flagged.

5. Apply routing thresholds.
   Map the ICP score to a routing recommendation:
   - AE: account meets ICP threshold, verified contact found,
     buying signal present. High-confidence handoff.
   - SDR: account meets partial ICP, or ICP met but no buying
     signal. Needs qualification before AE handoff.
   - Nurture: account misses ICP on core dimensions. Not ready
     for outreach. Flag the specific gaps.

   State the confidence level: High / Medium / Low.
   High: 3+ criteria confirmed, verified contact found.
   Medium: mixed signals, some criteria uncertain.
   Low: insufficient data or core criteria missed.

6. Return the routing output.
   One record per lead or account. Lead with the routing
   decision, follow with the score breakdown and reasoning.
   End with the verified contact details for AE and SDR routes.

## Output Format

### ICP Score and Route

ICP criteria used: [list the criteria and thresholds]
Routing thresholds: AE [score], SDR [score], Nurture [score]
Leads scored: [n]

---

For each lead or account:

**[Company Name]**
Routing: [AE / SDR / Nurture] — Confidence: [High / Medium / Low]
ICP Score: [0–100]

| Criterion | Value Found | Status |
|---|---|---|
| Industry | | Met / Missed / Uncertain |
| Employee count | | Met / Missed / Uncertain |
| Geography | | Met / Missed / Uncertain |
| Funding stage | | Met / Missed / Uncertain |
| Tech stack | | Met / Missed / Uncertain |
| Buying signal | | Met / Missed / Uncertain |

**Routing rationale:** [2–3 sentences explaining the decision —
which criteria drove it, which gaps exist, and what needs to
happen before the routing changes.]

**Verified contact:**
- Name: [initials only — e.g. J.K.]
- Title:
- Email: [domain only — j.k@[company].com]
- Direct dial: [masked — +1 415 555 ••••]
- Contact confirmed live via Lusha connector, [date]

*For nurture routes: omit verified contact. Return the specific
ICP gaps that need to close before re-scoring.*

---

### Unresolved Accounts

Accounts that could not be matched in Lusha:
[list of account names or domains]

Recommend verifying company name or domain and re-running.

---

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/icp-score-and-route-skill/

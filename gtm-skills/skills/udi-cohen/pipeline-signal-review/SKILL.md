---
name: pipeline-signal-review
title: Pipeline signal review
description: |
  Run a full signal check across every open deal in a pipeline. Takes a deal
  list with account names and stages. Returns a risk-ranked brief — stale
  contacts, missing buying group coverage, signal gaps, and a recommended next
  action for every deal that needs attention. Requires a Lusha connection.
category: RevOps
tags: [RevOps, Sales]
---

Run a full signal check across every open deal in a pipeline.
Rank deals by risk. Verify key contacts are still in seat.
Flag buying group gaps. Surface signals that change the deal
picture. Return a brief the rep or manager can act on before
the weekly review.

## Input

The user will provide via $ARGUMENTS:

- Deal list (required) — a list of open deals. For each deal:
  - Account name or domain (required)
  - Deal stage (required) — e.g. Stage 1, Discovery, Proposal,
    Negotiation, Pre-close
  - Key contacts (optional) — named contacts to verify per deal
  - Deal value (optional) — used to weight risk scoring
- Review context (optional) — what this review is for. Examples:
  - "weekly pipeline review — flag everything at risk"
  - "end of quarter audit — focus on deals in Stage 3+"
  - "manager 1:1 — inspect rep's full pipeline"

  If deal list is missing, ask once. If declined, return an
  error — the skill cannot run without a list of deals.

## Workflow

1. Anchor on the review context.
   Read the review context and deal list from $ARGUMENTS.
   Default to full pipeline risk review if no context supplied.
   State the parameters at the top of the output.

2. Resolve accounts via Lusha.
   For each deal in the list:
   - Resolve the account via companies_search using the name
     or domain.
   - Flag any accounts that could not be resolved and skip them.

3. Pull signals and verify contacts in parallel.
   For each resolved account, run these calls concurrently:
   - Contact verification: confirm key contacts are still in
     seat. Flag departures, role changes, and tenure risks.
     If no key contacts supplied, identify and verify the most
     senior contact in the primary buying function automatically.
   - Buying group coverage: check for verified contacts across
     all key buying roles — Champion, Economic Buyer, Technical
     Evaluator, Procurement. Flag missing roles.
   - Buying signals: intent topics, signal score 60+. Flag
     anything that changes the deal picture — intent on a
     competitor's category, intent on your category dropping.
   - Recent news and scoops: last 30 days. Leadership moves,
     funding, layoffs, budget signals, product launches.
   - Activity gap: flag any deal with no noted activity in
     30+ days as stale.

4. Score each deal by risk.
   Assign each deal a risk score based on:
   - Contact verification status — departed champion: high risk
   - Buying group coverage gaps — missing Economic Buyer at
     Stage 3+: high risk
   - Activity gap — no activity in 30+ days: medium risk
   - Negative signals — layoffs, budget cuts, competitor intent:
     high risk
   - Deal stage vs. signal alignment — late stage deal with no
     buying signals: medium risk
   - Deal value — weight higher-value deals more heavily

   Rank deals: At Risk (H) → Needs Attention (M) → On Track (L)

5. Write the pipeline brief.
   Lead with a summary: total deals reviewed, at-risk count,
   needs-attention count, on-track count, and the single most
   urgent action across the whole pipeline this week.
   Then the ranked deal list.

## Output Format

### Pipeline Review Brief

Review context: [restate in one line]
Deals reviewed: [n]
At risk: [n]
Needs attention: [n]
On track: [n]
Most urgent action: [one line — the single most important
action across the whole pipeline right now]

---

### At Risk Deals

For each at-risk deal, ranked by risk score:

**[Account Name]** — Stage: [stage] | Risk: High

| Risk Factor | Detail | Recommended Action |
|---|---|---|

Key contact status: [verified in seat / departed / unverifiable]
Buying group gaps: [missing roles, if any]
Next action: [one concrete action tied to the highest risk factor]

---

### Needs Attention

For each deal needing attention, ranked by risk score:

**[Account Name]** — Stage: [stage] | Risk: Medium

| Risk Factor | Detail | Recommended Action |
|---|---|---|

Next action: [one concrete action]

---

### On Track

Deals with no significant risk flags this week:
[list of account names and stages]

These deals were checked — nothing material surfaced.

---

### Contact Flags

Contacts who have departed or changed roles across the pipeline:

| Account | Contact | Previous Title | Flag | Recommended Action |
|---|---|---|---|---|

Privacy rules — apply to every row:
- Names: initials only (e.g. J.K.)
- Tag the table: Contacts confirmed live via Lusha connector,
  [date]

---

### Unresolved Accounts

Accounts that could not be matched in Lusha:
[list of account names or domains]

Recommend verifying company name or domain and re-running.

---

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/pipeline-review-skill/

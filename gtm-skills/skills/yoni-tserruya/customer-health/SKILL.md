---
name: customer-health
title: Customer health scan
description: |
  Scan a full book of business for expansion and churn risk signals in one
  pass. Takes a customer account list and returns a ranked brief — expansion
  signals at the top, churn risk flagged for immediate action. Verifies key
  contacts are still in seat and surfaces a recommended action for every
  account that moved. Requires a Lusha connection.
category: Deals
tags: [Sales, CS]
---

Scan a book of business for expansion and churn risk signals.
Rank accounts by signal type and strength. Verify key contacts
are still in seat. Return a brief the CSM or AM can act on
the same day.

## Input

The user will provide via $ARGUMENTS:

- Customer list (required) — a list of company names, domains,
  or Lusha company IDs. Paste inline or reference a saved list.
- Scan focus (optional) — which signals to prioritize.
  Default: both expansion and churn risk. Options:
  - Expansion only — hiring surges, funding, new buying centers,
    intent on adjacent products
  - Churn risk only — leadership changes, budget signals,
    engagement gaps, champion departures
- Lookback window (optional) — how far back to pull signals.
  Default: 30 days. Accept: 7 days, 90 days.
- Key contacts (optional) — a list of named contacts to verify
  per account. If not supplied, the skill identifies and verifies
  the most senior contact in each account automatically.

If customer list is missing, ask once. If declined, return an
error — the skill cannot run without a list of accounts.

## Workflow

1. Anchor on the scan focus.
   Read the scan focus and lookback window from $ARGUMENTS.
   Default to both expansion and churn risk, 30-day lookback,
   if not supplied. State the parameters at the top of the
   output so the reader knows what the scan covers.

2. Resolve accounts via Lusha.
   For each account in the list:
   - If a Lusha company ID is supplied, use it directly.
   - Otherwise resolve via companies_search using the name
     or domain.
   - Flag any accounts that could not be resolved and skip them.
     List unresolved accounts at the end of the output.

3. Pull signals and verify contacts in parallel.
   For each resolved account, run these calls concurrently:
   - Buying signals: intent topics, signal score 60+, ranked
     by score. Lookback window as specified.
   - News and scoops: leadership moves, funding, product
     launches, M&A, layoffs, budget signals.
   - Hiring signals: open roles in functions relevant to
     expansion or churn risk.
   - Contact verification: confirm key contacts are still
     in seat. Flag any departures or role changes.

4. Classify each signal as expansion or churn risk.
   Expansion signals:
   - Funding round or investment announcement
   - Hiring surge in a new function — new buying center
   - Intent on adjacent product categories
   - New executive hire in a relevant function
   - Product launch or market expansion announcement

   Churn risk signals:
   - Key contact departure or role change
   - Layoff announcement or headcount reduction
   - Budget-cut signal or cost-reduction news
   - Leadership change at C-suite or VP level
   - Engagement gap — no activity in 60+ days
   - Intent on a competitor's category

5. Score and rank accounts.
   Assign each account a health score based on:
   - Signal type (expansion vs. churn risk)
   - Signal strength and recency
   - Number of signals found
   - Contact verification status

   Rank order:
   1. Expansion signals — highest score first
   2. Churn risk signals — highest risk first
   3. No signals — list briefly at the end

6. Write the health brief.
   Lead with a summary: how many accounts scanned, how many
   had expansion signals, how many had churn risk signals,
   and the single most important action across the whole
   book this month.

## Output Format

### Customer Health Brief

Period: [start date] — [end date]
Accounts scanned: [n]
Expansion signals: [n accounts]
Churn risk flags: [n accounts]
Top action this month: [one line — the single most important
action across the whole book]

---

### Expansion Signals

For each account with expansion signals, ranked by signal strength:

**[Account Name]** — Expansion score: [H / M / L]

| Signal | Type | Date | Opportunity |
|---|---|---|---|

Key contact status: [verified in seat / departed — see flag]
Recommended action: [one line — what to do with this account
this month, tied to the strongest expansion signal]

---

### Churn Risk Flags

For each account with churn risk signals, ranked by risk level:

**[Account Name]** — Risk level: [H / M / L]

| Signal | Type | Date | Risk |
|---|---|---|---|

Key contact status: [verified in seat / departed — see flag]
Recommended action: [one line — what to do with this account
this month, tied to the strongest risk signal]

---

### Contact Flags

Contacts who have departed or changed roles since last scan:

| Account | Contact | Previous Title | Flag | Recommended Action |
|---|---|---|---|---|

Privacy rules — apply to every row:
- Names: initials only (e.g. J.K.)
- Tag the table: Contacts confirmed live via Lusha connector,
  [date]

---

### No-Signal Accounts

Accounts scanned with no signals in the lookback window:
[list of account names]

These accounts were checked — nothing moved this month.

---

### Unresolved Accounts

Accounts that could not be matched in Lusha:
[list of account names or domains]

Recommend verifying company name or domain and re-running.

---

Example outputs in this skill are illustrative — they reflect the
structure, fields, and format of real Lusha connector output, but
were not pulled from a live session. Run the skill with your own
data and connectors to see live results.

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/customer-health-skill/

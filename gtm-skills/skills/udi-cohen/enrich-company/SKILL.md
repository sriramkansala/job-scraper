---
name: enrich-company
title: Enrich a company
description: |
  Pull any company's full verified profile via Lusha. Takes a company name,
  domain, or Lusha company ID. Returns firmographics, funding stage, tech
  stack, employee count, revenue range, HQ, corporate structure, live buying
  signals, and verified contact count by seniority. Single company lookup —
  complete, verified, ready to act on. Requires a Lusha connection.
category: Research
tags: [Research]
---

Pull a company's full verified profile from Lusha. Return
firmographics, funding, tech stack, live buying signals, and
contact coverage. One company in, one complete profile out.

## Input

The user will provide via $ARGUMENTS one of:

- Company name — resolved via companies_search
- Domain — e.g. acme.com — resolved via companies_search
- Lusha company ID — used directly, skip the search step

If none are supplied, ask once. If the user provides a list
of companies, process them one by one and return a comparison
table at the end.

## Workflow

1. Resolve the company via Lusha.
   - If a Lusha company ID is supplied, use it directly.
   - Otherwise call companies_search with the company name
     or domain. Extract the company ID from the top match.
   - If multiple matches exist, surface the top two and ask
     the user to confirm before continuing.
   - If no match is found, flag it and ask the user to verify
     the company name or try the domain instead.

2. Pull the full profile in parallel.
   Once the company ID is confirmed, run these concurrently:
   - Firmographics: industry, employee count, revenue range,
     HQ, company type, founded year, description
   - Corporate structure: parent company, subsidiaries,
     ultimate parent if applicable
   - Funding: total raised, most recent round, date, amount,
     investors. For public companies: ticker, exchange.
   - Tech stack: technologies in active use
   - Buying signals: all signal types, score 60+, ranked
     by score, last 90 days
   - Contact coverage: total verified contacts in Lusha
     database at this company, broken down by seniority

3. Triage buying signals.
   Keep signals that are recent (last 90 days) and scored
   above 60. Rank by score. Flag the top 3 as most actionable.
   If no signals are found, note it clearly rather than
   omitting the section silently.

4. Return the full profile.
   Lead with the company snapshot. Follow with signals.
   Close with contact coverage so the reader knows what's
   available before they start prospecting.

## Output Format

### Company profile — [Company Name]

| Field | Value |
|---|---|
| Website | |
| Industry | |
| Employees | |
| Revenue range | |
| HQ | |
| Type | Public / Private |
| Founded | |
| Lusha company ID | |

### Corporate structure

- Parent company: [if applicable]
- Ultimate parent: [if applicable]
- Subsidiaries: [if applicable, list up to 5]

### Funding

| Field | Value |
|---|---|
| Total raised | |
| Most recent round | |
| Round date | |
| Round amount | |
| Lead investors | |

For public companies: replace with ticker, exchange, and
market cap where available.

### Tech stack

Technologies confirmed in active use at this company,
relevant to your GTM motion.

[list of technologies]

### Live buying signals

Signals firing at this account right now, ranked by score.
Top 3 flagged as most actionable.

| Signal | Type | Score | Date |
|---|---|---|---|

If no signals above threshold: "No signals above score 60
found for this account in the last 90 days."

### Contact coverage

| Seniority | Verified contacts in Lusha |
|---|---|
| C-suite | |
| VP | |
| Director | |
| Manager | |
| Individual contributor | |
| Total | |

Use this to assess whether Lusha has the contacts you need
before investing time in list building or prospecting.

---

If the user supplies multiple companies, return a summary
comparison table after individual profiles:

| Company | Industry | Employees | Funding stage | Top signal | Lusha contacts |
|---|---|---|---|---|---|

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/enrich-company-skill/

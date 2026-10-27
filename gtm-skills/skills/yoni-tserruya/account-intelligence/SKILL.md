---
name: account-intelligence
title: Account intelligence
description: |
  Pull a decision-ready intelligence brief on any target account. Takes a
  company name, domain, or Lusha company ID plus a one-line research context —
  QBR, competitive deal, cold outbound, or inbound triage. Returns
  firmographics, buying signals, key contacts verified via Lusha, recent news
  and scoops, and ranked next actions — all framed by your stated purpose.
  Requires a Lusha connection.
category: Research
tags: [Research, Sales]
---

Produce a high-signal intelligence brief on a target account. Lead
with a synthesized executive summary, suppress sections where data
is thin, and tie next steps to specific people and signals surfaced
during the session.

## Input

The user will provide via $ARGUMENTS an account identifier
(required) plus research context:

- Account identifier (required) — one of:
  - Preferred: a Lusha company ID. Use directly; skip the search step.
  - Fallback: a company name or domain. Resolve via companies_search
    as a first step.
- Research context (strongly recommended) — a sentence or two on
  why this brief is being pulled and what decision it supports.
  Examples:
  - "preparing for a QBR — focus on renewal risk and expansion levers"
  - "competitive deal vs. [vendor] — looking for displacement angles"
  - "cold outbound — find the warmest entry point and a credible
    reason to reach out"
  - "inbound triage — deciding between AE routing and nurture"

  This shapes signal triage, contact selection, news filtering,
  and TL;DR framing throughout.

## Workflow

1. Anchor on purpose.
   Read the research context from $ARGUMENTS.
   - If supplied, restate it in one sentence as the brief purpose
     and keep it as the framing lens for every downstream step.
   - If missing, ask the user once. If they decline, default to
     general account intelligence and state that assumption at the
     top of the brief so the reader knows the framing was not tailored.
   - Derive 2-4 priority themes from the purpose. Examples:
     - QBR → engagement health, exec stability, competing vendors,
       expansion signals
     - Competitive → intent on competitor category, recent product
       moves, named stakeholders, displacement angles
     - Cold outbound → warmest contact, strongest signal, credible
       reason to reach out now
     - Inbound triage → ICP fit, growth signals, prior engagement,
       intent on your category

   These themes drive what you surface and cut in every step below.

2. Resolve the account via Lusha.
   - If the user supplied a Lusha company ID, use it directly —
     skip the search step.
   - Otherwise, call companies_search with the company name or
     domain. Extract the company ID from the top match. If no
     confident match, surface the ambiguity before continuing
     rather than guessing.

3. Pull data in parallel.
   Once the company ID is confirmed, run these calls concurrently:
   - Firmographics: size, industry, HQ, revenue range, funding
     stage, tech stack signals
   - Buying signals: intent topics, signal score 60+, ranked by
     score. Do not pre-filter by topic — pull everything and triage
     in step 4.
   - Key contacts: VP+ and Director+ in the function most relevant
     to the brief purpose. Aim for 4-6 contacts. For each: verify
     email and direct dial via Lusha. Return title, seniority,
     department, tenure in current role.
   - Recent news and scoops: last 90 days. Pull broadly —
     leadership moves, funding, product launches, M&A, layoffs.
     Filtering happens in step 4.
   - Similar companies: for competitive context and peer benchmarking.

4. Triage against the brief purpose.
   Each retrieval is raw context. Now decide what makes the brief.
   - Buying signals: keep topics that map to the brief purpose,
     priority themes, your offerings, or suggest a non-obvious
     entry point (e.g. intent on a competitor's category). Drop
     noise. If nothing meaningful survives, replace the table with
     a one-line note.
   - News and scoops: use the brief purpose as the primary filter.
     For a renewal QBR, a layoff or budget-cut signal outranks a
     product release. For a competitive deal, a product launch
     outranks a routine leadership move. Dedupe items covering the
     same theme. Trim to 5-7.
   - Cross-reference: connect the dots across sources and tie them
     to the user's stated goal. A new CTO scoop + hiring surge in
     engineering → one insight, not two bullets.
   - Past-date flag: if any dates surfaced — renewal, contract end,
     last activity — and they are already in the past, flag them as
     needing verification. Could be active negotiation, stale data,
     or a missed milestone.
   - Section suppression: skip any section where data is thin or
     irrelevant to the brief purpose. Never pad.

5. Write the executive summary last.
   Re-read the full body, then write the TL;DR at the top. The
   Situation line must explicitly answer "why this brief, now"
   against the stated purpose — not just who the company is.

## Output Format

### TL;DR — [Company Name]

Brief purpose: [restate the research context in one line, or
"general account intelligence (no purpose supplied)" if defaulted.]

Situation. [2-4 sentences answering why this brief, now: who they
are, the dominant story right now, where the relationship stands,
and the specific signal that makes this purpose timely.]

Top 3 facts. Three most consequential data points across all sources.

Highest-leverage actions. 1-3 concrete actions, each pointing at a
specific person, signal, topic, or moment. No generic advice.

---

### Company Snapshot

| Field | Value |
| Website | |
| Industry | |
| Employees | |
| Revenue range | |
| HQ | |
| Type | Public / Private |
| Funding stage | |
| Founded | |
| Lusha company ID | |

---

### Buying Signals

Intent topics ranked by signal score. Show only topics retained
after triage.

| Topic | Signal Score | Category | Signal Date |

Highlight the top 3 and connect them to the brief purpose or a
specific contact. If nothing meaningful survived triage: "No intent
signals aligned to the brief purpose were found for this account
at this time."

---

### Key Contacts

Verified via Lusha. Show the 4-6 most relevant contacts.

Privacy rules — apply to every row:
- Names: initials only (e.g. J.K.)
- Email: domain only (j.k@[company].com)
- Direct dial: masked (e.g. +1 415 555 ....)
- Tag each row: Contact confirmed live via Lusha connector, [date]

| Name | Title | Seniority | Tenure | Email | Direct Dial |

Flag any contact with tenure under 6 months — recent hire, likely
a timing signal.

---

### Recent News & Scoops

Group by Leadership / Financial / Product / Strategic if 5+ items
span multiple categories. Otherwise list flat.

For each: headline, date, one-line summary.

Call out timing opportunities — e.g. "New VP of Sales appointed
6 weeks ago → vendor evaluation likely open."

---

### Competitive Peers

Top similar companies for benchmarking and competitive context.
If the peer set spans inconsistent industries, lead with a one-line
caveat that the cohort is directional.

| # | Company | Industry | Employees | Revenue | Country |

---

### Corporate Structure

- Parent / Ultimate parent: if applicable
- Funding: total raised, most recent round, date, amount.
  For public companies: "Public — see ticker for capital structure."

---

### Key Takeaways & Next Steps

3-5 bullets connecting the dots across sources, framed by the
stated purpose. Each next action must reference a specific person,
signal, deal, or moment surfaced above. No generic advice. Cut any
line without a concrete target.

---

Example outputs in this skill are illustrative — they reflect the
structure, fields, and format of real Lusha connector output, but
were not pulled from a live session. Run the skill with your own
data and connectors to see live results.

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/account-intelligence-skill/

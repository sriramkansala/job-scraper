---
name: buying-group
title: Buying group
description: |
  Map every decision-maker, influencer, and blocker at a target account. Takes
  a company name or domain plus a deal stage or research context. Returns
  verified contacts classified by buying role, coverage gaps by function,
  departure flags, and ranked next actions — all shaped by where you are in
  the deal. Requires a Lusha connection.
category: ABM
tags: [ABM, Sales]
---

Map the full buying group at a target account. Classify every
contact by role, verify each one live via Lusha, audit coverage
gaps by function, and tie next actions to specific people and
gaps — shaped by the deal stage the user provides.

## Input

The user will provide via $ARGUMENTS:

- Company (required) — name, domain, or Lusha company ID.
- Deal stage or research context (required) — where you are in
  the deal and what decision this map supports. Examples:
  - "Stage 2 discovery — mapping the full buying group for the
    first time"
  - "Stage 3 — procurement and IT now involved, auditing coverage"
  - "Pre-close — validating every key role before sending contract"
  - "CS renewal — mapping who's actually in the account today"

If deal stage is missing, ask once. If declined, default to
general buying group mapping and state that assumption at the
top of the output.

## Workflow

1. Anchor on deal stage.
   Read the deal stage and research context from $ARGUMENTS.
   Restate it in one sentence as the map purpose. Derive the
   functions most relevant to this stage. Examples:
   - Early discovery → Champion, Economic Buyer, key Influencers
   - Mid-stage → add Technical Evaluator, Procurement, IT
   - Pre-close → full audit across all functions, Blocker check
   - CS renewal → current contacts only, flag any departures

2. Resolve the account via Lusha.
   - If the user supplied a Lusha company ID, use it directly.
   - Otherwise call companies_search with the company name or
     domain. Confirm the match before continuing. If ambiguous,
     surface the top two options and ask the user to confirm.

3. Pull contacts in parallel by function.
   Search for VP+ and Director+ contacts across every function
   relevant to the deal stage. Run searches concurrently:
   - Sales / Revenue
   - Finance / Procurement
   - IT / Engineering / Security
   - Operations
   - Marketing (if relevant to the deal)
   - C-suite (CEO, CFO, CTO, COO — for deals above $50K ACV)

   For each contact found: verify email and direct dial via
   Lusha. Return title, seniority, department, tenure in
   current role, and LinkedIn URL if available.

4. Classify by buying role.
   Assign each verified contact to one of these roles based
   on title, seniority, and function:
   - Champion — internal advocate, likely your main contact
   - Economic Buyer — owns budget and final sign-off
   - Technical Evaluator — assesses fit, runs the POC
   - Influencer — shapes the decision without owning it
   - Blocker — can slow or stop the deal
   - Unknown — insufficient signal to classify; flag for follow-up

   One contact can hold multiple roles. Flag it when they do.

5. Audit coverage gaps.
   For each function relevant to the deal stage, check whether
   a verified contact exists. If not, flag it as a coverage gap.
   Rank gaps by deal risk: a missing Economic Buyer at Stage 3
   is higher risk than a missing Influencer at Stage 1.

6. Flag departure and tenure risk.
   - Any contact with tenure under 6 months: flag as recent hire.
     May still be evaluating inherited tools and relationships.
   - Any contact whose LinkedIn or Lusha data suggests a recent
     role change or departure: flag as departure risk. Surface
     who to re-thread with.

7. Write the summary last.
   Re-read the full map. The TL;DR must answer: "what does this
   buying group tell me about where this deal actually stands?"
   — not just who the contacts are.

## Output Format

### TL;DR — Buying Group: [Company Name]

Deal stage: [restate the deal stage in one line.]

Situation. [2-3 sentences: how complete is the buying group,
what are the biggest gaps, and what does that mean for the deal
right now.]

Highest-leverage actions. 1-3 concrete next steps, each pointing
at a specific gap, contact, or risk surfaced in the map.

---

### Buying Group Map

| Name | Title | Function | Buying Role | Tenure | Email | Direct Dial |
|---|---|---|---|---|---|---|

Privacy rules — apply to every row:
- Names: initials only (e.g. J.K.)
- Email: domain only (j.k@[company].com)
- Direct dial: masked (e.g. +1 415 555 ....)
- Tag the table: Contacts confirmed live via Lusha connector, [date]

Flag any contact with:
- Tenure under 6 months → Recent hire
- Role change or departure signal → Departure risk
- Multiple buying roles → Multi-role — verify alignment

---

### Coverage Gap Audit

Functions where no verified contact was found. Ranked by deal risk.

| Function | Gap | Deal Risk | Recommended Action |
|---|---|---|---|

If no gaps: "Full coverage confirmed across all relevant functions
for this deal stage."

---

### Departure & Tenure Flags

Contacts whose status may affect deal continuity.

| Name | Title | Flag | Reason | Recommended Action |
|---|---|---|---|---|

If none: "No departure or tenure flags for this account."

---

### Next Steps

3-5 bullets. Each must reference a specific gap, contact, or
risk from the map above. No generic advice. Cut any bullet
without a concrete target.

---

Example outputs in this skill are illustrative — they reflect the
structure, fields, and format of real Lusha connector output, but
were not pulled from a live session. Run the skill with your own
data and connectors to see live results.

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/buying-group-skill/

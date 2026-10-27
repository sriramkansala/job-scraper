---
name: data-quality
title: Data quality
description: |
  Verify, enrich, and clean any contact or account list against Lusha's
  verified B2B database. Checks emails, refreshes titles, fills missing direct
  dials, enriches firmographics, and flags duplicates and unverifiable
  records. Returns a clean list with a data quality summary showing exactly
  what was fixed and why. Requires a Lusha connection.
category: RevOps
tags: [RevOps]
---

Verify, enrich, and clean a contact or account list against
Lusha's verified B2B database. Show every change with source
and confidence level. Flag every record that can't be verified.
Return a clean list and a data quality summary.

## Input

The user will provide via $ARGUMENTS:

- Contact or account list (required) — paste inline or
  reference a saved list. Accepted formats:
  - Contact list: name, company, email, title (any combination)
  - Account list: company name or domain
  - Mixed: contacts and accounts together
- List context (recommended) — one sentence on what the list
  is for and what data quality bar it needs to clear. Examples:
  - "campaign list — needs verified emails and current titles"
  - "CRM import — needs deduplication and full enrichment
    before it hits Salesforce"
  - "territory file — quarterly refresh, flag anyone who has
    left and fill missing direct dials"

  If list context is missing, default to full verification
  and enrichment across all available fields and state that
  assumption at the top of the output.

## Workflow

1. Anchor on the list context.
   Read the list context from $ARGUMENTS. Identify which
   data quality checks are highest priority for this specific
   use case. State the parameters at the top of the output.

2. Parse and deduplicate the list.
   Before any enrichment:
   - Parse every record from the input.
   - Flag duplicate records — same email, same name and
     company, or same domain appearing more than once.
   - List duplicates in a separate section. Do not enrich
     duplicates — flag them for the user to resolve first.
   - State the total record count after deduplication.

3. Resolve and verify each record via Lusha.
   For each unique record, run these checks concurrently:

   Contact records:
   - Email verification: check the email against Lusha's
     verified database. Return one of:
     - Verified — email confirmed active
     - Updated — original email invalid, new email found
     - Bounced — email invalid, no replacement found
     - Unverifiable — contact not found in Lusha database
   - Title and role refresh: check whether the contact is
     still in the role on record. Return:
     - Confirmed — title and company match current Lusha data
     - Updated — title or company has changed, return new data
     - Departed — contact has left the company
     - Unverifiable — contact not found in Lusha database
   - Direct dial enrichment: return verified direct dial
     if available. Flag if not found.

   Account records:
   - Firmographic enrichment: fill missing fields — industry,
     employee count, revenue range, HQ, funding stage —
     from Lusha's company database.
   - Flag any accounts that could not be matched.

4. Classify each record.
   After verification and enrichment, classify every record:
   - Clean — all fields verified, no changes needed
   - Enriched — missing fields filled, existing fields confirmed
   - Updated — one or more fields corrected with new Lusha data
   - Flagged — contact departed, email bounced, or title changed
     — needs human review before use
   - Unverifiable — record could not be matched in Lusha —
     exclude from list or escalate for manual research

5. Write the data quality summary.
   Lead with the headline numbers: total records, clean,
   enriched, updated, flagged, unverifiable. Then the
   clean list. Then the flagged records. Then duplicates.
   Then unverifiable records.

## Output Format

### Data Quality Summary

List context: [restate in one line]
Total records processed: [n]
Clean: [n]
Enriched: [n]
Updated: [n]
Flagged — needs review: [n]
Unverifiable — excluded: [n]
Duplicates found: [n]

---

### Clean List

All verified and enriched records, ready to use.

Privacy rules — apply to every row:
- Names: initials only (e.g. J.K.)
- Email: domain only (j.k@[company].com)
- Direct dial: masked (e.g. +1 415 555 ••••)
- Tag the table: Records verified live via Lusha connector,
  [date]

| Name | Title | Company | Email | Direct Dial | Status |
|---|---|---|---|---|---|

Status values: Clean / Enriched / Updated

---

### Flagged Records — Needs Review

Records where something changed or a problem was found.
Do not use until reviewed.

| Name | Title | Company | Email | Flag | Reason | Recommended Action |
|---|---|---|---|---|---|---|

Flag types:
- Departed — contact has left the company
- Email bounced — invalid email, no replacement found
- Title changed — contact is still at company but role changed
- Company changed — contact has moved to a new company

---

### Duplicate Records

Records appearing more than once in the input list.
Resolve before enrichment.

| Name | Company | Email | Duplicate Of |
|---|---|---|---|

---

### Unverifiable Records

Records that could not be matched in Lusha's database.
Exclude from list or escalate for manual research.

| Name | Company | Email | Reason |
|---|---|---|---|

---

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/data-quality-skill/

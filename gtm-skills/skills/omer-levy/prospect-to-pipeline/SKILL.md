---
name: prospect-to-pipeline
title: Prospect to pipeline
description: |
  Find the right contact at a target account, verify their email and direct
  dial via Lusha, check for buying signals and recent news, and draft a first-
  touch message shaped around what you find. Takes a company and a one-line
  target — function, seniority, and reason for reaching out. Returns a
  verified contact and a ready-to-send first message in one pass. Requires a
  Lusha connection.
category: Prospecting
tags: [Sales]
---

Find the right contact at a target account, verify their details
live via Lusha, check for signals that make the outreach timely,
and draft a first-touch message worth sending. One pass — no
separate enrichment step, no template guessing.

## Input

The user will provide via $ARGUMENTS:

- Company (required) — name, domain, or Lusha company ID.
- Target (required) — function, seniority, and reason for
  reaching out. Examples:
  - "VP of Sales or above — we help sales teams scale outbound
    with verified data"
  - "Head of Revenue Operations — we reduce CRM data decay"
  - "CFO or VP Finance — reaching out around budget planning"

If target is missing, ask once. If declined, default to the
most senior contact in the company's primary revenue function
and state that assumption before continuing.

## Workflow

1. Anchor on the target.
   Read the function, seniority, and reason from $ARGUMENTS.
   Restate in one sentence: who you're looking for and why.
   This drives contact search, signal triage, and draft framing
   in every step below.

2. Resolve the account via Lusha.
   - If the user supplied a Lusha company ID, use it directly.
   - Otherwise call companies_search with the company name or
     domain. Confirm the match before continuing. If ambiguous,
     surface the top two options and ask to confirm.

3. Find the right contact.
   Search for contacts matching the target function and seniority.
   Return the top 3 matches ranked by relevance to the stated
   goal. For each: title, seniority, department, tenure in
   current role.

   Ask the user to confirm which contact to proceed with, or
   default to the top match and state that assumption.

4. Verify contact details via Lusha.
   For the confirmed contact: verify email and direct dial.
   Return both. If email is unavailable, flag it and return
   the direct dial only. If neither is available, flag it
   and ask the user how to proceed.

5. Check for signals.
   Pull buying signals, recent news, and scoops for the account.
   Last 90 days. Do not pre-filter — pull broadly and triage
   against the stated reason for reaching out.

   Keep signals that:
   - Map directly to the reason for reaching out
   - Suggest a non-obvious but credible entry point
   - Create a timing window (new hire, funding, hiring surge,
     product launch, intent on your category)

   Drop noise. If nothing meaningful survives, proceed without
   a signal hook and note it in the draft.

6. Draft the first-touch message.
   Write a first-touch email or LinkedIn message — the user's
   channel preference if stated, email by default.

   Rules:
   - Open with the strongest signal or timing hook found in
     step 5. If no signal, open with the most specific thing
     you know about their role or company context.
   - One clear reason why this person, why now.
   - One specific value statement tied to their function and
     the stated reason for reaching out.
   - One low-friction CTA — a question, not a meeting request.
   - Under 100 words for email. Under 300 characters for
     LinkedIn.
   - No generic openers. No "I hope this finds you well."
     No "I came across your profile."

7. Return the full output.
   Contact details, signal summary, and draft — in one clean
   output the user can act on immediately.

## Output Format

### Contact: [Company Name]

Target: [restate the function, seniority, and reason in one line.]

---

### Verified Contact

| Field | Value |
|---|---|
| Name | [initials only — e.g. J.K.] |
| Title | |
| Function | |
| Seniority | |
| Tenure | |
| Email | [domain only — j.k@[company].com] |
| Direct Dial | [masked — +1 415 555 ••••] |

Contact confirmed live via Lusha connector, [date].

---

### Signal Hook

The strongest signal found for this outreach — kept because it
creates a timing window or maps directly to the reason for
reaching out.

Signal: [topic or event]
Type: [Intent / News / Scoop / Hiring]
Date: [date]
Why it matters: [one sentence connecting the signal to the
reason for reaching out]

If no signal survived triage: "No signals aligned to this
outreach were found. Draft proceeds without a signal hook."

---

### First-Touch Draft

Channel: [Email / LinkedIn]

Subject: [subject line — email only]

[draft body]

---

### Alternative Contacts

If the top match wasn't confirmed or the user wants options:

| Name | Title | Seniority | Tenure | Email | Direct Dial |
|---|---|---|---|---|---|

---

Example outputs in this skill are illustrative — they reflect the
structure, fields, and format of real Lusha connector output, but
were not pulled from a live session. Run the skill with your own
data and connectors to see live results.

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/prospect-to-pipeline-skill/

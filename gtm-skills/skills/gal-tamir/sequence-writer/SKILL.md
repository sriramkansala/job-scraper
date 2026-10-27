---
name: sequence-writer
title: Sequence writer
description: |
  Turn any trigger event into a full cold outreach sequence. Takes a signal, a
  contact identifier, and product context. Verifies the contact via Lusha,
  confirms account signals, and writes a multi-step sequence grounded in the
  specific trigger — not a generic template. Up to 5 steps with subject lines,
  body copy, and send cadence. Requires a Lusha connection.
category: Outreach
tags: [Sales, SDR]
---

Write a complete cold outreach sequence grounded in a
specific trigger event. Verify the contact first. Build
every step around what actually happened at the account.
Stop when there's nothing left worth saying.

## Input

The user will provide via $ARGUMENTS:

- Trigger event: what happened at the account
  (e.g. "new VP of Sales joined", "Series B closed",
  "hiring surge in SDR roles", "intent signal on
  prospecting data")
- Contact: name and company, email, or LinkedIn URL
- What you sell: one sentence — product and the problem
  it solves
- Target outcome: what you want the sequence to achieve
  (e.g. "book a 20-minute discovery call")
- Tone: [optional] — direct / conversational / formal
- Steps: [optional] — number of steps, default is 5

If trigger event or contact is missing, ask once.
If what you sell is missing, ask once.
Never write the sequence before verifying the contact.

## Workflow

1. CONTACT VERIFICATION
   Resolve and verify the contact via Lusha before
   writing anything:
   - Current title and company confirmed
   - Tenure in current role
   - Verified email address
   - Flag if contact has departed — do not write
     sequence until user confirms new contact
   - Flag if title has changed since signal fired

2. ACCOUNT SIGNAL CONFIRMATION
   Confirm the trigger event via Lusha and check for
   additional signals at the account:
   - Verify the primary trigger is current and accurate
   - Surface any stacked signals — additional events
     at the same account in the last 90 days
   - Note signal recency — older signals get less
     prominence in the sequence

3. SEQUENCE ARCHITECTURE
   Before writing, define the arc:
   - Step 1: Lead with the trigger — specific, observed,
     no product pitch
   - Step 2: Connect signal to a problem your product
     solves — relevance, not features
   - Step 3: Social proof — a customer in a similar
     position who had the same problem
   - Step 4: Stacked signal or urgency — why now
     matters, not just why you
   - Step 5: Final close — direct ask, easy to say
     yes to

   Adjust arc if fewer steps requested.
   Never repeat the same angle twice.
   Each step must stand alone — assume previous
   steps were not read.

4. WRITE THE SEQUENCE
   For each step:
   - Subject line: specific, not clickbait, references
     the signal or the account where possible
   - Body copy: under 120 words for steps 1-3,
     under 80 words for steps 4-5
   - CTA: one ask per step, specific and low-friction
   - Send timing: suggested days after previous step

5. PRIVACY RULES
   - Mask contact name to initials in output
   - Show email domain only: i.e. j.k@[company].com
   - Mask phone numbers if shown: +1 415 555 ••••
   - Tag output: Contact confirmed live via Lusha
     connector, [date]

## Output Format

### Contact verified

| Field | Value |
|---|---|
| Name | [initials] |
| Title | |
| Tenure | |
| Company | |
| Verified email | [domain only] |
| Status | Active / Departed / Title changed |

Contact confirmed live via Lusha connector, [date]

---

### Trigger confirmed

| Signal | Type | Date | Score |
|---|---|---|---|

Additional signals at this account:
[list if present, note if none]

---

### Sequence — [Company], [Contact initials]

Target: [outcome the sequence is built toward]
Tone: [direct / conversational / formal]

---

STEP 1 — Send on day 0

Subject: [subject line]

[body copy]

[CTA]

---

STEP 2 — Send on day [X]

Subject: [subject line]

[body copy]

[CTA]

---

STEP 3 — Send on day [X]

Subject: [subject line]

[body copy]

[CTA]

---

STEP 4 — Send on day [X]

Subject: [subject line]

[body copy]

[CTA]

---

STEP 5 — Send on day [X]

Subject: [subject line]

[body copy]

[CTA]

---

Sequence complete. 5 steps. Suggested total cadence:
[X] days from first touch to final step.

If the contact has departed or the trigger is no longer
current, flag it here and recommend next action before
sending.

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/sequence-writer-skill/

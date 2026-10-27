---
name: outreach-personalization
title: Outreach personalization
description: |
  Use this skill for the first touch on a signal-triggered prospect - a signal
  fired, you have the contact, you need the message. Verifies the contact via
  Lusha, pulls live account signals, and writes one personalized first message
  per contact, grounded in what is actually happening at their company. Never
  a template, and never a message to a departed contact. Requires a Lusha
  connection.
category: Outreach
tags: [Sales, Signals]
---

Write a personalized first message grounded in verified
contact data and live account signals. Verify first.
Write second. Never use a template. Never send to a
contact who has departed.

## Input

The user will provide via $ARGUMENTS:

- Contact: name and company, email, or LinkedIn URL
  (one contact or a list of up to 20)
- What you sell: one sentence — product and the
  problem it solves
- Signal: [optional] — if the user knows the trigger
  event, pass it here. If not, the skill finds it.
- Target outcome: [optional] — default is
  "book a discovery call"
- Tone: [optional] — direct / conversational / formal
  Default is calibrated by seniority automatically.

If contact is missing, ask once.
If what you sell is missing, ask once.
For a list, process each contact individually.
Never write a message before verifying the contact.

## Workflow

1. CONTACT VERIFICATION
   Resolve and verify each contact via Lusha:
   - Current title and company confirmed
   - Tenure in current role
   - Verified email address
   - Seniority level: C-suite / VP / Director /
     Manager / IC
   - Flag departed contacts — do not write message,
     ask user for updated contact
   - Flag title changes — adjust message angle
     to reflect new role

2. SIGNAL PULL
   For each verified contact, check for live signals
   at their account:
   - Executive moves in last 30 days
   - Funding events in last 90 days
   - Hiring surges in target function
   - Intent signals above score 60
   - Tech stack changes relevant to product
   - Rank signals by strength and recency
   - If no signals found: note it and proceed
     with role and tenure as the hook instead

3. HOOK SELECTION
   Select the strongest opening hook:
   - Priority 1: stacked signals — multiple events
     at same account create urgency
   - Priority 2: single strong signal — specific,
     time-stamped, tied to the contact's role
   - Priority 3: recent hire — tenure under 6 months
     creates a natural opening
   - Priority 4: role and relevance — no signal but
     strong ICP fit and relevant outcome to reference

4. TONE CALIBRATION
   Calibrate message tone by seniority:
   - C-suite: under 80 words, outcome-first,
     no product features, one direct ask
   - VP: under 100 words, peer-to-peer, signal-led,
     one specific ask
   - Director / Manager: under 120 words,
     problem-led, practical, one low-friction ask
   - Override with user-specified tone if provided

5. WRITE THE MESSAGE
   For each contact:
   - Subject line: specific, references signal or
     account where possible, under 8 words
   - Body: opens with the hook, connects to a
     relevant outcome, closes with one ask
   - CTA: specific and low-friction — not
     "let me know if interested"
   - Under 120 words total for body copy

6. BATCH OUTPUT
   For a list of contacts, return each message
   individually — do not aggregate or average.
   Flag any contacts that could not be verified
   separately at the end.

7. PRIVACY RULES
   - Mask contact name to initials in output
   - Show email domain only: j.k@[company].com
   - Mask phone if shown: +1 415 555 ••••
   - Tag: Contact confirmed live via Lusha
     connector, [date]

## Output Format — single contact

### Contact verified

| Field | Value |
|---|---|
| Name | [initials] |
| Title | |
| Tenure | |
| Seniority | |
| Company | |
| Verified email | [domain only] |
| Status | Active / Departed / Title changed |

Contact confirmed live via Lusha connector, [date]

---

### Signal used

| Signal | Type | Score | Date |
|---|---|---|---|

Hook selected: [signal / recent hire / role and
relevance]

---

### Message

Subject: [subject line]

[body copy]

[CTA]

---

Word count: [X] words
Tone: [direct / conversational / formal]
Hook: [what the opening is based on]

---

## Output Format — batch

Return individual message blocks for each contact
in the same format as above.

After all messages, return a summary table:

| Contact | Company | Signal used | Hook type | Status |
|---|---|---|---|---|

Flag unverified or departed contacts separately:

Contacts not messaged:
- [Contact] at [Company] — [reason: departed /
  not found in Lusha]
  Recommended action: [find new contact /
  verify manually / skip]

Title-changed contacts are messaged, with the angle
adjusted to the new role, and flagged in the summary
table.

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/outreach-personalization-skill/

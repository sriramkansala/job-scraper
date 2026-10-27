---
name: territory-signal-digest
title: Territory signal digest
description: |
  Run a weekly signal sweep across every account in your territory. Takes an
  account list and returns a ranked brief — promotions, job changes, funding
  rounds, hiring surges, and intent spikes, sorted by signal strength.
  Designed to run every Monday morning before a pipeline review. Requires a
  Lusha connection.
category: Signals
tags: [Sales, Signals]
---

Run a weekly signal sweep across every account in a territory.
Rank accounts by signal strength. Surface what moved since last
week. Return a brief the rep can act on before their first call.

## Input

The user will provide via $ARGUMENTS:

- Account list (required) — a list of company names, domains,
  or Lusha company IDs. Paste inline or reference a saved list.
- Lookback window (optional) — how far back to pull signals.
  Default: 7 days for weekly digest. Accept: 30 days, 90 days.
- Signal focus (optional) — which signal types to prioritize.
  Default: all. Options:
  - Role changes (promotions, job changes, departures)
  - Hiring surges (open roles in target functions)
  - Funding (rounds, investment announcements)
  - Intent (buying signals on your category)
  - News (product launches, M&A, leadership moves)

If account list is missing, ask once. If declined, return an
error — the skill cannot run without a list of accounts.

## Workflow

1. Anchor on the digest purpose.
   Read the lookback window and signal focus from $ARGUMENTS.
   Default to 7-day lookback and all signal types if not supplied.
   State the parameters at the top of the output so the reader
   knows what the digest covers.

2. Resolve accounts via Lusha.
   For each account in the list:
   - If a Lusha company ID is supplied, use it directly.
   - Otherwise resolve via companies_search using the name
     or domain.
   - Flag any accounts that could not be resolved and skip them.
     List unresolved accounts at the end of the output.

3. Pull signals in parallel.
   For each resolved account, run these calls concurrently:
   - Buying signals: intent topics, signal score 60+, ranked
     by score. Lookback window as specified.
   - News and scoops: last 7 days (or specified window).
     Leadership moves, funding, product launches, M&A, layoffs.
   - Hiring signals: open roles in target functions posted in
     the lookback window.
   - Contact changes: promotions, job changes, departures for
     key contacts at the account.

4. Score and rank accounts.
   Assign each account a signal score based on:
   - Number of signals found
   - Signal strength (intent score, recency, signal type weight)
   - Signal type weights:
     - Funding round: high
     - Executive hire or departure: high
     - Intent on your category: high
     - Hiring surge in target function: medium
     - Product launch or M&A: medium
     - General news: low

   Rank accounts from highest to lowest signal score.
   Accounts with no signals go to the bottom — list them
   briefly so the rep knows they were checked.

5. Triage signals per account.
   For each account in the ranked list, keep only the signals
   that are worth the rep's attention this week. Drop noise.
   One account should not have more than 3-5 signal bullets
   unless every signal is genuinely high value.

6. Write the digest.
   Lead with a summary line: how many accounts were checked,
   how many had signals, and the single most important signal
   across the whole territory this week.
   Then the ranked account list.

## Output Format

### Territory Signal Digest

Period: [start date] — [end date]
Accounts checked: [n]
Accounts with signals: [n]
Top signal this week: [one line — the single most important
signal across the whole territory]

---

### Ranked Account List

For each account, in signal-rank order:

**[Account Name]** — Signal score: [H / M / L]

| Signal | Type | Date | Why it matters |
|---|---|---|---|

Recommended action: [one line — what to do with this account
this week, tied to the strongest signal]

---

Repeat for every account with signals.

---

### No-Signal Accounts

Accounts checked with no signals in the lookback window:
[list of account names]

These accounts were checked — nothing moved this week.

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

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/territory-signal-digest-skill/

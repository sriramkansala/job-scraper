---
name: handle-demo-request
title: Handle a demo request
description: |
  Use this skill when someone requests a demo through your website — a "Book a demo" form,
  a webhook carrying little more than a work email — and the question is what happens in the
  next sixty seconds. Enriches the person and company, decides fit and buyer persona
  separately, and routes the request down one of three paths: the qualified hand-raise that
  gets a booking email, the right company with the wrong person, and the account that should
  be sent to a free trial rather than a calendar. Covers inbound demo requests, form-fill
  routing, hand-raise qualification, MQL hygiene, and self-serve versus sales-assisted
  triage.
category: Signals
tags: [Sales, RevOps, Demand Gen]
---

# Handle a demo request

Runs on every inbound demo request. Produces a CRM record, a fit-and-persona verdict, exactly one outbound email (or none), and a single alert to the team — with the request routed by whether the company is a fit and whether the person is a buyer, never by a tier number alone.

The default handling — route every demo request to a rep and book the meeting — is wrong in both directions. It sends your team into meetings with companies that were never going to buy, and it treats a junior analyst at a perfect-fit account as if they were the CRO.

## Template placeholders

Replace every `{{...}}` before enabling. Full setup list in **references/setup-customization-checklist.md**.

- `{{CRM}}` — where contacts and companies live (e.g. HubSpot, Salesforce, Attio).
- `{{ALERT_CHANNEL}}` — the single channel every demo request posts to, whatever the outcome.
- `{{MQL_CHANNEL}}` — where qualified leads surface. Owned by your scoring pass, never posted to from here.
- `{{SALES_SENDER}}` — the person booking emails come from.
- `{{BOOKING_LINK}}` — their calendar link.
- `{{TRIAL_LINK}}` — your self-serve entry point.
- `{{SELF_SERVE_FLOOR}}` — the company size below which an account is self-serve, not sales-assisted (default: under 50 employees).
- `{{FUNDED_OVERRIDE}}` — the funding-and-size combination that pulls an account back onto the sales-assisted path regardless (default: more than 30 employees **and** more than $10M raised).
- `{{TOP_TIERS}}` — the tiers that justify an MQL stage rather than an awareness stage.
- `{{DECISION_MAKER_TITLES}}` — the titles that count as buying authority in your market.

---

## Step 1 — Gate the email before spending anything

Extract the work email. **Stop when there is no email, or when it is a consumer domain** — gmail, outlook, hotmail, yahoo, icloud, proton, and the rest.

Post a low-priority note to `{{ALERT_CHANNEL}}` saying a demo request arrived that could not be processed, include the raw address if there was one, and end. Do not enrich, do not write to `{{CRM}}`, do not send anything.

This gate exists because enrichment costs money and CRM pollution costs more. A personal address on a demo form is usually a student, a competitor, or a bot, and the cost of finding out is not zero.

## Step 2 — Enrich, then write to the CRM

Resolve the person (name, title, profile URL) and the company from the email domain (employee count, funding, industry, description, target market).

**If no real company resolves from the domain, that is a non-fit answer, not a missing one** — route to Step 5's non-fit path and say the domain could not be resolved.

Create or update the contact and company, associated to each other, with a note recording the source, the date, and the submitted address. CRM writes need no approval; they are reversible and they are the audit trail.

## Step 3 — Decide persona *before* you score

Classify the submitter as a decision-maker or not, from their title, using `{{DECISION_MAKER_TITLES}}`. Everyone else — individual contributors, junior titles, non-GTM functions, and any title that would not resolve — is not a decision-maker.

**The order matters.** Persona is an input to scoring, not a read of its output. Score first and you get a tier that has already blended "good company" and "good person" into one number, and you can no longer tell which one you are looking at.

## Step 4 — Score the account, with three directives

Run your normal account scoring pass in full: tier, deal-size band, ICP and target-market flags, and every hard stop it already enforces (competitor, investor, partner, government, self-serve). Do not re-implement any of that here.

Pass it three directives:

**1. Suppress the MQL alert for non-decision-makers.** If the submitter is not a decision-maker, the scoring pass does everything *except* announce. No `{{MQL_CHANNEL}}` post, no direct message, no briefing. Tier, tags, and CRM state all still happen. This keeps the MQL channel clean of accounts where no buyer has actually raised a hand — the alternative is a channel full of good logos that nobody can act on.

**2. Self-serve is not a full stop here.** Let the self-serve gate apply its tags and stage as normal, then keep going — this workflow still sends the free-trial email. A small company asking for a demo is the ideal free-trial audience, and silence is a worse answer than the wrong door.

**3. The funding override — don't cancel the demo.** Before scoring, resolve employee count (take the lower of enrichment and the profile) and total funding. If the company clears `{{FUNDED_OVERRIDE}}`, do not self-serve-gate it: score it on the sales-assisted path, do **not** suppress the MQL alert even for a non-decision-maker, and route it to Branch A. A funded company that asks for a demo gets a demo, not a self-serve brush-off.

## Step 5 — Route on fit × persona, never on tier

| Outcome | Path |
|---|---|
| **Competitor** | Post nothing, anywhere. Send nothing. End silently — the competitor gate forbids surfacing them, and scoring has already logged it. |
| **Investor, partner/vendor, or government** | One low-priority note naming the reason. No email. End. |
| **Self-serve, or out of ICP** | **Branch C** — free trial. |
| **Fit + decision-maker** | **Branch A** — booking email. |
| **Fit + not a decision-maker** | **Branch B** — surface, don't send. |

A fit account is one your scoring places in a target market with real sales-assisted deal size. **It is not the tier number.** A persona gate can cap a genuinely good company at a middling tier because a junior person was the only signal — that account is still a fit, and it belongs in Branch B, not Branch C.

### Branch A — the qualified hand-raise

1. Set the funnel stage by tier: `{{TOP_TIERS}}` → MQL stage; everything else → an awareness stage. A decision-maker demo request is real, but only the top tiers belong in MQL.
2. Send a booking email from `{{SALES_SENDER}}`. Subject names the company. Three short paragraphs, casual and specific: confirm what you do maps to their situation, referencing something concrete about their company. **Never write "I saw you filled out a form."** Close by inviting them onto `{{BOOKING_LINK}}` as a plain-text URL.
3. Post a high-priority alert to `{{ALERT_CHANNEL}}` — who, where, title, tier, why they qualify, that the email went out, and CRM links. Format in **references/alerting-and-channel-model.md**.

The MQL-channel post is not yours. Your scoring pass already made it. Do not rebuild it.

### Branch B — right company, wrong person

The account is real. The person is not a buyer. This is the case every inbound motion handles badly, and it is reached by fit, not tier.

1. Leave the CRM stage where scoring put it. Do not force an MQL stage from here.
2. **Send nothing.** No booking email — they cannot book. No free-trial email either — this is a fit account, not a self-serve one.
3. Confirm the MQL alert was suppressed (Step 4, directive 1). Do not post one now.
4. Post a medium-priority alert to `{{ALERT_CHANNEL}}` flagging explicitly that this is a fit account whose demo request came from a non-buyer, so a human can decide whether to route to the real buyer. Include the likely decision-makers at that account if your scoring surfaced them. **This alert is the only surfacing this case gets** — which is exactly why it has to carry enough for someone to act on.

### Branch C — not a sales-assisted fit

Covers both the out-of-ICP company and the self-serve one below `{{SELF_SERVE_FLOOR}}`.

1. Send a short free-trial email from `{{SALES_SENDER}}` — three or four sentences. Name the specific thing they would want to try, and invite them to `{{TRIAL_LINK}}` to try that exact use case. No calendar link.
2. Post a low-priority note to `{{ALERT_CHANNEL}}` with the reason they are not sales-assisted and that the trial email went out. Bump to medium for a recognizable brand or a large company — size that your own scoring under-reads is worth a human glance.

**Never send both emails.** One branch, one message.

## Step 6 — Keep the two channels separate

`{{ALERT_CHANNEL}}` is this workflow's channel and every outcome posts there exactly once. `{{MQL_CHANNEL}}` belongs to your scoring pass, with its own suppression and gating. Posting to it from here produces duplicates that quietly train the team to ignore both. Full model, priorities, and alert format in **references/alerting-and-channel-model.md**.

## What good looks like

- **Persona and fit are separately legible in the record.** Someone reading the account can tell whether it was the company or the person that failed, because those were decided in different steps.
- **The expert tell: the MQL channel stays boring.** Novices measure the inbound motion by how many leads it surfaces. What predicts a working motion is that everything surfaced is actionable — a channel where a good logo appears with nobody to call is a channel people stop opening.
- **Branch B produces action, not filing.** The test is whether anyone actually reached the real buyer. If those alerts are consistently read and dropped, the alert lacks the buying-committee detail, and that is a fixable defect rather than a fact of life.
- **The mediocre version routes on tier.** It sends a top-tier junior analyst to a rep and pushes a mid-tier CRO to a free trial, and it looks defensible in a dashboard the whole time.
- **The second mediocre version answers everything with a calendar link.** Self-serve companies do not book, do not show, and do not come back — the free-trial nudge exists because the wrong door is worse than a smaller one.
- **Nobody is surprised by an email.** Every send traces to a branch, and no account ever received two.

## Rules

- **MUST** gate consumer email domains before enriching or writing to the CRM. **NEVER** spend enrichment on an ungated address.
- **MUST** decide persona before scoring, and pass it in as a directive.
- **MUST** route on fit and persona together. **NEVER** route on the tier number alone.
- **MUST** send at most one email per request. **NEVER** send both the booking and the trial email.
- **MUST** treat an unresolvable company domain as non-fit, not as missing data.
- **MUST** leave the `{{MQL_CHANNEL}}` post to the scoring pass. **NEVER** rebuild or re-post it from here.
- **MUST** post competitor outcomes nowhere at all — no channel, no email.
- **MUST** queue outbound for human approval by default; flip to auto-send only once a team has decided a demo request is explicit enough consent, and only for these single acknowledgement emails.
- **NEVER** send a booking email to someone with no buying authority; surface them to a human instead.
- **MUST** treat every threshold here — `{{SELF_SERVE_FLOOR}}`, `{{FUNDED_OVERRIDE}}`, `{{TOP_TIERS}}` — as a tunable default, calibrated against your own closed-won history before it routes real requests.

---
title: Setup and customization checklist
description: (reference) Placeholders to fill, the policy decisions to make before enabling, calibration, and the invariants that must survive any customization.
---

# Setup and customization checklist

What to decide before this runs on live inbound.

## 1. Fill the placeholders

| Placeholder | What to put there | Default if unsure |
|---|---|---|
| `{{CRM}}` | Where contacts and companies live | Whatever your reps already work in |
| `{{ALERT_CHANNEL}}` | One channel, every demo request | A new channel — do not reuse an MQL channel |
| `{{MQL_CHANNEL}}` | Where your scoring pass surfaces qualified leads | Your existing one; this skill never posts there |
| `{{SALES_SENDER}}` | Who booking and trial emails come from | The person whose calendar the link opens |
| `{{BOOKING_LINK}}` | Their calendar link | A 30-minute meeting type |
| `{{TRIAL_LINK}}` | Self-serve entry point | Your signup URL, no campaign parameters |
| `{{SELF_SERVE_FLOOR}}` | Size below which an account is self-serve | Under 50 employees |
| `{{FUNDED_OVERRIDE}}` | The exception that pulls an account back to sales-assisted | More than 30 employees **and** more than $10M raised |
| `{{TOP_TIERS}}` | Tiers justifying an MQL stage | Your top two |
| `{{DECISION_MAKER_TITLES}}` | Titles with buying authority in your market | See below |

### Decision-maker titles

The default list is GTM leadership with budget: CRO, VP or Head of Sales, VP or Head of Marketing, CMO, CEO, founder or co-founder, RevOps lead, GTM engineer, growth lead, head of demand generation, agency owner.

Adjust for how your market actually buys. In a developer product the buyer may be a staff engineer; in mid-market the CEO signs everything. **The list is not a seniority ranking — it is a list of people who can say yes.** A director who owns the budget belongs on it; a VP who does not, does not.

## 2. Decide the auto-send policy first

This skill defaults to **queueing outbound for human approval**, which is the right starting posture.

Teams that treat a demo request as explicit consent flip Branch A and Branch C to auto-send, on the reasoning that someone who asked for a demo has asked to be contacted, and a reply an hour later beats a reply tomorrow. That is a defensible call and a common one.

Two conditions before you make it:

- **The flip covers these acknowledgement emails only.** It is not a general auto-send permission for the sender, and it must not silently become one for outbound sequences.
- **Read the first twenty out loud.** Auto-send makes every drafting weakness public at speed. If any of the twenty makes you wince, the voice guidance needs work before the volume does.

Branch B is never auto-send, because Branch B never sends.

## 3. Calibrate the thresholds against your own history

The numbers here are starting points, not findings.

- **`{{SELF_SERVE_FLOOR}}`** — take your closed-won accounts and find the size below which sales-assisted deals stopped being worth the touch. If you have never won below a size, that is your floor.
- **`{{FUNDED_OVERRIDE}}`** — this exists because size alone under-reads a funded company: thirty people with real money behind them buys like a much larger org. Check it against the funded accounts you have actually won.
- **`{{TOP_TIERS}}`** — should be narrow enough that the MQL channel stays short. If more than a small fraction of demo requests reach it, the bar is too low and the channel will be ignored within a month.

Re-check after a quarter of real volume, and change one threshold at a time — moving two at once makes the result unreadable.

## 4. Invariants — do not customize these away

These carry the judgment. Everything else is tunable.

- **Persona is decided before scoring**, and passed in. Reversing the order collapses "good company" and "good person" into one number.
- **Routing is fit × persona, never tier alone.** A capped tier on a genuinely good company is exactly the case this exists to catch.
- **One email per request, maximum.** The booking email and the trial email are mutually exclusive, always.
- **The MQL channel has one owner.** This workflow never posts there.
- **Competitors surface nowhere.**
- **Branch B sends nothing and surfaces everything.** The temptation is to send the junior person something friendly; that trains them to think they are the contact, and it is harder to route to the real buyer afterwards.

## 5. What to watch in the first month

- **The share of requests reaching Branch B.** Consistently high means your form is collecting the wrong person — a "what's your role" field will do more than any routing change.
- **Whether Branch B alerts get acted on.** If not, the alert is missing buying-committee detail.
- **Trial starts from Branch C.** Zero means the email is not landing, or the trial link is wrong. This is the cheapest branch to fix and the easiest to leave broken, because nobody complains about it.
- **Consumer-domain stops.** A sudden rise usually means a bot found your form, not that your market changed.

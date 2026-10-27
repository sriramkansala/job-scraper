---
title: Alerting and the two-channel model
description: (reference) Why demo requests and qualified leads go to different channels, the alert format every branch shares, and the priority ladder.
---

# Alerting and the two-channel model

Every demo request produces exactly one alert. Which channel it lands in, and how loud it is, is decided before anything is written.

## Two channels, two owners

| Channel | Owner | Posts |
|---|---|---|
| `{{ALERT_CHANNEL}}` | this workflow | Every outcome — all three branches, plus investor / partner / government notes |
| `{{MQL_CHANNEL}}` | your account scoring pass | Only qualified leads, with its own gating and suppression |

**The separation is the point.** The workflow channel answers "what came in and what did we do about it" — it is a log, and it is complete. The MQL channel answers "who should someone call today" — it is a queue, and it is short. Merge them and you get a queue nobody trusts, because most of what is in it is not a lead.

The failure this prevents is duplicate announcement. When two systems both post the qualified case, the team learns that every item appears twice, then stops reading whichever one they see second — usually the one that mattered.

**Net effect, so the routing is auditable:**

| Case | Workflow channel | MQL channel |
|---|---|---|
| Branch A, top tier | ✓ | ✓ (from scoring) |
| Branch A, lower tier | ✓ | — (scoring does not surface sub-tier) |
| Branch B (fit, non-buyer) | ✓ | — (suppressed at Step 4) |
| Branch C (non-fit / self-serve) | ✓ | — |
| Investor / partner / government | ✓ low note | — |
| Competitor | — | — |

Competitors get nothing anywhere. A competitor appearing in a channel invites a reply from someone who has not read the whole thread, and the scoring pass has already logged them where they belong.

## Priority ladder

- **High** — Branch A. A buyer at a fit account asked for a demo. This is the only case that should interrupt someone.
- **Medium** — Branch B, and Branch C when the company is a recognizable brand or unusually large. Both mean "a human should look at this today", not "right now".
- **Low** — Branch C in the ordinary case, and every hard-stop note. These are read in a batch, or not at all, and that is fine.

If everything is high priority, nothing is. The ladder is only doing its job when most posts are low.

## Alert format

Every post carries the same shape, so the channel can be skimmed vertically:

```text
WHO       — name, title, company
WHAT      — which branch fired, and what was sent (or that nothing was)
CONTEXT   — how they arrived, and when
ICP MATCH — fit verdict and tier, with the one line that decided it
INSIGHT   — the single most useful thing about this account
ACTIONS   — what the workflow already did, so nobody repeats it
LINKS     — CRM records
```

Two rules about the body:

**Say what was already done.** An alert that reports a lead without reporting the email already sent produces a second, near-identical email from a helpful human. The "actions taken" line is not a courtesy; it is a deduplication mechanism.

**Include the account profile in the body, not behind a link.** Size, maturity, and growth stage decide whether anyone acts, and an alert that requires opening the CRM to learn them will be triaged as "later" by whoever is on their phone.

## Branch B carries more

Branch B's alert is the only surfacing that case ever gets, so it needs everything a person requires to act without going back to the source: the fit verdict, why the submitter was not treated as a buyer, and the likely decision-makers at that account if scoring surfaced them.

An alert that says "fit account, wrong person" and stops has moved the work to a human without giving them the means to do it. Where these get read and dropped consistently, that is the defect to fix — not evidence that the case does not matter.

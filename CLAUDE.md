# Instructions for Claude

This repo runs Sriram's job search as a product designer. Read `README.md` for the overview. This file covers what to do when asked to work on it.

## Requests and what to do

| Request | Do this |
|---|---|
| "Run the job search", "refresh the target companies", "find companies to apply to" | The full workflow below |
| "Update my profile" or "rebuild the ICP" | Steps 1–2 only, then update the Profile & ICP doc in Linear |
| "Evaluate this job" or a pasted posting | Follow `career-ops/modes/oferta.md` (read `career-ops/README.md` first for how it maps onto this repo). Run its liveness and dealbreaker gates first, then blocks A–H. Then check the role against the six gates below. |
| "Who should I contact at X?" or "draft a note to the hiring manager" | First run `python3 tools/warm_paths.py "X"` (or `--all`). It reads his LinkedIn `Connections.csv` export from `tools/`, which is git-ignored. Then follow `career-ops/modes/contacto.md` for cold contacts. Check 2nd-degree paths with the search link it prints. Never send anything. |
| "Tailor my CV for X" or "make an ATS resume" | `career-ops/modes/ats.md` with `career-ops/templates/ats/cv-template.ats.html`, plus these steps: (1) act as the ATS parser and list every keyword, skill and requirement in the posting; (2) rewrite bullets to mirror that language using only facts from `profile/`; (3) give a before and after keyword match % and flag any line that reads as keyword stuffing. |
| "When do I follow up?", "why am I getting rejected?", interview or offer prep | `career-ops/modes/followup.md`, `patterns.md`, `interview-prep.md` or `offer-prep.md`. |
| Any other go-to-market request (outreach, positioning, research) | Pick the best skill from `gtm-skills/INDEX.md`, read its `SKILL.md` and follow it. Say which skill you picked. Ignore `swan.md` files. |

## The workflow

### 1. Profile

Read `profile/01-profile-and-icp.md`.

- **Missing or older than 3 months:** interview the user, at most 3 questions per message. Use their resume, a LinkedIn PDF export or their portfolio when they share one.
- **Facts disagree between sources:** list every conflict, and record where each fact came from.

### 2. ICP

Use the six gates in the profile file, in order:

1. Structural fit
2. Problem evidence
3. Exclusions
4. Reachability
5. Pay
6. Timing

Failing any gate excludes the company, and a strong result on one gate never rescues a failed one. The method is `gtm-skills/skills/tanyo-gochev/icp-matrix-builder/SKILL.md`.

### 3. Search

- **Split by segment:** Dev tools & AI, Fintech, B2B SaaS, Design tools. Run the segments in parallel when you can start subagents.
- **Sources:** company ATS boards (Ashby, Greenhouse, Lever, Workday, SmartRecruiters), LinkedIn public job pages, YC Work at a Startup, Wellfound and Remote Rocketship.
- **Re-check before adding:** confirm every company already in Linear still has a live posting.
- **When to stop:** when new queries mostly return companies you already have.
- **Rules (from `tam-builder`):**
  - One row per company, deduplicated by website domain.
  - Open the posting itself; never trust a search snippet.
  - Never infer a field. Write "unverified" instead.
  - Record the posting date and say whether it's a LinkedIn repost.

### 4. Tier

| Tier | Rule |
|---|---|
| Tier 1 | Passes all six gates; posted or reposted in the last 30 days |
| Tier 2 | Fits, but the posting is 30+ days old or one fact needs checking |
| Abroad | Outside India, and the posting itself states visa sponsorship or relocation help |
| Stretch | Asks more years than the profile has, sits below level, or the pay is unlikely to reach the floor |

Also record which case study to lead with, using the segment table in the profile file.

### 5. Save

Write `targets/YYYY-MM-DD-target-companies.md`:

- the tiered tables;
- what was searched;
- what was likely missed;
- the rejected companies, one line each with the reason.

Never edit an older dated file.

### 6. Sync to Linear

- **Project:** "Job Search System", team "Life".
- **Docs to update** (create if missing):

| Doc | Update with |
|---|---|
| Target companies | Replace the whole table with this run's results. Each company name links to its issue. |
| Run log | Add a dated entry at the top: segments searched, counts of new / still live / closed, and anything the user should check. |
| Profile & ICP | Only when the profile or ICP changed |

- **Issues: one per application (company + role).**
  - **Before creating one,** search the project for the company name. If an issue for the same role exists, update it instead. A different role at the same company gets its own issue.
  - **Title:** `Company — Role title`
  - **Labels:** one `job-tier`, one `job-segment`, and the `job-stage` label Shortlisted.
  - **New issues** start in Backlog.
  - **Description template:**

```
**Role:** [Role title](posting URL)
**Location:** as stated in the posting
**Posted:** date (note if LinkedIn repost)
**Pay:** as stated, or "not stated"
**Experience asked:** …
**What they make:** …
**Stage / funding:** … or "unverified"
**Why it fits:** one line
**Lead with:** case study
**Hiring manager:** name and title, or "unverified"
**Last checked:** YYYY-MM-DD
```

- **Updating existing issues:**
  - Refresh the description and the tier label.
  - If the posting has closed and the issue is still Shortlisted or Ready, move it to Canceled with a comment saying the posting is gone.
  - Never change an issue at stage Applied or later. Those belong to the user and the nightly email check.

## Tracking applications

The tracker uses stage labels on the Free plan's Life team. README.md has the stage table.

- **A stage change** means swapping the `job-stage` label, setting the matching Life status, setting the due date for the next action, and posting a comment:
  `STAGE <old> → <new> · <YYYY-MM-DD> · source: email <gmail message id> or manual · confidence: <high|medium|low>`
- **When the user tells you they applied, heard back, or withdrew,** make the change with `source: manual`. Ask for the channel (Cold apply / Referral / My outreach / Recruiter inbound) if it's unknown.
- **Never move an issue to Rejected, Ghosted or Withdrawn without the user's explicit go-ahead.**
- **The nightly email check** is the cloud routine "Nightly job-email check". It reads Gmail and writes the Daily digest, proposals and triage comments (issue "Unmatched job emails"). Don't duplicate its work. To change its behaviour, update the routine, not this file.
- **Email content never goes into this repo.** It's public. Rules, test sets and digests live in Linear.

## Never

- Apply to a job, message anyone, or sign in to a job site on the user's behalf. Finding and ranking only.
- Invent facts about the user or a company.

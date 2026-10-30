# Job search system

My job search as a product designer, in one repo. It does two things:

1. **Claude workflow.** Claude reads my profile, applies my ICP (the rules for which employers are worth applying to), searches for companies with live design roles that pass those rules, and writes the results to Linear as a tracker.
2. **Job scraper.** A Python script that pulls remote product-design jobs from public job boards every day and rebuilds a jobs dashboard.

Linear is where I track progress: [Job Search System project](https://linear.app/politiks/project/job-search-system-57c09ea78402).

## What's in the repo

| Path | What it is |
|---|---|
| `CLAUDE.md` | Instructions Claude follows when it works in this repo, including how to write to Linear |
| `profile/01-profile-and-icp.md` | My profile (from portfolio, resume and LinkedIn) and the ICP gates |
| `profile/designer-profile.md` | Answers for filling in application forms |
| `prompts/job-search-prompt.md` | A standalone prompt that runs the same workflow for anyone, in any AI agent |
| `targets/` | Each run's company list, one dated file per run |
| `tracking/applications-log.md` | Applications sent before the Linear tracker existed |
| `profile/linkedin-audit.md`, `profile/linkedin-post-ideas.md` | LinkedIn audit against 30 target job descriptions (headline, About, experience, skills), and 90 post ideas |
| `tools/warm_paths.py` | Who you know at a company, from your LinkedIn connections export (`tools/Connections.csv`, git-ignored) |
| `career-ops/` | Selected parts of [career-ops](https://github.com/career-ops-hq/career-ops) (MIT): evaluating one posting, finding contacts, an ATS CV template, cover letters, follow-ups, interview and offer prep. `career-ops/README.md` says how they fit in. |
| `gtm-skills/` | The [gtmskills.com](https://gtmskills.com) skill library (388 skills, MIT licence). `gtm-skills/INDEX.md` lists every skill in one line. |
| `orchestrator.py`, `requirements.txt`, `job-dashboard.html` | The job scraper and its dashboard |
| `.github/workflows/daily.yml` | Runs the scraper every day at 09:00 IST |
| `docs/related-repos.md` | 104 open-source repos for job scraping, resumes, AI job agents, networking and interviews, with the top 26 ranked for this setup |
| `docs/` | Scraper design and sources, a list of 88 job portals, and notes on auto-apply tools |

## How the Claude workflow runs

Open the repo in Claude Code (with the Linear connector enabled) and say **"run the job search"** or **"refresh the target companies"**. `CLAUDE.md` tells Claude what to do:

1. **Profile.** Read `profile/01-profile-and-icp.md`. If it's missing or stale, interview the user and rebuild it.
2. **ICP.** Apply the six gates: structural fit, problem evidence, exclusions, reachability, pay, timing. A company that fails any gate is out.
3. **Search.** Search company job boards (Ashby, Greenhouse, Lever, Workday, LinkedIn, YC and others), one search per industry segment, until new queries stop finding new companies. Every row is checked on the posting itself.
4. **Tier.** Sort the companies into Tier 1, Tier 2, Abroad or Stretch, and note which case study to lead with.
5. **Save.** Write `targets/YYYY-MM-DD-target-companies.md`.
6. **Sync to Linear.** Update the docs and create or update one issue per company (details below).

The skills behind it come from `gtm-skills/`:

- **ICP gates and tiers:** `icp-matrix-builder` by Tanyo Gochev.
- **List rules** (dedupe by website, never infer a field, report what was missed): `tam-builder` by Tanyo Gochev.
- **Reading postings:** `hiring-signal-prospecting` by Thomas Maitre.

To run it without this repo, paste `prompts/job-search-prompt.md` into any agent that has web search.

## What ends up in Linear

Project: **Job Search System** (team Life).

**Docs**

| Doc | What it holds |
|---|---|
| How this system works | This page, in short |
| Profile & ICP | The profile and the six gates |
| Target companies | The full table from the latest run, with a link to each issue |
| Run log | One entry per run: date, what was searched, what changed |
| Daily digest | Written by the nightly email check: what changed, what needs your decision, what's due |
| Weekly funnel | Written on Sundays: reply rate by channel and tier, days to first reply, applications with no next action |
| Tracking system design | How stages, channels and the email check work, and why |

**Issues: one per application (company + role)**

- **Title:** `Company — Role title`
- **Description:** the role link, location, posting date, pay, experience asked, what the company makes, stage, why it fits, which case study to lead with, and the hiring manager if named
- **Labels:**
  - `job-stage`: where the application is (table below)
  - `job-channel`: Cold apply, Referral, My outreach or Recruiter inbound
  - `job-tier`: Tier 1, Tier 2, Abroad or Stretch
  - `job-segment`: Dev tools & AI, Fintech, B2B SaaS or Design tools
- **Due date:** the next action. Every open application should have one.

**Stages**

On Linear's Free plan, stages are a label, and the Life team's status follows the stage.

| Stage label | Enters when | Life status | Next action |
|---|---|---|---|
| Shortlisted | Claude's search finds it | Backlog | Review it |
| Ready | You decide to apply | Todo | Apply, due in 3 days |
| Applied | A confirmation email arrives, or you give a date | Waiting | Follow up at 7 and 14 days |
| Screen | A recruiter call or assessment is booked | In Progress | Prepare, due the day before |
| Interviewing | An interview round is booked | In Progress | Prepare for the next round |
| Offer | Offer received | Done | Decide by the deadline |
| Rejected / Ghosted / Withdrawn | You confirm it | Canceled | — |

Every stage change adds a comment in this format, which the weekly report counts:

`STAGE <old> → <new> · <date> · source: email <id> or manual · confidence`

**When you change something yourself**, move the stage label and status, then add a `STAGE … · source: manual` comment. A one-line comment is enough.

**Nightly email check** (a cloud routine at 23:00 IST):

- It reads new job emails in Gmail. It may only search, read and add the `Jobs` / `Jobs/Processed` labels; send, reply, forward and trash are blocked.
- It matches each email to an issue. Anything it can't match goes to the triage issue, never a guess.
- It records a STAGE comment for each change and writes the Daily digest.
- During the dry run (until 4 Nov 2026) it only proposes changes.
- After that it applies confirmations and screen or interview invites automatically.
- Rejected, Ghosted and Withdrawn always wait for your approval: reply "approve" on the proposal.

On a refresh of the company list, Claude:

- adds new companies as Shortlisted;
- updates the details on existing issues;
- marks an issue Canceled only if its posting has closed **and** it's still Shortlisted or Ready.

It never changes an issue at Applied or later.

## Running the scraper

```bash
pip install -r requirements.txt
python orchestrator.py
```

This pulls live roles from 8 job-board APIs (including FreeHire, which pulls postings from company career pages, and Hacker News' "Who is hiring?" and YC job posts) and LinkedIn's no-login job feed. It writes `jobs.json` and rebuilds `job-dashboard.html`. Setting `SMTP_USER`, `SMTP_PASS` and `DIGEST_TO` turns on an email of new roles. Details are in [docs/scraper.md](docs/scraper.md).

## Privacy

This repo is public. It contains my profile, contact details, salary expectations and application history.

## Credits

`gtm-skills/` is a copy of [swan-gtm/gtm-skills](https://github.com/swan-gtm/gtm-skills), MIT-licensed; see `gtm-skills/LICENSE`. Each skill's author is credited in its own folder.

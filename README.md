# Remote Product Designer Job Scraper

A self-contained, multi-engine job scraper with automatic fallback. Runs anywhere Python runs — no Aside, no external service required for the core.

## What's inside

| File | Purpose |
|------|---------|
| `orchestrator.py` | The engine. Scrapes job portals with tier-based fallback, writes `jobs.json`, rebuilds the dashboard, and emails new roles. |
| `job-dashboard.html` | Standalone jobs page (search + filter + apply). Open in any browser. Regenerated each run. |
| `job-scraping-system.md` | The full design: 9-tool engine pool, fallback workflow, portal list, extracted jobs. |
| `job-scraper-sources.md` | Every scrapable endpoint + tips. |
| `remote-product-designer-jobs.md` | Human-readable job tracker. |
| `designer-profile.md` | Your "apply on my behalf" profile (fill in the TODOs). |
| `job-portals.md` / `job-portals.csv` | Master list of 74 job portals, tagged by scrape access + fallback tier. |
| `.github/workflows/daily.yml` | Cloud cron — runs the scraper daily and emails you. |

## Quick start

```bash
pip install -r requirements.txt
python orchestrator.py
```

This pulls live roles from 6 JSON APIs + LinkedIn's guest feed (Tier 0–1, no login),
writes `jobs.json`, and regenerates `job-dashboard.html`. Open the HTML to browse.

## Enable email alerts (replaces the old Aside routine)

Set these environment variables, then run the script:

```bash
export SMTP_USER="sriram.kansala@gmail.com"
export SMTP_PASS="your_gmail_app_password"   # https://myaccount.google.com/apppasswords
export DIGEST_TO="sriram.kansala@gmail.com"
python orchestrator.py
```

You'll get an email only when there are **new** roles since the last run (it diffs against `jobs.json`).

## Automate it

**Option A — local cron (Mac/Linux):**
```cron
0 9 * * * cd ~/Documents/job-scraper && /usr/bin/python3 orchestrator.py
```

**Option B — GitHub Actions (cloud, no machine needed):**
1. Push this folder to a GitHub repo.
2. In repo Settings → Secrets and variables → Actions, add: `SMTP_USER`, `SMTP_PASS`, `DIGEST_TO`.
3. `.github/workflows/daily.yml` runs it every day at 09:00 IST and emails you. It also commits the updated `jobs.json`/dashboard back to the repo.

## Scale to protected sites

`orchestrator.py` ships with Tier 0–1 working and **stub functions** for the heavier engines
(`make_scrapling_stealthy`, `make_patchright`, `make_agentql`, …). To cover anti-bot portals
(Naukri, Wellfound, Indeed), implement a stub and add it to that portal's chain in the
`PORTALS` registry. See `job-scraping-system.md` for the tier map.

## Fallback model

```
Tier 0 API/RSS → Tier 1 static HTML → Tier 2 JS render → Tier 3 anti-bot → Tier 4 AI agent → manual review
```
For each portal, the orchestrator tries engines cheapest-first, escalates on block/empty/captcha,
and caches the winning engine in `portal_cache.json` so the next run starts there.

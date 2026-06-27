# Auto-Apply & Form-Fill Tools (GitHub)
_9 catalogued. Generated 2026-06-27._

Open-source projects that auto-fill or auto-submit job applications. Useful for the "fill the apply links" goal — read the safety note first.

| Tool | Repo | Lang | Stars | License | Supported sites | Status | Notes |
|---|---|---|---|---|---|---|---|
| AIHawk (Jobs_Applier_AI_Agent) | feder-cr/Jobs_Applier_AI_Agent_AIHawk | Python | 29.9k | AGPL-3.0 | LinkedIn, Indeed + | ARCHIVED (May 2026) | Most-starred but archived; AI scores + applies. Unmaintained = risky. |
| LinkedIn AI Auto Job Applier | GodsScion/Auto_job_applier_linkedIn | Python | 2.5k | AGPL-3.0 | LinkedIn Easy Apply | Active (Apr 2026) | Finds jobs, answers Qs, tailors resume via OpenAI, auto-applies. Selenium. |
| ApplyPilot | Pickle-Pixel/ApplyPilot | Python | 1.1k | AGPL-3.0 | Any site / any form | Active (v0.3.0) | AI agent + Playwright; generates cover letters, autofills. General-purpose. |
| EasyApplyJobsBot | wodsuz/EasyApplyJobsBot | Python | 790 | Custom | LinkedIn, Glassdoor | Active (Mar 2026) | Auto-login + autofill Easy Apply. Some paid Pro features. |
| job-apply-plugin | neonwatty/job-apply-plugin | JS (Claude plugin) | 43 | MIT | LinkedIn, Greenhouse, Ashby, Lever, Rippling, Workday | Active (v1.0) | BEST FIT: form-FILL (not blind submit) across the exact ATSs you face. MIT license. |
| AutoApplyMax | Azoo92i/AutoApplyMax | JS (Chrome ext) | 39 | AGPL-3.0 | LinkedIn, Indeed + | Active (Apr 2026) | Browser extension; AI cover letters. Easiest to install (no coding). |
| OpenClaw | hkaanturgut/OpenClaw | Python | 13 | None | Google Jobs API + email | Active (self-host) | Nightly agent; drafts emails, you click to send. No-license = use cautiously. |
| job-autopilot | Schlaflied/job-autopilot | Python | 10 | GPL-3.0 | LinkedIn + cold email | Active (basic) | GPT-4 pipeline; auto-connect + resume optimization. |
| LinkedIn Apply Bot | adnanedrief | Node | 48 | None | LinkedIn | Unknown (2024) | Puppeteer auto-apply. Stale; no license. |

## Recommendation
For your case (Greenhouse / Lever / Ashby / Workday + LinkedIn), **neonwatty/job-apply-plugin** is the closest match: it FILLS forms across exactly those ATSs and leaves the final submit to you (MIT-licensed). That mirrors the safe approach we agreed on — autofill, you approve each send.

## Safety note (important)
- **Blind auto-SUBMIT bots on LinkedIn violate its Terms** and can get your real account restricted or banned. The high-star Python bots (AIHawk, GodsScion) auto-submit — higher risk.
- **Form-FILL tools** that stop before submit (job-apply-plugin) are far safer and keep quality high.
- **No-license repos** (OpenClaw, LinkedIn Apply Bot) grant no legal usage rights — avoid beyond reading.
- Recommended: assisted **fill + human approve** (what we agreed), not unattended bulk auto-submit.

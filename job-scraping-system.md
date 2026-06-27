# Job Scraping System — Tools, Workflow, Jobs & Portals
_Generated 2026-06-27 · For: Sriram (Product Designer, remote, India + Worldwide)_

This document captures a multi-engine scraping system. The idea: when you hit **"Scrape"**, an orchestrator tries the cheapest method first and, if a site blocks or returns nothing, automatically **escalates to the next engine** until one succeeds (or all are exhausted). Below are the three requested lists plus the workflow that ties them together.

---

## ⚙️ How the combined fallback workflow works

```
            ┌─────────────────────────────────────────────┐
  SCRAPE →  │  ORCHESTRATOR (per-portal escalation loop)   │
            └─────────────────────────────────────────────┘
   For each PORTAL, try ENGINES in tier order. On block / empty / captcha
   / timeout → escalate to next engine. Cache "what worked" per portal so
   next run starts at the winning tier.

  TIER 0  Official API / RSS ............ httpx / Scrapling Fetcher
          (RemoteOK, Remotive, Jobicy, Arbeitnow, Working Nomads, WWR RSS,
           LinkedIn guest endpoint)              ✅ cheapest, no browser
                       │ fail ↓
  TIER 1  Static HTML + TLS impersonation ... Scrapling Fetcher · Scrapy · Crawlee (Cheerio)
                       │ fail ↓
  TIER 2  JS-rendered pages ................. Crawl4AI · Crawlee (Playwright) · Scrapling DynamicFetcher
                       │ fail ↓
  TIER 3  Anti-bot (Cloudflare/Datadome/Akamai) ... Patchright · Scrapling StealthyFetcher · Camoufox
                       │ fail ↓
  TIER 4  Hard / dynamic / login / changing DOM ... AgentQL (query) · Stagehand (act+extract) · Browser-Use (autonomous)
                       │ fail ↓
            ❌ mark portal "needs manual review" + log reason
```

**Escalation triggers (what counts as "failed, try next"):**
- HTTP 403 / 429 / 999, redirect to `/checkpoint`, `/authwall`, or a Cloudflare/Datadome interstitial
- Empty result set or selector returns 0 items on a page that should have jobs
- CAPTCHA / Turnstile detected
- Timeout or JS-render never settles (network idle never reached)

**Per-portal memory:** store `{portal: winningTier, lastSuccess, selectorMap}` so repeat runs skip straight to the engine that worked last time, and only re-escalate if it breaks.

**Normalize everything** to one shape so all engines feed the same output:
`{ source, title, company, location, region, level, date, url }` → dedupe by URL → push to the dashboard + daily email digest.

---

## 📋 LIST 1 — Scraping GitHub repos / tools (the engine pool)

| # | Tool | Repo / Site | Lang | Tier | What it's best at | Anti-bot |
|---|------|-------------|------|------|-------------------|----------|
| 1 | **Patchright** | github.com/Kaliiiiiiiiii-Vinyzu/patchright | Py / Node / .NET | 3 | Drop-in **undetected Playwright** (Chromium only). Patches Runtime.enable/Console leaks, webdriver flags, closed shadow roots. | Passes Cloudflare, Kasada, Akamai, Datadome, F5, Fingerprint.com |
| 2 | **Browser-Use** | browser-use.com | Python | 4 | **Autonomous LLM browser agent** — give it a goal ("find product designer jobs"), it navigates & extracts. Best for unknown/changing sites. | Inherits underlying browser stealth |
| 3 | **Stagehand** | stagehand.dev | TS / Node | 4 | AI browser automation on Playwright with `act()` / `extract()` / `observe()`. Mix deterministic code + AI steps. | Works with Browserbase stealth |
| 4 | **AgentQL** | agentql.com | Py / JS (SaaS) | 4 | **AI query language** — describe data shape, it self-heals against DOM changes. Works behind auth; REST "browserless" mode + PDF parsing. | Hosted remote browsers |
| 5 | **Scrapy** | scrapy.org | Python | 1 | Battle-tested **large-scale crawl framework** — pipelines, middlewares, concurrency, retries. The workhorse for static/structured sites. | Add-ons (scrapy-impersonate) |
| 6 | **Crawlee** | crawlee.dev | TS / Python | 1-2 | Unified **Cheerio + Playwright/Puppeteer** crawler (Apify). Auto request queue, proxy & session rotation, autoscaling. | Built-in fingerprinting + proxy rotation |
| 7 | **Camoufox** | camoufox.com | Python | 3 | **Anti-detect Firefox** for AI agents. C++-level fingerprint injection (no JS traces), rotation, ~200MB, Playwright-compatible. | Tor/Arkenfox-grade fingerprint resistance |
| 8 | **Crawl4AI** | docs.crawl4ai.com | Python | 2 | **LLM-friendly crawler** — renders JS, outputs clean Markdown/structured data ready for AI. Async, fast. | Basic stealth, proxy support |
| 9 | **Scrapling** | github.com/D4Vinci/Scrapling | Python | 0-3 | **Adaptive all-rounder**: Fetcher (TLS impersonate), StealthyFetcher (auto-solves Cloudflare Turnstile), DynamicFetcher (Playwright), Spider framework, **self-healing selectors**, MCP server. | StealthyFetcher bypasses Cloudflare out of the box |

> Pairing tip: **Patchright** or **Camoufox** provide the stealthy *browser*; **Stagehand / Browser-Use / AgentQL** provide the *intelligence*; **Scrapy / Crawlee / Scrapling / Crawl4AI** provide the *crawl scaffolding*. The orchestrator picks the lightest combo that works per portal.

---

## 🌐 LIST 2 — Job portals available (scrape targets)

Verified live this session (✅) plus known targets per tier.

| Portal | Endpoint / URL | Access | Tier needed |
|--------|----------------|--------|-------------|
| ✅ RemoteOK | `remoteok.com/api` | JSON, no auth | 0 |
| ✅ Remotive | `remotive.com/api/remote-jobs?category=design` | JSON, no auth | 0 |
| ✅ Jobicy | `jobicy.com/api/v2/remote-jobs?tag=design` | JSON, no auth | 0 |
| ✅ Arbeitnow | `arbeitnow.com/api/job-board-api` | JSON, no auth | 0 |
| ✅ Working Nomads | `workingnomads.com/api/exposed_jobs/` | JSON, no auth | 0 |
| ✅ Himalayas | `himalayas.app/jobs/api` | JSON, no auth | 0 |
| ✅ LinkedIn (guest) | `linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search` | HTML cards, no login | 1 |
| ✅ We Work Remotely | `weworkremotely.com/categories/remote-design-jobs.rss` | RSS | 0 |
| Remote.co | `remote.co/remote-jobs/design/feed/` | RSS | 0-1 |
| Jobspresso | `jobspresso.co/?feed=job_feed&job_categories=design` | RSS | 0-1 |
| Wellfound (AngelList) | `wellfound.com/role/r/product-designer` | JS app | 2-3 |
| YC Work at a Startup | `workatastartup.com` | login GraphQL | 4 |
| Dribbble Jobs | `dribbble.com/jobs` | HTML | 1-2 |
| Built In | `builtin.com/jobs/design` | HTML, paginated | 1-2 |
| Otta / Welcome to the Jungle | `app.otta.com` | login | 4 |
| Indeed | `indeed.com` | Cloudflare anti-bot | 3 |
| Naukri (India) | `naukri.com` | anti-bot | 3 |
| Instahyre (India) | `instahyre.com` | login API | 4 |
| Cutshort (India) | `cutshort.io` | login | 4 |
| Foundit (India) | `foundit.in` | HTML | 2 |

---

## 💼 LIST 3 — Extracted jobs (81 roles, this run)

India: 48 · Worldwide: 12 · Region-locked: 21. Sorted India → Worldwide → other, newest first.

| # | Title | Company | Region | Location | Level | Date | Source | Link |
|---|-------|---------|--------|----------|-------|------|--------|------|
| 1 | Product Designer | Upgame - By Trackman | India | Chandigarh, India | Mid | 2026-06-27 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-upgame-by-trackman-4430640686) |
| 2 | User Experience Designer | Duruper | India | Bengaluru, Karnataka, India | Mid | 2026-06-27 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/user-experience-designer-at-duruper-4427319515) |
| 3 | Product Designer, Design Systems | Epicor | India | Hyderabad, Telangana, India | Mid | 2026-06-26 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-design-systems-at-epicor-4423509981) |
| 4 | UIUX Designer | HP | India | Bengaluru, Karnataka, India | Mid | 2026-06-26 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/uiux-designer-at-hp-4432972643) |
| 5 | Associate Product Designer (UI/UX) | Ebitaus | India | Chennai, Tamil Nadu, India | Junior | 2026-06-26 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/associate-product-designer-ui-ux-at-ebitaus-4430380892) |
| 6 | Product Designer, Zudo | Airblack | India | Gurugram, Haryana, India | Mid | 2026-06-25 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-zudo-at-airblack-4419654882) |
| 7 | Product Designer | Accenture in India | India | Bengaluru, Karnataka, India | Mid | 2026-06-25 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-accenture-in-india-4408960912) |
| 8 | Junior UI/UX Designer | AIQ Space Ventures | India | Mumbai, Maharashtra, India | Junior | 2026-06-25 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/junior-ui-ux-designer-at-aiq-space-ventures-4430210410) |
| 9 | Senior UI UX Designer | Tarento Group | India | Bengaluru, Karnataka, India | Senior | 2026-06-25 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/senior-ui-ux-designer-at-tarento-group-4432128860) |
| 10 | Senior UI/UX Designer | NetApp | India | Bengaluru, Karnataka, India | Senior | 2026-06-25 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/senior-ui-ux-designer-at-netapp-4426898377) |
| 11 | Product Designer - B2B SaaS | ixigo | India | Gurugram, Haryana, India | Mid | 2026-06-24 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-b2b-saas-at-ixigo-4432528963) |
| 12 | Product Designer, Adobe Express | Adobe | India | Bengaluru East, Karnataka, India | Mid | 2026-06-23 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-adobe-express-at-adobe-4431274835) |
| 13 | Product Designer - 2 | Acko | India | Bengaluru, Karnataka, India | Mid | 2026-06-23 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-2-at-acko-4423201549) |
| 14 | Product Designer II | Nykaa | India | Gurugram, Haryana, India | Mid | 2026-06-23 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-ii-at-nykaa-4430896236) |
| 15 | Product Designer | Aditya Birla Capital | India | Maharashtra, India | Mid | 2026-06-23 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-aditya-birla-capital-4422143090) |
| 16 | UI/UX Designer | Abusiness -&gt; SAP BTP, Integration Suite Developers | India | Gurugram, Haryana, India | Mid | 2026-06-23 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/ui-ux-designer-at-abusiness-sap-btp-integration-suite-developers-4429454766) |
| 17 | Product Designer | Glean | India | Bengaluru, Karnataka, India | Mid | 2026-06-22 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-glean-4372066055) |
| 18 | Senior UI/UX Designer | Cyara | India | Hyderabad, Telangana, India | Senior | 2026-06-19 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/senior-ui-ux-designer-at-cyara-4430903070) |
| 19 | Product Designer | Coding Ninjas | India | Gurugram, Haryana, India | Mid | 2026-06-17 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-coding-ninjas-4425078595) |
| 20 | Product Designer - Design Systems | JioStar | India | Bengaluru, Karnataka, India | Mid | 2026-06-16 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-design-systems-at-jiostar-4429244267) |
| 21 | Associate UX Designer | Taazaa Inc | India | Noida, Uttar Pradesh, India | Junior | 2026-06-16 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/associate-ux-designer-at-taazaa-inc-4429508966) |
| 22 | Product Designer - 2 | Navi | India | Bengaluru, Karnataka, India | Mid | 2026-06-15 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-2-at-navi-4427482142) |
| 23 | Product Designer | Everstage | India | Chennai, Tamil Nadu, India | Mid | 2026-06-12 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-everstage-4426907205) |
| 24 | User Experience Designer | JoVE | India | Delhi, India | Mid | 2026-06-12 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/user-experience-designer-at-jove-4427208116) |
| 25 | Product Designer II | Adobe | India | Noida, Uttar Pradesh, India | Mid | 2026-06-10 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-ii-at-adobe-4426063256) |
| 26 | Product Designer 2 | IDfy | India | Mumbai Metropolitan Region | Mid | 2026-06-10 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-2-at-idfy-4422688622) |
| 27 | Product Designer | Blitz | India | Greater Bengaluru Area | Mid | 2026-06-10 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-blitz-4422284766) |
| 28 | Product Designer | Raise Financial Services | India | Mumbai, Maharashtra, India | Mid | 2026-06-09 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-raise-financial-services-4422259103) |
| 29 | Product Designer | GreedyGame | India | Bengaluru, Karnataka, India | Mid | 2026-06-09 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-greedygame-4425551744) |
| 30 | Product Designer | Zerodha Fund House | India | Bengaluru, Karnataka, India | Mid | 2026-06-06 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-zerodha-fund-house-4424639476) |
| 31 | Product Designer | Grexa AI | India | Mumbai Metropolitan Region | Mid | 2026-06-04 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-grexa-ai-4420719889) |
| 32 | Product Designer | Instead | India | Bengaluru, Karnataka, India | Mid | 2026-06-03 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-instead-4420116406) |
| 33 | Product Design Assistant | TalentPop App | India | Bengaluru East, Karnataka, India | Junior | 2026-06-02 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-design-assistant-at-talentpop-app-4419606707) |
| 34 | Product Design Assistant | TalentPop App | India | Hyderabad, Telangana, India | Junior | 2026-06-02 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-design-assistant-at-talentpop-app-4419616665) |
| 35 | Product Designer | Laundryheap | India | Bengaluru, Karnataka, India | Mid | 2026-06-01 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-laundryheap-4421684779) |
| 36 | Product Designer | Delivery Hero | India | India | Mid | 2026-05-31 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-delivery-hero-4421634363) |
| 37 | UI/UX Designer | Tarento Group | India | Delhi, India | Mid | 2026-05-20 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/ui-ux-designer-at-tarento-group-4416179282) |
| 38 | Product Designer | Sarvam | India | Bengaluru, Karnataka, India | Mid | 2026-05-19 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-sarvam-4416602608) |
| 39 | Product Designer | ShopDeck | India | Bengaluru, Karnataka, India | Mid | 2026-05-15 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-shopdeck-4414977652) |
| 40 | UI/UX Product Designer | Valerie Group | India | Bengaluru East, Karnataka, India | Mid | 2026-04-29 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/ui-ux-product-designer-at-valerie-group-4408227687) |
| 41 | Entry-Level Product Designer (UX/UI) – Execution Focus, AI-Enabled Products | The Asia Group | India | Gurugram, Haryana, India | Junior | 2026-04-21 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/entry-level-product-designer-ux-ui-%E2%80%93-execution-focus-ai-enabled-products-at-the-asia-group-4404574855) |
| 42 | Product Designer | GoSats - The simplest onramp to Digital Assets in India | India | Bengaluru, Karnataka, India | Mid | 2026-04-19 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-gosats-the-simplest-onramp-to-digital-assets-in-india-4403080505) |
| 43 | UX Designer | Coulomb AI | India | Karnataka, India | Mid | 2026-03-26 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/ux-designer-at-coulomb-ai-4404381517) |
| 44 | Product Designer at a Stealth Startup | Katapult | India | Mumbai Metropolitan Region | Mid | 2026-02-01 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/product-designer-at-a-stealth-startup-at-katapult-4367758277) |
| 45 | Lead Product Designer | qoohoo | India | Bengaluru, Karnataka, India | Lead+ | 2025-12-30 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/lead-product-designer-at-qoohoo-4346578178) |
| 46 | UI and UX designer Fresher | BiCSoM | India | Bengaluru, Karnataka, India | Junior | 2025-09-10 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/ui-and-ux-designer-fresher-at-bicsom-4298730042) |
| 47 | Senior UI/UX Designer | Gramener | India | Greater Chennai Area | Senior | 2025-08-18 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/senior-ui-ux-designer-at-gramener-4288308792) |
| 48 | Senior UI/UX Designer | Coditude | India | Pune/Pimpri-Chinchwad Area | Senior | 2025-06-09 | LinkedIn | [apply](https://in.linkedin.com/jobs/view/senior-ui-ux-designer-at-coditude-4247426293) |
| 49 | Junior UX UI Designer | Work Force Nexus | Worldwide | Remote,  | Junior | 2026-06-24 | RemoteOK | [apply](https://remoteOK.com/remote-jobs/remote-junior-ux-ui-designer-work-force-nexus-1134022) |
| 50 | Product Designer Design Systems | Penn Interactive | Worldwide | Worldwide | Mid | 2026-06-16 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-design-systems-penn-interactive-1133499) |
| 51 | Product Designer | Gocertify | Worldwide | Worldwide | Mid | 2026-05-23 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-gocertify-1131914) |
| 52 | UX UI Designer — AI Application | 0g Labs | Worldwide | Probably worldwide | Mid | 2026-04-23 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-ux-ui-designer-ai-application-0g-labs-1131295) |
| 53 | Senior UX Researcher & Analyst | Casechek | Worldwide | Worldwide | Senior | 2026-04-10 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-senior-ux-researcher-analyst-casechek-1131059) |
| 54 | Product Designer | Sharebite | Worldwide | Worldwide | Mid | 2026-04-09 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-sharebite-1131049) |
| 55 | Product Designer | OpenRouter | Worldwide | Probably worldwide | Mid | 2026-03-27 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-openrouter-1130894) |
| 56 | Lead Product Designer | Alpaca | Worldwide | Worldwide | Lead+ | 2026-03-19 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-lead-product-designer-alpaca-1130835) |
| 57 | Lead Product Designer | Circle.so | Worldwide | Worldwide | Lead+ | 2026-03-16 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-lead-product-designer-circle-so-1130791) |
| 58 | Product Designer Creators | VRChat | Worldwide | Anywhere | Mid | 2026-02-25 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-creators-vrchat-1130544) |
| 59 | Product Designer | OnePay | Worldwide | Probably worldwide | Mid | 2025-12-05 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-onepay-1129110) |
| 60 | Product Designer | Khan Academy | Worldwide | Probably worldwide | Mid | 2016-07-15 | RemoteOK | [apply](https://remoteok.com/remote-jobs/18070-remote-product-designer-khan-academy) |
| 61 | Director, Product Design | Samsara | Region-locked | USA | Lead+ | 2026-06-25 | Jobicy | [apply](https://jobicy.com/jobs/143046-director-product-design) |
| 62 | Junior UI designer (Marketing team) | TechMagic | Region-locked | Ukraine | Junior | 2026-06-25 | Jobicy | [apply](https://jobicy.com/jobs/143375-junior-ui-designer-marketing-team) |
| 63 | UI/UX Designer | ManTech | Region-locked | USA | Mid | 2026-06-25 | Jobicy | [apply](https://jobicy.com/jobs/143624-ui-ux-designer) |
| 64 | Director of Product Design (Canada) | Proof | Region-locked | Canada | Lead+ | 2026-06-25 | Jobicy | [apply](https://jobicy.com/jobs/144694-director-of-product-design-canada) |
| 65 | Senior Product Manager - Product Design Simulation in Fusion | Autodesk | Region-locked | EMEA,  Germany,  Poland,  Spain | Senior | 2026-06-18 | Jobicy | [apply](https://jobicy.com/jobs/145063-senior-product-manager-product-design-simulation-in-fusion) |
| 66 | Senior Product Manager - Product Design Simulation in Fusion | Autodesk | Region-locked | EMEA,  Germany | Senior | 2026-06-17 | Jobicy | [apply](https://jobicy.com/jobs/146985-senior-product-manager-product-design-simulation-in-fusion-2) |
| 67 | Senior Product Designer (UX Specialist) - Media Company | Truelogic | Region-locked | LATAM | Senior | 2026-06-16 | Jobicy | [apply](https://jobicy.com/jobs/146873-senior-product-designer-ux-specialist-media-company) |
| 68 | Senior UI & UX / Graphic Designer | Lemon.io | Region-locked | Europe, North America, Latin America, APAC | Senior | 2026-06-11 | WorkingNomads | [apply](https://www.workingnomads.com/job/go/1658647/) |
| 69 | Senior User Experience Designer - AEC Platform Data | Autodesk | Region-locked | EMEA,  UK | Senior | 2026-06-10 | Jobicy | [apply](https://jobicy.com/jobs/146034-senior-user-experience-designer-aec-platform-data) |
| 70 | Product Designer | Butter | Region-locked | San Francisco Bay Area | Mid | 2026-06-09 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-butter-1133097) |
| 71 | Product Designer | Nevis | Region-locked | United States | Mid | 2026-06-03 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-nevis-1132791) |
| 72 | Product Designer | South Geeks | Region-locked | United States | Mid | 2026-05-27 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-south-geeks-1132403) |
| 73 | Product Designer | DesignMeshAI | Region-locked | United Kingdom | Mid | 2026-05-27 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-designmeshai-1132393) |
| 74 | Product Designer | Heidi | Region-locked | Australia | Mid | 2026-05-26 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-heidi-1132448) |
| 75 | Product Designer | Cint | Region-locked | United Kingdom | Mid | 2026-05-20 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-cint-1131922) |
| 76 | Staff Product Designer Business Banking | Monzo | Region-locked | United Kingdom | Lead+ | 2026-05-08 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-staff-product-designer-business-banking-monzo-1131519) |
| 77 | Senior Product Designer | Fluxon | Region-locked | United States | Senior | 2026-04-17 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-senior-product-designer-fluxon-1131196) |
| 78 | Product Designer | Bjak | Region-locked | United Kingdom | Mid | 2026-04-16 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-bjak-1131156) |
| 79 | Senior Product Designer | Kiefer | Region-locked | Greece | Senior | 2026-04-10 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-senior-product-designer-kiefer-1131074) |
| 80 | Product Designer | Skio | Region-locked | United States | Mid | 2026-01-13 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-product-designer-skio-1129544) |
| 81 | Member of Product Design Digital Assets | Anchorage Digital | Region-locked | United States | Mid | 2025-10-31 | RemoteOK | [apply](https://remoteok.com/remote-jobs/remote-member-of-product-design-digital-assets-anchorage-digital-1128734) |

---

## 🚧 Honest implementation note
These 9 tools are Python/Node frameworks that run on **your machine or a server** — they can't be pip/npm-installed inside this chat sandbox. So this doc is the **blueprint + the live data**. I can also generate a ready-to-run `orchestrator.py` that implements the tier-escalation loop above (starting with the Tier-0 APIs that already work, with stubs to plug in Patchright/Scrapling/etc.), and we can host it so your "Scrape" button triggers it. Say the word and I'll write that script.

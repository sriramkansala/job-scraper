# Remote Job Board Sources — Scraper Reference

Tested 2026-06-27. These are remote/design job boards with clean, no-auth endpoints you can hit with a custom scraper. ✅ = verified working this session.

## Clean JSON APIs (best for scraping)

| Board | Endpoint | Notes |
|---|---|---|
| ✅ RemoteOK | `https://remoteok.com/api` | Full feed (~100 recent). Tag filter: `?tags=design`. First array item is metadata; skip it. Fields: `position, company, location, tags, url, date`. |
| ✅ Remotive | `https://remotive.com/api/remote-jobs?category=design&limit=100` | Clean JSON `{jobs:[...]}`. Fields: `title, company_name, candidate_required_location, url, tags, publication_date`. |
| ✅ Jobicy | `https://jobicy.com/api/v2/remote-jobs?count=50&tag=design` | `{jobs:[...]}`. Use `tag=design` (NOT `industry=design`, which 400s). Supports `geo=` too. Fields: `jobTitle, companyName, jobGeo, url, pubDate`. |
| ✅ Arbeitnow | `https://www.arbeitnow.com/api/job-board-api` | `{data:[...]}`, ~100 jobs, paginated. Fields: `title, company_name, location, remote, url, tags, created_at` (unix). |
| ✅ Working Nomads | `https://www.workingnomads.com/api/exposed_jobs/` | Plain array, ~50 jobs. Fields: `title, company_name, location, category_name, tags, url, pub_date`. |
| ✅ Himalayas | `https://himalayas.app/jobs/api?limit=20&offset=0` | `{jobs:[...], totalCount}`. Paginate via `offset`. Note: their `query` param is ignored, so filter client-side. Fields: `title, companyName, companySlug, seniority, minSalary, maxSalary, locationRestrictions`. |
| ✅ LinkedIn (guest) | `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=product%20designer&location=India&f_WT=2&sortBy=DD&start=0` | No login needed. Returns HTML cards (`<li>`). Parse `<h3>` title, company, `job-search-card__location`, `datetime`, and `/jobs/view/<id>` link. `f_WT=2` = remote. Paginate with `start=0,10,20...`. **Richest source for India.** |

## RSS feeds (parse XML)

| Board | Feed |
|---|---|
| ✅ We Work Remotely | `https://weworkremotely.com/categories/remote-design-jobs.rss` (30 most recent; noisy, filter to digital roles) |
| Remote.co | `https://remote.co/remote-jobs/design/feed/` |
| Jobspresso | `https://jobspresso.co/?feed=job_feed&job_categories=design` |
| Authentic Jobs | `https://authenticjobs.com/rss/custom.php` |

## Harder targets (HTML scrape / anti-bot)

- **Wellfound (AngelList)** — `wellfound.com/role/r/product-designer` — heavy JS, needs headless browser.
- **Y Combinator – Work at a Startup** — `workatastartup.com` — login-gated GraphQL.
- **Dribbble Jobs** — `dribbble.com/jobs` — HTML scrape.
- **Built In** — `builtin.com/jobs/design` — HTML scrape, pagination.
- **Otta / Welcome to the Jungle** — `app.otta.com` — login-gated.
- **Indeed** — strong anti-bot (Cloudflare); avoid scraping, use their email alerts instead.

### India-specific boards
- **Naukri** — `naukri.com` — anti-bot; best via account + email alerts.
- **Instahyre** — `instahyre.com` — login-gated API.
- **Cutshort** — `cutshort.io` — login-gated.
- **Foundit (ex-Monster India)** — `foundit.in` — HTML scrape.

## Scraper tips
- Set a real `User-Agent` header (e.g. a Chrome UA) or some boards 403.
- Most feeds are small "recent" snapshots; run on a schedule and dedupe by URL/job-id to build history.
- Normalize to a common shape: `{source, title, company, location, region, date, url, level}`.
- Derive seniority from the title (junior/associate/entry vs senior vs lead/staff/principal).

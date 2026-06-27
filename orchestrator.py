#!/usr/bin/env python3
"""
Multi-engine job scraping orchestrator with automatic fallback.

Idea: one `scrape()` entry point. For each portal it tries engines from the
cheapest tier upward. If an engine is blocked / returns nothing / hits a
captcha, it escalates to the next engine until one succeeds or all are
exhausted. A small per-portal cache remembers the winning engine so the next
run starts there.

Tier 0  Official API / RSS .............. httpx (works today, no deps beyond httpx)
Tier 1  Static HTML + TLS impersonation .. Scrapling Fetcher / Scrapy / Crawlee
Tier 2  JS render ........................ Crawl4AI / Crawlee(Playwright) / Scrapling Dynamic
Tier 3  Anti-bot ......................... Patchright / Scrapling Stealthy / Camoufox
Tier 4  Hard/dynamic/login ............... AgentQL / Stagehand / Browser-Use

Install (only what you use):
    pip install httpx feedparser
    pip install scrapling && scrapling install        # tiers 0-3 in one lib
    pip install crawl4ai patchright camoufox browser-use agentql scrapy crawlee

Run:
    python orchestrator.py
"""
from __future__ import annotations
import json, re, time, html, datetime as dt
from dataclasses import dataclass, asdict
from typing import Callable, Optional

import httpx

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

# ---------------------------------------------------------------- data model
@dataclass
class Job:
    source: str
    title: str
    company: str
    location: str
    region: str
    level: str
    date: str
    url: str

def seniority(title: str) -> str:
    t = title.lower()
    if re.search(r"lead|principal|staff|head|director|\bvp\b", t): return "Lead+"
    if re.search(r"senior|\bsr\b", t): return "Senior"
    if re.search(r"junior|associate|entry|assistant|fresher|trainee", t): return "Junior"
    return "Mid"

def region_of(loc: str) -> str:
    l = (loc or "").lower()
    if "india" in l: return "India"
    if any(w in l for w in ("worldwide", "anywhere", "remote", "global")): return "Worldwide"
    return "Region-locked"

DESIGN = re.compile(r"product\s*design|ux|ui|user\s*experience|user\s*interface|interaction design|design system", re.I)
NOT_DESIGN = re.compile(r"engineer|developer|architect|sales|recruit|hr\b|data entry|scheduler", re.I)
def is_design(title: str) -> bool:
    return bool(title and DESIGN.search(title) and not NOT_DESIGN.search(title))

class Blocked(Exception):
    """Raised by an engine when it is blocked / empty / captcha'd so the
    orchestrator escalates to the next engine."""

# ---------------------------------------------------------------- TIER 0 engines (working today)
def t0_remoteok(_) -> list[Job]:
    d = httpx.get("https://remoteok.com/api", headers=UA, timeout=30).json()
    out = []
    for j in d[1:]:
        if is_design(j.get("position", "")):
            out.append(Job("RemoteOK", j["position"], j.get("company", ""), j.get("location", "Remote"),
                           region_of(j.get("location", "")), seniority(j["position"]),
                           (j.get("date", "") or "")[:10], j.get("url", "")))
    if not out: raise Blocked("no design rows")
    return out

def t0_remotive(_) -> list[Job]:
    d = httpx.get("https://remotive.com/api/remote-jobs?category=design&limit=100", headers=UA, timeout=30).json()
    out = [Job("Remotive", j["title"], j.get("company_name", ""), j.get("candidate_required_location", "Remote"),
               region_of(j.get("candidate_required_location", "")), seniority(j["title"]),
               (j.get("publication_date", "") or "")[:10], j.get("url", ""))
           for j in d.get("jobs", []) if is_design(j.get("title", ""))]
    if not out: raise Blocked("empty")
    return out

def t0_jobicy(_) -> list[Job]:
    d = httpx.get("https://jobicy.com/api/v2/remote-jobs?count=50&tag=design", headers=UA, timeout=30).json()
    out = [Job("Jobicy", html.unescape(j["jobTitle"]), j.get("companyName", ""), j.get("jobGeo", "Remote"),
               region_of(j.get("jobGeo", "")), seniority(j["jobTitle"]), (j.get("pubDate", "") or "")[:10], j.get("url", ""))
           for j in d.get("jobs", []) if is_design(j.get("jobTitle", ""))]
    if not out: raise Blocked("empty")
    return out

def t0_arbeitnow(_) -> list[Job]:
    d = httpx.get("https://www.arbeitnow.com/api/job-board-api", headers=UA, timeout=30).json()
    out = []
    for j in d.get("data", []):
        if is_design(j.get("title", "")):
            date = dt.datetime.utcfromtimestamp(j["created_at"]).strftime("%Y-%m-%d") if j.get("created_at") else ""
            out.append(Job("Arbeitnow", j["title"], j.get("company_name", ""), j.get("location", "Remote"),
                           region_of(j.get("location", "")), seniority(j["title"]), date, j.get("url", "")))
    if not out: raise Blocked("empty")
    return out

def t0_workingnomads(_) -> list[Job]:
    d = httpx.get("https://www.workingnomads.com/api/exposed_jobs/", headers=UA, timeout=30).json()
    out = [Job("WorkingNomads", j["title"], j.get("company_name", ""), j.get("location", "Remote"),
               region_of(j.get("location", "")), seniority(j["title"]), (j.get("pub_date", "") or "")[:10], j.get("url", ""))
           for j in d if is_design(j.get("title", ""))]
    if not out: raise Blocked("empty")
    return out

def t1_linkedin_guest(_) -> list[Job]:
    """Tier 1: LinkedIn guest HTML cards (no login). India + remote."""
    out, base = [], "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    for kw in ("product designer", "junior product designer", "UI UX designer"):
        for start in (0, 10):
            r = httpx.get(base, params={"keywords": kw, "location": "India", "f_WT": 2,
                          "sortBy": "DD", "start": start}, headers=UA, timeout=30)
            if r.status_code in (403, 429, 999):
                raise Blocked(f"linkedin {r.status_code}")
            for card in re.findall(r"<li>(.*?)</li>", r.text, re.S):
                title = re.search(r"<h3[^>]*>(.*?)</h3>", card, re.S)
                comp  = re.search(r'hidden-nested-link[^>]*>(.*?)</a>', card, re.S)
                loc   = re.search(r'job-search-card__location[^>]*>(.*?)</span>', card, re.S)
                date  = re.search(r'datetime="([^"]+)"', card)
                link  = re.search(r'href="([^"?]+)', card)
                if title and link:
                    t = re.sub("<.*?>", "", title.group(1)).strip()
                    if is_design(t):
                        out.append(Job("LinkedIn", t, re.sub("<.*?>", "", comp.group(1)).strip() if comp else "",
                                       re.sub("<.*?>", "", loc.group(1)).strip() if loc else "India",
                                       "India", seniority(t), date.group(1) if date else "", link.group(1)))
    if not out: raise Blocked("empty")
    return out

# ---------------------------------------------------------------- higher-tier engine STUBS
# Fill these in with the real libraries. Each must return list[Job] or raise Blocked.
def make_scrapling_stealthy(url: str, parse: Callable[[str], list[Job]]):
    def engine(_):
        from scrapling.fetchers import StealthyFetcher           # Tier 3
        page = StealthyFetcher.fetch(url, headless=True, solve_cloudflare=True)
        if page.status in (403, 429) or not page.html_content:
            raise Blocked("scrapling stealthy blocked")
        jobs = parse(page.html_content)
        if not jobs: raise Blocked("scrapling empty")
        return jobs
    return engine

def make_patchright(url: str, parse: Callable[[str], list[Job]]):
    def engine(_):
        from patchright.sync_api import sync_playwright            # Tier 3
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True); pg = b.new_page()
            pg.goto(url, wait_until="networkidle", timeout=45000)
            content = pg.content(); b.close()
        jobs = parse(content)
        if not jobs: raise Blocked("patchright empty")
        return jobs
    return engine

def make_agentql(url: str, query: str):
    def engine(_):
        import agentql                                            # Tier 4
        with agentql.wrap(__import__("playwright.sync_api", fromlist=["sync_playwright"])):
            pass  # see AgentQL docs: session.query_data(query) -> dict -> map to Job
        raise Blocked("agentql stub - implement mapping")
    return engine

# def make_browser_use(goal): ...   # Tier 4 autonomous agent
# def make_stagehand(url, instruction): ...  # Tier 4 act()/extract()
# def make_camoufox(url, parse): ...  # Tier 3 anti-detect Firefox

# ---------------------------------------------------------------- portal registry (ordered engine chains)
PORTALS: dict[str, list[Callable]] = {
    "RemoteOK":       [t0_remoteok],
    "Remotive":       [t0_remotive],
    "Jobicy":         [t0_jobicy],
    "Arbeitnow":      [t0_arbeitnow],
    "WorkingNomads":  [t0_workingnomads],
    "LinkedIn":       [t1_linkedin_guest],
    # Example of a full fallback chain for a protected portal:
    # "Wellfound": [t0_try_api, make_scrapling_stealthy(URL, parse), make_patchright(URL, parse),
    #               make_camoufox(URL, parse), make_agentql(URL, QUERY)],
}

CACHE_FILE = "portal_cache.json"
def load_cache(): 
    try: return json.load(open(CACHE_FILE))
    except Exception: return {}
def save_cache(c): json.dump(c, open(CACHE_FILE, "w"), indent=1)

# ---------------------------------------------------------------- the orchestrator
def scrape() -> list[Job]:
    cache, all_jobs, seen = load_cache(), [], set()
    for portal, engines in PORTALS.items():
        # start at the engine that worked last time, if known
        start = cache.get(portal, {}).get("winning_index", 0)
        order = list(range(start, len(engines))) + list(range(0, start))
        for idx in order:
            engine = engines[idx]
            try:
                jobs = engine(portal)
                cache[portal] = {"winning_index": idx, "last_success": dt.datetime.utcnow().isoformat(),
                                 "engine": engine.__name__}
                for j in jobs:
                    if j.url and j.url not in seen:
                        seen.add(j.url); all_jobs.append(j)
                print(f"✅ {portal:14s} via {engine.__name__:22s} → {len(jobs)} jobs")
                break
            except Blocked as e:
                print(f"↻ {portal:14s} {engine.__name__} blocked ({e}); escalating…")
            except Exception as e:
                print(f"↻ {portal:14s} {engine.__name__} error ({type(e).__name__}: {e}); escalating…")
            time.sleep(1)
        else:
            cache[portal] = {**cache.get(portal, {}), "needs_manual_review": True}
            print(f"❌ {portal:14s} all engines exhausted — manual review")
    save_cache(cache)
    # sort India → Worldwide → other, newest first
    rank = {"India": 0, "Worldwide": 1, "Region-locked": 2}
    all_jobs.sort(key=lambda j: (rank.get(j.region, 3), j.date), reverse=False)
    return all_jobs

# ---------------------------------------------------------------- standalone email digest (replaces Aside routine)
# Set these as environment variables (or GitHub Actions secrets):
#   SMTP_HOST (default smtp.gmail.com), SMTP_PORT (default 587),
#   SMTP_USER, SMTP_PASS (Gmail App Password), DIGEST_TO
import os, smtplib
from email.mime.text import MIMEText

def email_digest(new_jobs: list[Job]) -> None:
    to = os.environ.get("DIGEST_TO")
    user = os.environ.get("SMTP_USER")
    pw = os.environ.get("SMTP_PASS")
    if not (to and user and pw):
        print("(email skipped - set SMTP_USER, SMTP_PASS, DIGEST_TO to enable)")
        return
    if not new_jobs:
        print("(no new jobs - no email sent)")
        return
    rank = {"India": 0, "Worldwide": 1, "Region-locked": 2}
    new_jobs = sorted(new_jobs, key=lambda j: (rank.get(j.region, 3), j.date), reverse=False)
    rows = "".join(
        f'<tr><td>{j.title}</td><td>{j.company}</td><td>{j.region}</td>'
        f'<td>{j.location}</td><td>{j.level}</td><td>{j.date}</td>'
        f'<td><a href="{j.url}">Apply</a></td></tr>' for j in new_jobs)
    body = (f"<h2>{len(new_jobs)} new remote product designer roles</h2>"
            f"<table border=1 cellpadding=6 cellspacing=0>"
            f"<tr><th>Title</th><th>Company</th><th>Region</th><th>Location</th>"
            f"<th>Level</th><th>Date</th><th></th></tr>{rows}</table>")
    msg = MIMEText(body, "html")
    msg["Subject"] = f"{len(new_jobs)} new remote product designer roles ({dt.date.today()})"
    msg["From"], msg["To"] = user, to
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", 587))
    with smtplib.SMTP(host, port) as s:
        s.starttls(); s.login(user, pw); s.send_message(msg)
    print(f"✉ emailed {len(new_jobs)} new roles to {to}")

def build_dashboard(jobs: list[Job], path: str = "job-dashboard.html") -> None:
    """Regenerate the standalone HTML dashboard from the latest jobs."""
    data = json.dumps([asdict(j) for j in jobs])
    htmldoc = ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Remote Product Designer Jobs</title><style>"
        "body{font:15px system-ui;background:#0f1115;color:#e7eaf0;margin:0}"
        "header{padding:20px;border-bottom:1px solid #262b36}"
        "input,select{background:#181b22;border:1px solid #262b36;color:#e7eaf0;border-radius:8px;padding:8px}"
        ".wrap{padding:18px;max-width:1100px;margin:0 auto}"
        ".card{background:#181b22;border:1px solid #262b36;border-radius:12px;padding:16px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}"
        ".m{color:#9aa3b2;font-size:13px}.apply{background:#2ecc71;color:#06281a;font-weight:700;text-decoration:none;padding:10px 16px;border-radius:9px}"
        "</style></head><body><header><h2>Remote Product Designer Jobs</h2>"
        "<input id=q placeholder='Search...'> <select id=region><option value=''>All regions</option>"
        "<option>India</option><option>Worldwide</option><option>Region-locked</option></select></header>"
        "<div class=wrap><div id=grid></div></div><script>const J=" + data + ";"
        "function r(){const q=document.getElementById('q').value.toLowerCase(),rg=document.getElementById('region').value;"
        "document.getElementById('grid').innerHTML=J.filter(j=>(!q||(j.title+j.company).toLowerCase().includes(q))&&(!rg||j.region===rg))"
        ".map(j=>`<div class=card><div><b>${j.title}</b><div class=m>${j.company} - ${j.location} - ${j.date} - ${j.source}</div></div>`+"
        "`<a class=apply href='${j.url}' target=_blank>Apply</a></div>`).join('')}"
        "['q','region'].forEach(i=>document.getElementById(i).addEventListener('input',r));r();</script></body></html>")
    open(path, "w").write(htmldoc)
    print(f"dashboard -> {path}")

if __name__ == "__main__":
    # load previously seen URLs to compute what's NEW since last run
    try:
        prev = {j["url"] for j in json.load(open("jobs.json"))}
    except Exception:
        prev = set()
    jobs = scrape()
    new_jobs = [j for j in jobs if j.url not in prev]
    json.dump([asdict(j) for j in jobs], open("jobs.json", "w"), indent=1)
    build_dashboard(jobs)
    email_digest(new_jobs)
    print(f"\nTotal: {len(jobs)} jobs ({len(new_jobs)} new) -> jobs.json")

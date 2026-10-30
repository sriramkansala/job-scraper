#!/usr/bin/env python3
"""Who do I know at a company? Reads your LinkedIn connections export.

This is prompt 4 from @coachkunaalnaik's list, as a reusable script.

Get the export: LinkedIn > Settings > Data privacy > Get a copy of your data >
"Connections". LinkedIn emails a zip; put its Connections.csv next to this file.
Connections.csv is git-ignored, so it never reaches this public repo.

    python3 warm_paths.py "CloudSEK"                # one company
    python3 warm_paths.py --all                     # every company in the 30 Oct lists
    python3 warm_paths.py --all --out warm-paths-all.md

The export only lists your 1st-degree connections and their *current* company.
2nd-degree paths (who your connections know) aren't in it, so for each company
the script also prints a LinkedIn search link for 2nd-degree people there.
Open that in Chrome, or ask Claude to read it.
"""
from __future__ import annotations
import argparse, csv, io, json, re, sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).parent
LISTS = HERE.parent / "targets" / "2026-10-30-lists.json"
DESIGN = re.compile(r"design|ux|ui\b|product|research", re.I)
LEAD = re.compile(r"head|director|lead|manager|vp|principal|staff|founder|chief|cto|ceo", re.I)
RECRUIT = re.compile(r"recruit|talent|hiring|people partner|\bhr\b", re.I)

def norm(s: str) -> str:
    s = re.sub(r"\(.*?\)", "", s.lower())
    s = re.sub(r"\b(pvt|private|ltd|limited|inc|technologies|technology|labs|india|software|solutions|ai|group)\b", "", s)
    return re.sub(r"[^a-z0-9]", "", s)

def load_connections(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig")
    # LinkedIn puts a few "Notes:" lines above the header row.
    start = text.find("First Name")
    if start < 0: sys.exit(f"{path} doesn't look like a LinkedIn Connections.csv")
    return list(csv.DictReader(io.StringIO(text[start:])))

def matches(conns: list[dict], company: str) -> list[dict]:
    key = norm(company)
    if len(key) < 3: return []
    return [c for c in conns if (k := norm(c.get("Company", ""))) and (k == key or (len(k) > 3 and (k in key or key in k)))]

def role_of(c: dict) -> str:
    p = c.get("Position", "")
    if RECRUIT.search(p): return "recruiter"
    if DESIGN.search(p) and LEAD.search(p): return "design lead"
    if DESIGN.search(p): return "designer / product"
    if LEAD.search(p): return "leader"
    return "peer"

TEMPLATES = {
    "design lead": "Hi {first}, I saw {company} is hiring a {role}. I rebuilt our token system at Turinglabs (157 → 63 semantic tokens, theming from days to under an hour) and I've applied. Would you be open to a 10-minute chat about what the team needs?",
    "designer / product": "Hi {first}, I'm applying for the {role} role at {company}. As someone on the team, what does the design work look like day to day? And if it seems like a fit, would you be comfortable referring me?",
    "recruiter": "Hi {first}, I've applied for the {role} role at {company} (design systems, fintech and AI-assisted prototyping). Happy to share anything that helps you screen. Is the role still open?",
    "leader": "Hi {first}, I'm applying for the {role} role at {company}. Could you point me to the person who owns design hiring, or pass my name along?",
    "peer": "Hi {first}, I'm applying for the {role} role at {company}. Do you know who leads design there, and would you be open to referring me?",
}

def report(company: str, role: str, conns: list[dict]) -> str:
    found = matches(conns, company)
    plain = re.sub(r"\s*\(.*?\)", "", company).strip()
    search2 = f"https://www.linkedin.com/search/results/people/?keywords={quote(plain)}&network=%5B%22S%22%5D"
    lines = [f"## {company}" + (f" — {role}" if role else ""), ""]
    if not found:
        lines += ["No 1st-degree connections work here (by current company).", ""]
    else:
        lines += ["| Name | Position | Connected | Type | Profile |", "|---|---|---|---|---|"]
        for c in sorted(found, key=lambda c: ["design lead", "designer / product", "recruiter", "leader", "peer"].index(role_of(c))):
            lines.append(f"| {c['First Name']} {c['Last Name']} | {c.get('Position','')} | {c.get('Connected On','')} | {role_of(c)} | {c.get('URL','')} |")
        best = found[0]
        t = TEMPLATES[role_of(best)].format(first=best["First Name"], company=company, role=role or "design")
        lines += ["", f"Draft for {best['First Name']} (edit before sending; nothing is sent for you):", "", f"> {t}", ""]
    lines += [f"2nd-degree people at {company}: {search2}", ""]
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("company", nargs="?")
    ap.add_argument("--all", action="store_true", help="run for every company in the 30 Oct lists")
    ap.add_argument("--connections", default=str(HERE / "Connections.csv"))
    ap.add_argument("--out")
    a = ap.parse_args()
    path = Path(a.connections)
    if not path.exists(): sys.exit(f"Put your LinkedIn Connections.csv at {path} first (see the top of this file).")
    conns = load_connections(path)
    if a.all:
        d = json.loads(LISTS.read_text())
        rows = [(x["company"], x["role"]) for x in d["list2"]] + [(x["company"], x["role"]) for x in d["list1"]]
        seen, parts = set(), []
        hits = 0
        for co, ro in rows:
            if norm(co) in seen: continue
            seen.add(norm(co))
            if matches(conns, co): hits += 1
            parts.append(report(co, ro, conns))
        out = f"# Warm paths across {len(seen)} target companies\n\n{hits} companies have at least one 1st-degree connection.\n\n" + "\n".join(parts)
    elif a.company:
        out = report(a.company, "", conns)
    else:
        ap.error("give a company name or --all")
    if a.out: Path(a.out).write_text(out); print(f"wrote {a.out}")
    else: print(out)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Check a resume PDF the way an applicant tracking system (ATS) would read it.

Usage:
    python3 tools/check_resume_pdf.py resume.pdf [--jd jd.txt] [--dump]

Checks:
    text      extract the text layer (pypdf, plus pdfplumber when installed)
    garbled   broken words such as "M otion" or "201 9", glyph junk, and a
              garbled-text percentage
    contact   email, phone, LinkedIn and portfolio URLs present as plain text
    sections  Experience, Education, Skills and Projects headings detected
    dates     dates read as "Mon YYYY" (or a bare year) and ranges are ordered
    jd        with --jd: keywords from the job description found and missing,
              and a match percentage

Needs pypdf (pip install pypdf). pdfplumber is optional. No network use.
Exit code: 0 = PASS, 1 = WARN, 2 = FAIL, 3 = could not read the PDF.
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

try:
    import pypdf
except ImportError:  # pragma: no cover - environment dependent
    pypdf = None

try:
    import pdfplumber
except ImportError:  # pragma: no cover - environment dependent
    pdfplumber = None

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
RANK = {PASS: 0, WARN: 1, FAIL: 2}

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
MONTH_FULL = {
    "january": 1, "february": 2, "march": 3, "april": 4, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
    "december": 12,
}
PRESENT_WORDS = r"(?:present|current|now|today|ongoing)"


# --------------------------------------------------------------------------- #
# (a) Text extraction
# --------------------------------------------------------------------------- #
def extract_pypdf(path: Path) -> tuple[str, int, list[str]]:
    """Return (text, page count, link URIs) using pypdf's default extraction."""
    reader = pypdf.PdfReader(str(path))
    pages, uris = [], []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
        for annot in page.get("/Annots") or []:
            try:
                obj = annot.get_object()
                action = obj.get("/A")
                if action is not None:
                    uri = action.get_object().get("/URI")
                    if uri:
                        uris.append(str(uri))
            except Exception:
                continue
    return "\n".join(pages), len(reader.pages), uris


def extract_pdfplumber(path: Path) -> str | None:
    if pdfplumber is None:
        return None
    try:
        with pdfplumber.open(str(path)) as pdf:
            return "\n".join((p.extract_text() or "") for p in pdf.pages)
    except Exception:
        return None


# --------------------------------------------------------------------------- #
# (b) Broken words and garbled text
# --------------------------------------------------------------------------- #

BROKEN_PATTERNS = [
    # "D e s i g n": three or more letters separated by single spaces.
    ("letter-spaced", re.compile(r"\b(?:[A-Za-z] ){3,}[A-Za-z]\b")),
    # "M otion", "R edesigned": a lone capital followed by a lowercase fragment.
    ("split capital", re.compile(r"(?<![\w.&/])([B-HJ-Z]) ([a-z]{2,})\b")),
    # "L TIMindtree": a lone capital followed by an uppercase/camel token.
    ("split capital", re.compile(r"(?<![\w.&/])([B-HJ-Z]) ([A-Z]{2,}[a-z]*)\b")),
    # "Motio n", "desig ned": a fragment followed by a lone letter.
    ("split tail", re.compile(r"\b([A-Za-z]{2,}) ([b-hj-zB-HJ-Z])(?![\w.&/+#])")),
    # "m otion": a lone lowercase letter (not "a") followed by a fragment.
    ("split lowercase", re.compile(r"(?<![\w.&/'’-])([b-z]) ([a-z]{2,})\b")),
]
# "201 9", "20 19", "2 019": a year broken by a space.
SPLIT_YEAR = re.compile(r"(?<![\d.,])(\d{1,3}) (\d{1,3})(?![\d.,])")
# Glyphs a PDF writes when it has no usable Unicode mapping.
JUNK = re.compile(r"\(cid:\d+\)|[�-]")
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’.+#/&-]*")

# A lone "x" after a word is usually a multiplier ("faster by 3 x"), not a split word.
OK_TAIL_LETTERS = set("x")


def find_broken_words(text: str) -> list[tuple[str, str]]:
    hits: list[tuple[str, str]] = []
    seen_spans: set[tuple[int, int]] = set()
    for kind, pattern in BROKEN_PATTERNS:
        for m in pattern.finditer(text):
            if kind == "split tail" and m.group(2).lower() in OK_TAIL_LETTERS:
                continue
            span = m.span()
            if any(s < span[1] and span[0] < e for s, e in seen_spans):
                continue
            seen_spans.add(span)
            hits.append((kind, m.group(0)))
    for m in SPLIT_YEAR.finditer(text):
        joined = m.group(1) + m.group(2)
        if len(joined) == 4 and 1950 <= int(joined) <= 2099:
            hits.append(("split number", m.group(0)))
    for m in JUNK.finditer(text):
        hits.append(("glyph junk", repr(m.group(0))))
    # Words run together with no spaces, e.g. "ProductDesignerFigmaFramer".
    for m in re.finditer(r"[A-Za-z]{26,}", text):
        hits.append(("run-together", m.group(0)))
    return hits


def garbled_percent(text: str, hits: list[tuple[str, str]]) -> float:
    words = WORD.findall(text)
    if not words:
        return 100.0
    bad = 0
    for kind, frag in hits:
        if kind in ("letter-spaced",):
            bad += len(frag.split())
        elif kind == "run-together":
            bad += max(2, len(frag) // 8)
        else:
            bad += 2 if kind != "glyph junk" else 1
    return min(100.0, 100.0 * bad / len(words))


# --------------------------------------------------------------------------- #
# (c) Contact details
# --------------------------------------------------------------------------- #
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"(?<![\w/])(\+?\d[\d ()./-]{7,}\d)(?![\w/])")
LINKEDIN = re.compile(r"(?:https?://)?(?:[\w-]+\.)?linkedin\.com/in/[\w%-]+/?", re.I)
URL = re.compile(
    r"(?:https?://)?(?:www\.)?(?:[a-z0-9-]+\.)+"
    r"(?:com|ai|io|me|dev|design|co|in|net|org|app|site|xyz|page|studio|so|cc|tech|link|work)"
    r"(?:/[\w./%#?=&-]*)?",
    re.I,
)


def find_contacts(text: str, link_uris: list[str]) -> dict:
    emails = EMAIL.findall(text)
    phones = [p for p in PHONE.findall(text) if 10 <= len(re.sub(r"\D", "", p)) <= 15]
    # Ignore runs of years (e.g. "2014 2018 2019") that happen to have 10+ digits.
    phones = [p for p in phones
              if p.strip().startswith("+") or not re.fullmatch(r"(?:(?:19|20)\d\d[\s./-]*)+", p.strip())]
    linkedin = LINKEDIN.findall(text)
    email_domains = {e.split("@", 1)[1].lower() for e in emails}
    others = []
    for m in URL.finditer(text):
        u = m.group(0).rstrip(".,)/")
        low = u.lower()
        if "linkedin.com" in low or low in email_domains or "@" in text[max(0, m.start() - 1):m.start()]:
            continue
        # Skip things like "v1.1.3" or file sizes that slipped through.
        if not re.search(r"[a-z]", low.split(".")[0]):
            continue
        others.append(u)
    # Links that exist only as clickable annotations, not as visible text.
    hidden = []
    flat = re.sub(r"\s+", "", text).lower()
    for uri in link_uris:
        if uri.lower().startswith("mailto:"):
            target = uri[7:]
        elif uri.lower().startswith("tel:"):
            target = re.sub(r"\D", "", uri)
            if target and target[-10:] not in re.sub(r"\D", "", text):
                hidden.append(uri)
            continue
        else:
            target = re.sub(r"^https?://(www\.)?", "", uri, flags=re.I).rstrip("/")
        if target and target.lower() not in flat:
            hidden.append(uri)
    return {
        "email": sorted(set(emails)),
        "phone": sorted(set(p.strip() for p in phones)),
        "linkedin": sorted(set(linkedin)),
        "portfolio": sorted(set(others)),
        "link_only": sorted(set(hidden)),
    }


# --------------------------------------------------------------------------- #
# (d) Section headings
# --------------------------------------------------------------------------- #
SECTIONS = {
    "Experience": r"(work |professional |relevant )?experience|employment( history)?|work history|career history",
    "Education": r"education|academic background|qualifications",
    "Skills": r"(technical |core |key )?skills( (&|and) tools)?|competencies|tools( (&|and) skills)?|expertise",
    "Projects": r"(selected |side |personal |key )?projects",
}


def find_sections(text: str) -> dict[str, str | None]:
    lines = [ln.strip() for ln in text.splitlines()]
    found: dict[str, str | None] = {}
    for name, pattern in SECTIONS.items():
        rx = re.compile(r"^(?:" + pattern + r")\s*:?$", re.I)
        found[name] = next((ln for ln in lines if len(ln) <= 40 and rx.match(ln)), None)
    return found


# --------------------------------------------------------------------------- #
# (e) Dates
# --------------------------------------------------------------------------- #
MON_TOKEN = (
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|"
    r"Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
)
MONTH_YEAR = re.compile(r"\b(" + MON_TOKEN + r")(\.?),?\s+(\d{4})\b", re.I)
NUMERIC_DATE = re.compile(r"\b(0?[1-9]|1[0-2])\s*[/.-]\s*((?:19|20)\d\d)\b")
SEP = r"\s*(?:–|—|-|to)\s*"
RANGE = re.compile(
    r"\b(" + MON_TOKEN + r")\.?\s+(\d{4})" + SEP + r"(?:(" + MON_TOKEN + r")\.?\s+(\d{4})|(" + PRESENT_WORDS + r"))\b",
    re.I,
)
YEAR_RANGE = re.compile(r"(?<![\w/])((?:19|20)\d\d)" + SEP + r"((?:19|20)\d\d|" + PRESENT_WORDS + r")\b", re.I)


def month_number(token: str) -> int | None:
    t = token.lower().rstrip(".")
    return MONTHS.get(t[:3]) if (t[:3] in MONTHS) else MONTH_FULL.get(t)


def check_dates(text: str) -> dict:
    strict, nonstandard = [], []
    for m in MONTH_YEAR.finditer(text):
        mon, dot, year = m.group(1), m.group(2), m.group(3)
        canonical = mon[:1].upper() + mon[1:].lower()
        ok = (len(mon) == 3 and canonical[:3].lower() in MONTHS and not dot) or mon.lower() in MONTH_FULL or mon.lower() == "may"
        (strict if ok else nonstandard).append(m.group(0))
    numeric = [m.group(0) for m in NUMERIC_DATE.finditer(text)]
    reversed_ranges = []
    for m in RANGE.finditer(text):
        if m.group(5):
            continue
        a = (int(m.group(2)), month_number(m.group(1)) or 0)
        b = (int(m.group(4)), month_number(m.group(3)) or 0)
        if b < a:
            reversed_ranges.append(m.group(0))
    year_ranges = []
    for m in YEAR_RANGE.finditer(text):
        # Skip year ranges that are part of a Mon YYYY range already counted.
        before = text[max(0, m.start() - 5):m.start()]
        if re.search(MON_TOKEN + r"\.?\s*$", before, re.I):
            continue
        year_ranges.append(m.group(0))
        end = m.group(2)
        if end.isdigit() and int(end) < int(m.group(1)):
            reversed_ranges.append(m.group(0))
    return {
        "mon_yyyy": strict,
        "nonstandard": nonstandard,
        "numeric": numeric,
        "year_only_ranges": year_ranges,
        "reversed": reversed_ranges,
    }


# --------------------------------------------------------------------------- #
# (f) Job-description keyword coverage
# --------------------------------------------------------------------------- #
# Skills, tools and practices that recur in product-design postings. Only the
# ones that actually appear in the JD are used.
VOCAB = [
    "figma", "auto layout", "components", "variants", "prototyping", "prototype", "live prototypes",
    "wireframes", "user flows", "flows", "high-fidelity", "mockups", "handoff", "design system",
    "component library", "design tokens", "tokens", "theming", "accessibility", "wcag", "inclusive design",
    "usability", "usability testing", "user research", "research", "interviews", "a/b testing",
    "interaction design", "visual design", "visual hierarchy", "layout", "typography",
    "information architecture", "ux principles", "user-centered", "ux", "ui", "motion design",
    "micro-interactions", "transitions", "animation", "b2b", "saas", "enterprise", "dashboards",
    "data visualization", "risk visualization", "data-rich", "analytics", "usage data", "html", "css",
    "react", "javascript", "front-end", "claude code", "cursor", "v0", "vibe-coding", "ai",
    "ai-powered", "security", "cybersecurity", "fintech", "mobile", "ios", "android", "responsive",
    "end-to-end", "discovery", "stakeholders", "product managers", "engineers", "cross-functional",
    "mentoring", "mentor", "design reviews", "communication", "collaboration",
    "portfolio", "systems thinking", "framer", "protopie", "sketch", "adobe", "after effects", "rive",
    "jira", "linear", "agile", "scrum", "product strategy", "business goals", "technical constraints",
]

STOPWORDS = set("""
a about above across after again all also an and any are as at be been being both but by can could
did do does each few for from further had has have having he her here hers him his how i if in into
is it its itself just like make more most must my no nor not of off on once only or other our out over
own same she should so some such than that the their them then there these they this those through to
too under until up very was we were what when where which while who whom why will with would you your
yours we're you'll you’ll we’re etc e.g eg i.e ie per via within without across along among
""".split())
GENERIC = set("""
experience years year role team teams work working job candidate candidates ability strong excellent
good great new real deep high help ensure using use build building create creating including include
including well across based level highly will able responsibilities requirements qualifications
preferred required plus bonus company opportunity opportunities day days time looking join want need
nice like apply applicants equal employer skills skill knowledge understanding familiarity exposure
awareness basic proven track record hands-on comfortable fast-paced evolving priorities shape
quickly meaningful generous perks benefits salary competitive lead leading own owning lot things
""".split())

TITLE_WORDS = set("""
senior junior lead principal staff head manager director designer designers product products
engineer engineering research leadership intern associate vp chief
""".split())

KEEP_SECTIONS = re.compile(
    r"responsibilit|requirement|qualification|what you('|’)ll do|what you will do|you will|you('|’)ll|"
    r"about the role|role summary|the role|good to have|nice to have|preferred|must have|skills|"
    r"who you are|what we('|’)re looking for|what we look for|key responsibilities",
    re.I,
)
DROP_SECTIONS = re.compile(
    r"benefit|perks|what you('|’)ll get|what we offer|who are we|about us|about the company|"
    r"equal opportunity|milestones|product suite|compensation|why join",
    re.I,
)


def jd_relevant_text(jd: str) -> str:
    """Keep the role, responsibilities and requirements; drop company boilerplate."""
    lines = jd.splitlines()
    out, mode, saw_heading = [], None, False
    for line in lines:
        s = line.strip().strip("#*_ ").strip()
        is_heading = (
            bool(s) and len(s) <= 60 and not line.lstrip().startswith(("-", "*", "•"))
            and not s.endswith((".", ",", ";")) and len(s.split()) <= 8
        )
        if is_heading and DROP_SECTIONS.search(s):
            mode, saw_heading = "drop", True
            continue
        if is_heading and KEEP_SECTIONS.search(s):
            mode, saw_heading = "keep", True
            continue
        if mode == "keep":
            out.append(line)
    return "\n".join(out) if saw_heading and out else jd


def normalise(text: str) -> str:
    text = text.lower().replace("’", "'")
    text = re.sub(r"[-/_]", " ", text)
    text = re.sub(r"[^a-z0-9+#.' ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def stem(word: str) -> str:
    for suffix in ("ations", "ation", "ings", "ing", "ies", "es", "ed", "s"):
        if len(word) > len(suffix) + 3 and word.endswith(suffix):
            base = word[: -len(suffix)]
            # "theming" must not collapse to the stopword "them".
            return word if base in STOPWORDS else base
    return word


def stem_phrase(phrase: str) -> str:
    return " ".join(stem(w) for w in normalise(phrase).split())


def extract_jd_keywords(jd: str, limit: int = 45) -> list[str]:
    body = jd_relevant_text(jd)
    norm_body = " " + stem_phrase(body) + " "
    keywords: list[str] = []
    seen: set[str] = set()

    def add(term: str) -> None:
        key = stem_phrase(term)
        if key and key not in seen:
            seen.add(key)
            keywords.append(term)

    # 1. Known terms that the JD uses. Phrases are matched first so that a
    #    single word already covered by a phrase is not counted twice; the
    #    result is then put back in the order the JD mentions them.
    vocab_hits = []
    remaining = norm_body
    for term in sorted(VOCAB, key=len, reverse=True):
        key = stem_phrase(term)
        if f" {key} " in norm_body and f" {key} " in remaining:
            vocab_hits.append(term)
            if " " in key:
                remaining = remaining.replace(f" {key} ", " | ")
    vocab_hits.sort(key=lambda t: norm_body.find(f" {stem_phrase(t)} "))
    for term in vocab_hits:
        add(term)
    # 2. Capitalised names used mid-sentence (tools and products such as
    #    "Amplitude" or "Claude Code"), excluding job-title words.
    for m in re.finditer(r"\b([A-Z][a-zA-Z0-9]+(?: [A-Z][a-zA-Z0-9]+)?)\b", body):
        word = m.group(1)
        parts = word.lower().split()
        if any(p in STOPWORDS or p in GENERIC or p in TITLE_WORDS for p in parts) or len(word) < 3:
            continue
        prev = body[max(0, m.start() - 3):m.start()]
        if m.start() == 0 or re.search(r"(^|[\n.:!?•*-])\s*$", prev):
            continue  # start of a sentence or bullet, so the capital means nothing
        add(word)
    # 3. Frequent remaining words and bigrams.
    tokens = [w for w in normalise(body).split() if w not in STOPWORDS and w not in GENERIC and len(w) > 2 and not w.isdigit()]
    counts = collections.Counter(stem(w) for w in tokens)
    bigrams = collections.Counter(
        f"{a} {b}" for a, b in zip(tokens, tokens[1:])
    )
    for bg, n in bigrams.most_common():
        if n >= 2 and len(keywords) < limit:
            add(bg)
    for w, n in counts.most_common():
        if n >= 3 and len(keywords) < limit:
            add(w)
    return keywords


def keyword_coverage(resume: str, keywords: list[str]) -> tuple[list[str], list[str]]:
    norm_resume = " " + stem_phrase(resume) + " "
    found, missing = [], []
    for kw in keywords:
        key = stem_phrase(kw)
        (found if f" {key} " in norm_resume else missing).append(kw)
    return found, missing


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #
def short(items: list[str], n: int = 8) -> str:
    items = list(items)
    if not items:
        return "none"
    more = f" (+{len(items) - n} more)" if len(items) > n else ""
    return ", ".join(items[:n]) + more


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Check a resume PDF for ATS readability.")
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--jd", type=Path, help="job description text or markdown file")
    ap.add_argument("--dump", action="store_true", help="print the extracted text")
    args = ap.parse_args(argv)

    if pypdf is None:
        print("FAIL  pypdf is not installed. Run: python3 -m pip install pypdf (pdfplumber optional)")
        return 3
    if not args.pdf.is_file():
        print(f"FAIL  no such file: {args.pdf}")
        return 3

    try:
        text, pages, uris = extract_pypdf(args.pdf)
    except Exception as exc:
        print(f"FAIL  could not read {args.pdf}: {exc}")
        return 3
    plumber_text = extract_pdfplumber(args.pdf)

    results: list[tuple[str, str, str]] = []
    print(f"Resume: {args.pdf}")
    print(f"Pages: {pages}   Extractors: pypdf {pypdf.__version__}"
          + (f", pdfplumber {pdfplumber.__version__}" if plumber_text is not None else ", pdfplumber not installed"))
    if args.dump:
        print("\n----- extracted text (pypdf) -----\n" + text + "\n----- end -----\n")

    # (a) text layer
    words = WORD.findall(text)
    if len(words) < 50:
        results.append(("Text layer", FAIL, f"only {len(words)} words extracted; the PDF may be an image or outlined text"))
    else:
        results.append(("Text layer", PASS, f"{len(words)} words extracted"))
    results.append(("Page count", PASS if pages <= 2 else WARN, f"{pages} page(s)"))

    # (b) garbled text, worst of the two extractors
    hits = find_broken_words(text)
    pct = garbled_percent(text, hits)
    detail = f"{pct:.1f}% garbled (pypdf), {len(hits)} broken fragment(s)"
    if plumber_text is not None:
        p_hits = find_broken_words(plumber_text)
        p_pct = garbled_percent(plumber_text, p_hits)
        detail += f"; {p_pct:.1f}% (pdfplumber), {len(p_hits)} fragment(s)"
        if p_pct > pct:
            hits, pct = p_hits, p_pct
    status = PASS if not hits else (WARN if pct < 3 else FAIL)
    results.append(("Broken words", status, detail))
    if hits:
        print("\nBroken or garbled fragments:")
        for kind, frag in hits[:25]:
            print(f"  [{kind}] {frag!r}")
        if len(hits) > 25:
            print(f"  ... {len(hits) - 25} more")

    # (c) contact details
    c = find_contacts(text, uris)
    missing = [k for k in ("email", "phone", "linkedin") if not c[k]]
    if not c["email"] or not c["phone"]:
        status = FAIL
    elif missing or not c["portfolio"]:
        status = WARN
    else:
        status = PASS
    if c["link_only"] and status == PASS:
        status = WARN
    results.append((
        "Contact as text", status,
        f"email: {short(c['email'], 2)} | phone: {short(c['phone'], 2)} | "
        f"LinkedIn: {short(c['linkedin'], 2)} | portfolio/other URLs: {short(c['portfolio'], 3)}"
        + (f" | link-only (not in text): {short(c['link_only'], 3)}" if c["link_only"] else ""),
    ))

    # (d) sections
    secs = find_sections(text)
    missing_secs = [k for k, v in secs.items() if v is None]
    core_missing = [k for k in ("Experience", "Education", "Skills") if secs[k] is None]
    status = FAIL if core_missing else (WARN if missing_secs else PASS)
    results.append((
        "Section headings", status,
        "found: " + short([f"{k} ('{v}')" for k, v in secs.items() if v], 6)
        + ("; missing: " + ", ".join(missing_secs) if missing_secs else ""),
    ))

    # (e) dates
    d = check_dates(text)
    problems = d["nonstandard"] + d["numeric"] + d["reversed"]
    split_years = [f for k, f in hits if k == "split number"]
    if not d["mon_yyyy"]:
        status = FAIL
    elif problems or split_years:
        status = WARN
    else:
        status = PASS
    detail = f"{len(d['mon_yyyy'])} Mon YYYY date(s)"
    if d["year_only_ranges"]:
        detail += f", {len(d['year_only_ranges'])} year-only range(s) ({short(d['year_only_ranges'], 3)})"
    if d["nonstandard"]:
        detail += f"; non-standard: {short(d['nonstandard'], 4)}"
    if d["numeric"]:
        detail += f"; numeric: {short(d['numeric'], 4)}"
    if d["reversed"]:
        detail += f"; end before start: {short(d['reversed'], 3)}"
    if split_years:
        detail += f"; split years: {short(split_years, 4)}"
    results.append(("Dates", status, detail))

    # (f) JD keyword coverage (reported, but never fails the resume)
    if args.jd:
        try:
            jd_text = args.jd.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            results.append(("JD keywords", WARN, f"could not read {args.jd}: {exc}"))
        else:
            kws = extract_jd_keywords(jd_text)
            found, missing_kw = keyword_coverage(text, kws)
            pct_match = 100.0 * len(found) / len(kws) if kws else 0.0
            results.append(("JD keywords", PASS if pct_match >= 60 else WARN,
                            f"{pct_match:.0f}% match ({len(found)}/{len(kws)})"))
            print(f"\nJD keywords from {args.jd.name} ({len(kws)}):")
            print("  Found:   " + (", ".join(found) or "none"))
            print("  Missing: " + (", ".join(missing_kw) or "none"))
            print("  Add a missing keyword only where it is true; never stuff the resume.")

    # (g) summary
    print("\nSummary")
    width = max(len(r[0]) for r in results)
    for name, status, detail in results:
        print(f"  {status:<4}  {name:<{width}}  {detail}")
    overall = max((r[1] for r in results if r[0] != "JD keywords"), key=lambda s: RANK[s])
    print(f"\nOverall: {overall}")
    return RANK[overall]


if __name__ == "__main__":
    sys.exit(main())

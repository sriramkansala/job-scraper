---
name: tam-from-verified-data
title: TAM from verified data
description: |
  Use this skill when you need a defensible market-size number - annual
  planning, board prep, or territory design. Takes an ICP definition and
  returns TAM, SAM, and SOM built from Lusha's verified database: company
  counts, contact coverage, and signal density per segment, with every number
  traceable to real data instead of analyst-report extrapolation. Requires a
  Lusha connection.
category: Research
tags: [Research, ICP]
---

Build a verified TAM from Lusha's database. Take an ICP,
return company counts, contact coverage, and signal density
by segment. Break into TAM, SAM, and SOM. Make every number
traceable to real data.

## Input

The user will provide via $ARGUMENTS:

- ICP definition: industry, company size range, geography,
  funding stage, company type
- Target buyer: function and seniority
  (e.g. "VP of Sales, Head of RevOps")
- Segments to break down by: [optional] — default is
  industry, size, geography, funding stage
- What you sell: [optional] — used to calculate SOM
  based on signal activity in the market
- Exclusions: [optional] — industries, geographies,
  or company types to exclude from the TAM

If ICP definition is missing, ask once for the minimum:
industry, company size range, and geography.
Never estimate or interpolate — only return what Lusha
can verify.

## Workflow

1. TAM DEFINITION
   Translate the ICP into Lusha search parameters:
   - Industry and sub-verticals
   - Employee count range
   - Geography: country, region, or global
   - Funding stage if specified
   - Company type: public, private, PE-backed, etc.
   - Apply exclusions if provided

2. COMPANY COUNT — TAM
   Run the full TAM query via Lusha:
   - Total companies matching all ICP criteria
   - Break down by each segment dimension:
     * By industry / sub-vertical
     * By company size band
     * By geography
     * By funding stage
   - Flag any segments where Lusha coverage may be
     thinner — e.g. specific geographies or niche
     sub-verticals

3. CONTACT COVERAGE
   For each segment, return verified contact counts:
   - Total VP+ contacts in Lusha's database
   - Breakdown by seniority:
     * C-suite
     * VP
     * Director
     * Manager
   - Coverage ratio: contacts per company
     (high coverage = easier to prospect,
     low coverage = higher prospecting investment)

4. SIGNAL DENSITY
   For each segment, check current signal activity:
   - Funding events in last 90 days
   - Executive moves in last 30 days
   - Hiring surges — 10%+ headcount growth
   - Intent signals above score 60
   - Rank segments by signal density:
     High / Medium / Low

5. SAM CALCULATION
   Narrow TAM to serviceable addressable market:
   - Apply must-have ICP criteria only
   - Remove segments flagged as thin coverage
   - Remove segments with consistently low signal
     density unless user specifies otherwise
   - Return SAM company and contact counts

6. SOM CALCULATION
   Narrow SAM to serviceable obtainable market:
   - Filter to companies with active signals only
     (signal score 60+ in last 90 days)
   - These are the accounts most likely to convert
     in the near term
   - Return SOM company and contact counts
   - Note: SOM will change quarterly as signals
     shift — recommend re-running each quarter

7. SEGMENT PRIORITIZATION
   Rank all segments by combined score:
   - Company count (size of opportunity)
   - Contact coverage ratio (ease of penetration)
   - Signal density (near-term pipeline potential)
   - Return top 3 segments to prioritize first

## Output Format

### TAM summary

| Layer | Companies | VP+ contacts | Notes |
|---|---|---|---|
| TAM — full market | | | All ICP-fit companies |
| SAM — serviceable | | | Must-have criteria applied |
| SOM — obtainable | | | Active signals only |

---

### TAM breakdown by segment

#### By industry

| Industry | Companies | VP+ contacts | Signal density |
|---|---|---|---|

#### By company size

| Size band | Companies | VP+ contacts | Signal density |
|---|---|---|---|

#### By geography

| Geography | Companies | VP+ contacts | Signal density |
|---|---|---|---|

#### By funding stage

| Stage | Companies | VP+ contacts | Signal density |
|---|---|---|---|

---

### Segment prioritization

Ranked by combined score of size, coverage, and signals:

1. [Segment] — [reason: largest signal density /
   strongest coverage / highest company count]
2. [Segment]
3. [Segment]

---

### Data coverage notes

Flag any segments where Lusha's coverage is thinner
than the rest of the TAM — specific geographies,
niche sub-verticals, or company types where the
count may underrepresent the true market size.

---

### Recommended next step

Based on the TAM output, suggest:
- Which segment to build the first territory from
- Which play or skill to run next
  (e.g. Build territory plan, Find lookalike accounts,
  Get 10 best accounts this week)

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/tam-builder-skill/

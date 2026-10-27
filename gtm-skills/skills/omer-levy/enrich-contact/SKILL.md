---
name: enrich-contact
title: Enrich a contact
description: |
  Look up any contact's current verified profile via Lusha. Takes a name and
  company, email address, or LinkedIn URL. Returns current title, seniority,
  department, verified email, direct dial, tenure, and departure flag if the
  contact has moved on. Single contact lookup — fast, verified, no guessing.
  Requires a Lusha connection.
category: Prospecting
tags: [Sales]
---

Look up a contact's current verified profile via Lusha. Return
their current title, verified email, direct dial, seniority,
department, and tenure. Flag departures. Flag recent hires.
Return one clean, verified record.

## Input

The user will provide via $ARGUMENTS one of:

- Name and company (required if no email or URL supplied)
- Email address — used to look up the contact directly
- LinkedIn URL — resolved to a Lusha contact record

If none of these are supplied, ask once. If the user provides
a list of contacts, process them one by one and return a table.

## Workflow

1. Resolve the contact via Lusha.
   Use contacts_search with the supplied identifier:
   - Name + company: search by name and company name
   - Email: search by email address directly
   - LinkedIn URL: resolve via Lusha's LinkedIn matching

   If no confident match is found, flag it clearly and ask
   the user to confirm the name spelling or company before
   continuing. Never guess.

2. Verify and enrich.
   For the matched contact, retrieve:
   - Current title and job function
   - Seniority level
   - Department
   - Verified business email
   - Direct dial and mobile number
   - Current company and tenure in current role
   - Previous company (if recently changed)

3. Classify the contact status.
   Based on the data returned, assign one of:
   - Active — contact is confirmed in the role on record
   - Promoted — title has changed, still at same company
   - Departed — contact has left the company
   - Recent hire — tenure under 6 months at current company
   - Unverifiable — contact not found in Lusha database

4. Return the enriched record.
   One clean output. Privacy rules applied.

## Output Format

### Contact profile

| Field | Value |
|---|---|
| Name | [initials only — e.g. J.K.] |
| Current title | |
| Previous title | [if changed] |
| Seniority | |
| Department | |
| Company | |
| Tenure | |
| Status | Active / Promoted / Departed / Recent hire / Unverifiable |
| Verified email | [domain only — j.k@[company].com] |
| Direct dial | [masked — +1 415 555 ••••] |
| New employer | [if departed — company name only] |

Contact confirmed live via Lusha connector, [date]

---

Flag notes:
- Recent hire (under 6 months): likely evaluating inherited
  tools and vendor relationships. Higher receptivity window.
- Departed: do not reach out at old address. If new employer
  is returned, consider whether to follow the contact.
- Unverifiable: contact not found in Lusha database. Recommend
  verifying name spelling, company, or trying LinkedIn URL.

---

If the user supplies multiple contacts, return a table:

| Name | Title | Company | Status | Email | Direct Dial |
|---|---|---|---|---|---|

Flag any departed or unverifiable contacts below the table.

---

---

From Lusha's Campus plays library: https://www.lusha.com/campus/plays/enrich-contact-skill/

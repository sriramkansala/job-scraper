# LinkedIn profile audit, 30 Oct 2026

This runs prompt 1 from @coachkunaalnaik's list: audit the profile against the roles you're targeting, then rewrite the headline and About for recruiter search. It's based on your live profile, read in Chrome on 30 Oct, and the 30 job descriptions saved from the 30 Oct research run. Nothing on LinkedIn has been changed. You make the edits.

## What recruiters search for, and what your profile says

Number of the 30 target job descriptions that ask for each thing:

| Asked for | JDs | On your profile now |
|---|---|---|
| Design system | 24 | Yes (About) |
| Prototyping | 23 | **No** |
| AI / agents / LLM | 23 | **No** |
| B2B / enterprise / SaaS | 22 | Yes |
| Figma | 20 | Headline only, not in Skills |
| Metrics / impact | 18 | **No numbers anywhere** (the token numbers aren't on LinkedIn) |
| End-to-end ownership | 18 | Yes (About) |
| Fintech / financial | 17 | Yes |
| Code / front-end | 15 | **No** (Notate is missing) |
| User research | 15 | Skills only, as "Research" |
| Accessibility / WCAG | 14 | Yes |
| Motion / interaction | 11 | **No** (and Camberry says "Motion Graphic Artist") |
| Dashboards / data viz | 10 | Yes (About) |

## Gaps, most important first

1. **Notate and AI-assisted building are invisible.** 23 of 30 postings ask about AI, and 15 about code. Notate is your proof of both, and it's on no profile section.
2. **Your experience entries have no descriptions.** Turinglabs, L&T, Mountain Studio and Camberry show only a title and dates. Recruiters search experience text, and your token numbers (157 → 63, 137KB → 37KB, theming from 2–3 days to under an hour) appear nowhere on LinkedIn.
3. **Your skills section works against you.** Your top skills are Graphic Design, Presentation Skills and Leadership, followed by CATIA, Customer Service, Microsoft Office, Online Advertising and Social Media. None of the target roles ask for these. LinkedIn's matching uses this list.
4. **Your title and dates contradict each other.** These are the facts a background check confirms with HR:
   - **Turinglabs:** LinkedIn says Product Designer, while your About and resume say Senior Product Designer.
   - **L&T:** LinkedIn says you left in May 2023, which overlaps Turinglabs (from Feb 2023). Your resume says Dec 2022.
   - **Camberry:** LinkedIn says Sep 2019 – Sep 2020, and your resume says Aug 2019 – Jul 2020.
   - **Fix:** use whatever your offer and relieving letters say, everywhere.
5. **Your headline sends Bengaluru recruiters away.** "Open to Remote (Global)" plus "Private Equity" mislead: you're also open to Bengaluru hybrid, and the DCF work was for retail investors.
6. **Smaller issues:**
   - The old `sriramkansala.webflow.io` link is still on the L&T entry.
   - There's no featured section.
   - You have 0 posts, against 305 followers.

## Headline (LinkedIn allows 220 characters)

Pick the version that matches your official title:

> **If your title is Product Designer:** Product Designer · Design systems & tokens · AI-assisted prototyping (built Notate with Claude Code) · Fintech & data-heavy B2B · WCAG AA · Bengaluru, open to hybrid/remote

> **If your title is Senior Product Designer:** Senior Product Designer · Design systems & tokens · AI-assisted prototyping (built Notate with Claude Code) · Fintech & data-heavy B2B · WCAG AA · Bengaluru, open to hybrid/remote

## About (paste in full)

> I'm a product designer in Bengaluru with 5+ years designing fintech and enterprise B2B products, and a background in motion design. I do my best work where products are dense with data, and where the design system has to hold up in code rather than only in Figma.
>
> At Turinglabs I rebuilt our colour-token architecture from scratch: 157 component tokens became 63 semantic ones. The token payload dropped from 137KB to 37KB, client theming went from 2–3 days to under an hour, and WCAG AA contrast is checked when a token is defined, not audited afterwards. I also redesigned the core DCF flow into guided steps that retail investors can follow, and designed Equity Simulation for stress-testing scenarios before an investment decision.
>
> I prototype and ship with AI tools. Notate, a Chrome extension for capturing and reporting UI issues, is one I designed and built with Claude Code. It's live on the Chrome Web Store with Jira, Linear, GitLab and Trello integrations. On Artos, a personal-finance app with 10k+ downloads, I learned the hard way that a redesign can cost retention, and how to diagnose it.
>
> What I bring: design systems and tokens built for engineering handoff · accessibility built into the system · complex financial and analytics workflows made usable · AI-assisted prototyping in code · motion and interaction craft (Rive, Framer).
>
> Open to senior product design roles in Bengaluru (hybrid or on-site) or remote, in fintech, AI products, dev tools and B2B SaaS.
> Portfolio: sriramkansala.framer.ai

Every fact here comes from `job-scraper/profile/`. If you'd rather not mention the Artos retention drop, delete that sentence.

## Experience descriptions

**Turinglabs** (use your official title):
- Rebuilt the colour-token architecture: 157 component tokens → 63 semantic tokens, payload 137KB → 37KB, client theming from 2–3 days to under an hour.
- Designed a three-tier semantic token model with WCAG AA validated when a token is defined.
- Redesigned the core DCF flow into guided steps for retail investors.
- Designed Equity Simulation, for stress-testing scenarios before an investment decision.

**Larsen & Toubro Infotech, UX Designer:** fix the end date, and remove the webflow link.
- Redesigned enterprise analytics dashboards and internal tools for manufacturing and infrastructure clients.
- Rebuilt data-heavy reporting screens so critical information surfaces faster.
- Standardised UI patterns across modules with shared component specs.

**Camberry:** consider renaming the title to "Motion Designer", as on your resume.
- Explainer videos and UI animation for ed-tech, real-estate and consumer clients; motion style guides and principles.

**Add as Projects:**
- **Notate**, a Chrome extension I designed and built with Claude Code: element and region capture, screen recording, 60-second DOM replay, push to Jira, Linear, GitLab and Trello. Link to its Web Store page.
- **Artos**, a personal-finance Android app (10k+ downloads, ~1,500 DAU). I led the design end to end. I redesigned Market Watch around a 15–30 minute data delay, and I'm diagnosing a retention drop after the redesign.

## Skills (pin these 5 at the top)

Design Systems · Product Design · Prototyping · Interaction Design · Figma

Then add: Design Tokens, Accessibility (WCAG), User Experience (UX), Data Visualization, User Research, Information Architecture, Framer, Rive, Motion Design, AI-assisted Prototyping.

Remove: CATIA, Customer Service, Microsoft Office, PowerPoint, Online Advertising, Social Media, Marketing Strategy, Strategic Planning, and Graphic Design, unless you want it.

## Featured section

Pin three things:
- the Tokens case study;
- Notate's Web Store page;
- your portfolio.

Once you start posting (see `post-ideas-90.md`), pin your best post too.

# Job Portals Master List
_74 catalogued sources. Generated 2026-06-27._

Catalogued from a 200+ site sweep, deduped and tagged with how the scraper reaches each one (mapped to its fallback tier).

**Access -> tier:** api/rss = Tier 0 (httpx today) · html = Tier 1-2 · js = Tier 2 (headless browser) · antibot = Tier 3 (Patchright/Camoufox) · login = Tier 4 (AI agent + auth)

**Scrape-readiness:** Tier 0 = 13 · Tier 1-2 = 38 · Tier 2 = 7 · Tier 3 = 1 · Tier 4 = 15

## Core API (wired today) (6)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| RemoteOK | remoteok.com/api | Global | Free | api | 0 | WIRED - JSON API. |
| Jobicy | jobicy.com/api/v2/remote-jobs | Global | Free | api | 0 | WIRED - JSON API, tag=design. |
| Arbeitnow | arbeitnow.com/api/job-board-api | Global | Free | api | 0 | WIRED - JSON API. |
| Himalayas | himalayas.app/jobs/api | Global | Free | api | 0 | WIRED - JSON API, offset paginate. |
| LinkedIn (guest) | linkedin.com/jobs-guest/jobs/api | Global | Free | html | 1-2 | WIRED - guest cards, no login. |
| Jobspresso | jobspresso.co | Global | Free | rss | 0 | job_feed RSS. |

## General Remote Boards (9)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| WeWorkRemotely | weworkremotely.com | Global | Employer ~$299/post | rss | 0 | Has category RSS feeds (already wired). Largest remote board. |
| Remote.co | remote.co | Global | Free seeker; employer sub | rss | 0 | 100k+ jobs; design RSS feed available. |
| FlexJobs | flexjobs.com | Global | Seeker sub $149/yr | login | 4 | Screened jobs; paywalled, needs account. |
| Working Nomads | workingnomads.co | Global | Free; Pro $100/yr | api | 0 | exposed_jobs JSON API (already wired). |
| Virtual Vocations | virtualvocations.com | Global (US) | Sub ~$15/mo | login | 4 | Subscription-gated listings. |
| JustRemote | justremote.co | Global | Employer $189/30d | html | 1-2 | Static-ish HTML listings. |
| SkipTheDrive | skipthedrive.com | Global | Free; employer $99 | rss | 0 | WordPress job board; likely job_feed RSS. |
| Search Remotely | searchremotely.com | Global | Employer pays | html | 1-2 | AI recommendations; HTML. |
| Devex | devex.com/jobs | Global | Freemium | login | 4 | Aid/development sector. |

## Tech & Startups (8)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| Remotive | remotive.com | Global | Free; premium $49/yr | api | 0 | JSON API by category (already wired). |
| Arc | arc.dev | Global (US/EU) | Free seeker | js | 2 | Vetted senior devs/designers; JS app. |
| Wellfound (AngelList) | wellfound.com | Global | Free seeker | antibot | 3 | Startup jobs; heavy anti-bot + login for apply. |
| Tech Ladies | hiretechladies.com | Global | Employer $499+/mo | html | 1-2 | Community board. |
| Dice | dice.com | US (global listings) | Free browse | js | 2 | Established tech board; remote filter. |
| YC Work at a Startup | workatastartup.com | Global (YC) | Free | login | 4 | YC companies; login GraphQL. |
| Startup Jobs | startup.jobs | Global | Employer $279/post | html | 1-2 | Early-stage startups. |
| EdSurge Career Center | jobs.edsurge.com | US/Global | Employer pays | html | 1-2 | Education startups. |

## Design & Creative (5)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| Behance Jobs | behance.net/joblist | Global | Free (Adobe) | js | 2 | Adobe/Behance creative roles; JS app. |
| Dribbble Jobs | dribbble.com/jobs | Global | Employer $350-800/job | html | 1-2 | Creative community; remote search. |
| 99designs | 99designs.com | Global | Contest from $99 | js | 2 | Project/contest marketplace. |
| Crowdspring | crowdspring.com | Global | Per contest | js | 2 | Crowdsourced creative projects. |
| Smashing Magazine Jobs | jobs.smashingmagazine.com | Global | Employer $199/post | html | 1-2 | Designer/dev board. |

## Writing & Content (4)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| ProBlogger Jobs | problogger.com/jobs | Global | Free posting | html | 1-2 | Blogging/editing gigs. |
| FreelanceWriting.com | freelancewriting.com | Global | Free | html | 1-2 | Aggregated writing jobs. |
| AllFreelanceWriting | allfreelancewriting.com | Global | Free | html | 1-2 | Daily writing job list; no login. |
| JournalismJobs | journalismjobs.com | US/Global | Free browse | html | 1-2 | Journalism careers. |

## Marketing & Sales (5)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| MarketerHire | marketerhire.com | Global | Free talent; buyer fee | login | 4 | Vetted freelance marketers; matching. |
| Mayple | mayple.com | Global | Free talent | js | 2 | AI matching marketing freelancers. |
| GrowthHackers Jobs | growthhackers.com/jobs | Global | Employer pays | html | 1-2 | Growth roles board. |
| AMA Career Center | careers.ama.org | US/Global | Employer per post | html | 1-2 | American Marketing Assoc board. |
| Remote Jobs Club | remotejobs.club | Global | Free | html | 1-2 | Curated newsletter-style board. |

## Non-profit & Social Impact (4)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| Idealist | idealist.org | Global | Employer from $75 | html | 1-2 | Largest NGO/mission board. |
| Work for Good | workforgood.org | US/Global | Employer pays | html | 1-2 | Purpose-driven jobs. |
| The Impact Job | theimpactjob.com | Global | Free seeker | html | 1-2 | Handpicked impact jobs. |
| CharityVillage | charityvillage.com | Canada | Employer pays | html | 1-2 | Canadian nonprofit board. |

## Government & Public Sector (4)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| USAJOBS | usajobs.gov | USA | Free (gov) | api | 0 | Official US gov API (data.usajobs.gov); telework filter. |
| GovernmentJobs.com | governmentjobs.com | USA | Employer pays | html | 1-2 | State/local gov portal; telework filter. |
| UK Civil Service Jobs | civilservicejobs.service.gov.uk | UK | Free | html | 1-2 | UK gov roles; some remote. |
| EU Careers (EPSO) | eu-careers.europa.eu | Europe | Free | html | 1-2 | EU institutions; mostly onsite. |

## Education & Research (3)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| HigherEdJobs | higheredjobs.com | US/Global | Free browse | html | 1-2 | Higher-ed; online/remote filter. |
| TeachAway | teachaway.com | Global | Free browse | html | 1-2 | Online/abroad teaching jobs. |
| Academic Keys | academickeys.com | Global | Employer pays | html | 1-2 | University jobs aggregator. |

## Healthcare & Medical (3)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| Remote Nurse Connection | remotenurseconnection.com | USA | Membership | html | 1-2 | RN telehealth board + coaching. |
| The Remote Nurse | remotemedicaljobs.com | US/Global | Free browse | html | 1-2 | Telehealth/remote nursing. |
| Health eCareers | healthecareers.com | US | Free search | html | 1-2 | Medical board; remote filter. |

## Legal & Finance (4)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| Axiom | axiomlaw.com | Global | Company pays | login | 4 | On-demand legal talent; all remote. |
| LawJobs | lawjobs.com | USA | Employer pays | html | 1-2 | ABA legal listings. |
| eFinancialCareers | efinancialcareers.com | Global | Employer pays | js | 2 | Finance/banking; remote filter. |
| AccountingFly | accountingfly.com | USA | Employer pays | html | 1-2 | Accounting/CPA (mostly US). |

## Regional & Aggregators (6)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| EU Remote Jobs | euremotejobs.com | Europe | Employer ~$329 | html | 1-2 | Europe TZ remote; timezone filter. |
| LATAM Jobs | latam.jobs | Latin America | Free seeker | html | 1-2 | LATAM talent to remote jobs. |
| Remote Africa | remoteafrica.io | Africa | Employer ~$199/job | html | 1-2 | African professionals. |
| NoDesk | nodesk.co | Global | Free | html | 1-2 | Curated remote jobs + company rankings. |
| Remote Australia | remoteaustralia.com | Australia | Free seeker | html | 1-2 | Aussie remote roles. |
| EthicalJobs | ethicaljobs.com.au | Australia | Employer pays | html | 1-2 | Values-aligned AU jobs. |

## Freelance & Gig Marketplaces (10)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| Hubstaff Talent | talent.hubstaff.com | Global | Free | html | 1-2 | Free directory; no commissions. |
| Toptal | toptal.com | Global | Company pays | login | 4 | Vetted top 3% talent; gated. |
| Upwork | upwork.com | Global | 5-20% commission | login | 4 | Largest freelance marketplace. |
| Freelancer.com | freelancer.com | Global | Contest/project fees | login | 4 | Crowdsourcing + contests. |
| Fiverr | fiverr.com | Global | 20% fee | login | 4 | Microjobs marketplace. |
| PeoplePerHour | peopleperhour.com | Global | 20% commission | login | 4 | Small projects; escrow. |
| Guru | guru.com | Global | Free basic; tiers | login | 4 | Milestone pay; reviews. |
| Workana | workana.com | LATAM/Europe | Free; service fees | login | 4 | Bilingual; regional focus. |
| Catalant | gocatalant.com | Global | By project | login | 4 | Consultants to enterprise projects. |
| Consultants for Good | consultantsforgood.org | USA | Free directory | html | 1-2 | Skilled-volunteer network. |

## Niche (Crypto, Exec, etc.) (3)

| Site | URL | Scope | Pricing | Access | Tier | Notes |
|---|---|---|---|---|---|---|
| Web3 Career | web3.career | Global | Free browse | api | 0 | Crypto roles; has API/feed; pay-in-crypto filter. |
| CryptocurrencyJobs.co | cryptocurrencyjobs.co | Global | Free browse | rss | 0 | Blockchain jobs; RSS/newsletter. |
| BlueSteps | bluesteps.com | Global | Membership | login | 4 | C-suite/fractional exec network. |


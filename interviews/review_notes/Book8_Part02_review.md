# Book 8 Part 2 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the two research agents). Scope: 2 region profiles (United States, Canada). No pay content; no visa, work-permit, immigration, tax or employment-law claims.

## Process
Two agents researched one region each (15 and 13 WebSearch searches, snippet-only) and wrote profiles, source logs and progress files; merged with `scratch/B8_merge.py 2`; the lead wrote the header and the comparison table from the profiles. No spend-limit stops.

## Checks (`scratch/B8_check.py`)
| Check | Result |
|---|---|
| Profile numbering R1-R2 and all 15 template labels present and in order | pass for both |
| At least 10 evidence tags and 3 source URLs per profile; every `[S#]` used exists in the Sources list; every listed source is cited | pass (US 36 sources, Canada 35 sources) |
| Pay patterns (LPA, lakh, crore, CTC, salary, compensation, base pay, per annum, currency symbols and codes with digits) | 0 hits |
| Visa-digit flags | 1 flag, a false positive (a source tag after "federal announcement rules"), reviewed manually |
| Cross-references to Books 1-7: every "Book N Part M (topic)" scanned against plan.md titles | pass, 0 mismatches; the two Book 9 mentions say planned, not yet written |

## Findings and honest limits
- United States: rated Medium for big-tech loops and CV conventions and Thin for every other segment; each claim is tagged by segment (big tech, finance, healthcare, consulting, research labs, start-ups, government). Finance rests on one Capital One data analyst loop; start-ups on commentary only; government on the USAJOBS portal only.
- Canada: resume conventions are the solid part; interview evidence is single reports, mostly Toronto (RBC, Shopify guides, Meta, Affirm, Instacart, TD, Loblaw, Kinaxis, Exadel, Stripe); Montreal has only Intact and one Unity review plus postings; Vancouver, Waterloo, Ottawa and Calgary are covered only as hubs.
- Work authorisation: the US profile names USCIS, the Department of State and the Department of Labor without URLs (none appeared in the results); the Canada profile names the Government of Canada Work in Canada page and Job Bank. No rules, thresholds, fees or timelines appear.
- Law-adjacent items (Quebec Bill 96 job-ad point, Ontario "Canadian experience" posting change, Ontario AI-disclosure rule) are reported only as coverage and tagged [U].
- The roughly 18 per cent referral-hires figure (Ashby) has no identified source page and its attribution is flagged approximate.
- AI-policy sources for candidates conflict (Meta, Google, Anthropic) and are blogs or secondary reporting; the profile says to check with the recruiter.
- Left out on purpose: EEOC and employment-law summaries (law-firm pages), conflicting layoff counts, a data-engineering AI-in-take-home survey (kept only with a not-ML-evidence caveat), all pay figures.

## Not done
No page was opened (WebFetch fails in this environment). Nothing here replaces the employer's own pages and the official government sources named in each profile.

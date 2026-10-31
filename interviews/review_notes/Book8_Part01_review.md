# Book 8 Part 1 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the three research agents). Scope: 6 region profiles (Sweden, Germany, Netherlands, Ireland, United Kingdom, Switzerland). No pay content; no visa, work-permit, immigration, tax or employment-law claims.

## Process
Three agents researched two regions each (7 to 10 WebSearch searches per region, snippet-only) and wrote profiles, source logs and per-region progress files; merged with `scratch/B8_merge.py 1`; the lead wrote the header and the comparison table from the profiles. No spend-limit stops.

## Checks (`scratch/B8_check.py`)
| Check | Result |
|---|---|
| Profile numbering R1-R6 and all 15 template labels present and in order | pass for all 6 |
| At least 10 evidence tags and 3 source URLs per profile; every `[S#]` used exists in the profile's Sources list; every listed source is cited (R6 intentionally skips S15 as unused: the checker's unused-source rule was satisfied after the numbering was kept as is) | pass |
| Pay patterns (LPA, lakh, crore, CTC, salary, compensation, base pay, per annum, currency symbols and codes with digits) | 0 hits |
| Visa-digit flags (digits near visa, permit, sponsorship, immigration) | 2 flags, both false positives (source tags like [S16] next to "official" and "permit" in the Netherlands and Ireland work-authorisation sections), reviewed manually |
| Cross-references to Books 1-7: every "Book N Part M (topic)" scanned against plan.md titles | pass for Books 1-7; four references to Book 9 Part 1 (STAR/CARL) and "Book 9" were found: Book 9 is planned and not yet written, so the profiles now say "planned, not yet written" |

## Findings and honest limits
- No profile rates High: no country has an official or country-wide description of data and ML interview stages in the results.
- Official sources named in the work-authorisation sections (no rules summarised): Arbetsformedlingen, EURES, Migrationsverket (Sweden); Make it in Germany (Germany); government.nl, IND (Netherlands); gov.ie employment permits, Workplace Relations Commission (Ireland); GOV.UK Skilled Worker pages (UK); SEM, Job-Room (Switzerland).
- Stereotyped claims about national character ("directness", understatement) were discarded; only formal conventions that repeat across sources (formal address, punctuality, competency interviews, CV conventions) were kept, each tagged.
- Photo, references and cover-letter conventions conflict across sources in every country; the profiles record the disagreement instead of picking one.
- Employer-specific candidate reports are small, often old (2016-2023) and many are for software or other roles; the profiles label them anecdotal. Company examples point to Book 7 profiles by company name rather than repeating company claims.
- AI-in-hiring figures (Ireland, UK, Switzerland) come from recruiter or vendor surveys and are labelled weak; no source covers AI use inside technical rounds for most countries ([U]).
- Left out on purpose: all pay figures and ranges, immigration rules, thresholds, fees and processing times, Arbeitszeugnis legal claims, Opportunity Card details.

## Not done
No page was opened (WebFetch fails in this environment). Nothing here replaces the employer's own pages and the official government sources named in each profile.

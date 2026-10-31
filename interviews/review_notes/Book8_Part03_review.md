# Book 8 Part 3 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the three research agents). Scope: 5 profiles (Singapore, Malaysia, Indonesia, United Arab Emirates, India baseline) and the lead-written closing guide "India comparison and relocation preparation guide". No pay content; no visa, work-permit, immigration, tax or employment-law claims.

## Process
Three agents researched the profiles (10 to 11 WebSearch searches per region, snippet-only) and wrote profiles, source logs and progress files; merged with `scratch/B8_merge.py 3`; the lead wrote the header, the comparison table and the closing guide from the 13 profiles of Book 8. No spend-limit stops.

## Checks (`scratch/B8_check.py`)
| Check | Result |
|---|---|
| Profile numbering R1-R5 and all 15 template labels present and in order | pass for all 5 |
| At least 10 evidence tags and 3 source URLs per profile; every `[S#]` used exists in the Sources list; every listed source is cited | pass (India baseline lists 30 sources with S13 skipped, noted in its sources log) |
| Pay patterns (LPA, lakh, crore, CTC, salary, compensation, base pay, per annum, currency symbols and codes with digits), run over the whole part including the closing guide | 0 hits |
| Visa-digit flags | 2 flags, both false positives ("does not permit AI tools ... 2025" in the Singapore profile; a source tag next to "immigration pages" in the Indonesia profile), reviewed manually; the closing guide adds none |
| Cross-references to Books 1-7: every "Book N Part M (topic)" scanned against plan.md titles | pass, 0 mismatches; every Book 9 mention says planned, not yet written |

## Review of the closing guide
- Every row of the theme table was traced to the profile named in its "Where" column (take-home or case: Netherlands, Germany, UK, Sweden fintech anecdote, Singapore, Canada and some US segments, and no reports for Malaysia; CV length and photo conventions by country; cover letters; language lines; psikotes in Indonesia; referrals in the US and the India baseline; notice periods and background checks as baseline steps with other profiles marked [U]).
- The guide states no immigration, visa, tax or employment-law rule and no pay information, tells the reader to verify with the official sources named in each profile, and repeats that comparisons are of processes, not people.
- Where the profiles found nothing (notice periods and offer timing in most markets), the guide says to ask the recruiter instead of assuming.

## Findings and honest limits
- Evidence is Thin everywhere in this part except Singapore (Medium-Thin) and the India baseline (Thin to Medium): the best sources are a few anonymous reviews, aggregator guides and HR-vendor pages, several for engineering or analyst roles or regional rather than country-specific.
- Official pages named without rules: MOM Fair Consideration Framework page, MyCareersFuture, TAFEP (Singapore); PERKESO MYFutureJobs and the Immigration Department Expatriate Services Division, with the address flagged to verify (Malaysia); Ministry of Manpower KarirHub with the domain flagged to verify, and an official translation of the foreign-worker regulation flagged as possibly superseded (Indonesia); u.ae job-search page, MOHRE Virtual Labour Market and the Abu Dhabi government job portal, the last two from dated press (UAE); National Career Service portal, not about authorisation (India baseline).
- No GenAI or applied-scientist interview reports for any of the four overseas markets; no reports for Emirates NBD, Mashreq, FAB, Noon, Traveloka or Bukalapak data roles.
- Left out: pay figures and ranges, immigration rules, a Greenhouse global AI-interview figure and a "162 applications per offer" figure (secondhand or vendor-sourced), a teamblind thread whose body did not appear, Emiratisation effects (not in results).

## Not done
No page was opened (WebFetch fails in this environment). Nothing here replaces the employer's own pages and the official government sources named in each profile.

# Book 8 overall note
All 13 profiles (Parts 1-3) share the same evidence method and checker. No profile is rated High. Medium or better: Netherlands, and the US for big-tech loops and CV conventions; Germany is Medium for CV conventions only. Use the book as a map of what to prepare and what to verify, not as a description of the current process anywhere.

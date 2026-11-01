# Book 7 Part 1 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the five research agents). Scope: 10 company profiles (Google, Microsoft, Amazon, Meta, Apple, Netflix, Uber, LinkedIn, Adobe, Salesforce). No pay figures; no visa or legal claims.

## Process
Five agents researched two companies each (6 to 9 WebSearch searches per company, 6-9 for Salesforce and Adobe, snippet-only) and wrote profiles, source logs and per-company progress files; merged in company order with `scratch/B7_merge.py 1`; the lead wrote the header and the comparison table from the profiles. No spend-limit stops.

## Checks (`scratch/B7_check.py`)
| Check | Result |
|---|---|
| Profile numbering C1-C10 and all 13 template labels present and in order | pass for all 10 |
| At least 8 evidence tags per profile; at least 2 source URLs per profile | pass |
| 5 to 8 sample questions per profile, each tagged `[illustrative]` or `[S#]` | pass |
| Every `[S#]` used in a profile exists in that profile's Sources list; every listed source is used | pass (lead's own scan; 0 missing, 0 unused; now part of the checker) |
| Pay patterns (LPA, lakh, crore, CTC, salary, compensation, base pay, per annum, currency symbols, currency codes with digits) | 0 hits |
| Cross-references to Books 1-6 (40 distinct Book/Part pairs) | all resolve to real parts in plan.md; the topic parentheticals match the plan.md titles |

## Spot checks against the profiles' own sources
- Meta (C4): the "up to six 45-minute conversations" claim is tied to Meta's ML full-loop page snippet [S1]; Data Scientist rounds, timelines and the IC5/IC4 anecdote are tagged to third-party or anecdotal sources; the AI-enabled coding pilot is tagged as limited and partly conflicting; India is stated as no firsthand evidence found.
- Uber (C7): the only official source (careers/interviewing) is quoted for the Talent Acquisition conversation and regional variation only; round detail is tagged to prep guides and candidate reports; the AI-in-coding-rounds claim is tagged [U].
- Adobe (C9) and Salesforce (C10): rated Thin; the profiles state that no official process page was captured and that several source attributions are approximate.

## Findings and honest limits
- Evidence levels: Medium for Google, Microsoft, Amazon, Meta, Apple, Uber and LinkedIn; Thin for Netflix, Adobe and Salesforce. No profile is rated High: official pages surfaced only as short snippets.
- Round counts and durations disagree between sources for almost every company; the profiles keep the ranges and name who said what, and say "duration not found in sources" where there is none.
- India-specific interview evidence is thin or absent for all ten companies; the profiles say so instead of assuming the global process applies ([U] where assumed).
- AI-tool policies for candidates are reported inconsistently (Google, Meta, Amazon, Apple, Microsoft, LinkedIn); every such statement is tagged by source quality and the profiles tell candidates to confirm with the recruiter.
- Some third-party summaries combined several pages; those source entries say a detail cannot be tied to one URL (Google, Microsoft, Amazon, Apple, Adobe, Salesforce).
- Discarded on purpose: any pay or level-band content seen in results, commercial or mirror pages that could not be attributed.

## Not done
No page was opened (WebFetch fails in this environment). Nothing here replaces the company's own careers page or the recruiter's description of the current process.

# Review G1: Book12_Guide.md Sections 1 and 2 (lines 22-286)

Counts: about 45 claims/items checked; 5 edits. No em/en dashes, code fences balanced (6), no ANSWER_PENDING, blank lines after tables OK.

## Number audit
| Claim | Source | Result |
|---|---|---|
| Dashboards 75%, communication 73%, Excel 60%, SQL 54%, Power BI 40%, Python 32%, n=186, +/-7 | MS Addendum table | OK |
| MIS roles Excel 72%, Python 16% | MS Addendum per-sample (MIS col, n=32) | OK, now labelled as the 32-JD sub-sample |
| "Hyderabad, Bengaluru, GCC Python near 40%" | MS Addendum: Hyd 30, Blr 40, GCC 40 | Corrected (Hyderabad is 30%), sub-sample sizes 47/42/25 added |
| Project walk-through in about 14 of 20 profiles | IP Section 4 | OK (candidate-reported) |
| IBM HR sample about 1,470 rows x 35 columns | A12a sources (snippets) | OK, labelled snippet |
| GODL notified 2017 | A12a sources (13 Feb 2017, secondary) | OK |
| ResumeGo 2018, 482 respondents, US, author sells services | A12a sources | OK, labelled; not used as fact |
| One page for career changers / under about 10 years (Monster, CBS, Dice) | A12a sources | OK, snippet |
| Power BI publish-to-web wording revised July 2025 | A12a sources (community posts) | OK, labelled |
| Tableau Public free, data public; GitHub README locations | A12a sources | OK, snippet only |
| Code: 200 employees, seed 42, output Sales 51/4/7.8, Support 51/22/43.1, Tech 58/5/8.6, Finance 40/6/15.0 | Re-run in Python 3.13 | OK, output matches exactly; counts sum to 200 |
| Rs 6-10 LPA target; Today 2026-11-26 | plan/instructions | OK |
| 10 JDs keyword method, 3 follow-ups, 90 seconds, half a minute, time box, 8-10 SQL questions, 5-8 slides, 5 charts, 3 findings | none (our design) | OK, all labelled our rule/suggestion/illustrative; "Skill bars" sentence relabelled as our judgement |
| Bullet-table placeholders [N] | illustrative | OK, no invented numbers |

## Fixes
| Location | Problem | Fix |
|---|---|---|
| 2.1 Order paragraph | Python "near 40%" for Hyderabad wrong (30%); sub-samples quoted under the pooled margin | Rewrote with per-sample figures and sizes, noted they are less certain |
| 1.2 Functional format | Opinion stated as fact in first clause | Labelled both clauses blog opinion, unverified |
| 1.3 Compliance row | Awkward "only if true" inside the bullet | Moved into a bracketed instruction |
| 1.4 Skills bullet | "blogs call them weak" not traceable | Relabelled as our judgement |
| 2.1 Book 0 Q14 pointer | Needed the no-data caveat | Added "no data on how many are enough" (matches Book 0 Q14) |

## Pointers verified
Book 0 Q14, Q19, Q26, Q28, Q83, Q84, Q100 exist and match topic; Book 0 Guide Section 5.3 is the translation table. Book 10 Part 1, Book 4 Parts 3/8/9, Book 5 Part 7 (correlation vs causation), Book 3 Parts 4-9 and 11, Book 8 Part 8, Book 11 Parts 1/2/8, Book 9 Part 9, Books 2 and 7 all exist in plan.md Section 6 and match. No Book 13 pointer. Sections 1-2 contain no "Q<n>" references to Book 12 FAQs.

## Still unverified (labelled in text)
Blog resume advice, ATS layout advice, one-page rule, gap advice, README content list, Tableau/Power BI publish facts (snippets), dataset licences (not read), STAR critique, 90-second structure.

## Could not check
Live pages (GitHub, Tableau, Microsoft Learn, data.gov.in, Kaggle); no web access.

## Overlaps / ordering notes (report only)
Section 2.1 portfolio order (5 projects) vs Book 0 Q14 (2-3 first): consistent, both say so. Section 1.5 certificates and Section 5 overlap by design. Book 0 Q83/Q26 vs 1.3 table: guide points to them rather than repeating.

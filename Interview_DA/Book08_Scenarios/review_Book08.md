# review_Book08.md — Book 8 (Scenario-Based & Data Interpretation) review summary (Wave C, plan.md Section 8.6)

Date: 2026-11-12. One reviewer per part (9 parts) recomputed every figure in every answer that has data or numbers (reconciliations, rates, shares, decompositions, z/chi-square/Fisher/Wilson/DiD results, sample sizes, weighted scores, bridges, headcount and attrition arithmetic, time-zone and lakh/crore conversions) by code, from the question's inline data and the answer's stated assumptions and WITHOUT looking at the written result first; compared, fixed errors in place and wrote `review/review_PartNN.md` (per-fix detail there). Reviewer counts are the reviewers' own and approximate.

## Pass criteria (plan.md 8.6)
| Check | Result |
|---|---|
| Completeness | 640 of 640 answered; 0 `ANSWER_PENDING` (script check) |
| Count | 640 vs target 600 (met) |
| Ordering / numbering | Continuous Q1..Qn in all 9 parts (script check); a reviewer noted Part 4 difficulty order is slightly uneven inside star blocks; left as is |
| Template fields | Asked at, interviewer check, Say this, follow-ups, common mistakes present in all 640 (script check) |
| Markdown / style | Code fences balanced; no em dashes in answers (script check); blank lines added after inline data tables where missing |
| Accuracy | Every figure recomputed by code; real errors found and fixed (below) |

## Per part
| Part | Answers | Answers edited | Main fix types |
|---|---|---|---|
| 1 | 72 | 8 | Q28 simple average 10% not 6.7%, Q50 Excel ID display vs truncation claim, script wording, illustrative labels |
| 2 | 79 | 14 (6 wrong figures) | Q9 headcount 1,090 not 1,180, Q11 cumulative vs weekly, Q27 request count, Q28 capacity assumption, Q58 non-significant gap noted, Q76 hours |
| 3 | 70 | ~9 (5 substantive) | Q17 "at most 35", Q37 North range 40% to 52%, Q60 premise re-diagnosed (blanks outside the 1,170), Q61 0.78%, Q15 example split |
| 4 | 80 | ~11 (2 wrong) | Q54 mixed bases fixed, Q34 UTC vs IST dip wrong orders, jargon explained (Fisher, NPS, eNPS, Simpson) |
| 5 | 101 | 7 | Q57 and Q67 illustration datasets added, Q64 Wilson interval, Q34 follow-up (p values), Q47 arithmetic |
| 6 | 92 | 16 | Q24 sample sizes, Q38 premise misread, Q43 circular seasonal index stated, Q51 top-customer claim, Q77 assumption, causes hedged |
| 7 | 60 | 10 | script claims removed, Q36 weighting wording, Q46 offsetting-gaps check, Q50 "possibly unlawful (confirm with legal)" |
| 8 | 62 | ~12 | Q4 data inconsistency with Q5 (1,480 - 90 - 40), Q38 say-line vs working, Q22 export size, Q1 timing, Q53 reworded |
| 9 | 24 | 6 | Q2 steps count, Q13 mock setup (3 x 10 + 15 = 45 min), illustrative labels; hour totals correct |

## Known limits (not fixed; honest status)
- **Legal and policy points** (India's DPDP Act, GDPR, US four-fifths rule, minimum group sizes, breach notification, PF/ESI rates) are stated as principle only and labelled "from memory, unverified, confirm with legal/owner"; none could be verified (no web access).
- **Tool and platform facts** (Power BI Performance Analyzer, incremental refresh, query folding, Excel 15-digit and row limits, dbt, Great Expectations, IST having no daylight saving) are from memory and labelled unverified.
- **Illustrative figures**: all project, example and stakeholder-script numbers in Parts 8 and 9 and many in Parts 1-7 are invented examples (labelled), not data; personal-experience and project answers are templates the candidate must replace with true experience.
- **"Asked at"** claims rest on prep-site snippets; no first-hand company reports were found for most scenario types; stars are judgement. The Part 7 sources file still says 61 questions (the part has 60 after the duplicate removal).
- **Overlap:** many deliberate overlaps inside parts (join fan-out, Excel ID damage, mix/Simpson reversals, bridges, selection-bias cluster) and with other books (Book 7 root-cause cases, Book 6 Part 8 DI drills, Book 5 statistics, Book 4 performance); kept and cross-referenced; not removed.
- Some questions have inline-data premise issues that the answers diagnose rather than fix (Part 6 Q33 missing definitions table, Q42 stated 515 vs 510, Q44 "seven-day" with five days, Q45 "by region"; Part 3 Q60; Part 4 Q47/Q55 missing denominators).
- A human read-through by a non-technical reader is still advisable.

# review_Part12.md: Book 1 Part 12 (How to develop Excel skills), Wave C

Date: 2026-10-22. Scratch: C1_Part12/run.py (all formulas run with tools/xl_eval.py, LibreOffice 24.2).

## Counts
- Answers checked: 24 of 24, plus the appended "Skill-development plan" (sections A to F).
- Formula results re-executed and matching the printed Result: 39 values. Q3 INDEX-MATCH 57000; Q5 all 15 summary cells plus check cell 0; Q8 TEXTJOIN (TRUE and FALSE); Q14 six checks (230000, 290000, 4, 5, 1, 1); Q16 SUMIF 344000; Q21 seven cells (33.3%, 4200, 25%, 3900, 0, #DIV/0!, 25%); Q22 T1-T8; Q24 both lookups, three SUMIFS, #N/A, IFERROR. No mismatches. Plan arithmetic checked: weeks 1-11 sum to 240; Month 1 = 105.
- Answers edited: 5 (Q8, Q9, Q10, Q15, Q22) plus plan sections A, E, F (formatting and one wording fix).

## Fixes
| Where | Problem | Fix |
|---|---|---|
| Q9, Q15, Q22, plan A, B, E | Table started on the line right after text or a heading, so it will not render in many Markdown viewers | Blank line inserted before each of the 6 tables |
| Q8 Version note | TEXTJOIN availability was "from memory, unverified" | Replaced with fetched Microsoft page: Applies To names 365, 2024, 2021, 2019; not 2016. Added note that the `_xlfn.` prefix was needed only for the test harness |
| Q8 Result | FALSE edge case was stated but not shown as run | Added the executed output `Asha, Dev, Isha, ` |
| Q10 follow-up | "about 1 million rows: from memory, unverified" | Replaced with 1,048,576 rows by 16,384 columns (fetched page) |
| Plan F | Said every quiz has 6 to 8 questions, but Quiz 4 and Quiz 5 have 6 and Quiz 6 has 5 scenarios | Changed to "5 to 8" |
| Q22 Formula/Steps | Did not say the key was executed | Added "the formula key was run in full" |

## Newly verified from fetched pages
- Microsoft Support, "TEXTJOIN function" (Applies To includes Excel 2019; availability sentence).
- Microsoft Support, "Excel specifications and limits" (1,048,576 rows, 16,384 columns).

## Plan completeness (style_guide.md Section 7)
Present: A roadmap (12 weeks), B daily plan (120 min), C free resources, D practice datasets, E mini-projects (3), F self-check tests. All six required parts exist.
Resource claims match research/Book01_Part12_sources.md: Exceljet "free resources and paid training", Microsoft video training unverified, Chandoo blocked, TrumpExcel "15 Free Datasets", AIHR 8 of 9 free, MOS "Price based on the country or region" with no amount stated (Q19 and plan C both say so; no amount quoted anywhere in the part).

## "Asked at" check
All 24 say "commonly asked (no company-specific report found)", with extra context only where the sources file supports it (Q2 thebricks, Q3 and Q18 igmguru, Q5 and Q7 and Q14 and Q15 MIS anecdotes, Q15 Novartis March 2023 checked in research/interview_processes.md, Q11/Q16/Q17 JD tallies). No unsupported company claim found.

## Claims still unverified (labelled in text)
- Excel 2016/2019 end-of-support date (14 Oct 2025): reported only; Microsoft page returned 404 earlier and was not retried.
- Power Query built into Excel 2016 and later; FILTER, SORT, LET availability; Copilot paid-plan status; Google Sheets facts (QUERY, IMPORTRANGE, XLOOKUP/FILTER/UNIQUE in Sheets, .xlsx import); Inspect Workbook path; five keyboard shortcuts; pivot "% of Row Total" in old versions; COUNTIFS/AVERAGEIF being Excel 2007+; DATEDIF status; SUMIFS "" criterion and text-to-number coercion in real Excel. I did not fetch Google or those Microsoft pages in this review.
- XLOOKUP: Q3 states the Microsoft page conflict (note says not in 2016/2019, Applies To lists them) and treats it as 2021/365: consistent with the rule.

## Unresolved / report only
- Quizzes 1-6 in the plan have no written formula keys (only the Final, T1-T8, does); the plan tells the learner to write their own keys. Only the Final key was executed.
- Q8 TEXTJOIN, Q3 XLOOKUP (not run here, labelled) are the only formulas not executed; Q3 expected 57000 equals the executed INDEX-MATCH.
- Q15 and Q24 pivot/mock content not runnable; Q24 pivot totals hand-checked and labelled.
- Part contains 24 answers vs target 20: fine. Ordering: stars descend 3,2,1 and within star 🟢 then 🟡 (checked: Q1-Q4 🟢 then Q5-Q6 🟡 etc.); no duplicates.
- Code fences balanced (none in the part). Beginner clarity: whole part read; no change needed.

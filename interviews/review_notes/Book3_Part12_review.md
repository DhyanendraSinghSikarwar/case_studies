# Book 3 Part 12 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40, in 8 timed mock sets (F1-F3 FAANG-style, T1-T3 fintech, E1-E2 e-commerce). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-10, Q11-20, Q21-30, Q31-40; merged by heading: 40 of 40 merged, 0 skipped, 0 pending. No spend-limit stops.

## Structure checks (scratch/review_scripts/check_book3.py)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40 | pass |
| Star order and counts 16 / 16 / 8 | pass |
| Template labels in every answer | pass |
| One runnable Code program per question, `python3 -I`, SQL asserted equal to pandas | pass, no failures |

## Scoring notes
Each answer carries a scoring note inside **Then explain:** using the part-header rubric split (correct result, edge cases, method, explanation, follow-up), scaled to the question's points.

## Findings kept in the text (premises corrected, honest differences)
- Q5 (RANGE frame over text timestamps) fails in SQLite with an OperationalError; integer seconds work.
- Funnel step order: chained global minimums (6, 3, 2) differ from the strict earlier-than-previous-step join (7, 4, 3).
- Fan-out: the naive three-table join overstates net by 200 (900 vs 700).
- Empty featured list: NOT EXISTS returns all customers, HAVING and pandas merge return none.
- RANGE default frame hides a running-balance dip that a ROWS frame shows; NULL rank sorts first ascending in SQLite.
- SQL vs pandas: 3/0 gives NULL in SQLite and inf in pandas; isin ignores the NaN that breaks NOT IN; all-NaN sum is 0.0 (min_count=1 used for the assert).
- Q27 as-of premise did not hold for young cohorts; the answer uses a different as-of date and shows a true zero separately. Several definitional choices (GMV, denominators, abandoned session, tie handling) are stated in the answers.

## Not verified (hedged "not executed")
PostgreSQL, MySQL, SQL Server, BigQuery, Snowflake and Oracle syntax and behaviour (division by zero, FILTER, QUALIFY, NULLS LAST, GENERATE_SERIES, INTERVAL frames, recursive CTE syntax, CONNECT BY, ASOF JOIN, timestamp BETWEEN end-of-day). A few points are "by reasoning, not run" and labelled so.

## Evidence limits
No source was found that reports exact questions from a named company; every web fetch failed, so sources are snippet-only editorial guides. The sets are expert designs in the style of publicly described formats, not candidate reports (see research_notes/Book3_Part12_sources.md).

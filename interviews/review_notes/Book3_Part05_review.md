# Book 3 Part 05 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 46 questions, Q1-Q46. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (46 of 46 merged, 0 skipped, 0 pending; no spend-limit stops this part). Header status updated after the merge. The Part column of the B3P04 index rows was corrected from 3 to 4 while preparing this part.

## Structure checks (scripted, scratch/review_scripts/check_book3.py)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q46 | pass |
| Star order and counts 18 / 16 / 12 | pass (matches header) |
| All template labels in every answer | pass for all 46 |
| Exactly one sqlite3 Code program per question, run standalone with `python3 -I` | 46 of 46 exit 0 |

## Code
Each program builds the data in SQLite 3.45.1, runs the SQL (window frames, LAG/LEAD, recursive CTEs where needed), runs pandas 3.0.5 and asserts SQL equals pandas with stated tie-breakers and duplicate-date handling. Outputs pasted from real runs; Q41's timings vary per run and are described as machine-specific. Part 5 stays on running totals, frames, LAG/LEAD and moving averages (ranking is Part 4, gaps-islands Part 7, cohorts Part 6).

## Behaviours the Wave A note listed as unverified, now run (3.45.1 / 3.0.5)
GROUPS and EXCLUDE (CURRENT ROW, GROUP, TIES, NO OTHERS) run; GROUPS 1 PRECEDING ignores date gaps while RANGE respects them; RANGE with a numeric offset on a TEXT date gives silently wrong sums (each row summed only itself; ORDER BY julianday or an integer day number fixes it; the cause was not isolated); RANGE with an offset needs exactly one ORDER BY expression; RANGE INTERVAL, IGNORE NULLS, LAG IGNORE NULLS, NTH_VALUE FROM LAST, QUALIFY, DATE_TRUNC and DATEDIFF are errors; COUNT(DISTINCT) OVER is rejected; ln() and exp() exist in this build; pandas groupby().nth returns rows with the original index; expanding().rank() works (default average ties); groupby().rolling('7D', on=...) equals SQL RANGE 6 PRECEDING on distinct midnight dates and differs on duplicate dates; ewm default adjust=True; pct_change in pandas 3 does not forward-fill, fill_method must be None, zero base gives inf, freq='D' aligns by calendar; shift(freq=) moves labels not data; shift on int gives float64; Int64 cumsum keeps NA and skipna=False poisons the tail.

## Findings kept in the text
Default frame and duplicate-date peers in running totals; ROWS 7-day frames widening over missing days; LAG compares across missing months and LAG(12) breaks with gaps or duplicate months; LAG default fills only the edge; NULL-poisoned SQL recursions vs pandas skipping; the "obvious" leave-one-out mean formula wrong with NULL salaries; julianday float gaps (30.000000223517418) needing ROUND; LN-based running product diverges on returns <= -100% or NULL; transform('first') skipping NaN; resample('MS').sum() creating zeros; ambiguous "rank so far" with same-date games; three rises need LAG(3); thresholds like cum_share <= 0.8 dropping the crossing row; same-date ordering flipping an overdraft flag; the timings did not support "RANGE with offsets is expensive".

## Not verified (hedged "not executed" in the text)
PostgreSQL 11+ GROUPS/EXCLUDE, MySQL 8 having ROWS and RANGE only, PostgreSQL INTERVAL RANGE offsets, IGNORE NULLS support in Snowflake/BigQuery/Oracle, DATEDIFF/TIMESTAMPDIFF/DATE_TRUNC dialects, division by zero and integer division in other engines, SQLite window version history (3.25/3.28 from the Part 4 note), sliding-frame cost behaviour, LeetCode 1308/197/180/1321 wording (from memory or snippets), the root cause of the SQLite text-RANGE behaviour, banks posting credits before debits.

## Evidence limits
No candidate-reported questions were found; evidence is prep guides, public problem banks and the PostgreSQL, pandas and SQLite docs listed in the sources note (the SQLite window page returned 503 in Wave A). One guide claims a Microsoft phone screen asked a per-user running total; that is the site's own unverified claim. No source states a salary band. Stars and "Asked at" tags are indicative.

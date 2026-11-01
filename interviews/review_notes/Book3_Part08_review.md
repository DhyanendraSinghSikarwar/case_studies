# Book 3 Part 08 review (Wave C)

Date: 2026-10-25. Reviewer: lead session (independent of the four answer agents). Scope: 45 questions, Q1-Q45. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (45 of 45 merged, 0 skipped, 0 pending). All four agents were interrupted once by a spend limit and were resumed after the reset (the user lifted the pause with "continue working on that"). One premise error found by an answer agent in Q23-33 (rolling().nunique) was verified by the lead, passed to the Q34-45 agent, and corrected in the Q42 question text, question_index.md, the build script and the sources note. Header status updated after the merge.

## Structure checks (scripted, scratch/review_scripts/check_book3.py)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q45 | pass |
| Star order and counts 18 / 16 / 11 | pass (matches header) |
| All template labels in every answer | pass for all 45 |
| Exactly one sqlite3 Code program per question, run standalone with `python3 -I` | 45 of 45 exit 0 |

## Code
Each program builds the data in SQLite 3.45.1, runs the metric SQL (funnels, active users, conversion by arm, attribution, revenue metrics, recursive date spines), runs pandas 3.0.5 and asserts SQL equals pandas with fixed as-of dates and stated week-start, time-zone, test-user and bot conventions. Counts and rates only: no p-values, no vendor benchmarks. Retention (Part 6), sessionization (Part 7), ranking (Part 4) and running totals (Part 5) are cross-referenced by checked question numbers.

## Items the Wave A note listed as unverified, now run (3.45.1 / 3.0.5)
SQLite ROUND is half away from zero (ROUND(2.5)=3, ROUND(6.25,1)=6.3) while Python, numpy and Series.round differ (and ROUND(2.675,2) is 2.67 in SQLite and Python but 2.68 in numpy/pandas); integer division truncates; power, exp and ln are available in this build (math functions) with a lookup-table fallback shown (max error 0.1138 on the sample); no MEDIAN (ROW_NUMBER/COUNT median works, NTILE(2) is not a median); recursive-CTE date and month spines work; datetime(x,'-7 days') and unixepoch agree at the exact 7-day boundary; unixepoch exists (3.38+); pandas rolling().nunique EXISTS in 3.0.5 and was cross-checked against the SQL range join; nunique and median skip NaN; pivot_table/crosstab/value_counts/groupby drop NaN keys by default, pivot_table aggfunc defaults to mean, crosstab drops empty categories unless dropna=False, observed=True default for categorical keys; merge matches NaN keys while SQL joins match none; merge_asof tolerance includes exactly 7 days; tz_convert('Asia/Kolkata') equals +330 minutes.

## Findings kept in the text
Time-window funnels need maturity filters (naive rate 25.0 vs 50.0 for mature users); strict first-of-each vs chained funnels differ (2 vs 3 purchasers); step 3 exceeding step 2 traced to double counting (7, 6, 5, 3 across four versions); channel taken per step gives 200 percent conversion unless first-touch is used; any-order purchase-over-cart contaminated by purchasers without a cart (80.0 vs 60.0); filtering the joined table in WHERE drops non-converters; DAU classes need a first_seen_late column to sum to DAU; stickiness differs by definition (0.0774 vs 0.75); fan-out inflates LTV (3300 vs 2300) and GMV (1700 vs 1150); dashboard reconciliation causes overlap (single effects add to 7 vs an actual gap of 6); SELECT DISTINCT * misses retries with different timestamps and a LAG 5-second dedup collapses chains; BETWEEN on timestamp text with a bare date returned 0 users; ROUND differences across SQLite, Python and pandas.

## Not verified (hedged "not executed" in the text)
Postgres, MySQL, BigQuery, Snowflake and ClickHouse syntax and behaviour (FILTER, date_trunc, DATE_FORMAT, COUNTIF, SAFE_DIVIDE, QUALIFY, ILIKE, DISTINCT ON, LATERAL, PERCENTILE_CONT, CONVERT_TZ, CONVERT_TIMEZONE, windowFunnel, division by zero); Apple Mail Privacy Protection open-inflation point (general knowledge, hedged); SRM thresholds (pointer only, vendor-dependent); LeetCode 1174, 1633 and 262 statements (1174 from a mirror, others from snippets); DAU/MAU benchmark percentages (not quoted); older pandas versions' rolling().nunique behaviour; the toy dashboards in the reconciliation question cannot reproduce the 1,250 and 1,190 figures.

## Evidence limits
No candidate-reported questions were found, including for Swiggy, Paytm, Flipkart or Zomato; evidence is prep guides, public problem banks, the pandas pivot_table and crosstab docs and a few vendor and blog pages (nine opened; the rest snippets). No source states a salary band. Stars and "Asked at" tags are indicative.

# Book 3 Part 5 Sources & research notes (Window functions: running totals, LAG/LEAD, moving averages)

Date: 2026-10-24. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch returns a model-summarised view ("as summarised"). No candidate-reported questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found; every source is a prep guide, practice-site page, documentation page or a search snippet. Final count: 46 questions (3-star 18, 2-star 16, 1-star 12), one above the 45 target.

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| PostgreSQL window-function syntax | https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS | official docs | ROWS/RANGE/GROUPS; RANGE offset needs exactly one ORDER BY column; date/timestamp offsets are intervals; EXCLUDE CURRENT ROW/GROUP/TIES/NO OTHERS; default frame RANGE UNBOUNDED PRECEDING (through last peer); no ORDER BY means whole partition is the frame; frame_start cannot be UNBOUNDED FOLLOWING |
| PostgreSQL window functions table | https://www.postgresql.org/docs/current/functions-window.html | official docs | lag/lead offset default 1 and default NULL; first_value/last_value/nth_value use the frame; default frame is "unhelpful" for last_value; IGNORE NULLS/RESPECT NULLS and FROM LAST not implemented in PostgreSQL |
| pandas DataFrame.rolling | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html | official docs (page showed pandas 3.1.0 dev) | min_periods default = window size for int windows and 1 for offset windows; closed default 'right' (a, b]; offsets must be fixed frequencies ('B', 'ME' raise); center; step; on; forward-looking via FixedForwardWindowIndexer |
| pandas DataFrame.pct_change | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html | official docs | fill_method must be None and will be removed; use ffill() first; freq passes to shift; fraction not percent. Page does not cover zero base (inf) |
| pandas DataFrame.shift | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shift.html | official docs | periods can be a list; freq shifts the index not the data; fill_value; int becomes float64 with default NaN fill, integer fill_value keeps int |
| StrataScratch top five window functions blog | https://www.stratascratch.com/blog/top-five-sql-window-functions-for-data-science-interviews | blog guide | LAG/LEAD month-over-month (the example uses LEAD), SUM running total, 10-day moving average, ROW_NUMBER first visit, DENSE_RANK; only Netflix named (top shows) |
| LearnSQL revenue growth in SQL | https://learnsql.com/blog/revenue-growth-in-sql/ | blog guide | LAG for MoM, percent formula, first row NULL, LEAD(revenue, 12) for next year, does not discuss divide by zero or missing months |
| Craig Kerstiens month-over-month growth | https://craigkerstiens.com/2014/02/26/Tracking-Month-over-Month-Growth-in-SQL | blog | LAG over date_trunc month; the page's formula (1 - current/previous) has a sign error per the summary; gaps break LAG; NULLIF for zero; lag applied to the aggregate |
| codemia running total partitioned by user | https://codemia.io/practice/window-function-lead-lag-over-date | practice site | per-user running total; site states Microsoft data scientist phone screen (self-reported by the site, unverified); related Walmart, CrowdStrike, Cloudflare pages are only "related" |

## Fetch failed
- SQLite window functions page (https://www.sqlite.org/windowfunctions.html and sqlite.org variants): HTTP 503 three times. It was opened in Part 4 (see Book3_Part04_sources.md), but the frame, GROUPS, EXCLUDE and RANGE-offset text was NOT re-confirmed from the page in Part 5. Wave B must confirm by running.
- getgalaxy window-function interview page: 404. LeetCode restaurant-growth page: 403. GeeksforGeeks SQL interview questions: 403 (could not check for running-total entries). datasciencewallah Medium 1321 write-up: 403. Red Gate count-distinct article: not opened.

## Search results only (snippets, not opened)
- LeetCode 1321 Restaurant Growth: statement from a search snippet (moving average over 7 days, current plus 6 before, rounded to 2 decimals, ordered by visited_on); Medium walkthrough snippet (CTE of daily totals, ROWS 6 PRECEDING, filter first six days); an Inflearn thread reports a self-join solution that works in MySQL Workbench but fails on LeetCode. LeetCode 1308 (Running Total for Different Genders), 197 (Rising Temperature) and 180 (Consecutive Numbers): title-only from a Scribd list; statements below are from memory and unverified.
- Default frame and duplicate dates: reintech, oneuptime (MySQL), Brent Ozar, mssqltips, Databend and TiDB docs, Medium row-vs-range: all agree that the ORDER BY default is RANGE through peers, ROWS or a tie-breaker fixes it. Not opened.
- LAST_VALUE trap: oneuptime MySQL, SQL Server Central, Snowflake and Bodo docs, a 2009 PostgreSQL mailing-list thread. One snippet claims Snowflake's default frame is the whole window (differs from the standard): unverified, hedge or leave out.
- COUNT(DISTINCT) OVER: PostgreSQL mailing list (DISTINCT not implemented for window functions), a 2018 SQLite check-in that returns an error for DISTINCT in a window function (consistent with my run on SQLite 3.45.1), Red Gate DENSE_RANK trick, ITPro Today (SQL Server). First-occurrence flag trick is general knowledge, not found in a source.
- Forward fill: ibis how-to, DEV Community, SingleStore forum, Daft and VeloDB docs: running COUNT as group id then MAX/FIRST_VALUE; IGNORE NULLS native in some engines.
- getgalaxy, ai2sql, dataengineerthings, a LinkedIn "25 time series SQL questions" post and Scribd performance deck: guide-level mention only.
- DataLemur and StrataScratch company-labelled MoM or running-total problems: search surfaced no actual problem pages; nothing verified.
- pandas rolling '7D' versus SQL RANGE INTERVAL: search returned only pandas docs; the equivalence of (t-7D, t] to t-6..t for midnight daily data is my inference, to be run by Wave B.

## Quick checks I ran on this machine (SQLite 3.45.1, pandas 3.0.5), for Wave B to reproduce
- RANGE with a numeric offset on a TEXT date column (ORDER BY d RANGE BETWEEN 1 PRECEDING ...) raised no error and gave wrong sums; ordering by julianday(d) gave the right calendar window.
- GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW and ROWS ... EXCLUDE CURRENT ROW both ran on 3.45.1.
- count(distinct v) OVER (...) raised "DISTINCT is not supported for window functions".
- RANGE ... INTERVAL 1 DAY PRECEDING is a syntax error on SQLite.
- LAG(v, 1, -1) default works. ln() and exp() exist in this Python's SQLite build (math functions are build dependent).
- pandas: Series([0,5,nan,10]).pct_change() gave [nan, inf, nan, nan]; Series([1,2]).shift() dtype float64.

## Provenance of the questions
- Guide-supported: running total, per-group running total, LAG/LEAD, DoD/MoM change, moving average, default-frame duplicate-date trap, ROWS vs RANGE, LAST_VALUE trap, running balance, YoY with LAG(12) and the gap caveat, forward fill, cumulative distinct workaround, LeetCode 1321, 1308, 197, 180 (titles).
- Documentation-supported: frames, EXCLUDE, offsets, first/last/nth_value, IGNORE NULLS absence in PostgreSQL, pandas rolling/shift/pct_change.
- Expert gap-check only: inventory stock, meter resets, running rank, trailing-7-day customers, EWMA, reset-by-condition, cumprod, Pareto share, time gaps, leave-one-out EXCLUDE, performance, fault-finding drill, YTD reset, orders in trailing 7 days.
- Candidate-reported: none (codemia's Microsoft claim is site-reported only).
- Overlap with Part 4: FIRST_VALUE/LAST_VALUE/NTH_VALUE questions appear here because the Part 5 brief lists them; Part 4 covers them as rank-family helpers. Lead may merge if desired. Question index Part column: B3P05 rows use 5 (note B3P04 rows in the index carry 3, apparently a slip, left untouched).

## Unverified; Wave B must hedge or run
- SQLite frame/GROUPS/EXCLUDE text and 3.28.0 version history (page unreachable this session; run, and cite Part 4 notes for 3.25/3.28).
- PostgreSQL 11+ for GROUPS and EXCLUDE (version from general knowledge; the docs page opened does not give versions); MySQL 8.0 window support and absence of GROUPS/EXCLUDE; Snowflake and other engines' default frames; BigQuery/Snowflake RANGE with INTERVAL; DATEDIFF, DATE_TRUNC: hedge, not executed.
- pandas: groupby().nth(1) behaviour in 3.0, Rolling.rank / expanding().rank availability, rolling on groupby with 'on', ewm adjust default and first values, pct_change with periods and freq, cumsum skipna on nullable dtypes, shift(freq): run on 3.0.5.
- SQLite math functions (ln, exp) availability on other builds; recursive CTE for EWMA and capped reset (run).
- LeetCode 1308, 197, 180 statements (title only); 1321 exact wording (snippet only).
- Whether pandas rolling('7D') (t-7D, t] matches RANGE over day numbers t-6..t on midnight dates (inference, run).

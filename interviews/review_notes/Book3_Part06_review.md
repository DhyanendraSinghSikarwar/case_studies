# Book 3 Part 06 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 45 questions, Q1-Q45. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (45 of 45 merged, 0 skipped, 0 pending; no spend-limit stops this part). One agent reported briefly running sibling agents' files from the shared scratchpad by mistake (read-only; it removed the output files it created); all merged programs were re-run by the lead's check below and pass, and no answer shows signs of interference. Header status updated after the merge.

## Structure checks (scripted, scratch/review_scripts/check_book3.py)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q45 | pass |
| Star order and counts 18 / 16 / 11 | pass (matches header) |
| All template labels in every answer | pass for all 45 |
| Exactly one sqlite3 Code program per question, run standalone with `python3 -I` | 45 of 45 exit 0 |

## Code
Each program builds the data in SQLite 3.45.1, runs the SQL with date(), strftime(), julianday(), unixepoch() and modifiers (plus recursive calendar CTEs), runs pandas 3.0.5 and asserts SQL equals pandas, using fixed as-of dates and a stated week-start and time-zone convention. One row in Q45 is deliberately not asserted equal (pandas parses '2024-1-6', SQLite strftime returns NULL).

## Items the Wave A note listed as unverified, now run
ISO-year/week emulation date(d,'-3 days','weekday 4') matches isocalendar() on every day 2000-2040 (14,976 days); strftime %V %U %G %g return NULL, %W works; floor/ceiling/end of month/weekday -1 modifiers return NULL on 3.45.1; resample defaults (MS left/left; ME, W, W-MON right/right; W-MON needs closed='left', label='left'; 'M' removed in favour of 'ME'); dt.floor('MS') raises ValueError (non-fixed frequency); to_period('Q-MAR') labels by fiscal year end (2024-04 is 2025Q1); groupby drops NaT keys unless dropna=False; DateOffset month clipping and drift; tz_localize raises plain ValueError for ambiguous and nonexistent times (no AmbiguousTimeError in pd.errors, pytz not installed); bdate_range(freq='C', holidays) and np.busday_count (end date excluded); resample('D') on a tz-aware index gives 23 and 25 hour days; partial-string slicing includes the whole last day while <= Timestamp does not.

## Findings kept in the text
BETWEEN with bare end dates drops the last day; date('2024-02-30') rolls to 03-01; '+1 month' overflow vs DateOffset clipping; localtime depends on process TZ; CAST truncation vs Timedelta floor; classic vs cumulative vs rolling retention differ (rolling day-7 went 25.0 to 50.0 with the as-of date); immature cohorts must be NULL not 0; zero-fill then cumsum draws false flat tails; LAG(12) wrong with missing and duplicate months; Grouper emits empty weeks where SQL omits them; pandas groupby drops NULL keys (4 vs 5 rows); empty-table denominator NULL vs ZeroDivisionError; dividing by distinct dates overstates weekday averages; milliseconds read as seconds give year 55840 in pandas and NULL in SQLite; timediff is not symmetric; the "share of observed" survival curve is not monotone (teaching version, not Kaplan-Meier).

## Not verified (hedged "not executed" in the text)
DATE_TRUNC, DATEDIFF argument order, EXTRACT, AGE, TIMESTAMPDIFF, DATE_DIFF, AT TIME ZONE, CONVERT_TZ, CONVERT_TIMEZONE, generate_series, GENERATE_DATE_ARRAY, YEARWEEK/ISOWEEK/WEEKISO, week-start defaults, PIVOT, FILTER and month-add clipping per engine; DATETRUNC in SQL Server 2022; functional indexes and partition pruning elsewhere; the 4-4-5 fiscal calendar remark; LeetCode 550/1193/197/262 statements (sample data is our own); pytz error class names; pandas 2 behaviour for milliseconds read as seconds; VM-step counts (indicative only); India fiscal year April-March (from general knowledge).

## Evidence limits
No candidate-reported questions were found; the Intuit tag on one cohort-retention prompt is site-reported and unverified. Evidence is prep guides, public problem banks, the SQLite date function page (opened), the pandas time series guide (first 100,000 of 167,306 characters read) and retention-definition write-ups with no independent standard. No source states a salary band. Stars and "Asked at" tags are indicative.

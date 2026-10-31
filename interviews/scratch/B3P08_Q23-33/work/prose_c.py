P = {}

P[31] = dict(
say="Most differences are NULL versus NaN handling and number types: `nunique` and `COUNT(DISTINCT)` skip missing values but `len(set(series))` does not, `groupby` drops NaN keys while `GROUP BY` keeps a NULL group, SQLite `3/2` is 1 while pandas gives 1.5, SQLite rounds halves away from zero while Python and numpy round halves to even (and numpy and Python can still disagree), SQLite returns NULL for division by zero while pandas gives inf or NaN, and pandas `merge` matches NaN keys to each other while SQL joins never match NULLs. I ran every row below.",
schema_note="a five-row table `t(id, k, u, v)` with a NULL in each of `k`, `u` and `v` (k is a, a, NULL, NULL, b; u is 10, NULL, 10, NULL, 20), and two two-row tables `l` and `r` that each have a NULL key. There is no single query and pandas function pair here; every row is a small printed demonstration, so the SQL and pandas answers are the statements in the Code block.",
schema=None,
sqlnote="the statements are in the Code block (for example `SELECT COUNT(DISTINCT u) FROM t`, `SELECT 3/2`, `SELECT ROUND(2.5)`, `SELECT 1/0`, `SELECT l.k, lv, rv FROM l JOIN r ON l.k = r.k`).",
sqls=[],
sqlafter="",
pdnote="the pandas calls are in the Code block (`df['u'].nunique()`, `df.groupby('k')`, `pd.Series([3]) / 2`, `pd.Series(vals).round()`, `L.merge(R, on='k')`).",
example="""Translation table, every cell from my run (SQLite 3.45.1, pandas 3.0.5, numpy 2.5.3):

| Topic | SQL (SQLite) | pandas / Python |
|---|---|---|
| Distinct count of u (10, NULL, 10, NULL, 20) | `COUNT(DISTINCT u)` = 2; `COUNT(u)` = 3; `COUNT(*)` = 5 | `nunique()` = 2; `nunique(dropna=False)` = 3; `len(set(series))` = 4 (each NaN is a separate object); `len(unique())` = 3 |
| Group on k (a, a, NULL, NULL, b) | `GROUP BY k` returns three groups: NULL 2, a 2, b 1 | `groupby('k')` gives a 2, b 1 (NaN group dropped); `dropna=False` adds NaN 2; `value_counts()` drops NaN, `dropna=False` keeps it |
| Integer division | `3/2` = 1, `-3/2` = -1 (truncates toward zero), `3/2.0` = 1.5 | `3/2` = 1.5; `3//2` = 1; `-3//2` = -2 (floors); `int(-3/2)` = -1; Series `/` and `//` match Python |
| Rounding halves | `ROUND(0.5)`, `ROUND(2.5)`, `ROUND(-2.5)` = 1.0, 3.0, -3.0 | Python `round(2.5)` = 2, `round(0.5)` = 0, `round(-2.5)` = -2; numpy and `Series.round()` the same (half to even) |
| Rounding to 2 places | `ROUND(0.125, 2)` = 0.13, `ROUND(2.675, 2)` = 2.67, `ROUND(1.005, 2)` = 1.0 | Python 0.12, 2.67, 1.0; numpy and `Series.round(2)` 0.12, **2.68**, 1.0 |
| Division by zero | `1/0`, `1.0/0`, `0.0/0` all NULL; `1/NULLIF(0,0)` NULL; `SUM` and `AVG` of no rows NULL, `COUNT` 0 | Python `1/0` raises `ZeroDivisionError`; float Series gives inf (1/0) and NaN (0/0); empty `sum()` = 0.0, `mean()` = NaN |
| Join or merge on a NULL key | `INNER JOIN` returns only the 'a' row; `LEFT JOIN` keeps the NULL row with no match; `NULL = NULL` is NULL | `merge(on='k')` **matches NaN to NaN**: the inner merge returned the NaN row with rv 20 |
| Rolling distinct | no window `COUNT(DISTINCT ...)` in SQLite (range join, Q33) | `Series.rolling(n).nunique` exists in pandas 3.0.5 (docstring says added in 3.0.0), see Q33 |

What the run showed that I did not expect:
- `len(set(series))` is 4 and not 3: a float column with two NaN values gives two separate NaN objects, and a Python set treats each NaN as different from every other. `nunique()` and `unique()` handle this properly.
- `ROUND(2.675, 2)` agrees with Python's 2.67 but numpy and pandas give 2.68, so numpy is not the same as Python's `round` either. Neither is 'wrong'; they scale and round differently on binary floats.
- `rolling().nunique` is available in pandas 3.0.5, which contradicts the Wave A premise of its absence (checked here by `hasattr` and by a real call in Q33).""",
edge="""- `COUNT(DISTINCT col)`, `AVG(col)`, `SUM(col)` ignore NULL; `COUNT(*)` does not. pandas `size()` counts rows, `count()` counts non-null, like `COUNT(*)` and `COUNT(col)`.
- `SELECT DISTINCT u` returns the NULL as one distinct row (3 rows) while `COUNT(DISTINCT u)` gives 2: the two differ on NULL by design.
- Rounding a percentage like 12.5 percent to a whole number gives 13 in SQLite and 12 in pandas; in a reconciliation this shows as a one-unit mismatch that is not a data bug.
- A pandas integer Series divided by a zero Series gave inf and NaN in my run (no exception); Python integers raise.
- Other engines: PostgreSQL integer division also truncates and division by zero raises an error; MySQL `/` returns a decimal and `DIV` is integer division; BigQuery `/` returns a float and `SAFE_DIVIDE` returns NULL on zero (all from memory, not executed here).""",
explain="""- Rule of thumb: SQL treats NULL as unknown (never equal to anything, including NULL), pandas treats NaN as a value that most aggregations skip but that `merge`, `set` and sorting treat in their own way.
- For metric code, make the rule explicit: fill or filter missing keys before grouping, `dropna=False` where a NaN group matters, `* 1.0` or `/` for ratios, and one agreed rounding helper.
- If a pandas result must equal SQL to the cent, do not rely on `round`; round once at the end the same way (half away from zero needs a helper) or compare with a tolerance.
- Rows were run in the Code block; the three asserts at the bottom pin the claims 'COUNT(DISTINCT) equals nunique', '3/2 is 1 versus 1.5' and 'ROUND(2.5) is 3.0 versus Python 2'.""",
fu="""- How do you make pandas merge behave like SQL on NaN keys? Drop or mask the NaN-key rows before the merge (`dropna(subset=['k'])`); then an inner merge matches SQL.
- How do you round half away from zero in pandas? Use `np.sign(x) * np.floor(np.abs(x) * 100 + 0.5) / 100`, accepting binary float effects; I did not run this helper here.
- Why did the NULL group show in SQL but not in pandas by default? Different design: SQL groups NULLs together, pandas drops them unless `dropna=False`.""",
mist="""- Assuming `groupby` totals add to the table total when the key has NaN.
- Using `len(set(...))` on a float column for distinct users.
- Expecting `/` to be integer division in SQLite or float division in older engines without checking.
- Rounding in pandas and SQL separately and then 'finding a bug' of 0.01.
- Merging on a key with NaN and getting extra rows that SQL would not return.""",
)

P[32] = dict(
say="Count distinct users per arm (not rows), compare each count with the planned share times the total, and the chi-square statistic is the sum of (observed - expected)^2 / expected over the arms, computed in plain arithmetic in the query; users assigned to both arms are found with `HAVING COUNT(DISTINCT arm) > 1` and reported separately, and the p-value and the strictness of the threshold are left to Books 1 and 6 (teams commonly use strict thresholds such as p < 0.001 for SRM, which varies by team and is only a pointer here).",
schema_note="seventeen assignment rows, fourteen distinct users. User 2 is assigned to control twice, user 11 to treatment twice, and user 14 appears in both arms. The planned split is 50/50. A second, generated table of 10,000 control and 10,600 treatment users is used in the Code block for the arithmetic at scale.",
schema="SCHEMA",
sqlnote="`SQL_MAIN` in the Code block (the planned split is a small `plan` table so it can change; `SQL_BOTH`, `SQL_ROWS`, `SQL_DUP` and `SQL_CLEAN` are the supporting queries):",
sqls=["SQL_MAIN", "SQL_BOTH"],
sqlafter="",
pdnote="the same logic as a function, identical to the Code block (`clean=True` removes users in both arms first):",
example="""- Rows: control has 11 rows (users 1 to 9 with user 2 twice, plus user 14), treatment has 6 rows (users 10 to 13 with user 11 twice, plus user 14). Distinct users: control 10, treatment 5 (user 14 is in both). The row count of 17 against 14 distinct users shows three users with repeated rows (2, 11, 14).
- Per arm, counting user 14 in each arm: total 15, expected 7.5 each, observed shares 0.6667 and 0.3333, difference +2.5 and -2.5, chi parts 2.5^2/7.5 = 0.8333 each, chi-square 1.6667.
- Counting rows instead (wrong unit): 11 and 6, total 17, expected 8.5, chi-square 1.4706. The statistic changes because duplicates changed both the counts and the total.
- Removing the one user in both arms: 9 versus 4, total 13, expected 6.5, chi-square 1.9231.
- At scale (generated): 10,000 versus 10,600, total 20,600, expected 10,300, difference -300 and +300, chi parts 8.7379 each, chi-square 17.4757. Comparing that statistic with a threshold is out of scope here (Book 1 and Book 6).""",
edge="""- Users in both arms: reported by `SQL_BOTH` (user 14). Whether to count them in each arm, drop them, or keep their first assignment is a decision; the raw and clean versions are both printed.
- Repeat rows for the same user and arm (users 2 and 11) inflate row counts but not distinct counts, which is why distinct users are the unit.
- An arm with zero users would make `plan` and `obs` not join; use a LEFT JOIN from `plan` if an arm can be missing.
- Expected counts below about 5 make a chi-square approximation unreliable (rule of thumb from statistics, not checked here); the toy data is only for arithmetic.
- Assignment time: late assignment or filtering on users who reached a page can itself cause an imbalance; this query only counts.""",
explain="""- Counting unit: distinct users, because the randomisation unit is the user. Rows include retries and re-assignments.
- Expected count is the planned share times the total distinct users, not the planned share times the larger arm.
- The chi-square statistic here is just arithmetic on counts; turning it into a p-value (1 degree of freedom for two arms) and choosing a threshold belongs to Books 1 and 6, and thresholds differ between vendors and teams.
- Why an SRM invalidates the conversion table from Q13: if assignment counts are off from the plan, something other than the treatment (a bug, a filter, a redirect) decided who ended up in each arm, so the two arms are no longer comparable populations and uplift in the Q13 table could come from that, not from the treatment. Fix the cause before reading any metric (contamination handling is Q44).
- Dialect: the `VALUES` plan table works in SQLite and Postgres; in BigQuery or Snowflake use a CTE with `SELECT ... UNION ALL` (not executed here).""",
fu="""- Three arms? Add a row to `plan`; the chi-square sum is unchanged (degrees of freedom change, a Book 1 point).
- Check SRM per day or per segment? Group the observed CTE by day or segment, and compare each to its own total.
- What do you do when SRM is flagged? Stop reading results, find the cause, rerun or exclude the affected segment.""",
mist="""- Counting rows instead of distinct users.
- Computing expected counts from the larger arm.
- Ignoring users in both arms.
- Reading a small chi-square as proof of no problem on tiny samples.
- Computing the p-value here and skipping the cause analysis.""",
)

P[33] = dict(
say="Build a 31-row date spine with a recursive CTE, reduce events to distinct (user, date) rows, range-join each spine day to the user-days in `[day - 29, day]`, and take `COUNT(DISTINCT user_id)` for the rolling MAU and the distinct users on the day itself for DAU; stickiness is DAU over rolling MAU per day, and `ROWS BETWEEN 29 PRECEDING` over daily counts is wrong because a user active on five days would be counted five times.",
schema_note="fourteen events from 2024-01-31 to 2024-03-31 for five users. Conventions: the timestamps are UTC text, the day is the UTC date, and no test-user or bot table exists in this question so none is filtered (a real report would join `users` and filter, as in Q1). Events before March matter because the 30-day window reaches into February (2024 is a leap year). User 4's January 31 event is just outside the window of 2024-03-01; user 3's February 1 event is just inside. User 1 has two events on 2024-03-02, so one user-day.",
schema="SCHEMA",
sqlnote="`SQL_MAIN` in the Code block (`SQL_WRONG` is the window-frame version, printed for comparison):",
sqls=["SQL_MAIN"],
sqlafter="",
pdnote="the same logic as a function, identical to the Code block (cross merge of the spine with user-days, then filter to the window, then `nunique`):",
example="""- 2024-03-01: window is 2024-02-01 to 2024-03-01 (30 days: 29 in February because of the leap year, plus 1 March). Active users in it: user 3 (Feb 1, the first day of the window), user 2 (Feb 20), user 1 (Feb 5 and Mar 1). User 4 (Jan 31) is out. Rolling MAU = 3, DAU = 1 (user 1), stickiness 1/3 = 0.3333.
- 2024-03-02: window 2024-02-02 to 2024-03-02. User 3's last event (Feb 1) has dropped out, so users 1 and 2: MAU 2. DAU is 2 (user 1 twice on that day is one, plus user 2), stickiness 1.0.
- 2024-03-04: no events, DAU 0, but the rolling MAU is still 2 (users 1 and 2 are in the window). Without the spine this day would not exist; with it the row shows stickiness 0.0.
- 2024-03-15: user 3 returns; window is Feb 15 to Mar 15 so users 1, 2, 3, 5 give MAU 4, DAU 1, stickiness 0.25. 2024-03-31: window Mar 2 to Mar 31: users 1, 2, 3, 4, 5 are all in, MAU 5, DAU 2 (users 1 and 2), stickiness 0.4.
- Window-frame version: on 2024-03-31 summing daily DAU over 30 rows gives 8, not 5, because users 1 and 2 are counted on several days; on 2024-03-02 it gives 3 against a true 2. (That version also only sees March because the spine starts on March 1, a second flaw.)""",
edge="""- Days with no events: the LEFT JOIN from the spine keeps them (DAU 0). If the window had no users at all, MAU would be 0 and stickiness NULL through `NULLIF`; no such day occurs in this data (days with MAU 0: 0 in the output).
- Window length: a 30-day window ending on the day is `date(day, '-29 days')` to `day` inclusive. A 30-day window with `-30 days` is 31 days and a common off-by-one.
- Date arithmetic: I checked `date('2024-03-01','-29 days')` and `datetime('2024-03-08 10:00:00','+7 days')` against `unixepoch` arithmetic with 86400 seconds; they agree across the leap day (the Code block asserts it). Unlike `julianday` times a constant, this keeps whole days exact.
- Time zone: the day is the UTC date; a user in IST has evening events that fall on the next UTC date, so DAU by IST day differs (Q19, Q36).
- Duplicate events in a day are collapsed by the `DISTINCT` in the `ud` CTE; the range join then sees one row per user-day.
- pandas `Rolling.nunique`: exists in pandas 3.0.5 (the docstring says added in 3.0.0), so the premise that it does not exist is wrong for this version. It works on a time-indexed series with a `'30D'` window, but only produces values at rows that exist, so days without events still need the spine; the Code block checks it on the 7 days that have event rows.""",
explain="""- A rolling distinct count cannot be built from daily distinct counts: the same user appears on many days, so summing `DAU` over 30 days is a count of user-days, not users. The only fix is to look at the underlying user-days.
- The spine guarantees one output row per day, including quiet days, and supplies the right edge of each window. Without it you get rows only for days with events and a row-based frame such as `ROWS BETWEEN 29 PRECEDING` would silently span more than 30 calendar days.
- Range join cost: each spine day matches up to 30 days of user-days, so the work is roughly spine days times window rows. On a large table you pre-aggregate to user-days first (done in `ud`), index or sort on date, and limit the spine. SQLite's plan here shows a scan with a temporary B-tree for the distinct counts, which I printed; I did not benchmark anything, and other engines (hedged: not executed) have their own range-join and distinct-count strategies, for example approximate distinct functions.
- An alternative that avoids the range join is to track each user's last active date and compare, or to use first-active-date flags for trailing new-user counts; not run here.
- Stickiness is DAU over the same day's rolling MAU here. The calendar-month version (average DAU over calendar MAU) is Q15; fixed-date DAU/WAU/MAU is Q1.""",
fu="""- Rolling WAU instead? Change `-29 days` to `-6 days`; the rest is identical.
- Calendar MAU instead of rolling? Fix the window to the month, as in Q15.
- Faster for a big table? Pre-aggregate to user-days (already done), partition by date, and in warehouses consider approximate distinct counts and say it is approximate.""",
mist="""- `ROWS BETWEEN 29 PRECEDING` over daily distinct counts (shown, wrong).
- No spine, so quiet days vanish and the frame is not 30 calendar days.
- Off-by-one window (`-30 days`).
- Range joining raw events instead of distinct user-days.
- Mixing time zones between the spine and the events.""",
)

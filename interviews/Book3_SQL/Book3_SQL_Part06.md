# Book 3 — Part 6: Date/time: retention, cohorts, month-over-month and year-over-year, with pandas equivalents

**Topic:** storing and truncating dates (TEXT ISO, Unix integers, Julian days; SQLite date(), datetime(), strftime(), julianday(), unixepoch(), modifiers), week-start conventions and ISO week traps, date arithmetic and end-of-month edge cases, timestamps versus dates and time zones, date-filter traps (BETWEEN, half-open ranges, sargability), date spines and calendar tables, gap filling, MoM and YoY (missing months, partial months), month-to-date, fiscal years, cohort analysis (first-order cohorts, retention tables, day-N retention definitions), churn and resurrection, new versus returning, active users per period, lifetime and recency, seasonality, business days, late-arriving data, and the pandas counterparts (to_datetime, dt, resample, Grouper, Period, date_range, DateOffset, tz_localize and tz_convert, pivot_table for cohort matrices).
**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 18, ⭐⭐ 16, ⭐ 11)  |  **Date:** 2026-10-24  |  **Status:** Answers written (Wave B), Wave C review done

Scope note: this part covers date and time handling for analytics and cohort retention. Funnels and DAU/MAU metric design (Part 8), gaps and islands, streaks and sessionization (Part 7), ranking and top-N (Part 4) and running-total mechanics (Part 5) are out; where a question touches them it stops at 'present in month m and m+1', LAG on a completed spine, or a cross-reference.

Evidence limits: no candidate-reported SQL questions were found. Sources are the SQLite and pandas documentation (opened), practice-site pages (PracHub, DataDriven; opened), and search snippets of prep guides and LeetCode-style problem banks. PracHub tags one cohort-retention prompt as an Intuit data scientist technical screen; the page cites no primary source, so treat it as site-reported. 'Asked at' tags are source types, and 'expert gap-check' marks questions added from practice rather than from a found source. SQLite engine notes for Wave B (checked on the installed SQLite 3.45.1): strftime %U, %V, %G and %g return NULL, %W works; the 'floor' and 'ceiling' modifiers, 'end of month' and negative 'weekday' arguments (documented as newer additions) return NULL; run, do not assume.

---

### Q1 ⭐⭐⭐ 🟢 Storing dates in SQLite: SQLite has no native date type. Explain the three conventions (TEXT in ISO 8601 such as '2024-03-05' or '2024-03-05 14:30:00', INTEGER Unix seconds, REAL Julian day numbers), and show with a small table events(event_id, event_date) why ISO text sorts and compares correctly while 'DD/MM/YYYY' text does not (ORDER BY and a range filter go wrong). Show date(), datetime() and strftime() on both an ISO text value and a Unix integer (with the 'unixepoch' modifier), what an invalid date string returns (NULL), and the pandas side: pd.to_datetime with format=, errors='coerce' (NaT) and dayfirst.
**Asked at:** SQLite date and time functions documentation (lang_datefunc, opened), vendor documentation and not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** SQLite has no date type: a date is TEXT in ISO 8601 (`'2024-03-05'`, `'2024-03-05 14:30:00'`), INTEGER Unix seconds, or REAL Julian day, and `date()`, `datetime()`, `strftime()` and `julianday()` convert between them; ISO text is the one to store because its alphabetical order is its chronological order, and `DD/MM/YYYY` text is not.

**Schema and sample data:** two copies of the same five events, one in ISO text and one in `DD/MM/YYYY` text. Convention for this whole answer: no time zone is stored, so every value is read as UTC.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, event_date TEXT);      -- ISO 8601 text
CREATE TABLE events_dmy(event_id INTEGER PRIMARY KEY, event_date TEXT);  -- DD/MM/YYYY text
INSERT INTO events VALUES (1,'2023-12-01'),(2,'2024-02-28'),(3,'2024-03-05'),(4,'2025-01-15'),(5,'2024-12-31');
INSERT INTO events_dmy VALUES (1,'01/12/2023'),(2,'28/02/2024'),(3,'05/03/2024'),(4,'15/01/2025'),(5,'31/12/2024');
```

**SQL answer:** the main query is the ISO range filter and ordering (`SQL_MAIN`); the second query is the same filter on the `DD/MM/YYYY` column (`SQL_DMY_WRONG`) to show the failure. Function checks on literals are in the code block.

```sql
SELECT event_id, event_date, strftime('%Y', event_date) AS yr
FROM events
WHERE event_date BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY event_date
```
```sql
SELECT event_id, event_date FROM events_dmy
WHERE event_date BETWEEN '01/01/2024' AND '31/12/2024'
ORDER BY event_date
```

**pandas answer:** parse the `DD/MM/YYYY` text with an explicit `format=` and then filter; with `errors='coerce'` bad strings become `NaT` instead of raising, and `dayfirst=True` is the shortcut when you do not give a format.
```py
parsed = pd.to_datetime(dmy["event_date"], format="%d/%m/%Y")
pd_df = (dmy.assign(event_date=parsed)
            .loc[lambda d: d["event_date"].between("2024-01-01", "2024-12-31")]
            .sort_values("event_date"))
pd_df["yr"] = pd_df["event_date"].dt.strftime("%Y")
pd_df["event_date"] = pd_df["event_date"].dt.strftime("%Y-%m-%d")
```

**Example:** ISO column, sorted as text: `2023-12-01 < 2024-02-28 < 2024-03-05 < 2024-12-31 < 2025-01-15`, which is ids 1, 2, 3, 5, 4 and is also the true date order. `BETWEEN '2024-01-01' AND '2024-12-31'` keeps ids 2, 3, 5.
- `DD/MM/YYYY` column, sorted as text: the comparison looks at the day first, so `'01/12/2023' < '05/03/2024' < '15/01/2025' < '28/02/2024' < '31/12/2024'`, which is ids 1, 3, 4, 2, 5. A 2025 date lands in the middle of 2024.
- `BETWEEN '01/01/2024' AND '31/12/2024'` on that column: `'01/12/2023' >= '01/01/2024'` is true (the 4th character '1' beats '0') and `'15/01/2025' <= '31/12/2024'` is true ('1' is below '3'), so all five rows pass instead of ids 2, 3, 5.
- Julian day: `julianday('2024-03-05 14:30:00')` is `2460375.1041666665`; midnight is always a `.5`. Unix seconds: `unixepoch('2024-03-05 14:30:00')` is `1709649000`. `datetime(1709649000,'unixepoch')` gives the text back.

**Code:** run with `python3 -I`.
```python
# Q1: SQLite date storage, ISO text vs DD/MM/YYYY text, date()/datetime()/strftime(), pandas to_datetime
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, event_date TEXT);      -- ISO 8601 text
CREATE TABLE events_dmy(event_id INTEGER PRIMARY KEY, event_date TEXT);  -- DD/MM/YYYY text
INSERT INTO events VALUES (1,'2023-12-01'),(2,'2024-02-28'),(3,'2024-03-05'),(4,'2025-01-15'),(5,'2024-12-31');
INSERT INTO events_dmy VALUES (1,'01/12/2023'),(2,'28/02/2024'),(3,'05/03/2024'),(4,'15/01/2025'),(5,'31/12/2024');
"""
SQL_MAIN = """
SELECT event_id, event_date, strftime('%Y', event_date) AS yr
FROM events
WHERE event_date BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY event_date
"""
SQL_DMY_WRONG = """
SELECT event_id, event_date FROM events_dmy
WHERE event_date BETWEEN '01/01/2024' AND '31/12/2024'
ORDER BY event_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("ISO range 2024, ordered:", sql_df.values.tolist())
print("ISO order by text    :", [r[0] for r in con.execute("SELECT event_id FROM events ORDER BY event_date")])
print("DMY order by text    :", [r[0] for r in con.execute("SELECT event_id FROM events_dmy ORDER BY event_date")], "(true order is 1,2,3,5,4)")
print("DMY BETWEEN 2024     :", con.execute(SQL_DMY_WRONG).fetchall(), "(true answer: ids 2,3,5)")

# the same instant in three storage conventions (2024-03-05 14:30:00, no zone, treated as UTC)
print(con.execute("""SELECT date('2024-03-05 14:30:00'), datetime('2024-03-05'), strftime('%d/%m/%Y', '2024-03-05 14:30:00'),
                            unixepoch('2024-03-05 14:30:00'), julianday('2024-03-05 14:30:00')""").fetchone())
print(con.execute("""SELECT date(1709649000,'unixepoch'), datetime(1709649000,'unixepoch'),
                            strftime('%Y-%m',1709649000,'unixepoch'), datetime(1709649000)""").fetchone())
print("julian day REAL back to text:", con.execute("SELECT datetime(2460375.1041666665)").fetchone())
print("offset suffix:", con.execute("SELECT datetime('2024-03-10T12:00:00+05:30'), datetime('2024-03-10T12:00:00Z')").fetchone())
print("invalid strings:", con.execute("""SELECT date('hello'), date('31/12/2024'), date('2024-13-01'),
                                               date('2024-02-30'), date('2024-02-29'), date('2023-02-29')""").fetchone())

fix = [r[0] for r in con.execute("SELECT substr(event_date,7,4)||'-'||substr(event_date,4,2)||'-'||substr(event_date,1,2) FROM events_dmy ORDER BY event_id")]
assert fix == [r[0] for r in con.execute("SELECT event_date FROM events ORDER BY event_id")]
print("substr rewrite of DD/MM/YYYY to ISO matches the ISO table:", fix)

# pandas side: parse DMY text explicitly
dmy = pd.read_sql_query("SELECT event_id, event_date FROM events_dmy", con)
# pd:main
parsed = pd.to_datetime(dmy["event_date"], format="%d/%m/%Y")
pd_df = (dmy.assign(event_date=parsed)
            .loc[lambda d: d["event_date"].between("2024-01-01", "2024-12-31")]
            .sort_values("event_date"))
pd_df["yr"] = pd_df["event_date"].dt.strftime("%Y")
pd_df["event_date"] = pd_df["event_date"].dt.strftime("%Y-%m-%d")
# pd:end
# compared in event_date order (ISO text sorts like dates)
assert pd_df.reset_index(drop=True).values.tolist() == sql_df.values.tolist()
print("pandas == SQL:", pd_df.values.tolist())

bad = pd.Series(["05/03/2024", "31/03/2024", "31/02/2024", "hello"])
print(pd.to_datetime(bad, format="%d/%m/%Y", errors="coerce").tolist())
print("dayfirst=True :", pd.to_datetime(pd.Series(["05/03/2024"]), dayfirst=True)[0].date())
print("default guess :", pd.to_datetime(pd.Series(["05/03/2024"]))[0].date(), "(month first, 5 March vs 3 May)")
try:
    pd.to_datetime(pd.Series(["05/03/2024", "31/03/2024"]))
except ValueError as e:
    print("default on mixed day>12 raises ValueError:", str(e).splitlines()[0])
print("dtype:", parsed.dtype)
print("asserts passed")
```

**Output (my run):**
```text
ISO range 2024, ordered: [[2, '2024-02-28', '2024'], [3, '2024-03-05', '2024'], [5, '2024-12-31', '2024']]
ISO order by text    : [1, 2, 3, 5, 4]
DMY order by text    : [1, 3, 4, 2, 5] (true order is 1,2,3,5,4)
DMY BETWEEN 2024     : [(1, '01/12/2023'), (3, '05/03/2024'), (4, '15/01/2025'), (2, '28/02/2024'), (5, '31/12/2024')] (true answer: ids 2,3,5)
('2024-03-05', '2024-03-05 00:00:00', '05/03/2024', 1709649000, 2460375.1041666665)
('2024-03-05', '2024-03-05 14:30:00', '2024-03', None)
julian day REAL back to text: ('2024-03-05 14:30:00',)
offset suffix: ('2024-03-10 06:30:00', '2024-03-10 12:00:00')
invalid strings: (None, None, None, '2024-03-01', '2024-02-29', '2023-03-01')
substr rewrite of DD/MM/YYYY to ISO matches the ISO table: ['2023-12-01', '2024-02-28', '2024-03-05', '2025-01-15', '2024-12-31']
pandas == SQL: [[2, '2024-02-28', '2024'], [3, '2024-03-05', '2024'], [5, '2024-12-31', '2024']]
[Timestamp('2024-03-05 00:00:00'), Timestamp('2024-03-31 00:00:00'), NaT, NaT]
dayfirst=True : 2024-03-05
default guess : 2024-05-03 (month first, 5 March vs 3 May)
default on mixed day>12 raises ValueError: time data "31/03/2024" doesn't match format "%m/%d/%Y". You might want to try:
dtype: datetime64[us]
asserts passed
```

**Edge cases:**
- Invalid input returns NULL: `date('hello')`, `date('31/12/2024')` and `date('2024-13-01')` were all NULL. Honest surprise: `date('2024-02-30')` returned `2024-03-01` and `date('2023-02-29')` returned `2023-03-01`. SQLite accepts any day 1 to 31 and rolls it over, so it does not validate the calendar. pandas rejects the same string (`'31/02/2024'` became `NaT` with `errors='coerce'`).
- A bare integer with no modifier is read as a Julian day: `datetime(1709649000)` returned NULL because it is out of range. Always add `'unixepoch'` for Unix seconds (milliseconds are Part 6 Q37).
- A trailing offset is applied and converted to UTC: `datetime('2024-03-10T12:00:00+05:30')` gave `2024-03-10 06:30:00`, and a `Z` suffix gave `12:00:00` unchanged. A column that mixes offsets and bare values is therefore silently inconsistent.
- pandas default parsing is month first: `'05/03/2024'` became 2024-05-03; a column that also holds `'31/03/2024'` raises `ValueError` under the default inference (pandas 3.0.5). `dayfirst=True` fixed the first case; for a fixed layout, prefer `format='%d/%m/%Y'`.
- NULL dates: `strftime` of NULL is NULL, `NaT` in pandas; both drop out of range filters.

**Then explain:**
- Rule: store ISO 8601 text (`YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS`), Unix integers or Julian days, never `DD/MM/YYYY`. ISO text sorts, compares, groups and indexes correctly with plain string operators.
- Text is easiest to read and debug; Unix integers are compact and zone-neutral; Julian day REAL is convenient for day arithmetic (`julianday(b) - julianday(a)`). The functions accept all three: text as is, numbers with `'unixepoch'` or as Julian days.
- Mixed lengths still sort correctly against each other when the prefix is ISO: `'2024-01-31'` sorts before `'2024-01-31 00:00:00'` (shorter string first). That is the root of the BETWEEN trap in Q4.
- pandas has real datetime64 values, so ordering and comparison are by instant, not by characters. The pandas 3 default unit for strings was `us` in my run (`datetime64[us]`).
- Other engines (not executed here): PostgreSQL, MySQL, BigQuery and Snowflake have native DATE and TIMESTAMP types that reject invalid dates, unlike SQLite's rollover.

**Follow-ups:**
- *Which convention would you pick?* ISO text for readability and portability, or Unix integers if you need compact storage and arithmetic; say which zone it is in.
- *Can I index ISO text and use range scans?* Yes, a plain index on the column works for half-open ranges (Part 11 shows plans).
- *How do you fix a column of `DD/MM/YYYY`?* Rewrite it once: `substr(d,7,4)||'-'||substr(d,4,2)||'-'||substr(d,1,2)` in SQL (run in the code block and it matched the ISO table) or `pd.to_datetime(format='%d/%m/%Y')` in pandas, then store ISO.

**Common mistakes:**
- Sorting or filtering `DD/MM/YYYY` or `MM/DD/YYYY` text and trusting the order.
- Assuming `date()` returns NULL for a day that does not exist (it rolls over).
- `datetime(unix_seconds)` without `'unixepoch'`.
- Letting `to_datetime` guess day versus month on ambiguous strings.

### Q2 ⭐⭐⭐ 🟢 Truncate to day, week, month, quarter and year: orders(order_id, order_ts, amount) with ISO text timestamps. In SQLite return the month bucket two ways, strftime('%Y-%m', order_ts) (text) and date(order_ts, 'start of month') (a date), then a quarter bucket (SQLite has no quarter code, so derive it from the month number) and a year bucket. Give the DATE_TRUNC, EXTRACT and DATE_FORMAT equivalents in PostgreSQL, MySQL, BigQuery and Snowflake as hedged text (not executed), and the pandas versions: dt.to_period('M'), dt.to_period('Q'), dt.to_period('Y'), dt.normalize(), and why dt.floor('MS') is not allowed for calendar months.
**Asked at:** SQLite date and time functions documentation (lang_datefunc, opened), vendor documentation and not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Truncating means mapping each timestamp to a bucket label: `date(ts)` for the day, `strftime('%Y-%m', ts)` or `date(ts,'start of month')` for the month, `(month + 2) / 3` for the quarter and `strftime('%Y', ts)` for the year; pandas does the same with `dt.normalize()` and `dt.to_period('M' / 'Q' / 'Y')`.

**Schema and sample data:** six orders chosen to sit on bucket edges (the last second of 2023, the last evening of March, the first instant of April). Convention: naive timestamps, no time zone, read as UTC.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2023-12-31 23:59:59',100),(2,'2024-01-15 10:00:00',200),(3,'2024-03-31 23:30:00',300),
 (4,'2024-04-01 00:00:00',400),(5,'2024-06-30 12:00:00',500),(6,'2024-11-05 09:15:00',600);
```

**SQL answer:** `SQL_MAIN` returns every bucket per order; `SQL_QTR` sums revenue per quarter. The month is shown as text (`'2024-03'`) and as a date (`'2024-03-01'`); SQLite has no quarter code, so the quarter comes from integer division of the month number.

```sql
SELECT order_id,
       date(order_ts)                                   AS day_bucket,
       strftime('%Y-%m', order_ts)                      AS month_text,
       date(order_ts, 'start of month')                 AS month_date,
       strftime('%Y', order_ts) || 'Q' || ((CAST(strftime('%m', order_ts) AS INTEGER) + 2) / 3) AS quarter,
       strftime('%Y', order_ts)                         AS year_text
FROM orders
ORDER BY order_id
```
```sql
SELECT strftime('%Y', order_ts) || 'Q' || ((CAST(strftime('%m', order_ts) AS INTEGER) + 2) / 3) AS quarter,
       SUM(amount) AS revenue
FROM orders GROUP BY 1 ORDER BY 1
```

**pandas answer:** `to_period` gives calendar buckets as `Period` values (`astype(str)` for labels); `normalize()` keeps a timestamp but sets the time to midnight.
```py
ts = pd.to_datetime(orders["order_ts"])
pd_df = pd.DataFrame({
    "order_id": orders["order_id"],
    "day_bucket": ts.dt.normalize().dt.strftime("%Y-%m-%d"),
    "month_text": ts.dt.to_period("M").astype(str),
    "month_date": ts.dt.to_period("M").dt.start_time.dt.strftime("%Y-%m-%d"),
    "quarter": ts.dt.to_period("Q").astype(str),
    "year_text": ts.dt.to_period("Y").astype(str),
})
```

**Example:** - Order 1, `2023-12-31 23:59:59`: day `2023-12-31`, month `2023-12`, quarter `2023Q4` (month 12, `(12+2)/3 = 4`). One second later it would be a new month, quarter and year.
- Order 3, `2024-03-31 23:30:00`: month 3, `(3+2)/3 = 1`, so `2024Q1`. Order 4, `2024-04-01 00:00:00`: month 4, `(4+2)/3 = 2`, `2024Q2`.
- Quarter revenue: 2023Q4 = 100, 2024Q1 = 200 + 300 = 500, 2024Q2 = 400 + 500 = 900, 2024Q4 = 600. 2024Q3 has no orders and no row (the spine pattern is Part 6 Q6).

**Code:** run with `python3 -I`.
```python
# Q2: truncate to day / month / quarter / year in SQLite and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2023-12-31 23:59:59',100),(2,'2024-01-15 10:00:00',200),(3,'2024-03-31 23:30:00',300),
 (4,'2024-04-01 00:00:00',400),(5,'2024-06-30 12:00:00',500),(6,'2024-11-05 09:15:00',600);
"""
SQL_MAIN = """
SELECT order_id,
       date(order_ts)                                   AS day_bucket,
       strftime('%Y-%m', order_ts)                      AS month_text,
       date(order_ts, 'start of month')                 AS month_date,
       strftime('%Y', order_ts) || 'Q' || ((CAST(strftime('%m', order_ts) AS INTEGER) + 2) / 3) AS quarter,
       strftime('%Y', order_ts)                         AS year_text
FROM orders
ORDER BY order_id
"""
SQL_QTR = """
SELECT strftime('%Y', order_ts) || 'Q' || ((CAST(strftime('%m', order_ts) AS INTEGER) + 2) / 3) AS quarter,
       SUM(amount) AS revenue
FROM orders GROUP BY 1 ORDER BY 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print(con.execute(SQL_QTR).fetchall())

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
ts = pd.to_datetime(orders["order_ts"])
pd_df = pd.DataFrame({
    "order_id": orders["order_id"],
    "day_bucket": ts.dt.normalize().dt.strftime("%Y-%m-%d"),
    "month_text": ts.dt.to_period("M").astype(str),
    "month_date": ts.dt.to_period("M").dt.start_time.dt.strftime("%Y-%m-%d"),
    "quarter": ts.dt.to_period("Q").astype(str),
    "year_text": ts.dt.to_period("Y").astype(str),
})
# pd:end
# compared in order_id order
assert pd_df.equals(sql_df), (pd_df, sql_df)
print("pandas == SQL on", len(pd_df), "rows")
pd_q = orders.assign(q=ts.dt.to_period("Q").astype(str)).groupby("q")["amount"].sum()
assert pd_q.to_dict() == dict(con.execute(SQL_QTR).fetchall())
print(pd_q.to_dict())

print("period dtype:", ts.dt.to_period("M").dtype, "| normalize dtype:", ts.dt.normalize().dtype)
for freq in ["MS", "ME", "QS", "YS", "D"]:
    try:
        ts.dt.floor(freq)
        print("dt.floor(%r): ok" % freq)
    except Exception as e:
        print("dt.floor(%r): %s: %s" % (freq, type(e).__name__, e))
print("month start as Timestamp:", ts.dt.to_period("M").dt.to_timestamp().dt.strftime("%Y-%m-%d").tolist())
print("asserts passed")
```

**Output (my run):**
```text
 order_id day_bucket month_text month_date quarter year_text
        1 2023-12-31    2023-12 2023-12-01  2023Q4      2023
        2 2024-01-15    2024-01 2024-01-01  2024Q1      2024
        3 2024-03-31    2024-03 2024-03-01  2024Q1      2024
        4 2024-04-01    2024-04 2024-04-01  2024Q2      2024
        5 2024-06-30    2024-06 2024-06-01  2024Q2      2024
        6 2024-11-05    2024-11 2024-11-01  2024Q4      2024
[('2023Q4', 100), ('2024Q1', 500), ('2024Q2', 900), ('2024Q4', 600)]
pandas == SQL on 6 rows
{'2023Q4': 100, '2024Q1': 500, '2024Q2': 900, '2024Q4': 600}
period dtype: period[M] | normalize dtype: datetime64[us]
dt.floor('MS'): ValueError: <MonthBegin> is a non-fixed frequency
dt.floor('ME'): ValueError: <MonthEnd> is a non-fixed frequency
dt.floor('QS'): ValueError: <QuarterBegin: startingMonth=1> is a non-fixed frequency
dt.floor('YS'): ValueError: <YearBegin: month=1> is a non-fixed frequency
dt.floor('D'): ok
month start as Timestamp: ['2023-12-01', '2024-01-01', '2024-03-01', '2024-04-01', '2024-06-01', '2024-11-01']
asserts passed
```

**Edge cases:**
- Integer division: SQLite divides integers with truncation, so `(m + 2) / 3` is right; `m / 3` would put January in quarter 0. `strftime` returns text, hence the `CAST(... AS INTEGER)`.
- `strftime('%Y-%m')` is text, not a date: you cannot add months to it. `date(ts,'start of month')` is a real date and keeps working with other modifiers.
- Empty buckets are absent from `GROUP BY` output (no 2024Q3 row) and from `groupby` on a `Period` column.
- `dt.floor('MS')` fails on purpose: `ValueError: <MonthBegin> is a non-fixed frequency` (same message shape for `'ME'`, `'QS'` and `'YS'`; `'D'` works). `floor` only accepts fixed-length steps (day, hour, minute), and a month is 28 to 31 days. Use `to_period('M')`, `resample('MS')`, or `to_period('M').dt.to_timestamp()` for a month-start Timestamp.
- NULL timestamps give NULL buckets in SQL and `NaT` in pandas.

**Then explain:**
- Choose the bucket type by use: text labels for display and joins to other text labels, a real date when you will do date arithmetic, an integer such as `year*100 + month` for compact keys.
- Quarters here are calendar quarters (Jan to Mar = Q1). Fiscal quarters (April to March) are Part 6 Q25.
- `dt.normalize()` returns midnight of the same day and keeps `datetime64`; `to_period` changes the dtype to `period[M]`, which prints as `2024-03` and sorts correctly.
- Other engines, written from memory and not executed here. PostgreSQL: `DATE_TRUNC('month', ts)`, `EXTRACT(QUARTER FROM ts)`, `DATE_TRUNC('quarter', ts)`. MySQL has no `DATE_TRUNC`; people use `DATE_FORMAT(ts, '%Y-%m-01')` and `QUARTER(ts)`. BigQuery: `DATE_TRUNC(DATE(ts), MONTH)` or `TIMESTAMP_TRUNC(ts, MONTH)` and `EXTRACT(QUARTER FROM ts)`. Snowflake: `DATE_TRUNC('month', ts)` and `QUARTER(ts)`. Check the exact signatures in each manual.

**Follow-ups:**
- *Why is the month text safe to group on?* `YYYY-MM` is fixed width, so it sorts correctly; never use `%m` alone across years.
- *How do you get week and fiscal buckets?* Week: Part 6 Q5. Fiscal: Part 6 Q25.
- *Which would you use for a join to a calendar table?* The date form (`'2024-03-01'`), so keys match exactly.

**Common mistakes:**
- Grouping on `strftime('%m')` only, which merges March of different years.
- `month / 3` for the quarter, or forgetting the `CAST` and getting text arithmetic surprises.
- Calling `dt.floor('MS')` and expecting a month start.
- Mixing a `Period` column with a `Timestamp` column in a merge (they never compare equal; see Q29 in this part).

### Q3 ⭐⭐⭐ 🟢 Extracting parts and counting days between dates: orders(order_id, order_ts). Return year, month, day of month, day of week and day of year with strftime, and the days between two dates with julianday(b) - julianday(a) (a float) versus an integer count. Explain that strftime('%w') has Sunday = 0 while pandas dt.dayofweek has Monday = 0, that pandas (b - a).dt.days truncates while julianday gives a float (so a timestamp pair 36 hours apart is 1.5, not 1), and what rounding or date() wrapping you use to get whole calendar days.
**Asked at:** SQLite date and time functions documentation (lang_datefunc, opened), vendor documentation and not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `strftime` gives each part (`%Y`, `%m`, `%d`, `%w`, `%j`), and `julianday(b) - julianday(a)` gives elapsed days as a float, so 36 hours is 1.5; whole calendar days come from wrapping both sides in `date()` first, and whole elapsed days from `CAST` (truncate toward zero) or `ROUND`.

**Schema and sample data:** five orders with a delivery timestamp: a pair 36 hours apart, a 2-hour pair that crosses midnight, a same-day pair, a pair across New Year (day 366), and a row where delivery is before the order. The question names only `order_ts`; I added `delivered_ts` so there is a second timestamp to subtract. Convention: naive timestamps (UTC), `%w` Sunday-first.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, delivered_ts TEXT);
INSERT INTO orders VALUES
 (1,'2024-03-04 00:00:00','2024-03-05 12:00:00'),   -- Monday, 36 hours later
 (2,'2024-03-04 23:00:00','2024-03-05 01:00:00'),   -- 2 hours, but across midnight
 (3,'2024-03-10 09:00:00','2024-03-10 18:00:00'),   -- Sunday, same calendar day
 (4,'2024-12-31 08:00:00','2025-01-02 08:00:00'),   -- day 366, crosses the year
 (5,'2024-03-06 12:00:00','2024-03-06 00:00:00');   -- delivered BEFORE ordered: -0.5 days
```

**SQL answer:** `SQL_MAIN` returns year, month, day of month, day of week (Sunday = 0 and Monday = 0 forms), day of year, the float difference, the truncated integer, and the calendar-day count.

```sql
SELECT order_id,
       CAST(strftime('%Y', order_ts) AS INTEGER) AS yr,
       CAST(strftime('%m', order_ts) AS INTEGER) AS mon,
       CAST(strftime('%d', order_ts) AS INTEGER) AS dom,
       CAST(strftime('%w', order_ts) AS INTEGER) AS dow_sun0,
       (CAST(strftime('%w', order_ts) AS INTEGER) + 6) % 7 AS dow_mon0,
       CAST(strftime('%j', order_ts) AS INTEGER) AS doy,
       ROUND(julianday(delivered_ts) - julianday(order_ts), 4)         AS days_float,
       CAST(julianday(delivered_ts) - julianday(order_ts) AS INTEGER)  AS days_trunc,
       CAST(julianday(date(delivered_ts)) - julianday(date(order_ts)) AS INTEGER) AS cal_days
FROM orders ORDER BY order_id
```

**pandas answer:** `dt` accessors for the parts; `(d - o)` is a `Timedelta`, so use `total_seconds() / 86400` for the float and `.dt.days` for whole days; `dt.dayofweek` is Monday = 0, so convert when you compare with `%w`.
```py
o = pd.to_datetime(orders["order_ts"])
d = pd.to_datetime(orders["delivered_ts"])
delta = d - o
pd_df = pd.DataFrame({
    "order_id": orders["order_id"],
    "yr": o.dt.year, "mon": o.dt.month, "dom": o.dt.day,
    "dow_sun0": (o.dt.dayofweek + 1) % 7,
    "dow_mon0": o.dt.dayofweek,
    "doy": o.dt.dayofyear,
    "days_float": (delta.dt.total_seconds() / 86400).round(4),
    "days_trunc": np.trunc(delta.dt.total_seconds() / 86400).astype(int),
    "cal_days": (d.dt.normalize() - o.dt.normalize()).dt.days,
})
```

**Example:** - Order 1: Monday 2024-03-04 00:00 to Tuesday 2024-03-05 12:00. `%w` = 1, pandas `dayofweek` = 0, day of year 64. `julianday` difference = 1.5; `CAST` gives 1; calendar days = 1.
- Order 2: 23:00 to 01:00 next day. Elapsed 2 hours = 0.0833 days, `CAST` gives 0, but the calendar-day count is 1 because the dates differ.
- Order 3: Sunday 2024-03-10: `%w` = 0 but `dayofweek` = 6. Same calendar day, 0.375 days (9 hours).
- Order 4: 2024-12-31 is day 366 of a leap year, and 2 days later at the same hour.
- Order 5: delivery 12 hours before the order: float -0.5, `CAST` gives 0, calendar days 0.

**Code:** run with `python3 -I`.
```python
# Q3: extracting date parts and counting days between two timestamps
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, delivered_ts TEXT);
INSERT INTO orders VALUES
 (1,'2024-03-04 00:00:00','2024-03-05 12:00:00'),   -- Monday, 36 hours later
 (2,'2024-03-04 23:00:00','2024-03-05 01:00:00'),   -- 2 hours, but across midnight
 (3,'2024-03-10 09:00:00','2024-03-10 18:00:00'),   -- Sunday, same calendar day
 (4,'2024-12-31 08:00:00','2025-01-02 08:00:00'),   -- day 366, crosses the year
 (5,'2024-03-06 12:00:00','2024-03-06 00:00:00');   -- delivered BEFORE ordered: -0.5 days
"""
SQL_MAIN = """
SELECT order_id,
       CAST(strftime('%Y', order_ts) AS INTEGER) AS yr,
       CAST(strftime('%m', order_ts) AS INTEGER) AS mon,
       CAST(strftime('%d', order_ts) AS INTEGER) AS dom,
       CAST(strftime('%w', order_ts) AS INTEGER) AS dow_sun0,
       (CAST(strftime('%w', order_ts) AS INTEGER) + 6) % 7 AS dow_mon0,
       CAST(strftime('%j', order_ts) AS INTEGER) AS doy,
       ROUND(julianday(delivered_ts) - julianday(order_ts), 4)         AS days_float,
       CAST(julianday(delivered_ts) - julianday(order_ts) AS INTEGER)  AS days_trunc,
       CAST(julianday(date(delivered_ts)) - julianday(date(order_ts)) AS INTEGER) AS cal_days
FROM orders ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = pd.to_datetime(orders["order_ts"])
d = pd.to_datetime(orders["delivered_ts"])
delta = d - o
pd_df = pd.DataFrame({
    "order_id": orders["order_id"],
    "yr": o.dt.year, "mon": o.dt.month, "dom": o.dt.day,
    "dow_sun0": (o.dt.dayofweek + 1) % 7,
    "dow_mon0": o.dt.dayofweek,
    "doy": o.dt.dayofyear,
    "days_float": (delta.dt.total_seconds() / 86400).round(4),
    "days_trunc": np.trunc(delta.dt.total_seconds() / 86400).astype(int),
    "cal_days": (d.dt.normalize() - o.dt.normalize()).dt.days,
})
# pd:end
# compared in order_id order; column dtypes may differ, values must match
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas == SQL")
print("Timedelta.dt.days   :", delta.dt.days.tolist(), "(floors: row 5 is -1, SQL CAST gives", int(sql_df.loc[4, "days_trunc"]), ")")
print("36h pair, dt.days   :", int(delta.dt.days[0]), "| julianday diff:", float(sql_df.loc[0, "days_float"]))
print("round(), not CAST   :", con.execute("SELECT ROUND(julianday('2024-03-05 12:00:00') - julianday('2024-03-04 00:00:00'))").fetchone())
print("Sunday, strftime %w :", con.execute("SELECT strftime('%w','2024-03-10'), strftime('%u','2024-03-10')").fetchone(),
      "| pandas dayofweek:", int(pd.Timestamp('2024-03-10').dayofweek))
print("asserts passed")
```

**Output (my run):**
```text
 order_id   yr  mon  dom  dow_sun0  dow_mon0  doy  days_float  days_trunc  cal_days
        1 2024    3    4         1         0   64      1.5000           1         1
        2 2024    3    4         1         0   64      0.0833           0         1
        3 2024    3   10         0         6   70      0.3750           0         0
        4 2024   12   31         2         1  366      2.0000           2         2
        5 2024    3    6         3         2   66     -0.5000           0         0
pandas == SQL
Timedelta.dt.days   : [1, 0, 0, 2, -1] (floors: row 5 is -1, SQL CAST gives 0 )
36h pair, dt.days   : 1 | julianday diff: 1.5
round(), not CAST   : (2.0,)
Sunday, strftime %w : ('0', '7') | pandas dayofweek: 6
asserts passed
```

**Edge cases:**
- Float versus integer: `julianday` differences are REAL; `ROUND(x, 4)` was used to make the output comparable, and `ROUND(1.5)` gave 2.0 in SQLite. Floating error is tiny but do not test `= 1` without rounding.
- Truncation is not the same in the two tools: for -0.5 days, `CAST(... AS INTEGER)` returned 0 (toward zero) but pandas `.dt.days` returned -1 (it floors). I compared against `np.trunc` in the assert and printed `.dt.days` separately. For non-negative gaps they agree: the 36-hour pair is `1` in both.
- Calendar days and elapsed days answer different questions; state which one the business wants (SLA hours versus 'delivered the next day').
- NULL in either timestamp gives NULL (`NaT` minus anything gives `NaT`).
- `%w` is Sunday = 0 and `%u` is Monday = 1 to Sunday = 7 in SQLite (a Sunday gave `0` and `7`); pandas `dayofweek` is Monday = 0 to Sunday = 6 (Sunday gave `6`).

**Then explain:**
- Parts: `strftime('%Y')`, `'%m'`, `'%d'`, `'%w'`, `'%j'` return text; cast to integer to do arithmetic or compare numerically.
- Float days come directly from Julian days; multiply by 24 for hours or 86400 for seconds.
- Whole calendar days: `julianday(date(b)) - julianday(date(a))`; it ignores clock times, so 23:00 to 01:00 is 1.
- Whole elapsed days: `CAST(x AS INTEGER)` truncates; `ROUND` rounds half away from zero. Pick one and write it down.
- In pandas, `.dt.days` is the whole-day component of a Timedelta and discards the remainder; the float is `total_seconds() / 86400`.
- Other engines (not executed here): `DATEDIFF` argument order and unit semantics differ by engine; see Part 6 Q36.

**Follow-ups:**
- *How many full days old is an order as of a fixed date?* `julianday('2024-12-31') - julianday(date(order_ts))`; use an 'as of' date, not now (Q19).
- *How do you convert Sunday-first to Monday-first?* `(w + 6) % 7`, which I used above.
- *Hours between two timestamps?* `(julianday(b) - julianday(a)) * 24`.

**Common mistakes:**
- Reading 1.5 as '1 day' and losing 12 hours (or the reverse, thinking 2 hours is 0 days when the dates differ).
- Comparing SQLite weekdays (Sunday = 0) with pandas weekdays (Monday = 0) without converting.
- Using `.dt.days` on negative intervals and expecting truncation toward zero.
- Subtracting `strftime('%j')` values across a year boundary.

### Q4 ⭐⭐⭐ 🟢 The BETWEEN trap with timestamps: orders(order_id, order_ts, amount) where order_ts is 'YYYY-MM-DD HH:MM:SS'. Show that WHERE order_ts BETWEEN '2024-01-01' AND '2024-01-31' silently drops every order after midnight on 31 January, and that BETWEEN '2024-01-01' AND '2024-01-31 23:59:59' still misses fractional seconds. Rewrite with the half-open range order_ts >= '2024-01-01' AND order_ts < '2024-02-01', and show the same bug in pandas (df.loc['2024-01-01':'2024-01-31'] on a DatetimeIndex is inclusive of the whole last day by partial-string indexing, while a boolean mask with <= Timestamp is not). Say why half-open ranges compose with adjacent months.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** With a timestamp column, `BETWEEN '2024-01-01' AND '2024-01-31'` stops at midnight at the start of 31 January because the stored text is longer than the bound; use a half-open range, `order_ts >= '2024-01-01' AND order_ts < '2024-02-01'`, which catches every instant and chains cleanly onto the next month.

**Schema and sample data:** nine orders around the January boundary, including one at exactly midnight on 31 January, one at 23:59:59 and one at 23:59:59.500. Convention: naive timestamps, read as UTC.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2023-12-31 23:59:59',10),(2,'2024-01-01 00:00:00',20),(3,'2024-01-15 09:00:00',30),
 (4,'2024-01-31 00:00:00',40),(5,'2024-01-31 12:00:00',50),(6,'2024-01-31 23:59:59',60),
 (7,'2024-01-31 23:59:59.500',70),(8,'2024-02-01 00:00:00',80),(9,'2024-02-10 10:00:00',90);
```

**SQL answer:** the right answer is the half-open range (`SQL_MAIN`). The wrong versions are `SQL_B1` (bound is the bare date), `SQL_B2` (bound `23:59:59`), and a pair of adjacent-month `BETWEEN` queries (`SQL_JAN_B`, `SQL_FEB_B`) that double count.

```sql
SELECT COUNT(*) AS n, SUM(amount) AS revenue
FROM orders
WHERE order_ts >= '2024-01-01' AND order_ts < '2024-02-01'
```
```sql
SELECT order_id FROM orders WHERE order_ts BETWEEN '2024-01-01' AND '2024-01-31' ORDER BY 1
```
```sql
SELECT order_id FROM orders WHERE order_ts BETWEEN '2024-01-01' AND '2024-01-31 23:59:59' ORDER BY 1
```
```sql
SELECT order_id FROM orders WHERE order_ts BETWEEN '2024-01-01 00:00:00' AND '2024-02-01 00:00:00' ORDER BY 1
```
```sql
SELECT order_id FROM orders WHERE order_ts BETWEEN '2024-02-01' AND '2024-02-29' ORDER BY 1
```

**pandas answer:** build a boolean mask with a half-open range; the slice `df.loc['2024-01-01':'2024-01-31']` on a `DatetimeIndex` is a different, inclusive-of-the-whole-last-day rule, while a mask with `<= Timestamp('2024-01-31')` repeats the SQL bug.
```py
df = orders.assign(order_ts=pd.to_datetime(orders["order_ts"], format="ISO8601")).set_index("order_ts")
jan = df.loc[(df.index >= "2024-01-01") & (df.index < "2024-02-01")]
pd_df = pd.DataFrame({"n": [len(jan)], "revenue": [int(jan["amount"].sum())]})
```

**Example:** January belongs to ids 2 to 7 (20 + 30 + 40 + 50 + 60 + 70 = 270, six rows).
- `BETWEEN '2024-01-01' AND '2024-01-31'` returned ids 2 and 3. Text comparison: `'2024-01-31 00:00:00'` is longer than `'2024-01-31'` with the same prefix, so it is greater and is cut off. Ids 4 to 7 vanish, even the one at exactly midnight.
- `BETWEEN '2024-01-01' AND '2024-01-31 23:59:59'` returned ids 2 to 6; id 7 (`23:59:59.500`) is greater than the bound and is dropped.
- Half-open range: ids 2 to 7, count 6, revenue 270.
- Adjacent months: `BETWEEN '2024-01-01 00:00:00' AND '2024-02-01 00:00:00'` returned ids 2 to 8, so id 8 (`2024-02-01 00:00:00`) is counted in January and again in the February query. The half-open pair (`< '2024-02-01'`, then `>= '2024-02-01'`) puts it only in February.

**Code:** run with `python3 -I`.
```python
# Q4: the BETWEEN trap with timestamps; half-open ranges; pandas partial-string indexing
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2023-12-31 23:59:59',10),(2,'2024-01-01 00:00:00',20),(3,'2024-01-15 09:00:00',30),
 (4,'2024-01-31 00:00:00',40),(5,'2024-01-31 12:00:00',50),(6,'2024-01-31 23:59:59',60),
 (7,'2024-01-31 23:59:59.500',70),(8,'2024-02-01 00:00:00',80),(9,'2024-02-10 10:00:00',90);
"""
SQL_MAIN = """
SELECT COUNT(*) AS n, SUM(amount) AS revenue
FROM orders
WHERE order_ts >= '2024-01-01' AND order_ts < '2024-02-01'
"""
SQL_B1 = "SELECT order_id FROM orders WHERE order_ts BETWEEN '2024-01-01' AND '2024-01-31' ORDER BY 1"
SQL_B2 = "SELECT order_id FROM orders WHERE order_ts BETWEEN '2024-01-01' AND '2024-01-31 23:59:59' ORDER BY 1"
SQL_JAN_B = "SELECT order_id FROM orders WHERE order_ts BETWEEN '2024-01-01 00:00:00' AND '2024-02-01 00:00:00' ORDER BY 1"
SQL_FEB_B = "SELECT order_id FROM orders WHERE order_ts BETWEEN '2024-02-01' AND '2024-02-29' ORDER BY 1"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
ids = lambda s: [r[0] for r in con.execute(s)]
print("half-open Jan        :", sql_df.values.tolist(), "ids", ids("SELECT order_id FROM orders WHERE order_ts >= '2024-01-01' AND order_ts < '2024-02-01'"))
print("BETWEEN ..-01-31     :", ids(SQL_B1))
print("BETWEEN ..-01-31 23:59:59:", ids(SQL_B2))
print("Jan BETWEEN ..-01 00:00:00 AND ..-02-01 00:00:00:", ids(SQL_JAN_B), "| Feb BETWEEN ..-02-01 AND ..-02-29:", ids(SQL_FEB_B), "-> id 8 counted in both")
print("half-open Feb        :", ids("SELECT order_id FROM orders WHERE order_ts >= '2024-02-01' AND order_ts < '2024-03-01'"))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
df = orders.assign(order_ts=pd.to_datetime(orders["order_ts"], format="ISO8601")).set_index("order_ts")
jan = df.loc[(df.index >= "2024-01-01") & (df.index < "2024-02-01")]
pd_df = pd.DataFrame({"n": [len(jan)], "revenue": [int(jan["amount"].sum())]})
# pd:end
# single-row frames, compared directly
assert pd_df.values.tolist() == sql_df.values.tolist()
sliced = df.loc["2024-01-01":"2024-01-31"]
masked = df[(df.index >= pd.Timestamp("2024-01-01")) & (df.index <= pd.Timestamp("2024-01-31"))]
print("pandas half-open     :", pd_df.values.tolist())
print("loc['2024-01-01':'2024-01-31']        ids", sliced["order_id"].tolist(), "(whole last day included)")
print("mask <= Timestamp('2024-01-31')       ids", masked["order_id"].tolist(), "(same bug as BETWEEN)")
assert sliced["order_id"].tolist() == [2, 3, 4, 5, 6, 7]
assert masked["order_id"].tolist() == [2, 3, 4]
print("asserts passed")
```

**Output (my run):**
```text
half-open Jan        : [[6, 270]] ids [2, 3, 4, 5, 6, 7]
BETWEEN ..-01-31     : [2, 3]
BETWEEN ..-01-31 23:59:59: [2, 3, 4, 5, 6]
Jan BETWEEN ..-01 00:00:00 AND ..-02-01 00:00:00: [2, 3, 4, 5, 6, 7, 8] | Feb BETWEEN ..-02-01 AND ..-02-29: [8, 9] -> id 8 counted in both
half-open Feb        : [8, 9]
pandas half-open     : [[6, 270]]
loc['2024-01-01':'2024-01-31']        ids [2, 3, 4, 5, 6, 7] (whole last day included)
mask <= Timestamp('2024-01-31')       ids [2, 3, 4] (same bug as BETWEEN)
asserts passed
```

**Edge cases:**
- Fractional seconds: no `BETWEEN` upper bound written as a time is safe; `23:59:59.999` still misses `23:59:59.9995`. A `< next_day` bound has no such gap.
- Date-only columns behave differently: if the column holds `'2024-01-31'` with no time, `BETWEEN` to `'2024-01-31'` works. The trap is specific to timestamps; do not rely on that column staying date-only.
- Separator: a column mixing `' '` and `'T'` between date and time sorts `'T'` after `' '`, so range filters with a time in the bound can mis-sort (string-order reasoning, not run here).
- pandas partial string indexing: `df.loc['2024-01-01':'2024-01-31']` returned ids 2 to 7, including the `.500` row, because the string `'2024-01-31'` is treated as the whole day. The mask `index <= Timestamp('2024-01-31')` returned ids 2 to 4 (the Timestamp is midnight). I used a sorted index; I did not test an unsorted one.
- parsing: a column with and without fractional seconds raised `ValueError` under the default `to_datetime` inference in pandas 3.0.5, so I passed `format='ISO8601'`.

**Then explain:**
- A half-open range `[start, next_start)` includes the start instant and excludes the next one, so every instant belongs to exactly one bucket.
- Adjacent buckets compose: the end of one is literally the start of the next, no gap and no overlap, so month totals add up to the year total.
- The end bound is computed, not typed: `date('2024-01-01', '+1 month')` or a parameter, which avoids hard-coding 28, 29, 30 or 31.
- Sargability: both sides are plain comparisons on the bare column, so an index on `order_ts` can be used (Part 6 Q40).
- Other engines (not executed here): the same half-open rule applies in PostgreSQL, MySQL, BigQuery and Snowflake with real timestamp types; `BETWEEN` is inclusive on both ends everywhere.

**Follow-ups:**
- *And for dates in a `TIMESTAMP` that carry a time zone?* Decide the reporting zone first; the bounds must be in that zone (Q16).
- *Why not `<= '2024-01-31 23:59:59'`?* Misses fractional seconds and is easy to get wrong by one.
- *How do you check you did not drop rows?* Reconcile: sum of buckets equals the overall total (Q45 drill).

**Common mistakes:**
- Using `BETWEEN` on timestamps with a date-only upper bound.
- Writing `23:59:59` and thinking it is complete.
- Using `<= '2024-02-01'` as the end bound and double counting midnight on the first.
- Assuming a pandas slice string and a Timestamp mask behave the same.

### Q5 ⭐⭐⭐ 🟡 Weekly buckets and the week-start trap: orders(order_id, order_ts, amount). Group revenue by week with weeks starting Monday in SQLite using date(order_ts, 'weekday 0', '-6 days') and with weeks starting Sunday, and show a week that spans a month boundary and a year boundary (late December into early January). Compare SQLite strftime('%W') (week 1 begins on the first Monday, days before it are week 00) with %U, and report what SQLite 3.45 does with the ISO codes %V and %G (check the installed version; the SQLite docs list them in newer versions). In pandas show resample('W') (default W-SUN, labelled by the Sunday that ends the week), resample('W-MON', closed='left', label='left') and dt.to_period('W') (Monday to Sunday), and the year-boundary difference of dt.isocalendar().
**Asked at:** SQLite date and time functions documentation (lang_datefunc, opened), vendor documentation and not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** SQLite has no week-truncation function, so a Monday-start week is `date(ts, 'weekday 0', '-6 days')` (jump forward to the Sunday, step back six days) and a Sunday-start week is `date(ts, '-6 days', 'weekday 0')`; `strftime('%W')` is a Monday-based week number that is 0 before the first Monday, and in SQLite 3.45.1 `%U`, `%V` and `%G` return NULL, so ISO weeks need emulation.

**Schema and sample data:** eleven orders from 23 December 2024 to 2 February 2025 with amounts 1, 2, 4, 8 and so on, so any weekly total tells you exactly which orders it holds. Convention: weeks start Monday unless stated; naive timestamps, read as UTC.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-12-23 10:00:00',1),(2,'2024-12-25 12:00:00',2),(3,'2024-12-29 23:00:00',4),   -- Sunday
 (4,'2024-12-30 08:00:00',8),(5,'2024-12-31 20:00:00',16),                               -- Mon, Tue
 (6,'2025-01-01 09:00:00',32),(7,'2025-01-04 15:00:00',64),(8,'2025-01-05 22:00:00',128),-- Wed, Sat, Sun
 (9,'2025-01-06 07:00:00',256),                                                          -- Monday
 (10,'2025-01-31 18:00:00',512),(11,'2025-02-02 11:00:00',1024);                         -- Fri, Sun (month boundary)
```

**SQL answer:** `SQL_MAIN` is the Monday-start weekly revenue; `SQL_SUN` is the Sunday-start version; `SQL_CODES` prints the week codes per order, plus the ISO-year emulation `date(d,'-3 days','weekday 4')` (the Thursday of the ISO week decides the ISO year) and an ISO week number built from that Thursday.

```sql
SELECT date(order_ts, 'weekday 0', '-6 days') AS week_start_mon, SUM(amount) AS revenue
FROM orders
GROUP BY 1
ORDER BY 1
```
```sql
SELECT date(order_ts, '-6 days', 'weekday 0') AS week_start_sun, SUM(amount) AS revenue
FROM orders GROUP BY 1 ORDER BY 1
```
```sql
SELECT date(order_ts) AS d, strftime('%w', order_ts) AS w, strftime('%W', order_ts) AS W_mon,
       strftime('%U', order_ts) AS U_sun, strftime('%V', order_ts) AS V_iso, strftime('%G', order_ts) AS G_iso,
       strftime('%Y', date(order_ts, '-3 days', 'weekday 4')) AS iso_year_emul,
       CAST((CAST(strftime('%j', date(order_ts, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 AS INTEGER) + 1 AS iso_week_emul
FROM orders ORDER BY order_id
```

**pandas answer:** `dt.to_period('W')` is Monday to Sunday and `start_time` is the Monday; `resample('W-MON', closed='left', label='left')` reproduces the SQL Monday weeks (plus empty weeks); the default `resample('W')` is Sunday-ending and labelled by that Sunday; `dt.isocalendar()` gives the ISO year and week.
```py
pd_df = (orders.groupby(orders["order_ts"].dt.to_period("W").dt.start_time)["amount"].sum()
               .rename_axis("week_start_mon").reset_index(name="revenue"))
pd_df["week_start_mon"] = pd_df["week_start_mon"].dt.strftime("%Y-%m-%d")
```

**Example:** Monday weeks: 23 Dec to 29 Dec holds orders 1, 2, 3 (1 + 2 + 4 = 7); 30 Dec to 5 Jan holds 8 + 16 + 32 + 64 + 128 = 248 (this week spans the year boundary); 6 Jan to 12 Jan holds order 9 (256); 27 Jan to 2 Feb holds order 10 (31 Jan) and order 11 (Sunday 2 Feb) = 1536, a week that spans the month boundary.
- Sunday-start weeks put Sunday 29 Dec with the following week (3, 124, 384, 512, 1024), so the same orders produce different totals. Sunday-based labels are `2024-12-22`, `2024-12-29`, `2025-01-05`, `2025-01-26`, `2025-02-02`.
- `%W` for 30 Dec is `53`, for 31 Dec `53`, but for 1 Jan 2025 it is `00`: week 1 starts on the first Monday (6 Jan), and days before it are week 00. So one Monday-to-Sunday week is split across two `%W` labels and across two years if you also group by year.
- ISO emulation: 30 Dec 2024 minus 3 days is 27 Dec, next Thursday-or-same is 2 Jan 2025, so ISO year 2025, ISO week 1. pandas `isocalendar()` said year 2025, week 1 for 30 Dec through 5 Jan, matching the emulation.

**Code:** run with `python3 -I`.
```python
# Q5: weekly buckets, week-start conventions, %W/%U/%V/%G in SQLite 3.45, pandas W-SUN / W-MON / Period W
# Convention: weeks start MONDAY unless stated; timestamps are naive (no time zone, read as UTC).
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-12-23 10:00:00',1),(2,'2024-12-25 12:00:00',2),(3,'2024-12-29 23:00:00',4),   -- Sunday
 (4,'2024-12-30 08:00:00',8),(5,'2024-12-31 20:00:00',16),                               -- Mon, Tue
 (6,'2025-01-01 09:00:00',32),(7,'2025-01-04 15:00:00',64),(8,'2025-01-05 22:00:00',128),-- Wed, Sat, Sun
 (9,'2025-01-06 07:00:00',256),                                                          -- Monday
 (10,'2025-01-31 18:00:00',512),(11,'2025-02-02 11:00:00',1024);                         -- Fri, Sun (month boundary)
"""
SQL_MAIN = """
SELECT date(order_ts, 'weekday 0', '-6 days') AS week_start_mon, SUM(amount) AS revenue
FROM orders
GROUP BY 1
ORDER BY 1
"""
SQL_SUN = """
SELECT date(order_ts, '-6 days', 'weekday 0') AS week_start_sun, SUM(amount) AS revenue
FROM orders GROUP BY 1 ORDER BY 1
"""
SQL_CODES = """
SELECT date(order_ts) AS d, strftime('%w', order_ts) AS w, strftime('%W', order_ts) AS W_mon,
       strftime('%U', order_ts) AS U_sun, strftime('%V', order_ts) AS V_iso, strftime('%G', order_ts) AS G_iso,
       strftime('%Y', date(order_ts, '-3 days', 'weekday 4')) AS iso_year_emul,
       CAST((CAST(strftime('%j', date(order_ts, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 AS INTEGER) + 1 AS iso_week_emul
FROM orders ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print(pd.read_sql_query(SQL_SUN, con).to_string(index=False))
codes = pd.read_sql_query(SQL_CODES, con)
print(codes.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
orders["order_ts"] = pd.to_datetime(orders["order_ts"])
# pd:main
pd_df = (orders.groupby(orders["order_ts"].dt.to_period("W").dt.start_time)["amount"].sum()
               .rename_axis("week_start_mon").reset_index(name="revenue"))
pd_df["week_start_mon"] = pd_df["week_start_mon"].dt.strftime("%Y-%m-%d")
# pd:end
# compared in week_start order; empty weeks are absent on both sides
assert pd_df.values.tolist() == sql_df.values.tolist()
s = orders.set_index("order_ts")["amount"]
rs_mon = s.resample("W-MON", closed="left", label="left").sum()
rs_sun = s.resample("W").sum()
rs_mon_default = s.resample("W-MON").sum()
assert rs_mon[rs_mon > 0].rename_axis("week_start_mon").reset_index().assign(
    week_start_mon=lambda d: d["week_start_mon"].dt.strftime("%Y-%m-%d")).values.tolist() == sql_df.values.tolist()
print("resample('W-MON', closed='left', label='left') == SQL after dropping empty weeks")
print("resample('W') labels (Sunday that ENDS the week):", [(k.strftime("%m-%d"), int(v)) for k, v in rs_sun.items() if v > 0])
print("resample('W-MON') default (right/right, label = Monday ENDING the bin):", [(k.strftime("%m-%d"), int(v)) for k, v in rs_mon_default.items() if v > 0])
print("empty weeks in resample:", int((rs_mon == 0).sum()), "of", len(rs_mon))
sun = orders.groupby(orders["order_ts"].dt.to_period("W-SAT").dt.start_time)["amount"].sum()
assert sun.index.strftime("%Y-%m-%d").tolist() == pd.read_sql_query(SQL_SUN, con)["week_start_sun"].tolist()
print("Period('W-SAT') starts on Sunday: matches SQL Sunday weeks")
print("Period('W') of 2024-12-30:", orders["order_ts"].dt.to_period("W")[3])
iso = orders["order_ts"].dt.isocalendar()
assert iso["year"].astype(str).tolist() == codes["iso_year_emul"].tolist()
assert iso["week"].tolist() == codes["iso_week_emul"].tolist()
print("isocalendar year/week of 2024-12-30..2025-01-05:", iso.loc[3:7].values.tolist(), "== SQLite Thursday emulation")
print("asserts passed")
```

**Output (my run):**
```text
week_start_mon  revenue
    2024-12-23        7
    2024-12-30      248
    2025-01-06      256
    2025-01-27     1536
week_start_sun  revenue
    2024-12-22        3
    2024-12-29      124
    2025-01-05      384
    2025-01-26      512
    2025-02-02     1024
         d w W_mon U_sun V_iso G_iso iso_year_emul  iso_week_emul
2024-12-23 1    52  None  None  None          2024             52
2024-12-25 3    52  None  None  None          2024             52
2024-12-29 0    52  None  None  None          2024             52
2024-12-30 1    53  None  None  None          2025              1
2024-12-31 2    53  None  None  None          2025              1
2025-01-01 3    00  None  None  None          2025              1
2025-01-04 6    00  None  None  None          2025              1
2025-01-05 0    00  None  None  None          2025              1
2025-01-06 1    01  None  None  None          2025              2
2025-01-31 5    04  None  None  None          2025              5
2025-02-02 0    04  None  None  None          2025              5
resample('W-MON', closed='left', label='left') == SQL after dropping empty weeks
resample('W') labels (Sunday that ENDS the week): [('12-29', 7), ('01-05', 248), ('01-12', 256), ('02-02', 1536)]
resample('W-MON') default (right/right, label = Monday ENDING the bin): [('12-23', 1), ('12-30', 14), ('01-06', 496), ('02-03', 1536)]
empty weeks in resample: 2 of 6
Period('W-SAT') starts on Sunday: matches SQL Sunday weeks
Period('W') of 2024-12-30: 2024-12-30/2025-01-05
isocalendar year/week of 2024-12-30..2025-01-05: [[2025, 1, 1], [2025, 1, 2], [2025, 1, 3], [2025, 1, 6], [2025, 1, 7]] == SQLite Thursday emulation
asserts passed
```

**Edge cases:**
- SQLite 3.45.1: `strftime('%U')`, `%V` and `%G` returned NULL in my run (and `%W` worked). The SQLite documentation lists newer codes and modifiers as added in later versions; they are not available on this build. Do not assume; run it.
- Empty weeks: SQL `GROUP BY` omits them; pandas `resample` gives 6 weekly rows of which 2 were empty (sum 0) in this data; `groupby(to_period('W'))` omits them like SQL.
- `resample('W-MON')` with default arguments is right-closed and right-labelled (run result): the bin labelled 2024-12-23 held only order 1 (a Monday), and the bin labelled 2024-12-30 held orders 2, 3 and 4 (Wednesday 25 Dec to Monday 30 Dec) with sum 14, so each bin runs Tuesday to Monday and carries the label of its Monday. It is not the Monday-start week unless you pass `closed='left', label='left'`.
- `resample('W')` is the same as `W-SUN`: label is the Sunday that ends the week (`12-29: 7`, `01-05: 248`, `01-12: 256`, `02-02: 1536`). Labelling by the end of the week surprises people reading a chart.
- `%W` year splits and ISO year: calendar year (`strftime('%Y')`) and week number must not be combined; use the ISO year (Thursday rule) with the ISO week.
- NULL `order_ts` gives NULL week in SQL and `NaT` in pandas.

**Then explain:**
- State the week start before you write code: Monday (ISO, most of the world, pandas Period default) or Sunday (US convention, SQLite `%w` = 0 is Sunday).
- `'weekday 0'` means 'move forward to the next Sunday, or stay if already Sunday'. For Monday-start, subtract six days; a Sunday stays on its own week, which is correct for Monday-start.
- `%W` is Monday-based with week 00 before the first Monday; `%U` is its Sunday-based sibling (NULL here). Neither is the ISO week, where week 1 contains the first Thursday.
- ISO-year emulation: shift to the Thursday of the same ISO week (`date(d, '-3 days', 'weekday 4')`), take its year, and take the week number as `(day-of-year of that Thursday - 1) / 7 + 1`. I checked this against pandas `isocalendar()` on all eleven dates.
- Other engines (not executed here): PostgreSQL `DATE_TRUNC('week', ts)` is Monday-based; MySQL `WEEK(date, mode)` and `YEARWEEK` have several modes; BigQuery `DATE_TRUNC(d, WEEK)` is Sunday by default and `WEEK(MONDAY)` is Monday-based; Snowflake depends on the session parameter `WEEK_START`. Check each; I did not run them.

**Follow-ups:**
- *How do you compare 'same week last year'?* ISO week plus ISO year with care for 52 versus 53 week years (Part 6 Q43).
- *Week labels for a chart?* Label by the week start date, and say Monday.
- *A week that crosses a month?* Decide whether to split it (daily data) or assign it to its start date.

**Common mistakes:**
- Using `strftime('%W')` as the ISO week.
- Grouping on `strftime('%Y')` and week number together near 1 January.
- Reading the default `resample('W')` label as the week start.
- Forgetting that the Sunday needs `-6 days` (not `-7`) in the Monday-start formula.

### Q6 ⭐⭐⭐ 🟡 Monthly revenue with missing months: orders(order_id, order_ts, amount) where February 2024 has no orders. A plain GROUP BY month drops February. Build a date spine of months with a recursive CTE in SQLite (WITH RECURSIVE months(m) AS (SELECT '2024-01-01' UNION ALL SELECT date(m, '+1 month') FROM months WHERE m < '2024-04-01')), LEFT JOIN the aggregated orders and COALESCE to 0. Mention generate_series and calendar tables elsewhere as hedged text (not executed). Give pandas: resample('MS').sum() (empty months become 0) versus groupby on to_period('M') (missing month absent) and reindex with pd.date_range(freq='MS') to force the spine.
**Asked at:** search-result snippets of date-spine and churn guides (Galaxy cohort-churn glossary, a LinkedIn list of time-series SQL topics; not opened), guides and not candidate reports; analyst and data engineer screens
**Say this first (1 line):** A plain `GROUP BY` month cannot show a month that has no rows, so I build a spine of months with a recursive CTE, `LEFT JOIN` the aggregated revenue onto it and `COALESCE` to 0; in pandas `resample('MS').sum()` does this by itself, while `groupby(to_period('M'))` leaves the hole unless you reindex.

**Schema and sample data:** five orders: January has two, February has none, March one, April one at exactly midnight on 1 April, plus one in May that lies after the spine's end. Convention: naive timestamps, months are calendar months of the stored time (UTC).
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-01-10 09:00:00',100),(2,'2024-01-20 18:30:00',50),
 (3,'2024-03-05 12:00:00',70),(4,'2024-04-01 00:00:00',30),
 (5,'2024-05-02 10:00:00',999);   -- after the spine's last month
```

**SQL answer:** `SQL_PLAIN` is the plain aggregate; `SQL_MAIN` builds the spine, aggregates orders by month and joins. The spine ends at `'2024-04-01'`, so the May order is deliberately outside the report window.

```sql
SELECT date(order_ts, 'start of month') AS month, SUM(amount) AS revenue
FROM orders GROUP BY 1 ORDER BY 1
```
```sql
WITH RECURSIVE months(m) AS (
  SELECT '2024-01-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM months WHERE m < '2024-04-01'
),
monthly AS (
  SELECT date(order_ts, 'start of month') AS m, SUM(amount) AS revenue
  FROM orders GROUP BY 1
)
SELECT months.m AS month, COALESCE(monthly.revenue, 0) AS revenue
FROM months LEFT JOIN monthly ON monthly.m = months.m
ORDER BY months.m
```

**pandas answer:** `groupby(to_period('M'))` leaves February out; `reindex` onto `pd.date_range(..., freq='MS')` with `fill_value=0` forces the spine; `resample('MS').sum()` makes the empty month 0 automatically but also covers every month up to the last order (May here).
```py
spine = pd.date_range("2024-01-01", "2024-04-01", freq="MS")
by_period = orders.groupby(orders["order_ts"].dt.to_period("M"))["amount"].sum()
pd_df = (by_period.rename_axis("month").reset_index(name="revenue")
         .assign(month=lambda d: d["month"].dt.start_time)
         .set_index("month").reindex(spine, fill_value=0)
         .rename_axis("month").reset_index())
pd_df["month"] = pd_df["month"].dt.strftime("%Y-%m-%d")
```

**Example:** Plain `GROUP BY` returned Jan 150, Mar 70, Apr 30, May 999, with no February.
- Spine `2024-01-01, 02-01, 03-01, 04-01` (the recursive step adds one month while `m < '2024-04-01'`, so the last value is 04-01).
- Join: Jan 150, Feb no match so `COALESCE(NULL, 0) = 0`, Mar 70, Apr 30 (the midnight order belongs to April).
- The May order of 999 is not in the report because the spine stops at April; the spine, not the data, defines the window.

**Code:** run with `python3 -I`.
```python
# Q6: monthly revenue with a missing month: GROUP BY drops it, a date spine keeps it
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-01-10 09:00:00',100),(2,'2024-01-20 18:30:00',50),
 (3,'2024-03-05 12:00:00',70),(4,'2024-04-01 00:00:00',30),
 (5,'2024-05-02 10:00:00',999);   -- after the spine's last month
"""
SQL_PLAIN = """
SELECT date(order_ts, 'start of month') AS month, SUM(amount) AS revenue
FROM orders GROUP BY 1 ORDER BY 1
"""
SQL_MAIN = """
WITH RECURSIVE months(m) AS (
  SELECT '2024-01-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM months WHERE m < '2024-04-01'
),
monthly AS (
  SELECT date(order_ts, 'start of month') AS m, SUM(amount) AS revenue
  FROM orders GROUP BY 1
)
SELECT months.m AS month, COALESCE(monthly.revenue, 0) AS revenue
FROM months LEFT JOIN monthly ON monthly.m = months.m
ORDER BY months.m
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("plain GROUP BY:", con.execute(SQL_PLAIN).fetchall())
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("with spine    :", sql_df.values.tolist())

orders = pd.read_sql_query("SELECT * FROM orders", con)
orders["order_ts"] = pd.to_datetime(orders["order_ts"])
s = orders.set_index("order_ts")["amount"]
# pd:main
spine = pd.date_range("2024-01-01", "2024-04-01", freq="MS")
by_period = orders.groupby(orders["order_ts"].dt.to_period("M"))["amount"].sum()
pd_df = (by_period.rename_axis("month").reset_index(name="revenue")
         .assign(month=lambda d: d["month"].dt.start_time)
         .set_index("month").reindex(spine, fill_value=0)
         .rename_axis("month").reset_index())
pd_df["month"] = pd_df["month"].dt.strftime("%Y-%m-%d")
# pd:end
# compared in month order
assert pd_df.values.tolist() == sql_df.values.tolist()
print("groupby to_period('M'):", {str(k): int(v) for k, v in by_period.items()})
print("resample('MS').sum()  :", {k.strftime("%Y-%m"): int(v) for k, v in s.resample("MS").sum().items()})
print("reindexed to spine    :", pd_df.values.tolist())
print("asserts passed")
```

**Output (my run):**
```text
plain GROUP BY: [('2024-01-01', 150), ('2024-03-01', 70), ('2024-04-01', 30), ('2024-05-01', 999)]
with spine    : [['2024-01-01', 150], ['2024-02-01', 0], ['2024-03-01', 70], ['2024-04-01', 30]]
groupby to_period('M'): {'2024-01': 150, '2024-03': 70, '2024-04': 30, '2024-05': 999}
resample('MS').sum()  : {'2024-01': 150, '2024-02': 0, '2024-03': 70, '2024-04': 30, '2024-05': 999}
reindexed to spine    : [['2024-01-01', 150], ['2024-02-01', 0], ['2024-03-01', 70], ['2024-04-01', 30]]
asserts passed
```

**Edge cases:**
- The spine must start and stop on purpose. A spine built from `MIN` and `MAX` of the data hides leading and trailing empty months; a spine hard-coded too short drops data (May here).
- `date(m, '+1 month')` on a first-of-month is safe; on the 29th to 31st it overflows (Part 6 Q8), so always use month starts.
- `resample('MS').sum()` printed `2024-02: 0` and also `2024-05: 999`; the `to_period` groupby printed no February. For means, `resample` gives NaN for empty months, not 0.
- Join on the date form (`date(order_ts,'start of month') = m`), not on text of mixed shapes.
- NULL `amount` values would be ignored by `SUM`; a month with only NULL amounts would show `COALESCE(NULL,0) = 0` just like an empty month.

**Then explain:**
- The recursive CTE is standard SQL (`WITH RECURSIVE`), and it ran on SQLite 3.45. A recursive CTE has an anchor row and a step that stops by a condition; that is what makes it finite.
- Better in production: a physical calendar table (Part 6 Q31), because every query reuses the same spine.
- Other engines (not executed here): PostgreSQL has `generate_series('2024-01-01'::date, '2024-04-01', interval '1 month')`; BigQuery has `GENERATE_DATE_ARRAY(..., INTERVAL 1 MONTH)` with `UNNEST`; Snowflake and others often use a numbers table or recursive CTE; I did not run any of these.
- pandas: reindexing with an explicit `date_range` is the same idea as the spine and gives you control over the window.

**Follow-ups:**
- *What if you need a spine per customer?* Cross join the customer list with the month spine, then left join revenue.
- *Why not generate dates in every query?* Duplication and drift; use a calendar table.
- *How does this feed MoM?* The spine is step one in Q7.

**Common mistakes:**
- Reporting a month-by-month trend from a `GROUP BY` that silently omits zero months.
- Putting the orders table first in the join and then filtering in `WHERE`, which turns the left join back into an inner join.
- A spine that ends before the last data month.
- Expecting `groupby` on a `Period` to create empty groups (it does not).

### Q7 ⭐⭐⭐ 🟡 Month-over-month growth: monthly_revenue derived from orders(order_id, order_ts, amount). Compute revenue, the previous month's revenue with LAG, absolute change and percent change ROUND(100.0 * (rev - prev) / NULLIF(prev, 0), 1). Then show the bug: when a month has no orders, LAG compares with the wrong month (two months back) and the report looks fine. Fix by LEFT JOINing onto a month spine first so the empty month has revenue 0 and the next month shows growth from 0 (NULL, not infinity). Give the pandas version (resample('MS').sum(), pct_change(fill_method=None) giving inf on a zero base). Cross-reference Part 5 for LAG mechanics.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Month-over-month needs a complete month list: `LAG` is positional, so on a list with a missing month it compares March with January and the report still looks fine; join onto a month spine first so February is 0, then `LAG`, and use `NULLIF(prev, 0)` so the percent after a zero month is NULL instead of a divide error (pandas gives `inf`).

**Schema and sample data:** four orders: January has two (100 in total), February has none, March 150, April 120. Convention: calendar months of naive timestamps (UTC). LAG mechanics are Part 5 (cross-reference); here only the gap matters.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-01-10 09:00:00',60),(2,'2024-01-20 18:30:00',40),   -- Jan = 100
 (3,'2024-03-05 12:00:00',150),                                -- Mar = 150, Feb has no orders
 (4,'2024-04-09 00:00:00',120);                                -- Apr = 120
```

**SQL answer:** `SQL_NAIVE` runs `LAG` over the months that exist; `SQL_MAIN` builds the month spine, left-joins revenue, then applies `LAG`, absolute change and `ROUND(100.0 * (rev - prev) / NULLIF(prev, 0), 1)`.

```sql
WITH monthly AS (
  SELECT date(order_ts, 'start of month') AS month, SUM(amount) AS revenue
  FROM orders GROUP BY 1
)
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS pct_change
FROM monthly ORDER BY month
```
```sql
WITH RECURSIVE months(m) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(m, '+1 month') FROM months WHERE m < '2024-04-01'
),
monthly AS (
  SELECT months.m AS month, COALESCE(SUM(o.amount), 0) AS revenue
  FROM months LEFT JOIN orders o ON date(o.order_ts, 'start of month') = months.m
  GROUP BY months.m
),
x AS (
  SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_revenue FROM monthly
)
SELECT month, revenue, prev_revenue,
       revenue - prev_revenue AS change,
       ROUND(100.0 * (revenue - prev_revenue) / NULLIF(prev_revenue, 0), 1) AS pct_change
FROM x ORDER BY month
```

**pandas answer:** `resample('MS').sum()` produces the spine and zero months, then `shift()` for the previous month and a percent where a zero base is turned to NaN; `pct_change(fill_method=None)` is the built-in and returns `inf` on a zero base.
```py
rev = orders.set_index("order_ts")["amount"].resample("MS").sum()
pd_df = pd.DataFrame({"month": rev.index.strftime("%Y-%m-%d"), "revenue": rev.to_numpy()})
pd_df["prev_revenue"] = pd_df["revenue"].shift()
pd_df["change"] = pd_df["revenue"] - pd_df["prev_revenue"]
pd_df["pct_change"] = (100.0 * pd_df["change"] / pd_df["prev_revenue"].replace(0, np.nan)).round(1)
```

**Example:** Naive list: Jan 100, Mar 150, Apr 120. `LAG` for March returns 100 (January), so March shows +50.0 percent 'month over month' when it is really January to March; the output has no row for February and no warning.
- Spine version: Jan 100 (prev NULL, change NULL, percent NULL), Feb 0 (prev 100, change -100, percent -100.0), Mar 150 (prev 0, change +150, percent NULL because the base is zero), Apr 120 (prev 150, change -30, percent -20.0).
- pandas `pct_change(fill_method=None)` returned `[NaN, -1.0, inf, -0.2]`: -100 percent for February, `inf` for March, -20 percent for April. The NaN for January prints as `None` in my output.

**Code:** run with `python3 -I`.
```python
# Q7: month-over-month growth; LAG over a gappy month list is wrong, LAG over a spine is right
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-01-10 09:00:00',60),(2,'2024-01-20 18:30:00',40),   -- Jan = 100
 (3,'2024-03-05 12:00:00',150),                                -- Mar = 150, Feb has no orders
 (4,'2024-04-09 00:00:00',120);                                -- Apr = 120
"""
SQL_NAIVE = """
WITH monthly AS (
  SELECT date(order_ts, 'start of month') AS month, SUM(amount) AS revenue
  FROM orders GROUP BY 1
)
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS pct_change
FROM monthly ORDER BY month
"""
SQL_MAIN = """
WITH RECURSIVE months(m) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(m, '+1 month') FROM months WHERE m < '2024-04-01'
),
monthly AS (
  SELECT months.m AS month, COALESCE(SUM(o.amount), 0) AS revenue
  FROM months LEFT JOIN orders o ON date(o.order_ts, 'start of month') = months.m
  GROUP BY months.m
),
x AS (
  SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_revenue FROM monthly
)
SELECT month, revenue, prev_revenue,
       revenue - prev_revenue AS change,
       ROUND(100.0 * (revenue - prev_revenue) / NULLIF(prev_revenue, 0), 1) AS pct_change
FROM x ORDER BY month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("naive LAG on months that exist:")
print(pd.read_sql_query(SQL_NAIVE, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("LAG on the spine:")
print(sql_df.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
orders["order_ts"] = pd.to_datetime(orders["order_ts"])
# pd:main
rev = orders.set_index("order_ts")["amount"].resample("MS").sum()
pd_df = pd.DataFrame({"month": rev.index.strftime("%Y-%m-%d"), "revenue": rev.to_numpy()})
pd_df["prev_revenue"] = pd_df["revenue"].shift()
pd_df["change"] = pd_df["revenue"] - pd_df["prev_revenue"]
pd_df["pct_change"] = (100.0 * pd_df["change"] / pd_df["prev_revenue"].replace(0, np.nan)).round(1)
# pd:end
# compared in month order; SQL NULL and pandas NaN both read as NaN
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
pc = rev.pct_change(fill_method=None)
print("pct_change(fill_method=None):", [None if pd.isna(v) else v for v in pc.round(3).tolist()])
print("asserts passed")
```

**Output (my run):**
```text
naive LAG on months that exist:
     month  revenue  prev_revenue  pct_change
2024-01-01      100           NaN         NaN
2024-03-01      150         100.0        50.0
2024-04-01      120         150.0       -20.0
LAG on the spine:
     month  revenue  prev_revenue  change  pct_change
2024-01-01      100           NaN     NaN         NaN
2024-02-01        0         100.0  -100.0      -100.0
2024-03-01      150           0.0   150.0         NaN
2024-04-01      120         150.0   -30.0       -20.0
pct_change(fill_method=None): [None, -1.0, inf, -0.2]
asserts passed
```

**Edge cases:**
- Zero base: SQL with `NULLIF` returns NULL (unknown growth), pandas returns `inf`; both mean 'not defined', but only NULL survives averaging and charting safely. Say how a report should show it ('new' or n/a).
- First month: `LAG` returns NULL (no previous month); not 0.
- Partial current month: last month's total is incomplete if the data is mid-month; its percent change is not comparable (Q24 and Q17 handle this).
- In pandas 3 `pct_change` has no default forward fill, so pass `fill_method=None` (as in my run) to be explicit.
- Duplicated months in the input (a monthly table built by union) would make `LAG` compare a month with itself; aggregate first.

**Then explain:**
- `LAG(revenue)` looks at the previous row in the sort order; the spine guarantees the previous row is the previous month.
- Absolute change versus percent: report both; percent alone hides scale.
- `ROUND(..., 1)` and `100.0 *` keep the arithmetic in floating point; `100 *` on integers would still divide as REAL here because of `100.0`, but plain `(rev-prev)/prev` with two integers would truncate.
- Other engines (not executed here): the same `LAG` query runs in PostgreSQL, MySQL 8, BigQuery and Snowflake; division by zero errors in some (PostgreSQL) and returns NULL in others (MySQL), which is why `NULLIF` is portable.

**Follow-ups:**
- *Year over year?* Same-month-last-year, with the spine (Part 6 Q17).
- *How would you show the zero-base month?* 'n/a' or 'new', not infinity.
- *Where do the LAG details live?* Part 5.

**Common mistakes:**
- Running `LAG` over a table that is missing months.
- Dividing by `prev` without `NULLIF`.
- Treating a NULL first-month growth as 0.
- Using `pct_change()` and not noticing `inf`.

### Q8 ⭐⭐⭐ 🟡 Month arithmetic and end-of-month edge cases: what do date('2024-01-31', '+1 month'), date('2023-01-31', '+1 month') and date('2024-03-31', '-1 month') return in SQLite (overflow into the next month, so 2023-01-31 + 1 month is 2023-03-03), and how do you get the last day of the month safely (date(x, 'start of month', '+1 month', '-1 day'))? Show the pandas behaviour: Timestamp + pd.DateOffset(months=1) clips to the last valid day (2023-02-28), pd.offsets.MonthEnd, and Period arithmetic. Explain why 'one month later' needs a business definition, and give the effect on a subscription renewal on the 31st.
**Asked at:** SQLite date and time functions documentation (lang_datefunc, opened), vendor documentation and not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** SQLite overflows: adding a month to the 31st can land in the next month (`date('2023-01-31','+1 month')` is `2023-03-03`), so for last-day-of-month use `date(x,'start of month','+1 month','-1 day')`; pandas `DateOffset(months=1)` clips instead (`2023-02-28`), so the two tools disagree unless you emulate the clip.

**Schema and sample data:** two subscriptions that start on a 31st, one in a leap year (2024) and one not (2023), and a small numbers table 0 to 4 for renewal counts.
```sql
CREATE TABLE subs(sub_id INTEGER PRIMARY KEY, start_date TEXT);
INSERT INTO subs VALUES (1,'2024-01-31'),(2,'2023-01-31');
CREATE TABLE n(n INTEGER);
INSERT INTO n VALUES (0),(1),(2),(3),(4);
```

**SQL answer:** `SQL_MAIN` returns, for each subscription and renewal number n, the overflow date (`start + n months` as SQLite computes it) and a clipped date that falls back to the last day of the target month, anchored on the start date.

```sql
SELECT s.sub_id, n.n,
       date(s.start_date, printf('+%d months', n.n)) AS overflow_date,
       CASE WHEN strftime('%d', date(s.start_date, printf('+%d months', n.n))) <> strftime('%d', s.start_date)
            THEN date(s.start_date, 'start of month', printf('+%d months', n.n + 1), '-1 day')
            ELSE date(s.start_date, printf('+%d months', n.n)) END AS clipped_date
FROM subs s CROSS JOIN n
ORDER BY s.sub_id, n.n
```

**pandas answer:** `Timestamp + pd.DateOffset(months=k)` clips to the last valid day; anchoring on the start date (not chaining from the previous renewal) reproduces the SQL clipped column.
```py
rows = []
for sub_id, start in zip(subs["sub_id"], pd.to_datetime(subs["start_date"])):
    for k in range(5):
        rows.append((sub_id, k, (start + pd.DateOffset(months=k)).strftime("%Y-%m-%d")))
pd_df = pd.DataFrame(rows, columns=["sub_id", "n", "clipped_date"])
```

**Example:** - `date('2024-01-31','+1 month')` = `2024-03-02` (Feb 2024 has 29 days, so 31 February is 2 March). `date('2023-01-31','+1 month')` = `2023-03-03`. `date('2024-03-31','-1 month')` = `2024-03-02` (31 February again).
- Last day: `date('2024-01-31','start of month','+1 month','-1 day')` = `2024-01-31`; for 10 Feb 2023 it gave `2023-02-28`, for 10 Feb 2024 `2024-02-29`.
- Subscriber starting 2024-01-31, anchored on the start date: n = 0 to 4 gives overflow `01-31, 03-02, 03-31, 05-01, 05-31` but clipped `01-31, 02-29, 03-31, 04-30, 05-31`. The overflow version has no date in February or April and two in March; the clipped version has exactly one date in each month.

**Code:** run with `python3 -I`.
```python
# Q8: month arithmetic and end-of-month edges: SQLite overflow vs pandas DateOffset clipping
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE subs(sub_id INTEGER PRIMARY KEY, start_date TEXT);
INSERT INTO subs VALUES (1,'2024-01-31'),(2,'2023-01-31');
CREATE TABLE n(n INTEGER);
INSERT INTO n VALUES (0),(1),(2),(3),(4);
"""
# clipped = anchored on the start date, month-end clipped like pandas DateOffset
SQL_MAIN = """
SELECT s.sub_id, n.n,
       date(s.start_date, printf('+%d months', n.n)) AS overflow_date,
       CASE WHEN strftime('%d', date(s.start_date, printf('+%d months', n.n))) <> strftime('%d', s.start_date)
            THEN date(s.start_date, 'start of month', printf('+%d months', n.n + 1), '-1 day')
            ELSE date(s.start_date, printf('+%d months', n.n)) END AS clipped_date
FROM subs s CROSS JOIN n
ORDER BY s.sub_id, n.n
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print(con.execute("""SELECT date('2024-01-31','+1 month'), date('2023-01-31','+1 month'), date('2024-03-31','-1 month'),
                            date('2024-01-31','start of month','+1 month','-1 day'), date('2023-02-10','start of month','+1 month','-1 day'),
                            date('2024-02-10','start of month','+1 month','-1 day')""").fetchone())
print("newer-version modifiers on 3.45.1 (NULL = unsupported):", con.execute("SELECT date('2024-01-15','end of month'), date('2024-01-15','floor'), date('2024-01-15','weekday -1')").fetchone(), sqlite3.sqlite_version)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

subs = pd.read_sql_query("SELECT * FROM subs", con)
# pd:main
rows = []
for sub_id, start in zip(subs["sub_id"], pd.to_datetime(subs["start_date"])):
    for k in range(5):
        rows.append((sub_id, k, (start + pd.DateOffset(months=k)).strftime("%Y-%m-%d")))
pd_df = pd.DataFrame(rows, columns=["sub_id", "n", "clipped_date"])
# pd:end
# compared in (sub_id, n) order
assert pd_df["clipped_date"].tolist() == sql_df["clipped_date"].tolist()
print("pandas DateOffset(months=k) == SQL clipped_date for all", len(pd_df), "rows")

t = pd.Timestamp("2023-01-31")
print("Timestamp 2023-01-31 + DateOffset(months=1):", (t + pd.DateOffset(months=1)).date())
print("Timestamp 2024-03-31 - DateOffset(months=1):", (pd.Timestamp("2024-03-31") - pd.DateOffset(months=1)).date())
print("MonthEnd(1) from 01-31 / 01-15; MonthEnd(0) from 01-31 / 01-15:",
      [(pd.Timestamp(x) + pd.offsets.MonthEnd(k)).date().isoformat() for x, k in
       [("2024-01-31", 1), ("2024-01-15", 1), ("2024-01-31", 0), ("2024-01-15", 0)]])
p = pd.Period("2023-01-31", "M")
print("Period('2023-01-31','M') + 1:", p + 1, "| end_time:", (p + 1).end_time, "| months between:", (pd.Period("2024-03", "M") - pd.Period("2023-11", "M")).n)
# one-month-later chained from the previous renewal (drift) in pandas
d = pd.Timestamp("2024-01-31"); chain = [d.date().isoformat()]
for _ in range(4):
    d = d + pd.DateOffset(months=1); chain.append(d.date().isoformat())
print("chained renewals from 2024-01-31 (each +1 month from the last):", chain)
ends = ["2024-01-31", "2023-02-10", "2024-02-10"]
sql_last = [r[0] for r in con.execute("SELECT date(x,'start of month','+1 month','-1 day') FROM (SELECT '%s' AS x)" % "' AS x UNION ALL SELECT '".join(ends))]
pd_last = [(pd.Timestamp(x) + pd.offsets.MonthEnd(0)).date().isoformat() for x in ends]
assert sql_last == pd_last, (sql_last, pd_last)
print("last day of month, SQL == pandas MonthEnd(0):", sql_last)
print("asserts passed")
```

**Output (my run):**
```text
('2024-03-02', '2023-03-03', '2024-03-02', '2024-01-31', '2023-02-28', '2024-02-29')
newer-version modifiers on 3.45.1 (NULL = unsupported): (None, None, None) 3.45.1
 sub_id  n overflow_date clipped_date
      1  0    2024-01-31   2024-01-31
      1  1    2024-03-02   2024-02-29
      1  2    2024-03-31   2024-03-31
      1  3    2024-05-01   2024-04-30
      1  4    2024-05-31   2024-05-31
      2  0    2023-01-31   2023-01-31
      2  1    2023-03-03   2023-02-28
      2  2    2023-03-31   2023-03-31
      2  3    2023-05-01   2023-04-30
      2  4    2023-05-31   2023-05-31
pandas DateOffset(months=k) == SQL clipped_date for all 10 rows
Timestamp 2023-01-31 + DateOffset(months=1): 2023-02-28
Timestamp 2024-03-31 - DateOffset(months=1): 2024-02-29
MonthEnd(1) from 01-31 / 01-15; MonthEnd(0) from 01-31 / 01-15: ['2024-02-29', '2024-01-31', '2024-01-31', '2024-01-31']
Period('2023-01-31','M') + 1: 2023-02 | end_time: 2023-02-28 23:59:59.999999 | months between: 4
chained renewals from 2024-01-31 (each +1 month from the last): ['2024-01-31', '2024-02-29', '2024-03-29', '2024-04-29', '2024-05-29']
last day of month, SQL == pandas MonthEnd(0): ['2024-01-31', '2023-02-28', '2024-02-29']
asserts passed
```

**Edge cases:**
- Overflow is deterministic, not an error: the extra days roll forward. SQLite does not validate the day, so a rolled date looks legitimate.
- Chained renewals (each month added to the previous renewal) drift even with clipping: pandas from 2024-01-31 gave `01-31, 02-29, 03-29, 04-29, 05-29`, permanently stuck on the 29th. Anchor on the original day, or store the anchor day.
- pandas `MonthEnd(1)` from 31 January went to 29 February, from 15 January to 31 January; `MonthEnd(0)` rolls forward only if the date is not already a month end (31 Jan stayed, 15 Jan went to 31 Jan).
- `Period('2023-01-31','M') + 1` is the period `2023-02`; its `end_time` is `2023-02-28 23:59:59.999999`. Period arithmetic counts months, so it has no overflow.
- Negative months: pandas `2024-03-31 - DateOffset(months=1)` gave `2024-02-29` (clipped), SQLite gave `2024-03-02`.

**Then explain:**
- 'One month later' is a business definition: same day number clipped to month end (typical for pandas and most billing systems), same day with overflow (SQLite default), or 30 days. Write the rule down.
- For a renewal on the 31st, clipped anchored dates bill Jan 31, Feb 29, Mar 31, Apr 30, which is the usual intent; the overflow rule would bill on 2 March and 1 May, which looks like a bug (a business rule, not a fact about SQLite).
- Safe month math in SQLite: go through `'start of month'`, add months to the first, then add days back if needed.
- The 'end of month', 'floor' and negative 'weekday' modifiers are documented as newer additions and returned NULL in my run on SQLite 3.45.1 (see the output); I used the `start of month` form that works.
- Other engines (not executed here): PostgreSQL `date + interval '1 month'` clips to the month end; MySQL `DATE_ADD(d, INTERVAL 1 MONTH)` clips; BigQuery `DATE_ADD(d, INTERVAL 1 MONTH)` clips; Snowflake `DATEADD(month, 1, d)` clips. These are from memory and were not executed.

**Follow-ups:**
- *Billing on the 31st for 12 months?* Store the anchor day and compute each renewal from it with a clip.
- *First day of next month?* `date(x,'start of month','+1 month')`.
- *Months between two dates?* `(y2 - y1) * 12 + (m2 - m1)` (Q10).

**Common mistakes:**
- Trusting `+1 month` on a date after the 28th.
- Chaining month additions and drifting to the 28th or 29th.
- Assuming SQLite and pandas clip the same way.
- Hard-coding 30 days for 'a month'.

### Q9 ⭐⭐⭐ 🟡 First-order (acquisition) cohort assignment: orders(order_id, user_id, order_ts, amount) and users(user_id, signup_date) where some users never ordered. Assign each user's cohort month as the month of their first order (MIN(order_ts) per user), compute cohort size per month, and contrast with a signup-month cohort that includes never-purchasers. Show the pandas version with groupby('user_id')['order_ts'].transform('min') and to_period('M'), and say what each definition does to the denominator.
**Asked at:** search-result snippets of cohort-retention prep pages (Dataford 'joins for retention rates' Zomato-style first-order-month retention by city, PracHub Amazon-tagged monthly cohort retention, letsdatascience cohort guide, Level Up Gitconnected retention article; not opened, the Dataford page returned HTTP 429 and Level Up returned 403), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** A first-order cohort puts each user in the month of their first order (`MIN(order_ts)` per user), so its denominator holds only people who ordered; a signup-month cohort keeps never-purchasers in the denominator, so the same retention numerator looks smaller.

**Schema and sample data:** six users, two of whom never ordered (users 3 and 5); user 2 signed up in January but first ordered in February. Convention: months are calendar months of the stored text (naive, read as UTC).
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO users VALUES (1,'2024-01-05'),(2,'2024-01-20'),(3,'2024-01-28'),(4,'2024-02-03'),(5,'2024-02-10'),(6,'2024-02-25');
INSERT INTO orders VALUES
 (1,1,'2024-01-07 10:00:00',100),(2,1,'2024-03-15 11:00:00',50),
 (3,2,'2024-02-02 09:30:00',80),
 (4,4,'2024-02-04 12:00:00',60),(5,4,'2024-02-20 13:00:00',40),
 (6,6,'2024-04-01 00:00:00',90);
```

**SQL answer:** `first_order` takes `MIN(order_ts)` per user; the month cohort size counts those users; the signup cohort counts all users by signup month and also shows how many of them never ordered. Months from both sets are unioned so a month that has only one kind of cohort still appears.

```sql
WITH first_order AS (
  SELECT user_id, MIN(order_ts) AS first_ts FROM orders GROUP BY user_id
),
fo AS (
  SELECT strftime('%Y-%m', first_ts) AS month, COUNT(*) AS first_order_cohort FROM first_order GROUP BY 1
),
su AS (
  SELECT strftime('%Y-%m', signup_date) AS month, COUNT(*) AS signup_cohort,
         SUM(CASE WHEN user_id NOT IN (SELECT user_id FROM orders) THEN 1 ELSE 0 END) AS never_ordered
  FROM users GROUP BY 1
),
months AS (SELECT month FROM fo UNION SELECT month FROM su)
SELECT m.month,
       COALESCE(fo.first_order_cohort, 0) AS first_order_cohort,
       COALESCE(su.signup_cohort, 0)      AS signup_cohort,
       COALESCE(su.never_ordered, 0)      AS never_ordered
FROM months m LEFT JOIN fo ON fo.month = m.month LEFT JOIN su ON su.month = m.month
ORDER BY m.month
```

**pandas answer:** `groupby('user_id')['order_ts'].transform('min')` puts each user's first timestamp on every order row; `to_period('M')` makes the cohort; one row per user is then counted.
```py
orders["order_ts"] = pd.to_datetime(orders["order_ts"])
orders["first_ts"] = orders.groupby("user_id")["order_ts"].transform("min")
orders["cohort"] = orders["first_ts"].dt.to_period("M")
first_order = orders.drop_duplicates("user_id").set_index("user_id")["cohort"]
signup = pd.to_datetime(users["signup_date"]).dt.to_period("M")
out = pd.DataFrame({
    "first_order_cohort": first_order.value_counts(),
    "signup_cohort": signup.value_counts(),
    "never_ordered": signup[~users["user_id"].isin(orders["user_id"])].value_counts(),
}).fillna(0).astype(int).sort_index()
pd_df = out.rename_axis("month").reset_index()
pd_df["month"] = pd_df["month"].astype(str)
```

**Example:** First orders: user 1 on 2024-01-07 (Jan), user 2 on 2024-02-02 (Feb), user 4 on 2024-02-04 (Feb), user 6 on 2024-04-01 00:00:00 (Apr). Users 3 and 5 have no orders.
- First-order cohorts: 2024-01 has 1 user, 2024-02 has 2, 2024-04 has 1; total 4 buyers.
- Signup cohorts: 2024-01 has users 1, 2, 3 (size 3, one never ordered); 2024-02 has users 4, 5, 6 (size 3, one never ordered); 2024-04 has none.
- So January retention for a given later month would be divided by 1 under the first-order cohort and by 3 under the signup cohort. User 2 changes cohort: signed up in January, first ordered in February.

**Code:** run with `python3 -I`.
```python
# Q9: first-order (acquisition) cohort vs signup-month cohort
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO users VALUES (1,'2024-01-05'),(2,'2024-01-20'),(3,'2024-01-28'),(4,'2024-02-03'),(5,'2024-02-10'),(6,'2024-02-25');
INSERT INTO orders VALUES
 (1,1,'2024-01-07 10:00:00',100),(2,1,'2024-03-15 11:00:00',50),
 (3,2,'2024-02-02 09:30:00',80),
 (4,4,'2024-02-04 12:00:00',60),(5,4,'2024-02-20 13:00:00',40),
 (6,6,'2024-04-01 00:00:00',90);
"""
SQL_MAIN = """
WITH first_order AS (
  SELECT user_id, MIN(order_ts) AS first_ts FROM orders GROUP BY user_id
),
fo AS (
  SELECT strftime('%Y-%m', first_ts) AS month, COUNT(*) AS first_order_cohort FROM first_order GROUP BY 1
),
su AS (
  SELECT strftime('%Y-%m', signup_date) AS month, COUNT(*) AS signup_cohort,
         SUM(CASE WHEN user_id NOT IN (SELECT user_id FROM orders) THEN 1 ELSE 0 END) AS never_ordered
  FROM users GROUP BY 1
),
months AS (SELECT month FROM fo UNION SELECT month FROM su)
SELECT m.month,
       COALESCE(fo.first_order_cohort, 0) AS first_order_cohort,
       COALESCE(su.signup_cohort, 0)      AS signup_cohort,
       COALESCE(su.never_ordered, 0)      AS never_ordered
FROM months m LEFT JOIN fo ON fo.month = m.month LEFT JOIN su ON su.month = m.month
ORDER BY m.month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
orders["order_ts"] = pd.to_datetime(orders["order_ts"])
orders["first_ts"] = orders.groupby("user_id")["order_ts"].transform("min")
orders["cohort"] = orders["first_ts"].dt.to_period("M")
first_order = orders.drop_duplicates("user_id").set_index("user_id")["cohort"]
signup = pd.to_datetime(users["signup_date"]).dt.to_period("M")
out = pd.DataFrame({
    "first_order_cohort": first_order.value_counts(),
    "signup_cohort": signup.value_counts(),
    "never_ordered": signup[~users["user_id"].isin(orders["user_id"])].value_counts(),
}).fillna(0).astype(int).sort_index()
pd_df = out.rename_axis("month").reset_index()
pd_df["month"] = pd_df["month"].astype(str)
# pd:end
# compared in month order
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas == SQL")
print("users who ordered / users:", orders["user_id"].nunique(), "/", len(users))
print("user 2 signed up in 2024-01 but first ordered in", str(first_order[2]))
print("asserts passed")
```

**Output (my run):**
```text
  month  first_order_cohort  signup_cohort  never_ordered
2024-01                   1              3              1
2024-02                   2              3              1
2024-04                   1              0              0
pandas == SQL
users who ordered / users: 4 / 6
user 2 signed up in 2024-01 but first ordered in 2024-02
asserts passed
```

**Edge cases:**
- Users who never ordered: absent from the first-order cohort by construction, present in the signup cohort (`NOT IN (SELECT user_id FROM orders)` counted them; if `orders.user_id` could be NULL, `NOT IN` would return nothing, so `NOT EXISTS` is safer).
- Ties and time of day: `MIN(order_ts)` on text works for ISO timestamps; two orders on the same instant still give one cohort.
- A user whose first order is in a later month than signup moves months; cohort month must come from the first order, not signup.
- Refunds, cancelled or test orders: decide whether they count as 'first order' before writing `MIN`. I did not model them.
- Months with no cohort (2024-03 here) have no row; the spine pattern from Q6 fills them if needed.

**Then explain:**
- First-order (acquisition) cohorts measure customers by when they became customers; the denominator is 'users who bought'. This is the usual choice for repeat-purchase and order-retention questions.
- Signup cohorts measure the funnel from registration; the denominator includes people who never bought, so month-0 'retention' is below 100 percent. Funnel conversion design belongs to Part 8.
- Choose one, say it before coding, and keep the denominator fixed when you compute retention (Q11).
- `transform('min')` keeps the original row count (one value per order), while `groupby().min()` collapses to one row per user; I used `drop_duplicates('user_id')` after the transform to count users once.
- Other engines (not executed here): the `MIN() ... GROUP BY` form is the same everywhere; only the month truncation function differs (Q2, Q36).

**Follow-ups:**
- *Which one do you report to the CFO?* The one that matches the question: first-order for customer retention, signup for activation.
- *What if the first order is cancelled?* Filter by order status before `MIN`.
- *How do you avoid counting a user twice?* Group by user_id first; count distinct users per cohort.

**Common mistakes:**
- Using signup month as the cohort and calling it 'first purchase'.
- `NOT IN` against a nullable column.
- Taking `MIN(order_ts)` over a joined table that has fanned out rows (the minimum is fine, but the count of users is not).
- Counting orders rather than users in the cohort size.

### Q10 ⭐⭐⭐ 🟡 Cohort retention counts (month 0 to n): orders(order_id, user_id, order_ts). For each first-order cohort month return cohort_month, months_since_first (0, 1, 2, ...) and the number of distinct active users, counting a user once per cohort and month. Compute the month offset as (year difference * 12 + month difference) from strftime, not by subtracting month numbers (December to January breaks the naive form). Show the pandas cohort matrix with pivot_table(index='cohort', columns='period_number', values='user_id', aggfunc='nunique'), and note the 'at least one event in the calendar month' definition used in the PracHub-style prompt.
**Asked at:** PracHub 'compute cohort retention rate' listing (opened; the page tags it Intuit, Data Scientist, technical screen, but cites no primary source, so treat the attribution as site-reported and unverified); product-company data scientist screens
**Say this first (1 line):** For each user take the first order month as the cohort, compute each order's month offset as `(order year - cohort year) * 12 + (order month - cohort month)`, and count `DISTINCT user_id` per cohort and offset, so a user with three orders in one month counts once.

**Schema and sample data:** five users around the December to January boundary: user 1 orders twice in November, then December and January; user 2 orders in November and again in February; users 3, 4 and 5 start in December and January. Convention: calendar months of naive timestamps (UTC); a user is active in a month if they have at least one order in it.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT);
INSERT INTO orders VALUES
 (1,1,'2023-11-05 10:00:00'),(2,1,'2023-11-25 09:00:00'),(3,1,'2023-12-20 18:00:00'),(4,1,'2024-01-10 08:00:00'),
 (5,2,'2023-11-15 12:00:00'),(6,2,'2024-02-02 13:00:00'),
 (7,3,'2023-12-03 11:00:00'),(8,3,'2024-01-04 16:00:00'),(9,3,'2024-01-18 17:00:00'),
 (10,4,'2023-12-12 14:00:00'),
 (11,5,'2024-01-09 10:30:00'),(12,5,'2024-02-11 15:45:00');
```

**SQL answer:** the month index `year*12 + month` makes the subtraction exact across years; the cohort is the minimum index per user. The query counts distinct users per (cohort, offset). `SQL_NAIVE` shows what happens if you subtract month numbers.

```sql
WITH o AS (
  SELECT user_id,
         CAST(strftime('%Y', order_ts) AS INTEGER) AS y,
         CAST(strftime('%m', order_ts) AS INTEGER) AS m
  FROM orders
),
c AS (
  SELECT user_id, MIN(y * 12 + m) AS first_idx FROM o GROUP BY user_id
),
x AS (
  SELECT o.user_id,
         printf('%04d-%02d', (c.first_idx - 1) / 12, (c.first_idx - 1) % 12 + 1) AS cohort_month,
         (o.y * 12 + o.m) - c.first_idx AS months_since_first
  FROM o JOIN c ON c.user_id = o.user_id
)
SELECT cohort_month, months_since_first, COUNT(DISTINCT user_id) AS active_users
FROM x
GROUP BY cohort_month, months_since_first
ORDER BY cohort_month, months_since_first
```
```sql
WITH f AS (SELECT user_id, MIN(order_ts) AS first_ts FROM orders GROUP BY user_id)
SELECT o.user_id, strftime('%Y-%m', f.first_ts) AS cohort,
       CAST(strftime('%m', o.order_ts) AS INTEGER) - CAST(strftime('%m', f.first_ts) AS INTEGER) AS naive_offset
FROM orders o JOIN f USING(user_id) WHERE o.user_id = 1 GROUP BY o.user_id, strftime('%Y-%m', o.order_ts)
```

**pandas answer:** a per-user `transform('min')` on the month `Period`, the same year-and-month arithmetic for `period_number`, and `pivot_table(..., aggfunc='nunique')` to get the cohort matrix; I melt it back to long form to compare with SQL.
```py
orders["order_ts"] = pd.to_datetime(orders["order_ts"])
orders["ym"] = orders["order_ts"].dt.to_period("M")
orders["cohort"] = orders.groupby("user_id")["ym"].transform("min")
orders["period_number"] = ((orders["ym"].dt.year - orders["cohort"].dt.year) * 12
                           + (orders["ym"].dt.month - orders["cohort"].dt.month))
matrix = orders.pivot_table(index="cohort", columns="period_number", values="user_id", aggfunc="nunique")
pd_df = (matrix.rename_axis(columns=None).reset_index()
         .melt(id_vars="cohort", var_name="months_since_first", value_name="active_users")
         .dropna().astype({"active_users": int}))
pd_df["cohort_month"] = pd_df["cohort"].astype(str)
pd_df = (pd_df[["cohort_month", "months_since_first", "active_users"]]
         .sort_values(["cohort_month", "months_since_first"]).reset_index(drop=True))
```

**Example:** - User 1: orders in 2023-11 (two of them), 2023-12 and 2024-01. Cohort 2023-11; offsets 0, 0, 1, 2. After the distinct count the user is active at offsets 0, 1 and 2.
- User 2: 2023-11 and 2024-02: cohort 2023-11, offsets 0 and 3.
- Cohort 2023-11: offset 0 has users 1 and 2 (2), offset 1 has user 1 (1), offset 2 has user 1 (1), offset 3 has user 2 (1).
- Cohort 2023-12: users 3 and 4 at offset 0 (2); user 3 returns in January twice, counted once at offset 1 (1). Cohort 2024-01: user 5, offsets 0 and 1 (Feb), so 1 and 1.
- The naive offset (`month number - cohort month number`) for user 1 was `0, 1, -10`: January minus November. The correct offset is 2.

**Code:** run with `python3 -I`.
```python
# Q10: cohort retention counts, month 0..n, distinct active users per cohort and month offset
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT);
INSERT INTO orders VALUES
 (1,1,'2023-11-05 10:00:00'),(2,1,'2023-11-25 09:00:00'),(3,1,'2023-12-20 18:00:00'),(4,1,'2024-01-10 08:00:00'),
 (5,2,'2023-11-15 12:00:00'),(6,2,'2024-02-02 13:00:00'),
 (7,3,'2023-12-03 11:00:00'),(8,3,'2024-01-04 16:00:00'),(9,3,'2024-01-18 17:00:00'),
 (10,4,'2023-12-12 14:00:00'),
 (11,5,'2024-01-09 10:30:00'),(12,5,'2024-02-11 15:45:00');
"""
SQL_MAIN = """
WITH o AS (
  SELECT user_id,
         CAST(strftime('%Y', order_ts) AS INTEGER) AS y,
         CAST(strftime('%m', order_ts) AS INTEGER) AS m
  FROM orders
),
c AS (
  SELECT user_id, MIN(y * 12 + m) AS first_idx FROM o GROUP BY user_id
),
x AS (
  SELECT o.user_id,
         printf('%04d-%02d', (c.first_idx - 1) / 12, (c.first_idx - 1) % 12 + 1) AS cohort_month,
         (o.y * 12 + o.m) - c.first_idx AS months_since_first
  FROM o JOIN c ON c.user_id = o.user_id
)
SELECT cohort_month, months_since_first, COUNT(DISTINCT user_id) AS active_users
FROM x
GROUP BY cohort_month, months_since_first
ORDER BY cohort_month, months_since_first
"""
SQL_NAIVE = """
WITH f AS (SELECT user_id, MIN(order_ts) AS first_ts FROM orders GROUP BY user_id)
SELECT o.user_id, strftime('%Y-%m', f.first_ts) AS cohort,
       CAST(strftime('%m', o.order_ts) AS INTEGER) - CAST(strftime('%m', f.first_ts) AS INTEGER) AS naive_offset
FROM orders o JOIN f USING(user_id) WHERE o.user_id = 1 GROUP BY o.user_id, strftime('%Y-%m', o.order_ts)
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("naive month-number difference for user 1:", [r[2] for r in con.execute(SQL_NAIVE)], "(true 0, 1, 2)")

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
orders["order_ts"] = pd.to_datetime(orders["order_ts"])
orders["ym"] = orders["order_ts"].dt.to_period("M")
orders["cohort"] = orders.groupby("user_id")["ym"].transform("min")
orders["period_number"] = ((orders["ym"].dt.year - orders["cohort"].dt.year) * 12
                           + (orders["ym"].dt.month - orders["cohort"].dt.month))
matrix = orders.pivot_table(index="cohort", columns="period_number", values="user_id", aggfunc="nunique")
pd_df = (matrix.rename_axis(columns=None).reset_index()
         .melt(id_vars="cohort", var_name="months_since_first", value_name="active_users")
         .dropna().astype({"active_users": int}))
pd_df["cohort_month"] = pd_df["cohort"].astype(str)
pd_df = (pd_df[["cohort_month", "months_since_first", "active_users"]]
         .sort_values(["cohort_month", "months_since_first"]).reset_index(drop=True))
# pd:end
# compared after sorting by cohort_month, months_since_first
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas cohort matrix (NaN = month not observed or nobody active):")
print(matrix.to_string())
print("asserts passed")
```

**Output (my run):**
```text
cohort_month  months_since_first  active_users
     2023-11                   0             2
     2023-11                   1             1
     2023-11                   2             1
     2023-11                   3             1
     2023-12                   0             2
     2023-12                   1             1
     2024-01                   0             1
     2024-01                   1             1
naive month-number difference for user 1: [0, 1, -10] (true 0, 1, 2)
pandas cohort matrix (NaN = month not observed or nobody active):
period_number    0    1    2    3
cohort                           
2023-11        2.0  1.0  1.0  1.0
2023-12        2.0  1.0  NaN  NaN
2024-01        1.0  1.0  NaN  NaN
asserts passed
```

**Edge cases:**
- Year boundary: the naive month-number difference gives -10 for January after a November cohort; the year-times-12 form gives 2.
- Several orders in one month: counted once because of `COUNT(DISTINCT user_id)`; counting rows would inflate retention.
- Cells with nobody active are absent in SQL and NaN in the pandas matrix (cohort 2023-12 has no offset 2 row). Whether a missing cell is 'zero' or 'not yet observed' is Q11.
- Definition: 'active' here means at least one order in the calendar month, as in the PracHub-style prompt (any activity in calendar month k after the cohort month). Attribution to a company on that page is site-reported and unverified. A rolling window (30 days after signup) gives different numbers.
- Time zone: the month boundary depends on the zone of `order_ts`; an order at 23:30 UTC on 31 January is February in IST (Q16).
- NULL `order_ts` rows: `strftime` gives NULL, and they should be filtered out before the cohort step.

**Then explain:**
- Two-step shape: cohort per user, then activity per user and month, then a count; everything else is presentation.
- The month index trick (`year*12 + month`) avoids calendar functions for offsets and works in any engine.
- `COUNT(DISTINCT)` handles users with several orders in a month; in pandas `nunique` does.
- Matrix form: rows are cohorts, columns are offsets 0, 1, 2, ...; the diagonal triangle of missing cells is real, because later cohorts have fewer months of history.
- Other engines (not executed here): PostgreSQL and others use `DATE_TRUNC('month', ...)` and `DATEDIFF` or `AGE` for the offset; the arithmetic form above is portable.

**Follow-ups:**
- *Retention percent?* Divide by the month-0 count (Q11).
- *Day-based windows?* Different definition; Part 6 Q13.
- *Segment cohorts?* Add a segment column and a cohort size per segment (Q41).

**Common mistakes:**
- Subtracting month numbers (`strftime('%m')`) without the year.
- Counting orders instead of distinct users per month.
- Taking the cohort as the order month of each row instead of the user's first order month.
- Joining orders to itself and double counting before the distinct.

### Q11 ⭐⭐⭐ 🟡 Cohort retention percentage and the triangle: from the cohort counts above return retention % = 100 * active_users / cohort_size (cohort size is the month-0 count) as one row per cohort with columns m0, m1, m2, m3. Explain NULL versus 0 for months that have not happened yet (the triangle) versus months with zero retained users, and why a partial current month understates the latest column. Give SQL with conditional aggregation (SUM(CASE WHEN months_since = 1 ...)) and pandas dividing the pivot by its first column (div(axis=0)).
**Asked at:** DataDriven 'monthly cohort retention' / 'The Slow Fade' mock-interview page (opened; no company label, medium, L4 seniority), a practice-site problem and not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Retention percent is `100 * active_users / cohort_size` where cohort size is the month-0 count; pivot to one row per cohort with `SUM(CASE WHEN months_since = k THEN active_users END)`, and show NULL for months that have not happened yet but 0 for months that happened and nobody came back.

**Schema and sample data:** the same twelve orders as Q10 (five users, November 2023 to February 2024). Convention: calendar months of naive timestamps (UTC); the last loaded month is the latest month present in the data (February 2024). A second table, `orders_snap`, holds the same orders loaded only up to 5 February to show the partial-month effect.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT);
INSERT INTO orders VALUES
 (1,1,'2023-11-05 10:00:00'),(2,1,'2023-11-25 09:00:00'),(3,1,'2023-12-20 18:00:00'),(4,1,'2024-01-10 08:00:00'),
 (5,2,'2023-11-15 12:00:00'),(6,2,'2024-02-02 13:00:00'),
 (7,3,'2023-12-03 11:00:00'),(8,3,'2024-01-04 16:00:00'),(9,3,'2024-01-18 17:00:00'),
 (10,4,'2023-12-12 14:00:00'),
 (11,5,'2024-01-09 10:30:00'),(12,5,'2024-02-11 15:45:00');
CREATE TABLE orders_snap AS SELECT * FROM orders WHERE order_ts < '2024-02-06';  -- same data loaded only to 5 Feb
```

**SQL answer:** counts per (first month, offset) are the Q10 result; the final select pivots them into `m0` to `m3` with conditional aggregation, and the `CASE WHEN first_idx + k <= last_idx` guard produces NULL for months that have not happened yet. The `COALESCE(..., 0)` inside turns an observed month with no row into 0. The snapshot run is the same text with `orders` replaced by `orders_snap`.

```sql
WITH o AS (
  SELECT user_id, CAST(strftime('%Y', order_ts) AS INTEGER) * 12 + CAST(strftime('%m', order_ts) AS INTEGER) AS idx
  FROM orders
),
last AS (SELECT MAX(idx) AS last_idx FROM o),
c AS (SELECT user_id, MIN(idx) AS first_idx FROM o GROUP BY user_id),
counts AS (
  SELECT c.first_idx, o.idx - c.first_idx AS months_since, COUNT(DISTINCT o.user_id) AS active_users
  FROM o JOIN c ON c.user_id = o.user_id
  GROUP BY c.first_idx, o.idx - c.first_idx
)
SELECT printf('%04d-%02d', (first_idx - 1) / 12, (first_idx - 1) % 12 + 1) AS cohort_month,
       SUM(CASE WHEN months_since = 0 THEN active_users END) AS cohort_size,
       CASE WHEN first_idx + 0 <= last_idx THEN ROUND(100.0 * COALESCE(SUM(CASE WHEN months_since = 0 THEN active_users END), 0) / SUM(CASE WHEN months_since = 0 THEN active_users END), 1) END AS m0,
       CASE WHEN first_idx + 1 <= last_idx THEN ROUND(100.0 * COALESCE(SUM(CASE WHEN months_since = 1 THEN active_users END), 0) / SUM(CASE WHEN months_since = 0 THEN active_users END), 1) END AS m1,
       CASE WHEN first_idx + 2 <= last_idx THEN ROUND(100.0 * COALESCE(SUM(CASE WHEN months_since = 2 THEN active_users END), 0) / SUM(CASE WHEN months_since = 0 THEN active_users END), 1) END AS m2,
       CASE WHEN first_idx + 3 <= last_idx THEN ROUND(100.0 * COALESCE(SUM(CASE WHEN months_since = 3 THEN active_users END), 0) / SUM(CASE WHEN months_since = 0 THEN active_users END), 1) END AS m3
FROM counts, last
GROUP BY first_idx
ORDER BY first_idx
```

**pandas answer:** `pivot_table(... aggfunc='nunique')`, then `fillna(0).div(counts[0], axis=0)` to divide each row by its own month-0 count, then `.where(observed)` to put NaN back where the month has not happened.
```py
orders["order_ts"] = pd.to_datetime(orders["order_ts"])
orders["ym"] = orders["order_ts"].dt.to_period("M")
orders["cohort"] = orders.groupby("user_id")["ym"].transform("min")
orders["k"] = (orders["ym"].dt.year - orders["cohort"].dt.year) * 12 + (orders["ym"].dt.month - orders["cohort"].dt.month)
counts = orders.pivot_table(index="cohort", columns="k", values="user_id", aggfunc="nunique").reindex(columns=range(4))
last = orders["ym"].max()
observed = pd.DataFrame({k: (counts.index + k) <= last for k in range(4)}, index=counts.index)
pct = counts.fillna(0).div(counts[0], axis=0).mul(100).round(1).where(observed)
pd_df = pct.rename(columns=lambda k: f"m{k}").rename_axis(columns=None).reset_index()
pd_df.insert(1, "cohort_size", counts[0].astype(int).to_numpy())
pd_df["cohort_month"] = pd_df.pop("cohort").astype(str)
pd_df = pd_df[["cohort_month", "cohort_size", "m0", "m1", "m2", "m3"]]
```

**Example:** Last loaded month is 2024-02.
- Cohort 2023-11 (size 2): offset 1 = 1 user = 50.0, offset 2 = 1 user = 50.0, offset 3 = 1 user = 50.0 (February is observed). Row: 100, 50, 50, 50.
- Cohort 2023-12 (size 2): offset 1 (Jan) = user 3 = 50.0; offset 2 (Feb) has no row because nobody was active, but February is loaded, so it is 0.0; offset 3 would be March, not loaded, so NULL. Row: 100, 50, 0, NULL.
- Cohort 2024-01 (size 1): offset 1 (Feb) = user 5 = 100.0; offsets 2 and 3 are NULL. Row: 100, 100, NULL, NULL.
- Partial month: reload the same data only up to 5 February and the January cohort's m1 becomes 0.0 instead of 100.0, because user 5's 11 February order has not landed yet.

**Code:** run with `python3 -I`.
```python
# Q11: cohort retention percentage, the triangle (NULL = not yet observed, 0 = observed and nobody came back)
# Convention: months are calendar months of the naive timestamp (no time zone); the last loaded month is taken from the data.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT);
INSERT INTO orders VALUES
 (1,1,'2023-11-05 10:00:00'),(2,1,'2023-11-25 09:00:00'),(3,1,'2023-12-20 18:00:00'),(4,1,'2024-01-10 08:00:00'),
 (5,2,'2023-11-15 12:00:00'),(6,2,'2024-02-02 13:00:00'),
 (7,3,'2023-12-03 11:00:00'),(8,3,'2024-01-04 16:00:00'),(9,3,'2024-01-18 17:00:00'),
 (10,4,'2023-12-12 14:00:00'),
 (11,5,'2024-01-09 10:30:00'),(12,5,'2024-02-11 15:45:00');
CREATE TABLE orders_snap AS SELECT * FROM orders WHERE order_ts < '2024-02-06';  -- same data loaded only to 5 Feb
"""
SQL_MAIN = """
WITH o AS (
  SELECT user_id, CAST(strftime('%Y', order_ts) AS INTEGER) * 12 + CAST(strftime('%m', order_ts) AS INTEGER) AS idx
  FROM orders
),
last AS (SELECT MAX(idx) AS last_idx FROM o),
c AS (SELECT user_id, MIN(idx) AS first_idx FROM o GROUP BY user_id),
counts AS (
  SELECT c.first_idx, o.idx - c.first_idx AS months_since, COUNT(DISTINCT o.user_id) AS active_users
  FROM o JOIN c ON c.user_id = o.user_id
  GROUP BY c.first_idx, o.idx - c.first_idx
)
SELECT printf('%04d-%02d', (first_idx - 1) / 12, (first_idx - 1) % 12 + 1) AS cohort_month,
       SUM(CASE WHEN months_since = 0 THEN active_users END) AS cohort_size,
       CASE WHEN first_idx + 0 <= last_idx THEN ROUND(100.0 * COALESCE(SUM(CASE WHEN months_since = 0 THEN active_users END), 0) / SUM(CASE WHEN months_since = 0 THEN active_users END), 1) END AS m0,
       CASE WHEN first_idx + 1 <= last_idx THEN ROUND(100.0 * COALESCE(SUM(CASE WHEN months_since = 1 THEN active_users END), 0) / SUM(CASE WHEN months_since = 0 THEN active_users END), 1) END AS m1,
       CASE WHEN first_idx + 2 <= last_idx THEN ROUND(100.0 * COALESCE(SUM(CASE WHEN months_since = 2 THEN active_users END), 0) / SUM(CASE WHEN months_since = 0 THEN active_users END), 1) END AS m2,
       CASE WHEN first_idx + 3 <= last_idx THEN ROUND(100.0 * COALESCE(SUM(CASE WHEN months_since = 3 THEN active_users END), 0) / SUM(CASE WHEN months_since = 0 THEN active_users END), 1) END AS m3
FROM counts, last
GROUP BY first_idx
ORDER BY first_idx
"""
SQL_SNAP = SQL_MAIN.replace("FROM orders", "FROM orders_snap")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("full load through 2024-02:")
print(sql_df.to_string(index=False))
print("same orders, loaded only to 2024-02-05 (partial current month):")
print(pd.read_sql_query(SQL_SNAP, con).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
orders["order_ts"] = pd.to_datetime(orders["order_ts"])
orders["ym"] = orders["order_ts"].dt.to_period("M")
orders["cohort"] = orders.groupby("user_id")["ym"].transform("min")
orders["k"] = (orders["ym"].dt.year - orders["cohort"].dt.year) * 12 + (orders["ym"].dt.month - orders["cohort"].dt.month)
counts = orders.pivot_table(index="cohort", columns="k", values="user_id", aggfunc="nunique").reindex(columns=range(4))
last = orders["ym"].max()
observed = pd.DataFrame({k: (counts.index + k) <= last for k in range(4)}, index=counts.index)
pct = counts.fillna(0).div(counts[0], axis=0).mul(100).round(1).where(observed)
pd_df = pct.rename(columns=lambda k: f"m{k}").rename_axis(columns=None).reset_index()
pd_df.insert(1, "cohort_size", counts[0].astype(int).to_numpy())
pd_df["cohort_month"] = pd_df.pop("cohort").astype(str)
pd_df = pd_df[["cohort_month", "cohort_size", "m0", "m1", "m2", "m3"]]
# pd:end
# compared in cohort_month order; NaN (pandas) equals NULL (SQL)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas == SQL")
print("raw div without fillna/where (NaN everywhere, cannot tell 0 from not-yet):")
print(counts.div(counts[0], axis=0).mul(100).round(1).to_string())
print("asserts passed")
```

**Output (my run):**
```text
full load through 2024-02:
cohort_month  cohort_size    m0    m1   m2   m3
     2023-11            2 100.0  50.0 50.0 50.0
     2023-12            2 100.0  50.0  0.0  NaN
     2024-01            1 100.0 100.0  NaN  NaN
same orders, loaded only to 2024-02-05 (partial current month):
cohort_month  cohort_size    m0   m1   m2   m3
     2023-11            2 100.0 50.0 50.0 50.0
     2023-12            2 100.0 50.0  0.0  NaN
     2024-01            1 100.0  0.0  NaN  NaN
pandas == SQL
raw div without fillna/where (NaN everywhere, cannot tell 0 from not-yet):
k            0      1     2     3
cohort                           
2023-11  100.0   50.0  50.0  50.0
2023-12  100.0   50.0   NaN   NaN
2024-01  100.0  100.0   NaN   NaN
asserts passed
```

**Edge cases:**
- NULL versus 0: `SUM(CASE WHEN months_since = 2 THEN ... END)` on a cohort with no offset-2 row returns NULL, which looks the same as 'not yet' unless you guard with the observed test and `COALESCE`. In the raw pandas division, the real zero (cohort 2023-12, m2) and the not-yet cell are both NaN; I used `fillna(0)` then `where(observed)`.
- The triangle is the normal shape: later cohorts have fewer observed months. Do not average a column across cohorts as if every cohort contributed, and do not plot the NULLs as 0.
- Partial current month: the latest column understates retention because the month is incomplete (January cohort m1 fell from 100.0 to 0.0 in the snapshot). Report the latest month only when it is closed, or label it incomplete.
- Cohort size zero: a cohort with no month-0 users cannot exist here (the cohort is defined by activity); with signup cohorts it can, so guard the division with `NULLIF`.
- Small cohorts: a size-1 cohort goes from 0 to 100 percent on one user; show the counts next to the percentages.

**Then explain:**
- Cohort size is the denominator and it must not change with the column: month-0 active users, not the number active in month k.
- Conditional aggregation pivots rows into columns in standard SQL; SQLite has no `PIVOT`. The column list (`m0` to `m3`) is fixed in the text; a different number of columns needs different SQL or a pandas pivot.
- pandas: `div(axis=0)` aligns by row, so each cohort is divided by its own first column; the default `div` aligns on columns and would give NaN.
- Other engines (not executed here): Snowflake and SQL Server have `PIVOT`, PostgreSQL has `FILTER (WHERE ...)` on aggregates; conditional aggregation as written is the portable version.

**Follow-ups:**
- *Why is the last diagonal NULL?* Those months have not happened; they are unobserved, not zero.
- *What if the month is still running?* Exclude it or flag it as partial.
- *Weighted average retention across cohorts?* Sum of active users over sum of cohort sizes for the cohorts observed at that offset.

**Common mistakes:**
- Showing NULL months as 0 (or real zeros as blank).
- Dividing by the active users of the same month instead of the month-0 count.
- Using `div` without `axis=0`.
- Reporting the incomplete last month as if it were final.

### Q12 ⭐⭐⭐ 🟡 Day-1 retention (the LeetCode 550 pattern, Game Play Analysis IV): activity(player_id, device_id, event_date, games_played), fraction of players who logged in again on the day after their first login, rounded to 2 decimals. Write it with a first-login CTE and a join on date(first_login, '+1 day') = event_date, counting distinct players, with denominator all players. Show the common wrong answers (counting rows instead of players, counting any later login, dividing by logins). Give the pandas version (groupby transform('min'), merge, nunique).
**Asked at:** public LeetCode-style problem bank (550 Game Play Analysis IV, 1193 Monthly Transactions I, 197 Rising Temperature and 262 Trips and Users known from search snippets and third-party write-ups, statements not opened), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Find each player's first login, join back to `activity` on exactly `date(first_login, '+1 day')`, count distinct players who matched, and divide by all players (not by rows and not by logins), then round to 2 decimals.

**Schema and sample data:** twelve rows, five players. Dates are ISO text. Player 1 and player 3 each have two rows on their day-1 date (two devices), player 2 returns on day 4 not day 1, player 4 never returns, player 5 first logs in on 29 Feb 2024 and returns on 1 Mar (leap day boundary).
```sql
CREATE TABLE activity(player_id INTEGER, device_id INTEGER, event_date TEXT, games_played INTEGER);
INSERT INTO activity VALUES
 (1,2,'2024-03-01',5),(1,2,'2024-03-02',6),(1,3,'2024-03-02',1),(1,2,'2024-05-02',4),
 (2,3,'2024-03-05',1),(2,3,'2024-03-09',2),
 (3,1,'2024-03-02',0),(3,1,'2024-03-03',4),(3,4,'2024-03-03',2),
 (4,4,'2024-03-10',3),
 (5,1,'2024-02-29',2),(5,1,'2024-03-01',7);
```

**SQL answer:** `SQL_MAIN` in the Code block (first-login CTE, then a LEFT JOIN so players with no day-1 row stay in the denominator):
```sql
WITH fl AS (
  SELECT player_id, MIN(event_date) AS first_login
  FROM activity
  GROUP BY player_id
)
SELECT ROUND(1.0 * COUNT(DISTINCT a.player_id) / (SELECT COUNT(*) FROM fl), 2) AS fraction
FROM fl
LEFT JOIN activity a
  ON a.player_id = fl.player_id
 AND a.event_date = date(fl.first_login, '+1 day')
```
The three wrong answers are in the Code block as `SQL_ROWS` (`COUNT(a.player_id)` counts rows), `SQL_ANY_LATER` (`a.event_date > fl.first_login`) and `SQL_PER_LOGIN` (denominator `COUNT(*)` of `activity`).

**pandas answer:** same logic, shown once here and identical to the Code block:
```py
a = activity.assign(event_date=pd.to_datetime(activity["event_date"]))
a["first_login"] = a.groupby("player_id")["event_date"].transform("min")
day1 = a[a["event_date"] == a["first_login"] + pd.Timedelta(days=1)]
pd_val = round(day1["player_id"].nunique() / a["player_id"].nunique(), 2)
```

**Example:** first logins: P1 03-01, P2 03-05, P3 03-02, P4 03-10, P5 02-29.
- P1: day 1 is 03-02, there are two rows that day (devices 2 and 3), so P1 is retained (and produces two joined rows).
- P2: day 1 is 03-06, no row (the 03-09 login is day 4). Not retained.
- P3: day 1 is 03-03, two rows. Retained.
- P4: day 1 is 03-11, no row. Not retained.
- P5: `date('2024-02-29', '+1 day')` is 2024-03-01, which exists. Retained.
- 3 retained players out of 5 players = 0.6.

**Code:** run with `python3 -I`. The assert compares two scalars, so there is no row order to fix.
```python
# Q12: Day-1 retention (LeetCode 550 pattern): SQL first-login CTE + join, wrong answers, pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE activity(player_id INTEGER, device_id INTEGER, event_date TEXT, games_played INTEGER);
INSERT INTO activity VALUES
 (1,2,'2024-03-01',5),(1,2,'2024-03-02',6),(1,3,'2024-03-02',1),(1,2,'2024-05-02',4),
 (2,3,'2024-03-05',1),(2,3,'2024-03-09',2),
 (3,1,'2024-03-02',0),(3,1,'2024-03-03',4),(3,4,'2024-03-03',2),
 (4,4,'2024-03-10',3),
 (5,1,'2024-02-29',2),(5,1,'2024-03-01',7);
"""
SQL_MAIN = """
WITH fl AS (
  SELECT player_id, MIN(event_date) AS first_login
  FROM activity
  GROUP BY player_id
)
SELECT ROUND(1.0 * COUNT(DISTINCT a.player_id) / (SELECT COUNT(*) FROM fl), 2) AS fraction
FROM fl
LEFT JOIN activity a
  ON a.player_id = fl.player_id
 AND a.event_date = date(fl.first_login, '+1 day')
"""
SQL_ROWS = """
WITH fl AS (SELECT player_id, MIN(event_date) AS first_login FROM activity GROUP BY player_id)
SELECT ROUND(1.0 * COUNT(a.player_id) / (SELECT COUNT(*) FROM fl), 2)
FROM fl LEFT JOIN activity a
  ON a.player_id = fl.player_id AND a.event_date = date(fl.first_login, '+1 day')
"""
SQL_ANY_LATER = """
WITH fl AS (SELECT player_id, MIN(event_date) AS first_login FROM activity GROUP BY player_id)
SELECT ROUND(1.0 * COUNT(DISTINCT a.player_id) / (SELECT COUNT(*) FROM fl), 2)
FROM fl LEFT JOIN activity a
  ON a.player_id = fl.player_id AND a.event_date > fl.first_login
"""
SQL_PER_LOGIN = """
WITH fl AS (SELECT player_id, MIN(event_date) AS first_login FROM activity GROUP BY player_id)
SELECT ROUND(1.0 * COUNT(DISTINCT a.player_id) / (SELECT COUNT(*) FROM activity), 2)
FROM fl LEFT JOIN activity a
  ON a.player_id = fl.player_id AND a.event_date = date(fl.first_login, '+1 day')
"""
SQL_WHO = """
WITH fl AS (SELECT player_id, MIN(event_date) AS first_login FROM activity GROUP BY player_id)
SELECT fl.player_id, fl.first_login, date(fl.first_login, '+1 day') AS next_day,
       COUNT(a.player_id) AS rows_on_next_day
FROM fl LEFT JOIN activity a
  ON a.player_id = fl.player_id AND a.event_date = date(fl.first_login, '+1 day')
GROUP BY fl.player_id ORDER BY fl.player_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_val = con.execute(SQL_MAIN).fetchone()[0]
print("SQL day-1 retention:", sql_val)
print("wrong 1, count rows not players:", con.execute(SQL_ROWS).fetchone()[0])
print("wrong 2, any later login:", con.execute(SQL_ANY_LATER).fetchone()[0])
print("wrong 3, divide by login rows:", con.execute(SQL_PER_LOGIN).fetchone()[0])
print(pd.read_sql_query(SQL_WHO, con).to_string(index=False))

activity = pd.read_sql_query("SELECT * FROM activity", con)
# pd:main
a = activity.assign(event_date=pd.to_datetime(activity["event_date"]))
a["first_login"] = a.groupby("player_id")["event_date"].transform("min")
day1 = a[a["event_date"] == a["first_login"] + pd.Timedelta(days=1)]
pd_val = round(day1["player_id"].nunique() / a["player_id"].nunique(), 2)
# pd:end
print("pandas day-1 retention:", pd_val)
assert pd_val == sql_val  # scalar, no row order involved
# the same pandas result through an explicit merge of first logins back to activity
fl = a.groupby("player_id", as_index=False)["event_date"].min().rename(columns={"event_date": "first_login"})
m = fl.merge(a[["player_id", "event_date"]], on="player_id", how="left")
m_hit = m[m["event_date"] == m["first_login"] + pd.Timedelta(days=1)]
assert round(m_hit["player_id"].nunique() / len(fl), 2) == sql_val

# edge: empty table
con.execute("DELETE FROM activity")
print("empty table, SQL:", con.execute(SQL_MAIN).fetchone()[0])
try:
    print(round(a.iloc[0:0]["player_id"].nunique() / a.iloc[0:0]["player_id"].nunique(), 2))
except ZeroDivisionError as e:
    print("empty table, pandas: ZeroDivisionError:", e)
print("asserts passed")
```

**Output (my run):**
```text
SQL day-1 retention: 0.6
wrong 1, count rows not players: 1.0
wrong 2, any later login: 0.8
wrong 3, divide by login rows: 0.25
 player_id first_login   next_day  rows_on_next_day
         1  2024-03-01 2024-03-02                 2
         2  2024-03-05 2024-03-06                 0
         3  2024-03-02 2024-03-03                 2
         4  2024-03-10 2024-03-11                 0
         5  2024-02-29 2024-03-01                 1
pandas day-1 retention: 0.6
empty table, SQL: None
empty table, pandas: ZeroDivisionError: division by zero
asserts passed
```

**Edge cases:**
- Wrong answer 1, counting rows: players 1 and 3 each have two rows on day 1, so `COUNT(a.player_id)` gives 5 matched rows over 5 players, which is 1.0 in my run. Duplicate rows per player-day are normal when `device_id` is in the key, so always `COUNT(DISTINCT player_id)`.
- Wrong answer 2, any later login: players 1, 2, 3 and 5 all logged in again at some point, so 0.8 in my run. That is a different metric (ever came back), not day 1.
- Wrong answer 3, dividing by login rows: the denominator is 12 rows instead of 5 players, so 3/12 = 0.25 in my run. The denominator is players.
- First login is per player, not per player and device. A player who first used device 2 on day 1 and device 3 on day 2 is still day-1 retained.
- Empty table: SQLite returns NULL (division by zero gives NULL), but the pandas expression raised `ZeroDivisionError` in my run. Guard the denominator if the table can be empty.
- A player whose first login is the last date in the data cannot have returned yet. The LeetCode problem ignores that; in production you would drop such players from the denominator (the immature-cohort trap, Q13).
- Dates must be ISO `YYYY-MM-DD` text. `date()` returns NULL for anything else, and then the join silently matches nothing.

**Then explain:**
- Day 1 means the calendar day after the first login date, not 24 hours later. With dates (no times) the join key `date(first_login, '+1 day')` expresses that exactly and handles month ends and leap days.
- LEFT JOIN from the first-login CTE keeps never-returning players, so `COUNT(DISTINCT a.player_id)` ignores their NULLs but the denominator subquery still counts them.
- ROUND in SQLite returns a float, so the result prints `0.6`, not `0.60`; if the platform needs two decimals as text, format it at the edge.
- The same pattern generalises: replace `'+1 day'` by `'+7 days'` for exact day-7 (classic) retention; the other definitions are in Q13.
- Dialects (not executed here): MySQL uses `DATE_ADD(first_login, INTERVAL 1 DAY)` or `DATEDIFF(event_date, first_login) = 1`; PostgreSQL uses `first_login + 1` for a `DATE` or `+ INTERVAL '1 day'`. The LeetCode statement is, as I remember it, written for MySQL; I did not open the page.

**Follow-ups:**
- Day 7 instead of day 1? Change the offset, and exclude players whose first login is within 7 days of the as-of date.
- Per cohort day instead of one number? `GROUP BY first_login` and divide per group (Q13).
- Without a CTE? A correlated `EXISTS` on `date(MIN(...), '+1 day')` works, but the CTE reads better.

**Common mistakes:**
- Counting rows or dividing by rows (shown above: 1.0 and 0.25 instead of 0.6).
- Using `a.event_date > first_login` and calling it day 1.
- Taking `MIN(event_date)` per player and device.
- INNER JOIN, which silently shrinks the denominator to returners only, so the ratio is 1 by construction.
- Hard-coding 365 or 24-hour arithmetic instead of calendar-day arithmetic.

### Q13 ⭐⭐⭐ 🟡 Day-N retention definitions: logins(user_id, login_date) and users(user_id, signup_date). Compute day 1, day 7 and day 30 retention per signup-date cohort three ways, classic (logged in exactly on day N), cumulative (any login from day 1 through N) and rolling (on or after day N), and show on a small table that the three numbers differ and that rolling is unbounded and keeps rising. Explain why a cohort that signed up less than N days ago must be excluded or marked immature (the denominator trap) and which definition to state before writing code.
**Asked at:** retention-definition guides seen as search snippets (GoPractice day-N versus rolling retention, Linkrunner glossary, Metricgate retention curves; not opened): classic day N, cumulative within N days, rolling on-or-after N; guides and not candidate reports; product analyst and data scientist screens
**Say this first (1 line):** Before any code, state the definition: classic day N is "logged in exactly on day N after signup", cumulative is "at least once on days 1 through N", rolling is "on day N or any day after", and a cohort younger than N days is marked immature (NULL), not 0%.

**Schema and sample data:** eight users in three signup-date cohorts, ten logins, and a fixed as-of date of 2024-02-15 (never today, so the run is repeatable). Day offset = login date minus signup date in whole days. Time zone: dates are plain calendar dates with no time zone conversion; weeks do not appear in this question.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1,'2024-01-01'),(2,'2024-01-01'),(3,'2024-01-01'),(4,'2024-01-01'),
  (5,'2024-01-02'),(6,'2024-01-02'),(7,'2024-02-10'),(8,'2024-02-10');
INSERT INTO logins VALUES
 (1,'2024-01-02'),(1,'2024-01-08'),(1,'2024-01-31'),
 (2,'2024-01-02'),(2,'2024-01-05'),
 (3,'2024-01-04'),
 (4,'2024-02-10'),
 (5,'2024-01-09'),(5,'2024-01-03'),
 (7,'2024-02-11');
```

**SQL answer:** one query for all three definitions and N in (1, 7, 30), parameterised by `:as_of`; the maturity test `date(signup_date, '+N days') > :as_of` turns the cell into NULL. It is `SQL_MAIN` in the Code block:
```sql
WITH ns(n) AS (VALUES (1),(7),(30)),
size AS (
  SELECT signup_date, COUNT(*) AS cohort_size FROM users GROUP BY signup_date
),
d AS (
  SELECT u.user_id, u.signup_date,
         CAST(ROUND(julianday(l.login_date) - julianday(u.signup_date)) AS INTEGER) AS dn
  FROM users u
  LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date <= :as_of
)
SELECT s.signup_date, ns.n AS day_n, s.cohort_size,
  CASE WHEN date(s.signup_date, '+' || ns.n || ' days') > :as_of THEN NULL
       ELSE ROUND(100.0 * COUNT(DISTINCT CASE WHEN d.dn = ns.n THEN d.user_id END) / s.cohort_size, 1)
  END AS classic_pct,
  CASE WHEN date(s.signup_date, '+' || ns.n || ' days') > :as_of THEN NULL
       ELSE ROUND(100.0 * COUNT(DISTINCT CASE WHEN d.dn BETWEEN 1 AND ns.n THEN d.user_id END) / s.cohort_size, 1)
  END AS cumulative_pct,
  CASE WHEN date(s.signup_date, '+' || ns.n || ' days') > :as_of THEN NULL
       ELSE ROUND(100.0 * COUNT(DISTINCT CASE WHEN d.dn >= ns.n THEN d.user_id END) / s.cohort_size, 1)
  END AS rolling_pct
FROM size s
CROSS JOIN ns
JOIN d ON d.signup_date = s.signup_date
GROUP BY s.signup_date, ns.n
ORDER BY s.signup_date, ns.n
```

**pandas answer:** identical to the function in the Code block (shown once here):
```py
def day_n_table(users, logins, as_of):
    as_of_ts = pd.Timestamp(as_of)
    u = users.assign(signup_date=pd.to_datetime(users["signup_date"]))
    l = logins.assign(login_date=pd.to_datetime(logins["login_date"]))
    l = l[l["login_date"] <= as_of_ts]
    d = u.merge(l, on="user_id", how="left")
    d["dn"] = (d["login_date"] - d["signup_date"]).dt.days
    rows = []
    for cohort in sorted(u["signup_date"].unique()):
        g = d[d["signup_date"] == cohort]
        size = u[u["signup_date"] == cohort]["user_id"].nunique()
        for n in (1, 7, 30):
            mature = cohort + pd.Timedelta(days=n) <= as_of_ts
            def pct(mask):
                return round(100.0 * g.loc[mask, "user_id"].nunique() / size, 1) if mature else float("nan")
            rows.append({"signup_date": cohort.strftime("%Y-%m-%d"), "day_n": n, "cohort_size": size,
                         "classic_pct": pct(g["dn"] == n),
                         "cumulative_pct": pct(g["dn"].between(1, n)),
                         "rolling_pct": pct(g["dn"] >= n)})
    return pd.DataFrame(rows)
```

**Example:** cohort 2024-01-01 has users 1 to 4. Day offsets: user 1 logs in on days 1, 7, 30; user 2 on days 1 and 4; user 3 on day 3; user 4 on day 40.
- Classic day 1: users 1 and 2, 2 of 4 = 50.0. Classic day 7: only user 1 (01-08), 25.0. Classic day 30: user 1 (01-31), 25.0.
- Cumulative day 7 (days 1 to 7): users 1, 2, 3 = 75.0. Cumulative day 30: still users 1, 2, 3 (user 4 is on day 40) = 75.0.
- Rolling day 1 (day 1 or later): all four users = 100.0. Rolling day 7: users 1 (days 7 and 30) and 4 (day 40) = 50.0.
- Cohort 2024-02-10: day 1 is mature (02-11 is on or before 02-15), user 7 logged in, 50.0. Day 7 would need data through 02-17, so it is NULL, not 0.

**Code:** run with `python3 -I`. The pandas table is compared to the SQL table after sorting by `signup_date`, `day_n` (NaN compares equal to NaN in `assert_frame_equal`).
```python
# Q13: Day-N retention per signup-date cohort: classic, cumulative, rolling, with maturity check
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1,'2024-01-01'),(2,'2024-01-01'),(3,'2024-01-01'),(4,'2024-01-01'),
  (5,'2024-01-02'),(6,'2024-01-02'),(7,'2024-02-10'),(8,'2024-02-10');
INSERT INTO logins VALUES
 (1,'2024-01-02'),(1,'2024-01-08'),(1,'2024-01-31'),
 (2,'2024-01-02'),(2,'2024-01-05'),
 (3,'2024-01-04'),
 (4,'2024-02-10'),
 (5,'2024-01-09'),(5,'2024-01-03'),
 (7,'2024-02-11');
"""
SQL_MAIN = """
WITH ns(n) AS (VALUES (1),(7),(30)),
size AS (
  SELECT signup_date, COUNT(*) AS cohort_size FROM users GROUP BY signup_date
),
d AS (
  SELECT u.user_id, u.signup_date,
         CAST(ROUND(julianday(l.login_date) - julianday(u.signup_date)) AS INTEGER) AS dn
  FROM users u
  LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date <= :as_of
)
SELECT s.signup_date, ns.n AS day_n, s.cohort_size,
  CASE WHEN date(s.signup_date, '+' || ns.n || ' days') > :as_of THEN NULL
       ELSE ROUND(100.0 * COUNT(DISTINCT CASE WHEN d.dn = ns.n THEN d.user_id END) / s.cohort_size, 1)
  END AS classic_pct,
  CASE WHEN date(s.signup_date, '+' || ns.n || ' days') > :as_of THEN NULL
       ELSE ROUND(100.0 * COUNT(DISTINCT CASE WHEN d.dn BETWEEN 1 AND ns.n THEN d.user_id END) / s.cohort_size, 1)
  END AS cumulative_pct,
  CASE WHEN date(s.signup_date, '+' || ns.n || ' days') > :as_of THEN NULL
       ELSE ROUND(100.0 * COUNT(DISTINCT CASE WHEN d.dn >= ns.n THEN d.user_id END) / s.cohort_size, 1)
  END AS rolling_pct
FROM size s
CROSS JOIN ns
JOIN d ON d.signup_date = s.signup_date
GROUP BY s.signup_date, ns.n
ORDER BY s.signup_date, ns.n
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
AS_OF = "2024-02-15"
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"as_of": AS_OF})
print("as of", AS_OF)
print(sql_df.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
logins = pd.read_sql_query("SELECT * FROM logins", con)

# pd:main
def day_n_table(users, logins, as_of):
    as_of_ts = pd.Timestamp(as_of)
    u = users.assign(signup_date=pd.to_datetime(users["signup_date"]))
    l = logins.assign(login_date=pd.to_datetime(logins["login_date"]))
    l = l[l["login_date"] <= as_of_ts]
    d = u.merge(l, on="user_id", how="left")
    d["dn"] = (d["login_date"] - d["signup_date"]).dt.days
    rows = []
    for cohort in sorted(u["signup_date"].unique()):
        g = d[d["signup_date"] == cohort]
        size = u[u["signup_date"] == cohort]["user_id"].nunique()
        for n in (1, 7, 30):
            mature = cohort + pd.Timedelta(days=n) <= as_of_ts
            def pct(mask):
                return round(100.0 * g.loc[mask, "user_id"].nunique() / size, 1) if mature else float("nan")
            rows.append({"signup_date": cohort.strftime("%Y-%m-%d"), "day_n": n, "cohort_size": size,
                         "classic_pct": pct(g["dn"] == n),
                         "cumulative_pct": pct(g["dn"].between(1, n)),
                         "rolling_pct": pct(g["dn"] >= n)})
    return pd.DataFrame(rows)
# pd:end

pd_df = day_n_table(users, logins, AS_OF)
# compared after sorting by signup_date, day_n (already in that order); NaN equals NaN here
pd.testing.assert_frame_equal(pd_df.sort_values(["signup_date", "day_n"]).reset_index(drop=True),
                              sql_df.sort_values(["signup_date", "day_n"]).reset_index(drop=True),
                              check_dtype=False)
print("pandas equals SQL")

# rolling is unbounded: same cohort and N, earlier as-of date
early = pd.read_sql_query(SQL_MAIN, con, params={"as_of": "2024-01-20"})
print("as of 2024-01-20, cohort 2024-01-01, day 7 and day 30:")
print(early[(early.signup_date == "2024-01-01") & early.day_n.isin([7, 30])].to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
as of 2024-02-15
signup_date  day_n  cohort_size  classic_pct  cumulative_pct  rolling_pct
 2024-01-01      1            4         50.0            50.0        100.0
 2024-01-01      7            4         25.0            75.0         50.0
 2024-01-01     30            4         25.0            75.0         50.0
 2024-01-02      1            2         50.0            50.0         50.0
 2024-01-02      7            2         50.0            50.0         50.0
 2024-01-02     30            2          0.0            50.0          0.0
 2024-02-10      1            2         50.0            50.0         50.0
 2024-02-10      7            2          NaN             NaN          NaN
 2024-02-10     30            2          NaN             NaN          NaN
pandas equals SQL
as of 2024-01-20, cohort 2024-01-01, day 7 and day 30:
signup_date  day_n  cohort_size  classic_pct  cumulative_pct  rolling_pct
 2024-01-01      7            4         25.0            75.0         25.0
 2024-01-01     30            4          NaN             NaN          NaN
asserts passed
```

**Edge cases:**
- The three numbers differ on the same data (cohort 2024-01-01, day 7: 25.0, 75.0, 50.0). Cumulative is never below classic; rolling is not comparable with either.
- Rolling is unbounded: the same cohort and N gave 25.0 at as-of 2024-01-20 and 50.0 at as-of 2024-02-15, because user 4's login on day 40 arrived later. Classic day 7 stayed 25.0 in both runs. A rolling number therefore changes as time passes, which is why it cannot be reported for a young cohort.
- Day 30 for cohort 2024-01-02 is 0.0 classic and rolling (mature, nobody came back on day 30 or later) but 50.0 cumulative, a mature zero versus a NULL immature cell. Do not fill NULL with 0.
- Users with no logins at all (user 6, user 8) stay in the denominator through the LEFT JOIN. With an INNER JOIN the cohort size shrinks and every percentage inflates.
- Logins dated on or before the signup date (none in my sample, so not run) would give offset 0 or negative, which falls outside every window above; check for them in real data, they usually mean a bad signup date.
- Login timestamps with a time part would make `julianday` differences fractional; take `date()` of both sides first.

**Then explain:**
- Day offsets here are `ROUND(julianday(login) - julianday(signup))` cast to integer; with plain dates the difference is already whole, and rounding guards against timestamp inputs.
- Denominator trap: a cohort that signed up fewer than N days before the as-of date cannot have had a day-N, so the cell is NULL (or the cohort is excluded). Putting 0 there drags the retention curve down and looks like a product problem.
- Which definition to state first: ask what the business decision is. Classic matches "come back on the 7th day" push-notification thinking; cumulative matches "came back within a week"; rolling matches "still around after day N" and is the only one that is unbounded.
- Cohort by signup date is noisy when cohorts are small (two users here); real work usually groups to week or month cohorts (see Q10 and Q11 for month cohorts).
- Dialects (not executed here): `julianday` becomes `DATEDIFF(login_date, signup_date)` in MySQL, `login_date - signup_date` in PostgreSQL for `DATE` columns, and `DATE_DIFF` in BigQuery; the argument order of `DATEDIFF` differs between engines, so check the manual.

**Follow-ups:**
- Which one would you report on a dashboard? The one the stakeholder defined in writing, usually classic for day-1 and day-7, and always with the denominator shown.
- How do you compare two cohorts with different maturity? Only compare cells that are mature in both, or compare on the same day offset.
- Can classic be larger than cumulative? No, on the same N, classic day N is contained in cumulative days 1..N for N >= 1.

**Common mistakes:**
- Not stating the definition, so two people compute different numbers from the same table.
- Filling immature cells with 0.
- Counting login rows rather than distinct users (a user can log in twice on day 7).
- Using INNER JOIN so non-returning users vanish from the denominator.
- Treating rolling retention as comparable to classic retention.

### Q14 ⭐⭐⭐ 🟡 New versus returning customers per month: orders(order_id, user_id, order_ts, amount). For each month return the count of distinct customers whose first order ever falls in that month (new) and those who ordered in that month but had an earlier first order (returning), plus revenue split. Compare with a version using NOT EXISTS on earlier orders, and the pandas version with transform('min') on the order date and np.where. State what happens to a customer who orders twice in their first month.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Find each customer's first-order month once, then for every order compare its month with that first month: equal means the customer is new in that month, later means returning; count distinct customers and sum revenue under each label.

**Schema and sample data:** five customers over Jan to Mar 2024, ten orders. Customer 1 and customer 3 each order twice in their first month. Months are calendar months of the stored timestamp text (no time zone conversion; the timestamps are treated as already in the reporting zone).
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05 10:00:00',100),(2,1,'2024-01-20 12:00:00',50),(3,1,'2024-02-10 09:00:00',80),
 (4,2,'2024-01-15 15:00:00',200),(5,2,'2024-03-02 11:00:00',60),
 (6,3,'2024-02-03 08:00:00',40),(7,3,'2024-02-25 19:00:00',30),
 (8,4,'2024-03-10 14:00:00',90),
 (9,5,'2024-03-11 10:00:00',10),(10,5,'2024-03-12 10:00:00',20);
```

**SQL answer:** `SQL_MAIN` (first-order CTE plus conditional aggregation) and `SQL_NOT_EXISTS` (customer-level NOT EXISTS on any earlier order before the month start) are both in the Code block. The main one:
```sql
WITH f AS (
  SELECT user_id, MIN(order_ts) AS first_ts FROM orders GROUP BY user_id
),
j AS (
  SELECT o.user_id, o.amount,
         strftime('%Y-%m', o.order_ts) AS month,
         strftime('%Y-%m', f.first_ts) AS first_month
  FROM orders o JOIN f ON f.user_id = o.user_id
)
SELECT month,
       COUNT(DISTINCT CASE WHEN month = first_month THEN user_id END) AS new_customers,
       COUNT(DISTINCT CASE WHEN month > first_month THEN user_id END) AS returning_customers,
       SUM(CASE WHEN month = first_month THEN amount ELSE 0 END) AS new_revenue,
       SUM(CASE WHEN month > first_month THEN amount ELSE 0 END) AS returning_revenue
FROM j
GROUP BY month
ORDER BY month
```

**pandas answer:** identical to the Code block:
```py
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"]))
o["month"] = o["order_ts"].dt.to_period("M")
o["first_month"] = o.groupby("user_id")["order_ts"].transform("min").dt.to_period("M")
o["kind"] = np.where(o["month"] == o["first_month"], "new", "returning")
cust = o.groupby(["month", "kind"])["user_id"].nunique().unstack(fill_value=0)
rev = o.groupby(["month", "kind"])["amount"].sum().unstack(fill_value=0)
cust = cust.reindex(columns=["new", "returning"], fill_value=0)
rev = rev.reindex(columns=["new", "returning"], fill_value=0)
pd_df = pd.DataFrame({"month": cust.index.astype(str),
                      "new_customers": cust["new"].to_numpy(),
                      "returning_customers": cust["returning"].to_numpy(),
                      "new_revenue": rev["new"].to_numpy(),
                      "returning_revenue": rev["returning"].to_numpy()})
```

**Example:** first-order months: customer 1 Jan, 2 Jan, 3 Feb, 4 Mar, 5 Mar.
- January: customers 1 and 2 are new (2). Revenue 100 + 50 + 200 = 350, all new; nobody can be returning yet.
- February: customer 3 is new (first order 02-03), revenue 40 + 30 = 70 (both of their orders). Customer 1 is returning, revenue 80.
- March: customers 4 and 5 are new, revenue 90 + 10 + 20 = 120 (customer 5's two orders both count as new). Customer 2 is returning (first order in January, skipped February), revenue 60.

**Code:** run with `python3 -I`. Frames are compared after ordering by `month` ascending.
```python
# Q14: new vs returning customers per month, NOT EXISTS version, pandas np.where
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05 10:00:00',100),(2,1,'2024-01-20 12:00:00',50),(3,1,'2024-02-10 09:00:00',80),
 (4,2,'2024-01-15 15:00:00',200),(5,2,'2024-03-02 11:00:00',60),
 (6,3,'2024-02-03 08:00:00',40),(7,3,'2024-02-25 19:00:00',30),
 (8,4,'2024-03-10 14:00:00',90),
 (9,5,'2024-03-11 10:00:00',10),(10,5,'2024-03-12 10:00:00',20);
"""
SQL_MAIN = """
WITH f AS (
  SELECT user_id, MIN(order_ts) AS first_ts FROM orders GROUP BY user_id
),
j AS (
  SELECT o.user_id, o.amount,
         strftime('%Y-%m', o.order_ts) AS month,
         strftime('%Y-%m', f.first_ts) AS first_month
  FROM orders o JOIN f ON f.user_id = o.user_id
)
SELECT month,
       COUNT(DISTINCT CASE WHEN month = first_month THEN user_id END) AS new_customers,
       COUNT(DISTINCT CASE WHEN month > first_month THEN user_id END) AS returning_customers,
       SUM(CASE WHEN month = first_month THEN amount ELSE 0 END) AS new_revenue,
       SUM(CASE WHEN month > first_month THEN amount ELSE 0 END) AS returning_revenue
FROM j
GROUP BY month
ORDER BY month
"""
SQL_NOT_EXISTS = """
WITH om AS (
  SELECT user_id, strftime('%Y-%m', order_ts) AS month, SUM(amount) AS revenue
  FROM orders GROUP BY user_id, strftime('%Y-%m', order_ts)
)
SELECT month,
       SUM(CASE WHEN NOT EXISTS (SELECT 1 FROM orders p
                                 WHERE p.user_id = om.user_id AND p.order_ts < month || '-01')
                THEN 1 ELSE 0 END) AS new_customers,
       SUM(CASE WHEN EXISTS (SELECT 1 FROM orders p
                             WHERE p.user_id = om.user_id AND p.order_ts < month || '-01')
                THEN 1 ELSE 0 END) AS returning_customers,
       SUM(CASE WHEN NOT EXISTS (SELECT 1 FROM orders p
                                 WHERE p.user_id = om.user_id AND p.order_ts < month || '-01')
                THEN revenue ELSE 0 END) AS new_revenue,
       SUM(CASE WHEN EXISTS (SELECT 1 FROM orders p
                             WHERE p.user_id = om.user_id AND p.order_ts < month || '-01')
                THEN revenue ELSE 0 END) AS returning_revenue
FROM om
GROUP BY month
ORDER BY month
"""
SQL_ORDER_LEVEL = """
SELECT strftime('%Y-%m', o.order_ts) AS month,
       SUM(CASE WHEN NOT EXISTS (SELECT 1 FROM orders p WHERE p.user_id = o.user_id
                                 AND (p.order_ts < o.order_ts OR (p.order_ts = o.order_ts AND p.order_id < o.order_id)))
                THEN o.amount ELSE 0 END) AS first_order_revenue,
       SUM(CASE WHEN EXISTS (SELECT 1 FROM orders p WHERE p.user_id = o.user_id
                             AND (p.order_ts < o.order_ts OR (p.order_ts = o.order_ts AND p.order_id < o.order_id)))
                THEN o.amount ELSE 0 END) AS later_order_revenue
FROM orders o GROUP BY month ORDER BY month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
ne_df = pd.read_sql_query(SQL_NOT_EXISTS, con)
print("customer-level (first-order month), SQL_MAIN:")
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, ne_df)  # both ordered by month
print("NOT EXISTS version equals SQL_MAIN")
print("order-level split (second order in first month counts as later):")
print(pd.read_sql_query(SQL_ORDER_LEVEL, con).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"]))
o["month"] = o["order_ts"].dt.to_period("M")
o["first_month"] = o.groupby("user_id")["order_ts"].transform("min").dt.to_period("M")
o["kind"] = np.where(o["month"] == o["first_month"], "new", "returning")
cust = o.groupby(["month", "kind"])["user_id"].nunique().unstack(fill_value=0)
rev = o.groupby(["month", "kind"])["amount"].sum().unstack(fill_value=0)
cust = cust.reindex(columns=["new", "returning"], fill_value=0)
rev = rev.reindex(columns=["new", "returning"], fill_value=0)
pd_df = pd.DataFrame({"month": cust.index.astype(str),
                      "new_customers": cust["new"].to_numpy(),
                      "returning_customers": cust["returning"].to_numpy(),
                      "new_revenue": rev["new"].to_numpy(),
                      "returning_revenue": rev["returning"].to_numpy()})
# pd:end
# compared after sorting by month (already ascending)
pd.testing.assert_frame_equal(pd_df.sort_values("month").reset_index(drop=True), sql_df, check_dtype=False)
print("pandas equals SQL")
print(pd_df.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
customer-level (first-order month), SQL_MAIN:
  month  new_customers  returning_customers  new_revenue  returning_revenue
2024-01              2                    0          350                  0
2024-02              1                    1           70                 80
2024-03              2                    1          120                 60
NOT EXISTS version equals SQL_MAIN
order-level split (second order in first month counts as later):
  month  first_order_revenue  later_order_revenue
2024-01                  300                   50
2024-02                   40                  110
2024-03                  100                   80
pandas equals SQL
  month  new_customers  returning_customers  new_revenue  returning_revenue
2024-01              2                    0          350                  0
2024-02              1                    1           70                 80
2024-03              2                    1          120                 60
asserts passed
```

**Edge cases:**
- Customer ordering twice in the first month: counted once as new, and in the customer-level definition both orders' revenue is "new" (customer 1 gave 150 of January's 350, customer 3 gave 70 in February). The new count is a count of customers, not orders.
- The order-level alternative labels only the very first order as new. `SQL_ORDER_LEVEL` in the Code block returned January 300 first-order versus 50 later-order revenue, because customer 1's 01-20 order counts as "later". Same table, different split, so state which one the report means. Two orders with identical timestamps need the `order_id` tie-breaker (included in that query).
- A customer who skips a month (customer 2) is returning in March, not new again. A reactivated customer is returning; separating "returning" from "resurrected" is Q33.
- Customers with no orders never appear. A month with no orders at all does not appear either; add a month spine if the report must show it (Q6).
- Late or back-dated orders can change a customer's first month, which restates old rows (Q35).

**Then explain:**
- The two SQL versions returned identical frames: month-level `NOT EXISTS` asks "did this customer order before this month started", which is the same as `month > first_month`.
- The NOT EXISTS form is a correlated subquery per customer-month; the CTE form scans once. I did not time them on a large table.
- `groupby('user_id')['order_ts'].transform('min')` gives each row its customer's first timestamp; `to_period('M')` makes months comparable, and `np.where` labels the rows.
- `unstack(fill_value=0)` then `reindex(columns=[...], fill_value=0)` guarantees both columns even in a month with no returning customers (January here), where the `returning` column would otherwise be missing if no month had any.

**Follow-ups:**
- Percent new? `new_customers / (new_customers + returning_customers)` per month, guarding zero.
- New by first purchase date not first month (weekly)? Same CTE, bucket to week.
- Only completed orders count? Filter before computing the first order, otherwise a cancelled first order moves the cohort.

**Common mistakes:**
- Counting orders instead of distinct customers.
- Using `MIN(order_ts)` over the filtered month, which makes every customer "new" in every month.
- Labelling the second same-month order as returning without saying so.
- Comparing the full timestamp to a month string, instead of comparing months or `order_ts < month start`.

### Q15 ⭐⭐⭐ 🟡 Active users per month and week: events(user_id, event_ts). Count distinct active users per calendar month (MAU as a plain count, not stickiness; DAU/MAU design is Part 8) and per week starting Monday, one row per period. Explain that a user active in two weeks of the same month counts once per month but twice across the two weekly rows, so weekly counts do not add up to the monthly count, and give the pandas versions with groupby(pd.Grouper(key='event_ts', freq='MS'))['user_id'].nunique() and freq='W-MON'.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Group by the period key and `COUNT(DISTINCT user_id)`: `strftime('%Y-%m', event_ts)` for months and `date(event_ts, 'weekday 0', '-6 days')` for Monday-start weeks; the weekly rows will not add up to the monthly count because a user active in two weeks is counted once per week but only once per month.

**Schema and sample data:** nine events for five users in Jan and early Feb 2024. Convention: weeks start on Monday (2024-01-01 is a Monday); timestamps are used as stored, with no time zone conversion (treated as UTC or whatever one zone the table uses).
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-02 09:00:00'),(1,'2024-01-09 18:30:00'),
 (2,'2024-01-03 10:00:00'),(2,'2024-01-04 11:00:00'),
 (3,'2024-01-10 08:00:00'),(3,'2024-01-31 23:59:59'),
 (4,'2024-01-29 07:00:00'),(4,'2024-02-01 12:00:00'),
 (5,'2024-02-06 13:00:00');
```

**SQL answer:** `SQL_MONTH` and `SQL_WEEK` in the Code block:
```sql
SELECT strftime('%Y-%m', event_ts) AS month, COUNT(DISTINCT user_id) AS active_users
FROM events GROUP BY month ORDER BY month
```
```sql
SELECT date(event_ts, 'weekday 0', '-6 days') AS week_start, COUNT(DISTINCT user_id) AS active_users
FROM events GROUP BY week_start ORDER BY week_start
```
`date(x, 'weekday 0')` moves forward to the next Sunday (or stays if x is a Sunday), then `'-6 days'` lands on that week's Monday.

**pandas answer:** identical to the Code block:
```py
e = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
m_pd = (e.groupby(pd.Grouper(key="event_ts", freq="MS"))["user_id"].nunique()
          .rename("active_users").reset_index())
m_pd["month"] = m_pd["event_ts"].dt.strftime("%Y-%m")
m_pd = m_pd[["month", "active_users"]]
w_pd = (e.groupby(pd.Grouper(key="event_ts", freq="W-MON", closed="left", label="left"))["user_id"].nunique()
          .rename("active_users").reset_index())
w_pd["week_start"] = w_pd["event_ts"].dt.strftime("%Y-%m-%d")
w_pd = w_pd.loc[w_pd["active_users"] > 0, ["week_start", "active_users"]].reset_index(drop=True)
```

**Example:**
- Week starting 01-01: user 1 (01-02) and user 2 (01-03 and 01-04, counted once) = 2.
- Week starting 01-08: user 1 (01-09) and user 3 (01-10) = 2.
- Weeks starting 01-15 and 01-22 have no events, so SQL has no row for them.
- Week starting 01-29 (Mon 01-29 to Sun 02-04): user 3 (01-31) and user 4 (01-29 and 02-01) = 2. This week spans January and February.
- Week starting 02-05: user 5 = 1.
- Months: January = users 1, 2, 3, 4 = 4; February = users 4 (02-01) and 5 = 2.
- Weekly rows that start in January sum to 2 + 2 + 2 = 6, but January MAU is 4: users 1 and 3 each appear in two January weeks. User 4 is counted in January and in February monthly, which is correct, and in a single week.

**Code:** run with `python3 -I`. Both pairs are compared in ascending order of the period label.
```python
# Q15: distinct active users per month and per Monday-start week; Grouper defaults; ISO-year emulation
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-02 09:00:00'),(1,'2024-01-09 18:30:00'),
 (2,'2024-01-03 10:00:00'),(2,'2024-01-04 11:00:00'),
 (3,'2024-01-10 08:00:00'),(3,'2024-01-31 23:59:59'),
 (4,'2024-01-29 07:00:00'),(4,'2024-02-01 12:00:00'),
 (5,'2024-02-06 13:00:00');
"""
SQL_MONTH = """
SELECT strftime('%Y-%m', event_ts) AS month, COUNT(DISTINCT user_id) AS active_users
FROM events GROUP BY month ORDER BY month
"""
SQL_WEEK = """
SELECT date(event_ts, 'weekday 0', '-6 days') AS week_start, COUNT(DISTINCT user_id) AS active_users
FROM events GROUP BY week_start ORDER BY week_start
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
m_sql = pd.read_sql_query(SQL_MONTH, con)
w_sql = pd.read_sql_query(SQL_WEEK, con)
print("SQL monthly:"); print(m_sql.to_string(index=False))
print("SQL weekly (Monday start):"); print(w_sql.to_string(index=False))
print("sum of January-week rows (weeks starting 01-01..01-29):", int(w_sql[w_sql.week_start < "2024-02-01"].active_users.sum()),
      "vs January MAU:", int(m_sql.loc[m_sql.month == "2024-01", "active_users"].iloc[0]))

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
e = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
m_pd = (e.groupby(pd.Grouper(key="event_ts", freq="MS"))["user_id"].nunique()
          .rename("active_users").reset_index())
m_pd["month"] = m_pd["event_ts"].dt.strftime("%Y-%m")
m_pd = m_pd[["month", "active_users"]]
w_pd = (e.groupby(pd.Grouper(key="event_ts", freq="W-MON", closed="left", label="left"))["user_id"].nunique()
          .rename("active_users").reset_index())
w_pd["week_start"] = w_pd["event_ts"].dt.strftime("%Y-%m-%d")
w_pd = w_pd.loc[w_pd["active_users"] > 0, ["week_start", "active_users"]].reset_index(drop=True)
# pd:end
# compared in ascending month / week_start order; Grouper also emits empty weeks, filtered out above
pd.testing.assert_frame_equal(m_pd, m_sql, check_dtype=False)
pd.testing.assert_frame_equal(w_pd, w_sql, check_dtype=False)
print("pandas equals SQL (monthly and weekly)")

raw = e.groupby(pd.Grouper(key="event_ts", freq="W-MON"))["user_id"].nunique()
print("W-MON with default closed/label (right/right), labels are the Monday that ENDS each bin:")
print(raw.to_string())
all_weeks = e.groupby(pd.Grouper(key="event_ts", freq="W-MON", closed="left", label="left"))["user_id"].nunique()
print("empty weeks pandas keeps (SQL omits):", [d.strftime("%Y-%m-%d") for d in all_weeks[all_weeks == 0].index])

# ISO-year emulation for the week label's year (date(d,'-3 days','weekday 4') = Thursday of the ISO week)
dates = ["2023-01-01", "2024-12-30", "2021-01-01", "2024-01-01", "2026-12-31", "2020-12-31"]
for d in dates:
    iso_sql = con.execute("SELECT strftime('%Y', date(?, '-3 days', 'weekday 4'))", (d,)).fetchone()[0]
    iso_pd = pd.Timestamp(d).isocalendar().year
    assert int(iso_sql) == int(iso_pd), (d, iso_sql, iso_pd)
print("ISO-year emulation matches isocalendar().year for", dates)
print("strftime('%V') on 3.45.1:", con.execute("SELECT strftime('%V','2024-12-30')").fetchone()[0])
print("asserts passed")
```

**Output (my run):**
```text
SQL monthly:
  month  active_users
2024-01             4
2024-02             2
SQL weekly (Monday start):
week_start  active_users
2024-01-01             2
2024-01-08             2
2024-01-29             2
2024-02-05             1
sum of January-week rows (weeks starting 01-01..01-29): 6 vs January MAU: 4
pandas equals SQL (monthly and weekly)
W-MON with default closed/label (right/right), labels are the Monday that ENDS each bin:
event_ts
2024-01-08    2
2024-01-15    2
2024-01-22    0
2024-01-29    1
2024-02-05    2
2024-02-12    1
Freq: W-MON
empty weeks pandas keeps (SQL omits): ['2024-01-15', '2024-01-22']
ISO-year emulation matches isocalendar().year for ['2023-01-01', '2024-12-30', '2021-01-01', '2024-01-01', '2026-12-31', '2020-12-31']
strftime('%V') on 3.45.1: None
asserts passed
```

**Edge cases:**
- Weekly versus monthly: weekly distinct counts are not additive across weeks (6 versus 4 above), and a week that spans two months cannot be assigned to either without a rule. Decide whether the week belongs to the month of its Monday, or split the week at the month boundary; I used the Monday label and did not split.
- pandas surprise: `pd.Grouper(freq='W-MON')` with its defaults (closed and label both right) labels each bin by the Monday that ends it. The raw run printed above labels the first bin 2024-01-08 for events from Tue 01-02 to Mon 01-08, and the Monday 01-29 07:00 event falls into the bin labelled 01-29, i.e. the previous week. For Monday-start weeks pass `closed='left', label='left'`, which is what matches the SQL.
- Empty periods: pandas `Grouper` emits weeks 01-15 and 01-22 with 0; SQL omits them. I filtered the zeros out to compare; spine them in SQL if the report needs zero rows (Q6).
- `freq='MS'` labels each month by its first day and gave the same two months as `strftime('%Y-%m')` here (labels formatted for the comparison).
- A user with events at 23:59:59 on 01-31 is January; timestamps at midnight in another zone would move a day or a month (Q16).
- Year boundary: `strftime('%Y', event_ts)` with a Monday-start week label can show the calendar year of the Monday, while the ISO year differs (2024-12-30 is ISO week 1 of 2025). Using `date(d, '-3 days', 'weekday 4')` (the Thursday of the ISO week) as an emulation, the year matched pandas `isocalendar().year` for the six dates in the Code block (including 2023-01-01, 2024-12-30 and 2021-01-01), and `strftime('%V')` returned NULL on this SQLite 3.45.1 build (newer SQLite versions list it, I did not run one). Full ISO-week handling is Q43.

**Then explain:**
- Count distinct users per period; never sum monthly or weekly counts over a longer span, recount distinct users over that span.
- MAU here is a plain distinct count of users with at least one event in the calendar month. Rolling windows and DAU/MAU stickiness are Part 8, not covered here.
- `COUNT(DISTINCT ...)` in a group is portable across the common engines; the week truncation is the dialect-specific part: PostgreSQL `DATE_TRUNC('week', ts)` starts on Monday, and MySQL/BigQuery/Snowflake have different week-start defaults and parameters (not executed here, check the manual).

**Follow-ups:**
- Weekly actives for weeks starting Sunday? Change the week key (the Sunday-start and Monday-start arithmetic is Q5); the distinct count stays the same.
- Rolling 7-day or 28-day actives? A different query (self join or range on dates); Part 8 territory.
- Why not `strftime('%W')`? It numbers weeks without the year and starts them on Monday with a week 00 for the days before the first Monday; label by date instead.

**Common mistakes:**
- Using `COUNT(user_id)` (events) instead of `COUNT(DISTINCT user_id)`.
- Adding weekly actives to get monthly actives.
- Leaving `W-MON` at the defaults and shipping labels that are the week end.
- Forgetting that SQL drops empty periods while pandas keeps them.

### Q16 ⭐⭐⭐ 🟡 Time zones and day boundaries ('my daily counts differ by timezone'): orders(order_id, order_ts_utc, amount) stored as UTC ISO text. An order at 2024-03-05 20:00:00 UTC is already 6 March in India (UTC+5:30). Show daily order counts grouped by the UTC date, then by the IST date with datetime(order_ts_utc, '+5 hours', '+30 minutes') (and why the 'localtime' modifier depends on the server's own time zone and is not a safe way to say IST), and which orders move between days. Give the pandas version: pd.to_datetime(..., utc=True), tz_convert('Asia/Kolkata'), dt.date. State the rule: store UTC, convert at the reporting edge, decide the reporting time zone once.
**Asked at:** SQLite date and time functions documentation (lang_datefunc, opened), vendor documentation and not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** The counts differ because the day boundary is different: UTC midnight is 05:30 in India, so evening-UTC orders belong to the next IST date; store UTC, convert once at the reporting edge with a fixed offset (`+5 hours`, `+30 minutes`), and decide the reporting zone in writing.

**Schema and sample data:** six orders stored as UTC ISO text. Orders 2 and 3 straddle the IST midnight (18:29:59 versus 18:30:00 UTC), and order 6 moves across a month boundary. Reporting convention: IST is a fixed UTC+5:30 with no daylight saving.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts_utc TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-03-05 08:00:00',100),
 (2,'2024-03-05 18:29:59',200),
 (3,'2024-03-05 18:30:00',300),
 (4,'2024-03-05 20:00:00',400),
 (5,'2024-03-06 10:00:00',500),
 (6,'2024-03-31 19:00:00',600);
```

**SQL answer:** `SQL_UTC`, `SQL_IST` and `SQL_MOVED` (the orders whose date changes) are in the Code block. The IST one:
```sql
SELECT date(datetime(order_ts_utc, '+5 hours', '+30 minutes')) AS day, COUNT(*) AS orders
FROM orders GROUP BY day ORDER BY day
```

**pandas answer:** identical to the Code block:
```py
ts = pd.to_datetime(orders["order_ts_utc"], utc=True)
ist = ts.dt.tz_convert("Asia/Kolkata")
utc_pd = ts.dt.date.astype(str).value_counts().sort_index().rename_axis("day").reset_index(name="orders")
ist_pd = ist.dt.date.astype(str).value_counts().sort_index().rename_axis("day").reset_index(name="orders")
```

**Example:**
- UTC dates: orders 1 to 4 are 03-05 (4 orders), order 5 is 03-06 (1), order 6 is 03-31 (1).
- IST: order 1 is 13:30 on 03-05, order 2 is 23:59:59 on 03-05 (still the same day), order 3 is exactly 00:00:00 on 03-06, order 4 is 01:30 on 03-06, order 5 is 15:30 on 03-06, order 6 is 00:30 on 04-01.
- IST counts: 03-05 has 2, 03-06 has 3, 04-01 has 1. Orders 3, 4 and 6 move to the next date; order 6 also moves to the next month, so a monthly report in IST would assign it to April while UTC assigns it to March.

**Code:** run with `python3 -I`. The frames are compared in ascending day order. The last part sets the process time zone to show what the `localtime` modifier does.
```python
# Q16: UTC vs IST day boundaries; localtime modifier depends on host TZ; pandas tz_convert
import os
import sqlite3
import time
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts_utc TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-03-05 08:00:00',100),
 (2,'2024-03-05 18:29:59',200),
 (3,'2024-03-05 18:30:00',300),
 (4,'2024-03-05 20:00:00',400),
 (5,'2024-03-06 10:00:00',500),
 (6,'2024-03-31 19:00:00',600);
"""
SQL_UTC = """
SELECT date(order_ts_utc) AS day, COUNT(*) AS orders
FROM orders GROUP BY day ORDER BY day
"""
SQL_IST = """
SELECT date(datetime(order_ts_utc, '+5 hours', '+30 minutes')) AS day, COUNT(*) AS orders
FROM orders GROUP BY day ORDER BY day
"""
SQL_MOVED = """
SELECT order_id, order_ts_utc,
       datetime(order_ts_utc, '+5 hours', '+30 minutes') AS ist_ts,
       date(order_ts_utc) AS utc_day,
       date(datetime(order_ts_utc, '+5 hours', '+30 minutes')) AS ist_day
FROM orders
WHERE date(order_ts_utc) <> date(datetime(order_ts_utc, '+5 hours', '+30 minutes'))
ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
utc_sql = pd.read_sql_query(SQL_UTC, con)
ist_sql = pd.read_sql_query(SQL_IST, con)
print("UTC daily counts:"); print(utc_sql.to_string(index=False))
print("IST daily counts:"); print(ist_sql.to_string(index=False))
print("orders that change day:"); print(pd.read_sql_query(SQL_MOVED, con).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
ts = pd.to_datetime(orders["order_ts_utc"], utc=True)
ist = ts.dt.tz_convert("Asia/Kolkata")
utc_pd = ts.dt.date.astype(str).value_counts().sort_index().rename_axis("day").reset_index(name="orders")
ist_pd = ist.dt.date.astype(str).value_counts().sort_index().rename_axis("day").reset_index(name="orders")
# pd:end
# compared in ascending day order
pd.testing.assert_frame_equal(utc_pd, utc_sql, check_dtype=False)
pd.testing.assert_frame_equal(ist_pd, ist_sql, check_dtype=False)
print("pandas equals SQL for UTC and IST")
print("pandas IST timestamps:", [str(x) for x in ist])

# the 'localtime' modifier depends on the process time zone, not on a stated business zone
probe = "SELECT datetime('2024-03-05 20:00:00', 'localtime')"
print("host TZ env:", os.environ.get("TZ"), "| tzname:", time.tzname)
print("localtime on this host:", con.execute(probe).fetchone()[0])
for tz in ("Asia/Kolkata", "America/New_York"):
    os.environ["TZ"] = tz
    time.tzset()
    print("with TZ =", tz, "->", con.execute(probe).fetchone()[0])
print("asserts passed")
```

**Output (my run):**
```text
UTC daily counts:
       day  orders
2024-03-05       4
2024-03-06       1
2024-03-31       1
IST daily counts:
       day  orders
2024-03-05       2
2024-03-06       3
2024-04-01       1
orders that change day:
 order_id        order_ts_utc              ist_ts    utc_day    ist_day
        3 2024-03-05 18:30:00 2024-03-06 00:00:00 2024-03-05 2024-03-06
        4 2024-03-05 20:00:00 2024-03-06 01:30:00 2024-03-05 2024-03-06
        6 2024-03-31 19:00:00 2024-04-01 00:30:00 2024-03-31 2024-04-01
pandas equals SQL for UTC and IST
pandas IST timestamps: ['2024-03-05 13:30:00+05:30', '2024-03-05 23:59:59+05:30', '2024-03-06 00:00:00+05:30', '2024-03-06 01:30:00+05:30', '2024-03-06 15:30:00+05:30', '2024-04-01 00:30:00+05:30']
host TZ env: None | tzname: ('UTC', 'UTC')
localtime on this host: 2024-03-05 20:00:00
with TZ = Asia/Kolkata -> 2024-03-06 01:30:00
with TZ = America/New_York -> 2024-03-05 15:00:00
asserts passed
```

**Edge cases:**
- Boundary: 18:29:59 UTC stays on the same IST day and 18:30:00 UTC does not. Test the second on either side of the cutoff when you write the conversion.
- `'localtime'` converts using the time zone of the process running SQLite, not a business zone. On this host (tzname UTC) it returned `2024-03-05 20:00:00` for the 20:00 UTC order, i.e. no change; after I set the process `TZ` to `Asia/Kolkata` it returned `2024-03-06 01:30:00`, and with `America/New_York` it returned `2024-03-05 15:00:00`. The same query gives three different answers on three servers, so do not use it to mean IST.
- A fixed `+5 hours +30 minutes` is right for India because it has no daylight saving; for a zone with DST SQLite 3.45 has no named zones, so you need an offsets table (Q38) or conversion upstream.
- Strings with an offset such as `2024-03-10T12:00:00+05:30` are converted to UTC by SQLite's date functions (noted by Wave A on this build; I did not re-run it here). Keep the column in one convention.
- pandas: `pd.to_datetime(..., utc=True)` treats naive strings as UTC and returns tz-aware values; the tz database was available on this host (`Asia/Kolkata` worked). Mixing tz-naive and tz-aware values in a comparison raises a `TypeError` (Q30).
- `dt.date` returns Python `date` objects, so I turned them into strings (`astype(str)`) to compare with SQLite's text dates.

**Then explain:**
- Rule: store timestamps in UTC, convert at the reporting edge, decide the reporting zone once and name it in the metric definition ("orders by IST date").
- Dates move between days, which moves revenue between days and sometimes months; finance and product may legitimately want different zones, so the definition must be written.
- Do the conversion before truncating: `date(datetime(ts, '+5 hours', '+30 minutes'))`, never `datetime(date(ts), '+5 hours')`.
- Dialects (not executed here): PostgreSQL `ts AT TIME ZONE 'Asia/Kolkata'` (check which type you start with), MySQL `CONVERT_TZ(ts, 'UTC', 'Asia/Kolkata')` (needs the time zone tables loaded), BigQuery `DATE(ts, 'Asia/Kolkata')`, Snowflake `CONVERT_TIMEZONE`. I have not run any of them.

**Follow-ups:**
- Hourly profile in IST? Same conversion, then `strftime('%H', ...)` (Q26).
- Daylight saving zone? SQLite cannot do it with named zones; pandas `tz_convert` can (Q30, Q38).
- Customer's local day (per-user zone)? Join a user-to-offset or zone table; one global offset is wrong for multi-zone users.

**Common mistakes:**
- Grouping by `date(order_ts_utc)` and calling it the India day.
- Trusting `'localtime'` on a server whose zone nobody stated.
- Converting after truncating to the day.
- Adding 5.30 hours (5 hours 18 minutes) instead of 5 hours 30 minutes.

### Q17 ⭐⭐⭐ 🔴 Year-over-year growth with missing months: monthly_revenue(month, revenue) built from orders over 2022-2024 where some months have no sales. Compute same-month-last-year revenue and YoY % per month. Show that LAG(revenue, 12) is wrong when a month is missing or duplicated, and fix with a self join on date(month, '-1 year') or on a completed spine. Handle the first year (NULL, not 0), a zero base (NULLIF), and a partial current month (exclude or compare to the same days of last year). pandas: pct_change(12) after reindexing versus shift(freq='12MS') or a merge on the shifted period.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** `LAG(revenue, 12)` means "12 rows back", not "12 months back", so it is wrong the moment a month is missing or duplicated; build a complete month spine first and join each month to `date(month, '-1 year')`, returning NULL (not 0) for the first year and for a zero base.

**Schema and sample data:** monthly revenue stored as the first day of the month. 2023-05 and 2024-02 are missing, 2023-03 exists with revenue 0, and the as-of date is the fixed `2024-04-15`, so April 2024 is a partial month. Convention: calendar months, no time zone conversion.
```sql
CREATE TABLE monthly_revenue(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_revenue VALUES
 ('2023-01-01',100),('2023-02-01',120),('2023-03-01',0),('2023-04-01',150),
 ('2023-06-01',130),('2023-07-01',140),('2023-08-01',160),('2023-09-01',170),
 ('2023-10-01',180),('2023-11-01',200),('2023-12-01',300),
 ('2024-01-01',150),('2024-03-01',90),('2024-04-01',30);
```
The question mentions 2022 to 2024; I used 2023 to April 2024 so the hand check stays short. The first available year has no prior year to compare with.

**SQL answer:** `SQL_MAIN` in the Code block (spine, `LEFT JOIN` to fill gaps, self join one year back, partial month excluded); `SQL_LAG12_FULL` is the broken version:
```sql
WITH RECURSIVE spine(m) AS (
  SELECT '2023-01-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM spine WHERE m < date(:as_of, 'start of month')
),
cal AS (
  SELECT s.m AS month, COALESCE(r.revenue, 0) AS revenue
  FROM spine s LEFT JOIN monthly_revenue r ON r.month = s.m
)
SELECT c.month, c.revenue, p.revenue AS last_year,
       ROUND(100.0 * (c.revenue - p.revenue) / NULLIF(p.revenue, 0), 1) AS yoy_pct
FROM cal c
LEFT JOIN cal p ON p.month = date(c.month, '-1 year')
WHERE date(c.month, '+1 month') <= date(:as_of, '+1 day')
ORDER BY c.month
```
The self join is on a date key, so it does not care how many rows exist between the two months.

**pandas answer:** identical to the Code block:
```py
s = mr.set_index(pd.to_datetime(mr["month"]))["revenue"].astype(float)
spine = pd.date_range("2023-01-01", "2024-03-01", freq="MS")   # completed months only (as of 2024-04-15)
s_full = s.reindex(spine, fill_value=0)
yoy = (s_full.pct_change(12, fill_method=None) * 100).replace([np.inf, -np.inf], np.nan).round(1)
yoy_shift = ((s_full / s_full.shift(12, freq="MS").reindex(s_full.index) - 1) * 100).replace([np.inf, -np.inf], np.nan).round(1)
pd_df = pd.DataFrame({"month": s_full.index.strftime("%Y-%m-%d"), "revenue": s_full.to_numpy(),
                      "last_year": s_full.shift(12).to_numpy(), "yoy_pct": yoy.to_numpy()})
```

**Example:**
- Spine months 2023-01 to 2024-04; the filled series has 2023-05 and 2024-02 at 0.
- Broken `LAG(revenue, 12)`: with 2023-05 missing there are only 11 rows in 2023, so 2024-01 looks back 12 rows to nothing (NULL) instead of to 2023-01. Then 2024-03 is compared with 2023-01 (100) and 2024-04 with 2023-02 (120): each is off by one month.
- Correct: 2024-01 is 150 against 100 = +50.0. 2024-02 is 0 against 120 = -100.0 (the month is missing, filled as 0). 2024-03 is 90 against a base of 0, so NULLIF turns the percent into NULL, not infinity. 2024-04 has revenue 30 for 15 days, so it is dropped as partial.
- 2023 months have no last year in the data, so `last_year` and the percent are NULL, not 0.

**Code:** run with `python3 -I`. The SQL and pandas frames are compared in ascending month order.
```python
# Q17: YoY with missing months: LAG(12) is wrong, spine + self join is right; pandas pct_change(12) after reindex
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE monthly_revenue(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_revenue VALUES
 ('2023-01-01',100),('2023-02-01',120),('2023-03-01',0),('2023-04-01',150),
 ('2023-06-01',130),('2023-07-01',140),('2023-08-01',160),('2023-09-01',170),
 ('2023-10-01',180),('2023-11-01',200),('2023-12-01',300),
 ('2024-01-01',150),('2024-03-01',90),('2024-04-01',30);
"""
AS_OF = "2024-04-15"
SQL_LAG12_FULL = """
WITH x AS (
  SELECT month, revenue,
         LAG(month, 12) OVER (ORDER BY month) AS lag12_month,
         LAG(revenue, 12) OVER (ORDER BY month) AS lag12_revenue
  FROM monthly_revenue
)
SELECT month, revenue, lag12_month, lag12_revenue FROM x WHERE month >= '2024-01-01' ORDER BY month
"""
SQL_MAIN = """
WITH RECURSIVE spine(m) AS (
  SELECT '2023-01-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM spine WHERE m < date(:as_of, 'start of month')
),
cal AS (
  SELECT s.m AS month, COALESCE(r.revenue, 0) AS revenue
  FROM spine s LEFT JOIN monthly_revenue r ON r.month = s.m
)
SELECT c.month, c.revenue, p.revenue AS last_year,
       ROUND(100.0 * (c.revenue - p.revenue) / NULLIF(p.revenue, 0), 1) AS yoy_pct
FROM cal c
LEFT JOIN cal p ON p.month = date(c.month, '-1 year')
WHERE date(c.month, '+1 month') <= date(:as_of, '+1 day')
ORDER BY c.month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("LAG(12) on the table with missing months (2023-05 and 2024-02 are missing):")
print(pd.read_sql_query(SQL_LAG12_FULL, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"as_of": AS_OF})
print("spine + self join (as of", AS_OF, "; 2024-04 is partial so it is excluded):")
print(sql_df.to_string(index=False))

mr = pd.read_sql_query("SELECT * FROM monthly_revenue", con)
# pd:main
s = mr.set_index(pd.to_datetime(mr["month"]))["revenue"].astype(float)
spine = pd.date_range("2023-01-01", "2024-03-01", freq="MS")   # completed months only (as of 2024-04-15)
s_full = s.reindex(spine, fill_value=0)
yoy = (s_full.pct_change(12, fill_method=None) * 100).replace([np.inf, -np.inf], np.nan).round(1)
yoy_shift = ((s_full / s_full.shift(12, freq="MS").reindex(s_full.index) - 1) * 100).replace([np.inf, -np.inf], np.nan).round(1)
pd_df = pd.DataFrame({"month": s_full.index.strftime("%Y-%m-%d"), "revenue": s_full.to_numpy(),
                      "last_year": s_full.shift(12).to_numpy(), "yoy_pct": yoy.to_numpy()})
# pd:end
# compared in ascending month order; SQL last_year is NULL for 2023 because the spine starts in 2023-01
cmp_sql = sql_df.assign(revenue=sql_df["revenue"].astype(float), last_year=sql_df["last_year"].astype(float))
pd.testing.assert_frame_equal(pd_df, cmp_sql, check_dtype=False)
assert yoy_shift.equals(yoy)
print("pandas pct_change(12) after reindex equals SQL; shift(12, freq='MS') gives the same YoY")
print("pandas without the reindex, pct_change(12) on the 14-row series:")
raw = s.pct_change(12, fill_method=None).mul(100).round(1)
print(pd.DataFrame({"month": raw.index.strftime("%Y-%m-%d"), "yoy_pct": raw.to_numpy()}).tail(4).to_string(index=False))
print("zero base in pandas before replace, 2024-03:", (s_full.pct_change(12, fill_method=None) * 100).loc["2024-03-01"])

# duplicate month rows (a late adjustment row for 2023-06): LAG(12) shifts by one the other way
con.executescript("""
CREATE TABLE mr_dup(month TEXT, revenue INTEGER);
INSERT INTO mr_dup SELECT * FROM monthly_revenue;
INSERT INTO mr_dup VALUES ('2023-06-01', 5);
""")
dup = pd.read_sql_query(SQL_LAG12_FULL.replace("monthly_revenue", "mr_dup"), con)
print("LAG(12) with a duplicate 2023-06 row and the missing 2023-05 row:")
print(dup.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
LAG(12) on the table with missing months (2023-05 and 2024-02 are missing):
     month  revenue lag12_month  lag12_revenue
2024-01-01      150         NaN            NaN
2024-03-01       90  2023-01-01          100.0
2024-04-01       30  2023-02-01          120.0
spine + self join (as of 2024-04-15 ; 2024-04 is partial so it is excluded):
     month  revenue  last_year  yoy_pct
2023-01-01      100        NaN      NaN
2023-02-01      120        NaN      NaN
2023-03-01        0        NaN      NaN
2023-04-01      150        NaN      NaN
2023-05-01        0        NaN      NaN
2023-06-01      130        NaN      NaN
2023-07-01      140        NaN      NaN
2023-08-01      160        NaN      NaN
2023-09-01      170        NaN      NaN
2023-10-01      180        NaN      NaN
2023-11-01      200        NaN      NaN
2023-12-01      300        NaN      NaN
2024-01-01      150      100.0     50.0
2024-02-01        0      120.0   -100.0
2024-03-01       90        0.0      NaN
pandas pct_change(12) after reindex equals SQL; shift(12, freq='MS') gives the same YoY
pandas without the reindex, pct_change(12) on the 14-row series:
     month  yoy_pct
2023-12-01      NaN
2024-01-01      NaN
2024-03-01    -10.0
2024-04-01    -75.0
zero base in pandas before replace, 2024-03: inf
LAG(12) with a duplicate 2023-06 row and the missing 2023-05 row:
     month  revenue lag12_month  lag12_revenue
2024-01-01      150  2023-01-01            100
2024-03-01       90  2023-02-01            120
2024-04-01       30  2023-03-01              0
asserts passed
```

**Edge cases:**
- Missing month: broken LAG(12) returned `NaN` for 2024-01 and the 2023-01 and 2023-02 revenues for 2024-03 and 2024-04, as the output shows. A report built on it looks plausible, which is the danger.
- Duplicated month: with an extra 2023-06 row (a late adjustment) and the missing 2023-05 row, the two errors cancelled for 2024-01 (correct by accident, 2023-01) and then 2024-03 and 2024-04 were again off by one (2023-02 and 2023-03). Aggregate to one row per month before any LAG.
- A zero base in SQL gave NULL via `NULLIF`; the same in pandas gave `inf` before I replaced it (the printed `inf` for 2024-03). pandas 3.0 `pct_change` needs `fill_method=None` (no forward fill).
- Spine-filled zero is a business assumption: "missing" might mean no data loaded rather than no sales, in which case the YoY of -100.0 for 2024-02 is misleading. Flag it rather than hide it.
- Partial current month: I excluded it with `date(month, '+1 month') <= date(:as_of, '+1 day')`. The other fair option is to compare with the same days of last year, which needs daily data; I did not demonstrate it here.
- pandas without the reindex: `pct_change(12)` on the 14-row series printed -10.0 for 2024-03 (compared with 2023-01, wrong) and -75.0 for 2024-04, so reindex first. `shift(12, freq='MS')` shifts the index labels by 12 month starts, so it aligns by date, and its YoY equalled the reindex version in the run.

**Then explain:**
- Row-based windows count rows; YoY is a calendar relationship, so use a date join or a completed spine.
- `date(month, '-1 year')` on a month-start date is safe (day 1 never overflows); on a 29 February date it would land on 1 March 2023 (checked: SQLite rolls the invalid 2023-02-29 forward), so keep the month key as the first of the month.
- The recursive CTE is the SQLite spine; PostgreSQL has `generate_series`, and BigQuery/Snowflake have their own sequence generators (not executed here). A physical calendar table is Q31.
- Percent change on a small base (150 versus 100) is dramatic; consider also showing the absolute difference.

**Follow-ups:**
- Why not `RANGE` with an interval? SQLite RANGE offsets work on numbers, not text dates (Part 5); a date join is simpler.
- YoY for a fiscal year? Same join on the fiscal month key (Q32).
- Same-day-last-year (daily)? 364-day offset keeps weekdays aligned (Q43).

**Common mistakes:**
- `LAG(revenue, 12)` on an incomplete series.
- Filling the first year with 0 and reporting an infinite or 100 percent growth.
- Dividing by a zero base without `NULLIF`.
- Including the current partial month in a YoY chart.
- Calling `pct_change(12)` before the reindex.

### Q18 ⭐⭐⭐ 🔴 Month-over-month retention (active in both months): events(user_id, event_ts). For each month m return the users active in m, the users active in both m and m+1 (a self join or INTERSECT on distinct user-month pairs, only 'present in m and m+1', no streaks), and the retention rate. Also return users active in m but not m+1. Show a user active in months 1 and 3 but not 2 and what the m to m+1 view says about them. Give the pandas version with set operations on groupby sets or merge of the user-month frame with itself shifted by one period.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Reduce events to distinct (user, month) pairs, LEFT JOIN that table to itself on the same user and the next month, then per month count users (active), matched users (active in both m and m+1) and the difference (lost); the rate is matched over active, and the last loaded month has no judgeable next month.

**Schema and sample data:** thirteen events for six users over Jan to Apr 2024. User 2 is active in January and March but not February; user 6 is active only in January. Convention: calendar months of the stored timestamp, no time zone conversion. Fixed boundary: April is the last loaded month, so April to May is not reported (`:last_month = '2024-04'`).
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-03 10:00:00'),(1,'2024-01-20 10:00:00'),(1,'2024-02-05 10:00:00'),(1,'2024-03-07 10:00:00'),
 (2,'2024-01-11 10:00:00'),(2,'2024-03-15 10:00:00'),
 (3,'2024-01-25 10:00:00'),(3,'2024-02-14 10:00:00'),
 (4,'2024-02-02 10:00:00'),(4,'2024-03-02 10:00:00'),(4,'2024-04-09 10:00:00'),
 (5,'2024-03-21 10:00:00'),
 (6,'2024-01-29 10:00:00');
```

**SQL answer:** `SQL_MAIN` (self join on distinct user-months), `SQL_INTERSECT` (the INTERSECT form for one month pair) and `SQL_LOST` (the list of users active in m but not m+1) are in the Code block:
```sql
WITH um AS (
  SELECT DISTINCT user_id, strftime('%Y-%m', event_ts) AS m FROM events
)
SELECT a.m AS month,
       COUNT(*) AS active_users,
       CASE WHEN a.m < :last_month THEN COUNT(b.user_id) END AS active_next_month,
       CASE WHEN a.m < :last_month THEN COUNT(*) - COUNT(b.user_id) END AS lost_next_month,
       CASE WHEN a.m < :last_month THEN ROUND(100.0 * COUNT(b.user_id) / COUNT(*), 1) END AS retention_pct
FROM um a
LEFT JOIN um b
  ON b.user_id = a.user_id
 AND b.m = strftime('%Y-%m', date(a.m || '-01', '+1 month'))
GROUP BY a.m
ORDER BY a.m
```

**pandas answer:** identical to the Code block. The next-month rows are moved back one `Period` so a plain merge matches month m with m+1:
```py
e = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
um = e.assign(m=e["event_ts"].dt.to_period("M"))[["user_id", "m"]].drop_duplicates()
nxt = um.assign(m=um["m"] - 1, seen_next=1)          # the user's next-month row, moved back one period
j = um.merge(nxt, on=["user_id", "m"], how="left")
g = j.groupby("m").agg(active_users=("user_id", "size"), active_next_month=("seen_next", "count")).reset_index()
g["lost_next_month"] = g["active_users"] - g["active_next_month"]
g["retention_pct"] = (100.0 * g["active_next_month"] / g["active_users"]).round(1)
last = pd.Period(LAST_COMPLETE, "M")
g.loc[g["m"] >= last, ["active_next_month", "lost_next_month", "retention_pct"]] = float("nan")
g["month"] = g["m"].astype(str)
pd_df = g[["month", "active_users", "active_next_month", "lost_next_month", "retention_pct"]]
```

**Example:** distinct user-months: Jan {1, 2, 3, 6}, Feb {1, 3, 4}, Mar {1, 2, 4, 5}, Apr {4}.
- January: 4 active; in both Jan and Feb: users 1 and 3 (2); lost: users 2 and 6. Retention 2 / 4 = 50.0.
- February: 3 active; also in March: users 1 and 4 (2); lost: user 3. Retention 2 / 3 = 66.7.
- March: 4 active; also in April: user 4 only (1); lost: users 1, 2, 5. Retention 1 / 4 = 25.0.
- April: 1 active, but May has not happened (not loaded), so the retention cells are NULL, not 0.
- User 2 (Jan and Mar, not Feb): the Jan to Feb view marks them lost. The Feb to Mar view does not count them at all, because they were not active in February (so not in that month's denominator and not retained). In March they simply appear as active again. The m to m+1 view therefore treats a returning user as a loss and then as invisible; classifying that return is the churn/resurrection question (Q33).

**Code:** run with `python3 -I`. Frames are compared in ascending month order; the set-operation check compares sorted ids.
```python
# Q18: month-over-month retention (active in m and m+1), lost users, pandas merge on shifted period
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-03 10:00:00'),(1,'2024-01-20 10:00:00'),(1,'2024-02-05 10:00:00'),(1,'2024-03-07 10:00:00'),
 (2,'2024-01-11 10:00:00'),(2,'2024-03-15 10:00:00'),
 (3,'2024-01-25 10:00:00'),(3,'2024-02-14 10:00:00'),
 (4,'2024-02-02 10:00:00'),(4,'2024-03-02 10:00:00'),(4,'2024-04-09 10:00:00'),
 (5,'2024-03-21 10:00:00'),
 (6,'2024-01-29 10:00:00');
"""
LAST_COMPLETE = "2024-04"   # April is the last loaded month, so April -> May cannot be judged
SQL_MAIN = """
WITH um AS (
  SELECT DISTINCT user_id, strftime('%Y-%m', event_ts) AS m FROM events
)
SELECT a.m AS month,
       COUNT(*) AS active_users,
       CASE WHEN a.m < :last_month THEN COUNT(b.user_id) END AS active_next_month,
       CASE WHEN a.m < :last_month THEN COUNT(*) - COUNT(b.user_id) END AS lost_next_month,
       CASE WHEN a.m < :last_month THEN ROUND(100.0 * COUNT(b.user_id) / COUNT(*), 1) END AS retention_pct
FROM um a
LEFT JOIN um b
  ON b.user_id = a.user_id
 AND b.m = strftime('%Y-%m', date(a.m || '-01', '+1 month'))
GROUP BY a.m
ORDER BY a.m
"""
SQL_INTERSECT = """
SELECT user_id FROM (SELECT DISTINCT user_id, strftime('%Y-%m', event_ts) AS m FROM events) WHERE m = '2024-01'
INTERSECT
SELECT user_id FROM (SELECT DISTINCT user_id, strftime('%Y-%m', event_ts) AS m FROM events) WHERE m = '2024-02'
ORDER BY user_id
"""
SQL_LOST = """
WITH um AS (SELECT DISTINCT user_id, strftime('%Y-%m', event_ts) AS m FROM events)
SELECT a.m AS month, a.user_id
FROM um a
WHERE a.m < :last_month
  AND NOT EXISTS (SELECT 1 FROM um b WHERE b.user_id = a.user_id
                  AND b.m = strftime('%Y-%m', date(a.m || '-01', '+1 month')))
ORDER BY a.m, a.user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"last_month": LAST_COMPLETE})
print(sql_df.to_string(index=False))
print("INTERSECT, active in both 2024-01 and 2024-02:", [r[0] for r in con.execute(SQL_INTERSECT)])
lost = pd.read_sql_query(SQL_LOST, con, params={"last_month": LAST_COMPLETE})
print("users active in m but not m+1:"); print(lost.to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
e = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
um = e.assign(m=e["event_ts"].dt.to_period("M"))[["user_id", "m"]].drop_duplicates()
nxt = um.assign(m=um["m"] - 1, seen_next=1)          # the user's next-month row, moved back one period
j = um.merge(nxt, on=["user_id", "m"], how="left")
g = j.groupby("m").agg(active_users=("user_id", "size"), active_next_month=("seen_next", "count")).reset_index()
g["lost_next_month"] = g["active_users"] - g["active_next_month"]
g["retention_pct"] = (100.0 * g["active_next_month"] / g["active_users"]).round(1)
last = pd.Period(LAST_COMPLETE, "M")
g.loc[g["m"] >= last, ["active_next_month", "lost_next_month", "retention_pct"]] = float("nan")
g["month"] = g["m"].astype(str)
pd_df = g[["month", "active_users", "active_next_month", "lost_next_month", "retention_pct"]]
# pd:end
# compared in ascending month order
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas equals SQL")
# set-operation form of the same thing
sets = um.groupby("m")["user_id"].apply(set)
both = sets[pd.Period("2024-01")] & sets[pd.Period("2024-02")]
assert sorted(both) == [r[0] for r in con.execute(SQL_INTERSECT)]
lost_pd = [(str(p), u) for p in sets.index[:-1] for u in sorted(sets[p] - sets.get(p + 1, set()))]
assert lost_pd == [tuple(x) for x in lost.itertuples(index=False)]
print("set logic (intersection, difference) equals SQL")
print("asserts passed")
```

**Output (my run):**
```text
  month  active_users  active_next_month  lost_next_month  retention_pct
2024-01             4                2.0              2.0           50.0
2024-02             3                2.0              1.0           66.7
2024-03             4                1.0              3.0           25.0
2024-04             1                NaN              NaN            NaN
INTERSECT, active in both 2024-01 and 2024-02: [1, 3]
users active in m but not m+1:
  month  user_id
2024-01        2
2024-01        6
2024-02        3
2024-03        1
2024-03        2
2024-03        5
pandas equals SQL
set logic (intersection, difference) equals SQL
asserts passed
```

**Edge cases:**
- Duplicates: multiple events in a month are collapsed by `DISTINCT user_id, month` first (user 1 has two January events). Skipping this step makes `COUNT(*)` count events.
- Last month: `COUNT(b.user_id)` would be 0 and the retention 0 percent for April, which looks like total churn. The `CASE WHEN a.m < :last_month` turns it into NULL; pandas shows `NaN`.
- Gap months: a user active in months 1 and 3 but not 2 is lost at 1 to 2 and absent at 2 to 3. There is no streak logic here by design; streaks are Part 7.
- The month key comparison is on `'YYYY-MM'` text, which sorts correctly. The next month is built with `date(a.m || '-01', '+1 month')`, safe because the day is 1 (the end-of-month overflow rule only bites on days 29 to 31).
- A month where nobody was active would be absent from the table (no spine), so the "next month" of the month before it shows everyone lost; add a spine if that can happen (Q6).

**Then explain:**
- The denominator is the active users in month m, not the cohort of new users (that is cohort retention, Q10 and Q11). This metric is also called month-over-month retention or stickiness-by-month; I define it as the share of month-m actives who are active again in m+1.
- INTERSECT of the two user sets (users 1 and 3 for Jan and Feb) and the self join agree on who is retained; the self join also gives every month in one pass.
- pandas: either shift the user-month frame back one period and merge (used here), or build `groupby('m')['user_id'].apply(set)` and use `&` and `-`; both matched the SQL.
- Dialects (not executed here): `DATE_TRUNC('month', ts)` or `DATE_FORMAT(ts, '%Y-%m')` produce the month key in PostgreSQL and MySQL; `INTERSECT` exists in all four engines, but older MySQL versions lack it.

**Follow-ups:**
- Retained for three months in a row? That is a streak or island problem (Part 7).
- Users who came back after leaving? Resurrection (Q33).
- Weekly instead of monthly? Same query with a Monday-start week key and `'+7 days'`.

**Common mistakes:**
- Counting events instead of distinct user-months.
- Reporting the last loaded month as 0 percent retention.
- Dividing by new users instead of by active users in m.
- Subtracting month numbers (December to January breaks, Q10).

### Q19 ⭐⭐ 🟢 Customer lifetime and recency: orders(order_id, user_id, order_ts, amount). For each customer return first order date, last order date, lifetime in days (last minus first), number of orders, and recency in days relative to a fixed as-of date such as '2024-12-31' (not 'now', so the result is reproducible). Explain why a parameterised as-of date matters for tests and backfills, and give the pandas version with groupby agg and a Timedelta .dt.days. Mention a customer with one order (lifetime 0).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Group by customer for `MIN` and `MAX` of the order timestamp, `COUNT(*)` for orders, lifetime as last minus first calendar date, and recency as the as-of date minus the last order date, with the as-of date passed in as a parameter (here 2024-12-31) so the run is repeatable and orders after that date are ignored.

**Schema and sample data:** nine orders for five customers. Customer 2 and customer 4 have one order as of 2024-12-31 (lifetime 0). Customer 3 orders at 23:30 and then 00:30 the next calendar day (one hour apart). Customer 4's second order and all of customer 5's orders fall after the as-of date. Convention: dates are taken from the stored timestamp text with no time zone conversion.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-10 09:00:00',100),(2,1,'2024-03-15 10:00:00',50),(3,1,'2024-12-01 18:00:00',70),
 (4,2,'2024-05-05 12:00:00',200),
 (5,3,'2024-02-01 23:30:00',40),(6,3,'2024-02-02 00:30:00',60),
 (7,4,'2024-06-01 10:00:00',90),(8,4,'2025-01-05 09:00:00',30),
 (9,5,'2025-01-10 08:00:00',25);
```

**SQL answer:** `SQL_MAIN` in the Code block (parameter `:as_of`); `SQL_NAIVE` shows the timestamp-difference trap:
```sql
SELECT user_id,
       date(MIN(order_ts)) AS first_order,
       date(MAX(order_ts)) AS last_order,
       CAST(julianday(date(MAX(order_ts))) - julianday(date(MIN(order_ts))) AS INTEGER) AS lifetime_days,
       COUNT(*) AS orders,
       CAST(julianday(:as_of) - julianday(date(MAX(order_ts))) AS INTEGER) AS recency_days
FROM orders
WHERE order_ts < date(:as_of, '+1 day')
GROUP BY user_id
ORDER BY user_id
```

**pandas answer:** identical to the Code block:
```py
AS_OF = pd.Timestamp("2024-12-31")
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"]))
o = o[o["order_ts"] < AS_OF + pd.Timedelta(days=1)]
agg = o.groupby("user_id").agg(first_ts=("order_ts", "min"), last_ts=("order_ts", "max"),
                               orders=("order_id", "count")).reset_index()
pd_df = pd.DataFrame({
    "user_id": agg["user_id"],
    "first_order": agg["first_ts"].dt.strftime("%Y-%m-%d"),
    "last_order": agg["last_ts"].dt.strftime("%Y-%m-%d"),
    "lifetime_days": (agg["last_ts"].dt.normalize() - agg["first_ts"].dt.normalize()).dt.days,
    "orders": agg["orders"],
    "recency_days": (AS_OF - agg["last_ts"].dt.normalize()).dt.days,
})
```

**Example:** as of 2024-12-31 the filter keeps orders on or before that day (`order_ts < date(:as_of, '+1 day')`).
- Customer 1: first 2024-01-10, last 2024-12-01, 3 orders. Lifetime is 326 days (2024 is a leap year: day 10 to day 336), recency 30 days.
- Customer 2: one order on 2024-05-05, lifetime 0, recency 240 days.
- Customer 3: first 2024-02-01, last 2024-02-02, lifetime 1 calendar day, recency 333.
- Customer 4: only the 2024-06-01 order is visible, so one order, lifetime 0, recency 213. Customer 5 has no order on or before the as-of date, so they are not a customer yet and do not appear.

**Code:** run with `python3 -I`. The frames are compared in ascending `user_id` order.
```python
# Q19: customer lifetime and recency relative to a fixed as-of date
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-10 09:00:00',100),(2,1,'2024-03-15 10:00:00',50),(3,1,'2024-12-01 18:00:00',70),
 (4,2,'2024-05-05 12:00:00',200),
 (5,3,'2024-02-01 23:30:00',40),(6,3,'2024-02-02 00:30:00',60),
 (7,4,'2024-06-01 10:00:00',90),(8,4,'2025-01-05 09:00:00',30),
 (9,5,'2025-01-10 08:00:00',25);
"""
SQL_MAIN = """
SELECT user_id,
       date(MIN(order_ts)) AS first_order,
       date(MAX(order_ts)) AS last_order,
       CAST(julianday(date(MAX(order_ts))) - julianday(date(MIN(order_ts))) AS INTEGER) AS lifetime_days,
       COUNT(*) AS orders,
       CAST(julianday(:as_of) - julianday(date(MAX(order_ts))) AS INTEGER) AS recency_days
FROM orders
WHERE order_ts < date(:as_of, '+1 day')
GROUP BY user_id
ORDER BY user_id
"""
SQL_NAIVE = """
SELECT user_id,
       CAST(julianday(MAX(order_ts)) - julianday(MIN(order_ts)) AS INTEGER) AS lifetime_days_naive
FROM orders WHERE user_id = 3 GROUP BY user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"as_of": "2024-12-31"})
print("as of 2024-12-31:"); print(sql_df.to_string(index=False))
print("as of 2025-01-31 (the backfill gives a different answer):")
print(pd.read_sql_query(SQL_MAIN, con, params={"as_of": "2025-01-31"}).to_string(index=False))
print("naive lifetime for user 3 (timestamps, 1 hour apart):", con.execute(SQL_NAIVE).fetchone())

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
AS_OF = pd.Timestamp("2024-12-31")
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"]))
o = o[o["order_ts"] < AS_OF + pd.Timedelta(days=1)]
agg = o.groupby("user_id").agg(first_ts=("order_ts", "min"), last_ts=("order_ts", "max"),
                               orders=("order_id", "count")).reset_index()
pd_df = pd.DataFrame({
    "user_id": agg["user_id"],
    "first_order": agg["first_ts"].dt.strftime("%Y-%m-%d"),
    "last_order": agg["last_ts"].dt.strftime("%Y-%m-%d"),
    "lifetime_days": (agg["last_ts"].dt.normalize() - agg["first_ts"].dt.normalize()).dt.days,
    "orders": agg["orders"],
    "recency_days": (AS_OF - agg["last_ts"].dt.normalize()).dt.days,
})
# pd:end
# compared in ascending user_id order
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas equals SQL")
u3 = agg[agg["user_id"] == 3].iloc[0]
print("pandas naive lifetime for user 3 (.dt.days on the raw timestamps):", (u3["last_ts"] - u3["first_ts"]).days)
print("asserts passed")
```

**Output (my run):**
```text
as of 2024-12-31:
 user_id first_order last_order  lifetime_days  orders  recency_days
       1  2024-01-10 2024-12-01            326       3            30
       2  2024-05-05 2024-05-05              0       1           240
       3  2024-02-01 2024-02-02              1       2           333
       4  2024-06-01 2024-06-01              0       1           213
as of 2025-01-31 (the backfill gives a different answer):
 user_id first_order last_order  lifetime_days  orders  recency_days
       1  2024-01-10 2024-12-01            326       3            61
       2  2024-05-05 2024-05-05              0       1           271
       3  2024-02-01 2024-02-02              1       2           364
       4  2024-06-01 2025-01-05            218       2            26
       5  2025-01-10 2025-01-10              0       1            21
naive lifetime for user 3 (timestamps, 1 hour apart): (3, 0)
pandas equals SQL
pandas naive lifetime for user 3 (.dt.days on the raw timestamps): 0
asserts passed
```

**Edge cases:**
- One order: lifetime 0 and the first and last order dates are the same (customers 2 and 4). Say so in the definition, because a 0 here is not a missing value.
- Timestamps: customer 3's orders are one hour apart, so the raw difference is 0.04 days; the naive SQL (`julianday(MAX(order_ts)) - julianday(MIN(order_ts))` cast to integer) printed 0 and pandas `.dt.days` on the raw timestamps also printed 0, while the calendar-day version (`date()` in SQL, `.dt.normalize()` in pandas) gave 1. Decide whether lifetime means elapsed time or calendar days.
- As-of changes the answer: rerunning with `2025-01-31` changed customer 4 (lifetime 218, recency 26) and added customer 5, and every recency grew. This is why the as-of date is a parameter: a backfill, a test, or a re-run next week must reproduce the same number.
- Using `date('now')` makes the report non-reproducible and a unit test impossible; never use it in a query you want to assert.
- Orders after the as-of date must be filtered, or recency goes negative for customers whose last order is in the future relative to the as-of date.
- Refunded or cancelled orders: decide whether they count as orders before computing first and last (not in the sample).

**Then explain:**
- Lifetime = last order date minus first order date; it is a span, not tenure since signup (a customer with a signup date and no order has no lifetime here).
- Recency = as-of date minus last order date. It is the "R" in RFM analysis, where frequency is the `COUNT(*)`.
- In pandas, `groupby().agg()` with named aggregation gives min, max and count in one pass; a `Timedelta` difference exposes `.dt.days`, which truncates toward zero, so normalise to midnight first.
- Dialects (not executed here): `DATEDIFF(day, first, last)` in SQL Server and Snowflake (check argument order), `last - first` for dates in PostgreSQL, `DATEDIFF(last, first)` in MySQL.

**Follow-ups:**
- Average time between orders? Lifetime divided by (orders - 1), guarding single-order customers (NULL, not 0).
- Why is recency only meaningful with a fixed date? Because it is relative to "now", which changes.
- Customers who never ordered? They are absent here; start from `users` with a LEFT JOIN if they should appear with NULLs.

**Common mistakes:**
- `date('now')` inside the query.
- Treating a zero lifetime as missing, or dividing by it.
- Subtracting raw timestamps and getting fractional or truncated days.
- Leaving future orders in the as-of snapshot.

### Q20 ⭐⭐ 🟡 Time between first and second purchase and repeat purchase rate: orders(order_id, user_id, order_ts, amount). Using ROW_NUMBER per user, return days between order 1 and order 2 for users with at least two orders, the average and the median of that gap (median needs a window or sort trick in SQLite), the repeat purchase rate (users with 2 or more orders divided by users with 1 or more), and the repeat rate within 30 days of the first order. pandas: groupby cumcount, merge, quantile. Mention that orders on the same day need a tie-breaker.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Number each customer's orders with `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts, order_id)`, self join order 1 to order 2 for the gap in calendar days, take the average and the middle gap(s) for the median, and divide customers with 2 or more orders by customers with 1 or more for the repeat rate.

**Schema and sample data:** eleven orders for six customers, fixed as-of date 2024-04-15. Customer 3 and customer 6 have one order each. Customer 4's two orders have the identical timestamp (a tie), customer 6's first order is only 14 days before the as-of date. Convention: gaps are calendar days from the date part of the stored timestamp; no time zone conversion.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-01 10:00:00',100),(2,1,'2024-01-11 10:00:00',50),(3,1,'2024-03-01 10:00:00',70),
 (4,2,'2024-01-05 09:00:00',200),(5,2,'2024-02-20 09:00:00',80),
 (6,3,'2024-02-01 12:00:00',40),
 (8,4,'2024-03-01 10:00:00',90),(7,4,'2024-03-01 10:00:00',30),
 (9,5,'2024-01-15 08:00:00',25),(10,5,'2024-01-20 08:00:00',35),
 (11,6,'2024-04-01 15:00:00',60);
```

**SQL answer:** `SQL_GAPS`, `SQL_STATS` (average and median) and `SQL_RATES` are in the Code block. The gaps query:
```sql
WITH r AS (
  SELECT user_id, order_id, order_ts,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts, order_id) AS rn
  FROM orders
  WHERE order_ts < date(:as_of, '+1 day')
)
SELECT a.user_id,
       CAST(julianday(date(b.order_ts)) - julianday(date(a.order_ts)) AS INTEGER) AS gap_days
FROM r a JOIN r b ON b.user_id = a.user_id AND a.rn = 1 AND b.rn = 2
ORDER BY a.user_id
```
The median trick for an even or odd count `n`: number the sorted gaps `k = 1..n` and average the rows where `k IN ((n + 1) / 2, (n + 2) / 2)` (integer division); for an odd `n` both expressions point at the same middle row.

**pandas answer:** identical to the Code block (`cumcount`, merge, `quantile`):
```py
AS_OF_TS = pd.Timestamp(AS_OF)
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"]))
o = o[o["order_ts"] < AS_OF_TS + pd.Timedelta(days=1)].sort_values(["user_id", "order_ts", "order_id"])
o["rn"] = o.groupby("user_id").cumcount() + 1
first = o[o["rn"] == 1][["user_id", "order_ts"]].rename(columns={"order_ts": "first_ts"})
second = o[o["rn"] == 2][["user_id", "order_ts"]].rename(columns={"order_ts": "second_ts"})
u = first.merge(second, on="user_id", how="left")
u["gap_days"] = (u["second_ts"].dt.normalize() - u["first_ts"].dt.normalize()).dt.days
gaps_pd = u.dropna(subset=["gap_days"])[["user_id", "gap_days"]].astype({"gap_days": int}).reset_index(drop=True)
avg_gap = round(gaps_pd["gap_days"].mean(), 2)
median_gap = gaps_pd["gap_days"].quantile(0.5)
eligible = u["first_ts"].dt.normalize() + pd.Timedelta(days=30) <= AS_OF_TS
repeat30 = eligible & u["second_ts"].notna() & (u["second_ts"].dt.normalize() <= u["first_ts"].dt.normalize() + pd.Timedelta(days=30))
```

**Example:**
- Customer 1: orders 01-01 and 01-11, gap 10 days. Customer 2: 01-05 and 02-20, gap 46 (January has 31 days: 26 days left in January after the 5th, plus 20 = 46). Customer 5: 01-15 and 01-20, gap 5.
- Customer 4: both orders on 03-01 at 10:00. The tie-breaker `order_id` makes order 7 the first and order 8 the second (the output shows rn 1 and 2), gap 0.
- Customers 3 and 6 have one order, so no gap. Gaps are 10, 46, 0, 5; sorted 0, 5, 10, 46: average 61 / 4 = 15.25, median (5 + 10) / 2 = 7.5.
- Repeat rate: 4 customers with 2 or more orders out of 6 = 66.7 percent.
- Repeat within 30 days: customer 6's first order is 14 days old as of 2024-04-15, so they are not old enough to be judged and are left out of the denominator: 3 repeaters within 30 days (customers 1, 4, 5) out of 5 eligible = 60.0 percent. Using all 6 would give 50.0 percent, which understates it.

**Code:** run with `python3 -I`. The gap frames are compared in ascending `user_id` order; scalars compared directly.
```python
# Q20: first-to-second purchase gap, repeat purchase rate, repeat within 30 days (as-of aware)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-01 10:00:00',100),(2,1,'2024-01-11 10:00:00',50),(3,1,'2024-03-01 10:00:00',70),
 (4,2,'2024-01-05 09:00:00',200),(5,2,'2024-02-20 09:00:00',80),
 (6,3,'2024-02-01 12:00:00',40),
 (8,4,'2024-03-01 10:00:00',90),(7,4,'2024-03-01 10:00:00',30),
 (9,5,'2024-01-15 08:00:00',25),(10,5,'2024-01-20 08:00:00',35),
 (11,6,'2024-04-01 15:00:00',60);
"""
AS_OF = "2024-04-15"
SQL_GAPS = """
WITH r AS (
  SELECT user_id, order_id, order_ts,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts, order_id) AS rn
  FROM orders
  WHERE order_ts < date(:as_of, '+1 day')
)
SELECT a.user_id,
       CAST(julianday(date(b.order_ts)) - julianday(date(a.order_ts)) AS INTEGER) AS gap_days
FROM r a JOIN r b ON b.user_id = a.user_id AND a.rn = 1 AND b.rn = 2
ORDER BY a.user_id
"""
SQL_STATS = """
WITH r AS (
  SELECT user_id, order_id, order_ts,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts, order_id) AS rn
  FROM orders WHERE order_ts < date(:as_of, '+1 day')
),
g AS (
  SELECT a.user_id,
         CAST(julianday(date(b.order_ts)) - julianday(date(a.order_ts)) AS INTEGER) AS gap_days
  FROM r a JOIN r b ON b.user_id = a.user_id AND a.rn = 1 AND b.rn = 2
),
o AS (
  SELECT gap_days, ROW_NUMBER() OVER (ORDER BY gap_days) AS k, COUNT(*) OVER () AS n FROM g
)
SELECT (SELECT ROUND(AVG(gap_days), 2) FROM g) AS avg_gap,
       (SELECT AVG(gap_days) FROM o WHERE k IN ((n + 1) / 2, (n + 2) / 2)) AS median_gap
"""
SQL_RATES = """
WITH r AS (
  SELECT user_id, order_ts,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts, order_id) AS rn
  FROM orders WHERE order_ts < date(:as_of, '+1 day')
),
u AS (
  SELECT a.user_id, a.order_ts AS first_ts, b.order_ts AS second_ts
  FROM r a LEFT JOIN r b ON b.user_id = a.user_id AND b.rn = 2
  WHERE a.rn = 1
)
SELECT COUNT(*) AS customers,
       COUNT(second_ts) AS repeaters,
       ROUND(100.0 * COUNT(second_ts) / COUNT(*), 1) AS repeat_rate_pct,
       SUM(CASE WHEN date(first_ts, '+30 days') <= :as_of THEN 1 ELSE 0 END) AS eligible_30d,
       SUM(CASE WHEN date(first_ts, '+30 days') <= :as_of
                 AND second_ts IS NOT NULL
                 AND date(second_ts) <= date(first_ts, '+30 days') THEN 1 ELSE 0 END) AS repeat_30d,
       ROUND(100.0 * SUM(CASE WHEN date(first_ts, '+30 days') <= :as_of
                               AND second_ts IS NOT NULL
                               AND date(second_ts) <= date(first_ts, '+30 days') THEN 1 ELSE 0 END)
             / NULLIF(SUM(CASE WHEN date(first_ts, '+30 days') <= :as_of THEN 1 ELSE 0 END), 0), 1) AS repeat_30d_pct
FROM u
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"as_of": AS_OF}
gaps_sql = pd.read_sql_query(SQL_GAPS, con, params=P)
stats_sql = pd.read_sql_query(SQL_STATS, con, params=P)
rates_sql = pd.read_sql_query(SQL_RATES, con, params=P)
print("gaps:"); print(gaps_sql.to_string(index=False))
print(stats_sql.to_string(index=False))
print(rates_sql.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
AS_OF_TS = pd.Timestamp(AS_OF)
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"]))
o = o[o["order_ts"] < AS_OF_TS + pd.Timedelta(days=1)].sort_values(["user_id", "order_ts", "order_id"])
o["rn"] = o.groupby("user_id").cumcount() + 1
first = o[o["rn"] == 1][["user_id", "order_ts"]].rename(columns={"order_ts": "first_ts"})
second = o[o["rn"] == 2][["user_id", "order_ts"]].rename(columns={"order_ts": "second_ts"})
u = first.merge(second, on="user_id", how="left")
u["gap_days"] = (u["second_ts"].dt.normalize() - u["first_ts"].dt.normalize()).dt.days
gaps_pd = u.dropna(subset=["gap_days"])[["user_id", "gap_days"]].astype({"gap_days": int}).reset_index(drop=True)
avg_gap = round(gaps_pd["gap_days"].mean(), 2)
median_gap = gaps_pd["gap_days"].quantile(0.5)
eligible = u["first_ts"].dt.normalize() + pd.Timedelta(days=30) <= AS_OF_TS
repeat30 = eligible & u["second_ts"].notna() & (u["second_ts"].dt.normalize() <= u["first_ts"].dt.normalize() + pd.Timedelta(days=30))
# pd:end
# compared in ascending user_id order
pd.testing.assert_frame_equal(gaps_pd, gaps_sql, check_dtype=False)
assert avg_gap == stats_sql["avg_gap"][0] and median_gap == stats_sql["median_gap"][0]
r = rates_sql.iloc[0]
assert len(u) == r["customers"] and u["second_ts"].notna().sum() == r["repeaters"]
assert round(100.0 * u["second_ts"].notna().mean(), 1) == r["repeat_rate_pct"]
assert eligible.sum() == r["eligible_30d"] and repeat30.sum() == r["repeat_30d"]
assert round(100.0 * repeat30.sum() / eligible.sum(), 1) == r["repeat_30d_pct"]
print("pandas equals SQL: gaps", gaps_pd["gap_days"].tolist(), "avg", avg_gap, "median", median_gap)
# the tie-breaker: user 4 has two orders at the same timestamp
print("user 4 rows by order_id:", o[o["user_id"] == 4][["order_id", "order_ts", "rn"]].to_dict("records"))
print("asserts passed")
```

**Output (my run):**
```text
gaps:
 user_id  gap_days
       1        10
       2        46
       4         0
       5         5
 avg_gap  median_gap
   15.25         7.5
 customers  repeaters  repeat_rate_pct  eligible_30d  repeat_30d  repeat_30d_pct
         6          4             66.7             5           3            60.0
pandas equals SQL: gaps [10, 46, 0, 5] avg 15.25 median 7.5
user 4 rows by order_id: [{'order_id': 7, 'order_ts': Timestamp('2024-03-01 10:00:00'), 'rn': 1}, {'order_id': 8, 'order_ts': Timestamp('2024-03-01 10:00:00'), 'rn': 2}]
asserts passed
```

**Edge cases:**
- Same-day orders need a tie-breaker. Without `order_id` in the `ORDER BY`, `ROW_NUMBER` may give either order as first, which only matters if the amounts or items differ, but the numbering must be deterministic.
- Single-order customers have no gap and are excluded from the average and median (they are not zero); they stay in the repeat-rate denominator.
- Median in SQLite: there is no `MEDIAN`. The row-number trick above works; `quantile(0.5)` in pandas interpolates linearly (7.5 here), which equals the two-middle-values average for an even count, though for other quantiles the two can differ.
- The 30-day repeat rate must exclude customers whose first order is younger than 30 days as of the as-of date, as above; otherwise recent cohorts look worse than they are.
- Gaps use calendar days from the date part; with elapsed hours instead, a 23:30 order followed by a 00:30 order is 0 days apart in hours-rounded terms but 1 calendar day (Q3, Q19).
- Cancelled or returned orders: decide whether they count as an order before numbering.

**Then explain:**
- Repeat purchase rate is "of customers with at least one order, the share with at least two"; this is a lifetime figure, so older customers raise it, which is why the 30-day version exists.
- `ROW_NUMBER` windows are Part 4/5 territory; the point here is the self join of order 1 to order 2 (`a.rn = 1 AND b.rn = 2`).
- The pandas pipeline: sort, `groupby('user_id').cumcount()`, merge first and second on `user_id`, then `.dt.days` after normalising to midnight.
- Dialects (not executed here): PostgreSQL has `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gap)`, BigQuery has `PERCENTILE_CONT` as an analytic function, MySQL has no built-in median, and Snowflake has `MEDIAN`.

**Follow-ups:**
- Time to second purchase by cohort month? Group the gap by first-order month.
- Why a median alongside the mean? One long gap (46 days) pulls the mean to 15.25 while the median is 7.5.
- Third purchase? Join `rn = 3`, or use `LAG(order_ts)` (Part 5).

**Common mistakes:**
- Subtracting `MAX` and `MIN` dates and calling it the first to second gap.
- No tie-breaker on equal timestamps.
- Counting customers with one order as a 0-day gap.
- Judging 30-day repeat for customers who have not had 30 days yet.
- Using `AVG` of integers divided with integer division (use 100.0 or CAST).

### Q21 ⭐⭐ 🟡 Monthly Transactions I (the LeetCode 1193 pattern): transactions(id, country, state, amount, trans_date) with state in ('approved','declined'). For each month (YYYY-MM) and country return the number of transactions, approved count, total amount and approved amount, using strftime and conditional aggregation (SUM(CASE ...)). Note the NULL country group and the MySQL DATE_FORMAT version as hedged text, then give the pandas groupby with named aggregation.
**Asked at:** public LeetCode-style problem bank (550 Game Play Analysis IV, 1193 Monthly Transactions I, 197 Rising Temperature and 262 Trips and Users known from search snippets and third-party write-ups, statements not opened), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Group by the month key `strftime('%Y-%m', trans_date)` and `country`, use `COUNT(*)` and `SUM(amount)` for totals, and `SUM(CASE WHEN state = 'approved' THEN ... ELSE 0 END)` for the approved counts and amounts.

**Schema and sample data:** seven transactions (the four LeetCode-style sample rows as I remember them, plus three I added: two with a NULL country and one DE row in February with no approved transaction). Convention: months are calendar months of the stored `YYYY-MM-DD` date; no time zone conversion.
```sql
CREATE TABLE transactions(id INTEGER PRIMARY KEY, country TEXT, state TEXT, amount INTEGER, trans_date TEXT);
INSERT INTO transactions VALUES
 (121,'US','approved',1000,'2018-12-18'),
 (122,'US','declined',2000,'2018-12-19'),
 (123,'US','approved',2000,'2019-01-01'),
 (124,'DE','approved',2000,'2019-01-07'),
 (125,NULL,'approved',500,'2019-01-10'),
 (126,NULL,'declined',100,'2019-01-11'),
 (127,'DE','declined',300,'2019-02-03');
```

**SQL answer:** `SQL_MAIN` in the Code block; `SQL_NO_ELSE` shows what happens without `ELSE 0`:
```sql
SELECT strftime('%Y-%m', trans_date) AS month,
       country,
       COUNT(*) AS trans_count,
       SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count,
       SUM(amount) AS trans_total_amount,
       SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
FROM transactions
GROUP BY strftime('%Y-%m', trans_date), country
ORDER BY month, country
```

**pandas answer:** identical to the Code block (named aggregation on helper columns, `dropna=False` to keep the NULL country group):
```py
x = t.assign(trans_date=pd.to_datetime(t["trans_date"]))
x["month"] = x["trans_date"].dt.strftime("%Y-%m")
x["approved_amount"] = x["amount"].where(x["state"] == "approved", 0)
x["is_approved"] = (x["state"] == "approved").astype(int)
pd_df = (x.groupby(["month", "country"], dropna=False)
          .agg(trans_count=("id", "count"), approved_count=("is_approved", "sum"),
               trans_total_amount=("amount", "sum"), approved_total_amount=("approved_amount", "sum"))
          .reset_index())
```

**Example:**
- 2018-12 US: two transactions (1000 approved, 2000 declined): count 2, approved 1, total 3000, approved total 1000.
- 2019-01 US: one approved 2000, so 1, 1, 2000, 2000. 2019-01 DE: one approved 2000, so 1, 1, 2000, 2000.
- 2019-01 NULL country: rows 125 (approved 500) and 126 (declined 100): count 2, approved 1, total 600, approved total 500. All NULL countries form one group.
- 2019-02 DE: one declined 300: count 1, approved count 0, total 300, approved total 0 (not NULL, thanks to `ELSE 0`).

**Code:** run with `python3 -I`. Compared after ordering by `month`, then `country` with the NULL country first (as SQLite sorts NULL first).
```python
# Q21: Monthly Transactions I (LeetCode 1193 pattern)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE transactions(id INTEGER PRIMARY KEY, country TEXT, state TEXT, amount INTEGER, trans_date TEXT);
INSERT INTO transactions VALUES
 (121,'US','approved',1000,'2018-12-18'),
 (122,'US','declined',2000,'2018-12-19'),
 (123,'US','approved',2000,'2019-01-01'),
 (124,'DE','approved',2000,'2019-01-07'),
 (125,NULL,'approved',500,'2019-01-10'),
 (126,NULL,'declined',100,'2019-01-11'),
 (127,'DE','declined',300,'2019-02-03');
"""
SQL_MAIN = """
SELECT strftime('%Y-%m', trans_date) AS month,
       country,
       COUNT(*) AS trans_count,
       SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count,
       SUM(amount) AS trans_total_amount,
       SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
FROM transactions
GROUP BY strftime('%Y-%m', trans_date), country
ORDER BY month, country
"""
SQL_NO_ELSE = """
SELECT strftime('%Y-%m', trans_date) AS month, country,
       SUM(CASE WHEN state = 'approved' THEN amount END) AS approved_total_amount
FROM transactions GROUP BY month, country ORDER BY month, country
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("without ELSE 0:")
print(pd.read_sql_query(SQL_NO_ELSE, con).to_string(index=False))

t = pd.read_sql_query("SELECT * FROM transactions", con)
# pd:main
x = t.assign(trans_date=pd.to_datetime(t["trans_date"]))
x["month"] = x["trans_date"].dt.strftime("%Y-%m")
x["approved_amount"] = x["amount"].where(x["state"] == "approved", 0)
x["is_approved"] = (x["state"] == "approved").astype(int)
pd_df = (x.groupby(["month", "country"], dropna=False)
          .agg(trans_count=("id", "count"), approved_count=("is_approved", "sum"),
               trans_total_amount=("amount", "sum"), approved_total_amount=("approved_amount", "sum"))
          .reset_index())
# pd:end
# compared after sorting by month, country with the NULL country first (as SQLite sorts NULL first)
pd_df = pd_df.sort_values(["month", "country"], na_position="first").reset_index(drop=True)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas equals SQL")
dropped = x.groupby(["month", "country"]).agg(n=("id", "count")).reset_index()
print("pandas default groupby (dropna=True) rows:", len(dropped), "versus SQL rows:", len(sql_df))
print("asserts passed")
```

**Output (my run):**
```text
  month country  trans_count  approved_count  trans_total_amount  approved_total_amount
2018-12      US            2               1                3000                   1000
2019-01     NaN            2               1                 600                    500
2019-01      DE            1               1                2000                   2000
2019-01      US            1               1                2000                   2000
2019-02      DE            1               0                 300                      0
without ELSE 0:
  month country  approved_total_amount
2018-12      US                 1000.0
2019-01     NaN                  500.0
2019-01      DE                 2000.0
2019-01      US                 2000.0
2019-02      DE                    NaN
pandas equals SQL
pandas default groupby (dropna=True) rows: 4 versus SQL rows: 5
asserts passed
```

**Edge cases:**
- NULL country: SQL `GROUP BY` puts all NULLs in one group, and `ORDER BY country` puts it first in SQLite (NULLs first for ascending order). pandas `groupby` drops NaN keys by default: the default call returned 4 rows versus SQL's 5, silently losing the NULL-country group; `dropna=False` keeps it.
- Group with no approved rows (2019-02 DE): `SUM(CASE ... END)` without `ELSE 0` returned NULL (shown as NaN in the `SQL_NO_ELSE` output), while the version with `ELSE 0` returned 0. The LeetCode statement, as I remember it, wants 0.
- Months with no transactions at all do not appear (no spine).
- Counts are integers; amounts here are integers. With decimal money, sum in integer minor units or round at the end.
- `trans_date` must be ISO text; the month key from a `DD/MM/YYYY` string would be wrong or NULL (Q1).
- Output order is not specified by the original problem, so I fixed one.

**Then explain:**
- Conditional aggregation computes several filtered metrics in one scan: the `CASE` returns 1 or the amount for approved rows and 0 for the rest, and `SUM` adds them.
- MySQL version (hedged, not executed here): `DATE_FORMAT(trans_date, '%Y-%m')` instead of `strftime`, and `SUM(IF(state = 'approved', 1, 0))` is common; `COUNT(*)` and the `CASE` forms work unchanged. PostgreSQL would use `TO_CHAR(trans_date, 'YYYY-MM')` or `DATE_TRUNC('month', trans_date)`, and also has `COUNT(*) FILTER (WHERE state = 'approved')` (not executed).
- The original problem labels the month as `YYYY-MM`; grouping on the expression, not the alias, is the portable form, though SQLite accepts the alias.
- Named aggregation in pandas: `agg(new_name=('column', 'func'))`; the helper columns `is_approved` and `approved_amount` are the pandas equivalent of the `CASE`.

**Follow-ups:**
- Approval rate? `approved_count * 1.0 / trans_count`; NULL-safe with `NULLIF`.
- Month spine so empty months show zeros? Q6.
- Country-level total across months? Remove the month from `GROUP BY` or use `ROLLUP` where supported (SQLite does not have it).

**Common mistakes:**
- Filtering `WHERE state = 'approved'`, which drops the declined rows from `trans_count` and `trans_total_amount`.
- Forgetting `ELSE 0` and getting NULL sums.
- Losing the NULL country group in pandas through `groupby`'s default `dropna=True`.
- Grouping by `strftime('%m')` alone, which merges the same month of different years.

### Q22 ⭐⭐ 🟡 Rising temperature with date gaps (the LeetCode 197 pattern): weather(id, record_date, temperature). Return the ids of days warmer than the previous calendar day. Solve with a self join on date(w1.record_date, '-1 day') = w2.record_date and with LAG, and show that LAG compares with the previous row, which is wrong when a calendar day is missing, so the self join (or LAG plus a check that the date gap is exactly 1) is the correct one. pandas: shift with a date index and asfreq('D') or merge on shifted dates.
**Asked at:** public LeetCode-style problem bank (550 Game Play Analysis IV, 1193 Monthly Transactions I, 197 Rising Temperature and 262 Trips and Users known from search snippets and third-party write-ups, statements not opened), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Self join `weather` to itself on `w2.record_date = date(w1.record_date, '-1 day')` and keep rows where `w1.temperature > w2.temperature`; the join is calendar-based, so a missing day simply has no partner, whereas plain `LAG` compares with the previous row and gets gaps wrong unless you also check the date difference is exactly 1.

**Schema and sample data:** eleven readings with ids in date order. 2015-01-05 is missing (a gap), 2015-01-31 has no 2015-01-30 before it, and the data crosses a month boundary and the leap day of 2016. Convention: dates are ISO calendar dates, no time zone.
```sql
CREATE TABLE weather(id INTEGER PRIMARY KEY, record_date TEXT, temperature INTEGER);
INSERT INTO weather VALUES
 (1,'2015-01-01',10),(2,'2015-01-02',25),(3,'2015-01-03',20),(4,'2015-01-04',30),
 (5,'2015-01-06',35),(6,'2015-01-07',40),
 (7,'2015-01-31',20),(8,'2015-02-01',25),
 (9,'2016-02-28',15),(10,'2016-02-29',18),(11,'2016-03-01',20);
```

**SQL answer:** `SQL_JOIN` in the Code block, with `SQL_LAG_NAIVE` and `SQL_LAG_CHECKED` for comparison. (Part 5 Q13 covers the LAG mechanics in depth; this question is the LeetCode 197 pattern.)
```sql
SELECT w1.id
FROM weather w1
JOIN weather w2 ON w2.record_date = date(w1.record_date, '-1 day')
WHERE w1.temperature > w2.temperature
ORDER BY w1.id
```

**pandas answer:** identical to the Code block; two calendar-correct versions, `asfreq('D')` plus `shift(1)`, and a merge on date plus one day:
```py
w = weather.assign(record_date=pd.to_datetime(weather["record_date"])).set_index("record_date").sort_index()
daily = w.asfreq("D")                                   # inserts NaN rows for missing calendar days
rising = daily["temperature"] > daily["temperature"].shift(1)
ids_asfreq = sorted(daily.loc[rising, "id"].astype(int).tolist())
prev = weather.assign(record_date=pd.to_datetime(weather["record_date"]) + pd.Timedelta(days=1))
ids_merge = sorted(weather.assign(record_date=pd.to_datetime(weather["record_date"]))
                   .merge(prev[["record_date", "temperature"]], on="record_date", suffixes=("", "_prev"))
                   .query("temperature > temperature_prev")["id"].tolist())
```

**Example:**
- id 2 (01-02, 25) beats 01-01 (10): yes. id 3 (20) is lower than 25: no. id 4 (30) beats 20: yes.
- id 5 (01-06, 35) is warmer than the last row before it (id 4, 30 on 01-04), but 01-05 is missing, so there is no row for the previous calendar day: no. The naive LAG returns it, which is wrong.
- id 6 (01-07, 40) beats 01-06 (35): yes. id 7 (01-31) has no 01-30 row: no. id 8 (02-01, 25) beats 01-31 (20): yes, the month boundary works through `date()`.
- 2016 is a leap year: id 10 (02-29, 18) beats 02-28 (15): yes; id 11 (03-01, 20) beats 02-29 (18): yes, because `date('2016-03-01', '-1 day')` is `2016-02-29`.
- Result ids: 2, 4, 6, 8, 10, 11.

**Code:** run with `python3 -I`. Results are compared as sorted lists of ids.
```python
# Q22: Rising Temperature (LeetCode 197 pattern) with date gaps: self join, LAG, pandas asfreq / merge
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE weather(id INTEGER PRIMARY KEY, record_date TEXT, temperature INTEGER);
INSERT INTO weather VALUES
 (1,'2015-01-01',10),(2,'2015-01-02',25),(3,'2015-01-03',20),(4,'2015-01-04',30),
 (5,'2015-01-06',35),(6,'2015-01-07',40),
 (7,'2015-01-31',20),(8,'2015-02-01',25),
 (9,'2016-02-28',15),(10,'2016-02-29',18),(11,'2016-03-01',20);
"""
SQL_JOIN = """
SELECT w1.id
FROM weather w1
JOIN weather w2 ON w2.record_date = date(w1.record_date, '-1 day')
WHERE w1.temperature > w2.temperature
ORDER BY w1.id
"""
SQL_LAG_NAIVE = """
SELECT id FROM (
  SELECT id, temperature, LAG(temperature) OVER (ORDER BY record_date) AS prev_temp FROM weather
) WHERE temperature > prev_temp ORDER BY id
"""
SQL_LAG_CHECKED = """
SELECT id FROM (
  SELECT id, temperature, record_date,
         LAG(temperature) OVER (ORDER BY record_date) AS prev_temp,
         LAG(record_date) OVER (ORDER BY record_date) AS prev_date
  FROM weather
) WHERE temperature > prev_temp AND julianday(record_date) - julianday(prev_date) = 1
ORDER BY id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
join_ids = [r[0] for r in con.execute(SQL_JOIN)]
naive_ids = [r[0] for r in con.execute(SQL_LAG_NAIVE)]
checked_ids = [r[0] for r in con.execute(SQL_LAG_CHECKED)]
print("self join:", join_ids)
print("naive LAG:", naive_ids)
print("LAG + gap check:", checked_ids)
assert join_ids == checked_ids

weather = pd.read_sql_query("SELECT * FROM weather", con)
# pd:main
w = weather.assign(record_date=pd.to_datetime(weather["record_date"])).set_index("record_date").sort_index()
daily = w.asfreq("D")                                   # inserts NaN rows for missing calendar days
rising = daily["temperature"] > daily["temperature"].shift(1)
ids_asfreq = sorted(daily.loc[rising, "id"].astype(int).tolist())
prev = weather.assign(record_date=pd.to_datetime(weather["record_date"]) + pd.Timedelta(days=1))
ids_merge = sorted(weather.assign(record_date=pd.to_datetime(weather["record_date"]))
                   .merge(prev[["record_date", "temperature"]], on="record_date", suffixes=("", "_prev"))
                   .query("temperature > temperature_prev")["id"].tolist())
# pd:end
# compared as sorted id lists
assert ids_asfreq == join_ids and ids_merge == join_ids
print("pandas asfreq('D') + shift:", ids_asfreq)
print("pandas merge on date + 1 day:", ids_merge)
print("pandas naive shift on the raw sorted rows:",
      sorted(w.loc[w["temperature"] > w["temperature"].shift(1), "id"].tolist()))
print("asfreq rows:", len(daily), "of which missing days:", int(daily["id"].isna().sum()))
print("asserts passed")
```

**Output (my run):**
```text
self join: [2, 4, 6, 8, 10, 11]
naive LAG: [2, 4, 5, 6, 8, 10, 11]
LAG + gap check: [2, 4, 6, 8, 10, 11]
pandas asfreq('D') + shift: [2, 4, 6, 8, 10, 11]
pandas merge on date + 1 day: [2, 4, 6, 8, 10, 11]
pandas naive shift on the raw sorted rows: [2, 4, 5, 6, 8, 10, 11]
asfreq rows: 426 of which missing days: 415
asserts passed
```

**Edge cases:**
- Gap: the naive LAG returned an extra id 5 (`[2, 4, 5, 6, 8, 10, 11]`), the join and the checked LAG did not. pandas `shift(1)` on the raw sorted rows gave the same wrong id 5.
- `asfreq('D')` fills every missing day between the first and last date: here 426 rows, 415 of them missing days, because the data spans 2015 to 2016. Fine for a toy table, wasteful for sparse data over many years; the merge on date plus one day avoids that.
- A NULL temperature never compares as greater, in SQL (unknown) or pandas (NaN comparison is False), so such a row and the row after it drop out.
- Duplicate dates would produce duplicate pairs in the self join; the LeetCode problem assumes one row per date. Dedupe first.
- Dates stored as text must be ISO; `date()` returns NULL otherwise and the join silently matches nothing.
- The problem returns ids, not dates; the result order is unspecified, so I ordered by id.

**Then explain:**
- Self join: each row finds "yesterday" by key, so correctness does not depend on the data having no gaps or on the sort order.
- LAG: positional; fix it by also selecting `LAG(record_date)` and requiring a 1-day difference (`julianday` difference equal to 1, which is exact for whole dates; for timestamps take `date()` first).
- pandas: `asfreq('D')` reindexes onto a complete daily index so `shift(1)` is a calendar shift; the merge version moves a copy of the table forward one day and joins on the date, the pandas twin of the SQL self join.
- Dialects (not executed here): the LeetCode statement is, as I remember it, a MySQL problem, solved there with `DATEDIFF(w1.record_date, w2.record_date) = 1`; PostgreSQL uses `w1.record_date - w2.record_date = 1` for `DATE` columns or `w2.record_date + INTERVAL '1 day' = w1.record_date`; BigQuery uses `DATE_DIFF` or `DATE_SUB`.

**Follow-ups:**
- Warmer than the average of the previous 3 days? A range or self join over dates (Part 5 moving averages), again with gap awareness.
- Compare with the same day last week? Join on `date(record_date, '-7 days')`.
- Many years of daily data? Index `record_date` so the self join uses an index lookup (I did not time it).

**Common mistakes:**
- `LAG` without checking the date gap.
- Joining on `id = id - 1`, which only works when ids happen to follow dates.
- Subtracting dates as text.
- Treating a row after a gap as comparable with the last earlier row (the id 5 case above).

### Q23 ⭐⭐ 🟡 Cancellation rate by day (the LeetCode 262 pattern, Trips and Users): trips(id, client_id, driver_id, status, request_at) and users(user_id, banned, role). For request dates between 2013-10-01 and 2013-10-03 return the cancellation rate per day counting only trips whose client and driver are both unbanned, rounded to 2 decimals. Show the date filter (half-open on a timestamp), the double join to users, conditional aggregation, and a day with no trips (absent versus rate 0 versus NULL).
**Asked at:** public LeetCode-style problem bank (550 Game Play Analysis IV, 1193 Monthly Transactions I, 197 Rising Temperature and 262 Trips and Users known from search snippets and third-party write-ups, statements not opened), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Filter trips to the date range with a half-open timestamp range, inner-join `users` twice (client and driver, both `banned = 'No'`), then take `SUM(status <> 'completed') / COUNT(*)` per day; a day with no qualifying trips simply has no row, which is a choice I state (absent, 0 or NULL) rather than leave to the join.

**Schema and sample data:** two banned users (client 2, driver 13); `request_at` is a full timestamp so the date-filter trap is real. Date convention: the day is the first 10 characters of `request_at` as stored, no time-zone conversion (week start is not used in this question).
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, banned TEXT, role TEXT);
CREATE TABLE trips(id INTEGER PRIMARY KEY, client_id INTEGER, driver_id INTEGER,
                   status TEXT, request_at TEXT);
INSERT INTO users VALUES (1,'No','client'),(2,'Yes','client'),(3,'No','client'),(4,'No','client'),
  (10,'No','driver'),(11,'No','driver'),(12,'No','driver'),(13,'Yes','driver');
INSERT INTO trips VALUES
 (1,1,10,'completed','2013-10-01 08:00:00'),
 (2,2,11,'cancelled_by_driver','2013-10-01 09:00:00'),
 (3,3,12,'completed','2013-10-01 10:00:00'),
 (4,4,13,'cancelled_by_client','2013-10-01 11:00:00'),
 (5,1,11,'cancelled_by_client','2013-10-01 12:00:00'),
 (6,2,10,'cancelled_by_driver','2013-10-02 09:00:00'),
 (7,4,13,'completed','2013-10-02 10:00:00'),
 (8,3,12,'completed','2013-10-03 10:00:00'),
 (9,1,10,'cancelled_by_driver','2013-10-03 23:30:00'),
 (10,3,11,'completed','2013-10-04 09:00:00');
```

**SQL answer:** `SQL_MAIN` in the Code block, with `:lo` and `:hi` as parameters. The window is `request_at >= :lo AND request_at < date(:hi, '+1 day')`, so a trip at 23:30 on the last day is kept. `SQL_SPINE` adds a day spine to show the three options for an empty day.
```sql
SELECT substr(t.request_at, 1, 10) AS day,
       ROUND(1.0 * SUM(CASE WHEN t.status <> 'completed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate
FROM trips t
JOIN users c ON c.user_id = t.client_id AND c.banned = 'No' AND c.role = 'client'
JOIN users d ON d.user_id = t.driver_id AND d.banned = 'No' AND d.role = 'driver'
WHERE t.request_at >= :lo AND t.request_at < date(:hi, '+1 day')
GROUP BY substr(t.request_at, 1, 10)
ORDER BY day
```

**pandas answer:** the same filter with Timestamps, `isin` on the unbanned client and driver ids, then the mean of a boolean (cancelled) per day. This is the `cancel_rate` function in the Code block; the key lines are:
```py
    ok_c = users.loc[(users["banned"] == "No") & (users["role"] == "client"), "user_id"]
    ok_d = users.loc[(users["banned"] == "No") & (users["role"] == "driver"), "user_id"]
    t = t[t["client_id"].isin(ok_c) & t["driver_id"].isin(ok_d)]
    g = t.assign(day=t["request_at"].dt.strftime("%Y-%m-%d"),
                 cancelled=(t["status"] != "completed")).groupby("day")["cancelled"].mean().round(2)
```

**Example:** banned: client 2 and driver 13. 2013-10-01: trips 1, 3 and 5 qualify (trip 2 has banned client 2, trip 4 has banned driver 13); 1 of 3 is cancelled (trip 5), so 1/3 = 0.33. 2013-10-02: trip 6 has banned client 2 and trip 7 has banned driver 13, so nothing qualifies and the day has no row. 2013-10-03: trip 8 completed, trip 9 (23:30) cancelled by the driver, so 1/2 = 0.50. Trip 10 on 2013-10-04 is outside the window.

**Code:** run with `python3 -I`.
```python
# Q23: cancellation rate by day (LeetCode 262 pattern), SQL vs pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, banned TEXT, role TEXT);
CREATE TABLE trips(id INTEGER PRIMARY KEY, client_id INTEGER, driver_id INTEGER,
                   status TEXT, request_at TEXT);
INSERT INTO users VALUES (1,'No','client'),(2,'Yes','client'),(3,'No','client'),(4,'No','client'),
  (10,'No','driver'),(11,'No','driver'),(12,'No','driver'),(13,'Yes','driver');
INSERT INTO trips VALUES
 (1,1,10,'completed','2013-10-01 08:00:00'),
 (2,2,11,'cancelled_by_driver','2013-10-01 09:00:00'),
 (3,3,12,'completed','2013-10-01 10:00:00'),
 (4,4,13,'cancelled_by_client','2013-10-01 11:00:00'),
 (5,1,11,'cancelled_by_client','2013-10-01 12:00:00'),
 (6,2,10,'cancelled_by_driver','2013-10-02 09:00:00'),
 (7,4,13,'completed','2013-10-02 10:00:00'),
 (8,3,12,'completed','2013-10-03 10:00:00'),
 (9,1,10,'cancelled_by_driver','2013-10-03 23:30:00'),
 (10,3,11,'completed','2013-10-04 09:00:00');
"""
SQL_MAIN = """
SELECT substr(t.request_at, 1, 10) AS day,
       ROUND(1.0 * SUM(CASE WHEN t.status <> 'completed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate
FROM trips t
JOIN users c ON c.user_id = t.client_id AND c.banned = 'No' AND c.role = 'client'
JOIN users d ON d.user_id = t.driver_id AND d.banned = 'No' AND d.role = 'driver'
WHERE t.request_at >= :lo AND t.request_at < date(:hi, '+1 day')
GROUP BY substr(t.request_at, 1, 10)
ORDER BY day
"""
SQL_BETWEEN = """
SELECT substr(request_at, 1, 10) AS day, COUNT(*) AS trips
FROM trips WHERE request_at BETWEEN :lo AND :hi GROUP BY 1 ORDER BY 1
"""
SQL_SPINE = """
WITH RECURSIVE days(day) AS (
  SELECT :lo UNION ALL SELECT date(day, '+1 day') FROM days WHERE day < :hi
), ok AS (
  SELECT substr(t.request_at, 1, 10) AS day, t.status
  FROM trips t
  JOIN users c ON c.user_id = t.client_id AND c.banned = 'No' AND c.role = 'client'
  JOIN users d ON d.user_id = t.driver_id AND d.banned = 'No' AND d.role = 'driver'
)
SELECT days.day, COUNT(ok.day) AS trips,
       ROUND(1.0 * SUM(CASE WHEN ok.status <> 'completed' THEN 1 ELSE 0 END) / NULLIF(COUNT(ok.day), 0), 2) AS rate_null,
       COALESCE(ROUND(1.0 * SUM(CASE WHEN ok.status <> 'completed' THEN 1 ELSE 0 END) / NULLIF(COUNT(ok.day), 0), 2), 0) AS rate_zero
FROM days LEFT JOIN ok ON ok.day = days.day
GROUP BY days.day ORDER BY days.day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"lo": "2013-10-01", "hi": "2013-10-03"}
sql_df = pd.read_sql_query(SQL_MAIN, con, params=P)
print("SQL (2013-10-01..2013-10-03):")
print(sql_df.to_string(index=False))
print("BETWEEN '2013-10-01' AND '2013-10-03' trips per day (drops the 23:30 trip on 10-03):")
print(pd.read_sql_query(SQL_BETWEEN, con, params=P).to_string(index=False))
print("SQL with day spine (absent day -> NULL or 0):")
print(pd.read_sql_query(SQL_SPINE, con, params=P).to_string(index=False))
print("same SQL, window widened to 2013-10-04:")
print(pd.read_sql_query(SQL_MAIN, con, params={"lo": "2013-10-01", "hi": "2013-10-04"}).to_string(index=False))

trips = pd.read_sql_query("SELECT * FROM trips", con)
users = pd.read_sql_query("SELECT * FROM users", con)

def cancel_rate(trips, users, lo, hi):
    t = trips.assign(request_at=pd.to_datetime(trips["request_at"]))
    t = t[(t["request_at"] >= pd.Timestamp(lo)) & (t["request_at"] < pd.Timestamp(hi) + pd.Timedelta(days=1))]
    ok_c = users.loc[(users["banned"] == "No") & (users["role"] == "client"), "user_id"]
    ok_d = users.loc[(users["banned"] == "No") & (users["role"] == "driver"), "user_id"]
    t = t[t["client_id"].isin(ok_c) & t["driver_id"].isin(ok_d)]
    g = t.assign(day=t["request_at"].dt.strftime("%Y-%m-%d"),
                 cancelled=(t["status"] != "completed")).groupby("day")["cancelled"].mean().round(2)
    return g.reset_index(name="cancellation_rate")

pd_df = cancel_rate(trips, users, "2013-10-01", "2013-10-03")
# compared after sorting by day
assert pd_df.sort_values("day").reset_index(drop=True).equals(sql_df.sort_values("day").reset_index(drop=True)), (pd_df, sql_df)
wide = pd.read_sql_query(SQL_MAIN, con, params={"lo": "2013-10-01", "hi": "2013-10-04"})
assert cancel_rate(trips, users, "2013-10-01", "2013-10-04").equals(wide)
print("pandas:")
print(pd_df.to_string(index=False))
print("asserts passed: SQL == pandas for both windows")
```

**Output (my run):**
```text
SQL (2013-10-01..2013-10-03):
       day  cancellation_rate
2013-10-01               0.33
2013-10-03               0.50
BETWEEN '2013-10-01' AND '2013-10-03' trips per day (drops the 23:30 trip on 10-03):
       day  trips
2013-10-01      5
2013-10-02      2
SQL with day spine (absent day -> NULL or 0):
       day  trips  rate_null  rate_zero
2013-10-01      3       0.33       0.33
2013-10-02      0        NaN       0.00
2013-10-03      2       0.50       0.50
same SQL, window widened to 2013-10-04:
       day  cancellation_rate
2013-10-01               0.33
2013-10-03               0.50
2013-10-04               0.00
pandas:
       day  cancellation_rate
2013-10-01               0.33
2013-10-03               0.50
asserts passed: SQL == pandas for both windows
```

**Edge cases:**
- Day with no qualifying trips (2013-10-02): the plain `GROUP BY` returns no row at all. With a day spine and `LEFT JOIN`, `COUNT(ok.day)` is 0 and the rate is NULL because I divide by `NULLIF(COUNT(...), 0)`; wrapping it in `COALESCE(..., 0)` gives 0.00, which says "nothing was cancelled" when the truth is "nothing happened". Which one to show is a reporting decision; I would show NULL (or a blank) and keep the trip count next to it.
- A day that does exist but has no cancellations is a real 0.00. In my run that day appears when I widen the window to 2013-10-04 (one completed trip, rate 0.00); that is the difference between "rate 0" and "no row".
- `BETWEEN '2013-10-01' AND '2013-10-03'` on a timestamp column drops the whole of 2013-10-03 (both the 10:00 and the 23:30 trips), because every time on that day is greater than the bare date string `'2013-10-03'`. The second printed table shows trips per day with that filter: 10-03 is missing.
- Rounding: SQLite `ROUND(x, 2)` and pandas `.round(2)` returned the same values here; I compared the rounded results with `equals`. If you compare unrounded floats, use a tolerance.
- Orphans: a trip whose client or driver id is missing from `users` is dropped by the inner joins, and by `isin` in pandas; a `LEFT JOIN` with `banned IS NULL` would keep it, so decide whether unknown users count as unbanned.
- Roles: I also test `role = 'client'` and `role = 'driver'` on the joins. If ids are unique across roles (as in the public problem, as I remember it) this is redundant but protects against a driver id being used as a client id.

**Then explain:**
- The two joins to `users` are inner joins, so the ban rule is also the filter; putting `banned = 'No'` in `ON` or in `WHERE` gives the same rows for inner joins.
- Conditional aggregation: `SUM(CASE WHEN status <> 'completed' THEN 1 ELSE 0 END)` counts both cancellation statuses; `1.0 *` forces float division in SQLite (integer division would give 0).
- Half-open range: `>= lo AND < next day` works for dates, timestamps with fractions, and composes with the next window; it also lets an index on `request_at` be used (not timed here).
- Dialect (not executed): MySQL versions of this problem often write `request_at BETWEEN '2013-10-01' AND '2013-10-03'` because the public table stores a date-like string; that is only safe if there is no time part. PostgreSQL and BigQuery can cast with `request_at::date` or `DATE(request_at)` but that hides the column from an index; the half-open form avoids it.
- The public problem statement and its expected output were not opened for this book; my sample data is my own.

**Follow-ups:**
- "Rate per day per city?" Add `city` to `GROUP BY`, and keep the spine as days x cities so empty cells are explicit.
- "Weekly instead of daily?" Change the bucket; state the week start (Part 6 Q5).
- "Count a banned user's trips separately?" Move the ban test into a `CASE` instead of the join, so banned trips are counted in a second column.

**Common mistakes:**
- `BETWEEN` with a bare end date on a timestamp column (loses the last day).
- Joining `users` once, so only the client (or only the driver) is checked.
- Dividing by all trips including banned-user trips, or counting `status = 'cancelled_by_client'` only.
- Integer division (`SUM(...) / COUNT(*)` without `1.0 *`) giving 0.
- `COALESCE(rate, 0)` that turns "no trips" into a perfect-looking 0.00.

### Q24 ⭐⭐ 🟡 Month-to-date versus prior month-to-date: daily_sales(sale_date, amount) and a fixed as-of date such as '2024-03-17'. Return revenue from the first of the as-of month to the as-of date, revenue from the first of the previous month to the same day number (handle a day number that does not exist in the shorter month, such as the 31st), and the percent difference. Show the half-open ranges built with date modifiers, and the pandas version with boolean masks and DateOffset. State why comparing a partial month to a full month is the classic error.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Build both windows as half-open ranges from the as-of date: current is `[first of month, as_of + 1 day)`, prior is `[first of previous month, same day number + 1)` capped at the first of the as-of month; compare partial to partial, and note that SQLite's `'-1 month'` overflows (`2024-03-31` minus one month is `2024-03-02`), so I compute the prior end from the month start instead.

**Schema and sample data:** every day of February 2024 (29 days, leap year) at 100 and every day of March 2024 at 120, generated with a recursive CTE so the data is easy to check by hand. As-of dates are fixed in the code (never `now`). No time zone: `sale_date` is a plain date.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
WITH RECURSIVE d(x) AS (SELECT '2024-02-01' UNION ALL SELECT date(x, '+1 day') FROM d WHERE x < '2024-03-31')
INSERT INTO daily_sales SELECT x, CASE WHEN x < '2024-03-01' THEN 100 ELSE 120 END FROM d;
```

**SQL answer:** `SQL_MAIN` in the Code block with `:asof` as a parameter. The pieces are `date(:asof, 'start of month')` (first of the month), `date(:asof, '+1 day')` (exclusive current end), `date(:asof, 'start of month', '-1 month')` (first of the previous month; safe because it starts from the 1st) and the prior exclusive end `MIN(prev_start + day_number days, first of the as-of month)`, which clips the 31st to the end of a shorter month.
```sql
WITH b AS (
  SELECT date(:asof, 'start of month') AS cur_lo,
         date(:asof, '+1 day') AS cur_hi,
         date(:asof, 'start of month', '-1 month') AS prev_lo,
         MIN(date(:asof, 'start of month', '-1 month', '+' || CAST(strftime('%d', :asof) AS INTEGER) || ' days'),
             date(:asof, 'start of month')) AS prev_hi
), r AS (
  SELECT b.*,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= cur_lo AND sale_date < cur_hi) AS mtd,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= prev_lo AND sale_date < prev_hi) AS prev_mtd,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= prev_lo AND sale_date < cur_lo) AS prev_full
  FROM b
)
SELECT :asof AS asof, cur_lo, cur_hi, prev_lo, prev_hi, mtd, prev_mtd,
       ROUND(100.0 * (mtd - prev_mtd) / NULLIF(prev_mtd, 0), 1) AS pct_vs_prev_mtd,
       prev_full,
       ROUND(100.0 * (mtd - prev_full) / NULLIF(prev_full, 0), 1) AS pct_vs_full_prev_month
FROM r
```

**pandas answer:** boolean masks on `sale_date` with Timestamps. `asof - pd.DateOffset(months=1)` clips by itself to the last valid day, so the prior end needs no extra `MIN`:
```py
    asof = pd.Timestamp(asof)
    cur_lo = asof.replace(day=1)
    cur_hi = asof + pd.Timedelta(days=1)
    prev_asof = asof - pd.DateOffset(months=1)     # DateOffset clips: 2024-03-31 -> 2024-02-29
    prev_lo = cur_lo - pd.DateOffset(months=1)
    prev_hi = prev_asof + pd.Timedelta(days=1)
    m = lambda lo, hi: int(ds.loc[(ds["sale_date"] >= lo) & (ds["sale_date"] < hi), "amount"].sum())
    mt, pm = m(cur_lo, cur_hi), m(prev_lo, prev_hi)
    full = m(prev_lo, cur_lo)
```

**Example:** as-of 2024-03-17. Current window `[2024-03-01, 2024-03-18)` is 17 days at 120 = 2040. Prior window `[2024-02-01, 2024-02-18)` is 17 days at 100 = 1700. Difference (2040 - 1700) / 1700 = 20.0%. The wrong comparison is 2040 against all of February (2900): -29.7%, a decline that is only an artefact of 17 days versus 29. As-of 2024-03-31: the 31st does not exist in February, so the prior window is capped at `[2024-02-01, 2024-03-01)`, the whole of February (2900), against 31 days of March (3720): 28.3%. As-of 2024-03-01: one day each, 120 versus 100: 20.0%.

**Code:** run with `python3 -I`.
```python
# Q24: month-to-date vs prior month-to-date, fixed as-of dates
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
WITH RECURSIVE d(x) AS (SELECT '2024-02-01' UNION ALL SELECT date(x, '+1 day') FROM d WHERE x < '2024-03-31')
INSERT INTO daily_sales SELECT x, CASE WHEN x < '2024-03-01' THEN 100 ELSE 120 END FROM d;
"""
# ranges are half-open [lo, hi). The prior hi is the same day number + 1, capped at the first of the as-of month.
SQL_MAIN = """
WITH b AS (
  SELECT date(:asof, 'start of month') AS cur_lo,
         date(:asof, '+1 day') AS cur_hi,
         date(:asof, 'start of month', '-1 month') AS prev_lo,
         MIN(date(:asof, 'start of month', '-1 month', '+' || CAST(strftime('%d', :asof) AS INTEGER) || ' days'),
             date(:asof, 'start of month')) AS prev_hi
), r AS (
  SELECT b.*,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= cur_lo AND sale_date < cur_hi) AS mtd,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= prev_lo AND sale_date < prev_hi) AS prev_mtd,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= prev_lo AND sale_date < cur_lo) AS prev_full
  FROM b
)
SELECT :asof AS asof, cur_lo, cur_hi, prev_lo, prev_hi, mtd, prev_mtd,
       ROUND(100.0 * (mtd - prev_mtd) / NULLIF(prev_mtd, 0), 1) AS pct_vs_prev_mtd,
       prev_full,
       ROUND(100.0 * (mtd - prev_full) / NULLIF(prev_full, 0), 1) AS pct_vs_full_prev_month
FROM r
"""
SQL_NAIVE = "SELECT date(:asof, '-1 month') AS naive_prev_same_day"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
asofs = ["2024-03-17", "2024-03-31", "2024-03-01"]
sql_df = pd.concat([pd.read_sql_query(SQL_MAIN, con, params={"asof": a}) for a in asofs], ignore_index=True)
print(sql_df.T.to_string(header=False))
for a in ["2024-03-31", "2023-03-31"]:
    print("SQLite date('%s','-1 month') =" % a, con.execute(SQL_NAIVE, {"asof": a}).fetchone()[0])

ds = pd.read_sql_query("SELECT * FROM daily_sales", con)
ds["sale_date"] = pd.to_datetime(ds["sale_date"])

def mtd(ds, asof):
    asof = pd.Timestamp(asof)
    cur_lo = asof.replace(day=1)
    cur_hi = asof + pd.Timedelta(days=1)
    prev_asof = asof - pd.DateOffset(months=1)     # DateOffset clips: 2024-03-31 -> 2024-02-29
    prev_lo = cur_lo - pd.DateOffset(months=1)
    prev_hi = prev_asof + pd.Timedelta(days=1)
    m = lambda lo, hi: int(ds.loc[(ds["sale_date"] >= lo) & (ds["sale_date"] < hi), "amount"].sum())
    mt, pm = m(cur_lo, cur_hi), m(prev_lo, prev_hi)
    full = m(prev_lo, cur_lo)
    return dict(asof=asof.strftime("%Y-%m-%d"), cur_lo=cur_lo.strftime("%Y-%m-%d"), cur_hi=cur_hi.strftime("%Y-%m-%d"),
                prev_lo=prev_lo.strftime("%Y-%m-%d"), prev_hi=prev_hi.strftime("%Y-%m-%d"), mtd=mt, prev_mtd=pm,
                pct_vs_prev_mtd=round(100.0 * (mt - pm) / pm, 1), prev_full=full,
                pct_vs_full_prev_month=round(100.0 * (mt - full) / full, 1))
pd_df = pd.DataFrame([mtd(ds, a) for a in asofs])
# one row per as-of date, compared in the order of asofs
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas DateOffset: Timestamp('2024-03-31') - DateOffset(months=1) =", (pd.Timestamp("2024-03-31") - pd.DateOffset(months=1)).date())
print("asserts passed: SQL == pandas for", asofs)
```

**Output (my run):**
```text
asof                    2024-03-17  2024-03-31  2024-03-01
cur_lo                  2024-03-01  2024-03-01  2024-03-01
cur_hi                  2024-03-18  2024-04-01  2024-03-02
prev_lo                 2024-02-01  2024-02-01  2024-02-01
prev_hi                 2024-02-18  2024-03-01  2024-02-02
mtd                           2040        3720         120
prev_mtd                      1700        2900         100
pct_vs_prev_mtd               20.0        28.3        20.0
prev_full                     2900        2900        2900
pct_vs_full_prev_month       -29.7        28.3       -95.9
SQLite date('2024-03-31','-1 month') = 2024-03-02
SQLite date('2023-03-31','-1 month') = 2023-03-03
pandas DateOffset: Timestamp('2024-03-31') - DateOffset(months=1) = 2024-02-29
asserts passed: SQL == pandas for ['2024-03-17', '2024-03-31', '2024-03-01']
```

**Edge cases:**
- The 31st: the prior window is shorter in days than the current one (29 versus 31 in my run). That is a business decision to state; the alternative is to compare to the full previous month on the last day of the month.
- SQLite `date('2024-03-31', '-1 month')` returned `2024-03-02` and `date('2023-03-31', '-1 month')` returned `2023-03-03`, so using it as the prior end silently shifts the window. pandas `DateOffset(months=1)` returned `2024-02-29` (clipped).
- Days with no sales rows: `COALESCE(SUM(...), 0)` keeps the result at 0, but a missing day inside the window also shortens the comparison; check the day count if the feed can have gaps.
- Zero prior revenue: `NULLIF(prev_mtd, 0)` returns NULL instead of a division error (pandas would give `inf`; I did not hit it here).
- January as the as-of month: `'-1 month'` from the 1st goes to December of the previous year correctly, because it starts from day 1. I did not add January data to the sample, so this is stated, not run.

**Then explain:**
- Partial month versus full month is the classic error: on the 17th you have about half a month of sales on one side and a whole month on the other, so growth looks like a collapse (-29.7% above) even though the same-days comparison is +20.0%.
- Half-open ranges (`>= lo AND < hi`) make "through the as-of date inclusive" simply `hi = as_of + 1 day`, and they stay correct if `sale_date` ever becomes a timestamp.
- Do the month arithmetic from the first of the month; only day-of-month arithmetic from the 29th to the 31st misbehaves.
- Dialects (not executed): PostgreSQL `date_trunc('month', d)` and `d - INTERVAL '1 month'` clip to the end of the month; MySQL `DATE_SUB(d, INTERVAL 1 MONTH)` also clips; BigQuery `DATE_SUB(d, INTERVAL 1 MONTH)` clips; I am quoting these from memory.

**Follow-ups:**
- "Same-day-last-year (year-to-date)?" Same pattern with `'-1 year'`; 29 February needs the same capping rule.
- "Daily run-rate projection for the month?" That is a forecast; say it is, and keep it separate from the actuals.
- "Business-day-aligned comparison?" Join a calendar table (Q31) and compare the first n working days.

**Common mistakes:**
- Comparing the partial current month to the full previous month.
- `date(asof, '-1 month')` on the 31st (overflow into the wrong month).
- `BETWEEN` with the as-of date as a timestamp (loses the last day) or an exclusive end that is off by one.
- Using `now`/`today` so the figure changes on every run and can not be tested.

### Q25 ⭐⭐ 🟡 Fiscal years and quarters (India, April to March): orders(order_id, order_ts, amount). Derive the fiscal year label (FY2024-25 for April 2024 to March 2025), fiscal quarter (Q1 = April to June) and fiscal month number in SQLite with strftime and CASE or arithmetic, then total revenue per fiscal quarter. Give the pandas versions with dt.to_period('Q-MAR') and dt.qyear / dt.quarter, and a check on 31 March versus 1 April. Mention that quarter and DATE_TRUNC fiscal options in other engines differ (hedged, not executed).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Fiscal year starts in April: fiscal start year = calendar year minus 1 when the month is January to March, fiscal month = `(month + 8) % 12 + 1`, fiscal quarter = `(month + 8) % 12 / 3 + 1`; I label the year as `FY2024-25` for April 2024 to March 2025 and check the boundary rows 31 March and 1 April.

**Schema and sample data:** eight orders around the boundaries, ISO text timestamps. Convention: timestamps as stored (no time-zone conversion), fiscal year April to March (India), label uses the start year.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-03-31 23:59:59',100),(2,'2024-04-01 00:00:00',200),(3,'2024-06-30 12:00:00',300),
 (4,'2024-07-01 09:00:00',400),(5,'2024-12-25 10:00:00',500),(6,'2025-01-15 10:00:00',600),
 (7,'2025-03-31 18:00:00',700),(8,'2025-04-01 08:00:00',800);
```

**SQL answer:** `SQL_MAIN` for the quarter totals and `SQL_ROWS` for the row-level derivation, both in the Code block. `strftime('%m')` returns text, so I `CAST` it; in SQLite a comparison such as `month < 4` returns 1 or 0, which I subtract from the year.
```sql
WITH f AS (
  SELECT amount,
         CAST(strftime('%Y', order_ts) AS INTEGER) - (CAST(strftime('%m', order_ts) AS INTEGER) < 4) AS fy_start,
         (CAST(strftime('%m', order_ts) AS INTEGER) + 8) % 12 / 3 + 1 AS fq
  FROM orders
)
SELECT 'FY' || fy_start || '-' || substr(fy_start + 1, 3, 2) AS fiscal_year,
       'Q' || fq AS fiscal_quarter,
       SUM(amount) AS revenue, COUNT(*) AS orders
FROM f GROUP BY fy_start, fq ORDER BY fy_start, fq
```

**pandas answer:** `dt.to_period('Q-MAR')` gives fiscal quarters that end in March. The `Period` is labelled by the fiscal year END (April 2024 is `2025Q1`), `qyear` is that end year and `quarter` is the fiscal quarter number:
```py
p = orders["order_ts"].dt.to_period("Q-MAR")
print(pd.DataFrame({"d": orders["order_ts"].dt.strftime("%Y-%m-%d"), "period": p.astype(str),
                    "qyear": p.dt.qyear, "quarter": p.dt.quarter}).to_string(index=False))
fy_end = p.dt.qyear
pd_df = (orders.assign(fiscal_year="FY" + (fy_end - 1).astype(str) + "-" + (fy_end % 100).astype(str).str.zfill(2),
                       fiscal_quarter="Q" + p.dt.quarter.astype(str))
         .groupby(["fiscal_year", "fiscal_quarter"], as_index=False)
         .agg(revenue=("amount", "sum"), orders=("order_id", "count")))
```

**Example:** 2024-03-31 23:59:59 is month 3, so fiscal start year 2023 (FY2023-24), fiscal month 12, fiscal quarter `(3 + 8) % 12 / 3 + 1 = 11 / 3 + 1 = 4`. One second later, 2024-04-01 is month 4: start year 2024, fiscal month 1, quarter `12 % 12 / 3 + 1 = 1`. FY2024-25 Q1 (April to June) holds orders 2 and 3 (200 + 300 = 500); Q2 holds order 4 (400); Q3 holds order 5 (500); Q4 holds orders 6 and 7 (600 + 700 = 1300). Order 1 (100) is the last day of FY2023-24 and order 8 (800) is the first day of FY2025-26.

**Code:** run with `python3 -I`.
```python
# Q25: Indian fiscal year (April to March), fiscal quarter, fiscal month
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-03-31 23:59:59',100),(2,'2024-04-01 00:00:00',200),(3,'2024-06-30 12:00:00',300),
 (4,'2024-07-01 09:00:00',400),(5,'2024-12-25 10:00:00',500),(6,'2025-01-15 10:00:00',600),
 (7,'2025-03-31 18:00:00',700),(8,'2025-04-01 08:00:00',800);
"""
SQL_ROWS = """
SELECT order_id, substr(order_ts, 1, 10) AS d,
       CAST(strftime('%Y', order_ts) AS INTEGER) - (CAST(strftime('%m', order_ts) AS INTEGER) < 4) AS fy_start,
       (CAST(strftime('%m', order_ts) AS INTEGER) + 8) % 12 + 1 AS fiscal_month,
       (CAST(strftime('%m', order_ts) AS INTEGER) + 8) % 12 / 3 + 1 AS fiscal_quarter
FROM orders ORDER BY order_id
"""
SQL_MAIN = """
WITH f AS (
  SELECT amount,
         CAST(strftime('%Y', order_ts) AS INTEGER) - (CAST(strftime('%m', order_ts) AS INTEGER) < 4) AS fy_start,
         (CAST(strftime('%m', order_ts) AS INTEGER) + 8) % 12 / 3 + 1 AS fq
  FROM orders
)
SELECT 'FY' || fy_start || '-' || substr(fy_start + 1, 3, 2) AS fiscal_year,
       'Q' || fq AS fiscal_quarter,
       SUM(amount) AS revenue, COUNT(*) AS orders
FROM f GROUP BY fy_start, fq ORDER BY fy_start, fq
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
rows = pd.read_sql_query(SQL_ROWS, con)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(rows.to_string(index=False))
print(sql_df.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
orders["order_ts"] = pd.to_datetime(orders["order_ts"])
p = orders["order_ts"].dt.to_period("Q-MAR")
print(pd.DataFrame({"d": orders["order_ts"].dt.strftime("%Y-%m-%d"), "period": p.astype(str),
                    "qyear": p.dt.qyear, "quarter": p.dt.quarter}).to_string(index=False))
fy_end = p.dt.qyear
pd_df = (orders.assign(fiscal_year="FY" + (fy_end - 1).astype(str) + "-" + (fy_end % 100).astype(str).str.zfill(2),
                       fiscal_quarter="Q" + p.dt.quarter.astype(str))
         .groupby(["fiscal_year", "fiscal_quarter"], as_index=False)
         .agg(revenue=("amount", "sum"), orders=("order_id", "count")))
# compared after sorting by fiscal_year, fiscal_quarter
pd_df = pd_df.sort_values(["fiscal_year", "fiscal_quarter"]).reset_index(drop=True)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
# row-level check of the arithmetic against pandas
fm = (orders["order_ts"].dt.month + 8) % 12 + 1
assert fm.tolist() == rows["fiscal_month"].tolist()
assert p.dt.quarter.tolist() == rows["fiscal_quarter"].tolist()
assert (fy_end - 1).tolist() == rows["fy_start"].tolist()
print("asserts passed: SQL fiscal arithmetic == pandas Q-MAR for 8 rows and for the quarter totals")
```

**Output (my run):**
```text
 order_id          d  fy_start  fiscal_month  fiscal_quarter
        1 2024-03-31      2023            12               4
        2 2024-04-01      2024             1               1
        3 2024-06-30      2024             3               1
        4 2024-07-01      2024             4               2
        5 2024-12-25      2024             9               3
        6 2025-01-15      2024            10               4
        7 2025-03-31      2024            12               4
        8 2025-04-01      2025             1               1
fiscal_year fiscal_quarter  revenue  orders
  FY2023-24             Q4      100       1
  FY2024-25             Q1      500       2
  FY2024-25             Q2      400       1
  FY2024-25             Q3      500       1
  FY2024-25             Q4     1300       2
  FY2025-26             Q1      800       1
         d period  qyear  quarter
2024-03-31 2024Q4   2024        4
2024-04-01 2025Q1   2025        1
2024-06-30 2025Q1   2025        1
2024-07-01 2025Q2   2025        2
2024-12-25 2025Q3   2025        3
2025-01-15 2025Q4   2025        4
2025-03-31 2025Q4   2025        4
2025-04-01 2026Q1   2026        1
asserts passed: SQL fiscal arithmetic == pandas Q-MAR for 8 rows and for the quarter totals
```

**Edge cases:**
- Boundary: the SQL and pandas results agree on the 31 March / 1 April pair (fiscal quarter 4 versus 1, different fiscal year). The assert covers all eight rows.
- Integer division: `(month + 8) % 12 / 3` is integer division in SQLite only because both operands are integers; `CAST(... AS INTEGER)` on the `strftime` text is what makes that true. In an engine with decimal division (some do), wrap it in `FLOOR` (not executed).
- Quarter labels differ by convention: pandas `Q-MAR` periods are named by the fiscal year they END in (`2025Q1` for April 2024), which many people read as calendar 2025. I label with `FY2024-25` instead.
- A partial fiscal year at the end of the data shows a total for only the loaded quarters; do not read it as a full year (Q32).
- Time zone: a UTC timestamp at 20:00 on 31 March is already 1 April in India (UTC+5:30), so the fiscal year of that order depends on the reporting zone; convert before classifying.

**Then explain:**
- The shift by 8 turns April into position 0: `(4 + 8) % 12 = 0`, `(3 + 8) % 12 = 11`. Divide by 3 for the quarter and add 1.
- Fiscal year for January to March belongs to the PREVIOUS calendar year's April start, hence `year - (month < 4)`.
- A calendar table (Q31) with `fiscal_year` and `fiscal_quarter` columns beats repeating this arithmetic in every query.
- Other engines (not executed): PostgreSQL `date_trunc('quarter', d)` and `EXTRACT(QUARTER FROM d)` are calendar quarters, so a fiscal shift needs an interval offset such as `d + INTERVAL '9 months'`; MySQL has `QUARTER(d)` (calendar); BigQuery and Snowflake have no built-in April fiscal option that I know of, and some tools expose a fiscal-year-start setting. I am quoting these from memory.

**Follow-ups:**
- "Fiscal week number?" Needs an agreed week definition (Part 6 Q5 and Q43).
- "Fiscal year-to-date comparisons?" That is Q32.
- "Fiscal year that starts in October (US federal) or July?" Change the 8 to 2 (October) or 6 (July) and the `< 4` test to match; same structure.

**Common mistakes:**
- Using calendar quarters (`(month + 2) / 3`) for a fiscal report.
- Labelling `FY2025` when the team means FY2024-25 without saying which end of the year names it.
- Off-by-one at the boundary (`month <= 4`, or `month > 3` wrongly applied to the year).
- Reading pandas `Q-MAR` period labels as calendar quarters.

### Q26 ⭐⭐ 🟡 Seasonality by day-of-week and hour: orders(order_id, order_ts, amount) in UTC. Return the average daily orders per day of week (Monday first), the hourly profile in IST, and weekend versus weekday share. Explain why you average over actual number of days (count distinct dates) rather than count rows (a month has more of some weekdays), the strftime('%w') Sunday = 0 ordering trick (CASE or (w + 6) % 7), and the pandas groupby on dt.dayofweek with day_name().
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Convert UTC to IST first (`+5 hours, +30 minutes`), then bucket by Monday-first day of week using `(strftime('%w') + 6) % 7 + 1`, and divide each weekday's orders by the number of calendar days of that weekday in the window (from a date spine), not by the number of distinct dates that happened to have orders.

**Schema and sample data:** 17 orders in UTC, window = IST dates 2024-03-04 (Monday) to 2024-03-18 (Monday) inclusive, so 15 days: three Mondays and two of every other weekday. Conventions: week starts Monday in the output (Mon = 1 ... Sun = 7); the reporting time zone is IST for day of week, hour and weekend share (UTC timestamps in, converted at the reporting edge). Order 8 (2024-03-09 18:45 UTC) is 00:15 on Sunday 10 March in IST and order 16 (2024-03-17 20:00 UTC) is 01:30 on Monday 18 March.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-03-04 03:30:00',10),(2,'2024-03-04 08:00:00',10),(3,'2024-03-05 04:30:00',10),
 (4,'2024-03-06 04:30:00',10),(5,'2024-03-06 12:00:00',10),(6,'2024-03-08 05:00:00',10),
 (7,'2024-03-09 06:30:00',10),(8,'2024-03-09 18:45:00',10),(9,'2024-03-10 09:00:00',10),
 (10,'2024-03-11 03:30:00',10),(11,'2024-03-12 04:30:00',10),(12,'2024-03-13 04:30:00',10),
 (13,'2024-03-14 04:30:00',10),(14,'2024-03-15 04:30:00',10),(15,'2024-03-16 06:30:00',10),
 (16,'2024-03-17 20:00:00',10),(17,'2024-03-18 03:30:00',10);
```

**SQL answer:** `SQL_DOW` (average per day of week), `SQL_HOUR` (hourly profile) and `SQL_SHARE` (weekend share) in the Code block. The IST conversion is the expression `datetime(order_ts, '+5 hours', '+30 minutes')`, repeated in each query; I do not use the `'localtime'` modifier because it uses the server's own zone.
```sql
WITH RECURSIVE days(d) AS (
  SELECT :lo UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < :hi
), n_days AS (
  SELECT (CAST(strftime('%w', d) AS INTEGER) + 6) % 7 + 1 AS dow, COUNT(*) AS days_in_window FROM days GROUP BY 1
), o AS (
  SELECT (CAST(strftime('%w', datetime(order_ts, '+5 hours', '+30 minutes')) AS INTEGER) + 6) % 7 + 1 AS dow, date(datetime(order_ts, '+5 hours', '+30 minutes')) AS d FROM orders
  WHERE date(datetime(order_ts, '+5 hours', '+30 minutes')) BETWEEN :lo AND :hi
)
SELECT n.dow,
       CASE n.dow WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed' WHEN 4 THEN 'Thu'
                  WHEN 5 THEN 'Fri' WHEN 6 THEN 'Sat' ELSE 'Sun' END AS day_name,
       COUNT(o.d) AS orders, n.days_in_window,
       ROUND(1.0 * COUNT(o.d) / n.days_in_window, 2) AS avg_per_day,
       ROUND(1.0 * COUNT(o.d) / NULLIF(COUNT(DISTINCT o.d), 0), 2) AS naive_avg_distinct_dates
FROM n_days n LEFT JOIN o ON o.dow = n.dow
GROUP BY n.dow, n.days_in_window ORDER BY n.dow
```

**pandas answer:** shift the naive UTC timestamps by `Timedelta(hours=5, minutes=30)` (equivalent to `tz_localize('UTC').tz_convert('Asia/Kolkata')` for India, which has no DST), count orders per `dt.dayofweek + 1`, and take names from `day_name()` of the spine dates:
```py
o["ist"] = pd.to_datetime(o["order_ts"]) + pd.Timedelta(hours=5, minutes=30)   # naive timestamps hold UTC; shift = IST wall clock
o = o[(o["ist"] >= "2024-03-04") & (o["ist"] < "2024-03-19")]
spine = pd.DataFrame({"d": pd.date_range("2024-03-04", "2024-03-18", freq="D")})
spine["dow"] = spine["d"].dt.dayofweek + 1
n_days = spine.groupby("dow").size().rename("days_in_window")
o["dow"] = o["ist"].dt.dayofweek + 1
g = o.groupby("dow").agg(orders=("order_id", "count"), distinct_dates=("ist", lambda s: s.dt.normalize().nunique()))
pd_dow = n_days.to_frame().join(g, how="left").fillna(0).astype(int).reset_index()
names = spine.groupby("dow")["d"].first().dt.day_name().str[:3]   # day_name() from the spine dates
pd_dow["day_name"] = pd_dow["dow"].map(names)
```

**Example:** in IST, Monday 4 March has orders 1 and 2, Monday 11 March has order 10, Monday 18 March has orders 16 (shifted from Sunday UTC) and 17: five Monday orders over three Mondays = 1.67 per Monday. Sunday: order 8 (00:15 on 10 March) and order 9 (14:30 on 10 March) are both on the 10th; Sunday 17 March has no orders. Two Sundays in the window, 2 orders: 1.00 per Sunday, but dividing by distinct order dates (one Sunday) would give 2.00. Thursday: only 14 March has an order (7 March has none): 1 order over 2 Thursdays = 0.50, versus 1.00 by distinct dates. Weekend (Saturday or Sunday in IST): 4 of 17 orders, 23.5%.

**Code:** run with `python3 -I`.
```python
# Q26: seasonality by IST day of week and hour; window 2024-03-04 (Mon) .. 2024-03-18 (Mon) IST dates
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-03-04 03:30:00',10),(2,'2024-03-04 08:00:00',10),(3,'2024-03-05 04:30:00',10),
 (4,'2024-03-06 04:30:00',10),(5,'2024-03-06 12:00:00',10),(6,'2024-03-08 05:00:00',10),
 (7,'2024-03-09 06:30:00',10),(8,'2024-03-09 18:45:00',10),(9,'2024-03-10 09:00:00',10),
 (10,'2024-03-11 03:30:00',10),(11,'2024-03-12 04:30:00',10),(12,'2024-03-13 04:30:00',10),
 (13,'2024-03-14 04:30:00',10),(14,'2024-03-15 04:30:00',10),(15,'2024-03-16 06:30:00',10),
 (16,'2024-03-17 20:00:00',10),(17,'2024-03-18 03:30:00',10);
"""
# Monday-first day number: ((%w + 6) % 7) + 1 -> Mon=1 .. Sun=7
SQL_DOW = """
WITH RECURSIVE days(d) AS (
  SELECT :lo UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < :hi
), n_days AS (
  SELECT (CAST(strftime('%w', d) AS INTEGER) + 6) % 7 + 1 AS dow, COUNT(*) AS days_in_window FROM days GROUP BY 1
), o AS (
  SELECT (CAST(strftime('%w', datetime(order_ts, '+5 hours', '+30 minutes')) AS INTEGER) + 6) % 7 + 1 AS dow, date(datetime(order_ts, '+5 hours', '+30 minutes')) AS d FROM orders
  WHERE date(datetime(order_ts, '+5 hours', '+30 minutes')) BETWEEN :lo AND :hi
)
SELECT n.dow,
       CASE n.dow WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed' WHEN 4 THEN 'Thu'
                  WHEN 5 THEN 'Fri' WHEN 6 THEN 'Sat' ELSE 'Sun' END AS day_name,
       COUNT(o.d) AS orders, n.days_in_window,
       ROUND(1.0 * COUNT(o.d) / n.days_in_window, 2) AS avg_per_day,
       ROUND(1.0 * COUNT(o.d) / NULLIF(COUNT(DISTINCT o.d), 0), 2) AS naive_avg_distinct_dates
FROM n_days n LEFT JOIN o ON o.dow = n.dow
GROUP BY n.dow, n.days_in_window ORDER BY n.dow
"""
SQL_HOUR = """
SELECT CAST(strftime('%H', datetime(order_ts, '+5 hours', '+30 minutes')) AS INTEGER) AS ist_hour, COUNT(*) AS orders,
       ROUND(1.0 * COUNT(*) / 15, 2) AS avg_per_day
FROM orders WHERE date(datetime(order_ts, '+5 hours', '+30 minutes')) BETWEEN :lo AND :hi
GROUP BY 1 ORDER BY 1
"""
SQL_SHARE = """
SELECT SUM(CASE WHEN strftime('%w', datetime(order_ts, '+5 hours', '+30 minutes')) IN ('0','6') THEN 1 ELSE 0 END) AS weekend_orders,
       COUNT(*) AS orders,
       ROUND(100.0 * SUM(CASE WHEN strftime('%w', datetime(order_ts, '+5 hours', '+30 minutes')) IN ('0','6') THEN 1 ELSE 0 END) / COUNT(*), 1) AS weekend_pct
FROM orders WHERE date(datetime(order_ts, '+5 hours', '+30 minutes')) BETWEEN :lo AND :hi
"""
SQL_UTC_DOW = """
SELECT (CAST(strftime('%w', order_ts) AS INTEGER) + 6) % 7 + 1 AS dow_utc, COUNT(*) AS orders
FROM orders GROUP BY 1 ORDER BY 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"lo": "2024-03-04", "hi": "2024-03-18"}
dow = pd.read_sql_query(SQL_DOW, con, params=P)
hour = pd.read_sql_query(SQL_HOUR, con, params=P)
share = pd.read_sql_query(SQL_SHARE, con, params=P)
print(dow.to_string(index=False)); print(hour.to_string(index=False)); print(share.to_string(index=False))
print("UTC day-of-week counts (same orders, different boundary):")
print(pd.read_sql_query(SQL_UTC_DOW, con).to_string(index=False))

o = pd.read_sql_query("SELECT * FROM orders", con)
o["ist"] = pd.to_datetime(o["order_ts"]) + pd.Timedelta(hours=5, minutes=30)   # naive timestamps hold UTC; shift = IST wall clock
o = o[(o["ist"] >= "2024-03-04") & (o["ist"] < "2024-03-19")]
spine = pd.DataFrame({"d": pd.date_range("2024-03-04", "2024-03-18", freq="D")})
spine["dow"] = spine["d"].dt.dayofweek + 1
n_days = spine.groupby("dow").size().rename("days_in_window")
o["dow"] = o["ist"].dt.dayofweek + 1
g = o.groupby("dow").agg(orders=("order_id", "count"), distinct_dates=("ist", lambda s: s.dt.normalize().nunique()))
pd_dow = n_days.to_frame().join(g, how="left").fillna(0).astype(int).reset_index()
names = spine.groupby("dow")["d"].first().dt.day_name().str[:3]   # day_name() from the spine dates
pd_dow["day_name"] = pd_dow["dow"].map(names)
pd_dow["avg_per_day"] = (pd_dow["orders"] / pd_dow["days_in_window"]).round(2)
pd_dow["naive_avg_distinct_dates"] = (pd_dow["orders"] / pd_dow["distinct_dates"]).round(2)
pd_dow = pd_dow[["dow", "day_name", "orders", "days_in_window", "avg_per_day", "naive_avg_distinct_dates"]]
# compared in Monday-first order (dow 1..7)
pd.testing.assert_frame_equal(pd_dow, dow, check_dtype=False)
pd_hour = o.groupby(o["ist"].dt.hour).size().rename("orders").rename_axis("ist_hour").reset_index()
pd_hour["avg_per_day"] = (pd_hour["orders"] / 15).round(2)
pd.testing.assert_frame_equal(pd_hour, hour, check_dtype=False)
wk = int((o["ist"].dt.dayofweek >= 5).sum())
assert (wk, len(o), round(100.0 * wk / len(o), 1)) == tuple(share.iloc[0])
print("pandas day_name:", pd_dow["day_name"].tolist())
print("asserts passed: SQL == pandas for day-of-week, hourly profile and weekend share")
```

**Output (my run):**
```text
 dow day_name  orders  days_in_window  avg_per_day  naive_avg_distinct_dates
   1      Mon       5               3         1.67                      1.67
   2      Tue       2               2         1.00                      1.00
   3      Wed       3               2         1.50                      1.50
   4      Thu       1               2         0.50                      1.00
   5      Fri       2               2         1.00                      1.00
   6      Sat       2               2         1.00                      1.00
   7      Sun       2               2         1.00                      2.00
 ist_hour  orders  avg_per_day
        0       1         0.07
        1       1         0.07
        9       3         0.20
       10       7         0.47
       12       2         0.13
       13       1         0.07
       14       1         0.07
       17       1         0.07
 weekend_orders  orders  weekend_pct
              4      17         23.5
UTC day-of-week counts (same orders, different boundary):
 dow_utc  orders
       1       4
       2       2
       3       3
       4       1
       5       2
       6       3
       7       2
pandas day_name: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
asserts passed: SQL == pandas for day-of-week, hourly profile and weekend share
```

**Edge cases:**
- Days with zero orders (Thursday 7 March, Sunday 17 March): they must be in the denominator, which is why `n_days` comes from a recursive date spine. Dividing by `COUNT(DISTINCT date)` overstates Thursday (1.00 instead of 0.50) and Sunday (2.00 instead of 1.00); those two columns are printed side by side.
- Window length: 15 days gives Monday three occurrences. A 14-day window would give every weekday two; the unequal count is exactly why you divide by days, not rows.
- Time zone moves orders between days: with UTC day-of-week the Monday count is 4 instead of 5 and Saturday is 3 instead of 2 in my data (the extra UTC-table printed in the output), because two orders cross midnight when converted. State the zone before comparing numbers.
- Hour 0 and hour 1 in the hourly profile come from the two orders that cross midnight in IST.
- `%w` is Sunday = 0: without the `(w + 6) % 7` shift, Sunday sorts first.
- Weekday versus weekend share is share of orders (23.5%), not share of days; a weekend has 2 of 7 days (about 28.6% of days), so compare to that.
- The hourly profile divides by 15 days in my window; for a window with a different length, parametrise it.

**Then explain:**
- Average per weekday = total orders on that weekday / number of that weekday in the window. It is a rate per day, so it is comparable across weekdays even when the counts of weekdays differ.
- Convert once at the reporting edge: all three outputs here use the same IST expression.
- pandas `dt.dayofweek` is Monday = 0 (I add 1 to match the SQL numbering); `day_name()` gives names but sorts alphabetically if you group on it, so group on the number and map to names.
- Hedged (not executed): PostgreSQL `EXTRACT(ISODOW FROM d)` is Monday = 1 and `EXTRACT(DOW FROM d)` is Sunday = 0; MySQL `WEEKDAY(d)` is Monday = 0 and `DAYOFWEEK(d)` is Sunday = 1; named zones use `AT TIME ZONE` in PostgreSQL and `CONVERT_TZ` in MySQL. From memory.

**Follow-ups:**
- "Heatmap of day of week by hour?" Group by both numbers; keep empty cells with a 7 x 24 spine.
- "Seasonality across months or festivals?" Needs several years and an indicator for movable dates; weekday averaging is only the first step.
- "Is the weekend difference significant?" That is a statistics question (Book 1); here I only describe the data.

**Common mistakes:**
- Dividing by rows or distinct order dates instead of calendar days.
- Grouping by UTC weekday and reporting it as local.
- Sunday = 0 ordering left in the output.
- Using `'localtime'` and getting the server's zone.
- Reading a weekday average from a short window as seasonality.

### Q27 ⭐⭐ 🟡 Business days and holidays: tasks(task_id, start_date, end_date) and holidays(holiday_date). Count working days (Monday to Friday, excluding holidays) between start and end inclusive using a recursive CTE calendar and LEFT JOIN or NOT EXISTS on holidays, and show the closed-form day arithmetic and why it fails with holidays. pandas: np.busday_count with holidays=, pd.bdate_range(freq='C', holidays=...), and CustomBusinessDay. State whether the end date is inclusive; that choice changes every answer by one.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** I count Monday-to-Friday days from a recursive date calendar, `LEFT JOIN`ed to each task over `BETWEEN start_date AND end_date` (end inclusive), excluding holidays with `NOT EXISTS`; the closed-form arithmetic (full weeks times 5 plus the leftover days) is faster but breaks as soon as a holiday falls on a weekend or repeats, so it is only a check for the no-holiday case.

**Schema and sample data:** five tasks (a normal week, a range containing a Monday holiday, a range containing a Saturday holiday, a Saturday-only task, and an end before the start) and two holidays, one Monday (2024-03-25) and one Saturday (2024-03-30). Convention: start and end dates are both inclusive; weekend = Saturday and Sunday; dates are plain dates with no time zone.
```sql
CREATE TABLE tasks(task_id INTEGER PRIMARY KEY, start_date TEXT, end_date TEXT);
CREATE TABLE holidays(holiday_date TEXT PRIMARY KEY);
INSERT INTO tasks VALUES (1,'2024-03-18','2024-03-22'),(2,'2024-03-22','2024-03-26'),
  (3,'2024-03-29','2024-04-02'),(4,'2024-03-23','2024-03-23'),(5,'2024-03-27','2024-03-26');
INSERT INTO holidays VALUES ('2024-03-25'),('2024-03-30');
```

**SQL answer:** `SQL_MAIN` (calendar CTE, `LEFT JOIN`, `NOT EXISTS`) and `SQL_CLOSED` (closed-form) in the Code block.
```sql
WITH RECURSIVE cal(d) AS (
  SELECT (SELECT MIN(start_date) FROM tasks)
  UNION ALL SELECT date(d, '+1 day') FROM cal WHERE d < (SELECT MAX(end_date) FROM tasks)
)
SELECT t.task_id, t.start_date, t.end_date, COUNT(c.d) AS working_days
FROM tasks t
LEFT JOIN cal c
  ON c.d BETWEEN t.start_date AND t.end_date
 AND strftime('%w', c.d) NOT IN ('0', '6')
 AND NOT EXISTS (SELECT 1 FROM holidays h WHERE h.holiday_date = c.d)
GROUP BY t.task_id, t.start_date, t.end_date
ORDER BY t.task_id
```
```sql
WITH x AS (
  SELECT task_id,
         CAST(julianday(end_date) - julianday(start_date) AS INTEGER) + 1 AS n,
         (CAST(strftime('%w', start_date) AS INTEGER) + 6) % 7 AS w,
         start_date, end_date
  FROM tasks WHERE end_date >= start_date
), y AS (
  SELECT task_id, n / 7 * 5
         + MAX(0, MIN(w + n % 7, 5) - w) + MAX(0, MIN(w + n % 7 - 7, 5)) AS weekdays,
         start_date, end_date
  FROM x
)
SELECT task_id, weekdays AS closed_form_no_holidays,
       weekdays - (SELECT COUNT(*) FROM holidays h WHERE h.holiday_date BETWEEN start_date AND end_date) AS naive_minus_holidays
FROM y ORDER BY task_id
```

**pandas answer:** `np.busday_count` counts up to but excluding the end date, so pass `end + 1 day` for an inclusive end; `bdate_range(..., freq='C', holidays=...)` and `date_range(freq=CustomBusinessDay(holidays=...))` include both ends:
```py
bc = np.clip(np.busday_count(s, e + np.timedelta64(1, "D"), holidays=hol), 0, None)
cbd = pd.offsets.CustomBusinessDay(holidays=hol)
bd = [len(pd.bdate_range(a, b, freq="C", holidays=hol)) for a, b in zip(tasks["start_date"], tasks["end_date"])]
cb = [len(pd.date_range(a, b, freq=cbd)) for a, b in zip(tasks["start_date"], tasks["end_date"])]
```

**Example:** task 1, Monday 18 to Friday 22 March: 5 weekdays, no holidays, 5. Task 2, Friday 22 to Tuesday 26: weekdays are Fri 22, Mon 25, Tue 26 = 3, and Monday 25 is a holiday, so 2. Task 3, Friday 29 March to Tuesday 2 April: weekdays Fri 29, Mon 1, Tue 2 = 3; the holiday is Saturday 30 March, which is not a working day anyway, so the answer stays 3. The naive "weekdays minus holidays in the range" gives 2, which is wrong. Task 4 (a Saturday) is 0 and task 5 (end before start) is 0 because the join finds no days.

**Code:** run with `python3 -I`.
```python
# Q27: working days (Mon-Fri, minus holidays), start and end both INCLUSIVE
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE tasks(task_id INTEGER PRIMARY KEY, start_date TEXT, end_date TEXT);
CREATE TABLE holidays(holiday_date TEXT PRIMARY KEY);
INSERT INTO tasks VALUES (1,'2024-03-18','2024-03-22'),(2,'2024-03-22','2024-03-26'),
  (3,'2024-03-29','2024-04-02'),(4,'2024-03-23','2024-03-23'),(5,'2024-03-27','2024-03-26');
INSERT INTO holidays VALUES ('2024-03-25'),('2024-03-30');
"""
SQL_MAIN = """
WITH RECURSIVE cal(d) AS (
  SELECT (SELECT MIN(start_date) FROM tasks)
  UNION ALL SELECT date(d, '+1 day') FROM cal WHERE d < (SELECT MAX(end_date) FROM tasks)
)
SELECT t.task_id, t.start_date, t.end_date, COUNT(c.d) AS working_days
FROM tasks t
LEFT JOIN cal c
  ON c.d BETWEEN t.start_date AND t.end_date
 AND strftime('%w', c.d) NOT IN ('0', '6')
 AND NOT EXISTS (SELECT 1 FROM holidays h WHERE h.holiday_date = c.d)
GROUP BY t.task_id, t.start_date, t.end_date
ORDER BY t.task_id
"""
# closed form: full weeks * 5 + weekdays among the leftover days; w = Monday-based index of the start day
SQL_CLOSED = """
WITH x AS (
  SELECT task_id,
         CAST(julianday(end_date) - julianday(start_date) AS INTEGER) + 1 AS n,
         (CAST(strftime('%w', start_date) AS INTEGER) + 6) % 7 AS w,
         start_date, end_date
  FROM tasks WHERE end_date >= start_date
), y AS (
  SELECT task_id, n / 7 * 5
         + MAX(0, MIN(w + n % 7, 5) - w) + MAX(0, MIN(w + n % 7 - 7, 5)) AS weekdays,
         start_date, end_date
  FROM x
)
SELECT task_id, weekdays AS closed_form_no_holidays,
       weekdays - (SELECT COUNT(*) FROM holidays h WHERE h.holiday_date BETWEEN start_date AND end_date) AS naive_minus_holidays
FROM y ORDER BY task_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
closed = pd.read_sql_query(SQL_CLOSED, con)
print(sql_df.to_string(index=False))
print(closed.to_string(index=False))

tasks = pd.read_sql_query("SELECT * FROM tasks", con)
hol = pd.read_sql_query("SELECT * FROM holidays", con)["holiday_date"].tolist()
s = tasks["start_date"].to_numpy("datetime64[D]")
e = tasks["end_date"].to_numpy("datetime64[D]")
# busday_count excludes the end date, so add one day for an inclusive end; end < start gives a negative count, clip at 0
bc = np.clip(np.busday_count(s, e + np.timedelta64(1, "D"), holidays=hol), 0, None)
cbd = pd.offsets.CustomBusinessDay(holidays=hol)
bd = [len(pd.bdate_range(a, b, freq="C", holidays=hol)) for a, b in zip(tasks["start_date"], tasks["end_date"])]
cb = [len(pd.date_range(a, b, freq=cbd)) for a, b in zip(tasks["start_date"], tasks["end_date"])]
print("np.busday_count (end+1):", bc.tolist())
print("bdate_range freq='C':", bd)
print("date_range CustomBusinessDay:", cb)
# compared in task_id order
assert bc.tolist() == sql_df["working_days"].tolist() == bd == cb
print("exclusive end (busday_count without +1 day):", np.busday_count(s, e, holidays=hol).tolist())
# closed form (no holidays) checked against busday_count on 840 start/end pairs from 2024-03-01
con.execute("DELETE FROM tasks")
base = np.datetime64("2024-03-01", "D")
pairs = [(str(base + np.timedelta64(i, "D")), str(base + np.timedelta64(i + j, "D"))) for i in range(14) for j in range(60)]
con.executemany("INSERT INTO tasks(start_date, end_date) VALUES (?, ?)", pairs)
cf = dict(con.execute("SELECT task_id, closed_form_no_holidays FROM (" + SQL_CLOSED + ")").fetchall())
rows = con.execute("SELECT task_id, start_date, end_date FROM tasks").fetchall()
for tid, a, b in rows:
    assert cf[tid] == int(np.busday_count(np.datetime64(a, "D"), np.datetime64(b, "D") + np.timedelta64(1, "D"))), (a, b)
print("closed form (no holidays) matches busday_count on", len(rows), "start/end pairs")
print("asserts passed: SQL == busday_count == bdate_range('C') == CustomBusinessDay")
```

**Output (my run):**
```text
 task_id start_date   end_date  working_days
       1 2024-03-18 2024-03-22             5
       2 2024-03-22 2024-03-26             2
       3 2024-03-29 2024-04-02             3
       4 2024-03-23 2024-03-23             0
       5 2024-03-27 2024-03-26             0
 task_id  closed_form_no_holidays  naive_minus_holidays
       1                        5                     5
       2                        3                     2
       3                        3                     2
       4                        0                     0
np.busday_count (end+1): [5, 2, 3, 0, 0]
bdate_range freq='C': [5, 2, 3, 0, 0]
date_range CustomBusinessDay: [5, 2, 3, 0, 0]
exclusive end (busday_count without +1 day): [4, 1, 2, 0, -1]
closed form (no holidays) matches busday_count on 840 start/end pairs
asserts passed: SQL == busday_count == bdate_range('C') == CustomBusinessDay
```

**Edge cases:**
- Inclusive versus exclusive end: this changes every answer by one. With `busday_count(start, end)` and no `+ 1 day` the printed list is `[4, 1, 2, 0, -1]` instead of `[5, 2, 3, 0, 0]`. State the rule before coding.
- Holiday on a weekend (2024-03-30): the calendar join ignores it correctly; the closed-form minus holidays does not (task 3 gives 2). A holiday listed twice would also double-subtract in the closed form, which is why `holidays.holiday_date` is a primary key here.
- End before start (task 5): the `BETWEEN` join returns no calendar days, so `LEFT JOIN` keeps the task with count 0. `busday_count` can return a negative number for a reversed range (the exclusive form shows -1); I clip at 0 in the check.
- Tasks outside the calendar: the calendar runs from the earliest start to the latest end in `tasks`; with a fixed calendar table (Q31) make sure it covers the task dates.
- Different working week (Friday and Saturday weekend in some countries) needs a different weekend set; `weekmask` in numpy/pandas and a change to the `%w` test in SQL.
- Half-days, regional holidays, and time-of-day tasks are out of scope; state it.

**Then explain:**
- Calendar approach: generate one row per day, filter by weekday, filter by holiday, count per task. It is O(tasks x days) in the worst case but is easy to audit and to extend with a half-day rule.
- Closed form: `n / 7 * 5` plus the weekdays inside the `n % 7` leftover days, starting from the start day's weekday index. I checked it against `busday_count` on 840 start/end pairs (no holidays); it matches. Holidays are a set, not a count, so subtract only holidays that are weekdays and unique.
- pandas: `CustomBusinessDay(holidays=...)` is the object you reuse for offsets (`+ 5 * cbd`) as well as ranges; `freq='C'` is its alias in `bdate_range`.
- Hedged (not executed): PostgreSQL can use `generate_series(start, end, interval '1 day')` for the calendar and `EXTRACT(ISODOW FROM d) < 6`; MySQL 8 uses a recursive CTE as here; there is no portable built-in working-day function.

**Follow-ups:**
- "Add N working days to a start date?" Use the calendar with a row number over working days, or `start + N * CustomBusinessDay` in pandas.
- "Business days between timestamps?" Decide how partial days count first.
- "Holidays that differ by region?" Add `region` to `holidays` and to the join.

**Common mistakes:**
- Forgetting that `busday_count` excludes the end date.
- Subtracting the number of holidays instead of the number of weekday holidays.
- Counting `strftime('%w') BETWEEN 1 AND 5` with Sunday = 0 confusion (use `NOT IN ('0', '6')`).
- An inner join that silently drops tasks with zero working days.
- Mixing `DATE` strings with different formats so `BETWEEN` compares text wrongly.

### Q28 ⭐⭐ 🟡 pandas resample details versus SQL grouping: daily_sales(sale_date, amount) with gaps. Show resample('MS') (month start labels, left closed), resample('ME') (month end labels, closed and label right by default) and resample('W') (W-SUN, right closed and labelled), why resample('MS') creates empty months (sum 0, mean NaN) where SQL GROUP BY omits them, and the 'M' alias being gone in pandas 3 (use 'ME'). Reproduce a SQLite monthly sum and assert both frames match after reindexing the SQL result to the pandas spine.
**Asked at:** pandas time series user guide and DataFrame.resample reference (opened), official documentation and not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `resample('MS')` labels each month by its first day, closed left, and creates empty months (sum 0, mean NaN), while SQL `GROUP BY` omits months with no rows; `resample('ME')` labels by month end and is the pandas 3 spelling (`'M'` raises), and `resample('W')` is `W-SUN`, right closed and right labelled, so a week is named by the Sunday that ends it.

**Schema and sample data:** six sales days with gaps (nothing in February). Conventions: weeks end on Sunday for `W` (Monday start needs `closed='left', label='left'` on `W-MON`); no time zone, timestamps are naive.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-05',10),('2024-01-20',20),('2024-01-31',30),
  ('2024-03-03',40),('2024-03-15',50),('2024-04-01',60);
```

**SQL answer:** `SQL_MAIN` groups by month start and omits February. To compare with pandas I reindex the SQL result to the pandas month spine afterwards (in pandas), not inside SQL.
```sql
SELECT date(sale_date, 'start of month') AS month, SUM(amount) AS revenue, COUNT(*) AS n_days
FROM daily_sales GROUP BY 1 ORDER BY 1
```

**pandas answer:** the three resamples, then the reindex-and-compare step (full code below):
```py
ms = s.resample("MS").agg(["sum", "mean", "count"])
print("resample('MS') sum/mean/count:"); print(ms.to_string())
me = s.resample("ME").sum()
```
```py
spine = pd.date_range("2024-01-01", "2024-04-01", freq="MS")
sql_s = sql_df.assign(month=pd.to_datetime(sql_df["month"])).set_index("month")["revenue"].reindex(spine, fill_value=0)
pd_s = s.resample("MS").sum()
```

**Example:** daily sales: 5 Jan 10, 20 Jan 20, 31 Jan 30, 3 Mar 40, 15 Mar 50, 1 Apr 60. Months: January 60, February nothing, March 90, April 60. SQL returns three rows. `resample('MS')` returns four: 2024-02-01 has sum 0, mean NaN, count 0. `resample('ME')` returns the same four values labelled 01-31, 02-29, 03-31, 04-30. `resample('W')`: 31 Jan is a Wednesday, so its week runs Monday 29 Jan to Sunday 4 Feb and is labelled 2024-02-04, a February date for a January sale; 3 March is a Sunday and is labelled 2024-03-03 itself because the right edge is closed.

**Code:** run with `python3 -I`.
```python
# Q28: pandas resample (MS, ME, W) versus SQL GROUP BY; daily sales with gaps
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-05',10),('2024-01-20',20),('2024-01-31',30),
  ('2024-03-03',40),('2024-03-15',50),('2024-04-01',60);
"""
SQL_MAIN = """
SELECT date(sale_date, 'start of month') AS month, SUM(amount) AS revenue, COUNT(*) AS n_days
FROM daily_sales GROUP BY 1 ORDER BY 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL (February is absent):"); print(sql_df.to_string(index=False))

ds = pd.read_sql_query("SELECT * FROM daily_sales", con)
s = ds.assign(sale_date=pd.to_datetime(ds["sale_date"])).set_index("sale_date")["amount"]

ms = s.resample("MS").agg(["sum", "mean", "count"])
print("resample('MS') sum/mean/count:"); print(ms.to_string())
me = s.resample("ME").sum()
print("resample('ME') sum:"); print(me.to_string())
w = s.resample("W").sum()
print("resample('W') (W-SUN, right closed, right label) sum, non-empty weeks:")
print(w[w > 0].to_string())
print("W-SUN week 2024-01-29..2024-02-04 label:", w.index[w.index == "2024-02-04"].tolist())
wm = s.resample("W-MON").sum()
print("resample('W-MON') defaults (right closed, right label), non-empty:", {str(k.date()): int(v) for k, v in wm[wm > 0].items()})
wm2 = s.resample("W-MON", closed="left", label="left").sum()
print("resample('W-MON', closed='left', label='left') non-empty:", {str(k.date()): int(v) for k, v in wm2[wm2 > 0].items()})
try:
    s.resample("M")
except Exception as ex:
    print("resample('M') ->", type(ex).__name__ + ":", ex)
print("defaults on this install: MS closed/label =", s.resample("MS").sum().index[0].date(), "(left); ME first label =", me.index[0].date(), "(right)")
# timestamps: does a 15:00 sale on the last day of the month stay in that month under 'ME'?
ts = pd.Series([1, 2], index=pd.to_datetime(["2024-01-31 15:00", "2024-02-01 00:00"]))
print("ME with a 15:00 timestamp on 31 Jan:", ts.resample("ME").sum().to_dict())
print("MS with a 15:00 timestamp on 31 Jan:", ts.resample("MS").sum().to_dict())

# SQL result reindexed to the pandas spine
spine = pd.date_range("2024-01-01", "2024-04-01", freq="MS")
sql_s = sql_df.assign(month=pd.to_datetime(sql_df["month"])).set_index("month")["revenue"].reindex(spine, fill_value=0)
pd_s = s.resample("MS").sum()
# compared on the monthly spine, index = month start
pd.testing.assert_series_equal(sql_s, pd_s, check_names=False, check_freq=False, check_dtype=False)
# ME and MS agree on values, only labels differ
assert me.to_numpy().tolist() == pd_s.to_numpy().tolist()
print("SQL reindexed to spine:", sql_s.to_dict())
print("asserts passed: SQL (reindexed to the MS spine) == resample('MS').sum() == resample('ME').sum() values")
```

**Output (my run):**
```text
SQL (February is absent):
     month  revenue  n_days
2024-01-01       60       3
2024-03-01       90       2
2024-04-01       60       1
resample('MS') sum/mean/count:
            sum  mean  count
sale_date                   
2024-01-01   60  20.0      3
2024-02-01    0   NaN      0
2024-03-01   90  45.0      2
2024-04-01   60  60.0      1
resample('ME') sum:
sale_date
2024-01-31    60
2024-02-29     0
2024-03-31    90
2024-04-30    60
Freq: ME
resample('W') (W-SUN, right closed, right label) sum, non-empty weeks:
sale_date
2024-01-07    10
2024-01-21    20
2024-02-04    30
2024-03-03    40
2024-03-17    50
2024-04-07    60
W-SUN week 2024-01-29..2024-02-04 label: [Timestamp('2024-02-04 00:00:00')]
resample('W-MON') defaults (right closed, right label), non-empty: {'2024-01-08': 10, '2024-01-22': 20, '2024-02-05': 30, '2024-03-04': 40, '2024-03-18': 50, '2024-04-01': 60}
resample('W-MON', closed='left', label='left') non-empty: {'2024-01-01': 10, '2024-01-15': 20, '2024-01-29': 30, '2024-02-26': 40, '2024-03-11': 50, '2024-04-01': 60}
resample('M') -> ValueError: Invalid frequency: M. Failed to parse with error message: ValueError("'M' is no longer supported for offsets. Please use 'ME' instead.")
defaults on this install: MS closed/label = 2024-01-01 (left); ME first label = 2024-01-31 (right)
ME with a 15:00 timestamp on 31 Jan: {Timestamp('2024-01-31 00:00:00'): 1, Timestamp('2024-02-29 00:00:00'): 2}
MS with a 15:00 timestamp on 31 Jan: {Timestamp('2024-01-01 00:00:00'): 1, Timestamp('2024-02-01 00:00:00'): 2}
SQL reindexed to spine: {Timestamp('2024-01-01 00:00:00'): 60, Timestamp('2024-02-01 00:00:00'): 0, Timestamp('2024-03-01 00:00:00'): 90, Timestamp('2024-04-01 00:00:00'): 60}
asserts passed: SQL (reindexed to the MS spine) == resample('MS').sum() == resample('ME').sum() values
```

**Edge cases:**
- Empty month: sum 0 (a convenience, but it can hide "no data loaded" as "zero sales"), mean NaN, count 0. In SQL the row is simply absent. Choose zero or NULL deliberately (Q6, Q7).
- `W` labels: the label is the week end, so month-level reporting from weekly buckets mislabels boundary weeks (the 31 Jan sale in a week labelled 4 Feb).
- `W-MON` defaults: I ran both; with defaults, `W-MON` is also right closed and right labelled (the 1 April sale falls in the bucket labelled 2024-04-01, a week that ends on that Monday and starts on Tuesday 26 March). To get Monday-to-Sunday weeks labelled by their Monday I had to pass `closed='left', label='left'` (printed above: 2024-04-01 bucket holds 1 April). This matches the docs' note that W is right-closed; I confirmed it by running.
- Timestamps at 15:00 on the last day of a month: under `ME` I tested a 31 Jan 15:00 value and it stayed in January (label 2024-01-31); under `MS` it also stayed in January (label 2024-01-01), so month resampling is by calendar day boundaries and the time of day does not push it into the next bin.
- `'M'`: pandas 3.0.5 raised `ValueError: Invalid frequency: M. Failed to parse with error message: ValueError("'M' is no longer supported for offsets. Please use 'ME' instead.")`. Period frequencies still use `'M'` (as in `to_period('M')`).

**Then explain:**
- `GROUP BY` can only return groups that exist in the data; `resample` builds the full range from the first to the last timestamp, so gaps in the middle become rows. The range runs from the first to the last timestamp present in the data.
- Default closure/label: left/left for `MS`, right/right for `ME`, `W` and `QE`/`YE` (the end-anchored ones), as in the pandas `resample` reference (opened for the sources note); I ran `MS`, `ME`, `W` and `W-MON` to confirm.
- To reproduce a SQL monthly sum in pandas, either `groupby(dt.to_period('M'))` (no empty months, like SQL) or `resample` plus `reindex` on the SQL side; the assert in the code compares on the `MS` spine with `fill_value=0`.
- Hedged (not executed): in other engines the equivalent spine is `generate_series` (PostgreSQL), `GENERATE_DATE_ARRAY` (BigQuery) or a calendar table; I have not run them.

**Follow-ups:**
- "Why did my weekly total not match the monthly total?" Weeks straddle month ends; sum daily data to months directly.
- "Sum versus mean on a resampled gap?" Mean of daily data over empty days is NaN, but a monthly average per calendar day needs the day count (spine), not the mean of existing days.
- "How do I resample timestamps with a time zone?" Convert to the reporting zone first (Q30, Q38).

**Common mistakes:**
- Using `'M'` in pandas 3 and getting a `ValueError` (use `'ME'`).
- Assuming `W` weeks start on Monday and are labelled by their first day.
- Treating an empty resampled month as zero when it really means data was not loaded.
- Comparing `MS`-labelled and `ME`-labelled frames by index.

### Q29 ⭐⭐ 🟡 SQL versus pandas date gotchas (translation table, each row demonstrated): week start defaults (SQLite %w Sunday = 0 versus pandas Monday = 0), integer versus float day differences (julianday versus Timedelta.days), NULL versus NaT in comparisons and groupby (pandas groupby drops NaT keys by default, SQL groups NULL together), string dates compared as text versus datetime64, ISO week year boundary (isocalendar().year versus calendar year), and Period('2024-01') versus Timestamp('2024-01-01') equality and merging. Run each side by side on a six-row frame.
**Asked at:** pandas time series user guide and DataFrame.resample reference (opened), official documentation and not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Same dates, different defaults: `%w` is Sunday = 0 but pandas `dayofweek` is Monday = 0; `julianday` differences are floats but `Timedelta.days` truncates; SQL comparisons with NULL are unknown but a pandas comparison with NaT is False (so its negation is True); SQL groups NULLs together but pandas drops NaT keys; text dates compare as text; the ISO year is not the calendar year near 1 January; and `Period('2024-01')` is not equal to `Timestamp('2024-01-01')`.

**Schema and sample data:** a six-row frame `t` with a clean ISO date `d`, a loosely formatted text date `d_loose` (row 6 is `'2024-1-02'`, not zero-padded) and a timestamp pair `a`, `b`. Row 5 is all NULL. Conventions: week start Sunday = 0 in SQLite `%w`, Monday = 0 in pandas; ISO weeks start Monday; no time zone (all naive).
```sql
CREATE TABLE t(id INTEGER PRIMARY KEY, d TEXT, d_loose TEXT, a TEXT, b TEXT);
INSERT INTO t VALUES
 (1,'2024-12-30','2024-12-30','2024-01-01 00:00:00','2024-01-02 12:00:00'),
 (2,'2021-01-01','2021-01-01','2024-03-01 10:00:00','2024-03-01 23:00:00'),
 (3,'2023-01-01','2023-01-01','2024-03-01 00:00:00','2024-03-04 00:00:00'),
 (4,'2024-02-29','2024-02-29','2024-03-01 23:00:00','2024-03-02 01:00:00'),
 (5,NULL,NULL,NULL,NULL),
 (6,'2024-01-02','2024-1-02','2024-03-05 00:00:00','2024-03-05 00:00:00');
```

**SQL answer:** four queries in the Code block, one per gotcha. The row-level one is `SQL_ROWS`:
```sql
SELECT id,
       CAST(strftime('%w', d) AS INTEGER) AS w_sql,
       ROUND(julianday(b) - julianday(a), 4) AS days_float,
       strftime('%Y', d) AS cal_year,
       strftime('%Y', date(d, '-3 days', 'weekday 4')) AS iso_year,
       (CAST(strftime('%j', date(d, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week
FROM t ORDER BY id
```

**pandas answer:** parse once with `pd.to_datetime`, then use the accessors. The key lines per gotcha are in the Code block; the mapping that makes the weekday numbers comparable is `(d.dt.dayofweek + 1) % 7` (Monday 0 becomes 1, Sunday 6 becomes 0).

**Example:** the translation table, each row demonstrated by the run below.

| Gotcha | SQLite | pandas | In my run |
|---|---|---|---|
| Week start | `%w`: Sunday = 0 | `dayofweek`: Monday = 0 | 2024-12-30 (Monday) is 1 in SQL and 0 in pandas; 2023-01-01 (Sunday) is 0 and 6 |
| Day difference | `julianday(b) - julianday(a)` float | `(b - a).dt.days` integer floor | 36 hours: 1.5 versus 1; 13 hours: 0.5417 versus 0 |
| NULL / NaT in a comparison | `d > x` is NULL, `NOT (d > x)` is NULL, row excluded both ways | `NaT > x` is False, `~(NaT > x)` is True | greater: 3 rows in both; not-greater: 2 in SQL, 3 in pandas |
| GROUP BY a missing key | NULL is its own group | `groupby` drops NaT keys by default (`dropna=False` keeps) | SQL 4 groups, pandas 3 groups by default |
| Text versus datetime | `'2024-1-02' < '2024-01-05'` is false (text order), `date('2024-1-02')` is NULL | parsed to Timestamp: true | SQL ids 2, 3; pandas ids 2, 3, 6 |
| ISO year | emulate with `strftime('%Y', date(d, '-3 days', 'weekday 4'))` | `isocalendar().year` | 2024-12-30 is ISO 2025-W01, 2021-01-01 is 2020-W53, 2023-01-01 is 2022-W52 |
| Period versus Timestamp | month is text `'2024-01'` | `Period('2024-01') == Timestamp('2024-01-01')` is False | merge on Period column versus datetime column: 0 rows |

Row 1 of the first printed table: id 1 is 2024-12-30, `%w` = 1, ISO year 2025, ISO week 1; the pair is 36 hours apart, so 1.5 days.

**Code:** run with `python3 -I`.
```python
# Q29: SQL versus pandas date gotchas on a six-row frame (week start: Sunday=0 in %w, Monday=0 in pandas; zone: none, all naive)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE t(id INTEGER PRIMARY KEY, d TEXT, d_loose TEXT, a TEXT, b TEXT);
INSERT INTO t VALUES
 (1,'2024-12-30','2024-12-30','2024-01-01 00:00:00','2024-01-02 12:00:00'),
 (2,'2021-01-01','2021-01-01','2024-03-01 10:00:00','2024-03-01 23:00:00'),
 (3,'2023-01-01','2023-01-01','2024-03-01 00:00:00','2024-03-04 00:00:00'),
 (4,'2024-02-29','2024-02-29','2024-03-01 23:00:00','2024-03-02 01:00:00'),
 (5,NULL,NULL,NULL,NULL),
 (6,'2024-01-02','2024-1-02','2024-03-05 00:00:00','2024-03-05 00:00:00');
"""
SQL_ROWS = """
SELECT id,
       CAST(strftime('%w', d) AS INTEGER) AS w_sql,
       ROUND(julianday(b) - julianday(a), 4) AS days_float,
       strftime('%Y', d) AS cal_year,
       strftime('%Y', date(d, '-3 days', 'weekday 4')) AS iso_year,
       (CAST(strftime('%j', date(d, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week
FROM t ORDER BY id
"""
SQL_NULLCMP = """
SELECT SUM(d > '2024-01-01') AS gt, SUM(NOT (d > '2024-01-01')) AS not_gt, COUNT(*) AS n,
       SUM(d IS NULL) AS null_rows
FROM t
"""
SQL_GROUP = "SELECT strftime('%Y', d) AS y, COUNT(*) AS n FROM t GROUP BY 1 ORDER BY 1"
SQL_TEXTCMP = "SELECT id, d_loose, d_loose < '2024-01-05' AS lt_text, date(d_loose) AS date_of_loose FROM t ORDER BY id"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_rows = pd.read_sql_query(SQL_ROWS, con)
print(sql_rows.to_string(index=False))
t = pd.read_sql_query("SELECT * FROM t ORDER BY id", con)
d = pd.to_datetime(t["d"]); a = pd.to_datetime(t["a"]); b = pd.to_datetime(t["b"])

# 1 week start: SQLite Sunday = 0, pandas Monday = 0 -> (dayofweek + 1) % 7 maps pandas to %w
w_pd = (d.dt.dayofweek + 1) % 7
print("pandas dayofweek (Mon=0):", d.dt.dayofweek.tolist(), " mapped to Sunday=0:", w_pd.tolist())
# 2 day difference: julianday float vs Timedelta.days (floor) vs total seconds
diff = b - a
print("Timedelta.days (whole days):", diff.dt.days.tolist())
print("Timedelta / 1 day (float):", (diff / pd.Timedelta(days=1)).round(4).tolist())
# 3 NULL versus NaT
sql_null = pd.read_sql_query(SQL_NULLCMP, con)
print(sql_null.to_string(index=False))
pd_gt = int((d > pd.Timestamp("2024-01-01")).sum()); pd_not = int((~(d > pd.Timestamp("2024-01-01"))).sum())
print("pandas (d > ts).sum():", pd_gt, " (~(d > ts)).sum():", pd_not)
# 4 groupby with a missing key
sql_grp = pd.read_sql_query(SQL_GROUP, con)
print(sql_grp.to_string(index=False))
g_default = d.dt.year.groupby(d.dt.year).size()
g_keep = d.dt.year.groupby(d.dt.year, dropna=False).size()
print("pandas groupby default:", g_default.to_dict(), " dropna=False:", {str(k): int(v) for k, v in g_keep.items()})
# 5 text versus datetime
sql_txt = pd.read_sql_query(SQL_TEXTCMP, con)
print(sql_txt.to_string(index=False))
loose = pd.to_datetime(t["d_loose"])
print("pandas parsed d_loose < Timestamp('2024-01-05') ids:", t.loc[loose < pd.Timestamp("2024-01-05"), "id"].tolist(),
      "| SQL text compare ids:", sql_txt.loc[sql_txt["lt_text"] == 1, "id"].tolist())
# 6 ISO year
iso = d.dt.isocalendar()
print("pandas isocalendar year/week:", list(zip(iso["year"].astype("Int64").tolist(), iso["week"].astype("Int64").tolist())))
# 7 Period versus Timestamp
p = pd.Period("2024-01", "M"); ts = pd.Timestamp("2024-01-01")
print("Period('2024-01') == Timestamp('2024-01-01'):", p == ts, "| p.to_timestamp() == ts:", p.to_timestamp() == ts)
left = pd.DataFrame({"k": pd.period_range("2024-01", periods=2, freq="M"), "x": [1, 2]})
right = pd.DataFrame({"k": pd.to_datetime(["2024-01-01", "2024-02-01"]), "y": [3, 4]})
print("merge Period col with datetime col: rows =", len(left.merge(right, on="k")),
      "| after to_timestamp(): rows =", len(left.assign(k=left["k"].dt.to_timestamp()).merge(right, on="k")))
print("SQL text: '2024-01' = '2024-01-01' ->", con.execute("SELECT '2024-01' = '2024-01-01'").fetchone()[0],
      "| date('2024-01') ->", con.execute("SELECT date('2024-01')").fetchone()[0])

# asserts: the columns that are meant to agree
ok = t["d"].notna()
assert w_pd[ok].tolist() == sql_rows.loc[ok, "w_sql"].astype(int).tolist()
assert (diff / pd.Timedelta(days=1)).round(4).dropna().tolist() == sql_rows["days_float"].dropna().tolist()
assert sql_rows.loc[ok, "iso_year"].astype(int).tolist() == iso.loc[ok, "year"].astype(int).tolist()
assert sql_rows.loc[ok, "iso_week"].tolist() == iso.loc[ok, "week"].astype(int).tolist()
assert (int(sql_null["gt"][0]), int(sql_null["not_gt"][0])) == (pd_gt, pd_not - 1)   # NOT(NULL) is NULL, ~NaT-compare is True
assert dict(zip(sql_grp["y"].dropna().astype(int), sql_grp["n"][sql_grp["y"].notna()])) == g_default.to_dict()
# brute force: the ISO emulation against isocalendar() for every day 2000-01-01..2040-12-31
days = pd.date_range("2000-01-01", "2040-12-31", freq="D")
con.execute("CREATE TABLE cal(d TEXT)")
con.executemany("INSERT INTO cal VALUES (?)", [(x,) for x in days.strftime("%Y-%m-%d")])
emu = pd.read_sql_query("""SELECT d, CAST(strftime('%Y', date(d, '-3 days', 'weekday 4')) AS INTEGER) AS iso_year,
       (CAST(strftime('%j', date(d, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week FROM cal ORDER BY d""", con)
ref = days.isocalendar()
assert emu["iso_year"].tolist() == ref["year"].astype(int).tolist()
assert emu["iso_week"].tolist() == ref["week"].astype(int).tolist()
print("ISO emulation date(d,'-3 days','weekday 4') matches isocalendar() on all", len(days), "days 2000-2040")
print("asserts passed (compared in id order)")
```

**Output (my run):**
```text
 id  w_sql  days_float cal_year iso_year  iso_week
  1    1.0      1.5000     2024     2025       1.0
  2    5.0      0.5417     2021     2020      53.0
  3    0.0      3.0000     2023     2022      52.0
  4    4.0      0.0833     2024     2024       9.0
  5    NaN         NaN      NaN      NaN       NaN
  6    2.0      0.0000     2024     2024       1.0
pandas dayofweek (Mon=0): [0.0, 4.0, 6.0, 3.0, nan, 1.0]  mapped to Sunday=0: [1.0, 5.0, 0.0, 4.0, nan, 2.0]
Timedelta.days (whole days): [1.0, 0.0, 3.0, 0.0, nan, 0.0]
Timedelta / 1 day (float): [1.5, 0.5417, 3.0, 0.0833, nan, 0.0]
 gt  not_gt  n  null_rows
  3       2  6          1
pandas (d > ts).sum(): 3  (~(d > ts)).sum(): 3
   y  n
 NaN  1
2021  1
2023  1
2024  3
pandas groupby default: {2021.0: 1, 2023.0: 1, 2024.0: 3}  dropna=False: {'2021.0': 1, '2023.0': 1, '2024.0': 3, 'nan': 1}
 id    d_loose  lt_text date_of_loose
  1 2024-12-30      0.0    2024-12-30
  2 2021-01-01      1.0    2021-01-01
  3 2023-01-01      1.0    2023-01-01
  4 2024-02-29      0.0    2024-02-29
  5        NaN      NaN           NaN
  6  2024-1-02      0.0           NaN
pandas parsed d_loose < Timestamp('2024-01-05') ids: [2, 3, 6] | SQL text compare ids: [2, 3]
pandas isocalendar year/week: [(2025, 1), (2020, 53), (2022, 52), (2024, 9), (<NA>, <NA>), (2024, 1)]
Period('2024-01') == Timestamp('2024-01-01'): False | p.to_timestamp() == ts: True
merge Period col with datetime col: rows = 0 | after to_timestamp(): rows = 2
SQL text: '2024-01' = '2024-01-01' -> 0 | date('2024-01') -> None
ISO emulation date(d,'-3 days','weekday 4') matches isocalendar() on all 14976 days 2000-2040
asserts passed (compared in id order)
```

**Edge cases:**
- NULL row 5: SQL week, difference and ISO columns are NULL; pandas gives NaT, `NaN`, `<NA>`.
- The `NOT` trap: `~(d > x)` in pandas counted the NaT row (3 rows), the SQL `NOT (d > x)` did not (2 rows). That is why I wrote the assert as `pd_not - 1`: the one-row difference is the point.
- `d_loose`: SQL `date('2024-1-02')` returns NULL because SQLite only accepts zero-padded `YYYY-MM-DD`; a text comparison puts `'2024-1-02'` after `'2024-01-05'` (character `1` versus `0` at the sixth position), so the row is wrongly excluded, while pandas parsed it correctly (pandas 3.0.5 parsed `'2024-1-02'` in a column that contained it, as I ran it).
- Period merge: no error and no match; the frame just comes back empty. Convert with `to_timestamp()` first.
- ISO emulation: I ran `date(d, '-3 days', 'weekday 4')` (the Thursday of the ISO week) against `isocalendar()` for every day from 2000-01-01 to 2040-12-31 (14976 days) and both the ISO year and the ISO week (`(%j - 1) / 7 + 1` of that Thursday) matched. Per the Wave A sources note, SQLite 3.45.1 returns NULL for `%G`, `%V`, `%U` and `%g` (I did not re-run those codes here), so the emulation is needed; newer SQLite versions list ISO codes, which this build does not have.
- `%W` in SQLite (Monday-based, week 00 before the first Monday) is not the ISO week; I did not use it for the ISO assert.

**Then explain:**
- Always state: week start, whether differences are floats or whole days, how NULL/NaT are treated, and what zone the timestamps are in.
- `julianday` differences are floats; to get calendar days between dates, wrap both in `date()` first (or round after the subtraction) and decide whether midnight-aligned counts or elapsed time is meant.
- pandas parsing is more forgiving than SQLite, which can hide dirty text; validate with `errors='coerce'` and count the NaT.
- Hedged (not executed): PostgreSQL, MySQL, BigQuery have real date types, so the text-versus-date row mostly does not occur there; `DATEDIFF` arguments differ by engine (Q36).

**Follow-ups:**
- "How would you find mixed-format text dates in a column?" `WHERE date(col) IS NULL AND col IS NOT NULL`.
- "ISO week for 2021-01-01 in pandas?" `isocalendar()` gives year 2020, week 53.
- "Do `groupby` and SQL agree on empty groups?" Neither creates them; use a spine (Q6).

**Common mistakes:**
- Using `%w` and `dayofweek` interchangeably.
- Using `(b - a).dt.days` when elapsed hours matter, or `julianday` when whole days matter.
- Using `~` on a comparison with NaT and counting the missing rows.
- `groupby` without `dropna=False` and silently losing the NaT group.
- Grouping by calendar year and week number near 1 January.

### Q30 ⭐⭐ 🟡 Time zones in pandas: pd.to_datetime(['2024-11-03 01:30'], ...) in America/New_York is ambiguous (clock falls back) and 2024-03-10 02:30 does not exist (spring forward). Show tz_localize raising AmbiguousTimeError and NonExistentTimeError, and the fixes ambiguous='NaT' / True / False array, nonexistent='shift_forward'. Show tz_convert('Asia/Kolkata') (no DST), comparing tz-naive with tz-aware (TypeError), and why timestamps should be stored in UTC. Concept: SQLite has only the 'localtime' and 'utc' modifiers, no named zones.
**Asked at:** pandas time series user guide and DataFrame.resample reference (opened), official documentation and not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Storing naive local times is ambiguous around DST (a clock that falls back repeats 01:30, one that springs forward skips 02:30), so store UTC, convert at the reporting edge, and when you must localise use the `ambiguous` and `nonexistent` arguments; in pandas 3.0.5 here the default failures were plain `ValueError`s (with `ambiguous` / `nonexistent` hints), not the `AmbiguousTimeError` and `NonExistentTimeError` class names in the question, which come from pytz (not installed here).

**Schema and sample data:** no table needed for the pandas part: two naive timestamps (`2024-11-03 01:30` and `2024-03-10 02:30`) and three UTC instants. For SQLite I use text values with explicit offsets. Conventions: America/New_York for the DST cases, Asia/Kolkata (UTC+5:30, no DST) for the report, UTC for storage; no week start involved.

**SQL answer:** SQLite has no named zones, only fixed offsets, the `'utc'` modifier (treats the value as local time and converts to UTC using the host zone) and `'localtime'` (host zone). A trailing offset in the text is parsed and converted to UTC, which resolves the ambiguity explicitly. The query in the Code block:
```sql
SELECT datetime('2024-11-03 01:30:00-04:00') AS first_pass_utc,
       datetime('2024-11-03 01:30:00-05:00') AS second_pass_utc,
       datetime('2024-03-05 20:00:00', '+5 hours', '+30 minutes') AS ist_wall_clock
```

**pandas answer:** `tz_localize` for naive to aware, `tz_convert` for aware to aware. The error handling is a small helper `attempt(label, fn)` in the Code block, which prints the exception class and first line of the message. Fix arguments: `ambiguous='NaT'`, `ambiguous=[True]` (first pass, DST) or `[False]` (second pass, standard time), `nonexistent='shift_forward'`, `'shift_backward'`, `'NaT'` or a `Timedelta`.

**Example:** New York falls back on 2024-11-03 at 02:00 EDT to 01:00 EST. So 01:30 occurs twice: 01:30 EDT (UTC-4) is 05:30 UTC and 01:30 EST (UTC-5) is 06:30 UTC. `ambiguous=[True]` picks the first (05:30 UTC), `[False]` the second (06:30 UTC). On 2024-03-10 at 02:00 EST clocks jump to 03:00 EDT, so 02:30 does not exist: `shift_forward` gives 03:00 EDT, `shift_backward` gives 01:59:59.999999 EST, a `Timedelta('1h')` gives 03:30 EDT. Kolkata is +05:30 all year, so 20:00 UTC is 01:30 the next day in all three sample dates.

**Code:** run with `python3 -I`.
```python
# Q30: time zones in pandas (America/New_York DST edges, Asia/Kolkata); SQLite has only fixed offsets plus 'utc'/'localtime'
import sqlite3
import pandas as pd

def attempt(label, fn):
    try:
        r = fn()
        print(label, "->", r)
        return r
    except Exception as ex:
        print(label, "->", type(ex).__name__ + ":", str(ex).splitlines()[0])

amb = pd.to_datetime(["2024-11-03 01:30"])           # clock falls back: 01:30 happens twice
gap = pd.to_datetime(["2024-03-10 02:30"])           # clock springs forward: 02:30 never happens
print("naive dtype:", amb.dtype)
attempt("ambiguous 01:30 default", lambda: amb.tz_localize("America/New_York"))
attempt("nonexistent 02:30 default", lambda: gap.tz_localize("America/New_York"))
print("pd.errors has AmbiguousTimeError:", hasattr(pd.errors, "AmbiguousTimeError"), "| has NonExistentTimeError:", hasattr(pd.errors, "NonExistentTimeError"))
try:
    import pytz
except ImportError:
    print("pytz is not installed in this environment (pandas 3 uses zoneinfo)")
attempt("ambiguous='NaT'", lambda: amb.tz_localize("America/New_York", ambiguous="NaT"))
first = attempt("ambiguous=True (DST, first pass)", lambda: amb.tz_localize("America/New_York", ambiguous=[True]))
second = attempt("ambiguous=False (standard, second pass)", lambda: amb.tz_localize("America/New_York", ambiguous=[False]))
attempt("nonexistent='shift_forward'", lambda: gap.tz_localize("America/New_York", nonexistent="shift_forward"))
attempt("nonexistent='shift_backward'", lambda: gap.tz_localize("America/New_York", nonexistent="shift_backward"))
attempt("nonexistent='NaT'", lambda: gap.tz_localize("America/New_York", nonexistent="NaT"))
attempt("nonexistent=Timedelta('1h')", lambda: gap.tz_localize("America/New_York", nonexistent=pd.Timedelta("1h")))
print("UTC of the two 01:30s:", first.tz_convert("UTC")[0], "and", second.tz_convert("UTC")[0])

utc = pd.to_datetime(["2024-03-05 20:00:00", "2024-07-01 20:00:00", "2024-12-31 20:00:00"]).tz_localize("UTC")
ist = utc.tz_convert("Asia/Kolkata")
print("Kolkata (no DST, always +05:30):", [str(x) for x in ist])
naive = pd.Timestamp("2024-03-05 20:00:00")
attempt("naive < aware", lambda: naive < utc[0])
attempt("naive == aware", lambda: naive == utc[0])
attempt("Series naive vs aware compare", lambda: pd.Series(pd.to_datetime(["2024-03-05"])) < pd.Series(utc[:1]))
attempt("tz_localize on an already aware index", lambda: utc.tz_localize("Asia/Kolkata"))
print("same instant in two zones is equal:", utc[0] == ist[0])

# SQLite side: fixed offsets only. A text value with an explicit offset resolves the ambiguity by itself.
con = sqlite3.connect(":memory:")
SQL_OFFSET = """
SELECT datetime('2024-11-03 01:30:00-04:00') AS first_pass_utc,
       datetime('2024-11-03 01:30:00-05:00') AS second_pass_utc,
       datetime('2024-03-05 20:00:00', '+5 hours', '+30 minutes') AS ist_wall_clock
"""
row = con.execute(SQL_OFFSET).fetchone()
print("SQLite:", row)
assert row[0] == str(first.tz_convert("UTC")[0].tz_localize(None)).replace("T", " ")
assert row[1] == str(second.tz_convert("UTC")[0].tz_localize(None))
assert row[2] == str(ist[0].tz_localize(None))
print("SQLite datetime('2024-03-10 02:30:00-05:00') =", con.execute("SELECT datetime('2024-03-10 02:30:00-05:00')").fetchone()[0],
      "(SQLite does not know that 02:30 does not exist in New York)")
print("asserts passed: SQLite offset arithmetic == pandas tz_convert for the three instants")
```

**Output (my run):**
```text
naive dtype: datetime64[us]
ambiguous 01:30 default -> ValueError: Cannot infer dst time from 2024-11-03 01:30:00, try using the 'ambiguous' argument
nonexistent 02:30 default -> ValueError: 2024-03-10 02:30:00 is a nonexistent time due to daylight savings time. Try using the 'nonexistent' argument.
pd.errors has AmbiguousTimeError: False | has NonExistentTimeError: False
pytz is not installed in this environment (pandas 3 uses zoneinfo)
ambiguous='NaT' -> DatetimeIndex(['NaT'], dtype='datetime64[us, America/New_York]', freq=None)
ambiguous=True (DST, first pass) -> DatetimeIndex(['2024-11-03 01:30:00-04:00'], dtype='datetime64[us, America/New_York]', freq=None)
ambiguous=False (standard, second pass) -> DatetimeIndex(['2024-11-03 01:30:00-05:00'], dtype='datetime64[us, America/New_York]', freq=None)
nonexistent='shift_forward' -> DatetimeIndex(['2024-03-10 03:00:00-04:00'], dtype='datetime64[us, America/New_York]', freq=None)
nonexistent='shift_backward' -> DatetimeIndex(['2024-03-10 01:59:59.999999-05:00'], dtype='datetime64[us, America/New_York]', freq=None)
nonexistent='NaT' -> DatetimeIndex(['NaT'], dtype='datetime64[us, America/New_York]', freq=None)
nonexistent=Timedelta('1h') -> DatetimeIndex(['2024-03-10 03:30:00-04:00'], dtype='datetime64[us, America/New_York]', freq=None)
UTC of the two 01:30s: 2024-11-03 05:30:00+00:00 and 2024-11-03 06:30:00+00:00
Kolkata (no DST, always +05:30): ['2024-03-06 01:30:00+05:30', '2024-07-02 01:30:00+05:30', '2025-01-01 01:30:00+05:30']
naive < aware -> TypeError: Cannot compare tz-naive and tz-aware timestamps
naive == aware -> False
Series naive vs aware compare -> TypeError: Invalid comparison between dtype=datetime64[us] and DatetimeArray
tz_localize on an already aware index -> TypeError: Already tz-aware, use tz_convert to convert.
same instant in two zones is equal: True
SQLite: ('2024-11-03 05:30:00', '2024-11-03 06:30:00', '2024-03-06 01:30:00')
SQLite datetime('2024-03-10 02:30:00-05:00') = 2024-03-10 07:30:00 (SQLite does not know that 02:30 does not exist in New York)
asserts passed: SQLite offset arithmetic == pandas tz_convert for the three instants
```

**Edge cases:**
- Default behaviour: both ambiguous and nonexistent inputs raised `ValueError` with a hint to use the `ambiguous` or `nonexistent` argument. `pd.errors` in 3.0.5 has no `AmbiguousTimeError` or `NonExistentTimeError`, and pytz is not installed here. With pytz installed, the older class names may appear (not executed here).
- `ambiguous='NaT'` and `nonexistent='NaT'` return NaT, which then silently falls out of groupby (Q29); count them before dropping.
- Comparing naive with aware: `<` raised `TypeError: Cannot compare tz-naive and tz-aware timestamps`; `==` returned False without error. A Series comparison raised `TypeError: Invalid comparison between dtype=datetime64[us] and DatetimeArray`.
- `tz_localize` on an already aware index raised `TypeError: Already tz-aware, use tz_convert to convert.`
- The same instant in two zones is equal (`utc[0] == ist[0]` is True): equality is on the instant, not the wall clock.
- SQLite does not know that 02:30 does not exist: `datetime('2024-03-10 02:30:00-05:00')` simply returned 07:30:00 UTC.
- The `'localtime'` and `'utc'` modifiers depend on the host zone; I did not print their results because they would change with the machine.

**Then explain:**
- Store UTC (an unambiguous instant) and convert to the business zone at the edge; keep the zone name (not just the offset) when you must reproduce local rules in the future.
- Local wall-clock times need a zone name and a rule for the two bad cases; offsets alone resolve only the ambiguous case.
- India has no DST, so IST is a fixed `+05:30`; US/EU zones are not.
- pandas 3 default time unit for strings is microseconds (`datetime64[us]`), as printed.
- Hedged (not executed): PostgreSQL `AT TIME ZONE`, `timestamptz`; MySQL `CONVERT_TZ` (needs zone tables); BigQuery `TIMESTAMP`, `DATETIME(ts, 'Asia/Kolkata')`; I am quoting these from memory.

**Follow-ups:**
- "How do daily counts change with the time zone?" Q16 (the day boundary) and Q38 (DST days with 23 or 25 hours).
- "Why not store local times?" Ambiguity, nonexistence and rule changes.
- "How do I log events from several countries?" UTC plus the user's zone name if needed for reporting.

**Common mistakes:**
- Localising with a fixed offset (`-05:00`) and reading it as New York all year.
- Dropping the NaT rows from `ambiguous='NaT'` without counting them.
- Comparing naive and aware values and catching the `TypeError` with a blanket `except`.
- Using `'localtime'` in SQLite and assuming it is the business zone.

### Q31 ⭐⭐ 🟡 Calendar (date dimension) table: build calendar(cal_date, year, month, quarter, week_start_monday, day_of_week, is_weekend, fiscal_year, fiscal_quarter, is_holiday) for 2023-2024 with a recursive CTE in SQLite, load a small holidays table, and use it to fill zero-sales days and to compute revenue per working day. Explain why a physical calendar table beats generating the spine in every query, and show generate_series and pandas pd.date_range with dt accessors as the equivalents (generate_series hedged, not executed).
**Asked at:** search-result snippets of date-spine and churn guides (Galaxy cohort-churn glossary, a LinkedIn list of time-series SQL topics; not opened), guides and not candidate reports; analyst and data engineer screens
**Say this first (1 line):** A physical `calendar` table (one row per date with year, month, quarter, Monday week start, ISO-style day of week, weekend flag, fiscal year/quarter and holiday flag) is built once with a recursive CTE and then joined, so every report shares the same definitions and zero-sales days appear without rebuilding a spine each time.

**Schema and sample data:** holidays (five rows) and a small sales table (seven rows) with no sales on several days. Conventions: week starts Monday, `day_of_week` is Monday = 1 to Sunday = 7, fiscal year April to March labelled by start year (`FY2023-24`), dates are plain dates (no time zone), range 2023-01-01 to 2024-12-31 (731 days).
```sql
CREATE TABLE holidays(holiday_date TEXT PRIMARY KEY, name TEXT);
INSERT INTO holidays VALUES ('2023-01-26','Republic Day'),('2023-08-15','Independence Day'),
  ('2024-01-26','Republic Day'),('2024-08-15','Independence Day'),('2024-03-25','Holi');
CREATE TABLE sales(sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES ('2024-01-02',100),('2024-01-03',200),('2024-01-05',300),('2024-01-06',50),
  ('2024-01-26',70),('2024-02-01',400),('2024-02-02',600);
```

**SQL answer:** `SQL_CAL` builds the table; `SQL_ZERO` fills zero-sales days; `SQL_PER_WD` returns revenue per working day by month (Code block). The Monday week start uses `date(cal_date, 'weekday 0', '-6 days')`.
```sql
CREATE TABLE calendar AS
WITH RECURSIVE d(cal_date) AS (
  SELECT '2023-01-01' UNION ALL SELECT date(cal_date, '+1 day') FROM d WHERE cal_date < '2024-12-31'
), x AS (
  SELECT cal_date,
         CAST(strftime('%Y', cal_date) AS INTEGER) AS year,
         CAST(strftime('%m', cal_date) AS INTEGER) AS month,
         (CAST(strftime('%w', cal_date) AS INTEGER) + 6) % 7 + 1 AS day_of_week
  FROM d
)
SELECT x.cal_date, x.year, x.month,
       (x.month + 2) / 3 AS quarter,
       date(x.cal_date, 'weekday 0', '-6 days') AS week_start_monday,
       x.day_of_week,
       CASE WHEN x.day_of_week >= 6 THEN 1 ELSE 0 END AS is_weekend,
       'FY' || (x.year - (x.month < 4)) || '-' || substr(x.year - (x.month < 4) + 1, 3, 2) AS fiscal_year,
       (x.month + 8) % 12 / 3 + 1 AS fiscal_quarter,
       CASE WHEN h.holiday_date IS NULL THEN 0 ELSE 1 END AS is_holiday
FROM x LEFT JOIN holidays h ON h.holiday_date = x.cal_date
```
```sql
SELECT c.cal_date, c.day_of_week, COALESCE(SUM(s.amount), 0) AS revenue
FROM calendar c LEFT JOIN sales s ON s.sale_date = c.cal_date
WHERE c.cal_date >= '2024-01-01' AND c.cal_date < '2024-01-08'
GROUP BY c.cal_date, c.day_of_week ORDER BY c.cal_date
```
```sql
SELECT substr(c.cal_date, 1, 7) AS month,
       COUNT(*) AS days,
       SUM(CASE WHEN c.is_weekend = 0 AND c.is_holiday = 0 THEN 1 ELSE 0 END) AS working_days,
       (SELECT COALESCE(SUM(s.amount), 0) FROM sales s WHERE substr(s.sale_date, 1, 7) = substr(c.cal_date, 1, 7)) AS revenue
FROM calendar c
WHERE c.cal_date >= '2024-01-01' AND c.cal_date < '2024-03-01'
GROUP BY substr(c.cal_date, 1, 7) ORDER BY month
```

**pandas answer:** `pd.date_range` plus accessors, with `to_period('Q-MAR')` for the fiscal columns, built as a DataFrame of the same ten columns and compared whole:
```py
dr = pd.date_range("2023-01-01", "2024-12-31", freq="D")
fq = dr.to_period("Q-MAR")
cal_pd = pd.DataFrame({
    "cal_date": dr.strftime("%Y-%m-%d"), "year": dr.year, "month": dr.month, "quarter": dr.quarter,
    "week_start_monday": (dr - pd.to_timedelta(dr.dayofweek, unit="D")).strftime("%Y-%m-%d"),
    "day_of_week": dr.dayofweek + 1, "is_weekend": (dr.dayofweek >= 5).astype(int),
    "fiscal_year": ["FY%d-%02d" % (q.qyear - 1, q.qyear % 100) for q in fq],
    "fiscal_quarter": fq.quarter, "is_holiday": dr.isin(hol).astype(int)})
```

**Example:** 2024-03-31 is a Sunday: `day_of_week` 7, weekend 1, week start Monday 2024-03-25 (the same week as Holi on Monday 25 March, which is flagged `is_holiday`), fiscal year FY2023-24, fiscal quarter 4. 2024-04-01 is a Monday and the first day of FY2024-25 Q1. January 2024: 31 days, 23 weekdays (1 January is a Monday), minus the Friday 26 January holiday = 22 working days; revenue 100 + 200 + 300 + 50 + 70 = 720, so 720 / 22 = 32.73 per working day (the 6 January Saturday sale of 50 and the 26 January holiday sale of 70 are counted in revenue). February 2024: 29 days, 21 weekdays, no holiday; revenue 400 + 600 = 1000; 1000 / 21 = 47.62. In the first week of January the calendar join returns 0 for 1, 4 and 7 January (no sales rows) while the plain sales table would not show them.

**Code:** run with `python3 -I`.
```python
# Q31: calendar (date dimension) table 2023-2024; weeks start Monday; fiscal year April-March; all dates naive
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE holidays(holiday_date TEXT PRIMARY KEY, name TEXT);
INSERT INTO holidays VALUES ('2023-01-26','Republic Day'),('2023-08-15','Independence Day'),
  ('2024-01-26','Republic Day'),('2024-08-15','Independence Day'),('2024-03-25','Holi');
CREATE TABLE sales(sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES ('2024-01-02',100),('2024-01-03',200),('2024-01-05',300),('2024-01-06',50),
  ('2024-01-26',70),('2024-02-01',400),('2024-02-02',600);
"""
SQL_CAL = """
CREATE TABLE calendar AS
WITH RECURSIVE d(cal_date) AS (
  SELECT '2023-01-01' UNION ALL SELECT date(cal_date, '+1 day') FROM d WHERE cal_date < '2024-12-31'
), x AS (
  SELECT cal_date,
         CAST(strftime('%Y', cal_date) AS INTEGER) AS year,
         CAST(strftime('%m', cal_date) AS INTEGER) AS month,
         (CAST(strftime('%w', cal_date) AS INTEGER) + 6) % 7 + 1 AS day_of_week
  FROM d
)
SELECT x.cal_date, x.year, x.month,
       (x.month + 2) / 3 AS quarter,
       date(x.cal_date, 'weekday 0', '-6 days') AS week_start_monday,
       x.day_of_week,
       CASE WHEN x.day_of_week >= 6 THEN 1 ELSE 0 END AS is_weekend,
       'FY' || (x.year - (x.month < 4)) || '-' || substr(x.year - (x.month < 4) + 1, 3, 2) AS fiscal_year,
       (x.month + 8) % 12 / 3 + 1 AS fiscal_quarter,
       CASE WHEN h.holiday_date IS NULL THEN 0 ELSE 1 END AS is_holiday
FROM x LEFT JOIN holidays h ON h.holiday_date = x.cal_date
"""
SQL_ZERO = """
SELECT c.cal_date, c.day_of_week, COALESCE(SUM(s.amount), 0) AS revenue
FROM calendar c LEFT JOIN sales s ON s.sale_date = c.cal_date
WHERE c.cal_date >= '2024-01-01' AND c.cal_date < '2024-01-08'
GROUP BY c.cal_date, c.day_of_week ORDER BY c.cal_date
"""
SQL_PER_WD = """
SELECT substr(c.cal_date, 1, 7) AS month,
       COUNT(*) AS days,
       SUM(CASE WHEN c.is_weekend = 0 AND c.is_holiday = 0 THEN 1 ELSE 0 END) AS working_days,
       (SELECT COALESCE(SUM(s.amount), 0) FROM sales s WHERE substr(s.sale_date, 1, 7) = substr(c.cal_date, 1, 7)) AS revenue
FROM calendar c
WHERE c.cal_date >= '2024-01-01' AND c.cal_date < '2024-03-01'
GROUP BY substr(c.cal_date, 1, 7) ORDER BY month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
con.execute(SQL_CAL)
cal_sql = pd.read_sql_query("SELECT * FROM calendar ORDER BY cal_date", con)
print("rows:", len(cal_sql), "from", cal_sql["cal_date"].iloc[0], "to", cal_sql["cal_date"].iloc[-1])
print(cal_sql[cal_sql["cal_date"].isin(["2023-12-31", "2024-01-01", "2024-03-31", "2024-04-01", "2024-03-25"])].to_string(index=False))
zero = pd.read_sql_query(SQL_ZERO, con)
print(zero.to_string(index=False))
per = pd.read_sql_query(SQL_PER_WD, con)
per["revenue_per_working_day"] = (per["revenue"] / per["working_days"]).round(2)
print(per.to_string(index=False))

# pandas calendar
hol = pd.to_datetime(pd.read_sql_query("SELECT holiday_date FROM holidays", con)["holiday_date"])
dr = pd.date_range("2023-01-01", "2024-12-31", freq="D")
fq = dr.to_period("Q-MAR")
cal_pd = pd.DataFrame({
    "cal_date": dr.strftime("%Y-%m-%d"), "year": dr.year, "month": dr.month, "quarter": dr.quarter,
    "week_start_monday": (dr - pd.to_timedelta(dr.dayofweek, unit="D")).strftime("%Y-%m-%d"),
    "day_of_week": dr.dayofweek + 1, "is_weekend": (dr.dayofweek >= 5).astype(int),
    "fiscal_year": ["FY%d-%02d" % (q.qyear - 1, q.qyear % 100) for q in fq],
    "fiscal_quarter": fq.quarter, "is_holiday": dr.isin(hol).astype(int)})
# compared on all 731 rows in cal_date order, every column
pd.testing.assert_frame_equal(cal_pd, cal_sql, check_dtype=False)
sales = pd.read_sql_query("SELECT * FROM sales", con)
sales["sale_date"] = pd.to_datetime(sales["sale_date"])
daily = sales.groupby("sale_date")["amount"].sum().reindex(pd.date_range("2024-01-01", "2024-01-07"), fill_value=0)
assert daily.tolist() == zero["revenue"].tolist()
c = cal_pd.assign(d=dr)
wd = c[(c["d"] >= "2024-01-01") & (c["d"] < "2024-03-01")]
wd = wd.assign(month=wd["d"].dt.strftime("%Y-%m"), working=((wd["is_weekend"] == 0) & (wd["is_holiday"] == 0)).astype(int))
pd_per = wd.groupby("month").agg(days=("d", "size"), working_days=("working", "sum")).reset_index()
pd_per["revenue"] = pd_per["month"].map(sales.groupby(sales["sale_date"].dt.strftime("%Y-%m"))["amount"].sum()).fillna(0).astype(int)
pd_per["revenue_per_working_day"] = (pd_per["revenue"] / pd_per["working_days"]).round(2)
pd.testing.assert_frame_equal(pd_per, per, check_dtype=False)
print(pd_per.to_string(index=False))
print("asserts passed: SQL calendar == pandas calendar (731 rows x 10 cols), zero-fill and per-working-day match")
```

**Output (my run):**
```text
rows: 731 from 2023-01-01 to 2024-12-31
  cal_date  year  month  quarter week_start_monday  day_of_week  is_weekend fiscal_year  fiscal_quarter  is_holiday
2023-12-31  2023     12        4        2023-12-25            7           1   FY2023-24               3           0
2024-01-01  2024      1        1        2024-01-01            1           0   FY2023-24               4           0
2024-03-25  2024      3        1        2024-03-25            1           0   FY2023-24               4           1
2024-03-31  2024      3        1        2024-03-25            7           1   FY2023-24               4           0
2024-04-01  2024      4        2        2024-04-01            1           0   FY2024-25               1           0
  cal_date  day_of_week  revenue
2024-01-01            1        0
2024-01-02            2      100
2024-01-03            3      200
2024-01-04            4        0
2024-01-05            5      300
2024-01-06            6       50
2024-01-07            7        0
  month  days  working_days  revenue  revenue_per_working_day
2024-01    31            22      720                    32.73
2024-02    29            21     1000                    47.62
  month  days  working_days  revenue  revenue_per_working_day
2024-01    31            22      720                    32.73
2024-02    29            21     1000                    47.62
asserts passed: SQL calendar == pandas calendar (731 rows x 10 cols), zero-fill and per-working-day match
```

**Edge cases:**
- Coverage: the calendar must span the data; a sale outside 2023 to 2024 would not match any calendar row on an inner join, and would be lost. Extend it (or check `MIN`/`MAX`) in the load job.
- Sales on non-working days (a Saturday, a holiday) still add revenue but not working days, so revenue per working day is inflated for those months; decide whether to include them.
- Duplicate holidays: `holiday_date` is a primary key, so the left join cannot fan out the calendar.
- Changing holidays: a physical table needs a maintenance step; the holidays table is the part that changes each year (state dates are not looked up here, these are sample rows).
- Time zones: a `sale_date` derived from UTC may differ from the local date (Q16); build the date column in the reporting zone.
- Leap years: 2024 has 366 days; the table has 731 rows for 2023 and 2024 together, as asserted.

**Then explain:**
- A physical table beats a generated spine because definitions (week start, fiscal year, holidays) live in one place, joins are index-friendly, and analysts do not re-derive them. The recursive CTE is a one-time loader, not a per-query tool.
- Zero-fill: `calendar LEFT JOIN sales` keeps the empty days; a plain `GROUP BY sale_date` cannot.
- Working-day denominators let you compare months of different length.
- Equivalents (generate_series hedged, not executed): PostgreSQL `generate_series('2023-01-01'::date, '2024-12-31'::date, interval '1 day')`; pandas `pd.date_range('2023-01-01', '2024-12-31', freq='D')` with `.dt.year`, `.dt.dayofweek`, and so on (run above).

**Follow-ups:**
- "Add ISO week numbers?" Use the Thursday emulation (Q29/Q43).
- "Multiple countries' holidays?" Add `country` to `holidays` and to the join; the calendar becomes a calendar x country table.
- "Fiscal weeks?" Needs a rule (4-4-5 or 52/53 week); state it first.

**Common mistakes:**
- Generating a spine in every query slightly differently.
- Forgetting the holiday flag for weekends (it still must not subtract twice).
- Hard-coding Sunday-start weeks in one report and Monday-start in another.
- Letting the calendar end before the latest data date.

### Q32 ⭐⭐ 🔴 Fiscal-year-over-year comparison with missing months: monthly_revenue(month, revenue) for FY2023-24 and FY2024-25 where some months are missing. Return for each fiscal month (April = 1 to March = 12) revenue this fiscal year, revenue last fiscal year, and YoY percent, plus fiscal year-to-date for both years up to the latest loaded month only (so a half-loaded FY2024-25 compares to the same months of the prior year, not the full year). Build with a fiscal calendar spine and conditional aggregation; pandas: pivot on fiscal month and fiscal year with reindex 1..12 and cumsum limited by the last loaded month.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Map each month to a fiscal year and a fiscal month (April = 1 ... March = 12), join onto a 1-to-12 fiscal-month spine, use conditional aggregation to put this year and last year side by side, and compute year-to-date only up to the latest loaded fiscal month of the current year so a half-loaded year is compared with the same months of the prior year, not with its full total.

**Schema and sample data:** FY2023-24 has no August 2023; FY2024-25 is loaded through September 2024 (fiscal month 6) and is missing July 2024. Conventions: fiscal year April to March labelled by start year (`fy` = 2024 means FY2024-25), fiscal month = `(month + 8) % 12 + 1`, `month` column stores the first of the month as text, no time zone.
```sql
CREATE TABLE monthly_revenue(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_revenue VALUES
 ('2023-04-01',100),('2023-05-01',110),('2023-06-01',120),('2023-07-01',130),
 ('2023-09-01',150),('2023-10-01',160),('2023-11-01',170),('2023-12-01',180),
 ('2024-01-01',190),('2024-02-01',200),('2024-03-01',210),
 ('2024-04-01',120),('2024-05-01',121),('2024-06-01',132),
 ('2024-08-01',140),('2024-09-01',165);
```

**SQL answer:** `SQL_MAIN` in the Code block. `cur` is the latest fiscal year in the data, `latest` is its highest loaded fiscal month, `spine` is 1 to 12, `g` pivots the two years with `SUM(CASE ...)`, and the year-to-date columns are running sums that are blanked beyond the latest loaded month.
```sql
WITH f AS (
  SELECT revenue,
         CAST(strftime('%Y', month) AS INTEGER) - (CAST(strftime('%m', month) AS INTEGER) < 4) AS fy,
         (CAST(strftime('%m', month) AS INTEGER) + 8) % 12 + 1 AS fm
  FROM monthly_revenue
), cur AS (SELECT MAX(fy) AS fy FROM f),
latest AS (SELECT MAX(fm) AS fm FROM f WHERE fy = (SELECT fy FROM cur)),
spine(fm) AS (SELECT 1 UNION ALL SELECT fm + 1 FROM spine WHERE fm < 12),
g AS (
  SELECT s.fm,
         SUM(CASE WHEN f.fy = (SELECT fy FROM cur) THEN f.revenue END) AS rev_this,
         SUM(CASE WHEN f.fy = (SELECT fy FROM cur) - 1 THEN f.revenue END) AS rev_last
  FROM spine s LEFT JOIN f ON f.fm = s.fm
  GROUP BY s.fm
)
SELECT fm, rev_this, rev_last,
       ROUND(100.0 * (rev_this - rev_last) / NULLIF(rev_last, 0), 1) AS yoy_pct,
       CASE WHEN fm <= (SELECT fm FROM latest)
            THEN SUM(COALESCE(rev_this, 0)) OVER (ORDER BY fm) END AS ytd_this,
       CASE WHEN fm <= (SELECT fm FROM latest)
            THEN SUM(COALESCE(rev_last, 0)) OVER (ORDER BY fm) END AS ytd_last
FROM g ORDER BY fm
```

**pandas answer:** `pivot_table` on fiscal month and fiscal year, `reindex(range(1, 13))`, `cumsum` of `fillna(0)` and `where(fm <= latest_fm)`:
```py
p = mr["month"].dt.to_period("Q-MAR")
mr["fy"] = p.dt.qyear - 1
mr["fm"] = (mr["month"].dt.month + 8) % 12 + 1
piv = mr.pivot_table(index="fm", columns="fy", values="revenue", aggfunc="sum").reindex(range(1, 13))
cur_fy = mr["fy"].max()
rev_this, rev_last = piv[cur_fy], piv[cur_fy - 1]
latest_fm = int(mr.loc[mr["fy"] == cur_fy, "fm"].max())
pdf = pd.DataFrame({"fm": piv.index, "rev_this": rev_this.to_numpy(), "rev_last": rev_last.to_numpy()})
pdf["yoy_pct"] = (100.0 * (pdf["rev_this"] - pdf["rev_last"]) / pdf["rev_last"].replace(0, np.nan)).round(1)
mask = pdf["fm"] <= latest_fm
pdf["ytd_this"] = pdf["rev_this"].fillna(0).cumsum().where(mask)
pdf["ytd_last"] = pdf["rev_last"].fillna(0).cumsum().where(mask)
```

**Example:** this year (FY2024-25) by fiscal month: Apr 120, May 121, Jun 132, Jul missing, Aug 140, Sep 165. Last year: Apr 100, May 110, Jun 120, Jul 130, Aug missing, Sep 150, Oct 160 ... Mar 210. YoY for April: (120 - 100) / 100 = 20.0%; for July and August the result is NULL because one side is missing. Year-to-date through September (fiscal month 6): this year 120 + 121 + 132 + 0 + 140 + 165 = 678, last year 100 + 110 + 120 + 130 + 0 + 150 = 610, so 678 versus 610 is +11.1%. Comparing 678 to the full last year (1720) would give -60.6%.

**Code:** run with `python3 -I`.
```python
# Q32: fiscal-year-over-year with missing months; fiscal year April-March, label = start year; as-of = latest loaded month
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE monthly_revenue(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_revenue VALUES
 ('2023-04-01',100),('2023-05-01',110),('2023-06-01',120),('2023-07-01',130),
 ('2023-09-01',150),('2023-10-01',160),('2023-11-01',170),('2023-12-01',180),
 ('2024-01-01',190),('2024-02-01',200),('2024-03-01',210),
 ('2024-04-01',120),('2024-05-01',121),('2024-06-01',132),
 ('2024-08-01',140),('2024-09-01',165);
"""
# 2023-08 (last year) and 2024-07 (this year) are missing. Latest loaded month: 2024-09 = fiscal month 6.
SQL_MAIN = """
WITH f AS (
  SELECT revenue,
         CAST(strftime('%Y', month) AS INTEGER) - (CAST(strftime('%m', month) AS INTEGER) < 4) AS fy,
         (CAST(strftime('%m', month) AS INTEGER) + 8) % 12 + 1 AS fm
  FROM monthly_revenue
), cur AS (SELECT MAX(fy) AS fy FROM f),
latest AS (SELECT MAX(fm) AS fm FROM f WHERE fy = (SELECT fy FROM cur)),
spine(fm) AS (SELECT 1 UNION ALL SELECT fm + 1 FROM spine WHERE fm < 12),
g AS (
  SELECT s.fm,
         SUM(CASE WHEN f.fy = (SELECT fy FROM cur) THEN f.revenue END) AS rev_this,
         SUM(CASE WHEN f.fy = (SELECT fy FROM cur) - 1 THEN f.revenue END) AS rev_last
  FROM spine s LEFT JOIN f ON f.fm = s.fm
  GROUP BY s.fm
)
SELECT fm, rev_this, rev_last,
       ROUND(100.0 * (rev_this - rev_last) / NULLIF(rev_last, 0), 1) AS yoy_pct,
       CASE WHEN fm <= (SELECT fm FROM latest)
            THEN SUM(COALESCE(rev_this, 0)) OVER (ORDER BY fm) END AS ytd_this,
       CASE WHEN fm <= (SELECT fm FROM latest)
            THEN SUM(COALESCE(rev_last, 0)) OVER (ORDER BY fm) END AS ytd_last
FROM g ORDER BY fm
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_df["ytd_pct"] = (100.0 * (sql_df["ytd_this"] - sql_df["ytd_last"]) / sql_df["ytd_last"]).round(1)
print(sql_df.to_string(index=False))
last_row = sql_df.dropna(subset=["ytd_this"]).iloc[-1]
print("YTD through fiscal month %d: this FY %d vs last FY %d -> %.1f%%" % (last_row["fm"], last_row["ytd_this"], last_row["ytd_last"], last_row["ytd_pct"]))
full_last = pd.read_sql_query("SELECT SUM(revenue) AS s FROM monthly_revenue WHERE month < '2024-04-01'", con)["s"][0]
print("wrong comparison (this YTD vs the full last FY):", round(100.0 * (last_row["ytd_this"] - full_last) / full_last, 1), "% with last FY total", full_last)

mr = pd.read_sql_query("SELECT * FROM monthly_revenue", con)
mr["month"] = pd.to_datetime(mr["month"])
p = mr["month"].dt.to_period("Q-MAR")
mr["fy"] = p.dt.qyear - 1
mr["fm"] = (mr["month"].dt.month + 8) % 12 + 1
piv = mr.pivot_table(index="fm", columns="fy", values="revenue", aggfunc="sum").reindex(range(1, 13))
cur_fy = mr["fy"].max()
rev_this, rev_last = piv[cur_fy], piv[cur_fy - 1]
latest_fm = int(mr.loc[mr["fy"] == cur_fy, "fm"].max())
pdf = pd.DataFrame({"fm": piv.index, "rev_this": rev_this.to_numpy(), "rev_last": rev_last.to_numpy()})
pdf["yoy_pct"] = (100.0 * (pdf["rev_this"] - pdf["rev_last"]) / pdf["rev_last"].replace(0, np.nan)).round(1)
mask = pdf["fm"] <= latest_fm
pdf["ytd_this"] = pdf["rev_this"].fillna(0).cumsum().where(mask)
pdf["ytd_last"] = pdf["rev_last"].fillna(0).cumsum().where(mask)
pdf["ytd_pct"] = (100.0 * (pdf["ytd_this"] - pdf["ytd_last"]) / pdf["ytd_last"]).round(1)
# compared on fiscal month 1..12, NaN == NULL
pd.testing.assert_frame_equal(pdf, sql_df, check_dtype=False)
print("asserts passed: SQL == pandas pivot/reindex/cumsum for fiscal months 1..12; cur FY start year =", cur_fy, "latest fm =", latest_fm)
```

**Output (my run):**
```text
 fm  rev_this  rev_last  yoy_pct  ytd_this  ytd_last  ytd_pct
  1     120.0     100.0     20.0     120.0     100.0     20.0
  2     121.0     110.0     10.0     241.0     210.0     14.8
  3     132.0     120.0     10.0     373.0     330.0     13.0
  4       NaN     130.0      NaN     373.0     460.0    -18.9
  5     140.0       NaN      NaN     513.0     460.0     11.5
  6     165.0     150.0     10.0     678.0     610.0     11.1
  7       NaN     160.0      NaN       NaN       NaN      NaN
  8       NaN     170.0      NaN       NaN       NaN      NaN
  9       NaN     180.0      NaN       NaN       NaN      NaN
 10       NaN     190.0      NaN       NaN       NaN      NaN
 11       NaN     200.0      NaN       NaN       NaN      NaN
 12       NaN     210.0      NaN       NaN       NaN      NaN
YTD through fiscal month 6: this FY 678 vs last FY 610 -> 11.1%
wrong comparison (this YTD vs the full last FY): -60.6 % with last FY total 1720
asserts passed: SQL == pandas pivot/reindex/cumsum for fiscal months 1..12; cur FY start year = 2024 latest fm = 6
```

**Edge cases:**
- Missing month inside the loaded range (July 2024, August 2023): the monthly revenue and YoY are NULL for that month, and the YTD treats a missing month as 0. That is an assumption (no sales); if the month was simply not loaded, YTD is understated, and the per-month YTD percent is misleading at that point (fiscal month 4 shows -18.9%, a result of the missing July 2024, which then recovers to +11.5% at month 5 when last year's August is the missing one). Report the missing months next to the YTD.
- Future fiscal months (7 to 12): this-year columns are NULL and the YTD columns are NULL because they are beyond the latest loaded month; last year's later months are still shown in `rev_last` but not accumulated.
- Zero base: `NULLIF(rev_last, 0)` returns NULL instead of an error; pandas replaces 0 with NaN for the same effect.
- Duplicate month rows: `SUM(CASE ...)` would add them; the primary key on `month` prevents it. If the feed can restate months, deduplicate first.
- Fiscal year naming: here `fy` is the start year; do not mix with pandas `qyear` (end year) without the subtract of 1 (the code does).
- If the latest loaded month is mid-month (partial month), YTD for that month is partial; this question assumes complete loaded months.

**Then explain:**
- The spine guarantees 12 rows even if neither year has a row for a fiscal month; the join to the data is a `LEFT JOIN`.
- "Up to the latest loaded month only" is `latest_fm = MAX(fm)` for the current fiscal year, applied as a mask to both years' running totals so the comparison is like for like.
- Conditional aggregation (`SUM(CASE WHEN fy = ... THEN revenue END)`) is the SQL pivot; pandas does it with `pivot_table`.
- Hedged (not executed): engines with `PIVOT` clauses (SQL Server, Snowflake, Oracle) would shorten the pivot step; `generate_series` can supply the 1 to 12 spine in PostgreSQL.

**Follow-ups:**
- "Show all 12 months of last year as a forecast base?" Keep the columns but separate actual from baseline.
- "Quarter-level fiscal YoY?" Aggregate by fiscal quarter first (Q25), then compare.
- "What if the fiscal year changes definition?" Put the mapping in the calendar table (Q31).

**Common mistakes:**
- Comparing a half-loaded year with a full prior year.
- `LAG(revenue, 12)` on rows with gaps (Q17).
- Treating a missing month as 0 without saying so.
- Mixing fiscal year labels (start year versus end year).

### Q33 ⭐⭐ 🔴 Churn and resurrection by month: events(user_id, event_ts). Classify each user-month transition as new (first ever active month), retained (active in m-1 and m), churned (active in m-1 but not m), and resurrected (active in m, not in m-1, but active in some earlier month). Return counts per month in a reconciling table (previous active = retained + churned; active = new + retained + resurrected). Build from distinct user-month pairs and a first-active-month CTE; pandas with merge and set logic. Streak and island logic is Part 7; stay at the m-1 versus m level.
**Asked at:** search-result snippets of date-spine and churn guides (Galaxy cohort-churn glossary, a LinkedIn list of time-series SQL topics; not opened), guides and not candidate reports; analyst and data engineer screens
**Say this first (1 line):** Reduce the events to distinct (user, calendar month) pairs, compute each user's first active month, then for each month classify active users as new (first month), retained (active last month too) or resurrected (not active last month but active in some earlier month), count churned as last month's users missing from this month, and prove the two identities: previous active = retained + churned, and active = new + retained + resurrected.

**Schema and sample data:** six users over January to June 2024; nobody is active in April, which stresses the spine; user 2 has events at 23:59:59 on 31 January and 00:00:00 on 1 March (no February event). Conventions: month = calendar month of `event_ts` as stored (UTC, no conversion); a user is active in a month if they have at least one event; stay at the m-1 versus m level (streaks and islands are Part 7).
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-05 10:00:00'),(1,'2024-01-20 11:00:00'),(1,'2024-02-03 09:00:00'),(1,'2024-03-10 09:00:00'),
 (2,'2024-01-31 23:59:59'),(2,'2024-03-01 00:00:00'),(2,'2024-05-02 08:00:00'),
 (3,'2024-02-01 00:00:00'),(3,'2024-03-15 12:00:00'),
 (4,'2024-03-20 12:00:00'),(4,'2024-05-21 12:00:00'),(4,'2024-06-01 12:00:00'),
 (5,'2024-05-09 12:00:00'),
 (6,'2024-06-30 23:00:00');
```

**SQL answer:** `SQL_MAIN` in the Code block: `um` (distinct user-months), `first`, a month `spine`, `cur` (each user-month with a "was active last month" flag via `EXISTS`), `act` (new, retained, resurrected, active) and `lost` (churned, attributed to the month after their last active month).
```sql
WITH um AS (
  SELECT DISTINCT user_id, date(event_ts, 'start of month') AS m FROM events
), first AS (
  SELECT user_id, MIN(m) AS first_m FROM um GROUP BY user_id
), spine(m) AS (
  SELECT MIN(m) FROM um
  UNION ALL SELECT date(m, '+1 month') FROM spine WHERE m < (SELECT MAX(m) FROM um)
), cur AS (
  SELECT u.m, f.first_m,
         EXISTS (SELECT 1 FROM um p WHERE p.user_id = u.user_id AND p.m = date(u.m, '-1 month')) AS was_prev
  FROM um u JOIN first f ON f.user_id = u.user_id
), act AS (
  SELECT m, COUNT(*) AS active,
         SUM(CASE WHEN first_m = m THEN 1 ELSE 0 END) AS new,
         SUM(CASE WHEN first_m < m AND was_prev = 1 THEN 1 ELSE 0 END) AS retained,
         SUM(CASE WHEN first_m < m AND was_prev = 0 THEN 1 ELSE 0 END) AS resurrected
  FROM cur GROUP BY m
), lost AS (
  SELECT date(p.m, '+1 month') AS m, COUNT(*) AS churned
  FROM um p
  WHERE NOT EXISTS (SELECT 1 FROM um c WHERE c.user_id = p.user_id AND c.m = date(p.m, '+1 month'))
  GROUP BY 1
)
SELECT strftime('%Y-%m', s.m) AS month,
       COALESCE((SELECT active FROM act WHERE act.m = date(s.m, '-1 month')), 0) AS prev_active,
       COALESCE(a.new, 0) AS new, COALESCE(a.retained, 0) AS retained,
       COALESCE(l.churned, 0) AS churned, COALESCE(a.resurrected, 0) AS resurrected,
       COALESCE(a.active, 0) AS active
FROM spine s
LEFT JOIN act a ON a.m = s.m
LEFT JOIN lost l ON l.m = s.m
ORDER BY s.m
```

**pandas answer:** the same logic with merges: shift each pair forward one month to test "active last month" and backward to find users with no next month; `first_m` comes from `groupby(...).transform('min')`. A third check re-derives the counts with Python sets.
```py
um = ev.assign(m=ev["event_ts"].dt.to_period("M"))[["user_id", "m"]].drop_duplicates()
um["first_m"] = um.groupby("user_id")["m"].transform("min")
prev = um[["user_id", "m"]].assign(m=lambda x: x["m"] + 1, was_prev=True)          # shift each pair forward one month
cur = um.merge(prev, on=["user_id", "m"], how="left").fillna({"was_prev": False})
cur["kind"] = "new"
cur.loc[(cur["first_m"] < cur["m"]) & cur["was_prev"].astype(bool), "kind"] = "retained"
cur.loc[(cur["first_m"] < cur["m"]) & ~cur["was_prev"].astype(bool), "kind"] = "resurrected"
counts = cur.pivot_table(index="m", columns="kind", values="user_id", aggfunc="nunique").reindex(columns=["new", "retained", "resurrected"])
# churned: a pair (user, m) with no pair (user, m+1); attribute it to month m+1
nxt = um[["user_id", "m"]].assign(m=lambda x: x["m"] - 1, has_next=True)
lost = um[["user_id", "m"]].merge(nxt, on=["user_id", "m"], how="left")
churned = lost[lost["has_next"].isna()].assign(m=lambda x: x["m"] + 1).groupby("m")["user_id"].nunique().rename("churned")
```

**Example:** January: users 1 and 2 are new (2). February: user 1 retained, user 3 new, user 2 churned (active in January, not February). March: user 1 and user 3 retained (2), user 4 new, user 2 resurrected (first seen January, absent February, back in March): active 4. April: nobody active, so all four March users churned (4). May: user 5 new, users 2 and 4 resurrected (both were active in March, absent in April): active 3. June: user 4 retained, user 6 new, users 2 and 5 churned: active 2. Reconciliation for May: previous active 0 (April) = retained 0 + churned 0; active 3 = new 1 + retained 0 + resurrected 2.

**Code:** run with `python3 -I`.
```python
# Q33: new / retained / churned / resurrected per calendar month (UTC dates as stored; month = calendar month of event_ts)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-05 10:00:00'),(1,'2024-01-20 11:00:00'),(1,'2024-02-03 09:00:00'),(1,'2024-03-10 09:00:00'),
 (2,'2024-01-31 23:59:59'),(2,'2024-03-01 00:00:00'),(2,'2024-05-02 08:00:00'),
 (3,'2024-02-01 00:00:00'),(3,'2024-03-15 12:00:00'),
 (4,'2024-03-20 12:00:00'),(4,'2024-05-21 12:00:00'),(4,'2024-06-01 12:00:00'),
 (5,'2024-05-09 12:00:00'),
 (6,'2024-06-30 23:00:00');
"""
SQL_MAIN = """
WITH um AS (
  SELECT DISTINCT user_id, date(event_ts, 'start of month') AS m FROM events
), first AS (
  SELECT user_id, MIN(m) AS first_m FROM um GROUP BY user_id
), spine(m) AS (
  SELECT MIN(m) FROM um
  UNION ALL SELECT date(m, '+1 month') FROM spine WHERE m < (SELECT MAX(m) FROM um)
), cur AS (
  SELECT u.m, f.first_m,
         EXISTS (SELECT 1 FROM um p WHERE p.user_id = u.user_id AND p.m = date(u.m, '-1 month')) AS was_prev
  FROM um u JOIN first f ON f.user_id = u.user_id
), act AS (
  SELECT m, COUNT(*) AS active,
         SUM(CASE WHEN first_m = m THEN 1 ELSE 0 END) AS new,
         SUM(CASE WHEN first_m < m AND was_prev = 1 THEN 1 ELSE 0 END) AS retained,
         SUM(CASE WHEN first_m < m AND was_prev = 0 THEN 1 ELSE 0 END) AS resurrected
  FROM cur GROUP BY m
), lost AS (
  SELECT date(p.m, '+1 month') AS m, COUNT(*) AS churned
  FROM um p
  WHERE NOT EXISTS (SELECT 1 FROM um c WHERE c.user_id = p.user_id AND c.m = date(p.m, '+1 month'))
  GROUP BY 1
)
SELECT strftime('%Y-%m', s.m) AS month,
       COALESCE((SELECT active FROM act WHERE act.m = date(s.m, '-1 month')), 0) AS prev_active,
       COALESCE(a.new, 0) AS new, COALESCE(a.retained, 0) AS retained,
       COALESCE(l.churned, 0) AS churned, COALESCE(a.resurrected, 0) AS resurrected,
       COALESCE(a.active, 0) AS active
FROM spine s
LEFT JOIN act a ON a.m = s.m
LEFT JOIN lost l ON l.m = s.m
ORDER BY s.m
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
assert (sql_df["prev_active"] == sql_df["retained"] + sql_df["churned"]).all()
assert (sql_df["active"] == sql_df["new"] + sql_df["retained"] + sql_df["resurrected"]).all()

ev = pd.read_sql_query("SELECT * FROM events", con)
ev["event_ts"] = pd.to_datetime(ev["event_ts"])
um = ev.assign(m=ev["event_ts"].dt.to_period("M"))[["user_id", "m"]].drop_duplicates()
um["first_m"] = um.groupby("user_id")["m"].transform("min")
prev = um[["user_id", "m"]].assign(m=lambda x: x["m"] + 1, was_prev=True)          # shift each pair forward one month
cur = um.merge(prev, on=["user_id", "m"], how="left").fillna({"was_prev": False})
cur["kind"] = "new"
cur.loc[(cur["first_m"] < cur["m"]) & cur["was_prev"].astype(bool), "kind"] = "retained"
cur.loc[(cur["first_m"] < cur["m"]) & ~cur["was_prev"].astype(bool), "kind"] = "resurrected"
counts = cur.pivot_table(index="m", columns="kind", values="user_id", aggfunc="nunique").reindex(columns=["new", "retained", "resurrected"])
# churned: a pair (user, m) with no pair (user, m+1); attribute it to month m+1
nxt = um[["user_id", "m"]].assign(m=lambda x: x["m"] - 1, has_next=True)
lost = um[["user_id", "m"]].merge(nxt, on=["user_id", "m"], how="left")
churned = lost[lost["has_next"].isna()].assign(m=lambda x: x["m"] + 1).groupby("m")["user_id"].nunique().rename("churned")
spine = pd.period_range(um["m"].min(), um["m"].max(), freq="M")
pd_df = counts.join(churned, how="outer").reindex(spine).fillna(0).astype(int)
pd_df["active"] = pd_df["new"] + pd_df["retained"] + pd_df["resurrected"]
pd_df["prev_active"] = pd_df["active"].shift(1, fill_value=0)
pd_df = pd_df.rename_axis("month").reset_index()
pd_df["month"] = pd_df["month"].astype(str)
pd_df = pd_df[["month", "prev_active", "new", "retained", "churned", "resurrected", "active"]]
# compared in month order
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)

# third check: plain Python set logic per month
sets = um.groupby("m")["user_id"].agg(set)
seen = set()
for m in spine:
    c, p = sets.get(m, set()), sets.get(m - 1, set())
    row = sql_df[sql_df["month"] == str(m)].iloc[0]
    assert (len(c - seen), len(c & p), len(p - c), len((c - p) & seen)) == (row["new"], row["retained"], row["churned"], row["resurrected"])
    seen |= c
print("asserts passed: SQL == pandas merge logic == set logic; both reconciliations hold in every month")
```

**Output (my run):**
```text
  month  prev_active  new  retained  churned  resurrected  active
2024-01            0    2         0        0            0       2
2024-02            2    1         1        1            0       2
2024-03            2    1         2        0            1       4
2024-04            4    0         0        4            0       0
2024-05            0    1         0        0            2       3
2024-06            3    1         1        2            0       2
asserts passed: SQL == pandas merge logic == set logic; both reconciliations hold in every month
```

**Edge cases:**
- Empty month (April): the spine keeps it with active 0; without the spine the churn of four users would be invisible and May's two resurrected users would look like "returning after a gap" with no gap visible.
- Both identities are asserted for every month: `prev_active = retained + churned` and `active = new + retained + resurrected`. In May `prev_active` is 0 (April had no users), so nobody can be retained or churned.
- Churn is counted in the month after the user's last active month, so churn for the month after the last data month (July) is not reported; the final month's actives are not yet known to churn.
- Duplicate events in the same month: `DISTINCT` on (user, month) counts once (user 1 has two January events).
- A user active only in the latest month is new, not resurrected.
- Month boundary: user 2's 23:59:59 event on 31 January belongs to January; shifting the time zone (UTC versus IST) could move it to February and change the classification.
- A user whose events are exactly one month apart repeatedly is "retained" each time; a gap of one month flips them through "churned" then "resurrected" (user 2 in March, May).
- Definition caveat: "churned" here means absent for one calendar month; many products define churn after 30 or 90 days of inactivity, which is a different definition.

**Then explain:**
- Work with a distinct user-month table; everything is a membership test between month m-1 and month m.
- Resurrected = active in m, not active in m-1, but active in some earlier month (`first_m < m` and `was_prev = 0`). New = `first_m = m`.
- Month arithmetic on first-of-month dates with `date(m, '-1 month')` is safe, because day 1 never overflows (compare Q8).
- Hedged (not executed): PostgreSQL `date_trunc('month', event_ts)` and `generate_series` for the spine; BigQuery `DATE_TRUNC` and `GENERATE_DATE_ARRAY`; MySQL 8 uses a recursive CTE as here.

**Follow-ups:**
- "Add a rate?" retention = retained / prev_active, churn = churned / prev_active (NULLIF the denominator); Q18 has the month-over-month retention.
- "Resurrection after at least 3 months away?" That needs gap length (Part 7 territory).
- "By segment?" Add the segment to the pairs and the spine as in Q41.

**Common mistakes:**
- Calling every non-retained returning user new.
- No month spine, so empty months disappear and the identities fail.
- Counting events instead of distinct users.
- Attributing churn to the last active month instead of the first absent month (and then the identities do not reconcile).
- Treating the latest month's missing users as churned when the month is still open.

### Q34 ⭐⭐ 🔴 Active subscriptions per month from date ranges: subscriptions(sub_id, user_id, plan_price, start_date, end_date) where end_date is NULL for active subscriptions. For each month return the number of subscriptions active at month end, new, ended, and monthly recurring revenue, using a month spine and a range join (start_date <= month_end AND (end_date IS NULL OR end_date >= month_end)). Discuss inclusive versus exclusive end_date and a subscription that starts and ends in the same month, then give the pandas version with date_range and a cross merge or interval masks.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Build a month spine with a month_end for each row, join subscriptions on `start_date <= month_end AND (end_date IS NULL OR end_date >= month_end)` to get who is active at month end, count new and ended with separate range tests on the month itself, and sum plan_price over the active set for MRR.

**Schema and sample data:** six subscriptions. Sub 2 ends exactly on a month end, sub 3 starts and ends inside February, sub 4 starts on the leap day, user 2 comes back with a new subscription (sub 6). Convention: `end_date` is inclusive (the last day of service), dates are plain `YYYY-MM-DD` text, no time zone, no weeks involved.
```sql
CREATE TABLE subscriptions(sub_id INTEGER PRIMARY KEY, user_id INTEGER, plan_price INTEGER,
                           start_date TEXT, end_date TEXT);
INSERT INTO subscriptions VALUES
 (1, 1, 10, '2024-01-10', NULL),
 (2, 2, 20, '2024-01-20', '2024-03-31'),
 (3, 3, 30, '2024-02-05', '2024-02-20'),
 (4, 4, 15, '2024-02-29', NULL),
 (5, 5, 40, '2024-03-15', '2024-05-10'),
 (6, 2, 25, '2024-05-01', NULL);
```

**SQL answer:** the spine is a recursive CTE (`SQL_MAIN` in the Code block). Each measure is its own scalar subquery because the three measures use different membership rules; one join carrying all three would fan rows out and mix the rules.
```sql
WITH RECURSIVE spine(month_start) AS (
  SELECT '2024-01-01'
  UNION ALL
  SELECT date(month_start, '+1 month') FROM spine WHERE month_start < '2024-06-01'
), ms AS (
  SELECT strftime('%Y-%m', month_start) AS month,
         month_start,
         date(month_start, '+1 month', '-1 day') AS month_end
  FROM spine
)
SELECT ms.month,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.start_date <= ms.month_end
      AND (s.end_date IS NULL OR s.end_date >= ms.month_end)) AS active_at_end,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.start_date BETWEEN ms.month_start AND ms.month_end) AS new_subs,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.end_date BETWEEN ms.month_start AND ms.month_end) AS ended_subs,
  (SELECT COALESCE(SUM(s.plan_price), 0) FROM subscriptions s
    WHERE s.start_date <= ms.month_end
      AND (s.end_date IS NULL OR s.end_date >= ms.month_end)) AS mrr
FROM ms
ORDER BY ms.month
```
The exclusive-end_date variant changes one test, `s.end_date >= ms.month_end` becomes `s.end_date > ms.month_end` (`SQL_EXCL` in the code).

**pandas answer:** `date_range(..., freq="ME")` for the spine, a cross merge for the range join, boolean masks for each measure, then one `groupby`.
```py
spine = pd.DataFrame({"month_end": pd.date_range("2024-01-31", periods=6, freq="ME")})
spine["month_start"] = spine["month_end"].dt.to_period("M").dt.start_time
spine["month"] = spine["month_end"].dt.strftime("%Y-%m")
x = spine.merge(subs, how="cross")
x["active"] = (x["start_date"] <= x["month_end"]) & (x["end_date"].isna() | (x["end_date"] >= x["month_end"]))
x["new_subs"] = (x["start_date"] >= x["month_start"]) & (x["start_date"] <= x["month_end"])
x["ended_subs"] = x["end_date"].notna() & (x["end_date"] >= x["month_start"]) & (x["end_date"] <= x["month_end"])
x["mrr"] = x["plan_price"].where(x["active"], 0)
pd_df = (x.groupby("month", as_index=False)
          .agg(active_at_end=("active", "sum"), new_subs=("new_subs", "sum"),
               ended_subs=("ended_subs", "sum"), mrr=("mrr", "sum")))
```

**Example:**
- Jan (month end 01-31): sub 1 (start 01-10, open) and sub 2 (start 01-20, ends 03-31) are active, so active = 2 and MRR = 10 + 20 = 30. New = 2 (subs 1 and 2). Ended = 0.
- Feb (02-29): sub 3 started 02-05 and ended 02-20, so it is not active at month end. Active = subs 1, 2, 4 = 3, MRR = 10 + 20 + 15 = 45. New = 2 (subs 3 and 4), ended = 1 (sub 3).
- Mar (03-31): sub 5 starts 03-15. Sub 2 ends 03-31, which is inclusive, so it still counts: active = subs 1, 2, 4, 5 = 4, MRR = 85. Under an exclusive end_date sub 2 is gone at 03-31: active 3, MRR 65 (the `SQL_EXCL` output).
- May (05-31): sub 5 ended 05-10, sub 6 (user 2, 25) started 05-01: active = subs 1, 4, 6 = 3, MRR = 10 + 15 + 25 = 50.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q34: active subscriptions per month from date ranges (month spine + range join)
# Convention: end_date is INCLUSIVE (last day of service); dates are plain 'YYYY-MM-DD' text, no time zone.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE subscriptions(sub_id INTEGER PRIMARY KEY, user_id INTEGER, plan_price INTEGER,
                           start_date TEXT, end_date TEXT);
INSERT INTO subscriptions VALUES
 (1, 1, 10, '2024-01-10', NULL),
 (2, 2, 20, '2024-01-20', '2024-03-31'),
 (3, 3, 30, '2024-02-05', '2024-02-20'),
 (4, 4, 15, '2024-02-29', NULL),
 (5, 5, 40, '2024-03-15', '2024-05-10'),
 (6, 2, 25, '2024-05-01', NULL);
"""

SQL_MAIN = """
WITH RECURSIVE spine(month_start) AS (
  SELECT '2024-01-01'
  UNION ALL
  SELECT date(month_start, '+1 month') FROM spine WHERE month_start < '2024-06-01'
), ms AS (
  SELECT strftime('%Y-%m', month_start) AS month,
         month_start,
         date(month_start, '+1 month', '-1 day') AS month_end
  FROM spine
)
SELECT ms.month,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.start_date <= ms.month_end
      AND (s.end_date IS NULL OR s.end_date >= ms.month_end)) AS active_at_end,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.start_date BETWEEN ms.month_start AND ms.month_end) AS new_subs,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.end_date BETWEEN ms.month_start AND ms.month_end) AS ended_subs,
  (SELECT COALESCE(SUM(s.plan_price), 0) FROM subscriptions s
    WHERE s.start_date <= ms.month_end
      AND (s.end_date IS NULL OR s.end_date >= ms.month_end)) AS mrr
FROM ms
ORDER BY ms.month
"""

# Variant: end_date EXCLUSIVE (first day with no service): only the active test changes.
SQL_EXCL = SQL_MAIN.replace("s.end_date >= ms.month_end", "s.end_date > ms.month_end")

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
subs = pd.read_sql_query("SELECT * FROM subscriptions", con,
                         parse_dates=["start_date", "end_date"])

# --- pandas ---
spine = pd.DataFrame({"month_end": pd.date_range("2024-01-31", periods=6, freq="ME")})
spine["month_start"] = spine["month_end"].dt.to_period("M").dt.start_time
spine["month"] = spine["month_end"].dt.strftime("%Y-%m")
x = spine.merge(subs, how="cross")
x["active"] = (x["start_date"] <= x["month_end"]) & (x["end_date"].isna() | (x["end_date"] >= x["month_end"]))
x["new_subs"] = (x["start_date"] >= x["month_start"]) & (x["start_date"] <= x["month_end"])
x["ended_subs"] = x["end_date"].notna() & (x["end_date"] >= x["month_start"]) & (x["end_date"] <= x["month_end"])
x["mrr"] = x["plan_price"].where(x["active"], 0)
pd_df = (x.groupby("month", as_index=False)
          .agg(active_at_end=("active", "sum"), new_subs=("new_subs", "sum"),
               ended_subs=("ended_subs", "sum"), mrr=("mrr", "sum")))
# --- end pandas ---

sql_df = pd.read_sql_query(SQL_MAIN, con)
excl_df = pd.read_sql_query(SQL_EXCL, con)
# compare after sorting by month, ignoring dtype (SQL int64 vs pandas int64/bool sums)
pd.testing.assert_frame_equal(sql_df.sort_values("month").reset_index(drop=True),
                              pd_df.sort_values("month").reset_index(drop=True), check_dtype=False)
print("SQL (end_date inclusive):")
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")
print("\nSQL with EXCLUSIVE end_date (only active_at_end and mrr change):")
print(excl_df.to_string(index=False))
```

**Output (my run):**
```text
SQL (end_date inclusive):
  month  active_at_end  new_subs  ended_subs  mrr
2024-01              2         2           0   30
2024-02              3         2           1   45
2024-03              4         1           1   85
2024-04              3         0           0   65
2024-05              3         1           1   50
2024-06              3         0           0   50

pandas equals SQL: OK

SQL with EXCLUSIVE end_date (only active_at_end and mrr change):
  month  active_at_end  new_subs  ended_subs  mrr
2024-01              2         2           0   30
2024-02              3         2           1   45
2024-03              3         1           1   65
2024-04              3         0           0   65
2024-05              3         1           1   50
2024-06              3         0           0   50
```

**Edge cases:**
- Starts and ends in the same month (sub 3): it is counted in `new_subs` and `ended_subs` for February and never in `active_at_end`, so new minus ended does not equal the change in active when the month-end snapshot is used. Say which definition the report uses.
- End on the month-end day (sub 2): the single biggest source of off-by-one in this question. Inclusive end_date means active that day; exclusive means not. Ask which one the table uses, or read a few rows.
- `end_date IS NULL` must be tested explicitly, because `NULL >= month_end` is unknown and would drop every open subscription.
- A user with two subscriptions (user 2) is counted twice in `active_at_end` if both overlap; use `COUNT(DISTINCT user_id)` if the question is about users. `new_subs` also counts sub 6 as new although user 2 is a returning customer.
- A month with no active subscription still gets a row (zero) because the spine drives the query; `COALESCE(SUM(...), 0)` keeps MRR at 0 instead of NULL. `SUM` ignores a NULL plan_price.
- "Active at any time in the month" is a different definition (`start_date <= month_end AND (end_date IS NULL OR end_date >= month_start)`); do not mix the two in one report.
- Other engines (not executed here): the spine would come from `generate_series` in PostgreSQL or `GENERATE_DATE_ARRAY` in BigQuery instead of a recursive CTE, and `date(month_start, '+1 month', '-1 day')` becomes `LAST_DAY()` or `EOMONTH()` in some engines; see Q36.

**Then explain:**
- A range join matches a point (month end) to an interval (start to end); open-ended intervals use NULL, so the predicate must handle NULL on purpose.
- The spine is what makes empty months appear; without it a month with zero active subscriptions vanishes and any later LAG compares the wrong months (Part 5 and Q45).
- MRR here is the sum of the plan price of subscriptions active at month end; it ignores proration and mid-month changes, which is a modelling choice to state.
- pandas does the same with a cross merge (6 months x 6 subs = 36 rows here), which is fine for a toy but grows as months x subscriptions; at scale use `merge_asof`, an interval index or sort-based counting (start counts minus end counts, cumulated).

**Follow-ups:**
- How would you get monthly churn? Ended in month m divided by active at the end of month m-1 (cohort classification of new, retained, churned is Q33).
- What if the columns are timestamps? Then `end_date >= month_end` fails for an end at 14:00 on the last day; compare with a half-open `end_ts >= next_month_start` style bound (Q39, Q45).
- How do you avoid the cross merge in pandas? Count starts and ends per month with `value_counts`/`resample`, then `cumsum` the difference; that would give the active count without the 36-row product (not run here).

**Common mistakes:**
- Joining once and computing `new`, `ended` and `active` from the same joined rows, which multiplies rows.
- Forgetting `IS NULL` for open subscriptions.
- Using `BETWEEN` on timestamps for the month window.
- Building the spine from the data instead of a calendar, so quiet months disappear.

### Q35 ⭐ 🟡 Late-arriving data and event time versus processing time: events(event_id, user_id, event_ts, loaded_at). Explain why a daily report for yesterday changes tomorrow, show a query that reports by event_ts and a restated-total comparison versus the figures first published (using loaded_at <= a cut-off), and discuss lookback windows, reprocessing and how cohort retention for the latest month shifts as late rows land. Concept plus a small runnable example; no streaming tooling.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Rows arrive after the day they describe, so a report for yesterday is only a snapshot as of a load cut-off; I group by `event_ts` (not `loaded_at`), reproduce what was published with `loaded_at <= first_cutoff`, compare it with a later cut-off to see the restatement, and handle it with a lookback window that reprocesses the last few days.

**Schema and sample data:** twelve events. Events 3, 4, 7 and 8 land late (hours to days). Convention: `event_ts` and `loaded_at` are UTC text, the day is the UTC date, no week logic, and the cut-offs are fixed strings (never `now`) so the run is repeatable. Feb events 10 to 13 form a cohort of four users, March events 6, 7 and 8 are their return activity.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, loaded_at TEXT);
INSERT INTO events VALUES
 (10, 1, '2024-02-05 10:00:00', '2024-02-05 10:05:00'),
 (11, 2, '2024-02-06 11:00:00', '2024-02-06 11:05:00'),
 (12, 3, '2024-02-07 12:00:00', '2024-02-07 12:05:00'),
 (13, 4, '2024-02-08 13:00:00', '2024-02-08 13:05:00'),
 (1,  5, '2024-03-01 00:10:00', '2024-03-01 00:15:00'),
 (2,  6, '2024-03-01 10:00:00', '2024-03-01 10:05:00'),
 (3,  7, '2024-03-01 23:50:00', '2024-03-02 09:00:00'),
 (4,  8, '2024-03-01 12:00:00', '2024-03-04 08:00:00'),
 (5,  1, '2024-03-02 09:00:00', '2024-03-02 09:05:00'),
 (6,  2, '2024-03-10 09:00:00', '2024-03-10 09:05:00'),
 (7,  3, '2024-03-30 22:00:00', '2024-04-03 09:00:00'),
 (8,  4, '2024-03-31 21:00:00', '2024-04-05 09:00:00');
```

**SQL answer:** per event day, rows loaded by the first cut-off (`published`), rows loaded by the later cut-off (`restated`) and their difference (`SQL_MAIN`). `SUM(loaded_at <= :c1)` works in SQLite because a comparison is 0 or 1; other engines need `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` or `COUNT(*) FILTER (WHERE ...)` (PostgreSQL, not executed here).
```sql
SELECT date(event_ts) AS event_day,
       SUM(loaded_at <= :c1) AS published,
       SUM(loaded_at <= :c2) AS restated,
       SUM(loaded_at <= :c2) - SUM(loaded_at <= :c1) AS late_rows
FROM events
WHERE event_ts >= '2024-03-01' AND event_ts < '2024-03-03'
GROUP BY date(event_ts)
ORDER BY event_day
```
The retention-shift query (`SQL_RET`) takes the Feb-active users as the cohort and counts March activity that had been loaded by a cut-off.
```sql
WITH cohort AS (SELECT DISTINCT user_id FROM events WHERE event_ts >= '2024-02-01' AND event_ts < '2024-03-01'),
     back AS (SELECT DISTINCT user_id FROM events
              WHERE event_ts >= '2024-03-01' AND event_ts < '2024-04-01' AND loaded_at <= :cut)
SELECT COUNT(*) AS cohort_size, COUNT(b.user_id) AS retained,
       ROUND(100.0 * COUNT(b.user_id) / COUNT(*), 1) AS retention_pct
FROM cohort c LEFT JOIN back b ON b.user_id = c.user_id
```

**pandas answer:** boolean columns for "loaded by cut-off" and a `groupby` on the event day.
```py
ev = pd.read_sql_query("SELECT * FROM events", con, parse_dates=["event_ts", "loaded_at"])
win = ev[(ev["event_ts"] >= "2024-03-01") & (ev["event_ts"] < "2024-03-03")].copy()
win["event_day"] = win["event_ts"].dt.strftime("%Y-%m-%d")
win["published"] = win["loaded_at"] <= pd.Timestamp(C1)
win["restated"] = win["loaded_at"] <= pd.Timestamp(C2)
pd_df = win.groupby("event_day", as_index=False).agg(published=("published", "sum"), restated=("restated", "sum"))
pd_df["late_rows"] = pd_df["restated"] - pd_df["published"]
```

**Example:**
- Report for 2024-03-01, first published 2024-03-02 06:00:00: events 1 and 2 were loaded the same day, event 3 (event at 23:50) was loaded 03-02 09:00 and event 4 (event at 12:00) on 03-04. Published = 2. At the 03-06 cut-off all four are in, restated = 4, so the first number was 50% too low (2 late rows).
- 2024-03-02: event 5 occurred at 09:00, after the 06:00 publication, so published = 0 (a day still open) and restated = 1.
- Grouping the same rows by load date gives 2 and 2, which is the wrong axis: event 3 belongs to 03-01 but would be counted on 03-02.
- Largest arrival lags: event 8 is 4.5 days, event 7 is 3.46 days, event 4 is 2.83 days. A 3-day lookback would still miss events 7 and 8, so the window must be at least 5 days for this feed.
- Retention of the Feb cohort (users 1 to 4) in March: as of 2024-04-01 only users 1 and 2 have loaded March activity, 2 of 4 = 50.0%. As of 2024-04-10 users 3 and 4 have arrived (events 7 and 8, loaded 04-03 and 04-05): 4 of 4 = 100.0%. The latest month looked like a retention collapse that was a loading delay.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q35: late-arriving data, event time vs processing time (loaded_at)
# Convention: event_ts and loaded_at are UTC text 'YYYY-MM-DD HH:MM:SS'; the "day" is the UTC date; fixed cut-offs, never now().
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, loaded_at TEXT);
INSERT INTO events VALUES
 (10, 1, '2024-02-05 10:00:00', '2024-02-05 10:05:00'),
 (11, 2, '2024-02-06 11:00:00', '2024-02-06 11:05:00'),
 (12, 3, '2024-02-07 12:00:00', '2024-02-07 12:05:00'),
 (13, 4, '2024-02-08 13:00:00', '2024-02-08 13:05:00'),
 (1,  5, '2024-03-01 00:10:00', '2024-03-01 00:15:00'),
 (2,  6, '2024-03-01 10:00:00', '2024-03-01 10:05:00'),
 (3,  7, '2024-03-01 23:50:00', '2024-03-02 09:00:00'),
 (4,  8, '2024-03-01 12:00:00', '2024-03-04 08:00:00'),
 (5,  1, '2024-03-02 09:00:00', '2024-03-02 09:05:00'),
 (6,  2, '2024-03-10 09:00:00', '2024-03-10 09:05:00'),
 (7,  3, '2024-03-30 22:00:00', '2024-04-03 09:00:00'),
 (8,  4, '2024-03-31 21:00:00', '2024-04-05 09:00:00');
"""
C1 = "2024-03-02 06:00:00"   # when the report for 2024-03-01 was first published
C2 = "2024-03-06 00:00:00"   # the restatement cut-off

SQL_MAIN = """
SELECT date(event_ts) AS event_day,
       SUM(loaded_at <= :c1) AS published,
       SUM(loaded_at <= :c2) AS restated,
       SUM(loaded_at <= :c2) - SUM(loaded_at <= :c1) AS late_rows
FROM events
WHERE event_ts >= '2024-03-01' AND event_ts < '2024-03-03'
GROUP BY date(event_ts)
ORDER BY event_day
"""
SQL_BY_LOAD = """
SELECT date(loaded_at) AS load_day, COUNT(*) AS n
FROM events WHERE loaded_at >= '2024-03-01' AND loaded_at < '2024-03-03'
GROUP BY date(loaded_at) ORDER BY load_day
"""
SQL_LAG = """
SELECT event_id, ROUND(julianday(loaded_at) - julianday(event_ts), 2) AS lag_days
FROM events ORDER BY lag_days DESC, event_id LIMIT 3
"""
# Feb-active users (the cohort); retained = any March event LOADED by the cut-off
SQL_RET = """
WITH cohort AS (SELECT DISTINCT user_id FROM events WHERE event_ts >= '2024-02-01' AND event_ts < '2024-03-01'),
     back AS (SELECT DISTINCT user_id FROM events
              WHERE event_ts >= '2024-03-01' AND event_ts < '2024-04-01' AND loaded_at <= :cut)
SELECT COUNT(*) AS cohort_size, COUNT(b.user_id) AS retained,
       ROUND(100.0 * COUNT(b.user_id) / COUNT(*), 1) AS retention_pct
FROM cohort c LEFT JOIN back b ON b.user_id = c.user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"c1": C1, "c2": C2})

# --- pandas ---
ev = pd.read_sql_query("SELECT * FROM events", con, parse_dates=["event_ts", "loaded_at"])
win = ev[(ev["event_ts"] >= "2024-03-01") & (ev["event_ts"] < "2024-03-03")].copy()
win["event_day"] = win["event_ts"].dt.strftime("%Y-%m-%d")
win["published"] = win["loaded_at"] <= pd.Timestamp(C1)
win["restated"] = win["loaded_at"] <= pd.Timestamp(C2)
pd_df = win.groupby("event_day", as_index=False).agg(published=("published", "sum"), restated=("restated", "sum"))
pd_df["late_rows"] = pd_df["restated"] - pd_df["published"]
# --- end pandas ---

pd.testing.assert_frame_equal(sql_df.sort_values("event_day").reset_index(drop=True),
                              pd_df.sort_values("event_day").reset_index(drop=True), check_dtype=False)
print("report by event_ts, first published at", C1, "vs restated at", C2)
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")
print("\nsame two days grouped by loaded_at date (wrong axis):")
print(pd.read_sql_query(SQL_BY_LOAD, con).to_string(index=False))
print("\nlargest arrival lags (days):")
print(pd.read_sql_query(SQL_LAG, con).to_string(index=False))
for cut in ("2024-04-01 00:00:00", "2024-04-10 00:00:00"):
    r = pd.read_sql_query(SQL_RET, con, params={"cut": cut})
    print("\nMarch retention of the Feb cohort as of", cut)
    print(r.to_string(index=False))
    # pandas cross-check
    feb = set(ev[(ev.event_ts >= "2024-02-01") & (ev.event_ts < "2024-03-01")].user_id)
    mar = set(ev[(ev.event_ts >= "2024-03-01") & (ev.event_ts < "2024-04-01") & (ev.loaded_at <= pd.Timestamp(cut))].user_id)
    assert (len(feb), len(feb & mar)) == (int(r.cohort_size[0]), int(r.retained[0]))
```

**Output (my run):**
```text
report by event_ts, first published at 2024-03-02 06:00:00 vs restated at 2024-03-06 00:00:00
 event_day  published  restated  late_rows
2024-03-01          2         4          2
2024-03-02          0         1          1

pandas equals SQL: OK

same two days grouped by loaded_at date (wrong axis):
  load_day  n
2024-03-01  2
2024-03-02  2

largest arrival lags (days):
 event_id  lag_days
        8      4.50
        7      3.46
        4      2.83

March retention of the Feb cohort as of 2024-04-01 00:00:00
 cohort_size  retained  retention_pct
           4         2           50.0

March retention of the Feb cohort as of 2024-04-10 00:00:00
 cohort_size  retained  retention_pct
           4         4          100.0
```

**Edge cases:**
- `loaded_at` NULL (not yet loaded): `NULL <= cut-off` is unknown, so the row is excluded, which is the right as-of behaviour.
- Duplicates from retries or replays: dedupe on `event_id` before counting, and keep the first `loaded_at`; if reprocessing overwrites `loaded_at`, you can no longer reproduce an old cut-off.
- Events whose `event_ts` is in the future (device clock skew) or before the load window: decide whether they are dropped or flagged.
- A restated figure can also go down (events deleted or deduplicated later), so do not assume only increases.
- Time zone: if event_ts is device local time and loaded_at is server UTC, lag arithmetic is wrong by the offset.

**Then explain:**
- Event time is when the thing happened; processing (load) time is when the warehouse knew about it. Daily jobs aggregate what is loaded, so day D is incomplete when first computed and grows afterwards.
- Keep the published numbers (a snapshot table with an `as_of` column) so a restatement can be shown; the `loaded_at <= cut-off` filter reproduces the old view from raw data.
- Lookback and reprocessing: each run recomputes the last N days from raw data and overwrites those days (idempotent, same result when re-run); N comes from the lag distribution (a high percentile of `loaded_at - event_ts`), and days older than N are called final.
- Cohort retention: the cohort (denominator) is fixed by earlier months; the numerator for the latest month keeps growing as late rows land, so retention for immature or recent periods is flagged provisional, or computed only for periods older than the lookback.
- No streaming tooling is needed to reason about this; it is a batch-reporting concern.

**Follow-ups:**
- How do you tell stakeholders a number changed? Show the first-published and restated figures side by side with the cut-offs, and publish the lookback policy.
- Should you report by loaded_at instead? It never changes, but it answers "what arrived today", not "what happened that day"; use it for pipeline monitoring, not business reporting.
- What about the "as of" timestamp in code? Pass it as a parameter, as here, never `now()`, so a past report can be re-run.

**Common mistakes:**
- Grouping by `loaded_at` and calling it the daily number.
- Comparing the latest, still-landing month with older complete months.
- Using the current time inside the query, so reruns give different answers.
- Treating the first published number as the truth, or silently overwriting it without a record.

### Q36 ⭐ 🟡 Dialect map for date functions (hedge everything not run on SQLite 3.45): DATE_TRUNC, EXTRACT, DATE_PART, DATEDIFF argument orders, DATE_ADD and INTERVAL, generate_series, AGE in PostgreSQL, DATE_FORMAT and TIMESTAMPDIFF in MySQL, DATE_TRUNC with TIMESTAMP_TRUNC and DATE_DIFF in BigQuery, DATEADD and DATEDIFF in Snowflake and SQL Server. Pair each with the SQLite expression that is run (strftime, date modifiers, julianday), stress that the sign and order of DATEDIFF arguments differ between engines, and label every non-SQLite line 'not executed'.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** The functions differ per engine, and the one that bites is DATEDIFF, because the argument order and the sign change between engines; in SQLite I use `julianday(b) - julianday(a)` for days, `strftime` for extraction and formatting, and date modifiers for truncation and addition, and I label every non-SQLite line below as not executed.

**Schema and sample data:** no table is needed, two fixed dates stand in for columns: A = `2024-01-31` and B = `2024-03-15` (2024 is a leap year). Convention: plain dates, no time zone, weeks start on Monday where a week appears.

**SQL answer:** these are the SQLite expressions that ran (the list `SQLITE` in the Code block), each paired with the engine function it stands in for. Output of the run is below.
| Concept (engine function it stands in for) | SQLite expression (run) | Result |
|---|---|---|
| truncate to month (DATE_TRUNC) | `date('2024-03-15', 'start of month')` | `2024-03-01` |
| truncate to Monday week | `date('2024-03-15', '-6 days', 'weekday 1')` | `2024-03-11` |
| EXTRACT(year) | `CAST(strftime('%Y', '2024-03-15') AS INTEGER)` | `2024` |
| EXTRACT(month) | `CAST(strftime('%m', '2024-03-15') AS INTEGER)` | `3` |
| day of week, Mon=1..Sun=7 (ISODOW) | `CAST(strftime('%u', '2024-03-15') AS INTEGER)` | `5` |
| format as YYYY-MM (DATE_FORMAT) | `strftime('%Y-%m', '2024-03-15')` | `2024-03` |
| days between: B - A (DATEDIFF) | `CAST(julianday('2024-03-15') - julianday('2024-01-31') AS INTEGER)` | `44` |
| days between: A - B (sign flipped) | `CAST(julianday('2024-01-31') - julianday('2024-03-15') AS INTEGER)` | `-44` |
| add one month (DATE_ADD/INTERVAL) | `date('2024-01-31', '+1 month')` | `2024-03-02` |
| end of month (LAST_DAY/EOMONTH) | `date('2024-03-15', 'start of month', '+1 month', '-1 day')` | `2024-03-31` |
| elapsed whole months A to B | `(CAST(strftime('%Y','2024-03-15') AS INT)-CAST(strftime('%Y','2024-01-31') AS INT))*12 + CAST(strftime('%m','2024-03-15') AS INT)-CAST(strftime('%m','2024-01-31') AS INT) - (strftime('%d','2024-03-15') < strftime('%d','2024-01-31'))` | `1` |
| month boundaries crossed A to B | `(CAST(strftime('%Y','2024-03-15') AS INT)-CAST(strftime('%Y','2024-01-31') AS INT))*12 + CAST(strftime('%m','2024-03-15') AS INT)-CAST(strftime('%m','2024-01-31') AS INT)` | `2` |

Dialect lines from memory, **not executed here** (I did not run any of these engines; check each against the vendor documentation):
- PostgreSQL: `DATE_TRUNC('month', ts)`; `EXTRACT(YEAR FROM ts)` and `DATE_PART('year', ts)`; `date_b - date_a` gives integer days (so B - A is positive); `AGE(b, a)` returns an interval in years, months, days; `ts + INTERVAL '1 month'`; `generate_series(start, stop, INTERVAL '1 day')`; `to_char(ts, 'YYYY-MM')`.
- MySQL: `DATE_FORMAT(d, '%Y-%m')`; `DATEDIFF(b, a)` is `b - a` in days (later date first, opposite to SQL Server); `TIMESTAMPDIFF(MONTH, a, b)` is `b - a` in the unit, earlier date first, whole units elapsed; `DATE_ADD(d, INTERVAL 1 MONTH)`; `EXTRACT(YEAR FROM d)`; `LAST_DAY(d)`; no `DATE_TRUNC` as far as I recall; a series needs a recursive CTE (MySQL 8).
- BigQuery: `DATE_TRUNC(d, MONTH)` for DATE and `TIMESTAMP_TRUNC(ts, MONTH)` for TIMESTAMP; `DATE_DIFF(b, a, DAY)` is `b - a` (later date first); `DATE_ADD(d, INTERVAL 1 MONTH)`; `EXTRACT(YEAR FROM d)`; `GENERATE_DATE_ARRAY(start, end, INTERVAL 1 DAY)` with `UNNEST`; `FORMAT_DATE('%Y-%m', d)`.
- Snowflake: `DATEDIFF(day, a, b)` is `b - a` (unit first, earlier date first); `DATEADD(month, 1, d)`; `DATE_TRUNC('month', d)`; I believe month and year differences count calendar boundaries crossed.
- SQL Server: `DATEDIFF(day, a, b)` is `b - a`, and it counts date-part boundaries crossed, so `DATEDIFF(month, '2024-01-31', '2024-02-01')` is 1; `DATEADD(month, 1, d)`; `EOMONTH(d)`; `DATETRUNC` exists only from SQL Server 2022 as far as I recall.
- Week start differs and must be stated: PostgreSQL `DATE_TRUNC('week', ...)` starts Monday; BigQuery `DATE_TRUNC(d, WEEK)` starts Sunday unless `WEEK(MONDAY)` is given; MySQL `WEEK()` takes a mode argument; Snowflake depends on a session parameter. All from memory, not executed.

**pandas answer:** the same quantities, which agree with SQLite on every row that can be compared (assert in the code). pandas has no DATEDIFF: subtract Timestamps for days, subtract Periods for calendar months.
```py
a, b = pd.Timestamp(A), pd.Timestamp(B)
pd_vals = {
 "truncate to month (DATE_TRUNC)": str(b.to_period("M").start_time.date()),
 "truncate to Monday week": str((b - pd.Timedelta(days=b.weekday())).date()),
 "EXTRACT(year)": b.year,
 "EXTRACT(month)": b.month,
 "day of week, Mon=1..Sun=7 (ISODOW)": b.isoweekday(),
 "format as YYYY-MM (DATE_FORMAT)": b.strftime("%Y-%m"),
 "days between: B - A (DATEDIFF)": (b - a).days,
 "days between: A - B (sign flipped)": (a - b).days,
 "add one month (DATE_ADD/INTERVAL)": "n/a (pandas clips instead, see below)",
 "end of month (LAST_DAY/EOMONTH)": str((b + pd.offsets.MonthEnd(0)).date()),
 "elapsed whole months A to B": (b.to_period("M") - a.to_period("M")).n - (b.day < a.day),
 "month boundaries crossed A to B": (b.to_period("M") - a.to_period("M")).n,
}
pd_series = [str(d.date()) for d in pd.date_range(A, periods=4, freq="D")]
```

**Example:** A = 2024-01-31, B = 2024-03-15.
- Days: 2024-01-31 to 2024-03-01 is 30 days (February has 29), plus 14 more to March 15 is 44. Swapping the operands gives -44: the same sign trap as `DATEDIFF` argument order.
- Month boundaries crossed: January to March is 2 (this is what SQL Server style `DATEDIFF(month, ...)` counts). Whole months elapsed: 2024-01-31 plus 1 month is 2024-02-29 (clipped), plus 2 months is 2024-03-31, which is after March 15, so 1.
- Truncations: month start 2024-03-01, Monday of the week 2024-03-11 (March 15 is a Friday, `%u` = 5), end of month 2024-03-31.
- Add one month to 2024-01-31: SQLite gives 2024-03-02 (overflow), pandas `DateOffset(months=1)` gives 2024-02-29 (clip).

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q36: dialect map for date functions. ONLY the SQLite 3.45.1 and pandas 3.x lines below are executed.
# Convention: plain dates, no time zone; a week starts on Monday where a week matters.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
A, B = "2024-01-31", "2024-03-15"      # fixed example dates, never today

# (concept, SQLite expression that is run)
SQLITE = [
 ("truncate to month (DATE_TRUNC)",      f"date('{B}', 'start of month')"),
 ("truncate to Monday week",             f"date('{B}', '-6 days', 'weekday 1')"),
 ("EXTRACT(year)",                       f"CAST(strftime('%Y', '{B}') AS INTEGER)"),
 ("EXTRACT(month)",                      f"CAST(strftime('%m', '{B}') AS INTEGER)"),
 ("day of week, Mon=1..Sun=7 (ISODOW)",  f"CAST(strftime('%u', '{B}') AS INTEGER)"),
 ("format as YYYY-MM (DATE_FORMAT)",     f"strftime('%Y-%m', '{B}')"),
 ("days between: B - A (DATEDIFF)",      f"CAST(julianday('{B}') - julianday('{A}') AS INTEGER)"),
 ("days between: A - B (sign flipped)",  f"CAST(julianday('{A}') - julianday('{B}') AS INTEGER)"),
 ("add one month (DATE_ADD/INTERVAL)",   f"date('{A}', '+1 month')"),
 ("end of month (LAST_DAY/EOMONTH)",     f"date('{B}', 'start of month', '+1 month', '-1 day')"),
 ("elapsed whole months A to B",         f"(CAST(strftime('%Y','{B}') AS INT)-CAST(strftime('%Y','{A}') AS INT))*12"
                                         f" + CAST(strftime('%m','{B}') AS INT)-CAST(strftime('%m','{A}') AS INT)"
                                         f" - (strftime('%d','{B}') < strftime('%d','{A}'))"),
 ("month boundaries crossed A to B",     f"(CAST(strftime('%Y','{B}') AS INT)-CAST(strftime('%Y','{A}') AS INT))*12"
                                         f" + CAST(strftime('%m','{B}') AS INT)-CAST(strftime('%m','{A}') AS INT)"),
]
res = {c: con.execute("SELECT " + e).fetchone()[0] for c, e in SQLITE}
for c, v in res.items():
    print(f"{c:38s} {v}")

# generate_series emulation: recursive CTE (standard SQL, runs on SQLite)
SQL_SERIES = """
WITH RECURSIVE s(d) AS (SELECT '2024-01-31' UNION ALL SELECT date(d, '+1 day') FROM s WHERE d < '2024-02-03')
SELECT d FROM s
"""
series = [r[0] for r in con.execute(SQL_SERIES)]
print("\nrecursive-CTE series:", series)

# --- pandas ---
a, b = pd.Timestamp(A), pd.Timestamp(B)
pd_vals = {
 "truncate to month (DATE_TRUNC)": str(b.to_period("M").start_time.date()),
 "truncate to Monday week": str((b - pd.Timedelta(days=b.weekday())).date()),
 "EXTRACT(year)": b.year,
 "EXTRACT(month)": b.month,
 "day of week, Mon=1..Sun=7 (ISODOW)": b.isoweekday(),
 "format as YYYY-MM (DATE_FORMAT)": b.strftime("%Y-%m"),
 "days between: B - A (DATEDIFF)": (b - a).days,
 "days between: A - B (sign flipped)": (a - b).days,
 "add one month (DATE_ADD/INTERVAL)": "n/a (pandas clips instead, see below)",
 "end of month (LAST_DAY/EOMONTH)": str((b + pd.offsets.MonthEnd(0)).date()),
 "elapsed whole months A to B": (b.to_period("M") - a.to_period("M")).n - (b.day < a.day),
 "month boundaries crossed A to B": (b.to_period("M") - a.to_period("M")).n,
}
pd_series = [str(d.date()) for d in pd.date_range(A, periods=4, freq="D")]
# --- end pandas ---
for c, v in pd_vals.items():
    if not str(v).startswith("n/a"):
        assert res[c] == v, (c, res[c], v)
assert series == pd_series
print("\npandas equals SQLite on every comparable row: OK")

# the add-one-month difference between engines (SQLite overflows, pandas clips)
print("\nSQLite date('2024-01-31','+1 month') =", con.execute("SELECT date('2024-01-31','+1 month')").fetchone()[0])
print("SQLite date('2023-01-31','+1 month') =", con.execute("SELECT date('2023-01-31','+1 month')").fetchone()[0])
print("pandas Timestamp('2024-01-31') + DateOffset(months=1) =", (a + pd.DateOffset(months=1)).date())
print("pandas Timestamp('2023-01-31') + DateOffset(months=1) =", (pd.Timestamp("2023-01-31") + pd.DateOffset(months=1)).date())
print("SQLite 3.45.1 'end of month' modifier:", con.execute("SELECT date('2024-03-15','end of month')").fetchone()[0], "(NULL = not supported here)")
print("SQLite 3.45.1 strftime('%V'):", con.execute("SELECT strftime('%V','2024-03-15')").fetchone()[0], "(NULL = not supported here)")

# pandas extras from the hedge list
s = pd.Series(pd.to_datetime(["2024-03-15"]))
try:
    s.dt.floor("MS")
except Exception as e:
    print("\ndt.floor('MS') ->", type(e).__name__ + ":", e)
p = s.dt.to_period("Q-MAR")
print("to_period('Q-MAR'):", p.iloc[0], "| qyear:", p.dt.qyear.iloc[0], "| quarter:", p.dt.quarter.iloc[0])
print("np.busday_count('2024-01-01','2024-01-15') =", np.busday_count("2024-01-01", "2024-01-15"), "(end excluded, Mon-Fri)")
print("np.busday_count with holidays=['2024-01-02'] =", np.busday_count("2024-01-01", "2024-01-15", holidays=["2024-01-02"]))
bd = pd.bdate_range("2024-01-01", "2024-01-12", freq="C", holidays=["2024-01-02"])
print("bdate_range freq='C' with holiday:", [str(d.date()) for d in bd])
```

**Output (my run):**
```text
truncate to month (DATE_TRUNC)         2024-03-01
truncate to Monday week                2024-03-11
EXTRACT(year)                          2024
EXTRACT(month)                         3
day of week, Mon=1..Sun=7 (ISODOW)     5
format as YYYY-MM (DATE_FORMAT)        2024-03
days between: B - A (DATEDIFF)         44
days between: A - B (sign flipped)     -44
add one month (DATE_ADD/INTERVAL)      2024-03-02
end of month (LAST_DAY/EOMONTH)        2024-03-31
elapsed whole months A to B            1
month boundaries crossed A to B        2

recursive-CTE series: ['2024-01-31', '2024-02-01', '2024-02-02', '2024-02-03']

pandas equals SQLite on every comparable row: OK

SQLite date('2024-01-31','+1 month') = 2024-03-02
SQLite date('2023-01-31','+1 month') = 2023-03-03
pandas Timestamp('2024-01-31') + DateOffset(months=1) = 2024-02-29
pandas Timestamp('2023-01-31') + DateOffset(months=1) = 2023-02-28
SQLite 3.45.1 'end of month' modifier: None (NULL = not supported here)
SQLite 3.45.1 strftime('%V'): None (NULL = not supported here)

dt.floor('MS') -> ValueError: <MonthBegin> is a non-fixed frequency
to_period('Q-MAR'): 2024Q4 | qyear: 2024 | quarter: 4
np.busday_count('2024-01-01','2024-01-15') = 10 (end excluded, Mon-Fri)
np.busday_count with holidays=['2024-01-02'] = 9
bdate_range freq='C' with holiday: ['2024-01-01', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-08', '2024-01-09', '2024-01-10', '2024-01-11', '2024-01-12']
```

**Edge cases:**
- Month arithmetic: SQLite's `+1 month` overflows (`2023-01-31` gives `2023-03-03`), pandas clips to month end, and the engines above are said to clip as well (not executed). The result of "add a month" on day 29 to 31 is engine dependent.
- `strftime('%V')`, `%G`, `%U` return NULL on SQLite 3.45.1 (shown in the output), and the `end of month`, `floor` and negative `weekday` modifiers also return NULL here; they exist only in newer SQLite versions according to its documentation, so use `start of month` arithmetic and the `weekday 1` trick shown above.
- Timestamps versus dates: `julianday` differences are fractional days; cast or `ROUND` before comparing.
- NULL dates give NULL results everywhere; `DATEDIFF` of a NULL is NULL.
- In pandas, `dt.floor('MS')` fails (non-fixed frequency); use `dt.to_period('M').dt.start_time`.
- Fiscal quarters: `to_period('Q-MAR')` puts 2024-03-15 in fiscal quarter `2024Q4` with `qyear` 2024; fiscal year labelling and where the quarter number restarts is a policy choice to confirm.

**Then explain:**
- Truncate and extract: `DATE_TRUNC` is `date(x, 'start of month')` or `strftime`; `EXTRACT` is `CAST(strftime(...) AS INTEGER)`.
- Differences: SQLite has no `DATEDIFF`; days are a `julianday` subtraction. Months need a rule: boundaries crossed (SQL Server / Snowflake style) or whole months elapsed (MySQL `TIMESTAMPDIFF` style). They disagree (2 versus 1 here), so name the one you mean.
- Series: a recursive CTE is the portable spine; `generate_series` and `GENERATE_DATE_ARRAY` are shortcuts in other engines.
- Every dialect fact outside SQLite on this page comes from memory and is not executed.

**Follow-ups:**
- Why did your DATEDIFF give a negative number? The argument order is engine specific: MySQL and BigQuery take the later date first, SQL Server and Snowflake take the unit and then the earlier date first, PostgreSQL subtracts dates with `-`.
- How do you do business days? In pandas `np.busday_count('2024-01-01', '2024-01-15')` is 10 (Monday to Friday, end excluded) and 9 with `holidays=['2024-01-02']`; `pd.bdate_range(..., freq='C', holidays=[...])` skips the holiday (both ran).
- Does SQLite support the ISO week? Not via `%V` in 3.45.1; see Q43.

**Common mistakes:**
- Assuming `DATEDIFF(a, b)` means the same in every engine.
- Using `DATEDIFF(month, ...)` boundary counting as "months of tenure".
- Writing `date + 30 days` for "next month".
- Assuming SQLite honours functions from the newer docs (`%V`, `end of month`) on an older build.

### Q37 ⭐ 🟡 Unix timestamps, milliseconds and subseconds: events(event_id, event_ms) stores epoch milliseconds from an app. Show datetime(event_ms / 1000, 'unixepoch') versus the bug of passing milliseconds as seconds (year about 56000, NULL or nonsense), unixepoch(), the 'auto' modifier and its first-63-days-of-1970 caveat, the subsec modifier and %f, and timediff() (text result, calendar-style). pandas: pd.to_datetime(unit='ms'), the pandas 3 default time unit (us for strings), and float precision loss.
**Asked at:** SQLite date and time functions documentation (lang_datefunc, opened), vendor documentation and not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Divide epoch milliseconds by 1000 before the `'unixepoch'` modifier (use `/ 1000.0` with `'subsec'` to keep the milliseconds), because passing milliseconds as seconds means a year near 55,800, which SQLite 3.45.1 returns as NULL for current dates, and a nonsense but valid date for small values.

**Schema and sample data:** four events. Event 1 is 2023-11-14 22:13:20.123 UTC, events 2 and 3 straddle 2024-01-01 by 999 ms, event 4 is 10 days after the epoch. Convention: epoch values are UTC, no time-zone conversion, no weeks.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, event_ms INTEGER);
INSERT INTO events VALUES (1, 1700000000123), (2, 1704067200000), (3, 1704067200999), (4, 864000000);
```

**SQL answer:** integer division gives whole seconds, `/ 1000.0` plus `'subsec'` keeps milliseconds, and the last column is the bug (`SQL_MAIN`).
```sql
SELECT event_id,
       datetime(event_ms / 1000, 'unixepoch')               AS ts_seconds,
       datetime(event_ms / 1000.0, 'unixepoch', 'subsec')    AS ts_millis,
       datetime(event_ms, 'unixepoch')                       AS bug_ms_as_seconds
FROM events ORDER BY event_id
```
The other functions are probed one line each in the Code block (`unixepoch()`, `strftime('%s')`, `%f`, the `'auto'` modifier, `subsec`, `timediff`).

**pandas answer:** `pd.to_datetime(..., unit="ms")`, then format.
```py
ev = pd.read_sql_query("SELECT * FROM events ORDER BY event_id", con)
ts = pd.to_datetime(ev["event_ms"], unit="ms")
pd_df = pd.DataFrame({
    "event_id": ev["event_id"],
    "ts_seconds": ts.dt.strftime("%Y-%m-%d %H:%M:%S"),
    "ts_millis": ts.dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3],
})
```

**Example:**
- Event 1: 1700000000123 / 1000 = 1700000000 s, which is 2023-11-14 22:13:20; the remaining 123 ms survive only with `subsec`, giving `...22:13:20.123`.
- Event 3: 1704067200999 is 2024-01-01 00:00:00.999; integer seconds show `00:00:00`, the same as event 2, which is why dropping the milliseconds can merge distinct moments.
- Bug: `datetime(1700000000123, 'unixepoch')` treats the number as seconds, about 1.7e12 s, roughly year 55,840; SQLite returns NULL for events 1 to 3. Event 4 (864000000 ms) read as seconds gives 1997-05-19: valid-looking and wrong, the dangerous case.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q37: epoch milliseconds, unixepoch(), 'auto', subsec, timediff; pandas unit='ms'
# Convention: epoch values are UTC; no time-zone conversion anywhere in this block.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, event_ms INTEGER);
INSERT INTO events VALUES (1, 1700000000123), (2, 1704067200000), (3, 1704067200999), (4, 864000000);
"""
SQL_MAIN = """
SELECT event_id,
       datetime(event_ms / 1000, 'unixepoch')               AS ts_seconds,
       datetime(event_ms / 1000.0, 'unixepoch', 'subsec')    AS ts_millis,
       datetime(event_ms, 'unixepoch')                       AS bug_ms_as_seconds
FROM events ORDER BY event_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

# --- pandas ---
ev = pd.read_sql_query("SELECT * FROM events ORDER BY event_id", con)
ts = pd.to_datetime(ev["event_ms"], unit="ms")
pd_df = pd.DataFrame({
    "event_id": ev["event_id"],
    "ts_seconds": ts.dt.strftime("%Y-%m-%d %H:%M:%S"),
    "ts_millis": ts.dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3],
})
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df[["event_id", "ts_seconds", "ts_millis"]].sort_values("event_id").reset_index(drop=True),
                              pd_df.sort_values("event_id").reset_index(drop=True), check_dtype=False)
print("\npandas equals SQL (event_id, ts_seconds, ts_millis): OK; dtype of pd.to_datetime(unit='ms'):", ts.dtype)

# the arithmetic behind the bug: 1.7e12 seconds is about this many years after 1970
print("\nmilliseconds read as seconds = year about", round(1700000000123 / 31556952 + 1970))
for label, sql in [
    ("unixepoch(ts text)", "SELECT unixepoch('2024-01-01 00:00:00')"),
    ("unixepoch with subsec", "SELECT unixepoch('2024-01-01 00:00:00.500', 'subsec')"),
    ("unixepoch, no subsec (integer)", "SELECT unixepoch('2024-01-01 00:00:00.500')"),
    ("strftime('%s')", "SELECT strftime('%s', '2024-01-01 00:00:00')"),
    ("strftime('%f') SS.SSS", "SELECT strftime('%f', 1700000000.123, 'unixepoch')"),
    ("auto, a real unix time 1704067200", "SELECT datetime(1704067200, 'auto')"),
    ("auto, 864000 s (day 10 of 1970)", "SELECT datetime(864000, 'auto')"),
    ("unixepoch, 864000 s", "SELECT datetime(864000, 'unixepoch')"),
    ("auto, 8640000 s (day 100 of 1970)", "SELECT datetime(8640000, 'auto')"),
    ("auto, ms value 1704067200000", "SELECT datetime(1704067200000, 'auto')"),
    ("timediff later, earlier", "SELECT timediff('2024-03-01 12:00:00', '2024-01-31 00:00:00')"),
    ("timediff earlier, later", "SELECT timediff('2024-01-31 00:00:00', '2024-03-01 12:00:00')"),
    ("julianday diff in days", "SELECT julianday('2024-03-01 12:00:00') - julianday('2024-01-31 00:00:00')"),
]:
    print(f"{label:36s}", con.execute(sql).fetchone()[0])

# ms resolution through subsec vs float arithmetic
f = con.execute("SELECT event_ms / 1000.0 FROM events WHERE event_id = 3").fetchone()[0]
print("\n1704067200999 / 1000.0 =", repr(f), "| back to ms:", f * 1000)

# pandas: units and precision
print("\nto_datetime(strings) dtype:", pd.to_datetime(["2024-01-01 00:00:00.123456"]).dtype)
print("to_datetime(string with 9 fractional digits) dtype:", pd.to_datetime(["2024-01-01 00:00:00.123456789"]).dtype)
print("Timestamp('2024-01-01').unit:", pd.Timestamp("2024-01-01").unit)
print("to_datetime(ms int):", pd.to_datetime(1700000000123, unit="ms"), "| dtype:", pd.to_datetime([1700000000123], unit="ms").dtype)
try:
    print(pd.to_datetime(1700000000123, unit="s"))
except Exception as e:
    print("ms read as seconds in pandas ->", type(e).__name__ + ":", str(e)[:70])
ns = 1700000000123456789
print("ns as int:", pd.to_datetime(ns, unit="ns"), "| through float64:", pd.to_datetime(float(ns), unit="ns"))
print("float seconds 1700000000.123456:", pd.to_datetime(1700000000.123456, unit="s"))
print("int(float(ns)) =", int(float(ns)), "vs", ns)
```

**Output (my run):**
```text
 event_id          ts_seconds               ts_millis   bug_ms_as_seconds
        1 2023-11-14 22:13:20 2023-11-14 22:13:20.123                 NaN
        2 2024-01-01 00:00:00 2024-01-01 00:00:00.000                 NaN
        3 2024-01-01 00:00:00 2024-01-01 00:00:00.999                 NaN
        4 1970-01-11 00:00:00 1970-01-11 00:00:00.000 1997-05-19 00:00:00

pandas equals SQL (event_id, ts_seconds, ts_millis): OK; dtype of pd.to_datetime(unit='ms'): datetime64[ms]

milliseconds read as seconds = year about 55841
unixepoch(ts text)                   1704067200
unixepoch with subsec                1704067200.5
unixepoch, no subsec (integer)       1704067200
strftime('%s')                       1704067200
strftime('%f') SS.SSS                20.123
auto, a real unix time 1704067200    2024-01-01 00:00:00
auto, 864000 s (day 10 of 1970)      -2347-06-13 12:00:00
unixepoch, 864000 s                  1970-01-11 00:00:00
auto, 8640000 s (day 100 of 1970)    1970-04-11 00:00:00
auto, ms value 1704067200000         None
timediff later, earlier              +0000-00-30 12:00:00.000
timediff earlier, later              -0000-01-01 12:00:00.000
julianday diff in days               30.5

1704067200999 / 1000.0 = 1704067200.999 | back to ms: 1704067200999.0

to_datetime(strings) dtype: datetime64[us]
to_datetime(string with 9 fractional digits) dtype: datetime64[ns]
Timestamp('2024-01-01').unit: us
to_datetime(ms int): 2023-11-14 22:13:20.123000 | dtype: datetime64[ms]
55840-11-08 22:15:23
ns as int: 2023-11-14 22:13:20.123456789 | through float64: 2023-11-14 22:13:20.123456768
float seconds 1700000000.123456: 2023-11-14 22:13:20.123456001
int(float(ns)) = 1700000000123456768 vs 1700000000123456789
```

**Edge cases:**
- `'auto'` (a newer modifier, available in this 3.45.1): numbers are read as Julian day numbers if they are in the range roughly 0 to 5,373,484.5, otherwise as unix seconds. That range is about the first 63 days of 1970, so `datetime(864000, 'auto')` gives `-2347-06-13` (a Julian day) while `'unixepoch'` gives 1970-01-11. A millisecond value is out of range and returns NULL.
- `unixepoch('2024-01-01 00:00:00.500', 'subsec')` returns the float `1704067200.5`; without `subsec` the result is an integer.
- `strftime('%f', ...)` returns seconds with milliseconds (`SS.SSS`, `20.123` here), not just the fraction.
- `timediff(a, b)` is text, calendar-style (years, months, days, then time): `'+0000-00-30 12:00:00.000'` for 2024-03-01 12:00 minus 2024-01-31. Swapping the arguments did not give the mirror image: `'-0000-01-01 12:00:00.000'`. Do not parse it for logic; use `julianday` differences (30.5 days here) or integer second differences.
- ms through a float: `1704067200999 / 1000.0` is `1704067200.999` and multiplies back to `1704067200999.0`, so milliseconds are safe in a float64; nanosecond epochs (about 1.7e18) are not, see below.
- NULL `event_ms` stays NULL in every function; in pandas an integer column with NULLs becomes float64.

**Then explain:**
- Unix time is seconds since 1970-01-01 UTC; apps often send milliseconds, so check the magnitude: 10 digits is seconds, 13 is milliseconds, 16 microseconds, 19 nanoseconds.
- SQLite stores no time type; `'unixepoch'` tells `datetime()` the number means seconds.
- pandas 3: `pd.to_datetime(strings)` gives `datetime64[us]` by default (the output shows it; a string with nine fractional digits gives `ns`), `Timestamp('2024-01-01').unit` is `us`, and integers with `unit="ms"` give `datetime64[ms]`. The same milliseconds read with `unit="s"` produce `55840-11-08 22:15:23` in pandas 3 instead of raising an error (I did not run pandas 2 here).
- Precision: `float(1700000000123456789)` is `1700000000123456768`, so a nanosecond epoch that passed through a float is wrong in the last digits; float seconds `1700000000.123456` shows `...123456001`. Keep epochs as integers.

**Follow-ups:**
- How do you get milliseconds as text? `strftime('%Y-%m-%d %H:%M:%f', event_ms / 1000.0, 'unixepoch')`; `%f` gives `SS.SSS`.
- How do you bucket by hour? `event_ms / 3600000` with integer division gives an hour number without any date function (UTC).
- How do you know whether a column is ms or s? Look at `MIN` and `MAX` magnitudes; do not guess.

**Common mistakes:**
- Passing milliseconds as seconds.
- Dividing by 1000 as an integer and losing the milliseconds, or by 1000.0 and then comparing floats for equality.
- Trusting `'auto'` near 1970.
- Parsing the `timediff` text, or assuming it is symmetric.

### Q38 ⭐ 🟡 Day boundaries and DST in aggregation: hourly metrics for a US/Eastern day with 23 hours (2024-03-10) and 25 hours (2024-11-03). Show with pandas resample('D') on a tz-aware index that the day has 23 or 25 hourly buckets, why daily averages per hour differ, and that UTC date grouping avoids the issue but misaligns with the business day. SQLite cannot do named zones, so show the UTC-offset-by-date emulation (a small offsets table) as the workaround and label real DST rules in other engines as not executed.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Store UTC, convert to the business zone before bucketing, and divide by the real number of hours in the local day: on 2024-03-10 US/Eastern has 23 hourly buckets and on 2024-11-03 it has 25, so `total / 24` is wrong on both; pandas does it with `tz_convert` plus `resample('D')`, SQLite needs a small UTC-offset table because it has no named zones.

**Schema and sample data:** one reading per UTC hour with value 10, covering three local days around each switch (the rows are generated in the Code block; hand-checkable because every hour is worth 10). The offsets table hard-codes the 2024 US rules: Eastern Standard Time is UTC-5 (-300 minutes), Eastern Daylight Time is UTC-4 (-240 minutes), DST starts 2024-03-10 at 02:00 EST (07:00 UTC) and ends 2024-11-03 at 02:00 EDT (06:00 UTC). Convention: business day = US/Eastern calendar day, stored times are UTC, no week logic.
```sql
CREATE TABLE metrics(ts_utc TEXT PRIMARY KEY, value INTEGER);
CREATE TABLE tz_offsets(valid_from_utc TEXT PRIMARY KEY, utc_offset_min INTEGER);
INSERT INTO tz_offsets VALUES
  ('2024-01-01 00:00:00', -300),
  ('2024-03-10 07:00:00', -240),
  ('2024-11-03 06:00:00', -300);
```

**SQL answer:** for each reading pick the offset row with the latest `valid_from_utc` not after the reading, shift the instant by that many minutes, and take the date (`SQL_MAIN`). `SQL_UTC` shows the UTC-date alternative.
```sql
SELECT date(m.ts_utc, printf('%+d minutes', o.utc_offset_min)) AS local_day,
       COUNT(*)                     AS hours,
       SUM(m.value)                 AS total,
       ROUND(1.0 * SUM(m.value) / 24, 2)    AS naive_avg_div_24,
       ROUND(1.0 * SUM(m.value) / COUNT(*), 2) AS true_avg_per_hour
FROM metrics m
JOIN tz_offsets o
  ON o.valid_from_utc = (SELECT MAX(valid_from_utc) FROM tz_offsets WHERE valid_from_utc <= m.ts_utc)
GROUP BY local_day
ORDER BY local_day
```
```sql
SELECT date(ts_utc) AS utc_day, COUNT(*) AS hours, SUM(value) AS total
FROM metrics WHERE ts_utc >= '2024-03-10' AND ts_utc < '2024-03-11' GROUP BY utc_day
```

**pandas answer:** localize to UTC, convert to `America/New_York`, resample by day on the tz-aware index.
```py
m = pd.read_sql_query("SELECT * FROM metrics", con, parse_dates=["ts_utc"])
local = m.assign(ts=m["ts_utc"].dt.tz_localize("UTC").dt.tz_convert("America/New_York")).set_index("ts")
daily = local["value"].resample("D").agg(["count", "sum"])
daily = daily[daily["count"] > 0].reset_index()
pd_df = pd.DataFrame({
    "local_day": daily["ts"].dt.strftime("%Y-%m-%d"),
    "hours": daily["count"],
    "total": daily["sum"],
})
pd_df["naive_avg_div_24"] = (pd_df["total"] / 24).round(2)
pd_df["true_avg_per_hour"] = (pd_df["total"] / pd_df["hours"]).round(2)
```

**Example:**
- 2024-03-10 local day: midnight EST is 05:00 UTC, midnight EDT on 03-11 is 04:00 UTC, so the day holds 23 hourly rows; total 23 x 10 = 230. Dividing by 24 gives 9.58; dividing by the 23 real hours gives 10.0.
- 2024-11-03: midnight EDT is 04:00 UTC and midnight EST on 11-04 is 05:00 UTC, 25 rows, total 250; `/24` gives 10.42, the real average is 10.0.
- The UTC date 2024-03-10 always has 24 rows (240), but it runs from 19:00 EST on Mar 9 to 19:59 EDT on Mar 10: it avoids 23/25-hour days and answers a different question.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q38: DST day boundaries. Business day = US/Eastern calendar day; stored timestamps are UTC.
# Offsets table below hard-codes the 2024 US rules (EST -300 min, EDT -240 min); SQLite has no named zones.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE metrics(ts_utc TEXT PRIMARY KEY, value INTEGER);
CREATE TABLE tz_offsets(valid_from_utc TEXT PRIMARY KEY, utc_offset_min INTEGER);
INSERT INTO tz_offsets VALUES
  ('2024-01-01 00:00:00', -300),   -- EST
  ('2024-03-10 07:00:00', -240),   -- DST starts: 02:00 EST = 07:00 UTC
  ('2024-11-03 06:00:00', -300);   -- DST ends:   02:00 EDT = 06:00 UTC
""")
# one reading per UTC hour with value 10; three local days around each switch
spring = pd.date_range("2024-03-09 05:00", "2024-03-12 03:00", freq="h")   # local midnight Mar 9 to end of Mar 11
fall = pd.date_range("2024-11-02 04:00", "2024-11-05 04:00", freq="h")     # local midnight Nov 2 to end of Nov 4
rows = [(t.strftime("%Y-%m-%d %H:%M:%S"), 10) for t in spring.append(fall)]
con.executemany("INSERT INTO metrics VALUES (?, ?)", rows)

SQL_MAIN = """
SELECT date(m.ts_utc, printf('%+d minutes', o.utc_offset_min)) AS local_day,
       COUNT(*)                     AS hours,
       SUM(m.value)                 AS total,
       ROUND(1.0 * SUM(m.value) / 24, 2)    AS naive_avg_div_24,
       ROUND(1.0 * SUM(m.value) / COUNT(*), 2) AS true_avg_per_hour
FROM metrics m
JOIN tz_offsets o
  ON o.valid_from_utc = (SELECT MAX(valid_from_utc) FROM tz_offsets WHERE valid_from_utc <= m.ts_utc)
GROUP BY local_day
ORDER BY local_day
"""
SQL_UTC = """
SELECT date(ts_utc) AS utc_day, COUNT(*) AS hours, SUM(value) AS total
FROM metrics WHERE ts_utc >= '2024-03-10' AND ts_utc < '2024-03-11' GROUP BY utc_day
"""
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

# --- pandas ---
m = pd.read_sql_query("SELECT * FROM metrics", con, parse_dates=["ts_utc"])
local = m.assign(ts=m["ts_utc"].dt.tz_localize("UTC").dt.tz_convert("America/New_York")).set_index("ts")
daily = local["value"].resample("D").agg(["count", "sum"])
daily = daily[daily["count"] > 0].reset_index()
pd_df = pd.DataFrame({
    "local_day": daily["ts"].dt.strftime("%Y-%m-%d"),
    "hours": daily["count"],
    "total": daily["sum"],
})
pd_df["naive_avg_div_24"] = (pd_df["total"] / 24).round(2)
pd_df["true_avg_per_hour"] = (pd_df["total"] / pd_df["hours"]).round(2)
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df.sort_values("local_day").reset_index(drop=True),
                              pd_df.sort_values("local_day").reset_index(drop=True), check_dtype=False)
print("\npandas resample('D') on a tz-aware index equals the offsets-table SQL: OK")
print("\nbucket labels with their UTC offsets (pandas):")
print([str(t) for t in daily["ts"].iloc[[1, 2, 4, 5]]])

print("\nUTC date grouping for 2024-03-10 (always 24 hours, but not the business day):")
print(pd.read_sql_query(SQL_UTC, con).to_string(index=False))
print("business day 2024-03-10 starts at 05:00 UTC and ends 03:59 UTC on 03-11; the UTC date 03-10 is 19:00 EST Mar 9 .. 19:59 EDT Mar 10")

# tz_localize on wall-clock times that do not exist or repeat
for label, s in [("2024-03-10 02:30 (skipped)", "2024-03-10 02:30"), ("2024-11-03 01:30 (repeated)", "2024-11-03 01:30")]:
    try:
        pd.Timestamp(s).tz_localize("America/New_York")
    except Exception as e:
        print(f"\ntz_localize {label} ->", type(e).__name__ + ":", e)
print("ambiguous='NaT' ->", pd.Timestamp("2024-11-03 01:30").tz_localize("America/New_York", ambiguous="NaT"))
print("ambiguous=True (first, DST) ->", pd.Timestamp("2024-11-03 01:30").tz_localize("America/New_York", ambiguous=True))
print("nonexistent='shift_forward' ->", pd.Timestamp("2024-03-10 02:30").tz_localize("America/New_York", nonexistent="shift_forward"))

# the resample day: Mar 10 has 23 hourly rows even though the index step is one hour
h = pd.Series(1, index=pd.date_range("2024-03-10", periods=48, freq="h", tz="America/New_York"))
print("\nrange of 48 hourly steps from local midnight 2024-03-10: counts per local day ->", h.resample("D").count().tolist())
```

**Output (my run):**
```text
 local_day  hours  total  naive_avg_div_24  true_avg_per_hour
2024-03-09     24    240             10.00               10.0
2024-03-10     23    230              9.58               10.0
2024-03-11     24    240             10.00               10.0
2024-11-02     24    240             10.00               10.0
2024-11-03     25    250             10.42               10.0
2024-11-04     24    240             10.00               10.0

pandas resample('D') on a tz-aware index equals the offsets-table SQL: OK

bucket labels with their UTC offsets (pandas):
['2024-03-10 00:00:00-05:00', '2024-03-11 00:00:00-04:00', '2024-11-03 00:00:00-04:00', '2024-11-04 00:00:00-05:00']

UTC date grouping for 2024-03-10 (always 24 hours, but not the business day):
   utc_day  hours  total
2024-03-10     24    240
business day 2024-03-10 starts at 05:00 UTC and ends 03:59 UTC on 03-11; the UTC date 03-10 is 19:00 EST Mar 9 .. 19:59 EDT Mar 10

tz_localize 2024-03-10 02:30 (skipped) -> ValueError: 2024-03-10 02:30:00 is a nonexistent time due to daylight savings time. Try using the 'nonexistent' argument.

tz_localize 2024-11-03 01:30 (repeated) -> ValueError: Cannot infer dst time from 2024-11-03 01:30:00, try using the 'ambiguous' argument
ambiguous='NaT' -> NaT
ambiguous=True (first, DST) -> 2024-11-03 01:30:00-04:00
nonexistent='shift_forward' -> 2024-03-10 03:00:00-04:00

range of 48 hourly steps from local midnight 2024-03-10: counts per local day -> [23, 24, 1]
```

**Edge cases:**
- Missing hours: compare the bucket's count with the expected 23, 24 or 25; a day with 24 rows on a spring-forward date means duplicates, with 23 rows on an ordinary day means a gap.
- pandas `resample('D')` on a tz-aware index makes empty days between the two datasets (counts of 0); the code keeps days with at least one row. Bucket labels change offset (`-05:00` then `-04:00`), as printed.
- Converting wall-clock times: `tz_localize` on a skipped time (2024-03-10 02:30) and on a repeated time (2024-11-03 01:30) both raised `ValueError` in this run, with messages that name the `nonexistent` and `ambiguous` arguments. `ambiguous='NaT'` returns `NaT`, `ambiguous=True` picks the first (DST) occurrence, `nonexistent='shift_forward'` gives 03:00-04:00. Storing UTC avoids the question.
- The offsets table only knows the rules you put in; a different year needs more rows, and other zones need their own table. The SQLite `'localtime'` modifier uses the host zone, so it is not used here.
- Other engines (not executed here): PostgreSQL `ts AT TIME ZONE 'America/New_York'`, MySQL `CONVERT_TZ(ts, 'UTC', 'America/New_York')` (needs the time-zone tables loaded), BigQuery `DATE(ts, 'America/New_York')`, Snowflake `CONVERT_TIMEZONE`, SQL Server `AT TIME ZONE`; all from memory and they apply the real rules.

**Then explain:**
- A "day" is a local-calendar concept; its length is 24 hours except at DST switches.
- Rates (per hour) need the actual hour count; totals are not affected, but "average per hour" and "hourly share of the day" are.
- UTC grouping is simple and stable but misaligns with the business day, so a daily revenue report shifts by hours.
- Shifting by a fixed offset (always -5 hours) is the common bug: it is right only for half the year.

**Follow-ups:**
- Why not use `localtime` in SQLite? It depends on the machine's time zone, so results change between hosts.
- What about half-hour zones? The offset is in minutes (`+330`), so India works the same way.
- How would you build the offsets table at scale? Generate it from the tz database, one row per transition, and join with a range (Q39).

**Common mistakes:**
- Dividing by 24 on every day.
- Converting with a fixed offset.
- Localizing naive local timestamps without handling the ambiguous hour.
- Grouping by UTC date and presenting it as the business day.

### Q39 ⭐ 🟡 Range joins on dates: promotions(promo_id, start_date, end_date) and orders(order_id, order_ts, amount). Attribute each order to the promotion running on its date with a BETWEEN-style join, show the timestamp trap on an inclusive end_date (an order at 14:00 on the end date), overlapping promotions fanning out rows (double counted revenue) and how to detect it, and the pandas options (merge_asof when ranges do not overlap, IntervalIndex, or a cross merge and filter).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Join on `order_ts >= start_date AND order_ts < date(end_date, '+1 day')` instead of BETWEEN, because an order at 14:00 on the end date compares greater than the bare end date string; and count promotion matches per order, since overlapping promotions fan one order out into several rows and double count its revenue.

**Schema and sample data:** three promotions, P1 and P2 overlap on 2024-03-05 to 03-07, end dates are inclusive and are plain dates; six orders with timestamps (order 2 is at 14:00 on P1's end date and also inside P2, order 3 is at 14:00 on P2's end date, order 6 sits in the overlap). Convention: one time zone, no conversion, no week logic.
```sql
CREATE TABLE promotions(promo_id TEXT PRIMARY KEY, start_date TEXT, end_date TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO promotions VALUES ('P1','2024-03-01','2024-03-07'),('P2','2024-03-05','2024-03-10'),('P3','2024-03-15','2024-03-20');
INSERT INTO orders VALUES (1,'2024-03-02 10:00:00',100),(2,'2024-03-07 14:00:00',50),(3,'2024-03-10 14:00:00',70),
  (4,'2024-03-12 09:00:00',30),(5,'2024-03-16 12:00:00',40),(6,'2024-03-06 10:00:00',20);
```

**SQL answer:** four queries in the Code block. `SQL_NAIVE` is the BETWEEN trap, `SQL_FANOUT` is the correct window but shows the duplicate matches, `SQL_DETECT` finds orders matching more than one promotion, and `SQL_MAIN` assigns one promotion per order with the rule "the most recently started promotion wins" (a business rule to confirm).
```sql
SELECT o.order_id, p.promo_id
FROM orders o LEFT JOIN promotions p
  ON o.order_ts BETWEEN p.start_date AND p.end_date
ORDER BY o.order_id, p.promo_id
```
```sql
SELECT o.order_id, o.amount, p.promo_id
FROM orders o LEFT JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
ORDER BY o.order_id, p.promo_id
```
```sql
SELECT o.order_id, COUNT(*) AS matches
FROM orders o JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
GROUP BY o.order_id HAVING COUNT(*) > 1 ORDER BY o.order_id
```
```sql
SELECT o.order_id, o.amount, p.promo_id
FROM orders o
LEFT JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
 AND p.start_date = (SELECT MAX(p2.start_date) FROM promotions p2
                     WHERE o.order_ts >= p2.start_date AND o.order_ts < date(p2.end_date, '+1 day'))
ORDER BY o.order_id
```

**pandas answer:** a cross merge and filter shows every match; `merge_asof` gives one promotion per order using the same "latest start wins" rule as `SQL_MAIN` (then check the order is before the window end); an `IntervalIndex` works only when the intervals do not overlap.
```py
orders = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
promos = pd.read_sql_query("SELECT * FROM promotions", con, parse_dates=["start_date", "end_date"])
promos["end_excl"] = promos["end_date"] + pd.Timedelta(days=1)
# option A: cross merge and filter (shows every match, so fan-out is visible)
cross = orders.merge(promos, how="cross")
cross = cross[(cross["order_ts"] >= cross["start_date"]) & (cross["order_ts"] < cross["end_excl"])]
# option B: merge_asof = latest start <= order_ts, then check the window end (same rule as SQL_MAIN)
asof = pd.merge_asof(orders.sort_values("order_ts"), promos.sort_values("start_date"),
                     left_on="order_ts", right_on="start_date", direction="backward")
asof.loc[asof["order_ts"] >= asof["end_excl"], "promo_id"] = None
pd_df = asof[["order_id", "amount", "promo_id"]].sort_values("order_id").reset_index(drop=True)
```

**Example:**
- Order 3 (03-10 14:00, amount 70): `'2024-03-10 14:00:00' BETWEEN '2024-03-05' AND '2024-03-10'` is false because the text `2024-03-10 14:00:00` sorts after `2024-03-10`, so the naive query gives it no promotion. With `< date(end_date, '+1 day')` the bound is `2024-03-11` and it matches P2.
- Order 2 (03-07 14:00, 50): the same trap removes P1 (end `2024-03-07`), but it is inside P2 (03-05 to 03-10).
- Order 6 (03-06 10:00, 20) matches both P1 and P2. With the fan-out join the order appears twice; revenue becomes 310 + 50 + 20 = 380 (orders 2 and 6 each counted twice, as the output shows) against the true 310.
- With the latest start winning, orders 2, 3 and 6 go to P2; revenue by promotion: P1 100, P2 140, P3 40, none 30 (order 4, 03-12, has no promotion).

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q39: range joins on dates (promotions with INCLUSIVE end_date; orders have timestamps)
# Convention: order_ts is a naive local-business-time text 'YYYY-MM-DD HH:MM:SS'; one time zone, no conversion.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE promotions(promo_id TEXT PRIMARY KEY, start_date TEXT, end_date TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO promotions VALUES ('P1','2024-03-01','2024-03-07'),('P2','2024-03-05','2024-03-10'),('P3','2024-03-15','2024-03-20');
INSERT INTO orders VALUES (1,'2024-03-02 10:00:00',100),(2,'2024-03-07 14:00:00',50),(3,'2024-03-10 14:00:00',70),
  (4,'2024-03-12 09:00:00',30),(5,'2024-03-16 12:00:00',40),(6,'2024-03-06 10:00:00',20);
"""
# 1. the naive BETWEEN: end_date is a bare date, so '2024-03-10 14:00:00' > '2024-03-10' and the order falls out
SQL_NAIVE = """
SELECT o.order_id, p.promo_id
FROM orders o LEFT JOIN promotions p
  ON o.order_ts BETWEEN p.start_date AND p.end_date
ORDER BY o.order_id, p.promo_id
"""
# 2. right window (half-open at the next midnight), but overlaps fan rows out
SQL_FANOUT = """
SELECT o.order_id, o.amount, p.promo_id
FROM orders o LEFT JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
ORDER BY o.order_id, p.promo_id
"""
# 3. detection: one order matching more than one promotion
SQL_DETECT = """
SELECT o.order_id, COUNT(*) AS matches
FROM orders o JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
GROUP BY o.order_id HAVING COUNT(*) > 1 ORDER BY o.order_id
"""
# 4. main: one promotion per order, rule = the most recently started promotion wins
SQL_MAIN = """
SELECT o.order_id, o.amount, p.promo_id
FROM orders o
LEFT JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
 AND p.start_date = (SELECT MAX(p2.start_date) FROM promotions p2
                     WHERE o.order_ts >= p2.start_date AND o.order_ts < date(p2.end_date, '+1 day'))
ORDER BY o.order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
naive = pd.read_sql_query(SQL_NAIVE, con)
fan = pd.read_sql_query(SQL_FANOUT, con)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("naive BETWEEN (order 3, 14:00 on P2's end date, loses its promo; order 2 loses P1; order 6 still matches twice):")
print(naive.to_string(index=False))
print("\ndetect fan-out:")
print(pd.read_sql_query(SQL_DETECT, con).to_string(index=False))
print("\nrevenue: orders total =", con.execute("SELECT SUM(amount) FROM orders").fetchone()[0],
      "| sum after fan-out join =", int(fan["amount"].sum()))
print("\nmain (latest start wins):")
print(sql_df.to_string(index=False))
print("\nrevenue by promo, main:")
print(sql_df.groupby(sql_df["promo_id"].fillna("none"))["amount"].sum().to_string())

# --- pandas ---
orders = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
promos = pd.read_sql_query("SELECT * FROM promotions", con, parse_dates=["start_date", "end_date"])
promos["end_excl"] = promos["end_date"] + pd.Timedelta(days=1)
# option A: cross merge and filter (shows every match, so fan-out is visible)
cross = orders.merge(promos, how="cross")
cross = cross[(cross["order_ts"] >= cross["start_date"]) & (cross["order_ts"] < cross["end_excl"])]
# option B: merge_asof = latest start <= order_ts, then check the window end (same rule as SQL_MAIN)
asof = pd.merge_asof(orders.sort_values("order_ts"), promos.sort_values("start_date"),
                     left_on="order_ts", right_on="start_date", direction="backward")
asof.loc[asof["order_ts"] >= asof["end_excl"], "promo_id"] = None
pd_df = asof[["order_id", "amount", "promo_id"]].sort_values("order_id").reset_index(drop=True)
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df.sort_values("order_id").reset_index(drop=True), pd_df, check_dtype=False)
print("\npandas merge_asof equals SQL_MAIN: OK")
print("cross-merge matches per order:", cross.groupby("order_id").size().to_dict())

# option C: IntervalIndex (needs NON-overlapping intervals)
iv = pd.IntervalIndex.from_arrays(promos["start_date"], promos["end_excl"], closed="left")
print("IntervalIndex is_overlapping:", iv.is_overlapping)
try:
    iv.get_indexer(orders["order_ts"])
except Exception as e:
    print("get_indexer on overlapping ->", type(e).__name__ + ":", str(e)[:75])
ok = promos[promos["promo_id"].isin(["P2", "P3"])]
iv2 = pd.IntervalIndex.from_arrays(ok["start_date"], ok["end_excl"], closed="left")
pos = iv2.get_indexer(orders["order_ts"])
print("P2+P3 only, positions per order (-1 = none):", pos.tolist(), "| overlapping:", iv2.is_overlapping)
```

**Output (my run):**
```text
naive BETWEEN (order 3, 14:00 on P2's end date, loses its promo; order 2 loses P1; order 6 still matches twice):
 order_id promo_id
        1       P1
        2       P2
        3      NaN
        4      NaN
        5       P3
        6       P1
        6       P2

detect fan-out:
 order_id  matches
        2        2
        6        2

revenue: orders total = 310 | sum after fan-out join = 380

main (latest start wins):
 order_id  amount promo_id
        1     100       P1
        2      50       P2
        3      70       P2
        4      30      NaN
        5      40       P3
        6      20       P2

revenue by promo, main:
promo_id
P1      100
P2      140
P3       40
none     30

pandas merge_asof equals SQL_MAIN: OK
cross-merge matches per order: {1: 1, 2: 2, 3: 1, 5: 1, 6: 2}
IntervalIndex is_overlapping: True
get_indexer on overlapping -> InvalidIndexError: cannot handle overlapping indices; use IntervalIndex.get_indexer_non_unique
P2+P3 only, positions per order (-1 = none): [-1, 0, 0, -1, 1, 0] | overlapping: False
```

**Edge cases:**
- Detect fan-out before trusting any total: `GROUP BY order_id HAVING COUNT(*) > 1`, and compare `SUM(amount)` after the join with `SUM(amount)` on the orders table (380 against 310 here).
- Choosing the winner is a business rule: latest start, highest discount, a priority column, or split the amount across promotions. If promotions can nest (a short promotion inside a long one) the "latest start" rule from `merge_asof` can miss a still-running earlier promotion once the later one has ended, so check the window end and, if needed, use the cross merge.
- `merge_asof` needs both sides sorted by the key and finds only one match; it does not detect overlaps.
- `IntervalIndex.get_indexer` raises `InvalidIndexError` on overlapping intervals (printed in the run); with only P2 and P3 it returns positions, `-1` for no match.
- Orders on the end date at midnight exactly are inside the window; an end_date of NULL (open promotion) needs `OR end_date IS NULL` and is not modelled here.
- Dates stored as text in a consistent `YYYY-MM-DD` format compare correctly as strings; mixed formats do not (Q45).

**Then explain:**
- BETWEEN is inclusive on both ends, which is right for dates and wrong for timestamps against a date end bound; convert to a half-open interval `[start, end + 1 day)`.
- A range join can multiply rows, unlike an equality join on a key; always check cardinality.
- In pandas, the cross merge is the transparent option (rows = orders x promotions, filter after), `merge_asof` is the efficient single-match option, `IntervalIndex` is the lookup option for non-overlapping ranges.
- The fix for revenue by promotion is to pick one promotion per order before aggregating, not after.

**Follow-ups:**
- What if one order should count toward every promotion it falls in? Then fan-out is the intent, but totals by promotion will no longer add up to total revenue; say so and report it separately.
- What if end_date is exclusive in the source? Compare with `< end_date` directly.
- How would you do it for 10 million orders? Sort-merge style (`merge_asof`) or a range-aware join, plus an index on start_date; plans are Part 11.

**Common mistakes:**
- BETWEEN with a timestamp and an inclusive date end.
- Summing revenue after a join that fans out.
- Using `merge_asof` on unsorted frames or overlapping ranges without checking.
- Forgetting the unmatched (no promotion) orders by using an inner join, which also silently drops revenue.

### Q40 ⭐ 🟡 Performance of date filters (SQLite runnable, other engines hedged): orders(order_id, order_ts, amount) with 1,000,000 rows conceptually. Compare WHERE strftime('%Y-%m', order_ts) = '2024-03' (function on the column, cannot use an index) with WHERE order_ts >= '2024-03-01' AND order_ts < '2024-04-01' (sargable), run EXPLAIN QUERY PLAN on both with an index on order_ts, and mention an expression index. Cross-reference Part 11 for plans; partitioning by month is a hedged concept.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** A function wrapped around the column (`strftime('%Y-%m', order_ts) = '2024-03'`) cannot use a plain index on `order_ts` and scans every row, while the range `order_ts >= '2024-03-01' AND order_ts < '2024-04-01'` is sargable and does an index search; an expression index on the function is the other fix.

**Schema and sample data:** `orders(order_id, order_ts, amount)` with `order_ts` as `YYYY-MM-DD HH:MM:SS` text; the Code block generates 200,000 rows one every 157 seconds from 2024-01-01 (a stand-in for the 1,000,000 conceptual rows; a row count of this size is enough to show the plan). A plain index `idx_orders_ts` is on `order_ts`. Convention: naive timestamps, one time zone, no weeks. The data are synthetic, not hand-checkable row by row, so the hand check is on the March range: 31 days x 86400 s / 157 s = 17,058.9, which matches the printed count of 17,059.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
CREATE INDEX idx_orders_ts ON orders(order_ts);
```

**SQL answer:** the function version, the sargable range (`SQL_MAIN`), and a BETWEEN with a bare last day for comparison.
```sql
SELECT COUNT(*), SUM(amount) FROM orders WHERE strftime('%Y-%m', order_ts) = '2024-03'
```
```sql
SELECT COUNT(*), SUM(amount) FROM orders WHERE order_ts >= '2024-03-01' AND order_ts < '2024-04-01'
```
```sql
SELECT COUNT(*), SUM(amount) FROM orders WHERE order_ts BETWEEN '2024-03-01' AND '2024-03-31'
```
The expression index (created in the Code block after the first plan is printed):
```sql
CREATE INDEX idx_orders_month ON orders(strftime('%Y-%m', order_ts));
```

**pandas answer:** the pandas equivalent of a range filter is a boolean mask, or a partial-string slice on a sorted `DatetimeIndex`; pandas has no index plan to inspect, both scan memory.
```py
df = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
mask = (df["order_ts"] >= "2024-03-01") & (df["order_ts"] < "2024-04-01")
pd_res = (int(mask.sum()), int(df.loc[mask, "amount"].sum()))
by_slice = df.set_index("order_ts").sort_index().loc["2024-03"]           # partial-string slice on a sorted DatetimeIndex
```

**Example:**
- Function on the column: the plan line is `SCAN orders`; SQLite must evaluate `strftime` for all 200,000 rows even though an index on `order_ts` exists.
- Range: `SEARCH orders USING INDEX idx_orders_ts (order_ts>? AND order_ts<?)`; it seeks to `2024-03-01` and stops at `2024-04-01`, touching about 17,059 index entries.
- The VM instruction counter (a rough count from `set_progress_handler`, in steps of 100) is about 851,200 for the scan against about 102,400 for the range, roughly 8 times; treat it as indicative, not a benchmark.
- After the expression index the function version is `SEARCH ... USING INDEX idx_orders_month (<expr>=?)` and costs about the same as the range. The expression must be written the same way: `strftime('%Y/%m', order_ts)` does not match the index and the plan falls back to a scan (printed, on a covering index scan).

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q40: sargable date filters, EXPLAIN QUERY PLAN, expression index (SQLite 3.45.1 only; other engines hedged in prose)
# Convention: order_ts is naive text 'YYYY-MM-DD HH:MM:SS'; 200,000 synthetic rows stand in for 1,000,000.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER)")
base = pd.Timestamp("2024-01-01")
rows = [(i, (base + pd.Timedelta(seconds=157 * i)).strftime("%Y-%m-%d %H:%M:%S"), 1 + i % 50) for i in range(200_000)]
con.executemany("INSERT INTO orders VALUES (?,?,?)", rows)
con.execute("CREATE INDEX idx_orders_ts ON orders(order_ts)")
con.commit()

SQL_FUNC = "SELECT COUNT(*), SUM(amount) FROM orders WHERE strftime('%Y-%m', order_ts) = '2024-03'"
SQL_MAIN = "SELECT COUNT(*), SUM(amount) FROM orders WHERE order_ts >= '2024-03-01' AND order_ts < '2024-04-01'"
SQL_BAD_BETWEEN = "SELECT COUNT(*), SUM(amount) FROM orders WHERE order_ts BETWEEN '2024-03-01' AND '2024-03-31'"

def plan(sql):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

def vm_steps(sql):
    n = [0]
    def tick():
        n[0] += 1
        return 0
    con.set_progress_handler(tick, 100)       # callback every 100 VM instructions
    con.execute(sql).fetchall()
    con.set_progress_handler(None, 0)
    return n[0] * 100

r_func, r_main, r_bad = (con.execute(s).fetchone() for s in (SQL_FUNC, SQL_MAIN, SQL_BAD_BETWEEN))
print("rows, revenue  function-on-column:", r_func, "| range:", r_main, "| BETWEEN with last day as bare date:", r_bad)
assert r_func == r_main and r_bad != r_main

# --- pandas ---
df = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
mask = (df["order_ts"] >= "2024-03-01") & (df["order_ts"] < "2024-04-01")
pd_res = (int(mask.sum()), int(df.loc[mask, "amount"].sum()))
by_slice = df.set_index("order_ts").sort_index().loc["2024-03"]           # partial-string slice on a sorted DatetimeIndex
# --- end pandas ---
assert pd_res == tuple(r_main) and (len(by_slice), int(by_slice["amount"].sum())) == pd_res
print("pandas mask and .loc['2024-03'] equal SQL:", pd_res)

print("\nPLAN with plain index on order_ts")
print(" function on column :", plan(SQL_FUNC))
print(" range              :", plan(SQL_MAIN))
print("approx VM instructions  function:", vm_steps(SQL_FUNC), "| range:", vm_steps(SQL_MAIN))

con.execute("CREATE INDEX idx_orders_month ON orders(strftime('%Y-%m', order_ts))")
print("\nPLAN after expression index on strftime('%Y-%m', order_ts)")
print(" function on column :", plan(SQL_FUNC))
print(" range              :", plan(SQL_MAIN))
print("approx VM instructions  function:", vm_steps(SQL_FUNC), "| range:", vm_steps(SQL_MAIN))
try:
    print(" index on strftime with 'localtime' ->", con.execute("CREATE INDEX bad ON orders(strftime('%Y-%m', order_ts, 'localtime'))").fetchall())
except Exception as e:
    print(" index on strftime with 'localtime' ->", type(e).__name__ + ":", e)
print(" same filter written with a different format string:", plan("SELECT COUNT(*) FROM orders WHERE strftime('%Y/%m', order_ts) = '2024/03'"))
```

**Output (my run):**
```text
rows, revenue  function-on-column: (17059, 435000) | range: (17059, 435000) | BETWEEN with last day as bare date: (16509, 420975)
pandas mask and .loc['2024-03'] equal SQL: (17059, 435000)

PLAN with plain index on order_ts
 function on column : ['SCAN orders']
 range              : ['SEARCH orders USING INDEX idx_orders_ts (order_ts>? AND order_ts<?)']
approx VM instructions  function: 851200 | range: 102400

PLAN after expression index on strftime('%Y-%m', order_ts)
 function on column : ['SEARCH orders USING INDEX idx_orders_month (<expr>=?)']
 range              : ['SEARCH orders USING INDEX idx_orders_ts (order_ts>? AND order_ts<?)']
approx VM instructions  function: 102400 | range: 102400
 index on strftime with 'localtime' -> OperationalError: non-deterministic use of strftime() in an index
 same filter written with a different format string: ['SCAN orders USING COVERING INDEX idx_orders_ts']
```

**Edge cases:**
- BETWEEN `'2024-03-01' AND '2024-03-31'` is sargable but wrong for timestamps: it returned 16,509 rows against 17,059 (everything after midnight on 03-31 is lost); that is the same trap as Q39 and Q45.
- Index with a non-deterministic function is refused: `strftime(..., 'localtime')` raised `OperationalError: non-deterministic use of strftime() in an index`.
- If `order_ts` has mixed text formats the range comparison silently misorders; normalise on load.
- Planner behaviour depends on statistics, data volume and the SQLite version; on tiny tables a scan is also fine. Execution plans are covered in Part 11.
- Other engines (not executed here): the principle is the same in PostgreSQL, MySQL, BigQuery, Snowflake and SQL Server, wrapping the column in a function defeats a normal index unless there is a matching functional/expression index (PostgreSQL expression index, MySQL 8 functional index, SQL Server computed column). Partitioning by month (range partitions) lets the engine prune whole partitions when the filter is a range on the partition column; this is a concept here and I did not run it.

**Then explain:**
- Sargable means the predicate can be answered from the index order: a bare column compared with a constant range.
- Move the function to the constant side: compute `'2024-03-01'` and `'2024-04-01'` in the application or with `date()` on the constant, never on the column.
- Half-open ranges (`>= start AND < next_start`) also avoid the end-of-day trap.
- An expression index is the fallback when you cannot change the query, for example a BI tool that always emits `strftime`/`DATE_TRUNC`.

**Follow-ups:**
- How would you write "last 7 days" as of a fixed date? `order_ts >= date('2024-04-15', '-7 days') AND order_ts < '2024-04-16'`, with the as-of date passed as a parameter.
- Does an index on `(order_ts, amount)` help more? It can make the query covering (no table lookups); verify with the plan, not by assumption.
- Why can pandas filter by `.loc['2024-03']`? A sorted `DatetimeIndex` supports partial-string slicing; the slice includes the whole of March, end included.

**Common mistakes:**
- `WHERE DATE(order_ts) = ...` or `strftime` on the column.
- `BETWEEN` with a date end on a timestamp column.
- Creating an index and assuming every query uses it.
- Believing timings from a tiny table.

### Q41 ⭐ 🔴 Cohort retention by segment with a spine: users(user_id, signup_date, channel) and logins(user_id, login_date). Return one row per (channel, signup month, month offset 0 to 3) including offsets where nobody returned (0, not missing) by cross joining cohorts with an offset spine and LEFT JOINing activity. Explain why an INNER JOIN silently hides the zero cells that matter most and how to avoid mixing channels with different cohort sizes. pandas: reindex a MultiIndex pivot with fill_value=0.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Build one row per (channel, signup month, offset 0 to 3) by cross joining the cohorts with an offset spine, then LEFT JOIN the activity counts and `COALESCE` to 0; an INNER JOIN to activity silently drops the zero cells, and a cohort with no returns at all disappears completely.

**Schema and sample data:** twelve users in five (channel, signup month) cohorts and 24 login rows. User 1 logs in twice in February (distinct counting needed), organic user 12 never logs in (the whole March organic cohort is zero). Convention: calendar months from the stored `YYYY-MM-DD` text, no time zone, no weeks; as-of date fixed at 2024-04-30; retained at offset k means at least one login in the calendar month k months after the signup month.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, channel TEXT);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1,'2024-01-05','ads'),(2,'2024-01-20','ads'),(3,'2024-01-28','ads'),(4,'2024-01-31','ads'),
  (5,'2024-01-10','organic'),(6,'2024-01-15','organic'),(7,'2024-02-03','ads'),(8,'2024-02-14','ads'),(9,'2024-02-29','ads'),
  (10,'2024-02-02','organic'),(11,'2024-02-20','organic'),(12,'2024-03-10','organic');
INSERT INTO logins VALUES (1,'2024-01-05'),(1,'2024-02-10'),(1,'2024-02-25'),(1,'2024-03-02'),(2,'2024-01-20'),(2,'2024-02-02'),
  (3,'2024-01-28'),(4,'2024-01-31'),(4,'2024-02-01'),(5,'2024-01-10'),(5,'2024-02-11'),(5,'2024-03-12'),(5,'2024-04-01'),
  (6,'2024-01-15'),(6,'2024-02-20'),(7,'2024-02-03'),(7,'2024-03-05'),(8,'2024-02-14'),(9,'2024-02-29'),(9,'2024-03-01'),
  (10,'2024-02-02'),(10,'2024-03-03'),(10,'2024-04-04'),(11,'2024-02-20');
```

**SQL answer:** cohort sizes, an offset spine, distinct retained users per (channel, cohort, offset), then spine LEFT JOIN activity (`SQL_MAIN`). Cells whose calendar month is after the as-of date are not observed yet, so the percentage is NULL there rather than a false 0. `SQL_INNER` is the broken version.
```sql
WITH cohort AS (
  SELECT channel, strftime('%Y-%m', signup_date) AS cohort_month, COUNT(*) AS cohort_size
  FROM users GROUP BY channel, cohort_month
), offsets(month_offset) AS (VALUES (0), (1), (2), (3)),
act AS (
  SELECT u.channel, strftime('%Y-%m', u.signup_date) AS cohort_month,
         (CAST(strftime('%Y', l.login_date) AS INTEGER) * 12 + CAST(strftime('%m', l.login_date) AS INTEGER))
       - (CAST(strftime('%Y', u.signup_date) AS INTEGER) * 12 + CAST(strftime('%m', u.signup_date) AS INTEGER)) AS month_offset,
         COUNT(DISTINCT u.user_id) AS retained_users
  FROM users u JOIN logins l ON l.user_id = u.user_id
  GROUP BY 1, 2, 3
)
SELECT c.channel, c.cohort_month, o.month_offset, c.cohort_size,
       COALESCE(a.retained_users, 0) AS retained_users,
       CASE WHEN date(c.cohort_month || '-01', '+' || o.month_offset || ' months') <= '2024-04-30'
            THEN ROUND(100.0 * COALESCE(a.retained_users, 0) / c.cohort_size, 1) END AS retention_pct
FROM cohort c CROSS JOIN offsets o
LEFT JOIN act a ON a.channel = c.channel AND a.cohort_month = c.cohort_month AND a.month_offset = o.month_offset
ORDER BY c.channel, c.cohort_month, o.month_offset
```
```sql
WITH act AS (
  SELECT u.channel, strftime('%Y-%m', u.signup_date) AS cohort_month,
         (CAST(strftime('%Y', l.login_date) AS INTEGER) * 12 + CAST(strftime('%m', l.login_date) AS INTEGER))
       - (CAST(strftime('%Y', u.signup_date) AS INTEGER) * 12 + CAST(strftime('%m', u.signup_date) AS INTEGER)) AS month_offset,
         COUNT(DISTINCT u.user_id) AS retained_users
  FROM users u JOIN logins l ON l.user_id = u.user_id GROUP BY 1, 2, 3
)
SELECT * FROM act WHERE month_offset BETWEEN 0 AND 3 ORDER BY channel, cohort_month, month_offset
```

**pandas answer:** compute offsets with Period subtraction, `pivot_table` with `nunique`, then reindex the (channel, cohort) rows from the cohort sizes and the columns 0 to 3 with `fill_value=0`.
```py
users = pd.read_sql_query("SELECT * FROM users", con, parse_dates=["signup_date"])
logins = pd.read_sql_query("SELECT * FROM logins", con, parse_dates=["login_date"])
users["cohort_month"] = users["signup_date"].dt.to_period("M")
size = users.groupby(["channel", "cohort_month"])["user_id"].nunique().rename("cohort_size")
j = logins.merge(users, on="user_id")
j["month_offset"] = (j["login_date"].dt.to_period("M") - j["cohort_month"]).apply(lambda d: d.n)
j = j[j["month_offset"].between(0, 3)]
piv = j.pivot_table(index=["channel", "cohort_month"], columns="month_offset", values="user_id",
                    aggfunc="nunique", fill_value=0)
piv = piv.reindex(index=size.index, columns=[0, 1, 2, 3], fill_value=0)       # restores empty cells and empty cohorts
long = (piv.stack().rename("retained_users").reset_index()
          .merge(size.reset_index(), on=["channel", "cohort_month"]))
as_of_month = pd.Period("2024-04", "M")
long["observed"] = (long["cohort_month"] + long["month_offset"]) <= as_of_month
long["retention_pct"] = (100.0 * long["retained_users"] / long["cohort_size"]).round(1).where(long["observed"])
long["cohort_month"] = long["cohort_month"].astype(str)
pd_df = long[["channel", "cohort_month", "month_offset", "cohort_size", "retained_users", "retention_pct"]]
```

**Example:**
- Cohort ads / 2024-01 (users 1 to 4, size 4): month offset 0 (January) = everyone logged in on signup day, 4. Offset 1 (February): users 1, 2 and 4 logged in, user 3 did not, 3 of 4 = 75.0%. Offset 2 (March): only user 1, 1 of 4 = 25.0%. Offset 3 (April): nobody, 0 of 4 = 0.0%, a real zero that the spine keeps and an INNER JOIN removes.
- Cohort organic / 2024-03 (user 12, no logins): offsets 0 and 1 (March, April) are observed and are 0%; offsets 2 and 3 (May, June) are after the as-of date, so NULL.
- Spine version has 5 cohorts x 4 offsets = 20 rows; the INNER JOIN version has 12 rows (printed), and the organic 2024-03 cohort is not in it at all.
- Mixing channels: at offset 1, pooling all observed cells gives 8 retained of 12 users = 66.7%; the plain average of the five cell percentages is 58.3%. They differ because cohort sizes differ, so average counts, not percentages, and always keep channel in the grain.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q41: cohort retention by channel with a cohort x offset spine
# Convention: calendar months of the stored 'YYYY-MM-DD' text dates (no time zone); as-of date fixed at 2024-04-30.
# Retained at offset k = at least one login in the calendar month k months after the signup month.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, channel TEXT);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1,'2024-01-05','ads'),(2,'2024-01-20','ads'),(3,'2024-01-28','ads'),(4,'2024-01-31','ads'),
  (5,'2024-01-10','organic'),(6,'2024-01-15','organic'),(7,'2024-02-03','ads'),(8,'2024-02-14','ads'),(9,'2024-02-29','ads'),
  (10,'2024-02-02','organic'),(11,'2024-02-20','organic'),(12,'2024-03-10','organic');
INSERT INTO logins VALUES (1,'2024-01-05'),(1,'2024-02-10'),(1,'2024-02-25'),(1,'2024-03-02'),(2,'2024-01-20'),(2,'2024-02-02'),
  (3,'2024-01-28'),(4,'2024-01-31'),(4,'2024-02-01'),(5,'2024-01-10'),(5,'2024-02-11'),(5,'2024-03-12'),(5,'2024-04-01'),
  (6,'2024-01-15'),(6,'2024-02-20'),(7,'2024-02-03'),(7,'2024-03-05'),(8,'2024-02-14'),(9,'2024-02-29'),(9,'2024-03-01'),
  (10,'2024-02-02'),(10,'2024-03-03'),(10,'2024-04-04'),(11,'2024-02-20');
"""
SQL_MAIN = """
WITH cohort AS (
  SELECT channel, strftime('%Y-%m', signup_date) AS cohort_month, COUNT(*) AS cohort_size
  FROM users GROUP BY channel, cohort_month
), offsets(month_offset) AS (VALUES (0), (1), (2), (3)),
act AS (
  SELECT u.channel, strftime('%Y-%m', u.signup_date) AS cohort_month,
         (CAST(strftime('%Y', l.login_date) AS INTEGER) * 12 + CAST(strftime('%m', l.login_date) AS INTEGER))
       - (CAST(strftime('%Y', u.signup_date) AS INTEGER) * 12 + CAST(strftime('%m', u.signup_date) AS INTEGER)) AS month_offset,
         COUNT(DISTINCT u.user_id) AS retained_users
  FROM users u JOIN logins l ON l.user_id = u.user_id
  GROUP BY 1, 2, 3
)
SELECT c.channel, c.cohort_month, o.month_offset, c.cohort_size,
       COALESCE(a.retained_users, 0) AS retained_users,
       CASE WHEN date(c.cohort_month || '-01', '+' || o.month_offset || ' months') <= '2024-04-30'
            THEN ROUND(100.0 * COALESCE(a.retained_users, 0) / c.cohort_size, 1) END AS retention_pct
FROM cohort c CROSS JOIN offsets o
LEFT JOIN act a ON a.channel = c.channel AND a.cohort_month = c.cohort_month AND a.month_offset = o.month_offset
ORDER BY c.channel, c.cohort_month, o.month_offset
"""
# the same query with an INNER JOIN to activity and no spine
SQL_INNER = """
WITH act AS (
  SELECT u.channel, strftime('%Y-%m', u.signup_date) AS cohort_month,
         (CAST(strftime('%Y', l.login_date) AS INTEGER) * 12 + CAST(strftime('%m', l.login_date) AS INTEGER))
       - (CAST(strftime('%Y', u.signup_date) AS INTEGER) * 12 + CAST(strftime('%m', u.signup_date) AS INTEGER)) AS month_offset,
         COUNT(DISTINCT u.user_id) AS retained_users
  FROM users u JOIN logins l ON l.user_id = u.user_id GROUP BY 1, 2, 3
)
SELECT * FROM act WHERE month_offset BETWEEN 0 AND 3 ORDER BY channel, cohort_month, month_offset
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
inner = pd.read_sql_query(SQL_INNER, con)

# --- pandas ---
users = pd.read_sql_query("SELECT * FROM users", con, parse_dates=["signup_date"])
logins = pd.read_sql_query("SELECT * FROM logins", con, parse_dates=["login_date"])
users["cohort_month"] = users["signup_date"].dt.to_period("M")
size = users.groupby(["channel", "cohort_month"])["user_id"].nunique().rename("cohort_size")
j = logins.merge(users, on="user_id")
j["month_offset"] = (j["login_date"].dt.to_period("M") - j["cohort_month"]).apply(lambda d: d.n)
j = j[j["month_offset"].between(0, 3)]
piv = j.pivot_table(index=["channel", "cohort_month"], columns="month_offset", values="user_id",
                    aggfunc="nunique", fill_value=0)
piv = piv.reindex(index=size.index, columns=[0, 1, 2, 3], fill_value=0)       # restores empty cells and empty cohorts
long = (piv.stack().rename("retained_users").reset_index()
          .merge(size.reset_index(), on=["channel", "cohort_month"]))
as_of_month = pd.Period("2024-04", "M")
long["observed"] = (long["cohort_month"] + long["month_offset"]) <= as_of_month
long["retention_pct"] = (100.0 * long["retained_users"] / long["cohort_size"]).round(1).where(long["observed"])
long["cohort_month"] = long["cohort_month"].astype(str)
pd_df = long[["channel", "cohort_month", "month_offset", "cohort_size", "retained_users", "retention_pct"]]
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df.sort_values(["channel", "cohort_month", "month_offset"]).reset_index(drop=True),
                              pd_df.sort_values(["channel", "cohort_month", "month_offset"]).reset_index(drop=True),
                              check_dtype=False)
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")
print("\nINNER JOIN version: rows =", len(inner), "(spine version has", len(sql_df), ")")
print(inner.to_string(index=False))
print("organic 2024-03 cohort present in the INNER JOIN version?", bool((inner["cohort_month"] == "2024-03").any()))

# mixing channels: pooled rate vs unweighted mean of channel rates, offset 1, observed cells only
o1 = sql_df[(sql_df["month_offset"] == 1) & sql_df["retention_pct"].notna()]
pooled = 100.0 * o1["retained_users"].sum() / o1["cohort_size"].sum()
print("\noffset 1, observed cells: pooled =", round(pooled, 1), "| mean of cell percentages =", round(o1["retention_pct"].mean(), 1))
```

**Output (my run):**
```text
channel cohort_month  month_offset  cohort_size  retained_users  retention_pct
    ads      2024-01             0            4               4          100.0
    ads      2024-01             1            4               3           75.0
    ads      2024-01             2            4               1           25.0
    ads      2024-01             3            4               0            0.0
    ads      2024-02             0            3               3          100.0
    ads      2024-02             1            3               2           66.7
    ads      2024-02             2            3               0            0.0
    ads      2024-02             3            3               0            NaN
organic      2024-01             0            2               2          100.0
organic      2024-01             1            2               2          100.0
organic      2024-01             2            2               1           50.0
organic      2024-01             3            2               1           50.0
organic      2024-02             0            2               2          100.0
organic      2024-02             1            2               1           50.0
organic      2024-02             2            2               1           50.0
organic      2024-02             3            2               0            NaN
organic      2024-03             0            1               0            0.0
organic      2024-03             1            1               0            0.0
organic      2024-03             2            1               0            NaN
organic      2024-03             3            1               0            NaN

pandas equals SQL: OK

INNER JOIN version: rows = 12 (spine version has 20 )
channel cohort_month  month_offset  retained_users
    ads      2024-01             0               4
    ads      2024-01             1               3
    ads      2024-01             2               1
    ads      2024-02             0               3
    ads      2024-02             1               2
organic      2024-01             0               2
organic      2024-01             1               2
organic      2024-01             2               1
organic      2024-01             3               1
organic      2024-02             0               2
organic      2024-02             1               1
organic      2024-02             2               1
organic 2024-03 cohort present in the INNER JOIN version? False

offset 1, observed cells: pooled = 66.7 | mean of cell percentages = 58.3
```

**Edge cases:**
- Distinct users, not logins: user 1 has two February logins; `COUNT(DISTINCT user_id)` gives 1.
- Unobserved versus zero: a young cohort has offsets that cannot be observed yet (NULL here); showing 0 would look like churn (the same censoring idea as Q44).
- A cohort with no logins at all (organic March) is a row of zeros, not a missing row; the pivot needs the reindex with the cohort sizes, otherwise it is absent in pandas too.
- A login before the signup date would give a negative offset; the spine filters offsets to 0 to 3, so it drops out, but check the data.
- Users with no signup-month login still count in the denominator (cohort size comes from `users`, not from logins).
- Month offset uses calendar months, not 30-day periods; a user who signs up on 01-31 and logs in on 02-01 is offset 1 (user 4).

**Then explain:**
- A retention matrix is a grid; the grid has to be built first (cohort x offset), and the activity is attached to it.
- INNER JOIN keeps only cells with at least one returning user, so exactly the weak cells (zeros) vanish, making retention look better and charts jagged.
- The denominator is the cohort size per (channel, month), calculated from the users table independently of the join.
- Channel stays in the grain; compare channels, do not pool them unless you pool counts.
- In pandas, `reindex(..., fill_value=0)` on a MultiIndex pivot is the spine, and `stack` puts it back in long form.

**Follow-ups:**
- Day-N versus month-N retention? Different definition; state which (Part 8 covers metric design).
- How would you add a "rolling" retention (any login on or after month k)? Different numerator, and it is not available for the youngest cohorts.
- Offsets beyond 3? Change the `VALUES` list or generate it recursively; the as-of rule keeps the table honest.

**Common mistakes:**
- INNER JOIN or a `WHERE` on the right table of a LEFT JOIN, which turns it back into an inner join.
- Counting logins instead of distinct users.
- Zero-filling cells that are not observed yet.
- Averaging percentages across cohorts of different size.

### Q42 ⭐ 🔴 Cohort lifetime value by month: orders(order_id, user_id, order_ts, amount). For each first-order cohort and months_since_first, return cumulative revenue per cohort user (revenue to date divided by cohort size), with zero-fill for months with no sales so the cumulative line does not break. Cross-reference Part 5 for the running total mechanics and show the pandas version with pivot_table, fillna(0), cumsum(axis=1) and division by cohort size.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Assign each user to the month of their first order, build a cohort x months_since_first spine, left join monthly revenue with zero fill, take a running total per cohort (Part 5 mechanics) and divide by the cohort size; only offsets that have actually happened by the as-of date are shown, so young cohorts do not get a false flat line.

**Schema and sample data:** ten orders from six users. Cohorts by first-order month: Jan = users 1 and 2 (size 2), Feb = users 3 and 4 (size 2), Mar = user 5, Apr = user 6. Users 1, 2 and 3 buy again later, with a gap month (no sales in the cohort's second month). Convention: calendar months from the stored timestamps, no time zone, no weeks; as-of date 2024-04-30, so the last observed calendar month is April and offsets run 0 to 3.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05 09:30:00',100),(2,1,'2024-03-10 18:00:00',50),(3,2,'2024-01-20 11:00:00',60),
 (4,3,'2024-02-03 10:15:00',80),(5,3,'2024-02-20 19:45:00',20),(6,3,'2024-04-15 08:00:00',40),
 (7,4,'2024-02-14 12:00:00',30),(8,5,'2024-03-08 21:00:00',90),(9,2,'2024-04-02 07:30:00',10),
 (10,6,'2024-04-10 13:00:00',70);
```

**SQL answer:** first month per user, cohort sizes, an offset spine limited to observed months, revenue per (cohort, offset), then `SUM(...) OVER (PARTITION BY cohort ORDER BY offset ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` over the zero-filled revenue (`SQL_MAIN`). Running totals over frames are the subject of Part 5.
```sql
WITH o AS (
  SELECT user_id, amount, strftime('%Y-%m', order_ts) AS m,
         CAST(strftime('%Y', order_ts) AS INTEGER) * 12 + CAST(strftime('%m', order_ts) AS INTEGER) AS mi
  FROM orders
), first AS (
  SELECT user_id, MIN(mi) AS first_mi, MIN(m) AS cohort_month FROM o GROUP BY user_id
), cohort AS (
  SELECT first_mi, cohort_month, COUNT(*) AS cohort_size FROM first GROUP BY first_mi, cohort_month
), offsets(k) AS (VALUES (0), (1), (2), (3)),
spine AS (
  SELECT c.first_mi, c.cohort_month, c.cohort_size, k AS months_since_first
  FROM cohort c CROSS JOIN offsets
  WHERE c.first_mi + k <= 2024 * 12 + 4          -- observed only: calendar month <= as-of month
), rev AS (
  SELECT f.first_mi, o.mi - f.first_mi AS months_since_first, SUM(o.amount) AS revenue
  FROM o JOIN first f ON f.user_id = o.user_id GROUP BY 1, 2
)
SELECT s.cohort_month, s.months_since_first, s.cohort_size,
       COALESCE(r.revenue, 0) AS revenue,
       SUM(COALESCE(r.revenue, 0)) OVER (PARTITION BY s.cohort_month ORDER BY s.months_since_first
                                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_revenue,
       ROUND(1.0 * SUM(COALESCE(r.revenue, 0)) OVER (PARTITION BY s.cohort_month ORDER BY s.months_since_first
                                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / s.cohort_size, 2) AS ltv_per_user
FROM spine s LEFT JOIN rev r ON r.first_mi = s.first_mi AND r.months_since_first = s.months_since_first
ORDER BY s.cohort_month, s.months_since_first
```

**pandas answer:** `pivot_table`, `reindex` the offsets, `fillna(0)`, `cumsum(axis=1)`, divide by cohort size, then mask the unobserved cells (without the mask the zero fill creates a false flat tail).
```py
o = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
o["m"] = o["order_ts"].dt.to_period("M")
o["cohort"] = o.groupby("user_id")["m"].transform("min")
o["months_since_first"] = (o["m"] - o["cohort"]).apply(lambda d: d.n)
size = o.groupby("cohort")["user_id"].nunique()
rev = o.pivot_table(index="cohort", columns="months_since_first", values="amount", aggfunc="sum")
rev = rev.reindex(columns=[0, 1, 2, 3]).fillna(0)
cum = rev.cumsum(axis=1)
ltv = cum.div(size, axis=0)
last_obs = (pd.Period("2024-04", "M") - ltv.index).map(lambda d: d.n)           # highest observed offset per cohort
ltv = ltv.where(pd.DataFrame({k: last_obs >= k for k in ltv.columns}, index=ltv.index))   # mask unobserved cells
cum = cum.where(ltv.notna())
rev = rev.where(ltv.notna())
long = (rev.stack().rename("revenue").to_frame()
        .join(cum.stack().rename("cum_revenue")).join(ltv.stack().rename("ltv_per_user"))
        .dropna().reset_index())                      # pandas 3 stack() keeps NaN, so drop the unobserved cells
long["cohort_month"] = long["cohort"].astype(str)
long["cohort_size"] = long["cohort"].map(size).astype(int)
long[["revenue", "cum_revenue"]] = long[["revenue", "cum_revenue"]].astype(int)
long["ltv_per_user"] = long["ltv_per_user"].round(2)
pd_df = long[["cohort_month", "months_since_first", "cohort_size", "revenue", "cum_revenue", "ltv_per_user"]]
```

**Example:**
- Jan cohort (users 1 and 2): month 0 (January) revenue = 100 + 60 = 160. Month 1 (February) has no order: revenue 0 but the cumulative stays 160. Month 2 (March) = 50 (user 1), cumulative 210. Month 3 (April) = 10 (user 2), cumulative 220. Per cohort user: 80, 80, 105, 110.
- Feb cohort (users 3 and 4, size 2): month 0 = 80 + 20 + 30 = 130; month 1 (March) = 0; month 2 (April) = 40, cumulative 170, per user 65, 65, 85. Month 3 would be May, after the as-of date, so it is not reported.
- Mar cohort (user 5, 90): 90 then 90 (April had no order, cumulative stays). Apr cohort: 70 at month 0 only.
- The "wrong" table in the output zero-fills the unobserved cells and cumulates anyway: Feb shows 85.0 at month 3 and Mar and Apr show flat lines to month 3, which looks like a retained value that was never measured.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q42: cohort lifetime value (cumulative revenue per cohort user) with zero-filled months
# Convention: calendar months from stored text timestamps (no time zone); as-of date fixed at 2024-04-30, so only
# offsets whose calendar month is <= 2024-04 are reported. Cohort = month of the user's first order.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05 09:30:00',100),(2,1,'2024-03-10 18:00:00',50),(3,2,'2024-01-20 11:00:00',60),
 (4,3,'2024-02-03 10:15:00',80),(5,3,'2024-02-20 19:45:00',20),(6,3,'2024-04-15 08:00:00',40),
 (7,4,'2024-02-14 12:00:00',30),(8,5,'2024-03-08 21:00:00',90),(9,2,'2024-04-02 07:30:00',10),
 (10,6,'2024-04-10 13:00:00',70);
"""
SQL_MAIN = """
WITH o AS (
  SELECT user_id, amount, strftime('%Y-%m', order_ts) AS m,
         CAST(strftime('%Y', order_ts) AS INTEGER) * 12 + CAST(strftime('%m', order_ts) AS INTEGER) AS mi
  FROM orders
), first AS (
  SELECT user_id, MIN(mi) AS first_mi, MIN(m) AS cohort_month FROM o GROUP BY user_id
), cohort AS (
  SELECT first_mi, cohort_month, COUNT(*) AS cohort_size FROM first GROUP BY first_mi, cohort_month
), offsets(k) AS (VALUES (0), (1), (2), (3)),
spine AS (
  SELECT c.first_mi, c.cohort_month, c.cohort_size, k AS months_since_first
  FROM cohort c CROSS JOIN offsets
  WHERE c.first_mi + k <= 2024 * 12 + 4          -- observed only: calendar month <= as-of month
), rev AS (
  SELECT f.first_mi, o.mi - f.first_mi AS months_since_first, SUM(o.amount) AS revenue
  FROM o JOIN first f ON f.user_id = o.user_id GROUP BY 1, 2
)
SELECT s.cohort_month, s.months_since_first, s.cohort_size,
       COALESCE(r.revenue, 0) AS revenue,
       SUM(COALESCE(r.revenue, 0)) OVER (PARTITION BY s.cohort_month ORDER BY s.months_since_first
                                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_revenue,
       ROUND(1.0 * SUM(COALESCE(r.revenue, 0)) OVER (PARTITION BY s.cohort_month ORDER BY s.months_since_first
                                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / s.cohort_size, 2) AS ltv_per_user
FROM spine s LEFT JOIN rev r ON r.first_mi = s.first_mi AND r.months_since_first = s.months_since_first
ORDER BY s.cohort_month, s.months_since_first
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)

# --- pandas ---
o = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
o["m"] = o["order_ts"].dt.to_period("M")
o["cohort"] = o.groupby("user_id")["m"].transform("min")
o["months_since_first"] = (o["m"] - o["cohort"]).apply(lambda d: d.n)
size = o.groupby("cohort")["user_id"].nunique()
rev = o.pivot_table(index="cohort", columns="months_since_first", values="amount", aggfunc="sum")
rev = rev.reindex(columns=[0, 1, 2, 3]).fillna(0)
cum = rev.cumsum(axis=1)
ltv = cum.div(size, axis=0)
last_obs = (pd.Period("2024-04", "M") - ltv.index).map(lambda d: d.n)           # highest observed offset per cohort
ltv = ltv.where(pd.DataFrame({k: last_obs >= k for k in ltv.columns}, index=ltv.index))   # mask unobserved cells
cum = cum.where(ltv.notna())
rev = rev.where(ltv.notna())
long = (rev.stack().rename("revenue").to_frame()
        .join(cum.stack().rename("cum_revenue")).join(ltv.stack().rename("ltv_per_user"))
        .dropna().reset_index())                      # pandas 3 stack() keeps NaN, so drop the unobserved cells
long["cohort_month"] = long["cohort"].astype(str)
long["cohort_size"] = long["cohort"].map(size).astype(int)
long[["revenue", "cum_revenue"]] = long[["revenue", "cum_revenue"]].astype(int)
long["ltv_per_user"] = long["ltv_per_user"].round(2)
pd_df = long[["cohort_month", "months_since_first", "cohort_size", "revenue", "cum_revenue", "ltv_per_user"]]
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df.sort_values(["cohort_month", "months_since_first"]).reset_index(drop=True),
                              pd_df.sort_values(["cohort_month", "months_since_first"]).reset_index(drop=True),
                              check_dtype=False)
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")
raw = (o.pivot_table(index="cohort", columns="months_since_first", values="amount", aggfunc="sum")
         .reindex(columns=[0, 1, 2, 3]).fillna(0))
print("\nWRONG: zero-fill everything and cumsum, no as-of mask (false flat tails for young cohorts):")
print(raw.cumsum(axis=1).div(size, axis=0).round(2).to_string())
```

**Output (my run):**
```text
cohort_month  months_since_first  cohort_size  revenue  cum_revenue  ltv_per_user
     2024-01                   0            2      160          160          80.0
     2024-01                   1            2        0          160          80.0
     2024-01                   2            2       50          210         105.0
     2024-01                   3            2       10          220         110.0
     2024-02                   0            2      130          130          65.0
     2024-02                   1            2        0          130          65.0
     2024-02                   2            2       40          170          85.0
     2024-03                   0            1       90           90          90.0
     2024-03                   1            1        0           90          90.0
     2024-04                   0            1       70           70          70.0

pandas equals SQL: OK

WRONG: zero-fill everything and cumsum, no as-of mask (false flat tails for young cohorts):
months_since_first     0     1      2      3
cohort                                      
2024-01             80.0  80.0  105.0  110.0
2024-02             65.0  65.0   85.0   85.0
2024-03             90.0  90.0   90.0   90.0
2024-04             70.0  70.0   70.0   70.0
```

**Edge cases:**
- A month with no sales: the spine and `COALESCE(revenue, 0)` keep the row, so the running total does not skip or break.
- Unobserved offsets: exclude (NULL or drop), never zero-fill; the SQL does this with the `WHERE first_mi + k <= as-of month` filter, pandas with the mask.
- Cohort size is the count of users with a first order in that month, not the count of buyers in the later month; a user with several orders in a month counts once.
- Refunds or negative amounts make the cumulative line go down; the arithmetic is the same.
- Users with no orders are not in any cohort here (the cohort is defined by a first order); if the cohort should be signups, take the denominator from the users table and the question changes.
- `ORDER BY` inside the window needs a unique key per partition (the offset is unique per cohort); otherwise state the frame explicitly, as done here with `ROWS`.

**Then explain:**
- LTV here is cumulative revenue per original cohort user (not per active user), so the line can only go up when revenue is non-negative, and it plateaus when buying stops.
- Zero-fill matters because a window function over only the rows that exist carries the previous value correctly for a running total, but the missing offset row itself would be absent from the output and from any chart.
- Months since first is a calendar-month difference (`year * 12 + month`), not 30-day periods.
- Revenue to date divided by cohort size is gross revenue, not margin or discounted value; LTV with margin or a discount rate is a different metric.

**Follow-ups:**
- How would you get LTV by channel? Add channel to the cohort key; the spine and the denominator then use that key (Q41).
- How do you compare cohorts of different age? Compare the same offset (for example month 2) across cohorts, and only where observed.
- How do you extrapolate? Fit the shape of older cohorts and project; that is modelling, not SQL.

**Common mistakes:**
- Dividing by the number of buyers in the month instead of the cohort size.
- Letting the cumulative line extend over months that have not happened.
- Running a window over the sparse rows and plotting gaps as if they were zero revenue.
- Cutting the cohort month from a UTC timestamp when the business month is in another time zone (Q45).

### Q43 ⭐ 🔴 ISO week and year-boundary traps in year-over-year weekly comparison: sales(sale_date, amount). 2024-12-30 belongs to ISO week 1 of 2025 and 2021-01-01 to ISO week 53 of 2020. Show a naive strftime('%Y') plus week grouping splitting or merging weeks, the SQLite %W result, the ISO year emulation with date(d, '-3 days', 'weekday 4') (Thursday of the ISO week determines the ISO year), and pandas isocalendar(). Explain the 52 versus 53 week year problem for same-week-last-year comparisons and the 364-day offset alternative.
**Asked at:** SQLite date and time functions documentation (lang_datefunc, opened), vendor documentation and not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Group weeks by ISO year and ISO week, not by the calendar year plus `%W`; in SQLite 3.45.1 `%V` and `%G` return NULL, so I take the Thursday of the week, `date(d, '-3 days', 'weekday 4')`, whose year is the ISO year, and for same-week-last-year I either match ISO year minus 1 (week 53 then has no partner) or use a 364-day offset that always lands on the same weekday.

**Schema and sample data:** sixteen daily sales rows chosen around the year boundaries 2019/2020, 2020/2021, 2023/2024 and 2024/2025. Convention: weeks start on Monday (ISO 8601: week 1 is the week with the first Thursday of the year), dates are plain text, no time zone. 2024-12-30 is a Monday in ISO week 1 of 2025; 2021-01-01 is a Friday in ISO week 53 of 2020 (both premises in the question are correct, and the code checks them).
```sql
CREATE TABLE sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO sales VALUES
 ('2019-12-29',3),('2019-12-30',4),('2020-01-06',8),('2020-12-31',5),('2021-01-01',7),('2021-01-03',9),('2021-01-04',11),
 ('2023-12-31',15),('2024-01-01',25),('2024-01-02',35),
 ('2024-12-29',10),('2024-12-30',20),('2024-12-31',30),('2025-01-01',40),('2025-01-05',50),('2025-01-06',60);
```

**SQL answer:** `SQL_DAYS` shows the keys per date, `SQL_NAIVE` the naive grouping, and `SQL_MAIN` the weekly totals with last year's comparison by ISO key and by 364 days. The Monday of the week is `date(d, '-6 days', 'weekday 1')`.
```sql
SELECT sale_date,
       strftime('%Y', sale_date) || '-' || strftime('%W', sale_date) AS naive_year_week,
       strftime('%Y', date(sale_date, '-3 days', 'weekday 4'))        AS iso_year,
       (CAST(strftime('%j', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week,
       strftime('%V', sale_date)                                      AS native_V
FROM sales ORDER BY sale_date
```
```sql
SELECT strftime('%Y-%W', sale_date) AS naive_key, COUNT(*) AS days, SUM(amount) AS total
FROM sales WHERE sale_date >= '2024-12-23' GROUP BY 1 ORDER BY 1
```
```sql
WITH w AS (
  SELECT CAST(strftime('%Y', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) AS iso_year,
         (CAST(strftime('%j', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week,
         date(sale_date, '-6 days', 'weekday 1') AS week_start,
         SUM(amount) AS total
  FROM sales GROUP BY 1, 2, 3
)
SELECT a.iso_year, a.iso_week, a.week_start, a.total,
       b.total AS iso_match_last_year,
       c.total AS offset_364_last_year
FROM w a
LEFT JOIN w b ON b.iso_year = a.iso_year - 1 AND b.iso_week = a.iso_week
LEFT JOIN w c ON c.week_start = date(a.week_start, '-364 days')
ORDER BY a.week_start
```

**pandas answer:** `dt.isocalendar()` gives year, week and day; the week start is the date minus its weekday; last year's totals are looked up by (year - 1, week) or by `week_start - 364 days`.
```py
s = pd.read_sql_query("SELECT * FROM sales", con, parse_dates=["sale_date"])
iso = s["sale_date"].dt.isocalendar()
s["iso_year"], s["iso_week"] = iso["year"].astype(int), iso["week"].astype(int)
s["week_start"] = s["sale_date"] - pd.to_timedelta(s["sale_date"].dt.weekday, unit="D")
wk = s.groupby(["iso_year", "iso_week", "week_start"], as_index=False)["amount"].sum().rename(columns={"amount": "total"})
iso_prev = wk.set_index(["iso_year", "iso_week"])["total"]
prev_key = pd.MultiIndex.from_arrays([wk["iso_year"] - 1, wk["iso_week"]])
wk["iso_match_last_year"] = iso_prev.reindex(prev_key).to_numpy()
off = wk.set_index("week_start")["total"]
wk["offset_364_last_year"] = off.reindex(wk["week_start"] - pd.Timedelta(days=364)).to_numpy()
pd_df = wk.sort_values("week_start")
pd_df["week_start"] = pd_df["week_start"].dt.strftime("%Y-%m-%d")
```

**Example:**
- 2024-12-30 and 2024-12-31 are in ISO 2025-W01, but `strftime('%Y-%W')` labels them `2024-53`; 2025-01-01 and 2025-01-05 get `2025-00`. One ISO week (total 20 + 30 + 40 + 50 = 140) is split into two naive groups (50 and 90), and `2024-53` is not an ISO week of 2024 at all.
- Thursday rule: 2024-12-30 minus 3 days is 2024-12-27 (a Friday), `weekday 4` moves forward to the next Thursday, 2025-01-02, whose year is 2025, and `%j` = 2, so week = (2 - 1) / 7 + 1 = 1. For 2021-01-01 the Thursday is 2020-12-31 (day 366 of a leap year), week = 365 / 7 + 1 = 53, year 2020.
- Same ISO week last year: 2025-W01 (140) against 2024-W01 (25 + 35 = 60). 2020-W53 (21) has no 2019-W53 because 2019 has 52 ISO weeks (pandas confirms: 2020 -> 53, 2019 -> 52), so the ISO match is NULL while the 364-day offset gives the week starting 2019-12-30 (4).
- The two methods disagree for 2021-W01 (starts 2021-01-04): ISO match is 2020-W01 (4, the week starting 2019-12-30), 364 days back is the week starting 2020-01-06 (8, ISO 2020-W02).

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q43: ISO weeks, year boundaries, same-week-last-year
# Convention: weeks start on MONDAY (ISO 8601); dates are plain text, no time zone.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO sales VALUES
 ('2019-12-29',3),('2019-12-30',4),('2020-01-06',8),('2020-12-31',5),('2021-01-01',7),('2021-01-03',9),('2021-01-04',11),
 ('2023-12-31',15),('2024-01-01',25),('2024-01-02',35),
 ('2024-12-29',10),('2024-12-30',20),('2024-12-31',30),('2025-01-01',40),('2025-01-05',50),('2025-01-06',60);
"""
SQL_DAYS = """
SELECT sale_date,
       strftime('%Y', sale_date) || '-' || strftime('%W', sale_date) AS naive_year_week,
       strftime('%Y', date(sale_date, '-3 days', 'weekday 4'))        AS iso_year,
       (CAST(strftime('%j', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week,
       strftime('%V', sale_date)                                      AS native_V
FROM sales ORDER BY sale_date
"""
# weekly totals keyed by ISO year and week, then compared with the same ISO week one year earlier
SQL_MAIN = """
WITH w AS (
  SELECT CAST(strftime('%Y', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) AS iso_year,
         (CAST(strftime('%j', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week,
         date(sale_date, '-6 days', 'weekday 1') AS week_start,
         SUM(amount) AS total
  FROM sales GROUP BY 1, 2, 3
)
SELECT a.iso_year, a.iso_week, a.week_start, a.total,
       b.total AS iso_match_last_year,
       c.total AS offset_364_last_year
FROM w a
LEFT JOIN w b ON b.iso_year = a.iso_year - 1 AND b.iso_week = a.iso_week
LEFT JOIN w c ON c.week_start = date(a.week_start, '-364 days')
ORDER BY a.week_start
"""
SQL_NAIVE = """
SELECT strftime('%Y-%W', sale_date) AS naive_key, COUNT(*) AS days, SUM(amount) AS total
FROM sales WHERE sale_date >= '2024-12-23' GROUP BY 1 ORDER BY 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
days = pd.read_sql_query(SQL_DAYS, con)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(days.to_string(index=False))

# --- pandas ---
s = pd.read_sql_query("SELECT * FROM sales", con, parse_dates=["sale_date"])
iso = s["sale_date"].dt.isocalendar()
s["iso_year"], s["iso_week"] = iso["year"].astype(int), iso["week"].astype(int)
s["week_start"] = s["sale_date"] - pd.to_timedelta(s["sale_date"].dt.weekday, unit="D")
wk = s.groupby(["iso_year", "iso_week", "week_start"], as_index=False)["amount"].sum().rename(columns={"amount": "total"})
iso_prev = wk.set_index(["iso_year", "iso_week"])["total"]
prev_key = pd.MultiIndex.from_arrays([wk["iso_year"] - 1, wk["iso_week"]])
wk["iso_match_last_year"] = iso_prev.reindex(prev_key).to_numpy()
off = wk.set_index("week_start")["total"]
wk["offset_364_last_year"] = off.reindex(wk["week_start"] - pd.Timedelta(days=364)).to_numpy()
pd_df = wk.sort_values("week_start")
pd_df["week_start"] = pd_df["week_start"].dt.strftime("%Y-%m-%d")
# --- end pandas ---
# the emulated ISO key equals pandas isocalendar for every row
assert (days["iso_year"].astype(int).to_numpy() == s.sort_values("sale_date")["iso_year"].to_numpy()).all()
assert (days["iso_week"].to_numpy() == s.sort_values("sale_date")["iso_week"].to_numpy()).all()
print("\nemulation date(d,'-3 days','weekday 4') equals pandas isocalendar() on all", len(days), "dates: OK")
pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_df.reset_index(drop=True), check_dtype=False)
print("\nweekly totals with last-year comparisons:")
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")
print("\nnaive strftime('%Y-%W') grouping from 2024-12-23 on:")
print(pd.read_sql_query(SQL_NAIVE, con).to_string(index=False))

# resample anchors (pandas 3.0.5): which weekday ends the bin and which side is labelled
d = s.set_index("sale_date")["amount"]
d = d[d.index >= "2024-12-23"]
print("\nresample('W-SUN') (Mon..Sun bins, label = Sunday):", {str(k.date()): int(v) for k, v in d.resample("W-SUN").sum().items()})
print("resample('W-MON') (Tue..Mon bins, label = Monday):  ", {str(k.date()): int(v) for k, v in d.resample("W-MON").sum().items()})
print("resample('MS') labels:", [str(k.date()) for k in d.resample("MS").sum().index], "| (labels are the bin starts)")
print("weeks in ISO year: 2020 ->", pd.Timestamp("2020-12-28").isocalendar().week, "| 2019 ->", pd.Timestamp("2019-12-28").isocalendar().week,
      "| 2024 ->", pd.Timestamp("2024-12-28").isocalendar().week)
print("SQLite %V, %G on 3.45.1:", con.execute("SELECT strftime('%V','2024-12-30'), strftime('%G','2024-12-30'), strftime('%U','2024-12-30')").fetchone())
```

**Output (my run):**
```text
 sale_date naive_year_week iso_year  iso_week native_V
2019-12-29         2019-51     2019        52     None
2019-12-30         2019-52     2020         1     None
2020-01-06         2020-01     2020         2     None
2020-12-31         2020-52     2020        53     None
2021-01-01         2021-00     2020        53     None
2021-01-03         2021-00     2020        53     None
2021-01-04         2021-01     2021         1     None
2023-12-31         2023-52     2023        52     None
2024-01-01         2024-01     2024         1     None
2024-01-02         2024-01     2024         1     None
2024-12-29         2024-52     2024        52     None
2024-12-30         2024-53     2025         1     None
2024-12-31         2024-53     2025         1     None
2025-01-01         2025-00     2025         1     None
2025-01-05         2025-00     2025         1     None
2025-01-06         2025-01     2025         2     None

emulation date(d,'-3 days','weekday 4') equals pandas isocalendar() on all 16 dates: OK

weekly totals with last-year comparisons:
 iso_year  iso_week week_start  total  iso_match_last_year  offset_364_last_year
     2019        52 2019-12-23      3                  NaN                   NaN
     2020         1 2019-12-30      4                  NaN                   NaN
     2020         2 2020-01-06      8                  NaN                   NaN
     2020        53 2020-12-28     21                  NaN                   4.0
     2021         1 2021-01-04     11                  4.0                   8.0
     2023        52 2023-12-25     15                  NaN                   NaN
     2024         1 2024-01-01     60                  NaN                   NaN
     2024        52 2024-12-23     10                 15.0                  15.0
     2025         1 2024-12-30    140                 60.0                  60.0
     2025         2 2025-01-06     60                  NaN                   NaN

pandas equals SQL: OK

naive strftime('%Y-%W') grouping from 2024-12-23 on:
naive_key  days  total
  2024-52     1     10
  2024-53     2     50
  2025-00     2     90
  2025-01     1     60

resample('W-SUN') (Mon..Sun bins, label = Sunday): {'2024-12-29': 10, '2025-01-05': 140, '2025-01-12': 60}
resample('W-MON') (Tue..Mon bins, label = Monday):   {'2024-12-30': 30, '2025-01-06': 180}
resample('MS') labels: ['2024-12-01', '2025-01-01'] | (labels are the bin starts)
weeks in ISO year: 2020 -> 53 | 2019 -> 52 | 2024 -> 52
SQLite %V, %G on 3.45.1: (None, None, None)
```

**Edge cases:**
- 52 versus 53 week years: an ISO year has 53 weeks when 1 January is a Thursday, or a Wednesday in a leap year (2020 is the example here). Week 53 has no partner the year before, and week 1 can contain days from December.
- Never mix `%Y` with an ISO week: use the ISO year (Thursday's year) from the same expression. `%Y` of 2024-12-30 is 2024 but its ISO year is 2025.
- `%W` is the week number with Monday as the first day and days before the first Monday in week 00; it is not ISO (2024-12-30 gives 53). `%U` and `%V` and `%G` returned NULL in this run on SQLite 3.45.1.
- The 364-day offset (52 weeks) keeps weekday alignment, but after a few years the week drifts relative to the calendar (a 53-week year shifts it by one week), so holidays and seasons slide; fiscal calendars solve this with a 4-4-5 pattern (not executed or modelled here).
- Missing weeks: a LEFT JOIN returns NULL for the partner; in pandas `reindex` gives `NaN`. A week with partial data (as-of in mid-week) should not be compared with a full week.
- pandas resampling anchors: `resample('W-SUN')` makes Monday-to-Sunday bins labelled by the Sunday (matches ISO weeks); `resample('W-MON')` makes Tuesday-to-Monday bins labelled by the Monday and gives different totals (30 and 180 against 10, 140, 60 in the output). `resample('MS')` labels months by their first day.

**Then explain:**
- ISO 8601: weeks start Monday, week 1 contains the first Thursday, so the Thursday of a week decides which year it belongs to.
- Hence `date(d, '-3 days', 'weekday 4')`: step back 3 days, then move forward to a Thursday; for a Monday this is the same week's Thursday, for a Sunday it is the Thursday 3 days earlier.
- ISO week of year = `(day_of_year(Thursday) - 1) / 7 + 1`.
- Year-over-year weekly comparison has to choose: same ISO week (calendar aligned, 53-week gap) or same weekday 364 days earlier (weekday aligned, drifts). Say which and why.

**Follow-ups:**
- How would you compute ISO weeks on PostgreSQL, MySQL, BigQuery, Snowflake? Their functions (`EXTRACT(ISOYEAR ...)`, `YEARWEEK(d, 3)`, `ISOWEEK`, `WEEKISO`) exist as far as I know, not executed here; the logic is the same.
- What about weeks starting Sunday? Then it is a different convention (US); the Thursday trick does not apply; define the week start first.
- How do you handle the 53-week year in a chart? Compare 53 against 52 or use the 364-day offset and label the alignment.

**Common mistakes:**
- Grouping by `strftime('%Y')` plus a week number and splitting an ISO week across two years.
- Joining week 53 to a week that does not exist.
- Using `%W` and calling it ISO.
- Not stating the week-start convention.

### Q44 ⭐ 🔴 Tenure survival curve: subscriptions(sub_id, user_id, start_date, end_date) with NULL end_date for active. For each tenure month t (0 to 12) return the share of subscriptions that survived to month t, counting only subscriptions old enough to be observed at t (right-censoring: a subscription started two months ago cannot show month 6). Show the wrong version that treats unobserved as churned, with SQLite date arithmetic from an as-of date, and the pandas version with Timedelta months via DateOffset or period difference.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** For each tenure month t I compute every subscription's t-month anniversary, count a subscription as observed only if the anniversary is on or before the as-of date, and divide the survivors (end_date NULL or on or after the anniversary) by the observed count; dividing by all subscriptions treats the not-yet-observable ones as churned and understates survival.

**Schema and sample data:** ten subscriptions started between 2023-01 and 2024-05, some ended, some still active. Convention: as-of date `2024-06-30` (fixed, not today), end_date is inclusive (last day of service), dates are plain text, no time zone, no weeks; tenure month t is the t-month anniversary of start_date, clipped to the month end (2023-08-31 plus 6 months is 2024-02-29), and "survived to t" means still active on that anniversary.
```sql
CREATE TABLE subscriptions(sub_id INTEGER PRIMARY KEY, user_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO subscriptions VALUES
 (1,1,'2023-01-15',NULL),(2,2,'2023-01-20','2023-04-10'),(3,3,'2023-03-31','2023-05-15'),
 (4,4,'2023-05-10',NULL),(5,5,'2023-08-31','2023-12-31'),(6,6,'2023-09-05','2024-02-20'),
 (7,7,'2023-11-15',NULL),(8,8,'2024-01-31','2024-03-10'),(9,9,'2024-03-12',NULL),(10,10,'2024-05-20',NULL);
```

**SQL answer:** a `t` series 0 to 12 cross joined to subscriptions, the anniversary expression (the clip is a `CASE`, because SQLite's `+N months` overflows), then `observed`, `survived`, the correct share, and the wrong share (`SQL_MAIN`; the anniversary expression is built into the query text by the f-string in the Code block and printed here as evaluated).
```sql
WITH RECURSIVE t(t) AS (SELECT 0 UNION ALL SELECT t + 1 FROM t WHERE t < 12),
x AS (
  SELECT t.t, s.sub_id, s.end_date, CASE WHEN strftime('%d', date(s.start_date, '+' || t.t || ' months')) = strftime('%d', s.start_date)
        THEN date(s.start_date, '+' || t.t || ' months')
        ELSE date(s.start_date, 'start of month', '+' || (t.t + 1) || ' months', '-1 day') END AS anniv
  FROM t CROSS JOIN subscriptions s
)
SELECT t,
       SUM(anniv <= '2024-06-30')                                            AS observed,
       SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv)) AS survived,
       ROUND(100.0 * SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv))
             / SUM(anniv <= '2024-06-30'), 1)                                AS survival_pct,
       ROUND(100.0 * SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv))
             / COUNT(*), 1)                                                  AS wrong_pct_unobserved_as_churned
FROM x GROUP BY t HAVING SUM(anniv <= '2024-06-30') > 0 ORDER BY t
```

**pandas answer:** `start_date + pd.DateOffset(months=t)` (which clips by itself) per t, masks for observed and survived.
```py
subs = pd.read_sql_query("SELECT * FROM subscriptions", con, parse_dates=["start_date", "end_date"])
as_of = pd.Timestamp("2024-06-30")
rows = []
for t in range(13):
    anniv = subs["start_date"] + pd.DateOffset(months=t)          # DateOffset clips to month end
    observed = anniv <= as_of
    survived = observed & (subs["end_date"].isna() | (subs["end_date"] >= anniv))
    if observed.sum() > 0:
        rows.append({"t": t, "observed": int(observed.sum()), "survived": int(survived.sum()),
                     "survival_pct": round(100.0 * survived.sum() / observed.sum(), 1),
                     "wrong_pct_unobserved_as_churned": round(100.0 * survived.sum() / len(subs), 1)})
pd_df = pd.DataFrame(rows)
```

**Example:**
- t = 2: only subscription 10 (start 2024-05-20, anniversary 2024-07-20) is after the as-of date, so 9 are observed. Survivors: sub 2 ended 2023-04-10, after its anniversary 2023-03-20, so it survived month 2; sub 3 ended 2023-05-15, before 2023-05-31, did not; sub 8 ended 2024-03-10, before 2024-03-31, did not. Survivors 1, 2, 4, 5, 6, 7, 9 = 7, so 7 / 9 = 77.8%. The wrong version divides by 10 (all subscriptions): 70.0%.
- t = 12: observed are the four subscriptions that started on or before 2023-06-30 (subs 1, 2, 3, 4); survivors are subs 1 and 4, so 2 / 4 = 50.0%; the wrong version gives 2 / 10 = 20.0%.
- The wrong column keeps falling as t grows because the denominator never shrinks, even for subscriptions that are too young to be judged.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q44: tenure survival with right-censoring from a fixed as-of date
# Convention: dates are plain text, no time zone. as_of = 2024-06-30. end_date is INCLUSIVE (last day of service).
# A subscription "survives to month t" if it is still active on its t-month anniversary:
#   end_date IS NULL OR end_date >= anniversary. It is "observed at t" only if anniversary <= as_of.
# Anniversary = start_date + t months, clipped to the last day of the month (Aug 31 + 6 months = Feb 29, not Mar 2).
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE subscriptions(sub_id INTEGER PRIMARY KEY, user_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO subscriptions VALUES
 (1,1,'2023-01-15',NULL),(2,2,'2023-01-20','2023-04-10'),(3,3,'2023-03-31','2023-05-15'),
 (4,4,'2023-05-10',NULL),(5,5,'2023-08-31','2023-12-31'),(6,6,'2023-09-05','2024-02-20'),
 (7,7,'2023-11-15',NULL),(8,8,'2024-01-31','2024-03-10'),(9,9,'2024-03-12',NULL),(10,10,'2024-05-20',NULL);
"""
ANNIV = """CASE WHEN strftime('%d', date(s.start_date, '+' || t.t || ' months')) = strftime('%d', s.start_date)
        THEN date(s.start_date, '+' || t.t || ' months')
        ELSE date(s.start_date, 'start of month', '+' || (t.t + 1) || ' months', '-1 day') END"""
SQL_MAIN = f"""
WITH RECURSIVE t(t) AS (SELECT 0 UNION ALL SELECT t + 1 FROM t WHERE t < 12),
x AS (
  SELECT t.t, s.sub_id, s.end_date, {ANNIV} AS anniv
  FROM t CROSS JOIN subscriptions s
)
SELECT t,
       SUM(anniv <= '2024-06-30')                                            AS observed,
       SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv)) AS survived,
       ROUND(100.0 * SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv))
             / SUM(anniv <= '2024-06-30'), 1)                                AS survival_pct,
       ROUND(100.0 * SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv))
             / COUNT(*), 1)                                                  AS wrong_pct_unobserved_as_churned
FROM x GROUP BY t HAVING SUM(anniv <= '2024-06-30') > 0 ORDER BY t
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)

# --- pandas ---
subs = pd.read_sql_query("SELECT * FROM subscriptions", con, parse_dates=["start_date", "end_date"])
as_of = pd.Timestamp("2024-06-30")
rows = []
for t in range(13):
    anniv = subs["start_date"] + pd.DateOffset(months=t)          # DateOffset clips to month end
    observed = anniv <= as_of
    survived = observed & (subs["end_date"].isna() | (subs["end_date"] >= anniv))
    if observed.sum() > 0:
        rows.append({"t": t, "observed": int(observed.sum()), "survived": int(survived.sum()),
                     "survival_pct": round(100.0 * survived.sum() / observed.sum(), 1),
                     "wrong_pct_unobserved_as_churned": round(100.0 * survived.sum() / len(subs), 1)})
pd_df = pd.DataFrame(rows)
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df.sort_values("t").reset_index(drop=True), pd_df.sort_values("t").reset_index(drop=True),
                              check_dtype=False)
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")

print("\nplain date(start,'+t months') overflow vs clipped, subscription 5 (start 2023-08-31) and 8 (2024-01-31):")
for sid in (5, 8):
    st = con.execute("SELECT start_date FROM subscriptions WHERE sub_id = ?", (sid,)).fetchone()[0]
    for t in (1, 6):
        naive = con.execute("SELECT date(?, '+' || ? || ' months')", (st, t)).fetchone()[0]
        clip = (pd.Timestamp(st) + pd.DateOffset(months=t)).date()
        print(f"  sub {sid} start {st} +{t} months: SQLite plain modifier {naive} | pandas DateOffset {clip}")
# period arithmetic alternative: whole calendar-month difference, ignores the day of month
p = (as_of.to_period("M") - subs["start_date"].dt.to_period("M")).apply(lambda d: d.n)
print("\nperiod difference (calendar months from start month to as-of month):", p.tolist())
print("elapsed full months via DateOffset (max t with anniversary <= as_of):",
      [max(t for t in range(30) if st + pd.DateOffset(months=t) <= as_of) for st in subs["start_date"]])
```

**Output (my run):**
```text
 t  observed  survived  survival_pct  wrong_pct_unobserved_as_churned
 0        10        10         100.0                            100.0
 1        10        10         100.0                            100.0
 2         9         7          77.8                             70.0
 3         9         6          66.7                             60.0
 4         8         5          62.5                             50.0
 5         8         4          50.0                             40.0
 6         7         3          42.9                             30.0
 7         7         3          42.9                             30.0
 8         6         2          33.3                             20.0
 9         6         2          33.3                             20.0
10         5         2          40.0                             20.0
11         4         2          50.0                             20.0
12         4         2          50.0                             20.0

pandas equals SQL: OK

plain date(start,'+t months') overflow vs clipped, subscription 5 (start 2023-08-31) and 8 (2024-01-31):
  sub 5 start 2023-08-31 +1 months: SQLite plain modifier 2023-10-01 | pandas DateOffset 2023-09-30
  sub 5 start 2023-08-31 +6 months: SQLite plain modifier 2024-03-02 | pandas DateOffset 2024-02-29
  sub 8 start 2024-01-31 +1 months: SQLite plain modifier 2024-03-02 | pandas DateOffset 2024-02-29
  sub 8 start 2024-01-31 +6 months: SQLite plain modifier 2024-07-31 | pandas DateOffset 2024-07-31

period difference (calendar months from start month to as-of month): [17, 17, 15, 13, 10, 9, 7, 5, 3, 1]
elapsed full months via DateOffset (max t with anniversary <= as_of): [17, 17, 15, 13, 10, 9, 7, 5, 3, 1]
```

**Edge cases:**
- Right-censoring: an active subscription is not a survivor at t if it has not reached t yet; it is simply not in that month's denominator.
- The observed share is not monotone: it rises at t = 10 and 11 (40.0%, 50.0%) because the observed set changes with t (different, older subscriptions). A proper survival estimate (Kaplan-Meier) uses the at-risk set at each step; this simple "share of observed" is a teaching version, and I did not implement Kaplan-Meier here.
- Month-end starts: `date('2023-08-31', '+6 months')` is `2024-03-02` in SQLite (overflow) while `DateOffset` gives `2024-02-29`; the code clips in SQL so the two agree, and the output prints both for subscriptions 5 and 8.
- Start and end on the same day (tenure 0): `end_date >= anniversary` is true on day 0 with an inclusive end, so a same-day cancellation survives month 0 under this definition; decide whether that is wanted.
- NULL start_date is dropped (comparison unknown); NULL end_date means active.
- Period difference (`as_of.to_period('M') - start.to_period('M')`) counts calendar months, ignoring the day: it gave 17, 17, 15, ...; the `DateOffset` count of fully elapsed months is the same here, but they differ when the as-of day of month is before the start day (start on the 20th, as-of the 10th of the next month: period difference 1, fully elapsed months 0).

**Then explain:**
- Survival at t among those who could have reached t; every t has its own denominator.
- The wrong version makes churn look worse and the curve look steeper for recent cohorts; the censored ones are neither churned nor survived.
- SQLite month arithmetic overflows and has no `DATEDIFF`, so the anniversary is built with modifiers and compared as ISO text; pandas `DateOffset(months=t)` clips to month end.
- Everything is relative to a fixed as-of date; with `now` the numbers would change on each run.

**Follow-ups:**
- Why not use churn rate per month? That is a hazard (churned in month t divided by at risk at t), the building block of survival; it can be derived from the same table.
- Can you do it by start cohort? Group by the start month as well; small cohorts will be noisy.
- What about subscriptions with a pause or a reactivation? Not modelled; it changes the event definition (Part 7 owns streaks and islands).

**Common mistakes:**
- Dividing by all subscriptions at every t.
- Counting active subscriptions as survivors for months that have not happened.
- Using `date(start, '+t months')` without noticing the day-31 overflow.
- Using today's date instead of a fixed as-of date.

### Q45 ⭐ 🔴 Date report fault-finding drill: a monthly revenue report is wrong. List five suspects in the order you would check them (BETWEEN with timestamps, a missing month spine and LAG, a time-zone shift of the day or month boundary, text dates in mixed formats sorting wrongly, join fan-out before aggregation or a partial current month) and for each show a tiny reproducing SQLite query plus the pandas counterpart, finishing with a reconciliation query that proves monthly totals sum to the overall total.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** I check five suspects in order of how often they bite: BETWEEN with timestamps, a missing month spine with LAG, a time-zone shift of the month boundary, text dates in mixed formats, and join fan-out (plus a partial current month); then I run a reconciliation query that proves the monthly totals add up to the overall total and exposes any unassigned bucket.

**Schema and sample data:** three tiny tables. `orders` (UTC timestamps, six rows), `order_items` (orders 1 and 2 have several items, three orders have none) and `raw_orders` (four rows with mixed date formats). Convention: stored timestamps are UTC, the business month is India time (UTC+05:30, no daylight saving), no week logic, and the as-of date is fixed at 2024-04-15, so April is a partial month.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'2024-01-10 09:00:00',100),(2,'2024-01-31 14:00:00',50),(3,'2024-01-31 20:00:00',40),
  (4,'2024-03-05 10:00:00',70),(5,'2024-03-31 23:30:00',30),(6,'2024-04-02 08:00:00',20);
CREATE TABLE order_items(order_id INTEGER, sku TEXT);
INSERT INTO order_items VALUES (1,'a'),(1,'b'),(1,'c'),(2,'a'),(2,'b'),(4,'a');
CREATE TABLE raw_orders(order_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO raw_orders VALUES (1,'2024-01-05',10),(2,'2024-1-6',20),(3,'06/02/2024',30),(4,'2024-02-07',40);
```

**SQL answer:** one tiny query per suspect plus the reconciliation (`SQL_MAIN`), all in the Code block:
1. BETWEEN: `SQL_S1_BAD` and `SQL_S1_OK`.
2. Spine and LAG: `SQL_S2_BAD` and `SQL_S2_OK`.
3. Time zone: `SQL_S3_UTC` and `SQL_S3_IST`.
4. Mixed text dates: `SQL_S4_SORT` and `SQL_S4_BAD`.
5. Fan-out and partial month: `SQL_S5_BAD`, `SQL_S5_OK` and `SQL_S5_PARTIAL`.
```sql
SELECT SUM(amount) AS jan FROM orders WHERE order_ts BETWEEN '2024-01-01' AND '2024-01-31'
```
```sql
SELECT SUM(amount) AS jan FROM orders WHERE order_ts >= '2024-01-01' AND order_ts < '2024-02-01'
```
```sql
WITH m AS (SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1)
SELECT month, total, LAG(month) OVER (ORDER BY month) AS prev_month, LAG(total) OVER (ORDER BY month) AS prev_total FROM m
```
```sql
WITH RECURSIVE sp(ms) AS (SELECT '2024-01-01' UNION ALL SELECT date(ms, '+1 month') FROM sp WHERE ms < '2024-04-01'),
m AS (SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1)
SELECT strftime('%Y-%m', sp.ms) AS month, COALESCE(m.total, 0) AS total,
       LAG(COALESCE(m.total, 0)) OVER (ORDER BY sp.ms) AS prev_total
FROM sp LEFT JOIN m ON m.month = strftime('%Y-%m', sp.ms) ORDER BY sp.ms
```
```sql
SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1 ORDER BY 1
```
```sql
SELECT strftime('%Y-%m', datetime(order_ts, '+330 minutes')) AS month, SUM(amount) AS total FROM orders GROUP BY 1 ORDER BY 1
```
```sql
SELECT order_date FROM raw_orders ORDER BY order_date
```
```sql
SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total FROM raw_orders GROUP BY 1 ORDER BY 1
```
```sql
SELECT SUM(o.amount) AS total FROM orders o JOIN order_items i ON i.order_id = o.order_id
```
```sql
SELECT SUM(o.amount) AS total
FROM orders o LEFT JOIN (SELECT order_id, COUNT(*) AS n_items FROM order_items GROUP BY order_id) i ON i.order_id = o.order_id
```
```sql
SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total,
       MAX(CAST(strftime('%d', '2024-04-15') AS INTEGER)) AS days_covered
FROM orders WHERE order_ts >= '2024-04-01' AND order_ts < '2024-04-16' GROUP BY 1
```
The reconciliation, which adds an explicit bucket for unparseable months and compares the sum of the months with the overall total:
```sql
WITH m AS (
  SELECT COALESCE(strftime('%Y-%m', datetime(order_ts, '+330 minutes')), 'UNPARSED') AS month, SUM(amount) AS total
  FROM orders GROUP BY 1
)
SELECT (SELECT SUM(amount) FROM orders) AS overall, SUM(total) AS sum_of_months,
       (SELECT SUM(amount) FROM orders) - SUM(total) AS diff,
       SUM(month = 'UNPARSED') AS unparsed_buckets FROM m
```

**pandas answer:** the counterparts, in the same order (the printed lines at the end of the output give their values).
```py
o = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
items = pd.read_sql_query("SELECT * FROM order_items", con)
raw = pd.read_sql_query("SELECT * FROM raw_orders", con)
p1_bad = o.loc[o["order_ts"] <= pd.Timestamp("2024-01-31"), "amount"]             # timestamp compare loses the 31st
p1_ok = o.loc[(o["order_ts"] >= "2024-01-01") & (o["order_ts"] < "2024-02-01"), "amount"]
p1_slice = o.set_index("order_ts").sort_index().loc["2024-01-01":"2024-01-31", "amount"]   # string slice includes the whole last day
monthly = o.groupby(o["order_ts"].dt.to_period("M"))["amount"].sum()
filled = monthly.reindex(pd.period_range("2024-01", "2024-04", freq="M"), fill_value=0)
ist = o["order_ts"].dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
ist_month = o.groupby(ist.dt.strftime("%Y-%m"))["amount"].sum()
raw["d"] = pd.to_datetime(raw["order_date"], errors="coerce", format="ISO8601")
raw_month = raw.groupby(raw["d"].dt.strftime("%Y-%m"))["amount"].sum()            # NaT keys are dropped silently
raw_month_na = raw.groupby(raw["d"].dt.strftime("%Y-%m"), dropna=False)["amount"].sum()
fan = o.merge(items, on="order_id")["amount"].sum()
ok5 = o.merge(items.groupby("order_id").size().rename("n_items").reset_index(), on="order_id", how="left")["amount"].sum()
recon = (o["amount"].sum(), ist_month.sum(), o["amount"].sum() - ist_month.sum())
recon_raw = (raw["amount"].sum(), raw_month.sum(), raw["amount"].sum() - raw_month.sum())
```

**Example:** orders total 310 (100 + 50 + 40 + 70 + 30 + 20).
- Suspect 1: `BETWEEN '2024-01-01' AND '2024-01-31'` sees only order 1 (100); orders 2 and 3 are at `2024-01-31 14:00:00` and `20:00:00`, which sort after the string `2024-01-31`. The half-open range gives 190.
- Suspect 2: months with data are Jan 190, Mar 100, Apr 20; `LAG` puts January next to March (`prev_month` 2024-01), so the report says March fell by 90, when February was actually 0 and March rose by 100. With the spine February is a row of 0 and LAG for March is 0.
- Suspect 3: UTC months give 190 / 100 / 20. India time moves order 3 (UTC 01-31 20:00 = 02-01 01:30) into February and order 5 (UTC 03-31 23:30 = 04-01 05:00) into April: 150 / 40 / 70 / 50. Same grand total, different months.
- Suspect 4: `'2024-1-6'` and `'06/02/2024'` are not valid SQLite date text, so `strftime` gives NULL months (a NULL group of 50); the text sort order is `06/02/2024`, then `2024-01-05`, `2024-02-07`, `2024-1-6` (wrong order). pandas parses `'2024-1-6'` but not `'06/02/2024'`, so its monthly numbers differ from SQLite's (30 + 40 = 70 versus 10 + 40 = 50 in SQLite), and `groupby` drops the NaT key silently unless `dropna=False`.
- Suspect 5: an INNER JOIN to order_items multiplies orders 1 (3 items) and 2 (2 items) and drops the three orders without items: 3 x 100 + 2 x 50 + 70 = 470 against the true 310; pre-aggregating items before the join keeps 310. The partial month: April holds only 15 days of data (to 2024-04-15), so April revenue of 20 cannot be compared with a full month.
- Reconciliation: on `orders` (India months) overall 310, months 310, diff 0. On `raw_orders` overall 100, months 50, diff 50: the NULL-month rows are missing; pandas reports 30 missing for the same data.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q45: fault-finding drill for a wrong monthly revenue report
# Convention: orders.order_ts is UTC text 'YYYY-MM-DD HH:MM:SS'; the business month is India time (UTC+05:30, no DST).
# Fixed as-of date 2024-04-15, so April is a PARTIAL month. All amounts are toy numbers.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'2024-01-10 09:00:00',100),(2,'2024-01-31 14:00:00',50),(3,'2024-01-31 20:00:00',40),
  (4,'2024-03-05 10:00:00',70),(5,'2024-03-31 23:30:00',30),(6,'2024-04-02 08:00:00',20);
CREATE TABLE order_items(order_id INTEGER, sku TEXT);
INSERT INTO order_items VALUES (1,'a'),(1,'b'),(1,'c'),(2,'a'),(2,'b'),(4,'a');
CREATE TABLE raw_orders(order_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO raw_orders VALUES (1,'2024-01-05',10),(2,'2024-1-6',20),(3,'06/02/2024',30),(4,'2024-02-07',40);
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def q(sql, **p):
    return pd.read_sql_query(sql, con, params=p)

# Suspect 1: BETWEEN with timestamps
SQL_S1_BAD = "SELECT SUM(amount) AS jan FROM orders WHERE order_ts BETWEEN '2024-01-01' AND '2024-01-31'"
SQL_S1_OK = "SELECT SUM(amount) AS jan FROM orders WHERE order_ts >= '2024-01-01' AND order_ts < '2024-02-01'"
# Suspect 2: no month spine, LAG compares to the previous ROW
SQL_S2_BAD = """
WITH m AS (SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1)
SELECT month, total, LAG(month) OVER (ORDER BY month) AS prev_month, LAG(total) OVER (ORDER BY month) AS prev_total FROM m
"""
SQL_S2_OK = """
WITH RECURSIVE sp(ms) AS (SELECT '2024-01-01' UNION ALL SELECT date(ms, '+1 month') FROM sp WHERE ms < '2024-04-01'),
m AS (SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1)
SELECT strftime('%Y-%m', sp.ms) AS month, COALESCE(m.total, 0) AS total,
       LAG(COALESCE(m.total, 0)) OVER (ORDER BY sp.ms) AS prev_total
FROM sp LEFT JOIN m ON m.month = strftime('%Y-%m', sp.ms) ORDER BY sp.ms
"""
# Suspect 3: UTC month versus India-time month
SQL_S3_UTC = "SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1 ORDER BY 1"
SQL_S3_IST = "SELECT strftime('%Y-%m', datetime(order_ts, '+330 minutes')) AS month, SUM(amount) AS total FROM orders GROUP BY 1 ORDER BY 1"
# Suspect 4: text dates in mixed formats
SQL_S4_SORT = "SELECT order_date FROM raw_orders ORDER BY order_date"
SQL_S4_BAD = "SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total FROM raw_orders GROUP BY 1 ORDER BY 1"
# Suspect 5: join fan-out before aggregation, then the partial month
SQL_S5_BAD = "SELECT SUM(o.amount) AS total FROM orders o JOIN order_items i ON i.order_id = o.order_id"
SQL_S5_OK = """
SELECT SUM(o.amount) AS total
FROM orders o LEFT JOIN (SELECT order_id, COUNT(*) AS n_items FROM order_items GROUP BY order_id) i ON i.order_id = o.order_id
"""
SQL_S5_PARTIAL = """
SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total,
       MAX(CAST(strftime('%d', '2024-04-15') AS INTEGER)) AS days_covered
FROM orders WHERE order_ts >= '2024-04-01' AND order_ts < '2024-04-16' GROUP BY 1
"""
# Reconciliation: months (with an explicit bucket for unparseable dates) must add up to the overall total
SQL_MAIN = """
WITH m AS (
  SELECT COALESCE(strftime('%Y-%m', datetime(order_ts, '+330 minutes')), 'UNPARSED') AS month, SUM(amount) AS total
  FROM orders GROUP BY 1
)
SELECT (SELECT SUM(amount) FROM orders) AS overall, SUM(total) AS sum_of_months,
       (SELECT SUM(amount) FROM orders) - SUM(total) AS diff,
       SUM(month = 'UNPARSED') AS unparsed_buckets FROM m
"""
SQL_RECON_RAW = """
WITH m AS (SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total FROM raw_orders GROUP BY 1)
SELECT (SELECT SUM(amount) FROM raw_orders) AS overall, SUM(total) AS sum_of_months,
       (SELECT SUM(amount) FROM raw_orders) - SUM(total) AS diff FROM m WHERE month IS NOT NULL
"""
def show(title, df):
    print(f"--- {title}")
    print(df.to_string(index=False))

show("S1 BETWEEN '2024-01-01' AND '2024-01-31' (loses 31 Jan after 00:00)", q(SQL_S1_BAD))
show("S1 half-open range", q(SQL_S1_OK))
show("S2 LAG without spine (March compared with January)", q(SQL_S2_BAD))
show("S2 with spine", q(SQL_S2_OK))
show("S3 UTC month", q(SQL_S3_UTC))
show("S3 India-time month", q(SQL_S3_IST))
print("--- S4 text sort:", [r[0] for r in con.execute(SQL_S4_SORT)])
show("S4 strftime on mixed formats (NULL month = silently unassigned)", q(SQL_S4_BAD))
show("S5 INNER JOIN to order_items before SUM (multiplies orders 1 and 2, drops orders without items)", q(SQL_S5_BAD))
show("S5 pre-aggregate the many side first", q(SQL_S5_OK))
show("S5b partial month as of 2024-04-15", q(SQL_S5_PARTIAL))
show("RECONCILIATION on orders (India-time months)", q(SQL_MAIN))
show("RECONCILIATION on raw_orders (mixed formats)", q(SQL_RECON_RAW))

# --- pandas ---
o = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
items = pd.read_sql_query("SELECT * FROM order_items", con)
raw = pd.read_sql_query("SELECT * FROM raw_orders", con)
p1_bad = o.loc[o["order_ts"] <= pd.Timestamp("2024-01-31"), "amount"]             # timestamp compare loses the 31st
p1_ok = o.loc[(o["order_ts"] >= "2024-01-01") & (o["order_ts"] < "2024-02-01"), "amount"]
p1_slice = o.set_index("order_ts").sort_index().loc["2024-01-01":"2024-01-31", "amount"]   # string slice includes the whole last day
monthly = o.groupby(o["order_ts"].dt.to_period("M"))["amount"].sum()
filled = monthly.reindex(pd.period_range("2024-01", "2024-04", freq="M"), fill_value=0)
ist = o["order_ts"].dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
ist_month = o.groupby(ist.dt.strftime("%Y-%m"))["amount"].sum()
raw["d"] = pd.to_datetime(raw["order_date"], errors="coerce", format="ISO8601")
raw_month = raw.groupby(raw["d"].dt.strftime("%Y-%m"))["amount"].sum()            # NaT keys are dropped silently
raw_month_na = raw.groupby(raw["d"].dt.strftime("%Y-%m"), dropna=False)["amount"].sum()
fan = o.merge(items, on="order_id")["amount"].sum()
ok5 = o.merge(items.groupby("order_id").size().rename("n_items").reset_index(), on="order_id", how="left")["amount"].sum()
recon = (o["amount"].sum(), ist_month.sum(), o["amount"].sum() - ist_month.sum())
recon_raw = (raw["amount"].sum(), raw_month.sum(), raw["amount"].sum() - raw_month.sum())
# --- end pandas ---
assert int(p1_bad.sum()) == int(q(SQL_S1_BAD)["jan"][0]) == 100
assert int(p1_ok.sum()) == int(p1_slice.sum()) == int(q(SQL_S1_OK)["jan"][0]) == 190
assert filled.tolist() == q(SQL_S2_OK)["total"].tolist()
assert ist_month.to_dict() == dict(zip(*[q(SQL_S3_IST)[c] for c in ("month", "total")]))
assert int(fan) == int(q(SQL_S5_BAD)["total"][0]) and int(ok5) == int(q(SQL_S5_OK)["total"][0])
r = q(SQL_MAIN)
assert tuple(int(v) for v in r.iloc[0, :3]) == tuple(int(v) for v in recon)
r2 = q(SQL_RECON_RAW)
assert tuple(int(v) for v in r2.iloc[0, :3]) == (100, 50, 50)          # SQLite cannot parse two of the four dates
assert tuple(int(v) for v in recon_raw) == (100, 70, 30)               # pandas parses '2024-1-6' but not '06/02/2024'
print("\npandas equals SQL on suspects 1, 2, 3, 5 and both reconciliations on orders: OK; suspect 4 differs by design (see below)")
print("\npandas:")
print(" S1 <= Timestamp('2024-01-31'):", int(p1_bad.sum()), "| half-open:", int(p1_ok.sum()), "| .loc['2024-01-01':'2024-01-31']:", int(p1_slice.sum()))
print(" S2 monthly totals reindexed with fill_value=0:", filled.to_dict())
print(" S3 India-time months:", ist_month.to_dict())
print(" S4 parsed dates (errors='coerce', format='ISO8601'):", raw["d"].astype(str).tolist())
print(" S4 groupby months:", raw_month.to_dict(), "| with dropna=False:", raw_month_na.to_dict())
print(" S5 merge then sum:", int(fan), "| without the merge:", int(ok5))
print(" reconciliation orders:", tuple(int(v) for v in recon), "| raw_orders:", tuple(int(v) for v in recon_raw))
```

**Output (my run):**
```text
--- S1 BETWEEN '2024-01-01' AND '2024-01-31' (loses 31 Jan after 00:00)
 jan
 100
--- S1 half-open range
 jan
 190
--- S2 LAG without spine (March compared with January)
  month  total prev_month  prev_total
2024-01    190        NaN         NaN
2024-03    100    2024-01       190.0
2024-04     20    2024-03       100.0
--- S2 with spine
  month  total  prev_total
2024-01    190         NaN
2024-02      0       190.0
2024-03    100         0.0
2024-04     20       100.0
--- S3 UTC month
  month  total
2024-01    190
2024-03    100
2024-04     20
--- S3 India-time month
  month  total
2024-01    150
2024-02     40
2024-03     70
2024-04     50
--- S4 text sort: ['06/02/2024', '2024-01-05', '2024-02-07', '2024-1-6']
--- S4 strftime on mixed formats (NULL month = silently unassigned)
  month  total
    NaN     50
2024-01     10
2024-02     40
--- S5 INNER JOIN to order_items before SUM (multiplies orders 1 and 2, drops orders without items)
 total
   470
--- S5 pre-aggregate the many side first
 total
   310
--- S5b partial month as of 2024-04-15
  month  total  days_covered
2024-04     20            15
--- RECONCILIATION on orders (India-time months)
 overall  sum_of_months  diff  unparsed_buckets
     310            310     0                 0
--- RECONCILIATION on raw_orders (mixed formats)
 overall  sum_of_months  diff
     100             50    50

pandas equals SQL on suspects 1, 2, 3, 5 and both reconciliations on orders: OK; suspect 4 differs by design (see below)

pandas:
 S1 <= Timestamp('2024-01-31'): 100 | half-open: 190 | .loc['2024-01-01':'2024-01-31']: 190
 S2 monthly totals reindexed with fill_value=0: {Period('2024-01', 'M'): 190, Period('2024-02', 'M'): 0, Period('2024-03', 'M'): 100, Period('2024-04', 'M'): 20}
 S3 India-time months: {'2024-01': 150, '2024-02': 40, '2024-03': 70, '2024-04': 50}
 S4 parsed dates (errors='coerce', format='ISO8601'): ['2024-01-05', '2024-01-06', nan, '2024-02-07']
 S4 groupby months: {'2024-01': 30, '2024-02': 40} | with dropna=False: {'2024-01': 30, '2024-02': 40, nan: 30}
 S5 merge then sum: 470 | without the merge: 310
 reconciliation orders: (310, 310, 0) | raw_orders: (100, 70, 30)
```

**Edge cases:**
- The reconciliation catches lost or inflated rows (suspects 1, 4, 5) but not a shifted month (suspect 3, the sums still match) or a missing spine month (suspect 2); those need their own checks (compare the month list with the calendar, compare against a second source).
- Pandas partial-string slicing includes the whole last day (`.loc['2024-01-01':'2024-01-31']` gave 190), unlike `<= Timestamp('2024-01-31')` (100). That is a pandas versus plain comparison difference worth knowing.
- `groupby` on NaT keys drops them by default (the dropped 30 reappears with `dropna=False`); a SQL `GROUP BY` keeps the NULL group. The two tools fail differently.
- `fill_value=0` on `reindex` creates the zero months in pandas (the equivalent of the spine).
- Fixed as-of date: the partial-month flag compares the as-of day with the days in the month; with `now` the report changes on each run.
- The tz conversion used `Asia/Kolkata`, which has no DST; a zone with DST needs the offset table or a library (Q38).

**Then explain:**
- Order of suspicion: cheap and common first. Boundary filters and text dates produce silent row loss; the spine and the zone produce correct totals in the wrong months; fan-out produces a total that is too large.
- Reconcile first, localise second: if the monthly sum equals the overall total, rows are not lost or duplicated in the aggregation, and the problem is assignment (month, zone).
- State the grain of each table before joining; aggregate the many side first.
- Keep an explicit bucket for rows that do not parse so that they show up instead of disappearing.

**Follow-ups:**
- How would you prove a fix? Re-run the reconciliation, then compare to an independent total (finance ledger, raw table counts).
- How do you prevent the bug? Constraints and checks on load (date format, uniqueness), tests on reconciliation, a calendar table.
- What if the report is MoM? Complete the spine before `LAG` and compare like for like (partial months excluded).

**Common mistakes:**
- Trusting a report because the total looks plausible.
- Fixing one suspect and not re-reconciling.
- Using `BETWEEN` for timestamps, and `LAG` on sparse months.
- Ignoring NULL groups and dropped NaT keys.


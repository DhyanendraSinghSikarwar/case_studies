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

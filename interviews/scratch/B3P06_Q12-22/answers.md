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

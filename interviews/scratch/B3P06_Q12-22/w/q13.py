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

# Q32: sample ratio mismatch as counts: distinct users per arm, expected, difference, chi-square arithmetic
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE experiments(user_id INTEGER, arm TEXT, assigned_ts TEXT);
INSERT INTO experiments VALUES
 (1,'control','2024-03-01 09:00:00'),(2,'control','2024-03-01 09:01:00'),(2,'control','2024-03-02 09:00:00'),
 (3,'control','2024-03-01 09:02:00'),(4,'control','2024-03-01 09:03:00'),(5,'control','2024-03-01 09:04:00'),
 (6,'control','2024-03-01 09:05:00'),(7,'control','2024-03-01 09:06:00'),(8,'control','2024-03-01 09:07:00'),
 (9,'control','2024-03-01 09:08:00'),
 (10,'treatment','2024-03-01 09:09:00'),(11,'treatment','2024-03-01 09:10:00'),(11,'treatment','2024-03-03 09:00:00'),
 (12,'treatment','2024-03-01 09:11:00'),(13,'treatment','2024-03-01 09:12:00'),
 (14,'control','2024-03-01 09:13:00'),(14,'treatment','2024-03-02 09:13:00');
"""

# planned split is a parameter table; chi-square = sum over arms of (observed - expected)^2 / expected
SQL_MAIN = """
WITH plan(arm, planned) AS (VALUES ('control', 0.5), ('treatment', 0.5)),
obs AS (
  SELECT arm, COUNT(DISTINCT user_id) AS users FROM experiments GROUP BY arm
), tot AS (SELECT SUM(users) AS n FROM obs),
x AS (
  SELECT p.arm, o.users, o.users * 1.0 / t.n AS observed_share, p.planned * t.n AS expected,
         o.users - p.planned * t.n AS diff,
         (o.users - p.planned * t.n) * (o.users - p.planned * t.n) / (p.planned * t.n) AS chi_part
  FROM plan p JOIN obs o ON o.arm = p.arm CROSS JOIN tot t
)
SELECT arm, users, ROUND(observed_share, 4) AS observed_share, expected, diff,
       ROUND(chi_part, 4) AS chi_part, ROUND((SELECT SUM(chi_part) FROM x), 4) AS chi_square
FROM x ORDER BY arm
"""
# the same arithmetic on rows, to show the wrong counting unit
SQL_ROWS = SQL_MAIN.replace("COUNT(DISTINCT user_id)", "COUNT(*)")
assert SQL_ROWS != SQL_MAIN
SQL_BOTH = """
SELECT user_id, COUNT(DISTINCT arm) AS arms, COUNT(*) AS rows_
FROM experiments GROUP BY user_id HAVING COUNT(DISTINCT arm) > 1
"""
SQL_DUP = """
SELECT COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS distinct_users,
       (SELECT COUNT(*) FROM (SELECT user_id FROM experiments GROUP BY user_id HAVING COUNT(*) > 1)) AS users_with_repeat_rows
FROM experiments
"""
# clean: users that appear in exactly one arm
SQL_CLEAN = SQL_MAIN.replace("FROM experiments GROUP BY arm",
    "FROM experiments WHERE user_id NOT IN (SELECT user_id FROM experiments GROUP BY user_id HAVING COUNT(DISTINCT arm) > 1) GROUP BY arm")
assert SQL_CLEAN != SQL_MAIN

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL, distinct users per arm (users in both arms counted in each arm):")
print(sql_main.to_string(index=False))
print("SQL, same arithmetic on rows (wrong unit):")
print(pd.read_sql_query(SQL_ROWS, con).to_string(index=False))
print("SQL, after removing users that appear in both arms:")
sql_clean = pd.read_sql_query(SQL_CLEAN, con)
print(sql_clean.to_string(index=False))
print("users in both arms:")
print(pd.read_sql_query(SQL_BOTH, con).to_string(index=False))
print("row versus distinct counts:")
print(pd.read_sql_query(SQL_DUP, con).to_string(index=False))

exp = pd.read_sql_query("SELECT * FROM experiments", con)

# pd:main
def srm_counts(exp, planned={"control": 0.5, "treatment": 0.5}, clean=False):
    e = exp
    if clean:
        arms_per_user = e.groupby("user_id")["arm"].nunique()
        e = e[~e["user_id"].isin(arms_per_user[arms_per_user > 1].index)]
    obs = e.groupby("arm")["user_id"].nunique().rename("users").reset_index()
    n = obs["users"].sum()
    obs["planned"] = obs["arm"].map(planned)
    obs["observed_share"] = (obs["users"] / n).round(4)
    obs["expected"] = obs["planned"] * n
    obs["diff"] = obs["users"] - obs["expected"]
    chi_part = obs["diff"] ** 2 / obs["expected"]
    obs["chi_part"] = chi_part.round(4)
    obs["chi_square"] = round(float(chi_part.sum()), 4)
    return obs[["arm", "users", "observed_share", "expected", "diff", "chi_part", "chi_square"]]
# pd:end

pd_main = srm_counts(exp)
pd_clean = srm_counts(exp, clean=True)
# compare after sorting by arm (SQL ORDER BY arm)
pd.testing.assert_frame_equal(pd_main.sort_values("arm").reset_index(drop=True), sql_main, check_dtype=False)
pd.testing.assert_frame_equal(pd_clean.sort_values("arm").reset_index(drop=True), sql_clean, check_dtype=False)

# the same query on a generated table: 10,000 control and 10,600 treatment users (arithmetic at scale)
con.execute("DELETE FROM experiments")
con.executemany("INSERT INTO experiments VALUES (?, ?, '2024-03-01 00:00:00')",
                [(i, "control") for i in range(1, 10001)] + [(i, "treatment") for i in range(10001, 20601)])
big = pd.read_sql_query(SQL_MAIN, con)
print("generated 10,000 vs 10,600 users:")
print(big.to_string(index=False))
pd.testing.assert_frame_equal(srm_counts(pd.read_sql_query("SELECT * FROM experiments", con))
                              .sort_values("arm").reset_index(drop=True), big, check_dtype=False)
print("asserts passed")

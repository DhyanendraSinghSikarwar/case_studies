# Q32: SCD range collapse from daily plan snapshots, SQL + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE plan_snapshot(customer_id TEXT, snapshot_date TEXT, plan TEXT);
INSERT INTO plan_snapshot VALUES
 ('C1','2024-03-04','premium'),('C1','2024-03-01','basic'),('C1','2024-03-02','basic'),('C1','2024-03-02','basic'),
 ('C1','2024-03-03','basic'),('C1','2024-03-05','premium'),('C1','2024-03-06','premium'),
 ('C1','2024-03-07','basic'),('C1','2024-03-08','basic'),('C1','2024-03-09','basic'),('C1','2024-03-10','basic'),
 ('C2','2024-03-01','premium'),('C2','2024-03-02','premium'),
 ('C2','2024-03-04','premium'),('C2','2024-03-05','premium'),
 ('C3','2024-03-10','basic'),
 ('C4','2024-03-01','basic'),('C4','2024-03-02','basic'),('C4','2024-03-03','basic'),
 ('C5','2024-03-01','basic'),('C5','2024-03-02',NULL),('C5','2024-03-03',NULL),('C5','2024-03-04','basic');
"""
SQL_MAIN = """
WITH s AS (
  SELECT DISTINCT customer_id, snapshot_date, plan FROM plan_snapshot
),
f AS (
  SELECT *,
         CASE WHEN LAG(snapshot_date) OVER w IS NULL OR plan IS NOT LAG(plan) OVER w
              THEN 1 ELSE 0 END AS chg
  FROM s
  WINDOW w AS (PARTITION BY customer_id ORDER BY snapshot_date)
),
g AS (
  SELECT *, SUM(chg) OVER (PARTITION BY customer_id ORDER BY snapshot_date) AS grp
  FROM f
)
SELECT customer_id, plan,
       MIN(snapshot_date) AS valid_from,
       CASE WHEN MAX(snapshot_date) = '2024-03-10' THEN NULL ELSE MAX(snapshot_date) END AS valid_to
FROM g
GROUP BY customer_id, grp
ORDER BY customer_id, valid_from
"""
SQL_STRICT = """
WITH s AS (
  SELECT DISTINCT customer_id, snapshot_date, plan FROM plan_snapshot
),
f AS (
  SELECT *,
         CASE WHEN LAG(snapshot_date) OVER w IS NULL
                OR plan IS NOT LAG(plan) OVER w
                OR julianday(snapshot_date) - julianday(LAG(snapshot_date) OVER w) > 1
              THEN 1 ELSE 0 END AS chg
  FROM s
  WINDOW w AS (PARTITION BY customer_id ORDER BY snapshot_date)
),
g AS (
  SELECT *, SUM(chg) OVER (PARTITION BY customer_id ORDER BY snapshot_date) AS grp
  FROM f
)
SELECT customer_id, plan,
       MIN(snapshot_date) AS valid_from,
       CASE WHEN MAX(snapshot_date) = '2024-03-10' THEN NULL ELSE MAX(snapshot_date) END AS valid_to
FROM g
GROUP BY customer_id, grp
ORDER BY customer_id, valid_from
"""
SQL_WRONG = """
SELECT customer_id, plan, MIN(snapshot_date) AS valid_from, MAX(snapshot_date) AS valid_to
FROM (SELECT DISTINCT customer_id, snapshot_date, plan FROM plan_snapshot)
GROUP BY customer_id, plan
ORDER BY customer_id, valid_from
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL main (missing day does not break the range):")
print(sql_df.to_string(index=False))
print("SQL strict (a missing snapshot day breaks the range):")
print(pd.read_sql_query(SQL_STRICT, con).to_string(index=False))
print("wrong: GROUP BY customer_id, plan merges basic, premium, basic:")
print(pd.read_sql_query(SQL_WRONG, con).query("customer_id == 'C1'").to_string(index=False))

snap = pd.read_sql_query("SELECT * FROM plan_snapshot", con)
AS_OF = "2024-03-10"
# pd:main
s = snap.drop_duplicates().sort_values(["customer_id", "snapshot_date"]).reset_index(drop=True)
prev = s.groupby("customer_id")["plan"].shift()
first = s.groupby("customer_id").cumcount() == 0
same = (s["plan"] == prev) | (s["plan"].isna() & prev.isna())
s["grp"] = (first | ~same).groupby(s["customer_id"]).cumsum()
pd_df = (s.groupby(["customer_id", "grp"], as_index=False)
          .agg(plan=("plan", "first"), valid_from=("snapshot_date", "min"), valid_to=("snapshot_date", "max")))
pd_df["valid_to"] = pd_df["valid_to"].where(pd_df["valid_to"] != AS_OF, None)
pd_df = pd_df.drop(columns="grp").sort_values(["customer_id", "valid_from"]).reset_index(drop=True)
# pd:end
print("pandas:")
print(pd_df.to_string(index=False))
# compare after sorting by customer_id, valid_from; NULL and None both mapped to the text OPEN
norm = lambda d: d.fillna({"valid_to": "OPEN", "plan": "NULLPLAN"}).astype(str).reset_index(drop=True)
assert norm(pd_df).equals(norm(sql_df))
print("asserts passed")

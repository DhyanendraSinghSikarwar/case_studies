# Q36: top 10 percent of customers by spend: CUME_DIST vs PERCENT_RANK vs NTILE(10) vs RANK <= ceil(n/10)
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES
 (1,'C01'),(2,'C02'),(3,'C03'),(4,'C04'),(5,'C05'),(6,'C06'),(7,'C07'),(8,'C08'),(9,'C09'),(10,'C10'),(11,'C11'),(12,'C12'),(13,'C13'),(14,'C14'),(15,'C15'),(16,'C16'),(17,'C17'),(18,'C18'),(19,'C19'),(20,'C20'),(21,'C21'),(22,'C22'),(23,'C23'),(24,'C24'),(25,'C25');
INSERT INTO orders VALUES
 (1,1,3000),(2,1,2000),(3,2,4800),(4,3,4400),(5,4,4400),(6,5,4000),(7,6,3500),(8,7,3000),(9,8,2800),(10,9,2600),(11,10,2500),(12,11,2400),(13,12,2200),(14,13,2000),(15,14,1800),(16,15,1600),(17,16,1500),(18,17,1400),(19,18,1200),(20,19,1000),(21,20,900),(22,21,800),(23,22,600),(24,23,500),(25,24,400);
"""
SQL_MAIN = """
WITH spend AS (
  SELECT c.customer_id, COALESCE(SUM(o.amount), 0) AS total
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id),
scored AS (
  SELECT customer_id, total,
         CUME_DIST()    OVER (ORDER BY total DESC)                  AS cd,
         PERCENT_RANK() OVER (ORDER BY total DESC)                  AS pr,
         NTILE(10)      OVER (ORDER BY total DESC, customer_id)     AS nt,
         RANK()         OVER (ORDER BY total DESC)                  AS rk,
         COUNT(*)       OVER ()                                     AS n
  FROM spend)
SELECT customer_id, total, cd, pr, nt, rk,
       cd <= 0.10                 AS in_cume,
       pr <= 0.10                 AS in_prank,
       nt = 1                     AS in_ntile,
       rk <= (n + 9) / 10         AS in_rank
FROM scored
ORDER BY total DESC, customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL, top 7 rows:"); print(sql_df.head(7).round(4).to_string(index=False))
flags = ["in_cume", "in_prank", "in_ntile", "in_rank"]
print("\nSQL rows selected per rule (n = %d):" % len(sql_df), {f: int(sql_df[f].sum()) for f in flags})
for f in flags:
    print(f"  {f:9s}", sql_df.loc[sql_df[f] == 1, "customer_id"].tolist())

cust = pd.read_sql_query("SELECT customer_id FROM customers", con)
ords = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
tot = (cust.merge(ords.groupby("customer_id", as_index=False)["amount"].sum(), on="customer_id", how="left")
           .fillna({"amount": 0}).rename(columns={"amount": "total"}))
tot = tot.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
n = len(tot)
tot["cd"] = tot["total"].rank(method="max", ascending=False, pct=True)           # = CUME_DIST
rmin = tot["total"].rank(method="min", ascending=False)
tot["pr"] = (rmin - 1) / (n - 1)                                                  # = PERCENT_RANK
q, r = divmod(n, 10)
pos = np.arange(1, n + 1)                                                         # rows are already in NTILE order
big = r * (q + 1)
tot["nt"] = np.where(pos <= big, np.ceil(pos / (q + 1)), r + np.ceil((pos - big) / q)).astype("int64")
tot["rk"] = rmin.astype("int64")
tot["in_cume"] = tot["cd"] <= 0.10
tot["in_prank"] = tot["pr"] <= 0.10
tot["in_ntile"] = tot["nt"] == 1
tot["in_rank"] = tot["rk"] <= (n + 9) // 10
# pd:end
pct_default = tot["total"].rank(ascending=False, pct=True)                        # default method='average'
qc = pd.qcut(tot["total"], 10, labels=False)
print("\npandas selected per rule:", {f: int(tot[f].sum()) for f in flags},
      "| qcut(total, 10) top bin (label 9):", int((qc == 9).sum()))
print("pandas pct=True default method='average' for ids 3,4 (tied 4400):",
      pct_default[tot.customer_id.isin([3, 4])].round(4).tolist(), "vs method='max':",
      tot.loc[tot.customer_id.isin([3, 4]), "cd"].round(4).tolist())
# compared after sorting both by customer_id
a = sql_df.sort_values("customer_id").reset_index(drop=True)
b = tot.rename(columns={}).sort_values("customer_id").reset_index(drop=True)
for col in ["total", "cd", "pr", "nt", "rk"]:
    pd.testing.assert_series_equal(a[col].astype(float), b[col].astype(float), check_names=False, check_dtype=False)
for col in flags:
    assert a[col].astype(bool).tolist() == b[col].tolist(), col
print("asserts passed: SQL CUME_DIST/PERCENT_RANK/NTILE/RANK columns and flags == pandas versions")

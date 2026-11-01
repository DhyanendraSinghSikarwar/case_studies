# Q32: one CTE referenced several times vs the same derived table repeated; MATERIALIZED hints; pandas intermediate
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO sales VALUES
 (1,'North',100),(2,'North',50),(3,'South',80),(4,'East',200),
 (5,'West',40),(6,'West',20),(7,'West',10);
"""
SQL_MAIN = """
WITH region_totals AS (
  SELECT region, SUM(amount) AS total FROM sales GROUP BY region
)
SELECT region, total,
       (SELECT AVG(total) FROM region_totals) AS avg_total,
       (SELECT MAX(total) FROM region_totals) AS best_total
FROM region_totals
WHERE total > (SELECT AVG(total) FROM region_totals)
ORDER BY total DESC, region
"""
SQL_DERIVED = """
SELECT t.region, t.total,
       (SELECT AVG(total) FROM (SELECT region, SUM(amount) AS total FROM sales GROUP BY region)) AS avg_total,
       (SELECT MAX(total) FROM (SELECT region, SUM(amount) AS total FROM sales GROUP BY region)) AS best_total
FROM (SELECT region, SUM(amount) AS total FROM sales GROUP BY region) t
WHERE t.total > (SELECT AVG(total) FROM (SELECT region, SUM(amount) AS total FROM sales GROUP BY region))
ORDER BY t.total DESC, t.region
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL with one CTE referenced 4 times:")
print(sql_df.to_string(index=False))
der_df = pd.read_sql_query(SQL_DERIVED, con)
pd.testing.assert_frame_equal(sql_df, der_df)
print("\nassert: CTE version == derived table written out 4 times (same rows, same order)")

print("\nEXPLAIN QUERY PLAN, CTE version:")
for r in con.execute("EXPLAIN QUERY PLAN " + SQL_MAIN):
    print("  ", r[3])
for hint in ["MATERIALIZED", "NOT MATERIALIZED"]:
    q = SQL_MAIN.replace("AS (\n  SELECT region", "AS %s (\n  SELECT region" % hint)
    assert hint in q
    res = con.execute(q).fetchall()
    plan = [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + q)]
    print("\n%s hint parses on SQLite 3.45: rows=%s" % (hint, res))
    print("   plan:", plan)

sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:main
region_totals = sales.groupby("region", as_index=False).agg(total=("amount", "sum"))
avg_total = region_totals["total"].mean()
best_total = region_totals["total"].max()
pd_df = (region_totals[region_totals["total"] > avg_total]
         .assign(avg_total=avg_total, best_total=best_total)
         .sort_values(["total", "region"], ascending=[False, True])
         .reset_index(drop=True))
# pd:end
print("\npandas:")
print(pd_df.to_string(index=False))
# compared in the printed order (total DESC, region)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\nassert: SQL == pandas")
print("all region totals:", dict(zip(region_totals.region, region_totals.total)), "| average", avg_total)

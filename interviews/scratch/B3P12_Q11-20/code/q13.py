# Q13: first date running stock fell below zero, and lowest running stock, per sku
import sqlite3
import pandas as pd

def norm(df):
    return df.astype(object).where(df.notna(), None)

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE inventory_moves(move_id INTEGER PRIMARY KEY, sku TEXT, move_date TEXT, qty_change INTEGER);
INSERT INTO inventory_moves VALUES
 (1,'A','2025-01-01',10),(2,'A','2025-01-02',-4),(3,'A','2025-01-02',-8),(4,'A','2025-01-03',20),
 (5,'B','2025-01-01',5),(6,'B','2025-01-02',-7),(7,'B','2025-01-02',10),
 (8,'C','2025-01-01',3),(9,'C','2025-01-02',-3);
""")
sql = """
WITH r AS (
  SELECT sku, move_date,
         SUM(qty_change) OVER (PARTITION BY sku ORDER BY move_date, move_id
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS stock
  FROM inventory_moves)
SELECT sku, MIN(CASE WHEN stock < 0 THEN move_date END) AS first_negative_date, MIN(stock) AS lowest_stock
FROM r GROUP BY sku ORDER BY sku
"""
eod = """
WITH d AS (SELECT sku, move_date, SUM(qty_change) AS day_qty FROM inventory_moves GROUP BY sku, move_date),
r AS (SELECT sku, move_date, SUM(day_qty) OVER (PARTITION BY sku ORDER BY move_date ROWS UNBOUNDED PRECEDING) AS stock FROM d)
SELECT sku, MIN(CASE WHEN stock < 0 THEN move_date END) AS first_negative_date, MIN(stock) AS lowest_stock
FROM r GROUP BY sku ORDER BY sku
"""
a = pd.read_sql(sql, con)
print("SQL (running stock per move, ties by move_id)"); print(a.to_string(index=False))
print("\nSQL end-of-day variant (not the answer)"); print(pd.read_sql(eod, con).to_string(index=False))

m = pd.read_sql("SELECT * FROM inventory_moves", con).sort_values(["sku", "move_date", "move_id"])
m["stock"] = m.groupby("sku")["qty_change"].cumsum()
first_neg = m[m.stock < 0].groupby("sku")["move_date"].min().rename("first_negative_date")
low = m.groupby("sku")["stock"].min().rename("lowest_stock")
p = pd.concat([first_neg, low], axis=1).reset_index().sort_values("sku").reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(norm(a), norm(p), check_dtype=False)
print("\nassert passed: equal, rows ordered by sku (NULL and NaN normalised to None before comparing)")

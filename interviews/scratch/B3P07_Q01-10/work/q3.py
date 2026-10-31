# Q3: missing ids and gaps: LEAD/LAG test next - current > 1, and NOT EXISTS against a number spine
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE invoices(invoice_no INTEGER);
INSERT INTO invoices VALUES (15),(2),(1),(7),(10),(3),(8);
"""
SQL_MAIN = """
WITH x AS (
  SELECT invoice_no,
         LEAD(invoice_no) OVER (ORDER BY invoice_no) AS next_no
  FROM invoices
  WHERE invoice_no IS NOT NULL
)
SELECT invoice_no + 1 AS gap_start,
       next_no - 1   AS gap_end
FROM x
WHERE next_no - invoice_no > 1
ORDER BY gap_start
"""
SQL_LAG = """
WITH x AS (
  SELECT invoice_no,
         LAG(invoice_no) OVER (ORDER BY invoice_no) AS prev_no
  FROM invoices
  WHERE invoice_no IS NOT NULL
)
SELECT prev_no + 1 AS gap_start,
       invoice_no - 1 AS gap_end
FROM x
WHERE invoice_no - prev_no > 1
ORDER BY gap_start
"""
SQL_LAG_FROM_ONE = """
WITH x AS (
  SELECT invoice_no,
         COALESCE(LAG(invoice_no) OVER (ORDER BY invoice_no), 0) AS prev_no
  FROM invoices
  WHERE invoice_no IS NOT NULL
)
SELECT prev_no + 1 AS gap_start,
       invoice_no - 1 AS gap_end
FROM x
WHERE invoice_no - prev_no > 1
ORDER BY gap_start
"""
SQL_SPINE = """
WITH RECURSIVE spine(n) AS (
  SELECT MIN(invoice_no) FROM invoices
  UNION ALL
  SELECT n + 1 FROM spine WHERE n < (SELECT MAX(invoice_no) FROM invoices)
)
SELECT n AS missing_no
FROM spine s
WHERE NOT EXISTS (SELECT 1 FROM invoices i WHERE i.invoice_no = s.n)
ORDER BY n
"""
SQL_SPINE_RANGES = """
WITH RECURSIVE spine(n) AS (
  SELECT MIN(invoice_no) FROM invoices
  UNION ALL
  SELECT n + 1 FROM spine WHERE n < (SELECT MAX(invoice_no) FROM invoices)
),
missing AS (
  SELECT n FROM spine s
  WHERE NOT EXISTS (SELECT 1 FROM invoices i WHERE i.invoice_no = s.n)
),
y AS (
  SELECT n, n - ROW_NUMBER() OVER (ORDER BY n) AS grp FROM missing
)
SELECT MIN(n) AS gap_start, MAX(n) AS gap_end
FROM y
GROUP BY grp
ORDER BY gap_start
"""

def pd_gaps(inv):
    # pd:main
    s = inv["invoice_no"].dropna().astype("int64").sort_values().reset_index(drop=True)
    nxt = s.shift(-1)
    mask = (nxt - s) > 1
    pd_df = pd.DataFrame({"gap_start": s[mask] + 1, "gap_end": (nxt[mask] - 1).astype("int64")}).reset_index(drop=True)
    # pd:end
    return pd_df

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("LEAD version (gap ranges):")
print(sql_df.to_string(index=False))
lag_df = pd.read_sql_query(SQL_LAG, con)
pd.testing.assert_frame_equal(lag_df, sql_df)
print("LAG version equals LEAD version: True")
print("\nnumber spine + NOT EXISTS (single missing numbers):", [r[0] for r in con.execute(SQL_SPINE)])
spine_ranges = pd.read_sql_query(SQL_SPINE_RANGES, con)
pd.testing.assert_frame_equal(spine_ranges, sql_df)
print("spine singles re-grouped into ranges equals LEAD version: True")

inv = pd.read_sql_query("SELECT * FROM invoices", con)
pd_df = pd_gaps(inv)
# compared after sorting by gap_start (SQL ORDER BY gap_start; pandas input sorted by invoice_no)
pd.testing.assert_frame_equal(pd_df, sql_df)
print("pandas equals SQL: True")
s = inv["invoice_no"].sort_values().reset_index(drop=True)
print("shift(-1) dtype:", s.shift(-1).dtype, "| last value:", s.shift(-1).iloc[-1])
spine = pd.Series(range(int(s.min()), int(s.max()) + 1))
print("pandas spine, missing singles:", spine[~spine.isin(s)].tolist())

# edge cases
con.executescript("""
CREATE TABLE inv_b(invoice_no INTEGER);
INSERT INTO inv_b VALUES (3),(4),(6);
""")
print("\nnumbering should start at 1, table 3,4,6:")
print("  plain LAG (first row dropped):", con.execute(SQL_LAG.replace("FROM invoices", "FROM inv_b")).fetchall())
print("  COALESCE(LAG, 0):", con.execute(SQL_LAG_FROM_ONE.replace("FROM invoices", "FROM inv_b")).fetchall())
con.execute("INSERT INTO invoices VALUES (7)")
print("duplicate 7 added, LEAD version unchanged:", pd.read_sql_query(SQL_MAIN, con).equals(sql_df))
con.execute("INSERT INTO invoices VALUES (NULL)")
print("NULL added (filtered out), LEAD version unchanged:", pd.read_sql_query(SQL_MAIN, con).equals(sql_df))
nul = con.execute(SQL_MAIN.replace("  WHERE invoice_no IS NOT NULL\n", "")).fetchall()
print("NULL added, filter removed:", nul)
con.execute("DELETE FROM invoices")
print("empty table, LEAD rows:", con.execute(SQL_MAIN).fetchall())
print("empty table, spine rows:", con.execute(SQL_SPINE).fetchall())
con.execute("INSERT INTO invoices VALUES (5)")
print("single row, LEAD rows:", con.execute(SQL_MAIN).fetchall())
print("asserts passed")

# Q16: SQLite has no PIVOT: SUM(CASE), FILTER, a generated (dynamic) pivot, and pandas
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','Pen','Jan',100),('East','Pen','Jan',50),('East','Book','Feb',200),
 ('West','Pen','Feb',70),('West','Book','Mar',30),('North','Pen','Jan',10);
""")
print("SQLite", sqlite3.sqlite_version)
try:
    con.execute("SELECT * FROM sales PIVOT (SUM(amount) FOR month IN ('Jan','Feb','Mar'))")
except sqlite3.Error as e:
    print("PIVOT keyword in SQLite ->", type(e).__name__ + ":", e)

SQL_CASE = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
SQL_FILTER = """
SELECT region,
       SUM(amount) FILTER (WHERE month = 'Jan') AS Jan,
       SUM(amount) FILTER (WHERE month = 'Feb') AS Feb,
       SUM(amount) FILTER (WHERE month = 'Mar') AS Mar
FROM sales GROUP BY region ORDER BY region
"""
case_df = pd.read_sql_query(SQL_CASE, con)
filter_df = pd.read_sql_query(SQL_FILTER, con)
print("\nSUM(CASE ...) pivot:"); print(case_df.to_string(index=False))
pd.testing.assert_frame_equal(case_df, filter_df)
print("FILTER (WHERE ...) form returns the identical table")

MONTHS = ["Jan", "Feb", "Mar"]
sales = pd.read_sql_query("SELECT * FROM sales", con)
p = (sales.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
          .reindex(columns=MONTHS).reset_index())
p.columns.name = None
pd.testing.assert_frame_equal(p, case_df, check_dtype=False)
print("pandas pivot_table equals the SQL pivot (rows by region, columns Jan Feb Mar)")

# a new month arrives: the fixed IN list silently ignores it
con.execute("INSERT INTO sales VALUES ('East','Pen','Apr',500)")
fixed_total = pd.read_sql_query(SQL_CASE, con)[["Jan", "Feb", "Mar"]].sum().sum()
real_total = con.execute("SELECT SUM(amount) FROM sales").fetchone()[0]
print("\nafter inserting an Apr row: pivot columns add up to", fixed_total, "but SUM(amount) is", real_total)
print("audit query, months the fixed pivot does not cover:",
      con.execute("SELECT month, SUM(amount) FROM sales WHERE month NOT IN ('Jan','Feb','Mar') GROUP BY month").fetchall())

def build_pivot_sql(con):
    # month values come from the data; quote them as literals ('' doubling) and as identifiers ("" doubling)
    months = [r[0] for r in con.execute(
        "SELECT DISTINCT month FROM sales WHERE month IS NOT NULL "
        "ORDER BY INSTR('JanFebMarAprMayJunJulAugSepOctNovDec', month)")]
    lit = lambda v: "'" + v.replace("'", "''") + "'"
    ident = lambda v: '"' + v.replace('"', '""') + '"'
    cols = ",\n       ".join(f"SUM(CASE WHEN month = {lit(m)} THEN amount END) AS {ident(m)}" for m in months)
    return f"SELECT region,\n       {cols}\nFROM sales GROUP BY region ORDER BY region", months
dyn_sql, months_now = build_pivot_sql(con)
print("\ngenerated SQL text:"); print(dyn_sql)
dyn_df = pd.read_sql_query(dyn_sql, con)
print(dyn_df.to_string(index=False))
sales2 = pd.read_sql_query("SELECT * FROM sales", con)
p2 = (sales2.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
            .reindex(columns=months_now).reset_index())
p2.columns.name = None
pd.testing.assert_frame_equal(p2, dyn_df, check_dtype=False)
assert months_now == ["Jan", "Feb", "Mar", "Apr"]
print("generated pivot equals pandas pivot_table with Apr included (rows by region)")

# a hostile value is neutralised by the quoting
con.execute("INSERT INTO sales VALUES ('East','Pen','X'' OR 1=1 --',1)")
hostile_sql, _ = build_pivot_sql(con)
pd.read_sql_query(hostile_sql, con)
print("month value with a quote still produces valid SQL:")
print(next(l for l in hostile_sql.splitlines() if "1=1" in l).strip())

try:
    con.execute("SELECT region, SUM(amount) FROM sales GROUP BY GROUPING SETS ((region), ())")
except sqlite3.Error as e:
    print("GROUPING SETS in SQLite ->", type(e).__name__ + ":", e)

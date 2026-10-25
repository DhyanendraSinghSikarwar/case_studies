# Dynamic pivot: the column list comes from the data, so the application generates the SQL text.
import re
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('North','pen','2024-01',10),('North','pen','2024-02',20),('North','ink','2024-03',5),
 ('North','pen','2024-04',7), ('South','pen','2024-02',30),('South','ink','2024-04',8),
 ('South','ink',NULL,4),      ('South','pen','',6),
 ('East', 'pen','2023-12',9), ('East', 'ink','2024-04',1),
 ('East', 'pen','x''; DROP TABLE sales;--',2);
""")

def quote_ident(name):                       # identifier quoting: wrap in double quotes, double any inner quote
    return '"' + name.replace('"', '""') + '"'

# 1) ask the data for the categories, keep only values that pass a whitelist, newest N get their own column
MAX_COLS = 3
good = re.compile(r"^\d{4}-\d{2}$")
distinct = [r[0] for r in con.execute("SELECT DISTINCT month FROM sales")]
months = sorted((m for m in distinct if m is not None and good.match(m)), reverse=True)[:MAX_COLS][::-1]
print("distinct months seen:", distinct)
print("columns that get their own column:", months)

# 2) generate the SQL text: values are bound with ?, only the alias is spliced in (and it is quoted)
cols = ",\n  ".join(f"SUM(CASE WHEN month = ? THEN amount END) AS {quote_ident(m)}" for m in months)
marks = ",".join("?" * len(months))
other = f"SUM(CASE WHEN month IS NULL OR month NOT IN ({marks}) THEN amount END) AS other"
sql = (f"SELECT region,\n  {cols},\n  {other},\n  SUM(amount) AS total\nFROM sales\nGROUP BY region ORDER BY region")
params = months + months
print(sql)
print("params:", params)
cur = con.execute(sql, params)
header = [d[0] for d in cur.description]
sql_df = pd.DataFrame(cur.fetchall(), columns=header)
print(sql_df.to_string(index=False))

# 3) the reconciliation check: listed columns + other = total (NULL treated as 0)
chk = sql_df.fillna(0)
assert (chk[months + ["other"]].sum(axis=1) == chk["total"]).all()

# the naive version: NOT IN alone silently loses the NULL-month rows
naive = con.execute(f"SELECT SUM(amount) FROM sales WHERE month NOT IN ({marks})", months).fetchone()[0]
good_other = con.execute(f"SELECT SUM(amount) FROM sales WHERE month IS NULL OR month NOT IN ({marks})", months).fetchone()[0]
print("other with NOT IN only:", naive, "| other with IS NULL OR NOT IN:", good_other)

# pandas version of the same thing
df = pd.read_sql("SELECT * FROM sales", con)
df["bucket"] = df["month"].where(df["month"].isin(months), "other")   # NaN is not in the list -> 'other'
pv = df.pivot_table(index="region", columns="bucket", values="amount", aggfunc="sum")
pv = pv.reindex(columns=months + ["other"])
pv["total"] = df.groupby("region")["amount"].sum()
pv = pv.reset_index().rename_axis(columns=None)
print(pv.to_string(index=False))
a = sql_df.sort_values("region").reset_index(drop=True)
b = pv.sort_values("region").reset_index(drop=True)
pd.testing.assert_frame_equal(a, b, check_dtype=False)     # compared after sorting by region; NULL == NaN here

# the injection attempt: what happens if the weird month were spliced in as text
evil = "x'; DROP TABLE sales;--"
print("quote_ident(evil):", quote_ident(evil))
try:
    con.execute("SELECT 1 AS " + evil)
except sqlite3.Error as e:
    print("spliced raw ->", type(e).__name__, e)
print("sales still has", con.execute("SELECT COUNT(*) FROM sales").fetchone()[0], "rows")
print("SQLite limits: columns =", con.getlimit(sqlite3.SQLITE_LIMIT_COLUMN), "| bound parameters =", con.getlimit(sqlite3.SQLITE_LIMIT_VARIABLE_NUMBER))
con.close()
print("asserts passed")

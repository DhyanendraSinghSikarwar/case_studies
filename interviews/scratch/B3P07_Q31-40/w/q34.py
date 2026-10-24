# Q34: longest run of zeros and of strictly increasing readings, SQL + pandas
import sqlite3
import pandas as pd

VALUES = [0, 0, 3, 0, 0, 0, None, 0, 0, 1, 2, 2, 5, 6, 7, 3]
def load(con, vals):
    con.execute("DROP TABLE IF EXISTS readings")
    con.execute("CREATE TABLE readings(ts TEXT, value INTEGER)")
    rows = [("2024-03-01 %02d:00" % h, v) for h, v in enumerate(vals)]
    rows = rows[::-1]  # insert in reverse order: input is unsorted
    con.executemany("INSERT INTO readings VALUES (?, ?)", rows)

SQL_ZEROS = """
WITH r AS (
  SELECT ts,
         ROW_NUMBER() OVER (ORDER BY ts) AS rn_all,
         ROW_NUMBER() OVER (PARTITION BY COALESCE(value = 0, 0) ORDER BY ts) AS rn_part,
         COALESCE(value = 0, 0) AS is_zero
  FROM readings
)
SELECT MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS readings
FROM r
WHERE is_zero = 1
GROUP BY rn_all - rn_part
ORDER BY readings DESC, run_start
LIMIT 1
"""
SQL_ZEROS_FLAG = """
WITH f AS (
  SELECT ts, COALESCE(value = 0, 0) AS is_zero FROM readings
),
g AS (
  SELECT ts, is_zero, SUM(1 - is_zero) OVER (ORDER BY ts) AS grp FROM f
)
SELECT MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS readings
FROM g
WHERE is_zero = 1
GROUP BY grp
ORDER BY readings DESC, run_start
LIMIT 1
"""
SQL_UP = """
WITH f AS (
  SELECT ts, COALESCE(value > LAG(value) OVER (ORDER BY ts), 0) AS up FROM readings
),
g AS (
  SELECT ts, up, SUM(1 - up) OVER (ORDER BY ts) AS grp FROM f
)
SELECT MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS readings
FROM g
GROUP BY grp
HAVING COUNT(*) >= 2
ORDER BY readings DESC, run_start
LIMIT 1
"""
def run(con, sql):
    r = con.execute(sql).fetchall()
    return r[0] if r else None

con = sqlite3.connect(":memory:")
load(con, VALUES)
z = run(con, SQL_ZEROS); zf = run(con, SQL_ZEROS_FLAG); up = run(con, SQL_UP)
print("zeros, ROW_NUMBER difference:", z)
print("zeros, flag and group:       ", zf)
print("increasing run:              ", up)
assert z == zf

readings = pd.read_sql_query("SELECT * FROM readings", con)
# pd:main
def longest_runs(df):
    r = df.sort_values("ts").reset_index(drop=True)
    r["value"] = r["value"].astype("float64")     # an all-NULL column arrives as object dtype
    zero = r["value"].eq(0)                      # NaN == 0 is False
    zg = (~zero).cumsum()
    up = r["value"].gt(r["value"].shift())       # NaN comparisons are False
    ug = (~up).cumsum()
    def best(mask, grp, min_len):
        x = r[mask].groupby(grp[mask]).agg(run_start=("ts", "min"), run_end=("ts", "max"), readings=("ts", "size"))
        x = x[x["readings"] >= min_len].sort_values(["readings", "run_start"], ascending=[False, True])
        return None if x.empty else (x.iloc[0]["run_start"], x.iloc[0]["run_end"], int(x.iloc[0]["readings"]))
    all_rows = pd.Series(True, index=r.index)
    return best(zero, zg, 1), best(all_rows, ug, 2)
# pd:end
pz, pu = longest_runs(readings)
print("pandas zeros:", pz, " pandas increasing:", pu)
assert pz == z and pu == up   # tuples (run_start, run_end, readings)

print("--- edge cases (zeros, increasing) ---")
for name, vals in [("empty", []), ("one zero", [0]), ("one non-zero", [5]), ("one NULL", [None]),
                   ("all NULL", [None, None]), ("flat 4,4,4", [4, 4, 4]),
                   ("0,NULL,0 (NULL splits)", [0, None, 0]),
                   ("1,2,NULL,3,4 (NULL splits)", [1, 2, None, 3, 4]),
                   ("tie 1,2,3 then 0,5,6", [1, 2, 3, 0, 5, 6])]:
    load(con, vals)
    df = pd.read_sql_query("SELECT * FROM readings", con)
    s = (run(con, SQL_ZEROS), run(con, SQL_UP))
    p = longest_runs(df) if len(df) else (None, None)
    assert s == p, (name, s, p)
    print(name, "->", s)
print("asserts passed")

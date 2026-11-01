# Q38: SQL versus pandas differences on islands: five tiny reproductions, all run
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")

# ---- Row 1: duplicates break the ROW_NUMBER trick (SQL and pandas), fixed by dedup ----
con.executescript("""
CREATE TABLE logins(user_id TEXT, login_date TEXT);
INSERT INTO logins VALUES ('u','2024-03-01'),('u','2024-03-02'),('u','2024-03-02'),('u','2024-03-03');
""")
SQL_ISLANDS = """
WITH r AS (
  SELECT login_date, julianday(login_date) - ROW_NUMBER() OVER (ORDER BY login_date) AS k FROM {src}
)
SELECT MIN(login_date) AS s, MAX(login_date) AS e, COUNT(*) AS n FROM r GROUP BY k ORDER BY s
"""
raw = con.execute(SQL_ISLANDS.format(src="logins")).fetchall()
fixed = con.execute(SQL_ISLANDS.format(src="(SELECT DISTINCT login_date FROM logins)")).fetchall()
print("1 SQL raw  :", raw)
print("1 SQL dedup:", fixed)
lg = pd.read_sql_query("SELECT * FROM logins", con)
def pd_islands(df):
    d = pd.to_datetime(df["login_date"]).sort_values()
    k = (d - pd.Timestamp("1970-01-01")).dt.days - np.arange(len(d))
    return d.groupby(k.to_numpy()).agg(["min", "max", "size"]).sort_values("min").astype(str).values.tolist()
p_raw = pd_islands(lg); p_fix = pd_islands(lg.drop_duplicates())
print("1 pandas raw  :", p_raw)
print("1 pandas dedup:", p_fix)
assert len(raw) == 2 and len(fixed) == 1 and len(p_raw) == 2 and len(p_fix) == 1

# ---- Row 2: NULL != 1 is NULL in SQL; NaN != 1 and NaN != NaN are True in pandas ----
sql_row = con.execute("SELECT NULL != 1, NULL != NULL, NULL IS NOT 1, NULL IS NOT NULL, NULL IS DISTINCT FROM 1").fetchone()
print("2 SQL (NULL != 1, NULL != NULL, NULL IS NOT 1, NULL IS NOT NULL, IS DISTINCT FROM):", sql_row)
x = pd.Series([1.0, np.nan, np.nan, 2.0])
print("2 pandas x != x.shift():", (x != x.shift()).tolist())
print("2 pandas NaN != NaN:", np.nan != np.nan, "| nullable Int64 with <NA>:", (pd.Series([1, pd.NA], dtype="Int64") != 1).tolist())
assert sql_row == (None, None, 1, 0, 1)
assert (x != x.shift()).tolist() == [True, True, True, True]
# the SQL LAG flag with a plain <> drops the row after a NULL; IS NOT keeps it
con.executescript("""
CREATE TABLE st(ts INTEGER, state TEXT);
INSERT INTO st VALUES (1,'up'),(2,NULL),(3,NULL),(4,'up');
""")
q_ne = con.execute("SELECT ts FROM (SELECT ts, state, LAG(state) OVER (ORDER BY ts) AS p FROM st) WHERE p IS NULL OR state <> p").fetchall()
q_isnot = con.execute("SELECT ts FROM (SELECT ts, state, LAG(state) OVER (ORDER BY ts) AS p FROM st) WHERE state IS NOT p").fetchall()
print("2 SQL run starts, first-row test plus <> (loses ts 2, wrongly keeps ts 3):", q_ne, "| with IS NOT:", q_isnot)
assert q_ne == [(1,), (3,), (4,)] and q_isnot == [(1,), (2,), (4,)]

# ---- Row 3: shift upcasts int to float; NaT for datetimes; fill_value keeps int ----
i = pd.Series([1, 2, 3])
print("3 int shift dtype:", i.shift().dtype, "| fill_value=0:", i.shift(fill_value=0).dtype)
dts = pd.Series(pd.to_datetime(["2024-03-01", "2024-03-02"]))
print("3 datetime shift:", dts.shift().tolist())
print("3 diff on dates, dtype:", dts.diff().dtype, "| .dt.days:", dts.diff().dt.days.tolist())
print("3 SQL LAG on integers (SQLite types are dynamic, no upcast):",
      con.execute("SELECT LAG(v) OVER (ORDER BY v) FROM (SELECT 1 AS v UNION ALL SELECT 2)").fetchall())
assert i.shift().dtype == "float64" and i.shift(fill_value=0).dtype == "int64"
assert str(dts.shift().iloc[0]) == "NaT"

# ---- Row 4: ties in the ordering column ----
rng = np.random.default_rng(1)
n = 2000
t = pd.DataFrame({"ts": rng.integers(0, 5, n), "ev": np.arange(n)})        # ev records original position
default = t.sort_values("ts")
stable = t.sort_values("ts", kind="stable")
two_key = t.sort_values(["ts", "ev"])
print("4 sort_values default kind equals stable order:", default["ev"].tolist() == stable["ev"].tolist())
print("4 sort on two keys equals stable order:", two_key["ev"].tolist() == stable["ev"].tolist())
assert default["ts"].is_monotonic_increasing   # sorted by ts either way; only the tie order differs
small = pd.DataFrame({"ts": [1, 1, 1], "ev": ["a", "b", "c"]})
print("4 three tied rows, default kind:", small.sort_values("ts")["ev"].tolist())
# the pandas default kind, read from the signature
import inspect
print("4 default kind in signature:", inspect.signature(pd.DataFrame.sort_values).parameters["kind"].default)
con.executescript("CREATE TABLE tie(ts INTEGER, ev INTEGER); INSERT INTO tie VALUES (1,2),(1,1),(1,3);")
print("4 SQL ORDER BY ts only (tie order is not specified):", con.execute("SELECT ev FROM tie ORDER BY ts").fetchall(),
      "| ORDER BY ts, ev:", con.execute("SELECT ev FROM tie ORDER BY ts, ev").fetchall())

# ---- Row 5: groupby drops NaN keys; GROUP BY keeps NULL ----
g = pd.DataFrame({"k": ["a", None, "a", None], "v": [1, 2, 3, 4]})
print("5 pandas groupby default:", g.groupby("k")["v"].sum().to_dict())
print("5 pandas dropna=False   :", g.groupby("k", dropna=False)["v"].sum().to_dict())
con.executescript("CREATE TABLE g(k TEXT, v INTEGER); INSERT INTO g VALUES ('a',1),(NULL,2),('a',3),(NULL,4);")
print("5 SQL GROUP BY k:", con.execute("SELECT k, SUM(v) FROM g GROUP BY k ORDER BY k").fetchall())
assert g.groupby("k")["v"].sum().to_dict() == {"a": 4}
assert con.execute("SELECT COUNT(*) FROM (SELECT k FROM g GROUP BY k)").fetchone()[0] == 2
print("asserts passed")

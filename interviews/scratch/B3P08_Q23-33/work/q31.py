# Q31: SQL versus pandas differences in metric code, each row run on tiny data
import sqlite3
import warnings
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE t(id INTEGER, k TEXT, u INTEGER, v REAL);
INSERT INTO t VALUES (1,'a',10,1.0),(2,'a',NULL,2.0),(3,NULL,10,3.0),(4,NULL,NULL,NULL),(5,'b',20,4.0);
CREATE TABLE l(k TEXT, lv INTEGER);
CREATE TABLE r(k TEXT, rv INTEGER);
INSERT INTO l VALUES ('a',1),(NULL,2);
INSERT INTO r VALUES ('a',10),(NULL,20);
""")
df = pd.read_sql_query("SELECT * FROM t", con)
print("sqlite", sqlite3.sqlite_version, "pandas", pd.__version__, "numpy", np.__version__)

def q(sql):
    return con.execute(sql).fetchall()

print("\nRow 1: distinct count with a missing user id (column u: 10, NULL, 10, NULL, 20)")
print("  SQL COUNT(DISTINCT u):", q("SELECT COUNT(DISTINCT u) FROM t")[0][0],
      "| SQL COUNT(*):", q("SELECT COUNT(*) FROM t")[0][0],
      "| SQL COUNT(u):", q("SELECT COUNT(u) FROM t")[0][0])
print("  pandas nunique():", df["u"].nunique(), "| nunique(dropna=False):", df["u"].nunique(dropna=False),
      "| len(set(series)):", len(set(df["u"])), "| len(df['u'].unique()):", len(df["u"].unique()))
print("  SQL DISTINCT rows incl NULL group:", len(q("SELECT DISTINCT u FROM t")))

print("\nRow 2: grouping on a key with a missing value (k: a, a, NULL, NULL, b)")
print("  SQL GROUP BY k:", q("SELECT k, COUNT(*) FROM t GROUP BY k ORDER BY k"))
print("  pandas groupby default:", df.groupby("k").size().to_dict())
print("  pandas groupby dropna=False:", df.groupby("k", dropna=False).size().to_dict())
print("  value_counts default:", df["k"].value_counts().to_dict(), "| dropna=False:",
      df["k"].value_counts(dropna=False).to_dict())

print("\nRow 3: integer division and sign")
print("  SQLite 3 / 2 =", q("SELECT 3/2")[0][0], "| 3 / 2.0 =", q("SELECT 3/2.0")[0][0],
      "| -3 / 2 =", q("SELECT -3/2")[0][0], "| 3 * 1.0 / 2 =", q("SELECT 3*1.0/2")[0][0])
print("  Python 3 / 2 =", 3 / 2, "| 3 // 2 =", 3 // 2, "| -3 // 2 =", -3 // 2, "| int(-3 / 2) =", int(-3 / 2))
print("  pandas Series([3]) / 2 =", float((pd.Series([3]) / 2).iloc[0]), "| // 2 =", int((pd.Series([3]) // 2).iloc[0]),
      "| Series([-3]) // 2 =", int((pd.Series([-3]) // 2).iloc[0]))

print("\nRow 4: rounding (SQLite ROUND versus Python round, numpy and pandas)")
vals = [0.5, 1.5, 2.5, -2.5]
print("  SQLite ROUND(x):", [q(f"SELECT ROUND({x})")[0][0] for x in vals])
print("  Python round(x):", [round(x) for x in vals])
print("  numpy np.round(x):", [float(np.round(x)) for x in vals])
print("  pandas Series.round():", pd.Series(vals).round().tolist())
two = [0.125, 0.375, 2.675, 1.005]
print("  to 2 places:", two)
print("  SQLite ROUND(x, 2):", [q(f"SELECT ROUND({x}, 2)")[0][0] for x in two])
print("  Python round(x, 2):", [round(x, 2) for x in two])
print("  numpy np.round(x, 2):", [float(np.round(x, 2)) for x in two])
print("  pandas Series.round(2):", pd.Series(two).round(2).tolist())

print("\nRow 5: division by an empty or zero denominator")
print("  SQLite 1 / 0 =", q("SELECT 1/0")[0][0], "| 1.0 / 0 =", q("SELECT 1.0/0")[0][0],
      "| 0.0 / 0 =", q("SELECT 0.0/0")[0][0], "| 1 / NULLIF(0, 0) =", q("SELECT 1/NULLIF(0,0)")[0][0])
print("  SQLite SUM over zero rows:", q("SELECT SUM(v) FROM t WHERE id > 99")[0][0],
      "| COUNT over zero rows:", q("SELECT COUNT(*) FROM t WHERE id > 99")[0][0],
      "| AVG over zero rows:", q("SELECT AVG(v) FROM t WHERE id > 99")[0][0])
s = pd.Series([1.0, 0.0, 5.0]); z = pd.Series([0.0, 0.0, 5.0])
print("  pandas float Series 1/0, 0/0, 5/5:", (s / z).tolist())
print("  pandas int Series [1, 0] / [0, 0]:", (pd.Series([1, 0]) / pd.Series([0, 0])).tolist())
try:
    1 / 0
except ZeroDivisionError as e:
    print("  Python 1 / 0 raises ZeroDivisionError:", e)
empty = df[df["id"] > 99]
print("  pandas sum of empty:", empty["v"].sum(), "| mean of empty:", empty["v"].mean(), "| count:", int(empty["v"].count()))

print("\nRow 6: merge / join on keys that contain a missing value")
print("  SQL INNER JOIN on k:", q("SELECT l.k, lv, rv FROM l JOIN r ON l.k = r.k"))
print("  SQL LEFT JOIN on k:", q("SELECT l.k, lv, rv FROM l LEFT JOIN r ON l.k = r.k ORDER BY lv"))
L = pd.read_sql_query("SELECT * FROM l", con); R = pd.read_sql_query("SELECT * FROM r", con)
print("  pandas merge inner on k:")
print(L.merge(R, on="k").to_string(index=False))
print("  SQL NULL = NULL:", q("SELECT NULL = NULL")[0][0], "| NULL IS NULL:", q("SELECT NULL IS NULL")[0][0])

print("\nRow 7: rolling().nunique")
print("  hasattr(Series.rolling(2), 'nunique'):", hasattr(pd.Series([1, 2]).rolling(2), "nunique"))
print("  hasattr(Series.rolling(2), 'count'):", hasattr(pd.Series([1, 2]).rolling(2), "count"))

# assertions behind the table
assert q("SELECT COUNT(DISTINCT u) FROM t")[0][0] == df["u"].nunique() == 2
assert q("SELECT 3/2")[0][0] == 1 and 3 / 2 == 1.5
assert q("SELECT ROUND(2.5)")[0][0] == 3.0 and round(2.5) == 2
print("\nasserts passed")

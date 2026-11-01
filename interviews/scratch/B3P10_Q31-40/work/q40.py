# SQL versus pandas on NULL/NaN and strings: each row of the translation table is run on both sides and asserted.
import io
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
q1 = lambda sql, *a: con.execute(sql, a).fetchone()[0]
rows = []
def row(topic, sql_result, pandas_result, expected):
    assert (sql_result, pandas_result) == expected, (topic, sql_result, pandas_result, expected)
    rows.append((topic, repr(sql_result), repr(pandas_result)))

# 1 equality of missing values
nan = float("nan")
row("1 NaN == NaN  /  NULL = NULL", q1("SELECT NULL = NULL"), bool(nan == nan), (None, False))
row("1b null-safe equal of two missing values", q1("SELECT NULL IS NOT DISTINCT FROM NULL"), bool(pd.isna(nan) and pd.isna(nan)), (1, True))
a, b = pd.Series([1.0, np.nan, 3.0]), pd.Series([1.0, np.nan, 4.0])
sql_eq = [r[0] for r in con.execute("""WITH t(a,b) AS (VALUES (1.0,1.0),(NULL,NULL),(3.0,4.0))
                                       SELECT a IS NOT DISTINCT FROM b FROM t""")]
pd_eq = (a.eq(b) | (a.isna() & b.isna())).astype(int).tolist()
row("1c elementwise null-safe equal", sql_eq, pd_eq, ([1, 1, 0], [1, 1, 0]))
sql_plain = [r[0] for r in con.execute("WITH t(a,b) AS (VALUES (1.0,1.0),(NULL,NULL),(3.0,4.0)) SELECT a = b FROM t")]
row("1d plain a = b vs Series.eq", sql_plain, a.eq(b).astype(int).tolist(), ([1, None, 0], [1, 0, 0]))
row("1e Series.equals (whole object, NaN == NaN)", "no such operator", a.equals(a.copy()), ("no such operator", True))
s_na = pd.Series([pd.NA, 1], dtype="Int64")
row("1f pd.NA == pd.NA (nullable dtype)", q1("SELECT NULL = NULL"), "<NA>" if (s_na == s_na)[0] is pd.NA else "other", (None, "<NA>"))

# 2 group by
con.executescript("CREATE TABLE o(region TEXT, amount INTEGER); INSERT INTO o VALUES ('N',1),('N',2),(NULL,5),(NULL,NULL),('S',NULL);")
o = pd.read_sql("SELECT * FROM o", con)
row("2 groups with a NULL key", len(con.execute("SELECT region FROM o GROUP BY region").fetchall()),
    o.groupby("region").ngroups, (3, 2))
row("2b dropna=False keeps it", 3, o.groupby("region", dropna=False).ngroups, (3, 3))

# 3 empty string vs blank in CSV
csv_text = "name,city\nAsha,\nBen,Pune\n"
import csv as csvmod
con.execute("CREATE TABLE c(name TEXT, city TEXT)")
con.executemany("INSERT INTO c VALUES (?,?)", list(csvmod.reader(io.StringIO(csv_text)))[1:])
sql_city = q1("SELECT city FROM c WHERE name='Asha'")
pd_city = pd.read_csv(io.StringIO(csv_text)).loc[0, "city"]
row("3 blank CSV field", sql_city, bool(pd.isna(pd_city)), ("", True))
row("3b keep '' in pandas", sql_city, pd.read_csv(io.StringIO(csv_text), keep_default_na=False).loc[0, "city"], ("", ""))
row("3c COUNT(city) vs count()", q1("SELECT COUNT(city) FROM c"), int(pd.read_csv(io.StringIO(csv_text))["city"].count()), (2, 1))

# 4 sum of nothing
row("4 SUM of all-missing", q1("SELECT SUM(amount) FROM o WHERE region = 'S'"), float(o.loc[o.region == "S", "amount"].sum()), (None, 0.0))
row("4b with min_count=1", q1("SELECT SUM(amount) FROM o WHERE region = 'S'"),
    bool(np.isnan(o.loc[o.region == "S", "amount"].sum(min_count=1))), (None, True))

# 5 integer column with a gap
row("5 typeof of an INTEGER column with a NULL", q1("SELECT group_concat(t) FROM (SELECT DISTINCT typeof(amount) AS t FROM o ORDER BY t)"),
    str(o["amount"].dtype), ("integer,null", "float64"))
row("5b nullable Int64 keeps integers", q1("SELECT typeof(1)"), str(o["amount"].astype("Int64").dtype), ("integer", "Int64"))

# 6 LIKE vs contains
con.executescript("CREATE TABLE w(s TEXT); INSERT INTO w VALUES ('Apple'),('apple pie'),('a.b'),('axb'),('100%'),('1000'),('Ärger'),(NULL);")
w = pd.read_sql("SELECT s FROM w", con)
sql_like = [r[0] for r in con.execute("SELECT s FROM w WHERE s LIKE '%APPLE%' ORDER BY rowid")]
pd_def = w.loc[w["s"].str.contains("APPLE"), "s"].tolist()
pd_ci = w.loc[w["s"].str.contains("apple", case=False), "s"].tolist()
row("6 LIKE '%APPLE%' vs contains('APPLE')", sql_like, pd_def, (["Apple", "apple pie"], []))
row("6b contains(case=False)", sql_like, pd_ci, (["Apple", "apple pie"], ["Apple", "apple pie"]))
row("6c non-ASCII case", q1("SELECT 'Ärger' LIKE 'ärger'"), bool(w["s"].str.contains("ärger", case=False).iloc[6]), (0, True))
row("6d NULL row in the result", q1("SELECT NULL LIKE '%a%'"), bool(w["s"].str.contains("a").iloc[7]), (None, False))

# 7 wildcards vs regex metacharacters
sql_dot = [r[0] for r in con.execute("SELECT s FROM w WHERE s LIKE 'a.b' ORDER BY rowid")]
pd_dot = w.loc[w["s"].str.contains("a.b"), "s"].tolist()
row("7 'a.b': LIKE vs regex contains", sql_dot, pd_dot, (["a.b"], ["a.b", "axb"]))
pd_lit = w.loc[w["s"].str.contains("a.b", regex=False), "s"].tolist()
row("7b contains(regex=False)", sql_dot, pd_lit, (["a.b"], ["a.b"]))
sql_pct = [r[0] for r in con.execute("SELECT s FROM w WHERE s LIKE '100%' ORDER BY rowid")]
sql_pct_esc = [r[0] for r in con.execute(r"SELECT s FROM w WHERE s LIKE '100\%' ESCAPE '\' ORDER BY rowid")]
row("7c '100%': LIKE wildcard vs contains", sql_pct, w.loc[w["s"].str.contains("100%"), "s"].tolist(), (["100%", "1000"], ["100%"]))
row("7d LIKE '100\\%' ESCAPE vs contains(regex=False)", sql_pct_esc, w.loc[w["s"].str.contains("100%", regex=False), "s"].tolist(), (["100%"], ["100%"]))
sql_start = [r[0] for r in con.execute("SELECT s FROM w WHERE s LIKE 'a%' ORDER BY rowid")]
row("7e startswith vs LIKE 'a%'", sql_start, w.loc[w["s"].str.startswith("a"), "s"].tolist(), (["Apple", "apple pie", "a.b", "axb"], ["apple pie", "a.b", "axb"]))

# 8 sort position
vals = [3, None, 1]
con.execute("CREATE TABLE v(x INTEGER)"); con.executemany("INSERT INTO v VALUES (?)", [(x,) for x in vals])
sql_asc = [r[0] for r in con.execute("SELECT x FROM v ORDER BY x")]
pd_asc = [None if pd.isna(x) else int(x) for x in pd.Series(vals, dtype="float64").sort_values().tolist()]
row("8 ascending sort position of the missing value", sql_asc, pd_asc, ([None, 1, 3], [1, 3, None]))
sql_last = [r[0] for r in con.execute("SELECT x FROM v ORDER BY x NULLS LAST")]
row("8b NULLS LAST / default pandas", sql_last, pd_asc, ([1, 3, None], [1, 3, None]))

print(pd.DataFrame(rows, columns=["row", "SQLite 3.45", "pandas 3.0"]).to_string(index=False))
print("asserts passed")
con.close()

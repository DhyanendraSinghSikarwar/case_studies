# Q15: missing values in pandas 3 (str dtype) versus SQL NULL
import sqlite3
import numpy as np
import pandas as pd

print("pandas", pd.__version__, "| SQLite", sqlite3.sqlite_version)
vals = ["a", None, np.nan, "B", ""]

# <<pd_series
s = pd.Series(vals)                      # inferred dtype: str (pandas 3 default)
df = pd.DataFrame({"x": vals})           # the same inference inside a DataFrame column
t = pd.Series(vals, dtype="string")      # nullable string dtype, missing marker pd.NA
o = pd.Series(vals, dtype=object)        # legacy object dtype, keeps None and NaN as given
# >>
print("\ninferred dtypes: Series", s.dtype, "| DataFrame column", df["x"].dtype, "| string:", t.dtype, "| object:", o.dtype)
print("str    :", s.tolist(), " (None became NaN)")
print("string :", t.tolist())
print("object :", o.tolist())
print("isna   str/string/object:", s.isna().tolist(), t.isna().tolist(), o.isna().tolist())
print("== 'a' str   :", (s == "a").tolist())
print("== 'a' string:", (t == "a").tolist())
print("!= 'a' str   :", (s != "a").tolist(), "<- missing counts as 'not equal'")
print("!= 'a' string:", (t != "a").tolist(), "<- missing stays missing")
print("s == s (NaN with itself):", (s == s).tolist(), "| t == t:", (t == t).tolist())
print(".str.len() str:", s.str.len().tolist(), s.str.len().dtype, "| string:", t.str.len().tolist(), t.str.len().dtype)
print(".str.upper() str:", s.str.upper().tolist(), "| object:", o.str.upper().tolist())
print("s + '!' str:", (s + "!").tolist(), "| string:", (t + "!").tolist())
print("str.cat(sep='|') skips missing:", repr(s.str.cat(sep="|")))

# scalars
print("\nNaN == NaN:", np.nan == np.nan, "| None == None:", None == None, "| pd.NA == pd.NA:", pd.NA == pd.NA)
try:
    bool(pd.NA)
except TypeError as e:
    print("bool(pd.NA) -> TypeError:", e)
print("pd.isna of None, NaN, pd.NA, '', 'NaN':", [bool(pd.isna(v)) for v in (None, np.nan, pd.NA, "", "NaN")])

# mixed types
m = pd.Series(["a", 1, None])
print("\nmixed ['a', 1, None] dtype:", m.dtype, "| .str.upper():", m.str.upper().tolist(), "(the integer 1 becomes NaN, not '1')")
try:
    pd.Series([1, 2]).str.upper()
except AttributeError as e:
    print("ints .str ->", type(e).__name__ + ":", e)

# the astype(str) trap: what happens to missing values in pandas 3.0.5
print("\nastype(str) on the str Series      :", s.astype(str).tolist(), s.astype(str).dtype)
print("astype(str) on float [1.0, NaN]    :", pd.Series([1.0, np.nan]).astype(str).tolist())
print("astype(str) on object ['a', None]  :", pd.Series(["a", None], dtype=object).astype(str).tolist())
print(".map(str) on object ['a', None]    :", pd.Series(["a", None], dtype=object).map(str).tolist())
print("numpy astype(str) on [a, None, nan]:", np.array(["a", None, np.nan], dtype=object).astype(str).tolist())
print("f-string / str() on NaN            :", [f"{v}" for v in vals])

# SQL side: same values loaded into SQLite
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE v(id INTEGER PRIMARY KEY, x TEXT)")
con.executemany("INSERT INTO v VALUES (?, ?)", [(i, None if (isinstance(x, float) or x is None) else x) for i, x in enumerate(vals)])
sql_isnull = [r[0] for r in con.execute("SELECT x IS NULL FROM v ORDER BY id")]
sql_eq_a = [r[0] for r in con.execute("SELECT x = 'a' FROM v ORDER BY id")]
sql_ne_rows = [r[0] for r in con.execute("SELECT id FROM v WHERE x <> 'a' ORDER BY id")]
sql_len = [r[0] for r in con.execute("SELECT LENGTH(x) FROM v ORDER BY id")]
sql_scalar = con.execute("SELECT NULL = NULL, NULL IS NULL, NULL IS NOT DISTINCT FROM NULL, 'a' || NULL").fetchone()
print("\nSQL x IS NULL      :", sql_isnull)
print("SQL x = 'a'        :", sql_eq_a, "(Python None = SQL NULL)")
print("SQL WHERE x <> 'a' :", "ids", sql_ne_rows, "(NULL rows are not returned)")
print("SQL LENGTH(x)      :", sql_len)
print("SQL NULL = NULL, NULL IS NULL, IS NOT DISTINCT FROM, 'a'||NULL:", sql_scalar)

print("\nsort_values() default puts missing last:", s.sort_values().tolist(), "| na_position='first':", s.sort_values(na_position="first").tolist())
back = pd.read_sql_query("SELECT * FROM v ORDER BY id", con)
print("read_sql_query x dtype:", back["x"].dtype, "| after convert_dtypes():", back["x"].convert_dtypes().dtype, back["x"].convert_dtypes().tolist())

# comparisons (rows in id order)
assert [int(v) for v in s.isna()] == sql_isnull
assert [int(v) for v in t.isna()] == sql_isnull
# pandas str-dtype != 'a' is True for missing, SQL's <> drops them: they differ on ids 1 and 2
p_ne_naive = s.index[(s != "a")].tolist()
assert p_ne_naive == [1, 2, 3, 4] and sql_ne_rows == [3, 4]
# the SQL-like filter in pandas: nullable string dtype (NA mask counts as False) or an explicit notna()
assert t.index[(t != "a").fillna(False)].tolist() == sql_ne_rows
assert s.index[(s != "a") & s.notna()].tolist() == sql_ne_rows
# SQL = 'a' with NULL is NULL; pandas string dtype gives <NA> in the same places
assert [None if pd.isna(v) else int(v) for v in (t == "a")] == sql_eq_a
# lengths: SQL integer/NULL, pandas string dtype Int64/<NA>, str dtype float/NaN
assert [None if pd.isna(v) else int(v) for v in t.str.len()] == sql_len
assert [None if pd.isna(v) else int(v) for v in s.str.len()] == sql_len
print("\nasserts passed (compared in id order: isna flags, '<>' rows, '=' flags, lengths)")

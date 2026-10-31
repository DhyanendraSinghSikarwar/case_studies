# pandas conversions and category pitfalls, compared with SQLite CAST and affinity.
import io
import sqlite3
import numpy as np
import pandas as pd

csv = '''amount,amount_clean,pincode,when,status,country
"1,200","1,200",011001,2024-01-05,paid,NA
 45 ,45,110001,05/01/2024,paid,IN
x,7,400001,2024-03-07,refunded,None
1e3,"2,000",560001,not a date,paid,N/A
,,011001,,pending,IN
'''
raw = pd.read_csv(io.StringIO(csv))
print("default read_csv dtypes:", {k: str(v) for k, v in raw.dtypes.items()})
print("pincode as int loses the zero:", raw["pincode"].tolist(), "| country NA/None/N/A became:", raw["country"].tolist())
good = pd.read_csv(io.StringIO(csv), thousands=",", dtype={"pincode": str}, keep_default_na=False, na_values=[""])
print("thousands=',' + dtype/pincode + keep_default_na=False:", {k: str(v) for k, v in good.dtypes.items()})
print("amount_clean:", good["amount_clean"].tolist(), "| amount (has 'x') stays text:", good["amount"].tolist(), "| pincode:", good["pincode"].tolist(), "| country:", good["country"].tolist())
print("default NA markers:", sorted(pd._libs.parsers.STR_NA_VALUES))

amt = raw["amount"]
def attempt(label, f):
    try:
        print(f"{label:34} -> {f()}")
    except Exception as e:
        print(f"{label:34} -> {type(e).__name__}: {e}")
attempt("astype(int) on the amount column", lambda: amt.astype(int).tolist())
attempt("astype(int) on [' 45 ']", lambda: pd.Series([" 45 "]).astype(int).tolist())
attempt("astype(float) on ['1e3']", lambda: pd.Series(["1e3"]).astype(float).tolist())
attempt("astype(float) on ['']", lambda: pd.Series([""]).astype(float).tolist())
attempt("to_numeric (errors='raise')", lambda: pd.to_numeric(amt).tolist())
coerced = pd.to_numeric(amt, errors="coerce")
print("to_numeric coerce:", coerced.tolist(), str(coerced.dtype))
nocomma = pd.to_numeric(amt.str.replace(",", "", regex=False), errors="coerce")
print("remove commas first:", nocomma.tolist())
print("downcast='integer' on clean ints:", str(pd.to_numeric(pd.Series(["1", "200", "3"]), downcast="integer").dtype),
      "| with a NaN it stays:", str(pd.to_numeric(pd.Series(["1", None, "3"]), downcast="integer").dtype))

# ---- SQLite CAST outcomes for the same strings, and a NULL-giving 'safe cast'
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE raw(id INTEGER PRIMARY KEY, amount TEXT, pincode TEXT, d TEXT)")
con.executemany("INSERT INTO raw(amount, pincode, d) VALUES (?,?,?)",
                [(a if isinstance(a, str) else None, p, w if isinstance(w, str) else None)
                 for a, p, w in zip(raw["amount"], ["011001", "110001", "400001", "560001", "011001"], raw["when"])])
cast_rows = con.execute("""SELECT amount, CAST(amount AS INTEGER), CAST(amount AS REAL), CAST(pincode AS INTEGER)
                           FROM raw ORDER BY id""").fetchall()
for r in cast_rows:
    print("SQLite CAST", r)
safe_sql = """SELECT CASE WHEN trim(amount) GLOB '[0-9]*' AND trim(amount) NOT GLOB '*[^0-9.]*'
                   THEN CAST(trim(amount) AS REAL) END AS n FROM raw ORDER BY id"""
sql_safe = [r[0] for r in con.execute(safe_sql)]
print("SQL safe-cast (NULL for garbage):", sql_safe)
mask = amt.fillna("") != "1e3"     # '1e3': pandas accepts exponent notation, the GLOB rule does not
assert [None if v is None else v for v, m in zip(sql_safe, mask) if m] == \
       [None if np.isnan(v) else v for v, m in zip(coerced.tolist(), mask) if m] == [None, 45.0, None, None]
print("pandas coerce on '1e3':", coerced[3], "| SQL safe-cast:", sql_safe[3], "| CAST AS INTEGER:", cast_rows[3][1])

# dates
dates = raw["when"]
sql_dates = [r[0] for r in con.execute("SELECT date(d) FROM raw ORDER BY id")]
iso = pd.to_datetime(dates, format="%Y-%m-%d", errors="coerce").dt.strftime("%Y-%m-%d")
print("SQL date():", sql_dates)
assert sql_dates == [None if pd.isna(v) else v for v in iso]
attempt("to_datetime default, strict", lambda: pd.to_datetime(dates.dropna()).tolist())
print("coerce (format guessed from row 1):", pd.to_datetime(dates, errors="coerce").dt.strftime("%Y-%m-%d").tolist())
print("format='mixed':", pd.to_datetime(dates, errors="coerce", format="mixed").dt.strftime("%Y-%m-%d").tolist())
print("format='mixed', dayfirst=True:", pd.to_datetime(dates, errors="coerce", format="mixed", dayfirst=True).dt.strftime("%Y-%m-%d").tolist())

# affinity and STRICT
con.executescript("""
CREATE TABLE aff(i INTEGER, t TEXT, n NUMERIC, r REAL);
INSERT INTO aff VALUES (' 12',' 12',' 12',' 12'),('12 ','12 ','12 ','12 '),('x','x','x','x'),('1e3','1e3','1e3','1e3'),('0x10','0x10','0x10','0x10'),(12,12,12,12);
""")
for r in con.execute("SELECT typeof(i), i, typeof(t), t, typeof(r), r FROM aff"):
    print("affinity row:", r)
print("TEXT column ' 12' = 12 ->", con.execute("SELECT t = 12 FROM aff WHERE rowid = 1").fetchone()[0],
      "| INTEGER column ' 12' = 12 ->", con.execute("SELECT i = 12 FROM aff WHERE rowid = 1").fetchone()[0])
con.execute("CREATE TABLE st(i INTEGER, t TEXT) STRICT")
for v in [(" 12", "x"), ("x", "y"), ("12", 12)]:
    try:
        con.execute("INSERT INTO st VALUES (?,?)", v)
        print("STRICT insert ok:", v)
    except sqlite3.Error as e:
        print("STRICT insert", v, "->", e)
print("STRICT stored:", con.execute("SELECT typeof(i), i, typeof(t), t FROM st").fetchall())

# ---- category pitfalls
status = good["status"].astype("category")
print("categories:", status.cat.categories.tolist())
def assign_outside():
    status.loc[0] = "lost"
attempt("assign outside categories", assign_outside)
t = pd.Series(["a", None, "b"], dtype="category")
attempt("fillna with a new category", lambda: t.fillna("unknown").tolist())
print("add_categories first:", t.cat.add_categories("unknown").fillna("unknown").tolist())
df = pd.DataFrame({"status": pd.Categorical(["paid", "paid", "refunded"], categories=["pending", "paid", "refunded"]), "amt": [1, 2, 3]})
print("groupby default:", df.groupby("status")["amt"].sum().to_dict(), "| observed=False:", df.groupby("status", observed=False)["amt"].sum().to_dict())
ordered = pd.Series(pd.Categorical(["paid", "pending", "refunded"], categories=["pending", "paid", "refunded"], ordered=True))
print("sort by category order:", ordered.sort_values().tolist(), "| alphabetical:", sorted(["paid", "pending", "refunded"]))
up = status.str.upper()
print(".str on category works, result dtype:", str(up.dtype), up.tolist())
assert (str(coerced.dtype) == "float64") and good["pincode"].tolist()[0] == "011001"
print("asserts passed")
con.close()

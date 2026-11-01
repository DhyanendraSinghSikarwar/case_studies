# What SQLite 3.45 has and lacks for strings, and how to add REGEXP from Python.
import re
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)

def try_(expr):
    try:
        return con.execute("SELECT " + expr).fetchone()[0]
    except sqlite3.Error as e:
        return "ERROR: " + str(e)

print("--- missing in this build")
for e in ["'a' REGEXP 'a'", "split_part('a,b',',',1)", "reverse('abc')", "lpad('7',3,'0')", "char_length('abc')"]:
    print(f"{e:32} -> {try_(e)}")
print("--- present in this build")
for e in ["concat('a',NULL,'b')", "concat_ws(',','a',NULL,'b')", "printf('%05.1f',3.14159)", "format('%d items',3)",
          "octet_length('é')", "hex(unhex('4142'))", "iif(1<2,'yes','no')", "NULL IS DISTINCT FROM 1"]:
    print(f"{e:32} -> {try_(e)}")
con.execute("CREATE TABLE t(v TEXT)")
con.executemany("INSERT INTO t VALUES (?)", [("b",),("a",),("c",)])
print("string_agg ordered ->", con.execute("SELECT string_agg(v,'|' ORDER BY v DESC) FROM t").fetchone()[0])

# register a Python regexp(pattern, value): SQL 'X REGEXP Y' calls regexp(Y, X)
def regexp(pattern, value):
    return None if pattern is None or value is None else int(re.search(pattern, value) is not None)
con.create_function("regexp", 2, regexp, deterministic=True)
print("--- after create_function")
print("'abc123' REGEXP '\\d+'      ->", try_(r"'abc123' REGEXP '\d+'"))
print("NULL REGEXP 'a'           ->", try_("NULL REGEXP 'a'"))

con.executescript("""
CREATE TABLE codes(code TEXT);
INSERT INTO codes VALUES ('AB-1234'),('ab-1234'),('AB-12x4'),('AB-123'),(NULL),('AB-12345');
""")
q_re   = r"SELECT code FROM codes WHERE code REGEXP '^[A-Z]{2}-\d{4}$' ORDER BY rowid"
# same job with GLOB (case-sensitive, fixed-length classes only, no {4} quantifier)
q_glob = "SELECT code FROM codes WHERE code GLOB '[A-Z][A-Z]-[0-9][0-9][0-9][0-9]' ORDER BY rowid"
q_like = "SELECT code FROM codes WHERE code LIKE '__-____' ORDER BY rowid"     # LIKE only knows _ and %
r = lambda q: [x[0] for x in con.execute(q).fetchall()]
print("regexp:", r(q_re)); print("glob  :", r(q_glob)); print("like  :", r(q_like))
print("rows with only A-Z, 0-9 and - (GLOB negated class):",
      r("SELECT code FROM codes WHERE code NOT GLOB '*[^0-9A-Z-]*' AND code IS NOT NULL ORDER BY rowid"))

# LIKE is ASCII case-insensitive; the pragma flips that; GLOB is always case-sensitive
print("'a' LIKE 'A' ->", try_("'a' LIKE 'A'"), "| 'Ä' LIKE 'ä' ->", try_("'Ä' LIKE 'ä'"), "| 'a' GLOB 'A' ->", try_("'a' GLOB 'A'"))
con.execute("PRAGMA case_sensitive_like = ON")
print("after PRAGMA case_sensitive_like=ON: 'a' LIKE 'A' ->", try_("'a' LIKE 'A'"))
con.execute("PRAGMA case_sensitive_like = OFF")

# the registered function lives only in this connection
con2 = sqlite3.connect(":memory:")
try:
    con2.execute("SELECT 'a' REGEXP 'a'")
except sqlite3.Error as e:
    print("second connection ->", e)

# pandas equivalent, same rows
df = pd.read_sql("SELECT rowid AS id, code FROM codes", con)
m = df["code"].str.contains(r"^[A-Z]{2}-\d{4}$", regex=True)       # NaN row gives False here, not NULL
print("pandas:", df.loc[m, "code"].tolist())
assert df.loc[m, "code"].tolist() == r(q_re) == r(q_glob) == ["AB-1234"]
con.close()
print("asserts passed")

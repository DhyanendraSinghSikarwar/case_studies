# Q29: SQL string operations and their pandas .str equivalents, one contacts table, every row run.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE contacts(id INTEGER PRIMARY KEY, name TEXT, email TEXT, code TEXT);
INSERT INTO contacts VALUES
 (1,'Asha Rao',   'Asha.Rao@Example.com', '7'),
 (2,' ben kumar ','ben@test.org',         '42'),
 (3,NULL,         'noatsign',             '123'),
 (4,'Dee  Lee',   'dee.lee@a.b.com',      NULL),
 (5,'chitra',     NULL,                   '5');
""")
df = pd.read_sql("SELECT * FROM contacts ORDER BY id", con)
print("pandas dtypes:", dict(df.dtypes.astype(str)), "| missing marker in name:", repr(df["name"].iloc[2]))

def norm(vals):
    out = []
    for v in vals:
        if v is None or (isinstance(v, float) and np.isnan(v)) or v is pd.NA: out.append(None)
        elif isinstance(v, (np.integer, np.floating, float, int)) and float(v) == int(v): out.append(int(v))
        else: out.append(v)
    return out
def sql_col(expr): return norm([r[0] for r in con.execute(f"SELECT {expr} FROM contacts ORDER BY id")])

# (label, SQL expression, pandas Series, do they agree?)
s, e, c = df["name"], df["email"], df["code"]
cases = [
 ("LOWER / str.lower",            "LOWER(name)",         s.str.lower(), True),
 ("UPPER / str.upper",            "UPPER(name)",         s.str.upper(), True),
 ("TRIM / str.strip",             "TRIM(name)",          s.str.strip(), True),
 ("SUBSTR(name,1,3) / str[0:3]",  "SUBSTR(name, 1, 3)",  s.str[0:3], True),
 ("INSTR(email,'@') / find('@')+1", "INSTR(email, '@')", e.str.find("@") + 1, True),
 ("REPLACE(name,' ','_') / str.replace(' ','_')", "REPLACE(name, ' ', '_')", s.str.replace(" ", "_"), True),
 ("collapse double spaces: SQL REPLACE vs pandas str.replace(' +',' ') (default regex=False)", "REPLACE(name, '  ', ' ')", s.str.replace(" +", " "), False),
 ("same, with regex=True", "REPLACE(name, '  ', ' ')", s.str.replace(" +", " ", regex=True), True),
 ("name LIKE 'a%' vs str.startswith('a')", "COALESCE(name LIKE 'a%', 0)", s.str.startswith("a"), False),
 ("name LIKE 'a%' vs str.lower().startswith('a')", "COALESCE(name LIKE 'a%', 0)", s.str.lower().str.startswith("a"), True),
 ("raw name LIKE 'a%' (NULL kept) vs str.lower().startswith('a')", "name LIKE 'a%'", s.str.lower().str.startswith("a"), False),
 ("email LIKE '%.%' vs str.contains('.', regex=False)", "COALESCE(email LIKE '%.%', 0)", e.str.contains(".", regex=False), True),
 ("email LIKE '%.%' vs str.contains('.') (default regex=True)", "COALESCE(email LIKE '%.%', 0)", e.str.contains("."), False),
 ("name LIKE '%ASHA%' vs contains('ASHA', case=False, regex=False)", "COALESCE(name LIKE '%ASHA%', 0)", s.str.contains("ASHA", case=False, regex=False), True),
 ("name || '-' || code vs s + '-' + c", "name || '-' || code", s + "-" + c, True),
 ("CONCAT_WS('-', name, code) vs str.cat(c, sep='-', na_rep='')", "CONCAT_WS('-', name, code)", s.str.cat(c, sep="-", na_rep=""), False),
 ("CONCAT_WS('-', name, code) vs '-'.join(row.dropna())", "CONCAT_WS('-', name, code)", df[["name", "code"]].apply(lambda r: "-".join(r.dropna()), axis=1), True),
 ("LENGTH(name) vs str.len()", "LENGTH(name)", s.str.len(), True),
 ("domain: SUBSTR+INSTR vs str.split('@', n=1).str[1]", "CASE WHEN INSTR(email,'@')>0 THEN SUBSTR(email, INSTR(email,'@')+1) END", e.str.split("@", n=1).str[1], True),
 ("user part: SUBSTR+INSTR vs str.extract(named group)", "CASE WHEN INSTR(email,'@')>0 THEN SUBSTR(email, 1, INSTR(email,'@')-1) END", e.str.extract(r"(?P<user>[^@]+)@(?P<domain>.+)")["user"], True),
 ("SUBSTR('00000'||code,-5) vs zfill(5)", "SUBSTR('00000' || code, -5)", c.str.zfill(5), True),
 ("PRINTF('%5s', code) vs pad(5)", "PRINTF('%5s', code)", c.str.pad(5), False),
]
for label, sqlx, ser, agree in cases:
    a, b = sql_col(sqlx), norm(ser.tolist())
    same = a == b
    print(f"{label}\n    SQL   : {a}\n    pandas: {b}   [{'same' if same else 'DIFF'}]")
    assert same == agree, label          # every row is asserted: 'same' rows must match, 'DIFF' rows must still differ
print("rows asserted:", len(cases))

print("na handling of contains on NaN:",
      "str dtype ->", df["email"].str.contains("@").tolist(),
      "| object dtype ->", df["email"].astype(object).str.contains("@").tolist(),
      "| string dtype ->", df["email"].astype("string").str.contains("@").tolist(),
      "| na=True ->", df["email"].str.contains("@", na=True).tolist())
print("SQL: email LIKE '%@%' ->", sql_col("email LIKE '%@%'"))
print("str.len dtype:", s.str.len().dtype, "| s + 'x' on NaN:", (s + "x").tolist()[2])
print("title (no INITCAP in SQLite):", pd.Series(["o'neil", "mc donald", "ANNA-MARIE", "they're"]).str.title().tolist())
con.execute("PRAGMA case_sensitive_like = 1")
print("after PRAGMA case_sensitive_like=1, 'Asha' LIKE 'a%':", con.execute("SELECT 'Asha' LIKE 'a%'").fetchone()[0])
con.close()
print("asserts passed (rows marked same agree; rows marked DIFF are the documented differences, asserted to differ)")

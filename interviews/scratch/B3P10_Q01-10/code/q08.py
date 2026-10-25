# Q8: string-to-number CAST traps in SQLite and a validation that separates clean, fixable, invalid.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE raw_amounts(id INTEGER PRIMARY KEY, amount_text TEXT);
INSERT INTO raw_amounts VALUES
 (1,'1200'),(2,'1,200'),(3,' 45 '),(4,'007'),(5,'12abc'),(6,'abc'),(7,''),
 (8,'1e3'),(9,'3.7'),(10,'0x10'),(11,NULL);
""")

sql_cast = """
SELECT id, amount_text,
       CAST(amount_text AS INTEGER) AS as_int,
       CAST(amount_text AS REAL)    AS as_real,
       CAST(CAST(amount_text AS REAL) AS TEXT) = amount_text AS roundtrip_ok
FROM raw_amounts ORDER BY id
"""
cast = pd.read_sql(sql_cast, con)
print(cast.assign(amount_text=cast.amount_text.map(repr)).to_string(index=False)); print()

# 'clean' = digits with at most one dot and at least one digit; 'fixable' = clean after removing commas and spaces
sql_class = """
WITH s AS (
  SELECT id, amount_text AS x,
         REPLACE(REPLACE(TRIM(amount_text), ',', ''), ' ', '') AS f
  FROM raw_amounts
)
SELECT id, x,
  CASE
    WHEN x IS NULL OR TRIM(x) = ''                                    THEN 'missing'
    WHEN x GLOB '*[0-9]*' AND x NOT GLOB '*[^0-9.]*'
         AND LENGTH(x) - LENGTH(REPLACE(x, '.', '')) <= 1             THEN 'clean'
    WHEN f GLOB '*[0-9]*' AND f NOT GLOB '*[^0-9.]*'
         AND LENGTH(f) - LENGTH(REPLACE(f, '.', '')) <= 1             THEN 'fixable'
    ELSE 'invalid'
  END AS status,
  CASE WHEN f GLOB '*[0-9]*' AND f NOT GLOB '*[^0-9.]*' AND LENGTH(f) - LENGTH(REPLACE(f, '.', '')) <= 1
       THEN CAST(f AS REAL) END AS value
FROM s ORDER BY id
"""
cls = pd.read_sql(sql_class, con)
print(cls.assign(x=cls.x.map(repr)).to_string(index=False)); print()
print("zero from garbage vs a real zero:", con.execute("SELECT CAST('abc' AS INTEGER) = CAST('0' AS INTEGER)").fetchone()[0])
print("typeof(CAST('abc' AS INTEGER)):", con.execute("SELECT typeof(CAST('abc' AS INTEGER))").fetchone()[0])
print("'12abc' + 1 =", con.execute("SELECT '12abc' + 1").fetchone()[0], "(arithmetic coerces the same way)")

# pandas
raw = pd.read_sql("SELECT * FROM raw_amounts ORDER BY id", con)
x = raw["amount_text"]
coerced = pd.to_numeric(x, errors="coerce")
print("\nto_numeric(errors='coerce'):")
print(pd.DataFrame({"x": x.map(repr), "numeric": coerced}).to_string(index=False)); print()

f = x.str.strip().str.replace(",", "", regex=False).str.replace(" ", "", regex=False)
missing = x.isna() | (x.str.strip() == "")
pat = r"[0-9]*\.?[0-9]*"
is_clean = x.str.fullmatch(pat) & x.str.contains("[0-9]")
is_fix = f.str.fullmatch(pat) & f.str.contains("[0-9]")
status = np.select([missing, is_clean, is_fix], ["missing", "clean", "fixable"], default="invalid")
value = pd.to_numeric(f.where(is_fix), errors="coerce")
p = pd.DataFrame({"id": raw.id, "status": status, "value": value})

assert cls["status"].tolist() == p["status"].tolist()
assert np.allclose(cls["value"].fillna(-1), p["value"].fillna(-1))
print("asserts passed (id order): statuses", dict(zip(cls.id, cls.status)))

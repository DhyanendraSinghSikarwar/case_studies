# Q21: nth field and text between delimiters without split_part (SQLite) versus pandas str.split / str.extract.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products(id INTEGER PRIMARY KEY, sku TEXT, attributes_text TEXT);
INSERT INTO products VALUES
 (1,'ABC-123-XL','color=red;size=M'),
 (2,'XY-7-M',    'color=blue;size=L;fit=slim'),
 (3,'LONE',      'color=green'),
 (4,NULL,        NULL),
 (5,'A-B-C-D-E', 'size=S'),
 (6,'ABC-',      'size=;color=x'),
 (7,'Q-1',       'resize=XL');
""")

# the trap: INSTR returns 0 when the delimiter is missing, so INSTR-1 is -1 and INSTR+1 is 1
sql_trap = """
SELECT id, sku,
       SUBSTR(sku, 1, INSTR(sku, '-') - 1) AS naive_first,
       SUBSTR(sku, INSTR(sku, '-') + 1)    AS naive_rest
FROM products WHERE id IN (1, 3) ORDER BY id"""
print("trap (INSTR=0):")
for r in con.execute(sql_trap): print("  ", r)

sql = """
WITH a AS (
  SELECT id, sku, attributes_text,
         CASE WHEN INSTR(sku, '-') > 0 THEN SUBSTR(sku, INSTR(sku, '-') + 1) END AS rest1
  FROM products
), b AS (
  SELECT *, CASE WHEN INSTR(rest1, '-') > 0 THEN SUBSTR(rest1, 1, INSTR(rest1, '-') - 1) ELSE rest1 END AS seg2,
            INSTR(';' || attributes_text, ';size=') AS p
  FROM a
), c AS (
  SELECT *, CASE WHEN p > 0 THEN SUBSTR(';' || attributes_text, p + 6) END AS tail
  FROM b
)
SELECT id,
       CASE WHEN INSTR(sku, '-') > 0 THEN SUBSTR(sku, 1, INSTR(sku, '-') - 1) ELSE sku END AS seg1,
       seg2,
       SUBSTR(sku, LENGTH(RTRIM(sku, REPLACE(sku, '-', ''))) + 1)                         AS seg_last,
       CASE WHEN INSTR(tail, ';') > 0 THEN SUBSTR(tail, 1, INSTR(tail, ';') - 1) ELSE tail END AS size_value
FROM c ORDER BY id"""
sql_df = pd.read_sql(sql, con)
print(sql_df.to_string(index=False))

print("SUBSTR start 0 quirk: SUBSTR('abc', 0, 2) =", repr(con.execute("SELECT SUBSTR('abc', 0, 2)").fetchone()[0]), "(position 0 uses up one character of the length)")

# generic nth segment with a recursive split (Part 9 Q1 mechanics) and with json_each (fragile: breaks on quotes)
rec = """
WITH RECURSIVE sp(id, n, piece, rest) AS (
  SELECT id, 0, '', sku || '-' FROM products WHERE sku IS NOT NULL
  UNION ALL
  SELECT id, n + 1, SUBSTR(rest, 1, INSTR(rest, '-') - 1), SUBSTR(rest, INSTR(rest, '-') + 1)
  FROM sp WHERE rest <> ''
)
SELECT piece FROM sp WHERE id = 5 AND n = 4"""
print("recursive 4th segment of A-B-C-D-E:", con.execute(rec).fetchone()[0])
js = "SELECT value FROM json_each('[\"' || REPLACE((SELECT sku FROM products WHERE id = 5), '-', '\",\"') || '\"]') WHERE key = 3"
print("json_each 4th segment:", con.execute(js).fetchone()[0])

# pandas
p = pd.read_sql("SELECT * FROM products ORDER BY id", con)
parts = p["sku"].str.split("-")                       # list per row (NaN stays NaN)
wide = p["sku"].str.split("-", expand=True)           # one column per segment, None padded
print("expand=True columns:", wide.shape[1]); print(wide.to_string())
pd_df = pd.DataFrame({
    "id": p["id"],
    "seg1": parts.str[0],
    "seg2": parts.str[1],
    "seg_last": parts.str[-1],
    "size_value": p["attributes_text"].str.extract(r"(?:^|;)size=([^;]*)", expand=False),
})

def norm(df):
    return [tuple(None if pd.isna(v) else v for v in row) for row in df.itertuples(index=False)]

# compare after sorting by id (both already ordered by id)
assert norm(sql_df) == norm(pd_df), (norm(sql_df), norm(pd_df))
print("asserts passed (SQL == pandas, ordered by id)")

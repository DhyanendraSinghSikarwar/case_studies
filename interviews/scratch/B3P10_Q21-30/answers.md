### Q21 ⭐⭐ 🟡 Extract the nth field and text between delimiters without split_part: products(sku, attributes_text) where sku looks like 'ABC-123-XL' and 'XY-7-M' (variable length parts) and attributes_text looks like 'color=red;size=M'. Return the first, second and last segment of sku, and the value after 'size=' (up to the next ';' or end of string), using INSTR, SUBSTR and REPLACE tricks, with NULL handling when the delimiter is missing (INSTR returns 0, which makes SUBSTR return the wrong text: show it). Say which approach you would choose when there are more than three segments (recursive split from Part 9 plus a position filter, or JSON tricks, hedged). Mention SPLIT_PART, SUBSTRING_INDEX, SPLIT()[OFFSET] as hedged text. Add the pandas str.split(expand=True) and str.extract versions.
**Asked at:** SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds

**Say this first (1 line):** SQLite has no `split_part`, so I find the delimiter with `INSTR`, cut with `SUBSTR`, and guard every `INSTR` with a `CASE`, because `INSTR` returns 0 when the delimiter is missing and `SUBSTR` then quietly returns the wrong text.

**Schema and sample data:**
```sql
CREATE TABLE products(id INTEGER PRIMARY KEY, sku TEXT, attributes_text TEXT);
INSERT INTO products VALUES
 (1,'ABC-123-XL','color=red;size=M'),
 (2,'XY-7-M',    'color=blue;size=L;fit=slim'),
 (3,'LONE',      'color=green'),
 (4,NULL,        NULL),
 (5,'A-B-C-D-E', 'size=S'),
 (6,'ABC-',      'size=;color=x'),
 (7,'Q-1',       'resize=XL');
```

**SQL answer:** the query `sql` in the Code block. Step `a` drops the first segment (`rest1`), step `b` takes the second segment and finds the position of `';size='`, step `c` cuts the tail after it, and the final SELECT adds the first segment, the last segment and the `size` value. The last segment uses `SUBSTR(sku, LENGTH(RTRIM(sku, REPLACE(sku, '-', ''))) + 1)`: the second argument of `RTRIM` is a set of characters, `REPLACE(sku, '-', '')` is every non-dash character, so `RTRIM` strips the trailing non-dash characters and leaves everything up to and including the last dash. `sql_trap` shows the bug when `INSTR` is 0. For key=value text I search `';' || attributes_text` for `';size='`, so `resize=XL` is not mistaken for `size=`. The recursive split (`rec`) and the `json_each` version are in the Code block for the case of more than three segments.

**pandas answer:** `parts = p["sku"].str.split("-")` gives a list per row; `parts.str[0]`, `parts.str[1]` and `parts.str[-1]` are the first, second and last segment (a missing position gives NaN, a missing sku stays NaN). `str.split("-", expand=True)` gives one column per segment, padded with missing values. The size is `p["attributes_text"].str.extract(r"(?:^|;)size=([^;]*)", expand=False)`. All three are in the Code block as `pd_df`.

**Example:** Row 1, `ABC-123-XL`: `INSTR` finds the first dash at 4, so segment 1 is `SUBSTR(sku, 1, 3)` = `ABC` and `rest1` = `123-XL`. In `rest1` the dash is at 4, so segment 2 = `123`. For the last segment, `REPLACE` gives `ABC123XL`, `RTRIM` strips the trailing `XL` (both letters are in that set) and stops at the dash, leaving `ABC-123-` (length 8), so `SUBSTR(sku, 9)` = `XL`. For the attributes, `';' || 'color=red;size=M'` is `;color=red;size=M`, `';size='` starts at 11, and `SUBSTR(..., 11 + 6)` is `M`; there is no later `;`, so the value is `M`. Row 3, `LONE`: no dash, so segment 1 is the whole string, segment 2 is NULL, the last segment is `LONE`, and there is no `size=`, so NULL. The trap on the same row: `SUBSTR('LONE', 1, INSTR(...) - 1)` is `SUBSTR('LONE', 1, -1)`, which gave an empty string, and `SUBSTR(sku, INSTR(sku, '-') + 1)` is `SUBSTR('LONE', 1)`, which gave `LONE` (not NULL, and not "nothing"). Row 7 has `resize=XL`: the naive `INSTR(attributes_text, 'size=')` would find it inside `resize=`; the `';size='` form returns NULL.

**Code:** run with `python3 -I`.
```python
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
```

**Output (my run):**
```text
trap (INSTR=0):
   (1, 'ABC-123-XL', 'ABC', '123-XL')
   (3, 'LONE', '', 'LONE')
 id seg1 seg2 seg_last size_value
  1  ABC  123       XL          M
  2   XY    7        M          L
  3 LONE  NaN     LONE        NaN
  4  NaN  NaN      NaN        NaN
  5    A    B        E          S
  6  ABC                         
  7    Q    1        1        NaN
SUBSTR start 0 quirk: SUBSTR('abc', 0, 2) = 'a' (position 0 uses up one character of the length)
recursive 4th segment of A-B-C-D-E: D
json_each 4th segment: D
expand=True columns: 5
      0    1    2    3    4
0   ABC  123   XL  NaN  NaN
1    XY    7    M  NaN  NaN
2  LONE  NaN  NaN  NaN  NaN
3   NaN  NaN  NaN  NaN  NaN
4     A    B    C    D    E
5   ABC       NaN  NaN  NaN
6     Q    1  NaN  NaN  NaN
asserts passed (SQL == pandas, ordered by id)
```

**Edge cases:**
- NULL sku or NULL attributes_text: every expression returns NULL (row 4); pandas gives NaN.
- Empty segment is not NULL: `ABC-` gives segment 2 = `''` and last segment = `''` in both SQL and pandas (row 6), and `size=;color=x` gives an empty `size` value, while a missing key gives NULL.
- Fewer segments than asked: `LONE` has no segment 2 (NULL, same as pandas NaN). With the CASE guard this is deliberate; without it you get wrong text.
- Repeated delimiters (`A--B`) produce an empty middle segment; `str.split` does the same.
- `INSTR` is case-sensitive; `SIZE=` would not match `size=`.
- Duplicate keys: `INSTR` finds the first occurrence only.

**Then explain:**
- **Pattern:** position = `INSTR`, left part = `SUBSTR(x, 1, pos - 1)`, right part = `SUBSTR(x, pos + length_of_delimiter)`. Always wrap in `CASE WHEN INSTR(...) > 0`.
- **Why 0 is dangerous:** `INSTR` returns 0 for "not found", so `pos - 1` is -1 and `pos + 1` is 1. SQLite does not raise an error; it returns an empty string or the whole string. I also checked that `SUBSTR('abc', 0, 2)` returns `a`: position 0 uses up one character of the length.
- **Prefix trick for keys:** search for `';key='` inside `';' || text` so the match always starts at a field boundary.
- **More than three segments:** I would use a recursive split (the mechanics are in Part 9 Q1) that returns one row per segment with its position `n`, then filter `n = 4`. In my run it returned `D` for `A-B-C-D-E`. A `json_each` trick (turn `A-B-C` into a JSON array) also worked and returned `D`, but it breaks as soon as the data contains a double quote or backslash, so I would not ship it. Best of all, split once when loading so the segments live in columns.
- **Other engines (not executed here):** `SPLIT_PART(sku, '-', 2)` in PostgreSQL and Snowflake, `SUBSTRING_INDEX` in MySQL, and `SPLIT(sku, '-')[OFFSET(1)]` in BigQuery, as I remember them; check the engine's documentation before relying on them.
- **pandas:** `str.split(expand=True)` and `str.extract` do all of this in one step, and the result matches the SQL on every row (asserted in the Code block, ordered by `id`).

**Follow-ups:**
- *How do you get the last segment when the number of dashes varies?* The `RTRIM`/`REPLACE` trick above, or `str.split(...).str[-1]` in pandas.
- *How do you count the segments?* `LENGTH(sku) - LENGTH(REPLACE(sku, '-', '')) + 1` (not shown in the Code block).
- *Can an index help?* No: `SUBSTR` and `INSTR` on a column prevent index use; store the parsed parts if you filter on them often.

**Common mistakes:**
- Using the `INSTR` result without checking for 0.
- Off-by-one on the delimiter length (`+ 5` for `size=`, `+ 6` for `;size=`).
- Searching for `size=` and matching `resize=`.
- Treating an empty segment as NULL (or the reverse) and then counting wrongly.
- Starting `SUBSTR` at 0.

### Q22 ⭐⭐ 🟡 Type affinity and text-versus-number comparison traps: a table items(item_id, price_text, qty) where price_text is declared TEXT and qty INTEGER, loaded from CSV with values such as '9', '10', '100', '2.5', and a column code declared with no type. Show that ORDER BY price_text gives '10', '100', '2.5', '9', that '10' < '9' is true as text, that 10 < '9' is true because a number sorts before text in a cross-type comparison for a column without affinity, and that the same comparison against an INTEGER-affinity column converts the text. Fix with CAST, with ORDER BY LENGTH(x), x for non-negative integers, and by storing numbers as numbers. Show typeof() on inserted values, the comparison of '1' = 1 for literals versus for columns, and what STRICT tables change (SQLite 3.37 and later). Add the pandas sort_values on strings versus numbers and the natural-sort key technique.
**Asked at:** SQLite lang_corefunc and lang_expr documentation (opened: trim character sets, ASCII-only lower/upper and LIKE, length versus octet_length, concat/concat_ws NULL rules, CAST rules, IS DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL table); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds

**Say this first (1 line):** A column compared with a value gets converted by its declared affinity; literals and columns without a declared type are not, so text and numbers sort and compare differently, and the fix is to store numbers as numbers or to `CAST` explicitly.

**Schema and sample data:**
```sql
CREATE TABLE items(item_id INTEGER PRIMARY KEY, price_text TEXT, qty INTEGER, code);   -- code: no declared type
-- loaded from CSV text, so every value arrives as a string:
INSERT INTO items VALUES (1,'9','3','9'),(2,'10','12','10'),(3,'100','7','100'),(4,'2.5','5','2.5');
```

**SQL answer:** the queries in the Code block: `sql_text_order` (text order), `sql_cast_order` (`CAST(price_text AS REAL)`), `sql_len_order` (`LENGTH(x), x`, which only works for non-negative integers) and `sql_nat` (a natural order for codes like `A9`, `A10`). The comparison counts, the affinity table (`aff`) and the STRICT table (`s`) are in the Code block too.

**pandas answer:** `as_text = pd.read_csv(..., dtype=str)` keeps strings, so `sort_values()` sorts as text; the default `read_csv` turns `price_text` into `float64` and sorts numerically. For `A9, A10, A100` use a key: `nat.sort_values(key=lambda s: s.str.extract(r"(\d+)", expand=False).astype(int))`. Shown in the Code block.

**Example:** The CSV rows are `9, 10, 100, 2.5` for `price_text`. Stored as TEXT they compare character by character: `'1'` is smaller than `'9'`, so `'10'` and `'100'` come before `'9'`, and `'2.5'` starts with `'2'`, so the text order is `10, 100, 2.5, 9`. With `CAST(... AS REAL)` it is `2.5, 9, 10, 100`. The `LENGTH(x), x` trick gives `9, 10, 100, 2.5`: it is right for the integers (length first), but `'2.5'` has length 3, the same as `'100'`, and `'100' < '2.5'` as text, so it lands last. That is why the trick is only for non-negative integers. For comparisons: `price_text < 9` is true for 3 rows (`'10'`, `'100'`, `'2.5'`) because the TEXT column turns the number 9 into the text `'9'`; `qty < '9'` is also true for 3 rows (qty 3, 7, 5) because the INTEGER column turns `'9'` into the number 9; and `code < 9` is true for 0 rows, because `code` has no declared type, nothing is converted, and text is always greater than a number.

**Code:** run with `python3 -I`.
```python
# Q22: type affinity and text-versus-number traps in SQLite, STRICT tables, and the pandas equivalents.
import io
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE items(item_id INTEGER PRIMARY KEY, price_text TEXT, qty INTEGER, code);   -- code: no declared type
""")
csv_text = "item_id,price_text,qty,code\n1,9,3,9\n2,10,12,10\n3,100,7,100\n4,2.5,5,2.5\n"
rows = [tuple(line.split(",")) for line in csv_text.strip().split("\n")[1:]]   # every field arrives as a str, like a CSV
con.executemany("INSERT INTO items VALUES (?,?,?,?)", rows)
print("typeof:", con.execute("SELECT typeof(price_text), typeof(qty), typeof(code) FROM items WHERE item_id = 1").fetchone())

sql_text_order = "SELECT price_text FROM items ORDER BY price_text"
sql_cast_order = "SELECT price_text FROM items ORDER BY CAST(price_text AS REAL)"
sql_len_order  = "SELECT price_text FROM items ORDER BY LENGTH(price_text), price_text"
col = lambda q: [r[0] for r in con.execute(q).fetchall()]
print("ORDER BY price_text            :", col(sql_text_order))
print("ORDER BY CAST(.. AS REAL)      :", col(sql_cast_order))
print("ORDER BY LENGTH(x), x (breaks) :", col(sql_len_order))

print("literals  '10'<'9':", con.execute("SELECT '10' < '9'").fetchone()[0],
      "| 10<'9':", con.execute("SELECT 10 < '9'").fetchone()[0],
      "| '1'=1:", con.execute("SELECT '1' = 1").fetchone()[0])
cmp = lambda q: con.execute(q).fetchone()[0]
print("TEXT col  price_text < 9 (rows true):", cmp("SELECT COUNT(*) FROM items WHERE price_text < 9"))
print("no-type   code < 9       (rows true):", cmp("SELECT COUNT(*) FROM items WHERE code < 9"))
print("INTEGER   qty < '9'      (rows true):", cmp("SELECT COUNT(*) FROM items WHERE qty < '9'"))
print("TEXT col  price_text = 9 (rows true):", cmp("SELECT COUNT(*) FROM items WHERE price_text = 9"))
print("no-type   code = 9       (rows true):", cmp("SELECT COUNT(*) FROM items WHERE code = 9"))

# what each declared affinity does to the same input strings
con.executescript("CREATE TABLE aff(i INTEGER, n NUMERIC, r REAL, t TEXT, a);")
for v in ("12", " 12", "12 ", "1e3", "2.50", "007", "0x10", "abc"):
    con.execute("INSERT INTO aff VALUES (?,?,?,?,?)", (v,) * 5)
print("raw value | INTEGER | NUMERIC | REAL | TEXT | no type")
for r in con.execute("SELECT quote(t), typeof(i)||':'||quote(i), typeof(n)||':'||quote(n), typeof(r)||':'||quote(r), typeof(t), typeof(a) FROM aff"):
    print("  ", " | ".join(r))

# STRICT tables (SQLite 3.37+)
con.executescript("CREATE TABLE s(a INTEGER, b TEXT, c ANY) STRICT;")
for label, args in [("'12' into INTEGER", ("12", "x", 1)), ("' 12' into INTEGER", (" 12", "x", 1)),
                    ("'abc' into INTEGER", ("abc", "x", 1)), ("2.5 into INTEGER", (2.5, "x", 1)),
                    ("3.0 into INTEGER", (3.0, "x", 1)), ("5 into TEXT", (1, 5, 1)), ("'z' into ANY", (1, "x", "z"))]:
    try:
        con.execute("INSERT INTO s VALUES (?,?,?)", args); print("  STRICT ok  :", label)
    except sqlite3.Error as e:
        print("  STRICT FAIL:", label, "->", e)
print("  stored:", con.execute("SELECT a, typeof(a), b, typeof(b), c, typeof(c) FROM s").fetchall())

# natural sort of codes with a text prefix
con.executescript("CREATE TABLE codes(c TEXT); INSERT INTO codes VALUES ('A9'),('A10'),('A100'),('A2');")
sql_nat = "SELECT c FROM codes ORDER BY CAST(SUBSTR(c, 2) AS INTEGER)"
print("plain order:", col("SELECT c FROM codes ORDER BY c"), "| natural order:", col(sql_nat))

# pandas
df = pd.read_sql("SELECT * FROM items ORDER BY item_id", con)
print("pandas dtypes from SQL:", dict(df.dtypes.astype(str)))   # price_text stays str, qty int64
as_text = pd.read_csv(io.StringIO(csv_text), dtype=str)
as_num = pd.read_csv(io.StringIO(csv_text))
print("read_csv default dtypes:", dict(as_num.dtypes.astype(str)))
print("string sort :", as_text["price_text"].sort_values().tolist())
print("numeric sort:", as_num["price_text"].sort_values().tolist())
nat = pd.Series(["A9", "A10", "A100", "A2"])
nat_sorted = nat.sort_values(key=lambda s: s.str.extract(r"(\d+)", expand=False).astype(int)).tolist()
print("natural key :", nat_sorted)
na_csv = pd.read_csv(io.StringIO("code,n\nNA,1\nnull,2\nNone,3\nN/A,4\nnan,5\nxyz,6\n"))
print("read_csv NA markers -> NaN:", na_csv["code"].isna().tolist(), "| keep_default_na=False:",
      pd.read_csv(io.StringIO("code,n\nNA,1\nnull,2\nxyz,3\n"), keep_default_na=False)["code"].tolist())

assert col(sql_text_order) == sorted(as_text["price_text"]) == ["10", "100", "2.5", "9"]
assert col(sql_cast_order) == as_text.sort_values("price_text", key=lambda s: s.astype(float))["price_text"].tolist() == ["2.5", "9", "10", "100"]
assert col(sql_nat) == nat_sorted == ["A2", "A9", "A10", "A100"]
print("asserts passed (SQL == pandas for the three orderings)")
```

**Output (my run):**
```text
typeof: ('text', 'integer', 'text')
ORDER BY price_text            : ['10', '100', '2.5', '9']
ORDER BY CAST(.. AS REAL)      : ['2.5', '9', '10', '100']
ORDER BY LENGTH(x), x (breaks) : ['9', '10', '100', '2.5']
literals  '10'<'9': 1 | 10<'9': 1 | '1'=1: 0
TEXT col  price_text < 9 (rows true): 3
no-type   code < 9       (rows true): 0
INTEGER   qty < '9'      (rows true): 3
TEXT col  price_text = 9 (rows true): 1
no-type   code = 9       (rows true): 0
raw value | INTEGER | NUMERIC | REAL | TEXT | no type
   '12' | integer:12 | integer:12 | real:12.0 | text | text
   ' 12' | integer:12 | integer:12 | real:12.0 | text | text
   '12 ' | integer:12 | integer:12 | real:12.0 | text | text
   '1e3' | integer:1000 | integer:1000 | real:1000.0 | text | text
   '2.50' | real:2.5 | real:2.5 | real:2.5 | text | text
   '007' | integer:7 | integer:7 | real:7.0 | text | text
   '0x10' | text:'0x10' | text:'0x10' | text:'0x10' | text | text
   'abc' | text:'abc' | text:'abc' | text:'abc' | text | text
  STRICT ok  : '12' into INTEGER
  STRICT ok  : ' 12' into INTEGER
  STRICT FAIL: 'abc' into INTEGER -> cannot store TEXT value in INTEGER column s.a
  STRICT FAIL: 2.5 into INTEGER -> cannot store REAL value in INTEGER column s.a
  STRICT ok  : 3.0 into INTEGER
  STRICT ok  : 5 into TEXT
  STRICT ok  : 'z' into ANY
  stored: [(12, 'integer', 'x', 'text', 1, 'integer'), (12, 'integer', 'x', 'text', 1, 'integer'), (3, 'integer', 'x', 'text', 1, 'integer'), (1, 'integer', '5', 'text', 1, 'integer'), (1, 'integer', 'x', 'text', 'z', 'text')]
plain order: ['A10', 'A100', 'A2', 'A9'] | natural order: ['A2', 'A9', 'A10', 'A100']
pandas dtypes from SQL: {'item_id': 'int64', 'price_text': 'str', 'qty': 'int64', 'code': 'str'}
read_csv default dtypes: {'item_id': 'int64', 'price_text': 'float64', 'qty': 'int64', 'code': 'float64'}
string sort : ['10', '100', '2.5', '9']
numeric sort: [2.5, 9.0, 10.0, 100.0]
natural key : ['A2', 'A9', 'A10', 'A100']
read_csv NA markers -> NaN: [True, True, True, True, True, False] | keep_default_na=False: ['NA', 'null', 'xyz']
asserts passed (SQL == pandas for the three orderings)
```

**Edge cases:**
- The same input text under each affinity (Code block, `aff` table): `' 12'` and `'12 '` (leading or trailing space) became the integer 12 in INTEGER and NUMERIC columns and the real 12.0 in a REAL column, `'1e3'` became integer 1000, `'007'` became 7 (the zeros are lost), `'2.50'` became real 2.5, and `'0x10'` and `'abc'` stayed text. TEXT and no-type columns keep the string as given. These are my runs on SQLite 3.45.1.
- STRICT tables (SQLite 3.37 and later): an INTEGER column accepted `'12'` and `' 12'` (converted to 12), accepted `3.0` (stored as 3), and rejected `'abc'` (`cannot store TEXT value in INTEGER column s.a`) and `2.5` (`cannot store REAL value in INTEGER column s.a`). A TEXT column converted the integer 5 to `'5'`. An `ANY` column keeps whatever type arrives. So STRICT stops garbage but does not stop a numeric-looking string from being converted.
- NULL: `NULL < 9` is NULL for all of these, so NULL rows never show up in either direction.
- Negative numbers and decimals break the `LENGTH(x), x` trick (`'-5'` has length 2).
- pandas: `read_csv` treats `NA`, `null`, `None`, `N/A` and `nan` as missing by default (all five became NaN in my run), so a country code `NA` silently becomes missing; use `keep_default_na=False` or `na_values=[...]`.

**Then explain:**
- **Rule in one line:** if one side is a column with INTEGER, REAL or NUMERIC affinity, the other side is converted to a number when it looks like one; if one side has TEXT affinity and the other no affinity, the number is converted to text; literals alone get no conversion, so `'1' = 1` is false (my run: 0).
- **Cross-type order:** with no conversion a number is always smaller than text (`10 < '9'` is 1).
- **Fix:** best is to load numbers into INTEGER or REAL columns (or `CAST` while loading). Use `CAST` in the query when you cannot change the table; use `LENGTH(x), x` only for non-negative integers; use a natural-sort key for mixed codes.
- **Casting garbage:** `CAST('abc' AS REAL)` is 0.0, not an error, so a failed cast hides bad data (Q24 has the same trap for dates). Use `GLOB '*[^0-9]*'` or a round-trip check to find bad rows.
- **pandas:** `read_csv` infers dtypes for you, so check `dtypes` after loading. Sorting `str` values is lexicographic, exactly like SQLite's text order.
- Other engines are stricter (they usually raise an error on `'abc' < 5` or convert by their own rules); I did not execute any of them here.

**Follow-ups:**
- *Why did `' 12'` become an integer?* The INTEGER affinity accepts text that looks like a number, including surrounding spaces; `TEXT` affinity does not. I ran this; I did not find it stated in the pages opened for the Wave A note.
- *What would STRICT have changed?* It rejects `'abc'` and `2.5` in an INTEGER column with an error, instead of storing text.
- *How do you sort `v1.2`, `v1.10`?* Split into numeric parts and sort on those (a key function in pandas; two `CAST`s in SQL).

**Common mistakes:**
- Sorting numbers stored as text and trusting the order.
- Assuming a column named `price` is numeric because the values look numeric.
- Comparing a no-type column with a number and getting 0 rows without an error.
- Using `LENGTH(x), x` on decimals or negatives.
- Letting `read_csv` guess: `NA` becomes NaN, and `007` becomes 7.

### Q23 ⭐⭐ 🟡 Padding, truncation and number-to-string formatting: invoices(invoice_no, amount, customer_name). SQLite has no LPAD or RPAD: build zero-padded invoice codes ('INV-00042') with SUBSTR('00000' || n, -5) and with PRINTF('%05d'), left-justify with PRINTF('%-10s'), truncate names to 10 characters with an ellipsis, and format amounts as '1,234.50' (PRINTF with a thousands comma flag: test it on 3.45.1 and say it is not portable) and as rounded strings. Show that ROUND(703.125, 2) is 703.13 in SQLite and PRINTF('%.2f') may differ in the last digit for binary floats, and what happens with a negative width or a number longer than the pad (SUBSTR cuts digits). State LPAD, RPAD (PostgreSQL, MySQL, Oracle), FORMAT (SQL Server, MySQL) and TO_CHAR as hedged text. Add the pandas str.zfill, str.pad, f-string and round (banker's rounding) comparison.
**Asked at:** SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds

**Say this first (1 line):** SQLite has no `LPAD`/`RPAD`; use `PRINTF('%05d', n)` for zero padding (it never cuts digits), and treat `SUBSTR('00000' || n, -5)` as a trick that silently drops digits when the number is longer than the pad.

**Schema and sample data:**
```sql
CREATE TABLE invoices(invoice_no INTEGER PRIMARY KEY, amount REAL, customer_name TEXT);
INSERT INTO invoices VALUES
 (42,     1234.5,      'Alexander Hamilton'),
 (7,      0.5,         'Bo'),
 (123456, 1234567.891, 'Christopher Robin'),
 (99999,  703.125,     'Dee'),
 (5,      NULL,        NULL);
```

**SQL answer:** the single query `sql` in the Code block: `code_substr`, `code_printf` (`PRINTF('INV-%05d', invoice_no)`), `name_left` (`PRINTF('%-10s|', customer_name)`), `name_trunc` (first 9 characters plus an ellipsis when longer than 10), and `amount_comma` (`PRINTF('%,.2f', amount)`). Extra checks (negative numbers, NULL, rounding) follow it.

**pandas answer:** `pd_df` in the Code block: `str.zfill(5)` on the string version of the number, `str.ljust(10)` (or `str.pad(10, side="right")`), `str[:9]` plus an ellipsis, and an f-string `f"{x:,.2f}"` for the amount; `Series.round(2)` is shown separately.

**Example:** Invoice 42: `'00000' || 42` is `0000042`, and the last 5 characters are `00042`, so `INV-00042`. Invoice 123456 has 6 digits: `'00000123456'` last 5 characters are `23456`, so the trick prints `INV-23456` (wrong, and it can collide with invoice 23456), while `PRINTF('%05d')` prints `INV-123456`. A negative number goes wrong too: `'00000' || -42` ends `...00-42`, giving `INV-00-42`, while `PRINTF` gives `INV--0042`. The name `Alexander Hamilton` has 18 characters, so we keep 9 (`Alexander`) and add `…`; `Bo` is left as is and padded to 10 by `%-10s`. Amount 1234.5 becomes `1,234.50`. Invoice 99999 has amount 703.125: SQLite prints `703.13`, Python and pandas print `703.12` (see Edge cases).

**Code:** run with `python3 -I`.
```python
# Q23: padding, truncation and number formatting in SQLite (no LPAD/RPAD) versus pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE invoices(invoice_no INTEGER PRIMARY KEY, amount REAL, customer_name TEXT);
INSERT INTO invoices VALUES
 (42,     1234.5,      'Alexander Hamilton'),
 (7,      0.5,         'Bo'),
 (123456, 1234567.891, 'Christopher Robin'),
 (99999,  703.125,     'Dee'),
 (5,      NULL,        NULL);
""")

sql = """
SELECT invoice_no,
       'INV-' || SUBSTR('00000' || invoice_no, -5)                          AS code_substr,
       PRINTF('INV-%05d', invoice_no)                                       AS code_printf,
       PRINTF('%-10s|', customer_name)                                      AS name_left,
       CASE WHEN LENGTH(customer_name) > 10 THEN SUBSTR(customer_name, 1, 9) || '…' ELSE customer_name END AS name_trunc,
       PRINTF('%,.2f', amount)                                              AS amount_comma
FROM invoices ORDER BY invoice_no"""
sql_df = pd.read_sql(sql, con)
print(sql_df.to_string(index=False))

print("negative number:", con.execute("SELECT 'INV-' || SUBSTR('00000' || -42, -5), PRINTF('INV-%05d', -42)").fetchone())
print("NULL: || gives", con.execute("SELECT 'N:' || NULL").fetchone()[0], "| printf %s gives", repr(con.execute("SELECT PRINTF('%s', NULL)").fetchone()[0]),
      "| printf %d gives", repr(con.execute("SELECT PRINTF('%d', NULL)").fetchone()[0]))
print("right-justify:", repr(con.execute("SELECT PRINTF('%10s', 'abc')").fetchone()[0]))

# rounding: ROUND versus PRINTF, and Python/pandas
q = con.execute("""SELECT ROUND(703.125, 2), PRINTF('%.2f', 703.125), ROUND(2.675, 2), PRINTF('%.2f', 2.675),
                          ROUND(1.005, 2), PRINTF('%.2f', 1.005), ROUND(0.125, 2), PRINTF('%.2f', 0.125)""").fetchone()
print("SQLite ROUND/PRINTF 703.125, 2.675, 1.005, 0.125:", q)
print("Python round / format 703.125, 2.675, 1.005, 0.125:",
      (round(703.125, 2), f"{703.125:.2f}", round(2.675, 2), f"{2.675:.2f}", round(1.005, 2), f"{1.005:.2f}", round(0.125, 2), f"{0.125:.2f}"))
print("pandas Series.round(2) of the same four:", pd.Series([703.125, 2.675, 1.005, 0.125]).round(2).tolist())
print("PRINTF('%.0f') of 0.6, 1.6, 2.5, 2.6:", con.execute("SELECT PRINTF('%.0f',0.6), PRINTF('%.0f',1.6), PRINTF('%.0f',2.5), PRINTF('%.0f',2.6)").fetchone(),
      "| ROUND first:", con.execute("SELECT PRINTF('%.0f',ROUND(0.6)), PRINTF('%.0f',ROUND(1.6)), PRINTF('%.0f',ROUND(2.5)), PRINTF('%.0f',ROUND(2.6))").fetchone())

# pandas
p = pd.read_sql("SELECT * FROM invoices ORDER BY invoice_no", con)
pd_df = pd.DataFrame({
    "invoice_no": p["invoice_no"],
    "code_substr": "INV-" + p["invoice_no"].astype(str).str.zfill(5).str[-5:],          # same cut as SUBSTR(...,-5)
    "code_printf": p["invoice_no"].map(lambda n: f"INV-{n:05d}"),
    "name_left": p["customer_name"].str.ljust(10) + "|",
    "name_trunc": p["customer_name"].where(p["customer_name"].str.len() <= 10, p["customer_name"].str[:9] + "…"),
    "amount_comma": p["amount"].map(lambda x: None if pd.isna(x) else f"{x:,.2f}"),
})
print("SQL PRINTF('%,.2f', NULL):", repr(con.execute("SELECT PRINTF('%,.2f', NULL)").fetchone()[0]))
print("pad/justify/zfill in pandas:", pd.Series([7]).astype(str).str.zfill(5).tolist(), pd.Series(["ab"]).str.pad(6, side="left").tolist(),
      pd.Series(["-42"]).str.zfill(5).tolist())

def norm(df):
    return [tuple(None if (not isinstance(v, str) and pd.isna(v)) else v for v in row) for row in df.itertuples(index=False)]

s_rows, p_rows = norm(sql_df), norm(pd_df)
# the amount 703.125 row differs on purpose: SQLite rounds the exact tie up, Python's format rounds half to even
tie = [i for i, r in enumerate(s_rows) if r[0] == 99999][0]
assert s_rows[tie][5] == "703.13" and p_rows[tie][5] == "703.12"
for i, (a, b) in enumerate(zip(s_rows, p_rows)):
    if a[0] == 5:                      # NULL row: SQL PRINTF turns NULL into '' / 0.00, pandas keeps NaN (None here)
        assert a[3] == "          |" and b[3] is None and a[5] == "0.00" and b[5] is None
        continue
    cols = range(5) if i == tie else range(6)
    assert all(a[j] == b[j] for j in cols), (a, b)
print("asserts passed (SQL == pandas on every cell, except the two documented differences: the 703.125 tie and the NULL row)")
```

**Output (my run):**
```text
 invoice_no code_substr code_printf           name_left name_trunc amount_comma
          5   INV-00005   INV-00005                   |        NaN         0.00
          7   INV-00007   INV-00007         Bo        |         Bo         0.50
         42   INV-00042   INV-00042 Alexander Hamilton| Alexander…     1,234.50
      99999   INV-99999   INV-99999         Dee       |        Dee       703.13
     123456   INV-23456  INV-123456  Christopher Robin| Christoph… 1,234,567.89
negative number: ('INV-00-42', 'INV--0042')
NULL: || gives None | printf %s gives '' | printf %d gives '0'
right-justify: '       abc'
SQLite ROUND/PRINTF 703.125, 2.675, 1.005, 0.125: (703.13, '703.13', 2.67, '2.67', 1.0, '1.00', 0.13, '0.13')
Python round / format 703.125, 2.675, 1.005, 0.125: (703.12, '703.12', 2.67, '2.67', 1.0, '1.00', 0.12, '0.12')
pandas Series.round(2) of the same four: [703.12, 2.68, 1.0, 0.12]
PRINTF('%.0f') of 0.6, 1.6, 2.5, 2.6: ('0', '1', '2', '2') | ROUND first: ('1', '2', '3', '3')
SQL PRINTF('%,.2f', NULL): '0.00'
pad/justify/zfill in pandas: ['00007'] ['    ab'] ['-0042']
asserts passed (SQL == pandas on every cell, except the two documented differences: the 703.125 tie and the NULL row)
```

**Edge cases:**
- **Rounding differs by tool (my run):** `ROUND(703.125, 2)` and `PRINTF('%.2f', 703.125)` both gave 703.13 (SQLite rounds the exact tie up); Python's `round` and f-string gave 703.12; `Series.round(2)` gave 703.12 for 703.125, **2.68** for 2.675 (SQLite and Python both gave 2.67) and 0.12 for 0.125. So even pandas and Python round differently on 2.675. The stored double for 2.675 is just below the tie, so 2.67 is the exact answer; pandas' 2.68 presumably comes from scaling by 100 before rounding (I did not verify the mechanism). Compare money in integer cents, or use `decimal`.
- **`PRINTF('%.0f')` truncates in this SQLite build:** `0.6`, `1.6` and `2.6` printed `0`, `1`, `2`, and after `ROUND` first they printed `1`, `2`, `3`. The Wave A note guessed half-to-even rounding; the run shows truncation, so round first.
- **NULL:** `'N:' || NULL` is NULL, but `PRINTF('%s', NULL)` is an empty string and `PRINTF('%d', NULL)` is `0`; `PRINTF('%,.2f', NULL)` printed `0.00`, which looks like a real amount. Guard with `CASE WHEN amount IS NULL THEN NULL ELSE ... END`. pandas keeps NaN.
- **Longer than the pad:** `%05d` and `zfill` do not cut; `SUBSTR(..., -5)` does.
- **Negative width or number:** shown above; `zfill` keeps the sign first (`'-42'.zfill(5)` is `-0042`, same as `PRINTF`).
- **Thousands comma:** `%,d` and `%,.2f` worked in this SQLite 3.45.1 build; it is a SQLite extension I did not find documented in the pages opened, so do not rely on it in other engines.

**Then explain:**
- **Why `SUBSTR(..., -5)` works:** a negative start counts from the right, so it takes the last 5 characters. It is only safe when the number is known to have at most 5 digits and is not negative.
- **Left-justify and truncate:** `%-10s` pads on the right; for truncation use `SUBSTR` with an ellipsis (here a single character, so the total is 10). `LENGTH` counts characters, `OCTET_LENGTH` counts bytes.
- **Rounded strings:** `PRINTF('%.2f', x)` returns text, `ROUND(x, 2)` returns a number; do the arithmetic before formatting.
- **Other engines (not executed here):** `LPAD`/`RPAD` exist in PostgreSQL, MySQL and Oracle; SQL Server has `FORMAT` and `RIGHT('00000' || ...)`-style tricks; `TO_CHAR(n, 'FM00000')` in PostgreSQL and Oracle; MySQL also has `FORMAT(x, 2)`. I wrote these from memory.
- **pandas:** `zfill`, `pad`, `ljust` and f-strings match the SQL on every cell I asserted; the only differences are the 703.125 tie and the NULL row (asserted in the Code block).

**Follow-ups:**
- *How do you pad on the right with a custom character?* `SUBSTR(n || 'XXXXX', 1, 5)`-style tricks in SQLite (not run here), `str.pad(width, side="right", fillchar="x")` in pandas.
- *Why not `FORMAT` in SQLite?* `FORMAT` exists as an alias of `PRINTF` in this build, but other engines' `FORMAT` has different codes.
- *Should the invoice code be stored?* Store the integer and format on output; a padded string sorts correctly only while the width is fixed.

**Common mistakes:**
- Using `SUBSTR('0000' || n, -5)` with a short pad and losing digits.
- Formatting before summing (strings do not add).
- Assuming `PRINTF` of NULL gives NULL.
- Trusting `PRINTF('%.0f')` to round.
- Expecting SQL, Python and pandas to round a tie the same way.

### Q24 ⭐⭐ 🟡 String-to-date casting traps: raw_dates(id, d_text) with '2024-03-05', '2024-3-5', '05/03/2024', '2024-03-05 14:30', '20240305', '2024-02-30' and ''. Show what DATE(d_text) returns for each in SQLite (NULL for non-ISO shapes, not an error), why '05/03/2024' is ambiguous (5 March or 3 May), how to parse a dd/mm/yyyy string with SUBSTR into ISO form, and how to detect rows that failed to parse (WHERE DATE(x) IS NULL AND x <> ''). Show that '2024-02-30' returns NULL too. State TO_DATE (PostgreSQL, Oracle), STR_TO_DATE (MySQL), TRY_CONVERT (SQL Server) and SAFE.PARSE_DATE (BigQuery) as hedged text. Add pandas to_datetime with errors='coerce', format='mixed' and dayfirst, and show the same ambiguous string parsed two ways. Cross-reference Part 6 Q1 for date storage in SQLite.
**Asked at:** SQLite lang_corefunc and lang_expr documentation (opened: trim character sets, ASCII-only lower/upper and LIKE, length versus octet_length, concat/concat_ws NULL rules, CAST rules, IS DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL table); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds

**Say this first (1 line):** `DATE()` in SQLite returns NULL for anything that is not an ISO shape (no error), but it also quietly "fixes" impossible days such as `2024-02-30` into `2024-03-01`, so you need a round-trip check to find bad rows.

**Schema and sample data:**
```sql
CREATE TABLE raw_dates(id INTEGER PRIMARY KEY, d_text TEXT);
INSERT INTO raw_dates VALUES
 (1,'2024-03-05'),(2,'2024-3-5'),(3,'05/03/2024'),(4,'2024-03-05 14:30'),
 (5,'20240305'),(6,'2024-02-30'),(7,''),(8,NULL);
```

**SQL answer:** `sql_failed` (rows that fail to parse: `WHERE DATE(d_text) IS NULL AND d_text <> ''`) and `sql_clean` (a `CASE` with one branch per shape: ISO with or without time, `dd/mm/yyyy` rebuilt with `SUBSTR`, `yyyymmdd` rebuilt with `SUBSTR`, each branch guarded by `GLOB` and by a round-trip test `DATE(x) = x`) are in the Code block.

**pandas answer:** `pd.to_datetime(d, errors="coerce")`, `format="mixed"` and `dayfirst=True` are printed in the Code block. The comparable version parses each shape with an explicit format (`str.fullmatch` masks plus `format="%d/%m/%Y"` and so on) and gives the same result as the SQL `CASE`.

**Example:** Row 1 `2024-03-05` parses. Row 2 `2024-3-5` is NULL (SQLite needs two-digit month and day). Row 3 `05/03/2024` is NULL, and a human cannot tell whether it is 5 March or 3 May; my rule says day first, so the `SUBSTR` rebuild gives `2024-03-05`. Row 4 `2024-03-05 14:30` gives `2024-03-05` (a time part is accepted). Row 5 `20240305` is NULL for `DATE()`; the `GLOB` branch rebuilds it as `2024-03-05`. Row 6 `2024-02-30`: **`DATE()` returned `2024-03-01`, not NULL** (the question text assumes NULL; this run says otherwise). Only the round-trip check `DATE(x) = x` catches it (`2024-03-01` is not equal to `2024-02-30`), so the CASE returns NULL. Rows 7 and 8 (empty and NULL) are NULL; `sql_failed` skips them because of `d_text <> ''` and because `NULL <> ''` is not true. Failed rows: 2, 3 and 5.

**Code:** run with `python3 -I`.
```python
# Q24: string-to-date casting traps in SQLite and pandas.
import sqlite3
import warnings
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE raw_dates(id INTEGER PRIMARY KEY, d_text TEXT);
INSERT INTO raw_dates VALUES
 (1,'2024-03-05'),(2,'2024-3-5'),(3,'05/03/2024'),(4,'2024-03-05 14:30'),
 (5,'20240305'),(6,'2024-02-30'),(7,''),(8,NULL);
""")

print("DATE() per row:")
for r in con.execute("SELECT id, quote(d_text), DATE(d_text) FROM raw_dates ORDER BY id"): print("  ", r)
print("DATE of 2023-02-29 and 2024-04-31:", con.execute("SELECT DATE('2023-02-29'), DATE('2024-04-31')").fetchone())

print("other invalid shapes:", con.execute("SELECT DATE('2024-13-01'), DATE('2024-00-10'), DATE('2024-02-32')").fetchone())
sql_failed = "SELECT id FROM raw_dates WHERE DATE(d_text) IS NULL AND d_text <> '' ORDER BY id"
print("rows that failed to parse:", [r[0] for r in con.execute(sql_failed)])

# a strict round-trip check catches impossible dates that SQLite normalises (Feb 30 -> Mar 01)
sql_clean = """
SELECT id,
       CASE
         WHEN d_text GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]*'
              AND DATE(SUBSTR(d_text, 1, 10)) = SUBSTR(d_text, 1, 10)            THEN SUBSTR(d_text, 1, 10)
         WHEN d_text GLOB '[0-3][0-9]/[0-1][0-9]/[0-9][0-9][0-9][0-9]'
              AND DATE(SUBSTR(d_text,7,4)||'-'||SUBSTR(d_text,4,2)||'-'||SUBSTR(d_text,1,2))
                  = SUBSTR(d_text,7,4)||'-'||SUBSTR(d_text,4,2)||'-'||SUBSTR(d_text,1,2)
                                                                                THEN SUBSTR(d_text,7,4)||'-'||SUBSTR(d_text,4,2)||'-'||SUBSTR(d_text,1,2)
         WHEN d_text GLOB '[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9]'
              AND DATE(SUBSTR(d_text,1,4)||'-'||SUBSTR(d_text,5,2)||'-'||SUBSTR(d_text,7,2))
                  = SUBSTR(d_text,1,4)||'-'||SUBSTR(d_text,5,2)||'-'||SUBSTR(d_text,7,2)
                                                                                THEN SUBSTR(d_text,1,4)||'-'||SUBSTR(d_text,5,2)||'-'||SUBSTR(d_text,7,2)
       END AS iso
FROM raw_dates ORDER BY id"""
sql_df = pd.read_sql(sql_clean, con)
print(sql_df.to_string(index=False))

# pandas
p = pd.read_sql("SELECT * FROM raw_dates ORDER BY id", con)
d = p["d_text"]
print("coerce (format inferred from first value):", pd.to_datetime(d, errors="coerce").dt.strftime("%Y-%m-%d").tolist())
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    mixed = pd.to_datetime(d, format="mixed", errors="coerce")
    print("format='mixed':", mixed.dt.strftime("%Y-%m-%d").tolist(), "| warnings:", [type(x).__name__ for x in w])
dayfirst = pd.to_datetime(d, format="mixed", dayfirst=True, errors="coerce")
print("format='mixed', dayfirst=True:", dayfirst.dt.strftime("%Y-%m-%d").tolist())
print("same string two ways:", pd.to_datetime("05/03/2024", format="%m/%d/%Y").date(), "vs", pd.to_datetime("05/03/2024", format="%d/%m/%Y").date())
try:
    pd.to_datetime(d.dropna(), format="%Y-%m-%d")
except Exception as e:
    print("errors='raise' (default):", type(e).__name__)

# explicit per-shape parsing, the same rules as the SQL CASE
iso = d.str.fullmatch(r"\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?", na=False)
dmy = d.str.fullmatch(r"\d{2}/\d{2}/\d{4}", na=False)
compact = d.str.fullmatch(r"\d{8}", na=False)
parsed = pd.Series(pd.NaT, index=p.index, dtype="datetime64[ns]")
parsed[iso] = pd.to_datetime(d[iso].str[:10], format="%Y-%m-%d", errors="coerce")
parsed[dmy] = pd.to_datetime(d[dmy], format="%d/%m/%Y", errors="coerce")
parsed[compact] = pd.to_datetime(d[compact], format="%Y%m%d", errors="coerce")
pd_df = pd.DataFrame({"id": p["id"], "iso": parsed.dt.strftime("%Y-%m-%d")})
print(pd_df.to_string(index=False))

norm = lambda df: [tuple(None if pd.isna(v) else v for v in row) for row in df.itertuples(index=False)]
assert norm(sql_df) == norm(pd_df), (norm(sql_df), norm(pd_df))
print("asserts passed (SQL CASE parse == pandas per-shape parse, ordered by id)")
```

**Output (my run):**
```text
DATE() per row:
   (1, "'2024-03-05'", '2024-03-05')
   (2, "'2024-3-5'", None)
   (3, "'05/03/2024'", None)
   (4, "'2024-03-05 14:30'", '2024-03-05')
   (5, "'20240305'", None)
   (6, "'2024-02-30'", '2024-03-01')
   (7, "''", None)
   (8, 'NULL', None)
DATE of 2023-02-29 and 2024-04-31: ('2023-03-01', '2024-05-01')
other invalid shapes: (None, None, None)
rows that failed to parse: [2, 3, 5]
 id        iso
  1 2024-03-05
  2        NaN
  3 2024-03-05
  4 2024-03-05
  5 2024-03-05
  6        NaN
  7        NaN
  8        NaN
coerce (format inferred from first value): ['2024-03-05', '2024-03-05', nan, nan, nan, nan, nan, nan]
format='mixed': ['2024-03-05', '2024-03-05', '2024-05-03', '2024-03-05', '2024-03-05', nan, nan, nan] | warnings: []
format='mixed', dayfirst=True: ['2024-05-03', '2024-05-03', '2024-03-05', '2024-05-03', '2024-05-03', nan, nan, nan]
same string two ways: 2024-05-03 vs 2024-03-05
errors='raise' (default): ValueError
 id        iso
  1 2024-03-05
  2        NaN
  3 2024-03-05
  4 2024-03-05
  5 2024-03-05
  6        NaN
  7        NaN
  8        NaN
asserts passed (SQL CASE parse == pandas per-shape parse, ordered by id)
```

**Edge cases:**
- **Impossible dates are normalised, not rejected:** `DATE('2024-02-30')` gave `2024-03-01`, `DATE('2023-02-29')` gave `2023-03-01`, `DATE('2024-04-31')` gave `2024-05-01`. A month 13, month 00 or day 32 does give NULL (`2024-13-01`, `2024-00-10`, `2024-02-32` all returned NULL in my run). So the question's claim that `2024-02-30` returns NULL is wrong for SQLite 3.45.1.
- **Empty string and NULL:** both give NULL; separate them with `d_text <> ''` and `IS NOT NULL` if you need to report them differently.
- **Ambiguity:** `05/03/2024` has no right answer without a rule from the source system; do not guess per row.
- **pandas:** `to_datetime(d, errors="coerce")` took its format from the first value and gave `NaT` for the slash form, the compact form and the `14:30` form (`2024-3-5` still parsed). `format="mixed"` parsed `05/03/2024` as **3 May** (month first) and everything else as 5 March. `format="mixed", dayfirst=True` gave 5 March for the slash form but also turned the ISO strings `2024-03-05` into **3 May**, so do not use `dayfirst` on a column that also has ISO values. `2024-02-30` is `NaT` in pandas (no normalisation). Without `errors="coerce"` a bad value raises `ValueError`.
- The same string parsed two ways: `format="%m/%d/%Y"` gave 2024-05-03 and `format="%d/%m/%Y"` gave 2024-03-05.

**Then explain:**
- **ISO is the shape to rely on for SQLite date functions** (with the quirk above); store dates as `YYYY-MM-DD` text (Part 6 Q1 covers storage).
- **Detect failures:** `DATE(x) IS NULL AND x <> ''`, plus the round-trip test to catch normalised days.
- **Fix known shapes explicitly:** `GLOB` guard, then `SUBSTR` rebuild, then validate.
- **Other engines (not executed here, from memory):** `TO_DATE` (PostgreSQL, Oracle) and `STR_TO_DATE` (MySQL) take a format string; `TRY_CONVERT` (SQL Server) and `SAFE.PARSE_DATE` (BigQuery) return NULL instead of raising an error. Some of them raise errors on invalid input, unlike SQLite.
- **pandas:** be explicit with `format=`; `errors="coerce"` hides failures, so count the `NaT` rows against the input afterwards (`d.notna() & parsed.isna()`).

**Follow-ups:**
- *How would you report the bad rows?* `WHERE DATE(x) IS NULL AND x <> ''` plus the round-trip mismatch, with a count per shape.
- *Why not `CAST(x AS DATE)`?* SQLite has no date type; `CAST('2024-03-05' AS INTEGER)` and `AS NUMERIC` both gave 2024 in my check, which looks fine and is wrong.

**Common mistakes:**
- Believing `DATE()` returns NULL for every impossible date.
- Assuming `dd/mm/yyyy` without asking the source.
- Letting `errors="coerce"` swallow bad rows without counting them.
- Using `dayfirst=True` on a mixed column and flipping the ISO values.
- Comparing date strings that are not zero-padded (`'2024-3-5' > '2024-12-01'` is true as text).

### Q25 ⭐⭐ 🟡 NULL in DISTINCT, GROUP BY, UNION, INTERSECT, EXCEPT and COUNT(DISTINCT): contacts_a(email) and contacts_b(email) with NULLs and repeated values. Show that GROUP BY and DISTINCT put all NULLs in one group, that UNION, INTERSECT and EXCEPT treat NULLs as equal (so NULL INTERSECT NULL returns a row although NULL = NULL is not true), that COUNT(DISTINCT email) ignores NULL but SELECT DISTINCT email returns one NULL row, and that NULL does not match in a join or IN. Give the interview line 'comparison operators say unknown, set operators say same'. Show the difference between NOT IN and EXCEPT on the same data (the NOT IN with NULL trap is in Part 3 Q3, do not repeat). Add the pandas drop_duplicates, nunique(dropna=...) and groupby(dropna=...) equivalents. Cross-reference Part 1 Q16 for aggregation basics.
**Asked at:** SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; SQLite lang_corefunc and lang_expr documentation (opened: trim character sets, ASCII-only lower/upper and LIKE, length versus octet_length, concat/concat_ws NULL rules, CAST rules, IS DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL table); official documentation, not candidate reports; analyst, data scientist and data engineer rounds

**Say this first (1 line):** Comparison operators say "unknown", set operators and `GROUP BY` say "same": NULLs are grouped, de-duplicated and intersected as one value, but a NULL never matches in `=`, `IN` or a join.

**Schema and sample data:**
```sql
CREATE TABLE contacts_a(email TEXT);
CREATE TABLE contacts_b(email TEXT);
INSERT INTO contacts_a VALUES ('a@x.com'),('a@x.com'),(NULL),(NULL),('b@x.com');
INSERT INTO contacts_b VALUES ('a@x.com'),(NULL),('c@x.com'),(NULL);
```

**SQL answer:** the `queries` dictionary in the Code block: `distinct`, `group_by`, `union`, `union_all`, `intersect`, `except`, `not_in`, `join_eq`, `join_isnd` (null-safe join with `IS`) and `in_subquery`, plus the `COUNT(*)`, `COUNT(email)`, `COUNT(DISTINCT email)` line. The `NOT IN` trap itself is Part 3 Q3; here it is only compared with `EXCEPT`.

**pandas answer:** `drop_duplicates()`, `concat(...).drop_duplicates()`, `isin` for intersect and except, `groupby(a, dropna=False).size()`, `nunique(dropna=False)` and an inner `merge` on the email column, all in the Code block as `p_res`.

**Example:** `contacts_a` = `a@x.com`, `a@x.com`, NULL, NULL, `b@x.com`. `contacts_b` = `a@x.com`, NULL, `c@x.com`, NULL. `SELECT DISTINCT` on A gives 3 rows: NULL, `a@x.com`, `b@x.com` (the two NULLs collapse). `COUNT(*)` is 5, `COUNT(email)` is 3 (NULLs skipped), `COUNT(DISTINCT email)` is 2. `UNION` gives NULL, `a`, `b`, `c` (4 rows). `INTERSECT` gives NULL and `a@x.com`: both sides have a NULL and the operator treats them as the same, although `NULL = NULL` is not true. `EXCEPT` gives only `b@x.com`: `a@x.com` is in B, and the NULL in A is removed because B has a NULL. The `NOT IN` version of the same question returned **no rows** because B contains a NULL, so `EXCEPT` and `NOT IN` disagree on this data. The `=` join returned 2 rows (just the two `a@x.com` rows of A), while the null-safe join (`IS`) returned 6: 2 x 2 NULL pairs plus 2.

**Code:** run with `python3 -I`.
```python
# Q25: NULL in DISTINCT, GROUP BY, UNION, INTERSECT, EXCEPT, COUNT(DISTINCT), joins and IN, with pandas equivalents.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE contacts_a(email TEXT);
CREATE TABLE contacts_b(email TEXT);
INSERT INTO contacts_a VALUES ('a@x.com'),('a@x.com'),(NULL),(NULL),('b@x.com');
INSERT INTO contacts_b VALUES ('a@x.com'),(NULL),('c@x.com'),(NULL);
""")
def run(q): return [r[0] for r in con.execute(q).fetchall()]
def one(q): return con.execute(q).fetchone()[0]

queries = {
 "distinct":     "SELECT DISTINCT email FROM contacts_a ORDER BY email",
 "group_by":     "SELECT email, COUNT(*) FROM contacts_a GROUP BY email ORDER BY email",
 "union":        "SELECT email FROM contacts_a UNION SELECT email FROM contacts_b ORDER BY 1",
 "union_all":    "SELECT email FROM contacts_a UNION ALL SELECT email FROM contacts_b ORDER BY 1",
 "intersect":    "SELECT email FROM contacts_a INTERSECT SELECT email FROM contacts_b ORDER BY 1",
 "except":       "SELECT email FROM contacts_a EXCEPT SELECT email FROM contacts_b ORDER BY 1",
 "not_in":       "SELECT DISTINCT email FROM contacts_a WHERE email NOT IN (SELECT email FROM contacts_b) ORDER BY 1",
 "join_eq":      "SELECT a.email FROM contacts_a a JOIN contacts_b b ON a.email = b.email ORDER BY 1",
 "join_isnd":    "SELECT a.email FROM contacts_a a JOIN contacts_b b ON a.email IS b.email ORDER BY 1",
 "in_subquery":  "SELECT email FROM contacts_a WHERE email IN (SELECT email FROM contacts_b) ORDER BY 1",
}
sql_res = {k: run(q) for k, q in queries.items()}
for k, v in sql_res.items(): print(f"{k:12}", v)
print("COUNT(*), COUNT(email), COUNT(DISTINCT email), DISTINCT rows:",
      con.execute("SELECT COUNT(*), COUNT(email), COUNT(DISTINCT email) FROM contacts_a").fetchone(), len(sql_res["distinct"]))
print("NULL = NULL:", one("SELECT NULL = NULL"), "| NULL IS NULL:", one("SELECT NULL IS NULL"),
      "| NULL IS DISTINCT FROM NULL:", one("SELECT NULL IS DISTINCT FROM NULL"))

# pandas (str dtype: missing is NaN)
a = pd.read_sql("SELECT email FROM contacts_a", con)["email"]
b = pd.read_sql("SELECT email FROM contacts_b", con)["email"]
def sort_nulls_first(s): return s.sort_values(na_position="first").tolist()
def lst(x): return [None if pd.isna(v) else v for v in x]
p_res = {
 "distinct":  lst(sort_nulls_first(a.drop_duplicates())),
 "union":     lst(sort_nulls_first(pd.concat([a, b]).drop_duplicates())),
 "union_all": lst(sort_nulls_first(pd.concat([a, b]))),
 "intersect": lst(sort_nulls_first(a.drop_duplicates()[a.drop_duplicates().isin(b)])),
 "except":    lst(sort_nulls_first(a.drop_duplicates()[~a.drop_duplicates().isin(b)])),
}
g = a.groupby(a, dropna=False).size()
p_res["group_by"] = sorted([(None if pd.isna(k) else k, int(v)) for k, v in g.items()], key=lambda t: (t[0] is not None, t[0] or ""))  # NULL group first, like SQLite
merged = a.to_frame().merge(b.to_frame(), on="email")                 # inner merge on the email key
p_res["join_eq"] = lst(sort_nulls_first(merged["email"]))
print("pandas merge on email returns", len(merged), "rows:", p_res["join_eq"], "(NaN keys matched each other)")
print("nunique default:", a.nunique(), "| nunique(dropna=False):", a.nunique(dropna=False),
      "| groupby groups: default", len(a.groupby(a).size()), "vs dropna=False", len(g))
print("isin NaN:", pd.Series([float("nan"), 1.0]).isin([float("nan")]).tolist(), "| ==:", (pd.Series([float("nan")]) == float("nan")).tolist())

sql_cmp = {k: ([(r[0], r[1]) for r in con.execute(queries[k]).fetchall()] if k == "group_by" else v) for k, v in sql_res.items()}
for k in p_res:
    if k == "join_eq": continue
    assert sql_cmp[k] == p_res[k], (k, sql_cmp[k], p_res[k])
assert one("SELECT COUNT(DISTINCT email) FROM contacts_a") == a.nunique() == 2
assert a.nunique(dropna=False) == len(sql_res["distinct"]) == 3
assert sql_res["join_eq"] == ["a@x.com", "a@x.com"] and p_res["join_eq"] != sql_res["join_eq"]   # pandas merge differs from SQL ON a.email = b.email
assert p_res["join_eq"] == sql_res["join_isnd"]                                                    # ...but matches the null-safe join (IS)
print("asserts passed (set operations and group counts equal; pandas merge equals the null-safe SQL join, not the = join; NULLs sorted first in both)")
```

**Output (my run):**
```text
distinct     [None, 'a@x.com', 'b@x.com']
group_by     [None, 'a@x.com', 'b@x.com']
union        [None, 'a@x.com', 'b@x.com', 'c@x.com']
union_all    [None, None, None, None, 'a@x.com', 'a@x.com', 'a@x.com', 'b@x.com', 'c@x.com']
intersect    [None, 'a@x.com']
except       ['b@x.com']
not_in       []
join_eq      ['a@x.com', 'a@x.com']
join_isnd    [None, None, None, None, 'a@x.com', 'a@x.com']
in_subquery  ['a@x.com', 'a@x.com']
COUNT(*), COUNT(email), COUNT(DISTINCT email), DISTINCT rows: (5, 3, 2) 3
NULL = NULL: None | NULL IS NULL: 1 | NULL IS DISTINCT FROM NULL: 0
pandas merge on email returns 6 rows: [None, None, None, None, 'a@x.com', 'a@x.com'] (NaN keys matched each other)
nunique default: 2 | nunique(dropna=False): 3 | groupby groups: default 2 vs dropna=False 3
isin NaN: [True, False] | ==: [False]
asserts passed (set operations and group counts equal; pandas merge equals the null-safe SQL join, not the = join; NULLs sorted first in both)
```

**Edge cases:**
- NULL sorts first in SQLite ascending order; pandas `groupby` puts the NaN group last, so sort before comparing (the Code block does).
- `COUNT(DISTINCT)` is 2 but `SELECT DISTINCT` returns 3 rows: the NULL row is a row, but not a value.
- `UNION ALL` keeps every NULL (4 of them here).
- Duplicates: `UNION`, `INTERSECT` and `EXCEPT` also de-duplicate; `UNION ALL` does not.
- Empty strings are not NULL: `''` is a value that groups separately.
- **pandas surprises (my run):** `merge` matched NaN with NaN (6 rows, equal to the null-safe SQL join, not to the `=` join); `isin` treats NaN as found (`[nan, 1.0].isin([nan])` gave `[True, False]`) while `==` does not (`False`); `nunique()` defaults to `dropna=True` (2) and `nunique(dropna=False)` gives 3; `groupby` drops the NaN group by default (2 groups against 3).

**Then explain:**
- **Interview line:** "comparison operators say unknown, set operators say same."
- **Why:** `=`, `IN` and joins need a TRUE, and `NULL = NULL` is UNKNOWN. `DISTINCT`, `GROUP BY`, `UNION`, `INTERSECT` and `EXCEPT` use "not distinct from" semantics, so two NULLs are the same.
- **Safer anti-join:** `EXCEPT` or `NOT EXISTS` do not break on NULLs the way `NOT IN` does. Which one you want depends on whether a NULL should count as "present in B".
- **Null-safe equality:** `IS` in SQLite (and `IS DISTINCT FROM`, which also ran on 3.45.1) is the SQL way to match NULLs; Part 1 Q41 covers it.
- **Other engines:** the standard behaviour is the same in the engines I know, but I did not run Postgres, MySQL, BigQuery or Snowflake here (not executed).
- **Cross-references:** Part 1 Q16 for aggregation basics, Part 3 Q3 for `NOT IN`.

**Follow-ups:**
- *Does `INTERSECT` need the columns to match positionally?* Yes, by position and compatible types, not by name.
- *How do you make a join match NULLs?* `ON a.email IS b.email` in SQLite (null-safe), or `COALESCE` to a sentinel (risky if the sentinel is real data).
- *Which count should a report use?* Decide whether NULL is a category; `COUNT(DISTINCT)` hides it.

**Common mistakes:**
- Saying "NULL = NULL is false" (it is unknown).
- Expecting `INTERSECT` to drop NULL rows because `=` does.
- Using `NOT IN` where `EXCEPT` or `NOT EXISTS` was meant.
- Merging in pandas on a key with NaN and expecting SQL join behaviour.
- Reading `COUNT(DISTINCT)` as the number of rows `DISTINCT` returns.

### Q26 ⭐⭐ 🟡 NULLs in constraints and tri-state flags: create tables with UNIQUE(email), CHECK(age >= 18), a non-INTEGER PRIMARY KEY and a nullable boolean flag is_active (1, 0, NULL). Show by running that UNIQUE allows several NULLs, CHECK passes when the expression is NULL (UNKNOWN is accepted), SQLite allows NULL in a non-INTEGER PRIMARY KEY column for legacy reasons unless NOT NULL is added (and other engines do not), and that WHERE is_active = 0 misses NULL rows while WHERE is_active IS NOT TRUE (SQLite 3.23 and later) catches them. Show IS TRUE, IS NOT TRUE, IS FALSE, NOT NULL = NULL and the count of active, inactive and unknown users that sums to the total. State that PostgreSQL 15 added UNIQUE NULLS NOT DISTINCT and SQL Server treats a unique index as allowing one NULL (hedged, not executed). Add the pandas nullable boolean dtype version.
**Asked at:** SQLite lang_corefunc and lang_expr documentation (opened: trim character sets, ASCII-only lower/upper and LIKE, length versus octet_length, concat/concat_ws NULL rules, CAST rules, IS DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL table); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds

**Say this first (1 line):** A NULL passes UNIQUE (many NULLs are allowed) and passes CHECK (UNKNOWN counts as pass), SQLite lets a non-INTEGER PRIMARY KEY hold NULL unless you add NOT NULL, and a nullable flag has three states, so `WHERE is_active = 0` misses the unknown rows and `IS NOT TRUE` catches them.

**Schema and sample data:**
```sql
CREATE TABLE u_unique(email TEXT UNIQUE);
CREATE TABLE u_check(age INTEGER CHECK(age >= 18));
CREATE TABLE u_pk(code TEXT PRIMARY KEY, n INTEGER);            -- not INTEGER PRIMARY KEY
CREATE TABLE u_pk_nn(code TEXT PRIMARY KEY NOT NULL, n INTEGER);
CREATE TABLE u_pk_wr(code TEXT PRIMARY KEY, n INTEGER) WITHOUT ROWID;
CREATE TABLE u_pk_int(id INTEGER PRIMARY KEY, n INTEGER);
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_active INTEGER);          -- 1, 0 or NULL
INSERT INTO users VALUES (1,1),(2,1),(3,0),(4,NULL),(5,NULL);
```

**SQL answer:** the `attempt` lines in the Code block (each INSERT runs and prints ok or the error), then `sql_probe` (all the flag tests side by side), `sql_counts` (active, inactive, unknown, total) and the three `WHERE` variants.

**pandas answer:** `u["is_active"].astype("boolean")` gives the nullable boolean dtype (`True`, `False`, `<NA>`). Counts use `(flag == True).sum()`, `(flag == False).sum()` and `flag.isna().sum()`; `IS NOT TRUE` is `(flag != True).fillna(True)`. All in the Code block.

**Example:** Users 1 to 5 have flags 1, 1, 0, NULL, NULL. `is_active = 0` returns user 3 only. `is_active <> 1` also returns only user 3 (NULL <> 1 is unknown). `NOT is_active` is NULL for users 4 and 5, so it misses them too. `is_active IS NOT TRUE` returns users 3, 4 and 5. Counts: `IS TRUE` 2, `IS FALSE` 1, `IS NULL` 2, which sum to the 5 users. For constraints: the second `INSERT NULL` into the UNIQUE column succeeded (two NULL rows), `age = 17` failed with `CHECK constraint failed: age >= 18`, `age = NULL` and `18` passed, two NULL codes went into the `TEXT PRIMARY KEY` table, the `NOT NULL` version and the `WITHOUT ROWID` version rejected NULL, and a NULL into `INTEGER PRIMARY KEY` got the id 1.

**Code:** run with `python3 -I`.
```python
# Q26: NULLs in UNIQUE, CHECK, non-INTEGER PRIMARY KEY and tri-state flags; pandas nullable boolean.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE u_unique(email TEXT UNIQUE);
CREATE TABLE u_check(age INTEGER CHECK(age >= 18));
CREATE TABLE u_pk(code TEXT PRIMARY KEY, n INTEGER);
CREATE TABLE u_pk_nn(code TEXT PRIMARY KEY NOT NULL, n INTEGER);
CREATE TABLE u_pk_wr(code TEXT PRIMARY KEY, n INTEGER) WITHOUT ROWID;
CREATE TABLE u_pk_int(id INTEGER PRIMARY KEY, n INTEGER);
""")
def attempt(label, sql):
    try:
        con.execute(sql); print(f"  ok   : {label}")
    except sqlite3.Error as e:
        print(f"  FAIL : {label} -> {e}")
attempt("UNIQUE email, first NULL", "INSERT INTO u_unique VALUES (NULL)")
attempt("UNIQUE email, second NULL", "INSERT INTO u_unique VALUES (NULL)")
attempt("UNIQUE email, 'a' twice (second)", "INSERT INTO u_unique VALUES ('a')"); attempt("   ... duplicate 'a'", "INSERT INTO u_unique VALUES ('a')")
attempt("CHECK age=17", "INSERT INTO u_check VALUES (17)")
attempt("CHECK age=NULL", "INSERT INTO u_check VALUES (NULL)")
attempt("CHECK age=18", "INSERT INTO u_check VALUES (18)")
attempt("TEXT PRIMARY KEY NULL (1)", "INSERT INTO u_pk VALUES (NULL, 1)")
attempt("TEXT PRIMARY KEY NULL (2)", "INSERT INTO u_pk VALUES (NULL, 2)")
attempt("TEXT PRIMARY KEY NOT NULL, NULL", "INSERT INTO u_pk_nn VALUES (NULL, 1)")
attempt("WITHOUT ROWID PK, NULL", "INSERT INTO u_pk_wr VALUES (NULL, 1)")
attempt("INTEGER PRIMARY KEY, NULL", "INSERT INTO u_pk_int VALUES (NULL, 1)")
print("INTEGER PRIMARY KEY got id:", con.execute("SELECT id FROM u_pk_int").fetchone()[0],
      "| NULL rows in u_unique:", con.execute("SELECT COUNT(*) FROM u_unique WHERE email IS NULL").fetchone()[0],
      "| NULL rows in u_pk:", con.execute("SELECT COUNT(*) FROM u_pk WHERE code IS NULL").fetchone()[0])

# allow at most one NULL: a partial unique index on a constant for the NULL rows
con.executescript("CREATE TABLE u_one(email TEXT); CREATE UNIQUE INDEX u_one_null ON u_one((email IS NULL)) WHERE email IS NULL;")
attempt("u_one NULL (1)", "INSERT INTO u_one VALUES (NULL)")
attempt("u_one NULL (2)", "INSERT INTO u_one VALUES (NULL)")
attempt("u_one 'a' then 'a' again", "INSERT INTO u_one VALUES ('a'),('a')")

con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_active INTEGER);          -- 1, 0 or NULL
INSERT INTO users VALUES (1,1),(2,1),(3,0),(4,NULL),(5,NULL);
""")
sql_probe = """
SELECT user_id, is_active,
       is_active = 0        AS eq0,
       NOT is_active        AS not_flag,
       is_active IS TRUE    AS is_true,
       is_active IS FALSE   AS is_false,
       is_active IS NOT TRUE AS is_not_true,
       is_active IS NULL    AS is_null
FROM users ORDER BY user_id"""
print(pd.read_sql(sql_probe, con).to_string(index=False))
sql_counts = """
SELECT SUM(is_active IS TRUE) AS active, SUM(is_active IS FALSE) AS inactive, SUM(is_active IS NULL) AS unknown, COUNT(*) AS total
FROM users"""
sql_row = con.execute(sql_counts).fetchone()
print("counts (active, inactive, unknown, total):", sql_row)
print("WHERE is_active = 0 :", [r[0] for r in con.execute("SELECT user_id FROM users WHERE is_active = 0")])
print("WHERE is_active <> 1:", [r[0] for r in con.execute("SELECT user_id FROM users WHERE is_active <> 1")])
print("WHERE is_active IS NOT TRUE:", [r[0] for r in con.execute("SELECT user_id FROM users WHERE is_active IS NOT TRUE ORDER BY user_id")])
print("NULL IS TRUE / NULL IS NOT TRUE / NOT NULL:", con.execute("SELECT NULL IS TRUE, NULL IS NOT TRUE, NOT NULL").fetchone())

# pandas
u = pd.read_sql("SELECT * FROM users ORDER BY user_id", con)
print("read_sql dtype of is_active:", u["is_active"].dtype, "(NULL made it float64 with NaN)")
print("float: == 0 ->", u.index[u["is_active"] == 0].tolist(), "| != 1 ->", u.index[u["is_active"] != 1].tolist(), "(NaN != 1 is True in pandas, unlike SQL)")
flag = u["is_active"].astype("boolean")                      # nullable boolean: True, False, <NA>
print("boolean dtype:", flag.tolist())
print("== False ->", (flag == False).tolist(), "| ~flag ->", (~flag).tolist())     # noqa: E712
try:
    bool(flag.iloc[3])
except TypeError as e:
    print("bool(pd.NA):", e)
print("df[flag == False] rows:", u[flag == False]["user_id"].tolist(), "(NA in a mask counts as False)")   # noqa: E712
p_counts = (int((flag == True).sum()), int((flag == False).sum()), int(flag.isna().sum()), len(flag))     # noqa: E712
is_not_true = (flag != True).fillna(True)                    # NA != True is NA: fill to mimic IS NOT TRUE   # noqa: E712
print("pandas counts:", p_counts, "| IS NOT TRUE ids:", u.loc[is_not_true, "user_id"].tolist())
assert tuple(sql_row) == p_counts == (2, 1, 2, 5) and sum(p_counts[:3]) == p_counts[3]
assert u.loc[is_not_true, "user_id"].tolist() == [r[0] for r in con.execute("SELECT user_id FROM users WHERE is_active IS NOT TRUE ORDER BY user_id")] == [3, 4, 5]
print("asserts passed (SQL counts and IS NOT TRUE rows == pandas, ordered by user_id)")
```

**Output (my run):**
```text
  ok   : UNIQUE email, first NULL
  ok   : UNIQUE email, second NULL
  ok   : UNIQUE email, 'a' twice (second)
  FAIL :    ... duplicate 'a' -> UNIQUE constraint failed: u_unique.email
  FAIL : CHECK age=17 -> CHECK constraint failed: age >= 18
  ok   : CHECK age=NULL
  ok   : CHECK age=18
  ok   : TEXT PRIMARY KEY NULL (1)
  ok   : TEXT PRIMARY KEY NULL (2)
  FAIL : TEXT PRIMARY KEY NOT NULL, NULL -> NOT NULL constraint failed: u_pk_nn.code
  FAIL : WITHOUT ROWID PK, NULL -> NOT NULL constraint failed: u_pk_wr.code
  ok   : INTEGER PRIMARY KEY, NULL
INTEGER PRIMARY KEY got id: 1 | NULL rows in u_unique: 2 | NULL rows in u_pk: 2
  ok   : u_one NULL (1)
  FAIL : u_one NULL (2) -> UNIQUE constraint failed: index 'u_one_null'
  ok   : u_one 'a' then 'a' again
 user_id  is_active  eq0  not_flag  is_true  is_false  is_not_true  is_null
       1        1.0  0.0       0.0        1         0            0        0
       2        1.0  0.0       0.0        1         0            0        0
       3        0.0  1.0       1.0        0         1            1        0
       4        NaN  NaN       NaN        0         0            1        1
       5        NaN  NaN       NaN        0         0            1        1
counts (active, inactive, unknown, total): (2, 1, 2, 5)
WHERE is_active = 0 : [3]
WHERE is_active <> 1: [3]
WHERE is_active IS NOT TRUE: [3, 4, 5]
NULL IS TRUE / NULL IS NOT TRUE / NOT NULL: (0, 1, None)
read_sql dtype of is_active: float64 (NULL made it float64 with NaN)
float: == 0 -> [2] | != 1 -> [2, 3, 4] (NaN != 1 is True in pandas, unlike SQL)
boolean dtype: [True, True, False, <NA>, <NA>]
== False -> [False, False, True, <NA>, <NA>] | ~flag -> [False, False, True, <NA>, <NA>]
bool(pd.NA): boolean value of NA is ambiguous
df[flag == False] rows: [3] (NA in a mask counts as False)
pandas counts: (2, 1, 2, 5) | IS NOT TRUE ids: [3, 4, 5]
asserts passed (SQL counts and IS NOT TRUE rows == pandas, ordered by user_id)
```

**Edge cases:**
- `NULL IS TRUE` is 0, `NULL IS NOT TRUE` is 1, `NOT NULL` is NULL (my run: `(0, 1, None)`).
- Values other than 0 and 1 (for example 2) can be stored (not run here); only a CHECK on the flag would stop them, so add `CHECK (is_active IN (0, 1))`: a NULL still passes that CHECK too.
- A foreign key with a NULL column is not checked, for the same UNKNOWN reason (not run here).
- **pandas:** `read_sql` returned the flag as `float64` with NaN (ints plus NULL), where `!= 1` is True for NaN (pandas differs from SQL, which gives unknown) and `== 0` matches only the real zero. With the nullable boolean dtype, `== False` gives `<NA>` for the unknown rows, `bool(pd.NA)` raises `TypeError` (`boolean value of NA is ambiguous`), and using the NA mask to filter rows (`u[flag == False]`) treats NA as False, so it returns user 3 only.

**Then explain:**
- **Why UNIQUE allows many NULLs:** two NULLs are not "equal", so they do not violate uniqueness. The standard-style rule is the same in the engines I know, but I did not run them here (not executed).
- **Why CHECK passes NULL:** a CHECK fails only when the expression is FALSE; UNKNOWN is accepted. To forbid NULL add `NOT NULL`.
- **Non-INTEGER PRIMARY KEY:** SQLite lets NULL in for historical reasons (the run shows two NULL codes); `NOT NULL` or `WITHOUT ROWID` stops it. Most other engines reject NULL in a primary key; I did not execute any.
- **Tri-state flags:** pick one of: make the column `NOT NULL DEFAULT 0`, or keep NULL as "unknown" and always write `IS TRUE`, `IS FALSE`, `IS NOT TRUE`. Never write `<> 1` or `NOT flag` unless you want to lose NULLs.
- **Other engines (not executed):** PostgreSQL 15 added `UNIQUE NULLS NOT DISTINCT` so that NULLs count as equal, and I recall that SQL Server treats a unique constraint as allowing only one NULL; check the documentation of your version before relying on either.
- **pandas:** use the nullable `boolean` dtype so that NA stays NA instead of turning into False or NaN.

**Follow-ups:**
- *How do you allow only one NULL in SQLite?* A partial unique index: `CREATE UNIQUE INDEX u_one_null ON u_one((email IS NULL)) WHERE email IS NULL` (in the Code block: the second NULL failed with `UNIQUE constraint failed: index 'u_one_null'`, while repeated `'a'` values were still allowed).
- *What does `COUNT(*)` give per state?* `GROUP BY is_active` returns three groups: 1, 0 and NULL.
- *Should the flag be nullable at all?* Only if "unknown" is a real business state.

**Common mistakes:**
- `WHERE is_active != 1` to mean "not active".
- Believing CHECK(age >= 18) rejects NULL ages.
- Using a non-INTEGER PRIMARY KEY without NOT NULL in SQLite.
- Counting active and inactive and forgetting the unknown group (the three do not add up to the total).
- Casting a pandas NaN flag to `bool` (NaN becomes True).

### Q27 ⭐⭐ 🟡 Crosstab percentages: sales(region, product, amount). Return a region by product table of each cell's share of its row total (row percent), of its column total (column percent) and of the grand total, with ROUND to 1 decimal, using SUM(CASE ...) divided by a row total, a scalar subquery for the grand total and window SUM() OVER for the column total. Check each row of row percentages sums to 100 (explain why it can show 99.9 or 100.1 after rounding) and what happens when a total is zero (divide by NULLIF). Add the pandas pd.crosstab(..., values=..., aggfunc='sum', normalize='index' / 'columns' / True) version and assert it equals the SQL result.
**Asked at:** SQL pivot guides (datadriven.io, DataVidhya, Educative and a Medium write-up, search snippets only; the DataVidhya lesson page opened but showed only its introduction: CASE inside SUM or COUNT, dynamic pivot, NULL categories); guides, not candidate reports; analyst and data engineer rounds at product companies and GCCs; pandas user guide pages on reshaping and on working with text data (opened: pivot, pivot_table, melt, wide_to_long, stack, unstack, crosstab, explode, string dtype and the .str accessor); official documentation, not candidate reports; data scientist and analyst rounds

**Say this first (1 line):** Compute each cell once, then divide by a row, column or grand total taken with a window function or a scalar subquery, wrap the divisor in `NULLIF(..., 0)`, and expect rounded percentages to sum to 99.9 or 100.1.

**Schema and sample data:**
```sql
CREATE TABLE sales(region TEXT, product TEXT, amount REAL);
INSERT INTO sales VALUES
 ('East','A',4),('East','A',6),('East','B',10),('East','C',10),      -- East: 10 / 10 / 10
 ('South','A',10),('South','B',10),('South','C',40),                 -- South: 10 / 10 / 40
 ('West','A',10),('West','C',30),                                    -- West has no B row
 ('North','A',0),('North','B',0),('North','C',0);                    -- North totals zero
```

**SQL answer:** `pivot_sql(measure)` in the Code block builds the same query three times with `row_pct`, `col_pct` or `grand_pct`. The CTE `cell` sums the sales per region and product, `m` adds `SUM(amt) OVER (PARTITION BY region)`, `SUM(amt) OVER (PARTITION BY product)` and a scalar subquery for the grand total, and the outer query pivots one measure with `ROUND(SUM(CASE WHEN product = 'A' THEN ... END), 1)`.

**pandas answer:** `pd.crosstab(index=..., columns=..., values=..., aggfunc="sum", normalize="index")` (and `"columns"`, and `True`), times 100, rounded to 1. Because `crosstab` fills empty cells with 0.0, the Code block also builds the NULL-faithful version with `pivot_table` and explicit division, and asserts both.

**Example:** Rows: East 10, 10, 10 (total 30); South 10, 10, 40 (total 60); West A 10 and C 30 only (total 40); North 0, 0, 0 (total 0). Grand total 130. East row percent: 10/30 = 33.3 each, so the row shows 33.3 + 33.3 + 33.3 = **99.9**. South: 16.7 + 16.7 + 66.7 = **100.1**. West: 25.0, NULL, 75.0 (no B sales, so no cell). North: the row total is 0, `NULLIF` turns the divisor into NULL, so the whole row is NULL. Column totals: A 30, B 20, C 80, so East A is 10/30 = 33.3 and East C is 10/80 = 12.5. Grand percent: East A is 10/130 = 7.7, South C is 40/130 = 30.8.

**Code:** run with `python3 -I`.
```python
# Q27: crosstab percentages (row, column, grand) in SQLite versus pandas.crosstab(normalize=...).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(region TEXT, product TEXT, amount REAL);
INSERT INTO sales VALUES
 ('East','A',4),('East','A',6),('East','B',10),('East','C',10),      -- East: 10 / 10 / 10
 ('South','A',10),('South','B',10),('South','C',40),                 -- South: 10 / 10 / 40
 ('West','A',10),('West','C',30),                                    -- West has no B row
 ('North','A',0),('North','B',0),('North','C',0);                    -- North totals zero
""")

# one long CTE gives every cell its row total, column total and grand total; the outer query pivots one measure
def pivot_sql(measure):
    cols = ",\n       ".join(
        f"ROUND(SUM(CASE WHEN product = '{p}' THEN {measure} END), 1) AS {p.lower()}" for p in "ABC")
    return f"""
WITH cell AS (SELECT region, product, SUM(amount) AS amt FROM sales GROUP BY region, product),
m AS (
  SELECT region, product, amt,
         100.0 * amt / NULLIF(SUM(amt) OVER (PARTITION BY region), 0)  AS row_pct,
         100.0 * amt / NULLIF(SUM(amt) OVER (PARTITION BY product), 0) AS col_pct,
         100.0 * amt / NULLIF((SELECT SUM(amount) FROM sales), 0)     AS grand_pct
  FROM cell)
SELECT region,
       {cols}
FROM m GROUP BY region ORDER BY region"""

sql = {k: pivot_sql(k) for k in ("row_pct", "col_pct", "grand_pct")}
sql_df = {k: pd.read_sql(q, con).set_index("region") for k, q in sql.items()}
for k, v in sql_df.items():
    print(k); print(v.to_string())
print("row_pct row sums:", sql_df["row_pct"].sum(axis=1).round(2).to_dict())
print("col_pct col sums:", sql_df["col_pct"].sum(axis=0).round(2).to_dict(), "| grand_pct total:", round(float(sql_df["grand_pct"].sum().sum()), 2))
print("without NULLIF, North row_pct in SQLite:", con.execute("SELECT 100.0 * 0 / 0").fetchone()[0], "(division by zero gives NULL in SQLite)")
print("unrounded East row shares:", [round(100 * x / 30, 4) for x in (10, 10, 10)], "-> 33.3 * 3 =", round(33.3 * 3, 1))

# pandas
s = pd.read_sql("SELECT * FROM sales", con)
args = dict(index=s["region"], columns=s["product"], values=s["amount"], aggfunc="sum")
p_df = {
    "row_pct": (pd.crosstab(**args, normalize="index") * 100).round(1),
    "col_pct": (pd.crosstab(**args, normalize="columns") * 100).round(1),
    "grand_pct": (pd.crosstab(**args, normalize=True) * 100).round(1),
}
for k, v in p_df.items():
    v.columns.name = None; v.index.name = "region"
    print("pandas", k); print(v.to_string())

# crosstab fills empty cells and 0/0 with 0.0, SQL keeps NULL: so crosstab equals the SQL result after fillna(0)
# the SQL-faithful pandas version (NaN stays NaN, zero total -> NaN like NULLIF) uses pivot_table and explicit division
nan = float("nan")
tbl = s.pivot_table(index="region", columns="product", values="amount", aggfunc="sum")
faithful = {
    "row_pct": tbl.div(tbl.sum(axis=1).replace(0, nan), axis=0) * 100,
    "col_pct": tbl.div(tbl.sum(axis=0).replace(0, nan), axis=1) * 100,
    "grand_pct": tbl / tbl.sum().sum() * 100,
}
def rows(df):
    return [tuple(None if pd.isna(x) else round(float(x), 1) for x in row) for row in df.itertuples(index=False)]
for k in sql_df:
    assert list(sql_df[k].index) == list(p_df[k].index) == list(faithful[k].index)
    assert rows(sql_df[k].fillna(0)) == rows(p_df[k]), ("crosstab", k)       # crosstab == SQL with NULL shown as 0
    assert rows(sql_df[k]) == rows(faithful[k].round(1)), ("pivot_table", k)  # pivot_table + division == SQL exactly
print("faithful row_pct (NaN kept):"); print(faithful["row_pct"].round(1).to_string())
print("asserts passed (rows sorted by region): crosstab == SQL with NULL->0; pivot_table division == SQL with NULL kept")
```

**Output (my run):**
```text
row_pct
           a     b     c
region                  
East    33.3  33.3  33.3
North    NaN   NaN   NaN
South   16.7  16.7  66.7
West    25.0   NaN  75.0
col_pct
           a     b     c
region                  
East    33.3  50.0  12.5
North    0.0   0.0   0.0
South   33.3  50.0  50.0
West    33.3   NaN  37.5
grand_pct
          a    b     c
region                
East    7.7  7.7   7.7
North   0.0  0.0   0.0
South   7.7  7.7  30.8
West    7.7  NaN  23.1
row_pct row sums: {'East': 99.9, 'North': 0.0, 'South': 100.1, 'West': 100.0}
col_pct col sums: {'a': 99.9, 'b': 100.0, 'c': 100.0} | grand_pct total: 100.1
without NULLIF, North row_pct in SQLite: None (division by zero gives NULL in SQLite)
unrounded East row shares: [33.3333, 33.3333, 33.3333] -> 33.3 * 3 = 99.9
pandas row_pct
           A     B     C
region                  
East    33.3  33.3  33.3
North    0.0   0.0   0.0
South   16.7  16.7  66.7
West    25.0   0.0  75.0
pandas col_pct
           A     B     C
region                  
East    33.3  50.0  12.5
North    0.0   0.0   0.0
South   33.3  50.0  50.0
West    33.3   0.0  37.5
pandas grand_pct
          A    B     C
region                
East    7.7  7.7   7.7
North   0.0  0.0   0.0
South   7.7  7.7  30.8
West    7.7  0.0  23.1
faithful row_pct (NaN kept):
product     A     B     C
region                   
East     33.3  33.3  33.3
North     NaN   NaN   NaN
South    16.7  16.7  66.7
West     25.0   NaN  75.0
asserts passed (rows sorted by region): crosstab == SQL with NULL->0; pivot_table division == SQL with NULL kept
```

**Edge cases:**
- **Rounding:** the rounded parts need not sum to 100. The unrounded East shares are 33.3333 each, and 3 x 33.3 = 99.9; South's 16.67 and 66.67 round up and give 100.1. Show one more decimal, or put the rounding error in the largest cell, if the report must add to 100.
- **Zero total:** without `NULLIF`, `100.0 * 0 / 0` gives NULL in SQLite (it does not raise an error; my run), but PostgreSQL raises a division by zero error (not executed here, from memory). `NULLIF` makes the intent explicit in every engine.
- **Missing cell (West, B):** SQL gives NULL. `crosstab` gives 0.0 in all three tables, and gives 0.0 for the North row percent (0/0), where SQL gives NULL. The asserts in the Code block show `crosstab` equals the SQL result after `fillna(0)`, and the `pivot_table` division equals the SQL result exactly.
- **Column percent for North** is 0.0 (not NULL) in SQL because the column totals are not zero.
- Ties and duplicates: duplicate rows per cell are summed first (`cell`).

**Then explain:**
- **Three denominators:** row = total over the region, column = total over the product, grand = total over everything. A window `SUM() OVER (PARTITION BY ...)` gives the first two without a second query; a scalar subquery gives the grand total.
- **Order of operations:** aggregate to cell level first, then divide. Dividing raw rows by a total gives the same totals but is easy to get wrong with duplicates.
- **Why `100.0`:** it forces floating-point division; `100 * 4 / 10` with integers can truncate.
- **pandas:** `normalize` has three options: `"index"` (rows), `"columns"`, `True` (all). Check what happens to empty cells before comparing with SQL.
- Cross-reference: Part 1 Q10 for plain conditional aggregation.

**Follow-ups:**
- *How would you show counts and percentages together?* Two measures per cell in the long CTE, then pivot both.
- *Why use a window and not a self-join?* One scan, no join, same result.
- *How do you force the percentages to add to 100?* Largest remainder method: round down, then distribute the leftover units to the biggest remainders.

**Common mistakes:**
- Dividing by `SUM(amount)` without `NULLIF`.
- Using integer division.
- Calculating a column percent with the row total.
- Rounding before summing the percentages and then reporting the sum as an error.
- Assuming pandas `crosstab` returns NaN for empty cells (it returned 0.0 here).

### Q28 ⭐⭐ 🟡 pandas reshaping beyond pivot: scores wide table (student, math_2023, math_2024, sci_2023, sci_2024) and a long table (student, subject, year, score). Use melt (id_vars, var_name, value_name, ignore_index), wide_to_long (stub names, sep and suffix regex), stack and unstack (the pandas 3 future_stack behaviour: run and report whether NaN rows are kept), and set_index plus unstack for long to wide, with fill_value. Show that unstack sorts the index, that melt keeps NaN rows (dropna needed), and compare with the SQL UNION ALL unpivot and the SUM(CASE) pivot on the same data (assert same rows and state the order).
**Asked at:** pandas user guide pages on reshaping and on working with text data (opened: pivot, pivot_table, melt, wide_to_long, stack, unstack, crosstab, explode, string dtype and the .str accessor); official documentation, not candidate reports; data scientist and analyst rounds; SQL pivot guides (datadriven.io, DataVidhya, Educative and a Medium write-up, search snippets only; the DataVidhya lesson page opened but showed only its introduction: CASE inside SUM or COUNT, dynamic pivot, NULL categories); guides, not candidate reports; analyst and data engineer rounds at product companies and GCCs

**Say this first (1 line):** `melt` is the pandas `UNION ALL` unpivot (it keeps NaN rows), `wide_to_long` is for column names like `math_2023`, `stack`/`unstack` work on the index, and pandas 3 keeps NaN rows in `stack` where the old implementation dropped them.

**Schema and sample data:**
```sql
CREATE TABLE scores_wide(student TEXT, math_2023 INTEGER, math_2024 INTEGER, sci_2023 INTEGER, sci_2024 INTEGER);
INSERT INTO scores_wide VALUES ('Zed',90,92,80,NULL),('Ana',70,NULL,65,66),('Mia',NULL,NULL,NULL,NULL);
-- the long table scores_long (student, subject, year, score) is built from it by the UNION ALL query below
```

**SQL answer:** `sql_unpivot` (4-branch `UNION ALL`, one row per student, subject and year, NULL scores kept), `sql_w2l` (2 branches, one column per subject, the shape `wide_to_long` returns) and `sql_pivot` (`SUM(CASE WHEN subject = ... AND year = ... THEN score END)`) are in the Code block.

**pandas answer:** `wide.melt(id_vars="student", var_name="col", value_name="score")` then a split of `col` into subject and year; `pd.wide_to_long(wide, stubnames=["math", "sci"], i="student", j="year", sep="_", suffix=r"\d+")`; `long.set_index([...])["score"].unstack(["subject", "year"])` (with `fill_value`); and `stack` on a larger frame. All in the Code block.

**Example:** Three students: Zed 90, 92, 80, NULL; Ana 70, NULL, 65, 66; Mia all NULL. The wide table has 3 rows and 4 score columns, so the unpivot has 12 rows, and 6 of them have a NULL score (Zed 1, Ana 1, Mia 4). `melt` returned the same 12 rows, and 6 remain after `dropna`. `wide_to_long` returns 6 rows (student, year) with columns `math` and `sci`. Going back with `unstack` returns 3 rows sorted `Ana, Mia, Zed` although the input order was Zed, Ana, Mia, and the SQL `SUM(CASE)` pivot returns the same numbers, with NULL where all inputs are NULL.

**Code:** run with `python3 -I`.
```python
# Q28: pandas reshaping (melt, wide_to_long, stack/unstack) compared with SQL UNION ALL unpivot and SUM(CASE) pivot.
import sqlite3
import warnings
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE scores_wide(student TEXT, math_2023 INTEGER, math_2024 INTEGER, sci_2023 INTEGER, sci_2024 INTEGER);
INSERT INTO scores_wide VALUES ('Zed',90,92,80,NULL),('Ana',70,NULL,65,66),('Mia',NULL,NULL,NULL,NULL);
""")

# SQL: unpivot with UNION ALL (keeps NULL scores, like melt)
sql_unpivot = """
SELECT student, 'math' AS subject, 2023 AS year, math_2023 AS score FROM scores_wide
UNION ALL SELECT student, 'math', 2024, math_2024 FROM scores_wide
UNION ALL SELECT student, 'sci',  2023, sci_2023  FROM scores_wide
UNION ALL SELECT student, 'sci',  2024, sci_2024  FROM scores_wide
ORDER BY student, subject, year"""
con.execute("CREATE TABLE scores_long AS " + sql_unpivot.replace("ORDER BY student, subject, year", ""))
u_sql = pd.read_sql(sql_unpivot, con)

# SQL: wide-to-long with one column per subject (what wide_to_long returns)
sql_w2l = """
SELECT student, 2023 AS year, math_2023 AS math, sci_2023 AS sci FROM scores_wide
UNION ALL SELECT student, 2024, math_2024, sci_2024 FROM scores_wide ORDER BY student, year"""
w2l_sql = pd.read_sql(sql_w2l, con)

# SQL: long-to-wide with SUM(CASE ...)
sql_pivot = """
SELECT student,
       SUM(CASE WHEN subject = 'math' AND year = 2023 THEN score END) AS math_2023,
       SUM(CASE WHEN subject = 'math' AND year = 2024 THEN score END) AS math_2024,
       SUM(CASE WHEN subject = 'sci'  AND year = 2023 THEN score END) AS sci_2023,
       SUM(CASE WHEN subject = 'sci'  AND year = 2024 THEN score END) AS sci_2024
FROM scores_long GROUP BY student ORDER BY student"""
piv_sql = pd.read_sql(sql_pivot, con)
print("SQL unpivot rows:", len(u_sql), "| NULL scores kept:", int(u_sql["score"].isna().sum()))

# pandas
wide = pd.read_sql("SELECT * FROM scores_wide", con)
long = wide.melt(id_vars="student", var_name="col", value_name="score")          # melt keeps NaN rows
long[["subject", "year"]] = long["col"].str.split("_", expand=True)
long["year"] = long["year"].astype(int)
long = long[["student", "subject", "year", "score"]].sort_values(["student", "subject", "year"]).reset_index(drop=True)
print("melt rows:", len(long), "| after dropna:", len(long.dropna(subset=["score"])))

w2l = (pd.wide_to_long(wide, stubnames=["math", "sci"], i="student", j="year", sep="_", suffix=r"\d+")
         .reset_index().sort_values(["student", "year"]).reset_index(drop=True))

back = long.set_index(["student", "subject", "year"])["score"].unstack(["subject", "year"]).sort_index(axis=1)
back.columns = [f"{s}_{y}" for s, y in back.columns]
print("unstack index order:", back.index.tolist(), "(sorted; input order was Zed, Ana, Mia)")
idx = long.set_index(["student", "subject", "year"])["score"]
print("unstack(fill_value=0), NaN stored in the rows (Mia):", idx.unstack(["subject", "year"], fill_value=0).loc["Mia"].tolist(), "(explicit NaN is not 'missing', so it stays)")
gap = idx.dropna().unstack(["subject", "year"], fill_value=0)
print("unstack(fill_value=0) after dropna: Mia is gone,", "Mia" in gap.index, "| Ana's missing cell becomes 0:"); print(gap.to_string())
print("column order here is order of first appearance, not sorted: add .sort_index(axis=1) ->", gap.sort_index(axis=1).columns.tolist())
back = back.reset_index()

# stack with the pandas 3 behaviour, on a larger frame (1000 rows x 6 columns, 143 NaN)
big = pd.DataFrame(np.arange(6000, dtype=float).reshape(1000, 6), columns=list("abcdef"))
big.iloc[::7, 2] = np.nan
print("NaN cells:", int(big.isna().sum().sum()))
print("stack() default      :", big.stack().shape, "(NaN kept)")
print("stack(future_stack=True):", big.stack(future_stack=True).shape)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    old = big.stack(future_stack=False)
    print("stack(future_stack=False):", old.shape, "(old behaviour drops NaN) | warning:", [x.category.__name__ for x in w])
try:
    big.stack(dropna=True)
except Exception as e:
    print("stack(dropna=True):", type(e).__name__, "-", str(e)[:60])
print("stack(...).dropna() shape:", big.stack().dropna().shape)

def norm(df): return [tuple(None if pd.isna(v) else (int(v) if isinstance(v, float) else v) for v in row) for row in df.itertuples(index=False)]
assert norm(u_sql) == norm(long)                          # ordered by student, subject, year; 12 rows incl. NaN
assert norm(w2l_sql) == norm(w2l[["student", "year", "math", "sci"]])
assert norm(piv_sql) == norm(back)                        # ordered by student
assert big.stack(future_stack=True).shape == big.stack().shape == (6000,) and old.shape == (5857,)
print("asserts passed (UNION ALL == melt, wide_to_long == 2-branch UNION ALL, SUM(CASE) == unstack; all ordered by student[, subject, year])")
con.close()
```

**Output (my run):**
```text
SQL unpivot rows: 12 | NULL scores kept: 6
melt rows: 12 | after dropna: 6
unstack index order: ['Ana', 'Mia', 'Zed'] (sorted; input order was Zed, Ana, Mia)
unstack(fill_value=0), NaN stored in the rows (Mia): [nan, nan, nan, nan] (explicit NaN is not 'missing', so it stays)
unstack(fill_value=0) after dropna: Mia is gone, False | Ana's missing cell becomes 0:
subject  math   sci        math
year     2023  2023  2024  2024
student                        
Ana      70.0  65.0  66.0   0.0
Zed      90.0  80.0   0.0  92.0
column order here is order of first appearance, not sorted: add .sort_index(axis=1) -> [('math', 2023), ('math', 2024), ('sci', 2023), ('sci', 2024)]
NaN cells: 143
stack() default      : (6000,) (NaN kept)
stack(future_stack=True): (6000,)
stack(future_stack=False): (5857,) (old behaviour drops NaN) | warning: ['Pandas4Warning']
stack(dropna=True): ValueError - dropna must be unspecified as the new implementation does no
stack(...).dropna() shape: (5857,)
asserts passed (UNION ALL == melt, wide_to_long == 2-branch UNION ALL, SUM(CASE) == unstack; all ordered by student[, subject, year])
```

**Edge cases:**
- **`melt` keeps NaN rows;** use `dropna(subset=["score"])` (or `WHERE score IS NOT NULL` in SQL) to drop them. Both give 12 rows with NULLs and 6 without.
- **`unstack(fill_value=0)`** fills only cells that are missing from the index. The NaN scores are stored values, so Mia's row stayed `[nan, nan, nan, nan]` (my run). After `dropna`, Mia vanished from the result and Ana's missing `math_2024` became 0. SQL needs `COALESCE` to do the same.
- **Sorting:** `unstack` sorted the row index (`Ana, Mia, Zed`). The column order followed first appearance when some combinations were absent (my run: `math_2023, sci_2023, sci_2024, math_2024`), so add `.sort_index(axis=1)` before comparing.
- **Duplicates:** `unstack` and `pivot` raise an error when a student/subject/year pair repeats; SQL `SUM(CASE)` silently adds them. Use `pivot_table` with an `aggfunc` in pandas to mirror SQL.
- **stack on a larger frame (1000 rows x 6 columns, 143 NaN cells, my run):** `stack()` gave 6000 rows, `stack(future_stack=True)` gave 6000, `stack(future_stack=False)` gave 5857 and raised a `Pandas4Warning` (the old implementation drops NaN), `stack(dropna=True)` raised `ValueError` (the argument is not allowed with the new implementation), and `stack().dropna()` gave 5857. So in pandas 3.0.5 NaN rows are kept by default and `future_stack` is no longer needed.

**Then explain:**
- **Which tool:** `melt` for plain wide to long; `wide_to_long` when the column names follow `stub + separator + suffix` and you want one column per stub; `stack` when the labels are already in the columns index; `unstack` or `pivot` for long to wide.
- **SQL equivalents:** unpivot = `UNION ALL` (or `CROSS JOIN` with `VALUES`); pivot = `SUM(CASE ...)`. SQLite has no `PIVOT` or `UNPIVOT` keyword; SQL Server, Oracle, Snowflake and BigQuery have their own (not executed here).
- **NULL rule of thumb:** decide whether missing means "unknown" (keep NaN) or "none" (fill 0), before reshaping, not after.
- **Asserts:** UNION ALL equals `melt`, the 2-branch UNION ALL equals `wide_to_long`, and `SUM(CASE)` equals `unstack`, all ordered by student (then subject, year).

**Follow-ups:**
- *How do you unpivot in SQL without writing every column?* Generate the `UNION ALL` text from a column list (the dynamic pivot question later in this part).
- *What does `ignore_index` do in `melt`?* With `ignore_index=False` the original index is kept (not run here).
- *When is `pivot_table` better than `pivot`?* When there can be duplicate keys.

**Common mistakes:**
- Forgetting that `melt` keeps NaN rows (and that `unstack` fills by index, not by value).
- Using the deprecated `future_stack=False` or `dropna=` in pandas 3.
- Comparing unsorted frames.
- Assuming a `pivot` of duplicate keys sums them (it raises).
- Leaving the year as a string after splitting a column name.

### Q29 ⭐⭐ 🟡 SQL string operations in pandas, a translation table with each row run: LOWER/UPPER/TRIM (str.lower, str.strip), SUBSTR (str[a:b] and str.slice), INSTR (str.find), REPLACE (str.replace; pandas 3 default regex is False, check by running with a pattern like ' +'), LIKE 'a%' (str.startswith), LIKE '%a%' (str.contains with regex=False, and with the default regex=True a dot matches anything), case-insensitive LIKE (case=False), CONCAT and || (str.cat with na_rep versus + that propagates NaN), LENGTH (str.len), split (str.split with n and expand), regex extraction (str.extract with named groups), padding (zfill, pad), and the na argument of contains. Use one small contacts DataFrame with NaN and show every result next to the SQLite result.
**Asked at:** pandas user guide pages on reshaping and on working with text data (opened: pivot, pivot_table, melt, wide_to_long, stack, unstack, crosstab, explode, string dtype and the .str accessor); official documentation, not candidate reports; data scientist and analyst rounds; SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds

**Say this first (1 line):** Most SQL string functions have a one-line pandas twin, but the defaults differ in four places that bite: `str.replace` is not a regex any more, `str.contains` is a regex by default, `LIKE` ignores case but `startswith` does not, and NULL becomes NaN (or False) instead of staying NULL.

**Schema and sample data:**
```sql
CREATE TABLE contacts(id INTEGER PRIMARY KEY, name TEXT, email TEXT, code TEXT);
INSERT INTO contacts VALUES
 (1,'Asha Rao',   'Asha.Rao@Example.com', '7'),
 (2,' ben kumar ','ben@test.org',         '42'),
 (3,NULL,         'noatsign',             '123'),
 (4,'Dee  Lee',   'dee.lee@a.b.com',      NULL),
 (5,'chitra',     NULL,                   '5');
```

**SQL answer:** each pair is one SQL expression against one pandas expression in the `cases` list in the Code block (`LOWER`, `UPPER`, `TRIM`, `SUBSTR`, `INSTR`, `REPLACE`, `LIKE`, `||` and `CONCAT_WS`, `LENGTH`, `SUBSTR`+`INSTR` for splitting, `SUBSTR('00000' || code, -5)` and `PRINTF` for padding).

**pandas answer:** the second element of each pair: `str.lower`, `str.upper`, `str.strip`, `str[0:3]`, `str.find`, `str.replace`, `str.startswith`, `str.contains`, `+` and `str.cat`, `str.len`, `str.split(n=1)`, `str.extract` with named groups, `str.zfill` and `str.pad`. The loop prints SQL and pandas results side by side, with `same` or `DIFF`, and asserts both (22 rows).

**Example:** Contacts: `Asha Rao`, ` ben kumar ` (spaces around), NULL, `Dee  Lee` (two spaces), `chitra`; emails `Asha.Rao@Example.com`, `ben@test.org`, `noatsign`, `dee.lee@a.b.com`, NULL. `LOWER`, `UPPER`, `TRIM`, `SUBSTR(name, 1, 3)`, `LENGTH` and `INSTR(email, '@')` match pandas row by row (INSTR is 0 where `find` is -1, plus 1; NULL is NaN). The `DIFF` rows: `REPLACE(name, '  ', ' ')` gives `Dee Lee` while `str.replace(" +", " ")` left `Dee  Lee` (regex is off by default in pandas 3); `name LIKE 'a%'` is 1 for `Asha Rao` while `startswith('a')` is False; `email LIKE '%.%'` is 0 for `noatsign` while `str.contains('.')` (default regex) is True because a dot matches any character; `CONCAT_WS('-', name, code)` gives `123` for the NULL-name row while `str.cat(..., na_rep='')` gives `-123`; `PRINTF('%5s', code)` gives 5 spaces for a NULL code while `pad` keeps NaN.

**Code:** run with `python3 -I`.
```python
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
```

**Output (my run):**
```text
pandas dtypes: {'id': 'int64', 'name': 'str', 'email': 'str', 'code': 'str'} | missing marker in name: nan
LOWER / str.lower
    SQL   : ['asha rao', ' ben kumar ', None, 'dee  lee', 'chitra']
    pandas: ['asha rao', ' ben kumar ', None, 'dee  lee', 'chitra']   [same]
UPPER / str.upper
    SQL   : ['ASHA RAO', ' BEN KUMAR ', None, 'DEE  LEE', 'CHITRA']
    pandas: ['ASHA RAO', ' BEN KUMAR ', None, 'DEE  LEE', 'CHITRA']   [same]
TRIM / str.strip
    SQL   : ['Asha Rao', 'ben kumar', None, 'Dee  Lee', 'chitra']
    pandas: ['Asha Rao', 'ben kumar', None, 'Dee  Lee', 'chitra']   [same]
SUBSTR(name,1,3) / str[0:3]
    SQL   : ['Ash', ' be', None, 'Dee', 'chi']
    pandas: ['Ash', ' be', None, 'Dee', 'chi']   [same]
INSTR(email,'@') / find('@')+1
    SQL   : [9, 4, 0, 8, None]
    pandas: [9, 4, 0, 8, None]   [same]
REPLACE(name,' ','_') / str.replace(' ','_')
    SQL   : ['Asha_Rao', '_ben_kumar_', None, 'Dee__Lee', 'chitra']
    pandas: ['Asha_Rao', '_ben_kumar_', None, 'Dee__Lee', 'chitra']   [same]
collapse double spaces: SQL REPLACE vs pandas str.replace(' +',' ') (default regex=False)
    SQL   : ['Asha Rao', ' ben kumar ', None, 'Dee Lee', 'chitra']
    pandas: ['Asha Rao', ' ben kumar ', None, 'Dee  Lee', 'chitra']   [DIFF]
same, with regex=True
    SQL   : ['Asha Rao', ' ben kumar ', None, 'Dee Lee', 'chitra']
    pandas: ['Asha Rao', ' ben kumar ', None, 'Dee Lee', 'chitra']   [same]
name LIKE 'a%' vs str.startswith('a')
    SQL   : [1, 0, 0, 0, 0]
    pandas: [0, 0, 0, 0, 0]   [DIFF]
name LIKE 'a%' vs str.lower().startswith('a')
    SQL   : [1, 0, 0, 0, 0]
    pandas: [1, 0, 0, 0, 0]   [same]
raw name LIKE 'a%' (NULL kept) vs str.lower().startswith('a')
    SQL   : [1, 0, None, 0, 0]
    pandas: [1, 0, 0, 0, 0]   [DIFF]
email LIKE '%.%' vs str.contains('.', regex=False)
    SQL   : [1, 1, 0, 1, 0]
    pandas: [1, 1, 0, 1, 0]   [same]
email LIKE '%.%' vs str.contains('.') (default regex=True)
    SQL   : [1, 1, 0, 1, 0]
    pandas: [1, 1, 1, 1, 0]   [DIFF]
name LIKE '%ASHA%' vs contains('ASHA', case=False, regex=False)
    SQL   : [1, 0, 0, 0, 0]
    pandas: [1, 0, 0, 0, 0]   [same]
name || '-' || code vs s + '-' + c
    SQL   : ['Asha Rao-7', ' ben kumar -42', None, None, 'chitra-5']
    pandas: ['Asha Rao-7', ' ben kumar -42', None, None, 'chitra-5']   [same]
CONCAT_WS('-', name, code) vs str.cat(c, sep='-', na_rep='')
    SQL   : ['Asha Rao-7', ' ben kumar -42', '123', 'Dee  Lee', 'chitra-5']
    pandas: ['Asha Rao-7', ' ben kumar -42', '-123', 'Dee  Lee-', 'chitra-5']   [DIFF]
CONCAT_WS('-', name, code) vs '-'.join(row.dropna())
    SQL   : ['Asha Rao-7', ' ben kumar -42', '123', 'Dee  Lee', 'chitra-5']
    pandas: ['Asha Rao-7', ' ben kumar -42', '123', 'Dee  Lee', 'chitra-5']   [same]
LENGTH(name) vs str.len()
    SQL   : [8, 11, None, 8, 6]
    pandas: [8, 11, None, 8, 6]   [same]
domain: SUBSTR+INSTR vs str.split('@', n=1).str[1]
    SQL   : ['Example.com', 'test.org', None, 'a.b.com', None]
    pandas: ['Example.com', 'test.org', None, 'a.b.com', None]   [same]
user part: SUBSTR+INSTR vs str.extract(named group)
    SQL   : ['Asha.Rao', 'ben', None, 'dee.lee', None]
    pandas: ['Asha.Rao', 'ben', None, 'dee.lee', None]   [same]
SUBSTR('00000'||code,-5) vs zfill(5)
    SQL   : ['00007', '00042', '00123', None, '00005']
    pandas: ['00007', '00042', '00123', None, '00005']   [same]
PRINTF('%5s', code) vs pad(5)
    SQL   : ['    7', '   42', '  123', '     ', '    5']
    pandas: ['    7', '   42', '  123', None, '    5']   [DIFF]
rows asserted: 22
na handling of contains on NaN: str dtype -> [True, True, False, True, False] | object dtype -> [True, True, False, True, nan] | string dtype -> [True, True, False, True, <NA>] | na=True -> [True, True, False, True, True]
SQL: email LIKE '%@%' -> [1, 1, 0, 1, None]
str.len dtype: float64 | s + 'x' on NaN: nan
title (no INITCAP in SQLite): ["O'Neil", 'Mc Donald', 'Anna-Marie', "They'Re"]
after PRAGMA case_sensitive_like=1, 'Asha' LIKE 'a%': 0
asserts passed (rows marked same agree; rows marked DIFF are the documented differences, asserted to differ)
```

**Edge cases:**
- **NULL and `LIKE`:** SQL `name LIKE 'a%'` is NULL for a NULL name; pandas `str.startswith` returns False for NaN in the `str` dtype. The Code block compares the `COALESCE(..., 0)` form and the raw form.
- **`na` argument of `contains` (my run, email column with one NaN):** `str` dtype default gave `[True, True, False, True, False]`; object dtype gave `nan` for the missing row; `string` dtype gave `<NA>`; `na=True` gave `True`. SQL gave NULL for that row.
- **Case:** SQLite's `LIKE` is case-insensitive for ASCII only, and `PRAGMA case_sensitive_like = 1` made `'Asha' LIKE 'a%'` return 0 in my run. I did not test pandas `case=False` on non-ASCII text.
- **Concatenation:** `||` and `+` both propagate missing values; `CONCAT_WS` skips NULLs (it ran on 3.45.1), and the pandas equivalent is a row-wise join of the non-missing values, not `na_rep=''`.
- **Length:** `str.len()` returns `float64` when NaN is present; `LENGTH` returns an integer or NULL.
- **Title case:** SQLite has no `INITCAP`; `str.title()` gave `O'Neil` for `o'neil` and `Mc Donald` for `mc donald`, but `They'Re` for `they're`, so it is not a safe name formatter.

**Then explain:**
- **Translation table:** the printed output is the table; every `same` row is asserted equal and every `DIFF` row is asserted to differ.
- **Regex defaults (pandas 3.0.5, my run):** `str.replace` regex=False; `str.contains` regex=True. Always pass `regex=` explicitly, and pass `na=` when the column has missing values.
- **Indexing:** SQL `SUBSTR` is 1-based, pandas slices are 0-based.
- **`str` versus `string` dtype:** pandas 3 infers `str` with NaN as the missing marker; `dtype="string"` uses `pd.NA` and returns `<NA>` from `contains`.
- **Other engines (not executed):** regex functions (`REGEXP_REPLACE`, `REGEXP_LIKE`, `REGEXP_SUBSTR` in various spellings), `LPAD`, `INITCAP`, `SPLIT_PART` exist in other engines and not in this SQLite build; the 3.45.1 build used here has no `regexp`, `split_part`, `reverse`, `lpad` or `char_length` (from the Wave A check).

**Follow-ups:**
- *How do you do a regex match in SQLite?* Register a Python function with `create_function("regexp", 2, fn)` (it worked in the Wave A check), or avoid regex with `GLOB`/`LIKE`.
- *What is the pandas twin of `GLOB`?* `str.fullmatch` or `str.match` with a regex (not run here).
- *How do you reverse a string in SQLite?* Not built in; a recursive CTE, or do it in Python.

**Common mistakes:**
- Using `str.replace(" +", " ")` and expecting it to collapse spaces.
- Using `str.contains(".")` for a literal dot.
- Expecting `startswith` to be case-insensitive like `LIKE`.
- Concatenating with `+` and losing rows to NaN.
- Forgetting 0-based versus 1-based positions.

### Q30 ⭐⭐ 🔴 Pivot with totals and subtotals without ROLLUP or CUBE: sales(region, product, amount) with 2 regions and 3 products. SQLite has no ROLLUP, CUBE or GROUPING SETS. Produce the product-by-region table with a row for each region, a subtotal-per-product row and a grand total row (labelled 'ALL'), using UNION ALL of the detail query, the by-product query and the grand-total query, and show the ordering trick (a sort key column) that puts totals last. Explain the NULL-label trap (a real NULL product versus a subtotal NULL; GROUPING() in PostgreSQL, MySQL and SQL Server to tell them apart, hedged, not executed) and that the pivoted totals must equal the plain SUM. Cross-reference Part 1 Q36 for ROLLUP concepts. Add the pandas pivot_table(margins=True) and groupby-based version.
**Asked at:** SQL pivot guides (datadriven.io, DataVidhya, Educative and a Medium write-up, search snippets only; the DataVidhya lesson page opened but showed only its introduction: CASE inside SUM or COUNT, dynamic pivot, NULL categories); guides, not candidate reports; analyst and data engineer rounds at product companies and GCCs; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds

**Say this first (1 line):** Without `ROLLUP` or `CUBE`, build the subtotals as separate `GROUP BY` queries, stack them with `UNION ALL`, label the total rows `'ALL'`, and add a sort-key column so the totals come last; then check that the grand total equals the plain `SUM`.

**Schema and sample data:**
```sql
CREATE TABLE sales(region TEXT, product TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','A',10),('East','A',5),('East','B',20),('East','C',30),
 ('West','A',40),('West','B',15);                                   -- West has no C row
```

**SQL answer:** `sql_long` in the Code block: detail by region and product, a subtotal per region, a subtotal per product, and the grand total, with a `k` column (0 to 3) so `ORDER BY k, region, product` puts totals last. `sql_wide` is the pivoted shape (one row per region plus one `ALL` row, columns A, B, C and Total). `sql_null_label` and `sql_safe` show the NULL-label trap.

**pandas answer:** `pivot_table(index="region", columns="product", values="amount", aggfunc="sum", margins=True, margins_name="ALL")` gives the same table, and a `groupby(...).sum().unstack()` plus an `ALL` row built from column sums gives it a second way. Both are asserted equal to the SQL result.

**Example:** Sales: East A 10 + 5 (two rows), East B 20, East C 30; West A 40, West B 15; West has no C. Detail rows: East A 15, East B 20, East C 30, West A 40, West B 15. Region subtotals: East 65, West 55. Product subtotals: A 55, B 35, C 30. Grand total 120, and the plain `SUM(amount)` is 120. In the pivoted table: East 15, 20, 30, total 65; West 40, 15, NULL, total 55; ALL 55, 35, 30, total 120. The NULL in West's C cell stays NULL (no rows), it is not 0.

**Code:** run with `python3 -I`.
```python
# Q30: pivot with subtotals and a grand total without ROLLUP/CUBE (UNION ALL), and the NULL-label trap; pandas margins.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(region TEXT, product TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','A',10),('East','A',5),('East','B',20),('East','C',30),
 ('West','A',40),('West','B',15);                                   -- West has no C row
""")

# long layout: detail + region subtotal + product subtotal + grand total, with a sort key so totals come last
sql_long = """
SELECT region, product, SUM(amount) AS amount, 0 AS k FROM sales GROUP BY region, product
UNION ALL SELECT region, 'ALL', SUM(amount), 1 FROM sales GROUP BY region
UNION ALL SELECT 'ALL', product, SUM(amount), 2 FROM sales GROUP BY product
UNION ALL SELECT 'ALL', 'ALL', SUM(amount), 3 FROM sales
ORDER BY k, region, product"""
long_df = pd.read_sql(sql_long, con)
print(long_df.to_string(index=False))

# pivoted layout: one row per region, one row 'ALL', a Total column
sql_wide = """
SELECT region,
       SUM(CASE WHEN product = 'A' THEN amount END) AS a,
       SUM(CASE WHEN product = 'B' THEN amount END) AS b,
       SUM(CASE WHEN product = 'C' THEN amount END) AS c,
       SUM(amount) AS total, 0 AS k
FROM sales GROUP BY region
UNION ALL
SELECT 'ALL',
       SUM(CASE WHEN product = 'A' THEN amount END),
       SUM(CASE WHEN product = 'B' THEN amount END),
       SUM(CASE WHEN product = 'C' THEN amount END),
       SUM(amount), 1
FROM sales
ORDER BY k, region"""
wide_df = pd.read_sql(sql_wide, con).drop(columns="k")
print(wide_df.to_string(index=False))
plain = con.execute("SELECT SUM(amount) FROM sales").fetchone()[0]
print("plain SUM:", plain, "| ALL row total:", int(wide_df.loc[wide_df.region == "ALL", "total"].iloc[0]),
      "| sum of region totals:", int(wide_df.loc[wide_df.region != "ALL", "total"].sum()),
      "| sum of A,B,C in ALL row:", int(wide_df.loc[wide_df.region == "ALL", ["a", "b", "c"]].sum(axis=1).iloc[0]))

# the NULL-label trap: a real NULL product plus subtotals that use NULL as the label (what ROLLUP prints)
con.executescript("""
CREATE TABLE sales_n(region TEXT, product TEXT, amount INTEGER);
INSERT INTO sales_n VALUES ('East','A',10),('East',NULL,7),('West','A',5);
""")
sql_null_label = """
SELECT region, product, SUM(amount) AS amount FROM sales_n GROUP BY region, product
UNION ALL SELECT region, NULL, SUM(amount) FROM sales_n GROUP BY region
ORDER BY region, product"""
print("NULL used as the subtotal label (ROLLUP style):")
for r in con.execute(sql_null_label): print("  ", r)
print("  East rows where product IS NULL:", con.execute(f"SELECT COUNT(*) FROM ({sql_null_label.replace('ORDER BY region, product','')}) WHERE region='East' AND product IS NULL").fetchone()[0], "(real NULL product and subtotal are indistinguishable)")
sql_safe = """
SELECT region, COALESCE(product, '(no product)') AS product, SUM(amount) AS amount, 0 AS k FROM sales_n GROUP BY region, product
UNION ALL SELECT region, 'ALL', SUM(amount), 1 FROM sales_n GROUP BY region
ORDER BY region, k, product"""
print("explicit labels:"); 
for r in con.execute(sql_safe): print("  ", r)

# pandas
s = pd.read_sql("SELECT * FROM sales", con)
pt = s.pivot_table(index="region", columns="product", values="amount", aggfunc="sum", margins=True, margins_name="ALL")
pt.columns.name = None
print(pt.to_string())
p_wide = pt.reset_index().rename(columns={"A": "a", "B": "b", "C": "c", "ALL": "total"})

# groupby version: detail rows, then the ALL row
g = s.groupby(["region", "product"])["amount"].sum().unstack("product")
g["total"] = s.groupby("region")["amount"].sum()
all_row = g.sum(); all_row.name = "ALL"                      # column sums (NaN skipped) incl. total
g2 = pd.concat([g, all_row.to_frame().T]).reset_index().rename(columns={"index": "region", "product": "region"})
g2.columns.name = None
g2 = g2.rename(columns={"A": "a", "B": "b", "C": "c"})

def rows(df):
    return [tuple(None if pd.isna(v) else (int(v) if not isinstance(v, str) else v) for v in r) for r in df[["region", "a", "b", "c", "total"]].itertuples(index=False)]
assert rows(wide_df) == rows(p_wide) == rows(g2), (rows(wide_df), rows(p_wide), rows(g2))
assert plain == 120 == int(wide_df.loc[wide_df.region == "ALL", "total"].iloc[0])

# pandas drops a NaN product from pivot_table, so its margins lose the NULL-product amount
n = pd.read_sql("SELECT * FROM sales_n", con)
ptn = n.pivot_table(index="region", columns="product", values="amount", aggfunc="sum", margins=True, margins_name="ALL")
print("pandas margins grand total with a NaN product:", int(ptn.loc["ALL", "ALL"]), "| plain SUM:", int(n["amount"].sum()))
assert int(ptn.loc["ALL", "ALL"]) == 15 and int(n["amount"].sum()) == 22
print("asserts passed (UNION ALL pivot == pivot_table(margins=True) == groupby version; rows: regions sorted, then ALL)")
con.close()
```

**Output (my run):**
```text
region product  amount  k
  East       A      15  0
  East       B      20  0
  East       C      30  0
  West       A      40  0
  West       B      15  0
  East     ALL      65  1
  West     ALL      55  1
   ALL       A      55  2
   ALL       B      35  2
   ALL       C      30  2
   ALL     ALL     120  3
region  a  b    c  total
  East 15 20 30.0     65
  West 40 15  NaN     55
   ALL 55 35 30.0    120
plain SUM: 120 | ALL row total: 120 | sum of region totals: 120 | sum of A,B,C in ALL row: 120
NULL used as the subtotal label (ROLLUP style):
   ('East', None, 7)
   ('East', None, 17)
   ('East', 'A', 10)
   ('West', None, 5)
   ('West', 'A', 5)
  East rows where product IS NULL: 2 (real NULL product and subtotal are indistinguishable)
explicit labels:
   ('East', '(no product)', 7, 0)
   ('East', 'A', 10, 0)
   ('East', 'ALL', 17, 1)
   ('West', 'A', 5, 0)
   ('West', 'ALL', 5, 1)
           A     B     C  ALL
region                       
East    15.0  20.0  30.0   65
West    40.0  15.0   NaN   55
ALL     55.0  35.0  30.0  120
pandas margins grand total with a NaN product: 15 | plain SUM: 22
asserts passed (UNION ALL pivot == pivot_table(margins=True) == groupby version; rows: regions sorted, then ALL)
```

**Edge cases:**
- **Missing cell:** `SUM(CASE ...)` is NULL where no rows exist, and `pivot_table` shows NaN; the totals skip them. Use `COALESCE(..., 0)` only if the report should show zeros.
- **NULL-label trap (my run):** with a real NULL product and subtotals that use NULL as the label (what `ROLLUP` prints), the East rows `(East, NULL, 7)` and `(East, NULL, 17)` cannot be told apart: `WHERE product IS NULL` returns 2 rows. Labelling the subtotal `'ALL'` explicitly, and `COALESCE(product, '(no product)')` for the real NULL, keeps them separate. A real product literally named `ALL` would still collide, so choose a label that cannot be data or use a separate flag column.
- **pandas drops NaN keys:** with a NaN product, `pivot_table(margins=True)` gave a grand total of 15 against a plain SUM of 22 in my run (the 7 for the NULL product vanished), so the margins do not equal the plain sum unless NaN keys are filled first.
- **Ordering:** `UNION ALL` gives no order, and `ORDER BY` of a compound query must use result columns, hence the `k` column (SQLite raised `2nd ORDER BY term does not match any column in the result set` when I tried a computed expression).

**Then explain:**
- **Equivalence:** `ROLLUP(region, product)` gives detail, region subtotals and the grand total; `CUBE` adds product subtotals; here I wrote all four levels by hand. `GROUPING SETS` is the general form. SQLite has none of the three.
- **Telling a subtotal NULL from a real NULL:** `GROUPING(col)` returns 1 for a subtotal row in PostgreSQL, MySQL and SQL Server (not executed here, from memory); with `UNION ALL` you choose the label yourself.
- **Check:** the grand total must equal the plain `SUM(amount)`, and the `ALL` row total must equal the sum of the region totals (all 120 in my run).
- **Cost:** each `UNION ALL` branch scans the table again; with `ROLLUP` the engine can usually do it in one pass (I did not measure this).
- Cross-reference: Part 1 Q36 for ROLLUP concepts.

**Follow-ups:**
- *How would you add a subtotal per region and product group?* One more `UNION ALL` branch with the right `GROUP BY`.
- *Can a window function give the totals?* Yes, `SUM(...) OVER ()` on the detail rows, but that repeats the total on every row instead of adding a total row.
- *How do you sort so `ALL` is last but alphabetical otherwise?* A `k` or `region = 'ALL'` key as the first `ORDER BY` term (in a compound query it has to be a result column).

**Common mistakes:**
- Using NULL as the subtotal label and then mixing it with real NULLs.
- Forgetting the sort key, so totals appear in the middle.
- Subtotals that do not add up because of a filter in only one branch.
- `pivot_table(margins=True)` with NaN keys, giving a smaller total than the plain sum.
- Using `UNION` instead of `UNION ALL` and removing equal-looking rows (two regions with the same total).


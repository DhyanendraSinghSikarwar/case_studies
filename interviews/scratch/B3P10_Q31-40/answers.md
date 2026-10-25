### Q31 ⭐⭐ 🔴 Dynamic pivot at concept level (column list unknown in advance): sales(region, product, month, amount) where new months appear every month. Explain why SQL cannot return a result with a column list decided by the data (the column list is fixed at parse time), then show the standard approach: query the distinct values, generate the SUM(CASE WHEN month = 'x' THEN amount END) AS col text in the application (Python), execute it, and run it on SQLite with the generated SQL printed. Cover quoting identifiers and escaping string literals (SQL injection if month values come from users: use parameter binding for values and a whitelist or quote function for identifiers), column limits, NULL or blank categories, and the 'other' column that keeps totals reconciled. Mention SQL Server dynamic SQL with QUOTENAME and sp_executesql, PostgreSQL crosstab, Snowflake PIVOT ANY and BigQuery EXECUTE IMMEDIATE (hedged, not executed). Say when you would instead return long format and pivot in the BI tool or pandas.
**Asked at:** SQL pivot guides (datadriven.io, DataVidhya, Educative and a Medium write-up, search snippets only; the DataVidhya lesson page opened but showed only its introduction: CASE inside SUM or COUNT, dynamic pivot, NULL categories); guides, not candidate reports; analyst and data engineer rounds at product companies and GCCs; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** SQL cannot return a column list chosen by the data, because the columns are fixed when the statement is parsed. So I ask the data for the distinct categories, generate the `SUM(CASE WHEN month = ? THEN amount END) AS "col"` text in the application, bind the values as parameters, quote the aliases, and add an `other` and a `total` column so the numbers still reconcile.

**Schema and sample data:**
```sql
CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('North','pen','2024-01',10),('North','pen','2024-02',20),('North','ink','2024-03',5),
 ('North','pen','2024-04',7), ('South','pen','2024-02',30),('South','ink','2024-04',8),
 ('South','ink',NULL,4),      ('South','pen','',6),
 ('East', 'pen','2023-12',9), ('East', 'ink','2024-04',1),
 ('East', 'pen','x''; DROP TABLE sales;--',2);
```
The month column deliberately holds a NULL, a blank, an old month and a hostile string.

**SQL answer:** The generated statement is printed in the Code block output (`sql` and `params` variables). Steps: (1) `SELECT DISTINCT month FROM sales`; (2) keep only values that match the whitelist `^\d{4}-\d{2}$` in Python and take the newest three (`MAX_COLS = 3`); (3) build one `SUM(CASE WHEN month = ? THEN amount END) AS "<month>"` per kept month, where the value is a bound parameter and only the alias is spliced in, wrapped by `quote_ident`; (4) add `other` as `SUM(CASE WHEN month IS NULL OR month NOT IN (?,?,?) THEN amount END)` and `SUM(amount) AS total`; (5) `GROUP BY region`.

**pandas answer:** `df["bucket"] = df["month"].where(df["month"].isin(months), "other")`, then `pivot_table(index="region", columns="bucket", values="amount", aggfunc="sum")`, `reindex(columns=months + ["other"])`, and `total` from `groupby("region")["amount"].sum()`. pandas has no parse-time column list, so the dynamic part is free: the columns are whatever the data holds.

**Example:** Distinct months seen: 2024-01, 2024-02, 2024-03, 2024-04, NULL, blank, 2023-12 and the hostile string. Five pass the whitelist; the newest three are 2024-02, 2024-03 and 2024-04, so those get their own columns. North: 02 = 20, 03 = 5, 04 = 7, and 2024-01 (10) falls into `other`, total 42. South: 02 = 30, 04 = 8; the NULL-month row (4) and the blank-month row (6) go to `other` = 10, total 48. East: 04 = 1; 2023-12 (9) and the hostile string (2) go to `other` = 11, total 12. Listed columns plus `other` equal `total` on every row (asserted).

**Code:** run with `python3 -I`; the two results are compared after the stated sort, then asserted.
```python
# Dynamic pivot: the column list comes from the data, so the application generates the SQL text.
import re
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('North','pen','2024-01',10),('North','pen','2024-02',20),('North','ink','2024-03',5),
 ('North','pen','2024-04',7), ('South','pen','2024-02',30),('South','ink','2024-04',8),
 ('South','ink',NULL,4),      ('South','pen','',6),
 ('East', 'pen','2023-12',9), ('East', 'ink','2024-04',1),
 ('East', 'pen','x''; DROP TABLE sales;--',2);
""")

def quote_ident(name):                       # identifier quoting: wrap in double quotes, double any inner quote
    return '"' + name.replace('"', '""') + '"'

# 1) ask the data for the categories, keep only values that pass a whitelist, newest N get their own column
MAX_COLS = 3
good = re.compile(r"^\d{4}-\d{2}$")
distinct = [r[0] for r in con.execute("SELECT DISTINCT month FROM sales")]
months = sorted((m for m in distinct if m is not None and good.match(m)), reverse=True)[:MAX_COLS][::-1]
print("distinct months seen:", distinct)
print("columns that get their own column:", months)

# 2) generate the SQL text: values are bound with ?, only the alias is spliced in (and it is quoted)
cols = ",\n  ".join(f"SUM(CASE WHEN month = ? THEN amount END) AS {quote_ident(m)}" for m in months)
marks = ",".join("?" * len(months))
other = f"SUM(CASE WHEN month IS NULL OR month NOT IN ({marks}) THEN amount END) AS other"
sql = (f"SELECT region,\n  {cols},\n  {other},\n  SUM(amount) AS total\nFROM sales\nGROUP BY region ORDER BY region")
params = months + months
print(sql)
print("params:", params)
cur = con.execute(sql, params)
header = [d[0] for d in cur.description]
sql_df = pd.DataFrame(cur.fetchall(), columns=header)
print(sql_df.to_string(index=False))

# 3) the reconciliation check: listed columns + other = total (NULL treated as 0)
chk = sql_df.fillna(0)
assert (chk[months + ["other"]].sum(axis=1) == chk["total"]).all()

# the naive version: NOT IN alone silently loses the NULL-month rows
naive = con.execute(f"SELECT SUM(amount) FROM sales WHERE month NOT IN ({marks})", months).fetchone()[0]
good_other = con.execute(f"SELECT SUM(amount) FROM sales WHERE month IS NULL OR month NOT IN ({marks})", months).fetchone()[0]
print("other with NOT IN only:", naive, "| other with IS NULL OR NOT IN:", good_other)

# pandas version of the same thing
df = pd.read_sql("SELECT * FROM sales", con)
df["bucket"] = df["month"].where(df["month"].isin(months), "other")   # NaN is not in the list -> 'other'
pv = df.pivot_table(index="region", columns="bucket", values="amount", aggfunc="sum")
pv = pv.reindex(columns=months + ["other"])
pv["total"] = df.groupby("region")["amount"].sum()
pv = pv.reset_index().rename_axis(columns=None)
print(pv.to_string(index=False))
a = sql_df.sort_values("region").reset_index(drop=True)
b = pv.sort_values("region").reset_index(drop=True)
pd.testing.assert_frame_equal(a, b, check_dtype=False)     # compared after sorting by region; NULL == NaN here

# the injection attempt: what happens if the weird month were spliced in as text
evil = "x'; DROP TABLE sales;--"
print("quote_ident(evil):", quote_ident(evil))
try:
    con.execute("SELECT 1 AS " + evil)
except sqlite3.Error as e:
    print("spliced raw ->", type(e).__name__, e)
print("sales still has", con.execute("SELECT COUNT(*) FROM sales").fetchone()[0], "rows")
print("SQLite limits: columns =", con.getlimit(sqlite3.SQLITE_LIMIT_COLUMN), "| bound parameters =", con.getlimit(sqlite3.SQLITE_LIMIT_VARIABLE_NUMBER))
con.close()
print("asserts passed")
```

**Output (my run):**
```text
distinct months seen: ['2024-01', '2024-02', '2024-03', '2024-04', None, '', '2023-12', "x'; DROP TABLE sales;--"]
columns that get their own column: ['2024-02', '2024-03', '2024-04']
SELECT region,
  SUM(CASE WHEN month = ? THEN amount END) AS "2024-02",
  SUM(CASE WHEN month = ? THEN amount END) AS "2024-03",
  SUM(CASE WHEN month = ? THEN amount END) AS "2024-04",
  SUM(CASE WHEN month IS NULL OR month NOT IN (?,?,?) THEN amount END) AS other,
  SUM(amount) AS total
FROM sales
GROUP BY region ORDER BY region
params: ['2024-02', '2024-03', '2024-04', '2024-02', '2024-03', '2024-04']
region  2024-02  2024-03  2024-04  other  total
  East      NaN      NaN        1     11     12
 North     20.0      5.0        7     10     42
 South     30.0      NaN        8     10     48
other with NOT IN only: 27 | other with IS NULL OR NOT IN: 31
region  2024-02  2024-03  2024-04  other  total
  East      NaN      NaN      1.0   11.0     12
 North     20.0      5.0      7.0   10.0     42
 South     30.0      NaN      8.0   10.0     48
quote_ident(evil): "x'; DROP TABLE sales;--"
spliced raw -> OperationalError unrecognized token: "x'; DROP TABLE sales;--"
sales still has 11 rows
SQLite limits: columns = 2000 | bound parameters = 250000
asserts passed
```

**Edge cases:**
- NULL month: `month NOT IN (...)` is UNKNOWN for a NULL month, so without `month IS NULL OR` the NULL row vanishes from `other`. The run shows `other` = 27 with `NOT IN` alone versus 31 with the `IS NULL OR` guard (31 = NULL-month 4 + blank 6 + 2024-01 10 + 2023-12 9 + hostile 2; the NOT IN-only version loses the NULL row's 4). Part 1 Q13 has the NOT IN mechanics; the new point is that the catch-all column silently breaks the reconciliation.
- Blank category: `''` is a real value; here it falls into `other`. Whether blank should be its own 'unknown' column is a business choice; say it out loud.
- A region with no row in a month gets NULL, not 0 (no ELSE 0). A pandas pivot also gives NaN, which is why the numbers print as floats.
- The hostile month never becomes a column because it fails the whitelist, and it is never concatenated into SQL: values go through `?`. Spliced raw as an alias it is a syntax error (the run shows `OperationalError`). Honest note: Python's `execute()` accepts only one statement, so the `DROP TABLE` part would not have run through it anyway; drivers or `executescript` that accept several statements are where this bites (not executed here).
- Column limits: this build allows 2000 columns and 250000 bound parameters (read with `getlimit`; compile-time options, so other builds differ). Other engines have their own limits (not checked here).
- Quoting: bind parameters cannot be used for identifiers, so the alias needs `quote_ident` (double quotes, inner quotes doubled) plus a whitelist; that is the SQLite and standard-SQL convention, other engines use other quote characters (not executed).

**Then explain:**
- **Why SQL cannot do it:** a statement is parsed and planned before any row is read, so the output column names and count must already be known. The result shape cannot depend on the data it is about to read.
- **The standard fix:** two round trips. Query 1 gets the distinct values, the application builds the text, query 2 runs it. Values go in as parameters; identifiers are whitelisted and quoted.
- **`other` and `total`:** `total` is the reconciliation control (`SUM(amount)` for the group). `other` catches everything that did not get a column, so listed columns + `other` = `total` always; if they do not, the generator has a bug.
- **Dialects (not executed here):** SQL Server builds a string with `QUOTENAME` and runs it with `sp_executesql`; PostgreSQL `crosstab` (the `tablefunc` extension) still needs the output column list declared in the query, so the application still has to know the columns; Snowflake documents a `PIVOT` form that takes `ANY` in the value list, and BigQuery pivots with `EXECUTE IMMEDIATE` on a generated string. I am describing these from memory and did not run any of them.
- **When I would not do it in SQL:** return long format (`region, month, amount`) and pivot in the BI tool or pandas. New months then add rows, not columns, nothing breaks, and no SQL text is generated.

**Follow-ups:**
- *Can you do this in one query?* Not in portable SQL; the column list is fixed at parse time.
- *Why not a stored procedure or a view?* A view has the same fixed column list; it would have to be recreated each month.
- *What if there are 400 months?* Cap the columns, send the rest to `other`, or return long format.

**Common mistakes:**
- Building the SQL with an f-string around user-controlled values (injection).
- Forgetting that a NULL category breaks `NOT IN`, so the `other` column does not reconcile.
- Using `ELSE 0` everywhere and hiding the difference between 'no sales' and 'zero sales'.
- Hard-coding the month list and forgetting it every month.
- Believing `crosstab` is dynamic.


### Q32 ⭐ 🟡 Regular expressions are missing in SQLite: confirm by running that 'a' REGEXP 'a' fails with 'no such function: regexp' and that SPLIT_PART, REVERSE, LPAD and CHAR_LENGTH fail too, while CONCAT, CONCAT_WS, STRING_AGG, FORMAT, PRINTF, OCTET_LENGTH, UNHEX and IIF exist in 3.45.1. Show how to register a regexp function from Python with sqlite3 create_function (executed) and how the same job is done with GLOB character classes ([0-9], [^a-z]) and LIKE. Give a dialect map, hedged and not executed, for REGEXP_LIKE, REGEXP_REPLACE, REGEXP_SUBSTR (PostgreSQL, Oracle, MySQL 8, Snowflake, BigQuery), SPLIT_PART, STRING_AGG and CONCAT_WS NULL behaviour, and say that Python-registered functions are not available to other clients of the database file.
**Asked at:** SQLite lang_corefunc and lang_expr documentation (opened: trim character sets, ASCII-only lower/upper and LIKE, length versus octet_length, concat/concat_ws NULL rules, CAST rules, IS DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL table); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds
**Say this first (1 line):** SQLite 3.45.1 has no built-in `REGEXP` (the operator calls a `regexp()` function that does not exist), no `SPLIT_PART`, `REVERSE`, `LPAD` or `CHAR_LENGTH`; I register a regexp from Python with `create_function`, or use `GLOB` classes and `LIKE`, and I remember that a Python function exists only in that connection.

**Schema and sample data:**
```sql
CREATE TABLE codes(code TEXT);
INSERT INTO codes VALUES ('AB-1234'),('ab-1234'),('AB-12x4'),('AB-123'),(NULL),('AB-12345');
```
Goal: keep codes shaped like two capital letters, a dash and exactly four digits.

**SQL answer:** Three versions are in the Code block: `q_re` (`code REGEXP '^[A-Z]{2}-\d{4}$'`, needs the registered function), `q_glob` (`GLOB '[A-Z][A-Z]-[0-9][0-9][0-9][0-9]'`) and `q_like` (`LIKE '__-____'`, which only knows `_` and `%`).

**pandas answer:** `df["code"].str.contains(r"^[A-Z]{2}-\d{4}$", regex=True)` (the default). The NaN row gives False, not missing, so it drops out of the filter.

**Example:** Six codes. `AB-1234` is the only one with two capitals, a dash and four digits. `ab-1234` fails the capital-letter classes (GLOB and the regex are case-sensitive). `AB-12x4` has a letter in the digit part. `AB-123` is one digit short and `AB-12345` one too long (the regex anchors `^...$`; GLOB has no quantifier, so four `[0-9]` in a row pin the length). NULL gives UNKNOWN. All three methods return `['AB-1234']`. `LIKE '__-____'` only checks the length and the dash, so it also returns `ab-1234` and `AB-12x4`.

**Code:** run with `python3 -I`; the two results are compared after the stated sort, then asserted.
```python
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
```

**Output (my run):**
```text
SQLite 3.45.1 | pandas 3.0.5
--- missing in this build
'a' REGEXP 'a'                   -> ERROR: no such function: REGEXP
split_part('a,b',',',1)          -> ERROR: no such function: split_part
reverse('abc')                   -> ERROR: no such function: reverse
lpad('7',3,'0')                  -> ERROR: no such function: lpad
char_length('abc')               -> ERROR: no such function: char_length
--- present in this build
concat('a',NULL,'b')             -> ab
concat_ws(',','a',NULL,'b')      -> a,b
printf('%05.1f',3.14159)         -> 003.1
format('%d items',3)             -> 3 items
octet_length('é')                -> 2
hex(unhex('4142'))               -> 4142
iif(1<2,'yes','no')              -> yes
NULL IS DISTINCT FROM 1          -> 1
string_agg ordered -> c|b|a
--- after create_function
'abc123' REGEXP '\d+'      -> 1
NULL REGEXP 'a'           -> None
regexp: ['AB-1234']
glob  : ['AB-1234']
like  : ['AB-1234', 'ab-1234', 'AB-12x4']
rows with only A-Z, 0-9 and - (GLOB negated class): ['AB-1234', 'AB-123', 'AB-12345']
'a' LIKE 'A' -> 1 | 'Ä' LIKE 'ä' -> 0 | 'a' GLOB 'A' -> 0
after PRAGMA case_sensitive_like=ON: 'a' LIKE 'A' -> 0
second connection -> no such function: REGEXP
pandas: ['AB-1234']
asserts passed
```

**Edge cases:**
- `X REGEXP Y` is rewritten as `regexp(Y, X)`: pattern first, value second. Getting the argument order wrong gives silent nonsense. The Python function must return NULL (None) for NULL input to keep three-valued logic.
- `GLOB` has no `{n}`, `+`, `|` or optional parts; it is Unix-style globbing with `*`, `?`, `[a-z]` and `[^a-z]`. It cannot express 'one or more digits' exactly (the run uses a negated class: `NOT GLOB '*[^0-9A-Z-]*'` finds values made only of allowed characters).
- `LIKE` is ASCII case-insensitive (`'a' LIKE 'A'` is 1, `'Ä' LIKE 'ä'` is 0 in this build); `PRAGMA case_sensitive_like = ON` made `'a' LIKE 'A'` return 0 in the run. GLOB is always case-sensitive.
- The `regexp` function is per connection. A second connection (a BI tool, the `sqlite3` shell) fails with `no such function: REGEXP`. Python-registered functions are not stored in the database file.
- Error text: calling `'a' REGEXP 'a'` without the function fails with `no such function: REGEXP` on this build.

**Then explain:**
- **Confirmed missing here:** `REGEXP`, `SPLIT_PART`, `REVERSE`, `LPAD`, `CHAR_LENGTH`. **Confirmed present:** `concat`, `concat_ws`, `string_agg` (with `ORDER BY` inside), `format`, `printf`, `octet_length`, `unhex`, `iif`, `IS DISTINCT FROM`.
- **NULL rules of the two concatenations (run):** `concat('a',NULL,'b')` gives `ab` and `concat_ws(',','a',NULL,'b')` gives `a,b`: both skip NULL, unlike `||`, which returns NULL.
- **Padding instead of `LPAD`:** `printf('%05d', n)` for numbers, or `substr('0000' || n, -4)` for text.
- **Dialect map, not executed here (from memory, check your version):** PostgreSQL has `~`, `regexp_replace`, `regexp_match` and `substring(... from pattern)`, `split_part`, `string_agg`; MySQL 8 has `REGEXP_LIKE`, `REGEXP_REPLACE`, `REGEXP_SUBSTR` and `CONCAT_WS` that skips NULL arguments; Oracle has `REGEXP_LIKE`, `REGEXP_SUBSTR`, `REGEXP_REPLACE` and `LISTAGG`; Snowflake has `REGEXP_LIKE`, `REGEXP_SUBSTR`, `REGEXP_REPLACE`, `SPLIT_PART`; BigQuery has `REGEXP_CONTAINS`, `REGEXP_EXTRACT`, `REGEXP_REPLACE`, `SPLIT` and `STRING_AGG`. Function names and NULL behaviour differ by engine; I did not run any of them.
- **When to avoid the Python route:** if other clients read the same file, put the cleaning in the application or load an extension.

**Follow-ups:**
- *Why not use `LIKE` for everything?* No character classes, no quantifiers, and it ignores ASCII case.
- *Is `REGEXP` an operator or a function?* In SQLite it is sugar for calling the user-defined function `regexp`; that is why defining it makes it work.
- *Does `deterministic=True` matter?* It lets SQLite use the function in indexes and expressions that need determinism; the answer is the same here.

**Common mistakes:**
- Assuming `REGEXP` works because it does in MySQL.
- Swapping the argument order in the Python function.
- Forgetting the function dies with the connection.
- Using `LIKE '[0-9]%'` (brackets are GLOB, not LIKE).
- Expecting `LIKE` to match `Ä` and `ä`.


### Q33 ⭐ 🔴 Hard text cleaning and Unicode: names(id, name) containing a non-breaking space U+00A0, a tab, a newline, a zero-width space U+200B, accented letters in composed (é as U+00E9) and decomposed (e + U+0301) forms, German 'ß', Turkish 'İ', and an emoji. Show by running that TRIM misses U+00A0 and tabs, that LENGTH counts code points while OCTET_LENGTH counts bytes (and LENGTH stops at an embedded NUL), that UPPER and LOWER change only ASCII letters in SQLite, that 'é' = 'É' COLLATE NOCASE is false and that the composed and decomposed forms are different strings in SQL. Use HEX and UNICODE to find invisible characters, REPLACE with CHAR(160), CHAR(9), CHAR(10) and CHAR(8203) to clean, and say that Unicode normalisation (NFC or NFD) is not in SQLite so it is done in the application. Add the pandas str.normalize('NFC'), str.casefold and str.strip, and show pandas strip removes NBSP while SQL TRIM does not.
**Asked at:** SQLite lang_corefunc and lang_expr documentation (opened: trim character sets, ASCII-only lower/upper and LIKE, length versus octet_length, concat/concat_ws NULL rules, CAST rules, IS DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL table); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** SQLite string functions count code points (`LENGTH`) or bytes (`OCTET_LENGTH`) and fold case for ASCII only; `TRIM` strips spaces only unless you give the characters, composed and decomposed accents are different strings, and normalisation belongs in the application; pandas `strip`, `casefold` and `normalize` do the work SQLite cannot.

**Schema and sample data:**
The values contain NUL, NBSP and emoji, so they are inserted from Python parameters. The rows (id: content) are:
```text
1 'Asha' NBSP(U+00A0) 'Rao'     2 TAB 'Ben' SPACE        3 'Chi' LF 'tra'
4 'Dev' ZWSP(U+200B)           5 'René' (é = U+00E9)     6 'Rene' + U+0301 + 'e' (decomposed é)
7 'Straße'                      8 U+0130 'stanbul'        9 'Zoe ' + emoji U+1F600
10 'a' NUL 'b'
```
```sql
CREATE TABLE names(id INTEGER PRIMARY KEY, name TEXT);
```

**SQL answer:** `sql_df` query in the Code block (length, octet_length, length of trim, hex), the `scan` recursive CTE that walks each string character by character and keeps suspicious code points (`unicode()` of 160, 9, 10, 8203, 769), and the `clean` query that nests `replace(..., char(160), ' ')`, tab, newline and `char(8203)` removal inside `trim`. Part 9 Q1 has recursion mechanics.

**pandas answer:** `s.str.len()`, `s.str.normalize("NFC")`, `s.str.casefold()`, `s.str.strip()` and the clean-up `s.str.replace("\u200b", "", regex=False).str.replace(r"\s+", " ", regex=True).str.strip()` (the Code block shows each call).

**Example:** Row 1 'Asha<NBSP>Rao': 8 code points, 9 bytes (NBSP is 2 bytes in UTF-8, hex `C2A0`); `TRIM` changes nothing, so the NBSP stays and a join on 'Asha Rao' with a normal space fails. Row 2 '<TAB>Ben<space>': length 5, after `TRIM` 4: the trailing space went, the leading tab stayed. Row 4: 'Dev' plus U+200B shows length 4 but looks like 3; `hex` ends in `E2808B`. Rows 5 and 6 print identically but have lengths 5 and 6 and are not equal. Row 10: `LENGTH` stops at the NUL (1) while `OCTET_LENGTH` counts all three bytes. After the `replace` chain rows 1 to 4 become 'Asha Rao', 'Ben', 'Chi tra', 'Dev'; pandas gives the same four strings (asserted).

**Code:** run with `python3 -I`; the two results are compared after the stated sort, then asserted.
```python
# Hard text cleaning and Unicode in SQLite versus pandas.
import sqlite3
import unicodedata
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE names(id INTEGER PRIMARY KEY, name TEXT)")
rows = [
    (1, "Asha Rao"),            # NBSP between words
    (2, "\tBen "),                   # tab and a space around
    (3, "Chi\ntra"),                 # newline inside
    (4, "Dev​"),                # zero-width space at the end
    (5, "Renée"),               # composed e-acute
    (6, "Renée"),              # decomposed e + combining acute
    (7, "Straße"),              # German sharp s
    (8, "İstanbul"),            # Turkish capital dotted I
    (9, "Zoe \U0001F600"),           # emoji
    (10, "a\x00b"),                  # embedded NUL
]
con.executemany("INSERT INTO names VALUES (?,?)", rows)

q = """SELECT id, length(name) AS len, octet_length(name) AS bytes, length(trim(name)) AS len_trim,
              hex(name) AS hex_name
       FROM names ORDER BY id"""
sql_df = pd.read_sql(q, con)
print(sql_df.to_string(index=False))

# 1) TRIM versus the characters it does not know
print("trim keeps NBSP/tab?",
      con.execute("SELECT length(trim(?)), length(trim(?))", (" x ", "\tx\t")).fetchone(), "(3 and 3 = nothing stripped)")
print("trim with explicit set:",
      con.execute("SELECT length(trim(?, char(160, 9, 10, 32)))", (" \tx \n",)).fetchone()[0])

# 2) case folding is ASCII-only
print("upper/lower:", con.execute("SELECT upper('straße é'), lower('ÀB İ'), 'é' = 'É' COLLATE NOCASE, 'e' = 'E' COLLATE NOCASE").fetchone())

# 3) composed and decomposed are different strings
print("composed = decomposed:", con.execute("SELECT (SELECT name FROM names WHERE id=5) = (SELECT name FROM names WHERE id=6)").fetchone()[0],
      "| lengths:", con.execute("SELECT length(name) FROM names WHERE id IN (5,6) ORDER BY id").fetchall())

# 4) find invisible characters: unicode() of the first char, and a scan with a recursive CTE
scan = """
WITH RECURSIVE ch(id, pos, cp) AS (
  SELECT id, 1, unicode(substr(name,1,1)) FROM names WHERE id IN (1,2,3,4,6)
  UNION ALL
  SELECT n.id, ch.pos+1, unicode(substr(n.name, ch.pos+1, 1))
  FROM ch JOIN names n ON n.id = ch.id WHERE ch.pos < length(n.name)
)
SELECT id, pos, cp FROM ch WHERE cp IN (160, 9, 10, 8203, 769) ORDER BY id, pos"""
print("suspect code points (id, position, code point):", con.execute(scan).fetchall())

# 5) clean with REPLACE and CHAR
clean = """SELECT id, trim(replace(replace(replace(replace(name, char(160), ' '), char(9), ' '), char(10), ' '), char(8203), '')) AS cleaned
           FROM names WHERE id IN (1,2,3,4) ORDER BY id"""
sql_clean = pd.read_sql(clean, con)
print(sql_clean.to_string(index=False))

# 6) pandas
s = pd.Series([r[1] for r in rows], index=[r[0] for r in rows], name="name")
print("pandas dtype:", s.dtype)
print("pandas strip on NBSP-x-NBSP and tab-x-tab:", pd.Series(["\u00a0x\u00a0", "\tx\t"]).str.strip().tolist())
print("strip leaves the zero-width space: length of 'Dev'+U+200B after strip =", pd.Series(["Dev\u200b"]).str.strip().str.len()[0])
same = (s.str.len().values == sql_df["len"].values)
print("pandas len equals SQL length on rows:", [int(i) for i in sql_df["id"][same]], "| differs on:", [int(i) for i in sql_df["id"][~same]])
assert list(sql_df["id"][~same]) == [10]
nfc = s.str.normalize("NFC")
print("NFC makes 5 == 6:", nfc[5] == nfc[6], "| raw:", s[5] == s[6])
print("casefold('Straße') =", pd.Series(["Straße"]).str.casefold()[0], "| upper('ß') =", pd.Series(["ß"]).str.upper()[0],
      "| lower('İ') length =", len(pd.Series(["İ"]).str.lower()[0]))
# NUL: SQL length stops at the NUL, Python len does not
print("NUL row: SQL length =", sql_df.loc[9, "len"], "| Python len =", len("a\x00b"), "| octet_length =", sql_df.loc[9, "bytes"])

p_clean = (s[[1, 2, 3, 4]].str.replace("​", "", regex=False)
            .str.replace(r"\s+", " ", regex=True).str.strip())    # \s matches NBSP, tab, newline in Python regex
print(p_clean.tolist())
assert sql_clean["cleaned"].tolist() == p_clean.tolist() == ["Asha Rao", "Ben", "Chi tra", "Dev"]

# Python title() surprise for names (pandas str.title)
print("str.title:", pd.Series(["o'neil", "mcdonald", "ASHA rao"]).str.title().tolist())
print("composed != decomposed in SQL, equal after unicodedata NFC:",
      unicodedata.normalize("NFC", rows[4][1]) == unicodedata.normalize("NFC", rows[5][1]))
con.close()
print("asserts passed")
```

**Output (my run):**
```text
 id  len  bytes  len_trim           hex_name
  1    8      9         8 41736861C2A052616F
  2    5      5         4         0942656E20
  3    7      7         7     4368690A747261
  4    4      6         4       446576E2808B
  5    5      6         5       52656EC3A965
  6    6      7         6     52656E65CC8165
  7    6      7         6     53747261C39F65
  8    8      9         8 C4B07374616E62756C
  9    5      8         5   5A6F6520F09F9880
 10    1      3         1             610062
trim keeps NBSP/tab? (3, 3) (3 and 3 = nothing stripped)
trim with explicit set: 1
upper/lower: ('STRAßE é', 'Àb İ', 0, 1)
composed = decomposed: 0 | lengths: [(5,), (6,)]
suspect code points (id, position, code point): [(1, 5, 160), (2, 1, 9), (3, 4, 10), (4, 4, 8203), (6, 5, 769)]
 id  cleaned
  1 Asha Rao
  2      Ben
  3  Chi tra
  4      Dev
pandas dtype: str
pandas strip on NBSP-x-NBSP and tab-x-tab: ['x', 'x']
strip leaves the zero-width space: length of 'Dev'+U+200B after strip = 4
pandas len equals SQL length on rows: [1, 2, 3, 4, 5, 6, 7, 8, 9] | differs on: [10]
NFC makes 5 == 6: True | raw: False
casefold('Straße') = strasse | upper('ß') = SS | lower('İ') length = 2
NUL row: SQL length = 1 | Python len = 3 | octet_length = 3
['Asha Rao', 'Ben', 'Chi tra', 'Dev']
str.title: ["O'Neil", 'Mcdonald', 'Asha Rao']
composed != decomposed in SQL, equal after unicodedata NFC: True
asserts passed
```

**Edge cases:**
- `TRIM(x, chars)` removes any of the listed characters; `trim(?, char(160, 9, 10, 32))` stripped an NBSP, tab, space and newline run to leave `x`.
- `upper('straße é')` gives `STRAßE é`: only ASCII letters change. `lower('ÀB İ')` gives `Àb İ`. `'é' = 'É' COLLATE NOCASE` is 0 (while `'e' = 'E' COLLATE NOCASE` is 1). So case-insensitive de-duplication of accented names needs the application or an ICU build (this build has none).
- pandas is Unicode-aware and so differs from SQL: `casefold('Straße')` is `strasse`, `upper('ß')` is `SS`, and `lower('İ')` has length 2 (i plus a combining dot). Do not expect pandas and SQL case folding to agree on non-ASCII text.
- `str.len()` agrees with SQL `LENGTH` on every row except the NUL row (SQL 1, Python 3), which the code asserts.
- Emoji and other characters outside the BMP are one code point in SQLite's `LENGTH`; grapheme clusters (a flag, a family emoji) are several. Not run for those.
- `Series.str.title()` on `"o'neil"` gave `O'Neil`, `mcdonald` gave `Mcdonald`: title-casing names is wrong for 'McDonald' and similar; treat it as a display hack.
- SQLite has no `normalize()`; NFC/NFD happens in the application (`unicodedata.normalize` or `str.normalize`).

**Then explain:**
- **Code points versus bytes:** `LENGTH` counts characters (it stops at an embedded NUL for TEXT), `OCTET_LENGTH` counts bytes. `é` is 1 and 2; an emoji is 1 and 4.
- **Finding invisible characters:** `HEX(name)` shows the bytes (`C2A0` is NBSP, `E2808B` is the zero-width space, `CC81` is a combining acute); `UNICODE(substr(name, i, 1))` gives the code point; compare `LENGTH(name)` with the length you can see.
- **TRIM:** by default only the space character. List the others explicitly or use `REPLACE`.
- **Normalisation:** 'é' as one code point and as two are different strings in SQL (`=` is false, lengths 5 and 6). Normalise to NFC on ingestion.
- **pandas:** `str.strip()` removes NBSP, tab and newline (it strips any whitespace); that is a real difference from `TRIM`. It does not remove a zero-width space (a string ending in U+200B kept length 4 after `strip` in the run), so the replace of `\u200b` is still needed.
- Dialect note: other engines have their own `TRIM`, `LENGTH` and collation rules; not executed here.

**Follow-ups:**
- *Why can't I just add `COLLATE NOCASE`?* It folds ASCII letters only.
- *Where do I normalise?* At load time, once, in the application (NFC), and store the clean text; then SQL comparisons are exact.
- *How do I find non-ASCII rows?* compare `LENGTH(name)` with `OCTET_LENGTH(name)`: they differ when a multi-byte character is present (an NBSP, an accent or an emoji).

**Common mistakes:**
- Trusting that `TRIM` removed 'whitespace' that came from a web page or Excel.
- Joining on names with an NBSP and getting no match.
- Believing `LENGTH` is bytes.
- Using `UPPER`/`LOWER` for case-insensitive matching on non-English names.
- Cleaning with a regex in SQL that does not exist in SQLite.


### Q34 ⭐ 🔴 Parse key=value text and log lines: logs(raw_line) with '2024-03-05 12:01:33 ERROR user=42 action=login ip=10.0.0.7', some lines missing user, some with extra spaces and a NULL line. Extract the level, the user id and the action with SUBSTR and INSTR (find 'user=', read to the next space or end of line), count lines per level and distinct users with errors, and list lines the parser could not read instead of dropping them silently. Then generalise: split a key=value;key=value attribute text into (key, value) rows with a recursive CTE (reference Part 9 Q1 for recursion mechanics) and pivot them to columns with MAX(CASE). Add the pandas str.extract with named groups, str.split and explode, and pivot version, and assert the pandas result equals the SQL result.
**Asked at:** SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** I normalise spaces first, then read each field with `SUBSTR` and `INSTR` (find the key, read to the next space, or to the end by appending a space), classify every line as ok, null, unreadable or bad user so nothing is dropped silently, and for key=value text I split with a recursive CTE and pivot with `MAX(CASE ...)`.

**Schema and sample data:**
```sql
CREATE TABLE logs(id INTEGER PRIMARY KEY, raw_line TEXT);
INSERT INTO logs VALUES
 (1,'2024-03-05 12:01:33 ERROR user=42 action=login ip=10.0.0.7'),
 (2,'2024-03-05 12:02:10 INFO user=7 action=view ip=10.0.0.8'),
 (3,'2024-03-05 12:03:00 ERROR action=login ip=10.0.0.9'),
 (4,'2024-03-05  12:04:05   ERROR  user=42   action=pay'),
 (5,NULL),
 (6,'2024-03-05 12:05:00 WARN user=9'),
 (7,'garbage line'),
 (8,'2024-03-05 12:06:00 ERROR user=abc action=x');
CREATE TABLE attrs(id INTEGER PRIMARY KEY, txt TEXT);
INSERT INTO attrs VALUES (1,'user=42;action=login;ip=10.0.0.7'),(2,'user=7;action=view'),
                         (3,'action=pay;note=a=b;'),(4,NULL),(5,'');
```

**SQL answer:** `parse_sql` in the Code block (CTEs `norm`, `p1`, `p2`, final SELECT with a `status` CASE), then the counts per level and distinct error users on the temp table `parsed`. For attributes: `kv_sql` (recursive CTE `split` peels one `key=value` piece off the front each step, `kv` cuts at the first `=`) and `wide_sql` (`LEFT JOIN` back to `attrs`, `MAX(CASE WHEN k = 'user' THEN v END)` and so on).

**pandas answer:** `raw.str.extract(r"^(?P<ts>...)\s+(?P<level>[A-Z]+)\b")`, `raw.str.extract(r"\buser=(?P<user_txt>\S*)")` and the same for `action`, then `np.select` for `status`. For key=value: `str.split(";")`, `explode`, `str.split("=", n=1, expand=True)`, then `pivot(index="id", columns="k", values="v")` reindexed to all ids.

**Example:** Line 1 is clean: level ERROR, user 42, action login. Line 3 has no `user=`: `instr` returns 0, so `user_rest` is NULL, the user stays NULL, the line is still 'ok'. Line 4 has runs of spaces; the three `replace('  ',' ')` passes squeeze it back to a single-spaced line, so it parses like line 1. Line 5 is NULL, which becomes 'null line'. Line 7 fails the timestamp `GLOB`, so it is 'unreadable' and has no level. Line 8 has `user=abc`, not digits, so it is 'bad user' (still counted under its level). Counts by level over ok and bad-user lines: ERROR 4 (lines 1, 3, 4, 8), INFO 1, WARN 1. Distinct users with an ERROR line among ok lines: only user 42 (lines 1 and 4) because line 3 has no user and line 8's user is bad. Eight rows in, eight rows out.
For the attributes: line 3's `note=a=b` splits at the first `=` into key `note`, value `a=b`; the trailing `;` leaves an empty piece which is dropped; rows with a NULL or empty text produce no pairs but the `LEFT JOIN` keeps their ids with all-NULL columns.

**Code:** run with `python3 -I`; the two results are compared after the stated sort, then asserted.
```python
# Parse log lines and key=value text with SUBSTR/INSTR, a recursive CTE, then the pandas version.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE logs(id INTEGER PRIMARY KEY, raw_line TEXT);
INSERT INTO logs VALUES
 (1,'2024-03-05 12:01:33 ERROR user=42 action=login ip=10.0.0.7'),
 (2,'2024-03-05 12:02:10 INFO user=7 action=view ip=10.0.0.8'),
 (3,'2024-03-05 12:03:00 ERROR action=login ip=10.0.0.9'),
 (4,'2024-03-05  12:04:05   ERROR  user=42   action=pay'),
 (5,NULL),
 (6,'2024-03-05 12:05:00 WARN user=9'),
 (7,'garbage line'),
 (8,'2024-03-05 12:06:00 ERROR user=abc action=x');
""")

parse_sql = """
WITH norm AS (                      -- collapse runs of spaces (3 passes handle runs up to 8) and trim
  SELECT id, raw_line,
         trim(replace(replace(replace(raw_line,'  ',' '),'  ',' '),'  ',' ')) AS s
  FROM logs
), p1 AS (
  SELECT id, raw_line, s,
         CASE WHEN substr(s,1,19) GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
              THEN substr(s,21) END AS after_ts                       -- NULL when the prefix is not a timestamp
  FROM norm
), p2 AS (
  SELECT id, raw_line, s, after_ts,
         substr(after_ts, 1, instr(after_ts || ' ', ' ') - 1) AS level,
         CASE WHEN instr(s, ' user=') > 0 THEN substr(s, instr(s, ' user=') + 6) END AS user_rest,
         CASE WHEN instr(s, ' action=') > 0 THEN substr(s, instr(s, ' action=') + 8) END AS action_rest
  FROM p1
)
SELECT id,
       level,
       substr(user_rest, 1, instr(user_rest || ' ', ' ') - 1)       AS user_txt,
       substr(action_rest, 1, instr(action_rest || ' ', ' ') - 1)   AS action,
       CASE WHEN raw_line IS NULL THEN 'null line'
            WHEN after_ts IS NULL OR level NOT IN ('ERROR','WARN','INFO') THEN 'unreadable'
            WHEN user_rest IS NOT NULL AND (substr(user_rest, 1, instr(user_rest || ' ', ' ') - 1) = ''
                 OR substr(user_rest, 1, instr(user_rest || ' ', ' ') - 1) GLOB '*[^0-9]*') THEN 'bad user'
            ELSE 'ok' END AS status
FROM p2 ORDER BY id"""
sql_parsed = pd.read_sql(parse_sql, con)
print(sql_parsed.to_string(index=False))

con.execute("CREATE TEMP TABLE parsed AS " + parse_sql)
print(con.execute("SELECT level, COUNT(*) FROM parsed WHERE status IN ('ok','bad user') GROUP BY level ORDER BY level").fetchall())
print("distinct users with an ERROR line:", con.execute(
    "SELECT COUNT(DISTINCT user_txt) FROM parsed WHERE level='ERROR' AND status='ok' AND user_txt IS NOT NULL").fetchone()[0])
print("lines the parser could not read:", con.execute(
    "SELECT id, status FROM parsed WHERE status <> 'ok' ORDER BY id").fetchall())
print("rows in = rows out:", con.execute("SELECT (SELECT COUNT(*) FROM logs), (SELECT COUNT(*) FROM parsed)").fetchone())

# ---- pandas: extract with named groups
logs = pd.read_sql("SELECT * FROM logs", con)
raw = logs["raw_line"]
head = raw.str.extract(r"^(?P<ts>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(?P<level>[A-Z]+)\b")
user = raw.str.extract(r"\buser=(?P<user_txt>\S*)")
act = raw.str.extract(r"\baction=(?P<action>\S+)")
p = pd.concat([logs["id"], head["level"], user, act], axis=1)
p["level"] = p["level"].where(p["level"].isin(["ERROR", "WARN", "INFO"]))
ok = p["level"].notna()
bad_user = p["user_txt"].notna() & ~p["user_txt"].fillna("").str.fullmatch(r"\d+")
p["status"] = np.select([raw.isna(), ~ok, bad_user], ["null line", "unreadable", "bad user"], default="ok")
print(p.to_string(index=False))
a = sql_parsed.fillna("<NA>").astype(str).reset_index(drop=True)
b = p[["id", "level", "user_txt", "action", "status"]].fillna("<NA>").astype(str).reset_index(drop=True)
# SQL gives NULL level for the null line; the unreadable row 7 has level 'garbage' in SQL only if after_ts passed (it did not)
a["id"] = a["id"].astype(int); b["id"] = b["id"].astype(int)
pd.testing.assert_frame_equal(a, b)           # compared in id order

# ---- generalise: key=value;key=value text -> (key, value) rows -> columns
con.executescript("""
CREATE TABLE attrs(id INTEGER PRIMARY KEY, txt TEXT);
INSERT INTO attrs VALUES (1,'user=42;action=login;ip=10.0.0.7'),(2,'user=7;action=view'),
                         (3,'action=pay;note=a=b;'),(4,NULL),(5,'');
""")
kv_sql = """
WITH RECURSIVE split(id, key_val, rest) AS (
  SELECT id, NULL, txt || ';' FROM attrs WHERE txt IS NOT NULL          -- NULL txt produces no rows
  UNION ALL
  SELECT id, substr(rest, 1, instr(rest, ';') - 1), substr(rest, instr(rest, ';') + 1)
  FROM split WHERE rest <> ''
), kv AS (
  SELECT id, substr(key_val, 1, instr(key_val, '=') - 1) AS k, substr(key_val, instr(key_val, '=') + 1) AS v
  FROM split WHERE key_val IS NOT NULL AND instr(key_val, '=') > 0     -- empty pieces and pieces without '=' dropped
)
SELECT id, k, v FROM kv ORDER BY id, k"""
sql_kv = pd.read_sql(kv_sql, con)
print(sql_kv.to_string(index=False))
wide_sql = f"""
WITH RECURSIVE split(id, key_val, rest) AS (
  SELECT id, NULL, txt || ';' FROM attrs WHERE txt IS NOT NULL
  UNION ALL
  SELECT id, substr(rest, 1, instr(rest, ';') - 1), substr(rest, instr(rest, ';') + 1) FROM split WHERE rest <> ''
), kv AS (
  SELECT id, substr(key_val, 1, instr(key_val, '=') - 1) AS k, substr(key_val, instr(key_val, '=') + 1) AS v
  FROM split WHERE key_val IS NOT NULL AND instr(key_val, '=') > 0
)
SELECT a.id,
       MAX(CASE WHEN k = 'user'   THEN v END) AS user,
       MAX(CASE WHEN k = 'action' THEN v END) AS action,
       MAX(CASE WHEN k = 'ip'     THEN v END) AS ip,
       MAX(CASE WHEN k = 'note'   THEN v END) AS note
FROM attrs a LEFT JOIN kv ON kv.id = a.id
GROUP BY a.id ORDER BY a.id"""
sql_wide = pd.read_sql(wide_sql, con)
print(sql_wide.to_string(index=False))

at = pd.read_sql("SELECT * FROM attrs", con)
long = (at.assign(pair=at["txt"].str.split(";")).explode("pair")
          .dropna(subset=["pair"]))
long = long[long["pair"].str.contains("=", regex=False)]
long[["k", "v"]] = long["pair"].str.split("=", n=1, expand=True)
p_kv = long[["id", "k", "v"]].sort_values(["id", "k"]).reset_index(drop=True)
pd.testing.assert_frame_equal(p_kv, sql_kv.sort_values(["id", "k"]).reset_index(drop=True), check_dtype=False)
p_wide = (long.pivot(index="id", columns="k", values="v")
              .reindex(index=at["id"], columns=["user", "action", "ip", "note"]).reset_index().rename_axis(columns=None))
pd.testing.assert_frame_equal(p_wide.astype(object).where(p_wide.notna(), None),
                              sql_wide.astype(object).where(sql_wide.notna(), None), check_dtype=False)
print(p_wide.to_string(index=False))

# counting a substring: SQL length/replace trick versus str.count (regex, non-overlapping)
print("SQL count of 'aa' in 'aaa':", con.execute("SELECT (length('aaa') - length(replace('aaa','aa',''))) / length('aa')").fetchone()[0],
      "| pandas str.count:", pd.Series(["aaa"]).str.count("aa")[0],
      "| '=' per attrs line (pandas):", at["txt"].str.count("=").tolist())
con.close()
print("asserts passed")
```

**Output (my run):**
```text
 id level user_txt action     status
  1 ERROR       42  login         ok
  2  INFO        7   view         ok
  3 ERROR      NaN  login         ok
  4 ERROR       42    pay         ok
  5   NaN      NaN    NaN  null line
  6  WARN        9    NaN         ok
  7   NaN      NaN    NaN unreadable
  8 ERROR      abc      x   bad user
[('ERROR', 4), ('INFO', 1), ('WARN', 1)]
distinct users with an ERROR line: 1
lines the parser could not read: [(5, 'null line'), (7, 'unreadable'), (8, 'bad user')]
rows in = rows out: (8, 8)
 id level user_txt action     status
  1 ERROR       42  login         ok
  2  INFO        7   view         ok
  3 ERROR      NaN  login         ok
  4 ERROR       42    pay         ok
  5   NaN      NaN    NaN  null line
  6  WARN        9    NaN         ok
  7   NaN      NaN    NaN unreadable
  8 ERROR      abc      x   bad user
 id      k        v
  1 action    login
  1     ip 10.0.0.7
  1   user       42
  2 action     view
  2   user        7
  3 action      pay
  3   note      a=b
 id user action       ip note
  1   42  login 10.0.0.7  NaN
  2    7   view      NaN  NaN
  3  NaN    pay      NaN  a=b
  4  NaN    NaN      NaN  NaN
  5  NaN    NaN      NaN  NaN
 id user action       ip note
  1   42  login 10.0.0.7  NaN
  2    7   view      NaN  NaN
  3  NaN    pay      NaN  a=b
  4  NaN    NaN      NaN  NaN
  5  NaN    NaN      NaN  NaN
SQL count of 'aa' in 'aaa': 1 | pandas str.count: 1 | '=' per attrs line (pandas): [3.0, 2.0, 3.0, nan, 0.0]
asserts passed
```

**Edge cases:**
- Space runs: three `replace('  ',' ')` passes squeeze any run up to 8 spaces; longer runs need more passes (or a recursive collapse). SQLite has no regex replace.
- `instr(x || ' ', ' ')` is the trick for 'read to the next space or to the end': appending a space guarantees a hit.
- A NULL line stays in the result with status 'null line'; `WHERE` on it would silently drop it.
- A missing key gives `instr = 0`; always test it before `substr`, otherwise `substr(s, 0 + 6)` returns garbage from the wrong position.
- The recursive step needs `WHERE rest <> ''` as the stop; a NULL `txt` is excluded in the anchor.
- Values containing `=`: cut at the first `=` only (`instr` finds the first); `str.split("=", n=1)` does the same in pandas.
- Counting a key with the `length(s) - length(replace(s, k, ''))` trick counts non-overlapping hits like pandas `str.count`: both gave 1 for `'aa'` in `'aaa'`; `str.count` is a regex count, so a metacharacter key such as `.` needs escaping.
- pandas `read_sql` shows NULL as NaN; the comparison code fills missing with a marker before `assert_frame_equal`.

**Then explain:**
- **Do not trust one regex-like parse:** always report counts of unreadable and null lines, otherwise quality problems hide as lower totals.
- **`LENGTH`-based tricks:** fine for one key, fragile for many; the recursive CTE gives one row per pair.
- **Recursive CTE shape:** anchor (`txt || ';'`), recursive member (one piece out, rest in), stop when the rest is empty. Part 9 Q1 has the mechanics.
- **Dialects, not executed here:** PostgreSQL could use `regexp_match` or `split_part`/`string_to_table`, MySQL `SUBSTRING_INDEX`, BigQuery `REGEXP_EXTRACT` and `SPLIT`; I did not run any of them.
- **pandas side:** `str.extract` with named groups gives named columns; a missing match gives NaN. The `explode`/`split`/`pivot` chain is the same idea as the CTE.

**Follow-ups:**
- *How would you handle a user that appears twice in one line?* `MAX` would hide it; use `COUNT` per key to flag it.
- *What about quoted values with spaces?* Not parseable with a space delimiter; use a real parser in the application.
- *Why a LEFT JOIN in the pivot?* So ids with no pairs still appear.

**Common mistakes:**
- Dropping unparseable lines in a `WHERE` instead of reporting them.
- Using `substr` without checking `instr > 0`.
- Splitting `note=a=b` at the last `=` or with a plain split (pandas `split("=")` without `n=1`).
- Forgetting the trailing delimiter, losing the last pair.
- Counting `COUNT(user)` as lines with users when a bad value is present.


### Q35 ⭐ 🔴 Find duplicates ignoring case and spaces: customers(customer_id, name, email, city) with near-duplicates such as 'Asha Rao ' and 'asha  rao', emails 'A@X.com' and ' a@x.com', and NBSP characters. Build a normalised key (LOWER, TRIM, collapse repeated spaces, REPLACE CHAR(160)), list duplicate groups with the ids involved, pick the row to keep (smallest id), and show a delete or flag statement. Explain false positives (two real people with the same name and city) and the review step before deletion. Cross-reference Part 4 Q10 (finding exact duplicates) and Part 3 Q25 (deleting duplicates) and do not repeat them. Add the pandas str.casefold, str.strip, duplicated(keep=False) and drop_duplicates(subset=...) version and assert the same group sizes.
**Asked at:** Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds; SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds
**Say this first (1 line):** I build a normalised key (NBSP and tab to space, collapse spaces, trim, lower), group on it to list the ids per duplicate group, keep the smallest id, flag the others instead of deleting, and review groups where other fields disagree before anything is removed; pandas does the same with `casefold`, `strip` and `duplicated`.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT);
-- inserted from Python so the NBSP (U+00A0) in id 3 is exact
-- 1 ('Asha Rao ', 'a@x.com', 'Pune')       2 ('asha  rao', ' a@x.com', 'pune')
-- 3 ('Asha<NBSP>Rao', 'A@X.com', 'Pune ')  4 ('Ben Cruz', 'ben@y.com', 'Delhi')
-- 5 ('Ben Cruz', 'ben2@y.com', 'Mumbai')   6 ('Chitra Nair', 'c@z.com', 'Goa')
-- 7 ('chitra nair', NULL, 'GOA')           8 ('Raj Shah', 'raj1@q.com', 'Pune')
-- 9 ('Raj Shah', 'raj2@q.com', 'Pune')     10 ('Dev Rao', NULL, 'Pune')
```

**SQL answer:** `groups_sql` in the Code block (CTE `k` with `name_key`, `city_key`, `email_key`, then `GROUP BY name_key, city_key HAVING COUNT(*) > 1` with `group_concat(customer_id, ',' ORDER BY customer_id)`, `MIN(customer_id)` as keeper, `COUNT(DISTINCT email_key)` and the NULL-email count) and `flag_sql` (an `UPDATE` that sets `dup_of` to the group's smallest id for every other row).

**pandas answer:** `norm()` (replace NBSP, collapse `\s+`, `strip`, `casefold`), `df.duplicated(subset=[...], keep=False)` to select group members, a `groupby` for sizes and ids, and `sort_values("customer_id").drop_duplicates(subset=[...], keep="first")` for the survivors.

**Example:** Keys: ids 1, 2, 3 all normalise to ('asha rao', 'pune') (trailing space, double space, NBSP and case removed); group size 3, keep 1, one distinct email (`a@x.com` after trim and lower), so these are safe to merge. Ids 6 and 7 become ('chitra nair', 'goa'), keep 6, one email is NULL, so it is probably the same person but check. Ids 8 and 9 are ('raj shah', 'pune') with two different emails: same name and city, different people possibly, so `distinct_emails` = 2 flags them for review. Ben Cruz (4, 5) differs by city and is not a group. Dev Rao (10) is alone. Flagged ids: 2, 3, 7, 9 (point to 1, 1, 6, 8); pandas drops the same four.

**Code:** run with `python3 -I`; the two results are compared after the stated sort, then asserted.
```python
# Duplicates that differ only by case, spaces and NBSP: normalised key, groups, keeper, flag.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT)")
con.executemany("INSERT INTO customers VALUES (?,?,?,?)", [
    (1, "Asha Rao ", "a@x.com", "Pune"),
    (2, "asha  rao", " a@x.com", "pune"),
    (3, "Asha Rao", "A@X.com", "Pune "),
    (4, "Ben Cruz", "ben@y.com", "Delhi"),
    (5, "Ben Cruz", "ben2@y.com", "Mumbai"),      # same name, different city: not a duplicate
    (6, "Chitra Nair", "c@z.com", "Goa"),
    (7, "chitra nair", None, "GOA"),              # duplicate by name and city, email missing
    (8, "Raj Shah", "raj1@q.com", "Pune"),        # two real people with the same name and city
    (9, "Raj Shah", "raj2@q.com", "Pune"),
    (10, "Dev Rao", None, "Pune"),
])

# normalised key as a reusable CTE: NBSP and tab to space, collapse spaces, trim, ASCII lower
NORM = lambda col: (f"lower(trim(replace(replace(replace(replace(replace({col}, char(160), ' '), char(9), ' '),"
                    f" '  ', ' '), '  ', ' '), '  ', ' ')))")
groups_sql = f"""
WITH k AS (
  SELECT customer_id, name, email, city,
         {NORM('name')} AS name_key, {NORM('city')} AS city_key,
         lower(trim(replace(email, char(160), ''))) AS email_key
  FROM customers
)
SELECT name_key, city_key,
       COUNT(*)                                              AS n,
       group_concat(customer_id, ',' ORDER BY customer_id)   AS ids,
       MIN(customer_id)                                      AS keep_id,
       COUNT(DISTINCT email_key)                             AS distinct_emails,
       SUM(email_key IS NULL)                                AS null_emails
FROM k GROUP BY name_key, city_key HAVING COUNT(*) > 1
ORDER BY MIN(customer_id)"""
sql_groups = pd.read_sql(groups_sql, con)
print(sql_groups.to_string(index=False))

# flag instead of delete: dup_of points at the smallest id of the group
con.execute("ALTER TABLE customers ADD COLUMN dup_of INTEGER")
flag_sql = f"""
UPDATE customers SET dup_of = (
  SELECT MIN(c2.customer_id) FROM customers c2
  WHERE {NORM('c2.name')} = {NORM('customers.name')} AND {NORM('c2.city')} = {NORM('customers.city')})
WHERE customer_id <> (
  SELECT MIN(c2.customer_id) FROM customers c2
  WHERE {NORM('c2.name')} = {NORM('customers.name')} AND {NORM('c2.city')} = {NORM('customers.city')})"""
con.execute(flag_sql)
print("flagged:", con.execute("SELECT customer_id, dup_of FROM customers WHERE dup_of IS NOT NULL ORDER BY 1").fetchall())
# review step before any delete: show the groups where emails disagree
print("needs review (two different non-null emails):",
      [tuple(r) for r in sql_groups.loc[sql_groups["distinct_emails"] > 1, ["name_key", "city_key", "ids"]].itertuples(index=False)])
print("rows that a DELETE WHERE dup_of IS NOT NULL would remove:", con.execute("SELECT COUNT(*) FROM customers WHERE dup_of IS NOT NULL").fetchone()[0])

# ---- pandas
df = pd.read_sql("SELECT customer_id, name, email, city FROM customers", con)
def norm(s):
    return (s.str.replace(" ", " ", regex=False).str.replace(r"\s+", " ", regex=True)
             .str.strip().str.casefold())
df["name_key"], df["city_key"] = norm(df["name"]), norm(df["city"])
df["email_key"] = df["email"].str.replace(" ", "", regex=False).str.strip().str.casefold()
dup_mask = df.duplicated(subset=["name_key", "city_key"], keep=False)
p_groups = (df[dup_mask].groupby(["name_key", "city_key"])
              .agg(n=("customer_id", "size"), ids=("customer_id", lambda s: ",".join(map(str, sorted(s)))),
                   keep_id=("customer_id", "min"), distinct_emails=("email_key", "nunique"),
                   null_emails=("email_key", lambda s: int(s.isna().sum())))
              .reset_index().sort_values("keep_id").reset_index(drop=True))
print(p_groups.to_string(index=False))
pd.testing.assert_frame_equal(p_groups, sql_groups, check_dtype=False)     # compared in keep_id order

kept = df.sort_values("customer_id").drop_duplicates(subset=["name_key", "city_key"], keep="first")
removed = sorted(set(df["customer_id"]) - set(kept["customer_id"]))
assert removed == sorted(r[0] for r in con.execute("SELECT customer_id FROM customers WHERE dup_of IS NOT NULL"))
print("pandas would drop ids:", removed, "| duplicated(keep=False) rows:", int(dup_mask.sum()))

# why the careless key fails
naive = con.execute("SELECT COUNT(*) FROM (SELECT name, city FROM customers GROUP BY name, city HAVING COUNT(*) > 1)").fetchone()[0]
print("exact GROUP BY name, city finds", naive, "duplicate groups; the normalised key finds", len(sql_groups))
print("ASCII-only warning:", con.execute("SELECT lower('RENÉ') = lower('rené')").fetchone()[0], "(0: É not folded by SQLite lower)")
con.close()
print("asserts passed")
```

**Output (my run):**
```text
   name_key city_key  n   ids  keep_id  distinct_emails  null_emails
   asha rao     pune  3 1,2,3        1                1            0
chitra nair      goa  2   6,7        6                1            1
   raj shah     pune  2   8,9        8                2            0
flagged: [(2, 1), (3, 1), (7, 6), (9, 8)]
needs review (two different non-null emails): [('raj shah', 'pune', '8,9')]
rows that a DELETE WHERE dup_of IS NOT NULL would remove: 4
   name_key city_key  n   ids  keep_id  distinct_emails  null_emails
   asha rao     pune  3 1,2,3        1                1            0
chitra nair      goa  2   6,7        6                1            1
   raj shah     pune  2   8,9        8                2            0
pandas would drop ids: [2, 3, 7, 9] | duplicated(keep=False) rows: 7
exact GROUP BY name, city finds 1 duplicate groups; the normalised key finds 3
ASCII-only warning: 0 (0: É not folded by SQLite lower)
asserts passed
```

**Edge cases:**
- A plain `GROUP BY name, city` finds only 1 duplicate group (ids 8 and 9, the false positive!) and misses the real ones; the normalised key finds 3 groups.
- `lower` is ASCII-only: `lower('RENÉ') = lower('rené')` is 0, so accented duplicates need application-side `casefold` and NFC (see Q33).
- NULL email: `lower(trim(NULL))` is NULL, ignored by `COUNT(DISTINCT)`, so I count NULL emails separately; a NULL is neither a match nor a conflict.
- Whether to key on name + city or on email is a business rule. Email-only keys miss people with two emails; name-only keys merge strangers.
- Ties for the keeper: smallest id is deterministic; 'most complete row' or 'most recent' are other rules that need a window function (Part 3 Q25 covers the delete itself).
- The three `replace('  ',' ')` passes squeeze runs of up to 8 spaces only.

**Then explain:**
- **Normalised key:** every step removes one kind of noise: `char(160)` to space, collapse spaces, `trim`, `lower`.
- **False positives:** two real people can share a name and city. The review rule here is 'different non-NULL emails means look at it by hand'.
- **Flag before delete:** I add `dup_of`, check the counts and a sample, then `DELETE ... WHERE dup_of IS NOT NULL` in a transaction with a backup. Exact duplicates are Part 4 Q10 and the delete mechanics are Part 3 Q25; I do not repeat them.
- **pandas:** `duplicated(keep=False)` marks every member (7 rows here); `drop_duplicates(keep="first")` after sorting by id keeps the smallest id, like `MIN(customer_id)`.
- Dialect note: `lower`/collation rules differ in other engines; not executed here.

**Follow-ups:**
- *How would you merge, not just delete?* Re-point foreign keys to the keeper first, then delete.
- *What about 'Asha R.'?* That is fuzzy matching (edit distance, phonetics), beyond a normalised key.
- *Should the key be a column?* Yes, a stored normalised column with an index makes the check cheap.

**Common mistakes:**
- Deleting everything in a group (`HAVING COUNT(*) > 1` is not a delete rule).
- Forgetting NBSP, tab or case and finding nothing.
- Merging two real people with the same name.
- Comparing emails case-sensitively.
- Using `duplicated()` default `keep='first'` when you wanted the whole group listed.


### Q36 ⭐ 🔴 NULL-aware data-quality audit report: customers(customer_id, name, email, phone, city, signup_date) with NULLs, empty strings, whitespace-only strings and 'N/A' or 'NULL' text. Return one row per column with total rows, NULL count, empty-string count, whitespace-only count, placeholder-text count, distinct count, and percentage missing, generated with UNION ALL (one SELECT per column) or a Python loop that builds the SQL from PRAGMA table_info. Explain why COUNT(*) - COUNT(col) misses blanks, how to count 'effectively missing' in one expression, and how to flag duplicate keys. Add the pandas version using isna, str.strip and eq plus melt of the summary, assert the audit equals the SQL one, and say how you would automate it (concept level only; monitoring belongs to Book 4).
**Asked at:** SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** `COUNT(*) - COUNT(col)` counts only real NULLs, so I generate one SELECT per column from `PRAGMA table_info` that counts NULL, empty, whitespace-only and placeholder text separately and also one 'effectively missing' number, UNION ALL them into one row per column, and check the same audit in pandas.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER, name TEXT, email TEXT, phone TEXT, city TEXT, signup_date TEXT);
INSERT INTO customers VALUES
 (1,'Asha','asha@x.com','98100 00001','Pune','2024-01-05'),
 (2,'Ben','ben@y.com','','Delhi','2024-01-09'),
 (3,'Chitra',NULL,'N/A','Pune','NULL'),
 (4,'Dev','dev@x.com','   ','Goa',''),
 (5,'  ','DEV@x.com',NULL,'pune','2024-02-01'),
 (6,NULL,'n/a','98100 00006','Delhi',NULL),
 (7,'Gita','gita@z.com','98100 00007','NULL','2024-02-11'),
 (8,'Hari','asha@x.com','98100 00008','','2024-02-20');
```

**SQL answer:** `one_col(c)` builds one SELECT for a column (the Code block prints the one for `phone`); the column list comes from `PRAGMA table_info(customers)` and each name is quoted. `audit_sql` joins them with `UNION ALL`. Placeholders are `N/A, NA, NULL, NONE, -` compared as `upper(trim(col))`.

**pandas answer:** A loop over columns: `isna().sum()`, `(s == "").sum()`, `((s.str.strip() == "") & (s != "")).sum()`, `s.str.strip().str.upper().isin(PLACEHOLDERS).sum()`, `s.nunique()`, then `pd.DataFrame(rows)` and `melt(id_vars="column_name")` to the long (metric, value) shape.

**Example:** Phone has 8 rows. NULL: row 5 (1). Empty string: row 2 (1). Whitespace-only: row 4, three spaces (1; counted separately from empty because `''` is excluded from that test). Placeholder: row 3, 'N/A' (1). Effectively missing: 1 + 1 + 1 + 1 = 4, so 50.0 per cent missing, while `COUNT(*) - COUNT(phone)` reports only 1. Name: NULL 1 (row 6), whitespace-only 1 (row 5, two spaces), effectively missing 2, so 25.0. signup_date: NULL row 6, empty row 4, 'NULL' text row 3: three problems of three different kinds = 37.5 per cent. Duplicate keys: no repeated `customer_id`; emails repeat after lower and trim (ids 1 and 8, ids 4 and 5), and the text 'n/a' email (row 6) is excluded before grouping.

**Code:** run with `python3 -I`; the two results are compared after the stated sort, then asserted.
```python
# NULL-aware data-quality audit: one row per column, built from PRAGMA table_info.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER, name TEXT, email TEXT, phone TEXT, city TEXT, signup_date TEXT);
INSERT INTO customers VALUES
 (1,'Asha','asha@x.com','98100 00001','Pune','2024-01-05'),
 (2,'Ben','ben@y.com','','Delhi','2024-01-09'),
 (3,'Chitra',NULL,'N/A','Pune','NULL'),
 (4,'Dev','dev@x.com','   ','Goa',''),
 (5,'  ','DEV@x.com',NULL,'pune','2024-02-01'),
 (6,NULL,'n/a','98100 00006','Delhi',NULL),
 (7,'Gita','gita@z.com','98100 00007','NULL','2024-02-11'),
 (8,'Hari','asha@x.com','98100 00008','','2024-02-20');
""")
PLACEHOLDERS = ("N/A", "NA", "NULL", "NONE", "-")
ph = ",".join("'" + p + "'" for p in PLACEHOLDERS)

cols = [r[1] for r in con.execute("PRAGMA table_info(customers)")]       # column names from the catalog
def one_col(c):
    q = '"' + c + '"'                                                    # quoted identifier
    return f"""SELECT '{c}' AS column_name,
  COUNT(*) AS total_rows,
  COUNT(*) - COUNT({q}) AS null_count,
  SUM({q} = '') AS empty_count,
  SUM({q} IS NOT NULL AND {q} <> '' AND trim({q}) = '') AS whitespace_only,
  SUM({q} IS NOT NULL AND upper(trim({q})) IN ({ph})) AS placeholder_count,
  COUNT(DISTINCT {q}) AS distinct_count,
  SUM({q} IS NULL OR trim({q}) = '' OR upper(trim({q})) IN ({ph})) AS effectively_missing,
  round(100.0 * SUM({q} IS NULL OR trim({q}) = '' OR upper(trim({q})) IN ({ph})) / COUNT(*), 1) AS pct_missing
FROM customers"""
audit_sql = "\nUNION ALL\n".join(one_col(c) for c in cols)
print(one_col("phone"))
sql_audit = pd.read_sql(audit_sql, con)
print(sql_audit.to_string(index=False))

# COUNT(*) - COUNT(col) versus effectively missing
print("phone: COUNT(*)-COUNT(phone) =", con.execute("SELECT COUNT(*)-COUNT(phone) FROM customers").fetchone()[0],
      "| effectively missing =", int(sql_audit.loc[sql_audit.column_name == "phone", "effectively_missing"].iloc[0]))

# duplicate keys: customer_id exact, email after normalisation, ignoring missing values
print("duplicate customer_id:", con.execute("SELECT customer_id FROM customers GROUP BY customer_id HAVING COUNT(*) > 1").fetchall())
print("duplicate emails (lower+trim, missing excluded):", con.execute("""
  SELECT lower(trim(email)) AS e, group_concat(customer_id, ',' ORDER BY customer_id)
  FROM customers WHERE email IS NOT NULL AND trim(email) <> '' AND upper(trim(email)) NOT IN ('N/A','NA','NULL','NONE','-')
  GROUP BY lower(trim(email)) HAVING COUNT(*) > 1""").fetchall())

# ---- pandas: same audit
df = pd.read_sql("SELECT * FROM customers", con)
rows = []
for c in df.columns:
    s = df[c]
    if pd.api.types.is_numeric_dtype(s):
        empty = ws = ph_n = 0
        miss = int(s.isna().sum())
    else:
        stripped = s.str.strip()
        empty = int((s == "").sum())
        ws = int(((stripped == "") & (s != "")).sum())
        ph_n = int(stripped.str.upper().isin(PLACEHOLDERS).sum())
        miss = int((s.isna() | (stripped == "") | stripped.str.upper().isin(PLACEHOLDERS)).sum())
    rows.append({"column_name": c, "total_rows": len(s), "null_count": int(s.isna().sum()), "empty_count": empty,
                 "whitespace_only": ws, "placeholder_count": ph_n, "distinct_count": int(s.nunique()),
                 "effectively_missing": miss, "pct_missing": round(100.0 * miss / len(s), 1)})
p_audit = pd.DataFrame(rows)
pd.testing.assert_frame_equal(p_audit, sql_audit, check_dtype=False)     # compared in column order
print("pandas audit equals SQL audit")
long = p_audit.melt(id_vars="column_name", var_name="metric", value_name="value")
print(long[long["metric"].isin(["effectively_missing", "pct_missing"])].to_string(index=False))

# honest differences
print("NBSP-only phone: SQL trim =", con.execute("SELECT length(trim(char(160)))").fetchone()[0], "(not whitespace), pandas strip ->",
      repr(pd.Series([" "]).str.strip()[0]))
print("printf('%.0f') of 12.5, 2.5, 2.9, 3.5, 100.6:", con.execute("SELECT printf('%.0f',12.5), printf('%.0f',2.5), printf('%.0f',2.9), printf('%.0f',3.5), printf('%.0f',100.6)").fetchone())
print("round() of the same:", con.execute("SELECT round(12.5), round(2.5), round(2.9), round(3.5), round(100.6)").fetchone(),
      "| printf('%.0f', round(x)):", con.execute("SELECT printf('%.0f',round(2.9)), printf('%.0f',round(100.6))").fetchone(),
      "| Python '%.0f' % 2.5, 3.5, 2.9:", ["%.0f" % 2.5, "%.0f" % 3.5, "%.0f" % 2.9])
con.close()
print("asserts passed")
```

**Output (my run):**
```text
SELECT 'phone' AS column_name,
  COUNT(*) AS total_rows,
  COUNT(*) - COUNT("phone") AS null_count,
  SUM("phone" = '') AS empty_count,
  SUM("phone" IS NOT NULL AND "phone" <> '' AND trim("phone") = '') AS whitespace_only,
  SUM("phone" IS NOT NULL AND upper(trim("phone")) IN ('N/A','NA','NULL','NONE','-')) AS placeholder_count,
  COUNT(DISTINCT "phone") AS distinct_count,
  SUM("phone" IS NULL OR trim("phone") = '' OR upper(trim("phone")) IN ('N/A','NA','NULL','NONE','-')) AS effectively_missing,
  round(100.0 * SUM("phone" IS NULL OR trim("phone") = '' OR upper(trim("phone")) IN ('N/A','NA','NULL','NONE','-')) / COUNT(*), 1) AS pct_missing
FROM customers
column_name  total_rows  null_count  empty_count  whitespace_only  placeholder_count  distinct_count  effectively_missing  pct_missing
customer_id           8           0            0                0                  0               8                    0          0.0
       name           8           1            0                1                  0               7                    2         25.0
      email           8           1            0                0                  1               6                    2         25.0
      phone           8           1            1                1                  1               7                    4         50.0
       city           8           0            1                0                  1               6                    2         25.0
signup_date           8           1            1                0                  1               7                    3         37.5
phone: COUNT(*)-COUNT(phone) = 1 | effectively missing = 4
duplicate customer_id: []
duplicate emails (lower+trim, missing excluded): [('asha@x.com', '1,8'), ('dev@x.com', '4,5')]
pandas audit equals SQL audit
column_name              metric  value
customer_id effectively_missing    0.0
       name effectively_missing    2.0
      email effectively_missing    2.0
      phone effectively_missing    4.0
       city effectively_missing    2.0
signup_date effectively_missing    3.0
customer_id         pct_missing    0.0
       name         pct_missing   25.0
      email         pct_missing   25.0
      phone         pct_missing   50.0
       city         pct_missing   25.0
signup_date         pct_missing   37.5
NBSP-only phone: SQL trim = 1 (not whitespace), pandas strip -> ''
printf('%.0f') of 12.5, 2.5, 2.9, 3.5, 100.6: ('12', '2', '2', '3', '100')
round() of the same: (13.0, 3.0, 3.0, 4.0, 101.0) | printf('%.0f', round(x)): ('3', '101') | Python '%.0f' % 2.5, 3.5, 2.9: ['2', '4', '3']
asserts passed
```

**Edge cases:**
- `COUNT(DISTINCT col)` skips NULL but counts `''`, `'N/A'` and `'NULL'` as values (phone shows 7 distinct values: four real numbers, the empty string, the three-space string and 'N/A'). Distinct count is therefore not a quality measure on its own.
- Placeholder text is a business list. The word 'NULL' in a column is a string, not a NULL.
- NBSP-only values: `trim(char(160))` still has length 1 (not whitespace for SQL), while pandas `str.strip` turns it into `''`. I kept NBSP out of the sample so both sides agree; with NBSP data the two audits would differ (shown in the output).
- Numeric columns: `trim(customer_id)` converts to text, so the checks run; pandas skips the string tests for numeric dtypes (they are 0).
- `SUM(cond)` is NULL if there are no rows; here there always are rows. Use `TOTAL()` or `COALESCE` for empty tables.
- Rounding: `round(x, 1)` is fine; do not use `printf('%.0f', x)` for whole-number percentages: in this build it truncated (`printf('%.0f', 2.9)` gave `2`, `12.5` gave `12`), while `round()` and `printf('%.0f', round(x))` gave 3 and 13. Python's `'%.0f' % 2.5` gave `2` (half to even) and `3.5` gave `4`.

**Then explain:**
- **Why `COUNT(*) - COUNT(col)` misses blanks:** `COUNT(col)` counts non-NULL values, and `''`, whitespace and `'N/A'` are non-NULL. Part 1 Q4 and Q6 cover the basics.
- **One expression for 'effectively missing':** `col IS NULL OR trim(col) = '' OR upper(trim(col)) IN (...)`. Put the NULL test first; `trim(NULL) = ''` is UNKNOWN, and `TRUE OR UNKNOWN` is TRUE, so the first test settles the NULL case.
- **Percentage:** `100.0 * missing / COUNT(*)`; the `100.0` forces decimal division (integer division would give 0 or 1).
- **Duplicate keys:** `GROUP BY normalised_key HAVING COUNT(*) > 1` after excluding missing values (a NULL key is not a duplicate of another NULL).
- **Preventing it:** a `CHECK (trim(email) <> '')` constraint or a STRICT table with proper types stops new blanks at the door; a NULL still passes a CHECK (UNKNOWN is accepted), so add `NOT NULL` if needed.
- **Automation (concept only):** run the same generated query on a schedule, store the results by date, and alert on a threshold change. Monitoring design belongs to Book 4.
- Dialect note: PostgreSQL, MySQL and others have the same logic with their own catalog views instead of `PRAGMA table_info`; not executed here.

**Follow-ups:**
- *How do you audit 200 columns?* Generate the SQL in a loop from the catalog, as here.
- *Can you do it in one scan?* Yes, one SELECT with all the SUM expressions; the UNION ALL version scans once per column, which is fine for small tables.
- *What is the difference between NULL and empty for a join key?* Part 2 Q6.

**Common mistakes:**
- Reporting `COUNT(*) - COUNT(col)` as the missing rate.
- Counting `''` as whitespace-only (or the reverse) and double counting.
- Dividing integers and getting 0 per cent.
- Treating the string 'NULL' as NULL.
- Trusting `TRIM` to catch NBSP.


### Q37 ⭐ 🔴 Palindrome and anagram style puzzles in SQL: words(word) with 'madam', 'Level', 'abc', 'A man a plan', NULL and ''. Check for palindromes ignoring case and spaces with a recursive CTE (SQLite has no REVERSE: build the reversed string one character at a time, reference Part 9 Q1 for recursion mechanics), then find anagram groups by building a sorted-character signature per word (split to characters with a recursive CTE, sort, group_concat in order) and grouping on it. Explain why these are brain teasers and give the shorter pandas answer (s == s[::-1], ''.join(sorted(w))) and assert both give the same groups. State that PostgreSQL, MySQL and SQL Server have REVERSE (hedged, not executed) and say what an interviewer is really testing.
**Asked at:** Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** These are brain teasers: SQLite has no `REVERSE`, so I rebuild the string one character at a time with a recursive CTE and compare, and for anagrams I split into characters, sort them with `group_concat(c, '' ORDER BY c)` and group on that signature; in pandas it is one line each.

**Schema and sample data:**
```sql
CREATE TABLE words(word TEXT);
INSERT INTO words VALUES ('madam'),('Level'),('abc'),('A man a plan'),(NULL),(''),
  ('Taco cat'),('listen'),('Silent'),('tinsel'),('cab'),('bca');
```

**SQL answer:** `pal_sql` (CTE `w` normalises with `lower(replace(word,' ',''))`, `rev` prepends one character per step: `substr(norm, i+1, 1) || r`, the last step has `i = length(norm)`) and `anag_sql` (CTE `ch` splits into characters, `sig` builds `group_concat(c, '' ORDER BY c)`, the final query groups by signature). Part 9 Q1 has recursion mechanics.

**pandas answer:** `norm = df["word"].str.lower().str.replace(" ", "", regex=False)`; `norm.str[::-1]` reverses; `norm == reversed` tests; `"".join(sorted(w))` builds the signature and `groupby("signature")` groups.

**Example:** 'madam' reversed is 'madam': palindrome. 'Level' normalises to 'level' and matches its reverse: palindrome (case ignored). 'Taco cat' becomes 'tacocat': palindrome. 'A man a plan' becomes 'amanaplan', reverse 'nalpanama': not a palindrome. 'abc' is not. '' (empty) reverses to '' so it counts as a palindrome by this rule, and NULL is excluded by `WHERE word IS NOT NULL`. Anagrams: 'abc', 'bca', 'cab' share the sorted signature 'abc'; 'Silent', 'listen', 'tinsel' share 'eilnst' after lower-casing. 'madam' and the others are alone and filtered by `HAVING COUNT(*) > 1`.

**Code:** run with `python3 -I`; the two results are compared after the stated sort, then asserted.
```python
# Palindromes and anagram groups in SQLite (no REVERSE) versus pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE words(word TEXT);
INSERT INTO words VALUES ('madam'),('Level'),('abc'),('A man a plan'),(NULL),(''),
  ('Taco cat'),('listen'),('Silent'),('tinsel'),('cab'),('bca');
""")

pal_sql = """
WITH RECURSIVE w AS (
  SELECT DISTINCT word, lower(replace(word, ' ', '')) AS norm FROM words WHERE word IS NOT NULL
), rev(word, norm, i, r) AS (
  SELECT word, norm, 0, '' FROM w
  UNION ALL
  SELECT word, norm, i + 1, substr(norm, i + 1, 1) || r      -- prepend the next character
  FROM rev WHERE i < length(norm)
)
SELECT word, norm, r AS reversed, (norm = r) AS is_palindrome
FROM rev WHERE i = length(norm) ORDER BY word"""
sql_pal = pd.read_sql(pal_sql, con)
print(sql_pal.to_string(index=False))

anag_sql = """
WITH RECURSIVE w AS (
  SELECT DISTINCT word, lower(replace(word, ' ', '')) AS norm FROM words WHERE word IS NOT NULL
), ch(word, norm, pos, c) AS (
  SELECT word, norm, 1, substr(norm, 1, 1) FROM w WHERE norm <> ''
  UNION ALL
  SELECT word, norm, pos + 1, substr(norm, pos + 1, 1) FROM ch WHERE pos < length(norm)
), sig AS (
  SELECT word, group_concat(c, '' ORDER BY c) AS signature FROM ch GROUP BY word
)
SELECT signature, COUNT(*) AS n, group_concat(word, ',' ORDER BY word) AS members
FROM sig GROUP BY signature HAVING COUNT(*) > 1 ORDER BY signature"""
sql_anag = pd.read_sql(anag_sql, con)
print(sql_anag.to_string(index=False))

# group_concat(DISTINCT x, sep) is rejected: DISTINCT works only with a single argument
try:
    con.execute("SELECT group_concat(DISTINCT word, '|') FROM words").fetchall()
except sqlite3.Error as e:
    print("group_concat(DISTINCT word, '|') ->", e)
print("group_concat(DISTINCT word) works, default separator ',':", con.execute("SELECT group_concat(DISTINCT word) FROM (SELECT word FROM words WHERE word IN ('abc','abc','cab') ORDER BY word)").fetchone()[0])
print("string_agg with ORDER BY works:", con.execute("SELECT string_agg(word, '|' ORDER BY word) FROM words WHERE word LIKE '%a%'").fetchone()[0])
print("reverse:", end=" ")
try:
    con.execute("SELECT reverse('abc')")
except sqlite3.Error as e:
    print(e)

# ---- pandas
df = pd.read_sql("SELECT word FROM words", con)
norm = df["word"].str.lower().str.replace(" ", "", regex=False)
p_pal = pd.DataFrame({"word": df["word"], "norm": norm})
p_pal = p_pal.dropna().drop_duplicates()
p_pal["reversed"] = p_pal["norm"].str[::-1]
p_pal["is_palindrome"] = (p_pal["norm"] == p_pal["reversed"]).astype(int)
p_pal = p_pal.sort_values("word").reset_index(drop=True)
pd.testing.assert_frame_equal(p_pal[["word", "norm", "reversed", "is_palindrome"]], sql_pal, check_dtype=False)  # sorted by word (binary)

nn = p_pal[p_pal["norm"] != ""].copy()
nn["signature"] = nn["norm"].map(lambda w: "".join(sorted(w)))
p_anag = (nn.groupby("signature").agg(n=("word", "size"), members=("word", lambda s: ",".join(sorted(s))))
            .query("n > 1").reset_index())
pd.testing.assert_frame_equal(p_anag, sql_anag, check_dtype=False)       # sorted by signature
print("pandas palindromes:", p_pal.loc[p_pal.is_palindrome == 1, "word"].tolist())
print("pandas anagram groups:", p_anag[["signature", "members"]].values.tolist())
con.close()
print("asserts passed")
```

**Output (my run):**
```text
        word      norm  reversed  is_palindrome
                                              1
A man a plan amanaplan nalpanama              0
       Level     level     level              1
      Silent    silent    tnelis              0
    Taco cat   tacocat   tacocat              1
         abc       abc       cba              0
         bca       bca       acb              0
         cab       cab       bac              0
      listen    listen    netsil              0
       madam     madam     madam              1
      tinsel    tinsel    lesnit              0
signature  n              members
      abc  3          abc,bca,cab
   eilnst  3 Silent,listen,tinsel
group_concat(DISTINCT word, '|') -> DISTINCT aggregates must have exactly one argument
group_concat(DISTINCT word) works, default separator ',': abc,cab
string_agg with ORDER BY works: A man a plan|Taco cat|abc|bca|cab|madam
reverse: no such function: reverse
pandas palindromes: ['', 'Level', 'Taco cat', 'madam']
pandas anagram groups: [['abc', 'abc,bca,cab'], ['eilnst', 'Silent,listen,tinsel']]
asserts passed
```

**Edge cases:**
- NULL: decide first. Here a NULL word is dropped; an empty string is a palindrome (decide whether the business wants that).
- `DISTINCT` in the CTE `w` matters if the same word appears twice; otherwise the recursion starts the same word twice.
- Case: `lower` is ASCII only, so 'É' will not fold (Q33).
- `group_concat(DISTINCT c, '')` is rejected by SQLite (`DISTINCT aggregates must have exactly one argument`): the run shows it. `group_concat(DISTINCT word)` with one argument works but the separator is fixed to a comma. The ordered form `group_concat(c, '' ORDER BY c)` works in 3.45.1 (the ORDER BY inside the aggregate was added in SQLite 3.44 according to the Wave A sources note; I ran only 3.45.1).
- Output order of `group_concat` without `ORDER BY` is not guaranteed.
- Signature collisions are impossible for sorted characters, but the signature of words with different lengths is different, so only true anagrams match.

**Then explain:**
- **Why recursion:** SQLite has no `REVERSE`, so build it: each step prepends the next character. PostgreSQL, MySQL and SQL Server have a `REVERSE` function (from memory, not executed here), so the real answer there is `norm = REVERSE(norm)`.
- **Why brain teaser:** it is not something you would do in production SQL; interviewers use it to see if you can think recursively, handle NULL and empty input, and know when to leave SQL.
- **What the interviewer is testing:** recursion base and stop condition, normalisation (case and spaces), NULL and empty handling, and the judgement that a two-line pandas or Python answer is better when the data is small.
- **pandas:** `s == s[::-1]` and `''.join(sorted(w))` give the same groups; the code asserts both the palindrome table and the anagram groups match.

**Follow-ups:**
- *Is the recursion expensive?* One row per character per word; fine for a word list, not for large text.
- *How do you do it without recursion?* Join to a numbers table of positions (Part 9) or use `REVERSE` where it exists.
- *How would you ignore punctuation?* More `replace` calls, or the application.

**Common mistakes:**
- Forgetting to normalise case and spaces.
- Treating NULL as a palindrome or as an empty string.
- No stop condition in the recursive member.
- Using `group_concat(DISTINCT c, '')` and being surprised by the error.
- Grouping on the unsorted string.


### Q38 ⭐ 🔴 Transposing a table: a small matrix kpis(metric, q1, q2, q3, q4) (3 metrics by 4 quarters) must be transposed so each quarter is a row and each metric is a column. Show the two-step method (unpivot with UNION ALL or CROSS JOIN VALUES, then pivot with MAX(CASE)), why transposing needs all values to share a type (text versus number mixing) and the NULL handling, and say why a true general transpose is not a SQL operation (column count fixed by the query). Add the pandas df.set_index('metric').T and stack/unstack versions and assert the SQL and pandas results match. Mention PIVOT/UNPIVOT in SQL Server and Oracle as hedged text.
**Asked at:** SQL pivot guides (datadriven.io, DataVidhya, Educative and a Medium write-up, search snippets only; the DataVidhya lesson page opened but showed only its introduction: CASE inside SUM or COUNT, dynamic pivot, NULL categories); guides, not candidate reports; analyst and data engineer rounds at product companies and GCCs; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Transposing in SQL is two steps: unpivot the quarter columns into rows with `CROSS JOIN (VALUES ...)` or `UNION ALL`, then pivot the metric rows into columns with `MAX(CASE ...)`; a fully general transpose is not a SQL operation because the output column list is fixed by the query.

**Schema and sample data:**
```sql
CREATE TABLE kpis(metric TEXT, q1, q2, q3, q4);   -- no declared types: values keep their own type
INSERT INTO kpis VALUES ('revenue', 100, 120, 130, 150),
                        ('cost',     60,  70, NULL,  90),
                        ('rating',  4.5, 4.0, 4.2, 4.8);
```

**SQL answer:** `unpivot_sql` (`kpis` cross joined to the four quarter names, with a `CASE quarter WHEN 'q1' THEN q1 ...` picking the value), `union_sql` (the `UNION ALL` spelling, asserted to give the same 12 rows) and `transpose_sql` (`GROUP BY quarter` over the long rows with `MAX(CASE WHEN metric = 'revenue' THEN val END)` and so on). SQLite does not accept a column list on a derived table (`AS q(quarter)` is a syntax error here), so the quarter names come from `(SELECT column1 AS quarter FROM (VALUES ...))`.

**pandas answer:** `k.set_index("metric").T` and `k.set_index("metric").stack().unstack("metric")`, each followed by `rename_axis(...)` and `reset_index()`. The Code block runs the stack version with warnings turned into errors to show the default `stack()` is the new implementation.

**Example:** Unpivot: each of the 3 metrics times 4 quarters gives 12 rows, e.g. (cost, q3, NULL). Pivot: group by quarter; for q1 the revenue cell is MAX of {100 for revenue rows, NULL for the other metrics} = 100, cost = 60, rating = 4.5. For q3: revenue 130, cost NULL (kept because UNION ALL and CROSS JOIN keep NULL values), rating 4.2. The result is 4 rows by 3 metric columns. `df.T` and `stack().unstack()` give the same table; in the SQL result revenue stays integer while cost and rating arrive as floats in pandas (a NULL or a decimal forces float), and `df.T` makes all three float64 because each original q1 to q4 column mixes integers and decimals.

**Code:** run with `python3 -I`; the two results are compared after the stated sort, then asserted.
```python
# Transpose a small matrix: unpivot (CROSS JOIN VALUES), then pivot (MAX CASE); pandas .T and stack/unstack.
import sqlite3
import warnings
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE kpis(metric TEXT, q1, q2, q3, q4);          -- no declared types: values keep their own type
INSERT INTO kpis VALUES ('revenue', 100, 120, 130, 150),
                        ('cost',     60,  70, NULL,  90),
                        ('rating',  4.5, 4.0, 4.2, 4.8);
""")

unpivot_sql = """
SELECT k.metric, q.quarter,
       CASE q.quarter WHEN 'q1' THEN k.q1 WHEN 'q2' THEN k.q2 WHEN 'q3' THEN k.q3 WHEN 'q4' THEN k.q4 END AS val
FROM kpis k CROSS JOIN (SELECT column1 AS quarter FROM (VALUES ('q1'),('q2'),('q3'),('q4'))) AS q"""
print(pd.read_sql(unpivot_sql + " ORDER BY k.metric, q.quarter", con).to_string(index=False))

transpose_sql = f"""
WITH long AS ({unpivot_sql})
SELECT quarter,
       MAX(CASE WHEN metric = 'revenue' THEN val END) AS revenue,
       MAX(CASE WHEN metric = 'cost'    THEN val END) AS cost,
       MAX(CASE WHEN metric = 'rating'  THEN val END) AS rating
FROM long GROUP BY quarter ORDER BY quarter"""
sql_t = pd.read_sql(transpose_sql, con)
print(sql_t.to_string(index=False))

# the UNION ALL spelling of the same unpivot gives the same rows
union_sql = ("SELECT metric,'q1' AS quarter,q1 AS val FROM kpis UNION ALL SELECT metric,'q2',q2 FROM kpis "
             "UNION ALL SELECT metric,'q3',q3 FROM kpis UNION ALL SELECT metric,'q4',q4 FROM kpis")
a = sorted(con.execute(unpivot_sql).fetchall(), key=lambda r: (r[0], r[1]))
b = sorted(con.execute(union_sql).fetchall(), key=lambda r: (r[0], r[1]))
assert a == b and len(a) == 12
print("typeof of the revenue/cost/rating cells in the long table:",
      con.execute(f"WITH long AS ({unpivot_sql}) SELECT metric, group_concat(DISTINCT typeof(val)) FROM long GROUP BY metric ORDER BY metric").fetchall())

# mixing types: a text value lands in the same output column as numbers
con.execute("INSERT INTO kpis VALUES ('status','ok','ok','late','ok')")
mixed = pd.read_sql(f"""WITH long AS ({unpivot_sql})
   SELECT quarter, MAX(CASE WHEN metric='revenue' THEN val END) AS revenue,
                   MAX(CASE WHEN metric='status'  THEN val END) AS status FROM long GROUP BY quarter ORDER BY quarter""", con)
print(mixed.to_string(index=False), "| pandas dtypes:", dict(mixed.dtypes.astype(str)))
print("what a single column mixing both gives for MAX:", con.execute(
    f"WITH long AS ({unpivot_sql}) SELECT MAX(val), MIN(val) FROM long WHERE quarter = 'q1'").fetchone(), "(text sorts above numbers)")
con.execute("DELETE FROM kpis WHERE metric = 'status'")

# ---- pandas
k = pd.read_sql("SELECT * FROM kpis", con)
t1 = k.set_index("metric").T.rename_axis(index="quarter", columns=None).reset_index()
with warnings.catch_warnings():
    warnings.simplefilter("error")                         # any deprecation warning would fail the run
    t2 = (k.set_index("metric").stack().unstack("metric")   # new stack keeps NaN rows
            .rename_axis(index="quarter", columns=None).reset_index())
cols = ["quarter", "revenue", "cost", "rating"]
t1, t2 = t1[cols], t2[cols]
print(t1.to_string(index=False))
for p in (t1, t2):
    pd.testing.assert_frame_equal(p.sort_values("quarter").reset_index(drop=True), sql_t, check_dtype=False)   # sorted by quarter
print("df.T dtypes:", dict(t1.dtypes.astype(str)))

# stack on a larger frame: future_stack default, legacy, and how to drop NaN
rng = np.random.default_rng(0)
big = pd.DataFrame(rng.normal(size=(1000, 4)), columns=list("abcd"))
big.iloc[::7, 1] = np.nan
big.iloc[::50, :] = np.nan
print("NaN cells:", int(big.isna().sum().sum()), "of", big.size)
print("stack() default      ->", big.stack().shape[0], "rows")
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    legacy = big.stack(future_stack=False)
print("stack(future_stack=False) ->", legacy.shape[0], "rows;", w[0].category.__name__ if w else "no warning")
print("stack().dropna()     ->", big.stack().dropna().shape[0], "rows (matches legacy:", big.stack().dropna().shape[0] == legacy.shape[0], ")")
try:
    big.stack(dropna=False)
except ValueError as e:
    print("stack(dropna=False) ->", e)
con.close()
print("asserts passed")
```

**Output (my run):**
```text
 metric quarter   val
   cost      q1  60.0
   cost      q2  70.0
   cost      q3   NaN
   cost      q4  90.0
 rating      q1   4.5
 rating      q2   4.0
 rating      q3   4.2
 rating      q4   4.8
revenue      q1 100.0
revenue      q2 120.0
revenue      q3 130.0
revenue      q4 150.0
quarter  revenue  cost  rating
     q1      100  60.0     4.5
     q2      120  70.0     4.0
     q3      130   NaN     4.2
     q4      150  90.0     4.8
typeof of the revenue/cost/rating cells in the long table: [('cost', 'integer,null'), ('rating', 'real'), ('revenue', 'integer')]
quarter  revenue status
     q1      100     ok
     q2      120     ok
     q3      130   late
     q4      150     ok | pandas dtypes: {'quarter': 'str', 'revenue': 'int64', 'status': 'str'}
what a single column mixing both gives for MAX: ('ok', 4.5) (text sorts above numbers)
quarter  revenue  cost  rating
     q1    100.0  60.0     4.5
     q2    120.0  70.0     4.0
     q3    130.0   NaN     4.2
     q4    150.0  90.0     4.8
df.T dtypes: {'quarter': 'str', 'revenue': 'float64', 'cost': 'float64', 'rating': 'float64'}
NaN cells: 220 of 4000
stack() default      -> 4000 rows
stack(future_stack=False) -> 3780 rows; Pandas4Warning
stack().dropna()     -> 3780 rows (matches legacy: True )
stack(dropna=False) -> dropna must be unspecified as the new implementation does not introduce rows of NA values. This argument will be removed in a future version of pandas.
asserts passed
```

**Edge cases:**
- Types: one SQL column has one type per cell but SQLite lets a column hold mixed types. When a text metric (`status`) is pivoted next to numbers it works, but `MAX` over a column that mixes numbers and text returns the text (text sorts above numbers: `('ok', 4.5)` in the run). Engines other than SQLite generally need all values of one output column to share a type, so cast to text first (not executed here).
- NULL: `UNION ALL`/`CROSS JOIN` keep NULL rows; SQL Server and Oracle's `UNPIVOT` drop NULLs by default (from memory, not executed here; Oracle has an `INCLUDE NULLS` option, also from memory). Dropping NULLs makes a quarter disappear if every metric is NULL.
- `MAX` is the usual pivot aggregate when there is at most one value per cell; if there can be several, use `SUM` or decide on a rule, otherwise it hides the duplicates.
- A quarter named in no `CASE` branch is lost, which is why the generated column list matters (Q31).
- pandas stack on a larger frame (1000 by 4 with 220 NaN cells): `stack()` default returned 4000 rows (NaN kept, new implementation), `stack(future_stack=False)` returned 3780 and emitted `Pandas4Warning`, `stack().dropna()` also gave 3780, and `stack(dropna=False)` raises `ValueError`. So on pandas 3 the NaN-dropping behaviour must be asked for with `.dropna()`.

**Then explain:**
- **Why two steps:** one operation turns columns into rows, the other rows into columns; SQL has neither as a keyword in SQLite.
- **Why not a general transpose:** the number and names of output columns are fixed when the statement is parsed. A table with an unknown number of metrics needs dynamic SQL (Q31), or you do it in pandas.
- **Dialects (not executed here):** SQL Server and Oracle have `PIVOT` and `UNPIVOT` operators; Snowflake and BigQuery have their own forms; MySQL and SQLite have neither. I did not run any of them.
- **pandas:** `.T` is one call; `stack`/`unstack` is the reshaping vocabulary; both give the same table, asserted after sorting by quarter.
- **Ordering:** `GROUP BY quarter ORDER BY quarter` gives q1 to q4 only because the labels sort that way; do not rely on a pivot's row order without ORDER BY.

**Follow-ups:**
- *What if the metric list grows?* Generate the CASE list (Q31) or keep long format.
- *Why MAX and not SUM?* Both work for one value per cell; MAX also works for text.
- *Is a `kpis` table with q1..q4 columns a good design?* It is a wide report format; the long table `(metric, quarter, value)` is easier to query.

**Common mistakes:**
- Pivoting without first checking there is one value per cell.
- Mixing text and numbers in one output column and getting surprising `MAX`/sort results.
- Dropping NULL rows in the unpivot and losing periods.
- Assuming the pivoted rows come out in quarter order without ORDER BY.
- Calling `stack(dropna=False)` on pandas 3.


### Q39 ⭐ 🔴 pandas astype, to_numeric, to_datetime and category pitfalls: a DataFrame read from CSV with amount strings ('1,200', ' 45 ', 'x', '1e3', ''), a pincode column with leading zeros ('011001'), a mixed date column and a status column converted to category. Show astype(int) failing on 'x', to_numeric with errors='coerce' and downcast, the thousands='' option of read_csv, dtype=str for leading-zero codes, to_datetime errors and format='mixed', and category pitfalls: assigning a value outside the categories raises, groupby with observed default (check on pandas 3.0.x), fillna with a new category, sorting by category order, and .str on a category column. Compare each with the SQLite CAST outcome from the CAST trap question in this part.
**Asked at:** pandas user guide pages on reshaping and on working with text data (opened: pivot, pivot_table, melt, wide_to_long, stack, unstack, crosstab, explode, string dtype and the .str accessor); official documentation, not candidate reports; data scientist and analyst rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** In pandas, `astype` is strict (it raises), `to_numeric(errors='coerce')` is lenient (garbage becomes NaN), `read_csv` has its own NA list, dates guess the format from the first value, and categories forbid unknown values; SQLite `CAST` never fails and quietly turns garbage into 0.

**Schema and sample data:**
```text
amount,amount_clean,pincode,when,status,country
"1,200","1,200",011001,2024-01-05,paid,NA
 45 ,45,110001,05/01/2024,paid,IN
x,7,400001,2024-03-07,refunded,None
1e3,"2,000",560001,not a date,paid,N/A
,,011001,,pending,IN
```
The CSV text is built inside the Code block with `io.StringIO`; for SQLite the `amount`, `pincode` and `when` columns are loaded into a `raw` table (and an `aff` table tests affinity).

**SQL answer:** `CAST(amount AS INTEGER)` and `CAST(amount AS REAL)` on the raw strings; a 'safe cast' that gives NULL for garbage (`CASE WHEN trim(amount) GLOB '[0-9]*' AND trim(amount) NOT GLOB '*[^0-9.]*' THEN CAST(trim(amount) AS REAL) END`); `date(d)` for the dates; and the `aff` and `st` (STRICT) tables for type affinity. SQLite has no `TRY_CAST`.

**pandas answer:** `astype(int)`, `pd.to_numeric(..., errors="coerce")` and `downcast="integer"`, `read_csv(thousands=",", dtype={"pincode": str}, keep_default_na=False, na_values=[""])`, `pd.to_datetime(..., errors="coerce")` with `format="mixed"` and `dayfirst=True`, and `astype("category")` with `add_categories`.

**Example:** Amounts '1,200', ' 45 ', 'x', '1e3', blank. `astype(int)` stops at '1,200' (`ValueError: invalid literal for int()`). `to_numeric(coerce)` gives NaN, 45.0, NaN, 1000.0, NaN: the comma value becomes NaN (so remove commas first), the padded ' 45 ' parses, 'x' and the blank are NaN, and '1e3' is accepted. SQLite `CAST(.. AS INTEGER)` gives 1, 45, 0, 1 for the first four: '1,200' stops at the comma and gives 1, 'x' gives 0, and '1e3' as INTEGER gives 1 but as REAL gives 1000.0. Pincode '011001' read as an integer loses the zero (11001); `dtype={"pincode": str}` keeps '011001'; `CAST('011001' AS INTEGER)` gives 11001. Dates: 2024-01-05 and 2024-03-07 parse in ISO form; '05/01/2024', 'not a date' and the blank are NaT with `coerce` (pandas guesses the format from the first value), the same rows that SQLite `date()` returns NULL for (asserted).

**Code:** run with `python3 -I`; the two results are compared after the stated sort, then asserted.
```python
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
```

**Output (my run):**
```text
default read_csv dtypes: {'amount': 'str', 'amount_clean': 'str', 'pincode': 'int64', 'when': 'str', 'status': 'str', 'country': 'str'}
pincode as int loses the zero: [11001, 110001, 400001, 560001, 11001] | country NA/None/N/A became: [nan, 'IN', nan, nan, 'IN']
thousands=',' + dtype/pincode + keep_default_na=False: {'amount': 'str', 'amount_clean': 'float64', 'pincode': 'str', 'when': 'str', 'status': 'str', 'country': 'str'}
amount_clean: [1200.0, 45.0, 7.0, 2000.0, nan] | amount (has 'x') stays text: ['1,200', ' 45 ', 'x', '1e3', nan] | pincode: ['011001', '110001', '400001', '560001', '011001'] | country: ['NA', 'IN', 'None', 'N/A', 'IN']
default NA markers: ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'None', 'n/a', 'nan', 'null']
astype(int) on the amount column   -> ValueError: invalid literal for int() with base 10: '1,200'
astype(int) on [' 45 ']            -> [45]
astype(float) on ['1e3']           -> [1000.0]
astype(float) on ['']              -> ValueError: could not convert string to float: ''
to_numeric (errors='raise')        -> ValueError: Unable to parse string "1,200" at position 0
to_numeric coerce: [nan, 45.0, nan, 1000.0, nan] float64
remove commas first: [1200.0, 45.0, nan, 1000.0, nan]
downcast='integer' on clean ints: int16 | with a NaN it stays: float64
SQLite CAST ('1,200', 1, 1.0, 11001)
SQLite CAST (' 45 ', 45, 45.0, 110001)
SQLite CAST ('x', 0, 0.0, 400001)
SQLite CAST ('1e3', 1, 1000.0, 560001)
SQLite CAST (None, None, None, 11001)
SQL safe-cast (NULL for garbage): [None, 45.0, None, None, None]
pandas coerce on '1e3': 1000.0 | SQL safe-cast: None | CAST AS INTEGER: 1
SQL date(): ['2024-01-05', None, '2024-03-07', None, None]
to_datetime default, strict        -> ValueError: time data "05/01/2024" doesn't match format "%Y-%m-%d". You might want to try:
    - passing `format` if your strings have a consistent format;
    - passing `format='ISO8601'` if your strings are all ISO8601 but not necessarily in exactly the same format;
    - passing `format='mixed'`, and the format will be inferred for each element individually. You might want to use `dayfirst` alongside this.
coerce (format guessed from row 1): ['2024-01-05', nan, '2024-03-07', nan, nan]
format='mixed': ['2024-01-05', '2024-05-01', '2024-03-07', nan, nan]
format='mixed', dayfirst=True: ['2024-05-01', '2024-01-05', '2024-07-03', nan, nan]
affinity row: ('integer', 12, 'text', ' 12', 'real', 12.0)
affinity row: ('integer', 12, 'text', '12 ', 'real', 12.0)
affinity row: ('text', 'x', 'text', 'x', 'text', 'x')
affinity row: ('integer', 1000, 'text', '1e3', 'real', 1000.0)
affinity row: ('text', '0x10', 'text', '0x10', 'text', '0x10')
affinity row: ('integer', 12, 'text', '12', 'real', 12.0)
TEXT column ' 12' = 12 -> 0 | INTEGER column ' 12' = 12 -> 1
STRICT insert ok: (' 12', 'x')
STRICT insert ('x', 'y') -> cannot store TEXT value in INTEGER column st.i
STRICT insert ok: ('12', 12)
STRICT stored: [('integer', 12, 'text', 'x'), ('integer', 12, 'text', '12')]
categories: ['paid', 'pending', 'refunded']
assign outside categories          -> TypeError: Cannot setitem on a Categorical with a new category (lost), set the categories first
fillna with a new category         -> TypeError: Cannot setitem on a Categorical with a new category (unknown), set the categories first
add_categories first: ['a', 'unknown', 'b']
groupby default: {'paid': 3, 'refunded': 3} | observed=False: {'pending': 0, 'paid': 3, 'refunded': 3}
sort by category order: ['pending', 'paid', 'refunded'] | alphabetical: ['paid', 'pending', 'refunded']
.str on category works, result dtype: object ['PAID', 'PAID', 'REFUNDED', 'PAID', 'PENDING']
asserts passed
```

**Edge cases:**
- `astype(int)` accepted `' 45 '` (Python's `int()` strips spaces) but failed on `'1e3'`; `astype(float)` accepted `'1e3'` but failed on `''` (`could not convert string to float`).
- `errors="coerce"` hides bad data; check how many NaN you created. `downcast="integer"` gave `int16` for clean integers, and with a missing value the dtype stayed `float64`.
- `thousands=","` worked for `amount_clean` (float64) but the `amount` column, which holds 'x', stays text.
- The default `read_csv` NA list includes `NA`, `N/A`, `NULL`, `None`, `null`, `n/a`, `nan`, `NaN`, `<NA>`, `#N/A`, `#N/A N/A`, `#NA`, `-NaN`, `-nan`, `1.#IND`, `1.#QNAN`, `-1.#IND`, `-1.#QNAN` and the empty string (printed in the output). So the country code `NA` (Namibia) and the text 'None' became NaN; `keep_default_na=False, na_values=[""]` kept them.
- Dates: strict `to_datetime` raised on '05/01/2024' because the format was taken from the first value (`%Y-%m-%d`). `format="mixed"` parsed '05/01/2024' as 2024-05-01 (month first, 1 May). Adding `dayfirst=True` turned it into 2024-01-05 but also flipped the ISO strings: '2024-01-05' became 2024-05-01 and '2024-03-07' became 2024-07-03 (printed in the output). Mixed formats are ambiguous; fix the format at the source.
- SQLite affinity (run): an INTEGER column stores `' 12'` and `'12 '` as the integer 12 (leading and trailing spaces allowed), `'1e3'` as 1000, `'x'` and `'0x10'` stay text; a TEXT column keeps `' 12'` as text and converts the integer 12 to `'12'`; `t = 12` is 0 for the TEXT column holding `' 12'` but `i = 12` is 1 for the INTEGER column. A STRICT table accepted `' 12'` into INTEGER (stored as 12) and rejected `'x'` with `cannot store TEXT value in INTEGER column`.
- Category: assigning 'lost' or `fillna('unknown')` raised `TypeError ... set the categories first`; `add_categories` first works. In this run (pandas 3.0.5) `groupby` on a categorical gave only the observed groups by default; `observed=False` added the empty 'pending' group with 0. Sorting an ordered categorical followed category order (pending, paid, refunded), not alphabetical. `.str.upper()` on a category column worked and returned `object` dtype.

**Then explain:**
- **astype versus to_numeric:** `astype` is a strict cast (error on the first bad value); `to_numeric` is the parsing tool with `errors` and `downcast` options.
- **SQLite CAST:** never raises; it reads the longest numeric prefix and returns 0 if there is none. `'12abc'` is 12 and `''` is 0, which is dangerous because 0 looks like data. A NULL-returning safe cast needs a `CASE` with `GLOB` checks (no `TRY_CAST` in SQLite). Other engines have `TRY_CAST` or `SAFE_CAST` (not executed here).
- **Leading zeros:** codes are labels, not numbers; read them as text.
- **Categories:** compact and ordered, but closed sets; the nulls, new values and empty groups behave differently from plain strings.
- **Comparison:** SQL gives 0 for garbage, pandas coerce gives NaN, SQL safe-cast gives NULL; pandas NaN and SQL NULL then agree.

**Follow-ups:**
- *Why does `read_csv` read my `NA` country as missing?* Because `NA` is in the default list; switch it off with `keep_default_na=False`.
- *Is `observed` default always True?* I only checked 3.0.5 here (it was observed-only); older versions defaulted differently.
- *How would you validate amounts?* Coerce, count the new NaN, and report them with the original strings.

**Common mistakes:**
- Casting a pincode to int and losing the zero.
- Using `errors="coerce"` and not counting what was lost.
- Believing `CAST('abc' AS INTEGER)` raises in SQLite.
- Using `dayfirst=True` on mixed ISO and local formats.
- Assigning a new value to a category column without adding the category.


### Q40 ⭐ 🔴 SQL versus pandas differences on strings and NULLs, a translation table with each row demonstrated on tiny data: NaN == NaN is False and NULL = NULL is NULL (both not true), IS NOT DISTINCT FROM versus Series.equals, groupby dropna (pandas default drops NaN keys, SQL GROUP BY keeps NULL), empty string versus NaN (read_csv turns blanks into NaN, SQL keeps ''), sum of an all-missing column (0 versus NULL), integer column becoming float when it holds NaN, LIKE (ASCII case-insensitive in SQLite) versus str.contains (case-sensitive regex by default), SQL wildcards versus regex metacharacters (a literal dot and percent sign), and sort position of NULL versus NaN. Run each row with SQLite and pandas 3.0.x and assert the stated result. Cross-reference Part 1 Q16 and say what is new here.
**Asked at:** pandas user guide pages on reshaping and on working with text data (opened: pivot, pivot_table, melt, wide_to_long, stack, unstack, crosstab, explode, string dtype and the .str accessor); official documentation, not candidate reports; data scientist and analyst rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** pandas and SQL disagree on missing values and strings in about ten systematic ways; the translation table in the Code block runs each one on SQLite and pandas and asserts the stated result: NULL = NULL is NULL (not true) but `IS NOT DISTINCT FROM` is true, `NaN == NaN` is False, groupby drops NaN keys, blanks become NaN in `read_csv`, empty sums differ, integers become floats, and `LIKE` is a wildcard pattern while `str.contains` is a case-sensitive regex.

**Schema and sample data:**
```sql
CREATE TABLE o(region TEXT, amount INTEGER);
INSERT INTO o VALUES ('N',1),('N',2),(NULL,5),(NULL,NULL),('S',NULL);
CREATE TABLE w(s TEXT);
INSERT INTO w VALUES ('Apple'),('apple pie'),('a.b'),('axb'),('100%'),('1000'),('Ärger'),(NULL);
CREATE TABLE v(x INTEGER);   INSERT INTO v VALUES (3),(NULL),(1);
CREATE TABLE c(name TEXT, city TEXT);   -- Asha has a blank city: the CSV text is 'name,city' / 'Asha,' / 'Ben,Pune'
```

**SQL answer:** Each translation row is a one-line SQL query in the Code block (the left column of the printed table).

**pandas answer:** Each row has its pandas counterpart in the right column; the `row()` helper asserts both against the stated pair before adding it to the table.

**Example:** Row 1: `NULL = NULL` returns NULL (no row would match), while `NaN == NaN` is False; `NULL IS NOT DISTINCT FROM NULL` is 1 and the pandas null-safe version is `a.eq(b) | (a.isna() & b.isna())`; `Series.equals` treats NaNs in the same place as equal, a whole-object test with no SQL counterpart. With the nullable `Int64`/`string` dtypes `pd.NA == pd.NA` is `<NA>`, like SQL. Row 2: `GROUP BY region` over N, N, NULL, NULL, S gives 3 groups; `groupby("region")` gives 2 and `dropna=False` gives 3. Row 3: the blank CSV city is `''` in SQLite, NaN in pandas (`keep_default_na=False` keeps `''`), and `COUNT(city)` is 2 while `count()` is 1. Row 4: `SUM` of an all-NULL group is NULL; pandas `sum()` is 0.0 and `sum(min_count=1)` is NaN. Row 5: an INTEGER column with a NULL has typeof integer and null; pandas gives `float64`, or `Int64` with the nullable dtype. Row 6: `LIKE '%APPLE%'` matches 'Apple' and 'apple pie'; `contains('APPLE')` matches nothing; `case=False` fixes it; for 'Ärger' SQL `LIKE` does not fold (0) but pandas does (True). Row 7: `LIKE 'a.b'` matches only 'a.b' but regex `a.b` also matches 'axb'; `LIKE '100%'` matches '100%' and '1000' (percent is a wildcard) but `contains('100%')` matches only the literal; `LIKE 'a%'` also matches 'Apple' (case-insensitive) but `startswith('a')` does not. Row 8: ascending, NULL sorts first in SQLite and NaN last in pandas; `NULLS LAST` aligns them.

**Code:** run with `python3 -I`; the two results are compared after the stated sort, then asserted.
```python
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
```

**Output (my run):**
```text
                                            row                          SQLite 3.45                  pandas 3.0
                   1 NaN == NaN  /  NULL = NULL                                 None                       False
       1b null-safe equal of two missing values                                    1                        True
                 1c elementwise null-safe equal                            [1, 1, 0]                   [1, 1, 0]
                    1d plain a = b vs Series.eq                         [1, None, 0]                   [1, 0, 0]
    1e Series.equals (whole object, NaN == NaN)                   'no such operator'                        True
             1f pd.NA == pd.NA (nullable dtype)                                 None                      '<NA>'
                       2 groups with a NULL key                                    3                           2
                       2b dropna=False keeps it                                    3                           3
                              3 blank CSV field                                   ''                        True
                           3b keep '' in pandas                                   ''                          ''
                      3c COUNT(city) vs count()                                    2                           1
                           4 SUM of all-missing                                 None                         0.0
                            4b with min_count=1                                 None                        True
      5 typeof of an INTEGER column with a NULL                       'integer,null'                   'float64'
               5b nullable Int64 keeps integers                            'integer'                     'Int64'
          6 LIKE '%APPLE%' vs contains('APPLE')               ['Apple', 'apple pie']                          []
                        6b contains(case=False)               ['Apple', 'apple pie']      ['Apple', 'apple pie']
                              6c non-ASCII case                                    0                        True
                      6d NULL row in the result                                 None                       False
                7 'a.b': LIKE vs regex contains                              ['a.b']              ['a.b', 'axb']
                       7b contains(regex=False)                              ['a.b']                     ['a.b']
           7c '100%': LIKE wildcard vs contains                     ['100%', '1000']                    ['100%']
7d LIKE '100\%' ESCAPE vs contains(regex=False)                             ['100%']                    ['100%']
                     7e startswith vs LIKE 'a%' ['Apple', 'apple pie', 'a.b', 'axb'] ['apple pie', 'a.b', 'axb']
 8 ascending sort position of the missing value                         [None, 1, 3]                [1, 3, None]
                 8b NULLS LAST / default pandas                         [1, 3, None]                [1, 3, None]
asserts passed
```

**Edge cases:**
- The NULL row in `LIKE` and in `str.contains`: SQL gives NULL (row not returned either way), pandas 3.0.5's default `str` dtype gives False for the missing value. With `dtype="string"` it would give `<NA>` (checked in Wave A, not part of this run).
- Part 1 Q16 already covers rows 2, 4 and the sort position (and `COUNT` versus `count`); what is new here is the comparison semantics (row 1), the CSV blank (row 3), integer-to-float (row 5) and the string matching rows (6 and 7). They are repeated in one line only so every row of the table has a run.
- `IS NOT DISTINCT FROM` ran on SQLite 3.45.1; older versions and some engines lack it (MySQL uses `<=>`, from memory, not executed here).
- `bool(pd.NA)` raises `TypeError` (Wave A check); filters with `pd.NA` need `.fillna(False)` first.
- A pattern with `_` also matches any single character in `LIKE`: `LIKE 'a_b'` would match 'a.b' and 'axb'. Use `ESCAPE` for a literal.

**Then explain:**
- **Equality:** SQL uses three-valued logic (a comparison with NULL is UNKNOWN); NaN is an ordinary float that happens to be unequal to itself; `pd.NA` is closer to SQL NULL.
- **Missing keys:** pandas drops them from groups by default; SQL keeps one NULL group.
- **Empty versus missing:** SQL stores `''` and NULL differently; `read_csv` merges blank and many placeholders into NaN.
- **Sums and dtypes:** an empty sum is NULL in SQL and 0 in pandas; NaN forces floats unless a nullable dtype is used.
- **Strings:** `LIKE` has two wildcards, is case-insensitive for ASCII (SQLite) and anchored; `str.contains` is a regex that searches anywhere and is case-sensitive; use `regex=False` or `re.escape` for literals.
- **Sorting:** SQLite sorts NULL as the smallest value; pandas puts NaN last. Both can be changed (`NULLS LAST`, `na_position`).
- Dialect note: other SQL engines differ on `LIKE` case sensitivity and NULL ordering (not executed here).

**Follow-ups:**
- *How do I make pandas behave like SQL?* `dropna=False`, `min_count=1`, nullable dtypes, `keep_default_na=False`, explicit `na_position`.
- *Which side is right?* Neither; they have different models, so state the rule you want and test it.
- *Is `==` in pandas ever NULL-like?* With `pd.NA` (nullable dtypes), yes.

**Common mistakes:**
- Writing `WHERE col = NULL` or `df[df.col == np.nan]`.
- Expecting `str.contains` to be case-insensitive or literal.
- Treating `LIKE 'a.b'` as a regex.
- Forgetting a blank CSV field becomes NaN.
- Comparing SQL and pandas results without aligning missing values and sort order.

### Q1 ⭐⭐⭐ 🟢 Pivot with conditional aggregation: sales(region, product, month, amount) where month holds 'Jan', 'Feb', 'Mar' and several rows can exist per region, product and month. Return one row per region with one column per month (jan, feb, mar) holding the summed amount, plus a total column, using SUM(CASE WHEN month = 'Jan' THEN amount END) and the COUNT(CASE ...) variant for number of sales per month. Explain why the CASE goes inside the aggregate, what ELSE 0 versus no ELSE changes when a region has no January rows (0 versus NULL), why the GROUP BY is on region only, and say SQLite and MySQL have no PIVOT keyword so this is the portable answer. Cross-reference Part 1 Q10 for plain conditional aggregation; add the pandas pivot_table version.
**Asked at:** Indian IT-services and GCC SQL question banks (Scribd and Telegram uploads and blog guides seen only as search snippets, quality unverified, not candidate reports); fresher to mid-level analyst rounds; SQL pivot guides (datadriven.io, DataVidhya, Educative and a Medium write-up, search snippets only; the DataVidhya lesson page opened but showed only its introduction: CASE inside SUM or COUNT, dynamic pivot, NULL categories); guides, not candidate reports; analyst and data engineer rounds at product companies and GCCs
**Say this first (1 line):** Put the CASE inside the aggregate, one `SUM(CASE WHEN month = 'X' THEN amount END)` per output column, and group by region only; SQLite and MySQL have no PIVOT keyword, so this is the portable answer.

**Schema and sample data:**
```sql
CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','A','Jan',100),('East','A','Jan',50),('East','B','Feb',200),('East','A','Mar',30),
 ('West','A','Feb',80),('West','B','Feb',20),('West','B','Mar',60),
 ('North','A','Mar',40);
```

**SQL answer:** the main pivot is `sql_sum` in the Code block (variants: `sql_else0`, `sql_count`, `sql_filter`).
```sql
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS mar,
       SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY region
```
The count version is `COUNT(CASE WHEN month = 'Jan' THEN 1 END)`, with no ELSE.

**pandas answer:** `pivot_table` builds the same table; the Code block reorders the columns and adds the total from a plain groupby.
```py
pt = sales.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
pt = pt[months]
pt["total"] = sales.groupby("region")["amount"].sum()
```

**Example:** East has Jan rows 100 and 50, so jan = 150; Feb = 200; Mar = 30; total = 380. West has no Jan rows: the CASE returns NULL for every West row, `SUM` of nothing but NULLs is NULL, so jan is NULL (0 with `ELSE 0`). West feb = 80 + 20 = 100, mar = 60, total = 160. North has only March: jan and feb NULL, mar = 40, total = 40. For counts, East jan_n = 2 because two rows exist (two sales, not one).

**Code:** run with `python3 -I`.
```python
# Q1: pivot with conditional aggregation (SUM and COUNT of CASE) vs pandas pivot_table.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','A','Jan',100),('East','A','Jan',50),('East','B','Feb',200),('East','A','Mar',30),
 ('West','A','Feb',80),('West','B','Feb',20),('West','B','Mar',60),
 ('North','A','Mar',40);
""")

sql_sum = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS mar,
       SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY region
"""
sql_else0 = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount ELSE 0 END) AS jan,
       SUM(CASE WHEN month = 'Feb' THEN amount ELSE 0 END) AS feb,
       SUM(CASE WHEN month = 'Mar' THEN amount ELSE 0 END) AS mar,
       SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY region
"""
sql_count = """
SELECT region,
       COUNT(CASE WHEN month = 'Jan' THEN 1 END) AS jan_n,
       COUNT(CASE WHEN month = 'Feb' THEN 1 END) AS feb_n,
       COUNT(CASE WHEN month = 'Mar' THEN 1 END) AS mar_n
FROM sales
GROUP BY region
ORDER BY region
"""
sql_filter = """
SELECT region,
       SUM(amount) FILTER (WHERE month = 'Jan') AS jan,
       SUM(amount) FILTER (WHERE month = 'Feb') AS feb,
       SUM(amount) FILTER (WHERE month = 'Mar') AS mar,
       SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY region
"""

def show(title, q):
    df = pd.read_sql(q, con)
    print(title); print(df.to_string(index=False)); print()
    return df

s_sum = show("SUM(CASE) no ELSE (missing month = NULL):", sql_sum)
s_else0 = show("SUM(CASE ... ELSE 0) (missing month = 0):", sql_else0)
s_cnt = show("COUNT(CASE ... THEN 1 END):", sql_count)
s_fil = show("SUM(amount) FILTER (WHERE ...):", sql_filter)
assert s_sum.equals(s_fil)

# wrong version: CASE outside the aggregate needs GROUP BY region, month and gives one row per month
wrong = pd.read_sql("SELECT region, CASE WHEN month='Jan' THEN SUM(amount) END AS jan "
                    "FROM sales GROUP BY region, month ORDER BY region, month", con)
print("CASE outside SUM, grouped by region and month: %d rows instead of 3" % len(wrong)); print()

# pandas
sales = pd.read_sql("SELECT * FROM sales", con)
months = ["Jan", "Feb", "Mar"]
pt = sales.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
print("pivot_table default column order:", list(pt.columns))
pt = pt[months]
pt.columns = [m.lower() for m in months]
pt["total"] = sales.groupby("region")["amount"].sum()
p_sum = pt.reset_index().rename_axis(columns=None).sort_values("region").reset_index(drop=True)
print(p_sum.to_string(index=False)); print()

cnt = sales.pivot_table(index="region", columns="month", values="amount", aggfunc="count", fill_value=0)
cnt = cnt[months]
cnt.columns = [m.lower() + "_n" for m in months]
p_cnt = cnt.reset_index().rename_axis(columns=None).sort_values("region").reset_index(drop=True)

# compare after sorting by region; NaN in pandas == NULL in SQL (read_sql gives NaN for NULL)
pd.testing.assert_frame_equal(s_sum.sort_values("region").reset_index(drop=True), p_sum, check_dtype=False)
pd.testing.assert_frame_equal(s_cnt.sort_values("region").reset_index(drop=True), p_cnt, check_dtype=False)
print("pivot_table with fill_value=0 turns the missing West/Jan into 0:",
      sales.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", fill_value=0).loc["West", "Jan"])
print("asserts passed (compared after sorting by region)")
```

**Output (my run):**
```text
SUM(CASE) no ELSE (missing month = NULL):
region   jan   feb  mar  total
  East 150.0 200.0   30    380
 North   NaN   NaN   40     40
  West   NaN 100.0   60    160

SUM(CASE ... ELSE 0) (missing month = 0):
region  jan  feb  mar  total
  East  150  200   30    380
 North    0    0   40     40
  West    0  100   60    160

COUNT(CASE ... THEN 1 END):
region  jan_n  feb_n  mar_n
  East      2      1      1
 North      0      0      1
  West      0      2      1

SUM(amount) FILTER (WHERE ...):
region   jan   feb  mar  total
  East 150.0 200.0   30    380
 North   NaN   NaN   40     40
  West   NaN 100.0   60    160

CASE outside SUM, grouped by region and month: 6 rows instead of 3

pivot_table default column order: ['Feb', 'Jan', 'Mar']
region   jan   feb  mar  total
  East 150.0 200.0 30.0    380
 North   NaN   NaN 40.0     40
  West   NaN 100.0 60.0    160

pivot_table with fill_value=0 turns the missing West/Jan into 0: 0
asserts passed (compared after sorting by region)
```

**Edge cases:**
- **No ELSE gives NULL, ELSE 0 gives 0.** With no January rows, `SUM(CASE ... END)` is NULL ("no data") and `SUM(CASE ... ELSE 0 END)` is 0. Pick on purpose: NULL keeps "nothing happened" separate from "summed to zero", 0 is friendlier for a report. `COALESCE(SUM(...), 0)` gives the same as `ELSE 0`.
- **COUNT must not have ELSE 0.** `COUNT(CASE WHEN month = 'Jan' THEN 1 ELSE 0 END)` counts every row, because 0 is not NULL. Leave the ELSE out, or use `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`.
- **Labels outside the list** ('jan', ' Feb', 'Apr', NULL) do not land in any column but are still in `SUM(amount)`, so columns can add up to less than the total. That is the reconciliation problem in Q10.
- **NULL amounts:** `SUM` skips them; a month whose only rows have a NULL amount still shows NULL, while `COUNT(CASE ... THEN 1 END)` counts that row.
- **A region with no sales at all** is not in `sales`, so it has no output row; join from a regions table if it must appear.

**Then explain:**
- **Why the CASE is inside the aggregate:** each output column is "sum over this region, but only the rows of that month". The CASE turns other-month rows into NULL, which `SUM` skips. Outside the aggregate it is evaluated per row, so you would need `GROUP BY region, month` (in my run that gave 6 rows instead of 3).
- **Why GROUP BY region only:** region is the row key. Month and product are folded into the columns or summed away, so one row per region comes out.
- **FILTER form:** `SUM(amount) FILTER (WHERE month = 'Jan')` ran on SQLite 3.45.1 and matched the CASE result. It is the same idea in cleaner syntax (PostgreSQL also has it; not executed here). MySQL has no FILTER, from memory, so use CASE or `IF()` there.
- **Other engines:** SQL Server, Oracle, Snowflake and BigQuery have a `PIVOT` keyword (not executed here). SQLite and MySQL do not, so the CASE form is the one that works everywhere.
- **pandas:** `pivot_table` sorts the new columns alphabetically (my run gave Feb, Jan, Mar), so reorder them. Missing combinations are NaN, like NULL; `fill_value=0` gives the `ELSE 0` behaviour (West/Jan became 0). `aggfunc="count"` counts non-NaN amounts, like `COUNT(CASE ...)` on the amount column.
- Plain conditional aggregation basics are in Part 1 Q10; this question is the reshaping use of it.

**Follow-ups:**
- *What if new months appear?* The column list is fixed at parse time, so you generate the SQL from the distinct months in the application (Q31) or return long format.
- *How do you add a column for "all other months"?* `SUM(CASE WHEN month NOT IN ('Jan','Feb','Mar') THEN amount END)`, and watch NULL months (Q10).
- *Which is better, SUM(CASE) or FILTER?* Same result; FILTER reads better where it exists, CASE works everywhere.

**Common mistakes:**
- Grouping by region and month and calling it a pivot.
- Writing `ELSE 0` inside `COUNT` and counting every row.
- Forgetting that a missing month shows NULL, then adding columns with `+` and getting NULL totals (Q10).
- Using `SUM(amount)` for the total column and not noticing it differs from jan + feb + mar when other labels exist.

### Q2 ⭐⭐⭐ 🟢 Clean messy customer names: customers(customer_id, name) where name has leading and trailing spaces, double spaces inside ('  Asha   Rao '), mixed case ('RAHUL sharma') and some empty strings. Return a cleaned name with TRIM, a REPLACE loop for double spaces (explain why one REPLACE(name, '  ', ' ') is not enough for three or more spaces and show the fix), LOWER for comparison, and LENGTH before and after to prove what changed. Show that TRIM(x, 'ab') removes a set of characters, not a substring, and that TRIM without a second argument strips only the space character (not tabs or newlines). Add the pandas str.strip, str.replace(r'\s+', ' ', regex=True) and str.casefold version and state that pandas strip also removes Unicode whitespace.
**Asked at:** SQLite lang_corefunc and lang_expr documentation (opened: trim character sets, ASCII-only lower/upper and LIKE, length versus octet_length, concat/concat_ws NULL rules, CAST rules, IS DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL table); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds
**Say this first (1 line):** `TRIM(name)` strips the edges, a REPLACE trick collapses the inner runs of spaces, `LOWER` gives a comparison key, and `LENGTH` before and after proves what changed; in SQLite `TRIM` with no second argument removes only the space character, not tabs or newlines.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO customers VALUES
 (1,'  Asha   Rao '),(2,'RAHUL sharma'),(3,''),(4,'Meena    Iyer     Nair'),
 (5,NULL),(6,char(9)||'Dev'||char(9)),(7,'   ');
```

**SQL answer:** the cleaning query is `sql_clean` in the Code block; its core expression is the marker version of the space collapse:
```sql
REPLACE(REPLACE(REPLACE(TRIM(name), '  ', ' ' || char(1)), char(1) || ' ', ''), char(1), '')
```
`sql_one` (a single REPLACE) and `sql_three` (three nested REPLACEs) are there for the comparison.

**pandas answer:** strip, collapse with a regex (pandas 3 needs `regex=True`), casefold for the key.
```py
p_clean = cust["name"].str.strip().str.replace(r"\s+", " ", regex=True)
```
`p_clean.str.casefold()` is the comparison key.

**Example:** customer 1 is `'  Asha   Rao '`, 13 characters. `TRIM` leaves `'Asha   Rao'` (three spaces inside). One `REPLACE(x, '  ', ' ')` turns the three spaces into two (it works through the string left to right on non-overlapping pairs), giving `'Asha  Rao'`. The marker version gives `'Asha Rao'`, length 8, and `LOWER` gives `'asha rao'`. Customer 4 has runs of 4 and 5 spaces: one REPLACE gives runs of 2 and 3, the marker version gives `'Meena Iyer Nair'`, 22 characters down to 15. Customers 3 (`''`) and 7 (`'   '`) both end as `''` with length 0. Customer 5 stays NULL, with NULL lengths.

**Code:** run with `python3 -I`.
```python
# Q2: clean messy customer names with TRIM, REPLACE, LOWER, LENGTH; same in pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO customers VALUES
 (1,'  Asha   Rao '),(2,'RAHUL sharma'),(3,''),(4,'Meena    Iyer     Nair'),
 (5,NULL),(6,char(9)||'Dev'||char(9)),(7,'   ');
""")

# one REPLACE only halves runs of spaces; the marker trick collapses any run to one space
sql_one = "REPLACE(TRIM(name), '  ', ' ')"
sql_three = "REPLACE(REPLACE(REPLACE(TRIM(name), '  ', ' '), '  ', ' '), '  ', ' ')"
sql_marker = ("REPLACE(REPLACE(REPLACE(TRIM(name), '  ', ' ' || char(1)), char(1) || ' ', ''), char(1), '')")
sql_clean = f"""
SELECT customer_id,
       name AS raw,
       LENGTH(name) AS len_before,
       {sql_marker} AS clean,
       LENGTH({sql_marker}) AS len_after,
       LOWER({sql_marker}) AS cmp_key
FROM customers
ORDER BY customer_id
"""
df_sql = pd.read_sql(sql_clean, con)
print(df_sql.assign(raw=df_sql.raw.map(repr)).to_string(index=False)); print()

print("--- why one REPLACE is not enough (customer 1 and 4) ---")
for cid in (1, 4):
    one, three, marker = con.execute(
        f"SELECT {sql_one}, {sql_three}, {sql_marker} FROM customers WHERE customer_id = ?", (cid,)).fetchone()
    print(cid, "one REPLACE:", repr(one), "| three REPLACEs:", repr(three), "| marker trick:", repr(marker))
# a run of 10 spaces: three passes leave a double space, the marker trick does not
one, three, marker = con.execute(
    "WITH t(name) AS (SELECT 'a' || '          ' || 'b') "
    f"SELECT {sql_one}, {sql_three}, {sql_marker} FROM t").fetchone()
print("10 spaces:", repr(one), repr(three), repr(marker))

print("\n--- TRIM semantics ---")
print("TRIM('abcba','ab') =", repr(con.execute("SELECT TRIM('abcba','ab')").fetchone()[0]), "(a set of characters, not a substring)")
print("TRIM('abab','ab')  =", repr(con.execute("SELECT TRIM('abab','ab')").fetchone()[0]))
print("TRIM('xabx','xab') =", repr(con.execute("SELECT TRIM('xabx','xab')").fetchone()[0]))
print("TRIM(tab+Dev+tab) length:", con.execute("SELECT LENGTH(TRIM(name)) FROM customers WHERE customer_id=6").fetchone()[0], "(tabs stay, 5 not 3)")
print("TRIM(name, space+tab) length:",
      con.execute("SELECT LENGTH(TRIM(name, ' ' || char(9) || char(10) || char(13))) FROM customers WHERE customer_id=6").fetchone()[0])
print("TRIM(NBSP+x+NBSP) length:", con.execute("SELECT LENGTH(TRIM(char(160) || 'x' || char(160)))").fetchone()[0], "(NBSP stays)")

# pandas
cust = pd.read_sql("SELECT * FROM customers ORDER BY customer_id", con)
p_clean = cust["name"].str.strip().str.replace(r"\s+", " ", regex=True)
p = pd.DataFrame({"customer_id": cust.customer_id, "clean": p_clean, "cmp_key": p_clean.str.casefold(),
                  "len_after": p_clean.str.len()})
print("\npandas dtype of name:", cust["name"].dtype, "| missing marker:", cust["name"][4])
print(p.to_string(index=False))
print("pandas strip on tab+Dev+tab:", repr(cust.loc[5, "name"].strip()), "-> pandas strips tabs and NBSP:",
      repr(pd.Series([" x \t"]).str.strip()[0]))

print("str.replace(r'\\s+', ' ') without regex=True leaves it alone (pandas 3 default regex=False):",
      repr(pd.Series(["a   b"]).str.replace(r"\s+", " ")[0]))
# SQL's TRIM(name) strips only spaces, so for customer 6 SQL keeps tabs: make SQL strip tabs too for a fair comparison
sql_fair = f"""SELECT customer_id,
  REPLACE(REPLACE(REPLACE(TRIM(REPLACE(REPLACE(name, char(9), ' '), char(10), ' ')), '  ', ' ' || char(1)), char(1) || ' ', ''), char(1), '') AS clean
FROM customers ORDER BY customer_id"""
fair = pd.read_sql(sql_fair, con)
assert fair["clean"].fillna("<NULL>").tolist() == p["clean"].fillna("<NULL>").tolist()
# customer 7 ('   ') and 3 ('') both end as '' in SQL and pandas; customer 5 stays NULL / NaN
assert pd.isna(fair.loc[4, "clean"]) and pd.isna(p.loc[4, "clean"])
assert fair.loc[6, "clean"] == "" == p.loc[6, "clean"]
print("asserts passed (compared in customer_id order; tabs mapped to spaces in the SQL first)")
```

**Output (my run):**
```text
 customer_id                      raw  len_before           clean  len_after         cmp_key
           1          '  Asha   Rao '        13.0        Asha Rao        8.0        asha rao
           2           'RAHUL sharma'        12.0    RAHUL sharma       12.0    rahul sharma
           3                       ''         0.0                        0.0                
           4 'Meena    Iyer     Nair'        22.0 Meena Iyer Nair       15.0 meena iyer nair
           5                      nan         NaN             NaN        NaN             NaN
           6                '\tDev\t'         5.0         \tDev\t        5.0         \tdev\t
           7                    '   '         3.0                        0.0                

--- why one REPLACE is not enough (customer 1 and 4) ---
1 one REPLACE: 'Asha  Rao' | three REPLACEs: 'Asha Rao' | marker trick: 'Asha Rao'
4 one REPLACE: 'Meena  Iyer   Nair' | three REPLACEs: 'Meena Iyer Nair' | marker trick: 'Meena Iyer Nair'
10 spaces: 'a     b' 'a  b' 'a b'

--- TRIM semantics ---
TRIM('abcba','ab') = 'c' (a set of characters, not a substring)
TRIM('abab','ab')  = ''
TRIM('xabx','xab') = ''
TRIM(tab+Dev+tab) length: 5 (tabs stay, 5 not 3)
TRIM(name, space+tab) length: 3
TRIM(NBSP+x+NBSP) length: 3 (NBSP stays)

pandas dtype of name: str | missing marker: nan
 customer_id           clean         cmp_key  len_after
           1        Asha Rao        asha rao        8.0
           2    RAHUL sharma    rahul sharma       12.0
           3                                        0.0
           4 Meena Iyer Nair meena iyer nair       15.0
           5             NaN             NaN        NaN
           6             Dev             dev        3.0
           7                                        0.0
pandas strip on tab+Dev+tab: 'Dev' -> pandas strips tabs and NBSP: 'x'
str.replace(r'\s+', ' ') without regex=True leaves it alone (pandas 3 default regex=False): 'a   b'
asserts passed (compared in customer_id order; tabs mapped to spaces in the SQL first)
```

**Edge cases:**
- **Why one REPLACE is not enough:** a run of n spaces becomes about n/2 spaces per pass (3 became 2, 4 became 2, 5 became 3). Three nested REPLACEs handled these rows but left a double space in my 10-space test (`'a  b'`). The marker trick has no such limit: each `'  '` becomes space plus `char(1)`, then `char(1)` followed by a space is deleted, then any left-over marker is deleted. It assumes `char(1)` never occurs in the data. A recursive CTE that repeats REPLACE until `INSTR(x, '  ') = 0` also works (Part 9 Q1 for the mechanics) but is longer.
- **TRIM removes a set of characters, not a substring:** `TRIM('abcba','ab')` gave `'c'` and `TRIM('abab','ab')` gave `''`.
- **Default TRIM strips only spaces:** `TRIM(tab || 'Dev' || tab)` kept length 5. Listing the characters, `TRIM(name, ' ' || char(9) || char(10) || char(13))`, gave 3. NBSP (`char(160)`) also survived `TRIM` (length stayed 3); Q9 and Q33 go deeper.
- **NULL and empty:** `TRIM(NULL)` is NULL, `LENGTH(NULL)` is NULL; `''` and `'   '` clean to `''`, which is not NULL. Decide whether blanks should become NULL (`NULLIF(x, '')` after cleaning).
- **LOWER is ASCII-only in SQLite** (no ICU in this build), so accented capitals are not lowered; see Q33.

**Then explain:**
- Order matters: TRIM first so edge spaces do not leave a marker or a stray space behind, then collapse, then LOWER for the comparison key (keep the cleaned original for display).
- `LENGTH(name) - LENGTH(clean)` is the number of characters removed; a quick way to count dirty rows.
- **pandas differs from SQLite TRIM:** `str.strip()` removes all Unicode whitespace (tabs, newlines and NBSP, which I confirmed by running), and `\s+` also matches those, so the pandas result for customer 6 is `'Dev'` while plain SQL `TRIM` keeps the tabs. To assert equality the Code block first maps tab and newline to a space inside the SQL (the `sql_fair` query), then compares.
- **pandas 3 default:** `str.replace` has `regex=False` by default (my run: the pattern `\s+` without `regex=True` left `'a   b'` unchanged), so a regex must be requested. The name column is the `str` dtype with NaN as the missing marker, and `str.len` returns floats because of the NaN.
- `casefold` is the Unicode-aware lower; SQLite has no equivalent without an extension.
- Other engines have `TRIM`, `BTRIM`, `LTRIM` and regex replace for runs of whitespace (`REGEXP_REPLACE`); not executed here.

**Follow-ups:**
- *How would you do it with a regex in SQL?* SQLite has none built in (Q32); engines that have `REGEXP_REPLACE(name, '\s+', ' ')` do it in one call (not executed here).
- *How do you compare names case-insensitively without changing the data?* `LOWER(a) = LOWER(b)`, or `COLLATE NOCASE` (ASCII only).
- *Should you clean at query time?* No: clean once at load and keep the raw value in a separate column.

**Common mistakes:**
- Assuming `REPLACE(x, '  ', ' ')` once is enough.
- Thinking `TRIM(x, 'ab')` removes the text "ab" from the ends only.
- Expecting `TRIM` to remove tabs, newlines or NBSP.
- Comparing `LENGTH` of raw and clean values for NULL rows and expecting 0 (it is NULL).

### Q3 ⭐⭐⭐ 🟢 Extract the username and domain from email addresses: contacts(name, email, phone) where some emails are NULL, some are blank, one has no '@', one has two '@' and one has trailing spaces. Use INSTR, SUBSTR and LOWER(TRIM(...)) to return username, domain and the top-level part after the last dot (the last dot needs a technique because SQLite has no reverse or split_part: explain one, for example REPLACE tricks or a recursive CTE, and say which is simpler). Count contacts per domain, treating invalid emails as their own 'invalid' bucket (use a simple LIKE '%_@_%._%' check and say it is not full validation). State SPLIT_PART (PostgreSQL), SUBSTRING_INDEX (MySQL) and SUBSTRING with CHARINDEX (SQL Server) as hedged text, not executed. Add the pandas str.split and str.extract versions.
**Asked at:** SQLite lang_corefunc and lang_expr documentation (opened: trim character sets, ASCII-only lower/upper and LIKE, length versus octet_length, concat/concat_ws NULL rules, CAST rules, IS DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL table); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds
**Say this first (1 line):** Normalise with `LOWER(TRIM(email))`, check validity first (NULL, blank, no `@`, two `@`), then use `INSTR` for the `@` and `SUBSTR` on either side; for the part after the last dot, `RTRIM(domain, REPLACE(domain, '.', ''))` is the shortest trick in SQLite, and a recursive CTE is the general (longer) one.

**Schema and sample data:**
```sql
CREATE TABLE contacts(name TEXT, email TEXT, phone TEXT);
INSERT INTO contacts VALUES
 ('Asha',  'Asha.Rao@Example.com', '98765 43210'),
 ('Ben',   'ben@mail.example.co.in', NULL),
 ('Chitra', NULL, NULL),
 ('Dev',   '', NULL),
 ('Esha',  'esha.example.com', NULL),
 ('Farid', 'a@b@c.com', NULL),
 ('Gita',  '  gita@EXAMPLE.com  ', NULL),
 ('Hari',  'hari@example.com', NULL);
```

**SQL answer:** `sql_parse` returns username, domain and tld; `sql_count` counts per domain with an `'invalid'` bucket; `sql_tld_cte` is the recursive alternative.
```sql
WITH c AS (
  SELECT name, LOWER(TRIM(email)) AS e FROM contacts
), v AS (
  SELECT name, e,
         (e LIKE '%_@_%._%' AND LENGTH(e) - LENGTH(REPLACE(e, '@', '')) = 1) AS ok
  FROM c
), p AS (
  SELECT name, e, ok,
         CASE WHEN ok THEN SUBSTR(e, INSTR(e, '@') + 1) END AS domain
  FROM v
)
SELECT name,
       CASE WHEN ok THEN SUBSTR(e, 1, INSTR(e, '@') - 1) END AS username,
       domain,
       CASE WHEN ok THEN SUBSTR(domain, LENGTH(RTRIM(domain, REPLACE(domain, '.', ''))) + 1) END AS tld
FROM p
ORDER BY name
```
The validity test is `e LIKE '%_@_%._%'` plus exactly one `@` (`LENGTH(e) - LENGTH(REPLACE(e, '@', '')) = 1`). It is a shape check, not full validation: it accepts `a@b..c` style oddities and rejects nothing about real mailboxes.

**pandas answer:** `str.extract` with two groups gives username and domain; `str.split("@", expand=True)` also works but returns three columns for the two-`@` row. The last label comes from `rsplit`.
```py
parts = e.str.extract(r"^([^@]+)@([^@]+)$")           # str.extract: columns 0 and 1
p["tld"] = p["domain"].str.rsplit(".", n=1).str[-1]
```

**Example:** `'  gita@EXAMPLE.com  '` becomes `'gita@example.com'` after `LOWER(TRIM())`. `INSTR` finds the `@` at position 5, so `SUBSTR(e, 1, 4)` is `'gita'` and `SUBSTR(e, 6)` is `'example.com'`. For the last dot: `REPLACE('example.com', '.', '')` is `'examplecom'`, whose characters are every non-dot character; `RTRIM('example.com', 'examplecom')` strips trailing characters from that set, stopping at the dot, leaving `'example.'` (8 characters); `SUBSTR(domain, 9)` is `'com'`. Ben's domain `mail.example.co.in` gives `'in'`. Chitra (NULL), Dev (blank), Esha (no `@`) and Farid (two `@`) are invalid, so the counts are invalid 4, example.com 3 (Asha, Gita, Hari) and mail.example.co.in 1.

**Code:** run with `python3 -I`.
```python
# Q3: username, domain, top-level part of emails; invalid bucket; pandas split/extract.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE contacts(name TEXT, email TEXT, phone TEXT);
INSERT INTO contacts VALUES
 ('Asha',  'Asha.Rao@Example.com', '98765 43210'),
 ('Ben',   'ben@mail.example.co.in', NULL),
 ('Chitra', NULL, NULL),
 ('Dev',   '', NULL),
 ('Esha',  'esha.example.com', NULL),
 ('Farid', 'a@b@c.com', NULL),
 ('Gita',  '  gita@EXAMPLE.com  ', NULL),
 ('Hari',  'hari@example.com', NULL);
""")

sql_parse = """
WITH c AS (
  SELECT name, LOWER(TRIM(email)) AS e FROM contacts
), v AS (
  SELECT name, e,
         (e LIKE '%_@_%._%' AND LENGTH(e) - LENGTH(REPLACE(e, '@', '')) = 1) AS ok
  FROM c
), p AS (
  SELECT name, e, ok,
         CASE WHEN ok THEN SUBSTR(e, INSTR(e, '@') + 1) END AS domain
  FROM v
)
SELECT name,
       CASE WHEN ok THEN SUBSTR(e, 1, INSTR(e, '@') - 1) END AS username,
       domain,
       CASE WHEN ok THEN SUBSTR(domain, LENGTH(RTRIM(domain, REPLACE(domain, '.', ''))) + 1) END AS tld
FROM p
ORDER BY name
"""
sql_count = """
WITH c AS (SELECT LOWER(TRIM(email)) AS e FROM contacts), v AS (
  SELECT e, (e LIKE '%_@_%._%' AND LENGTH(e) - LENGTH(REPLACE(e, '@', '')) = 1) AS ok FROM c)
SELECT CASE WHEN ok THEN SUBSTR(e, INSTR(e, '@') + 1) ELSE 'invalid' END AS domain, COUNT(*) AS n
FROM v
GROUP BY 1
ORDER BY n DESC, domain
"""
# the other technique: a recursive CTE that peels one label at a time (same answer, longer)
sql_tld_cte = """
WITH RECURSIVE t(name, rest) AS (
  SELECT name, SUBSTR(LOWER(TRIM(email)), INSTR(LOWER(TRIM(email)), '@') + 1)
  FROM contacts WHERE LOWER(TRIM(email)) LIKE '%_@_%._%'
  UNION ALL
  SELECT name, SUBSTR(rest, INSTR(rest, '.') + 1) FROM t WHERE INSTR(rest, '.') > 0
)
SELECT name, rest AS tld FROM t WHERE INSTR(rest, '.') = 0 ORDER BY name
"""
parsed = pd.read_sql(sql_parse, con)
print(parsed.to_string(index=False)); print()
counts = pd.read_sql(sql_count, con)
print(counts.to_string(index=False)); print()
cte = pd.read_sql(sql_tld_cte, con)
# a@b@c.com passes the LIKE check, so the CTE returns 'com' for Farid where the guarded query returns NULL
print("recursive CTE tld (no two-@ guard):", dict(zip(cte.name, cte.tld)))
no_at = con.execute("SELECT SUBSTR(email, 1, INSTR(email, '@') - 1), SUBSTR(email, INSTR(email, '@') + 1) "
                    "FROM contacts WHERE name = 'Esha'").fetchone()
print("unguarded username and domain for 'esha.example.com' (no @, INSTR = 0):", no_at)

# pandas
df = pd.read_sql("SELECT name, email FROM contacts", con)
e = df["email"].str.strip().str.lower()
ok = e.str.fullmatch(r".+@.+\..+").fillna(False) & (e.str.count("@") == 1)
parts = e.str.extract(r"^([^@]+)@([^@]+)$")           # str.extract: columns 0 and 1
split = e.str.split("@", expand=True)                  # str.split: also works for the two-part rows
p = pd.DataFrame({"name": df.name,
                  "username": parts[0].where(ok),
                  "domain": parts[1].where(ok)})
p["tld"] = p["domain"].str.rsplit(".", n=1).str[-1]
print("\nstr.split(expand=True) column count:", split.shape[1], "(3 because 'a@b@c.com' has two @)")
print(p.to_string(index=False))
p_counts = p["domain"].fillna("invalid").value_counts().rename_axis("domain").reset_index(name="n")
p_counts = p_counts.sort_values(["n", "domain"], ascending=[False, True]).reset_index(drop=True)

pd.testing.assert_frame_equal(parsed.sort_values("name").reset_index(drop=True),
                              p.sort_values("name").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(counts, p_counts, check_dtype=False)
print("asserts passed (parse compared after sorting by name; counts sorted by n desc, domain)")
```

**Output (my run):**
```text
  name username             domain tld
  Asha asha.rao        example.com com
   Ben      ben mail.example.co.in  in
Chitra      NaN                NaN NaN
   Dev      NaN                NaN NaN
  Esha      NaN                NaN NaN
 Farid      NaN                NaN NaN
  Gita     gita        example.com com
  Hari     hari        example.com com

            domain  n
           invalid  4
       example.com  3
mail.example.co.in  1

recursive CTE tld (no two-@ guard): {'Asha': 'com', 'Ben': 'in', 'Farid': 'com', 'Gita': 'com', 'Hari': 'com'}
unguarded username and domain for 'esha.example.com' (no @, INSTR = 0): ('', 'esha.example.com')

str.split(expand=True) column count: 3 (3 because 'a@b@c.com' has two @)
  name username             domain tld
  Asha asha.rao        example.com com
   Ben      ben mail.example.co.in  in
Chitra      NaN                NaN NaN
   Dev      NaN                NaN NaN
  Esha      NaN                NaN NaN
 Farid      NaN                NaN NaN
  Gita     gita        example.com com
  Hari     hari        example.com com
asserts passed (parse compared after sorting by name; counts sorted by n desc, domain)
```

**Edge cases:**
- **No `@`:** `INSTR` returns 0, so the unguarded `SUBSTR(email, 1, INSTR - 1)` is `SUBSTR(email, 1, -1)` and gave `''` for Esha, and the "domain" came back as the whole string. Always guard with the validity flag.
- **Two `@`:** `'a@b@c.com'` passes the simple `LIKE` check. Without the exactly-one-`@` guard the recursive CTE returned `'com'` for Farid; with it Farid is invalid. Real validation is the application's job (or a regex engine).
- **NULL and blank:** `LOWER(TRIM(NULL))` is NULL, and NULL `LIKE` anything is NULL, so the `CASE` falls to the invalid branch; blank fails the pattern. Both go in the invalid bucket.
- **Case:** the domain is lower-cased before grouping, otherwise `Example.com` and `example.com` become two groups. The username is lower-cased here too; in real mail the local part can be case-sensitive, so keep the original if that matters.
- **Subdomains:** `mail.example.co.in` has top-level part `in`; the registrable domain `example.co.in` needs a public-suffix list, not string tricks.

**Then explain:**
- **Which last-dot technique:** the `RTRIM` trick is one expression but needs a sentence to explain; the recursive CTE peels one label at a time until no dot remains, is easy to read and generalises to the nth label, but costs a CTE (recursion mechanics: Part 9 Q1). I use the trick for the last label and the CTE for "any position".
- SQLite has no `REVERSE` or `SPLIT_PART` (Q32), which is why both techniques are needed.
- **Other dialects (not executed here):** PostgreSQL `SPLIT_PART(email, '@', 2)`; MySQL `SUBSTRING_INDEX(email, '@', -1)` (the last piece, and `SUBSTRING_INDEX(domain, '.', -1)` for the last label); SQL Server `SUBSTRING(email, CHARINDEX('@', email) + 1, LEN(email))`.
- **pandas:** `str.split` and `str.extract` both propagate NaN, so NULL emails stay missing; the Code block uses `.where(ok)` so the invalid rows are missing like the SQL `CASE` without ELSE. The assertion compares after sorting by name, NULL equal to NaN.

**Follow-ups:**
- *How would you validate more strictly?* In Python with a regex or a library, or `REGEXP_LIKE` where the engine has it (not executed here); in SQLite register a function (Q32).
- *How do you count contacts per top-level part?* Group by the `tld` expression in the same way, with the same invalid bucket.
- *Why not group by the raw email column?* Case and spaces would split one domain into several groups.

**Common mistakes:**
- Not handling the missing `@`: `INSTR` returns 0 and `SUBSTR` returns a plausible wrong value, not an error.
- Counting invalid rows as a domain called NULL.
- Forgetting `TRIM` and `LOWER` before grouping.
- Treating the `LIKE` shape check as validation.

### Q4 ⭐⭐⭐ 🟡 NULL inside CASE, and COALESCE versus IFNULL versus NULLIF versus IIF: employees(employee_id, name, salary, dept) with NULL salaries and some NULL names. Show that CASE WHEN salary > 50000 THEN 'high' WHEN salary <= 50000 THEN 'low' END returns NULL for NULL salary (the ELSE-less CASE), that CASE salary WHEN NULL THEN ... never matches (use IS NULL in the searched form), and that a NULL condition falls through to ELSE. Then solve the LeetCode 1873 Calculate Special Bonus idea (bonus = salary when employee_id is odd and name does not start with 'M', else 0) with a NULL name present and show the NULL trap in 'name NOT LIKE 'M%''. Compare COALESCE (any number of arguments, standard, first non-NULL), IFNULL (two arguments, SQLite and MySQL), NULLIF(x, 0) for safe division and IIF (SQLite 3.32 and later, also SQL Server) and say which ones are standard. Cross-reference Part 1 Q6 and Part 1 Q44 and do not repeat their content; this question adds the NULL-in-CASE and bonus angle.
**Asked at:** LeetCode public problems via the doocs mirror (opened: 1484 Group Sold Products By The Date, 1795 Rearrange Products Table, 1667 Fix Names in a Table, 1527 Patients With a Condition, 1873 Calculate Special Bonus); public problem bank, not a candidate report; analyst and data scientist screens; SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds
**Say this first (1 line):** A CASE without ELSE returns NULL when no branch is true, a NULL condition is not true so it falls through to the next branch or the ELSE, and `CASE x WHEN NULL` never matches; so put an explicit `IS NULL` branch first and decide on purpose what a NULL name or salary should do.

**Schema and sample data:**
```sql
CREATE TABLE employees(employee_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, dept TEXT);
INSERT INTO employees VALUES
 (1,'Asha',60000,'Eng'),(2,'Meera',40000,'Ops'),(3,'Mohan',50000,'Eng'),(4,NULL,30000,'Ops'),
 (5,NULL,70000,'Eng'),(6,'Zoya',NULL,'Ops'),(7,'Ravi',50000,NULL),(8,'Hema',0,'Eng');
```

**SQL answer:** `sql_band` shows the CASE variants, `sql_bonus_naive` and `sql_bonus` solve the LeetCode 1873 idea, `sql_funcs` compares the NULL functions (all in the Code block). The fixed bonus:
```sql
SELECT employee_id, name, salary,
  CASE WHEN employee_id % 2 = 1 AND COALESCE(name, '') NOT LIKE 'M%' THEN salary ELSE 0 END AS bonus
FROM employees ORDER BY employee_id
```

**pandas answer:** comparisons with NaN are False, so `np.where` hides missing salaries in the else branch; use `np.select` with an `isna` condition first. For the bonus the NaN name counts as "does not start with M".
```py
band_safe = np.select([emp.salary.isna(), emp.salary > 50000], ["unknown", "high"], default="low")
p_bonus = np.where(odd & ~starts_m, emp.salary, 0)               # NaN name counts as 'not M': same as the COALESCE fix
```

**Example:** Zoya (id 6) has a NULL salary. `salary > 50000` and `salary <= 50000` are both UNKNOWN, so the no-ELSE CASE returns NULL; with `ELSE 'not high'` she silently becomes "not high"; `CASE salary WHEN NULL` compares `salary = NULL`, which is never true, so even Zoya gets the ELSE; `IIF(salary > 50000, 'high', 'low')` calls her "low". Only the `salary IS NULL` branch first gives `'unknown'`. For the bonus (odd id and name not starting with M), employee 5 has a NULL name: `NULL NOT LIKE 'M%'` is NULL, so the `AND` is not true, the CASE takes `ELSE 0` and the naive query pays 0 where the "does not start with M" reading says 70000. Employees 1 (60000) and 7 (50000) are odd with a name not starting with M; 3 (Mohan) is odd but starts with M, so 0.

**Code:** run with `python3 -I`.
```python
# Q4: NULL inside CASE, special bonus with a NULL name, COALESCE / IFNULL / NULLIF / IIF.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(employee_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, dept TEXT);
INSERT INTO employees VALUES
 (1,'Asha',60000,'Eng'),(2,'Meera',40000,'Ops'),(3,'Mohan',50000,'Eng'),(4,NULL,30000,'Ops'),
 (5,NULL,70000,'Eng'),(6,'Zoya',NULL,'Ops'),(7,'Ravi',50000,NULL),(8,'Hema',0,'Eng');
""")

def q(sql):
    return pd.read_sql(sql, con)

sql_band = """
SELECT employee_id, salary,
  CASE WHEN salary > 50000 THEN 'high' WHEN salary <= 50000 THEN 'low' END                  AS band_no_else,
  CASE WHEN salary > 50000 THEN 'high' ELSE 'not high' END                                  AS band_else,
  CASE salary WHEN NULL THEN 'is null' ELSE 'never matches' END                              AS simple_case_null,
  CASE WHEN salary IS NULL THEN 'unknown' WHEN salary > 50000 THEN 'high' ELSE 'low' END     AS band_safe,
  IIF(salary > 50000, 'high', 'low')                                                         AS iif_band
FROM employees ORDER BY employee_id
"""
print(q(sql_band).to_string(index=False)); print()

sql_bonus_naive = """
SELECT employee_id, name, salary,
  CASE WHEN employee_id % 2 = 1 AND name NOT LIKE 'M%' THEN salary ELSE 0 END AS bonus
FROM employees ORDER BY employee_id
"""
sql_bonus = """
SELECT employee_id, name, salary,
  CASE WHEN employee_id % 2 = 1 AND COALESCE(name, '') NOT LIKE 'M%' THEN salary ELSE 0 END AS bonus
FROM employees ORDER BY employee_id
"""
naive = q(sql_bonus_naive)
fixed = q(sql_bonus)
print(pd.DataFrame({"employee_id": naive.employee_id, "name": naive.name, "naive_bonus": naive.bonus,
                    "fixed_bonus": fixed.bonus}).to_string(index=False)); print()
print("NULL NOT LIKE 'M%' ->", con.execute("SELECT NULL NOT LIKE 'M%'").fetchone()[0], "(NULL, so the CASE takes ELSE 0)")

sql_funcs = """
SELECT employee_id,
       COALESCE(salary, 0)                  AS coalesce_,
       IFNULL(salary, -1)                   AS ifnull_,
       COALESCE(name, dept, 'n/a')          AS first_non_null,
       100.0 / NULLIF(salary, 0)            AS safe_div,
       salary / 1.0                         AS plain
FROM employees WHERE employee_id IN (1, 4, 6, 7, 8) ORDER BY employee_id
"""
print(q(sql_funcs).to_string(index=False)); print()
print("IFNULL with three arguments:", end=" ")
try:
    con.execute("SELECT IFNULL(NULL, NULL, 3)")
except sqlite3.Error as ex:
    print("error:", ex)
print("100.0 / 0 in SQLite (no NULLIF):", con.execute("SELECT 100.0 / 0").fetchone()[0], "(NULL, not an error)")

# pandas versions
emp = q("SELECT * FROM employees ORDER BY employee_id")
print("\npandas NaN comparisons: salary > 50000 for NaN ->", (emp.salary > 50000)[5])
band_trap = np.where(emp.salary > 50000, "high", "low")           # NaN silently becomes 'low'
band_safe = np.select([emp.salary.isna(), emp.salary > 50000], ["unknown", "high"], default="low")
print("np.where trap for Zoya:", band_trap[5], "| np.select with isna first:", band_safe[5])

odd = emp.employee_id % 2 == 1
starts_m = emp.name.str.startswith("M")
print("name.str.startswith('M') for the NULL name:", starts_m[3], "(pandas 3 str dtype gives False, not NaN)")
p_bonus = np.where(odd & ~starts_m, emp.salary, 0)               # NaN name counts as 'not M': same as the COALESCE fix
p_bonus = pd.Series(p_bonus).fillna(0)  # NaN salary would stay NaN in SQL; see the edge case
pd.testing.assert_series_equal(fixed.bonus.astype(float), p_bonus.astype(float), check_names=False)
assert naive.bonus.tolist() != fixed.bonus.tolist()
assert q(sql_band).band_safe.tolist() == list(band_safe)
print("asserts passed (employee_id order)")
```

**Output (my run):**
```text
 employee_id  salary band_no_else band_else simple_case_null band_safe iif_band
           1 60000.0         high      high    never matches      high     high
           2 40000.0          low  not high    never matches       low      low
           3 50000.0          low  not high    never matches       low      low
           4 30000.0          low  not high    never matches       low      low
           5 70000.0         high      high    never matches      high     high
           6     NaN          NaN  not high    never matches   unknown      low
           7 50000.0          low  not high    never matches       low      low
           8     0.0          low  not high    never matches       low      low

 employee_id  name  naive_bonus  fixed_bonus
           1  Asha        60000        60000
           2 Meera            0            0
           3 Mohan            0            0
           4   NaN            0            0
           5   NaN            0        70000
           6  Zoya            0            0
           7  Ravi        50000        50000
           8  Hema            0            0

NULL NOT LIKE 'M%' -> None (NULL, so the CASE takes ELSE 0)
 employee_id  coalesce_  ifnull_ first_non_null  safe_div   plain
           1      60000    60000           Asha  0.001667 60000.0
           4      30000    30000            Ops  0.003333 30000.0
           6          0       -1           Zoya       NaN     NaN
           7      50000    50000           Ravi  0.002000 50000.0
           8          0        0           Hema       NaN     0.0

IFNULL with three arguments: error: wrong number of arguments to function IFNULL()
100.0 / 0 in SQLite (no NULLIF): None (NULL, not an error)

pandas NaN comparisons: salary > 50000 for NaN -> False
np.where trap for Zoya: low | np.select with isna first: unknown
name.str.startswith('M') for the NULL name: False (pandas 3 str dtype gives False, not NaN)
asserts passed (employee_id order)
```

**Edge cases:**
- **NULL name is a business decision.** LeetCode 1873 has no NULL names. If a missing name should count as "not starting with M", use `COALESCE(name, '') NOT LIKE 'M%'` (employee 5 gets 70000); if unknown should not be paid, keep the naive form and say so. Either way write it down: the naive form decides by accident.
- **NULL salary on an odd id** would make the bonus NULL, not 0, because the THEN branch returns the NULL salary; wrap it in `COALESCE(salary, 0)` if the output must be a number. (In the Code block pandas is compared after `fillna(0)`, which matters only for that case; this sample has no such row, so nothing changes.)
- **Division:** `100.0 / NULLIF(salary, 0)` is NULL for salary 0 (Hema) and for the NULL salary (Zoya). SQLite returns NULL for `100.0 / 0` even without NULLIF (my run), but PostgreSQL, SQL Server and others raise a division-by-zero error (from memory, not executed here), so the NULLIF is the portable habit.
- **IIF and ELSE-less branches:** `IIF(cond, a, b)` is `CASE WHEN cond THEN a ELSE b END`, so a NULL condition goes to `b`, the same trap.

**Then explain:**
- **Which are standard:** `CASE` and `COALESCE` and `NULLIF` are standard SQL. `IFNULL` is a two-argument SQLite and MySQL function (three arguments gave "wrong number of arguments" on SQLite 3.45.1). `IIF` exists in SQLite (3 arguments used here on 3.45.1), SQL Server and some others, but is not standard. I would write `CASE` in a portable answer.
- **COALESCE** returns the first non-NULL of any number of arguments (`COALESCE(name, dept, 'n/a')` gave `Ops` for employee 4, whose name is NULL). It is the answer to "replace NULL with a default".
- **NULLIF(x, y)** returns NULL when x = y, else x; its main use is the safe-division and "turn a blank or zero into NULL" tool.
- **pandas:** the NaN comparison is False, not UNKNOWN, so the "high / low" split with `np.where` puts NaN in "low" (my run) and a three-way `np.select` with `isna` first is the fix. `Series.str.startswith('M')` returned False for the missing name in the pandas 3 `str` dtype, so `~starts_m` is True and the pandas bonus matches the `COALESCE` version, not the naive one.
- Cross-reference: COALESCE and NULLIF basics are in Part 1 Q6 and CASE subtleties in Part 1 Q44; this question adds the NULL-in-CASE and bonus angle.

**Follow-ups:**
- *How would you return 'unknown' for NULL?* An explicit `WHEN salary IS NULL` branch first.
- *Why does `CASE salary WHEN NULL` fail?* It expands to `salary = NULL`, which is UNKNOWN.
- *Would `salary <= 50000` as the second branch be needed if there is an ELSE?* No, but the ELSE then also catches NULL; that is exactly the trap.

**Common mistakes:**
- `name NOT LIKE 'M%'` on a nullable column, thinking NULL means "does not match".
- `CASE col WHEN NULL`.
- Relying on ELSE to mean "everything else" when NULLs are present.
- Using `IFNULL` or `IIF` in a portable answer.

### Q5 ⭐⭐⭐ 🟡 Unpivot survey columns (wide to long): survey(user_id, q1, q2, q3) with integer ratings 1 to 5 and NULL for unanswered questions. Return (user_id, question, rating) with one row per answered question, first with UNION ALL (the LeetCode 1795 Rearrange Products Table shape, where NULL prices are dropped) and then with CROSS JOIN over a VALUES list that picks the column with CASE, so the table is scanned once. Say which one is better for many columns and why UNION (not ALL) is risky (it removes legitimate duplicates). Say SQLite has no UNPIVOT, then describe SQL Server, Oracle, Snowflake and BigQuery UNPIVOT (and that UNPIVOT drops NULLs by default, with options to keep them) as hedged text, not executed. Add the pandas melt version with dropna and state the row order.
**Asked at:** LeetCode public problems via the doocs mirror (opened: 1484 Group Sold Products By The Date, 1795 Rearrange Products Table, 1667 Fix Names in a Table, 1527 Patients With a Condition, 1873 Calculate Special Bonus); public problem bank, not a candidate report; analyst and data scientist screens; SQL pivot guides (datadriven.io, DataVidhya, Educative and a Medium write-up, search snippets only; the DataVidhya lesson page opened but showed only its introduction: CASE inside SUM or COUNT, dynamic pivot, NULL categories); guides, not candidate reports; analyst and data engineer rounds at product companies and GCCs
**Say this first (1 line):** SQLite has no UNPIVOT, so wide to long is one `SELECT` per column glued with `UNION ALL` (never plain `UNION`), or a `CROSS JOIN` with a `VALUES` list of column names and a `CASE` that picks the column, which reads the table once; either way add `WHERE rating IS NOT NULL` to drop unanswered questions.

**Schema and sample data:**
```sql
CREATE TABLE survey(user_id INTEGER PRIMARY KEY, q1 INTEGER, q2 INTEGER, q3 INTEGER);
INSERT INTO survey VALUES (1,5,3,NULL),(2,NULL,NULL,NULL),(3,4,4,4),(4,2,NULL,5);
```

**SQL answer:** `sql_union_all` and `sql_cross` are in the Code block and returned the same 7 rows.
```sql
SELECT user_id, 'q1' AS question, q1 AS rating FROM survey WHERE q1 IS NOT NULL
UNION ALL
SELECT user_id, 'q2', q2 FROM survey WHERE q2 IS NOT NULL
UNION ALL
SELECT user_id, 'q3', q3 FROM survey WHERE q3 IS NOT NULL
ORDER BY question, user_id
```
```sql
WITH qs(question) AS (VALUES ('q1'), ('q2'), ('q3')),
long AS (
  SELECT s.user_id, qs.question,
         CASE qs.question WHEN 'q1' THEN s.q1 WHEN 'q2' THEN s.q2 WHEN 'q3' THEN s.q3 END AS rating
  FROM survey s CROSS JOIN qs
)
SELECT user_id, question, rating FROM long WHERE rating IS NOT NULL
ORDER BY question, user_id
```

**pandas answer:** `melt` plus `dropna`.
```py
melted = survey.melt(id_vars="user_id", value_vars=["q1", "q2", "q3"], var_name="question", value_name="rating")
p = melted.dropna(subset=["rating"]).reset_index(drop=True)
```

**Example:** user 1 answered q1 = 5 and q2 = 3 (q3 is NULL): two rows. User 2 answered nothing: no rows (they vanish from the long table, which matters if you count respondents). User 3 gave 4, 4, 4: three rows. User 4 answered q1 = 2 and q3 = 5: two rows. Total 2 + 0 + 3 + 2 = 7. Without the NULL filter the same query returns 12 rows (4 users times 3 questions).

**Code:** run with `python3 -I`.
```python
# Q5: unpivot survey columns: UNION ALL, CROSS JOIN over VALUES, pandas melt.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE survey(user_id INTEGER PRIMARY KEY, q1 INTEGER, q2 INTEGER, q3 INTEGER);
INSERT INTO survey VALUES (1,5,3,NULL),(2,NULL,NULL,NULL),(3,4,4,4),(4,2,NULL,5);
""")

sql_union_all = """
SELECT user_id, 'q1' AS question, q1 AS rating FROM survey WHERE q1 IS NOT NULL
UNION ALL
SELECT user_id, 'q2', q2 FROM survey WHERE q2 IS NOT NULL
UNION ALL
SELECT user_id, 'q3', q3 FROM survey WHERE q3 IS NOT NULL
ORDER BY question, user_id
"""
sql_cross = """
WITH qs(question) AS (VALUES ('q1'), ('q2'), ('q3')),
long AS (
  SELECT s.user_id, qs.question,
         CASE qs.question WHEN 'q1' THEN s.q1 WHEN 'q2' THEN s.q2 WHEN 'q3' THEN s.q3 END AS rating
  FROM survey s CROSS JOIN qs
)
SELECT user_id, question, rating FROM long WHERE rating IS NOT NULL
ORDER BY question, user_id
"""
# UNION (not ALL) over (user_id, rating) only: legitimate duplicates vanish
sql_union_bad = """
SELECT user_id, q1 AS rating FROM survey WHERE q1 IS NOT NULL
UNION SELECT user_id, q2 FROM survey WHERE q2 IS NOT NULL
UNION SELECT user_id, q3 FROM survey WHERE q3 IS NOT NULL
"""
sql_union_all_bad = sql_union_bad.replace("UNION SELECT", "UNION ALL SELECT")

a = pd.read_sql(sql_union_all, con)
b = pd.read_sql(sql_cross, con)
print(a.to_string(index=False)); print()
assert a.equals(b)
print("rows kept: UNION ALL %d, CROSS JOIN %d" % (len(a), len(b)))
print("UNION on (user_id, rating): %d rows; UNION ALL on the same: %d rows (user 3 gave 4,4,4)" % (
    len(con.execute(sql_union_bad).fetchall()), len(con.execute(sql_union_all_bad).fetchall())))
print("keeping unanswered rows: %d rows when the IS NOT NULL filter is dropped" % len(con.execute(
    sql_cross.replace("WHERE rating IS NOT NULL", "")).fetchall()))

for label, sql in (("UNION ALL", sql_union_all), ("CROSS JOIN", sql_cross)):
    plan = [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]
    print(label, "plan:", plan)

# pandas
survey = pd.read_sql("SELECT * FROM survey", con)
melted = survey.melt(id_vars="user_id", value_vars=["q1", "q2", "q3"], var_name="question", value_name="rating")
print("\nmelt keeps NaN rows:", len(melted), "rows; after dropna:", end=" ")
p = melted.dropna(subset=["rating"]).reset_index(drop=True)
print(len(p))
print("melt row order (before sorting): question blocks in column order, users inside each block")
print(melted.head(5).to_string(index=False))
p["rating"] = p["rating"].astype(int)
# compare after sorting by (question, user_id)
p = p.sort_values(["question", "user_id"]).reset_index(drop=True)
pd.testing.assert_frame_equal(a, p[["user_id", "question", "rating"]], check_dtype=False)
print("asserts passed (compared after sorting by question, user_id)")
```

**Output (my run):**
```text
 user_id question  rating
       1       q1       5
       3       q1       4
       4       q1       2
       1       q2       3
       3       q2       4
       3       q3       4
       4       q3       5

rows kept: UNION ALL 7, CROSS JOIN 7
UNION on (user_id, rating): 5 rows; UNION ALL on the same: 7 rows (user 3 gave 4,4,4)
keeping unanswered rows: 12 rows when the IS NOT NULL filter is dropped
UNION ALL plan: ['MERGE (UNION ALL)', 'LEFT', 'MERGE (UNION ALL)', 'LEFT', 'SCAN survey', 'USE TEMP B-TREE FOR ORDER BY', 'RIGHT', 'SCAN survey', 'USE TEMP B-TREE FOR ORDER BY', 'RIGHT', 'SCAN survey', 'USE TEMP B-TREE FOR ORDER BY']
CROSS JOIN plan: ['MATERIALIZE qs', 'SCAN 3 CONSTANT ROWS', 'SCAN s', 'SCAN qs', 'USE TEMP B-TREE FOR ORDER BY']

melt keeps NaN rows: 12 rows; after dropna: 7
melt row order (before sorting): question blocks in column order, users inside each block
 user_id question  rating
       1       q1     5.0
       2       q1     NaN
       3       q1     4.0
       4       q1     2.0
       1       q2     3.0
asserts passed (compared after sorting by question, user_id)
```

**Edge cases:**
- **NULL ratings:** the filter drops them (the LeetCode 1795 Rearrange Products Table shape drops NULL prices the same way). Keep them if "not answered" must be visible; then also keep a respondent with no answers (user 2).
- **UNION versus UNION ALL:** `UNION` removes duplicate rows. If the select list does not include the question label, legitimate repeats vanish: on `(user_id, rating)` only, `UNION` gave 5 rows where `UNION ALL` gave 7, because user 3's three 4s collapsed into one. With the question label in the select list the rows differ, so it does no harm here, but it adds a sort or hash and the risk is not worth it.
- **Mixed types:** every branch must produce one type for `rating`; mixing text and numbers in one CASE gives a column with mixed types in SQLite (no error), which breaks the average later.
- **Duplicate user rows:** if `survey` had two rows for a user, both would unpivot; the key is assumed unique.

**Then explain:**
- **Which is better for many columns:** the `VALUES` form lists each column name once in the CASE and once in the VALUES list, and `EXPLAIN QUERY PLAN` showed one `SCAN s` against three `SCAN survey` lines for the `UNION ALL` form (SQLite 3.45.1; the plan text is engine-specific). With 50 columns, `UNION ALL` is 50 repeated scans of the same table, so the `CROSS JOIN VALUES` form is shorter and scans once. The `CASE` is still long to write; generate it in code (Q31).
- **Dialects (not executed here):** SQL Server, Oracle, Snowflake and BigQuery have `UNPIVOT`, written like `UNPIVOT (rating FOR question IN (q1, q2, q3))`; from memory it drops NULL values by default, and Oracle and Snowflake, from memory, have an option to include NULLs (`INCLUDE NULLS`). Check your engine's documentation. PostgreSQL and MySQL have no keyword; PostgreSQL's `CROSS JOIN LATERAL (VALUES ...)` is the usual form. SQLite and MySQL use the forms above.
- **pandas:** `melt` keeps NaN rows (12 rows) until you `dropna` (7 rows). Its row order is column by column: all q1 rows first (users in table order), then q2, then q3, which is why the SQL result is ordered by `question, user_id` before comparing. The ratings come out as float because of the NaN; the Code block casts them to int and compares after sorting by `(question, user_id)`.
- `melt` is the inverse of the pivot in Q6.

**Follow-ups:**
- *How do you keep user 2?* Skip the `IS NOT NULL` filter and filter in the report, or `LEFT JOIN` the users table to the long table.
- *How would you get an average per question?* `GROUP BY question` on the long table: `AVG` skips NULLs, so you can even leave the filter out.
- *Why is the UNION ALL form still common?* It is the simplest to read and works on every engine.

**Common mistakes:**
- Using `UNION` and losing rows.
- Forgetting that NULLs become rows, then counting 12 answers when 7 exist.
- Mixing types between branches.
- Assuming the output order: neither SQL form guarantees it without an `ORDER BY`.

### Q6 ⭐⭐⭐ 🟡 Long to wide: answers(user_id, question, answer) in long format where answer is text ('Yes', 'No', 'Maybe') and some users skipped some questions, plus the question list ('q1', 'q2', 'q3'). Return one row per user with one column per question using MAX(CASE WHEN question = 'q1' THEN answer END). Explain why MAX is used for text, what happens when a user has two rows for the same question (silently picks the larger string, a data bug that should be checked with HAVING COUNT(*) > 1), and why missing answers come out as NULL. Add the pandas pivot version, show that pivot raises ValueError on duplicate (user, question) pairs while pivot_table(aggfunc='first') does not, and reset_index and columns.name cleanup.
**Asked at:** SQL pivot guides (datadriven.io, DataVidhya, Educative and a Medium write-up, search snippets only; the DataVidhya lesson page opened but showed only its introduction: CASE inside SUM or COUNT, dynamic pivot, NULL categories); guides, not candidate reports; analyst and data engineer rounds at product companies and GCCs; pandas user guide pages on reshaping and on working with text data (opened: pivot, pivot_table, melt, wide_to_long, stack, unstack, crosstab, explode, string dtype and the .str accessor); official documentation, not candidate reports; data scientist and analyst rounds
**Say this first (1 line):** One row per user with `MAX(CASE WHEN question = 'q1' THEN answer END)` per question; `MAX` is only a way to pick the single value, so a user with two rows for the same question silently gets the alphabetically larger answer, which is a data bug to catch with `HAVING COUNT(*) > 1`.

**Schema and sample data:**
```sql
CREATE TABLE answers(user_id INTEGER, question TEXT, answer TEXT);
INSERT INTO answers VALUES
 (1,'q1','Yes'),(1,'q2','No'),(1,'q3','Maybe'),
 (2,'q1','No'),(2,'q3','Yes'),
 (3,'q2','Maybe'),
 (4,'q1','No'),(4,'q1','Yes'),(4,'q2','Yes');   -- user 4 answered q1 twice (a data bug)
```

**SQL answer:** `sql_wide` pivots; `sql_dups` finds the duplicates.
```sql
SELECT user_id,
       MAX(CASE WHEN question = 'q1' THEN answer END) AS q1,
       MAX(CASE WHEN question = 'q2' THEN answer END) AS q2,
       MAX(CASE WHEN question = 'q3' THEN answer END) AS q3
FROM answers
GROUP BY user_id
ORDER BY user_id
```
```sql
SELECT user_id, question, COUNT(*) AS n FROM answers GROUP BY user_id, question HAVING COUNT(*) > 1
```

**pandas answer:** `pivot` for clean data, `pivot_table` with an explicit `aggfunc` when duplicates exist, then clean up the index and column-axis name.
```py
answers.pivot(index="user_id", columns="question", values="answer")
out = answers.pivot_table(index="user_id", columns="question", values="answer", aggfunc=how)
return out.reset_index().rename_axis(columns=None)
```

**Example:** user 1 has all three: Yes, No, Maybe. User 2 skipped q2, so the q2 `CASE` is NULL for both of that user's rows and `MAX` of nothing but NULL is NULL. User 3 has only q2: q1 and q3 are NULL. User 4 has q1 twice, 'No' and 'Yes': `MAX` of the strings picks `'Yes'` because `'Yes' > 'No'` in text order, and the other answer disappears without an error (the same query with `MIN` gave `'No'`).

**Code:** run with `python3 -I`.
```python
# Q6: long to wide with MAX(CASE) for text answers; duplicates; pandas pivot vs pivot_table.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE answers(user_id INTEGER, question TEXT, answer TEXT);
INSERT INTO answers VALUES
 (1,'q1','Yes'),(1,'q2','No'),(1,'q3','Maybe'),
 (2,'q1','No'),(2,'q3','Yes'),
 (3,'q2','Maybe'),
 (4,'q1','No'),(4,'q1','Yes'),(4,'q2','Yes');   -- user 4 answered q1 twice (a data bug)
""")

sql_wide = """
SELECT user_id,
       MAX(CASE WHEN question = 'q1' THEN answer END) AS q1,
       MAX(CASE WHEN question = 'q2' THEN answer END) AS q2,
       MAX(CASE WHEN question = 'q3' THEN answer END) AS q3
FROM answers
GROUP BY user_id
ORDER BY user_id
"""
sql_dups = """
SELECT user_id, question, COUNT(*) AS n FROM answers GROUP BY user_id, question HAVING COUNT(*) > 1
"""
sql_min = sql_wide.replace("MAX(", "MIN(")

wide = pd.read_sql(sql_wide, con)
print(wide.to_string(index=False)); print()
print("duplicate (user, question) pairs:", con.execute(sql_dups).fetchall())
print("same query with MIN, user 4 q1:", pd.read_sql(sql_min, con).set_index("user_id").loc[4, "q1"],
      "(MAX gave", wide.set_index("user_id").loc[4, "q1"] + ")")

# pandas
answers = pd.read_sql("SELECT * FROM answers", con)
try:
    answers.pivot(index="user_id", columns="question", values="answer")
except ValueError as ex:
    print("\npivot with duplicates -> ValueError:", ex)

clean = answers[answers.user_id != 4]
p_clean = (clean.pivot(index="user_id", columns="question", values="answer")
           .reset_index().rename_axis(columns=None))
print("pivot on the clean rows:"); print(p_clean.to_string(index=False))

def pt(how):
    out = answers.pivot_table(index="user_id", columns="question", values="answer", aggfunc=how)
    return out.reset_index().rename_axis(columns=None)

p_first = pt("first")
p_max = pt("max")
print("\npivot_table aggfunc='first', user 4 q1:", p_first.set_index("user_id").loc[4, "q1"], "(first row in the data: 'No')")
print("pivot_table aggfunc='max',   user 4 q1:", p_max.set_index("user_id").loc[4, "q1"])

# compare after sorting by user_id; NULL in SQL = NaN in pandas
pd.testing.assert_frame_equal(wide, p_max, check_dtype=False)
assert not wide.equals(p_first)                       # 'first' and MAX disagree on user 4
print("columns.name after pivot (before rename_axis):", answers.pivot_table(
    index="user_id", columns="question", values="answer", aggfunc="max").columns.name)
print("user 3 has no q1 and no q3 -> missing cells:", wide.set_index("user_id").loc[3].tolist())
print("asserts passed (compared in user_id order)")
```

**Output (my run):**
```text
 user_id  q1    q2    q3
       1 Yes    No Maybe
       2  No   NaN   Yes
       3 NaN Maybe   NaN
       4 Yes   Yes   NaN

duplicate (user, question) pairs: [(4, 'q1', 2)]
same query with MIN, user 4 q1: No (MAX gave Yes)

pivot with duplicates -> ValueError: Index contains duplicate entries, cannot reshape
pivot on the clean rows:
 user_id  q1    q2    q3
       1 Yes    No Maybe
       2  No   NaN   Yes
       3 NaN Maybe   NaN

pivot_table aggfunc='first', user 4 q1: No (first row in the data: 'No')
pivot_table aggfunc='max',   user 4 q1: Yes
columns.name after pivot (before rename_axis): question
user 3 has no q1 and no q3 -> missing cells: [nan, 'Maybe', nan]
asserts passed (compared in user_id order)
```

**Edge cases:**
- **Why MAX works for text:** `MAX` and `MIN` accept text (they compare as strings) and ignore NULLs, so with exactly one non-NULL row per user and question they return that row's answer. `SUM` would not work on text.
- **Duplicates:** `MAX` picks the larger string, `MIN` the smaller; neither is "the latest answer". If a timestamp exists, select by it (a window function, Parts 4 and 5), or reject the data. Run the `HAVING COUNT(*) > 1` check first.
- **Missing answers are NULL** because the `CASE` without `ELSE` gives NULL and `MAX` ignores it; in pandas they are NaN.
- **A user with no answer rows** is absent from both results; start from a users table and `LEFT JOIN` to keep them.
- **Case differences** ('yes' versus 'Yes') are different strings; clean them first (Q2).

**Then explain:**
- **pandas `pivot` is strict:** with the duplicate (4, q1) it raised `ValueError: Index contains duplicate entries, cannot reshape` (my run), which is a useful data-quality alarm. `pivot_table` aggregates instead of failing, so it hides the problem unless you check duplicates first.
- **`aggfunc` matters:** `pivot_table(aggfunc="first")` gave `'No'` for user 4 (the first row in the data) while SQL `MAX` gave `'Yes'`, and the Code block asserts that they differ; `aggfunc="max"` equals the SQL result, and the assert compares after sorting by user_id with NaN equal to NULL.
- **Cleanup:** after `pivot` the column axis has a name (`question`); `reset_index()` and `rename_axis(columns=None)` give a plain table like the SQL result.
- **Dialects (not executed here):** SQL Server, Oracle, Snowflake and BigQuery have `PIVOT (MAX(answer) FOR question IN ('q1','q2','q3'))`; they also need the aggregate, for the same duplicate reason.

**Follow-ups:**
- *How would you keep the latest answer?* Rank rows per (user, question) by timestamp and keep rank 1, then pivot.
- *What about numeric answers?* `MAX(CASE ...)` works the same; `SUM(CASE ...)` would double-count a duplicate instead of hiding it.
- *Why not `GROUP_CONCAT`?* To show all answers when there are duplicates (Q17).

**Common mistakes:**
- Using `MAX` on a data bug and trusting the result.
- Using `pivot_table` and never discovering duplicates.
- Forgetting that users without any rows disappear.
- Leaving the `question` axis name on the pandas result.

### Q7 ⭐⭐⭐ 🟡 LIKE, wildcards and ESCAPE: products(product_id, name) with names such as '100% Cotton', 'cotton_blend', 'Cotton Shirt', 'COTTON' and 'pure cotton'. Write filters that (a) match names containing the literal text '100%' (ESCAPE clause), (b) match the literal underscore in 'cotton_blend' without matching 'cotton blend', (c) are case-insensitive and then case-sensitive (SQLite LIKE is ASCII case-insensitive, GLOB is case-sensitive, PRAGMA case_sensitive_like), (d) start with 'cotton' or contain the word after a space (the LeetCode 1527 Patients With a Condition pattern 'DIAB1%' OR '% DIAB1%'), and show why LIKE '%cotton%' also matches 'cottonwood'. Show that backslash is not the default escape character. Mention that a leading wildcard cannot use an ordinary index (point to Part 11 for query plans) and that PostgreSQL has ILIKE and MySQL LIKE depends on collation (hedged, not executed).
**Asked at:** LeetCode public problems via the doocs mirror (opened: 1484 Group Sold Products By The Date, 1795 Rearrange Products Table, 1667 Fix Names in a Table, 1527 Patients With a Condition, 1873 Calculate Special Bonus); public problem bank, not a candidate report; analyst and data scientist screens; SQLite lang_corefunc and lang_expr documentation (opened: trim character sets, ASCII-only lower/upper and LIKE, length versus octet_length, concat/concat_ws NULL rules, CAST rules, IS DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL table); official documentation, not candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** `%` and `_` are wildcards, so to match them literally you need `ESCAPE` (there is no default escape character, not even backslash); SQLite `LIKE` is case-insensitive for ASCII, `GLOB` is case-sensitive and uses `*`, `?` and `[...]`, and `LIKE '%cotton%'` also matches `cottonwood` because it matches text, not words.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO products VALUES
 (1,'100% Cotton'),(2,'cotton_blend'),(3,'Cotton Shirt'),(4,'COTTON'),(5,'pure cotton'),
 (6,'cotton blend'),(7,'cottonwood table'),(8,'1000 Cotton');
```
(The question lists five names; I added three to show the traps: `'cotton blend'` with a space, `'cottonwood table'` and `'1000 Cotton'`.)

**SQL answer:** the filters are the `sql` dictionary in the Code block; the key ones:
```sql
name LIKE '%100\%%' ESCAPE '\'            -- (a) literal percent sign
name LIKE '%cotton\_blend%' ESCAPE '\'    -- (b) literal underscore
name LIKE '%cotton%'                       -- (c) case-insensitive (ASCII)
name GLOB '*cotton*'                       -- (c) case-sensitive
name LIKE 'cotton' OR name LIKE 'cotton %' OR name LIKE '% cotton' OR name LIKE '% cotton %'   -- (d) whole word
```

**pandas answer:** `str.contains` with `regex=False` for literals, `case=False` for case-insensitive, and a regex for word boundaries.
```py
 "a_literal_percent":    pid(n.str.contains("100%", regex=False)),
 "c_like_default":       pid(n.str.contains("cotton", case=False)),
 "d_whole_word":         pid(n.str.contains(r"(?:^|\s)cotton(?:\s|$)", case=False)),
```

**Example:** (a) `'%100\%%' ESCAPE '\'` means "contains 100 followed by a literal percent sign": only id 1. The unescaped `'%100%%'` is "contains 100": ids 1 and 8 (`'1000 Cotton'`). (b) With `\_` only `'cotton_blend'` (id 2) matches; the plain `_` also matches `'cotton blend'` (id 6) because `_` is any one character. (c) `LIKE '%cotton%'` matches all 8 rows (it ignores ASCII case); `GLOB '*cotton*'` matches ids 2, 5, 6 and 7, the ones with lower-case `cotton`. (d) `LIKE 'cotton%' OR LIKE '% cotton%'` also matches everything here, including `cottonwood`; the whole-word version gives ids 1, 3, 4, 5, 6, 8: not `cotton_blend` (an underscore is not a space) and not `cottonwood table`.

**Code:** run with `python3 -I`.
```python
# Q7: LIKE, wildcards, ESCAPE, GLOB, case_sensitive_like; pandas str.contains.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO products VALUES
 (1,'100% Cotton'),(2,'cotton_blend'),(3,'Cotton Shirt'),(4,'COTTON'),(5,'pure cotton'),
 (6,'cotton blend'),(7,'cottonwood table'),(8,'1000 Cotton');
""")

def ids(where, params=()):
    return [r[0] for r in con.execute(f"SELECT product_id FROM products WHERE {where} ORDER BY product_id", params)]

sql = {
 "a_literal_percent":      r"name LIKE '%100\%%' ESCAPE '\'",
 "a_unescaped_percent":    "name LIKE '%100%%'",
 "a_backslash_no_escape":  r"name LIKE '%100\%%'",
 "b_literal_underscore":   r"name LIKE '%cotton\_blend%' ESCAPE '\'",
 "b_unescaped_underscore": "name LIKE '%cotton_blend%'",
 "c_like_default":         "name LIKE '%cotton%'",
 "c_glob":                 "name GLOB '*cotton*'",
 "d_prefix_or_word":       "name LIKE 'cotton%' OR name LIKE '% cotton%'",
 "d_whole_word":           "name LIKE 'cotton' OR name LIKE 'cotton %' OR name LIKE '% cotton' OR name LIKE '% cotton %'",
}
res = {k: ids(v) for k, v in sql.items()}
for k, v in res.items():
    print(f"{k:24s} {v}")

# PRAGMA case_sensitive_like is deprecated but works on 3.45.1: it changes LIKE for the whole connection
con.execute("PRAGMA case_sensitive_like = ON")
csl = ids("name LIKE '%cotton%'")
print("\nwith PRAGMA case_sensitive_like = ON, LIKE '%cotton%':", csl)
con.execute("PRAGMA case_sensitive_like = OFF")
print("after turning it OFF again:                       ", ids("name LIKE '%cotton%'"))

# an index on name is not used for a leading wildcard
con.execute("CREATE INDEX ix_name ON products(name)")
for label, where in (("name = 'COTTON'", "name = 'COTTON'"), ("LIKE '%cotton%'", "name LIKE '%cotton%'")):
    plan = [r[3] for r in con.execute(f"EXPLAIN QUERY PLAN SELECT * FROM products WHERE {where}")]
    print(f"plan for {label:16s}", plan)

# pandas: str.contains is regex and case-sensitive by default; regex=False for a literal
df = pd.read_sql("SELECT * FROM products ORDER BY product_id", con)
n = df["name"]
def pid(mask): return df.loc[mask, "product_id"].tolist()
p = {
 "a_literal_percent":    pid(n.str.contains("100%", regex=False)),
 "b_literal_underscore": pid(n.str.contains("cotton_blend", regex=False)),
 "b_unescaped_underscore": pid(n.str.contains("cotton.blend", regex=True)),
 "c_like_default":       pid(n.str.contains("cotton", case=False)),
 "c_glob":               pid(n.str.contains("cotton")),            # default: case-sensitive
 "d_prefix_or_word":     pid(n.str.contains(r"^cotton|\scotton", case=False)),
 "d_whole_word":         pid(n.str.contains(r"(?:^|\s)cotton(?:\s|$)", case=False)),
}
print("\npandas str.contains('100%') regex=True also works because % is not special:",
      pid(n.str.contains("100%")) == res["a_literal_percent"])
for k, v in p.items():
    print(f"pandas {k:24s} {v}")
for k, v in p.items():
    assert v == res[k], k
assert csl == res["c_glob"]            # case-sensitive LIKE equals GLOB here
assert res["a_unescaped_percent"] == [1, 8] and res["a_backslash_no_escape"] == []
assert 7 in res["c_like_default"] and 7 not in res["d_whole_word"]
print("asserts passed (id lists compared in product_id order)")
```

**Output (my run):**
```text
a_literal_percent        [1]
a_unescaped_percent      [1, 8]
a_backslash_no_escape    []
b_literal_underscore     [2]
b_unescaped_underscore   [2, 6]
c_like_default           [1, 2, 3, 4, 5, 6, 7, 8]
c_glob                   [2, 5, 6, 7]
d_prefix_or_word         [1, 2, 3, 4, 5, 6, 7, 8]
d_whole_word             [1, 3, 4, 5, 6, 8]

with PRAGMA case_sensitive_like = ON, LIKE '%cotton%': [2, 5, 6, 7]
after turning it OFF again:                        [1, 2, 3, 4, 5, 6, 7, 8]
plan for name = 'COTTON'  ['SEARCH products USING COVERING INDEX ix_name (name=?)']
plan for LIKE '%cotton%'  ['SCAN products']

pandas str.contains('100%') regex=True also works because % is not special: True
pandas a_literal_percent        [1]
pandas b_literal_underscore     [2]
pandas b_unescaped_underscore   [2, 6]
pandas c_like_default           [1, 2, 3, 4, 5, 6, 7, 8]
pandas c_glob                   [2, 5, 6, 7]
pandas d_prefix_or_word         [1, 2, 3, 4, 5, 6, 7, 8]
pandas d_whole_word             [1, 3, 4, 5, 6, 8]
asserts passed (id lists compared in product_id order)
```

**Edge cases:**
- **Backslash is not the default escape:** `LIKE '%100\%%'` without `ESCAPE` returned no rows (the backslash is just a character, and then `%` is a wildcard). You must write `ESCAPE '\'` (or another character, such as `ESCAPE '!'`).
- **`PRAGMA case_sensitive_like = ON`** made `LIKE '%cotton%'` return ids 2, 5, 6, 7, the same as `GLOB`, on SQLite 3.45.1 (my run). It is a setting for the whole connection, off by default, and documented as deprecated from memory (not verified in the docs here), so do not rely on it; I turned it off again and the result returned to 8 rows.
- **ASCII only:** `LIKE` case-folding covers only ASCII letters, so `'Ä' LIKE 'ä'` is false (checked in the Wave A notes).
- **NULL:** `NULL LIKE '%x%'` is NULL, so NULL names are never returned and `NOT LIKE` does not return them either (Q4).
- **The LeetCode 1527 pattern** (`conditions LIKE 'DIAB1%' OR conditions LIKE '% DIAB1%'`) finds a code at the start of the text or after a space, but also matches `DIAB100`, because it checks only the start; add a trailing space or end-of-text test for an exact code.

**Then explain:**
- **Index use:** a leading wildcard (`'%cotton%'`) cannot use an ordinary index: my `EXPLAIN QUERY PLAN` showed `SCAN products` for it and a `SEARCH ... USING COVERING INDEX` for an equality. Plans and `LIKE 'prefix%'` index rules are Part 11.
- **LIKE versus GLOB:** `GLOB` is case-sensitive and Unix-style (`*`, `?`, `[a-z]`, `[^0-9]`); it has no escape clause (a literal `*` goes in brackets, `[*]`).
- **pandas differs:** `str.contains` is case-sensitive and regex by default (`.` matches anything, so `cotton.blend` matched both `cotton_blend` and `cotton blend`); there is no `LIKE`, so `regex=False` for a literal and `case=False` for case-insensitive. The Code block asserts the id lists equal the SQL ones in `product_id` order; the default `str.contains("cotton")` equals `GLOB`, and `case=False` equals `LIKE`.
- **Other engines (hedged, not executed here):** PostgreSQL `LIKE` is case-sensitive and has `ILIKE`; MySQL `LIKE` depends on the column collation (case-insensitive for the common default collations, from memory); both use backslash as the default escape in the usual settings, which differs from SQLite.

**Follow-ups:**
- *How do you match a whole word?* Pad with spaces, `' ' || name || ' ' LIKE '% cotton %'`, which handles start and end in one test (punctuation still breaks it); or a regex where available.
- *Why can a case-insensitive search be slow?* `LOWER(name) LIKE ...` hides the column from a plain index (Q9, Part 11).
- *Why did `100%` match 1000 Cotton?* Without escaping, `%` means "any characters".

**Common mistakes:**
- Searching for `'%'` or `'_'` literally without `ESCAPE`.
- Assuming backslash is automatically the escape character.
- Believing `LIKE` is case-sensitive everywhere (or case-insensitive everywhere).
- Using `'%word%'` as a "whole word" test.

### Q8 ⭐⭐⭐ 🟡 String-to-number CAST traps: raw_amounts(id, amount_text) holding '1200', '1,200', ' 45 ', '007', '12abc', 'abc', '', '1e3', '3.7', '0x10' and NULL. Show what CAST(... AS INTEGER) and CAST(... AS REAL) return for each in SQLite (garbage gives 0, a numeric prefix is used, '1e3' as INTEGER versus REAL, thousands separators stop the parse, hex text gives 0), explain why a zero from garbage is indistinguishable from a real zero, and write a validation that separates 'clean number', 'dirty but fixable' (strip commas and spaces with REPLACE and TRIM) and 'invalid' (for example a GLOB check such as NOT GLOB '*[^0-9.]*' plus a non-empty check, or comparing CAST(CAST(x AS REAL) AS TEXT) to the input). State that PostgreSQL raises an error for invalid input, SQL Server has TRY_CAST and BigQuery has SAFE_CAST (hedged, not executed). Add the pandas to_numeric(errors='coerce') comparison and say how it treats '1,200', ' 45 ' and '1e3'.
**Asked at:** SQLite lang_corefunc and lang_expr documentation (opened: trim character sets, ASCII-only lower/upper and LIKE, length versus octet_length, concat/concat_ws NULL rules, CAST rules, IS DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL table); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** In SQLite `CAST(text AS INTEGER or REAL)` never fails: it reads the longest numeric prefix and returns 0 when there is none, so garbage and a real zero look the same; validate the text first (a GLOB check after stripping commas and spaces), classify clean, fixable and invalid, and cast only the first two.

**Schema and sample data:**
```sql
CREATE TABLE raw_amounts(id INTEGER PRIMARY KEY, amount_text TEXT);
INSERT INTO raw_amounts VALUES
 (1,'1200'),(2,'1,200'),(3,' 45 '),(4,'007'),(5,'12abc'),(6,'abc'),(7,''),
 (8,'1e3'),(9,'3.7'),(10,'0x10'),(11,NULL);
```

**SQL answer:** `sql_cast` shows the raw casts; `sql_class` classifies and converts.
```sql
SELECT id, amount_text,
       CAST(amount_text AS INTEGER) AS as_int,
       CAST(amount_text AS REAL)    AS as_real,
       CAST(CAST(amount_text AS REAL) AS TEXT) = amount_text AS roundtrip_ok
FROM raw_amounts ORDER BY id
```
```sql
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
```

**pandas answer:** `to_numeric(errors="coerce")` on the raw text, and the same classification with `str.fullmatch`.
```py
coerced = pd.to_numeric(x, errors="coerce")
f = x.str.strip().str.replace(",", "", regex=False).str.replace(" ", "", regex=False)
```

**Example:** id 1 `'1200'` casts to 1200 and is clean. id 2 `'1,200'`: the parse stops at the comma, so both casts return 1 (wrong, not an error); stripping the comma gives 1200, status fixable. id 3 `' 45 '` casts to 45 already (SQLite ignores leading and trailing spaces here), but it is not a clean string: fixable. id 4 `'007'` is 7 and clean (leading zeros lost; keep text if it is a code, not an amount). id 5 `'12abc'` casts to 12 (the numeric prefix) and is invalid. id 6 `'abc'`, id 7 `''` and id 10 `'0x10'` all cast to 0 (hex is not parsed). id 8 `'1e3'` is 1 as INTEGER and 1000.0 as REAL (the INTEGER cast stops at the `e`). id 9 `'3.7'` is 3 as INTEGER and 3.7 as REAL. id 11 NULL stays NULL. The classification: clean for 1, 4, 9; fixable for 2 and 3; invalid for 5, 6, 8, 10; missing for 7 and 11.

**Code:** run with `python3 -I`.
```python
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
```

**Output (my run):**
```text
 id amount_text  as_int  as_real  roundtrip_ok
  1      '1200'  1200.0   1200.0           0.0
  2     '1,200'     1.0      1.0           0.0
  3      ' 45 '    45.0     45.0           0.0
  4       '007'     7.0      7.0           0.0
  5     '12abc'    12.0     12.0           0.0
  6       'abc'     0.0      0.0           0.0
  7          ''     0.0      0.0           0.0
  8       '1e3'     1.0   1000.0           0.0
  9       '3.7'     3.0      3.7           1.0
 10      '0x10'     0.0      0.0           0.0
 11         nan     NaN      NaN           NaN

 id       x  status  value
  1  '1200'   clean 1200.0
  2 '1,200' fixable 1200.0
  3  ' 45 ' fixable   45.0
  4   '007'   clean    7.0
  5 '12abc' invalid    NaN
  6   'abc' invalid    NaN
  7      '' missing    NaN
  8   '1e3' invalid    NaN
  9   '3.7'   clean    3.7
 10  '0x10' invalid    NaN
 11     nan missing    NaN

zero from garbage vs a real zero: 1
typeof(CAST('abc' AS INTEGER)): integer
'12abc' + 1 = 13 (arithmetic coerces the same way)

to_numeric(errors='coerce'):
      x  numeric
 '1200'   1200.0
'1,200'      NaN
 ' 45 '     45.0
  '007'      7.0
'12abc'      NaN
  'abc'      NaN
     ''      NaN
  '1e3'   1000.0
  '3.7'      3.7
 '0x10'      NaN
    nan      NaN

asserts passed (id order): statuses {1: 'clean', 2: 'fixable', 3: 'fixable', 4: 'clean', 5: 'invalid', 6: 'invalid', 7: 'missing', 8: 'invalid', 9: 'clean', 10: 'invalid', 11: 'missing'}
```

**Edge cases:**
- **Zero from garbage:** `CAST('abc' AS INTEGER) = CAST('0' AS INTEGER)` is 1 (true), and the result has type `integer`, so nothing marks the failure. Arithmetic coerces the same way (`'12abc' + 1` is 13).
- **The round-trip test is weak:** `CAST(CAST(x AS REAL) AS TEXT) = x` is false for `'1200'` (it becomes `'1200.0'`) and `'007'`; it is true only for `'3.7'` in this data. I show it in the `roundtrip_ok` column as a trap, not as the recommended check.
- **`'1e3'`:** my rule calls it invalid because it contains `e`. If scientific notation is legal in your feed, accept `CAST(x AS REAL)` for it, and notice the INTEGER cast gives 1.
- **Empty string and NULL:** `''` casts to 0 (a real-looking zero) while NULL stays NULL; the classification marks both missing.
- **Negative numbers, currency symbols and a trailing minus** are not handled by this GLOB rule; extend it deliberately.

**Then explain:**
- **The validation:** `x NOT GLOB '*[^0-9.]*'` means "contains no character that is not a digit or a dot"; add `x GLOB '*[0-9]*'` (at least one digit, so `'.'` and `''` fail) and at most one dot (`LENGTH(x) - LENGTH(REPLACE(x, '.', '')) <= 1`). Run the same test on the cleaned value `f` to find the fixable rows. Strings that need a decision (`'12abc'`, `'0x10'`) go to a reject list for a human.
- **pandas versus SQLite:** `to_numeric(errors="coerce")` gave NaN for `'1,200'`, `'12abc'`, `'abc'`, `''`, `'0x10'` and NULL, and parsed `' 45 '` as 45, `'007'` as 7 and `'1e3'` as 1000. So pandas does not make up a 0 for garbage (NaN is distinguishable), does not use prefixes (`'12abc'` is NaN, SQLite gave 12) and accepts scientific notation. The Code block asserts the status and value columns equal the SQL ones, in id order.
- **Other engines (hedged, not executed here):** PostgreSQL raises an error for an invalid cast (`'abc'::integer`); SQL Server has `TRY_CAST` and BigQuery has `SAFE_CAST`, which return NULL on failure, which is the behaviour you want. SQLite has neither, hence the GLOB guard.

**Follow-ups:**
- *Why not just use CAST and filter `= 0`?* A real zero would be flagged and `'12abc'` would pass as 12.
- *Where should this check live?* At load time, with a rejects table, not in every report.
- *How do you keep leading zeros?* Store ids and codes as text and never cast them.

**Common mistakes:**
- Trusting `CAST` to raise an error.
- Summing a text column and getting silent prefix values.
- Using `CAST(...) = 0` to find bad rows.
- Forgetting that `' 45 '` is accepted by the cast but is still a dirty string.

### Q9 ⭐⭐⭐ 🟡 Debugging: 'my join misses rows because of trailing spaces and case.' customers(customer_id, name) has 'Asha Rao' and orders(order_id, customer_name, amount) has 'Asha Rao ' (trailing space), 'asha rao' and 'Asha Rao' (non-breaking space U+00A0). Show that the equality join returns only exact matches, diagnose with LENGTH, HEX and UNICODE of the suspect values, fix with TRIM and LOWER on both sides (and say why a fix that wraps the indexed column in a function loses the index; point to Part 11), and show that TRIM does not remove U+00A0 unless it is listed or replaced first. Say the real fix is to clean the data once at load time and use customer_id as the join key. Cross-reference Part 2 Q35 for the pandas merge dtype version and Part 1 Q39 for case, whitespace and collation in filters; add the pandas merge with str.strip and str.casefold.
**Asked at:** SQLite lang_corefunc and lang_expr documentation (opened: trim character sets, ASCII-only lower/upper and LIKE, length versus octet_length, concat/concat_ws NULL rules, CAST rules, IS DISTINCT FROM, CASE without ELSE, IN/NOT IN NULL table); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** An equality join matches only byte-identical strings, so diagnose with `LENGTH`, `HEX` and `UNICODE`, normalise both sides (`REPLACE` char(160) with a space, `TRIM`, `LOWER`), and then fix it for good by cleaning at load time and joining on `customer_id`.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_name TEXT, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha Rao');
INSERT INTO orders VALUES
 (101,'Asha Rao ',250),                         -- trailing space
 (102,'asha rao',120),                          -- lower case
 (103,'Asha' || char(160) || 'Rao',90),         -- NBSP between the words
 (104,'Asha Rao',400),                          -- exact
 (105,'Asha Rao' || char(160),30);              -- NBSP at the end
```
(Order 103 and 105 are my two readings of "non-breaking space": inside the name and at its end.)

**SQL answer:** the three joins and the diagnostic query are in the Code block; the diagnosis and the fix:
```sql
SELECT order_id, customer_name, LENGTH(customer_name) AS len, OCTET_LENGTH(customer_name) AS bytes,
       HEX(customer_name) AS hex, UNICODE(SUBSTR(customer_name, -1)) AS last_cp,
       UNICODE(SUBSTR(customer_name, 5, 1)) AS fifth_cp
FROM orders ORDER BY order_id
```
```sql
SELECT o.order_id FROM orders o JOIN customers c
  ON LOWER(TRIM(REPLACE(o.customer_name, char(160), ' '))) = LOWER(TRIM(REPLACE(c.name, char(160), ' ')))
ORDER BY o.order_id
```

**pandas answer:** build one normalised key on both sides (collapse all whitespace, strip, casefold) and merge on it.
```py
def key(s):
    return s.str.replace(r"\s+", " ", regex=True).str.strip().str.casefold()
merged = orders.merge(customers[["customer_id", "k"]], on="k", how="inner")
```

**Example:** the exact join returns only order 104 (revenue 400 out of 890). Diagnosis: order 101 has length 9 and its hex ends in `20` (a space); 103 has length 8 but 9 bytes and `C2A0` (the UTF-8 encoding of U+00A0) in the middle, with `UNICODE` of the fifth character 160; 105 has length 9, 10 bytes and a last code point of 160. `LOWER(TRIM())` on both sides recovers 101, 102 and 104 but not 103 or 105, because `TRIM` removes only spaces and the NBSP is not a space. Replacing `char(160)` with a space first (then `TRIM`, then `LOWER`) matches all five orders: revenue 890.

**Code:** run with `python3 -I`.
```python
# Q9: joins that miss rows because of trailing spaces, case and NBSP; diagnose and fix; pandas merge.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_name TEXT, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha Rao');
INSERT INTO orders VALUES
 (101,'Asha Rao ',250),                         -- trailing space
 (102,'asha rao',120),                          -- lower case
 (103,'Asha' || char(160) || 'Rao',90),         -- NBSP between the words
 (104,'Asha Rao',400),                          -- exact
 (105,'Asha Rao' || char(160),30);              -- NBSP at the end
""")

def rows(sql):
    return [r for r in con.execute(sql)]

sql_exact = "SELECT o.order_id FROM orders o JOIN customers c ON o.customer_name = c.name ORDER BY o.order_id"
sql_trim_lower = ("SELECT o.order_id FROM orders o JOIN customers c "
                  "ON LOWER(TRIM(o.customer_name)) = LOWER(TRIM(c.name)) ORDER BY o.order_id")
sql_fixed = """
SELECT o.order_id FROM orders o JOIN customers c
  ON LOWER(TRIM(REPLACE(o.customer_name, char(160), ' '))) = LOWER(TRIM(REPLACE(c.name, char(160), ' ')))
ORDER BY o.order_id
"""
sql_diag = """
SELECT order_id, customer_name, LENGTH(customer_name) AS len, OCTET_LENGTH(customer_name) AS bytes,
       HEX(customer_name) AS hex, UNICODE(SUBSTR(customer_name, -1)) AS last_cp,
       UNICODE(SUBSTR(customer_name, 5, 1)) AS fifth_cp
FROM orders ORDER BY order_id
"""
print(pd.read_sql(sql_diag, con).assign(customer_name=lambda d: d.customer_name.map(repr)).to_string(index=False)); print()

print("exact equality join      :", [r[0] for r in rows(sql_exact)])
print("TRIM + LOWER on both     :", [r[0] for r in rows(sql_trim_lower)], "(103 and 105 still missing)")
print("TRIM('Asha Rao' || NBSP) length:", con.execute("SELECT LENGTH(TRIM('Asha Rao' || char(160)))").fetchone()[0], "(unchanged, 9)")
print("TRIM with NBSP listed    :", con.execute("SELECT LENGTH(TRIM('Asha Rao' || char(160), ' ' || char(160)))").fetchone()[0], "(8)")
print("+ REPLACE char(160) first:", [r[0] for r in rows(sql_fixed)])

sql_total = """
SELECT SUM(o.amount) FROM orders o JOIN customers c
ON LOWER(TRIM(REPLACE(o.customer_name, char(160), ' '))) = LOWER(TRIM(REPLACE(c.name, char(160), ' ')))"""
print("revenue for Asha: exact join", con.execute(sql_exact.replace("o.order_id", "SUM(o.amount)").replace(" ORDER BY o.order_id", "")).fetchone()[0],
      "| after cleaning", con.execute(sql_total).fetchone()[0], "| all orders", con.execute("SELECT SUM(amount) FROM orders").fetchone()[0])

# the index point (details of plans are Part 11)
con.execute("CREATE INDEX ix_cust_name ON orders(customer_name)")
for label, where in (("customer_name = 'Asha Rao'", "customer_name = 'Asha Rao'"),
                     ("LOWER(TRIM(customer_name)) = ...", "LOWER(TRIM(customer_name)) = 'asha rao'")):
    plan = [r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE " + where)]
    print(f"plan for {label:34s}", plan)

# pandas
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)

def key(s):
    return s.str.replace(r"\s+", " ", regex=True).str.strip().str.casefold()

strip_only = orders.assign(k=orders.customer_name.str.strip().str.casefold())
print("\nstr.strip().str.casefold() only, keys:", strip_only.k.map(repr).tolist())
print("str.strip removes the trailing NBSP of 105 but not the NBSP inside 103")
orders["k"] = key(orders.customer_name)
customers["k"] = key(customers.name)
merged = orders.merge(customers[["customer_id", "k"]], on="k", how="inner")
p_ids = sorted(merged.order_id.tolist())
sql_ids = [r[0] for r in rows(sql_fixed)]
assert p_ids == sql_ids == [101, 102, 103, 104, 105]
assert [r[0] for r in rows(sql_exact)] == [104]
assert strip_only.merge(customers[["customer_id", "k"]], on="k").order_id.tolist() != p_ids
print("pandas matched order ids:", p_ids, "| revenue:", merged.amount.sum())
print("asserts passed (order ids compared sorted)")
```

**Output (my run):**
```text
 order_id  customer_name  len  bytes                  hex  last_cp  fifth_cp
      101    'Asha Rao '    9      9   417368612052616F20       32        32
      102     'asha rao'    8      8     617368612072616F      111        32
      103  'Asha\xa0Rao'    8      9   41736861C2A052616F      111       160
      104     'Asha Rao'    8      8     417368612052616F      111        32
      105 'Asha Rao\xa0'    9     10 417368612052616FC2A0      160        32

exact equality join      : [104]
TRIM + LOWER on both     : [101, 102, 104] (103 and 105 still missing)
TRIM('Asha Rao' || NBSP) length: 9 (unchanged, 9)
TRIM with NBSP listed    : 8 (8)
+ REPLACE char(160) first: [101, 102, 103, 104, 105]
revenue for Asha: exact join 400 | after cleaning 890 | all orders 890
plan for customer_name = 'Asha Rao'         ['SEARCH orders USING INDEX ix_cust_name (customer_name=?)']
plan for LOWER(TRIM(customer_name)) = ...   ['SCAN orders']

str.strip().str.casefold() only, keys: ["'asha rao'", "'asha rao'", "'asha\\xa0rao'", "'asha rao'", "'asha rao'"]
str.strip removes the trailing NBSP of 105 but not the NBSP inside 103
pandas matched order ids: [101, 102, 103, 104, 105] | revenue: 890
asserts passed (order ids compared sorted)
```

**Edge cases:**
- **TRIM and NBSP:** `LENGTH(TRIM('Asha Rao' || char(160)))` stayed 9; listing it, `TRIM(x, ' ' || char(160))`, gave 8. Replace first if NBSP can also sit inside the text.
- **LENGTH versus bytes:** `LENGTH` counts characters, `OCTET_LENGTH` counts bytes; NBSP is 1 character but 2 bytes, so a length/bytes mismatch is a quick sign of non-ASCII text.
- **Index cost:** with an index on `orders(customer_name)`, `WHERE customer_name = 'Asha Rao'` showed `SEARCH ... USING INDEX`, but `WHERE LOWER(TRIM(customer_name)) = 'asha rao'` showed `SCAN orders`: wrapping the column in a function hides it from the plain index. Part 11 covers plans and expression indexes; the real fix is below.
- **Over-matching:** two different customers whose names differ only by case or spacing now collide; that is another reason to join on an id.
- **ASCII-only LOWER:** accented capitals are not lowered by SQLite (Q33).

**Then explain:**
- **Diagnose first:** `LENGTH`, `OCTET_LENGTH`, `HEX` and `UNICODE(SUBSTR(x, n, 1))` show exactly which character is odd. Do not guess.
- **The real fix:** clean once when loading (strip, collapse, standardise case in a separate key column or a dimension table), and have orders carry `customer_id`. Joining on free-text names is the bug.
- **pandas:** `str.strip()` removes NBSP at the ends (confirmed: order 105 matched), but an NBSP inside the text survives, so `str.strip().str.casefold()` alone still missed order 103 (the Code block asserts the merge differs). The `\s+` collapse is what handles it, because `\s` matches NBSP in Python's Unicode regex. For the merge dtype mismatch (strings versus numbers) see Part 2 Q35; for case, whitespace and collation in filters see Part 1 Q39.
- The merge result and the SQL result are compared as sorted lists of order ids: both give 101 to 105.

**Follow-ups:**
- *Why does the join "fail silently"?* A non-match is not an error; the rows are simply absent from an inner join. Count rows before and after, or run an anti-join for unmatched orders.
- *Would COLLATE NOCASE fix it?* Only the case part (ASCII); spaces and NBSP remain.
- *How do you find all affected rows?* `WHERE customer_name <> TRIM(customer_name)` or `WHERE HEX(customer_name) LIKE '%C2A0%'`.

**Common mistakes:**
- Trusting `TRIM` for all invisible whitespace.
- Fixing one side only (`TRIM(a) = b`).
- Normalising in every query instead of at load.
- Not checking how many rows the join lost.

### Q10 ⭐⭐⭐ 🟡 Debugging: 'my pivot totals do not match.' sales(region, product, month, amount) where month values include 'Jan', 'Feb', 'Mar' but also 'jan', ' Feb' (leading space), 'Apr' and NULL, and amount has some NULLs. A teammate's pivot of jan, feb and mar columns plus a total column built as jan + feb + mar differs from SELECT SUM(amount). Show the reconciliation: add an other column (month not in the list or NULL), explain that jan + feb + mar is NULL if any piece is NULL (use COALESCE or sum the CASE directly), check that the pivot grand total equals the plain SUM(amount), and fix the dirty month labels with TRIM and a case-insensitive comparison. Show the final self-check query that returns zero rows when the pivot reconciles. Add the pandas pivot_table(margins=True) check.
**Asked at:** SQL pivot guides (datadriven.io, DataVidhya, Educative and a Medium write-up, search snippets only; the DataVidhya lesson page opened but showed only its introduction: CASE inside SUM or COUNT, dynamic pivot, NULL categories); guides, not candidate reports; analyst and data engineer rounds at product companies and GCCs; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** The pivot total is wrong for three reasons: `jan + feb + mar` is NULL if any piece is NULL, dirty labels ('jan', ' Feb') and other months ('Apr', NULL) are in none of the columns, and NULL amounts hide cells; fix it by normalising the label, adding an `other` column and a total taken straight from `SUM(amount)`, then prove it with a self-check query that returns zero rows.

**Schema and sample data:**
```sql
CREATE TABLE sales(id INTEGER PRIMARY KEY, region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 (1,'East','A','Jan',100),(2,'East','A','Feb',50),(3,'East','B','Mar',NULL),(4,'East','B','jan',30),
 (5,'West','A',' Feb',70),(6,'West','A','Mar',40),(7,'West','B','Apr',20),(8,'West','B',NULL,10),
 (9,'North','A','Jan',60),(10,'North','A','Feb',NULL),
 (11,'West','A','Jan',15),(12,'West','A','Feb',25);
```

**SQL answer:** the teammate's version, the fixed pivot and the self-check (all in the Code block).
```sql
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS mar,
       SUM(CASE WHEN month = 'Jan' THEN amount END)
     + SUM(CASE WHEN month = 'Feb' THEN amount END)
     + SUM(CASE WHEN month = 'Mar' THEN amount END) AS total
FROM sales GROUP BY region ORDER BY region
```
```sql
WITH s AS (SELECT region, LOWER(TRIM(month)) AS m, amount FROM sales)
SELECT region,
       SUM(CASE WHEN m = 'jan' THEN amount END) AS jan,
       SUM(CASE WHEN m = 'feb' THEN amount END) AS feb,
       SUM(CASE WHEN m = 'mar' THEN amount END) AS mar,
       SUM(CASE WHEN m IS NULL OR m NOT IN ('jan', 'feb', 'mar') THEN amount END) AS other,
       SUM(amount) AS total
FROM s GROUP BY region ORDER BY region
```
The self-check is `make_check(...)` in the Code block: it joins the pivot to `SELECT region, SUM(amount) FROM sales GROUP BY region`, returns the regions where `COALESCE(jan,0) + COALESCE(feb,0) + COALESCE(mar,0) + COALESCE(other,0)` differs from the plain total, and a `GRAND` row if the grand totals differ. Zero rows means reconciled.

**pandas answer:** normalise the label, send everything else to `other`, and use `margins=True` for the totals.
```py
m = sales.month.str.strip().str.lower()
m = m.where(m.isin(["jan", "feb", "mar"]), "other")     # NaN is not in the list, so it becomes 'other'
pt = sales.pivot_table(index="region", columns="m", values="amount", aggfunc="sum", margins=True, margins_name="total")
```

**Example:** the plain `SUM(amount)` is 420. The teammate's pivot: East jan = 100 (the 'jan' row of 30 is not matched), feb = 50, mar = NULL (its only March row has a NULL amount), so `jan + feb + mar` is NULL. North is NULL because its feb and mar cells are NULL. West gets 80 (15 + 25 + 40), because the ' Feb' row (70), the 'Apr' row (20) and the NULL-month row (10) are in no column. So the totals are NULL, NULL and 80, and the column sums to 80, not 420. The fix: lower-case and trim the label (the 'jan' row joins January: East jan = 130; ' Feb' joins February: West feb = 70 + 25 = 95), add `other` (West: 20 + 10 = 30) and take `total = SUM(amount)`: East 180, North 60, West 180, grand total 420. The five parts add to 420 as well.

**Code:** run with `python3 -I`.
```python
# Q10: pivot totals that do not match: dirty labels, NULL month, NULL amounts; reconciliation and self-check.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(id INTEGER PRIMARY KEY, region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 (1,'East','A','Jan',100),(2,'East','A','Feb',50),(3,'East','B','Mar',NULL),(4,'East','B','jan',30),
 (5,'West','A',' Feb',70),(6,'West','A','Mar',40),(7,'West','B','Apr',20),(8,'West','B',NULL,10),
 (9,'North','A','Jan',60),(10,'North','A','Feb',NULL),
 (11,'West','A','Jan',15),(12,'West','A','Feb',25);
""")

sql_teammate = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS mar,
       SUM(CASE WHEN month = 'Jan' THEN amount END)
     + SUM(CASE WHEN month = 'Feb' THEN amount END)
     + SUM(CASE WHEN month = 'Mar' THEN amount END) AS total
FROM sales GROUP BY region ORDER BY region
"""
sql_fixed = """
WITH s AS (SELECT region, LOWER(TRIM(month)) AS m, amount FROM sales)
SELECT region,
       SUM(CASE WHEN m = 'jan' THEN amount END) AS jan,
       SUM(CASE WHEN m = 'feb' THEN amount END) AS feb,
       SUM(CASE WHEN m = 'mar' THEN amount END) AS mar,
       SUM(CASE WHEN m IS NULL OR m NOT IN ('jan', 'feb', 'mar') THEN amount END) AS other,
       SUM(amount) AS total
FROM s GROUP BY region ORDER BY region
"""
def make_check(pivot_sql, parts):
    """Rows that disagree with the plain SUM(amount), per region and for the grand total. Zero rows = reconciled."""
    pivot_sql = pivot_sql.replace(" ORDER BY region", "")
    return f"""
WITH pivot AS ({pivot_sql}), plain AS (SELECT region, SUM(amount) AS total FROM sales GROUP BY region)
SELECT p.region, {parts} AS parts, pl.total AS plain_total
FROM pivot p JOIN plain pl ON pl.region = p.region
WHERE {parts} <> COALESCE(pl.total, 0)
UNION ALL
SELECT 'GRAND', SUM({parts}), (SELECT SUM(amount) FROM sales)
FROM pivot p
HAVING SUM({parts}) <> (SELECT SUM(amount) FROM sales)
"""

parts_fixed = "COALESCE(p.jan, 0) + COALESCE(p.feb, 0) + COALESCE(p.mar, 0) + COALESCE(p.other, 0)"
parts_teammate = "COALESCE(p.jan, 0) + COALESCE(p.feb, 0) + COALESCE(p.mar, 0)"
sql_check = make_check(sql_fixed, parts_fixed)
sql_check_teammate = make_check(sql_teammate, parts_teammate)
sql_in_other = """
SELECT month, COUNT(*) AS n_rows, SUM(amount) AS amount
FROM sales
WHERE LOWER(TRIM(month)) IS NULL OR LOWER(TRIM(month)) NOT IN ('jan', 'feb', 'mar')
GROUP BY month ORDER BY month
"""

print("plain SUM(amount):", con.execute("SELECT SUM(amount) FROM sales").fetchone()[0])
t = pd.read_sql(sql_teammate, con)
print("\nteammate pivot (jan + feb + mar):"); print(t.to_string(index=False))
print("sum of the teammate total column:", t.total.sum(), "vs SUM(amount) above")
print("distinct month labels:", [r[0] for r in con.execute("SELECT DISTINCT month FROM sales ORDER BY 1")])

f = pd.read_sql(sql_fixed, con)
print("\nfixed pivot with other and a direct SUM(amount) total:"); print(f.to_string(index=False))
print("pivot grand total:", f.total.sum(), "| sum of the five parts:", f[["jan", "feb", "mar", "other"]].fillna(0).sum().sum())
bad = con.execute(sql_check_teammate).fetchall()
print("\nself-check on the teammate's pivot (parts vs total, no 'other'):", bad)
good = con.execute(sql_check).fetchall()
print("self-check on the fixed pivot returns:", good)
assert good == []

print("what lands in other (month label, rows, amount):", con.execute(sql_in_other).fetchall())

# pandas
sales = pd.read_sql("SELECT * FROM sales", con)
raw = sales.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", margins=True, margins_name="total")
print("\npandas pivot_table on the raw labels, margins=True:"); print(raw)
print("pandas grand total cell:", raw.loc["total", "total"], "vs df.amount.sum():", sales.amount.sum(),
      "(rows with a NaN month key are dropped from the pivot)")

m = sales.month.str.strip().str.lower()
m = m.where(m.isin(["jan", "feb", "mar"]), "other")     # NaN is not in the list, so it becomes 'other'
sales["m"] = m
pt = sales.pivot_table(index="region", columns="m", values="amount", aggfunc="sum", margins=True, margins_name="total")
pt = pt.reindex(columns=["jan", "feb", "mar", "other", "total"]).reset_index().rename_axis(columns=None)
grand = pt.loc[pt.region == "total", "total"].item()
pt = pt[pt.region != "total"].sort_values("region").reset_index(drop=True)
print("\npandas fixed pivot (margins=True):"); print(pt.to_string(index=False))
assert grand == sales.amount.sum() == con.execute("SELECT SUM(amount) FROM sales").fetchone()[0]

# SQL gives NULL for a cell whose rows all have NULL amounts, pandas sum gives 0: compare after filling both with 0
pd.testing.assert_frame_equal(f.fillna(0), pt.fillna(0), check_dtype=False)
print("East/Mar: SQL", f.set_index('region').loc['East', 'mar'], "| pandas", pt.set_index('region').loc['East', 'mar'])
print("asserts passed (compared after sorting by region, NULL/NaN filled with 0 on both sides)")
```

**Output (my run):**
```text
plain SUM(amount): 420

teammate pivot (jan + feb + mar):
region  jan  feb  mar  total
  East  100 50.0  NaN    NaN
 North   60  NaN  NaN    NaN
  West   15 25.0 40.0   80.0
sum of the teammate total column: 80.0 vs SUM(amount) above
distinct month labels: [None, ' Feb', 'Apr', 'Feb', 'Jan', 'Mar', 'jan']

fixed pivot with other and a direct SUM(amount) total:
region  jan  feb  mar  other  total
  East  130 50.0  NaN    NaN    180
 North   60  NaN  NaN    NaN     60
  West   15 95.0 40.0   30.0    180
pivot grand total: 420 | sum of the five parts: 420.0

self-check on the teammate's pivot (parts vs total, no 'other'): [('East', 150, 180), ('West', 80, 180), ('GRAND', 290, 420)]
self-check on the fixed pivot returns: []
what lands in other (month label, rows, amount): [(None, 1, 10), ('Apr', 1, 20)]

pandas pivot_table on the raw labels, margins=True:
month    Feb   Apr   Feb    Jan   Mar   jan  total
region                                            
East     NaN   NaN  50.0  100.0   0.0  30.0  180.0
North    NaN   NaN   0.0   60.0   NaN   NaN   60.0
West    70.0  20.0  25.0   15.0  40.0   NaN  170.0
total   70.0  20.0  75.0  175.0  40.0  30.0  410.0
pandas grand total cell: 410.0 vs df.amount.sum(): 420.0 (rows with a NaN month key are dropped from the pivot)

pandas fixed pivot (margins=True):
region   jan  feb  mar  other  total
  East 130.0 50.0  0.0    NaN  180.0
 North  60.0  0.0  NaN    NaN   60.0
  West  15.0 95.0 40.0   30.0  180.0
East/Mar: SQL nan | pandas 0.0
asserts passed (compared after sorting by region, NULL/NaN filled with 0 on both sides)
```

**Edge cases:**
- **NULL in `+`:** `NULL + 5` is NULL, so one missing month cell wipes out the total (East and North above). Either sum the CASE directly (`SUM(amount)`) or wrap each piece in `COALESCE(piece, 0)`; never add nullable aggregates with `+`.
- **A NULL month needs its own test:** `month NOT IN ('jan','feb','mar')` is NULL, not true, for a NULL month, so it would drop that row from `other`. The query uses `m IS NULL OR m NOT IN (...)`. The extra query in the Code block lists what lands in `other`: the NULL month (1 row, amount 10) and 'Apr' (1 row, amount 20).
- **NULL amounts:** the East/March cell is NULL in SQL because its only row has a NULL amount. That is "no data", not 0. pandas gives 0.0 for the same cell (a `sum` of all-NaN is 0), which is why the Code block fills both sides with 0 before the assert.
- **`other` hides new dirt:** a misspelt label ('Janu') lands in `other` and the check still passes, because the check proves the totals add up, not that the labels are right. Look at the `other` breakdown too.
- **Do not silently drop rows:** the self-check should include rows with NULL region or amount if those can exist.

**Then explain:**
- **Reconciliation recipe:** (1) compute the plain total, (2) pivot with an `other` bucket so every row lands somewhere, (3) compare per row and for the grand total. When parts and total disagree, `other` and the NULLs are where to look.
- **The teammate's self-check fails:** run against the teammate's pivot (without `other`), the check returned East 150 versus 180, West 80 versus 180 and a GRAND row of 290 versus 420 (North passes after the COALESCE, even though the teammate's total cell is NULL). On the fixed pivot it returns no rows.
- **pandas:** `pivot_table(margins=True)` adds a `total` row and column. On the raw labels it produced two separate `Feb` columns ('Feb' and ' Feb'), a lower-case 'jan' column, and a grand total of 410 against `df.amount.sum()` of 420, because rows whose month is NaN are dropped from the pivot (the NaN-month row held 10). That is the same bug as in SQL: a pivot total can differ from the plain sum. After the normalise-and-other step the pandas grand total equals 420, asserted against the SQL `SUM(amount)`.
- **Dialects (not executed here):** SQL Server, Oracle, Snowflake and BigQuery `PIVOT` also, from memory, ignore labels not in the `IN` list, so the same reconciliation is needed there.

**Follow-ups:**
- *Why not just add `other` as `total - jan - feb - mar`?* It hides the same NULL problem; compute `other` from the rows.
- *How do you prevent dirty labels?* Constrain or clean at load, or join to a months dimension table.
- *Why a grand-total check as well as a per-row check?* Rows with a NULL region would not match any region in the per-region join.

**Common mistakes:**
- `jan + feb + mar` as the total.
- Forgetting that `x NOT IN (...)` is NULL for a NULL `x`.
- Declaring victory because the pivot "looks right" without comparing to `SUM(amount)`.
- Using `COALESCE(amount, 0)` inside the CASE to hide NULL amounts, then reporting zero for "no data".

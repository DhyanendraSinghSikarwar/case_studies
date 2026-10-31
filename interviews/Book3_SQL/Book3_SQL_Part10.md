# Book 3 — Part 10: Pivot and unpivot, string operations and NULL traps, with pandas equivalents

**Topic:** pivot with conditional aggregation (CASE inside SUM and COUNT, FILTER), SQLite having no PIVOT or UNPIVOT (emulation, other engines hedged), dynamic pivot at concept level, unpivot with UNION ALL and CROSS JOIN VALUES, wide to long and long to wide, pivot totals and subtotals without ROLLUP, crosstab percentages, transposing; string functions that run in SQLite (SUBSTR, INSTR, REPLACE, TRIM character sets, UPPER and LOWER, LENGTH versus OCTET_LENGTH, PRINTF and FORMAT, LIKE with ESCAPE and GLOB, group_concat and string_agg, HEX, UNICODE and CHAR), what SQLite lacks (REGEXP, SPLIT_PART, REVERSE, LPAD), splitting delimited strings, parsing emails, phone numbers, names, SKUs and key=value logs, cleaning dirty text (whitespace, NBSP, case, Unicode), collation and sort order, casting traps and type affinity, padding and number formatting; NULL traps with new angles (CASE and COALESCE family, row-wise versus column-wise NULL, NULL versus empty string versus 0 versus 'NULL' text, set operators, constraints and tri-state flags), data-quality audits, duplicates ignoring case and spaces; and pandas (pivot, pivot_table, crosstab, melt, wide_to_long, stack, unstack, explode, the .str accessor, astype and to_numeric, to_datetime errors, NaN versus None versus NA, the pandas 3 default str dtype, category pitfalls) with SQL-versus-pandas differences.
**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 15, ⭐⭐ 16, ⭐ 9)  |  **Date:** 2026-10-25  |  **Status:** Answers written (Wave B), Wave C review done

Scope note: this part covers reshaping, text handling and new NULL angles. Part 1 owns NULL basics (Q4 COUNT and aggregates with NULLs, Q5 three-valued logic, Q6 COALESCE and NULLIF, Q10 plain conditional aggregation, Q13 NOT IN with NULL, Q14 ORDER BY with NULLs, Q16 SQL versus pandas NULL in grouping, Q36 ROLLUP concepts, Q39 case, whitespace and collation in filters, Q41 null-safe equality, Q44 CASE subtleties), Part 2 owns join NULL keys (Q6) and the pandas merge dtype mismatch (Q35), Part 3 owns the NOT IN NULL trap (Q3), ANY/ALL emulation (Q22) and deleting duplicates (Q25), Part 4 owns exact-duplicate detection (Q10), Part 6 owns date storage (Q1), and Part 9 owns recursion mechanics (Q1) that the split, parse and puzzle questions use. Questions here take new angles and point to those headings instead of repeating them. Every question states its tables so Wave B can build sample data; keep tables small enough to check by hand.

Evidence limits: no candidate-reported SQL questions were found. Sources are official documentation (SQLite lang_corefunc and lang_expr, pandas reshaping and text user guides, all opened), LeetCode problems on the doocs mirror (1484, 1795, 1667, 1527, 1873, opened; they are public problem statements, not candidate reports) and search snippets only (datadriven.io, DataVidhya, Educative, prachub, dataford, Interview Query, DesignGurus, Scribd and Telegram question banks). leetcode.com pages were not opened. 'Asked at' tags are source types, not company reports. Environment (checked by running): SQLite 3.45.1 has no regexp (error), split_part, reverse, lpad or char_length, but has concat, concat_ws, string_agg, format, printf (including the %,d comma flag), octet_length, unhex, iif and IS DISTINCT FROM; pandas 3.0.5 infers the str dtype with NaN as the missing marker. All other engines are hedged as not executed.

---

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

### Q11 ⭐⭐⭐ 🟡 Split a delimited column into rows: orders_tags(order_id, tags) where tags is a comma-separated string ('red,blue,sale'), with NULL, an empty string, an empty element ('a,,b') and spaces after commas. Return (order_id, tag, position) one row per tag using a recursive CTE (SQLite has no split_part, string_split or generate_series; recursion mechanics are in Part 9 Q1, do not repeat them), explain how to handle the last element without a trailing delimiter (append a delimiter first) and how to keep NULL and empty rows or drop them deliberately. Then count orders per tag. Mention STRING_SPLIT (SQL Server), UNNEST(STRING_TO_ARRAY(...)) (PostgreSQL), JSON_TABLE and SUBSTRING_INDEX tricks (MySQL) and SPLIT with UNNEST (BigQuery) as hedged text, not executed. Add the pandas str.split(',') plus explode version and state what explode does to NaN and empty strings.
**Asked at:** SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Append a comma to the string, then let a recursive CTE cut off everything before the first comma, one element per level, with a position counter; a LEFT JOIN back to the table keeps the NULL row, and a `WHERE tag <> ''` drops the empty elements when you want them gone.

**Schema and sample data:** six orders chosen to hit every case: a normal list, spaces after the comma, NULL, an empty string, an empty element in the middle, and a repeated tag.
```sql
CREATE TABLE orders_tags(order_id INTEGER PRIMARY KEY, tags TEXT);
INSERT INTO orders_tags VALUES
 (1,'red,blue,sale'),
 (2,'red, sale'),
 (3,NULL),
 (4,''),
 (5,'a,,b'),
 (6,'sale,sale');
```

**SQL answer:** `SQL_SPLIT` (keep everything), `SQL_SPLIT_CLEAN` (drop NULL and empty) and `SQL_COUNT` (orders per tag) are in the Code block. The main one, identical to the Code block:
```sql
SQL_SPLIT = """
WITH RECURSIVE s(order_id, pos, tag, rest) AS (
  SELECT order_id, 0, NULL, tags || ','          -- append a delimiter so the last element is cut like the others
  FROM orders_tags WHERE tags IS NOT NULL
  UNION ALL
  SELECT order_id, pos + 1,
         TRIM(SUBSTR(rest, 1, INSTR(rest, ',') - 1)),
         SUBSTR(rest, INSTR(rest, ',') + 1)
  FROM s WHERE rest <> ''
)
SELECT o.order_id, s.tag, s.pos AS position
FROM orders_tags o LEFT JOIN s ON s.order_id = o.order_id AND s.pos > 0
ORDER BY o.order_id, s.pos
"""
```
- The anchor row has `pos = 0` and `rest = tags || ','`. Appending the delimiter first means every element, including the last, ends with a comma, so one cutting rule handles all of them. Without it the last element is lost (the Code block prints that trap: `['red', 'blue']`).
- The recursive step takes the text before the first comma (`SUBSTR(rest, 1, INSTR(rest, ',') - 1)`), keeps the text after it as the new `rest`, and stops when `rest` is empty. The `0` anchor row is only a starter: it is excluded with `pos > 0`.
- `TRIM` removes the space after the comma (it strips only the space character; tabs and NBSP survive, see Q2 in this part for that).
- NULL: the anchor has `WHERE tags IS NOT NULL` because `NULL || ','` is NULL and the recursion would never start for it. The final `LEFT JOIN` puts that order back with a NULL tag, so nothing silently disappears.
- Recursion mechanics (termination, UNION ALL versus UNION, the one-reference rule) are in Part 9 Q1 and not repeated here.

Orders per tag (`SQL_COUNT`, same split, drop-rule applied):
```sql
SQL_COUNT = """
WITH RECURSIVE s(order_id, pos, tag, rest) AS (
  SELECT order_id, 0, NULL, tags || ',' FROM orders_tags WHERE tags IS NOT NULL
  UNION ALL
  SELECT order_id, pos + 1, TRIM(SUBSTR(rest, 1, INSTR(rest, ',') - 1)), SUBSTR(rest, INSTR(rest, ',') + 1)
  FROM s WHERE rest <> ''
)
SELECT tag, COUNT(DISTINCT order_id) AS orders, COUNT(*) AS mentions
FROM s WHERE pos > 0 AND tag <> ''
GROUP BY tag ORDER BY orders DESC, tag
"""
```
`COUNT(DISTINCT order_id)` is the number of orders; `COUNT(*)` is the number of mentions. They differ for order 6, which lists `sale` twice.

**pandas answer:** `str.split(",")` makes a list per row, `explode` makes one row per element:
```py
def split_tags(df):
    t = df.assign(tag=df["tags"].str.split(",")).explode("tag")     # one row per element; NaN and '' survive
    t["tag"] = t["tag"].str.strip()
    t["position"] = t.groupby("order_id").cumcount() + 1
    return t[["order_id", "tag", "position"]]
```
and the clean and count versions:
```py
p_clean = p_all[p_all["tag"].notna() & (p_all["tag"] != "")].reset_index(drop=True)
p_cnt = (p_clean.groupby("tag")
         .agg(orders=("order_id", "nunique"), mentions=("order_id", "size"))
         .reset_index().sort_values(["orders", "tag"], ascending=[False, True]).reset_index(drop=True))
```

**Example:** by hand.
- Order 1, `red,blue,sale` becomes `red,blue,sale,`. Level 1 cuts `red` (rest `blue,sale,`), level 2 cuts `blue`, level 3 cuts `sale`, rest is `''`, stop. Positions 1, 2, 3.
- Order 2, `red, sale` becomes `red, sale,`: elements `red` and ` sale`; TRIM makes it `sale`.
- Order 3 is NULL: no recursion rows; the LEFT JOIN returns `(3, NULL, NULL)`.
- Order 4 is `''`, so `rest` is `','`: one element, the empty string, at position 1. An empty string is a list with one empty element, not an empty list.
- Order 5, `a,,b,`: elements `a`, `''`, `b` at positions 1, 2, 3. The empty element keeps its position, so after dropping it the positions are 1 and 3 (gaps), which is useful if you need to know where it was.
- Order 6 gives `sale` twice. Counting: `sale` appears in orders 1, 2, 6 (3 orders, 4 mentions); `red` in orders 1, 2; `a`, `b`, `blue` once each.

**Code:** run with `python3 -I`. I compare SQL and pandas after sorting by `order_id, position` (and by `orders DESC, tag` for the counts).
```python
# Q11: split a comma-separated column into rows (recursive CTE) and count orders per tag
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders_tags(order_id INTEGER PRIMARY KEY, tags TEXT);
INSERT INTO orders_tags VALUES
 (1,'red,blue,sale'),
 (2,'red, sale'),
 (3,NULL),
 (4,''),
 (5,'a,,b'),
 (6,'sale,sale');
""")

SQL_SPLIT = """
WITH RECURSIVE s(order_id, pos, tag, rest) AS (
  SELECT order_id, 0, NULL, tags || ','          -- append a delimiter so the last element is cut like the others
  FROM orders_tags WHERE tags IS NOT NULL
  UNION ALL
  SELECT order_id, pos + 1,
         TRIM(SUBSTR(rest, 1, INSTR(rest, ',') - 1)),
         SUBSTR(rest, INSTR(rest, ',') + 1)
  FROM s WHERE rest <> ''
)
SELECT o.order_id, s.tag, s.pos AS position
FROM orders_tags o LEFT JOIN s ON s.order_id = o.order_id AND s.pos > 0
ORDER BY o.order_id, s.pos
"""
SQL_SPLIT_CLEAN = """
WITH RECURSIVE s(order_id, pos, tag, rest) AS (
  SELECT order_id, 0, NULL, tags || ',' FROM orders_tags WHERE tags IS NOT NULL
  UNION ALL
  SELECT order_id, pos + 1, TRIM(SUBSTR(rest, 1, INSTR(rest, ',') - 1)), SUBSTR(rest, INSTR(rest, ',') + 1)
  FROM s WHERE rest <> ''
)
SELECT order_id, tag, pos AS position FROM s WHERE pos > 0 AND tag <> '' ORDER BY order_id, pos
"""
SQL_COUNT = """
WITH RECURSIVE s(order_id, pos, tag, rest) AS (
  SELECT order_id, 0, NULL, tags || ',' FROM orders_tags WHERE tags IS NOT NULL
  UNION ALL
  SELECT order_id, pos + 1, TRIM(SUBSTR(rest, 1, INSTR(rest, ',') - 1)), SUBSTR(rest, INSTR(rest, ',') + 1)
  FROM s WHERE rest <> ''
)
SELECT tag, COUNT(DISTINCT order_id) AS orders, COUNT(*) AS mentions
FROM s WHERE pos > 0 AND tag <> ''
GROUP BY tag ORDER BY orders DESC, tag
"""

sql_all = pd.read_sql_query(SQL_SPLIT, con)
print("SQL, every order kept (NULL tag = NULL or missing list; '' = empty element):")
print(sql_all.to_string(index=False))
sql_clean = pd.read_sql_query(SQL_SPLIT_CLEAN, con)
print("\nSQL, empty and NULL dropped deliberately:")
print(sql_clean.to_string(index=False))
sql_cnt = pd.read_sql_query(SQL_COUNT, con)
print("\nSQL, orders per tag:")
print(sql_cnt.to_string(index=False))

def split_tags(df):
    t = df.assign(tag=df["tags"].str.split(",")).explode("tag")     # one row per element; NaN and '' survive
    t["tag"] = t["tag"].str.strip()
    t["position"] = t.groupby("order_id").cumcount() + 1
    return t[["order_id", "tag", "position"]]
raw = pd.read_sql_query("SELECT * FROM orders_tags", con)
p_all = split_tags(raw)
print("\npandas str.split + explode (raw):")
print(p_all.to_string(index=False))
print("tags dtype:", raw["tags"].dtype, "| NaN row after explode:", p_all.loc[p_all["order_id"] == 3, "tag"].tolist())

p_clean = p_all[p_all["tag"].notna() & (p_all["tag"] != "")].reset_index(drop=True)
p_cnt = (p_clean.groupby("tag")
         .agg(orders=("order_id", "nunique"), mentions=("order_id", "size"))
         .reset_index().sort_values(["orders", "tag"], ascending=[False, True]).reset_index(drop=True))

# Comparison rows: order_id, position (both sorted by order_id, position).
# SQL keeps NULL for order 3; pandas keeps NaN. Map NaN -> None to compare the all-rows version.
a = sql_all.copy()
b = p_all.copy()
b["position"] = b["position"].astype("float")
a["position"] = a["position"].astype("float")
# SQL gives NULL position for the NULL-tags order; pandas numbers it 1. Align by design: set both to NaN there.
b.loc[b["tag"].isna(), "position"] = np.nan
pd.testing.assert_frame_equal(a.reset_index(drop=True), b.reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_clean, p_clean, check_dtype=False)
pd.testing.assert_frame_equal(sql_cnt, p_cnt, check_dtype=False)
print("\nasserts passed: all-rows, cleaned rows and per-tag counts match (sorted by order_id, position / orders desc, tag)")

# trap: no trailing delimiter appended -> the last element is lost
bad = con.execute("""
WITH RECURSIVE s(order_id, pos, tag, rest) AS (
  SELECT order_id, 0, NULL, tags FROM orders_tags WHERE order_id = 1
  UNION ALL
  SELECT order_id, pos + 1, SUBSTR(rest, 1, INSTR(rest, ',') - 1), SUBSTR(rest, INSTR(rest, ',') + 1)
  FROM s WHERE INSTR(rest, ',') > 0
) SELECT tag FROM s WHERE pos > 0""").fetchall()
print("without appending ',' (order 1):", [r[0] for r in bad], "-> 'sale' is lost")
print("explode on NaN/'':", pd.Series([np.nan, "", "a,b"]).str.split(",").explode().tolist())
```

**Output (my run):**
```text
SQL, every order kept (NULL tag = NULL or missing list; '' = empty element):
 order_id  tag  position
        1  red       1.0
        1 blue       2.0
        1 sale       3.0
        2  red       1.0
        2 sale       2.0
        3  NaN       NaN
        4            1.0
        5    a       1.0
        5            2.0
        5    b       3.0
        6 sale       1.0
        6 sale       2.0

SQL, empty and NULL dropped deliberately:
 order_id  tag  position
        1  red         1
        1 blue         2
        1 sale         3
        2  red         1
        2 sale         2
        5    a         1
        5    b         3
        6 sale         1
        6 sale         2

SQL, orders per tag:
 tag  orders  mentions
sale       3         4
 red       2         2
   a       1         1
   b       1         1
blue       1         1

pandas str.split + explode (raw):
 order_id  tag  position
        1  red         1
        1 blue         2
        1 sale         3
        2  red         1
        2 sale         2
        3  NaN         1
        4              1
        5    a         1
        5              2
        5    b         3
        6 sale         1
        6 sale         2
tags dtype: str | NaN row after explode: [nan]

asserts passed: all-rows, cleaned rows and per-tag counts match (sorted by order_id, position / orders desc, tag)
without appending ',' (order 1): ['red', 'blue'] -> 'sale' is lost
explode on NaN/'': [nan, '', 'a', 'b']
```
Honest notes from the run: SQL gives the NULL order a NULL position, while pandas numbers it 1 (`cumcount`), so the Code block sets that one position to NaN before comparing; the explode result for a NaN row is a single NaN row, and for `''` it is a single empty-string row. The pandas `tags` column has the `str` dtype (pandas 3.0.5).

**Edge cases:**
- NULL and empty string are different: NULL means unknown or no list, `''` is a list with one empty element. Decide per business rule; the SQL and the pandas code above both keep them in the "keep everything" version and drop both in the "clean" version.
- Empty element (`a,,b`): kept as `''` unless you filter it; its position still counts.
- Duplicates inside one list (`sale,sale`): `COUNT(DISTINCT order_id)` versus `COUNT(*)`.
- Spaces: only after a trim; a tab or NBSP after the comma would stay. Case: `Sale` and `sale` are different tags unless you `LOWER` them.
- Lists with a trailing comma (`a,b,`) produce a final empty element; the filter removes it.

**Then explain:**
- **Why append a delimiter:** it makes the last element look like all the others, so you need no special case and no `CASE WHEN INSTR(...) = 0`.
- **Why a position column:** it keeps the original order and distinguishes repeated values.
- **No helper functions in SQLite 3.45.1:** I ran it and there is no `split_part` and no `generate_series` (both fail with 'no such function' or 'no such table'). The recursive CTE is the portable way.
- **Other engines (not executed here):** SQL Server has `STRING_SPLIT(tags, ',')` (and, from SQL Server 2022, an optional ordinal column); PostgreSQL has `UNNEST(STRING_TO_ARRAY(tags, ',')) WITH ORDINALITY`; MySQL 8 has no split function, so people use `JSON_TABLE` on a JSON array built with `REPLACE`, or a numbers table with `SUBSTRING_INDEX`; BigQuery has `SPLIT(tags, ',')` combined with `UNNEST`. I did not run any of these, and null/empty handling differs by engine (check each).
- **The real fix** is a child table `order_tags(order_id, tag)`; comma-separated columns break first normal form and cannot be indexed on a tag.

**Follow-ups:**
- *How do you split into columns instead of rows?* Fixed number of elements: `SUBSTR`/`INSTR` per position; unknown number: rows are the right shape. pandas: `str.split(",", expand=True)`.
- *What if the delimiter can appear inside a value?* You need quoting rules, so do it in code (a CSV parser), not in SQL.
- *How would you count tags in Postgres?* `UNNEST(STRING_TO_ARRAY(...))` then `GROUP BY` (hedged, not executed).

**Common mistakes:**
- Forgetting the trailing delimiter and losing the last element.
- Starting the recursion from NULL tags, or dropping NULL orders silently with an inner join.
- Not trimming, so `' sale'` and `'sale'` are different tags.
- Counting mentions when the question asked for orders (no `DISTINCT`).
- Assuming `explode` drops NaN or empty lists: NaN stays as NaN and `''` stays as `''`.

### Q12 ⭐⭐⭐ 🟡 Row-wise versus column-wise NULL: survey(user_id, q1, q2, q3) with ratings where NULL means 'not answered'. Compute each respondent's average rating (a) as (q1 + q2 + q3) / 3.0 and show it is NULL if any answer is missing, (b) correctly as the sum of non-NULL answers divided by the count of non-NULL answers, using COALESCE and CASE, or by unpivoting and using AVG, and (c) the average of each question across users with AVG(q1) (column-wise, NULLs ignored). Show that AVG(COALESCE(q1, 0)) changes the answer, say when treating missing as 0 is wrong, and state the answer for a respondent with all three NULL. Add the pandas df[['q1','q2','q3']].mean(axis=1), skipna and sum(min_count=1) behaviour and show it matches the SQL (b) for every row, with NaN where SQL gives NULL.
**Asked at:** SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** `(q1 + q2 + q3) / 3.0` is NULL as soon as one answer is missing, because `+` with NULL gives NULL; the correct row average is the sum of the answered questions divided by the number of answered questions, which is what `AVG` does column-wise and what `mean(axis=1)` does in pandas.

**Schema and sample data:** five respondents; NULL means "not answered".
```sql
CREATE TABLE survey(user_id INTEGER PRIMARY KEY, q1 INTEGER, q2 INTEGER, q3 INTEGER);  -- NULL = not answered
INSERT INTO survey VALUES
 (1,4,5,3),
 (2,4,NULL,2),
 (3,NULL,NULL,NULL),
 (4,5,NULL,NULL),
 (5,1,2,NULL);
```

**SQL answer:** four queries are in the Code block, identical to the text here.
```sql
SQL_A = """
SELECT user_id, (q1 + q2 + q3) / 3.0 AS avg_a FROM survey ORDER BY user_id
"""
```
That is (a), the trap.
```sql
SQL_B = """
SELECT user_id,
       (COALESCE(q1, 0) + COALESCE(q2, 0) + COALESCE(q3, 0)) * 1.0
         / NULLIF((q1 IS NOT NULL) + (q2 IS NOT NULL) + (q3 IS NOT NULL), 0) AS avg_b
FROM survey ORDER BY user_id
"""
```
That is (b). The numerator treats a missing answer as 0 only because it adds nothing; the denominator counts how many answers exist (`q1 IS NOT NULL` is 1 or 0 in SQLite, so the three flags add up). `NULLIF(count, 0)` turns an all-NULL respondent into NULL instead of a divide-by-zero. The second way to get (b) is to unpivot with `UNION ALL` and let `AVG` skip the NULLs:
```sql
SQL_B_UNPIVOT = """
SELECT user_id, AVG(score) AS avg_b2
FROM (SELECT user_id, q1 AS score FROM survey
      UNION ALL SELECT user_id, q2 FROM survey
      UNION ALL SELECT user_id, q3 FROM survey)
GROUP BY user_id ORDER BY user_id
"""
```
And (c), the column-wise averages next to the coerced version:
```sql
SQL_C = """
SELECT AVG(q1) AS q1_avg, AVG(q2) AS q2_avg, AVG(q3) AS q3_avg,
       AVG(COALESCE(q1, 0)) AS q1_avg_zero, AVG(COALESCE(q2, 0)) AS q2_avg_zero, AVG(COALESCE(q3, 0)) AS q3_avg_zero
FROM survey
"""
```
The `IS NOT NULL` addition is a SQLite (and MySQL) habit; in standard SQL write `CASE WHEN q1 IS NOT NULL THEN 1 ELSE 0 END` instead (I only ran SQLite here, not executed on other engines).

**pandas answer:**
```py
survey = pd.read_sql_query("SELECT * FROM survey", con).set_index("user_id")
qs = survey[["q1", "q2", "q3"]]
p_b = qs.mean(axis=1)                          # skipna=True by default: sum of answers / number of answers
p_a = qs.mean(axis=1, skipna=False)            # same as (q1+q2+q3)/3.0: NaN if any answer missing
p_sum = qs.sum(axis=1, min_count=1)            # NaN (not 0) when every answer is missing
p_c = qs.mean()                                # column-wise, NaN ignored
```

**Example:** by hand.
- User 1 answers 4, 5, 3: (a) and (b) both give 12 / 3 = 4.0.
- User 2 answers 4, NULL, 2: (a) is `4 + NULL + 2` = NULL. (b) is 6 / 2 = 3.0.
- User 3 answers nothing: (a) NULL; (b) 0 / NULLIF(0, 0) = NULL. The honest answer is "no average", not 0.
- User 4 answers only 5: (b) is 5.0 (one answer, so the average is that answer). User 5: (1 + 2) / 2 = 1.5.
- Columns: q1 has answers 4, 4, 5, 1, so `AVG(q1)` = 14 / 4 = 3.5; with NULL turned into 0 it is 14 / 5 = 2.8. q2 has two answers (5 and 2): 3.5 versus 7 / 5 = 1.4. q3 has two answers (3 and 2): 2.5 versus 1.0.

**Code:** run with `python3 -I`. Rows are compared in `user_id` order; SQL NULL arrives in pandas as NaN and `assert_series_equal` treats NaN positions as equal.
```python
# Q12: row-wise versus column-wise NULL in a survey (SQL vs pandas)
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE survey(user_id INTEGER PRIMARY KEY, q1 INTEGER, q2 INTEGER, q3 INTEGER);  -- NULL = not answered
INSERT INTO survey VALUES
 (1,4,5,3),
 (2,4,NULL,2),
 (3,NULL,NULL,NULL),
 (4,5,NULL,NULL),
 (5,1,2,NULL);
""")

SQL_A = """
SELECT user_id, (q1 + q2 + q3) / 3.0 AS avg_a FROM survey ORDER BY user_id
"""
SQL_B = """
SELECT user_id,
       (COALESCE(q1, 0) + COALESCE(q2, 0) + COALESCE(q3, 0)) * 1.0
         / NULLIF((q1 IS NOT NULL) + (q2 IS NOT NULL) + (q3 IS NOT NULL), 0) AS avg_b
FROM survey ORDER BY user_id
"""
SQL_B_UNPIVOT = """
SELECT user_id, AVG(score) AS avg_b2
FROM (SELECT user_id, q1 AS score FROM survey
      UNION ALL SELECT user_id, q2 FROM survey
      UNION ALL SELECT user_id, q3 FROM survey)
GROUP BY user_id ORDER BY user_id
"""
SQL_C = """
SELECT AVG(q1) AS q1_avg, AVG(q2) AS q2_avg, AVG(q3) AS q3_avg,
       AVG(COALESCE(q1, 0)) AS q1_avg_zero, AVG(COALESCE(q2, 0)) AS q2_avg_zero, AVG(COALESCE(q3, 0)) AS q3_avg_zero
FROM survey
"""
a = pd.read_sql_query(SQL_A, con)
b = pd.read_sql_query(SQL_B, con)
b2 = pd.read_sql_query(SQL_B_UNPIVOT, con)
c = pd.read_sql_query(SQL_C, con)
print("(a) (q1+q2+q3)/3.0:"); print(a.to_string(index=False))
print("(b) sum of answers / number of answers:"); print(b.to_string(index=False))
print("(b) via UNION ALL unpivot + AVG:"); print(b2.to_string(index=False))
print("(c) per question, NULLs ignored versus NULL coerced to 0:"); print(c.round(3).to_string(index=False))

survey = pd.read_sql_query("SELECT * FROM survey", con).set_index("user_id")
qs = survey[["q1", "q2", "q3"]]
p_b = qs.mean(axis=1)                          # skipna=True by default: sum of answers / number of answers
p_a = qs.mean(axis=1, skipna=False)            # same as (q1+q2+q3)/3.0: NaN if any answer missing
p_sum = qs.sum(axis=1, min_count=1)            # NaN (not 0) when every answer is missing
p_c = qs.mean()                                # column-wise, NaN ignored
print("\ndtypes:", dict(qs.dtypes.astype(str)), "(NULL made the integer columns float64)")
print("pandas mean(axis=1):", p_b.tolist())
print("pandas mean(axis=1, skipna=False):", p_a.tolist())
print("pandas sum(axis=1) default (all-NaN row gives 0.0):", qs.sum(axis=1).tolist())
print("pandas sum(axis=1, min_count=1):", p_sum.tolist())
print("pandas q1.fillna(0).mean():", qs["q1"].fillna(0).mean(), "versus q1.mean():", qs["q1"].mean())

# matches: compare rows ordered by user_id; SQL NULL arrives as NaN in pandas
pd.testing.assert_series_equal(p_b.reset_index(drop=True), b["avg_b"], check_names=False)
pd.testing.assert_series_equal(p_b.reset_index(drop=True), b2["avg_b2"], check_names=False)
pd.testing.assert_series_equal(p_a.reset_index(drop=True), a["avg_a"], check_names=False)
assert np.allclose(p_c.to_numpy(), c.loc[0, ["q1_avg", "q2_avg", "q3_avg"]].to_numpy(dtype=float))
assert b.loc[b["user_id"] == 3, "avg_b"].isna().all() and np.isnan(p_b.loc[3])
print("asserts passed (compared in user_id order; NULL in SQL equals NaN in pandas)")

# the all-NULL respondent
print("respondent 3 (all NULL): SQL (b) =", con.execute("SELECT * FROM (" + SQL_B.replace("ORDER BY user_id", "") + ") WHERE user_id = 3").fetchone()[1],
      "| pandas mean =", p_b.loc[3], "| sum(min_count=1) =", p_sum.loc[3])
print("total() and sum on all NULL:", con.execute("SELECT SUM(q1), TOTAL(q1) FROM survey WHERE user_id = 3").fetchone())
```

**Output (my run):**
```text
(a) (q1+q2+q3)/3.0:
 user_id  avg_a
       1    4.0
       2    NaN
       3    NaN
       4    NaN
       5    NaN
(b) sum of answers / number of answers:
 user_id  avg_b
       1    4.0
       2    3.0
       3    NaN
       4    5.0
       5    1.5
(b) via UNION ALL unpivot + AVG:
 user_id  avg_b2
       1     4.0
       2     3.0
       3     NaN
       4     5.0
       5     1.5
(c) per question, NULLs ignored versus NULL coerced to 0:
 q1_avg  q2_avg  q3_avg  q1_avg_zero  q2_avg_zero  q3_avg_zero
    3.5     3.5     2.5          2.8          1.4          1.0

dtypes: {'q1': 'float64', 'q2': 'float64', 'q3': 'float64'} (NULL made the integer columns float64)
pandas mean(axis=1): [4.0, 3.0, nan, 5.0, 1.5]
pandas mean(axis=1, skipna=False): [4.0, nan, nan, nan, nan]
pandas sum(axis=1) default (all-NaN row gives 0.0): [12.0, 6.0, 0.0, 5.0, 3.0]
pandas sum(axis=1, min_count=1): [12.0, 6.0, nan, 5.0, 3.0]
pandas q1.fillna(0).mean(): 2.8 versus q1.mean(): 3.5
asserts passed (compared in user_id order; NULL in SQL equals NaN in pandas)
respondent 3 (all NULL): SQL (b) = None | pandas mean = nan | sum(min_count=1) = nan
total() and sum on all NULL: (None, 0.0)
```

**Edge cases:**
- All three NULL: (b) is NULL (SQL) and NaN (pandas `mean`). Do not show it as 0 in a dashboard: that would say "this person rated everything zero".
- `SUM` over an all-NULL set is NULL, but `TOTAL` returns 0.0 (the Code block prints `(None, 0.0)`). In pandas `sum(axis=1)` returns 0.0 for an all-NaN row by default; `min_count=1` makes it NaN, which matches SQL `SUM`.
- Treating missing as 0 is wrong when 0 is not a possible rating (a 1 to 5 scale) or when "not answered" is unrelated to the opinion. It is acceptable only when NULL really means "none", for example "number of purchases".
- If the scale is 1 to 5 and someone types 0 for "skip", you have two missing markers; normalise first (`NULLIF(q1, 0)`), the same idea as the blank-to-NULL step in Q13.
- The coerced column average pulls every question toward 0 by the share of missing answers (q2: 3.5 became 1.4).
- Row-wise versus column-wise are different questions: `AVG(q1)` ignores NULL across rows; `(q1+q2+q3)` does arithmetic across columns where NULL poisons the result.
- Integer division: `(q1 + q2 + q3) / 3` without `.0` would truncate in SQLite (and in PostgreSQL, hedged: not executed); the `3.0` and `* 1.0` are deliberate.

**Then explain:**
- **Why (a) fails:** NULL is "unknown", so `4 + NULL + 2` is unknown. Aggregates like `AVG`, `SUM`, `COUNT(col)` skip NULL; operators like `+` do not.
- **Why (b) works:** the numerator uses `COALESCE(x, 0)` only to stop the poisoning (adding 0 changes nothing), while the denominator counts real answers.
- **Unpivot is the clean generalisation:** if you add `q4`, the `UNION ALL` version needs one more line, while the `COALESCE` version needs two edits. With many questions, store the answers long (`user_id, question, score`) in the first place.
- **pandas matches (b):** `mean(axis=1)` skips NaN by default (`skipna=True`); `skipna=False` reproduces (a). The columns became `float64` because NULL forced it.
- **Which one to use:** the skip-missing average, but also report the answered count, because an average over one answer is weak evidence.
- Cross-reference: aggregate and NULL basics are in Part 1 Q4 and Q5; this question is about the row-wise direction.

**Follow-ups:**
- *Average only respondents who answered at least two questions?* `HAVING` or `WHERE` on the answered count (`>= 2`).
- *Weighted average with different weights per question?* Divide the weighted sum of answered questions by the sum of the weights of the answered questions, not by the total weight.
- *Median instead of mean?* Needs the unpivot shape plus a ranking or sorting step; pandas `median(axis=1)` skips NaN.

**Common mistakes:**
- Using `(q1 + q2 + q3) / 3` and not noticing the NULLs and the integer division.
- Dividing the sum of answers by 3 (counting missing as zero) and calling it fixed.
- `AVG(COALESCE(q1, 0))` "to avoid NULL": it changes the meaning.
- Reporting an all-NULL respondent as 0, or dropping them without saying so.
- In pandas, `df.sum(axis=1)` and assuming an all-NaN row is NaN (it is 0.0 unless `min_count=1`).

### Q13 ⭐⭐⭐ 🟡 NULL versus empty string versus 0 versus the text 'NULL': customers(customer_id, name, phone, city) where missing phone is stored in four ways (NULL, '', '   ' and 'NULL' or 'N/A' text) and a numeric column credit_limit has NULL and 0. Show which predicates catch which (IS NULL, = '', TRIM(phone) = '', phone = 'NULL', COALESCE and NULLIF(TRIM(phone), '')), why WHERE phone <> '' silently drops NULL rows, and write one expression that normalises all four forms to a real NULL. Show that COUNT(phone) counts blanks and the text 'NULL' but not real NULLs, and that AVG(credit_limit) changes if NULL is coerced to 0. Add the pandas equivalent with replace, str.strip, isna and na_values in read_csv, and say which of 'NA', 'NULL', 'None' and '' pandas treats as missing by default when reading CSV (check by running). Cross-reference Part 1 Q4 and Q5 for basics.
**Asked at:** SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** They are five different things: a real NULL (unknown), an empty string, whitespace, the text `'NULL'` or `'N/A'`, and a numeric 0; each needs its own predicate, `WHERE phone <> ''` silently drops the NULL rows, and one `CASE` (or `NULLIF` chain) over a properly trimmed value turns all the missing forms into a real NULL.

**Schema and sample data:** nine customers; the phone is "missing" in six different ways, and `credit_limit` has both NULL and 0.
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, phone TEXT, city TEXT, credit_limit INTEGER);
INSERT INTO customers VALUES
 (1,'Asha','98765 43210','Pune',5000),
 (2,'Ben',NULL,'Delhi',NULL),
 (3,'Chitra','','Mumbai',0),
 (4,'Dev','   ','Pune',2000),
 (5,'Esha','NULL','Delhi',3000),
 (6,'Farid','N/A','Mumbai',NULL),
 (7,'Gita',' 98111 22222 ','Pune',1000),
 (8,'Hari',char(9),'Delhi',4000),      -- a tab only
 (9,'Ila',char(160),'Pune',0);         -- a no-break space only
```

**SQL answer:** the predicate grid and counts are in the Code block. The normaliser is one expression, identical to the Code block:
```sql
SQL_NORM = """
SELECT customer_id,
       CASE WHEN UPPER(TRIM(phone, ' ' || char(9) || char(10) || char(13) || char(160)))
                 IN ('', 'NULL', 'N/A', 'NA', 'NONE')
            THEN NULL
            ELSE TRIM(phone, ' ' || char(9) || char(10) || char(13) || char(160))
       END AS phone_clean
FROM customers ORDER BY customer_id
"""
```
- `TRIM(x, chars)` removes any of the listed characters from both ends. Plain `TRIM(phone)` strips only the space character, so the tab and NBSP rows survive it; the character set `' ' || char(9) || char(10) || char(13) || char(160)` handles space, tab, newline, carriage return and NBSP.
- `UPPER(...) IN ('', 'NULL', 'N/A', 'NA', 'NONE')` catches empty, blank and the text forms in any case. A NULL phone gives UNKNOWN in the `CASE` condition, so it falls to the `ELSE` branch, which is `TRIM(NULL, ...)` = NULL. The result is NULL for all missing forms and the trimmed string for real numbers.
- A `NULLIF` chain does the same job: `NULLIF(NULLIF(NULLIF(TRIM(phone), ''), 'NULL'), 'N/A')`; I prefer `CASE ... IN (...)` because you can add a token without nesting. Both are the standard `NULLIF` and `CASE` (see Part 1 Q6 and Q44 for those functions).

The count and average queries:
```sql
SQL_COUNTS = """
SELECT COUNT(*)                                   AS rows_total,
       COUNT(phone)                               AS count_phone,
       SUM(phone <> '')                           AS phone_ne_empty,
       (SELECT COUNT(phone_clean) FROM (""" + SQL_NORM.replace("ORDER BY customer_id", "") + """)) AS count_clean,
       AVG(credit_limit)                          AS avg_limit,
       AVG(COALESCE(credit_limit, 0))             AS avg_limit_null_as_0
FROM customers
"""
```

**pandas answer:**
```py
df = pd.read_sql_query("SELECT * FROM customers ORDER BY customer_id", con)
clean = df["phone"].str.strip()                                   # pandas strip removes tab and NBSP too
p_norm = clean.mask(clean.str.upper().isin(["", "NULL", "N/A", "NA", "NONE"]))   # NaN stays NaN (isin gives False)
```
`str.strip()` with no argument removes all Unicode whitespace, so unlike SQLite's `TRIM`, it handles the tab and NBSP rows without a character list. The `read_csv` part of the Code block checks which spellings pandas already treats as missing when reading a file.

**Example:** by hand, then the grid in the output.
- Row 2 (NULL): `phone IS NULL` is true; `phone = ''`, `phone = 'NULL'` and `phone <> ''` are all UNKNOWN, so `WHERE phone <> ''` leaves it out. That is the silent drop.
- Row 3 (`''`): `= ''` true, `TRIM(...) = ''` true, `<> ''` false.
- Row 4 (`'   '`): `= ''` false (it has three characters), but `TRIM(phone) = ''` is true; so `= ''` misses it and `<> ''` keeps it, as if it were a phone number.
- Rows 5 and 6 (`'NULL'`, `'N/A'`): real text. `IS NULL`, `= ''` and `TRIM = ''` all miss them; only `= 'NULL'` catches row 5, and row 6 needs its own predicate.
- Rows 8 and 9 (tab, NBSP): `TRIM(phone) = ''` is false for both (hex `09` and `C2A0`), which is why the normaliser uses a character set.
- Counts: `COUNT(phone)` is 8 (it skips only row 2). After normalising, only rows 1 and 7 hold a phone, so the real count is 2. `WHERE phone <> ''` returns ids 1, 4, 5, 6, 7, 8, 9: seven rows, of which five are fake phones.
- Credit limit: the values are 5000, NULL, 0, 2000, 3000, NULL, 1000, 4000, 0. `AVG` skips the two NULLs: 15000 / 7 = 2142.857. With NULL turned into 0 it is 15000 / 9 = 1666.667. The existing zeros (rows 3 and 9) stay in both, because 0 is a real value.

**Code:** run with `python3 -I`. SQL and pandas are compared in `customer_id` order (NULL equals NaN).
```python
# Q13: NULL vs '' vs blanks vs the text 'NULL' vs 0 (SQL and pandas)
import io
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, phone TEXT, city TEXT, credit_limit INTEGER);
INSERT INTO customers VALUES
 (1,'Asha','98765 43210','Pune',5000),
 (2,'Ben',NULL,'Delhi',NULL),
 (3,'Chitra','','Mumbai',0),
 (4,'Dev','   ','Pune',2000),
 (5,'Esha','NULL','Delhi',3000),
 (6,'Farid','N/A','Mumbai',NULL),
 (7,'Gita',' 98111 22222 ','Pune',1000),
 (8,'Hari',char(9),'Delhi',4000),      -- a tab only
 (9,'Ila',char(160),'Pune',0);         -- a no-break space only
""")

print("--- which predicate catches which row (1 = true, 0 = false, NULL = unknown) ---")
flags = pd.read_sql_query("""
SELECT customer_id AS id, quote(phone) AS stored, hex(phone) AS hex,
       IFNULL(phone IS NULL, 'NULL')                    AS is_null,
       IFNULL(phone = '', 'NULL')                       AS eq_empty,
       IFNULL(TRIM(phone) = '', 'NULL')                 AS trim_empty,
       IFNULL(phone = 'NULL', 'NULL')                   AS eq_text_null,
       IFNULL(NULLIF(TRIM(phone), '') IS NULL, 'NULL')  AS nullif_trim,
       IFNULL(phone <> '', 'NULL')                      AS ne_empty
FROM customers ORDER BY customer_id""", con)
print(flags.to_string(index=False))

SQL_NORM = """
SELECT customer_id,
       CASE WHEN UPPER(TRIM(phone, ' ' || char(9) || char(10) || char(13) || char(160)))
                 IN ('', 'NULL', 'N/A', 'NA', 'NONE')
            THEN NULL
            ELSE TRIM(phone, ' ' || char(9) || char(10) || char(13) || char(160))
       END AS phone_clean
FROM customers ORDER BY customer_id
"""
SQL_COUNTS = """
SELECT COUNT(*)                                   AS rows_total,
       COUNT(phone)                               AS count_phone,
       SUM(phone <> '')                           AS phone_ne_empty,
       (SELECT COUNT(phone_clean) FROM (""" + SQL_NORM.replace("ORDER BY customer_id", "") + """)) AS count_clean,
       AVG(credit_limit)                          AS avg_limit,
       AVG(COALESCE(credit_limit, 0))             AS avg_limit_null_as_0
FROM customers
"""
norm = pd.read_sql_query(SQL_NORM, con)
print("\nSQL normalised phone:"); print(norm.to_string(index=False))
counts = pd.read_sql_query(SQL_COUNTS, con)
print("\nSQL counts and averages:"); print(counts.to_string(index=False))
print("WHERE phone <> '' returns ids:", [r[0] for r in con.execute("SELECT customer_id FROM customers WHERE phone <> '' ORDER BY 1")])
print("WHERE phone IS NULL OR phone <> '' returns", con.execute("SELECT COUNT(*) FROM customers WHERE phone IS NULL OR phone <> ''").fetchone()[0], "rows")
print("WHERE TRIM(phone) = '' returns ids:", [r[0] for r in con.execute("SELECT customer_id FROM customers WHERE TRIM(phone) = '' ORDER BY 1")], "(tab and NBSP rows 8, 9 are missed)")

df = pd.read_sql_query("SELECT * FROM customers ORDER BY customer_id", con)
clean = df["phone"].str.strip()                                   # pandas strip removes tab and NBSP too
p_norm = clean.mask(clean.str.upper().isin(["", "NULL", "N/A", "NA", "NONE"]))   # NaN stays NaN (isin gives False)
print("\npandas phone dtype:", df["phone"].dtype, "| isna count after normalising:", int(p_norm.isna().sum()))
print("pandas: mean skips NaN:", df["credit_limit"].mean(), "| fillna(0).mean():", df["credit_limit"].fillna(0).mean(),
      "| count(phone) before:", int(df["phone"].count()), "after:", int(p_norm.count()))

# match: compare by customer_id order, NULL == NaN
pd.testing.assert_series_equal(p_norm.reset_index(drop=True), norm["phone_clean"], check_names=False, check_dtype=False)
assert int(df["phone"].count()) == counts.loc[0, "count_phone"] == 8
assert int(p_norm.count()) == counts.loc[0, "count_clean"] == 2
assert abs(df["credit_limit"].mean() - counts.loc[0, "avg_limit"]) < 1e-9
assert abs(df["credit_limit"].fillna(0).mean() - counts.loc[0, "avg_limit_null_as_0"]) < 1e-9
print("asserts passed (pandas matches SQL in customer_id order)")

# read_csv default NA handling: which spellings become NaN?
tokens = ["", "NULL", "N/A", "NA", "None", "nan", "NaN", "null", "n/a", "#N/A", "<NA>", "Null", "na", "NAN", "   ", "-", "0"]
csv_text = "k,v\n" + "\n".join(f'{i},"{t}"' for i, t in enumerate(tokens))
got = pd.read_csv(io.StringIO(csv_text), dtype={"v": "str"})
isna = dict(zip(tokens, got["v"].isna()))
print("\nread_csv default: parsed as missing:", [t for t in tokens if isna[t]])
print("read_csv default: kept as text     :", [t for t in tokens if not isna[t]])
got2 = pd.read_csv(io.StringIO(csv_text), dtype={"v": "str"}, keep_default_na=False, na_values=["NULL", "N/A"])
print("keep_default_na=False, na_values=['NULL','N/A'] -> missing:", [t for t, m in zip(tokens, got2["v"].isna()) if m])
assert not isna["   "] and isna["NULL"] and isna["N/A"] and isna[""] and isna["None"] and not isna["Null"]
```

**Output (my run):**
```text
--- which predicate catches which row (1 = true, 0 = false, NULL = unknown) ---
 id          stored                        hex  is_null eq_empty trim_empty eq_text_null  nullif_trim ne_empty
  1   '98765 43210'     3938373635203433323130        0        0          0            0            0        1
  2            NULL                                   1     NULL       NULL         NULL            1     NULL
  3              ''                                   0        1          1            0            1        0
  4           '   '                     202020        0        0          1            0            1        1
  5          'NULL'                   4E554C4C        0        0          0            1            0        1
  6           'N/A'                     4E2F41        0        0          0            0            0        1
  7 ' 98111 22222 ' 20393831313120323232323220        0        0          0            0            0        1
  8            '\t'                         09        0        0          0            0            0        1
  9             ' '                       C2A0        0        0          0            0            0        1

SQL normalised phone:
 customer_id phone_clean
           1 98765 43210
           2         NaN
           3         NaN
           4         NaN
           5         NaN
           6         NaN
           7 98111 22222
           8         NaN
           9         NaN

SQL counts and averages:
 rows_total  count_phone  phone_ne_empty  count_clean   avg_limit  avg_limit_null_as_0
          9            8               7            2 2142.857143          1666.666667
WHERE phone <> '' returns ids: [1, 4, 5, 6, 7, 8, 9]
WHERE phone IS NULL OR phone <> '' returns 8 rows
WHERE TRIM(phone) = '' returns ids: [3, 4] (tab and NBSP rows 8, 9 are missed)

pandas phone dtype: str | isna count after normalising: 7
pandas: mean skips NaN: 2142.8571428571427 | fillna(0).mean(): 1666.6666666666667 | count(phone) before: 8 after: 2
asserts passed (pandas matches SQL in customer_id order)

read_csv default: parsed as missing: ['', 'NULL', 'N/A', 'NA', 'None', 'nan', 'NaN', 'null', 'n/a', '#N/A', '<NA>']
read_csv default: kept as text     : ['Null', 'na', 'NAN', '   ', '-', '0']
keep_default_na=False, na_values=['NULL','N/A'] -> missing: ['NULL', 'N/A']
```
Honest notes from the run: `read_csv` with its defaults treated these spellings as missing: empty, `NULL`, `N/A`, `NA`, `None`, `nan`, `NaN`, `null`, `n/a`, `#N/A`, `<NA>`. It kept `Null`, `na`, `NAN`, a three-space string, `-` and `0` as text, so the match is case-sensitive and whitespace is not stripped. So SQL and pandas disagree on `'NULL'` and `'N/A'` text: SQL stores them as ordinary text, while `read_csv` would have made them missing before you ever see them. (In my run I read the table with `read_sql_query`, so pandas kept them as text and the normaliser matched SQL.) The default set also includes forms such as `-nan`, `1.#IND` and `-1.#QNAN`; I printed the ones I tested, not the whole internal list.

**Edge cases:**
- `credit_limit`: NULL means unknown; 0 means a real zero limit. Coercing NULL to 0 changes `AVG` from 2142.857 to 1666.667 and also changes the meaning (a customer with no limit set is not a customer with a zero limit).
- Phone numbers with only digits would be stored as TEXT; if the column were INTEGER, a leading zero could not exist.
- Case: `'null'` and `'Null'` are caught by `UPPER` in SQL; in pandas `read_csv` the default list is case-sensitive (`Null` stayed text), but my `str.upper().isin(...)` handles all cases.
- `UPPER` and `LOWER` are ASCII-only in SQLite, which is fine for these tokens.
- Uniqueness: if you add `UNIQUE(phone)`, SQLite accepts many NULLs but only one `''` (this behaviour is in the Wave A notes; other engines differ and I did not run them).
- Tokens like `'-'`, `'unknown'`, `'0000000000'` are not in the list: you need to look at the data (`GROUP BY phone ORDER BY COUNT(*) DESC`) to find the junk values.

**Then explain:**
- **NULL versus empty versus 0 versus text:** NULL is "I do not know", `''` is "known and empty", 0 is a number, `'NULL'` is a four-letter word typed by someone or exported by a bad tool. Aggregates (`COUNT(col)`, `AVG`) react to them differently, which is the whole trap.
- **Why `<> ''` drops NULL:** the comparison is UNKNOWN, `WHERE` keeps only TRUE (three-valued logic is in Part 1 Q5). If you want "has a non-empty value", test the normalised value: `NULLIF(TRIM(phone), '') IS NOT NULL`.
- **Normalise once, early:** put the `CASE` in a view or a staging step, so the rest of your queries can trust `IS NULL`.
- **pandas:** `isna()` is the one test; `read_csv(na_values=[...], keep_default_na=False)` sets the NA spellings at load time (the Code block shows `['NULL', 'N/A']` only).
- Dialect notes (not executed): other engines treat `''` differently (Oracle treats an empty string as NULL, from memory; I did not test it), and `TRIM` with a character list has different syntax (`TRIM(BOTH ... FROM ...)` in standard SQL, hedged).

**Follow-ups:**
- *How do you find all the fake-missing spellings?* Profile the column: `SELECT phone, COUNT(*) ... GROUP BY phone ORDER BY 2 DESC LIMIT 20`, then add what you find to the `IN` list.
- *Should you clean it in SQL or at load?* At load into a staging table, keep the raw column, add a `phone_clean` column, so the cleaning is auditable.
- *How do you fix the data permanently?* `UPDATE` to NULL plus a `CHECK (phone IS NULL OR TRIM(phone) <> '')` constraint (a CHECK that evaluates to NULL passes, so it will not reject NULL).

**Common mistakes:**
- `WHERE phone = NULL` instead of `IS NULL` (never true).
- `WHERE phone <> ''` and believing it returns "all customers with phones" (it loses NULL and keeps blanks and `'NULL'`).
- Counting `COUNT(phone)` as "customers with a phone".
- `TRIM(phone) = ''` and trusting it for tab or NBSP-only values in SQLite.
- `COALESCE(credit_limit, 0)` before `AVG`, which changes the answer.
- Trusting `read_csv` or `df.isna()` to have caught `'Null'` or a whitespace-only value.

### Q14 ⭐⭐⭐ 🟡 pandas pivot, pivot_table and crosstab: a DataFrame sales(region, product, month, amount) with duplicate (region, product) pairs, a NaN amount and a NaN product. Show pivot raising ValueError on duplicates, pivot_table with aggfunc ('sum', 'mean', a list and a dict), fill_value, margins=True with margins_name, dropna and observed for categorical keys, what happens to a NaN row label (dropped by default), and crosstab for counts. Explain that pivot_table aggregates NaN away (sum of all NaN is 0 for a non-empty group while the SQL SUM is NULL; show how min_count or a custom aggfunc changes it). Compare each result with the SQL SUM(CASE ...) pivot on the same data and assert they match. State the pandas version used and the observed default found by running.
**Asked at:** pandas user guide pages on reshaping and on working with text data (opened: pivot, pivot_table, melt, wide_to_long, stack, unstack, crosstab, explode, string dtype and the .str accessor); official documentation, not candidate reports; data scientist and analyst rounds; SQL pivot guides (datadriven.io, DataVidhya, Educative and a Medium write-up, search snippets only; the DataVidhya lesson page opened but showed only its introduction: CASE inside SUM or COUNT, dynamic pivot, NULL categories); guides, not candidate reports; analyst and data engineer rounds at product companies and GCCs
**Say this first (1 line):** `pivot` only reshapes and raises `ValueError` on duplicates, `pivot_table` aggregates (default mean; I use sum/mean/count), `crosstab` counts rows; in pandas 3.0.5 the sum of an all-NaN group is 0.0 while SQL `SUM` gives NULL, so to match the SQL `SUM(CASE ...)` pivot you need `min_count=1` (through a custom aggfunc) and `dropna=False`.

**Schema and sample data:** eight rows. Duplicates: East/Pen/Jan twice. A NaN amount: East/Pen/Feb and North/Pen/Jan. A NaN product: West/None/Jan. The `month` order Jan, Feb, Mar is not alphabetical, which matters later.
```sql
CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','Pen','Jan',100),('East','Pen','Jan',50),('East','Pen','Feb',NULL),
 ('East','Book','Jan',200),('West','Pen','Feb',70),('West','Book','Mar',30),
 ('West',NULL,'Jan',40),('North','Pen','Jan',NULL);
```
(The Code block inserts the same rows with `executemany`.)

**SQL answer:** four pivots over `region` (SUM with a Total column, AVG, COUNT of amounts, COUNT of rows), identical to the Code block:
```sql
SQL_SUM = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS Mar,
       SUM(amount) AS Total
FROM sales GROUP BY region ORDER BY region
"""
SQL_AVG = """
SELECT region,
       AVG(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       AVG(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       AVG(CASE WHEN month = 'Mar' THEN amount END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
SQL_COUNT_AMOUNTS = """
SELECT region,
       COUNT(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       COUNT(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       COUNT(CASE WHEN month = 'Mar' THEN amount END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
SQL_COUNT_ROWS = """
SELECT region,
       COUNT(CASE WHEN month = 'Jan' THEN 1 END) AS Jan,
       COUNT(CASE WHEN month = 'Feb' THEN 1 END) AS Feb,
       COUNT(CASE WHEN month = 'Mar' THEN 1 END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
```
(They are Python string assignments in the Code block; the SQL is the text inside the quotes.) The `CASE` sits inside the aggregate and has no `ELSE`, so rows of other months become NULL and are skipped. The pivot is on `region` only; product is ignored, so the NaN product does not matter for this SQL.

**pandas answer:** identical to the Code block:
```py
def sum_or_nan(s):                      # like SQL SUM: NaN when there is no non-NaN value
    return s.sum(min_count=1)

p_sum = (df.pivot_table(index="region", columns="month", values="amount", aggfunc=sum_or_nan, dropna=False)
           .reindex(columns=MONTHS))
p_mean = df.pivot_table(index="region", columns="month", values="amount", aggfunc="mean", dropna=False).reindex(columns=MONTHS)
p_cnt_amt = df.pivot_table(index="region", columns="month", values="amount", aggfunc="count", fill_value=0).reindex(columns=MONTHS)
p_cnt_rows = pd.crosstab(df["region"], df["month"]).reindex(columns=MONTHS, fill_value=0)
p_margins = df.pivot_table(index="region", columns="month", values="amount", aggfunc=sum_or_nan,
                           margins=True, margins_name="Total", dropna=False).reindex(columns=MONTHS + ["Total"])
```

**Example:** by hand, per region.
- East has Jan rows 100, 50, 200, a Feb row with a NaN amount, and nothing in Mar. Jan sum 350 (mean 116.667 over 3 rows, count 3). Feb: the only amount is NaN, so SQL `SUM` is NULL, `COUNT(amount)` 0, but the row count is 1. Mar: no rows at all: SUM NULL, both counts 0.
- North has one row: Jan, NaN. Every cell is NULL for sums and means; the row count for Jan is 1.
- West: Jan 40 (the NaN-product row), Feb 70, Mar 30. Total 140.
- Totals: East 350, North NULL, West 140; the grand total is 490 (`SUM(amount)` over everything).
- By product, the NaN-product row vanishes: Book 230 and Pen 220 add to 450, not 490. SQL `GROUP BY product` keeps a NULL group worth 40.

**Code:** run with `python3 -I`. Rows are compared ordered by `region`, columns in the order Jan, Feb, Mar (pandas sorts columns alphabetically as Feb, Jan, Mar unless you reindex).
```python
# Q14: pandas pivot, pivot_table, crosstab versus the SQL SUM(CASE ...) pivot
import sqlite3
import numpy as np
import pandas as pd

print("pandas", pd.__version__, "| SQLite", sqlite3.sqlite_version)
rows = [("East", "Pen", "Jan", 100), ("East", "Pen", "Jan", 50), ("East", "Pen", "Feb", None),
        ("East", "Book", "Jan", 200), ("West", "Pen", "Feb", 70), ("West", "Book", "Mar", 30),
        ("West", None, "Jan", 40), ("North", "Pen", "Jan", None)]
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER)")
con.executemany("INSERT INTO sales VALUES (?,?,?,?)", rows)
df = pd.DataFrame(rows, columns=["region", "product", "month", "amount"])
print("dtypes:", {c: str(t) for c, t in df.dtypes.items()}, "| NaN product:", df["product"].isna().sum(), "| NaN amount:", df["amount"].isna().sum())

SQL_SUM = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS Mar,
       SUM(amount) AS Total
FROM sales GROUP BY region ORDER BY region
"""
SQL_AVG = """
SELECT region,
       AVG(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       AVG(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       AVG(CASE WHEN month = 'Mar' THEN amount END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
SQL_COUNT_AMOUNTS = """
SELECT region,
       COUNT(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       COUNT(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       COUNT(CASE WHEN month = 'Mar' THEN amount END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
SQL_COUNT_ROWS = """
SELECT region,
       COUNT(CASE WHEN month = 'Jan' THEN 1 END) AS Jan,
       COUNT(CASE WHEN month = 'Feb' THEN 1 END) AS Feb,
       COUNT(CASE WHEN month = 'Mar' THEN 1 END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
MONTHS = ["Jan", "Feb", "Mar"]
def q(sql): return pd.read_sql_query(sql, con).set_index("region")
sql_sum, sql_avg, sql_cnt_amt, sql_cnt_rows = q(SQL_SUM), q(SQL_AVG), q(SQL_COUNT_AMOUNTS), q(SQL_COUNT_ROWS)
print("\nSQL SUM(CASE) pivot with Total (NULL = no non-NULL amount):"); print(sql_sum)

# 1. pivot cannot aggregate
try:
    df.pivot(index="region", columns="month", values="amount")
except ValueError as e:
    print("\npivot with duplicates -> ValueError:", e)

# the all-NaN row is dropped by default (dropna=True drops rows and columns that are entirely NaN)
no_keep = df.pivot_table(index="region", columns="month", values="amount", aggfunc=lambda s: s.sum(min_count=1))
print("min_count=1 with default dropna: regions kept =", no_keep.index.tolist(), "(North is gone)")
no_keep_mean = df.pivot_table(index="region", columns="month", values="amount", aggfunc="mean")
print("mean with default dropna: regions kept =", no_keep_mean.index.tolist())

# 2. default pivot_table: sum of an all-NaN group is 0.0, not NaN
p_default = df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
print("\npivot_table sum (default), columns come out alphabetical:"); print(p_default)
p_default = p_default.reindex(columns=MONTHS)
diff = ~np.isclose(p_default.to_numpy(float), sql_sum[MONTHS].to_numpy(float), equal_nan=True)
print("cells that differ from SQL after reindexing the months:", [(r, m) for (r, m), d in zip(
    [(r, m) for r in p_default.index for m in MONTHS], diff.ravel()) if d],
    "(pandas 0.0 where SQL has NULL)")

def sum_or_nan(s):                      # like SQL SUM: NaN when there is no non-NaN value
    return s.sum(min_count=1)

p_sum = (df.pivot_table(index="region", columns="month", values="amount", aggfunc=sum_or_nan, dropna=False)
           .reindex(columns=MONTHS))
p_mean = df.pivot_table(index="region", columns="month", values="amount", aggfunc="mean", dropna=False).reindex(columns=MONTHS)
p_cnt_amt = df.pivot_table(index="region", columns="month", values="amount", aggfunc="count", fill_value=0).reindex(columns=MONTHS)
p_cnt_rows = pd.crosstab(df["region"], df["month"]).reindex(columns=MONTHS, fill_value=0)
p_margins = df.pivot_table(index="region", columns="month", values="amount", aggfunc=sum_or_nan,
                           margins=True, margins_name="Total", dropna=False).reindex(columns=MONTHS + ["Total"])
for p in (p_sum, p_mean, p_cnt_amt, p_cnt_rows, p_margins):
    p.columns.name = None
    p.index.name = "region"

print("\nsum with min_count=1 and dropna=False:"); print(p_sum)
print("\nmargins=True, margins_name='Total':"); print(p_margins)
print("\nmean:"); print(p_mean.round(3))
print("\ncount of non-NaN amounts, fill_value=0:"); print(p_cnt_amt)
print("\ncrosstab (row counts):"); print(p_cnt_rows)

# comparisons, rows ordered by region, columns Jan, Feb, Mar
pd.testing.assert_frame_equal(p_sum, sql_sum[MONTHS], check_dtype=False)
pd.testing.assert_frame_equal(p_mean, sql_avg[MONTHS], check_dtype=False)
pd.testing.assert_frame_equal(p_cnt_amt, sql_cnt_amt[MONTHS], check_dtype=False)
pd.testing.assert_frame_equal(p_cnt_rows, sql_cnt_rows[MONTHS], check_dtype=False)
pd.testing.assert_series_equal(p_margins.loc[sql_sum.index, "Total"], sql_sum["Total"], check_dtype=False)
assert p_margins.loc["Total", "Total"] == con.execute("SELECT SUM(amount) FROM sales").fetchone()[0] == 490
print("\nasserts passed: sum, mean, count, crosstab and margins match the SQL pivot (rows by region, columns Jan Feb Mar)")

# list and dict aggfunc, fill_value
gb = (df.groupby(["region", "month"])["amount"].sum(min_count=1).unstack().reindex(columns=MONTHS))
pd.testing.assert_frame_equal(gb, sql_sum[MONTHS], check_dtype=False, check_names=False)
print("groupby(['region','month'])['amount'].sum(min_count=1).unstack() also equals the SQL sum pivot (North kept)")
m1 = df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", margins=True, margins_name="Total")
m2 = df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", margins=True, margins_name="Total", dropna=False)
print("default sum margins, North Total: dropna=True ->", m1.loc["North", "Total"], "| dropna=False ->", m2.loc["North", "Total"], "(SQL SUM is NULL)")

print("\naggfunc=['sum','mean'] columns:", df.pivot_table(index="region", columns="month", values="amount", aggfunc=["sum", "mean"]).columns.tolist()[:3], "...")
print("aggfunc={'amount': ['sum','count']} column levels:", df.pivot_table(index="region", columns="month", values="amount",
      aggfunc={"amount": ["sum", "count"]}).columns.nlevels)
print("fill_value=0 on the default sum turns every NaN cell into 0:", df.pivot_table(index="region", columns="month",
      values="amount", aggfunc="sum", fill_value=0).to_numpy().tolist())

# NaN row label
by_prod = df.pivot_table(index="product", columns="month", values="amount", aggfunc="sum")
print("\nindex='product' (default): labels", by_prod.index.tolist(), "| total", by_prod.sum().sum(), "(the NaN-product 40 vanished; region total is 490)")
by_prod2 = df.pivot_table(index="product", columns="month", values="amount", aggfunc="sum", dropna=False)
print("index='product', dropna=False: labels", by_prod2.index.tolist(), "| total", by_prod2.sum().sum())
print("crosstab on product default rows:", pd.crosstab(df["product"], df["month"]).index.tolist(),
      "| dropna=False:", pd.crosstab(df["product"], df["month"], dropna=False).index.tolist())
sql_prod = con.execute("SELECT product, SUM(amount) FROM sales GROUP BY product ORDER BY product").fetchall()
print("SQL GROUP BY product keeps the NULL group:", sql_prod)

# categorical month with an unobserved category
cat = df.assign(month=pd.Categorical(df["month"], categories=MONTHS + ["Apr"]))
a = cat.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
b = cat.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", observed=False)
print("\ncategorical month with unused 'Apr': default columns", a.columns.tolist(), "| observed=False columns", b.columns.tolist(),
      "| Apr cells:", b["Apr"].tolist())
assert a.columns.tolist() == MONTHS and "Apr" in b.columns
print("asserts passed (categorical)")
```

**Output (my run):** pandas 3.0.5 and SQLite 3.45.1.
```text
pandas 3.0.5 | SQLite 3.45.1
dtypes: {'region': 'str', 'product': 'str', 'month': 'str', 'amount': 'float64'} | NaN product: 1 | NaN amount: 2

SQL SUM(CASE) pivot with Total (NULL = no non-NULL amount):
          Jan   Feb   Mar  Total
region                          
East    350.0   NaN   NaN  350.0
North     NaN   NaN   NaN    NaN
West     40.0  70.0  30.0  140.0

pivot with duplicates -> ValueError: Index contains duplicate entries, cannot reshape
min_count=1 with default dropna: regions kept = ['East', 'West'] (North is gone)
mean with default dropna: regions kept = ['East', 'West']

pivot_table sum (default), columns come out alphabetical:
month    Feb    Jan   Mar
region                   
East     0.0  350.0   NaN
North    NaN    0.0   NaN
West    70.0   40.0  30.0
cells that differ from SQL after reindexing the months: [('East', 'Feb'), ('North', 'Jan')] (pandas 0.0 where SQL has NULL)

sum with min_count=1 and dropna=False:
          Jan   Feb   Mar
region                   
East    350.0   NaN   NaN
North     NaN   NaN   NaN
West     40.0  70.0  30.0

margins=True, margins_name='Total':
          Jan   Feb   Mar  Total
region                          
East    350.0   NaN   NaN  350.0
North     NaN   NaN   NaN    NaN
West     40.0  70.0  30.0  140.0
Total   390.0  70.0  30.0  490.0

mean:
            Jan   Feb   Mar
region                     
East    116.667   NaN   NaN
North       NaN   NaN   NaN
West     40.000  70.0  30.0

count of non-NaN amounts, fill_value=0:
        Jan  Feb  Mar
region               
East      3    0    0
North     0    0    0
West      1    1    1

crosstab (row counts):
        Jan  Feb  Mar
region               
East      3    1    0
North     1    0    0
West      1    1    1

asserts passed: sum, mean, count, crosstab and margins match the SQL pivot (rows by region, columns Jan Feb Mar)
groupby(['region','month'])['amount'].sum(min_count=1).unstack() also equals the SQL sum pivot (North kept)
default sum margins, North Total: dropna=True -> nan | dropna=False -> 0.0 (SQL SUM is NULL)

aggfunc=['sum','mean'] columns: [('sum', 'Feb'), ('sum', 'Jan'), ('sum', 'Mar')] ...
aggfunc={'amount': ['sum','count']} column levels: 2
fill_value=0 on the default sum turns every NaN cell into 0: [[0.0, 350.0, 0.0], [0.0, 0.0, 0.0], [70.0, 40.0, 30.0]]

index='product' (default): labels ['Book', 'Pen'] | total 450.0 (the NaN-product 40 vanished; region total is 490)
index='product', dropna=False: labels ['Book', 'Pen', nan] | total 490.0
crosstab on product default rows: ['Book', 'Pen'] | dropna=False: ['Book', 'Pen', nan]
SQL GROUP BY product keeps the NULL group: [(None, 40), ('Book', 230), ('Pen', 220)]

categorical month with unused 'Apr': default columns ['Jan', 'Feb', 'Mar'] | observed=False columns ['Jan', 'Feb', 'Mar', 'Apr'] | Apr cells: [0.0, 0.0, 0.0]
asserts passed (categorical)
```

**Edge cases:**
- **All-NaN group:** default `pivot_table(aggfunc="sum")` gives 0.0 for East/Feb and North/Jan (two cells differ from SQL, listed in the output) but NaN for East/Mar, because no rows exist for that cell. So pandas has two kinds of empty: "rows existed but all NaN" (0.0) and "no rows" (NaN); SQL gives NULL for both.
- **`min_count=1`:** the aggfunc `s.sum(min_count=1)` makes the first kind NaN, like SQL. But with the default `dropna=True`, a region whose cells are all NaN (North) is dropped from the result: I printed `regions kept = ['East', 'West']`. `dropna=False` keeps it. The same row loss happens for `mean` (North is dropped by default).
- **Margins:** `margins=True` adds a row and column called `All`, or the name you give in `margins_name` (I used `Total`). The margin cells use the same aggfunc, so with `sum_or_nan` North's Total is NaN, matching SQL `SUM(amount)`. With the plain `"sum"` aggfunc the margin for North depends on `dropna` (the output prints NaN for the default and 0.0 for `dropna=False`, while SQL `SUM` is NULL), so use the same aggfunc and flags for the body and the margins and check the totals.
- **NaN row label:** the NaN product is dropped from the index by default (labels `['Book', 'Pen']`, total 450). With `dropna=False` it appears as a `NaN` label (total 490). `crosstab` behaves the same way (its `dropna=False` shows the NaN row).
- **Categorical keys:** with an unused category `Apr`, the default (`observed=True` in pandas 3.0.5, checked by running) shows only Jan, Feb, Mar; `observed=False` adds an `Apr` column filled with 0.0 (the sum of an empty group), not NaN.
- **`pivot` with duplicates:** `ValueError: Index contains duplicate entries, cannot reshape`. `pivot` is for data that is already unique per (index, columns) pair; otherwise `pivot_table` or `groupby().sum().unstack()`.
- **`fill_value=0`:** applies after aggregation and turns every empty cell, including genuinely missing ones, into 0. Fine for counts, misleading for sums or means.
- **List or dict `aggfunc`:** a list gives a column MultiIndex with the function name on top (`('sum', 'Feb')`...); a dict `{'amount': ['sum', 'count']}` gives two levels. SQL needs one `CASE` aggregate per cell.
- Columns are sorted alphabetically (`Feb, Jan, Mar`): use a Categorical month or `reindex` (I used `reindex`).

**Then explain:**
- **`pivot` versus `pivot_table` versus `crosstab`:** `pivot` = reshape, no aggregation. `pivot_table` = `groupby` + aggregate + `unstack`, with `fill_value`, `margins` and `dropna`. `crosstab` = a counts table (or an aggregate when you pass `values` and `aggfunc`) built from separate Series, handy when the data is not in one frame.
- **What matches SQL:** with `min_count=1` and `dropna=False` the sum pivot equals `SUM(CASE ...)` cell for cell; `mean` equals `AVG(CASE ...)` once North is kept; `count` equals `COUNT(CASE ... THEN amount END)` (fill_value=0, because pandas gives NaN for a cell with no rows and SQL gives 0); `crosstab` equals `COUNT(CASE ... THEN 1 END)`. All of that is asserted in the Code block.
- **Why the difference exists:** pandas `sum` has `min_count=0` by default, so the sum of nothing is 0; SQL says the sum of no non-NULL values is NULL (Part 1 Q4 has the SQL side). Choose deliberately: NaN means "no data", 0 means "data summing to zero".
- Same results in SQL by `SUM(amount) FILTER (WHERE month = 'Jan')` is Q16.
- The pandas docs page I opened covers pivot, pivot_table, margins, crosstab; `dropna`, `observed` and `fill_value` behaviour above was checked by running, not from that page.

**Follow-ups:**
- *Percent of row total?* `pd.crosstab(..., normalize="index")`; in SQL divide each cell by the region total.
- *Pivot with multiple value columns?* `values=["amount", "qty"]` in pandas; in SQL one `CASE` per cell per measure.
- *Why not `groupby().sum().unstack()`?* It is the same thing with explicit control: `df.groupby(["region","month"])["amount"].sum(min_count=1).unstack()` kept North and matched the SQL sum pivot (asserted in the Code block).

**Common mistakes:**
- Using `pivot` on data with duplicates.
- Expecting `pivot_table` to keep rows or columns that are entirely NaN.
- Trusting the 0.0 in a pivot cell as "no sales" when the real state is "amount unknown".
- Losing rows with a NaN key (a product with no name) and having a total that no longer ties to the source.
- Comparing to SQL without sorting the months (`Feb Jan Mar`).
- `fill_value=0` hiding genuinely missing data.
- Writing `df.product` for the column: it is the `DataFrame.product` method, use `df["product"]`.

### Q15 ⭐⭐⭐ 🟡 Missing values in pandas versus SQL, and the pandas 3 string dtype: a Series built from ['a', None, np.nan, 'B', ''] and a DataFrame column with the same values. Report by running on the installed pandas 3.0.x: the inferred dtype (str), what marker a missing string holds (NaN, not None), how isna, == and != behave, how the .str accessor treats missing values (propagates NaN, returns float for .str.len), what dtype='string' (pd.NA, nullable) and dtype=object do differently, what happens with mixed types, and what bool(pd.NA) does. Compare with SQL NULL (NULL = NULL is NULL, NaN == NaN is False, pd.NA == pd.NA is pd.NA) and say which of those you would use in a data pipeline. Include the astype(str) trap on missing values.
**Asked at:** pandas user guide pages on reshaping and on working with text data (opened: pivot, pivot_table, melt, wide_to_long, stack, unstack, crosstab, explode, string dtype and the .str accessor); official documentation, not candidate reports; data scientist and analyst rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** In pandas 3.0.5 a list of strings with None infers the `str` dtype, and every missing value is stored as NaN (the None is converted); NaN is not equal to anything (not even itself) but `!=` says True for it, whereas SQL NULL makes both `=` and `<>` UNKNOWN; the nullable `string` dtype (marker `pd.NA`) is the one that behaves like SQL.

**Schema and sample data:** five values, entered as a Series, as a DataFrame column, and as a SQLite table (Python `None` and NaN both become NULL).
```sql
CREATE TABLE v(id INTEGER PRIMARY KEY, x TEXT);
-- ids 0..4 hold: 'a', NULL, NULL, 'B', ''
```
```py
s = pd.Series(vals)                      # inferred dtype: str (pandas 3 default)
df = pd.DataFrame({"x": vals})           # the same inference inside a DataFrame column
t = pd.Series(vals, dtype="string")      # nullable string dtype, missing marker pd.NA
o = pd.Series(vals, dtype=object)        # legacy object dtype, keeps None and NaN as given
```

**SQL answer:** four tiny queries, run in the Code block: `SELECT x IS NULL FROM v`, `SELECT x = 'a' FROM v`, `SELECT id FROM v WHERE x <> 'a'`, and `SELECT LENGTH(x) FROM v`, plus the scalar test `SELECT NULL = NULL, NULL IS NULL, NULL IS NOT DISTINCT FROM NULL, 'a' || NULL` (all ordered by `id`).

**pandas answer:** the Series construction above, then `isna()`, `==`, `!=`, `.str.len()`, `.str.upper()`; the SQL-like filter is `(s != "a") & s.notna()` for the `str` dtype or `(t != "a").fillna(False)` for the `string` dtype.

**Example:** by hand on the five values `'a'`, missing, missing, `'B'`, `''`.
- SQL `x = 'a'` gives true, NULL, NULL, false, false. `WHERE x <> 'a'` keeps only ids 3 and 4 (`'B'` and `''`): the two NULL rows are neither equal nor unequal.
- pandas `str` dtype: `s != 'a'` is `[False, True, True, True, True]`, so the two missing rows are included. This is the opposite of SQL and the most common silent bug when translating a filter.
- pandas `string` dtype: `t != 'a'` is `[False, <NA>, <NA>, True, True]`; using it as a mask treats NA as False, and the result is ids 3 and 4, same as SQL.
- Lengths: SQL `LENGTH` is `[1, NULL, NULL, 1, 0]`; pandas `str` gives `[1.0, nan, nan, 1.0, 0.0]` (float64 because NaN forces it); `string` gives `[1, <NA>, <NA>, 1, 0]` (Int64).
- The empty string is not missing in either world: length 0, `isna` False.

**Code:** run with `python3 -I`. Rows are compared in `id` order.
```python
# Q15: missing values in pandas 3 (str dtype) versus SQL NULL
import sqlite3
import numpy as np
import pandas as pd

print("pandas", pd.__version__, "| SQLite", sqlite3.sqlite_version)
vals = ["a", None, np.nan, "B", ""]

s = pd.Series(vals)                      # inferred dtype: str (pandas 3 default)
df = pd.DataFrame({"x": vals})           # the same inference inside a DataFrame column
t = pd.Series(vals, dtype="string")      # nullable string dtype, missing marker pd.NA
o = pd.Series(vals, dtype=object)        # legacy object dtype, keeps None and NaN as given
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
```

**Output (my run):**
```text
pandas 3.0.5 | SQLite 3.45.1

inferred dtypes: Series str | DataFrame column str | string: string | object: object
str    : ['a', nan, nan, 'B', '']  (None became NaN)
string : ['a', <NA>, <NA>, 'B', '']
object : ['a', None, nan, 'B', '']
isna   str/string/object: [False, True, True, False, False] [False, True, True, False, False] [False, True, True, False, False]
== 'a' str   : [True, False, False, False, False]
== 'a' string: [True, <NA>, <NA>, False, False]
!= 'a' str   : [False, True, True, True, True] <- missing counts as 'not equal'
!= 'a' string: [False, <NA>, <NA>, True, True] <- missing stays missing
s == s (NaN with itself): [True, False, False, True, True] | t == t: [True, <NA>, <NA>, True, True]
.str.len() str: [1.0, nan, nan, 1.0, 0.0] float64 | string: [1, <NA>, <NA>, 1, 0] Int64
.str.upper() str: ['A', nan, nan, 'B', ''] | object: ['A', None, nan, 'B', '']
s + '!' str: ['a!', nan, nan, 'B!', '!'] | string: ['a!', <NA>, <NA>, 'B!', '!']
str.cat(sep='|') skips missing: 'a|B|'

NaN == NaN: False | None == None: True | pd.NA == pd.NA: <NA>
bool(pd.NA) -> TypeError: boolean value of NA is ambiguous
pd.isna of None, NaN, pd.NA, '', 'NaN': [True, True, True, False, False]

mixed ['a', 1, None] dtype: object | .str.upper(): ['A', nan, None] (the integer 1 becomes NaN, not '1')
ints .str -> AttributeError: Can only use .str accessor with string values, not integer

astype(str) on the str Series      : ['a', nan, nan, 'B', ''] str
astype(str) on float [1.0, NaN]    : ['1.0', nan]
astype(str) on object ['a', None]  : ['a', nan]
.map(str) on object ['a', None]    : ['a', 'None']
numpy astype(str) on [a, None, nan]: ['a', 'None', 'nan']
f-string / str() on NaN            : ['a', 'None', 'nan', 'B', '']

SQL x IS NULL      : [0, 1, 1, 0, 0]
SQL x = 'a'        : [1, None, None, 0, 0] (Python None = SQL NULL)
SQL WHERE x <> 'a' : ids [3, 4] (NULL rows are not returned)
SQL LENGTH(x)      : [1, None, None, 1, 0]
SQL NULL = NULL, NULL IS NULL, IS NOT DISTINCT FROM, 'a'||NULL: (None, 1, 1, None)

sort_values() default puts missing last: ['', 'B', 'a', nan, nan] | na_position='first': [nan, nan, '', 'B', 'a']
read_sql_query x dtype: str | after convert_dtypes(): string ['a', <NA>, <NA>, 'B', '']

asserts passed (compared in id order: isna flags, '<>' rows, '=' flags, lengths)
```
Honest notes from the run:
- **Premise corrected on `astype(str)`:** in pandas 3.0.5 `astype(str)` no longer turns missing values into the text `'nan'` or `'None'`: it maps to the `str` dtype and keeps NaN (the run shows `['a', nan, nan, 'B', '']`, also for a float column and an object column). The trap now lives elsewhere: `.map(str)`, `.apply(str)`, f-strings and numpy's `astype(str)` all produced `'None'` or `'nan'` text in my run. From memory, pandas 2.x `astype(str)` produced those strings; I did not run pandas 2 here.
- In the mixed Series `['a', 1, None]` (dtype object), `.str.upper()` turned the integer `1` into NaN instead of `'1'`.
- `None == None` is True in plain Python (it is not SQL).

**Edge cases:**
- **Empty string versus missing:** `''` is a value: `isna` is False, `LENGTH` is 0. Strings like `'NaN'` and `'NULL'` are also just text (`pd.isna('NaN')` is False in the run); see Q13 for converting such text to real missing values.
- **Missing in the key of a group-by or join:** SQL puts NULLs in one group in `GROUP BY` and never matches NULL keys in joins; the pandas side is covered in Part 1 Q16 and Part 2 Q35 and not repeated here.
- **`str.cat` and `+`:** `str.cat(sep='|')` skips missing values (result `'a|B|'`), while `s + '!'` propagates them, like SQL `||` does with NULL (`'a' || NULL` is NULL in the run). SQL `concat()` and `concat_ws` skip NULL in SQLite 3.45.1 (Wave A run), so there are both behaviours in SQL as well.
- **Sorting:** pandas `sort_values` puts missing last by default (`na_position`); SQL NULL ordering is covered in Part 1 Q14.
- **`bool(pd.NA)` raises:** `TypeError: boolean value of NA is ambiguous`, so `if s[0] == "a":` on a `string` Series with an NA crashes, while on the `str` dtype it silently takes the False branch.

**Then explain:**
- **What marker, what dtype:** `str` dtype uses NaN (a float that is "not a number") as the missing marker; `string` uses `pd.NA`; `object` keeps whatever you put (None and NaN differ there). `isna()` treats None, NaN and pd.NA the same, so always test with `isna`, never with `== np.nan` or `is None`.
- **Comparisons:**

| | SQL NULL | `str` (NaN) | `string` (pd.NA) |
|---|---|---|---|
| `x == x` for a missing value | NULL (UNKNOWN) | False | `<NA>` |
| `x != 'a'` for a missing value | NULL | True | `<NA>` |
| `x == x` for NaN scalars | not applicable | `np.nan == np.nan` is False | `pd.NA == pd.NA` is `<NA>` |
| `.str.len()` of missing | NULL | NaN (result is float64) | `<NA>` (Int64) |
| used in `if` or `bool()` | not allowed | False branch | TypeError |

- **Which to use in a pipeline (my opinion, not a rule):** convert key columns to `string` (or `Int64`) at the boundary if you want SQL-like three-valued logic and loud failures; keep the default `str` dtype for speed and simplicity, but then every filter needs an explicit `notna()`, and you must decide what a missing value means before you compare. Never use `==` on missing values.
- **SQL side:** `NULL IS NOT DISTINCT FROM NULL` is TRUE in SQLite 3.45.1 (printed above); Part 1 Q41 covers null-safe equality.

**Follow-ups:**
- *Why did `.str.len()` return floats?* A NaN cannot live in an integer NumPy column, so pandas upcasts to float64; the nullable `string` dtype returns `Int64` instead.
- *What does `fillna('')` do?* It makes missing and empty the same; fine for display, wrong when "unknown" and "empty" mean different things.
- *How do you read a SQL NULL into pandas with the nullable types?* `convert_dtypes()` or `astype('string')` after `read_sql_query`; the Code block prints the dtype after `convert_dtypes()`.

**Common mistakes:**
- Filtering with `df[df.col != 'x']` and expecting SQL behaviour: the missing rows are kept.
- Testing `value == np.nan` (always False) or `value is None` (misses NaN).
- Assuming `astype(str)` produces `'nan'`, or that `.map(str)` is safe: it is the other way round in pandas 3.0.5.
- Treating NaN and empty string as the same thing, or `'NaN'` text as missing.
- Using `if series_value:` on `pd.NA`.

### Q16 ⭐⭐ 🟢 SQLite has no PIVOT or UNPIVOT: what do the other engines offer and what is portable? sales(region, product, month, amount). Show the portable SUM(CASE ...) pivot (executed), the SQLite FILTER (WHERE ...) form SUM(amount) FILTER (WHERE month = 'Jan') (executed), and then, hedged as not executed, SQL Server and Oracle PIVOT (aggregate FOR column IN (list)), Snowflake PIVOT (and its dynamic ANY form, hedged), BigQuery PIVOT, PostgreSQL crosstab from tablefunc and FILTER, and MySQL (no PIVOT, CASE only). Explain why the IN list must be a fixed list in most engines and why that makes pivots hard to make dynamic. Include the one-line interview answer for 'write a pivot' when the engine is unknown.
**Asked at:** SQL pivot guides (datadriven.io, DataVidhya, Educative and a Medium write-up, search snippets only; the DataVidhya lesson page opened but showed only its introduction: CASE inside SUM or COUNT, dynamic pivot, NULL categories); guides, not candidate reports; analyst and data engineer rounds at product companies and GCCs; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** SQLite and MySQL have no `PIVOT`, so the portable answer for "write a pivot" when the engine is unknown is `SUM(CASE WHEN col = 'x' THEN val END)` per output column with `GROUP BY` on the row key; SQL Server, Oracle, Snowflake and BigQuery have a `PIVOT` clause (not executed here), and all of them need the output columns listed up front.

**Schema and sample data:** six sales rows over three months.
```sql
CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','Pen','Jan',100),('East','Pen','Jan',50),('East','Book','Feb',200),
 ('West','Pen','Feb',70),('West','Book','Mar',30),('North','Pen','Jan',10);
```

**SQL answer:** two executed forms, identical to the Code block.
```sql
SQL_CASE = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
```
```sql
SQL_FILTER = """
SELECT region,
       SUM(amount) FILTER (WHERE month = 'Jan') AS Jan,
       SUM(amount) FILTER (WHERE month = 'Feb') AS Feb,
       SUM(amount) FILTER (WHERE month = 'Mar') AS Mar
FROM sales GROUP BY region ORDER BY region
"""
```
The `CASE` has no `ELSE`, so cells with no matching rows are NULL, which is what a pivot should show (no data). `FILTER (WHERE ...)` after an aggregate is standard SQL; SQLite supports it (I believe since 3.30; it ran on 3.45.1 here); PostgreSQL has it too (hedged, not executed), MySQL does not, so `CASE` is the one that works everywhere.

Dialect forms, all **not executed here** and written from memory of the documentation:
- SQL Server and Oracle: `SELECT * FROM (SELECT region, month, amount FROM sales) AS src PIVOT (SUM(amount) FOR month IN ([Jan], [Feb], [Mar])) AS p` (SQL Server uses square brackets for the column names, Oracle uses string literals like `'Jan'` and an optional alias per column). Oracle also has `UNPIVOT`.
- Snowflake: `SELECT * FROM sales PIVOT (SUM(amount) FOR month IN ('Jan','Feb','Mar'))`; I believe newer Snowflake versions accept `IN (ANY ...)` or a subquery to make it dynamic, but I did not verify that, so do not quote it as fact.
- BigQuery: `FROM sales PIVOT (SUM(amount) FOR month IN ('Jan','Feb','Mar'))` with a fixed list as well.
- PostgreSQL: the `crosstab` function from the `tablefunc` extension (the column list has to be declared in the `AS ct(...)` clause) or `SUM(...) FILTER (WHERE ...)` as above.
- MySQL: no `PIVOT`; use `SUM(CASE ...)` or `SUM(IF(month = 'Jan', amount, NULL))`.

**pandas answer:** identical to the Code block:
```py
MONTHS = ["Jan", "Feb", "Mar"]
sales = pd.read_sql_query("SELECT * FROM sales", con)
p = (sales.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
          .reindex(columns=MONTHS).reset_index())
p.columns.name = None
```

**Example:** by hand. East has Jan rows 100 and 50 (sum 150), Feb 200, no March rows. North has only Jan 10. West has Feb 70 and Mar 30. So the pivot is East 150 / 200 / NULL, North 10 / NULL / NULL, West NULL / 70 / 30. Pandas shows the NULLs as NaN and the integer columns as float64 for that reason. The `FILTER` form gives the same cells; pandas `pivot_table` gives the same table once the month columns are put back in Jan, Feb, Mar order (it sorts them alphabetically otherwise).

**Code:** run with `python3 -I`. Rows are compared by `region`, columns Jan, Feb, Mar (then Jan to Apr after the new month arrives).
```python
# Q16: SQLite has no PIVOT: SUM(CASE), FILTER, a generated (dynamic) pivot, and pandas
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','Pen','Jan',100),('East','Pen','Jan',50),('East','Book','Feb',200),
 ('West','Pen','Feb',70),('West','Book','Mar',30),('North','Pen','Jan',10);
""")
print("SQLite", sqlite3.sqlite_version)
try:
    con.execute("SELECT * FROM sales PIVOT (SUM(amount) FOR month IN ('Jan','Feb','Mar'))")
except sqlite3.Error as e:
    print("PIVOT keyword in SQLite ->", type(e).__name__ + ":", e)

SQL_CASE = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS Jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS Feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS Mar
FROM sales GROUP BY region ORDER BY region
"""
SQL_FILTER = """
SELECT region,
       SUM(amount) FILTER (WHERE month = 'Jan') AS Jan,
       SUM(amount) FILTER (WHERE month = 'Feb') AS Feb,
       SUM(amount) FILTER (WHERE month = 'Mar') AS Mar
FROM sales GROUP BY region ORDER BY region
"""
case_df = pd.read_sql_query(SQL_CASE, con)
filter_df = pd.read_sql_query(SQL_FILTER, con)
print("\nSUM(CASE ...) pivot:"); print(case_df.to_string(index=False))
pd.testing.assert_frame_equal(case_df, filter_df)
print("FILTER (WHERE ...) form returns the identical table")

MONTHS = ["Jan", "Feb", "Mar"]
sales = pd.read_sql_query("SELECT * FROM sales", con)
p = (sales.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
          .reindex(columns=MONTHS).reset_index())
p.columns.name = None
pd.testing.assert_frame_equal(p, case_df, check_dtype=False)
print("pandas pivot_table equals the SQL pivot (rows by region, columns Jan Feb Mar)")

# a new month arrives: the fixed IN list silently ignores it
con.execute("INSERT INTO sales VALUES ('East','Pen','Apr',500)")
fixed_total = pd.read_sql_query(SQL_CASE, con)[["Jan", "Feb", "Mar"]].sum().sum()
real_total = con.execute("SELECT SUM(amount) FROM sales").fetchone()[0]
print("\nafter inserting an Apr row: pivot columns add up to", fixed_total, "but SUM(amount) is", real_total)
print("audit query, months the fixed pivot does not cover:",
      con.execute("SELECT month, SUM(amount) FROM sales WHERE month NOT IN ('Jan','Feb','Mar') GROUP BY month").fetchall())

def build_pivot_sql(con):
    # month values come from the data; quote them as literals ('' doubling) and as identifiers ("" doubling)
    months = [r[0] for r in con.execute(
        "SELECT DISTINCT month FROM sales WHERE month IS NOT NULL "
        "ORDER BY INSTR('JanFebMarAprMayJunJulAugSepOctNovDec', month)")]
    lit = lambda v: "'" + v.replace("'", "''") + "'"
    ident = lambda v: '"' + v.replace('"', '""') + '"'
    cols = ",\n       ".join(f"SUM(CASE WHEN month = {lit(m)} THEN amount END) AS {ident(m)}" for m in months)
    return f"SELECT region,\n       {cols}\nFROM sales GROUP BY region ORDER BY region", months
dyn_sql, months_now = build_pivot_sql(con)
print("\ngenerated SQL text:"); print(dyn_sql)
dyn_df = pd.read_sql_query(dyn_sql, con)
print(dyn_df.to_string(index=False))
sales2 = pd.read_sql_query("SELECT * FROM sales", con)
p2 = (sales2.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
            .reindex(columns=months_now).reset_index())
p2.columns.name = None
pd.testing.assert_frame_equal(p2, dyn_df, check_dtype=False)
assert months_now == ["Jan", "Feb", "Mar", "Apr"]
print("generated pivot equals pandas pivot_table with Apr included (rows by region)")

# a hostile value is neutralised by the quoting
con.execute("INSERT INTO sales VALUES ('East','Pen','X'' OR 1=1 --',1)")
hostile_sql, _ = build_pivot_sql(con)
pd.read_sql_query(hostile_sql, con)
print("month value with a quote still produces valid SQL:")
print(next(l for l in hostile_sql.splitlines() if "1=1" in l).strip())

try:
    con.execute("SELECT region, SUM(amount) FROM sales GROUP BY GROUPING SETS ((region), ())")
except sqlite3.Error as e:
    print("GROUPING SETS in SQLite ->", type(e).__name__ + ":", e)
```

**Output (my run):**
```text
SQLite 3.45.1
PIVOT keyword in SQLite -> OperationalError: near "(": syntax error

SUM(CASE ...) pivot:
region   Jan   Feb  Mar
  East 150.0 200.0  NaN
 North  10.0   NaN  NaN
  West   NaN  70.0 30.0
FILTER (WHERE ...) form returns the identical table
pandas pivot_table equals the SQL pivot (rows by region, columns Jan Feb Mar)

after inserting an Apr row: pivot columns add up to 460.0 but SUM(amount) is 960
audit query, months the fixed pivot does not cover: [('Apr', 500)]

generated SQL text:
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS "Jan",
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS "Feb",
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS "Mar",
       SUM(CASE WHEN month = 'Apr' THEN amount END) AS "Apr"
FROM sales GROUP BY region ORDER BY region
region   Jan   Feb  Mar   Apr
  East 150.0 200.0  NaN 500.0
 North  10.0   NaN  NaN   NaN
  West   NaN  70.0 30.0   NaN
generated pivot equals pandas pivot_table with Apr included (rows by region)
month value with a quote still produces valid SQL:
SUM(CASE WHEN month = 'X'' OR 1=1 --' THEN amount END) AS "X' OR 1=1 --",
GROUPING SETS in SQLite -> OperationalError: near "SETS": syntax error
```

**Edge cases:**
- **Why the IN list must be fixed:** the number and names of the output columns are part of the query's result schema, which the database must know when it plans the query, before it reads any data. A `PIVOT` clause, a `SUM(CASE)` list and a `crosstab` column definition all fix the columns at parse time. That is why a new month does not appear automatically: in the run, after an April row was inserted, the three pivot columns added up to 460 while `SUM(amount)` was 960; the audit query found the missing `Apr`, 500.
- **Dynamic pivot:** generate the SQL text from `SELECT DISTINCT month` in a second step and run it. In the run I did that in Python (the generated SQL is printed in the output and matched pandas with Apr included). Inside the database this is dynamic SQL: SQL Server uses `QUOTENAME` plus `sp_executesql`, Oracle and Snowflake have `EXECUTE IMMEDIATE`, PostgreSQL needs `format()` and `EXECUTE` in PL/pgSQL (all not executed here). SQLite has no dynamic SQL inside the engine.
- **Quoting:** values from data become column names; the generator doubles quotes for literals and identifiers (the Code block feeds it a month called `X' OR 1=1 --` and it still produces valid SQL). Never paste raw values into SQL text.
- **Column order:** `DISTINCT` has no order; I sorted months with `INSTR` over a month-name string. In real data use a month number or a date.
- **NULL month or NULL key:** a NULL `month` matches no `CASE` branch and contributes to no cell, but `SUM(amount)` over the group still includes it, so the cells can add up to less than the row total. In `FILTER` or `CASE` pivots, NULL rows vanish silently (the same trap as the Apr row).
- **Duplicates per cell:** sum, count or max has to be chosen; `PIVOT` clauses and pandas `pivot` need an aggregate or unique keys (see Q14 for the `ValueError`).
- **Many columns:** a 50-column pivot is a reporting-layer job; consider returning long format and pivoting in the BI tool.

**Then explain:**
- **One-line answer when the engine is unknown:** "Conditional aggregation: `SUM(CASE WHEN month = 'Jan' THEN amount END) AS jan` for each column, grouped by the row key; use `PIVOT` if the engine has it and the columns are fixed." (Part 1 Q10 has plain conditional aggregation; this question is about engines and dynamics.)
- **CASE versus FILTER:** same result; `FILTER` reads better, `CASE` is portable.
- **`COUNT(CASE WHEN ... THEN 1 END)`** for counts, not `SUM(CASE ... ELSE 0)` unless you want 0 instead of NULL in empty cells.
- **pandas:** `pivot_table` takes the column list from the data, so it is dynamic by nature; that is the practical reason analysts pivot in pandas or in the BI tool.

**Follow-ups:**
- *How do you do it when you cannot know the columns?* Generate the SQL (above), or return long format.
- *Unpivot?* `UNION ALL` of one `SELECT` per column (or `CROSS JOIN (VALUES ...)`), covered in another question of this part; engines with `UNPIVOT` need the column list as well.
- *Is `GROUPING SETS` related?* No; it adds subtotal rows, not columns. SQLite 3.45.1 raised a syntax error on `GROUPING SETS` in the Code block; the engines that have it are not executed here.

**Common mistakes:**
- Putting the `CASE` outside the aggregate (one row per source row instead of one per region).
- `ELSE 0` and then reading 0 as "sold nothing" when it was "no rows".
- Hard-coding the months and silently dropping new ones.
- Pasting data values into generated SQL without quoting.
- Claiming SQLite or MySQL have `PIVOT`: SQLite raised `OperationalError: near "(": syntax error` on it in my run.

### Q17 ⭐⭐ 🟡 String aggregation and group_concat: employees(emp_id, dept, name) and the LeetCode 1484 Group Sold Products By The Date shape activities(sell_date, product) with duplicates. Return per department the comma-separated list of names, per date the count of distinct products and their names sorted and comma-separated. Show GROUP_CONCAT(name, ', '), GROUP_CONCAT(DISTINCT name) (SQLite allows DISTINCT only with the default separator, test it), and the ORDER BY inside the aggregate (SQLite 3.44 and later: group_concat(name ORDER BY name) and string_agg, test both on 3.45.1) versus the older subquery-ORDER-BY trick whose order is not guaranteed. Show how NULL names are skipped and what an all-NULL group returns. State MySQL GROUP_CONCAT ... ORDER BY ... SEPARATOR and its group_concat_max_len limit, PostgreSQL STRING_AGG, SQL Server STRING_AGG with WITHIN GROUP and Oracle LISTAGG (all hedged, not executed). Add the pandas groupby agg(', '.join) and sorted(set(...)) versions.
**Asked at:** LeetCode public problems via the doocs mirror (opened: 1484 Group Sold Products By The Date, 1795 Rearrange Products Table, 1667 Fix Names in a Table, 1527 Patients With a Condition, 1873 Calculate Special Bonus); public problem bank, not a candidate report; analyst and data scientist screens; SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds
**Say this first (1 line):** `GROUP_CONCAT(name, ', ' ORDER BY name)` (or `STRING_AGG(name, ', ' ORDER BY name)`) builds the list in SQLite 3.44 and later; `DISTINCT` works only with the single-argument form, so for a custom separator de-duplicate in a subquery first; NULL names are skipped and an all-NULL group returns NULL.

**Schema and sample data:** seven employees (one department with a duplicate name and a NULL name, one department whose only name is NULL) and the seven activity rows from the LeetCode 1484 example.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept TEXT, name TEXT);
INSERT INTO employees VALUES
 (1,'Eng','Zoya'),(2,'Eng','Asha'),(3,'Eng','Ben'),(4,'Eng','Asha'),(5,'Eng',NULL),
 (6,'Sales','Dev'),(7,'HR',NULL);
CREATE TABLE activities(sell_date TEXT, product TEXT);
INSERT INTO activities VALUES
 ('2020-05-30','Headphone'),('2020-06-01','Pencil'),('2020-06-02','Mask'),('2020-05-30','Basketball'),
 ('2020-06-01','Bible'),('2020-06-02','Mask'),('2020-05-30','T-Shirt');
```
LeetCode 1484 is a public problem statement (opened on the doocs mirror); the rows above are my own copy of its example, not a candidate report.

**SQL answer:** the three main queries, identical to the Code block:
```sql
SQL_DEPT = """
SELECT dept, GROUP_CONCAT(name, ', ' ORDER BY name) AS names
FROM employees GROUP BY dept ORDER BY dept
"""
SQL_DEPT_DISTINCT = """
SELECT dept, GROUP_CONCAT(name, ', ' ORDER BY name) AS names
FROM (SELECT DISTINCT dept, name FROM employees)
GROUP BY dept ORDER BY dept
"""
SQL_DATES = """
SELECT sell_date,
       COUNT(DISTINCT product) AS num_sold,
       GROUP_CONCAT(product, ',' ORDER BY product) AS products
FROM (SELECT DISTINCT sell_date, product FROM activities)
GROUP BY sell_date ORDER BY sell_date
"""
```
- `SQL_DEPT` lists names per department sorted, duplicates kept (Asha appears twice).
- `SQL_DEPT_DISTINCT` removes duplicates in a subquery, because `GROUP_CONCAT(DISTINCT name, ', ')` is rejected (see below).
- `SQL_DATES` gives, per date, the number of distinct products and their sorted list, the shape LeetCode 1484 asks for. The inner `SELECT DISTINCT` already removed the duplicate `Mask`; `COUNT(DISTINCT product)` makes the intent explicit.

`STRING_AGG` is accepted as a synonym on 3.45.1 (run):
```sql
SQL_STRING_AGG = """
SELECT dept, STRING_AGG(name, ', ' ORDER BY name) AS names
FROM employees GROUP BY dept ORDER BY dept
"""
```
and the older trick, whose order is not guaranteed by the SQL standard or SQLite (it matched in my run only because the engine happened to scan the sorted subquery in order):
```sql
SQL_OLD_TRICK = """
SELECT dept, GROUP_CONCAT(name, ', ') AS names
FROM (SELECT dept, name FROM employees ORDER BY name)
GROUP BY dept ORDER BY dept
"""
```

**pandas answer:** identical to the Code block:
```py
emp = pd.read_sql_query("SELECT * FROM employees", con)
acts = pd.read_sql_query("SELECT * FROM activities", con)
p_dept = (emp.groupby("dept")["name"]
             .agg(lambda s: ", ".join(sorted(s.dropna())))
             .rename("names").reset_index())
p_dept["names"] = p_dept["names"].replace("", None)        # SQL gives NULL for an all-NULL group
p_dates = (acts.groupby("sell_date")["product"]
               .agg(num_sold="nunique", products=lambda s: ",".join(sorted(set(s))))
               .reset_index())
```

**Example:** by hand.
- Eng has names Zoya, Asha, Ben, Asha and a NULL: sorted and joined with `', '` that is `Asha, Asha, Ben, Zoya`; the NULL is skipped, so 5 rows but 4 names. Deduplicated: `Asha, Ben, Zoya`.
- Sales has `Dev`. HR has one row whose name is NULL, so the aggregate has nothing to join and returns NULL (not an empty string).
- Dates: on 2020-05-30 the products are Headphone, Basketball, T-Shirt, so 3 distinct, sorted `Basketball,Headphone,T-Shirt`. On 2020-06-01: Bible, Pencil. On 2020-06-02: Mask twice, so 1 distinct, `Mask`.

**Code:** run with `python3 -I`. SQL and pandas are compared ordered by `dept` and `sell_date`.
```python
# Q17: string aggregation with group_concat / string_agg, SQL versus pandas
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept TEXT, name TEXT);
INSERT INTO employees VALUES
 (1,'Eng','Zoya'),(2,'Eng','Asha'),(3,'Eng','Ben'),(4,'Eng','Asha'),(5,'Eng',NULL),
 (6,'Sales','Dev'),(7,'HR',NULL);
CREATE TABLE activities(sell_date TEXT, product TEXT);
INSERT INTO activities VALUES
 ('2020-05-30','Headphone'),('2020-06-01','Pencil'),('2020-06-02','Mask'),('2020-05-30','Basketball'),
 ('2020-06-01','Bible'),('2020-06-02','Mask'),('2020-05-30','T-Shirt');
""")
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)

def run(sql):
    return pd.read_sql_query(sql, con)

# 1. plain group_concat: order inside the group is not guaranteed
print("\n1. GROUP_CONCAT(name, ', ') with no ORDER BY (order is whatever the scan gave):")
print(run("SELECT dept, GROUP_CONCAT(name, ', ') AS names FROM employees GROUP BY dept ORDER BY dept").to_string(index=False))

# 2. DISTINCT: only with the default separator
print("\n2. DISTINCT:")
print("   GROUP_CONCAT(DISTINCT name)       ->", run("SELECT GROUP_CONCAT(DISTINCT name) AS g FROM employees WHERE dept = 'Eng'")["g"][0])
try:
    run("SELECT GROUP_CONCAT(DISTINCT name, ', ') FROM employees")
except Exception as e:
    print("   GROUP_CONCAT(DISTINCT name, ', ') ->", type(e).__name__ + ":", e)

SQL_DEPT = """
SELECT dept, GROUP_CONCAT(name, ', ' ORDER BY name) AS names
FROM employees GROUP BY dept ORDER BY dept
"""
SQL_DEPT_DISTINCT = """
SELECT dept, GROUP_CONCAT(name, ', ' ORDER BY name) AS names
FROM (SELECT DISTINCT dept, name FROM employees)
GROUP BY dept ORDER BY dept
"""
SQL_DATES = """
SELECT sell_date,
       COUNT(DISTINCT product) AS num_sold,
       GROUP_CONCAT(product, ',' ORDER BY product) AS products
FROM (SELECT DISTINCT sell_date, product FROM activities)
GROUP BY sell_date ORDER BY sell_date
"""
SQL_STRING_AGG = """
SELECT dept, STRING_AGG(name, ', ' ORDER BY name) AS names
FROM employees GROUP BY dept ORDER BY dept
"""
SQL_OLD_TRICK = """
SELECT dept, GROUP_CONCAT(name, ', ') AS names
FROM (SELECT dept, name FROM employees ORDER BY name)
GROUP BY dept ORDER BY dept
"""
dept = run(SQL_DEPT)
dept_d = run(SQL_DEPT_DISTINCT)
dates = run(SQL_DATES)
sagg = run(SQL_STRING_AGG)
old = run(SQL_OLD_TRICK)
print("\n3. GROUP_CONCAT(name, ', ' ORDER BY name):"); print(dept.to_string(index=False))
print("   same with DISTINCT applied in a subquery:"); print(dept_d.to_string(index=False))
print("   per date, distinct products sorted (LeetCode 1484 shape):"); print(dates.to_string(index=False))
print("   STRING_AGG(name, ', ' ORDER BY name) equals GROUP_CONCAT version:", sagg.equals(dept))
print("   older subquery ORDER BY trick (no guarantee, but it happened to match here):", old.equals(dept))
one = con.execute("SELECT GROUP_CONCAT(DISTINCT name ORDER BY name) FROM employees WHERE dept='Eng'").fetchone()[0]
print("   GROUP_CONCAT(DISTINCT name ORDER BY name) (default ',') ->", one)

# 4. NULLs
print("\n4. NULL names are skipped; an all-NULL group returns NULL, not ''; Eng has 5 rows, 4 names:")
nul = run("SELECT dept, COUNT(*) AS rows_, COUNT(name) AS names_, GROUP_CONCAT(name, ', ' ORDER BY name) AS g, "
          "COALESCE(GROUP_CONCAT(name, ', ' ORDER BY name), '') AS g_or_empty FROM employees GROUP BY dept ORDER BY dept")
print(nul.to_string(index=False))
print("   NULL separator row-wise: 'a' || NULL ->", con.execute("SELECT 'a' || NULL").fetchone()[0],
      "| concat('a', NULL, 'b') ->", con.execute("SELECT concat('a', NULL, 'b')").fetchone()[0])

emp = pd.read_sql_query("SELECT * FROM employees", con)
acts = pd.read_sql_query("SELECT * FROM activities", con)
p_dept = (emp.groupby("dept")["name"]
             .agg(lambda s: ", ".join(sorted(s.dropna())))
             .rename("names").reset_index())
p_dept["names"] = p_dept["names"].replace("", None)        # SQL gives NULL for an all-NULL group
p_dates = (acts.groupby("sell_date")["product"]
               .agg(num_sold="nunique", products=lambda s: ",".join(sorted(set(s))))
               .reset_index())
print("\npandas groupby + join:"); print(p_dept.to_string(index=False)); print(p_dates.to_string(index=False))
try:
    emp.groupby("dept")["name"].agg(", ".join)
except TypeError as e:
    print("agg(', '.join) on a column with NaN -> TypeError:", e)
p_dist = (emp.groupby("dept")["name"].agg(lambda s: ", ".join(sorted(set(s.dropna())))).rename("names").reset_index())
p_dist["names"] = p_dist["names"].replace("", None)

# comparisons (ordered by dept / sell_date)
pd.testing.assert_frame_equal(p_dept, dept, check_dtype=False)
pd.testing.assert_frame_equal(p_dist, dept_d, check_dtype=False)
pd.testing.assert_frame_equal(p_dates, dates, check_dtype=False)
assert sagg.equals(dept)
print("asserts passed (SQL and pandas equal, ordered by dept / sell_date; the pandas '' became None for the all-NULL group)")
```

**Output (my run):**
```text
SQLite 3.45.1 | pandas 3.0.5

1. GROUP_CONCAT(name, ', ') with no ORDER BY (order is whatever the scan gave):
 dept                 names
  Eng Zoya, Asha, Ben, Asha
   HR                   NaN
Sales                   Dev

2. DISTINCT:
   GROUP_CONCAT(DISTINCT name)       -> Zoya,Asha,Ben
   GROUP_CONCAT(DISTINCT name, ', ') -> DatabaseError: Execution failed on sql 'SELECT GROUP_CONCAT(DISTINCT name, ', ') FROM employees': DISTINCT aggregates must have exactly one argument

3. GROUP_CONCAT(name, ', ' ORDER BY name):
 dept                 names
  Eng Asha, Asha, Ben, Zoya
   HR                   NaN
Sales                   Dev
   same with DISTINCT applied in a subquery:
 dept           names
  Eng Asha, Ben, Zoya
   HR             NaN
Sales             Dev
   per date, distinct products sorted (LeetCode 1484 shape):
 sell_date  num_sold                     products
2020-05-30         3 Basketball,Headphone,T-Shirt
2020-06-01         2                 Bible,Pencil
2020-06-02         1                         Mask
   STRING_AGG(name, ', ' ORDER BY name) equals GROUP_CONCAT version: True
   older subquery ORDER BY trick (no guarantee, but it happened to match here): True
   GROUP_CONCAT(DISTINCT name ORDER BY name) (default ',') -> Asha,Ben,Zoya

4. NULL names are skipped; an all-NULL group returns NULL, not ''; Eng has 5 rows, 4 names:
 dept  rows_  names_                     g            g_or_empty
  Eng      5       4 Asha, Asha, Ben, Zoya Asha, Asha, Ben, Zoya
   HR      1       0                   NaN                      
Sales      1       1                   Dev                   Dev
   NULL separator row-wise: 'a' || NULL -> None | concat('a', NULL, 'b') -> ab

pandas groupby + join:
 dept                 names
  Eng Asha, Asha, Ben, Zoya
   HR                   NaN
Sales                   Dev
 sell_date  num_sold                     products
2020-05-30         3 Basketball,Headphone,T-Shirt
2020-06-01         2                 Bible,Pencil
2020-06-02         1                         Mask
agg(', '.join) on a column with NaN -> TypeError: sequence item 4: expected str instance, float found
asserts passed (SQL and pandas equal, ordered by dept / sell_date; the pandas '' became None for the all-NULL group)
```
Honest notes from the run:
- **`DISTINCT` with a separator is rejected** in SQLite 3.45.1: `GROUP_CONCAT(DISTINCT name, ', ')` fails with `DISTINCT aggregates must have exactly one argument`. `GROUP_CONCAT(DISTINCT name)` works but uses the default `,` separator.
- **ORDER BY inside the aggregate works on 3.45.1** for both `group_concat` and `string_agg` (I did not open the release documentation for 3.44; older SQLite versions would raise a syntax error, which I did not test). `GROUP_CONCAT(DISTINCT name ORDER BY name)` also ran.
- Without `ORDER BY` the Eng list came out in scan order (`Zoya, Asha, Ben, Asha`), which is just how the rows happen to be stored.
- In pandas, `agg(", ".join)` on a column with NaN raised `TypeError: sequence item 4: expected str instance, float found`, so NaN must be dropped first.

**Edge cases:**
- **NULL names:** skipped by `GROUP_CONCAT` (rows 5 versus names 4). If you want them shown, `COALESCE(name, '?')` inside the aggregate.
- **All-NULL group:** NULL. `COALESCE(GROUP_CONCAT(...), '')` converts it; pandas `join` of an empty list gives `''`, which the Code block turns into None to match SQL.
- **Empty strings** are not NULL: they are included and produce stray separators (`a, , b`). Filter with `NULLIF(name, '')` first (Q13 covers normalising blanks).
- **Separator inside the data:** a name containing a comma makes the list ambiguous; pick a separator that cannot occur, or return JSON (`json_group_array`, not tested here).
- **Sort order:** `ORDER BY name` is binary on SQLite (uppercase before lowercase, ASCII); pandas `sorted` is also by code point, so they agree here; a case-insensitive order needs `LOWER(name)` or a collation (SQLite's binary comparison put `'B'` before `'a'` in the Wave A run).
- **Length limits:** MySQL truncates `GROUP_CONCAT` at `group_concat_max_len` (default 1024 bytes in my memory of the documentation; not executed here), SQL Server `STRING_AGG` returns a limited type unless you cast, Oracle `LISTAGG` raises an overflow error on very long lists (not executed). SQLite has a large default limit that I did not test.

**Then explain:**
- **Other engines (not executed):** MySQL `GROUP_CONCAT(name ORDER BY name SEPARATOR ', ')` (the separator is a keyword, not a second argument) and supports `DISTINCT` together with it; PostgreSQL `STRING_AGG(name, ', ' ORDER BY name)` (and `DISTINCT` is allowed if the `ORDER BY` expression matches); SQL Server (2017 and later) `STRING_AGG(name, ', ') WITHIN GROUP (ORDER BY name)`; Oracle `LISTAGG(name, ', ') WITHIN GROUP (ORDER BY name)`; BigQuery has `STRING_AGG(name, ', ' ORDER BY name)`. All written from memory of their documentation, not verified here.
- **Why the order guarantee matters:** a result that depends on the physical scan order can change after an index is added or a plan changes; the subquery trick is a habit from old versions, not a promise.
- **De-duplicating first versus `DISTINCT`:** the subquery works everywhere; the `DISTINCT` inside the aggregate is shorter where allowed.
- **Aggregating in the database versus the app:** fine for reports and the LeetCode shape; if the list feeds another query, store the rows, not a delimited string (Q11 shows how painful splitting is).

**Follow-ups:**
- *Why is the order of group_concat random without ORDER BY?* Because a group is an unordered set; the engine concatenates in the order it encounters rows.
- *How would you get distinct, sorted values with a custom separator?* Subquery with `SELECT DISTINCT`, then `GROUP_CONCAT(x, sep ORDER BY x)`, as `SQL_DEPT_DISTINCT`.
- *How do you do it in pandas for a whole frame at once?* `groupby(...).agg(names=("name", lambda s: ", ".join(sorted(s.dropna()))))`.

**Common mistakes:**
- `GROUP_CONCAT(DISTINCT x, ', ')`: error on SQLite; and in MySQL the separator syntax is different.
- Relying on the order without an `ORDER BY` inside the aggregate.
- Forgetting the all-NULL group returns NULL (and then `'' || NULL` surprises downstream).
- Joining with `', '.join` in pandas on a column with NaN.
- Using the list as a join key later.

### Q18 ⭐⭐ 🟡 Title case and initials: customers(customer_id, full_name) with 'RAHUL sharma', 'asha rao', 'ASHA' and 'anil kumar singh'. First do LeetCode 1667 Fix Names in a Table (capitalise the first letter and lower the rest of a one-word name with UPPER(SUBSTR(name, 1, 1)) || LOWER(SUBSTR(name, 2))), then proper case for several words (SQLite has no INITCAP: say so, and show a recursive CTE word by word or a two-word-only approach), then initials ('R.S.', 'A.R.'). Explain what breaks for names such as 'McDonald', 'de la Cruz' and non-ASCII letters (SQLite UPPER and LOWER are ASCII-only without ICU, tested). Mention INITCAP (PostgreSQL, Oracle, Snowflake) as hedged text. Add the pandas str.title and str.capitalize versions and their apostrophe trap ("o'neil" becomes "O'Neil" or "O'neil": check by running).
**Asked at:** LeetCode public problems via the doocs mirror (opened: 1484 Group Sold Products By The Date, 1795 Rearrange Products Table, 1667 Fix Names in a Table, 1527 Patients With a Condition, 1873 Calculate Special Bonus); public problem bank, not a candidate report; analyst and data scientist screens; SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds
**Say this first (1 line):** For a one-word name it is `UPPER(SUBSTR(name, 1, 1)) || LOWER(SUBSTR(name, 2))` (LeetCode 1667); SQLite has no `INITCAP`, so several words need a word-by-word recursive CTE; and `UPPER`/`LOWER` in SQLite only change ASCII letters, so names like `JOSÉ` or `élodie` come out wrong, while pandas `str.title` handles Unicode but has its own apostrophe trap.

**Schema and sample data:** the four names from the question, plus `mcDONALD`, `de la cRUZ`, two non-ASCII names, an apostrophe name and a NULL.
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, full_name TEXT);
INSERT INTO customers VALUES
 (1,'RAHUL sharma'),(2,'asha rao'),(3,'ASHA'),(4,'anil kumar singh'),
 (5,'mcDONALD'),(6,'de la cRUZ'),
 (7,'élodie dupont'),(8,'JOSÉ ruiz'),(9,'o''neil'),(10,NULL);
```

**SQL answer:** the LeetCode 1667 formula and the word-by-word version, identical to the Code block.
```sql
SQL_ONE_WORD = """
SELECT customer_id, UPPER(SUBSTR(full_name, 1, 1)) || LOWER(SUBSTR(full_name, 2)) AS name
FROM customers ORDER BY customer_id
"""
```
That is right for `ASHA` (row 3) and wrong for any multi-word name, because `LOWER(SUBSTR(name, 2))` lowercases the later words too (`Rahul sharma`).
```sql
SQL_PROPER = """
WITH RECURSIVE w(customer_id, rest, proper, initials) AS (
  SELECT customer_id, LTRIM(TRIM(full_name) || ' '), '', ''
  FROM customers WHERE full_name IS NOT NULL
  UNION ALL
  SELECT customer_id,
         LTRIM(SUBSTR(rest, INSTR(rest, ' ') + 1)),
         proper || CASE WHEN proper = '' THEN '' ELSE ' ' END
                || UPPER(SUBSTR(rest, 1, 1)) || LOWER(SUBSTR(rest, 2, INSTR(rest, ' ') - 2)),
         initials || UPPER(SUBSTR(rest, 1, 1)) || '.'
  FROM w WHERE rest <> ''
)
SELECT c.customer_id, c.full_name, w.proper AS proper_name, w.initials
FROM customers c LEFT JOIN w ON w.customer_id = c.customer_id AND w.rest = ''
ORDER BY c.customer_id
"""
```
How the recursive CTE works (the recursion mechanics themselves are in Part 9 Q1):
- The anchor puts the trimmed name plus one trailing space in `rest`, so every word, including the last, ends with a space. `proper` and `initials` start empty.
- Each step takes the first word (`SUBSTR(rest, 1, INSTR(rest, ' ') - 1)`), capitalises its first letter and lowercases the others, appends it to `proper` (with a space between words), appends `UPPER(first letter) || '.'` to `initials`, and removes the word from `rest`. `LTRIM` also swallows extra spaces between words.
- The recursion stops when `rest` is empty; the final row (`rest = ''`) holds the answer, which the `LEFT JOIN ... w.rest = ''` picks up. A NULL name never enters the CTE, so the `LEFT JOIN` returns NULL for it.
- A two-word-only approach would use `INSTR` once to split at the first space, which is shorter but fails for `anil kumar singh`; the recursive version has no word limit.

**pandas answer:** identical to the Code block:
```py
cust = pd.read_sql_query("SELECT * FROM customers ORDER BY customer_id", con)
p_one = cust["full_name"].str.capitalize()
p_title = cust["full_name"].str.title()
p_init = cust["full_name"].str.split().map(
    lambda ws: "".join(w[0].upper() + "." for w in ws) if isinstance(ws, list) else None)
```

**Example:** by hand.
- `RAHUL sharma`: LeetCode formula gives `Rahul sharma`. Word by word: `RAHUL` becomes `Rahul`, `sharma` becomes `Sharma`, giving `Rahul Sharma` and initials `R.S.`.
- `asha rao`: `Asha Rao`, `A.R.`. `ASHA`: `Asha`, `A.`. `anil kumar singh`: `Anil Kumar Singh`, `A.K.S.`.
- `mcDONALD` becomes `Mcdonald`: a rule that knows about `Mc` prefixes would need a special case. `de la cRUZ` becomes `De La Cruz`; the Spanish or Dutch convention of lowercase particles (`de la Cruz`) cannot be inferred from the string.
- `élodie dupont`: SQLite's `UPPER('é')` is `é` (unchanged), so the first word stays lowercase: `élodie Dupont`, initials `é.D.`. `JOSÉ ruiz`: `LOWER('JOSÉ')` leaves the `É`, so the result is `JosÉ Ruiz`.
- `o'neil`: SQL gives `O'neil` (the letter after the apostrophe is not a word start for SQL, which only splits on spaces).

**Code:** run with `python3 -I`. SQL and pandas are compared ordered by `customer_id` for rows 1 to 6 and the NULL row, and the awkward rows 7 to 9 are asserted to differ in exactly the way shown.
```python
# Q18: title case and initials in SQLite (no INITCAP) versus pandas
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, full_name TEXT);
INSERT INTO customers VALUES
 (1,'RAHUL sharma'),(2,'asha rao'),(3,'ASHA'),(4,'anil kumar singh'),
 (5,'mcDONALD'),(6,'de la cRUZ'),
 (7,'élodie dupont'),(8,'JOSÉ ruiz'),(9,'o''neil'),(10,NULL);
""")
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)
print("UPPER('é') =", con.execute("SELECT UPPER('é')").fetchone()[0], "| LOWER('É') =", con.execute("SELECT LOWER('É')").fetchone()[0],
      "| UPPER('ß') =", con.execute("SELECT UPPER('ß')").fetchone()[0])
try:
    con.execute("SELECT INITCAP('abc')")
except sqlite3.Error as e:
    print("INITCAP ->", e)

SQL_ONE_WORD = """
SELECT customer_id, UPPER(SUBSTR(full_name, 1, 1)) || LOWER(SUBSTR(full_name, 2)) AS name
FROM customers ORDER BY customer_id
"""
SQL_PROPER = """
WITH RECURSIVE w(customer_id, rest, proper, initials) AS (
  SELECT customer_id, LTRIM(TRIM(full_name) || ' '), '', ''
  FROM customers WHERE full_name IS NOT NULL
  UNION ALL
  SELECT customer_id,
         LTRIM(SUBSTR(rest, INSTR(rest, ' ') + 1)),
         proper || CASE WHEN proper = '' THEN '' ELSE ' ' END
                || UPPER(SUBSTR(rest, 1, 1)) || LOWER(SUBSTR(rest, 2, INSTR(rest, ' ') - 2)),
         initials || UPPER(SUBSTR(rest, 1, 1)) || '.'
  FROM w WHERE rest <> ''
)
SELECT c.customer_id, c.full_name, w.proper AS proper_name, w.initials
FROM customers c LEFT JOIN w ON w.customer_id = c.customer_id AND w.rest = ''
ORDER BY c.customer_id
"""
one = pd.read_sql_query(SQL_ONE_WORD, con)
prop = pd.read_sql_query(SQL_PROPER, con)
print("\nLeetCode 1667 formula applied to every row (right only for one-word names):")
print(one.to_string(index=False))
print("\nrecursive CTE: proper case and initials:")
print(prop.to_string(index=False))

cust = pd.read_sql_query("SELECT * FROM customers ORDER BY customer_id", con)
p_one = cust["full_name"].str.capitalize()
p_title = cust["full_name"].str.title()
p_init = cust["full_name"].str.split().map(
    lambda ws: "".join(w[0].upper() + "." for w in ws) if isinstance(ws, list) else None)
out = pd.DataFrame({"full_name": cust["full_name"], "capitalize": p_one, "title": p_title, "initials": p_init})
print("\npandas str.capitalize, str.title and initials:")
print(out.to_string(index=False))
print("pandas dtype:", cust["full_name"].dtype, "| title of \"o'neil\":", pd.Series(["o'neil"]).str.title().tolist(),
      "| capitalize:", pd.Series(["o'neil"]).str.capitalize().tolist(), "| title of '3rd floor':", pd.Series(["3rd floor"]).str.title().tolist())

# comparisons: rows 1-6 are ASCII without apostrophes: SQL and pandas must agree (ordered by customer_id)
ascii_ids = [1, 2, 3, 4, 5, 6]
sql6 = prop[prop["customer_id"].isin(ascii_ids)].reset_index(drop=True)
pd6 = out.iloc[:6].reset_index(drop=True)
assert sql6["proper_name"].tolist() == pd6["title"].tolist()
assert sql6["initials"].tolist() == pd6["initials"].tolist()
assert one.loc[[2], "name"].tolist() == p_one.iloc[[2]].tolist() == ["Asha"]       # the one-word name
assert prop.loc[prop["customer_id"] == 10, "proper_name"].isna().all() and pd.isna(p_title.iloc[9])
# rows 7-9: they differ, and that is the point
diff = {i: (prop.loc[prop["customer_id"] == i, "proper_name"].iloc[0], p_title.iloc[i - 1]) for i in (7, 8, 9)}
print("\nSQL versus pandas title on the awkward rows (SQL, pandas):", diff)
assert diff[7][0] == "élodie Dupont" and diff[7][1] == "Élodie Dupont"
assert diff[8] == ("JosÉ Ruiz", "José Ruiz")
assert diff[9] == ("O'neil", "O'Neil")
print("asserts passed: rows 1-6 and the NULL row match; rows 7-9 differ as shown")

# extra edge rows: empty string, extra spaces, hyphen, apostrophe-s
con.executescript("CREATE TABLE c2(customer_id INTEGER PRIMARY KEY, full_name TEXT); "
                  "INSERT INTO c2 VALUES (1,''),(2,'  anil   kumar '),(3,'anne-marie'),(4,'it''s ok');")
e_sql = pd.read_sql_query(SQL_PROPER.replace("FROM customers c", "FROM c2 c").replace("FROM customers WHERE", "FROM c2 WHERE"), con)
e_pd = pd.read_sql_query("SELECT * FROM c2 ORDER BY customer_id", con)["full_name"]
print("\nextra rows, SQL proper_name:", e_sql["proper_name"].tolist(), "initials:", e_sql["initials"].tolist())
print("extra rows, pandas title   :", e_pd.str.title().tolist())
assert e_sql["proper_name"].tolist() == ["", "Anil Kumar", "Anne-marie", "It's Ok"]
assert e_pd.str.title().tolist() == ["", "  Anil   Kumar ", "Anne-Marie", "It'S Ok"]
print("asserts passed (extra rows)")
```

**Output (my run):**
```text
SQLite 3.45.1 | pandas 3.0.5
UPPER('é') = é | LOWER('É') = É | UPPER('ß') = ß
INITCAP -> no such function: INITCAP

LeetCode 1667 formula applied to every row (right only for one-word names):
 customer_id             name
           1     Rahul sharma
           2         Asha rao
           3             Asha
           4 Anil kumar singh
           5         Mcdonald
           6       De la cruz
           7    élodie dupont
           8        JosÉ ruiz
           9           O'neil
          10              NaN

recursive CTE: proper case and initials:
 customer_id        full_name      proper_name initials
           1     RAHUL sharma     Rahul Sharma     R.S.
           2         asha rao         Asha Rao     A.R.
           3             ASHA             Asha       A.
           4 anil kumar singh Anil Kumar Singh   A.K.S.
           5         mcDONALD         Mcdonald       M.
           6       de la cRUZ       De La Cruz   D.L.C.
           7    élodie dupont    élodie Dupont     é.D.
           8        JOSÉ ruiz        JosÉ Ruiz     J.R.
           9           o'neil           O'neil       O.
          10              NaN              NaN      NaN

pandas str.capitalize, str.title and initials:
       full_name       capitalize            title initials
    RAHUL sharma     Rahul sharma     Rahul Sharma     R.S.
        asha rao         Asha rao         Asha Rao     A.R.
            ASHA             Asha             Asha       A.
anil kumar singh Anil kumar singh Anil Kumar Singh   A.K.S.
        mcDONALD         Mcdonald         Mcdonald       M.
      de la cRUZ       De la cruz       De La Cruz   D.L.C.
   élodie dupont    Élodie dupont    Élodie Dupont     É.D.
       JOSÉ ruiz        José ruiz        José Ruiz     J.R.
          o'neil           O'neil           O'Neil       O.
             NaN              NaN              NaN      NaN
pandas dtype: str | title of "o'neil": ["O'Neil"] | capitalize: ["O'neil"] | title of '3rd floor': ['3Rd Floor']

SQL versus pandas title on the awkward rows (SQL, pandas): {7: ('élodie Dupont', 'Élodie Dupont'), 8: ('JosÉ Ruiz', 'José Ruiz'), 9: ("O'neil", "O'Neil")}
asserts passed: rows 1-6 and the NULL row match; rows 7-9 differ as shown

extra rows, SQL proper_name: ['', 'Anil Kumar', 'Anne-marie', "It's Ok"] initials: ['', 'A.K.', 'A.', 'I.O.']
extra rows, pandas title   : ['', '  Anil   Kumar ', 'Anne-Marie', "It'S Ok"]
asserts passed (extra rows)
```
Honest notes from the run:
- `UPPER('é')` returned `é` and `LOWER('É')` returned `É`: SQLite 3.45.1 here is ASCII-only for case conversion (no ICU, as Wave A recorded). `INITCAP` fails with `no such function`.
- pandas `str.title` turned `o'neil` into `O'Neil` (it capitalises after any non-letter, which is right for O'Neil and wrong for `3rd floor` -> `3Rd Floor` and `it's ok` -> `It'S Ok`; both ran), while `str.capitalize` gave `O'neil`. Neither knows `McDonald`.
- pandas gets `élodie` and `JOSÉ` right because Python's string methods are Unicode-aware.

**Edge cases:**
- **NULL name:** stays NULL in both; `capitalize` and `title` propagate NaN.
- **Empty string:** the CTE returns an empty `proper_name` (the anchor has `rest = ''` and is its own final row); pandas returns `''` (extra rows in the output).
- **Extra spaces:** the CTE collapses them (`'  anil   kumar '` became `Anil Kumar`), `str.title()` keeps them (`'  Anil   Kumar '`); the initials code in pandas uses `split()`, which collapses them.
- **Tabs or NBSP between words:** SQL splits only on the space character (Q2 shows the TRIM side); pandas `split()` without an argument splits on any whitespace.
- **Names with hyphens or apostrophes:** `anne-marie` becomes `Anne-marie` in SQL and `Anne-Marie` in pandas `title`; `it's ok` becomes `It's Ok` in SQL and `It'S Ok` in pandas (extra rows at the end of the output).
- **Particles and prefixes** (`de la`, `van`, `Mc`, `Mac`): there is no correct general rule; store the display name as entered and normalise only for matching.
- **Initials** for a name with a leading space or punctuation, or a first character that is a combining mark: not handled.

**Then explain:**
- **INITCAP:** PostgreSQL, Oracle and Snowflake have `INITCAP`, but their notion of a word boundary (non-alphanumerics, in my memory) differs from engine to engine and I did not run any of them; do not assume equal results across engines.
- **Why SQLite is ASCII-only:** without the ICU extension SQLite's `UPPER`/`LOWER` only map A-Z; a build with ICU, or application code, is needed for the rest. `COLLATE NOCASE` is also ASCII-only (`'é' = 'É' COLLATE NOCASE` was 0 in Wave A).
- **Pick the layer:** if a title-cased display name is needed, doing it in the application (Python, with Unicode support) is more reliable; in SQL do it only for matching or quick clean-up.
- Dedup or match names with `LOWER(TRIM(...))` and accept that non-ASCII letters will not fold (Part 1 Q39 covers case and collation in filters).

**Follow-ups:**
- *How do you do initials in one pass without a recursive CTE?* For a fixed maximum of three words you can use nested `INSTR`/`SUBSTR`; for the general case use the recursive CTE or the application.
- *How would you capitalise only the first word of the sentence?* The one-word formula already does that.
- *Case-insensitive comparison of `JOSÉ` and `José`?* SQLite `LOWER` will not fold the accent letter; Python `casefold()` and `str.casefold()` in pandas will.

**Common mistakes:**
- Using the one-word formula on full names and calling it title case.
- Expecting `LOWER`/`UPPER` to handle accented letters in SQLite.
- Assuming `INITCAP` exists everywhere.
- Using `str.title()` blindly: `o'neil` and `3rd` come out unexpectedly.
- Forgetting that a trailing or double space creates an empty word and a stray `.` in the initials.

### Q19 ⭐⭐ 🟡 Count occurrences of a substring and words: logs(raw_line) such as 'error error warn', 'ok', NULL and 'Error,error'. Use LENGTH(s) - LENGTH(REPLACE(s, 'error', '')) divided by LENGTH('error') to count occurrences, explain the case-sensitivity fix (LOWER on both sides), the overlapping-match trap ('aaa' contains 'aa' once or twice?), the NULL result, and the word-count formula using spaces (LENGTH(TRIM(s)) - LENGTH(REPLACE(TRIM(s), ' ', '')) + 1) and the double-space and empty-string failures. Count the number of vowels in a name the same way. Add the pandas str.count (regex) versus str.count on a literal, and show which one treats overlapping the same as SQL.
**Asked at:** SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Count occurrences as `(LENGTH(s) - LENGTH(REPLACE(s, pat, ''))) / LENGTH(pat)`; it is case-sensitive (lower both sides), counts non-overlapping matches left to right (`'aaa'` contains `'aa'` once), returns NULL for a NULL line, and the space-based word count breaks on empty strings and double spaces.

**Schema and sample data:** seven log lines (a repeat, a clean line, NULL, mixed case with a comma, an empty string, double spaces, leading and trailing spaces) and five names for the vowel count.
```sql
CREATE TABLE logs(id INTEGER PRIMARY KEY, raw_line TEXT);
INSERT INTO logs VALUES
 (1,'error error warn'),(2,'ok'),(3,NULL),(4,'Error,error'),(5,''),(6,'a  b   c'),(7,'  disk  full  ');
CREATE TABLE names(id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO names VALUES (1,'Anil'),(2,'RAHUL'),(3,'Rhythm'),(4,'Aeiou'),(5,NULL);
```

**SQL answer:** identical to the Code block.
```sql
SQL_COUNTS = """
SELECT id,
       (LENGTH(raw_line) - LENGTH(REPLACE(raw_line, 'error', ''))) / LENGTH('error')                 AS err_case_sensitive,
       (LENGTH(raw_line) - LENGTH(REPLACE(LOWER(raw_line), LOWER('error'), ''))) / LENGTH('error')   AS err_any_case,
       LENGTH(TRIM(raw_line)) - LENGTH(REPLACE(TRIM(raw_line), ' ', '')) + 1                         AS words_naive,
       CASE WHEN TRIM(raw_line) = '' THEN 0
            ELSE LENGTH(TRIM(REPLACE(REPLACE(REPLACE(raw_line, '  ', ' '), '  ', ' '), '  ', ' ')))
               - LENGTH(REPLACE(TRIM(REPLACE(REPLACE(REPLACE(raw_line, '  ', ' '), '  ', ' '), '  ', ' ')), ' ', '')) + 1
       END                                                                                           AS words_fixed
FROM logs ORDER BY id
"""
```
- **Occurrences:** removing every match shortens the string by `LENGTH(pat)` per match, so the length difference divided by `LENGTH(pat)` is the count. Integer division in SQLite is exact here because the difference is always a multiple of the pattern length.
- **Case:** `REPLACE` is case-sensitive, so `'Error'` is not removed; `LOWER(raw_line)` and `LOWER('error')` fix it (ASCII only, Q18 and Q2 have the details).
- **Words:** the naive formula counts spaces and adds 1. `words_fixed` collapses runs of spaces with three `REPLACE` passes (each pass halves a run; Q2 explains why one pass is not enough), trims, and returns 0 for blank lines.

Vowels:
```sql
SQL_VOWELS = """
SELECT id, name,
       LENGTH(name) - LENGTH(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(LOWER(name), 'a', ''), 'e', ''), 'i', ''), 'o', ''), 'u', '')) AS vowels
FROM names ORDER BY id
"""
```

**pandas answer:** identical to the Code block:
```py
logs = pd.read_sql_query("SELECT * FROM logs ORDER BY id", con)
names = pd.read_sql_query("SELECT * FROM names ORDER BY id", con)
line = logs["raw_line"]
p = pd.DataFrame({
    "id": logs["id"],
    "err_case_sensitive": line.str.count("error"),
    "err_any_case": line.str.count("error", flags=re.IGNORECASE),
    "words": line.str.split().str.len(),
})
p_vowels = names["name"].str.count("[aeiouAEIOU]")
```

**Example:** by hand.
- Line 1, `error error warn` (16 characters). Removing both `error` leaves ` ` + ` warn` = `  warn`, 6 characters. (16 - 6) / 5 = 2. Words: 2 spaces + 1 = 3.
- Line 4, `Error,error`: case-sensitive removal only finds the lowercase one: (11 - 6) / 5 = 1. With `LOWER` on both sides: (11 - 1) / 5 = 2. Words by spaces: 0 spaces + 1 = 1, even though a comma separates two tokens.
- Line 5, the empty string: the naive word count gives 0 - 0 + 1 = 1 (wrong, it has no words); the fixed one returns 0.
- Line 6, `a  b   c` (8 characters, 5 of them spaces): naive 8 - 3 + 1 = 6, but there are 3 words. Line 7, `  disk  full  `: trimming helps the ends but the inner double space makes the naive count 3 instead of 2.
- Line 3 is NULL: `LENGTH(NULL)` is NULL, so every count is NULL.
- Vowels: `Anil` has A and i = 2; `RAHUL` lowercased is `rahul` with a and u = 2; `Rhythm` has none (y is not counted) = 0; `Aeiou` = 5; NULL gives NULL.
- Overlap: `REPLACE('aaa', 'aa', '')` scans left to right, removes the first `aa` and is left with `a`, so (3 - 1) / 2 = 1.

**Code:** run with `python3 -I`. SQL and pandas are compared ordered by `id` (SQL NULL equals pandas NaN).
```python
# Q19: counting substrings, words and vowels with LENGTH/REPLACE, versus pandas str.count
import re
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE logs(id INTEGER PRIMARY KEY, raw_line TEXT);
INSERT INTO logs VALUES
 (1,'error error warn'),(2,'ok'),(3,NULL),(4,'Error,error'),(5,''),(6,'a  b   c'),(7,'  disk  full  ');
CREATE TABLE names(id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO names VALUES (1,'Anil'),(2,'RAHUL'),(3,'Rhythm'),(4,'Aeiou'),(5,NULL);
""")
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)

SQL_COUNTS = """
SELECT id,
       (LENGTH(raw_line) - LENGTH(REPLACE(raw_line, 'error', ''))) / LENGTH('error')                 AS err_case_sensitive,
       (LENGTH(raw_line) - LENGTH(REPLACE(LOWER(raw_line), LOWER('error'), ''))) / LENGTH('error')   AS err_any_case,
       LENGTH(TRIM(raw_line)) - LENGTH(REPLACE(TRIM(raw_line), ' ', '')) + 1                         AS words_naive,
       CASE WHEN TRIM(raw_line) = '' THEN 0
            ELSE LENGTH(TRIM(REPLACE(REPLACE(REPLACE(raw_line, '  ', ' '), '  ', ' '), '  ', ' ')))
               - LENGTH(REPLACE(TRIM(REPLACE(REPLACE(REPLACE(raw_line, '  ', ' '), '  ', ' '), '  ', ' ')), ' ', '')) + 1
       END                                                                                           AS words_fixed
FROM logs ORDER BY id
"""
SQL_VOWELS = """
SELECT id, name,
       LENGTH(name) - LENGTH(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(LOWER(name), 'a', ''), 'e', ''), 'i', ''), 'o', ''), 'u', '')) AS vowels
FROM names ORDER BY id
"""
sql = pd.read_sql_query(SQL_COUNTS, con)
vow = pd.read_sql_query(SQL_VOWELS, con)
print("\nSQL counts (NULL line gives NULL; the empty line gives words_naive = 1):")
print(sql.to_string(index=False))
print("\nSQL vowels:"); print(vow.to_string(index=False))

logs = pd.read_sql_query("SELECT * FROM logs ORDER BY id", con)
names = pd.read_sql_query("SELECT * FROM names ORDER BY id", con)
line = logs["raw_line"]
p = pd.DataFrame({
    "id": logs["id"],
    "err_case_sensitive": line.str.count("error"),
    "err_any_case": line.str.count("error", flags=re.IGNORECASE),
    "words": line.str.split().str.len(),
})
p_vowels = names["name"].str.count("[aeiouAEIOU]")
print("\npandas str.count / split:"); print(p.to_string(index=False))

# comparisons (ordered by id; SQL NULL equals pandas NaN)
pd.testing.assert_series_equal(p["err_case_sensitive"], sql["err_case_sensitive"].astype(float), check_names=False)
pd.testing.assert_series_equal(p["err_any_case"], sql["err_any_case"].astype(float), check_names=False)
pd.testing.assert_series_equal(p["words"], sql["words_fixed"].astype(float), check_names=False)
pd.testing.assert_series_equal(p_vowels, vow["vowels"].astype(float), check_names=False)
assert sql["words_naive"].tolist()[:2] == [3, 1] and sql.loc[4, "words_naive"] == 1 and sql.loc[5, "words_naive"] == 6 and sql.loc[6, "words_naive"] == 3
print("asserts passed (SQL and pandas equal, ordered by id; the naive word count is not asserted equal because it is wrong)")

# overlap
print("\noverlap: does 'aaa' contain 'aa' once or twice?")
sql_overlap = con.execute("SELECT (LENGTH('aaa') - LENGTH(REPLACE('aaa', 'aa', ''))) / LENGTH('aa'), REPLACE('aaa', 'aa', '')").fetchone()
a = pd.Series(["aaa"])
print("  SQL LENGTH/REPLACE:", sql_overlap[0], "(REPLACE leaves", repr(sql_overlap[1]) + ")")
print("  pandas str.count('aa')            :", a.str.count("aa")[0])
print("  pandas str.count('(?=aa)') lookahead:", a.str.count("(?=aa)")[0])
print("  Python 'aaa'.count('aa')          :", "aaa".count("aa"))
assert sql_overlap[0] == a.str.count("aa")[0] == "aaa".count("aa") == 1 and a.str.count("(?=aa)")[0] == 2

# regex versus literal
b = pd.Series(["a.b.c"])
print("\nstr.count is always a regex: '.' ->", b.str.count(".")[0], "| r'\\.' ->", b.str.count(r"\.")[0],
      "| re.escape('.') ->", b.str.count(re.escape("."))[0], "| SQL on 'a.b.c':",
      con.execute("SELECT LENGTH('a.b.c') - LENGTH(REPLACE('a.b.c', '.', ''))").fetchone()[0])
# the empty pattern: REPLACE(s, '', '') returns s unchanged, and dividing by LENGTH('') = 0 gives NULL in SQLite
print("\nempty pattern: REPLACE('abc', '', '') ->", repr(con.execute("SELECT REPLACE('abc', '', '')").fetchone()[0]),
      "| 3 / LENGTH('') ->", con.execute("SELECT 3 / LENGTH('')").fetchone()[0], "(division by zero is NULL in SQLite)")
# a substring is not a word
print("substring is not a word: 'terrors' counts", con.execute("SELECT (LENGTH('terrors') - LENGTH(REPLACE('terrors', 'error', ''))) / 5").fetchone()[0], "occurrence of 'error'")

# LIKE case-insensitivity and PRAGMA case_sensitive_like
print("\n'Error' LIKE '%error%':", con.execute("SELECT 'Error' LIKE '%error%'").fetchone()[0], "| REPLACE is case-sensitive:",
      con.execute("SELECT REPLACE('Error', 'error', '')").fetchone()[0])
con.execute("PRAGMA case_sensitive_like = 1")
print("after PRAGMA case_sensitive_like = 1: 'Error' LIKE '%error%' ->", con.execute("SELECT 'Error' LIKE '%error%'").fetchone()[0])
con.execute("PRAGMA case_sensitive_like = 0")
```

**Output (my run):**
```text
SQLite 3.45.1 | pandas 3.0.5

SQL counts (NULL line gives NULL; the empty line gives words_naive = 1):
 id  err_case_sensitive  err_any_case  words_naive  words_fixed
  1                 2.0           2.0          3.0          3.0
  2                 0.0           0.0          1.0          1.0
  3                 NaN           NaN          NaN          NaN
  4                 1.0           2.0          1.0          1.0
  5                 0.0           0.0          1.0          0.0
  6                 0.0           0.0          6.0          3.0
  7                 0.0           0.0          3.0          2.0

SQL vowels:
 id   name  vowels
  1   Anil     2.0
  2  RAHUL     2.0
  3 Rhythm     0.0
  4  Aeiou     5.0
  5    NaN     NaN

pandas str.count / split:
 id  err_case_sensitive  err_any_case  words
  1                 2.0           2.0    3.0
  2                 0.0           0.0    1.0
  3                 NaN           NaN    NaN
  4                 1.0           2.0    1.0
  5                 0.0           0.0    0.0
  6                 0.0           0.0    3.0
  7                 0.0           0.0    2.0
asserts passed (SQL and pandas equal, ordered by id; the naive word count is not asserted equal because it is wrong)

overlap: does 'aaa' contain 'aa' once or twice?
  SQL LENGTH/REPLACE: 1 (REPLACE leaves 'a')
  pandas str.count('aa')            : 1
  pandas str.count('(?=aa)') lookahead: 2
  Python 'aaa'.count('aa')          : 1

str.count is always a regex: '.' -> 5 | r'\.' -> 2 | re.escape('.') -> 2 | SQL on 'a.b.c': 2

empty pattern: REPLACE('abc', '', '') -> 'abc' | 3 / LENGTH('') -> None (division by zero is NULL in SQLite)
substring is not a word: 'terrors' counts 1 occurrence of 'error'

'Error' LIKE '%error%': 1 | REPLACE is case-sensitive: Error
after PRAGMA case_sensitive_like = 1: 'Error' LIKE '%error%' -> 0
```
Honest notes from the run:
- pandas `str.count` has no `regex=False` option (signature `count(pat, flags=0)`): the pattern is always a regex, so `'.'` counted every character (5 in `a.b.c`) while `r'\.'` or `re.escape('.')` counted the two dots, as SQL does.
- Overlap: pandas `str.count('aa')` on `'aaa'` is 1, Python `'aaa'.count('aa')` is 1 and SQL `LENGTH`/`REPLACE` is 1, so all three count non-overlapping matches. Only the regex lookahead `(?=aa)` counts 2 (overlapping).
- `PRAGMA case_sensitive_like = 1` changed `'Error' LIKE '%error%'` from 1 to 0 on this SQLite. I did not open the documentation for that pragma, so I do not claim anything about its status or scope beyond this run; `REPLACE` and `=` are case-sensitive regardless.
- pandas returns floats (NaN for the NULL line), the SQL integers arrive as floats in the DataFrame for the same reason.

**Edge cases:**
- **NULL line:** NULL in SQL, NaN in pandas (`str.count` and `str.split().str.len()` keep missing).
- **Empty pattern:** `REPLACE(s, '', '')` returns `s` unchanged, and `LENGTH('')` is 0, so the division is by zero, which SQLite turns into NULL (printed in the output). Guard it with `NULLIF(LENGTH(pat), 0)`; some other engines raise an error instead (not executed here).
- **Overlap:** if you do need overlapping counts (`'aaa'` has two overlapping `aa`), loop over start positions with a recursive CTE or use a regex lookahead in pandas; `REPLACE` cannot do it.
- **Substring is not a word:** the formula counts `error` inside `terrors` (output shows 1); for whole words pad with delimiters first and count `' error '` in `' ' || s || ' '`, which also needs a rule for punctuation.
- **Counting `'a'` in a field that contains the pattern with different case, accents:** SQLite `LOWER` is ASCII-only, so `É` and `é` differ.
- **Words:** tabs and newlines are not spaces for `REPLACE(..., ' ', '')`; pandas `split()` with no argument splits on any whitespace. Commas and hyphens create tokens the space formula cannot see.
- **Long lines:** the formula is O(length) per row, fine; for large text columns use full-text search (FTS5 is compiled into this SQLite, per Wave A) rather than counting.

**Then explain:**
- **Why it works:** `REPLACE` deletes matches, `LENGTH` measures the shrink; it is arithmetic on lengths, not a search.
- **Why case matters:** `REPLACE`, `=`, `INSTR` and `GLOB` are case-sensitive in SQLite; `LIKE` is case-insensitive for ASCII (run above).
- **Characters versus bytes:** `LENGTH` counts characters; with multi-byte characters it is still fine, because both lengths use the same unit.
- **Other engines (not executed):** PostgreSQL, MySQL 8, Oracle, BigQuery and Snowflake have regex functions that count matches directly (for example `REGEXP_COUNT` in Oracle and Snowflake, in my memory) and `CHAR_LENGTH`/`LEN` variants; names and NULL/empty-pattern behaviour differ, so check the manual. SQLite has no `REGEXP` function unless the application registers one (`no such function: regexp` when I ran the `x REGEXP y` operator form in this session; the sources note correction reports the text in uppercase, so the exact case may depend on how it is called).
- **pandas:** `str.count` is regex-based and non-overlapping; use `str.split().str.len()` for words; both propagate missing values.

**Follow-ups:**
- *Count a word case-insensitively but only as a whole word?* Normalise punctuation to spaces with nested `REPLACE`, lowercase, pad with spaces, then count `' error '` with the formula (note that overlapping `' error error '` shares the middle space; so pad each occurrence or count twice with a replacement of two spaces).
- *Count characters instead of a substring?* Same formula with a one-character pattern; the vowel count is that repeated for five letters.
- *Find the position of the second occurrence?* Nested `INSTR` on the substring after the first match, or a recursive CTE.

**Common mistakes:**
- Forgetting to divide by `LENGTH(pat)` (the difference counts characters, not matches).
- Case-sensitive counting of `Error`.
- `LENGTH(s) - LENGTH(REPLACE(s, ' ', '')) + 1` on empty strings, trailing spaces and double spaces.
- Calling `str.count('.')` in pandas and getting the length of the string.
- Assuming `REPLACE` counts overlaps.

### Q20 ⭐⭐ 🟡 Phone numbers without regular expressions: contacts(name, phone) with values '+91 98765-43210', '(022) 2345 6789', '098765 43210', '9876543210', '98765 43210 ext 12' and NULL. SQLite has no REGEXP_REPLACE: strip spaces, dashes and brackets with nested REPLACE, keep the last 10 digits with SUBSTR(x, -10), flag numbers that are not 10 digits after cleaning (including those with letters, via GLOB '*[^0-9]*'), and return a standard form such as +91-XXXXX-XXXXX with PRINTF or concatenation. Explain which cases you refuse to guess (extensions, landlines with STD codes). State REGEXP_REPLACE availability in PostgreSQL, MySQL 8, Oracle, BigQuery and Snowflake as hedged text. Add the pandas str.replace(r'\D', '', regex=True) and str[-10:] version.
**Asked at:** SQL string-function and NULL-handling practice pages (datadriven.io, prachub, dataford, Interview Query, DesignGurus, search snippets; the prachub topic page opened and lists question titles with company labels but does not say whether they are candidate reports); guides, not candidate reports; analyst and data science rounds; Expert extension from the scope list: no source found that reports this exact question; documentation and general practice only; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Strip the separators with nested `REPLACE`, flag anything that still has a non-digit using `GLOB '*[^0-9]*'`, accept only the shapes you can name (10 digits, 0 plus 10, 91 plus 10, mobile starting 6 to 9), take `SUBSTR(x, -10)` only for those, and send extensions and landlines with STD codes to review instead of guessing.

**Schema and sample data:** the five formats from the question, a NULL, and a 9-digit number.
```sql
CREATE TABLE contacts(id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
INSERT INTO contacts VALUES
 (1,'Asha','+91 98765-43210'),
 (2,'Ben','(022) 2345 6789'),
 (3,'Chitra','098765 43210'),
 (4,'Dev','9876543210'),
 (5,'Esha','98765 43210 ext 12'),
 (6,'Farid',NULL),
 (7,'Gita','98765-4321');
```

**SQL answer:** identical to the Code block.
```sql
SQL_PHONE = """
WITH c AS (
  SELECT id, name, phone,
         REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(phone, ' ', ''), '-', ''), '(', ''), ')', ''), '+', '') AS d
  FROM contacts
), s AS (
  SELECT *,
         CASE WHEN phone IS NULL THEN 'missing'
              WHEN d GLOB '*[^0-9]*' THEN 'review: non-digit (extension or text)'
              WHEN (LENGTH(d) = 10 AND d GLOB '[6-9]*')
                OR (LENGTH(d) = 11 AND d GLOB '0[6-9]*')
                OR (LENGTH(d) = 12 AND d GLOB '91[6-9]*') THEN 'ok'
              WHEN LENGTH(d) = 11 AND d GLOB '0*' THEN 'review: landline with STD code'
              ELSE 'review: length ' || LENGTH(d)
         END AS status
  FROM c
)
SELECT id, name, phone, d AS cleaned, status,
       CASE WHEN status = 'ok'
            THEN PRINTF('+91-%s-%s', SUBSTR(d, -10, 5), SUBSTR(d, -5))
       END AS standard
FROM s ORDER BY id
"""
```
- `c` removes space, dash, both brackets and plus with five nested `REPLACE` calls; `d` is the "cleaned" string. `NULL` stays `NULL` all the way.
- `d GLOB '*[^0-9]*'` is true when any character is not a digit (`GLOB` is case-sensitive, supports `[^...]` and is available without extensions; this is not a regex). It catches the `ext` row.
- The accepted shapes are 10 digits starting 6-9, `0` plus such a number (11 digits) and `91` plus such a number (12 digits). The assumption that Indian mobile numbers start with 6, 7, 8 or 9 is mine; check it against your telecom rules before relying on it.
- `SUBSTR(d, -10, 5)` and `SUBSTR(d, -5)` take the first and second half of the last 10 digits; `PRINTF('+91-%s-%s', ...)` (or `'+91-' || ... || '-' || ...`) builds the standard form. Only `ok` rows get a standard form.

**pandas answer:** identical to the Code block (the cleaning mirrors the SQL, so the letters are still there to be detected):
```py
contacts = pd.read_sql_query("SELECT * FROM contacts ORDER BY id", con)
d = contacts["phone"].str.replace(r"[ \-()+]", "", regex=True)           # same cleaning as the nested REPLACE
has_other = d.str.contains(r"[^0-9]", regex=True)                          # letters etc. (check BEFORE removing them)
n = d.str.len()
ok = ((n == 10) & d.str.match(r"[6-9]")) | ((n == 11) & d.str.match(r"0[6-9]")) | ((n == 12) & d.str.match(r"91[6-9]"))
status = np.select(
    [contacts["phone"].isna(), has_other.fillna(False), ok.fillna(False), (n == 11) & d.str.match(r"0"),],
    ["missing", "review: non-digit (extension or text)", "ok", "review: landline with STD code"],
    default="review: length " + n.astype("Int64").astype(str))
last10 = d.str[-10:]
standard = np.where(status == "ok", "+91-" + last10.str[:5] + "-" + last10.str[5:], None)
p = pd.DataFrame({"id": contacts["id"], "cleaned": d, "status": status, "standard": standard})
```

**Example:** by hand.
- Row 1 `+91 98765-43210` becomes `919876543210` (12 digits starting `91` then `9`): ok, last 10 = `9876543210`, standard `+91-98765-43210`.
- Row 2 `(022) 2345 6789` becomes `02223456789` (11 digits, starts `0` then `2`, not 6-9): that is a landline with the STD code 022, so it is not guessed.
- Row 3 `098765 43210` becomes `09876543210`: 11 digits, `0` then `9`: a mobile with the trunk 0, ok.
- Row 4 is already 10 digits: ok. Row 5 becomes `9876543210ext12`: letters remain, so it is flagged; the extension is not guessed.
- Row 6 NULL: `missing`. Row 7 `98765-4321` has 9 digits: `review: length 9`.

**Code:** run with `python3 -I`. SQL and pandas are compared on `status`, `cleaned` and `standard`, ordered by `id`.
```python
# Q20: phone numbers without regular expressions (SQLite) versus pandas str.replace(r'\D')
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE contacts(id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
INSERT INTO contacts VALUES
 (1,'Asha','+91 98765-43210'),
 (2,'Ben','(022) 2345 6789'),
 (3,'Chitra','098765 43210'),
 (4,'Dev','9876543210'),
 (5,'Esha','98765 43210 ext 12'),
 (6,'Farid',NULL),
 (7,'Gita','98765-4321');
""")
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)

SQL_PHONE = """
WITH c AS (
  SELECT id, name, phone,
         REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(phone, ' ', ''), '-', ''), '(', ''), ')', ''), '+', '') AS d
  FROM contacts
), s AS (
  SELECT *,
         CASE WHEN phone IS NULL THEN 'missing'
              WHEN d GLOB '*[^0-9]*' THEN 'review: non-digit (extension or text)'
              WHEN (LENGTH(d) = 10 AND d GLOB '[6-9]*')
                OR (LENGTH(d) = 11 AND d GLOB '0[6-9]*')
                OR (LENGTH(d) = 12 AND d GLOB '91[6-9]*') THEN 'ok'
              WHEN LENGTH(d) = 11 AND d GLOB '0*' THEN 'review: landline with STD code'
              ELSE 'review: length ' || LENGTH(d)
         END AS status
  FROM c
)
SELECT id, name, phone, d AS cleaned, status,
       CASE WHEN status = 'ok'
            THEN PRINTF('+91-%s-%s', SUBSTR(d, -10, 5), SUBSTR(d, -5))
       END AS standard
FROM s ORDER BY id
"""
sql = pd.read_sql_query(SQL_PHONE, con)
print("\nSQL:"); print(sql.to_string(index=False))

contacts = pd.read_sql_query("SELECT * FROM contacts ORDER BY id", con)
d = contacts["phone"].str.replace(r"[ \-()+]", "", regex=True)           # same cleaning as the nested REPLACE
has_other = d.str.contains(r"[^0-9]", regex=True)                          # letters etc. (check BEFORE removing them)
n = d.str.len()
ok = ((n == 10) & d.str.match(r"[6-9]")) | ((n == 11) & d.str.match(r"0[6-9]")) | ((n == 12) & d.str.match(r"91[6-9]"))
status = np.select(
    [contacts["phone"].isna(), has_other.fillna(False), ok.fillna(False), (n == 11) & d.str.match(r"0"),],
    ["missing", "review: non-digit (extension or text)", "ok", "review: landline with STD code"],
    default="review: length " + n.astype("Int64").astype(str))
last10 = d.str[-10:]
standard = np.where(status == "ok", "+91-" + last10.str[:5] + "-" + last10.str[5:], None)
p = pd.DataFrame({"id": contacts["id"], "cleaned": d, "status": status, "standard": standard})
print("\npandas:"); print(p.to_string(index=False))

# comparison: ordered by id; NULL equals NaN/None
s_cmp = sql[["id", "cleaned", "status", "standard"]].copy()
for col in ("cleaned", "standard"):
    s_cmp[col] = s_cmp[col].astype(object).where(s_cmp[col].notna(), None)
    p[col] = p[col].astype(object).where(p[col].notna(), None)
assert s_cmp["status"].tolist() == p["status"].tolist()
assert s_cmp["standard"].tolist() == p["standard"].tolist()
assert s_cmp["cleaned"].tolist() == p["cleaned"].tolist()
print("\nasserts passed (status, cleaned digits and standard form equal, ordered by id)")

# the trap: strip everything that is not a digit first, then take the last 10
naive = contacts["phone"].str.replace(r"\D", "", regex=True).str[-10:]
print("\nnaive pandas str.replace(r'\\D', '').str[-10:]:")
print(pd.DataFrame({"phone": contacts["phone"], "naive_last10": naive}).to_string(index=False))
assert naive[4] == "7654321012" and naive[1] == "2223456789" and naive[2] == "9876543210"
print("row 5 (extension) and row 2 (landline) silently become 10-digit 'numbers'; the status check above refuses them")
print("SQLite SUBSTR(x, -10) on a 5-char string:", con.execute("SELECT SUBSTR('12345', -10)").fetchone()[0], "(returns what exists, no error)")
```

**Output (my run):**
```text
SQLite 3.45.1 | pandas 3.0.5

SQL:
 id   name              phone         cleaned                                status        standard
  1   Asha    +91 98765-43210    919876543210                                    ok +91-98765-43210
  2    Ben    (022) 2345 6789     02223456789        review: landline with STD code             NaN
  3 Chitra       098765 43210     09876543210                                    ok +91-98765-43210
  4    Dev         9876543210      9876543210                                    ok +91-98765-43210
  5   Esha 98765 43210 ext 12 9876543210ext12 review: non-digit (extension or text)             NaN
  6  Farid                NaN             NaN                               missing             NaN
  7   Gita         98765-4321       987654321                      review: length 9             NaN

pandas:
 id         cleaned                                status        standard
  1    919876543210                                    ok +91-98765-43210
  2     02223456789        review: landline with STD code             NaN
  3     09876543210                                    ok +91-98765-43210
  4      9876543210                                    ok +91-98765-43210
  5 9876543210ext12 review: non-digit (extension or text)             NaN
  6             NaN                               missing             NaN
  7       987654321                      review: length 9             NaN

asserts passed (status, cleaned digits and standard form equal, ordered by id)

naive pandas str.replace(r'\D', '').str[-10:]:
             phone naive_last10
   +91 98765-43210   9876543210
   (022) 2345 6789   2223456789
      098765 43210   9876543210
        9876543210   9876543210
98765 43210 ext 12   7654321012
               NaN          NaN
        98765-4321    987654321
row 5 (extension) and row 2 (landline) silently become 10-digit 'numbers'; the status check above refuses them
SQLite SUBSTR(x, -10) on a 5-char string: 12345 (returns what exists, no error)
```
Honest notes from the run:
- The tempting pandas version `str.replace(r"\D", "", regex=True).str[-10:]` produced `7654321012` for the extension row (`987654321012`, last 10 digits) and `2223456789` for the landline, both plausible-looking and both wrong; only the pre-clean check for letters and the shape rules catch them. In SQL the `GLOB` check does the same job.
- `SUBSTR('12345', -10)` returned `12345`: it does not fail on short strings, so the length test has to come first.
- The pandas `str.replace` default is `regex=False`, so the code passes `regex=True` explicitly; `r"[ \-()+]"` is the same character set as the nested `REPLACE`.

**Edge cases:**
- **NULL:** stays NULL through `REPLACE`; the `CASE` tests it first because `NULL GLOB ...` is NULL and would otherwise fall into the length branch.
- **Extensions** (`ext 12`, `x12`): refuse, or split at the letter before cleaning if the business wants the extension kept separately.
- **Landlines and STD codes:** length and the first digit differ by city (2-digit codes with 8-digit numbers, longer codes with shorter numbers); without a code table, flag them.
- **Other country codes** (`+44 ...`): the 12-digit rule would not match; they fall to the length branch for review. Do not assume +91.
- **Digits in other scripts:** `GLOB '[0-9]'` matches ASCII digits only; Devanagari digits would be flagged as non-digit.
- **Tabs and NBSP:** not removed by my `REPLACE` list; they would be flagged as non-digit (good) but then need manual cleanup (Q2 covers TRIM limits).
- **Duplicate numbers in different formats:** compare `standard`, not the raw text.

**Then explain:**
- **No REGEXP_REPLACE:** SQLite does not have it by default (Wave A run), so use `REPLACE` for each character, `GLOB` for classes, `SUBSTR` with a negative start for "last N". Nested `REPLACE` grows with each character; in a view or CTE it stays readable.
- **Other engines (not executed here):** `REGEXP_REPLACE` exists in PostgreSQL, MySQL 8, Oracle, BigQuery and Snowflake (in my memory of their documentation; signatures and the flags argument differ, and I did not run them), which would reduce the cleaning to `REGEXP_REPLACE(phone, '[^0-9]', '')`.
- **Policy beats cleverness:** accept only the shapes you can name, keep the raw column and add a status column, so the review queue is a `WHERE status <> 'ok'` away.
- **pandas:** `str.replace(r'\D', '', regex=True)` and `str[-10:]` are fine only after letters and lengths are checked.

**Follow-ups:**
- *How do you check the first digit is 6-9 with GLOB?* `d GLOB '[6-9]*'` for 10-digit strings (or on `SUBSTR(d, -10)`).
- *Could a CHECK constraint enforce this?* A `CHECK (phone GLOB '[6-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')` on the cleaned column works in SQLite; a NULL passes a CHECK, so add `NOT NULL` if needed.
- *What if there are millions of rows?* The cleaning is a scan with cheap string functions; store the cleaned value in a column once rather than recomputing it in every query.

**Common mistakes:**
- `SUBSTR(x, -10)` on the raw string (the last 10 characters include dashes and spaces).
- Stripping non-digits first and then taking the last 10 digits, which turns extensions and landlines into fake mobile numbers.
- Assuming every 11-digit number starting with 0 is a mobile.
- Forgetting NULL in the `CASE`.
- Treating `GLOB` like `LIKE` (it is case-sensitive and uses `*`, `?` and `[...]`).

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


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

PROSE = {}

PROSE[21] = dict(
say="""SQLite has no `split_part`, so I find the delimiter with `INSTR`, cut with `SUBSTR`, and guard every `INSTR` with a `CASE`, because `INSTR` returns 0 when the delimiter is missing and `SUBSTR` then quietly returns the wrong text.""",
sql="""the query `sql` in the Code block. Step `a` drops the first segment (`rest1`), step `b` takes the second segment and finds the position of `';size='`, step `c` cuts the tail after it, and the final SELECT adds the first segment, the last segment and the `size` value. The last segment uses `SUBSTR(sku, LENGTH(RTRIM(sku, REPLACE(sku, '-', ''))) + 1)`: the second argument of `RTRIM` is a set of characters, `REPLACE(sku, '-', '')` is every non-dash character, so `RTRIM` strips the trailing non-dash characters and leaves everything up to and including the last dash. `sql_trap` shows the bug when `INSTR` is 0. For key=value text I search `';' || attributes_text` for `';size='`, so `resize=XL` is not mistaken for `size=`. The recursive split (`rec`) and the `json_each` version are in the Code block for the case of more than three segments.""",
pandas="""`parts = p["sku"].str.split("-")` gives a list per row; `parts.str[0]`, `parts.str[1]` and `parts.str[-1]` are the first, second and last segment (a missing position gives NaN, a missing sku stays NaN). `str.split("-", expand=True)` gives one column per segment, padded with missing values. The size is `p["attributes_text"].str.extract(r"(?:^|;)size=([^;]*)", expand=False)`. All three are in the Code block as `pd_df`.""",
example="""Row 1, `ABC-123-XL`: `INSTR` finds the first dash at 4, so segment 1 is `SUBSTR(sku, 1, 3)` = `ABC` and `rest1` = `123-XL`. In `rest1` the dash is at 4, so segment 2 = `123`. For the last segment, `REPLACE` gives `ABC123XL`, `RTRIM` strips the trailing `XL` (both letters are in that set) and stops at the dash, leaving `ABC-123-` (length 8), so `SUBSTR(sku, 9)` = `XL`. For the attributes, `';' || 'color=red;size=M'` is `;color=red;size=M`, `';size='` starts at 11, and `SUBSTR(..., 11 + 6)` is `M`; there is no later `;`, so the value is `M`. Row 3, `LONE`: no dash, so segment 1 is the whole string, segment 2 is NULL, the last segment is `LONE`, and there is no `size=`, so NULL. The trap on the same row: `SUBSTR('LONE', 1, INSTR(...) - 1)` is `SUBSTR('LONE', 1, -1)`, which gave an empty string, and `SUBSTR(sku, INSTR(sku, '-') + 1)` is `SUBSTR('LONE', 1)`, which gave `LONE` (not NULL, and not "nothing"). Row 7 has `resize=XL`: the naive `INSTR(attributes_text, 'size=')` would find it inside `resize=`; the `';size='` form returns NULL.""",
edge="""- NULL sku or NULL attributes_text: every expression returns NULL (row 4); pandas gives NaN.
- Empty segment is not NULL: `ABC-` gives segment 2 = `''` and last segment = `''` in both SQL and pandas (row 6), and `size=;color=x` gives an empty `size` value, while a missing key gives NULL.
- Fewer segments than asked: `LONE` has no segment 2 (NULL, same as pandas NaN). With the CASE guard this is deliberate; without it you get wrong text.
- Repeated delimiters (`A--B`) produce an empty middle segment; `str.split` does the same.
- `INSTR` is case-sensitive; `SIZE=` would not match `size=`.
- Duplicate keys: `INSTR` finds the first occurrence only.""",
explain="""- **Pattern:** position = `INSTR`, left part = `SUBSTR(x, 1, pos - 1)`, right part = `SUBSTR(x, pos + length_of_delimiter)`. Always wrap in `CASE WHEN INSTR(...) > 0`.
- **Why 0 is dangerous:** `INSTR` returns 0 for "not found", so `pos - 1` is -1 and `pos + 1` is 1. SQLite does not raise an error; it returns an empty string or the whole string. I also checked that `SUBSTR('abc', 0, 2)` returns `a`: position 0 uses up one character of the length.
- **Prefix trick for keys:** search for `';key='` inside `';' || text` so the match always starts at a field boundary.
- **More than three segments:** I would use a recursive split (the mechanics are in Part 9 Q1) that returns one row per segment with its position `n`, then filter `n = 4`. In my run it returned `D` for `A-B-C-D-E`. A `json_each` trick (turn `A-B-C` into a JSON array) also worked and returned `D`, but it breaks as soon as the data contains a double quote or backslash, so I would not ship it. Best of all, split once when loading so the segments live in columns.
- **Other engines (not executed here):** `SPLIT_PART(sku, '-', 2)` in PostgreSQL and Snowflake, `SUBSTRING_INDEX` in MySQL, and `SPLIT(sku, '-')[OFFSET(1)]` in BigQuery, as I remember them; check the engine's documentation before relying on them.
- **pandas:** `str.split(expand=True)` and `str.extract` do all of this in one step, and the result matches the SQL on every row (asserted in the Code block, ordered by `id`).""",
follow="""- *How do you get the last segment when the number of dashes varies?* The `RTRIM`/`REPLACE` trick above, or `str.split(...).str[-1]` in pandas.
- *How do you count the segments?* `LENGTH(sku) - LENGTH(REPLACE(sku, '-', '')) + 1` (not shown in the Code block).
- *Can an index help?* No: `SUBSTR` and `INSTR` on a column prevent index use; store the parsed parts if you filter on them often.""",
mistakes="""- Using the `INSTR` result without checking for 0.
- Off-by-one on the delimiter length (`+ 5` for `size=`, `+ 6` for `;size=`).
- Searching for `size=` and matching `resize=`.
- Treating an empty segment as NULL (or the reverse) and then counting wrongly.
- Starting `SUBSTR` at 0.""",
)

PROSE[22] = dict(
say="""A column compared with a value gets converted by its declared affinity; literals and columns without a declared type are not, so text and numbers sort and compare differently, and the fix is to store numbers as numbers or to `CAST` explicitly.""",
sql="""the queries in the Code block: `sql_text_order` (text order), `sql_cast_order` (`CAST(price_text AS REAL)`), `sql_len_order` (`LENGTH(x), x`, which only works for non-negative integers) and `sql_nat` (a natural order for codes like `A9`, `A10`). The comparison counts, the affinity table (`aff`) and the STRICT table (`s`) are in the Code block too.""",
pandas="""`as_text = pd.read_csv(..., dtype=str)` keeps strings, so `sort_values()` sorts as text; the default `read_csv` turns `price_text` into `float64` and sorts numerically. For `A9, A10, A100` use a key: `nat.sort_values(key=lambda s: s.str.extract(r"(\\d+)", expand=False).astype(int))`. Shown in the Code block.""",
example="""The CSV rows are `9, 10, 100, 2.5` for `price_text`. Stored as TEXT they compare character by character: `'1'` is smaller than `'9'`, so `'10'` and `'100'` come before `'9'`, and `'2.5'` starts with `'2'`, so the text order is `10, 100, 2.5, 9`. With `CAST(... AS REAL)` it is `2.5, 9, 10, 100`. The `LENGTH(x), x` trick gives `9, 10, 100, 2.5`: it is right for the integers (length first), but `'2.5'` has length 3, the same as `'100'`, and `'100' < '2.5'` as text, so it lands last. That is why the trick is only for non-negative integers. For comparisons: `price_text < 9` is true for 3 rows (`'10'`, `'100'`, `'2.5'`) because the TEXT column turns the number 9 into the text `'9'`; `qty < '9'` is also true for 3 rows (qty 3, 7, 5) because the INTEGER column turns `'9'` into the number 9; and `code < 9` is true for 0 rows, because `code` has no declared type, nothing is converted, and text is always greater than a number.""",
edge="""- The same input text under each affinity (Code block, `aff` table): `' 12'` and `'12 '` (leading or trailing space) became the integer 12 in INTEGER and NUMERIC columns and the real 12.0 in a REAL column, `'1e3'` became integer 1000, `'007'` became 7 (the zeros are lost), `'2.50'` became real 2.5, and `'0x10'` and `'abc'` stayed text. TEXT and no-type columns keep the string as given. These are my runs on SQLite 3.45.1.
- STRICT tables (SQLite 3.37 and later): an INTEGER column accepted `'12'` and `' 12'` (converted to 12), accepted `3.0` (stored as 3), and rejected `'abc'` (`cannot store TEXT value in INTEGER column s.a`) and `2.5` (`cannot store REAL value in INTEGER column s.a`). A TEXT column converted the integer 5 to `'5'`. An `ANY` column keeps whatever type arrives. So STRICT stops garbage but does not stop a numeric-looking string from being converted.
- NULL: `NULL < 9` is NULL for all of these, so NULL rows never show up in either direction.
- Negative numbers and decimals break the `LENGTH(x), x` trick (`'-5'` has length 2).
- pandas: `read_csv` treats `NA`, `null`, `None`, `N/A` and `nan` as missing by default (all five became NaN in my run), so a country code `NA` silently becomes missing; use `keep_default_na=False` or `na_values=[...]`.""",
explain="""- **Rule in one line:** if one side is a column with INTEGER, REAL or NUMERIC affinity, the other side is converted to a number when it looks like one; if one side has TEXT affinity and the other no affinity, the number is converted to text; literals alone get no conversion, so `'1' = 1` is false (my run: 0).
- **Cross-type order:** with no conversion a number is always smaller than text (`10 < '9'` is 1).
- **Fix:** best is to load numbers into INTEGER or REAL columns (or `CAST` while loading). Use `CAST` in the query when you cannot change the table; use `LENGTH(x), x` only for non-negative integers; use a natural-sort key for mixed codes.
- **Casting garbage:** `CAST('abc' AS REAL)` is 0.0, not an error, so a failed cast hides bad data (Q24 has the same trap for dates). Use `GLOB '*[^0-9]*'` or a round-trip check to find bad rows.
- **pandas:** `read_csv` infers dtypes for you, so check `dtypes` after loading. Sorting `str` values is lexicographic, exactly like SQLite's text order.
- Other engines are stricter (they usually raise an error on `'abc' < 5` or convert by their own rules); I did not execute any of them here.""",
follow="""- *Why did `' 12'` become an integer?* The INTEGER affinity accepts text that looks like a number, including surrounding spaces; `TEXT` affinity does not. I ran this; I did not find it stated in the pages opened for the Wave A note.
- *What would STRICT have changed?* It rejects `'abc'` and `2.5` in an INTEGER column with an error, instead of storing text.
- *How do you sort `v1.2`, `v1.10`?* Split into numeric parts and sort on those (a key function in pandas; two `CAST`s in SQL).""",
mistakes="""- Sorting numbers stored as text and trusting the order.
- Assuming a column named `price` is numeric because the values look numeric.
- Comparing a no-type column with a number and getting 0 rows without an error.
- Using `LENGTH(x), x` on decimals or negatives.
- Letting `read_csv` guess: `NA` becomes NaN, and `007` becomes 7.""",
)

PROSE[23] = dict(
say="""SQLite has no `LPAD`/`RPAD`; use `PRINTF('%05d', n)` for zero padding (it never cuts digits), and treat `SUBSTR('00000' || n, -5)` as a trick that silently drops digits when the number is longer than the pad.""",
sql="""the single query `sql` in the Code block: `code_substr`, `code_printf` (`PRINTF('INV-%05d', invoice_no)`), `name_left` (`PRINTF('%-10s|', customer_name)`), `name_trunc` (first 9 characters plus an ellipsis when longer than 10), and `amount_comma` (`PRINTF('%,.2f', amount)`). Extra checks (negative numbers, NULL, rounding) follow it.""",
pandas="""`pd_df` in the Code block: `str.zfill(5)` on the string version of the number, `str.ljust(10)` (or `str.pad(10, side="right")`), `str[:9]` plus an ellipsis, and an f-string `f"{x:,.2f}"` for the amount; `Series.round(2)` is shown separately.""",
example="""Invoice 42: `'00000' || 42` is `0000042`, and the last 5 characters are `00042`, so `INV-00042`. Invoice 123456 has 6 digits: `'00000123456'` last 5 characters are `23456`, so the trick prints `INV-23456` (wrong, and it can collide with invoice 23456), while `PRINTF('%05d')` prints `INV-123456`. A negative number goes wrong too: `'00000' || -42` ends `...00-42`, giving `INV-00-42`, while `PRINTF` gives `INV--0042`. The name `Alexander Hamilton` has 18 characters, so we keep 9 (`Alexander`) and add `…`; `Bo` is left as is and padded to 10 by `%-10s`. Amount 1234.5 becomes `1,234.50`. Invoice 99999 has amount 703.125: SQLite prints `703.13`, Python and pandas print `703.12` (see Edge cases).""",
edge="""- **Rounding differs by tool (my run):** `ROUND(703.125, 2)` and `PRINTF('%.2f', 703.125)` both gave 703.13 (SQLite rounds the exact tie up); Python's `round` and f-string gave 703.12; `Series.round(2)` gave 703.12 for 703.125, **2.68** for 2.675 (SQLite and Python both gave 2.67) and 0.12 for 0.125. So even pandas and Python round differently on 2.675. The stored double for 2.675 is just below the tie, so 2.67 is the exact answer; pandas' 2.68 presumably comes from scaling by 100 before rounding (I did not verify the mechanism). Compare money in integer cents, or use `decimal`.
- **`PRINTF('%.0f')` truncates in this SQLite build:** `0.6`, `1.6` and `2.6` printed `0`, `1`, `2`, and after `ROUND` first they printed `1`, `2`, `3`. The Wave A note guessed half-to-even rounding; the run shows truncation, so round first.
- **NULL:** `'N:' || NULL` is NULL, but `PRINTF('%s', NULL)` is an empty string and `PRINTF('%d', NULL)` is `0`; `PRINTF('%,.2f', NULL)` printed `0.00`, which looks like a real amount. Guard with `CASE WHEN amount IS NULL THEN NULL ELSE ... END`. pandas keeps NaN.
- **Longer than the pad:** `%05d` and `zfill` do not cut; `SUBSTR(..., -5)` does.
- **Negative width or number:** shown above; `zfill` keeps the sign first (`'-42'.zfill(5)` is `-0042`, same as `PRINTF`).
- **Thousands comma:** `%,d` and `%,.2f` worked in this SQLite 3.45.1 build; it is a SQLite extension I did not find documented in the pages opened, so do not rely on it in other engines.""",
explain="""- **Why `SUBSTR(..., -5)` works:** a negative start counts from the right, so it takes the last 5 characters. It is only safe when the number is known to have at most 5 digits and is not negative.
- **Left-justify and truncate:** `%-10s` pads on the right; for truncation use `SUBSTR` with an ellipsis (here a single character, so the total is 10). `LENGTH` counts characters, `OCTET_LENGTH` counts bytes.
- **Rounded strings:** `PRINTF('%.2f', x)` returns text, `ROUND(x, 2)` returns a number; do the arithmetic before formatting.
- **Other engines (not executed here):** `LPAD`/`RPAD` exist in PostgreSQL, MySQL and Oracle; SQL Server has `FORMAT` and `RIGHT('00000' || ...)`-style tricks; `TO_CHAR(n, 'FM00000')` in PostgreSQL and Oracle; MySQL also has `FORMAT(x, 2)`. I wrote these from memory.
- **pandas:** `zfill`, `pad`, `ljust` and f-strings match the SQL on every cell I asserted; the only differences are the 703.125 tie and the NULL row (asserted in the Code block).""",
follow="""- *How do you pad on the right with a custom character?* `SUBSTR(n || 'XXXXX', 1, 5)`-style tricks in SQLite (not run here), `str.pad(width, side="right", fillchar="x")` in pandas.
- *Why not `FORMAT` in SQLite?* `FORMAT` exists as an alias of `PRINTF` in this build, but other engines' `FORMAT` has different codes.
- *Should the invoice code be stored?* Store the integer and format on output; a padded string sorts correctly only while the width is fixed.""",
mistakes="""- Using `SUBSTR('0000' || n, -5)` with a short pad and losing digits.
- Formatting before summing (strings do not add).
- Assuming `PRINTF` of NULL gives NULL.
- Trusting `PRINTF('%.0f')` to round.
- Expecting SQL, Python and pandas to round a tie the same way.""",
)

PROSE[24] = dict(
say="""`DATE()` in SQLite returns NULL for anything that is not an ISO shape (no error), but it also quietly "fixes" impossible days such as `2024-02-30` into `2024-03-01`, so you need a round-trip check to find bad rows.""",
sql="""`sql_failed` (rows that fail to parse: `WHERE DATE(d_text) IS NULL AND d_text <> ''`) and `sql_clean` (a `CASE` with one branch per shape: ISO with or without time, `dd/mm/yyyy` rebuilt with `SUBSTR`, `yyyymmdd` rebuilt with `SUBSTR`, each branch guarded by `GLOB` and by a round-trip test `DATE(x) = x`) are in the Code block.""",
pandas="""`pd.to_datetime(d, errors="coerce")`, `format="mixed"` and `dayfirst=True` are printed in the Code block. The comparable version parses each shape with an explicit format (`str.fullmatch` masks plus `format="%d/%m/%Y"` and so on) and gives the same result as the SQL `CASE`.""",
example="""Row 1 `2024-03-05` parses. Row 2 `2024-3-5` is NULL (SQLite needs two-digit month and day). Row 3 `05/03/2024` is NULL, and a human cannot tell whether it is 5 March or 3 May; my rule says day first, so the `SUBSTR` rebuild gives `2024-03-05`. Row 4 `2024-03-05 14:30` gives `2024-03-05` (a time part is accepted). Row 5 `20240305` is NULL for `DATE()`; the `GLOB` branch rebuilds it as `2024-03-05`. Row 6 `2024-02-30`: **`DATE()` returned `2024-03-01`, not NULL** (the question text assumes NULL; this run says otherwise). Only the round-trip check `DATE(x) = x` catches it (`2024-03-01` is not equal to `2024-02-30`), so the CASE returns NULL. Rows 7 and 8 (empty and NULL) are NULL; `sql_failed` skips them because of `d_text <> ''` and because `NULL <> ''` is not true. Failed rows: 2, 3 and 5.""",
edge="""- **Impossible dates are normalised, not rejected:** `DATE('2024-02-30')` gave `2024-03-01`, `DATE('2023-02-29')` gave `2023-03-01`, `DATE('2024-04-31')` gave `2024-05-01`. A month 13, month 00 or day 32 does give NULL (`2024-13-01`, `2024-00-10`, `2024-02-32` all returned NULL in my run). So the question's claim that `2024-02-30` returns NULL is wrong for SQLite 3.45.1.
- **Empty string and NULL:** both give NULL; separate them with `d_text <> ''` and `IS NOT NULL` if you need to report them differently.
- **Ambiguity:** `05/03/2024` has no right answer without a rule from the source system; do not guess per row.
- **pandas:** `to_datetime(d, errors="coerce")` took its format from the first value and gave `NaT` for the slash form, the compact form and the `14:30` form (`2024-3-5` still parsed). `format="mixed"` parsed `05/03/2024` as **3 May** (month first) and everything else as 5 March. `format="mixed", dayfirst=True` gave 5 March for the slash form but also turned the ISO strings `2024-03-05` into **3 May**, so do not use `dayfirst` on a column that also has ISO values. `2024-02-30` is `NaT` in pandas (no normalisation). Without `errors="coerce"` a bad value raises `ValueError`.
- The same string parsed two ways: `format="%m/%d/%Y"` gave 2024-05-03 and `format="%d/%m/%Y"` gave 2024-03-05.""",
explain="""- **ISO is the shape to rely on for SQLite date functions** (with the quirk above); store dates as `YYYY-MM-DD` text (Part 6 Q1 covers storage).
- **Detect failures:** `DATE(x) IS NULL AND x <> ''`, plus the round-trip test to catch normalised days.
- **Fix known shapes explicitly:** `GLOB` guard, then `SUBSTR` rebuild, then validate.
- **Other engines (not executed here, from memory):** `TO_DATE` (PostgreSQL, Oracle) and `STR_TO_DATE` (MySQL) take a format string; `TRY_CONVERT` (SQL Server) and `SAFE.PARSE_DATE` (BigQuery) return NULL instead of raising an error. Some of them raise errors on invalid input, unlike SQLite.
- **pandas:** be explicit with `format=`; `errors="coerce"` hides failures, so count the `NaT` rows against the input afterwards (`d.notna() & parsed.isna()`).""",
follow="""- *How would you report the bad rows?* `WHERE DATE(x) IS NULL AND x <> ''` plus the round-trip mismatch, with a count per shape.
- *Why not `CAST(x AS DATE)`?* SQLite has no date type; `CAST('2024-03-05' AS INTEGER)` and `AS NUMERIC` both gave 2024 in my check, which looks fine and is wrong.""",
mistakes="""- Believing `DATE()` returns NULL for every impossible date.
- Assuming `dd/mm/yyyy` without asking the source.
- Letting `errors="coerce"` swallow bad rows without counting them.
- Using `dayfirst=True` on a mixed column and flipping the ISO values.
- Comparing date strings that are not zero-padded (`'2024-3-5' > '2024-12-01'` is true as text).""",
)

PROSE[25] = dict(
say="""Comparison operators say "unknown", set operators and `GROUP BY` say "same": NULLs are grouped, de-duplicated and intersected as one value, but a NULL never matches in `=`, `IN` or a join.""",
sql="""the `queries` dictionary in the Code block: `distinct`, `group_by`, `union`, `union_all`, `intersect`, `except`, `not_in`, `join_eq`, `join_isnd` (null-safe join with `IS`) and `in_subquery`, plus the `COUNT(*)`, `COUNT(email)`, `COUNT(DISTINCT email)` line. The `NOT IN` trap itself is Part 3 Q3; here it is only compared with `EXCEPT`.""",
pandas="""`drop_duplicates()`, `concat(...).drop_duplicates()`, `isin` for intersect and except, `groupby(a, dropna=False).size()`, `nunique(dropna=False)` and an inner `merge` on the email column, all in the Code block as `p_res`.""",
example="""`contacts_a` = `a@x.com`, `a@x.com`, NULL, NULL, `b@x.com`. `contacts_b` = `a@x.com`, NULL, `c@x.com`, NULL. `SELECT DISTINCT` on A gives 3 rows: NULL, `a@x.com`, `b@x.com` (the two NULLs collapse). `COUNT(*)` is 5, `COUNT(email)` is 3 (NULLs skipped), `COUNT(DISTINCT email)` is 2. `UNION` gives NULL, `a`, `b`, `c` (4 rows). `INTERSECT` gives NULL and `a@x.com`: both sides have a NULL and the operator treats them as the same, although `NULL = NULL` is not true. `EXCEPT` gives only `b@x.com`: `a@x.com` is in B, and the NULL in A is removed because B has a NULL. The `NOT IN` version of the same question returned **no rows** because B contains a NULL, so `EXCEPT` and `NOT IN` disagree on this data. The `=` join returned 2 rows (just the two `a@x.com` rows of A), while the null-safe join (`IS`) returned 6: 2 x 2 NULL pairs plus 2.""",
edge="""- NULL sorts first in SQLite ascending order; pandas `groupby` puts the NaN group last, so sort before comparing (the Code block does).
- `COUNT(DISTINCT)` is 2 but `SELECT DISTINCT` returns 3 rows: the NULL row is a row, but not a value.
- `UNION ALL` keeps every NULL (4 of them here).
- Duplicates: `UNION`, `INTERSECT` and `EXCEPT` also de-duplicate; `UNION ALL` does not.
- Empty strings are not NULL: `''` is a value that groups separately.
- **pandas surprises (my run):** `merge` matched NaN with NaN (6 rows, equal to the null-safe SQL join, not to the `=` join); `isin` treats NaN as found (`[nan, 1.0].isin([nan])` gave `[True, False]`) while `==` does not (`False`); `nunique()` defaults to `dropna=True` (2) and `nunique(dropna=False)` gives 3; `groupby` drops the NaN group by default (2 groups against 3).""",
explain="""- **Interview line:** "comparison operators say unknown, set operators say same."
- **Why:** `=`, `IN` and joins need a TRUE, and `NULL = NULL` is UNKNOWN. `DISTINCT`, `GROUP BY`, `UNION`, `INTERSECT` and `EXCEPT` use "not distinct from" semantics, so two NULLs are the same.
- **Safer anti-join:** `EXCEPT` or `NOT EXISTS` do not break on NULLs the way `NOT IN` does. Which one you want depends on whether a NULL should count as "present in B".
- **Null-safe equality:** `IS` in SQLite (and `IS DISTINCT FROM`, which also ran on 3.45.1) is the SQL way to match NULLs; Part 1 Q41 covers it.
- **Other engines:** the standard behaviour is the same in the engines I know, but I did not run Postgres, MySQL, BigQuery or Snowflake here (not executed).
- **Cross-references:** Part 1 Q16 for aggregation basics, Part 3 Q3 for `NOT IN`.""",
follow="""- *Does `INTERSECT` need the columns to match positionally?* Yes, by position and compatible types, not by name.
- *How do you make a join match NULLs?* `ON a.email IS b.email` in SQLite (null-safe), or `COALESCE` to a sentinel (risky if the sentinel is real data).
- *Which count should a report use?* Decide whether NULL is a category; `COUNT(DISTINCT)` hides it.""",
mistakes="""- Saying "NULL = NULL is false" (it is unknown).
- Expecting `INTERSECT` to drop NULL rows because `=` does.
- Using `NOT IN` where `EXCEPT` or `NOT EXISTS` was meant.
- Merging in pandas on a key with NaN and expecting SQL join behaviour.
- Reading `COUNT(DISTINCT)` as the number of rows `DISTINCT` returns.""",
)

PROSE[26] = dict(
say="""A NULL passes UNIQUE (many NULLs are allowed) and passes CHECK (UNKNOWN counts as pass), SQLite lets a non-INTEGER PRIMARY KEY hold NULL unless you add NOT NULL, and a nullable flag has three states, so `WHERE is_active = 0` misses the unknown rows and `IS NOT TRUE` catches them.""",
sql="""the `attempt` lines in the Code block (each INSERT runs and prints ok or the error), then `sql_probe` (all the flag tests side by side), `sql_counts` (active, inactive, unknown, total) and the three `WHERE` variants.""",
pandas="""`u["is_active"].astype("boolean")` gives the nullable boolean dtype (`True`, `False`, `<NA>`). Counts use `(flag == True).sum()`, `(flag == False).sum()` and `flag.isna().sum()`; `IS NOT TRUE` is `(flag != True).fillna(True)`. All in the Code block.""",
example="""Users 1 to 5 have flags 1, 1, 0, NULL, NULL. `is_active = 0` returns user 3 only. `is_active <> 1` also returns only user 3 (NULL <> 1 is unknown). `NOT is_active` is NULL for users 4 and 5, so it misses them too. `is_active IS NOT TRUE` returns users 3, 4 and 5. Counts: `IS TRUE` 2, `IS FALSE` 1, `IS NULL` 2, which sum to the 5 users. For constraints: the second `INSERT NULL` into the UNIQUE column succeeded (two NULL rows), `age = 17` failed with `CHECK constraint failed: age >= 18`, `age = NULL` and `18` passed, two NULL codes went into the `TEXT PRIMARY KEY` table, the `NOT NULL` version and the `WITHOUT ROWID` version rejected NULL, and a NULL into `INTEGER PRIMARY KEY` got the id 1.""",
edge="""- `NULL IS TRUE` is 0, `NULL IS NOT TRUE` is 1, `NOT NULL` is NULL (my run: `(0, 1, None)`).
- Values other than 0 and 1 (for example 2) can be stored (not run here); only a CHECK on the flag would stop them, so add `CHECK (is_active IN (0, 1))`: a NULL still passes that CHECK too.
- A foreign key with a NULL column is not checked, for the same UNKNOWN reason (not run here).
- **pandas:** `read_sql` returned the flag as `float64` with NaN (ints plus NULL), where `!= 1` is True for NaN (pandas differs from SQL, which gives unknown) and `== 0` matches only the real zero. With the nullable boolean dtype, `== False` gives `<NA>` for the unknown rows, `bool(pd.NA)` raises `TypeError` (`boolean value of NA is ambiguous`), and using the NA mask to filter rows (`u[flag == False]`) treats NA as False, so it returns user 3 only.""",
explain="""- **Why UNIQUE allows many NULLs:** two NULLs are not "equal", so they do not violate uniqueness. The standard-style rule is the same in the engines I know, but I did not run them here (not executed).
- **Why CHECK passes NULL:** a CHECK fails only when the expression is FALSE; UNKNOWN is accepted. To forbid NULL add `NOT NULL`.
- **Non-INTEGER PRIMARY KEY:** SQLite lets NULL in for historical reasons (the run shows two NULL codes); `NOT NULL` or `WITHOUT ROWID` stops it. Most other engines reject NULL in a primary key; I did not execute any.
- **Tri-state flags:** pick one of: make the column `NOT NULL DEFAULT 0`, or keep NULL as "unknown" and always write `IS TRUE`, `IS FALSE`, `IS NOT TRUE`. Never write `<> 1` or `NOT flag` unless you want to lose NULLs.
- **Other engines (not executed):** PostgreSQL 15 added `UNIQUE NULLS NOT DISTINCT` so that NULLs count as equal, and I recall that SQL Server treats a unique constraint as allowing only one NULL; check the documentation of your version before relying on either.
- **pandas:** use the nullable `boolean` dtype so that NA stays NA instead of turning into False or NaN.""",
follow="""- *How do you allow only one NULL in SQLite?* A partial unique index: `CREATE UNIQUE INDEX u_one_null ON u_one((email IS NULL)) WHERE email IS NULL` (in the Code block: the second NULL failed with `UNIQUE constraint failed: index 'u_one_null'`, while repeated `'a'` values were still allowed).
- *What does `COUNT(*)` give per state?* `GROUP BY is_active` returns three groups: 1, 0 and NULL.
- *Should the flag be nullable at all?* Only if "unknown" is a real business state.""",
mistakes="""- `WHERE is_active != 1` to mean "not active".
- Believing CHECK(age >= 18) rejects NULL ages.
- Using a non-INTEGER PRIMARY KEY without NOT NULL in SQLite.
- Counting active and inactive and forgetting the unknown group (the three do not add up to the total).
- Casting a pandas NaN flag to `bool` (NaN becomes True).""",
)

PROSE[27] = dict(
say="""Compute each cell once, then divide by a row, column or grand total taken with a window function or a scalar subquery, wrap the divisor in `NULLIF(..., 0)`, and expect rounded percentages to sum to 99.9 or 100.1.""",
sql="""`pivot_sql(measure)` in the Code block builds the same query three times with `row_pct`, `col_pct` or `grand_pct`. The CTE `cell` sums the sales per region and product, `m` adds `SUM(amt) OVER (PARTITION BY region)`, `SUM(amt) OVER (PARTITION BY product)` and a scalar subquery for the grand total, and the outer query pivots one measure with `ROUND(SUM(CASE WHEN product = 'A' THEN ... END), 1)`.""",
pandas="""`pd.crosstab(index=..., columns=..., values=..., aggfunc="sum", normalize="index")` (and `"columns"`, and `True`), times 100, rounded to 1. Because `crosstab` fills empty cells with 0.0, the Code block also builds the NULL-faithful version with `pivot_table` and explicit division, and asserts both.""",
example="""Rows: East 10, 10, 10 (total 30); South 10, 10, 40 (total 60); West A 10 and C 30 only (total 40); North 0, 0, 0 (total 0). Grand total 130. East row percent: 10/30 = 33.3 each, so the row shows 33.3 + 33.3 + 33.3 = **99.9**. South: 16.7 + 16.7 + 66.7 = **100.1**. West: 25.0, NULL, 75.0 (no B sales, so no cell). North: the row total is 0, `NULLIF` turns the divisor into NULL, so the whole row is NULL. Column totals: A 30, B 20, C 80, so East A is 10/30 = 33.3 and East C is 10/80 = 12.5. Grand percent: East A is 10/130 = 7.7, South C is 40/130 = 30.8.""",
edge="""- **Rounding:** the rounded parts need not sum to 100. The unrounded East shares are 33.3333 each, and 3 x 33.3 = 99.9; South's 16.67 and 66.67 round up and give 100.1. Show one more decimal, or put the rounding error in the largest cell, if the report must add to 100.
- **Zero total:** without `NULLIF`, `100.0 * 0 / 0` gives NULL in SQLite (it does not raise an error; my run), but PostgreSQL raises a division by zero error (not executed here, from memory). `NULLIF` makes the intent explicit in every engine.
- **Missing cell (West, B):** SQL gives NULL. `crosstab` gives 0.0 in all three tables, and gives 0.0 for the North row percent (0/0), where SQL gives NULL. The asserts in the Code block show `crosstab` equals the SQL result after `fillna(0)`, and the `pivot_table` division equals the SQL result exactly.
- **Column percent for North** is 0.0 (not NULL) in SQL because the column totals are not zero.
- Ties and duplicates: duplicate rows per cell are summed first (`cell`).""",
explain="""- **Three denominators:** row = total over the region, column = total over the product, grand = total over everything. A window `SUM() OVER (PARTITION BY ...)` gives the first two without a second query; a scalar subquery gives the grand total.
- **Order of operations:** aggregate to cell level first, then divide. Dividing raw rows by a total gives the same totals but is easy to get wrong with duplicates.
- **Why `100.0`:** it forces floating-point division; `100 * 4 / 10` with integers can truncate.
- **pandas:** `normalize` has three options: `"index"` (rows), `"columns"`, `True` (all). Check what happens to empty cells before comparing with SQL.
- Cross-reference: Part 1 Q10 for plain conditional aggregation.""",
follow="""- *How would you show counts and percentages together?* Two measures per cell in the long CTE, then pivot both.
- *Why use a window and not a self-join?* One scan, no join, same result.
- *How do you force the percentages to add to 100?* Largest remainder method: round down, then distribute the leftover units to the biggest remainders.""",
mistakes="""- Dividing by `SUM(amount)` without `NULLIF`.
- Using integer division.
- Calculating a column percent with the row total.
- Rounding before summing the percentages and then reporting the sum as an error.
- Assuming pandas `crosstab` returns NaN for empty cells (it returned 0.0 here).""",
)

PROSE[28] = dict(
say="""`melt` is the pandas `UNION ALL` unpivot (it keeps NaN rows), `wide_to_long` is for column names like `math_2023`, `stack`/`unstack` work on the index, and pandas 3 keeps NaN rows in `stack` where the old implementation dropped them.""",
sql="""`sql_unpivot` (4-branch `UNION ALL`, one row per student, subject and year, NULL scores kept), `sql_w2l` (2 branches, one column per subject, the shape `wide_to_long` returns) and `sql_pivot` (`SUM(CASE WHEN subject = ... AND year = ... THEN score END)`) are in the Code block.""",
pandas="""`wide.melt(id_vars="student", var_name="col", value_name="score")` then a split of `col` into subject and year; `pd.wide_to_long(wide, stubnames=["math", "sci"], i="student", j="year", sep="_", suffix=r"\\d+")`; `long.set_index([...])["score"].unstack(["subject", "year"])` (with `fill_value`); and `stack` on a larger frame. All in the Code block.""",
example="""Three students: Zed 90, 92, 80, NULL; Ana 70, NULL, 65, 66; Mia all NULL. The wide table has 3 rows and 4 score columns, so the unpivot has 12 rows, and 6 of them have a NULL score (Zed 1, Ana 1, Mia 4). `melt` returned the same 12 rows, and 6 remain after `dropna`. `wide_to_long` returns 6 rows (student, year) with columns `math` and `sci`. Going back with `unstack` returns 3 rows sorted `Ana, Mia, Zed` although the input order was Zed, Ana, Mia, and the SQL `SUM(CASE)` pivot returns the same numbers, with NULL where all inputs are NULL.""",
edge="""- **`melt` keeps NaN rows;** use `dropna(subset=["score"])` (or `WHERE score IS NOT NULL` in SQL) to drop them. Both give 12 rows with NULLs and 6 without.
- **`unstack(fill_value=0)`** fills only cells that are missing from the index. The NaN scores are stored values, so Mia's row stayed `[nan, nan, nan, nan]` (my run). After `dropna`, Mia vanished from the result and Ana's missing `math_2024` became 0. SQL needs `COALESCE` to do the same.
- **Sorting:** `unstack` sorted the row index (`Ana, Mia, Zed`). The column order followed first appearance when some combinations were absent (my run: `math_2023, sci_2023, sci_2024, math_2024`), so add `.sort_index(axis=1)` before comparing.
- **Duplicates:** `unstack` and `pivot` raise an error when a student/subject/year pair repeats; SQL `SUM(CASE)` silently adds them. Use `pivot_table` with an `aggfunc` in pandas to mirror SQL.
- **stack on a larger frame (1000 rows x 6 columns, 143 NaN cells, my run):** `stack()` gave 6000 rows, `stack(future_stack=True)` gave 6000, `stack(future_stack=False)` gave 5857 and raised a `Pandas4Warning` (the old implementation drops NaN), `stack(dropna=True)` raised `ValueError` (the argument is not allowed with the new implementation), and `stack().dropna()` gave 5857. So in pandas 3.0.5 NaN rows are kept by default and `future_stack` is no longer needed.""",
explain="""- **Which tool:** `melt` for plain wide to long; `wide_to_long` when the column names follow `stub + separator + suffix` and you want one column per stub; `stack` when the labels are already in the columns index; `unstack` or `pivot` for long to wide.
- **SQL equivalents:** unpivot = `UNION ALL` (or `CROSS JOIN` with `VALUES`); pivot = `SUM(CASE ...)`. SQLite has no `PIVOT` or `UNPIVOT` keyword; SQL Server, Oracle, Snowflake and BigQuery have their own (not executed here).
- **NULL rule of thumb:** decide whether missing means "unknown" (keep NaN) or "none" (fill 0), before reshaping, not after.
- **Asserts:** UNION ALL equals `melt`, the 2-branch UNION ALL equals `wide_to_long`, and `SUM(CASE)` equals `unstack`, all ordered by student (then subject, year).""",
follow="""- *How do you unpivot in SQL without writing every column?* Generate the `UNION ALL` text from a column list (the dynamic pivot question later in this part).
- *What does `ignore_index` do in `melt`?* With `ignore_index=False` the original index is kept (not run here).
- *When is `pivot_table` better than `pivot`?* When there can be duplicate keys.""",
mistakes="""- Forgetting that `melt` keeps NaN rows (and that `unstack` fills by index, not by value).
- Using the deprecated `future_stack=False` or `dropna=` in pandas 3.
- Comparing unsorted frames.
- Assuming a `pivot` of duplicate keys sums them (it raises).
- Leaving the year as a string after splitting a column name.""",
)

PROSE[29] = dict(
say="""Most SQL string functions have a one-line pandas twin, but the defaults differ in four places that bite: `str.replace` is not a regex any more, `str.contains` is a regex by default, `LIKE` ignores case but `startswith` does not, and NULL becomes NaN (or False) instead of staying NULL.""",
sql="""each pair is one SQL expression against one pandas expression in the `cases` list in the Code block (`LOWER`, `UPPER`, `TRIM`, `SUBSTR`, `INSTR`, `REPLACE`, `LIKE`, `||` and `CONCAT_WS`, `LENGTH`, `SUBSTR`+`INSTR` for splitting, `SUBSTR('00000' || code, -5)` and `PRINTF` for padding).""",
pandas="""the second element of each pair: `str.lower`, `str.upper`, `str.strip`, `str[0:3]`, `str.find`, `str.replace`, `str.startswith`, `str.contains`, `+` and `str.cat`, `str.len`, `str.split(n=1)`, `str.extract` with named groups, `str.zfill` and `str.pad`. The loop prints SQL and pandas results side by side, with `same` or `DIFF`, and asserts both (22 rows).""",
example="""Contacts: `Asha Rao`, ` ben kumar ` (spaces around), NULL, `Dee  Lee` (two spaces), `chitra`; emails `Asha.Rao@Example.com`, `ben@test.org`, `noatsign`, `dee.lee@a.b.com`, NULL. `LOWER`, `UPPER`, `TRIM`, `SUBSTR(name, 1, 3)`, `LENGTH` and `INSTR(email, '@')` match pandas row by row (INSTR is 0 where `find` is -1, plus 1; NULL is NaN). The `DIFF` rows: `REPLACE(name, '  ', ' ')` gives `Dee Lee` while `str.replace(" +", " ")` left `Dee  Lee` (regex is off by default in pandas 3); `name LIKE 'a%'` is 1 for `Asha Rao` while `startswith('a')` is False; `email LIKE '%.%'` is 0 for `noatsign` while `str.contains('.')` (default regex) is True because a dot matches any character; `CONCAT_WS('-', name, code)` gives `123` for the NULL-name row while `str.cat(..., na_rep='')` gives `-123`; `PRINTF('%5s', code)` gives 5 spaces for a NULL code while `pad` keeps NaN.""",
edge="""- **NULL and `LIKE`:** SQL `name LIKE 'a%'` is NULL for a NULL name; pandas `str.startswith` returns False for NaN in the `str` dtype. The Code block compares the `COALESCE(..., 0)` form and the raw form.
- **`na` argument of `contains` (my run, email column with one NaN):** `str` dtype default gave `[True, True, False, True, False]`; object dtype gave `nan` for the missing row; `string` dtype gave `<NA>`; `na=True` gave `True`. SQL gave NULL for that row.
- **Case:** SQLite's `LIKE` is case-insensitive for ASCII only, and `PRAGMA case_sensitive_like = 1` made `'Asha' LIKE 'a%'` return 0 in my run. I did not test pandas `case=False` on non-ASCII text.
- **Concatenation:** `||` and `+` both propagate missing values; `CONCAT_WS` skips NULLs (it ran on 3.45.1), and the pandas equivalent is a row-wise join of the non-missing values, not `na_rep=''`.
- **Length:** `str.len()` returns `float64` when NaN is present; `LENGTH` returns an integer or NULL.
- **Title case:** SQLite has no `INITCAP`; `str.title()` gave `O'Neil` for `o'neil` and `Mc Donald` for `mc donald`, but `They'Re` for `they're`, so it is not a safe name formatter.""",
explain="""- **Translation table:** the printed output is the table; every `same` row is asserted equal and every `DIFF` row is asserted to differ.
- **Regex defaults (pandas 3.0.5, my run):** `str.replace` regex=False; `str.contains` regex=True. Always pass `regex=` explicitly, and pass `na=` when the column has missing values.
- **Indexing:** SQL `SUBSTR` is 1-based, pandas slices are 0-based.
- **`str` versus `string` dtype:** pandas 3 infers `str` with NaN as the missing marker; `dtype="string"` uses `pd.NA` and returns `<NA>` from `contains`.
- **Other engines (not executed):** regex functions (`REGEXP_REPLACE`, `REGEXP_LIKE`, `REGEXP_SUBSTR` in various spellings), `LPAD`, `INITCAP`, `SPLIT_PART` exist in other engines and not in this SQLite build; the 3.45.1 build used here has no `regexp`, `split_part`, `reverse`, `lpad` or `char_length` (from the Wave A check).""",
follow="""- *How do you do a regex match in SQLite?* Register a Python function with `create_function("regexp", 2, fn)` (it worked in the Wave A check), or avoid regex with `GLOB`/`LIKE`.
- *What is the pandas twin of `GLOB`?* `str.fullmatch` or `str.match` with a regex (not run here).
- *How do you reverse a string in SQLite?* Not built in; a recursive CTE, or do it in Python.""",
mistakes="""- Using `str.replace(" +", " ")` and expecting it to collapse spaces.
- Using `str.contains(".")` for a literal dot.
- Expecting `startswith` to be case-insensitive like `LIKE`.
- Concatenating with `+` and losing rows to NaN.
- Forgetting 0-based versus 1-based positions.""",
)

PROSE[30] = dict(
say="""Without `ROLLUP` or `CUBE`, build the subtotals as separate `GROUP BY` queries, stack them with `UNION ALL`, label the total rows `'ALL'`, and add a sort-key column so the totals come last; then check that the grand total equals the plain `SUM`.""",
sql="""`sql_long` in the Code block: detail by region and product, a subtotal per region, a subtotal per product, and the grand total, with a `k` column (0 to 3) so `ORDER BY k, region, product` puts totals last. `sql_wide` is the pivoted shape (one row per region plus one `ALL` row, columns A, B, C and Total). `sql_null_label` and `sql_safe` show the NULL-label trap.""",
pandas="""`pivot_table(index="region", columns="product", values="amount", aggfunc="sum", margins=True, margins_name="ALL")` gives the same table, and a `groupby(...).sum().unstack()` plus an `ALL` row built from column sums gives it a second way. Both are asserted equal to the SQL result.""",
example="""Sales: East A 10 + 5 (two rows), East B 20, East C 30; West A 40, West B 15; West has no C. Detail rows: East A 15, East B 20, East C 30, West A 40, West B 15. Region subtotals: East 65, West 55. Product subtotals: A 55, B 35, C 30. Grand total 120, and the plain `SUM(amount)` is 120. In the pivoted table: East 15, 20, 30, total 65; West 40, 15, NULL, total 55; ALL 55, 35, 30, total 120. The NULL in West's C cell stays NULL (no rows), it is not 0.""",
edge="""- **Missing cell:** `SUM(CASE ...)` is NULL where no rows exist, and `pivot_table` shows NaN; the totals skip them. Use `COALESCE(..., 0)` only if the report should show zeros.
- **NULL-label trap (my run):** with a real NULL product and subtotals that use NULL as the label (what `ROLLUP` prints), the East rows `(East, NULL, 7)` and `(East, NULL, 17)` cannot be told apart: `WHERE product IS NULL` returns 2 rows. Labelling the subtotal `'ALL'` explicitly, and `COALESCE(product, '(no product)')` for the real NULL, keeps them separate. A real product literally named `ALL` would still collide, so choose a label that cannot be data or use a separate flag column.
- **pandas drops NaN keys:** with a NaN product, `pivot_table(margins=True)` gave a grand total of 15 against a plain SUM of 22 in my run (the 7 for the NULL product vanished), so the margins do not equal the plain sum unless NaN keys are filled first.
- **Ordering:** `UNION ALL` gives no order, and `ORDER BY` of a compound query must use result columns, hence the `k` column (SQLite raised `2nd ORDER BY term does not match any column in the result set` when I tried a computed expression).""",
explain="""- **Equivalence:** `ROLLUP(region, product)` gives detail, region subtotals and the grand total; `CUBE` adds product subtotals; here I wrote all four levels by hand. `GROUPING SETS` is the general form. SQLite has none of the three.
- **Telling a subtotal NULL from a real NULL:** `GROUPING(col)` returns 1 for a subtotal row in PostgreSQL, MySQL and SQL Server (not executed here, from memory); with `UNION ALL` you choose the label yourself.
- **Check:** the grand total must equal the plain `SUM(amount)`, and the `ALL` row total must equal the sum of the region totals (all 120 in my run).
- **Cost:** each `UNION ALL` branch scans the table again; with `ROLLUP` the engine can usually do it in one pass (I did not measure this).
- Cross-reference: Part 1 Q36 for ROLLUP concepts.""",
follow="""- *How would you add a subtotal per region and product group?* One more `UNION ALL` branch with the right `GROUP BY`.
- *Can a window function give the totals?* Yes, `SUM(...) OVER ()` on the detail rows, but that repeats the total on every row instead of adding a total row.
- *How do you sort so `ALL` is last but alphabetical otherwise?* A `k` or `region = 'ALL'` key as the first `ORDER BY` term (in a compound query it has to be a result column).""",
mistakes="""- Using NULL as the subtotal label and then mixing it with real NULLs.
- Forgetting the sort key, so totals appear in the middle.
- Subtotals that do not add up because of a filter in only one branch.
- `pivot_table(margins=True)` with NaN keys, giving a smaller total than the plain sum.
- Using `UNION` instead of `UNION ALL` and removing equal-looking rows (two regions with the same total).""",
)

F = "`" * 3
P = {}

P[31] = dict(
say="SQL cannot return a column list chosen by the data, because the columns are fixed when the statement is parsed. So I ask the data for the distinct categories, generate the `SUM(CASE WHEN month = ? THEN amount END) AS \"col\"` text in the application, bind the values as parameters, quote the aliases, and add an `other` and a `total` column so the numbers still reconcile.",
schema=f"""{F}sql
CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('North','pen','2024-01',10),('North','pen','2024-02',20),('North','ink','2024-03',5),
 ('North','pen','2024-04',7), ('South','pen','2024-02',30),('South','ink','2024-04',8),
 ('South','ink',NULL,4),      ('South','pen','',6),
 ('East', 'pen','2023-12',9), ('East', 'ink','2024-04',1),
 ('East', 'pen','x''; DROP TABLE sales;--',2);
{F}
The month column deliberately holds a NULL, a blank, an old month and a hostile string.""",
sql="""The generated statement is printed in the Code block output (`sql` and `params` variables). Steps: (1) `SELECT DISTINCT month FROM sales`; (2) keep only values that match the whitelist `^\\d{4}-\\d{2}$` in Python and take the newest three (`MAX_COLS = 3`); (3) build one `SUM(CASE WHEN month = ? THEN amount END) AS "<month>"` per kept month, where the value is a bound parameter and only the alias is spliced in, wrapped by `quote_ident`; (4) add `other` as `SUM(CASE WHEN month IS NULL OR month NOT IN (?,?,?) THEN amount END)` and `SUM(amount) AS total`; (5) `GROUP BY region`.""",
pandas="""`df["bucket"] = df["month"].where(df["month"].isin(months), "other")`, then `pivot_table(index="region", columns="bucket", values="amount", aggfunc="sum")`, `reindex(columns=months + ["other"])`, and `total` from `groupby("region")["amount"].sum()`. pandas has no parse-time column list, so the dynamic part is free: the columns are whatever the data holds.""",
example="""Distinct months seen: 2024-01, 2024-02, 2024-03, 2024-04, NULL, blank, 2023-12 and the hostile string. Five pass the whitelist; the newest three are 2024-02, 2024-03 and 2024-04, so those get their own columns. North: 02 = 20, 03 = 5, 04 = 7, and 2024-01 (10) falls into `other`, total 42. South: 02 = 30, 04 = 8; the NULL-month row (4) and the blank-month row (6) go to `other` = 10, total 48. East: 04 = 1; 2023-12 (9) and the hostile string (2) go to `other` = 11, total 12. Listed columns plus `other` equal `total` on every row (asserted).""",
edge="""- NULL month: `month NOT IN (...)` is UNKNOWN for a NULL month, so without `month IS NULL OR` the NULL row vanishes from `other`. The run shows `other` = 27 with `NOT IN` alone versus 31 with the `IS NULL OR` guard (31 = NULL-month 4 + blank 6 + 2024-01 10 + 2023-12 9 + hostile 2; the NOT IN-only version loses the NULL row's 4). Part 1 Q13 has the NOT IN mechanics; the new point is that the catch-all column silently breaks the reconciliation.
- Blank category: `''` is a real value; here it falls into `other`. Whether blank should be its own 'unknown' column is a business choice; say it out loud.
- A region with no row in a month gets NULL, not 0 (no ELSE 0). A pandas pivot also gives NaN, which is why the numbers print as floats.
- The hostile month never becomes a column because it fails the whitelist, and it is never concatenated into SQL: values go through `?`. Spliced raw as an alias it is a syntax error (the run shows `OperationalError`). Honest note: Python's `execute()` accepts only one statement, so the `DROP TABLE` part would not have run through it anyway; drivers or `executescript` that accept several statements are where this bites (not executed here).
- Column limits: this build allows 2000 columns and 250000 bound parameters (read with `getlimit`; compile-time options, so other builds differ). Other engines have their own limits (not checked here).
- Quoting: bind parameters cannot be used for identifiers, so the alias needs `quote_ident` (double quotes, inner quotes doubled) plus a whitelist; that is the SQLite and standard-SQL convention, other engines use other quote characters (not executed).""",
explain=f"""- **Why SQL cannot do it:** a statement is parsed and planned before any row is read, so the output column names and count must already be known. The result shape cannot depend on the data it is about to read.
- **The standard fix:** two round trips. Query 1 gets the distinct values, the application builds the text, query 2 runs it. Values go in as parameters; identifiers are whitelisted and quoted.
- **`other` and `total`:** `total` is the reconciliation control (`SUM(amount)` for the group). `other` catches everything that did not get a column, so listed columns + `other` = `total` always; if they do not, the generator has a bug.
- **Dialects (not executed here):** SQL Server builds a string with `QUOTENAME` and runs it with `sp_executesql`; PostgreSQL `crosstab` (the `tablefunc` extension) still needs the output column list declared in the query, so the application still has to know the columns; Snowflake documents a `PIVOT` form that takes `ANY` in the value list, and BigQuery pivots with `EXECUTE IMMEDIATE` on a generated string. I am describing these from memory and did not run any of them.
- **When I would not do it in SQL:** return long format (`region, month, amount`) and pivot in the BI tool or pandas. New months then add rows, not columns, nothing breaks, and no SQL text is generated.""",
follow=f"""- *Can you do this in one query?* Not in portable SQL; the column list is fixed at parse time.
- *Why not a stored procedure or a view?* A view has the same fixed column list; it would have to be recreated each month.
- *What if there are 400 months?* Cap the columns, send the rest to `other`, or return long format.""",
mistakes="""- Building the SQL with an f-string around user-controlled values (injection).
- Forgetting that a NULL category breaks `NOT IN`, so the `other` column does not reconcile.
- Using `ELSE 0` everywhere and hiding the difference between 'no sales' and 'zero sales'.
- Hard-coding the month list and forgetting it every month.
- Believing `crosstab` is dynamic.""")

P[32] = dict(
say="SQLite 3.45.1 has no built-in `REGEXP` (the operator calls a `regexp()` function that does not exist), no `SPLIT_PART`, `REVERSE`, `LPAD` or `CHAR_LENGTH`; I register a regexp from Python with `create_function`, or use `GLOB` classes and `LIKE`, and I remember that a Python function exists only in that connection.",
schema=f"""{F}sql
CREATE TABLE codes(code TEXT);
INSERT INTO codes VALUES ('AB-1234'),('ab-1234'),('AB-12x4'),('AB-123'),(NULL),('AB-12345');
{F}
Goal: keep codes shaped like two capital letters, a dash and exactly four digits.""",
sql="""Three versions are in the Code block: `q_re` (`code REGEXP '^[A-Z]{2}-\\d{4}$'`, needs the registered function), `q_glob` (`GLOB '[A-Z][A-Z]-[0-9][0-9][0-9][0-9]'`) and `q_like` (`LIKE '__-____'`, which only knows `_` and `%`).""",
pandas="""`df["code"].str.contains(r"^[A-Z]{2}-\\d{4}$", regex=True)` (the default). The NaN row gives False, not missing, so it drops out of the filter.""",
example="""Six codes. `AB-1234` is the only one with two capitals, a dash and four digits. `ab-1234` fails the capital-letter classes (GLOB and the regex are case-sensitive). `AB-12x4` has a letter in the digit part. `AB-123` is one digit short and `AB-12345` one too long (the regex anchors `^...$`; GLOB has no quantifier, so four `[0-9]` in a row pin the length). NULL gives UNKNOWN. All three methods return `['AB-1234']`. `LIKE '__-____'` only checks the length and the dash, so it also returns `ab-1234` and `AB-12x4`.""",
edge="""- `X REGEXP Y` is rewritten as `regexp(Y, X)`: pattern first, value second. Getting the argument order wrong gives silent nonsense. The Python function must return NULL (None) for NULL input to keep three-valued logic.
- `GLOB` has no `{n}`, `+`, `|` or optional parts; it is Unix-style globbing with `*`, `?`, `[a-z]` and `[^a-z]`. It cannot express 'one or more digits' exactly (the run uses a negated class: `NOT GLOB '*[^0-9A-Z-]*'` finds values made only of allowed characters).
- `LIKE` is ASCII case-insensitive (`'a' LIKE 'A'` is 1, `'Ä' LIKE 'ä'` is 0 in this build); `PRAGMA case_sensitive_like = ON` made `'a' LIKE 'A'` return 0 in the run. GLOB is always case-sensitive.
- The `regexp` function is per connection. A second connection (a BI tool, the `sqlite3` shell) fails with `no such function: REGEXP`. Python-registered functions are not stored in the database file.
- Error text: calling `'a' REGEXP 'a'` without the function fails with `no such function: REGEXP` on this build.""",
explain=f"""- **Confirmed missing here:** `REGEXP`, `SPLIT_PART`, `REVERSE`, `LPAD`, `CHAR_LENGTH`. **Confirmed present:** `concat`, `concat_ws`, `string_agg` (with `ORDER BY` inside), `format`, `printf`, `octet_length`, `unhex`, `iif`, `IS DISTINCT FROM`.
- **NULL rules of the two concatenations (run):** `concat('a',NULL,'b')` gives `ab` and `concat_ws(',','a',NULL,'b')` gives `a,b`: both skip NULL, unlike `||`, which returns NULL.
- **Padding instead of `LPAD`:** `printf('%05d', n)` for numbers, or `substr('0000' || n, -4)` for text.
- **Dialect map, not executed here (from memory, check your version):** PostgreSQL has `~`, `regexp_replace`, `regexp_match` and `substring(... from pattern)`, `split_part`, `string_agg`; MySQL 8 has `REGEXP_LIKE`, `REGEXP_REPLACE`, `REGEXP_SUBSTR` and `CONCAT_WS` that skips NULL arguments; Oracle has `REGEXP_LIKE`, `REGEXP_SUBSTR`, `REGEXP_REPLACE` and `LISTAGG`; Snowflake has `REGEXP_LIKE`, `REGEXP_SUBSTR`, `REGEXP_REPLACE`, `SPLIT_PART`; BigQuery has `REGEXP_CONTAINS`, `REGEXP_EXTRACT`, `REGEXP_REPLACE`, `SPLIT` and `STRING_AGG`. Function names and NULL behaviour differ by engine; I did not run any of them.
- **When to avoid the Python route:** if other clients read the same file, put the cleaning in the application or load an extension.""",
follow=f"""- *Why not use `LIKE` for everything?* No character classes, no quantifiers, and it ignores ASCII case.
- *Is `REGEXP` an operator or a function?* In SQLite it is sugar for calling the user-defined function `regexp`; that is why defining it makes it work.
- *Does `deterministic=True` matter?* It lets SQLite use the function in indexes and expressions that need determinism; the answer is the same here.""",
mistakes="""- Assuming `REGEXP` works because it does in MySQL.
- Swapping the argument order in the Python function.
- Forgetting the function dies with the connection.
- Using `LIKE '[0-9]%'` (brackets are GLOB, not LIKE).
- Expecting `LIKE` to match `Ä` and `ä`.""")

P[33] = dict(
say="SQLite string functions count code points (`LENGTH`) or bytes (`OCTET_LENGTH`) and fold case for ASCII only; `TRIM` strips spaces only unless you give the characters, composed and decomposed accents are different strings, and normalisation belongs in the application; pandas `strip`, `casefold` and `normalize` do the work SQLite cannot.",
schema=f"""The values contain NUL, NBSP and emoji, so they are inserted from Python parameters. The rows (id: content) are:
{F}text
1 'Asha' NBSP(U+00A0) 'Rao'     2 TAB 'Ben' SPACE        3 'Chi' LF 'tra'
4 'Dev' ZWSP(U+200B)           5 'René' (é = U+00E9)     6 'Rene' + U+0301 + 'e' (decomposed é)
7 'Straße'                      8 U+0130 'stanbul'        9 'Zoe ' + emoji U+1F600
10 'a' NUL 'b'
{F}
{F}sql
CREATE TABLE names(id INTEGER PRIMARY KEY, name TEXT);
{F}""",
sql="""`sql_df` query in the Code block (length, octet_length, length of trim, hex), the `scan` recursive CTE that walks each string character by character and keeps suspicious code points (`unicode()` of 160, 9, 10, 8203, 769), and the `clean` query that nests `replace(..., char(160), ' ')`, tab, newline and `char(8203)` removal inside `trim`. Part 9 Q1 has recursion mechanics.""",
pandas="""`s.str.len()`, `s.str.normalize("NFC")`, `s.str.casefold()`, `s.str.strip()` and the clean-up `s.str.replace("\\u200b", "", regex=False).str.replace(r"\\s+", " ", regex=True).str.strip()` (the Code block shows each call).""",
example="""Row 1 'Asha<NBSP>Rao': 8 code points, 9 bytes (NBSP is 2 bytes in UTF-8, hex `C2A0`); `TRIM` changes nothing, so the NBSP stays and a join on 'Asha Rao' with a normal space fails. Row 2 '<TAB>Ben<space>': length 5, after `TRIM` 4: the trailing space went, the leading tab stayed. Row 4: 'Dev' plus U+200B shows length 4 but looks like 3; `hex` ends in `E2808B`. Rows 5 and 6 print identically but have lengths 5 and 6 and are not equal. Row 10: `LENGTH` stops at the NUL (1) while `OCTET_LENGTH` counts all three bytes. After the `replace` chain rows 1 to 4 become 'Asha Rao', 'Ben', 'Chi tra', 'Dev'; pandas gives the same four strings (asserted).""",
edge="""- `TRIM(x, chars)` removes any of the listed characters; `trim(?, char(160, 9, 10, 32))` stripped an NBSP, tab, space and newline run to leave `x`.
- `upper('straße é')` gives `STRAßE é`: only ASCII letters change. `lower('ÀB İ')` gives `Àb İ`. `'é' = 'É' COLLATE NOCASE` is 0 (while `'e' = 'E' COLLATE NOCASE` is 1). So case-insensitive de-duplication of accented names needs the application or an ICU build (this build has none).
- pandas is Unicode-aware and so differs from SQL: `casefold('Straße')` is `strasse`, `upper('ß')` is `SS`, and `lower('İ')` has length 2 (i plus a combining dot). Do not expect pandas and SQL case folding to agree on non-ASCII text.
- `str.len()` agrees with SQL `LENGTH` on every row except the NUL row (SQL 1, Python 3), which the code asserts.
- Emoji and other characters outside the BMP are one code point in SQLite's `LENGTH`; grapheme clusters (a flag, a family emoji) are several. Not run for those.
- `Series.str.title()` on `"o'neil"` gave `O'Neil`, `mcdonald` gave `Mcdonald`: title-casing names is wrong for 'McDonald' and similar; treat it as a display hack.
- SQLite has no `normalize()`; NFC/NFD happens in the application (`unicodedata.normalize` or `str.normalize`).""",
explain=f"""- **Code points versus bytes:** `LENGTH` counts characters (it stops at an embedded NUL for TEXT), `OCTET_LENGTH` counts bytes. `é` is 1 and 2; an emoji is 1 and 4.
- **Finding invisible characters:** `HEX(name)` shows the bytes (`C2A0` is NBSP, `E2808B` is the zero-width space, `CC81` is a combining acute); `UNICODE(substr(name, i, 1))` gives the code point; compare `LENGTH(name)` with the length you can see.
- **TRIM:** by default only the space character. List the others explicitly or use `REPLACE`.
- **Normalisation:** 'é' as one code point and as two are different strings in SQL (`=` is false, lengths 5 and 6). Normalise to NFC on ingestion.
- **pandas:** `str.strip()` removes NBSP, tab and newline (it strips any whitespace); that is a real difference from `TRIM`. It does not remove a zero-width space (a string ending in U+200B kept length 4 after `strip` in the run), so the replace of `\\u200b` is still needed.
- Dialect note: other engines have their own `TRIM`, `LENGTH` and collation rules; not executed here.""",
follow=f"""- *Why can't I just add `COLLATE NOCASE`?* It folds ASCII letters only.
- *Where do I normalise?* At load time, once, in the application (NFC), and store the clean text; then SQL comparisons are exact.
- *How do I find non-ASCII rows?* compare `LENGTH(name)` with `OCTET_LENGTH(name)`: they differ when a multi-byte character is present (an NBSP, an accent or an emoji).""",
mistakes="""- Trusting that `TRIM` removed 'whitespace' that came from a web page or Excel.
- Joining on names with an NBSP and getting no match.
- Believing `LENGTH` is bytes.
- Using `UPPER`/`LOWER` for case-insensitive matching on non-English names.
- Cleaning with a regex in SQL that does not exist in SQLite.""")

P[34] = dict(
say="I normalise spaces first, then read each field with `SUBSTR` and `INSTR` (find the key, read to the next space, or to the end by appending a space), classify every line as ok, null, unreadable or bad user so nothing is dropped silently, and for key=value text I split with a recursive CTE and pivot with `MAX(CASE ...)`.",
schema=f"""{F}sql
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
{F}""",
sql="""`parse_sql` in the Code block (CTEs `norm`, `p1`, `p2`, final SELECT with a `status` CASE), then the counts per level and distinct error users on the temp table `parsed`. For attributes: `kv_sql` (recursive CTE `split` peels one `key=value` piece off the front each step, `kv` cuts at the first `=`) and `wide_sql` (`LEFT JOIN` back to `attrs`, `MAX(CASE WHEN k = 'user' THEN v END)` and so on).""",
pandas="""`raw.str.extract(r"^(?P<ts>...)\\s+(?P<level>[A-Z]+)\\b")`, `raw.str.extract(r"\\buser=(?P<user_txt>\\S*)")` and the same for `action`, then `np.select` for `status`. For key=value: `str.split(";")`, `explode`, `str.split("=", n=1, expand=True)`, then `pivot(index="id", columns="k", values="v")` reindexed to all ids.""",
example="""Line 1 is clean: level ERROR, user 42, action login. Line 3 has no `user=`: `instr` returns 0, so `user_rest` is NULL, the user stays NULL, the line is still 'ok'. Line 4 has runs of spaces; the three `replace('  ',' ')` passes squeeze it back to a single-spaced line, so it parses like line 1. Line 5 is NULL, which becomes 'null line'. Line 7 fails the timestamp `GLOB`, so it is 'unreadable' and has no level. Line 8 has `user=abc`, not digits, so it is 'bad user' (still counted under its level). Counts by level over ok and bad-user lines: ERROR 4 (lines 1, 3, 4, 8), INFO 1, WARN 1. Distinct users with an ERROR line among ok lines: only user 42 (lines 1 and 4) because line 3 has no user and line 8's user is bad. Eight rows in, eight rows out.
For the attributes: line 3's `note=a=b` splits at the first `=` into key `note`, value `a=b`; the trailing `;` leaves an empty piece which is dropped; rows with a NULL or empty text produce no pairs but the `LEFT JOIN` keeps their ids with all-NULL columns.""",
edge="""- Space runs: three `replace('  ',' ')` passes squeeze any run up to 8 spaces; longer runs need more passes (or a recursive collapse). SQLite has no regex replace.
- `instr(x || ' ', ' ')` is the trick for 'read to the next space or to the end': appending a space guarantees a hit.
- A NULL line stays in the result with status 'null line'; `WHERE` on it would silently drop it.
- A missing key gives `instr = 0`; always test it before `substr`, otherwise `substr(s, 0 + 6)` returns garbage from the wrong position.
- The recursive step needs `WHERE rest <> ''` as the stop; a NULL `txt` is excluded in the anchor.
- Values containing `=`: cut at the first `=` only (`instr` finds the first); `str.split("=", n=1)` does the same in pandas.
- Counting a key with the `length(s) - length(replace(s, k, ''))` trick counts non-overlapping hits like pandas `str.count`: both gave 1 for `'aa'` in `'aaa'`; `str.count` is a regex count, so a metacharacter key such as `.` needs escaping.
- pandas `read_sql` shows NULL as NaN; the comparison code fills missing with a marker before `assert_frame_equal`.""",
explain=f"""- **Do not trust one regex-like parse:** always report counts of unreadable and null lines, otherwise quality problems hide as lower totals.
- **`LENGTH`-based tricks:** fine for one key, fragile for many; the recursive CTE gives one row per pair.
- **Recursive CTE shape:** anchor (`txt || ';'`), recursive member (one piece out, rest in), stop when the rest is empty. Part 9 Q1 has the mechanics.
- **Dialects, not executed here:** PostgreSQL could use `regexp_match` or `split_part`/`string_to_table`, MySQL `SUBSTRING_INDEX`, BigQuery `REGEXP_EXTRACT` and `SPLIT`; I did not run any of them.
- **pandas side:** `str.extract` with named groups gives named columns; a missing match gives NaN. The `explode`/`split`/`pivot` chain is the same idea as the CTE.""",
follow=f"""- *How would you handle a user that appears twice in one line?* `MAX` would hide it; use `COUNT` per key to flag it.
- *What about quoted values with spaces?* Not parseable with a space delimiter; use a real parser in the application.
- *Why a LEFT JOIN in the pivot?* So ids with no pairs still appear.""",
mistakes="""- Dropping unparseable lines in a `WHERE` instead of reporting them.
- Using `substr` without checking `instr > 0`.
- Splitting `note=a=b` at the last `=` or with a plain split (pandas `split("=")` without `n=1`).
- Forgetting the trailing delimiter, losing the last pair.
- Counting `COUNT(user)` as lines with users when a bad value is present.""")

P[35] = dict(
say="I build a normalised key (NBSP and tab to space, collapse spaces, trim, lower), group on it to list the ids per duplicate group, keep the smallest id, flag the others instead of deleting, and review groups where other fields disagree before anything is removed; pandas does the same with `casefold`, `strip` and `duplicated`.",
schema=f"""{F}sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT);
-- inserted from Python so the NBSP (U+00A0) in id 3 is exact
-- 1 ('Asha Rao ', 'a@x.com', 'Pune')       2 ('asha  rao', ' a@x.com', 'pune')
-- 3 ('Asha<NBSP>Rao', 'A@X.com', 'Pune ')  4 ('Ben Cruz', 'ben@y.com', 'Delhi')
-- 5 ('Ben Cruz', 'ben2@y.com', 'Mumbai')   6 ('Chitra Nair', 'c@z.com', 'Goa')
-- 7 ('chitra nair', NULL, 'GOA')           8 ('Raj Shah', 'raj1@q.com', 'Pune')
-- 9 ('Raj Shah', 'raj2@q.com', 'Pune')     10 ('Dev Rao', NULL, 'Pune')
{F}""",
sql="""`groups_sql` in the Code block (CTE `k` with `name_key`, `city_key`, `email_key`, then `GROUP BY name_key, city_key HAVING COUNT(*) > 1` with `group_concat(customer_id, ',' ORDER BY customer_id)`, `MIN(customer_id)` as keeper, `COUNT(DISTINCT email_key)` and the NULL-email count) and `flag_sql` (an `UPDATE` that sets `dup_of` to the group's smallest id for every other row).""",
pandas="""`norm()` (replace NBSP, collapse `\\s+`, `strip`, `casefold`), `df.duplicated(subset=[...], keep=False)` to select group members, a `groupby` for sizes and ids, and `sort_values("customer_id").drop_duplicates(subset=[...], keep="first")` for the survivors.""",
example="""Keys: ids 1, 2, 3 all normalise to ('asha rao', 'pune') (trailing space, double space, NBSP and case removed); group size 3, keep 1, one distinct email (`a@x.com` after trim and lower), so these are safe to merge. Ids 6 and 7 become ('chitra nair', 'goa'), keep 6, one email is NULL, so it is probably the same person but check. Ids 8 and 9 are ('raj shah', 'pune') with two different emails: same name and city, different people possibly, so `distinct_emails` = 2 flags them for review. Ben Cruz (4, 5) differs by city and is not a group. Dev Rao (10) is alone. Flagged ids: 2, 3, 7, 9 (point to 1, 1, 6, 8); pandas drops the same four.""",
edge="""- A plain `GROUP BY name, city` finds only 1 duplicate group (ids 8 and 9, the false positive!) and misses the real ones; the normalised key finds 3 groups.
- `lower` is ASCII-only: `lower('RENÉ') = lower('rené')` is 0, so accented duplicates need application-side `casefold` and NFC (see Q33).
- NULL email: `lower(trim(NULL))` is NULL, ignored by `COUNT(DISTINCT)`, so I count NULL emails separately; a NULL is neither a match nor a conflict.
- Whether to key on name + city or on email is a business rule. Email-only keys miss people with two emails; name-only keys merge strangers.
- Ties for the keeper: smallest id is deterministic; 'most complete row' or 'most recent' are other rules that need a window function (Part 3 Q25 covers the delete itself).
- The three `replace('  ',' ')` passes squeeze runs of up to 8 spaces only.""",
explain=f"""- **Normalised key:** every step removes one kind of noise: `char(160)` to space, collapse spaces, `trim`, `lower`.
- **False positives:** two real people can share a name and city. The review rule here is 'different non-NULL emails means look at it by hand'.
- **Flag before delete:** I add `dup_of`, check the counts and a sample, then `DELETE ... WHERE dup_of IS NOT NULL` in a transaction with a backup. Exact duplicates are Part 4 Q10 and the delete mechanics are Part 3 Q25; I do not repeat them.
- **pandas:** `duplicated(keep=False)` marks every member (7 rows here); `drop_duplicates(keep="first")` after sorting by id keeps the smallest id, like `MIN(customer_id)`.
- Dialect note: `lower`/collation rules differ in other engines; not executed here.""",
follow=f"""- *How would you merge, not just delete?* Re-point foreign keys to the keeper first, then delete.
- *What about 'Asha R.'?* That is fuzzy matching (edit distance, phonetics), beyond a normalised key.
- *Should the key be a column?* Yes, a stored normalised column with an index makes the check cheap.""",
mistakes="""- Deleting everything in a group (`HAVING COUNT(*) > 1` is not a delete rule).
- Forgetting NBSP, tab or case and finding nothing.
- Merging two real people with the same name.
- Comparing emails case-sensitively.
- Using `duplicated()` default `keep='first'` when you wanted the whole group listed.""")

P[36] = dict(
say="`COUNT(*) - COUNT(col)` counts only real NULLs, so I generate one SELECT per column from `PRAGMA table_info` that counts NULL, empty, whitespace-only and placeholder text separately and also one 'effectively missing' number, UNION ALL them into one row per column, and check the same audit in pandas.",
schema=f"""{F}sql
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
{F}""",
sql="""`one_col(c)` builds one SELECT for a column (the Code block prints the one for `phone`); the column list comes from `PRAGMA table_info(customers)` and each name is quoted. `audit_sql` joins them with `UNION ALL`. Placeholders are `N/A, NA, NULL, NONE, -` compared as `upper(trim(col))`.""",
pandas="""A loop over columns: `isna().sum()`, `(s == "").sum()`, `((s.str.strip() == "") & (s != "")).sum()`, `s.str.strip().str.upper().isin(PLACEHOLDERS).sum()`, `s.nunique()`, then `pd.DataFrame(rows)` and `melt(id_vars="column_name")` to the long (metric, value) shape.""",
example="""Phone has 8 rows. NULL: row 5 (1). Empty string: row 2 (1). Whitespace-only: row 4, three spaces (1; counted separately from empty because `''` is excluded from that test). Placeholder: row 3, 'N/A' (1). Effectively missing: 1 + 1 + 1 + 1 = 4, so 50.0 per cent missing, while `COUNT(*) - COUNT(phone)` reports only 1. Name: NULL 1 (row 6), whitespace-only 1 (row 5, two spaces), effectively missing 2, so 25.0. signup_date: NULL row 6, empty row 4, 'NULL' text row 3: three problems of three different kinds = 37.5 per cent. Duplicate keys: no repeated `customer_id`; emails repeat after lower and trim (ids 1 and 8, ids 4 and 5), and the text 'n/a' email (row 6) is excluded before grouping.""",
edge="""- `COUNT(DISTINCT col)` skips NULL but counts `''`, `'N/A'` and `'NULL'` as values (phone shows 7 distinct values: four real numbers, the empty string, the three-space string and 'N/A'). Distinct count is therefore not a quality measure on its own.
- Placeholder text is a business list. The word 'NULL' in a column is a string, not a NULL.
- NBSP-only values: `trim(char(160))` still has length 1 (not whitespace for SQL), while pandas `str.strip` turns it into `''`. I kept NBSP out of the sample so both sides agree; with NBSP data the two audits would differ (shown in the output).
- Numeric columns: `trim(customer_id)` converts to text, so the checks run; pandas skips the string tests for numeric dtypes (they are 0).
- `SUM(cond)` is NULL if there are no rows; here there always are rows. Use `TOTAL()` or `COALESCE` for empty tables.
- Rounding: `round(x, 1)` is fine; do not use `printf('%.0f', x)` for whole-number percentages: in this build it truncated (`printf('%.0f', 2.9)` gave `2`, `12.5` gave `12`), while `round()` and `printf('%.0f', round(x))` gave 3 and 13. Python's `'%.0f' % 2.5` gave `2` (half to even) and `3.5` gave `4`.""",
explain=f"""- **Why `COUNT(*) - COUNT(col)` misses blanks:** `COUNT(col)` counts non-NULL values, and `''`, whitespace and `'N/A'` are non-NULL. Part 1 Q4 and Q6 cover the basics.
- **One expression for 'effectively missing':** `col IS NULL OR trim(col) = '' OR upper(trim(col)) IN (...)`. Put the NULL test first; `trim(NULL) = ''` is UNKNOWN, and `TRUE OR UNKNOWN` is TRUE, so the first test settles the NULL case.
- **Percentage:** `100.0 * missing / COUNT(*)`; the `100.0` forces decimal division (integer division would give 0 or 1).
- **Duplicate keys:** `GROUP BY normalised_key HAVING COUNT(*) > 1` after excluding missing values (a NULL key is not a duplicate of another NULL).
- **Preventing it:** a `CHECK (trim(email) <> '')` constraint or a STRICT table with proper types stops new blanks at the door; a NULL still passes a CHECK (UNKNOWN is accepted), so add `NOT NULL` if needed.
- **Automation (concept only):** run the same generated query on a schedule, store the results by date, and alert on a threshold change. Monitoring design belongs to Book 4.
- Dialect note: PostgreSQL, MySQL and others have the same logic with their own catalog views instead of `PRAGMA table_info`; not executed here.""",
follow=f"""- *How do you audit 200 columns?* Generate the SQL in a loop from the catalog, as here.
- *Can you do it in one scan?* Yes, one SELECT with all the SUM expressions; the UNION ALL version scans once per column, which is fine for small tables.
- *What is the difference between NULL and empty for a join key?* Part 2 Q6.""",
mistakes="""- Reporting `COUNT(*) - COUNT(col)` as the missing rate.
- Counting `''` as whitespace-only (or the reverse) and double counting.
- Dividing integers and getting 0 per cent.
- Treating the string 'NULL' as NULL.
- Trusting `TRIM` to catch NBSP.""")

P[37] = dict(
say="These are brain teasers: SQLite has no `REVERSE`, so I rebuild the string one character at a time with a recursive CTE and compare, and for anagrams I split into characters, sort them with `group_concat(c, '' ORDER BY c)` and group on that signature; in pandas it is one line each.",
schema=f"""{F}sql
CREATE TABLE words(word TEXT);
INSERT INTO words VALUES ('madam'),('Level'),('abc'),('A man a plan'),(NULL),(''),
  ('Taco cat'),('listen'),('Silent'),('tinsel'),('cab'),('bca');
{F}""",
sql="""`pal_sql` (CTE `w` normalises with `lower(replace(word,' ',''))`, `rev` prepends one character per step: `substr(norm, i+1, 1) || r`, the last step has `i = length(norm)`) and `anag_sql` (CTE `ch` splits into characters, `sig` builds `group_concat(c, '' ORDER BY c)`, the final query groups by signature). Part 9 Q1 has recursion mechanics.""",
pandas="""`norm = df["word"].str.lower().str.replace(" ", "", regex=False)`; `norm.str[::-1]` reverses; `norm == reversed` tests; `"".join(sorted(w))` builds the signature and `groupby("signature")` groups.""",
example="""'madam' reversed is 'madam': palindrome. 'Level' normalises to 'level' and matches its reverse: palindrome (case ignored). 'Taco cat' becomes 'tacocat': palindrome. 'A man a plan' becomes 'amanaplan', reverse 'nalpanama': not a palindrome. 'abc' is not. '' (empty) reverses to '' so it counts as a palindrome by this rule, and NULL is excluded by `WHERE word IS NOT NULL`. Anagrams: 'abc', 'bca', 'cab' share the sorted signature 'abc'; 'Silent', 'listen', 'tinsel' share 'eilnst' after lower-casing. 'madam' and the others are alone and filtered by `HAVING COUNT(*) > 1`.""",
edge="""- NULL: decide first. Here a NULL word is dropped; an empty string is a palindrome (decide whether the business wants that).
- `DISTINCT` in the CTE `w` matters if the same word appears twice; otherwise the recursion starts the same word twice.
- Case: `lower` is ASCII only, so 'É' will not fold (Q33).
- `group_concat(DISTINCT c, '')` is rejected by SQLite (`DISTINCT aggregates must have exactly one argument`): the run shows it. `group_concat(DISTINCT word)` with one argument works but the separator is fixed to a comma. The ordered form `group_concat(c, '' ORDER BY c)` works in 3.45.1 (the ORDER BY inside the aggregate was added in SQLite 3.44 according to the Wave A sources note; I ran only 3.45.1).
- Output order of `group_concat` without `ORDER BY` is not guaranteed.
- Signature collisions are impossible for sorted characters, but the signature of words with different lengths is different, so only true anagrams match.""",
explain=f"""- **Why recursion:** SQLite has no `REVERSE`, so build it: each step prepends the next character. PostgreSQL, MySQL and SQL Server have a `REVERSE` function (from memory, not executed here), so the real answer there is `norm = REVERSE(norm)`.
- **Why brain teaser:** it is not something you would do in production SQL; interviewers use it to see if you can think recursively, handle NULL and empty input, and know when to leave SQL.
- **What the interviewer is testing:** recursion base and stop condition, normalisation (case and spaces), NULL and empty handling, and the judgement that a two-line pandas or Python answer is better when the data is small.
- **pandas:** `s == s[::-1]` and `''.join(sorted(w))` give the same groups; the code asserts both the palindrome table and the anagram groups match.""",
follow=f"""- *Is the recursion expensive?* One row per character per word; fine for a word list, not for large text.
- *How do you do it without recursion?* Join to a numbers table of positions (Part 9) or use `REVERSE` where it exists.
- *How would you ignore punctuation?* More `replace` calls, or the application.""",
mistakes="""- Forgetting to normalise case and spaces.
- Treating NULL as a palindrome or as an empty string.
- No stop condition in the recursive member.
- Using `group_concat(DISTINCT c, '')` and being surprised by the error.
- Grouping on the unsorted string.""")

P[38] = dict(
say="Transposing in SQL is two steps: unpivot the quarter columns into rows with `CROSS JOIN (VALUES ...)` or `UNION ALL`, then pivot the metric rows into columns with `MAX(CASE ...)`; a fully general transpose is not a SQL operation because the output column list is fixed by the query.",
schema=f"""{F}sql
CREATE TABLE kpis(metric TEXT, q1, q2, q3, q4);   -- no declared types: values keep their own type
INSERT INTO kpis VALUES ('revenue', 100, 120, 130, 150),
                        ('cost',     60,  70, NULL,  90),
                        ('rating',  4.5, 4.0, 4.2, 4.8);
{F}""",
sql="""`unpivot_sql` (`kpis` cross joined to the four quarter names, with a `CASE quarter WHEN 'q1' THEN q1 ...` picking the value), `union_sql` (the `UNION ALL` spelling, asserted to give the same 12 rows) and `transpose_sql` (`GROUP BY quarter` over the long rows with `MAX(CASE WHEN metric = 'revenue' THEN val END)` and so on). SQLite does not accept a column list on a derived table (`AS q(quarter)` is a syntax error here), so the quarter names come from `(SELECT column1 AS quarter FROM (VALUES ...))`.""",
pandas="""`k.set_index("metric").T` and `k.set_index("metric").stack().unstack("metric")`, each followed by `rename_axis(...)` and `reset_index()`. The Code block runs the stack version with warnings turned into errors to show the default `stack()` is the new implementation.""",
example="""Unpivot: each of the 3 metrics times 4 quarters gives 12 rows, e.g. (cost, q3, NULL). Pivot: group by quarter; for q1 the revenue cell is MAX of {100 for revenue rows, NULL for the other metrics} = 100, cost = 60, rating = 4.5. For q3: revenue 130, cost NULL (kept because UNION ALL and CROSS JOIN keep NULL values), rating 4.2. The result is 4 rows by 3 metric columns. `df.T` and `stack().unstack()` give the same table; in the SQL result revenue stays integer while cost and rating arrive as floats in pandas (a NULL or a decimal forces float), and `df.T` makes all three float64 because each original q1 to q4 column mixes integers and decimals.""",
edge="""- Types: one SQL column has one type per cell but SQLite lets a column hold mixed types. When a text metric (`status`) is pivoted next to numbers it works, but `MAX` over a column that mixes numbers and text returns the text (text sorts above numbers: `('ok', 4.5)` in the run). Engines other than SQLite generally need all values of one output column to share a type, so cast to text first (not executed here).
- NULL: `UNION ALL`/`CROSS JOIN` keep NULL rows; SQL Server and Oracle's `UNPIVOT` drop NULLs by default (from memory, not executed here; Oracle has an `INCLUDE NULLS` option, also from memory). Dropping NULLs makes a quarter disappear if every metric is NULL.
- `MAX` is the usual pivot aggregate when there is at most one value per cell; if there can be several, use `SUM` or decide on a rule, otherwise it hides the duplicates.
- A quarter named in no `CASE` branch is lost, which is why the generated column list matters (Q31).
- pandas stack on a larger frame (1000 by 4 with 220 NaN cells): `stack()` default returned 4000 rows (NaN kept, new implementation), `stack(future_stack=False)` returned 3780 and emitted `Pandas4Warning`, `stack().dropna()` also gave 3780, and `stack(dropna=False)` raises `ValueError`. So on pandas 3 the NaN-dropping behaviour must be asked for with `.dropna()`.""",
explain=f"""- **Why two steps:** one operation turns columns into rows, the other rows into columns; SQL has neither as a keyword in SQLite.
- **Why not a general transpose:** the number and names of output columns are fixed when the statement is parsed. A table with an unknown number of metrics needs dynamic SQL (Q31), or you do it in pandas.
- **Dialects (not executed here):** SQL Server and Oracle have `PIVOT` and `UNPIVOT` operators; Snowflake and BigQuery have their own forms; MySQL and SQLite have neither. I did not run any of them.
- **pandas:** `.T` is one call; `stack`/`unstack` is the reshaping vocabulary; both give the same table, asserted after sorting by quarter.
- **Ordering:** `GROUP BY quarter ORDER BY quarter` gives q1 to q4 only because the labels sort that way; do not rely on a pivot's row order without ORDER BY.""",
follow=f"""- *What if the metric list grows?* Generate the CASE list (Q31) or keep long format.
- *Why MAX and not SUM?* Both work for one value per cell; MAX also works for text.
- *Is a `kpis` table with q1..q4 columns a good design?* It is a wide report format; the long table `(metric, quarter, value)` is easier to query.""",
mistakes="""- Pivoting without first checking there is one value per cell.
- Mixing text and numbers in one output column and getting surprising `MAX`/sort results.
- Dropping NULL rows in the unpivot and losing periods.
- Assuming the pivoted rows come out in quarter order without ORDER BY.
- Calling `stack(dropna=False)` on pandas 3.""")

P[39] = dict(
say="In pandas, `astype` is strict (it raises), `to_numeric(errors='coerce')` is lenient (garbage becomes NaN), `read_csv` has its own NA list, dates guess the format from the first value, and categories forbid unknown values; SQLite `CAST` never fails and quietly turns garbage into 0.",
schema=f"""{F}text
amount,amount_clean,pincode,when,status,country
"1,200","1,200",011001,2024-01-05,paid,NA
 45 ,45,110001,05/01/2024,paid,IN
x,7,400001,2024-03-07,refunded,None
1e3,"2,000",560001,not a date,paid,N/A
,,011001,,pending,IN
{F}
The CSV text is built inside the Code block with `io.StringIO`; for SQLite the `amount`, `pincode` and `when` columns are loaded into a `raw` table (and an `aff` table tests affinity).""",
sql="""`CAST(amount AS INTEGER)` and `CAST(amount AS REAL)` on the raw strings; a 'safe cast' that gives NULL for garbage (`CASE WHEN trim(amount) GLOB '[0-9]*' AND trim(amount) NOT GLOB '*[^0-9.]*' THEN CAST(trim(amount) AS REAL) END`); `date(d)` for the dates; and the `aff` and `st` (STRICT) tables for type affinity. SQLite has no `TRY_CAST`.""",
pandas="""`astype(int)`, `pd.to_numeric(..., errors="coerce")` and `downcast="integer"`, `read_csv(thousands=",", dtype={"pincode": str}, keep_default_na=False, na_values=[""])`, `pd.to_datetime(..., errors="coerce")` with `format="mixed"` and `dayfirst=True`, and `astype("category")` with `add_categories`.""",
example="""Amounts '1,200', ' 45 ', 'x', '1e3', blank. `astype(int)` stops at '1,200' (`ValueError: invalid literal for int()`). `to_numeric(coerce)` gives NaN, 45.0, NaN, 1000.0, NaN: the comma value becomes NaN (so remove commas first), the padded ' 45 ' parses, 'x' and the blank are NaN, and '1e3' is accepted. SQLite `CAST(.. AS INTEGER)` gives 1, 45, 0, 1 for the first four: '1,200' stops at the comma and gives 1, 'x' gives 0, and '1e3' as INTEGER gives 1 but as REAL gives 1000.0. Pincode '011001' read as an integer loses the zero (11001); `dtype={"pincode": str}` keeps '011001'; `CAST('011001' AS INTEGER)` gives 11001. Dates: 2024-01-05 and 2024-03-07 parse in ISO form; '05/01/2024', 'not a date' and the blank are NaT with `coerce` (pandas guesses the format from the first value), the same rows that SQLite `date()` returns NULL for (asserted).""",
edge="""- `astype(int)` accepted `' 45 '` (Python's `int()` strips spaces) but failed on `'1e3'`; `astype(float)` accepted `'1e3'` but failed on `''` (`could not convert string to float`).
- `errors="coerce"` hides bad data; check how many NaN you created. `downcast="integer"` gave `int16` for clean integers, and with a missing value the dtype stayed `float64`.
- `thousands=","` worked for `amount_clean` (float64) but the `amount` column, which holds 'x', stays text.
- The default `read_csv` NA list includes `NA`, `N/A`, `NULL`, `None`, `null`, `n/a`, `nan`, `NaN`, `<NA>`, `#N/A`, `#N/A N/A`, `#NA`, `-NaN`, `-nan`, `1.#IND`, `1.#QNAN`, `-1.#IND`, `-1.#QNAN` and the empty string (printed in the output). So the country code `NA` (Namibia) and the text 'None' became NaN; `keep_default_na=False, na_values=[""]` kept them.
- Dates: strict `to_datetime` raised on '05/01/2024' because the format was taken from the first value (`%Y-%m-%d`). `format="mixed"` parsed '05/01/2024' as 2024-05-01 (month first, 1 May). Adding `dayfirst=True` turned it into 2024-01-05 but also flipped the ISO strings: '2024-01-05' became 2024-05-01 and '2024-03-07' became 2024-07-03 (printed in the output). Mixed formats are ambiguous; fix the format at the source.
- SQLite affinity (run): an INTEGER column stores `' 12'` and `'12 '` as the integer 12 (leading and trailing spaces allowed), `'1e3'` as 1000, `'x'` and `'0x10'` stay text; a TEXT column keeps `' 12'` as text and converts the integer 12 to `'12'`; `t = 12` is 0 for the TEXT column holding `' 12'` but `i = 12` is 1 for the INTEGER column. A STRICT table accepted `' 12'` into INTEGER (stored as 12) and rejected `'x'` with `cannot store TEXT value in INTEGER column`.
- Category: assigning 'lost' or `fillna('unknown')` raised `TypeError ... set the categories first`; `add_categories` first works. In this run (pandas 3.0.5) `groupby` on a categorical gave only the observed groups by default; `observed=False` added the empty 'pending' group with 0. Sorting an ordered categorical followed category order (pending, paid, refunded), not alphabetical. `.str.upper()` on a category column worked and returned `object` dtype.""",
explain=f"""- **astype versus to_numeric:** `astype` is a strict cast (error on the first bad value); `to_numeric` is the parsing tool with `errors` and `downcast` options.
- **SQLite CAST:** never raises; it reads the longest numeric prefix and returns 0 if there is none. `'12abc'` is 12 and `''` is 0, which is dangerous because 0 looks like data. A NULL-returning safe cast needs a `CASE` with `GLOB` checks (no `TRY_CAST` in SQLite). Other engines have `TRY_CAST` or `SAFE_CAST` (not executed here).
- **Leading zeros:** codes are labels, not numbers; read them as text.
- **Categories:** compact and ordered, but closed sets; the nulls, new values and empty groups behave differently from plain strings.
- **Comparison:** SQL gives 0 for garbage, pandas coerce gives NaN, SQL safe-cast gives NULL; pandas NaN and SQL NULL then agree.""",
follow=f"""- *Why does `read_csv` read my `NA` country as missing?* Because `NA` is in the default list; switch it off with `keep_default_na=False`.
- *Is `observed` default always True?* I only checked 3.0.5 here (it was observed-only); older versions defaulted differently.
- *How would you validate amounts?* Coerce, count the new NaN, and report them with the original strings.""",
mistakes="""- Casting a pincode to int and losing the zero.
- Using `errors="coerce"` and not counting what was lost.
- Believing `CAST('abc' AS INTEGER)` raises in SQLite.
- Using `dayfirst=True` on mixed ISO and local formats.
- Assigning a new value to a category column without adding the category.""")

P[40] = dict(
say="pandas and SQL disagree on missing values and strings in about ten systematic ways; the translation table in the Code block runs each one on SQLite and pandas and asserts the stated result: NULL = NULL is NULL (not true) but `IS NOT DISTINCT FROM` is true, `NaN == NaN` is False, groupby drops NaN keys, blanks become NaN in `read_csv`, empty sums differ, integers become floats, and `LIKE` is a wildcard pattern while `str.contains` is a case-sensitive regex.",
schema=f"""{F}sql
CREATE TABLE o(region TEXT, amount INTEGER);
INSERT INTO o VALUES ('N',1),('N',2),(NULL,5),(NULL,NULL),('S',NULL);
CREATE TABLE w(s TEXT);
INSERT INTO w VALUES ('Apple'),('apple pie'),('a.b'),('axb'),('100%'),('1000'),('Ärger'),(NULL);
CREATE TABLE v(x INTEGER);   INSERT INTO v VALUES (3),(NULL),(1);
CREATE TABLE c(name TEXT, city TEXT);   -- Asha has a blank city: the CSV text is 'name,city' / 'Asha,' / 'Ben,Pune'
{F}""",
sql="""Each translation row is a one-line SQL query in the Code block (the left column of the printed table).""",
pandas="""Each row has its pandas counterpart in the right column; the `row()` helper asserts both against the stated pair before adding it to the table.""",
example="""Row 1: `NULL = NULL` returns NULL (no row would match), while `NaN == NaN` is False; `NULL IS NOT DISTINCT FROM NULL` is 1 and the pandas null-safe version is `a.eq(b) | (a.isna() & b.isna())`; `Series.equals` treats NaNs in the same place as equal, a whole-object test with no SQL counterpart. With the nullable `Int64`/`string` dtypes `pd.NA == pd.NA` is `<NA>`, like SQL. Row 2: `GROUP BY region` over N, N, NULL, NULL, S gives 3 groups; `groupby("region")` gives 2 and `dropna=False` gives 3. Row 3: the blank CSV city is `''` in SQLite, NaN in pandas (`keep_default_na=False` keeps `''`), and `COUNT(city)` is 2 while `count()` is 1. Row 4: `SUM` of an all-NULL group is NULL; pandas `sum()` is 0.0 and `sum(min_count=1)` is NaN. Row 5: an INTEGER column with a NULL has typeof integer and null; pandas gives `float64`, or `Int64` with the nullable dtype. Row 6: `LIKE '%APPLE%'` matches 'Apple' and 'apple pie'; `contains('APPLE')` matches nothing; `case=False` fixes it; for 'Ärger' SQL `LIKE` does not fold (0) but pandas does (True). Row 7: `LIKE 'a.b'` matches only 'a.b' but regex `a.b` also matches 'axb'; `LIKE '100%'` matches '100%' and '1000' (percent is a wildcard) but `contains('100%')` matches only the literal; `LIKE 'a%'` also matches 'Apple' (case-insensitive) but `startswith('a')` does not. Row 8: ascending, NULL sorts first in SQLite and NaN last in pandas; `NULLS LAST` aligns them.""",
edge="""- The NULL row in `LIKE` and in `str.contains`: SQL gives NULL (row not returned either way), pandas 3.0.5's default `str` dtype gives False for the missing value. With `dtype="string"` it would give `<NA>` (checked in Wave A, not part of this run).
- Part 1 Q16 already covers rows 2, 4 and the sort position (and `COUNT` versus `count`); what is new here is the comparison semantics (row 1), the CSV blank (row 3), integer-to-float (row 5) and the string matching rows (6 and 7). They are repeated in one line only so every row of the table has a run.
- `IS NOT DISTINCT FROM` ran on SQLite 3.45.1; older versions and some engines lack it (MySQL uses `<=>`, from memory, not executed here).
- `bool(pd.NA)` raises `TypeError` (Wave A check); filters with `pd.NA` need `.fillna(False)` first.
- A pattern with `_` also matches any single character in `LIKE`: `LIKE 'a_b'` would match 'a.b' and 'axb'. Use `ESCAPE` for a literal.""",
explain=f"""- **Equality:** SQL uses three-valued logic (a comparison with NULL is UNKNOWN); NaN is an ordinary float that happens to be unequal to itself; `pd.NA` is closer to SQL NULL.
- **Missing keys:** pandas drops them from groups by default; SQL keeps one NULL group.
- **Empty versus missing:** SQL stores `''` and NULL differently; `read_csv` merges blank and many placeholders into NaN.
- **Sums and dtypes:** an empty sum is NULL in SQL and 0 in pandas; NaN forces floats unless a nullable dtype is used.
- **Strings:** `LIKE` has two wildcards, is case-insensitive for ASCII (SQLite) and anchored; `str.contains` is a regex that searches anywhere and is case-sensitive; use `regex=False` or `re.escape` for literals.
- **Sorting:** SQLite sorts NULL as the smallest value; pandas puts NaN last. Both can be changed (`NULLS LAST`, `na_position`).
- Dialect note: other SQL engines differ on `LIKE` case sensitivity and NULL ordering (not executed here).""",
follow=f"""- *How do I make pandas behave like SQL?* `dropna=False`, `min_count=1`, nullable dtypes, `keep_default_na=False`, explicit `na_position`.
- *Which side is right?* Neither; they have different models, so state the rule you want and test it.
- *Is `==` in pandas ever NULL-like?* With `pd.NA` (nullable dtypes), yes.""",
mistakes="""- Writing `WHERE col = NULL` or `df[df.col == np.nan]`.
- Expecting `str.contains` to be case-insensitive or literal.
- Treating `LIKE 'a.b'` as a regex.
- Forgetting a blank CSV field becomes NaN.
- Comparing SQL and pandas results without aligning missing values and sort order.""")

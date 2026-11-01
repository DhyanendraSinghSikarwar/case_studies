P2 = {}
P2[8] = '''**Say this first (1 line):** Filter out NULL salaries, compute `DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC)` in a CTE, keep `rnk <= 3`, and join to `departments`; `DENSE_RANK` counts distinct salary levels, so ties are all included and a department can return more than three people.

**Schema and sample data:** IT has levels 90, 85 (three people tied), 69 and 60; Sales has two salaries plus a NULL; HR has no employees.
{{SCHEMA}}

**SQL answer:**
{{SQL:SQL_MAIN}}
The Code block also builds `RANK` and `ROW_NUMBER` variants of the same filter by string substitution, to compare counts.

**pandas answer:** dense rank within each department, descending, then filter and merge.
{{PD:main}}

**Example:**
- IT salary levels descending: 90 (Max), 85 (Joe, Randy, Will), 69 (Janet), 60 (Ravi). Top three levels are 90, 85, 69, so five people: Max, Joe, Randy, Will, Janet. Ravi (level 4) is out.
- Sales: levels 80 and 60 only, so both Henry and Sam are returned (fewer than three levels means everyone is included).
- HR: no employees, no rows.
- Compare: `RANK <= 3` gives IT ranks 1, 2, 2, 2, 5: Max, Joe, Randy, Will and not Janet (6 rows overall). `ROW_NUMBER <= 3` gives only three IT people (5 rows overall). Only `DENSE_RANK` returns the five who hold one of the top three salary levels.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- NULL salary (Tia in Sales): without `WHERE salary IS NOT NULL` SQLite ranks NULL as the smallest value, so in a department with fewer than three levels it gets a rank and is returned with a NULL salary (output line "without the IS NOT NULL filter" shows Tia). pandas `rank` gives NaN and `NaN <= 3` is False, so pandas would drop her. A real SQL/pandas difference; the filter makes them agree.
- Department with fewer than three salary levels: all employees returned.
- Department with no employees: not in the output (inner join).
- Ties: all tied employees stay, so more than three rows per department is correct here.

**Then explain:**
- "Top three salaries" here means top three distinct amounts, so rank levels: `DENSE_RANK`. `RANK` skips (1, 2, 2, 2, 5) and would cut Janet; `ROW_NUMBER` would pick arbitrary people among the 85 tie.
- The window cannot sit in `WHERE`, hence the CTE (Q3).
- pandas `rank(method="dense", ascending=False)` does the same inside `groupby`; it returns floats.
- I know the LeetCode 185 wording only from snippets; the definition I used is the one stated in the question.

**Follow-ups:**
- *Exactly three people per department?* `ROW_NUMBER` with a tie-breaker (Q4).
- *Include departments with no employees?* `LEFT JOIN` from `departments`; the NULL employee row would need a decision.
- *Why not `LIMIT`?* `LIMIT` applies to the whole result, not per group.

**Common mistakes:**
- Using `RANK` or `ROW_NUMBER` for "top three salaries".
- Forgetting to filter NULL salaries and returning a NULL earner.
- Joining the departments table first and ranking after (fine for results, but a join fan-out can change ranks, Q48).
'''
P2[9] = '''**Say this first (1 line):** Number each customer's rows with `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC, update_id DESC)` and keep `rn = 1`; the `update_id` tie-breaker makes the winner among rows sharing `updated_at` a fixed rule, and flipping the order direction (ASC) keeps the first row instead.

**Schema and sample data:** nine update rows for five customers. Customer 1 has two rows on the same date (update 2 and 3); customer 4 has a NULL date row and a dated row; customer 5 has only a NULL date.
```sql
CREATE TABLE customer_updates(update_id INTEGER PRIMARY KEY, customer_id INTEGER, email TEXT, updated_at TEXT);
INSERT INTO customer_updates VALUES
 (1,1,'a@x.com','2026-01-01'),(2,1,'a2@x.com','2026-02-01'),(3,1,'a3@x.com','2026-02-01'),
 (4,2,'b@x.com','2026-01-15'),(5,3,'c@x.com','2026-03-05'),(6,3,'c0@x.com','2026-01-01'),
 (7,4,'d@x.com',NULL),(8,4,'d2@x.com','2026-01-10'),(9,5,'e@x.com',NULL);
```

**SQL answer:** tie rule: later `update_id` wins. `SQL_FIRST` flips both keys to ASC for "keep the first row". `SQL_NOTIE` drops the tie-breaker.
{{SQL:SQL_MAIN}}
{{SQL:SQL_FIRST}}
{{SQL:SQL_NOTIE}}

**pandas answer:** sort by the same keys, then keep the first row per customer.
{{PD:main}}
{{PD:first}}

**Example:**
- Customer 1: updates 2 and 3 share 2026-02-01, the latest date. `update_id DESC` puts 3 first, so update 3 (a3@x.com) wins. Update 1 is older.
- Customer 2 has one row, kept. Customer 3: 2026-03-05 beats 2026-01-01, so update 5.
- Customer 4: NULL date sorts last in a DESC order (in SQLite and in pandas), so the dated update 8 wins.
- Customer 5 only has a NULL-date row, so that row is still returned (update 9).
- Keep-first (ASC): customer 1 gives update 1, customer 3 gives update 6.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- Ties without the tie-breaker: customer 1's pick is left to the engine. On SQLite 3.45 it returned update 2 in both runs (even with the input rows inserted in reverse, because `update_id` is the rowid and the scan follows it), so it looks repeatable here, but that is an implementation side effect, not a promise. Other engines were not executed.
- NULL dates: keep-latest agrees between SQL and pandas (NULL/NaN last). Keep-first does not: SQLite sorts NULL smallest, so ASC puts NULL first and picks update 7 for customer 4, while `sort_values` defaults to `na_position="last"` and picks update 8. The output shows customer 4 as the one disagreement; fix with `na_position="first"` or by filtering NULL dates. NULL ordering defaults in PostgreSQL and MySQL differ from SQLite (not executed here).
- Dates must sort correctly as text: ISO `YYYY-MM-DD` does.
- Customer with a single row: kept.

**Then explain:**
- `ROW_NUMBER` is the right tool because it gives exactly one winner per customer. `RANK` would keep both tied rows.
- Repeatable results need a total order inside the window: `updated_at DESC, update_id DESC`. Rows that differ in no ordering column get an arbitrary order.
- Keep first: reverse the directions (or use ASC on both keys).
- pandas: `drop_duplicates(subset=..., keep="first")` keeps the first row it sees, so sort first. Sorting both columns descending reproduces the SQL rule.
- Deleting the losers instead of selecting the winner is Q35.

**Follow-ups:**
- *Is `GROUP BY customer_id, MAX(updated_at)` enough?* It loses the other columns and returns both tied rows when joined back; the window version returns one.
- *Several columns define "latest"?* Add keys to the ORDER BY (Q44).
- *Performance?* An index on `(customer_id, updated_at)` can help; deeper tuning is Q40 and Part 11.

**Common mistakes:**
- Omitting the tie-breaker and trusting the result.
- Sorting ascending in pandas and keeping `first`.
- Assuming NULLs sort the same way in every tool (see the keep-first difference).
'''
P2[10] = '''**Say this first (1 line):** `COUNT(*) OVER (PARTITION BY email)` gives every row the size of its email group, so `> 1` lists all copies; the `GROUP BY email HAVING COUNT(*) > 1` version needs a join back to the rows, and `ROW_NUMBER() = 1` marks the first copy, so `rn > 1` marks the extra ones; NULL emails form one group in both.

**Schema and sample data:** eight users. a@x.com appears three times, two users have a NULL email, and 'A@x.com' differs only by case.
{{SCHEMA}}

**SQL answer:** first copy = lowest `user_id`.
{{SQL:SQL_MAIN}}
{{SQL:SQL_GROUP}}

**pandas answer:**
{{PD:main}}

**Example:**
- a@x.com: users 1, 3, 7 give copies = 3 and rn = 1, 2, 3, so user 1 is the first copy and users 3 and 7 are extras.
- NULL: users 4 and 5 are one partition (PARTITION BY puts NULLs together), copies = 2, so user 4 is first and 5 is an extra.
- b@x.com, c@x.com: one row each, not listed. 'A@x.com' (user 8) is a different string in SQLite (default binary comparison) and in pandas, so not a duplicate.
- Result: users 1, 3, 4, 5, 7.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- NULL emails are grouped together by `PARTITION BY`, `GROUP BY` and by pandas `duplicated` (NaN/None counted equal). Whether two NULL emails are "the same person" is a business decision; exclude them with `WHERE email IS NOT NULL` if not.
- The GROUP BY version joined with `=` loses the NULL group (`NULL = NULL` is not true; output shows [1, 3, 7]); I joined with `IS`, which is NULL-safe in SQLite (PostgreSQL uses `IS NOT DISTINCT FROM`, MySQL `<=>`; not executed).
- `COUNT(email)` instead of `COUNT(*)` counts non-NULL values, so the NULL group counts 0 and drops out ([1, 3, 7]): a quiet difference.
- Case and whitespace: 'A@x.com' is not matched here; a case-insensitive rule needs `LOWER(email)` (and in pandas `str.lower()`). Some engines compare text case-insensitively by default (MySQL collations, from memory, not executed).

**Then explain:**
- Window version: one pass, keeps the row detail, gives you the count and the first-copy flag together. GROUP BY version: shows only the duplicated values unless you join back.
- `ROW_NUMBER = 1` marks the keeper; `rn > 1` marks what you would delete (Q35). The order inside OVER decides which copy is "first", so give it a unique key (`user_id`).
- pandas: `duplicated(subset="email", keep=False)` marks all copies; `keep="first"` marks only the later ones, which is the `rn > 1` set.

**Follow-ups:**
- *Count the duplicate groups?* `COUNT(DISTINCT email)` over the filtered rows, or `GROUP BY ... HAVING` then count.
- *Remove the duplicates?* Keep `rn = 1` or delete `rn > 1` (Q35).
- *Duplicates across several columns?* Partition by all of them.

**Common mistakes:**
- Using `=` to join back and silently losing NULL groups.
- Using `COUNT(email)` and not flagging NULL duplicates.
- Not saying which copy is kept.
'''
P2[11] = '''**Say this first (1 line):** `RANK() <= 3` returns four rows when several employees tie for the last qualifying place, because tied rows share a rank; `ROW_NUMBER() <= 3` returns exactly three but drops one of the tied employees arbitrarily; pick the behaviour the business wants, and fix the first with `ROW_NUMBER` plus a stated tie rule, the second with `RANK` (or `DENSE_RANK`).

**Schema and sample data:** department 10 has Ben at 90 and three people tied at 70; department 20 has four distinct salaries.
{{SCHEMA}}

**SQL answer:** tie rule for the exactly-N version: lower `emp_id` first.
{{SQL:SQL_RANK}}
{{SQL:SQL_ROWNUM}}

**pandas answer:** `rank(method="min")` reproduces RANK; sort plus `head(3)` reproduces ROW_NUMBER.
{{PD:main}}

**Example:**
- Department 10: salaries 90, 70, 70, 70. `RANK` gives 1, 2, 2, 2, so all four are `<= 3`: four rows. That is the report "more than N".
- `ROW_NUMBER` with `emp_id` as tie-break gives Ben 1, Asha 2, Chitra 3, Dev 4: Dev is dropped although he earns the same as Asha and Chitra. That is the report "someone is missing".
- Department 20: 90, 80, 70, 60 are all distinct, so both give three rows (Hari at 60 is out).

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- If the tie-break were missing, which tied employee `ROW_NUMBER` drops would be engine-dependent; I did not rely on that, and the query above has `emp_id` in the ORDER BY.
- The number of rows per department with RANK is 3 or more; it is never fewer than N when N rows exist.
- A department with fewer than N people returns them all in both.
- NULL salaries rank last in DESC in SQLite; filter them if they should not appear (Q4 shows a NULL taking a slot).

**Then explain:**
- Both behaviours are "correct" for their function: `RANK` treats equal salaries as equal, so it cannot cut between them; `ROW_NUMBER` forces distinct numbers, so it must cut.
- Decide with the business: "everyone who is in the top 3 by salary" (ties included, use `RANK`) versus "exactly three people" (use `ROW_NUMBER` and agree the tie rule, such as earlier hire date or lower id).
- If they want three salary levels, use `DENSE_RANK` (Q8).
- pandas: `rank(method="min") <= 3` matches the RANK rows; `head(3)` after sorting matches ROW_NUMBER.

**Follow-ups:**
- *How do I stop the extra rows without losing fairness?* Say so out loud and add the agreed tie-break columns.
- *How do I check the count?* count rows per department in the result, as the "rows per dept" line does.
- *What does the interviewer want?* I would ask which rule applies before coding.

**Common mistakes:**
- Using `RANK` when exactly N is required, or `ROW_NUMBER` when ties should be kept.
- Adding a tie-breaker to `RANK` (it turns it into ROW_NUMBER, since ties disappear).
- Not telling the stakeholder that the cutoff rule exists.
'''
P2[12] = '''**Say this first (1 line):** Rank with `ROW_NUMBER() OVER (ORDER BY score DESC, last_updated, player_id)` so no two rows tie in the ORDER BY; with only `score DESC` the order of tied rows is left to the engine, so positions can change between runs or engines.

**Schema and sample data:** six players; three tie at 90 (Ben and Chitra even share the same date) and two tie at 80.
```sql
CREATE TABLE players(player_id INTEGER PRIMARY KEY, name TEXT, score INTEGER, last_updated TEXT);
INSERT INTO players VALUES (1,'Asha',90,'2026-03-01'),(2,'Ben',90,'2026-02-01'),(3,'Chitra',90,'2026-02-01'),
 (4,'Dev',80,'2026-01-20'),(5,'Esha',80,'2026-01-05'),(6,'Farid',100,'2026-04-01');
```

**SQL answer:** rule: higher score first, then earlier `last_updated`, then lower `player_id`.
{{SQL:SQL_MAIN}}
{{SQL:SQL_PARTIAL}}
{{SQL:SQL_RANK}}

**pandas answer:** sort with a list of columns and number the rows, or pre-sort by the tie-breakers and use `rank(method="first")`.
{{PD:main}}
{{PD:rank}}

**Example:**
- Farid 100 is first.
- Three players at 90: Ben and Chitra (2026-02-01) come before Asha (2026-03-01) because earlier date wins; Ben and Chitra tie on date, so `player_id` puts Ben (2) before Chitra (3). Positions: Farid 1, Ben 2, Chitra 3, Asha 4.
- Two at 80: Esha (2026-01-05) before Dev (2026-01-20), positions 5 and 6.
- Score only: SQLite numbered the tied rows in row order: by player id the positions were [2, 3, 4, 5, 6, 1], so Asha got 2 (full rule: 4) and Dev got 5 (full rule: 6). It looks stable, but it just reflects scan order.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- Honest result: on SQLite 3.45 the score-only query gave the same positions when I inserted the rows in reverse, so I could not make it flip. The standard does not promise that, and an index, a parallel plan or another engine can change it; other engines were not executed.
- If the product requirement is shared positions for equal scores, use `RANK` on score only: output `[2, 2, 2, 5, 5, 1]`.
- NULL scores: they rank last in DESC in SQLite; pandas `sort_values` puts NaN last too (not in this data).
- Ties in all three columns are impossible here because `player_id` is unique; that is what makes the order total.

**Then explain:**
- An ORDER BY is deterministic only if it is a total order. Add a unique column last (`player_id`).
- `ROW_NUMBER` over a tied order must still give different numbers, so the engine picks; a different plan or data layout can pick differently.
- Choose tie-breakers that mean something to users (earlier achievement wins), then the unique id as the last resort.
- pandas: `sort_values(["score","last_updated","player_id"], ascending=[False, True, True])` gives the order; `rank(method="first")` follows row order among ties, so pre-sort by the tie-breakers.

**Follow-ups:**
- *Shared positions with a gap?* `RANK` on score only.
- *Is the outer `ORDER BY position` needed?* Yes; ordering inside `OVER` does not order the result (Q37).
- *Do I need an index?* Not for correctness.

**Common mistakes:**
- Calling a leaderboard deterministic because it gave the same output twice.
- Using `RANK` and expecting no ties.
- Using `rank(method="first")` in pandas on an unsorted frame.
'''
P2[13] = '''**Say this first (1 line):** In SQL you can write `GROUP BY region, product` and `RANK() OVER (PARTITION BY region ORDER BY SUM(amount) DESC)` in the same SELECT, because the grouping happens first and the window then runs over the grouped rows; a window function cannot go inside an aggregate, and a CTE that aggregates first is the clearer alternative.

**Schema and sample data:** nine sales rows. North has a tie (B and C at 120); East has a product whose only sale has a NULL amount.
{{SCHEMA}}

**SQL answer:**
{{SQL:SQL_MAIN}}
The CTE alternative (same rows):
{{SQL:SQL_CTE}}

**pandas answer:** `groupby` sum, then `groupby("region")` rank. `min_count=1` makes an all-NaN sum NaN, as in SQL.
{{PD:main}}

**Example:**
- North: A = 100 + 50 = 150, B = 120, C = 120, D = 30. `RANK` gives A 1, B 2, C 2, D 4 (tie shares 2, the next is 4).
- South: A 200 rank 1, B 80 rank 2.
- East: C 40 rank 1; X's only amount is NULL, so `SUM` is NULL, which sorts last in DESC and gets rank 2.
- Output is ordered by region, rank, product so the tie between B and C is shown in a fixed order.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- NULL total: SQL `SUM` of only NULLs is NULL (and still gets a rank, last). pandas `.sum()` returns 0.0 for an all-NaN group (output line), which gives X a 0.0 total instead of NULL (same rank 2 here, wrong number); I used `min_count=1` plus `na_option="bottom"` to match.
- Ties: shared rank with `RANK`; use `ROW_NUMBER` with a tie-breaker for unique positions.
- A region with one product: rank 1.
- Nesting error: `SUM(RANK() OVER (...))` fails with `misuse of window function RANK()` in SQLite 3.45 (output). Message wording on other engines was not executed.

**Then explain:**
- Order of evaluation: `FROM`, `WHERE`, `GROUP BY`, `HAVING`, then window functions (which see one row per group), then `SELECT` list, `ORDER BY`. That is why `SUM(amount)` is allowed inside the window's ORDER BY: it is already computed.
- A window function can use aggregate results, but an aggregate cannot contain a window function, since windows run after aggregates.
- CTE form: aggregate in the CTE, rank in the next step; clearer, and the only way to filter on the rank (`WHERE rnk <= 2`), because windows are not allowed in `WHERE` (Q3).
- pandas: two steps, `groupby([...]).sum()` then `groupby("region").rank(...)`.

**Follow-ups:**
- *Top product per region?* Filter `rnk = 1` in an outer query (ties kept) or `ROW_NUMBER` for one.
- *Rank across all regions instead?* Drop `PARTITION BY`.
- *Why not rank before grouping?* You would rank individual sales, not product totals (Q48 shows how the wrong grain misleads).

**Common mistakes:**
- Putting the window function inside `SUM` or trying to filter on the alias in the same SELECT.
- Forgetting that the window sees grouped rows, not the original sales rows.
- Using `.sum()` in pandas and ranking an all-NaN group as 0.
'''

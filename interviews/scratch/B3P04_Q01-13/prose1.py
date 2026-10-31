# prose templates Q1-Q7 (markers: {{SCHEMA}} {{SQL:NAME}} {{PD:name}} {{CODE}} {{OUT}})
P = {}
P[1] = '''**Say this first (1 line):** A window function computes a value over a set of related rows but keeps every input row; `GROUP BY` collapses each group to one row, so `AVG(salary) OVER (PARTITION BY dept_id)` gives each employee the department average next to their own salary, while `GROUP BY dept_id` gives one row per department.

**Schema and sample data:** seven employees, one NULL salary (Gita), and a department (30) with one person.
{{SCHEMA}}

**SQL answer:** `SQL_WINDOW` keeps all rows, `SQL_GROUP` collapses, `SQL_ORDERED` shows `OVER ()` and an `ORDER BY` inside `OVER` (all in the Code block).
{{SQL:SQL_WINDOW}}
{{SQL:SQL_GROUP}}
{{SQL:SQL_ORDERED}}

**pandas answer:** `transform("mean")` is the window version (one value per original row); `groupby().agg()` is the GROUP BY version.
{{PD:window}}
{{PD:group}}

**Example:** averages ignore NULL.
- Dept 10: (50 + 70 + 60) / 3 = 60, so Asha, Ben and Chitra all show 60.
- Dept 20: Dev 90, Esha 40, Gita NULL, so (90 + 40) / 2 = 65 (NULL is skipped); all three rows show 65.
- Dept 30: Farid alone, 55.
- `OVER ()` has no PARTITION BY, so the whole table is one partition: (50+70+60+90+40+55) / 6 = 60.83 on every row.
- With `ORDER BY emp_id` inside `OVER`, the average becomes "so far": dept 10 shows 50, then (50+70)/2 = 60, then 60; dept 20 shows 90, then 65, then 65 (Gita's NULL adds nothing). That is a running value, which is Part 5 territory; here it only shows that ORDER BY inside OVER changes what the function sees.
- GROUP BY returns 3 rows for 7 input rows; the window query returns 7.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- NULL salary: skipped by `AVG` in both forms (Gita still gets a department average of 65, her own salary stays NULL / NaN).
- NULL `dept_id` (none in this data): `PARTITION BY` and `GROUP BY` both put all NULLs in one group. In pandas, `groupby` drops NaN keys by default, so `transform` would give NaN for those rows (the Part 3 Q5 answer shows this); pass `dropna=False` to keep them.
- A one-row partition: the average is the row itself (Farid, 55).
- Empty table: the window query returns no rows, and so does GROUP BY (no groups).

**Then explain:**
- `OVER (...)` is what turns an aggregate into a window function. `PARTITION BY` splits rows into groups for the calculation only; no PARTITION BY means one partition holding every row.
- `ORDER BY` inside `OVER` orders rows within the partition, and for aggregates it also shrinks the frame (default frame: start of partition up to the current row and its ties). I only show the idea; running totals are Part 5.
- Use a window when you need row detail next to a group number (above-average earners, share of total). Use GROUP BY when you want the summary only.
- Window functions run after `WHERE`, `GROUP BY` and `HAVING`, so they see the rows that survived those steps.
- pandas mapping: window = `groupby(...).transform(...)` (same length as the frame, same index); GROUP BY = `groupby(...).agg(...)` (one row per group).

**Follow-ups:**
- *Can I get both in one query?* Yes: `GROUP BY` first, then a window over the grouped rows (Q13 does this).
- *Can I filter on the window value?* Not in `WHERE`; wrap it in a CTE or subquery (Q3).
- *Is the window slower?* It needs the rows grouped and, if ordered, sorted; I did not time it (Q40 looks at the plan).

**Common mistakes:**
- Expecting `OVER` to reduce rows.
- Forgetting `PARTITION BY` and getting the company-wide average on every row.
- Adding `ORDER BY` inside `OVER` for an average and getting a running average by accident.
- In pandas, using `groupby().mean()` where `transform("mean")` is needed, which gives a different length.
'''
P[2] = '''**Say this first (1 line):** On scores 100, 100, 90, 80, `ROW_NUMBER` gives 1,2,3,4 (always unique), `RANK` gives 1,1,3,4 (ties share a number and the next number skips), and `DENSE_RANK` gives 1,1,2,3 (ties share a number and nothing is skipped).

**Schema and sample data:**
{{SCHEMA}}

**SQL answer:** `SQL_MAIN` shows the three side by side. For `ROW_NUMBER` I add `player_id` as a stated tie-breaker (lower player_id first) so the result is deterministic. `SQL_NOTIE` is the same function with `ORDER BY score DESC` only.
{{SQL:SQL_MAIN}}
{{SQL:SQL_NOTIE}}

**pandas answer:** `rank(method=..., ascending=False)` with `first`, `min` and `dense`; rank returns floats, so I cast to int (there are no NaN here).
{{PD:main}}

**Example:**

| player | score | ROW_NUMBER | RANK | DENSE_RANK |
|---|---|---|---|---|
| 1 | 100 | 1 | 1 | 1 |
| 2 | 100 | 2 | 1 | 1 |
| 3 | 90 | 3 | 3 | 2 |
| 4 | 80 | 4 | 4 | 3 |

- Players 1 and 2 are tied on score, so `RANK` and `DENSE_RANK` give both 1.
- `RANK` then skips to 3 because two rows already sit above player 3 (rank = 1 + number of rows strictly ahead). `DENSE_RANK` gives 2 (it counts distinct score levels).
- `ROW_NUMBER` just numbers the sorted rows; with the `player_id` tie-break player 1 gets 1 and player 2 gets 2.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- Ties: the only function that must break them is `ROW_NUMBER`. Without a tie-breaker the standard promises only that the tied rows get 1 and 2 in some order. In my SQLite 3.45 run the unbroken query gave player 1 the 1 (the same as the stated tie-break), but that is the engine's scan order showing through, not a guarantee; other engines were not executed.
- pandas `method="first"` breaks ties by row order in the frame, not by any column. On the same data reversed, player 2 got 1 and player 1 got 2 (see output). So sort first if you need a rule.
- NULL scores: SQL ranks them (NULL is smallest in SQLite, so last in DESC); pandas `rank` leaves NaN as NaN by default (`na_option="keep"`). No NULLs in this data; Q29 and Q30 cover it.
- A table with one row: all three give 1.

**Then explain:**
- `RANK` has gaps after ties; `DENSE_RANK` never has gaps; `ROW_NUMBER` never has ties.
- Use `ROW_NUMBER` when you need exactly one row per rank (dedup, pagination), `RANK` for competition-style positions, `DENSE_RANK` for "top N levels".
- pandas map: `first` = ROW_NUMBER (on a pre-sorted frame), `min` = RANK, `dense` = DENSE_RANK. `method="min"` gives the lowest position of the tied group, which is what RANK does.
- `ascending=False` is needed because SQL used `ORDER BY score DESC`; pandas ranks smallest first by default.

**Follow-ups:**
- *Which one is arbitrary on ties and why?* `ROW_NUMBER`: it must give distinct numbers to rows that compare equal, so the engine picks an order unless you supply more `ORDER BY` columns.
- *What do the numbers look like for 100, 100, 100?* 1,2,3 / 1,1,1 / 1,1,1.
- *What is `method="max"`?* The highest position of the tie; it has no direct built-in SQL twin (Q42 relates it to `CUME_DIST`).

**Common mistakes:**
- Believing `ROW_NUMBER` is "the same as RANK but without ties" and trusting which tied row got 1.
- Forgetting `ascending=False` in pandas and ranking the lowest score first.
- Reading `RANK = 2` as "second place" when two rows tie for first (no row has rank 2).
'''
P[3] = '''**Say this first (1 line):** A window function cannot be in `WHERE` because `WHERE` runs before windows are computed; compute the rank in a CTE or subquery, then filter on it in the outer query.

**Schema and sample data:** nine employees; department 10 has a tie at the top (Ben and Dev both 70) and five people; department 20 has a tie at 80.
{{SCHEMA}}

**SQL answer:** `SQL_FAIL` is the broken query. `SQL_MAIN` is the CTE fix, `SQL_SUBQ` is the derived-table fix (same rows).
{{SQL:SQL_FAIL}}
{{SQL:SQL_MAIN}}
{{SQL:SQL_SUBQ}}

Dialect text, not executed here: BigQuery, Snowflake and DuckDB accept `QUALIFY`, which filters on a window result without the wrapper. SQLite, PostgreSQL and MySQL do not have it.
```sql
SELECT dept_id, emp_id, name, salary
FROM employees
QUALIFY RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) <= 3;
```

**pandas answer:** compute the rank as a column, then filter on it; `method="min"` matches `RANK`.
{{PD:main}}

**Example:**
- Department 10 salaries: 70, 70, 60, 50, 40. `RANK` gives 1, 1, 3, 4, 5, so `rnk <= 3` keeps Ben, Dev (rank 1) and Chitra (rank 3).
- Department 20: 90, 80, 80 gives ranks 1, 2, 2: all three rows stay.
- Department 30: Ila alone, rank 1.
- 7 rows come back; Asha (rank 4) and Esha (rank 5) are filtered out.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- The error: SQLite 3.45 says `misuse of window function RANK()` (see output). Message text differs by engine (not executed elsewhere).
- Order of evaluation matters for results, not just syntax. Putting a `WHERE` inside the CTE changes the ranks: with `WHERE salary < 70` first, Chitra becomes rank 1 in department 10 because the 70s were removed before ranking (last query in the output). If you want "top 3 overall, then something else", filter after.
- Ties at the cutoff: `RANK <= 3` can return more than three rows per department (Q11).
- Department with fewer than three people returns them all.

**Then explain:**
- Logical order: `FROM`, `WHERE`, `GROUP BY`, `HAVING`, window functions, `SELECT` list, `DISTINCT`, `ORDER BY`, `LIMIT`. The window value does not exist yet when `WHERE` runs.
- Window functions are allowed only in the `SELECT` list and `ORDER BY` (SQLite docs, and the PostgreSQL tutorial says the same for PostgreSQL).
- The CTE and the subquery give the same result here; pick the readable one. Whether an engine rewrites them identically is not something I measured.
- `QUALIFY` is just sugar for that wrapper, so the CTE form is the portable answer.

**Follow-ups:**
- *Can I put the rank in `HAVING`?* No, `HAVING` runs before windows too.
- *Can I use the alias `rnk` in the same SELECT's `WHERE`?* No, for the same reason (aliases come after windows).
- *What if I only want the top row per group?* Use `ROW_NUMBER() = 1` or `RANK() = 1` in the same wrapper (Q4, Q7).

**Common mistakes:**
- Writing `WHERE rnk <= 3` against an alias in the same query.
- Filtering with `WHERE` before ranking and not realising ranks are computed on the survivors.
- Saying `QUALIFY` works "in SQL"; it is not in SQLite, PostgreSQL or MySQL.
'''
P[4] = '''**Say this first (1 line):** Number each department's rows with `ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id)` in a CTE and keep `rn <= 3`; because `ROW_NUMBER` never repeats a number, you get exactly three rows per department when that many exist, and the `emp_id` tie-breaker makes the choice among equal salaries repeatable.

**Schema and sample data:** twelve employees. Department 10 has three people tied at 70 plus two lower salaries; department 20 has only two salaries and a NULL; department 30 has four people all at 55.
{{SCHEMA}}

**SQL answer:** tie-break rule I state: among equal salaries, the lower `emp_id` comes first.
{{SQL:SQL_MAIN}}

**pandas answer:** sort by department, salary descending, emp_id ascending, then either `groupby().head(3)` or `groupby().cumcount()`; `cumcount` starts at 0, so add 1 to match `ROW_NUMBER`.
{{PD:head}}
{{PD:cum}}

**Example:**
- Dept 10: sorted by salary DESC then emp_id: Ben (70, id 2), Dev (70, id 4), Esha (70, id 5), Chitra (60), Asha (50). Top three: Ben, Dev, Esha. Chitra at 60 is out even though she is the next-best, because three people tie at 70 and `ROW_NUMBER` hands out 1, 2, 3 to them.
- Dept 20: Farid 90, Gita 80, Hari NULL. Only three rows exist and NULL sorts last in descending order in both SQLite and pandas, so Hari is returned as number 3 with a NULL salary.
- Dept 30: four people at 55 (Ila 9, Jay 10, Kiran 11, Lata 12). The tie-breaker keeps Ila, Jay, Kiran and drops Lata.
- Nine rows total, three per department.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- Fewer than three rows in a department: you get what exists. With the NULL salary here, department 20 filled its third slot with a NULL-salary employee; add `WHERE salary IS NOT NULL` inside the CTE (and `dropna` in pandas) if that is unwanted.
- Ties at the cutoff are cut arbitrarily by `ROW_NUMBER`; the `emp_id` rule makes it a rule instead of luck. If the business wants every tied person, use `RANK` (Q11).
- The `cumcount` list in the output starts at 0 in every group (dept 10 has 0 to 4); that is why it needs `+ 1`.
- `groupby().head(3)` keeps the original index labels and has no rank column; the cumcount version gives you `rn`.

**Then explain:**
- `ROW_NUMBER` assigns a distinct integer to each row of the partition in `ORDER BY` order, so `rn <= 3` returns at most three rows per partition.
- Without `emp_id`, rows tied on salary can be numbered in any order, so which three come back can change between runs or engines (the standard leaves it open; PostgreSQL's tutorial says tied rows are numbered in unspecified order).
- The window cannot be in `WHERE`, so the CTE wrapper is needed (Q3).
- pandas: sort once with all the keys, then `head(3)` per group is the shortest form; `cumcount()` is the version that also gives you the number.

**Follow-ups:**
- *Top 3 including ties?* `RANK() <= 3` (Q11).
- *Top 3 salary levels?* `DENSE_RANK() <= 3` (Q8).
- *Need the output ordered?* Add the outer `ORDER BY` as I did; the order inside `OVER` does not order the result.

**Common mistakes:**
- Leaving out the unique tie-breaker and calling the result deterministic.
- Forgetting that `cumcount` starts at 0.
- Calling `groupby().head(3)` on an unsorted frame (it takes the first three rows as they come).
'''
P[5] = '''**Say this first (1 line):** Rank the distinct salaries with `DENSE_RANK() OVER (ORDER BY salary DESC)` in a CTE and take `MAX(salary)` where the rank is 2; the `MAX` wrapper returns NULL when no rank-2 row exists, and `ROW_NUMBER` or `RANK = 2` fail when the top salary is tied.

**Schema and sample data:** the same table shape, four different contents (each run in its own in-memory database).
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
-- A tied top:      100, 100, 90, 80
-- B one distinct:  50, 50
-- C empty table
-- D with a NULL:   NULL, 70, 70, 40
```
The exact rows are in the Code block.

**SQL answer:** `SQL_MAIN` is the answer; `SQL_RANK2` and `SQL_ROWNUM2` are the wrong versions for comparison.
{{SQL:SQL_MAIN}}
{{SQL:SQL_RANK2}}
{{SQL:SQL_ROWNUM2}}

**pandas answer:** drop NaN, drop duplicates, take the two largest, return the second or `None`.
{{PD:main}}

**Example:**
- A (100, 100, 90, 80): distinct levels are 100, 90, 80, so DENSE_RANK gives 1, 1, 2, 3 and the second highest is 90. `RANK` gives 1, 1, 3, 4: no row has rank 2, so it returns NULL, which is wrong. `ROW_NUMBER` gives 1, 2, 3, 4: the second row is the other 100, wrong.
- B (50, 50): only one distinct salary, so there is no second highest. DENSE_RANK has no rank 2, so `MAX` of nothing is NULL. `ROW_NUMBER = 2` returns 50, wrong.
- C: empty table, NULL.
- D: the NULL is filtered out, salaries 70, 70, 40 give levels 70 and 40, so the answer is 40.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- Fewer than two distinct values: NULL in SQL, `None` in pandas (the assert compares them).
- NULL salaries: filtered with `WHERE salary IS NOT NULL`, otherwise NULL would take a rank of its own (NULL sorts as smallest in SQLite).
- Why `MAX`: an aggregate over zero rows returns one row containing NULL, so the caller always gets exactly one row. A bare `SELECT salary ... WHERE rnk = 2` would return zero rows, or two identical rows when the second level is tied.
- A pandas surprise I hit: on the empty dataset the salary column had dtype object, and `nlargest` raised `TypeError: Cannot use method 'nlargest' with dtype object`. I cast the column to float in the script; real data from `read_sql_query` with no rows can do the same.
- `nlargest(2)` alone would return duplicates (100, 100), so `drop_duplicates()` first.

**Then explain:**
- You want the second highest value, not the second row, so rank values: `DENSE_RANK`.
- `RANK` skips numbers after a tie, so rank 2 can be missing. `ROW_NUMBER` counts rows, so it counts duplicates as separate positions.
- The `LIMIT 1 OFFSET 1` plus `DISTINCT` version works too (Part 3 Q15); the window version generalises to Nth and to per-group (Q6, Q46).
- I only know LeetCode 176's wording from third-party snippets; the behaviour above is what I ran.

**Follow-ups:**
- *Generalise to Nth?* Parameterise the rank (Q6).
- *Second highest per department?* Add `PARTITION BY dept_id` and group the result (Q46).
- *Without window functions?* `MAX(salary) WHERE salary < (SELECT MAX(salary) ...)`; it returns NULL naturally when absent.

**Common mistakes:**
- `RANK = 2` or `ROW_NUMBER = 2`.
- Returning no row instead of NULL.
- Forgetting `drop_duplicates` before `nlargest`.
'''
P[6] = '''**Say this first (1 line):** Rank the distinct non-NULL salaries with `DENSE_RANK() OVER (ORDER BY salary DESC)`, bind N as a `?` parameter, and return `MAX(salary)` where `rnk = ?`; when N is bigger than the number of distinct values the `MAX` gives NULL.

**Schema and sample data:** seven employees, four distinct salaries (100, 90, 80, 70) and one NULL.
{{SCHEMA}}

**SQL answer:** SQLite has no stored functions, so N goes in as a parameter from Python (`con.execute(SQL, (n,))`). `SQL_OFFSET` is the Part 3 style comparison.
{{SQL:SQL_MAIN}}
{{SQL:SQL_OFFSET}}

**pandas answer:** unique descending values, with an explicit range guard.
{{PD:main}}

**Example:** distinct values descending: 100, 90, 80, 70.
- N = 1 gives 100, N = 2 gives 90 (the duplicate 100 does not take a place), N = 3 gives 80, N = 4 gives 70.
- N = 5 and N = 10: there are only four levels, so no rank-5 row exists, so NULL.
- N = 0: no row has rank 0, so NULL from the window version.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- N = 0: the window version returns NULL, but the `OFFSET ? - 1` version computes `OFFSET -1`, which SQLite treats as 0, so it returned 100 (the highest) silently (output, N = 0 row). Same trap as in Part 3 Q15. Other engines reportedly reject a negative OFFSET (not executed here). Validate N >= 1 in the caller.
- pandas: `u.iloc[n - 1]` with `n = 0` is `iloc[-1]`, the smallest value (70 here, printed below the table). Hence the `1 <= n <= len(u)` guard.
- Ties: rows with equal salary share one level; `DISTINCT`/`DENSE_RANK` both count levels.
- NULL salaries: excluded by the filter.
- Duplicates and fewer-than-N values behave as above.

**Then explain:**
- "Nth highest" means the Nth distinct value, so I rank values, not rows. `DENSE_RANK` numbers distinct levels 1, 2, 3 without gaps, so `rnk = N` is exactly that level.
- `RANK` has gaps after ties and `ROW_NUMBER` counts duplicates, so both can miss or misplace the Nth level (Q5).
- Compare the OFFSET version in Part 3: `SELECT DISTINCT salary ... LIMIT 1 OFFSET N-1` gives the same answers for N >= 1 here, but it has the N = 0 trap and is not per-group. The window form extends to `PARTITION BY`.
- Both versions sort the salaries; I did not time them on large data.

**Follow-ups:**
- *Nth highest per department?* Partition and group (Q46).
- *Without a parameter?* A view or CTE with a literal; in engines with functions (PostgreSQL, MySQL) the LeetCode answer is often a function (not executed here).
- *Why return NULL?* The caller can tell "no such level" from an error.

**Common mistakes:**
- Using `ROW_NUMBER` or `RANK` and getting wrong values with ties.
- Not guarding N <= 0.
- Using OFFSET N instead of N-1.
'''
P[7] = '''**Say this first (1 line):** Use `RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) = 1` in a CTE (or `salary = MAX(salary) OVER (PARTITION BY dept_id)`), join to `departments`, and every employee tied at the department maximum comes back; `ROW_NUMBER() = 1` returns only one of them.

**Schema and sample data:** IT has a tie at 90 (Max and Randy); Sales has Henry 80, Sam 60 and Tia with a NULL salary; HR has no employees; Zed has a NULL department.
{{SCHEMA}}

**SQL answer:**
{{SQL:SQL_MAIN}}
Alternative with `MAX() OVER`:
{{SQL:SQL_MAX}}
The `ROW_NUMBER` version, to show what goes wrong (tie rule: lower emp_id):
{{SQL:SQL_ROWNUM}}

**pandas answer:** compare each salary to its group's `transform("max")`, then merge to the department names.
{{PD:main}}

**Example:**
- IT: max is 90, held by Max and Randy. Both are returned (Joe at 70 is not).
- Sales: Henry 80 is the max. Sam is lower; Tia's NULL salary is never equal to 80.
- HR: no employees, so with an inner join it does not appear.
- Zed (99, NULL department): his partition is the NULL group, ranks first inside it, but the join to `departments` finds no match (`NULL = dept_id` is not true), so he is dropped.
- `ROW_NUMBER() = 1` returns Max for IT only, losing Randy: it hands out 1 to exactly one row per department.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- Ties: all tied rows are returned (that is the point).
- All-NULL department: `MAX(salary) OVER` is NULL and `salary = NULL` is never true, so nobody is returned; by the NULL-peers rule `RANK` should rank the NULLs together as 1 and return them with NULL salary, so the two forms would differ on that edge (reasoned, not run: this data has no all-NULL department). Filter `salary IS NOT NULL` if it matters.
- Department with no employees: absent from an inner join; a `LEFT JOIN` from `departments` would show it with NULLs.
- NULL department: dropped by the join; pandas `groupby` drops the NaN key too, so `transform` gives NaN and the mask is False.

**Then explain:**
- `RANK` gives equal salaries the same rank, so rank 1 can be several rows. That is the correct answer to "everyone earning the max".
- `ROW_NUMBER = 1` is right only when you want exactly one row per department, with a stated tie rule (Q4, Q45).
- `MAX() OVER` reads more directly ("salary equals the department max") and has no rank to think about.
- I know the LeetCode 184 statement only from list snippets; the behaviour above is from my run.

**Follow-ups:**
- *One row per department even with ties?* `ROW_NUMBER` with a tie-breaker.
- *Top two salaries per department?* `DENSE_RANK <= 2` or `RANK <= 2` (Q8, Q11).
- *Without window functions?* A join to `SELECT dept_id, MAX(salary) ... GROUP BY dept_id` on dept and salary.

**Common mistakes:**
- `ROW_NUMBER() = 1` when ties must be kept.
- Using an inner join and not noticing the NULL-department or empty departments dropped.
- In pandas, `idxmax` per group, which returns only the first tied row (Q17, Q34).
'''

# Book 13 — Logical Reasoning & Analytical Thinking | Part 9: Data-Analyst Logic: Boolean, SQL/Excel NULL Traps, Decision Tables and Tracing 🟡🔴

**Target:** 60 questions | **Actual:** 60 questions
**Scope:** Boolean logic and truth tables, IF/AND/OR logic, SQL and Excel logic puzzles (NULL and three-valued logic, NOT IN traps, join and filter semantics), decision tables, flowchart and pseudocode tracing, and edge cases; SQL syntax how-to stays in Book 2, and puzzles state the dialect when it matters.

### Q1 ⭐⭐⭐ 🟢 In SQL's three-valued logic, what do `TRUE AND NULL`, `FALSE AND NULL`, `TRUE OR NULL`, `FALSE OR NULL` and `NOT NULL` evaluate to, and what does a `WHERE` clause do with a row whose condition evaluates to UNKNOWN?
**Asked at:** commonly asked (no company-specific report found); NULL and UNKNOWN semantics are covered in standard SQL references (Modern SQL, Snowflake docs), not reported for a named firm.
**What the interviewer is checking:** Whether you know NULL means "unknown", so a condition can be neither true nor false.
**Say this in the interview:** "NULL means unknown. TRUE AND NULL is unknown, FALSE AND NULL is false, TRUE OR NULL is true, FALSE OR NULL is unknown, NOT NULL is unknown. WHERE keeps only rows that are TRUE, so UNKNOWN rows are dropped, just like FALSE rows."
**Answer:** **`TRUE AND NULL` = NULL (UNKNOWN); `FALSE AND NULL` = FALSE; `TRUE OR NULL` = TRUE; `FALSE OR NULL` = NULL; `NOT NULL` = NULL. WHERE discards rows whose condition is UNKNOWN.**
**Step-by-step reasoning:**
1. Treat NULL as "some value I do not know".
2. AND: if one side is FALSE, the result is FALSE whatever the unknown is. Otherwise, an unknown makes the whole thing unknown.
3. OR: if one side is TRUE, the result is TRUE whatever the unknown is. Otherwise unknown.
4. NOT of an unknown is still unknown.
5. WHERE (and ON, HAVING) keeps a row only when the condition is TRUE.

Real output from Python sqlite3 (SQLite 3.53.1; SQLite writes TRUE as 1, FALSE as 0, UNKNOWN as None):
```sql
SELECT 1 AND NULL, 0 AND NULL, 1 OR NULL, 0 OR NULL, NOT NULL;
-- (None, 0, 1, None, None)
```
**Fast method (30 seconds):** FALSE wins in AND, TRUE wins in OR ("the decider wins"); if no decider is present, the answer is UNKNOWN.
**Check:** verified by script on sqlite3; the same table is standard SQL three-valued logic.
**Explain simply:**
- UNKNOWN is a third truth value, not an error and not the text "null".
- WHERE is a filter that asks "is this definitely true?". Unknown is "not definitely true", so the row goes.
- Consequence: `WHERE x = 5` and `WHERE NOT (x = 5)` together still miss rows where x is NULL.
**Likely follow-ups:** 1) *What is `NOT (TRUE AND NULL)`?* NOT of UNKNOWN is UNKNOWN (sqlite3 gives None). 2) *What is `NULL AND NULL`?* UNKNOWN (sqlite3 gives None).
**Common mistakes / traps:** Saying `FALSE AND NULL` is NULL; saying `NULL = NULL` is TRUE; thinking WHERE keeps UNKNOWN rows.

### Q2 ⭐⭐⭐ 🟢 A table `employees` has 10 rows. The `bonus` column holds: 5000, 0, NULL, 2000, NULL, 0, 3000, NULL, 0, 1500. How many rows does `SELECT * FROM employees WHERE bonus <> 0` return?
**Asked at:** commonly asked (no company-specific report found); a classic NULL-filter trap in SQL interview lists.
**What the interviewer is checking:** Whether you remember that a comparison with NULL is UNKNOWN, so NULL rows vanish from both `= 0` and `<> 0`.
**Say this in the interview:** "Four. The NULL rows give UNKNOWN for `bonus <> 0`, and WHERE drops them. Only 5000, 2000, 3000 and 1500 pass."
**Answer:** **4 rows** (not 7).
**Step-by-step reasoning:**
1. Rows with value 0 (three of them): `0 <> 0` is FALSE, dropped.
2. Rows with NULL (three of them): `NULL <> 0` is UNKNOWN, dropped.
3. Rows 5000, 2000, 3000, 1500: TRUE, kept. 10 - 3 - 3 = 4.

Real output from Python sqlite3:
```sql
SELECT bonus FROM employees WHERE bonus <> 0;
-- [(5000,), (2000,), (3000,), (1500,)]
SELECT COUNT(*) FROM employees WHERE bonus <> 0 OR bonus IS NULL;
-- 7
```
**Fast method (30 seconds):** count the non-NULL, non-zero values; ignore NULLs entirely.
**Check:** verified by script on sqlite3 (count 4; zeros 3; NULLs 3).
**Explain simply:**
- Any comparison (`=`, `<>`, `>`) with NULL gives UNKNOWN.
- To keep the unknown-bonus people too, say so: `WHERE bonus <> 0 OR bonus IS NULL` (7 rows), or `COALESCE(bonus, 0) <> 0` (back to 4, because it turns NULL into 0).
**Likely follow-ups:** 1) *How many rows for `WHERE NOT (bonus = 0)`?* Still 4 (script-verified), since NOT UNKNOWN is UNKNOWN. 2) *How many with `bonus <> 0 OR bonus IS NULL`?* 7.
**Common mistakes / traps:** Answering 7 (thinking "not zero" includes NULL); answering 10 minus 3 zeros.

### Q3 ⭐⭐⭐ 🟢 Which expression is equivalent to `NOT (status = 'Active' AND tenure > 2)`? (Assume neither column contains NULL.)
- (a) `status <> 'Active' AND tenure <= 2`
- (b) `status <> 'Active' OR tenure <= 2`
- (c) `status = 'Active' OR tenure > 2`
- (d) `status <> 'Active' AND tenure > 2`
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** De Morgan's law: negating a whole condition flips AND to OR and negates each part.
**Say this in the interview:** "NOT of an AND becomes an OR of the NOTs. The opposite of 'Active' is 'not Active', and the opposite of 'tenure > 2' is 'tenure <= 2'. That is option (b)."
**Answer:** **(b) `status <> 'Active' OR tenure <= 2`**
**Step-by-step reasoning:**
1. De Morgan: NOT (P AND Q) = (NOT P) OR (NOT Q).
2. NOT (status = 'Active') = status <> 'Active'.
3. NOT (tenure > 2) = tenure <= 2 (the boundary 2 moves to the "not" side).
4. Result: option (b).
5. Why others fail: (a) uses AND, which is too strict: for (Active, tenure 1) the original is TRUE but (a) is FALSE. (c) is not the negation of anything here. (d) keeps tenure > 2 unchanged.
**Fast method (30 seconds):** "break the line, change the sign": flip AND/OR, flip each comparison (`=` to `<>`, `>` to `<=`).
**Check:** verified by script over sample cases (status Active/Other, tenure 1, 2, 3, 5): the original and (b) agree in all 8 cases; (a), (c), (d) each disagree in some.
**Explain simply:**
- De Morgan's laws: NOT (A AND B) = NOT A OR NOT B; NOT (A OR B) = NOT A AND NOT B.
- The opposite of `>` is `<=`, not `<`: the equal case belongs to the opposite side.
- This only holds cleanly without NULLs; with NULLs, UNKNOWN values complicate it (see Q14).
**Likely follow-ups:** 1) *Negate `a > 5 OR b = 'X'`.* `a <= 5 AND b <> 'X'`. 2) *Which people does the original keep?* Everyone except Active staff with tenure over 2.
**Common mistakes / traps:** Flipping the comparisons but keeping AND (option a); writing `tenure < 2` and losing the value 2.

### Q4 ⭐⭐⭐ 🟢 Cell A1 holds a number and cell B1 holds `=IF(AND(A1>=10, A1<20), "Mid", IF(A1>=20, "High", "Low"))`. What does B1 show when A1 is 9, 10, 19 and 20 in turn?
**Asked at:** commonly asked (no company-specific report found); nested IF boundary tracing is a common Excel screening item.
**What the interviewer is checking:** Careful handling of boundary values (`>=` versus `>`) and the order of nested conditions.
**Say this in the interview:** "9 is Low, 10 is Mid, 19 is Mid, 20 is High. The Mid band is 10 up to but not including 20, and 20 falls to the second test."
**Answer:** **9 gives Low; 10 gives Mid; 19 gives Mid; 20 gives High.**
**Step-by-step reasoning:**
1. A1 = 9: 9>=10 is false, so AND is false; inner IF: 9>=20 false, so "Low".
2. A1 = 10: 10>=10 true and 10<20 true, so "Mid".
3. A1 = 19: 19>=10 true and 19<20 true, so "Mid".
4. A1 = 20: 20<20 false, so AND is false; inner IF: 20>=20 true, so "High".

| A1 | A1>=10 | A1<20 | AND | A1>=20 | B1 |
|---|---|---|---|---|---|
| 9 | F | T | F | F | Low |
| 10 | T | T | T | n/a | Mid |
| 19 | T | T | T | n/a | Mid |
| 20 | T | F | F | T | High |

**Fast method (30 seconds):** write the bands as intervals: Low is below 10, Mid is [10, 20), High is 20 and above. Then place each number. A square bracket includes the end, a round one excludes it.
**Check:** verified by a Python re-implementation of the IF logic (9 Low, 10 Mid, 19 Mid, 20 High); Excel itself not run here, but these are plain numeric comparisons.
**Explain simply:**
- AND returns TRUE only if every part is TRUE.
- IF(test, if_true, if_false): the third slot can hold another IF, which is checked only when the first test fails.
- Boundary values (10 and 20) are where interviewers look for slips.
**Likely follow-ups:** 1) *What does B1 show for 15.5?* Mid (10 <= 15.5 < 20). 2) *Can the AND be dropped?* Yes: `IF(A1>=20,"High",IF(A1>=10,"Mid","Low"))` gives the same result because earlier tests already rule out the higher bands.
**Common mistakes / traps:** Calling 20 "Mid" (reading `<20` as `<=20`); calling 10 "Low".

### Q5 ⭐⭐⭐ 🟢 A table `tickets` has 8 rows. Its `resolved_by` column holds: Ana, Ana, NULL, Raj, NULL, Raj, Ana, NULL. What do `COUNT(*)`, `COUNT(resolved_by)` and `COUNT(DISTINCT resolved_by)` return?
**Asked at:** commonly asked (no company-specific report found); a standard SQL aggregate-and-NULL question.
**What the interviewer is checking:** Whether you know `COUNT(*)` counts rows but `COUNT(column)` skips NULLs.
**Say this in the interview:** "8, 5 and 2. COUNT(*) counts every row; COUNT of the column skips the three NULLs; the distinct count sees only Ana and Raj."
**Answer:** **`COUNT(*)` = 8; `COUNT(resolved_by)` = 5; `COUNT(DISTINCT resolved_by)` = 2.**
**Step-by-step reasoning:**
1. `COUNT(*)` counts rows: 8.
2. `COUNT(resolved_by)` counts non-NULL values: Ana x3, Raj x2 = 5.
3. `COUNT(DISTINCT resolved_by)` counts different non-NULL values: Ana and Raj = 2.

Real output from Python sqlite3:
```sql
SELECT COUNT(*), COUNT(resolved_by), COUNT(DISTINCT resolved_by) FROM tickets;
-- [(8, 5, 2)]
```
**Fast method (30 seconds):** 8 rows minus 3 NULLs = 5; unique names = 2.
**Check:** verified by script on sqlite3.
**Explain simply:**
- Aggregate functions (SUM, AVG, COUNT of a column, MIN, MAX) ignore NULLs; only `COUNT(*)` counts rows regardless.
- NULL is not counted as a "distinct value" either.
- To count unresolved tickets, use `COUNT(*) - COUNT(resolved_by)` (= 3) or `SUM(CASE WHEN resolved_by IS NULL THEN 1 ELSE 0 END)`.
**Likely follow-ups:** 1) *What if all 8 values were NULL?* `COUNT(*)` = 8, `COUNT(col)` = 0 (script-verified for a 2-row all-NULL case: COUNT(*) = 2). 2) *How many unresolved tickets?* 3.
**Common mistakes / traps:** Saying all three return 8; counting NULL as a third distinct value (answer 3).

### Q6 ⭐⭐⭐ 🟢 Table `A` has `id` values 1, 2, 3, 4. Table `B` has `id` values 2 and NULL. How many rows does `SELECT id FROM A WHERE id NOT IN (SELECT id FROM B)` return, and why?
**Asked at:** commonly asked (no company-specific report found); the "NOT IN with a NULL" trap is widely described in SQL references (Modern SQL, jOOQ).
**What the interviewer is checking:** Whether you know that one NULL in the subquery makes `NOT IN` return nothing.
**Say this in the interview:** "Zero rows. `id NOT IN (2, NULL)` means id<>2 AND id<>NULL. The second part is UNKNOWN for every id, so no row can ever be TRUE. Use NOT EXISTS, or filter out NULLs in the subquery."
**Answer:** **0 rows.**
**Step-by-step reasoning:**
1. `id NOT IN (2, NULL)` expands to `id <> 2 AND id <> NULL`.
2. For id = 1: TRUE AND UNKNOWN = UNKNOWN. Same for 3 and 4.
3. For id = 2: FALSE AND UNKNOWN = FALSE.
4. No row gives TRUE, so WHERE keeps none.

Real output from Python sqlite3:
```sql
SELECT id FROM A WHERE id NOT IN (SELECT id FROM B);
-- []
SELECT id FROM A WHERE id NOT IN (SELECT id FROM B WHERE id IS NOT NULL);
-- [(1,), (3,), (4,)]
SELECT id FROM A WHERE NOT EXISTS (SELECT 1 FROM B WHERE B.id = A.id);
-- [(1,), (3,), (4,)]
```
**Fast method (30 seconds):** if the subquery in `NOT IN` can contain a NULL, expect zero rows.
**Check:** verified by script on sqlite3 (empty result, then both fixes give 1, 3, 4).
**Explain simply:**
- `IN` is a chain of ORs; `NOT IN` is a chain of ANDs of `<>`. One UNKNOWN in an AND chain can stop it ever being TRUE.
- Two fixes: add `WHERE id IS NOT NULL` inside the subquery, or use `NOT EXISTS`.
- The query is silently wrong, not an error, which is why it is dangerous.
**Likely follow-ups:** 1) *What does `id IN (SELECT id FROM B)` return?* Only id 2; the NULL does not create false matches (OR chain: a TRUE wins). 2) *What if B had no NULL?* Rows 1, 3, 4.
**Common mistakes / traps:** Answering 3 (ignoring the NULL); saying the query raises an error.

### Q7 ⭐⭐⭐ 🟢 Trace the pseudocode and give the printed value:
```
total = 0
FOR i = 1 TO 6
    IF i MOD 2 = 0 THEN
        total = total + i
    ELSE
        total = total - 1
PRINT total
```
**Asked at:** commonly asked (no company-specific report found); pseudocode output tracing is reported in prep-site lists for TCS, Infosys, Accenture and Cognizant (prep-site claim, unverified).
**What the interviewer is checking:** Patient, error-free step-by-step tracing with a table.
**Say this in the interview:** "I trace it in a table. Even i adds i, odd i subtracts 1. The result is 9."
**Answer:** **9**
**Step-by-step reasoning:** (MOD gives the remainder after division; `i MOD 2 = 0` means i is even.)

| i | even? | action | total after |
|---|---|---|---|
| 1 | no | total - 1 | -1 |
| 2 | yes | total + 2 | 1 |
| 3 | no | total - 1 | 0 |
| 4 | yes | total + 4 | 4 |
| 5 | no | total - 1 | 3 |
| 6 | yes | total + 6 | 9 |

**Fast method (30 seconds):** evens 2 + 4 + 6 = 12; odds 1, 3, 5 each subtract 1 so -3; 12 - 3 = 9. This works because the operations only add and subtract, so order does not matter.
**Check:** verified by running the loop in Python (prints 9).
**Explain simply:**
- `FOR i = 1 TO 6` runs with i = 1, 2, 3, 4, 5, 6 (both ends included).
- `MOD` is the remainder; even numbers have remainder 0 when divided by 2.
- A trace table (one row per loop turn) prevents slips.
**Likely follow-ups:** 1) *What if the loop ran to 4?* 2 + 4 - 2 = 4 (script-verified). 2) *What if the line were `total = total - i` in the ELSE?* Odds 1 + 3 + 5 = 9 subtracted from 12 gives 3.
**Common mistakes / traps:** Starting at 0 instead of 1; treating the else branch as `total - i`; stopping before i = 6.

### Q8 ⭐⭐⭐ 🟡 Trace this flowchart, written as numbered boxes, and give the two printed values:
```
1  START: a = 48, b = 18, count = 0
2  IF b = 0 THEN GO TO 6
3  r = a MOD b
4  a = b ; b = r ; count = count + 1
5  GO TO 2
6  PRINT a, count
```
**Asked at:** commonly asked (no company-specific report found); flowchart tracing is reported in prep-site lists for service-company tests (prep-site claim, unverified).
**What the interviewer is checking:** Following a loop built from GO TO jumps, and spotting the Euclid greatest-common-divisor pattern.
**Say this in the interview:** "I trace each pass. It is Euclid's algorithm, so a ends as the GCD of 48 and 18, which is 6, after 3 passes. It prints 6 and 3."
**Answer:** **Prints `6` and `3` (a = 6, count = 3).**
**Step-by-step reasoning:**

| Pass | b = 0? | r = a MOD b | a after | b after | count |
|---|---|---|---|---|---|
| start | | | 48 | 18 | 0 |
| 1 | no | 48 MOD 18 = 12 | 18 | 12 | 1 |
| 2 | no | 18 MOD 12 = 6 | 12 | 6 | 2 |
| 3 | no | 12 MOD 6 = 0 | 6 | 0 | 3 |
| exit | yes (box 2 jumps to 6) | | | | |

Box 6 prints a = 6 and count = 3.
**Fast method (30 seconds):** recognise Euclid: repeatedly replace (a, b) by (b, a MOD b) until b is 0. The answer a is the GCD (greatest common divisor, the biggest number dividing both). The pass count needs the trace.
**Check:** verified by running the loop in Python (6, 3).
**Explain simply:**
- Box 2 is a test: if b is 0, jump to box 6; otherwise carry on to boxes 3, 4, 5, then back to 2.
- In box 4, `a = b ; b = r` uses the OLD b for a, and the new r for b.
- GCD(48, 18) = 6 is a sanity check on the first answer.
**Likely follow-ups:** 1) *Start with a = 35, b = 14.* 35 MOD 14 = 7, then 14 MOD 7 = 0: prints 7 and 2 (script-verified). 2) *What if b started at 0?* Box 2 jumps straight to 6, printing a and 0.
**Common mistakes / traps:** Counting the final test as a pass (answering 4); printing b (0) instead of a.

### Q9 ⭐⭐⭐ 🟡 A table `t` has an integer column `x` that contains some NULLs. Why does `SELECT * FROM t WHERE x = x` not return every row, and what does it return?
**Asked at:** commonly asked (no company-specific report found); a standard "NULL is not equal to itself" interview probe.
**What the interviewer is checking:** Whether you accept that NULL = NULL is UNKNOWN, not TRUE.
**Say this in the interview:** "For a NULL row, `x = x` is NULL = NULL, which is UNKNOWN, so WHERE drops the row. It returns exactly the rows where x is not NULL. To include NULLs, add `OR x IS NULL`."
**Answer:** **It returns only the rows where `x` is not NULL (every row whose x is NULL is dropped).**
**Step-by-step reasoning:**
1. A non-NULL x: `x = x` is TRUE, row kept.
2. A NULL x: `NULL = NULL` is UNKNOWN, row dropped.
3. So `WHERE x = x` is a hidden way of writing `WHERE x IS NOT NULL`.

Real output from Python sqlite3 for x = 1, NULL, 3, NULL, 5:
```sql
SELECT * FROM t WHERE x = x;
-- [(1,), (3,), (5,)]
SELECT * FROM t WHERE x = x OR x IS NULL;
-- [(1,), (None,), (3,), (None,), (5,)]
```
**Check:** verified by script on sqlite3.
**Explain simply:**
- NULL means "unknown", and two unknowns are not known to be equal.
- Use `IS NULL` / `IS NOT NULL` to test for NULL, never `= NULL`.
- Some databases offer `IS NOT DISTINCT FROM` so that NULL matches NULL (see Q16).
**Likely follow-ups:** 1) *Does `x <> x` return anything?* No rows: for non-NULL it is FALSE, for NULL it is UNKNOWN. 2) *What does `WHERE x IS NOT NULL` return for the same data?* Same three rows.
**Common mistakes / traps:** Saying it returns every row because "a thing equals itself"; saying it errors.

### Q10 ⭐⭐⭐ 🟡 In Excel, cell A1 is truly empty (nothing typed, no formula). What do `=A1=0`, `=A1=""` and `=A1>0` return?
**Asked at:** commonly asked (no company-specific report found); Excel blank-cell behaviour is a frequent spreadsheet interview trap.
**What the interviewer is checking:** Whether you know Excel treats an empty cell as both 0 and empty text, depending on the comparison.
**Say this in the interview:** "From memory, not run here: an empty cell equals 0 and equals empty text, so TRUE and TRUE, and it is not greater than 0, so FALSE. I would confirm in the tool."
**Answer:** **From memory, not run here; confirm in Excel: `=A1=0` is TRUE, `=A1=""` is TRUE, `=A1>0` is FALSE.**
**Step-by-step reasoning:**
1. In a comparison, Excel treats a truly empty cell as 0 when compared with a number, so `A1=0` is TRUE and `A1>0` is FALSE.
2. In a comparison with text, it treats the empty cell as empty text, so `A1=""` is TRUE.
3. Both can be TRUE at once, so you cannot use `=0` to tell "blank" from "zero" (a typed 0 gives `=A1=0` TRUE but `=A1=""` FALSE).
**Fast method (30 seconds):** to detect a truly blank cell use `=ISBLANK(A1)` (TRUE only for a truly empty cell); a typed 0 or a formula returning "" are not blank by that test (from memory, not run here).
**Check:** not run here (no Excel available); behaviour as documented and widely taught, labelled unverified.
**Explain simply:**
- A truly empty cell is different from a cell holding 0 or a formula that returns "" (empty text).
- Excel's comparisons quietly convert the blank to whatever the other side needs.
- This is why SUM and AVERAGE results depend on whether blanks are really empty.
**Likely follow-ups:** 1) *What does `=ISBLANK(A1)` return?* TRUE for a truly empty cell (from memory, not run here). 2) *What if A1 holds `=""`?* Then `A1=""` is TRUE but ISBLANK is FALSE, and `A1=0` is FALSE (from memory, not run here).
**Common mistakes / traps:** Answering `=A1=0` is FALSE because "nothing is not zero"; using `=A1=0` as a blank test.

### Q11 ⭐⭐⭐ 🟡 A leave-approval rule is applied top to bottom and the first matching rule wins:
1. If the request falls in a blackout period, Reject.
2. Else if the leave balance is less than the days requested, Reject.
3. Else if the days requested are 2 or fewer, Auto-approve.
4. Else Manager approval.

| Request | Balance (days) | Days requested | Blackout period |
|---|---|---|---|
| A | 5 | 2 | No |
| B | 5 | 3 | No |
| C | 1 | 2 | No |
| D | 10 | 1 | Yes |
| E | 2 | 2 | No |

How many requests end in each outcome (Auto-approve, Manager approval, Reject)?
**Asked at:** commonly asked (no company-specific report found); decision-table and rule-ordering items appear in decision-table testing guides (BrowserStack, Tricentis; not interview reports).
**What the interviewer is checking:** Applying ordered rules with "first match wins" and noticing boundary cases (balance equal to days).
**Say this in the interview:** "Auto-approve 2 (A and E), Manager approval 1 (B), Reject 2 (C and D). E is the boundary: balance 2 is not less than 2, so rule 2 does not fire."
**Answer:** **Auto-approve: 2 (A, E). Manager approval: 1 (B). Reject: 2 (C, D).**
**Step-by-step reasoning:**

| Request | Rule 1 blackout? | Rule 2 balance < days? | Rule 3 days <= 2? | Outcome |
|---|---|---|---|---|
| A | No | 5 < 2 no | 2 <= 2 yes | Auto-approve |
| B | No | 5 < 3 no | 3 <= 2 no | Manager approval (rule 4) |
| C | No | 1 < 2 yes | not reached | Reject |
| D | Yes | not reached | not reached | Reject |
| E | No | 2 < 2 no | 2 <= 2 yes | Auto-approve |

**Fast method (30 seconds):** go row by row and stop at the first rule that fires; check the boundary rows (E) specifically.
**Check:** verified by a Python function applying the rules in order (A Auto, B Mgr, C Reject, D Reject, E Auto); counts 2, 1, 2 sum to 5 requests.
**Explain simply:**
- A decision table maps conditions to outcomes. With "first match wins", the order of the rules matters.
- D has plenty of balance and a small request, but rule 1 fires first, so it is rejected.
- Rule 4 is the default ("else"), which makes the rule set complete: every request gets an outcome.
**Likely follow-ups:** 1) *If E's balance were 1?* Rule 2 fires (1 < 2): Reject (hand-checked), giving Reject 3 and Auto-approve 1. 2) *If rules 2 and 3 swapped places?* C (balance 1, days 2) would be Auto-approved, a bug: overdrawn leave approved.
**Common mistakes / traps:** Rejecting E because balance equals days; applying rule 3 to D before rule 1.

### Q12 ⭐⭐⭐ 🟡 Table `employees(emp_id, name)` has rows (1, Asha), (2, Bala), (3, Chitra), (4, Dev). Table `attendance(emp_id, status)` has rows (1, Present), (1, Absent), (2, Absent), (3, Present). How many rows do these two queries return?
- Query 1: `SELECT e.name FROM employees e LEFT JOIN attendance a ON e.emp_id = a.emp_id AND a.status = 'Present'`
- Query 2: `SELECT e.name FROM employees e LEFT JOIN attendance a ON e.emp_id = a.emp_id WHERE a.status = 'Present'`
**Asked at:** commonly asked (no company-specific report found); "filter in ON versus WHERE" is a frequent LEFT JOIN interview question.
**What the interviewer is checking:** Whether you know that a WHERE on the right-hand table turns a LEFT JOIN into an inner join.
**Say this in the interview:** "Query 1 returns 4 rows, because the Present test is part of the join condition and unmatched employees are still kept with NULLs. Query 2 returns 2, because WHERE a.status = 'Present' throws away the NULL rows."
**Answer:** **Query 1: 4 rows. Query 2: 2 rows (Asha and Chitra).**
**Step-by-step reasoning:**
1. Query 1: each employee is matched only to Present rows. Asha has one Present row (kept once; her Absent row does not match), Bala has none (kept with NULL), Chitra has one, Dev has none (NULL). 1 + 1 + 1 + 1 = 4.
2. Query 2: the join first matches on emp_id alone (Asha twice, Bala once, Chitra once, Dev NULL = 5 rows), then WHERE keeps only status = 'Present': Asha and Chitra.

Real output from Python sqlite3 (name, status):
```sql
-- Query 1
-- [('Asha', 'Present'), ('Bala', None), ('Chitra', 'Present'), ('Dev', None)]
-- Query 2
-- [('Asha', 'Present'), ('Chitra', 'Present')]
```
**Fast method (30 seconds):** in a LEFT JOIN, a condition in ON never removes left-table rows; a condition in WHERE on the right table removes the NULL-extended rows.
**Check:** verified by script on sqlite3 (4 rows and 2 rows).
**Explain simply:**
- LEFT JOIN means "keep every left row, attach right rows where they match, otherwise NULLs".
- WHERE runs after the join; `NULL = 'Present'` is UNKNOWN, so unmatched rows vanish.
- To list employees with no Present record, use Query 1's join plus `WHERE a.emp_id IS NULL` (here Bala and Dev).
**Likely follow-ups:** 1) *How many rows with no extra condition at all (a plain LEFT JOIN on emp_id)?* 5 (Asha twice, Dev with NULL; script-verified). A plain inner join would give 4, because Dev has no attendance row. 2) *Which query finds "everyone, with attendance shown only if Present"?* Query 1.
**Common mistakes / traps:** Answering 5 for Query 1 (counting Asha's Absent row); answering 4 for Query 2.

### Q13 ⭐⭐⭐ 🟡 Table `staff(dept, salary)` has rows: (Sales, 40000), (Sales, 60000), (HR, 30000), (HR, 70000), (IT, 80000), (HR, 55000). How many rows does each query return?
- Query 1: `WHERE dept = 'Sales' OR dept = 'HR' AND salary > 50000`
- Query 2: `WHERE (dept = 'Sales' OR dept = 'HR') AND salary > 50000`
**Asked at:** commonly asked (no company-specific report found); AND/OR precedence is a standard filter trap.
**What the interviewer is checking:** Operator precedence: AND binds tighter than OR, and brackets change the meaning.
**Say this in the interview:** "Query 1 is Sales, OR (HR with salary over 50000): 4 rows. Query 2 puts the brackets round the departments, so salary over 50000 applies to both: 3 rows."
**Answer:** **Query 1: 4 rows. Query 2: 3 rows.**
**Step-by-step reasoning:**
1. Query 1 reads as `dept = 'Sales' OR (dept = 'HR' AND salary > 50000)`. All Sales rows qualify (40000, 60000), plus HR rows above 50000 (70000, 55000). Total 4. HR 30000 and IT 80000 do not.
2. Query 2: first dept must be Sales or HR, then salary > 50000: Sales 60000, HR 70000, HR 55000. Total 3.

Real output from Python sqlite3:
```sql
-- Query 1
-- [('Sales', 40000), ('Sales', 60000), ('HR', 70000), ('HR', 55000)]
-- Query 2
-- [('Sales', 60000), ('HR', 70000), ('HR', 55000)]
```
**Fast method (30 seconds):** put invisible brackets round every AND first, then read the OR. When in doubt, add brackets yourself.
**Check:** verified by script on sqlite3 (4 and 3).
**Explain simply:**
- Precedence in SQL: NOT first, then AND, then OR (like multiplication before addition).
- Query 1 includes the low-paid Sales row (40000) because that row only needs the Sales test.
- Writing brackets makes intent clear to the next reader.
**Likely follow-ups:** 1) *Rewrite Query 2 with IN.* `dept IN ('Sales','HR') AND salary > 50000`, 3 rows (script-verified). 2) *Which row differs between the two queries?* (Sales, 40000).
**Common mistakes / traps:** Reading left to right as if brackets were there; answering 3 for Query 1.

### Q14 ⭐⭐⭐ 🔴 Column `x` is NULL and column `y` is 5 in a row. Which of these conditions evaluate to TRUE for this row (so the row is kept by `WHERE`)? (a) `x > 3 OR y > 3`; (b) `x > 3 AND y > 3`; (c) `NOT (x > 3)`; (d) `x IS NULL AND y > 3`; (e) `x = x`.
**Asked at:** commonly asked (no company-specific report found); a compact NULL logic check often used in SQL screens.
**What the interviewer is checking:** Evaluating each condition with three-valued logic and knowing that only TRUE passes WHERE.
**Say this in the interview:** "x > 3 is UNKNOWN because x is NULL. (a) UNKNOWN OR TRUE is TRUE. (b) UNKNOWN AND TRUE is UNKNOWN. (c) NOT UNKNOWN is UNKNOWN. (d) IS NULL is a real TRUE test, so TRUE. (e) NULL = NULL is UNKNOWN. So (a) and (d) keep the row."
**Answer:** **(a) and (d) are TRUE; (b), (c) and (e) are UNKNOWN (row dropped).**
**Step-by-step reasoning:**

| Condition | Parts | Result | Kept by WHERE? |
|---|---|---|---|
| (a) `x > 3 OR y > 3` | UNKNOWN OR TRUE | TRUE | yes |
| (b) `x > 3 AND y > 3` | UNKNOWN AND TRUE | UNKNOWN | no |
| (c) `NOT (x > 3)` | NOT UNKNOWN | UNKNOWN | no |
| (d) `x IS NULL AND y > 3` | TRUE AND TRUE | TRUE | yes |
| (e) `x = x` | NULL = NULL | UNKNOWN | no |

Real output from Python sqlite3 for the row (NULL, 5) (value of the condition; None means UNKNOWN):
```sql
-- (a) 1   (b) None   (c) None   (d) 1   (e) None
-- COUNT(*) FROM z WHERE <cond>: a=1, b=0, c=0, d=1, e=0
```
**Fast method (30 seconds):** first replace every comparison involving x with "U" (unknown), then apply: U OR TRUE = TRUE, U AND TRUE = U, NOT U = U. Only IS NULL / IS NOT NULL give a real TRUE/FALSE for a NULL.
**Check:** verified by script on sqlite3.
**Explain simply:**
- WHERE keeps TRUE only; UNKNOWN is thrown away, like FALSE.
- (c) is the surprising one: the opposite of an unknown is still unknown, so `NOT (x > 3)` does not rescue the row.
- To keep NULL rows deliberately, write `x IS NULL` into the condition.
**Likely follow-ups:** 1) *How would you make (c) keep this row?* `NOT (x > 3) OR x IS NULL`, which is TRUE OR... for this row (UNKNOWN OR TRUE = TRUE). 2) *What does `x > 3 OR x <= 3` return for this row?* UNKNOWN (so the row is dropped, even though it "looks like" a tautology).
**Common mistakes / traps:** Treating UNKNOWN as FALSE inside NOT (answering that (c) is TRUE); assuming `x = x` is always TRUE.

### Q15 ⭐⭐⭐ 🔴 Table `A` has `id` values 1, NULL, 3. Table `B` has `id` values 3 and 4. How many rows does `SELECT id FROM A WHERE id NOT IN (SELECT id FROM B)` return, and which value is it?
**Asked at:** commonly asked (no company-specific report found); NOT IN with NULLs is a standard SQL interview trap on prep and blog sites (unverified).
**What the interviewer is checking:** Whether you know that a NULL on the left of `NOT IN` gives UNKNOWN, and that `WHERE` keeps only TRUE rows.
**Say this in the interview:** "This time the NULL is in the outer table, not in the subquery list. 1 is not in (3, 4), so it passes; 3 is in the list, so it fails; NULL compared with anything is UNKNOWN, so that row is dropped. One row, the value 1."
**Answer:** **1 row, and the value is 1.** The NULL row is not returned.
**Step-by-step reasoning:**
1. `id NOT IN (3, 4)` means `NOT (id = 3 OR id = 4)`.
2. Row id = 1: `1 = 3` is FALSE, `1 = 4` is FALSE, so OR gives FALSE, NOT gives TRUE. Kept.
3. Row id = 3: `3 = 3` is TRUE, so the OR is TRUE, NOT gives FALSE. Dropped.
4. Row id = NULL: `NULL = 3` and `NULL = 4` are both UNKNOWN, UNKNOWN OR UNKNOWN is UNKNOWN, NOT UNKNOWN is UNKNOWN. `WHERE` keeps only TRUE, so it is dropped.
Real sqlite3 output (SQLite 3.53.1):
```
SELECT id FROM A WHERE id NOT IN (SELECT id FROM B) -> [(1,)]
SELECT id FROM A WHERE NOT EXISTS (SELECT 1 FROM B WHERE B.id=A.id) -> [(1,), (None,)]
```
**Fast method (30 seconds):** Ask two things: is there a NULL in the list inside the brackets (then NOT IN returns nothing), and is there a NULL in the outer column (then that outer row is dropped)? Here only the second is true.
**Check:** Ran both queries on sqlite3 (output above). Note the `NOT EXISTS` version keeps the NULL row, because no B row matches it.
**Explain simply:**
- UNKNOWN means "cannot tell". `WHERE` treats UNKNOWN like FALSE, so the row is not shown.
- A NULL value is never "not in" a list, because the database cannot say it differs from every list member.
**Likely follow-ups:** 1) *What if B also held a NULL?* Then no outer row can be TRUE, so 0 rows (see Q6 and Q22). 2) *How do you keep the NULL row?* Use `NOT EXISTS`, or `WHERE id IS NULL OR id NOT IN (...)`; decide what the business wants first.
**Common mistakes / traps:** Answering 2 (1 and NULL) because "NULL is not in the list"; or answering 0 by copying the "NOT IN with NULL returns nothing" rule when the NULL is on the wrong side.

### Q16 ⭐⭐ 🟢 How do you correctly compare two columns that may both be NULL so that NULL matches NULL (for example with `IS NOT DISTINCT FROM` or a manual expression), and why does `a = b` fail for this?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know NULL is "unknown", so `=` can never say NULL matches NULL, and the null-safe alternatives.
**Say this in the interview:** "`a = b` gives UNKNOWN when either side is NULL, and WHERE drops UNKNOWN. For a null-safe match I use `a IS NOT DISTINCT FROM b` where the database supports it, or `(a = b OR (a IS NULL AND b IS NULL))`."
**Answer:** **Use `a IS NOT DISTINCT FROM b` (standard SQL; PostgreSQL supports it), or the manual form `(a = b) OR (a IS NULL AND b IS NULL)`. `a = b` fails because NULL = NULL is UNKNOWN, not TRUE.**
Real sqlite3 output for pairs (a, b), columns: `a=b`, `a IS b`, manual expression, `a IS NOT DISTINCT FROM b` (SQLite 3.53.1; SQLite spells the null-safe test `IS`, and also accepts the standard form in recent versions):
```
(1, 1)       -> 1, 1, 1, 1
(1, NULL)    -> NULL, 0, NULL, 0
(NULL, 1)    -> NULL, 0, NULL, 0
(NULL, NULL) -> NULL, 1, 1, 1
(1, 2)       -> 0, 0, 0, 0
```
Note the manual expression returns NULL (not 0) for (1, NULL); in a `WHERE` that still drops the row, which is the same effect as FALSE. For a strict TRUE/FALSE result use `IS NOT DISTINCT FROM`.
Support by database (from memory, not run here; confirm in the tool): PostgreSQL has `IS NOT DISTINCT FROM`; MySQL uses `a <=> b`; SQL Server recent versions have `IS NOT DISTINCT FROM`, older ones need the manual form; Oracle needs the manual form or `DECODE`.
**Explain simply:**
- NULL means "value not known", so two unknowns might or might not be equal; SQL answers UNKNOWN.
- "Distinct from" is the null-safe version of "not equal": it treats two NULLs as the same thing.
**Likely follow-ups:** 1) *Where does this matter?* Joining on a key that has NULLs (a plain `ON a.k = b.k` never matches NULL rows, see Q37 in this part), and comparing old and new snapshots to find changes. 2) *What does `a <> b` return for (NULL, NULL)?* UNKNOWN too.
**Common mistakes / traps:** Writing `a = NULL` or `a = b OR a IS NULL` (the second matches (NULL, 1) wrongly). The manual form must test that both sides are NULL.

### Q17 ⭐⭐ 🟢 Define XOR (exclusive or). For three Boolean inputs A, B and C, how many of the 8 input combinations make `A XOR B XOR C` true?
**Asked at:** commonly asked (no company-specific report found); symbolic logic is listed among test topics by assessment vendors (reported, unverified).
**What the interviewer is checking:** Whether you can define XOR precisely and extend it to three inputs without guessing.
**Say this in the interview:** "XOR is true when exactly one of two inputs is true, that is, when they differ. Chained over three inputs it is true when an odd number of inputs are true. That is 4 of the 8 combinations."
**Answer:** **4 combinations.**
**Step-by-step reasoning:**
1. Two inputs: A XOR B is true for (1,0) and (0,1) only, so it means "A and B differ".
2. A XOR B XOR C is (A XOR B) XOR C. It flips each time one more input is true, so the result is true exactly when an odd number of inputs are true.
3. Odd counts: one true (3 ways: C(3,1)) or three true (1 way: C(3,3)). 3 + 1 = 4.
4. The true rows are (A,B,C) = (0,0,1), (0,1,0), (1,0,0), (1,1,1).
**Fast method (30 seconds):** Half of all combinations (8 / 2 = 4) make a parity (odd or even count) test true, for any number of inputs of at least one.
**Check:** Verified by script over all 8 combinations: exactly the four rows listed. Also 8 of 16 for four inputs.
**Explain simply:**
- Inclusive OR is true when at least one is true; XOR excludes the "both" case.
- Chained XOR is a parity check: it asks whether the count of TRUE inputs is odd.
**Likely follow-ups:** 1) *How many combinations make A XOR B true?* 2 of 4. 2) *Careful: is "exactly one of three is true" the same as the chained XOR?* No. Exactly one gives 3 rows; chained XOR also counts the all-true row, giving 4.
**Common mistakes / traps:** Answering 3 (reading three-way XOR as "exactly one"), or forgetting the (1,1,1) row.

### Q18 ⭐⭐ 🟢 Cell C1 holds `=IF(OR(A1="", B1=""), "Missing", A1+B1)`. What does C1 show for (i) A1 = 5 and B1 truly empty, (ii) A1 = 5 and B1 = 0, (iii) A1 and B1 both empty?
**Asked at:** commonly asked (no company-specific report found); blank-cell handling is a standard Excel screening topic on prep sites (unverified).
**What the interviewer is checking:** Whether you separate "empty" from "zero" in Excel comparisons.
**Say this in the interview:** "A truly empty cell equals the empty text, so `B1=""` is TRUE and it shows Missing. A zero is a number, not empty text, so (ii) adds to 5. Both empty gives Missing."
**Answer:** **(i) Missing; (ii) 5; (iii) Missing.** (Excel behaviour from memory, not run here; confirm in the tool.)
**Step-by-step reasoning:**
1. In Excel, a truly empty cell compared with `""` gives TRUE (an empty cell counts as empty text in a text comparison).
2. (i) `B1=""` is TRUE, so OR is TRUE, result "Missing".
3. (ii) `A1=""` is FALSE (5 is a number) and `B1=""` is FALSE (0 is a number, not empty text), so OR is FALSE and the formula returns 5 + 0 = 5.
4. (iii) Both comparisons are TRUE, result "Missing".
**Explain simply:**
- "Truly empty" means nothing typed and no formula. A cell with a formula returning `""` looks empty but is text; it also tests as `=""`.
- Zero is a real value; treating it as missing would wrongly hide valid zeros.
**Likely follow-ups:** 1) *What if B1 held a single space?* It is text " ", not equal to "", so the formula would try 5 + " " and show a #VALUE! error (from memory, unverified). 2) *Which test is stricter for blank?* `ISBLANK(B1)` is TRUE only for a truly empty cell.
**Common mistakes / traps:** Thinking an empty cell and zero are the same (they are not for `=""`), or answering 5 for (i).

### Q19 ⭐⭐ 🟢 Trace the pseudocode and give the printed values:
```
a = 7
b = 3
a = a + b
b = a - b
a = a - b
PRINT a, b
```
**Asked at:** commonly asked (no company-specific report found); output-tracing questions are reported on prep sites for service-company aptitude sets (unverified).
**What the interviewer is checking:** Careful line-by-line tracing, and recognising the swap-without-temp trick.
**Say this in the interview:** "I keep a trace table. a becomes 10, then b becomes 10 - 3 = 7, then a becomes 10 - 7 = 3. It prints 3 and 7: the two values are swapped."
**Answer:** **3 7**
**Step-by-step reasoning:**
| After line | a | b |
|---|---|---|
| start | 7 | 3 |
| a = a + b | 10 | 3 |
| b = a - b | 10 | 7 |
| a = a - b | 3 | 7 |
**Fast method (30 seconds):** Three lines of "sum, then subtract" is the classic arithmetic swap: the output is the inputs in reversed order.
**Check:** Ran the lines in Python: prints 3 7.
**Explain simply:**
- A trace table records every variable after each line, so you never rely on memory.
- Each line uses the current values, not the starting values.
**Likely follow-ups:** 1) *Would it work with a = 5, b = 5?* Yes: 10, 5, 5, prints 5 5 (swap of equal values). 2) *What risk does this swap have in real systems?* Overflow for huge integers (not an issue in Python).
**Common mistakes / traps:** Using the original b in the last line (answering 4 7 or 7 3).

### Q20 ⭐⭐ 🟢 Table `X` has `v` values 1, 2, 2, 3. Table `Y` has `v` values 2, 3, 4. How many rows do `SELECT v FROM X UNION SELECT v FROM Y` and `SELECT v FROM X UNION ALL SELECT v FROM Y` return?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** UNION removes duplicates, UNION ALL keeps every row.
**Say this in the interview:** "UNION de-duplicates, so the distinct values 1, 2, 3, 4 give 4 rows. UNION ALL just stacks 4 + 3 = 7 rows."
**Answer:** **UNION returns 4 rows; UNION ALL returns 7 rows.**
**Step-by-step reasoning:**
1. UNION ALL stacks both results: 4 rows from X plus 3 rows from Y = 7 (values 1, 2, 2, 3, 2, 3, 4).
2. UNION then removes duplicate rows from that stack: distinct values are 1, 2, 3, 4 = 4 rows. The duplicate 2 inside X is removed too, not just the overlap with Y.
Real sqlite3 output:
```
SELECT count(*) FROM (SELECT v FROM X UNION SELECT v FROM Y) -> [(4,)]
SELECT count(*) FROM (SELECT v FROM X UNION ALL SELECT v FROM Y) -> [(7,)]
```
**Fast method (30 seconds):** UNION ALL = row counts added. UNION = count of distinct values across both.
**Check:** Ran both on sqlite3 (output above).
**Explain simply:**
- UNION ALL is faster because it skips the duplicate-removal step; use it when you know there are no overlaps or you want to keep duplicates.
- Both queries need the same number of columns with compatible types.
**Likely follow-ups:** 1) *How many rows from `X INTERSECT Y`?* 2 (values 2 and 3, de-duplicated). 2) *Does UNION guarantee sorted output?* No, add `ORDER BY` if order matters.
**Common mistakes / traps:** Thinking UNION only removes duplicates between the two tables (giving 5) instead of all duplicates.

### Q21 ⭐⭐ 🟡 A shortlist rule says: shortlist a candidate if experience is at least 2 years AND (SQL test passed OR Python test passed) AND NOT flagged by background check. Which candidates are shortlisted?

| Candidate | Experience (years) | SQL passed | Python passed | Flagged |
|---|---|---|---|---|
| C1 | 3 | Yes | No | No |
| C2 | 1.5 | Yes | Yes | No |
| C3 | 4 | No | No | No |
| C4 | 2 | No | Yes | Yes |
| C5 | 2 | No | Yes | No |
| C6 | 5 | Yes | Yes | No |
**Asked at:** commonly asked (no company-specific report found); rule-evaluation tables are a common HR-analytics and decision-logic exercise.
**What the interviewer is checking:** Applying AND, OR, NOT with correct precedence and boundary values (at least 2 includes exactly 2).
**Say this in the interview:** "I test each row against three gates: experience at least 2, at least one test passed, and not flagged. C1, C5 and C6 pass all three."
**Answer:** **C1, C5 and C6.**
**Step-by-step reasoning:**
| Cand. | Exp >= 2 | SQL or Python | Not flagged | Shortlisted |
|---|---|---|---|---|
| C1 | Yes | Yes | Yes | **Yes** |
| C2 | No (1.5) | Yes | Yes | No |
| C3 | Yes | No | Yes | No |
| C4 | Yes (exactly 2) | Yes | No | No |
| C5 | Yes (exactly 2) | Yes | Yes | **Yes** |
| C6 | Yes | Yes | Yes | **Yes** |
The brackets matter: `(SQL OR Python)` is one gate. Without them, AND binds tighter than OR in most languages and the meaning changes.
**Fast method (30 seconds):** Cross off by the cheapest "no" first: experience below 2 removes C2, no test removes C3, flag removes C4.
**Check:** Evaluated the rule on all six rows by script: C1, C5, C6.
**Explain simply:**
- AND needs every part true; OR needs at least one; NOT flips.
- "At least 2" means 2 or more, so C4 and C5 pass that gate.
**Likely follow-ups:** 1) *If the rule were `experience > 2`?* C5 drops out (exactly 2); shortlist is C1 and C6. 2) *If brackets were removed, `exp>=2 AND SQL OR Python AND NOT flagged`?* C2 would sneak in via the Python part; always bracket mixed AND/OR.
**Common mistakes / traps:** Treating "at least 2" as "more than 2", or shortlisting C4 because they passed a test and ignoring the flag.

### Q22 ⭐⭐ 🟡 Table `A` has `id` values 1, 2, 3, 4 and table `B` has `id` values 2 and NULL. Which ids does `SELECT id FROM A WHERE NOT EXISTS (SELECT 1 FROM B WHERE B.id = A.id)` return, and why does it differ from the `NOT IN` version of the same query?
**Asked at:** commonly asked (no company-specific report found); NOT IN versus NOT EXISTS is a widely taught SQL trap (unverified for any single company).
**What the interviewer is checking:** Whether you understand why NOT EXISTS is NULL-safe and NOT IN is not.
**Say this in the interview:** "NOT EXISTS only asks whether a matching row exists; a NULL in B never matches, so it is harmless. It returns 1, 3 and 4. NOT IN with a NULL in the list returns nothing, because every comparison becomes UNKNOWN."
**Answer:** **NOT EXISTS returns ids 1, 3 and 4. The NOT IN version returns 0 rows.**
**Step-by-step reasoning:**
1. NOT EXISTS: for each A row, look for a B row with `B.id = A.id`. Only id 2 finds one. The B row with NULL gives `NULL = A.id`, which is UNKNOWN, so it is not a match. So ids 1, 3, 4 have no match and are kept.
2. NOT IN: `id NOT IN (2, NULL)` means `id <> 2 AND id <> NULL`. For id = 1: TRUE AND UNKNOWN = UNKNOWN, dropped. Same for 3 and 4. For id = 2: FALSE. So no row is TRUE.
Real sqlite3 output:
```
NOT IN                      -> []
NOT EXISTS                  -> [(1,), (3,), (4,)]
NOT IN (NULLs filtered out) -> [(1,), (3,), (4,)]
IN                          -> [(2,)]
```
**Fast method (30 seconds):** If the subquery column can contain NULL, prefer `NOT EXISTS`, or add `WHERE id IS NOT NULL` inside the NOT IN subquery.
**Check:** Ran all four queries on sqlite3 (output above).
**Explain simply:**
- EXISTS tests "is there at least one matching row"; it returns TRUE or FALSE, never UNKNOWN.
- NOT IN expands to a chain of "not equal" tests joined by AND, and one UNKNOWN poisons the chain.
**Likely follow-ups:** 1) *Does a NULL in A change NOT EXISTS?* Yes: an A row with NULL has no match, so it is returned (see Q15). 2) *Is a LEFT JOIN ... WHERE B.id IS NULL also safe?* Yes, same result as NOT EXISTS here.
**Common mistakes / traps:** Assuming NOT IN and NOT EXISTS are interchangeable, or expecting 1, 3, 4 from NOT IN.

### Q23 ⭐⭐ 🟡 Using symbols A, B and `→` for "implies", how many of these four statements are tautologies (true for every combination of A and B)?
- (i) A OR NOT A
- (ii) (A AND B) → A
- (iii) (A → B) → (B → A)
- (iv) NOT (A AND B) is equivalent to (NOT A) OR (NOT B)
**Asked at:** commonly asked (no company-specific report found); propositional logic is listed among test topics by assessment vendors (reported, unverified).
**What the interviewer is checking:** Building a truth table and knowing that implication is false only when the first part is true and the second false.
**Say this in the interview:** "I build the four-row truth table. (i), (ii) and (iv) are always true; (iii) fails when A is false and B is true. So 3 tautologies."
**Answer:** **3 tautologies: (i), (ii) and (iv).** (iii) is not.
**Step-by-step reasoning:**
`P → Q` is false only when P is true and Q is false.
| A | B | (i) | (ii) | A→B | B→A | (iii) | (iv) |
|---|---|---|---|---|---|---|---|
| T | T | T | T | T | T | T | T |
| T | F | T | T | F | T | T | T |
| F | T | T | T | T | F | **F** | T |
| F | F | T | T | T | T | T | T |
(i) is the law of the excluded middle. (ii) says that if both are true then A is true. (iii) compares a statement with its converse, which is not equivalent. (iv) is De Morgan's law.
**Fast method (30 seconds):** Look for a counterexample row. For (iii), make `A → B` true while `B → A` is false: A false, B true.
**Check:** Truth table computed by script over all 4 rows: three always true, (iii) fails on A = F, B = T.
**Explain simply:**
- A tautology is a statement true in every case; a truth table lists every case.
- "Implies" is not "if and only if"; the reverse direction (converse) does not follow.
**Likely follow-ups:** 1) *Is `(A → B) → (NOT B → NOT A)` a tautology?* Yes, it is the contrapositive. 2) *Is `A AND NOT A` a tautology?* No, it is always false (a contradiction).
**Common mistakes / traps:** Treating (iii) as true because "implication works both ways", or counting (iv) wrong by forgetting De Morgan flips AND to OR.

### Q24 ⭐⭐ 🟡 Cells A1:A6 hold: 5, 3, (truly empty), 7, 5, the text "n/a". What does `=COUNTIF(A1:A6, "<>5")` return?
**Asked at:** commonly asked (no company-specific report found); Excel COUNTIF quirks are a common screening topic (unverified).
**What the interviewer is checking:** Whether you know `"<>5"` counts everything that is not the number 5, including blanks and text.
**Say this in the interview:** "`<>5` means every cell that is not equal to 5, so it counts the 3, the 7, the empty cell and the text. I get 4. If I want only numbers other than 5, I add a second condition."
**Answer:** **4** (the cells holding 3, 7, the empty cell A3 and "n/a"). From memory, not run here; confirm in the tool.
**Step-by-step reasoning:**
1. Cells equal to 5: A1 and A5, so these two are excluded.
2. The other four cells are A2 (3), A3 (empty), A4 (7), A6 ("n/a").
3. Excel's `"<>5"` criterion counts blank cells and text as "not equal to 5", so all four count: 4.
4. To count only numbers other than 5: `=COUNTIFS(A1:A6,"<>5",A1:A6,"<>")` removes blanks but still keeps text; use `=SUMPRODUCT(ISNUMBER(A1:A6)*(A1:A6<>5))` for numbers only, giving 2 (also from memory, unverified).
**Explain simply:**
- COUNTIF reads its criterion as text, and `<>` means "not equal", with no check on type.
- Compare this with SQL: in SQL `x <> 5` skips NULL rows; Excel's COUNTIF counts blanks. The two tools disagree.
**Likely follow-ups:** 1) *What does `=COUNTIF(A1:A6,"<>")` count?* The non-empty cells, 5 here (from memory, unverified). 2) *What does `=COUNTIF(A1:A6,5)` return?* 2.
**Common mistakes / traps:** Answering 2 (thinking only numbers are counted), or 3 (forgetting the text cell).

### Q25 ⭐⭐ 🟡 A column `score` holds 80, NULL, 60, 100. What does `AVG(score)` return, and what would `AVG(COALESCE(score, 0))` return?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That aggregates ignore NULL, and that filling NULL with 0 changes the meaning of the average.
**Say this in the interview:** "AVG skips NULLs, so it is (80 + 60 + 100) / 3 = 80. If I replace NULL with 0 first, the denominator becomes 4 and the average is 240 / 4 = 60. Which is right depends on whether NULL means 'not tested' or 'scored zero'."
**Answer:** **`AVG(score)` = 80; `AVG(COALESCE(score, 0))` = 60.**
**Step-by-step reasoning:**
1. `AVG` adds the non-NULL values (80 + 60 + 100 = 240) and divides by their count (3): 80.
2. `COALESCE(score, 0)` returns the first non-NULL argument, so NULL becomes 0. Values: 80, 0, 60, 100; sum 240, count 4; average 60.
Real sqlite3 output:
```
SELECT AVG(score), AVG(COALESCE(score,0)), COUNT(score), SUM(score) FROM s
-> [(80.0, 60.0, 3, 240)]
```
**Explain simply:**
- `COUNT(column)`, `SUM`, `AVG`, `MIN` and `MAX` all skip NULL; only `COUNT(*)` counts every row.
- NULL means "no value"; zero means "a value of zero". Mixing them changes the result.
**Likely follow-ups:** 1) *What does AVG return if every value is NULL?* NULL, not 0. 2) *Which average would you report for an absent candidate?* Ask the business: absent usually means exclude, a zero score means include.
**Common mistakes / traps:** Assuming AVG divides by the total row count (giving 60), or filling blanks with 0 without thinking.

### Q26 ⭐⭐ 🟡 Trace the pseudocode and give the two printed values:
```
n = 27
steps = 0
WHILE n <> 1 AND steps < 5
    IF n MOD 2 = 0 THEN n = n / 2
    ELSE n = 3 * n + 1
    steps = steps + 1
PRINT n, steps
```
**Asked at:** commonly asked (no company-specific report found); loop tracing appears in reported service-company aptitude sets (prep-site claim, unverified).
**What the interviewer is checking:** Tracing a WHILE loop with two stop conditions, and not running past the step limit.
**Say this in the interview:** "I trace each pass: 27 becomes 82, 41, 124, 62, 31. After 5 passes steps hits 5 and the loop stops, even though n is not yet 1. It prints 31 and 5."
**Answer:** **31 5**
**Step-by-step reasoning:**
| Pass | n before | Rule | n after | steps |
|---|---|---|---|---|
| 1 | 27 (odd) | 3n + 1 | 82 | 1 |
| 2 | 82 (even) | n / 2 | 41 | 2 |
| 3 | 41 (odd) | 3n + 1 | 124 | 3 |
| 4 | 124 (even) | n / 2 | 62 | 4 |
| 5 | 62 (even) | n / 2 | 31 | 5 |
Before pass 6 the test `steps < 5` is false, so the loop ends. `MOD` means the remainder after division.
**Fast method (30 seconds):** Note the loop cap first: at most 5 passes, so you only compute 5 values.
**Check:** Ran the loop in Python: ends at n = 31, steps = 5.
**Explain simply:**
- A WHILE loop re-checks its condition before every pass; AND needs both parts true to continue.
- This is the Collatz rule (halve if even, else triple and add one); it eventually reaches 1 for 27 but needs many more steps.
**Likely follow-ups:** 1) *What if the cap were steps < 3?* Prints 124 3. 2) *What if the condition used OR?* The loop would continue while either part is true, so it only stops when n = 1 and steps >= 5: it runs 111 passes and prints 1 111 (script-verified).
**Common mistakes / traps:** Running until n = 1, or stopping one pass early or late (printing 62 4 or 94 6).

### Q27 ⭐⭐ 🟡 A decision table has three Yes/No conditions C1, C2 and C3, so there are 8 possible combinations. The table defines rules for these combinations only: YYY, YYN, YNY, NYY, NNY, NNN (written C1 C2 C3). How many combinations are missing, and which are they?
**Asked at:** commonly asked (no company-specific report found); completeness of decision tables is a standard testing topic on testing guides (unverified).
**What the interviewer is checking:** Systematic enumeration of all 2 x 2 x 2 = 8 cases and spotting the gaps.
**Say this in the interview:** "Three Yes/No conditions give 8 combinations. The table covers 6, so 2 are missing: YNN and NYN. I would ask the business what should happen there, or add a default rule."
**Answer:** **2 combinations are missing: YNN and NYN.**
**Step-by-step reasoning:**
1. List all 8 in order: YYY, YYN, YNY, YNN, NYY, NYN, NNY, NNN.
2. Cross off the six defined: YYY, YYN, YNY, NYY, NNY, NNN.
3. Left over: YNN and NYN.
4. Both missing cases have exactly one Yes in C1 or C2 and No in C3 (C3 = N with C1 and C2 different).
**Fast method (30 seconds):** Count first: 8 total minus 6 defined = 2 missing, then list in a fixed order (YYY down to NNN, like binary counting) so none is skipped.
**Check:** Verified by script (set difference of all 8 combinations and the 6 given).
**Explain simply:**
- A decision table is complete when every combination of conditions has an outcome.
- A missing combination is a gap where real data would get no rule; fix it with an explicit rule or a default "else".
**Likely follow-ups:** 1) *With 4 conditions, how many combinations?* 2^4 = 16. 2) *What if two rules cover the same combination with different results?* That is a conflict; the table needs a precedence rule or a fix.
**Common mistakes / traps:** Listing combinations in random order and missing one, or concluding only 1 is missing.

### Q28 ⭐⭐ 🟡 A query uses `CASE WHEN score >= 40 THEN 'Pass' WHEN score >= 75 THEN 'Distinction' WHEN score IS NULL THEN 'Absent' ELSE 'Fail' END`. What does it return for scores 30, 60, 80 and NULL?
**Asked at:** commonly asked (no company-specific report found); CASE ordering errors are a common SQL review topic (unverified).
**What the interviewer is checking:** That CASE stops at the first matching branch, so branch order matters, and how NULL flows through it.
**Say this in the interview:** "CASE takes the first true branch. 80 matches `>= 40` first, so it is Pass, and Distinction can never be reached. NULL makes both comparisons UNKNOWN, so it falls to the IS NULL branch: Absent. 30 gets Fail, 60 gets Pass."
**Answer:** **30 gives Fail; 60 gives Pass; 80 gives Pass (not Distinction); NULL gives Absent.**
**Step-by-step reasoning:**
1. 30: `30 >= 40` FALSE, `30 >= 75` FALSE, not NULL, so ELSE: Fail.
2. 60: `60 >= 40` TRUE, so Pass (stop).
3. 80: `80 >= 40` TRUE, so Pass (stop). The Distinction branch is unreachable.
4. NULL: `NULL >= 40` is UNKNOWN (not TRUE), `NULL >= 75` is UNKNOWN, `NULL IS NULL` is TRUE: Absent.
Real sqlite3 output:
```
Original order  -> (30,'Fail'), (60,'Pass'), (80,'Pass'), (None,'Absent')
Fixed order     -> (30,'Fail'), (60,'Pass'), (80,'Distinction'), (None,'Absent')
```
The fixed order puts `IS NULL` first, then `>= 75`, then `>= 40`, then ELSE.
**Fast method (30 seconds):** Order CASE branches from most specific to least specific (highest threshold first), and put the NULL test early or last deliberately.
**Check:** Ran both versions on sqlite3 (output above).
**Explain simply:**
- CASE is evaluated top to bottom and returns the first TRUE condition; UNKNOWN counts as not true.
- A branch that can never be reached is a silent bug, not an error.
**Likely follow-ups:** 1) *What happens with no ELSE and score 30?* The result is NULL. 2) *Would `score = NULL` ever be TRUE in a branch?* No, use `IS NULL` (see Q48).
**Common mistakes / traps:** Answering Distinction for 80, or sending NULL to Fail by assuming ELSE catches every non-match (here the IS NULL branch comes first).

### Q29 ⭐⭐ 🟡 Column `region` holds: North, NULL, South, North, NULL, NULL. How many groups does `SELECT region, COUNT(*) FROM t GROUP BY region` return, and what is the count in the NULL group?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know that GROUP BY puts all NULLs into one group, even though NULL = NULL is not true.
**Say this in the interview:** "GROUP BY treats NULLs as one group, so I get three groups: North 2, South 1, NULL 3."
**Answer:** **3 groups; the NULL group has a count of 3.**
**Step-by-step reasoning:**
1. Distinct values are North, South and "missing". GROUP BY groups missing values together, so that is 3 groups.
2. North appears 2 times, South 1 time, NULL 3 times (total 6 rows).
Run on Python sqlite3 (real output):
```
SELECT region, COUNT(*) FROM t GROUP BY region ORDER BY region
  -> [(None, 3), ('North', 2), ('South', 1)]
SELECT COUNT(DISTINCT region), COUNT(region), COUNT(*) FROM t
  -> [(2, 3, 6)]
```
**Check:** the second query shows `COUNT(region)` = 3 (skips NULLs) while `COUNT(*)` = 6 (counts rows); 2 + 1 + 3 = 6.
**Explain simply:**
- NULL means "value unknown or missing". A comparison `NULL = NULL` gives UNKNOWN, not TRUE.
- Still, the SQL standard says GROUP BY, DISTINCT and set operators treat NULLs as "the same" for grouping purposes.
- `COUNT(*)` counts rows; `COUNT(column)` counts only non-NULL values.
**Likely follow-ups:** 1) *What does `COUNT(region)` return for the whole table?* 3 (verified above). 2) *What does `COUNT(DISTINCT region)` return?* 2, because NULL is not counted as a value (verified above).
**Common mistakes / traps:** Saying "2 groups" because NULLs are dropped, or "3 NULL groups" because NULL is not equal to NULL.

### Q30 ⭐⭐ 🟡 A `login_ts` timestamp column holds: 2025-01-01 09:00, 2025-06-15 14:30, 2025-12-31 18:45, 2025-12-31 23:59, 2026-01-01 08:00. A date literal such as '2025-12-31' is read as midnight at the start of that day. How many rows does `WHERE login_ts BETWEEN '2025-01-01' AND '2025-12-31'` return, and what is the safer way to write the filter for "all of 2025"?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you spot that BETWEEN is inclusive at both ends and that a date means midnight, so the last day loses its daytime rows.
**Say this in the interview:** "BETWEEN with a bare end date stops at midnight starting that day, so the 31 December evening logins are lost. I use a half-open range: on or after 1 January 2025 and strictly before 1 January 2026."
**Answer:** **2 rows. Safer: `login_ts >= '2025-01-01' AND login_ts < '2026-01-01'` (returns 4 rows).**
**Step-by-step reasoning:**
1. BETWEEN a AND b means `>= a AND <= b`.
2. The upper bound '2025-12-31' is 2025-12-31 00:00. Both 18:45 and 23:59 on that day are later than midnight, so they fail.
3. Rows kept: 2025-01-01 09:00 and 2025-06-15 14:30 = 2.
4. The half-open filter keeps the first four rows and excludes 2026-01-01 08:00.
Run on Python sqlite3 (real output; timestamps stored as text in ISO format, which sorts correctly):
```
... WHERE login_ts BETWEEN '2025-01-01' AND '2025-12-31'
  -> [('2025-01-01 09:00',), ('2025-06-15 14:30',)]
... WHERE login_ts >= '2025-01-01' AND login_ts < '2026-01-01'
  -> [('2025-01-01 09:00',), ('2025-06-15 14:30',), ('2025-12-31 18:45',), ('2025-12-31 23:59',)]
```
**Check:** all 5 rows classified by script output above; the 4 rows in the safe version are exactly the 2025 ones.
**Explain simply:**
- "Half-open" means include the start, exclude the end: [start, next period start).
- It works for any precision (seconds, milliseconds) and the next range starts exactly where this one ends, so no gaps or overlaps.
- Caveat: in a column of pure dates (no time part), BETWEEN works. The trap is for timestamps. How a database reads a date literal against a timestamp column can differ by product (from memory, not run here; confirm in the tool).
**Likely follow-ups:** 1) *Why not `<= '2025-12-31 23:59'`?* It misses 23:59:30. 2) *Filter for December 2025?* `>= '2025-12-01' AND < '2026-01-01'`.
**Common mistakes / traps:** Answering 4 or 5; writing `'2025-12-31 23:59:59'` and still missing fractions of a second.

### Q31 ⭐⭐ 🟡 Simplify the filter `(region = 'West' AND tier = 'Gold') OR (region = 'West' AND tier <> 'Gold')`. Is it the same as `region = 'West'` when `tier` can be NULL? If not, what is the exactly equivalent filter?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you remember that simplification rules from two-valued logic ("X or not X is always true") fail when NULL is possible.
**Say this in the interview:** "Factoring out `region = 'West'` leaves `tier = 'Gold' OR tier <> 'Gold'`, which is not always true: with a NULL tier it is UNKNOWN. So it is the same as `region = 'West' AND tier IS NOT NULL`."
**Answer:** **Not the same. Exact equivalent: `region = 'West' AND tier IS NOT NULL`.**
**Step-by-step reasoning:**
1. Factor: `region = 'West' AND (tier = 'Gold' OR tier <> 'Gold')`.
2. If tier is not NULL, one of the two is true, so the bracket is TRUE.
3. If tier is NULL, both comparisons are UNKNOWN, and UNKNOWN OR UNKNOWN is UNKNOWN. WHERE keeps only TRUE, so the row is dropped.
4. So the bracket is TRUE exactly when `tier IS NOT NULL`.
Test data: (1 West Gold), (2 West Silver), (3 West NULL), (4 East Gold), run on sqlite3:
```
original filter            -> [(1,), (2,)]
region = 'West'            -> [(1,), (2,), (3,)]
West AND tier IS NOT NULL  -> [(1,), (2,)]
```
**Check:** row 3 (NULL tier) is the only difference; the script shows the original equals the IS NOT NULL version.
**Explain simply:**
- Three-valued logic: a condition can be TRUE, FALSE or UNKNOWN (UNKNOWN appears when NULL is compared).
- WHERE keeps only rows that are TRUE, so UNKNOWN rows vanish.
- The law "A OR NOT A = TRUE" holds only if A can never be UNKNOWN.
**Likely follow-ups:** 1) *How to include NULL tiers too?* Just use `region = 'West'`. 2) *Write "tier is not Gold, NULLs included"?* `tier <> 'Gold' OR tier IS NULL` (or `tier IS DISTINCT FROM 'Gold'` where supported; from memory, SQLite uses `IS NOT`).
**Common mistakes / traps:** Simplifying to `region = 'West'` by "X or not X"; assuming `<>` returns NULL rows.

### Q32 ⭐⭐ 🟡 A rule gives a discount when the order quantity is at least 1000 and below 5000 (whole numbers only). Which minimum set of quantities tests both boundaries on each side, and why is a "typical" value such as 2500 not enough?
**Asked at:** commonly asked (no company-specific report found); boundary-value testing is a standard decision-table testing topic (testing guides, unverified for interviews).
**What the interviewer is checking:** Whether you test the edges, where "at least" versus "more than" mistakes live.
**Say this in the interview:** "Rule is 1000 <= q < 5000 for whole numbers. I test 999, 1000, 4999 and 5000: just outside and just inside at each edge."
**Answer:** **999 (no discount), 1000 (discount), 4999 (discount), 5000 (no discount).**
**Step-by-step reasoning:**
1. Lower edge: 1000 is the first included whole number; 999 is the last excluded one.
2. Upper edge: 4999 is the last included; 5000 is the first excluded (rule says "below 5000").
3. Expected results: No, Yes, Yes, No. Checked by script: rule `1000 <= x < 5000` gives False, True, True, False for the four values, and True for 2500.
4. A wrong rule such as `>1000` (instead of `>=1000`) or `<=5000` (instead of `<5000`) still gives the same result for 2500, but fails at one of the four edge values.
**Check:** hand-and-script check above; re-run: the slips `>1000`, `>=1001`, `<=5000` and `<4999` each flip exactly one of the four edge tests (1000, 1000, 5000, 4999 respectively) and leave 2500 unchanged.
**Explain simply:**
- "Boundary value testing": most bugs sit at the edges of a range, so test just below, on, and just above (or the first and last valid values).
- A mid-range value like 2500 only proves the middle works.
- "Whole numbers only" lets us use 999 and 4999 as the neighbours; with decimals we would add values like 999.99.
**Likely follow-ups:** 1) *Decimals allowed?* Test 999.99, 1000, 4999.99, 5000. 2) *Is 2500 useless?* It is one "typical" representative; add it if you want a middle check, but it is not a minimum for edges.
**Common mistakes / traps:** Testing only 1000 and 5000 (misses the neighbour), or treating 5000 as discounted.

### Q33 ⭐⭐ 🔴 Trace the recursive function and give `f(6)`, and the total number of times `f` is called (including the first call) when evaluating `f(5)`:
```
FUNCTION f(n)
    IF n <= 1 THEN RETURN 1
    RETURN f(n - 1) + f(n - 2)
```
**Asked at:** pseudocode and recursion tracing is reported on prep sites for TCS, Infosys, Accenture, Cognizant (prep-site claim, unverified).
**What the interviewer is checking:** Whether you can trace a recursive call tree without losing track, and spot repeated work.
**Say this in the interview:** "Base cases f(0) = f(1) = 1, then each value is the sum of the previous two: 1, 1, 2, 3, 5, 8, 13. So f(6) = 13. For calls, c(n) = 1 + c(n-1) + c(n-2), which gives 15 for n = 5."
**Answer:** **f(6) = 13; evaluating f(5) makes 15 calls in total (and f(5) itself = 8).**
**Step-by-step reasoning:**
1. f(0) = 1, f(1) = 1 (base case, 1 call each).
2. f(2) = f(1) + f(0) = 2; f(3) = 3; f(4) = 5; f(5) = 8; f(6) = 13.
3. Number of calls c(n): c(0) = c(1) = 1; c(n) = 1 (this call) + c(n-1) + c(n-2).
4. c(2) = 3, c(3) = 5, c(4) = 9, c(5) = 15 (c(5) = 1 + 9 + 5).
Table (verified by running the function with a call counter):

| n | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| f(n) | 1 | 1 | 2 | 3 | 5 | 8 | 13 | 21 |
| calls | 1 | 1 | 3 | 5 | 9 | 15 | 25 | 41 |

**Fast method (30 seconds):** Values follow the Fibonacci pattern (add the previous two). Calls follow "calls = 2 x f(n) - 1": for n = 5, 2 x 8 - 1 = 15. This works because each call that returns 1 is a leaf, and a tree with L leaves where every inner node has 2 children has 2L - 1 nodes; f(n) equals the number of leaves.
**Check:** the script printed f(6) = 13 and, for f(5), value 8 and 15 calls.
**Explain simply:**
- Recursion means a function calls itself on a smaller input; the base case (n <= 1) stops it.
- The same small values are recomputed many times (f(2) is computed 3 times inside f(5)), which is why this is slow for large n.
**Likely follow-ups:** 1) *How many calls for f(6)?* 25 (script). 2) *How to speed up?* Remember (cache) results, or loop upward keeping the last two values.
**Common mistakes / traps:** Giving 6 or 8 for f(6) by treating f(0) as 0; counting only the leaf calls (8) instead of all calls (15).

### Q34 ⭐⭐ 🔴 A bonus rule in Excel is `bonus = salary * IF(rating >= 4, IF(tenure >= 3, 20%, 10%), IF(rating = 3, 5%, 0))`. Compute the total bonus for these five employees.

| Employee | Salary | Rating | Tenure (years) |
|---|---|---|---|
| E1 | 50000 | 5 | 4 |
| E2 | 40000 | 4 | 1 |
| E3 | 60000 | 3 | 5 |
| E4 | 30000 | 2 | 6 |
| E5 | 80000 | 4 | 3 |
**Asked at:** commonly asked (no company-specific report found); nested IF logic is a standard Excel screening topic (unverified as a company-specific item).
**What the interviewer is checking:** Whether you can follow nested IF branches in the right order, including boundary values (>= means "equal counts").
**Say this in the interview:** "Rating 4 or more goes to the tenure split: 20% if tenure is 3 or more, else 10%. Rating exactly 3 gets 5%, anything lower gets 0. Total is 33,000."
**Answer:** **Total bonus = 33,000.**
**Step-by-step reasoning:**
1. E1: rating 5 (>= 4), tenure 4 (>= 3) so 20% of 50000 = 10,000.
2. E2: rating 4, tenure 1 (< 3) so 10% of 40000 = 4,000.
3. E3: rating 3 (not >= 4, equals 3) so 5% of 60000 = 3,000.
4. E4: rating 2 (not >= 4, not 3) so 0% = 0 (tenure 6 is never looked at).
5. E5: rating 4, tenure 3 (>= 3 counts the boundary) so 20% of 80000 = 16,000.
6. Sum: 10,000 + 4,000 + 3,000 + 0 + 16,000 = 33,000.
**Check:** script re-implemented the rule and printed [10000, 4000, 3000, 0, 16000], total 33,000 (Python logic, not run in Excel; the IF logic is standard).
**Explain simply:**
- Nested IF: an IF inside another IF's "true" or "false" slot. Only one branch runs.
- `20%` in Excel is just 0.2.
- Tenure only matters when rating is at least 4.
**Likely follow-ups:** 1) *What if E5's rule were `tenure > 3`?* E5 drops to 10%: 8,000, total 25,000 (hand-checked: 33,000 - 16,000 + 8,000). 2) *Rating 3.5?* It fails `>= 4` and `= 3`, so 0.
**Common mistakes / traps:** Treating tenure 3 as below the cut-off; giving E4 a bonus because of tenure.

### Q35 ⭐⭐ 🔴 Trace the nested loops and give the printed value:
```
count = 0
FOR i = 1 TO 4
    FOR j = i TO 4
        IF (i + j) MOD 3 = 0 THEN count = count + 1
PRINT count
```
**Asked at:** loop tracing is reported on prep sites for TCS, Infosys, Accenture, Cognizant (prep-site claim, unverified).
**What the interviewer is checking:** Whether you handle a loop whose inner start depends on the outer variable, and the MOD (remainder) test.
**Say this in the interview:** "The pairs are those with j >= i. I list the pairs whose sum divides by 3: (1,2), (2,4), (3,3). So it prints 3."
**Answer:** **3**
**Step-by-step reasoning:** (MOD 3 = 0 means the sum leaves remainder 0 when divided by 3.)
1. i = 1: j = 1..4, sums 2, 3, 4, 5. Only 3 qualifies: (1,2). count = 1.
2. i = 2: j = 2..4, sums 4, 5, 6. Only 6: (2,4). count = 2.
3. i = 3: j = 3..4, sums 6, 7. Only 6: (3,3). count = 3.
4. i = 4: j = 4, sum 8, remainder 2. No. count stays 3.
**Check:** script ran the loops and printed 3, with pairs [(1,2), (2,4), (3,3)].
**Explain simply:**
- 10 pairs are visited in total (4 + 3 + 2 + 1), not 16, because j starts at i.
- MOD gives the remainder: 6 MOD 3 = 0, 7 MOD 3 = 1.
**Likely follow-ups:** 1) *If j started at 1 instead of i?* All 16 ordered pairs: pairs summing to 3 or 6: (1,2),(2,1),(2,4),(4,2),(3,3) = 5 (hand-checked: sum 3: two, sum 6: three; sum 9 impossible). 2) *How many iterations ran?* 10.
**Common mistakes / traps:** Running j from 1 each time (gives 5); counting (3,3) twice or forgetting it, because i = j.

### Q36 ⭐⭐ 🔴 Table `P` has `k` values 1, NULL, NULL, 2 and table `Q` has `k` values NULL, 2. What do `SELECT k FROM P EXCEPT SELECT k FROM Q` and `SELECT k FROM P INTERSECT SELECT k FROM Q` return? (Use the standard rule that set operators treat NULLs as equal to each other and remove duplicates.)
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know set operators compare NULLs as equal and remove duplicates, unlike `=` in a join.
**Say this in the interview:** "Set operators treat NULLs as equal and de-duplicate. P distinct is {1, NULL, 2}, Q is {NULL, 2}. EXCEPT leaves 1; INTERSECT leaves NULL and 2."
**Answer:** **EXCEPT returns one row: 1. INTERSECT returns two rows: NULL and 2.**
**Step-by-step reasoning:**
1. Remove duplicates: P becomes {1, NULL, 2} (the two NULLs merge). Q is {NULL, 2}.
2. EXCEPT = in P but not in Q: 1 only (NULL and 2 are in Q).
3. INTERSECT = in both: NULL and 2.
Real sqlite3 output:
```
SELECT k FROM P EXCEPT SELECT k FROM Q   -> [(1,)]
SELECT k FROM P INTERSECT SELECT k FROM Q -> [(None,), (2,)]
```
(Row order is not guaranteed in SQL without ORDER BY.)
**Check:** script output above matches the hand set arithmetic.
**Explain simply:**
- EXCEPT = "subtract", INTERSECT = "overlap"; both give distinct rows. (Some products also offer ALL versions that keep duplicates; from memory, not run here.)
- The "NULLs are equal" rule here is a separate convention from `=`: a join on `P.k = Q.k` would not match NULLs.
- Oracle calls EXCEPT `MINUS` (from memory, not run here).
**Likely follow-ups:** 1) *How many rows does `UNION` of P and Q give?* 3: 1, NULL, 2 (hand-checked). 2) *Does `NOT IN` behave the same as EXCEPT?* No: `1 NOT IN (NULL, 2)` is UNKNOWN, so that gets different results when NULL is present.
**Common mistakes / traps:** Thinking NULLs never match and answering INTERSECT = {2}; keeping both NULLs.

### Q37 ⭐⭐ 🔴 Table `A` has `k` values 1, NULL, 2, 2 and table `B` has `k` values 2, NULL, 3. How many rows do `A INNER JOIN B ON A.k = B.k` and `A LEFT JOIN B ON A.k = B.k` return?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know NULL never joins to NULL, and that duplicates multiply in joins.
**Say this in the interview:** "NULL = NULL is not true, so NULLs never match. The two 2s in A each match the one 2 in B, so the inner join gives 2 rows. The left join keeps all 4 rows of A, adding unmatched 1 and NULL with NULLs on the right: 4 rows."
**Answer:** **INNER JOIN: 2 rows. LEFT JOIN: 4 rows.**
**Step-by-step reasoning:**
1. A rows: 1 (no match), NULL (never matches), 2 (matches B's 2), 2 (matches B's 2).
2. Inner join: only matched pairs: (2,2) twice = 2 rows.
3. Left join: every A row appears at least once: 1 and NULL with NULL on the right, plus the two (2,2) = 4 rows.
Real sqlite3 output:
```
A INNER JOIN B -> [(2, 2), (2, 2)]
A LEFT JOIN B  -> [(1, None), (None, None), (2, 2), (2, 2)]
```
**Check:** left join row count = 4 = rows of A, because each A row matches at most one B row here.
**Explain simply:**
- A join condition keeps a pair only if it is TRUE; NULL = NULL is UNKNOWN, so no match.
- A LEFT JOIN keeps every left row; where nothing matches, right columns are NULL.
- If a left row matched several right rows, it would appear several times.
**Likely follow-ups:** 1) *Full outer join rows?* 4 left rows' output plus unmatched B rows NULL and 3: 6 rows (hand-checked, not run). 2) *How to make NULLs match?* Use `A.k = B.k OR (A.k IS NULL AND B.k IS NULL)` (hand-checked; or `IS NOT DISTINCT FROM` where available, from memory).
**Common mistakes / traps:** Counting NULL-NULL as a match (inner = 3); forgetting the 2s duplicate on the left (inner = 1).

### Q38 ⭐ 🟢 A dashboard hides every row where `NOT (region = 'East' OR channel = 'Online')` is false. The rows are (East, Online), (East, Store), (West, Online), (West, Store) as (region, channel). Which rows stay visible?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you apply De Morgan's rule carefully and read "hides when false" correctly (visible means true).
**Say this in the interview:** "Rows with the condition false are hidden, so only rows where it is true stay. NOT (East OR Online) means not East AND not Online, which is only (West, Store)."
**Answer:** **Only (West, Store) stays visible.**
**Step-by-step reasoning:**
1. Visible = condition is TRUE.
2. De Morgan: NOT (A OR B) = (NOT A) AND (NOT B), i.e. region is not East AND channel is not Online.
3. (East, Online): fails both. (East, Store): fails region. (West, Online): fails channel. (West, Store): passes both.
Real sqlite3 output of the condition (1 = true, 0 = false):
```
('East','Online',0) ('East','Store',0) ('West','Online',0) ('West','Store',1)
```
**Check:** the script gives true only for (West, Store).
**Explain simply:**
- De Morgan's laws: "not (A or B)" equals "not A and not B"; "not (A and B)" equals "not A or not B".
- "Hides rows where X is false" is a double negative: the rows you keep are where X is true.
**Likely follow-ups:** 1) *Which rows stay if the condition were `NOT (region = 'East' AND channel = 'Online')`?* Everything except (East, Online) (hand-checked by De Morgan). 2) *Which are hidden here?* The other three.
**Common mistakes / traps:** Reading it as "show rows where it is false" and answering the other three; wrongly turning OR into OR after the NOT.

### Q39 ⭐ 🟢 In Excel, what do `="apple"="APPLE"`, `=EXACT("apple","APPLE")` and `="a"<"B"` return?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know Excel's text comparison ignores case, and the function that does not.
**Say this in the interview:** "The `=` comparison in Excel ignores case, so the first is TRUE. EXACT is case-sensitive, so FALSE. Text comparison is alphabetical and also case-insensitive, so 'a' < 'B' is TRUE."
**Answer:** **TRUE, FALSE, TRUE** (from memory, not run here; confirm in Excel).
**Explain simply:**
- Excel's `=`, `<` and `>` on text ignore uppercase and lowercase; `EXACT(a, b)` is the case-sensitive test.
- Text is compared alphabetically (a, then b, and so on). Excel also treats any text as greater than any number in a comparison (from memory, not run here).
- Other tools differ: in SQLite, `'apple' = 'APPLE'` is false by default, and `'a' < 'B'` is false (it compares character codes, uppercase letters first). I ran this on sqlite3 for the contrast: it is a different tool, not Excel.
**Likely follow-ups:** 1) *How to do a case-sensitive lookup?* Combine EXACT with other functions, or use a helper column (from memory). 2) *What does `="10"=10` return?* FALSE, text versus number (from memory, not run here).
**Common mistakes / traps:** Assuming `=` is case-sensitive like in most programming languages.

### Q40 ⭐ 🟢 Cell A1 holds a number. What does `=IF(A1, "Y", "N")` return when A1 is 0, 2 and -1?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know Excel treats numbers as logical values: zero is FALSE, any non-zero number is TRUE.
**Say this in the interview:** "Excel reads 0 as FALSE and any other number, including negatives, as TRUE. So 0 gives N, 2 gives Y, -1 gives Y."
**Answer:** **0 returns "N"; 2 returns "Y"; -1 returns "Y"** (from memory, not run here; confirm in Excel).
**Explain simply:**
- When the test in IF is a number, Excel converts it: zero means false, non-zero means true.
- Negative numbers are non-zero, so they count as TRUE.
- Text such as "yes" in A1 would give #VALUE! (from memory, not run here).
**Likely follow-ups:** 1) *Blank cell A1?* A blank behaves like 0, so "N" (from memory, not run here). 2) *Safer way to write it?* `=IF(A1<>0, "Y", "N")` makes the intent clear.
**Common mistakes / traps:** Assuming negatives are FALSE (as "less than 1"); assuming only 1 is TRUE.

### Q41 ⭐ 🟢 Access rules: (1) a user who can edit can also view; (2) a user can approve only if the user can edit; (3) Meena cannot view. Using the contrapositive, what can you conclude about Meena's ability to edit and to approve?
**Asked at:** commonly asked (no company-specific report found); conditional and contrapositive reasoning is a standard logical-reasoning topic (prep-site lists, unverified).
**What the interviewer is checking:** Whether you reverse and negate an "if-then" correctly (contrapositive), a valid inference.
**Say this in the interview:** "Rule 1 says edit implies view. Its contrapositive: no view implies no edit. Meena cannot view, so she cannot edit. Rule 2 says approve implies edit; contrapositive: no edit implies no approve. So she cannot approve either."
**Answer:** **Meena cannot edit and cannot approve.**
**Step-by-step reasoning:**
1. Rule 1: Edit then View. Contrapositive: not View then not Edit.
2. Fact: Meena cannot view, so she cannot edit.
3. Rule 2: Approve then Edit. Contrapositive: not Edit then not Approve.
4. She cannot edit, so she cannot approve. The chain: approve then edit then view; no view breaks the chain at the root.
**Check:** brute force over all 8 combinations of (view, edit, approve) true/false that satisfy rules 1 and 2: the only one with view false is (false, false, false) (hand-checked, 3 small steps).
**Explain simply:**
- Contrapositive of "if P then Q" is "if not Q then not P"; it always has the same truth as the original.
- Do not use the converse ("if Q then P") or inverse ("if not P then not Q"); they are not equivalent. For example, "can view" does not imply "can edit".
**Likely follow-ups:** 1) *If Ravi can view, can he edit?* Cannot tell (converse trap). 2) *If Anil can approve?* Then he can edit and view.
**Common mistakes / traps:** Concluding "Meena can edit but not approve"; applying the converse.

### Q42 ⭐ 🟡 Cells A1 and A3 hold TRUE, and A2 is truly empty. What does `=AND(A1:A3)` return, and what does it return if A1:A3 are all empty?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know how Excel's AND treats empty cells in a range and what happens if nothing logical is found.
**Say this in the interview:** "AND ignores empty cells in a range, so it just checks A1 and A3, both TRUE, giving TRUE. If every cell is empty there is nothing to evaluate and Excel returns #VALUE!."
**Answer:** **TRUE for the first formula; #VALUE! for the all-empty range** (from memory, not run here; confirm in Excel).
**Explain simply:**
- In a range reference, AND and OR ignore text and empty cells; only logical values (and numbers, where zero is FALSE) are evaluated. This differs from `=A1*A2*A3`-style arithmetic where empty counts as 0.
- If no logical values are found at all, AND and OR return #VALUE! (from memory, not run here).
- Compare SQL: AND with NULL is UNKNOWN when the other side is TRUE, so Excel's "ignore blanks" is not three-valued logic.
**Likely follow-ups:** 1) *What if A2 holds the text "TRUE"?* Text in a range is ignored (from memory, not run here). 2) *What does `=AND(A1, A2)` with direct reference return?* Written as separate arguments a blank is typically treated as 0 (FALSE) (from memory, not run here, confirm).
**Common mistakes / traps:** Assuming blank counts as FALSE and answering FALSE; assuming all-empty AND returns TRUE (empty "all" is TRUE in math, but not in Excel).

### Q43 ⭐ 🟡 Trace the pseudocode and give the printed value (`DIV` is integer division):
```
n = 1234
s = 0
WHILE n > 0
    s = s + (n MOD 10) * 2
    n = n DIV 10
PRINT s
```
**Asked at:** commonly asked (no company-specific report found); pseudocode output-tracing MCQs are reported on prep sites for service-company aptitude sets (unverified).
**What the interviewer is checking:** Whether you can follow a loop step by step without skipping an iteration.
**Say this in the interview:** "MOD 10 picks the last digit, DIV 10 chops it off. So the loop doubles each digit and adds them up. Digits 4, 3, 2, 1 give 8 + 6 + 4 + 2 = 20."
**Answer:** **20**
**Step-by-step reasoning:** (`MOD` is the remainder after division; `DIV` throws the remainder away.)
1. Write a small table of n and s after each pass.

| Pass | last digit (n MOD 10) | s after | n after |
|---|---|---|---|
| start | | 0 | 1234 |
| 1 | 4 | 8 | 123 |
| 2 | 3 | 14 | 12 |
| 3 | 2 | 18 | 1 |
| 4 | 1 | 20 | 0 |

2. n = 0 so `n > 0` is false and the loop stops. PRINT s gives 20.
**Fast method (30 seconds):** Spot the pattern: the loop visits every digit once, so the answer is 2 x (digit sum) = 2 x (1+2+3+4) = 20.
**Check:** Verified by script (the same loop gave 20 with the table above).
**Explain simply:**
- A "trace" means playing computer: write the variable values after every pass.
- The loop ends when its condition turns false, here when n reaches 0.
**Likely follow-ups:** 1) *What if n = 0 at the start?* The loop body never runs and it prints 0. 2) *What if the line were `s = s + n MOD 10`?* It would print the plain digit sum, 10.
**Common mistakes / traps:** Stopping one pass early; forgetting the "x 2"; reading `n DIV 10` as decimal division (123.4).

### Q44 ⭐ 🟡 Trace this flowchart and give the two printed values (`DIV` is integer division):
```
1  START: x = 100, k = 0
2  IF x < 10 THEN GO TO 5
3  x = x DIV 3 ; k = k + 1
4  GO TO 2
5  PRINT x, k
```
**Asked at:** commonly asked (no company-specific report found); flowchart tracing is reported on prep sites for TCS, Infosys, Accenture and Cognizant style sets (unverified).
**What the interviewer is checking:** Following jumps (GO TO) and testing the exit condition each time.
**Say this in the interview:** "Line 2 is the exit test, lines 3 and 4 loop back to it. I divide by 3 until x is below 10: 100, 33, 11, 3. That is 3 divisions, so it prints 3 and 3."
**Answer:** **x = 3 and k = 3 (printed as "3 3")**
**Step-by-step reasoning:**
1. x = 100, k = 0. Is 100 < 10? No, so go to line 3.
2. x = 33, k = 1. Is 33 < 10? No.
3. x = 11, k = 2. Is 11 < 10? No.
4. x = 3, k = 3. Is 3 < 10? Yes, jump to line 5.
5. PRINT 3, 3.
**Fast method (30 seconds):** Note the test comes BEFORE the division, so 11 is still divided once more even though it is close to 10. Write one line per pass: (100,0) (33,1) (11,2) (3,3).
**Check:** Verified by script (same four states).
**Explain simply:**
- `IF ... THEN GO TO 5` means "leave the loop"; `GO TO 2` means "test again".
- Integer division drops the fraction: 100 DIV 3 = 33, not 33.33.
**Likely follow-ups:** 1) *If the start were x = 9?* The test passes at once, nothing is divided, and it prints 9 and 0. 2) *If the test were x <= 11?* It would stop at x = 11, k = 2.
**Common mistakes / traps:** Using decimal division; counting k from 1; stopping at 11 because it "looks small enough".

### Q45 ⭐ 🟡 How many times does the body run in `FOR i = 1 TO n STEP 2` when n = 10, n = 1 and n = 0? Why do such off-by-one checks matter in edge-case testing?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Boundary thinking: loops that run zero times or an odd count.
**Say this in the interview:** "i takes 1, 3, 5 and so on while i is at most n. For n = 10 that is 1, 3, 5, 7, 9, which is 5 runs; for n = 1 it is 1 run; for n = 0 the loop never starts, so 0 runs."
**Answer:** **n = 10: 5 times; n = 1: 1 time; n = 0: 0 times.**
**Step-by-step reasoning:**
1. Assumption (standard for FOR loops): the loop runs while i <= n, and a loop whose start is already beyond n runs zero times.
2. n = 10: i = 1, 3, 5, 7, 9 (11 is above 10): 5 runs.
3. n = 1: i = 1 only: 1 run.
4. n = 0: start value 1 is above 0: 0 runs.
5. Formula for positive n: runs = (n + 1) DIV 2 (gives 5, 1, 0).
**Check:** Verified by script (Python range(1, n+1, 2) gave lengths 5, 1, 0).
**Explain simply:**
- An "off-by-one error" is being wrong by exactly one step at an edge, for example processing 9 rows when there are 10.
- The empty case (zero runs) and the single case are where code and formulas most often break, so testers try them first.
- In reporting terms: a monthly loop over 0 months, or a range that includes or excludes the last day, are the same kind of edge.
**Likely follow-ups:** 1) *n = 11?* i = 1, 3, 5, 7, 9, 11: 6 runs. 2) *If the loop were `FOR i = 1 TO n` with STEP 1 and n = 10?* 10 runs.
**Common mistakes / traps:** Answering n / 2 = 5 for n = 1 (gives 0.5); forgetting the end value is included when it is reachable (n = 11); assuming a loop always runs at least once.

### Q46 ⭐ 🟡 How many of the 16 combinations of Boolean inputs A, B, C and D make `(A OR B) AND (C OR D)` true?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Counting truth-table rows by structure instead of listing all 16.
**Say this in the interview:** "(A OR B) is false only when both are false, so it is true in 3 of 4 combinations. Same for (C OR D). The two pairs are independent, so 3 x 3 = 9."
**Answer:** **9 of the 16 combinations**
**Step-by-step reasoning:**
1. Pair (A, B) has 4 combinations: 00, 01, 10, 11. `A OR B` is true in 01, 10, 11, so 3.
2. Pair (C, D) works the same way: 3 true.
3. `AND` needs both parts true, and the pairs do not affect each other, so multiply: 3 x 3 = 9.
4. Cross-check by complement: the formula is false in 16 - 9 = 7 combinations (whenever A and B are both false, or C and D are both false: 4 + 4 - 1 = 7).
**Check:** Verified by script (looped over all 16 combinations: 9 true).
**Explain simply:**
- OR is true if at least one input is true; AND is true only if both sides are true.
- When two conditions use different inputs, you can count each separately and multiply.
**Likely follow-ups:** 1) *How many make `(A AND B) OR (C AND D)` true?* 7 (verified by script; hand check: 4 + 4 - 1 by inclusion and exclusion). 2) *With 3 inputs per side, `(A OR B OR C) AND (D OR E OR F)`?* 7 x 7 = 49 of 64 (verified by script).
**Common mistakes / traps:** Adding 3 + 3 = 6; counting only the all-true row; forgetting that "OR" includes both-true.

### Q47 ⭐ 🟡 For `SELECT 100 + NULL`, `SELECT COALESCE(NULL, NULL, 7)`, `SELECT NULLIF(5, 5)` and `SELECT NULLIF(5, 6)`, what does each return?
**Asked at:** commonly asked (no company-specific report found); NULL handling is a standard SQL interview topic (prep and reference sites, unverified for specific companies).
**What the interviewer is checking:** Whether you know NULL poisons arithmetic and how COALESCE and NULLIF work.
**Say this in the interview:** "Anything plus NULL is NULL, because NULL means unknown. COALESCE returns the first non-NULL value, so 7. NULLIF returns NULL when the two values are equal, otherwise the first value: NULL and 5."
**Answer:** **NULL; 7; NULL; 5**
**Step-by-step reasoning:** Real output on Python sqlite3 (Python `None` is how it shows SQL NULL):
```
SELECT 100 + NULL                -> [(None,)]
SELECT COALESCE(NULL, NULL, 7)   -> [(7,)]
SELECT NULLIF(5, 5)              -> [(None,)]
SELECT NULLIF(5, 6)              -> [(5,)]
```
1. NULL = "value unknown". 100 plus an unknown is unknown.
2. COALESCE(a, b, c) walks left to right and returns the first value that is not NULL.
3. NULLIF(a, b) returns NULL if a = b, else a.
**Check:** Run on sqlite3 (output above). These four behave the same in PostgreSQL and other standard-following databases (from memory, not run here).
**Explain simply:**
- NULL is "no known value", not zero and not an empty string.
- COALESCE fills gaps: `COALESCE(bonus, 0)` treats a missing bonus as 0.
- NULLIF avoids divide-by-zero: `x / NULLIF(y, 0)` gives NULL instead of an error when y is 0.
**Likely follow-ups:** 1) *What does `SELECT 100 + COALESCE(NULL, 0)` give?* 100. 2) *`SELECT NULLIF('', '')`?* NULL (two equal values).
**Common mistakes / traps:** Thinking 100 + NULL = 100; thinking NULLIF(5, 5) returns 0 or 5.

### Q48 ⭐ 🟡 A query is `SELECT CASE WHEN bonus = NULL THEN 'Missing' ELSE 'Present' END`. What does it return for bonus values NULL, 0 and 500, and how should the condition be written?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The classic "= NULL never matches" trap.
**Say this in the interview:** "bonus = NULL is never true, it is UNKNOWN, so CASE falls to ELSE and every row says Present, even the NULL one. The condition must be bonus IS NULL."
**Answer:** **All three return 'Present'. Write `WHEN bonus IS NULL THEN 'Missing'`.**
**Step-by-step reasoning:** Real output on Python sqlite3 (a three-row table with bonus NULL, 0, 500):
```
Wrong : CASE WHEN bonus = NULL ...
[(None, 'Present'), (0, 'Present'), (500, 'Present')]
Right : CASE WHEN bonus IS NULL ...
[(None, 'Missing'), (0, 'Present'), (500, 'Present')]
```
1. `bonus = NULL` compares with an unknown value, so the result is UNKNOWN for every row, including the NULL one.
2. CASE takes a WHEN branch only if its condition is TRUE. UNKNOWN is not TRUE, so ELSE runs.
3. `IS NULL` is the special test that returns TRUE or FALSE only.
**Check:** Run on sqlite3 (output above).
**Explain simply:**
- You cannot ask "is unknown equal to unknown?" and get yes; the honest answer is "don't know".
- Use `IS NULL` and `IS NOT NULL` for blank checks.
- Careful: 0 is a real value (a bonus of zero), not "Missing".
**Likely follow-ups:** 1) *Would `bonus <> NULL` work?* No, also UNKNOWN for every row. 2) *Safe one-liner?* `CASE WHEN bonus IS NULL THEN 'Missing' ELSE 'Present' END` or `COALESCE(bonus, -1)`.
**Common mistakes / traps:** Expecting 'Missing' for the NULL row; treating 0 as missing; believing the query errors (it runs quietly with the wrong answer, which is why it is dangerous).

### Q49 ⭐ 🟡 Table `candidates` has an `email` column holding: a@x.com, b@x.com, a@x.com, c@x.com, b@x.com, a@x.com, NULL, NULL. How many rows does `SELECT email, COUNT(*) FROM candidates GROUP BY email HAVING COUNT(*) > 1` return, and which of them is a trap for a duplicate check?
**Asked at:** commonly asked (no company-specific report found); duplicate-finding with GROUP BY and HAVING is a standard SQL interview task (unverified for specific companies).
**What the interviewer is checking:** Knowing that GROUP BY puts all NULLs into one group.
**Say this in the interview:** "It returns 3 rows: a@x.com with 3, b@x.com with 2, and NULL with 2. The NULL row is the trap: two missing emails are not duplicates of each other, they are just missing."
**Answer:** **3 rows: a@x.com (3), b@x.com (2) and NULL (2). The NULL row is the trap.**
**Step-by-step reasoning:** Real output on Python sqlite3:
```
GROUP BY email HAVING COUNT(*) > 1:
[(None, 2), ('a@x.com', 3), ('b@x.com', 2)]
All groups: [(None, 2), ('a@x.com', 3), ('b@x.com', 2), ('c@x.com', 1)]
With WHERE email IS NOT NULL:
[('a@x.com', 3), ('b@x.com', 2)]
```
1. GROUP BY treats all NULLs as one group (a special rule, even though NULL = NULL is not true elsewhere).
2. COUNT(*) counts rows, so the NULL group has 2.
3. c@x.com appears once, so HAVING removes it. Three groups remain.
4. A real duplicate check should filter out NULLs first: `WHERE email IS NOT NULL`, leaving 2 rows.
**Check:** Run on sqlite3 (output above). Same GROUP BY rule in standard SQL (from memory for other databases, not run here).
**Explain simply:**
- GROUP BY "groups alike things"; for this purpose it treats NULLs as alike.
- `COUNT(*)` counts rows; `COUNT(email)` counts only non-NULL emails (here 6 versus 8 rows).
- Missing data and duplicate data are different problems; report them separately.
**Likely follow-ups:** 1) *How many distinct emails?* `COUNT(DISTINCT email)` = 3 (NULLs ignored). 2) *How would you list the duplicate rows themselves?* Join back to the grouped result or use a window function (not run here).
**Common mistakes / traps:** Answering 2 (forgetting the NULL group); calling the NULL pair "duplicates" and deleting them.

### Q50 ⭐ 🟡 What does `=IFS(A1>10,"High", A1>5,"Mid")` return when A1 is 12, 7 and 3, and how do you add a default result?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowing IFS has no built-in "else" and returns an error if nothing matches.
**Say this in the interview:** "It reads the tests left to right and returns the first match: 12 gives High, 7 gives Mid, and 3 matches nothing so Excel shows #N/A. For a default, add a last test of TRUE with the default value."
**Answer:** **12 returns "High"; 7 returns "Mid"; 3 returns #N/A. Default: `=IFS(A1>10,"High", A1>5,"Mid", TRUE,"Low")`.**
**Step-by-step reasoning:** (Excel was not available here; this is from memory, not run here; confirm in Excel. I only checked the first-match logic with a small Python imitation.)
1. A1 = 12: first test 12>10 is TRUE, so "High" (later tests are not used).
2. A1 = 7: 7>10 is FALSE; 7>5 is TRUE, so "Mid".
3. A1 = 3: both are FALSE; no pair matches, so IFS returns the #N/A error.
4. Adding the pair `TRUE,"Low"` at the end always matches when nothing earlier did.
**Fast method (30 seconds):** Put the strictest test first; order matters because the first TRUE wins.
**Check:** First-match logic checked with a small Python imitation (High, Mid, none); the #N/A result itself is from memory, not run here.
**Explain simply:**
- IFS is a tidier nested IF; it has no "otherwise" slot.
- `TRUE` as a test means "always yes", so it works as the default.
**Likely follow-ups:** 1) *What if the tests were in the order A1>5 then A1>10?* 12 would return "Mid", wrong; order matters. 2) *Alternative to IFS?* Nested IF, where the last value is the default.
**Common mistakes / traps:** Expecting a blank or 0 for 3; putting the broader test first; thinking IFS evaluates all tests and picks the best.

### Q51 ⭐ 🟡 Apply one pass of bubble sort (compare each adjacent pair from left to right and swap if the left value is larger) to the list [5, 2, 4, 1, 3]. What is the list after the pass, and how many swaps happened?
**Asked at:** commonly asked (no company-specific report found); sorting traces appear in pseudocode-style prep material (unverified).
**What the interviewer is checking:** Careful step-by-step execution of a defined procedure.
**Say this in the interview:** "I walk the list once comparing neighbours. The 5 keeps getting swapped to the right until it hits the end. Result [2, 4, 1, 3, 5] with 4 swaps."
**Answer:** **[2, 4, 1, 3, 5] after 4 swaps**
**Step-by-step reasoning:**
1. Compare 5 and 2: 5 > 2, swap: [2, 5, 4, 1, 3] (swap 1)
2. Compare 5 and 4: swap: [2, 4, 5, 1, 3] (swap 2)
3. Compare 5 and 1: swap: [2, 4, 1, 5, 3] (swap 3)
4. Compare 5 and 3: swap: [2, 4, 1, 3, 5] (swap 4)
5. A pass has n - 1 = 4 comparisons; all 4 led to swaps because the largest value started at the front.
**Fast method (30 seconds):** One pass carries the largest value to the end; the others shift left by one only where the large value passed them.
**Check:** Verified by script (same four intermediate lists).
**Explain simply:**
- Bubble sort repeatedly compares neighbours; big values "bubble" to the right.
- After one pass only the last position is guaranteed to be correct, the list is not fully sorted yet.
**Likely follow-ups:** 1) *How many passes to fully sort this list?* 3 passes (verified by script; a list of 5 needs at most 4). 2) *Pass on an already sorted list?* 4 comparisons, 0 swaps.
**Common mistakes / traps:** Giving the fully sorted list [1, 2, 3, 4, 5]; swapping 2 and 4 after they are already in order; counting comparisons (4) and swaps (4) as the same thing in general (here they coincide only by luck).

### Q52 ⭐ 🟡 How many rows does the truth table of a formula with 5 Boolean variables have, and how many different Boolean functions of 2 variables exist?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you see the powers of two behind truth tables.
**Say this in the interview:** "Each variable is true or false, so 5 variables give 2 to the power 5 = 32 rows. With 2 variables there are 4 rows, and each row's output can be 0 or 1 independently, so 2 to the power 4 = 16 different functions."
**Answer:** **32 rows; 16 Boolean functions of 2 variables.**
**Step-by-step reasoning:**
1. Rows = 2^n for n variables: 2^5 = 32.
2. Two variables have 2^2 = 4 input rows.
3. A function chooses an output (0 or 1) for each of the 4 rows: 2^4 = 16.
4. These 16 include AND, OR, XOR, NAND, NOR, "always true" and "always false".
**Fast method (30 seconds):** Each extra variable doubles the rows; each extra row doubles the number of possible functions.
**Check:** Verified by script (32 = 2**5; 16 = 2**(2**2); product of 4 binary inputs lists 16 rows as a sanity test).
**Explain simply:**
- Truth table: a list of every combination of inputs with the formula's result.
- The number of functions grows very fast: 3 variables give 2^8 = 256 functions (hand-checked).
**Likely follow-ups:** 1) *How many rows for 10 variables?* 1,024. 2) *Why test all rows of a real rule?* To catch combinations nobody thought of.
**Common mistakes / traps:** Answering 5 x 5 = 25 or 10 for rows; answering 4 (rows) for the function count.

### Q53 ⭐ 🟡 In Excel, what do `="10">9`, `="10">"9"` and `=10>9` return, and what rule explains the first two?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness that text and numbers compare differently, a common cause of wrong filters when numbers are stored as text.
**Say this in the interview:** "The first is TRUE because Excel ranks any text above any number. The second is FALSE because both are text and compare character by character, and '1' comes before '9'. The third is plain numbers: TRUE."
**Answer:** **TRUE, FALSE, TRUE.** (From memory, not run here; Excel was not available. Confirm in Excel.)
**Step-by-step reasoning:**
1. `="10">9`: "10" in quotes is text, 9 is a number. Excel's ordering is numbers < text < logical values, so text is greater than any number: TRUE.
2. `="10">"9"`: both are text. Text compares character by character from the left: "1" versus "9". "1" is smaller, so "10" is not greater than "9": FALSE.
3. `=10>9`: both numbers, 10 is bigger: TRUE.
**Check:** Not run here (Excel unavailable); stated from memory of Excel's documented comparison order. Verify in the tool.
**Explain simply:**
- Quotes make text. A number stored as text (for example an imported ID or salary) sorts and compares like text.
- Look for numbers aligned to the left of a cell or a small green triangle as hints, and convert with `VALUE()`.
**Likely follow-ups:** 1) *Fix for the second formula?* `=VALUE("10")>VALUE("9")` returns TRUE (from memory, not run here). 2) *Do SQL databases do the same?* Not necessarily; many convert or raise an error, so test in your database.
**Common mistakes / traps:** Expecting "10" > "9" to be TRUE because 10 is bigger as a number; assuming Excel converts quoted numbers automatically in comparisons.

### Q54 ⭐ 🟡 In PostgreSQL, what do `SELECT 7/2`, `SELECT 7.0/2` and `SELECT -7/2` return?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Integer versus decimal division, a silent source of wrong rates and percentages.
**Say this in the interview:** "Two whole numbers give a whole-number result, cut towards zero: 7/2 is 3 and -7/2 is -3. If one side has a decimal, the result is a decimal: 7.0/2 is 3.5. To be safe I add a decimal or a cast."
**Answer:** **3; 3.5 (shown as 3.5000000000000000 in PostgreSQL); -3.** (PostgreSQL was not available here; this is from memory, not run here. Confirm in the tool.)
**Step-by-step reasoning:**
1. `7/2`: both integers, so integer division; the fraction is dropped: 3.
2. `7.0/2`: 7.0 is a decimal (numeric) value, so the answer is numeric: 3.5 (PostgreSQL prints extra zeros).
3. `-7/2`: integer division truncates towards zero, so -3, not -4 (not "floor").
**Check:** I ran the same three on Python sqlite3 as a related, not identical, test. Real output: `[(3, 3.5, -3)]`. SQLite happens to give the same values; the PostgreSQL display of 3.5 is from memory. Dialects differ in other places, for example some databases return decimals for 7/2 (from memory, not run here).
**Explain simply:**
- "Integer division" throws away the remainder instead of rounding.
- It matters in HR rates: `leavers / headcount` with two integer columns gives 0 for any rate below 100%.
- Fix: `leavers * 1.0 / headcount` or `CAST(leavers AS numeric) / headcount`.
**Likely follow-ups:** 1) *How do I get the remainder?* `7 % 2` gives 1 (from memory, not run here). 2) *What does floor division of -7/2 give in Python?* -4 (checked in Python: `-7 // 2`), unlike PostgreSQL's -3.
**Common mistakes / traps:** Answering 3.5 for the first; answering -4 for the third; computing percentages with two integer columns and getting 0.

### Q55 ⭐ 🟡 A data-quality rule list for attrition reporting is: attrition % = leavers / average headcount x 100. Name at least five edge cases you would test before trusting this formula in a report.
**Asked at:** commonly asked (no company-specific report found); a HR-analytics reporting judgement question (our own construction, no source claim).
**What the interviewer is checking:** Whether you can anticipate data and logic edge cases, not only compute the formula.
**Say this in the interview:** "I would test zero headcount, a missing headcount, an average built from the wrong periods, people who joined and left in the same period, and leavers counted twice or outside the period. I also check integer division and what counts as a leaver."
**Answer:** **At least these eight edge cases, grouped below.** Priorities are our suggestion.
**Step-by-step reasoning:**
1. **Zero average headcount** (a new or closed team): division by zero. Use `NULLIF(avg_headcount, 0)` to return NULL instead of an error.
2. **Missing (NULL) headcount** in some months: the average silently ignores NULLs; decide whether that is right.
3. **Integer division:** two integer columns can give 0 for any rate below 100% in many databases. Cast one side to decimal.
4. **Same-period joiners and leavers:** someone who joined and left within the period appears in leavers but may not be in the opening or closing headcount.
5. **Definition of "average headcount":** (opening + closing) / 2 versus a 12-month average give different answers; report which one you used.
6. **Duplicates and re-hires:** the same person counted as a leaver twice, or a rehire counted as new.
7. **Period mismatch:** leavers counted for 12 months but headcount for one month, so the rate is not comparable; annualising a short period must be explicit.
8. **Who counts as a leaver:** voluntary vs involuntary, transfers, contractors, retirements; and leavers with exit dates outside the period or in the future.
**Worked mini-example (sqlite3 run, my own two-row demo):** January headcount 100, February headcount 0, 5 leavers each month.
```
SELECT d, 5*100.0/hc, 5*100.0/NULLIF(hc,0), 5*100/hc FROM h
[('Jan', 5.0, 5.0, 5), ('Feb', None, None, None)]
```
SQLite returns NULL for division by zero; PostgreSQL raises an error (from memory, not run here), so guard with NULLIF either way.
**Explain simply:**
- An edge case is an unusual input where a formula that works on normal data can break.
- Attrition is a ratio, so both parts (top and bottom) need clear definitions.
**Likely follow-ups:** 1) *A team of 3 people with 1 leaver shows 33%. Is that a problem?* Not an error, but a small base makes the percentage swing; show counts beside it. 2) *Attrition above 100%?* Possible if many leave and are replaced within a period; check it is real.
**Common mistakes / traps:** Listing only "divide by zero"; not stating the definition of average headcount; reporting a percentage without the numbers behind it.

### Q56 ⭐ 🟡 How do you trace a pseudocode or flowchart question quickly and accurately in an online test (what do you write down, when do you stop, and which traps do you check)?
**Asked at:** commonly asked (no company-specific report found); pseudocode and flowchart tracing questions are reported on prep sites for several service-company tests (unverified).
**What the interviewer is checking:** A calm, repeatable method for following code by hand.
**Say this in the interview:** "I write a small table with a column for each variable and one row per pass, update it line by line, and stop when the loop condition is false. Before I answer I check the first and last pass, integer division, and what exactly gets printed."
**Answer:** **Use a variable table, one row per pass, follow the exit condition exactly, then run a short trap checklist. Our suggestion, not a research result.**
**Worked mini-example (verified by script):** Q43's loop: n = 1234. Table rows (n, s): (123, 8), (12, 14), (1, 18), (0, 20). Stop because n > 0 is false; print 20. Q44: (x, k) rows (100,0) (33,1) (11,2) (3,3); the test is before the division, so print 3 and 3.
**Method:**
1. **Write down** all variables with their start values in column headings (pencil on scratch paper, or the on-screen notepad).
2. **One row per pass:** copy the values after the last line of the body, not halfway.
3. **Read the loop test first:** is it checked before the body (WHILE) or after (REPEAT-UNTIL)? Is it `<` or `<=`?
4. **Stop** the moment the exit condition becomes false; do not do "one more for luck".
5. **Check the print line:** is PRINT inside the loop (prints many times) or after it (once)? Print order matters.
6. **Trap checklist:** integer division and MOD (7 DIV 2 = 3, 7 MOD 2 = 1); off-by-one at the first and last pass; variables updated in the wrong order (use the old value on the right-hand side); STEP size; a loop that runs zero times; nested loops (inner restarts fully each outer pass).
7. **Time rule of thumb (our suggestion):** if the loop would run more than about 10 or 15 passes, look for a pattern (digit sum, doubling, arithmetic series) instead of tracing everything, then confirm with the first two and last two passes.
**Explain simply:**
- A trace means acting like the computer: do exactly what the line says, nothing smarter.
- The table is your memory; the mistakes come from doing it in your head.
**Likely follow-ups:** 1) *What if the answer choices are close?* Trace the two edge inputs (smallest and largest) to eliminate options. 2) *What if there is a recursion?* Same table, one row per call, then unwind the returns (not shown here).
**Common mistakes / traps:** Tracing in your head; ignoring whether the test is before or after the body; using the new value of a variable too early within a line; printing the value after one extra pass.

### Q57 ⭐ 🟡 How would you explain the `NOT IN` NULL trap to a non-technical manager, and what are two safe rewrites?
**Asked at:** commonly asked (no company-specific report found); the NOT IN with NULL trap is a standard item in SQL interview lists (prep-site and technical-blog claim, unverified).
**What the interviewer is checking:** Whether you understand three-valued logic well enough to explain it without jargon, and whether you know the safe patterns.
**Say this in the interview:** "NULL means 'unknown', not 'empty'. `NOT IN` asks 'is this value different from every value on the list?' If one value on the list is unknown, I can never be sure, so the answer is 'unknown' for everyone and the query returns nothing. I use `NOT EXISTS`, or I filter the NULLs out of the list."
**Answer:** **A single NULL in the `NOT IN` list makes every comparison "unknown", so the query silently returns zero rows. Two safe rewrites: `NOT EXISTS`, or `NOT IN` with `WHERE ... IS NOT NULL` inside the subquery (a `LEFT JOIN ... IS NULL` also works).**
**Explain simply:**
- Manager story (our wording): "You have a list of 4 employees. HR gives you a list of people who resigned: Bala, and one name that is blank because the form was not filled. You ask: who is NOT on the resigned list? The blank might be Asha, or Chitra, or anybody. You cannot honestly say any of them is safe, so the system answers 'cannot tell' for everyone." The report shows nothing, with no error message, which is why it is dangerous.
- Technical reason: `x NOT IN (2, NULL)` is the same as `x <> 2 AND x <> NULL`. The second part is UNKNOWN (never TRUE), so the whole condition is FALSE or UNKNOWN. `WHERE` keeps only rows that are TRUE.
- `NOT EXISTS` works because it asks "does a matching row exist?" and only tests rows where the ids actually match. NULL never matches, so it is simply ignored.

Worked example (run on Python sqlite3). Tables: `employees` has ids 1 to 4 (Asha, Bala, Chitra, Dev); `resigned` has ids 2 and NULL.
```sql
-- The trap: one NULL in the list
SELECT name
FROM employees
WHERE emp_id NOT IN (SELECT emp_id FROM resigned);

-- Safe rewrite 1: drop the NULLs from the list
SELECT name
FROM employees
WHERE emp_id NOT IN (SELECT emp_id FROM resigned WHERE emp_id IS NOT NULL);

-- Safe rewrite 2: NOT EXISTS
SELECT name
FROM employees AS e
WHERE NOT EXISTS (SELECT 1 FROM resigned AS r WHERE r.emp_id = e.emp_id);
```
Real output: the trap returns `[]` (no rows); rewrite 1 returns `Asha, Chitra, Dev`; rewrite 2 returns `Asha, Chitra, Dev`. (A `LEFT JOIN resigned ... WHERE r.emp_id IS NULL` also returned `Asha, Chitra, Dev`.) The fixed versions give the expected "everyone except Bala".
**Likely follow-ups:** 1) *Does `IN` have the same trap?* No: `x IN (2, NULL)` is TRUE when x is 2, and UNKNOWN otherwise, which `WHERE` drops, which is what you wanted anyway. The trap only bites when you negate. 2) *Which rewrite do you prefer?* `NOT EXISTS`, because it stays correct even if a NULL appears later; the `IS NOT NULL` filter must be remembered every time.
**Common mistakes / traps:** Testing the query on clean data with no NULLs and trusting it; the trap appears only when a NULL arrives later. Also, writing `<> NULL` or `NOT IN (NULL)` by hand: both return nothing.

### Q58 ⭐ 🔴 A record is valid only if both rules hold: (1) if status = 'Closed' then close_date is not NULL; (2) if close_date is not NULL then amount > 0.

| Record | Status | close_date | Amount |
|---|---|---|---|
| R1 | Closed | 2025-03-01 | 0 |
| R2 | Open | NULL | 0 |
| R3 | Closed | NULL | 100 |
| R4 | Open | 2025-04-10 | 50 |
| R5 | Closed | 2025-05-02 | 20 |

Which records are invalid, and which rule does each break?
**Asked at:** commonly asked (no company-specific report found); "if-then" rule checking is a standard data-validation exercise (no company report in the sources file).
**What the interviewer is checking:** Whether you know that an "if P then Q" rule is broken only when P is true and Q is false.
**Say this in the interview:** "An if-then rule fails only when the 'if' part is true and the 'then' part is false. R1 has a close date but amount 0, so rule 2 fails. R3 is Closed but has no close date, so rule 1 fails. The other three pass. R2 passes both rules because its 'if' parts are false."
**Answer:** **Invalid: R1 (breaks rule 2) and R3 (breaks rule 1). Valid: R2, R4, R5.**
**Step-by-step reasoning:**
1. Rule 1 is broken only if status is Closed AND close_date is NULL. Only R3 matches.
2. Rule 2 is broken only if close_date is not NULL AND amount is not above 0. Only R1 matches (date present, amount 0).
3. R2: status Open, so rule 1's "if" is false (rule holds). close_date is NULL, so rule 2's "if" is false (rule holds). Valid, even though amount is 0.
4. R4: Open, date present, amount 50 above 0: both rules hold. R5: Closed, date present, amount 20: both hold.

| Record | Rule 1 | Rule 2 | Result |
|---|---|---|---|
| R1 | holds | **broken** | invalid |
| R2 | holds (if false) | holds (if false) | valid |
| R3 | **broken** | holds (if false) | invalid |
| R4 | holds | holds | valid |
| R5 | holds | holds | valid |
**Fast method (30 seconds):** Turn each rule into the one situation that breaks it ("Closed but no date"; "has date but amount 0 or less") and scan the table for only those two situations.
**Check:** Verified by script on sqlite3: a `CASE` for "status = 'Closed' AND close_date IS NULL" flagged only R3, and "close_date IS NOT NULL AND NOT amount > 0" flagged only R1.
**Explain simply:**
- "If P then Q" is the same as "NOT P OR Q". It is only false when P is true and Q is false.
- When the "if" part is false, the rule is "vacuously true": nothing is required of the record.
- Rule 2 does not say Open records need amount above 0; so R2 with amount 0 is allowed by these two rules.

Real SQL for the checks (sqlite3 output: R1 flagged for rule 2, R3 flagged for rule 1, nothing else):
```sql
-- Flag records that break each rule
SELECT record,
       CASE WHEN status = 'Closed' AND close_date IS NULL
            THEN 'breaks rule 1' END AS rule_1_check,
       CASE WHEN close_date IS NOT NULL AND NOT amount > 0
            THEN 'breaks rule 2' END AS rule_2_check
FROM records;
```
**Likely follow-ups:** 1) *Is R2 really fine?* Under these two rules yes; a business might add a third rule (for example "amount must be above 0 for every record") and then R2 would fail. Say so, and ask. 2) *What if close_date could hold NULL and status were also NULL?* `status = 'Closed'` becomes UNKNOWN; decide explicitly with `COALESCE` or an `IS NULL` check.
**Common mistakes / traps:** Marking R2 invalid because amount is 0 (rule 2 never applies to it); thinking rule 1 also demands that Open records have no date (the converse is not stated, so R4 is fine).

### Q59 ⭐ 🔴 A decision table has three Yes/No conditions (C1, C2, C3) and three rules, where `-` means "does not matter": Rule 1 = (Y, Y, -), Rule 2 = (Y, -, Y), Rule 3 = (N, -, -). How many of the 8 combinations are covered by at least one rule, which combination is covered by two rules (a conflict risk), and which one is not covered?
**Asked at:** commonly asked (no company-specific report found); completeness and conflict checks are standard in decision-table testing guides (BrowserStack, Visual Paradigm and similar, unverified snippets).
**What the interviewer is checking:** Whether you can expand "don't care" entries and check completeness and overlap, not just read the table.
**Say this in the interview:** "I expand each dash into both Y and N and list every combination each rule covers. Rule 1 covers YYY and YYN, Rule 2 covers YYY and YNY, Rule 3 covers all four N-starting ones. Seven are covered, YYY is covered twice, and YNN is not covered."
**Answer:** **7 of 8 combinations are covered; YYY is covered by Rules 1 and 2 (conflict risk); YNN is covered by no rule.**
**Step-by-step reasoning:**
1. Rule 1 (Y, Y, -): C3 free, so YYY and YYN.
2. Rule 2 (Y, -, Y): C2 free, so YYY and YNY.
3. Rule 3 (N, -, -): C2 and C3 free, so NYY, NYN, NNY, NNN (4 combinations).
4. Union: YYY, YYN, YNY, NYY, NYN, NNY, NNN = 7.

| C1 C2 C3 | Rules covering it |
|---|---|
| YYY | 1 and 2 (overlap) |
| YYN | 1 |
| YNY | 2 |
| **YNN** | **none (gap)** |
| NYY | 3 |
| NYN | 3 |
| NNY | 3 |
| NNN | 3 |
**Fast method (30 seconds):** Count "free" dashes: a rule with k dashes covers 2^k combinations. Here 2 + 2 + 4 = 8 slots, but 8 slots minus 1 duplicate (YYY counted twice) = 7 distinct, so exactly 1 combination is missing. Then find which by listing.
**Check:** Verified by script: each of the 8 combinations was tested against all three rules; the output matched the table above.
**Explain simply:**
- A decision table is a grid of conditions and the action to take; "-" means that condition does not change the outcome.
- Gap: a case no rule handles (the system has no defined answer). Overlap: a case two rules handle; harmless only if both give the same action.
- A good table has a default ("otherwise") rule so gaps cannot happen silently.
**Likely follow-ups:** 1) *What if Rule 2 were (Y, N, Y)?* Then there is no overlap: Rule 2 covers only YNY; YYY is covered only by Rule 1; the gap YNN remains, so 7 are still covered (YYY, YYN, YNY, plus four N-cases). 2) *How would you close the gap?* Add Rule 4 = (Y, N, N) or a default rule.
**Common mistakes / traps:** Counting 2 + 2 + 4 = 8 and declaring the table complete; that ignores the double-counted YYY.

### Q60 ⭐ 🔴 A nightly load failed in exactly one step: Extract, Transform or Load. Three analysts speak. Asha: "It was Transform or Load." Bala: "It was not Load." Chitra: "It was Extract." Exactly one of the three statements is true. Which step failed, and whose statement is true?
**Asked at:** commonly asked (no company-specific report found); "exactly one statement is true" puzzles are a classic reasoning format.
**What the interviewer is checking:** Systematic case testing: assume each possibility, count true statements, keep only the case that fits the stated condition.
**Say this in the interview:** "Only three possible failures, so I test each. If Extract failed, Bala and Chitra are both true: two truths, rejected. If Transform failed, Asha and Bala are both true: rejected. If Load failed, only Asha is true: exactly one. So Load failed and Asha is right."
**Answer:** **The Load step failed; only Asha's statement is true.**
**Step-by-step reasoning:**

| Step that failed | Asha (Transform or Load) | Bala (not Load) | Chitra (Extract) | True count |
|---|---|---|---|---|
| Extract | False | True | True | 2 (reject) |
| Transform | True | True | False | 2 (reject) |
| **Load** | **True** | **False** | **False** | **1 (accept)** |
1. The failure is exactly one of three steps, so try each.
2. Keep only the case with exactly one true statement: Load.
3. Unique, because the other two cases give two true statements.
**Fast method (30 seconds):** if Load did not fail, Bala is true, and then Chitra (Extract) or Asha (Transform or Load) must also be true because the failed step is Extract or Transform; that makes two truths. So only Load can work.
**Check:** Verified by script over all 3 cases: true counts were 2, 2, 1.
**Explain simply:**
- "Exactly one is true" is a counting condition: test each possible world and count truths.
- "Or" is true if at least one side is true, so Asha's statement is true for both Transform and Load.
**Likely follow-ups:** 1) *What if the rule were "exactly two are true"?* Then both Extract and Transform fit (2 truths each), so the puzzle is not unique. 2) *What if "exactly one is false"?* Brute force gives: Extract has one false, Transform has one false, Load has two false, so again not unique (checked from the same table).
**Common mistakes / traps:** Reading Asha's "or" as exclusive; taking the first case that looks plausible without counting the truths in the others.

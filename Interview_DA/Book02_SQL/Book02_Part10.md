# Book 2 (SQL) - Part 10: Duplicates, Nth Highest, Gaps & Islands, Recursive CTE, Query Optimisation [P0]

**Target:** 40 questions | **Actual:** 43
**Scope:** Classic SQL puzzle forms only: de-duplication, Nth highest (with and without windows), gaps and islands, recursive CTE hierarchies, query optimisation/indexes. Generic top-N per group is Part 5; window running totals are Part 6.

### Q1 ⭐⭐⭐ 🟢 Find all duplicate rows (e.g., duplicate employee emails) in a table and how many times each appears.
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Find the second highest salary without using window functions (MAX with a subquery).
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Find the Nth highest salary using DENSE_RANK().
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Why do we use DENSE_RANK (not ROW_NUMBER or RANK) for the Nth highest salary when two people have the same salary?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 Delete duplicate rows from a table but keep exactly one copy of each (ROW_NUMBER with a CTE).
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Find the Nth highest salary without window functions (correlated subquery / COUNT DISTINCT).
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Find the second highest salary using LIMIT/OFFSET, and return NULL when it does not exist.
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 A query is running slowly. Walk through how you would optimise it.
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 What does EXPLAIN show, and how do you read a query plan (scan vs index lookup, cost, rows)?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 When will a database NOT use an index? (Functions on columns, type mismatch, non-sargable filters.)
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🔴 Using a recursive CTE, list all direct and indirect reports of a given manager from an employee table (employee_id, manager_id).
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🔴 Gaps and islands: find the longest streak of consecutive login days for each user.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐ 🟢 Find duplicates based on a combination of columns (e.g., same name + date of birth + department).
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟢 How do you quickly check whether a table has duplicates by comparing COUNT(*) with COUNT(DISTINCT column)?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 Why is SELECT * discouraged in production queries?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 Remove duplicate rows without ROW_NUMBER (using MIN(id) / self join).
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 Among duplicate records for each customer, keep only the latest one (by updated date).
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 Find the top 3 distinct salaries in the company (including ties).
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 How do you delete duplicates from a table that has no primary key or unique ID?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Find the missing numbers in a sequence (e.g., missing invoice or order IDs).
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Find employees who were absent on 3 or more consecutive days from an attendance table (gaps and islands).
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Use a recursive CTE to generate numbers from 1 to 10.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Use a recursive CTE to generate a calendar of dates and find the dates with no sales.
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Use a recursive CTE to show the level (depth) of each employee in the org chart (CEO = level 1).
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Is it faster to filter with WHERE or HAVING? Explain when each is applied.
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Compare EXISTS, IN and JOIN: which is faster for checking presence and why?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 In a composite (multi-column) index, why does column order matter?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Why is LIKE '%abc' slow while LIKE 'abc%' can use an index?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 CTE vs temp table vs subquery: which is faster for reuse of an intermediate result?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Compute a running total without window functions (self join or correlated subquery).
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Gaps and islands: group consecutive employee IDs into ranges with start and end (e.g., 1-3, 7-9).
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🔴 Use a recursive CTE to build the full reporting chain as text (CEO > VP > Manager > Employee) for every employee.
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🔴 How do you stop a recursive CTE from looping forever when the hierarchy has a cycle?
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🔴 Merge overlapping date ranges (e.g., overlapping leave or booking periods) into single continuous periods.
<!-- ANSWER_PENDING -->

### Q35 ⭐ 🟢 Why do duplicates appear in HR or sales data in the first place, and how can constraints prevent them?
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🟡 How would you safely delete duplicates from a table with hundreds of millions of rows (batches, staging table, transaction, backup)?
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 Find the median salary without a MEDIAN function.
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 Why is OFFSET pagination slow on large tables, and what is keyset pagination?
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 What is a covering index and an index-only scan?
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 When would you partition a large table, and how does partition pruning speed up queries?
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🔴 For every manager, compute total team headcount (direct plus indirect) using a recursive CTE.
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Gaps report: list missing date ranges (start and end of each gap) in a daily sales table.
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 Rewrite a slow correlated subquery as a JOIN or window function and prove the improvement using EXPLAIN ANALYZE.
<!-- ANSWER_PENDING -->


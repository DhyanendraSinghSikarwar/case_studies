# Cross-part duplicate resolution (Book 2, Wave A)

Method: token-overlap scan of all 693 Book 2 questions (Jaccard >= 0.5 across different parts) plus keyword checks (never ordered, earn more than manager, second highest, duplicates). Exact/near-identical pairs were removed from one part and the part renumbered. Kept copy = the part whose topic owns the question.

| Removed (old ID) | Question | Kept copy |
|---|---|---|
| B2P2Q10 | In what order does SQL run a query (FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY)? Why does that order matter for aggregates? | B2P1Q13 |
| B2P2Q29 | How do you find duplicates based on a combination of columns (e.g., same name and date of birth), and show how many times each repeats? | B2P10Q14 |
| B2P4Q7 | Find the second highest salary using a subquery (MAX with a nested subquery) and explain how it works. | B2P10Q2 |
| B2P4Q8 | Find customers who have never placed an order (compare NOT IN, NOT EXISTS and LEFT JOIN ... IS NULL). | B2P3Q12 |
| B2P4Q17 | Why does NOT IN return no rows when the subquery contains a NULL? How do you avoid it? | B2P1Q37 |
| B2P4Q21 | Find employees who earn more than their manager (self-join vs subquery). | B2P3Q20 |
| B2P4Q29 | Find the latest order per customer using a subquery (MAX(order_date) matched back to the table). | B2P3Q50 |
| B2P4Q45 | What is a lateral join / CROSS APPLY and how is it related to correlated subqueries? | B2P3Q67 |
| B2P5Q49 | What is CUME_DIST() and how is it different from PERCENT_RANK()? | B2P6Q44 |
| B2P5Q53 | Why does LAST_VALUE() often return the wrong result by default, and how do you fix it? | B2P6Q25 |
| B2P5Q65 | What is the difference between the ROWS and RANGE frame, and does it affect RANK()? | B2P6Q11 |
| B2P6Q1 | What is a window function in SQL, and how is it different from GROUP BY? | B2P5Q1 |
| B2P6Q13 | Can you use a window function in a WHERE clause? Why not, and how do you filter on its result? | B2P5Q13 |
| B2P6Q21 | Can you use several window functions with different OVER() clauses in one query? | B2P5Q36 |
| B2P6Q22 | What is the difference between an aggregate function (SUM, AVG) and the same function used as a window function? | B2P5Q18 |
| B2P6Q43 | Which SQL databases support window functions, and from which version (MySQL 8, SQL Server, PostgreSQL, SQLite)? | B2P5Q48 |
| B2P6Q51 | Can you nest a window function inside another window function? How do you work around it? | B2P5Q70 |
| B2P6Q52 | How do window functions affect query performance, and how do indexes on PARTITION BY and ORDER BY columns help? | B2P5Q64 |
| B2P7Q1 | What is NULL in SQL, and how is it different from zero or an empty string? | B2P1Q9 |
| B2P7Q7 | Difference between COUNT(*) and COUNT(column) when the column has NULLs? | B2P2Q5 |
| B2P7Q42 | Why does NOT IN return no rows when the subquery contains NULL? How do you fix it? | B2P1Q37 |
| B2P8Q3 | E-commerce: Using `customers` and `orders`, list the customers who have never placed an order. | B2P3Q12 |
| B2P8Q8 | HR: Find employees who earn more than the average salary of their own department. | B2P4Q5 |
| B2P8Q9 | HR: `employees` has a manager_id pointing to another employee. List employees who earn more than their manager. | B2P3Q20 |
| B2P9Q13 | Find the longest streak of consecutive login days for each user (gaps-and-islands with ROW_NUMBER). | B2P10Q13 |
| B2P10Q5 | What is an index, and how does it make a query faster? | B2P11Q5 |
| B2P10Q15 | What is the difference between SELECT DISTINCT and GROUP BY for removing duplicates? | B2P2Q23 |
| B2P10Q16 | What is the difference between UNION and UNION ALL, and why does it matter for duplicates and speed? | B2P11Q17 |
| B2P11Q18 | What is the difference between WHERE and HAVING? | B2P2Q3 |
| B2P11Q42 | What is the difference between a view, a CTE and a temporary table? When do you use which? | B2P4Q18 |

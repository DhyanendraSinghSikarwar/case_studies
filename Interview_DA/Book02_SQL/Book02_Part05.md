# Book 2 — Part 5: Window functions: ROW_NUMBER, RANK, DENSE_RANK, top-N per group 🟡

- Target: 65 questions
- Actual: 71 questions
- Scope: ranking window functions (OVER, PARTITION BY, ROW_NUMBER/RANK/DENSE_RANK/NTILE, ties, top-N per group). Running totals/LAG/LEAD/moving averages are Part 6; nth-highest/dedup/gaps-islands are Part 10.

### Q1 ⭐⭐⭐ 🟢 What is a window function in SQL, in plain words, and how is it different from GROUP BY?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What does the OVER() clause do?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What does PARTITION BY do inside OVER()? Explain with an HR example (employees by department).
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What does ORDER BY inside OVER() do for ranking functions?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What does ROW_NUMBER() do, and when would you use it?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 What does RANK() do, and how does it treat tied values?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 What does DENSE_RANK() do, and how does it treat tied values?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 What is the difference between ROW_NUMBER, RANK and DENSE_RANK? Show it with salaries 100, 100, 90, 80.
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟢 Can you use RANK() without ORDER BY in OVER()? What happens?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Write a query to find the top 3 highest-paid employees in each department.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Write a query to find the highest-paid employee in each department (include everyone tied at the top).
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Write a query to find the second-highest salary in each department.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Why can't you use a window function directly in the WHERE clause, and how do you filter on a rank instead?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 How do you do top-N per group using a CTE or subquery with ROW_NUMBER?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Which function would you choose for top-N per group when ties exist, and why?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 Write a query to rank sales representatives by total sales within each region.
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 Write a query to find the top 5 products by revenue in each category.
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 What is the difference between a window function and an aggregate function?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 Can you use PARTITION BY without ORDER BY, and what does the result look like?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 What happens if you omit PARTITION BY? What is the 'partition' then?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 How do you rank in descending order (highest value gets rank 1)?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 What does NTILE() do? Give an example such as splitting employees into 4 salary quartiles.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 What is the SQL order of execution, and why does it matter for window functions?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 How do you get the latest record per customer (for example, most recent order) using ROW_NUMBER?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 How do you get the first order of each customer using a window function?
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Write a query to find the top 3 students by marks in each class, keeping ties.
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Write a query to rank employees by tenure within each department.
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Write a query that shows each employee's salary rank within their department and across the whole company in the same output.
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 If two employees tie for 2nd place, what rank does RANK() give the next person? What about DENSE_RANK()?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 How would you break ties in ROW_NUMBER deterministically (for example by employee ID)?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Is ROW_NUMBER() deterministic when ORDER BY values tie? Explain the risk.
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do NULL values behave in the ORDER BY of a ranking function (NULLS FIRST or LAST)?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Write a query to find the top-selling product each month.
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 Write a query to find the department with the highest total salary using a ranking function.
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 Write a query to find the top 2 hiring sources by number of hires in each year.
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 Can you use two window functions with different PARTITION BY in one query? Give an example.
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 What is the difference between using ROW_NUMBER() and LIMIT/TOP for 'top 1 per group'?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 How do you display ROW_NUMBER, RANK and DENSE_RANK side by side in one query?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 How do you number rows 1..n in a table without a ranking-specific column (a simple serial number)?
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 Write a query to find employees whose salary is the highest in their department and above 50,000.
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 How do you use a window function inside a subquery, and why do you need to wrap it?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 What is PERCENT_RANK() and how is it different from RANK()?
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 Write a query to rank customers by total spend and show the top 10 percent.
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 How would you rank employees by performance rating within each manager's team?
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🔴 Write a query to find the top 3 products by revenue per category, but return only categories with at least 3 products.
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🔴 Find the top-N per group when N differs by group (for example a lookup table gives N for each department).
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟢 What is the difference between RANK and DENSE_RANK in terms of 'gaps' in the sequence?
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟢 Which SQL databases support window functions (MySQL 8, PostgreSQL, SQL Server, Oracle, SQLite) and which do not?
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🟡 What is the difference between RANK() and PERCENT_RANK() on a 5-row example?
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🟡 Write a query to find the top 3 and the bottom 3 earners in each department in one result.
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🟡 How do FIRST_VALUE() and LAST_VALUE() help in ranking-style questions (for example, highest salary in the department shown beside every row)?
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🟡 How do you get the top-N per group without window functions (correlated subquery or self join)? Compare the two approaches.
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🟡 Using CROSS APPLY or LATERAL join, how do you get top-N per group? When is it faster?
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🟡 Write a query to find employees earning more than the average of their department using a window function instead of a join.
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🟡 How do you rank rows by two columns (for example department rank, then salary within it)?
<!-- ANSWER_PENDING -->

### Q56 ⭐ 🟡 How do you rank by multiple criteria with tie-breakers (score descending, then name ascending)?
<!-- ANSWER_PENDING -->

### Q57 ⭐ 🟡 How do you create a leaderboard where tied players share a rank and the next rank is not skipped?
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🟡 Write a query to rank months by revenue within each year.
<!-- ANSWER_PENDING -->

### Q59 ⭐ 🟡 What does the NTILE(n) function do when rows do not divide evenly into n buckets?
<!-- ANSWER_PENDING -->

### Q60 ⭐ 🟡 How would you use ROW_NUMBER to pick a random sample of 2 employees per department?
<!-- ANSWER_PENDING -->

### Q61 ⭐ 🟡 Write a query to assign a 'salary band' (top 25 percent, middle, bottom 25 percent) using NTILE or PERCENT_RANK.
<!-- ANSWER_PENDING -->

### Q62 ⭐ 🔴 How do window functions perform on large tables, and how would an index on the PARTITION BY/ORDER BY columns help?
<!-- ANSWER_PENDING -->

### Q63 ⭐ 🔴 Write a query to find the top 3 products per category along with each product's share of the category's revenue.
<!-- ANSWER_PENDING -->

### Q64 ⭐ 🔴 How would you find departments where the top earner earns more than twice the second-highest earner?
<!-- ANSWER_PENDING -->

### Q65 ⭐ 🔴 How would you rank hierarchical data (employees under each manager) combining a ranking function with a self join?
<!-- ANSWER_PENDING -->

### Q66 ⭐ 🔴 Write a query to find the top 3 customers per city by order count, breaking ties by most recent order date.
<!-- ANSWER_PENDING -->

### Q67 ⭐ 🔴 Can you use a window function in GROUP BY, HAVING or another window function? How do you work around it?
<!-- ANSWER_PENDING -->

### Q68 ⭐ 🔴 You see duplicated rank values in your ROW_NUMBER output. What are the likely causes?
<!-- ANSWER_PENDING -->

### Q69 ⭐ 🔴 Explain a top-N per group result that returns more than N rows. Why does it happen and how do you fix it?
<!-- ANSWER_PENDING -->

### Q70 ⭐ 🔴 Compare QUALIFY (Snowflake, BigQuery) with a subquery filter for window-function results.
<!-- ANSWER_PENDING -->

### Q71 ⭐ 🔴 A manager asks: 'show top 3 salaries per department, but I want 3 distinct salary values, not 3 people.' Which function and why?
<!-- ANSWER_PENDING -->

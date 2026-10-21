# Book 2 — SQL · Part 7: CASE WHEN, NULL handling, string & date functions 🟢🟡

**Target:** 50 questions  |  **Actual:** 60

**Scope:** conditional logic (CASE WHEN, IIF), NULL behaviour (IS NULL, COALESCE, NULLIF, NULL in aggregates/joins/NOT IN), string functions and date functions, with MySQL / PostgreSQL / SQL Server differences noted where they matter.

### Q1 ⭐⭐⭐ 🟢 How do you check for NULL values? Why does `WHERE col = NULL` return nothing?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What does COALESCE do? Replace missing salaries with 0 in a report.
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Write a CASE WHEN statement to label employees as Low / Medium / High based on salary.
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Explain the syntax of CASE WHEN. What are the simple and searched forms?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 How do NULLs behave in aggregate functions (COUNT(*), COUNT(col), SUM, AVG)?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 How do you find the difference in days between two dates (e.g., joining date and today) in MySQL, PostgreSQL and SQL Server?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 How do you get the current date and current timestamp in each dialect (NOW, CURRENT_DATE, GETDATE)?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 How do you filter rows for the last 30 days / this month / this year?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟢 How do you concatenate first name and last name into a full name? Does it differ across dialects?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 How do you use CASE WHEN inside an aggregate (conditional aggregation) to count male and female employees in one query?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 How do you get the month and year from a date column and group sales by month?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 How do you calculate each employee's tenure in years from their joining date?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How does NULL affect joins and comparisons, such as WHERE col <> 'X' skipping NULL rows?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 How do you pivot rows to columns using CASE WHEN (e.g., monthly sales in separate columns)?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 What is NULLIF and when do you use it (e.g., avoiding divide-by-zero)?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 How do you avoid a division-by-zero error when calculating a percentage?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 Difference between COALESCE, IFNULL, ISNULL and NVL?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 How do you use IIF or IF in place of CASE WHEN?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 How do you use UPPER, LOWER and TRIM to clean text before comparing it?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 How do you find the length of a string and filter names longer than 10 characters?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 How do you extract the first 3 characters of a string with SUBSTRING / LEFT?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 How do you use REPLACE to remove or change characters, such as hyphens in phone numbers?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 How do you use LIKE with % and _ wildcards to search text patterns?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟢 Which employees have names starting with 'A' or ending with 'n'? Show LIKE patterns.
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟢 How do you add or subtract days, months or years from a date (DATE_ADD, DATEADD, INTERVAL)?
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟢 How do you extract day, month, year, weekday using EXTRACT, DATEPART or DAY/MONTH/YEAR?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟢 How do you change a date's display format (DATE_FORMAT, TO_CHAR, FORMAT)?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟢 What is CAST and CONVERT? Convert text to number and number to text.
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟢 How do you handle NULLs in CONCAT? How does it differ in MySQL vs PostgreSQL vs SQL Server?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 How do you extract the domain from an email address (the part after @)?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 How do you split a full name into first name and last name in SQL?
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you do case-insensitive search across MySQL, PostgreSQL (ILIKE) and SQL Server?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 What is DATE_TRUNC / how do you truncate dates to month or week in each dialect?
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you convert a text date such as '15-08-2025' to a proper date (STR_TO_DATE, TO_DATE, CONVERT)?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 How do you use CASE WHEN in ORDER BY for custom sort order (e.g., High, Medium, Low)?
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 How do you use CASE WHEN inside UPDATE to change values conditionally?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 How do you create age bands or salary buckets using CASE WHEN and count per bucket?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 How do you find employees whose birthday falls this month?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 How do you handle NULLs when sorting (NULLS FIRST / NULLS LAST) across dialects?
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 How do you count NULLs and non-NULLs of a column in one query?
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 How do you calculate the percentage of rows meeting a condition (e.g., attrition rate) using CASE WHEN?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 How do you find missing dates or the first and last day of a month?
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 What are NULL-safe comparisons (IS DISTINCT FROM, <=> in MySQL)?
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 How do you calculate working days / exclude weekends between two dates?
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🟢 How do you use TRIM, LTRIM and RTRIM to remove spaces?
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🟢 How do you pad numbers with leading zeros (LPAD, RIGHT, FORMAT)?
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟡 How do you find the day of the week with the highest sales?
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 How do you group sales by fiscal year or quarter (e.g., April-March)?
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🟡 How do you find a character's position inside a string (CHARINDEX, POSITION, INSTR)?
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🟡 How do you count occurrences of a character in a string?
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🟡 How do you use REGEXP / regular expressions to validate emails or phone numbers?
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🟡 How do you aggregate strings (GROUP_CONCAT, STRING_AGG, LISTAGG)?
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🟡 What is the difference between DATE, DATETIME and TIMESTAMP data types?
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🟡 How do you compare timestamps while ignoring the time part (e.g., filter a full day)?
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🟡 How do you use nested CASE WHEN? When should you avoid it?
<!-- ANSWER_PENDING -->

### Q56 ⭐ 🟡 Why is wrapping a date column in a function (YEAR(col)=2025) bad for speed, and what is the better filter?
<!-- ANSWER_PENDING -->

### Q57 ⭐ 🟡 How do you detect and clean inconsistent text values (e.g., 'Hyd', 'hyderabad ') in a city column?
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🟡 What is implicit type conversion and how can it cause wrong results in comparisons?
<!-- ANSWER_PENDING -->

### Q59 ⭐ 🔴 How do you handle time zones in timestamps (AT TIME ZONE, CONVERT_TZ)?
<!-- ANSWER_PENDING -->

### Q60 ⭐ 🔴 How do you generate a continuous series of dates (calendar table) in each dialect?
<!-- ANSWER_PENDING -->


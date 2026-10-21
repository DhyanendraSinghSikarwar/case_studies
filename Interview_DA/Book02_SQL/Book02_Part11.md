# Book 2 — SQL | Part 11: DB Concepts (keys, normalization, indexes, views, stored procedures, DDL/DML, transactions/ACID, OLTP vs OLAP, data warehouse basics)

- **Target:** 35 questions (minimum)
- **Actual:** 44 questions
- **Scope:** Database-concept questions asked in DA/BA technical rounds (🟢🟡, a few ⭐ 🔴 design questions). Heavy query writing lives in Parts 1-10. Questions on UNION/UNION ALL, WHERE vs HAVING and DELETE/TRUNCATE/DROP appear here with a database-concept framing; Parts 1-2 cover their query-writing use.
- **Ordering:** ⭐⭐⭐ → ⭐, then 🟢 → 🔴.

### Q1 ⭐⭐⭐ 🟢 What is a primary key, and how is it different from a foreign key?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What are DDL, DML, DCL and TCL commands? Give one example of each.
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is the difference between DELETE, TRUNCATE and DROP?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What is a view in SQL, and why would an analyst use one?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What is an index, and how does it make a query faster?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 What is normalization, and why do databases use it?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 What are the ACID properties of a database transaction?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 What is the difference between OLTP and OLAP systems?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 What are 1NF, 2NF and 3NF? Explain each with a simple table example.
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 What is a star schema? What are fact tables and dimension tables?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐ 🟢 What is the difference between a primary key and a unique key?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐ 🟢 What is a candidate key, a composite key and a surrogate key?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐ 🟢 What is a database, a DBMS and an RDBMS?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟢 What are constraints in SQL (NOT NULL, UNIQUE, CHECK, DEFAULT)? Why are they useful?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 What is a transaction? What do COMMIT and ROLLBACK do?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 What is a data warehouse, and how is it different from an operational database?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 What is the difference between UNION and UNION ALL?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 What is a schema, and what is the difference between a table and a view?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 What is the difference between a clustered and a non-clustered index?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 What is a stored procedure? How is it different from a user-defined function?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 What is denormalization, and when would you choose it over normalization?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 What is a snowflake schema, and how does it differ from a star schema?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 What is the difference between a view and a materialized view?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 What is ETL? How is it different from ELT?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 What is referential integrity? What happens if you delete a parent row that has child rows (CASCADE, RESTRICT, SET NULL)?
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 What are the types of relationships between tables (one-to-one, one-to-many, many-to-many)? How is many-to-many stored?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 When should you NOT create an index? What are the costs of indexes?
<!-- ANSWER_PENDING -->

### Q28 ⭐ 🟢 What is the difference between SQL and NoSQL databases? When would you use each?
<!-- ANSWER_PENDING -->

### Q29 ⭐ 🟢 What is an ER diagram, and what do entities, attributes and relationships mean?
<!-- ANSWER_PENDING -->

### Q30 ⭐ 🟢 What are the common SQL data types (INT, VARCHAR, DATE, DECIMAL)? Why does choosing the right type matter?
<!-- ANSWER_PENDING -->

### Q31 ⭐ 🟡 What is a trigger? Give a business use case and a drawback.
<!-- ANSWER_PENDING -->

### Q32 ⭐ 🟡 What is BCNF, and how does it differ from 3NF?
<!-- ANSWER_PENDING -->

### Q33 ⭐ 🟡 What are transaction isolation levels and the problems they prevent (dirty read, non-repeatable read, phantom read)?
<!-- ANSWER_PENDING -->

### Q34 ⭐ 🟡 What is a slowly changing dimension (Type 1, Type 2, Type 3)? Give an HR example such as an employee changing department.
<!-- ANSWER_PENDING -->

### Q35 ⭐ 🟡 What is a data mart, and how is it different from a data warehouse and a data lake?
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🟡 What is a temporary table, and how does it differ from a CTE or a table variable?
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 What is a deadlock, and how can it be avoided?
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 What is table partitioning, and how does it help with large tables?
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 How do you read a query execution plan (EXPLAIN) at a basic level to spot a missing index?
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 What is a composite index, and does the order of its columns matter?
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🟡 What is the grain of a fact table, and why must you define it before building reports?
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Design a simple database for an HR system (employees, departments, salaries, attendance): tables, keys and relationships.
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 How would you design a star schema for a sales or hiring-funnel report? Name the fact table, dimensions and measures.
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 What is the CAP theorem, and why do analytics databases often relax consistency?
<!-- ANSWER_PENDING -->


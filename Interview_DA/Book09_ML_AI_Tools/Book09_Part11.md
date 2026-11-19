# Book 9 — Basic ML + AI Tools for Analysts | Part 11: Cloud Basics for Analysts (AWS/Azure/GCP, Snowflake, BigQuery, Fabric) 🟢🟡🔴

**Target:** 15 questions | **Actual:** 21 questions
**Scope:** cloud concepts an entry-level analyst should be able to explain (storage vs warehouse, warehouse vs lake, cost and access basics, Snowflake, BigQuery, Microsoft Fabric); low frequency, so stars stay at the low end.

### Q1 ⭐⭐ 🟢 What does "the cloud" mean for a data analyst, and how is working with cloud-hosted data different from working with files on your laptop or an on-premise server?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐ 🟢 What is the difference between a database, a data warehouse and a data lake, and which one would an analyst usually query for reporting?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐ 🟢 What is Snowflake, and what does "storage and compute are separate" mean for an analyst running queries?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐ 🟢 Name the main object-storage service and the main analytics warehouse service on AWS, Azure and Google Cloud, and say which are storage and which are warehouses.
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐ 🟡 BigQuery on-demand pricing is based on bytes scanned. A table holds 2 TB across 10 columns of roughly equal size, and you need only 2 columns. Compare the data scanned and the cost of `SELECT *` against selecting just those 2 columns, using an illustrative rate of 5 currency units per TB scanned.
Data: 2 TB table, 10 equal-sized columns, illustrative rate 5 per TB scanned (assumption for calculation only, not a quoted price).
<!-- ANSWER_PENDING -->

### Q6 ⭐ 🟢 What is the difference between OLTP and OLAP systems, and why do analysts run reports on a warehouse instead of the live application database?
<!-- ANSWER_PENDING -->

### Q7 ⭐ 🟢 Explain in one minute what Microsoft Fabric and OneLake are, as you would to a Power BI user who has never heard of them.
<!-- ANSWER_PENDING -->

### Q8 ⭐ 🟢 What is the shared responsibility model in cloud, and what does the principle of least privilege (IAM) mean for the access an analyst should request?
<!-- ANSWER_PENDING -->

### Q9 ⭐ 🟢 Your manager asks why the team should move its reports from Excel files on a shared drive to a cloud warehouse. Give two benefits and two risks or costs to check.
<!-- ANSWER_PENDING -->

### Q10 ⭐ 🟢 Before uploading an employee payroll or attrition file to a cloud storage bucket or an online AI or analytics tool, what checks would you make?
<!-- ANSWER_PENDING -->

### Q11 ⭐ 🟡 What is the difference between a Fabric lakehouse and a Fabric warehouse, and what is the SQL analytics endpoint of a lakehouse used for?
<!-- ANSWER_PENDING -->

### Q12 ⭐ 🟡 In Power BI, how do Import, DirectQuery and Direct Lake modes differ, and when would you prefer each?
<!-- ANSWER_PENDING -->

### Q13 ⭐ 🟡 What is the difference between partitioning and clustering a BigQuery table, and which would you apply to a sales table queried mostly by order date and then by region?
<!-- ANSWER_PENDING -->

### Q14 ⭐ 🟡 Read this BigQuery query on a table partitioned by `order_date`. Does it limit the data scanned, and how would you fix it if not?
```sql
SELECT customer_id, SUM(amount)
FROM sales.orders
WHERE FORMAT_DATE('%Y-%m', order_date) = '2026-10'
GROUP BY customer_id;
```
<!-- ANSWER_PENDING -->

### Q15 ⭐ 🟡 A Snowflake virtual warehouse is billed at 2 credits per hour while running. It runs 3 hours every weekday and auto-suspends otherwise. How many credits does it use in a 4-week month (20 weekdays), and what single change would you try first if the team wants to cut the bill?
Data: 2 credits per hour (illustrative figure), 3 hours per weekday, 20 weekdays.
<!-- ANSWER_PENDING -->

### Q16 ⭐ 🟡 You ran `DROP TABLE hr.attendance` by mistake on a Snowflake table. What features might let you recover it, and what do you do right away?
<!-- ANSWER_PENDING -->

### Q17 ⭐ 🟡 What is the difference between ETL and ELT, and why is ELT common with cloud warehouses such as Snowflake and BigQuery?
<!-- ANSWER_PENDING -->

### Q18 ⭐ 🟡 Your BigQuery or Snowflake bill doubled this month and your analyst team is the main user. What would you check, in order, before changing anything?
<!-- ANSWER_PENDING -->

### Q19 ⭐ 🟡 What is schema-on-write versus schema-on-read, and which applies when CSV files sit in S3 or Azure Data Lake and you query them directly?
<!-- ANSWER_PENDING -->

### Q20 ⭐ 🔴 In Snowflake, a table `raw_events` has a VARIANT column `payload` holding JSON such as `{"employee": {"id": 101, "dept": "HR"}, "event": "login"}`. Write a query that returns employee id, department and event as separate typed columns.
<!-- ANSWER_PENDING -->

### Q21 ⭐ 🔴 A company already uses Microsoft 365 and Power BI heavily, while another uses Google Workspace and mostly SQL notebooks. How would your cloud platform recommendation for analytics differ, and what non-technical factors would you weigh?
<!-- ANSWER_PENDING -->

# Book 3 — Python & pandas for Analysts | Part 9: EDA End-to-End Tasks (Live-Coding Style) 🟡🔴

**Target:** 50 questions | **Actual:** 54 questions
**Scope:** end-to-end exploratory data analysis tasks in pandas as asked in live-coding and take-home rounds: load, inspect, clean, summarise, compare groups, chart and explain findings, using HR, payroll, attendance and sales data.

### Q1 ⭐⭐⭐ 🟢 You are given a CSV file you have never seen. What are the first five things you do in pandas to understand it?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Write code to load employees.csv and print its shape, column dtypes and the number of missing values per column.
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟡 Write code to calculate the overall attrition rate (percentage of employees with Attrition = 'Yes') from an HR DataFrame.
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 Write code to find the attrition rate by department and sort the departments from highest to lowest.
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 Walk me through a complete EDA of an employee attrition dataset using pandas, from loading the file to your final recommendations.
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Write code to check for duplicate rows in a DataFrame, count them, and remove them while keeping the first occurrence.
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Write code to find the top 5 job roles by average monthly income, showing role, average income and headcount.
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 A sales DataFrame has order_date, region and revenue. Write code to find total revenue per region and the share (percentage) of each region in the total.
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Write code to merge an employee table with a department table and then check that the merge did not create extra rows or lose employees.
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Write code to find which columns have missing values, what percentage is missing in each, and decide how you would treat each (drop, fill, or leave).
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 After you finish an EDA in an interview, how do you present your findings in plain business language instead of reading out code output?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Write code to detect outliers in a salary column using the IQR rule and list the employees flagged.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Write code to convert a joining_date column stored as text into datetime, then create columns for joining year, joining month and tenure in years.
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🔴 You get a messy attendance file with mixed date formats, 'Present'/'present '/'P' status values and blank employee IDs. Write the cleaning code step by step.
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🔴 Given a hiring funnel DataFrame (candidate_id, stage, date), write code to compute the number of candidates reaching each stage and the conversion rate from one stage to the next.
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 What is the difference between df.info(), df.describe() and df.head(), and what does each tell you in the first minutes of EDA?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 Write code to list all categorical columns and print the value counts of each, including missing values.
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 Write code to select only numeric columns of a DataFrame and compute their mean, median and standard deviation.
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 How do you check whether a column that looks numeric (for example salary) was loaded as object, and how do you convert it safely?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Write code to find the correlation between numeric columns in an HR dataset and list the top 3 pairs with the strongest relationship.
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Write code to compare the average salary, age and tenure of employees who left versus those who stayed.
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Write code to create age bands (for example 18-25, 26-35, 36-45, 46+) with pd.cut and show attrition rate per band.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Write code to build a payroll summary: headcount, total gross pay and average gross pay per department, with clear column names.
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Write code to find employees with more than 3 absences in a month from a daily attendance DataFrame.
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Write code to flag employees whose salary is above the average of their own department (not the whole company).
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Write code to find the department-wise count of employees who joined in each year using a pivot table or crosstab.
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Write code to identify the columns that have only one unique value or a unique value for every row, and explain why you would drop them.
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Why does a merge sometimes return more rows than the left table, and how do you detect and prevent it with validate= and indicator=True?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 You get a SettingWithCopyWarning while creating a new column on a filtered DataFrame during EDA. Why does it happen and how do you fix it?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 You get a KeyError for a column name that you can clearly see in the file. What are the likely causes (spaces, case, encoding) and how do you fix them?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Write code to standardise column names (strip spaces, lower case, replace spaces with underscores) right after loading a file.
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Write code to find the month with the highest total sales in a sales DataFrame and the month-over-month growth percentage.
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Write code to check whether two DataFrames (for example last month and this month employee lists) have employees present in one but missing in the other.
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 Write code to find the top 3 products by revenue within each region.
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 How do you decide between dropping, filling with the median, or flagging missing values in a dataset during EDA? Show the code for each option.
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 How would you check data quality of a new dataset (completeness, duplicates, valid ranges, consistent categories) and produce a short data-quality summary table in pandas?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 Write code to plot a histogram of salary, a bar chart of attrition by department and a boxplot of salary by job level, and say what each chart tells you.
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🔴 Write code that takes any DataFrame and prints an automatic profile: shape, dtypes, missing percentage, unique counts and basic statistics in one summary table.
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🔴 Write code to compute a 3-month rolling average of monthly headcount and flag months where hiring dropped more than 20 percent.
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🔴 Write code to find employees whose exit date is before their joining date, or whose age is below 18 or above 70, as data validity checks.
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🔴 Write code to compare cohorts: for each joining-year cohort, calculate the percentage still employed after 1 and 2 years.
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🔴 You find that 15 percent of the salary column is missing. How do you investigate whether the missingness is random or related to department or location before filling it?
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🔴 Interviewer gives you a 5-minute task: 'Which department needs retention attention most?' Which columns, aggregations and charts do you use to answer it with evidence?
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🔴 Write code to reconcile two payroll files by employee ID and list records where net pay differs by more than 1 rupee.
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🔴 How do you handle a dataset too large to fit comfortably in memory when doing EDA in pandas (chunksize, usecols, dtypes)?
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🔴 After your EDA shows that overtime and low income are linked to attrition, what are the limits of this conclusion, and how do you explain correlation versus causation to HR?
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟢 How do you read only selected columns and rows of a large CSV file to start EDA quickly?
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 Write code to export your cleaned DataFrame and a summary table to one Excel file with two sheets.
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🟡 How do you make your EDA notebook reproducible and easy for a reviewer to follow in a take-home assignment (structure, comments, markdown, random seed, order of cells)?
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🟡 Which pandas profiling or auto-EDA tools do you know, and why should you still do manual EDA in an interview?
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🟡 In a take-home EDA assignment given 48 hours, how do you decide what to include in your final report, and what do you leave out?
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 Write code to create a simple attrition risk score from three rules (overtime, low satisfaction, short tenure) and check how well it separates leavers from stayers.
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 Write a function that takes any DataFrame and a target column and returns the target's rate for each categorical column, so you can scan for drivers quickly.
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🔴 A stakeholder asks: 'Is attrition higher in Hyderabad than Bengaluru?' How do you check this in pandas, and how do you avoid overclaiming when one city has very few employees?
<!-- ANSWER_PENDING -->

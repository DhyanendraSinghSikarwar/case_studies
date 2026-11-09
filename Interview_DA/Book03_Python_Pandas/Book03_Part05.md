# Book 3 — Python & pandas for Analysts | Part 5: pandas: groupby, merge, pivot, apply 🟡

**Target:** 70 questions | **Actual:** 83 questions
**Scope:** pandas groupby and aggregation, merge/join/concat, pivot_table/crosstab/melt, and apply/map, as asked in data/MIS analyst live-coding rounds.

### Q1 ⭐⭐⭐ 🟢 What does groupby() do in pandas, and what are the split-apply-combine steps?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Write code to find the average salary by department from an employee DataFrame.
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Write code to count the number of employees in each department using groupby.
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What is the difference between size() and count() in a pandas groupby?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What is the difference between merge() and join() in pandas?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 What join types does pd.merge() support through the how= argument, and how do they map to SQL joins?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 Write code to left-merge an employee DataFrame with a department DataFrame on the column dept_id.
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 What is the difference between merge() and concat() in pandas?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟢 What is pivot_table() in pandas, and how do you create one?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟢 Write code to build a pivot table of average salary with department as rows and gender as columns.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟢 What is the difference between apply(), map() and applymap() in pandas?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Write code to group by department and compute headcount, average salary and maximum salary in one step using named aggregation.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 What is the difference between agg() and transform() in a pandas groupby?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Write code to add a column showing each employee's department average salary next to their own salary.
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Write code to find the top 3 highest-paid employees in each department.
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 After a merge, your row count increased unexpectedly. What are the likely causes and how do you check?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 How do you find the rows in one DataFrame that have no match in another (an anti join) in pandas?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 What is the difference between pivot() and pivot_table() in pandas?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🟡 Write code using apply() with a lambda to create a column that labels each employee 'High' or 'Low' by salary, and explain when a vectorised alternative is better.
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐⭐ 🟡 Why is apply() with axis=1 slow, and what do you use instead?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐⭐ 🟡 You get a SettingWithCopyWarning after filtering a DataFrame and assigning a new column. What does it mean and how do you fix it?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐⭐ 🟡 Write code to replicate Excel's VLOOKUP in pandas using merge.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 How do you group by two columns, for example department and location, and get the average salary for each pair?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟢 After groupby, the group key becomes the index. How do you turn it back into a normal column?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟢 What is the effect of as_index=False in groupby, and how does it compare with reset_index()?
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟢 How do you sort the result of a groupby in descending order of the aggregated value?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟢 Write code to find the number of employees by gender within each department as a table.
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟢 What is the difference between value_counts() and groupby().size()?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟢 What does groupby() actually return, and how do you look at a single group such as the 'Finance' department?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟢 Write code to find the number of unique candidates per recruitment source (nunique) from a hiring DataFrame.
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟢 How do you merge two DataFrames when the key column has different names, for example emp_id and employee_id?
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟢 Write code to stack the January, February and March attendance DataFrames into one DataFrame.
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟢 What does ignore_index=True do in pd.concat()?
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟢 What is pd.crosstab(), and how does it differ from pivot_table()?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟢 What is the purpose of the suffixes argument in merge()?
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟢 By default, are rows with NaN in the groupby key included in the result? How do you change that?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟢 Write code to map department codes ('FIN', 'HR', 'IT') to full department names using a dictionary and map().
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟢 Why does a KeyError appear after a groupby aggregation when you refer to the grouping column, and how do you fix it?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 Write code to calculate the attrition rate (percentage of leavers) by department.
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 Write code to show each employee's salary as a percentage of their department's total payroll.
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 Write code to keep only the departments that have more than 10 employees using groupby().filter().
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 Write code to find the department whose average salary is above the company-wide average.
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 Write code to calculate a running (cumulative) total of sales within each region.
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 Write code to rank employees by salary within each department.
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 Write code to compare each month's headcount with the previous month for every department using shift().
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 How do you merge on two columns, for example employee ID and month?
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟡 What does the validate argument in merge() do, and when would you use it?
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟡 What does indicator=True do in merge(), and how do you use the _merge column?
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🟡 After a merge, integer columns turn into floats. Why does this happen and how do you fix it?
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🟡 A merge returns zero matching rows even though the IDs look the same. What would you check?
<!-- ANSWER_PENDING -->

### Q51 ⭐⭐ 🟡 Write code to merge an employees table with an attendance table and calculate each employee's attendance percentage.
<!-- ANSWER_PENDING -->

### Q52 ⭐⭐ 🟡 Write code to merge a payroll table with a deductions table and compute net pay, treating missing deductions as zero.
<!-- ANSWER_PENDING -->

### Q53 ⭐⭐ 🟡 What does an outer merge return, and how do you handle the NaN values it creates?
<!-- ANSWER_PENDING -->

### Q54 ⭐⭐ 🟡 Write code to build a pivot table of headcount by department and month, with row and column totals.
<!-- ANSWER_PENDING -->

### Q55 ⭐⭐ 🟡 What do the fill_value, margins and aggfunc arguments do in pivot_table()?
<!-- ANSWER_PENDING -->

### Q56 ⭐⭐ 🟡 How do you apply more than one aggregation function (sum and mean) to a column in pivot_table()?
<!-- ANSWER_PENDING -->

### Q57 ⭐⭐ 🟡 What does melt() do, and when do you use it?
<!-- ANSWER_PENDING -->

### Q58 ⭐⭐ 🟡 What do stack() and unstack() do, and how are they related to pivot tables?
<!-- ANSWER_PENDING -->

### Q59 ⭐⭐ 🟡 How do you replicate Excel's SUMIFS in pandas?
<!-- ANSWER_PENDING -->

### Q60 ⭐⭐ 🟡 Write code to find the employee with the highest salary in each department using idxmax().
<!-- ANSWER_PENDING -->

### Q61 ⭐⭐ 🟡 Write code to apply a custom function that labels performance rating bands to every row.
<!-- ANSWER_PENDING -->

### Q62 ⭐⭐ 🟡 How do you pass extra arguments to a function used in apply()?
<!-- ANSWER_PENDING -->

### Q63 ⭐⭐ 🟡 Write code to assign a grade ('A', 'B', 'C') from a score using np.select or np.where instead of apply().
<!-- ANSWER_PENDING -->

### Q64 ⭐⭐ 🟡 Write code to bucket employees into tenure bands (0-1, 1-3, 3+ years) with pd.cut and count each band.
<!-- ANSWER_PENDING -->

### Q65 ⭐⭐ 🟡 After agg() with several functions, the columns become a MultiIndex. How do you flatten them?
<!-- ANSWER_PENDING -->

### Q66 ⭐⭐ 🟡 What is the difference between concat() with axis=0 and axis=1, and what happens when the indexes do not match?
<!-- ANSWER_PENDING -->

### Q67 ⭐ 🟢 What is the difference between map() and replace() for changing values in a column?
<!-- ANSWER_PENDING -->

### Q68 ⭐ 🟡 Write code to calculate stage-to-stage conversion rates in a hiring funnel (applied, screened, interviewed, offered, joined).
<!-- ANSWER_PENDING -->

### Q69 ⭐ 🟡 Write code to turn a monthly leavers list into a wide table of department by month with zeros where there were no leavers.
<!-- ANSWER_PENDING -->

### Q70 ⭐ 🟡 How do you get the latest record per employee using groupby when an employee appears several times?
<!-- ANSWER_PENDING -->

### Q71 ⭐ 🟡 How do you merge on the index of one DataFrame and a column of another?
<!-- ANSWER_PENDING -->

### Q72 ⭐ 🟡 What does a cross join do, and how do you do it in pandas?
<!-- ANSWER_PENDING -->

### Q73 ⭐ 🟡 What is the difference between groupby with apply() and groupby with agg(), and which is faster?
<!-- ANSWER_PENDING -->

### Q74 ⭐ 🟡 Why is iterrows() slow, and what are faster alternatives for row-wise logic?
<!-- ANSWER_PENDING -->

### Q75 ⭐ 🟡 Is a pivot_table the same as groupby().unstack()? Show both for the same result.
<!-- ANSWER_PENDING -->

### Q76 ⭐ 🟡 Why should you avoid calling concat() inside a loop, and what is the better pattern?
<!-- ANSWER_PENDING -->

### Q77 ⭐ 🟡 Write code to find employees present in both a 'trained' list and a 'certified' list.
<!-- ANSWER_PENDING -->

### Q78 ⭐ 🟡 What does the observed argument do when grouping by a categorical column?
<!-- ANSWER_PENDING -->

### Q79 ⭐ 🔴 Write code to calculate a 3-month rolling average of headcount within each department.
<!-- ANSWER_PENDING -->

### Q80 ⭐ 🔴 What is merge_asof(), and when would an analyst use it?
<!-- ANSWER_PENDING -->

### Q81 ⭐ 🔴 Write code to find the second-highest salary in each department.
<!-- ANSWER_PENDING -->

### Q82 ⭐ 🔴 Write code to calculate each department's share of total attrition and flag departments contributing more than 25%.
<!-- ANSWER_PENDING -->

### Q83 ⭐ 🔴 How would you reconcile two employee lists (HRMS and payroll) to find missing, extra and mismatched records using merge?
<!-- ANSWER_PENDING -->

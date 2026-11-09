# Book 3 — Python & pandas for Analysts | Part 5: pandas: groupby, merge, pivot, apply 🟡

**Target:** 70 questions | **Actual:** 83 questions
**Scope:** pandas groupby and aggregation, merge/join/concat, pivot_table/crosstab/melt, and apply/map, as asked in data/MIS analyst live-coding rounds.

### Q1 ⭐⭐⭐ 🟢 What does groupby() do in pandas, and what are the split-apply-combine steps?
**Asked at:** commonly asked (no company-specific report found); pandas data manipulation is reported in a Tiger Analytics technical round (snippet-level source only).
**What the interviewer is checking:** Do you understand groupby as three steps, not just the syntax?
**Say this in the interview:** "groupby splits the table into one small table per group, applies a calculation to each, and combines the results into one output. It is the pandas version of SQL GROUP BY or an Excel pivot table."
**Explain simply:**
- **Split:** rows are sorted into buckets by a column, for example one bucket per department.
- **Apply:** a function runs on each bucket separately (mean, count, sum, max).
- **Combine:** the per-bucket answers are stitched into one Series or DataFrame, with the group names as the index.
- groupby on its own calculates nothing; it only prepares the groups. The work happens when you add an aggregation such as `.mean()`.
- The result of an aggregation has one row per group, so it is shorter than the original table.
**Sample data:**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "Karan", "Divya", "Imran", "Sana"],
    "department": ["HR", "HR", "Finance", "Finance", "Finance", "IT", "IT"],
    "salary": [50000, 60000, 70000, 80000, 90000, 65000, None],
})
```
**Code (what you write in the interview):**
```python
# split by department, apply mean to salary, combine into one result
average_salary = employees.groupby("department")["salary"].mean()
print(average_salary)
```
**Output:**
```
department
Finance    80000.0
HR         55000.0
IT         65000.0
Name: salary, dtype: float64
```
**What it means:** Three groups went in, three averages came out. Sana's missing salary is skipped, so IT's average is just Imran's 65000.
**Likely follow-ups:**
- *What if I group by two columns?* Pass a list: `groupby(["department", "gender"])`.
- *Does groupby sort the groups?* Yes, by key, by default.
**Common mistakes:** Forgetting the aggregation (you only get a groupby object); expecting the group column to stay a normal column (it becomes the index).

### Q2 ⭐⭐⭐ 🟢 Write code to find the average salary by department from an employee DataFrame.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you write the most basic groupby cleanly?
**Say this in the interview:** "I group by department, pick the salary column and take the mean."
**Explain simply:**
- `groupby("department")` makes the groups; `["salary"]` picks the column; `.mean()` is the calculation.
- Missing values (NaN, meaning "no value") are skipped by default.
- Add `.reset_index()` if you want department back as a normal column.
**Sample data:** same `employees` table as Q1 (7 rows, Sana's salary is missing).
**Code (what you write in the interview):**
```python
average_salary = employees.groupby("department")["salary"].mean().reset_index()
print(average_salary)
```
**Output:**
```
  department   salary
0    Finance  80000.0
1         HR  55000.0
2         IT  65000.0
```
**What it means:** One row per department with its average pay.
**Alternative:** `employees.pivot_table(index="department", values="salary", aggfunc="mean")` gives the same numbers.
**Likely follow-ups:**
- *How do you round it?* Add `.round(0)` after `.mean()`.
- *How do you rename the column?* Use named aggregation (Q12).
**Common mistakes:** Using `employees.mean()` on the whole table; forgetting the column name in brackets, which averages every numeric column.

### Q3 ⭐⭐⭐ 🟢 Write code to count the number of employees in each department using groupby.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you pick the right counting method and know what it counts?
**Say this in the interview:** "I group by department and use size() to count rows, so every employee is counted, even if some columns are blank."
**Explain simply:**
- `size()` counts all rows in each group, including rows with missing values.
- `count()` counts only non-missing values in the column you pick (see Q4).
- Counting a column that is always filled, such as `emp_id`, gives the same answer as size.
**Sample data:** same `employees` table as Q1.
**Code (what you write in the interview):**
```python
headcount = employees.groupby("department").size()
print(headcount)
```
**Output:**
```
department
Finance    3
HR         2
IT         2
dtype: int64
```
**What it means:** Finance has 3 employees, HR 2, IT 2. Sana is counted in IT even though her salary is blank.
**Alternative:** `employees["department"].value_counts()` (sorted biggest first).
**Likely follow-ups:**
- *How do I get a normal table?* `.size().reset_index(name="headcount")`.
**Common mistakes:** Using `count()` on a column with blanks and under-counting people.

### Q4 ⭐⭐⭐ 🟢 What is the difference between size() and count() in a pandas groupby?
**Asked at:** commonly asked; PracHub's 2026 pandas-for-analysts page lists size vs count (snippet-level source).
**What the interviewer is checking:** Do you know that NaN changes the answer?
**Say this in the interview:** "size() counts rows including blanks, count() counts only the non-blank values in each column."
**Explain simply:**
- NaN means "missing value".
- `size()` returns one number per group: the number of rows.
- `count()` returns one number per column per group: how many cells are filled.
- If no column has blanks, both give the same number.
**Sample data:** same `employees` table as Q1 (Sana's salary is blank).
**Code (what you write in the interview):**
```python
print(employees.groupby("department")["salary"].size())
print(employees.groupby("department")["salary"].count())
```
**Output:**
```
department
Finance    3
HR         2
IT         2
Name: salary, dtype: int64
department
Finance    3
HR         2
IT         1
Name: salary, dtype: int64
```
**What it means:** IT has 2 employees (size) but only 1 salary on record (count).
**Likely follow-ups:**
- *Which do you use for headcount?* size(), because a person with a blank field is still a person.
**Common mistakes:** Using count() for headcount; also using count() as the denominator of a rate when blanks should be included.

### Q5 ⭐⭐⭐ 🟢 What is the difference between merge() and join() in pandas?
**Asked at:** commonly asked; merge vs join appears in several public question banks (Naukri Code360 and others, snippet-level).
**What the interviewer is checking:** Do you know join is a convenient shortcut for merge?
**Say this in the interview:** "merge joins on columns and is the flexible one. join is a shortcut that joins on the index by default. I use merge almost always."
**Explain simply:**
- `merge()` can join on any column name, or different names on each side (`left_on`, `right_on`). Default is an inner join.
- `join()` is a DataFrame method that matches on the index, and its default is a left join.
- Both do the same work underneath; join is just shorter when the keys are already the index.
- Join needs index set up first, which is an extra step.
**Sample data:** `employees` (Q1 plus `dept_id`) and a small `departments` table.
```python
departments = pd.DataFrame({
    "dept_id": [10, 20, 30, 50],
    "dept_name": ["Human Resources", "Finance", "IT", "Legal"],
})
```
**Code (what you write in the interview):**
```python
# merge: use the dept_id column directly
by_merge = employees.merge(departments, on="dept_id", how="left")

# join: first move dept_id into the index of both tables
by_join = employees.set_index("dept_id").join(departments.set_index("dept_id"))
print(by_join.head(3))
```
**Output:**
```
         emp_id   name department gender   salary        dept_name
dept_id                                                           
10            1   Asha         HR      F  50000.0  Human Resources
10            2   Ravi         HR      M  60000.0  Human Resources
20            3  Meena    Finance      F  70000.0          Finance
```
**What it means:** Same result either way; merge needs less setup. Note join moves dept_id into the index.
**Likely follow-ups:**
- *Which is the default join type?* merge: inner; join: left.
**Common mistakes:** Calling join on columns without setting the index (you get an overlap error or wrong matches).

### Q6 ⭐⭐⭐ 🟢 What join types does pd.merge() support through the how= argument, and how do they map to SQL joins?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you connect pandas to SQL joins you already know?
**Say this in the interview:** "how takes inner, left, right, outer and cross, and they match the SQL joins one to one."
**Explain simply:**

| how= | SQL | Rows kept |
|---|---|---|
| `"inner"` (default) | INNER JOIN | only keys found in both tables |
| `"left"` | LEFT JOIN | all left rows, blanks where no match |
| `"right"` | RIGHT JOIN | all right rows, blanks where no match |
| `"outer"` | FULL OUTER JOIN | all rows from both |
| `"cross"` | CROSS JOIN | every left row with every right row |

- Unmatched sides are filled with NaN (missing value).
- In HR terms: "employees with their department name" is a left join from employees.
**Likely follow-ups:**
- *Which one for an anti join?* left with `indicator=True` (Q17).
**Common mistakes:** Forgetting that the default is inner and silently losing employees whose department is missing from the lookup.

### Q7 ⭐⭐⭐ 🟢 Write code to left-merge an employee DataFrame with a department DataFrame on the column dept_id.
**Asked at:** commonly asked (no company-specific report found); merge tasks are described as common live-coding in PapersAdda 2026 (anecdotal).
**What the interviewer is checking:** Can you write a merge and explain what happens to unmatched rows?
**Say this in the interview:** "A left merge keeps every employee and adds the department name where dept_id matches. Employees with no match get a blank."
**Explain simply:**
- Left table (employees) is the one you keep in full.
- Employee Sana has dept_id 40, which is not in the department table, so her dept_name is NaN (missing).
- Department 50 (Legal) has no employees, so it does not appear.
**Sample data:** `employees` (7 rows with `dept_id`) and `departments` from Q5.
**Code (what you write in the interview):**
```python
employees_with_dept = employees.merge(departments, on="dept_id", how="left")
print(employees_with_dept[["name", "dept_id", "dept_name"]])
```
**Output:**
```
    name  dept_id        dept_name
0   Asha       10  Human Resources
1   Ravi       10  Human Resources
2  Meena       20          Finance
3  Karan       20          Finance
4  Divya       20          Finance
5  Imran       30               IT
6   Sana       40              NaN
```
**What it means:** All 7 employees are kept; Sana's department is unknown.
**Likely follow-ups:**
- *Check row count?* `len(employees_with_dept) == len(employees)` should be True if department ids are unique.
**Common mistakes:** Writing `how="inner"` by accident and dropping Sana; not checking for duplicate dept_id in the department table (Q16).

### Q8 ⭐⭐⭐ 🟢 What is the difference between merge() and concat() in pandas?
**Asked at:** commonly asked; merge vs concat is on public question banks (snippet-level).
**What the interviewer is checking:** Do you know one adds columns by matching, the other just stacks?
**Say this in the interview:** "merge matches rows by a key and adds columns, like a lookup or SQL join. concat just stacks tables on top of each other, like SQL UNION ALL, no matching."
**Explain simply:**
- `merge`: side by side, matched on a key column. Row count can change.
- `concat`: stacks vertically by default (`axis=0`); it lines up columns by name.
- Use concat for monthly files with the same layout; use merge to bring in data from another table.
**Sample data:** `jan` (2 rows) and `feb` (2 rows) with columns `emp_id`, `name`.
**Code (what you write in the interview):**
```python
# stack: no matching, just rows one after another
combined = pd.concat([jan, feb])
print(combined)
```
**Output:**
```
   emp_id   name
0       1   Asha
1       2   Ravi
2       3  Meena
3       4  Karan
```
**What it means:** 4 rows from 2 + 2; nothing was matched. (Here the index happened to continue; see Q33 for when it repeats.)
**Likely follow-ups:**
- *Can concat go sideways?* Yes, `axis=1`, but it matches on index, so merge is safer.
**Common mistakes:** Using concat when you need a lookup; using merge to stack files.

### Q9 ⭐⭐⭐ 🟢 What is pivot_table() in pandas, and how do you create one?
**Asked at:** commonly asked; pivot_table is a standard item on question banks (snippet-level).
**What the interviewer is checking:** Can you relate it to an Excel pivot table?
**Say this in the interview:** "It is the Excel pivot table in code: pick what goes in rows, what goes in columns, which value to summarise and how."
**Explain simply:**
- `index` = row labels, `columns` = column labels, `values` = the number to summarise, `aggfunc` = how (mean, sum, count). Default aggfunc is mean.
- It groups for you, so duplicates are fine (unlike `pivot`, see Q18).
- Missing combinations show as NaN (use `fill_value=0` to show 0).
- `margins=True` adds a Total row and column, like Excel's Grand Total.
**Sample data:** `employees` table from Q1 plus `gender`.
**Code (what you write in the interview):**
```python
headcount_table = employees.pivot_table(
    index="department",
    columns="gender",
    values="emp_id",
    aggfunc="count",
    fill_value=0,
)
print(headcount_table)
```
**Output:**
```
gender      F  M
department      
Finance     2  1
HR          1  1
IT          1  1
```
**What it means:** Headcount of each gender in each department, with empty cells shown as 0.
**Likely follow-ups:**
- *Difference from groupby?* Same idea; pivot_table lays the second key across columns.
**Common mistakes:** Forgetting `aggfunc` and getting averages when you wanted counts.

### Q10 ⭐⭐⭐ 🟢 Write code to build a pivot table of average salary with department as rows and gender as columns.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you write a pivot_table quickly with the right arguments?
**Say this in the interview:** "pivot_table with index department, columns gender, values salary, and aggfunc mean."
**Explain simply:**
- IT has no female employee with a salary (Sana's is blank), so that cell is NaN (missing).
- This is a good place to mention the pay gap analysis HR often asks for.
**Sample data:** `employees` table from Q1 plus `gender`.
**Code (what you write in the interview):**
```python
salary_table = employees.pivot_table(
    index="department",
    columns="gender",
    values="salary",
    aggfunc="mean",
)
print(salary_table)
```
**Output:**
```
gender            F        M
department                  
Finance     80000.0  80000.0
HR          50000.0  60000.0
IT              NaN  65000.0
```
**What it means:** Finance pays both genders the same on average; HR men earn 10000 more; IT has no female salary on record.
**Likely follow-ups:**
- *Show a total?* Add `margins=True`.
**Common mistakes:** Treating the NaN as zero pay; it just means no data.

### Q11 ⭐⭐⭐ 🟢 What is the difference between apply(), map() and applymap() in pandas?
**Asked at:** commonly asked; Towards Data Science and several question banks cover this (snippet-level).
**What the interviewer is checking:** Do you know which works on a column, a table or each cell?
**Say this in the interview:** "map works on one column element by element, often with a dictionary. apply runs a function over a column or over rows. applymap was for every cell of a table; it is now called DataFrame.map."
**Explain simply:**
- `Series.map(dict or function)`: one column, one value at a time; values not in the dictionary become NaN.
- `Series.apply(function)`: similar on one column; `DataFrame.apply(function, axis=1)` passes a whole row.
- `DataFrame.applymap`: every cell; renamed `DataFrame.map` in pandas 2.1 (renaming from memory; I ran `DataFrame.map` in pandas 3.0.5 and it works).
- All three are slow compared with vectorised maths like `employees["salary"] * 1.1` (see Q20).
**Sample data:** `employees` table from Q1.
**Code (what you write in the interview):**
```python
# map: swap a code for a label using a dictionary
print(employees["department"].map({"HR": "Human Resources"}).head(3))

# apply on a column: raise each salary by 10 percent
print(employees["salary"].apply(lambda salary: salary * 1.1).head(3))

# apply on rows: build a label from two columns
print(employees.apply(lambda row: row["name"] + "-" + row["department"], axis=1).head(2))
```
**Output:**
```
0    Human Resources
1    Human Resources
2                NaN
Name: department, dtype: str
0    55000.0
1    66000.0
2    77000.0
Name: salary, dtype: float64
0    Asha-HR
1    Ravi-HR
dtype: str
```
**What it means:** map replaced matched values and left NaN for "Finance", which was not in the dictionary; apply transformed each value or row.
**Likely follow-ups:**
- *Which is fastest?* Vectorised operations, then map, then apply.
**Common mistakes:** Using applymap in new code (it is deprecated); expecting map to keep unmatched values.

### Q12 ⭐⭐⭐ 🟡 Write code to group by department and compute headcount, average salary and maximum salary in one step using named aggregation.
**Asked at:** commonly asked; named aggregation is covered in freeacademy and similar lessons (snippet-level).
**What the interviewer is checking:** Can you produce a clean summary table in one go?
**Say this in the interview:** "I use agg with new_name equals a pair of column and function. It gives clean column names directly."
**Explain simply:**
- Each argument is `output_name=("source_column", "function")`.
- Count of `emp_id` gives headcount; `mean` and `max` ignore blank salaries.
- Add `.reset_index()` so department becomes a normal column.
**Sample data:** `employees` table from Q1.
**Code (what you write in the interview):**
```python
department_summary = employees.groupby("department").agg(
    headcount=("emp_id", "count"),
    average_salary=("salary", "mean"),
    max_salary=("salary", "max"),
).reset_index()
print(department_summary)
```
**Output:**
```
  department  headcount  average_salary  max_salary
0    Finance          3         80000.0     90000.0
1         HR          2         55000.0     60000.0
2         IT          2         65000.0     65000.0
```
**What it means:** One summary row per department with three measures.
**Alternative:** Older style `agg({"salary": ["mean", "max"]})` gives a two-level column header that is harder to read.
**Likely follow-ups:**
- *Use your own function?* Yes: `("salary", lambda s: s.max() - s.min())` for the pay range.
**Common mistakes:** Passing a dictionary of lists and ending up with a multi-level header; counting `salary` for headcount when blanks exist.

### Q13 ⭐⭐⭐ 🟡 What is the difference between agg() and transform() in a pandas groupby?
**Asked at:** commonly asked (no company-specific report found); transform is a recurring "senior" pandas question.
**What the interviewer is checking:** Do you know one shrinks the table and the other keeps the row count?
**Say this in the interview:** "agg returns one row per group. transform returns a result the same length as the original, so each row gets its group's value and I can add it as a column."
**Explain simply:**
- `agg` = summary table (3 departments gives 3 rows).
- `transform` = the group calculation broadcast back to every row (7 employees gives 7 values, in the original order).
- Use transform when you need the group number next to the individual (salary vs department average, share of total).
**Sample data:** `employees` table from Q1.
**Code (what you write in the interview):**
```python
print(employees.groupby("department")["salary"].agg("mean"))
print(employees.groupby("department")["salary"].transform("mean"))
```
**Output:**
```
department
Finance    80000.0
HR         55000.0
IT         65000.0
Name: salary, dtype: float64
0    55000.0
1    55000.0
2    80000.0
3    80000.0
4    80000.0
5    65000.0
6    65000.0
Name: salary, dtype: float64
```
**What it means:** Three rows from agg, seven from transform (one per employee).
**Likely follow-ups:**
- *Why not merge the agg result back?* transform does it in one step with no key.
**Common mistakes:** Trying to assign an agg result to a column (lengths do not match, so you get NaN or an error).

### Q14 ⭐⭐⭐ 🟡 Write code to add a column showing each employee's department average salary next to their own salary.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you reach for transform instead of a manual merge?
**Say this in the interview:** "groupby department, take salary, and transform with mean. That puts the department average on every employee row."
**Explain simply:**
- Result lines up with the original rows, so a simple column assignment works.
- You can then compare: `salary - dept_average_salary`.
**Sample data:** `employees` table from Q1.
**Code (what you write in the interview):**
```python
employees["dept_average_salary"] = employees.groupby("department")["salary"].transform("mean")
print(employees[["name", "department", "salary", "dept_average_salary"]])
```
**Output:**
```
    name department   salary  dept_average_salary
0   Asha         HR  50000.0              55000.0
1   Ravi         HR  60000.0              55000.0
2  Meena    Finance  70000.0              80000.0
3  Karan    Finance  80000.0              80000.0
4  Divya    Finance  90000.0              80000.0
5  Imran         IT  65000.0              65000.0
6   Sana         IT      NaN              65000.0
```
**What it means:** Divya earns 10000 above her Finance average; Sana's own salary is blank but she still sees her department's average.
**Alternative:** Build the averages with `groupby().mean()`, then `merge` them back on department; longer but fine.
**Likely follow-ups:**
- *Median instead?* Replace `"mean"` with `"median"`.
**Common mistakes:** Using `.mean()` instead of `.transform("mean")`, which gives a short table that does not fit as a column.

### Q15 ⭐⭐⭐ 🟡 Write code to find the top 3 highest-paid employees in each department.
**Asked at:** commonly asked; top-N per group is a classic live-coding task (no company-specific report found).
**What the interviewer is checking:** Can you combine sort and groupby, and know about ties?
**Say this in the interview:** "I sort by salary from highest to lowest, then group by department and take head(3). Each group keeps its first three rows, which are its top three."
**Explain simply:**
- Sorting first is the key; groupby keeps the sorted order inside each group.
- `head(3)` on a groupby returns up to 3 rows per group; groups with fewer people return what they have (IT has 2).
- Blank salaries sort to the end, so Sana appears last in IT only because IT has room.
- Ties are broken by position, not shared. For ties use `rank(method="min")`.
**Sample data:** `employees` table from Q1 (7 rows).
**Code (what you write in the interview):**
```python
top_paid = (
    employees
    .sort_values("salary", ascending=False)
    .groupby("department")
    .head(3)
)
print(top_paid[["name", "department", "salary"]])
```
**Output:**
```
    name department   salary
4  Divya    Finance  90000.0
3  Karan    Finance  80000.0
2  Meena    Finance  70000.0
1   Ravi         HR  60000.0
0   Asha         HR  50000.0
5  Imran         IT  65000.0
6   Sana         IT      NaN
```
**What it means:** Up to three best-paid people per department (shown here sorted by department by luck of the data; add a second sort if you need that order).
**Alternative:** `employees.groupby("department")["salary"].rank(ascending=False) <= 3` keeps ties together.
**Likely follow-ups:**
- *Only the single highest?* `head(1)` or `idxmax`.
**Common mistakes:** Calling head(3) without sorting first (you get the first three rows, not the highest); not dropping blank salaries when they matter.

### Q16 ⭐⭐⭐ 🟡 After a merge, your row count increased unexpectedly. What are the likely causes and how do you check?
**Asked at:** commonly asked; join cardinality (one-to-many surprises) is highlighted by PracHub's 2026 pandas-for-analysts page (snippet-level).
**What the interviewer is checking:** Do you understand duplicate keys multiply rows, and can you prove it?
**Say this in the interview:** "Almost always duplicate keys in the other table. If a key appears twice there, each matching row on my side is repeated twice. I check duplicates first, then use validate to catch it."
**Explain simply:**
- One employee matched to two rows in the lookup becomes two rows (a many-to-many or one-to-many join).
- Other causes: merging on the wrong column, or key columns with repeated values on both sides.
- Check duplicates in the lookup key with `duplicated()`, and compare `len()` before and after.
- `validate="many_to_one"` makes pandas raise an error if the right table has duplicate keys.
**Sample data:** `employees` (7 rows) and `dept_managers`, where dept 10 has two managers.
```python
dept_managers = pd.DataFrame({
    "dept_id": [10, 10, 20],
    "manager": ["A", "B", "C"],
})
```
**Code (what you write in the interview):**
```python
merged = employees.merge(dept_managers, on="dept_id", how="left")
print(len(employees), len(merged))

# how many duplicate keys are in the lookup table?
print(dept_managers["dept_id"].duplicated().sum())

# stop with an error if the lookup is not unique
employees.merge(dept_managers, on="dept_id", validate="many_to_one")
```
**Output:**
```
7 9
1
MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
```
**What it means:** 7 employees became 9 rows because dept 10 appears twice in the lookup; one duplicate key was found. The validate check gives a clear error (message shortened).
**Likely follow-ups:**
- *How do you fix it?* Drop duplicates in the lookup (`drop_duplicates("dept_id")`) or decide which manager to keep.
**Common mistakes:** Not comparing row counts before and after; deduplicating the wrong table.

### Q17 ⭐⭐⭐ 🟡 How do you find the rows in one DataFrame that have no match in another (an anti join) in pandas?
**Asked at:** commonly asked (no company-specific report found); anti join appears in reconciliation-style tasks.
**What the interviewer is checking:** Do you know pandas has no built-in anti join and can you build one?
**Say this in the interview:** "I left-merge with indicator=True and keep rows marked left_only. A shorter way is isin with a tilde to negate it."
**Explain simply:**
- Anti join means "rows in A that are not in B", like SQL's `LEFT JOIN ... WHERE b.key IS NULL`.
- `indicator=True` adds a `_merge` column saying `both`, `left_only` or `right_only`.
- HR use: employees whose department is not in the master list.
**Sample data:** `employees` and `departments` from Q5 (Sana's dept_id 40 is not in departments).
**Code (what you write in the interview):**
```python
checked = employees.merge(departments, on="dept_id", how="left", indicator=True)
no_match = checked[checked["_merge"] == "left_only"]
print(no_match[["name", "dept_id"]])
```
**Output:**
```
   name  dept_id
6  Sana       40
```
**What it means:** Sana is the only employee whose department does not exist in the department list.
**Alternative:** `employees[~employees["dept_id"].isin(departments["dept_id"])]` gives the same row (verified by running), and is shorter.
**Likely follow-ups:**
- *Rows in B not in A?* Swap the tables, or use `right_only`.
**Common mistakes:** Forgetting the `~`; using an inner merge and finding nothing; blank keys (NaN) never match, so they show as unmatched.

### Q18 ⭐⭐⭐ 🟡 What is the difference between pivot() and pivot_table() in pandas?
**Asked at:** commonly asked (no company-specific report found); the pivot vs pivot_table comparison appears in pandas question banks (Naukri Code360, Towards Data Science).
**What the interviewer is checking:** Whether you know that pivot() only reshapes and fails on duplicates, while pivot_table() summarises.
**Say this in the interview:** "pivot() just rearranges data, so every row/column pair must be unique or it errors. pivot_table() aggregates, like an Excel pivot, so it handles duplicates by averaging, summing or counting them."
**Explain simply:**
- A pivot turns values of one column (for example gender) into column headings.
- `pivot()` does no maths. It needs exactly one row for each department and gender pair, otherwise pandas raises `ValueError: Index contains duplicate entries, cannot reshape` (I ran this).
- `pivot_table()` has an `aggfunc` (aggregate function: mean, sum, count). The default is mean. It also offers `fill_value` and `margins` (totals).
- Rule of thumb: clean, unique data and pure reshaping, use `pivot()`. Real HR data with repeated rows, use `pivot_table()`.
**Sample data:** six employees; Finance has two female employees, so the pair (Finance, F) repeats.
**Code (what you write in the interview):**
```python
import pandas as pd

# One row per employee: department and gender repeat
employees = pd.DataFrame({
    "department": ["Finance", "Finance", "Finance", "HR", "HR", "IT"],
    "gender": ["F", "F", "M", "F", "M", "M"],
    "salary": [50000, 60000, 55000, 40000, 45000, 70000],
})

# pivot_table: duplicates (Finance + F twice) are combined with an aggregate
average_salary = employees.pivot_table(
    index="department", columns="gender", values="salary", aggfunc="mean"
)
print(average_salary)
```
**Output:**
```text
gender            F        M
department                  
Finance     55000.0  55000.0
HR          40000.0  45000.0
IT              NaN  70000.0
```
**What it means:** The two Finance women (50,000 and 60,000) were averaged to 55,000. IT has no female employee, so that cell is NaN (empty). `employees.pivot(...)` on the same data raises the duplicate error.
**Likely follow-ups:** 1) *How do you fill the NaN?* `fill_value=0` in pivot_table. 2) *When does pivot() work?* When each pair is unique, for example one headcount row per department per month.
**Common mistakes:** Using `pivot()` on data with repeats; forgetting that the default `aggfunc` is mean, so a count needs `aggfunc="count"`.

### Q19 ⭐⭐⭐ 🟡 Write code using apply() with a lambda to create a column that labels each employee 'High' or 'Low' by salary, and explain when a vectorised alternative is better.
**Asked at:** commonly asked (no company-specific report found); apply vs vectorised operations is a recurring theme in pandas prep material (Towards Data Science, PracHub).
**What the interviewer is checking:** Whether you can write the lambda, and whether you know a faster column-wise alternative exists.
**Say this in the interview:** "I call apply on the salary column with a lambda that returns High or Low. On big data I would use np.where instead, because it works on the whole column at once rather than one value at a time."
**Explain simply:**
- A lambda is a tiny one-line function with no name: `lambda s: ...` means "for each salary s, do this".
- `Series.apply()` calls that function once per value, in plain Python.
- Vectorised means the work is done on the entire column in fast compiled code. `np.where(condition, value_if_true, value_if_false)` is the vectorised version of an if/else.
- For a few hundred rows, either is fine. For hundreds of thousands, vectorised is far faster.
**Sample data:** four employees with salaries 30,000 to 90,000; cut-off 50,000.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": [30000, 65000, 48000, 90000],
})

# apply runs the lambda once for every salary
employees["level"] = employees["salary"].apply(lambda s: "High" if s >= 50000 else "Low")
print(employees)
```
**Output:**
```text
    name  salary level
0   Asha   30000   Low
1   Ravi   65000  High
2  Meena   48000   Low
3   John   90000  High
```
**What it means:** Anyone earning 50,000 or more is labelled High, the rest Low.
**Alternative:** vectorised, same result (I ran it and the output is identical):
```python
import numpy as np

employees["level"] = np.where(employees["salary"] >= 50000, "High", "Low")
```
**Likely follow-ups:** 1) *More than two labels?* `pd.cut` or `np.select`. 2) *What about missing salaries?* NaN is not >= 50000, so it becomes Low; handle NaN first if that is wrong.
**Common mistakes:** Forgetting the `else` in the lambda; using `apply` on the whole DataFrame instead of one column; writing `>` when the rule says "50,000 or more".

### Q20 ⭐⭐⭐ 🟡 Why is apply() with axis=1 slow, and what do you use instead?
**Asked at:** commonly asked (no company-specific report found); apply slowness is covered in prep articles (Towards Data Science "apply vs vectorized operations").
**What the interviewer is checking:** That you understand row-by-row Python is slow and know the column-wise fix.
**Say this in the interview:** "With axis=1, pandas builds a small Series for every row and runs a Python function on it, so it is a Python loop in disguise. I use column arithmetic, np.where or np.select instead, which run in fast compiled code."
**Explain simply:**
- `axis=1` means "go across each row". For 1 lakh rows, the function is called 1 lakh times and a new row object is built each time.
- Vectorised operations (`df["a"] * df["b"]`) process the whole column in one go in compiled code (C), with no Python loop.
- In a test on 200,000 rows on this machine: apply(axis=1) took about 0.96 seconds, column arithmetic about 0.002 seconds (roughly 500 times faster). Exact times vary by machine.
- Use apply(axis=1) only when the logic really cannot be written with columns (for example complicated text parsing across several fields).
**Sample data:** three employees with salary and bonus percentage.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena"],
    "salary": [30000, 65000, 48000],
    "bonus_percent": [5, 10, 8],
})

# Slow way: Python function called once per row
employees["bonus_slow"] = employees.apply(
    lambda row: row["salary"] * row["bonus_percent"] / 100, axis=1
)

# Fast way: work on whole columns at once
employees["bonus"] = employees["salary"] * employees["bonus_percent"] / 100
print(employees)
```
**Output:**
```text
    name  salary  bonus_percent  bonus_slow   bonus
0   Asha   30000              5      1500.0  1500.0
1   Ravi   65000             10      6500.0  6500.0
2  Meena   48000              8      3840.0  3840.0
```
**What it means:** Both columns give the same bonus; the second is the one to write in real work because it stays fast as data grows.
**Likely follow-ups:** 1) *Conditions across columns?* `np.where` or `np.select`. 2) *Is apply on one column also slow?* Yes, still a Python loop, but without the per-row object cost.
**Common mistakes:** Reaching for `apply(axis=1)` by habit; forgetting `axis=1` (then pandas applies the function per column and errors).

### Q21 ⭐⭐⭐ 🟡 You get a SettingWithCopyWarning after filtering a DataFrame and assigning a new column. What does it mean and how do you fix it?
**Asked at:** commonly asked (no company-specific report found); a classic pandas gotcha in question banks.
**What the interviewer is checking:** Whether you understand view vs copy and know the safe pattern: `.copy()` or `.loc`.
**Say this in the interview:** "pandas is warning that I may be changing a temporary slice rather than the real DataFrame, so my change may be lost. The fix is to call .copy() after filtering when I want a separate table, or to use .loc on the original when I want to change it."
**Explain simply:**
- Filtering (`df[df["department"] == "HR"]`) may give a view (a window onto the same data) or a copy (a separate table). Older pandas could not always tell, so it warned.
- Chained assignment means two steps in a row such as `df[mask]["salary"] = 0`. The first step may create a temporary copy, so the assignment can silently go nowhere.
- Fix 1: `hr_employees = df[mask].copy()`, then add columns freely.
- Fix 2: to change the original, use one step: `df.loc[mask, "salary"] = 0`.
- Version note (verified by running on pandas 3.0.5): with Copy-on-Write (pandas 3 default), a filtered result is always its own copy, so assigning a new column to it gives no warning and never touches the original. Chained assignment on the original does not work, and pandas raises a `ChainedAssignmentError` warning. `SettingWithCopyWarning` itself is what you meet on pandas 2.x and older (from memory, unverified here). Writing `.copy()` and `.loc` is correct in all versions.
**Sample data:** four employees in HR and IT.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "department": ["HR", "IT", "HR", "IT"],
    "salary": [30000, 65000, 48000, 90000],
})

# Take an independent copy of the filtered rows, then add the column
hr_employees = employees[employees["department"] == "HR"].copy()
hr_employees["salary_with_raise"] = hr_employees["salary"] * 1.10
print(hr_employees)
```
**Output:**
```text
    name department  salary  salary_with_raise
0   Asha         HR   30000            33000.0
2  Meena         HR   48000            52800.0
```
**What it means:** `hr_employees` is its own table, so adding a column is safe and the original `employees` is untouched. To change the original instead, write `employees.loc[employees["department"] == "HR", "salary"] = 0`.
**Likely follow-ups:** 1) *Should I silence the warning?* No, fix the cause. 2) *Why is the index 0 and 2?* The filter keeps the original row labels.
**Common mistakes:** Ignoring the warning; chaining `df[mask]["col"] = value` and expecting the original to change; using `.copy()` when you actually wanted to update the original.

### Q22 ⭐⭐⭐ 🟡 Write code to replicate Excel's VLOOKUP in pandas using merge.
**Asked at:** commonly asked (no company-specific report found); the Excel-to-pandas lookup is a standard live task for analysts switching from Excel.
**What the interviewer is checking:** That you can do a lookup with a left merge and know what happens for unmatched keys.
**Say this in the interview:** "VLOOKUP is a left merge: keep every row of my main table and bring in matching columns from the lookup table. Unmatched rows get NaN, which is Excel's #N/A."
**Explain simply:**
- The main table (employees) is the left table; the lookup table (departments) is the right table.
- `how="left"` keeps every employee even if no department is found.
- Unlike VLOOKUP, merge can bring in several columns at once, and it does not need the key to be the first column.
- VLOOKUP returns only the first match. A merge returns one row for every match, so duplicate keys in the lookup table multiply rows. Check the lookup key is unique first.
**Sample data:** employee John has dept_id 40, which is missing in the department table.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "dept_id": [10, 20, 10, 40],
})
departments = pd.DataFrame({
    "dept_id": [10, 20, 30],
    "dept_name": ["Finance", "HR", "IT"],
})

# Left merge keeps every employee, like VLOOKUP keeps every row of the main list
employees_with_dept = employees.merge(departments, on="dept_id", how="left")
print(employees_with_dept)
```
**Output:**
```text
    name  dept_id dept_name
0   Asha       10   Finance
1   Ravi       20        HR
2  Meena       10   Finance
3   John       40       NaN
```
**What it means:** Every employee is kept and gets a department name; John has no match, so his name is NaN, like #N/A in Excel.
**Likely follow-ups:** 1) *Row count went up?* Duplicate keys in the lookup table. 2) *Different key names?* `left_on` and `right_on` (see Q31).
**Common mistakes:** Using the default `how="inner"`, which silently drops unmatched employees; keys with different data types (text "10" vs number 10); not checking the lookup table for duplicates.

### Q23 ⭐⭐ 🟢 How do you group by two columns, for example department and location, and get the average salary for each pair?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you pass a list of columns to groupby and understand the multi-level result.
**Say this in the interview:** "I pass both columns as a list to groupby, pick the salary column and take the mean. I get one average for every department and location pair."
**Explain simply:**
- `groupby(["department", "location"])` makes one group for each unique pair, for example (HR, Pune).
- The result has a MultiIndex (two index levels), because both keys become the row labels.
- Only pairs that exist in the data appear (there is no IT in Hyderabad here, so no row for it).
- Column order in the list sets the nesting order of the output.
**Sample data:** six employees across three departments and two cities.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Finance", "Finance", "HR", "HR", "HR", "IT"],
    "location": ["Hyderabad", "Pune", "Hyderabad", "Hyderabad", "Pune", "Pune"],
    "salary": [50000, 60000, 40000, 44000, 45000, 70000],
})

# Pass both columns as a list, then take the mean of salary
average_salary = employees.groupby(["department", "location"])["salary"].mean()
print(average_salary)
```
**Output:**
```text
department  location 
Finance     Hyderabad    50000.0
            Pune         60000.0
HR          Hyderabad    42000.0
            Pune         45000.0
IT          Pune         70000.0
Name: salary, dtype: float64
```
**What it means:** HR in Hyderabad averages 42,000 (the mean of 40,000 and 44,000); HR in Pune is 45,000.
**Alternative:** add `.unstack()` to turn locations into columns, or use `as_index=False` to get plain columns (Q25).
**Likely follow-ups:** 1) *How to flatten to normal columns?* `.reset_index()`. 2) *More than one measure?* Named aggregation.
**Common mistakes:** Writing `groupby("department", "location")` without the list (the second argument means something else and raises an error); expecting empty pairs to show up.

### Q24 ⭐⭐ 🟢 After groupby, the group key becomes the index. How do you turn it back into a normal column?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know `reset_index()` and why the key was in the index.
**Say this in the interview:** "I call reset_index() on the result. It moves the group keys from the index back into ordinary columns and gives a fresh 0, 1, 2 numbering."
**Explain simply:**
- By default groupby uses the group key as the index (the row labels), not as a column.
- That is fine for lookups, but awkward for merging, exporting to Excel or plotting.
- `reset_index()` turns the index into a column. It returns a new object, so assign it back.
- The other route is to set `as_index=False` up front (Q25).
**Sample data:** five employees in three departments.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Finance", "Finance", "HR", "HR", "IT"],
    "salary": [50000, 60000, 40000, 44000, 70000],
})

average_salary = employees.groupby("department")["salary"].mean()

# Move the department index back into a normal column
average_salary = average_salary.reset_index()
print(average_salary)
```
**Output:**
```text
  department   salary
0    Finance  55000.0
1         HR  42000.0
2         IT  70000.0
```
**What it means:** The result is now an ordinary table with department and salary as columns.
**Likely follow-ups:** 1) *Does reset_index change the original?* No, it returns a new one. 2) *What does `drop=True` do?* It throws the index away instead of making a column.
**Common mistakes:** Not assigning the result back; using `drop=True` and losing the department names.

### Q25 ⭐⭐ 🟢 What is the effect of as_index=False in groupby, and how does it compare with reset_index()?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know both give a flat table, and how they differ.
**Say this in the interview:** "as_index=False keeps the group keys as normal columns from the start. reset_index() does the same afterwards. For a simple aggregation, the final table is the same."
**Explain simply:**
- `as_index=True` (default): keys go to the index.
- `as_index=False`: keys stay as columns, and the result already has a 0, 1, 2 index.
- `reset_index()` is a separate step after groupby. It also works on a Series result, and after any step, so it is more flexible.
- Detail: with `as_index=False` you must name the column you aggregate (`["salary"]`), or every other column is aggregated too.
**Sample data:** five employees in three departments.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Finance", "Finance", "HR", "HR", "IT"],
    "salary": [50000, 60000, 40000, 44000, 70000],
})

# as_index=False keeps department as a normal column from the start
average_salary = employees.groupby("department", as_index=False)["salary"].mean()
print(average_salary)
```
**Output:**
```text
  department   salary
0    Finance  55000.0
1         HR  42000.0
2         IT  70000.0
```
**What it means:** Same table as the `reset_index()` version in Q24: the department is a column, not the index.
**Likely follow-ups:** 1) *Which do you prefer?* `as_index=False` for a one-step flat result; `reset_index()` when chaining after other steps like `.size()` or `.sort_values()`.
**Common mistakes:** Thinking they give different data (they give the same table here); forgetting to name the column in brackets, so every other column is averaged too.

### Q26 ⭐⭐ 🟢 How do you sort the result of a groupby in descending order of the aggregated value?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you chain `sort_values(ascending=False)` after the aggregation.
**Say this in the interview:** "I aggregate first, then call sort_values with ascending=False. By default groupby sorts by the group key (department name), not by the value."
**Explain simply:**
- groupby orders the output by the group keys alphabetically. That is not the same as ordering by average salary.
- After `.mean()` the result is a Series (a single column with labels), so `sort_values(ascending=False)` sorts it high to low.
- If the result is a DataFrame with several columns, name the column: `sort_values("salary", ascending=False)`.
- Add `.head(3)` for "top 3 departments".
**Sample data:** five employees in three departments.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Finance", "Finance", "HR", "HR", "IT"],
    "salary": [50000, 60000, 40000, 44000, 70000],
})

average_salary = employees.groupby("department")["salary"].mean()

# Highest average first
average_salary = average_salary.sort_values(ascending=False)
print(average_salary)
```
**Output:**
```text
department
IT         70000.0
Finance    55000.0
HR         42000.0
Name: salary, dtype: float64
```
**What it means:** IT has the highest average salary, HR the lowest.
**Likely follow-ups:** 1) *How to break ties?* Pass a list of columns to `sort_values`. 2) *Where does NaN go?* To the end by default.
**Common mistakes:** Sorting before the groupby (does nothing useful); forgetting `ascending=False` (default is lowest first); using `sort=False` in groupby, which only controls key ordering.

### Q27 ⭐⭐ 🟢 Write code to find the number of employees by gender within each department as a table.
**Asked at:** commonly asked (no company-specific report found); a typical HR diversity-by-department task.
**What the interviewer is checking:** That you can produce a department-by-gender count table quickly.
**Say this in the interview:** "I use pd.crosstab with department as rows and gender as columns. It counts the rows for each pair and fills zero where there are none."
**Explain simply:**
- A crosstab (cross-tabulation) is a table of counts, with one variable down the side and another across the top.
- Missing combinations show 0, which is correct (nobody there), not NaN.
- This is the same as the groupby route with `.size().unstack()`, shown below.
**Sample data:** six employees; IT has no female employee.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Finance", "Finance", "Finance", "HR", "HR", "IT"],
    "gender": ["F", "M", "F", "F", "M", "M"],
})

# Departments down the side, genders across the top, counts inside
headcount_table = pd.crosstab(employees["department"], employees["gender"])
print(headcount_table)
```
**Output:**
```text
gender      F  M
department      
Finance     2  1
HR          1  1
IT          0  1
```
**What it means:** Finance has 2 women and 1 man; IT has no women.
**Alternative:** groupby version (I ran it and the table is identical):
```python
employees.groupby(["department", "gender"]).size().unstack(fill_value=0)
```
**Likely follow-ups:** 1) *Percentages instead of counts?* `normalize="index"` gives each row as shares that add up to 1. 2) *Add totals?* `margins=True`.
**Common mistakes:** Forgetting `fill_value=0` in the unstack version (gives NaN); using `count()` instead of `size()`.

### Q28 ⭐⭐ 🟢 What is the difference between value_counts() and groupby().size()?
**Asked at:** commonly asked (no company-specific report found); size vs count style questions are listed on PracHub.
**What the interviewer is checking:** That you know they count the same thing but differ in order and flexibility.
**Say this in the interview:** "Both count rows per group. value_counts() is a quick shortcut that sorts by count, biggest first. groupby().size() sorts by the group key and fits better into a longer groupby pipeline."
**Explain simply:**
- `value_counts()` works on one column (or a few) and returns counts sorted from highest to lowest by default.
- `groupby().size()` returns counts ordered by the group key (alphabetical here).
- Both include every row in the group, even with missing values in other columns. Missing values in the key itself: `value_counts()` drops NaN by default (`dropna=True`); groupby also drops NaN keys by default (`dropna=True`).
- Result names differ: value_counts gives a Series called `count` (pandas 2 and 3); size gives an unnamed Series. Use `.reset_index(name="headcount")` to get a clean table.
**Sample data:** six employees: 2 Finance, 3 HR, 1 IT.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Finance", "Finance", "HR", "HR", "HR", "IT"],
})

# Quick way: counts, biggest first
print(employees["department"].value_counts())

# groupby way: counts, in alphabetical order of department
print(employees.groupby("department").size())
```
**Output:**
```text
department
HR         3
Finance    2
IT         1
Name: count, dtype: int64
department
Finance    2
HR         3
IT         1
dtype: int64
```
**What it means:** Same counts (HR 3, Finance 2, IT 1); only the order differs.
**Likely follow-ups:** 1) *Percent share?* `value_counts(normalize=True)`. 2) *Make value_counts alphabetical?* Add `.sort_index()`.
**Common mistakes:** Assuming the same order; confusing `size()` (all rows) with `count()` (non-missing values only).

### Q29 ⭐⭐ 🟢 What does groupby() actually return, and how do you look at a single group such as the 'Finance' department?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know groupby is lazy (a recipe) and can fetch one group with `get_group`.
**Say this in the interview:** "groupby returns a DataFrameGroupBy object, which is not a table yet. It only remembers how the rows are split. Nothing is calculated until I apply something like mean(). To see one group I use get_group('Finance')."
**Explain simply:**
- The object is a plan: "split by department". Printing it shows only a memory address, like `<pandas.api.typing.DataFrameGroupBy object at 0x...>` (the address changes every run).
- `get_group("Finance")` returns the rows of that group as a normal DataFrame, with the original index labels.
- You can also loop with `for name, group in groups:` to see each group, useful for exploring.
- Equivalent without groupby: `employees[employees["department"] == "Finance"]`.
**Sample data:** five employees across Finance, HR, IT.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "department": ["Finance", "HR", "Finance", "IT", "HR"],
    "salary": [50000, 40000, 60000, 70000, 44000],
})

groups = employees.groupby("department")
print(groups)

# Look at one group
finance_employees = groups.get_group("Finance")
print(finance_employees)
```
**Output:**
```text
<pandas.api.typing.DataFrameGroupBy object at 0x7f296db08ec0>
    name department  salary
0   Asha    Finance   50000
2  Meena    Finance   60000
```
**What it means:** The first line is just the plan; the table below it holds the two Finance employees.
**Likely follow-ups:** 1) *How many groups?* `groups.ngroups`. 2) *What if the name does not exist?* `get_group` raises a KeyError.
**Common mistakes:** Expecting groupby alone to print a table; typing the group name with the wrong spelling or case.

### Q30 ⭐⭐ 🟢 Write code to find the number of unique candidates per recruitment source (nunique) from a hiring DataFrame.
**Asked at:** commonly asked (no company-specific report found); a typical recruitment-analytics task.
**What the interviewer is checking:** That you use `nunique()` so a candidate who applied twice is counted once.
**Say this in the interview:** "I group by source and call nunique on the candidate ID. That counts distinct candidates rather than rows, so repeat applications are not double counted."
**Explain simply:**
- `nunique()` means "number of unique values". It ignores repeats (and ignores NaN by default).
- `size()` or `count()` would count applications (rows), not people.
- In the sample, candidate 101 applied via LinkedIn and Naukri, and candidate 102 applied through Referral twice.
- A candidate can legitimately appear under two sources; each source counts them once.
**Sample data:** six applications.
**Code (what you write in the interview):**
```python
import pandas as pd

applications = pd.DataFrame({
    "candidate_id": [101, 102, 101, 103, 104, 102],
    "source": ["LinkedIn", "Referral", "Naukri", "LinkedIn", "Referral", "Referral"],
})

# Count each candidate once per source
unique_candidates = applications.groupby("source")["candidate_id"].nunique()
print(unique_candidates)
```
**Output:**
```text
source
LinkedIn    2
Naukri      1
Referral    2
Name: candidate_id, dtype: int64
```
**What it means:** Referral has 3 application rows but only 2 different people (102 and 104), so the answer is 2.
**Likely follow-ups:** 1) *Total unique candidates overall?* `applications["candidate_id"].nunique()` gives 4. 2) *Why does the total differ from the sum of the sources?* Candidate 101 appears in two sources.
**Common mistakes:** Using `count()` and counting applications; forgetting the column in brackets, so every column gets nunique.

### Q31 ⭐⭐ 🟢 How do you merge two DataFrames when the key column has different names, for example emp_id and employee_id?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know `left_on` and `right_on`.
**Say this in the interview:** "I use left_on for the key name in the left table and right_on for the key name in the right table. Because the names differ, both columns stay in the result, so I drop one afterwards."
**Explain simply:**
- `on=` only works when both tables use the same column name.
- `left_on="emp_id", right_on="employee_id"` tells pandas which two columns to match.
- Both key columns are kept in the result, since they have different names. Drop the extra one with `.drop(columns="employee_id")`.
- Another option: rename one column first (`payroll.rename(columns={"employee_id": "emp_id"})`) and then use `on="emp_id"`.
**Sample data:** an employees table and a payroll table with different key names.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "emp_id": [1, 2, 3],
    "name": ["Asha", "Ravi", "Meena"],
})
payroll = pd.DataFrame({
    "employee_id": [1, 2, 3],
    "salary": [50000, 40000, 60000],
})

# Tell pandas which column to use on each side
merged = employees.merge(payroll, left_on="emp_id", right_on="employee_id", how="left")
print(merged)
```
**Output:**
```text
   emp_id   name  employee_id  salary
0       1   Asha            1   50000
1       2   Ravi            2   40000
2       3  Meena            3   60000
```
**What it means:** Each employee is matched to their salary; `emp_id` and `employee_id` carry the same value, so you can drop one.
**Likely follow-ups:** 1) *Key made of two columns?* Pass lists to `left_on` and `right_on`, in the same order. 2) *Types differ (text vs number)?* Convert with `astype` first, or nothing matches (or pandas raises an error).
**Common mistakes:** Using `on=` with different names (KeyError); forgetting that both key columns remain.

### Q32 ⭐⭐ 🟢 Write code to stack the January, February and March attendance DataFrames into one DataFrame.
**Asked at:** commonly asked (no company-specific report found); a typical monthly-files task for HR/MIS analysts.
**What the interviewer is checking:** That you use `pd.concat` with a list to stack rows, not merge.
**Say this in the interview:** "I put the three DataFrames in a list and call pd.concat. It stacks them one below the other. I pass ignore_index=True to get a clean 0 to n numbering."
**Explain simply:**
- `concat` glues tables together along an axis. The default `axis=0` stacks rows (like copy and paste below).
- Columns are matched by name. A column missing from one table becomes NaN for those rows.
- Without `ignore_index`, the original index labels repeat (0, 1, 0, 1, 0, 1), which causes confusion when selecting by label.
- Real data has no month column unless you add one. See the alternative.
**Sample data:** three small monthly tables for employees 1 and 2.
**Code (what you write in the interview):**
```python
import pandas as pd

january = pd.DataFrame({"emp_id": [1, 2], "days_present": [22, 20]})
february = pd.DataFrame({"emp_id": [1, 2], "days_present": [19, 21]})
march = pd.DataFrame({"emp_id": [1, 2], "days_present": [23, 18]})

# Stack the three tables one below the other
attendance = pd.concat([january, february, march])
print(attendance)
```
**Output:**
```text
   emp_id  days_present
0       1            22
1       2            20
0       1            19
1       2            21
0       1            23
1       2            18
```
**What it means:** Six rows, two per month. The index repeats 0, 1; adding `ignore_index=True` fixes that (Q33). Note that this stacked table does not say which month each row belongs to.
**Alternative:** label each month while stacking (I ran it):
```python
attendance = pd.concat([january, february, march], keys=["Jan", "Feb", "Mar"], names=["month"]).reset_index(level="month")
```
This gives a `month` column with Jan, Feb, Mar (the index still repeats; add `.reset_index(drop=True)` for a clean one).
**Likely follow-ups:** 1) *Many monthly files?* Read them in a loop into a list, then one `pd.concat`. 2) *Different column names?* Rename first, or you get extra NaN columns.
**Common mistakes:** Using `merge` to stack; calling concat in a loop one frame at a time (slow); forgetting that no month column exists.

### Q33 ⭐⭐ 🟢 What does ignore_index=True do in pd.concat()?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you understand index labels and why duplicates are a problem.
**Say this in the interview:** "It throws away the old row labels and numbers the stacked result again from 0 to n minus 1, so there are no repeated index values."
**Explain simply:**
- Every DataFrame has an index (row labels). Each small table starts at 0.
- Plain concat keeps those labels, so after stacking you get repeats (0, 1, 0, 1).
- With repeats, `df.loc[0]` returns several rows, not one (I ran this and got two rows back).
- `ignore_index=True` gives a clean 0, 1, 2, 3 sequence. Use it when the old labels carry no meaning. Do not use it if the index holds something meaningful like an employee ID.
**Sample data:** two monthly tables.
**Code (what you write in the interview):**
```python
import pandas as pd

january = pd.DataFrame({"emp_id": [1, 2], "days_present": [22, 20]})
february = pd.DataFrame({"emp_id": [1, 2], "days_present": [19, 21]})

# Without ignore_index the labels 0, 1 would repeat
attendance = pd.concat([january, february], ignore_index=True)
print(attendance)
```
**Output:**
```text
   emp_id  days_present
0       1            22
1       2            20
2       1            19
3       2            21
```
**What it means:** Four rows with a fresh, unique index 0 to 3.
**Likely follow-ups:** 1) *Same effect after concat?* `reset_index(drop=True)`. 2) *Does it change the data?* No, only the index labels.
**Common mistakes:** Using it when the index is meaningful (such as employee IDs) and losing it; thinking it removes duplicate rows (it does not).

### Q34 ⭐⭐ 🟢 What is pd.crosstab(), and how does it differ from pivot_table()?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know crosstab is a counting shortcut and pivot_table is the general summary tool.
**Say this in the interview:** "crosstab builds a frequency table, counts of rows for each pair of categories, straight from columns. pivot_table is more general: it is called on a DataFrame and can sum, average or count any column. crosstab is basically a count-focused special case."
**Explain simply:**
- crosstab (cross-tabulation) takes the columns (Series) as arguments: `pd.crosstab(df["department"], df["gender"])`. The default is counting, with 0 for empty cells.
- `pivot_table` is a DataFrame method: you name `index`, `columns`, `values` and `aggfunc`. The default `aggfunc` is mean, and empty cells are NaN.
- crosstab extras: `normalize="index"` for row percentages (each row adds up to 1) and `margins=True` for totals. It can also take `values=` with `aggfunc=` for averages, giving the same result as pivot_table (I ran this).
- Rule of thumb: counting categories, crosstab. Anything with a number column, pivot_table.
**Sample data:** six employees with department, gender and salary.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Finance", "Finance", "Finance", "HR", "HR", "IT"],
    "gender": ["F", "M", "F", "F", "M", "M"],
    "salary": [50000, 55000, 60000, 40000, 45000, 70000],
})

# crosstab counts rows for each department and gender pair
print(pd.crosstab(employees["department"], employees["gender"]))

# pivot_table needs a values column and an aggregate, here the average salary
print(employees.pivot_table(index="department", columns="gender", values="salary", aggfunc="mean"))
```
**Output:**
```text
gender      F  M
department      
Finance     2  1
HR          1  1
IT          0  1
gender            F        M
department                  
Finance     55000.0  55000.0
HR          40000.0  45000.0
IT              NaN  70000.0
```
**What it means:** The first table is headcount (IT has 0 women). The second is average salary (IT shows NaN because there is nothing to average).
**Likely follow-ups:** 1) *Percentage of each department by gender?* `pd.crosstab(..., normalize="index")`, for example Finance F is 0.67. 2) *Which is faster to type for counts?* crosstab.
**Common mistakes:** Passing the column names as strings to crosstab without a DataFrame (it needs the Series); expecting NaN instead of 0 for empty cells in crosstab; forgetting that pivot_table defaults to mean, not count.

### Q35 ⭐⭐ 🟢 What is the purpose of the suffixes argument in merge()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know what happens when both tables have a column with the same name?
**Say this in the interview:** "If both tables have a non-key column with the same name, pandas has to rename them or they would clash. By default it adds _x and _y, and suffixes lets me choose meaningful names like _2025 and _2026."
**Explain simply:**
- A merge puts columns from two tables side by side. A key column (the one we match on) appears once; other same-named columns appear twice.
- Default names are `salary_x` (left table) and `salary_y` (right table), which tell the reader nothing.
- `suffixes=("_left", "_right")` takes two strings, first for the left table, second for the right.
- It only matters for columns that are NOT the merge key.

**Sample data:**
```python
import pandas as pd
employees_2025 = pd.DataFrame({"emp_id": [1, 2, 3], "salary": [50000, 60000, 55000]})
employees_2026 = pd.DataFrame({"emp_id": [1, 2, 3], "salary": [54000, 63000, 55000]})
```
**Code (what you write in the interview):**
```python
salary_comparison = employees_2025.merge(
    employees_2026,
    on="emp_id",
    suffixes=("_2025", "_2026"),
)
print(salary_comparison)
```
**Output:**
```
   emp_id  salary_2025  salary_2026
0       1        50000        54000
1       2        60000        63000
2       3        55000        55000
```
**What it means:** Each employee now shows both years' salary with clear column names, ready for a "pay change" calculation.
**Likely follow-ups:**
- *What if you pass the same suffix twice or an empty one?* Duplicate resulting names raise an error in recent pandas; an empty string on one side keeps that side's original name.
- *Alternative to suffixes?* Rename the columns before merging.

**Common mistakes:** Expecting suffixes to rename the key column; forgetting to rename and then guessing which of `_x`/`_y` is which table.

### Q36 ⭐⭐ 🟢 By default, are rows with NaN in the groupby key included in the result? How do you change that?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know groupby silently drops rows with a missing key?
**Say this in the interview:** "By default no: rows where the group key is NaN are dropped. I pass dropna=False to keep them as their own group."
**Explain simply:**
- NaN means a missing value (an employee with no department filled in).
- `groupby("department")` ignores those rows, so totals can look smaller than the real total without any warning.
- `dropna=False` keeps them as a separate group labelled NaN.
- Good habit: check how many keys are missing before trusting a group total.

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "department": ["HR", "IT", None, "IT", None],
    "salary": [50000, 70000, 40000, 80000, 45000],
})
```
**Code (what you write in the interview):**
```python
# default: rows with a missing department are dropped
print(employees.groupby("department")["salary"].sum())

# dropna=False keeps them as their own group (shown as NaN)
print(employees.groupby("department", dropna=False)["salary"].sum())
```
**Output:**
```
department
HR     50000
IT    150000
Name: salary, dtype: int64
department
HR      50000
IT     150000
NaN     85000
Name: salary, dtype: int64
```
**What it means:** The first total misses 85,000 of payroll belonging to people with no department; the second shows it.
**Likely follow-ups:**
- *Does this apply to NaN in the value column?* No, `sum`/`mean` skip NaN values by default; this is only about the key.

**Common mistakes:** Reconciling group totals to the grand total and not noticing a gap caused by missing keys.

### Q37 ⭐⭐ 🟢 Write code to map department codes ('FIN', 'HR', 'IT') to full department names using a dictionary and map().
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you do a simple lookup/recode with `map()`?
**Say this in the interview:** "I build a dictionary of code to name and call map() on the column. Any code not in the dictionary becomes NaN, so I check for that."
**Explain simply:**
- A dictionary is a set of "code: name" pairs.
- `Series.map(dict)` looks up every value of the column in the dictionary.
- Values not found become NaN (here, "OPS"), which is a useful way to spot unexpected codes.
- Use `.fillna(...)` afterwards if you want a default instead.

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "dept_code": ["FIN", "HR", "IT", "IT", "OPS"],
})
```
**Code (what you write in the interview):**
```python
dept_names = {"FIN": "Finance", "HR": "Human Resources", "IT": "Information Technology"}

employees["department"] = employees["dept_code"].map(dept_names)
print(employees)
```
**Output:**
```
    name dept_code              department
0   Asha       FIN                 Finance
1   Ravi        HR         Human Resources
2  Meena        IT  Information Technology
3   John        IT  Information Technology
4  Priya       OPS                     NaN
```
**What it means:** Known codes became full names; the unknown "OPS" shows NaN, flagging a code missing from the dictionary.
**Alternative:** `replace(dept_names)` keeps unknown values unchanged instead of making them NaN (see Q67).
**Likely follow-ups:**
- *Keep the original when no match?* `employees["dept_code"].map(dept_names).fillna(employees["dept_code"])`.

**Common mistakes:** Not noticing the NaNs for unmapped codes; stray spaces or lowercase in the data so nothing matches.

### Q38 ⭐⭐ 🟢 Why does a KeyError appear after a groupby aggregation when you refer to the grouping column, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that the group key becomes the index?
**Say this in the interview:** "After groupby, the grouping column moves into the index, so it is no longer a normal column and asking for it gives KeyError. I fix it with reset_index(), or as_index=False in the groupby."
**Explain simply:**
- The result of `groupby("department")["salary"].mean()` is labelled by department; those labels live in the index (row labels), not in a column.
- `result["department"]` looks for a column, finds none, and raises `KeyError: 'department'`.
- `reset_index()` moves the labels back to a normal column.
- Or use `result.index` to read them as they are.

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "department": ["HR", "IT", "IT", "HR"],
    "salary": [50000, 70000, 80000, 60000],
})
```
**Code (what you write in the interview):**
```python
avg_salary = employees.groupby("department")["salary"].mean()

# avg_salary["department"] raises KeyError: 'department' is now the index, not a column.
# Fix: turn the index back into a column.
avg_salary = avg_salary.reset_index()
print(avg_salary["department"])
```
**Output:**
```
0    HR
1    IT
Name: department, dtype: str
```
(Without `reset_index()`, the real error printed was `KeyError 'department'`.)
**What it means:** After `reset_index()` the department is an ordinary column again and can be used in merges, filters and charts.
**Alternative:** `employees.groupby("department", as_index=False)["salary"].mean()` does it in one step.
**Likely follow-ups:**
- *as_index=False vs reset_index()?* Same result here (Q25).

**Common mistakes:** Re-running `groupby` on the result by the same column name; assuming the column "disappeared".

### Q39 ⭐⭐ 🟡 Write code to calculate the attrition rate (percentage of leavers) by department.
**Asked at:** commonly asked (no company-specific report found); HR-flavoured version of a standard groupby task
**What the interviewer is checking:** Can you turn a status into 1/0 and use a group average as a rate?
**Say this in the interview:** "I make a 1/0 flag for leavers; the mean of that flag per department is the share of leavers, so times 100 gives the attrition percentage."
**Explain simply:**
- Attrition rate = leavers divided by headcount, as a percentage.
- A flag of 1 for "Left" and 0 otherwise means sum = leavers and count = headcount, so mean = leavers / headcount.
- Simple version uses the employee list as the base; real HR often uses average headcount over the period, so state the definition you are using.

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "department": ["HR", "HR", "IT", "IT", "IT", "Finance"],
    "status": ["Left", "Active", "Active", "Left", "Left", "Active"],
})
```
**Code (what you write in the interview):**
```python
# 1 for a leaver, 0 for everyone else
employees["left"] = (employees["status"] == "Left").astype(int)

# the average of 1s and 0s is the share of leavers
attrition_rate = employees.groupby("department")["left"].mean() * 100
print(attrition_rate.round(1))
```
**Output:**
```
department
Finance     0.0
HR         50.0
IT         66.7
Name: left, dtype: float64
```
**What it means:** Two of the three IT employees left (66.7%), one of two in HR (50%), and nobody in Finance.
**Likely follow-ups:**
- *Why not divide in two steps?* You can: leavers = sum, headcount = size, rate = leavers / headcount.

**Common mistakes:** Forgetting to convert True/False to a number format when displaying; using a percentage of total leavers (a different question, see Q82) instead of within-department rate.

### Q40 ⭐⭐ 🟡 Write code to show each employee's salary as a percentage of their department's total payroll.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know `transform()` returns a value for every row?
**Say this in the interview:** "I use groupby with transform('sum') to get the department total on every row, then divide each salary by it."
**Explain simply:**
- `agg("sum")` gives one row per department; `transform("sum")` gives the same department total repeated on each employee row, so the lengths match.
- That makes row-by-row division easy.
- Percentages within each department add up to 100.

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "department": ["HR", "HR", "IT", "IT", "IT"],
    "salary": [40000, 60000, 50000, 70000, 80000],
})
```
**Code (what you write in the interview):**
```python
# department total, repeated on every row of that department
department_payroll = employees.groupby("department")["salary"].transform("sum")

employees["pct_of_dept_payroll"] = (employees["salary"] / department_payroll * 100).round(1)
print(employees)
```
**Output:**
```
    name department  salary  pct_of_dept_payroll
0   Asha         HR   40000                 40.0
1   Ravi         HR   60000                 60.0
2  Meena         IT   50000                 25.0
3   John         IT   70000                 35.0
4  Priya         IT   80000                 40.0
```
**What it means:** Asha's pay is 40% of the HR payroll; the three IT shares add to 100%.
**Likely follow-ups:**
- *Why not agg?* It returns fewer rows, so you would need a merge back.

**Common mistakes:** Using `agg` and getting a length mismatch; dividing by the company total instead of the department total.

### Q41 ⭐⭐ 🟡 Write code to keep only the departments that have more than 10 employees using groupby().filter().
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know `filter` works on whole groups, not rows?
**Say this in the interview:** "groupby().filter() keeps or drops entire groups based on a condition about the group. Here the condition is that the group has more than 10 rows."
**Explain simply:**
- Normal filtering (`df[df.salary > x]`) tests each row.
- `groupby().filter(func)` calls the function once per department; if it returns True, all that department's rows are kept.
- `len(group)` is the number of employees in that department.
- The result keeps the original rows and columns, not a summary.

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "department": ["IT"] * 12 + ["HR"] * 4 + ["Finance"] * 11,
    "salary": range(30000, 30000 + 27 * 1000, 1000),
})
```
**Code (what you write in the interview):**
```python
big_departments = employees.groupby("department").filter(lambda group: len(group) > 10)

print(big_departments["department"].value_counts())
```
**Output:**
```
department
IT         12
Finance    11
Name: count, dtype: int64
```
**What it means:** HR (4 people) is dropped; IT and Finance stay with all their rows.
**Alternative:** `employees[employees.groupby("department")["salary"].transform("size") > 10]` is faster on big data.
**Likely follow-ups:**
- *Does filter return one row per group?* No, it returns the original employee rows.

**Common mistakes:** Expecting a summary table; using `> 10` when the question means "10 or more".

### Q42 ⭐⭐ 🟡 Write code to find the department whose average salary is above the company-wide average.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you compare group averages against an overall number?
**Say this in the interview:** "I compute the company average once, the average per department, and keep the departments where the average is higher."
**Explain simply:**
- Company-wide average comes from all employees, not from the average of department averages (these differ when team sizes differ).
- Department averages come from `groupby().mean()`.
- Filtering a Series with a True/False condition keeps only matching departments.

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "department": ["HR", "HR", "IT", "IT", "Finance", "Finance"],
    "salary": [40000, 50000, 80000, 90000, 60000, 62000],
})
```
**Code (what you write in the interview):**
```python
company_average = employees["salary"].mean()
department_average = employees.groupby("department")["salary"].mean()

above_average = department_average[department_average > company_average]
print("Company average:", company_average)
print(above_average)
```
**Output:**
```
Company average: 63666.666666666664
department
IT    85000.0
Name: salary, dtype: float64
```
**What it means:** Only IT pays on average more than the company average of about 63,667.
**Likely follow-ups:**
- *What if departments differ a lot in size?* Mention that the company average is weighted by headcount; that is why we use all rows.

**Common mistakes:** Averaging the department averages; comparing with `>=` when the question says "above".

### Q43 ⭐⭐ 🟡 Write code to calculate a running (cumulative) total of sales within each region.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you do a window-style calculation per group with `cumsum()`?
**Say this in the interview:** "I sort by region and month first, then groupby region and use cumsum, so the total restarts for each region."
**Explain simply:**
- A running total adds each new value to everything before it.
- `groupby("region")["sales"].cumsum()` does this separately per region.
- It follows the current row order, so sort by date first or the total is meaningless.

**Sample data:**
```python
import pandas as pd
sales = pd.DataFrame({
    "region": ["North", "North", "North", "South", "South", "South"],
    "month": ["2026-01", "2026-02", "2026-03", "2026-01", "2026-02", "2026-03"],
    "sales": [100, 150, 120, 80, 90, 110],
})
```
**Code (what you write in the interview):**
```python
# order matters for a running total
sales = sales.sort_values(["region", "month"])

sales["running_total"] = sales.groupby("region")["sales"].cumsum()
print(sales)
```
**Output:**
```
  region    month  sales  running_total
0  North  2026-01    100            100
1  North  2026-02    150            250
2  North  2026-03    120            370
3  South  2026-01     80             80
4  South  2026-02     90            170
5  South  2026-03    110            280
```
**What it means:** North's total climbs 100, 250, 370; South starts again from 80.
**Likely follow-ups:**
- *Other cumulative functions?* `cumcount`, `cummax`, `cumprod`.

**Common mistakes:** Not sorting by date; using `cumsum()` without groupby, so the total carries into the next region.

### Q44 ⭐⭐ 🟡 Write code to rank employees by salary within each department.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you do the pandas version of SQL `RANK() OVER (PARTITION BY ...)`?
**Say this in the interview:** "groupby department, then rank on salary with ascending=False so the highest paid is rank 1. I choose method='min' so ties share a rank like SQL RANK."
**Explain simply:**
- `rank()` gives a position number; by default it is ascending (lowest = 1), so set `ascending=False`.
- The default method averages tied ranks (giving 2.5); `method="min"` gives ties the lower rank (SQL RANK), `method="dense"` gives no gaps (SQL DENSE_RANK).
- Output is a float; add `.astype(int)` if needed (when there are no NaN).

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya", "Kiran"],
    "department": ["HR", "HR", "HR", "IT", "IT", "IT"],
    "salary": [50000, 60000, 50000, 90000, 70000, 80000],
})
```
**Code (what you write in the interview):**
```python
# rank 1 = highest salary; tied salaries share the same rank
employees["salary_rank"] = (
    employees.groupby("department")["salary"].rank(method="min", ascending=False)
)
print(employees.sort_values(["department", "salary_rank"]))
```
**Output:**
```
    name department  salary  salary_rank
1   Ravi         HR   60000          1.0
0   Asha         HR   50000          2.0
2  Meena         HR   50000          2.0
3   John         IT   90000          1.0
5  Kiran         IT   80000          2.0
4  Priya         IT   70000          3.0
```
**What it means:** Asha and Meena tie at rank 2 in HR; each department is ranked on its own.
**Likely follow-ups:**
- *Rank 1 to N with no ties?* `method="first"`.

**Common mistakes:** Leaving ascending=True (rank 1 is the lowest paid); ranking the whole company rather than per department.

### Q45 ⭐⭐ 🟡 Write code to compare each month's headcount with the previous month for every department using shift().
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you use `shift()` within groups so departments do not leak into each other?
**Say this in the interview:** "I sort by department and month, then groupby department and shift(1), which moves each row's value down one so every month sees last month's headcount."
**Explain simply:**
- `shift(1)` moves values down one row; the first row of each group becomes NaN (no previous month).
- Doing it inside `groupby` stops HR's last month leaking into IT's first month.
- Change = this month minus previous month.

**Sample data:**
```python
import pandas as pd
headcount = pd.DataFrame({
    "department": ["HR", "HR", "HR", "IT", "IT", "IT"],
    "month": ["2026-01", "2026-02", "2026-03", "2026-01", "2026-02", "2026-03"],
    "headcount": [20, 22, 21, 50, 48, 55],
})
```
**Code (what you write in the interview):**
```python
# months must be in order within each department
headcount = headcount.sort_values(["department", "month"])

headcount["previous_month"] = headcount.groupby("department")["headcount"].shift(1)
headcount["change"] = headcount["headcount"] - headcount["previous_month"]
print(headcount)
```
**Output:**
```
  department    month  headcount  previous_month  change
0         HR  2026-01         20             NaN     NaN
1         HR  2026-02         22            20.0     2.0
2         HR  2026-03         21            22.0    -1.0
3         IT  2026-01         50             NaN     NaN
4         IT  2026-02         48            50.0    -2.0
5         IT  2026-03         55            48.0     7.0
```
**What it means:** HR grew by 2 then dropped by 1; IT dipped by 2 and then rose by 7; each department's first month has no comparison.
**Alternative:** `groupby("department")["headcount"].diff()` gives the change directly.
**Likely follow-ups:**
- *Why floats?* NaN in the first row forces a float column.

**Common mistakes:** `shift()` without groupby; not sorting; month stored as text in a non-sortable format like "Jan", "Feb".

### Q46 ⭐⭐ 🟡 How do you merge on two columns, for example employee ID and month?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a composite key and its row-multiplying risk?
**Say this in the interview:** "I pass a list to on, like on=['emp_id','month']. A row matches only if both values match, which is what I need when an employee has one record per month."
**Explain simply:**
- Employee ID alone repeats every month, so merging on it would pair every January row with every February row (row explosion).
- A list in `on=[...]` means "match on both columns together".
- If the names differ, use `left_on=[...]` and `right_on=[...]` as lists in the same order.

**Sample data:**
```python
import pandas as pd
attendance = pd.DataFrame({
    "emp_id": [1, 1, 2, 2],
    "month": ["Jan", "Feb", "Jan", "Feb"],
    "days_present": [20, 18, 22, 21],
})
payroll = pd.DataFrame({
    "emp_id": [1, 1, 2, 2],
    "month": ["Jan", "Feb", "Jan", "Feb"],
    "net_pay": [48000, 46000, 55000, 55000],
})
```
**Code (what you write in the interview):**
```python
combined = attendance.merge(payroll, on=["emp_id", "month"], how="left")
print(combined)
```
**Output:**
```
   emp_id month  days_present  net_pay
0       1   Jan            20    48000
1       1   Feb            18    46000
2       2   Jan            22    55000
3       2   Feb            21    55000
```
**What it means:** Each employee-month matched exactly one payroll row, so 4 rows stay 4 rows.
**Likely follow-ups:**
- *How do you check it did not multiply rows?* Compare row counts before and after, or use `validate="1:1"` (Q47).

**Common mistakes:** Merging on emp_id alone; month stored differently in the two tables ("Jan" vs "2026-01").

### Q47 ⭐⭐ 🟡 What does the validate argument in merge() do, and when would you use it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you protect merges against silent duplicates?
**Say this in the interview:** "validate checks the relationship between the tables, like one-to-one or many-to-one. If the data breaks that rule, pandas raises an error instead of quietly multiplying rows. I use it when I expect a lookup table to have unique keys."
**Explain simply:**
- Options: `"1:1"`, `"1:m"`, `"m:1"`, `"m:m"` (m:m checks nothing).
- `"m:1"` means many rows on the left, but each key must appear only once on the right (a lookup).
- Failure raises `MergeError` immediately, so bad data is caught at the merge step.
- Use it for ID-to-department, ID-to-salary-grade lookups, and any merge in a recurring report.

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({"emp_id": [1, 2, 3], "name": ["Asha", "Ravi", "Meena"]})
# emp_id 2 is accidentally listed twice
departments = pd.DataFrame({"emp_id": [1, 2, 2, 3], "department": ["HR", "IT", "Finance", "IT"]})
```
**Code (what you write in the interview):**
```python
# "m:1" means: many employee rows, but each emp_id appears once in departments
merged = employees.merge(departments, on="emp_id", how="left", validate="m:1")
```
**Output:**
```
MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
```
(The message continues by listing the duplicated key, emp_id 2.)
**What it means:** The merge stopped because emp_id 2 appears twice in the lookup; without validate, Ravi would silently appear twice.
**Likely follow-ups:**
- *Why not just drop_duplicates?* Only after deciding which duplicate is right; here Ravi has two departments, a data problem to resolve.

**Common mistakes:** Using the wrong direction (`"1:m"` instead of `"m:1"`); treating validate as a fix rather than a check.

### Q48 ⭐⭐ 🟡 What does indicator=True do in merge(), and how do you use the _merge column?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you see which side each row came from, for reconciliation and anti joins?
**Say this in the interview:** "indicator=True adds a _merge column saying whether each row matched in both tables, only the left, or only the right. I filter on it to find unmatched records."
**Explain simply:**
- Values: `both`, `left_only`, `right_only`.
- With `how="outer"` you see all three; filtering `left_only` gives an anti join (rows with no match on the right).
- Use it to check that a merge matched as expected, e.g. HRMS vs payroll.

**Sample data:**
```python
import pandas as pd
hrms = pd.DataFrame({"emp_id": [1, 2, 3, 4], "name": ["Asha", "Ravi", "Meena", "John"]})
payroll = pd.DataFrame({"emp_id": [2, 3, 4, 5], "salary": [60000, 50000, 70000, 45000]})
```
**Code (what you write in the interview):**
```python
merged = hrms.merge(payroll, on="emp_id", how="outer", indicator=True)
print(merged)

# employees in HRMS but missing from payroll
print(merged[merged["_merge"] == "left_only"])
```
**Output:**
```
   emp_id   name   salary      _merge
0       1   Asha      NaN   left_only
1       2   Ravi  60000.0        both
2       3  Meena   50000.0        both
3       4   John  70000.0        both
4       5    NaN  45000.0  right_only
   emp_id  name  salary     _merge
0       1  Asha      NaN   left_only
```
**What it means:** Asha is in HRMS but not payroll; emp_id 5 is in payroll but not HRMS.
**Likely follow-ups:**
- *Rename the column?* `indicator="source"`.

**Common mistakes:** Forgetting that unmatched rows have NaN in the other table's columns, which is not the same as the value being missing in the original.

### Q49 ⭐⭐ 🟡 After a merge, integer columns turn into floats. Why does this happen and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand NaN forces a float column?
**Say this in the interview:** "Whole-number columns can't hold NaN, so when a left merge has unmatched rows and fills them with NaN, pandas converts the column to float. I fill the gaps, for example with 0, and convert back with astype(int), or use the nullable Int64 type if I need to keep the gaps."
**Explain simply:**
- The default integer type has no way to store 'missing', but floats do (NaN).
- Unmatched rows in a left/right/outer merge create missing values, so the column becomes float (5000 becomes 5000.0).
- Fix 1: `fillna(0).astype(int)` when zero is a sensible default.
- Fix 2: `astype("Int64")` (capital I) keeps whole numbers with a proper missing marker.

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({"emp_id": [1, 2, 3, 4], "name": ["Asha", "Ravi", "Meena", "John"]})
bonuses = pd.DataFrame({"emp_id": [1, 2, 3], "bonus": [5000, 3000, 4000]})
```
**Code (what you write in the interview):**
```python
merged = employees.merge(bonuses, on="emp_id", how="left")
print(merged.dtypes)

# fix: fill the gap with 0, then convert back to whole numbers
merged["bonus"] = merged["bonus"].fillna(0).astype(int)
print(merged)
```
**Output:**
```
emp_id      int64
name          str
bonus     float64
dtype: object
   emp_id   name  bonus
0       1   Asha   5000
1       2   Ravi   3000
2       3  Meena   4000
3       4   John      0
```
**What it means:** John had no bonus record, so bonus became float; after filling with 0 it is a whole number again.
**Likely follow-ups:**
- *Is 0 always right?* No: for "no data" you may prefer to keep it missing (use `Int64`).

**Common mistakes:** Calling `astype(int)` before filling NaN (raises an error); filling with 0 when the gap really means "unknown".

### Q50 ⭐⭐ 🟡 A merge returns zero matching rows even though the IDs look the same. What would you check?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you debug key mismatches methodically?
**Say this in the interview:** "I check the data types of both key columns, then print the raw values to look for hidden spaces, different case, or leading zeros, and clean both sides the same way before merging."
**Explain simply:**
- Values that look identical can differ invisibly: `"E101"` vs `"E101 "` (trailing space) vs `"e101"` (case).
- Number vs text: if one side is a number and the other text, pandas raises a `ValueError` about merging int64 and str (in pandas 3 that is what I saw); in older versions it could return no matches. Convert with `astype`.
- Also check leading zeros (`007` vs `7`) and Excel-style IDs that became decimals (`101.0`).
- `isin()` quickly counts how many keys match.

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({"emp_id": ["E101", "E102", "E103"], "name": ["Asha", "Ravi", "Meena"]})
payroll = pd.DataFrame({"emp_id": ["e101 ", "e102 ", "e103 "], "salary": [50000, 60000, 55000]})
```
**Code (what you write in the interview):**
```python
# 1. how many keys match at all?
print(employees["emp_id"].isin(payroll["emp_id"]).sum())

# 2. look at the raw values (spaces and case are invisible in a table)
print(payroll["emp_id"].tolist())

# fix: same case and no stray spaces on both sides
payroll["emp_id"] = payroll["emp_id"].str.strip().str.upper()

merged = employees.merge(payroll, on="emp_id", how="left")
print(merged)
```
**Output:**
```
0
['e101 ', 'e102 ', 'e103 ']
  emp_id   name  salary
0   E101   Asha   50000
1   E102   Ravi   60000
2   E103  Meena   55000
```
**What it means:** Zero keys matched because of lowercase letters and trailing spaces; after cleaning, all three match.
**Likely follow-ups:**
- *Other causes?* Wrong column chosen, wrong join type (`inner` with no overlap), or the data genuinely does not overlap.

**Common mistakes:** Cleaning only one side; trusting how the values look on screen.

### Q51 ⭐⭐ 🟡 Write code to merge an employees table with an attendance table and calculate each employee's attendance percentage.
**Asked at:** commonly asked (no company-specific report found); HR-flavoured merge task
**What the interviewer is checking:** Can you combine a merge with a simple calculation, and think about employees with no record?
**Say this in the interview:** "I left merge employees with attendance on emp_id so nobody drops out, then attendance percentage is days present divided by working days times 100. Employees with no attendance record get NaN, which I would flag rather than hide."
**Explain simply:**
- Left merge keeps every employee from the employees table.
- Attendance % = days present / working days x 100.
- John has no attendance record: his values are NaN, so the percentage is NaN (not 0%). That is a data gap to raise, not a real zero.
- Note the columns turn into floats because of the NaN (see Q49).

**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "emp_id": [1, 2, 3, 4],
    "name": ["Asha", "Ravi", "Meena", "John"],
})
attendance = pd.DataFrame({
    "emp_id": [1, 2, 3],
    "days_present": [20, 18, 22],
    "working_days": [22, 22, 22],
})
```
**Code (what you write in the interview):**
```python
# left merge keeps every employee, even without attendance records
merged = employees.merge(attendance, on="emp_id", how="left")

merged["attendance_pct"] = (merged["days_present"] / merged["working_days"] * 100).round(1)
print(merged)
```
**Output:**
```
   emp_id   name  days_present  working_days  attendance_pct
0       1   Asha          20.0          22.0            90.9
1       2   Ravi          18.0          22.0            81.8
2       3  Meena          22.0          22.0           100.0
3       4   John           NaN           NaN             NaN
```
**What it means:** Asha attended 90.9% of working days; John shows NaN because the attendance table has no row for him.
**Likely follow-ups:**
- *If attendance has several rows per employee (daily)?* Aggregate first (sum days present per employee), then merge, to avoid duplicating employee rows.

**Common mistakes:** Using an inner merge and silently losing employees; dividing by the wrong denominator (calendar days instead of working days); merging before aggregating a many-row-per-employee table.

### Q52 ⭐⭐ 🟡 Write code to merge a payroll table with a deductions table and compute net pay, treating missing deductions as zero.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you pick a left merge, and do you handle the NaN that a left merge creates before doing the maths?
**Say this in the interview:** "I merge with how='left' so no employee drops out of payroll. Employees with no deduction row get NaN, so I fill that with 0 before subtracting."
**Explain simply:**
- Net pay (take-home) is gross pay minus deductions such as tax or PF.
- A left merge keeps every row of the left table (payroll) and attaches matches from the right (deductions).
- Where there is no match, pandas puts NaN (a "missing value" marker). NaN in a subtraction makes the whole answer NaN, so fill it first.
**Sample data:**
```python
import pandas as pd
payroll = pd.DataFrame({"emp_id": [101, 102, 103, 104], "gross_pay": [50000, 62000, 45000, 70000]})
deductions = pd.DataFrame({"emp_id": [101, 103, 104], "deduction": [5000, 3000, 8500]})
```
**Code (what you write in the interview):**
```python
# keep every payroll row, even if the employee has no deduction
payroll_with_deductions = payroll.merge(deductions, on="emp_id", how="left")

# no deduction row means zero deduction
payroll_with_deductions["deduction"] = payroll_with_deductions["deduction"].fillna(0)

payroll_with_deductions["net_pay"] = payroll_with_deductions["gross_pay"] - payroll_with_deductions["deduction"]
print(payroll_with_deductions)
```
**Output:**
```
   emp_id  gross_pay  deduction  net_pay
0     101      50000     5000.0  45000.0
1     102      62000        0.0  62000.0
2     103      45000     3000.0  42000.0
3     104      70000     8500.0  61500.0
```
**What it means:** Employee 102 had no deduction row, so their net pay equals gross pay (62000) instead of NaN.
**Alternative:** `payroll["gross_pay"] - payroll_with_deductions["deduction"].fillna(0)` in one line, without changing the column.
**Likely follow-ups:**
- What if deductions has two rows per employee? Rows double and pay is counted twice; sum deductions per employee first with groupby.
- Why not an inner merge? It would silently drop employees with no deductions.
**Common mistakes:** Using an inner merge (drops people); forgetting fillna so net pay becomes NaN; filling the whole table with 0 instead of just the deduction column.

### Q53 ⭐⭐ 🟡 What does an outer merge return, and how do you handle the NaN values it creates?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know outer keeps unmatched rows from both sides, and that NaN is expected, not an error?
**Say this in the interview:** "An outer merge returns every row from both tables, matched where possible. Unmatched rows get NaN in the other table's columns. I then fill, or flag, those NaN depending on what they mean."
**Explain simply:**
- Outer join (SQL: FULL OUTER JOIN) = matched rows + left-only rows + right-only rows.
- NaN here means "this ID is not in the other list". That can be the real finding, for example someone in the HR system but not in payroll.
- Handle it with `fillna()` for numbers or labels, or keep NaN and filter with `isna()` to list the gaps.
- Add `indicator=True` if you want to see which side each row came from.
**Sample data:**
```python
import pandas as pd
hrms = pd.DataFrame({"emp_id": [1, 2, 3], "name": ["Asha", "Ravi", "Meena"]})
payroll = pd.DataFrame({"emp_id": [2, 3, 4], "salary": [60000, 52000, 48000]})
```
**Code (what you write in the interview):**
```python
both_lists = hrms.merge(payroll, on="emp_id", how="outer")
print(both_lists)

# fill the gaps column by column
both_lists["name"] = both_lists["name"].fillna("Unknown")
both_lists["salary"] = both_lists["salary"].fillna(0)
print(both_lists)
```
**Output:**
```
   emp_id   name   salary
0       1   Asha      NaN
1       2   Ravi  60000.0
2       3  Meena  52000.0
3       4    NaN  48000.0
   emp_id     name   salary
0       1     Asha      0.0
1       2     Ravi  60000.0
2       3    Meena  52000.0
3       4  Unknown  48000.0
```
**What it means:** Employee 1 is in HR but not payroll; employee 4 is in payroll but not HR. Both survive the outer merge.
**Likely follow-ups:**
- Should you always fill with 0? No. 0 salary is a made-up number; sometimes leaving NaN or flagging is more honest.
**Common mistakes:** Filling NaN blindly and hiding a real data gap; using `fillna(0)` on text columns; expecting integers to stay integers (they become floats when NaN appears).

### Q54 ⭐⭐ 🟡 Write code to build a pivot table of headcount by department and month, with row and column totals.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build an Excel-style pivot in pandas, including totals?
**Say this in the interview:** "I use pivot_table with department as rows, month as columns, count of employee IDs as the value, and margins=True for the totals."
**Explain simply:**
- A pivot table reshapes a long list into a grid: one row per department, one column per month.
- `aggfunc="count"` counts how many rows fall into each cell.
- `margins=True` adds a total row and total column (the "Grand Total" in Excel).
- Month columns come out in alphabetical order (Feb before Jan) when they are text; use real dates or reorder the columns if order matters.
**Sample data:**
```python
import pandas as pd
records = pd.DataFrame({
    "emp_id": [1, 2, 3, 4, 5, 6, 7],
    "department": ["HR", "HR", "IT", "IT", "IT", "HR", "IT"],
    "month": ["Jan", "Jan", "Jan", "Jan", "Feb", "Feb", "Feb"],
})
```
**Code (what you write in the interview):**
```python
headcount = pd.pivot_table(
    records,
    index="department",
    columns="month",
    values="emp_id",
    aggfunc="count",   # count the employees in each cell
    margins=True,      # adds the total row and total column
    margins_name="Total",
)
print(headcount)
```
**Output:**
```
month       Feb  Jan  Total
department                 
HR            1    2      3
IT            2    2      4
Total         3    4      7
```
**What it means:** IT had 2 people in February and 2 in January; the company total across both months is 7 records.
**Alternative:** `pd.crosstab(records["department"], records["month"], margins=True)` gives the same counts with less typing.
**Likely follow-ups:**
- How is this different from groupby? Same maths; pivot_table just lays the result out as a grid.
**Common mistakes:** Using `aggfunc="sum"` on an ID column; forgetting that totals add up records, not unique people (a person in two months counts twice).

### Q55 ⭐⭐ 🟡 What do the fill_value, margins and aggfunc arguments do in pivot_table()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the three most-used pivot_table options and what each changes?
**Say this in the interview:** "aggfunc is how to summarise each cell (default mean), fill_value replaces empty cells, and margins adds the grand totals."
**Explain simply:**
- `aggfunc`: the summary used in each cell, such as "sum", "count", "mean" or a list of them. Default is mean, a common surprise.
- `fill_value`: what to put in cells with no data. Without it you get NaN.
- `margins`: True adds an "All" row and column, like Grand Total in an Excel pivot.
**Sample data:**
```python
import pandas as pd
sales = pd.DataFrame({
    "region": ["North", "North", "South", "South", "East"],
    "product": ["A", "B", "A", "A", "B"],
    "amount": [100, 200, 150, 50, 300],
})
```
**Code (what you write in the interview):**
```python
summary = sales.pivot_table(
    index="region",
    columns="product",
    values="amount",
    aggfunc="sum",
    fill_value=0,
    margins=True,
)
print(summary)
```
**Output:**
```
product    A    B  All
region               
East       0  300  300
North    100  200  300
South    200    0  200
All      300  500  800
```
**What it means:** East never sold product A, so that cell shows 0 (not NaN) because of `fill_value=0`. The All row and column are the totals.
**Likely follow-ups:**
- What if you leave out aggfunc? You get averages, which is wrong if you wanted totals.
**Common mistakes:** Forgetting the default is mean; using `fill_value` and then being surprised the All totals still look right (they are computed from real data, not the filled zeros).

### Q56 ⭐⭐ 🟡 How do you apply more than one aggregation function (sum and mean) to a column in pivot_table()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know aggfunc accepts a list, and do you understand the resulting two-level columns?
**Say this in the interview:** "I pass a list to aggfunc, like ['sum', 'mean']. The result has two column levels: the function on top, then the original columns."
**Explain simply:**
- `aggfunc=["sum", "mean"]` computes both for each cell.
- The top column level is the function name, the lower level is the pivot's columns (here location).
- Different functions for different columns: pass a dictionary, for example `{"salary": "sum", "age": "mean"}`.
- NaN means no employees in that department and location.
**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "department": ["HR", "HR", "IT", "IT", "IT"],
    "location": ["Pune", "Pune", "Pune", "Delhi", "Delhi"],
    "salary": [40000, 50000, 70000, 80000, 90000],
})
```
**Code (what you write in the interview):**
```python
salary_summary = employees.pivot_table(
    index="department",
    columns="location",
    values="salary",
    aggfunc=["sum", "mean"],
)
print(salary_summary)
```
**Output:**
```
                 sum              mean         
location       Delhi     Pune    Delhi     Pune
department                                     
HR               NaN  90000.0      NaN  45000.0
IT          170000.0  70000.0  85000.0  70000.0
```
**What it means:** IT in Delhi has a total payroll of 170000 and an average of 85000. HR has nobody in Delhi, so NaN.
**Likely follow-ups:**
- How to get one function's block? `salary_summary["mean"]`.
**Common mistakes:** Forgetting the columns are two-level and indexing with a single name; reading NaN as zero.

### Q57 ⭐⭐ 🟡 What does melt() do, and when do you use it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand wide vs long format and that melt is the reverse of a pivot?
**Say this in the interview:** "melt turns a wide table, where months are separate columns, into a long table with one row per employee per month. I use it when I need to group, filter or plot by month."
**Explain simply:**
- Wide format: one column per month (Jan, Feb, Mar), easy to read, hard to analyse.
- Long format: one column called month and one called value, easy for groupby and charts.
- `id_vars` are the columns that stay put; the rest are "melted" into rows.
- `var_name` and `value_name` name the two new columns.
**Sample data:**
```python
import pandas as pd
attendance = pd.DataFrame({
    "emp_id": [1, 2],
    "Jan": [22, 20],
    "Feb": [19, 21],
    "Mar": [21, 22],
})
```
**Code (what you write in the interview):**
```python
attendance_long = attendance.melt(
    id_vars="emp_id",          # columns to keep as they are
    var_name="month",          # the old column names go here
    value_name="days_present", # the old cell values go here
)
print(attendance_long)
```
**Output:**
```
   emp_id month  days_present
0       1   Jan            22
1       2   Jan            20
2       1   Feb            19
3       2   Feb            21
4       1   Mar            21
5       2   Mar            22
```
**What it means:** 2 employees times 3 months gives 6 rows, one per employee per month.
**Likely follow-ups:**
- How do you go back to wide? `pivot` or `pivot_table`.
**Common mistakes:** Forgetting `id_vars`, so the ID gets melted too; leaving default column names `variable` and `value`.

### Q58 ⭐⭐ 🟡 What do stack() and unstack() do, and how are they related to pivot tables?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you see that unstack is how a grouped result becomes a pivot grid, and stack is the reverse?
**Say this in the interview:** "unstack moves the inner index level into columns, making a wide table. stack does the opposite. groupby followed by unstack gives the same grid as a pivot table."
**Explain simply:**
- After `groupby` on two columns you get a result with a two-level index (department, then gender).
- `unstack()` takes the last level (gender) and makes it columns: a pivot-style grid.
- `stack()` squeezes columns back into an index level: long format again.
- Note: missing combinations become NaN after unstack, and stack drops those NaN rows by default.
**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "department": ["HR", "HR", "IT", "IT", "IT"],
    "gender": ["F", "M", "F", "M", "M"],
})
```
**Code (what you write in the interview):**
```python
headcount = employees.groupby(["department", "gender"]).size()
print(headcount)

wide_table = headcount.unstack()      # inner level (gender) becomes columns
print(wide_table)

long_again = wide_table.stack()       # back to one long column
print(long_again)
```
**Output:**
```
department  gender
HR          F         1
            M         1
IT          F         1
            M         2
dtype: int64
gender      F  M
department      
HR          1  1
IT          1  2
department  gender
HR          F         1
            M         1
IT          F         1
            M         2
dtype: int64
```
**What it means:** Same numbers, two shapes: long (one row per pair) and wide (a grid).
**Likely follow-ups:**
- Which level moves? The last one by default; `unstack(0)` moves the first.
**Common mistakes:** Mixing up which level moves; forgetting `fill_value=0` in unstack when you want zeros instead of NaN.

### Q59 ⭐⭐ 🟡 How do you replicate Excel's SUMIFS in pandas?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you translate an Excel habit into a boolean filter plus sum, and know groupby does it for all categories at once?
**Say this in the interview:** "I filter rows with conditions joined by &, select the amount column, and call sum. If I need it for every category, groupby does that in one line."
**Explain simply:**
- SUMIFS = add up a column only for rows meeting conditions.
- In pandas: build True/False conditions, combine with `&` (and) or `|` (or), keep each condition in brackets.
- `.loc[condition, "amount"]` picks the matching rows of one column; `.sum()` adds them.
**Sample data:**
```python
import pandas as pd
sales = pd.DataFrame({
    "region": ["North", "North", "South", "North", "South"],
    "product": ["A", "B", "A", "A", "B"],
    "amount": [100, 200, 150, 50, 300],
})
```
**Code (what you write in the interview):**
```python
# one condition, like SUMIF
north_total = sales.loc[sales["region"] == "North", "amount"].sum()
print(north_total)

# two conditions, like SUMIFS
north_a_total = sales.loc[(sales["region"] == "North") & (sales["product"] == "A"), "amount"].sum()
print(north_a_total)

# the same sum for every region at once
print(sales.groupby("region")["amount"].sum())
```
**Output:**
```
350
150
region
North    350
South    450
Name: amount, dtype: int64
```
**What it means:** North sold 350 in total, of which 150 was product A.
**Likely follow-ups:**
- COUNTIFS equivalent? Same filter, then `len()` or `.sum()` on the True/False condition.
**Common mistakes:** Using `and` instead of `&`; leaving out the brackets around each condition (gives an error); an empty match returns 0, not an error.

### Q60 ⭐⭐ 🟡 Write code to find the employee with the highest salary in each department using idxmax().
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know idxmax returns the row label, and that you then use loc to fetch the full row?
**Say this in the interview:** "groupby department, take idxmax of salary to get the row label of the top earner, then loc those labels to get the full rows."
**Explain simply:**
- `max()` gives the highest salary but loses the name.
- `idxmax()` gives the index label (row number) where the max sits, so you can fetch the whole row.
- It returns only one row per group; if two people tie, only the first is returned.
**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "Kiran", "Sana"],
    "department": ["HR", "HR", "IT", "IT", "IT"],
    "salary": [50000, 60000, 80000, 95000, 70000],
})
```
**Code (what you write in the interview):**
```python
# row label of the highest salary in each department
top_row_labels = employees.groupby("department")["salary"].idxmax()

# pull those full rows
highest_paid = employees.loc[top_row_labels]
print(highest_paid)
```
**Output:**
```
    name department  salary
1   Ravi         HR   60000
3  Kiran         IT   95000
```
**What it means:** Ravi leads HR and Kiran leads IT.
**Alternative:** `employees.sort_values("salary", ascending=False).groupby("department").head(1)`; this also works and is easy to extend to top N.
**Likely follow-ups:**
- How to keep ties? Use `rank(method="min")` or compare salary to `transform("max")`.
**Common mistakes:** Expecting idxmax to return the salary or the name; fails on a column with all NaN; assuming ties are returned.

### Q61 ⭐⭐ 🟡 Write code to apply a custom function that labels performance rating bands to every row.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you write a small function and apply it to a column?
**Say this in the interview:** "I write a plain function that takes one rating and returns a band, then call apply on the rating column. For large data I would switch to np.select or pd.cut."
**Explain simply:**
- A function is a reusable recipe: rating goes in, band comes out.
- `apply(function)` runs that recipe on every value of the column, one at a time.
- Put the strictest condition first, because `if/elif` stops at the first match.
**Sample data:**
```python
import pandas as pd
reviews = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "Kiran"],
    "rating": [4.6, 3.8, 2.4, 3.1],
})
```
**Code (what you write in the interview):**
```python
def rating_band(rating):
    if rating >= 4.5:
        return "Outstanding"
    elif rating >= 3.5:
        return "Meets expectations"
    else:
        return "Needs improvement"

reviews["band"] = reviews["rating"].apply(rating_band)
print(reviews)
```
**Output:**
```
    name  rating                band
0   Asha     4.6         Outstanding
1   Ravi     3.8  Meets expectations
2  Meena     2.4   Needs improvement
3  Kiran     3.1   Needs improvement
```
**What it means:** Each employee gets a band based on their own rating.
**Alternative:** `pd.cut(reviews["rating"], bins=[0, 3.5, 4.5, 5], labels=[...], right=False)`; faster for big tables.
**Likely follow-ups:**
- What about a missing rating? NaN fails every `>=` test and lands in the else branch ("Needs improvement"), which is wrong; handle it with `pd.isna(rating)` first.
**Common mistakes:** Conditions in the wrong order; forgetting `return`; using `apply` on the whole DataFrame when one column is enough.

### Q62 ⭐⭐ 🟡 How do you pass extra arguments to a function used in apply()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know apply forwards extra arguments, so you avoid hard-coded numbers or messy lambdas?
**Say this in the interview:** "Anything after the function name in apply is passed to the function. For example apply(label_salary, cutoff=60000)."
**Explain simply:**
- apply calls your function once per value (or per row with `axis=1`).
- Extra keyword arguments written inside `apply(...)` are handed to your function each time.
- This keeps the function reusable: change the cutoff without editing the function.
- A lambda also works: `apply(lambda s: label_salary(s, 60000))`, but extra arguments are cleaner.
**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({"name": ["Asha", "Ravi", "Meena"], "salary": [50000, 80000, 65000]})
```
**Code (what you write in the interview):**
```python
def label_salary(salary, cutoff, high_label="High", low_label="Low"):
    if salary >= cutoff:
        return high_label
    return low_label

# extra values go after the function name
employees["level"] = employees["salary"].apply(label_salary, cutoff=60000)
print(employees)

# row-wise version: extra keywords work the same way
def bonus(row, rate):
    return row["salary"] * rate

employees["bonus"] = employees.apply(bonus, axis=1, rate=0.1)
print(employees)
```
**Output:**
```
    name  salary level
0   Asha   50000   Low
1   Ravi   80000  High
2  Meena   65000  High
    name  salary level   bonus
0   Asha   50000   Low  5000.0
1   Ravi   80000  High  8000.0
2  Meena   65000  High  6500.0
```
**What it means:** The cutoff and the bonus rate are inputs, not hard-coded inside the function.
**Likely follow-ups:**
- Positional extras? Use `args=(60000,)` on a Series apply.
**Common mistakes:** Calling the function with brackets (`apply(label_salary())`); passing the extra value as the first argument; forgetting `axis=1` when the function needs the full row.

### Q63 ⭐⭐ 🟡 Write code to assign a grade ('A', 'B', 'C') from a score using np.select or np.where instead of apply().
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know vectorised options that are faster and shorter than apply?
**Say this in the interview:** "np.select takes a list of conditions and a list of results, and the first true condition wins. np.where is for a simple yes/no. Both run on the whole column at once, so they are much faster than apply."
**Explain simply:**
- "Vectorised" means the work is done on the entire column in one go, not row by row in Python.
- `np.select(conditions, choices, default=...)` is like nested IFs in Excel.
- `np.where(condition, value_if_true, value_if_false)` is like a single IF.
- Order matters: put the highest threshold first.
**Sample data:**
```python
import pandas as pd
import numpy as np
students = pd.DataFrame({"name": ["Asha", "Ravi", "Meena", "Kiran"], "score": [85, 72, 55, 90]})
```
**Code (what you write in the interview):**
```python
conditions = [
    students["score"] >= 80,
    students["score"] >= 60,
]
grades = ["A", "B"]

# the first matching condition wins; everything else gets "C"
students["grade"] = np.select(conditions, grades, default="C")
print(students)

# np.where for just two outcomes
students["result"] = np.where(students["score"] >= 60, "Pass", "Fail")
print(students)
```
**Output:**
```
    name  score grade
0   Asha     85     A
1   Ravi     72     B
2  Meena     55     C
3  Kiran     90     A
    name  score grade result
0   Asha     85     A   Pass
1   Ravi     72     B   Pass
2  Meena     55     C   Fail
3  Kiran     90     A   Pass
```
**What it means:** 72 matches both conditions, but the first listed (>= 80) fails and the second passes, so B.
**Likely follow-ups:**
- Missing score? NaN fails every condition and gets the default "C"; set the default or handle NaN explicitly.
**Common mistakes:** Wrong condition order; forgetting `default` with text choices (numpy 2.5 raises a dtype error; with numbers it fills 0); using `and` instead of `&` when combining conditions.

### Q64 ⭐⭐ 🟡 Write code to bucket employees into tenure bands (0-1, 1-3, 3+ years) with pd.cut and count each band.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you bin a number into ranges and understand which edge belongs to which bin?
**Say this in the interview:** "pd.cut takes bin edges and labels. By default each bin includes its right edge, so 1.0 year is in 0-1 and 3.0 is in 1-3. Then value_counts counts each band."
**Explain simply:**
- Binning = turning a number (tenure in years) into a group (band).
- Edges `[0, 1, 3, inf]` make three bins: (0,1], (1,3], (3, infinity).
- `right=True` (default) means the upper edge is included.
- Use `float("inf")` for the open-ended "3+" bin.
**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "Kiran", "Sana", "Dev"],
    "tenure_years": [0.5, 1.0, 2.5, 3.0, 7.2, 0.9],
})
```
**Code (what you write in the interview):**
```python
tenure_bands = pd.cut(
    employees["tenure_years"],
    bins=[0, 1, 3, float("inf")],
    labels=["0-1", "1-3", "3+"],
    right=True,   # 1.0 goes in "0-1", 3.0 goes in "1-3"
)
employees["tenure_band"] = tenure_bands
print(employees["tenure_band"].value_counts().sort_index())
```
**Output:**
```
tenure_band
0-1    3
1-3    2
3+     1
Name: count, dtype: int64
```
**What it means:** 3 people have up to 1 year, 2 have 1 to 3 years, and 1 has more than 3.
**Likely follow-ups:**
- Tenure of exactly 0? With the first edge at 0 and `right=True`, 0 is excluded and becomes NaN; start the bins at -1 or use `include_lowest=True`.
- Equal-sized groups instead? `pd.qcut`.
**Common mistakes:** Labels count not equal to bins minus one (error); the edge case above; forgetting `sort_index()`, so value_counts orders by size instead of band.

### Q65 ⭐⭐ 🟡 After agg() with several functions, the columns become a MultiIndex. How do you flatten them?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the clean fix (named aggregation) as well as the manual flatten?
**Say this in the interview:** "The easiest fix is named aggregation, which gives flat names from the start. If I already have a MultiIndex, I join the two levels with an underscore and reset the index."
**Explain simply:**
- A MultiIndex on columns is a two-level header, like ("salary", "mean").
- Joining the two parts with `"_".join(...)` makes one flat name like `salary_mean`.
- `reset_index()` turns the grouping key (department) from the index back into a normal column.
- Named aggregation, `name=(column, function)`, avoids the problem entirely.
**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({
    "department": ["HR", "HR", "IT", "IT", "IT"],
    "salary": [40000, 50000, 70000, 80000, 90000],
    "age": [30, 35, 28, 40, 45],
})
```
**Code (what you write in the interview):**
```python
summary = employees.groupby("department").agg({"salary": ["count", "mean"], "age": ["max"]})
print(summary)

# join the two levels into one name, then bring department back as a column
summary.columns = ["_".join(column) for column in summary.columns]
summary = summary.reset_index()
print(summary)

# or avoid the problem: named aggregation gives flat names directly
summary = employees.groupby("department").agg(
    headcount=("salary", "count"),
    avg_salary=("salary", "mean"),
    oldest=("age", "max"),
)
print(summary)
```
**Output:**
```
           salary          age
            count     mean max
department                     
HR              2  45000.0  35
IT              3  80000.0  45
  department  salary_count  salary_mean  age_max
0         HR             2      45000.0       35
1         IT             3      80000.0       45
            headcount  avg_salary  oldest
department                               
HR              2     45000.0      35
IT              3     80000.0      45
```
**What it means:** The same numbers, but now every column has one clear name you can use in later code.
**Likely follow-ups:**
- Why does a MultiIndex hurt? You must write `df[("salary", "mean")]`, which is awkward to export or merge.
**Common mistakes:** Joining before columns are all strings; forgetting that the grouping key stays in the index until `reset_index()`.

### Q66 ⭐⭐ 🟡 What is the difference between concat() with axis=0 and axis=1, and what happens when the indexes do not match?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know axis=0 stacks rows, axis=1 sits side by side by index, and that mismatches create NaN?
**Say this in the interview:** "axis=0 stacks tables on top of each other. axis=1 places them side by side, lining rows up by index label. Where an index label is in one table but not the other, the gaps are filled with NaN."
**Explain simply:**
- axis=0 (default): add more rows; use it for monthly files with the same columns.
- axis=1: add more columns; rows are matched by index label, not by position.
- Default `join="outer"` keeps every label from both sides, hence NaN. `join="inner"` keeps only the common labels.
- With axis=0, `ignore_index=True` gives a fresh 0, 1, 2 numbering.
**Sample data:**
```python
import pandas as pd
jan = pd.DataFrame({"emp_id": [1, 2], "days": [22, 20]})
feb = pd.DataFrame({"emp_id": [1, 2], "days": [19, 21]})
names = pd.DataFrame({"name": ["Asha", "Ravi", "Meena"]}, index=[0, 1, 2])
salaries = pd.DataFrame({"salary": [50000, 60000]}, index=[1, 2])
```
**Code (what you write in the interview):**
```python
# axis=0: stack rows
print(pd.concat([jan, feb], ignore_index=True))

# axis=1: side by side, matched on the index
print(pd.concat([names, salaries], axis=1))
```
**Output:**
```
   emp_id  days
0       1    22
1       2    20
2       1    19
3       2    21
    name   salary
0   Asha      NaN
1   Ravi  50000.0
2  Meena  60000.0
```
**What it means:** Asha has index 0, which `salaries` lacks, so her salary is NaN. The salaries lined up with Ravi and Meena by label, not by order.
**Likely follow-ups:**
- Is this the same as merge? No: concat matches on index labels; merge matches on column values.
**Common mistakes:** Assuming axis=1 lines up by row position; not resetting the index after a stack; stacking tables with different column names (creates extra NaN columns).

### Q67 ⭐ 🟢 What is the difference between map() and replace() for changing values in a column?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know what happens to values that are not in your dictionary?
**Say this in the interview:** "Both use a dictionary. map changes every value, so anything not in the dictionary becomes NaN. replace only changes the values it finds and leaves the rest alone."
**Explain simply:**
- `map` = translate every value using a lookup; a missing key means NaN.
- `replace` = find and swap only the listed values; everything else is kept.
- Use `map` for a complete code-to-name lookup; use `replace` for small fixes such as typos.
**Sample data:**
```python
import pandas as pd
employees = pd.DataFrame({"dept_code": ["FIN", "HR", "IT", "OPS"]})
```
**Code (what you write in the interview):**
```python
names = {"FIN": "Finance", "HR": "Human Resources"}
employees["map_result"] = employees["dept_code"].map(names)
employees["replace_result"] = employees["dept_code"].replace(names)
print(employees)
```
**Output:**
```
  dept_code       map_result   replace_result
0       FIN          Finance          Finance
1        HR  Human Resources  Human Resources
2        IT              NaN               IT
3       OPS              NaN              OPS
```
**What it means:** IT and OPS were not in the dictionary: map turned them into NaN, replace kept them.
**Likely follow-ups:**
- How to keep unmatched with map? `map(names).fillna(employees["dept_code"])`.
**Common mistakes:** Using map with an incomplete dictionary and losing data; using replace when you wanted unmatched values flagged as missing.

### Q68 ⭐ 🟡 Write code to calculate stage-to-stage conversion rates in a hiring funnel (applied, screened, interviewed, offered, joined).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use shift to compare a row with the previous row, and do you divide by the right denominator?
**Say this in the interview:** "I divide each stage's count by the previous stage's count using shift(1), and also by the first stage for the overall conversion."
**Explain simply:**
- Conversion rate = how many moved on, divided by how many were at the earlier stage.
- `shift(1)` moves the column down one row, so each row can see the row above it.
- The first stage has no previous stage, so its step rate is NaN, which is correct.
- Step rate answers "where do we lose people"; overall rate answers "how many applicants end up joining".
**Sample data:**
```python
import pandas as pd
funnel = pd.DataFrame({
    "stage": ["Applied", "Screened", "Interviewed", "Offered", "Joined"],
    "candidates": [1000, 400, 120, 40, 30],
})
```
**Code (what you write in the interview):**
```python
# divide each stage by the one before it
funnel["step_pct"] = (funnel["candidates"] / funnel["candidates"].shift(1) * 100).round(1)

# divide each stage by the very first stage
funnel["overall_pct"] = (funnel["candidates"] / funnel["candidates"].iloc[0] * 100).round(1)
print(funnel)
```
**Output:**
```
         stage  candidates  step_pct  overall_pct
0      Applied        1000       NaN        100.0
1     Screened         400      40.0         40.0
2  Interviewed         120      30.0         12.0
3      Offered          40      33.3          4.0
4       Joined          30      75.0          3.0
```
**What it means:** The biggest drop is Screened to Interviewed (only 30% move on). Overall, 3% of applicants join.
**Likely follow-ups:**
- What if each stage is a separate column per row? Divide the columns directly, for example `df["screened"] / df["applied"]`.
- Stages out of order? Sort the rows first, since shift depends on order.
**Common mistakes:** Dividing by the first stage and calling it stage-to-stage; row order wrong so shift compares the wrong stages; dividing by zero when a stage has no candidates (gives inf).

### Q69 ⭐ 🟡 Write code to turn a monthly leavers list into a wide table of department by month with zeros where there were no leavers.
**Asked at:** commonly asked (no company-specific report found); a combined "aggregate, pivot and label" task appears on PracHub practice questions.
**What the interviewer is checking:** Whether you can reshape a long list (one row per leaver) into a department by month grid and handle the empty cells.
**Say this in the interview:** "Each row is one leaver, so I just need to count rows for each department and month pair. `pd.crosstab` does exactly that, and it puts 0 where nobody left."
**Explain simply:**
- A "long" list has one row per event (one row per leaver). A "wide" table has departments down the side and months across the top.
- `crosstab` is a pandas shortcut that counts how often each pair of values appears together.
- Pairs that never appear (for example HR in January) show as 0 automatically, so no extra fill step is needed.
- If you use `pivot_table` instead, you must add `fill_value=0`, otherwise empty cells show as NaN (pandas' "missing value" marker).

**Sample data:**

| department | month |
|---|---|
| Sales | Jan |
| Sales | Jan |
| IT | Jan |
| HR | Feb |
| IT | Mar |
| Sales | Mar |

**Code (what you write in the interview):**
```python
import pandas as pd

leavers = pd.DataFrame({
    "department": ["Sales", "Sales", "IT", "HR", "IT", "Sales"],
    "month": ["Jan", "Jan", "Jan", "Feb", "Mar", "Mar"],
})

# Count leavers for each department and month, fill gaps with 0
leavers_table = pd.crosstab(leavers["department"], leavers["month"])
print(leavers_table)
```
**Output:**
```text
month       Feb  Jan  Mar
department               
HR            1    0    0
IT            0    1    1
Sales         0    2    1
```
**What it means:** Sales lost 2 people in January and 1 in March; HR only lost 1, in February. The zeros are real "nobody left" cells.
**Alternative:** `leavers.assign(leaver_count=1).pivot_table(index="department", columns="month", values="leaver_count", aggfunc="sum", fill_value=0)` gives the same table (checked by running).
**Likely follow-ups:** 1) *Months are in the wrong order (Feb, Jan, Mar).* Pandas sorts text alphabetically; reorder with `leavers_table[["Jan", "Feb", "Mar"]]`, or store months as real dates. 2) *How do I add totals?* `pd.crosstab(..., margins=True)`.
**Common mistakes:** Forgetting `fill_value=0` in `pivot_table`; leaving month names as text so they sort alphabetically; counting with a column that has missing values (use `size`/`crosstab`, not `count` on a column).

### Q70 ⭐ 🟡 How do you get the latest record per employee using groupby when an employee appears several times?
**Asked at:** commonly asked (no company-specific report found); "latest row per ID" is a standard dedupe task in analyst prep lists.
**What the interviewer is checking:** Whether you sort before you pick, and whether you know the date must be a real date and not text.
**Say this in the interview:** "I sort by date so the newest record is last, then take the last row of each employee group with `groupby('emp_id').tail(1)`."
**Explain simply:**
- Groupby does not sort by date for you. If you pick "last" without sorting, you get the last row in the file, which may not be the newest.
- Convert the date column with `pd.to_datetime` first. As text, "2025-10-01" and "2025-9-01" can sort wrongly.
- `tail(1)` keeps the final row of each group and keeps all columns, so you get the full record.

**Sample data:**

| emp_id | update_date | salary |
|---|---|---|
| 101 | 2025-01-01 | 50000 |
| 101 | 2025-06-01 | 55000 |
| 102 | 2025-02-01 | 60000 |
| 102 | 2025-03-01 | 62000 |
| 103 | 2025-04-01 | 48000 |

**Code (what you write in the interview):**
```python
import pandas as pd

records = pd.DataFrame({
    "emp_id": [101, 101, 102, 102, 103],
    "update_date": ["2025-01-01", "2025-06-01", "2025-02-01", "2025-03-01", "2025-04-01"],
    "salary": [50000, 55000, 60000, 62000, 48000],
})

# Make sure dates are real dates, then sort so the newest is last
records["update_date"] = pd.to_datetime(records["update_date"])
records = records.sort_values("update_date")

# Keep the last (newest) row for each employee
latest_records = records.groupby("emp_id").tail(1)
print(latest_records)
```
**Output:**
```text
   emp_id update_date  salary
3     102  2025-03-01   62000
4     103  2025-04-01   48000
1     101  2025-06-01   55000
```
**What it means:** One row per employee, each being their most recent update. The rows come out in date order, not employee order.
**Alternative:** `records.loc[records.groupby("emp_id")["update_date"].idxmax()]` picks the row with the biggest date per employee, and no sorting is needed. `sort_values("update_date").drop_duplicates("emp_id", keep="last")` also gives the same rows (both checked by running).
**Likely follow-ups:** 1) *What if two records share the same latest date?* `tail(1)` takes whichever sorted last; add a second sort column (like a record ID) to make it predictable. 2) *Why not `groupby().last()`?* It returns the last non-null value of each column separately, which can mix values from different rows.
**Common mistakes:** Not sorting first; sorting dates stored as text; using `groupby().max()` on every column, which builds a row that never existed.

### Q71 ⭐ 🟡 How do you merge on the index of one DataFrame and a column of another?
**Asked at:** commonly asked (no company-specific report found); a rarer merge follow-up (gap-fill question).
**What the interviewer is checking:** Whether you know `merge` can match a column on one side to the index on the other.
**Say this in the interview:** "I use `left_on` for the column in the first table and `right_index=True` to say the second table's key is its index."
**Explain simply:**
- The index is the row label on the far left of a DataFrame. After a groupby, or when you use `set_index`, the key often lives there.
- `left_on="dept_id"` means "match this column from the left table".
- `right_index=True` means "to the index of the right table".
- You can also reset the index first (`reset_index()`) and merge normally on two columns.

**Sample data:** `employees` has columns emp_id, name, dept_id. `departments` has dept_name, with dept_id (10, 20) as its index.

**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "emp_id": [1, 2, 3],
    "name": ["Asha", "Ben", "Carla"],
    "dept_id": [10, 20, 10],
})
departments = pd.DataFrame(
    {"dept_name": ["Finance", "IT"]},
    index=[10, 20],
)

# Left side uses a column (dept_id), right side uses its index
merged = employees.merge(departments, left_on="dept_id", right_index=True, how="left")
print(merged)
```
**Output:**
```text
   emp_id   name  dept_id dept_name
0       1   Asha       10   Finance
1       2    Ben       20        IT
2       3  Carla       10   Finance
```
**What it means:** Each employee now has their department name, looked up through the department table's index.
**Likely follow-ups:** 1) *Both tables keyed by index?* Use `left_index=True, right_index=True`, or `employees.join(departments)`. 2) *Is the result index kept?* With `right_index=True` the left table's row labels are kept (shown above).
**Common mistakes:** Writing `on="dept_id"` when the key is the index (KeyError); forgetting the key must have the same dtype (number vs text) on both sides.

### Q72 ⭐ 🟡 What does a cross join do, and how do you do it in pandas?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question, not tied to a specific company report.
**What the interviewer is checking:** That you know a cross join pairs every row with every row, and when that is useful.
**Say this in the interview:** "A cross join gives every combination of rows from two tables, no key needed. In pandas it is `merge(..., how='cross')`."
**Explain simply:**
- Normal joins match on a key. A cross join has no key: every row of table A is paired with every row of table B.
- Rows in the result = rows in A times rows in B. 2 employees times 3 months is 6 rows. Large tables explode quickly.
- HR use: build a full employee by month grid, so months with no activity still show up (then left-merge the real data onto it).
- `how="cross"` needs pandas 1.2 or newer.

**Sample data:** `employees` has 2 names (Asha, Ben); `months` has 3 values (Jan, Feb, Mar).

**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"name": ["Asha", "Ben"]})
months = pd.DataFrame({"month": ["Jan", "Feb", "Mar"]})

# Every employee paired with every month
employee_months = employees.merge(months, how="cross")
print(employee_months)
```
**Output:**
```text
   name month
0  Asha   Jan
1  Asha   Feb
2  Asha   Mar
3   Ben   Jan
4   Ben   Feb
5   Ben   Mar
```
**What it means:** Two people times three months gives six rows, one for every possible pair.
**Likely follow-ups:** 1) *SQL name?* `CROSS JOIN` (a Cartesian product, meaning all combinations). 2) *Danger?* 10,000 rows crossed with 10,000 rows is 100 million rows; check sizes first.
**Common mistakes:** Passing `on=` with `how="cross"` (not allowed); crossing two big tables by accident; confusing it with an outer join.

### Q73 ⭐ 🟡 What is the difference between groupby with apply() and groupby with agg(), and which is faster?
**Asked at:** commonly asked (no company-specific report found); sources only support apply vs vectorised speed in general (Towards Data Science).
**What the interviewer is checking:** That you prefer built-in aggregation and keep `apply` for logic that agg cannot express.
**Say this in the interview:** "`agg` uses fast built-in calculations like mean or sum. `apply` runs my own Python function on every group, so it is more flexible but slower. I use agg when I can."
**Explain simply:**
- `agg` (aggregate) collapses each group to one value using built-in or named functions, which pandas runs in optimised code.
- `apply` hands each group to a function you write; it can return anything (a number, a table, several rows) but runs Python once per group.
- Speed matters most when there are many groups. In my test with 20,000 groups, `agg("mean")` took about 0.003 seconds and `apply(lambda ...)` about 0.6 seconds (machine-specific, but the gap is large).
- Use `apply` for things like "top 3 rows per group" where the result is not a single number.

**Sample data:**

| department | salary |
|---|---|
| IT | 70000 |
| IT | 80000 |
| HR | 50000 |
| HR | 54000 |
| Sales | 60000 |

**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["IT", "IT", "HR", "HR", "Sales"],
    "salary": [70000, 80000, 50000, 54000, 60000],
})

# Fast: built-in aggregation
average_salary = employees.groupby("department")["salary"].agg("mean")

# Slower: apply runs our own function once per group
average_salary_apply = employees.groupby("department")["salary"].apply(lambda group: group.mean())

print(average_salary)
print(average_salary_apply)
```
**Output:**
```text
department
HR       52000.0
IT       75000.0
Sales    60000.0
Name: salary, dtype: float64
department
HR       52000.0
IT       75000.0
Sales    60000.0
Name: salary, dtype: float64
```
**What it means:** Both give the same answer here, so choose the faster, simpler `agg`.
**Likely follow-ups:** 1) *When is apply the right tool?* When the output is not one value per group, for example the top 3 rows per group. 2) *Is there something between them?* `transform` keeps the original row count (Q13).
**Common mistakes:** Using `apply` for a plain mean or sum; writing a Python loop over groups; forgetting apply can return a different shape than agg.

### Q74 ⭐ 🟡 Why is iterrows() slow, and what are faster alternatives for row-wise logic?
**Asked at:** commonly asked (no company-specific report found); the apply vs vectorised theme is covered by Towards Data Science articles.
**What the interviewer is checking:** That you think in whole columns, not one row at a time.
**Say this in the interview:** "`iterrows` builds a new Series object for every row and runs Python on each, so it is slow. I use vectorised column maths first, then `np.where`, `map` or `apply` if I must."
**Explain simply:**
- "Vectorised" means one operation on the whole column at once, run in fast compiled code.
- `iterrows` loops one row at a time in plain Python and creates an object per row. On 200,000 rows my test took about 3.4 seconds against 0.001 seconds for one vectorised line (machine-specific).
- `iterrows` also turns each row into one Series. Mixed columns (numbers and text) become one common type, so numbers can lose their original type.
- Order of preference: column maths, `np.where` or `np.select` for if/else, `map` with a dictionary, `apply` (axis=1), `itertuples` last.

**Sample data:**

| name | salary |
|---|---|
| Asha | 40000 |
| Ben | 90000 |
| Carla | 65000 |

**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ben", "Carla"],
    "salary": [40000, 90000, 65000],
})

# Slow way: loop over every row
bonus_list = []
for index, row in employees.iterrows():
    bonus_list.append(row["salary"] * 0.10)
employees["bonus_loop"] = bonus_list

# Fast way: one vectorised line
employees["bonus"] = employees["salary"] * 0.10
print(employees)
```
**Output:**
```text
    name  salary  bonus_loop   bonus
0   Asha   40000      4000.0  4000.0
1    Ben   90000      9000.0  9000.0
2  Carla   65000      6500.0  6500.0
```
**What it means:** Same bonus both ways; the single-line version is shorter and far faster on real data.
**Likely follow-ups:** 1) *If I truly need a loop?* `itertuples()` is much faster than `iterrows()` and keeps types. 2) *Can you change the DataFrame inside the loop?* Avoid it; build a list and assign once.
**Common mistakes:** Looping to do simple arithmetic; trying to modify `row` and expecting the DataFrame to change; ignoring that `iterrows` can change dtypes.

### Q75 ⭐ 🟡 Is a pivot_table the same as groupby().unstack()? Show both for the same result.
**Asked at:** commonly asked (no company-specific report found); groupby vs pivot_table is compared in a Towards Data Science article.
**What the interviewer is checking:** That you see pivot_table as groupby plus reshape, and know both routes.
**Say this in the interview:** "Yes, for a simple case they give the same table. pivot_table is groupby, aggregate, then move one key into columns, all in one call. With groupby I do the last step myself with `unstack`."
**Explain simply:**
- `groupby(["department", "gender"])` gives one value per pair, stacked down the rows.
- `unstack()` moves the inner key (gender) out of the row labels and across as columns.
- `pivot_table` does both steps and also offers `fill_value`, `margins` (totals) and several aggregations.
- Differences: missing pairs become NaN in both unless you add `fill_value`; `pivot_table` drops empty rows and columns by default.

**Sample data:**

| department | gender | salary |
|---|---|---|
| IT | F | 70000 |
| IT | M | 80000 |
| HR | F | 50000 |
| HR | M | 54000 |
| HR | M | 56000 |

**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["IT", "IT", "HR", "HR", "HR"],
    "gender": ["F", "M", "F", "M", "M"],
    "salary": [70000, 80000, 50000, 54000, 56000],
})

# Way 1: pivot_table
using_pivot_table = employees.pivot_table(
    index="department", columns="gender", values="salary", aggfunc="mean")

# Way 2: groupby then unstack
using_groupby = employees.groupby(["department", "gender"])["salary"].mean().unstack()

print(using_pivot_table)
print(using_groupby)
```
**Output:**
```text
gender            F        M
department                  
HR          50000.0  55000.0
IT          70000.0  80000.0
gender            F        M
department                  
HR          50000.0  55000.0
IT          70000.0  80000.0
```
**What it means:** Identical tables: average salary by department (rows) and gender (columns).
**Likely follow-ups:** 1) *When pick pivot_table?* When you want totals or `fill_value`. 2) *When pick groupby?* When you need several aggregations or more control before reshaping.
**Common mistakes:** Forgetting `aggfunc` (default is mean, which may hide the intent); not noticing NaN for missing pairs.

### Q76 ⭐ 🟡 Why should you avoid calling concat() inside a loop, and what is the better pattern?
**Asked at:** commonly asked (no company-specific report found); a standard performance question, gap-fill without a direct source.
**What the interviewer is checking:** That you know each concat copies all the data, and you collect first and join once.
**Say this in the interview:** "Every `concat` builds a brand new table and copies everything so far, so a loop gets slower and slower. I put the pieces in a list and call `concat` once after the loop."
**Explain simply:**
- Joining inside the loop copies the growing table again at each step: 12 monthly files means 12 copies of bigger and bigger data.
- Appending to a plain Python list is cheap; one `concat` at the end copies the data once.
- The old `DataFrame.append` was removed in pandas 2.0 for the same reason (from memory, unverified here); `pd.concat` is the replacement.

**Sample data:** Three small files jan.csv, feb.csv, mar.csv, each with emp and days columns.

**Code (what you write in the interview):**
```python
import pandas as pd

monthly_files = ["jan.csv", "feb.csv", "mar.csv"]

# Collect each month in a list, then join once at the end
monthly_tables = []
for file_name in monthly_files:
    monthly_tables.append(pd.read_csv(file_name))

all_months = pd.concat(monthly_tables, ignore_index=True)
print(all_months)
```
**Output:**
```text
   emp  days
0    1     1
1    2     2
2    1     2
3    2     3
4    1     3
5    2     4
```
**What it means:** All three months are stacked into one table after a single concat.
**Likely follow-ups:** 1) *Why `ignore_index=True`?* It renumbers rows 0 to 5 instead of repeating 0, 1 for each file. 2) *Shorter form?* `pd.concat([pd.read_csv(f) for f in monthly_files])`.
**Common mistakes:** Starting with an empty DataFrame and concatenating in the loop; forgetting to reset the index.

### Q77 ⭐ 🟡 Write code to find employees present in both a 'trained' list and a 'certified' list.
**Asked at:** commonly asked (no company-specific report found); a gap-fill HR task.
**What the interviewer is checking:** That you recognise an "in both" question as an inner join (the overlap).
**Say this in the interview:** "I inner-merge the two lists on employee ID; an inner join keeps only IDs found in both."
**Explain simply:**
- Inner merge keeps rows whose key exists in both tables, which is the overlap of two lists.
- If an ID appears twice in one list, the result repeats it; call `drop_duplicates()` first if each person should count once.
- Another route is `isin`, which checks membership without bringing columns across (see Alternative).

**Sample data:** `trained` has emp_id 1, 2, 3, 4. `certified` has emp_id 3, 4, 5.

**Code (what you write in the interview):**
```python
import pandas as pd

trained = pd.DataFrame({"emp_id": [1, 2, 3, 4]})
certified = pd.DataFrame({"emp_id": [3, 4, 5]})

# Inner merge keeps only IDs found in both lists
trained_and_certified = trained.merge(certified, on="emp_id", how="inner")
print(trained_and_certified)
```
**Output:**
```text
   emp_id
0       3
1       4
```
**What it means:** Employees 3 and 4 are both trained and certified.
**Alternative:** `trained[trained["emp_id"].isin(certified["emp_id"])]` keeps the trained rows whose ID is in the certified list. It never multiplies rows if the certified list has duplicates (checked by running).
**Likely follow-ups:** 1) *Trained but not certified?* Use `~isin(...)` (Q17). 2) *Using sets?* `set(a) & set(b)`.
**Common mistakes:** Duplicate IDs creating extra rows; IDs stored as text in one table and numbers in the other (no match).

### Q78 ⭐ 🟡 What does the observed argument do when grouping by a categorical column?
**Asked at:** commonly asked (no company-specific report found); a rarer pandas detail (gap-fill question).
**What the interviewer is checking:** That you know categorical columns remember unused categories and that groupby can show or hide them.
**Say this in the interview:** "A categorical column has a fixed list of allowed values. `observed=False` shows every allowed value, even ones with no rows; `observed=True` shows only values that actually appear."
**Explain simply:**
- A categorical column is one with a fixed set of labels, such as pay grades A, B, C.
- If grade C exists in the list but nobody has it, `observed=False` still prints a C row (NaN for a mean, 0 for a count).
- Version note, verified by running on pandas 3.0.5: the default is now `observed=True`, so empty categories are hidden unless you ask for them. In older pandas 2.x the default was `False` with a warning (from memory, unverified here). Write it explicitly so your code behaves the same everywhere.
- Showing empty categories is useful for complete reports; hiding them gives a cleaner result.

**Sample data:** Grade is categorical with allowed values A, B, C. Rows: A 50000, A 60000, B 70000. Nobody is in C.

**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "grade": pd.Categorical(["A", "A", "B"], categories=["A", "B", "C"]),
    "salary": [50000, 60000, 70000],
})

# observed=False shows every category, even empty ones
print(employees.groupby("grade", observed=False)["salary"].mean())

# observed=True shows only categories that appear in the data
print(employees.groupby("grade", observed=True)["salary"].mean())
```
**Output:**
```text
grade
A    55000.0
B    70000.0
C        NaN
Name: salary, dtype: float64
grade
A    55000.0
B    70000.0
Name: salary, dtype: float64
```
**What it means:** Grade C has nobody, so it shows NaN (no data) in the first result and is left out of the second.
**Likely follow-ups:** 1) *Why does it matter with multiple keys?* With `observed=False` you get every combination of categories, which can be a huge table. 2) *Does it affect plain text columns?* No, only categorical dtype.
**Common mistakes:** Being surprised by extra empty rows (or missing ones after a pandas upgrade); not setting `observed` explicitly.

### Q79 ⭐ 🔴 Write code to calculate a 3-month rolling average of headcount within each department.
**Asked at:** commonly asked (no company-specific report found); rolling-per-group is a senior-leaning gap-fill question.
**What the interviewer is checking:** That the rolling window is calculated separately per department and does not leak across them.
**Say this in the interview:** "I group by department, then apply `rolling(3).mean()` to headcount inside each group, so IT's window never mixes with HR's. The data must be in month order first."
**Explain simply:**
- A rolling average takes the mean of the last N rows (here 3 months) and slides forward one row at a time.
- Without groupby, the window would run straight across the department boundary and mix rows from IT and HR.
- `transform` returns a result in the original row order and size, so it drops straight into a new column.
- The first 2 rows of each department are NaN because there are not yet 3 months to average. Add `min_periods=1` if you want partial averages instead.

**Sample data:**

| department | month | headcount |
|---|---|---|
| IT | Jan | 10 |
| IT | Feb | 12 |
| IT | Mar | 11 |
| IT | Apr | 14 |
| HR | Jan | 5 |
| HR | Feb | 6 |
| HR | Mar | 7 |

**Code (what you write in the interview):**
```python
import pandas as pd

headcount = pd.DataFrame({
    "department": ["IT", "IT", "IT", "IT", "HR", "HR", "HR"],
    "month": ["Jan", "Feb", "Mar", "Apr", "Jan", "Feb", "Mar"],
    "headcount": [10, 12, 11, 14, 5, 6, 7],
})

# Rolling average of the last 3 months, calculated separately for each department
headcount["rolling_3_month_avg"] = (
    headcount.groupby("department")["headcount"]
    .transform(lambda months: months.rolling(3).mean())
)
print(headcount)
```
**Output:**
```text
  department month  headcount  rolling_3_month_avg
0         IT   Jan         10                  NaN
1         IT   Feb         12                  NaN
2         IT   Mar         11            11.000000
3         IT   Apr         14            12.333333
4         HR   Jan          5                  NaN
5         HR   Feb          6                  NaN
6         HR   Mar          7            6.000000
```
**What it means:** IT in March is (10 + 12 + 11) / 3 = 11. HR's first full window ends in March, and nothing from IT leaks into it.
**Alternative:** `headcount.groupby("department")["headcount"].rolling(3, min_periods=1).mean().reset_index(level=0, drop=True)` gives partial averages for early months (checked by running); the extra `reset_index` is needed to line the result up with the original rows.
**Likely follow-ups:** 1) *Data not sorted?* Sort by department and month (as a real date) first. 2) *Missing months?* Reindex to a full month list, otherwise "3 rows" is not "3 months".
**Common mistakes:** Rolling without groupby; sorting months as text (Apr before Feb); forgetting the first rows are NaN.

### Q80 ⭐ 🔴 What is merge_asof(), and when would an analyst use it?
**Asked at:** commonly asked (no company-specific report found); a senior-leaning gap-fill question.
**What the interviewer is checking:** That you know it matches "nearest earlier" values instead of exact ones, such as the salary that applied on a date.
**Say this in the interview:** "`merge_asof` is a merge on the nearest key rather than an equal key. For each row on the left, it picks the closest earlier row on the right. I would use it to find which salary or policy was in force on a given date."
**Explain simply:**
- A normal merge needs exact matches. `merge_asof` takes the most recent row at or before the date (`direction="backward"`, the default).
- Both tables must be sorted by the matching column, otherwise pandas raises an error.
- `by="emp_id"` makes it match within each employee.
- HR uses: salary in force on each working day, grade or policy version on a date, latest appraisal before a promotion.

**Sample data:** Salary changes for employee 1: 50000 from 2025-01-01, 55000 from 2025-07-01. Work dates: 2025-02-10, 2025-06-15, 2025-08-20.

**Code (what you write in the interview):**
```python
import pandas as pd

# Both tables must be sorted by the column we match on
salary_changes = pd.DataFrame({
    "emp_id": [1, 1],
    "change_date": pd.to_datetime(["2025-01-01", "2025-07-01"]),
    "new_salary": [50000, 55000],
})
attendance = pd.DataFrame({
    "emp_id": [1, 1, 1],
    "work_date": pd.to_datetime(["2025-02-10", "2025-06-15", "2025-08-20"]),
})

# For each work date, take the latest salary change on or before it
result = pd.merge_asof(
    attendance, salary_changes,
    left_on="work_date", right_on="change_date",
    by="emp_id", direction="backward")
print(result)
```
**Output:**
```text
   emp_id  work_date change_date  new_salary
0       1 2025-02-10  2025-01-01       50000
1       1 2025-06-15  2025-01-01       50000
2       1 2025-08-20  2025-07-01       55000
```
**What it means:** The first two work dates use the January salary; the August date uses the July raise.
**Likely follow-ups:** 1) *Date before any change?* The row gets NaN. 2) *Limit how far back?* Use `tolerance=pd.Timedelta("30D")`.
**Common mistakes:** Not sorting both tables; forgetting `by=` and mixing employees; using an exact merge for date lookups.

### Q81 ⭐ 🔴 Write code to find the second-highest salary in each department.
**Asked at:** commonly asked (no company-specific report found); "second-highest salary" is a classic SQL question adapted to pandas.
**What the interviewer is checking:** How you handle ties (two people with the same salary) and departments with fewer than two distinct salaries.
**Say this in the interview:** "I rank salaries inside each department with `rank(method='dense')`, highest first, and keep rank 2. Dense rank means ties share a rank and the next rank is not skipped, so the second-highest salary is a real second value."
**Explain simply:**
- `groupby("department")["salary"].rank(...)` gives each salary a rank within its department.
- `ascending=False` makes rank 1 the highest.
- Dense rank: salaries 90, 80, 80, 70 get ranks 1, 2, 2, 3. A normal rank would give 1, 2, 2, 4, skipping 3; dense avoids the gap.
- Departments with only one distinct salary (Sales below) have no second-highest, so they simply do not appear.
- Ties both come back (Ben and Carla). If the interviewer wants one salary value per department, drop duplicates on department.

**Sample data:**

| name | department | salary |
|---|---|---|
| Asha | IT | 90000 |
| Ben | IT | 80000 |
| Carla | IT | 80000 |
| Dev | HR | 50000 |
| Esha | HR | 60000 |
| Farid | Sales | 70000 |

**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ben", "Carla", "Dev", "Esha", "Farid"],
    "department": ["IT", "IT", "IT", "HR", "HR", "Sales"],
    "salary": [90000, 80000, 80000, 50000, 60000, 70000],
})

# Dense rank: ties share a rank, and no rank numbers are skipped
employees["salary_rank"] = employees.groupby("department")["salary"].rank(
    method="dense", ascending=False)

second_highest = employees[employees["salary_rank"] == 2]
print(second_highest)
```
**Output:**
```text
    name department  salary  salary_rank
1    Ben         IT   80000          2.0
2  Carla         IT   80000          2.0
3    Dev         HR   50000          2.0
```
**What it means:** IT's second-highest salary is 80000 (shared by two people), HR's is 50000. Sales has nobody in second place.
**Alternative:** Drop repeated salaries, sort, and take the second row per department: `employees.drop_duplicates(["department", "salary"]).sort_values("salary", ascending=False).groupby("department").nth(1)` (checked by running; it returns one row per department).
**Likely follow-ups:** 1) *Third highest?* Change 2 to 3. 2) *Why not `nlargest(2)`?* With ties it counts the duplicate as second place, which is wrong for "second-highest value".
**Common mistakes:** Sorting and taking row 2 without handling ties; forgetting `ascending=False`; expecting every department to have a result.

### Q82 ⭐ 🔴 Write code to calculate each department's share of total attrition and flag departments contributing more than 25%.
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured gap-fill question.
**What the interviewer is checking:** That you divide each department's leavers by the company-wide total, and use the right comparison at the 25% boundary.
**Say this in the interview:** "I count leavers per department, divide by the total leavers across all departments, multiply by 100, and flag anything strictly above 25."
**Explain simply:**
- "Share of attrition" means a department's leavers out of all leavers (not its own attrition rate, which uses its headcount).
- The denominator is the total of the leaver counts, so the shares add up to 100%.
- "More than 25%" means strictly greater. A department at exactly 25% is not flagged (IT and Ops below).
- `reset_index(name=...)` turns the counts into a normal table with a named column.

**Sample data:** 8 leavers: Sales 3, IT 2, Ops 2, HR 1.

**Code (what you write in the interview):**
```python
import pandas as pd

leavers = pd.DataFrame({
    "department": ["Sales", "Sales", "Sales", "IT", "IT", "HR", "Ops", "Ops"],
})

# Leavers per department
leavers_by_department = leavers.groupby("department").size().reset_index(name="leavers")

# Each department's share of all leavers, in percent
total_leavers = leavers_by_department["leavers"].sum()
leavers_by_department["share_pct"] = leavers_by_department["leavers"] / total_leavers * 100

# Flag departments above 25%
leavers_by_department["above_25_pct"] = leavers_by_department["share_pct"] > 25
print(leavers_by_department)
```
**Output:**
```text
  department  leavers  share_pct  above_25_pct
0         HR        1       12.5         False
1         IT        2       25.0         False
2         Ops        2       25.0         False
3       Sales        3       37.5          True
```
**What it means:** Sales causes 37.5% of all exits, so only Sales is flagged. IT and Ops sit exactly at 25%, which is not "more than".
**Likely follow-ups:** 1) *Is this the attrition rate?* No: the rate divides by each department's average headcount. 2) *Share without an extra column?* `value_counts(normalize=True) * 100`.
**Common mistakes:** Dividing by department headcount instead of total leavers; using `>=` when asked "more than"; forgetting the share is of a total that must include every department.

### Q83 ⭐ 🔴 How would you reconcile two employee lists (HRMS and payroll) to find missing, extra and mismatched records using merge?
**Asked at:** commonly asked (no company-specific report found); an HR reconciliation task, gap-fill without a direct source.
**What the interviewer is checking:** That you use an outer merge with `indicator=True` to classify rows, then compare values on matched rows.
**Say this in the interview:** "I outer-merge on employee ID with `indicator=True`. That adds a column telling me whether each row is in HRMS only, payroll only, or both. For the 'both' rows I compare the fields, like salary, to find mismatches."
**Explain simply:**
- HRMS is the HR system of record; payroll is what gets paid. They should agree.
- Outer merge keeps every ID from both sides. `indicator=True` adds `_merge` with `left_only`, `right_only` or `both`.
- `left_only` is missing in payroll (someone in HRMS is not being paid); `right_only` is extra in payroll (paid but not in HRMS, a red flag).
- `suffixes` rename the repeated salary columns so you can compare them side by side.
- Note: the salary columns became decimals (50000.0) because missing sides are NaN.

**Sample data:**

| HRMS emp_id | salary | Payroll emp_id | salary |
|---|---|---|---|
| 1 | 50000 | 2 | 60000 |
| 2 | 60000 | 3 | 72000 |
| 3 | 70000 | 4 | 80000 |
| 4 | 80000 | 5 | 90000 |

**Code (what you write in the interview):**
```python
import pandas as pd

hrms = pd.DataFrame({
    "emp_id": [1, 2, 3, 4],
    "salary": [50000, 60000, 70000, 80000],
})
payroll = pd.DataFrame({
    "emp_id": [2, 3, 4, 5],
    "salary": [60000, 72000, 80000, 90000],
})

# Outer merge keeps everyone; indicator=True adds a column saying where each row came from
comparison = hrms.merge(payroll, on="emp_id", how="outer",
                        suffixes=("_hrms", "_payroll"), indicator=True)

missing_in_payroll = comparison[comparison["_merge"] == "left_only"]
extra_in_payroll = comparison[comparison["_merge"] == "right_only"]

# In both lists, but salary differs
both = comparison[comparison["_merge"] == "both"]
salary_mismatch = both[both["salary_hrms"] != both["salary_payroll"]]

print(missing_in_payroll)
print(extra_in_payroll)
print(salary_mismatch)
```
**Output:**
```text
   emp_id  salary_hrms  salary_payroll     _merge
0       1      50000.0             NaN  left_only
   emp_id  salary_hrms  salary_payroll     _merge
4       5          NaN         90000.0  right_only
   emp_id  salary_hrms  salary_payroll     _merge
2       3      70000.0         72000.0   both
```
**What it means:** Employee 1 is missing from payroll, employee 5 is in payroll but not in HRMS, and employee 3 is in both but paid 72000 instead of 70000.
**Likely follow-ups:** 1) *Duplicate IDs?* Check `duplicated("emp_id")` first or the merge multiplies rows (Q16). 2) *Does merge compare NaN fields well?* `NaN != NaN` is True, so blanks on both sides look like mismatches; fill or handle them first.
**Common mistakes:** Using inner merge (hides missing records); not using `indicator=True`; comparing text with different spacing or case; IDs of different types.

# Book 3 — Python & pandas for Analysts | Part 9: EDA End-to-End Tasks (Live-Coding Style) 🟡🔴

**Target:** 50 questions | **Actual:** 54 questions
**Scope:** end-to-end exploratory data analysis tasks in pandas as asked in live-coding and take-home rounds: load, inspect, clean, summarise, compare groups, chart and explain findings, using HR, payroll, attendance and sales data.

### Q1 ⭐⭐⭐ 🟢 You are given a CSV file you have never seen. What are the first five things you do in pandas to understand it?
**Asked at:** commonly asked (no company-specific report found); a Glassdoor Pivigo report mentions "use pandas on a basic data set and do exploratory data analysis" (snippet only, unverified).
**What the interviewer is checking:** Whether you have a calm, repeatable routine before you calculate anything.
**Say this in the interview:** "I look at the first rows, then the shape, then the column types, then missing values and duplicates, then a quick summary of numbers and categories. Only then do I ask questions of the data."
**Explain simply:**
- **EDA (exploratory data analysis):** getting to know a dataset before analysing it.
- **CSV file and DataFrame:** a CSV is a plain-text table, one row per line; pandas loads it into a DataFrame, its own table of rows and columns (I name it `employees`).
- **Step 1, `head()`:** see real rows, so I know what one row means (one employee? one day?).
- **Step 2, `shape`:** (rows, columns), to know the size.
- **Step 3, `info()`:** each column's type and how many values are filled; a salary stored as text shows up here.
- **Step 4, `isna().sum()` and `duplicated().sum()`:** missing values and repeated rows.
- **Step 5, `describe()` and `value_counts()`:** min, max, average for numbers; counts for categories.
**Sample data:** `employees.csv`, 8 employees with Department, JobRole, Age, MonthlyIncome, Attrition (one Department and one MonthlyIncome left blank).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("employees.csv")

# 1. Look at the first rows
print(employees.head())

# 2. Size of the table
print(employees.shape)

# 3. Column types and non-null counts
employees.info()

# 4. Missing values and duplicate rows
print(employees.isna().sum())
print(employees.duplicated().sum())

# 5. Summary of numbers and of text columns
print(employees.describe())
print(employees["Department"].value_counts(dropna=False))
```
**Output:**
```
   EmployeeID Department    JobRole  Age  MonthlyIncome Attrition
0         101      Sales  Executive   29        42000.0       Yes
1         102      Sales  Executive   41        55000.0        No
2         103         HR  Recruiter   35        38000.0        No
3         104         HR  Recruiter   27            NaN       Yes
4         105         IT  Developer   31        70000.0        No
(8, 6)
<class 'pandas.DataFrame'>
RangeIndex: 8 entries, 0 to 7
Data columns (total 6 columns):
 #   Column         Non-Null Count  Dtype  
---  ------         --------------  -----  
 0   EmployeeID     8 non-null      int64  
 1   Department     7 non-null      str    
 2   JobRole        8 non-null      str    
 3   Age            8 non-null      int64  
 4   MonthlyIncome  7 non-null      float64
 5   Attrition      8 non-null      str    
dtypes: float64(1), int64(2), str(3)
memory usage: 516.0 bytes
EmployeeID       0
Department       1
JobRole          0
Age              0
MonthlyIncome    1
Attrition        0
dtype: int64
0
       EmployeeID        Age  MonthlyIncome
count     8.00000   8.000000       7.000000
mean    104.50000  34.000000   61000.000000
std       2.44949   6.907553   19536.291016
min     101.00000  26.000000   38000.000000
25%     102.75000  28.500000   47000.000000
50%     104.50000  33.000000   55000.000000
75%     106.25000  38.750000   75000.000000
max     108.00000  45.000000   90000.000000
Department
IT       3
Sales    2
HR       2
NaN      1
Name: count, dtype: int64
```
**What it means:** 8 employees, no duplicates, one missing Department and one missing MonthlyIncome; I would note both before going further.
**Likely follow-ups:**
- *What if the file is huge?* Read a sample first with `nrows=1000` (see Q47).
- *What do you do after these five?* Write down questions to answer (Q5).
**Common mistakes:** jumping straight to charts; trusting `describe()` without checking types first (a numeric column read as text is silently left out); forgetting that `describe()` ignores missing values.

### Q2 ⭐⭐⭐ 🟢 Write code to load employees.csv and print its shape, column dtypes and the number of missing values per column.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic loading and the three standard health checks.
**Say this in the interview:** "`read_csv` to load, `shape` for rows and columns, `dtypes` for types, and `isna().sum()` counts blanks per column."
**Explain simply:**
- **dtype:** the data type of a column (`int64` whole numbers, `float64` decimals, `str` text).
- **`isna()`:** gives True where a value is missing; `sum()` counts the Trues.
- **Why MonthlyIncome is `float64`:** a column with a blank cannot be whole numbers, so pandas uses decimals with `NaN` (not a number) for the blank.
**Sample data:** same `employees.csv` as Q1 (8 rows, one blank Department, one blank MonthlyIncome).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("employees.csv")

print(employees.shape)
print(employees.dtypes)
print(employees.isna().sum())
```
**Output:**
```
(8, 6)
EmployeeID         int64
Department           str
JobRole              str
Age                int64
MonthlyIncome    float64
Attrition            str
dtype: object
EmployeeID       0
Department       1
JobRole          0
Age              0
MonthlyIncome    1
Attrition        0
dtype: int64
```
**What it means:** 8 rows, 6 columns, and exactly two cells are empty.
**Alternative:** `employees.info()` shows types and non-null counts together.
**Likely follow-ups:**
- *Why does pandas show `str` and not `object`?* Version note, verified on pandas 3.0.5: text columns are `str` now; older pandas 2.x shows `object`.
- *File will not load?* Check the path, `encoding="utf-8"` or `"latin-1"`, and the separator (`sep=";"`).
**Common mistakes:** writing `shape()` with brackets (it is an attribute); forgetting `.sum()` so you only get a True/False table; treating "N/A" or "-" text as real values (use `na_values=["N/A", "-"]`).

### Q3 ⭐⭐⭐ 🟡 Write code to calculate the overall attrition rate (percentage of employees with Attrition = 'Yes') from an HR DataFrame.
**Asked at:** commonly asked (no company-specific report found); attrition rate is the standard HR practice dataset metric (IBM HR notebooks, snippet-level).
**What the interviewer is checking:** Can you turn a Yes/No column into a percentage correctly.
**Say this in the interview:** "Attrition rate is leavers divided by total employees times 100. I count rows where Attrition is 'Yes' and divide by the number of rows."
**Explain simply:**
- **Attrition:** employees leaving the company.
- **Attrition rate:** leavers / total employees x 100.
- **Trick:** `(column == "Yes")` gives True/False per row; pandas counts True as 1, so `sum()` is the number of leavers.
**Sample data:** 8 employees, 3 with Attrition = Yes.
**Code (what you write in the interview):**
```python
import pandas as pd

hr = pd.DataFrame({
    "EmployeeID": [1, 2, 3, 4, 5, 6, 7, 8],
    "Attrition": ["Yes", "No", "No", "Yes", "No", "No", "Yes", "No"],
})

# True for leavers, and True counts as 1 when we sum
employees_who_left = (hr["Attrition"] == "Yes").sum()
attrition_rate = employees_who_left / len(hr) * 100

print(f"Attrition rate: {attrition_rate:.1f}%")
```
**Output:**
```
Attrition rate: 37.5%
```
**What it means:** 3 of 8 employees left, so 37.5%.
**Alternative:** `(hr["Attrition"] == "Yes").mean() * 100` gives the same number in one line (mean of True/False is the share of True).
**Likely follow-ups:**
- *What about blanks in Attrition?* `len(hr)` counts them as stayers; I would drop or investigate them first.
- *Is this annual attrition?* Only if the data covers one year; otherwise say the period.
**Common mistakes:** dividing by the number of "No" rows; forgetting to multiply by 100; spelling differences ("yes", "Yes ") making the count too low (clean text first, see Q14).

### Q4 ⭐⭐⭐ 🟡 Write code to find the attrition rate by department and sort the departments from highest to lowest.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the groupby-then-mean trick on a 0/1 column.
**Say this in the interview:** "I make a 1/0 column for 'left', group by department, take the average, which is the leaver share, then sort descending."
**Explain simply:**
- **groupby:** split rows into one bucket per department, then calculate inside each bucket.
- **Average of 1/0:** the share of ones, so it is the attrition rate.
- **`sort_values(ascending=False)`:** biggest first.
**Sample data:** 8 employees in Sales, HR and IT with a Yes/No Attrition column.
**Code (what you write in the interview):**
```python
import pandas as pd

hr = pd.DataFrame({
    "Department": ["Sales", "Sales", "HR", "HR", "IT", "IT", "IT", "Sales"],
    "Attrition": ["Yes", "No", "No", "Yes", "No", "No", "Yes", "No"],
})

# 1 if the employee left, 0 if stayed, so the average is the leaver share
hr["Left"] = (hr["Attrition"] == "Yes").astype(int)

attrition_by_department = hr.groupby("Department")["Left"].mean() * 100
attrition_by_department = attrition_by_department.round(1).sort_values(ascending=False)

print(attrition_by_department)
```
**Output:**
```
Department
HR       50.0
IT       33.3
Sales    33.3
Name: Left, dtype: float64
```
**What it means:** HR loses half its people in this tiny sample; IT and Sales tie at one third. With so few rows, I would also show headcount before drawing conclusions.
**Likely follow-ups:**
- *How do you show counts too?* `hr.groupby("Department")["Left"].agg(["mean", "count"])`.
- *Ties?* Tied departments can come out in either order; add a second sort key (for example the department name) if the order matters.
**Common mistakes:** averaging the text column (error); sorting before calculating; reporting a high rate for a department of 3 people without saying so.

### Q5 ⭐⭐⭐ 🟡 Walk me through a complete EDA of an employee attrition dataset using pandas, from loading the file to your final recommendations.
**Asked at:** commonly asked (no company-specific report found); EDA on the IBM HR attrition dataset is a common practice version (public notebooks, snippet-level).
**What the interviewer is checking:** Can you run a structured analysis and end with a business recommendation, not just output.
**Say this in the interview:** "I start with a business question, load and check quality, calculate the overall attrition rate, split it by department, overtime, income and tenure, and then recommend where HR should act, with the caveat that this shows links, not causes."
**Explain simply:**
- **1. Question first:** "Who leaves and why might they?" so the work has a goal.
- **2. Load and inspect:** shape, types, missing values, duplicates (Q1).
- **3. Clean:** remove duplicates, fix text and dates, decide on missing values.
- **4. Overall rate:** one headline number (Q3).
- **5. Split by groups:** department, overtime, age band, income, tenure (Q4, Q21, Q22).
- **6. Compare leavers and stayers:** averages of income, age, tenure.
- **7. Recommend:** two or three actions, plus limits (small groups, correlation is not causation, Q46).
**Sample data:** `hr_attrition.csv`, 10 employees with Department, OverTime, MonthlyIncome, Attrition.
**Code (what you write in the interview):**
```python
import pandas as pd

# 1. Load and look
hr = pd.read_csv("hr_attrition.csv")
print(hr.shape)
hr.info()

# 2. Clean: duplicates and missing values
hr = hr.drop_duplicates()
print(hr.isna().sum())

# 3. Overall attrition rate
hr["Left"] = (hr["Attrition"] == "Yes").astype(int)
print("Overall attrition:", round(hr["Left"].mean() * 100, 1), "%")

# 4. Attrition by group
print(hr.groupby("Department")["Left"].mean().mul(100).round(1))
print(hr.groupby("OverTime")["Left"].mean().mul(100).round(1))

# 5. Compare income of leavers and stayers
print(hr.groupby("Attrition")["MonthlyIncome"].mean())
```
**Output:**
```
(10, 5)
<class 'pandas.DataFrame'>
RangeIndex: 10 entries, 0 to 9
Data columns (total 5 columns):
 #   Column         Non-Null Count  Dtype
---  ------         --------------  -----
 0   EmployeeID     10 non-null     int64
 1   Department     10 non-null     str  
 2   OverTime       10 non-null     str  
 3   MonthlyIncome  10 non-null     int64
 4   Attrition      10 non-null     str  
dtypes: int64(2), str(3)
memory usage: 532.0 bytes
EmployeeID       0
Department       0
OverTime         0
MonthlyIncome    0
Attrition        0
dtype: int64
Overall attrition: 30.0 %
Department
HR        0.0
IT       25.0
Sales    66.7
Name: Left, dtype: float64
OverTime
No      0.0
Yes    75.0
Name: Left, dtype: float64
Attrition
No     56000.000000
Yes    32666.666667
Name: MonthlyIncome, dtype: float64
```
**What it means:** 30% left overall; Sales and overtime workers leave most, and leavers earn less on average. My recommendation: look at Sales workload and overtime first, and pay for the lowest earners, while saying 10 rows is only an illustration.
**Likely follow-ups:**
- *What chart would you add?* Bar chart of attrition by department, boxplot of income by Attrition.
- *How do you end?* Three findings, one recommendation each, and one caveat (Q11).
**Common mistakes:** listing code output without a conclusion; not mentioning group sizes; claiming overtime "causes" attrition.

### Q6 ⭐⭐⭐ 🟡 Write code to check for duplicate rows in a DataFrame, count them, and remove them while keeping the first occurrence.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** `duplicated()` and `drop_duplicates()`, and the meaning of `keep`.
**Say this in the interview:** "`duplicated()` marks repeats, `.sum()` counts them, and `drop_duplicates(keep='first')` removes them, keeping the first copy."
**Explain simply:**
- **Duplicate row:** every column value matches an earlier row.
- **`keep="first"`:** the first copy stays (it is also the default); `"last"` keeps the final one; `False` drops all copies.
- **Subset:** if only the ID matters, use `subset=["EmployeeID"]`.
**Sample data:** 6 rows where Ravi (102) and John (104) appear twice.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "EmployeeID": [101, 102, 102, 103, 104, 104],
    "Name": ["Asha", "Ravi", "Ravi", "Meena", "John", "John"],
    "Department": ["HR", "IT", "IT", "Sales", "IT", "IT"],
})

# True for every row that repeats an earlier row
duplicate_flags = employees.duplicated()
print("Duplicate rows:", duplicate_flags.sum())

# Keep the first copy, drop the rest
employees_clean = employees.drop_duplicates(keep="first")
print(employees_clean)
```
**Output:**
```
Duplicate rows: 2
   EmployeeID   Name Department
0         101   Asha         HR
1         102   Ravi         IT
3         103  Meena      Sales
4         104   John         IT
```
**What it means:** 2 repeated rows were found and removed; 4 unique employees remain (the index keeps its old numbers, which is fine).
**Likely follow-ups:**
- *Same ID but different salary?* That is a conflict, not a duplicate; use `subset=["EmployeeID"]` after checking which row is right.
- *Reset the index?* Add `.reset_index(drop=True)`.
**Common mistakes:** assuming `drop_duplicates()` changes the original (it returns a new table); ignoring near-duplicates like "Ravi " vs "Ravi"; deleting duplicates before asking whether repeats are legitimate (for example one row per attendance day).

### Q7 ⭐⭐⭐ 🟡 Write code to find the top 5 job roles by average monthly income, showing role, average income and headcount.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Named aggregation, sorting and `head()` together.
**Say this in the interview:** "Group by job role, calculate mean income and count in one step with named aggregation, sort high to low and take the top 5."
**Explain simply:**
- **`agg` with names:** `new_name=("column", "function")` gives clear column names.
- **Headcount:** how many employees are in the role; it tells you if the average is trustworthy.
- **`head(5)`:** first five rows after sorting.
**Sample data:** 10 employees across 7 roles.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "JobRole": ["Developer", "Developer", "Analyst", "Recruiter", "Recruiter",
                "Manager", "Designer", "Accountant", "Executive", "Executive"],
    "MonthlyIncome": [70000, 90000, 52000, 38000, 36000,
                      80000, 45000, 41000, 42000, 55000],
})

role_summary = employees.groupby("JobRole").agg(
    average_income=("MonthlyIncome", "mean"),
    headcount=("MonthlyIncome", "count"),
)

top_5_roles = role_summary.sort_values("average_income", ascending=False).head(5)
print(top_5_roles)
```
**Output:**
```
           average_income  headcount
JobRole                             
Developer         80000.0          2
Manager           80000.0          1
Analyst           52000.0          1
Executive         48500.0          2
Designer          45000.0          1
```
**What it means:** Developers and Managers tie at 80,000 on average; but the Manager figure is one person, so I would say it is not a reliable role average.
**Likely follow-ups:**
- *Ties at rank 5?* `head(5)` cuts them arbitrarily; mention it or use `nlargest(5, "average_income", keep="all")`.
- *Median instead of mean?* Better when a few very high salaries pull the average up.
**Common mistakes:** forgetting headcount; sorting ascending; `count` ignores blanks while `size` counts all rows.

### Q8 ⭐⭐⭐ 🟡 A sales DataFrame has order_date, region and revenue. Write code to find total revenue per region and the share (percentage) of each region in the total.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Group sum, then divide by the grand total.
**Say this in the interview:** "Sum revenue per region, then divide each region by the sum of all regions and multiply by 100. Shares should add up to 100."
**Explain simply:**
- **Share (percent of total):** a part divided by the whole.
- **Series arithmetic:** dividing a whole column of region totals by one number works for every region at once.
- `order_date` is not needed here; say so, it shows you read the question.
**Sample data:** 6 orders across North, South and West.
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({
    "order_date": ["2026-01-05", "2026-01-12", "2026-02-03", "2026-02-20", "2026-03-08", "2026-03-15"],
    "region": ["North", "South", "North", "West", "South", "North"],
    "revenue": [1000, 600, 1400, 500, 900, 600],
})

revenue_by_region = sales.groupby("region")["revenue"].sum()
share_percent = revenue_by_region / revenue_by_region.sum() * 100

result = pd.DataFrame({
    "total_revenue": revenue_by_region,
    "share_percent": share_percent.round(1),
})
print(result)
```
**Output:**
```
        total_revenue  share_percent
region                              
North            3000           60.0
South            1500           30.0
West              500           10.0
```
**What it means:** North brings 60% of the 5,000 revenue; West only 10%.
**Likely follow-ups:**
- *Share by month too?* Group by month and region, then divide by the monthly total with `transform("sum")`.
- *Rounded shares not adding to 100?* Round only for display.
**Common mistakes:** dividing by the row count, not the revenue total; dropping rows with missing revenue silently; mixing currencies.

### Q9 ⭐⭐⭐ 🟡 Write code to merge an employee table with a department table and then check that the merge did not create extra rows or lose employees.
**Asked at:** commonly asked (no company-specific report found); merge row-count checks appear in PracHub pandas-for-analysts material (snippet only).
**What the interviewer is checking:** Do you verify a merge instead of trusting it.
**Say this in the interview:** "I use a left merge so no employee is dropped, `validate='many_to_one'` so duplicate department keys raise an error, and `indicator=True` to see unmatched rows. Then I compare row counts."
**Explain simply:**
- **Left merge:** keep every row of the employee table, add department details where the key matches.
- **`validate="many_to_one"`:** many employees to one department; it fails if a DeptID repeats in the department table.
- **`indicator=True`:** adds `_merge` showing `both`, `left_only` or `right_only`.
**Sample data:** 5 employees; employee 5 has DeptID 99, which is not in the department table.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "EmployeeID": [1, 2, 3, 4, 5],
    "DeptID": [10, 10, 20, 30, 99],
})
departments = pd.DataFrame({
    "DeptID": [10, 20, 30],
    "DeptName": ["HR", "IT", "Sales"],
})

# validate stops the merge if a DeptID repeats in departments
merged = employees.merge(departments, on="DeptID", how="left",
                         validate="many_to_one", indicator=True)

print("Rows before:", len(employees), "| after:", len(merged))
print(merged["_merge"].value_counts())

# Employees whose department was not found
print(merged[merged["_merge"] == "left_only"])
```
**Output:**
```
Rows before: 5 | after: 5
_merge
both          4
left_only     1
right_only    0
Name: count, dtype: int64
   EmployeeID  DeptID DeptName     _merge
4           5      99      NaN  left_only
```
**What it means:** same 5 rows before and after, so nothing was added or lost; but one employee has an unknown department that I must report and fix.
**Likely follow-ups:**
- *What if the row count rose?* A key repeated in the right table; `validate` would have raised an error (see Q28).
- *Why not an inner merge?* It would silently drop employee 5.
**Common mistakes:** using the default inner merge; checking only that the code ran; not looking at keys with different types (text "10" vs number 10) or stray spaces.

### Q10 ⭐⭐⭐ 🟡 Write code to find which columns have missing values, what percentage is missing in each, and decide how you would treat each (drop, fill, or leave).
**Asked at:** commonly asked (no company-specific report found); a Tiger Analytics report mentions mean imputation (snippet only, unverified).
**What the interviewer is checking:** Can you measure missingness and justify a treatment per column.
**Say this in the interview:** "`isna().mean() * 100` gives percent missing per column. Then I decide per column: drop if mostly empty, fill numbers with the median, fill text with 'Unknown', or leave it if the blank itself has meaning."
**Explain simply:**
- **Missing value:** an empty cell, shown as `NaN`.
- **Drop a column:** when most of it is empty, it adds little.
- **Fill with median:** the middle value; safer than the average when a few salaries are very high.
- **Leave:** when blank means something, for example "Manager" blank for the CEO or "no manager".
**Sample data:** 10 employees; Salary 2 blanks, Manager 8 blanks, Department 1 blank.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "EmployeeID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Salary": [50, 60, None, 55, 70, 65, None, 58, 62, 90],
    "Manager": [None, None, None, "A", None, None, None, None, None, "B"],
    "Department": ["HR", "IT", "IT", None, "HR", "IT", "HR", "IT", "HR", "IT"],
})

missing_percent = employees.isna().mean() * 100
missing_percent = missing_percent[missing_percent > 0].round(1)
print(missing_percent)

# Rule of thumb for the decision
for column, percent in missing_percent.items():
    if percent > 50:
        print(column, "-> drop the column")
    elif pd.api.types.is_numeric_dtype(employees[column]):
        print(column, "-> fill with the median and add a missing flag")
    else:
        print(column, "-> fill with 'Unknown'")
```
**Output:**
```
Salary        20.0
Manager       80.0
Department    10.0
dtype: float64
Salary -> fill with the median and add a missing flag
Manager -> drop the column
Department -> fill with 'Unknown'
```
**What it means:** the code only suggests; I confirm with the business first (for example Manager may be blank because many staff have no manager, so I would ask before dropping).
**Likely follow-ups:**
- *Why add a missing flag?* The fact that salary is blank may itself matter (Q42).
- *Why not just drop all rows with blanks?* You may lose a big share of the data and bias the result.
**Common mistakes:** one rule for every column; filling with the average when salaries are skewed; not asking what a blank means.

### Q11 ⭐⭐⭐ 🟡 After you finish an EDA in an interview, how do you present your findings in plain business language instead of reading out code output?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can turn numbers into a story and a recommendation for non-technical people.
**Say this in the interview:** "I start with the answer, then give two or three findings with one number each, say how confident I am, and end with what I recommend and what I would check next."
**Explain simply:**
- **Answer first:** "Sales has the highest attrition, 67% against 30% overall."
- **One number per finding:** more than that loses the listener.
- **Compare, do not just report:** "twice the company average" means more than "67%".
- **Say how sure you are:** "only 3 people in this group", "this shows a link, not a cause".
- **End with an action:** who should do what next, and what data would settle the doubts.
- **Do not read code:** describe what you did in one line ("I excluded 12 duplicate rows").
**What it means:** the interviewer is hiring someone who can brief a manager, so a clear answer, a number, a caveat and an action matter more than the code.
**Likely follow-ups:**
- *How long should a summary be?* Three findings and a recommendation fit in under two minutes.
- *Which chart?* One bar chart that shows the main comparison.
**Common mistakes:** reading column names aloud; showing every table; using jargon like "p-value" or "standard deviation" without a plain meaning; no recommendation.

### Q12 ⭐⭐⭐ 🟡 Write code to detect outliers in a salary column using the IQR rule and list the employees flagged.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the IQR rule and can you apply it as a filter.
**Say this in the interview:** "IQR is Q3 minus Q1, the spread of the middle half. Anything below Q1 minus 1.5 IQR or above Q3 plus 1.5 IQR is flagged as an outlier."
**Explain simply:**
- **Quartiles:** Q1 is the value with 25% of data below it; Q3 has 75% below.
- **IQR (interquartile range):** Q3 minus Q1.
- **Outlier:** a value far from the rest. Flagged does not mean wrong; check it (a CEO salary is real).
**Sample data:** 8 salaries, the last one 250,000.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "EmployeeID": [1, 2, 3, 4, 5, 6, 7, 8],
    "Salary": [40000, 42000, 45000, 47000, 50000, 52000, 55000, 250000],
})

q1 = employees["Salary"].quantile(0.25)
q3 = employees["Salary"].quantile(0.75)
iqr = q3 - q1

lower_limit = q1 - 1.5 * iqr
upper_limit = q3 + 1.5 * iqr

outliers = employees[(employees["Salary"] < lower_limit) | (employees["Salary"] > upper_limit)]
print("Limits:", lower_limit, upper_limit)
print(outliers)
```
**Output:**
```
Limits: 31500.0 65500.0
   EmployeeID  Salary
7           8  250000
```
**What it means:** only employee 8 falls outside 31,500 to 65,500; I would check whether it is a typo or a senior leader.
**Likely follow-ups:**
- *Remove outliers?* Not automatically; first check if they are real, then decide, and report both ways if it changes the result.
- *Outliers within each department?* Do the same inside a groupby, because a senior role is not an outlier among seniors.
**Common mistakes:** using `&` instead of `|` (nothing is both too low and too high); forgetting brackets around each condition; deleting real high earners.

### Q13 ⭐⭐⭐ 🟡 Write code to convert a joining_date column stored as text into datetime, then create columns for joining year, joining month and tenure in years.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** `to_datetime`, the `.dt` accessor and date subtraction.
**Say this in the interview:** "`pd.to_datetime` converts the text; then `.dt.year` and `.dt.month` give parts; tenure is today's date minus joining date in days, divided by 365.25."
**Explain simply:**
- **Datetime:** a real date type, so pandas can do date maths. Text dates cannot be subtracted.
- **`.dt`:** the doorway to date parts (year, month, day, weekday).
- **Tenure:** time in the company. 365.25 allows for leap years.
- **Fixed as-of date:** in real work I use today; here a fixed date keeps the result repeatable.
**Sample data:** 3 employees with joining dates as text.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "EmployeeID": [1, 2, 3],
    "joining_date": ["2021-03-15", "2019-11-01", "2024-07-20"],
})

employees["joining_date"] = pd.to_datetime(employees["joining_date"])
employees["joining_year"] = employees["joining_date"].dt.year
employees["joining_month"] = employees["joining_date"].dt.month

# Fixed reporting date so the answer is repeatable
as_of_date = pd.Timestamp("2026-01-01")
employees["tenure_years"] = ((as_of_date - employees["joining_date"]).dt.days / 365.25).round(1)

print(employees)
```
**Output:**
```
   EmployeeID joining_date  joining_year  joining_month  tenure_years
0           1   2021-03-15          2021              3           4.8
1           2   2019-11-01          2019             11           6.2
2           3   2024-07-20          2024              7           1.5
```
**What it means:** employee 2 has the longest service, 6.2 years, as at 1 Jan 2026.
**Likely follow-ups:**
- *Bad dates in the column?* `errors="coerce"` turns them into `NaT` (missing date) so you can count them.
- *Day-first dates like 05/03/2026?* Add `dayfirst=True`, and state your assumption.
- *Employees who left?* Use the exit date instead of today for their tenure.
**Common mistakes:** subtracting text dates; using today's date for employees who already left; confusing day/month order.

### Q14 ⭐⭐⭐ 🔴 You get a messy attendance file with mixed date formats, 'Present'/'present '/'P' status values and blank employee IDs. Write the cleaning code step by step.
**Asked at:** commonly asked (no company-specific report found); messy-data tasks are a standard live-coding pattern (PracHub snippet, unverified).
**What the interviewer is checking:** Can you clean three different problems in a clear order and check the result.
**Say this in the interview:** "Blank IDs first, because a row without an employee is useless; then dates, trying each known format; then status text, strip spaces, lower case, and map short codes to full words. I finish with a value count to check."
**Explain simply:**
- **Blank IDs:** an empty string is not `NaN`, so I convert it first, then drop the rows.
- **Mixed date formats:** parse each format separately with `errors="coerce"` (bad ones become `NaT`) and combine with `fillna`.
- **Status clean-up:** `str.strip()` removes spaces, `str.lower()` unifies case, `replace` maps `p` to `present`.
- **Check at the end:** counts show only clean values remain.
**Sample data:** 6 rows with three date styles, messy statuses and two blank IDs.
**Code (what you write in the interview):**
```python
import pandas as pd

attendance = pd.DataFrame({
    "employee_id": ["E1", "E2", "", "E4", None, "E1"],
    "date": ["2026-03-02", "03/03/2026", "4 Mar 2026", "2026-03-05", "06/03/2026", "2026-03-09"],
    "status": ["Present", "present ", "P", "Absent", "A", "P"],
})

# Step 1: blank IDs become missing, then drop those rows
attendance["employee_id"] = attendance["employee_id"].replace("", pd.NA)
attendance = attendance.dropna(subset=["employee_id"])

# Step 2: try each known date format, keep whichever one works
date_text = attendance["date"]
date_iso = pd.to_datetime(date_text, format="%Y-%m-%d", errors="coerce")
date_slash = pd.to_datetime(date_text, format="%d/%m/%Y", errors="coerce")
date_words = pd.to_datetime(date_text, format="%d %b %Y", errors="coerce")
attendance["date"] = date_iso.fillna(date_slash).fillna(date_words)

# Step 3: trim spaces, lower case, then map short codes to full words
attendance["status"] = attendance["status"].str.strip().str.lower()
attendance["status"] = attendance["status"].replace({"p": "present", "a": "absent"})

print(attendance)
print(attendance["status"].value_counts())
```
**Output:**
```
  employee_id       date   status
0          E1 2026-03-02  present
1          E2 2026-03-03  present
3          E4 2026-03-05   absent
5          E1 2026-03-09  present
status
present    3
absent     1
Name: count, dtype: int64
```
**What it means:** 2 rows without an ID were removed, all dates are one type, and status has only "present" and "absent". I would also tell the interviewer how many rows I dropped.
**Likely follow-ups:**
- *Is 03/03/2026 day-first or month-first?* Ambiguous dates need a business rule; I assume day-first (India) and say it. One `format="mixed", dayfirst=True` call misread the ISO date `2026-03-02` as 3 February when I ran it on pandas 3.0.5, so I parse each format separately.
- *Should dropping rows be silent?* No, count and report them.
**Common mistakes:** only `dropna` when blanks are empty strings (they stay); forgetting `strip()` so "present " counts separately; not checking for `NaT` left after parsing.

### Q15 ⭐⭐⭐ 🔴 Given a hiring funnel DataFrame (candidate_id, stage, date), write code to compute the number of candidates reaching each stage and the conversion rate from one stage to the next.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Unique counting, ordering stages, and `shift` for step-to-step rates.
**Say this in the interview:** "Count unique candidates per stage, put the stages in funnel order, then divide each stage by the one before it using `shift`."
**Explain simply:**
- **Funnel:** applicants narrow down at each stage (Applied, Screened, Interviewed, Offered).
- **`nunique`:** counts each candidate once, even if the file has repeat rows.
- **`reindex(stage_order)`:** puts stages in funnel order, not alphabetical.
- **`shift(1)`:** moves values down one row so each stage sits next to the previous one.
**Sample data:** 11 rows; one row per candidate per stage reached (5 applied, 3 screened, 2 interviewed, 1 offered).
**Code (what you write in the interview):**
```python
import pandas as pd

funnel = pd.DataFrame({
    "candidate_id": [1, 2, 3, 4, 5, 1, 2, 3, 1, 2, 1],
    "stage": ["Applied", "Applied", "Applied", "Applied", "Applied",
              "Screened", "Screened", "Screened",
              "Interviewed", "Interviewed", "Offered"],
    "date": pd.to_datetime(["2026-01-01"] * 11),
})

stage_order = ["Applied", "Screened", "Interviewed", "Offered"]

# Count each candidate once per stage
candidates_per_stage = funnel.groupby("stage")["candidate_id"].nunique()
candidates_per_stage = candidates_per_stage.reindex(stage_order)

# Divide each stage by the stage before it
conversion_rate = (candidates_per_stage / candidates_per_stage.shift(1) * 100).round(1)

print(pd.DataFrame({"candidates": candidates_per_stage, "conversion_%": conversion_rate}))
```
**Output:**
```
             candidates  conversion_%
stage                                
Applied               5           NaN
Screened              3          60.0
Interviewed           2          66.7
Offered               1          50.0
```
**What it means:** 60% of applicants pass screening, 67% of those get interviewed, and half of interviewed candidates get an offer. The first stage has no previous stage, so it shows `NaN`.
**Likely follow-ups:**
- *Overall conversion?* Last stage divided by first: 1 / 5 = 20%.
- *Where is the biggest drop?* Interview to offer: only 50% move on, so half are lost there (screening loses 40%, interview loses 33%). That is where I would investigate.
**Common mistakes:** using `count` when candidates can repeat; letting stages sort alphabetically; dividing by the first stage when asked for step-to-step rates.

### Q16 ⭐⭐ 🟢 What is the difference between df.info(), df.describe() and df.head(), and what does each tell you in the first minutes of EDA?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know which tool answers which question.
**Say this in the interview:** "`head` shows actual rows, `info` shows structure, types and missing counts, `describe` shows statistics of the numbers. Together they tell me what the data looks like, whether it is clean, and what values are normal."
**Explain simply:**
- **`head(n)`:** the first n rows (default 5); tells me what one row means and how values look.
- **`info()`:** rows, columns, type and non-null count per column; spots wrong types and missing data.
- **`describe()`:** count, mean, std, min, quartiles, max for numeric columns; spots impossible values (age 250) and skew.
- **Note:** `info()` prints directly, so do not wrap it in `print`; `describe()` skips text columns unless you pass `include="all"`.
**Sample data:** 4 employees; one salary is missing.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "Department": ["HR", "IT", "IT", "Sales"],
    "Salary": [40000, 70000, None, 50000],
})

print(employees.head(2))
employees.info()
print(employees.describe())
```
**Output:**
```
  Department   Salary
0         HR  40000.0
1         IT  70000.0
<class 'pandas.DataFrame'>
RangeIndex: 4 entries, 0 to 3
Data columns (total 2 columns):
 #   Column      Non-Null Count  Dtype  
---  ------      --------------  -----  
 0   Department  4 non-null      str    
 1   Salary      3 non-null      float64
dtypes: float64(1), str(1)
memory usage: 196.0 bytes
             Salary
count      3.000000
mean   53333.333333
std    15275.252317
min    40000.000000
25%    45000.000000
50%    50000.000000
75%    60000.000000
max    70000.000000
```
**What it means:** `info` shows Salary has 3 of 4 values; `describe` shows its count is also 3 and the average is about 53,333 (blank ignored).
**Likely follow-ups:**
- *What does `describe` miss?* Text columns, unless `include="all"`; use `value_counts()` for them.
- *`head` vs `sample`?* `sample` picks random rows, a better look when the file is sorted.
**Common mistakes:** trusting only `head()`; assuming `describe` counts blanks; saying `info` gives statistics.

### Q17 ⭐⭐ 🟢 Write code to list all categorical columns and print the value counts of each, including missing values.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** `select_dtypes`, looping over columns and `dropna=False`.
**Say this in the interview:** "I pick the non-numeric columns with `select_dtypes`, loop over them and print `value_counts(dropna=False)` so blanks are counted too."
**Explain simply:**
- **Categorical column:** text labels such as Department or Attrition.
- **`select_dtypes(exclude="number")`:** everything that is not a number.
- **`dropna=False`:** shows the missing count as its own row (`NaN`).
- Version note (verified on pandas 3.0.5): `include="object"` still works but warns, because text is now the `str` type. `exclude="number"` works on old and new versions, but it also picks up date columns.
**Sample data:** `employees.csv` from Q1.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("employees.csv")

categorical_columns = employees.select_dtypes(exclude="number").columns

for column in categorical_columns:
    print(employees[column].value_counts(dropna=False))
    print()
```
**Output:**
```
Department
IT       3
Sales    2
HR       2
NaN      1
Name: count, dtype: int64

JobRole
Executive    2
Recruiter    2
Developer    2
Analyst      1
Manager      1
Name: count, dtype: int64

Attrition
No     5
Yes    3
Name: count, dtype: int64

```
**What it means:** I can see every label, its frequency, and the one missing Department. This also exposes spelling variants like "HR" and "Hr".
**Likely follow-ups:**
- *Columns with too many labels (like names)?* Check `nunique()` first and skip those.
- *Numeric codes that are really categories (grade 1, 2, 3)?* Check them by hand.
**Common mistakes:** forgetting `dropna=False` (blanks vanish); including ID columns; assuming all text columns are categories.

### Q18 ⭐⭐ 🟢 Write code to select only numeric columns of a DataFrame and compute their mean, median and standard deviation.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** `select_dtypes` and `agg` with several functions.
**Say this in the interview:** "`select_dtypes(include='number')` keeps numeric columns, then `agg` with a list of functions gives mean, median and std in one table."
**Explain simply:**
- **Mean:** the average.
- **Median:** the middle value; not pulled up by a few very big values.
- **Standard deviation (std):** how spread out values are around the mean; large means very different values.
- **Mean far from median:** a sign of skew or outliers.
**Sample data:** `employees.csv` from Q1 (numeric columns EmployeeID, Age, MonthlyIncome).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("employees.csv")

numeric_columns = employees.select_dtypes(include="number")
summary = numeric_columns.agg(["mean", "median", "std"])
print(summary.round(1))
```
**Output:**
```
        EmployeeID   Age  MonthlyIncome
mean         104.5  34.0        61000.0
median       104.5  33.0        55000.0
std            2.4   6.9        19536.3
```
**What it means:** average income is 61,000 but the median is 55,000, so a few higher salaries pull the average up. The EmployeeID row is meaningless; an ID is a label, so I would drop it first.
**Likely follow-ups:**
- *What about missing values?* They are skipped automatically (MonthlyIncome used 7 values).
- *Per department?* `employees.groupby("Department")["MonthlyIncome"].agg(["mean", "median", "std"])`.
**Common mistakes:** including ID columns; running `mean()` on a table with text (error in current pandas); reporting the mean alone for skewed pay data.

### Q19 ⭐⭐ 🟢 How do you check whether a column that looks numeric (for example salary) was loaded as object, and how do you convert it safely?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you check dtypes before calculating, and convert without crashing on bad values.
**Say this in the interview:** "I run df.dtypes or df.info(). If salary says object (pandas 3 shows str), it is text. I clean it, then use pd.to_numeric with errors='coerce' so bad entries become NaN instead of stopping my code."
**Explain simply:**
- `dtypes` lists the type of each column: `int64`/`float64` are numbers; `object` or `str` is text.
- A numeric-looking column becomes text when even one cell has a comma, a currency sign or 'N/A'.
- `pd.to_numeric` converts text to numbers. `errors='coerce'` turns anything that cannot convert into NaN (pandas' empty marker).
- Afterwards count the new NaN values to see how many cells were bad; do not hide them.
**Sample data:** Salary typed as text, with a comma and an 'N/A'.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [1, 2, 3, 4],
    "salary": ["45000", "52,000", "N/A", "61000"],
})

# Step 1: check the type of each column
print(employees.dtypes)

# Step 2: remove commas, then convert; bad values become NaN instead of crashing
employees["salary"] = employees["salary"].str.replace(",", "")
employees["salary"] = pd.to_numeric(employees["salary"], errors="coerce")

print(employees)
print(employees["salary"].dtype)
```
**Output:**
```text
employee_id    int64
salary           str
dtype: object
   employee_id   salary
0            1  45000.0
1            2  52000.0
2            3      NaN
3            4  61000.0
float64
```
**What it means:** Salary started as text (`str`; older pandas shows `object`). After cleaning it is a float column, and 'N/A' became NaN. You can now take averages.
**Likely follow-ups:**
1. Why not `astype(float)`? It raises an error on the first bad value. `to_numeric(errors='coerce')` is safer.
2. How do I see which cells failed? `employees[employees['salary'].isna()]` after converting, compared with the raw file.
**Common mistakes:** Using `errors='coerce'` and never checking how many values became NaN. Forgetting that commas or currency symbols must be removed first. Assuming the column is numeric because it looks numeric when printed.

### Q20 ⭐⭐ 🟡 Write code to find the correlation between numeric columns in an HR dataset and list the top 3 pairs with the strongest relationship.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can turn a correlation grid into a ranked list of pairs, without double counting.
**Say this in the interview:** "I call corr() to get a grid, flatten it into pairs, keep each pair once, and sort by absolute strength. I would also warn that correlation is not causation."
**Explain simply:**
- Correlation is a number from -1 to 1 showing how two columns move together. Near 1 or -1 is strong; near 0 is weak.
- `corr()` gives a grid where every pair appears twice and every column pairs with itself at 1.0.
- Keeping only pairs where the first name sorts before the second removes both problems.
- Sorting by absolute value matters: -0.9 is as strong as +0.9.
**Sample data:** Small employee table with age, tenure, salary and satisfaction (8 rows, created in the code).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "age": [25, 32, 41, 29, 50, 38, 45, 27],
    "tenure_years": [1, 5, 12, 3, 20, 9, 15, 2],
    "salary": [30000, 48000, 70000, 41000, 90000, 62000, 75000, 33000],
    "satisfaction": [3, 4, 2, 4, 3, 1, 4, 2],
})

# Correlation between every pair of numeric columns
correlations = employees.corr(numeric_only=True)

# Turn the grid into a list of pairs
pairs = correlations.unstack()

# Keep each pair once (drops a column paired with itself and mirror copies)
pairs = pairs[pairs.index.get_level_values(0) < pairs.index.get_level_values(1)]

# Strongest first, ignoring the sign
top_3_pairs = pairs.sort_values(key=abs, ascending=False).head(3)
print(top_3_pairs.round(3))
```
**Output:**
```text
age     salary          0.997
        tenure_years    0.995
salary  tenure_years    0.991
dtype: float64
```
**What it means:** Age, salary and tenure move together almost perfectly in this tiny sample; that is expected because older staff usually have longer tenure and higher pay. It says nothing about why.
**Likely follow-ups:**
1. What if columns are text? `numeric_only=True` skips them; encode them first if needed.
2. Does a high correlation prove cause? No, it only shows two columns move together.
**Common mistakes:** Reading the self-correlation (1.0) as a finding. Listing each pair twice. Sorting without `abs` so strong negative pairs are lost. Treating correlation as cause.

### Q21 ⭐⭐ 🟡 Write code to compare the average salary, age and tenure of employees who left versus those who stayed.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can compare two groups with groupby, a core attrition-analysis step.
**Say this in the interview:** "I group by the attrition column and take the mean of salary, age and tenure. Then I read the gap: leavers are lower paid, younger and newer."
**Explain simply:**
- `groupby('attrition')` splits rows into the Yes group and the No group.
- Picking three columns in double brackets and calling `mean()` gives one average per group.
- `round(1)` only tidies the display.
- Medians can be safer if a few salaries are extremely high.
**Sample data:** Six employees, three left (Yes) and three stayed (No).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "attrition": ["Yes", "No", "No", "Yes", "No", "Yes"],
    "salary": [32000, 55000, 61000, 35000, 48000, 40000],
    "age": [24, 38, 45, 27, 33, 30],
    "tenure_years": [1, 8, 12, 2, 6, 3],
})

# Average of each column for people who left (Yes) and stayed (No)
comparison = employees.groupby("attrition")[["salary", "age", "tenure_years"]].mean()
print(comparison.round(1))
```
**Output:**
```text
            salary   age  tenure_years
attrition                             
No         54666.7  38.7           8.7
Yes        35666.7  27.0           2.0
```
**What it means:** Leavers earn about 35,700 on average against 54,700 for stayers, are younger (27 vs 38.7) and have much shorter tenure (2 vs 8.7 years). So the risk sits with junior, lower-paid staff.
**Likely follow-ups:**
1. Is the gap proof of cause? No; check group sizes and use a test or more variables.
2. How would you use the median? Replace `mean()` with `median()`.
**Common mistakes:** Forgetting the double brackets (using single brackets with a list fails). Comparing averages when the groups are tiny. Claiming cause from a difference.

### Q22 ⭐⭐ 🟡 Write code to create age bands (for example 18-25, 26-35, 36-45, 46+) with pd.cut and show attrition rate per band.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can bin a number into bands and compute a rate per band.
**Say this in the interview:** "pd.cut groups ages into bands. I turn Attrition into True/False, and the mean of that is the share who left, per band."
**Explain simply:**
- `pd.cut` sorts numbers into bins you define. Bins are 'right-closed': `(17, 25]` means above 17 up to and including 25, so 18 to 25.
- `labels` gives the bands readable names.
- True counts as 1 and False as 0, so the mean of a True/False column is the percentage who left (after times 100).
- `observed=True` keeps only bands that actually exist in the data.
**Sample data:** Ten employees with age and attrition.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "age": [22, 24, 29, 31, 35, 40, 44, 48, 55, 23],
    "attrition": ["Yes", "No", "Yes", "No", "No", "No", "Yes", "No", "No", "Yes"],
})

# Group ages into bands: (17, 25] means 18 to 25, and so on
employees["age_band"] = pd.cut(
    employees["age"],
    bins=[17, 25, 35, 45, 100],
    labels=["18-25", "26-35", "36-45", "46+"],
)

# True for people who left; the average of True/False is the share who left
employees["left"] = employees["attrition"] == "Yes"
attrition_rate = employees.groupby("age_band", observed=True)["left"].mean() * 100
print(attrition_rate.round(1))
```
**Output:**
```text
age_band
18-25    66.7
26-35    33.3
36-45    50.0
46+       0.0
Name: left, dtype: float64
```
**What it means:** Attrition is highest in the youngest band (66.7%) and zero for 46+. Check band sizes: with 10 rows each band holds very few people.
**Likely follow-ups:**
1. Why bins start at 17? Because the first interval excludes its left edge; 17 makes 18 the first age included.
2. Is there another way? `pd.qcut` makes bands of equal size instead of fixed ranges.
**Common mistakes:** Writing bins that leave out the lowest or highest ages (those rows become NaN). Forgetting that the left edge is excluded. Reporting a rate for a band with only two people.

### Q23 ⭐⭐ 🟡 Write code to build a payroll summary: headcount, total gross pay and average gross pay per department, with clear column names.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can summarise by group with named columns, a very common payroll report.
**Say this in the interview:** "I group by department and use named aggregation, so each output column has a clear name: headcount, total and average gross pay."
**Explain simply:**
- Gross pay is the pay before tax and deductions.
- `agg` with `name=(column, function)` builds each summary column and names it in one go.
- `count` counts employees, `sum` adds pay, `mean` averages it.
- `reset_index()` turns the department from the row label back into a normal column.
**Sample data:** Five employees across three departments.
**Code (what you write in the interview):**
```python
import pandas as pd

payroll = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5],
    "department": ["HR", "HR", "IT", "IT", "Sales"],
    "gross_pay": [4000, 4500, 6000, 7000, 5000],
})

# One summary row per department, with clear column names
payroll_summary = payroll.groupby("department").agg(
    headcount=("employee_id", "count"),
    total_gross_pay=("gross_pay", "sum"),
    average_gross_pay=("gross_pay", "mean"),
).reset_index()
print(payroll_summary)
```
**Output:**
```text
  department  headcount  total_gross_pay  average_gross_pay
0         HR          2             8500             4250.0
1         IT          2            13000             6500.0
2      Sales          1             5000             5000.0
```
**What it means:** Each row is one department: IT has 2 people costing 13,000 in total, so 6,500 each on average.
**Likely follow-ups:**
1. How do I add a percentage of total? `payroll_summary['total_gross_pay'] / payroll_summary['total_gross_pay'].sum() * 100`.
2. Should I use `count` or `size`? `count` ignores blanks in that column; `size` counts all rows.
**Common mistakes:** Using `count` on a column with blanks and getting a wrong headcount. Leaving default names like `gross_pay` for three different numbers. Averaging averages instead of totals.

### Q24 ⭐⭐ 🟡 Write code to find employees with more than 3 absences in a month from a daily attendance DataFrame.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can filter rows, group by two keys and filter on the group count.
**Say this in the interview:** "I keep only absent days, add a month column, count absences per employee per month, and keep counts above 3."
**Explain simply:**
- First turn the text date into a real date with `pd.to_datetime`.
- `dt.to_period('M')` gives the month (for example 2026-03), so March of different years does not mix.
- `groupby` on employee and month, then `size()` counts rows in each group.
- Filter the counts with `> 3`, which means 4 or more.
**Sample data:** Daily attendance for three employees in March 2026.
**Code (what you write in the interview):**
```python
import pandas as pd

attendance = pd.DataFrame({
    "employee_id": [101, 101, 101, 101, 101, 102, 102, 103],
    "date": ["2026-03-02", "2026-03-05", "2026-03-09", "2026-03-12", "2026-03-20",
             "2026-03-03", "2026-03-04", "2026-03-10"],
    "status": ["Absent", "Absent", "Absent", "Absent", "Present",
               "Absent", "Absent", "Absent"],
})
attendance["date"] = pd.to_datetime(attendance["date"])

# Keep only absent days and label each with its month
absences = attendance[attendance["status"] == "Absent"].copy()
absences["month"] = absences["date"].dt.to_period("M")

# Count absences per employee per month, then keep more than 3
absence_counts = absences.groupby(["employee_id", "month"]).size()
frequent_absentees = absence_counts[absence_counts > 3]
print(frequent_absentees)
```
**Output:**
```text
employee_id  month  
101          2026-03    4
dtype: int64
```
**What it means:** Employee 101 had 4 absences in March 2026, so they are flagged. Employee 102 had 2, below the limit.
**Likely follow-ups:**
1. How do I get names, not IDs? Merge the result with the employee table.
2. What about leave that is approved? Exclude those statuses before counting.
**Common mistakes:** Counting by employee only, which mixes months. Using `>= 3` when the question says more than 3. Forgetting to convert the date column. Counting Present rows by mistake.

### Q25 ⭐⭐ 🟡 Write code to flag employees whose salary is above the average of their own department (not the whole company).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know transform, which gives a group average back on every row.
**Say this in the interview:** "I use groupby with transform('mean'), which returns the department average on each row. Then a simple comparison gives the flag."
**Explain simply:**
- `groupby('department')['salary'].mean()` returns one row per department, which does not line up with employees.
- `transform('mean')` returns the same average but repeated on every employee row, so you can compare directly.
- The comparison `salary > department_average` gives True or False per person.
- Dina earns exactly the average, so she is not above it.
**Sample data:** Six employees in three departments.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ben", "Chen", "Dina", "Evan", "Fay"],
    "department": ["HR", "HR", "IT", "IT", "IT", "Sales"],
    "salary": [40000, 50000, 60000, 80000, 100000, 45000],
})

# Average salary of each person's own department, written on every row
employees["department_average"] = employees.groupby("department")["salary"].transform("mean")

# True when the person earns more than their department average
employees["above_department_average"] = employees["salary"] > employees["department_average"]
print(employees)
```
**Output:**
```text
   name department  salary  department_average  above_department_average
0  Asha         HR   40000             45000.0                     False
1   Ben         HR   50000             45000.0                      True
2  Chen         IT   60000             80000.0                     False
3  Dina         IT   80000             80000.0                     False
4  Evan         IT  100000             80000.0                      True
5   Fay      Sales   45000             45000.0                     False
```
**What it means:** Ben (HR) and Evan (IT) earn more than their own department's average. Dina equals it, so she is False. Sales has one person, who always equals the average.
**Alternative:** Merge the groupby mean back onto the table; it works but needs more steps than transform.
**Likely follow-ups:**
1. Why not use the company average? A fair comparison is with peers in the same department.
2. How to filter just those people? `employees[employees['above_department_average']]`.
**Common mistakes:** Computing the plain groupby mean and then trying to compare it with the full table (lengths do not match). Using the company-wide mean. Ignoring departments with one person.

### Q26 ⭐⭐ 🟡 Write code to find the department-wise count of employees who joined in each year using a pivot table or crosstab.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can build a count table of two categories with crosstab or pivot_table.
**Say this in the interview:** "pd.crosstab counts rows for each department and year pair. I extract the year from the joining date first."
**Explain simply:**
- Convert the text to a date, then `dt.year` pulls out the year.
- `pd.crosstab(rows, columns)` counts how many rows fall in each combination.
- Departments become rows, years become columns, and cells are headcount joined.
- Combinations with no joiners show 0, not blank.
**Sample data:** Six employees with department and joining date.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["HR", "HR", "IT", "IT", "IT", "Sales"],
    "joining_date": ["2022-03-01", "2023-07-15", "2022-01-10",
                     "2022-11-05", "2023-02-20", "2023-09-01"],
})
employees["joining_year"] = pd.to_datetime(employees["joining_date"]).dt.year

# Rows are departments, columns are years, cells are counts
joiners = pd.crosstab(employees["department"], employees["joining_year"])
print(joiners)
```
**Output:**
```text
joining_year  2022  2023
department              
HR               1     1
IT               2     1
Sales            0     1
```
**What it means:** IT hired 2 people in 2022 and 1 in 2023; Sales hired nobody in 2022. This shows hiring trends by department at a glance.
**Alternative:** `employees.pivot_table(index='department', columns='joining_year', values='joining_date', aggfunc='count', fill_value=0)` gives the same table.
**Likely follow-ups:**
1. Crosstab or pivot table? Same counts here; crosstab is shorter for plain counts, pivot_table is more flexible for sums and averages.
2. How to add totals? Add `margins=True` to crosstab.
**Common mistakes:** Using the full date as columns instead of the year. Forgetting to convert text to dates. Using `pivot_table` without `aggfunc='count'`: the default is the average, which fails on dates or text.

### Q27 ⭐⭐ 🟡 Write code to identify the columns that have only one unique value or a unique value for every row, and explain why you would drop them.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you spot columns that carry no information or are only identifiers.
**Say this in the interview:** "nunique() shows distinct values per column. One value means a constant column; as many values as rows means an ID. Neither helps in analysis."
**Explain simply:**
- `nunique()` counts distinct values in each column.
- A constant column (same value everywhere) cannot explain any difference between employees.
- A column unique per row (ID, email) cannot be grouped or generalised; it only identifies a person.
- Dropping them shrinks the table and avoids noise in models. Keep the ID if you need it to join or look up people.
**Sample data:** Four employees with a constant country and unique ID and email.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104],
    "country": ["India", "India", "India", "India"],
    "department": ["HR", "IT", "HR", "Sales"],
    "email": ["a@x.com", "b@x.com", "c@x.com", "d@x.com"],
})

unique_counts = employees.nunique()

# Same value on every row
constant_columns = unique_counts[unique_counts == 1].index.tolist()

# Different value on every row
all_unique_columns = unique_counts[unique_counts == len(employees)].index.tolist()

print("Constant:", constant_columns)
print("All unique:", all_unique_columns)
```
**Output:**
```text
Constant: ['country']
All unique: ['employee_id', 'email']
```
**What it means:** `country` is the same for everyone, so it explains nothing. `employee_id` and `email` identify people but are useless for patterns. Keep the ID as a lookup key, drop the rest for modelling.
**Likely follow-ups:**
1. Do you always drop IDs? No, keep one for merging and tracing back.
2. What about a column with 99% one value? Treat it as nearly constant and review it.
**Common mistakes:** Dropping the employee ID before you need it for a merge. Forgetting that missing values are not counted by `nunique()` by default. Dropping a column without asking what it means.

### Q28 ⭐⭐ 🟡 Why does a merge sometimes return more rows than the left table, and how do you detect and prevent it with validate= and indicator=True?
**Asked at:** commonly asked; merge row-count checks and `validate=` are named in prep-blog snippets (PracHub, GoLinuxCloud)
**What the interviewer is checking:** Whether you understand many-to-many merges and know the built-in safety checks.
**Say this in the interview:** "A merge returns extra rows when the key repeats in the other table: each match multiplies the row. I compare row counts, use indicator=True to see where rows came from, and use validate='many_to_one' so pandas stops the merge if the key is not unique."
**Explain simply:**
- Merge joins rows with equal keys. If dept 20 appears twice in the department table, each employee in dept 20 is matched twice.
- `indicator=True` adds a `_merge` column: `both`, `left_only` or `right_only`, showing which rows matched.
- `validate='many_to_one'` raises a `MergeError` if the right table has repeated keys.
- Prevent it by removing duplicates in the lookup table first (`drop_duplicates(subset='dept_id')`) or fixing the source.
**Sample data:** Three employees and a department table that wrongly lists dept 20 twice.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [1, 2, 3],
    "dept_id": [10, 20, 20],
})
departments = pd.DataFrame({
    "dept_id": [10, 20, 20],          # dept 20 appears twice by mistake
    "dept_name": ["HR", "IT", "IT Ops"],
})

# Plain merge: 3 employees become 4 rows
merged = employees.merge(departments, on="dept_id", how="left", indicator=True)
print(len(employees), "->", len(merged))
print(merged["_merge"].value_counts())

# validate stops the merge when the right table has repeated keys
try:
    employees.merge(departments, on="dept_id", how="left", validate="many_to_one")
except pd.errors.MergeError as error:
    print(error)
```
**Output:**
```text
3 -> 5
_merge
both          5
left_only     0
right_only    0
Name: count, dtype: int64
Merge keys are not unique in right dataset; not a many-to-one merge

Duplicates in right:
  dept_id
      20 ...
```
**What it means:** Three employees became 5 rows: the two employees in dept 20 each matched both dept 20 rows. `_merge` shows all 5 as `both`, so the count check is what reveals the problem. `validate` raised an error, which is the safeguard.
**Likely follow-ups:**
1. Which validate values exist? `one_to_one`, `one_to_many`, `many_to_one`, `many_to_many`.
2. How do I find lost rows? Filter `_merge == 'left_only'`.
**Common mistakes:** Not comparing row counts before and after. Using an inner merge and silently losing employees. Dropping duplicates without checking which row is right.

### Q29 ⭐⭐ 🟡 You get a SettingWithCopyWarning while creating a new column on a filtered DataFrame during EDA. Why does it happen and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand copies versus views and can write safe code.
**Say this in the interview:** "The warning means I may be changing a slice of another table, so pandas is not sure what happens. I fix it by taking an explicit .copy() of the filtered table, or by using .loc on the original."
**Explain simply:**
- Filtering creates a new table that may share data with the original; writing to it was ambiguous in older pandas, hence the warning.
- Fix: `filtered = df[df['department'] == 'IT'].copy()` and then add columns to `filtered`.
- To change the original table, use `df.loc[condition, 'column'] = value`.
- Verified here on pandas 3: the original table is not changed and no warning appears, because pandas 3 always copies on write. Older 2.x versions can warn, so writing `.copy()` is still good habit (2.x behaviour from memory, unverified).
**Sample data:** Four employees; we want a bonus column only for the IT slice.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ben", "Chen", "Dina"],
    "department": ["HR", "IT", "IT", "Sales"],
    "salary": [40000, 60000, 80000, 45000],
})

# Risky: a slice that may or may not be a copy
it_staff = employees[employees["department"] == "IT"]
it_staff["bonus"] = it_staff["salary"] * 0.1

# Fix: make an explicit copy, then add the column
it_staff = employees[employees["department"] == "IT"].copy()
it_staff["bonus"] = it_staff["salary"] * 0.1
print(it_staff)
print("bonus" in employees.columns)
```
**Output:**
```text
   name department  salary   bonus
1   Ben         IT   60000  6000.0
2  Chen         IT   80000  8000.0
False
```
**What it means:** The IT slice gets its own bonus column and the original table has no `bonus` column (False). That is the safe, predictable result.
**Likely follow-ups:**
1. How do I update the original? `employees.loc[employees['department'] == 'IT', 'bonus'] = ...`.
2. Should I silence the warning? No; fix the cause.
**Common mistakes:** Ignoring the warning, or hiding it with options. Chaining indexing like `df[df.x > 1]['y'] = 0`, which never updates the original. Expecting the original to change when working on a slice.

### Q30 ⭐⭐ 🟡 You get a KeyError for a column name that you can clearly see in the file. What are the likely causes (spaces, case, encoding) and how do you fix them?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you debug dirty column names methodically instead of guessing.
**Say this in the interview:** "First I print the column list to see exactly what the names are. Usually there is a hidden space, a different capital letter, or an invisible character at the start of the file."
**Explain simply:**
- Print `df.columns.tolist()`; quotes reveal leading and trailing spaces such as `'Salary '`.
- Case matters: `Salary` and `salary` are different names.
- A file saved by Excel with a BOM (an invisible marker) can make the first column look like `\ufeffEmployee ID`. Reload with `encoding='utf-8-sig'`.
- Fix by cleaning names once after loading: `strip()` and `lower()`.
**Sample data:** A table whose names have a leading and a trailing space.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    " Employee ID": [1, 2],
    "Salary ": [40000, 50000],
    "department": ["HR", "IT"],
})

# repr (the quoted form) shows hidden spaces
print(employees.columns.tolist())

# Fix: clean the names, then use the clean name
employees.columns = employees.columns.str.strip().str.lower()
print(employees.columns.tolist())
print(employees["salary"].mean())
```
**Output:**
```text
[' Employee ID', 'Salary ', 'department']
['employee id', 'salary', 'department']
45000.0
```
**What it means:** The list showed `' Employee ID'` and `'Salary '`; `df['Salary']` would raise a KeyError. After cleaning, `df['salary']` works.
**Likely follow-ups:**
1. How do I fix a BOM? `pd.read_csv(path, encoding='utf-8-sig')`.
2. How do I search for a similar name? `[c for c in df.columns if 'sal' in c.lower()]`.
**Common mistakes:** Retyping the name again and again without printing the real names. Cleaning names but forgetting to use the new lowercase version. Missing non-breaking spaces copied from web pages.

### Q31 ⭐⭐ 🟡 Write code to standardise column names (strip spaces, lower case, replace spaces with underscores) right after loading a file.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you start each project with consistent, easy column names.
**Say this in the interview:** "Right after loading I strip spaces, lower case everything and replace spaces with underscores, so names are predictable and easy to type."
**Explain simply:**
- `df.columns.str` lets you apply text functions to every column name at once.
- `strip()` removes spaces at the ends, `lower()` makes everything small letters, `replace(' ', '_')` swaps inner spaces.
- Order matters: strip first, otherwise an end space becomes a stray underscore.
- Assign the result back to `df.columns`.
**Sample data:** Three columns with spaces and capitals.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    " Employee ID ": [1, 2],
    "Joining Date": ["2024-01-05", "2024-03-10"],
    "Monthly SALARY": [40000, 50000],
})

# Strip spaces, lower case, then spaces become underscores
employees.columns = (
    employees.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)
print(employees.columns.tolist())
```
**Output:**
```text
['employee_id', 'joining_date', 'monthly_salary']
```
**What it means:** Names are now `employee_id`, `joining_date`, `monthly_salary`: no spaces, all lower case, safe to use as `df.monthly_salary`.
**Likely follow-ups:**
1. How to rename one column? `df.rename(columns={'old': 'new'})`.
2. What about symbols like '%'? Add another `.str.replace`.
**Common mistakes:** Replacing spaces before stripping, which leaves leading underscores. Forgetting to assign back. Using names with spaces and then needing brackets and quotes everywhere.

### Q32 ⭐⭐ 🟡 Write code to find the month with the highest total sales in a sales DataFrame and the month-over-month growth percentage.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can aggregate by month, find the max and compute growth.
**Say this in the interview:** "I convert dates, total revenue by month, use idxmax to find the best month, and pct_change times 100 for month-over-month growth."
**Explain simply:**
- `dt.to_period('M')` labels each date with its month, so grouping gives monthly totals.
- `idxmax()` returns the label (the month) with the highest value; `max()` returns the value.
- `pct_change()` compares each month with the previous one: (this - last) / last.
- The first month has no previous month, so its growth is NaN.
**Sample data:** Six orders across three months.
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({
    "order_date": ["2026-01-05", "2026-01-20", "2026-02-11",
                   "2026-02-25", "2026-03-08", "2026-03-30"],
    "revenue": [1000, 500, 1200, 600, 1000, 800],
})
sales["order_date"] = pd.to_datetime(sales["order_date"])

# Total revenue for each calendar month
monthly_revenue = sales.groupby(sales["order_date"].dt.to_period("M"))["revenue"].sum()

best_month = monthly_revenue.idxmax()
print("Best month:", best_month, monthly_revenue.max())

# Percentage change from the previous month
growth_percent = monthly_revenue.pct_change() * 100
print(growth_percent.round(1))
```
**Output:**
```text
Best month: 2026-02 1800
order_date
2026-01     NaN
2026-02    20.0
2026-03     0.0
Freq: M, Name: revenue, dtype: float64
```
**What it means:** February was best with 1,800 revenue; it grew 20% over January (1,500), and March (1,800) was flat (0%).
**Likely follow-ups:**
1. What if months are missing? Reindex to a full month range first.
2. Year-over-year growth? `pct_change(12)` on monthly data.
**Common mistakes:** Grouping by month name only, which mixes years. Forgetting to convert dates first. Reading the NaN in the first month as an error.

### Q33 ⭐⭐ 🟡 Write code to check whether two DataFrames (for example last month and this month employee lists) have employees present in one but missing in the other.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can reconcile two lists, a typical HR data check.
**Say this in the interview:** "I use isin with a tilde to find IDs in one list but not the other, both directions: leavers or missing, and new joiners."
**Explain simply:**
- `isin` checks whether each value is in another list; it returns True/False.
- `~` (tilde) flips True and False, giving 'not in'.
- Last month minus this month is who disappeared; this month minus last month is who is new.
- Compare with a unique ID, never with names, which can repeat or have typos.
**Sample data:** Two small employee ID lists.
**Code (what you write in the interview):**
```python
import pandas as pd

last_month = pd.DataFrame({"employee_id": [101, 102, 103, 104]})
this_month = pd.DataFrame({"employee_id": [102, 103, 104, 105]})

# In last month's list but not this month's (left or missing)
missing_this_month = last_month[~last_month["employee_id"].isin(this_month["employee_id"])]

# In this month's list but not last month's (new joiners)
new_this_month = this_month[~this_month["employee_id"].isin(last_month["employee_id"])]

print(missing_this_month)
print(new_this_month)
```
**Output:**
```text
   employee_id
0          101
   employee_id
3          105
```
**What it means:** Employee 101 was on last month's list but not this month's. Employee 105 is new this month.
**Alternative:** `last_month.merge(this_month, on='employee_id', how='outer', indicator=True)` shows `left_only` and `right_only` rows in one table.
**Likely follow-ups:**
1. How to do it in one go? Merge with `how='outer'` and `indicator=True`.
2. What about duplicates in a list? Run `drop_duplicates()` first.
**Common mistakes:** Comparing by name instead of ID. Checking only one direction. Forgetting that IDs may be stored as text in one file and numbers in the other.

### Q34 ⭐⭐ 🟡 Write code to find the top 3 products by revenue within each region.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can rank within groups, a classic top-N-per-group task.
**Say this in the interview:** "I total revenue by region and product, sort within each region from highest to lowest, then take the first three per region with groupby head(3)."
**Explain simply:**
- First add up revenue for each region and product pair.
- Sorting by region, then revenue descending, puts each region's best products first.
- `groupby('region').head(3)` keeps the first three rows of each region.
- Regions with fewer than three products simply show fewer rows.
**Sample data:** Seven rows of region, product and revenue.
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({
    "region": ["North", "North", "North", "North", "South", "South", "South"],
    "product": ["A", "B", "C", "D", "A", "B", "C"],
    "revenue": [500, 900, 300, 700, 400, 200, 600],
})

# Total revenue of each product in each region
product_revenue = sales.groupby(["region", "product"])["revenue"].sum().reset_index()

# Sort biggest first inside each region, then keep the first 3 of each region
top_3_products = (
    product_revenue
    .sort_values(["region", "revenue"], ascending=[True, False])
    .groupby("region")
    .head(3)
)
print(top_3_products)
```
**Output:**
```text
  region product  revenue
1  North       B      900
3  North       D      700
0  North       A      500
6  South       C      600
4  South       A      400
5  South       B      200
```
**What it means:** North shows its top 3 (B, D, A) and drops C; South has only 3 products so all appear.
**Likely follow-ups:**
1. How to handle ties? `head` just takes the first rows; use `rank(method='min')` if ties should all be kept.
2. Another way? `nlargest(3)` inside `groupby`.
**Common mistakes:** Taking the overall `head(3)` instead of per region. Sorting only by revenue, so regions interleave. Forgetting to add up repeated product rows first.

### Q35 ⭐⭐ 🟡 How do you decide between dropping, filling with the median, or flagging missing values in a dataset during EDA? Show the code for each option.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you choose a missing-value strategy with reasons, not by habit.
**Say this in the interview:** "It depends on how much is missing and why. Few missing and random: drop. Numbers with outliers: fill with median. If missingness may mean something, flag it first, then fill."
**Explain simply:**
- Drop when little is missing and rows are not important or the target is missing; dropping many rows biases results.
- Fill with the median for skewed numbers like salary; the mean is pulled by extreme values.
- Flag with a True/False column when 'missing' itself carries meaning, e.g. no performance rating may mean a new joiner.
- Always say what you did and why, and never fill the key column you are predicting silently.
**Sample data:** Five employees, two with no salary.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5],
    "salary": [40000, None, 52000, 48000, None],
})

# Option 1: drop rows with no salary
dropped = employees.dropna(subset=["salary"])

# Option 2: fill with the median (not hurt by very high salaries)
filled = employees.copy()
filled["salary"] = filled["salary"].fillna(filled["salary"].median())

# Option 3: flag first, so the gap is not hidden, then fill
flagged = employees.copy()
flagged["salary_was_missing"] = flagged["salary"].isna()
flagged["salary"] = flagged["salary"].fillna(flagged["salary"].median())

print(len(dropped), "rows left after dropping")
print(filled)
print(flagged)
```
**Output:**
```text
3 rows left after dropping
   employee_id   salary
0            1  40000.0
1            2  48000.0
2            3  52000.0
3            4  48000.0
4            5  48000.0
   employee_id   salary  salary_was_missing
0            1  40000.0               False
1            2  48000.0                True
2            3  52000.0               False
3            4  48000.0               False
4            5  48000.0                True
```
**What it means:** Dropping leaves 3 rows. Filling puts the median (48,000) into both gaps. The flagged version fills the same way but keeps a record of which were filled.
**Likely follow-ups:**
1. Why median over mean? A few very high salaries would inflate the mean.
2. What if 40% is missing? Think about dropping the column or collecting the data again.
**Common mistakes:** Filling with 0, which looks like a real value. Filling before checking why data is missing. Not recording what was filled. Changing the original DataFrame without a copy.

### Q36 ⭐⭐ 🟡 How would you check data quality of a new dataset (completeness, duplicates, valid ranges, consistent categories) and produce a short data-quality summary table in pandas?
**Asked at:** commonly asked; the data-quality EDA task wording appears in a PracHub practice question (snippet)
**What the interviewer is checking:** Whether you check data quality in a structured way before trusting any analysis.
**Say this in the interview:** "I check four things: completeness (missing counts and percentages), duplicates, valid ranges, and consistent categories. Then I put the numbers in one small table and say what I would fix."
**Explain simply:**
- Completeness: how many cells are missing per column, as a count and a percent.
- Duplicates: repeated whole rows and repeated IDs that should be unique.
- Valid ranges: values that are impossible, such as age 150 (`between(18, 65)`).
- Consistent categories: `value_counts()` reveals variants like `IT` and `it ` (stray space).
**Sample data:** Five employees with a duplicate row, an impossible age and an inconsistent department label.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [1, 2, 2, 4, 5],
    "age": [28, 34, 34, 150, None],
    "department": ["HR", "IT", "IT", "it ", "Sales"],
    "salary": [40000, 55000, 55000, 62000, None],
})

# Completeness and variety, one row per column
quality = pd.DataFrame({
    "missing_count": employees.isna().sum(),
    "missing_percent": (employees.isna().mean() * 100).round(1),
    "unique_values": employees.nunique(),
})
print(quality)

# Duplicates, impossible ages and inconsistent labels
print("Duplicate rows:", employees.duplicated().sum())
print("Duplicate employee_ids:", employees["employee_id"].duplicated().sum())
print("Ages outside 18-65:", (~employees["age"].between(18, 65)).sum())
print(employees["department"].value_counts())
```
**Output:**
```text
             missing_count  missing_percent  unique_values
employee_id              0              0.0              4
age                      1             20.0              3
department               0              0.0              4
salary                   1             20.0              3
Duplicate rows: 1
Duplicate employee_ids: 1
Ages outside 18-65: 2
department
IT       2
HR       1
it       1
Sales    1
Name: count, dtype: int64
```
**What it means:** Age and salary are each 20% missing; one row is an exact duplicate and one ID repeats; two ages fail the range check (150 and the missing one, because a missing value is not between 18 and 65); and the department has inconsistent labels (`IT` versus `it `). That is a clear to-do list before analysis.
**Likely follow-ups:**
1. How would you fix categories? `str.strip().str.title()` or `str.upper()`.
2. Would you remove the age 150? Check the source first; maybe fix it, else set to NaN.
**Common mistakes:** Only checking missing values and nothing else. Not looking at value_counts, so spelling variants stay hidden. Deleting rows without telling anyone.

### Q37 ⭐⭐ 🟡 Write code to plot a histogram of salary, a bar chart of attrition by department and a boxplot of salary by job level, and say what each chart tells you.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you pick the right chart for the question and read it in business words.
**Say this in the interview:** "Histogram for how salaries are spread, bar chart to compare attrition across departments, boxplot to compare salary spread across job levels and spot outliers."
**Explain simply:**
- **Histogram:** groups salaries into bins and counts people per bin; shows the shape (skew, clusters).
- **Bar chart:** one bar per department; plot the attrition **rate** (leavers divided by headcount), not the raw count, or big departments always look worse.
- **Boxplot:** the box is the middle 50% of salaries, the line inside is the median, dots beyond the whiskers are outliers.
- Always add a title and axis labels so a reader needs no explanation.
**Sample data:** 8 employees with department, job_level, monthly_income, attrition.
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

employees = pd.DataFrame({
    "department": ["Sales","Sales","Sales","IT","IT","IT","HR","HR"],
    "job_level": [1,2,3,1,2,3,1,2],
    "monthly_income": [30000,42000,90000,45000,60000,150000,28000,40000],
    "attrition": ["Yes","No","No","No","Yes","No","No","No"],
})

# 1. Histogram: how salaries are spread
employees["monthly_income"].plot(kind="hist", bins=5, title="Salary distribution")
plt.xlabel("Monthly income")
plt.show()

# 2. Bar chart: attrition rate (%) per department
attrition_rate = (employees["attrition"] == "Yes").groupby(employees["department"]).mean() * 100
attrition_rate.sort_values(ascending=False).plot(kind="bar", title="Attrition rate by department (%)")
plt.ylabel("Attrition %")
plt.show()

# 3. Boxplot: salary spread at each job level
employees.boxplot(column="monthly_income", by="job_level")
plt.show()
```
**Output:** three charts open one after another (images are not pasted here). The numbers behind the bar chart:
```
IT       33.3
Sales    33.3
HR        0.0
```
**What it means:** the histogram shows most pay is low with a long tail of high earners (right skew); the bar chart says IT and Sales lose a third of staff while HR loses none; the boxplot shows pay rising with level and a wider spread at the top.
**Likely follow-ups:**
- *Why rate and not count?* Counts depend on department size; rate is fair.
- *What if a chart shows outliers?* Check if they are real (executives) or data errors before removing.
**Common mistakes:** plotting raw leaver counts, too many bins or too few, missing titles and labels, forgetting `plt.show()` in a script.

### Q38 ⭐⭐ 🔴 Write code that takes any DataFrame and prints an automatic profile: shape, dtypes, missing percentage, unique counts and basic statistics in one summary table.
**Asked at:** commonly asked (no company-specific report found); a Pivigo candidate report mentions EDA with pandas as a live task (snippet only).
**What the interviewer is checking:** Can you wrap repeated steps into a reusable function and combine pieces into one table.
**Say this in the interview:** "I build one table with a row per column: dtype, missing percent, unique values, then join the describe statistics for the numeric columns."
**Explain simply:**
- **Function:** a named block of code you can call on any DataFrame, so you do not retype the steps.
- **dtype:** the type of data in a column (number, text, date).
- **Unique count:** `nunique()` counts distinct values, useful to spot IDs and constant columns.
- **Join:** `describe()` only covers numeric columns, so text columns show blank (NaN) statistics.
**Sample data:** 5 employees with a missing department, age and income.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Sales","IT","IT","HR",None],
    "age": [29, 41, None, 35, 52],
    "monthly_income": [30000, 60000, 62000, None, 90000],
})

def profile(df):
    summary = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing_pct": (df.isna().mean() * 100).round(1),
        "unique_values": df.nunique(),
    })
    # basic statistics only exist for numeric columns, others stay blank
    stats = df.describe().T[["mean", "min", "max"]]
    summary = summary.join(stats)
    print("Shape:", df.shape)
    return summary

print(profile(employees))
```
**Output:**
```
Shape: (5, 3)
                  dtype  missing_pct  unique_values      mean      min      max
department          str         20.0              3       NaN      NaN      NaN
age             float64         20.0              4     39.25     29.0     52.0
monthly_income  float64         20.0              4  60500.00  30000.0  90000.0
```
**What it means:** every column on one line: each has 20% missing; department is text so it has no mean. (On this pandas 3 install text shows as `str`; older versions show `object`.)
**Likely follow-ups:**
- *How do you add text columns' info?* `describe(include="all")`.
- *What if a column is all unique?* Likely an ID, exclude from analysis.
**Common mistakes:** counting missing with `isnull().sum()` only (gives counts, not percent), forgetting `.T` so statistics line up per column, crashing on a DataFrame with no numeric columns.

### Q39 ⭐⭐ 🔴 Write code to compute a 3-month rolling average of monthly headcount and flag months where hiring dropped more than 20 percent.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** `rolling`, `pct_change` and a boolean flag, and whether you know the first rows will be blank.
**Say this in the interview:** "Rolling average with window 3 smooths the trend; percent change of hires versus last month, and I flag anything below minus 20."
**Explain simply:**
- **Rolling average:** each month's value is the average of that month and the 2 before it, so noise is smoothed.
- **Window:** how many rows are averaged (3 here). The first 2 months have no result (NaN) because they lack history.
- **pct_change:** (this month minus last month) divided by last month.
- Data must be sorted by month first.
**Sample data:** 6 months of headcount and hires.
**Code (what you write in the interview):**
```python
import pandas as pd

monthly = pd.DataFrame({
    "month": ["2025-01","2025-02","2025-03","2025-04","2025-05","2025-06"],
    "headcount": [100, 108, 115, 118, 119, 121],
    "hires": [10, 12, 15, 6, 12, 14],
})

# Average of this month and the two before it
monthly["headcount_3m_avg"] = monthly["headcount"].rolling(window=3).mean().round(1)

# Percentage change in hires versus the previous month
monthly["hiring_change_pct"] = (monthly["hires"].pct_change() * 100).round(1)

# Flag months where hiring fell by more than 20 percent
monthly["hiring_drop_flag"] = monthly["hiring_change_pct"] < -20
print(monthly.to_string())
```
**Output:**
```
     month  headcount  hires  headcount_3m_avg  hiring_change_pct  hiring_drop_flag
0  2025-01        100     10               NaN                NaN             False
1  2025-02        108     12               NaN               20.0             False
2  2025-03        115     15             107.7               25.0             False
3  2025-04        118      6             113.7              -60.0              True
4  2025-05        119     12             117.3              100.0             False
5  2025-06        121     14             119.3               16.7             False
```
**What it means:** April hiring fell 60%, so it is flagged; May's jump back is a rebound, not a new problem.
**Likely follow-ups:**
- *How to keep the first months?* `rolling(3, min_periods=1)`.
- *Drop versus the rolling average instead?* Compare hires to its own rolling mean.
**Common mistakes:** unsorted months, comparing headcount instead of hires for the "hiring drop", forgetting the first month's change is NaN (so the flag is False, not a drop).

### Q40 ⭐⭐ 🔴 Write code to find employees whose exit date is before their joining date, or whose age is below 18 or above 70, as data validity checks.
**Asked at:** commonly asked (no company-specific report found); PracHub lists data-quality diagnosis as an EDA task (snippet only).
**What the interviewer is checking:** Do you test business rules, combine conditions correctly and handle blank exit dates.
**Say this in the interview:** "I write each rule as a True/False check, combine with `|` (or), and list the rows that break any rule."
**Explain simply:**
- **Validity check:** a rule real data must obey (nobody leaves before they join).
- **Boolean mask:** a column of True/False used to filter rows.
- **`|` means or, `&` means and;** each condition needs its own brackets.
- **NaT:** blank date. Comparing with NaT gives False, so active employees (no exit date) are correctly not flagged.
**Sample data:** 5 employees; ID 2 is 17, ID 3 exits before joining, ID 4 is 72.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5],
    "age": [28, 17, 45, 72, 33],
    "joining_date": pd.to_datetime(["2020-01-10","2023-05-01","2019-03-15","2010-07-01","2021-09-01"]),
    "exit_date": pd.to_datetime(["2022-02-01", None, "2018-12-31", None, None]),
})

exit_before_joining = employees["exit_date"] < employees["joining_date"]
age_out_of_range = (employees["age"] < 18) | (employees["age"] > 70)

invalid_rows = employees[exit_before_joining | age_out_of_range]
print(invalid_rows)
```
**Output:**
```
   employee_id  age joining_date  exit_date
1            2   17   2023-05-01        NaT
2            3   45   2019-03-15 2018-12-31
3            4   72   2010-07-01        NaT
```
**What it means:** three records need review with HR; do not delete blindly, a 72-year-old consultant may be real.
**Likely follow-ups:**
- *What do you do with them?* Report to the data owner, fix at source, or flag in a column.
- *Missing age?* A NaN age passes both tests, so check missing separately.
**Common mistakes:** using `or` instead of `|`, missing brackets, forgetting that dates must be real datetimes (text dates compare wrongly).

### Q41 ⭐⭐ 🔴 Write code to compare cohorts: for each joining-year cohort, calculate the percentage still employed after 1 and 2 years.
**Asked at:** commonly asked (no company-specific report found); a standard retention-analysis composite.
**What the interviewer is checking:** Cohort thinking and the trap of counting people who have not had enough time yet.
**Say this in the interview:** "A cohort is everyone who joined in the same year. For each person I check whether they were still here at their 1 and 2 year anniversary, but only count those who have reached that anniversary by today."
**Explain simply:**
- **Cohort:** a group that shares a starting point (joining year).
- **Still employed after N years:** no exit date, or exit later than joining date plus N years.
- **Censoring:** someone who joined 6 months ago cannot show 1-year retention yet; leave them blank (NaN) so they are not counted as "stayed".
- `mean()` of True/False gives the share (True = 1) and skips NaN.
**Sample data:** 8 employees joining 2021 to 2023, some with exit dates; today is 2024-12-31.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": range(1, 9),
    "joining_date": pd.to_datetime(["2021-03-01","2021-06-01","2021-09-01","2022-01-15",
                                    "2022-04-01","2022-08-01","2023-02-01","2023-05-01"]),
    "exit_date": pd.to_datetime(["2021-12-01", None, "2023-10-01", "2022-06-01",
                                 None, "2024-01-01", None, None]),
})
today = pd.Timestamp("2024-12-31")

employees["joining_year"] = employees["joining_date"].dt.year

# Only count people who have had N full years to be observed
for years in [1, 2]:
    anniversary = employees["joining_date"] + pd.DateOffset(years=years)
    observed = anniversary <= today
    still_there = employees["exit_date"].isna() | (employees["exit_date"] > anniversary)
    employees[f"stayed_{years}y"] = still_there.astype(float).where(observed)

retention = employees.groupby("joining_year")[["stayed_1y", "stayed_2y"]].mean() * 100
print(retention.round(1))
```
**Output:**
```
              stayed_1y  stayed_2y
joining_year                      
2021               66.7       66.7
2022               66.7       33.3
2023              100.0        NaN
```
**What it means:** the 2022 joiners keep fewer people at year 2 (33%) than 2021 did (67%); 2023 has no 2-year number yet.
**Likely follow-ups:**
- *Small cohorts?* Show headcount beside the percentage; 3 people is not a trend.
- *How to chart?* Line per cohort, years on the x-axis.
**Common mistakes:** treating "no exit date yet" as retained for people who have not reached the anniversary, using calendar year differences instead of exact anniversaries.

### Q42 ⭐⭐ 🔴 You find that 15 percent of the salary column is missing. How do you investigate whether the missingness is random or related to department or location before filling it?
**Asked at:** commonly asked (no company-specific report found); Tiger Analytics candidate reports mention mean imputation (snippet only).
**What the interviewer is checking:** Do you understand that missing values can carry a pattern, and that filling blindly can hide it.
**Say this in the interview:** "I create a flag column for missing salary and compare the missing rate across department and location. If it is similar everywhere it looks random; if one group is high, the cause is probably a process issue, and I fix or ask before filling."
**Explain simply:**
- **Missing completely at random (MCAR):** blanks have no pattern; filling with the median is usually safe.
- **Related to a group (MAR):** e.g. one department never entered salary; a company-wide median would be wrong for them.
- **Related to the value itself (MNAR):** e.g. high earners hide pay; hardest case, cannot be seen in the data, so ask the data owner.
- **Method:** flag, group, compare rates. Also compare other columns (age, tenure) between missing and not-missing rows.
**Sample data:** 10 employees, 4 salaries missing, mostly in Sales.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Sales","Sales","Sales","Sales","IT","IT","IT","IT","HR","HR"],
    "location": ["Hyderabad","Hyderabad","Bengaluru","Bengaluru","Hyderabad","Bengaluru","Bengaluru","Bengaluru","Hyderabad","Hyderabad"],
    "monthly_income": [None, None, None, 40000, 60000, 65000, None, 70000, 35000, 36000],
})

employees["salary_missing"] = employees["monthly_income"].isna()

# Share of missing salary inside each department and location
print(employees.groupby("department")["salary_missing"].mean() * 100)
print(employees.groupby("location")["salary_missing"].mean() * 100)
```
**Output:**
```
department
HR        0.0
IT       25.0
Sales    75.0
Name: salary_missing, dtype: float64
location
Bengaluru    40.0
Hyderabad    40.0
Name: salary_missing, dtype: float64
```
**What it means:** location makes no difference (40% each) but Sales is missing 75%, so it is not random; talk to Sales or HR ops before filling.
**Likely follow-ups:**
- *Then how do you fill?* Median within department, or flag and leave it out of salary analysis.
- *Any formal test?* A chi-square test of the missing flag against department (it checks whether the gap is bigger than chance would explain).
**Common mistakes:** filling the median first and losing the evidence, checking only the overall percent, ignoring that small groups give noisy percentages.

### Q43 ⭐⭐ 🔴 Interviewer gives you a 5-minute task: 'Which department needs retention attention most?' Which columns, aggregations and charts do you use to answer it with evidence?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you turn a vague business ask into a clear metric, a few steps and a decision, fast.
**Say this in the interview:** "I would define attrition rate per department, show it next to headcount so small teams do not mislead, check one or two drivers like overtime and tenure, and answer with a ranked bar chart and one sentence."
**Explain simply:**
- **Columns:** department, attrition (Yes/No), headcount (rows), plus drivers: overtime, monthly income, years at company, satisfaction.
- **Aggregations:** `groupby("department")` with count of employees, count of leavers, attrition rate (%).
- **Rank by rate, but keep headcount:** 50% of 4 people is not the same as 20% of 400.
- **Drill down for the top department:** which job roles, tenure bands or overtime groups drive it.
- **Charts:** (1) sorted bar chart of attrition rate by department with the company average line; (2) bar chart of rate by overtime or tenure inside the top department.
- **Finish:** "Department X is highest at N%, about Y people a year, mostly short-tenure staff working overtime; I'd start with a stay-interview there."
**What it means:** the answer is a ranked department with a number, its headcount, one likely driver and a next step, delivered in a few minutes.
**Likely follow-ups:**
- *What if two departments are close?* Look at headcount and cost of leavers (salary).
- *Is it the department or the roles in it?* Break down by job role.
**Common mistakes:** ranking by number of leavers only, no company benchmark, a long analysis with no recommendation, overclaiming causes from one chart.

### Q44 ⭐⭐ 🔴 Write code to reconcile two payroll files by employee ID and list records where net pay differs by more than 1 rupee.
**Asked at:** commonly asked (no company-specific report found); PracHub-style merge and data-check tasks.
**What the interviewer is checking:** Outer merge, `indicator`, tolerance comparison, and noticing IDs missing from one file.
**Say this in the interview:** "I outer-merge on employee ID so no one is dropped, use indicator to see which file each ID came from, then list the ones in both files where the absolute difference is more than 1 rupee, and separately the ones in only one file."
**Explain simply:**
- **Reconcile:** compare two sources of the same facts and list where they disagree.
- **Outer merge:** keeps IDs from both files; missing side becomes NaN.
- **`indicator=True`:** adds `_merge` with `both`, `left_only` or `right_only`.
- **Tolerance:** pay is calculated in decimals, so allow a 1 rupee rounding gap; `abs()` catches differences in both directions.
**Sample data:** HR file has IDs 101 to 104, bank file has 101, 102, 103, 105.
**Code (what you write in the interview):**
```python
import pandas as pd

payroll_hr = pd.DataFrame({"employee_id": [101, 102, 103, 104], "net_pay": [50000.00, 42000.00, 38500.50, 61000.00]})
payroll_bank = pd.DataFrame({"employee_id": [101, 102, 103, 105], "net_pay": [50000.00, 41990.00, 38500.00, 47000.00]})

# Keep every ID from both files and note where each ID was found
reconciled = payroll_hr.merge(payroll_bank, on="employee_id", how="outer",
                              suffixes=("_hr", "_bank"), indicator=True)

# Records present in both files with a difference of more than 1 rupee
reconciled["difference"] = reconciled["net_pay_hr"] - reconciled["net_pay_bank"]
mismatches = reconciled[(reconciled["_merge"] == "both") & (reconciled["difference"].abs() > 1)]
print(mismatches)

# IDs found in only one file
print(reconciled[reconciled["_merge"] != "both"])
```
**Output:**
```
   employee_id  net_pay_hr  net_pay_bank _merge  difference
1          102     42000.0       41990.0   both        10.0
   employee_id  net_pay_hr  net_pay_bank      _merge  difference
3          104     61000.0           NaN   left_only         NaN
4          105         NaN       47000.0  right_only         NaN
```
**What it means:** employee 102 differs by Rs 10 (investigate); 103's 0.50 gap is within tolerance; 104 is paid in HR but not in the bank file, 105 the reverse.
**Likely follow-ups:**
- *Duplicate IDs?* Use `validate="one_to_one"` in the merge so it errors.
- *Why not inner merge?* It would hide missing employees.
**Common mistakes:** inner merge (silently loses unmatched IDs), comparing with `!=` on decimals, forgetting `abs()` so negative differences are missed.

### Q45 ⭐⭐ 🔴 How do you handle a dataset too large to fit comfortably in memory when doing EDA in pandas (chunksize, usecols, dtypes)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know cheap fixes before reaching for big-data tools.
**Say this in the interview:** "First load only the columns I need with `usecols`, use smaller types like category, and if it still does not fit, read in chunks and combine small per-chunk results."
**Explain simply:**
- **`usecols`:** read only the listed columns; usually the biggest saving, because unused columns are never loaded.
- **`dtype`:** text columns with few repeated values become `category`; whole numbers can be `int32` instead of `int64`.
- **`chunksize`:** returns the file in pieces of N rows; you process each piece and keep only a small summary (a sum, a count), never the whole piece.
- **Other options:** read a sample with `nrows`, filter rows early, or move to a database/Parquet file.
- Only sums, counts, min and max combine easily across chunks; an average needs sum and count kept separately.
**Sample data:** `employees.csv` with 12 rows (chunk size 5 here only to show the idea; use 100,000 or more for real).
**Code (what you write in the interview):**
```python
import pandas as pd

total_rows = 0
income_by_department = {}

# Read 5 rows at a time (use 100_000 or more for a real big file), only 2 columns
chunks = pd.read_csv("employees.csv", usecols=["department", "monthly_income"],
                     dtype={"department": "category"}, chunksize=5)

for chunk in chunks:
    total_rows += len(chunk)
    # keep a small running result from each chunk, not the whole chunk
    chunk_total = chunk.groupby("department", observed=True)["monthly_income"].sum()
    for department, income in chunk_total.items():
        income_by_department[department] = income_by_department.get(department, 0) + income

print(total_rows)
print(income_by_department)
```
**Output:**
```
12
{'HR': 146000, 'IT': 142000, 'Sales': 138000}
```
**What it means:** the whole file was processed three chunks at a time, never fully in memory, and we still got totals per department.
**Likely follow-ups:**
- *Median per department?* Does not combine across chunks; use a sample or a database.
- *When do you stop using pandas?* Files far beyond memory: SQL, Parquet, or tools like Dask.
**Common mistakes:** loading everything then dropping columns, appending every chunk to a list (memory is used anyway), averaging chunk averages (wrong when chunks differ in size).

### Q46 ⭐⭐ 🔴 After your EDA shows that overtime and low income are linked to attrition, what are the limits of this conclusion, and how do you explain correlation versus causation to HR?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Honest, careful interpretation, and plain-language communication with non-technical stakeholders.
**Say this in the interview:** "It shows an association, not proof of cause. People who work overtime may leave for a different reason, such as a bad manager, and low income may just reflect junior roles. I would call it a lead to test, not a cause to act on blindly."
**Explain simply:**
- **Correlation:** two things move together. **Causation:** one makes the other happen.
- **Confounders:** hidden third factors, e.g. junior staff both earn less and leave more; seniority explains both.
- **Reverse direction:** the cause may run the other way; staff already planning to leave may have been passed over for raises, so low income follows the decision to leave.
- **Data limits:** one snapshot, survivors only, small groups, self-reported satisfaction.
- **Plain example for HR:** "Ice cream sales and sunburn rise together, but ice cream does not cause sunburn; summer does."
- **What to do:** compare like with like (overtime vs non-overtime within the same job level), then test a small pilot such as capping overtime in one team.
**What it means:** I tell HR the data points to where to look, not what to blame, and I propose a small test before any big policy change.
**Likely follow-ups:**
- *How would you prove causation?* An experiment (pilot vs control group) is the strongest evidence.
- *What do you tell HR to do now?* Low-cost actions: review overtime load and pay bands, then measure again.
**Common mistakes:** saying "overtime causes attrition", presenting percentages without group sizes, hiding the limits to sound confident.

### Q47 ⭐ 🟢 How do you read only selected columns and rows of a large CSV file to start EDA quickly?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the read_csv options that save time and memory.
**Say this in the interview:** "`usecols` for columns, `nrows` for the first rows, `skiprows` to jump ahead, and `chunksize` if I need to process everything in pieces."
**Explain simply:**
- **`usecols=[...]`:** only these columns are read.
- **`nrows=N`:** stops after N data rows; ideal for a first look at a huge file.
- **`skiprows`:** skips rows; keep row 0 (the header) by skipping from 1 onward.
- Looking at the first rows is not a random sample, so confirm with the full data before concluding.
**Sample data:** `employees.csv` with employee_id, department, age, monthly_income, notes and 12 rows.
**Code (what you write in the interview):**
```python
import pandas as pd

# Only 3 columns and only the first 5 rows
sample = pd.read_csv("employees.csv", usecols=["employee_id", "department", "monthly_income"], nrows=5)
print(sample)

# Skip the first 5 data rows, read the next 3 (keep the header)
middle = pd.read_csv("employees.csv", usecols=["employee_id", "department"], skiprows=range(1, 6), nrows=3)
print(middle)
```
**Output:**
```
   employee_id department  monthly_income
0            1      Sales           30000
1            2         IT           31000
2            3         HR           32000
3            4      Sales           33000
4            5         IT           34000
   employee_id department
0            6         HR
1            7      Sales
2            8         IT
```
**What it means:** you get a quick, light preview without loading the whole file.
**Likely follow-ups:**
- *Whole file in pieces?* `chunksize` (see Q45).
- *Speed up types?* Pass `dtype`.
**Common mistakes:** `skiprows=5` (removes the header too), mistyped column names in `usecols`, treating the first rows as representative.

### Q48 ⭐ 🟡 Write code to export your cleaned DataFrame and a summary table to one Excel file with two sheets.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you hand results to non-coders in the format they use, with `ExcelWriter`.
**Say this in the interview:** "I open one `ExcelWriter` and write each DataFrame to its own sheet, with `index=False` so no extra index column appears."
**Explain simply:**
- **ExcelWriter:** keeps one workbook open so several sheets go into the same file.
- **`sheet_name`:** the tab name.
- **`index=False`:** leaves out pandas' row numbers.
- Needs the `openpyxl` package installed.
- Calling `to_excel("file.xlsx")` twice would overwrite the file, that is why we use one writer.
**Sample data:** 5 cleaned employee rows; summary is count and average income per department.
**Code (what you write in the interview):**
```python
import pandas as pd

cleaned_employees = pd.DataFrame({
    "department": ["Sales","Sales","IT","IT","HR"],
    "monthly_income": [30000, 42000, 60000, 65000, 35000],
})

department_summary = cleaned_employees.groupby("department")["monthly_income"].agg(["count", "mean"]).reset_index()

# One workbook, two sheets (needs the openpyxl package)
with pd.ExcelWriter("hr_report.xlsx") as writer:
    cleaned_employees.to_excel(writer, sheet_name="Cleaned data", index=False)
    department_summary.to_excel(writer, sheet_name="Summary", index=False)
```
**Output:** no printed output; the file `hr_report.xlsx` is created with the sheets `['Cleaned data', 'Summary']`. The Summary sheet holds:
```
  department  count   mean
0         HR      1  35000
1         IT      2  62500
2      Sales      2  36000
```
**What it means:** a stakeholder opens one Excel file and finds the data on one tab and the summary on another.
**Likely follow-ups:**
- *Formatting?* Use openpyxl or xlsxwriter after writing for column widths.
- *CSV instead?* One file per table, no sheets.
**Common mistakes:** writing twice to the same filename (second overwrites first), leaving the index column in, missing `openpyxl`.

### Q49 ⭐ 🟡 How do you make your EDA notebook reproducible and easy for a reviewer to follow in a take-home assignment (structure, comments, markdown, random seed, order of cells)?
**Asked at:** commonly asked (no company-specific report found); take-homes are reported in analyst hiring (snippet-level only).
**What the interviewer is checking:** Professional habits: can someone else rerun your work and get the same answer.
**Say this in the interview:** "Clear sections, markdown that states the question and the finding, cells that run top to bottom from a fresh restart, a fixed random seed, and the data path and assumptions written at the top."
**Explain simply:**
- **Reproducible:** a stranger runs it from the top and gets the same numbers.
- **Structure:** 1) question and summary, 2) load and check data, 3) cleaning, 4) analysis, 5) findings and next steps.
- **Markdown cells:** one sentence per section saying what and why; end each chart with "what this shows".
- **Random seed:** any sampling or model uses a fixed seed (for example `random_state=42`) so results do not change.
- **Order:** use "Restart and run all" before sending; no cell should depend on one lower down.
- **Housekeeping:** relative file paths, list libraries, state cleaning decisions (rows dropped and why), no leftover debug cells.
**What it means:** the reviewer should be able to rerun the notebook once, get your numbers, and follow your reasoning without asking you anything.
**Likely follow-ups:**
- *Notebook or script?* Notebook for narrative, script for repeated pipelines.
- *Version control?* Keep the data file and notebook together with a README.
**Common mistakes:** cells run out of order, hard-coded local paths, no explanation for dropped rows, 40 charts with no story.

### Q50 ⭐ 🟡 Which pandas profiling or auto-EDA tools do you know, and why should you still do manual EDA in an interview?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of tools, plus judgment that tools do not replace thinking.
**Say this in the interview:** "I know ydata-profiling (formerly pandas-profiling), sweetviz and D-Tale; they give a quick overview, but I still do manual EDA because the tool does not know the business question or the data quirks."
**Explain simply:**
- **ydata-profiling:** one command makes an HTML report of missing values, distributions and correlations.
- **sweetviz:** compares two datasets (for example leavers versus stayers). **D-Tale:** an interactive table in the browser. (Names from memory, not run here.)
- **Why still manual:** the tool will not say that salary of 0 is an error, that "P" and "Present" are the same, or which metric answers the business question.
- **In an interview:** installing packages or internet access may not be allowed, and the interviewer wants to see your thinking.
- **Best use:** run an auto report to scan quickly, then do targeted manual checks.
**What it means:** auto-EDA tools save time on the first scan, but the judgment about what is wrong and what matters is still mine.
**Likely follow-ups:**
- *Downsides?* Slow on big data, heavy output, no business context.
- *Would you use it at work?* Yes for first scan, then verify the findings by hand.
**Common mistakes:** naming the tool but not its limits, pasting the report as the final analysis, using the old name only.

### Q51 ⭐ 🟡 In a take-home EDA assignment given 48 hours, how do you decide what to include in your final report, and what do you leave out?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Prioritising, storytelling and focus on what the business asked.
**Say this in the interview:** "I start from the question, keep only findings that answer it or change a decision, and move everything else to an appendix."
**Explain simply:**
- **Start:** restate the question and who will read the report (usually a manager, not a coder).
- **Include:** a short summary at the top, the 3 to 5 strongest findings with one clear chart each, data issues that affect the result (missing values, outliers), assumptions, and recommendations with next steps.
- **Leave out or move to an appendix:** dead ends, every chart you tried, long code output, raw describe tables.
- **Be honest:** state limits (small groups, correlation not causation).
- **Time plan:** about 20% understanding the data, 40% cleaning and analysis, 20% writing and charts, 20% review and rerun.
**What it means:** a good report is short, answers the question first and shows its limits; it is judged on focus, not on how much was tried.
**Likely follow-ups:**
- *What if you find something unexpected?* Include it if relevant, with a caution.
- *How long should the report be?* A page or two plus the notebook.
**Common mistakes:** showing everything you tried, no recommendation, not checking that the notebook reruns, ignoring the actual question.

### Q52 ⭐ 🔴 Write code to create a simple attrition risk score from three rules (overtime, low satisfaction, short tenure) and check how well it separates leavers from stayers.
**Asked at:** commonly asked (no company-specific report found); a gap-fill composite question.
**What the interviewer is checking:** Rule-based scoring and a simple check that higher scores mean higher attrition.
**Say this in the interview:** "One point per rule, add them for a score of 0 to 3, then group by score and see whether the attrition rate rises with the score."
**Explain simply:**
- **Risk score:** a simple count of risk signs; easy to explain to HR.
- **Rules here:** overtime is Yes; satisfaction 2 or below; tenure under 2 years.
- **`astype(int)`:** turns True/False into 1/0 so they can be added.
- **Check:** if the rate climbs from score 0 to 3, the score separates leavers from stayers.
- This only describes the same data you built the rules on; test on new data before trusting it.
**Sample data:** 10 employees with overtime, satisfaction, tenure_years and attrition.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "overtime": ["Yes","Yes","No","Yes","No","No","Yes","No","No","Yes"],
    "satisfaction": [1, 2, 4, 1, 3, 4, 3, 2, 4, 2],
    "tenure_years": [1, 2, 6, 1, 4, 8, 5, 3, 7, 1],
    "attrition": ["Yes","Yes","No","Yes","No","No","No","Yes","No","Yes"],
})

# One point for each risk rule that is true
employees["risk_score"] = (
    (employees["overtime"] == "Yes").astype(int)
    + (employees["satisfaction"] <= 2).astype(int)
    + (employees["tenure_years"] < 2).astype(int)
)

# Attrition rate and headcount at each score: it should rise with the score
employees["left"] = (employees["attrition"] == "Yes").astype(int)
print(employees.groupby("risk_score")["left"].agg(headcount="count", attrition_rate="mean"))
```
**Output:**
```
            headcount  attrition_rate
risk_score                           
0                   4             0.0
1                   2             0.5
2                   1             1.0
3                   3             1.0
```
**What it means:** nobody with score 0 left, everyone with score 2 or 3 left, so the score separates the two groups well (on this tiny sample, so treat it as a demo).
**Likely follow-ups:**
- *How to improve?* Weight the rules, or use logistic regression.
- *How to validate?* Hold out data or use a later period.
**Common mistakes:** judging on tiny groups, thresholds chosen after seeing the results, treating the score as proof of cause.

### Q53 ⭐ 🔴 Write a function that takes any DataFrame and a target column and returns the target's rate for each categorical column, so you can scan for drivers quickly.
**Asked at:** commonly asked (no company-specific report found); a gap-fill composite question.
**What the interviewer is checking:** Can you wrap a repeated groupby in a reusable loop.
**Say this in the interview:** "I turn the target into 1/0, loop over the text columns, and for each show headcount and the target rate per category, sorted high to low."
**Explain simply:**
- **Target:** the outcome you care about, here attrition Yes/No.
- **Rate:** the average of the 1/0 column, i.e. the percentage of Yes.
- **`select_dtypes`:** picks only text/category columns.
- **Headcount beside the rate:** a 100% rate on 1 person means nothing.
**Sample data:** 6 employees with department, overtime and attrition.
**Code (what you write in the interview):**
```python
import pandas as pd

def target_rate_by_category(df, target_column):
    # Treat Yes as 1 and everything else as 0
    target = (df[target_column] == "Yes").astype(int)
    for column in df.select_dtypes(include=["object", "category", "string"]).columns:
        if column == target_column:
            continue
        summary = target.groupby(df[column]).agg(headcount="count", rate="mean")
        print(column)
        print(summary.sort_values("rate", ascending=False), "\n")

employees = pd.DataFrame({
    "department": ["Sales","Sales","IT","IT","HR","HR"],
    "overtime": ["Yes","Yes","No","Yes","No","No"],
    "attrition": ["Yes","No","No","Yes","No","No"],
})
target_rate_by_category(employees, "attrition")
```
**Output:**
```
department
            headcount  rate
department                 
IT                  2   0.5
Sales               2   0.5
HR                  2   0.0 

overtime
          headcount      rate
overtime                     
Yes               3  0.666667
No                3  0.000000 

```
**What it means:** overtime shows the biggest gap (67% versus 0%), a lead to look at first; department splits less.
**Likely follow-ups:**
- *Numeric columns?* Bin them with `pd.cut` first.
- *High-cardinality columns like ID?* Skip them (many categories of 1 row).
**Common mistakes:** including the target itself in the loop, forgetting that string columns may be `str` dtype in newer pandas (the list above covers it), reading rate without headcount.

### Q54 ⭐ 🔴 A stakeholder asks: 'Is attrition higher in Hyderabad than Bengaluru?' How do you check this in pandas, and how do you avoid overclaiming when one city has very few employees?
**Asked at:** commonly asked (no company-specific report found); a gap-fill composite question.
**What the interviewer is checking:** Group comparison plus statistical caution about small samples.
**Say this in the interview:** "I show attrition rate with headcount and number of leavers for both cities. If one city is small, I say the difference could be chance and avoid a firm claim."
**Explain simply:**
- **Compare rates, not counts,** and always show headcount and leavers beside the rate.
- **Small sample:** one extra leaver in 4 people moves the rate by 25 points, so the number is unstable.
- **How to avoid overclaiming:** say "higher in the data, but based on only 4 people"; give the counts; if needed use a confidence interval or a Fisher exact test (a test of whether a gap between two small groups could just be chance), or wait for more data or more months.
- **Other fixes:** compare over a longer period, or combine similar small locations.
**Sample data:** 4 Hyderabad employees (1 left) and 12 Bengaluru employees (2 left).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "city": ["Hyderabad"]*4 + ["Bengaluru"]*12,
    "attrition": ["Yes","No","No","No"] + ["Yes"]*2 + ["No"]*10,
})
employees["left"] = (employees["attrition"] == "Yes").astype(int)

# Headcount, leavers and attrition rate (%) for each city
by_city = employees.groupby("city")["left"].agg(headcount="count", leavers="sum", attrition_rate="mean")
by_city["attrition_rate"] = (by_city["attrition_rate"] * 100).round(1)
print(by_city)
```
**Output:**
```
           headcount  leavers  attrition_rate
city                                         
Bengaluru         12        2            16.7
Hyderabad          4        1            25.0
```
**What it means:** Hyderabad looks higher (25% versus 16.7%), but that is one person versus two; I would answer "slightly higher, not reliable yet".
**Likely follow-ups:**
- *Which test?* Fisher exact test for small counts, chi-square for larger ones.
- *Would you report it?* Yes, with the counts and a clear warning.
**Common mistakes:** saying "Hyderabad is worse" from 1 leaver, showing only percentages, comparing counts (Bengaluru has more leavers just because it is bigger).

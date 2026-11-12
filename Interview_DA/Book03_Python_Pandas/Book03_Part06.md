# Book 3 — Python & pandas for Analysts | Part 6: Data Cleaning: Missing Values, Duplicates, Types, Outliers 🟡

**Target:** 60 questions | **Actual:** 63 questions
**Scope:** pandas data cleaning for analysts: missing values, duplicates, data types, text and date fixes, outliers, SettingWithCopyWarning and common errors.

### Q1 ⭐⭐⭐ 🟢 How do you check for missing values in a pandas DataFrame and count them per column?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the first health check on any dataset, and can you chain two simple methods?
**Say this in the interview:** "I use `isna()` to mark every empty cell as True, then `sum()` to count the Trues in each column. That tells me which columns have gaps before I touch anything."
**Explain simply:**
- A **DataFrame** is a table; a **missing value** is an empty cell, shown as `NaN` ("not a number", pandas' marker for empty).
- `isna()` gives a same-shaped table of True/False. True means missing.
- `sum()` treats True as 1, so it counts the gaps in each column.
- Use `.isna().sum().sum()` for the grand total.

**Sample data:** 4 employees; one department and two salaries are missing.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "department": ["HR", "IT", None, "HR"],
    "salary": [45000, None, 52000, None],
})

# True where a cell is empty, then add up the Trues per column
print(employees.isna().sum())
```
**Output:**
```
name          0
department    1
salary        2
dtype: int64
```
**What it means:** Salary has 2 gaps, department has 1, name is complete. I would look at salary first.
**Likely follow-ups:**
- *How do you see this as a percentage?* `employees.isna().mean() * 100`.
- *Does a blank text like "" count?* No, `isna()` ignores empty strings (see Q16).

**Common mistakes:** Using `df.count()` and forgetting it counts the non-missing cells; looking only at `head()` and missing gaps further down.

### Q2 ⭐⭐⭐ 🟢 What is the difference between isna() and isnull() in pandas?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** A quick "do you know the library" trivia check.
**Say this in the interview:** "There is no difference. `isnull()` is just another name for `isna()`. I use `isna()` because it matches `dropna()` and `fillna()`."
**Explain simply:**
- Both return True for missing cells (`NaN`, `None`, `NaT` for missing dates).
- The two names exist because pandas was copied in style from R, where it is `is.na`, and from SQL, where it is `IS NULL`.
- The opposites are `notna()` and `notnull()`.

**Sample data:** 2 employees, one salary missing.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"name": ["Asha", "Ravi"], "salary": [45000, None]})

# Both give the same answer
print(employees.isna())
print(employees.isnull())
print(employees.isna().equals(employees.isnull()))
```
**Output:**
```
    name  salary
0  False   False
1  False    True
    name  salary
0  False   False
1  False    True
True
```
**What it means:** The two tables are identical, so pick one name and stay consistent.
**Likely follow-ups:**
- *Which should I use?* Either; `isna()` is the one I see most.

**Common mistakes:** Thinking `isnull()` also catches empty strings or zeros. It does not.

### Q3 ⭐⭐⭐ 🟢 How do you remove duplicate rows in pandas?
**Asked at:** commonly asked (no company-specific report found; drop_duplicates appears in most pandas question lists)
**What the interviewer is checking:** Do you know `drop_duplicates()` and that it returns a new table.
**Say this in the interview:** "I call `drop_duplicates()`. By default it compares every column and keeps the first copy of each row. It returns a cleaned copy, so I save it in a new variable."
**Explain simply:**
- A **duplicate** is a row identical to an earlier one in every column.
- The original table is not changed unless you assign the result back.
- To judge duplicates on only some columns, use `subset` (see Q9).

**Sample data:** Ravi appears twice, exactly the same.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [101, 102, 102, 103],
    "name": ["Asha", "Ravi", "Ravi", "Meena"],
    "department": ["HR", "IT", "IT", "Finance"],
})

# Keep the first copy of every fully identical row
employees_clean = employees.drop_duplicates()
print(employees_clean)
```
**Output:**
```
   employee_id   name department
0          101   Asha         HR
1          102   Ravi         IT
3          103  Meena    Finance
```
**What it means:** The second Ravi row (index 2) is gone. The index keeps its old numbers; use `reset_index(drop=True)` if you want 0, 1, 2.
**Likely follow-ups:**
- *Does it change the original?* No, unless you assign it back.
- *What if only the ID repeats?* Use `subset="employee_id"`.

**Common mistakes:** Calling `drop_duplicates()` and not saving the result, so nothing seems to happen. Also missing near-duplicates like "Ravi" vs "Ravi " (trailing space).

### Q4 ⭐⭐⭐ 🟢 How do you find duplicate rows in a DataFrame without deleting them?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you look before you delete?
**Say this in the interview:** "I use `duplicated()`, which gives True for each repeated row, and filter the table with it. I inspect first so I know what I would be deleting."
**Explain simply:**
- `duplicated()` marks a row True if an identical row appeared earlier.
- The first copy is marked False by default, so it is not shown.
- `sum()` on the result counts the repeats.

**Sample data:** Same 4 rows as Q3.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [101, 102, 102, 103],
    "name": ["Asha", "Ravi", "Ravi", "Meena"],
    "department": ["HR", "IT", "IT", "Finance"],
})

# True for every repeat after the first copy
is_repeat = employees.duplicated()
print(employees[is_repeat])
print("Number of duplicate rows:", is_repeat.sum())
```
**Output:**
```
   employee_id  name department
2          102  Ravi         IT
Number of duplicate rows: 1
```
**What it means:** One repeated row exists. To see both copies, use `keep=False` (Q31).
**Likely follow-ups:**
- *How do you check only some columns?* `duplicated(subset=["employee_id"])`.

**Common mistakes:** Expecting both copies to show. Only the later copy is flagged by default.

### Q5 ⭐⭐⭐ 🟢 What does df.info() tell you, and why is it usually the first step in data cleaning?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you diagnose before you fix?
**Say this in the interview:** "`info()` shows the row count, each column's data type and how many non-empty values it has. In one glance I see missing values and wrong types, like dates stored as text."
**Explain simply:**
- **Non-Null Count** lower than the row count means that column has gaps.
- **Dtype** (data type) shows whether a column is number (`int64`, `float64`) or text (`str`; older pandas shows `object`).
- A date column showing as text means I must convert it before any date maths.
- It also shows memory used.

**Sample data:** 4 employees, one salary and one join date missing, join date stored as text.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": [45000, None, 52000, 48000],
    "join_date": ["2022-01-10", "2021-06-01", None, "2023-03-15"],
})

employees.info()
```
**Output:**
```
<class 'pandas.DataFrame'>
RangeIndex: 4 entries, 0 to 3
Data columns (total 3 columns):
 #   Column     Non-Null Count  Dtype  
---  ------     --------------  -----  
 0   name       4 non-null      str    
 1   salary     3 non-null      float64
 2   join_date  3 non-null      str    
dtypes: float64(1), str(2)
memory usage: 228.0 bytes
```
**What it means:** Salary and join_date each have one gap, and join_date is text, so I need `pd.to_datetime()`. (Output shown from pandas 3.0.5; older versions print `DataFrame` as `pandas.core.frame.DataFrame` and `object` for text.)
**Likely follow-ups:**
- *What comes after info()?* `describe()` for number ranges, then `isna().sum()` and `duplicated().sum()`.

**Common mistakes:** Trusting that a column that "looks numeric" is numeric. Salary like "45,000" is text.

### Q6 ⭐⭐⭐ 🟢 How do you check the data type of each column, and how do you change a column's type with astype()?
**Asked at:** commonly asked (no company-specific report found; astype vs to_numeric appears in pandas question lists)
**What the interviewer is checking:** Basic type handling.
**Say this in the interview:** "`df.dtypes` lists each column's type. `astype()` converts a column to a new type, for example employee ID from text to a whole number. It raises an error if a value cannot convert."
**Explain simply:**
- **Data type** = what kind of thing a column holds: whole number (`int`), decimal (`float`), text (`str`), date (`datetime64`), category.
- `astype(int)`, `astype(float)`, `astype(str)`, `astype("category")` are the common ones.
- Assign the result back, as `astype` returns a new column.

**Sample data:** employee_id stored as text.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena"],
    "employee_id": ["101", "102", "103"],
    "salary": [45000, 38000, 52000],
})

# Data type of each column
print(employees.dtypes)

# Change employee_id from text to whole number
employees["employee_id"] = employees["employee_id"].astype(int)
print(employees.dtypes)
```
**Output:**
```
name             str
employee_id      str
salary         int64
dtype: object
name             str
employee_id    int64
salary         int64
dtype: object
```
**What it means:** employee_id is now a number. (Older pandas prints `object` where this shows `str`.)
**Likely follow-ups:**
- *What if one value is "N/A"?* `astype(int)` fails; use `pd.to_numeric(errors="coerce")` (Q10, Q24).

**Common mistakes:** Forgetting to assign back; converting dirty text with `astype` and getting a ValueError.

### Q7 ⭐⭐⭐ 🟢 What is the difference between dropna() and fillna(), and when would you use each?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you choose between removing and filling, not just name the methods.
**Say this in the interview:** "`dropna()` removes rows with gaps, `fillna()` replaces gaps with a value. I drop when few rows are affected or the field is essential; I fill when losing rows would hurt, using a sensible value."
**Explain simply:**
- `dropna()` loses data (whole rows) but never invents any.
- `fillna()` keeps rows but adds assumptions.
- A row missing the key field (say employee ID) is usually dropped; a missing rating may be filled or flagged.
- By default `dropna()` drops a row if any column is empty.

**Sample data:** Ravi has no salary; Meena and John have no rating.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": [45000, None, 52000, 48000],
    "rating": [4, 3, None, None],
})

# dropna removes the rows that have a gap
print(employees.dropna())

# fillna puts a value into the gaps
print(employees.fillna({"rating": 0}))
```
**Output:**
```
   name   salary  rating
0  Asha  45000.0     4.0
    name   salary  rating
0   Asha  45000.0     4.0
1   Ravi      NaN     3.0
2  Meena  52000.0     0.0
3   John  48000.0     0.0
```
**What it means:** `dropna()` left only 1 of 4 rows, which shows how costly it can be. `fillna` kept all rows, but filling rating with 0 is questionable (a 0 looks like a real bad score).
**Likely follow-ups:**
- *Which columns does dropna check?* All, unless you pass `subset=` (Q17).

**Common mistakes:** Running `dropna()` on a wide table and losing almost every row; filling with 0 when 0 has a real meaning.

### Q8 ⭐⭐⭐ 🟡 How do you handle missing values in a salary column: when do you fill with the mean, the median or a constant, and how do you do it in pandas?
**Asked at:** commonly asked; one 2024 Tiger Analytics candidate report mentions mean imputation (snippet only, unverified).
**What the interviewer is checking:** Do you pick the fill value for a reason, especially skewed salaries?
**Say this in the interview:** "Salaries are usually skewed by a few very high pay packages, so I fill with the median. Mean is fine for evenly spread data, and a constant like 0 or 'Unknown' only when it truly means 'none'."
**Explain simply:**
- **Mean** = average; one huge salary drags it up.
- **Median** = middle value; barely moves for extreme values.
- **Constant** = a fixed value you choose; good for categories ("Unknown"), risky for numbers.
- Even better when possible: fill with the department median (Q29).

**Sample data:** Priya earns 400,000, far above the others; Ravi's salary is missing.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "salary": [45000, None, 52000, 48000, 400000],
})

# Median is safe when a few very high salaries exist
median_salary = employees["salary"].median()
employees["salary"] = employees["salary"].fillna(median_salary)
print(employees)
```
**Output:**
```
    name    salary
0   Asha   45000.0
1   Ravi   50000.0
2  Meena   52000.0
3   John   48000.0
4  Priya  400000.0
```
**What it means:** Ravi gets 50,000, a believable salary. The mean would have given 136,250, which is wrong for almost everyone.
**Likely follow-ups:**
- *Does filling change the average?* The mean stays the same with mean-fill, but spread shrinks; say so to the stakeholder.

**Common mistakes:** Filling salary with 0 (drags down averages and payroll totals); using the mean on skewed data.

### Q9 ⭐⭐⭐ 🟡 How does drop_duplicates() decide which row to keep, and how do you use the subset and keep arguments?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand which row survives and how to define "duplicate".
**Say this in the interview:** "`subset` says which columns decide a duplicate; `keep` says which copy survives: first (default), last, or False to drop all copies. Pandas just uses row order, so I sort first if 'latest' matters."
**Explain simply:**
- `subset="employee_id"`: two rows are duplicates if the ID matches, even if other columns differ.
- `keep="first"`: keep the topmost; `keep="last"`: keep the bottommost; `keep=False`: remove every row that has a repeat.
- It does not know which row is "better"; it only looks at position.

**Sample data:** Employee 102 appears twice with different departments.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [101, 102, 102, 103],
    "department": ["HR", "IT", "Finance", "HR"],
    "salary": [45000, 38000, 41000, 52000],
})

# Same employee_id counts as a duplicate; keep the last row
print(employees.drop_duplicates(subset="employee_id", keep="last"))

# keep=False drops every row that has a repeat
print(employees.drop_duplicates(subset="employee_id", keep=False))
```
**Output:**
```
   employee_id department  salary
0          101         HR   45000
2          102    Finance   41000
3          103         HR   52000
   employee_id department  salary
0          101         HR   45000
3          103         HR   52000
```
**What it means:** With `keep="last"` the Finance row survives; with `keep=False` employee 102 vanishes entirely.
**Likely follow-ups:**
- *How do you keep the most recent record?* Sort by date, then `keep="last"` (Q12).

**Common mistakes:** Assuming pandas keeps the "best" or newest row; forgetting to sort first.

### Q10 ⭐⭐⭐ 🟡 A column holding numbers is stored as text because of values like 'N/A' or '12,500'. How do you convert it to numeric safely using pd.to_numeric()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you clean text first and convert without crashing.
**Say this in the interview:** "I remove the commas with `str.replace`, then use `pd.to_numeric(errors='coerce')`. Coerce turns anything that cannot be a number, like 'N/A', into NaN instead of raising an error."
**Explain simply:**
- `to_numeric` converts text to numbers.
- Default `errors="raise"` stops at the first bad value; `errors="coerce"` swaps it for `NaN`.
- Commas must be removed first, otherwise "12,500" also becomes NaN.
- Afterward, count the NaNs to see how many values were unreadable.

**Sample data:** Salary stored as text including "12,500" and "N/A".
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": ["45000", "12,500", "N/A", "48000"],
})

# Remove commas first, then convert; anything unreadable becomes NaN
employees["salary"] = employees["salary"].str.replace(",", "")
employees["salary"] = pd.to_numeric(employees["salary"], errors="coerce")
print(employees)
print(employees["salary"].dtype)
```
**Output:**
```
    name   salary
0   Asha  45000.0
1   Ravi  12500.0
2  Meena      NaN
3   John  48000.0
float64
```
**What it means:** "12,500" became 12500 and "N/A" became a missing value, ready for filling or dropping.
**Likely follow-ups:**
- *Why float and not int?* NaN cannot live in a normal int column.

**Common mistakes:** Skipping the comma removal, so valid salaries silently become NaN; using coerce without checking how many values it wiped out.

### Q11 ⭐⭐⭐ 🟡 How do you detect outliers in a salary column using the IQR method in pandas?
**Asked at:** a candidate-reported Glassdoor question asks to write an IQR outlier function (snippet only; company not confirmed); commonly asked.
**What the interviewer is checking:** Can you code the IQR rule and explain the 1.5 multiplier.
**Say this in the interview:** "I find the 25th and 75th percentiles, take the gap between them (the IQR), and flag anything below Q1 minus 1.5 times IQR or above Q3 plus 1.5 times IQR."
**Explain simply:**
- **Percentile**: value below which that share of data falls. Q1 = 25th, Q3 = 75th.
- **IQR** (interquartile range) = Q3 minus Q1, the spread of the middle half of salaries.
- The "fences" are lower and upper limits; points outside are **outliers** (unusually extreme values).
- 1.5 is a convention, not a law.

**Sample data:** Kiran earns 400,000, far above the rest.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya", "Kiran"],
    "salary": [45000, 38000, 52000, 48000, 41000, 400000],
})

# Q1 and Q3 are the 25th and 75th percentiles
q1 = employees["salary"].quantile(0.25)
q3 = employees["salary"].quantile(0.75)
iqr = q3 - q1

# Anything beyond 1.5 x IQR from the box is an outlier
lower_limit = q1 - 1.5 * iqr
upper_limit = q3 + 1.5 * iqr

outliers = employees[(employees["salary"] < lower_limit) | (employees["salary"] > upper_limit)]
print(lower_limit, upper_limit)
print(outliers)
```
**Output:**
```
28500.0 64500.0
    name  salary
5  Kiran  400000
```
**What it means:** Salaries outside 28,500 to 64,500 are flagged; only Kiran. Flagged does not mean wrong: he may be a real senior leader, so check before removing.
**Likely follow-ups:**
- *When is IQR better than z-score?* On skewed data or small samples, since it does not depend on the mean (Q33).

**Common mistakes:** Deleting outliers automatically; forgetting `|` (or) and using `and`; missing parentheses around each condition.

### Q12 ⭐⭐⭐ 🟡 You have an employee table with repeated Employee IDs. Write code to keep only the most recent record per employee.
**Asked at:** commonly asked; a keep-latest-record task appears in training-blog snippets (unverified).
**What the interviewer is checking:** Do you sort before dropping duplicates.
**Say this in the interview:** "I make sure the date column is a real date, sort oldest to newest, then `drop_duplicates` on employee ID with `keep='last'`, so the newest row stays."
**Explain simply:**
- `drop_duplicates` keeps by position, not by date, so sorting first decides the winner.
- Text dates can sort wrongly ("10-02" before "9-01"), so convert with `to_datetime` first.
- Ascending sort plus `keep="last"` keeps the latest.

**Sample data:** Employees 101 and 102 each have two records.
**Code (what you write in the interview):**
```python
import pandas as pd

records = pd.DataFrame({
    "employee_id": [101, 102, 101, 103, 102],
    "department": ["HR", "IT", "Finance", "HR", "IT"],
    "updated_on": ["2023-01-01", "2023-02-10", "2024-05-01", "2023-07-15", "2022-11-20"],
})

# Make sure dates are real dates, oldest first
records["updated_on"] = pd.to_datetime(records["updated_on"])
records = records.sort_values("updated_on")

# For each employee keep the last (most recent) row
latest_records = records.drop_duplicates(subset="employee_id", keep="last")
print(latest_records)
```
**Output:**
```
   employee_id department updated_on
1          102         IT 2023-02-10
3          103         HR 2023-07-15
2          101    Finance 2024-05-01
```
**What it means:** One row per employee, each the most recent (101 is now in Finance).
**Alternative:** `records.sort_values("updated_on").groupby("employee_id").tail(1)` gives the same rows.
**Likely follow-ups:**
- *What if two records share the same date?* The tie follows row order; add a second sort column.

**Common mistakes:** Using `keep="first"` without sorting; sorting text dates; forgetting to assign the sorted table back.

### Q13 ⭐⭐⭐ 🟡 What are the steps you follow to clean a messy dataset in pandas before analysis?
**Asked at:** commonly asked (no company-specific report found; "diagnose before fix" is a theme in prep blogs)
**What the interviewer is checking:** Do you have a repeatable order of work, not random fixes.
**Say this in the interview:** "First inspect, then fix: look at the shape, types, missing values and duplicates; tidy names, text and types; remove duplicates; handle missing values and outliers; then check the result again and note every change."
**Explain simply:**
- 1. **Inspect**: `head()`, `info()`, `describe()`, `isna().sum()`.
- 2. **Standardise**: column names, spaces, capitals, date and number types.
- 3. **Duplicates**: find, then remove.
- 4. **Missing values**: drop, fill or flag, with a reason.
- 5. **Outliers and wrong values**: check, do not delete blindly.
- 6. **Validate and document**: re-check counts and keep a list of changes for stakeholders.

Order matters: fix text and types before duplicates (otherwise "HR " and "HR" look different).

**Sample data:** Messy names, spaces, mixed case, a comma number, an "N/A" and a duplicate.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "Employee ID": [101, 102, 102, 103],
    "Department": [" hr", "IT ", "IT ", "Hr"],
    "Salary": ["45,000", "38000", "38000", "N/A"],
})

# 1. Tidy the column names
employees.columns = employees.columns.str.lower().str.replace(" ", "_")

# 2. Fix text and number types
employees["department"] = employees["department"].str.strip().str.upper()
employees["salary"] = pd.to_numeric(employees["salary"].str.replace(",", ""), errors="coerce")

# 3. Remove duplicates, then deal with missing values
employees = employees.drop_duplicates()
employees["salary"] = employees["salary"].fillna(employees["salary"].median())
print(employees)
```
**Output:**
```
   employee_id department   salary
0          101         HR  45000.0
1          102         IT  38000.0
3          103         HR  41500.0
```
**What it means:** Clean names, consistent department, numeric salary, no repeats, and no gaps. I would still tell the team that one salary was estimated.
**Likely follow-ups:**
- *Why not drop duplicates first?* Messy text hides duplicates.

**Common mistakes:** Cleaning without looking first; filling gaps before fixing types; changing the data without recording what was done.

### Q14 ⭐⭐⭐ 🟡 What is the SettingWithCopyWarning, why does it appear, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand views vs copies and the safe way to assign.
**Say this in the interview:** "It warns that I may be changing a copy of the data rather than the original, usually after filtering and then assigning in a second step. I fix it with `.copy()` when I want a new table, or a single `.loc[rows, column] = value` when I want to change the original."
**Explain simply:**
- Filtering (`df[df.salary > 40000]`) may return a **view** (a window on the original) or a **copy** (separate data); pandas could not always tell, so it warned.
- **Chained assignment** = two steps in a row, like `df[mask]["col"] = x`. The change may land on a throwaway copy.
- Fix 1: `.copy()` after the filter. Fix 2: `df.loc[mask, "col"] = x`.
- Verified here with pandas 3.0.5: that warning no longer exists. Pandas 3 uses **Copy-on-Write** (every result behaves as its own copy), so filtered tables are always independent, and chained assignment on the original raises a `ChainedAssignmentError` warning and does nothing. Pandas 2.x and older still show `SettingWithCopyWarning`.

**Sample data:** 4 employees; we want a bonus column for those above 40,000.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": [45000, 38000, 52000, 48000],
})

# Risky: filter, then change the filtered piece
high_earners = employees[employees["salary"] > 40000]
high_earners["bonus"] = 5000

# Safe: take an explicit copy first
high_earners = employees[employees["salary"] > 40000].copy()
high_earners["bonus"] = 5000
print(high_earners)
```
**Output:**
```
    name  salary  bonus
0   Asha   45000   5000
2  Meena   52000   5000
3   John   48000   5000
```
**What it means:** The safe version is clear in every pandas version. (On pandas 2.x the "risky" lines print `SettingWithCopyWarning`; on 3.0.5 they ran silently, as checked.)
**Likely follow-ups:**
- *How do you update the original?* `employees.loc[employees["salary"] > 40000, "bonus"] = 5000`.

**Common mistakes:** Ignoring or silencing the warning; using chained `df[mask]["col"] = x` and expecting the original to change.

### Q15 ⭐⭐⭐ 🔴 How do you decide whether to drop, fill or flag missing values, and how do you explain the choice to a business stakeholder?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Judgement and communication, not syntax.
**Say this in the interview:** "First I ask why it is missing and how much is missing. If it is a small share and random, dropping is fine; if the field matters I fill with a reasoned value; and I flag filled values so nobody mistakes them for real data. Then I explain the choice and its impact in plain words."
**Explain simply:**
- **Why missing?** Never collected, not applicable (e.g. no exit date for current staff), data error, or people declined to answer? "Not applicable" is not a gap to fill.
- **How much?** A few percent: drop or fill. Over about 30 to 40 percent: question the column.
- **Drop** when the row is useless without the field (no employee ID).
- **Fill** when the field matters and a fair estimate exists (median salary by department).
- **Flag** by adding a True/False column, so the gap stays visible and analysts can test its effect.
- **Tell the stakeholder:** what you did, how many rows, and how it could change results. Example: "12 percent of ratings were missing; I filled them with the median and marked them; averages move by under 0.1."

**Sample data:** John and Ravi have no performance rating.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "rating": [4, None, 3, None],
})

# Flag first, so the gap is never hidden
employees["rating_missing"] = employees["rating"].isna()

# Then fill; analysts can still filter on the flag
employees["rating"] = employees["rating"].fillna(employees["rating"].median())
print(employees)
```
**Output:**
```
    name  rating  rating_missing
0   Asha     4.0           False
1   Ravi     3.5            True
2  Meena     3.0           False
3   John     3.5            True
```
**What it means:** Both the filled number and the honest "this was missing" marker are kept.
**Likely follow-ups:**
- *What if data is missing for a reason, such as unhappy employees skipping a survey?* Then filling hides a pattern; report the missingness itself as a finding.

**Common mistakes:** Always dropping or always filling without asking why; not telling stakeholders about the assumption; filling "not applicable" fields.

### Q16 ⭐⭐ 🟢 What is the difference between NaN, None and an empty string in pandas?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know which blanks pandas actually treats as missing.
**Say this in the interview:** "NaN and None both count as missing; pandas converts None to NaN in number columns. An empty string is a real piece of text of length zero, so pandas does not see it as missing, and I have to replace it myself."
**Explain simply:**
- **NaN** ("not a number"): the standard missing marker from numpy; it is a float.
- **None**: Python's "nothing"; pandas treats it as missing too.
- **"" (empty string)**: text with zero characters; counted by `isna()` as present, so it hides gaps.
- Related: `NaT` is missing for dates; `pd.NA` is the newer universal missing marker.
- Convert blanks: `df.replace("", np.nan)`, then the usual missing-value tools work.

**Sample data:** One text column with a real value, None, NaN and an empty string.
**Code (what you write in the interview):**
```python
import pandas as pd
import numpy as np

comments = pd.Series(["Good", None, np.nan, ""])

# Which cells does pandas treat as missing?
print(comments.isna())
```
**Output:**
```
0    False
1     True
2     True
3    False
dtype: bool
```
**What it means:** None and NaN are missing (True); the empty string at position 3 is not, so a missing-value count would undercount it.
**Likely follow-ups:**
- *How do you fix empty strings?* `comments.replace("", np.nan)`.
- *Is NaN equal to NaN?* No; `np.nan == np.nan` is False, so use `isna()`.

**Common mistakes:** Filtering with `df["col"] == None` (does not work); trusting `isna().sum()` on survey columns that contain blank strings or spaces.

### Q17 ⭐⭐ 🟢 How do you drop rows where a specific column is missing, using dropna(subset=...)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can remove rows based on one column only, not the whole row.
**Say this in the interview:** "dropna with subset lets me say which column must be filled. Rows where that column is empty are removed, and missing values in other columns do not matter."
**Explain simply:**
- `dropna()` removes rows that have missing values (NaN means 'not a number', pandas' marker for empty).
- Without `subset`, one empty cell anywhere in the row removes the whole row, which can throw away good data.
- `subset=["salary"]` checks only the salary column. You can pass several columns in the list.
- It returns a new table; the original is unchanged unless you save the result.
**Sample data:** Employee table where two salaries are missing. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104],
    "department": ["HR", "IT", "HR", "Sales"],
    "salary": [45000, None, 52000, None],
})

# Keep only rows where salary is present
employees_with_salary = employees.dropna(subset=["salary"])
print(employees_with_salary)
```
**Output:**
```text
   employee_id department   salary
0          101         HR  45000.0
2          103         HR  52000.0
```
**What it means:** Employees 102 and 104 had no salary, so those rows are gone. Salary became decimals (45000.0) because NaN forces a float column.
**Likely follow-ups:**
1. How do I change the original table? Assign it back: `employees = employees.dropna(subset=["salary"])`.
2. What if I need both salary and department filled? `subset=["salary", "department"]`; a row is dropped if either is missing.
**Common mistakes:** Calling `dropna()` with no subset and losing rows only because an unimportant column was empty. Forgetting to assign the result. Missing values written as text like 'N/A' are not NaN, so dropna will not see them.

### Q18 ⭐⭐ 🟢 How do you fill missing values with the previous or next value using ffill() and bfill()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know how to fill gaps in ordered data (dates, shifts) using neighbouring values.
**Say this in the interview:** "ffill carries the last known value down into the gaps, bfill pulls the next known value up. I use them when the data is in order, like attendance or status logs."
**Explain simply:**
- `ffill()` means forward fill: copy the last value downward into empty cells.
- `bfill()` means backward fill: copy the next value upward into empty cells.
- Only sensible when rows are in a meaningful order (sort by date first) and the value really stays the same until it changes.
- In pandas 3 the old `fillna(method="ffill")` form is removed (verified: use `.ffill()` directly).
**Sample data:** Shift of an employee, recorded only when it changes. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

attendance = pd.DataFrame({
    "date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
    "shift": ["Morning", None, None, "Night"],
})

# Carry the last known value forward
attendance["shift_ffill"] = attendance["shift"].ffill()

# Pull the next known value backward
attendance["shift_bfill"] = attendance["shift"].bfill()
print(attendance)
```
**Output:**
```text
         date    shift shift_ffill shift_bfill
0  2026-01-01  Morning     Morning     Morning
1  2026-01-02      NaN     Morning       Night
2  2026-01-03      NaN     Morning       Night
3  2026-01-04    Night       Night       Night
```
**What it means:** On 2 and 3 Jan, ffill says Morning (last known) and bfill says Night (next known). Which is right depends on the business rule.
**Likely follow-ups:**
1. How do I fill within each employee? `df.groupby("employee_id")["shift"].ffill()`, so values do not leak between people.
2. Can I limit how far it fills? Yes, `ffill(limit=1)` fills only one gap in a row.
**Common mistakes:** Using it on unsorted data, or across different employees. Using it for numbers like salary where carrying a value forward is a guess.

### Q19 ⭐⭐ 🟢 How do you rename columns in a DataFrame, and why clean column names (spaces, capitals) at the start?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you start analysis with tidy, predictable column names.
**Say this in the interview:** "I use rename for a specific column, and I clean all names at once with str.strip, lower and replace. Clean names mean no typing errors and I can use df.salary style access."
**Explain simply:**
- `rename(columns={old: new})` changes only the columns you list.
- `df.columns = df.columns.str...` cleans every name in one go.
- Spaces and capitals cause errors: `"Annual Salary "` with a hidden trailing space is hard to spot and fails to match.
- Lower case with underscores (`date_of_joining`) is easy to type and works with dot access and SQL-style tools.
**Sample data:** Messy column names, as they often arrive from an HRMS export. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "Employee ID": [101, 102],
    "Date Of Joining": ["2024-01-10", "2025-03-05"],
    "Annual Salary ": [45000, 52000],
})

# Clean every name at once: trim spaces, lower case, spaces to underscores
employees.columns = employees.columns.str.strip().str.lower().str.replace(" ", "_")

# Rename one column on purpose
employees = employees.rename(columns={"annual_salary": "salary"})
print(employees.columns.tolist())
```
**Output:**
```text
['employee_id', 'date_of_joining', 'salary']
```
**What it means:** All three names are now lower case with underscores, and the salary column has a short name.
**Likely follow-ups:**
1. Does rename change the original? No, it returns a new DataFrame unless you assign it back.
2. Can I rename with a function? Yes, `rename(columns=str.lower)`.
**Common mistakes:** Forgetting a trailing space in the name, writing `rename({...})` without `columns=`, and not assigning the result.

### Q20 ⭐⭐ 🟢 How do you remove leading and trailing spaces from a text column in pandas?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the most common text-cleaning step and the `.str` accessor.
**Say this in the interview:** "I use str.strip. It removes spaces at the start and end of every value. The .str part tells pandas to apply the text method to the whole column."
**Explain simply:**
- `.str` lets you use text methods on a whole column at once.
- `strip()` removes spaces at both ends; `lstrip()` only the left, `rstrip()` only the right.
- Hidden spaces make 'HR' and 'HR ' count as different values in groupby and merges.
- It does not touch spaces inside the text ('Asha  Rao' keeps both spaces).
**Sample data:** Names with stray spaces. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"name": ["  Asha ", "Ravi", " Meena  "]})

# Remove spaces at the start and end of every name
employees["name"] = employees["name"].str.strip()
print(employees["name"].tolist())
```
**Output:**
```text
['Asha', 'Ravi', 'Meena']
```
**What it means:** The three names are now clean with no leading or trailing spaces.
**Likely follow-ups:**
1. What about spaces inside the text? `str.replace("  ", " ")` or a regex `\s+` to one space.
2. What if the column has NaN? `.str.strip()` leaves NaN as NaN; no error.
**Common mistakes:** Calling `df["name"].strip()` without `.str`, or not assigning the result back.

### Q21 ⭐⭐ 🟢 How do you make text consistent in pandas, for example turning 'hr', 'HR ' and 'Hr' into 'HR'?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can standardise categories so groupby and counts are correct.
**Say this in the interview:** "I strip the spaces and then make the case the same with str.upper, so 'hr', 'HR ' and 'Hr' all become 'HR'. Then value_counts confirms there are no leftover variants."
**Explain simply:**
- Computers treat 'hr', 'HR' and 'HR ' as three different values.
- Chain `.str.strip()` then `.str.upper()` (or `.lower()`, or `.title()` for names).
- Check with `value_counts()` afterwards.
- Real spelling differences ('Human Resources' vs 'HR') need a replace or map (see Q23).
**Sample data:** Department column typed by different people. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"department": ["hr", "HR ", "Hr", "it", " IT"]})

# Trim spaces, then make everything upper case
employees["department"] = employees["department"].str.strip().str.upper()
print(employees["department"].value_counts())
```
**Output:**
```text
department
HR    3
IT    2
Name: count, dtype: int64
```
**What it means:** All variants collapsed into two clean departments: 3 in HR and 2 in IT.
**Likely follow-ups:**
1. When would I use title()? For names and cities, where 'asha rao' should look like 'Asha Rao'.
2. How do I fix 'H.R.'? Use `str.replace` or a mapping dictionary.
**Common mistakes:** Changing case but forgetting the trailing spaces. Not saving the cleaned column back.

### Q22 ⭐⭐ 🟢 How do you change a text column to datetime using pd.to_datetime()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can turn text dates into real dates, and know about format and day-first issues.
**Say this in the interview:** "I use pd.to_datetime and pass the format, so pandas does not guess whether 03-04 means March or April. After that I can use .dt to get year, month and tenure."
**Explain simply:**
- Dates read from CSV are text (type `object` or `str`); you cannot subtract or group by month until they are datetime.
- `format="%d-%m-%Y"` says day-month-year (`%d` day, `%m` month, `%Y` four-digit year).
- Without a format, '03-04-2025' can be read as 4 March or 3 April; Indian data is usually day first.
- Once converted, `.dt.year`, `.dt.month`, `.dt.day_name()` work.
- Bad values raise an error unless you use `errors="coerce"` (Q27).
**Sample data:** Joining dates stored as day-month-year text. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"joining_date": ["15-01-2024", "03-03-2025", "20-07-2023"]})

# Tell pandas the exact layout: day-month-year
employees["joining_date"] = pd.to_datetime(employees["joining_date"], format="%d-%m-%Y")

print(employees.dtypes)
print(employees["joining_date"].dt.year.tolist())
```
**Output:**
```text
joining_date    datetime64[us]
dtype: object
[2024, 2025, 2023]
```
**What it means:** The column is now a true date type, and we can pull out the year of joining.
**Likely follow-ups:**
1. What if the formats are mixed? Use `dayfirst=True` or convert in groups; check the NaT rows after `errors="coerce"`.
2. What type do I get? `datetime64`; in pandas 3 the unit shows as `us` (microseconds), verified here.
**Common mistakes:** Letting pandas guess the day and month order, and doing date maths on text columns.

### Q23 ⭐⭐ 🟢 How do you replace specific values in a column, for example 'Male' and 'M' to 'M', using replace() or map()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can standardise category labels and know how replace and map differ.
**Say this in the interview:** "replace changes only the values I list and leaves everything else alone. map needs every value in the dictionary, otherwise unlisted values become NaN. For cleaning I usually start with replace."
**Explain simply:**
- `replace({old: new})` is safe: anything not listed stays as it was.
- `map({old: new})` looks up every value; missing keys turn into NaN, which can silently erase data.
- Use `map` when you want a complete recoding and want unexpected values to stand out as NaN.
- After replacing, run `value_counts()` to confirm the labels.
**Sample data:** Gender column with mixed labels. The 'M' value is already correct. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"gender": ["Male", "M", "Female", "F", "Male"]})

# replace(): changes only the listed values, leaves the rest alone
employees["gender_replace"] = employees["gender"].replace({"Male": "M", "Female": "F"})

# map(): every value must be in the dictionary, otherwise it becomes NaN
employees["gender_map"] = employees["gender"].map({"Male": "M", "M": "M", "Female": "F", "F": "F"})
print(employees)
```
**Output:**
```text
   gender gender_replace gender_map
0    Male              M          M
1       M              M          M
2  Female              F          F
3       F              F          F
4    Male              M          M
```
**What it means:** Both methods give the same answer here because the dictionary for map covered every value.
**Likely follow-ups:**
1. What if I forget a key in map? That value becomes NaN; check with `isna().sum()`.
2. Can I keep unlisted values with map? Yes: `s.map(mapping).fillna(s)`.
**Common mistakes:** Using `map` with an incomplete dictionary and losing values. Writing 'Male' to 'M' and forgetting 'Female' to 'F'.

### Q24 ⭐⭐ 🟢 What is the difference between astype(int) and pd.to_numeric(), and what happens if the column has missing values?
**Asked at:** commonly asked; astype vs to_numeric appears in pandas interview lists (Flexiple)
**What the interviewer is checking:** Whether you know that astype is strict and to_numeric is forgiving, and what happens with NaN.
**Say this in the interview:** "astype(int) forces the type and crashes on text or missing values. to_numeric can turn bad text into NaN with errors='coerce'. A normal int column cannot hold NaN, so I use Int64 (capital I) or keep it as float."
**Explain simply:**
- `astype(int)` is a strict conversion: any text like 'abc' or any NaN raises an error.
- `pd.to_numeric(..., errors="coerce")` converts what it can and turns the rest into NaN.
- Plain integer columns cannot store NaN, so a column with gaps stays float (25.0) after to_numeric.
- `astype("Int64")` (capital I, 'nullable integer') keeps whole numbers and shows `<NA>` for gaps.
**Sample data:** Small series with text and with a gap. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

ages = pd.Series(["25", "31", "abc"])
ages_with_gap = pd.Series([25, 31, None])

# to_numeric: bad text can become NaN instead of crashing
print(pd.to_numeric(ages, errors="coerce"))

# astype(int) fails when the column has a missing value
try:
    ages_with_gap.astype(int)
except ValueError as error:
    print("Error:", error)

# Nullable integer type keeps the gap
print(ages_with_gap.astype("Int64"))
```
**Output:**
```text
0    25.0
1    31.0
2     NaN
dtype: float64
Error: Cannot convert non-finite values (NA or inf) to integer.Replace or remove non-finite values or cast to an integer typethat supports these values (e.g. 'Int64')
0      25
1      31
2    <NA>
dtype: Int64
```
**What it means:** The text 'abc' became NaN; `astype(int)` refused the gap; `Int64` kept whole numbers with `<NA>`.
**Likely follow-ups:**
1. When do I use astype? When the data is already clean and I only need a different type, e.g. `astype("category")`.
2. Why is it float after to_numeric? Because NaN is a float value; use Int64 if you need whole numbers.
**Common mistakes:** Using `astype(int)` on a column with NaN or 'N/A'. Not checking how many values became NaN after coerce.

### Q25 ⭐⭐ 🟢 How do you count unique values in a column, and how do you check for inconsistent spellings with value_counts()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can inspect a column for spelling variants before grouping.
**Say this in the interview:** "nunique gives the number of different values. value_counts lists each value and its count, so if I expect two cities and see five rows, I know there are spelling or case variants to clean."
**Explain simply:**
- `nunique()` counts distinct values (ignores NaN by default).
- `value_counts()` lists every distinct value with its frequency, biggest first.
- Variants like 'Hyderabad', 'HYDERABAD' and 'Hyderabad ' (trailing space) appear as separate lines.
- Add `dropna=False` to also count missing values.
**Sample data:** City column with inconsistent spellings. The last 'Hyderabad ' has a trailing space you cannot see. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"city": ["Hyderabad", "HYDERABAD", "Bengaluru", "Bangalore", "Hyderabad "]})

# How many different values
print(employees["city"].nunique())

# How often each value appears; spelling variants show up as separate rows
print(employees["city"].value_counts())
```
**Output:**
```text
5
city
Hyderabad     1
HYDERABAD     1
Bengaluru     1
Bangalore     1
Hyderabad     1
Name: count, dtype: int64
```
**What it means:** There are 5 'different' cities where the business has only 2. That tells us the column needs cleaning (strip, case, and a mapping for Bangalore/Bengaluru).
**Likely follow-ups:**
1. Why does a trailing space show as a separate row? Because 'Hyderabad ' and 'Hyderabad' are different strings; strip first.
2. How do I see unique values as a list? `employees["city"].unique()`.
**Common mistakes:** Trusting `nunique()` alone (it says 5 but not which are wrong), and forgetting that NaN is skipped.

### Q26 ⭐⭐ 🟢 How do you drop columns that are not needed, or columns with too many missing values?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can trim the table to useful columns.
**Say this in the interview:** "drop with columns= removes columns I name. For sparse columns I use dropna with axis=1 and thresh, which keeps only columns with enough real values."
**Explain simply:**
- `drop(columns=[...])` removes named columns (a typo raises an error).
- `dropna(axis=1)` works on columns instead of rows.
- `thresh=n` means 'keep the column only if it has at least n non-missing values'.
- Here half the rows is the minimum, so `internal_notes` (1 of 4 filled) is dropped.
**Sample data:** Employee table with a useless column and a mostly empty column. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104],
    "name": ["Asha", "Ravi", "Meena", "John"],
    "internal_notes": [None, None, None, "late"],
    "temp_column": [1, 1, 1, 1],
})

# Drop columns we do not need
employees = employees.drop(columns=["temp_column"])

# Keep only columns that have at least 50% of values filled
minimum_filled = len(employees) * 0.5
employees = employees.dropna(axis=1, thresh=minimum_filled)
print(employees.columns.tolist())
```
**Output:**
```text
['employee_id', 'name']
```
**What it means:** Only `employee_id` and `name` remain.
**Likely follow-ups:**
1. How do I drop columns with more than 30% missing? `df.loc[:, df.isna().mean() <= 0.3]` (see Q28).
2. Does drop change the original? No, assign it back.
**Common mistakes:** Forgetting `columns=` or `axis=1` (which drops rows instead). Dropping a column that looks empty but matters for the business.

### Q27 ⭐⭐ 🟢 What does the errors='coerce' argument do in to_numeric() and to_datetime()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know how to avoid crashes on bad values and what you get back.
**Say this in the interview:** "errors='coerce' means: if a value cannot be converted, do not stop, turn it into NaN (or NaT for dates). The default, 'raise', stops with an error. I always count the NaNs afterwards to see what was lost."
**Explain simply:**
- Default `errors="raise"` stops at the first bad value, which is useful when you want to know.
- `errors="coerce"` turns bad values into NaN (numbers) or NaT (dates, 'not a time').
- It is safe but can hide problems, so check `isna().sum()` after.
- Pandas 3 note: the older `errors="ignore"` option was removed (from memory, unverified).
**Sample data:** A salary text column and a date column with one bad entry each. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

salaries = pd.Series(["45000", "N/A", "52000"])
dates = pd.Series(["2024-01-15", "not a date", "2025-03-05"])

# Bad values become NaN / NaT instead of raising an error
print(pd.to_numeric(salaries, errors="coerce"))
print(pd.to_datetime(dates, errors="coerce"))
```
**Output:**
```text
0    45000.0
1        NaN
2    52000.0
dtype: float64
0   2024-01-15
1          NaT
2   2025-03-05
dtype: datetime64[us]
```
**What it means:** 'N/A' became NaN and 'not a date' became NaT; the valid values converted normally.
**Likely follow-ups:**
1. How do I see which values failed? `df[converted.isna() & df["col"].notna()]` shows originals that became NaN.
2. Does coerce change good values? No, only unconvertible ones.
**Common mistakes:** Using coerce and never checking, so a whole column quietly becomes NaN. Confusing NaT with NaN (NaT is the date version).

### Q28 ⭐⭐ 🟡 How do you calculate the percentage of missing values in each column, and how do you list columns with more than 30% missing?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can measure missing data as a percentage and filter on it.
**Say this in the interview:** "isna gives True/False for each cell, and mean of that is the fraction missing, because True counts as 1. Multiply by 100 for a percentage, then filter for those above 30."
**Explain simply:**
- `isna()` gives True where a value is missing.
- `.mean()` of True/False gives the share of True (True = 1, False = 0).
- `* 100` converts to percent.
- Filter the result with `> 30` and take `.index` to list the column names.
**Sample data:** Five employees, salary 20% missing, manager 80% missing. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5],
    "salary": [45000, None, 52000, 48000, 50000],
    "manager": [None, None, "Asha", None, None],
})

# Share of missing values per column, as a percentage
missing_percent = employees.isna().mean() * 100
print(missing_percent)

# Columns where more than 30% is missing
too_empty = missing_percent[missing_percent > 30].index.tolist()
print(too_empty)
```
**Output:**
```text
employee_id     0.0
salary         20.0
manager        80.0
dtype: float64
['manager']
```
**What it means:** Salary is 20% missing (keep and fill), manager is 80% missing, so it is the only column above the 30% line.
**Likely follow-ups:**
1. How do I count instead of percent? `df.isna().sum()`.
2. What then? Drop, fill or flag the sparse columns depending on whether they matter (Q15).
**Common mistakes:** Writing `isna().sum() / len(df)` wrongly or forgetting `.index` so you list numbers instead of names.

### Q29 ⭐⭐ 🟡 How do you fill missing values within each group, for example filling a missing salary with the department median using groupby and transform()?
**Asked at:** commonly asked; groupby fill listed in pandas interview lists (Flexiple)
**What the interviewer is checking:** Whether you can fill gaps using group-level logic without losing the row shape.
**Say this in the interview:** "transform('median') gives each row the median of its own department, with the same length as the table, so I can pass it straight into fillna. That fills a missing HR salary with the HR median, not the company-wide one."
**Explain simply:**
- `groupby(...).transform("median")` returns a column the same length as the original, where each row holds its group's median.
- `fillna(that_column)` fills each gap from the matching row of that column.
- Median is preferred over mean for salary because a few very high salaries drag the mean up.
- A department where every salary is missing stays NaN (no median to use).
**Sample data:** HR median is 45,000 (of 40,000 and 50,000), IT median is 80,000. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["HR", "HR", "HR", "IT", "IT"],
    "salary": [40000, None, 50000, 80000, None],
})

# Median salary of each employee's own department, repeated on every row
department_median = employees.groupby("department")["salary"].transform("median")

# Fill each gap with its own department's median
employees["salary"] = employees["salary"].fillna(department_median)
print(employees)
```
**Output:**
```text
  department   salary
0         HR  40000.0
1         HR  45000.0
2         HR  50000.0
3         IT  80000.0
4         IT  80000.0
```
**What it means:** The HR gap became 45,000 and the IT gap became 80,000, each from its own department.
**Likely follow-ups:**
1. Why not use groupby().median() directly? It returns one row per group, so it cannot be lined up with the employees.
2. What if a whole group is missing? Fill the rest with the overall median afterwards.
**Common mistakes:** Filling with the overall mean and ignoring departments, or using `apply` in a way that changes the shape.

### Q30 ⭐⭐ 🟡 How do you use the thresh and how arguments of dropna()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the two controls for how strict dropna is.
**Say this in the interview:** "how='any' drops a row if any value is missing, which is the default. how='all' drops only fully empty rows. thresh=n keeps a row only if it has at least n real values."
**Explain simply:**
- `how="any"` (default): one missing value is enough to drop the row.
- `how="all"`: drop only if everything in the row is missing.
- `thresh=n`: minimum number of non-missing values to keep the row; it replaces `how` (you cannot use both together).
- Useful for survey data where partly answered rows are still valuable.
**Sample data:** Survey with 4 respondents; the third answered nothing, the fourth answered only q3. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

survey = pd.DataFrame({
    "q1": [5, None, None, None],
    "q2": [4, 3, None, None],
    "q3": [None, 2, None, 1],
})

# how="all": drop a row only if every value is missing
print(survey.dropna(how="all"))

# thresh=2: keep a row only if it has at least 2 real values
print(survey.dropna(thresh=2))
```
**Output:**
```text
    q1   q2   q3
0  5.0  4.0  NaN
1  NaN  3.0  2.0
3  NaN  NaN  1.0
    q1   q2   q3
0  5.0  4.0  NaN
1  NaN  3.0  2.0
```
**What it means:** `how="all"` removed only the empty respondent. `thresh=2` also removed the respondent who answered just one question.
**Likely follow-ups:**
1. Can I use how and thresh together? No, pandas raises an error.
2. Does it work on columns? Yes, with `axis=1`.
**Common mistakes:** Thinking thresh is the number of missing values (it counts present values). Using `how="all"` and expecting partly empty rows to go.

### Q31 ⭐⭐ 🟡 How do you find all rows that are duplicates on Employee ID and month, including the first occurrence (keep=False)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can show every copy of a duplicate, not just the extras.
**Say this in the interview:** "duplicated with subset checks the two key columns, and keep=False marks every copy as a duplicate, including the first one, so I can look at all of them together before deciding what to delete."
**Explain simply:**
- `duplicated()` returns True/False for each row.
- By default (`keep="first"`) the first copy is False and only later copies are True.
- `keep=False` marks all copies True, so you see the full set to review.
- `subset=["employee_id", "month"]` defines 'duplicate' as same employee in the same month, even if other columns differ.
**Sample data:** Payroll where employee 101 appears twice for January. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

payroll = pd.DataFrame({
    "employee_id": [101, 101, 102, 103, 103],
    "month": ["Jan", "Jan", "Jan", "Jan", "Feb"],
    "salary": [45000, 45000, 52000, 40000, 40000],
})

# keep=False marks every copy, including the first one
repeated_rows = payroll[payroll.duplicated(subset=["employee_id", "month"], keep=False)]
print(repeated_rows)
```
**Output:**
```text
   employee_id month  salary
0          101   Jan   45000
1          101   Jan   45000
```
**What it means:** Only employee 101 in January is repeated, and both copies are shown.
**Likely follow-ups:**
1. Then how do I delete them? `drop_duplicates(subset=["employee_id", "month"])` keeps the first.
2. Why check before deleting? The copies may differ (e.g. different salary), so you must pick the right one.
**Common mistakes:** Using the default and missing the first copy. Checking whole-row duplicates when the rule is on two columns. Employee 103 is not a duplicate because the months differ.

### Q32 ⭐⭐ 🟡 How do you clean a currency column like 'Rs. 45,000' and convert it to a number?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can clean messy text into numbers safely.
**Say this in the interview:** "I remove the 'Rs.' label and commas with str.replace, trim spaces, and then convert with to_numeric using errors='coerce' so bad entries like N/A become NaN instead of crashing."
**Explain simply:**
- Currency columns arrive as text, so you cannot add or average them.
- `str.replace("Rs.", "", regex=False)` removes the label; `regex=False` means treat the text literally (the dot is not a wildcard).
- Remove the commas the same way, then `strip()` leftover spaces.
- `pd.to_numeric(..., errors="coerce")` then makes real numbers, with NaN for anything that still fails.
**Sample data:** Payroll with currency text and one 'N/A'. (the data is created inside the code block below)
**Code (what you write in the interview):**
```python
import pandas as pd

payroll = pd.DataFrame({"salary": ["Rs. 45,000", "Rs. 52,500", "N/A"]})

# Remove the "Rs." label and the commas, then trim spaces
cleaned_text = payroll["salary"].str.replace("Rs.", "", regex=False)
cleaned_text = cleaned_text.str.replace(",", "", regex=False).str.strip()

# Convert to numbers; bad text such as "N/A" becomes NaN
payroll["salary_number"] = pd.to_numeric(cleaned_text, errors="coerce")
print(payroll)
```
**Output:**
```text
       salary  salary_number
0  Rs. 45,000        45000.0
1  Rs. 52,500        52500.0
2         N/A            NaN
```
**What it means:** The text became real numbers (45000.0, 52500.0) and the N/A became NaN, ready for sum and average.
**Alternative:** A one-pattern version, `str.replace(r"[^0-9.]", "", regex=True)`, removes everything except digits and the dot. It is shorter, but it breaks 'Rs. 45,000' by keeping the dot from 'Rs.' (I tested it: 45000 became 0.45), so remove the label first.
**Likely follow-ups:**
1. What about 'Rs. 45,000.50'? Works: the decimal part stays, the result is 45000.5.
2. What about a lakh format '1,25,000'? Removing all commas handles it too.
**Common mistakes:** Using regex for the dot and getting the wrong numbers. Forgetting to assign the result. Not checking how many NaN were created.

### Q33 ⭐⭐ 🟡 How do you detect outliers using the z-score in pandas, and when is the IQR method better?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can code a z-score yourself and know its weakness.
**Say this in the interview:** "A z-score tells me how many standard deviations a value is from the average. I flag anything beyond 3. But the average and spread are themselves pulled by extreme values, so on skewed data like salary I prefer IQR, which uses quartiles and is not distorted."
**Explain simply:**
- Standard deviation = the typical distance of values from the average. Z-score = (value - average) / standard deviation.
- A common rule: z-score above 3 or below -3 is an outlier (about 3 in 1,000 values in a bell-shaped column).
- Weak spot: one huge salary inflates the average and the spread, so it can hide itself. In very small data a z-score of 3 may be impossible to reach.
- IQR (the middle 50% of values) is better for skewed data, small data, or data with many outliers.
**Sample data:** 12 employees, 11 earning 32,000 to 42,000 and one earning 400,000.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya", "Kiran", "Sana", "Dev", "Neha", "Arun", "Isha", "Vikram"],
    "salary": [32000, 35000, 38000, 41000, 36000, 39000, 34000, 40000, 37000, 33000, 42000, 400000],
})

# z-score = how many standard deviations a salary is from the average
average_salary = employees["salary"].mean()
salary_spread = employees["salary"].std()
employees["z_score"] = (employees["salary"] - average_salary) / salary_spread

# flag anyone more than 3 standard deviations away
outliers = employees[employees["z_score"].abs() > 3]
print(outliers)
```
**Output:**
```
      name  salary   z_score
11  Vikram  400000  3.173982
```
**What it means:** Vikram's salary is about 3.2 standard deviations above average, so he is flagged.
**Likely follow-ups:**
- *Why not always z-score?* It assumes a roughly bell-shaped column and is distorted by the outliers it hunts.
- *Is 3 a law?* No, it is a convention; some teams use 2.5 or 2.
**Common mistakes:** Using z-score on skewed salary data; forgetting `.abs()` so low outliers are missed; applying it to a column with blanks without knowing `mean()` skips NaN.

### Q34 ⭐⭐ 🟡 How do you handle outliers: remove, cap (winsorize) or keep? Show how to cap values at the 1st and 99th percentiles with clip().
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Judgement first (why is it an outlier?), then the clip code.
**Say this in the interview:** "First I check whether it is an error or a real value. Errors I fix or remove; real extremes I usually keep or cap, depending on the analysis. To cap, I compute the 1st and 99th percentile and use clip()."
**Explain simply:**
- Remove: when it is clearly a data error (salary typed as 3,000,000,000).
- Cap (winsorize): pull extreme values back to a limit, so they stay in the data but stop dragging the average. Percentile = the value below which that percent of rows fall.
- Keep: when the value is real and the question is about it (for example, executive pay in a payroll audit).
- Whatever you choose, tell the stakeholder and note it in the cleaning log.
**Sample data:** 12 salaries; one very low (3,000) and one very high (400,000).
**Code (what you write in the interview):**
```python
import pandas as pd

salaries = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya", "Kiran", "Sana", "Dev", "Neha", "Arun", "Isha", "Vikram"],
    "salary": [3000, 35000, 38000, 41000, 36000, 39000, 34000, 40000, 37000, 33000, 42000, 400000],
})

# the 1st and 99th percentile values become the lower and upper limits
lower_limit = salaries["salary"].quantile(0.01)
upper_limit = salaries["salary"].quantile(0.99)

# clip pulls anything outside the limits back to the limit
salaries["salary_capped"] = salaries["salary"].clip(lower=lower_limit, upper=upper_limit)
print(salaries.loc[[0, 11], ["name", "salary", "salary_capped"]])
```
**Output:**
```
      name  salary  salary_capped
0     Asha    3000         6300.0
11  Vikram  400000       360620.0
```
**What it means:** The two extremes are pulled in to the limits; every other salary is untouched. I save the result in a new column so the original stays available.
**Likely follow-ups:**
- *Why a new column?* So the raw data is never lost and the change is auditable.
- *Is capping at 1 and 99 always right?* No; 5 and 95 is also used. It is a judgement call to state openly.
**Common mistakes:** Capping before checking if the values are errors; overwriting the original column; capping the whole file when outliers differ by group (see grade-wise logic).

### Q35 ⭐⭐ 🟡 How do you split a 'Full Name' column into first and last name using str.split()?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know `expand=True`, `n=1`, and think about names that do not fit the pattern.
**Say this in the interview:** "I strip spaces, then use str.split with a space, n=1 so it only splits once, and expand=True so the pieces become separate columns."
**Explain simply:**
- `str.split(" ")` cuts each text at the spaces. By default it gives a list inside one column.
- `expand=True` turns the pieces into separate columns.
- `n=1` means one cut only, so "Ravi Kumar Singh" becomes first = Ravi, last = Kumar Singh.
- A one-word name gets a blank (NaN) last name; decide what to do with those.
**Sample data:** four names, one with extra spaces, one with three parts, one with a single word.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "full_name": ["Asha Rao", "Ravi Kumar Singh", "  Meena Iyer ", "Prince"],
})

# strip spaces, then split at the first space only: first name, then everything else
employees[["first_name", "last_name"]] = (
    employees["full_name"].str.strip().str.split(" ", n=1, expand=True)
)
print(employees)
```
**Output:**
```
          full_name first_name    last_name
0          Asha Rao       Asha          Rao
1  Ravi Kumar Singh       Ravi  Kumar Singh
2       Meena Iyer       Meena         Iyer
3            Prince     Prince          NaN
```
**What it means:** Every name is split into two columns; the single-word name gets an empty last name that I would flag for review.
**Likely follow-ups:**
- *What about names like "Mary Ann Smith"?* No rule is perfect; I would state my rule (first word = first name) and check a sample.
- *Why strip first?* Leading spaces would create an empty first piece.
**Common mistakes:** Forgetting `expand=True` (you get lists); not using `n=1`, which creates a different number of columns per row and causes a length error.

### Q36 ⭐⭐ 🟡 How do you filter rows with invalid values, for example ages below 18 or above 70, or negative salaries?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Boolean filtering with `|`, `&` and brackets, and that you look at bad rows before dropping them.
**Say this in the interview:** "I build a condition for each rule, join them with | for 'any rule broken', and look at those rows first. Then I keep the valid ones, or send the bad ones back to the data owner."
**Explain simply:**
- A condition like `age < 18` gives True/False for every row; using it inside `df[...]` keeps the True rows.
- Join conditions with `|` (or) and `&` (and). Each condition needs its own brackets.
- `between(18, 70)` is a tidy way to say "18 to 70, both included".
- Do not delete silently: count and show the invalid rows, then decide.
**Sample data:** five employees: one aged 16, one aged 82, one with salary -5,000.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "age": [28, 16, 45, 82, 33],
    "salary": [45000, 30000, -5000, 60000, 52000],
})

# rows that break a rule: age outside 18 to 70, or a negative salary
invalid_rows = employees[
    (employees["age"] < 18) | (employees["age"] > 70) | (employees["salary"] < 0)
]

# rows that pass every rule
valid_rows = employees[
    employees["age"].between(18, 70) & (employees["salary"] >= 0)
]
print(invalid_rows)
print(valid_rows)
```
**Output:**
```
    name  age  salary
1   Ravi   16   30000
2  Meena   45   -5000
3   John   82   60000
    name  age  salary
0   Asha   28   45000
4  Priya   33   52000
```
**What it means:** Three rows break at least one rule and are set aside; two rows are clean.
**Likely follow-ups:**
- *What about missing ages?* A missing age fails both tests silently in some forms; I check `isna()` separately.
- *Why not delete the 16-year-old?* It may be a typing error or a real intern; ask the source.
**Common mistakes:** Using `and` / `or` instead of `&` / `|`; forgetting brackets around each condition (gives an error); dropping bad rows without telling anyone.

### Q37 ⭐⭐ 🟡 Why does df[df['salary'] > 0]['bonus'] = 0 not work reliably, and what is the correct way using loc?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you understand chained indexing and the single-step `.loc` fix.
**Say this in the interview:** "That is two steps: first filter the rows, which may give me a copy, then set a value on that copy. The original may not change. With .loc I give the row condition and the column in one step, so it writes to the original."
**Explain simply:**
- Chained indexing = two selections in a row: `df[condition]["bonus"]`. The first one can return a copy (a separate duplicate), so the second one edits the duplicate.
- Older pandas gave a SettingWithCopyWarning and sometimes worked, sometimes not (that is the "unreliable" part).
- In pandas 3.0 (checked by running it here) it never changes the original and raises a ChainedAssignmentError warning.
- Correct form: `df.loc[row_condition, "column"] = value`.
**Sample data:** three employees, one with salary 0.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena"],
    "salary": [45000, 0, 52000],
    "bonus": [5000, 3000, 4000],
})

# one step: row condition and column name together
employees.loc[employees["salary"] > 0, "bonus"] = 0
print(employees)
```
**Output:**
```
    name  salary  bonus
0   Asha   45000      0
1   Ravi       0   3000
2  Meena   52000      0
```
**What it means:** Bonus became 0 only where salary is above 0. The chained version left every bonus unchanged when I ran it in pandas 3.0.
**Likely follow-ups:**
- *Does Copy-on-Write change this?* Yes, it makes chained assignment never work, which is at least predictable.
**Common mistakes:** Believing the warning is harmless; silencing the warning instead of fixing the code; chaining `.loc[...]["col"] = ...` as well.

### Q38 ⭐⭐ 🟡 How do you convert a column to the category dtype, and why is it useful?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know category saves memory and speeds up repeated labels.
**Say this in the interview:** "I use astype('category'). It stores each distinct label once and keeps a small number code per row, so columns like department or grade use far less memory."
**Explain simply:**
- dtype = the data type of a column. Category is meant for text with few distinct values (department, grade, gender).
- Pandas keeps a list of labels (`categories`) and just a number per row pointing to the label.
- Benefits: smaller memory (in a quick test here, 200,000 department values went from about 10.6 MB to 0.2 MB), faster group-bys, and you can set a custom order (Junior, Mid, Senior).
- Not useful for columns where almost every value is different, such as names.
**Sample data:** six employees across three departments.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya", "Kiran"],
    "department": ["HR", "Finance", "HR", "IT", "HR", "Finance"],
})

# store the repeated text as a small set of labels
employees["department"] = employees["department"].astype("category")

print(employees["department"].dtype)
print(employees["department"].cat.categories)
```
**Output:**
```
category
Index(['Finance', 'HR', 'IT'], dtype='str')
```
**What it means:** The column is now a category with three labels, however many rows there are.
**Likely follow-ups:**
- *Any trap?* New values not in the category list become NaN if you assign them; add the label first.
**Common mistakes:** Converting high-variety columns; forgetting that category comparisons like `<` only work if you define an ordered category.

### Q39 ⭐⭐ 🟡 What is the difference between inplace=True and assigning the result back, and why do many people avoid inplace?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the modern style and its reasons.
**Say this in the interview:** "Most pandas methods return a new object. I assign it back, like df['salary'] = df['salary'].fillna(...). inplace=True changes the original and returns nothing, but it does not save memory, cannot be chained, and is being discouraged."
**Explain simply:**
- Assigning back: you see exactly what is being replaced, and you can chain steps.
- `inplace=True` returns `None`, so `df = df.drop_duplicates(inplace=True)` wipes your data (I confirmed it returns None).
- Often it still makes a copy inside, so there is no real memory benefit.
- In pandas 3.0, `df["salary"].fillna(0, inplace=True)` does not update the DataFrame at all and shows a warning (verified by running it).
**Sample data:** three employees, one with a missing salary.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena"],
    "salary": [45000, None, 52000],
})

# preferred: assign the result back
employees["salary"] = employees["salary"].fillna(employees["salary"].median())
print(employees)
```
**Output:**
```
    name   salary
0   Asha  45000.0
1   Ravi  48500.0
2  Meena  52000.0
```
**What it means:** The blank became the median (48,500) and the column was replaced in one clear step.
**Likely follow-ups:**
- *Is inplace ever fine?* Yes on a whole DataFrame, like `df.drop(columns=..., inplace=True)`, but the plain assignment is still the safer habit.
**Common mistakes:** Assigning the result of an inplace call (gets None); using inplace on a single column of a DataFrame.

### Q40 ⭐⭐ 🟡 How do you create a flag column marking missing values, so you keep that information after filling?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know filling destroys the "was missing" information unless you save it first.
**Say this in the interview:** "Before I fill, I create a True/False column using isna(). Then the fill is traceable, and later I can check whether imputed rows behave differently."
**Explain simply:**
- Imputing (filling) = replacing a blank with an estimate such as the median.
- After filling, you cannot tell real salaries from estimated ones, so flag first.
- The flag is useful for reports ("12% of salaries were estimated") and for models.
- Order matters: flag, then fill.
**Sample data:** four employees, two without a salary.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": [45000, None, 52000, None],
})

# flag first, while the blanks are still blank
employees["salary_was_missing"] = employees["salary"].isna()

# then fill with the median
employees["salary"] = employees["salary"].fillna(employees["salary"].median())
print(employees)
```
**Output:**
```
    name   salary  salary_was_missing
0   Asha  45000.0               False
1   Ravi  48500.0                True
2  Meena  52000.0               False
3   John  48500.0                True
```
**What it means:** Ravi and John carry an estimated salary and are clearly marked.
**Likely follow-ups:**
- *Can you count them?* `employees["salary_was_missing"].sum()` gives 2.
**Common mistakes:** Filling first and flagging after (everything is False); flagging with `== ""` when the blanks are real NaN.

### Q41 ⭐⭐ 🟡 How do you standardise inconsistent department names such as 'Human Resources', 'HR' and 'H.R.' into one value?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A two-step approach: tidy the text, then map to official names.
**Say this in the interview:** "First I trim spaces, lower-case and remove dots so small differences disappear. Then I map each remaining spelling to one official name with a dictionary. I check with value_counts that nothing is left unmapped."
**Explain simply:**
- Tidying text first means the dictionary needs fewer entries ("hr" covers "HR", " hr ", "H.R.").
- A dictionary (`{old: new}`) is the official lookup you can show to the HR team.
- `map()` gives NaN for anything not in the dictionary, which is useful: unmapped spellings are easy to spot.
- `.replace(".", "", regex=False)` treats the dot as plain text; otherwise "." means "any character" in a regular expression.
**Sample data:** five employees with four spellings of HR.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "department": ["Human Resources", "HR", "H.R.", " hr ", "Finance"],
})

# step 1: tidy the text (trim spaces, lower case, remove dots)
tidy_text = (
    employees["department"].str.strip().str.lower().str.replace(".", "", regex=False)
)

# step 2: map every spelling to one official name
department_names = {"human resources": "HR", "hr": "HR", "finance": "Finance"}
employees["department_clean"] = tidy_text.map(department_names)
print(employees)
```
**Output:**
```
    name       department department_clean
0   Asha  Human Resources               HR
1   Ravi               HR               HR
2  Meena             H.R.               HR
3   John              hr                HR
4  Priya          Finance          Finance
```
**What it means:** All four HR spellings now read "HR".
**Likely follow-ups:**
- *What if there are hundreds of spellings?* Review `value_counts()` of the unmapped ones and extend the dictionary; fuzzy matching is a last resort.
**Common mistakes:** Mapping before tidying; not checking for NaN after `map()`; using `replace(".", "")` without `regex=False`.

### Q42 ⭐⭐ 🟡 A column of Yes/No answers contains blanks and mixed case. How do you clean it and convert it to True/False?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Tidy text, map, and a sensible choice for blanks.
**Say this in the interview:** "I strip and lower-case the text, map yes to True and no to False, and leave blanks as missing instead of guessing. I use the nullable boolean type so True, False and missing can all coexist."
**Explain simply:**
- Mixed case and stray spaces ("YES", " no") would otherwise count as different answers.
- Anything not in the map (blank, NaN) becomes missing, which is honest: we do not know the answer.
- A plain True/False column cannot hold "missing" cleanly; the `"boolean"` type can (it shows `<NA>`).
- Do not turn blanks into False: that says "No" when the person never answered.
**Sample data:** five survey answers: "Yes", " no", "YES", an empty string and a missing value.
**Code (what you write in the interview):**
```python
import pandas as pd

survey = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "willing_to_relocate": ["Yes", " no", "YES", "", None],
})

# trim spaces and lower case, then map to True/False
answers = survey["willing_to_relocate"].str.strip().str.lower()
survey["relocate_flag"] = answers.map({"yes": True, "no": False}).astype("boolean")
print(survey)
```
**Output:**
```
    name willing_to_relocate  relocate_flag
0   Asha                 Yes           True
1   Ravi                  no          False
2  Meena                 YES           True
3   John                               <NA>
4  Priya                 NaN           <NA>
```
**What it means:** Real answers became True/False; the two unanswered rows stay missing.
**Likely follow-ups:**
- *What about "Y" or "yeah"?* Add them to the dictionary after checking `value_counts()`.
**Common mistakes:** `== "Yes"` comparisons, which turn every blank into False; skipping the lower-case step.

### Q43 ⭐⭐ 🟡 How do you find rows with an invalid email or phone number using str.contains() or a regular expression?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic regex comfort and handling of missing values.
**Say this in the interview:** "I write a simple pattern for the email shape and use str.contains with na=False. For phone I strip everything that is not a digit and check the length is 10. Then I filter with ~ to see the invalid rows."
**Explain simply:**
- A regular expression (regex) is a pattern language for text. `\w` = a letter, digit or underscore; `\d` = a digit; `\D` = anything that is not a digit.
- `^` and `$` mean "start" and "end", so the whole value must match.
- `na=False` makes missing emails count as "no match", so they land in the invalid list instead of causing an error.
- `~` flips True/False. A simple pattern catches obvious errors; it does not prove an email really exists.
**Sample data:** four contacts: "ravi@abc" has no dot after the @, one phone has 5 digits, one email is missing.
**Code (what you write in the interview):**
```python
import pandas as pd

contacts = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "email": ["asha@abc.com", "ravi@abc", "meena.k@abc.co.in", None],
    "phone": ["9876543210", "98765", "98765-43210", "9123456789"],
})

# a simple email pattern: text, an @, text, a dot, text
email_pattern = r"^[\w.+-]+@[\w-]+\.[\w.]+$"
valid_email = contacts["email"].str.contains(email_pattern, regex=True, na=False)

# keep digits only, then a valid phone has exactly 10 digits
phone_digits = contacts["phone"].str.replace(r"\D", "", regex=True)
valid_phone = phone_digits.str.len() == 10

invalid_contacts = contacts[~valid_email | ~valid_phone]
print(invalid_contacts)
```
**Output:**
```
   name     email       phone
1  Ravi  ravi@abc       98765
3  John       NaN  9123456789
```
**What it means:** Ravi has a bad email and phone; John has no email on file. Meena's "98765-43210" passes because I removed the dash first.
**Likely follow-ups:**
- *Do you use one perfect email regex?* No, a simple one is enough for cleaning; real validation is sending an email.
**Common mistakes:** Forgetting `na=False` (NaN breaks the filter); no `^...$`, so partial matches pass; Indian numbers with +91 need extra handling.

### Q44 ⭐⭐ 🟡 Attendance data has a missing check-out time on some days. How would you handle it in pandas?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Business judgement: do not invent hours; flag, calculate safely and report.
**Say this in the interview:** "I would not guess the check-out time. I flag those days, calculate hours worked so it stays blank for them, and share the list with HR operations to confirm. If policy says to assume the shift end time, I would fill it and keep the flag."
**Explain simply:**
- A missing check-out could mean a forgotten swipe, a system fault, or a person who left early. The data cannot tell which.
- Subtracting a date-time from NaT (a missing date-time) gives NaT, so `hours_worked` becomes NaN automatically and does not pollute averages.
- Averages like `mean()` skip NaN, so average hours are based only on complete days; I state that.
- Options by rule: leave blank, fill with scheduled shift end, or treat as half-day; each needs HR policy agreement.
**Sample data:** four attendance rows; Asha has no check-out on 4 Nov.
**Code (what you write in the interview):**
```python
import pandas as pd

attendance = pd.DataFrame({
    "employee": ["Asha", "Asha", "Ravi", "Ravi"],
    "check_in": pd.to_datetime(["2025-11-03 09:05", "2025-11-04 09:00", "2025-11-03 09:30", "2025-11-04 09:10"]),
    "check_out": pd.to_datetime(["2025-11-03 18:00", None, "2025-11-03 17:30", "2025-11-04 18:15"]),
})

# flag the days with no check-out so they can be reviewed
attendance["check_out_missing"] = attendance["check_out"].isna()

# hours worked stays blank (NaN) when check-out is missing; no guessing
time_worked = attendance["check_out"] - attendance["check_in"]
attendance["hours_worked"] = time_worked.dt.total_seconds() / 3600
print(attendance[["employee", "check_out_missing", "hours_worked"]])
```
**Output:**
```
  employee  check_out_missing  hours_worked
0     Asha              False      8.916667
1     Asha               True           NaN
2     Ravi              False      8.000000
3     Ravi              False      9.083333
```
**What it means:** Three days have hours; Asha's 4 Nov is flagged for follow-up instead of showing a made-up number.
**Likely follow-ups:**
- *How would you tell the manager?* "N days had no check-out; hours are for complete days only."
**Common mistakes:** Filling with 0 (shows 0 hours worked); filling with the mean without telling anyone; checking out time on a different date (night shift) and getting negative hours.

### Q45 ⭐⭐ 🔴 You merge two files and the row count goes up unexpectedly. How do you check for duplicate keys and clean them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know duplicate keys multiply rows and you have a repeatable check.
**Say this in the interview:** "A merge returns one row for every matching pair. If the key repeats on the right side, each left row is copied for each match, so rows grow. I find repeated keys with duplicated(keep=False), decide which row is correct, drop the rest, and re-merge with validate so it stops me if it happens again."
**Explain simply:**
- Key = the column used to match the two tables (here `dept_id`). It should be unique in the lookup table.
- In the example, Finance appears twice in the departments table, so Ravi appears twice after the merge (3 rows became 4).
- `keep=False` shows all copies of a repeated key, so you can decide which is right (here, the old name is wrong).
- `validate="many_to_one"` raises an error if the right table has repeated keys.
**Sample data:** 3 employees; a departments table where `dept_id` 20 appears twice.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee": ["Asha", "Ravi", "Meena"],
    "dept_id": [10, 20, 10],
})
departments = pd.DataFrame({
    "dept_id": [10, 20, 20],
    "dept_name": ["HR", "Finance", "Finance (old)"],
})

merged = employees.merge(departments, on="dept_id", how="left")
print(len(employees), len(merged))

# find the repeated keys (keep=False shows every copy)
duplicate_keys = departments[departments.duplicated("dept_id", keep=False)]
print(duplicate_keys)

# keep one row per key, then merge again; validate stops it if keys repeat
departments_clean = departments.drop_duplicates("dept_id", keep="first")
merged = employees.merge(departments_clean, on="dept_id", how="left", validate="many_to_one")
print(len(employees), len(merged))
```
**Output:**
```
3 4
   dept_id      dept_name
1       20        Finance
2       20  Finance (old)
3 3
```
**What it means:** The duplicate key added a row (3 to 4). After cleaning the lookup table, the row count stays 3.
**Likely follow-ups:**
- *How do you decide which duplicate to keep?* Ask the data owner or use a date column; `keep="first"` is only a placeholder rule.
- *What if duplicates are on the left table?* Same check on the left; both sides can be wrong.
**Common mistakes:** Not comparing row counts before and after; dropping duplicates blindly; using an outer or inner merge and not noticing lost rows.

### Q46 ⭐ 🟢 How do you reset the index after removing rows, and why does the index have gaps?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the index is a label that stays with the row.
**Say this in the interview:** "The index is each row's label. When I filter rows out, the remaining rows keep their original labels, so there are gaps. reset_index(drop=True) renumbers them 0, 1, 2."
**Explain simply:**
- Index = the row labels on the left (0, 1, 2...).
- Filtering or dropping does not renumber; labels stay attached to rows, so you can still trace back to the source row.
- `drop=True` discards the old labels. Without it, pandas keeps the old index as a new column called `index`.
- Reset when you need clean numbering for display, export or position-based work.
**Sample data:** four employees, one with a negative salary removed.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": [45000, -100, 52000, 48000],
})

valid_employees = employees[employees["salary"] > 0]
print(valid_employees)

# drop=True throws away the old index instead of keeping it as a column
valid_employees = valid_employees.reset_index(drop=True)
print(valid_employees)
```
**Output:**
```
    name  salary
0   Asha   45000
2  Meena   52000
3   John   48000
    name  salary
0   Asha   45000
1  Meena   52000
2   John   48000
```
**What it means:** Row 1 was removed, leaving a gap; after reset the rows are numbered 0 to 2.
**Likely follow-ups:**
- *Does the gap cause errors?* Only with `.loc[1]` (label 1 no longer exists) versus `.iloc[1]` (second row).
**Common mistakes:** Forgetting `drop=True` and getting an extra `index` column; not saving the result back.

### Q47 ⭐ 🟢 How do you convert a column of 'Yes'/'No' to 1/0 in pandas?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic `map()` with a dictionary.
**Say this in the interview:** "I use map with a dictionary, Yes to 1 and No to 0. Then I can sum the column to count the Yeses or average it to get a percentage, like an attrition rate."
**Explain simply:**
- `map()` replaces each value using a lookup dictionary.
- Values not in the dictionary become NaN, which exposes spelling problems ("yes", "Y").
- 1/0 columns are handy: sum = count of Yes, mean = share of Yes.
**Sample data:** three employees with a Yes/No "left company" column.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena"],
    "left_company": ["Yes", "No", "Yes"],
})

employees["left_flag"] = employees["left_company"].map({"Yes": 1, "No": 0})
print(employees)
```
**Output:**
```
    name left_company  left_flag
0   Asha          Yes          1
1   Ravi           No          0
2  Meena          Yes          1
```
**What it means:** Two of three employees left, so the mean of `left_flag` (0.67) is the attrition rate.
**Alternative:** `(employees["left_company"] == "Yes").astype(int)`; shorter, but any blank or typo silently becomes 0.
**Likely follow-ups:**
- *If the text has mixed case?* Clean with `.str.strip().str.lower()` first and use lower-case keys.
**Common mistakes:** Mixed-case values turning into NaN; using the `==` form when blanks exist.

### Q48 ⭐ 🟢 What does the nunique() method do, and how is it different from unique()?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Count versus list, and the NaN difference.
**Say this in the interview:** "unique() gives me the actual distinct values; nunique() gives me how many there are. nunique() ignores missing values by default, while unique() includes them."
**Explain simply:**
- `unique()` returns the list of distinct values (in order of first appearance).
- `nunique()` returns a single number: how many distinct values.
- NaN is shown by `unique()` but not counted by `nunique()` unless you pass `dropna=False`.
- On a whole DataFrame, `df.nunique()` gives the count per column, handy for spotting ID columns (unique per row) and category columns.
**Sample data:** six department values, one missing.
**Code (what you write in the interview):**
```python
import pandas as pd

departments = pd.Series(["HR", "IT", "HR", "Finance", "IT", None])

print(departments.unique())
print(departments.nunique())
print(departments.nunique(dropna=False))
```
**Output:**
```
<StringArray>
['HR', 'IT', 'Finance', nan]
Length: 4, dtype: str
3
4
```
**What it means:** There are 3 real departments; counting the missing value as its own entry gives 4. (In pandas 3.0 the unique list prints as a StringArray; in older versions it is a plain array.)
**Likely follow-ups:**
- *How do you count employees per department?* `value_counts()`, which counts rows per value.
**Common mistakes:** Expecting `nunique()` to count NaN; using `len(unique())` and getting a count that includes NaN.

### Q49 ⭐ 🟡 How do you replace placeholder values like -1, 999 or 'Unknown' with NaN before cleaning?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that fake values hide inside "complete" columns and would wreck averages?
**Say this in the interview:** "Placeholders like -1 or 999 are missing data in disguise. I replace them with NaN first, so pandas treats them as missing and the averages and counts are honest."
**Explain simply:**
- NaN means "no value" in pandas. Functions like `mean()` skip it, but they happily include a 999.
- `replace(old, new)` swaps a value; I use `np.nan` as the new value.
- I find placeholders first with `value_counts()` or `describe()` (a minimum of -1 is a giveaway).
- Replacing turns whole-number columns into decimals (29 becomes 29.0) because NaN is a decimal type.
**Sample data:** 4 employees; age uses -1, tenure_months uses 999, department uses "Unknown".
**Code (what you write in the interview):**
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "Karan"],
    "age": [29, -1, 41, 35],
    "tenure_months": [24, 999, 60, 12],
    "department": ["HR", "Unknown", "IT", "Unknown"],
})

employees["age"] = employees["age"].replace(-1, np.nan)
employees["tenure_months"] = employees["tenure_months"].replace(999, np.nan)
employees["department"] = employees["department"].replace("Unknown", np.nan)

print(employees)
print(employees.isna().sum())
```
**Output:**
```
    name   age  tenure_months department
0   Asha  29.0           24.0         HR
1   Ravi   NaN            NaN        NaN
2  Meena  41.0           60.0         IT
3  Karan  35.0           12.0        NaN
name             0
age              1
tenure_months    1
department       2
dtype: int64
```
**What it means:** The three placeholders are now real missing values, so `isna().sum()` counts them and a later `mean()` will ignore them.
**Likely follow-ups:**
- *Can I do it for the whole table at once?* Yes: `df.replace([-1, 999, "Unknown"], np.nan)`, but only if those values are placeholders in every column.
- *Why not just delete those rows?* Deleting loses the other good columns of that row; decide after you know how many there are.
**Common mistakes:** Replacing -1 everywhere when -1 is a valid value in some column (for example a profit/loss column); forgetting to assign the result back (`replace` returns a new column).

### Q50 ⭐ 🟡 How do you fill missing values using interpolate(), and when is it appropriate?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know interpolation is for ordered numeric data, not a general fill?
**Say this in the interview:** "interpolate() estimates a missing number from the values around it, by default drawing a straight line between the last and next known values. I use it only for ordered data like a monthly headcount, never for categories or unrelated rows."
**Explain simply:**
- Interpolation means "guess a value that sits between two known values".
- It makes sense when the order matters and the numbers change smoothly: headcount by month, daily temperature, a meter reading.
- It does not make sense for unordered data. Two employees side by side in a table have no link, so a salary "between" them is meaningless.
- It cannot fill a gap at the very start (nothing before it); leading NaNs stay NaN.
**Sample data:** headcount by month, with March and April missing.
**Code (what you write in the interview):**
```python
import pandas as pd

headcount = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "headcount": [100, 104, None, None, 116, 120],
})

headcount["filled"] = headcount["headcount"].interpolate()
print(headcount)
```
**Output:**
```
  month  headcount  filled
0   Jan      100.0   100.0
1   Feb      104.0   104.0
2   Mar        NaN   108.0
3   Apr        NaN   112.0
4   May      116.0   116.0
5   Jun      120.0   120.0
```
**What it means:** Headcount went from 104 to 116 over three steps, so each missing month gets a 4-person step: 108 and 112.
**Likely follow-ups:**
- *Difference from ffill?* ffill copies the last value (104, 104); interpolate follows the trend.
- *What if dates are unevenly spaced?* Set the date as the index and use `method="time"`.
**Common mistakes:** Using it on unsorted data; using it on text or on cross-sectional data (a salary column of different employees); hiding a long gap with made-up numbers instead of flagging it.

### Q51 ⭐ 🟡 How do you find near-duplicate company names such as 'Infosys Ltd' and 'Infosys Limited' in pandas?
**Asked at:** commonly asked (no company-specific report found); the fuzzy-duplicate topic is listed as a niche item in prep lists.
**What the interviewer is checking:** Can you standardise text first, so that "different" spellings collapse into one key?
**Say this in the interview:** "I make a cleaned copy of the name: lower case, no dots, 'limited' and 'ltd' removed, extra spaces gone. Then I look for repeated cleaned names. For harder typos I would use difflib or a fuzzy matching library."
**Explain simply:**
- Exact duplicate checks fail because "Infosys Ltd" and "Infosys Limited" are different text.
- The fix is a **key**: a simplified version of the name that is the same for look-alikes.
- `duplicated(subset, keep=False)` shows every row of a repeated key, so I can review them before merging.
- I always keep the original column and review the groups by eye; automatic merging can join two genuinely different companies.
**Sample data:** six company names with spacing, case and "Ltd/Limited" differences.
**Code (what you write in the interview):**
```python
import pandas as pd

candidates = pd.DataFrame({"company": ["Infosys Ltd", "Infosys Limited", "TCS", "Tcs ", "Wipro Ltd.", "Wipro"]})

# make a cleaned version: lower case, no dots, no 'ltd/limited', single spaces
candidates["clean_name"] = (
    candidates["company"].str.lower()
    .str.replace(".", "", regex=False)
    .str.replace(r"\b(limited|ltd)\b", "", regex=True)
    .str.split().str.join(" ")
)

# names that appear more than once after cleaning are near-duplicates
duplicates = candidates[candidates.duplicated("clean_name", keep=False)]
print(duplicates.sort_values("clean_name"))
```
**Output:**
```
           company clean_name
0      Infosys Ltd    infosys
1  Infosys Limited    infosys
2              TCS        tcs
3             Tcs         tcs
4       Wipro Ltd.      wipro
5            Wipro      wipro
```
**What it means:** Three pairs that looked different are now clearly the same company; I would map each pair to one official name.
**Alternative:** For spelling mistakes ("Infossys"), `difflib.get_close_matches("Infosys Limited", names, cutoff=0.8)` returns the closest names (it returned `['Infosys Limited', 'Infosys Ltd']` when I ran it). For large data, libraries such as rapidfuzz are used (not run here).
**Likely follow-ups:**
- *Why not drop duplicates straight away?* Review first; "Tata Motors" and "Tata Steel" may look close but are different.
**Common mistakes:** Overwriting the original names with no copy; cleaning so aggressively that different companies collapse; comparing every name with every other name on a huge table (very slow).

### Q52 ⭐ 🟡 How do you use select_dtypes() to clean numeric and text columns separately?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you apply the right cleaning to the right kind of column without typing every column name?
**Say this in the interview:** "select_dtypes picks columns by their data type. I get the list of numeric columns and fill them with the median, and the list of text columns and trim and tidy them."
**Explain simply:**
- **dtype** means the type of data in a column: number, text, date.
- `select_dtypes(include="number")` returns only numeric columns; `exclude="number"` returns the rest.
- I only need `.columns` from it, which gives a list of names I can loop over.
- Text methods like `.str.strip()` fail on numeric columns, and `median()` fails on text, so separating them avoids errors.
**Sample data:** 3 employees with messy names/departments and missing salary and age.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": [" Asha ", "ravi", "MEENA"],
    "department": ["hr ", "IT", " Finance"],
    "salary": [50000.0, None, 70000.0],
    "age": [29, 31, None],
})

numeric_columns = employees.select_dtypes(include="number").columns
text_columns = employees.select_dtypes(exclude="number").columns

# numbers: fill gaps with each column's median
employees[numeric_columns] = employees[numeric_columns].fillna(employees[numeric_columns].median())

# text: trim spaces and make capitalisation consistent
for column in text_columns:
    employees[column] = employees[column].str.strip().str.title()

print(employees)
```
**Output:**
```
    name department   salary   age
0   Asha         Hr  50000.0  29.0
1   Ravi         It  60000.0  31.0
2  Meena    Finance  70000.0  30.0
```
**What it means:** Missing salary became 60000 (median of 50000 and 70000), missing age became 30, and all text is tidy. Note "HR" became "Hr"; acronyms need a separate fix (see the department-name question).
**Likely follow-ups:**
- *Why did you use exclude="number" instead of include="object"?* In pandas 3 text columns have the `str` type, not `object`. I verified `include="object"` still selects them but gives a deprecation warning, so `exclude="number"` is safer.
**Common mistakes:** Using `include="object"` and silently missing text columns in newer pandas; running `.str` methods on a column with numbers; ID columns count as numeric, so do not fill or scale them.

### Q53 ⭐ 🟡 How do you check whether a column's values are consistent with another column, for example exit date earlier than join date?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you do cross-column sanity checks, and handle missing values correctly?
**Say this in the interview:** "I make sure both columns are real dates, then compare them row by row with a boolean filter: exit date less than join date. Those rows are impossible, so I list them and send them back to the data owner."
**Explain simply:**
- Comparing two columns in pandas works row by row: `df["a"] < df["b"]` gives True or False for each employee.
- Convert text to dates first with `to_datetime`; text dates compare alphabetically, which is risky.
- A missing exit date (NaT, "not a time") means the person is still working. Comparing with NaT gives False, so those rows are not flagged. That is the behaviour we want.
- I report, not auto-fix: I do not know which of the two dates is wrong.
**Sample data:** 4 employees; 102 and 104 exit before they joined; 103 is still employed.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104],
    "join_date": ["2022-03-01", "2023-06-15", "2021-01-10", "2024-02-01"],
    "exit_date": ["2024-05-31", "2023-05-01", None, "2024-01-15"],
})
employees["join_date"] = pd.to_datetime(employees["join_date"])
employees["exit_date"] = pd.to_datetime(employees["exit_date"])

# exit before join is impossible; missing exit dates (still working) compare as False
bad_dates = employees[employees["exit_date"] < employees["join_date"]]
print(bad_dates)
```
**Output:**
```
   employee_id  join_date  exit_date
1          102 2023-06-15 2023-05-01
3          104 2024-02-01 2024-01-15
```
**What it means:** Two records have impossible dates. I would count them, share the list with HR operations, and exclude them from tenure calculations until corrected.
**Likely follow-ups:**
- *Other cross-column checks?* Age versus join date (joined before age 18), bonus larger than salary, check-out before check-in.
**Common mistakes:** Comparing columns still stored as text; mistaking day/month order when parsing; treating missing exit dates as errors.

### Q54 ⭐ 🟡 What is Copy-on-Write in newer pandas versions, and how does it change the SettingWithCopyWarning problem?
**Asked at:** commonly asked (no company-specific report found); a niche, version-awareness question.
**What the interviewer is checking:** Do you know that modern pandas made copies predictable?
**Say this in the interview:** "With Copy-on-Write, every subset or derived object behaves like its own copy. Changing it never changes the original. So the old SettingWithCopyWarning confusion goes away, and chained assignment simply does nothing to the original."
**Explain simply:**
- Old pandas sometimes returned a "view" (a window onto the original data) and sometimes a copy, and you could not tell which. That was the source of SettingWithCopyWarning.
- **Copy-on-Write (CoW)** means data is only physically copied at the moment you modify it, and the change stays with the object you modified.
- Result: a filtered table is safely independent. No more guessing.
- Chained assignment (`df[mask]["col"] = value`) edits a temporary object, so the original never changes. In my run on pandas 3.0.5 it raised a `ChainedAssignmentError` warning and left the data unchanged.
- The correct habit is unchanged: `df.loc[mask, "col"] = value`.
**Sample data:** 3 employees, one with salary 0.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"name": ["Asha", "Ravi", "Meena"], "salary": [50000, 0, 70000]})

# 1. Chained assignment: changes a temporary copy
employees[employees["salary"] > 0]["salary"] = 99999
print(employees["salary"].tolist())

# 2. A subset is its own copy: editing it never touches employees
paid = employees[employees["salary"] > 0]
paid["bonus"] = 5000
print(employees.columns.tolist())
```
**Output:** (the first line also printed a `ChainedAssignmentError` warning on pandas 3.0.5)
```
[50000, 0, 70000]
['name', 'salary']
```
**What it means:** Neither step touched `employees`, and the second step raised no SettingWithCopyWarning. If I want to change the original, I use `.loc`.
**Likely follow-ups:**
- *Which version has it by default?* Pandas 3.0 (I ran 3.0.5). It was optional in 2.x; from memory, unverified: pandas 2.x had an opt-in switch.
- *Is `.copy()` still needed?* Not for safety, but harmless.
**Common mistakes:** Believing chained assignment now works; assuming the subset updates the original; writing code that only works on one pandas version.

### Q55 ⭐ 🟡 How do you apply a custom cleaning function to a column using apply(), and why are vectorised string methods usually faster?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you write a custom function, and do you know the built-in way first?
**Say this in the interview:** "apply runs my own Python function on every value in a column. I reach for it only when no built-in method fits, because built-in vectorised methods like `.str.strip()` are shorter, handle missing values, and are usually faster."
**Explain simply:**
- **Vectorised** means one pandas command handles the whole column at once, instead of me looping value by value.
- `apply(function)` calls my function once per value. It is flexible but slower on big data, because it runs Python each time.
- Vectorised methods also skip missing values safely. My function would crash on NaN.
- Honest note: for text, the speed gap is smaller than for numbers. On 600,000 text values I measured about 0.15 s for `apply` and 0.19 s for the `.str` chain (timings vary by machine), so apply was not slower here. The real wins are safety with missing values and readability. For number maths (`df["a"] * 2`), vectorising is dramatically faster.
**Sample data:** four department values with spaces and mixed case.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"department": [" hr ", "IT", "Finance ", "hr"]})

def clean_department(text):
    return text.strip().title()

employees["with_apply"] = employees["department"].apply(clean_department)
employees["vectorised"] = employees["department"].str.strip().str.title()
print(employees)
```
**Output:**
```
  department with_apply vectorised
0        hr          Hr         Hr
1         IT         It         It
2   Finance     Finance    Finance
3         hr         Hr         Hr
```
**What it means:** Both give the same answer. With a missing value, `apply` raised `AttributeError: 'float' object has no attribute 'strip'`, while `.str.strip()` returned NaN for it (verified).
**Likely follow-ups:**
- *When is apply the right tool?* Custom rules with several steps or conditions, for example a function that maps a salary to a band.
- *Faster than apply for conditions?* `np.where` or `.loc` filters.
**Common mistakes:** Using `apply(axis=1)` for simple maths (very slow); forgetting the function must `return` a value; not handling NaN inside the function.

### Q56 ⭐ 🟡 How do you remove outliers separately within each group, such as salary outliers per job grade?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that "outlier" depends on the group (a 150k salary is normal for a senior grade, extreme for a junior one)?
**Say this in the interview:** "I calculate Q1, Q3 and the IQR inside each grade using groupby with transform, so every row gets its own grade's limits. Then I keep rows inside the limits."
**Explain simply:**
- **IQR method:** the middle 50% of values sits between Q1 (25th percentile) and Q3 (75th). Anything beyond 1.5 times that spread outside the box is flagged.
- `groupby(...).transform(...)` returns a result the same length as the table, so I can compare row by row.
- One global IQR would flag whole senior grades as outliers, or miss real errors in junior grades.
- Check how many rows get removed before deleting. Sometimes I flag instead of delete.
**Sample data:** 12 employees in two grades, with one extreme value each (90,000 in L1 and 150,000 in L2).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "grade": ["L1"]*6 + ["L2"]*6,
    "salary": [30000, 32000, 31000, 33000, 30500, 90000,
               80000, 82000, 81000, 83000, 79000, 150000],
})

q1 = employees.groupby("grade")["salary"].transform(lambda s: s.quantile(0.25))
q3 = employees.groupby("grade")["salary"].transform(lambda s: s.quantile(0.75))
iqr = q3 - q1

# keep rows inside the limits of their OWN grade
inside = employees["salary"].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
cleaned = employees[inside]
print(cleaned)
print(employees[~inside])
```
**Output:**
```
   grade  salary
0     L1   30000
1     L1   32000
2     L1   31000
3     L1   33000
4     L1   30500
6     L2   80000
7     L2   82000
8     L2   81000
9     L2   83000
10    L2   79000
   grade  salary
5     L1   90000
11    L2  150000
```
**What it means:** One outlier per grade was found. A single global rule would have kept 90,000 (it is below L2's normal pay) and compared grades unfairly.
**Likely follow-ups:**
- *Do you always delete them?* No; first ask whether it is a typo, a real executive salary, or a data error.
**Common mistakes:** Using `groupby().apply` and getting a shorter result that cannot filter the original; tiny groups (with 4 rows, quartiles are unreliable); removing real high earners.

### Q57 ⭐ 🟡 How do you reduce memory by downcasting numeric columns with to_numeric(downcast=...)?
**Asked at:** commonly asked (no company-specific report found); a niche, senior-leaning question.
**What the interviewer is checking:** Do you think about memory when the HR file is huge?
**Say this in the interview:** "By default pandas stores whole numbers in 8 bytes. If the values are small, like ages, `to_numeric(downcast='integer')` picks the smallest integer type that fits, which can cut memory a lot."
**Explain simply:**
- **Downcast** means store the same numbers in a smaller container: int8 holds -128 to 127, int32 holds about plus or minus 2 billion.
- Pandas checks the actual min and max of the column and chooses the smallest safe type.
- `memory_usage(deep=True).sum()` gives total bytes so I can show the saving.
- It only matters for large data (lakhs of rows). For small files, skip it.
**Sample data:** 100,000 rows made by repeating 4 employees, with age, rating, salary.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "age": [29, 41, 35, 52] * 25000,
    "rating": [3, 4, 5, 2] * 25000,
    "salary": [50000, 60000, 72000, 95000] * 25000,
})
before = employees.memory_usage(deep=True).sum()

for column in ["age", "rating", "salary"]:
    employees[column] = pd.to_numeric(employees[column], downcast="integer")

after = employees.memory_usage(deep=True).sum()
print(employees.dtypes)
print(before, after)
```
**Output:**
```
age        int8
rating     int8
salary    int32
dtype: object
2400132 600132
```
**What it means:** Memory fell from about 2.4 MB to 0.6 MB, a 75% saving, with no change to the values.
**Likely follow-ups:**
- *What about text columns?* Convert repeated text to `category` dtype for a similar saving.
- *Risk?* Later maths may overflow a small type (for example summing int8 values), so check before heavy calculations.
**Common mistakes:** Downcasting a column that still contains NaN with `downcast="integer"` (it stays float); downcasting IDs you later join on a differently typed column.

### Q58 ⭐ 🟡 How do you deal with a column that mixes dates in different formats, such as '05-11-2025' and '2025/11/05'?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you notice the day/month ambiguity and choose a safe parsing method?
**Say this in the interview:** "I first agree with the data owner what '05-11-2025' means; in India it is normally 5 November. Then I parse each format on its own with an explicit format and combine the results, rather than letting pandas guess."
**Explain simply:**
- `to_datetime(..., format="%d-%m-%Y")` reads only that pattern: `%d` day, `%m` month, `%Y` four-digit year.
- `errors="coerce"` turns anything that does not match into NaT ("not a time"), so each pass only fills the rows it understands.
- `fillna` merges the passes: the second format fills the gaps left by the first.
- Warning that I found by running it: `format="mixed", dayfirst=True` read '2025/11/05' wrongly as **11 May 2025** (output `2025-05-11`), swapping day and month for year-first dates.
**Sample data:** four join dates in two formats.
**Code (what you write in the interview):**
```python
import pandas as pd

joining = pd.DataFrame({"join_date": ["05-11-2025", "2025/11/05", "12-01-2025", "2025/12/31"]})

day_first = pd.to_datetime(joining["join_date"], format="%d-%m-%Y", errors="coerce")
year_first = pd.to_datetime(joining["join_date"], format="%Y/%m/%d", errors="coerce")
joining["clean_date"] = day_first.fillna(year_first)
print(joining)
```
**Output:**
```
    join_date clean_date
0  05-11-2025 2025-11-05
1  2025/11/05 2025-11-05
2  12-01-2025 2025-01-12
3  2025/12/31 2025-12-31
```
**What it means:** Both spellings of 5 November now give the same date, and every row was parsed. I would check `clean_date.isna().sum()` to catch rows that matched neither format.
**Likely follow-ups:**
- *What if some dates are 12-31-2025 (US order)?* Day 31 and month 12 would fail the day-first pass; I would find these in the leftover NaT rows and handle them separately.
**Common mistakes:** Trusting automatic parsing on ambiguous dates (05-11 versus 11-05 cannot be settled by code); using `dayfirst=True` on year-first text; not counting the NaT rows afterwards.

### Q59 ⭐ 🟡 Why can astype(int) fail with 'Cannot convert non-finite values (NA or inf) to integer', and what is the fix (for example the nullable Int64 type)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand that normal integers cannot hold missing values?
**Say this in the interview:** "A normal int column has no place to store 'missing', so astype(int) fails when there is a NaN. The fix is the nullable Int64 type with a capital I, which keeps whole numbers and allows missing values, or to fill the gaps first."
**Explain simply:**
- NaN is a decimal (float) concept, so a column with missing numbers is float. That is why ages show as 29.0.
- "Non-finite" means NaN or infinity; neither can become a whole number.
- `Int64` (capital I) is pandas' **nullable integer**: whole numbers plus a proper missing marker, `<NA>`.
- Alternatives: fill first (`fillna(0)` only if zero is truthful), or drop the missing rows, or leave it as float.
**Sample data:** 3 employees, one age missing.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"employee_id": [101, 102, 103], "age": [29, None, 41]})

try:
    employees["age"].astype(int)
except Exception as error:
    print(error)

employees["age"] = employees["age"].astype("Int64")
print(employees["age"])
```
**Output:**
```
Cannot convert non-finite values (NA or inf) to integer.Replace or remove non-finite values or cast to an integer typethat supports these values (e.g. 'Int64')
0      29
1    <NA>
2      41
Name: age, dtype: Int64
```
**What it means:** The error is pandas telling us the fix itself. With `Int64`, ages are whole numbers again and the gap is kept honestly as missing.
**Likely follow-ups:**
- *Does the same fix work for text like '29'?* Convert with `pd.to_numeric(..., errors="coerce")` first, then `astype("Int64")`.
- *Why not fillna(0)?* An age of 0 would be a fake value that spoils averages.
**Common mistakes:** Typing `"int64"` in lowercase (that is the normal type and fails the same way); filling with 0 just to make the error go away; values like 29.5 cannot convert to Int64 either.

### Q60 ⭐ 🔴 You get a 5-lakh-row HR file with inconsistent columns, duplicates and blanks. Walk me through your cleaning plan and how you would document every change.
**Asked at:** commonly asked (no company-specific report found); "diagnose before fix" is a theme in prep lists.
**What the interviewer is checking:** Do you work in a disciplined order, keep the raw data safe, and leave an audit trail?
**Say this in the interview:** "I keep the raw file untouched, inspect first, then clean in a fixed order: column names, types, duplicates, text, missing values, outliers. After each step I record what changed and how many rows it touched, so another person can repeat and trust it."
**Explain simply:**
- **Step 0, protect:** never overwrite the raw file; work on a copy and write the code in a script or notebook, not by hand edits.
- **Step 1, inspect:** `info()`, `head()`, `describe()`, `isna().sum()`, `duplicated().sum()`, and `value_counts()` on key columns.
- **Step 2, structure:** tidy column names; fix data types (dates, numbers stored as text).
- **Step 3, duplicates:** exact duplicates first; then duplicates on the business key (employee ID).
- **Step 4, text and placeholders:** trim spaces, fix case and spellings, turn 'N/A' or 999 into NaN.
- **Step 5, missing values:** drop, fill or flag per column, with a reason; agree with the business owner.
- **Step 6, check:** validate with assertions and compare row counts before and after.
- **Documenting:** a **change log** with one line per step (what, how many rows, why), saved next to the clean file, plus the script itself.
**Sample data:** 4 rows with a bad column name, a duplicate row, 'N/A' salary and a missing department.
**Code (what you write in the interview):**
```python
import pandas as pd

raw = pd.DataFrame({
    " Employee ID": [101, 101, 102, 103],
    "Dept Name": ["hr ", "hr ", "IT", None],
    "Salary": ["50,000", "50,000", "N/A", "72,000"],
})
change_log = []

# 1. tidy column names
raw.columns = raw.columns.str.strip().str.lower().str.replace(" ", "_")
change_log.append(f"columns renamed to {list(raw.columns)}")

# 2. remove exact duplicate rows
rows_before = len(raw)
clean = raw.drop_duplicates()
change_log.append(f"duplicates removed: {rows_before - len(clean)}")

# 3. fix text and number types
clean["dept_name"] = clean["dept_name"].str.strip().str.upper()
clean["salary"] = pd.to_numeric(clean["salary"].str.replace(",", ""), errors="coerce")
change_log.append(f"salary set to NaN where not a number: {clean['salary'].isna().sum()}")

# 4. keep a record of what is still missing, then decide with the business
change_log.append(f"missing per column: {clean.isna().sum().to_dict()}")

print(clean)
for line in change_log:
    print(line)
```
**Output:**
```
   employee_id dept_name   salary
0          101        HR  50000.0
2          102        IT      NaN
3          103       NaN  72000.0
columns renamed to ['employee_id', 'dept_name', 'salary']
duplicates removed: 1
salary set to NaN where not a number: 1
missing per column: {'employee_id': 0, 'dept_name': 1, 'salary': 1}
```
**What it means:** 4 rows became 3, and the log says exactly why. In the real project the log would be saved to a file and shared with the business owner.
**Likely follow-ups:**
- *Five lakh rows: any speed concern?* Use vectorised methods, read only needed columns, convert repeated text to `category`; 5 lakh rows fits in memory comfortably on a normal laptop (from memory, unverified).
- *Who approves the fill/drop rules?* The data owner, for example HR operations.
**Common mistakes:** Cleaning the original file in place; deleting rows silently; fixing in Excel by hand with no record; not checking row counts at the end.

### Q61 ⭐ 🔴 How do you build a reusable data-cleaning function or pipeline in pandas using pipe()?
**Asked at:** commonly asked (no company-specific report found); a niche, senior-leaning question.
**What the interviewer is checking:** Can you turn one-off cleaning into small reusable, ordered steps?
**Say this in the interview:** "I write one small function per cleaning step, each taking a DataFrame and returning a DataFrame. Then I chain them with pipe, so the cleaning reads like a recipe and I can reuse it next month on a new file."
**Explain simply:**
- **pipe(function)** passes the DataFrame into my function, so `df.pipe(f)` is the same as `f(df)` but chains neatly left to right.
- Small functions are easy to test and to reuse; order of steps is visible at a glance.
- Each function starts with `df.copy()` so it never changes the caller's data by surprise.
- Standard methods like `drop_duplicates()` can sit in the same chain.
**Sample data:** 3 rows with a spaced column name, a duplicate and an 'N/A' salary.
**Code (what you write in the interview):**
```python
import pandas as pd

raw = pd.DataFrame({
    " Employee ID": [101, 101, 102],
    "Dept": ["hr ", "hr ", "it"],
    "Salary": ["50,000", "50,000", "N/A"],
})

def clean_columns(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def fix_types(df):
    df = df.copy()
    df["dept"] = df["dept"].str.strip().str.upper()
    df["salary"] = pd.to_numeric(df["salary"].str.replace(",", ""), errors="coerce")
    return df

clean = (
    raw
    .pipe(clean_columns)
    .pipe(fix_types)
    .drop_duplicates()
)
print(clean)
```
**Output:**
```
   employee_id dept   salary
0          101   HR  50000.0
2          102   IT      NaN
```
**What it means:** Three messy rows became two clean ones, and the steps are named and reusable on any file with the same layout.
**Likely follow-ups:**
- *Extra arguments?* `df.pipe(function, argument)` passes them on.
- *Why not one giant function?* Hard to test and to read; small steps can be reordered or reused.
**Common mistakes:** A function that forgets to `return df`; changing the input in place; hard-coding column names that differ between files (check columns exist first).

### Q62 ⭐ 🔴 How do you validate the data after cleaning, using assertions and simple quality checks?
**Asked at:** commonly asked (no company-specific report found); a niche, senior-leaning question.
**What the interviewer is checking:** Do you prove the data is clean, rather than assume?
**Say this in the interview:** "After cleaning I write checks that must be true: IDs are unique, no missing salaries, salaries positive, departments from the approved list. An assert stops the script with a clear message if any rule breaks, so bad data never reaches the dashboard."
**Explain simply:**
- **assert** is a Python statement: `assert condition, "message"`. If the condition is False, the program stops and shows the message.
- `.all()` turns a column of True/False into one answer: True only if every row passes.
- Simple quality checks beyond asserts: row counts before and after, `describe()` for sanity (min and max), and `isna().sum()`.
- Asserts guard against rules I can state; `describe()` and eyeballing catch the surprises.
**Sample data:** 3 clean employee records.
**Code (what you write in the interview):**
```python
import pandas as pd

clean = pd.DataFrame({
    "employee_id": [101, 102, 103],
    "salary": [50000, 62000, 72000],
    "department": ["HR", "IT", "IT"],
})

assert clean["employee_id"].is_unique, "duplicate employee IDs"
assert clean["salary"].notna().all(), "missing salaries"
assert (clean["salary"] > 0).all(), "non-positive salaries"
assert clean["department"].isin(["HR", "IT", "Finance"]).all(), "unknown department"

print("all checks passed")
print(clean.describe())
```
**Output:**
```
all checks passed
       employee_id        salary
count          3.0      3.000000
mean         102.0  61333.333333
std            1.0  11015.141095
min          101.0  50000.000000
25%          101.5  56000.000000
50%          102.0  62000.000000
75%          102.5  67000.000000
max          103.0  72000.000000
```
**What it means:** Every rule passed. When I tried a salary of -5, the assert stopped with `AssertionError: non-positive salaries` (verified), which is exactly the safety net we want.
**Likely follow-ups:**
- *Do asserts always run?* Not if Python is run with the `-O` option (from memory, unverified), so for production pipelines people often raise an explicit error instead.
- *Any library?* Tools such as pandera or Great Expectations exist (not run here).
**Common mistakes:** Forgetting `.all()` (an assert on a whole column is an error); checking only the shape; assuming a missing salary slips through `salary > 0`: it does not, because `NaN > 0` is False, so the check fails (but add the explicit `notna()` check for a clearer message).

### Q63 ⭐ 🔴 How do you detect outliers in a column that is highly skewed, such as salary, and why might a log transform help?
**Asked at:** a candidate-reported "write a Python function that detects outliers using the IQR method" question appears on Glassdoor (snippet only, company not confirmed); otherwise commonly asked.
**What the interviewer is checking:** Do you know the IQR rule misbehaves on skewed data, and that a transform can fix it?
**Say this in the interview:** "Salary is right-skewed: many ordinary salaries and a long tail of very high ones. Plain IQR flags too many high earners. I take the log first, run IQR on the logged values, and only the truly extreme ones remain. Then I decide whether to keep, cap or remove them."
**Explain simply:**
- **Skewed** means the data is lopsided; a few huge values drag the right tail out.
- A **log transform** compresses large numbers more than small ones, turning "multiply by 2" into "add a fixed amount", which makes the data more symmetric.
- On symmetric data, the IQR and z-score rules work properly.
- Log needs positive numbers only (use `np.log1p` if zeros exist).
- Detect on the logged scale, but report outliers in the original salary values.
**Sample data:** 12 salaries from 30,000 to 900,000.
**Code (what you write in the interview):**
```python
import pandas as pd
import numpy as np

salaries = pd.Series([30000, 35000, 40000, 45000, 52000, 60000, 75000, 95000, 130000, 200000, 350000, 900000])

def iqr_outliers(values):
    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1
    return (values < q1 - 1.5 * iqr) | (values > q3 + 1.5 * iqr)

print("raw salary outliers:", salaries[iqr_outliers(salaries)].tolist())

log_salaries = np.log(salaries)
print("log salary outliers:", salaries[iqr_outliers(log_salaries)].tolist())
print("skew before and after:", round(salaries.skew(), 2), round(log_salaries.skew(), 2))
```
**Output:**
```
raw salary outliers: [350000, 900000]
log salary outliers: [900000]
skew before and after: 2.75 1.14
```
**What it means:** On the raw scale, 350,000 is also flagged, even though it may be a normal senior salary. After the log, only 900,000 stands out. Skew (0 means symmetric) dropped from 2.75 to 1.14.
**Likely follow-ups:**
- *Other options?* Compare within job grade (see the per-group question), or use percentiles (top 1%).
- *Do you delete the 900,000 row?* Not before checking whether it is a typo (extra zero) or a real executive pay.
**Common mistakes:** Applying the log to zero or negative values (gives -inf or NaN); reporting log values to stakeholders instead of rupees; removing high earners that are legitimate.

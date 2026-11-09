# Book 3 — Python & pandas for Analysts | Part 4: pandas: read, select, filter, sort 🟢

**Target:** 70 questions | **Actual:** 75 questions
**Scope:** loading data with pandas, inspecting it, selecting columns and rows (loc/iloc), filtering, sorting and basic column creation, plus common errors; groupby, merge, cleaning and dates are in other parts.

### Q1 ⭐⭐⭐ 🟢 What is pandas, and what is the difference between a Series and a DataFrame?
**Asked at:** commonly asked (no company-specific report found); a Tiger Analytics candidate report (via a search summary) lists "what is a DataFrame in pandas" as an opening question, and Adaface lists Series vs DataFrame as an early question.
**What the interviewer is checking:** Whether you know the two basic pandas building blocks in plain words.
**Say this in the interview:** "Pandas is the Python library for working with table-like data. A DataFrame is the whole table with rows and columns, like an Excel sheet. A Series is one single column of that table."
**Explain simply:**
- Library: a ready-made toolbox of code that someone else wrote. You load it with `import pandas as pd`.
- DataFrame: a 2-dimensional table. Every column has a name and its own data type (numbers, text, dates).
- Series: a 1-dimensional list of values with an index (the row labels) and a name. Picking one column out of a DataFrame gives you a Series.
- Think of it as: DataFrame = worksheet, Series = one column of the worksheet.
**Sample data:** `employees.csv` has 8 rows and the columns employee_id, name, department, salary.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("employees.csv")

# One column of the table is a Series
salary = employees["salary"]

print(type(employees).__name__)
print(type(salary).__name__)
print(salary.head(3))
```
**Output:**
```text
DataFrame
Series
0    40000
1    35000
2    60000
Name: salary, dtype: int64
```
**What it means:** The whole table is a DataFrame; the single `salary` column is a Series with the row numbers (0, 1, 2) as its index.
**Likely follow-ups:**
- *Why use pandas instead of Excel?* It handles millions of rows, repeats the same steps on new files, and keeps your steps written down.
- *Can a DataFrame have one column?* Yes, `df[["salary"]]` is still a DataFrame (see Q21 in this part).
**Common mistakes:** Saying a Series is "a row" (it can be, but usually it is a column); forgetting that every column in a DataFrame is a Series.

### Q2 ⭐⭐⭐ 🟢 How do you read a CSV file into a pandas DataFrame, and how do you read an Excel sheet?
**Asked at:** commonly asked (no company-specific report found); `read_csv` is in the DataCamp and AskPython pandas question sets.
**What the interviewer is checking:** That you know the loading functions and the `sheet_name` option.
**Say this in the interview:** "`pd.read_csv('file.csv')` for a CSV and `pd.read_excel('file.xlsx', sheet_name='Jan')` for an Excel sheet. Both return a DataFrame."
**Explain simply:**
- CSV means "comma separated values": a plain text file where each line is a row and commas separate the columns.
- `read_excel` needs a helper library called `openpyxl` installed for `.xlsx` files.
- If you skip `sheet_name`, pandas reads the first sheet only.
- Always look at the result with `head()` straight after loading.
**Sample data:** `employees.csv` (same 8-row file as Q1), and an Excel file `employees.xlsx` with a sheet named `Jan` holding the same rows.
**Code (what you write in the interview):**
```python
import pandas as pd

# Read a CSV file
employees = pd.read_csv("employees.csv")

# Read one sheet from an Excel file
january_employees = pd.read_excel("employees.xlsx", sheet_name="Jan")

print(employees.head(3))
```
**Output:**
```text
   employee_id   name department  salary
0          101   Asha      Sales   40000
1          102   Ravi         HR   35000
2          103  Meena    Finance   60000
```
**What it means:** The file is now a table in memory that we can filter, sort and summarise.
**Likely follow-ups:**
- *What if the file uses semicolons or tabs?* Add `sep=";"` or `sep="\t"`.
- *How do you read all sheets?* `sheet_name=None` returns a dictionary of DataFrames.
**Common mistakes:** Wrong file path (run the code from the folder that holds the file, or give the full path); forgetting `openpyxl`; assuming Excel reads every sheet by default.

### Q3 ⭐⭐⭐ 🟢 Write code to load an employee CSV file and look at the first 5 and last 5 rows.
**Asked at:** commonly asked (no company-specific report found); a basic live-coding warm-up.
**What the interviewer is checking:** That you load data and do a quick sanity check before any analysis.
**Say this in the interview:** "I load it with `read_csv`, then use `head()` for the first 5 rows and `tail()` for the last 5. The default for both is 5."
**Explain simply:**
- `head()` shows the top of the table, `tail()` shows the bottom.
- Looking at the bottom matters because broken files often have a "Total" row or blank rows at the end.
- Pass a number to change it: `head(10)`.
**Sample data:** `employees.csv` with 8 rows (IDs 101 to 108).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("employees.csv")

# First 5 rows
print(employees.head())

# Last 5 rows
print(employees.tail())
```
**Output:**
```text
   employee_id   name department  salary
0          101   Asha      Sales   40000
1          102   Ravi         HR   35000
2          103  Meena    Finance   60000
3          104  Karan      Sales   45000
4          105   Anil    Finance   55000
   employee_id   name department  salary
3          104  Karan      Sales   45000
4          105   Anil    Finance   55000
5          106   Sara         IT   70000
6          107    Dev         HR   38000
7          108  Priya      Sales   52000
```
**What it means:** Both views look sensible, so the file loaded correctly. With only 8 rows the two views overlap (rows 3 and 4 appear in both).
**Likely follow-ups:**
- *How to see a random sample?* `employees.sample(5)`.
- *How to see only 3 rows?* `employees.head(3)`.
**Common mistakes:** Forgetting the brackets (`employees.head` without `()` prints the method, not the rows); never checking the tail.

### Q4 ⭐⭐⭐ 🟢 How do you check the number of rows and columns of a DataFrame?
**Asked at:** commonly asked (no company-specific report found); GoLinuxCloud notes interviewers expect you to check row counts after each step.
**What the interviewer is checking:** That you use `shape` and know it has no brackets.
**Say this in the interview:** "`df.shape` gives a pair: rows first, then columns. `len(df)` gives just the number of rows."
**Explain simply:**
- `shape` is an attribute (a stored property), so no brackets. It returns a tuple, which is a fixed pair like `(8, 4)`.
- You can unpack it into two named variables.
- Check `shape` before and after a filter to see how many rows you removed.
**Sample data:** `employees.csv` (8 rows, 4 columns).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("employees.csv")

print(employees.shape)

# Split the pair into two named numbers
number_of_rows, number_of_columns = employees.shape
print(number_of_rows, number_of_columns)

# Rows only
print(len(employees))
```
**Output:**
```text
(8, 4)
8 4
8
```
**What it means:** 8 employees and 4 columns of information about each.
**Likely follow-ups:**
- *Does shape count the header row?* No, the header is the column names, not data.
- *How many cells?* `employees.size` (rows times columns).
**Common mistakes:** Writing `shape()` with brackets (error: tuple is not callable); mixing up the order (rows first, columns second).

### Q5 ⭐⭐⭐ 🟢 How do you quickly see column names, data types and non-null counts of a DataFrame using info()?
**Asked at:** commonly asked (no company-specific report found); `info()` is standard in pandas first-look checklists.
**What the interviewer is checking:** That you can spot missing values and wrong data types in one call.
**Say this in the interview:** "`df.info()` prints each column name, how many non-null (non-missing) values it has, and its data type. If a count is lower than the total rows, that column has missing values."
**Explain simply:**
- Non-null count: how many cells actually hold a value. Missing cells are shown as NaN (not a number) or None.
- Compare each count with the row count at the top ("8 entries"). A gap means missing data.
- The Dtype column shows whether something that should be a number was read as text.
- `info()` prints directly, so do not wrap it in `print()`.
**Sample data:** The 8-row employee file, where Meena's department was left blank.
**Code (what you write in the interview):**
```python
employees.info()
```
**Output:**
```text
<class 'pandas.DataFrame'>
RangeIndex: 8 entries, 0 to 7
Data columns (total 4 columns):
 #   Column       Non-Null Count  Dtype
---  ------       --------------  -----
 0   employee_id  8 non-null      int64
 1   name         8 non-null      str  
 2   department   7 non-null      str  
 3   salary       8 non-null      int64
dtypes: int64(2), str(2)
memory usage: 388.0 bytes
```
**What it means:** `department` has 7 values out of 8 rows, so one is missing. `salary` is numeric, which is what we want.
**Likely follow-ups:**
- *How do you count missing values per column?* `employees.isna().sum()`.
- *How is info() different from describe()?* `info()` is about structure and missing data; `describe()` gives statistics of numeric columns.
**Common mistakes:** Writing `print(df.info())` (adds a stray `None`); ignoring a numeric column showing a text dtype. Note: on pandas 3 text columns show as `str`; on pandas 2 they show as `object`.

### Q6 ⭐⭐⭐ 🟢 How do you select a single column and multiple columns from a DataFrame?
**Asked at:** commonly asked (no company-specific report found); a core filter-and-select basic in every pandas guide.
**What the interviewer is checking:** Single brackets vs double brackets, and what each returns.
**Say this in the interview:** "One column: `df['salary']`, which gives a Series. Several columns: pass a list, `df[['name', 'salary']]`, which gives a DataFrame."
**Explain simply:**
- Single brackets with one name return one column (a Series).
- Double brackets: the inner brackets are a Python list of names, the outer brackets are the selection. Result stays a table.
- The order in your list is the order of the columns in the result.
**Sample data:** The 8-row `employees` table.
**Code (what you write in the interview):**
```python
# One column
names = employees["name"]

# Several columns (note the double brackets)
names_and_salaries = employees[["name", "salary"]]

print(names.head(3))
print(names_and_salaries.head(3))
```
**Output:**
```text
0     Asha
1     Ravi
2    Meena
Name: name, dtype: str
    name  salary
0   Asha   40000
1   Ravi   35000
2  Meena   60000
```
**What it means:** The first is a single list of names; the second is a small two-column table.
**Likely follow-ups:**
- *What about `df.name`?* Works for simple names but fails with spaces, and clashes with built-in attributes; use brackets.
- *Single column but keep it a table?* `df[["name"]]`.
**Common mistakes:** `df["name", "salary"]` (KeyError, needs a list); a typo or extra space in the column name.

### Q7 ⭐⭐⭐ 🟢 What is the difference between loc and iloc in pandas?
**Asked at:** commonly asked (no company-specific report found); loc vs iloc is in the DataCamp pandas set.
**What the interviewer is checking:** Label-based vs position-based selection, and the slicing difference.
**Say this in the interview:** "`loc` selects by label, meaning the index value and column name. `iloc` selects by integer position, counting from 0. The `i` stands for integer."
**Explain simply:**
- Label: the name written on the row or column. If employee_id is the index, label 103 is Meena's row.
- Position: the order number, starting at 0, no matter what the label is.
- `loc` slices include the end label; `iloc` slices exclude the end position (see Q37 in this part).
- Both use `[rows, columns]`.
**Sample data:** The `employees` table with `employee_id` set as the index.
**Code (what you write in the interview):**
```python
employees_by_id = employees.set_index("employee_id")

# By label: the row whose employee_id is 103
print(employees_by_id.loc[103])

# By position: the third row (counting from 0)
print(employees_by_id.iloc[2])

# Labels 102 to 104, two columns by name
print(employees_by_id.loc[102:104, ["name", "salary"]])
```
**Output:**
```text
name            Meena
department    Finance
salary          60000
Name: 103, dtype: object
name            Meena
department    Finance
salary          60000
Name: 103, dtype: object
              name  salary
employee_id                
102           Ravi   35000
103          Meena   60000
104          Karan   45000
```
**What it means:** Label 103 and position 2 happen to be the same row here, but only because we counted the position. The slice `102:104` returned three rows, including 104.
**Likely follow-ups:**
- *When do the two give different rows?* Whenever the index is not 0, 1, 2... for example after filtering or with employee IDs.
- *Can loc filter with a condition?* Yes, `df.loc[df["salary"] > 50000, "name"]`.
**Common mistakes:** Using `iloc` with a label, or `loc` with a position after the index changed; expecting `loc` slices to stop before the end.

### Q8 ⭐⭐⭐ 🟢 Write code to filter an employee DataFrame to show only employees from the Sales department.
**Asked at:** commonly asked (no company-specific report found); the classic boolean-filter task in pandas screens.
**What the interviewer is checking:** That you can write a condition and use it to pick rows.
**Say this in the interview:** "I write a True/False condition for each row, `employees['department'] == 'Sales'`, and pass it inside square brackets, which keeps only the True rows."
**Explain simply:**
- The comparison gives a column of True and False, one per row. This is called a boolean mask.
- Putting the mask in `employees[...]` keeps only the rows marked True.
- `==` compares; a single `=` assigns, so do not mix them up.
- Text must match exactly, including capital letters.
**Sample data:** The 8-row `employees` table (3 Sales employees).
**Code (what you write in the interview):**
```python
sales_employees = employees[employees["department"] == "Sales"]

print(sales_employees)
```
**Output:**
```text
   employee_id   name department  salary
0          101   Asha      Sales   40000
3          104  Karan      Sales   45000
7          108  Priya      Sales   52000
```
**What it means:** Three of the 8 employees are in Sales. The original row numbers (0, 3, 7) are kept.
**Likely follow-ups:**
- *Why are the row numbers 0, 3, 7?* The index travels with the rows; use `reset_index(drop=True)` for a fresh count.
- *What about "sales" in lowercase or with spaces?* It would not match; clean with `str.strip().str.lower()` first.
**Common mistakes:** Using `=` instead of `==`; forgetting quotes around Sales; expecting the original table to change (filtering makes a new table).

### Q9 ⭐⭐⭐ 🟢 Write code to sort an employee DataFrame by salary from highest to lowest.
**Asked at:** commonly asked (no company-specific report found); sorting DataFrames is a named coding task in Interview Kickstart's pandas guide.
**What the interviewer is checking:** `sort_values` and the `ascending` flag.
**Say this in the interview:** "`employees.sort_values('salary', ascending=False)`. The default is low to high, so I turn ascending off for highest first."
**Explain simply:**
- `sort_values` orders the rows by one or more columns.
- `ascending=False` means biggest first.
- It returns a new sorted table; the original is unchanged unless you save the result.
- Missing values go to the end by default.
**Sample data:** The 8-row `employees` table.
**Code (what you write in the interview):**
```python
employees_by_salary = employees.sort_values("salary", ascending=False)

print(employees_by_salary)
```
**Output:**
```text
   employee_id   name department  salary
5          106   Sara         IT   70000
2          103  Meena    Finance   60000
4          105   Anil    Finance   55000
7          108  Priya      Sales   52000
3          104  Karan      Sales   45000
0          101   Asha      Sales   40000
6          107    Dev         HR   38000
1          102   Ravi         HR   35000
```
**What it means:** Sara earns the most (70,000) and Ravi the least (35,000).
**Likely follow-ups:**
- *How do you sort by two columns?* See Q15 in this part.
- *Just the top 5?* `nlargest(5, "salary")`.
**Common mistakes:** Writing `df.sort_values("salary")` and expecting it to be high to low; not saving the result; the old `inplace=True` habit (avoid it, assign instead).

### Q10 ⭐⭐⭐ 🟢 How do you add a new column to a DataFrame, for example annual salary from monthly salary?
**Asked at:** commonly asked (no company-specific report found); creating a column from existing ones is in Adaface's pandas set.
**What the interviewer is checking:** That you know column maths works on the whole column at once.
**Say this in the interview:** "I assign to a new column name: `df['annual_salary'] = df['monthly_salary'] * 12`. Pandas does the maths for every row at once."
**Explain simply:**
- Assigning to a column name that does not exist creates it; if it exists, it overwrites it.
- Maths on a column is applied row by row automatically, so no loop is needed (this is called vectorised).
- You can combine columns too: `df['a'] + df['b']`.
**Sample data:**

| name | monthly_salary |
|---|---|
| Asha | 40000 |
| Ravi | 35000 |
| Meena | 60000 |

**Code (what you write in the interview):**
```python
payroll["annual_salary"] = payroll["monthly_salary"] * 12

print(payroll)
```
**Output:**
```text
    name  monthly_salary  annual_salary
0   Asha           40000         480000
1   Ravi           35000         420000
2  Meena           60000         720000
```
**What it means:** Each employee now has a yearly figure next to the monthly one.
**Likely follow-ups:**
- *Add a column based on a condition?* `np.where(df["salary"] > 50000, "High", "Normal")`.
- *Add it as a copy, not changing the original?* `df.assign(annual_salary=df["monthly_salary"] * 12)`.
**Common mistakes:** Using a loop for something one line can do; misspelling the existing column; adding a column to a filtered slice (see Q16 in this part).

### Q11 ⭐⭐⭐ 🟢 How do you check the data type of each column, and what does the 'object' dtype mean?
**Asked at:** commonly asked (no company-specific report found); a standard data-inspection question.
**What the interviewer is checking:** That you can read dtypes and know 'object' usually means text (or mixed values).
**Say this in the interview:** "`df.dtypes` lists each column with its type. `object` is the general-purpose type pandas uses for text, and also for columns that mix numbers and text. On the newest pandas, plain text shows as `str`."
**Explain simply:**
- dtype means data type: `int64` whole numbers, `float64` decimals, `datetime64` dates, `bool` True/False.
- `object` is a "container" type that can hold anything, mostly Python strings. A numeric column that shows `object` usually has stray text in it (like "N/A" or "40,000").
- Wrong dtype breaks maths and sorting, so check it first.
- Version note (verified by running on pandas 3.0.5): text columns display as `str`. On pandas 2.x and earlier the same columns display as `object`.
**Sample data:** The 8-row `employees` table.
**Code (what you write in the interview):**
```python
print(employees.dtypes)
```
**Output:**
```text
employee_id    int64
name             str
department       str
salary         int64
dtype: object
```
**What it means:** IDs and salary are numbers, name and department are text. Salary being a number means we can add, average and compare it.
**Likely follow-ups:**
- *How do you change a type?* `df["salary"] = df["salary"].astype(int)`, or `pd.to_numeric(..., errors="coerce")` for messy values.
- *Why is a numeric column object?* Usually a text entry like "N/A" or a comma in the number.
**Common mistakes:** Saying object means "object-oriented"; not noticing that numbers stored as text sort as text ("100" before "20").

### Q12 ⭐⭐⭐ 🟢 Write code to filter rows where the department is Sales, HR or Finance using isin().
**Asked at:** commonly asked (no company-specific report found); a frequent follow-up to basic filtering.
**What the interviewer is checking:** That you use `isin()` instead of a long chain of `or` conditions.
**Say this in the interview:** "`df['department'].isin(['Sales', 'HR', 'Finance'])` gives True for any row whose department is in that list. I pass it inside the square brackets to keep those rows."
**Explain simply:**
- `isin` means "is this value in my list?". The list goes in square brackets.
- It replaces writing `== "Sales" | == "HR" | == "Finance"`, which is long and bracket-heavy.
- Spelling and capitalisation must match exactly.
**Sample data:** The 8-row `employees` table (departments: Sales, HR, Finance, IT).
**Code (what you write in the interview):**
```python
selected_departments = ["Sales", "HR", "Finance"]

selected_employees = employees[employees["department"].isin(selected_departments)]

print(selected_employees)
```
**Output:**
```text
   employee_id   name department  salary
0          101   Asha      Sales   40000
1          102   Ravi         HR   35000
2          103  Meena    Finance   60000
3          104  Karan      Sales   45000
4          105   Anil    Finance   55000
6          107    Dev         HR   38000
7          108  Priya      Sales   52000
```
**What it means:** Seven rows remain; only Sara (IT, row 5) was dropped.
**Likely follow-ups:**
- *How to exclude those departments?* Put `~` before the condition (see Q39 in this part).
- *Does isin handle missing values?* A missing value is never "in" the list, so that row is dropped.
**Common mistakes:** Passing the values without a list (`isin("Sales", "HR")` is an error); using `in` instead of `isin`.

### Q13 ⭐⭐⭐ 🟡 Write code to filter employees with salary above 50,000 who are also in the Finance department. Why do you need brackets around each condition?
**Asked at:** commonly asked (no company-specific report found); multi-condition filtering is a standard medium-level pandas task.
**What the interviewer is checking:** `&` for "and" and the bracket rule caused by operator precedence.
**Say this in the interview:** "I join the two conditions with `&` and put each condition in its own brackets. Without brackets, Python evaluates `&` before `>` and `==`, and the code fails."
**Explain simply:**
- `&` means "and" (both must be true), `|` means "or", `~` means "not".
- Operator precedence is the order Python does things in. `&` ranks higher than `>` and `==`, so `salary > 50000 & dept == "Finance"` is read as `50000 & dept`, which makes no sense.
- Brackets force each comparison to finish first.
**Sample data:** The 8-row `employees` table.
**Code (what you write in the interview):**
```python
high_paid_finance = employees[(employees["salary"] > 50000) & (employees["department"] == "Finance")]

print(high_paid_finance)
```
**Output:**
```text
   employee_id   name department  salary
2          103  Meena    Finance   60000
4          105   Anil    Finance   55000
```
**What it means:** Meena and Anil are the Finance employees paid above 50,000. Without brackets the code stops with: `TypeError: unsupported operand type(s) for &: 'int' and 'StringArray'` (as seen on pandas 3.0.5; the exact wording differs by version).
**Alternative:** `employees.query("salary > 50000 and department == 'Finance'")` needs no brackets and reads like English.
**Likely follow-ups:**
- *How do you write "or"?* Use `|` with the same brackets.
- *Is 50,000 itself included?* No, `>` is strictly above; use `>=` to include it.
**Common mistakes:** Forgetting brackets; using `and` (see Q14); writing the department without quotes.

### Q14 ⭐⭐⭐ 🟡 What is the difference between using 'and' and '&' when filtering a DataFrame, and what error do you get if you use 'and'?
**Asked at:** commonly asked (no company-specific report found); a classic pandas trap question.
**What the interviewer is checking:** That you know `and` works on single True/False values, while `&` works row by row.
**Say this in the interview:** "`and` is for one True or False. A filter has a whole column of True/False values, so I need `&`, which compares row by row. Using `and` gives `ValueError: The truth value of a Series is ambiguous`."
**Explain simply:**
- Python's `and` needs a single yes/no answer. A column of 8 answers is ambiguous: is it true if all are true? any?
- `&` is the element-wise "and": it checks row 1 with row 1, row 2 with row 2, and so on.
- Same story: `or` fails, use `|`; `not` fails, use `~`.
- The error message itself suggests `.any()` or `.all()`, but for a filter that is not what you want.
**Sample data:** The 8-row `employees` table.
**Code (what you write in the interview):**
```python
# Wrong: raises an error
employees[(employees["salary"] > 50000) and (employees["department"] == "Finance")]

# Right: row by row
employees[(employees["salary"] > 50000) & (employees["department"] == "Finance")]
```
**Output:**
```text
ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
```
(The correct line prints the two Finance rows shown in Q13.)
**What it means:** The error is pandas refusing to guess; switching to `&` fixes it.
**Likely follow-ups:**
- *Why not `.all()`?* That collapses the whole column to one answer, losing the row-wise filter.
- *Does `&` need brackets?* Yes (Q13).
**Common mistakes:** Using `and`/`or`/`not` in filters; forgetting brackets after switching to `&`.

### Q15 ⭐⭐⭐ 🟡 Write code to sort a DataFrame by department (A to Z) and then by salary (high to low) within each department.
**Asked at:** commonly asked (no company-specific report found); sorting tasks appear in Interview Kickstart's pandas coding list.
**What the interviewer is checking:** Sorting by two columns with a different direction for each.
**Say this in the interview:** "I pass a list of columns to `sort_values` and a matching list for `ascending`: True for department, False for salary."
**Explain simply:**
- The first column is the main sort; the second only breaks ties within the same first value.
- `ascending=[True, False]` lines up one-to-one with the column list.
- Both lists must be the same length.
**Sample data:** The 8-row `employees` table.
**Code (what you write in the interview):**
```python
sorted_employees = employees.sort_values(
    ["department", "salary"],
    ascending=[True, False],
)

print(sorted_employees)
```
**Output:**
```text
   employee_id   name department  salary
2          103  Meena    Finance   60000
4          105   Anil    Finance   55000
6          107    Dev         HR   38000
1          102   Ravi         HR   35000
5          106   Sara         IT   70000
7          108  Priya      Sales   52000
3          104  Karan      Sales   45000
0          101   Asha      Sales   40000
```
**What it means:** Departments run A to Z (Finance, HR, IT, Sales) and inside each one the highest salary is first.
**Likely follow-ups:**
- *Tidy row numbers?* Add `.reset_index(drop=True)`.
- *Top earner per department?* That needs `groupby`, covered in another part.
**Common mistakes:** Passing a single `ascending=False` (flips both columns); mismatched list lengths; swapping the column order, which changes the result.

### Q16 ⭐⭐⭐ 🟡 What does SettingWithCopyWarning mean, and how do you avoid it?
**Asked at:** commonly asked (no company-specific report found); a staple pandas question in prep guides.
**What the interviewer is checking:** That you understand views vs copies and know the safe habit.
**Say this in the interview:** "It warns that I am changing a slice that may be a copy of my data, so the change might not reach the original table. I avoid it by taking an explicit `.copy()` of a filtered slice, or by using `.loc` to set values. In pandas 3 with Copy-on-Write, the warning is gone and a filtered result is always its own copy."
**Explain simply:**
- Filtering creates a new table. Older pandas could not always tell whether it was a separate copy or a window onto the original, so it warned you.
- Safe habit 1: `sales = df[df["department"] == "Sales"].copy()`, then edit `sales` freely.
- Safe habit 2: to change the original, use `df.loc[condition, "column"] = value` in one step.
- Version note (verified by running on pandas 3.0.5): no warning appears and the original is untouched. On pandas 2.x and earlier, the same line printed the warning. From memory, unverified here.
**Sample data:** The 8-row `employees` table.
**Code (what you write in the interview):**
```python
# Safe: make an independent copy of the slice, then edit it
sales_employees = employees[employees["department"] == "Sales"].copy()
sales_employees["bonus"] = sales_employees["salary"] * 0.1

# Or change the original table directly with loc
employees.loc[employees["department"] == "Sales", "bonus"] = employees["salary"] * 0.1

print(sales_employees)
print(employees.head(3))
```
**Output:**
```text
   employee_id   name department  salary   bonus
0          101   Asha      Sales   40000  4000.0
3          104  Karan      Sales   45000  4500.0
7          108  Priya      Sales   52000  5200.0
   employee_id   name department  salary   bonus
0          101   Asha      Sales   40000  4000.0
1          102   Ravi         HR   35000     NaN
2          103  Meena    Finance   60000     NaN
```
**What it means:** The copy holds the Sales bonuses; the original table got a bonus column filled only for Sales (NaN, meaning blank, for the rest).
**Likely follow-ups:**
- *Does chained indexing like `df[a][b] = x` work?* Avoid it: it is unreliable in old pandas and does not modify the original in pandas 3.
- *Should I hide the warning?* No, fix the cause.
**Common mistakes:** Silencing the warning instead of fixing the code; editing a filtered slice and expecting the original to change; assuming `.copy()` is needed in every case (it is not needed when you only read).

### Q17 ⭐⭐⭐ 🟡 You get KeyError when selecting a column that clearly exists in your CSV. What are the common causes and how do you fix them?
**Asked at:** commonly asked (no company-specific report found); a practical debugging question for messy real-world files.
**What the interviewer is checking:** That you debug by printing the real column names instead of trusting what you see.
**Say this in the interview:** "First I print `df.columns` to see what pandas actually read. The usual causes are hidden spaces, different capital letters, a wrong header row, or a different delimiter. I clean the names and select again."
**Explain simply:**
- KeyError means pandas could not find that exact name. It compares characters, so `"salary "` (with a trailing space) is a different name from `"salary"`.
- Common causes: trailing or leading spaces; upper vs lower case (`Salary`); hidden BOM character at the start of the first column (`﻿employee_id`, from Excel-saved files; fix with `encoding="utf-8-sig"`); header not on the first line (use `header=`/`skiprows=`); wrong separator so everything is in one column (use `sep=`); simple typo.
- Fix names once after loading, then use the cleaned names everywhere.
**Sample data:** A CSV whose header line is `employee_id,name,department,salary ` (note the space after salary).
**Code (what you write in the interview):**
```python
staff = pd.read_csv("staff.csv")

# See exactly what pandas read
print(staff.columns.tolist())

# Remove stray spaces from all column names, then select
staff.columns = staff.columns.str.strip()
print(staff["salary"].tolist())
```
**Output:**
```text
['employee_id', 'name', 'department', 'salary ']
[40000, 35000]
```
**What it means:** The list shows `'salary '` with a hidden space. After stripping, `staff["salary"]` works. Before the fix, `staff["salary"]` raised `KeyError: 'salary'`.
**Alternative:** To make names consistent in one go: `staff.columns = staff.columns.str.strip().str.lower()`.
**Likely follow-ups:**
- *How can you avoid it?* Standardise the column names right after reading.
- *Why does `df.columns` show a single odd column?* Probably the wrong `sep`.
**Common mistakes:** Retyping the same name and hoping; not looking at `df.columns`; forgetting that Excel exports add hidden characters.

### Q18 ⭐⭐ 🟢 How do you rename columns in a DataFrame?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** `rename` with a dictionary vs replacing all names.
**Say this in the interview:** "`df.rename(columns={'old': 'new'})` for specific columns. To replace every name, assign a full list to `df.columns`."
**Explain simply:**
- A dictionary is a set of `old name: new name` pairs written in curly brackets.
- `rename` changes only the columns you list and leaves others alone.
- Assigning to `df.columns` needs exactly one new name per column, in order.
- Good names are short, lower case, no spaces: `monthly_salary`, not `Monthly Salary (INR)`.
**Sample data:** `employees.csv` (columns employee_id, name, department, salary).
**Code (what you write in the interview):**
```python
employees = pd.read_csv("employees.csv")

# Rename only some columns
employees = employees.rename(columns={"name": "employee_name", "salary": "monthly_salary"})

print(employees.columns.tolist())
```
**Output:**
```text
['employee_id', 'employee_name', 'department', 'monthly_salary']
```
**What it means:** Two columns got new names; the others are unchanged.
**Alternative:** Replace all names at once: `employees.columns = ["id", "name", "dept", "pay"]` (the list length must equal the number of columns, otherwise you get an error).
**Likely follow-ups:**
- *What if a name in the dictionary does not exist?* It is silently ignored unless you pass `errors="raise"`.
- *Clean all names at once?* `df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")`.
**Common mistakes:** Not saving the result (`rename` returns a new table); using `index=` instead of `columns=` (that renames row labels).

### Q19 ⭐⭐ 🟢 How do you drop a column or a row from a DataFrame, and what does axis mean?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** `drop` with `columns=`/`index=` and the meaning of axis 0 and 1.
**Say this in the interview:** "`df.drop(columns=['department'])` removes a column and `df.drop(index=[0, 1])` removes rows by their index label. Axis 0 means down the rows, axis 1 means across the columns."
**Explain simply:**
- Axis is the direction pandas works in: axis 0 = rows (top to bottom), axis 1 = columns (left to right).
- `drop('department', axis=1)` means the same as `drop(columns='department')`. The named versions are easier to read, so I prefer them.
- `drop` returns a new table; save it in a variable or the original stays as it was.
- Rows are dropped by index label, not by position, so after filtering check the labels first.
**Sample data:** The 8-row `employees` table.
**Code (what you write in the interview):**
```python
# Drop a column
without_department = employees.drop(columns=["department"])

# Drop the first two rows (index labels 0 and 1)
without_first_two = employees.drop(index=[0, 1])

print(without_department.head(3))
print(without_first_two.head(3))
```
**Output:**
```text
   employee_id   name  salary
0          101   Asha   40000
1          102   Ravi   35000
2          103  Meena   60000
   employee_id   name department  salary
2          103  Meena    Finance   60000
3          104  Karan      Sales   45000
4          105   Anil    Finance   55000
```
**What it means:** The first table has lost the `department` column; the second starts at employee 103 because rows 0 and 1 are gone.
**Likely follow-ups:**
- *Drop rows by condition?* Better to filter: `df[df["salary"] > 0]`.
- *Drop a column with missing values?* `dropna(axis=1)`.
**Common mistakes:** Forgetting `axis=1` when using the old style `drop("department")` (it looks for a row labelled "department" and raises an error); mixing `axis=` with `columns=` in one call (ValueError); not saving the result.

### Q20 ⭐⭐ 🟢 How do you list the unique values of a column and count how many unique values it has?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you know unique() (the values) and nunique() (the count) and can tell them apart.
**Say this in the interview:** "unique() gives me the distinct values, nunique() gives me how many distinct values there are. nunique() skips missing values unless I ask it not to."
**Explain simply:**
- **unique values** means each different value listed once, for example every department name once, even if 500 people work in Sales.
- `unique()` returns the list of distinct values; `nunique()` returns just the count of them.
- Missing values (NaN, meaning an empty cell) are shown by `unique()` but not counted by `nunique()`. Use `nunique(dropna=False)` to count them too.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# the different departments, each listed once
print(employees["department"].unique())

# how many different departments there are
print(employees["department"].nunique())
```
**Output:**
```text
<StringArray>
['Sales', 'HR', 'Finance', 'IT']
Length: 4, dtype: str
4
```
**What it means:** There are 4 different departments: Sales, HR, Finance and IT.
**Alternative:** `employees['department'].value_counts()` also shows each value and how many rows have it, which is handy when the interviewer asks "how many people in each?".
**Likely follow-ups:** 1) *Does nunique count blanks?* No, not by default; add `dropna=False` (I checked: a column with 1 blank and 1 real value gives 1, or 2 with `dropna=False`). 2) *How do I list unique values for the whole table?* Loop over the columns, or call `employees.nunique()` to get the count for every column at once.
**Common mistakes:** Writing `unique` without brackets; calling `unique()` on a DataFrame (it only works on a single column); forgetting that blanks are skipped by `nunique()`, so the count can look one short.

### Q21 ⭐⭐ 🟢 What is the difference between df['col'] and df[['col']]?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you understand the difference between a Series (one column) and a DataFrame (a table).
**Say this in the interview:** "Single brackets give me one column as a Series, which is like a plain list with an index. Double brackets give me a DataFrame with one column, so it is still a table."
**Explain simply:**
- A **Series** is one column of values with row labels. A **DataFrame** is a table with rows and columns.
- `df['col']` returns a Series. The inner `['col']` inside another pair of brackets is a list, so `df[['col']]` returns a DataFrame.
- Use double brackets when the next step needs a table (for example `.to_csv`, or selecting several columns). Use single brackets when you want to do maths or filtering on one column.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# single brackets: a Series
salary_series = employees["salary"]
print(type(salary_series))
print(salary_series.shape)

# double brackets: a DataFrame with one column
salary_table = employees[["salary"]]
print(type(salary_table))
print(salary_table.shape)
```
**Output:**
```text
<class 'pandas.Series'>
(6,)
<class 'pandas.DataFrame'>
(6, 1)
```
**What it means:** The first is one column of 6 values (shape (6,)). The second is a table with 6 rows and 1 column (shape (6, 1)).
**Likely follow-ups:** 1) *How do you get two columns?* Pass a list: `employees[['name', 'salary']]`, so the double brackets are really a list inside the normal brackets. 2) *Can you convert a Series to a DataFrame?* Yes, `salary_series.to_frame()`.
**Common mistakes:** Writing `df['name', 'salary']` for two columns (this raises a KeyError because pandas looks for a column called the tuple); forgetting that a Series has no column headers to print in table form.

### Q22 ⭐⭐ 🟢 What is the difference between a view and a copy of a DataFrame, and how do you make an independent copy with copy()?
**Asked at:** commonly asked (no company-specific report found); the pandas 3.0 Copy-on-Write change is discussed in 2026 blogs and the PDEP-7 proposal.
**What the interviewer is checking:** Whether you know that changing a slice should not silently change the original table, and that copy() makes that explicit.
**Say this in the interview:** "A view shares the same data as the original, a copy has its own data. In pandas 3 every slice behaves like a copy, but I still write copy() when I plan to change a slice, so my intent is clear."
**Explain simply:**
- A **view** is another window onto the same data in memory: change it and the original changes too. A **copy** is separate data: changes stay inside it.
- In older pandas (2.x and before) it was hard to predict which one you got; that confusion caused the SettingWithCopyWarning.
- In pandas 3.0 a feature called **Copy-on-Write** means any new DataFrame behaves like a copy, so changing it never touches the original. I ran the code below on pandas 3.0.5.
- `.copy()` gives an independent copy explicitly and works the same in every version.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# take the Sales rows and make an independent copy
sales_team = employees[employees["department"] == "Sales"].copy()

# give everyone in the copy a raise
sales_team["salary"] = sales_team["salary"] + 5000

# the original table is untouched
print(sales_team[["name", "salary"]])
print(employees.loc[[0, 3], ["name", "salary"]])
```
**Output:**
```text
    name  salary
0   Asha   50000
3  Meena   33000
    name  salary
0   Asha   45000
3  Meena   28000
```
**What it means:** The raise shows only in `sales_team`. The original `employees` still has 45000 and 28000.
**Likely follow-ups:** 1) *Is copy() still needed in pandas 3?* Not for safety (I verified that without it the original is unchanged too), but it is good practice and needed if the code must also run on pandas 2.x (this is from memory, unverified). 2) *Is a copy slow?* It uses extra memory for big tables, which is why pandas avoids copying until you change something.
**Common mistakes:** Assuming that on older pandas a slice is always a copy (it can be a view); modifying a filtered slice and expecting the original to change in pandas 3 (it will not).

### Q23 ⭐⭐ 🟢 Write code to show the top 5 highest-paid employees.
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you can sort and take the top rows, ideally with nlargest.
**Say this in the interview:** "I would use nlargest: it gives me the top 5 rows by salary in one step."
**Explain simply:**
- `nlargest(5, 'salary')` returns the 5 rows with the biggest salary, already sorted from highest to lowest.
- The sort-then-head way (`sort_values(...).head(5)`) gives the same answer; see Q35 for when each is better.
- My sample has only 6 people, so the top 5 leaves out just one person.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# the 5 highest-paid employees
top_earners = employees.nlargest(5, "salary")
print(top_earners[["name", "salary"]])
```
**Output:**
```text
    name  salary
4  Arjun   65000
2   Anil   58000
5   Sara   52000
0   Asha   45000
1   Ravi   32000
```
**What it means:** Arjun (65000) is first, then Anil, Sara, Asha and Ravi. Meena, the lowest paid, is left out.
**Alternative:** ```python
# sort high to low, then keep the first 5
top_earners = employees.sort_values("salary", ascending=False).head(5)
```
**Likely follow-ups:** 1) *What if two people tie for 5th place?* `nlargest` keeps the first one it meets by default; `keep='all'` keeps all tied rows (I verified this). 2) *Top 5 per department?* That needs groupby, covered in a later part.
**Common mistakes:** Forgetting `ascending=False` in the sort version (you get the lowest paid); using `head(5)` without sorting first, which just returns the first 5 rows in file order.

### Q24 ⭐⭐ 🟢 How do you select the first 10 rows and the first 3 columns using iloc?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you remember that iloc is by position and that its slices exclude the end.
**Say this in the interview:** "iloc works by position: rows first, then columns. So iloc[:10, :3] means the first 10 rows and the first 3 columns."
**Explain simply:**
- **iloc** means "integer location": you select by position number, starting from 0, not by label.
- Inside the brackets the first part is rows, the second part is columns, separated by a comma.
- `:10` means "from the start up to, but not including, position 10", which is the first 10 rows. `:3` is the first 3 columns.
- My sample has 12 employees so the output shows 10 rows.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": range(101, 113),
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara", "Kiran", "Divya", "Imran", "Neha", "Vikram", "Pooja"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR", "IT", "Finance", "Sales", "HR", "IT", "Finance"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000, 61000, 39000, 47000, 35000, 70000, 44000],
})
```
**Code (what you write in the interview):**
```python
# first 10 rows, first 3 columns
first_block = employees.iloc[:10, :3]
print(first_block)
```
**Output:**
```text
   employee_id   name department
0          101   Asha      Sales
1          102   Ravi         HR
2          103   Anil    Finance
3          104  Meena      Sales
4          105  Arjun         IT
5          106   Sara         HR
6          107  Kiran         IT
7          108  Divya    Finance
8          109  Imran      Sales
9          110   Neha         HR
```
**What it means:** You get 10 rows (positions 0 to 9) and the first three columns: employee_id, name, department.
**Alternative:** `employees.head(10).iloc[:, :3]` does the same in two steps.
**Likely follow-ups:** 1) *What if the table has fewer than 10 rows?* iloc slicing does not fail, it just returns what exists. 2) *How is this different from loc?* loc uses labels, iloc uses positions (see Q7 and Q37).
**Common mistakes:** Writing `iloc[10, 3]`, which gives one single cell, not a block; putting the columns first; forgetting the colon in `iloc[:10, :3]`.

### Q25 ⭐⭐ 🟢 Write code to filter employees whose name starts with 'A' using str.startswith().
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you know the `.str` accessor (text tools for a column) and can build a True/False filter.
**Say this in the interview:** "I use str.startswith on the name column, which gives True or False for each row, and I use that to filter."
**Explain simply:**
- `.str` unlocks text methods on a whole column at once; `startswith('A')` is True for names that begin with A.
- Filtering with that True/False column keeps only the True rows.
- It is case sensitive: `'a'` would not match `'Asha'`. For both cases use `str.lower().str.startswith('a')`.
- Blank names: in pandas 3.0 with the default text type they give False and are dropped (I verified). For safety on older versions add `na=False`.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# True for names that begin with A
name_starts_with_a = employees["name"].str.startswith("A")

# keep only those rows
a_employees = employees[name_starts_with_a]
print(a_employees[["name", "department"]])
```
**Output:**
```text
    name department
0   Asha      Sales
2   Anil    Finance
4  Arjun         IT
```
**What it means:** Asha, Anil and Arjun start with A. Ravi, Meena and Sara are removed.
**Likely follow-ups:** 1) *How do you match any capitalisation?* `employees['name'].str.lower().str.startswith('a')`. 2) *Names ending in a letter?* `str.endswith('a')`.
**Common mistakes:** Writing `employees['name'].startswith('A')` without `.str` (an AttributeError); using `==` with a star like `'A*'` (that is not how pandas works); forgetting case sensitivity.

### Q26 ⭐⭐ 🟢 How do you filter rows where a column is between two values, for example salary between 30,000 and 60,000?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you know between() and that both ends are included.
**Say this in the interview:** "I use salary.between(30000, 60000). Both ends are included by default."
**Explain simply:**
- `between(low, high)` gives True when the value is at or above `low` and at or below `high`.
- It replaces the longer form `(salary >= 30000) & (salary <= 60000)`.
- To leave out an end, use `inclusive='left'`, `'right'` or `'neither'` (I checked `'left'` excludes the upper end).
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# salary from 30,000 to 60,000, both ends included
mid_salary = employees[employees["salary"].between(30000, 60000)]
print(mid_salary[["name", "salary"]])
```
**Output:**
```text
   name  salary
0  Asha   45000
1  Ravi   32000
2  Anil   58000
5  Sara   52000
```
**What it means:** Four people earn between 30,000 and 60,000. Meena (28,000) and Arjun (65,000) fall outside.
**Alternative:** ```python
# the long way, each condition in brackets
mid_salary = employees[(employees["salary"] >= 30000) & (employees["salary"] <= 60000)]
```
**Likely follow-ups:** 1) *Does a salary of exactly 60,000 count?* Yes, by default. 2) *Does it work on dates?* Yes, `between` works on dates and text too.
**Common mistakes:** Thinking the ends are excluded; writing `30000 <= salary <= 60000` directly (a chained comparison raises an error on a column); forgetting brackets in the long form.

### Q27 ⭐⭐ 🟢 How do you read only selected columns from a large CSV using usecols?
**Asked at:** commonly asked (no company-specific report found); a standard-practice question, not tied to a company in the sources.
**What the interviewer is checking:** Whether you know how to save memory and time by loading only the columns you need.
**Say this in the interview:** "I pass usecols to read_csv with the list of columns I need. pandas then skips the rest while reading, which saves memory on a large file."
**Explain simply:**
- **usecols** tells `read_csv` which columns to load; the others are never put in memory.
- Give it a list of column names (or column positions).
- This matters for big HR files such as a payroll export with 80 columns when you need only 3.
**Sample data:** a file called `employees.csv` with these contents.
```text
employee_id,name,department,job_title,salary,left_company
101,Asha,Sales,Sales Manager,45000,No
102,Ravi,HR,HR Executive,32000,Yes
103,Anil,Finance,finance MANAGER,58000,No
104,Meena,Sales,Sales Executive,28000,Yes
105,Arjun,IT,IT Analyst,65000,No
106,Sara,HR,HR Manager,52000,No
```
**Code (what you write in the interview):**
```python
import pandas as pd

# load only three columns from the file
employees = pd.read_csv("employees.csv", usecols=["name", "department", "salary"])
print(employees)
```
**Output:**
```text
    name department  salary
0   Asha      Sales   45000
1   Ravi         HR   32000
2   Anil    Finance   58000
3  Meena      Sales   28000
4  Arjun         IT   65000
5   Sara         HR   52000
```
**What it means:** Only the three requested columns arrive, so `employee_id` and the rest are never loaded.
**Alternative:** For files too big even for that, add `nrows=1000` to read a first slice, or `chunksize=` to read in pieces (not run here).
**Likely follow-ups:** 1) *In what order do the columns appear?* In the file's order, not the order you list them (from memory, verify on your data). 2) *What if a name is misspelt?* pandas raises a ValueError saying the column is not in the file.
**Common mistakes:** Giving column names with different spelling or capitals than the file header; passing a single string instead of a list; selecting columns after loading and thinking that saves memory (it does not, the whole file was already loaded).

### Q28 ⭐⭐ 🟢 How do you save a DataFrame to a CSV file without writing the index, and how do you write it to Excel?
**Asked at:** commonly asked (no company-specific report found); a standard-practice question, not tied to a company in the sources.
**What the interviewer is checking:** Whether you know `index=False` and that Excel output needs a helper library.
**Say this in the interview:** "to_csv with index=False saves the table without the extra row-number column. to_excel works the same way, and it needs the openpyxl library installed."
**Explain simply:**
- Every DataFrame has an **index** (the row labels 0, 1, 2...). By default `to_csv` writes it as an extra first column, which usually you do not want.
- `index=False` leaves it out.
- `to_excel` writes an `.xlsx` file; pandas uses the `openpyxl` package behind the scenes, so install it if you get an ImportError. You can also pass `sheet_name=`.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# save to CSV without the row numbers
employees.to_csv("employees_clean.csv", index=False)

# save to Excel, also without the row numbers
employees.to_excel("employees_clean.xlsx", sheet_name="Employees", index=False)
```
**Output:**
```text
(nothing is printed; the code creates two files)
```
**What it means:** Two files appear in the working folder. The first lines of the CSV are:

```text
employee_id,name,department,job_title,salary,left_company
101,Asha,Sales,Sales Manager,45000,No
102,Ravi,HR,HR Executive,32000,Yes
```

There is no extra number column in front. (I confirmed both files were created and the CSV starts as shown.)
**Likely follow-ups:** 1) *How do you write two sheets in one file?* Use `with pd.ExcelWriter('file.xlsx') as writer:` and call `to_excel(writer, sheet_name=...)` for each table. 2) *How do you read it back?* `pd.read_csv(...)` or `pd.read_excel(...)` (see Q2).
**Common mistakes:** Forgetting `index=False` and getting an unnamed extra column when the file is read again; forgetting the file extension; having the file open in Excel while saving (a permission error).

### Q29 ⭐⭐ 🟢 What is the difference between head(), sample() and tail(), and how do you pick 5 random rows?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you can look at the start, the end and a random part of the data, and know why random matters.
**Say this in the interview:** "head shows the first rows, tail the last rows, and sample picks random rows. I use sample(5) to get 5 random rows, and random_state if I want the same rows every time."
**Explain simply:**
- `head(n)`: the first n rows (default 5). `tail(n)`: the last n rows.
- `sample(n)`: n rows picked at random from anywhere, so each run gives different rows.
- Random rows help because the first rows of a file can be unusual (for example sorted by hire date), so they may not represent all the data.
- `random_state=1` fixes the random pick so you and a colleague see the same rows; it is only needed for repeatability.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# 5 random rows; random_state makes the pick repeatable
random_five = employees.sample(5, random_state=1)
print(random_five[["name", "department"]])
```
**Output:**
```text
    name department
2   Anil    Finance
1   Ravi         HR
4  Arjun         IT
0   Asha      Sales
3  Meena      Sales
```
**What it means:** Five of the six employees come back in a shuffled order. Without `random_state` the rows would change on every run.
**Alternative:** `employees.sample(frac=0.2)` picks 20 percent of the rows instead of a fixed count.
**Likely follow-ups:** 1) *Does sample change the original?* No, it returns a new table. 2) *Why use tail?* To check the end of the file for totals rows or incomplete data.
**Common mistakes:** Expecting `head()` to be random; asking for `sample(n)` with n larger than the number of rows (an error); assuming the same rows will come back on each run without random_state.

### Q30 ⭐⭐ 🟢 How do you find the maximum salary and the row (employee) who earns it?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you know that max() gives the value only and idxmax() gives the row position of it.
**Say this in the interview:** "max gives me the highest salary. To get who earns it I use idxmax, which returns the row label of that maximum, and then I look up that row with loc."
**Explain simply:**
- `max()` returns just the number.
- `idxmax()` returns the **index label** (the row name) where the maximum sits.
- `loc[label]` then pulls out that whole row, so you see the name and other details.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# the highest salary
highest_salary = employees["salary"].max()
print(highest_salary)

# the row label of that salary, then the whole row
top_row_label = employees["salary"].idxmax()
print(employees.loc[top_row_label])
```
**Output:**
```text
65000
employee_id            105
name                 Arjun
department              IT
job_title       IT Analyst
salary               65000
left_company            No
Name: 4, dtype: object
```
**What it means:** The highest salary is 65000 and it belongs to Arjun in IT.
**Alternative:** `employees.nlargest(1, 'salary')` returns the same single row as a one-row table.
**Likely follow-ups:** 1) *What if two people tie?* `idxmax` returns only the first one it finds; use a filter such as `employees[employees['salary'] == highest_salary]` to see all. 2) *What about the lowest?* `min()` and `idxmin()`.
**Common mistakes:** Using `max()` and expecting a row; using `iloc[idxmax()]` when the index is not 0 to n (it mixes labels and positions); not handling ties.

### Q31 ⭐⭐ 🟢 How do you count the rows that satisfy a condition, for example how many employees have left the company?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you know that a True/False column can be counted with sum().
**Say this in the interview:** "I make a True/False check for left_company equal to Yes, then sum it. True counts as 1, so the sum is the number of rows that match."
**Explain simply:**
- A condition like `employees['left_company'] == 'Yes'` gives True or False for every row.
- pandas treats True as 1 and False as 0, so `.sum()` counts the Trues.
- This is the attrition count: the number of employees who left. Divide by the total (`len(employees)`) for the attrition rate.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# True for employees who left; summing counts the Trues
employees_who_left = (employees["left_company"] == "Yes").sum()
print(employees_who_left)
```
**Output:**
```text
2
```
**What it means:** 2 of the 6 employees have left.
**Alternative:** ```python
# filter first, then count the rows that remain
employees_who_left = len(employees[employees["left_company"] == "Yes"])
```
**Likely follow-ups:** 1) *How do I get the percentage?* `(employees['left_company'] == 'Yes').mean() * 100` gives 33.3 here, because the mean of True/False is the share of True. 2) *Does it count blank values?* A blank is not equal to "Yes", so it counts as False, not as left.
**Common mistakes:** Using `count()` on the filtered column, which counts non-blank cells; using `.sum()` on the text column itself, which joins the words together instead of counting; mismatching capital letters (`'yes'` is not `'Yes'`).

### Q32 ⭐⭐ 🟢 How do you check for duplicate column names or confirm the DataFrame shape after each filter?
**Asked at:** commonly asked (no company-specific report found); checking row counts after each filter is advised in pandas interview guides (GoLinuxCloud).
**What the interviewer is checking:** Whether you have a habit of verifying your data: duplicated headers and row counts after each step.
**Say this in the interview:** "I check columns.duplicated().any() for repeated column names, and I print shape after each filter to make sure I did not lose or keep rows by mistake."
**Explain simply:**
- A DataFrame can have two columns with the same name (for example after joining files). Selecting that name then returns two columns, which causes confusing results.
- `employees.columns.duplicated()` marks each repeated name as True; `.any()` says whether there is at least one.
- `shape` gives (number of rows, number of columns). Compare it before and after a filter: the rows should drop as you expect, the columns should stay the same.
**Sample data:**
```python
# note: "department" appears twice
employees = pd.DataFrame(
    [[101, "Asha", "Sales", "Sales"],
     [102, "Ravi", "HR", "HR"],
     [103, "Anil", "Finance", "Finance"],
     [104, "Meena", "Sales", "Sales"]],
    columns=["employee_id", "name", "department", "department"],
)
```
**Code (what you write in the interview):**
```python
# is any column name repeated?
print(employees.columns.duplicated().any())

# shape before and after a filter
print(employees.shape)
later_joiners = employees[employees["employee_id"] > 102]
print(later_joiners.shape)
```
**Output:**
```text
True
(4, 4)
(2, 4)
```
**What it means:** The first line says True: one column name appears twice. The table has 4 rows and 4 columns, and after keeping IDs above 102 there are 2 rows and still 4 columns. (I filtered on employee_id because filtering on the repeated name `department` raises an error.)
**Alternative:** `employees.columns[employees.columns.duplicated()]` shows which names are repeated.
**Likely follow-ups:** 1) *How do I fix duplicates?* Rename the columns (see Q18) or drop one; `employees.loc[:, ~employees.columns.duplicated()]` keeps the first of each name. 2) *Why check shape?* A merge or filter that silently adds or drops rows is a classic error.
**Common mistakes:** Using `df.columns.unique()` and not comparing its length; checking only the final shape and not each step; forgetting that `shape` has no brackets after it.

### Q33 ⭐⭐ 🟡 What is the index of a DataFrame, and how do you set a column such as employee ID as the index?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you know the index is the row label and that set_index makes a column that label.
**Say this in the interview:** "The index is the label for each row, 0, 1, 2 by default. I can use set_index to make employee_id the row label so I can look rows up by ID."
**Explain simply:**
- The **index** is the column of row labels on the far left of a DataFrame. It is not a normal data column.
- By default it is just 0, 1, 2.... A unique business key such as employee ID is a better label.
- `set_index('employee_id')` moves that column into the index. Then `loc[103]` finds the employee with ID 103.
- pandas returns a new table; you must save it back to a name (or use `inplace=True`, which beginners should avoid).
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# make employee_id the row label
employees = employees.set_index("employee_id")
print(employees.head(3))

# look up one employee by ID
print(employees.loc[103, "name"])
```
**Output:**
```text
             name department        job_title  salary left_company
employee_id                                                       
101          Asha      Sales    Sales Manager   45000           No
102          Ravi         HR     HR Executive   32000          Yes
103          Anil    Finance  finance MANAGER   58000           No
Anil
```
**What it means:** The IDs now sit on the left as labels, and looking up 103 returns Anil.
**Alternative:** `pd.read_csv('employees.csv', index_col='employee_id')` sets the index while reading.
**Likely follow-ups:** 1) *Must the index be unique?* No, but a unique one makes lookups clean; duplicates return several rows. 2) *How do I undo it?* `reset_index()` (see Q34).
**Common mistakes:** Forgetting to save the result, so nothing changes; trying to select the index with `employees['employee_id']` afterwards (it is no longer a column, that is a KeyError); assuming the index must be a number.

### Q34 ⭐⭐ 🟡 How do you reset the index after filtering or sorting, and what does drop=True do?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you know that filtering keeps the old row numbers and how to tidy them.
**Say this in the interview:** "After a filter or sort the old row numbers stay. reset_index gives fresh 0, 1, 2 numbers, and drop=True throws the old numbers away instead of keeping them as a new column."
**Explain simply:**
- Filtering rows keeps their original labels, so you might see 0, 3, 5 in the index. That is correct but untidy.
- `reset_index()` renumbers 0, 1, 2....
- Without `drop=True` the old index is added back as a new column called `index`. With `drop=True` it is discarded.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# keep the better-paid rows
well_paid = employees[employees["salary"] > 50000]

# renumber the rows from 0 and discard the old numbers
well_paid = well_paid.reset_index(drop=True)
print(well_paid[["name", "salary"]])
```
**Output:**
```text
    name  salary
0   Anil   58000
1  Arjun   65000
2   Sara   52000
```
**What it means:** The three well-paid employees (Anil, Arjun, Sara) are now numbered 0, 1, 2 instead of their old positions 2, 4, 5.
**Likely follow-ups:** 1) *What happens without drop=True?* The old numbers become an extra column named `index` (I checked this). 2) *Is it required?* No, but it avoids surprises when you later use `loc` or `iloc` on the filtered table.
**Common mistakes:** Not saving the result back; forgetting `drop=True` and ending up with a useless `index` column; calling `reset_index` when the index is a real key like employee ID that you wanted to keep (then you do want it as a column, so skip drop).

### Q35 ⭐⭐ 🟡 What is the difference between nlargest() and sort_values().head(), and when would you use each?
**Asked at:** commonly asked (no company-specific report found); the comparison is covered in the pandas docs and a 2026 Lerner Python post (snippet-level only).
**What the interviewer is checking:** Whether you know a convenient top-N shortcut and its limits.
**Say this in the interview:** "nlargest(n, column) is a shortcut for sorting and taking the top n. It is shorter and usually faster on big data, but sort_values().head() is more flexible, for example it can sort text or by several columns."
**Explain simply:**
- Both give the top rows by a column. `nlargest(3, 'salary')` is one call; `sort_values('salary', ascending=False).head(3)` is two.
- `nlargest` is meant for numeric columns. On a text column it raises an error (I verified), while `sort_values` sorts text A to Z.
- `sort_values` can sort by several columns with different directions; `nlargest` can take several columns but all in the same direction.
- Ties: `nlargest` has `keep='first'` (default), `'last'` or `'all'` to control tied rows at the cut-off.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# shortcut: top 3 salaries
top_three = employees.nlargest(3, "salary")
print(top_three[["name", "salary"]])

# the longer way gives the same rows
top_three_again = employees.sort_values("salary", ascending=False).head(3)
print(top_three_again[["name", "salary"]])
```
**Output:**
```text
    name  salary
4  Arjun   65000
2   Anil   58000
5   Sara   52000
    name  salary
4  Arjun   65000
2   Anil   58000
5   Sara   52000
```
**What it means:** Both print Arjun, Anil and Sara in the same order, so for plain top-N I would use nlargest, and sort_values when the sorting needs are more complex.
**Alternative:** For the smallest values use `nsmallest`.
**Likely follow-ups:** 1) *Which is faster?* `nlargest` usually, on large tables (stated in the pandas docs and blog snippets, not timed here). 2) *Top 5 within each department?* That needs groupby, covered in a later part.
**Common mistakes:** Using `nlargest` on a text column; forgetting `ascending=False` in the sort version; ignoring ties at the cut-off.

### Q36 ⭐⭐ 🟡 How do you select rows by label and specific columns using loc, for example employees 101 to 105 and only name and salary?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you know that loc takes labels, rows first then columns, and that the end label is included.
**Say this in the interview:** "With employee ID as the index, I write loc[101:105, ['name', 'salary']]. The part before the comma picks rows by label, the part after picks the columns."
**Explain simply:**
- **loc** selects by label: `loc[rows, columns]`.
- `101:105` is a label slice, and unlike normal Python it **includes** 105 (see Q37).
- A list of column names, `['name', 'salary']`, picks just those columns, in the order given.
- This needs the ID as the index first (see Q33). If it is still a normal column, use a filter instead.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})

# employee_id is the row label (see Q33)
employees = employees.set_index("employee_id")
```
**Code (what you write in the interview):**
```python
# rows with ID 101 to 105, and only these two columns
selected = employees.loc[101:105, ["name", "salary"]]
print(selected)
```
**Output:**
```text
              name  salary
employee_id               
101           Asha   45000
102           Ravi   32000
103           Anil   58000
104          Meena   28000
105          Arjun   65000
```
**What it means:** Five rows come back (101, 102, 103, 104, 105), each showing only name and salary. ID 106 is not included because it is outside the range.
**Alternative:** ```python
# works even when employee_id is a normal column
selected = employees[employees["employee_id"].between(101, 105)][["name", "salary"]]
```
**Likely follow-ups:** 1) *Why do we get 5 rows and not 4?* loc includes the end label. 2) *What if a label does not exist?* A single missing label raises a KeyError; for a slice on a sorted index it just returns what lies in range.
**Common mistakes:** Using round brackets `loc(...)` instead of square; forgetting to set the index first; writing the columns without a list (`loc[101:105, 'name', 'salary']` is an error).

### Q37 ⭐⭐ 🟡 Why does loc slicing include the end label while iloc slicing excludes the end position?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you understand the logic behind two slicing rules that look inconsistent.
**Say this in the interview:** "loc works with labels, so asking for 101 to 103 means those labels, and 103 is included. iloc works with positions and follows the normal Python rule of stopping before the end."
**Explain simply:**
- With **labels**, there is no natural way to say "the label just before 103" (labels can be names, dates, IDs), so asking for "up to 103" must mean "including 103".
- With **positions**, "up to position 3" has a natural meaning: stop before it. This matches Python lists, so `iloc[0:3]` gives positions 0, 1, 2.
- The same lines of data show the difference below.
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})

# employee_id is the row label (see Q33)
employees = employees.set_index("employee_id")
```
**Code (what you write in the interview):**
```python
# loc: by label, end label included (101, 102, 103)
print(employees.loc[101:103, "name"])

# iloc: by position, end position excluded (positions 0, 1, 2; column 0 is name)
print(employees.iloc[0:3, 0])
```
**Output:**
```text
employee_id
101    Asha
102    Ravi
103    Anil
Name: name, dtype: str
employee_id
101    Asha
102    Ravi
103    Anil
Name: name, dtype: str
```
**What it means:** Both return Asha, Ravi and Anil, but that is a coincidence of this table: label 103 is at position 2. With a different index the two would return different rows.
**Likely follow-ups:** 1) *What does this mean for the count of rows?* `loc[a:b]` returns b minus a plus 1 rows when labels are consecutive; `iloc[a:b]` returns b minus a rows. 2) *Which is safer?* Use loc when you know the label, iloc when you know the position.
**Common mistakes:** Using the iloc rule for loc (and being one row short); mixing up which one accepts names (loc) and which only numbers (iloc).

### Q38 ⭐⭐ 🟡 How do you filter rows where a text column contains a word, for example job title containing 'Manager', ignoring upper or lower case?
**Asked at:** commonly asked (no company-specific report found); this topic appears in general pandas interview guides (DataCamp, AskPython).
**What the interviewer is checking:** Whether you can search inside text and ignore capitals.
**Say this in the interview:** "I use str.contains with the word and case=False, so Manager, manager and MANAGER all match."
**Explain simply:**
- `str.contains('Manager')` is True when the word appears anywhere in the text.
- By default it is case sensitive. `case=False` ignores upper or lower case.
- It treats the word as a regular expression (a pattern language) by default. For a plain word that makes no difference; for symbols such as `+` or `(` add `regex=False`.
- Blank cells give a missing result that breaks the filter on older pandas; add `na=False` to be safe (my sample has no blanks).
**Sample data:**
```python
employees = pd.DataFrame({
    "employee_id": [101, 102, 103, 104, 105, 106],
    "name": ["Asha", "Ravi", "Anil", "Meena", "Arjun", "Sara"],
    "department": ["Sales", "HR", "Finance", "Sales", "IT", "HR"],
    "job_title": ["Sales Manager", "HR Executive", "finance MANAGER", "Sales Executive", "IT Analyst", "HR Manager"],
    "salary": [45000, 32000, 58000, 28000, 65000, 52000],
    "left_company": ["No", "Yes", "No", "Yes", "No", "No"],
})
```
**Code (what you write in the interview):**
```python
# True when the job title has "manager" in any capitalisation
is_manager = employees["job_title"].str.contains("manager", case=False)

managers = employees[is_manager]
print(managers[["name", "job_title"]])
```
**Output:**
```text
   name        job_title
0  Asha    Sales Manager
2  Anil  finance MANAGER
5  Sara       HR Manager
```
**What it means:** Three job titles match: Sales Manager, finance MANAGER and HR Manager.
**Alternative:** ```python
# same idea by converting to lower case first
managers = employees[employees["job_title"].str.lower().str.contains("manager")]
```
**Likely follow-ups:** 1) *How do I search for two words?* Use `|` for "or": `str.contains('manager|director', case=False)`. 2) *How do I exclude them?* Put `~` in front of the condition: `employees[~is_manager]`.
**Common mistakes:** Forgetting `.str`; forgetting `case=False` and missing 'finance MANAGER'; leaving blanks without `na=False`; searching for text that includes special regex characters.

### Q39 ⭐⭐ 🟡 How do you filter rows that are NOT in a list of values, for example all departments except HR and Admin?
**Asked at:** commonly asked (no company-specific report found); a standard follow-up to `isin()` in pandas filtering guides.
**What the interviewer is checking:** Whether you know `isin()` plus the `~` (NOT) operator.
**Say this in the interview:** "I use `isin()` to find the rows that ARE in the list, then put a tilde in front to flip it, so I keep every row that is not in the list."
**Explain simply:**
- `isin(["HR", "Admin"])` gives True for HR and Admin rows and False for the rest.
- `~` means NOT. It flips True to False and False to True.
- Use `~`, not the word `not`; `not` does not work on a whole column.
- Missing values: a blank department is not in the list, so that row is kept. Check this if blanks matter.
**Sample data:** 5 employees with name, department, salary.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "department": ["Sales", "HR", "Admin", "Finance", "Sales"],
    "salary": [45000, 52000, 38000, 70000, 61000],
})

# ~ means NOT: keep rows whose department is NOT in the list
not_hr_or_admin = employees[~employees["department"].isin(["HR", "Admin"])]
print(not_hr_or_admin)
```
**Output:**
```text
    name department  salary
0   Asha      Sales   45000
3   John    Finance   70000
4  Priya      Sales   61000
```
**What it means:** Ravi (HR) and Meena (Admin) are gone; everyone else stays.
**Alternative:** `employees[(employees["department"] != "HR") & (employees["department"] != "Admin")]`. It works but gets long with many values.
**Likely follow-ups:** 1) *What about blank departments?* They are kept, because blank is not in the list (I ran this to check). 2) *Why not `not in`?* That is for single Python values, not a column.
**Common mistakes:** Forgetting the `~`; using `not` or `!`; forgetting the square brackets around the list.

### Q40 ⭐⭐ 🟡 How do you filter rows with missing values in a column, for example employees with no manager ID, using isna()?
**Asked at:** commonly asked (no company-specific report found); missing-data checks are a screen theme in pandas guides (GoLinuxCloud).
**What the interviewer is checking:** Whether you know that you cannot test for missing values with `== None` or `== np.nan`.
**Say this in the interview:** "I use `isna()` on the column. It returns True where the value is missing, and I use that as the filter."
**Explain simply:**
- Missing values in pandas show as `NaN` (Not a Number, the standard "blank" marker).
- `NaN == NaN` is False, so `== np.nan` never finds anything. `isna()` is the right test.
- Use `notna()` for the opposite: rows that have a value.
**Sample data:** 4 employees; Ravi and John have no manager ID.
**Code (what you write in the interview):**
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "manager_id": [101, np.nan, 102, np.nan],
})

# isna() gives True where the value is missing
no_manager = employees[employees["manager_id"].isna()]
print(no_manager)
```
**Output:**
```text
   name  manager_id
1  Ravi         NaN
3  John         NaN
```
**What it means:** Two employees have no manager recorded; these are rows to investigate or fix.
**Alternative:** `employees[employees["manager_id"].notna()]` keeps only the rows that do have a manager.
**Likely follow-ups:** 1) *How do you count them?* `employees["manager_id"].isna().sum()`. 2) *Is an empty string missing?* No, only real NaN; clean empty text first.
**Common mistakes:** Using `== np.nan` or `== None`; forgetting that a blank space " " is not NaN.

### Q41 ⭐⭐ 🟡 What is the query() method in pandas, and how does it compare with boolean indexing?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know a second, more readable way to filter, and its limits.
**Say this in the interview:** "`query()` lets me write the filter as a short text condition, like SQL's WHERE. It gives the same result as boolean indexing and is often easier to read when there are several conditions."
**Explain simply:**
- Boolean indexing: build True/False per row with conditions, then use it to pick rows. Needs brackets and `&`.
- `query()`: pass the condition as text. Use plain `and` / `or` inside the text, and no brackets per condition.
- Column names with spaces need backticks, like `` `Hire Date` ``.
- Boolean indexing is more flexible (any Python function); `query()` is cleaner for simple conditions.
**Sample data:** 5 employees with department and salary.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "department": ["Sales", "HR", "Finance", "Finance", "Sales"],
    "salary": [45000, 52000, 38000, 70000, 61000],
})

# Boolean indexing
result_one = employees[(employees["department"] == "Finance") & (employees["salary"] > 50000)]

# query(): the same filter written as a short text condition
result_two = employees.query("department == 'Finance' and salary > 50000")

print(result_one)
print(result_two)
```
**Output:**
```text
   name department  salary
3  John    Finance   70000
   name department  salary
3  John    Finance   70000
```
**What it means:** Both give the same rows; `query()` just reads more like English.
**Likely follow-ups:** 1) *How do I use a variable?* Put `@` before it (Q42). 2) *Does query change the original?* No, it returns a new DataFrame.
**Common mistakes:** Forgetting quotes around text values inside the query string; using a column name with spaces without backticks.

### Q42 ⭐⭐ 🟡 How do you use a Python variable inside query()?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the `@` prefix.
**Say this in the interview:** "Inside `query()` I put an `@` before the variable name. Without the `@`, pandas looks for a column with that name."
**Explain simply:**
- The query text is not normal Python code, so pandas needs a signal to look outside the DataFrame.
- `@salary_limit` means "use my variable `salary_limit`".
- This lets you change the limit in one place instead of editing the text.
**Sample data:** 5 employees with department and salary.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "department": ["Sales", "HR", "Finance", "Finance", "Sales"],
    "salary": [45000, 52000, 38000, 70000, 61000],
})

salary_limit = 50000
chosen_department = "Sales"

# @ tells query() to use the Python variable, not a column
result = employees.query("salary > @salary_limit and department == @chosen_department")
print(result)
```
**Output:**
```text
    name department  salary
4  Priya      Sales   61000
```
**What it means:** Only Priya is in Sales and earns above 50,000.
**Alternative:** An f-string, `f"salary > {salary_limit}"`. It works but `@` is cleaner and safer for text values.
**Likely follow-ups:** 1) *What if the variable is a list?* `department in @my_list` works. 2) *What error if you forget `@`?* An `UndefinedVariableError`, since pandas looks for a column.
**Common mistakes:** Forgetting `@`; putting quotes around the variable name.

### Q43 ⭐⭐ 🟡 How do you read only the first 1,000 rows of a large CSV file, and why would you do it?
**Asked at:** commonly asked (no company-specific report found); a gap-fill style question on handling large files.
**What the interviewer is checking:** Whether you know how to avoid loading a huge file blindly.
**Say this in the interview:** "I use `nrows=1000` in `read_csv`. I do it to preview the columns and data types quickly, and to test my code, without waiting for or running out of memory on a huge file."
**Explain simply:**
- `nrows` tells pandas to stop reading after that many data rows (the header is not counted).
- Reading is fast and uses little memory, so it is a safe first look.
- Once the code works on the sample, remove `nrows` to run on the full file.
- Caution: the first 1,000 rows may not represent the whole file (for example, sorted by date).
**Sample data:** a file `employees_big.csv` with 2,500 rows (employee_id, department, salary).
**Code (what you write in the interview):**
```python
import pandas as pd

# Read only the first 1,000 rows to preview a big file quickly
preview = pd.read_csv("employees_big.csv", nrows=1000)
print(preview.shape)
print(preview.head(3))
```
**Output:**
```text
(1000, 3)
   employee_id department  salary
0            1      Sales   30000
1            2         HR   30010
2            3    Finance   30020
```
**What it means:** Only 1,000 of the 2,500 rows were loaded, which is enough to see the structure.
**Alternative:** `chunksize=1000` reads the whole file in pieces of 1,000 rows, useful when you must process everything but cannot fit it in memory.
**Likely follow-ups:** 1) *How to skip rows instead?* `skiprows`. 2) *How to load fewer columns?* `usecols`.
**Common mistakes:** Trusting a sample that is not representative; forgetting to remove `nrows` later.

### Q44 ⭐⭐ 🟡 What are the common parameters of read_csv() that you use for messy files (sep, header, skiprows, encoding, na_values)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you have handled real, untidy exports, not only clean practice files.
**Say this in the interview:** "`sep` for the separator, `skiprows` to skip junk lines at the top, `header` to say which line holds column names, `encoding` for special characters, and `na_values` to tell pandas which text means missing."
**Explain simply:**
- `sep`: the character between columns. Default is a comma; use `";"` or `"\t"` (tab) when different.
- `skiprows`: number of lines to ignore at the top (report titles, dates).
- `header`: which line has the column names (0 is the first line after skipping); `header=None` if there are none.
- `encoding`: how text was saved (Q46). `na_values`: extra markers to read as missing, like "NA" or "-".
**Sample data:** `messy.csv` has 2 junk lines, then a semicolon-separated table where Ravi's salary is "NA" and Meena's is "-".
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv(
    "messy.csv",
    sep=";",                 # columns are separated by semicolons
    skiprows=2,              # skip the two junk lines above the header
    header=0,                # the next line is the header
    encoding="utf-8",        # how the text was saved
    na_values=["NA", "-"],   # treat these as missing
)
print(employees)
print(employees.dtypes)
```
**Output:**
```text
   employee_id   name   salary
0            1   Asha  45000.0
1            2   Ravi      NaN
2            3  Meena      NaN
employee_id      int64
name               str
salary         float64
dtype: object
```
**What it means:** The file loaded cleanly, and "NA" and "-" became real missing values, so salary is a number column (float64) instead of text.
**Likely follow-ups:** 1) *Why float?* NaN is a float, so a column with missing values becomes float. 2) *Text column dtype?* Shows `str` here (pandas 3.0, verified); older versions show `object`.
**Common mistakes:** Wrong `sep` (everything lands in one column); not telling pandas about "-" so the salary column stays text.

### Q45 ⭐⭐ 🟡 How do you read a specific sheet of an Excel workbook into pandas, and which extra library is needed?
**Asked at:** commonly asked (no company-specific report found); `read_excel` appears alongside `read_csv` in pandas basics guides.
**What the interviewer is checking:** Whether you know `sheet_name` and that Excel needs a helper library.
**Say this in the interview:** "I use `pd.read_excel` with `sheet_name`. For .xlsx files pandas needs the `openpyxl` library installed."
**Explain simply:**
- `sheet_name` takes the sheet's name (text) or its position (0 is the first sheet). Default is the first sheet.
- pandas itself does not read Excel; it relies on a helper library: `openpyxl` for .xlsx (install with `pip install openpyxl`). Older .xls files need `xlrd`.
- `sheet_name=None` reads all sheets into a dictionary of DataFrames.
**Sample data:** `hr_data.xlsx` with sheets "Employees" and "Attrition".
**Code (what you write in the interview):**
```python
import pandas as pd

# Needs openpyxl installed (pip install openpyxl) for .xlsx files
attrition = pd.read_excel("hr_data.xlsx", sheet_name="Attrition")
print(attrition)
```
**Output:**
```text
  month  leavers
0   Jan        3
1   Feb        5
```
**What it means:** Only the Attrition sheet was loaded, as its own table.
**Likely follow-ups:** 1) *What error if openpyxl is missing?* An `ImportError` asking you to install it (from memory, not triggered here). 2) *Read all sheets?* `sheet_name=None`.
**Common mistakes:** Misspelling the sheet name (case matters); forgetting the library; expecting merged cells or formulas to behave like in Excel.

### Q46 ⭐⭐ 🟡 What does the error UnicodeDecodeError mean when reading a CSV, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand text encodings, a very common real-world snag with HR exports.
**Say this in the interview:** "It means the file was saved with a different character encoding than the one pandas assumed, which is UTF-8. I fix it by passing the right `encoding`, commonly `latin-1` or `cp1252`."
**Explain simply:**
- Encoding is the rule that turns bytes in a file into letters. Accented names like José or Zoë are where rules differ.
- pandas tries UTF-8 first. If the file was saved in Excel on Windows, it is often `cp1252` or `latin-1`.
- Running the plain `read_csv` on my sample file gave: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 13`.
- Try `encoding="latin-1"` (it never fails but may show wrong characters if it is not the real encoding), or check the real one with a text editor.
**Sample data:** `names_latin.csv`, saved in latin-1, with names José and Zoë.
**Code (what you write in the interview):**
```python
import pandas as pd

# pd.read_csv("names_latin.csv") fails with UnicodeDecodeError, so tell pandas the real encoding
employees = pd.read_csv("names_latin.csv", encoding="latin-1")
print(employees)
```
**Output:**
```text
   name    city
0  José  Málaga
1   Zoë    Köln
```
**What it means:** With the right encoding, the accented names read correctly.
**Likely follow-ups:** 1) *Best way to avoid it?* Save files as UTF-8. 2) *What about `errors="replace"`?* `encoding_errors="replace"` swaps bad bytes for a symbol; loses data, last resort.
**Common mistakes:** Assuming the file is corrupt; guessing `latin-1` and not checking the names look right.

### Q47 ⭐⭐ 🟡 What does FileNotFoundError mean when calling read_csv(), and how do you check the file path and current working directory?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can debug a path problem methodically.
**Say this in the interview:** "It means Python cannot find a file at the path I gave. I check the current working directory with `os.getcwd()`, check the file exists with `os.path.exists()`, and then either move the file or use the full path."
**Explain simply:**
- A relative path like `"employees.csv"` is searched in the current working directory (the folder Python is running from), not where the script or notebook happens to be.
- Typos, wrong extension (`.csv` vs `.xlsx`) and hidden extensions are common.
- `os.listdir()` shows the files in the current folder.
- Windows paths: use forward slashes or a raw string `r"C:\data\employees.csv"`, because `\` is a special character.
**Code (what you write in the interview):**
```python
import os
import pandas as pd

# Where is Python looking right now?
print(os.getcwd())

# Does the file exist at that path?
print(os.path.exists("employees.csv"))

# Fix: use the full path, with forward slashes
# employees = pd.read_csv("/home/hr/data/employees.csv")
```
**Output:**
```text
/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/B03P04_Q39-57
False
```
**What it means:** Python is looking in that folder, and `employees.csv` is not there (False). The path printed will be your own folder on your machine.
**Likely follow-ups:** 1) *How to change the folder?* `os.chdir(path)`. 2) *Does `read_csv` accept a web URL?* Yes.
**Common mistakes:** Assuming the file is in the same folder as the notebook; typing a backslash path without a raw string; file open in another program is a different error (PermissionError).

### Q48 ⭐⭐ 🟡 How do you create a new column using a condition, for example 'High' if salary is above 60,000 else 'Low', using np.where()?
**Asked at:** commonly asked; Adaface lists "new column from conditions" among pandas questions.
**What the interviewer is checking:** Whether you can do an if/else on a whole column without a loop.
**Say this in the interview:** "`np.where` takes a condition, a value for True and a value for False. It works on the whole column at once, like an IF formula in Excel."
**Explain simply:**
- `np.where(condition, value_if_true, value_if_false)` (`np` is NumPy, the numbers library pandas is built on).
- Same idea as Excel `=IF(C2>60000,"High","Low")`, applied to every row.
- For three or more bands use `np.select` or `pd.cut`.
- Note: a missing salary makes the condition False, so it would be labelled "Low". Handle blanks separately.
**Sample data:** 4 employees with salary.
**Code (what you write in the interview):**
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": [45000, 62000, 38000, 70000],
})

# np.where(condition, value if True, value if False)
employees["salary_band"] = np.where(employees["salary"] > 60000, "High", "Low")
print(employees)
```
**Output:**
```text
    name  salary salary_band
0   Asha   45000         Low
1   Ravi   62000        High
2  Meena   38000         Low
3   John   70000        High
```
**What it means:** Ravi and John are above 60,000, so they get "High".
**Alternative:** `employees["salary"].apply(lambda s: "High" if s > 60000 else "Low")`; slower and longer, so `np.where` is preferred.
**Likely follow-ups:** 1) *Exactly 60,000?* `>` excludes it, so it is "Low"; use `>=` to include. 2) *Three bands?* `np.select`.
**Common mistakes:** Using Python `if` on a column; mixing up the True and False values; forgetting NaN falls into the False branch.

### Q49 ⭐⭐ 🟡 How do you sort a DataFrame by index, and what is the difference between sort_values() and sort_index()?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate "sort by content" from "sort by row label".
**Say this in the interview:** "`sort_values` sorts by what is inside a column. `sort_index` sorts by the row labels, the index."
**Explain simply:**
- The index is the row label on the far left (Q33). Here the labels are employee IDs.
- `sort_values("salary")` reorders rows by salary.
- `sort_index()` reorders rows by their ID labels.
- Both return a new DataFrame, and both accept `ascending=False`.
**Sample data:** 3 employees with IDs 103, 101, 102 as the index.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame(
    {"name": ["Asha", "Ravi", "Meena"], "salary": [45000, 62000, 38000]},
    index=[103, 101, 102],
)

# sort_values sorts by what is inside a column
by_salary = employees.sort_values("salary")

# sort_index sorts by the row labels
by_label = employees.sort_index()

print(by_salary)
print(by_label)
```
**Output:**
```text
      name  salary
102  Meena   38000
103   Asha   45000
101   Ravi   62000
      name  salary
101   Ravi   62000
102  Meena   38000
103   Asha   45000
```
**What it means:** First table is in salary order (lowest first); second is in ID order.
**Likely follow-ups:** 1) *Sort columns A to Z?* `sort_index(axis=1)`. 2) *Sort high to low?* `ascending=False`.
**Common mistakes:** Using `sort_values` with an index name and expecting it to work as a column in every version; forgetting to assign the result.

### Q50 ⭐⭐ 🟡 What does the inplace parameter do, and why is it better to assign the result back instead?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the modern, safer habit.
**Say this in the interview:** "`inplace=True` changes the DataFrame directly and returns nothing. I prefer assigning the result back, like `df = df.sort_values(...)`, because it is clearer, it can be chained, and `inplace` does not actually save memory or time."
**Explain simply:**
- Without `inplace`: the method returns a new DataFrame; the original is unchanged until you assign.
- With `inplace=True`: the original is changed and the method returns `None`.
- A classic bug: `df = df.sort_values("salary", inplace=True)` makes `df` become `None`.
- The pandas team discourages `inplace`, and it breaks method chaining (several steps joined with dots).
**Sample data:** 3 employees.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"name": ["Asha", "Ravi", "Meena"], "salary": [45000, 62000, 38000]})

# Recommended: assign the result back
employees = employees.sort_values("salary", ascending=False)

# inplace=True changes the DataFrame and returns None
employees.sort_values("salary", inplace=True)
print(employees)
```
**Output:**
```text
    name  salary
2  Meena   38000
0   Asha   45000
1   Ravi   62000
```
**What it means:** Both styles change the data (the second sort put it back lowest first); the first style is the one to use.
**Likely follow-ups:** 1) *Does inplace save memory?* Usually no; pandas often still makes a copy inside. 2) *Which methods have it?* `sort_values`, `drop`, `rename`, `fillna` and more.
**Common mistakes:** `df = df.method(inplace=True)` (result becomes None); expecting the original to change when you forgot to assign.

### Q51 ⭐⭐ 🟡 What is the difference between idxmax() and max()?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can find not just the highest value but who has it.
**Say this in the interview:** "`max()` gives the highest value. `idxmax()` gives the index label of the row that holds it, so I can look up who earns the maximum."
**Explain simply:**
- `max()` answers "how high?" (a salary number).
- `idxmax()` answers "which row?" (a row label); `idxmin()` is the lowest.
- Combine with `loc` to read other columns for that row.
- With ties, `idxmax()` returns the first one only.
**Sample data:** 4 employees with salary.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": [45000, 62000, 38000, 70000],
})

highest_salary = employees["salary"].max()
row_of_highest = employees["salary"].idxmax()

print(highest_salary)
print(row_of_highest)
print(employees.loc[row_of_highest, "name"])
```
**Output:**
```text
70000
3
John
```
**What it means:** The top salary is 70,000, it sits in row 3, and that employee is John.
**Likely follow-ups:** 1) *Ties?* Only the first is returned; filter `salary == max` to see all. 2) *Missing values?* Skipped by default.
**Common mistakes:** Expecting `idxmax()` to return the value; using the label as a position with `iloc` when the index is not 0, 1, 2.

### Q52 ⭐⭐ 🟡 How do you create a DataFrame from a Python dictionary and from a list of lists?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can build small test data by hand.
**Say this in the interview:** "From a dictionary, each key becomes a column name and each list is that column's values. From a list of lists, each inner list is a row, so I pass `columns=` to name them."
**Explain simply:**
- Dictionary of lists: easy to read column by column.
- List of lists: reads like rows in a spreadsheet; without `columns=` you get plain numbers 0, 1, 2 as headings.
- All columns or rows must have the same length, otherwise you get a `ValueError`.
- A list of dictionaries (one per row) also works.
**Code (what you write in the interview):**
```python
import pandas as pd

# From a dictionary: each key is a column
from_dictionary = pd.DataFrame({
    "name": ["Asha", "Ravi"],
    "salary": [45000, 62000],
})

# From a list of lists: each inner list is a row, so name the columns
from_rows = pd.DataFrame(
    [["Asha", 45000], ["Ravi", 62000]],
    columns=["name", "salary"],
)

print(from_dictionary)
print(from_rows)
```
**Output:**
```text
   name  salary
0  Asha   45000
1  Ravi   62000
   name  salary
0  Asha   45000
1  Ravi   62000
```
**What it means:** Both routes build the identical table.
**Likely follow-ups:** 1) *What if lists have different lengths?* `ValueError: All arrays must be of the same length`. 2) *Custom row labels?* `index=[...]`.
**Common mistakes:** Forgetting `columns=` for a list of lists; unequal list lengths; passing a plain dictionary of single values (needs `index=[0]`).

### Q53 ⭐⭐ 🟡 How do you select all columns of a particular data type, for example only numeric columns, using select_dtypes()?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can pick columns by type, handy before maths or summaries.
**Say this in the interview:** "`select_dtypes(include='number')` returns only the numeric columns. I can also use `exclude` to drop a type."
**Explain simply:**
- dtype means data type: numbers, text, dates and so on.
- `include="number"` covers whole numbers and decimals; `include="object"` or `"str"` is for text columns (the name depends on the pandas version).
- Handy to run `.describe()` or correlations only on number columns.
- It returns a new DataFrame with just those columns.
**Sample data:** 2 employees with name, department, salary, age.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi"],
    "department": ["Sales", "HR"],
    "salary": [45000, 62000],
    "age": [29, 41],
})

numeric_columns = employees.select_dtypes(include="number")
print(numeric_columns)

# The opposite: everything except numbers
text_columns = employees.select_dtypes(exclude="number")
print(text_columns.columns.tolist())
```
**Output:**
```text
   salary  age
0   45000   29
1   62000   41
['name', 'department']
```
**What it means:** Salary and age are numeric; name and department are text.
**Likely follow-ups:** 1) *Does an ID column count?* Yes, if stored as number; exclude it by name. 2) *Dates?* `include="datetime"`.
**Common mistakes:** Forgetting that numbers stored as text (Q54) are not selected; including IDs in maths.

### Q54 ⭐⭐ 🟡 Why does a column of numbers read as object dtype from a CSV, and how do you spot it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you check dtypes after loading, and know the usual dirty-data causes.
**Say this in the interview:** "If even one value in the column is not a clean number, like '45,000', 'N/A' or a stray space, pandas reads the whole column as text. I spot it with `dtypes` or `info()` and fix it by cleaning, then converting."
**Explain simply:**
- One bad cell makes the whole column text. Common causes: commas in numbers, currency symbols, "N/A" or "-", trailing spaces.
- Spot it: `df.dtypes` shows `object` (older pandas) or `str` (pandas 3.0, as in my run) for a column you expect to be numeric.
- Fix: clean the text, then `astype(int)`; or `pd.to_numeric(col, errors="coerce")` which turns bad values into NaN.
- Better: use `na_values` or `thousands=","` in `read_csv`.
**Sample data:** `salary_text.csv` where salaries are "45,000", 52000, "61,500".
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("salary_text.csv")
print(employees.dtypes)

# Fix: remove the commas, then convert to numbers
employees["salary"] = employees["salary"].str.replace(",", "").astype(int)
print(employees.dtypes)
```
**Output:**
```text
name      str
salary    str
dtype: object
name        str
salary    int64
dtype: object
```
**What it means:** Salary was text because of the commas; after cleaning it is a real number column (int64) you can add and average.
**Alternative:** `pd.read_csv("salary_text.csv", thousands=",")` reads it as numbers straight away.
**Likely follow-ups:** 1) *Why not just astype?* It fails on "45,000". 2) *Bad values you cannot clean?* `pd.to_numeric(..., errors="coerce")`.
**Common mistakes:** Not checking dtypes after loading; summing a text column (joins text or errors); using `astype(int)` on a column with NaN.

### Q55 ⭐⭐ 🟡 How do you reorder columns or move one column to the front of a DataFrame?
**Asked at:** commonly asked (no company-specific report found); a gap-fill practice question.
**What the interviewer is checking:** Whether you know that selecting columns in a list also reorders them.
**Say this in the interview:** "I select the columns again using a list in the order I want. To move one to the front, I put its name first in that list."
**Explain simply:**
- `df[["a", "b", "c"]]` returns the columns in exactly the order you list.
- Assign it back to keep the new order.
- For many columns, build the list with code: `["employee_id"] + [c for c in df.columns if c != "employee_id"]`.
- Columns you leave out of the list are dropped.
**Sample data:** 2 employees where `employee_id` is last.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi"],
    "salary": [45000, 62000],
    "employee_id": [101, 102],
})

# Reorder by listing the columns in the order you want
employees = employees[["employee_id", "name", "salary"]]
print(employees)
```
**Output:**
```text
   employee_id  name  salary
0          101  Asha   45000
1          102  Ravi   62000
```
**What it means:** The ID column now comes first; the data is unchanged.
**Likely follow-ups:** 1) *Many columns?* Build the list in code. 2) *Insert a new column at a position?* `employees.insert(0, "new_col", values)`.
**Common mistakes:** Using single brackets (returns one column); forgetting a column, which silently drops it.

### Q56 ⭐⭐ 🟡 How do you filter a DataFrame using multiple conditions with OR, for example employees in Sales or with salary above 80,000?
**Asked at:** commonly asked (no company-specific report found); the OR twin of the AND filter in Q13.
**What the interviewer is checking:** Whether you use `|` with brackets, not the word `or`.
**Say this in the interview:** "I put each condition in its own brackets and join them with the pipe symbol `|`, which means OR. The word `or` fails on a column."
**Explain simply:**
- `|` means OR (keep the row if either is true); `&` means AND; `~` means NOT.
- Brackets are needed because `|` is evaluated before `>` and `==`; without them you get an error.
- A row that meets both conditions appears once, not twice.
**Sample data:** 5 employees with department and salary.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "department": ["Sales", "HR", "Finance", "Finance", "Sales"],
    "salary": [45000, 52000, 38000, 85000, 61000],
})

# | means OR; each condition goes in its own brackets
sales_or_high_paid = employees[(employees["department"] == "Sales") | (employees["salary"] > 80000)]
print(sales_or_high_paid)
```
**Output:**
```text
    name department  salary
0   Asha      Sales   45000
3   John    Finance   85000
4  Priya      Sales   61000
```
**What it means:** Asha and Priya are in Sales; John is not in Sales but earns over 80,000, so he is included too.
**Alternative:** `employees.query("department == 'Sales' or salary > 80000")`.
**Likely follow-ups:** 1) *Why not `or`?* It tries to turn a whole column into one True/False and raises `ValueError`. 2) *Combine AND and OR?* Use extra brackets to make the order clear.
**Common mistakes:** Missing brackets; using `or` / `||`; mixing up AND and OR.

### Q57 ⭐⭐ 🔴 What is chained indexing, for example df[df['dept']=='Sales']['salary'] = 0, and why does it fail to update the original DataFrame?
**Asked at:** commonly asked (no company-specific report found); the pandas 3.0 Copy-on-Write change is documented in the pandas docs (PDEP-7).
**What the interviewer is checking:** Whether you understand views vs copies and know the one-step `loc` fix.
**Say this in the interview:** "Chained indexing means two selections in a row, like filter then pick a column, and then assigning to the result. The first selection returns a temporary copy, so I change the copy and the original is untouched. The fix is one `loc` step: `df.loc[condition, 'salary'] = 0`."
**Explain simply:**
- `df[df["dept"] == "Sales"]` makes a new filtered table; `["salary"] = 0` then writes into that temporary table, which is thrown away.
- In older pandas this sometimes worked and sometimes did not (hence `SettingWithCopyWarning`, Q16), which made it risky.
- In pandas 3.0 (Copy-on-Write) it never works; I ran it and got a `ChainedAssignmentError` warning and no change to the data.
- `loc[rows, column] = value` is a single operation on the original, so it always works.
**Sample data:** 3 employees; Asha and Meena are in Sales.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena"],
    "department": ["Sales", "HR", "Sales"],
    "salary": [45000, 52000, 38000],
})

# Chained: two steps, the first one makes a temporary copy
employees[employees["department"] == "Sales"]["salary"] = 0
print(employees)

# One step with loc updates the real DataFrame
employees.loc[employees["department"] == "Sales", "salary"] = 0
print(employees)
```
**Output:**
```text
ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment.
Such chained assignment never works to update the original DataFrame or Series, because the intermediate object on which we are setting values always behaves as a copy (due to Copy-on-Write).
(warning text shortened; it advises using .loc[row_indexer, col_indexer] = value)
    name department  salary
0   Asha      Sales   45000
1   Ravi         HR   52000
2  Meena      Sales   38000
    name department  salary
0   Asha      Sales       0
1   Ravi         HR   52000
2  Meena      Sales       0
```
**What it means:** The chained line changed nothing (salaries are still 45,000 and 38,000); the `loc` line set Sales salaries to 0.
**Likely follow-ups:** 1) *What did older pandas do?* Often showed `SettingWithCopyWarning` and sometimes updated, sometimes not (from memory, not run here). 2) *What is Copy-on-Write?* Any result of an operation behaves as its own copy, so you cannot accidentally change another object.
**Common mistakes:** Ignoring the warning; writing `df[mask]["col"] = value`; assuming it worked because no error stopped the code.

### Q58 ⭐ 🟡 How do you update the values of selected rows, for example give a 10% raise to employees in the Sales department, using loc?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the safe pattern `df.loc[rows, column] = new_value` for changing data in place?
**Say this in the interview:** "I build a True/False filter for Sales, then use loc with that filter and the salary column, and multiply by 1.10. loc changes the original table directly, with no warning."
**Explain simply:**
- `loc[rows, column]` means "these rows, this column". The first part is a True/False filter (a boolean mask); the second is the column to change.
- `*=` means "multiply the current value and store it back".
- Using one loc call (not two steps stacked together) is what makes the update land on the real DataFrame (see Q57).
- In pandas 3.0, if the column holds whole numbers (int) and the raise gives decimals, pandas stops with a `TypeError` instead of quietly converting. I ran this and saw it. Fix: store salary as decimals first, with `astype(float)`.
**Sample data:**
| emp_id | department | salary |
|---|---|---|
| 101 | Sales | 40000.0 |
| 102 | HR | 35000.0 |
| 103 | Sales | 50000.0 |
| 104 | Finance | 60000.0 |
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "emp_id": [101, 102, 103, 104],
    "department": ["Sales", "HR", "Sales", "Finance"],
    "salary": [40000.0, 35000.0, 50000.0, 60000.0],
})

# Select Sales rows and the salary column, then multiply by 1.10
is_sales = employees["department"] == "Sales"
employees.loc[is_sales, "salary"] *= 1.10
print(employees)
```
**Output:**
```
   emp_id department   salary
0     101      Sales  44000.0
1     102         HR  35000.0
2     103      Sales  55000.0
3     104    Finance  60000.0
```
**What it means:** Only the two Sales salaries went up by 10%; HR and Finance are untouched.
**Likely follow-ups:**
- *Why not `df[df.dept=="Sales"]["salary"] *= 1.1`?* That is chained indexing, which does not update the original (Q57).
- *How to raise Sales by 10% and HR by 5%?* Run a second loc line with its own filter.
**Common mistakes:** Forgetting that the filter must be a boolean mask of the same length; using `=` instead of `==` in the filter; trying to put decimals into an integer column.

### Q59 ⭐ 🟡 How do you set a column as the index and then select a row by that label, such as employee ID 105?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that the index is the row label and that `loc` reads by label?
**Say this in the interview:** "I call `set_index('emp_id')` so employee IDs become the row labels, then `loc[105]` returns that employee's row."
**Explain simply:**
- The index is the label column on the far left of a DataFrame. By default it is 0, 1, 2 and so on.
- `set_index` moves a column into that label position. It returns a new DataFrame, so assign it back.
- `loc[105]` looks for the label 105, not the 105th row. The employee does not have to be at position 105.
- If the ID is not found, you get a `KeyError`.
**Sample data:**
| emp_id | name | salary |
|---|---|---|
| 101 | Asha | 40000 |
| 103 | Ravi | 50000 |
| 105 | Meena | 45000 |
| 107 | John | 60000 |
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "emp_id": [101, 103, 105, 107],
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": [40000, 50000, 45000, 60000],
})

# Make emp_id the row label, then pick the row by that label
employees = employees.set_index("emp_id")
print(employees.loc[105])
```
**Output:**
```
name      Meena
salary    45000
Name: 105, dtype: object
```
**What it means:** We got Meena's full record, found by her ID.
**Likely follow-ups:**
- *Can the index have duplicates?* Yes, but then `loc[id]` returns several rows. Check with `employees.index.is_unique`.
- *How do I get emp_id back as a normal column?* `employees.reset_index()`.
**Common mistakes:** Not assigning the result of `set_index` back; using `iloc[105]` and getting an `IndexError` or the wrong person; forgetting that `loc[105]` with a single label returns a Series, while `loc[[105]]` returns a DataFrame.

### Q60 ⭐ 🟡 What is the difference between at/iat and loc/iloc?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know there is a fast, single-cell version of loc and iloc?
**Say this in the interview:** "`at` and `iat` read or write exactly one cell, so they are a bit faster. `at` uses labels like loc; `iat` uses positions like iloc. loc and iloc can handle many rows and columns at once."
**Explain simply:**
- `at[row_label, column_name]`: one cell by label.
- `iat[row_number, column_number]`: one cell by position (counting from 0).
- `loc` and `iloc` accept lists, slices and filters; `at` and `iat` accept only one row and one column.
- For one cell the speed gain is small, so it only matters when you loop over many cells. In an interview, loc/iloc is also fine.
**Sample data:**
| emp_id (index) | name | salary |
|---|---|---|
| 101 | Asha | 40000 |
| 103 | Ravi | 50000 |
| 105 | Meena | 45000 |
| 107 | John | 60000 |
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "emp_id": [101, 103, 105, 107],
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": [40000, 50000, 45000, 60000],
}).set_index("emp_id")

# By label: employee 105, column salary
print(employees.at[105, "salary"])

# By position: 3rd row (2), 2nd column (1), which is also salary
print(employees.iat[2, 1])

# Writing one cell
employees.at[105, "salary"] = 47000
print(employees.at[105, "salary"])
```
**Output:**
```
45000
45000
47000
```
**What it means:** Both ways reach Meena's salary; the label way survives re-sorting, the position way does not.
**Likely follow-ups:**
- *Can I give `at` a slice?* No, it is single-cell only.
**Common mistakes:** Passing a position to `at` (it wants labels) or a label to `iat`; expecting `at` to accept a filter.

### Q61 ⭐ 🟡 How do you select every second row of a DataFrame using slicing?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the slice pattern `start:stop:step`?
**Say this in the interview:** "I use `iloc[::2]`. The first two blanks mean 'from the start to the end' and the 2 is the step, so it takes rows 0, 2, 4 and so on."
**Explain simply:**
- A slice is `start:stop:step`. Leaving start and stop blank means "everything".
- Counting starts at 0, so `::2` gives the 1st, 3rd, 5th rows.
- For every second row starting from the 2nd row, use `iloc[1::2]`.
- `employees[::2]` also works on rows, but `iloc` makes it clear you mean positions.
**Sample data:** 6 employees (Asha, Ravi, Meena, John, Priya, Kiran) with salaries.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya", "Kiran"],
    "salary": [40000, 50000, 45000, 60000, 52000, 38000],
})

# Start to end, step 2: rows 0, 2, 4
print(employees.iloc[::2])
```
**Output:**
```
    name  salary
0   Asha   40000
2  Meena   45000
4  Priya   52000
```
**What it means:** We took alternate rows; the original row numbers (0, 2, 4) are kept as labels.
**Likely follow-ups:**
- *Why would an analyst do this?* To take a quick, evenly spread sample of sorted data. For a random sample use `sample()`.
**Common mistakes:** Thinking `::2` starts at the second row; confusing the step with the stop value.

### Q62 ⭐ 🟡 How do you sort a DataFrame by a text column with a custom order, for example Low, Medium, High, using a categorical type?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know sorting text is alphabetical by default, and how to fix it?
**Say this in the interview:** "Alphabetical order would give High, Low, Medium. I convert the column to an ordered categorical with the order I want, then sort."
**Explain simply:**
- A categorical column is a text column with a fixed list of allowed values. Here the list is Low, Medium, High.
- `ordered=True` tells pandas that Low is smaller than Medium, which is smaller than High.
- Sorting then follows that order, and comparisons like `risk_level > "Low"` work too.
- Values not in the list become missing (NaN), so spell the list carefully.
**Sample data:** 4 employees with an attrition risk level: Asha High, Ravi Low, Meena Medium, John Low.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "risk_level": ["High", "Low", "Medium", "Low"],
})

# Tell pandas the real order of the labels
risk_order = pd.CategoricalDtype(["Low", "Medium", "High"], ordered=True)
employees["risk_level"] = employees["risk_level"].astype(risk_order)

print(employees.sort_values("risk_level"))
```
**Output:**
```
    name risk_level
1   Ravi        Low
3   John        Low
2  Meena     Medium
0   Asha       High
```
**What it means:** Rows are now Low, Medium, High, as a manager would expect.
**Likely follow-ups:**
- *Alternative without categorical?* Map to numbers: `df["risk_level"].map({"Low": 1, "Medium": 2, "High": 3})` and sort by that, or use `sort_values(key=...)`.
**Common mistakes:** Forgetting `ordered=True`; typos or extra spaces in the data that turn values into NaN.

### Q63 ⭐ 🟡 How do you keep sorting stable and place missing values at the top or bottom using na_position?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know where missing values go and what "stable" means?
**Say this in the interview:** "By default missing values go last. `na_position='first'` puts them on top. A stable sort keeps tied rows in their original order, which I ask for with `kind='stable'`."
**Explain simply:**
- Stable sort: if two employees have the same salary, they stay in the same order as before.
- `na_position` takes `"last"` (default) or `"first"`.
- From memory (unverified here): the default `kind` for a single column is quicksort, which does not promise stability, so say `kind="stable"` when ties matter.
- NaN means "missing value" (blank salary).
**Sample data:**
| name | salary |
|---|---|
| Asha | 40000 |
| Ravi | missing |
| Meena | 40000 |
| John | 60000 |
| Priya | missing |
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "salary": [40000, None, 40000, 60000, None],
})

# Missing salaries at the top; equal salaries keep their original order
sorted_employees = employees.sort_values("salary", na_position="first", kind="stable")
print(sorted_employees)
```
**Output:**
```
    name   salary
1   Ravi      NaN
4  Priya      NaN
0   Asha  40000.0
2  Meena  40000.0
3   John  60000.0
```
**What it means:** Blank salaries are shown first so HR can chase them; Asha stays ahead of Meena as in the original.
**Likely follow-ups:**
- *Does it matter for multi-column sorts?* Ties are broken by the next column; stability only matters for rows tied on all sort columns.
**Common mistakes:** Assuming NaN sorts to the top (it is the bottom by default); assuming ties keep their order without asking.

### Q64 ⭐ 🟡 How do you read a CSV with a custom delimiter such as pipe or semicolon?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know `sep` and why a wrong value gives one giant column?
**Say this in the interview:** "A delimiter is the character that separates fields. I pass it with `sep`, for example `sep='|'` or `sep=';'`."
**Explain simply:**
- CSV means "comma-separated values", but exported files often use `;` (common in European Excel settings) or `|`.
- If `sep` is wrong, every row lands in one column and `shape` shows 1 column. That is the clue.
- `sep="\t"` reads tab-separated files.
- `sep=None, engine="python"` lets pandas guess, but being explicit is safer.
**Sample data:** Two small text files with the same 2 employees, one pipe-separated, one semicolon-separated.
**Code (what you write in the interview):**
```python
import pandas as pd
from io import StringIO

pipe_text = """emp_id|name|salary
101|Asha|40000
102|Ravi|50000"""

semicolon_text = """emp_id;name;salary
101;Asha;40000
102;Ravi;50000"""

employees = pd.read_csv(StringIO(pipe_text), sep="|")
print(employees)

# In a real file: pd.read_csv("employees.csv", sep=";")
employees = pd.read_csv(StringIO(semicolon_text), sep=";")
print(employees.shape)
```
**Output:**
```
   emp_id  name  salary
0     101  Asha   40000
1     102  Ravi   50000
(2, 3)
```
**What it means:** Both files load into 3 proper columns once the right separator is given.
**Likely follow-ups:**
- *How do you know the delimiter?* Open the file in a text editor or print the first line.
**Common mistakes:** Leaving the default comma; forgetting that `|` is a normal character here (no escaping needed with `sep="|"`).

### Q65 ⭐ 🟡 How do you rename the index or axis labels and set a column name for the index?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know `rename` (changes labels) versus `rename_axis` (changes the name of the axis)?
**Say this in the interview:** "`rename(index={old: new})` changes row labels. `rename_axis('emp_id')` gives a name to the index itself."
**Explain simply:**
- The index has two things: its labels (101, 102) and its own name (blank by default).
- `rename(index=...)` swaps labels using a dictionary of old to new; labels not listed stay as they are.
- `rename_axis("emp_id")` sets the name shown above the index. For the column headers use `rename_axis(columns="metric")`.
- Both return new objects, so assign the result back.
**Sample data:** 3 employees with index 101, 102, 103 and a salary column.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame(
    {"salary": [40000, 50000, 45000]},
    index=[101, 102, 103],
)

# Give the index a name
employees = employees.rename_axis("emp_id")

# Change some index labels
employees = employees.rename(index={101: 1001, 102: 1002})
print(employees)
```
**Output:**
```
        salary
emp_id        
1001     40000
1002     50000
103      45000
```
**What it means:** The index now has a heading, and the first two IDs were changed while 103 stayed.
**Likely follow-ups:**
- *How do I rename columns?* `rename(columns={...})` (Q18).
**Common mistakes:** Confusing `rename_axis` with `rename`; not assigning back.

### Q66 ⭐ 🟡 How do you filter columns by name pattern, for example all columns starting with 'Q1_' using filter() or str.startswith()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you pick columns by name rather than typing each one?
**Say this in the interview:** "`df.filter(regex='^Q1_')` keeps columns whose names start with Q1_. Or I check the column names with `str.startswith` and select those."
**Explain simply:**
- A regex is a text pattern; `^` means "starts with". `filter(like="Q1_")` is simpler but matches anywhere in the name.
- `df.columns.str.startswith("Q1_")` gives True/False for each column name.
- Useful for survey files with columns like `Q1_sales`, `Q2_sales`.
- `filter` works on columns by default; use `axis=0` for row labels.
**Sample data:** A survey table with columns `emp_id`, `Q1_sales`, `Q1_costs`, `Q2_sales`.
**Code (what you write in the interview):**
```python
import pandas as pd

survey = pd.DataFrame({
    "emp_id": [1, 2],
    "Q1_sales": [10, 20],
    "Q1_costs": [5, 6],
    "Q2_sales": [11, 21],
})

# Option 1: filter with a pattern (regex means a text pattern)
print(survey.filter(regex="^Q1_"))

# Option 2: str.startswith on the column names
q1_columns = survey.columns[survey.columns.str.startswith("Q1_")]
print(survey[q1_columns])
```
**Output:**
```
   Q1_sales  Q1_costs
0        10         5
1        20         6
   Q1_sales  Q1_costs
0        10         5
1        20         6
```
**What it means:** Both ways return only the Q1 columns; `emp_id` and Q2 are dropped.
**Likely follow-ups:**
- *Keep emp_id too?* `survey.loc[:, survey.columns.str.startswith("Q1_") | (survey.columns == "emp_id")]`, or build the list of names first.
**Common mistakes:** Forgetting `^`, so `Q1_` also matches names like `Prev_Q1_x`; using `df[...]` filter syntax meant for rows.

### Q67 ⭐ 🟡 How do you use where() and mask() to replace values by a condition without changing the shape of the DataFrame?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the difference between filtering (drops rows) and replacing (keeps shape)?
**Say this in the interview:** "`where` keeps a value when the condition is True and replaces it otherwise. `mask` is the opposite: it replaces where the condition is True. The table keeps the same number of rows."
**Explain simply:**
- Filtering with `df[df.salary > 50000]` removes rows; `where` and `mask` never do.
- Default replacement is NaN (missing); give a second value to use something else.
- Example: cap very high salaries at 100,000 for a report, or hide them with 0.
- Easy way to remember: `where` = "keep where true"; `mask` = "hide where true".
**Sample data:**
| name | salary |
|---|---|
| Asha | 40000 |
| Ravi | 90000 |
| Meena | 45000 |
| John | 120000 |
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John"],
    "salary": [40000, 90000, 45000, 120000],
})

# where: keep the value if the condition is True, otherwise replace it
employees["capped_salary"] = employees["salary"].where(employees["salary"] <= 100000, 100000)

# mask: the opposite, replace the value when the condition is True
employees["hidden_salary"] = employees["salary"].mask(employees["salary"] > 100000, 0)
print(employees)
```
**Output:**
```
    name  salary  capped_salary  hidden_salary
0   Asha   40000          40000          40000
1   Ravi   90000          90000          90000
2  Meena   45000          45000          45000
3   John  120000         100000              0
```
**What it means:** John's 120000 became 100000 in one column and 0 in the other; no row was lost.
**Likely follow-ups:**
- *Alternative?* `np.where(condition, a, b)` (Q48) or `clip(upper=100000)` for capping.
**Common mistakes:** Mixing up where and mask; expecting rows to disappear.

### Q68 ⭐ 🟡 How do you transpose a DataFrame, and when is it useful?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know `.T` swaps rows and columns?
**Say this in the interview:** "`df.T` flips rows into columns and columns into rows. It is useful when a small summary table reads better the other way round."
**Explain simply:**
- Transpose means turn the table on its side.
- Common use: the output of `describe()` or a small summary with many columns, so it fits on screen.
- Data types can change after a transpose: if columns have mixed types, everything may become `object`.
- It is for display or small tables, not a data-cleaning step on big data.
**Sample data:** A summary with rows `headcount`, `leavers` and columns `Sales`, `HR`.
**Code (what you write in the interview):**
```python
import pandas as pd

summary = pd.DataFrame(
    {"Sales": [10, 2], "HR": [5, 1]},
    index=["headcount", "leavers"],
)
print(summary.T)
```
**Output:**
```
       headcount  leavers
Sales         10        2
HR             5        1
```
**What it means:** Each department is now a row, which is easier to read with many metrics.
**Likely follow-ups:**
- *Same as `transpose()`?* Yes, `.T` is the short form.
**Common mistakes:** Transposing a big table and losing numeric dtypes; forgetting the result is a new DataFrame.

### Q69 ⭐ 🟡 How do you display all columns or more rows when a DataFrame is truncated in the notebook?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know pandas options and that truncation is only display, not data loss?
**Say this in the interview:** "I use `pd.set_option('display.max_columns', None)` and `display.max_rows`. The data is unchanged; only what the notebook shows changes."
**Explain simply:**
- By default pandas shows about 20 columns and 60 rows, with `...` in between.
- `None` means "no limit"; a number sets a limit.
- `pd.reset_option(name)` brings back the default.
- `pd.option_context(...)` with a `with` block changes the setting only temporarily.
**Code (what you write in the interview):**
```python
import pandas as pd

# Show every column and up to 100 rows
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

# Back to normal
pd.reset_option("display.max_columns")
pd.reset_option("display.max_rows")
```
**What it means:** The first two lines change only how much the notebook shows (verified: runs without error, no visible output); the last two restore the defaults.
**Likely follow-ups:**
- *Show wider text cells?* `pd.set_option("display.max_colwidth", None)`.
**Common mistakes:** Setting `max_rows` to a huge number and freezing the notebook on a million rows; thinking the data was cut.

### Q70 ⭐ 🟡 How do you check the memory used by a DataFrame, and how can the category dtype reduce it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know `memory_usage(deep=True)` and when text repeats a lot?
**Say this in the interview:** "`df.memory_usage(deep=True)` shows bytes per column. A text column with few distinct values, like department, is much smaller as category because pandas stores each value once plus small codes."
**Explain simply:**
- `deep=True` counts the real text size, not just pointers.
- Category dtype suits columns with few unique values repeated many times: department, gender, grade.
- It is a poor fit for columns that are mostly unique, like employee name.
- Bytes: divide by 1,000,000 for megabytes.
**Sample data:** 100,000 rows, department repeating among 3 values, and a numeric salary column.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Sales", "HR", "Finance", "Sales"] * 25000,
    "salary": range(100000),
})

before = employees.memory_usage(deep=True)
print(before)

employees["department"] = employees["department"].astype("category")
after = employees.memory_usage(deep=True)
print(after)
```
**Output:**
```
Index             132
department    5375000
salary         800000
dtype: int64
Index            132
department    100161
salary        800000
dtype: int64
```
**What it means:** The department column shrank from about 5.4 MB to about 0.1 MB. Exact bytes depend on the pandas version.
**Likely follow-ups:**
- *Other ways to save memory?* Read only needed columns (`usecols`) and use smaller number types (`int32`).
**Common mistakes:** Forgetting `deep=True` and underestimating text memory; converting high-variety columns to category.

### Q71 ⭐ 🟡 How do you read data directly from a URL or from an in-memory text string with read_csv?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know `read_csv` accepts more than a file path?
**Say this in the interview:** "For a URL I pass the web address to `read_csv`. For text already in memory I wrap it in `StringIO` so pandas treats it like a file."
**Explain simply:**
- `read_csv("https://...")` downloads and reads the file (needs internet; I did not run this line here).
- `StringIO` (from the standard `io` module) turns a string into a file-like object. Handy for tests and examples.
- Everything else (`sep`, `usecols`) works the same.
**Code (what you write in the interview):**
```python
import pandas as pd
from io import StringIO

csv_text = """emp_id,name,salary
101,Asha,40000
102,Ravi,50000"""

employees = pd.read_csv(StringIO(csv_text))
print(employees)

# From a web address (needs internet): pd.read_csv("https://example.com/employees.csv")
```
**Output:**
```
   emp_id  name  salary
0     101  Asha    40000
1     102  Ravi    50000
```
**What it means:** The text was read exactly like a file would be.
**Likely follow-ups:**
- *Why might a URL fail?* No internet, a login-protected link, or a link to a web page instead of the raw CSV.
**Common mistakes:** Passing the text string directly (pandas treats it as a file name and raises `FileNotFoundError`); using a GitHub page link instead of the "raw" link.

### Q72 ⭐ 🔴 What is a MultiIndex, and how do you select rows from one?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand hierarchical row labels and tuple selection?
**Say this in the interview:** "A MultiIndex uses two or more columns as the row label, like department then grade. I select the outer level with `loc['Sales']`, an exact row with a tuple like `loc[('HR','L2')]`, and an inner level with `xs`."
**Explain simply:**
- Think of a folder (department) with sub-folders (grade). Each row has a two-part label.
- `set_index([...])` with a list of columns builds it. `groupby` with two keys also produces one.
- `loc["Sales"]` gives all Sales rows; the tuple picks one exact row.
- `xs("L1", level="grade")` ("cross-section") picks a value from an inner level across all departments.
- `reset_index()` turns it back into normal columns.
**Sample data:**
| department | grade | headcount |
|---|---|---|
| Sales | L1 | 10 |
| Sales | L2 | 4 |
| HR | L1 | 3 |
| HR | L2 | 1 |
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Sales", "Sales", "HR", "HR"],
    "grade": ["L1", "L2", "L1", "L2"],
    "headcount": [10, 4, 3, 1],
}).set_index(["department", "grade"])
print(employees)

print(employees.loc["Sales"])
print(employees.loc[("HR", "L2")])
print(employees.xs("L1", level="grade"))
```
**Output:**
```
                  headcount
department grade           
Sales      L1            10
           L2             4
HR         L1             3
           L2             1
       headcount
grade           
L1            10
L2             4
headcount    1
Name: (HR, L2), dtype: int64
            headcount
department           
Sales              10
HR                  3
```
**What it means:** We read one department, one exact cell group, and one grade across all departments.
**Likely follow-ups:**
- *Is MultiIndex needed for analysis?* Often no; many analysts use `reset_index()` and plain filters, which are easier to read.
**Common mistakes:** Using `loc["L1"]` for an inner level (KeyError); slicing a MultiIndex that is not sorted.

### Q73 ⭐ 🔴 How do you read a large CSV file in chunks, and when is it needed?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you work with a file too big for memory?
**Say this in the interview:** "I pass `chunksize` to `read_csv`; it returns pieces one at a time. I process each piece, keep a running total, and never hold the whole file in memory."
**Explain simply:**
- Needed when the file is bigger than your computer's memory (for example, years of attendance swipes).
- `chunksize=4` means 4 rows per piece (use something like 100,000 for real files).
- Each chunk is a normal DataFrame. Keep only small results (sums, counts), not the chunks.
- Averages need a total and a count, not an average of chunk averages.
**Sample data:** 10 generated employee rows with salary 40001 to 40010.
**Code (what you write in the interview):**
```python
import pandas as pd
from io import StringIO

csv_text = "emp_id,department,salary\n" + "\n".join(
    f"{i},{'Sales' if i % 2 else 'HR'},{40000 + i}" for i in range(1, 11)
)

total_salary = 0
row_count = 0

# Read 4 rows at a time instead of the whole file
for chunk in pd.read_csv(StringIO(csv_text), chunksize=4):
    total_salary += chunk["salary"].sum()
    row_count += len(chunk)

print(row_count, total_salary / row_count)
```
**Output:**
```
10 40005.5
```
**What it means:** All 10 rows were counted across 3 chunks, giving the right average salary.
**Likely follow-ups:**
- *Other options?* `usecols`, smaller dtypes, or a database/SQL for very large data.
**Common mistakes:** Appending every chunk into one list and running out of memory anyway; averaging the chunk averages.

### Q74 ⭐ 🔴 How do you select the rows with the lowest salary in each department without groupby, using sort_values and iloc?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you solve "first row per group" without groupby?
**Say this in the interview:** "I sort by salary ascending, then `drop_duplicates('department')` keeps the first row per department, which is the lowest. If they insist on iloc, I loop over departments and take `iloc[0]` of each sorted slice."
**Explain simply:**
- Premise note: `iloc` alone cannot pick per group; the usual no-groupby trick is sort then `drop_duplicates`. The iloc version needs a small loop.
- `drop_duplicates(subset)` keeps the first row for each value, so sorting first decides who is "first".
- Ties: if two people have the same lowest salary, only one is kept (the first one after sorting).
- For a tie-friendly version, use `groupby` with `transform("min")` (not "without groupby", so only as a mention).
**Sample data:**
| name | department | salary |
|---|---|---|
| Asha | Sales | 40000 |
| Ravi | Sales | 35000 |
| Meena | HR | 45000 |
| John | HR | 30000 |
| Priya | Finance | 60000 |
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya"],
    "department": ["Sales", "Sales", "HR", "HR", "Finance"],
    "salary": [40000, 35000, 45000, 30000, 60000],
})

# Lowest salary first, then keep the first row seen for each department
lowest_paid = employees.sort_values("salary").drop_duplicates("department")
print(lowest_paid)

# With iloc: loop over departments, take row 0 after sorting
rows = []
for department in employees["department"].unique():
    in_department = employees[employees["department"] == department]
    rows.append(in_department.sort_values("salary").iloc[0])
print(pd.DataFrame(rows))
```
**Output:**
```
    name department  salary
3   John         HR   30000
1   Ravi      Sales   35000
4  Priya    Finance   60000
    name department  salary
1   Ravi      Sales   35000
3   John         HR   30000
4  Priya    Finance   60000
```
**What it means:** Each department appears once with its lowest-paid employee (Ravi in Sales, John in HR, Priya in Finance).
**Likely follow-ups:**
- *Highest instead?* Sort with `ascending=False`.
**Common mistakes:** Forgetting to sort before `drop_duplicates`; sorting only by department; ignoring ties.

### Q75 ⭐ 🔴 What changed with Copy-on-Write in pandas 3.0, and what does it mean for SettingWithCopyWarning?
**Asked at:** commonly asked (no company-specific report found); the pandas 3.0 change is described in the pandas Copy-on-Write proposal (PDEP-7) and 2026 blog posts.
**What the interviewer is checking:** Do you know current pandas behaviour and not just old tutorials?
**Say this in the interview:** "From pandas 3.0, Copy-on-Write is always on: any subset or derived DataFrame behaves as its own copy, so changing it never changes the original. SettingWithCopyWarning is gone, and chained assignment simply does not update the original."
**Explain simply:**
- Copy-on-Write means pandas copies data only at the moment you change it, so results behave like independent copies without wasting memory.
- Before 3.0, `sales = df[df.dept == "Sales"]` might or might not be a view of `df`; that confusion caused SettingWithCopyWarning.
- In 3.0 the answer is simple: it is never linked to `df`.
- Chained assignment (`df[mask]["col"] = 0`) now does nothing to `df`; I ran it on pandas 3.0.5 and saw a `ChainedAssignmentError` warning.
- To update the original, write `df.loc[mask, "col"] = value` (Q58). `inplace=True` is not needed.
**Sample data:** 3 employees: Sales 40000, HR 35000, Sales 50000.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Sales", "HR", "Sales"],
    "salary": [40000, 35000, 50000],
})

# 1. Chained assignment: no longer changes the original
employees[employees["department"] == "Sales"]["salary"] = 0
print(employees["salary"].tolist())

# 2. A subset is its own copy
sales = employees[employees["department"] == "Sales"]
sales.loc[:, "salary"] = 0
print(employees["salary"].tolist())

# 3. Correct way
employees.loc[employees["department"] == "Sales", "salary"] = 0
print(employees["salary"].tolist())
```
**Output:**
```
[40000, 35000, 50000]
[40000, 35000, 50000]
[0, 35000, 0]
```
(Step 1 also printed a `ChainedAssignmentError` warning on pandas 3.0.5.)
**What it means:** Steps 1 and 2 left the original unchanged; only the single loc line in step 3 updated it.
**Likely follow-ups:**
- *Do I still need `.copy()`?* Not to protect the original, but it does no harm and keeps code readable for older pandas.
- *What about pandas 2.x?* From memory (unverified here): the warning existed and Copy-on-Write was opt-in.
**Common mistakes:** Believing SettingWithCopyWarning still protects you; writing old-style chained assignment and wondering why nothing changes.

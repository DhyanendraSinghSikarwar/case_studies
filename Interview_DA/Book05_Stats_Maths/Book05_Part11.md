# Book 5 — Statistics & Maths for Data Analysts | Part 11: Stats in Excel & Python 🟢🟡

**Target:** 30 questions | **Actual:** 34 questions
**Scope:** Excel and Python/pandas functions and one-liners for descriptive stats, percentiles, outliers, correlation, regression, t-test, chi-square and confidence intervals.

### Q1 ⭐⭐⭐ 🟢 Which Excel functions do you use to find the mean, median and mode of a column of salaries?
**Asked at:** commonly asked (no company-specific report found); appears in generic Excel and DA prep lists (Analytics Vidhya, Interview Query; search snippets only).
**What the interviewer is checking:** Do you know the three "centre" measures and which one to trust when salaries are skewed?
**Say this in the interview:** "I use AVERAGE for the mean, MEDIAN for the middle value and MODE.SNGL for the most common value. For salaries I report the median too, because a few very high salaries pull the mean up."
**Explain simply:**
- **Mean** = add everything up, divide by how many values: `=AVERAGE(B2:B11)`.
- **Median** = the middle value once sorted: `=MEDIAN(B2:B11)`. Half the staff earn less, half earn more.
- **Mode** = the value that appears most often: `=MODE.SNGL(B2:B11)` (Excel 2010+; the older `MODE` still works). `MODE.MULT` returns all modes if there is a tie.
- If there is no repeated value, MODE.SNGL returns #N/A.
**Worked example:** Ten monthly salaries in B2:B11: 30000, 35000, 35000, 42000, 45000, 48000, 52000, 60000, 75000, 150000. The mean is 57,200, the median is 46,500 and the mode is 35,000. One director at 150,000 drags the mean far above what a typical employee earns, so the median (46,500) describes the "typical" person better.
**Excel / Python:**
```python
import pandas as pd

# Ten monthly salaries (one very high value at the end)
monthly_salaries = pd.Series([30000, 35000, 35000, 42000, 45000,
                              48000, 52000, 60000, 75000, 150000])

# Mean = sum divided by count
print("mean", monthly_salaries.mean())

# Median = middle value after sorting
print("median", monthly_salaries.median())

# Mode = most frequent value (returned as a list because there can be ties)
print("mode", monthly_salaries.mode().tolist())
```
```
mean 57200.0
median 46500.0
mode [35000]
```
The Excel formulas above give the same three numbers (checked against Python; not run in Excel here).
**Likely follow-ups:** 1) *Which is best for salaries?* Median, because it ignores extreme values. 2) *Can there be two modes?* Yes; MODE.MULT or pandas `mode()` shows all.
**Common mistakes:** Reporting only the mean for skewed pay data; forgetting that text or blank cells are ignored by AVERAGE.

### Q2 ⭐⭐⭐ 🟢 How do you get a quick statistical summary of a dataset in Python using pandas describe()?
**Asked at:** commonly asked (no company-specific report found); describe() appears in pandas cheat sheets for analysts (Medium, GoLinuxCloud; snippets only).
**What the interviewer is checking:** Can you take a first look at a new dataset in one line and read the output?
**Say this in the interview:** "I call `df.describe()`. For numeric columns it gives count, mean, standard deviation, min, the 25th, 50th and 75th percentiles and max. With `include='all'` it also summarises text columns."
**Explain simply:**
- **count** = non-missing values; if it is lower than the row count, you have missing data.
- **std** = standard deviation, how spread out values are (sample version, divides by n-1).
- **25% / 50% / 75%** = quartiles; 50% is the median.
- By default only numeric columns are shown. Text columns need `include="all"` (then you see unique, top, freq).
**Worked example:** Eight employees with age, salary and attrition (left company Yes/No).
**Excel / Python:**
```python
import pandas as pd

# Small HR table: age, monthly salary and whether the person left
employees = pd.DataFrame({
    "age": [24, 28, 31, 35, 29, 42, 38, 26],
    "salary": [30000, 35000, 45000, 52000, 40000, 75000, 60000, 32000],
    "attrition": ["No", "Yes", "No", "No", "Yes", "No", "No", "Yes"]})

# Summary of the numeric columns
print(employees.describe())
```
```
             age        salary
count   8.000000      8.000000
mean   31.625000  46125.000000
std     6.209152  15505.183465
min    24.000000  30000.000000
25%    27.500000  34250.000000
50%    30.000000  42500.000000
75%    35.750000  54000.000000
max    42.000000  75000.000000
```
Average salary is 46,125 but the median is 42,500, so a few higher salaries pull the average up. The attrition column is skipped because it is text.
**Likely follow-ups:** 1) *How do I include text columns?* `describe(include="all")`. 2) *How do I get other percentiles?* `describe(percentiles=[0.1, 0.9])`.
**Common mistakes:** Not noticing the count is below the row count; reading std as the "average difference" without knowing it is n-1 based.

### Q3 ⭐⭐⭐ 🟢 What is the difference between COUNT, COUNTA, COUNTBLANK and COUNTIF in Excel?
**Asked at:** commonly asked (no company-specific report found); the COUNT/COUNTA/COUNTBLANK trio appears in Excel FAQ lists (Scribd upload, weak source).
**What the interviewer is checking:** Do you know exactly what each function counts (numbers, non-empty, empty, or matching a rule)?
**Say this in the interview:** "COUNT counts only numbers, COUNTA counts anything not empty, COUNTBLANK counts empty cells, and COUNTIF counts cells that meet one condition."
**Explain simply:**
- `COUNT(range)`: numbers only (dates count too, they are numbers inside Excel). Text and blanks are ignored.
- `COUNTA(range)`: every non-empty cell, numbers and text.
- `COUNTBLANK(range)`: empty cells (and cells holding `""`).
- `COUNTIF(range, condition)`: cells that match, e.g. `">=45000"`. For several conditions use `COUNTIFS`.
**Worked example:** Cells A2:A8 hold: 40000, 52000, (blank), Asha, 45000, (blank), 38000.
- `=COUNT(A2:A8)` returns 4 (the four numbers)
- `=COUNTA(A2:A8)` returns 5 (four numbers plus the text "Asha")
- `=COUNTBLANK(A2:A8)` returns 2
- `=COUNTIF(A2:A8,">=45000")` returns 2 (52000 and 45000)

Checked by counting the same list in Python (4, 5, 2, 2); not run in Excel here. Note 4 + 1 text + 2 blanks = 7 cells.
**Excel / Python:**
```python
import pandas as pd

# The same seven cells; None means an empty cell
cells = pd.Series([40000, 52000, None, "Asha", 45000, None, 38000])

# COUNT: numbers only
numbers_only = sum(isinstance(value, (int, float)) and not pd.isna(value) for value in cells)

# COUNTA: anything that is not empty
non_empty = sum(not pd.isna(value) for value in cells)

# COUNTBLANK: empty cells
blanks = sum(pd.isna(value) for value in cells)

# COUNTIF >= 45000: numbers meeting the rule
at_least_45000 = sum(isinstance(value, (int, float)) and not pd.isna(value) and value >= 45000
                     for value in cells)

print(numbers_only, non_empty, blanks, at_least_45000)
```
```
4 5 2 2
```
The four numbers match COUNT, COUNTA, COUNTBLANK and COUNTIF in that order.
**Likely follow-ups:** 1) *Which one finds missing salaries?* COUNTBLANK, or COUNTA vs total rows. 2) *Multiple conditions?* COUNTIFS.
**Common mistakes:** Using COUNT on a text column and getting 0; forgetting that a cell with a space looks blank but is counted by COUNTA.

### Q4 ⭐⭐⭐ 🟢 How do you calculate the average salary per department using a pandas groupby?
**Asked at:** commonly asked (no company-specific report found); groupby is a standard pandas question in analyst lists (GoLinuxCloud, Medium; snippets only).
**What the interviewer is checking:** Can you do "split into groups, then calculate" in pandas, the equivalent of a pivot table or SQL GROUP BY?
**Say this in the interview:** "I use `df.groupby('department')['salary'].mean()`. It splits the rows by department, then averages salary inside each group. If I want several measures I use `.agg(['mean','count','max'])`."
**Explain simply:**
- groupby = sort the rows into piles by a column, then calculate on each pile.
- Pick the column to calculate on (`['salary']`) before the function (`.mean()`).
- `.agg([...])` gives several statistics in one table.
- Output is indexed by department; use `.reset_index()` if you want it as a normal table.
**Worked example:** Seven staff in three departments.
**Excel / Python:**
```python
import pandas as pd

# Seven employees with department and salary
staff = pd.DataFrame({
    "department": ["Sales", "Sales", "HR", "HR", "IT", "IT", "IT"],
    "salary": [40000, 50000, 35000, 45000, 60000, 70000, 80000]})

# Average salary per department
average_salary_by_department = staff.groupby("department")["salary"].mean()
print(average_salary_by_department)

# Average, headcount and highest salary together
summary_by_department = staff.groupby("department")["salary"].agg(["mean", "count", "max"])
print(summary_by_department)
```
```
department
HR       40000.0
IT       70000.0
Sales    45000.0
Name: salary, dtype: float64
               mean  count    max
department                       
HR          40000.0      2  45000
IT          70000.0      3  80000
Sales       45000.0      2  50000
```
IT pays the most on average (70,000) and has the most people (3).
**Likely follow-ups:** 1) *How is this different from a pivot table?* Same idea, written as code so it can be repeated. 2) *Group by two columns?* `groupby(["department", "city"])`.
**Common mistakes:** Forgetting to choose a column, so pandas tries to average every column; not noticing groupby drops rows whose group is missing.

### Q5 ⭐⭐⭐ 🟢 What is the difference between AVERAGE, AVERAGEIF and AVERAGEIFS in Excel, and how would you find the average salary of the Sales team in Hyderabad?
**Asked at:** commonly asked (no company-specific report found); conditional functions are in generic Excel lists (Minova junior DA guide, snippet only).
**What the interviewer is checking:** Can you average only the rows that meet one or more conditions?
**Say this in the interview:** "AVERAGE averages everything, AVERAGEIF averages rows meeting one condition, AVERAGEIFS meets several conditions at once. For Sales in Hyderabad I use AVERAGEIFS with two condition pairs."
**Explain simply:**
- `AVERAGE(range)`: plain average of all numbers.
- `AVERAGEIF(condition_range, condition, average_range)`: one rule.
- `AVERAGEIFS(average_range, cond_range1, cond1, cond_range2, cond2, ...)`: several rules, all must be true. Careful: the range to average comes FIRST here, but LAST in AVERAGEIF.
- If no row matches, you get #DIV/0!. AVERAGEIFS exists in Excel 2007+.
**Worked example:** Layout: A2:A7 team, B2:B7 city, C2:C7 salary.

| team | city | salary |
|---|---|---|
| Sales | Hyderabad | 40000 |
| Sales | Hyderabad | 50000 |
| Sales | Bengaluru | 80000 |
| HR | Hyderabad | 35000 |
| Sales | Hyderabad | 60000 |
| IT | Hyderabad | 70000 |

- `=AVERAGE(C2:C7)` returns 55,833.33
- `=AVERAGEIF(A2:A7,"Sales",C2:C7)` returns 57,500 (all four Sales rows)
- `=AVERAGEIFS(C2:C7,A2:A7,"Sales",B2:B7,"Hyderabad")` returns 50,000 (the three Hyderabad Sales rows: 40000, 50000, 60000)

Values checked in Python; formulas not run in Excel here.
**Excel / Python:**
```python
import pandas as pd

# Same six rows as the sheet
rows = pd.DataFrame({
    "team": ["Sales", "Sales", "Sales", "HR", "Sales", "IT"],
    "city": ["Hyderabad", "Hyderabad", "Bengaluru", "Hyderabad", "Hyderabad", "Hyderabad"],
    "salary": [40000, 50000, 80000, 35000, 60000, 70000]})

# Keep only Sales rows that are also in Hyderabad
is_sales_in_hyderabad = (rows["team"] == "Sales") & (rows["city"] == "Hyderabad")

# Average salary of those rows only
print(rows[is_sales_in_hyderabad]["salary"].mean())
```
```
50000.0
```
Only three rows pass both tests, and their average is 50,000.
**Likely follow-ups:** 1) *Why not AVERAGEIF twice?* It handles one condition only. 2) *Text conditions?* Not case sensitive; wildcards like "Sal*" work.
**Common mistakes:** Mixing up the argument order of AVERAGEIFS; using ranges of different sizes (gives #VALUE!).

### Q6 ⭐⭐⭐ 🟢 What is the difference between STDEV.S and STDEV.P in Excel, and which one do you use for a sample of 50 employees?
**Asked at:** commonly asked (no company-specific report found); the n vs n-1 difference is covered in Excel statistics references (CASRAI, snippet only).
**What the interviewer is checking:** Do you know when your data is a sample and when it is the whole population?
**Say this in the interview:** "STDEV.S divides by n minus 1 and is for a sample; STDEV.P divides by n and is for the whole population. Fifty employees picked from a company of thousands is a sample, so I use STDEV.S."
**Explain simply:**
- **Standard deviation** = typical distance of values from the average.
- A sample tends to understate the true spread, so we divide by n-1 to correct it (called Bessel's correction).
- If your 50 people are ALL the employees you care about, that is the population and STDEV.P is right.
- The two get closer as the data gets bigger.
- STDEV.S and STDEV.P need Excel 2010+ (older: STDEV and STDEVP).
**Formula in plain words:** spread = square root of (sum of squared distances from the mean, divided by n-1 for a sample or n for a population). In symbols: s = sqrt( sum((x - mean)^2) / (n - 1) ).
**Worked example:** Six salaries in B2:B7: 30000, 35000, 42000, 45000, 52000, 60000. `=STDEV.S(B2:B7)` returns 10,972.69; `=STDEV.P(B2:B7)` returns 10,016.65.
**Excel / Python:**
```python
import numpy as np

# Six monthly salaries
salaries = np.array([30000, 35000, 42000, 45000, 52000, 60000])

# Sample standard deviation: divide by n-1 (like STDEV.S)
sample_std = salaries.std(ddof=1)

# Population standard deviation: divide by n (like STDEV.P)
population_std = salaries.std(ddof=0)

print("sample", sample_std)
print("population", population_std)
```
```
sample 10972.693379476163
population 10016.652800877813
```
The sample figure is larger because it divides by 5 instead of 6.
**Likely follow-ups:** 1) *What about the 50 employees being the whole team?* Then population, STDEV.P. 2) *Which do tests use?* The sample version.
**Common mistakes:** Using STDEV.P by default; mixing it up with the old STDEV function (which is sample).

### Q7 ⭐⭐⭐ 🟢 How do you calculate the correlation between two columns (for example, experience and salary) in Excel and in Python?
**Asked at:** commonly asked (no company-specific report found); corr() is in pandas cheat sheets for analysts (Medium; snippet only).
**What the interviewer is checking:** Can you measure how strongly two numbers move together, and do you know correlation is not causation?
**Say this in the interview:** "In Excel I use `=CORREL(A2:A7,B2:B7)`. In pandas it is `df['experience'].corr(df['salary'])`. The result runs from -1 to +1; near +1 means salary rises with experience."
**Explain simply:**
- **Correlation (Pearson r)** measures straight-line association: +1 perfect upward, -1 perfect downward, 0 none.
- It only shows they move together, not that one causes the other.
- Both columns must be numeric and of equal length; pairs with missing values are skipped in pandas.
**Worked example:** Experience (years) in A2:A7 = 1, 2, 3, 5, 7, 10; salary in B2:B7 = 30000, 34000, 41000, 48000, 60000, 75000. `=CORREL(A2:A7,B2:B7)` returns 0.9981, a very strong positive link.
**Excel / Python:**
```python
import pandas as pd

# Experience in years and the matching salary
experience_and_salary = pd.DataFrame({
    "experience_years": [1, 2, 3, 5, 7, 10],
    "salary": [30000, 34000, 41000, 48000, 60000, 75000]})

# Correlation between two columns
correlation = experience_and_salary["experience_years"].corr(experience_and_salary["salary"])
print(correlation)
```
```
0.9981496767271922
```
A value this close to 1 means salary rises almost in a straight line with experience in this made-up data. Excel's CORREL gives the same number (not run in Excel here).
**Likely follow-ups:** 1) *Does r = 0 mean no relationship?* Only no straight-line one; a curve can hide. 2) *Which Excel functions?* CORREL or PEARSON.
**Common mistakes:** Saying high correlation proves causation; ignoring outliers that can distort r.

### Q8 ⭐⭐⭐ 🟡 Why does np.std give a different answer from pandas .std(), and what is ddof?
**Asked at:** commonly asked (no company-specific report found); the numpy vs pandas default is a well-known gotcha (Gorelik blog, 2017; snippet only).
**What the interviewer is checking:** Do you know the two libraries use different defaults for sample vs population?
**Say this in the interview:** "ddof means 'delta degrees of freedom', the number subtracted from n in the divisor. numpy defaults to ddof=0 (population), pandas defaults to ddof=1 (sample). Set `ddof=1` in numpy, or `ddof=0` in pandas, to make them match."
**Explain simply:**
- Divisor = n minus ddof.
- `np.std(data)` uses ddof=0, so it divides by n.
- `Series.std()` uses ddof=1, so it divides by n-1.
- pandas also skips missing values by default; plain numpy functions return NaN if any value is missing.
**Worked example:** Same six salaries as Q6.
**Excel / Python:**
```python
import numpy as np
import pandas as pd

# Six salaries
salaries = [30000, 35000, 42000, 45000, 52000, 60000]

# numpy default: ddof=0 (population)
print("numpy default   ", np.std(salaries))

# pandas default: ddof=1 (sample)
print("pandas default  ", pd.Series(salaries).std())

# Make numpy behave like pandas
print("numpy ddof=1    ", np.std(salaries, ddof=1))

# Make pandas behave like numpy
print("pandas ddof=0   ", pd.Series(salaries).std(ddof=0))
```
```
numpy default    10016.652800877813
pandas default   10972.693379476163
numpy ddof=1     10972.693379476163
pandas ddof=0    10016.652800877813
```
The numbers differ only because of the divisor; neither is wrong. For a sample of employees, the ddof=1 figure (10,972.69) is the right one.
**Likely follow-ups:** 1) *Which is STDEV.S in Excel?* ddof=1. 2) *Does ddof matter for large data?* Barely.
**Common mistakes:** Comparing numpy and pandas results and thinking one is buggy; using ddof=0 on a sample.

### Q9 ⭐⭐ 🟢 How do you calculate a weighted average in Excel using SUMPRODUCT, and how do you do it in Python?
**Asked at:** commonly asked (no company-specific report found); a standard Excel analyst question (standard practice, no named source).
**What the interviewer is checking:** Do you know that some values count more than others, and how to compute that?
**Say this in the interview:** "A weighted average multiplies each value by its weight, adds them up, and divides by the total weight. In Excel: `=SUMPRODUCT(values, weights)/SUM(weights)`. In Python I use `np.average(values, weights=weights)`."
**Explain simply:**
- A normal average treats every value equally; a weighted average lets important items count more.
- Examples: performance rating made of KPIs with different importance; average pay across departments of different sizes.
- If weights already add up to 1 (100%), you can skip the division, but dividing is a safe habit.
**Formula in plain words:** sum of (value times weight), divided by sum of weights. In symbols: sum(w*x) / sum(w).
**Worked example:** An employee's score: Delivery 4.0 (weight 50%), Teamwork 3.0 (30%), Learning 5.0 (20%). Scores in B2:B4, weights in C2:C4: `=SUMPRODUCT(B2:B4,C2:C4)/SUM(C2:C4)` returns 3.9 (2.0 + 0.9 + 1.0). A plain average would give 4.0, which hides that teamwork counts more than learning.
**Excel / Python:**
```python
import numpy as np

# Scores for each criterion and how much each criterion matters
scores = np.array([4.0, 3.0, 5.0])
weights = np.array([0.5, 0.3, 0.2])

# Multiply each score by its weight, add up, divide by total weight
weighted_average = (scores * weights).sum() / weights.sum()
print(weighted_average)

# Same thing with the built-in helper
print(np.average(scores, weights=weights))
```
```
3.9
3.9
```
Both routes give 3.9, matching the Excel formula (not run in Excel here).
**Likely follow-ups:** 1) *Why not AVERAGE?* It ignores importance. 2) *Does SUMPRODUCT need equal sizes?* Yes, or #VALUE!.
**Common mistakes:** Averaging the department averages without weighting by headcount.

### Q10 ⭐⭐ 🟢 How do you find quartiles and percentiles in Excel, and what is the difference between PERCENTILE.INC and PERCENTILE.EXC?
**Asked at:** commonly asked (no company-specific report found); the INC/EXC functions are listed in Microsoft's statistical functions reference (snippet only).
**What the interviewer is checking:** Do you know what a percentile means and that Excel has two calculation methods?
**Say this in the interview:** "A percentile is the value below which a given percent of the data falls. QUARTILE.INC and PERCENTILE.INC include the min and max as 0% and 100%; the EXC versions exclude them, so they only work for a narrower range and can give slightly different answers."
**Explain simply:**
- Quartiles split sorted data into four parts: Q1 = 25th percentile, Q2 = median, Q3 = 75th percentile.
- `=QUARTILE.INC(range,1)` or `=PERCENTILE.INC(range,0.25)` (Excel 2010+; matches pandas `quantile()` and numpy defaults).
- `.EXC` works with positions 1 to n+1 so percentiles below 1/(n+1) or above n/(n+1) return #NUM!.
- For small data the two methods differ; for large data they converge.
**Worked example:** Eight salaries (in thousands) in A2:A9: 30, 35, 42, 45, 52, 60, 75, 90.
- `=PERCENTILE.INC(A2:A9,0.25)` returns 40.25 (position 0.25 x 7 = 1.75, so 35 + 0.75 x 7)
- `=PERCENTILE.EXC(A2:A9,0.25)` returns 36.75 (position 0.25 x 9 = 2.25, so 35 + 0.25 x 7)
- `=PERCENTILE.INC(A2:A9,0.75)` returns 63.75; `.EXC` returns 71.25
- `=PERCENTILE.EXC(A2:A9,0.9)` returns #NUM! here, because 0.9 is above 8/9 = 0.889.
**Excel / Python:**
```python
import numpy as np

# Eight salaries in thousands
salaries_in_thousands = np.array([30, 35, 42, 45, 52, 60, 75, 90])

# INC method (numpy default, same as PERCENTILE.INC)
print("INC 25th", np.percentile(salaries_in_thousands, 25))
print("INC 75th", np.percentile(salaries_in_thousands, 75))

# EXC method (numpy calls it "weibull")
print("EXC 25th", np.percentile(salaries_in_thousands, 25, method="weibull"))
print("EXC 75th", np.percentile(salaries_in_thousands, 75, method="weibull"))
```
```
INC 25th 40.25
INC 75th 63.75
EXC 25th 36.75
EXC 75th 71.25
```
Same data, two methods, two answers. State which one you used. Python's numpy would silently cap the EXC 90th percentile at 90, while Excel returns an error. EXC formulas not run in Excel here; numbers computed in Python.
**Likely follow-ups:** 1) *Which should I use?* INC is the common default. 2) *Is PERCENTILE the same as .INC?* Yes, the old function equals INC.
**Common mistakes:** Entering 25 instead of 0.25; comparing results from tools that use different methods.

### Q11 ⭐⭐ 🟢 How do you check for missing values in pandas, and how does a missing value affect mean(), sum() and count()?
**Asked at:** commonly asked (no company-specific report found); data-cleaning questions are standard in pandas lists (standard practice, no named source).
**What the interviewer is checking:** Can you find missing data and do you know pandas skips it by default?
**Say this in the interview:** "I use `df.isna().sum()` to count missing values per column. By default mean() and sum() skip missing values, and count() counts only the non-missing ones, so mean is based on fewer rows than the table has."
**Explain simply:**
- Missing values show up as NaN (not a number).
- `isna()` marks each cell True or False; `.sum()` adds the Trues; `.mean()` gives the share missing.
- `skipna=True` is the default; `mean(skipna=False)` returns NaN if anything is missing.
- `len(df)` counts all rows; `count()` counts rows with data.
**Worked example:** Five employees, two with no salary recorded (40% missing).
**Excel / Python:**
```python
import pandas as pd
import numpy as np

# Salary is missing for Ravi and Divya
employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "Karan", "Divya"],
    "salary": [40000, np.nan, 50000, 60000, np.nan]})

# Number of missing values per column
print(employees.isna().sum())

# Percentage missing per column
print(employees.isna().mean() * 100)

# Effect on the statistics
print("mean ", employees["salary"].mean())
print("sum  ", employees["salary"].sum())
print("count", employees["salary"].count())
print("rows ", len(employees))

# Mean when we refuse to skip missing values
print("mean skipna=False", employees["salary"].mean(skipna=False))
```
```
name      0
salary    2
dtype: int64
name       0.0
salary    40.0
dtype: float64
mean  50000.0
sum   150000.0
count 3
rows  5
mean skipna=False nan
```
The mean 50,000 is based on only 3 people, not 5. Always report how many rows were missing.
**Likely follow-ups:** 1) *isna vs isnull?* Same thing. 2) *How does Excel treat blanks?* AVERAGE ignores them too.
**Common mistakes:** Treating missing as zero; not checking count() against the row count.

### Q12 ⭐⭐ 🟢 How do you fill missing values with the mean or median in pandas, and when would you choose the median?
**Asked at:** commonly asked (no company-specific report found); a standard imputation question (standard practice, no named source).
**What the interviewer is checking:** Can you fill gaps sensibly and explain why median resists outliers?
**Say this in the interview:** "I use `fillna(df['salary'].median())`. I choose the median when the column is skewed or has outliers, because the mean gets pulled by extreme values and would fill gaps with an unrealistic number."
**Explain simply:**
- Filling gaps with a typical value is called imputation.
- Mean works for roughly symmetric data; median for skewed data like salary.
- Filling with one value shrinks the natural spread of the data, so note it in your report. Sometimes dropping the rows or flagging them is better.
- `fillna` returns a new Series; assign it back to keep the result.
**Worked example:** Salaries 30000, 35000, 40000, missing, 45000, 300000 (one extreme value). The mean is 90,000, the median is 40,000.
**Excel / Python:**
```python
import pandas as pd
import numpy as np

# One missing salary and one very large salary
salaries = pd.Series([30000, 35000, 40000, np.nan, 45000, 300000])

# Mean and median ignoring the missing value
print("mean  ", salaries.mean())
print("median", salaries.median())

# Fill the gap with the mean (pulled up by the 300000)
print(salaries.fillna(salaries.mean()).tolist())

# Fill the gap with the median (realistic)
print(salaries.fillna(salaries.median()).tolist())
```
```
mean   90000.0
median 40000.0
[30000.0, 35000.0, 40000.0, 90000.0, 45000.0, 300000.0]
[30000.0, 35000.0, 40000.0, 40000.0, 45000.0, 300000.0]
```
Mean-filling invents a 90,000 salary that nobody near that group earns; median-filling gives 40,000, which looks like a normal employee.
**Likely follow-ups:** 1) *Fill by group?* `groupby("department")["salary"].transform("median")`. 2) *When drop instead?* When few rows are missing and they look random.
**Common mistakes:** Not assigning the result back; imputing before splitting data in modelling.

### Q13 ⭐⭐ 🟢 How do you build a pivot table in Excel to show average, count and maximum of salary by department?
**Asked at:** commonly asked (no company-specific report found); pivot tables are a staple of Excel interviews (standard practice, no named source).
**What the interviewer is checking:** Can you summarise a table interactively, including several measures of one field?
**Say this in the interview:** "I click inside the data, Insert, PivotTable, put Department in Rows and drag Salary into Values three times, changing each to Average, Count and Max through Value Field Settings."
**Explain simply:**
- Step 1: Click any cell in the data (a clean table with headers, no blank rows). Ideally convert it to a Table with Ctrl+T.
- Step 2: Insert > PivotTable > OK.
- Step 3: Drag **Department** to Rows; drag **Salary** to Values.
- Step 4: Salary defaults to Sum. Click it > Value Field Settings > choose Average. Drag Salary into Values twice more and set Count and Max. Rename the headings if you like.
- Refresh (right-click > Refresh) after the data changes; a pivot does not update on its own.
**Worked example:** Data in A1:B8 (Department, Salary): Sales 40000, Sales 50000, HR 35000, HR 45000, IT 60000, IT 70000, IT 80000. Expected pivot (checked with the pandas equivalent below; not run in Excel here):

| Department | Average | Count | Max |
|---|---|---|---|
| HR | 40000 | 2 | 45000 |
| IT | 70000 | 3 | 80000 |
| Sales | 45000 | 2 | 50000 |

**Excel / Python:**
```python
import pandas as pd

# Same seven rows as the sheet
staff = pd.DataFrame({
    "department": ["Sales", "Sales", "HR", "HR", "IT", "IT", "IT"],
    "salary": [40000, 50000, 35000, 45000, 60000, 70000, 80000]})

# pandas version of the pivot table
pivot = staff.pivot_table(index="department", values="salary",
                          aggfunc=["mean", "count", "max"])
print(pivot)
```
```
               mean  count    max
             salary salary salary
department                       
HR          40000.0      2  45000
IT          70000.0      3  80000
Sales       45000.0      2  50000
```
Same result as the Excel pivot.
**Likely follow-ups:** 1) *Pivot does not update?* Refresh it. 2) *Percent of total?* Show Values As > % of Column Total.
**Common mistakes:** Blank rows or merged headers in the source; forgetting that numbers stored as text get counted, not summed.

### Q14 ⭐⭐ 🟢 How do you use value_counts() in pandas to see the percentage share of each category, such as attrition Yes/No?
**Asked at:** commonly asked (no company-specific report found); a staple first-look command (standard practice, no named source).
**What the interviewer is checking:** Can you quickly see how a category is split, such as the attrition rate?
**Say this in the interview:** "`value_counts()` gives counts per category; adding `normalize=True` turns them into proportions, and multiplying by 100 gives percentages. For attrition it gives the attrition rate directly."
**Explain simply:**
- Counts tell you how many; proportions tell you what share.
- `normalize=True` returns fractions that add up to 1.
- Missing values are excluded unless you pass `dropna=False`.
- Results are sorted from largest to smallest by default.
**Worked example:** 100 employees: 84 stayed, 16 left, so attrition is 16%.
**Excel / Python:**
```python
import pandas as pd

# 100 employees: 84 stayed (No) and 16 left (Yes)
attrition = pd.Series(["No"] * 84 + ["Yes"] * 16)

# Counts of each category
print(attrition.value_counts())

# Share of each category as a fraction
print(attrition.value_counts(normalize=True))

# Share as a percentage, rounded to one decimal
print((attrition.value_counts(normalize=True) * 100).round(1))
```
```
No     84
Yes    16
Name: count, dtype: int64
No     0.84
Yes    0.16
Name: proportion, dtype: float64
No     84.0
Yes    16.0
Name: proportion, dtype: float64
```
Attrition is 16%: 16 of 100 people left.
**Likely follow-ups:** 1) *Include missing values?* `dropna=False`. 2) *Excel equivalent?* `=COUNTIF(range,"Yes")/COUNTA(range)`.
**Common mistakes:** Forgetting the percentages are relative to non-missing rows only.

### Q15 ⭐⭐ 🟢 How do you calculate a moving average in Excel and in pandas?
**Asked at:** commonly asked (no company-specific report found); standard trend-smoothing question (standard practice, no named source).
**What the interviewer is checking:** Can you smooth noisy monthly data to see a trend?
**Say this in the interview:** "A moving average averages the last few periods and slides forward each month. In Excel I write `=AVERAGE(B2:B4)` and copy it down; in pandas I use `rolling(window=3).mean()`."
**Explain simply:**
- Month-to-month numbers (resignations, hires) jump around; a 3-month average smooths this out.
- The first window-1 rows have no result because there are not enough earlier values yet.
- Excel: the formula in row 4 averages rows 2 to 4; copying down slides the range. Alternatively, Data Analysis ToolPak > Moving Average.
- Longer window means smoother but slower to react.
**Worked example:** Monthly resignations Jan to Jun: 4, 6, 5, 9, 7, 8 in B2:B7. In C4 type `=AVERAGE(B2:B4)` and copy down. Result: Mar 5.00, Apr 6.67, May 7.00, Jun 8.00 (pandas output below; not run in Excel here).
**Excel / Python:**
```python
import pandas as pd

# Resignations per month
monthly = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "resignations": [4, 6, 5, 9, 7, 8]})

# Average of the current and previous two months
monthly["moving_avg_3"] = monthly["resignations"].rolling(window=3).mean()

print(monthly)
```
```
  month  resignations  moving_avg_3
0   Jan             4           NaN
1   Feb             6           NaN
2   Mar             5      5.000000
3   Apr             9      6.666667
4   May             7      7.000000
5   Jun             8      8.000000
```
The raw numbers jump (5, 9, 7), but the smoothed line rises steadily from 5 to 8, showing resignations trending up.
**Likely follow-ups:** 1) *Why NaN at the start?* Not enough history. 2) *Fill the start?* `min_periods=1`.
**Common mistakes:** Using the wrong window; forgetting to sort by date first.

### Q16 ⭐⭐ 🟢 How do you rank values in Excel using RANK.EQ and PERCENTRANK.INC, and what happens with ties?
**Asked at:** commonly asked (no company-specific report found); a standard Excel ranking question (standard practice, no named source).
**What the interviewer is checking:** Do you know how ties are treated and the difference between a rank and a percentile rank?
**Say this in the interview:** "RANK.EQ gives each value its position; tied values get the same rank and the next rank is skipped. PERCENTRANK.INC gives the share of values below it, from 0 to 1."
**Explain simply:**
- `=RANK.EQ(value, range, 0)`: 0 or omitted means largest = rank 1; 1 means smallest = rank 1 (Excel 2010+).
- Ties get the same rank, and the next rank is skipped (1, 2, 3, 3, 5).
- `=PERCENTRANK.INC(range, value)` = (number of values below) / (n - 1). Default shows 3 decimals.
- Use it to say "this employee is in the top 25%".
**Worked example:** Five sales scores in B2:B6: A 50, B 60, C 60, D 70, E 80.
- `=RANK.EQ(B3,$B$2:$B$6,0)` for 60 returns 3, same for the other 60. 70 is rank 2, 80 is rank 1, 50 is rank 5 (rank 4 is skipped).
- `=PERCENTRANK.INC($B$2:$B$6,B4)` for 70 returns 0.75 (3 of 4 gaps below it).
**Excel / Python:**
```python
import pandas as pd

# Five scores, two of them tied at 60
scores = pd.Series([50, 60, 60, 70, 80], index=["A", "B", "C", "D", "E"])

# Rank with largest = 1; ties share the lower rank number (like RANK.EQ)
ranks = scores.rank(ascending=False, method="min")
print(ranks)

# Percent rank: how many values are below, divided by (n - 1)
for score in scores:
    values_below = (scores < score).sum()
    percent_rank = values_below / (len(scores) - 1)
    print(score, percent_rank)
```
```
A    5.0
B    3.0
C    3.0
D    2.0
E    1.0
dtype: float64
50 0.0
60 0.25
60 0.25
70 0.75
80 1.0
```
Tied 60s share rank 3, and nobody gets rank 4. Python results used as the check; Excel formulas not run here.
**Likely follow-ups:** 1) *Average rank for ties?* RANK.AVG. 2) *Difference from percentile?* Percent rank is for a value in your data.
**Common mistakes:** Expecting ranks 3 and 4 for ties; forgetting to lock the range with $.

### Q17 ⭐⭐ 🟡 How do you flag outliers using the IQR rule in Excel?
**Asked at:** commonly asked; "basic statistics" was reported for an Accenture Bangalore interview (research/interview_processes.md), but no report of this exact question was found.
**What the interviewer is checking:** Can you set objective outlier limits and flag points with a formula?
**Say this in the interview:** "I calculate Q1 and Q3 with QUARTILE.INC, then IQR = Q3 minus Q1. Anything below Q1 minus 1.5 times IQR, or above Q3 plus 1.5 times IQR, is flagged as an outlier. An IF formula with OR flags each row."
**Explain simply:**
- **IQR** (interquartile range) = Q3 minus Q1, the spread of the middle half of the data.
- The 1.5 multiplier is a convention (Tukey's rule), not a law. An outlier is a point to investigate, not automatically delete.
- Lock the limit cells with `$` so the formula copies down.
**Worked example:** Ten salaries (in thousands) in A2:A11: 30, 32, 35, 38, 40, 42, 45, 48, 50, 150. Put these in D2:D5:
- D2 `=QUARTILE.INC($A$2:$A$11,1)` returns 35.75
- D3 `=QUARTILE.INC($A$2:$A$11,3)` returns 47.25
- D4 `=D3-D2` returns 11.5 (IQR)
- Lower limit `=D2-1.5*D4` returns 18.5; upper limit `=D3+1.5*D4` returns 64.5
- In B2 (copy down): `=IF(OR(A2<$E$2,A2>$E$3),"Outlier","OK")`, where E2 holds the lower and E3 the upper limit. Only 150 is flagged.

Values checked in Python; formulas not run in Excel here.
**Excel / Python:**
```python
import pandas as pd

# Ten salaries in thousands; the last one is unusually high
salaries = pd.Series([30, 32, 35, 38, 40, 42, 45, 48, 50, 150])

# Quartiles and IQR
quartile_1 = salaries.quantile(0.25)
quartile_3 = salaries.quantile(0.75)
iqr = quartile_3 - quartile_1

# Fences beyond which a value is an outlier
lower_limit = quartile_1 - 1.5 * iqr
upper_limit = quartile_3 + 1.5 * iqr
print(quartile_1, quartile_3, iqr, lower_limit, upper_limit)

# Values outside the fences
outliers = salaries[(salaries < lower_limit) | (salaries > upper_limit)]
print(outliers.tolist())
```
```
35.75 47.25 11.5 18.5 64.5
[150]
```
Only the 150 salary falls outside 18.5 to 64.5, so it is the single outlier.
**Likely follow-ups:** 1) *Why 1.5?* Convention that works for typical data; 3 gives "extreme" outliers. 2) *Do you delete outliers?* Only after checking whether they are errors or real.
**Common mistakes:** Deleting outliers automatically; using the whole-column range without locking with $.

### Q18 ⭐⭐ 🟡 How do you detect outliers in Python using the IQR method with quantile()?
**Asked at:** commonly asked (no company-specific report found); the Part 11 sources note only that Accenture Bangalore reported "basic statistics" questions in general.
**What the interviewer is checking:** Can you turn the IQR rule into clean pandas code and explain why it is safer than the mean-based rule?
**Say this in the interview:** "I take Q1 and Q3 with quantile(), compute IQR as Q3 minus Q1, and flag anything below Q1 minus 1.5 times IQR or above Q3 plus 1.5 times IQR. Then I look at those rows before deciding to keep, cap or remove them."
**Explain simply:**
- **Quartiles** cut sorted data into four equal parts; Q1 is the 25th percentile and Q3 the 75th.
- **IQR (interquartile range)** is the width of the middle 50% of values, so one huge salary cannot distort it.
- Values beyond the "fences" (1.5 x IQR past the quartiles) are only flagged as unusual; an outlier is not automatically an error.
**Formula in plain words:** lower fence = Q1 minus 1.5 times (Q3 minus Q1); upper fence = Q3 plus 1.5 times (Q3 minus Q1).
**Worked example:** 12 monthly salaries (in thousands): Q1 = 39.5, Q3 = 49, IQR = 9.5, fences 25.25 and 63.25. Only 150 lies outside, so it is the one flagged value.
**Excel / Python:**
```python
import pandas as pd

# Monthly salaries in thousands of rupees for 12 employees (one very high value)
monthly_salaries = pd.Series([32, 35, 38, 40, 41, 43, 45, 47, 48, 52, 55, 150])

# Step 1: first quartile (25th percentile) and third quartile (75th percentile)
q1 = monthly_salaries.quantile(0.25)
q3 = monthly_salaries.quantile(0.75)

# Step 2: IQR is the spread of the middle half of the data
iqr = q3 - q1

# Step 3: fences are 1.5 IQRs below Q1 and above Q3
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr
print("Q1:", q1, "Q3:", q3, "IQR:", iqr)
print("Lower fence:", lower_fence, "Upper fence:", upper_fence)

# Step 4: keep only values outside the fences
is_outlier = (monthly_salaries < lower_fence) | (monthly_salaries > upper_fence)
outliers = monthly_salaries[is_outlier]
print("Outliers:", outliers.tolist())
```
Output:
```
Q1: 39.5 Q3: 49.0 IQR: 9.5
Lower fence: 25.25 Upper fence: 63.25
Outliers: [150]
```
Only the 150 salary falls outside the fences. By default quantile() interpolates the same way as Excel's QUARTILE.INC.
**Likely follow-ups:** 1) *Why 1.5?* A convention (Tukey's rule); use 3 for "extreme" outliers. 2) *Would you delete it?* Not blindly: check if it is a data-entry error or a real senior package.
**Common mistakes:** Deleting outliers automatically; using the mean and standard deviation on heavily skewed salary data; forgetting that quartile methods differ slightly between tools.

### Q19 ⭐⭐ 🟡 How do you calculate a z-score in Excel (STANDARDIZE) and in Python, and what does a z-score of 2.5 tell you?
**Asked at:** commonly asked (no company-specific report found); generic prep lists.
**What the interviewer is checking:** Do you understand a z-score as "how many standard deviations from the average", not just the formula?
**Say this in the interview:** "A z-score is the value minus the mean, divided by the standard deviation. A z of 2.5 means the value sits 2.5 standard deviations above average, which is unusual: roughly 0.6% of values in a bell-shaped distribution are higher."
**Explain simply:**
- **Standard deviation** is the typical distance of values from the average.
- A z-score puts different measures on one scale, so you can compare salary with tenure.
- Rough guide: beyond plus or minus 2 is unusual, beyond 3 is rare (for roughly bell-shaped data).
**Formula in plain words:** z = (the value minus the mean) divided by the standard deviation.
**Worked example:** Salary mean 50,000, standard deviation 8,000. An employee on 70,000 has z = (70,000 - 50,000) / 8,000 = 2.5. In a normal distribution the chance of being above that is about 0.62%.
**Excel / Python:**
Excel (2010+; not run in Excel here, matched to Python). Put the value in A2 (70000), mean in B2 (50000), standard deviation in C2 (8000): `=STANDARDIZE(A2,B2,C2)` returns 2.5. For a whole column in A2:A21 use `=(A2-AVERAGE($A$2:$A$21))/STDEV.S($A$2:$A$21)` and copy down.
```python
import pandas as pd

# Engagement scores for 20 employees
engagement_scores = pd.Series([62, 65, 70, 72, 75, 78, 80, 82, 85, 90,
                               95, 60, 68, 74, 77, 81, 83, 88, 92, 98])

# Step 1: mean and sample standard deviation (pandas .std() uses n-1)
average_score = engagement_scores.mean()
spread_score = engagement_scores.std()

# Step 2: z-score = (value - mean) / standard deviation, for every employee
z_scores = (engagement_scores - average_score) / spread_score

# Step 3: look at the highest score (98)
print("Mean:", round(average_score, 2), "SD:", round(spread_score, 2))
print("z-score of the 98 score:", round(z_scores.iloc[19], 2))

# Step 4: the same idea with a plain salary example (mean 50,000, SD 8,000, salary 70,000)
salary_z = (70000 - 50000) / 8000
print("Salary z-score:", salary_z)
```
Output:
```
Mean: 78.75 SD: 10.75
z-score of the 98 score: 1.79
Salary z-score: 2.5
```
The top score is 1.79 standard deviations above the average, so it is high but not unusual; the salary at 2.5 would be.
**Likely follow-ups:** 1) *Does it need a normal distribution?* The "0.6%" reading does; the z-score itself does not. 2) *Sample or population SD?* STDEV.S for a sample; pandas .std() already uses the sample version.
**Common mistakes:** Mixing STDEV.S and STDEV.P between steps; reading z-scores as probabilities directly; trusting them on skewed data.

### Q20 ⭐⭐ 🟡 How do you enable and use the Data Analysis ToolPak in Excel to get descriptive statistics?
**Asked at:** commonly asked (no company-specific report found); ToolPak tutorials (GoSkills, Noble Desktop) cover it, but no interview report was seen.
**What the interviewer is checking:** Do you know the add-in is off by default and can you read its output?
**Say this in the interview:** "I enable it under File, Options, Add-ins, Manage Excel Add-ins, Go, tick Analysis ToolPak. Then Data, Data Analysis, Descriptive Statistics, select the column, tick Labels, Summary statistics and Output Range."
**Explain simply:**
- **ToolPak** is a free Microsoft add-in that adds a Data Analysis button to the Data tab (Windows and recent Mac Excel).
- Descriptive Statistics gives mean, standard error, median, mode, standard deviation, variance, kurtosis, skewness, range, min, max, sum, count and optionally a confidence level.
- The output is static numbers, not formulas; it does not update when data changes.
**Worked example:** For 10 salaries (in thousands) 32, 35, 38, 40, 41, 43, 45, 47, 48, 52 in A2:A11, ToolPak shows Mean 42.1, Median 42, Standard Deviation 6.1545, Range 20, Count 10. Mode shows #N/A because no value repeats. Confidence Level (95%) gives 4.4027.
**Excel / Python:**
Excel steps are above (not run in Excel here). The same numbers in Python:
```python
import pandas as pd
import numpy as np

# Same 10 salaries (thousands) used in the Excel example
salaries = pd.Series([32, 35, 38, 40, 41, 43, 45, 47, 48, 52])

# Rebuild the main ToolPak lines to show they match
print("Mean:", salaries.mean())
print("Standard Error:", round(salaries.std() / np.sqrt(len(salaries)), 4))
print("Median:", salaries.median())
print("Standard Deviation:", round(salaries.std(), 4))
print("Sample Variance:", round(salaries.var(), 4))
print("Kurtosis:", round(salaries.kurt(), 4))
print("Skewness:", round(salaries.skew(), 4))
print("Range:", salaries.max() - salaries.min())
print("Sum:", salaries.sum(), "Count:", len(salaries))
```
Output:
```
Mean: 42.1
Standard Error: 1.9462
Median: 42.0
Standard Deviation: 6.1545
Sample Variance: 37.8778
Kurtosis: -0.5794
Skewness: -0.0889
Range: 20
Sum: 421 Count: 10
```
Each line matches what the ToolPak reports; pandas describe() gives a similar but shorter summary.
**Likely follow-ups:** 1) *ToolPak missing?* It is not on Excel for the web; use formulas instead. 2) *Why formulas over ToolPak?* They refresh automatically.
**Common mistakes:** Forgetting to tick "Labels in first row"; expecting live-updating results; confusing Standard Error with Standard Deviation.

### Q21 ⭐⭐ 🟡 How do you run a simple linear regression in Excel using SLOPE, INTERCEPT, RSQ or LINEST, and how do you read R-squared?
**Asked at:** commonly asked (no company-specific report found); regression appears in generic analyst prep lists.
**What the interviewer is checking:** Can you fit a line, state it in words and read R-squared honestly (without claiming causation)?
**Say this in the interview:** "SLOPE gives how much salary rises per extra year of experience, INTERCEPT the starting level, RSQ the share of salary variation explained by experience. LINEST returns slope and intercept together, and with stats=TRUE more detail."
**Explain simply:**
- **Simple linear regression** draws the best straight line through points: salary = intercept + slope x experience.
- **Slope** is the change in Y for one more unit of X.
- **R-squared** (0 to 1) is the share of the variation in Y that the line explains; 0.99 means very tight fit.
- A strong fit shows association, not that experience causes the pay.
**Worked example:** Experience 1 to 10 years in A2:A11, salary (thousands) 28, 31, 36, 38, 45, 47, 50, 56, 57, 64 in B2:B11. Slope = 3.903 (about 3,900 rupees more per year), intercept = 23.733, R-squared = 0.9899. At 12 years the line predicts 70.57.
**Excel / Python:**
Excel (not run in Excel here, values matched to Python; LINEST works in all versions, in 365 it spills): 
`=SLOPE(B2:B11,A2:A11)` returns 3.903; `=INTERCEPT(B2:B11,A2:A11)` returns 23.7333; `=RSQ(B2:B11,A2:A11)` returns 0.9899; `=INDEX(LINEST(B2:B11,A2:A11,TRUE,TRUE),3,1)` returns R-squared too. Note: Y range first, X range second.
```python
import numpy as np
from scipy import stats

# Years of experience and salary (thousands) for 10 employees
experience_years = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
salary_thousands = np.array([28, 31, 36, 38, 45, 47, 50, 56, 57, 64])

# Fit the straight line, same numbers as SLOPE, INTERCEPT and RSQ
fit = stats.linregress(experience_years, salary_thousands)
print("Slope:", round(fit.slope, 4))
print("Intercept:", round(fit.intercept, 4))
print("R-squared:", round(fit.rvalue ** 2, 4))

# FORECAST for 12 years of experience
print("Predicted salary at 12 years:", round(fit.intercept + fit.slope * 12, 2))
```
Output:
```
Slope: 3.903
Intercept: 23.7333
R-squared: 0.9899
Predicted salary at 12 years: 70.57
```
About 99% of the salary differences in this small sample line up with experience.
**Likely follow-ups:** 1) *Does high R-squared prove experience drives pay?* No; role, grade or city may be behind both. 2) *Is 12 years safe to predict?* Slightly beyond the data (max 10); treat with care.
**Common mistakes:** Swapping the X and Y ranges; reading R-squared as causation; trusting a line from 10 points for far-away predictions.

### Q22 ⭐⭐ 🟡 How do you run a simple linear regression in Python and read the coefficient and R-squared?
**Asked at:** commonly asked (no company-specific report found); generic prep lists.
**What the interviewer is checking:** Can you run OLS with statsmodels, remember the intercept and read the key outputs?
**Say this in the interview:** "I use statsmodels OLS with add_constant so there is an intercept. The coefficient on experience is the salary change per extra year, R-squared is the share explained, and I check the p-value for the slope."
**Explain simply:**
- **OLS (ordinary least squares)** picks the line with the smallest total squared gaps to the points.
- **Coefficient** = slope; the constant = intercept.
- **P-value** for the slope: a small value says the slope is unlikely to be zero by chance.
- **Adjusted R-squared** penalises extra predictors; it matters once you have more than one X.
**Worked example:** Same data as Q21: slope 3.903, intercept 23.733, R-squared 0.9899, adjusted 0.9886, slope p-value about 2.9e-09. Each extra year of experience is linked to about 3,900 rupees more salary.
**Excel / Python:**
```python
import numpy as np
import statsmodels.api as sm

experience_years = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
salary_thousands = np.array([28, 31, 36, 38, 45, 47, 50, 56, 57, 64])

# Step 1: statsmodels needs an explicit intercept column
x_with_intercept = sm.add_constant(experience_years)

# Step 2: fit ordinary least squares and read the key numbers
model = sm.OLS(salary_thousands, x_with_intercept).fit()
print("Intercept and slope:", model.params.round(4))
print("R-squared:", round(model.rsquared, 4))
print("Adjusted R-squared:", round(model.rsquared_adj, 4))
print("Slope p-value:", model.pvalues[1])
```
Output:
```
Intercept and slope: [23.7333  3.903 ]
R-squared: 0.9899
Adjusted R-squared: 0.9886
Slope p-value: 2.858114343298436e-09
```
The first number is the intercept, the second the slope. Printing model.summary() shows the full table.
**Likely follow-ups:** 1) *Why add_constant?* Without it the line is forced through zero. 2) *scipy alternative?* stats.linregress gives the same slope and intercept for one predictor.
**Common mistakes:** Forgetting the constant; quoting R-squared without checking a scatter plot; ignoring p-values and sample size.

### Q23 ⭐⭐ 🟡 How do you run a two-sample t-test in Excel using T.TEST, and what do the type and tails arguments mean?
**Asked at:** commonly asked (no company-specific report found); t-test types are covered in ToolPak tutorials.
**What the interviewer is checking:** Do you know the three types and one- vs two-tailed, and can you state the conclusion?
**Say this in the interview:** "T.TEST(array1, array2, tails, type) returns the p-value. Tails is 1 or 2; type is 1 for paired, 2 for two samples equal variance, 3 for unequal variance. I default to type 3 and 2 tails unless I have a directional hypothesis."
**Explain simply:**
- **t-test** asks whether two group averages differ by more than chance would explain.
- **p-value**: the probability of a difference this large if the groups really had the same average; below 0.05 is the usual cut-off.
- **Tails = 2** tests "different"; **tails = 1** tests "higher" only, and must be decided before seeing data.
- **Type 1 paired** is for the same people measured twice (before and after training).
**Worked example:** Engagement scores: Sales (8 people) average 51.25, Support (9 people) average 45.67. Type 3, two tails gives p = 0.0697 (not below 0.05, so no clear difference). Type 2 gives 0.0660. One-tailed type 3 gives 0.0349, which shows why picking tails after seeing data is cheating.
**Excel / Python:**
Excel (2010+; not run in Excel here, matched to Python). Sales scores in A2:A9, Support scores in B2:B10: `=T.TEST(A2:A9,B2:B10,2,3)` returns 0.0697; `=T.TEST(A2:A9,B2:B10,2,2)` returns 0.0660; `=T.TEST(A2:A9,B2:B10,1,3)` returns 0.0349. See Q24 for the Python run.
**Likely follow-ups:** 1) *Groups of different size?* Fine for types 2 and 3; type 1 needs equal pairs. 2) *Significant means important?* No, check the size of the difference.
**Common mistakes:** Using paired type on independent groups; picking one tail to get p under 0.05; saying "p = 0.07 proves no difference".

### Q24 ⭐⭐ 🟡 How do you run a two-sample t-test in Python using scipy, and why do you often set equal_var=False?
**Asked at:** commonly asked (no company-specific report found); generic prep lists.
**What the interviewer is checking:** Do you know Welch's test and why equal spread should not be assumed?
**Say this in the interview:** "I use scipy.stats.ttest_ind(group_a, group_b, equal_var=False). That is Welch's t-test; it does not assume both groups have the same spread, so it is safer and loses almost nothing when the spreads happen to be equal."
**Explain simply:**
- **Welch's t-test** adjusts the degrees of freedom when the groups' variances differ.
- The default in scipy is equal_var=True, which is the classic pooled test and can mislead with unequal spread and unequal group sizes.
- The result has a t statistic and a p-value; add alternative="greater" or "less" for one-sided tests.
**Worked example:** Same Sales and Support scores as Q23. Spreads differ (variance 39.07 vs 28.75). Welch gives t = 1.9644, p = 0.0697; pooled gives t = 1.9833, p = 0.0660; one-sided Welch p = 0.0349. These match Excel's types 3 and 2.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Engagement scores: Sales team (8 people) and Support team (9 people)
sales_scores = np.array([42, 45, 48, 50, 52, 55, 58, 60])
support_scores = np.array([38, 40, 41, 44, 46, 47, 50, 52, 53])

# Step 1: Welch test (does not assume equal spread)
welch = stats.ttest_ind(sales_scores, support_scores, equal_var=False)
print("Welch   t:", round(welch.statistic, 4), "p:", round(welch.pvalue, 4))

# Step 2: classic test assuming equal spread
pooled = stats.ttest_ind(sales_scores, support_scores, equal_var=True)
print("Pooled  t:", round(pooled.statistic, 4), "p:", round(pooled.pvalue, 4))

# Step 3: one-sided question "is Sales higher?"
one_sided = stats.ttest_ind(sales_scores, support_scores, equal_var=False, alternative="greater")
print("One-sided Welch p:", round(one_sided.pvalue, 4))
```
Output:
```
Welch   t: 1.9644 p: 0.0697
Pooled  t: 1.9833 p: 0.066
One-sided Welch p: 0.0349
```
With p about 0.07 we cannot claim a real difference at the 5% level, though the sample is small.
**Likely follow-ups:** 1) *Same people before and after?* Use stats.ttest_rel. 2) *Not normal and tiny groups?* Consider Mann-Whitney.
**Common mistakes:** Leaving the default equal_var=True; running a one-sided test after looking at the data; ignoring sample size.

### Q25 ⭐⭐ 🟡 How do you run a chi-square test of independence in Excel (CHISQ.TEST) and in Python (chi2_contingency)?
**Asked at:** commonly asked (no company-specific report found); generic prep lists.
**What the interviewer is checking:** Can you set up a counts table, understand expected counts and interpret the p-value?
**Say this in the interview:** "I build a table of counts, for example department by left or stayed. The test compares actual counts with the counts expected if department and attrition were unrelated. A small p-value says they are probably related."
**Explain simply:**
- **Chi-square test of independence** checks whether two categories (department, attrition) are linked.
- **Expected counts** = row total x column total / grand total.
- It needs raw counts (not percentages) and expected counts of roughly 5 or more per cell.
- It tells you that a link exists, not how strong or why.
**Formula in plain words:** for each cell take (actual minus expected) squared, divide by expected, and add them all up.
**Worked example:** 100 employees per department. Left: Sales 30, Support 20, Tech 50. Overall 33.3% left, so expected 33.3 per department. Chi-square = 21.0, 2 degrees of freedom, p = 0.0000275. Attrition clearly differs by department.
**Excel / Python:**
Excel (2010+; not run in Excel here, matched to Python). Actual counts in B2:C4 (left, stayed). Excel needs an expected table too: in E2 enter `=SUM($B2:$C2)*SUM(B$2:B$4)/SUM($B$2:$C$4)`, copy across to F2 and down to row 4. Then `=CHISQ.TEST(B2:C4,E2:F4)` returns 0.0000275 (the p-value, not the chi-square).
```python
import numpy as np
from scipy.stats import chi2_contingency

# Rows: Sales, Support, Tech. Columns: Left, Stayed (100 people per department)
observed_counts = np.array([[30, 70],
                            [20, 80],
                            [50, 50]])

chi_square_value, p_value, degrees_of_freedom, expected_counts = chi2_contingency(observed_counts)
print("Chi-square:", round(chi_square_value, 2))
print("p-value:", p_value)
print("Degrees of freedom:", degrees_of_freedom)
print("Expected counts:")
print(expected_counts.round(2))
```
Output:
```
Chi-square: 21.0
p-value: 2.7536449349747192e-05
Degrees of freedom: 2
Expected counts:
[[33.33 66.67]
 [33.33 66.67]
 [33.33 66.67]]
```
The p-value is far below 0.05, so department and attrition are not independent. Python builds the expected table for you.
**Likely follow-ups:** 1) *Which department differs?* Compare each department's rate or look at cell-by-cell contributions. 2) *Very small counts?* Use Fisher's exact test.
**Common mistakes:** Feeding percentages instead of counts; forgetting Excel needs the expected range; reading a small p-value as "strong effect".

### Q26 ⭐⭐ 🟡 How do you calculate a 95% confidence interval for a mean in Excel using CONFIDENCE.T, and in Python?
**Asked at:** commonly asked (no company-specific report found); generic prep lists.
**What the interviewer is checking:** Do you know the interval is mean plus or minus a margin, and the right way to describe it?
**Say this in the interview:** "CONFIDENCE.T(0.05, standard deviation, n) gives the margin of error for a 95% interval using the t-distribution. I add and subtract it from the sample mean. It says the true average is plausibly in that range."
**Explain simply:**
- **Confidence interval** is a range built so that, repeated many times, about 95% of such ranges would contain the true average.
- **Margin of error** = t critical value x standard error; **standard error** = standard deviation divided by the square root of n.
- Use the t version for small samples; CONFIDENCE.NORM uses the normal and gives a narrower interval (0.1554 here).
**Formula in plain words:** mean plus or minus (t value x standard deviation / square root of sample size).
**Worked example:** 12 satisfaction scores: mean 3.95, standard deviation 0.2747, standard error 0.0793, t critical 2.201. Margin 0.1745, so the 95% interval is 3.775 to 4.125.
**Excel / Python:**
Excel (2010+; not run in Excel here, matched to Python). Scores in A2:A13: margin `=CONFIDENCE.T(0.05,STDEV.S(A2:A13),COUNT(A2:A13))` returns 0.1745; lower limit `=AVERAGE(A2:A13)-CONFIDENCE.T(0.05,STDEV.S(A2:A13),COUNT(A2:A13))` returns 3.775.
```python
import numpy as np
from scipy import stats

# Satisfaction scores (1 to 5) from 12 employees
satisfaction = np.array([3.8, 4.1, 3.5, 4.4, 3.9, 4.0, 3.6, 4.2, 3.7, 4.3, 4.0, 3.9])

# Step 1: basic numbers
sample_size = len(satisfaction)
sample_mean = satisfaction.mean()
sample_sd = satisfaction.std(ddof=1)

# Step 2: standard error and t critical value for 95% with n-1 degrees of freedom
standard_error = sample_sd / np.sqrt(sample_size)
t_critical = stats.t.ppf(0.975, sample_size - 1)

# Step 3: margin of error (this equals Excel's CONFIDENCE.T) and the interval
margin_of_error = t_critical * standard_error
print("Mean:", round(sample_mean, 3), "SD:", round(sample_sd, 4))
print("t critical:", round(t_critical, 4), "Margin of error:", round(margin_of_error, 4))
print("95% CI:", round(sample_mean - margin_of_error, 3), "to", round(sample_mean + margin_of_error, 3))
```
Output:
```
Mean: 3.95 SD: 0.2747
t critical: 2.201 Margin of error: 0.1745
95% CI: 3.775 to 4.125
```
We estimate the true average satisfaction is between about 3.78 and 4.12.
**Likely follow-ups:** 1) *What does 95% mean?* The method captures the true mean 95% of the time; not a 95% chance for this one interval. 2) *How to narrow it?* Larger sample.
**Common mistakes:** Using STDEV.P; using CONFIDENCE (old) or the normal version for small samples; saying "95% of employees fall in this range".

### Q27 ⭐ 🟢 What is the difference between COVARIANCE.S and COVARIANCE.P in Excel, and how do you get a covariance matrix in pandas?
**Asked at:** commonly asked (no company-specific report found); gap-filled from standard practice.
**What the interviewer is checking:** Do you know S divides by n-1, P by n, and that pandas uses the sample version?
**Say this in the interview:** "Covariance shows whether two columns move together. COVARIANCE.S divides by n minus 1 and is for samples; COVARIANCE.P divides by n and is for a full population. pandas .cov() gives the sample version as a matrix."
**Explain simply:**
- **Covariance** is positive when both rise together, negative when one rises as the other falls.
- Its size depends on the units, so it is hard to compare; correlation is covariance rescaled to between -1 and 1.
**Formula in plain words:** average of (X minus its mean) times (Y minus its mean); divide by n-1 for a sample, n for a population.
**Worked example:** 6 employees: experience 1 to 6 years, salary 30, 34, 41, 43, 52, 56 (thousands). Sample covariance = 18.6; population = 15.5 (18.6 x 5/6). Positive: more experience goes with higher pay.
**Excel / Python:**
Excel (2010+; not run in Excel here, matched to Python). Experience A2:A7, salary B2:B7: `=COVARIANCE.S(A2:A7,B2:B7)` returns 18.6; `=COVARIANCE.P(A2:A7,B2:B7)` returns 15.5.
```python
import pandas as pd

employees = pd.DataFrame({
    "experience_years": [1, 2, 3, 4, 5, 6],
    "salary_thousands": [30, 34, 41, 43, 52, 56],
    "absent_days": [9, 8, 8, 5, 4, 2],
})

# Covariance matrix (pandas uses the sample version, n-1)
print(employees.cov())

# Population version for one pair, by hand: average of products of deviations (divide by n)
exp_dev = employees["experience_years"] - employees["experience_years"].mean()
sal_dev = employees["salary_thousands"] - employees["salary_thousands"].mean()
print("Population covariance:", (exp_dev * sal_dev).mean())
print("Sample covariance:", (exp_dev * sal_dev).sum() / (len(employees) - 1))
```
Output:
```
                  experience_years  salary_thousands  absent_days
experience_years               3.5         18.600000         -5.0
salary_thousands              18.6        100.666667        -26.2
absent_days                  -5.0        -26.200000          7.6
Population covariance: 15.5
Sample covariance: 18.6
```
The diagonal holds each column's variance; absence is negatively linked with experience and salary.
**Likely follow-ups:** 1) *Why prefer correlation?* Unit-free and easier to read. 2) *Which to use for 50 employees sampled from 5,000?* The sample version.
**Common mistakes:** Comparing covariances across different units; using the old COVAR function (population) by accident.

### Q28 ⭐ 🟢 How do you check the shape of a distribution in Excel and Python using SKEW, KURT, a histogram or skew()?
**Asked at:** commonly asked (no company-specific report found); gap-filled from standard practice.
**What the interviewer is checking:** Can you describe skew and kurtosis in words and say which way salaries skew?
**Say this in the interview:** "I look at a histogram first, then SKEW for direction and KURT for tails. Positive skew means a long right tail, typical of salary data, where the mean sits above the median."
**Explain simply:**
- **Skewness**: 0 is symmetric, positive means long right tail, negative long left tail.
- **Kurtosis** (Excel KURT and pandas .kurt() both give excess kurtosis): above 0 means heavier tails and more extreme values than a bell curve.
- A mean far above the median is a quick skew warning.
**Worked example:** 10 salaries (thousands) 30 to 45 plus one senior package of 95. Skew = 2.82, excess kurtosis = 8.41, mean 42.6 vs median 37. Strongly right-skewed, so report the median.
**Excel / Python:**
Excel (not run in Excel here, matched to Python; SKEW and KURT exist in all versions). Data in A2:A11: `=SKEW(A2:A11)` returns 2.82; `=KURT(A2:A11)` returns 8.41. For a histogram use Insert, Charts, Histogram (2016+).
```python
import pandas as pd

# Ten salaries (thousands); one senior package of 95 stretches the right side
salaries = pd.Series([30, 32, 33, 35, 36, 38, 40, 42, 45, 95])

print("Skew:", round(salaries.skew(), 3))
print("Excess kurtosis:", round(salaries.kurt(), 3))
print("Mean:", salaries.mean(), "Median:", salaries.median())

# Text histogram in bins of 10
bins = [30, 40, 50, 60, 70, 80, 90, 100]
counts = pd.cut(salaries, bins=bins, right=False).value_counts().sort_index()
print(counts)
```
Output:
```
Skew: 2.82
Excess kurtosis: 8.41
Mean: 42.6 Median: 37.0
[30, 40)     6
[40, 50)     3
[50, 60)     0
[60, 70)     0
[70, 80)     0
[80, 90)     0
[90, 100)    1
Name: count, dtype: int64
```
Most salaries cluster low with one far to the right, so the mean (42.6) is pulled above the median (37).
**Likely follow-ups:** 1) *What would you do about skew?* Use the median, or a log transform for modelling. 2) *What is a skew of 0.2?* Roughly symmetric.
**Common mistakes:** Reading kurtosis as "peakedness" only; computing skew on tiny samples and over-trusting it.

### Q29 ⭐ 🟢 How do you take a random sample of rows in Excel and in pandas, and why set random_state?
**Asked at:** commonly asked (no company-specific report found); gap-filled from standard practice.
**What the interviewer is checking:** Do you understand reproducibility: same seed, same sample?
**Say this in the interview:** "In pandas I use df.sample(n=...) or frac=..., and set random_state so anyone rerunning gets the same rows. In Excel I add a RAND() helper column and sort by it, then take the top rows."
**Explain simply:**
- **Random sample** gives every row an equal chance to be picked.
- **random_state** is a seed number for the random generator; fixed seed means identical sample on every run.
- Excel's RAND() recalculates on every change, so copy and paste as values to freeze the sample.
**Worked example:** 10 employees, sample 3 with random_state=42: rows 9, 2 and 6 each time. Without a seed, a colleague would get different rows and numbers would not reconcile.
**Excel / Python:**
Excel: put `=RAND()` in B2 next to employee IDs in A2:A11, copy down, sort by column B and take the first 3 rows. In Excel 365 (not run in Excel here): `=TAKE(SORTBY(A2:A11,RANDARRAY(10)),3)`.
```python
import pandas as pd

employees = pd.DataFrame({"emp_id": range(1, 11),
                          "dept": ["S", "S", "H", "H", "F", "F", "S", "H", "F", "S"]})

# Sample 3 rows, twice, with the same random_state
print(employees.sample(n=3, random_state=42))
print(employees.sample(n=3, random_state=42))

# Sample 30% of the rows
print(employees.sample(frac=0.3, random_state=7))
```
Output:
```
   emp_id dept
8       9    F
1       2    S
5       6    F
   emp_id dept
8       9    F
1       2    S
5       6    F
   emp_id dept
8       9    F
5       6    F
0       1    S
```
Both runs with seed 42 return the same three rows. The exact rows depend on the pandas/numpy version, but a fixed seed gives repeatable results within one setup.
**Likely follow-ups:** 1) *Sample by department?* df.groupby("dept").sample(n=1). 2) *Is a sample always representative?* Small ones can miss groups; use stratified sampling.
**Common mistakes:** Forgetting to freeze RAND(); no seed in a reported analysis; sampling the first N rows (not random).

### Q30 ⭐ 🟢 How do you build and read a correlation matrix in pandas, and why must you select numeric columns first?
**Asked at:** commonly asked; correlation and select_dtypes appear in pandas question lists (GoLinuxCloud and similar prep sites).
**What the interviewer is checking:** Can you produce the matrix, read the signs and avoid the text-column error?
**Say this in the interview:** "I select numeric columns with select_dtypes, then call .corr(). Each cell is between -1 and 1: close to 1 means they rise together, close to -1 means one rises as the other falls, near 0 means no straight-line link."
**Explain simply:**
- **Correlation** measures the strength and direction of a straight-line relationship.
- The diagonal is always 1 (a column against itself) and the matrix is mirrored.
- Text columns such as employee names cannot be correlated; in pandas 2.0 and later .corr() raises an error instead of silently skipping them.
- Correlation is not causation.
**Worked example:** 6 employees: experience and salary 0.99, experience and absence -0.97, salary and absence -0.95. More experience goes with higher pay and fewer absent days.
**Excel / Python:**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_name": ["A", "B", "C", "D", "E", "F"],
    "experience_years": [1, 2, 3, 4, 5, 6],
    "salary_thousands": [30, 34, 41, 43, 52, 56],
    "absent_days": [9, 8, 8, 5, 4, 2],
})

# Step 1: keep only number columns
numeric_columns = employees.select_dtypes(include="number")

# Step 2: correlation matrix
print(numeric_columns.corr().round(2))

# Step 3: what happens without selecting
try:
    employees.corr()
except ValueError as error:
    print("Error:", error)
```
Output:
```
                  experience_years  salary_thousands  absent_days
experience_years              1.00              0.99        -0.97
salary_thousands              0.99              1.00        -0.95
absent_days                  -0.97             -0.95         1.00
Error: could not convert string to float: 'A'
```
Selecting numbers first avoids the error. (Alternatively, employees.corr(numeric_only=True).)
**Likely follow-ups:** 1) *Excel equivalent?* CORREL for one pair, or ToolPak Correlation for a matrix. 2) *Strong correlation but odd scatter?* Plot it; outliers can fake or hide a link.
**Common mistakes:** Including ID columns (meaningless); reading 0.99 as causation; ignoring outliers.

### Q31 ⭐ 🟢 What does mode() return in pandas, and why is the result a Series and not a single number?
**Asked at:** commonly asked (no company-specific report found); gap-filled from standard practice.
**What the interviewer is checking:** Do you know data can have several modes and how to get one value out?
**Say this in the interview:** "Mode is the most frequent value. pandas returns a Series because there can be ties: if two values appear equally often, both are modes. To get a single number I take .mode()[0]."
**Explain simply:**
- **Mode** = the value that appears most often; useful for categories such as the most common department.
- Ties give several values; if all values are unique, every value is returned.
- Excel's MODE.SNGL returns only the first mode, and #N/A if nothing repeats.
**Worked example:** Shift lengths 3, 3, 5, 5, 7 give modes 3 and 5. Departments Sales, HR, Sales, IT give Sales.
**Excel / Python:**
```python
import pandas as pd

# Two values tie for most common
shift_lengths = pd.Series([3, 3, 5, 5, 7])
print(shift_lengths.mode())

# Text column: one winner, still a Series
departments = pd.Series(["Sales", "HR", "Sales", "IT"])
print(departments.mode())
print("First value:", departments.mode()[0])

# All values unique: every value is a mode
print(pd.Series([1, 2, 3]).mode().tolist())
```
Output:
```
0    3
1    5
dtype: int64
0    Sales
dtype: str
First value: Sales
[1, 2, 3]
```
The index numbers 0 and 1 are just positions of the modes. The dtype label "str" depends on the pandas version (older versions print "object").
**Likely follow-ups:** 1) *Excel with ties?* MODE.MULT (2010+, array formula). 2) *Mode of a numeric salary column?* Rarely useful; bin the values first.
**Common mistakes:** Treating the Series as a number in arithmetic; using mode on continuous values.

### Q32 ⭐ 🟡 How do you use NORM.DIST, NORM.S.DIST and NORM.INV in Excel to find probabilities and cut-off values?
**Asked at:** commonly asked (no company-specific report found); gap-filled from standard practice.
**What the interviewer is checking:** Do you know cumulative probability versus the inverse (cut-off), and the role of the TRUE flag?
**Say this in the interview:** "NORM.DIST with TRUE gives the chance of being at or below a value. NORM.S.DIST does the same for a z-score. NORM.INV goes the other way: give a probability, get the cut-off value."
**Explain simply:**
- **Normal distribution** is the bell curve described by a mean and a standard deviation.
- **NORM.DIST(x, mean, sd, TRUE)** = P(value is at most x); FALSE gives curve height, rarely needed.
- **NORM.S.DIST(z, TRUE)** is the standard normal (mean 0, sd 1).
- **NORM.INV(p, mean, sd)** returns the value below which p of the data lies.
**Worked example:** Assessment scores, mean 60, sd 8. P(score at most 70) = 0.8944. P(above 75) = 1 minus NORM.DIST(75,...) = 0.0304. P(50 to 70) = 0.7887. The cut-off for the top 10% (90th percentile) is 70.25.
**Excel / Python:**
Excel (2010+; not run in Excel here, matched to Python): `=NORM.DIST(70,60,8,TRUE)` returns 0.8944; `=1-NORM.DIST(75,60,8,TRUE)` returns 0.0304; `=NORM.S.DIST(2.5,TRUE)` returns 0.9938; `=NORM.INV(0.9,60,8)` returns 70.25.
```python
from scipy import stats

# Assessment scores: mean 60, standard deviation 8
print("P(score <= 70):", round(stats.norm.cdf(70, 60, 8), 4))
print("P(score > 75):", round(stats.norm.sf(75, 60, 8), 4))
print("P(50 <= score <= 70):", round(stats.norm.cdf(70, 60, 8) - stats.norm.cdf(50, 60, 8), 4))
print("Cut-off for top 10%:", round(stats.norm.ppf(0.90, 60, 8), 2))
print("Standard normal P(z <= 2.5):", round(stats.norm.cdf(2.5), 4))
print("z for 95th percentile:", round(stats.norm.ppf(0.95), 4))
```
Output:
```
P(score <= 70): 0.8944
P(score > 75): 0.0304
P(50 <= score <= 70): 0.7887
Cut-off for top 10%: 70.25
Standard normal P(z <= 2.5): 0.9938
z for 95th percentile: 1.6449
```
About 3% of employees would score above 75, and scoring 70.25 or more puts you in the top 10%.
**Likely follow-ups:** 1) *Probability of exactly one value?* Zero for a continuous variable; use ranges. 2) *Is my data normal?* Check a histogram or skew first.
**Common mistakes:** Using FALSE and expecting a probability; forgetting "1 minus" for the upper tail; using sample data that is clearly skewed.

### Q33 ⭐ 🟡 How do you use BINOM.DIST and POISSON.DIST in Excel, with a worked example?
**Asked at:** commonly asked (no company-specific report found); gap-filled from standard practice.
**What the interviewer is checking:** Can you pick binomial (fixed tries) versus Poisson (events per time) and use the cumulative flag correctly?
**Say this in the interview:** "Binomial counts successes in a fixed number of independent tries with the same chance, like offer rejections out of 12 offers. Poisson counts events per period at an average rate, like resignations per month. In both, FALSE gives exactly k and TRUE gives k or fewer."
**Explain simply:**
- **BINOM.DIST(k, n, p, cumulative)**: n tries, chance p each.
- **POISSON.DIST(k, mean, cumulative)**: mean events per period, events independent.
- "More than k" = 1 minus the cumulative probability at k.
**Worked example:** Binomial: 12 offers, each with 15% chance of rejection. P(exactly 3 reject) = 0.1720; P(3 or fewer) = 0.9078; P(more than 3) = 0.0922. Poisson: 4 resignations per month on average. P(exactly 2) = 0.1465; P(2 or fewer) = 0.2381; P(more than 5) = 0.2149.
**Excel / Python:**
Excel (2010+; not run in Excel here, matched to Python): `=BINOM.DIST(3,12,0.15,FALSE)` returns 0.1720; `=1-BINOM.DIST(3,12,0.15,TRUE)` returns 0.0922; `=POISSON.DIST(2,4,FALSE)` returns 0.1465; `=1-POISSON.DIST(5,4,TRUE)` returns 0.2149.
```python
from scipy import stats

# Binomial: 12 offers, each 15% chance of rejection
print("P(exactly 3):", round(stats.binom.pmf(3, 12, 0.15), 4))
print("P(3 or fewer):", round(stats.binom.cdf(3, 12, 0.15), 4))
print("P(more than 3):", round(1 - stats.binom.cdf(3, 12, 0.15), 4))

# Poisson: 4 resignations per month on average
print("P(exactly 2):", round(stats.poisson.pmf(2, 4), 4))
print("P(2 or fewer):", round(stats.poisson.cdf(2, 4), 4))
print("P(more than 5):", round(1 - stats.poisson.cdf(5, 4), 4))
```
Output:
```
P(exactly 3): 0.172
P(3 or fewer): 0.9078
P(more than 3): 0.0922
P(exactly 2): 0.1465
P(2 or fewer): 0.2381
P(more than 5): 0.2149
```
A month with more than 5 resignations happens roughly one month in five, so it is not alarming on its own.
**Likely follow-ups:** 1) *When does Poisson fit badly?* When events cluster, such as batch layoffs. 2) *Binomial assumption that can fail?* Independence between candidates.
**Common mistakes:** Mixing up TRUE and FALSE; using Poisson when there is a fixed number of tries; computing "more than k" with the cumulative at k+1.

### Q34 ⭐ 🟡 How do you forecast the next value in Excel using FORECAST.LINEAR or TREND, and what are the limits of the forecast?
**Asked at:** commonly asked; FORECAST and TREND appear in Excel FAQ lists (weak, user-uploaded source), with no company-specific report.
**What the interviewer is checking:** Can you forecast with a straight line and be honest about how far to trust it?
**Say this in the interview:** "FORECAST.LINEAR fits a straight line to past data and reads off the value for a new X. TREND does the same for one or many new X values. The limits: it assumes the trend stays straight, so it is only reliable for the near future."
**Explain simply:**
- **FORECAST.LINEAR(x, known_y's, known_x's)** returns one predicted value; it needs Excel 2016+ (older versions have FORECAST).
- **TREND(known_y's, known_x's, new_x's)** returns predictions for several points at once.
- Both ignore seasonality (such as hiring peaks) and sudden changes.
- Predicting far past the data (extrapolation) is risky.
**Worked example:** Monthly hires for months 1 to 6: 20, 24, 25, 29, 33, 34. The line: slope 2.89 hires per month, intercept 17.4, R-squared 0.975. Forecast month 7 = 37.6, month 8 = 40.49. Month 18 gives 69.34, which is not credible if hiring is capped by headcount budget.
**Excel / Python:**
Excel (not run in Excel here, matched to Python). Months in A2:A7, hires in B2:B7: `=FORECAST.LINEAR(7,B2:B7,A2:A7)` returns 37.6; `=TREND(B2:B7,A2:A7,A8)` with 7 in A8 returns 37.6 too. Note Y first, then X.
```python
import numpy as np
from scipy import stats

month_number = np.array([1, 2, 3, 4, 5, 6])
hires = np.array([20, 24, 25, 29, 33, 34])

fit = stats.linregress(month_number, hires)
print("Slope:", round(fit.slope, 4), "Intercept:", round(fit.intercept, 4), "R-squared:", round(fit.rvalue**2, 4))
print("Month 7:", round(fit.intercept + fit.slope * 7, 2))
print("Month 8:", round(fit.intercept + fit.slope * 8, 2))
print("Month 18:", round(fit.intercept + fit.slope * 18, 2))
```
Output:
```
Slope: 2.8857 Intercept: 17.4 R-squared: 0.9748
Month 7: 37.6
Month 8: 40.49
Month 18: 69.34
```
The next month or two are reasonable; month 18 is a big stretch beyond six data points.
**Likely follow-ups:** 1) *Seasonal data?* Use FORECAST.ETS (2016+). 2) *How would you show uncertainty?* Give a range, for example with FORECAST.ETS.CONFINT or a prediction interval.
**Common mistakes:** Swapping X and Y; forecasting far ahead; ignoring seasonality or a recent change in trend.

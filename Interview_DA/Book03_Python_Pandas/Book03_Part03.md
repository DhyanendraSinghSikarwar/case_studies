# Book 3 — Python & pandas for Analysts | Part 3: NumPy Basics 🟢

**Target:** 25 questions | **Actual:** 30 questions
**Scope:** NumPy fundamentals for data analysts: arrays, indexing, vectorization, axis, broadcasting, np.where, NaN handling and common errors, with small HR-flavoured live-coding tasks.

### Q1 ⭐⭐⭐ 🟢 What is NumPy, and why do data analysts use it?
**Asked at:** commonly asked (no company-specific report found); a Tiger Analytics candidate report mentions basic NumPy/pandas questions (unverified, snippet only).
**What the interviewer is checking:** Do you know what NumPy is for, and that pandas sits on top of it.
**Say this in the interview:** "NumPy is Python's library for fast number crunching. It gives you the array, a grid of numbers of one type, so I can do maths on a whole column at once instead of looping. Pandas is built on it."
**Explain simply:**
- **Library:** a ready-made toolbox of code you import (`import numpy as np`).
- **Array (ndarray):** a fixed-type list of numbers, 1D (a row) or 2D (a table of rows and columns).
- **Why analysts use it:** it is much faster than plain Python loops, uses less memory, and has built-in sum, mean, min, max and filters.
- **Why you still care when you use pandas:** number columns in pandas are stored as NumPy arrays, so its rules (data types, NaN, axis) carry over.
**What it means:** think of it as Excel-style whole-column maths, but for millions of rows in code.
**Likely follow-ups:**
- *Why not just use lists?* Lists are slow for maths and have no vector operations (see Q2).
- *Do you use NumPy directly at work?* Mostly through pandas; directly for quick calculations like `np.where` and `np.mean`.
**Common mistakes:** saying NumPy is "for machine learning only", or forgetting the usual alias `np`.

### Q2 ⭐⭐⭐ 🟢 What is the difference between a Python list and a NumPy array?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know arrays hold one type and do maths element by element.
**Say this in the interview:** "A list can mix types and `*` repeats it. A NumPy array holds one type and `*` multiplies every value. Arrays are faster and use less memory."
**Explain simply:**
- **List:** flexible, can hold numbers, text and more together, but maths needs a loop.
- **Array:** every item has the same type (for example all integers), stored compactly, so maths is fast.
- **Element-wise:** the operation is applied to each value separately.
- **Fixed size:** an array does not grow like `list.append`; you build a new one.
**Sample data:** three salaries, 30000, 45000, 60000.
**Code (what you write in the interview):**
```python
import numpy as np

salary_list = [30000, 45000, 60000]
salary_array = np.array([30000, 45000, 60000])

# On a list, * 2 repeats the list
print(salary_list * 2)

# On an array, * 2 doubles every value
print(salary_array * 2)
```
**Output:**
```
[30000, 45000, 60000, 30000, 45000, 60000]
[ 60000  90000 120000]
```
**What it means:** the same `* 2` gives a repeated list but a doubled array.
**Likely follow-ups:**
- *What if an array has mixed types?* NumPy converts them all to one type (ints and floats become floats; adding text turns everything into text).
- *When is a list better?* Small, mixed or growing collections.
**Common mistakes:** expecting `list * 2` to double the values; thinking arrays can hold mixed types.

### Q3 ⭐⭐⭐ 🟢 How do you create a NumPy array from a list and check its shape, size and data type?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic array creation and the three attributes `shape`, `size`, `dtype`.
**Say this in the interview:** "`np.array(list)` creates it. `.shape` gives the rows and columns, `.size` the total number of values, `.dtype` the type of the values."
**Explain simply:**
- **shape:** a tuple of dimensions. `(4,)` means 1D with 4 items; `(2, 2)` means 2 rows and 2 columns.
- **size:** total count of values (rows times columns).
- **dtype:** data type, such as `int64` (whole numbers) or `float64` (decimals).
- These are attributes, not functions, so no brackets.
**Sample data:** four salaries, and a 2 by 2 version.
**Code (what you write in the interview):**
```python
import numpy as np

salaries = np.array([30000, 45000, 60000, 52000])

print(salaries.shape)
print(salaries.size)
print(salaries.dtype)

# A list of lists makes a 2D array
two_d = np.array([[30000, 45000], [60000, 52000]])
print(two_d.shape, two_d.size, two_d.dtype)
```
**Output:**
```
(4,)
4
int64
(2, 2) 4 int64
```
**What it means:** the first array has 4 values in one dimension; the second has 2 rows and 2 columns, 4 values in all.
**Likely follow-ups:**
- *What dtype if the list has 1, 2.5, 3?* `float64`, because NumPy upgrades to fit the decimal.
- *How many dimensions?* `.ndim`.
**Common mistakes:** writing `salaries.shape()` with brackets (error); confusing `size` with `len` on 2D arrays (`len` gives rows only). The dtype `int64` is the default on Linux/Mac; on some Windows setups older NumPy gave `int32` (from memory, unverified).

### Q4 ⭐⭐⭐ 🟢 How do you select elements from a 1D and a 2D NumPy array using indexing and slicing?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Zero-based indexing, slice ends, and the `[row, column]` form.
**Say this in the interview:** "Indexing starts at 0. A slice `a[1:4]` includes position 1 but stops before 4. For 2D I write `a[row, column]`, and a colon means all."
**Explain simply:**
- **Index:** the position of a value; the first is 0, the last is -1.
- **Slice:** `start:stop`, where stop is not included.
- **2D:** `array[row, column]`; `[:, 1]` means all rows, column 1.
- A slice gives back a smaller array, a single index gives one value.
**Sample data:** five salaries; a 3 by 3 table (rows are employees, columns are months).
**Code (what you write in the interview):**
```python
import numpy as np

salaries = np.array([30000, 45000, 60000, 52000, 75000])
print(salaries[0])       # first value
print(salaries[-1])      # last value
print(salaries[1:4])     # positions 1, 2, 3

pay = np.array([[30000, 31000, 32000],
                [45000, 46000, 47000],
                [60000, 61000, 62000]])
print(pay[1, 2])         # row 1, column 2
print(pay[0])            # whole first row
print(pay[:, 1])         # whole column 1
print(pay[0:2, 1:3])     # first two rows, last two columns
```
**Output:**
```
30000
75000
[45000 60000 52000]
47000
[30000 31000 32000]
[31000 46000 61000]
[[31000 32000]
 [46000 47000]]
```
**What it means:** `pay[:, 1]` pulls the second month for every employee.
**Likely follow-ups:**
- *Does a slice copy the data?* No, it is a view of the same data (changing it changes the original).
- *Difference from `pay[0][1]`?* Same result, but `pay[0, 1]` is one step and clearer.
**Common mistakes:** thinking the stop index is included; counting from 1; mixing up row and column order.

### Q5 ⭐⭐⭐ 🟢 Write code to filter a NumPy array of salaries to keep only values above 50,000 (boolean indexing).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can filter with a condition instead of a loop.
**Say this in the interview:** "I write the condition `salaries > 50000`, which gives True/False for each value, and pass that inside the brackets to keep only the True ones."
**Explain simply:**
- **Boolean array:** a list of True/False answers, one per value.
- **Boolean indexing:** using that True/False list as a filter; True rows stay.
- It works like a filter in Excel, but in one line.
- The result is a new, shorter array.
**Sample data:** `[32000, 58000, 47000, 91000, 50000, 65000]`
**Code (what you write in the interview):**
```python
import numpy as np

salaries = np.array([32000, 58000, 47000, 91000, 50000, 65000])

# Keep only salaries strictly above 50,000
high_salaries = salaries[salaries > 50000]
print(high_salaries)
```
**Output:**
```
[58000 91000 65000]
```
**What it means:** 50,000 itself is dropped because the rule is "above"; use `>=` to keep it.
**Likely follow-ups:**
- *Two conditions?* Use `&` with brackets (see Q23 of this part).
- *How many matched?* `(salaries > 50000).sum()` (see Q12).
**Common mistakes:** using `>=` by accident; writing a Python `if` or `for` loop when one line is enough.

### Q6 ⭐⭐⭐ 🟢 Write code to find the sum, mean, minimum and maximum of a NumPy array of daily attendance counts.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Built-in aggregate methods on arrays.
**Say this in the interview:** "Arrays have `.sum()`, `.mean()`, `.min()` and `.max()` built in, so no loop is needed."
**Explain simply:**
- **Aggregate:** one number that summarises many values.
- **Mean:** the average, total divided by count.
- Each method returns a single number for a 1D array.
- For a 2D array you can add `axis` (see Q8).
**Sample data:** seven days of attendance: `[120, 118, 125, 110, 130, 95, 101]`
**Code (what you write in the interview):**
```python
import numpy as np

daily_attendance = np.array([120, 118, 125, 110, 130, 95, 101])

print(daily_attendance.sum())
print(daily_attendance.mean())
print(daily_attendance.min())
print(daily_attendance.max())
```
**Output:**
```
799
114.14285714285714
95
130
```
**What it means:** 799 attendances in the week, about 114 per day, lowest day 95, highest 130.
**Likely follow-ups:**
- *Which day had the lowest?* `daily_attendance.argmin()` gives the position (Q22).
- *What if there is a NaN?* `sum` and `mean` become `nan`; use `np.nanmean` (Q20).
**Common mistakes:** forgetting that `mean` of integers returns a decimal; using Python's `sum()` on large arrays (works but slower).

### Q7 ⭐⭐⭐ 🟢 Write code to add a 10% hike to every value in a NumPy array of salaries without using a loop.
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured version of the vectorization basics.
**What the interviewer is checking:** Whether you use whole-array maths.
**Say this in the interview:** "I multiply the whole array by 1.10. NumPy applies it to every salary, so no loop."
**Explain simply:**
- **10% hike:** new salary = old salary times 1.10 (old plus 10% of old).
- **Vectorised:** one operation applied to all values together.
- **Decimals:** the result is float because 1.10 is a decimal.
**Sample data:** `[30000, 45000, 60000, 52000]`
**Code (what you write in the interview):**
```python
import numpy as np

salaries = np.array([30000, 45000, 60000, 52000])

# Multiply by 1.10 for a 10% hike
new_salaries = salaries * 1.10
print(new_salaries)
```
**Output:**
```
[33000. 49500. 66000. 57200.]
```
**What it means:** each salary rose by 10%; the original array is unchanged.
**Likely follow-ups:**
- *Whole rupees only?* `np.round(new_salaries)` or `.astype(int)` (Q14).
- *Hike only for salaries under 40,000?* `np.where(salaries < 40000, salaries * 1.10, salaries)`.
**Common mistakes:** multiplying by 0.10 (that gives only the hike amount); adding 10 instead of 10%; tiny float noise (the second salary is stored as 49500.00000000001) shows up if you print with more precision, so round for reports.

### Q8 ⭐⭐⭐ 🟡 What does the axis parameter mean in NumPy, and what is the difference between axis=0 and axis=1?
**Asked at:** commonly asked (no company-specific report found); axis is a named topic in Adaface and other lists (snippet).
**What the interviewer is checking:** Whether you can say which direction a calculation runs.
**Say this in the interview:** "`axis=0` collapses the rows, so you get one result per column. `axis=1` collapses the columns, so you get one result per row."
**Explain simply:**
- **Axis:** the direction along which a function works.
- **axis=0:** go down the rows; answer per column.
- **axis=1:** go across the columns; answer per row.
- Memory trick: the axis you name is the one that disappears.
**Sample data:** hours worked, rows are 2 employees, columns are 3 days.
**Code (what you write in the interview):**
```python
import numpy as np

hours = np.array([[8, 9, 7],
                  [6, 8, 8]])

# Total per day (one result per column)
print(hours.sum(axis=0))

# Total per employee (one result per row)
print(hours.sum(axis=1))
```
**Output:**
```
[14 17 15]
[24 22]
```
**What it means:** the team worked 14, 17 and 15 hours on days 1 to 3; employee 1 worked 24 hours, employee 2 worked 22.
**Likely follow-ups:**
- *What without axis?* It totals every value into one number (46 here).
- *Same in pandas?* Yes, `axis=0` is down rows (per column), `axis=1` across (per row).
**Common mistakes:** reversing the two; thinking axis=0 means "by row".

### Q9 ⭐⭐⭐ 🟡 What is vectorization in NumPy, and why is it faster than a Python loop?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you understand why arrays beat loops, not just that they do.
**Say this in the interview:** "Vectorization means one operation on the whole array. The loop runs inside NumPy's compiled C code on same-type data, instead of Python handling each value one by one."
**Explain simply:**
- **Vectorization:** writing `array * 1.10` instead of a `for` loop.
- **Why faster:** (1) the loop runs inside NumPy in compiled C code (code already translated to machine instructions), not in interpreted Python, which reads one line at a time; (2) values sit side by side in memory with one type, so there is no per-item type checking.
- **Also shorter and clearer**, which matters for readable analysis.
- Timed on 1 million values on pandas 3.0.5 / NumPy 2.5.3: looping over the NumPy array took about 1.6 seconds, looping over a plain list about 50 ms, and the vectorised line about 1 ms. Exact times depend on the machine; the order does not.
**Sample data:** `[30000, 45000, 60000, 52000]`
**Code (what you write in the interview):**
```python
import numpy as np

salaries = np.array([30000, 45000, 60000, 52000])

# Loop version: touches one value at a time
new_salaries_loop = []
for salary in salaries:
    new_salaries_loop.append(salary * 1.10)

# Vectorised version: one line, whole array
new_salaries = salaries * 1.10
print(new_salaries)
```
**Output:**
```
[33000. 49500. 66000. 57200.]
```
**What it means:** both versions give the same answer; the second is shorter and much faster on big data.
**Likely follow-ups:**
- *Is a loop ever fine?* Yes, for tiny data or logic that cannot be expressed in array form.
- *Name vectorised functions.* `np.sum`, `np.sqrt`, `np.where`, and operators like `+`, `>`.
**Common mistakes:** looping over a NumPy array out of habit; claiming "NumPy is faster because it is magic" without naming C and same-type storage.

### Q10 ⭐⭐ 🟢 How do you create arrays quickly using np.zeros, np.ones, np.arange and np.linspace?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the quick creators and the arange vs linspace difference.
**Say this in the interview:** "`zeros` and `ones` make arrays of 0s and 1s of a given shape. `arange` counts by a step size; `linspace` gives a set number of evenly spaced points including the end."
**Explain simply:**
- **np.zeros(4) / np.ones((2, 3)):** pass a shape; they start as floats.
- **np.arange(start, stop, step):** like `range`; stop is not included.
- **np.linspace(start, stop, count):** you choose how many points; stop is included.
- Use `zeros` as a blank table to fill later.
**Code (what you write in the interview):**
```python
import numpy as np

print(np.zeros(4))
print(np.ones((2, 3)))
print(np.arange(1, 10, 2))
print(np.linspace(0, 100, 5))
```
**Output:**
```
[0. 0. 0. 0.]
[[1. 1. 1.]
 [1. 1. 1.]]
[1 3 5 7 9]
[  0.  25.  50.  75. 100.]
```
**What it means:** `arange` stepped by 2 and stopped before 10; `linspace` gave exactly 5 points from 0 to 100.
**Likely follow-ups:**
- *When use linspace?* When you know how many points you want, especially with decimal steps.
- *Why avoid arange with decimals?* Float steps can give surprising lengths; linspace is safer.
**Common mistakes:** passing `np.zeros(2, 3)` instead of `np.zeros((2, 3))` (shape needs its own brackets); expecting `arange` to include the stop value.

### Q11 ⭐⭐ 🟢 How do you change the shape of a NumPy array using reshape?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That the total count must stay the same, and what -1 does.
**Say this in the interview:** "`reshape(rows, columns)` rearranges the same values into a new grid. The numbers must multiply to the original size, and -1 lets NumPy work out one dimension."
**Explain simply:**
- **Reshape:** same data, new layout; no values change.
- **Rule:** rows times columns must equal the size (12 values can be 3 by 4, not 5 by 3).
- **-1:** "figure this one out for me".
**Sample data:** 12 months numbered 1 to 12.
**Code (what you write in the interview):**
```python
import numpy as np

monthly = np.arange(1, 13)

# 3 rows (quarters) by 4 columns
quarters = monthly.reshape(3, 4)
print(quarters)

# Let NumPy work out the columns
print(monthly.reshape(4, -1).shape)
```
**Output:**
```
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]]
(4, 3)
```
**What it means:** 12 values fit in 3 rows of 4, or 4 rows of 3 when -1 is used.
**Likely follow-ups:**
- *What if sizes do not match?* `ValueError: cannot reshape array of size 12 into shape (5,3)`.
- *Does it copy?* Usually it returns a view of the same data.
**Common mistakes:** choosing a shape that does not multiply to the size; using -1 more than once.

### Q12 ⭐⭐ 🟢 How do you count how many values in a NumPy array satisfy a condition (for example, employees with more than 5 years of experience)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know True counts as 1, so `.sum()` counts matches.
**Say this in the interview:** "The condition gives True/False for each value. Summing it counts the Trues, because True is 1 and False is 0."
**Explain simply:**
- **Condition array:** `experience_years > 5` gives True/False per employee.
- **Sum of booleans:** each True adds 1, so the sum is the count.
- **Mean of booleans:** gives the share (a percentage once multiplied by 100).
**Sample data:** years of experience: `[2, 7, 5, 10, 6, 1, 8]`
**Code (what you write in the interview):**
```python
import numpy as np

experience_years = np.array([2, 7, 5, 10, 6, 1, 8])

more_than_five = experience_years > 5
print(more_than_five.sum())

# Share of employees, as a fraction
print(more_than_five.mean())
```
**Output:**
```
4
0.5714285714285714
```
**What it means:** 4 of 7 employees (about 57%) have more than 5 years; the one with exactly 5 is not counted.
**Alternative:** `np.count_nonzero(experience_years > 5)` gives the same 4.
**Likely follow-ups:**
- *Count with two conditions?* Combine with `&` first (Q23).
- *How to see who they are?* `experience_years[experience_years > 5]`.
**Common mistakes:** using `len(experience_years > 5)` (that returns 7, the total length); `>` vs `>=`.

### Q13 ⭐⭐ 🟢 How does NumPy relate to pandas?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know pandas is built on NumPy and when to use which.
**Say this in the interview:** "Pandas is built on top of NumPy. Each DataFrame column is backed by a NumPy array, and pandas adds labels, mixed column types, missing-data handling and table tools like groupby."
**Explain simply:**
- **NumPy:** raw grid of same-type numbers, no column names.
- **Pandas:** table with column names and row labels, different types per column, and tools for real-world messy data.
- **Link:** a Series or column converts to an array with `.to_numpy()`, and arrays go into pandas with `pd.Series(array)`.
- Many NumPy functions (`np.where`, `np.mean`) work directly on pandas columns.
- Rule of thumb: tables and files in pandas; fast number maths in NumPy.
**Sample data:** salaries 30000, 45000, 60000 in a DataFrame.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"salary": [30000, 45000, 60000]})

# Pull the column out as a NumPy array
salary_array = employees["salary"].to_numpy()
print(salary_array)
print(type(salary_array))
```
**Output:**
```
[30000 45000 60000]
<class 'numpy.ndarray'>
```
**What it means:** the pandas column converts straight to a NumPy array.
**Likely follow-ups:**
- *Is pandas always NumPy underneath?* For number columns, yes. Text is different: in pandas 3.0.5 a text column has the `str` dtype, which is not a NumPy array (it uses Arrow storage when the pyarrow package is installed, from memory, unverified). Also in pandas 3, `to_numpy()` on a column can return a read-only array, so call `.copy()` if you need to edit it.
- *Why not only NumPy?* No labels, no mixed types, awkward for missing data and grouping.
**Common mistakes:** saying pandas replaces NumPy; forgetting that both must be imported separately.

### Q14 ⭐⭐ 🟢 How do you change the data type of a NumPy array (for example, float to int)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** `astype`, and that converting to int cuts decimals instead of rounding.
**Say this in the interview:** "I use `astype(int)`. It returns a new array and truncates decimals, so I round first if I want proper rounding."
**Explain simply:**
- **astype:** makes a converted copy; the original stays as it was.
- **Truncate:** `45000.99` becomes `45000`; the decimal part is chopped, not rounded.
- **Strings of digits:** `astype(int)` also turns text like "30000" into numbers.
**Sample data:** `[30000.75, 45000.5, 60000.99]`
**Code (what you write in the interview):**
```python
import numpy as np

salaries = np.array([30000.75, 45000.5, 60000.99])

# Cuts off the decimals
print(salaries.astype(int))

# Rounds first, then converts
print(np.round(salaries).astype(int))
```
**Output:**
```
[30000 45000 60000]
[30001 45000 60001]
```
**What it means:** plain `astype(int)` lost the .75 and .99 instead of rounding; the second line rounded properly.
**Likely follow-ups:**
- *What about text?* `np.array(["30000", "45000"]).astype(int)` gives `[30000 45000]`; text that is not a number raises an error.
- *Does it change the original?* No, assign the result to keep it.
**Common mistakes:** assuming `astype` rounds; not assigning the result; the .5 case rounds to the nearest even number (45000.5 became 45000), so tell the interviewer if exact rounding matters.

### Q15 ⭐⭐ 🟢 Write code to find the unique values in a NumPy array and how many times each appears.
**Asked at:** a Tiger Analytics candidate report mentions removing duplicates using NumPy or pandas (search-engine summary, page not opened).
**What the interviewer is checking:** `np.unique` and its `return_counts` option.
**Say this in the interview:** "`np.unique` returns the sorted distinct values. Adding `return_counts=True` also gives how many times each appears."
**Explain simply:**
- **Unique:** each distinct value once (duplicates removed).
- **return_counts=True:** returns a second array of counts in the same order.
- **Sorted:** the values come out in sorted order, not original order.
**Sample data:** employee departments: `["HR", "IT", "HR", "Sales", "IT", "HR"]`
**Code (what you write in the interview):**
```python
import numpy as np

departments = np.array(["HR", "IT", "HR", "Sales", "IT", "HR"])

department_names, headcount = np.unique(departments, return_counts=True)
print(department_names)
print(headcount)
```
**Output:**
```
['HR' 'IT' 'Sales']
[3 2 1]
```
**What it means:** HR has 3 employees, IT 2, Sales 1; the two arrays line up by position.
**Alternative:** `np.unique(array)` alone just removes duplicates (for example `[3,1,3,2,1]` becomes `[1 2 3]`). In pandas, `pd.Series(departments).value_counts()` does the same.
**Likely follow-ups:**
- *Remove duplicates but keep the original order?* `np.unique` sorts, so use pandas `drop_duplicates()` instead.
- *Which department is the largest?* `department_names[headcount.argmax()]`.
**Common mistakes:** expecting original order; forgetting that counts come back as a second value, so unpacking into one name gives a tuple.

### Q16 ⭐⭐ 🟢 How do you sort a NumPy array, and what does np.argsort return?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know `np.sort` returns sorted values, while `np.argsort` returns positions, and you can use those positions to reorder a second array.
**Say this in the interview:** "`np.sort` gives me the values in order. `np.argsort` gives me the index positions that would sort the array, so I can use them to sort another array, like names, in the same order."
**Explain simply:**
- `np.sort(array)` returns a new sorted copy (lowest to highest); the original is not changed.
- `np.argsort(array)` does not return salaries; it returns positions. Here `[1 0 3 2]` means "the smallest value is at position 1, the next at position 0", and so on.
- Positions are useful when two arrays line up (names and salaries). Sorting salaries alone would break the link to names.
- For highest first, reverse the result with `[::-1]`.
**Sample data:** salaries `[45000, 30000, 60000, 52000]` for Asha, Ravi, Meena, Kiran.
**Code (what you write in the interview):**
```python
import numpy as np

salaries = np.array([45000, 30000, 60000, 52000])
names = np.array(["Asha", "Ravi", "Meena", "Kiran"])

# Sorted copy of the salaries (lowest to highest)
sorted_salaries = np.sort(salaries)

# argsort gives the POSITIONS that would sort the array
sort_positions = np.argsort(salaries)

# Use the positions to put the names in the same order
names_by_salary = names[sort_positions]

print(sorted_salaries)
print(sort_positions)
print(names_by_salary)
```
**Output:**
```text
[30000 45000 52000 60000]
[1 0 3 2]
['Ravi' 'Asha' 'Kiran' 'Meena']
```
**What it means:** Ravi earns the least and Meena the most. `argsort` let us sort the names by salary without losing who earns what.
**Likely follow-ups:** 1) *How do I sort in descending order?* `np.sort(salaries)[::-1]`. 2) *Sort a 2D array?* `np.sort(array, axis=1)` sorts each row; `axis=0` sorts each column.
**Common mistakes:** Thinking `argsort` returns sorted values; sorting two related arrays separately so names and salaries no longer match.

### Q17 ⭐⭐ 🟡 What is broadcasting in NumPy? Explain with an example of subtracting column averages from a 2D array.
**Asked at:** commonly asked (no company-specific report found); broadcasting is listed in NumPy question sets (Adaface).
**What the interviewer is checking:** Whether you understand that NumPy can combine arrays of different shapes by stretching the smaller one, without a loop.
**Say this in the interview:** "Broadcasting means NumPy automatically stretches a smaller array to match a bigger one so they can be used in one operation. For example, I can subtract a row of three column averages from every row of a table in one line."
**Explain simply:**
- Broadcasting: NumPy repeats the smaller array across the bigger one (without really copying it) so the shapes fit.
- Rule of thumb: compare shapes from the right; each pair of sizes must be equal, or one of them must be 1.
- Here the table is 3 rows by 3 columns and the averages are 3 values (one per column), so the 3 averages are applied to every row.
- It replaces a loop over rows, so it is shorter and faster.
**Sample data:** rows are employees, columns are Jan, Feb, Mar sales.
**Code (what you write in the interview):**
```python
import numpy as np

# Rows are employees, columns are Jan, Feb, Mar
monthly_sales = np.array([[10, 20, 30],
                          [20, 40, 60],
                          [30, 60, 90]])

# One average per column (axis=0 means down the rows)
column_averages = monthly_sales.mean(axis=0)

# NumPy stretches the 3 averages across every row automatically
difference_from_average = monthly_sales - column_averages

print(column_averages)
print(difference_from_average)
```
**Output:**
```text
[20. 40. 60.]
[[-10. -20. -30.]
 [  0.   0.   0.]
 [ 10.  20.  30.]]
```
**What it means:** Each number now shows how far that employee is above or below the average for that month. The middle employee sits exactly on the average.
**Likely follow-ups:** 1) *What if I want row averages instead?* Use `mean(axis=1, keepdims=True)` so the shape is 3 by 1 and stretches across columns. Without `keepdims` the shapes do not line up: a 2 by 3 table raises a `ValueError`, and a square 3 by 3 table gives no error but silently wrong numbers. 2) *When does broadcasting fail?* When sizes differ and neither is 1 (for example 3 columns against 4 values); NumPy raises a `ValueError`.
**Common mistakes:** Using the wrong axis for the averages; forgetting `keepdims=True` for row-wise operations.

### Q18 ⭐⭐ 🟡 How do you use np.where to create a label array, for example "Present" or "Absent", from an attendance-hours array?
**Asked at:** commonly asked (no company-specific report found); `np.where` conditional labelling is a standard NumPy topic (Algocademy tutorial).
**What the interviewer is checking:** That you can do an if/else on a whole array in one step instead of a loop.
**Say this in the interview:** "`np.where(condition, value_if_true, value_if_false)` checks every element and picks one of two values. It is like an IF formula in Excel applied to the whole array."
**Explain simply:**
- Three parts: the condition, what to return where it is True, what to return where it is False.
- It returns a new array of the same length; the original hours are untouched.
- For more than two labels (Present, Half day, Absent) use `np.select` or nest `np.where` calls.
**Sample data:** hours worked `[8.5, 0, 4, 9, 0, 7.5]`.
**Code (what you write in the interview):**
```python
import numpy as np

attendance_hours = np.array([8.5, 0, 4, 9, 0, 7.5])

# If hours are above 0 write "Present", otherwise "Absent"
status = np.where(attendance_hours > 0, "Present", "Absent")

print(status)
```
**Output:**
```text
['Present' 'Absent' 'Present' 'Present' 'Absent' 'Present']
```
**What it means:** Two employees had 0 hours, so they are labelled Absent; everyone else is Present.
**Likely follow-ups:** 1) *What if "Present" means at least 8 hours?* Change the condition to `attendance_hours >= 8`. 2) *What about NaN hours?* `NaN > 0` is False, so a missing value would be labelled Absent; check `np.isnan` first if that matters.
**Common mistakes:** Using a Python `if` on an array (it errors); forgetting that missing values silently fall into the "false" label.

### Q19 ⭐⭐ 🟡 Write code to find the row-wise and column-wise totals of a 2D NumPy array of monthly sales (rows are employees, columns are months).
**Asked at:** commonly asked (no company-specific report found); axis-based aggregation appears in NumPy lists (Adaface).
**What the interviewer is checking:** That you pick the right axis for "per employee" versus "per month".
**Say this in the interview:** "`axis=1` collapses the columns, so I get one total per row, which is per employee. `axis=0` collapses the rows, so I get one total per column, which is per month."
**Explain simply:**
- `axis` is the direction NumPy moves while adding.
- `axis=1` moves across each row (left to right): one answer per employee.
- `axis=0` moves down each column: one answer per month.
- Memory trick: the axis you name is the one that disappears. A 3 by 3 array summed over axis=1 leaves 3 values.
**Sample data:** 3 employees by 3 months.
**Code (what you write in the interview):**
```python
import numpy as np

# Rows are employees, columns are months
monthly_sales = np.array([[100, 200, 300],
                          [150, 250, 350],
                          [120, 220, 320]])

# Total per employee: add across the columns
row_totals = monthly_sales.sum(axis=1)

# Total per month: add down the rows
column_totals = monthly_sales.sum(axis=0)

print(row_totals)
print(column_totals)
```
**Output:**
```text
[600 750 660]
[370 670 970]
```
**What it means:** The first employee sold 600 in total; January sales across all employees were 370.
**Likely follow-ups:** 1) *What does `sum()` with no axis do?* It adds every number into one grand total. 2) *How would I get averages?* Replace `sum` with `mean`.
**Common mistakes:** Swapping axis 0 and 1; expecting the totals to keep the 2D shape (they come back as 1D).

### Q20 ⭐⭐ 🟡 How do you handle NaN (missing values) in a NumPy array: detect them, compute a mean ignoring them, and replace them?
**Asked at:** commonly asked (no company-specific report found); a NaN comparison pitfall is covered in np.where tutorials (Algocademy, snippet only).
**What the interviewer is checking:** That you know a normal `mean` returns NaN when one value is missing, and that you know the `nan`-safe tools.
**Say this in the interview:** "I detect missing values with `np.isnan`, calculate with `np.nanmean` which skips them, and replace them with `np.where`. A plain `mean` would just return NaN."
**Explain simply:**
- NaN means "Not a Number", NumPy's marker for a missing value. It only lives in float arrays.
- NaN is contagious: any calculation touching it gives NaN, so `salaries.mean()` returns `nan`.
- You cannot test with `== np.nan` because NaN is not equal to anything, even itself. Use `np.isnan`.
- Whether to fill with the mean, a zero or drop the rows is a business decision; say so.
**Sample data:** salaries `[40000, nan, 55000, 60000, nan]`.
**Code (what you write in the interview):**
```python
import numpy as np

salaries = np.array([40000, np.nan, 55000, 60000, np.nan])

# Detect: True where the value is missing
is_missing = np.isnan(salaries)

# Mean that skips the missing values
average_salary = np.nanmean(salaries)

# Replace missing values with that average
salaries_filled = np.where(is_missing, average_salary, salaries)

print(is_missing)
print(average_salary)
print(salaries_filled)
```
**Output:**
```text
[False  True False False  True]
51666.666666666664
[40000.         51666.66666667 55000.         60000.
 51666.66666667]
```
**What it means:** Two salaries were missing. The average of the three known values is about 51,667, and that fills the gaps. (For comparison, `salaries.mean()` on the original array returns `nan`.)
**Likely follow-ups:** 1) *Other nan-safe functions?* `np.nansum`, `np.nanmax`, `np.nanmin`. 2) *How to drop the missing values?* `salaries[~np.isnan(salaries)]`.
**Common mistakes:** Testing with `== np.nan`; forgetting that filling with the mean can hide a data quality problem.

### Q21 ⭐⭐ 🟡 What is the difference between a view and a copy in NumPy, and why can it cause bugs?
**Asked at:** commonly asked (no company-specific report found); copy versus view is a recurring NumPy question (TheLinuxCode 2026 list).
**What the interviewer is checking:** That you know slices share memory with the original, so editing a slice can silently change your source data.
**Say this in the interview:** "A view is another window onto the same data, so changing it changes the original. A copy is independent. Basic slicing gives a view, so I use `.copy()` when I want to edit safely."
**Explain simply:**
- View: no new data is stored; both names point to the same numbers. Slices like `array[:2]` are views.
- Copy: a separate block of data. `.copy()` and boolean or fancy indexing (`array[array > 5]`) give copies.
- Bug example: you take "the first two salaries", raise one by mistake, and the master salary array changes too.
- Views are fast and use less memory, which is why NumPy does it by default.
**Sample data:** salaries `[40000, 50000, 60000, 70000]`.
**Code (what you write in the interview):**
```python
import numpy as np

salaries = np.array([40000, 50000, 60000, 70000])

# A slice is a VIEW: it shares memory with the original
first_two = salaries[:2]
first_two[0] = 99999
print(salaries)

# .copy() makes an independent array
safe_two = salaries[:2].copy()
safe_two[0] = 1
print(salaries)
```
**Output:**
```text
[99999 50000 60000 70000]
[99999 50000 60000 70000]
```
**What it means:** Editing the slice changed the original (first line). Editing the `.copy()` left it alone (the second print is unchanged).
**Likely follow-ups:** 1) *How can I check?* `np.shares_memory(a, b)` or look at `b.base`. 2) *Is this the same in pandas?* Different rules; pandas 3 uses Copy-on-Write (editing a column taken from a DataFrame does not change the DataFrame), so do not assume NumPy behaviour carries over.
**Common mistakes:** Assuming a slice is a copy; calling `.copy()` everywhere "just in case" on huge arrays and wasting memory.

### Q22 ⭐⭐ 🟡 What do np.argmax and np.argmin return, and how would you find which employee has the highest salary?
**Asked at:** commonly asked (no company-specific report found); `argmax` axis behaviour appears in NumPy lists (TheLinuxCode 2026).
**What the interviewer is checking:** That you know these return a position, not the value, and that you can turn the position into a name.
**Say this in the interview:** "`np.argmax` returns the index of the largest value, `np.argmin` the index of the smallest. I use that index on the names array to find who it is."
**Explain simply:**
- `max` returns the biggest value; `argmax` returns where it sits (position counted from 0).
- The position works on any array that lines up with the salaries, like names or employee IDs.
- If two employees tie for highest, `argmax` returns only the first one.
- On a 2D array pass `axis` to get one answer per row or column.
**Sample data:** names and salaries as parallel arrays.
**Code (what you write in the interview):**
```python
import numpy as np

names = np.array(["Asha", "Ravi", "Meena", "Kiran"])
salaries = np.array([45000, 30000, 60000, 52000])

# Position of the highest and lowest salary
highest_position = np.argmax(salaries)
lowest_position = np.argmin(salaries)

# Use the position to look up the name
print(highest_position, names[highest_position])
print(lowest_position, names[lowest_position])
```
**Output:**
```text
2 Meena
1 Ravi
```
**What it means:** Meena (position 2) has the highest salary and Ravi (position 1) the lowest.
**Likely follow-ups:** 1) *What if there is a tie?* Only the first is returned; use `np.where(salaries == salaries.max())` to get all. 2) *What if there are NaNs?* `argmax` returns the position of the first NaN; use `np.nanargmax` to ignore it.
**Common mistakes:** Reporting the position as if it were the salary; forgetting positions start at 0.

### Q23 ⭐⭐ 🟡 How do you combine multiple conditions on a NumPy array (and, or, not)? Why does the Python keyword and give an error?
**Asked at:** commonly asked (no company-specific report found); combined boolean filters are a common NumPy and pandas live task.
**What the interviewer is checking:** That you use `&`, `|`, `~` with brackets, and can explain the error from `and`.
**Say this in the interview:** "For arrays I use `&` for and, `|` for or and `~` for not, and I put each condition in brackets. The word `and` expects one True or False, but an array has many, so NumPy raises an error."
**Explain simply:**
- Python `and` / `or` ask "is this whole object True or False?". An array of many values cannot answer that, so you get `ValueError: The truth value of an array with more than one element is ambiguous`.
- `&`, `|`, `~` work element by element, which is what we want.
- Brackets are required because Python works out `&` before it works out `>` and `<`, so the condition gets scrambled. Without brackets you get the same `ValueError`.
- `~` flips every True to False and back.
**Sample data:** salaries `[45000, 30000, 60000, 52000, 80000]`.
**Code (what you write in the interview):**
```python
import numpy as np

salaries = np.array([45000, 30000, 60000, 52000, 80000])

# AND: both conditions, each in its own brackets
mid_range = salaries[(salaries > 40000) & (salaries < 70000)]

# OR: either condition
extremes = salaries[(salaries < 35000) | (salaries > 75000)]

# NOT: flip a condition
not_high = salaries[~(salaries > 50000)]

print(mid_range)
print(extremes)
print(not_high)
```
**Output:**
```text
[45000 60000 52000]
[30000 80000]
[45000 30000]
```
**What it means:** The first line keeps salaries between 40,000 and 70,000; the second keeps the lowest and highest; the third keeps everyone not above 50,000.
**Likely follow-ups:** 1) *Same in pandas?* Yes, the same `&`, `|`, `~` with brackets. 2) *Is there a function version?* `np.logical_and`, `np.logical_or`, `np.logical_not`.
**Common mistakes:** Using `and`/`or`; leaving out brackets around each condition.

### Q24 ⭐ 🟢 How do you generate reproducible random numbers in NumPy (np.random.seed or default_rng)?
**Asked at:** commonly asked (no company-specific report found); seeds are listed in NumPy prep lists (TheLinuxCode 2026).
**What the interviewer is checking:** That you know a seed makes "random" numbers repeat, and which modern method to use.
**Say this in the interview:** "I create a generator with a fixed seed, `np.random.default_rng(42)`. The same seed gives the same numbers every run, so my results can be reproduced. The older way is `np.random.seed(42)`."
**Explain simply:**
- Computers make pseudo-random numbers: a formula that looks random but starts from a seed number.
- Same seed means same sequence, which matters when you share analysis or test code.
- `default_rng` is the recommended modern approach; `np.random.seed` sets a global state and still works (older style).
- Outputs depend on the NumPy version's generator, so only the seed and method are stable for your own environment.
**Code (what you write in the interview):**
```python
import numpy as np

# A generator with a fixed seed gives the same numbers every run
rng = np.random.default_rng(42)

random_numbers = rng.integers(1, 100, size=5)

print(random_numbers)
```
**Output:**
```text
[ 9 77 65 44 43]
```
**What it means:** Five whole numbers between 1 and 99. Running it again with seed 42 gives these same five.
**Likely follow-ups:** 1) *Does the seed value matter?* No, any whole number works; 42 is a habit. 2) *Is a seed good for security?* No, never use it for passwords or tokens.
**Common mistakes:** Forgetting that `integers` excludes the upper limit; expecting the same numbers without setting the seed.

### Q25 ⭐ 🟢 How do you join two NumPy arrays using np.concatenate, np.vstack and np.hstack?
**Asked at:** commonly asked (no company-specific report found); array joining is a basic NumPy topic.
**What the interviewer is checking:** That you know which function builds a longer array, new rows, or new columns.
**Say this in the interview:** "`np.concatenate` joins arrays end to end along an axis. `np.vstack` stacks them vertically as new rows; `np.hstack` places them side by side."
**Explain simply:**
- `concatenate` on 1D arrays gives one longer 1D array.
- `vstack` makes each input a row of a 2D array (arrays must have the same length).
- `hstack` on 1D arrays behaves like `concatenate`; on 2D arrays it adds columns.
- For 2D arrays, `np.concatenate([a, b], axis=0)` equals `vstack` and `axis=1` equals `hstack`.
**Sample data:** two teams' scores `[10, 20, 30]` and `[40, 50, 60]`.
**Code (what you write in the interview):**
```python
import numpy as np

team_a = np.array([10, 20, 30])
team_b = np.array([40, 50, 60])

# One long 1D array
joined = np.concatenate([team_a, team_b])

# Stack as rows (2 rows, 3 columns)
stacked_rows = np.vstack([team_a, team_b])

# Place side by side (one row, 6 columns)
side_by_side = np.hstack([team_a, team_b])

print(joined)
print(stacked_rows)
print(side_by_side)
```
**Output:**
```text
[10 20 30 40 50 60]
[[10 20 30]
 [40 50 60]]
[10 20 30 40 50 60]
```
**What it means:** `joined` and `side_by_side` are the same long list; `stacked_rows` is a small table with one team per row.
**Likely follow-ups:** 1) *What if the lengths differ in `vstack`?* It raises a `ValueError`. 2) *Which pandas tool is similar?* `pd.concat`.
**Common mistakes:** Passing the arrays separately instead of inside a list or tuple; joining arrays with mismatched shapes.

### Q26 ⭐ 🟡 What is the difference between flatten and ravel in NumPy?
**Asked at:** commonly asked (no company-specific report found); a classic NumPy copy-versus-view question.
**What the interviewer is checking:** That you know `flatten` always copies, while `ravel` returns a view when it can.
**Say this in the interview:** "Both turn a 2D array into 1D. `flatten` always gives a new copy. `ravel` returns a view when possible, so it is faster, but editing it can change the original."
**Explain simply:**
- Both read the array row by row and produce a single flat line.
- `flatten()`: safe, independent copy.
- `ravel()`: usually a view (shares memory), so it is quicker and uses less memory.
- Use `flatten` when you plan to edit the result; use `ravel` when you only read it.
**Sample data:** a 2 by 3 table of sales.
**Code (what you write in the interview):**
```python
import numpy as np

monthly_sales = np.array([[1, 2, 3],
                          [4, 5, 6]])

flat_copy = monthly_sales.flatten()
flat_view = monthly_sales.ravel()

# Change the flattened results and see what happens to the original
flat_copy[0] = 100
flat_view[1] = 200

print(flat_copy)
print(monthly_sales)
```
**Output:**
```text
[100   2   3   4   5   6]
[[  1 200   3]
 [  4   5   6]]
```
**What it means:** Changing the `flatten` result did not touch the original (the 1 is still there). Changing the `ravel` result changed the original (the 2 became 200).
**Likely follow-ups:** 1) *Does `ravel` always return a view?* No; for some non-contiguous arrays it has to copy. 2) *Is `reshape(-1)` the same?* It also flattens, with the same view-if-possible behaviour.
**Common mistakes:** Assuming both copy; editing a `ravel` result and corrupting the source data.

### Q27 ⭐ 🟡 How do you calculate a running total and the difference between consecutive values using np.cumsum and np.diff?
**Asked at:** commonly asked (no company-specific report found); running totals are a common analyst task.
**What the interviewer is checking:** That you know the two functions and what each output means, including that `diff` is one element shorter.
**Say this in the interview:** "`np.cumsum` gives the running total: each value is the sum of everything up to that point. `np.diff` gives the change from each value to the next, so the result has one fewer element."
**Explain simply:**
- Running total: after day 1 we have 3 hires, after day 2 we have 3 + 5 = 8, and so on.
- Difference: day 2 minus day 1, day 3 minus day 2, and so on. Five days give only four differences.
- Positive difference means growth from the previous day; negative means a fall.
- The last value of `cumsum` equals the overall sum.
**Sample data:** daily hires `[3, 5, 2, 4, 6]`.
**Code (what you write in the interview):**
```python
import numpy as np

daily_hires = np.array([3, 5, 2, 4, 6])

# Running total: hires so far
total_so_far = np.cumsum(daily_hires)

# Change from one day to the next
change_from_previous_day = np.diff(daily_hires)

print(total_so_far)
print(change_from_previous_day)
```
**Output:**
```text
[ 3  8 10 14 20]
[ 2 -3  2  2]
```
**What it means:** By day 5 we hired 20 people in total. Hiring went up by 2 on day 2, dropped by 3 on day 3, then rose again.
**Likely follow-ups:** 1) *Pandas equivalent?* `cumsum()` and `diff()` on a Series. 2) *Can `diff` work on a 2D array?* Yes, with `axis`.
**Common mistakes:** Expecting `diff` to have the same length as the input; confusing a running total with the daily values.

### Q28 ⭐ 🟡 How do you pick a random sample of 5 employee IDs from an array using NumPy?
**Asked at:** commonly asked (no company-specific report found); a gap-fill HR-flavoured task built on standard NumPy sampling.
**What the interviewer is checking:** That you know `choice` and the `replace=False` setting so nobody is picked twice.
**Say this in the interview:** "I use `rng.choice(employee_ids, size=5, replace=False)`. `replace=False` means each ID can be chosen only once, which is what you want for a sample of people."
**Explain simply:**
- Sampling without replacement: once an ID is picked it is out of the draw.
- Sampling with replacement (the default) can pick the same ID twice.
- Setting a seed on the generator makes the sample repeatable, useful for audits.
- The sample size cannot be larger than the array when `replace=False`.
**Sample data:** employee IDs 101 to 120.
**Code (what you write in the interview):**
```python
import numpy as np

employee_ids = np.arange(101, 121)

rng = np.random.default_rng(7)

# replace=False means nobody is picked twice
sample_ids = rng.choice(employee_ids, size=5, replace=False)

print(sample_ids)
```
**Output:**
```text
[111 113 116 112 118]
```
**What it means:** These five IDs are the random sample. With seed 7 the same five come out each run; without a seed they change each time.
**Likely follow-ups:** 1) *Pandas equivalent?* `df.sample(n=5)`. 2) *How do I sample 10%?* Set `size` to `int(len(employee_ids) * 0.1)`.
**Common mistakes:** Forgetting `replace=False` and getting duplicates; asking for more items than exist.

### Q29 ⭐ 🟡 What is the difference between np.nan, None and 0 when representing missing data?
**Asked at:** commonly asked (no company-specific report found); a gap-fill concept question from standard practice.
**What the interviewer is checking:** That you understand each one behaves differently in calculations and never use 0 to mean "missing".
**Say this in the interview:** "`np.nan` is a float placeholder that keeps arrays numeric and can be skipped with `nanmean`. `None` is a Python object that makes the array slow, general-purpose and breaks maths. `0` is a real number, so it drags averages down."
**Explain simply:**
- `np.nan`: "unknown number". The array stays `float64`; use `np.isnan` and the `nan` functions.
- `None`: Python's "nothing". Putting it in an array turns the whole array into `object` type (a slow, catch-all type where each value is a separate Python item); `mean()` then fails with a `TypeError`.
- `0`: a real value (for example, zero hours worked). It is counted in averages, which is wrong if the value was simply not recorded.
- `np.nan == np.nan` is `False`, so you cannot test for it with `==`.
**Sample data:** salaries `[40000, ?, 60000]` where `?` is stored three different ways.
**Code (what you write in the interview):**
```python
import numpy as np

# np.nan keeps the array numeric
with_nan = np.array([40000, np.nan, 60000])
print(with_nan.dtype, np.nanmean(with_nan))

# None turns the array into slow, general "object" type
with_none = np.array([40000, None, 60000])
print(with_none.dtype)

# 0 is a real number and drags the average down
with_zero = np.array([40000, 0, 60000])
print(with_zero.mean())

print(np.nan == np.nan)
```
**Output:**
```text
float64 50000.0
object
33333.333333333336
False
```
**What it means:** With `nan` the average of the known salaries is 50,000. With 0 it falls to about 33,333, which is wrong. With `None` the dtype is `object`, and calling `.mean()` fails (`TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'`).
**Likely follow-ups:** 1) *How does pandas show missing data?* As `NaN` (and `NA` / `None` in some types); `isna()` handles all of them. 2) *Does NaN work in integer arrays?* No, NumPy integer arrays cannot hold NaN; the array becomes float.
**Common mistakes:** Filling missing values with 0 and reporting a wrong average; testing for NaN with `==`.

### Q30 ⭐ 🔴 Write code to calculate a 3-day moving average of an array using NumPy only.
**Asked at:** commonly asked (no company-specific report found); a rolling mean task appears in DataCamp's NumPy question list.
**What the interviewer is checking:** That you can build a rolling calculation without pandas, and know why the result is shorter than the input.
**Say this in the interview:** "A 3-day moving average is the average of each window of 3 consecutive days. In NumPy I slide a window of weights one third each along the data with `np.convolve`, using `mode='valid'` so I only keep full windows."
**Explain simply:**
- Moving (rolling) average: smooth out day-to-day noise by averaging the latest 3 days.
- `np.ones(3) / 3` makes three weights of one third each; multiplying and adding is the same as averaging.
- `mode="valid"` keeps only positions where all 3 days exist, so 6 days give 4 averages (length n minus 2).
- The first average belongs to day 3 (it needs days 1 to 3).
**Sample data:** daily hires `[3, 5, 2, 4, 6, 9]`.
**Code (what you write in the interview):**
```python
import numpy as np

daily_hires = np.array([3, 5, 2, 4, 6, 9])

# Each window of 3 days gets weight 1/3, then we slide it along
window = np.ones(3) / 3
moving_average = np.convolve(daily_hires, window, mode="valid")

print(moving_average)
```
**Output:**
```text
[3.33333333 3.66666667 4.         6.33333333]
```
**What it means:** Days 1 to 3 average 3.33, days 2 to 4 average 3.67, and so on. The jump to 6.33 shows hiring picking up at the end.
**Alternative:** A plain loop that takes each 3-day slice and averages it, easier to explain line by line (gives the same four values; it reuses `daily_hires` from above):
```python
moving_average = []
for start in range(len(daily_hires) - 2):
    three_days = daily_hires[start:start + 3]
    moving_average.append(three_days.mean())
```
**Likely follow-ups:** 1) *Pandas version?* `pd.Series(daily_hires).rolling(3).mean()`, which returns NaN for the first two days instead of dropping them. 2) *Why is the output shorter?* The first two days do not have 3 days of history.
**Common mistakes:** Forgetting `mode="valid"` (the edges then mix in zeros and look wrong); using a window that does not sum to 1 (the values would not be averages).

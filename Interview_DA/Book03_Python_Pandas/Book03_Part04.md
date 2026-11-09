# Book 3 — Python & pandas for Analysts | Part 4: pandas: read, select, filter, sort 🟢

**Target:** 70 questions | **Actual:** 75 questions
**Scope:** loading data with pandas, inspecting it, selecting columns and rows (loc/iloc), filtering, sorting and basic column creation, plus common errors; groupby, merge, cleaning and dates are in other parts.

### Q1 ⭐⭐⭐ 🟢 What is pandas, and what is the difference between a Series and a DataFrame?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 How do you read a CSV file into a pandas DataFrame, and how do you read an Excel sheet?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Write code to load an employee CSV file and look at the first 5 and last 5 rows.
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 How do you check the number of rows and columns of a DataFrame?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 How do you quickly see column names, data types and non-null counts of a DataFrame using info()?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 How do you select a single column and multiple columns from a DataFrame?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 What is the difference between loc and iloc in pandas?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 Write code to filter an employee DataFrame to show only employees from the Sales department.
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟢 Write code to sort an employee DataFrame by salary from highest to lowest.
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟢 How do you add a new column to a DataFrame, for example annual salary from monthly salary?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟢 How do you check the data type of each column, and what does the 'object' dtype mean?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟢 Write code to filter rows where the department is Sales, HR or Finance using isin().
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Write code to filter employees with salary above 50,000 who are also in the Finance department. Why do you need brackets around each condition?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 What is the difference between using 'and' and '&' when filtering a DataFrame, and what error do you get if you use 'and'?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Write code to sort a DataFrame by department (A to Z) and then by salary (high to low) within each department.
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 What does SettingWithCopyWarning mean, and how do you avoid it?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 You get KeyError when selecting a column that clearly exists in your CSV. What are the common causes and how do you fix them?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 How do you rename columns in a DataFrame?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 How do you drop a column or a row from a DataFrame, and what does axis mean?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 How do you list the unique values of a column and count how many unique values it has?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 What is the difference between df['col'] and df[['col']]?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 What is the difference between a view and a copy of a DataFrame, and how do you make an independent copy with copy()?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 Write code to show the top 5 highest-paid employees.
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟢 How do you select the first 10 rows and the first 3 columns using iloc?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟢 Write code to filter employees whose name starts with 'A' using str.startswith().
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟢 How do you filter rows where a column is between two values, for example salary between 30,000 and 60,000?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟢 How do you read only selected columns from a large CSV using usecols?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟢 How do you save a DataFrame to a CSV file without writing the index, and how do you write it to Excel?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟢 What is the difference between head(), sample() and tail(), and how do you pick 5 random rows?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟢 How do you find the maximum salary and the row (employee) who earns it?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟢 How do you count the rows that satisfy a condition, for example how many employees have left the company?
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟢 How do you check for duplicate column names or confirm the DataFrame shape after each filter?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 What is the index of a DataFrame, and how do you set a column such as employee ID as the index?
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you reset the index after filtering or sorting, and what does drop=True do?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 What is the difference between nlargest() and sort_values().head(), and when would you use each?
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 How do you select rows by label and specific columns using loc, for example employees 101 to 105 and only name and salary?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 Why does loc slicing include the end label while iloc slicing excludes the end position?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 How do you filter rows where a text column contains a word, for example job title containing 'Manager', ignoring upper or lower case?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 How do you filter rows that are NOT in a list of values, for example all departments except HR and Admin?
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 How do you filter rows with missing values in a column, for example employees with no manager ID, using isna()?
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 What is the query() method in pandas, and how does it compare with boolean indexing?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 How do you use a Python variable inside query()?
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 How do you read only the first 1,000 rows of a large CSV file, and why would you do it?
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 What are the common parameters of read_csv() that you use for messy files (sep, header, skiprows, encoding, na_values)?
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 How do you read a specific sheet of an Excel workbook into pandas, and which extra library is needed?
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 What does the error UnicodeDecodeError mean when reading a CSV, and how do you fix it?
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟡 What does FileNotFoundError mean when calling read_csv(), and how do you check the file path and current working directory?
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟡 How do you create a new column using a condition, for example 'High' if salary is above 60,000 else 'Low', using np.where()?
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🟡 How do you sort a DataFrame by index, and what is the difference between sort_values() and sort_index()?
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🟡 What does the inplace parameter do, and why is it better to assign the result back instead?
<!-- ANSWER_PENDING -->

### Q51 ⭐⭐ 🟡 What is the difference between idxmax() and max()?
<!-- ANSWER_PENDING -->

### Q52 ⭐⭐ 🟡 How do you create a DataFrame from a Python dictionary and from a list of lists?
<!-- ANSWER_PENDING -->

### Q53 ⭐⭐ 🟡 How do you select all columns of a particular data type, for example only numeric columns, using select_dtypes()?
<!-- ANSWER_PENDING -->

### Q54 ⭐⭐ 🟡 Why does a column of numbers read as object dtype from a CSV, and how do you spot it?
<!-- ANSWER_PENDING -->

### Q55 ⭐⭐ 🟡 How do you reorder columns or move one column to the front of a DataFrame?
<!-- ANSWER_PENDING -->

### Q56 ⭐⭐ 🟡 How do you filter a DataFrame using multiple conditions with OR, for example employees in Sales or with salary above 80,000?
<!-- ANSWER_PENDING -->

### Q57 ⭐⭐ 🔴 What is chained indexing, for example df[df['dept']=='Sales']['salary'] = 0, and why does it fail to update the original DataFrame?
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🟡 How do you update the values of selected rows, for example give a 10% raise to employees in the Sales department, using loc?
<!-- ANSWER_PENDING -->

### Q59 ⭐ 🟡 How do you set a column as the index and then select a row by that label, such as employee ID 105?
<!-- ANSWER_PENDING -->

### Q60 ⭐ 🟡 What is the difference between at/iat and loc/iloc?
<!-- ANSWER_PENDING -->

### Q61 ⭐ 🟡 How do you select every second row of a DataFrame using slicing?
<!-- ANSWER_PENDING -->

### Q62 ⭐ 🟡 How do you sort a DataFrame by a text column with a custom order, for example Low, Medium, High, using a categorical type?
<!-- ANSWER_PENDING -->

### Q63 ⭐ 🟡 How do you keep sorting stable and place missing values at the top or bottom using na_position?
<!-- ANSWER_PENDING -->

### Q64 ⭐ 🟡 How do you read a CSV with a custom delimiter such as pipe or semicolon?
<!-- ANSWER_PENDING -->

### Q65 ⭐ 🟡 How do you rename the index or axis labels and set a column name for the index?
<!-- ANSWER_PENDING -->

### Q66 ⭐ 🟡 How do you filter columns by name pattern, for example all columns starting with 'Q1_' using filter() or str.startswith()?
<!-- ANSWER_PENDING -->

### Q67 ⭐ 🟡 How do you use where() and mask() to replace values by a condition without changing the shape of the DataFrame?
<!-- ANSWER_PENDING -->

### Q68 ⭐ 🟡 How do you transpose a DataFrame, and when is it useful?
<!-- ANSWER_PENDING -->

### Q69 ⭐ 🟡 How do you display all columns or more rows when a DataFrame is truncated in the notebook?
<!-- ANSWER_PENDING -->

### Q70 ⭐ 🟡 How do you check the memory used by a DataFrame, and how can the category dtype reduce it?
<!-- ANSWER_PENDING -->

### Q71 ⭐ 🟡 How do you read data directly from a URL or from an in-memory text string with read_csv?
<!-- ANSWER_PENDING -->

### Q72 ⭐ 🔴 What is a MultiIndex, and how do you select rows from one?
<!-- ANSWER_PENDING -->

### Q73 ⭐ 🔴 How do you read a large CSV file in chunks, and when is it needed?
<!-- ANSWER_PENDING -->

### Q74 ⭐ 🔴 How do you select the rows with the lowest salary in each department without groupby, using sort_values and iloc?
<!-- ANSWER_PENDING -->

### Q75 ⭐ 🔴 What changed with Copy-on-Write in pandas 3.0, and what does it mean for SettingWithCopyWarning?
<!-- ANSWER_PENDING -->

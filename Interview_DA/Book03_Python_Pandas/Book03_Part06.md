# Book 3 — Python & pandas for Analysts | Part 6: Data Cleaning: Missing Values, Duplicates, Types, Outliers 🟡

**Target:** 60 questions | **Actual:** 63 questions
**Scope:** pandas data cleaning for analysts: missing values, duplicates, data types, text and date fixes, outliers, SettingWithCopyWarning and common errors.

### Q1 ⭐⭐⭐ 🟢 How do you check for missing values in a pandas DataFrame and count them per column?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is the difference between isna() and isnull() in pandas?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 How do you remove duplicate rows in pandas?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 How do you find duplicate rows in a DataFrame without deleting them?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What does df.info() tell you, and why is it usually the first step in data cleaning?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 How do you check the data type of each column, and how do you change a column's type with astype()?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 What is the difference between dropna() and fillna(), and when would you use each?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 How do you handle missing values in a salary column: when do you fill with the mean, the median or a constant, and how do you do it in pandas?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 How does drop_duplicates() decide which row to keep, and how do you use the subset and keep arguments?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 A column holding numbers is stored as text because of values like 'N/A' or '12,500'. How do you convert it to numeric safely using pd.to_numeric()?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 How do you detect outliers in a salary column using the IQR method in pandas?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 You have an employee table with repeated Employee IDs. Write code to keep only the most recent record per employee.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 What are the steps you follow to clean a messy dataset in pandas before analysis?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 What is the SettingWithCopyWarning, why does it appear, and how do you fix it?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🔴 How do you decide whether to drop, fill or flag missing values, and how do you explain the choice to a business stakeholder?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 What is the difference between NaN, None and an empty string in pandas?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 How do you drop rows where a specific column is missing, using dropna(subset=...)?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 How do you fill missing values with the previous or next value using ffill() and bfill()?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 How do you rename columns in a DataFrame, and why clean column names (spaces, capitals) at the start?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 How do you remove leading and trailing spaces from a text column in pandas?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 How do you make text consistent in pandas, for example turning 'hr', 'HR ' and 'Hr' into 'HR'?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 How do you change a text column to datetime using pd.to_datetime()?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 How do you replace specific values in a column, for example 'Male' and 'M' to 'M', using replace() or map()?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟢 What is the difference between astype(int) and pd.to_numeric(), and what happens if the column has missing values?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟢 How do you count unique values in a column, and how do you check for inconsistent spellings with value_counts()?
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟢 How do you drop columns that are not needed, or columns with too many missing values?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟢 What does the errors='coerce' argument do in to_numeric() and to_datetime()?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How do you calculate the percentage of missing values in each column, and how do you list columns with more than 30% missing?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 How do you fill missing values within each group, for example filling a missing salary with the department median using groupby and transform()?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 How do you use the thresh and how arguments of dropna()?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 How do you find all rows that are duplicates on Employee ID and month, including the first occurrence (keep=False)?
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you clean a currency column like 'Rs. 45,000' and convert it to a number?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 How do you detect outliers using the z-score in pandas, and when is the IQR method better?
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you handle outliers: remove, cap (winsorize) or keep? Show how to cap values at the 1st and 99th percentiles with clip().
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 How do you split a 'Full Name' column into first and last name using str.split()?
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 How do you filter rows with invalid values, for example ages below 18 or above 70, or negative salaries?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 Why does df[df['salary'] > 0]['bonus'] = 0 not work reliably, and what is the correct way using loc?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 How do you convert a column to the category dtype, and why is it useful?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 What is the difference between inplace=True and assigning the result back, and why do many people avoid inplace?
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 How do you create a flag column marking missing values, so you keep that information after filling?
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 How do you standardise inconsistent department names such as 'Human Resources', 'HR' and 'H.R.' into one value?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 A column of Yes/No answers contains blanks and mixed case. How do you clean it and convert it to True/False?
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 How do you find rows with an invalid email or phone number using str.contains() or a regular expression?
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 Attendance data has a missing check-out time on some days. How would you handle it in pandas?
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🔴 You merge two files and the row count goes up unexpectedly. How do you check for duplicate keys and clean them?
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🟢 How do you reset the index after removing rows, and why does the index have gaps?
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟢 How do you convert a column of 'Yes'/'No' to 1/0 in pandas?
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟢 What does the nunique() method do, and how is it different from unique()?
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🟡 How do you replace placeholder values like -1, 999 or 'Unknown' with NaN before cleaning?
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🟡 How do you fill missing values using interpolate(), and when is it appropriate?
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🟡 How do you find near-duplicate company names such as 'Infosys Ltd' and 'Infosys Limited' in pandas?
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🟡 How do you use select_dtypes() to clean numeric and text columns separately?
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🟡 How do you check whether a column's values are consistent with another column, for example exit date earlier than join date?
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🟡 What is Copy-on-Write in newer pandas versions, and how does it change the SettingWithCopyWarning problem?
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🟡 How do you apply a custom cleaning function to a column using apply(), and why are vectorised string methods usually faster?
<!-- ANSWER_PENDING -->

### Q56 ⭐ 🟡 How do you remove outliers separately within each group, such as salary outliers per job grade?
<!-- ANSWER_PENDING -->

### Q57 ⭐ 🟡 How do you reduce memory by downcasting numeric columns with to_numeric(downcast=...)?
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🟡 How do you deal with a column that mixes dates in different formats, such as '05-11-2025' and '2025/11/05'?
<!-- ANSWER_PENDING -->

### Q59 ⭐ 🟡 Why can astype(int) fail with 'Cannot convert non-finite values (NA or inf) to integer', and what is the fix (for example the nullable Int64 type)?
<!-- ANSWER_PENDING -->

### Q60 ⭐ 🔴 You get a 5-lakh-row HR file with inconsistent columns, duplicates and blanks. Walk me through your cleaning plan and how you would document every change.
<!-- ANSWER_PENDING -->

### Q61 ⭐ 🔴 How do you build a reusable data-cleaning function or pipeline in pandas using pipe()?
<!-- ANSWER_PENDING -->

### Q62 ⭐ 🔴 How do you validate the data after cleaning, using assertions and simple quality checks?
<!-- ANSWER_PENDING -->

### Q63 ⭐ 🔴 How do you detect outliers in a column that is highly skewed, such as salary, and why might a log transform help?
<!-- ANSWER_PENDING -->

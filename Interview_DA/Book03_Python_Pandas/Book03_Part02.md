# Book 3 — Python & pandas for Analysts | Part 2: Strings, File Handling, Error Handling 🟢

**Target:** 45 questions | **Actual:** 50 questions
**Scope:** Python string methods and formatting, regex basics, reading and writing text/CSV/JSON files, and try/except error handling for analyst scripts.

### Q1 ⭐⭐⭐ 🟢 What does `with open(...) as f:` do, and why is it preferred over calling open() and close() yourself?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is the difference between the file modes 'r', 'w', 'a' and 'r+', and which one can silently destroy existing data?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Explain try, except, else and finally in Python with a small example.
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Write code to open a CSV file in plain Python (no pandas) and print its first 5 lines.
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 A name column contains '  rAVI   kumar '. Write code to turn it into 'Ravi Kumar'.
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 What do split() and join() do? Split 'Asha,Sales,45000' into parts and rebuild it with '|' as the separator.
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 What does it mean that Python strings are immutable, and why does name.strip() not change name?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 How do you use an f-string to print 'Ravi earns Rs 45,000.50 in Sales' from variables, with a thousands separator and two decimals?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟢 How do you handle a FileNotFoundError when a monthly attendance file is missing?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟢 What does ValueError: invalid literal for int() mean, and how do you avoid your script crashing on it?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟢 How do you take the first 3 characters, and the numeric part, of an employee code such as 'HYD-1045' using slicing or split?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Write code to convert salary strings like 'Rs. 45,000' into integers, skipping bad values such as 'N/A' with try/except.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Read a CSV with csv.DictReader and compute the total salary per department using a dictionary.
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Why should you catch specific exceptions instead of a bare `except:`, and what can go wrong with a bare except?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 What is the difference between upper(), lower(), title() and capitalize()?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 What do startswith() and endswith() do, and how would you filter employee IDs that start with 'HYD'?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 What is the difference between find() and index() when the substring is not present?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 What is the difference between read(), readline() and readlines()?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 Write code to save a list of employee names to a text file, one name per line.
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 How do you check whether a string is only digits, only letters, or letters and digits (isdigit, isalpha, isalnum)? Validate that a mobile number is 10 digits.
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 What is the difference between f-strings, str.format() and the % operator for formatting text?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 How do you pad employee ID 45 to '00045' using zfill() or format specifiers?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 How do you split the full name 'Ravi Kumar Singh' into first name and last name?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟢 How do you read a Python traceback, and where do you look first?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟢 What is the difference between a syntax error and an exception? Give an example of each.
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟢 How do you check whether a file exists before opening it, using os.path or pathlib?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟢 What is a raw string (r'...') and why do you need it for Windows file paths such as 'C:\data\new_hires.csv'?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟢 How do you raise your own exception, for example rejecting a negative salary with raise ValueError?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Write code to extract all email addresses from a block of text using re.findall.
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 What is the difference between re.match, re.search, re.findall and re.sub?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Write code to standardise messy phone numbers such as '+91 98765-43210' by removing non-digits and keeping the last 10 digits.
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Write code to read a pipe-delimited attendance log with lines like 'E101|2024-08-01|P' and count present days per employee.
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 How do you read and write JSON files with json.load and json.dump?
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 When do you use csv.reader, csv.DictReader and pandas.read_csv?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 Write a function that returns the attrition rate but returns None instead of crashing when headcount is 0 (ZeroDivisionError).
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 Write code to process a file row by row, collect the bad rows in a separate file, and keep going when a row fails.
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 When does the else block of try/except run, and does finally still run if the try block has a return statement?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 What does newline='' do when writing a CSV, and why do you sometimes get blank lines between rows?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 A column holds 'Sales - Hyderabad'. Write code to split it into department and city and strip the extra spaces.
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 Write code to remove duplicate employee IDs from a text file while keeping the original order.
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 Write code to list all .csv files in a folder using os.listdir or glob.
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🟢 What are escape characters such as \n and \t, and when do you use triple-quoted strings?
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🟢 How do you compare two strings ignoring case, and what is the difference between lower() and casefold()?
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🟢 How do you check whether a string is empty or contains only spaces?
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🟡 What is the difference between greedy and non-greedy regex matching, for example .* and .*?
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🟡 Write a regex with capture groups to pull the currency and amount out of 'INR 45000'.
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟡 How do you read a very large text file without loading it all into memory?
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 How do you define and use a custom exception class, and when is it worth it in an analyst script?
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🟡 When do you use assert, and how does it differ from raising an exception?
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 What is a context manager, and how would you write one with __enter__ and __exit__ (or contextlib)?
<!-- ANSWER_PENDING -->

# Book 3 — Python & pandas for Analysts | Part 2: Strings, File Handling, Error Handling 🟢

**Target:** 45 questions | **Actual:** 50 questions
**Scope:** Python string methods and formatting, regex basics, reading and writing text/CSV/JSON files, and try/except error handling for analyst scripts.

### Q1 ⭐⭐⭐ 🟢 What does `with open(...) as f:` do, and why is it preferred over calling open() and close() yourself?
**Asked at:** commonly asked (no company-specific report found); file handling appears as a standard theme in Python prep question banks (ClimbTheLadder, Packt).
**What the interviewer is checking:** Whether you know files must be closed, and that `with` does it for you even when something fails.
**Say this in the interview:** "`with open()` opens the file and automatically closes it when the block ends, even if an error happens inside. With plain open() and close(), an error before close() leaves the file open."
**Explain simply:**
- `open()` gives you a file object (here called `f`) that you read from or write to.
- A file left open can lock the file (a problem on Windows), lose unsaved writes, or leak resources.
- `with` is a "context manager": a block that sets something up and always cleans up at the end.
- You do not need to remember `f.close()`, so there is nothing to forget.
**Sample data:** `attendance.txt` with 3 lines (employee, date, P for present or A for absent).
**Code (what you write in the interview):**
```python
# open the file; "with" closes it for us when the block ends
with open("attendance.txt") as f:
    for line in f:
        print(line.strip())
```
**Output:**
```text
E101,2024-08-01,P
E102,2024-08-01,A
E103,2024-08-01,P
```
**What it means:** The file was read line by line and closed automatically afterwards.
**Alternative:** `f = open("attendance.txt")` ... `f.close()`. It works, but if an error happens in between, close() never runs. A `try/finally` would fix that, but `with` is shorter.
**Likely follow-ups:** 1) *Is the file closed after the block?* Yes, `f.closed` is True. 2) *Can you open two files in one `with`?* Yes, separate them with a comma.
**Common mistakes:** Reading from `f` after the `with` block (error: I/O operation on closed file); forgetting `.strip()` so each line carries a hidden newline.

### Q2 ⭐⭐⭐ 🟢 What is the difference between the file modes 'r', 'w', 'a' and 'r+', and which one can silently destroy existing data?
**Asked at:** commonly asked (no company-specific report found); modes are a standard item in file-handling question banks (AshokIT notes, ClimbTheLadder).
**What the interviewer is checking:** That you know `'w'` wipes the file and that you are careful with it.
**Say this in the interview:** "'r' reads, 'w' writes from scratch and erases whatever was there, 'a' adds to the end, 'r+' reads and writes without erasing. 'w' is the dangerous one because it destroys existing data with no warning."
**Explain simply:**
- `'r'` (read, the default): the file must exist, otherwise FileNotFoundError.
- `'w'` (write): creates the file if missing; if it exists, it is emptied the moment you open it, even before you write anything.
- `'a'` (append): creates the file if missing; new text goes at the end, old content stays.
- `'r+'` (read and write): the file must exist; nothing is erased, but writing overwrites from the current position.
**Sample data:** `names.txt` already holds three lines: Old1, Old2, Old3.
**Code (what you write in the interview):**
```python
with open("names.txt", "a") as f:   # "a" adds to the end, old lines stay
    f.write("Ravi\n")

with open("names.txt", "w") as f:   # "w" wipes the file first
    f.write("Asha\n")

with open("names.txt") as f:
    print(f.read())
```
**Output:**
```text
Asha

```
**What it means:** The append kept the old names, but the later `'w'` threw away all four lines (Old1 to Old3 and Ravi). Only Asha is left, and Python never warned us. (The blank line is just the newline after Asha.)
**Likely follow-ups:** 1) *How do you avoid wiping a file by accident?* Use mode `'x'` (create only, errors if the file exists) or check first that it exists. 2) *Where does `'a'` write?* Always at the end.
**Common mistakes:** Using `'w'` when you meant to add rows to a log; forgetting `\n` so appended lines join together.

### Q3 ⭐⭐⭐ 🟢 Explain try, except, else and finally in Python with a small example.
**Asked at:** commonly asked; try/except/finally is listed as a technical-stage question on practice platforms (Dataford) and was reported once on Glassdoor (Securin), not a data-analyst-specific report.
**What the interviewer is checking:** That you know the order of the four blocks and when each runs.
**Say this in the interview:** "`try` holds the risky code. `except` runs only if it fails. `else` runs only if it did not fail. `finally` runs no matter what, which is where I put clean-up."
**Explain simply:**
- `try`: code that might raise an error (an "exception" is Python's word for a runtime error).
- `except ValueError`: what to do if that specific error happens; the script keeps going instead of crashing.
- `else`: runs only when `try` finished with no error, so the success steps stay out of the risky block.
- `finally`: always runs, error or not (closing a connection, printing "done").
**Code (what you write in the interview):**
```python
try:
    salary = int("abc")          # risky step: "abc" is not a number
except ValueError:
    print("Salary is not a number")
else:
    print("Converted fine:", salary)   # only if no error
finally:
    print("Done")                # always runs
```
**Output:**
```text
Salary is not a number
Done
```
**What it means:** The error was caught, `else` was skipped, and `finally` still ran. With `int("45000")` the output is `Converted fine: 45000` then `Done` (I ran that too).
**Likely follow-ups:** 1) *Can you have try without except?* Yes, with `finally` only. 2) *Can you have several except blocks?* Yes, one per error type; the first match wins.
**Common mistakes:** Putting too much code inside `try`; thinking `else` runs after an error (it does the opposite).

### Q4 ⭐⭐⭐ 🟢 Write code to open a CSV file in plain Python (no pandas) and print its first 5 lines.
**Asked at:** commonly asked (no company-specific report found); a basic live-coding task in file-handling banks.
**What the interviewer is checking:** That you can read a file without pandas and stop after 5 lines.
**Say this in the interview:** "I open the file with `with`, loop over the lines, count them, and stop at 5. A file object reads one line at a time, so this works even for a huge file."
**Explain simply:**
- Looping over a file gives one line at a time, including the hidden newline at the end, so I use `strip()`.
- `enumerate` gives a counter (0, 1, 2...) next to each line.
- The header row counts as line 1, so you see the header plus 4 data rows.
**Sample data:** `employees.csv` with a header and 7 employee rows.
**Code (what you write in the interview):**
```python
with open("employees.csv") as f:
    for line_number, line in enumerate(f):
        if line_number == 5:      # stop after 5 lines
            break
        print(line.strip())
```
**Output:**
```text
emp_id,name,department,salary
E1,Asha,Sales,45000
E2,Ravi,IT,60000
E3,Meena,Sales,52000
E4,John,HR,40000
```
**What it means:** Five lines were printed: the header and the first 4 employees.
**Alternative:** `from itertools import islice` then `for line in islice(f, 5): print(line.strip())`. Same output, shorter.
**Likely follow-ups:** 1) *Why not `f.readlines()[:5]`?* It loads the whole file into memory first. 2) *What if the file has fewer than 5 lines?* The loop simply ends early.
**Common mistakes:** Printing without `strip()` (blank line after every row); forgetting `break` so the whole file prints.

### Q5 ⭐⭐⭐ 🟢 A name column contains '  rAVI   kumar '. Write code to turn it into 'Ravi Kumar'.
**Asked at:** commonly asked (no company-specific report found); text cleaning is a typical first Python task for analysts.
**What the interviewer is checking:** That you handle both the extra spaces (outside and in the middle) and the capitals.
**Say this in the interview:** "`split()` with no argument breaks on any run of spaces and drops the extras, `join` puts the words back with one space, and `title()` fixes the capitals."
**Explain simply:**
- `strip()` only removes spaces at the two ends, so it would leave the gap in the middle.
- `split()` with no argument treats any amount of whitespace as one separator and ignores the ends.
- `" ".join(words)` glues the list back using one space.
- `title()` makes the first letter of each word capital and the rest small.
**Code (what you write in the interview):**
```python
name = "  rAVI   kumar "

# split() drops extra spaces, join() puts back single spaces, title() fixes capitals
clean_name = " ".join(name.split()).title()
print(clean_name)
```
**Output:**
```text
Ravi Kumar
```
**What it means:** The messy text is now clean and consistent, ready for grouping or matching.
**Likely follow-ups:** 1) *Does `title()` always work?* No: `"o'neil mcdonald".title()` gives `O'Neil Mcdonald` (I ran it), so names with apostrophes or prefixes need care. 2) *How would you do it in pandas?* `df["name"].str.split().str.join(" ").str.title()`, covered in the pandas parts.
**Common mistakes:** Using only `strip()`; using `split(" ")`, which keeps empty strings for repeated spaces.

### Q6 ⭐⭐⭐ 🟢 What do split() and join() do? Split 'Asha,Sales,45000' into parts and rebuild it with '|' as the separator.
**Asked at:** commonly asked (no company-specific report found); string manipulation is reported in Python rounds at analytics firms such as Tiger Analytics (Glassdoor search summaries, details not read).
**What the interviewer is checking:** That you know they are opposites and that `join` is called on the separator.
**Say this in the interview:** "`split` breaks one text into a list at a separator. `join` does the reverse: it glues a list of text pieces into one string using a separator."
**Explain simply:**
- `"a,b".split(",")` gives `["a", "b"]`: text to list.
- `"|".join(parts)` gives `"a|b"`: list to text. The separator comes first, which surprises beginners.
- `join` only accepts text pieces, so numbers must be converted with `str()` first.
**Code (what you write in the interview):**
```python
record = "Asha,Sales,45000"

parts = record.split(",")       # text -> list
print(parts)

rebuilt = "|".join(parts)       # list -> text
print(rebuilt)
```
**Output:**
```text
['Asha', 'Sales', '45000']
Asha|Sales|45000
```
**What it means:** One comma-separated record became three fields, then one pipe-separated record.
**Likely follow-ups:** 1) *What type is `parts[2]`?* A string `'45000'`, not a number. 2) *What does `"a,b,c".split(",", 1)` do?* Splits only once: `['a', 'b,c']`.
**Common mistakes:** Writing `parts.join("|")` (join belongs to the string); joining a list that contains integers (TypeError).

### Q7 ⭐⭐⭐ 🟢 What does it mean that Python strings are immutable, and why does name.strip() not change name?
**Asked at:** commonly asked (no company-specific report found); immutability is a standard string-basics question (Fiveable, dev.to).
**What the interviewer is checking:** That you know string methods return a new string and you must save it.
**Say this in the interview:** "Immutable means a string cannot be changed after it is created. Methods like `strip()` build a new string and return it, so I must assign it back, for example `name = name.strip()`."
**Explain simply:**
- Immutable: once created, the text itself never changes; you can only create a new text.
- `name.strip()` returns a cleaned copy; the original `name` is untouched.
- If you do not store the copy, it is thrown away.
- Lists are the opposite: they are mutable and can change in place. Strings and tuples cannot.
**Code (what you write in the interview):**
```python
name = "  Ravi "

name.strip()                    # result thrown away
print(repr(name))

name = name.strip()             # keep the result
print(repr(name))
```
**Output:**
```text
'  Ravi '
'Ravi'
```
**What it means:** The first call changed nothing visible; only after assigning the result did `name` become clean. (`repr` shows the quotes so you can see the spaces.)
**Likely follow-ups:** 1) *What happens on `name[0] = "r"`?* TypeError: strings do not support item assignment. 2) *Why are strings immutable?* Safety and speed; they can be reused and used as dictionary keys.
**Common mistakes:** Calling `.strip()` or `.replace()` and expecting the variable to change.

### Q8 ⭐⭐⭐ 🟢 How do you use an f-string to print 'Ravi earns Rs 45,000.50 in Sales' from variables, with a thousands separator and two decimals?
**Asked at:** commonly asked (no company-specific report found); formatting is a standard string-basics task.
**What the interviewer is checking:** That you know the format spec `:,.2f`.
**Say this in the interview:** "I put an `f` before the quotes, use curly braces for the variables, and after a colon add `,.2f`: the comma is the thousands separator and `.2f` means two decimal places."
**Explain simply:**
- An f-string is a string starting with `f` where `{name}` is replaced by the variable's value.
- After the colon in the braces you write the display format.
- `,` adds thousands separators; `.2f` shows a float with exactly 2 decimals.
**Code (what you write in the interview):**
```python
name = "Ravi"
salary = 45000.5
department = "Sales"

print(f"{name} earns Rs {salary:,.2f} in {department}")
```
**Output:**
```text
Ravi earns Rs 45,000.50 in Sales
```
**What it means:** The number is shown the way a person would read a salary: with commas and paise.
**Likely follow-ups:** 1) *How to show a percentage?* `f"{rate:.1%}"` turns 0.123 into 12.3%. 2) *Does formatting change the value?* No, only how it prints.
**Common mistakes:** Forgetting the `f` prefix (prints the braces literally); writing `.2` instead of `.2f`.

### Q9 ⭐⭐⭐ 🟢 How do you handle a FileNotFoundError when a monthly attendance file is missing?
**Asked at:** commonly asked (no company-specific report found); file-handling question banks list it as a typical case.
**What the interviewer is checking:** That you catch this specific error and keep the script running with a clear message.
**Say this in the interview:** "I wrap the open in `try` and catch `FileNotFoundError`. I print which file was missing and continue, so one missing month does not stop the whole report."
**Explain simply:**
- Python raises FileNotFoundError when you open a file in read mode and it does not exist at that path.
- Catch it specifically, not every error, so real bugs still show up.
- Decide what "handle" means: skip, log, or stop with a clear message.
**Sample data:** `attendance_2024_09.csv` does not exist.
**Code (what you write in the interview):**
```python
file_name = "attendance_2024_09.csv"

try:
    with open(file_name) as f:
        lines = f.readlines()
    print("Rows read:", len(lines))
except FileNotFoundError:
    print("File missing:", file_name, "- skipping this month")
```
**Output:**
```text
File missing: attendance_2024_09.csv - skipping this month
```
**What it means:** The script reported the problem and carried on instead of crashing.
**Alternative:** Check first with `os.path.exists(file_name)` (see Q26), but try/except is safer because the file can vanish between the check and the open.
**Likely follow-ups:** 1) *What if the folder is wrong?* Same error; print the full path. 2) *Which other file errors exist?* PermissionError (file locked or no rights).
**Common mistakes:** Using a bare `except:`; a wrong relative path (the working folder is not where you think).

### Q10 ⭐⭐⭐ 🟢 What does ValueError: invalid literal for int() mean, and how do you avoid your script crashing on it?
**Asked at:** commonly asked (no company-specific report found); a staple error-handling question.
**What the interviewer is checking:** That you can explain the cause and handle it with try/except.
**Say this in the interview:** "It means I asked `int()` to convert text that is not a whole number, like 'N/A' or '12.5'. I wrap the conversion in `try/except ValueError` and skip or log the bad value."
**Explain simply:**
- `int("29")` works; `int("N/A")` fails because "N/A" is not a number.
- `int("12.5")` also fails (decimal text); use `float()` first.
- Data from files arrives as text, so bad values are common in real HR data.
- Catching `ValueError` lets the script continue with the next value.
**Code (what you write in the interview):**
```python
ages = ["29", "34", "N/A", "41"]

for age_text in ages:
    try:
        age = int(age_text)
        print(age)
    except ValueError:
        print("Skipped bad value:", age_text)
```
**Output:**
```text
29
34
Skipped bad value: N/A
41
```
**What it means:** Good values were converted; the bad one was reported and the loop carried on.
**Likely follow-ups:** 1) *What about empty text `""`?* Also a ValueError. 2) *What about `None`?* That is a TypeError, a different error.
**Common mistakes:** Catching the error but silently ignoring it, so bad data goes unnoticed; trying `int("45,000")` without removing commas.

### Q11 ⭐⭐⭐ 🟢 How do you take the first 3 characters, and the numeric part, of an employee code such as 'HYD-1045' using slicing or split?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured gap-fill of the standard slicing/split task.
**What the interviewer is checking:** That you know slicing `[:3]` and `split("-")` and remember to convert text to a number.
**Say this in the interview:** "`code[:3]` gives the first three characters. `code.split('-')` gives `['HYD', '1045']`, so index 1 is the number part, and I wrap it in `int()` to make it a number."
**Explain simply:**
- Slicing `[start:stop]` takes characters by position; `[:3]` means from the start up to (not including) position 3.
- `split("-")` cuts at the dash and returns a list; `[1]` picks the second piece.
- Slicing is fine when the prefix is always 3 letters; `split` is safer when lengths vary.
**Code (what you write in the interview):**
```python
code = "HYD-1045"

city_code = code[:3]                    # first 3 characters
number_part = int(code.split("-")[1])   # text after the dash, as a number

print(city_code)
print(number_part)
```
**Output:**
```text
HYD
1045
```
**What it means:** We separated the city code (HYD) from the running number (1045).
**Likely follow-ups:** 1) *How do you get the last 4 characters?* `code[-4:]`. 2) *What if a code has no dash?* `split("-")[1]` raises IndexError; check first or use try/except.
**Common mistakes:** Using `code[:2]` (off by one, stop is excluded); leaving the number as text so it sorts as "1045" before "999".

### Q12 ⭐⭐⭐ 🟡 Write code to convert salary strings like 'Rs. 45,000' into integers, skipping bad values such as 'N/A' with try/except.
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured composite of cleaning plus error handling.
**What the interviewer is checking:** Cleaning text step by step, then handling the failure case.
**Say this in the interview:** "I remove 'Rs.' and the commas, strip the spaces, and convert with `int()`. If a value like 'N/A' fails, the `except ValueError` skips it and the loop continues."
**Explain simply:**
- `replace("Rs.", "")` deletes the currency text; `replace(",", "")` deletes thousands commas.
- `strip()` removes leftover spaces.
- `int()` only works on clean digits, so anything else raises ValueError and is caught.
- Good values go into a new list; bad ones are reported, not hidden.
**Sample data:** `["Rs. 45,000", "Rs. 52,500", "N/A", "Rs. 60,000"]`
**Code (what you write in the interview):**
```python
raw_salaries = ["Rs. 45,000", "Rs. 52,500", "N/A", "Rs. 60,000"]
clean_salaries = []

for text in raw_salaries:
    try:
        number_text = text.replace("Rs.", "").replace(",", "").strip()
        clean_salaries.append(int(number_text))
    except ValueError:
        print("Skipped:", text)

print(clean_salaries)
```
**Output:**
```text
Skipped: N/A
[45000, 52500, 60000]
```
**What it means:** Three salaries were converted; "N/A" was skipped and reported.
**Likely follow-ups:** 1) *What if a value is `None` or NaN?* `None.replace` raises AttributeError, so check for missing values first. 2) *What if salaries have decimals?* Use `float()`.
**Common mistakes:** Forgetting that `replace` returns a new string; leaving the space after "Rs." so `int(" 45000")` is fine but "Rs 45000" is not.

### Q13 ⭐⭐⭐ 🟡 Read a CSV with csv.DictReader and compute the total salary per department using a dictionary.
**Asked at:** commonly asked (no company-specific report found); dictionary and loop tasks are reported in Python rounds at analytics firms (Tiger Analytics, Glassdoor summaries, details not read).
**What the interviewer is checking:** DictReader basics, converting text to numbers, and the `get(key, 0)` counting pattern.
**Say this in the interview:** "`DictReader` turns each row into a dictionary keyed by the header. I convert salary to int and add it to a running total per department using `get(department, 0)`."
**Explain simply:**
- `csv.DictReader` reads the header row for you; each row is a dictionary like `{"name": "Asha", "salary": "45000"}`.
- The csv module returns everything as text, so `int(...)` is needed before adding.
- `total_salary.get(department, 0)` returns the current total, or 0 the first time a department appears.
**Sample data:** `employees.csv` with 7 rows: Sales (Asha 45000, Meena 52000, Sam 48000), IT (Ravi 60000, Priya 70000), HR (John 40000, Kiran 41000).
**Code (what you write in the interview):**
```python
import csv

total_salary = {}

with open("employees.csv") as f:
    for row in csv.DictReader(f):
        department = row["department"]
        salary = int(row["salary"])        # csv gives text, so convert
        total_salary[department] = total_salary.get(department, 0) + salary

print(total_salary)
```
**Output:**
```text
{'Sales': 145000, 'IT': 130000, 'HR': 81000}
```
**What it means:** Sales spends 1,45,000 in salaries, IT 1,30,000 and HR 81,000.
**Alternative:** In pandas it is `pd.read_csv("employees.csv").groupby("department")["salary"].sum()`.
**Likely follow-ups:** 1) *What if a salary is blank?* `int("")` fails; wrap in try/except or skip empty values. 2) *What if the file uses another delimiter?* `csv.DictReader(f, delimiter="|")`.
**Common mistakes:** Adding strings (gives "4500060000"); writing `total_salary[department] += salary` without setting a starting value (KeyError).

### Q14 ⭐⭐⭐ 🟡 Why should you catch specific exceptions instead of a bare `except:`, and what can go wrong with a bare except?
**Asked at:** commonly asked (no company-specific report found); error-handling best practice appears in try/except question sets (Analytics Vidhya MCQs).
**What the interviewer is checking:** That you know bare except hides real bugs and can even block Ctrl+C.
**Say this in the interview:** "A bare except catches every error, including my own typos, so it hides real bugs behind a wrong message. I catch the specific error I expect, like ValueError, and let anything else show up."
**Explain simply:**
- A bare `except:` catches everything, even `KeyboardInterrupt` (pressing Ctrl+C) and `SystemExit`, so the script can become hard to stop (from memory, not run here).
- It hides programming mistakes (typos, wrong names) behind a misleading message.
- A specific except documents exactly what you expect to go wrong.
- If you must catch broadly, use `except Exception as e:` and print or log `e`.
**Code (what you write in the interview):**
```python
salary = 45000

try:
    bonus = salry * 0.1      # typo in the variable name
except:
    print("Salary is missing")
```
**Output:**
```text
Salary is missing
```
**What it means:** The real problem is a typo (`salry`, a NameError), but the bare except printed a wrong, misleading message and hid it. With `except ValueError:` the typo would have crashed loudly and been fixed.
**Likely follow-ups:** 1) *Can you catch two errors together?* Yes: `except (ValueError, TypeError):`. 2) *When is `except Exception` acceptable?* At the top of a batch job, if you log the error.
**Common mistakes:** `except: pass` (silent failure); logging nothing, so you never learn what failed.

### Q15 ⭐⭐ 🟢 What is the difference between upper(), lower(), title() and capitalize()?
**Asked at:** commonly asked (no company-specific report found); a standard string-method question (dev.to string questions).
**What the interviewer is checking:** That you know title() capitalises every word and capitalize() only the first letter of the whole text.
**Say this in the interview:** "`upper` makes everything capital, `lower` everything small, `title` capitalises the first letter of every word, and `capitalize` capitalises only the first letter of the whole string and lowers the rest."
**Explain simply:**
- All four return a new string; the original does not change.
- Use `lower()` before comparing text so "HR" and "hr" match.
- `title()` suits names; `capitalize()` suits a single sentence.
**Code (what you write in the interview):**
```python
text = "rAVI kUMAR from hr team"

print(text.upper())
print(text.lower())
print(text.title())
print(text.capitalize())
```
**Output:**
```text
RAVI KUMAR FROM HR TEAM
ravi kumar from hr team
Ravi Kumar From Hr Team
Ravi kumar from hr team
```
**What it means:** Same text, four different styles; note "HR" became "Hr" with `title()`.
**Likely follow-ups:** 1) *Which one for case-insensitive matching?* `lower()` (or `casefold()`). 2) *Any trap with title()?* Apostrophes: `"o'neil".title()` gives `O'Neil`, and acronyms like HR are changed.
**Common mistakes:** Expecting `capitalize()` to fix every word; forgetting to assign the result.

### Q16 ⭐⭐ 🟢 What do startswith() and endswith() do, and how would you filter employee IDs that start with 'HYD'?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured gap-fill of a standard string-method task.
**What the interviewer is checking:** That you know they return True or False and can use them as a filter.
**Say this in the interview:** "`startswith` checks whether text begins with a given piece and returns True or False; `endswith` checks the end. To filter, I loop through the IDs and keep the ones where `startswith('HYD')` is True."
**Explain simply:**
- Both return a boolean (True or False), so they fit directly inside an `if`.
- They are case sensitive: `"hyd-1".startswith("HYD")` is False.
- You can pass several options as a tuple: `startswith(("HYD", "BLR"))`.
**Sample data:** `["HYD-101", "BLR-202", "HYD-303", "PUN-404"]`
**Code (what you write in the interview):**
```python
employee_ids = ["HYD-101", "BLR-202", "HYD-303", "PUN-404"]

hyderabad_ids = [emp_id for emp_id in employee_ids if emp_id.startswith("HYD")]
print(hyderabad_ids)
print("HYD-101".endswith("101"))
```
**Output:**
```text
['HYD-101', 'HYD-303']
True
```
**What it means:** Only the two Hyderabad IDs were kept; the last line shows `endswith` returning True.
**Likely follow-ups:** 1) *How to ignore case?* `emp_id.upper().startswith("HYD")`. 2) *Pandas version?* `df[df["emp_id"].str.startswith("HYD")]`.
**Common mistakes:** Wrong case; using `==` when you only need the beginning to match.

### Q17 ⭐⭐ 🟢 What is the difference between find() and index() when the substring is not present?
**Asked at:** commonly asked (no company-specific report found); a standard string-method question.
**What the interviewer is checking:** That you know `find` returns -1 while `index` raises ValueError.
**Say this in the interview:** "Both return the position of the first match. If the text is not found, `find` quietly returns -1, but `index` raises a ValueError."
**Explain simply:**
- Positions start at 0, so the first character is position 0.
- `find` is safe for "does it exist?" checks, but you must test for -1.
- `index` is stricter: you want a crash if the text must be there.
- To only check presence, `"-" in code` is simplest.
**Code (what you write in the interview):**
```python
code = "HYD-1045"

print(code.find("-"))       # position found
print(code.find("X"))       # not found: -1

print(code.index("-"))
print(code.index("X"))      # not found: error
```
**Output:**
```text
3
-1
3
Traceback (most recent call last):
  File "q17.py", line 7, in <module>
    print(code.index("X"))      # not found: error
ValueError: substring not found
```
**What it means:** For a missing value, `find` gives -1 and `index` stops the script with an error.
**Likely follow-ups:** 1) *Danger of -1?* Using it as a slice position silently gives wrong results (`code[-1]` is the last character). 2) *How to search from the right?* `rfind` and `rindex`.
**Common mistakes:** Treating -1 as "found" in an `if` (`if code.find("X"):` is True for -1); forgetting that position 0 is falsy in `if code.find(...)`.

### Q18 ⭐⭐ 🟢 What is the difference between read(), readline() and readlines()?
**Asked at:** commonly asked (no company-specific report found); file-reading methods appear in file-handling question banks (ClimbTheLadder, AshokIT notes).
**What the interviewer is checking:** Whether you know what type each one returns and which is safe for big files.
**Say this in the interview:** "read() gives the whole file as one string, readline() gives one line each time I call it, and readlines() gives a list of all lines. They all keep the newline character at the end of each line."
**Explain simply:**
- `read()`: the entire file as one long string. Fine for small files.
- `readline()`: only the next line, as a string. Each call moves forward one line.
- `readlines()`: a list where every item is one line. Loads the whole file into memory, like `read()`.
- For a big file, loop directly over the file object (`for line in f:`), which reads one line at a time.
**Sample data:** `employees.txt` has three lines: Asha, Ravi, Meena.
**Code (what you write in the interview):**
```python
# read(): whole file as one string
with open("employees.txt") as f:
    everything = f.read()
print(repr(everything))

# readline(): one line per call
with open("employees.txt") as f:
    first_line = f.readline()
    second_line = f.readline()
print(repr(first_line), repr(second_line))

# readlines(): list of all lines
with open("employees.txt") as f:
    all_lines = f.readlines()
print(all_lines)
```
**Output:**
```text
'Asha\nRavi\nMeena\n'
'Asha\n' 'Ravi\n'
['Asha\n', 'Ravi\n', 'Meena\n']
```
**What it means:** `repr()` shows the hidden `\n` (new line) at the end of each line. You usually call `.strip()` to remove it.
**Likely follow-ups:** 1) *Which one for a 5 GB file?* None of them; loop with `for line in f`. 2) *What does readline() return at the end of the file?* An empty string.
**Common mistakes:** Forgetting the `\n` is still there; using `read()` on a huge file and running out of memory.

### Q19 ⭐⭐ 🟢 Write code to save a list of employee names to a text file, one name per line.
**Asked at:** commonly asked (no company-specific report found); writing to files is a standard file-handling task.
**What the interviewer is checking:** That you know write mode and that `write()` does not add a new line for you.
**Say this in the interview:** "I open the file in write mode with `with`, loop over the names, and write each name plus a newline character."
**Explain simply:**
- `"w"` mode creates the file, or erases it if it already exists (see Q2).
- `write()` writes exactly what you give it, so you add `"\n"` yourself to end each line.
- `with` closes the file automatically, which makes sure the data is saved.
**Sample data:** `employee_names = ["Asha", "Ravi", "Meena"]`
**Code (what you write in the interview):**
```python
employee_names = ["Asha", "Ravi", "Meena"]

# "w" creates the file (or overwrites an old one)
with open("names_out.txt", "w") as f:
    for name in employee_names:
        f.write(name + "\n")

# read it back to check
with open("names_out.txt") as f:
    print(f.read())
```
**Output:**
```text
Asha
Ravi
Meena

```
**What it means:** The file has one name per line (the blank line at the end of the output is just the last newline plus `print`'s own).
**Alternative:** `f.write("\n".join(employee_names))` writes the same names, but with no newline after the last one.
**Likely follow-ups:** 1) *How to add names without erasing?* Use `"a"` (append) mode. 2) *What if a name is not a string?* Convert it with `str(name)`.
**Common mistakes:** Forgetting `"\n"` so all names run together on one line; using `"w"` on a file you meant to keep.

### Q20 ⭐⭐ 🟢 How do you check whether a string is only digits, only letters, or letters and digits (isdigit, isalpha, isalnum)? Validate that a mobile number is 10 digits.
**Asked at:** commonly asked (no company-specific report found); string-method checks appear in string question banks (dev.to).
**What the interviewer is checking:** Whether you know the three methods and can combine them with `len()` for a real validation.
**Say this in the interview:** "isdigit is True when every character is a digit, isalpha when every character is a letter, and isalnum when every character is a letter or a digit. For a mobile number I check isdigit and also that the length is 10."
**Explain simply:**
- All three return `True` or `False`, and they return `False` for an empty string.
- Spaces, dashes and symbols make all three `False` (so `"Ravi Kumar"` is not alpha because of the space).
- `isdigit()` alone is not enough for a mobile number: `"123"` is all digits but too short. Add `len(mobile) == 10`.
**Code (what you write in the interview):**
```python
print("45000".isdigit())        # only digits
print("Ravi".isalpha())         # only letters
print("HR101".isalnum())        # letters and digits
print("Ravi Kumar".isalpha())   # space makes it False

# mobile number: all digits and exactly 10 characters
mobile = "9876543210"
if mobile.isdigit() and len(mobile) == 10:
    print("valid")
else:
    print("invalid")
```
**Output:**
```text
True
True
True
False
valid
```
**What it means:** The first three checks pass; the space in "Ravi Kumar" fails; the mobile number passes both rules.
**Likely follow-ups:** 1) *What about "-5" or "4.5"?* `isdigit()` returns False for both (the dash and dot are not digits). 2) *Does a leading +91 pass?* No; clean it first (see Q31).
**Common mistakes:** Checking only digits and not the length; forgetting the input has spaces or a trailing newline (call `.strip()` first).

### Q21 ⭐⭐ 🟢 What is the difference between f-strings, str.format() and the % operator for formatting text?
**Asked at:** commonly asked (no company-specific report found); string formatting appears in string study guides (Fiveable).
**What the interviewer is checking:** Whether you know the modern way (f-strings) and can still read the older two.
**Say this in the interview:** "All three put values into text. The % operator is the oldest, `.format()` came next, and f-strings are the newest and the most readable, so I use f-strings."
**Explain simply:**
- f-string: put `f` before the quote and write the variable inside `{}`. Needs Python 3.6 or newer.
- `.format()`: put `{}` placeholders in the text and pass the values to `.format(...)`.
- `%` operator: `%s` for text, `%.2f` for a decimal number, then `% (values)`. Older style, still seen in old code.
- The format spec after a colon, like `:,.2f`, works in f-strings and `.format()`. The `%` style has no thousands separator.
**Code (what you write in the interview):**
```python
name = "Ravi"
salary = 45000.5

print(f"{name} earns Rs {salary:,.2f}")                 # f-string
print("{} earns Rs {:,.2f}".format(name, salary))       # str.format()
print("%s earns Rs %.2f" % (name, salary))              # % operator
```
**Output:**
```text
Ravi earns Rs 45,000.50
Ravi earns Rs 45,000.50
Ravi earns Rs 45000.50
```
**What it means:** The first two give the same nicely formatted number; the `%` version cannot add the comma.
**Likely follow-ups:** 1) *Why are f-strings preferred?* The value sits right where it appears in the text, so it is easier to read and to get right. 2) *Can an f-string run code?* Yes, for example `{salary * 12:,.0f}`.
**Common mistakes:** Forgetting the `f` before the quote (the braces print as text); mixing the order of values in `.format()` or `%`.

### Q22 ⭐⭐ 🟢 How do you pad employee ID 45 to '00045' using zfill() or format specifiers?
**Asked at:** commonly asked (no company-specific report found); HR-flavoured gap-fill (employee IDs).
**What the interviewer is checking:** Whether you know `zfill` works on strings, so a number must be converted first.
**Say this in the interview:** "zfill(5) pads a string with zeros on the left to width 5, so I convert the number to a string first. An f-string with `:05d` does the same in one step."
**Explain simply:**
- `zfill` is a string method; calling it on an integer gives an error, so use `str(45)` first.
- In a format spec, `05d` means "width 5, pad with 0, treat as a whole number".
- If the number is already longer than the width, nothing is cut off.
**Code (what you write in the interview):**
```python
employee_id = 45

print(str(employee_id).zfill(5))     # zfill needs a string
print(f"{employee_id:05d}")          # f-string format spec
print("{:05d}".format(employee_id))  # str.format version
```
**Output:**
```text
00045
00045
00045
```
**What it means:** All three give the same 5-character ID with leading zeros.
**Likely follow-ups:** 1) *Why keep the ID as text?* A number loses leading zeros, so store IDs as strings. 2) *What does `"-5".zfill(4)` give?* `-005`; zfill keeps the sign in front.
**Common mistakes:** Calling `.zfill()` on an int; using `:05` on a string (it pads with spaces on the right, not zeros).

### Q23 ⭐⭐ 🟢 How do you split the full name 'Ravi Kumar Singh' into first name and last name?
**Asked at:** commonly asked (no company-specific report found); name splitting is a common HR data-cleaning task.
**What the interviewer is checking:** Whether you handle names with more than two words and don't assume exactly one space.
**Say this in the interview:** "I split on spaces, take the first item as the first name and the last item as the last name. If they want everything after the first word as the surname, I split once with maxsplit 1."
**Explain simply:**
- `split()` with no argument splits on any run of spaces and gives a list of words.
- `parts[0]` is the first word; `parts[-1]` is the last word (index -1 means "from the end").
- `split(" ", 1)` cuts only at the first space, so "Kumar Singh" stays together as the last name.
- A one-word name still works with `[0]` and `[-1]` (both give the same word); a two-variable unpack would crash.
**Code (what you write in the interview):**
```python
full_name = "Ravi Kumar Singh"

# first word and last word
parts = full_name.split()
first_name = parts[0]
last_name = parts[-1]
print(first_name, last_name)

# alternative: everything after the first space is the surname
first_name, last_name = full_name.split(" ", 1)
print(first_name, "|", last_name)
```
**Output:**
```text
Ravi Singh
Ravi | Kumar Singh
```
**What it means:** Choose by business rule: "Singh" alone, or "Kumar Singh" as the surname. Say which you chose.
**Likely follow-ups:** 1) *What if there is only one word?* `split(" ", 1)` returns one item and the unpack fails; check `len(parts)` first. 2) *How to do this on a whole column?* Use `df["name"].str.split()` in pandas.
**Common mistakes:** Splitting on `" "` when the text has double spaces (gives empty items); assuming every name has exactly two words.

### Q24 ⭐⭐ 🟢 How do you read a Python traceback, and where do you look first?
**Asked at:** commonly asked (no company-specific report found); debugging skill is part of the exception-handling theme.
**What the interviewer is checking:** Whether you stay calm and read errors in the right order instead of guessing.
**Say this in the interview:** "I read from the bottom up. The last line gives the error type and message. Then I look at the line just above it for where it happened in my code, and trace upward to see how the program got there."
**Explain simply:**
- A traceback (the error report Python prints when a script crashes) lists the chain of function calls, oldest at the top, newest at the bottom.
- The last line is the most useful: the exception type (`KeyError`) and the detail (`'Ravi'`).
- The last `File ... line N` entry is the exact line that failed; earlier entries show who called it.
- Look for the entries that are in your own file; ignore library internals unless nothing else points to your code.
**Sample data:** `salaries = {"Asha": 45000}` and we ask for "Ravi".
**Code (what you write in the interview):**
```python
def get_salary(salaries, name):
    return salaries[name]

salaries = {"Asha": 45000}
print(get_salary(salaries, "Ravi"))
```
**Output:** (file path shortened to `salary_check.py`)
```text
Traceback (most recent call last):
  File "salary_check.py", line 5, in <module>
    print(get_salary(salaries, "Ravi"))
          ~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "salary_check.py", line 2, in get_salary
    return salaries[name]
           ~~~~~~~~^^^^^^
KeyError: 'Ravi'
```
**What it means:** Bottom line: a `KeyError` for 'Ravi', so that name is not in the dictionary. The line above says it happened in `get_salary` at line 2, called from line 5.
**Likely follow-ups:** 1) *What if the error is inside a pandas file?* Scroll up to the last line that is in your own script. 2) *What next?* Print the values involved or use `.get()` with a default.
**Common mistakes:** Reading from the top and getting lost; ignoring the message text; changing code before understanding the error.

### Q25 ⭐⭐ 🟢 What is the difference between a syntax error and an exception? Give an example of each.
**Asked at:** commonly asked (no company-specific report found); exception-handling basics.
**What the interviewer is checking:** That you know when each is detected and that only exceptions can be caught with try/except.
**Say this in the interview:** "A syntax error means the code is written wrongly, so Python refuses to run it at all. An exception happens while the code is running, even though the code was valid, and I can catch it with try/except."
**Explain simply:**
- Syntax error: broken grammar, like a missing colon. Python spots it before running any line, so nothing runs.
- Exception: valid code that fails at run time, like dividing text by a number or opening a missing file. Earlier lines do run first.
- You fix a syntax error by correcting the code; you handle an exception with try/except, or by validating the input.
**Code (what you write in the interview):**
```python
# Syntax error: missing colon after the if condition
salary = 45000
if salary > 40000
    print("high")
```
```python
# Exception: valid code, but text cannot be divided by a number
salary = "45000"
bonus = salary / 10
```
**Output:** (file paths shortened)
```text
  File "syntax_demo.py", line 2
    if salary > 40000
                     ^
SyntaxError: expected ':'

Traceback (most recent call last):
  File "exception_demo.py", line 2, in <module>
    bonus = salary / 10
            ~~~~~~~^~~~
TypeError: unsupported operand type(s) for /: 'str' and 'int'
```
**What it means:** The first never started running; the second ran line 1 and failed on line 2.
**Likely follow-ups:** 1) *Can you catch a SyntaxError with try/except?* Not in the same file, because the file does not run; it is only catchable in special cases like `eval`. 2) *Name common exceptions.* ValueError, TypeError, KeyError, FileNotFoundError, ZeroDivisionError.
**Common mistakes:** Thinking try/except fixes broken syntax; calling every error a "syntax error".

### Q26 ⭐⭐ 🟢 How do you check whether a file exists before opening it, using os.path or pathlib?
**Asked at:** commonly asked (no company-specific report found); related to the missing-file handling in Q9.
**What the interviewer is checking:** That you know both tools and the trade-off with try/except.
**Say this in the interview:** "`os.path.exists(path)` or `Path(path).exists()` returns True or False. pathlib is the modern way. I can also just try to open the file and catch FileNotFoundError, which avoids the file disappearing between the check and the open."
**Explain simply:**
- `os.path.exists`: older function-style tool, works with plain strings.
- `pathlib.Path`: modern object-style tool; `Path("a.csv").exists()`. Also has `.is_file()` and `.is_dir()`.
- `exists()` is True for folders too; use `.is_file()` if you need a file specifically.
- Checking first is fine for simple scripts; try/except is safer in busy shared folders.
**Sample data:** `employees.csv` exists; `august_attendance.csv` does not.
**Code (what you write in the interview):**
```python
import os
from pathlib import Path

print(os.path.exists("employees.csv"))           # os.path way
print(Path("employees.csv").exists())            # pathlib way

# typical use: skip a missing monthly file
if Path("august_attendance.csv").exists():
    print("reading file")
else:
    print("file missing, skipping")
```
**Output:**
```text
True
True
file missing, skipping
```
**What it means:** The first two checks find the file; the August file is missing, so the script skips it instead of crashing.
**Likely follow-ups:** 1) *Difference between exists and is_file?* exists is True for folders as well. 2) *Is the check enough?* Not fully; the file could vanish right after, so try/except is more robust.
**Common mistakes:** Relying on a relative path without knowing the current working folder; typos in the file name.

### Q27 ⭐⭐ 🟢 What is a raw string (r'...') and why do you need it for Windows file paths such as 'C:\data\new_hires.csv'?
**Asked at:** commonly asked (no company-specific report found); a classic gotcha for analysts on Windows.
**What the interviewer is checking:** That you know backslash is the escape character in Python strings.
**Say this in the interview:** "In a normal string, a backslash starts a special code, like `\n` for a new line. A raw string, with `r` before the quote, treats backslashes as plain characters, so Windows paths work."
**Explain simply:**
- Escape character: a backslash that gives the next letter a special meaning (`\n` = new line, `\t` = tab).
- In `"C:\data\new_hires.csv"`, the `\n` in `\new_hires` becomes a new line, which silently breaks the path.
- Raw string `r"C:\data\new_hires.csv"` keeps every backslash as it is.
- Other fixes: double the backslashes (`"C:\\data\\new_hires.csv"`) or use forward slashes (`"C:/data/new_hires.csv"`).
- A raw string cannot end with a single backslash.
**Code (what you write in the interview):**
```python
bad_path = "C:\data\new_hires.csv"
good_path = r"C:\data\new_hires.csv"

print(bad_path)
print(good_path)
```
**Output:**
```text
C:\data
ew_hires.csv
C:\data\new_hires.csv
```
**What it means:** The normal string turned `\n` into a line break, so the path is split in two (Python also printed a SyntaxWarning about `\d`, not shown). The raw string is correct.
**Likely follow-ups:** 1) *Are raw strings only for paths?* No, also for regex patterns (Q29). 2) *Easiest safe option?* `pathlib.Path("C:/data/new_hires.csv")` with forward slashes.
**Common mistakes:** Copy-pasting a Windows path without the `r`; thinking the error is in the file when it is in the string.

### Q28 ⭐⭐ 🟢 How do you raise your own exception, for example rejecting a negative salary with raise ValueError?
**Asked at:** commonly asked (no company-specific report found); validation theme in exception handling.
**What the interviewer is checking:** That you can stop bad data early with a clear message.
**Say this in the interview:** "I check the value with an if, and if it is invalid I use `raise ValueError('message')`. The caller can then catch it with try/except or let the script stop with a clear reason."
**Explain simply:**
- `raise` creates an error on purpose and stops the current function.
- Use `ValueError` when the type is right but the value is wrong (a negative salary). Use `TypeError` for a wrong type.
- The message should say what is wrong in plain words, so the next person can fix the data.
- Raising is better than silently returning a bad value, which would spread wrong numbers into reports.
**Code (what you write in the interview):**
```python
def check_salary(salary):
    # reject impossible values early
    if salary < 0:
        raise ValueError("Salary cannot be negative")
    return salary

try:
    check_salary(-500)
except ValueError as error:
    print("Rejected:", error)
```
**Output:**
```text
Rejected: Salary cannot be negative
```
**What it means:** The bad salary was stopped, and the message we wrote reached the user.
**Likely follow-ups:** 1) *Raise vs assert?* raise is for validating data at run time; assert is for internal checks while developing (see Q49). 2) *Can you re-raise?* Yes, a bare `raise` inside `except` passes the error on.
**Common mistakes:** Raising a vague message like "error"; using `print` and carrying on with bad data; raising the base `Exception` instead of a specific type.

### Q29 ⭐⭐ 🟡 Write code to extract all email addresses from a block of text using re.findall.
**Asked at:** commonly asked (no company-specific report found); regex basics appear in DA question sets (Naukri Code360).
**What the interviewer is checking:** That you can write a simple, readable pattern and use the `re` module.
**Say this in the interview:** "I import re and call `re.findall` with a pattern for 'some word characters, an at sign, a domain with a dot'. It returns a list of every match. It is a practical pattern, not a perfect one."
**Explain simply:**
- Regex (regular expression): a mini-language for describing text patterns.
- `\w` means a letter, digit or underscore; `+` means "one or more"; `\.` means a literal dot. Put `r` before the pattern string (Q27).
- `[\w.]+` means "word characters or dots, one or more".
- `findall` returns all non-overlapping matches as a list of strings.
**Sample data:** Text with two emails and a phone fragment.
**Code (what you write in the interview):**
```python
import re

text = "Contact asha@company.com or ravi.k@mail.co.in. Call 98765 for help."

# name part, @, then domain ending in a dot and letters
emails = re.findall(r"[\w.]+@[\w.]+\.\w+", text)
print(emails)
```
**Output:**
```text
['asha@company.com', 'ravi.k@mail.co.in']
```
**What it means:** Both emails were found; the trailing full stop after `.in` was not included because the pattern must end on a word character.
**Likely follow-ups:** 1) *Is this a perfect email validator?* No; real email rules are complex, this is good enough for extraction. 2) *What if there are no matches?* You get an empty list.
**Common mistakes:** Forgetting the `r` prefix; not escaping the dot (`.` alone means "any character"); expecting a single string back instead of a list.

### Q30 ⭐⭐ 🟡 What is the difference between re.match, re.search, re.findall and re.sub?
**Asked at:** commonly asked (no company-specific report found); core regex functions.
**What the interviewer is checking:** That you know where each one looks and what it returns.
**Say this in the interview:** "match only checks the start of the text, search finds the first match anywhere, findall returns a list of all matches, and sub replaces matches with new text."
**Explain simply:**
- `re.match`: must match at position 0, otherwise returns `None`.
- `re.search`: scans the whole text, returns the first match (a match object; use `.group()` to get the text) or `None`.
- `re.findall`: a list of every match; empty list if none.
- `re.sub(pattern, replacement, text)`: returns a new string with matches replaced.
**Sample data:** `"Employee E101 joined, then E102 joined"`
**Code (what you write in the interview):**
```python
import re

text = "Employee E101 joined, then E102 joined"

print(re.match(r"E\d+", text))                 # not at the start
print(re.match(r"Employee", text).group())     # at the start
print(re.search(r"E\d+", text).group())        # first match anywhere
print(re.findall(r"E\d+", text))               # all matches
print(re.sub(r"E\d+", "ID", text))             # replace matches
```
**Output:**
```text
None
Employee
E101
['E101', 'E102']
Employee ID joined, then ID joined
```
**What it means:** `match` fails for E101 because the text starts with "Employee". The others find the IDs wherever they are.
**Likely follow-ups:** 1) *What does `\d+` mean?* One or more digits. 2) *What does match return on failure?* `None`, so calling `.group()` on it crashes; check first.
**Common mistakes:** Using `match` when you meant `search`; calling `.group()` on `None`; forgetting that `sub` returns a new string and does not change the original.

### Q31 ⭐⭐ 🟡 Write code to standardise messy phone numbers such as '+91 98765-43210' by removing non-digits and keeping the last 10 digits.
**Asked at:** commonly asked (no company-specific report found); HR/contact data cleaning gap-fill.
**What the interviewer is checking:** That you can clean text with `re.sub` and slicing, and know why taking the last 10 is safe.
**Say this in the interview:** "First I remove every character that is not a digit with `re.sub(r'\D', '', phone)`, then I take the last 10 characters with `[-10:]`, which drops the country code."
**Explain simply:**
- `\D` means "any character that is not a digit". Replacing it with an empty string deletes it.
- `[-10:]` means "the last 10 characters", so +91 or a leading 0 falls away.
- If fewer than 10 digits remain, the number is bad data; check `len()` and flag it.
**Code (what you write in the interview):**
```python
import re

phone = "+91 98765-43210"

# keep digits only
digits_only = re.sub(r"\D", "", phone)

# keep the last 10 digits (drops the country code)
last_10_digits = digits_only[-10:]
print(last_10_digits)
```
**Output:**
```text
9876543210
```
**What it means:** The messy number is now a clean 10-digit mobile number.
**Alternative:** Without regex: `"".join(ch for ch in phone if ch.isdigit())[-10:]`.
**Likely follow-ups:** 1) *What if only 8 digits remain?* Slicing will not complain, so validate the length (Q20). 2) *Same for a column?* `df["phone"].str.replace(r"\D", "", regex=True).str[-10:]`.
**Common mistakes:** Removing only spaces and dashes but leaving the `+`; using `[:10]` (first 10) instead of `[-10:]`.

### Q32 ⭐⭐ 🟡 Write code to read a pipe-delimited attendance log with lines like 'E101|2024-08-01|P' and count present days per employee.
**Asked at:** commonly asked (no company-specific report found); HR-flavoured gap-fill, and dictionary counting appears in Tiger Analytics Python round reports (snippet-level, unverified).
**What the interviewer is checking:** File reading, splitting, and counting with a dictionary, with no pandas.
**Say this in the interview:** "I read the file line by line, split each line on the pipe, and if the status is P I add one to that employee's count in a dictionary, using `get` with a default of 0."
**Explain simply:**
- `line.strip().split("|")` removes the newline and cuts the line into three parts, which I unpack into names.
- A dictionary (key to value pairs) holds each employee ID and their count.
- `present_days.get(id, 0)` returns the current count, or 0 the first time we see that employee.
- An employee with no P at all never gets added; mention this and add them with 0 if needed.
**Sample data:** `attendance_log.txt`
```text
E101|2024-08-01|P
E102|2024-08-01|A
E101|2024-08-02|P
E102|2024-08-02|P
E101|2024-08-03|A
```
**Code (what you write in the interview):**
```python
present_days = {}

with open("attendance_log.txt") as f:
    for line in f:
        # split one line into its three parts
        employee_id, date, status = line.strip().split("|")
        if status == "P":
            present_days[employee_id] = present_days.get(employee_id, 0) + 1

print(present_days)
```
**Output:**
```text
{'E101': 2, 'E102': 1}
```
**What it means:** E101 was present 2 days and E102 was present 1 day.
**Likely follow-ups:** 1) *What if a line is blank or has a missing part?* The unpack raises ValueError; wrap it in try/except or skip empty lines. 2) *How in pandas?* `pd.read_csv(file, sep="|", names=[...])` then filter and `groupby`.
**Common mistakes:** Forgetting `.strip()` (the status becomes `"P\n"` and never equals `"P"`); starting a count without a default and getting a KeyError.

### Q33 ⭐⭐ 🟡 How do you read and write JSON files with json.load and json.dump?
**Asked at:** commonly asked (no company-specific report found); JSON is common in API and config data.
**What the interviewer is checking:** That you know the file versions versus the string versions.
**Say this in the interview:** "`json.dump(data, file)` writes a Python dictionary or list into a file as JSON, and `json.load(file)` reads it back into Python. The ones ending in s, `dumps` and `loads`, work on strings instead of files."
**Explain simply:**
- JSON (JavaScript Object Notation): a text format for nested data, common in web APIs. It looks like a Python dictionary.
- Open the file in `"w"` to dump and in `"r"` (default) to load.
- `indent=2` makes the saved file easy to read.
- JSON turns Python `None` into `null` and tuples into lists; dates are not supported directly (convert them to text first).
**Code (what you write in the interview):**
```python
import json

employee = {"name": "Asha", "department": "Sales", "salary": 45000}

# write the dictionary to a file
with open("employee.json", "w") as f:
    json.dump(employee, f, indent=2)

# read it back into a dictionary
with open("employee.json") as f:
    loaded_employee = json.load(f)

print(loaded_employee["name"])
```
**Output:**
```text
Asha
```
**What it means:** The data went out to a file and came back as a normal dictionary.
**Likely follow-ups:** 1) *load vs loads?* `load` reads from a file, `loads` from a string. 2) *How to turn JSON into a DataFrame?* `pd.read_json` or `pd.json_normalize` for nested data.
**Common mistakes:** Passing the file name instead of the open file to `json.load`; trying to dump a date or numpy number (TypeError).

### Q34 ⭐⭐ 🟡 When do you use csv.reader, csv.DictReader and pandas.read_csv?
**Asked at:** commonly asked (no company-specific report found); decision-style question on tools.
**What the interviewer is checking:** Whether you choose the right tool by data size and task, not by habit.
**Say this in the interview:** "csv.reader gives each row as a list, csv.DictReader gives each row as a dictionary with the header names, and pandas.read_csv gives a whole table I can analyse. For analysis I use pandas; for small row-by-row jobs or when I cannot install pandas, I use the csv module."
**Explain simply:**
- `csv.reader`: each row is a list of text values; you use positions (`row[2]`). Fast and light, but easy to mix up columns.
- `csv.DictReader`: each row is a dictionary, so you write `row["salary"]`. Clearer, still plain Python.
- `pandas.read_csv`: loads into a DataFrame (a table) with data types guessed, ready for filtering, grouping and joining.
- Both csv readers return everything as text, so convert numbers yourself with `int()`. pandas guesses numbers for you.
**Sample data:** `employees.csv` with columns employee, department, salary.
**Code (what you write in the interview):**
```python
import csv
import pandas as pd

# csv.reader: rows as lists
with open("employees.csv") as f:
    for row in csv.reader(f):
        print(row)

# csv.DictReader: rows as dictionaries
with open("employees.csv") as f:
    for row in csv.DictReader(f):
        print(row["employee"], row["salary"])

# pandas: a full table
print(pd.read_csv("employees.csv"))
```
**Output:**
```text
['employee', 'department', 'salary']
['Asha', 'Sales', '45000']
['Ravi', 'HR', '38000']
['Meena', 'Sales', '52000']
Asha 45000
Ravi 38000
Meena 52000
  employee department  salary
0     Asha      Sales   45000
1     Ravi         HR   38000
2    Meena      Sales   52000
```
**What it means:** `reader` even returns the header as a normal row, and all its values are text. pandas returns a table with `salary` already a number.
**Likely follow-ups:** 1) *When is the csv module still better?* Tiny scripts, strict row-by-row processing of huge files, or limited environments. 2) *Can pandas read big files in pieces?* Yes, with `chunksize`.
**Common mistakes:** Forgetting that csv values are strings (summing them gives text joined together); forgetting the header row appears in `csv.reader` output; opening the file without `newline=""` when writing (see Q38).

### Q35 ⭐⭐ 🟡 Write a function that returns the attrition rate but returns None instead of crashing when headcount is 0 (ZeroDivisionError).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you guard a division and handle the one failure you expect, without hiding other bugs?
**Say this in the interview:** "Attrition rate is people who left divided by headcount, times 100. If headcount is 0 the division fails, so I catch ZeroDivisionError and return None, which means 'no rate'. I would not return 0, because 0% attrition is a real answer and this is not."
**Explain simply:**
- Attrition rate = employees who left / headcount x 100. Example: 12 left out of 240 = 5%.
- Dividing by zero raises `ZeroDivisionError` (Python's way of saying "this maths is impossible").
- `try` runs the risky line; `except ZeroDivisionError` runs only if that exact error happens.
- `None` is Python's "no value". Returning it tells the caller "not calculable", which is different from 0.
**Code (what you write in the interview):**
```python
def attrition_rate(employees_left, headcount):
    try:
        return employees_left / headcount * 100
    except ZeroDivisionError:
        # no employees, so a rate has no meaning
        return None


print(attrition_rate(12, 240))
print(attrition_rate(0, 0))
```
**Output:**
```
5.0
None
```
**What it means:** A normal team gives 5.0 (percent). An empty team gives None instead of a crash, so a loop over many departments keeps running.
**Alternative:** `if headcount == 0: return None` before dividing. Both are fine; the `if` check is simpler to read, `try/except` is what the question asks for.
**Likely follow-ups:**
- *Why not return 0?* It would claim "nobody left" for a team that does not exist.
- *What if headcount is a string?* That raises `TypeError`, which this function deliberately does not catch.
**Common mistakes:** Using a bare `except:` that hides every error; returning 0; forgetting `* 100` so the rate is 0.05 instead of 5.

### Q36 ⭐⭐ 🟡 Write code to process a file row by row, collect the bad rows in a separate file, and keep going when a row fails.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you put `try/except` inside the loop so one bad row does not stop the whole run?
**Say this in the interview:** "I read row by row, wrap the conversion in try/except inside the loop, write failures plus the reason to a bad-rows file, and carry on. At the end I report how many were good."
**Explain simply:**
- The `try` goes inside the `for` loop. If it wrapped the loop, the first bad row would end everything.
- `csv.DictReader` reads each row as a dictionary, so you use column names like `row["salary"]`.
- Saving the error message next to the bad row lets HR or the data owner fix it later.
- `newline=""` stops blank lines in CSV files on Windows (see Q38).
**Sample data:** `employees.csv`
```
emp_id,name,salary
E101,Asha,45000
E102,Ravi,N/A
E103,Meena,52000
E104,John,
E105,Kiran,61000
```
**Code (what you write in the interview):**
```python
import csv

good_rows = []

with open("employees.csv", newline="") as source, open("bad_rows.csv", "w", newline="") as bad_file:
    reader = csv.DictReader(source)
    bad_writer = csv.writer(bad_file)
    bad_writer.writerow(["emp_id", "name", "salary", "reason"])

    for row in reader:
        try:
            row["salary"] = int(row["salary"])
            good_rows.append(row)
        except ValueError as error:
            # save the bad row with the reason, then carry on
            bad_writer.writerow([row["emp_id"], row["name"], row["salary"], str(error)])

print(len(good_rows), "good rows")
```
**Output:**
```
3 good rows
```
Contents of `bad_rows.csv` after the run:
```
emp_id,name,salary,reason
E102,Ravi,N/A,invalid literal for int() with base 10: 'N/A'
E104,John,,invalid literal for int() with base 10: ''
```
**What it means:** 3 clean rows were kept; the 2 rows with 'N/A' and a blank salary went to a separate file with the reason, and the script never crashed.
**Likely follow-ups:**
- *How would you do it in pandas?* `pd.to_numeric(df["salary"], errors="coerce")`, then filter the rows that became NaN.
- *Why save the reason?* So the person fixing the data knows what was wrong.
**Common mistakes:** Putting `try` outside the loop; catching everything with a bare `except`; silently dropping bad rows with no record.

### Q37 ⭐⭐ 🟡 When does the else block of try/except run, and does finally still run if the try block has a return statement?
**Asked at:** try/except/finally appears as a technical-stage question on a practice platform (Dataford, snippet only); otherwise commonly asked.
**What the interviewer is checking:** Do you know the exact order: try, then except or else, then always finally?
**Say this in the interview:** "`else` runs only when the try block finished with no error. `finally` always runs, even if the try block has a return, so it is where I put cleanup like closing a file."
**Explain simply:**
- `try`: the risky code.
- `except`: runs only if an error happened.
- `else`: runs only if there was no error (and the try block did not return early).
- `finally`: runs every time, error or not, return or not.
- With `return` inside `try`, Python first runs `finally`, then actually returns. The `else` block is skipped because the function already left.
**Code (what you write in the interview):**
```python
def demo():
    try:
        number = int("42")
        return "try returned"
    except ValueError:
        return "except returned"
    else:
        print("else ran")
    finally:
        print("finally ran")


print(demo())
```
**Output:**
```
finally ran
try returned
```
**What it means:** "finally ran" printed before the returned text, and "else ran" never printed. Without the `return`, the same code prints "else ran" then "finally ran" (checked by running it).
**Likely follow-ups:**
- *What if finally also has a return?* It overrides the earlier return (and can hide an error), so avoid it.
- *Why use else at all?* It keeps the risky line alone in `try`, so you only catch errors from that line.
**Common mistakes:** Thinking `else` runs after `except`; thinking `return` skips `finally`; putting lots of code in `try` so unrelated errors get caught.

### Q38 ⭐⭐ 🟡 What does newline='' do when writing a CSV, and why do you sometimes get blank lines between rows?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the Windows blank-line gotcha when using the `csv` module?
**Say this in the interview:** "The csv writer ends each row with `\r\n` by itself. On Windows, Python's text mode also converts `\n` into `\r\n`, so you can end up with two line endings and a blank line. Opening the file with `newline=''` tells Python not to touch line endings, so the csv module controls them."
**Explain simply:**
- A "newline" is the invisible character that ends a line. Windows uses two characters (`\r\n`); Linux and Mac use one (`\n`).
- Python's normal text mode translates line endings for you. The csv module also writes its own. Doing both doubles up.
- `newline=''` means "no translation". The Python docs recommend it for all csv files, for reading and writing.
- The blank-line symptom shows on Windows; I could only run this on Linux, where it looks fine either way (the Windows symptom itself is from memory, unverified here).
**Code (what you write in the interview):**
```python
import csv

with open("out.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["emp_id", "name"])
    writer.writerow(["E101", "Asha"])

with open("out.csv", "rb") as file:
    print(file.read())
```
**Output:**
```
b'emp_id,name\r\nE101,Asha\r\n'
```
**What it means:** The file holds exactly one `\r\n` per row, which is what we want. (The last two lines just show the raw bytes to prove it.)
**Likely follow-ups:**
- *Do you need it when reading?* Yes, it is also recommended, so quoted fields with line breaks inside are read correctly.
- *Does pandas have this problem?* `df.to_csv()` handles it for you.
**Common mistakes:** Forgetting `newline=''` and seeing blank rows in Excel; "fixing" it by deleting blank rows afterwards instead of fixing the open call.

### Q39 ⭐⭐ 🟡 A column holds 'Sales - Hyderabad'. Write code to split it into department and city and strip the extra spaces.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic string cleaning: split, unpack and strip.
**Say this in the interview:** "I split on the dash, unpack into two variables, then strip the spaces around each. I split only at the first dash in case a city name has a dash too."
**Explain simply:**
- `split("-", 1)` cuts the text at the first dash and returns a list of two pieces: `["Sales ", " Hyderabad"]`.
- The pieces still have spaces, so `strip()` removes spaces from both ends.
- `department, city = ...` is "unpacking": the first piece goes to `department`, the second to `city`.
- Strings are immutable (cannot be changed in place), so `strip()` returns a new string that you must save.
**Code (what you write in the interview):**
```python
text = "Sales - Hyderabad"

# split only at the first dash, then remove extra spaces
department, city = text.split("-", 1)
department = department.strip()
city = city.strip()

print(department)
print(city)
```
**Output:**
```
Sales
Hyderabad
```
**What it means:** The one messy cell became two clean values.
**Alternative:** In pandas, for a whole column: `df[["department", "city"]] = df["dept_city"].str.split("-", n=1, expand=True)` and then `.str.strip()` on each column (from memory, not run here).
**Likely follow-ups:**
- *What if a row has no dash?* Unpacking fails with `ValueError`; check `"-" in text` first.
- *Why split on "-" and not " - "?* Splitting on the dash alone also copes with uneven spacing.
**Common mistakes:** Forgetting to save the stripped result; splitting without `1` and breaking on 'Navi-Mumbai'; assuming every row has a dash.

### Q40 ⭐⭐ 🟡 Write code to remove duplicate employee IDs from a text file while keeping the original order.
**Asked at:** Python rounds at the analytics firms in the internal research note are described as mostly basic (lists, strings, duplicates); no company-specific report found for this exact task.
**What the interviewer is checking:** Do you know `set()` loses order, and can you keep order with a "seen" set?
**Say this in the interview:** "I keep a set of IDs I have already seen, because checking a set is fast. I walk through the file once, and only add an ID to my result list the first time I see it. That keeps the original order."
**Explain simply:**
- A set is a collection with no duplicates and no guaranteed order, so `set(ids)` alone would scramble the order.
- `seen_ids` answers "have I met this one before?" instantly; `unique_ids` holds the ordered result.
- `line.strip()` removes the hidden newline at the end of each line, otherwise 'E101\n' and 'E101' look different.
**Sample data:** `ids.txt` has the lines E101, E102, E101, E103, E102, E104.
**Code (what you write in the interview):**
```python
seen_ids = set()
unique_ids = []

with open("ids.txt") as file:
    for line in file:
        employee_id = line.strip()
        if employee_id not in seen_ids:
            seen_ids.add(employee_id)
            unique_ids.append(employee_id)

with open("unique_ids.txt", "w") as file:
    for employee_id in unique_ids:
        file.write(employee_id + "\n")

print(unique_ids)
```
**Output:**
```
['E101', 'E102', 'E103', 'E104']
```
**What it means:** Each ID appears once, in the order it first showed up, and the clean list is saved to `unique_ids.txt`.
**Alternative:** `list(dict.fromkeys(ids))` keeps first-seen order in one line (dictionaries remember insertion order).
**Likely follow-ups:**
- *Why not just `list(set(ids))`?* It removes duplicates but does not promise the order.
- *Why a set and not `in unique_ids`?* Searching a list gets slower as it grows; a set stays fast.
**Common mistakes:** Forgetting `strip()`; using `set()` and losing the order; not noticing IDs differing only by case or spaces.

### Q41 ⭐⭐ 🟡 Write code to list all .csv files in a folder using os.listdir or glob.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you find files in a folder, for example before combining monthly files?
**Say this in the interview:** "`glob` with a pattern like `*.csv` is the shortest. With `os.listdir` I get every name and keep the ones ending in .csv."
**Explain simply:**
- `glob.glob("reports/*.csv")` returns paths of files matching the pattern; `*` means "anything".
- `os.listdir("reports")` returns every file and folder name, so you must filter yourself with `endswith(".csv")`.
- Neither promises a sorted order, so wrap in `sorted()` when order matters.
**Sample data:** folder `reports` holds `jan.csv`, `feb.csv`, `notes.txt`.
**Code (what you write in the interview):**
```python
import glob
import os

# option 1: glob with a pattern
print(sorted(glob.glob("reports/*.csv")))

# option 2: os.listdir and filter by ending
csv_files = []
for file_name in os.listdir("reports"):
    if file_name.endswith(".csv"):
        csv_files.append(file_name)
print(sorted(csv_files))
```
**Output:**
```
['reports/feb.csv', 'reports/jan.csv']
['feb.csv', 'jan.csv']
```
**What it means:** Both skip `notes.txt`. `glob` gives the folder path with each name; `listdir` gives bare names.
**Likely follow-ups:**
- *Search sub-folders too?* `glob.glob("reports/**/*.csv", recursive=True)`.
- *Then combine them?* Read each with `pd.read_csv` and join with `pd.concat`.
**Common mistakes:** Forgetting `*.csv` is a pattern, not a regex; using `listdir` and forgetting to add the folder name before opening the file; relying on the order.

### Q42 ⭐ 🟢 What are escape characters such as \n and \t, and when do you use triple-quoted strings?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic string literacy.
**Say this in the interview:** "An escape character is a backslash plus a letter that stands for something you cannot type directly: `\n` is a new line, `\t` is a tab. Triple quotes let me write a string over several lines, handy for long messages or SQL."
**Explain simply:**
- `\n` = new line, `\t` = tab, `\\` = one real backslash, `\'` = a quote inside a quote.
- A normal string must stay on one line. Triple quotes (`"""..."""`) keep line breaks exactly as typed.
- Typical uses: email or letter templates, multi-line SQL queries, doc strings (the description under a function).
**Code (what you write in the interview):**
```python
print("Name\tDept\nAsha\tSales")

message = """Dear Asha,
Your offer letter is attached.
Regards, HR"""
print(message)
```
**Output:**
```
Name	Dept
Asha	Sales
Dear Asha,
Your offer letter is attached.
Regards, HR
```
**What it means:** `\t` made a gap, `\n` started a new line, and the triple-quoted text printed on three lines as typed.
**Likely follow-ups:**
- *Windows paths?* `\n` in 'C:\new' breaks it; use a raw string (Q27).
**Common mistakes:** Writing a Windows path with single backslashes; leaving a triple-quoted string open; expecting `\n` to show literally when printing.

### Q43 ⭐ 🟢 How do you compare two strings ignoring case, and what is the difference between lower() and casefold()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Safe, case-insensitive matching of names or departments.
**Say this in the interview:** "I convert both sides to the same case and compare. `casefold()` is a stronger `lower()` that also handles special characters, like the German ß becoming 'ss'. For plain English names, `lower()` is enough."
**Explain simply:**
- 'Ravi Kumar' and 'RAVI kumar' are the same person but Python says they are different until you align the case.
- `lower()` only makes letters lowercase.
- `casefold()` is built for comparing: it also maps special letters, so 'straße' and 'STRASSE' match.
- Always apply the same method to both strings.
**Code (what you write in the interview):**
```python
name_a = "Ravi Kumar"
name_b = "RAVI kumar"
print(name_a.casefold() == name_b.casefold())

print("straße".lower() == "STRASSE".lower())
print("straße".casefold() == "STRASSE".casefold())
```
**Output:**
```
True
False
True
```
**What it means:** Names match once case is ignored. The last two lines show the only real difference: `lower()` misses the ß case, `casefold()` catches it.
**Likely follow-ups:**
- *In pandas?* `df["name"].str.casefold()` or `.str.lower()`.
**Common mistakes:** Lowercasing only one side; forgetting `strip()` for stray spaces; thinking `casefold` is for display (it is for comparing).

### Q44 ⭐ 🟢 How do you check whether a string is empty or contains only spaces?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Awareness that '   ' is not empty but is still useless data.
**Say this in the interview:** "I strip the spaces first, then test if what is left is empty: `if not text.strip()`. An empty string counts as False in Python."
**Explain simply:**
- `""` is empty. `"   "` has three characters, so `len` is 3, yet it holds no real text.
- `strip()` removes spaces from both ends, turning '   ' into ''.
- `not ''` is True, so the `if` fires for both cases.
- `text.isspace()` is another check, but it returns False for an empty string, so it misses that case.
**Code (what you write in the interview):**
```python
for text in ["", "   ", " Asha "]:
    if not text.strip():
        print(repr(text), "is empty or only spaces")
    else:
        print(repr(text), "has real text")
```
**Output:**
```
'' is empty or only spaces
'   ' is empty or only spaces
' Asha ' has real text
```
**What it means:** Blank and space-only cells are both flagged; a real name with stray spaces is kept.
**Likely follow-ups:**
- *What about None?* `None.strip()` crashes; check `text is None` first.
**Common mistakes:** Using `text == ""` (misses spaces); calling `strip()` on None or a number.

### Q45 ⭐ 🟡 What is the difference between greedy and non-greedy regex matching, for example .* and .*?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know why a pattern sometimes grabs far too much text?
**Say this in the interview:** "`.*` is greedy: it matches as much as it can, so it runs to the last possible end. `.*?` is non-greedy (lazy): it stops at the first possible end."
**Explain simply:**
- A regex (regular expression) is a pattern for finding text.
- `.` means any character, `*` means "as many as possible, including none".
- Adding `?` after the `*` flips it to "as few as possible".
- Example: between `<b>` and `</b>`, greedy grabs from the first `<b>` to the last `</b>`; non-greedy gives each bold word separately.
**Code (what you write in the interview):**
```python
import re

text = "<b>Asha</b> and <b>Ravi</b>"

print(re.findall(r"<b>.*</b>", text))
print(re.findall(r"<b>.*?</b>", text))
```
**Output:**
```
['<b>Asha</b> and <b>Ravi</b>']
['<b>Asha</b>', '<b>Ravi</b>']
```
**What it means:** Greedy returned one big chunk; non-greedy returned the two separate pieces, which is usually what you want.
**Likely follow-ups:**
- *Other non-greedy forms?* `+?` and `??` work the same way.
**Common mistakes:** Using `.*` between two markers and capturing everything in between; forgetting the `r` before the pattern string.

### Q46 ⭐ 🟡 Write a regex with capture groups to pull the currency and amount out of 'INR 45000'.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use `()` groups to pull separate parts out of one text?
**Say this in the interview:** "I put parentheses around each part I want: three capital letters for the currency, digits for the amount. `search` finds it and `group(1)`, `group(2)` give me each part."
**Explain simply:**
- Parentheses `( )` make a capture group, a part of the match you can pull out on its own.
- `[A-Z]{3}` = exactly three capital letters. `\s*` = zero or more spaces. `\d+` = one or more digits.
- `group(0)` is the whole match; `group(1)` and `group(2)` are the first and second brackets.
- `re.search` returns None if nothing matches, so check before using it.
**Code (what you write in the interview):**
```python
import re

text = "INR 45000"
match = re.search(r"([A-Z]{3})\s*(\d+)", text)

if match:
    currency = match.group(1)
    amount = int(match.group(2))
    print(currency, amount)
```
**Output:**
```
INR 45000
```
**What it means:** The currency stays text ('INR') and the amount became a real number (45000) that you can add up.
**Likely follow-ups:**
- *Amounts like '45,000.50'?* Use `([\d,]+\.?\d*)` and remove commas before converting.
- *Name the groups?* `(?P<currency>[A-Z]{3})` then `match.group("currency")`.
**Common mistakes:** Forgetting the `if match` check (None crashes); leaving the amount as a string; forgetting the `r` prefix.

### Q47 ⭐ 🟡 How do you read a very large text file without loading it all into memory?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know to loop over the file (one line at a time) instead of `read()` or `readlines()`?
**Say this in the interview:** "I loop directly over the file object. Python then reads one line at a time, so memory stays small however big the file is. In pandas I use `chunksize`."
**Explain simply:**
- `file.read()` and `file.readlines()` load everything into memory at once; a 5 GB file can crash a laptop.
- `for line in file:` is lazy: it fetches the next line only when needed.
- Keep running totals (counters) instead of storing every line.
- For CSV analysis, `pd.read_csv(path, chunksize=100000)` gives you the file in pieces.
**Sample data:** `ids.txt` has 6 lines (E101, E102, E101, E103, E102, E104).
**Code (what you write in the interview):**
```python
total_lines = 0
e101_count = 0

with open("ids.txt") as file:
    for line in file:  # reads one line at a time
        total_lines += 1
        if line.startswith("E101"):
            e101_count += 1

print(total_lines, e101_count)
```
**Output:**
```
6 2
```
**What it means:** The file has 6 lines and E101 appears twice, found without ever holding the whole file in memory.
**Alternative:** `for chunk in pd.read_csv("big.csv", chunksize=100000):` then process each chunk (from memory, not run here).
**Likely follow-ups:**
- *Why not `readlines()`?* It builds a full list of lines in memory.
**Common mistakes:** Using `read()` on a huge file; appending every line to a list "to process later".

### Q48 ⭐ 🟡 How do you define and use a custom exception class, and when is it worth it in an analyst script?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know how to name your own errors so they are clear and catchable on their own?
**Say this in the interview:** "A custom exception is a small class that inherits from `Exception`. I raise it for a business rule, like an invalid salary, and catch it by name. It is worth it in a longer pipeline where I need to tell 'bad data' apart from a real bug."
**Explain simply:**
- A class is a blueprint; here the blueprint just gives your error its own name: `class InvalidSalaryError(Exception): pass`.
- `raise` triggers it; `except InvalidSalaryError` catches only that kind.
- Built-in errors like `ValueError` are fine for one-off scripts. A custom one pays off when many checks exist and you want to handle data problems differently from code bugs.
**Code (what you write in the interview):**
```python
class InvalidSalaryError(Exception):
    pass


def check_salary(salary):
    if salary <= 0:
        raise InvalidSalaryError(f"Salary must be positive, got {salary}")
    return salary


try:
    check_salary(-500)
except InvalidSalaryError as error:
    print("Skipping row:", error)
```
**Output:**
```
Skipping row: Salary must be positive, got -500
```
**What it means:** The bad value triggered our own named error with a readable message, and the script handled it and moved on.
**Likely follow-ups:**
- *Why inherit from Exception, not BaseException?* `BaseException` includes things like Ctrl+C that you should not catch.
**Common mistakes:** Making a custom error for every tiny case; inheriting from the wrong class; using it where a plain `ValueError` would do.

### Q49 ⭐ 🟡 When do you use assert, and how does it differ from raising an exception?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you separate "checking my own work" from "handling bad input"?
**Say this in the interview:** "`assert` is a sanity check for something that must be true if my code is right, like 'row count matches the report'. It stops the script loudly when wrong. For bad user or file data I raise a proper exception, because asserts can be switched off."
**Explain simply:**
- `assert condition, "message"` does nothing if the condition is True; if False it raises `AssertionError` with your message.
- Use it for internal checks while building a pipeline: totals match, no duplicate IDs, no missing keys.
- Do not use it to validate outside data. Running Python with the `-O` flag removes all asserts, so the check silently disappears (from memory, not run here).
- `raise` is for expected problems you want to catch and handle; `assert` is for "this should never happen".
**Code (what you write in the interview):**
```python
employees = [{"id": "E101"}, {"id": "E102"}, {"id": "E103"}]
headcount_report = 3

# sanity check on our own work: stops loudly if wrong
assert len(employees) == headcount_report, "Headcount does not match the report"
print("check passed")

employees.pop()
assert len(employees) == headcount_report, "Headcount does not match the report"
```
**Output:**
```
check passed
Traceback (most recent call last):
  ...
AssertionError: Headcount does not match the report
```
(The traceback file path line is trimmed here with `...`.)
**What it means:** The first check passed silently. After we removed an employee the numbers disagreed, so the script stopped with our message instead of producing a wrong report.
**Likely follow-ups:**
- *Assert or ValueError for a negative salary in a file?* ValueError (or a custom error), since file data is outside input.
**Common mistakes:** Using assert to validate user input; putting code with side effects inside the assert; leaving off the message.

### Q50 ⭐ 🔴 What is a context manager, and how would you write one with __enter__ and __exit__ (or contextlib)?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Do you understand what `with` really does (setup, then guaranteed cleanup)?
**Say this in the interview:** "A context manager is anything used after `with`. Python calls `__enter__` at the start and `__exit__` at the end, even if an error happens. `with open(...)` is the everyday example. I can write my own as a class, or more briefly with `contextlib.contextmanager`."
**Explain simply:**
- `with` guarantees cleanup: file closed, connection released, timer stopped.
- Class way: `__enter__` does setup, `__exit__` does cleanup. If `__exit__` returns False, any error still reaches you (it is not hidden).
- `contextlib` way: write a generator function (a function using `yield`) with `@contextmanager`; code before `yield` is setup, code after is cleanup. Put `yield` inside `try/finally` so cleanup still runs on errors.
- Analyst uses: timing a slow step, opening and closing a database connection, temporarily changing a setting.
**Code (what you write in the interview):**
```python
class Timer:
    def __enter__(self):
        print("Starting")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Finished (runs even if there was an error)")
        return False  # do not hide errors


with Timer():
    print("Processing payroll file")
```
**Output:**
```
Starting
Processing payroll file
Finished (runs even if there was an error)
```
**What it means:** The "Starting" and "Finished" lines wrap the work automatically, which is the same promise `with open()` makes to close a file.
**Alternative:** With contextlib (checked by running; same wrapping output with "Finished"):
```python
from contextlib import contextmanager


@contextmanager
def timer():
    print("Starting")
    try:
        yield
    finally:
        print("Finished")


with timer():
    print("Processing payroll file")
```
**Likely follow-ups:**
- *What are the three `__exit__` arguments?* The error type, value and traceback if one happened, else None.
- *What if `__exit__` returns True?* The error is swallowed; avoid that unless intended.
**Common mistakes:** Forgetting `return self` in `__enter__` when you need `as name`; skipping `try/finally` in the contextlib version; returning True from `__exit__` and hiding real bugs.

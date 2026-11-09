# Book 3 — Python & pandas for Analysts | Part 11: Jupyter, APIs, Excel Automation, Using AI Assistants Correctly 🟡

**Target:** 40 questions | **Actual:** 48 questions
**Scope:** Jupyter notebook basics, calling APIs and handling JSON, Python-driven Excel automation with pandas and openpyxl, and using AI assistants safely for analysis code.

### Q1 ⭐⭐⭐ 🟢 What is a Jupyter Notebook, and why do data analysts use it?
**Asked at:** commonly asked (no company-specific report found); Jupyter basics appear in prep lists such as InterviewPrep and ClimbTheLadder (snippet only).
**What the interviewer is checking:** Do you know what a notebook is and why it suits analysis work.
**Say this in the interview:** "A Jupyter Notebook is a document where I write Python in small blocks, run them one at a time, and see the table or chart right below. I use it to explore data and explain my steps in the same place."
**Explain simply:**
- **Notebook:** one file (`.ipynb`) holding code, results, charts and written notes together.
- **Cell:** one block. You run it alone and see its output straight away.
- **Why analysts like it:** you can try an idea, look at the result, fix it and move on, without re-running everything.
- **Why managers like it:** the file shows the steps, the numbers and the explanation, so others can follow the reasoning.
- Think of it as Excel's "see it instantly" feel, but with code that can handle far more rows.
**What it means:** it is a workbench for exploring data and showing your working.
**Likely follow-ups:**
- *Any downside?* Cells can be run in any order, which can give wrong results (see Q26).
- *What would you use for a daily automatic job?* A `.py` script (see Q27).
**Common mistakes:** saying it is "a programming language" (it is a tool that runs Python), or treating it as the right place for scheduled jobs.

### Q2 ⭐⭐⭐ 🟢 How do you use ChatGPT or another AI assistant to help you write pandas code?
**Asked at:** commonly asked (no company-specific report found); DataCamp's 2026 interview prep says candidates are expected to validate AI-assisted output (snippet only).
**What the interviewer is checking:** Do you use AI as a helper you control, not a source you trust blindly.
**Say this in the interview:** "I describe my table and the goal in plain words, using column names and a few fake rows, never real employee data. Then I read the code, run it on a small sample, and check the answer by hand before I use it."
**Explain simply:**
- **Give context:** column names, data types, what each row means, what result I want (see Q16).
- **Use fake or masked sample rows:** protect employee data (see Q17).
- **Ask for explanation:** "explain each line" helps me learn and catch mistakes.
- **Review and test:** run on a small sample, compare with a manual count (see Q3 and Q8).
- **Good uses:** syntax I forgot, error messages, first drafts, explaining unfamiliar code.
**What it means:** AI speeds up typing; I remain responsible for the numbers.
**Likely follow-ups:**
- *Would you paste your whole file?* No, see Q17.
- *What if it gives an error?* Paste the error message (no real data) and ask what it means, then read the fix before applying it.
**Common mistakes:** copying code straight into a report, sharing real salaries or names, or asking vague questions like "analyse my data".

### Q3 ⭐⭐⭐ 🟢 What are the risks of using AI-generated Python code, and how do you check it before trusting it?
**Asked at:** commonly asked (no company-specific report found); an AI-code verification question appears on PracHub's question bank (snippet only).
**What the interviewer is checking:** Do you know AI code can run without error and still be wrong, and do you have a checking routine.
**Say this in the interview:** "The big risk is code that runs and looks fine but gives a wrong number. So I read it line by line, test on a tiny table where I know the answer, check edge cases, and compare the total with Excel or a manual count."
**Explain simply:**
- **Wrong logic:** for example dividing by the wrong headcount, or averaging averages.
- **Hallucination:** AI invents a function or option that does not exist (see Q31).
- **Outdated code:** uses old pandas methods that were removed or changed.
- **Silent data issues:** blanks, duplicates and text-typed numbers are ignored without warning.
- **Privacy:** pasting real employee data into a public tool leaks it.
- **How I check:** read each line; run on 5 rows I can verify by hand; compare row counts and totals before and after; try blanks and duplicates; confirm against a second method.
**What it means:** "it ran" is not proof; "it matches my manual check" is.
**Likely follow-ups:**
- *What is the quickest check?* Compare one department's number with a hand calculation.
- *Would you still use AI?* Yes, for drafts and syntax, never as the final judge.
**Common mistakes:** trusting code because there is no error message, and testing only on the full real file where you cannot see mistakes.

### Q4 ⭐⭐⭐ 🟢 What is the difference between a code cell and a Markdown cell in Jupyter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic notebook literacy.
**Say this in the interview:** "A code cell holds Python that runs and shows output. A Markdown cell holds formatted text, like headings and notes, which I use to explain what the code does."
**Explain simply:**
- **Code cell:** you write Python; running it shows the result below (a table, number or chart).
- **Markdown cell:** plain text with simple symbols, such as `# Title` for a heading and `- item` for a bullet. Running it just displays the formatted text.
- **Why both:** code gives the answer, Markdown gives the story (purpose, assumptions, conclusions).
- A third type, "Raw", is plain text that is never formatted or run; rarely used.
**What it means:** code cells calculate, Markdown cells communicate.
**Likely follow-ups:**
- *How do you switch the type?* In command mode press `M` for Markdown and `Y` for code (see Q10).
**Common mistakes:** typing notes inside a code cell (it causes a syntax error) or forgetting to run a Markdown cell so it still shows raw symbols.

### Q5 ⭐⭐⭐ 🟡 What does "Restart kernel and run all" do, and why should you do it before sharing a notebook?
**Asked at:** commonly asked (no company-specific report found); a 2025 academic study on notebook use discusses "restart and run all" (snippet only).
**What the interviewer is checking:** Do you know how to prove a notebook works from top to bottom.
**Say this in the interview:** "It clears Python's memory and then runs every cell in order from the top. I do it before sharing so I know the notebook gives the same results for someone else, not just on my machine with leftover variables."
**Explain simply:**
- **Kernel:** the Python engine behind the notebook that remembers your variables (see Q9).
- **Restart:** wipes that memory, so old variables and deleted cells' leftovers vanish.
- **Run all:** runs cells top to bottom in order.
- **Why it matters:** if a cell depended on something you ran earlier but later deleted, it now fails, and you find the problem before your colleague does.
- It also removes stale outputs that no longer match the code.
**What it means:** it is the "does it really work from scratch?" test.
**Likely follow-ups:**
- *Will it lose my data?* It loses variables in memory, not your files. Reloading data is part of the notebook.
- *What if a cell is slow?* Fine; that is still better than shipping a broken notebook.
**Common mistakes:** sharing without doing it, so the file only works in your session.

### Q6 ⭐⭐⭐ 🟡 Write code to combine all the monthly Excel files in a folder into one DataFrame and add a column showing the source file name.
**Asked at:** commonly asked (no company-specific report found); a Glassdoor candidate report mentions pandas with Excel files (snippet only, employer not seen).
**What the interviewer is checking:** Loop over files, read each, tag it, stack with `concat`.
**Say this in the interview:** "I list the files with `glob`, read each one with `read_excel`, add a `source_file` column, collect them in a list and stack them with `pd.concat`."
**Explain simply:**
- **glob:** finds file names that match a pattern, like `*.xlsx`.
- **concat:** stacks tables on top of each other (same columns).
- **Source column:** keeps track of which month each row came from.
- **ignore_index=True:** renumbers rows 0, 1, 2... instead of repeating each file's numbers.
**Sample data:** three small files, `attendance_jan.xlsx`, `attendance_feb.xlsx` and `attendance_mar.xlsx` in a folder called `monthly_files`, each with `employee_id` and `days_present`.
**Code (what you write in the interview):**
```python
import glob
import os
import pandas as pd

# find every Excel file in the folder
file_paths = sorted(glob.glob("monthly_files/*.xlsx"))

monthly_tables = []
for file_path in file_paths:
    one_month = pd.read_excel(file_path)
    # remember which file each row came from
    one_month["source_file"] = os.path.basename(file_path)
    monthly_tables.append(one_month)

# stack all tables into one DataFrame
all_months = pd.concat(monthly_tables, ignore_index=True)
print(all_months)
```
**Output:**
```
   employee_id  days_present          source_file
0          101            21  attendance_feb.xlsx
1          102            19  attendance_feb.xlsx
2          104            17  attendance_feb.xlsx
3          101            20  attendance_jan.xlsx
4          102            18  attendance_jan.xlsx
5          103            22  attendance_jan.xlsx
6          101            22  attendance_mar.xlsx
7          103            20  attendance_mar.xlsx
8          104            18  attendance_mar.xlsx
```
**What it means:** nine rows from three files in one table, each row labelled with its file. `sorted` orders names alphabetically (feb before jan), not by calendar; sort the month column later if order matters.
**Likely follow-ups:**
- *What if column names differ between files?* `concat` makes extra columns full of blanks; rename columns to match first.
- *What if there are CSVs too?* Use `pd.read_csv` and a `*.csv` pattern.
- *Skip temporary files?* Excel lock files start with `~$`; filter them out.
**Common mistakes:** calling `concat` inside the loop (slow), forgetting `ignore_index`, and not checking that every file has the same columns.

### Q7 ⭐⭐⭐ 🟡 How would you automate a monthly HR attendance report in Python so it is produced without manual Excel work?
**Asked at:** commonly asked (no company-specific report found); MIS automation job descriptions in our JD sample mention Python reporting (internal research).
**What the interviewer is checking:** Can you break a manual report into repeatable steps: read, clean, calculate, save, schedule.
**Say this in the interview:** "I write the steps once as a script: read the month's file, clean it, calculate attendance percentage, and save a formatted Excel report. Then I schedule it to run each month, and I add checks so a bad input stops the job instead of sending a wrong report."
**Explain simply:**
- **Step 1, read:** pull the raw attendance files from a fixed folder.
- **Step 2, clean:** fix dates, remove duplicates, handle blanks.
- **Step 3, calculate:** attendance percentage, absentees, department totals.
- **Step 4, save:** write the report to Excel with formatting (see Q38).
- **Step 5, check:** row counts and totals match the source, otherwise stop and alert someone.
- **Step 6, schedule:** run automatically (see Q43).
**Sample data:** one month of attendance, three employees, 22 working days.
**Code (what you write in the interview):**
```python
import pandas as pd

# 1. read the raw attendance file
attendance = pd.read_excel("monthly_files/attendance_jan.xlsx")

# 2. calculate: attendance percentage out of 22 working days
attendance["attendance_pct"] = (attendance["days_present"] / 22 * 100).round(1)

# 3. save the finished report
attendance.to_excel("attendance_report.xlsx", index=False)
print(attendance)
```
**Output:**
```
   employee_id  days_present  attendance_pct
0          101            20            90.9
1          102            18            81.8
2          103            22           100.0
```
**What it means:** the same few lines can be rerun every month with no manual copying; this is the core, and in real life I would add cleaning, checks and formatting.
**Likely follow-ups:**
- *How does the next month's file get picked up?* Build the file name from the month, or take the newest file in the folder.
- *What if the input is wrong?* Check columns and row counts first and stop with a clear message.
**Common mistakes:** automating without validation checks, hard-coding the 22 working days, and not keeping a copy of the input used.

### Q8 ⭐⭐⭐ 🟡 You ask an AI assistant for code that calculates attrition rate by department, and the output looks wrong. How do you debug and verify it?
**Asked at:** commonly asked (no company-specific report found); verifying AI-assisted analysis is a recurring interview theme (Microsoft Research study, snippet only).
**What the interviewer is checking:** A calm, step-by-step check: definition, inputs, small test, manual comparison.
**Say this in the interview:** "First I agree on the definition: leavers divided by headcount. Then I check the inputs, test one department by hand, and compare with the code's number. Usually the problem is the denominator, duplicates, or text values like 'Yes' not matching."
**Explain simply:**
- **Attrition rate:** people who left divided by people counted, as a percentage (often average headcount in real reports).
- **Check the definition:** did the AI divide by the right number?
- **Check the inputs:** duplicate employees, blank departments, "yes" vs "Yes", extra spaces.
- **Test one group by hand:** count leavers and headcount for one department and compare.
- **Then fix the code** and rerun; do not just ask AI again blindly.
**Sample data:** six employees in three departments; `left_company` says Yes or No.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_excel("employees.xlsx")

# 1 if the person left, 0 if still here
employees["left_flag"] = (employees["left_company"] == "Yes").astype(int)

# attrition rate = leavers / headcount, per department
attrition = employees.groupby("department")["left_flag"].mean() * 100
print(attrition.round(1))

# manual check on one department
sales = employees[employees["department"] == "Sales"]
print(len(sales), sales["left_flag"].sum())
```
**Output:**
```
department
HR         0.0
IT       100.0
Sales     50.0
Name: left_flag, dtype: float64
2 1
```
**What it means:** Sales has 2 people and 1 leaver, which is 50 percent, matching the table. The manual check agrees, so I trust this logic; if it disagreed I would look at the definition and the data first.
**Likely follow-ups:**
- *Why does the mean work?* The mean of 0s and 1s is the share of 1s.
- *What if the AI used a different denominator?* Ask what the company's definition is (opening headcount or average headcount) and match it.
**Common mistakes:** not agreeing on the definition, ignoring duplicates and blanks, and checking only the code, not the data.

### Q9 ⭐⭐ 🟢 What is a kernel in Jupyter, and what happens when you restart it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the kernel holds memory, not files.
**Say this in the interview:** "The kernel is the Python engine running behind the notebook. It remembers my variables. When I restart it, that memory is wiped, but my notebook file and data files stay as they are."
**Explain simply:**
- **Kernel:** the running Python process that executes your cells.
- **Memory:** variables like `employees` live in the kernel, not in the file.
- **Restart:** clears all variables and imports; you must rerun the cells.
- **Interrupt:** stops a long-running cell without clearing memory.
- **When to restart:** the notebook is stuck, memory is full, or you want a clean test (see Q5).
**What it means:** restart = fresh Python session, same notebook file.
**Likely follow-ups:**
- *Does restart delete the outputs?* Not unless you choose "clear outputs".
**Common mistakes:** thinking a restart deletes the notebook or the data files, or forgetting to rerun the import cell afterwards.

### Q10 ⭐⭐ 🟢 What are the Jupyter keyboard shortcuts you use most often (run cell, add cell above or below, delete cell, switch to Markdown)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Real hands-on use.
**Say this in the interview:** "Shift+Enter runs a cell and moves on. In command mode, A adds a cell above, B below, D D deletes, M switches to Markdown and Y back to code. Esc enters command mode."
**Explain simply:**
- **Two modes:** edit mode (typing in the cell, green border) and command mode (cell selected, blue border; press Esc).
- **Shift+Enter:** run cell and select the next one.
- **Ctrl+Enter:** run cell and stay on it.
- **A / B:** insert cell above / below (command mode).
- **D, D:** delete the selected cell (press D twice).
- **M / Y:** change cell to Markdown / code.
- **Z:** undo a cell deletion.
**What it means:** these few keys let me work without the mouse. In JupyterLab and VS Code the shortcuts are mostly the same (from memory, unverified).
**Likely follow-ups:**
- *Where do you see all shortcuts?* Command mode, press H.
**Common mistakes:** pressing A or D while still in edit mode (it types letters instead), which confuses beginners.

### Q11 ⭐⭐ 🟢 How do you install a Python library such as openpyxl, and how do you install it from inside a Jupyter notebook?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know `pip install` and the notebook version.
**Say this in the interview:** "In a terminal I run `pip install openpyxl`. Inside a notebook I run `%pip install openpyxl` in a cell, because that installs into the same Python the notebook is using. Then I `import` it."
**Explain simply:**
- **Library:** extra code someone else wrote, such as `openpyxl` for Excel files.
- **pip:** Python's installer for libraries.
- **Terminal:** `pip install openpyxl`.
- **Notebook:** `%pip install openpyxl` (the `%` makes sure it targets the notebook's own Python). `!pip install openpyxl` often works too, but may install into a different Python.
- **After installing:** run `import openpyxl`; if the notebook was already using an older copy, restart the kernel.
- **Anaconda users:** `conda install openpyxl` also works.
**What it means:** install once, import every time you use it.
**Likely follow-ups:**
- *How do you check what is installed?* `pip list` or `pip show openpyxl`.
- *Why use a virtual environment?* See Q36.
**Common mistakes:** installing in one Python and running another (so "module not found" persists), and forgetting to restart the kernel.

### Q12 ⭐⭐ 🟢 What is an API, explained simply for a non-technical person?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you explain a technical idea in plain words.
**Say this in the interview:** "An API is like a waiter in a restaurant. I do not walk into the kitchen; I ask the waiter for something, and the waiter brings it back. In the same way my code asks another system, for example an HR system, for data, and it replies in a set format."
**Explain simply:**
- **API:** a set of rules for one program to ask another program for data or actions.
- **Request:** my question, sent to a web address (URL).
- **Response:** the answer, usually in JSON (see Q14).
- **Why analysts care:** pull fresh data automatically instead of downloading files by hand.
- **Example:** fetch today's exchange rate, or list employees from an HR system.
**What it means:** it is a safe, controlled doorway to someone else's data.
**Likely follow-ups:**
- *Do you always need a key?* Many APIs need an API key or token to know who is asking (see Q40).
**Common mistakes:** giving a definition full of jargon, or confusing an API with a database.

### Q13 ⭐⭐ 🟢 How do you fetch data from a REST API in Python using the requests library?
**Asked at:** commonly asked (no company-specific report found); the `requests` then `.json()` then DataFrame pattern is common in tutorials (likegeeks, snippet only).
**What the interviewer is checking:** The basic call: `get`, check status, read JSON.
**Say this in the interview:** "I call `requests.get(url, timeout=10)`, check the call worked with `raise_for_status()`, and read the data with `.json()`."
**Explain simply:**
- **REST API:** an API you call with a normal web address and standard actions; `GET` means "give me data".
- **requests:** the Python library for making these calls (`pip install requests`).
- **timeout:** stops the code waiting forever if the server is slow.
- **raise_for_status():** raises an error if the server replied with a failure code (see Q21).
- **.json():** turns the reply into Python dictionaries and lists.
**Sample data:** the live API call was not run here (no real service). I served a small local file `employees.json` at `http://localhost:8000` and ran the same code against it; with a real API you only change the URL (and add an API key, see Q40).
**Code (what you write in the interview):**
```python
import requests

url = "http://localhost:8000/employees.json"
response = requests.get(url, timeout=10)

# stop with a clear error if the call failed
response.raise_for_status()

data = response.json()
print(response.status_code)
print(data)
```
**Output:**
```
200
{'employees': [{'id': 1, 'name': 'Asha', 'department': 'HR'}, {'id': 2, 'name': 'Ravi', 'department': 'IT'}]}
```
**What it means:** status 200 means success, and `data` is now a Python dictionary I can turn into a DataFrame (see Q19).
**Likely follow-ups:**
- *How do you send filters?* Use `params={"department": "HR"}`.
- *How do you handle failures?* See Q21.
**Common mistakes:** no `timeout`, not checking the status, and putting the API key in the code (see Q40).

### Q14 ⭐⭐ 🟢 What is JSON, and how does it differ from a CSV file?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Nested versus flat data.
**Say this in the interview:** "JSON is a text format of labelled values that can be nested, so one employee can hold a list of skills. CSV is a flat table of rows and columns. APIs usually send JSON; CSV is easier for Excel and pandas."
**Explain simply:**
- **JSON:** `{"name": "Asha", "skills": ["Excel", "SQL"]}`; keys and values, with lists and nested objects allowed. It maps to Python dictionaries and lists.
- **CSV:** each line is a row, values separated by commas; every row has the same columns.
- **Difference:** JSON handles nested, uneven data; CSV is flat, smaller and simpler.
- **Converting:** nested JSON must be flattened before it fits a table (see Q20).
**Code (what you write in the interview):**
```python
import json
import pandas as pd

# JSON: nested, one employee holds a list of skills
employee_json = '{"id": 1, "name": "Asha", "skills": ["Excel", "SQL"]}'
employee = json.loads(employee_json)
print(employee["skills"][0])

# CSV: flat rows and columns only
flat_table = pd.DataFrame({"id": [1, 2], "name": ["Asha", "Ravi"]})
print(flat_table.to_csv(index=False))
```
**Output:**
```
Excel
id,name
1,Asha
2,Ravi

```
**What it means:** JSON keeps the skills list inside one employee; CSV has no place for that without extra columns or rows.
**Likely follow-ups:**
- *Which is smaller?* CSV, because JSON repeats the key names.
**Common mistakes:** saying JSON is "a file only for websites", or forgetting JSON keys are always text in quotes.

### Q15 ⭐⭐ 🟢 What is the difference between openpyxl and pandas when working with Excel files?
**Asked at:** commonly asked (no company-specific report found); the DataCamp Python Excel tutorial describes this split (snippet only).
**What the interviewer is checking:** Do you pick the right tool: tables versus cells and formatting.
**Say this in the interview:** "pandas treats a sheet as a table of data: read it, calculate, write it back. openpyxl works on the workbook itself: individual cells, formulas, fonts, colours, column widths. pandas actually uses openpyxl underneath to read and write `.xlsx`."
**Explain simply:**
- **pandas:** best for analysis; one line to read a sheet into a DataFrame and one to save.
- **openpyxl:** best for editing a specific cell, adding formulas, and formatting.
- **Together:** pandas does the calculations, openpyxl polishes the final report.
- **Limit:** pandas does not keep formatting or formulas when it rewrites a file; openpyxl keeps what it can but does not calculate formula results.
**Sample data:** `employees.xlsx` with six employees.
**Code (what you write in the interview):**
```python
import pandas as pd
from openpyxl import load_workbook

# pandas: read the whole sheet as a table, then calculate
employees = pd.read_excel("employees.xlsx")
print(employees["department"].value_counts())

# openpyxl: open the workbook and change one cell directly
workbook = load_workbook("employees.xlsx")
sheet = workbook.active
sheet["B2"] = "Sales Team"
workbook.save("employees_edited.xlsx")
print(sheet["B2"].value)
```
**Output:**
```
department
Sales    2
HR       2
IT       2
Name: count, dtype: int64
Sales Team
```
**What it means:** pandas answered "how many per department"; openpyxl changed one cell. Different jobs.
**Likely follow-ups:**
- *Which for a formatted report?* pandas to write the data, then openpyxl to format (see Q38).
**Common mistakes:** using openpyxl to analyse thousands of rows cell by cell, or expecting pandas to preserve formatting.

### Q16 ⭐⭐ 🟢 What information should you give an AI assistant in a prompt to get useful pandas code?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you write a clear, safe, specific prompt.
**Say this in the interview:** "I give it the goal, the column names and types, three fake sample rows, the exact output I want, my pandas version, and any rules like how blanks should be treated. I never include real employee data."
**Explain simply:**
- **Goal:** "attrition rate by department as a percentage."
- **Data description:** column names, data types, what one row means (one employee, one day).
- **Fake sample rows:** three made-up rows so it sees the shape.
- **Expected output:** columns I want, rounded how, sorted how.
- **Rules:** treat blanks as zero? Which status counts as "left"? Use the company definition.
- **Environment:** Python and pandas version, so it does not use removed functions.
- **Ask for:** short code with comments and a line-by-line explanation.
**Example prompt:** "I have a pandas DataFrame `employees` with columns employee_id (int), department (text), left_company ('Yes'/'No'). Sample rows: (1, 'Sales', 'Yes'), (2, 'Sales', 'No'), (3, 'HR', 'No'). Give me code that returns attrition rate as a percentage per department, rounded to 1 decimal, sorted highest first. Use pandas 2.x. Add comments."
**What it means:** a precise prompt gets code close to correct; a vague prompt gets guesses.
**Likely follow-ups:**
- *Why fake rows?* To protect privacy (see Q17).
**Common mistakes:** vague prompts ("analyse my data"), leaving out column names, pasting real data, and not stating the output format.

### Q17 ⭐⭐ 🟢 Should you paste real employee data such as salaries or names into a public AI tool? What is the safe alternative?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand that employee data is confidential and you can still use AI help safely.
**Say this in the interview:** "No. Salaries and names are personal data, and a public tool sends them outside the company. I would share only the column names, a few made-up rows, or an anonymised sample, and ask for code. I run that code myself on the real file."
**Explain simply:**
- Public AI tools send your text to an outside company's servers. Once pasted, you cannot take it back, and it may break company policy or data-protection law.
- The AI does not need real data to write code. It needs the structure: column names, data types, and what you want.
- Safe options: (1) describe the columns in words; (2) paste 3 to 5 invented rows; (3) anonymise a real sample (drop names, replace IDs, turn exact salary into a band); (4) use a company-approved AI tool, if IT has provided one.
- Always run the AI's code on the real file on your own machine, not inside the chat.
**Sample data:** `employees.csv` with employee_id, name, department, monthly_salary, status (5 rows, as in Q18).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("employees.csv")

# Drop names and replace real IDs with dummy ones
safe_employees = employees.drop(columns=["name"])
safe_employees["employee_id"] = range(1, len(safe_employees) + 1)

# Replace exact salary with a band
safe_employees["salary_band"] = pd.cut(
    safe_employees["monthly_salary"],
    bins=[0, 45000, 55000, 100000],
    labels=["Low", "Medium", "High"],
)
safe_employees = safe_employees.drop(columns=["monthly_salary"])
print(safe_employees)
```
**Output:**
```
   employee_id department  status salary_band
0            1         HR  Active         Low
1            2      Sales    Left      Medium
2            3      Sales  Active      Medium
3            4    Finance  Active        High
4            5         HR    Left         Low
```
**What it means:** No name, no real ID, no exact pay is left, yet the table still has the shape the AI needs to write correct code.
**Likely follow-ups:**
- *Is anonymising enough?* Not always. A rare combination (one Finance manager in a small city) can still identify someone, so keep the sample small and check company policy.
- *Who decides what is allowed?* The company's data-protection or IT policy; ask if unsure.
**Common mistakes:** Pasting "just one row" of real data; pasting a file "to check it quickly"; thinking deleting the name is enough when employee ID and salary still point to one person.

### Q18 ⭐⭐ 🟢 How do you read a CSV file in a notebook and quickly check its shape, columns and first rows?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic pandas fluency: load a file and inspect it before doing anything else.
**Say this in the interview:** "I load it with `pd.read_csv`, then check `shape` for rows and columns, `columns` for names, and `head()` for the first rows, so I know what I am working with."
**Explain simply:**
- A CSV is a plain text file where each line is a row and commas separate the columns.
- `shape` gives (number of rows, number of columns).
- `columns` lists the column names; spelling and extra spaces matter later.
- `head()` shows the first 5 rows by default; `head(10)` shows 10.
**Sample data:** `employees.csv`

| employee_id | name | department | monthly_salary | status |
|---|---|---|---|---|
| 101 | Asha | HR | 45000 | Active |
| 102 | Ravi | Sales | 52000 | Left |
| 103 | Meena | Sales | 48000 | Active |
| 104 | Karan | Finance | 60000 | Active |
| 105 | Divya | HR | 41000 | Left |

**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("employees.csv")

print(employees.shape)
print(employees.columns.tolist())
print(employees.head())
```
**Output:**
```
(5, 5)
['employee_id', 'name', 'department', 'monthly_salary', 'status']
   employee_id   name department  monthly_salary  status
0          101   Asha         HR           45000  Active
1          102   Ravi      Sales           52000    Left
2          103  Meena      Sales           48000  Active
3          104  Karan    Finance           60000  Active
4          105  Divya         HR           41000    Left
```
**What it means:** 5 employees and 5 columns, and the data looks as expected.
**Alternative:** `employees.info()` also shows column types and how many values are missing.
**Likely follow-ups:**
- *File uses semicolons or another encoding?* Use `sep=";"` or `encoding="latin-1"`.
- *Dates?* Add `parse_dates=["join_date"]`.
**Common mistakes:** Writing `employees.shape()` with brackets (it is not a function); not checking the file path, which gives FileNotFoundError; skipping the check and finding wrong types later.

### Q19 ⭐⭐ 🟡 How do you convert a JSON response from an API into a pandas DataFrame?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the flow: API response, Python list of dictionaries, DataFrame.
**Say this in the interview:** "I call `response.json()` to turn the reply into Python lists and dictionaries. If it is a list of records, `pd.DataFrame(records)` gives me the table directly."
**Explain simply:**
- JSON is text in a standard format: `{"name": "Asha"}` is one record (a dictionary of key and value). A list of those is many records.
- `response.json()` converts that text to Python objects. `json.loads(text)` does the same for text you already hold.
- A list of flat dictionaries maps straight to a DataFrame: each dictionary is a row, each key a column.
- If the records are nested, or hidden under a key like `"data"`, see Q20.
**Sample data:** a mock API reply held as text. **The live API call was not run here**; with a real API the first line would be `records = requests.get(url, timeout=10).json()`.
**Code (what you write in the interview):**
```python
import json
import pandas as pd

# This text is what the API sends back (mock response)
response_text = '[{"employee_id": 101, "name": "Asha", "department": "HR"}, {"employee_id": 102, "name": "Ravi", "department": "Sales"}]'

records = json.loads(response_text)   # with requests this is response.json()
employees = pd.DataFrame(records)
print(employees)
```
**Output:**
```
   employee_id  name department
0          101  Asha         HR
1          102  Ravi      Sales
```
**What it means:** Two records became two rows, ready for filtering and grouping.
**Likely follow-ups:**
- *Reply is `{"data": [...]}`?* Use `pd.DataFrame(reply["data"])`.
- *Nested fields?* `pd.json_normalize` (next question).
**Common mistakes:** Passing the raw `response` object or the raw text string to `DataFrame`; forgetting to check the status first (Q21); not looking at the JSON structure before converting.

### Q20 ⭐⭐ 🟡 How do you flatten nested JSON from an API into a DataFrame using json_normalize?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you can handle realistic API data where records contain records.
**Say this in the interview:** "When a field holds another dictionary, `pd.DataFrame` leaves it as one messy cell. `pd.json_normalize` opens it up into separate columns named like `department.name`."
**Explain simply:**
- Nested means a value is itself a dictionary, for example department with a name and a location inside.
- `json_normalize` flattens each level into its own column and joins the names with a dot.
- For a list hidden under a key, use `record_path="key"` (for example each employee's list of past jobs).
- You can rename the columns afterwards to tidy names.
**Sample data:** two nested records written in the code (mock; no live API call was run).
**Code (what you write in the interview):**
```python
import pandas as pd

records = [
    {"employee_id": 101, "name": "Asha",
     "department": {"name": "HR", "location": "Hyderabad"}, "salary": {"monthly": 45000}},
    {"employee_id": 102, "name": "Ravi",
     "department": {"name": "Sales", "location": "Pune"}, "salary": {"monthly": 52000}},
]

employees = pd.json_normalize(records)
print(employees)
```
**Output:**
```
   employee_id  name department.name department.location  salary.monthly
0          101  Asha              HR           Hyderabad           45000
1          102  Ravi           Sales                Pune           52000
```
**What it means:** Every inner value now has its own column, so I can filter by `department.location` like any other column.
**Likely follow-ups:**
- *Dots in names are awkward?* Rename them: `employees.columns = employees.columns.str.replace(".", "_", regex=False)`.
- *Records missing some keys?* They become NaN (empty).
**Common mistakes:** Using `pd.DataFrame` and being left with dictionaries inside cells; not printing the first record to see the structure; expecting a list inside a record to flatten without `record_path`.

### Q21 ⭐⭐ 🟡 How do you check whether an API request succeeded, and how do you handle a failed request or a timeout?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That your script does not break silently or hang forever when the API misbehaves.
**Say this in the interview:** "I always set a `timeout`, call `raise_for_status()` so error codes become errors, and wrap it in try/except to catch a timeout or a bad status and handle it cleanly."
**Explain simply:**
- Every reply has a status code (200 means OK; 4xx and 5xx mean problems, see Q22).
- `raise_for_status()` does nothing on success and raises an error on 4xx/5xx, so you cannot use bad data by accident.
- Without `timeout`, `requests` can wait forever. A timeout (in seconds) makes it give up.
- try/except means: try this, and if this specific error happens, do the fallback instead of crashing.
**Sample data:** no live API was called here. To run offline I started a tiny local server on my own machine that answers `/ok` with 200, `/missing` with 404 and `/slow` after 3 seconds (that server is test scaffolding, not part of the answer).
**Code (what you write in the interview):**
```python
import requests

def get_employees(url):
    try:
        response = requests.get(url, timeout=2)   # never wait forever
        response.raise_for_status()               # error for 401, 404, 429, 500...
        return response.json()
    except requests.exceptions.Timeout:
        print("Request timed out, try again later")
    except requests.exceptions.HTTPError as error:
        print("API returned an error:", error.response.status_code)
    return None
```
**Output:** (calling it for the three local test URLs)
```
ok -> [{'employee_id': 101}]
API returned an error: 404
missing -> None
Request timed out, try again later
slow -> None
```
**What it means:** Success returns data; a 404 and a timeout are reported and return `None` instead of crashing the report.
**Alternative:** For temporary problems (timeout, 429, 500), retry 2 or 3 times with a pause (`time.sleep`) before giving up.
**Likely follow-ups:**
- *Why not just check `status_code == 200`?* You can, but `raise_for_status` is shorter and covers every error code.
- *Should you retry a 401 or 404?* No; retrying will not fix a wrong key or address.
**Common mistakes:** No timeout; calling `.json()` on an error reply; a bare `except:` that hides every problem; retrying forever.

### Q22 ⭐⭐ 🟡 What are HTTP status codes 200, 401, 404 and 429, and what do they mean when you call an API?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you can read an API error and know what to do next.
**Say this in the interview:** "200 is success, 401 means my key is missing or wrong, 404 means that address or record does not exist, and 429 means I am sending too many requests, so I should slow down and retry."
**Explain simply:**
- An HTTP status code is a 3-digit number the server sends with every reply to say how it went. Codes starting with 2 are success, 4 are your side's mistake, 5 are the server's problem.

| Code | Meaning | What I do |
|---|---|---|
| 200 | OK, data returned | Use `response.json()` |
| 401 | Unauthorized: key missing, wrong or expired | Check the API key and header; do not retry |
| 404 | Not found: wrong URL or the record does not exist | Check the URL and ID; do not retry |
| 429 | Too many requests (rate limit) | Wait (the `Retry-After` header often says how long) and retry |

- Related: 403 means "you are known but not allowed", 500 means the server broke (retry later).
- Example: pulling 5,000 employee records one by one may hit 429; fetch in pages or add a short pause.
**Likely follow-ups:**
- *401 vs 403?* 401: who are you? 403: I know you, but no access.
- *How do you avoid 429?* Fewer calls, pause between calls, cache results, retry with waiting.
**Common mistakes:** Mixing up 401 and 404; retrying instantly in a loop on 429 (makes it worse); assuming a reply with an error code still contains valid data.

### Q23 ⭐⭐ 🟡 How do you load several sheets of one workbook at once with pandas, and what does sheet_name=None return?
**Asked at:** commonly asked (no company-specific report found; one Glassdoor snippet mentions reading an Excel sheet with pandas)
**What the interviewer is checking:** Whether you can pull a multi-sheet HR workbook into Python in one step.
**Say this in the interview:** "`pd.read_excel(file, sheet_name=None)` reads every sheet and returns a dictionary: the keys are sheet names and the values are DataFrames."
**Explain simply:**
- By default `read_excel` reads only the first sheet.
- `sheet_name=None` means "all sheets"; the result is a dictionary (name to DataFrame).
- You pick one with `all_sheets["Attendance"]`, or loop over `.items()`.
- You can also pass a list, `sheet_name=["Employees", "Budget"]`, for just those.
**Sample data:** `hr_workbook.xlsx` with sheets Employees (5 rows), Attendance (3 rows), Budget (3 rows).
**Code (what you write in the interview):**
```python
import pandas as pd

all_sheets = pd.read_excel("hr_workbook.xlsx", sheet_name=None)

print(type(all_sheets))
print(list(all_sheets.keys()))
print(all_sheets["Attendance"])
```
**Output:**
```
<class 'dict'>
['Employees', 'Attendance', 'Budget']
   employee_id  days_present
0          101            22
1          102            19
2          103            21
```
**What it means:** One call gave me all three sheets, each as its own table.
**Likely follow-ups:**
- *Stack all sheets into one table?* `pd.concat(all_sheets, names=["sheet"])` works when the sheets have the same columns.
- *Needs a library?* Yes, `openpyxl` for `.xlsx`.
**Common mistakes:** Expecting one DataFrame back; reading the workbook once per sheet; wrong sheet-name spelling or capital letters (KeyError).

### Q24 ⭐⭐ 🟡 Write code to read an Excel file, add a column for annual salary from monthly salary, and save the result to a new Excel file.
**Asked at:** one Glassdoor report (snippet only, employer not seen) asked how to get data from an Excel sheet and operate on it with pandas; otherwise commonly asked.
**What the interviewer is checking:** The read, change, write cycle that automates manual Excel work.
**Say this in the interview:** "Read with `read_excel`, create the new column by multiplying monthly salary by 12, and save with `to_excel` using `index=False` so no extra number column is written."
**Explain simply:**
- Column arithmetic works on the whole column at once, no loop needed.
- Save to a new file name so the original stays safe.
- `index=False` stops pandas writing its 0, 1, 2 row numbers as an extra column.
**Sample data:** `employees.xlsx`, same 5 employees as Q18.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_excel("employees.xlsx")

# Annual salary = monthly salary x 12 months
employees["annual_salary"] = employees["monthly_salary"] * 12

employees.to_excel("employees_with_annual.xlsx", index=False)
print(employees[["name", "monthly_salary", "annual_salary"]])
```
**Output:**
```
    name  monthly_salary  annual_salary
0   Asha           45000         540000
1   Ravi           52000         624000
2  Meena           48000         576000
3  Karan           60000         720000
4  Divya           41000         492000
```
**What it means:** Each employee has a yearly figure, and the new file holds the full table including the new column.
**Likely follow-ups:**
- *Salary read as text?* Convert with `pd.to_numeric(..., errors="coerce")`.
- *Blank salary?* The result is NaN (empty), not zero.
**Common mistakes:** Forgetting `index=False`; overwriting the source file; running with the output file open in Excel (permission error); a loop over rows instead of one column operation.

### Q25 ⭐⭐ 🟡 How do you write two DataFrames to two different sheets of the same Excel file?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know `ExcelWriter`; calling `to_excel` twice with the same file name would overwrite the first sheet.
**Say this in the interview:** "I open one `pd.ExcelWriter`, then call `to_excel` for each DataFrame with its own `sheet_name`. The `with` block saves the file at the end."
**Explain simply:**
- `ExcelWriter` is a handle on one workbook that stays open while you add sheets.
- Each `to_excel(writer, sheet_name=...)` adds one sheet.
- `with` closes and saves the file automatically.
**Sample data:** `employees` (5 rows, from the CSV) and a small `attendance` table (3 rows).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("employees.csv")
attendance = pd.DataFrame({"employee_id": [101, 102, 103], "days_present": [22, 19, 21]})

with pd.ExcelWriter("hr_report.xlsx") as writer:
    employees.to_excel(writer, sheet_name="Employees", index=False)
    attendance.to_excel(writer, sheet_name="Attendance", index=False)

print(pd.ExcelFile("hr_report.xlsx").sheet_names)
```
**Output:**
```
['Employees', 'Attendance']
```
**What it means:** One workbook, two sheets, ready to email. (The last print is only to confirm the sheets here.)
**Likely follow-ups:**
- *Add a sheet to an existing file?* `pd.ExcelWriter("file.xlsx", mode="a", engine="openpyxl")`.
- *Formatting?* Use openpyxl afterwards (Q29).
**Common mistakes:** Calling `to_excel("same.xlsx")` twice (second call replaces the first file); forgetting the `with` so nothing is saved; sheet names longer than 31 characters.

### Q26 ⭐⭐ 🟡 What is out-of-order execution in Jupyter, and how can it give you wrong results?
**Asked at:** commonly asked (no company-specific report found; an arXiv 2025 study on Jupyter use, snippet only, discusses restart and run all)
**What the interviewer is checking:** That you know a notebook remembers variables in memory, whatever order the cells were run.
**Say this in the interview:** "Jupyter runs cells in the order you click, not top to bottom. A variable keeps its latest value, so re-running one cell can change results silently and the notebook no longer matches what the page shows."
**Explain simply:**
- The kernel (the program running your code) keeps variables in memory. Cells are not automatically re-run in sequence.
- The number beside each cell (`In [5]`) shows the real order it ran in.
- If you re-run a cell that changes data (a raise, a filter), it applies again on top of the earlier change.
- Fix: before trusting or sharing, use "Restart kernel and run all" (Q5) so the notebook runs once from the top.
**Sample data:** three cells shown below. Here I ran them as a plain script in the same order to get the output (not inside a live notebook).
**Code (what you write in the interview):**
```python
import pandas as pd

# Cell 1
employees = pd.DataFrame({"name": ["Asha", "Ravi", "Meena"], "monthly_salary": [45000, 52000, 48000]})

# Cell 2: give everyone a 5000 raise
employees["monthly_salary"] = employees["monthly_salary"] + 5000

# Cell 3: check the total payroll
print(employees["monthly_salary"].sum())

# You scroll up and run Cell 2 again, then Cell 3 again
employees["monthly_salary"] = employees["monthly_salary"] + 5000
print(employees["monthly_salary"].sum())
```
**Output:**
```
160000
175000
```
**What it means:** One raise was meant (160,000), but a second run of Cell 2 added another 15,000 and nothing on the page shows it. Restart and run all would give 160,000 again.
**Likely follow-ups:**
- *How do you avoid it?* Create new columns instead of overwriting; keep cells independent; restart and run all often.
- *Deleted a cell, variable still works?* Yes, it stays in memory until the kernel restarts.
**Common mistakes:** Sharing a notebook that was never run top to bottom; trusting numbers from a cell run long ago; overwriting the original DataFrame.

### Q27 ⭐⭐ 🟡 What is the difference between running code in a Jupyter notebook and running a .py script, and when would you use each?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know exploration tools versus automation tools.
**Say this in the interview:** "I use a notebook to explore and explain, because I can run small pieces and see results. When the work is final and must run on its own, like a monthly report, I move it into a `.py` script."
**Explain simply:**

| | Notebook (.ipynb) | Script (.py) |
|---|---|---|
| Runs | Cell by cell, in any order | Top to bottom, every time |
| Shows | Code, tables, charts and notes together | Only what you print or save |
| Best for | Exploring data, learning, sharing findings | Repeatable jobs, scheduling, automation |
| Risk | Out-of-order cells (Q26) | Harder to inspect step by step |

- A script runs from a terminal with `python monthly_report.py`, and can be scheduled (Windows Task Scheduler, cron).
- A common flow: explore in a notebook, then copy the clean steps into a script.
**Likely follow-ups:**
- *Can a notebook be scheduled?* Yes with tools, but a script is simpler and safer.
- *Where do you write the script?* Any editor, such as VS Code.
**Common mistakes:** Treating a messy notebook as a production job; putting hard-coded file paths from your laptop into a shared script; thinking a notebook and script behave differently in what the code does (the code is the same; the way it runs differs).

### Q28 ⭐⭐ 🟡 How do you read an Excel file that has a title in the first rows, a merged header or footer notes?
**Asked at:** commonly asked (no company-specific report found; messy report files are typical of MIS-style roles)
**What the interviewer is checking:** Whether you can handle real, untidy Excel reports instead of clean practice files.
**Say this in the interview:** "I open the file first to see where the real header sits. Then I use `header=` to point to that row, `skiprows` to drop rows above, and `skipfooter` to drop notes at the bottom."
**Explain simply:**
- `header=2` means the column names are on the third row (counting from 0).
- `skipfooter=3` drops the last 3 rows; `usecols="A:C"` picks columns.
- A merged cell keeps its value only in the top-left cell, the rest read as empty (NaN). A merged title is harmless once skipped; for a merged group header over several columns, rename the columns yourself with `names=[...]` or fill the gaps.
**Sample data:** `attendance_report.xlsx`: row 1 title (merged across A:C), row 2 blank, row 3 header, rows 4 to 6 data, row 7 blank, rows 8 to 9 notes. Without options the read gives a title as header and notes as data rows.
**Code (what you write in the interview):**
```python
import pandas as pd

attendance = pd.read_excel(
    "attendance_report.xlsx",
    header=2,         # real header is on the 3rd row
    skipfooter=3,     # ignore blank line + 2 note lines at the bottom
)
print(attendance)
```
**Output:**
```
   employee_id   name  days_present
0          101   Asha            22
1          102   Ravi            19
2          103  Meena            21
```
**What it means:** Only the real table is loaded, with proper column names and numeric types.
**Likely follow-ups:**
- *Footer length changes monthly?* Read everything, then drop rows where `employee_id` is empty or not a number.
- *Several tables in one sheet?* Read with `usecols` and `nrows` for each block.
**Common mistakes:** Not looking at the file first; off-by-one in `header` (it starts at 0); leaving notes in the data so a numeric column becomes text and sums fail.

### Q29 ⭐⭐ 🟡 How do you use openpyxl to open a workbook, read a cell value and write a value to a cell?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you can edit a specific cell in an existing workbook, which pandas does not do well.
**Say this in the interview:** "`load_workbook` opens the file, `workbook.active` gives the sheet, `sheet["B2"].value` reads a cell, assigning to `sheet["E2"]` writes one, and `workbook.save` saves it."
**Explain simply:**
- openpyxl works cell by cell, like a person clicking in Excel; pandas works on whole tables.
- A cell address is column letter plus row number, so B2 is column B, row 2.
- Changes live only in memory until you call `save`.
- To read the value a formula calculated (not the formula text), open with `load_workbook(file, data_only=True)`.
**Sample data:** `employees.xlsx`: header in row 1, Asha in row 2 (name in B2, status in E2).
**Code (what you write in the interview):**
```python
from openpyxl import load_workbook

workbook = load_workbook("employees.xlsx")
sheet = workbook.active

# Read the name in B2 (row 2, column B)
print(sheet["B2"].value)

# Write a new value into E2 and save
sheet["E2"] = "Resigned"
workbook.save("employees_updated.xlsx")
```
**Output:**
```
Asha
```
**What it means:** I read Asha's name and changed her status in a copy of the file (saved under a new name to protect the original).
**Likely follow-ups:**
- *Loop through rows?* `for row in sheet.iter_rows(values_only=True):`.
- *Why not pandas?* See Q15: pandas for tables, openpyxl for formatting and single cells.
**Common mistakes:** Forgetting `save`; expecting the saved file to keep charts or macros (openpyxl may drop some); reading a formula cell without `data_only=True` and getting the formula text; saving over the original file.

### Q30 ⭐⭐ 🟡 Write code to loop through a list of department names and save each department's data to a separate Excel file.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Loop plus filter plus export, the core of "send each manager their team's file" automation.
**Say this in the interview:** "For each department name I filter the rows for it and save that slice with `to_excel`, using the department name in the file name."
**Explain simply:**
- The loop runs the same three steps once per department: filter, build a file name, save.
- An f-string (`f"{department}_employees.xlsx"`) puts the variable inside the text, giving `HR_employees.xlsx`.
- `employees["department"] == department` gives True or False per row; using it inside `employees[...]` keeps only the True rows.
**Sample data:** `employees.xlsx` (5 rows: HR 2, Sales 2, Finance 1).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_excel("employees.xlsx")
departments = ["HR", "Sales", "Finance"]

for department in departments:
    department_data = employees[employees["department"] == department]
    department_data.to_excel(f"{department}_employees.xlsx", index=False)
    print("Saved", department, "with", len(department_data), "rows")
```
**Output:**
```
Saved HR with 2 rows
Saved Sales with 2 rows
Saved Finance with 1 rows
```
**What it means:** Three files were created, one per department, each with only that team's rows.
**Alternative:** Skip the list and loop over the groups: `for department, group in employees.groupby("department"):` (then save `group`).
**Likely follow-ups:**
- *A department name has a slash or odd characters?* Clean the file name first.
- *Email each file?* Possible with `smtplib` or Outlook automation, but only to the right owner; watch confidentiality.
**Common mistakes:** A department typo giving an empty file; forgetting `index=False`; one fixed file name so each loop overwrites the last; saving files in an unexpected folder.

### Q31 ⭐⭐ 🟡 What is hallucination in AI assistants, and how can it show up in code, for example with a pandas function that does not exist?
**Asked at:** commonly asked (no company-specific report found; verifying AI output is a stated expectation in 2026 prep articles, snippet only)
**What the interviewer is checking:** That you do not trust AI blindly and know how to catch made-up answers.
**Say this in the interview:** "Hallucination means the AI states something false in a confident tone. In code that can be a function or argument that does not exist, or an old one that was removed. I run the code, read the error, and check the official pandas documentation."
**Explain simply:**
- The AI predicts likely text; it does not look things up or run code, so it can invent names that sound right.
- Typical signs: `AttributeError` (method does not exist), an unknown argument, or code that runs but does something different from what was claimed.
- Dangerous case: it runs without error but the logic is subtly wrong (see Q32).
- Checks: run on a tiny sample, look up the function in the official docs, ask the AI to explain each line, and compare with a number you know.
**Sample data:** a 3-row list of names, one repeated.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"name": ["Asha", "Asha", "Ravi"]})

# AI suggested this method, but it does not exist
print(hasattr(employees, "remove_duplicates"))

# The real method
print(employees.drop_duplicates())
```
**Output:**
```
False
   name
0  Asha
2  Ravi
```
**What it means:** `remove_duplicates` does not exist; the real method is `drop_duplicates`. Another case I confirmed here: `DataFrame.append`, which older tutorials use, raises `AttributeError` in pandas 3.0.5 because it was removed (use `pd.concat`).
**Likely follow-ups:**
- *Does a successful run mean the code is right?* No; check the result against a known number.
- *Does pasting the error back help?* Often yes, but still verify the fix.
**Common mistakes:** Copying code without running it; trusting an answer because it sounds sure; using outdated syntax from old tutorials; pasting real employee data to "help" the AI (Q17).

### Q32 ⭐⭐ 🟡 What would you do if an AI assistant suggests code that gives a different number from your manual Excel calculation?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you reconcile numbers step by step instead of blindly picking one side.
**Say this in the interview:** "I do not assume either is right. I compare row counts first, then check duplicates, blanks and data types, because the gap is usually a data issue. I fix the cause, then re-check against Excel."
**Explain simply:**
- Step 1: same input? Same file, same filters, same period.
- Step 2: row count in pandas (`shape`) versus Excel's row count.
- Step 3: look for duplicates, blanks, numbers stored as text, extra spaces, different date handling.
- Step 4: test the AI's logic on 3 to 5 rows by hand.
- Step 5: after fixing, both should match; note what caused the gap. Excel can be wrong too (hidden rows, a formula that skipped a row).
**Sample data:** `payroll_check.csv`: 5 rows, with employee 102 listed twice and employee 103 salary blank. My manual Excel total of the 4 unique people was 157,000.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.read_csv("payroll_check.csv")

print(employees.shape)                     # rows, same as Excel?
print(employees.duplicated().sum())        # repeated rows
print(employees["monthly_salary"].isna().sum())   # blanks
print(employees["monthly_salary"].sum())   # pandas total

employees = employees.drop_duplicates()
print(employees["monthly_salary"].sum())   # total after removing the repeat
```
**Output:**
```
(5, 2)
1
1
209000.0
157000.0
```
**What it means:** The AI's total of 209,000 counted employee 102 twice. After removing the duplicate it is 157,000, matching Excel. The blank salary is skipped by both pandas and Excel, so it did not cause the gap (but I would still ask HR why it is blank).
**Likely follow-ups:**
- *Which one is right?* Whichever matches the business rule; here a person should be paid once.
- *What if they still differ?* Compare a sample of individual rows, or sum by department in both tools to find where the gap sits.
**Common mistakes:** Assuming the AI is right because it ran; assuming Excel is right without checking; changing code until the numbers match without understanding why; not recording what the difference was.

### Q33 ⭐⭐ 🟡 How do you document a notebook so a colleague can understand and re-run it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you treat a notebook as a document other people must trust, not just scratch paper?
**Say this in the interview:** "I put a title and purpose at the top, explain each section in a Markdown cell, list the input files and the libraries needed, keep cells in a clean top-to-bottom order, and finish with 'Restart kernel and run all' so I know it really runs."
**Explain simply:**
- **Markdown cell:** a cell for plain-text notes (headings, bullets), not code (see Q4).
- **Top cell:** title, author, date, one-line purpose, and what the output is (for example "monthly attrition by department").
- **Setup cell:** all `import` lines together, and the input file names in one place, so a colleague changes one line, not ten.
- **Section headings and short comments:** say *why* a step exists ("remove test employees"), not just what the code does.
- **Requirements:** list library versions in a `requirements.txt` file (see Q36) and say which Python version you used.
- **Last check:** Kernel > Restart and run all (see Q5); fix anything that breaks.

**Sample data:** a typical notebook skeleton (Markdown cells shown as comments).
**Code (what you write in the interview):**
```python
# [Markdown] # Monthly Attrition Report
# [Markdown] Purpose: attrition rate by department. Input: hr_data.xlsx. Author: Priya, Nov 2026

# [Code] setup
import pandas as pd
input_file = "hr_data.xlsx"          # change this line to use another file

# [Markdown] ## 1. Load and clean (we drop test employees)
# [Code] employees = pd.read_excel(input_file)
```
**What it means:** A stranger can read the purpose, see which file to change, and re-run from the top without asking me anything.
**Likely follow-ups:**
- *Would you share the .ipynb or an HTML copy?* HTML for managers (Q35), the notebook plus requirements for colleagues who will re-run it.
- *Where do you keep passwords?* Never in the notebook (see Q40).

**Common mistakes:** No explanation at all; file paths like `C:\Users\me\Desktop` that only work on one laptop; leaving old, unused cells; never checking a full re-run.

### Q34 ⭐ 🟢 How do you add a chart or an image output inside a Jupyter notebook, and what does %matplotlib inline do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you produce a quick chart in a notebook and do you know the "magic command" for it?
**Say this in the interview:** "I build the chart with pandas `.plot()` or matplotlib and call `plt.show()`; Jupyter draws it right under the cell. `%matplotlib inline` tells Jupyter to show charts as pictures inside the notebook; in current versions it is already the default."
**Explain simply:**
- **matplotlib** is Python's basic charting library; `plt` is its usual short name.
- **Magic command:** a line starting with `%` that talks to Jupyter itself, not to Python. `%matplotlib inline` means "draw charts inside the notebook".
- To show a saved picture instead, use `from IPython.display import Image; Image("chart.png")`.
- To keep a chart for a report, `plt.savefig("headcount.png")` before `plt.show()`.

**Sample data:** headcount by department (4 rows, in the code).
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

headcount = pd.DataFrame({
    "department": ["HR", "IT", "Sales", "Finance"],
    "employees": [12, 40, 55, 18],
})

headcount.plot(kind="bar", x="department", y="employees", title="Headcount by department")
plt.show()
```
**Output:** a bar chart with four bars (HR 12, IT 40, Sales 55, Finance 18) drawn under the cell. (Run here without a screen using the non-display backend: the code ran without errors, but the picture itself was not looked at.)
**What it means:** Sales is the biggest team, HR the smallest.
**Likely follow-ups:**
- *Why does my chart not appear in a plain .py script?* Outside Jupyter a window opens when you call `plt.show()`; use `plt.savefig` on a server.
- *Do I still need `%matplotlib inline`?* Usually not in recent Jupyter; harmless to keep (from memory, not tested here).

**Common mistakes:** Forgetting to label the chart title and axes; forgetting `plt.show()` in scripts; typing `%matplotlib inline` in a plain `.py` file, where `%` is a syntax error.

### Q35 ⭐ 🟢 How do you export a Jupyter notebook to HTML or PDF to share with a manager?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you deliver results to someone who does not use Python?
**Say this in the interview:** "In Jupyter I use File > Save and Export As > HTML. I run the whole notebook first so the outputs are fresh, and I hide the code if the manager only wants the results."
**Explain simply:**
- **HTML export:** one file that opens in any browser, with charts and tables included. No Python needed to read it.
- **PDF:** needs extra software installed (LaTeX), so many people open the HTML and use Print > Save as PDF instead.
- **Command line:** `jupyter nbconvert --to html report.ipynb`. Add `--no-input` to hide the code cells.
- Clean up first: Restart and run all (Q5), delete scratch cells, add Markdown headings.

**Sample data:** none needed.
**Code (what you write in the interview):**
```
jupyter nbconvert --to html --no-input monthly_report.ipynb
```
**Output:** creates `monthly_report.html` next to the notebook. (Not run here: nbconvert is not installed in this environment, so the command is from memory, unverified.)
**What it means:** The manager gets a clean web page with tables and charts, without the code.
**Likely follow-ups:**
- *Is there any data risk?* Yes, the HTML contains every output shown, including names or salaries. Check before emailing.

**Common mistakes:** Exporting stale outputs; sharing HTML that shows employee-level personal data; trying PDF export without LaTeX and giving up.

### Q36 ⭐ 🟢 What is a virtual environment, and why would an analyst use one?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know how to keep projects from breaking each other?
**Say this in the interview:** "A virtual environment is a private folder of Python libraries for one project. I use one so that upgrading pandas for project B does not break project A, and so a colleague can recreate my exact setup."
**Explain simply:**
- **Library version:** pandas 1.x and 3.x behave differently, so code written for one can fail on the other.
- A **virtual environment** ("venv") holds its own copy of the libraries, separate from the rest of the computer.
- `pip freeze > requirements.txt` saves the list of libraries and versions; a colleague runs `pip install -r requirements.txt`.
- Conda environments do the same job if your company uses Anaconda.

**Sample data:** none needed.
**Code (what you write in the interview):**
```
python -m venv hr_env
hr_env\Scripts\activate          # Windows (on Mac/Linux: source hr_env/bin/activate)
pip install pandas openpyxl
pip freeze > requirements.txt
```
**Output:** a new `hr_env` folder; the prompt changes to `(hr_env)`; `requirements.txt` lists the installed libraries. (Commands not run here, from memory, unverified.)
**What it means:** The project has its own clean toolbox and a recipe to rebuild it.
**Likely follow-ups:**
- *How do you use it in Jupyter?* Install `ipykernel` inside it and pick that kernel in the notebook.

**Common mistakes:** Installing everything into the base Python; forgetting to activate before `pip install`; not saving `requirements.txt`.

### Q37 ⭐ 🟢 What is the difference between Jupyter Notebook, JupyterLab, Google Colab and VS Code notebooks?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the tools and when each fits?
**Say this in the interview:** "They all run the same `.ipynb` notebook files. Jupyter Notebook is the classic simple browser version, JupyterLab is the newer fuller workspace, Colab is Google's free hosted version, and VS Code runs notebooks inside an editor I may already use for scripts."
**Explain simply:**
- **Jupyter Notebook:** one notebook per browser tab, runs on your own computer; simple.
- **JupyterLab:** same engine, but with a file browser, several tabs side by side, terminal; more like an IDE (a full coding workspace).
- **Google Colab:** runs on Google's computers, needs only a browser and Google account, easy sharing, free. Your data is uploaded to Google, so be careful with employee data.
- **VS Code notebooks:** notebooks inside Visual Studio Code, with a debugger, Git and Copilot-style helpers.

**Sample data:** none needed.
**What it means:** Same notebook file, different place to run it. For confidential HR data I prefer a local setup (Jupyter or VS Code); Colab is good for learning or public data.
**Likely follow-ups:**
- *Which would you use at work?* Whatever the company approves and keeps data inside its network.

**Common mistakes:** Thinking they are different languages or file formats; uploading real payroll files to Colab.

### Q38 ⭐ 🟡 How do you apply formatting such as bold headers, column width and number formats to an Excel report with openpyxl?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you make an automated report look finished, not like raw output?
**Say this in the interview:** "I save the data with pandas, reopen the file with openpyxl, set the header font to bold, set column widths, set a number format on the money column, and save again."
**Explain simply:**
- **pandas** writes the data; **openpyxl** (a library that edits `.xlsx` files) handles looks.
- `Font(bold=True)` makes bold text; `column_dimensions["A"].width` sets width.
- `number_format = "#,##0.00"` is the same code you type in Excel's Format Cells (thousands separator, 2 decimals).
- `sheet[1]` is the first row (the header row).

**Sample data:** average salary by department.
**Code (what you write in the interview):**
```python
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font

report = pd.DataFrame({
    "department": ["HR", "IT", "Sales"],
    "avg_salary": [48250.5, 72000.0, 55100.75],
})
report.to_excel("salary_report.xlsx", index=False)

workbook = load_workbook("salary_report.xlsx")
sheet = workbook.active

for cell in sheet[1]:                      # row 1 is the header row
    cell.font = Font(bold=True)

sheet.column_dimensions["A"].width = 18    # column width
sheet.column_dimensions["B"].width = 14

for row in range(2, sheet.max_row + 1):    # number format on the salary column
    sheet.cell(row=row, column=2).number_format = "#,##0.00"

workbook.save("salary_report.xlsx")
```
**Output:** no printed output; the file is saved. Reading it back showed: header bold = `True`, column A width = `18.0`, B2 format = `#,##0.00`.
**What it means:** The file opens in Excel with a bold header, readable widths and formatted salaries.
**Likely follow-ups:**
- *Can pandas alone do this?* Only a little (with `xlsxwriter`); openpyxl is the usual tool for editing styles.

**Common mistakes:** Formatting before saving the pandas file (the later `to_excel` overwrites it); forgetting `workbook.save`; leaving the file open in Excel, which blocks saving.

### Q39 ⭐ 🟡 How do you add an Excel formula, such as a SUM at the bottom of a column, using openpyxl?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a formula is just text starting with `=`, and that Python does not calculate it?
**Say this in the interview:** "I write the formula as a string, like `=SUM(B2:B4)`, into the cell below the data. Excel calculates it when the file is opened."
**Explain simply:**
- openpyxl stores the formula text; it does not work out the answer.
- Find the last data row with `sheet.max_row`, then write the total one row below.
- The benefit: the total stays live in Excel if someone edits the numbers.
- If you only need the number in a report, calculate it in pandas (`payroll["salary"].sum()`) and write the value instead.

**Sample data:** 3 employees with salaries.
**Code (what you write in the interview):**
```python
import pandas as pd
from openpyxl import load_workbook

payroll = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena"],
    "salary": [45000, 52000, 61000],
})
payroll.to_excel("payroll.xlsx", index=False)

workbook = load_workbook("payroll.xlsx")
sheet = workbook.active

last_row = sheet.max_row                       # 4 (header + 3 employees)
sheet.cell(row=last_row + 1, column=1, value="Total")
sheet.cell(row=last_row + 1, column=2, value=f"=SUM(B2:B{last_row})")

workbook.save("payroll.xlsx")
```
**Output:** no printed output. Reading the file back showed cell A5 = `Total` and B5 = `=SUM(B2:B4)`. Reading with `data_only=True` gave `None`, because the formula has not been calculated yet (it needs to be opened and saved in Excel once).
**What it means:** The formula is in place and Excel will show 158000 when opened (I did not open Excel here).
**Likely follow-ups:**
- *Why is the value None when I read it back?* openpyxl never calculates; Excel stores the result when it saves.

**Common mistakes:** Writing `SUM(B2:B4)` without the `=` (it becomes plain text); hard-coding the range when the row count changes; expecting Python to show the total.

### Q40 ⭐ 🟡 How do you send an API key safely in a request without writing it into the notebook?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you protect secrets, since notebooks get emailed and committed to Git?
**Say this in the interview:** "I store the key as an environment variable on my machine, read it with `os.environ`, and send it in the request header. The key never appears in the notebook, so sharing the file is safe."
**Explain simply:**
- An **API key** is a password that identifies you to a service; anyone holding it can use your account.
- An **environment variable** is a named value kept by the operating system, outside your files.
- A **header** is extra information sent with the request; many APIs expect `Authorization: Bearer <key>`.
- A `.env` file plus `python-dotenv` is another common way; add `.env` to `.gitignore` so it is never shared.
- If a key leaked, revoke it and create a new one.

**Sample data:** a made-up HR API address `api.example.com` (not a real service).
**Code (what you write in the interview):**
```python
import os
import requests

api_key = os.environ["HR_API_KEY"]            # set in the terminal, not in the notebook
headers = {"Authorization": f"Bearer {api_key}"}

response = requests.get("https://api.example.com/employees", headers=headers, timeout=10)
```
**Output:** the live call was not run here (the address is fictional and there is no network call). I checked the header-building part offline with `HR_API_KEY=abc123`: the header came out as `Bearer abc123`. With the variable unset, the code stops with `KeyError: 'HR_API_KEY'`, which is the behaviour you want (it fails loudly).
**What it means:** The secret lives outside the file; the code only reads it.
**Likely follow-ups:**
- *Why not just paste it in a variable?* The notebook may be shared, emailed or committed with the key inside.
- *What if it already leaked?* Revoke and rotate it immediately.

**Common mistakes:** Hard-coding the key; leaving it in the saved notebook output (a printed `headers`); committing `.env`.

### Q41 ⭐ 🟡 How do you collect data from an API that returns results in pages (pagination)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you write a loop that keeps asking for the next page until there is nothing left?
**Say this in the interview:** "APIs send big results in pages, for example 100 rows each. I loop: request page 1, add the rows to a list, go to page 2, and stop when a page comes back empty. Then I turn the list into a DataFrame."
**Explain simply:**
- **Pagination:** splitting a long result into pages. You ask for them with a parameter such as `page=2` (some APIs use `offset` or a "next" link instead; read the docs).
- Collect rows in a plain list, and build the DataFrame once at the end (faster and simpler).
- Stop when the page is empty or the API says there is no next page.
- Add a safety limit on pages so a bug cannot loop forever.

**Sample data:** a mock API with 5 employees, 2 per page. In real life the call inside `get_page` would be `requests.get(url, params={"page": page}).json()`; the live call was not run here.
**Code (what you write in the interview):**
```python
import pandas as pd

# Mock API: 5 employees, 2 per page
all_employees = [{"id": i, "name": f"Emp{i}"} for i in range(1, 6)]
def get_page(page):
    start = (page - 1) * 2
    return all_employees[start:start + 2]

rows = []
page = 1
while True:
    results = get_page(page)
    if not results:            # empty page means no more data
        break
    rows.extend(results)
    page += 1

employees = pd.DataFrame(rows)
print(employees)
```
**Output:**
```
   id  name
0   1  Emp1
1   2  Emp2
2   3  Emp3
3   4  Emp4
4   5  Emp5
```
**What it means:** Three requests (2 + 2 + 1 rows) plus one empty page gave all 5 employees in one table.
**Likely follow-ups:**
- *What if the API gives a "next" URL?* Loop while that URL exists.
- *How do you avoid hitting the rate limit?* Add a pause (Q42).

**Common mistakes:** Only reading page 1 and assuming that is all the data; infinite loop when the stop condition never triggers; appending DataFrames in the loop (slow).

### Q42 ⭐ 🟡 What is rate limiting in an API, and how do you stay within it in a loop of requests?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know APIs cap how fast you can call them, and can you slow down politely?
**Say this in the interview:** "Rate limiting means the API allows only a certain number of requests per minute. In a loop I add `time.sleep` between calls, and if I get a 429 error I wait and retry with a growing delay."
**Explain simply:**
- **Rate limit:** a cap such as 60 calls per minute, to protect the service from overload.
- Going over it returns status **429 "Too Many Requests"** (see Q22), and repeated abuse can get your key blocked.
- Simple fix: `time.sleep(1)` between calls. 1 call per second is 60 per minute.
- Better: on a 429, wait (many APIs send a `Retry-After` header with the seconds), double the wait each retry, and give up after a few tries (called **exponential backoff**).

**Sample data:** four employee IDs; the API call is a mock (live call not run here).
**Code (what you write in the interview):**
```python
import time

employee_ids = [101, 102, 103, 104]

def fetch_employee(employee_id):          # stands in for requests.get(...)
    return {"id": employee_id}

results = []
for employee_id in employee_ids:
    results.append(fetch_employee(employee_id))
    time.sleep(0.5)                        # pause so we stay under the limit (2 calls per second)

print(len(results), "employees fetched")
```
**Output:**
```
4 employees fetched
```
(took about 2 seconds because of the pauses)
**What it means:** The loop deliberately runs slower so the API never sees more than 2 calls per second.
**Alternative:** Retry on a 429 with growing waits (mock: the first two calls are rejected).
```python
import time

def call_api(attempt):                     # mock: first two calls are rate limited (429)
    return 429 if attempt < 2 else 200

for attempt in range(5):
    status = call_api(attempt)
    if status == 429:
        wait = 2 ** attempt                # wait 1s, 2s, 4s ...
        print("Too many requests, waiting", wait, "seconds")
        time.sleep(wait)
    else:
        print("Success")
        break
```
Output: `Too many requests, waiting 1 seconds`, `Too many requests, waiting 2 seconds`, `Success`.
**Likely follow-ups:**
- *How do you know the limit?* The API documentation, or response headers.

**Common mistakes:** Hammering the API with no pause; retrying forever; ignoring the `Retry-After` value.

### Q43 ⭐ 🟡 How would you schedule a Python report script to run every Monday morning?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a script needs an outside scheduler and that notebooks are not the right tool for it?
**Say this in the interview:** "I put the report in a `.py` script that runs from start to finish without me, then schedule it with Windows Task Scheduler, or cron on Linux or Mac, for Monday at 8 am. In a company I would ask IT about an approved scheduler such as Airflow or a server job."
**Explain simply:**
- **Script first:** it must run unattended: no manual steps, file paths that always work, the output saved or emailed.
- **Task Scheduler (Windows):** create a task, trigger "Weekly, Monday, 08:00", action "run python with the script path".
- **cron (Linux/Mac):** a one-line timetable. `0 8 * * 1 python3 /home/me/weekly_report.py` means minute 0, hour 8, any day of month, any month, Monday.
- **Log and alert:** write a log line on success or failure so someone notices if it breaks.
- The computer must be on, or use a shared server.

**Sample data:** none needed.
**Code (what you write in the interview):**
```
0 8 * * 1  python3 /home/me/weekly_report.py >> /home/me/report.log 2>&1
```
**Output:** none to show; the line is put in `crontab -e`. (Not run here: scheduling needs a real machine; syntax is from memory, unverified.)
**What it means:** Every Monday at 8:00 the script runs and its messages go to a log file.
**Likely follow-ups:**
- *What if the laptop is off?* The job is missed, so use a server or a company scheduler.
- *Where do credentials go?* Environment variables, not the script (Q40).

**Common mistakes:** Relying on relative paths that break when the scheduler starts from a different folder; no logging; scheduling a notebook instead of a script.

### Q44 ⭐ 🟡 How would you use an AI assistant to explain a long piece of unfamiliar pandas code, and how do you confirm the explanation is right?
**Asked at:** commonly asked (no company-specific report found; AI-assisted analysis checking is a topic in 2026 prep material, snippet level only)
**What the interviewer is checking:** Do you use AI to learn faster but still verify, instead of believing it?
**Say this in the interview:** "I paste the code, with fake or sample data and no real employee details, and ask it to explain it line by line in plain English. Then I check each claim by running the code step by step on a small table and looking at what each line produces."
**Explain simply:**
- Ask for **line-by-line**, and what the input and output of each step look like.
- Run the code **one line at a time** in a notebook, printing the DataFrame after each step.
- Compare the AI's claim with the real result (rows before and after, new columns, types).
- Check unknown functions in the **official pandas documentation**; AI can invent functions or misdescribe defaults.
- Test with a tiny table where you know the answer by hand.

**Sample data:** none needed (use a 5 row copy of the real shape, with made-up values).
**Code (what you write in the interview):**
```python
# Code the AI explained as "keeps employees who left, then counts them by department"
left = employees[employees["status"] == "Left"]
print(len(employees), len(left))          # does the row count drop like the AI said?
print(left.groupby("department").size())
```
**What it means:** If the AI says "filters rows" I should see fewer rows; the numbers prove it, not the AI's confidence.
**Likely follow-ups:**
- *What if the explanation is wrong?* Trust the run, not the text; ask the AI again with the actual output pasted in.

**Common mistakes:** Accepting a fluent explanation without running anything; pasting real names or salaries; not reading the docs for functions you do not know.

### Q45 ⭐ 🟡 How do you pick up a notebook written by someone else and check it still runs on your machine?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you have a safe, methodical routine for inherited work?
**Say this in the interview:** "I make a copy, read it top to bottom, create a clean environment with the libraries it needs, fix the file paths, then Restart and run all. When it runs, I compare a few key numbers with the previous output."
**Explain simply:**
- **Copy first:** never experiment on the original.
- **Read the notes and imports:** which libraries and which input files does it need? Check for a `requirements.txt`.
- **Environment:** make a virtual environment (Q36) and `pip install -r requirements.txt`.
- **Paths:** replace paths like `C:\Users\former_colleague\...` with files you have.
- **Run all:** Kernel > Restart and run all (Q5); read the first error, fix it, repeat.
- **Compare:** the totals should match the old saved outputs (headcount, sums). If not, find out why before using it.
- **Security check:** look for hard-coded passwords or keys and do not run code you do not understand on live data.

**Sample data:** none needed.
**What it means:** Matching totals after a clean re-run tells me the notebook is reproducible on my machine and I can trust it.
**Likely follow-ups:**
- *What if a library version is missing from the notes?* Read error messages, try the version that matches the notebook's date, then record it.

**Common mistakes:** Running cells in a random order; ignoring a `ModuleNotFoundError`; not comparing against the old results; editing the original.

### Q46 ⭐ 🔴 Write a script that reads daily attendance Excel files, calculates the absenteeism percentage per employee and writes a formatted summary workbook with one sheet per department.
**Asked at:** commonly asked (no company-specific report found; MIS and automation job descriptions in the research list this kind of task)
**What the interviewer is checking:** Can you chain reading many files, a groupby, writing several sheets and basic formatting into one clear script?
**Say this in the interview:** "I read all the daily files with glob, stack them with concat, mark each row absent or not, and take the average per employee (absent days divided by total days). Then I write one sheet per department and finish with bold headers and column widths."
**Explain simply:**
- **glob** lists the files that match a pattern (`attendance/*.xlsx`).
- **concat** stacks the daily tables into one long table.
- **Absenteeism %** = absent days / working days x 100. A True/False "is absent" column averages to exactly that share.
- `ExcelWriter` lets you write several sheets into one file; `groupby` on department makes one table per sheet.
- Then openpyxl formats (see Q38).

**Sample data:** 3 daily files (3, 4, 5 Nov 2026) with employee_id, name, department, status. Asha is present all 3 days, Ravi is absent on 2 of 3, Meena absent on 2 of 3, John present all 3. (Files created locally for the test.)
**Code (what you write in the interview):**
```python
import glob
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font

# 1. Read every daily file and stack them into one table
daily_tables = [pd.read_excel(file) for file in glob.glob("attendance/*.xlsx")]
attendance = pd.concat(daily_tables, ignore_index=True)

# 2. Absenteeism % per employee = absent days / total days * 100
attendance["is_absent"] = attendance["status"] == "Absent"
summary = attendance.groupby(["department", "employee_id", "name"])["is_absent"].mean() * 100
summary = summary.round(1).reset_index(name="absenteeism_pct")

# 3. One sheet per department
with pd.ExcelWriter("absenteeism_summary.xlsx") as writer:
    for department, rows in summary.groupby("department"):
        rows.drop(columns="department").to_excel(writer, sheet_name=department, index=False)

# 4. Format: bold headers and wider columns on every sheet
workbook = load_workbook("absenteeism_summary.xlsx")
for sheet in workbook:
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    for letter in ["A", "B", "C"]:
        sheet.column_dimensions[letter].width = 18
workbook.save("absenteeism_summary.xlsx")
```
**Output:** (reading the saved workbook back)
```
HR
   employee_id  name  absenteeism_pct
0            1  Asha              0.0
1            2  Ravi             66.7
IT
   employee_id   name  absenteeism_pct
0            3  Meena             66.7
1            4   John              0.0
```
Header cells were confirmed bold.
**What it means:** Ravi and Meena missed 2 of 3 days (66.7%), Asha and John none. Each department has its own sheet, ready to send to its manager.
**Likely follow-ups:**
- *What about leave or holidays?* Exclude approved leave and holidays from the day count, otherwise absenteeism is overstated; confirm the definition with HR.
- *What if an employee has no row on some days?* They are counted over days they appear; decide how to handle joiners and leavers.
- *Sheet names?* Excel limits names to 31 characters and bans some symbols.

**Common mistakes:** Dividing by the wrong number of days; averaging the percentages of departments (average of averages); forgetting `index=False`; writing a new file each loop and overwriting the earlier sheets (use one `ExcelWriter`).

### Q47 ⭐ 🔴 How do you decide whether to automate a recurring Excel task with Python, and when is Excel, Power Query or VBA the better choice?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Judgement: do you pick the right tool and weigh time saved against effort, not just reach for Python?
**Say this in the interview:** "I ask how often it runs, how long it takes by hand, how many people depend on it, and how messy the data is. If it is small or one-off I stay in Excel. If it is a repeatable refresh of tables inside Excel, Power Query. If it needs to drive Excel buttons or formatting inside the workbook, VBA. If it handles many files, an API, or heavy logic, Python."
**Explain simply:**
- **Rule of thumb:** (minutes saved per run x runs per year) compared with the hours to build and maintain it. Weekly 2-hour task: worth automating. A one-off: not.
- **Excel formulas/pivots:** best for small, visual, one-off work, and when the team only knows Excel.
- **Power Query** (Excel's built-in data cleaning and combining tool, records steps and refreshes with one click): best for combining and cleaning files inside Excel, no code.
- **VBA** (Excel's macro language): best for actions inside the workbook (buttons, printing, formatting) when everyone has Excel.
- **Python:** best for many files, APIs, larger data, repeatable tests, version control, scheduling.
- Also weigh: who will maintain it, whether IT allows Python, data sensitivity, how stable the input format is.

**Sample data:** none needed.
**What it means:** The best tool is the simplest one that the team can maintain. Automating a broken or unclear process just makes mistakes faster, so I document the manual steps first.
**Likely follow-ups:**
- *Example?* Monthly attendance from 30 site files: Python (or Power Query). A one-time payroll check of one file: Excel.
- *What about maintenance?* Whoever builds it must hand over notes and tests (Q33).

**Common mistakes:** Automating a task done once; building in Python something nobody else can maintain; ignoring how often the input format changes.

### Q48 ⭐ 🔴 Describe a full workflow where an AI assistant helps you build a report, covering the prompt, review, testing and documentation, and say what you would never delegate to it.
**Asked at:** commonly asked (no company-specific report found; AI-code verification questions appear on question banks such as PracHub, snippet only)
**What the interviewer is checking:** Do you use AI as a fast junior helper while keeping ownership of correctness, privacy and decisions?
**Say this in the interview:** "I describe the problem and the table structure with fake data, ask for code, then I review it line by line, test it on a small case I can check by hand, compare it with my own Excel numbers, and document it. I never paste real employee data, and I never delegate the definitions, the final numbers or the conclusions."
**Explain simply:**
1. **Define first (me):** what the report must show, e.g. attrition rate by department, and the exact definition (leavers / average headcount).
2. **Prompt:** give the goal, column names and types, 5 rows of **made-up** data, the pandas version, the output format wanted, and rules ("do not modify the original table"). See Q16.
3. **Review:** read every line; look for functions that do not exist, wrong filters, wrong divisors, silent NaN handling, changed row counts.
4. **Test:** run on the tiny table and check by hand; compare with an Excel pivot on a real extract (done locally); test edge cases (empty department, duplicates, missing dates).
5. **Reconcile:** totals must match the source and HR's own numbers before anything is shared.
6. **Document:** Markdown notes, assumptions, source files, version, and a note that AI helped, then Restart and run all (Q5).
7. **Review by a person** before it goes to management.

**Never delegate:**
- Pasting real names, IDs, salaries or health data into a public tool (use fake or masked data or a company-approved tool; see Q17).
- Business definitions and policy judgement (who counts as an employee, what is "absent").
- Checking that the numbers are right, and signing off the result.
- Conclusions or recommendations that affect people (hiring, pay, performance, dismissal), and anything requiring legal or ethical decisions.

**Sample data:** none needed.
**What it means:** AI speeds up first drafts; I stay accountable for the number, and the data stays protected.
**Likely follow-ups:**
- *What if AI and Excel disagree?* Reconcile row by row until the cause is found (Q32), never just pick the nicer number.
- *What if the company bans external AI?* Use the approved internal tool, or ask for logic and pseudocode only, no data.

**Common mistakes:** Trusting code that "runs without errors" (it can run and still be wrong); pasting real employee files; no tests; no record of how the report was built.

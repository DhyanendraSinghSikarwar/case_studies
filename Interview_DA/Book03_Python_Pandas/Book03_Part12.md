# Book 3 — Python & pandas for Analysts | Part 12: How to Develop Python Skills 🟢🟡

**Target:** 20 questions | **Actual:** 29 questions
**Scope:** learning-journey interview questions plus the zero-to-job-ready Python and pandas skill-development plan (roadmap, daily plan, free resources, datasets, mini-projects, self-check tests).

### Q1 ⭐⭐⭐ 🟢 How did you learn Python, and how long did it take you?
**Asked at:** commonly asked (no company-specific report found); a standard opener for career switchers.
**What the interviewer is checking:** Is your learning structured and honest, and did you apply it to real data, not only watch videos?
**Say this in the interview:** "I learned in stages: Python basics first, then pandas for data, then small HR-style projects. I practised most days for about 4 months before I felt comfortable with everyday analysis, and I still learn on every new dataset." This is a template. Replace the stages, resources and months with what you truly did; never claim a course or project you did not do.
**Explain simply:**
- **Stage 1 (weeks 1-3):** Python basics: variables (named boxes for values), lists, loops, `if` conditions, functions (reusable steps).
- **Stage 2 (weeks 4-8):** pandas (the Python library for tables, like Excel in code): load a file, filter, clean, group, merge.
- **Stage 3 (weeks 9-16):** a real project on HR data, plus charts and a short write-up.
- Honest message: basics take months of regular practice; mastery comes from using it at work.
**Likely follow-ups:**
- *Which resource helped most?* Name one or two you really used (see Q7).
- *What is still weak?* Name one topic honestly (see Q2).
**Common mistakes:** Listing ten courses and no project; claiming "two weeks"; giving a timeline you cannot back with something you built.

### Q2 ⭐⭐⭐ 🟢 How would you rate yourself in Python out of 10, and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Self-awareness: can you rate yourself with evidence, not "10/10" or "3/10"?
**Say this in the interview:** "I would say 6 out of 10 for data-analyst work. I am comfortable cleaning data, filtering, grouping, merging and making charts in pandas. I am still building depth in writing my own functions and in performance on large files." This is a template. Pick your own number (5 to 7 is typical for a fresher) and name strengths you have actually shown.
**Explain simply:**
- Give 2 strengths, each backed by something you did, and 1 named gap with what you are doing about it.
- A self-check rubric you can use (be honest, answer from memory without searching): can you load a CSV, handle blank values, remove duplicates, filter rows, group and average, merge two tables, and explain each line aloud? 3 or 4 of 6 is about a 4; all 6 without help is about a 6 or 7.
- 9 or 10 invites hard follow-ups you may not survive.
**Likely follow-ups:**
- *Why not higher?* Name a real gap: "I have not yet written code for large datasets."
- *Prove the number.* Walk through one analysis end to end (see Q4).
**Common mistakes:** Claiming 9/10 then missing a basic `groupby`; being vague ("average"); rating low with no plan.

### Q3 ⭐⭐⭐ 🟢 You come from HR with no programming background. How did you learn Python?
**Asked at:** commonly asked (no company-specific report found); typical for HR-to-analytics switchers.
**What the interviewer is checking:** Can you learn technical material alone, and do you turn HR knowledge into an advantage?
**Say this in the interview:** "I started from questions HR already asks: why do people leave, which team has the highest absence, is pay fair. I learned just enough Python to answer each one, and I did the same analysis first in Excel so I could see that the code gave the same answer. HR gave me business sense; practice gave me the method." Template: replace with your real first question and tools.
**Explain simply:**
- Learn through questions you care about; Python becomes a tool, not a subject.
- Compare with Excel: if the code and the Excel result match, you understand it.
- You do not need to become a software engineer; analyst Python is mostly pandas (see Q14).
- Your HR knowledge (what a sensible attrition rate looks like) catches errors that pure coders miss.
**Likely follow-ups:**
- *How many hours a week?* Be specific and true (see Q9).
- *Did you get stuck?* Yes; give one example and the fix (see Q5).
**Common mistakes:** Apologising for the HR background; saying "I have no programming background" and stopping, instead of showing what you built.

### Q4 ⭐⭐⭐ 🟢 Walk me through a Python or pandas project you built from start to finish.
**Asked at:** commonly asked (no company-specific report found); Python project-based questions are reported for some analytics firms (Tiger Analytics Glassdoor snippet, contents not read, unverified).
**What the interviewer is checking:** Can you tell a clear story: question, data, cleaning, analysis, result, action?
**Say this in the interview:** "I wanted to know which department loses most people. I loaded the employee file, cleaned blanks and duplicates, turned the Yes/No leaver column into 1 and 0, grouped by department, and found Sales had the highest attrition. I then checked it against Excel and wrote two recommendations." Use YOUR real project; the steps below are the structure, not a story to claim. Small project ideas if you have none yet: attrition by department, absence patterns by weekday, hiring funnel conversion, salary gap by gender and grade.
**Explain simply:**
- Structure: **Question, Data, Cleaning, Analysis, Result, What changed or what you would do next.**
- Mention one problem you hit and how you fixed it; interviewers trust that.
- Quote numbers, but only real ones from your project.
**Sample data:** 8 employees (department, left_company Yes/No).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "department": ["Sales", "Sales", "Sales", "Support", "Support", "Support", "IT", "IT"],
    "left_company": ["Yes", "No", "Yes", "No", "No", "Yes", "No", "No"],
})

# turn Yes/No into 1/0 so the average becomes the attrition rate
employees["left_flag"] = (employees["left_company"] == "Yes").astype(int)

# attrition rate and headcount per department
attrition_by_department = employees.groupby("department")["left_flag"].agg(["count", "mean"])
attrition_by_department = attrition_by_department.rename(columns={"count": "headcount", "mean": "attrition_rate"})

print(attrition_by_department.sort_values("attrition_rate", ascending=False))
```
**Output:**
```
            headcount  attrition_rate
department                           
Sales               3        0.666667
Support             3        0.333333
IT                  2        0.000000
```
**What it means:** Sales lost 2 of 3 people (67%). With tiny sample sizes you would say "worth investigating", not "proven".
**Likely follow-ups:**
- *What would you do differently?* Add tenure and manager as factors.
- *How did you validate it?* Cross-check one department by hand in Excel.
**Common mistakes:** Describing tools instead of the business question; no result or recommendation; claiming a project you cannot explain line by line.

### Q5 ⭐⭐⭐ 🟡 Which Python topic did you find hardest, and how did you overcome it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Honesty about difficulty and a concrete method for getting past it.
**Say this in the interview:** "`groupby` and `merge` were hardest at first, because I could not picture what happens to the rows. I fixed it by working on a 5-row table, drawing the result on paper, then running the code and comparing. Once I could predict the output, it clicked." Template: swap in your own hardest topic. Common honest answers: groupby, merge types, dates, `loc` vs `iloc`, copy warnings.
**Explain simply:**
- **groupby:** split rows into groups, calculate per group, put the results back in one table (like a PivotTable).
- **merge:** join two tables on a shared column (like VLOOKUP); `how="left"` keeps every row of the left table.
- The method generalises: tiny data, predict the result, run, compare, repeat.
- Show the fix, not only the struggle.
**Likely follow-ups:**
- *What would you tell a beginner?* Always predict the output before running.
- *Anything still hard?* Name one real gap.
**Common mistakes:** Saying "nothing was hard"; naming a topic and giving no method; picking a topic far beyond analyst level to look clever.

### Q6 ⭐⭐⭐ 🟡 Which Python libraries and functions have you actually used in a real analysis, and what was the result?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Real hands-on use, not a memorised list of library names.
**Say this in the interview:** "Mostly pandas: `read_csv`, `fillna`, `drop_duplicates`, `merge`, `groupby`, `value_counts`; matplotlib or seaborn for charts. In my attrition analysis, merging the exit survey showed pay was the top stated reason." Only list what you have really run; the result must be your own.
**Explain simply:**
- **pandas:** tables. **numpy:** fast number arrays (pandas uses it inside). **matplotlib/seaborn:** charts.
- Name a function plus what it did to the data, plus the outcome.
- Stop at what you can explain; "I have not used scikit-learn" is a fine answer for an analyst role.
**Sample data:** 5 employees with blank values, plus a 3-row exit survey.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5],
    "department": ["Sales", "Sales", "Support", "Support", None],
    "salary": [50000, 54000, None, 42000, 46000],
})
exit_survey = pd.DataFrame({
    "employee_id": [1, 3, 4],
    "reason": ["Pay", "Manager", "Pay"],
})

# fix missing values and remove duplicate rows
employees["department"] = employees["department"].fillna("Unknown")
employees["salary"] = employees["salary"].fillna(employees["salary"].median())
employees = employees.drop_duplicates()

# bring the exit reason next to each employee (like VLOOKUP)
combined = employees.merge(exit_survey, on="employee_id", how="left")

# average salary per department
print(combined.groupby("department")["salary"].mean())
print(combined["reason"].value_counts())
```
**Output:**
```
department
Sales      52000.0
Support    45000.0
Unknown    46000.0
Name: salary, dtype: float64
reason
Pay        2
Manager    1
Name: count, dtype: int64
```
**What it means:** Blanks are filled (median salary, a middle value not pulled by extremes), departments are compared, and Pay is the most common exit reason (2 of 3 who answered). Employees who did not leave have no reason, so `value_counts` skips them.
**Likely follow-ups:**
- *Why median, not mean?* Outliers do not distort it.
- *Why `how="left"`?* To keep all employees, not only those with a survey.
**Common mistakes:** Listing libraries never used; filling blanks without telling anyone; forgetting that a left merge creates blanks.

### Q7 ⭐⭐ 🟢 Which free resources would you recommend to a beginner learning Python for data analysis?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know good resources and have you used them, or are you name-dropping?
**Say this in the interview:** "I would pick one structured course and one practice source, not ten. For example Kaggle Learn's Python and Pandas courses, the official 'Ten minutes to pandas' page, and practice on a real HR dataset." Recommend only what you actually used.
**Explain simply:** All below are from memory, unverified, check the link before you commit time.
- **Kaggle Learn** (kaggle.com/learn): short free Python and Pandas lessons with exercises in the browser.
- **Python official tutorial** (docs.python.org/3/tutorial): accurate, a bit dry.
- **pandas docs, "10 minutes to pandas"** (pandas.pydata.org): quick tour of the core.
- **Automate the Boring Stuff with Python** (automatetheboringstuff.com): free online book, friendly for beginners.
- **Python for Data Analysis** by Wes McKinney (wesmckinney.com/book): author's free online edition; the deeper reference.
- **freeCodeCamp** and **Harvard CS50P** (free on YouTube/edX): full beginner courses.
- **Google Colab** (colab.research.google.com): free notebook in the browser, no installation.
- Practice: HackerRank, StrataScratch (limited free tier), Kaggle datasets.
**Likely follow-ups:**
- *Which one first?* A structured course, then projects.
- *Video or book?* Both, but always type the code yourself.
**Common mistakes:** Hoarding courses ("tutorial hell"); recommending paid resources as free; watching without typing.

### Q8 ⭐⭐ 🟢 In what order did you study Python topics, and why that order?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A logical, analyst-focused sequence; you did not start with advanced topics.
**Say this in the interview:** "Basics, then pandas, then cleaning, then analysis and charts, then a project. Each step needs the one before it, and I skipped web development and machine learning because analyst work does not need them first." Adapt to the order you truly followed.
**Explain simply:** This is the zero-to-job-ready roadmap.
- **Weeks 1-3, basics:** variables, strings, numbers, lists, dictionaries, `if`, loops, functions.
- **Weeks 4-5, pandas core:** DataFrame (a table), `read_csv`, `head`, `info`, select columns, filter rows, sort.
- **Weeks 6-7, cleaning:** blanks, duplicates, wrong data types, text clean-up, dates.
- **Weeks 8-9, analysis:** `groupby`, `merge`, pivot tables, `value_counts`.
- **Weeks 10-11, charts and Excel/SQL links:** matplotlib or seaborn; read and write Excel.
- **Weeks 12-14, projects** (see Q4) and **weeks 15-16, interview practice:** timed problems, explaining code aloud.
- Why this order: you cannot clean a table you cannot load, and you cannot explain results you cannot chart.
**Likely follow-ups:**
- *What did you skip?* Classes, web frameworks, deep learning (for later, if ever).
- *Would you change it?* Start projects earlier.
**Common mistakes:** Spending a month on object-oriented programming; learning libraries before basics; never finishing a project.

### Q9 ⭐⭐ 🟢 How much time do you spend practising Python each week, and roughly how many problems have you solved?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Consistency and honesty; a believable number, not a boast.
**Say this in the interview:** "About 6 to 8 hours a week, mostly in short daily sessions plus one longer weekend block, and roughly 100 practice problems and 3 small projects so far." These numbers are placeholders. Quote your own true hours and count; if you are early in the journey, say the plan you are following.
**Explain simply:** A daily practice plan (about 1 hour on weekdays, 2 hours on weekend):
- **10 min:** review yesterday's code, retype one snippet from memory.
- **35 min:** one new topic from the roadmap (Q8), typing every example.
- **15 min:** 1 or 2 small problems on the topic, solved without looking.
- **Weekend:** 2 hours on your project; Sunday, write down 3 things learned.
- Maths: 5 weekdays x 1 hour + 3 hours weekend = about 8 hours a week, about 32 hours a month.
- Consistency beats length: 1 hour daily beats 7 hours on Sunday.
**Likely follow-ups:**
- *Is the count the point?* No; quality and explaining solutions matter more.
- *How do you track it?* A simple log (date, topic, minutes).
**Common mistakes:** Inflating the problem count; saying "I practise daily" with nothing to show; counting video watching as practice.

### Q10 ⭐⭐ 🟢 Which practice datasets have you worked with in pandas?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** You used real, messy data, and you know how to start with a new file.
**Say this in the interview:** "The IBM HR Analytics attrition dataset, the Titanic dataset for cleaning, and a sales dataset for grouping and merging. With any new file I first check shape, the first rows, data types, blanks and the main category counts." Name only datasets you really opened.
**Explain simply:** From memory, unverified, check the link before relying on them.
- **IBM HR Analytics Employee Attrition & Performance** (Kaggle): about 1,470 rows, a fictional dataset made by IBM data scientists; the standard HR practice file.
- **Titanic** (Kaggle competition data): classic for missing values and grouping.
- **Palmer Penguins** and **tips** (available through seaborn's `load_dataset`, needs internet): small and clean, good for first charts.
- **Superstore sales** style retail datasets (Kaggle): grouping, dates, merging.
- **Gapminder** (gapminder.org): countries over time.
- Also useful: your own anonymised or made-up HR data (attendance, payroll, hiring funnel); never practise on real employee data you are not allowed to use.
**Sample data:** 5 rows shaped like the attrition file.
**Code (what you write in the interview):**
```python
import pandas as pd

# stands in for pd.read_csv("employee_attrition.csv")
employees = pd.DataFrame({
    "Age": [41, 49, 37, 33, 27],
    "Department": ["Sales", "R&D", "R&D", "R&D", "R&D"],
    "MonthlyIncome": [5993, 5130, 2090, 2909, 3468],
    "Attrition": ["Yes", "No", "Yes", "No", "No"],
})

# first look at any new dataset
print(employees.shape)
print(employees.head(3))
employees.info()
print(employees["Attrition"].value_counts())
```
**Output:**
```
(5, 4)
   Age Department  MonthlyIncome Attrition
0   41      Sales           5993       Yes
1   49        R&D           5130        No
2   37        R&D           2090       Yes
<class 'pandas.DataFrame'>
RangeIndex: 5 entries, 0 to 4
Data columns (total 4 columns):
 #   Column         Non-Null Count  Dtype
---  ------         --------------  -----
 0   Age            5 non-null      int64
 1   Department     5 non-null      str  
 2   MonthlyIncome  5 non-null      int64
 3   Attrition      5 non-null      str  
dtypes: int64(2), str(2)
memory usage: 292.0 bytes
Attrition
No     3
Yes    2
Name: count, dtype: int64
```
**What it means:** 5 rows, 4 columns, no blanks, 2 leavers. Output shown is from pandas 3.0.5; older pandas 2.x prints `DataFrame` as `pandas.core.frame.DataFrame` and text columns as `object`.
**Likely follow-ups:**
- *What did you find in it?* Quote a real finding from your own run.
- *Any quality issues?* Mention blanks, duplicates, odd values you checked.
**Common mistakes:** Naming datasets never opened; skipping the first-look checks; using confidential employee data.

### Q11 ⭐⭐ 🟢 How would you set up a free Python and Jupyter environment on your own laptop?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Practical comfort: can you get a working workspace without help?
**Say this in the interview:** "Install Python from python.org, create a virtual environment (a private folder of libraries for one project), install pandas and JupyterLab with pip, and start Jupyter. If I do not want any installation, I use Google Colab in the browser."
**Explain simply:** Commands you type in a terminal (Command Prompt or PowerShell on Windows). I confirmed `python -m venv` creates an environment on a machine here; the `pip install` and `jupyter lab` steps were not run here (from memory, unverified).
```
python -m venv hr-env
hr-env\Scripts\activate            (Windows)
source hr-env/bin/activate         (Mac or Linux)
pip install pandas matplotlib jupyterlab
jupyter lab
```
- **Virtual environment:** keeps one project's library versions separate from others.
- **JupyterLab:** opens in your browser; code and results sit in cells (blocks you run one at a time).
- **Alternatives:** Anaconda (one big installer with most data libraries included), Google Colab (free, browser, nothing to install), VS Code with the Python extension.
- Check it works: `import pandas as pd` then `pd.__version__` in a cell.
**Likely follow-ups:**
- *Why a virtual environment?* So an upgrade for one project does not break another (see Q29).
- *Colab vs local?* Colab is fastest to start; local gives you files and control.
**Common mistakes:** Installing into the wrong Python; forgetting to activate the environment; installing everything globally.

### Q12 ⭐⭐ 🟢 What HR questions can Python answer that Excel struggles with?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know when Python genuinely adds value instead of replacing Excel for show?
**Say this in the interview:** "Python helps when data is big, comes from many files, or the work repeats every month. Examples: combining 12 monthly attendance files, cleaning messy text, tenure-band attrition across years, and re-running the whole analysis with one click next month. Excel is still fine for small one-off tables."
**Explain simply:**
- **Many files:** loop over 12 monthly files and stack them into one table.
- **Large data:** Excel slows down near about a million rows; pandas handles bigger tables more comfortably.
- **Repeatable:** the script is a saved recipe; Excel manual steps are easy to get wrong or forget.
- **Messy text and dates:** one cleaning rule applied to every row.
- **Deeper analysis:** statistics, forecasting and charts of any kind (see Book 5).
**Sample data:** 6 employees with joining and leaving dates (blank leaving date = still employed).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5, 6],
    "joining_date": pd.to_datetime(["2022-01-10", "2023-03-05", "2021-07-19", "2024-02-01", "2022-11-30", "2023-08-14"]),
    "leaving_date": pd.to_datetime(["2023-02-01", None, "2024-06-30", "2024-09-15", None, None]),
})

# tenure in years; people still employed are measured up to a fixed report date
report_date = pd.Timestamp("2025-01-01")
end_date = employees["leaving_date"].fillna(report_date)
employees["tenure_years"] = (end_date - employees["joining_date"]).dt.days / 365

# group tenure into bands and count leavers in each band
employees["tenure_band"] = pd.cut(employees["tenure_years"], bins=[0, 1, 2, 10], labels=["0-1 yr", "1-2 yrs", "2+ yrs"])
employees["left"] = employees["leaving_date"].notna()
print(employees.groupby("tenure_band", observed=True)["left"].agg(["count", "sum"]))
```
**Output:**
```
             count  sum
tenure_band            
0-1 yr           1    1
1-2 yrs          3    1
2+ yrs           2    1
```
**What it means:** `count` is people in each tenure band, `sum` is how many left. The same steps work for 6 rows or 600,000.
**Likely follow-ups:**
- *Would you replace Excel?* No; use Excel for quick views and sharing, Python for scale and repetition.
- *What about Power BI?* Complements it (see Book 4).
**Common mistakes:** Saying Python is "better" without a reason; using it for a 20-row table; forgetting that "still employed" rows have blank dates.

### Q13 ⭐⭐ 🟢 You already know Excel and SQL. What carried over to pandas, and what did you have to unlearn?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you map known skills to new ones and spot the traps in the switch?
**Say this in the interview:** "The thinking carried over: VLOOKUP became `merge`, PivotTable and GROUP BY became `groupby`, WHERE became a filter. What I unlearned was clicking on cells: in pandas you work on whole columns at once, and you must write down every step."
**Explain simply:**

| Excel | SQL | pandas |
|---|---|---|
| VLOOKUP / XLOOKUP | LEFT JOIN | `merge(how="left")` |
| PivotTable | GROUP BY | `groupby(...).agg(...)` |
| Filter | WHERE | `df[df["col"] > x]` |
| Formula dragged down | calculated column | `df["new"] = df["a"] * df["b"]` |
| Remove Duplicates | DISTINCT | `drop_duplicates()` |

- **Unlearn 1:** no cell addresses like B2; you name columns.
- **Unlearn 2:** no formula dragging; one line works on every row.
- **Unlearn 3:** blanks are `NaN` (not a number marker), and they quietly skip in averages.
- **Unlearn 4:** nothing is saved or visible until you print or write it out.
**Sample data:** 4 employees plus a department bonus table.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [1, 2, 3, 4],
    "department": ["Sales", "Sales", "IT", "IT"],
    "salary": [50000, 54000, 70000, 66000],
})
bonus_table = pd.DataFrame({
    "department": ["Sales", "IT"],
    "bonus_percent": [10, 5],
})

# Excel VLOOKUP / SQL LEFT JOIN
with_bonus = employees.merge(bonus_table, on="department", how="left")

# Excel formula dragged down a column: pandas does the whole column at once
with_bonus["bonus_amount"] = with_bonus["salary"] * with_bonus["bonus_percent"] / 100

# Excel PivotTable / SQL GROUP BY
print(with_bonus.groupby("department")["bonus_amount"].sum())
```
**Output:**
```
department
IT        6800.0
Sales    10400.0
Name: bonus_amount, dtype: float64
```
**What it means:** Total bonus is 10,400 for Sales and 6,800 for IT, the same answer a VLOOKUP plus PivotTable would give.
**Likely follow-ups:**
- *Biggest trap?* A merge key with duplicates multiplies rows; check the row count after merging.
- *Where is Excel still better?* Quick looks, sharing, manual edits.
**Common mistakes:** Writing loops over rows where one column formula works; not checking row counts after a merge.

### Q14 ⭐⭐ 🟢 How much Python do you really need for a data analyst role, and where do you stop and leave the rest to data scientists?
**Asked at:** commonly asked (no company-specific report found). Internal research (research/market_skills_2026.md) found Python in about 32% of sampled analyst job descriptions pooled; see that file for the sample.
**What the interviewer is checking:** Realistic scope: you know the analyst toolkit and you do not pretend to be a data scientist.
**Say this in the interview:** "For analyst work I need pandas for cleaning, joining and summarising, basic charts, reading and writing Excel and CSV, and enough Python to write small functions and loops. Machine learning model building, deep learning and production code belong to data scientists and engineers; I understand what they do but I do not claim it."
**Explain simply:** A self-check, "job-ready" list. You are ready when you can do these without searching, on a new dataset, in a timed hour:
- Load a file and run first-look checks (shape, types, blanks, duplicates).
- Clean: fill or drop blanks, fix types and dates, tidy text.
- Filter, sort, `groupby`, `merge`, pivot.
- Make 2 clear charts and write 3 sentences of finding.
- Explain every line you wrote, and check your result another way (Excel or SQL).
- **Stop here:** model tuning, neural networks, writing web apps, deploying code. Learn them later only if the role needs them (see Book 9 for ML).
**Likely follow-ups:**
- *Is SQL or Python more important?* Usually SQL first, Python second (see Book 2).
- *Would you learn ML?* Basics for understanding, in the next phase.
**Common mistakes:** Over-claiming ML skills; under-learning pandas basics; saying "I know everything".

### Q15 ⭐⭐ 🟢 How do you use AI assistants to learn Python without depending on them?
**Asked at:** commonly asked (no company-specific report found); sources suggest "use AI as a tutor, not a code generator" is a common stance (DataCamp webinar snippet, 2025-26, unverified).
**What the interviewer is checking:** Do you understand your code, or only paste it?
**Say this in the interview:** "I use AI as a tutor. I try first myself, then ask it to explain an error or review my code, and I never paste code I cannot explain line by line. I verify results on a small example or in Excel. In a live test I would rely on my own knowledge." Describe your real habits honestly.
**Explain simply:**
- **Try first:** write your attempt, even if wrong, before asking.
- **Ask for explanations:** "Explain this line", "Why does this error appear?", not "Write the whole solution".
- **Predict, then run:** guess the output before running AI-suggested code.
- **Verify:** small sample, hand calculation, or Excel check; AI can be confidently wrong or use outdated functions.
- **Weekly no-AI session:** solve problems with only documentation, to test yourself.
- **Privacy:** never paste real employee data into an AI tool; use made-up or anonymised samples.
**Likely follow-ups:**
- *What if AI gives wrong code?* Check against the official docs and a small test.
- *Is using AI cheating in interviews?* Follow the interview rules; if not allowed, do not use it.
**Common mistakes:** Pasting AI code you cannot explain; sharing confidential data; never practising without it.

### Q16 ⭐⭐ 🟡 How do you learn a pandas function or library you have never used before?
**Asked at:** commonly asked (no company-specific report found); a self-reliance check.
**What the interviewer is checking:** Can you teach yourself a new tool in a repeatable way, not by copy-pasting from the internet?
**Say this in the interview:** "I follow the same four steps: read the official help for what goes in and what comes out, run it on a tiny table where I can predict the answer by hand, change one option at a time to see what moves, then try it on the real data and check the result. This is my own routine; the example below is just one illustration."
**Explain simply:**
- **Help first:** in Jupyter (a notebook where you run code in small pieces), type the function name followed by `?`, or call `help(...)`. It lists the inputs (called parameters) and what comes back.
- **Tiny table:** 4 rows you can calculate in your head, so you can tell if the function did what you expected.
- **One change at a time:** for `rank`, try `ascending=False`, then `method="dense"`, and watch the ties.
- **Then real data,** and note the function in a personal cheat sheet with one HR example.
**Sample data:** four employees with salaries (see code).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "Kiran"],
    "salary": [50000, 60000, 45000, 55000],
})

# In Jupyter, type employees["salary"].rank? to read the help. Here I just test it
# on a tiny table where I can predict the answer by hand.
employees["salary_rank"] = employees["salary"].rank(ascending=False)
print(employees)
```
**Output:**
```
    name  salary  salary_rank
0   Asha   50000          3.0
1   Ravi   60000          1.0
2  Meena   45000          4.0
3  Kiran   55000          2.0
```
**What it means:** Ravi earns most so he gets rank 1. I could predict this by hand, so I trust the function and can now use it on the full payroll.
**Likely follow-ups:** 1) *What if the docs are confusing?* Read the "Examples" section at the bottom, or search the error text, then test the idea on the tiny table. 2) *Do you use AI?* As a tutor to explain, then I verify by running (see Q15).
**Common mistakes:** Pasting a Stack Overflow or chatbot answer straight onto real data without a tiny test; never reading the parameters (for example missing that ties get the average rank by default).

### Q17 ⭐⭐ 🟡 How do you check that your pandas output is correct when there is no answer key?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you validate your own results, the habit that separates a trusted analyst from a risky one?
**Say this in the interview:** "I never trust a result just because the code ran. I reconcile it: do the parts add up to the total I get another way, does the row count make sense, are there hidden duplicates, and does one group match when I calculate it separately. Finally I ask if the number is sensible for HR, for example attrition of 150% is impossible."
**Explain simply:**
- **Reconcile:** the sum of department totals must equal the overall total.
- **Count rows before and after** every filter or merge. A merge that adds rows usually means duplicate keys (Q20).
- **Spot-check one group** with a separate, simpler calculation, or compare with Excel on a small slice.
- **Sanity check against business sense:** negative headcount, tenure of 80 years, percentages above 100.
- **Look for blanks (missing values)**; they are silently skipped by `sum` and `mean`, which can hide a problem.
**Sample data:** five employees (see code).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "emp_id": [1, 2, 3, 4, 5],
    "department": ["Sales", "Sales", "HR", "HR", "IT"],
    "salary": [50000, 60000, 45000, 55000, 70000],
})
salary_by_department = employees.groupby("department")["salary"].sum()

# Check 1: parts add up to the whole
print(employees["salary"].sum(), salary_by_department.sum())

# Check 2: row count and hidden duplicates
print(len(employees), employees["emp_id"].nunique())

# Check 3: recompute one group with a simple filter
print(employees[employees["department"] == "Sales"]["salary"].sum())
```
**Output:**
```
280000 280000
5 5
110000
```
**What it means:** Total matches the sum of the parts, 5 rows have 5 unique employee IDs (no duplicates), and Sales equals 50,000 + 60,000. The result is reconciled.
**Likely follow-ups:** 1) *What if a check fails?* Stop, find which step changed the numbers by printing row counts after each step. 2) *Other check?* Compare with the source system or Excel pivot for one month.
**Common mistakes:** Checking only that no error appeared; forgetting that blanks are skipped; comparing two numbers that came from the same flawed step.

### Q18 ⭐⭐ 🟡 How would you prepare for a live Python coding round in two weeks?
**Asked at:** commonly asked (no company-specific report found). Company reports in research/interview_processes.md describe Python in the technical rounds of several service and analytics firms (for example Accenture, Tiger Analytics, Amazon BA, HSBC) as basic Python and pandas, single-anecdote level.
**What the interviewer is checking:** Realistic planning and knowing what live rounds actually test.
**Say this in the interview:** "In two weeks I would not learn new topics; I would drill the ones that appear most: filtering, groupby, merge, missing values, duplicates and string/date cleaning in pandas, plus basic loops, lists and dictionaries. Every day I would solve problems while typing code live, then explain it aloud."
**Explain simply:** (a template; adjust to your hours, roughly 1.5 to 2 hours a day)
- **Days 1-3:** Python basics: lists, dictionaries, loops, functions, string tricks (count duplicates, reverse a string).
- **Days 4-8:** pandas core: read a CSV, filter, sort, `groupby`, `merge`, `fillna`, `drop_duplicates`, `value_counts`, dates. Use an HR file (attrition, attendance).
- **Days 9-11:** mixed practice on a timer, 20-30 minutes a problem, without searching.
- **Days 12-13:** mock interview with a friend or by recording yourself explaining; redo failed problems.
- **Day 14:** light revision of your cheat sheet; sleep.
- Practice on free platforms such as StrataScratch, DataLemur, HackerRank (from memory, unverified: check what is free today).
**Likely follow-ups:** 1) *What if you only have 1 hour a day?* Cut breadth: skip advanced topics, keep groupby, merge, cleaning. 2) *How do you know you are ready?* Q27's self-test.
**Common mistakes:** Watching videos instead of typing; memorising answers instead of the method; never practising speaking while coding.

### Q19 ⭐⭐ 🟡 What do you do in a live coding test when you blank on syntax or hit an error you cannot fix?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Calm problem solving and communication. Interviewers know people forget syntax; they watch how you recover.
**Say this in the interview:** "I say it aloud: 'I forget the exact name, but I know I need a function that sorts rows by a column.' If I can look things up in the test, I check the help. If not, I explain the logic, write the closest version, and ask if I may continue. For errors I read the last line of the message, check the data type of each column, and test the step on 3 rows."
**Explain simply:**
- **Do not freeze silently.** Say the plan in plain words first: filter, group, count. The logic carries most marks.
- **Find the name** if allowed: `dir(...)` lists what an object can do; `help(...)` explains it.
- **Read the error from the bottom up:** the last line names the problem (KeyError means a wrong column name, TypeError often means a wrong data type).
- **Shrink the problem:** run the failing line on a tiny sample, or print `df.columns` and `df.dtypes`.
- **If stuck for 3-4 minutes,** ask a clarifying question or for a hint, politely, and move on.
**Sample data:** two employees (see code).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"name": ["Asha", "Ravi"], "salary": [50000, 60000]})

# Blank on a method name? List what a Series can do, filtered by a keyword
print([name for name in dir(employees["salary"]) if "sort" in name])
```
**Output:**
```
['argsort', 'searchsorted', 'sort_index', 'sort_values']
```
**What it means:** `sort_values` is the one I wanted. This trick only works if the test allows running code; if it is a whiteboard, describe the step in words.
**Likely follow-ups:** 1) *Would you ask the interviewer?* Yes, about the problem, not for the whole answer. 2) *Can you Google?* Ask first; many rounds allow documentation.
**Common mistakes:** Going silent; deleting everything and restarting; panicking over a typo; guessing random fixes.

### Q20 ⭐⭐ 🟡 Tell me about a time your Python code gave a wrong result and how you found the bug.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Honesty, debugging method, and whether you learned a lasting lesson.
**Say this in the interview:** This is a story template; use a bug you really had, never an invented one. Example shape: "My payroll total after combining two tables was higher than the real payroll. I printed the totals before and after the merge and saw the total jumped. One employee had two training records, so the merge copied that salary twice. I summarised the training table to one row per employee first, and the total matched again. Now I always check row counts and totals around every merge."
**Explain simply:**
- Structure: **what happened, how I noticed, how I found the cause, the fix, what I do now.**
- The most common real cause is a merge (joining two tables on a shared column) on a key that repeats, which duplicates rows.
- Detection came from a reconciliation check (Q17), not from an error message; wrong results often raise no error.
- Other genuine causes: numbers stored as text, blanks skipped, wrong filter condition, date format mix-ups.
**Sample data:** employees and a training table where employee 2 appears twice (see code).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "emp_id": [1, 2, 3],
    "salary": [50000, 60000, 45000],
})
# Training table: Ravi (emp_id 2) attended two courses
training = pd.DataFrame({
    "emp_id": [1, 2, 2, 3],
    "course": ["Excel", "SQL", "Python", "Excel"],
})

merged = employees.merge(training, on="emp_id")
print("Payroll before:", employees["salary"].sum())
print("Payroll after merge:", merged["salary"].sum())

# Fix: one row per employee before merging
courses_per_employee = training.groupby("emp_id").size().reset_index(name="courses")
fixed = employees.merge(courses_per_employee, on="emp_id")
print("Payroll after fix:", fixed["salary"].sum())
```
**Output:**
```
Payroll before: 155000
Payroll after merge: 215000
Payroll after fix: 155000
```
**What it means:** The merge counted Ravi's 60,000 twice (155,000 + 60,000 = 215,000). After reducing the training table to one row per employee, payroll is correct again.
**Likely follow-ups:** 1) *How do you prevent it?* Check keys are unique, or merge with `validate="one_to_many"` style checks (from memory, check docs). 2) *Did anyone act on the wrong number?* Answer truthfully; caught before sharing is the best story.
**Common mistakes:** Saying "I never make mistakes"; blaming the data without proof; telling a bug story with no lesson.

### Q21 ⭐⭐ 🟡 What is your plan to improve your Python over the next three months?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Direction, realism, and whether your plan ties to the job.
**Say this in the interview:** "Month one I sharpen the core I use daily: cleaning, groupby, merge, dates. Month two I build two portfolio projects on HR-style data and push them to GitHub. Month three I add what the role needs, such as plotting and automating a weekly report, and I do timed practice. I check progress with a self-test every four weeks." (Adjust to your real hours and goals.)
**Explain simply:**
- **Weeks 1-4, depth in basics:** 45 minutes on weekdays, 2 hours at weekends; 30+ small problems.
- **Weeks 5-8, projects:** one cleaning-and-summary project and one attrition analysis with charts; write a short findings note for each.
- **Weeks 9-12, job mode:** timed mocks, a script that automates a recurring report, read other people's notebooks on Kaggle (from memory, unverified: check the link).
- **Measure:** problems solved, projects finished, mock-test score; not hours watched.
- **Stop line:** analyst level; leave machine learning for later (Q14).
**Likely follow-ups:** 1) *What if you fall behind?* Cut scope, never the daily habit. 2) *What after three months?* Learn what the team uses, for example plotting libraries or database connections.
**Common mistakes:** A plan with ten courses and no output; promising 4 hours a day while working full time (Q25).

### Q22 ⭐ 🟢 Which platforms have you practised Python on (HackerRank, LeetCode, Kaggle, StrataScratch)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Have you actually practised, and do you know which platform fits an analyst?
**Say this in the interview:** Only name platforms you really used. Example: "I used Kaggle for datasets and its short Learn lessons, and StrataScratch for interview-style pandas and SQL problems. I tried HackerRank for basics but I do not practise heavy algorithm problems on LeetCode, because analyst rounds focus on data manipulation."
**Explain simply:**
- **Kaggle:** datasets, free notebooks, short courses; good for projects (from memory, unverified, check the link).
- **StrataScratch and DataLemur:** interview-style data questions with real company flavour; some content is free, some paid (from memory, unverified).
- **HackerRank:** basic Python, string and list problems, and the format many companies use for online tests.
- **LeetCode:** algorithm practice; useful for easy-level lists and strings, less so for analyst roles.
- Prefer platforms that give you a table to manipulate over pure puzzle sites.
**Likely follow-ups:** 1) *How many problems?* Give an honest number (Q9). 2) *Favourite problem?* Describe one you truly solved.
**Common mistakes:** Listing platforms you only signed up for; claiming a ranking you do not have.

### Q23 ⭐ 🟢 Have you shared your Python work publicly, for example on GitHub or Kaggle?
**Asked at:** commonly asked (no company-specific report found); a differentiator, not a requirement.
**What the interviewer is checking:** Evidence of real work you can show, and basic habits like clean code and documentation.
**Say this in the interview:** Be honest. If yes: "Yes, I have two notebooks on GitHub, an attrition analysis and a data-cleaning project, each with a short README that states the question, the data source and the finding." If not yet: "Not yet publicly, since my work so far used company data I cannot share, but I am building two public projects on open datasets this month."
**Explain simply:**
- **GitHub** is a free site where you store code and notebooks so others can view them; a **README** is the front-page description.
- Each project should state: question, data source, steps, 2-3 findings, how to run it.
- Never upload confidential employee data. Use public or made-up data.
- Keep a clean notebook: run top to bottom, remove failed experiments, add short comments.
**Likely follow-ups:** 1) *Walk me through one.* Use the Q4 structure. 2) *Is Git hard?* Learn four commands: add, commit, push, and pull.
**Common mistakes:** Publishing real employee data; an empty repository; a notebook full of errors and no explanation.

### Q24 ⭐ 🟢 Do Python certifications help, and have you done any?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Perspective: do you value proof of skill over paper?
**Say this in the interview:** Answer with what is true for you. Example: "A certificate helps a little to get past resume filters and shows discipline, but interviews are decided by live coding and projects. I have done [name only what you completed]; what I would rather show you is my project."
**Explain simply:**
- Certificates can help with screening, especially for career switchers with no data title yet.
- They do not replace practice: live rounds test whether you can write code now.
- Examples of options (from memory, unverified, check the current offering and cost): Python Institute entry-level exams such as PCEP, and data analytics certificates on Coursera or similar platforms.
- Better order: skill, project, then certificate if it adds structure or a deadline.
**Likely follow-ups:** 1) *Which one would you recommend?* One that includes hands-on projects and is affordable. 2) *Would you do one for this role?* Only if it fills a real gap.
**Common mistakes:** Claiming a certificate you did not finish; saying certificates are worthless (sounds dismissive of learning).

### Q25 ⭐ 🟢 How do you keep your Python skills current while working a full-time job?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Consistency and whether you apply Python to real work.
**Say this in the interview:** "Small and daily beats big and rare: 30 to 40 minutes on weekdays, a longer block on one weekend day, and I look for a work task to automate with Python, such as a monthly headcount report. Real tasks keep skills alive better than tutorials." (Replace with your real routine.)
**Explain simply:**
- **Time slot:** the same time each day (for example before work) so it becomes a habit.
- **Apply at work:** replace one repeated Excel task with a script, keeping the Excel version to compare (Q17).
- **Keep a log:** one line a day of what you practised; it motivates you and gives talking points.
- **Review monthly:** redo an old problem from memory, since forgetting is normal.
- Respect company data rules: no confidential data in public tools.
**Likely follow-ups:** 1) *What if a busy week breaks the streak?* 10 minutes still counts; restart the next day. 2) *What have you automated?* Describe one real example only.
**Common mistakes:** Binge-learning on weekends then stopping; learning with no use case.

### Q26 ⭐ 🟡 How would you build a Python portfolio project from a public HR dataset such as employee attrition?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you run a complete analysis (question, clean, analyse, conclude) and explain it to a business reader?
**Say this in the interview:** "I would start with a business question: which groups lose the most people, and what do they have in common? I would use the IBM HR Analytics Employee Attrition dataset from Kaggle (from memory, unverified, check the link; it is a sample dataset created by IBM data scientists, not real company records). I would clean it, calculate attrition rate by department, overtime, tenure and pay band, chart the biggest differences, and finish with two recommendations and the limits of the data."
**Explain simply:**
- **Steps:** 1) question and data source; 2) load and inspect (shape, types, blanks, duplicates); 3) clean; 4) analyse with `groupby`; 5) chart; 6) findings and recommendations; 7) README on GitHub.
- **Attrition rate** = people who left / total people, as a percentage. Converting Yes/No to 1/0 makes the average equal the rate.
- **Be honest about limits:** the data is a snapshot; a difference between groups is not proof of cause.
- **Other HR-style practice data (from memory, unverified):** Kaggle HR analytics sets, or build a made-up attendance and payroll table.
**Sample data:** six rows in the same style as the attrition file (the real file has many more rows and columns).
**Code (what you write in the interview):**
```python
import pandas as pd

# Small stand-in for the IBM HR attrition file (same style of columns)
hr = pd.DataFrame({
    "Attrition": ["Yes", "No", "No", "Yes", "No", "No"],
    "Department": ["Sales", "Sales", "HR", "HR", "R&D", "R&D"],
    "OverTime": ["Yes", "No", "No", "Yes", "No", "Yes"],
})

# Turn Yes/No into 1/0 so the average is the attrition rate
hr["left"] = (hr["Attrition"] == "Yes").astype(int)

attrition_by_department = hr.groupby("Department")["left"].mean() * 100
attrition_by_overtime = hr.groupby("OverTime")["left"].mean() * 100
print(attrition_by_department.round(1))
print(attrition_by_overtime.round(1))
```
**Output:**
```
Department
HR       50.0
R&D       0.0
Sales    50.0
Name: left, dtype: float64
OverTime
No      0.0
Yes    66.7
Name: left, dtype: float64
```
**What it means:** In this tiny sample, people working overtime left more often (2 of 3). With real data you would confirm with more rows and say it is a pattern, not proof that overtime causes exit.
**Likely follow-ups:** 1) *What would you recommend?* Look into workload and manager support for the high-attrition group. 2) *What would you add?* A chart and a check of group sizes.
**Common mistakes:** Only printing tables with no business conclusion; claiming causation; skipping group sizes (a 100% rate from 2 people means little).

### Q27 ⭐ 🟡 How do you know you are job-ready in Python? What self-test would you use?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you measure readiness against concrete tasks, not feelings.
**Say this in the interview:** "I use a task checklist. Without notes, in 60 minutes, can I take a messy HR file, clean it, answer three business questions with groupby and merge, make one chart, and explain every line? If I can do that twice on fresh data, I call myself job-ready for an analyst role."
**Explain simply:** (a self-check you can run on yourself)
- **Test 1, load and inspect (5 min):** read a CSV; show shape, types, blanks, duplicates.
- **Test 2, clean (15 min):** fix types and dates, handle blanks, drop duplicates, tidy text.
- **Test 3, answer (20 min):** attrition by department, average salary by grade, top 5 by tenure, using `groupby`, `merge`, `sort_values`.
- **Test 4, check (10 min):** reconcile totals and row counts (Q17).
- **Test 5, explain (10 min):** say the findings in plain words for a manager.
- **Pass mark:** correct answers, no searching for basic syntax, two fresh datasets in a row.
- **Also tick:** 3 finished projects, 50+ solved problems (your own target; numbers are a guide, not a rule), one mock interview done.
**Likely follow-ups:** 1) *What if you fail part of it?* Drill that part for a week and retest. 2) *Is perfect needed?* No; analyst roles need accuracy and clear explanation, not advanced algorithms (Q14).
**Common mistakes:** Judging readiness by courses finished; never testing under a timer without notes.

### Q28 ⭐ 🟡 How would you teach Python basics to a non-technical colleague in four weeks?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you explain simply and structure learning; a leadership and communication signal.
**Say this in the interview:** "I would teach through their own work: a spreadsheet they already know. Week one is just reading and looking at a table, week two filtering and sorting, week three grouping and combining tables, week four a small project on their own data. Each week ends with a task they must do themselves, because people learn by typing, not watching."
**Explain simply:** (a template plan; adjust to the learner)
- **Week 1, comfort:** run a notebook, store values in variables, load a CSV, look at the first rows. Compare each step to Excel.
- **Week 2, filter and sort:** pick rows that meet a condition (like an Excel filter) and sort them; fix blanks.
- **Week 3, group and combine:** `groupby` is the pivot table; `merge` is VLOOKUP.
- **Week 4, mini project:** monthly headcount or attendance summary, with a short explanation.
- **Method:** 20 minutes of explaining, 40 minutes of their typing, one real question per session, praise errors as learning.
- Plan about 3 sessions a week of 1 hour, plus 20 minutes of daily practice.
**Likely follow-ups:** 1) *What do beginners struggle with?* Error messages and brackets; show them to read the last line of an error. 2) *How would you test progress?* A short end-of-week task.
**Common mistakes:** Starting with theory and jargon; showing too much code at once; doing the typing yourself.

### Q29 ⭐ 🟡 Your old code breaks after a pandas or Python upgrade. How do you handle deprecation warnings and version changes?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness that tools change, and a calm, methodical way to fix breakages.
**Say this in the interview:** "A deprecation warning means 'this still works but will be removed'. I do not ignore it: I read the message, which usually names the replacement, fix it, and re-run. For breakage I check the version, read the release notes, fix the code, and for important reports I pin the library version in a requirements file so the environment is reproducible."
**Explain simply:**
- **Deprecation warning:** an early notice that a feature will be removed. Fix it while it is only a warning.
- **Find versions:** `pd.__version__`. Read the "what's new" page (release notes) of the version you upgraded to.
- **Real examples I checked by running on pandas 3.0.5:** `df.append(...)` no longer exists (use `pd.concat`); `fillna(method="ffill")` now raises an error (use `ffill()`); chained assignment such as `df["a"].fillna(0, inplace=True)` does not change the DataFrame and warns, so assign the result back instead.
- **Safety:** keep a requirements file or a separate environment per project; test on a copy first, with a small known result to compare.
- Do not hide warnings forever; muting them only delays the break.
**Sample data:** a salary column with one blank (see code).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"salary": [50000, None, 45000]})

# Old way (removed in pandas 3): employees["salary"].fillna(method="ffill")
# Current way:
employees["salary"] = employees["salary"].ffill()
print(employees)
```
**Output:**
```
    salary
0  50000.0
1  50000.0
2  45000.0
```
**What it means:** The blank was filled with the previous value, using the supported method. The same line with the old `method=` option raised an error in this version.
**Likely follow-ups:** 1) *How do you avoid surprises?* Pin versions and rerun a small test on key reports after upgrades. 2) *Should you always upgrade?* Not blindly; test first, especially for scheduled reports.
**Common mistakes:** Silencing all warnings; upgrading on a live report without testing; fixing by guessing instead of reading the message.

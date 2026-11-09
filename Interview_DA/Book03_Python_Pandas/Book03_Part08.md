# Book 3 — Python & pandas for Analysts | Part 8: Visualization: matplotlib, seaborn 🟢🟡

**Target:** 45 questions | **Actual:** 50 questions
**Scope:** plotting from pandas data with matplotlib and seaborn: core chart code, customisation, saving, seaborn statistical plots, common errors, and report-ready charts (chart-design principles and BI tools stay in Book 4).

### Q1 ⭐⭐⭐ 🟢 What is the difference between matplotlib and seaborn, and when do you use each?
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** Whether you know seaborn is built on top of matplotlib and can pick the right one for the job.
**Say this in the interview:** "Matplotlib is the base plotting library: it gives full control over every detail. Seaborn sits on top of it and makes statistical charts, like boxplots and heatmaps, in one line with nicer default styling. I use seaborn for quick, good-looking analysis and matplotlib when I need to fine-tune the chart."
**Explain simply:**
- Matplotlib is like drawing by hand with a pen: powerful, but you set many things yourself.
- Seaborn is like a ready-made template: you hand it a DataFrame and column names and it does the grouping and styling.
- Seaborn charts are matplotlib objects underneath, so you can still add titles or save with matplotlib commands (`plt.title`, `plt.savefig`).
- Use seaborn for distributions, group comparisons and correlations; use matplotlib for custom layouts, annotations and anything seaborn does not offer.
**Likely follow-ups:** 1) *Can you use both together?* Yes, this is the normal way: seaborn draws, matplotlib finishes (title, size, save). 2) *Which is faster to learn?* Seaborn for simple charts, matplotlib for control.
**Common mistakes:** Thinking they are competitors; forgetting `import matplotlib.pyplot as plt` when using seaborn and then being unable to add a title or call `plt.show()`.

### Q2 ⭐⭐⭐ 🟢 Write code to draw a bar chart of employee headcount by department using pandas and matplotlib.
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** Can you go from raw rows to counts to a labelled bar chart.
**Say this in the interview:** "I count employees per department with `value_counts`, then plot that result as a bar chart and add a title and axis labels."
**Explain simply:**
- Headcount means the number of employees. Each row is one employee, so counting rows per department gives it.
- `value_counts()` counts how many times each department appears, biggest first.
- A bar chart fits because departments are separate categories.
**Sample data:** 8 employees: Sales 3, IT 2, HR 2, Finance 1.
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "John", "Priya", "Karan", "Sita", "Arjun"],
    "department": ["Sales", "IT", "HR", "Sales", "IT", "Sales", "HR", "Finance"],
})

# Count employees in each department
headcount = employees["department"].value_counts()

headcount.plot(kind="bar")
plt.title("Headcount by Department")
plt.xlabel("Department")
plt.ylabel("Number of employees")
plt.show()
```
**Output:** (plot rendered with a non-display backend, ran with no errors) A bar chart with four bars: Sales at 3, IT at 2, HR at 2, Finance at 1, in that order (largest first), with the title and axis labels shown.
**What it means:** Sales is the biggest team. The bars are ordered high to low because `value_counts` sorts that way.
**Alternative:** `sns.countplot(data=employees, x="department")` counts and draws in one line.
**Likely follow-ups:** 1) *How do you sort alphabetically?* `value_counts().sort_index()`. 2) *Why is there no `plt.figure()`?* pandas creates the chart for you.
**Common mistakes:** Plotting the raw column (no counting step); forgetting axis labels; using `kind="line"` for categories.

### Q3 ⭐⭐⭐ 🟢 Write code to plot a line chart of monthly hires over a year.
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** Whether you choose a line for time and keep the months in the right order.
**Say this in the interview:** "Time trend means a line chart. I put month on the x-axis, hires on the y-axis, add markers so each month is visible, and label the chart."
**Explain simply:**
- A line connects points in order, so the eye sees rise and fall over time.
- `marker="o"` puts a dot on every month, which helps with only 12 points.
- Months must already be in calendar order, because the line follows row order.
**Sample data:** 12 rows, month name and hires (12, 9, 15, 20, 18, 14, 10, 22, 25, 17, 11, 8).
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

monthly_hires = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "hires": [12, 9, 15, 20, 18, 14, 10, 22, 25, 17, 11, 8],
})

plt.plot(monthly_hires["month"], monthly_hires["hires"], marker="o")
plt.title("Monthly Hires, 2025")
plt.xlabel("Month")
plt.ylabel("Number of hires")
plt.show()
```
**Output:** (plot rendered with a non-display backend, ran with no errors) One line with 12 dots, rising to a peak of 25 in September and falling to 8 in December.
**What it means:** Hiring peaks in the third quarter and slows at year end.
**Alternative:** `monthly_hires.plot(x="month", y="hires", marker="o")` does the same from pandas.
**Likely follow-ups:** 1) *What if months are real dates?* Convert with `pd.to_datetime` so they sort and format correctly (see Q33). 2) *Why not a bar chart?* Bars also work, but a line shows trend better.
**Common mistakes:** Month names sorted alphabetically (Apr, Aug, Dec...) after a groupby; missing months leaving gaps; no axis labels.

### Q4 ⭐⭐⭐ 🟢 How do you add a title, axis labels and a legend to a matplotlib chart?
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** The basic labelling calls, and that the legend needs `label=` on each line.
**Say this in the interview:** "`plt.title`, `plt.xlabel`, `plt.ylabel` for the text, and I give each line a `label=` and call `plt.legend()` so matplotlib knows what to show."
**Explain simply:**
- Title says what the chart is; axis labels say what each axis measures (include units).
- A legend is the key that tells which colour is which series.
- `plt.legend()` only shows items that were given a `label`.
- In the `fig, ax` style the same calls are `ax.set_title`, `ax.set_xlabel`, `ax.set_ylabel`, `ax.legend()`.
**Sample data:** Small lists: hires and exits for Jan to Apr.
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr"]
hires = [12, 9, 15, 20]
exits = [5, 7, 6, 9]

# label= on each line is what the legend reads
plt.plot(months, hires, label="Hires")
plt.plot(months, exits, label="Exits")

plt.title("Hires and Exits by Month")
plt.xlabel("Month")
plt.ylabel("Number of employees")
plt.legend()
plt.show()
```
**Output:** (plot rendered with a non-display backend, ran with no errors) Two lines titled "Hires and Exits by Month" with labelled axes and a legend box listing Hires and Exits.
**What it means:** A reader can tell the chart's topic, what each axis is, and which line is which without asking you.
**Likely follow-ups:** 1) *Where does the legend go?* `plt.legend(loc="upper right")`. 2) *Why is my legend empty?* No `label=` was given.
**Common mistakes:** Calling `plt.legend()` without labels (warning: "No artists with labels found"); calling title before the plot is drawn in a different figure.

### Q5 ⭐⭐⭐ 🟢 Write code to draw a histogram of employee salaries and explain how you choose the number of bins.
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** That you know a histogram shows a distribution and that bins change the story.
**Say this in the interview:** "A histogram groups salaries into ranges (bins) and counts people in each. I start with a default or a rule like Sturges, then try a few bin counts and keep the one that shows the shape without too much noise."
**Explain simply:**
- A bin is one range, for example 30,000 to 45,000. The bar height is how many employees fall in it.
- Too few bins hide the shape; too many bins make it jagged and noisy.
- Rules of thumb: `bins="auto"`, about the square root of the row count, or Sturges (1 + log2 of n). For 15 rows, 5 to 7 bins is sensible.
- Always try two or three values; there is no single correct number.
**Sample data:** 15 salaries from 32,000 to 120,000 (one high earner).
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

employees = pd.DataFrame({
    "salary": [32000, 35000, 38000, 41000, 42000, 45000, 47000, 52000,
               55000, 58000, 61000, 66000, 72000, 85000, 120000],
})

plt.hist(employees["salary"], bins=6, edgecolor="black")
plt.title("Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Number of employees")
plt.show()
```
**Output:** (plot rendered with a non-display backend, ran with no errors) Six bars with counts 6, 5, 2, 1, 0, 1 (checked with numpy): most people earn under 60,000 and one person sits far right at 120,000.
**What it means:** The distribution is right-skewed: a few high salaries stretch the tail.
**Likely follow-ups:** 1) *Histogram vs bar chart?* Histogram bins a number; a bar chart compares categories. 2) *What does skew tell you?* Mean is above median, so report the median.
**Common mistakes:** Forgetting `edgecolor` (bars blur together); using `plt.bar` instead; leaving NaN in the column; judging the shape from one bin setting.

### Q6 ⭐⭐⭐ 🟢 Write code to draw a scatter plot of years of experience against salary.
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** Choosing a scatter for two numbers and putting the cause (experience) on x and the outcome (salary) on y.
**Say this in the interview:** "A scatter plot puts one dot per employee, experience on the x-axis and salary on the y-axis, so I can see whether they move together."
**Explain simply:**
- Each dot is one person; its position shows two values at once.
- Dots rising left to right mean a positive relationship.
- A relationship is not proof of cause: experience may not be the only driver.
**Sample data:** 8 employees, years_experience 1 to 12, salary 30,000 to 95,000.
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

employees = pd.DataFrame({
    "years_experience": [1, 2, 3, 5, 6, 8, 10, 12],
    "salary": [30000, 34000, 40000, 52000, 55000, 70000, 82000, 95000],
})

plt.scatter(employees["years_experience"], employees["salary"])
plt.title("Experience vs Salary")
plt.xlabel("Years of experience")
plt.ylabel("Salary")
plt.show()
```
**Output:** (plot rendered with a non-display backend, ran with no errors) Eight dots climbing steadily from bottom left to top right.
**What it means:** More experience goes with higher salary in this sample, a strong positive relationship.
**Alternative:** `sns.scatterplot(data=employees, x="years_experience", y="salary")`, which also lets you colour by department with `hue` (Q31).
**Likely follow-ups:** 1) *How do you quantify it?* `employees.corr()` gives the correlation. 2) *Many overlapping points?* Use `alpha=0.3` (Q44).
**Common mistakes:** Swapping the axes; using a line chart for unordered points; reading correlation as causation.

### Q7 ⭐⭐⭐ 🟢 How do you save a chart as an image file in matplotlib, and why does savefig sometimes save a blank image?
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** Knowing `plt.savefig` and the order of calls.
**Say this in the interview:** "I use `plt.savefig('name.png')`. It must come before `plt.show()`, because in a normal script `show()` closes the figure, so saving afterwards writes an empty canvas."
**Explain simply:**
- The file type comes from the extension (`.png`, `.jpg`, `.pdf`, `.svg`).
- `dpi=150` (dots per inch) makes it sharper; `bbox_inches="tight"` stops labels being cut off.
- Blank image cause: `savefig` called after `plt.show()` (from memory: this happens in scripts and many interactive backends; in a notebook it often still works). Another cause: saving a different figure than the one you drew on.
- With the `fig, ax` style, `fig.savefig(...)` always saves the right figure.
**Sample data:** Small lists of department headcount.
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

departments = ["Sales", "IT", "HR"]
headcount = [30, 25, 8]

plt.bar(departments, headcount)
plt.title("Headcount by Department")

# save BEFORE plt.show(), because show() clears the figure
plt.savefig("headcount.png", dpi=150, bbox_inches="tight")
plt.show()
```
**Output:** No printed text. A file `headcount.png` is created (confirmed the file was written when run).
**What it means:** The image file is ready to paste into a slide or email.
**Likely follow-ups:** 1) *Transparent background?* `transparent=True`. 2) *Save as PDF?* Change the extension.
**Common mistakes:** `savefig` after `show`; relative file path ending up in an unexpected folder; low dpi blurry slides.

### Q8 ⭐⭐⭐ 🟢 What does plt.show() do, and is it needed in a Jupyter notebook?
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** Whether you understand when a chart is displayed.
**Say this in the interview:** "`plt.show()` opens the chart window and displays everything drawn so far. In a Jupyter notebook the chart usually appears automatically at the end of the cell, so it is not required, but I still add it because it hides the extra text line and works the same in scripts."
**Explain simply:**
- In a plain `.py` script nothing appears on screen until `plt.show()` runs.
- In Jupyter, the inline backend displays the figure when the cell finishes.
- Without `show()` in a notebook you may see a line like `<Axes: ...>` printed above the chart; `show()` removes it.
- `show()` also ends the figure, so the next plot starts fresh (and `savefig` must come first, Q7).
**Likely follow-ups:** 1) *Why does my script finish with no chart?* `plt.show()` is missing, or the backend has no display (server). 2) *Chart shows twice in notebook?* Remove the extra display call.
**Common mistakes:** Forgetting `show()` in a script; calling `savefig` after it.

### Q9 ⭐⭐⭐ 🟢 Which Python plot would you use to show a trend over time, a comparison between categories, a distribution and a relationship between two numbers?
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** The question-to-chart mapping (full chart design theory is Book 4).
**Say this in the interview:** "Trend: line. Comparison between categories: bar. Distribution: histogram or boxplot. Relationship between two numbers: scatter."
**Explain simply:**
| Question | Chart | Code |
|---|---|---|
| Trend over time | Line | `plt.plot(x, y)` or `df.plot(kind="line")` |
| Compare categories | Bar | `plt.bar(...)` or `sns.barplot(...)` |
| Distribution of one number | Histogram, boxplot | `plt.hist(...)`, `sns.boxplot(...)` |
| Relationship of two numbers | Scatter | `plt.scatter(x, y)` |
- HR examples: monthly headcount (line), attrition by department (bar), salary spread (histogram), experience vs pay (scatter).
- Pick the chart from the question you are answering, not from what looks fancy.
**Likely follow-ups:** 1) *Parts of a whole?* Stacked bar, or a pie only for 2 to 3 slices (Q22). 2) *Compare distributions across groups?* Boxplot or violin.
**Common mistakes:** Line chart for categories; pie chart with many slices; histogram for categories.

### Q10 ⭐⭐⭐ 🟡 What is the difference between plt.plot() and fig, ax = plt.subplots(), and which style do you prefer?
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** Whether you know the two matplotlib interfaces and can justify one.
**Say this in the interview:** "`plt.plot()` is the quick state-based style: matplotlib tracks the 'current' chart for you. `fig, ax = plt.subplots()` is the object style: I hold the figure and the chart in variables. I prefer the second because it is explicit, and it scales to several charts on one page."
**Explain simply:**
- Figure (`fig`) is the whole canvas; axes (`ax`) is one chart drawn on it.
- `plt.` functions act on whichever chart is current, which is fine for one quick plot.
- With `ax` you say exactly which chart you are changing, so no mix-ups with multiple subplots.
- Method names differ slightly: `plt.title` vs `ax.set_title`, `plt.xlabel` vs `ax.set_xlabel`.
**Sample data:** Small lists, hires for Jan to Mar.
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar"]
hires = [12, 9, 15]

# fig is the whole picture, ax is the one chart drawn on it
fig, ax = plt.subplots()
ax.plot(months, hires)
ax.set_title("Hires by Month")
ax.set_xlabel("Month")
ax.set_ylabel("Hires")
plt.show()
```
**Output:** (plot rendered with a non-display backend, ran with no errors) A single line chart with the title and labels.
**What it means:** Same picture as the `plt.plot` version, but every setting is attached to a named object.
**Likely follow-ups:** 1) *How do you draw 4 charts?* `fig, axes = plt.subplots(2, 2)` (Q25). 2) *Does pandas accept `ax`?* Yes, `df.plot(ax=ax)`.
**Common mistakes:** Mixing `plt.title` and `ax.set_title` across subplots; forgetting `plt.subplots` returns two things.

### Q11 ⭐⭐⭐ 🟡 Write code to draw a correlation heatmap of the numeric columns of a DataFrame using seaborn.
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** That you compute correlation on numeric columns only, then draw it with `sns.heatmap`.
**Say this in the interview:** "I call `corr(numeric_only=True)` to get a table of correlations, then pass it to `sns.heatmap` with `annot=True` to print the numbers in the cells."
**Explain simply:**
- Correlation is a number from -1 to +1 showing how strongly two columns move together; +1 moves together, -1 opposite, 0 no link.
- A heatmap colours that table so strong links stand out.
- Text columns (like department) cannot be correlated, so `numeric_only=True` skips them.
- The diagonal is always 1 (a column with itself).
**Sample data:** 8 employees with age, tenure_years, salary and a text column department.
**Code (what you write in the interview):**
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

employees = pd.DataFrame({
    "age": [25, 30, 35, 40, 45, 50, 28, 33],
    "tenure_years": [1, 3, 6, 9, 12, 20, 2, 5],
    "salary": [30000, 42000, 55000, 68000, 80000, 110000, 36000, 50000],
    "department": ["IT", "HR", "IT", "Sales", "HR", "Sales", "IT", "HR"],
})

# Correlation only works on numbers, so keep numeric columns
correlation = employees.corr(numeric_only=True)

sns.heatmap(correlation, annot=True, cmap="coolwarm")
plt.title("Correlation of Numeric Columns")
plt.show()
```
**Output:** (plot rendered with a non-display backend, ran with no errors) A 3 by 3 coloured grid with the department column excluded. The numbers printed in the cells: age and tenure 0.97, age and salary 0.99, tenure and salary 1.00 (rounded; diagonal 1.00).
**What it means:** In this small sample age, tenure and salary all rise together. Correlation is not cause.
**Likely follow-ups:** 1) *Customise it?* See Q42. 2) *Which correlation method?* `method="spearman"` for ranks or skewed data.
**Common mistakes:** Passing the raw DataFrame to `sns.heatmap`; leaving text columns in (error in recent pandas without `numeric_only`); forgetting `annot=True`.

### Q12 ⭐⭐⭐ 🟡 Write code to draw a boxplot of salary by department in seaborn, and explain how to read it.
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** Can you draw it and read median, spread and outliers.
**Say this in the interview:** "`sns.boxplot` with department on x and salary on y. The box is the middle 50 percent of people, the line inside is the median, the whiskers show the normal range, and dots beyond the whiskers are outliers."
**Explain simply:**
- Box edges are the 25th and 75th percentiles (Q1 and Q3); the height of the box is the IQR (middle 50 percent spread).
- Line inside the box: the median (the middle salary).
- Whiskers reach up to 1.5 times the IQR from the box; dots outside are flagged outliers.
- A higher box means higher pay; a taller box means more spread.
**Sample data:** 18 salaries (in thousands): 6 each for IT, HR, Sales; IT has one very high value, 150.
**Code (what you write in the interview):**
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

employees = pd.DataFrame({
    "department": ["IT"] * 6 + ["HR"] * 6 + ["Sales"] * 6,
    "salary": [60, 65, 70, 72, 80, 150,
               40, 42, 45, 47, 50, 52,
               35, 45, 55, 60, 70, 75],
})

sns.boxplot(data=employees, x="department", y="salary")
plt.title("Salary by Department")
plt.show()
```
**Output:** (plot rendered with a non-display backend, ran with no errors) Three boxes. IT sits highest with a single dot far above at 150; HR is the lowest and tightest; Sales is the widest.
**What it means:** IT pays most but has one extreme earner; Sales pay varies a lot; HR pay is similar across people.
**Likely follow-ups:** 1) *Find the outlier rows?* See Q34. 2) *Boxplot vs violin?* Q35.
**Common mistakes:** Calling the line in the box the mean (it is the median); swapping x and y; treating outliers as errors without checking.

### Q13 ⭐⭐⭐ 🟡 How do you plot directly from a pandas DataFrame, and how do you plot the result of a groupby?
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** Knowing the `.plot()` method works on both DataFrames and the Series that `groupby` returns.
**Say this in the interview:** "Every DataFrame and Series has `.plot(kind=...)`, which uses matplotlib behind the scenes. For a groupby I first aggregate, for example `mean()`, and call `.plot(kind='bar')` on the result, because the group names become the index and so the x-axis."
**Explain simply:**
- `df["col"].plot(kind="hist")` plots one column; `df.plot(x="a", y="b", kind="scatter")` plots two.
- `groupby(...)[...].mean()` gives a Series whose index is the group labels; `.plot` uses the index as x and the values as y.
- Other kinds: `"line"`, `"bar"`, `"barh"`, `"hist"`, `"box"`, `"scatter"`, `"pie"`.
- Add `plt.title` and labels afterwards as usual.
**Sample data:** 6 employees with department and salary.
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

employees = pd.DataFrame({
    "department": ["Sales", "IT", "HR", "Sales", "IT", "Sales"],
    "salary": [40000, 60000, 45000, 50000, 70000, 45000],
})

# Plot straight from the DataFrame
employees["salary"].plot(kind="hist", bins=4)
plt.show()

# Plot the result of a groupby: average salary per department
average_salary = employees.groupby("department")["salary"].mean()
average_salary.plot(kind="bar")
plt.ylabel("Average salary")
plt.show()
```
**Output:** (plots rendered with a non-display backend, ran with no errors) First a histogram of the six salaries; second a bar chart with HR 45,000, IT 65,000, Sales 45,000 (alphabetical by department).
**What it means:** IT has the highest average salary.
**Likely follow-ups:** 1) *Several groups side by side?* `groupby(...).mean().plot(kind="bar")` on a DataFrame. 2) *Sort the bars?* `sort_values()` first (Q14).
**Common mistakes:** Trying to plot the `groupby` object before aggregating; wrong `kind` spelling; forgetting that the index becomes the x-axis.

### Q14 ⭐⭐⭐ 🟡 Write code to plot attrition rate by department as a bar chart sorted from highest to lowest.
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** The attrition calculation (share who left per department) and sorting before plotting.
**Say this in the interview:** "Attrition rate is leavers divided by headcount. If I flag leavers as 1 and stayers as 0, the mean of that column per department is the rate. I sort descending and plot a bar chart."
**Explain simply:**
- Attrition rate is the percentage of employees who left in a group.
- Averaging a 0/1 column gives the share of ones, which is the rate; times 100 for percent.
- `sort_values(ascending=False)` puts the highest bar first.
- Rates are fair across teams of different sizes; raw leaver counts are not.
**Sample data:** 10 employees: Sales 4 (2 left), IT 3 (1 left), HR 3 (0 left).
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

employees = pd.DataFrame({
    "department": ["Sales", "Sales", "Sales", "Sales", "IT", "IT", "IT", "HR", "HR", "HR"],
    "left_company": [1, 1, 0, 0, 0, 0, 1, 0, 0, 0],   # 1 = left, 0 = stayed
})

# The average of a 0/1 column is the share who left
attrition_rate = employees.groupby("department")["left_company"].mean() * 100

attrition_rate = attrition_rate.sort_values(ascending=False)

attrition_rate.plot(kind="bar")
plt.title("Attrition Rate by Department")
plt.xlabel("Department")
plt.ylabel("Attrition rate (%)")
plt.show()
```
**Output:** (plot rendered with a non-display backend, ran with no errors) Three bars in this order, values checked by running: Sales 50.0, IT 33.3, HR 0.0.
**What it means:** Half of Sales left, one third of IT, nobody in HR; Sales needs attention first.
**Likely follow-ups:** 1) *Small teams?* Show headcount too, as 1 leaver in 3 people is noisy. 2) *Add a company average line?* Q40.
**Common mistakes:** Plotting counts instead of rates; sorting after plotting (no effect); not sorting at all; forgetting to say the time period.

### Q15 ⭐⭐ 🟢 What is the standard way to import matplotlib and seaborn, and what is pyplot?
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** Basic familiarity with the standard aliases.
**Say this in the interview:** "`import matplotlib.pyplot as plt` and `import seaborn as sns`. Pyplot is the module inside matplotlib that holds the plotting functions like `plot`, `bar` and `show`."
**Explain simply:**
- An alias (`plt`, `sns`) is just a short nickname so you type less; everyone uses these two.
- Matplotlib is a big package; `pyplot` is the part with the simple chart commands.
- Pandas is usually imported too: `import pandas as pd`.
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt
import seaborn as sns
```
**Output:** No output (the imports run silently).
**What it means:** From now on `plt.` and `sns.` give access to the plotting functions.
**Likely follow-ups:** 1) *Do I need matplotlib to use seaborn?* It must be installed, but you still import `plt` to title, size and save. 2) *Notebook magic?* `%matplotlib inline` (Q24).
**Common mistakes:** `import matplotlib as plt` (no plotting functions); `import seaborn as sb` then calling `sns`; forgetting the install.

### Q16 ⭐⭐ 🟢 How do you change the figure size of a chart?
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** The `figsize` argument and that it is in inches, width first.
**Say this in the interview:** "I pass `figsize=(width, height)` in inches, either to `plt.figure` or to `plt.subplots`. For pandas plots it is `df.plot(figsize=(10, 5))`."
**Explain simply:**
- `(10, 5)` means 10 inches wide and 5 inches tall; the default is about (6.4, 4.8).
- Create the figure first, then plot. Calling `plt.figure(figsize=...)` after the plot starts a new blank figure.
- Seaborn plots drawn on an existing figure follow its size; for `catplot`/`displot` use `height` and `aspect` instead.
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar"]
hires = [12, 9, 15]

# width and height are in inches
plt.figure(figsize=(10, 5))
plt.plot(months, hires)
plt.show()

# with the fig, ax style
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(months, hires)
plt.show()
```
**Output:** (plots rendered with a non-display backend, ran with no errors) Two identical wide line charts.
**What it means:** The chart is wider than tall, better for time series and long labels.
**Likely follow-ups:** 1) *How to make it sharper?* Raise `dpi`. 2) *Size for a slide?* About (10, 5).
**Common mistakes:** Setting `figsize` after plotting; swapping width and height; thinking the unit is pixels.

### Q17 ⭐⭐ 🟢 How do you rotate or fix overlapping x-axis labels?
**Asked at:** commonly asked (no company-specific report found); topic appears in general matplotlib/seaborn question banks (TechPrep, Testbook).
**What the interviewer is checking:** The common fixes: rotation, alignment, wider figure, or a horizontal bar chart.
**Say this in the interview:** "I rotate the labels with `plt.xticks(rotation=45, ha='right')` and call `plt.tight_layout()` so nothing is cut off. If labels are still long, I make the chart wider or switch to a horizontal bar chart."
**Explain simply:**
- Overlap happens when labels are long or there are many categories.
- `rotation=45` tilts them; `ha="right"` (horizontal alignment) lines the end of each label under its bar so it reads cleanly.
- `plt.tight_layout()` adjusts margins so tilted labels are not clipped at the bottom.
- Other fixes: `figsize=(12, 5)`, shorter names, or `plt.barh` (long names read easily on the y-axis).
- With `ax`, use `ax.tick_params(axis="x", rotation=45)`.
**Sample data:** Four long department names with headcounts 40, 55, 12, 20.
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

departments = ["Customer Support", "Software Engineering", "Human Resources", "Finance and Accounts"]
headcount = [40, 55, 12, 20]

plt.bar(departments, headcount)

# tilt the labels, and align their right end under the bar
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
```
**Output:** (plot rendered with a non-display backend, ran with no errors) A bar chart whose four long department names are tilted 45 degrees and fully visible.
**What it means:** The reader can read every department name without overlap.
**Likely follow-ups:** 1) *Dates on the x-axis?* Use `fig.autofmt_xdate()` (Q33). 2) *Why not rotate 90?* Harder to read; 30 to 45 is easier.
**Common mistakes:** Rotating without `ha="right"` (labels look shifted); no `tight_layout` so labels are cut; calling `xticks` before the plot exists.

### Q18 ⭐⭐ 🟢 How do you plot multiple lines on the same chart with a legend, for example hires and exits per month?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you know that each line needs a label and that the legend must be switched on.
**Say this in the interview:** "I call plot once per line on the same axes and give each a label. Then plt.legend() builds the legend from those labels."
**Explain simply:**
- Matplotlib keeps drawing on the same chart until you call `plt.show()`, so two `plt.plot` calls give two lines on one chart.
- `label=` names the line. `plt.legend()` turns those names into the little key. Without `label=`, the legend is empty and Matplotlib warns you.
- Always add a title and axis labels, so the reader knows what the numbers are.
**Sample data:**
```python
import pandas as pd

monthly = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "hires": [12, 15, 9, 20, 14, 11],
    "exits": [5, 8, 7, 6, 12, 9],
})
```
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

# One plt.plot call per line; label= is what the legend shows
plt.plot(monthly["month"], monthly["hires"], label="Hires")
plt.plot(monthly["month"], monthly["exits"], label="Exits")

plt.title("Hires and exits per month")
plt.xlabel("Month")
plt.ylabel("Number of employees")
plt.legend()
plt.show()
```
**Output:** A line chart with two lines (Hires and Exits) over Jan to Jun and a legend in the corner. No text is printed. (Plot not rendered in this document; the code was run with a headless backend and produced no errors.)
**What it means:** Hires peaked in April (20) while exits peaked in May (12), so the gap between the lines shows net hiring each month.
**Alternative:**
```python
# Shortcut: pandas draws one line per column
monthly.set_index("month").plot(title="Hires and exits per month")
plt.show()
```
**Likely follow-ups:** 1) *How do you move the legend?* `plt.legend(loc="upper left")`. 2) *What if the two series have very different scales?* Use a second y-axis with `twinx()`, or two charts.
**Common mistakes:** Forgetting `label=`; calling `plt.legend()` before the lines are drawn; leaving the chart without a title or axis labels.

### Q19 ⭐⭐ 🟢 How do you change the colours of a chart or use a seaborn colour palette?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you know `color` (one colour) versus `palette` (a set of colours) and can pick sensible colours.
**Say this in the interview:** "In matplotlib I pass color= for one colour. In seaborn I pass palette= with a palette name like Set2, and hue= so each category gets its own colour."
**Explain simply:**
- A **palette** is just a ready-made list of colours that look good together. Seaborn has many: `Set2`, `pastel`, `Blues`, `viridis`.
- Use a **categorical** palette (`Set2`, `tab10`) when the groups have no order, like departments. Use a **sequential** one (`Blues`) when low to high matters.
- In seaborn 0.13, passing `palette` without `hue` gives a warning, so set `hue` to the same column as `x` and hide the duplicate legend with `legend=False`.
- Keep colours meaningful: not a rainbow just for decoration, and remember colour-blind readers.
**Sample data:**
```python
import pandas as pd

headcount = pd.DataFrame({
    "department": ["Sales", "IT", "HR", "Finance"],
    "employees": [40, 55, 12, 20],
})
```
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Matplotlib: give one colour for all bars, by name or hex code
plt.bar(headcount["department"], headcount["employees"], color="steelblue")
plt.title("Headcount by department (one colour)")
plt.show()

# Seaborn: a palette gives each bar its own colour from a ready-made set
sns.barplot(data=headcount, x="department", y="employees",
            hue="department", palette="Set2", legend=False)
plt.title("Headcount by department (Set2 palette)")
plt.show()
```
**Output:** Two bar charts: the first with all four bars in steel blue, the second with four different soft colours. No text is printed. (Plot not rendered in this document; the code ran without errors or warnings.)
**What it means:** The data is the same in both charts; only the colouring changes.
**Alternative:**
```python
# See what colours a palette contains
print(sns.color_palette("Set2").as_hex())
```
```text
['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3']
```
**Likely follow-ups:** 1) *How do you set one palette for the whole notebook?* `sns.set_palette("Set2")` or `sns.set_theme(palette="Set2")`. 2) *How do you pick colours for colour-blind readers?* Use `palette="colorblind"`.
**Common mistakes:** Using `palette` without `hue` in new seaborn (warning); using a sequential palette for unordered groups; too many bright colours.

### Q20 ⭐⭐ 🟢 How do you add data labels (values) on top of the bars in a bar chart?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you know the one-line `bar_label` helper instead of looping and placing text by hand.
**Say this in the interview:** "I keep the bars that plt.bar returns and pass them to plt.bar_label, which prints each value on top of its bar."
**Explain simply:**
- `plt.bar` returns the bars as an object. `bar_label` reads each bar's height and writes it above the bar.
- For seaborn, get the axes (`ax = sns.barplot(...)`) and use `ax.bar_label(ax.containers[0])`.
- Format the numbers with `fmt`, for example `plt.bar_label(bars, fmt="%.1f")` for one decimal.
- `bar_label` needs matplotlib 3.4 or newer (it ran here on 3.11). On very old versions, loop over the bars and use `plt.text`.
**Sample data:**
```python
import pandas as pd

headcount = pd.DataFrame({
    "department": ["Sales", "IT", "HR", "Finance"],
    "employees": [40, 55, 12, 20],
})
```
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

# plt.bar returns the bars; bar_label writes each bar's value on top
bars = plt.bar(headcount["department"], headcount["employees"])
plt.bar_label(bars)

plt.title("Headcount by department")
plt.ylabel("Employees")
plt.show()
```
**Output:** A bar chart where 40, 55, 12 and 20 are printed above the Sales, IT, HR and Finance bars. No text is printed. (Plot not rendered in this document; both versions ran without errors.)
**What it means:** The reader can see exact values without reading them off the axis.
**Alternative:**
```python
import seaborn as sns

# Seaborn: the bars are stored in ax.containers
ax = sns.barplot(data=headcount, x="department", y="employees")
ax.bar_label(ax.containers[0])
plt.show()
```
**Likely follow-ups:** 1) *How do you put the labels inside the bar?* `label_type="center"`. 2) *How do you stop the top label being cut off?* Raise the y limit a little, `plt.ylim(0, 65)`.
**Common mistakes:** Calling `bar_label` before the bars exist; labelling a stacked chart without `label_type="center"`; too many bars so the numbers overlap.

### Q21 ⭐⭐ 🟢 How do you set axis limits and add gridlines to a chart?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you can control what range the reader sees, and know that the y axis range can change the story.
**Say this in the interview:** "plt.xlim and plt.ylim set the visible range, and plt.grid switches on gridlines. For a percentage I usually start the y axis at zero so the chart does not exaggerate small changes."
**Explain simply:**
- `plt.ylim(0, 100)` fixes the vertical range. Matplotlib normally picks a range itself, which may zoom in and make a small dip look dramatic.
- `plt.grid(axis="y")` draws lines only across the y axis; `axis="both"` draws both.
- `linestyle="--"` makes dashes and `alpha=0.5` makes them faint so they do not fight with the data.
- With the object style (`fig, ax = plt.subplots()`), the same calls are `ax.set_xlim`, `ax.set_ylim` and `ax.grid`.
**Sample data:**
```python
import pandas as pd

attendance = pd.DataFrame({
    "week": [1, 2, 3, 4, 5, 6],
    "attendance_rate": [92, 95, 90, 88, 94, 97],
})
```
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

plt.plot(attendance["week"], attendance["attendance_rate"], marker="o")

# Axis limits: (lowest, highest) shown on each axis
plt.xlim(1, 6)
plt.ylim(0, 100)

# Gridlines: light dashed lines on the y axis only
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.title("Weekly attendance rate")
plt.xlabel("Week")
plt.ylabel("Attendance (%)")
plt.show()
```
**Output:** A line chart with markers, y axis from 0 to 100, x axis from 1 to 6, and faint dashed horizontal gridlines. No text is printed. (Plot not rendered in this document; the code ran without errors.)
**What it means:** The 88% to 97% swings look modest on a 0 to 100 scale, which is honest for attendance.
**Alternative:**
```python
# Same idea with the object-oriented style
fig, ax = plt.subplots()
ax.plot(attendance["week"], attendance["attendance_rate"], marker="o")
ax.set_ylim(0, 100)
ax.grid(True)
plt.show()
```
**Likely follow-ups:** 1) *Is it always wrong to not start at zero?* For bars yes (length means value); for lines it can be fine if you label it clearly. 2) *How do you flip an axis?* `plt.gca().invert_yaxis()`.
**Common mistakes:** Truncating a bar chart axis; heavy dark gridlines; setting limits that cut off data points.

### Q22 ⭐⭐ 🟢 How do you draw a pie chart in matplotlib, and why do analysts usually avoid it?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you can draw it, and whether you know its weakness (a sign of chart-choice judgement).
**Say this in the interview:** "plt.pie with labels and autopct draws it. But I usually prefer a sorted bar chart, because people compare lengths much more accurately than angles."
**Explain simply:**
- A pie chart shows parts of a whole. Each slice is that category's share of the total.
- `autopct="%1.0f%%"` prints the percentage on each slice (0 decimals).
- Why analysts avoid it: humans judge angles and areas poorly, so slices of 30% and 33% look the same; it fails with more than about 5 slices; it cannot show change over time or compare two pies well.
- When it is acceptable: 2 to 4 slices where one is clearly the big story, like "70% remote".
**Sample data:**
```python
import pandas as pd

hiring_source = pd.DataFrame({
    "source": ["Referral", "Job portal", "Campus", "Agency"],
    "hires": [30, 45, 15, 10],
})
```
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

# autopct writes each slice's share of the total as a percentage
plt.pie(hiring_source["hires"], labels=hiring_source["source"], autopct="%1.0f%%")
plt.title("Hires by source")
plt.show()
```
**Output:** A pie with four slices labelled Referral 30%, Job portal 45%, Campus 15% and Agency 10%. No text is printed. (Plot not rendered in this document; both versions ran without errors.)
**What it means:** Job portals bring almost half of hires. A bar chart shows the same thing with easier comparison.
**Alternative:**
```python
# The usual better choice: a sorted bar chart
sorted_sources = hiring_source.sort_values("hires", ascending=False)
plt.bar(sorted_sources["source"], sorted_sources["hires"])
plt.title("Hires by source")
plt.show()
```
**Likely follow-ups:** 1) *How do you make a donut chart?* `wedgeprops={"width": 0.4}`. 2) *How do you pull one slice out?* `explode=[0.1, 0, 0, 0]`.
**Common mistakes:** Too many tiny slices; no percentages or labels; using a pie for values that do not add up to a whole.

### Q23 ⭐⭐ 🟢 What is a seaborn theme or style, and how do you set one with sns.set_theme()?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you know seaborn can restyle all charts in one line, and which options exist.
**Say this in the interview:** "A theme is the overall look: background, gridlines, colours and font size. I call sns.set_theme once at the top of the notebook and every chart picks it up."
**Explain simply:**
- `style` controls the background and grid: `darkgrid` (the default), `whitegrid`, `dark`, `white`, `ticks`.
- `palette` sets the default colours, `font_scale` makes all text bigger or smaller.
- `context` ("paper", "notebook", "talk", "poster") scales sizes for where the chart will be shown.
- It also changes plain matplotlib charts afterwards, because seaborn updates matplotlib's global settings.
- `sns.set_theme()` is the current name; the older `sns.set()` still works but `set_theme` is preferred.
**Sample data:**
```python
import pandas as pd

headcount = pd.DataFrame({
    "department": ["Sales", "IT", "HR", "Finance"],
    "employees": [40, 55, 12, 20],
})
```
**Code (what you write in the interview):**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# Set the look once; every chart after this uses it
sns.set_theme(style="whitegrid", palette="pastel", font_scale=1.1)

sns.barplot(data=headcount, x="department", y="employees",
            hue="department", legend=False)
plt.title("Headcount by department")
plt.show()
```
**Output:** A bar chart on a white background with light gridlines and soft pastel bars, slightly larger text. No text is printed. (Plot not rendered in this document; the code ran without errors or warnings.)
**What it means:** One line gave every chart a consistent, clean look.
**Alternative:**
```python
# Only change the background style, keep everything else
sns.set_style("darkgrid")
```
**Likely follow-ups:** 1) *How do you go back to normal?* `sns.reset_defaults()` (or `plt.style.use("default")` for matplotlib). 2) *How do you remove the top and right border?* `sns.despine()`.
**Common mistakes:** Calling `set_theme` after drawing (it only affects later charts); mixing several styles in one report; forgetting that it also changes later matplotlib charts.

### Q24 ⭐⭐ 🟢 How do you show charts inline in a Jupyter notebook?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you have actually used notebooks and know the magic command and `plt.show()`.
**Say this in the interview:** "I put %matplotlib inline at the top, then the chart appears right below the cell. In current Jupyter it is already the default, and plt.show() is a good habit anyway."
**Explain simply:**
- `%matplotlib inline` is a Jupyter "magic command" (a special line starting with `%`). It tells the notebook to draw charts as pictures under the cell.
- It only works in Jupyter or IPython, not in a plain `.py` script (there it is a syntax error). In a script, use `plt.show()` to open a window, or `plt.savefig("chart.png")`.
- In modern Jupyter and VS Code notebooks inline is already the default (from memory, not tested here, since there is no notebook in this environment).
- Run the magic line before importing pyplot, ideally in the first cell.
**Code (what you write in the interview):**
```python
%matplotlib inline
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [10, 20, 15])
plt.title("Shows right below the cell")
plt.show()
```
**Output:** In a notebook, a small line chart appears under the cell. The magic line cannot run in plain Python, so I ran the same code without it: the chart was drawn and no errors occurred. (Plot not rendered in this document.)
**What it means:** The chart lives inside the notebook, so the report and the picture stay together.
**Alternative:**
```python
# Interactive charts you can zoom and pan (needs the ipympl package)
%matplotlib widget
```
**Likely follow-ups:** 1) *Why does my chart not appear in a script?* You need `plt.show()` at the end. 2) *How do you save a chart?* `plt.savefig("chart.png", dpi=150)` before `plt.show()`.
**Common mistakes:** Putting `%matplotlib inline` in a `.py` file; calling `plt.savefig` after `plt.show()` (saves a blank image); forgetting `plt.show()` outside notebooks.

### Q25 ⭐⭐ 🟡 Write code to create a 2x2 grid of subplots, each showing a different chart.
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you know `plt.subplots`, the figure versus axes idea, and how to index a grid.
**Say this in the interview:** "plt.subplots(2, 2) gives me a figure and a 2 by 2 array of axes. I draw each chart on its own axes with axes[row, column], then call tight_layout so nothing overlaps."
**Explain simply:**
- The **figure** is the whole page. Each **axes** is one chart on it. `subplots(2, 2)` creates the page and four empty charts.
- `axes` is a 2D array, so `axes[0, 1]` means row 0, column 1 (counting from zero).
- On an axes, titles use `set_title`, labels use `set_xlabel`, and limits use `set_xlim` (the `set_` versions), unlike `plt.title`.
- With one row or one column, `axes` is a 1D array, so `axes[0]` not `axes[0, 0]`: a common error.
- `sharex=True` or `sharey=True` makes charts share an axis.
**Sample data:** 60 made-up employees:
```python
import pandas as pd
import numpy as np

rng = np.random.default_rng(1)
employees = pd.DataFrame({
    "department": rng.choice(["Sales", "IT", "HR", "Finance"], size=60),
    "age": rng.integers(23, 55, size=60),
    "tenure_years": rng.integers(1, 15, size=60),
})
employees["salary"] = 30000 + employees["tenure_years"] * 2500 + rng.integers(-5000, 5000, size=60)
employees["left"] = rng.choice(["Left", "Stayed"], size=60, p=[0.3, 0.7])
```
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

# 2 rows x 2 columns; axes[row, column] picks one chart
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Top left: bar chart of headcount by department
headcount = employees["department"].value_counts()
axes[0, 0].bar(headcount.index, headcount.values)
axes[0, 0].set_title("Headcount by department")

# Top right: line chart of average salary by tenure
salary_by_tenure = employees.groupby("tenure_years")["salary"].mean()
axes[0, 1].plot(salary_by_tenure.index, salary_by_tenure.values)
axes[0, 1].set_title("Average salary by tenure")

# Bottom left: histogram of age
axes[1, 0].hist(employees["age"], bins=8)
axes[1, 0].set_title("Age distribution")

# Bottom right: scatter of tenure against salary
axes[1, 1].scatter(employees["tenure_years"], employees["salary"])
axes[1, 1].set_title("Tenure vs salary")

# Stop the titles and labels overlapping
fig.tight_layout()
plt.show()
```
**Output:** One page with four charts: a bar chart (top left), a line (top right), a histogram (bottom left) and a scatter (bottom right). No text is printed. (Plot not rendered in this document; the code ran without errors.)
**What it means:** One figure tells a small story: who works where, how pay grows with years, how old people are, and whether tenure drives pay.
**Alternative:**
```python
# Unpack the four charts into names instead of using [row, column]
fig, ((top_left, top_right), (bottom_left, bottom_right)) = plt.subplots(2, 2)
```
**Likely follow-ups:** 1) *How do you make one chart wider?* `plt.subplot_mosaic` or `GridSpec`. 2) *How do you add one title for the whole page?* `fig.suptitle("...")`.
**Common mistakes:** Using `axes[0]` on a 2D grid; mixing `plt.title` with axes (it only titles the last one); forgetting `tight_layout`.

### Q26 ⭐⭐ 🟡 What is the difference between seaborn countplot() and barplot()?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you understand that one counts rows and the other summarises a numeric column.
**Say this in the interview:** "countplot counts how many rows are in each category, so I only give it x. barplot plots a number, by default the average of a column per category, and adds a small error bar."
**Explain simply:**
- `countplot` = "how many?" It does the counting itself. Like `value_counts()` drawn as bars.
- `barplot` = "what is the average (or another statistic) of this column?" Like `groupby().mean()` drawn as bars. Use `estimator="sum"` to total instead.
- The thin black line on a barplot is an **error bar** (a 95% confidence interval: the range the true average probably lies in). It can be hidden with `errorbar=None`.
- If you already have counts in a table, use `barplot` (or `plt.bar`), not `countplot`.
**Sample data:** 60 made-up employees:
```python
import pandas as pd
import numpy as np

rng = np.random.default_rng(1)
employees = pd.DataFrame({
    "department": rng.choice(["Sales", "IT", "HR", "Finance"], size=60),
    "age": rng.integers(23, 55, size=60),
    "tenure_years": rng.integers(1, 15, size=60),
})
employees["salary"] = 30000 + employees["tenure_years"] * 2500 + rng.integers(-5000, 5000, size=60)
employees["left"] = rng.choice(["Left", "Stayed"], size=60, p=[0.3, 0.7])
```
**Code (what you write in the interview):**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# countplot counts the rows for you: only x is needed
sns.countplot(data=employees, x="department")
plt.title("Number of employees (countplot)")
plt.show()

# barplot needs a number column for y, and shows its average by default
sns.barplot(data=employees, x="department", y="salary")
plt.title("Average salary (barplot)")
plt.show()
```
**Output:** Chart 1: four bars showing how many employees are in each department. Chart 2: four bars showing average salary per department, each with a small error bar. No text is printed. (Plot not rendered in this document; the code ran without errors.)
**What it means:** The first chart answers headcount questions, the second answers pay questions.
**Alternative:**
```python
# The same two charts in plain pandas terms
print(employees["department"].value_counts())
print(employees.groupby("department")["salary"].mean().round(0))
```
```text
department
IT         19
Finance    18
Sales      14
HR          9
Name: count, dtype: int64
department
Finance    48411.0
HR         48616.0
IT         51617.0
Sales      53250.0
Name: salary, dtype: float64
```
**Likely follow-ups:** 1) *Can barplot show a total?* Yes: `estimator="sum"`. 2) *Can countplot split by a second category?* Yes: add `hue="left"`.
**Common mistakes:** Passing a `y` to `countplot` (error); thinking `barplot` shows totals; ignoring the error bars.

### Q27 ⭐⭐ 🟡 Write code to draw a histogram with a density curve (KDE) in seaborn and split it by a category using hue.
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you know `histplot`, `kde=True` and `hue`, and what a KDE is.
**Say this in the interview:** "I use sns.histplot with x as the column, kde=True for the smooth curve, and hue set to the category so each group gets its own colour."
**Explain simply:**
- A **histogram** groups values into ranges (bins) and counts how many fall in each bin.
- A **KDE** (kernel density estimate) is a smooth curve drawn through the histogram, showing the shape of the distribution without the bin jumpiness.
- `hue="left"` draws one histogram and one curve per group, overlaid in different colours.
- If one group is much bigger, its bars look taller. For comparing shapes use `stat="density", common_norm=False`.
**Sample data:** 60 made-up employees:
```python
import pandas as pd
import numpy as np

rng = np.random.default_rng(1)
employees = pd.DataFrame({
    "department": rng.choice(["Sales", "IT", "HR", "Finance"], size=60),
    "age": rng.integers(23, 55, size=60),
    "tenure_years": rng.integers(1, 15, size=60),
})
employees["salary"] = 30000 + employees["tenure_years"] * 2500 + rng.integers(-5000, 5000, size=60)
employees["left"] = rng.choice(["Left", "Stayed"], size=60, p=[0.3, 0.7])
```
**Code (what you write in the interview):**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# hue splits the data by the "left" column; kde=True adds the smooth curve
sns.histplot(data=employees, x="salary", hue="left", kde=True)
plt.title("Salary distribution: employees who left vs stayed")
plt.show()
```
**Output:** Two overlapping histograms (Left and Stayed) with a smooth curve over each, and a legend. No text is printed. (Plot not rendered in this document; the code ran without errors.)
**What it means:** If the "Left" curve sits to the left of "Stayed", people who left tended to earn less.
**Alternative:**
```python
# Compare groups of different sizes fairly: show shares, not counts
sns.histplot(data=employees, x="salary", hue="left", kde=True, stat="density", common_norm=False)
plt.show()
```
**Likely follow-ups:** 1) *How do you change the number of bins?* `bins=15`. 2) *How do you stack instead of overlay?* `multiple="stack"`.
**Common mistakes:** Using the deprecated `distplot` (see Q28); comparing raw counts of groups with different sizes; too few rows for a meaningful curve.

### Q28 ⭐⭐ 🟡 What is the difference between histplot, displot and the deprecated distplot in seaborn?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you know the difference between axes-level and figure-level functions, and that `distplot` is outdated.
**Say this in the interview:** "histplot draws one histogram on one chart. displot is the figure-level version: it can split into several charts with col or row. distplot is the old function, deprecated, so I use histplot or displot instead."
**Explain simply:**
- **Axes-level** (`histplot`): draws onto one chart; you can place it in a `subplots` grid and use `plt.title`.
- **Figure-level** (`displot`): creates its own whole figure, so it can make a grid of charts with `col=` or `row=`. Resize it with `height=` and `aspect=`, not `figsize`.
- `displot(kind=...)` can be `"hist"` (default), `"kde"` or `"ecdf"`.
- `distplot` is deprecated. I ran it on seaborn 0.13.2: it still works but prints a warning saying it will be removed in v0.14.0.
**Sample data:** 60 made-up employees:
```python
import pandas as pd
import numpy as np

rng = np.random.default_rng(1)
employees = pd.DataFrame({
    "department": rng.choice(["Sales", "IT", "HR", "Finance"], size=60),
    "age": rng.integers(23, 55, size=60),
    "tenure_years": rng.integers(1, 15, size=60),
})
employees["salary"] = 30000 + employees["tenure_years"] * 2500 + rng.integers(-5000, 5000, size=60)
employees["left"] = rng.choice(["Left", "Stayed"], size=60, p=[0.3, 0.7])
```
**Code (what you write in the interview):**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# histplot: one histogram on one chart
sns.histplot(data=employees, x="salary", kde=True)
plt.show()

# displot: the same, but it can make a separate chart per department
sns.displot(data=employees, x="salary", col="department", col_wrap=2, kde=True)
plt.show()
```
**Output:** Chart 1: one histogram of salary with a curve. Chart 2: four small histograms in a 2 by 2 grid, one per department. No text is printed. (Plot not rendered in this document; the code ran without errors.)
**What it means:** Use `histplot` for one chart and `displot` when you want the same chart repeated for each group.
**Alternative:**
```python
# Old code you may see online: still runs, but warns and is slated for removal
sns.distplot(employees["salary"])
```
**Likely follow-ups:** 1) *Which one for a subplots grid?* `histplot`, because it takes `ax=`. 2) *Replacement for `distplot(kde=False)`?* `histplot`.
**Common mistakes:** Using `distplot` from old tutorials; passing `ax=` to `displot` (not supported); setting `figsize` on `displot`.

### Q29 ⭐⭐ 🟡 Write code to draw a stacked bar chart of employees who left and stayed, by department.
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you can reshape data into a table of counts, then plot it stacked.
**Say this in the interview:** "First I count with pd.crosstab so each department is a row and Left and Stayed are columns. Then plot with kind=bar and stacked=True."
**Explain simply:**
- A **crosstab** is a counting table: rows are one category, columns another, cells are how many rows match both.
- pandas draws one bar per row of the table. `stacked=True` piles the columns on top of each other instead of placing them side by side.
- A stacked bar shows the total (height) and the parts (segments). The bottom segment is easy to compare across bars; the top ones are harder.
- To compare attrition fairly between big and small departments, use percentages (the Alternative).
**Sample data:**
```python
import pandas as pd

employees = pd.DataFrame({
    "department": ["Sales", "Sales", "Sales", "IT", "IT", "HR", "HR", "Finance", "Finance", "Sales", "IT", "HR"],
    "status": ["Left", "Stayed", "Stayed", "Stayed", "Left", "Stayed", "Stayed", "Left", "Stayed", "Left", "Stayed", "Stayed"],
})
```
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

# Count employees for every department and status pair
counts = pd.crosstab(employees["department"], employees["status"])
print(counts)

# stacked=True piles the Stayed bar on top of the Left bar
counts.plot(kind="bar", stacked=True)
plt.title("Employees who left and stayed, by department")
plt.ylabel("Employees")
plt.xticks(rotation=0)
plt.show()
```
**Output:**
```text
status      Left  Stayed
department              
Finance        1       1
HR             0       3
IT             1       2
Sales          2       2
```
Plus a stacked bar chart with one bar per department. (Plot not rendered in this document; the table above is the real data it draws.)
**What it means:** Sales has the most people and the most leavers (2), but compare shares before judging a department.
**Alternative:**
```python
# Show the share of leavers in each department instead (each bar adds to 100%)
shares = pd.crosstab(employees["department"], employees["status"], normalize="index") * 100
shares.plot(kind="bar", stacked=True)
plt.show()
```
**Likely follow-ups:** 1) *How do you put Left at the bottom?* Reorder the columns: `counts[["Left", "Stayed"]]`. 2) *Why the percentage version?* Raw counts hide that a small department may lose a bigger share.
**Common mistakes:** Plotting the raw rows instead of the counted table; forgetting `stacked=True` (gives side-by-side bars); long department names overlapping (rotate the labels).

### Q30 ⭐⭐ 🟡 Write code to draw a grouped (side-by-side) bar chart comparing two years of revenue by region.
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you can get data in the right shape (wide for pandas, long for seaborn) and know that side by side is the default.
**Say this in the interview:** "With one column per year, pandas draws grouped bars automatically: revenue.plot with x as region and kind bar. In seaborn I would reshape to long form and use hue for the year."
**Explain simply:**
- **Grouped** bars sit side by side (default). **Stacked** bars pile up (needs `stacked=True`). Grouped is better for comparing years; stacked is better for totals.
- **Wide** data has one column per year (our table). **Long** data has one row per region and year. pandas plotting likes wide; seaborn likes long.
- `melt` turns wide into long. Column names here are text ("2024"), which keeps pandas from treating them as numbers.
- The unit "lakhs" is made up for the sample; use your real unit.
**Sample data:**
```python
import pandas as pd

revenue = pd.DataFrame({
    "region": ["North", "South", "East", "West"],
    "2024": [120, 95, 80, 110],
    "2025": [135, 90, 100, 125],
})
```
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

# Region on the x axis; each year column becomes one bar in the group
revenue.plot(x="region", kind="bar")
plt.title("Revenue by region: 2024 vs 2025")
plt.ylabel("Revenue (lakhs)")
plt.xticks(rotation=0)
plt.show()
```
**Output:** A bar chart with four groups (North, South, East, West); each group has two bars, one for 2024 and one for 2025, and a legend. No text is printed. (Plot not rendered in this document; both versions ran without errors.)
**What it means:** North, East and West grew; South dropped from 95 to 90.
**Alternative:**
```python
import seaborn as sns

# Seaborn wants long data: one row per region and year
revenue_long = revenue.melt(id_vars="region", var_name="year", value_name="revenue")
sns.barplot(data=revenue_long, x="region", y="revenue", hue="year")
plt.show()
```
**Likely follow-ups:** 1) *How do you add values on top?* `bar_label` for each container (see Q20). 2) *How do you widen the bars?* `width=0.8`.
**Common mistakes:** Forgetting `x="region"` (region becomes a third bar series or errors); using wide data in seaborn; leaving the labels rotated and hard to read.

### Q31 ⭐⭐ 🟡 What is the hue parameter in seaborn, and how do you use it on a scatter plot?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you know `hue` adds a third variable to a chart using colour.
**Say this in the interview:** "hue splits the data by a column and gives each group its own colour, so I can add a third variable to a two-variable scatter plot. I just pass hue equals the column name."
**Explain simply:**
- A scatter plot normally shows two numbers (x and y). `hue` adds a third variable through colour, and a legend is created automatically.
- With a **category** column (department), you get separate colours. With a **number** column, you get a smooth colour gradient.
- `style=` changes marker shape and `size=` changes marker size, for even more variables. Do not overdo it.
- `hue` works in most seaborn charts (`barplot`, `histplot`, `boxplot`, `lineplot`), not only scatter.
**Sample data:** 60 made-up employees:
```python
import pandas as pd
import numpy as np

rng = np.random.default_rng(1)
employees = pd.DataFrame({
    "department": rng.choice(["Sales", "IT", "HR", "Finance"], size=60),
    "age": rng.integers(23, 55, size=60),
    "tenure_years": rng.integers(1, 15, size=60),
})
employees["salary"] = 30000 + employees["tenure_years"] * 2500 + rng.integers(-5000, 5000, size=60)
employees["left"] = rng.choice(["Left", "Stayed"], size=60, p=[0.3, 0.7])
```
**Code (what you write in the interview):**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# hue colours each dot by department
sns.scatterplot(data=employees, x="tenure_years", y="salary", hue="department")
plt.title("Salary vs tenure, coloured by department")
plt.show()
```
**Output:** A scatter plot of tenure against salary with dots in four colours (one per department) and a legend. No text is printed. (Plot not rendered in this document; both versions ran without errors.)
**What it means:** You can see whether the pay and tenure pattern is the same in every department or one department stands out.
**Alternative:**
```python
# Also change the dot shape by attrition status, for a second split
sns.scatterplot(data=employees, x="tenure_years", y="salary",
                hue="department", style="left", palette="Set2")
plt.show()
```
**Likely follow-ups:** 1) *How do you control the colours?* `palette=`. 2) *How do you move the legend outside?* `plt.legend(bbox_to_anchor=(1, 1))`.
**Common mistakes:** Using `hue` with too many categories (a rainbow nobody can read); using a number column with few distinct values and expecting separate colours; forgetting `data=` when passing column names.

### Q32 ⭐⭐ 🟡 What does sns.pairplot() show, and when is it useful or a bad idea?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you know it is a quick exploration tool and can say when to avoid it.
**Say this in the interview:** "pairplot draws a grid: a scatter plot for every pair of numeric columns, and a histogram of each column on the diagonal. It is great for a first look at relationships. It is a bad idea with many columns or many rows."
**Explain simply:**
- With 3 numeric columns you get a 3 by 3 grid of 9 small charts. Off-diagonal cells show how two columns relate; the diagonal shows each column's distribution.
- `hue="left"` colours points by group, so you can see whether leavers behave differently.
- **Useful for:** early exploration, spotting linear patterns, clusters and outliers, and choosing which pairs to study.
- **Bad idea when:** there are many columns (10 columns means 100 charts, unreadable and slow), huge datasets (points pile up and the plot takes a long time), or data is mostly categorical (it ignores text columns).
- It only shows patterns; it does not prove cause and effect.
**Sample data:** 60 made-up employees:
```python
import pandas as pd
import numpy as np

rng = np.random.default_rng(1)
employees = pd.DataFrame({
    "department": rng.choice(["Sales", "IT", "HR", "Finance"], size=60),
    "age": rng.integers(23, 55, size=60),
    "tenure_years": rng.integers(1, 15, size=60),
})
employees["salary"] = 30000 + employees["tenure_years"] * 2500 + rng.integers(-5000, 5000, size=60)
employees["left"] = rng.choice(["Left", "Stayed"], size=60, p=[0.3, 0.7])
```
**Code (what you write in the interview):**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# Pick only the numeric columns you care about; hue colours by attrition
columns_to_compare = ["age", "tenure_years", "salary", "left"]
sns.pairplot(employees[columns_to_compare], hue="left")
plt.show()
```
**Output:** A 3 by 3 grid (age, tenure_years, salary) with scatter plots off the diagonal, histograms on the diagonal, and two colours for Left and Stayed. No text is printed. (Plot not rendered in this document; both versions ran without errors.)
**What it means:** In the tenure and salary panel, the dots slope upward: longer tenure tends to go with higher pay.
**Alternative:**
```python
# Same idea for one pair only, when pairplot is too much
sns.scatterplot(data=employees, x="tenure_years", y="salary", hue="left")
plt.show()
```
**Likely follow-ups:** 1) *How do you limit the columns?* `vars=[...]` or select columns first. 2) *What is the next step after spotting a pattern?* Check it with a correlation number or a proper test.
**Common mistakes:** Running it on a whole 30-column table; reading a pattern as cause and effect; forgetting that overlapping points hide density.

### Q33 ⭐⭐ 🟡 Write code to plot daily attendance as a time series with readable date labels on the x-axis.
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you know the date column must be a real datetime, and how to stop labels from overlapping.
**Say this in the interview:** "I make sure the date column is a datetime, plot date against value, and call fig.autofmt_xdate() so the date labels tilt and stay readable. For full control I use a date formatter."
**Explain simply:**
- Matplotlib understands dates only when the column is a `datetime` type. If dates are text, convert first: `df["date"] = pd.to_datetime(df["date"])`. Otherwise every date becomes its own label, which is a mess.
- `fig.autofmt_xdate()` rotates the labels and aligns them to the right.
- Optional: `DateFormatter("%d %b")` sets the style (`%d` day, `%b` short month, `%Y` year) and `WeekdayLocator` decides how often a label appears.
- The dips in this sample are weekends (low attendance), a good pattern to point out.
**Sample data:** 30 days of attendance (weekend dips):
```python
import pandas as pd

attendance = pd.DataFrame({
    "date": pd.date_range("2026-03-01", periods=30),
    "present": [52, 50, 55, 54, 53, 20, 18, 51, 53, 56, 55, 52, 19, 17, 50,
                54, 55, 53, 51, 22, 18, 52, 56, 54, 55, 53, 21, 19, 50, 52],
})
```
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(attendance["date"], attendance["present"])

ax.set_title("Daily attendance, March 2026")
ax.set_ylabel("Employees present")

# Tilt and align the date labels so they do not overlap
fig.autofmt_xdate()
plt.show()
```
**Output:** A wide line chart of March 2026; the date labels are tilted at the bottom; the line dips sharply on every weekend. No text is printed. (Plot not rendered in this document; both versions ran without errors.)
**What it means:** Weekday attendance sits around 50 to 56; weekends drop to under 25.
**Alternative:**
```python
import matplotlib.dates as mdates

# Choose exactly which dates are labelled and how they look: a tick every week, like "02 Mar"
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(attendance["date"], attendance["present"])
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
fig.autofmt_xdate()
plt.show()
```
**Likely follow-ups:** 1) *How do you plot a 7-day average?* `attendance["present"].rolling(7).mean()` and plot that as a second line. 2) *How do you plot per month?* `resample("ME", on="date").sum()` first (needs pandas 2.2+; "M" in older versions, from memory).
**Common mistakes:** Plotting text dates; forgetting to sort by date; labels so crowded they overlap.

### Q34 ⭐⭐ 🟡 How do you spot outliers visually with a boxplot, and then find those rows in pandas?
**Asked at:** commonly asked (no company-specific report found); appears in matplotlib/seaborn question banks (TechPrep, Testbook, PythonGuides; snippet-level only)
**What the interviewer is checking:** Whether you can read a boxplot and then turn what you see into code that returns the actual rows.
**Say this in the interview:** "In the boxplot, dots beyond the whiskers are possible outliers. Then I calculate the same limits in pandas, Q1 minus 1.5 times IQR and Q3 plus 1.5 times IQR, and filter the rows outside them."
**Explain simply:**
- A **boxplot** draws the middle 50% of values as a box. The line inside is the median. Whiskers reach to the furthest value inside the limits; dots beyond are flagged.
- **Q1** and **Q3** are the 25th and 75th percentiles. The **IQR** (interquartile range) is Q3 minus Q1, the width of the box.
- The standard rule: a value is an outlier if it is below Q1 - 1.5 x IQR or above Q3 + 1.5 x IQR. That is exactly where the whiskers stop.
- An outlier is not automatically an error. Check it: a data-entry typo (12000 instead of 120000) or a real executive salary? Decide whether to fix, keep, or report it separately.
**Sample data:**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meera", "Karan", "Sita", "Dev", "Anil", "Priya", "Rohan", "Neha"],
    "salary": [42000, 45000, 47000, 44000, 46000, 43000, 48000, 45500, 160000, 12000],
})
```
**Code (what you write in the interview):**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: look. Dots beyond the whiskers are possible outliers
sns.boxplot(data=employees, x="salary")
plt.show()

# Step 2: find those rows with the same rule the boxplot uses (1.5 x IQR)
q1 = employees["salary"].quantile(0.25)
q3 = employees["salary"].quantile(0.75)
iqr = q3 - q1
lower_limit = q1 - 1.5 * iqr
upper_limit = q3 + 1.5 * iqr

outliers = employees[(employees["salary"] < lower_limit) | (employees["salary"] > upper_limit)]
print(outliers)
```
**Output:**
```text
    name  salary
8  Rohan  160000
9   Neha   12000
```
Plus a horizontal boxplot with two dots far outside the box. (Plot not rendered in this document; the printed rows are real.)
**What it means:** Two employees, Rohan (160,000) and Neha (12,000), sit far outside the normal 42,000 to 48,000 range and should be checked.
**Alternative:**
```python
# Z-score alternative: more than 3 standard deviations from the mean
z_scores = (employees["salary"] - employees["salary"].mean()) / employees["salary"].std()
print(employees[z_scores.abs() > 3])
```
```text
Empty DataFrame
Columns: [name, salary]
Index: []
```
In this tiny sample the z-score rule finds nothing, because the two extreme values inflate the standard deviation and hide each other. The IQR rule is more robust for small or skewed data.
**Likely follow-ups:** 1) *Do you always remove outliers?* No: investigate first; remove only if clearly an error. 2) *Why does IQR work better than the mean and standard deviation?* Quartiles are not pulled by extreme values.
**Common mistakes:** Deleting outliers without checking them; using a z-score rule on skewed or tiny data; forgetting the lower limit.

### Q35 ⭐⭐ 🟡 What is a violin plot, and how does it differ from a boxplot?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a violin plot is a boxplot plus the shape of the data?
**Say this in the interview:** "A boxplot shows five summary numbers. A violin plot adds a mirrored curve showing how many people sit at each value, so I can see two humps, which a box would hide."
**Explain simply:**
- A boxplot shows the median, the middle half of values (the box) and the outliers (dots). It says nothing about the shape.
- A violin draws a smooth curve (a density estimate, meaning 'how crowded is each value') on both sides. Wide part = many employees at that salary.
- Use a violin when you suspect two groups inside one (for example junior and senior staff in Sales). Use a boxplot for a quick, simple comparison.
- With very few points (under about 20 per group) the curve is unreliable; a boxplot or dots are safer.
**Sample data:** Salary in thousands, 6 employees per department (in the code below).
**Code (what you write in the interview):**
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

employees = pd.DataFrame({
    "department": ["Sales"] * 6 + ["IT"] * 6,
    "salary": [30, 32, 35, 36, 70, 75, 48, 50, 52, 55, 58, 60],  # in thousands
})

# violin: the shape shows where most salaries sit
sns.violinplot(data=employees, x="department", y="salary")
plt.title("Salary spread by department")
plt.show()
```
**Output:** (chart only, no printed output). Sales should show two humps (about 30-36 and 70-75) while IT is one smooth bump; a boxplot of Sales would show just one wide box.
**What it means:** Sales has two salary clusters, which the violin reveals and a boxplot hides.
**Alternative:** `sns.boxplot` for the plain version; `sns.violinplot(..., inner="box")` draws a small box inside the violin.
**Likely follow-ups:**
- *Is a violin always better?* No. It is harder for managers to read and misleads on small samples.
- *What is `inner`?* What to draw inside the violin: box, points, quartiles or nothing.
**Common mistakes:** Using a violin on tiny groups; forgetting the curve is smoothed, so it can extend past the real minimum and maximum (use `cut=0` to stop that).

### Q36 ⭐⭐ 🟡 What is plt.tight_layout() (or constrained_layout), and when do you need it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know how to stop labels and titles overlapping or being cut off?
**Say this in the interview:** "`tight_layout()` automatically adjusts the spacing between charts and the edges so nothing overlaps. I call it right before showing or saving. The newer option is `layout="constrained"` set when creating the figure."
**Explain simply:**
- Matplotlib places charts using fixed default margins. Long labels, rotated text or several charts side by side then collide or get cut off.
- `fig.tight_layout()` recalculates the margins to fit everything. Call it after all titles and labels are set.
- `plt.subplots(..., layout="constrained")` does the same but keeps adjusting, and also handles legends and colourbars better.
- You need it for multiple subplots, long category names and saved images.
**Sample data:** Three long department names on the x-axis and two charts side by side (in the code).
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

departments = ["Customer Support", "Human Resources", "Information Technology"]
attrition = [14, 6, 9]

fig, (left_chart, right_chart) = plt.subplots(1, 2, figsize=(9, 3))

left_chart.bar(departments, attrition)
left_chart.set_title("Attrition % by department")
left_chart.set_xlabel("Department")
left_chart.set_ylabel("Attrition %")
left_chart.tick_params(axis="x", rotation=30)

right_chart.plot([1, 2, 3], [5, 7, 6])
right_chart.set_title("Hires per month")

# stops labels and titles from being cut off or overlapping
fig.tight_layout()
plt.show()
```
**Output:** (chart only, no printed output). Without the last line the long names and the second title crowd each other; with it, everything fits.
**What it means:** Everything fits inside the image with no overlap or clipping.
**Alternative:** `fig, axes = plt.subplots(1, 2, layout="constrained")` instead of calling `tight_layout()`.
**Likely follow-ups:**
- *Tight vs constrained?* Constrained is newer and more reliable; do not mix both.
- *Legend outside the plot still cut off when saving?* Use `savefig(..., bbox_inches="tight")`.
**Common mistakes:** Calling `tight_layout()` before adding labels (so it fits the old layout); using both layout methods together.

### Q37 ⭐⭐ 🟡 How do you handle missing values before plotting, and what does matplotlib do with NaN?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you check for missing data first and know what a plot does with it?
**Say this in the interview:** "First I count the missing values with isna. Matplotlib does not crash on NaN, it just leaves a gap in a line or skips the bar, so I decide whether to drop, fill or leave the gap, based on what is true for the business."
**Explain simply:**
- NaN means 'not a number', the way pandas stores a blank cell.
- Matplotlib skips NaN points: a line breaks into pieces, a bar is missing, no error is raised. That silence is the danger.
- Drop (`dropna`) when the days really have no data. Fill (`fillna`) only with a reason, for example 0 absences when nobody was absent, never an invented average for attendance.
- Dropping rows from a line chart joins the neighbouring points, which can hide a real gap in data. Say that in a note.
**Sample data:** Attendance with two missing days (day 3 and 4).
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

attendance = pd.DataFrame({
    "day": [1, 2, 3, 4, 5, 6],
    "hours_worked": [8.0, 7.5, None, None, 8.0, 7.0],
})

# 1. see how many values are missing
print(attendance["hours_worked"].isna().sum())

# 2. decide: drop the missing days (or fill them if the business agrees)
clean_attendance = attendance.dropna(subset=["hours_worked"])

plt.plot(attendance["day"], attendance["hours_worked"], label="with gap")
plt.plot(clean_attendance["day"], clean_attendance["hours_worked"], "--", label="missing days dropped")
plt.legend()
plt.show()
```
**Output:**
```
2
```
**What it means:** Two days have no hours. The raw line shows the gap honestly; the dropped version hides it.
**Alternative:** `attendance["hours_worked"].interpolate()` draws a straight estimate across the gap (only for smooth, continuous data).
**Likely follow-ups:**
- *How do you find where the gaps are?* `attendance[attendance["hours_worked"].isna()]`.
- *Does a plot treat 0 like NaN?* No, 0 is drawn as a real value, so filling NaN with 0 drags the line down.
**Common mistakes:** Filling every blank with 0 or the mean without thinking; thinking the data is complete because no error appeared.

### Q38 ⭐⭐ 🟡 My plot shows nothing or shows an error such as ValueError x and y must have the same size. How do you debug it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you debug in a calm order: check the data first, then the code?
**Say this in the interview:** "For the size error I print the length of x and y, because plot needs the same number of each. For a blank chart I check the data is not empty after my filter and that I called plt.show()."
**Explain simply:**
- `ValueError: x and y must have same first dimension` means x and y have different lengths: here 5 months but only 4 hire counts.
- A blank chart usually means the data was empty (a filter matched nothing, or a typo in the filter value), or all values were NaN, or `plt.show()` was missing in a script.
- Check in this order: `len()` or `.shape` of both inputs, `.empty` on the DataFrame, `.isna().sum()`, then the dtypes (numbers stored as text plot as categories).
- Fix the cause (find the missing month), not the symptom (do not just cut months to length 4).
**Sample data:** 5 months but 4 hire counts; a filter that matches no row (in the code).
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May"]
hires = [12, 15, 9, 14]  # one value is missing

# step 1: compare lengths
print(len(months), len(hires))

# step 2: for a DataFrame, check it is not empty after filtering
hiring = pd.DataFrame({"month": months[:4], "hires": hires})
it_hiring = hiring[hiring["month"] == "Dec"]
print(it_hiring.empty)

plt.plot(months, hires)
```
**Output:**
```
5 4
True
```
**What it means:** Lengths 5 and 4 explain the error. `True` means the filtered DataFrame is empty, so a plot of it would be blank. The prints point to the problem before touching the chart code.
**Alternative:** Plotting straight from the DataFrame (`hiring.plot(x="month", y="hires")`) removes the length problem because both columns come from one table.
**Likely follow-ups:**
- *Plot is blank in a Jupyter notebook?* Check the cell ran and the inline backend is on.
- *Numbers on the axis are in the wrong order?* They are probably text; convert with `astype(float)`.
**Common mistakes:** Padding the shorter list with zeros to silence the error; not checking an empty filter result.

### Q39 ⭐⭐ 🟡 Why does a KeyError appear when plotting a DataFrame column, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a KeyError means the name does not match exactly?
**Say this in the interview:** "A KeyError means pandas cannot find that exact column name. I print df.columns, usually spot a trailing space, different capital letters or a typo, then clean the names once with strip and lower."
**Explain simply:**
- `KeyError: 'department'` means 'no column called exactly that'. Spaces and capitals count: `"Department "` is not `"department"`.
- Excel files often come with trailing spaces or mixed case headers.
- Print `df.columns.tolist()` (a list shows the spaces inside the quotes).
- Clean all headers once: `df.columns = df.columns.str.strip().str.lower()`. Optionally replace spaces with underscores.
**Sample data:** One column has a trailing space (`"Department "`), so `employees["Department"]` fails.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "Department ": ["Sales", "IT", "Sales"],
    "Salary": [40000, 55000, 42000],
})

# step 1: look at the exact column names
print(employees.columns.tolist())

# step 2: clean them once, then use the clean names
employees.columns = employees.columns.str.strip().str.lower()
print(employees.columns.tolist())

employees.groupby("department")["salary"].mean().plot(kind="bar")
```
**Output:**
```
['Department ', 'Salary']
['department', 'salary']
```
**What it means:** The name was the problem, not the plot. The first list shows the hidden trailing space.
**Alternative:** `employees.rename(columns={"Department ": "department"})` fixes only the named column.
**Likely follow-ups:**
- *KeyError after groupby?* The grouping column became the index; use `reset_index()`.
- *Same error on `df[["a","b"]]`?* Check each name in the list.
**Common mistakes:** Retyping the name again and again instead of printing the columns; forgetting to use the clean names everywhere afterwards.

### Q40 ⭐ 🟡 How do you draw a horizontal reference line, such as the company average attrition, on a chart?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you add context (a benchmark) to a chart in one line?
**Say this in the interview:** "I use axhline with the average value. That draws a horizontal line across the chart, and I label it so a manager sees which departments are above or below average."
**Explain simply:**
- `plt.axhline(y)` draws a horizontal line at height y across the whole chart. `axvline` draws a vertical one.
- Calculate the average with pandas, do not type the number by hand, so it updates with new data.
- Give it a `label` and call `legend()` so the line is explained; a dashed red line stands out from the bars.
- Note: the average of department rates is not the true company rate when departments differ in size; use total left / total headcount for the company figure.
**Sample data:** Four departments with attrition rates.
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

attrition = pd.DataFrame({
    "department": ["Sales", "IT", "HR", "Finance"],
    "attrition_rate": [18, 10, 6, 8],
})
company_average = attrition["attrition_rate"].mean()

plt.bar(attrition["department"], attrition["attrition_rate"])

# horizontal line at the company average
plt.axhline(company_average, color="red", linestyle="--", label=f"Company average ({company_average:.1f}%)")
plt.ylabel("Attrition %")
plt.legend()
plt.show()
```
**Output:** (chart only, no printed output). Four bars with a dashed red line at 10.5%: Sales (18) is above it, HR (6), Finance (8) and IT (10) are below.
**What it means:** Sales stands out above the company average, the rest are below.
**Alternative:** With the object style: `ax.axhline(company_average, ...)`. For a band use `ax.axhspan(8, 12, alpha=0.2)`.
**Likely follow-ups:**
- *Line for a target, not an average?* Same call with the target value.
- *Horizontal bar chart?* Then use `axvline`.
**Common mistakes:** Hard-coding the average; forgetting the legend so nobody knows what the line is.

### Q41 ⭐ 🟡 How do you create a chart with two y-axes using twinx(), and when is it a bad idea?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know twinx and also why dual axes can mislead?
**Say this in the interview:** "twinx makes a second y-axis sharing the same x-axis, so I can show headcount as bars on the left and attrition rate as a line on the right. I use it carefully, because two scales can be stretched to suggest a link that is not there."
**Explain simply:**
- `ax.twinx()` creates a second axes on top, with the same x and its own y-axis on the right.
- Colour the line and its axis label the same so readers know which axis belongs to which series.
- Good use: two measures in different units over the same months (people vs percent).
- Bad idea: the two y-ranges are chosen freely, so you can make lines cross or move together by changing the scale. Prefer two stacked charts when you can.
**Sample data:** Five months of headcount (count) and attrition rate (percent).
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May"]
headcount = [200, 210, 220, 215, 225]
attrition_rate = [2.1, 1.8, 2.5, 3.0, 2.2]

fig, left_axis = plt.subplots()

# left axis: headcount as bars
left_axis.bar(months, headcount, color="lightsteelblue")
left_axis.set_ylabel("Headcount")

# twinx() gives a second y-axis that shares the same x-axis
right_axis = left_axis.twinx()
right_axis.plot(months, attrition_rate, color="red", marker="o")
right_axis.set_ylabel("Attrition %")

plt.title("Headcount and attrition")
plt.show()
```
**Output:** (chart only, no printed output). Bars for headcount on the left axis, a red line with dots for attrition % on the right axis.
**What it means:** One picture shows how team size and attrition moved month by month.
**Alternative:** Two charts stacked with `plt.subplots(2, 1, sharex=True)`, usually clearer and cannot be manipulated by axis range.
**Likely follow-ups:**
- *Why risky?* Axis ranges are arbitrary, so the visual correlation is arbitrary.
- *Can you add a third axis?* Possible but a sign you need separate charts.
**Common mistakes:** Not labelling both axes; using the same colour for both series; reading the point where lines cross as meaningful.

### Q42 ⭐ 🟡 How do you customise a seaborn heatmap: annotations, colour map, centre value and hiding the upper triangle?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the main heatmap arguments and why the mask is used?
**Say this in the interview:** "I use annot=True to print the numbers, cmap to choose colours, center=0 so zero is the neutral colour for correlations, and a mask from numpy triu to hide the repeated upper half."
**Explain simply:**
- A heatmap colours a table of numbers; a correlation table (values -1 to +1) is the classic case.
- `annot=True` writes the number in each cell; `fmt=".2f"` rounds to 2 decimals.
- `cmap="coolwarm"` with `center=0` makes positive red, negative blue, zero white. `vmin=-1, vmax=1` keeps colours comparable across charts.
- The table is mirrored along the diagonal, so `np.triu(...)` builds a True/False grid for the upper triangle and `mask=` hides those cells.
**Sample data:** Four columns for eight employees (invented, tiny sample, so correlations come out very high).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

employees = pd.DataFrame({
    "age": [24, 29, 35, 41, 28, 50, 33, 45],
    "tenure_years": [1, 3, 8, 12, 2, 20, 6, 15],
    "salary": [30, 38, 60, 75, 35, 95, 52, 80],
    "engagement": [8, 7, 6, 5, 9, 4, 7, 5],
})
correlations = employees.corr()

# hide the upper triangle, it repeats the lower one
hide_upper = np.triu(np.ones_like(correlations, dtype=bool))

sns.heatmap(correlations, mask=hide_upper, annot=True, fmt=".2f",
            cmap="coolwarm", center=0, vmin=-1, vmax=1)
plt.show()
```
**Output:** (chart only, no printed output). Lower triangle only: age, tenure and salary all about 0.99 correlated with each other, engagement about -0.94 with each.
**What it means:** Older, longer-tenured staff earn more and, in this sample, report lower engagement. Correlation is not cause.
**Alternative:** `sns.heatmap(correlations, annot=True, cmap="Blues")` without a mask is fine for a quick look.
**Likely follow-ups:**
- *Why center?* So that 0 gets the neutral colour; otherwise the middle colour is the data midpoint.
- *Which correlation does `corr()` use?* Pearson by default, for numbers only.
**Common mistakes:** Running `corr()` with text columns (select numeric columns first); forgetting `vmin/vmax`; reading strong correlation as cause.

### Q43 ⭐ 🟡 What are FacetGrid, catplot and relplot in seaborn, and when do you use them?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know seaborn's way of making one panel per group?
**Say this in the interview:** "All three make a grid of small charts, one per group. catplot is for category charts, relplot for relationship charts like scatter and line, and FacetGrid is the manual base underneath when I want to choose the plot myself."
**Explain simply:**
- Small multiples = the same chart repeated per group (for example per department), so groups compare side by side.
- `catplot(kind=...)`: box, bar, violin, strip, count. Use `col=` or `row=` to split into panels.
- `relplot(kind="scatter" or "line")`: two numeric columns, plus `hue` for colour and `col` for panels.
- `FacetGrid` + `.map(function, column)` is the most flexible, with more code. These create their own figure, so you do not call `plt.subplots` first.
**Sample data:** Six employees with department, gender, tenure and salary.
**Code (what you write in the interview):**
```python
import pandas as pd
import seaborn as sns

employees = pd.DataFrame({
    "department": ["Sales", "Sales", "IT", "IT", "Sales", "IT"],
    "gender": ["F", "M", "F", "M", "F", "M"],
    "salary": [30, 35, 50, 55, 33, 60],
    "tenure_years": [1, 3, 2, 6, 2, 8],
})

# catplot: category on x, one panel per gender
sns.catplot(data=employees, x="department", y="salary", kind="box", col="gender")

# relplot: relationship (scatter or line), one panel per department
sns.relplot(data=employees, x="tenure_years", y="salary", col="department", kind="scatter")

# FacetGrid: the manual version, you choose the plot for every panel
grid = sns.FacetGrid(employees, col="department")
grid.map(sns.histplot, "salary")
```
**Output:** (chart only, no printed output). catplot: two panels (F, M) of salary boxes by department; relplot: two scatter panels (Sales, IT); FacetGrid: two salary histograms.
**What it means:** Same data, split into panels so each group is easy to compare.
**Alternative:** Plain matplotlib `plt.subplots` plus a loop gives full control, with more code.
**Likely follow-ups:**
- *Difference from `hue`?* `hue` colours groups inside one chart; `col` gives each group its own chart.
- *Why can't I put catplot in a subplot?* They are figure-level and make their own figure.
**Common mistakes:** Passing `ax=` to catplot or relplot (not supported); too many panels to read; forgetting that `catplot` defaults to a strip (dot) plot.

### Q44 ⭐ 🟡 How do you plot a scatter plot with a very large number of points so it stays readable?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know overplotting (points piling on top of each other) and its fixes?
**Say this in the interview:** "With 100,000 points, solid dots become one blob. I make the dots small and see-through with s and alpha, or I switch to a hexbin or 2D histogram that counts points per cell, or I plot a random sample."
**Explain simply:**
- Overplotting hides density: 10 points and 10,000 points on the same spot look identical.
- `alpha=0.05` makes each dot nearly transparent, so crowded areas look darker; `s=2` shrinks them.
- `hexbin` counts points in hexagons and colours by count; fast even for millions of rows.
- A random sample (`df.sample(5000)`) is acceptable for exploring, but say you sampled.
**Sample data:** 100,000 simulated employees (random numbers with a fixed seed, only to create volume).
**Code (what you write in the interview):**
```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(1)
tenure = rng.normal(5, 2, 100000)
salary = tenure * 5 + rng.normal(30, 8, 100000)

# small, see-through dots: dense areas look darker
plt.scatter(tenure, salary, s=2, alpha=0.05)
plt.xlabel("Tenure (years)")
plt.ylabel("Salary (thousands)")
plt.show()

# alternative: count points per hexagon
plt.hexbin(tenure, salary, gridsize=40, cmap="Blues")
plt.colorbar(label="Employees")
plt.show()
```
**Output:** (chart only, no printed output). The first chart shows a dense diagonal band, darker in the middle; the second shows the same pattern as blue hexagons with a colourbar of employee counts.
**What it means:** The relationship (more tenure, more salary) is visible and the dense core is clear.
**Alternative:** `sns.kdeplot(x=tenure, y=salary, fill=True)` or `plt.hist2d`.
**Likely follow-ups:**
- *Why not just sample?* Fine for exploring; show the full data for final reports.
- *Plot is slow?* Aggregate first (hexbin, bins) instead of drawing every point.
**Common mistakes:** Leaving default big opaque dots; not mentioning that a sample was used; forgetting the colourbar on hexbin.

### Q45 ⭐ 🟡 How do you choose colours that work for colour-blind readers and for a company colour theme?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you design for accessibility and brand consistency, not just default colours?
**Say this in the interview:** "I use a colour-blind-safe palette like seaborn's colorblind, avoid red-green pairs, and add a second cue such as labels or markers. For the company theme I set the hex codes myself in a dictionary so every chart uses the same colours."
**Explain simply:**
- About 1 in 12 men is red-green colour-blind, so red vs green alone is not readable.
- `sns.color_palette("colorblind")` gives tested colours (blue, orange, green, vermillion). Viridis is a good continuous option.
- Company colours: put hex codes in a dictionary keyed by category so Sales is always the same colour across all charts.
- Do not rely on colour alone: label bars directly, or use different markers or line styles. Also check the chart in greyscale.
**Sample data:** Three departments with company hex colours.
**Code (what you write in the interview):**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# a palette built to stay distinguishable for colour-blind readers
print(sns.color_palette("colorblind").as_hex()[:4])

# company colours: set them yourself, one per category
company_colours = {"Sales": "#1F4E79", "IT": "#E69F00", "HR": "#009E73"}

departments = list(company_colours)
attrition = [18, 10, 6]
plt.bar(departments, attrition, color=list(company_colours.values()))
plt.ylabel("Attrition %")
plt.show()
```
**Output:**
```
['#0173b2', '#de8f05', '#029e73', '#d55e00']
```
**What it means:** The printed list shows the safe palette's first four colours; the bar chart uses the company's own colours.
**Alternative:** `sns.set_palette("colorblind")` once at the top applies the palette to all later charts.
**Likely follow-ups:**
- *Which colours to avoid together?* Red and green, and green and brown.
- *Brand colours not colour-blind safe?* Keep the brand but add labels or patterns.
**Common mistakes:** Using red for bad and green for good only; too many colours (keep to 5 or 6 categories); changing a department's colour between charts.

### Q46 ⭐ 🟡 How do you generate and save one chart per department in a loop for a monthly report?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you automate a repeatable report without memory or file mistakes?
**Say this in the interview:** "I group the data by department, and in a for loop I draw one chart, save it with the department name in the file name, and close the figure so memory does not fill up."
**Explain simply:**
- `groupby("department")` in a loop gives the department name and its own small table each time.
- Create a fresh figure for each department (`plt.subplots()`), so charts do not draw on top of each other.
- `savefig` writes the image; `dpi=150` keeps it sharp; `bbox_inches="tight"` stops labels being cut off.
- `plt.close(fig)` releases the figure; skipping it gives a warning after 20 open figures and wastes memory.
**Sample data:** Three months of hires for two departments.
**Code (what you write in the interview):**
```python
import os
import pandas as pd
import matplotlib.pyplot as plt

hiring = pd.DataFrame({
    "department": ["Sales", "Sales", "Sales", "IT", "IT", "IT"],
    "month": ["Jan", "Feb", "Mar", "Jan", "Feb", "Mar"],
    "hires": [5, 8, 6, 3, 2, 4],
})

os.makedirs("charts", exist_ok=True)

for department, department_data in hiring.groupby("department"):
    fig, ax = plt.subplots()
    ax.plot(department_data["month"], department_data["hires"], marker="o")
    ax.set_title(f"Hires per month: {department}")
    fig.savefig(f"charts/{department}_hires.png", dpi=150, bbox_inches="tight")
    plt.close(fig)  # frees memory; otherwise figures pile up

print(sorted(os.listdir("charts")))
```
**Output:**
```
['IT_hires.png', 'Sales_hires.png']
```
**What it means:** One image file per department, ready to paste into the monthly pack.
**Alternative:** Put all departments in one picture with `sns.relplot(..., col="department")` and save once.
**Likely follow-ups:**
- *Department names with spaces or slashes?* Clean the name before using it in a file name.
- *Run monthly?* Wrap in a function and pass the month.
**Common mistakes:** Not closing figures; drawing all departments on the same axes by creating the figure outside the loop.

### Q47 ⭐ 🟡 When would you use Plotly instead of matplotlib or seaborn?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know when interactivity is worth it?
**Say this in the interview:** "I use Plotly when the reader needs to interact: hover to see exact numbers, zoom, filter, or open it in a browser or a Dash dashboard. For a static slide or PDF I stay with matplotlib or seaborn."
**Explain simply:**
- Plotly charts are interactive HTML: hover tooltips, zoom, click legend items to hide a series.
- `plotly.express` makes a chart in one line from a DataFrame. Plotly is a separate package (`pip install plotly`).
- Good for dashboards (Dash, Streamlit), emailed HTML reports, exploring data with many categories.
- Matplotlib or seaborn is better for printed or static slides, tight control of every detail, and quick analyst work without extra installs.
**Sample data:** Four departments with attrition rates.
**Code (what you write in the interview):**
```python
import pandas as pd
import plotly.express as px

attrition = pd.DataFrame({
    "department": ["Sales", "IT", "HR", "Finance"],
    "attrition_rate": [18, 10, 6, 8],
})

figure = px.bar(attrition, x="department", y="attrition_rate", title="Attrition % by department")
figure.write_html("attrition.html")  # interactive: hover, zoom, share by email
```
**Output:** (no printed output; the chart is saved to attrition.html). The code ran and wrote `attrition.html` (interactive bar chart); not opened in a browser here.
**What it means:** The manager can hover over a bar to read the exact rate.
**Alternative:** `figure.show()` opens it in the browser or notebook instead of saving.
**Likely follow-ups:**
- *Can Plotly save a PNG?* Yes, with the extra `kaleido` package.
- *Matplotlib or Plotly for a PDF report?* Matplotlib.
**Common mistakes:** Using interactive charts in a printed report; forgetting that the HTML file needs a browser, not a slide.

### Q48 ⭐ 🔴 How would you visualise attrition by department and tenure band in a single chart?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you show two category dimensions and one measure clearly, and pick the right chart?
**Say this in the interview:** "Two categories and one rate fit a heatmap well: departments as rows, tenure bands as columns, colour and number showing attrition percent. A grouped bar chart is the alternative if there are only a few departments."
**Explain simply:**
- Make tenure bands with `pd.cut` (0-1, 1-3, 3+ years); bands are the 'buckets' of a continuous number.
- If `left` is 1 for leavers and 0 for stayers, the mean of `left` is the attrition rate, so `pivot_table(..., aggfunc="mean")` gives it.
- Heatmap: easy to spot the hottest cell. Grouped bars (`sns.barplot(hue="tenure_band")`): easier to read exact heights.
- Always check the group size: a 100% in a cell with 1 or 2 people means little.
**Sample data:** 16 employees: department, tenure in years, left (1 = left).
**Code (what you write in the interview):**
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

employees = pd.DataFrame({
    "department": ["Sales"] * 6 + ["IT"] * 6 + ["HR"] * 4,
    "tenure_years": [0.5, 1, 2, 4, 6, 9, 0.8, 1.5, 3, 5, 7, 10, 0.7, 2, 4, 8],
    "left": [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],  # 1 = left
})

# group tenure into bands
employees["tenure_band"] = pd.cut(employees["tenure_years"], bins=[0, 1, 3, 100],
                                  labels=["0-1 yr", "1-3 yrs", "3+ yrs"])

# average of 1/0 "left" = attrition rate; rows are departments, columns are bands
attrition_table = employees.pivot_table(index="department", columns="tenure_band",
                                        values="left", aggfunc="mean", observed=True) * 100
print(attrition_table.round(0))

sns.heatmap(attrition_table, annot=True, fmt=".0f", cmap="Reds")
plt.title("Attrition % by department and tenure band")
plt.show()
```
**Output:**
```
tenure_band  0-1 yr  1-3 yrs  3+ yrs
department                          
HR              0.0      0.0    50.0
IT            100.0      0.0    33.0
Sales         100.0    100.0     0.0
```
**What it means:** New joiners in Sales and IT leave the most; long-tenure Sales staff stay. These cells hold only 1 to 3 people, so the numbers are not reliable; with real data check each cell's size.
**Alternative:** `sns.barplot(data=employees, x="department", y="left", hue="tenure_band")` (bar height is the mean of `left`).
**Likely follow-ups:**
- *Why not a stacked bar?* Hard to compare the middle segments.
- *Cells too small?* Merge bands or show the headcount in each cell.
**Common mistakes:** Averaging department rates instead of using the 1/0 flag; unequal bands; forgetting `observed=True` (otherwise pandas warns about empty categories).

### Q49 ⭐ 🔴 Write code to build a one-page summary figure for a hiring funnel: funnel bars, a monthly trend and a source-wise split.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you organise several charts on one page cleanly and save it?
**Say this in the interview:** "I make one figure with three panels using plt.subplots(1, 3). The first panel is the funnel as horizontal bars, the second is hires per month as a line, the third is hires by source as bars. Then tight_layout, a title and savefig."
**Explain simply:**
- A funnel is horizontal bars in stage order, biggest on top; `invert_yaxis()` puts the first stage at the top.
- `plt.subplots(1, 3)` returns the figure and three axes; unpack them into named variables so each chart is easy to follow.
- Use a line for a trend over time, bars for comparing categories.
- Give each panel a clear title and keep the same style across panels.
**Sample data:** Three small Series: funnel counts, hires per month, hires by source.
**Code (what you write in the interview):**
```python
import pandas as pd
import matplotlib.pyplot as plt

funnel = pd.Series({"Applied": 500, "Screened": 300, "Interviewed": 120, "Offered": 40, "Joined": 30})
monthly_hires = pd.Series({"Jan": 8, "Feb": 11, "Mar": 9, "Apr": 14, "May": 12, "Jun": 15})
hires_by_source = pd.Series({"Referral": 40, "Job portal": 35, "Agency": 15, "Campus": 10})

fig, (funnel_ax, trend_ax, source_ax) = plt.subplots(1, 3, figsize=(14, 4))

funnel_ax.barh(funnel.index, funnel.values)
funnel_ax.invert_yaxis()  # first stage on top
funnel_ax.set_title("Hiring funnel")

trend_ax.plot(monthly_hires.index, monthly_hires.values, marker="o")
trend_ax.set_title("Hires per month")

source_ax.bar(hires_by_source.index, hires_by_source.values)
source_ax.set_title("Hires by source")
source_ax.tick_params(axis="x", rotation=20)

fig.suptitle("Hiring summary, H1")
fig.tight_layout()
fig.savefig("hiring_summary.png", dpi=150)
plt.show()
```
**Output:** (chart only, no printed output). Saved as hiring_summary.png. Left: bars shrinking from 500 applied to 30 joined. Middle: hires rising from 8 in January to 15 in June. Right: Referral biggest with 40, then Job portal 35.
**What it means:** One page answers three questions: where do candidates drop off, is hiring improving, and which source works.
**Alternative:** `plt.subplot_mosaic` or GridSpec for uneven layouts, for example one wide trend chart on top.
**Likely follow-ups:**
- *Add conversion percentages?* Divide each stage by the previous with `funnel / funnel.shift()`.
- *Different scales on panels?* Fine, each panel has its own axis.
**Common mistakes:** Creating separate figures instead of one; forgetting `invert_yaxis` so the funnel is upside down; calling `savefig` after `plt.show()` (the saved image can be blank), which is why savefig comes first.

### Q50 ⭐ 🔴 How do you remove clutter from a default matplotlib chart (spines, gridlines, legend position) so it is ready for a manager's slide?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you think about the audience: remove noise, keep the message?
**Say this in the interview:** "I remove the top and right borders, turn off the gridlines, put the legend outside the data, write the title as the message, and save at high resolution with a tight bounding box."
**Explain simply:**
- Chart junk is anything that does not help the reader: extra borders (spines), heavy gridlines, a legend sitting on the data.
- `ax.spines[["top", "right"]].set_visible(False)` removes two borders; `ax.grid(False)` removes gridlines.
- `legend(frameon=False, bbox_to_anchor=(1, 1))` moves the legend beside the chart, or label the lines directly.
- Make the title state the takeaway ("Sales hiring is rising while IT is flat"), and save with `dpi=200` and `bbox_inches="tight"` so nothing is cut off.
**Sample data:** Two departments, five months of hires.
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May"]
sales = [8, 9, 7, 10, 12]
it = [5, 6, 6, 7, 6]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(months, sales, marker="o", label="Sales")
ax.plot(months, it, marker="o", label="IT")

# remove the box lines that add no information
ax.spines[["top", "right"]].set_visible(False)

# no gridlines, a clear title that states the message
ax.grid(False)
ax.set_title("Sales hiring is rising while IT is flat", loc="left")
ax.set_ylabel("Hires")

# legend outside the data
ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(1, 1))

fig.savefig("hires_slide.png", dpi=200, bbox_inches="tight")
plt.show()
```
**Output:** (chart only, no printed output). Saved as hires_slide.png: a clean two-line chart with only left and bottom axes, a message title and the legend on the right.
**What it means:** The reader sees the story at once, with nothing extra to ignore.
**Alternative:** `plt.style.use("seaborn-v0_8-whitegrid")` or `sns.despine()` for a quick clean-up.
**Likely follow-ups:**
- *Why legend outside?* It cannot hide data points.
- *Gridlines never?* Light gridlines help when readers must read exact values.
**Common mistakes:** Saving without `bbox_inches="tight"` so the outside legend is cut; tiny fonts for slides; keeping a default title like 'Figure 1'.

# Book 5 — Statistics & Maths for Data Analysts | Part 2: Descriptive Statistics 🟢

**Target:** 60 questions | **Actual:** 60 questions
**Scope:** mean/median/mode, variance, standard deviation, percentiles, quartiles, IQR, outliers and describing data in plain business terms.

### Q1 ⭐⭐⭐ 🟢 What are mean, median and mode, and how do you calculate each?
**Asked at:** commonly asked (no company-specific report found); appears in every statistics interview guide we found (upGrad, 365 Data Science, Exponent).
**What the interviewer is checking:** Whether you know the three "typical value" measures and can calculate each without a tool.
**Say this in the interview:** "Mean is the sum divided by the count. Median is the middle value after sorting. Mode is the most frequent value. Together they describe the centre of the data, and I compare them to see if a few extreme values are pulling the mean."
**Explain simply:**
- **Mean (average):** add everything up, divide by how many values there are.
- **Median:** sort the values and take the middle one; with an even count, average the two middle ones.
- **Mode:** the value that appears most often; useful for categories too (most common job grade).
- These three are called measures of central tendency, meaning "where the middle of the data sits".
**Formula in plain words:** mean = total of all values divided by number of values; in symbols, x̄ = Σx / n.
**Worked example:** Monthly salaries (Rs thousand) of 7 people: 30, 32, 35, 35, 38, 40, 90. Sum = 300, so mean = 300 / 7 = 42.86. Sorted, the 4th value is 35, so median = 35. The value 35 appears twice, so mode = 35. The mean is higher because of the 90.
**Excel / Python:**
```python
import statistics

# Monthly salaries in Rs thousand for 7 employees
monthly_salaries = [30, 32, 35, 35, 38, 40, 90]

# Mean: total divided by count
print("Mean:", round(statistics.mean(monthly_salaries), 2))

# Median: middle value after sorting
print("Median:", statistics.median(monthly_salaries))

# Mode: most frequent value
print("Mode:", statistics.mode(monthly_salaries))
```
Output:
```
Mean: 42.86
Median: 35
Mode: 35
```
The mean (42.86) sits above the median (35) because one high salary drags it up.
Excel (not run in Excel here): put the salaries in A2:A8, then `=AVERAGE(A2:A8)` returns 42.86, `=MEDIAN(A2:A8)` returns 35, `=MODE.SNGL(A2:A8)` returns 35 (MODE.SNGL needs Excel 2010 or later).
**Likely follow-ups:** 1) *Which is best?* Depends on shape; see Q2. 2) *Can there be two modes?* Yes (Q22).
**Common mistakes:** Forgetting to sort before picking the median; calling the mode "the highest value" instead of "the most frequent value".

### Q2 ⭐⭐⭐ 🟢 When would you use the median instead of the mean? Give an example with salaries.
**Asked at:** commonly asked (no company-specific report found); a mean-vs-median scenario question appears on practice platforms such as Dataford.
**What the interviewer is checking:** Whether you understand that extreme values distort the mean.
**Say this in the interview:** "I use the median when the data is skewed or has extreme values, like salaries. A few very high pay packages pull the mean up, while the median still shows what a typical person earns."
**Explain simply:**
- The mean uses every value, so one huge value moves it a lot.
- The median only cares about the middle position, so extremes barely change it.
- Salary, house prices and response times are classic "median" columns because they have long tails of large values.
- If the data is roughly symmetric with no extremes, mean and median are close and either is fine.
**Worked example:** Eight employees, monthly salary in Rs thousand: 30, 32, 34, 35, 36, 38, 40, 300 (the last is a founder). Mean = 545 / 8 = 68.1, yet 7 of 8 people earn 40 or less. Median = (35 + 36) / 2 = 35.5, which describes the typical person.
**Excel / Python:**
```python
import pandas as pd

# Monthly salaries in Rs thousand; the last one is a founder
salaries = pd.Series([30, 32, 34, 35, 36, 38, 40, 300])

# Average, pulled up by the founder
print("Mean:", salaries.mean())

# Middle value, not affected by the founder
print("Median:", salaries.median())
```
Output:
```
Mean: 68.125
Median: 35.5
```
Reporting 68 as "average salary" would mislead; 35.5 is the honest typical figure.
**Likely follow-ups:** 1) *Would you ever prefer the mean?* Yes, for totals and budgets, since mean x count gives the total payroll. 2) *Why is the median robust?* See Q31.
**Common mistakes:** Reporting only the mean for salary data; saying the median is "always better".

### Q3 ⭐⭐⭐ 🟢 What is standard deviation, and what does it tell you about a dataset?
**Asked at:** commonly asked (no company-specific report found); standard deviation and variance recur in 365 Data Science and upGrad lists.
**What the interviewer is checking:** Whether you understand spread, not just the formula.
**Say this in the interview:** "Standard deviation measures how far values typically sit from the average. Small means values are tightly clustered, large means they are spread out. It is in the same units as the data, so it is easy to interpret."
**Explain simply:**
- Two groups can have the same average but very different consistency; the average alone hides this.
- Standard deviation (SD) is roughly "the typical distance of a value from the mean".
- Low SD means predictable (steady attendance); high SD means volatile.
- For bell-shaped data, about 68% of values fall within one SD of the mean.
**Formula in plain words:** find each value's gap from the mean, square the gaps, average them (dividing by n-1 for a sample), then take the square root. Symbols: s = √( Σ(x - x̄)² / (n-1) ).
**Worked example:** Days present per week-block for two teams (5 values each). Team A: 8, 9, 10, 11, 12; Team B: 10, 10, 10, 10, 10. Both average 10 days, but Team A varies while Team B never does.
**Excel / Python:**
```python
import statistics

# Days present in five periods for each team
team_a_days = [8, 9, 10, 11, 12]
team_b_days = [10, 10, 10, 10, 10]

# Mean and sample standard deviation of each team
print("Team A mean:", statistics.mean(team_a_days), "SD:", round(statistics.stdev(team_a_days), 2))
print("Team B mean:", statistics.mean(team_b_days), "SD:", statistics.stdev(team_b_days))
```
Output:
```
Team A mean: 10 SD: 1.58
Team B mean: 10 SD: 0.0
```
Same average, but Team A swings by about 1.6 days either way while Team B is perfectly steady. Excel: `=STDEV.S(A2:A6)` (Excel 2010+; not run in Excel here).
**Likely follow-ups:** 1) *Can SD be negative?* No, it is a square root, so 0 or more. 2) *Why n-1?* See Q12.
**Common mistakes:** Comparing SDs of columns with different units or scales (use Q26); treating SD as "the maximum deviation".

### Q4 ⭐⭐⭐ 🟢 What is the difference between variance and standard deviation, and why do we usually report standard deviation?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know SD is just the square root of variance and why units matter.
**Say this in the interview:** "Variance is the average squared distance from the mean; standard deviation is its square root. I report SD because it is in the original units, so a salary SD is in rupees, not rupees squared."
**Explain simply:**
- Squaring the gaps stops positives and negatives cancelling out, but it also squares the units.
- Variance of salaries in Rs would be in "Rs squared", which nobody can picture.
- Taking the square root brings it back to Rs.
- Variance is still useful in maths because variances add up neatly (Q53).
**Formula in plain words:** variance = average of squared gaps from the mean (n-1 for a sample); SD = square root of variance.
**Worked example:** Salaries (Rs thousand): 30, 32, 35, 35, 38, 40. Mean = 35. Squared gaps: 25, 9, 0, 0, 9, 25 (sum 68). Sample variance = 68 / 5 = 13.6 (Rs thousand squared). SD = √13.6 = 3.69 Rs thousand.
**Excel / Python:**
```python
import statistics

# Salaries in Rs thousand
salaries = [30, 32, 35, 35, 38, 40]

# Mean and the squared gap of each salary from it
mean_salary = statistics.mean(salaries)
squared_gaps = [(s - mean_salary) ** 2 for s in salaries]
print("Mean:", mean_salary)
print("Squared gaps:", squared_gaps)

# Sample variance and its square root
variance = statistics.variance(salaries)
std_dev = statistics.stdev(salaries)
print("Variance:", variance)
print("Standard deviation:", round(std_dev, 2))
```
Output:
```
Mean: 35
Squared gaps: [25, 9, 0, 0, 9, 25]
Variance: 13.6
Standard deviation: 3.69
```
Excel (2010+; not run in Excel here): `=VAR.S(A2:A7)` returns 13.6, `=STDEV.S(A2:A7)` returns 3.69.
**Likely follow-ups:** 1) *Which is more sensitive to outliers?* Both, variance even more. 2) *When is variance preferred?* When combining independent sources of variation.
**Common mistakes:** Quoting variance to a manager; forgetting variance units are squared.

### Q5 ⭐⭐⭐ 🟢 What is the difference between descriptive and inferential statistics?
**Asked at:** commonly asked (no company-specific report found); listed in upGrad's 2025 statistics question set.
**What the interviewer is checking:** Whether you separate "summarising what we have" from "drawing conclusions about what we do not have".
**Say this in the interview:** "Descriptive statistics summarise the data I actually have, like the average salary of my 500 employees. Inferential statistics use a sample to draw conclusions about a bigger group, with some uncertainty, like estimating company-wide engagement from a 50-person survey."
**Explain simply:**
- Descriptive: mean, median, SD, charts, tables. No guessing involved.
- Inferential: confidence intervals, hypothesis tests, predictions. Always carries uncertainty.
- This Part covers descriptive; the later parts cover inferential.
**Worked example:** A company has 2,000 employees. HR surveys a random 50. Saying "these 50 averaged 69.18" is descriptive. Saying "so the whole company probably averages around 69, give or take a few points" is inferential.
**Excel / Python:**
```python
import numpy as np

# Simulated engagement scores for all 2,000 employees (normally unknown)
rng = np.random.default_rng(7)
all_scores = np.round(rng.normal(70, 10, 2000), 1)

# A random sample of 50 employees is what HR actually surveys
sample_scores = rng.choice(all_scores, size=50, replace=False)

# Descriptive: summarise the sample we have
print("Sample mean:", round(sample_scores.mean(), 2))

# In real life we never see this; here we peek to check the inference
print("True company mean:", round(all_scores.mean(), 2))
```
Output:
```
Sample mean: 69.18
True company mean: 69.6
```
The sample mean is close to, but not exactly, the company mean; inference is about handling that gap sensibly.
**Likely follow-ups:** 1) *Give an inferential example.* A hypothesis test on whether attrition differs between two branches. 2) *Is a chart descriptive?* Yes.
**Common mistakes:** Calling any use of an average "inferential"; presenting sample results as certain facts about the population.

### Q6 ⭐⭐⭐ 🟢 What is an outlier, and how does it affect the mean, median and standard deviation?
**Asked at:** commonly asked; Glassdoor snippets show "what are outliers and how to identify them" in junior data analyst interviews (title seen only).
**What the interviewer is checking:** Whether you know which statistics are fragile.
**Say this in the interview:** "An outlier is a value far from the rest. It can pull the mean a lot and blow up the standard deviation, but the median barely moves."
**Explain simply:**
- An outlier may be a real extreme (a CEO's salary) or an error (an extra zero typed in).
- Mean: pulled toward the outlier.
- Standard deviation: inflated, because gaps are squared.
- Median: moves by at most one position, so it is robust.
**Worked example:** Salaries (Rs thousand) 30, 32, 34, 35, 36, 38, 40. Add one founder at 300 and see what changes.
**Excel / Python:**
```python
import statistics

# Salaries without and with an outlier (Rs thousand)
without_outlier = [30, 32, 34, 35, 36, 38, 40]
with_outlier = without_outlier + [300]

# Compare the three statistics for each version
for label, data in [("Without outlier", without_outlier), ("With outlier", with_outlier)]:
    print(label, "mean:", round(statistics.mean(data), 2),
          "median:", statistics.median(data),
          "SD:", round(statistics.stdev(data), 2))
```
Output:
```
Without outlier mean: 35 median: 35 SD: 3.42
With outlier mean: 68.12 median: 35.5 SD: 93.74
```
One person doubled the mean and multiplied the SD by about 27, while the median moved by 0.5.
**Likely follow-ups:** 1) *How do you detect outliers?* IQR rule (Q10) or z-score (Q30). 2) *Do you always remove them?* No (Q16).
**Common mistakes:** Deleting outliers automatically; forgetting that SD is also hurt, not only the mean.

### Q7 ⭐⭐⭐ 🟢 What is a percentile? What does it mean if your salary is at the 90th percentile?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can explain position in a ranking.
**Say this in the interview:** "The p-th percentile is the value below which p percent of the data falls. At the 90th percentile, about 90% of people earn the same or less and about 10% earn more."
**Explain simply:**
- Percentiles split sorted data into 100 slices.
- It tells you rank, not the amount itself: the 90th percentile of salary is a rupee figure, and "being at the 90th percentile" means you are near the top.
- The 50th percentile is the median.
**Worked example:** 20 salaries (Rs thousand). The 90th percentile works out to 123, and 18 of the 20 people (90%) earn 123 or less.
**Excel / Python:**
```python
import numpy as np

# 20 monthly salaries in Rs thousand
salaries = [25, 28, 30, 32, 35, 38, 40, 45, 50, 55, 60, 65, 70, 75, 80, 90, 100, 120, 150, 200]

# The salary value at the 90th percentile
p90 = np.percentile(salaries, 90)

# What share of people earn at or below that value
count_at_or_below = sum(1 for s in salaries if s <= p90)
print("90th percentile value:", round(p90, 1))
print("Share at or below it:", count_at_or_below / len(salaries))
```
Output:
```
90th percentile value: 123.0
Share at or below it: 0.9
```
Excel (not run in Excel here): `=PERCENTILE.INC(A2:A21, 0.9)` (2010+) uses the same interpolation and gives 123.
**Likely follow-ups:** 1) *Percentile vs percentage?* A percentage is a share of a total; a percentile is a rank position. 2) *Tools differ slightly?* Yes (Q42).
**Common mistakes:** Saying "90th percentile means I scored 90%"; mixing percentile value and percentile rank (Q28).

### Q8 ⭐⭐⭐ 🟢 Calculate the mean, median and mode of this data: 4, 8, 6, 5, 3, 8, 9.
**Asked at:** commonly asked (no company-specific report found); a standard warm-up calculation.
**What the interviewer is checking:** Basic arithmetic discipline, especially sorting before the median.
**Say this in the interview:** "Sum is 43 over 7 values, so mean is about 6.14. Sorted: 3, 4, 5, 6, 8, 8, 9, so the median is 6. The value 8 appears twice, so the mode is 8."
**Explain simply:**
- Step 1: add: 4+8+6+5+3+8+9 = 43.
- Step 2: divide by 7 values: 6.14.
- Step 3: sort, then take the 4th of 7 values: 6.
- Step 4: count repeats: 8 appears twice, everything else once.
**Formula in plain words:** mean = 43 / 7; median = value at position (n+1)/2 = 4th.
**Worked example:** As above; note the three answers differ (6.14, 6, 8), which hints the data is slightly uneven.
**Excel / Python:**
```python
import statistics

data = [4, 8, 6, 5, 3, 8, 9]

# Sort first; the median needs ordered values
print("Sorted:", sorted(data))
print("Sum:", sum(data), "Count:", len(data))
print("Mean:", round(sum(data) / len(data), 2))
print("Median:", statistics.median(data))
print("Mode:", statistics.mode(data))
```
Output:
```
Sorted: [3, 4, 5, 6, 8, 8, 9]
Sum: 43 Count: 7
Mean: 6.14
Median: 6
Mode: 8
```
Excel: values in A2:A8; `=AVERAGE(A2:A8)`, `=MEDIAN(A2:A8)`, `=MODE.SNGL(A2:A8)` (not run in Excel here).
**Likely follow-ups:** 1) *What if we add a 10?* Mean 6.63, median 7 (8 values, middle two 6 and 8). 2) *Which would you report?* Mean or median; no outliers here.
**Common mistakes:** Taking the middle of the unsorted list (which would give 5); rounding the mean too early.

### Q9 ⭐⭐⭐ 🟢 The average salary in a team of 5 is Rs 6 lakh, but four people earn Rs 4 lakh each. What does that tell you, and which average would you report?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured version of the mean-vs-median question.
**What the interviewer is checking:** Whether you can reverse-engineer a mean and spot skew.
**Say this in the interview:** "A mean of 6 lakh over 5 people means total pay of 30 lakh. Four people take 16 lakh, so the fifth earns 14 lakh. The mean is pulled up by one person; the median of 4 lakh describes the team better, so I would report the median and mention the mean."
**Explain simply:**
- Total = mean x count = 6 x 5 = 30 lakh.
- Four people at 4 lakh = 16 lakh, leaving 14 lakh for the fifth.
- The "average" of 6 lakh is a figure that nobody in the team actually earns.
- Median = 4 lakh, which matches what 80% of the team earns.
**Worked example:** Salaries: 4, 4, 4, 4, 14 (Rs lakh). Mean = 6, median = 4, mode = 4.
**Excel / Python:**
```python
import statistics

# Total pay implied by the average, then the missing fifth salary
team_total = 6 * 5
fifth_person = team_total - 4 * 4
print("Total:", team_total, "Fifth person:", fifth_person)

# Median of the five salaries
print("Median:", statistics.median([4, 4, 4, 4, fifth_person]))
```
Output:
```
Total: 30 Fifth person: 14
Median: 4
```
The fifth person earns 14 lakh, and the typical salary is 4 lakh.
**Likely follow-ups:** 1) *Would you ever quote the mean?* Yes, for budget totals. 2) *Is the data skewed?* Yes, to the right (Q24).
**Common mistakes:** Saying "most of the team earns about 6 lakh"; not checking whether the numbers fit (the fifth salary must be 14).

### Q10 ⭐⭐⭐ 🟡 What is the IQR, and how do you use it to detect outliers?
**Asked at:** a Glassdoor candidate report (snippet seen only) describes being asked to write a Python function that detects outliers using the IQR method and explain the logic; IQR also appears in analytics interview question searches.
**What the interviewer is checking:** Whether you can state the rule and apply it.
**Say this in the interview:** "IQR is Q3 minus Q1, the spread of the middle 50% of data. I flag a value as an outlier if it is below Q1 minus 1.5 times IQR or above Q3 plus 1.5 times IQR."
**Explain simply:**
- Q1 (25th percentile) and Q3 (75th percentile) are the quartiles (Q11).
- IQR ignores the top and bottom 25%, so extremes cannot distort it.
- The 1.5 multiplier gives "fences"; values outside are flagged for review, not automatically deleted.
**Formula in plain words:** IQR = Q3 minus Q1. Lower fence = Q1 minus 1.5 x IQR; upper fence = Q3 plus 1.5 x IQR.
**Worked example:** Salaries (Rs thousand): 28, 30, 32, 33, 35, 36, 38, 40, 42, 95. Q1 = 32.25, Q3 = 39.5, IQR = 7.25. Fences: 21.375 and 50.375. Only 95 lies outside.
**Excel / Python:**
```python
import numpy as np

# Salaries in Rs thousand
data = [28, 30, 32, 33, 35, 36, 38, 40, 42, 95]

# Quartiles and the IQR
q1 = np.percentile(data, 25)
q3 = np.percentile(data, 75)
iqr = q3 - q1

# Fences: anything outside is flagged
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr
outliers = [v for v in data if v < lower_fence or v > upper_fence]

print("Q1:", q1, "Q3:", q3, "IQR:", iqr)
print("Fences:", lower_fence, upper_fence)
print("Outliers:", outliers)
```
Output:
```
Q1: 32.25 Q3: 39.5 IQR: 7.25
Fences: 21.375 50.375
Outliers: [95]
```
Excel (not run in Excel here): `=QUARTILE.INC(A2:A11,1)` gives 32.25 and `=QUARTILE.INC(A2:A11,3)` gives 39.5, matching Python's default method (2010+).
**Likely follow-ups:** 1) *Why 1.5?* See Q49. 2) *What if the data is not symmetric?* The rule still works but may flag many on the long tail side.
**Common mistakes:** Using IQR = max minus min; deleting flagged points without checking whether they are real.

### Q11 ⭐⭐⭐ 🟡 What are quartiles, and how do you read a box plot?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can read distribution shape from a standard chart.
**Say this in the interview:** "Quartiles split sorted data into four equal parts: Q1 at 25%, Q2 (the median) at 50%, Q3 at 75%. A box plot draws a box from Q1 to Q3 with a line at the median, whiskers to the furthest non-outlier values, and dots for outliers."
**Explain simply:**
- The box holds the middle 50% of the data; its width is the IQR.
- A median line off-centre in the box, or one long whisker, signals skew.
- Dots beyond the whiskers are the points outside the 1.5 x IQR fences.
- Box plots let you compare several groups side by side (attrition by department).
**Worked example:** Using the 10 salaries from Q10: Q1 = 32.25, median = 35.5, Q3 = 39.5; the box spans 32.25 to 39.5, the upper whisker stops at 42 (the largest value inside the fence), and 95 appears as a dot.
**Excel / Python:**
```python
import numpy as np

# Same ten salaries as Q10
data = [28, 30, 32, 33, 35, 36, 38, 40, 42, 95]

# The three quartile cut points
q1, median, q3 = np.percentile(data, [25, 50, 75])
print("Q1:", q1, "Median:", median, "Q3:", q3)
```
Output:
```
Q1: 32.25 Median: 35.5 Q3: 39.5
```
Plot it with `seaborn.boxplot` or Excel's Insert > Box and Whisker chart (2016+; not run in Excel here).
**Likely follow-ups:** 1) *What does a long upper whisker mean?* Right skew. 2) *Does a box plot show the mean?* Not by default.
**Common mistakes:** Thinking whiskers always reach min and max; reading box length as the whole range.

### Q12 ⭐⭐⭐ 🟡 Why does the sample standard deviation divide by n-1 instead of n?
**Asked at:** commonly asked; sample vs population variance is a recurring item in 365 Data Science and upGrad lists.
**What the interviewer is checking:** Whether you know the intuition, not just the rule.
**Say this in the interview:** "A sample's values sit closer to the sample's own mean than to the true population mean, so dividing by n underestimates the spread. Dividing by n-1 corrects that on average; it is called Bessel's correction."
**Explain simply:**
- We do not know the true population mean, so we use the sample mean, which is by construction the point closest to the sample values.
- That makes the squared gaps too small on average.
- Using n-1 (the "degrees of freedom": once the mean is fixed, only n-1 values are free to vary) fixes the shortfall.
- For large n the difference is tiny; for small samples it matters.
**Formula in plain words:** sample variance = sum of squared gaps divided by (n minus 1).
**Worked example:** I drew many random groups of 5 from a population with true variance 99.3 and averaged the two versions.
**Excel / Python:**
```python
import numpy as np

# A large population with a known spread
rng = np.random.default_rng(1)
whole_group = rng.normal(50, 10, 100000)
print("True variance:", round(whole_group.var(), 1))

# Repeatedly draw 5 values and compute variance both ways
divide_by_n = []
divide_by_n_minus_1 = []
for _ in range(20000):
    small_sample = rng.choice(whole_group, size=5)
    divide_by_n.append(small_sample.var(ddof=0))
    divide_by_n_minus_1.append(small_sample.var(ddof=1))

# Compare the averages of each method
print("Average with n:", round(np.mean(divide_by_n), 1))
print("Average with n-1:", round(np.mean(divide_by_n_minus_1), 1))
```
Output:
```
True variance: 99.3
Average with n: 79.8
Average with n-1: 99.7
```
Dividing by n lands near 80% (4/5) of the truth; n-1 lands on it.
**Likely follow-ups:** 1) *Which does Excel use?* `STDEV.S` uses n-1, `STDEV.P` uses n. 2) *Is the SD itself then unbiased?* Not exactly (Q55).
**Common mistakes:** Saying "to make the number bigger" without the reason; using n-1 on a full population.

### Q13 ⭐⭐⭐ 🟡 What is the difference between population and sample, and between a parameter and a statistic?
**Asked at:** commonly asked (no company-specific report found); 365 Data Science notes sampling focus for entry-level roles.
**What the interviewer is checking:** Core vocabulary of statistics.
**Say this in the interview:** "The population is everyone I care about; a sample is the part I actually measure. A number describing the population is a parameter; the same number computed from a sample is a statistic, used to estimate the parameter."
**Explain simply:**
- Population: all 2,000 employees. Sample: the 50 who answered the survey.
- Parameter: true company average engagement (usually unknown). Statistic: the survey average.
- Symbols: population mean is μ, sample mean is x̄; population SD is σ, sample SD is s.
- A good sample is random and representative; a biased sample gives a misleading statistic.
**Worked example:** Population mean (parameter) of simulated engagement scores = 69.6; the mean of a random sample of 50 (statistic) = 69.18. The statistic estimates the parameter with a small error.
**Excel / Python:**
```python
import numpy as np

# Engagement scores for all 2,000 employees
rng = np.random.default_rng(7)
all_scores = np.round(rng.normal(70, 10, 2000), 1)

# Random sample of 50 employees
sample_scores = rng.choice(all_scores, size=50, replace=False)

print("Population mean (parameter):", round(all_scores.mean(), 2))
print("Sample mean (statistic):", round(sample_scores.mean(), 2))
```
Output:
```
Population mean (parameter): 69.6
Sample mean (statistic): 69.18
```
**Likely follow-ups:** 1) *When is the whole group your sample?* Rarely; treat it as a population if you only care about those people. 2) *What is sampling error?* The gap between statistic and parameter.
**Common mistakes:** Calling the survey result the "true" average; mixing up the symbols.

### Q14 ⭐⭐⭐ 🟡 Calculate the sample standard deviation of 2, 4, 4, 4, 5, 5, 7, 9 step by step.
**Asked at:** commonly asked (no company-specific report found); a classic textbook example.
**What the interviewer is checking:** Whether you can carry out the formula by hand without slipping.
**Say this in the interview:** "Mean is 5. Squared gaps sum to 32. Sample variance is 32 divided by 7, which is 4.571, so the sample standard deviation is about 2.14."
**Explain simply:**
- Step 1: mean = 40 / 8 = 5.
- Step 2: gaps from mean: -3, -1, -1, -1, 0, 0, 2, 4.
- Step 3: square them: 9, 1, 1, 1, 0, 0, 4, 16; sum = 32.
- Step 4: divide by n-1 = 7: 4.571.
- Step 5: square root: 2.138.
**Formula in plain words:** s = square root of (sum of squared gaps / (n - 1)).
**Worked example:** The data itself. (If this were a whole population, divide by 8 to get variance 4 and SD exactly 2; the question says sample, so 2.14.)
**Excel / Python:**
```python
values = [2, 4, 4, 4, 5, 5, 7, 9]

# Step 1: the mean
mean_value = sum(values) / len(values)

# Step 2: each value's gap from the mean
gaps = [v - mean_value for v in values]

# Step 3: square each gap and add them up
squared_gaps = [g ** 2 for g in gaps]
total_squared = sum(squared_gaps)

# Step 4 and 5: divide by n-1, then take the square root
sample_variance = total_squared / (len(values) - 1)
sample_sd = sample_variance ** 0.5

print("Mean:", mean_value)
print("Gaps:", gaps)
print("Squared gaps:", squared_gaps)
print("Sum:", total_squared)
print("Sample variance:", round(sample_variance, 3))
print("Sample SD:", round(sample_sd, 3))
```
Output:
```
Mean: 5.0
Gaps: [-3.0, -1.0, -1.0, -1.0, 0.0, 0.0, 2.0, 4.0]
Squared gaps: [9.0, 1.0, 1.0, 1.0, 0.0, 0.0, 4.0, 16.0]
Sum: 32.0
Sample variance: 4.571
Sample SD: 2.138
```
Excel: `=STDEV.S(A2:A9)` returns 2.138 (2010+; not run in Excel here).
**Likely follow-ups:** 1) *Population SD?* 2.0. 2) *Why do the gaps sum to zero before squaring?* The mean is the balance point.
**Common mistakes:** Dividing by 8 when the question says sample; forgetting to square root at the end.

### Q15 ⭐⭐⭐ 🟡 Explain standard deviation to a non-technical manager using employee attendance or salary data.
**Asked at:** commonly asked (no company-specific report found); a communication-focused gap-fill question.
**What the interviewer is checking:** Whether you can translate a technical idea into plain business language.
**Say this in the interview:** "The average tells you the typical attendance; the standard deviation tells you how much individual employees usually differ from it. If average attendance is 22 days with a standard deviation of about 2, most people are between 20 and 24 days."
**Explain simply:**
- Average = the centre. Standard deviation = the usual wiggle room around it.
- Small SD: everyone behaves similarly; large SD: a mix of very regular and very irregular people.
- Use it to say what is normal and to spot unusual cases (someone at 15 days).
- Avoid formulas with managers; use the "usual range" idea.
**Worked example:** Days present in a month for 9 employees: 19, 20, 21, 22, 22, 22, 23, 24, 25. Mean 22, SD 1.87, so "usual range" is about 20.1 to 23.9 days. 5 of 9 fall inside; with so few people the 68% rule is only a rough guide.
**Excel / Python:**
```python
import statistics

# Days present in a month for 9 employees
days_present = [19, 20, 21, 22, 22, 22, 23, 24, 25]

# Mean and standard deviation
mean_days = statistics.mean(days_present)
sd_days = statistics.stdev(days_present)

# The "usual range" is one SD either side of the mean
low = mean_days - sd_days
high = mean_days + sd_days
inside = [d for d in days_present if low <= d <= high]

print("Mean:", mean_days, "SD:", round(sd_days, 2))
print("Typical range:", round(low, 1), "to", round(high, 1))
print("Inside:", len(inside), "of", len(days_present))
```
Output:
```
Mean: 22 SD: 1.87
Typical range: 20.1 to 23.9
Inside: 5 of 9
```
In one line for the manager: "People are usually within about two days of the 22-day average."
**Likely follow-ups:** 1) *What would a high SD mean here?* Uneven attendance, worth checking by team or shift. 2) *Is SD good or bad?* Neither; it depends on context.
**Common mistakes:** Saying "SD is the average"; giving the formula instead of the meaning.

### Q16 ⭐⭐⭐ 🟡 A dataset has an outlier. How do you decide whether to remove it, cap it or keep it?
**Asked at:** commonly asked; "how to handle outliers" follows the IQR question in the Glassdoor reports we saw (snippets only).
**What the interviewer is checking:** Judgment, not just technique.
**Say this in the interview:** "First I find out why it is there. If it is an error I fix or remove it; if it is real but would distort a model or average, I might cap it or report the median; if it is real and important, I keep it and report it."
**Explain simply:**
- **Remove/fix:** data-entry mistakes, impossible values (age 250), duplicates. Check the source first.
- **Cap (winsorise):** replace extremes with a limit such as the upper fence, when you must keep the row but reduce its pull.
- **Keep:** genuine extremes that matter, like a top performer's pay or a fraud case; analyse them separately.
- Always document what you did and show results with and without.
**Worked example:** Salaries (Rs thousand): 32, 34, 35, 36, 38, 40, 42, 45, 480. The 480 may be a typo for 48. Upper fence = 42 + 1.5 x 7 = 52.5.
**Excel / Python:**
```python
import numpy as np
import statistics

salaries = [32, 34, 35, 36, 38, 40, 42, 45, 480]

# Upper fence from the IQR rule
q1 = np.percentile(salaries, 25)
q3 = np.percentile(salaries, 75)
upper_fence = q3 + 1.5 * (q3 - q1)
print("Upper fence:", upper_fence)

# Option 1: keep as is; Option 2: remove; Option 3: cap at the fence
print("Mean as is:", round(statistics.mean(salaries), 2))
print("Mean without 480:", round(statistics.mean(salaries[:-1]), 2))
capped = [min(s, upper_fence) for s in salaries]
print("Mean after capping:", round(statistics.mean(capped), 2))
print("Median either way:", statistics.median(salaries), statistics.median(salaries[:-1]))
```
Output:
```
Upper fence: 52.5
Mean as is: 86.89
Mean without 480: 37.75
Mean after capping: 39.39
Median either way: 38 37.0
```
The mean swings from 86.9 to 37.8 depending on the choice; the median barely moves, so it is the safer summary if I cannot confirm the value.
**Likely follow-ups:** 1) *How do you confirm an error?* Ask the data owner or check the source system. 2) *Does it change for models?* Tree models tolerate outliers; linear models do not.
**Common mistakes:** Deleting every flagged value; changing data silently without documentation.

### Q17 ⭐⭐⭐ 🟡 Two teams have the same average monthly sales but different standard deviations. Which team is more consistent and what would you tell the manager?
**Asked at:** commonly asked (no company-specific report found); gap-fill business scenario.
**What the interviewer is checking:** Whether you see that an average hides variability.
**Say this in the interview:** "The team with the lower standard deviation is more consistent. Same average, but one hits it every month and the other swings between very good and very bad months, which matters for planning and forecasting."
**Explain simply:**
- Lower SD means predictable results; higher SD means volatile.
- Compare using the coefficient of variation (SD / mean) if the averages differ (Q26).
- Recommend investigating why the volatile team swings (seasonality, one big client, staffing gaps).
- Neither is automatically "better": consistency is good for planning, but a volatile team may have higher peaks.
**Worked example:** Monthly sales (lakh), six months. Team A: 48, 50, 52, 49, 51, 50. Team B: 20, 80, 35, 65, 50, 50. Both average 50.
**Excel / Python:**
```python
import statistics

team_a = [48, 50, 52, 49, 51, 50]
team_b = [20, 80, 35, 65, 50, 50]

# Mean, SD and SD as a percent of the mean for each team
for name, sales in [("A", team_a), ("B", team_b)]:
    mean_sales = statistics.mean(sales)
    sd_sales = statistics.stdev(sales)
    print("Team", name, "mean:", mean_sales, "SD:", round(sd_sales, 2),
          "CV:", round(sd_sales / mean_sales * 100, 1), "%")
```
Output:
```
Team A mean: 50 SD: 1.41 CV: 2.8 %
Team B mean: 50 SD: 21.21 CV: 42.4 %
```
Team A varies by about 1.4 lakh around 50; Team B by about 21 lakh. Tell the manager Team A is far more predictable.
**Likely follow-ups:** 1) *Is Team B worse?* Not necessarily; look at why. 2) *What else would you check?* Trend over time, not just spread.
**Common mistakes:** Judging teams on the average alone; calling the higher SD team "better" because it has bigger peaks.

### Q18 ⭐⭐ 🟢 What is the range of a dataset, and what is its main weakness?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the simplest spread measure and its limits.
**Say this in the interview:** "Range is the maximum minus the minimum. It is easy but uses only two values, so one extreme value changes it completely and it says nothing about the values in between."
**Explain simply:**
- Quick to compute and easy to explain (salaries run from X to Y).
- Weakness: one outlier inflates it; it ignores everything between the ends.
- Also tends to grow as you collect more data.
- IQR or SD give a more reliable spread.
**Formula in plain words:** range = largest value minus smallest value.
**Worked example:** Salaries (Rs thousand) 32 to 42 have range 10. Add a founder at 300 and the range jumps to 268.
**Excel / Python:**
```python
salaries = [32, 34, 35, 36, 38, 40, 42]

# Range = largest minus smallest
print("Range:", max(salaries) - min(salaries))

# Add one outlier and recompute
salaries.append(300)
print("Range with outlier:", max(salaries) - min(salaries))
```
Output:
```
Range: 10
Range with outlier: 268
```
One person changed the range from 10 to 268. Excel: `=MAX(A2:A8)-MIN(A2:A8)` (not run in Excel here).
**Likely follow-ups:** 1) *Better alternative?* IQR. 2) *When is range useful?* Quick sanity checks on data limits.
**Common mistakes:** Reporting range without min and max values; using it as the sole spread measure.

### Q19 ⭐⭐ 🟢 What is a histogram, and what can you learn from it that the mean alone cannot show?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you look at the shape of data, not just one number.
**Say this in the interview:** "A histogram groups values into ranges (bins) and shows how many fall in each. It reveals shape: skew, multiple peaks, gaps and outliers, none of which a single average can show."
**Explain simply:**
- Bars show counts per bin; the bars touch because the data is continuous.
- You can see skew, a bell shape, two peaks, or odd spikes.
- The bin width matters: too wide hides detail, too narrow looks noisy.
- Different from a bar chart, which compares separate categories.
**Worked example:** Appraisal scores for 22 employees: a low group around 22 to 26 and a high group around 60 to 64. The mean is 43, a score almost nobody has. The histogram shows two clusters and nothing in the middle.
**Excel / Python:**
```python
import statistics
import numpy as np

# 22 appraisal scores in two clusters
scores = [22]*3 + [24]*5 + [26]*3 + [60]*3 + [62]*5 + [64]*3
print("Mean:", statistics.mean(scores))

# Count scores in bins of width 10 and draw a text histogram
counts, edges = np.histogram(scores, bins=[20, 30, 40, 50, 60, 70])
for i in range(len(counts)):
    print(int(edges[i]), "-", int(edges[i+1]), ":", "#" * int(counts[i]))
```
Output:
```
Mean: 43
20 - 30 : ###########
30 - 40 : 
40 - 50 : 
50 - 60 : 
60 - 70 : ###########
```
Mean 43 sits in an empty gap; the histogram shows two separate groups. In Excel, use Insert > Histogram chart (2016+; not run in Excel here).
**Likely follow-ups:** 1) *What does bimodal suggest?* Two subgroups (Q59). 2) *How do you choose bins?* Try a few widths.
**Common mistakes:** Using a histogram for categories; ignoring bin width.

### Q20 ⭐⭐ 🟢 What are the types of data (nominal, ordinal, interval, ratio), and which averages apply to each?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you pick statistics that make sense for the data type.
**Say this in the interview:** "Nominal is labels with no order, like department. Ordinal has an order but uneven gaps, like a 1 to 5 rating. Interval has equal gaps but no true zero, like temperature in Celsius. Ratio has equal gaps and a true zero, like salary. Mode works for all, median needs at least ordinal, and mean needs interval or ratio."
**Explain simply:**
- **Nominal:** names only (department, city). Only the mode makes sense.
- **Ordinal:** ranked (rating: poor, fair, good). Mode and median; the mean is debatable since the gap between "good" and "great" is not a fixed number.
- **Interval:** equal steps, zero is arbitrary (temperature in Celsius, calendar year). Mode, median, mean; ratios like "twice as hot" are meaningless.
- **Ratio:** true zero (salary, tenure, sick days). All averages, and ratios like "twice the salary" make sense.
- In practice, many analysts do average 1 to 5 survey ratings, but they should say it is an assumption.

| Type | HR example | Mode | Median | Mean |
|---|---|---|---|---|
| Nominal | Department | Yes | No | No |
| Ordinal | Performance rating (1 to 5) | Yes | Yes | Debatable |
| Interval | Temperature in the office | Yes | Yes | Yes |
| Ratio | Salary, tenure | Yes | Yes | Yes |

**Worked example:** Average employee ID is meaningless (nominal label stored as a number); average salary is meaningful (ratio).
**Likely follow-ups:** 1) *Is a rating of 1 to 5 ordinal or interval?* Strictly ordinal; often treated as interval. 2) *Is age ratio?* Yes.
**Common mistakes:** Averaging codes such as department IDs or pin codes; treating ordinal scores as exact measurements without saying so.

### Q21 ⭐⭐ 🟢 What is a frequency distribution, and how do you build one in a table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you turn a long list of raw values into a small summary table that shows how often each value (or range) occurs?
**Say this in the interview:** "A frequency distribution is a table that lists each value, or each range of values, and how many times it occurs. I add relative frequency (the percent of the total) and cumulative frequency (the running total) so patterns are easy to read."
**Explain simply:**
- **Frequency** means a simple count: how many employees took 3 leave days.
- **Relative frequency** is the count divided by the total, shown as a percent.
- **Cumulative frequency** is the running total, which answers "how many took 3 days or fewer?".
- For a continuous column such as salary, first group values into **bins** (ranges like 20,000 to 40,000), then count per bin. Keep bins equal in width and non-overlapping.
**Formula in plain words:** relative frequency = count of that value divided by total count. In symbols: f / n.
**Worked example:** Leave days taken last year by 20 employees. The table below shows that 4 employees took exactly 2 days, and 9 employees (45%) took 2 days or fewer.
**Excel / Python:**
Excel layout: leave days in A2:A21, the distinct values 0 to 8 in D2:D10. In E2 type `=COUNTIF($A$2:$A$21, D2)` and copy down; it returns how many employees took that many days (all Excel versions; not run in Excel here). For bins, use `=FREQUENCY(A2:A21, bin_limits)` (array formula in older Excel).
```python
import pandas as pd

# Leave days taken last year by 20 employees
leave_days = [0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 6, 8, 0, 2, 3, 1]
leave_series = pd.Series(leave_days)

# Count how many employees took each number of leave days
frequency = leave_series.value_counts().sort_index()
table = pd.DataFrame({"frequency": frequency})

# Turn each count into a percent of all 20 employees
table["relative_pct"] = (table["frequency"] / len(leave_series) * 100).round(1)

# Running total of the counts
table["cumulative_freq"] = table["frequency"].cumsum()
print(table)

# For a continuous column, group salaries into equal-width bins first
salaries = [22000, 25000, 28000, 31000, 34000, 36000, 41000,
            45000, 52000, 58000, 64000, 75000, 90000, 120000]
salary_bins = pd.cut(pd.Series(salaries), bins=[20000, 40000, 60000, 80000, 120000])
bin_counts = salary_bins.value_counts().sort_index()
print(bin_counts.to_string())
```
```text
   frequency  relative_pct  cumulative_freq
0          2          10.0                2
1          3          15.0                5
2          4          20.0                9
3          5          25.0               14
4          2          10.0               16
5          2          10.0               18
6          1           5.0               19
8          1           5.0               20
(20000, 40000]     6
(40000, 60000]     4
(60000, 80000]     2
(80000, 120000]    2
```
Each row of the first table is one leave-day value: for example 3 days was taken by 5 employees (25%), and 14 of 20 took 3 days or fewer. In the second table, 6 of 14 employees earn between 20,000 and 40,000 (the bin includes its upper limit).
**Likely follow-ups:** 1) *How many bins?* Usually 5 to 10; too few hides the shape, too many looks noisy. 2) *What chart shows it?* A bar chart for categories, a histogram for binned numbers (Q19).
**Common mistakes:** Overlapping or unequal bins; forgetting that bin edges belong to one bin only; reporting counts without percents when groups differ in size.

### Q22 ⭐⭐ 🟢 Can a dataset have more than one mode, or no mode? Give examples.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that mode is the most frequent value and that it may be one, several or none?
**Say this in the interview:** "Yes to both. If two values tie for most frequent the data is bimodal, with more ties it is multimodal, and if every value appears once there is no mode."
**Explain simply:**
- **Mode** = the value that appears most often.
- One mode: 2, 3, 3, 5, 7 has mode 3.
- Two modes (bimodal): 1, 2, 2, 3, 3, 4 has modes 2 and 3.
- No mode: 10, 20, 30, 40, every value appears once.
- Mode is the only average that works for categories, such as the most common department or job title.
**Worked example:** Shoe sizes of 6 new joiners: 7, 8, 8, 9, 9, 10 has two modes (8 and 9), so the admin team should stock both sizes.
**Excel / Python:**
Excel: `=MODE.SNGL(A2:A7)` returns the first mode only, and returns `#N/A` when there is no mode. `=MODE.MULT(A2:A7)` returns all modes (select several cells and press Ctrl+Shift+Enter in older Excel; Excel 2010+; not run in Excel here).
```python
import statistics

# Three small datasets: one mode, two modes, no repeated value
one_mode_data = [2, 3, 3, 5, 7]
two_mode_data = [1, 2, 2, 3, 3, 4]
no_mode_data = [10, 20, 30, 40]

# multimode returns every value tied for most frequent
print(statistics.multimode(one_mode_data))
print(statistics.multimode(two_mode_data))
print(statistics.multimode(no_mode_data))
```
```text
[3]
[2, 3]
[10, 20, 30, 40]
```
The first two lists show one and two modes. For the last list Python returns every value because all tie at one occurrence; that means "no useful mode".
**Likely follow-ups:** 1) *Is a bimodal dataset a problem?* It often means two groups are mixed (Q59). 2) *Mode of decimals?* Group into bins first (Q50).
**Common mistakes:** Saying the mode is 0 when there is none; reporting only one mode when two tie.

### Q23 ⭐⭐ 🟢 What are the 25th, 50th and 75th percentiles called, and how do they relate to the median?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the quartile names and that the 50th percentile is the median?
**Say this in the interview:** "They are the first quartile Q1, the second quartile Q2 and the third quartile Q3. Q2 is the median itself, so the median is just the 50th percentile."
**Explain simply:**
- **Percentile** = the value below which a given percent of the data falls.
- **Q1 (25th percentile):** a quarter of values are at or below it.
- **Q2 (50th percentile):** the median, the middle value; half the values are below it.
- **Q3 (75th percentile):** three quarters of values are at or below it.
- Together the three cut the sorted data into four equal-sized groups. Q3 minus Q1 is the IQR (Q10).
**Worked example:** Salaries (lakh per year) of 10 employees: 3, 4, 4, 5, 6, 7, 8, 9, 12, 30. Q1 is 4.25, median is 6.5, Q3 is 8.75, so the middle half of staff earns between 4.25 and 8.75 lakh.
**Excel / Python:**
Excel: salaries in A2:A11; `=QUARTILE.INC(A2:A11, 1)` for Q1, `2` for the median, `3` for Q3 (Excel 2010+; same as `PERCENTILE.INC` with 0.25, 0.5, 0.75; not run in Excel here).
```python
import numpy as np

# Annual salaries in lakh for 10 employees
salaries_lakh = [3, 4, 4, 5, 6, 7, 8, 9, 12, 30]

# Ask for the 25th, 50th and 75th percentiles in one step
q1, q2, q3 = np.percentile(salaries_lakh, [25, 50, 75])

# Check that the 50th percentile equals the median
median_value = np.median(salaries_lakh)

print("Q1:", q1)
print("Q2:", q2)
print("Q3:", q3)
print("Median:", median_value)
```
```text
Q1: 4.25
Q2: 6.5
Q3: 8.75
Median: 6.5
```
Q2 and the median are the same number, 6.5. Q1 and Q3 fall between data points, so they are interpolated (Q42).
**Likely follow-ups:** 1) *What is the IQR?* Q3 minus Q1 = 4.5 here. 2) *Why do tools differ?* Different interpolation rules (Q42).
**Common mistakes:** Treating the quartile as a group of people instead of a cut-off value; saying the median is not a percentile.

### Q24 ⭐⭐ 🟢 What is skewness, and how does it affect the choice between mean and median?
**Asked at:** commonly asked (no company-specific report found); one candidate report mentions a "median greater than mean in negatively skewed data" question at an Indian company (single anecdote, unverified).
**What the interviewer is checking:** Can you connect the shape of data to the right average?
**Say this in the interview:** "Skewness measures how lopsided a distribution is. Right (positive) skew has a long tail of high values and pulls the mean above the median; left (negative) skew does the opposite. With strong skew I report the median."
**Explain simply:**
- **Symmetric:** both sides look alike; mean and median are close.
- **Right-skewed:** a few very high values, like salaries with a few CXOs; mean greater than median.
- **Left-skewed:** a few very low values, like test scores where most do well but a few fail; mean less than median.
- The mean is pulled toward the tail because it uses every value; the median only cares about the middle position.
**Worked example:** Salaries in lakh: 3, 4, 4, 5, 5, 6, 6, 7, 8, 9, 12, 30 have mean 8.25 but median 6, skew value +2.44 (right). Exam scores 20, 55, 70, 75, 78, 80, 82, 85, 88, 90 have mean 72.3 but median 79, skew value -1.72 (left).
**Excel / Python:**
Excel: `=SKEW(A2:A13)` (all versions; sample-adjusted formula; not run in Excel here; Python below uses the plain population formula, so the numbers can differ slightly).
```python
import numpy as np
from scipy import stats

# Right-skewed data: a few very high salaries (lakh)
salaries_lakh = [3, 4, 4, 5, 5, 6, 6, 7, 8, 9, 12, 30]

# Left-skewed data: most people score high, a few score very low
exam_scores = [20, 55, 70, 75, 78, 80, 82, 85, 88, 90]

# Compare mean, median and skewness for each dataset
for name, values in [("salaries", salaries_lakh), ("exam scores", exam_scores)]:
    mean_value = np.mean(values)
    median_value = np.median(values)
    skew_value = stats.skew(values)
    print(name, "| mean:", round(mean_value, 2), "| median:", median_value,
          "| skew:", round(skew_value, 2))
```
```text
salaries | mean: 8.25 | median: 6.0 | skew: 2.44
exam scores | mean: 72.3 | median: 79.0 | skew: -1.72
```
Positive skew value with mean above median means a right tail; negative skew with mean below median means a left tail.
**Likely follow-ups:** 1) *What skew value counts as "high"?* Roughly beyond +1 or -1 is strongly skewed (rule of thumb). 2) *Does mean greater than median always mean right skew?* No (Q40).
**Common mistakes:** Mixing up the direction (skew is named after the tail, not the hump); using the mean on salary data without checking skew.

### Q25 ⭐⭐ 🟢 What is the five-number summary?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the five values that summarise a dataset and that they drive a box plot?
**Say this in the interview:** "It is the minimum, first quartile, median, third quartile and maximum. Together they show the centre, the spread and the extremes without being thrown off by outliers, and they are exactly what a box plot draws."
**Explain simply:**
- **Minimum / maximum:** the smallest and largest values.
- **Q1, median, Q3:** the 25th, 50th and 75th percentiles (Q23).
- The gap between Q1 and Q3 is the IQR; the gap between min and max is the range.
- A median far from the middle of the box, or a max far above Q3, hints at skew or outliers.
**Worked example:** Monthly salaries (thousand rupees) of 10 staff: 30, 32, 35, 36, 40, 42, 45, 50, 55, 90. The summary is 30, 35.25, 41, 48.75, 90. The top value 90 sits far above Q3, so it is worth checking.
**Excel / Python:**
Excel: `=QUARTILE.INC(A2:A11, 0)` gives the minimum, `1` Q1, `2` median, `3` Q3, `4` the maximum (Excel 2010+; not run in Excel here).
```python
import numpy as np

# Monthly salaries in thousand rupees for 10 employees
monthly_salaries = [30, 32, 35, 36, 40, 42, 45, 50, 55, 90]

# Percentiles 0, 25, 50, 75, 100 are exactly the five numbers
minimum, q1, median_value, q3, maximum = np.percentile(monthly_salaries, [0, 25, 50, 75, 100])

print("Minimum:", minimum)
print("Q1:", q1)
print("Median:", median_value)
print("Q3:", q3)
print("Maximum:", maximum)
```
```text
Minimum: 30.0
Q1: 35.25
Median: 41.0
Q3: 48.75
Maximum: 90.0
```
The middle half of staff earn between 35.25 and 48.75 thousand; the single 90 is a candidate outlier.
**Likely follow-ups:** 1) *Which chart shows it?* The box plot (Q11). 2) *Does pandas `describe()` give it?* Yes, plus count, mean and standard deviation.
**Common mistakes:** Listing mean instead of median; forgetting the minimum and maximum.

### Q26 ⭐⭐ 🟡 What is the coefficient of variation, and when is it better than standard deviation?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you compare variability of things measured in different units or at different scales?
**Say this in the interview:** "The coefficient of variation is standard deviation divided by the mean, as a percent. It is a unit-free measure of relative spread, so I use it to compare variability between columns with different units or very different averages."
**Explain simply:**
- Standard deviation (SD) is in the data's own units, so Rs 8,000 and 1.6 years cannot be compared directly.
- Dividing by the mean converts spread into "percent of the average".
- A bigger CV means more relative variation.
- It only makes sense for positive, ratio-type data with a meaningful zero (not temperature in Celsius) and a mean not close to zero.
**Formula in plain words:** CV = standard deviation divided by mean, times 100. In symbols: CV = (s / mean) x 100.
**Worked example:** Five employees' salaries (Rs): 30,000 to 50,000, mean 40,000, SD 7,906, so CV is 19.8%. Their tenure (years) is 1 to 5, mean 3, SD 1.58, so CV is 52.7%. Tenure varies far more in relative terms, though 7,906 "looks" bigger than 1.58.
**Excel / Python:**
Excel: data in A2:A6; `=STDEV.S(A2:A6)/AVERAGE(A2:A6)` returns the CV as a decimal (format as %; Excel 2010+; not run in Excel here).
```python
import numpy as np

# Salaries in rupees and tenure in years for the same 5 employees
salaries = [30000, 35000, 40000, 45000, 50000]
tenure_years = [1, 2, 3, 4, 5]

# For each column compute mean, sample SD and the CV percent
for name, values in [("salary", salaries), ("tenure", tenure_years)]:
    mean_value = np.mean(values)
    sample_sd = np.std(values, ddof=1)
    cv_percent = sample_sd / mean_value * 100
    print(name, "| mean:", mean_value, "| SD:", round(sample_sd, 2),
          "| CV %:", round(cv_percent, 1))
```
```text
salary | mean: 40000.0 | SD: 7905.69 | CV %: 19.8
tenure | mean: 3.0 | SD: 1.58 | CV %: 52.7
```
In relative terms tenure (52.7%) is much more spread out than salary (19.8%).
**Likely follow-ups:** 1) *When does CV fail?* When the mean is near zero or negative. 2) *Example in HR?* Comparing pay spread between two departments with very different average pay.
**Common mistakes:** Comparing raw SDs across different units; using CV on data with a mean near zero.

### Q27 ⭐⭐ 🟡 What is a weighted mean, and when is it better than a simple mean? Calculate one for exam or appraisal scores.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that not all values count equally and can you apply weights correctly?
**Say this in the interview:** "A weighted mean multiplies each value by its importance (weight), adds them, and divides by the total weight. I use it whenever some items matter more, like an appraisal where targets count 50%."
**Explain simply:**
- A simple mean treats every value as equally important.
- A weight says how much a value should count; weights are often percentages adding to 100%.
- Use it for appraisal scores, course grades, or averaging group averages of different sizes (Q41).
**Formula in plain words:** Multiply each value by its weight, add everything up, then divide by the sum of the weights. In symbols: sum(w x value) / sum(w).
**Worked example:** An appraisal: Targets 80 (weight 50%), Teamwork 90 (30%), Learning 70 (20%). Weighted mean = 0.5 x 80 + 0.3 x 90 + 0.2 x 70 = 40 + 27 + 14 = 81. The simple mean would be 80, which ignores that targets matter more.
**Excel / Python:**
Excel: scores in B2:B4, weights in C2:C4; `=SUMPRODUCT(B2:B4, C2:C4)/SUM(C2:C4)` returns 81 (all versions; not run in Excel here).
```python
import numpy as np

# Appraisal scores for Targets, Teamwork, Learning
scores = [80, 90, 70]

# How much each area counts (adds to 1.0)
weights = [0.5, 0.3, 0.2]

# Simple mean treats all three equally
simple_mean = np.mean(scores)

# Weighted mean counts targets more
weighted_mean = np.average(scores, weights=weights)

print("Simple mean:", simple_mean)
print("Weighted mean:", weighted_mean)
```
```text
Simple mean: 80.0
Weighted mean: 81.0
```
The weighted score (81) is higher because the weakest score, 70, carries only 20% of the weight while the two stronger scores carry 80%.
**Likely follow-ups:** 1) *What if weights do not add to 1?* Dividing by the sum of weights handles it. 2) *Can weights be counts?* Yes, that is how you combine group means (Q43).
**Common mistakes:** Dividing by the number of items instead of the sum of weights; weights that do not reflect real importance.

### Q28 ⭐⭐ 🟡 How do you calculate a percentile rank, and how is it different from a percentile value?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the two directions: value to rank, and rank to value?
**Say this in the interview:** "Percentile rank starts from a score and tells you the percent of the group at or below it. A percentile value starts from a percent and gives you the score at that cut-off. For example, a score of 72 may have percentile rank 60, and the 90th percentile value may be 85.5."
**Explain simply:**
- **Percentile rank:** score in, percent out. "What share of people did I beat or match?"
- **Percentile value:** percent in, score out. "What score do I need to be in the top 10%?"
- Definitions differ on ties: some count only values strictly below, some count values at or below.
**Formula in plain words:** Percentile rank = (number of values at or below the score divided by total count) x 100. In symbols: (count at or below / n) x 100.
**Worked example:** 10 candidates' test scores: 55, 60, 62, 65, 70, 72, 75, 80, 85, 90. A score of 72 has 6 values at or below it out of 10, so percentile rank is 60. Counting only strictly below gives 5 of 10 = 50. The 90th percentile value is 85.5.
**Excel / Python:**
Excel: scores in A2:A11; `=PERCENTRANK.INC(A2:A11, 72)` returns 0.555 (it uses the number below divided by n minus 1, so it differs from the 60 above) and `=PERCENTILE.INC(A2:A11, 0.9)` returns 85.5 (Excel 2010+; not run in Excel here).
```python
import numpy as np
from scipy import stats

# Test scores of 10 candidates
test_scores = [55, 60, 62, 65, 70, 72, 75, 80, 85, 90]

# Percentile rank: share of scores at or below 72
rank_at_or_below = stats.percentileofscore(test_scores, 72, kind="weak")

# Percentile rank: share of scores strictly below 72
rank_strictly_below = stats.percentileofscore(test_scores, 72, kind="strict")

# Percentile value: the score at the 90th percentile
value_at_90th = np.percentile(test_scores, 90)

print("Rank (at or below):", rank_at_or_below)
print("Rank (strictly below):", rank_strictly_below)
print("90th percentile value:", value_at_90th)
```
```text
Rank (at or below): 60.0
Rank (strictly below): 50.0
90th percentile value: 85.5
```
Rank answers "how many are below this score"; the 90th percentile value answers "which score is the cut-off". They are inverse operations.
**Likely follow-ups:** 1) *Why do tools disagree on rank?* Different tie and counting rules (Q42). 2) *Which one would a hiring report show?* Rank, to tell a candidate where they stand.
**Common mistakes:** Calling 72 "the 72nd percentile"; mixing up the two directions.

### Q29 ⭐⭐ 🟡 How do you find the median of grouped data, or of an even number of values?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you handle the two standard textbook cases without a calculator trap?
**Say this in the interview:** "With an even count, I sort and average the two middle values. With grouped data I find the class containing the middle position and interpolate inside it using the formula L + ((N/2 - CF) / f) x h."
**Explain simply:**
- **Even count:** no single middle value, so take the mean of the two middle ones. For 12, 15, 18, 20, 22, 30 the middle two are 18 and 20, giving 19.
- **Grouped data** (only class intervals and counts are known): find the **median class**, the first class where the cumulative count reaches N/2, then assume values are evenly spread inside it.
- L = lower limit of that class, CF = cumulative count before it, f = count in it, h = class width.
**Formula in plain words:** Median = lower limit of the median class + ((half the total - cumulative count before the class) / count in the class) x class width. In symbols: L + ((N/2 - CF) / f) x h.
**Worked example:** Days taken to fill 50 vacancies: 0-10 days (8), 10-20 (10), 20-30 (16), 30-40 (10), 40-50 (6). N/2 = 25. Cumulative counts are 8, 18, 34, so the median class is 20-30 with L = 20, CF = 18, f = 16, h = 10. Median = 20 + ((25 - 18) / 16) x 10 = 24.375 days (an estimate).
**Excel / Python:**
Excel: for the even case `=MEDIAN(A2:A7)` returns 19; grouped data has no built-in, so use the formula above in a cell (not run in Excel here).
```python
import numpy as np

# Case 1: an even number of values, average the two middle ones
even_values = [12, 15, 18, 20, 22, 30]
even_median = np.median(even_values)

# Case 2: grouped data, find the median class then interpolate
class_counts = [8, 10, 16, 10, 6]
class_lower_limits = [0, 10, 20, 30, 40]
class_width = 10
total_count = sum(class_counts)
half_count = total_count / 2

cumulative_before = 0
for count, lower_limit in zip(class_counts, class_lower_limits):
    # The median class is the first one where the running total passes half
    if cumulative_before + count >= half_count:
        grouped_median = lower_limit + ((half_count - cumulative_before) / count) * class_width
        break
    cumulative_before += count

print("Even-count median:", even_median)
print("Grouped median:", grouped_median)
```
```text
Even-count median: 19.0
Grouped median: 24.375
```
The even-count median is the midpoint of 18 and 20. The grouped median is about 24.4 days, an estimate because the raw values are not known.
**Likely follow-ups:** 1) *Is grouped median exact?* No, it is an estimate. 2) *What about odd count?* Just the middle value.
**Common mistakes:** Using the class midpoint instead of interpolating; forgetting to sort first.

### Q30 ⭐⭐ 🟡 What is a z-score, and how do you use it to compare two values from different distributions?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you put values on a common scale using standard deviations?
**Say this in the interview:** "A z-score says how many standard deviations a value is above or below its own group's mean. Because it removes units and scale, I can compare a value from one distribution with a value from another."
**Explain simply:**
- Subtract the group's mean, then divide by the group's standard deviation.
- z = 0 means exactly average; z = +2 means two SDs above average; negative means below.
- Comparing raw numbers across groups is unfair if the groups have different averages and spreads; z-scores make it fair.
- In roughly bell-shaped data, |z| above 3 is unusual (rule of thumb).
**Formula in plain words:** z = (value minus mean) divided by standard deviation. In symbols: z = (x - mean) / s.
**Worked example:** Asha scored 78 in a test where the mean was 70 and SD 8: z = 1.0. Ravi scored 64 in a different test where the mean was 52 and SD 6: z = 2.0. Asha has the higher raw score, but Ravi did better relative to his group.
**Excel / Python:**
Excel: `=STANDARDIZE(78, 70, 8)` returns 1 (all versions; not run in Excel here).
```python
# A z-score tells how many standard deviations a value is from its group mean
def z_score(value, group_mean, group_sd):
    difference_from_mean = value - group_mean
    return difference_from_mean / group_sd

asha_z = z_score(78, 70, 8)
ravi_z = z_score(64, 52, 6)

print("Asha z-score:", asha_z)
print("Ravi z-score:", ravi_z)
```
```text
Asha z-score: 1.0
Ravi z-score: 2.0
```
Ravi is 2 standard deviations above his group, Asha only 1, so Ravi is the stronger performer relative to peers.
**Likely follow-ups:** 1) *Does z-score need normal data?* The calculation does not, but interpreting it as "unusual" works best for bell-shaped data. 2) *Where else is it used?* Outlier detection (|z| > 3).
**Common mistakes:** Using the wrong mean or SD (each value must use its own group's); reading a z-score as a percent.

### Q31 ⭐⭐ 🟡 Why is the median robust to outliers, and what does robust mean in statistics?
**Asked at:** commonly asked (no company-specific report found); the median's robustness to outliers appears in the Exponent guide snippet we saw.
**What the interviewer is checking:** Can you explain robustness with a clear reason, not just the slogan?
**Say this in the interview:** "A statistic is robust if a few extreme values barely change it. The median only depends on the middle position, so making the biggest value larger does not move it; the mean adds up every value, so one huge value drags it."
**Explain simply:**
- **Robust** = resistant to outliers or bad data.
- The median sorts the data and picks the middle; the size of the extremes does not matter, only their order.
- The mean uses the actual size of every value, so one extreme can move it a lot.
- Robustness is measured by the **breakdown point**: the share of data that must be corrupted before the statistic can be changed arbitrarily. The median needs about 50%; the mean needs just one value.
**Worked example:** Salaries (thousand): 30, 32, 35, 38, 40 have mean 35 and median 35. Add one CEO at 1,000 and the mean jumps to 195.8 while the median only moves to 36.5.
**Excel / Python:**
```python
import numpy as np

# Salaries of 5 employees in thousand rupees
base_salaries = [30, 32, 35, 38, 40]

# The same team after adding one extreme salary
salaries_with_ceo = base_salaries + [1000]

print("Without CEO | mean:", np.mean(base_salaries), "| median:", np.median(base_salaries))
print("With CEO    | mean:", round(np.mean(salaries_with_ceo), 1), "| median:", np.median(salaries_with_ceo))
```
```text
Without CEO | mean: 35.0 | median: 35.0
With CEO    | mean: 195.8 | median: 36.5
```
One extreme value changed the mean by about 160 but the median by only 1.5.
**Likely follow-ups:** 1) *Other robust measures?* IQR and MAD (Q54). 2) *Is robust always better?* No; it ignores information in the extremes, which may be real and important.
**Common mistakes:** Saying the median "ignores" outliers completely (it still counts them as one position); assuming outliers are always errors.

### Q32 ⭐⭐ 🟡 Attrition rates by month are 2%, 3%, 2%, 12%, 3%, 2%. Which summary statistic would you report to HR leadership, and why?
**Asked at:** commonly asked (no company-specific report found); HR-flavoured gap-fill.
**What the interviewer is checking:** Can you choose a summary that is honest when one month is unusual, without hiding it?
**Say this in the interview:** "I would report the median, 2.5%, as the typical month, and separately flag that the fourth month hit 12% and explain why. The mean of 4% is pulled up by that single spike and describes no actual month."
**Explain simply:**
- Mean = 4.0%; median = 2.5%. Five of six months are between 2% and 3%.
- Without the spike the mean would be 2.4%, so one month nearly doubled the average.
- But do not delete the spike: a 12% month could be a layoff, a bonus-cycle exit wave, or a data error. Leadership needs to hear about it.
- Report both: "typical month 2.5%, with one exceptional month at 12%".
**Worked example:** Total attrition over the six months is 24 percentage points; the one month of 12% contributes half of it.
**Excel / Python:**
Excel: rates in B2:B7; `=MEDIAN(B2:B7)` returns 2.5%, `=AVERAGE(B2:B7)` returns 4% (all versions; not run in Excel here).
```python
import numpy as np

# Monthly attrition rates in percent
monthly_attrition = [2, 3, 2, 12, 3, 2]

# Typical month (median) vs average month (mean)
median_rate = np.median(monthly_attrition)
mean_rate = np.mean(monthly_attrition)

# Mean if the spike month is set aside, only to show its effect
without_spike = [2, 3, 2, 3, 2]
mean_without_spike = np.mean(without_spike)

print("Median:", median_rate)
print("Mean:", mean_rate)
print("Mean without the 12% month:", mean_without_spike)
```
```text
Median: 2.5
Mean: 4.0
Mean without the 12% month: 2.4
```
The median describes a normal month; the mean (4.0) is higher than five of the six months.
**Likely follow-ups:** 1) *Would you remove the 12%?* Not without checking its cause (Q16). 2) *Is monthly the right unit?* For a true annual rate, compute exits over average headcount for the year instead of averaging months.
**Common mistakes:** Quoting the mean without mentioning the spike; silently dropping the spike.

### Q33 ⭐⭐ 🟡 How do you choose between mean, median and mode for a given business column such as order value, age or shoe size?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you match the average to the data type and shape?
**Say this in the interview:** "I look at the data type and the shape. Categories or sizes: mode. Numbers with a long tail, like order value or salary: median. Roughly symmetric numbers, like age in a stable workforce: mean."
**Explain simply:**
- **Shoe size** is a discrete label; the question is "which size sells most?", so use the mode. A mean of 8.3 is not a size you can stock.
- **Order value** is usually right-skewed (many small orders, few huge ones). Median shows the typical order; mean is useful for total revenue planning (mean x number of orders = total).
- **Age** is often fairly symmetric, so the mean works; check the histogram first (Q19), and use the median if there is skew.
- If the purpose is a total or a forecast, the mean is the one that adds up; if it is "what is typical", the median is safer.
**Worked example:** Orders of Rs 200, 250, 300, 300, 350, 400, 9,000: mean = 1,543, median = 300, mode = 300. The mean describes no real order; the median is the typical one.
**Excel / Python:**
```python
import numpy as np
import statistics

# Seven order values in rupees, one of them very large
order_values = [200, 250, 300, 300, 350, 400, 9000]

mean_order = np.mean(order_values)
median_order = np.median(order_values)
mode_order = statistics.mode(order_values)

print("Mean:", round(mean_order, 1))
print("Median:", median_order)
print("Mode:", mode_order)
```
```text
Mean: 1542.9
Median: 300.0
Mode: 300
```
Median and mode (300) describe the typical order; the mean (1,542.9) is dragged up by one bulk order.
**Likely follow-ups:** 1) *Which for ordinal data like ratings 1 to 5?* Median or mode. 2) *Which for revenue per month?* Mean, because totals matter.
**Common mistakes:** Averaging category codes; reporting mean for skewed money data without a caveat.

### Q34 ⭐⭐ 🟡 What is the mean absolute deviation, and how does it differ from standard deviation?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a second way to measure spread and why SD is preferred?
**Say this in the interview:** "Mean absolute deviation is the average distance of values from the mean, ignoring direction. Standard deviation squares the distances first, so it punishes big gaps more. MAD is easier to explain; SD is used more because it fits the maths of the normal distribution."
**Explain simply:**
- Step 1: find the mean. Step 2: find each value's distance from the mean and drop the minus sign. Step 3: average those distances.
- SD squares distances, averages, then takes the square root, so large deviations count extra.
- Because of that, SD is more sensitive to outliers than mean absolute deviation, and SD is always at least as large.
- Note: "MAD" is also used for median absolute deviation (Q54); say which one you mean.
**Formula in plain words:** Add up the distances of each value from the mean (ignoring signs) and divide by the number of values. In symbols: sum(|x - mean|) / n.
**Worked example:** Data 2, 4, 4, 4, 5, 5, 7, 9 (mean 5): distances are 3, 1, 1, 1, 0, 0, 2, 4, total 12, so mean absolute deviation is 1.5, while the population SD is 2.0. Replace 9 with 29 and the mean absolute deviation becomes 5.375 but SD jumps to 8.23.
**Excel / Python:**
Excel: `=AVEDEV(A2:A9)` returns 1.5 (all versions; not run in Excel here).
```python
import numpy as np

# Original data and the same data with one extreme value
normal_data = [2, 4, 4, 4, 5, 5, 7, 9]
data_with_outlier = [2, 4, 4, 4, 5, 5, 7, 29]

for label, values in [("normal", normal_data), ("with outlier", data_with_outlier)]:
    values_array = np.array(values)
    mean_value = np.mean(values_array)
    # Distance of each value from the mean, signs removed
    distances = np.abs(values_array - mean_value)
    mean_abs_deviation = np.mean(distances)
    # Population SD for a like-for-like comparison
    standard_deviation = np.std(values_array, ddof=0)
    print(label, "| mean abs dev:", round(mean_abs_deviation, 3),
          "| SD:", round(standard_deviation, 3))
```
```text
normal | mean abs dev: 1.5 | SD: 2.0
with outlier | mean abs dev: 5.375 | SD: 8.231
```
The outlier raised the SD from 2.0 to 8.23 (about 4 times) but the mean absolute deviation only from 1.5 to 5.375 (about 3.6 times).
**Likely follow-ups:** 1) *Why is SD more popular?* Squares are easier to work with mathematically and variances add (Q53). 2) *Which is more robust?* Neither; median absolute deviation is (Q54).
**Common mistakes:** Confusing mean and median absolute deviation; forgetting the absolute value (plain deviations sum to zero).

### Q35 ⭐⭐ 🟡 A manager says 'the average employee takes 6 sick days.' What follow-up questions would you ask before trusting that number?
**Asked at:** commonly asked (no company-specific report found); HR-flavoured gap-fill.
**What the interviewer is checking:** Do you question a single number instead of accepting it?
**Say this in the interview:** "I would ask which average, which people, which period and how it is distributed. A mean of 6 could be driven by a couple of long-term illnesses while most staff took one or two days."
**Explain simply:**
- **Which average?** Mean or median? Ask for both.
- **Who is included?** All employees or only those who took leave? Part-timers, new joiners, contractors? Are zeros included?
- **What period?** A year, a flu season, a pandemic year?
- **Spread and outliers:** a few long absences (surgery, maternity-related medical leave) can inflate the mean.
- **Data quality:** how is sick leave recorded, and does "sick day" include half-days or work-from-home?
- **Comparison:** compared with what, last year or an industry benchmark?
**Worked example:** 12 employees took 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 40 sick days. Mean = 5.1 but median = 2; 25% took none; without the 40-day case the mean is 1.9. "Average 6" would mislead.
**Excel / Python:**
```python
import numpy as np

# Sick days taken last year by 12 employees
sick_days = [0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 40]
sick_days_array = np.array(sick_days)

mean_days = np.mean(sick_days_array)
median_days = np.median(sick_days_array)

# Share of employees who took no sick days at all
share_with_zero = np.mean(sick_days_array == 0)

# Mean if the single 40-day case is set aside
mean_without_longest = np.mean(sick_days_array[sick_days_array < 40])

print("Mean:", round(mean_days, 2))
print("Median:", median_days)
print("Share with zero days:", share_with_zero)
print("Mean without the 40-day case:", round(mean_without_longest, 2))
```
```text
Mean: 5.08
Median: 2.0
Share with zero days: 0.25
Mean without the 40-day case: 1.91
```
The typical person took 2 days; one long absence lifts the mean to about 5.
**Likely follow-ups:** 1) *What would you report?* Median, share with zero, and number of long absences. 2) *Is a mean of 6 useless?* No, it is right for total leave cost planning, but not for "typical".
**Common mistakes:** Accepting "average" without asking which; excluding zero-leave people unknowingly.

### Q36 ⭐⭐ 🟡 How do you describe the spread of a dataset to a business audience in one or two sentences?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you translate statistics into plain business language?
**Say this in the interview:** "I say what the typical value is, and how far people usually are from it, in the original units. For example: 'Most employees earn around Rs 40,000, and a typical person is within about Rs 8,000 of that.'"
**Explain simply:**
- Skip jargon like "variance". Use the data's own units (rupees, days, hours).
- Pair a centre with a spread: mean with standard deviation, or median with the middle-50% range (IQR).
- Give the range for most people: "about two thirds of employees are within one SD of the mean" (for bell-shaped data).
- Mention extremes separately: "a few earn much more".
- Offer a comparison to make it meaningful: "this team's spread is double that of last year".
**Worked example:** Salaries 30,000, 35,000, 40,000, 45,000, 50,000: mean 40,000, SD 7,906. Sentence: "Salaries average Rs 40,000, and a typical employee is about Rs 8,000 above or below that. The middle half earn between Rs 35,000 and Rs 45,000."
**Excel / Python:**
```python
import numpy as np

# Salaries in rupees for 5 employees
salaries = [30000, 35000, 40000, 45000, 50000]

mean_salary = np.mean(salaries)
sample_sd = np.std(salaries, ddof=1)
q1, q3 = np.percentile(salaries, [25, 75])

print("Average salary:", mean_salary)
print("Typical distance from average:", round(sample_sd))
print("Middle half earns between:", q1, "and", q3)
```
```text
Average salary: 40000.0
Typical distance from average: 7906
Middle half earns between: 35000.0 and 45000.0
```
These three numbers fill in the sentence template above.
**Likely follow-ups:** 1) *Which spread measure for skewed data?* IQR. 2) *Should you show a chart?* Yes, a histogram or box plot supports the sentence.
**Common mistakes:** Quoting the variance (squared units); giving a spread without the centre.

### Q37 ⭐⭐ 🟡 How would you summarise a numeric column in a new dataset before doing any analysis?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you have a sensible first-look routine for new data?
**Say this in the interview:** "I check how many values are missing, then look at count, mean, median, min, max, quartiles and standard deviation, check the skew, and plot a histogram and box plot to see shape and outliers. Only then do I decide how to clean or analyse."
**Explain simply:**
- **Count and missing:** are there gaps? How many?
- **Centre:** mean and median; a big gap between them suggests skew.
- **Spread:** SD, IQR, min and max; do min and max look realistic (a negative salary, an age of 200)?
- **Shape:** histogram for distribution, box plot for outliers.
- **Context:** units, definition of the column, and whether zeros really mean zero or "missing".
**Worked example:** A salary column of 11 rows has 1 missing value. The 10 remaining have mean 45.5, median 41, max 90 and skew 2.09, so the data is right-skewed and the 90 deserves a check.
**Excel / Python:**
```python
import pandas as pd

# A salary column in thousand rupees, with one missing value
employees = pd.DataFrame({"salary": [30, 32, 35, 36, 40, 42, 45, 50, 55, 90, None]})
salary_column = employees["salary"]

# Step 1: how many values are missing?
missing_count = salary_column.isna().sum()

# Step 2: count, mean, std, min, quartiles, max (missing values are skipped)
summary = salary_column.describe()

# Step 3: check how lopsided the data is
skew_value = salary_column.skew()

print("Missing values:", missing_count)
print(summary)
print("Skewness:", round(skew_value, 2))
```
```text
Missing values: 1
count    10.000000
mean     45.500000
std      17.500794
min      30.000000
25%      35.250000
50%      41.000000
75%      48.750000
max      90.000000
Name: salary, dtype: float64
Skewness: 2.09
```
Mean (45.5) above median (41) and positive skew agree: a few high salaries pull the data right.
**Likely follow-ups:** 1) *Excel equivalent?* Data Analysis ToolPak "Descriptive Statistics" or functions like AVERAGE, MEDIAN, STDEV.S. 2) *What next?* Investigate outliers and missing values (Q51).
**Common mistakes:** Jumping to modelling without checking missing values and range; trusting the mean alone.

### Q38 ⭐⭐ 🟡 If you add a constant to every value, or multiply every value by a constant, what happens to the mean and standard deviation?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand how shifting and scaling affect centre and spread?
**Say this in the interview:** "Adding a constant shifts the mean by that constant and leaves the standard deviation unchanged. Multiplying by a constant multiplies both the mean and the standard deviation by that constant (by its absolute value for the SD)."
**Explain simply:**
- **Add 5,000 to everyone:** everyone moves up together, so the average rises by 5,000 but the gaps between people stay the same, so SD is unchanged.
- **Give everyone a 10% raise (multiply by 1.1):** the average rises 10% and the gaps stretch by 10%, so SD rises 10% as well.
- Variance gets multiplied by the constant squared.
- This is why a flat raise keeps pay spread equal while a percentage raise widens it.
**Formula in plain words:** New mean = constant x old mean + shift. New SD = |constant| x old SD. In symbols: mean(aX + b) = a x mean(X) + b; SD(aX + b) = |a| x SD(X).
**Worked example:** Salaries 30,000, 40,000, 50,000, 60,000: mean 45,000, SD 12,910. After +5,000: mean 50,000, SD 12,910. After x1.1: mean 49,500, SD 14,201.
**Excel / Python:**
```python
import numpy as np

# Four salaries in rupees
salaries = np.array([30000, 40000, 50000, 60000])

# Same people after a flat raise and after a 10 percent raise
after_flat_raise = salaries + 5000
after_percent_raise = salaries * 1.1

for label, values in [("original", salaries),
                      ("+5000 flat", after_flat_raise),
                      ("x1.1 percent", after_percent_raise)]:
    mean_value = np.mean(values)
    sample_sd = np.std(values, ddof=1)
    print(label, "| mean:", round(mean_value, 2), "| SD:", round(sample_sd, 2))
```
```text
original | mean: 45000.0 | SD: 12909.94
+5000 flat | mean: 50000.0 | SD: 12909.94
x1.1 percent | mean: 49500.0 | SD: 14200.94
```
The flat raise moved the mean but left the SD at 12,909.94; the percent raise changed both by 10%.
**Likely follow-ups:** 1) *What happens to the coefficient of variation?* Unchanged by scaling (Q26). 2) *Converting Celsius to Fahrenheit?* That is multiply plus add: SD only gets the multiplier.
**Common mistakes:** Saying SD rises when you add a constant; forgetting that a negative multiplier does not make SD negative.

### Q39 ⭐⭐ 🟡 The mean of 10 numbers is 50. If one number, 80, is replaced with 20, what is the new mean?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you work from the total, not the average?
**Say this in the interview:** "Mean times count gives the total: 500. Replacing 80 with 20 lowers the total by 60 to 440, and 440 divided by 10 is 44."
**Explain simply:**
- Mean = total divided by count, so total = mean x count.
- Old total = 50 x 10 = 500.
- Change in total = 20 - 80 = -60, so new total = 440.
- The count stays 10, so new mean = 44. Shortcut: the mean falls by 60 / 10 = 6.
**Formula in plain words:** New mean = (old mean x count - old value + new value) / count.
**Worked example:** (50 x 10 - 80 + 20) / 10 = 440 / 10 = 44. In HR terms: 10 employees average 50 training hours; one's record is corrected from 80 to 20 hours, so the team average falls from 50 to 44.
**Excel / Python:**
```python
# Given facts
count_of_numbers = 10
old_mean = 50
old_value = 80
new_value = 20

# Rebuild the total from the mean, swap the value, recompute
old_total = old_mean * count_of_numbers
new_total = old_total - old_value + new_value
new_mean = new_total / count_of_numbers

print("Old total:", old_total)
print("New total:", new_total)
print("New mean:", new_mean)
```
```text
Old total: 500
New total: 440
New mean: 44.0
```
The total dropped from 500 to 440, so the mean fell from 50 to 44.
**Likely follow-ups:** 1) *What if the value were removed instead?* Divide the new total by 9 (Q43 for combined means). 2) *Does the median change?* Possibly, it depends on position.
**Common mistakes:** Computing 50 - 60 = -10 without dividing by 10; forgetting the count.

### Q40 ⭐⭐ 🔴 If the mean of a dataset is greater than its median, what does it say about the shape of the data, and is this always true?
**Asked at:** one candidate report mentions a mean-versus-median skew question at an Indian company (single anecdote, unverified); otherwise commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the rule of thumb and that it has exceptions?
**Say this in the interview:** "Usually mean greater than median suggests right (positive) skew, a long tail of high values. But it is only a rule of thumb: there are datasets where the mean is above the median and the data is actually left-skewed, especially with small or discrete data, so I always look at a histogram."
**Explain simply:**
- Usual story: high outliers pull the mean up and leave the median alone, so mean > median means a right tail.
- The rule holds for many common single-peaked, smooth distributions, but it is not a theorem.
- Counterexamples exist when the two tails are unbalanced in a mixed way (a long thin tail on one side and a heavy block on the other), or the data is discrete with ties at the median.
- Skewness is defined by the third moment, which is a different calculation from mean minus median, so the two can disagree.
- Practical rule: use the comparison as a hint, then confirm with a histogram and the skewness number (Q24).
**Worked example:** The data 1, 4, 6, 6, 8, 10, 10 has mean 6.43 and median 6, so mean is greater than median. Yet its skewness is -0.41 (slightly left-skewed, the longer tail is on the low side).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# A small dataset where the mean is above the median
counterexample_data = [1, 4, 6, 6, 8, 10, 10]

mean_value = np.mean(counterexample_data)
median_value = np.median(counterexample_data)
skewness = stats.skew(counterexample_data)

print("Mean:", round(mean_value, 2))
print("Median:", median_value)
print("Skewness:", round(skewness, 2))
```
```text
Mean: 6.43
Median: 6.0
Skewness: -0.41
```
The mean exceeds the median (6.43 against 6) yet the skewness is negative, so mean above median does not always mean right skew.
**Likely follow-ups:** 1) *Which is the reliable check?* A histogram plus the skewness value. 2) *Does it hold for the normal distribution?* There mean equals median.
**Common mistakes:** Presenting the rule as always true; deciding skew from mean and median alone.

### Q41 ⭐⭐ 🔴 How does the average of group averages differ from the overall average, and when is it wrong to average averages?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question from standard practice.
**What the interviewer is checking:** Whether you remember that groups of different sizes must be weighted.
**Say this in the interview:** "Averaging averages is only right when every group has the same size. Otherwise I weight each group average by its headcount, which is the same as total divided by total."
**Explain simply:**
- A group average hides how many people stand behind it. A 10-person team and a 40-person team should not count equally.
- The overall average is the total of all values divided by the total count.
- Averaging averages is safe only for equal group sizes.
**Formula in plain words:** Overall average = (sum of each group's average times its count) divided by (total count). In symbols: (n1·m1 + n2·m2) / (n1 + n2).
**Worked example:** HR has 10 people averaging 40,000; Sales has 40 people averaging 60,000. The simple average of 40,000 and 60,000 is 50,000, but most employees sit in Sales, so the true company average is 56,000.
**Excel / Python:**
```python
# Average salary and headcount for two departments
hr_headcount = 10
hr_average_salary = 40000
sales_headcount = 40
sales_average_salary = 60000

# Wrong way: simple average of the two group averages
average_of_averages = (hr_average_salary + sales_average_salary) / 2

# Right way: add up all the salary money, then divide by all the people
total_salary_money = hr_headcount * hr_average_salary + sales_headcount * sales_average_salary
total_people = hr_headcount + sales_headcount
overall_average = total_salary_money / total_people

print("Average of averages:", average_of_averages)
print("Overall average    :", overall_average)
```
Output (real run):
```
Average of averages: 50000.0
Overall average    : 56000.0
```
The weighted answer (56,000) leans towards the bigger team; the shortcut (50,000) understates pay by 6,000. In Excel use `=SUMPRODUCT(counts, averages)/SUM(counts)` (any version).
**Likely follow-ups:** 1) *Does the same trap apply to percentages?* Yes (see Q57). 2) *Can you get the overall median from group medians?* No; you need the raw data.
**Common mistakes:** Averaging monthly or departmental averages directly; forgetting this also affects attrition rates by team.

### Q42 ⭐⭐ 🔴 How do different tools (Excel, SQL, Python) calculate percentiles differently, and why can answers differ slightly?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question.
**What the interviewer is checking:** Whether you know a percentile needs a rule when the cut falls between two data points.
**Say this in the interview:** "There is no single definition. Excel's PERCENTILE.INC, pandas and SQL's PERCENTILE_CONT all interpolate between neighbours; PERCENTILE.EXC uses a different position rule; PERCENTILE_DISC returns an actual data value. So small differences are normal, especially on small data."
**Explain simply:**
- The 25th percentile of 8 values lands between two values, so each tool needs a rule to pick a number.
- *Inclusive* (INC, `linear`): position = 1 + p × (n − 1), then interpolate. This is the default in Excel's older `PERCENTILE`, `QUARTILE`, pandas and numpy.
- *Exclusive* (EXC): position = p × (n + 1); gives an error if p is too close to 0 or 1.
- *Discrete* (`PERCENTILE_DISC`): returns a real value from the data, no blending.
- With thousands of rows the methods nearly agree; on small samples they can differ noticeably.
**Worked example:** Eight salaries (in thousands): 20, 25, 30, 35, 40, 50, 70, 120. Inclusive 25th percentile: position 1 + 0.25 × 7 = 2.75, so 25 + 0.75 × (30 − 25) = 28.75.
**Excel / Python:**
```python
import numpy as np

# Eight monthly salaries (in thousands), already sorted
salaries = np.array([20, 25, 30, 35, 40, 50, 70, 120])

# Inclusive method (Excel PERCENTILE.INC, pandas default, SQL PERCENTILE_CONT)
p25_inclusive = np.percentile(salaries, 25, method="linear")
p90_inclusive = round(np.percentile(salaries, 90, method="linear"), 2)

# Exclusive method (Excel PERCENTILE.EXC)
p25_exclusive = np.percentile(salaries, 25, method="weibull")
p90_exclusive = np.percentile(salaries, 90, method="weibull")

# Pick-an-actual-value method (SQL PERCENTILE_DISC, takes the first value reaching 25%)
p25_discrete = np.percentile(salaries, 25, method="inverted_cdf")
p90_discrete = np.percentile(salaries, 90, method="inverted_cdf")

print("25th percentile: inclusive", p25_inclusive, "| exclusive", p25_exclusive, "| discrete", p25_discrete)
print("90th percentile: inclusive", p90_inclusive, "| exclusive", p90_exclusive, "| discrete", p90_discrete)
```
Output (real run):
```
25th percentile: inclusive 28.75 | exclusive 26.25 | discrete 25
90th percentile: inclusive 85.0 | exclusive 120.0 | discrete 120
```
In Excel: `=PERCENTILE.INC(A2:A9, 0.25)` gives 28.75 and `=PERCENTILE.EXC(A2:A9, 0.25)` gives 26.25 (needs Excel 2010+; not run in Excel here, matched by hand and in Python). In SQL: `PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary)` matches the inclusive result; `PERCENTILE_DISC` matches the discrete one (syntax varies by database, not run here).
**Likely follow-ups:** 1) *Which should I use?* State which one you used and stay consistent. 2) *Why does EXC show 120 at the 90th here?* With only 8 points, the exclusive position falls past the last value; numpy caps it at the maximum, while Excel's `PERCENTILE.EXC` returns a #NUM! error for that p.
**Common mistakes:** Assuming two tools must match exactly; mixing methods across a report.

### Q43 ⭐⭐ 🔴 You have the mean and count for two groups. How do you compute the combined mean, and how would you combine their standard deviations?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question.
**What the interviewer is checking:** Whether you know the combined mean is weighted and that SDs cannot simply be averaged.
**Say this in the interview:** "The combined mean is the count-weighted average of the two means. For the SD I rebuild the combined variance: the spread inside each group plus the spread of the group means around the combined mean, then take the square root."
**Explain simply:**
- Combined mean = total of all values divided by total count.
- You cannot average two SDs; the gap between the two group means adds extra spread.
- Variance (SD squared) is what combines properly, so work in variance, then take the root at the end.
**Formula in plain words:** Combined variance = [sum over groups of (n−1)·SD² (spread inside) + sum over groups of n·(group mean − combined mean)² (spread between)] divided by (total n − 1).
**Worked example:** Team A: 30 people, mean score 52, SD 6. Team B: 20 people, mean 60, SD 8. Combined mean 55.2, combined SD about 7.86 (not 7, the plain average of 6 and 8).
**Excel / Python:**
```python
import numpy as np

# Summary numbers we are given for two teams (no raw data)
count_a, mean_a, sd_a = 30, 52.0, 6.0
count_b, mean_b, sd_b = 20, 60.0, 8.0

# Combined mean = weighted by headcount
total_count = count_a + count_b
combined_mean = (count_a * mean_a + count_b * mean_b) / total_count

# Combined variance: spread inside each group, plus spread of group means around the combined mean
within_a = (count_a - 1) * sd_a ** 2
within_b = (count_b - 1) * sd_b ** 2
between_a = count_a * (mean_a - combined_mean) ** 2
between_b = count_b * (mean_b - combined_mean) ** 2
combined_variance = (within_a + within_b + between_a + between_b) / (total_count - 1)
combined_sd = combined_variance ** 0.5

print("Combined mean:", round(combined_mean, 2))
print("Combined SD  :", round(combined_sd, 3))

# Check: build fake raw data with exactly these means and SDs, then pool it
rng = np.random.default_rng(1)
raw_a = rng.normal(size=count_a)
raw_a = (raw_a - raw_a.mean()) / raw_a.std(ddof=1) * sd_a + mean_a
raw_b = rng.normal(size=count_b)
raw_b = (raw_b - raw_b.mean()) / raw_b.std(ddof=1) * sd_b + mean_b
pooled = np.concatenate([raw_a, raw_b])
print("Check from raw data: mean", round(pooled.mean(), 2), "SD", round(pooled.std(ddof=1), 3))
print("Wrong shortcut (average the two SDs):", (sd_a + sd_b) / 2)
```
Output (real run):
```
Combined mean: 55.2
Combined SD  : 7.861
Check from raw data: mean 55.2 SD 7.861
Wrong shortcut (average the two SDs): 7.0
```
The check pools fabricated raw values built to match each team's mean and SD exactly, and it agrees with the formula.
**Likely follow-ups:** 1) *Why not average the SDs?* It ignores that the groups centre in different places. 2) *Can you combine medians?* No, not from summaries.
**Common mistakes:** Averaging SDs; mixing n and n−1 (population vs sample SD) between groups.

### Q44 ⭐ 🟡 What is a trimmed mean, and when would you use it?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Knowledge of a middle path between the mean and the median.
**Say this in the interview:** "A trimmed mean drops a fixed percentage of the lowest and highest values, then averages the rest. I use it when a few extreme values distort the mean but I still want to use most of the data."
**Explain simply:**
- Sort the values, cut, say, 10% from each end, and average what remains.
- It sits between the mean (trim 0%) and the median (trim almost 50%).
- Useful for salary, tenure or time-to-hire data with a few extremes.
**Worked example:** Ten salaries (thousands): nine between 30 and 48 plus a director at 300. The mean is 64.6, which describes nobody. Dropping the lowest and highest leaves a trimmed mean of 39.5, close to the median 39.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Ten monthly salaries in thousands; the last one is a director
salaries = np.array([30, 32, 35, 36, 38, 40, 42, 45, 48, 300])

# Ordinary mean
plain_mean = salaries.mean()

# Trimmed mean: drop the lowest 10% and highest 10% (1 value each end), average the rest
trimmed_mean = stats.trim_mean(salaries, proportiontocut=0.10)

# Same thing by hand
sorted_salaries = np.sort(salaries)
middle_values = sorted_salaries[1:-1]
manual_trimmed_mean = middle_values.mean()

print("Plain mean  :", plain_mean)
print("Trimmed mean:", trimmed_mean)
print("By hand     :", manual_trimmed_mean)
print("Median      :", np.median(salaries))
```
Output (real run):
```
Plain mean  : 64.6
Trimmed mean: 39.5
By hand     : 39.5
Median      : 39.0
```
In Excel: `=TRIMMEAN(A2:A11, 0.2)` trims 20% in total (10% each end, so 1 value from each end here) and returns 39.5 (available in all modern versions; not run in Excel here). Note Excel's percentage is the total cut, scipy's is per end.
**Likely follow-ups:** 1) *How much should I trim?* 5-20% is common; say what you chose. 2) *Why not just use the median?* The trimmed mean uses more of the data.
**Common mistakes:** Confusing Excel's total-cut percentage with scipy's per-side one; trimming without telling the audience.

### Q45 ⭐ 🟡 What are the geometric mean and harmonic mean, and when is each appropriate?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Whether you can choose the right average for growth rates and for rates per unit.
**Say this in the interview:** "The geometric mean is for things that multiply, like growth rates over several years. The harmonic mean is for averaging rates such as speed, where the same amount of work is done at each rate."
**Explain simply:**
- Geometric mean: multiply the growth factors, then take the n-th root. It gives the one steady rate that reaches the same end result.
- Harmonic mean: n divided by the sum of 1/value. It suits "per hour" or "per unit" rates over equal amounts of work.
- The simple (arithmetic) mean overstates both cases.
**Formula in plain words:** Geometric mean = (product of the factors) raised to 1/n. Harmonic mean = n ÷ (1/x1 + 1/x2 + ...).
**Worked example:** Headcount grows 10%, then 20%, then falls 15%. Starting at 1,000 it ends at 1,122. The geometric mean rate is 3.912% a year; the simple average of the rates would say 5.0% and overshoot to 1,157.6. A recruiter screens 10 CVs/hour one week and 20 CVs/hour the next, same CV count each week: the true average is 13.33, not 15.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Headcount grew 10%, then 20%, then fell 15% over three years
growth_factors = np.array([1.10, 1.20, 0.85])

# Arithmetic mean of the growth rates (misleading)
arithmetic_mean_rate = growth_factors.mean() - 1

# Geometric mean: the single yearly rate that gives the same end result
geometric_mean_rate = stats.gmean(growth_factors) - 1

start_headcount = 1000
end_headcount = start_headcount * growth_factors.prod()
rebuilt_with_geometric = start_headcount * (1 + geometric_mean_rate) ** 3
rebuilt_with_arithmetic = start_headcount * (1 + arithmetic_mean_rate) ** 3

print("Real end headcount          :", round(end_headcount, 1))
print("Geometric mean rate         :", round(geometric_mean_rate * 100, 3), "%")
print("Rebuilt with geometric rate :", round(rebuilt_with_geometric, 1))
print("Rebuilt with arithmetic rate:", round(rebuilt_with_arithmetic, 1))

# Harmonic mean: a recruiter screens 10 CVs/hour in week 1 and 20 CVs/hour in week 2, same number of CVs each week
speeds = np.array([10, 20])
harmonic_speed = stats.hmean(speeds)
print("Average screening speed (harmonic):", round(harmonic_speed, 2), "CVs per hour")
print("Simple mean would wrongly say      :", speeds.mean())
```
Output (real run):
```
Real end headcount          : 1122.0
Geometric mean rate         : 3.912 %
Rebuilt with geometric rate : 1122.0
Rebuilt with arithmetic rate: 1157.6
Average screening speed (harmonic): 13.33 CVs per hour
Simple mean would wrongly say      : 15.0
```
In Excel: `=GEOMEAN(B2:B4)` and `=HARMEAN(B2:B4)` (all versions; not run in Excel here).
**Likely follow-ups:** 1) *Can the geometric mean handle zero or negatives?* No; factors must be positive. 2) *Which is largest?* Arithmetic ≥ geometric ≥ harmonic.
**Common mistakes:** Averaging percentage growth rates arithmetically; using the harmonic mean when time, not work, is the equal part.

### Q46 ⭐ 🟡 What is the standard error, and how is it different from standard deviation?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Whether you separate "spread of people" from "uncertainty in the average".
**Say this in the interview:** "Standard deviation says how much individual values vary. Standard error says how much the sample average would vary if I repeated the survey. It equals the SD divided by the square root of the sample size, so more data makes the average more precise, but does not shrink the people's spread."
**Explain simply:**
- SD describes the data: how far employees differ from each other.
- SE describes the estimate: how far my sample mean might be from the true mean.
- Quadrupling the sample size halves the SE.
**Formula in plain words:** Standard error of the mean = sample SD divided by the square root of n. In symbols: s / √n.
**Worked example:** A company of 400 has engagement scores with SD 12. Surveying 36 people gives an expected SE of 12/6 = 2. In the sample below the survey SD came out at 10.03, giving SE 1.67; repeating the survey 5,000 times shows the averages really do vary by about 1.77 (close to 2; sampling from a small company also shaves it a little).
**Excel / Python:**
```python
import numpy as np

rng = np.random.default_rng(7)

# Engagement scores of 400 employees (our pretend whole company)
company_scores = rng.normal(loc=70, scale=12, size=400)

# One survey sample of 36 employees
survey_sample = rng.choice(company_scores, size=36, replace=False)
sample_sd = survey_sample.std(ddof=1)
standard_error = sample_sd / np.sqrt(len(survey_sample))

# Repeat the survey 5000 times and see how much the sample averages themselves vary
sample_means = []
for _ in range(5000):
    one_sample = rng.choice(company_scores, size=36, replace=False)
    sample_means.append(one_sample.mean())
spread_of_sample_means = np.std(sample_means, ddof=1)

print("SD of the 36 scores (spread of people):", round(sample_sd, 2))
print("Standard error from formula            :", round(standard_error, 2))
print("Formula using true company SD 12 :", round(12 / np.sqrt(36), 2))
print("SD of 5000 repeated sample means       :", round(spread_of_sample_means, 2))
```
Output (real run):
```
SD of the 36 scores (spread of people): 10.03
Standard error from formula            : 1.67
Formula using true company SD 12 : 2.0
SD of 5000 repeated sample means       : 1.77
```
In Excel: `=STDEV.S(A2:A37)/SQRT(COUNT(A2:A37))` (Excel 2010+; not run in Excel here).
**Likely follow-ups:** 1) *Which goes in a confidence interval?* The SE. 2) *Does a bigger sample reduce SD?* No, it only makes SD more accurately estimated.
**Common mistakes:** Reporting SE as if it were the spread of employees; forgetting the square root.

### Q47 ⭐ 🟡 What is kurtosis, and what does a high value tell an analyst about the data?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Whether you know kurtosis is about tail weight (extremes), not "peakedness" alone.
**Say this in the interview:** "Kurtosis measures how heavy the tails are compared with a normal curve. High (positive excess) kurtosis means extreme values are more common than a normal distribution would predict, so SD-based thinking understates the risk of outliers."
**Explain simply:**
- Excess kurtosis subtracts 3, so a normal distribution scores 0.
- Positive: heavy tails, more extremes (fat-tailed). Negative: light tails, fewer extremes.
- It matters when you set alerts or limits: with high kurtosis, "3 SD" events happen more often than 0.3% of the time.
**Worked example:** Two sets of 5,000 monthly overtime changes, both with SD 10. The normal set has excess kurtosis about −0.07 and 10 values beyond 3 SD; the heavy-tailed set has about 2.92 and 53 such values, five times more extremes despite the same SD.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(3)

# Two sets of 5000 monthly overtime changes with the same mean (0) and SD (10)
normal_data = rng.normal(loc=0, scale=10, size=5000)
heavy_tail_raw = rng.standard_t(df=5, size=5000)
heavy_tail_data = heavy_tail_raw / heavy_tail_raw.std() * 10

# Excess kurtosis: 0 means "like a normal bell curve"
print("Normal      : SD", round(normal_data.std(), 2), "excess kurtosis", round(stats.kurtosis(normal_data), 2))
print("Heavy-tailed: SD", round(heavy_tail_data.std(), 2), "excess kurtosis", round(stats.kurtosis(heavy_tail_data), 2))

# How many values lie more than 3 SD from the mean?
extreme_normal = (np.abs(normal_data) > 30).sum()
extreme_heavy = (np.abs(heavy_tail_data) > 30).sum()
print("Values beyond 3 SD: normal", extreme_normal, "| heavy-tailed", extreme_heavy)
```
Output (real run):
```
Normal      : SD 10.06 excess kurtosis -0.07
Heavy-tailed: SD 10.0 excess kurtosis 2.92
Values beyond 3 SD: normal 10 | heavy-tailed 53
```
In Excel: `=KURT(A2:A5001)` returns sample excess kurtosis (all versions; not run in Excel here).
**Likely follow-ups:** 1) *Is kurtosis the same as peakedness?* Not reliably; it is tail weight. 2) *What would you do with a high value?* Check outliers and prefer robust measures (median, IQR).
**Common mistakes:** Forgetting whether a tool reports kurtosis or excess kurtosis (Excel and pandas report excess; some tools add 3).

### Q48 ⭐ 🟡 What is a decile, and when would a business report deciles instead of quartiles?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Whether you can link a stats term to a business use.
**Say this in the interview:** "Deciles split sorted data into ten equal-sized groups, with cut points at the 10th, 20th, up to the 90th percentile. A business uses them when four groups are too coarse, for example pay bands, performance rating curves or customer value tiers."
**Explain simply:**
- Quartiles give 4 slices (25% each); deciles give 10 slices (10% each).
- D1 is the 10th percentile, D5 is the median, D9 is the 90th percentile.
- Useful to see the tails: "top 10%" and "bottom 10%" of earners.
**Worked example:** For 200 simulated salaries the decile cut points rise from 19.3 (D1) to 67.6 (D9) thousand; the top 10% of people earn 20.6% of total pay, which shows skew that quartiles would blur.
**Excel / Python:**
```python
import numpy as np

rng = np.random.default_rng(11)

# 200 monthly salaries (in thousands), right-skewed like real pay
salaries = np.round(rng.lognormal(mean=3.6, sigma=0.5, size=200), 1)

# Decile cut points: 10th, 20th ... 90th percentile
decile_points = np.percentile(salaries, np.arange(10, 100, 10))
for decile_number, cut_point in zip(range(1, 10), decile_points):
    print("D" + str(decile_number), "=", round(cut_point, 1))

# Share of total pay going to the top 10% of earners
top_cut = np.percentile(salaries, 90)
top_decile_pay = salaries[salaries > top_cut].sum()
share_of_pay = top_decile_pay / salaries.sum()
print("Top 10% of people earn", round(share_of_pay * 100, 1), "% of total pay")
```
Output (real run):
```
D1 = 19.3
D2 = 25.2
D3 = 28.7
D4 = 33.1
D5 = 37.0
D6 = 43.0
D7 = 48.0
D8 = 53.2
D9 = 67.6
Top 10% of people earn 20.6 % of total pay
```
In Excel: `=PERCENTILE.INC(A2:A201, 0.9)` for D9 (2010+; not run in Excel here).
**Likely follow-ups:** 1) *Is D5 the median?* Yes. 2) *Deciles vs percentiles?* Deciles are every tenth percentile.
**Common mistakes:** Calling the 10 groups "deciles" when they are the 9 cut points; unequal group sizes when ties exist.

### Q49 ⭐ 🟡 What is the Tukey fence, and why is the multiplier 1.5?
**Asked at:** commonly asked; IQR-based outlier detection was reported as a live Python question on Glassdoor (candidate report snippet in `research/Book05_Part02_sources.md`, company not stated).
**What the interviewer is checking:** Whether you know the outlier rule and that 1.5 is a convention with a reason.
**Say this in the interview:** "A Tukey fence flags points below Q1 minus 1.5 times the IQR or above Q3 plus 1.5 times the IQR. The 1.5 was chosen by John Tukey as a practical balance: on perfectly bell-shaped data it flags only about 0.7% of points, so flagged points are worth a look."
**Explain simply:**
- IQR (interquartile range) = Q3 − Q1, the spread of the middle 50%.
- Fences: lower = Q1 − 1.5 × IQR, upper = Q3 + 1.5 × IQR. Beyond them is a "suspect outlier".
- 3 × IQR is sometimes used for "far out" points.
- The 1.5 is a convention, not a law of nature; on normal data the fences sit at about ±2.7 SD.
**Worked example:** Notice periods in days: 30, 30, 45, 45, 60, 60, 60, 75, 90, 180. Q1 = 45, Q3 = 71.25, IQR = 26.25, fences 5.6 and 110.6. Only 180 is flagged.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Part 1: the 1.5 multiplier on a perfect bell curve with SD = 1
q1 = stats.norm.ppf(0.25)
q3 = stats.norm.ppf(0.75)
iqr = q3 - q1
upper_fence = q3 + 1.5 * iqr
share_flagged = 2 * (1 - stats.norm.cdf(upper_fence))
print("IQR =", round(iqr, 3), "SDs | upper fence =", round(upper_fence, 3), "SDs")
print("Share of normal data flagged as outliers:", round(share_flagged * 100, 2), "%")
for multiplier in [1.0, 1.5, 3.0]:
    fence = q3 + multiplier * iqr
    flagged = 2 * (1 - stats.norm.cdf(fence))
    print("multiplier", multiplier, "-> flags", round(flagged * 100, 3), "%")

# Part 2: a small HR example, notice period in days
notice_days = np.array([30, 30, 45, 45, 60, 60, 60, 75, 90, 180])
q1_days, q3_days = np.percentile(notice_days, [25, 75])
iqr_days = q3_days - q1_days
lower = q1_days - 1.5 * iqr_days
upper = q3_days + 1.5 * iqr_days
print("Q1", q1_days, "Q3", q3_days, "IQR", iqr_days, "fences", lower, upper)
print("Outliers:", notice_days[(notice_days < lower) | (notice_days > upper)])
```
Output (real run):
```
IQR = 1.349 SDs | upper fence = 2.698 SDs
Share of normal data flagged as outliers: 0.7 %
multiplier 1.0 -> flags 4.302 %
multiplier 1.5 -> flags 0.698 %
multiplier 3.0 -> flags 0.0 %
Q1 45.0 Q3 71.25 IQR 26.25 fences 5.625 110.625
Outliers: [180]
```
In Excel, with Q1 in D1 and Q3 in D2: `=D2+1.5*(D2-D1)` for the upper fence (use `QUARTILE.INC`, 2010+; not run in Excel here).
**Likely follow-ups:** 1) *Should I delete flagged points?* No, investigate first. 2) *Why not z-scores?* Mean and SD are themselves distorted by outliers.
**Common mistakes:** Treating flagged values as errors automatically; using the rule on tiny samples.

### Q50 ⭐ 🟡 What is the mode of continuous data, and how do you estimate it from a histogram?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Whether you see that exact repeats are rare in continuous data, so the mode must be estimated.
**Say this in the interview:** "With continuous values like tenure in months, almost no two values are identical, so the raw mode is meaningless. I bin the data into a histogram, find the tallest bar (the modal class), and refine it with a formula or read the peak of a smoothed curve."
**Explain simply:**
- Make a histogram with sensible bin widths; the tallest bar is the modal class.
- Refine using neighbouring bars: mode ≈ lower edge + width × (f1 − f0) / (2·f1 − f0 − f2), where f1 is the tallest bar and f0, f2 are the bars either side.
- Or fit a smooth curve (kernel density estimate) and read the peak.
- The answer depends on bin width, so say what you used.
**Worked example:** 500 simulated tenure values (months): tallest bar 16-24 (104 people). The formula gives 23.5; the smooth curve peaks at 24.1; the true mode used to generate the data is 24. The mean (32.8) and median (31.0) sit higher because of a right tail.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(5)

# 500 tenure values in months: continuous, so almost no two are exactly equal
tenure_months = rng.gamma(shape=4, scale=8, size=500)

# Step 1: bin the data with width 8 and find the tallest bar
bin_edges = np.arange(0, 120, 8)
counts, edges = np.histogram(tenure_months, bins=bin_edges)
tallest = counts.argmax()
modal_class = (int(edges[tallest]), int(edges[tallest + 1]))
print("Tallest bar covers", modal_class, "with", counts[tallest], "people")

# Step 2: refine inside the bar using the neighbouring bar heights
f0 = counts[tallest - 1]
f1 = counts[tallest]
f2 = counts[tallest + 1]
bar_width = 8
mode_estimate = edges[tallest] + (f1 - f0) / (2 * f1 - f0 - f2) * bar_width
print("Mode from histogram formula:", round(mode_estimate, 1))

# Step 3: smooth curve (kernel density) peak
smooth_curve = stats.gaussian_kde(tenure_months)
grid = np.linspace(0, 100, 1001)
kde_peak = grid[smooth_curve(grid).argmax()]
print("Mode from smooth curve     :", round(kde_peak, 1))
print("Mean and median            :", round(tenure_months.mean(), 1), round(np.median(tenure_months), 1))
print("True mode of this gamma is (shape-1)*scale =", (4 - 1) * 8)
```
Output (real run):
```
Tallest bar covers (16, 24) with 104 people
Mode from histogram formula: 23.5
Mode from smooth curve     : 24.1
Mean and median            : 32.8 31.0
True mode of this gamma is (shape-1)*scale = 24
```
In Excel, build the histogram with `FREQUENCY` or the Histogram chart, then read the tallest bin.
**Likely follow-ups:** 1) *Why does bin width matter?* Wide bins blur, narrow bins are noisy. 2) *Can there be two modes?* Yes (Q59).
**Common mistakes:** Using `MODE` on decimals and getting an error or a meaningless value.

### Q51 ⭐ 🟡 How do you handle missing values when calculating summary statistics, and how does it change the mean?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Whether you choose a treatment deliberately rather than letting the tool decide.
**Say this in the interview:** "First I count how many are missing and ask why. Most tools skip blanks, so the mean is of the answers received. Treating blanks as zero drags the mean down badly. Filling with the mean or median keeps the average but understates the spread."
**Explain simply:**
- Skipping missing values (pandas and Excel `AVERAGE` default): fine if missing at random.
- Zero-filling: only right if a blank truly means zero (for example no overtime).
- Median/mean fill: keeps the average, shrinks SD, and fakes precision.
- If the people who did not answer differ (say, disengaged staff skip the survey), every option is biased; report the response rate.
**Worked example:** Engagement scores for 8 employees, 2 blank: the mean of the 6 answers is 7.5. Blanks as zero gives 5.625. Median-fill keeps 7.5, but the SD drops from 1.05 to 0.89.
**Excel / Python:**
```python
import numpy as np
import pandas as pd

# Engagement scores for 8 employees; two did not answer
survey = pd.DataFrame({
    "employee": ["A", "B", "C", "D", "E", "F", "G", "H"],
    "engagement": [8, 7, np.nan, 9, 6, np.nan, 8, 7],
})

# Option 1: pandas skips blanks by default
mean_skipping_blanks = survey["engagement"].mean()

# Option 2: wrongly treat blanks as zero
mean_blanks_as_zero = survey["engagement"].fillna(0).mean()

# Option 3: fill blanks with the median of the answers (keeps the mean, shrinks the spread)
median_answer = survey["engagement"].median()
filled_with_median = survey["engagement"].fillna(median_answer)

print("Answers given:", survey["engagement"].count(), "of", len(survey))
print("Mean skipping blanks:", round(mean_skipping_blanks, 2))
print("Mean with blanks as 0:", mean_blanks_as_zero)
print("Mean after median fill:", round(filled_with_median.mean(), 2))
print("SD skipping blanks:", round(survey["engagement"].std(), 2), "| SD after median fill:", round(filled_with_median.std(), 2))
```
Output (real run):
```
Answers given: 6 of 8
Mean skipping blanks: 7.5
Mean with blanks as 0: 5.625
Mean after median fill: 7.5
SD skipping blanks: 1.05 | SD after median fill: 0.89
```
In Excel, `=AVERAGE(B2:B9)` ignores truly empty cells, and `COUNT` vs `ROWS` tells you how many are missing (all versions; not run in Excel here). Cells containing 0 or "NA" text behave differently.
**Likely follow-ups:** 1) *When to drop rows?* When few are missing and random. 2) *When to impute?* When many are missing and you need the full table, and you document it.
**Common mistakes:** Silent zero-filling; not reporting the number missing.

### Q52 ⭐ 🔴 Why do two datasets with identical mean, median and standard deviation sometimes look completely different (Anscombe's quartet)?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Whether you know summary numbers can hide shape, so you should always plot the data.
**Say this in the interview:** "Summary statistics compress a whole dataset into a few numbers, and many different shapes share the same numbers. Anscombe's quartet has four datasets with nearly identical means, SDs and correlation, yet one is a line, one a curve, and one dominated by a single extreme point. So I always plot before trusting summaries."
**Explain simply:**
- Anscombe (1973) built four small datasets of 11 points each to prove the point.
- Mean of y is 7.5 and SD about 2.03 in all four; the correlation is about 0.816.
- Plots show a straight line, a curve, a line with one outlier, and a vertical stack with one far point.
- Habit to build: chart first, then summarise.
**Worked example:** The code below uses sets I, II and IV from the published data; the three print the same summary numbers. (Set III, the line with one outlier, shares them too.)
**Excel / Python:**
```python
import numpy as np

# Anscombe's quartet, sets I and II (published data)
x_values = np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], dtype=float)
y_set_one = np.array([8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68])
y_set_two = np.array([9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74])
x_set_four = np.array([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], dtype=float)
y_set_four = np.array([6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89])

def describe(label, x, y):
    correlation = np.corrcoef(x, y)[0, 1]
    print(label, "| mean y", round(y.mean(), 2), "| SD y", round(y.std(ddof=1), 2),
          "| mean x", round(x.mean(), 2), "| correlation", round(correlation, 3))

describe("Set I  (straight-line scatter)", x_values, y_set_one)
describe("Set II (a smooth curve)      ", x_values, y_set_two)
describe("Set IV (one extreme point)   ", x_set_four, y_set_four)
```
Output (real run):
```
Set I  (straight-line scatter) | mean y 7.5 | SD y 2.03 | mean x 9.0 | correlation 0.816
Set II (a smooth curve)       | mean y 7.5 | SD y 2.03 | mean x 9.0 | correlation 0.816
Set IV (one extreme point)    | mean y 7.5 | SD y 2.03 | mean x 9.0 | correlation 0.817
```
A scatter chart in Excel (Insert > Scatter) would show the very different shapes.
**Likely follow-ups:** 1) *What would you do in practice?* Plot histograms and scatters before modelling. 2) *Is there a modern version?* The "Datasaurus Dozen" makes the same point (from memory, not verified here).
**Common mistakes:** Trusting a correlation coefficient without a scatter plot.

### Q53 ⭐ 🔴 Why is variance additive for independent variables but standard deviation is not?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Whether you understand the maths of combining spread.
**Say this in the interview:** "For independent variables, variances add: Var(X+Y) = Var(X) + Var(Y). Standard deviation is the square root of variance, and a square root of a sum is not the sum of square roots, so SDs combine like the sides of a right-angled triangle: SD of the total = square root of (SD1² + SD2²)."
**Explain simply:**
- Independent means one does not tell you anything about the other, so their ups and downs partly cancel.
- Because they partly cancel, the total spread is less than the sum of the two SDs.
- If they are not independent, you must add a covariance term.
**Formula in plain words:** Variance of the total = variance of X + variance of Y (independent). SD of the total = square root of that sum.
**Worked example:** Hiring time = screening hours (SD 3) + interview hours (SD 4), independent. Variances 9 and 16 add to 25, so the total SD is 5, not 7.
**Excel / Python:**
```python
import numpy as np

rng = np.random.default_rng(2)

# Two independent things: hours spent on screening (SD 3) and on interviews (SD 4)
screening_hours = rng.normal(loc=10, scale=3, size=1_000_000)
interview_hours = rng.normal(loc=20, scale=4, size=1_000_000)
total_hours = screening_hours + interview_hours

print("Variance: screening", round(screening_hours.var(), 2), "| interviews", round(interview_hours.var(), 2),
      "| total", round(total_hours.var(), 2))
print("SD: screening", round(screening_hours.std(), 2), "| interviews", round(interview_hours.std(), 2),
      "| total", round(total_hours.std(), 2))
print("Sum of SDs would be 7; correct SD is sqrt(9 + 16) =", (9 + 16) ** 0.5)
```
Output (real run):
```
Variance: screening 9.0 | interviews 15.99 | total 24.98
SD: screening 3.0 | interviews 4.0 | total 5.0
Sum of SDs would be 7; correct SD is sqrt(9 + 16) = 5.0
```
A simulation of a million cases lands on 5 (tiny differences from 9 and 16 are sampling noise).
**Likely follow-ups:** 1) *What if they are correlated?* Add 2 × covariance. 2) *Does the same hold for differences X − Y?* Yes, variances still add.
**Common mistakes:** Adding SDs; subtracting variances for X − Y.

### Q54 ⭐ 🔴 What is the median absolute deviation (MAD), and why is it a more robust spread measure than standard deviation?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Knowledge of robust statistics.
**Say this in the interview:** "MAD is the median of how far each value is from the median. Because it uses medians, a few extreme values barely move it, while the standard deviation squares every distance, so one outlier inflates it enormously."
**Explain simply:**
- Step 1: find the median. Step 2: take each value's distance from it. Step 3: the median of those distances is the MAD.
- Multiply by 1.4826 to make it comparable to SD on bell-shaped data ("scaled MAD").
- Robust: up to nearly half the data can be extreme before MAD breaks.
**Worked example:** Days to hire for 9 roles: 28, 30, 31, 33, 35, 36, 38, 40, 200. The SD is 55.5, driven by the 200-day role. MAD is 4, scaled 5.93, which describes the typical roles. Without the extreme role the SD drops to 4.12 while the scaled MAD barely moves (5.19).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Days taken to hire for 9 roles; the last one is a stuck senior role
days_to_hire = np.array([28, 30, 31, 33, 35, 36, 38, 40, 200])

# Standard deviation (sample)
standard_deviation = days_to_hire.std(ddof=1)

# MAD: median of the distances from the median
median_days = np.median(days_to_hire)
distances_from_median = np.abs(days_to_hire - median_days)
mad = np.median(distances_from_median)

# Scaled MAD, comparable to SD for bell-shaped data
scaled_mad = 1.4826 * mad

print("Median:", median_days)
print("Distances from median:", distances_from_median)
print("MAD:", mad, "| scaled MAD:", round(scaled_mad, 2))
print("Standard deviation:", round(standard_deviation, 2))
print("scipy check:", round(stats.median_abs_deviation(days_to_hire, scale="normal"), 2))

# Same data without the extreme role
without_extreme = days_to_hire[:-1]
print("SD without it:", round(without_extreme.std(ddof=1), 2),
      "| scaled MAD without it:", round(stats.median_abs_deviation(without_extreme, scale="normal"), 2))
```
Output (real run):
```
Median: 35.0
Distances from median: [  7.   5.   4.   2.   0.   1.   3.   5. 165.]
MAD: 4.0 | scaled MAD: 5.93
Standard deviation: 55.51
scipy check: 5.93
SD without it: 4.12 | scaled MAD without it: 5.19
```
In Excel, MAD needs a helper column: put `=ABS(A2-MEDIAN($A$2:$A$10))` down a column, then `=MEDIAN(B2:B10)` (all versions; not run in Excel here). Do not confuse it with Excel's `AVEDEV`, which is a different (mean absolute deviation) measure.
**Likely follow-ups:** 1) *Why 1.4826?* It makes MAD match the SD for normal data. 2) *When is MAD worse?* It is less efficient on clean normal data.
**Common mistakes:** Confusing median absolute deviation with mean absolute deviation.

### Q55 ⭐ 🔴 Is the sample standard deviation an unbiased estimator of the population standard deviation, even though sample variance is unbiased?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Depth on estimator properties; premise check.
**Say this in the interview:** "No. Dividing by n−1 makes the sample variance unbiased, but the square root is a curved function, so the sample SD is slightly too small on average. The bias is small for large samples and noticeable for very small ones."
**Explain simply:**
- Unbiased means the estimate is right on average over many samples.
- Variance with n−1 is right on average. The root of an average is not the average of roots (Jensen's inequality: for a concave function like the square root, the average of the root is below the root of the average).
- For n = 5 the sample SD averages about 94% of the true SD. A correction factor (c4) exists but is rarely used in practice.
**Worked example:** Draw 400,000 samples of 5 from a population with SD exactly 10. The sample variances average 99.95 (about 100, unbiased). The sample SDs average 9.40, below 10.
**Excel / Python:**
```python
import numpy as np

rng = np.random.default_rng(42)
true_sd = 10.0
sample_size = 5
number_of_samples = 400_000

# Draw many small samples of 5 from a population whose true SD is exactly 10
samples = rng.normal(loc=50, scale=true_sd, size=(number_of_samples, sample_size))

# Sample variance with n-1 and sample SD, for every sample
sample_variances = samples.var(axis=1, ddof=1)
sample_sds = samples.std(axis=1, ddof=1)

print("True variance:", true_sd ** 2, "| average of sample variances:", round(sample_variances.mean(), 2))
print("True SD      :", true_sd, "| average of sample SDs      :", round(sample_sds.mean(), 2))
print("Theory for n=5: average SD is about 0.94 x true SD =", round(0.94 * true_sd, 2))
```
Output (real run):
```
True variance: 100.0 | average of sample variances: 99.95
True SD      : 10.0 | average of sample SDs      : 9.4
Theory for n=5: average SD is about 0.94 x true SD = 9.4
```
The two averages show the contrast: variance is right on average, SD is not. In practice analysts still use `STDEV.S` (Excel 2010+; not run here); the bias is negligible beyond about 30 values.
**Likely follow-ups:** 1) *Why n−1?* We estimate the mean from the same data, which uses up one degree of freedom. 2) *Does it matter in practice?* Rarely.
**Common mistakes:** Claiming "n−1 makes everything unbiased".

### Q56 ⭐ 🔴 How would you compute a running mean and running standard deviation for a stream of data without storing every value?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Algorithmic thinking and awareness of numerical stability.
**Say this in the interview:** "I keep three numbers: the count, the running mean and a running sum of squared gaps. For each new value I update them (Welford's algorithm), and the SD comes from the sum of squared gaps divided by n−1. The sum-of-squares shortcut can lose accuracy on large numbers, so I prefer Welford."
**Explain simply:**
- Only three numbers are stored, however long the stream.
- New mean = old mean + (new value − old mean) / count.
- Update the squared-gap total with (new value − old mean) × (new value − new mean).
- Handy for daily attendance feeds or live ticket counts.
**Worked example:** Eight daily attendance counts; the final running mean 214.125 and SD 10.629 match the usual full-data calculation.
**Excel / Python:**
```python
import numpy as np

# Welford's method: keep only a count, a running mean and a running sum of squared gaps
count = 0
running_mean = 0.0
sum_of_squared_gaps = 0.0

daily_attendance_counts = [212, 205, 220, 198, 230, 215, 208, 225]

for new_value in daily_attendance_counts:
    count = count + 1
    gap_before = new_value - running_mean
    running_mean = running_mean + gap_before / count
    gap_after = new_value - running_mean
    sum_of_squared_gaps = sum_of_squared_gaps + gap_before * gap_after

    if count > 1:
        running_sd = (sum_of_squared_gaps / (count - 1)) ** 0.5
    else:
        running_sd = 0.0
    print("after", count, "values: mean", round(running_mean, 3), "SD", round(running_sd, 3))

print("Check with numpy: mean", round(np.mean(daily_attendance_counts), 3),
      "SD", round(np.std(daily_attendance_counts, ddof=1), 3))
```
Output (real run):
```
after 1 values: mean 212.0 SD 0.0
after 2 values: mean 208.5 SD 4.95
after 3 values: mean 212.333 SD 7.506
after 4 values: mean 208.75 SD 9.43
after 5 values: mean 213.0 SD 12.53
after 6 values: mean 213.333 SD 11.237
after 7 values: mean 212.571 SD 10.454
after 8 values: mean 214.125 SD 10.629
Check with numpy: mean 214.125 SD 10.629
```
Each line shows the stats updated after one more value; the last line matches numpy.
**Likely follow-ups:** 1) *Why not store sum and sum of squares?* Subtracting two huge numbers can lose precision. 2) *Can it do the median?* Not exactly; that needs approximate methods.
**Common mistakes:** Dividing by n instead of n−1 for sample SD; forgetting the first value has no SD.

### Q57 ⭐ 🔴 Why can the average of ratios (like a mean of per-store conversion rates) differ from the overall ratio, and which is right?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question.
**What the interviewer is checking:** Whether you weight ratios by their denominators.
**Say this in the interview:** "The average of ratios gives every store equal weight, even a tiny one. The overall ratio, total orders over total visitors, weights each store by its volume. For one company-wide figure the overall ratio is normally right; the average of ratios is right only if I truly want 'the typical store'."
**Explain simply:**
- Each ratio has its own denominator; averaging ratios ignores them.
- Same trap as averaging averages (Q41), and a form of Simpson's paradox when groups differ in size.
- Pick by the question: "how does the business do?" (overall) or "how does a typical store do?" (average of ratios).
**Worked example:** Three stores: 30/100, 80/400 and 500/5,000 orders per visitors. The average of the rates is 20.00%; the overall rate is 610/5,500 = 11.09%. Most visitors are at the large, weaker store.
**Excel / Python:**
```python
import pandas as pd

# Conversion = orders / visitors, for three stores
stores = pd.DataFrame({
    "store": ["Small", "Medium", "Large"],
    "visitors": [100, 400, 5000],
    "orders": [30, 80, 500],
})
stores["conversion_rate"] = stores["orders"] / stores["visitors"]

# Average of the three rates (treats every store as equal)
average_of_rates = stores["conversion_rate"].mean()

# Overall rate: total orders / total visitors
overall_rate = stores["orders"].sum() / stores["visitors"].sum()

print(stores)
print("Average of rates:", round(average_of_rates * 100, 2), "%")
print("Overall rate    :", round(overall_rate * 100, 2), "%")
```
Output (real run):
```
    store  visitors  orders  conversion_rate
0   Small       100      30              0.3
1  Medium       400      80              0.2
2   Large      5000     500              0.1
Average of rates: 20.0 %
Overall rate    : 11.09 %
```
Excel: `=SUM(orders)/SUM(visitors)` for overall, `=AVERAGE(rates)` for the other (all versions; not run in Excel here). The same applies to attrition rates by department.
**Likely follow-ups:** 1) *Which would you show leadership?* The overall rate, plus the per-store breakdown. 2) *What about Power BI?* Build the ratio as a measure (sum / sum), not by averaging a column of ratios.
**Common mistakes:** Averaging a ratio column in a pivot table.

### Q58 ⭐ 🔴 Is the 90th percentile of response time a better SLA measure than the mean? Explain with an example.
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Whether you understand skewed service-time data and promises in terms of "most users".
**Say this in the interview:** "Yes, usually. Response times are right-skewed: most are fast and a few are very slow. The mean is dragged by the slow ones and describes almost no real ticket. A 90th-percentile SLA says 9 out of 10 are done within X hours, which is something a user can actually experience and a team can be held to. I would still watch the worst cases separately."
**Explain simply:**
- Percentile SLA: "90% of tickets resolved within X hours".
- The mean mixes fast and slow tickets into a number few experience.
- A percentile ignores the exact size of the worst 10%, so also track the 99th percentile or the maximum.
**Worked example:** 20 HR helpdesk tickets (hours): most 1-8, two outliers at 40 and 72. The mean is 8.65 hours and the median 3. Yet the 90th percentile is 11.2 hours: the promise "90% within 11.2 hours" is concrete, and the mean (8.65) is higher than 18 of the 20 tickets.
**Excel / Python:**
```python
import numpy as np

# Hours taken to resolve 20 HR helpdesk tickets
resolution_hours = np.array([1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6, 8, 40, 72])

mean_hours = resolution_hours.mean()
median_hours = np.median(resolution_hours)
p90_hours = round(np.percentile(resolution_hours, 90), 1)
share_within_mean = (resolution_hours <= mean_hours).mean()
share_within_p90 = (resolution_hours <= p90_hours).mean()

print("Mean:", mean_hours, "| median:", median_hours, "| 90th percentile:", p90_hours)
print("Tickets resolved within the mean:", share_within_mean * 100, "%")
print("Tickets resolved within the 90th percentile:", share_within_p90 * 100, "%")
```
Output (real run):
```
Mean: 8.65 | median: 3.0 | 90th percentile: 11.2
Tickets resolved within the mean: 90.0 %
Tickets resolved within the 90th percentile: 90.0 %
```
In Excel: `=PERCENTILE.INC(A2:A21, 0.9)` (2010+; not run in Excel here).
**Likely follow-ups:** 1) *Why not the median?* It ignores the slow tail completely. 2) *Why p99?* Critical services care about the worst 1%.
**Common mistakes:** Quoting an average resolution time as the SLA; forgetting the slowest 10% still exist.

### Q59 ⭐ 🔴 A distribution is bimodal. What does that suggest, and how should you report its centre?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Whether you look for hidden groups instead of quoting one average.
**Say this in the interview:** "Two peaks usually mean two different groups mixed together, such as two shifts or two job levels. A single mean or median can land in the gap where nobody sits, so I find the groups, then report each group's centre separately, and mention both modes."
**Explain simply:**
- Look for a split variable: shift, team, location, gender, grade.
- Report the centre of each group, or the two modes, and the share of people in each.
- The overall mean is still computable, but label it as not typical.
**Worked example:** Engagement scores (1-10) for 20 employees: night shift scores around 2, day shift around 8-9. The overall mean is 5.45 and median 5.5, but no one scored between 4 and 7. Reported by shift: night mean 2.4, day mean 8.5.
**Excel / Python:**
```python
import numpy as np

# Engagement scores (1-10) from 20 employees: two very different groups
night_shift_scores = [2, 2, 3, 2, 3, 2, 3, 2, 3, 2]
day_shift_scores = [8, 9, 8, 9, 8, 9, 8, 9, 8, 9]
all_scores = np.array(night_shift_scores + day_shift_scores)

print("Overall mean:", all_scores.mean(), "| overall median:", np.median(all_scores))
print("People scoring between 4 and 7:", ((all_scores >= 4) & (all_scores <= 7)).sum())

# Report each group separately
print("Night shift: mean", np.mean(night_shift_scores), "median", np.median(night_shift_scores))
print("Day shift  : mean", np.mean(day_shift_scores), "median", np.median(day_shift_scores))
```
Output (real run):
```
Overall mean: 5.45 | overall median: 5.5
People scoring between 4 and 7: 0
Night shift: mean 2.4 median 2.0
Day shift  : mean 8.5 median 8.5
```
Plot a histogram first (Excel Histogram chart, or pandas `hist`) to see the two peaks.
**Likely follow-ups:** 1) *How to find the groups?* Segment by candidate variables and compare histograms. 2) *Can the groups be unequal?* Yes; report their shares.
**Common mistakes:** Reporting "average engagement is 5.5, neutral" when the company is actually split.

### Q60 ⭐ 🔴 How do you report salary data fairly when it has a long right tail and some people are on stock-based pay?
**Asked at:** commonly asked (no company-specific report found); a gap-fill, HR-flavoured question.
**What the interviewer is checking:** Judgement about skew, components of pay and honest communication.
**Say this in the interview:** "I lead with the median and the 25th to 75th percentile range, not the mean, because a few very high earners pull the mean up. I report cash pay and stock separately, since stock is lumpy and only some people hold it, and I state how I valued the stock and how many people have it."
**Explain simply:**
- Median plus quartiles (or P10/P50/P90) describe a typical person; the mean answers "what is the total pay bill per head".
- Split the components: base cash, bonus, stock. Show how many receive stock and its median among holders.
- Show the mean alongside as a cost measure, and say why the two differ.
- Note the valuation date and method for stock (grant value vs vesting value), since it moves.
- Check sample sizes before publishing small groups (privacy and noise).
**Worked example:** 12 employees (lakh rupees): cash pay median 11.5, Q1 8.75, Q3 17, mean 15.7. Including stock, the mean total jumps to 32.8 but the median stays 11.5, because only 4 of 12 hold stock; the top earner alone is 49.6% of all total pay.
**Excel / Python:**
```python
import numpy as np

# 12 employees: yearly cash pay and the yearly value of stock grants (in lakh rupees)
cash_pay = np.array([6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 30, 45])
stock_value = np.array([0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 40, 150])
total_pay = cash_pay + stock_value

def five_numbers(label, values):
    q1, median, q3 = np.percentile(values, [25, 50, 75])
    print(label, "| mean", round(values.mean(), 1), "| median", median, "| Q1", q1, "| Q3", q3, "| max", values.max())

five_numbers("Cash pay    ", cash_pay)
five_numbers("Total pay   ", total_pay)

people_with_stock = (stock_value > 0).sum()
print("People holding stock:", people_with_stock, "of", len(stock_value))
print("Median stock among holders:", np.median(stock_value[stock_value > 0]))
print("Top earner share of all total pay:", round(total_pay.max() / total_pay.sum() * 100, 1), "%")
```
Output (real run):
```
Cash pay     | mean 15.7 | median 11.5 | Q1 8.75 | Q3 17.0 | max 45
Total pay    | mean 32.8 | median 11.5 | Q1 8.75 | Q3 23.25 | max 195
People holding stock: 4 of 12
Median stock among holders: 25.0
Top earner share of all total pay: 49.6 %
```
In Excel: `=MEDIAN(range)`, `=QUARTILE.INC(range,1)`, `=QUARTILE.INC(range,3)` (2010+; not run in Excel here).
**Likely follow-ups:** 1) *Would you cap the top values?* Prefer reporting median and percentiles over editing data. 2) *Gender pay gap?* Compare medians within the same grade.
**Common mistakes:** Reporting only the mean; mixing cash and stock into one number without explanation.

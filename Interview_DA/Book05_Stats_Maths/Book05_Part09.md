# Book 5 — Statistics & Maths for Data Analysts | Part 9: Outliers, Simpson's Paradox, Misleading Stats 🟡

**Target:** 40 questions | **Actual:** 41 questions
**Scope:** detecting and handling outliers, Simpson's paradox, and the common ways averages, percentages and charts mislead.

### Q1 ⭐⭐⭐ 🟢 What is an outlier?
**Asked at:** commonly asked (no company-specific report found); "what are outliers and how do you identify them" recurs in candidate-reported Glassdoor junior data analyst lists (undated; seen at snippet level only).
**What the interviewer is checking:** Can you define it simply, and do you know an outlier is something to investigate, not automatically delete?
**Say this in the interview:** "An outlier is a value that sits far away from the rest of the data. For example, in a team where salaries are Rs 22,000 to Rs 28,000 a month, one salary of Rs 95,000 is an outlier. It could be a typing mistake, a genuine rare case like a senior hire, or a sign that the person belongs to a different group, so I investigate before I decide what to do."
**Explain simply:**
- "Far away" is a judgement, so analysts use a rule (IQR or z-score, see Q5 and Q6) to make it consistent.
- An outlier is not the same as a mistake (see Q10). It is just unusual.
- Outliers matter because they pull the *mean* (the ordinary average) towards themselves, while the *median* (the middle value) barely moves.
**Worked example:** 11 employees earn (in Rs thousand per month) 22, 25, 24, 27, 23, 26, 28, 25, 24, 26 and 95. The median is 25. The mean is 31.36, higher than 10 of the 11 people, because of the single 95.
**Likely follow-ups:** 1) *Is an outlier always bad?* No, it can be your most interesting finding (Q7). 2) *Can there be outliers in more than one column at once?* Yes, see Q40.
**Common mistakes:** Calling every large number an outlier without a rule; assuming an outlier must be an error.

### Q2 ⭐⭐⭐ 🟢 How do you identify outliers in a dataset?
**Asked at:** commonly asked (no company-specific report found); appears in candidate-reported Glassdoor junior data analyst lists (undated, snippet level) and in general prep sites such as InterviewKickstart.
**What the interviewer is checking:** Do you know more than one method, and do you start by looking at the data?
**Say this in the interview:** "First I look at the data: sort it, make a box plot or histogram. Then I apply a rule. My default is the IQR rule, because it does not get fooled by the outliers themselves. I also use z-scores when the data is roughly bell-shaped and large enough. Whatever gets flagged, I then check why it is unusual."
**Explain simply:**
- *Visual:* box plot (dots beyond the whiskers), histogram, scatter plot.
- *IQR rule:* flag values below Q1 minus 1.5 times IQR, or above Q3 plus 1.5 times IQR (Q5). *IQR* is the width of the middle half of the data.
- *Z-score rule:* flag values more than 3 standard deviations from the mean (Q6). A *standard deviation* is the typical distance of a value from the mean.
- *Business rules:* an age of 250 or a negative salary is impossible, so flag it regardless of statistics.
**Formula in plain words:** Upper fence = Q3 + 1.5 x (Q3 - Q1). Lower fence = Q1 - 1.5 x (Q3 - Q1). Z-score = (value - mean) / standard deviation.
**Worked example:** Same 11 salaries as Q1 (Rs thousand): Q1 = 24, Q3 = 26.5, IQR = 2.5, fences are 20.25 and 30.25, so only 95 is flagged. Z-score of 95 is 3.01, also flagged.
**Excel / Python:**
```python
import numpy as np

# monthly salaries in Rs thousand for 11 employees
monthly_salaries = np.array([22, 25, 24, 27, 23, 26, 28, 25, 24, 26, 95])

# step 1: IQR rule. Find the 25th and 75th percentiles (Q1 and Q3)
q1 = np.percentile(monthly_salaries, 25)
q3 = np.percentile(monthly_salaries, 75)
iqr = q3 - q1

# step 2: build the two fences
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr
print("Q1, Q3, IQR:", q1, q3, iqr)
print("fences:", lower_fence, upper_fence)

# step 3: keep the salaries that fall outside the fences
outside_fences = (monthly_salaries < lower_fence) | (monthly_salaries > upper_fence)
print("IQR outliers:", monthly_salaries[outside_fences])

# step 4: z-score rule. How many standard deviations from the mean is each salary?
average_salary = monthly_salaries.mean()
spread = monthly_salaries.std(ddof=1)
z_scores = (monthly_salaries - average_salary) / spread
print("mean %.2f sd %.2f" % (average_salary, spread))
print("z-scores:", np.round(z_scores, 2))
```
Output:
```
Q1, Q3, IQR: 24.0 26.5 2.5
fences: 20.25 30.25
IQR outliers: [95]
mean 31.36 sd 21.18
z-scores: [-0.44 -0.3  -0.35 -0.21 -0.39 -0.25 -0.16 -0.3  -0.35 -0.25  3.01]
```
Both methods point to the Rs 95,000 salary. Excel (2010+; not run in Excel here): with salaries in A2:A12, `=QUARTILE.INC(A2:A12,1)` gives 24 and `=QUARTILE.INC(A2:A12,3)` gives 26.5; `=STANDARDIZE(A12,AVERAGE($A$2:$A$12),STDEV.S($A$2:$A$12))` gives 3.01 (matches the Python by calculation).
**Likely follow-ups:** 1) *Which do you prefer?* IQR for skewed or small data, z-score for large bell-shaped data. 2) *What after detecting?* Investigate (Q19).
**Common mistakes:** Using only z-scores on skewed salary data; treating the rule's flag as proof of an error.

### Q3 ⭐⭐⭐ 🟢 How do you handle outliers in a dataset?
**Asked at:** commonly asked (no company-specific report found); "best way to handle outliers" recurs in candidate-reported Glassdoor lists and in Dataford's practice question (investigate first, then treat).
**What the interviewer is checking:** Do you investigate first and choose a treatment that fits the cause, rather than deleting automatically?
**Say this in the interview:** "I never delete blindly. First I find out why the value is unusual. If it is a typing error I fix it from the source, or mark it missing. If it is real, I usually keep it and use robust measures like the median, or cap extreme values (winsorize), or report results with and without it. I always document what I did."
**Explain simply:**
- *Fix:* correct an obvious data-entry error (Rs 2,50,000 typed as Rs 25,00,000).
- *Remove:* only if it is invalid or does not belong to the group you study.
- *Cap (winsorize):* replace extremes by a limit value, so they stay but lose their pull (Q17).
- *Transform:* a log transformation shrinks big values (Q32).
- *Use robust statistics:* median and IQR instead of mean and standard deviation.
- *Keep and report:* if it is real and important, keep it and show results with and without it (Q33).
**Worked example:** Salaries from Q1: mean is 31.36. Dropping the 95 gives mean 25.0. Capping 95 at the upper fence 30.25 gives mean 25.48. The median stays 25.0 throughout.
**Excel / Python:**
```python
import numpy as np

# monthly salaries in Rs thousand, the last one is the unusual 95
monthly_salaries = np.array([22, 25, 24, 27, 23, 26, 28, 25, 24, 26, 95])

# upper and lower limits from the IQR rule (see Q2)
lower_fence = 20.25
upper_fence = 30.25

# option 1: cap values at the fences (winsorize)
capped_salaries = np.clip(monthly_salaries, lower_fence, upper_fence)

# option 2: drop the last salary
salaries_without_outlier = np.delete(monthly_salaries, 10)

print("median", np.median(monthly_salaries))
print("capped mean %.2f" % capped_salaries.mean())
print("mean without outlier %.2f" % salaries_without_outlier.mean())
```
Output:
```
median 25.0
capped mean 25.48
mean without outlier 25.00
```
Capping keeps all 11 people in the data but stops one salary dragging the average.
**Likely follow-ups:** 1) *When do you keep it?* See Q7. 2) *What if you are unsure?* Run the analysis both ways and report both.
**Common mistakes:** Deleting because "it looks wrong"; changing data silently without a note; treating every outlier the same way.

### Q4 ⭐⭐⭐ 🟢 Your company's average salary is Rs 14 lakh but most employees earn about Rs 6 lakh. Which average would you report to the CEO, and why?
**Asked at:** commonly asked (no company-specific report found); the salary mean-versus-median framing appears in Interview Query's analytics-company guides (figures there are self-reported and not used here).
**What the interviewer is checking:** Do you know mean is pulled by extremes and median describes the typical person?
**Say this in the interview:** "I would report the median as the headline, and mention the mean alongside it with a one-line explanation. A few very high earners, such as top leadership, pull the mean up to Rs 14 lakh, but the median tells the CEO what a typical employee earns, around Rs 6 lakh. Reporting only the mean would give a false picture of pay."
**Explain simply:**
- *Mean:* add all salaries, divide by headcount. Every value counts, so extreme values pull it.
- *Median:* the middle person when everyone is lined up by salary. It does not care how large the top salaries are.
- When salaries are *right-skewed* (a long tail of high earners), mean is above median.
- Best to show both, plus a distribution (percentiles or a histogram).
**Worked example:** 20 employees (Rs lakh per year): 18 earn between 5 and 7, and two senior leaders earn 80 and 97. The mean is 14.0, the median is 5.75, and 18 of the 20 people earn less than the mean.
**Excel / Python:**
```python
import numpy as np

# yearly salaries in Rs lakh: 18 regular staff and 2 senior leaders
salaries_lakh = np.array([5.0]*6 + [5.5]*4 + [6.0]*4 + [6.5]*2 + [7.0]*2 + [80.0, 97.0])

# average of all salaries
mean_salary = salaries_lakh.mean()

# middle salary
median_salary = np.median(salaries_lakh)

# how many people earn less than the mean
below_mean = (salaries_lakh < mean_salary).sum()

print(len(salaries_lakh), mean_salary, median_salary, below_mean)
```
Output:
```
20 14.0 5.75 18
```
The mean says Rs 14 lakh but 18 of 20 people earn less, so the median (5.75) is the honest "typical" figure. Excel: `=AVERAGE(A2:A21)` and `=MEDIAN(A2:A21)`.
**Likely follow-ups:** 1) *Would you ever report the mean?* Yes, for total payroll cost, since totals need the mean. 2) *Anything else?* Percentiles (25th, 75th, 90th).
**Common mistakes:** Reporting only the mean; forgetting the mean is the right tool for budget totals.

### Q5 ⭐⭐⭐ 🟡 Explain the IQR method for detecting outliers. In a salary dataset Q1 is Rs 15,000 and Q3 is Rs 28,000: is Rs 95,000 an outlier?
**Asked at:** commonly asked (no company-specific report found); IQR and z-score are the two standard outlier methods in prep material.
**What the interviewer is checking:** Can you apply the 1.5 x IQR rule accurately and quickly?
**Say this in the interview:** "IQR is Q3 minus Q1, the spread of the middle 50% of people. I build fences 1.5 times IQR below Q1 and above Q3. Here IQR is 13,000, so the upper fence is 28,000 plus 19,500, which is 47,500. Rs 95,000 is well above that, so yes, it is an outlier."
**Explain simply:**
- *Q1* (first quartile) is the value with 25% of data below it. *Q3* has 75% below it.
- The factor 1.5 is a convention (John Tukey's rule of thumb), not a law of nature. Use 3 for "extreme" outliers.
- It works well because Q1 and Q3 hardly move when an outlier is present.
**Formula in plain words:** Upper fence = Q3 + 1.5 x IQR. Lower fence = Q1 - 1.5 x IQR, where IQR = Q3 - Q1.
**Worked example:** IQR = 28,000 - 15,000 = 13,000. Upper fence = 28,000 + 1.5 x 13,000 = 47,500. Lower fence = 15,000 - 19,500 = -4,500 (below zero, so no low salary can be an outlier). 95,000 > 47,500, so it is an outlier.
**Excel / Python:**
```python
# given quartiles of the salary data
q1 = 15000
q3 = 28000

# width of the middle half of the data
iqr = q3 - q1

# fences
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

# test the salary in question
salary_to_check = 95000
is_outlier = salary_to_check < lower_fence or salary_to_check > upper_fence
print(iqr, lower_fence, upper_fence, is_outlier)
```
Output:
```
13000 -4500.0 47500.0 True
```
Excel (cells: Q1 in B1, Q3 in B2, salary in B3; not run in Excel here, simple arithmetic): `=OR(B3<B1-1.5*(B2-B1), B3>B2+1.5*(B2-B1))` returns TRUE.
**Likely follow-ups:** 1) *Why 1.5?* Convention that flags about 0.7% of a normal distribution. 2) *Would 40,000 be an outlier?* No, it is below 47,500.
**Common mistakes:** Forgetting to multiply the IQR by 1.5; adding 1.5 to the quartile instead of 1.5 times IQR.

### Q6 ⭐⭐⭐ 🟡 Explain the z-score method for detecting outliers. When does it fail?
**Asked at:** commonly asked (no company-specific report found); z-score masking and the modified z-score appear in general outlier reference material.
**What the interviewer is checking:** Do you know the method and, more importantly, its weaknesses?
**Say this in the interview:** "A z-score says how many standard deviations a value is from the mean. Values beyond 3 (or -3) are usually flagged. It fails when the data is skewed, when the sample is small, and when there are several outliers, because the outliers inflate the mean and standard deviation that the z-score itself uses, so they hide each other."
**Explain simply:**
- *Standard deviation* is the typical distance of values from the mean.
- The 3 cut-off comes from the bell curve, where only about 0.3% of values are beyond 3.
- *Small samples:* with n values, the highest possible z-score is (n-1)/sqrt(n). For n = 10 that is 2.85, so nothing can ever pass 3.
- *Masking:* several outliers raise the standard deviation, so each looks less extreme (see Q38).
- *Skewed data:* a normal distribution is assumed; salary data is not.
**Formula in plain words:** z = (value - mean) / standard deviation.
**Worked example:** 10 salaries (Rs thousand) with one 95: z of 95 is 2.84, below 3 and not flagged, even though IQR flags it. With three high salaries 95, 98, 102 among 13 values, their z-scores are only 1.65, 1.74 and 1.86, none flagged, while the IQR rule catches all three.
**Excel / Python:**
```python
import numpy as np

# 10 salaries in Rs thousand with one very high value
ten_salaries = np.array([22, 25, 24, 27, 23, 26, 28, 25, 24, 95])

# z-score of every salary
z_scores = (ten_salaries - ten_salaries.mean()) / ten_salaries.std(ddof=1)
print("z of 95: %.2f" % z_scores[-1], " maximum possible: %.2f" % (9 / np.sqrt(10)))

# 13 salaries, three of them very high (masking)
thirteen_salaries = np.array([22, 25, 24, 27, 23, 26, 28, 25, 24, 26, 95, 98, 102])
z_scores_13 = (thirteen_salaries - thirteen_salaries.mean()) / thirteen_salaries.std(ddof=1)
print("z of the three high salaries:", np.round(z_scores_13[-3:], 2))
print("flagged by z beyond 3:", (np.abs(z_scores_13) > 3).sum())
```
Output:
```
z of 95: 2.84  maximum possible: 2.85
z of the three high salaries: [1.65 1.74 1.86]
flagged by z beyond 3: 0
```
The z-score method misses all of them; use IQR or the modified z-score (Q18).
**Likely follow-ups:** 1) *What instead?* IQR or MAD-based z-score. 2) *Why use 3?* Bell-curve convention; 2.5 or 3.5 are also used.
**Common mistakes:** Using it on skewed data; trusting it on tiny samples; forgetting that outliers distort the mean and standard deviation.

### Q7 ⭐⭐⭐ 🟡 Should you always remove outliers? When would you keep one?
**Asked at:** commonly asked (no company-specific report found); handling-outliers questions in candidate lists expect "investigate first".
**What the interviewer is checking:** Judgement: do you treat outliers as information, not noise?
**Say this in the interview:** "No. I remove a value only if it is a clear error or does not belong to the population I am studying. I keep it if it is real and relevant: a genuine top performer's bonus, a fraud case, a real spike in resignations. Removing real extremes makes the analysis look cleaner but wrong."
**Explain simply:**
- *Remove or fix:* impossible values (age 250), duplicated rows, wrong units (salary entered in rupees instead of thousands).
- *Keep:* real, rare events that the business cares about, such as one large resignation wave or a record hiring month.
- *Keep but separate:* the CEO's salary in a pay analysis of all staff is real, but may need a separate group.
- If unsure, show the result both ways.
**Worked example:** Monthly resignations are 4, 5, 3, 6, 5, 4 and then 31 in the month a branch closed. Deleting 31 would hide the very event leadership wants to understand. Mean with 31 is 8.29; without it 4.5. Report both and explain the branch closure.
**Excel / Python:**
```python
import numpy as np

# monthly resignations including a spike of 31 from a branch closure
monthly_resignations = np.array([4, 5, 3, 6, 5, 4, 31])
print("mean with spike: %.2f" % monthly_resignations.mean())
print("mean without spike: %.2f" % monthly_resignations[:-1].mean())
```
Output:
```
mean with spike: 8.29
mean without spike: 4.50
```
Both numbers are useful: 4.5 is the normal month, 8.29 includes the closure.
**Likely follow-ups:** 1) *What do you document?* Which values, why, and the effect on results. 2) *Who decides?* The analyst proposes; the business owner confirms.
**Common mistakes:** Removing outliers just to improve a model's fit or a p-value.

### Q8 ⭐⭐⭐ 🟡 What is Simpson's paradox? Explain it with an example.
**Asked at:** commonly asked (no company-specific report found); "explain Simpson's paradox with an example" is listed on practice platforms such as PracHub (attribution to specific companies there is unverified).
**What the interviewer is checking:** Can you explain it in plain words with numbers, and say what to do about it?
**Say this in the interview:** "Simpson's paradox is when a trend that appears in every subgroup reverses when you combine the groups. It happens when the groups are very different in size and mix, so the overall figure is dominated by a hidden factor. The fix is to look at the data by the relevant segment before trusting the overall number."
**Explain simply:**
- The hidden factor (a *confounder*) is linked to both the group and the outcome.
- No arithmetic mistake is involved; the combined rate is a weighted average and the weights differ.
- Example: classroom training vs online training, success rate of passing a certification.
**Worked example:**

| | Junior pass | Senior pass | Overall |
|---|---|---|---|
| Classroom | 81 of 87 (93.1%) | 192 of 263 (73.0%) | 273 of 350 (78.0%) |
| Online | 234 of 270 (86.7%) | 55 of 80 (68.8%) | 289 of 350 (82.6%) |

Classroom wins for both juniors and seniors, yet online wins overall, because online mostly trained easier-to-pass juniors, and classroom mostly trained seniors.
**Excel / Python:**
```python
# (passed, trained) counts for each training mode and employee level
classroom = {"junior": (81, 87), "senior": (192, 263)}
online = {"junior": (234, 270), "senior": (55, 80)}

for mode_name, mode_data in [("Classroom", classroom), ("Online", online)]:
    junior_passed, junior_trained = mode_data["junior"]
    senior_passed, senior_trained = mode_data["senior"]
    # pass rate inside each level, then overall
    junior_rate = 100 * junior_passed / junior_trained
    senior_rate = 100 * senior_passed / senior_trained
    overall_rate = 100 * (junior_passed + senior_passed) / (junior_trained + senior_trained)
    print(mode_name, "junior %.1f senior %.1f overall %.1f" % (junior_rate, senior_rate, overall_rate))
```
Output:
```
Classroom junior 93.1 senior 73.0 overall 78.0
Online junior 86.7 senior 68.8 overall 82.6
```
The ranking flips between the level-wise rows and the overall column.
**Likely follow-ups:** 1) *Which result is right?* Depends on the cause; see Q25. 2) *How to spot it?* Always split by likely confounders (Q24).
**Common mistakes:** Believing it is a calculation error; trusting overall rates without checking mix.

### Q9 ⭐⭐⭐ 🟡 Two recruiters have different offer-acceptance rates overall, but the ranking flips when you look department by department. Show with numbers how this can happen.
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured version of the standard Simpson's paradox question.
**What the interviewer is checking:** Can you build a numeric example yourself and explain the mix effect?
**Say this in the interview:** "Recruiter A can be better in every department but look worse overall, if A handles mostly the hard department, where acceptance is low for everyone, while B handles mostly the easy one. The overall rate is a weighted average, and the weights, meaning how many offers each recruiter made in each department, are very different."
**Explain simply:**
- Acceptance rate = offers accepted / offers made.
- Tech offers are easy to close here; Sales offers are hard.
- A makes 10 Tech and 90 Sales offers; B makes 90 Tech and 10 Sales offers.
**Worked example:**

| | Tech | Sales | Overall |
|---|---|---|---|
| Recruiter A | 9 of 10 (90.0%) | 30 of 90 (33.3%) | 39 of 100 (39.0%) |
| Recruiter B | 60 of 90 (66.7%) | 3 of 10 (30.0%) | 63 of 100 (63.0%) |

A beats B in Tech (90% vs 66.7%) and in Sales (33.3% vs 30%), yet B looks far better overall (63% vs 39%).
**Excel / Python:**
```python
# (accepted, offers made) for each recruiter and department
recruiter_a = {"Tech": (9, 10), "Sales": (30, 90)}
recruiter_b = {"Tech": (60, 90), "Sales": (3, 10)}

for recruiter_name, results in [("A", recruiter_a), ("B", recruiter_b)]:
    tech_accepted, tech_offers = results["Tech"]
    sales_accepted, sales_offers = results["Sales"]
    tech_rate = 100 * tech_accepted / tech_offers
    sales_rate = 100 * sales_accepted / sales_offers
    overall_rate = 100 * (tech_accepted + sales_accepted) / (tech_offers + sales_offers)
    print(recruiter_name, "tech %.1f%% sales %.1f%% overall %.1f%%" % (tech_rate, sales_rate, overall_rate))
```
Output:
```
A tech 90.0% sales 33.3% overall 39.0%
B tech 66.7% sales 30.0% overall 63.0%
```
Judging recruiters on the overall rate would punish A for taking the harder roles.
**Likely follow-ups:** 1) *Who is the better recruiter?* A, department for department. 2) *What should you report?* The department-wise table.
**Common mistakes:** Comparing recruiters on the overall rate without checking the mix of roles.

### Q10 ⭐⭐ 🟢 How is an outlier different from a data-entry error?
**Asked at:** commonly asked (no company-specific report found); a standard follow-up to outlier questions.
**What the interviewer is checking:** Do you separate "unusual but real" from "wrong"?
**Say this in the interview:** "An outlier is a statistically unusual value; a data-entry error is a value that is wrong. An age of 250 is an error because it is impossible. A salary of Rs 4 lakh a month for a director is an outlier: unusual, but plausible. An error can look like an outlier, but not every outlier is an error, so I verify against the source before changing anything."
**Explain simply:**
- Test an impossible value with a simple business rule (age 18 to 70, salary above zero, joining date not in the future).
- Test a plausible value against source records or ask the data owner.
- Errors get fixed or marked missing; real outliers are kept or handled with robust methods.
**Worked example:** In a six-row table, age 250 fails the rule and is an error; a salary of Rs 4,00,000 per month is flagged, but it is a possible figure and needs a check with HR.
**Excel / Python:**
```python
import pandas as pd

# small employee table: one impossible age and one very high but possible salary
employees = pd.DataFrame({
    "emp_id": ["E1", "E2", "E3", "E4", "E5", "E6"],
    "age": [28, 34, 41, 250, 30, 38],
    "monthly_salary": [24000, 26000, 25000, 27000, 23000, 400000],
})

# an age below 18 or above 70 is impossible, so this is an error
impossible_age = employees[(employees["age"] < 18) | (employees["age"] > 70)]
print(impossible_age)

# a very high salary is possible, so only flag it for a check
high_salary = employees[employees["monthly_salary"] > 100000]
print(high_salary)
```
Output:
```
  emp_id  age  monthly_salary
3     E4  250           27000
  emp_id  age  monthly_salary
5     E6   38          400000
```
E4 is an error to fix; E6 is a flag to verify.
**Likely follow-ups:** 1) *How do you check?* Source system, a manager, or HR records. 2) *What if you cannot verify?* Keep, mark, and report with and without.
**Common mistakes:** Deleting a real value because it is big; keeping a clearly impossible one.

### Q11 ⭐⭐ 🟢 How does a box plot show outliers?
**Asked at:** commonly asked (no company-specific report found); box plots are the standard visual for outliers.
**What the interviewer is checking:** Can you read a box plot properly?
**Say this in the interview:** "A box plot draws a box from Q1 to Q3 with a line at the median. Whiskers extend to the furthest data points still within 1.5 times IQR of the box. Any point beyond the whiskers is drawn as an individual dot, and those dots are the outliers by the IQR rule."
**Explain simply:**
- Box = middle 50% of data; line inside = median.
- Whisker ends = the smallest and largest values *inside* the fences, not the fences themselves.
- Dots = values outside the fences.
- Caveat: the whisker rule is a convention that some tools change.
**Worked example:** Salaries (Rs thousand) 22 to 28 plus a 95: box from 24.0 to 26.5, median 25.0, whiskers end at 22 and 28, and 95 shows as a lone dot.
**Excel / Python:**
```python
import numpy as np

# monthly salaries in Rs thousand
monthly_salaries = np.array([22, 25, 24, 27, 23, 26, 28, 25, 24, 26, 95])

# the box edges and the fences
q1, q3 = np.percentile(monthly_salaries, [25, 75])
iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

# whiskers end at the most extreme values still inside the fences
inside_fences = monthly_salaries[(monthly_salaries >= lower_fence) & (monthly_salaries <= upper_fence)]
print("box from", q1, "to", q3, "median", np.median(monthly_salaries))
print("lower whisker ends at", inside_fences.min(), "upper whisker ends at", inside_fences.max())
print("dots beyond whiskers:", monthly_salaries[(monthly_salaries < lower_fence) | (monthly_salaries > upper_fence)])
```
Output:
```
box from 24.0 to 26.5 median 25.0
lower whisker ends at 22 upper whisker ends at 28
dots beyond whiskers: [95]
```
This reproduces by hand what a box plot draws. To draw it, use `matplotlib` `plt.boxplot(monthly_salaries)` (not run here, matplotlib is not installed in this environment) or Excel's Box and Whisker chart (2016+, not run here).
**Likely follow-ups:** 1) *Do dots mean errors?* No, only unusual values. 2) *Box plot weakness?* Hides bimodal shapes (Q28).
**Common mistakes:** Thinking whiskers go to the fences, or that every dot is an error.

### Q12 ⭐⭐ 🟢 Attrition fell from 10% to 5%. A manager says "attrition was halved". What is wrong or incomplete about presenting it that way?
**Asked at:** commonly asked (no company-specific report found); a common HR-analytics scenario.
**What the interviewer is checking:** Do you notice relative vs absolute change and missing context?
**Say this in the interview:** "Halved is arithmetically right as a relative change, 50%, but it can overstate the story. The absolute fall is 5 percentage points. I would ask: how many people is that, over what period, for which group, how was attrition defined, and was the base the same? With a small headcount, 5 fewer leavers can be just random variation."
**Explain simply:**
- Relative change: (5 - 10) / 10 = -50%. Absolute change: 10% to 5% is a drop of 5 percentage points (Q13).
- Check headcount: 10% of 200 is 20 people, 5% is 10 people. A change of 10 people.
- Check time period, seasonality, definition (voluntary only? including contract?), and whether the headcount changed.
- Check whether the drop is lasting or a one-quarter blip (*regression to the mean*, Q30).
**Worked example:** With 200 employees, attrition of 10% means 20 leavers and 5% means 10 leavers. "Halved" is true, yet it is 10 fewer people, which for a team this size could be partly chance.
**Excel / Python:**
```python
# attrition rates and headcount
old_rate = 10
new_rate = 5
headcount = 200

# percentage-point change and relative change
point_change = new_rate - old_rate
relative_change = (new_rate - old_rate) / old_rate * 100

# number of leavers before and after
old_leavers = headcount * old_rate / 100
new_leavers = headcount * new_rate / 100
print(point_change, relative_change, old_leavers, new_leavers)
```
Output:
```
-5 -50.0 20.0 10.0
```
A 50% relative fall equals only 5 percentage points, or 10 fewer leavers.
**Likely follow-ups:** 1) *What would you present instead?* Both numbers, headcounts and the trend over several months. 2) *Is "halved" wrong?* Not wrong, but incomplete.
**Common mistakes:** Quoting only the dramatic relative change; ignoring headcount size.

### Q13 ⭐⭐ 🟢 What is the difference between percentage change and percentage-point change? Give an HR example.
**Asked at:** commonly asked (no company-specific report found); a common reporting-accuracy question.
**What the interviewer is checking:** Can you tell the two apart and avoid confusing audiences?
**Say this in the interview:** "A percentage-point change is the plain difference between two percentages. A percentage change is that difference divided by the starting value. If attrition rises from 8% to 10%, that is a 2 percentage-point rise but a 25% increase."
**Explain simply:**
- Percentage points answer "how far did the rate move?".
- Percentage change answers "by what fraction of the old rate did it move?".
- Always say which one you mean, because the two numbers look very different.
**Formula in plain words:** Percentage-point change = new % - old %. Percentage change = (new % - old %) / old % x 100.
**Worked example:** Attrition 8% to 10%: 10 - 8 = +2 points; (10 - 8) / 8 x 100 = +25%.
**Excel / Python:**
```python
# attrition rate last year and this year, in percent
old_rate = 8
new_rate = 10

# plain difference in percentage points
point_change = new_rate - old_rate

# change relative to the starting rate
percentage_change = (new_rate - old_rate) / old_rate * 100
print(point_change, percentage_change)
```
Output:
```
2 25.0
```
Excel: old in A1, new in B1: `=B1-A1` gives 2 (points) and `=(B1-A1)/A1` gives 0.25, shown as 25% with percent format (not run in Excel here; simple arithmetic).
**Likely follow-ups:** 1) *Which to use?* Points for rates moving at a low level; percentage change for relative size. Best to show both.
**Common mistakes:** Writing "attrition rose 2%" when meaning 2 points; mixing the two in one sentence.

### Q14 ⭐⭐ 🟢 How can a chart with a truncated y-axis mislead the reader?
**Asked at:** commonly asked (no company-specific report found); a standard chart-honesty question.
**What the interviewer is checking:** Do you understand that bar length should match the value?
**Say this in the interview:** "If a bar chart's y-axis starts at, say, 76 instead of 0, the bar heights no longer show the real proportion. A small difference looks huge. A bar chart should start at zero because the length of the bar is the quantity; a line chart can start elsewhere if the scale is clearly labelled."
**Explain simply:**
- Bars encode value by length, so cutting off the bottom exaggerates differences.
- The reader may not check the axis labels.
- A truncated axis is more acceptable for line charts showing change over time, if clearly marked.
**Worked example:** Engagement scores are 78 for Team A and 80 for Team B, a real difference of 2.6%. With the y-axis starting at 76, the bars are 2 and 4 units tall, so B looks twice as high.
**Excel / Python:**
```python
# engagement scores for the two teams
team_a_score = 78
team_b_score = 80

# real ratio between the two bars when the axis starts at zero
real_ratio = team_b_score / team_a_score

# visual ratio when the axis starts at 76
axis_start = 76
visual_ratio = (team_b_score - axis_start) / (team_a_score - axis_start)
print("real ratio %.3f, visual ratio %.1f" % (real_ratio, visual_ratio))
```
Output:
```
real ratio 1.026, visual ratio 2.0
```
The chart makes a 2.6% difference look like 100%.
**Likely follow-ups:** 1) *When is truncation fine?* Line charts with clear labels. 2) *How to fix?* Start bars at zero, or show the numbers on the bars.
**Common mistakes:** Truncating bar charts to make small changes dramatic; not labelling the axis start.

### Q15 ⭐⭐ 🟢 What is cherry-picking in data analysis, and how do you avoid it?
**Asked at:** commonly asked (no company-specific report found). Listed as a gap-fill (standard practice) in the Part 9 sources file.
**What the interviewer is checking:** Do you report the whole picture honestly, not just the numbers that support a story?
**Say this in the interview:** "Cherry-picking means showing only the data points, time periods or segments that support a conclusion and hiding the rest. I avoid it by deciding the question, the period and the metric before I look at results, and by showing the full range."
**Explain simply:**
- It is selective evidence: the numbers may all be true, but the choice of which ones to show is what misleads.
- Common forms: choosing a convenient start date, dropping an inconvenient department, or testing many cuts and reporting only the one that "worked".
- Defence: fix the definition and time window first, show the full series, and say how many cuts you tried.
- Let a colleague check which rows or periods were left out.
**Worked example:** Attrition by quarter over two years. A manager says "attrition fell from 9.5% to 6.5%" by starting at a high quarter (Q2-24) and ending at the lowest of all (Q4-25). The full-year averages show 2025 (8.475%) was actually higher than 2024 (7.875%).
**Excel / Python:**
```python
import pandas as pd

# Attrition % for eight quarters
attrition = pd.Series(
    [8.0, 9.5, 7.2, 6.8, 9.1, 10.4, 7.9, 6.5],
    index=["Q1-24", "Q2-24", "Q3-24", "Q4-24", "Q1-25", "Q2-25", "Q3-25", "Q4-25"],
)

# Cherry-picked view: start at a high quarter, end at the lowest quarter
print("Peak to latest:", attrition["Q2-24"], "->", attrition["Q4-25"])

# Honest view: average of each full year
average_2024 = attrition.iloc[:4].mean()
average_2025 = attrition.iloc[4:].mean()
print("2024 average:", average_2024)
print("2025 average:", average_2025)
```
Output:
```
Peak to latest: 9.5 -> 6.5
2024 average: 7.875
2025 average: 8.475
```
The peak-to-latest view shows a 3-point fall, but the yearly averages show attrition rose slightly. Same data, opposite story.
**Likely follow-ups:** 1) *Is it always deliberate?* No, often it is unconscious; a written analysis plan guards against it. 2) *Link to testing many cuts?* Testing 20 segments will show a "significant" one by luck alone (Texas sharpshooter, see Q34).
**Common mistakes:** Picking the time window after seeing the chart; reporting the best segment without saying how many were tried.

### Q16 ⭐⭐ 🟡 Why is the average of department-wise averages not the same as the company-wide average? Show with an example.
**Asked at:** commonly asked (no company-specific report found). Listed as a gap-fill (standard practice) in the sources file.
**What the interviewer is checking:** Do you understand weighted versus simple averages?
**Say this in the interview:** "A company average gives every employee one vote, but an average of department averages gives every department one vote. A department of 10 and a department of 90 count equally in the second, which is wrong unless the sizes are equal."
**Explain simply:**
- Each department average hides how many people are behind it.
- The correct company average is the total salary bill divided by total headcount, which is the same as a headcount-weighted average of the department averages.
- The two agree only when every department has the same headcount (or the same average).
**Formula in plain words:** Company average = sum of (headcount x department average) divided by total headcount. In symbols: Σ(n_i × avg_i) / Σ n_i.
**Worked example:** Support has 10 people averaging Rs 40,000; Engineering has 90 averaging Rs 60,000. Average of averages = Rs 50,000. True company average = (10 x 40,000 + 90 x 60,000) / 100 = Rs 58,000.
**Excel / Python:**
Excel: put headcount in B2:B3 and average salary in C2:C3. `=AVERAGE(C2:C3)` returns 50000 (wrong for the company). `=SUMPRODUCT(B2:B3,C2:C3)/SUM(B2:B3)` returns 58000 (works in all modern Excel; checked here in Python, not run in Excel).
```python
import pandas as pd

# Two departments: headcount and their average monthly salary
departments = pd.DataFrame({
    "department": ["Support", "Engineering"],
    "headcount": [10, 90],
    "average_salary": [40000, 60000],
})

# Simple average of the two department averages (each department counts once)
average_of_averages = departments["average_salary"].mean()

# Company-wide average: weight each department by its headcount
total_salary_bill = (departments["headcount"] * departments["average_salary"]).sum()
company_average = total_salary_bill / departments["headcount"].sum()

print("Average of averages:", average_of_averages)
print("Company-wide average:", company_average)
```
Output:
```
Average of averages: 50000.0
Company-wide average: 58000.0
```
The simple average treats the 10-person team as equal to the 90-person team, so it understates the company average by Rs 8,000.
**Likely follow-ups:** 1) *Does the same apply to percentages?* Yes: average attrition rate of departments is not company attrition; divide total leavers by total headcount. 2) *Is it related to Simpson's paradox?* Same root cause, ignoring group sizes.
**Common mistakes:** Averaging percentages or averages from a pivot table without weights.

### Q17 ⭐⭐ 🟡 What is winsorization, and how is it different from trimming and from deleting outliers?
**Asked at:** commonly asked (no company-specific report found). Listed as a gap-fill (standard practice; winsorization described in the zaps/alooba/statsig reference pages named in the sources file).
**What the interviewer is checking:** Can you name the options for treating extremes and tell them apart?
**Say this in the interview:** "Winsorization replaces extreme values with the nearest acceptable value, so the row stays but its pull is limited. Trimming drops a fixed share from each end. Deleting removes chosen rows. They differ in whether the row survives and how many rows go."
**Explain simply:**
- Winsorizing at 10%: the lowest 10% become the next-lowest kept value, the top 10% become the highest kept value. Sample size is unchanged.
- Trimming: the same 10% at each end are removed, so the sample shrinks.
- Deleting: you remove specific rows you judge wrong, usually one by one. This needs a reason such as a proven entry error.
- Winsorizing and trimming are rule-based (a percentage), so they are easier to defend as not hand-picked.
**Worked example:** Ten salaries where one person earns Rs 3,00,000 against a typical Rs 30,000 to 45,000. Original mean 63,100; winsorized mean 37,800; 10% trimmed mean 37,625; deleting just the 300000 gives 36,778.
**Excel / Python:**
```python
import numpy as np
from scipy import stats
from scipy.stats.mstats import winsorize

# Ten monthly salaries; the last one (300000) is an extreme value
salaries = np.array([30, 32, 33, 35, 36, 38, 40, 42, 45, 300]) * 1000

# Winsorize: pull the lowest 10% and highest 10% in to the nearest kept value
winsorized = np.array(winsorize(salaries, limits=[0.1, 0.1]))
print("Winsorized values:", winsorized)
print("Winsorized mean:", winsorized.mean())

# Trimmed mean: drop 10% from each end, then average what is left
print("Trimmed mean:", stats.trim_mean(salaries, 0.1))

# Deleting only the one extreme value
print("Mean after deleting 300000:", np.sort(salaries)[:-1].mean())
print("Original mean:", salaries.mean())
```
Output:
```
Winsorized values: [32000 32000 33000 35000 36000 38000 40000 42000 45000 45000]
Winsorized mean: 37800.0
Trimmed mean: 37625.0
Mean after deleting 300000: 36777.77777777778
Original mean: 63100.0
```
The extreme 300000 is pulled down to 45000 when winsorized, and the lowest 30000 is lifted to 32000. The mean falls from 63,100 to about 37,800.
**Likely follow-ups:** 1) *How much to winsorize?* Commonly 1% to 5% per tail, or 5% to 10% for small samples (a rule of thumb, from memory, unverified); choose before looking at results and state it. 2) *Which keeps sample size?* Winsorizing.
**Common mistakes:** Winsorizing silently without telling readers; using it to hide a data error that should be fixed or deleted.

### Q18 ⭐⭐ 🟡 What is the modified z-score (median and MAD), and why is it more robust than the ordinary z-score?
**Asked at:** commonly asked (no company-specific report found). Listed as a gap-fill (standard practice; modified z-score described in the zaps/alooba/statsig reference pages named in the sources file).
**What the interviewer is checking:** Do you know the ordinary z-score can be fooled by the outliers it is trying to find?
**Say this in the interview:** "The modified z-score uses the median and MAD (median absolute deviation) instead of the mean and standard deviation. Because the median and MAD barely move when extremes are present, it still flags them, while the ordinary z-score can be dragged along and miss them."
**Explain simply:**
- MAD = the median of how far each value sits from the median. It is a typical distance that outliers cannot inflate much.
- The ordinary z-score uses the mean and standard deviation, and both are pulled up by outliers. This is called masking: big values hide each other.
- Rule of thumb (Iglewicz and Hoaglin): flag if the modified z is above 3.5 in size. The 0.6745 makes the scale comparable to a normal z-score.
**Formula in plain words:** Modified z = 0.6745 x (value minus median) divided by MAD. In symbols: M = 0.6745 (x − median) / MAD.
**Worked example:** Twelve salaries: nine between Rs 30,000 and 45,000 and three at Rs 3,00,000 to 3,20,000. The mean is 105,083 and the standard deviation 123,714, so even the top salary has a z of only 1.74 and nothing is flagged at the usual 3. The median is 39,000, MAD 6,000, and the modified z of the three is about 29 to 32.
**Excel / Python:**
```python
import numpy as np

# Twelve salaries; three are very high, so they hide each other
salaries = np.array([30, 32, 33, 35, 36, 38, 40, 42, 45, 300, 310, 320]) * 1000

# Ordinary z-score: distance from the mean in standard deviations
mean_salary = salaries.mean()
std_salary = salaries.std(ddof=1)
ordinary_z = (salaries - mean_salary) / std_salary
print("Largest ordinary z:", round(ordinary_z.max(), 2))

# Modified z-score: uses the median and the MAD (median absolute deviation)
median_salary = np.median(salaries)
absolute_gaps = np.abs(salaries - median_salary)
mad = np.median(absolute_gaps)
modified_z = 0.6745 * (salaries - median_salary) / mad
print("Median:", median_salary, " MAD:", mad)
print("Modified z of the top three:", np.round(modified_z[-3:], 2))

# Flag values with modified z above 3.5 (the usual cut-off)
print("Flagged:", salaries[np.abs(modified_z) > 3.5])
```
Output:
```
Largest ordinary z: 1.74
Median: 39000.0  MAD: 6000.0
Modified z of the top three: [29.34 30.46 31.59]
Flagged: [300000 310000 320000]
```
The ordinary z-score misses all three; the modified z-score flags all three.
**Likely follow-ups:** 1) *What if MAD is 0?* More than half the values are identical; use IQR or another method. 2) *Why 3.5?* A convention from Iglewicz and Hoaglin; tune to context.
**Common mistakes:** Forgetting the 0.6745 constant; using it on tiny samples without care.

### Q19 ⭐⭐ 🟡 How would you decide whether an outlier is an error, a rare real event, or a different population?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you investigate before treating, using a logical sequence?
**Say this in the interview:** "I ask three questions in order: is the value impossible or inconsistent, which suggests an error; is it possible and verifiable, which suggests a rare real event; or does it belong to a different group altogether, such as senior management in a salary table. The treatment follows the answer."
**Explain simply:**
- Error: impossible values (age 150), wrong units, typos, duplicated rows. Check the source system, fix or remove, and tell the data owner.
- Rare real event: possible and traceable, such as a one-time bulk order. Keep it, but report with and without it.
- Different population: normal for its own group, odd for the whole. Analyse the group separately (executives apart from staff).
- Practical checks: logic rules, compare with peers (same grade), trace to source, ask the business owner.
**Worked example:** In a small table, E7 has age 150, which is impossible, so an entry error. E8 earns Rs 95 lakh versus an L2 median of Rs 8.5 lakh; possible, so ask HR whether E8 is really a different band (for example a leadership role) before deciding.
**Excel / Python:**
```python
import pandas as pd

# Small employee table with two suspicious rows
employees = pd.DataFrame({
    "employee": ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"],
    "age": [29, 34, 41, 26, 38, 31, 150, 33],
    "salary_lakh": [6, 8, 12, 5, 10, 7, 9, 95],
    "grade": ["L1", "L2", "L3", "L1", "L3", "L2", "L2", "L2"],
})

# Test 1: is the value impossible? (age above 70 is not plausible for an employee)
print("Impossible ages:\n", employees[employees["age"] > 70][["employee", "age"]])

# Test 2: is the value normal for its own peer group?
grade_median = employees.groupby("grade")["salary_lakh"].median()
print("Median salary by grade:\n", grade_median)
print("E8 salary:", employees.loc[7, "salary_lakh"], "vs L2 median", grade_median["L2"])
```
Output:
```
Impossible ages:
   employee  age
6       E7  150
Median salary by grade:
 grade
L1     5.5
L2     8.5
L3    11.0
Name: salary_lakh, dtype: float64
E8 salary: 95 vs L2 median 8.5
```
Age 150 fails the sanity test. The 95 lakh salary passes it but is far from its grade median, so it needs a business answer, not an automatic delete.
**Likely follow-ups:** 1) *What if you cannot reach the owner?* Report with and without the point and state your assumption. 2) *Do you ever just delete?* Only when it is clearly an error.
**Common mistakes:** Deleting by statistics alone; treating every large value as an error.

### Q20 ⭐⭐ 🟡 A single day shows sales ten times the normal level. How do you check whether to include it in a monthly trend analysis?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you investigate a spike before deciding, and show sensitivity?
**Say this in the interview:** "I would not drop it or keep it blindly. First I find out why: a data error, a real one-off such as a bulk order or campaign, or a duplicate load. Then I show the trend with and without that day, and I explain the choice."
**Explain simply:**
- Check the data: duplicate rows, wrong units (paise vs rupees), a test transaction.
- Check the business: a promotion, festival, bulk corporate order, system backfill that dumped many days into one.
- If it is an error, correct it or exclude it. If real but one-off, keep it in revenue totals but use a version without it to judge the underlying trend.
- Always state the choice and its impact.
**Worked example:** Thirty days of sales around Rs 100 thousand, with day 9 at 1,000 (about 9.9 times the typical day). Month total is 3,936 with it and 2,936 without, so that one day is about a quarter of the month's sales.
**Excel / Python:**
```python
import numpy as np

# 30 days of sales (in thousands); day 9 shows 1000
daily_sales = np.array([100, 95, 110, 105, 98, 102, 97, 108, 1000, 101,
                        99, 104, 96, 103, 107, 100, 94, 106, 98, 102,
                        105, 99, 101, 97, 109, 103, 95, 100, 104, 98])

# Compare the spike to a typical day
typical_day = np.median(daily_sales)
print("Typical day:", typical_day, " Spike is", round(daily_sales[8] / typical_day, 1), "x typical")

# Monthly total and average with and without the spike day
without_spike = np.delete(daily_sales, 8)
print("Total with spike:", daily_sales.sum(), " without:", without_spike.sum())
print("Daily mean with spike:", daily_sales.mean(), " without:", round(without_spike.mean(), 1))
```
Output:
```
Typical day: 101.0  Spike is 9.9 x typical
Total with spike: 3936  without: 2936
Daily mean with spike: 131.2  without: 101.2
```
The single day adds about 1,000 to the month total and lifts the daily mean from 101 to 131. That one day, not the trend, drives the monthly number.
**Likely follow-ups:** 1) *What if it was a real bulk order?* Report it separately as a one-off and show the underlying trend without it. 2) *What if it recurs yearly?* Then it is seasonality, not an outlier.
**Common mistakes:** Removing it without checking; keeping it and letting one day set the trend.

### Q21 ⭐⭐ 🟡 What is survivorship bias? Give an example from HR or business data.
**Asked at:** commonly asked (no company-specific report found). The ModernAnalyst page in the sources file lists survivorship bias as an analyst error (snippet-level).
**What the interviewer is checking:** Do you notice when the data only includes the "survivors"?
**Say this in the interview:** "Survivorship bias is drawing conclusions only from the cases that made it through a filter, and ignoring those that dropped out. In HR, an engagement survey of current employees ignores everyone who already left unhappy."
**Explain simply:**
- The missing group is often systematically different, so the visible group looks better than reality.
- Other HR examples: studying the habits of top performers without looking at people with the same habits who failed; hiring success judged only on those who accepted offers.
- Fix: ask who is missing, include leavers (exit interview data, earlier survey waves), and say the limitation.
**Worked example:** Ten people were on a team; six stayed (average engagement 82.8) and four left (average 53.75). A survey of current staff would report 82.8, while the whole group's picture was 71.2.
**Excel / Python:**
```python
import pandas as pd

# Engagement scores (0-100): 6 people who stayed, 4 who left
survey = pd.DataFrame({
    "status": ["stayed"] * 6 + ["left"] * 4,
    "score": [78, 82, 85, 80, 88, 84, 52, 48, 55, 60],
})

# Average of current employees only (what a survivor-only survey shows)
print("Stayed only:", round(survey[survey["status"] == "stayed"]["score"].mean(), 1))
# Average of everyone who was in the team
print("Everyone:", survey["score"].mean())
print("Left only:", survey[survey["status"] == "left"]["score"].mean())
```
Output:
```
Stayed only: 82.8
Everyone: 71.2
Left only: 53.75
```
The survivors-only number looks 11.6 points better than the truth, because the unhappy people have already left.
**Likely follow-ups:** 1) *Famous example?* Armour added to planes only where returning bombers were hit (Abraham Wald's point: the missing planes were hit elsewhere; from memory, unverified). 2) *Is it a type of selection bias?* Yes.
**Common mistakes:** Treating a survey of current staff as a survey of all staff over time.

### Q22 ⭐⭐ 🟡 What is the base rate fallacy? Give a numeric example.
**Asked at:** commonly asked (no company-specific report found). Base rate fallacy appears on the eokultv statistics-mistakes page named in the sources file (snippet-level).
**What the interviewer is checking:** Can you combine an accuracy figure with how common the thing is?
**Say this in the interview:** "The base rate fallacy is ignoring how common something is overall when judging a test result. A model that is 90% accurate can still be mostly wrong about who it flags, when the thing it looks for is rare."
**Explain simply:**
- Base rate = how common the event is before any test (here, 5% of employees resign).
- When the event is rare, even a small false-alarm rate creates many false flags, because the group of non-leavers is so large.
- Precision (the share of flagged people who really leave) is the number to quote, along with accuracy.
**Worked example:** Of 1,000 employees, 50 will resign. The model finds 90% of them (45) and wrongly flags 10% of the 950 stayers (95). Of the 140 flagged, only 45 will leave: about 32%.
**Excel / Python:**
```python
# 1000 employees, 5% will actually resign in the next year
total_employees = 1000
true_leavers = total_employees * 0.05
stayers = total_employees - true_leavers

# The model catches 90% of leavers and wrongly flags 10% of stayers
correctly_flagged = true_leavers * 0.90
wrongly_flagged = stayers * 0.10

# Of everyone flagged, what share will really leave?
share_real = correctly_flagged / (correctly_flagged + wrongly_flagged)
print("Correctly flagged:", correctly_flagged)
print("Wrongly flagged:", wrongly_flagged)
print("Chance a flagged person really leaves:", round(share_real, 3))
```
Output:
```
Correctly flagged: 45.0
Wrongly flagged: 95.0
Chance a flagged person really leaves: 0.321
```
Flagged does not mean "will leave": two out of three flagged people are not leavers. Acting on every flag (say, a retention bonus) wastes money.
**Likely follow-ups:** 1) *Is it Bayes' theorem?* Yes; this is Bayes in counts. 2) *What if the base rate was 30%?* Precision would rise sharply.
**Common mistakes:** Quoting only the model's accuracy; ignoring the false positives.

### Q23 ⭐⭐ 🟡 A 100% conversion rate looks great on a dashboard. Why can small sample sizes make percentages misleading?
**Asked at:** commonly asked (no company-specific report found). Gap-fill (standard practice).
**What the interviewer is checking:** Do you know a percentage needs its denominator, and can you show uncertainty?
**Say this in the interview:** "A 100% rate from 2 visitors is just 2 out of 2. With such a small sample, luck dominates, so the true rate could be anywhere from about 34% to 100%. I show the count next to the percentage and give a confidence range."
**Explain simply:**
- Small samples swing wildly: one more failure would move 2/2 to 2/3, which is 67%.
- A confidence interval is a range of plausible values for the true rate; it is wide for small samples and narrow for large ones.
- Dashboard fixes: show n (the count), hide or grey out rates for tiny groups, and use ranges or minimum sample thresholds.
**Worked example:** Campaign A has 2 of 2 converting (100%). Campaign B has 45 of 60 (75%). Campaign C has 450 of 600 (also 75%). A and B look different, but A's range is vast.
**Excel / Python:**
```python
from statsmodels.stats.proportion import proportion_confint

# (conversions, visitors) for three campaigns
campaigns = {"Campaign A": (2, 2), "Campaign B": (45, 60), "Campaign C": (450, 600)}

for name, (converted, visitors) in campaigns.items():
    rate = converted / visitors
    # 95% Wilson confidence interval: a plausible range for the true rate
    low, high = proportion_confint(converted, visitors, alpha=0.05, method="wilson")
    print(name, "rate:", round(rate, 2), " 95% range:", round(low, 2), "to", round(high, 2))
```
Output:
```
Campaign A rate: 1.0  95% range: 0.34 to 1.0
Campaign B rate: 0.75  95% range: 0.63 to 0.84
Campaign C rate: 0.75  95% range: 0.71 to 0.78
```
The 100% campaign has a 95% range from 0.34 to 1.0, so it says almost nothing. Campaigns B and C have the same 75%, but C's range is far tighter because it has ten times the data.
**Likely follow-ups:** 1) *How big a sample is enough?* Depends on the precision needed; the range tells you. 2) *Same issue for averages?* Yes.
**Common mistakes:** Ranking items by rate without a minimum count; showing percentages with no n.

### Q24 ⭐⭐ 🟡 How would you check your own analysis for Simpson's paradox before sharing it?
**Asked at:** commonly asked (no company-specific report found). Gap-fill (standard practice).
**What the interviewer is checking:** Do you have a routine to catch it before presenting?
**Say this in the interview:** "Before I share a comparison, I split it by the likely confounding variables, such as job level, department or location, and check whether the direction of the difference is the same inside each group as in the total."
**Explain simply:**
- Simpson's paradox: a trend in the total reverses inside the groups, because the groups differ in size and mix.
- Routine: list variables that could affect both the group and the outcome; compute the rate overall and per segment; compare the direction.
- Also look at group sizes: if one programme was mostly given to one level, the totals are not like-for-like.
- If the direction flips, present the segment view and explain why.
**Worked example:** A mentoring programme appears to help: 64% of mentored employees stayed versus 52% of the non-mentored. But within juniors it is 70% vs 80% and within seniors 40% vs 45%: mentored people do worse in both groups. Mentoring was given mostly to juniors, who have higher retention anyway.
**Excel / Python:**
```python
import pandas as pd

# Retention by mentoring programme and job level
data = pd.DataFrame({
    "level": ["Junior", "Junior", "Senior", "Senior"],
    "programme": ["Mentored", "Not mentored", "Mentored", "Not mentored"],
    "employees": [80, 20, 20, 80],
    "retained": [56, 16, 8, 36],
})

# Step 1: overall retention rate per programme
overall = data.groupby("programme")[["employees", "retained"]].sum()
overall["rate"] = overall["retained"] / overall["employees"]
print(overall)

# Step 2: the same rate inside each level
data["rate"] = data["retained"] / data["employees"]
print(data.pivot(index="level", columns="programme", values="rate"))
```
Output:
```
              employees  retained  rate
programme                              
Mentored            100        64  0.64
Not mentored        100        52  0.52
programme  Mentored  Not mentored
level                            
Junior          0.7          0.80
Senior          0.4          0.45
```
Overall, mentored is 12 points better; inside each level it is 5 to 10 points worse. The reversal comes from the mix (80 of 100 mentored are juniors, who retain better).
**Likely follow-ups:** 1) *In Excel?* A pivot table with Level in rows and Programme in columns. 2) *How many variables to check?* Those you have a reason to think affect both.
**Common mistakes:** Only looking at the total; slicing by dozens of variables until something flips.

### Q25 ⭐⭐ 🟡 Which would you trust to make a decision, the overall result or the segment-level result? How do you decide in a Simpson's paradox case?
**Asked at:** commonly asked (no company-specific report found). Gap-fill (standard practice).
**What the interviewer is checking:** Do you know the answer depends on the causal story, not always on one view?
**Say this in the interview:** "Neither automatically. I ask why the groups differ. If the segment variable is a confounder, something that influences both who gets the treatment and the outcome, I trust the segment-level result. If it is a consequence of the treatment, I trust the overall."
**Explain simply:**
- Confounder example: job level affects who is mentored and also affects retention. Comparing within a level removes that distortion, so trust the segments.
- Counter-case: if the programme itself moves people into a segment (for example it causes more promotions), then slicing by that segment hides part of the real effect; trust the overall.
- This needs knowledge of how the data arose; statistics alone cannot tell you. Ideally, confirm with a randomised test.
**Worked example:** In the mentoring data (Q24), juniors dominate the mentored group. Level is set before mentoring starts and affects retention, so it is a confounder. Segment result: mentoring did not raise retention (70% vs 80%; 40% vs 45%). Do not scale the programme based on the overall 64% vs 52%.
**Excel / Python:**
The snippet in Q24 produces both views; no new calculation is needed here. In an interview, say which variable you treat as a confounder and why.
**Likely follow-ups:** 1) *How to be sure?* A randomised pilot. 2) *Could you adjust statistically?* Yes, with regression including the segment variable.
**Common mistakes:** Always trusting the segments (or the total) by rule; not asking which variable comes first in time.

### Q26 ⭐⭐ 🔴 Revenue per customer is dominated by a few very large "whale" customers. How would you report and analyse it?
**Asked at:** commonly asked (no company-specific report found). Gap-fill (standard practice).
**What the interviewer is checking:** Can you report skewed money data honestly and with several lenses?
**Say this in the interview:** "I would not report only the mean, because two whales drive it. I show the median for the typical customer, the share of revenue the top customers give, and report the whales separately, with and without them. For modelling I may use a log scale."
**Explain simply:**
- The mean is revenue divided by customers, so a few giants inflate it above what a typical customer pays.
- Report: median, percentiles (25th, 75th, 90th), concentration (top 1% or top 10 customers' share of revenue), and the mean with and without whales.
- Treat whales as a segment, managed with account management, because losing one is a business risk.
- For trend or model work: log transform, winsorize, or analyse segments separately. Do not delete them from revenue totals.
**Worked example:** 20 customers. Eighteen spend Rs 8,000 to 22,000 and two spend Rs 50 lakh and Rs 32 lakh. Mean Rs 4,23,050; median Rs 15,000; the two whales are 97% of revenue; mean without them Rs 14,500.
**Excel / Python:**
```python
import pandas as pd

# Yearly revenue per customer (Rs); the last two are whales
revenue = pd.Series([12, 15, 9, 20, 18, 11, 14, 16, 10, 13,
                     17, 19, 8, 22, 14, 15, 12, 16, 5000, 3200]) * 1000

# Mean versus median
print("Mean:", revenue.mean(), " Median:", revenue.median())

# How concentrated is revenue? Share from the top 2 customers
top_two_share = revenue.nlargest(2).sum() / revenue.sum()
print("Top 2 customers share of revenue:", round(top_two_share, 3))

# Mean of the regular customers only
regular = revenue.drop(revenue.nlargest(2).index)
print("Mean without the 2 whales:", regular.mean())
```
Output:
```
Mean: 423050.0  Median: 15000.0
Top 2 customers share of revenue: 0.969
Mean without the 2 whales: 14500.0
```
The mean (Rs 4.2 lakh) describes nobody; the typical customer pays Rs 15,000. Concentration (97% from two customers) is itself an important finding.
**Likely follow-ups:** 1) *Remove whales?* No, segment them; they are real revenue. 2) *Which test for comparing groups?* Use medians or rank-based tests, or compare log values.
**Common mistakes:** Reporting only the mean; deleting whales and understating revenue.

### Q27 ⭐ 🟢 What are some common ways statistics are used to mislead in reports and presentations?
**Asked at:** commonly asked (no company-specific report found). Gap-fill (standard practice).
**What the interviewer is checking:** Can you spot misleading statistics, and do you avoid them yourself?
**Say this in the interview:** "The usual tricks are a mean on skewed data, a truncated axis, cherry-picked periods, percentages with no counts, and treating correlation as proof of cause. I try to show the denominator, the full period and the spread."
**Explain simply:**
- Wrong average: mean of skewed data such as salary (use the median).
- Chart tricks: truncated y-axis, dual axes, 3D or distorted pies.
- Selective evidence: cherry-picked dates or segments, survivorship bias.
- Percentages without counts: "up 100%" from 1 to 2; confusing percent with percentage-point change.
- Cause claims: correlation reported as causation; ignoring Simpson's paradox.
- Missing context: no base rate, no sample size, no uncertainty.
**Worked example:** "Attrition doubled" can mean 1 leaver to 2 in a team of 40 (2.5% to 5%). True, but meaningless without the count. A truthful version: "Two leavers this quarter versus one last quarter, in a team of 40."
**Likely follow-ups:** 1) *How do you protect yourself?* Show n, the full period, the median alongside the mean, and a note on method. 2) *Which is the most common?* Averages on skewed data and truncated charts.
**Common mistakes:** Believing misleading stats are always deliberate; many are accidental, so always add context.

### Q28 ⭐ 🟡 Why can a mean be misleading for bimodal or skewed data? What would you report instead?
**Asked at:** commonly asked (no company-specific report found). Gap-fill (standard practice).
**What the interviewer is checking:** Do you look at the shape of the data before choosing a summary?
**Say this in the interview:** "The mean can land in an empty gap where nobody actually sits. For skewed data it is pulled toward the tail. I would show the distribution, and report the median and percentiles, or report each cluster separately."
**Explain simply:**
- Bimodal means two peaks, which often means two different groups mixed together (juniors and seniors, two shifts).
- The mean describes neither group. Even the median can sit in the gap.
- Skewed data (salary): a few large values pull the mean up; the median is steadier.
- Report: histogram, median, percentiles (25th, 75th), and group-wise means when groups are known.
**Worked example:** Twelve salaries: six juniors at Rs 22,000 to 28,000 and six seniors at Rs 95,000 to 1,10,000. Mean Rs 63,500, median Rs 61,500, yet no one earns near those figures.
**Excel / Python:**
```python
import pandas as pd

# Monthly salaries: a junior group and a senior group, nothing in between
salaries = pd.Series([22, 24, 25, 26, 27, 28, 95, 98, 100, 102, 105, 110]) * 1000

print("Mean:", salaries.mean(), " Median:", salaries.median())

# Report each group separately instead
junior_group = salaries[salaries < 60000]
senior_group = salaries[salaries > 60000]
print("Junior group mean:", round(junior_group.mean()), " Senior group mean:", round(senior_group.mean()))

# How many people earn within Rs 10,000 of the overall mean?
near_mean = (salaries - salaries.mean()).abs() < 10000
print("People near the mean:", near_mean.sum())
```
Output:
```
Mean: 63500.0  Median: 61500.0
Junior group mean: 25333  Senior group mean: 101667
People near the mean: 0
```
Both the mean and the median fall in the empty middle. The group means (Rs 25,333 and Rs 1,01,667) describe the workforce much better.
**Likely follow-ups:** 1) *How do you spot bimodality?* A histogram. 2) *Is the mean ever right?* Yes, for roughly symmetric data, or when you need totals.
**Common mistakes:** Quoting one number without plotting; assuming the median always fixes the problem.

### Q29 ⭐ 🟡 What is Anscombe's quartet, and what lesson does it teach analysts?
**Asked at:** commonly asked (no company-specific report found); a differentiator question, not a standard one.
**What the interviewer is checking:** Do you know that summary numbers can hide the real shape of the data, and that you always plot first?
**Say this in the interview:** "Anscombe's quartet is four small datasets with almost identical mean, spread, correlation and trend line, yet they look completely different on a chart: one is a clean line, one is a curve, one has an outlier, one is driven by a single point. The lesson is: never trust summary numbers alone, always plot the data."
**Explain simply:**
- Statistician Francis Anscombe built it in 1973. Each of the four sets has 11 pairs of (x, y) values.
- All four share the same average of x (9) and y (about 7.5), the same spread of y, the same correlation (about 0.82) and the same trend line (y = 3 + 0.5x).
- Plotted, set I is a normal scatter, set II is a curve (a straight line is the wrong model), set III is a perfect line with one outlier pulling it, set IV has all x equal except one far-away point that creates the whole "trend".
- HR link: two teams can have the same average engagement and correlation with tenure, but one may be split into two groups and another driven by one person.
**Worked example:** Below, the four datasets give the same numbers (values copied from the published quartet).
**Excel / Python:**
```python
import numpy as np

# The x values shared by sets I, II and III, and the separate x values of set IV
x_shared = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
x_set_four = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]

# The y values of each of the four sets
y_set_one = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
y_set_two = [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]
y_set_three = [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]
y_set_four = [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]

all_sets = {
    "I": (x_shared, y_set_one),
    "II": (x_shared, y_set_two),
    "III": (x_shared, y_set_three),
    "IV": (x_set_four, y_set_four),
}

# For each set, print mean of x, mean of y, variance of y, slope, intercept, correlation
for set_name, (x_values, y_values) in all_sets.items():
    x_values = np.array(x_values)
    y_values = np.array(y_values)
    slope, intercept = np.polyfit(x_values, y_values, 1)
    correlation = np.corrcoef(x_values, y_values)[0, 1]
    print(set_name, round(x_values.mean(), 2), round(y_values.mean(), 2),
          round(y_values.var(ddof=1), 2), round(slope, 2), round(intercept, 2), round(correlation, 3))
```
Output (columns: mean x, mean y, variance of y, slope, intercept, correlation):
```
I 9.0 7.5 4.13 0.5 3.0 0.816
II 9.0 7.5 4.13 0.5 3.0 0.816
III 9.0 7.5 4.12 0.5 3.0 0.816
IV 9.0 7.5 4.12 0.5 3.0 0.817
```
Four rows with the same numbers, but four completely different pictures when plotted.
**Likely follow-ups:** 1) *Is there a modern version?* Yes, the "Datasaurus Dozen" shows the same idea (from memory, not checked here). 2) *What do you do in practice?* Plot a scatter plot and a histogram before reporting any correlation or average.
**Common mistakes:** Reporting r = 0.82 as proof of a straight-line relationship; thinking the quartet proves statistics are useless (it shows summaries are incomplete, not wrong).

### Q30 ⭐ 🟡 What is regression to the mean? Give an example that could fool a manager.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you spot that an extreme result is partly luck and will usually move back toward average without any intervention?
**Say this in the interview:** "Regression to the mean means that if something was extremely high or low the first time, it is likely to be closer to average the next time, purely because part of the first result was luck. A manager can wrongly credit a training programme for the improvement."
**Explain simply:**
- Any score is partly real skill and partly luck or noise (a bad day, an easy batch of customers).
- If you pick the people with the lowest first scores, many of them were unlucky, so on average they score higher next time anyway.
- The same happens in reverse: the top performers drop a little.
- The fix: compare against a control group chosen the same way but not given the training, and do not pick groups only by an extreme result.
**Worked example:** 1,000 employees; each monthly score = steady skill + random luck (simulated, so we know the truth). We pick the bottom 10% in month 1 and "send them to training", but in this simulation no training happens at all.
**Excel / Python:**
```python
import numpy as np

# Random generator with a fixed seed so results repeat
random_generator = np.random.default_rng(42)
number_of_employees = 1000

# Each person has a stable underlying skill
true_skill = random_generator.normal(70, 8, number_of_employees)

# Each month's score is skill plus random luck
month_one_score = true_skill + random_generator.normal(0, 8, number_of_employees)
month_two_score = true_skill + random_generator.normal(0, 8, number_of_employees)

# Find the lowest 10% and highest 10% of month one
bottom_ten_percent = month_one_score <= np.percentile(month_one_score, 10)
top_ten_percent = month_one_score >= np.percentile(month_one_score, 90)

# Average month one and month two score for each group
print("Bottom 10%: month 1 =", round(month_one_score[bottom_ten_percent].mean(), 1),
      " month 2 =", round(month_two_score[bottom_ten_percent].mean(), 1))
print("Top 10%:    month 1 =", round(month_one_score[top_ten_percent].mean(), 1),
      " month 2 =", round(month_two_score[top_ten_percent].mean(), 1))
```
Output:
```
Bottom 10%: month 1 = 48.7  month 2 = 60.8
Top 10%:    month 1 = 88.9  month 2 = 80.6
```
The "trainees" improved by about 12 points and the stars fell by about 8 points with no intervention at all. A manager who only looked at the bottom group would claim the training worked.
**Likely follow-ups:** 1) *How do you prove a programme works?* Randomly split people into trained and untrained groups and compare the change. 2) *When is regression strongest?* When the measure is noisy (low correlation between months; here it was about 0.48).
**Common mistakes:** Calling it a "law" that forces numbers to the average (it is a statistical effect of selecting extremes); explaining the drop of top performers as "complacency" with no evidence.

### Q31 ⭐ 🟡 What is Goodhart's law? Give an example of a KPI that stops being useful once it becomes a target.
**Asked at:** commonly asked (no company-specific report found); gap-fill question, standard practice.
**What the interviewer is checking:** Do you understand that people change behaviour to hit a metric, so the metric stops measuring what you wanted?
**Say this in the interview:** "Goodhart's law says that when a measure becomes a target, it stops being a good measure. If I reward 'tickets closed', people will close tickets fast without fixing the problem, so the KPI looks great while the real outcome gets worse."
**Explain simply:**
- A KPI (key performance indicator, a number used to judge performance) is usually a stand-in for something we really care about, such as customer problems being solved.
- Once pay, bonus or praise depends on the stand-in, people optimise the stand-in, sometimes by gaming it.
- HR examples: recruiters judged on "time to fill" accept weaker candidates; managers judged on "attrition" discourage resignations or reclassify exits; "training hours" rises with useless courses.
- Defence: pair the KPI with a quality check (a counter-metric) and review the KPI regularly.
**Worked example:** Two support agents are ranked by tickets closed. Asha closes 40 and 2 are reopened; Ravi closes 55 and 22 are reopened. Ravi tops the "closed" ranking, but Asha solved more problems for good (38 vs 33).
**Excel / Python:**
```python
import pandas as pd

# Tickets closed and tickets that the customer had to reopen
ticket_counts = pd.DataFrame({
    "agent": ["Asha", "Ravi"],
    "closed": [40, 55],
    "reopened": [2, 22],
})

# Tickets that really stayed solved
ticket_counts["still_solved"] = ticket_counts["closed"] - ticket_counts["reopened"]

print(ticket_counts)
```
Output:
```
  agent  closed  reopened  still_solved
0  Asha      40         2            38
1  Ravi      55        22            33
```
Ranked by "closed" Ravi wins; ranked by "still solved" Asha wins. The target changed the winner.
**Likely follow-ups:** 1) *How do you reduce the problem?* Use several balanced metrics and spot-check quality. 2) *Is it the same as Campbell's law?* Closely related (Campbell's law is the social-science version; from memory).
**Common mistakes:** Dropping KPIs altogether; adding one more single number that can also be gamed.

### Q32 ⭐ 🟡 Why might a log transformation help with outliers and skewed data, and what is the downside when explaining results?
**Asked at:** commonly asked (no company-specific report found); gap-fill question.
**What the interviewer is checking:** Do you know a standard fix for right-skewed data and can you still explain results in plain business terms?
**Say this in the interview:** "A log transformation replaces each value by its logarithm, which compresses big values a lot and small values a little. Salaries, revenue and handling times are often right-skewed, and the log makes them more symmetric and pulls in extreme highs. The downside is that results are on the log scale, so I must convert back and explain them as percentage or ratio differences, which is harder for non-technical audiences."
**Explain simply:**
- Logarithm: the power you raise a base to. The natural log of 60 is about 4.09; of 12 is about 2.48.
- Equal steps on the log scale mean equal percentage changes, not equal rupee changes. A 5x gap (12 to 60) becomes a small, steady gap.
- Needs values above zero (log of 0 is undefined; people sometimes use log(1 + value)).
- Downside: the average of logs, converted back, is the geometric mean, not the ordinary mean, so the number reported is different and needs a careful label.
**Worked example:** Ten salaries in lakh: 4, 5, 5, 6, 6, 7, 8, 9, 12, 60.
**Excel / Python:**
```python
import numpy as np

# Salaries in lakh; the 60 is a very high earner
salaries_in_lakh = np.array([4, 5, 5, 6, 6, 7, 8, 9, 12, 60])

# Ordinary mean and median
print("mean:", salaries_in_lakh.mean())
print("median:", np.median(salaries_in_lakh))

# Natural log of every salary
log_salaries = np.log(salaries_in_lakh)

# Average on the log scale, then converted back to lakh (the geometric mean)
average_log_salary = log_salaries.mean()
geometric_mean = np.exp(average_log_salary)
print("average of logs:", round(average_log_salary, 3))
print("back-converted (geometric mean):", round(geometric_mean, 2))

# Gap between 12 and 60 in lakh vs on the log scale
print("raw gap:", 60 - 12)
print("log gap:", round(np.log(60) - np.log(12), 2))
```
Output:
```
mean: 12.2
median: 6.5
average of logs: 2.099
back-converted (geometric mean): 8.16
raw gap: 48
log gap: 1.61
```
The one huge salary drags the mean to 12.2 lakh; the log-based average (8.16) is much less affected. In Excel use `=LN(B2)` for each value, then `=EXP(AVERAGE(C2:C11))` for the geometric mean (works in all Excel versions; not run in Excel here). In a log model, a difference of 0.10 on the log scale is about a 10.5% change (`exp(0.10) - 1 = 0.1052`).
**Likely follow-ups:** 1) *What if there are zeros?* Use log(1 + value) and say so. 2) *Is it the same as removing outliers?* No, every point is kept, just compressed.
**Common mistakes:** Calling the back-converted average "the mean"; applying log to negative or zero values; presenting log-scale coefficients without translating to percentages.

### Q33 ⭐ 🟡 How do you report results when removing an outlier changes the conclusion?
**Asked at:** commonly asked (no company-specific report found); gap-fill question.
**What the interviewer is checking:** Honesty and judgement: do you hide the sensitivity or show it?
**Say this in the interview:** "I report both versions side by side, say clearly which one I recommend and why, and flag that the conclusion depends on one point. I never silently delete it. I also investigate whether the point is an error, a real rare case, or a different group."
**Explain simply:**
- If one point flips the answer, the finding is fragile, and decision makers must know that.
- Steps: (1) check the data source for a mistake; (2) run the analysis with and without; (3) try a robust method (median, Spearman rank correlation); (4) state which result you act on and the evidence for that choice.
- Write the decision rule in advance if possible, to avoid choosing the version you like.
**Worked example:** Tenure (years 1 to 10) vs engagement score for 10 employees. Employee 10 scored 40, far below the rest.
**Excel / Python:**
```python
from scipy import stats

# Years of tenure and engagement score for ten employees
tenure_years = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
engagement_score = [60, 62, 58, 66, 63, 67, 64, 69, 65, 40]

# Correlation with everyone included
correlation_all, p_value_all = stats.pearsonr(tenure_years, engagement_score)

# Correlation after leaving out the last employee (the outlier)
correlation_without, p_value_without = stats.pearsonr(tenure_years[:-1], engagement_score[:-1])

# A robust check: Spearman rank correlation with everyone included
spearman_all, _ = stats.spearmanr(tenure_years, engagement_score)

print("With the outlier:    r =", round(correlation_all, 2), " p =", round(p_value_all, 3))
print("Without the outlier: r =", round(correlation_without, 2), " p =", round(p_value_without, 3))
print("Spearman, all data:  rho =", round(spearman_all, 2))
```
Output:
```
With the outlier:    r = -0.24  p = 0.509
Without the outlier: r = 0.71  p = 0.031
Spearman, all data:  rho = 0.25
```
With everyone, the link looks weak and negative (not significant); without one person, it is clearly positive. The honest report shows both and explains that the conclusion rests on one employee, whom I would investigate first. (p-value: the chance of seeing a link this strong or stronger by luck alone if there were really none; below 0.05 is the usual "significant" line.)
**Likely follow-ups:** 1) *Which one do you pick?* The one supported by the investigation (error means remove, genuine means keep and report both). 2) *Small sample?* With 10 points, sensitivity is expected; say so.
**Common mistakes:** Presenting only the version that supports the story; removing the point because it "spoils" the result.

### Q34 ⭐ 🟡 What is the Texas sharpshooter fallacy?
**Asked at:** commonly asked (no company-specific report found); gap-fill question.
**What the interviewer is checking:** Do you understand that finding a pattern after looking, and then pretending you predicted it, is invalid?
**Say this in the interview:** "A man fires bullets at a barn wall, then paints a target around the tightest cluster and claims he is a sharpshooter. In analytics it means mining lots of data for any pattern, then presenting it as if that was the hypothesis all along. With enough slicing, random noise always gives something that looks real."
**Explain simply:**
- Hypothesis first, data second. Otherwise a "significant" result may be chance.
- If you test 20 things at the 5% level, you expect about one false alarm even when nothing is going on.
- Examples: "attrition is higher among employees born in March, in Pune, and on the 3rd floor" after checking 60 slices.
- Avoid it: state the question before looking, correct for multiple tests (for example Bonferroni: divide the 0.05 limit by the number of tests), and confirm on fresh data.
**Worked example:** Simulate 2,000 studies where there is no real effect, each running 20 comparisons between two groups of 30.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

random_generator = np.random.default_rng(7)
number_of_studies = 2000
studies_with_a_false_alarm = 0

for study in range(number_of_studies):
    smallest_p_value = 1.0
    # Twenty comparisons where both groups come from the same population
    for comparison in range(20):
        group_a = random_generator.normal(0, 1, 30)
        group_b = random_generator.normal(0, 1, 30)
        p_value = stats.ttest_ind(group_a, group_b).pvalue
        smallest_p_value = min(smallest_p_value, p_value)
    # Count the study if any comparison looked "significant"
    if smallest_p_value < 0.05:
        studies_with_a_false_alarm += 1

print("Share with at least one false 'finding':", studies_with_a_false_alarm / number_of_studies)
print("Theory: 1 - 0.95**20 =", round(1 - 0.95 ** 20, 3))
```
Output:
```
Share with at least one false 'finding': 0.651
Theory: 1 - 0.95**20 = 0.642
```
Even with no real effect, about 64% of studies that try 20 comparisons find something "significant".
**Likely follow-ups:** 1) *How does it differ from cherry-picking?* Cherry-picking selects the supporting data; the sharpshooter draws the target after the fact (they overlap). 2) *Is exploring data wrong?* No, but label it as exploratory and test findings on new data.
**Common mistakes:** Reporting only the "winning" slice without saying how many were tried.

### Q35 ⭐ 🟡 Why is a pie chart or dual-axis chart sometimes considered misleading?
**Asked at:** commonly asked (no company-specific report found); gap-fill question.
**What the interviewer is checking:** Chart literacy: can you choose a chart that does not trick the reader?
**Say this in the interview:** "Humans compare lengths on a common baseline well but compare angles and areas poorly, so pie slices of 24, 25 and 26 percent look identical, and many slices are unreadable. Dual-axis charts let you choose two different scales, so you can make two lines appear to move together or cross, which suggests a relationship that may not exist."
**Explain simply:**
- Pie: fine for 2 to 4 parts when one part is clearly bigger. Bad for similar slices, many categories or comparing across several pies. A sorted bar chart is better.
- Dual-axis: left and right scales are chosen by the author. Changing either scale moves where the lines cross. Two series that both trend upward also look "related" even if unconnected (a shared trend, not a cause).
- Better: two separate small charts stacked, or index both series to 100 at the start.
**Worked example:** Headcount (100 to 133) and cafeteria cost in lakh (20 to 27) over 6 months both rise, so a dual-axis chart shows them moving together. Their correlation is very high, but both simply grow with company size.
**Excel / Python:**
```python
import numpy as np

# Monthly headcount and cafeteria cost (lakh) over six months
headcount = np.array([100, 105, 111, 118, 126, 133])
cafeteria_cost = np.array([20, 21, 22, 24, 25, 27])

# How strongly the two lines move together
correlation = np.corrcoef(headcount, cafeteria_cost)[0, 1]
print("Correlation:", round(correlation, 3))
```
Output:
```
Correlation: 0.995
```
Near-perfect "match", but it only shows that both grow with time and company size. The pie example: slices of 24, 25, 26 and 25 add to 100 and are almost impossible to rank by eye.
**Likely follow-ups:** 1) *When is dual axis acceptable?* Rarely; when units truly differ and both axes start at sensible, clearly labelled values. 2) *What replaces a pie?* A sorted bar chart.
**Common mistakes:** 3-D pies (distort area further); using dual axes to "prove" correlation.

### Q36 ⭐ 🔴 What is the ecological fallacy? Give an example.
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Do you know that patterns in group averages may not hold for individuals?
**Say this in the interview:** "The ecological fallacy is assuming that a relationship seen between group averages also holds for the individuals inside those groups. For example, departments with more average overtime may have higher average engagement, but inside each department, people who work more overtime can be less engaged."
**Explain simply:**
- Aggregated data (department, city, branch averages) hides what happens inside groups.
- Group-level patterns can come from group differences (for example department type or seniority) rather than individual behaviour.
- Rule: group-level data supports group-level conclusions only. Individual conclusions need individual-level data.
- It is related to Simpson's paradox: both come from mixing levels.
**Worked example (synthetic data built to show the effect):** 4 departments, 50 employees each. Departments with higher average overtime have higher average engagement, but within each department more overtime means lower engagement.
**Excel / Python:**
```python
import numpy as np
import pandas as pd

random_generator = np.random.default_rng(3)
rows = []

# Department baseline: average overtime hours and average engagement
department_baselines = {"A": (5, 50), "B": (10, 60), "C": (15, 70), "D": (20, 80)}

for department, (overtime_base, engagement_base) in department_baselines.items():
    overtime = overtime_base + random_generator.normal(0, 2, 50)
    # Inside a department, 1 extra overtime hour lowers engagement by about 2 points
    engagement = engagement_base - 2.0 * (overtime - overtime_base) + random_generator.normal(0, 2, 50)
    for overtime_value, engagement_value in zip(overtime, engagement):
        rows.append((department, overtime_value, engagement_value))

employees = pd.DataFrame(rows, columns=["department", "overtime", "engagement"])

# Department averages and their correlation
department_averages = employees.groupby("department")[["overtime", "engagement"]].mean()
print(department_averages.round(1))
print("Correlation of the 4 department averages:",
      round(department_averages["overtime"].corr(department_averages["engagement"]), 2))

# Correlation inside each department
for department, group in employees.groupby("department"):
    print(department, "within-department correlation:",
          round(group["overtime"].corr(group["engagement"]), 2))
```
Output:
```
            overtime  engagement
department                      
A                5.0        49.6
B               10.3        59.8
C               14.7        71.1
D               19.8        80.6
Correlation of the 4 department averages: 1.0
A within-department correlation: -0.9
B within-department correlation: -0.91
C within-department correlation: -0.88
D within-department correlation: -0.92
```
At department level, more overtime goes with higher engagement (r = 1.0 on 4 points); inside every department the relationship is strongly negative (about -0.9). Concluding "overtime raises engagement for a person" would be the fallacy.
**Likely follow-ups:** 1) *How do you avoid it?* Use individual-level data where the claim is about individuals. 2) *Does the reverse also apply?* Yes, individual patterns need not hold for groups.
**Common mistakes:** Using regional averages to make claims about individuals; confusing it with the plain fact that averages hide spread.

### Q37 ⭐ 🔴 What is the difference between an outlier, a high-leverage point and an influential point?
**Asked at:** commonly asked (no company-specific report found); regression-diagnostics topic.
**What the interviewer is checking:** Regression depth: do you know that unusual does not automatically mean damaging?
**Say this in the interview:** "An outlier has an unusual y value given its x, a high-leverage point has an unusual x value (far from the other x's), and an influential point is one that really changes the fitted line when removed. High leverage plus being off the trend is what makes a point influential."
**Explain simply:**
- Outlier: far from the line vertically (large residual, the gap between actual and predicted).
- High leverage: far from the other points horizontally; it has the power to pull the line, whether or not it does.
- Influential: removing it changes the slope or predictions a lot. Measured by Cook's distance (a score of how much the fit changes if the point is deleted).
- Not all three overlap: a high-leverage point lying on the trend is not harmful; an outlier in the middle of the x range has little pull.
**Worked example:** Salary against tenure for 12 employees (slope 0.42 lakh per year). We add one extra person in three different ways.
**Excel / Python:**
```python
import numpy as np
import statsmodels.api as sm

# Tenure in years and salary in lakh for 12 employees
tenure = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], dtype=float)
salary = np.array([4.0, 4.4, 4.9, 5.2, 5.8, 6.1, 6.6, 6.9, 7.5, 7.8, 8.2, 8.6])

def fit_line(tenure_values, salary_values):
    design_matrix = sm.add_constant(tenure_values)
    return sm.OLS(salary_values, design_matrix).fit()

original_fit = fit_line(tenure, salary)
print("Original slope:", round(original_fit.params[1], 3))

# Three scenarios for one extra person (tenure, salary)
scenarios = {
    "A: 30 years, salary on the trend": (30.0, 4.0 + 0.45 * (30 - 1)),
    "B: 6.5 years, salary far too high": (6.5, 12.0),
    "C: 30 years, salary far below trend": (30.0, 6.0),
}

for scenario_name, (extra_tenure, extra_salary) in scenarios.items():
    new_tenure = np.append(tenure, extra_tenure)
    new_salary = np.append(salary, extra_salary)
    new_fit = fit_line(new_tenure, new_salary)
    influence = new_fit.get_influence()
    leverage = influence.hat_matrix_diag[-1]
    cooks_distance = influence.cooks_distance[0][-1]
    print(scenario_name, "| slope:", round(new_fit.params[1], 3),
          "| leverage:", round(leverage, 2), "| Cook's D:", round(cooks_distance, 2))
```
Output:
```
Original slope: 0.421
A: 30 years, salary on the trend | slope: 0.448 | leverage: 0.8 | Cook's D: 16.45
B: 6.5 years, salary far too high | slope: 0.421 | leverage: 0.08 | Cook's D: 0.46
C: 30 years, salary far below trend | slope: 0.081 | leverage: 0.8 | Cook's D: 21.65
```
B is an outlier with low leverage: the slope does not move. C has high leverage and is off the trend: the slope collapses from 0.42 to 0.08, so it is influential. A has high leverage too (0.8) and sits only slightly off the line; its slope changes little (0.42 to 0.45), although Cook's D is large because the original points fit the line very tightly, so even a small miss at a far-away x counts. This shows the difference between "could pull" and "did pull"; I judge by the change in slope as well as Cook's D, since cutoffs vary.
**Likely follow-ups:** 1) *What do you do with an influential point?* Check it for error, then report results with and without. 2) *Which statistic measures leverage?* The hat value; points above about 2 to 3 times the average leverage are flagged (rule of thumb, from memory).
**Common mistakes:** Deleting every outlier; assuming leverage points are always bad.

### Q38 ⭐ 🔴 What is the masking effect in outlier detection, and how can you avoid it?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Do you know that outliers can hide each other when the method itself uses the mean and standard deviation?
**Say this in the interview:** "Masking is when several outliers inflate the mean and standard deviation so much that none of them look unusual to the z-score method. I avoid it by using robust measures, such as the median and MAD, the modified z-score, or the IQR method, which are not pulled by extreme values."
**Explain simply:**
- The z-score uses the mean and standard deviation, and extreme values distort both.
- With a few big outliers, the standard deviation grows, so the z-scores shrink and fall under the usual cutoff of 3.
- Robust methods use the median (middle value), the MAD (median absolute deviation, the typical distance from the median) or quartiles, which ignore a few extreme values.
- Also, remove or investigate points one at a time, or use robust multivariate methods (Q40).
- Limit: even the IQR rule can be masked when more than about a quarter of the values are extreme, because then Q3 itself is pulled up.
**Worked example:** Monthly overtime hours of 13 employees: ten normal values (5 to 10) and three very high ones (70, 75, 80).
**Excel / Python:**
```python
import numpy as np

overtime_hours = np.array([5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 70, 75, 80], dtype=float)

# Method 1: ordinary z-score
mean_hours = overtime_hours.mean()
standard_deviation = overtime_hours.std(ddof=1)
z_scores = (overtime_hours - mean_hours) / standard_deviation
flagged_by_z = overtime_hours[np.abs(z_scores) > 3]
print("mean:", round(mean_hours, 1), " standard deviation:", round(standard_deviation, 1))
print("Largest z-score:", round(z_scores.max(), 2))
print("Flagged by z-score (|z| > 3):", flagged_by_z)

# Method 2: modified z-score using median and MAD
median_hours = np.median(overtime_hours)
mad = np.median(np.abs(overtime_hours - median_hours))
modified_z_scores = 0.6745 * (overtime_hours - median_hours) / mad
flagged_by_modified_z = overtime_hours[np.abs(modified_z_scores) > 3.5]
print("median:", median_hours, " MAD:", mad)
print("Flagged by modified z-score (> 3.5):", flagged_by_modified_z)

# Method 3: IQR fences
first_quartile, third_quartile = np.percentile(overtime_hours, [25, 75])
iqr = third_quartile - first_quartile
lower_fence = first_quartile - 1.5 * iqr
upper_fence = third_quartile + 1.5 * iqr
flagged_by_iqr = overtime_hours[(overtime_hours < lower_fence) | (overtime_hours > upper_fence)]
print("IQR fences:", lower_fence, upper_fence, " Flagged by IQR:", flagged_by_iqr)
```
Output:
```
mean: 23.1  standard deviation: 29.7
Largest z-score: 1.92
Flagged by z-score (|z| > 3): []
median: 8.0  MAD: 2.0
Flagged by modified z-score (> 3.5): [70. 75. 80.]
IQR fences: 2.5 14.5  Flagged by IQR: [70. 75. 80.]
```
The three extreme values inflate the mean to 23.1 and the standard deviation to 29.7, so the largest z-score is only 1.92 and nothing is flagged. The robust methods flag all three (the 0.6745 and 3.5 are the standard modified z-score constants, from Iglewicz and Hoaglin, quoted from memory).
**Likely follow-ups:** 1) *What is swamping?* The opposite problem: normal points wrongly flagged because outliers distort the fit. 2) *Which method do you start with?* A plot plus the IQR rule.
**Common mistakes:** Trusting |z| > 3 on small or heavily contaminated data; assuming IQR is immune when a large share of the data is extreme.

### Q39 ⭐ 🔴 What is Berkson's paradox? Give an example.
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Do you understand selection bias that creates a false relationship between two unrelated traits?
**Say this in the interview:** "Berkson's paradox is when two traits that are unrelated in the whole population show a negative relationship inside a group that was selected on one or both. For example, if a company hires people with a high combined score of skill and interview, among those hired the strong-interview people look less skilled."
**Explain simply:**
- The selection rule (for example "skill plus interview must be high enough") creates the link.
- To pass, a person weak on one trait must be strong on the other, so within the selected group the traits trade off.
- It is a type of collider bias (selecting on a result of both traits).
- Warning: analysing only hired, admitted, hospitalised or surveyed people can give such false patterns.
**Worked example (simulation):** 100,000 applicants with independent skill and interview scores (standard normal). Hire those whose sum is above 2.
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(5)
number_of_applicants = 100000

# Two independent scores, each on a standardised scale
skill_score = random_generator.normal(0, 1, number_of_applicants)
interview_score = random_generator.normal(0, 1, number_of_applicants)

# Correlation among all applicants
print("All applicants, correlation:", round(np.corrcoef(skill_score, interview_score)[0, 1], 3))

# Hire only when the combined score is high
is_hired = (skill_score + interview_score) > 2.0
print("Share hired:", round(is_hired.mean(), 3))

# Correlation among hired people only
print("Hired only, correlation:", round(np.corrcoef(skill_score[is_hired], interview_score[is_hired])[0, 1], 3))
```
Output:
```
All applicants, correlation: 0.004
Share hired: 0.08
Hired only, correlation: -0.732
```
Skill and interview performance are unrelated overall (0.004) but strongly negative (-0.73) among the 8% who were hired.
**Likely follow-ups:** 1) *How is it different from Simpson's paradox?* Simpson's is a reversal caused by mixing groups; Berkson's is a false link created by selecting a subset. 2) *How to avoid it?* Check how the data were selected and include the people who were filtered out.
**Common mistakes:** Concluding "good interviewers are worse at the job" from hired employees only.

### Q40 ⭐ 🔴 How do you detect outliers when the data has several variables, for example height and weight together?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Do you know that a point can be normal on each variable but unusual in combination?
**Say this in the interview:** "I would look at the variables together, with a scatter plot first, and use Mahalanobis distance, which measures how far a point is from the centre of the data while allowing for how the variables move together. A tall, very light person can look normal on height and on weight separately yet be a clear outlier as a pair."
**Explain simply:**
- Univariate checks (one variable at a time) miss combinations that break the usual relationship.
- Mahalanobis distance is a distance measure adjusted for the scale and correlation of the variables. Squared distance is compared to a chi-square cutoff (a standard statistical table for distances), for example the 99.9th percentile.
- Other options: isolation forest, local outlier factor (machine-learning methods, mention by name only). Use robust versions if there are many outliers (masking, Q38).
- Always check flagged points for errors before removing.
**Worked example (synthetic):** 300 people whose weight follows height, plus one person at 185 cm and 50 kg.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

random_generator = np.random.default_rng(11)

# 300 realistic people: taller people weigh more
heights = random_generator.normal(170, 8, 300)
weights = 0.9 * (heights - 170) + 68 + random_generator.normal(0, 4, 300)

# Add one unusual person: tall and very light
heights = np.append(heights, [185])
weights = np.append(weights, [50])
data = np.column_stack([heights, weights])

# Centre and spread of the data, allowing for correlation
average_values = data.mean(axis=0)
covariance_matrix = np.cov(data, rowvar=False)
inverse_covariance = np.linalg.inv(covariance_matrix)

# Squared Mahalanobis distance for every person
differences = data - average_values
squared_distances = np.einsum("ij,jk,ik->i", differences, inverse_covariance, differences)

# Cutoff: 99.9th percentile of chi-square with 2 variables
cutoff = stats.chi2.ppf(0.999, df=2)

print("Last person height z-score:", round((heights[-1] - heights.mean()) / heights.std(ddof=1), 2))
print("Last person weight z-score:", round((weights[-1] - weights.mean()) / weights.std(ddof=1), 2))
print("Squared distance of last person:", round(squared_distances[-1], 1), " cutoff:", round(cutoff, 1))
print("Number flagged:", int((squared_distances > cutoff).sum()))
```
Output:
```
Last person height z-score: 2.0
Last person weight z-score: -2.22
Squared distance of last person: 55.3  cutoff: 13.8
Number flagged: 1
```
On each variable alone, the person is only about 2 standard deviations away (not alarming), but combined their distance is 55.3 against a cutoff of 13.8, so they are flagged. Exactly one person is flagged.
**Likely follow-ups:** 1) *What if there are many variables?* Mahalanobis still works (change df to the number of variables); for large or messy data use isolation forest. 2) *Assumption?* Roughly bell-shaped data for the chi-square cutoff.
**Common mistakes:** Checking each column separately and calling the data clean; using the cutoff blindly on skewed data.

### Q41 ⭐ 🔴 A dashboard shows average handling time falling every month, yet customers complain more. What statistical pitfalls could explain this?
**Asked at:** commonly asked (no company-specific report found); gap-fill scenario question.
**What the interviewer is checking:** Structured thinking: can you list plausible causes (metric gaming, mix change, wrong average) and say how you would test each?
**Say this in the interview:** "Handling time is only a proxy for good service. It can fall because agents rush calls or end them early (Goodhart's law), so customers call back; because the mix of calls changed toward easy ones (a Simpson's-type mix effect); because the average hides skew or a long tail of angry customers; or because calls are measured differently. I would check repeat-call rate, resolution rate, handling time by call type and the median, not just the average."
**Explain simply:**
- Goodhart's law (Q31): if agents are judged on speed, speed improves and quality can fall.
- Hidden cost: unresolved calls come back as extra calls. The time per call falls, but total time per customer problem can rise.
- Mix effect: more simple queries in the mix lowers the average even if each type got slower.
- Average vs median: the mean can fall because a few very long calls disappeared, while typical customers are still unhappy; or the complaints come from a small group the average hides.
- Survivorship bias: customers who gave up and left do not appear in the data.
- Wrong direction of cause: complaints may be driving agents to rush (a different story).
**Worked example:** 1,000 calls each month. Average handling time falls 10, 8, 6 minutes while calls resolved on the first call fall from 800 to 600.
**Excel / Python:**
```python
import pandas as pd

monthly_calls = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar"],
    "calls": [1000, 1000, 1000],
    "resolved_first_call": [800, 700, 600],
    "average_handling_minutes": [10, 8, 6],
})

# Calls that were not resolved the first time and will return
monthly_calls["repeat_calls"] = monthly_calls["calls"] - monthly_calls["resolved_first_call"]

# Total handling time spent in the month
monthly_calls["total_minutes"] = monthly_calls["calls"] * monthly_calls["average_handling_minutes"]

print(monthly_calls.to_string())
```
Output:
```
  month  calls  resolved_first_call  average_handling_minutes  repeat_calls  total_minutes
0   Jan   1000                  800                        10           200          10000
1   Feb   1000                  700                         8           300          8000
2   Mar   1000                  600                         6           400          6000
```
The dashboard's number improves every month, while the repeat calls double from 200 to 400; the real quality is getting worse. (The three-month figures are made up for illustration.)
**Likely follow-ups:** 1) *What would you add to the dashboard?* First-call resolution, repeat-contact rate, customer satisfaction and handling time by call type. 2) *How do you prove the cause?* Compare agents or teams where the target was introduced and where it was not, or look before and after.
**Common mistakes:** Defending the dashboard because the number "improved"; proposing one cause without a way to test it.

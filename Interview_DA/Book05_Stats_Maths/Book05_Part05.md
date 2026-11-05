# Book 5 — Statistics & Maths for Data Analysts | Part 5: Sampling, Bias, CLT, Confidence Intervals 🟡

**Target:** 50 questions | **Actual:** 51 questions
**Scope:** populations and samples, sampling methods, sampling and survey bias, the Central Limit Theorem, standard error, and confidence intervals (interpretation and calculation).

### Q1 ⭐⭐⭐ 🟢 Why do analysts use a sample instead of surveying the whole population?
**Asked at:** commonly asked (no company-specific report found); the population/sample basics appear in every statistics prep list we found.
**What the interviewer is checking:** Do you know the practical trade-off: a well-chosen sample gives a reliable answer at a fraction of the cost and time?
**Say this in the interview:** "The population is everyone I care about; a sample is a smaller group drawn from it. Surveying everyone is usually too slow, too expensive or impossible, so I study a properly chosen sample and use statistics to say how far off my estimate could be."
**Explain simply:**
- **Population:** every employee, customer or invoice you want to learn about. **Sample:** the part you actually measure.
- A **parameter** is a true number about the population (average satisfaction of all staff); a **statistic** is the same number computed from the sample. We use the statistic to estimate the parameter.
- Reasons: cost, time, some tests destroy the item (testing product lifetime), and a population may be unreachable (past candidates).
- A sample is only trustworthy if it is chosen fairly (Q2) and big enough (Q12).
**Worked example:** A company has 8,000 employees. Surveying all of them takes weeks. A random sample of 400 gives, at 95% confidence, a margin of error of about plus or minus 4.9 percentage points for a satisfaction percentage (worst case, 50%).
**Excel / Python:**
```python
import numpy as np

# size of the sample we survey
sample_size = 400

# worst-case proportion (50% gives the widest margin)
worst_case_proportion = 0.5

# standard error of a proportion, then 95% margin of error (1.96 is the 95% z value)
standard_error = np.sqrt(worst_case_proportion * (1 - worst_case_proportion) / sample_size)
margin_of_error = 1.96 * standard_error

print("Margin of error (percentage points):", round(margin_of_error * 100, 2))
```
Output: `Margin of error (percentage points): 4.9`. Surveying 400 of 8,000 people already gives an answer within about 5 points.
**Likely follow-ups:** 1) *When would you NOT sample?* When the population is small, or every record is already in the database (then just use all of it). 2) *Does a bigger sample always help?* Only if it is chosen fairly (Q36).
**Common mistakes:** Calling any small group a "sample" without asking how it was chosen; mixing up parameter and statistic.

### Q2 ⭐⭐⭐ 🟢 What is simple random sampling?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you define it precisely (every member has an equal chance) and say how you would do it?
**Say this in the interview:** "Simple random sampling means every member of the population has the same chance of being picked, and every possible group of that size is equally likely. In practice I number everyone in the list and let a random number generator pick the IDs."
**Explain simply:**
- You need a complete list of the population (the **sampling frame**), such as the employee master file.
- Picking is done by chance only, not by judgement or convenience, which is why it avoids picker's bias.
- Usually done **without replacement** (a person cannot be picked twice).
- Weakness: a small random sample can, by luck, miss a small group (for example the 10 HR staff among 1,000).
**Worked example:** Employee IDs 1001 to 1020; pick 5 at random.
**Excel / Python:**
```python
import numpy as np

# fixed seed so the result can be repeated
random_generator = np.random.default_rng(42)

# the sampling frame: all employee IDs
employee_ids = np.arange(1001, 1021)

# pick 5 different IDs, each equally likely
chosen_ids = random_generator.choice(employee_ids, size=5, replace=False)
print(chosen_ids)
```
Output: `[1014 1009 1012 1002 1020]`. Excel (2007+): put IDs in A2:A21, `=RAND()` in B2:B21, sort by column B and take the top 5 (not run in Excel here).
**Likely follow-ups:** 1) *Why a seed?* So the same sample can be reproduced for audit. 2) *With or without replacement?* Without, unless the method needs it (bootstrapping, Q43).
**Common mistakes:** Calling "the first 50 rows" or "whoever answers" random; forgetting you need a full list first.

### Q3 ⭐⭐⭐ 🟢 What is sampling bias, and why is it dangerous?
**Asked at:** commonly asked; bias types are listed in TryExponent's statistics-bias page (search snippet only).
**What the interviewer is checking:** Do you understand that a biased sample misleads even when it is big, and that statistics cannot fix it afterwards?
**Say this in the interview:** "Sampling bias happens when the way I picked the sample makes some people more likely to be included than others, so the sample no longer looks like the population. It is dangerous because the result is systematically wrong and gives a false sense of confidence."
**Explain simply:**
- Bias is a **systematic** push in one direction, unlike random error, which averages out.
- A bigger sample does not cure it (Q36); it just makes you more sure of the wrong answer.
- Common causes: convenient groups, only volunteers, missing groups from the list, people who do not reply.
**Worked example:** 1,000 employees: 600 office staff averaging about 7.5 out of 10 on engagement and 400 plant staff averaging about 5.5. If the survey is emailed only to office staff, HR sees about 7.45, while the true company average is about 6.64.
**Excel / Python:**
```python
import numpy as np

# fixed seed to reproduce the example
random_generator = np.random.default_rng(1)

# simulated engagement scores (1 to 10) for office and plant staff
office_scores = random_generator.normal(7.5, 1.0, 600).clip(1, 10)
plant_scores = random_generator.normal(5.5, 1.2, 400).clip(1, 10)

# true average of everybody
all_scores = np.concatenate([office_scores, plant_scores])

print("True company average:", round(all_scores.mean(), 2))
print("Office-only average:", round(office_scores.mean(), 2))
```
Output: `True company average: 6.64` and `Office-only average: 7.45`. The office-only survey overstates engagement by almost one point.
**Likely follow-ups:** 1) *How do you spot it?* Compare sample makeup (department, location) with the HR master data. 2) *How do you reduce it?* Random selection, stratification, weighting (Q46).
**Common mistakes:** Believing "n = 5,000 is big so it must be fine."

### Q4 ⭐⭐⭐ 🟢 What is selection bias? Give an example.
**Asked at:** commonly asked; selection bias is named in TryExponent's bias list (snippet only).
**What the interviewer is checking:** Can you separate it from other biases and give a clean HR example?
**Say this in the interview:** "Selection bias is when the people or records that end up in my analysis are not a fair picture of the group I want to study, because of how they were chosen or who dropped out. Example: judging a training programme only on employees who completed it."
**Explain simply:**
- It is the umbrella problem of "who got into the data". Sampling bias, survivorship, non-response and voluntary response are all forms of it.
- It appears before analysis; no formula afterwards fixes it unless you know how selection happened.
- Ask: "Who is missing, and why?"
**Worked example:** HR compares performance of employees who completed a leadership course with those who did not and finds completers score higher. But managers chose who attended (their best people), so the gap may reflect who was selected, not what the course did. Suppose 200 attended with an average rating of 4.2 and 800 did not with 3.4; that 0.8 gap mixes course effect and selection effect.
**Likely follow-ups:** 1) *How would you fix this?* Random assignment, or compare people matched on earlier ratings. 2) *Is it the same as sampling bias?* Sampling bias is selection bias arising from how a sample is drawn.
**Common mistakes:** Treating it as a data-cleaning issue; forgetting that dropouts also create selection.

### Q5 ⭐⭐⭐ 🟢 What is the Central Limit Theorem, in simple words?
**Asked at:** commonly asked; Dataford lists it as a Wells Fargo data analyst question (search snippet, unverified); also in PrachHub's CLT page.
**What the interviewer is checking:** Can you state it without jargon and say why it matters?
**Say this in the interview:** "If I take many random samples and calculate each sample's average, those averages form a bell-shaped curve centred on the true average, even if the original data is not bell-shaped. The more people in each sample, the narrower that curve."
**Explain simply:**
- It is about the **average of samples**, not the raw data.
- The spread of those sample averages is the **standard error**: population SD divided by the square root of the sample size.
- Rule of thumb: 30 or more usually works for mildly skewed data (Q26).
- This is what lets us build confidence intervals and tests using the normal curve.
**Formula in plain words:** Standard error equals the data's standard deviation divided by the square root of the sample size: SE = σ / √n.
**Worked example:** Monthly salaries are right-skewed (a few very high earners). Population mean about 3,617, SD about 2,366. Taking 5,000 samples of 30 people each, the sample averages centre near 3,610 with spread 439, matching 2,366 / √30 = 432.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# fixed seed to reproduce results
random_generator = np.random.default_rng(7)

# a skewed salary population of 100,000 people (monthly, in rupees)
monthly_salaries = random_generator.lognormal(mean=10.5, sigma=0.6, size=100000) / 12
print("Population mean:", round(monthly_salaries.mean()), "SD:", round(monthly_salaries.std()))

# for each sample size, draw 5,000 samples and record each sample average
for sample_size in (2, 30, 200):
    sample_averages = []
    for repeat in range(5000):
        one_sample = random_generator.choice(monthly_salaries, sample_size)
        sample_averages.append(one_sample.mean())
    sample_averages = np.array(sample_averages)
    expected_se = monthly_salaries.std() / np.sqrt(sample_size)
    print(sample_size, "mean of averages:", round(sample_averages.mean()),
          "spread:", round(sample_averages.std()), "theory:", round(expected_se),
          "skew:", round(stats.skew(sample_averages), 2))
```
Output: `Population mean: 3617 SD: 2366`, then `2 ... 3636 1668 1673 1.6`, `30 ... 3610 439 432 0.44`, `200 ... 3616 169 167 0.13`. Skewness (lopsidedness) falls from 2.17 in the raw data towards 0 for the averages: they become bell-shaped.
**Likely follow-ups:** 1) *Does the data itself become normal?* No, only the sample average. 2) *Needs normal data?* No (Q8).
**Common mistakes:** Saying "the data becomes normal with large samples."

### Q6 ⭐⭐⭐ 🟢 What is a confidence interval?
**Asked at:** commonly asked; appears in PrachHub, techprep.app and Medium CI question lists (snippets).
**What the interviewer is checking:** Do you know it is a range for an unknown true value, built from a sample, with a stated reliability?
**Say this in the interview:** "A confidence interval is a range around my sample estimate that is likely to contain the true population value. A 95% interval means that if I repeated the survey many times, about 95% of the intervals built this way would contain the true value."
**Explain simply:**
- A sample gives one **point estimate** (a single number); the interval admits it is uncertain.
- Structure: estimate plus or minus margin of error.
- Wider interval means more caution, narrower means more precision (Q11, Q12).
**Formula in plain words:** Sample average, plus or minus (critical value times standard error): x̄ ± t × s/√n.
**Worked example:** 20 employees' engagement scores average 7.105 (SD 0.719). SE = 0.719/√20 = 0.161. With 19 degrees of freedom the t value is 2.093, so the 95% interval is 6.77 to 7.44.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# engagement scores (out of 10) from 20 sampled employees
scores = np.array([6.5, 7.2, 8.0, 5.8, 7.5, 6.9, 7.8, 6.2, 7.1, 8.3,
                   6.6, 7.4, 5.9, 7.7, 6.8, 7.0, 8.1, 6.4, 7.3, 7.6])

# sample average, sample SD (ddof=1 means divide by n-1) and sample size
sample_mean = scores.mean()
sample_sd = scores.std(ddof=1)
sample_size = len(scores)

# standard error and t value for 95% with n-1 degrees of freedom
standard_error = sample_sd / np.sqrt(sample_size)
t_value = stats.t.ppf(0.975, sample_size - 1)

# the interval
lower_limit = sample_mean - t_value * standard_error
upper_limit = sample_mean + t_value * standard_error
print(round(sample_mean, 3), round(sample_sd, 3), round(standard_error, 3), round(t_value, 3))
print("95% CI:", round(lower_limit, 2), "to", round(upper_limit, 2))
```
Output: `7.105 0.719 0.161 2.093` and `95% CI: 6.77 to 7.44`. Excel (2010+): `=CONFIDENCE.T(0.05, STDEV.S(A2:A21), 20)` returns the margin of error, about 0.34 (not run in Excel here).
**Likely follow-ups:** 1) *Why t not z here?* Small sample, SD estimated (Q34). 2) *Is it a probability about the true mean?* No (Q30).
**Common mistakes:** Reading it as "95% of employees score in this range."

### Q7 ⭐⭐⭐ 🟢 What is the difference between standard deviation and standard error?
**Asked at:** commonly asked; techprep.app's CI list covers SE (snippet only).
**What the interviewer is checking:** Do you know SD describes spread of individual values and SE describes how precise the sample average is?
**Say this in the interview:** "Standard deviation measures how spread out individual employees are around the average. Standard error measures how much the sample average itself would wobble from sample to sample. SE is the SD divided by the square root of the sample size, so it shrinks as the sample grows, while SD does not."
**Explain simply:**
- SD answers: "how different are people from each other?" SE answers: "how far off might my average be?"
- Collecting more data does not change SD much, but SE keeps falling.
- SE is what goes into confidence intervals; SD is what goes into describing the data.
**Formula in plain words:** SE equals SD divided by the square root of n: SE = s / √n.
**Worked example:** Using the 20 engagement scores from Q6: SD 0.719 means most people sit within about 0.7 points of the average; SE 0.161 means the average itself is pinned down to about 0.16. With 80 people and the same SD, SE would be 0.719/√80 = 0.080 (half), while SD stays 0.719.
**Excel / Python:**
```python
import numpy as np

# SD of the data and the sample size from the Q6 example
sample_sd = 0.719
sample_size = 20

# standard error with 20 people
standard_error_20 = sample_sd / np.sqrt(20)

# standard error if we had 80 people and the same SD
standard_error_80 = sample_sd / np.sqrt(80)

print(round(standard_error_20, 3), round(standard_error_80, 3))
```
Output: `0.161 0.08`. Quadrupling the sample halves the SE. Excel: `=STDEV.S(A2:A21)/SQRT(COUNT(A2:A21))` (2010+; not run in Excel here).
**Likely follow-ups:** 1) *Which goes in a CI?* SE. 2) *Does SD shrink with n?* No.
**Common mistakes:** Quoting SE as if it were the spread of employees.

### Q8 ⭐⭐⭐ 🟡 Why is the Central Limit Theorem useful when the data itself is not normally distributed?
**Asked at:** commonly asked; Dataford tags the "why is CLT useful" question to a Wells Fargo DA listing (snippet only, unverified).
**What the interviewer is checking:** Do you understand that CLT lets us use normal-curve tools on averages even for skewed data?
**Say this in the interview:** "Real HR data like salary or tenure is skewed, but my conclusions are usually about averages. CLT says averages from reasonably large random samples behave like a normal distribution, so I can still build confidence intervals and run tests, without needing the raw data to be bell-shaped."
**Explain simply:**
- Tools such as z and t intervals assume the sample average is roughly normal, not the data.
- CLT supplies that: the skew fades as sample size grows.
- It does not rescue tiny samples, extreme outliers, or biased sampling (Q26, Q48).
**Worked example:** The skewed salaries in Q5 have skewness 2.17. Averages of 30 have skewness 0.44 and averages of 200 have 0.13, nearly symmetrical, so a normal-based interval is reasonable.
**Excel / Python:** Same simulation as Q5; the lines to read are the skew values `1.6`, `0.44`, `0.13` for sample sizes 2, 30 and 200. The lopsidedness of the averages fades quickly as the sample grows.
**Likely follow-ups:** 1) *What if the data is extremely skewed?* Need a larger n, or bootstrap (Q43). 2) *Is this about the median too?* The standard CLT is for averages and sums.
**Common mistakes:** Claiming the data becomes normal; applying CLT to a sample of 8.

### Q9 ⭐⭐⭐ 🟡 How do you interpret a 95% confidence interval?
**Asked at:** commonly asked; interpretation is the core of CI lists such as techprep.app (snippet only).
**What the interviewer is checking:** Can you give the correct long-run meaning without saying "95% probability the mean is inside"?
**Say this in the interview:** "If we repeated the sampling many times and built an interval each time, about 95% of those intervals would contain the true value. For my one interval, I say I am 95% confident the true value is in it, meaning the method is right 95% of the time."
**Explain simply:**
- The interval changes from sample to sample; the true value stays fixed.
- "95%" describes the **method's** success rate, not a probability for one finished interval (Q30).
- Practical reading: the plausible values for the true average are in this range.
**Worked example:** True average engagement is 7.0. We simulate 1,000 surveys of 50 people and build an interval each time. 947 of the 1,000 intervals contain 7.0, close to the promised 95%.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# fixed seed to reproduce results
random_generator = np.random.default_rng(3)

# the true average that we pretend not to know, and survey settings
true_mean = 7.0
sample_size = 50
number_of_surveys = 1000
t_value = stats.t.ppf(0.975, sample_size - 1)

# count how many intervals catch the true mean
intervals_containing_truth = 0
for survey in range(number_of_surveys):
    sample_scores = random_generator.normal(true_mean, 1.2, sample_size)
    sample_mean = sample_scores.mean()
    standard_error = sample_scores.std(ddof=1) / np.sqrt(sample_size)
    lower_limit = sample_mean - t_value * standard_error
    upper_limit = sample_mean + t_value * standard_error
    if lower_limit <= true_mean <= upper_limit:
        intervals_containing_truth += 1

print(intervals_containing_truth, "out of", number_of_surveys)
```
Output: `947 out of 1000`. About 95% of intervals work; about 5% miss, and we never know which ones.
**Likely follow-ups:** 1) *Does 95% mean 95% of employees are in it?* No. 2) *What changes if I want 99%?* Wider interval (Q29).
**Common mistakes:** "There is a 95% chance the mean is between a and b" (Q30).

### Q10 ⭐⭐⭐ 🟡 Calculate a 95% confidence interval for the mean: sample mean 50, standard deviation 10, sample size 100.
**Asked at:** commonly asked; PrachHub shows a similar worked 95% CI (snippet only).
**What the interviewer is checking:** Can you calculate it step by step and state the answer in words?
**Say this in the interview:** "Standard error is 10 divided by the square root of 100, which is 1. The margin of error is 1.96 times 1, about 1.96. So the 95% interval is 48.04 to 51.96."
**Explain simply:**
- Step 1: SE = 10/√100 = 1.
- Step 2: margin of error = 1.96 × 1 = 1.96 (1.96 is the normal-curve value that leaves 2.5% in each tail).
- Step 3: 50 − 1.96 = 48.04 and 50 + 1.96 = 51.96.
- With n = 100 the exact t value is 1.984, giving 48.02 to 51.98; the difference is tiny.
**Formula in plain words:** Mean, plus or minus 1.96 times (SD divided by the square root of n): x̄ ± 1.96 × s/√n.
**Worked example:** Average tenure is 50 months in a sample of 100 employees, SD 10. We are 95% confident the true average tenure is between about 48 and 52 months.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# given values
sample_mean = 50
sample_sd = 10
sample_size = 100

# standard error
standard_error = sample_sd / np.sqrt(sample_size)

# z version (1.96) and t version (n-1 = 99 degrees of freedom)
z_value = 1.96
t_value = stats.t.ppf(0.975, sample_size - 1)

print("z interval:", sample_mean - z_value * standard_error, sample_mean + z_value * standard_error)
print("t value:", round(t_value, 3))
print("t interval:", round(sample_mean - t_value * standard_error, 2),
      round(sample_mean + t_value * standard_error, 2))
```
Output: `z interval: 48.04 51.96`, `t value: 1.984`, `t interval: 48.02 51.98`. Excel (2010+): `=CONFIDENCE.NORM(0.05, 10, 100)` returns 1.96 (not run in Excel here).
**Likely follow-ups:** 1) *What if n were 400?* SE 0.5, interval 49.02 to 50.98. 2) *z or t?* t if SD is estimated (Q34).
**Common mistakes:** Forgetting to divide by √n; using SD as the margin.

### Q11 ⭐⭐⭐ 🟡 What is the margin of error, and what affects its size?
**Asked at:** commonly asked; techprep.app lists SE vs margin of error (snippet only).
**What the interviewer is checking:** Do you know the three levers: confidence level, variability, sample size?
**Say this in the interview:** "Margin of error is the plus-or-minus part of a confidence interval: critical value times standard error. It grows with higher confidence and with more variability in the data, and shrinks as the sample gets bigger."
**Explain simply:**
- Higher confidence (99% vs 95%) gives a bigger critical value, so a wider margin.
- More variable data (larger SD) gives a bigger margin.
- Larger sample gives a smaller margin, but with diminishing returns (need 4x the people to halve it).
- It covers only random sampling error, not bias.
**Formula in plain words:** Margin of error equals critical value times SD divided by the square root of n.
**Worked example:** With n = 100: SD 5 gives 0.98, SD 10 gives 1.96, SD 20 gives 3.92. With SD 10 fixed: critical values are 1.645 (90%), 1.96 (95%), 2.576 (99%).
**Excel / Python:**
```python
import numpy as np

# margin of error for three different SDs, sample size fixed at 100
for sample_sd in (5, 10, 20):
    margin = 1.96 * sample_sd / np.sqrt(100)
    print("SD", sample_sd, "margin", round(margin, 2))
```
Output: `SD 5 margin 0.98`, `SD 10 margin 1.96`, `SD 20 margin 3.92`. Doubling the spread doubles the margin.
**Likely follow-ups:** 1) *Does it include bias?* No. 2) *How do I shrink it cheaply?* Lower variability (better measurement), or accept lower confidence.
**Common mistakes:** Thinking a small margin of error means the survey is unbiased.

### Q12 ⭐⭐⭐ 🟡 How does sample size affect the width of a confidence interval?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know width falls with the square root of n, not in proportion to n?
**Say this in the interview:** "A larger sample makes the interval narrower, because the standard error is SD divided by the square root of n. To halve the width I need four times the sample, so there are diminishing returns."
**Explain simply:**
- Width = 2 × margin of error, and the margin falls with 1/√n.
- 4x the sample halves the width; 100x the sample cuts it to a tenth.
- A tight interval around a biased estimate is still wrong (Q36).
**Worked example:** SD 10, 95% confidence: n = 25 gives width 7.84; n = 100 gives 3.92; n = 400 gives 1.96; n = 1,600 gives 0.98.
**Excel / Python:**
```python
import numpy as np

# standard deviation of the data
sample_sd = 10

# try four sample sizes, each four times the last
for sample_size in (25, 100, 400, 1600):
    standard_error = sample_sd / np.sqrt(sample_size)
    margin = 1.96 * standard_error
    full_width = 2 * margin
    print(sample_size, "SE", standard_error, "margin", round(margin, 2), "width", round(full_width, 2))
```
Output: `25 SE 2.0 margin 3.92 width 7.84`, `100 SE 1.0 margin 1.96 width 3.92`, `400 SE 0.5 margin 0.98 width 1.96`, `1600 SE 0.25 margin 0.49 width 0.98`. Every 4x in people halves the width.
**Likely follow-ups:** 1) *Is it worth surveying 10x more?* Width only falls by about 3.2x. 2) *What else narrows it?* Lower SD, lower confidence level.
**Common mistakes:** Assuming doubling the sample halves the width.

### Q13 ⭐⭐ 🟢 What is stratified sampling, and when would you use it?
**Asked at:** commonly asked; stratified vs cluster appears in Statology and Statsig pages (snippets only).
**What the interviewer is checking:** Do you know you split the population into groups first, then sample from every group?
**Say this in the interview:** "In stratified sampling I divide the population into meaningful groups called strata, such as department, then randomly sample from each group, usually in proportion to its size. I use it when groups differ and I want every one represented."
**Explain simply:**
- Strata must not overlap, and every person belongs to exactly one.
- Guarantees small groups are not missed by luck, and often gives tighter estimates.
- Needs a list with the grouping variable (department) for everyone.
**Worked example:** 100 employees: 60 Sales, 30 IT, 10 HR. A 20% stratified sample gives 12, 6 and 2 people, total 20.
**Excel / Python:**
```python
import numpy as np
import pandas as pd

# fixed seed so the salary column is repeatable
random_generator = np.random.default_rng(11)

# a table of 100 employees: department, city and salary
employees = pd.DataFrame({
    "emp_id": range(1, 101),
    "dept": ["Sales"] * 60 + ["IT"] * 30 + ["HR"] * 10,
    "city": ["Pune"] * 25 + ["Delhi"] * 25 + ["Goa"] * 25 + ["Kochi"] * 25,
})
employees["salary"] = random_generator.integers(25000, 90000, 100)

# take 20% randomly from inside each department
stratified_sample = employees.groupby("dept", group_keys=False).sample(frac=0.2, random_state=5)

print(stratified_sample["dept"].value_counts().to_dict(), len(stratified_sample))
```
Output: `{'Sales': 12, 'IT': 6, 'HR': 2} 20`. Each department keeps its share.
**Likely follow-ups:** 1) *Proportional or equal allocation?* Proportional keeps the mix; equal helps compare small groups (then weight). 2) *Versus quota?* Quota is non-random (Q42).
**Common mistakes:** Mixing it up with cluster sampling (Q23).

### Q14 ⭐⭐ 🟢 What is cluster sampling, and when would you use it?
**Asked at:** commonly asked; Statology and Statsig compare it with stratified (snippets only).
**What the interviewer is checking:** Do you know you randomly pick whole groups, then survey people inside them, to save cost?
**Say this in the interview:** "In cluster sampling I divide the population into naturally occurring groups, like offices, randomly choose a few whole groups, and survey everyone in them. I use it when a full list is hard to get or travelling to every site is costly."
**Explain simply:**
- Clusters should each look like a small version of the whole population.
- Cheaper and simpler logistically, but less precise if clusters differ from each other.
- Example: select 2 of 4 city offices and survey all staff there.
**Worked example:** Using the same 100-employee table (25 per city): randomly choose 2 of 4 cities and survey all their employees, which gives 50 people from Delhi and Goa.
**Excel / Python:**
```python
import numpy as np

# employees table as built in Q13 (city column: Pune, Delhi, Goa, Kochi, 25 each)
city_names = employees["city"].unique()

# randomly choose 2 whole cities
random_generator = np.random.default_rng(2)
chosen_cities = random_generator.choice(city_names, size=2, replace=False)

# keep everyone who works in the chosen cities
cluster_sample = employees[employees["city"].isin(chosen_cities)]
print(sorted(chosen_cities), len(cluster_sample))
```
Output: `['Delhi', 'Goa'] 50`. Everyone in two offices was surveyed, none in the others.
**Likely follow-ups:** 1) *Weakness?* Higher sampling error if clusters differ. 2) *One-stage vs two-stage?* Two-stage samples people inside chosen clusters too.
**Common mistakes:** Sampling a few people from every cluster (that is closer to stratified).

### Q15 ⭐⭐ 🟢 What is systematic sampling?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the "every k-th item after a random start" rule and its one risk?
**Say this in the interview:** "In systematic sampling I pick a random starting point and then take every k-th record, where k is population size divided by sample size. It is quick and spreads the sample evenly. The risk is a hidden repeating pattern in the list that lines up with k."
**Explain simply:**
- k = N / n. For 10,000 records and 200 wanted, k = 50.
- Needs an ordered list; random start keeps it fair.
- Danger: if the list repeats every 50 rows (say weekly cycles), the sample can be badly skewed.
**Worked example:** From the 100-employee table, we want 20 people, so k = 5. A random start of 3 picks rows 3, 8, 13 ... which are IDs 4, 9, 14, 19, 24 (rows are counted from 0).
**Excel / Python:**
```python
import numpy as np

# employees table as built in Q13
step_size = 5

# random start between 0 and step_size - 1
random_start = int(np.random.default_rng(4).integers(0, step_size))

# take every 5th row beginning at the random start
systematic_sample = employees.iloc[random_start::step_size]

print(random_start, len(systematic_sample), systematic_sample["emp_id"].head(5).tolist())
```
Output: `3 20 [4, 9, 14, 19, 24]`. In Excel, helper column `=MOD(ROW()-ROW($A$2), 5)=3` marks every 5th row (not run in Excel here).
**Likely follow-ups:** 1) *Biggest risk?* Hidden periodicity. 2) *Is it random?* Only the start is random.
**Common mistakes:** Starting at row 1 every time; using it on a list sorted by salary without thinking.

### Q16 ⭐⭐ 🟢 What is the difference between probability sampling and non-probability sampling?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the key difference is whether chance, with known probabilities, decides who is picked?
**Say this in the interview:** "In probability sampling every member has a known, non-zero chance of selection, so I can calculate margins of error and generalise. In non-probability sampling selection depends on convenience or judgement, so I cannot measure sampling error properly."
**Explain simply:**
- **Probability:** simple random, stratified, cluster, systematic.
- **Non-probability:** convenience, quota, snowball, voluntary response, judgement.
- Non-probability is cheaper and fine for early exploration or hard-to-reach groups, but results should not be generalised with a confidence level.
**Worked example:** Randomly picking 200 employee IDs from the HR master is probability sampling. Emailing a link and analysing whoever clicks is non-probability.
**Likely follow-ups:** 1) *When would you still use non-probability?* Pilot work, rare populations (Q40). 2) *Can weighting fix it?* Partly (Q46).
**Common mistakes:** Quoting a "95% confidence" for a convenience sample as if it were random.

### Q17 ⭐⭐ 🟢 What is convenience sampling, and what is wrong with it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you name the weakness (hidden bias, cannot generalise) and a better alternative?
**Say this in the interview:** "Convenience sampling means using whoever is easiest to reach, like colleagues on my floor. It is fast and cheap, but the easy-to-reach people are often different from everyone else, so results are biased and I cannot measure how wrong they might be."
**Explain simply:**
- Examples: surveying the people at the canteen, using only the people who reply first.
- Problem: not everyone had a chance of being picked, so the sample may over-represent one type.
- Acceptable for brainstorming or pilot testing a questionnaire, not for decisions.
- Fix: draw a random sample from the HR master list.
**Worked example:** An HR analyst checks policy awareness by asking 30 people in the head office. Remote and plant employees, who may know much less, are never asked, so awareness looks higher than it really is (see the office-only effect in Q3).
**Likely follow-ups:** 1) *Is it ever fine?* For pilots, with a clear warning. 2) *How to improve it?* Random selection or at least quotas and weighting.
**Common mistakes:** Believing a large convenience sample becomes representative.

### Q18 ⭐⭐ 🟢 What is survivorship bias? Give an example.
**Asked at:** commonly asked (no company-specific report found); the sources file lists survivorship bias and exit-interview filtering as an HR-style scenario (CASRAI guide, snippet only).
**What the interviewer is checking:** Do you notice that the data you can see may only include the "survivors", not everyone who started?
**Say this in the interview:** "Survivorship bias is when I only analyse the people or things that made it through a filter and forget the ones that dropped out, so my picture looks better than reality."
**Explain simply:**
- The people who left, failed or were removed are missing from your data, so the remaining group looks healthier than the full group was.
- HR example: an engagement survey sent only to **current** employees misses everyone who already quit, often the unhappiest ones.
- Another example: studying only successful hires' interview scores to decide what predicts success, ignoring candidates you rejected or who left in month two.
- Fix: include the leavers (exit data, earlier survey waves, a cohort of everyone hired in a year).
**Worked example:** 1,000 people were hired last year. 600 stayed with an average engagement score of 7.5 out of 10. 400 left; before leaving their average was 5.0. A survey of current staff reports 7.5, but the true average of the whole hiring cohort is (600 x 7.5 + 400 x 5.0) / 1000 = 6.5.
**Excel / Python:**
```python
# Headcount and engagement score for people who stayed vs people who left
stayers = 600
leavers = 400
stayer_score = 7.5
leaver_score = 5.0

# A survey of current employees only sees the stayers
survey_result = stayer_score

# The honest average for the whole hiring cohort includes the leavers
cohort_average = (stayers * stayer_score + leavers * leaver_score) / (stayers + leavers)

print("Survey of current staff:", survey_result)
print("True cohort average:", cohort_average)
```
```text
Survey of current staff: 7.5
True cohort average: 6.5
```
The survey overstates engagement by a full point because the unhappy leavers are invisible.
**Likely follow-ups:** 1) *How do you spot it?* Ask "who is missing from this data and why?" 2) *How is it different from selection bias?* It is a type of selection bias where the filter is "survived".
**Common mistakes:** Treating the visible group as everyone; only reading success stories.

### Q19 ⭐⭐ 🟢 What is non-response bias?
**Asked at:** commonly asked (no company-specific report found); the sources file lists non-response among the bias types prep sites ask (TryExponent, Albert.io, snippets only).
**What the interviewer is checking:** Do you know that people who do not answer may differ from people who do?
**Say this in the interview:** "Non-response bias happens when the people who did not reply are systematically different from those who did, so the replies do not represent the whole group."
**Explain simply:**
- Low response alone is not the problem; **different** non-responders is the problem.
- HR example: very busy shift workers or very disengaged staff may ignore the survey, so scores look better than reality.
- Check it by comparing respondents to the workforce (department, grade, location) and by following up with a sample of non-responders.
- A higher response rate lowers the risk but does not remove it.
**Worked example:** 1,000 employees are surveyed and 300 reply; 80% of repliers are satisfied. Suppose the 700 silent employees are only 50% satisfied. The true satisfaction is (300 x 0.80 + 700 x 0.50) / 1000 = 59%, not 80%.
**Excel / Python:**
```python
# Who replied and who stayed silent
responders = 300
non_responders = 700

# Satisfaction rate in each group (the silent group's rate is an assumption)
responder_satisfaction = 0.80
non_responder_satisfaction = 0.50

# Weighted average gives the true company-wide rate
true_satisfaction = (responders * responder_satisfaction + non_responders * non_responder_satisfaction) / 1000

print("Reported:", responder_satisfaction)
print("True:", true_satisfaction)
```
```text
Reported: 0.8
True: 0.59
```
The survey reports 80% but the real figure is 59%, because silent employees are less satisfied.
**Likely follow-ups:** 1) *How do you reduce it?* Reminders, short surveys, anonymity, follow-up with non-responders. 2) *Can you fix it afterwards?* Partly, by weighting (Q46).
**Common mistakes:** Assuming "300 is a big sample, so it is fine"; ignoring who is missing.

### Q20 ⭐⭐ 🟢 What is voluntary response bias?
**Asked at:** commonly asked (no company-specific report found); the sources file lists voluntary response in the AP Statistics sampling taxonomy (Albert.io, snippet only).
**What the interviewer is checking:** Can you tell why "opt-in" surveys over-represent strong opinions?
**Say this in the interview:** "Voluntary response bias is when people choose themselves into the sample, and people with strong feelings choose to respond much more often than people who are neutral."
**Explain simply:**
- It is a special case of non-response bias where the **respondent decides** to take part (an open link, a suggestion box, a poll in a group chat).
- Results skew towards the very happy and especially the very unhappy.
- Random selection by the analyst avoids it; self-selection does not.
**Worked example:** 1,000 employees, of whom 200 are strongly unhappy with the canteen. In an open poll, 40% of the unhappy vote but only 5% of the others. Votes: 80 unhappy and 40 others, so 66.7% of the votes are complaints, while the true share is 20%.
**Excel / Python:**
```python
# Population split into strongly unhappy and everyone else
unhappy_employees = 200
other_employees = 800

# Chance that each type bothers to vote in the open poll
unhappy_vote_rate = 0.40
other_vote_rate = 0.05

# Expected number of votes from each group
unhappy_votes = unhappy_employees * unhappy_vote_rate
other_votes = other_employees * other_vote_rate

# Share of votes that are complaints vs the true share
poll_share = unhappy_votes / (unhappy_votes + other_votes)
true_share = unhappy_employees / (unhappy_employees + other_employees)

print("Votes:", unhappy_votes, other_votes)
print("Poll share unhappy:", round(poll_share, 3))
print("True share unhappy:", true_share)
```
```text
Votes: 80.0 40.0
Poll share unhappy: 0.667
True share unhappy: 0.2
```
The poll makes the problem look more than three times bigger than it is.
**Likely follow-ups:** 1) *Is it useless then?* It is fine for ideas and feedback, not for measuring percentages. 2) *Fix?* Randomly pick people and chase their replies.
**Common mistakes:** Quoting poll percentages as if they described all employees.

### Q21 ⭐⭐ 🟢 What is undercoverage bias?
**Asked at:** commonly asked (no company-specific report found); the sources file lists undercoverage in the AP Statistics taxonomy (Albert.io, snippet only).
**What the interviewer is checking:** Do you check whether your list of people (the sampling frame) actually includes everyone?
**Say this in the interview:** "Undercoverage bias is when some part of the population has no chance of being picked because it is missing from the list I sample from."
**Explain simply:**
- The **sampling frame** is the list you draw from (an email list, a payroll file).
- If the list leaves groups out, no amount of random picking brings them back.
- HR example: an email-only survey misses factory staff without company email.
- Different from non-response: here they were never asked at all.
**Worked example:** 1,200 employees: 900 have email (70% satisfied) and 300 factory workers do not (50% satisfied). An email survey says 70%; the truth is (900 x 0.70 + 300 x 0.50) / 1200 = 65%.
**Excel / Python:**
```python
# Employees reachable by email and employees missing from the email list
emailed_group = 900
factory_group = 300

# Satisfaction in each group (the factory rate is an assumption)
emailed_satisfaction = 0.70
factory_satisfaction = 0.50

# True rate across everybody
true_satisfaction = (emailed_group * emailed_satisfaction + factory_group * factory_satisfaction) / (emailed_group + factory_group)

print("Email survey says:", emailed_satisfaction)
print("True satisfaction:", true_satisfaction)
```
```text
Email survey says: 0.7
True satisfaction: 0.65
```
The email survey is five points too high because a whole group was never invited.
**Likely follow-ups:** 1) *Fix?* Use the full HR master list and add paper or kiosk surveys. 2) *Compare with non-response?* Undercoverage is not being on the list; non-response is being on it but not answering.
**Common mistakes:** Assuming "random sample of the list" means "random sample of the people".

### Q22 ⭐⭐ 🟢 What is the difference between sampling error and non-sampling error?
**Asked at:** commonly asked (no company-specific report found); general prep-site topic, not company-specific in the sources file.
**What the interviewer is checking:** Do you know that some error shrinks with bigger samples and some never does?
**Say this in the interview:** "Sampling error is the natural luck-of-the-draw difference between a random sample and the population; it shrinks as the sample grows. Non-sampling error is everything else, such as bad questions, missing groups, or data-entry mistakes, and a bigger sample does not fix it."
**Explain simply:**
- **Sampling error:** random, measurable (that is what the margin of error covers), averages out.
- **Non-sampling error:** coverage gaps, non-response, wrong wording, measurement and typing errors; systematic and not covered by a margin of error.
- Both can exist together; non-sampling error is usually the bigger worry.
**Worked example:** A company of 10,000 people has an average salary near 41,000. Random samples of 100 land close to it (small random scatter). A sample taken only from the top half of earners (a frame problem) is off by about 15,000, however often you repeat it.
**Excel / Python:**
```python
import numpy as np

# Build a pretend company of 10,000 salaries
rng = np.random.default_rng(42)
all_salaries = rng.lognormal(mean=10.5, sigma=0.5, size=10000).round(0)
true_average = all_salaries.mean()

# Sampling error: 2,000 fair random samples of 100 people
fair_sample_averages = []
for _ in range(2000):
    fair_sample = rng.choice(all_salaries, 100, replace=False)
    fair_sample_averages.append(fair_sample.mean())

# Non-sampling error: the list only contains the top half of earners
median_salary = np.percentile(all_salaries, 50)
reachable_salaries = all_salaries[all_salaries >= median_salary]
biased_sample_averages = []
for _ in range(2000):
    biased_sample = rng.choice(reachable_salaries, 100, replace=False)
    biased_sample_averages.append(biased_sample.mean())

print("True average:", round(true_average))
print("Fair samples, average of averages:", round(np.mean(fair_sample_averages)))
print("Fair samples, scatter:", round(np.std(fair_sample_averages)))
print("Biased samples, average of averages:", round(np.mean(biased_sample_averages)))
```
```text
True average: 41008
Fair samples, average of averages: 40956
Fair samples, scatter: 2185
Biased samples, average of averages: 56740
```
Fair samples centre on the truth with small scatter; the biased frame centres about 15,800 too high no matter how many samples we take.
**Likely follow-ups:** 1) *Does a bigger sample help?* It shrinks sampling error only. 2) *Which is in the margin of error?* Sampling error only.
**Common mistakes:** Believing a "±3%" margin of error covers biased questions or missing groups.

### Q23 ⭐⭐ 🟢 What is the difference between stratified sampling and cluster sampling?
**Asked at:** commonly asked; the sources file lists "cluster vs stratified" comparisons (Statology, Statsig, snippets only).
**What the interviewer is checking:** Can you separate "sample from every group" from "pick whole groups"?
**Say this in the interview:** "In stratified sampling I split the population into groups that differ from each other and sample from every group. In cluster sampling I randomly pick a few whole groups and survey everyone inside them."
**Explain simply:**
- **Stratified:** groups (strata) are internally similar, such as grade levels; every group is represented; aims for **accuracy**.
- **Cluster:** groups (clusters) are mini-versions of the population, such as offices; only some are visited; aims for **lower cost**.
- Stratified usually gives more precise estimates; cluster is cheaper when people are spread out but is less precise.
**Worked example:** 600 employees in 6 offices (100 each), each with 50 junior, 30 mid, 20 senior. Stratified 10%: 30 junior, 18 mid, 12 senior from all 6 offices. Cluster: pick 2 offices at random and survey all 200 people.
**Excel / Python:**
```python
import numpy as np
import pandas as pd

# Build 600 employees: 6 offices, each with 50 junior, 30 mid, 20 senior
offices = ["Office A", "Office B", "Office C", "Office D", "Office E", "Office F"]
grade_pattern = np.repeat(["Junior", "Mid", "Senior"], [50, 30, 20])
employees = pd.DataFrame({
    "office": np.repeat(offices, 100),
    "grade": np.tile(grade_pattern, 6),
})

# Stratified: take 10% from every grade
stratified_sample = employees.groupby("grade").sample(frac=0.10, random_state=1)
print("Stratified counts:", stratified_sample["grade"].value_counts().to_dict())
print("Offices covered:", stratified_sample["office"].nunique())

# Cluster: randomly pick 2 whole offices and keep everyone in them
rng = np.random.default_rng(7)
chosen_offices = list(rng.choice(offices, 2, replace=False))
cluster_sample = employees[employees["office"].isin(chosen_offices)]
print("Cluster size:", len(cluster_sample))
print("Offices covered:", cluster_sample["office"].nunique())
```
```text
Stratified counts: {'Junior': 30, 'Mid': 18, 'Senior': 12}
Offices covered: 6
Cluster size: 200
Offices covered: 2
```
Stratified touches all 6 offices with 60 people; cluster surveys 200 people in only 2 offices.
**Likely follow-ups:** 1) *Which is more accurate?* Usually stratified. 2) *When cluster?* When travel or admin cost dominates.
**Common mistakes:** Mixing up the names; forgetting that cluster sampling surveys everyone inside the chosen clusters.

### Q24 ⭐⭐ 🟢 What is a sampling distribution?
**Asked at:** commonly asked (no company-specific report found); it underpins the CLT items in the sources file.
**What the interviewer is checking:** Do you understand that a statistic (like a sample mean) varies from sample to sample?
**Say this in the interview:** "If I took many samples and calculated the mean of each, those means would form their own distribution. That is the sampling distribution; its spread is the standard error."
**Explain simply:**
- One sample gives one mean; another sample gives a slightly different mean.
- The **sampling distribution** is the pattern of those means (or any other statistic) across all possible samples.
- It is centred on the population mean (for random samples) and its spread is the **standard error** (Q7).
- In real life you take only one sample; theory (CLT) tells you what the pattern would look like.
**Formula in plain words:** spread of the sample means = population standard deviation divided by the square root of the sample size. SE = sigma / sqrt(n).
**Worked example:** For a company's salaries, draw 3,000 random samples of 50 people and record each mean. The means centre on the population mean and their spread matches sigma / sqrt(50).
**Excel / Python:**
```python
import numpy as np

# A pretend company of 20,000 salaries
rng = np.random.default_rng(1)
all_salaries = rng.lognormal(mean=10.5, sigma=0.5, size=20000).round(0)

# Take 3,000 samples of 50 people and record each sample mean
sample_means = []
for _ in range(3000):
    one_sample = rng.choice(all_salaries, 50)
    sample_means.append(one_sample.mean())

# Compare the spread of the means with the SE formula
print("Population mean:", round(all_salaries.mean()))
print("Population SD:", round(all_salaries.std()))
print("Mean of sample means:", round(np.mean(sample_means)))
print("SD of sample means:", round(np.std(sample_means)))
print("Formula SD / sqrt(50):", round(all_salaries.std() / np.sqrt(50)))
```
```text
Population mean: 40875
Population SD: 21784
Mean of sample means: 40866
SD of sample means: 3094
Formula SD / sqrt(50): 3081
```
The means cluster around the true mean, and their scatter (about 3,080) matches the formula even though salaries themselves are skewed.
**Likely follow-ups:** 1) *Is it a real dataset?* No, it is the theoretical pattern across repeated samples. 2) *What shapes it?* The CLT (Q5).
**Common mistakes:** Confusing it with the distribution of the raw data.

### Q25 ⭐⭐ 🟢 How would you explain a confidence interval to a non-technical manager?
**Asked at:** commonly asked (no company-specific report found); the sources file notes this communication question was answered from general knowledge (the search for it failed).
**What the interviewer is checking:** Can you communicate uncertainty in plain language, correctly?
**Say this in the interview:** "Our survey says 62% are satisfied, but that comes from a sample, so I give a range. The range is about 57% to 67%. If we repeated the survey many times, ranges built this way would capture the true figure about 95% of the time."
**Explain simply:**
- Start with the best estimate, then the range, then how sure we are.
- Say "plausible range for the true value", not "the exact answer".
- A narrow range means precise; a wide range means be careful with decisions.
- Avoid the phrase "95% probability the truth is in this range" (see Q30).
**Formula in plain words:** estimate plus or minus about 2 standard errors. For a proportion: p plus or minus 1.96 x sqrt(p x (1 - p) / n).
**Worked example:** 400 employees surveyed, 62% satisfied: standard error 2.4 points, margin 4.8 points, range 57.2% to 66.8%.
**Excel / Python:**
```python
import math

# Survey result: 62% of 400 employees are satisfied
sample_size = 400
satisfied_share = 0.62

# Standard error and margin of error for a proportion
standard_error = math.sqrt(satisfied_share * (1 - satisfied_share) / sample_size)
margin_of_error = 1.96 * standard_error

# Lower and upper ends of the 95% range
lower_end = satisfied_share - margin_of_error
upper_end = satisfied_share + margin_of_error

print("Standard error:", round(standard_error, 4))
print("Margin of error:", round(margin_of_error, 4))
print("Range:", round(lower_end, 3), "to", round(upper_end, 3))
```
```text
Standard error: 0.0243
Margin of error: 0.0476
Range: 0.572 to 0.668
```
So we report "about 62%, likely between 57% and 67%".
**Likely follow-ups:** 1) *What if the manager wants one number?* Give the estimate, with the range beside it. 2) *Why not just 100% sure?* A range that is certain would be so wide it is useless.
**Common mistakes:** Quoting the number without the range; using words like "standard error" with the manager.

### Q26 ⭐⭐ 🟡 Is a sample size of 30 always enough for the Central Limit Theorem to work?
**Asked at:** commonly asked; the sources file notes a skewed-data CLT follow-up on PrachHub (snippet only).
**What the interviewer is checking:** Do you know "n = 30" is a rule of thumb, not a guarantee?
**Say this in the interview:** "No. Thirty is a rough guide that works for fairly symmetric data. With very skewed or heavy-tailed data, like salaries or order values, you may need hundreds or more."
**Explain simply:**
- The CLT says sample means become roughly normal as n grows; how fast depends on how skewed the data is.
- Symmetric data: n of 15 to 30 is often fine. Very skewed data: 30 can leave the confidence interval too narrow in practice.
- Test it by simulation: build intervals many times and count how often they catch the truth (the coverage should be about 95%).
**Worked example:** For skewed data (exponential and a heavy lognormal), the "95%" interval at n = 30 actually catches the truth less often than 95%; it improves with n.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(3)

# Fraction of 95% t-intervals that catch the true mean
def coverage(draw_sample, true_mean, sample_size, repeats=5000):
    hits = 0
    for _ in range(repeats):
        sample = draw_sample(sample_size)
        sample_mean = sample.mean()
        standard_error = sample.std(ddof=1) / np.sqrt(sample_size)
        t_value = stats.t.ppf(0.975, sample_size - 1)
        if sample_mean - t_value * standard_error <= true_mean <= sample_mean + t_value * standard_error:
            hits += 1
    return hits / repeats

# Two skewed data types: exponential (mean 1) and heavy-tailed lognormal
draw_exponential = lambda size: rng.exponential(1.0, size)
draw_heavy = lambda size: rng.lognormal(0, 1.5, size)
heavy_true_mean = np.exp(1.5 ** 2 / 2)

for sample_size in (30, 200, 1000):
    exp_cover = coverage(draw_exponential, 1.0, sample_size)
    heavy_cover = coverage(draw_heavy, heavy_true_mean, sample_size)
    print(sample_size, "exponential:", exp_cover, "heavy-tailed:", heavy_cover)
```
```text
30 exponential: 0.917 heavy-tailed: 0.7976
200 exponential: 0.9416 heavy-tailed: 0.878
1000 exponential: 0.951 heavy-tailed: 0.92
```
At n = 30 the heavy-tailed "95%" interval really works only about 80% of the time; even at n = 1,000 it is a little short.
**Likely follow-ups:** 1) *What do you do for heavy tails?* Bigger n, median or log transform, or bootstrap (Q43, Q48). 2) *Where does 30 come from?* A textbook convention.
**Common mistakes:** Treating 30 as a magic number.

### Q27 ⭐⭐ 🟡 Calculate the standard error of the mean: standard deviation 12, sample size 36.
**Asked at:** commonly asked (gap-fill calculation question; the sources file mentions SE-from-sample-size exercises on techprep.app, snippet only).
**What the interviewer is checking:** Can you apply SE = SD / sqrt(n) quickly?
**Say this in the interview:** "Standard error is the standard deviation divided by the square root of the sample size. The square root of 36 is 6, so 12 divided by 6 is 2."
**Explain simply:**
- **Standard error (SE)** tells you how much a sample mean typically wobbles from sample to sample.
- Bigger samples give smaller SE, but slowly: to halve the SE you need four times the people.
**Formula in plain words:** standard deviation divided by the square root of the sample size. SE = s / sqrt(n).
**Worked example:** s = 12 (for example, monthly overtime hours), n = 36, so SE = 12 / 6 = 2 hours. A sample of 144 would give 12 / 12 = 1.
**Excel / Python:**
```python
import math

# Given values
standard_deviation = 12
sample_size = 36

# Standard error of the mean
standard_error = standard_deviation / math.sqrt(sample_size)
print("Standard error:", standard_error)
```
```text
Standard error: 2.0
```
Excel (not run in Excel here): with the SD in B1 and n in B2, `=B1/SQRT(B2)` returns 2. For raw data in A2:A37, `=STDEV.S(A2:A37)/SQRT(COUNT(A2:A37))` (STDEV.S needs Excel 2010+).
**Likely follow-ups:** 1) *SE vs SD?* Q7. 2) *Use SD or s?* The sample SD if the population SD is unknown.
**Common mistakes:** Forgetting the square root; dividing by n.

### Q28 ⭐⭐ 🟡 Calculate a 95% confidence interval for a proportion: 200 of 500 surveyed employees are satisfied.
**Asked at:** commonly asked (gap-fill calculation question; no company-specific report found).
**What the interviewer is checking:** Do you use the proportion formula (not the mean formula) and interpret the result?
**Say this in the interview:** "The sample proportion is 200 / 500 = 0.40. Its standard error is the square root of 0.4 x 0.6 / 500, about 0.022. Margin of error is 1.96 times that, about 4.3 points, so the interval is roughly 35.7% to 44.3%."
**Explain simply:**
- A **proportion** is a share (40% satisfied). Its uncertainty depends on the share itself and on n.
- 1.96 is the z-value that leaves 2.5% in each tail for 95% confidence.
- This normal approximation works when both successes and failures are at least about 10 (here 200 and 300).
**Formula in plain words:** proportion plus or minus 1.96 x square root of (proportion x (1 - proportion) / n).
**Worked example:** p = 0.40, SE = 0.0219, margin = 0.0429, interval 0.357 to 0.443.
**Excel / Python:**
```python
import math

# Survey results
satisfied_count = 200
sample_size = 500

# Sample proportion
sample_proportion = satisfied_count / sample_size

# Standard error and margin of error
standard_error = math.sqrt(sample_proportion * (1 - sample_proportion) / sample_size)
margin_of_error = 1.96 * standard_error

# Interval ends
lower_end = sample_proportion - margin_of_error
upper_end = sample_proportion + margin_of_error

print("Proportion:", sample_proportion)
print("Standard error:", round(standard_error, 5))
print("Margin of error:", round(margin_of_error, 4))
print("95% CI:", round(lower_end, 4), "to", round(upper_end, 4))
```
```text
Proportion: 0.4
Standard error: 0.02191
Margin of error: 0.0429
95% CI: 0.3571 to 0.4429
```
We are 95% confident the true satisfied share is between about 35.7% and 44.3%.
Excel (not run in Excel here): with proportion in B1 (0.4) and n in B2 (500), margin `=1.96*SQRT(B1*(1-B1)/B2)` returns 0.0429.
**Likely follow-ups:** 1) *Small n or p near 0 or 1?* Use Wilson or exact intervals. 2) *Is it 0.4 plus or minus 4.3 percent or points?* Percentage points.
**Common mistakes:** Using the standard deviation of raw data instead of sqrt(p(1-p)/n); mixing percentages with proportions.

### Q29 ⭐⭐ 🟡 What is the difference between a 90%, 95% and 99% confidence interval for the same data?
**Asked at:** commonly asked (no company-specific report found); a standard CI topic in the sources file.
**What the interviewer is checking:** Do you understand the confidence versus precision trade-off?
**Say this in the interview:** "Higher confidence means a wider interval. For the same data, 99% is wider than 95%, which is wider than 90%, because to be more sure of catching the truth you need a bigger net."
**Explain simply:**
- Same sample, same estimate; only the multiplier (z-value) changes: 1.645, 1.96, 2.576.
- A wider range is safer but less useful for decisions.
- 95% is the common compromise.
**Formula in plain words:** estimate plus or minus (z-value x standard error).
**Worked example:** Sample mean 50, SD 10, n = 100, so SE = 1. Widths: about 3.29, 3.92 and 5.15.
**Excel / Python:**
```python
from scipy import stats

# Same data for all three intervals
sample_mean = 50
standard_error = 10 / 10

for confidence_level in (0.90, 0.95, 0.99):
    # z-value that leaves the right amount in each tail
    z_value = stats.norm.ppf(1 - (1 - confidence_level) / 2)
    margin_of_error = z_value * standard_error
    lower_end = sample_mean - margin_of_error
    upper_end = sample_mean + margin_of_error
    print(confidence_level, "z =", round(z_value, 3), "CI:", round(lower_end, 2), "to", round(upper_end, 2))
```
```text
0.9 z = 1.645 CI: 48.36 to 51.64
0.95 z = 1.96 CI: 48.04 to 51.96
0.99 z = 2.576 CI: 47.42 to 52.58
```
The more confident we want to be, the wider the range.
**Likely follow-ups:** 1) *Why not 100%?* It would be infinitely wide. 2) *How to narrow without losing confidence?* Increase sample size (Q12).
**Common mistakes:** Thinking higher confidence means a more accurate estimate.

### Q30 ⭐⭐ 🟡 Is it correct to say there is a 95% probability that the true mean lies inside a given 95% confidence interval?
**Asked at:** commonly asked (no company-specific report found); the sources file lists CI misinterpretation as a 2-star topic.
**What the interviewer is checking:** Do you know the strict meaning of the "95%"?
**Say this in the interview:** "Strictly, no. The true mean is a fixed number, so once I have calculated one interval it either contains it or it does not. The 95% describes the method: 95% of intervals built this way would catch the truth. In practice, many people say 'I am 95% confident', which is fine."
**Explain simply:**
- Before sampling, the interval is random; after, it is fixed.
- The 95% is the long-run hit rate of the procedure.
- Many interviewers accept "95% confident" as the plain-language version; do not say "95% probability".
**Worked example:** Draw 1,000 samples from a population with true mean 50 (SD 10, n = 100), build a 95% interval from each, and count how many contain 50.
**Excel / Python:**
```python
import numpy as np

# Population with true mean 50 and SD 10
rng = np.random.default_rng(11)
true_mean = 50
population_sd = 10

# Build 1,000 intervals and count how many catch the true mean
intervals_that_hit = 0
for _ in range(1000):
    sample = rng.normal(true_mean, population_sd, 100)
    sample_mean = sample.mean()
    standard_error = sample.std(ddof=1) / 10
    lower_end = sample_mean - 1.96 * standard_error
    upper_end = sample_mean + 1.96 * standard_error
    if lower_end <= true_mean <= upper_end:
        intervals_that_hit += 1

print("Intervals containing the true mean out of 1000:", intervals_that_hit)
```
```text
Intervals containing the true mean out of 1000: 944
```
About 95% of the intervals catch the truth (the exact count varies; 5% miss).
**Likely follow-ups:** 1) *Bayesian alternative?* A credible interval does allow the probability wording. 2) *What if the interviewer says "95% confident"?* Acceptable shorthand.
**Common mistakes:** Saying "95% of employees fall in this range"; that confuses the CI with the spread of individuals.

### Q31 ⭐⭐ 🟡 What is the difference between confidence level and significance level?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know they are two sides of one number?
**Say this in the interview:** "Significance level (alpha) is the chance of a false alarm I am willing to accept, usually 5%. Confidence level is 1 minus alpha, so 95%."
**Explain simply:**
- **Alpha = 0.05** means: if there is truly no effect, I accept a 5% risk of wrongly calling it an effect.
- **Confidence level = 1 - alpha = 95%** describes the interval.
- Link: a 95% interval and a two-sided test at alpha 0.05 agree; if the interval excludes the "no effect" value, the test is significant.
**Formula in plain words:** confidence level = 1 minus significance level.
**Worked example:** alpha 0.05 gives 95% confidence and a z-value of 1.96; alpha 0.01 gives 99%.
**Excel / Python:**
```python
from scipy import stats

# Significance level chosen by the analyst
alpha = 0.05

# The matching confidence level and two-sided critical z-value
confidence_level = 1 - alpha
critical_z = stats.norm.ppf(1 - alpha / 2)

print("Confidence level:", round(confidence_level, 2))
print("Critical z:", round(critical_z, 3))
```
```text
Confidence level: 0.95
Critical z: 1.96
```
Alpha 5% corresponds to a 95% interval and a cut-off of 1.96 standard errors.
**Likely follow-ups:** 1) *Can you pick alpha after seeing data?* No. 2) *Does lower alpha mean wider intervals?* Yes.
**Common mistakes:** Saying alpha is the probability the null hypothesis is true.

### Q32 ⭐⭐ 🟡 Only 300 of 1,000 employees answered your engagement survey. What problems does this create and what would you do?
**Asked at:** commonly asked (HR scenario gap-fill; the sources file marks the 300-of-1,000 scenario as a gap-fill, not seen in a source).
**What the interviewer is checking:** Do you think about who answered, not just how many?
**Say this in the interview:** "A 30% response rate gives a wide margin of error, but the bigger risk is non-response bias: the 700 silent people may feel differently. I would compare respondents with the workforce, weight if needed, follow up with a sample of non-responders, and report results with caveats."
**Explain simply:**
- **Precision:** 300 answers still give a modest margin of error (about 5 points at 70%).
- **Bias:** the real danger; respondents may be the very happy or very unhappy.
- **Steps:** check respondent mix by department, grade and location; send reminders; follow up with a random sample of non-responders; weight to match the workforce (Q46); report the response rate and avoid over-claiming.
- A best-case/worst-case range shows how much non-response could matter.
**Worked example:** 70% of the 300 respondents are favourable (210 people). If non-responders were all unfavourable, true favourability would be 21%; if all favourable, 91%. The honest range without more information is huge, so understanding the non-responders matters.
**Excel / Python:**
```python
import math

# Survey facts
employees = 1000
respondents = 300
favourable_share = 0.70

# Favourable people among those who answered
favourable_count = favourable_share * respondents

# Margin of error from sampling luck alone (assumes respondents are random)
standard_error = math.sqrt(favourable_share * (1 - favourable_share) / respondents)
margin_of_error = 1.96 * standard_error

# Extreme cases for the 700 who stayed silent
non_respondents = employees - respondents
worst_case = favourable_count / employees
best_case = (favourable_count + non_respondents) / employees

print("Favourable respondents:", favourable_count)
print("Margin of error:", round(margin_of_error, 4))
print("Worst case overall:", worst_case)
print("Best case overall:", best_case)
```
```text
Favourable respondents: 210.0
Margin of error: 0.0519
Worst case overall: 0.21
Best case overall: 0.91
```
The sampling margin is only about 5 points, but non-response could swing the true figure anywhere from 21% to 91%.
**Likely follow-ups:** 1) *Is 30% bad?* Not automatically; representativeness matters more than rate. 2) *How to prevent it?* Short, anonymous, protected time to answer.
**Common mistakes:** Quoting a margin of error as if it covers non-response bias.

### Q33 ⭐⭐ 🟡 How many people must you survey for a margin of error of plus or minus 3% at 95% confidence?
**Asked at:** commonly asked (gap-fill calculation question; no company-specific report found).
**What the interviewer is checking:** Can you rearrange the margin-of-error formula and choose a safe assumption?
**Say this in the interview:** "Using the safe assumption of 50% (the most variable case), n = 1.96 squared x 0.5 x 0.5 / 0.03 squared, which is about 1,067, so I round up to 1,068. If the population is small, like 1,000 employees, a finite population correction brings it down to about 517."
**Explain simply:**
- Margin of error E = z x sqrt(p(1-p)/n); solve for n.
- If you do not know p, use 0.5 because it needs the largest sample (conservative).
- Always round **up**.
- For a small population, you need fewer (finite population correction, Q51).
**Formula in plain words:** n = (z squared x p x (1 - p)) divided by (margin of error squared).
**Worked example:** z = 1.96, p = 0.5, E = 0.03 gives 1,067.1, so 1,068. If p is believed to be 0.8, 683 people.
**Excel / Python:**
```python
import math

# Inputs: 95% confidence, margin of error 3 points
z_value = 1.96
margin_of_error = 0.03

# Safe assumption p = 0.5, and an optimistic one p = 0.8
for assumed_share in (0.5, 0.8):
    exact_size = z_value ** 2 * assumed_share * (1 - assumed_share) / margin_of_error ** 2
    required_size = math.ceil(exact_size)
    print("p =", assumed_share, "exact:", round(exact_size, 1), "needed:", required_size)

# Adjust for a small population of 1,000 employees (finite population correction)
population = 1000
adjusted_size = 1068 / (1 + (1068 - 1) / population)
print("For 1,000 employees:", math.ceil(adjusted_size))
```
```text
p = 0.5 exact: 1067.1 needed: 1068
p = 0.8 exact: 683.0 needed: 683
For 1,000 employees: 517
```
About 1,068 people for a large population, but only about 517 if you are surveying a 1,000-person company.
Excel (not run in Excel here): `=ROUNDUP(1.96^2*0.5*0.5/0.03^2,0)` returns 1068.
**Likely follow-ups:** 1) *What if you want 2%?* Roughly 2,401. 2) *Does this include non-response?* No; divide by the expected response rate to know how many to invite.
**Common mistakes:** Rounding down; forgetting that precision costs 4x the people to halve the margin.

### Q34 ⭐⭐ 🟡 When do you use a t-distribution instead of a z-distribution for a confidence interval?
**Asked at:** commonly asked (gap-fill; no company-specific report found).
**What the interviewer is checking:** Do you know to use t when the population standard deviation is unknown?
**Say this in the interview:** "In practice I almost always use t for a mean, because I rarely know the population standard deviation and have to estimate it from the sample. The t-distribution has fatter tails to allow for that extra uncertainty, especially with small samples. With large samples t and z are almost identical."
**Explain simply:**
- **z:** population SD known (rare) or very large samples.
- **t:** population SD unknown, estimated by the sample SD; uses **degrees of freedom** (n - 1), a count tied to sample size.
- Smaller n gives a larger t-value and a wider interval; as n grows, t approaches 1.96.
- For proportions, z is the usual choice.
**Worked example:** 10 time-to-hire values (days): the mean is 4.8 and the sample SD is 0.712. t-multiplier is 2.262 versus 1.96 for z, so the t interval is a bit wider.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# How the t multiplier shrinks toward z as the sample grows
for sample_size in (10, 30, 100, 1000):
    t_value = stats.t.ppf(0.975, sample_size - 1)
    print("n =", sample_size, "t =", round(t_value, 3))
print("z =", round(stats.norm.ppf(0.975), 3))

# Ten time-to-hire values in days
days_to_hire = np.array([4.2, 5.1, 3.8, 6.0, 4.9, 5.5, 4.4, 5.2, 3.9, 5.0])
sample_mean = days_to_hire.mean()
sample_sd = days_to_hire.std(ddof=1)
standard_error = sample_sd / np.sqrt(len(days_to_hire))

# t-based and z-based intervals
t_value = stats.t.ppf(0.975, len(days_to_hire) - 1)
print("Mean:", round(sample_mean, 2), "SD:", round(sample_sd, 3), "SE:", round(standard_error, 3))
print("t interval:", round(sample_mean - t_value * standard_error, 2), "to", round(sample_mean + t_value * standard_error, 2))
print("z interval:", round(sample_mean - 1.96 * standard_error, 2), "to", round(sample_mean + 1.96 * standard_error, 2))
```
```text
n = 10 t = 2.262
n = 30 t = 2.045
n = 100 t = 1.984
n = 1000 t = 1.962
z = 1.96
Mean: 4.8 SD: 0.712 SE: 0.225
t interval: 4.29 to 5.31
z interval: 4.36 to 5.24
```
With only 10 values, z would give an interval that is too narrow (4.36 to 5.24) compared with the honest t interval (4.29 to 5.31).
Excel (not run in Excel here): `=CONFIDENCE.T(0.05, STDEV.S(A2:A11), COUNT(A2:A11))` returns the margin of error (Excel 2010+).
**Likely follow-ups:** 1) *Does t need normal data?* For small n, roughly normal data; for large n the CLT helps. 2) *Rule of n above 30 use z?* Fine as a convention, but t is never wrong.
**Common mistakes:** Using z with small samples; using n instead of n - 1 for degrees of freedom.

### Q35 ⭐⭐ 🟡 Exit interviews show that employees leave mainly for better pay. Why might this conclusion be biased?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured scenario, listed in the sources file as a gap-fill from standard practice (survivorship and exit-interview filtering is discussed in generic guides).
**What the interviewer is checking:** Can you spot who is missing from the data and why the answers may not be honest?
**Say this in the interview:** "Exit interviews only cover leavers who agreed to talk, and people often give a safe reason like pay instead of the real one, such as a bad manager. So I would not treat the result as the true cause of attrition without checking other data."
**Explain simply:**
- **Non-response bias:** only some leavers take part, and they may differ from those who refuse (the angriest often skip it).
- **Social desirability / response bias:** people say what is polite. "Better offer" is easier to say than "my manager was unfair".
- **Survivorship view:** the people who stayed are not asked at all, so we never learn if they are paid the same and stay anyway.
- **Timing:** the interview happens on the way out, when people want a clean exit.
- Fix: compare with stay interviews, engagement surveys, pay data of leavers vs stayers, and anonymous follow-ups after 3 to 6 months.
**Worked example:** 200 employees left; only 80 did an exit interview and 52 of them (65%) named pay. Suppose the 120 who skipped the interview named pay at a lower rate (30 of 120, an assumption for illustration). The true share is lower.
**Excel / Python:**
```python
# Leavers in the year and how many gave an exit interview
leavers_total = 200
interviewed = 80
interviewed_citing_pay = 52

# Assumed (illustrative) number of non-interviewed leavers who would have cited pay
skipped_citing_pay_assumed = 30

# Share citing pay among interviewed only
share_among_interviewed = interviewed_citing_pay / interviewed

# Share citing pay among all leavers
all_citing_pay = interviewed_citing_pay + skipped_citing_pay_assumed
share_among_all = all_citing_pay / leavers_total

print("Pay cited, among interviewed:", round(share_among_interviewed * 100, 1), "%")
print("Pay cited, among all leavers (assumed):", round(share_among_all * 100, 1), "%")
```
```text
Pay cited, among interviewed: 65.0 %
Pay cited, among all leavers (assumed): 41.0 %
```
The exit interviews alone would suggest 65%, but under this assumption the real figure is about 41%. The 30 is made up; the point is that missing people can change the story.
**Likely follow-ups:** 1) *How would you check the pay claim?* Compare salary vs market for leavers and stayers. 2) *Would a bigger sample help?* Not if the same people keep skipping (Q36).
**Common mistakes:** Treating "reasons given" as "reasons real"; forgetting the people who stayed and the people who skipped.

### Q36 ⭐⭐ 🟡 Does a larger sample size remove bias?
**Asked at:** commonly asked (no company-specific report found); a gap-fill misconception question in the sources file.
**What the interviewer is checking:** Do you know that size fixes random noise, not a flawed method?
**Say this in the interview:** "No. A bigger sample reduces random error, so the estimate becomes more precise, but if the way I picked people is biased, I just get a very precise wrong answer."
**Explain simply:**
- **Random error** (luck of the draw) shrinks as the sample grows.
- **Bias** (systematic error, for example only happy people answer) does not shrink; it stays the same size.
- The famous case is a huge but unrepresentative poll that still gets the answer wrong.
- Better fix: better selection (random sampling, follow-up of non-responders, weighting, Q46).
**Worked example:** 100,000 employees with a true average engagement of 5.99. When happier people are more likely to answer, the average stays near 6.3 to 6.4 whether we ask 100 or 10,000 people. Random samples hover around the truth.
**Excel / Python:**
```python
import numpy as np

# Make the random numbers repeatable
rng = np.random.default_rng(42)

# Population: 100,000 employees with engagement scores around 6.0 (scale 1 to 10)
engagement_scores = rng.normal(loc=6.0, scale=1.5, size=100000).clip(1, 10)
true_mean = engagement_scores.mean()
print("True average engagement:", round(true_mean, 2))

# Happier employees are more likely to answer: chance of answering grows with the score
chance_of_answering = engagement_scores / engagement_scores.sum()

for sample_size in [100, 1000, 10000]:
    # Biased sample: who answers depends on how happy they are
    biased_sample = rng.choice(engagement_scores, size=sample_size, replace=False, p=chance_of_answering)
    # Random sample: everyone has the same chance
    random_sample = rng.choice(engagement_scores, size=sample_size, replace=False)
    print("n =", sample_size,
          "| biased mean:", round(biased_sample.mean(), 2),
          "| random mean:", round(random_sample.mean(), 2))
```
```text
True average engagement: 5.99
n = 100 | biased mean: 6.34 | random mean: 6.11
n = 1000 | biased mean: 6.42 | random mean: 5.94
n = 10000 | biased mean: 6.34 | random mean: 6.03
```
The biased column stays about 0.4 points too high no matter how many people answer; the random column wanders near 6 and gets closer on average as n grows.
**Likely follow-ups:** 1) *What does a larger sample fix?* Random error and the width of the confidence interval (Q12). 2) *How do you reduce bias?* Random selection, chasing non-responders, weighting.
**Common mistakes:** Saying "we surveyed 5,000 people so it must be right"; confusing precision with accuracy.

### Q37 ⭐⭐ 🟡 How would you pick a sample of 200 invoices from 10,000 for an audit?
**Asked at:** commonly asked (no company-specific report found); a gap-fill scenario question in the sources file.
**What the interviewer is checking:** Can you choose a sampling method that is fair and fit for the purpose?
**Say this in the interview:** "I would use a random method so every invoice has an equal chance. If big-value invoices matter most, I would split invoices by amount first and sample more from the high-value group (stratified sampling)."
**Explain simply:**
- **Simple random sample:** a computer picks 200 invoice numbers at random. Fair and simple.
- **Systematic sample:** take every 50th invoice (10,000 / 200 = 50) after a random start. Easy to do by hand, but unsafe if the list has a repeating pattern.
- **Stratified sample:** split into groups (large vs small invoices) and sample each group. Good when a small group holds most of the money.
- Do not pick "the first 200" or "the ones that look odd" (convenience or judgement choice, biased).
**Worked example:** 10,000 invoices, the top 10% by amount are "large". Taking 100 from large and 100 from the rest covers about 5% of total value, versus about 2% from a pure random pick, so the audit sees more of the money at risk.
**Excel / Python:**
```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)

# 10,000 invoices numbered 1 to 10,000, each with an amount
invoices = pd.DataFrame({
    "invoice_number": np.arange(1, 10001),
    "amount": rng.lognormal(mean=7, sigma=1, size=10000).round(2),
})

# Method 1: simple random sample of 200 invoices
random_sample = invoices.sample(n=200, random_state=1)

# Method 2: systematic sample: every 50th invoice after a random start between 1 and 50
step = 10000 // 200
start = int(rng.integers(1, step + 1))
systematic_sample = invoices.iloc[start - 1::step]
print("Step:", step, "| start:", start, "| size:", len(systematic_sample))

# Method 3: stratified: top 10% by amount are "large"; pick 100 from each group
cutoff = invoices["amount"].quantile(0.90)
large_invoices = invoices[invoices["amount"] >= cutoff]
small_invoices = invoices[invoices["amount"] < cutoff]
stratified_sample = pd.concat([
    large_invoices.sample(n=100, random_state=2),
    small_invoices.sample(n=100, random_state=3),
])

# Compare how much money each sample covers
total_value = invoices["amount"].sum()
print("Value covered, stratified:", round(stratified_sample["amount"].sum() / total_value * 100, 1), "%")
print("Value covered, random:", round(random_sample["amount"].sum() / total_value * 100, 1), "%")
```
```text
Step: 50 | start: 32 | size: 200
Value covered, stratified: 5.0 %
Value covered, random: 2.1 %
```
Both samples have 200 invoices, but the stratified one examines more of the total value. (In Excel, a quick random pick: add a column =RAND(), sort by it, take the top 200; not run in Excel here.)
**Likely follow-ups:** 1) *Why not every 50th from the start?* A random start is needed so the choice is not predictable. 2) *What if fraud is rare?* Add a targeted check on risky invoices on top of the random sample.
**Common mistakes:** Picking convenient invoices; using a systematic step on a list that has a built-in pattern; forgetting to record the method so the audit can be repeated.

### Q38 ⭐⭐ 🟡 What is the difference between the Law of Large Numbers and the Central Limit Theorem?
**Asked at:** commonly asked (no company-specific report found); "difference" questions are a gap-fill in the sources file.
**What the interviewer is checking:** Do you separate "the average settles down" from "the shape of the average is normal"?
**Say this in the interview:** "The Law of Large Numbers says that as the sample grows, the sample average gets close to the true average. The Central Limit Theorem says that if you repeat sampling, the averages themselves follow a bell curve, with a spread that shrinks as the sample grows."
**Explain simply:**
- **LLN** is about where the average ends up (the true mean).
- **CLT** is about the shape and spread of the sample averages around that mean (normal, with spread = standard deviation / square root of n, Q7).
- LLN tells you that more data is better; CLT lets you build confidence intervals and tests.
**Formula in plain words:** spread of sample averages = population standard deviation divided by the square root of the sample size. SE = s / sqrt(n).
**Worked example:** Time to hire is skewed with a true mean near 30 days. One sample of 5 gave 15.85, of 5,000 gave 30.3 (LLN). Averages of 50 hires, repeated 5,000 times, have spread 4.25, matching 30/sqrt(50) = 4.24, and the skewness falls from 2.0 (raw) to 0.25 (CLT).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Make the random numbers repeatable
rng = np.random.default_rng(3)

# Skewed population: days to fill a vacancy, true mean about 30
time_to_hire_days = rng.exponential(scale=30, size=200000)
print("True population mean:", round(time_to_hire_days.mean(), 2))

# Law of Large Numbers: one sample growing bigger, the average settles near the truth
for sample_size in [5, 50, 500, 5000, 50000]:
    sample = rng.choice(time_to_hire_days, size=sample_size)
    print("n =", sample_size, "-> sample mean:", round(sample.mean(), 2))

# CLT: take 5,000 samples of 50 hires and keep each sample's average
sample_means = []
for _ in range(5000):
    sample = rng.choice(time_to_hire_days, size=50)
    sample_means.append(sample.mean())
sample_means = np.array(sample_means)

print("Skewness of raw data:", round(stats.skew(time_to_hire_days), 2))
print("Skewness of the 5,000 sample means:", round(stats.skew(sample_means), 2))
print("SD of sample means:", round(sample_means.std(), 2), "| theory 30/sqrt(50) =", round(30 / np.sqrt(50), 2))
```
```text
True population mean: 30.08
n = 5 -> sample mean: 15.85
n = 50 -> sample mean: 32.06
n = 500 -> sample mean: 31.28
n = 5000 -> sample mean: 30.3
n = 50000 -> sample mean: 30.16
Skewness of raw data: 2.0
Skewness of the 5,000 sample means: 0.25
SD of sample means: 4.25 | theory 30/sqrt(50) = 4.24
```
The first block shows averages closing in on 30 (LLN). The second shows the averages becoming nearly symmetric with the predicted spread (CLT).
**Likely follow-ups:** 1) *Does LLN fix bias?* No (Q36). 2) *Does CLT make my raw data normal?* No, only the sampling distribution of the mean (Q8).
**Common mistakes:** Saying CLT makes the data normal; treating the two as the same idea.

### Q39 ⭐⭐ 🟡 A survey of 200 employees shows 58 percent satisfaction; what margin of error would you report, and what would you tell HR?
**Asked at:** commonly asked (no company-specific report found); an HR calculation question, a gap-fill in the sources file.
**What the interviewer is checking:** Can you compute a margin of error for a proportion and explain it in HR language?
**Say this in the interview:** "The margin of error is about plus or minus 6.8 points, so the true satisfaction is probably between 51% and 65%. I would tell HR that more than half are satisfied, but we should not claim exactly 58%."
**Explain simply:**
- **Margin of error:** how far the survey result could plausibly be from the true value, due to sampling luck only.
- It assumes the 200 are a fair random sample; bias would add extra error that this does not cover (Q36).
- Report it as "58% (95% CI 51 to 65%)".
**Formula in plain words:** margin of error = 1.96 times the square root of (share x (1 minus share) / sample size). ME = 1.96 x sqrt(p(1-p)/n).
**Worked example:** p = 0.58, n = 200: SE = sqrt(0.58 x 0.42 / 200) = 0.0349, ME = 1.96 x 0.0349 = 0.0684.
**Excel / Python:** Excel (any version): put 0.58 in B1 and 200 in B2, then `=1.96*SQRT(B1*(1-B1)/B2)` returns 0.0684 (checked in Python; not run in Excel here).
```python
import math

# Survey result
satisfied_share = 0.58
survey_size = 200

# Standard error for a proportion
standard_error = math.sqrt(satisfied_share * (1 - satisfied_share) / survey_size)

# 95% margin of error (1.96 is the z value for 95%)
margin_of_error = 1.96 * standard_error

lower_limit = satisfied_share - margin_of_error
upper_limit = satisfied_share + margin_of_error
print("Standard error:", round(standard_error, 4))
print("Margin of error:", round(margin_of_error, 4))
print("Interval:", round(lower_limit * 100, 1), "% to", round(upper_limit * 100, 1), "%")
```
```text
Standard error: 0.0349
Margin of error: 0.0684
Interval: 51.2 % to 64.8 %
```
We are 95% confident the true satisfaction is between about 51% and 65%.
**Likely follow-ups:** 1) *What if the response rate is low?* Check non-response bias (Q32). 2) *How would you tighten it?* Survey more people (Q12); to halve the margin you need about four times as many.
**Common mistakes:** Reporting 58% with no range; treating the margin as covering bias; forgetting it is in percentage points, not percent.

### Q40 ⭐ 🟢 What is snowball sampling, and when is it used?
**Asked at:** commonly asked (no company-specific report found); named in generic sampling taxonomies only.
**What the interviewer is checking:** Do you know when sampling is non-random and why that limits the conclusions?
**Say this in the interview:** "Snowball sampling means asking people who take part to refer others like them. It is used for hard-to-reach groups, but because it is not random, I would not generalise from it."
**Explain simply:**
- Start with a few people, each introduces more; the sample "rolls" bigger like a snowball.
- It is a **non-probability** method (not everyone has a known chance of being picked, Q16).
- Useful when there is no list of the group, for example former employees who left for competitors, or employees with a hidden concern.
- Risk: friends refer friends, so the sample is similar and not representative.
**Worked example:** To understand why night-shift contract workers feel disconnected, there is no HR list of them. You interview 5, each names 2 more, until you reach about 40. Good for ideas and themes; not for a company-wide percentage.
**Likely follow-ups:** 1) *Can you compute a margin of error from it?* Not validly, since it is not random. 2) *Alternative?* Build a list first and sample randomly, if possible.
**Common mistakes:** Treating the results as representative; using it when a proper list exists.

### Q41 ⭐ 🟢 What are recall bias and observer bias?
**Asked at:** commonly asked (no company-specific report found); bias taxonomies are in the sources list (generic prep sites).
**What the interviewer is checking:** Can you name measurement-related biases and give an example of each?
**Say this in the interview:** "Recall bias is when people remember past events wrongly. Observer bias is when the person collecting the data lets their expectations affect what they record."
**Explain simply:**
- **Recall bias:** "How many days were you absent last year?" People forget or round, or remember recent or dramatic events more. Fix: use attendance records, ask about shorter periods.
- **Observer bias:** a manager rating an employee they already like or dislike, or an interviewer who hears answers through their own expectation. Fix: standard rubrics, blind scoring, multiple raters.
- Both are **measurement** (information) bias: the data collection is distorted, not who is picked.
**Worked example:** A survey asks leavers to rate their manager one year later; those who left on bad terms remember it as worse (recall). A hiring manager who thinks "referrals are better" scores referral candidates higher on the same answers (observer).
**Likely follow-ups:** 1) *How is this different from selection bias?* Selection bias is about who is in the data (Q4); these are about how values are recorded. 2) *Can a larger sample fix them?* No (Q36).
**Common mistakes:** Mixing these with selection bias; thinking honesty alone removes them.

### Q42 ⭐ 🟡 What is quota sampling, and how does it differ from stratified sampling?
**Asked at:** commonly asked (no company-specific report found); a gap-fill comparison question in the sources file.
**What the interviewer is checking:** Do you know that both split the population into groups, but only one picks randomly?
**Say this in the interview:** "Both make sure each group is represented. In stratified sampling, people inside each group are picked randomly. In quota sampling, the interviewer just fills a set number from each group however they like, so it is non-random."
**Explain simply:**
- **Stratified (probability):** split into groups (strata), then random selection within each, so each person has a known chance.
- **Quota (non-probability):** set a target (for example 60 women and 40 men), then take whoever is easy to reach until the quota fills.
- Quota is cheaper and faster, but selection bias can hide inside each quota, and margins of error are not strictly valid.
**Worked example:** To survey 100 employees from 300 head office and 700 warehouse staff, you set 30 and 70. Stratified: draw 30 head office and 70 warehouse names randomly from HR lists. Quota: a surveyor approaches the first 30 head office and 70 warehouse staff they meet, probably those at their desks and on easy shifts.
**Likely follow-ups:** 1) *Which is better?* Stratified, if a list exists. 2) *Why use quota?* No list available, tight time.
**Common mistakes:** Saying the two are the same; assuming meeting the quota makes the sample random.

### Q43 ⭐ 🟡 What is bootstrapping, and when would an analyst use it?
**Asked at:** commonly asked (no company-specific report found); the sources file notes a bootstrap follow-up for skewed data in one practice-platform page (snippet only).
**What the interviewer is checking:** Do you understand resampling and know when formulas are hard or unreliable?
**Say this in the interview:** "Bootstrapping means re-drawing many samples from my own data, with replacement, to see how much my result would change. I use it for the median or for skewed data where there is no easy formula for a confidence interval."
**Explain simply:**
- Treat your sample as a mini population; draw a new sample of the same size, **with replacement** (the same person can appear twice).
- Compute your statistic (median, for example) each time, repeat thousands of times.
- The middle 95% of those results is a 95% bootstrap interval.
- It needs a sample that is reasonably representative and not tiny; it does not repair bias.
**Worked example:** 40 salaries (in thousands), sample median 37.65. Resampling 10,000 times gives a median interval of 34.2 to 49.2, wide and uneven because the data is skewed.
**Excel / Python:**
```python
import numpy as np

# Make the random numbers repeatable
rng = np.random.default_rng(11)

# A sample of 40 monthly salaries (in thousands), right-skewed
salaries = np.round(rng.lognormal(mean=3.7, sigma=0.5, size=40), 1)
print("Sample median:", np.median(salaries))

# Bootstrap: resample 40 salaries WITH replacement, 10,000 times, record each median
bootstrap_medians = []
for _ in range(10000):
    resample = rng.choice(salaries, size=len(salaries), replace=True)
    bootstrap_medians.append(np.median(resample))

# The middle 95% of the 10,000 medians is the bootstrap interval
lower_limit = np.percentile(bootstrap_medians, 2.5)
upper_limit = np.percentile(bootstrap_medians, 97.5)
print("95% bootstrap interval for the median:", round(lower_limit, 1), "to", round(upper_limit, 1))
```
```text
Sample median: 37.65
95% bootstrap interval for the median: 34.2 to 49.2
```
The sample median is 37.65, but with only 40 people the true median could plausibly be anywhere from about 34 to 49.
**Likely follow-ups:** 1) *Why with replacement?* Otherwise every resample would be identical to the original. 2) *When does it fail?* Very small samples, or biased data.
**Common mistakes:** Sampling without replacement; thinking it creates new information; using it to fix a biased sample.

### Q44 ⭐ 🟡 A poll of 1,000 people shows Candidate A at 52% with a margin of error of plus or minus 3%. Can you say A is leading?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question in the sources file.
**What the interviewer is checking:** Do you apply the margin of error rather than reading the headline number?
**Say this in the interview:** "Not with confidence. A's true support could be anywhere from 49% to 55%, and the 'other' side could be at 50%, so the poll cannot rule out a tie or a small deficit."
**Explain simply:**
- Interval for A: 52% plus or minus 3 = 49% to 55%. It includes 50%, the tie point in a two-way race.
- Also note the margin for the **lead** (A minus B) is about double the margin for A alone, since both numbers carry error.
- Premise check: the exact margin for n = 1,000 and p = 52% is about 3.1 points, which pollsters round to 3.
- "Leading" in the sample is true; "leading in the population" is not established.
**Worked example:** A = 52%, B = 48%, a lead of 4 points. The 95% margin for that lead is about 6 points, so the true lead could be between roughly minus 2 and plus 10.
**Excel / Python:**
```python
import math

# Poll result
share_for_candidate_a = 0.52
poll_size = 1000

# 95% margin of error for a proportion
margin = 1.96 * math.sqrt(share_for_candidate_a * (1 - share_for_candidate_a) / poll_size)
lower_limit = share_for_candidate_a - margin
upper_limit = share_for_candidate_a + margin

print("Margin of error:", round(margin * 100, 2), "points")
print("Interval for A:", round(lower_limit * 100, 1), "to", round(upper_limit * 100, 1))
```
```text
Margin of error: 3.1 points
Interval for A: 48.9 to 55.1
```
The interval includes 50%, so we cannot say A is ahead.
**Likely follow-ups:** 1) *What would make it conclusive?* A larger sample or a bigger gap. 2) *Is the margin for the lead the same?* No, it is roughly twice as large.
**Common mistakes:** Comparing 52 to 48 and ignoring the margin; saying the margin applies to the gap.

### Q45 ⭐ 🟡 What does it mean if a confidence interval for a difference includes zero?
**Asked at:** commonly asked (no company-specific report found); not tied to a specific company in the sources file.
**What the interviewer is checking:** Can you link confidence intervals to significance in plain terms?
**Say this in the interview:** "It means the data are consistent with no difference, so we cannot claim a real difference at that confidence level. It does not prove the two are equal; it may just mean we do not have enough data."
**Explain simply:**
- Zero in the interval = 'no difference' is a plausible value.
- This matches a test: a 95% interval including 0 means the p-value is above 0.05 (not significant at 5%).
- "Not significant" is not "no effect". It is often "not enough data".
- An interval entirely above (or below) zero means a real difference is likely and shows how big it could be.
**Worked example:** Attrition: Branch A 30 of 200 leave (15%), Branch B 20 of 200 (10%), difference 5 points, 95% interval minus 1.5 to plus 11.5, includes 0. With 2,000 per branch and the same rates, the interval is 3.0 to 7.0, excluding 0.
**Excel / Python:**
```python
import math

# Attrition in two branches
left_branch_a, size_branch_a = 30, 200
left_branch_b, size_branch_b = 20, 200
rate_a = left_branch_a / size_branch_a
rate_b = left_branch_b / size_branch_b
difference = rate_a - rate_b

# Standard error of a difference between two proportions
standard_error = math.sqrt(rate_a * (1 - rate_a) / size_branch_a + rate_b * (1 - rate_b) / size_branch_b)
margin = 1.96 * standard_error
print("Difference:", round(difference, 3))
print("95% interval (200 each):", round(difference - margin, 3), "to", round(difference + margin, 3))

# Same rates, ten times more employees per branch
size_branch_a = size_branch_b = 2000
standard_error = math.sqrt(rate_a * (1 - rate_a) / size_branch_a + rate_b * (1 - rate_b) / size_branch_b)
margin = 1.96 * standard_error
print("95% interval (2000 each):", round(difference - margin, 3), "to", round(difference + margin, 3))
```
```text
Difference: 0.05
95% interval (200 each): -0.015 to 0.115
95% interval (2000 each): 0.03 to 0.07
```
With 200 people each the 5-point gap could be luck; with 2,000 each the same gap is clearly real.
**Likely follow-ups:** 1) *Does it mean the groups are the same?* No. 2) *What would you do?* Collect more data or report the range honestly.
**Common mistakes:** Saying "no difference exists"; ignoring that a wide interval means high uncertainty.

### Q46 ⭐ 🟡 What is post-stratification weighting, and why is it used when survey respondents are unrepresentative?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic for analytics firms per the sources file.
**What the interviewer is checking:** Do you know a practical fix for a survey where some groups answered more than others?
**Say this in the interview:** "After the survey, I give each group a weight so its influence matches its real share of the workforce. Groups that under-responded count more and groups that over-responded count less."
**Explain simply:**
- You need known group sizes from HR records (department, location, grade).
- **Weight** = group's share of the workforce divided by its share of respondents.
- It corrects imbalance in the groups you can measure. It cannot fix differences inside a group (for example, unhappy warehouse staff who did not answer).
- Very large weights make results unstable, so check them.
**Formula in plain words:** weight = share of workforce / share of respondents; weighted result = sum of (group rate x group workforce share).
**Worked example:** Head office 30% of staff but 60% of respondents; warehouse 50% of staff but 20% of respondents; field sales 20% and 20%. Raw satisfaction 66%; weighted 57%.
**Excel / Python:**
```python
import pandas as pd

# Workforce makeup (from HR records) and survey respondents (what we got)
groups = pd.DataFrame({
    "group": ["Head office", "Warehouse", "Field sales"],
    "workforce": [300, 500, 200],
    "respondents": [150, 50, 50],
    "satisfied": [120, 25, 20],
})
total_workforce = groups["workforce"].sum()
total_respondents = groups["respondents"].sum()

# Raw result ignores who is over- or under-represented
raw_share = groups["satisfied"].sum() / total_respondents
print("Raw satisfaction:", round(raw_share * 100, 1), "%")

# Satisfaction inside each group
groups["satisfaction_rate"] = groups["satisfied"] / groups["respondents"]

# Weight = share of workforce divided by share of respondents
groups["workforce_share"] = groups["workforce"] / total_workforce
groups["respondent_share"] = groups["respondents"] / total_respondents
groups["weight"] = groups["workforce_share"] / groups["respondent_share"]

# Weighted result: each group's rate counts according to its workforce share
weighted_share = (groups["satisfaction_rate"] * groups["workforce_share"]).sum()
print(groups[["group", "satisfaction_rate", "workforce_share", "respondent_share", "weight"]].round(3).to_string(index=False))
print("Weighted satisfaction:", round(weighted_share * 100, 1), "%")
```
```text
Raw satisfaction: 66.0 %
      group  satisfaction_rate  workforce_share  respondent_share  weight
Head office                0.8              0.3               0.6     0.5
  Warehouse                0.5              0.5               0.2     2.5
Field sales                0.4              0.2               0.2     1.0
Weighted satisfaction: 57.0 %
```
Head office was over-heard, so the raw figure looked better than reality; weighting brings it to 57%.
**Likely follow-ups:** 1) *Does it remove all non-response bias?* No, only along the groups you weight by. 2) *Why not just resurvey?* Cost and time; weighting is a quick correction.
**Common mistakes:** Weighting by groups with no link to the answer; using huge weights from tiny groups.

### Q47 ⭐ 🟡 What assumptions must hold for the Central Limit Theorem to apply?
**Asked at:** commonly asked (no company-specific report found); a practice-platform page in the sources file lists independence and random sampling as the conditions (snippet only).
**What the interviewer is checking:** Do you know CLT is not magic and when it breaks?
**Say this in the interview:** "The observations should be independent, come from random sampling, and the data should have a finite variance. The sample must also be big enough for the shape; skewed data needs more than 30."
**Explain simply:**
- **Independent and random:** one person's answer should not tell you another's. Teams, families, repeated measures of the same person break this.
- **Finite variance:** no extreme tails that make the spread explode (very heavy-tailed data, Q48).
- **Large enough n:** the more skewed the data, the larger n must be (Q26).
- Sample must be drawn from the population you care about (random sampling), or the centre is biased.
**Worked example:** Mood scores of 20 independent people have averages that vary by about 0.55; if all 20 come from one team (sharing a team mood), averages vary by about 2.0, so a normal-theory interval would be far too narrow.
**Excel / Python:**
```python
import numpy as np

# Make the random numbers repeatable
rng = np.random.default_rng(5)

independent_averages = []
one_team_averages = []

for _ in range(3000):
    # Independent: 20 different people, each with their own variation
    mood_scores_independent = rng.normal(0, 2.5, size=20)
    independent_averages.append(mood_scores_independent.mean())

    # Not independent: 20 people from ONE team who all share the same team mood
    team_mood = rng.normal(0, 2)
    personal_variation = rng.normal(0, 1.5, size=20)
    mood_scores_one_team = team_mood + personal_variation
    one_team_averages.append(mood_scores_one_team.mean())

print("Spread of averages, 20 independent people:", round(np.std(independent_averages), 2))
print("Spread of averages, 20 people from one team:", round(np.std(one_team_averages), 2))
```
```text
Spread of averages, 20 independent people: 0.55
Spread of averages, 20 people from one team: 2.01
```
The same number of people gives much more uncertainty when they are not independent, so the usual formula would give false confidence.
**Likely follow-ups:** 1) *Is n = 30 enough?* Not always (Q26). 2) *What if data is clustered?* Use methods that account for clusters.
**Common mistakes:** Citing only "n above 30"; forgetting independence.

### Q48 ⭐ 🔴 How do you handle the Central Limit Theorem for heavy-tailed data such as salaries or order values?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic per the sources file.
**What the interviewer is checking:** Do you know the CLT can be slow for skewed data and what to do instead?
**Say this in the interview:** "For very skewed data, the average converges slowly, so I would not trust a normal-based interval at n = 30. I would use a larger sample, a bootstrap interval, a log transform, or report the median."
**Explain simply:**
- Salaries have a long right tail; a few huge values pull the mean (here mean 74,505 against a median of 36,295).
- CLT still holds when variance is finite, but may need hundreds or thousands of observations. If variance is infinite (extreme tails), it fails.
- Options: **bigger n**; **bootstrap** (Q43); **log transform** (analyse the log, report the geometric mean); **median** or trimmed mean; check tail outliers.
- Always show the distribution before choosing a method.
**Worked example:** Salaries (skewness 9.6). Skewness of sample means: 1.28 at n = 30, 0.52 at n = 300, 0.13 at n = 3,000. The 95% interval built the usual way at n = 30 captured the true mean only 84.2% of the time (not 95%); the same check on the log scale gave 94.0%.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Make the random numbers repeatable
rng = np.random.default_rng(21)

# Very skewed "salaries" (heavy right tail)
salaries = rng.lognormal(mean=10.5, sigma=1.2, size=500000)
print("Skewness of raw salaries:", round(stats.skew(salaries), 1))
print("Mean:", round(salaries.mean()), "| Median:", round(np.median(salaries)))

# How lopsided are the sample averages for different sample sizes?
for sample_size in [30, 300, 3000]:
    means = [rng.choice(salaries, size=sample_size).mean() for _ in range(2000)]
    print("n =", sample_size, "-> skewness of sample means:", round(stats.skew(means), 2))

# Does the usual 95% interval capture the true mean 95% of the time when n = 30?
true_mean = salaries.mean()
hits = 0
trials = 2000
for _ in range(trials):
    sample = rng.choice(salaries, size=30)
    standard_error = sample.std(ddof=1) / np.sqrt(30)
    if sample.mean() - 1.96 * standard_error <= true_mean <= sample.mean() + 1.96 * standard_error:
        hits += 1
print("Coverage of normal-theory interval at n=30:", round(hits / trials * 100, 1), "%")

# Same check on the log scale
log_salaries = np.log(salaries)
true_log_mean = log_salaries.mean()
hits = 0
for _ in range(trials):
    sample = rng.choice(log_salaries, size=30)
    standard_error = sample.std(ddof=1) / np.sqrt(30)
    if sample.mean() - 1.96 * standard_error <= true_log_mean <= sample.mean() + 1.96 * standard_error:
        hits += 1
print("Coverage on log scale at n=30:", round(hits / trials * 100, 1), "%")
```
```text
Skewness of raw salaries: 9.6
Mean: 74505 | Median: 36295
n = 30 -> skewness of sample means: 1.28
n = 300 -> skewness of sample means: 0.52
n = 3000 -> skewness of sample means: 0.13
Coverage of normal-theory interval at n=30: 84.2 %
Coverage on log scale at n=30: 94.0 %
```
Sample averages of skewed data stay lopsided for small n, so the "95%" interval is really about 84%. The log scale fixes most of it.
**Likely follow-ups:** 1) *Mean or median for salaries?* Usually median for the "typical" person. 2) *What if variance is infinite?* The CLT does not apply; use robust methods.
**Common mistakes:** Blindly using n = 30; reporting the mean of salaries as "typical".

### Q49 ⭐ 🔴 What is the difference between a confidence interval and a prediction interval?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic per the sources file.
**What the interviewer is checking:** Do you know one is about the average and the other about one new value?
**Say this in the interview:** "A confidence interval estimates the average. A prediction interval estimates where one new individual value will fall, so it is much wider because individuals vary more than averages."
**Explain simply:**
- **Confidence interval (CI):** where is the true mean? It narrows as n grows.
- **Prediction interval (PI):** where will the next single observation be? It includes both uncertainty about the mean and the person-to-person spread, so it never shrinks below the natural variation.
- Use CI to report an average ("average salary is about 48.7k, plus or minus 2.5k"); use PI for planning a single case ("a new hire is likely paid between 30k and 67k").
**Formula in plain words:** CI half-width = t x s / sqrt(n); PI half-width = t x s x sqrt(1 + 1/n). The extra "1" is the person-to-person spread.
**Worked example:** 50 salaries: mean 48,663, SD 8,970. CI: 46,114 to 51,212. PI: 30,458 to 66,867.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Make the random numbers repeatable
rng = np.random.default_rng(8)

# A sample of 50 monthly salaries
salaries = rng.normal(50000, 8000, size=50).round(0)
sample_size = len(salaries)
sample_mean = salaries.mean()
sample_sd = salaries.std(ddof=1)

# t value for 95% confidence with 49 degrees of freedom
t_value = stats.t.ppf(0.975, df=sample_size - 1)

# Confidence interval for the average salary
ci_half_width = t_value * sample_sd / np.sqrt(sample_size)

# Prediction interval for one new hire's salary
pi_half_width = t_value * sample_sd * np.sqrt(1 + 1 / sample_size)

print("Mean:", round(sample_mean), "SD:", round(sample_sd), "t:", round(t_value, 3))
print("95% CI for the average:", round(sample_mean - ci_half_width), "to", round(sample_mean + ci_half_width))
print("95% prediction interval for one new hire:", round(sample_mean - pi_half_width), "to", round(sample_mean + pi_half_width))
```
```text
Mean: 48663 SD: 8970 t: 2.01
95% CI for the average: 46114 to 51212
95% prediction interval for one new hire: 30458 to 66867
```
The average is pinned down to about 5,000 wide, but one new person could be anywhere in a range about 36,000 wide. (Here the sample mean is 48,663 although the data was generated around 50,000; that is ordinary sampling variation.)
**Likely follow-ups:** 1) *Does the PI shrink with large n?* Only down to the natural spread. 2) *Where is it used?* Regression forecasts.
**Common mistakes:** Using a CI to say where individual values fall; expecting 95% of people to lie inside a CI.

### Q50 ⭐ 🔴 Do two overlapping 95% confidence intervals mean there is no significant difference?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic per the sources file.
**What the interviewer is checking:** Do you avoid a common shortcut and know the right test?
**Say this in the interview:** "No. Overlapping intervals can still hide a significant difference. The right check is the interval for the difference itself. Non-overlap does imply significance, but overlap does not imply non-significance."
**Explain simply:**
- The standard error of a difference is about 1.41 times one group's standard error (square root of 2), not double; so the overlap rule is too strict.
- Intervals can overlap by a modest amount and still have a difference interval that excludes zero.
- Correct approach: build the CI for the difference, or run the test directly (Q45).
**Worked example:** Average engagement: Team A 70, Team B 76, each with standard error 2. CI A: 66.1 to 73.9; CI B: 72.1 to 79.9, they overlap. Difference 6, SE of difference 2.83, z = 2.12, p = 0.034; CI for the difference 0.46 to 11.54, excludes 0, so it is significant at 5%.
**Excel / Python:**
```python
import math
from scipy import stats

# Two team averages and their standard errors
mean_team_a, mean_team_b = 70.0, 76.0
se_team_a = se_team_b = 2.0

# Individual 95% intervals
print("CI A:", round(mean_team_a - 1.96 * se_team_a, 1), "to", round(mean_team_a + 1.96 * se_team_a, 1))
print("CI B:", round(mean_team_b - 1.96 * se_team_b, 1), "to", round(mean_team_b + 1.96 * se_team_b, 1))

# The right check: standard error of the DIFFERENCE
difference = mean_team_b - mean_team_a
se_difference = math.sqrt(se_team_a ** 2 + se_team_b ** 2)
z_value = difference / se_difference
p_value = 2 * (1 - stats.norm.cdf(z_value))
print("Difference:", difference, "| SE of difference:", round(se_difference, 2),
      "| z:", round(z_value, 2), "| p:", round(p_value, 3))
print("CI for difference:", round(difference - 1.96 * se_difference, 2), "to", round(difference + 1.96 * se_difference, 2))
```
```text
CI A: 66.1 to 73.9
CI B: 72.1 to 79.9
Difference: 6.0 | SE of difference: 2.83 | z: 2.12 | p: 0.034
CI for difference: 0.46 to 11.54
```
The two intervals overlap (72.1 to 73.9), yet the difference is significant at 5%.
**Likely follow-ups:** 1) *If the intervals do not overlap?* Then the difference is significant. 2) *What about paired data?* Use the CI of the paired differences.
**Common mistakes:** Calling overlapping intervals "no difference"; comparing two intervals instead of testing the difference.

### Q51 ⭐ 🔴 What is the finite population correction, and when does it matter?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic per the sources file.
**What the interviewer is checking:** Do you know sampling a large share of a small population reduces uncertainty?
**Say this in the interview:** "When I sample a big fraction of a small population without replacement, say more than about 5 to 10%, I multiply the standard error by a correction factor below 1. For a small fraction of a large population, it does not matter."
**Explain simply:**
- Normal formulas assume the population is huge compared to the sample. If you survey almost everyone, little uncertainty is left. At 100% there is none.
- **Correction factor:** square root of (N minus n) / (N minus 1), where N is the population size and n is the sample size.
- Rule of thumb: ignore it if the sample is under about 5% of the population.
- HR example: surveying 200 of 500 employees is a lot; 200 of 1,000,000 customers is not.
**Formula in plain words:** corrected SE = usual SE x sqrt((N - n) / (N - 1)).
**Worked example:** Survey scores with SD 12, n = 200. Usual SE = 12 / sqrt(200) = 0.849. If N = 500: FPC = 0.775, corrected SE = 0.658. If N = 10,000: FPC 0.990, SE 0.840.
**Excel / Python:** Excel: put N in B1 and n in B2, then `=SQRT((B1-B2)/(B1-1))`. For B1 = 500 and B2 = 200 it returns 0.775 (checked in Python; not run in Excel here).
```python
import math

# Sample size and spread of survey scores
sample_size = 200
standard_deviation = 12.0

# Usual standard error (ignores population size)
usual_standard_error = standard_deviation / math.sqrt(sample_size)

for population_size in [500, 1000, 10000, 1000000]:
    # Finite population correction factor
    correction_factor = math.sqrt((population_size - sample_size) / (population_size - 1))
    corrected_standard_error = usual_standard_error * correction_factor
    print("N =", population_size,
          "| FPC:", round(correction_factor, 3),
          "| SE plain:", round(usual_standard_error, 3),
          "| SE corrected:", round(corrected_standard_error, 3))
```
```text
N = 500 | FPC: 0.775 | SE plain: 0.849 | SE corrected: 0.658
N = 1000 | FPC: 0.895 | SE plain: 0.849 | SE corrected: 0.759
N = 10000 | FPC: 0.99 | SE plain: 0.849 | SE corrected: 0.84
N = 1000000 | FPC: 1.0 | SE plain: 0.849 | SE corrected: 0.848
```
In a company of 500, surveying 200 people cuts the standard error by about 22%; in a population of a million it changes nothing.
**Likely follow-ups:** 1) *Does it apply with replacement?* No. 2) *What if you survey everyone?* The correction goes to zero (a census has no sampling error).
**Common mistakes:** Applying it to huge populations; forgetting it only applies when sampling without replacement.

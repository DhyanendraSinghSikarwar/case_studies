# Book 5 — Statistics & Maths for Data Analysts | Part 3: Distributions 🟡

**Target:** 50 questions | **Actual:** 50 questions
**Scope:** normal, binomial and Poisson distributions, z-scores, the empirical rule, skewness and kurtosis, with worked-number and HR-flavoured scenarios.

### Q1 ⭐⭐⭐ 🟢 What is a normal distribution, and what are its key properties?
**Asked at:** commonly asked (no company-specific report found); a search snippet of an Interview Query Tiger Analytics guide mentions basic probability and distributions (page not read in full).
**What the interviewer is checking:** Can you describe the bell curve in plain words and name its properties, not just say "bell shape"?
**Say this in the interview:** "A normal distribution is the symmetric bell-shaped pattern where most values sit near the average and fewer and fewer sit far away on either side. It is fully described by two numbers: the mean, which sets the centre, and the standard deviation, which sets the spread."
**Explain simply:**
- A **distribution** is just a description of how often each value occurs.
- Symmetric: the left half is a mirror image of the right half.
- Mean, median and mode are all the same value, at the peak.
- The **standard deviation** (SD, the typical distance of a value from the mean) controls width: bigger SD, flatter and wider curve.
- The tails never quite touch zero, and about 68%, 95% and 99.7% of values lie within 1, 2 and 3 SDs of the mean (the empirical rule, see Q2).
**Formula in plain words:** The curve height at a value depends only on how many SDs it is from the mean: height is largest at the mean and falls smoothly on both sides. Symbols: X ~ N(μ, σ), where μ is the mean and σ the SD.
**Worked example:** Salaries (monthly, in rupees) with mean 50,000 and SD 10,000. I simulated 100,000 salaries to check the properties.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Make a repeatable random generator
random_generator = np.random.default_rng(42)

# Simulate 100,000 salaries from a normal curve: mean 50,000, SD 10,000
simulated_salaries = random_generator.normal(50000, 10000, 100000)

# Mean and median should be almost identical for a symmetric curve
print("mean", round(simulated_salaries.mean()), "median", round(np.median(simulated_salaries)))

# Share of salaries within 1 SD of the mean (40,000 to 60,000)
distance_from_mean = abs(simulated_salaries - 50000)
share_within_one_sd = np.mean(distance_from_mean <= 10000) * 100
print("share within 1 sd", round(share_within_one_sd, 1))

# Skewness (lopsidedness) should be close to 0
print("skew", round(stats.skew(simulated_salaries), 3))
```
Output: `mean 49958 median 49910`, `share within 1 sd 68.2`, `skew 0.007`. Mean and median match, about 68% sit within one SD, and skew is near zero: symmetric.
**Likely follow-ups:** 1) *Is real data ever perfectly normal?* No, it is a useful approximation. 2) *What two numbers define it?* Mean and SD.
**Common mistakes:** Calling any bell-looking histogram normal without checking symmetry and tails; thinking the mean and SD of a dataset are the same as its shape.

### Q2 ⭐⭐⭐ 🟢 What is the 68-95-99.7 (empirical) rule?
**Asked at:** commonly asked (no company-specific report found); the rule appears in standard statistics question lists (DataCamp snippet, Penn State STAT 500 course page, neither read in full).
**What the interviewer is checking:** Do you know the three percentages, and that they apply to roughly normal data?
**Say this in the interview:** "For roughly bell-shaped data, about 68% of values fall within 1 standard deviation of the mean, about 95% within 2, and about 99.7% within 3. It gives a quick sense of what is typical and what is unusual."
**Explain simply:**
- The **standard deviation (SD)** is the typical distance of a value from the average.
- 1 SD either side of the mean: about 68%. 2 SDs: about 95%. 3 SDs: about 99.7%.
- So only about 5% of values are beyond 2 SDs and about 0.3% beyond 3 SDs.
- It only works for roughly normal data (see Q41 for skewed data).
**Formula in plain words:** Range = mean minus k SDs, to mean plus k SDs, for k = 1, 2, 3. Symbols: μ ± kσ.
**Worked example:** Salaries with mean 50,000 and SD 10,000: about 68% earn 40,000 to 60,000; about 95% earn 30,000 to 70,000; about 99.7% earn 20,000 to 80,000. Someone on 95,000 is 4.5 SDs away, extremely unusual.
**Excel / Python:**
```python
from scipy import stats

# For each number of SDs, find the share of a normal curve inside +/- that many SDs
for number_of_sds in (1, 2, 3):
    share_below_upper = stats.norm.cdf(number_of_sds)
    share_below_lower = stats.norm.cdf(-number_of_sds)
    share_inside = (share_below_upper - share_below_lower) * 100
    print(number_of_sds, round(share_inside, 2))
```
Output: `1 68.27`, `2 95.45`, `3 99.73`. These are the exact values behind the rounded 68, 95, 99.7. Excel: `=NORM.S.DIST(1,TRUE)-NORM.S.DIST(-1,TRUE)` returns 0.6827 (Excel 2010+, not run in Excel here).
**Likely follow-ups:** 1) *Why is 95% sometimes written as 1.96 SDs?* Exactly 95% sits within 1.96 SDs. 2) *Does it hold for skewed data?* No.
**Common mistakes:** Applying it to skewed data such as salaries; reading "68%" as "68% of the range" instead of 68% of the values.

### Q3 ⭐⭐⭐ 🟢 What is skewness, and what is the difference between positive (right) and negative (left) skew?
**Asked at:** commonly asked (no company-specific report found); skewness with mean and median appears in standard prep lists (DataCamp snippet, not read in full).
**What the interviewer is checking:** Do you know skewness measures lopsidedness, and which way the tail points?
**Say this in the interview:** "Skewness measures how lopsided a distribution is. Positive or right skew means a long tail on the right, a few very high values, like salaries. Negative or left skew means a long tail on the left, a few very low values. The tail direction names the skew, not where the bulk of the data sits."
**Explain simply:**
- Skewness near 0: roughly symmetric.
- Positive (right) skew: most values are low, a few are very high, so the tail stretches right (salary, tenure, bonuses).
- Negative (left) skew: most values are high, a few are very low (marks on an easy test, attendance percentage).
- Rough guide: between -0.5 and 0.5 is fairly symmetric; beyond +/-1 is strongly skewed.
**Formula in plain words:** Take each value's distance from the mean, cube it (so direction is kept), average these, and divide by the SD cubed to make it unit-free. Symbols: skew = average of ((x − mean)/SD)³.
**Worked example:** Twelve employees' monthly salaries in thousands: 30, 32, 35, 36, 38, 40, 42, 45, 50, 60, 95, 150. Flip them (100 minus each) and you get a mirror-image, left-skewed set.
**Excel / Python:**
```python
from scipy import stats

# Salaries in thousands: most are modest, two are very high
salaries_in_thousands = [30, 32, 35, 36, 38, 40, 42, 45, 50, 60, 95, 150]

# Mirror the data to create a left-skewed set
mirrored_values = [100 - value for value in salaries_in_thousands]

# bias=False gives the same sample skewness that Excel's SKEW uses
print("right skew", round(stats.skew(salaries_in_thousands, bias=False), 2))
print("left skew", round(stats.skew(mirrored_values, bias=False), 2))
```
Output: `right skew 2.29`, `left skew -2.29`. Positive means a right tail; the mirrored data has the same size but the opposite sign. Excel: `=SKEW(A2:A13)` (sample version, all versions, not run in Excel here).
**Likely follow-ups:** 1) *Which is more common in HR data?* Right skew (salary, tenure). 2) *Does skew 0 prove normal?* No (Q28).
**Common mistakes:** Naming the skew by where the bulk of the data is; it is named by the tail.

### Q4 ⭐⭐⭐ 🟢 In a right-skewed distribution, what is the order of mean, median and mode, and which would you report for employee salaries?
**Asked at:** commonly asked (no company-specific report found); "skewness vs mean/median" appears in DataCamp's list (snippet only).
**What the interviewer is checking:** Do you know the ordering and can you choose a sensible average for money data?
**Say this in the interview:** "In a right-skewed distribution the mean is pulled up by the few very high values, so the order is mode, then median, then mean, smallest to largest. For salaries I would report the median because it is not dragged up by a few very high earners, and I would mention the mean alongside."
**Explain simply:**
- Mean = sum divided by count; every value counts, so extreme values pull it.
- Median = the middle value; extremes barely move it.
- Mode = the most frequent value, at the peak.
- Right skew: mode < median < mean. Left skew is the reverse: mean < median < mode.
**Worked example:** Twelve salaries in thousands: 25, 28, 30, 30, 30, 32, 35, 38, 45, 60, 120, 250. The two high earners lift the mean to 60.25, but the middle employee earns about 33.5.
**Excel / Python:**
```python
import numpy as np
from collections import Counter

# Monthly salaries in thousands
salaries_in_thousands = [25, 28, 30, 30, 30, 32, 35, 38, 45, 60, 120, 250]

# Average of all values
mean_salary = np.mean(salaries_in_thousands)

# Middle value
median_salary = np.median(salaries_in_thousands)

# Most frequent value
mode_salary = Counter(salaries_in_thousands).most_common(1)[0][0]

print("mean", mean_salary, "median", median_salary, "mode", mode_salary)
```
Output: `mean 60.25 median 33.5 mode 30`. Mode < median < mean, so the data is right-skewed and the median (33.5k) describes a typical employee better than the mean. Excel: `=AVERAGE(A2:A13)`, `=MEDIAN(A2:A13)`, `=MODE.SNGL(A2:A13)` (2010+, not run in Excel here).
**Likely follow-ups:** 1) *When would you report the mean?* For totals, such as payroll budgeting. 2) *What else could you report?* Percentiles.
**Common mistakes:** Reversing the order; reporting only the mean for salary.

### Q5 ⭐⭐⭐ 🟢 What is a z-score, and how do you calculate it?
**Asked at:** commonly asked (no company-specific report found); z-scores are a standard item in stats question lists.
**What the interviewer is checking:** Can you compute and interpret a z-score as "how many SDs from the mean"?
**Say this in the interview:** "A z-score says how many standard deviations a value is above or below the mean. You subtract the mean from the value and divide by the SD. It puts different measures on one common scale, so I can compare them or flag outliers."
**Explain simply:**
- Positive z: above average. Negative z: below. Zero: exactly average.
- Because it is in SD units, z = 2 means the same "unusualness" whether it came from salary or test marks.
- On a normal curve, z maps to a percentile (z = 1.5 is about the 93rd percentile).
**Formula in plain words:** (value minus mean) divided by standard deviation. Symbols: z = (x − μ) / σ.
**Worked example:** Salary 65,000, mean 50,000, SD 10,000: z = (65,000 − 50,000) / 10,000 = 1.5, so this employee is 1.5 SDs above average, higher paid than about 93% of employees (if roughly normal).
**Excel / Python:**
```python
from scipy import stats

employee_salary = 65000
mean_salary = 50000
salary_sd = 10000

# Distance from the mean, measured in SDs
z_score = (employee_salary - mean_salary) / salary_sd

# Share of a normal curve below this z-score
percentile_share = stats.norm.cdf(z_score)

print(z_score, round(percentile_share, 4))
```
Output: `1.5 0.9332`. About 93.3% of employees earn less. Excel: `=STANDARDIZE(65000,50000,10000)` returns 1.5, and `=NORM.S.DIST(1.5,TRUE)` returns 0.9332 (not run in Excel here; NORM.S.DIST needs 2010+).
**Likely follow-ups:** 1) *What z is "unusual"?* Beyond +/-2 or +/-3 is common. 2) *Is z-score the same as standardisation?* Yes.
**Common mistakes:** Dividing by the variance instead of the SD; reading the percentile from z when the data is not roughly normal.

### Q6 ⭐⭐⭐ 🟡 What is the difference between the binomial and Poisson distributions?
**Asked at:** commonly asked (no company-specific report found); binomial vs Poisson is a standard comparison (GeeksforGeeks page, snippet only).
**What the interviewer is checking:** Do you know when you count successes out of a fixed number of tries versus events in a time window?
**Say this in the interview:** "Binomial counts successes out of a fixed number of tries, each with the same success probability, like how many of 20 employees leave. Poisson counts how many times an event happens in a fixed time or space with no fixed upper limit, like resignations per month. Poisson has mean equal to variance."
**Explain simply:**
- Binomial: fixed number of trials (n), two outcomes each, same probability (p), independent. Counts run from 0 to n.
- Poisson: events scattered over time at an average rate (λ, "lambda"), count has no fixed maximum.
- Binomial mean = n·p, variance = n·p·(1 − p). Poisson mean = variance = λ.
- If n is large and p is small, Poisson approximates binomial (Q49).
**Worked example:** 20 employees, each with a 5% chance of leaving: P(exactly 2 leave) binomial = 0.1887. Poisson with the same mean (λ = 1) gives 0.1839, close but not equal.
**Excel / Python:**
```python
from scipy import stats

# Binomial: exactly 2 of 20 employees leave, each with a 5% chance
binomial_probability = stats.binom.pmf(2, 20, 0.05)

# Poisson with the same average of 1 leaver
poisson_probability = stats.poisson.pmf(2, 1)

print(round(binomial_probability, 4), round(poisson_probability, 4))
```
Output: `0.1887 0.1839`. Excel: `=BINOM.DIST(2,20,0.05,FALSE)` and `=POISSON.DIST(2,1,FALSE)` (2010+, not run in Excel here).
**Likely follow-ups:** 1) *Which has an upper limit?* Binomial (n). 2) *Which would you use for calls per hour?* Poisson.
**Common mistakes:** Using Poisson when there is a clear maximum such as headcount; forgetting both need independence.

### Q7 ⭐⭐⭐ 🟡 Salaries have a mean of 50,000 and a standard deviation of 10,000 and are roughly normal. What percentage of employees earn between 40,000 and 60,000?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you spot that 40,000 and 60,000 are exactly 1 SD each side of the mean?
**Say this in the interview:** "40,000 and 60,000 are one standard deviation below and above the mean, so by the empirical rule about 68% of employees earn in that band."
**Explain simply:**
- z for 40,000 = (40,000 − 50,000) / 10,000 = −1. z for 60,000 = +1.
- The area under a normal curve between z = −1 and z = +1 is about 68.3%.
- Premise note: real salaries are usually right-skewed, so this is only valid because the question says "roughly normal".
**Formula in plain words:** Share between = share below 60,000 minus share below 40,000 (both read off the normal curve).
**Worked example:** 68.27%. In a team of 200, about 137 people earn between 40,000 and 60,000.
**Excel / Python:**
```python
from scipy import stats

# Share of employees earning less than 60,000 and less than 40,000
share_below_60000 = stats.norm.cdf(60000, 50000, 10000)
share_below_40000 = stats.norm.cdf(40000, 50000, 10000)

# Share in between
share_between = share_below_60000 - share_below_40000

print(round(share_between, 4))
```
Output: `0.6827`. Excel: `=NORM.DIST(60000,50000,10000,TRUE)-NORM.DIST(40000,50000,10000,TRUE)` (2010+, not run in Excel here).
**Likely follow-ups:** 1) *And between 30,000 and 70,000?* About 95.4%. 2) *Is it exactly 68%?* 68.27%.
**Common mistakes:** Saying 95% (that is 2 SDs); applying this to skewed pay data.

### Q8 ⭐⭐⭐ 🟡 Give examples of business data that is roughly normal and data that is not. How would you tell?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you recognise normal-like versus skewed data and check it, not assume?
**Say this in the interview:** "Roughly normal: employee performance ratings in a large team, test scores, measurement errors, the average of many things. Not normal: salaries, sales per customer, time to resolve tickets, tenure, because they have a floor at zero and a long right tail. I check with a histogram, comparing mean and median, the skewness number, and a Q-Q plot."
**Explain simply:**
- Normal-ish data usually comes from many small independent influences added together.
- Money, waiting time and counts with a floor are typically right-skewed.
- Tells: symmetric histogram, mean close to median, skewness near 0, points on a straight line in a Q-Q plot (Q25).
**Worked example:** Simulated engagement scores (mean 3.2, SD 0.6) versus salaries: the salaries show mean well above median and skew above 2.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

random_generator = np.random.default_rng(1)

# Symmetric-looking data: engagement scores
engagement_scores = random_generator.normal(3.2, 0.6, 5000)

# Right-skewed data: salaries (lognormal)
salaries = random_generator.lognormal(10.6, 0.6, 5000)

for name, values in (("scores", engagement_scores), ("salaries", salaries)):
    print(name, "mean", round(values.mean(), 2), "median", round(np.median(values), 2), "skew", round(stats.skew(values), 2))
```
Output: `scores mean 3.19 median 3.18 skew 0.06` and `salaries mean 47669.14 median 40233.52 skew 2.15`. Scores: mean is about median and skew near 0. Salaries: mean far above median and large skew, so not normal.
**Likely follow-ups:** 1) *What would you do with skewed data?* Report median, or take logs (Q26). 2) *Do small samples show normality well?* No, plots are noisy.
**Common mistakes:** Assuming normal because the textbook says so; relying on one test or one chart.

### Q9 ⭐⭐ 🟢 What is a standard normal distribution?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it is the normal curve with mean 0 and SD 1, and why that helps?
**Say this in the interview:** "The standard normal is the normal distribution with mean 0 and standard deviation 1. Any normal variable can be converted to it by calculating z-scores, which lets us use one table or function for every normal problem."
**Explain simply:**
- Subtract the mean and divide by the SD: any normal data becomes standard normal.
- The x-axis is then in SD units; 0 is the average.
- Key values: P(Z < 0) = 0.5, and 1.96 cuts off the top 2.5%.
**Formula in plain words:** z = (value − mean) / SD; then look up the area under the standard curve.
**Worked example:** Salary 65,000 (mean 50,000, SD 10,000) becomes z = 1.5 on the standard curve (Q5).
**Excel / Python:**
```python
from scipy import stats

# Half of the curve lies below the mean (z = 0)
print(round(stats.norm.cdf(0), 2))

# z-value that leaves 2.5% in the upper tail (used for 95% intervals)
print(round(stats.norm.ppf(0.975), 2))
```
Output: `0.5` and `1.96`. Excel: `=NORM.S.INV(0.975)` returns 1.96 (2010+, not run in Excel here).
**Likely follow-ups:** 1) *Why standardise?* To compare different scales. 2) *Variance of the standard normal?* 1.
**Common mistakes:** Thinking standardising makes data normal; it only rescales the shape that is already there.

### Q10 ⭐⭐ 🟢 What is a probability distribution, and what is the difference between discrete and continuous distributions?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand a distribution as "all possible values with their chances", and the counting vs measuring distinction?
**Say this in the interview:** "A probability distribution lists every possible outcome with how likely it is. Discrete means countable outcomes, like the number of resignations, and each value has its own probability. Continuous means measured values on a scale, like salary or tenure in years, where probability is the area under a curve over a range."
**Explain simply:**
- Discrete: 0, 1, 2, 3 resignations; binomial and Poisson are examples.
- Continuous: any value in a range; normal and exponential are examples.
- Probabilities always add up (or integrate) to 1.
- For continuous data, a single exact value has probability 0 (Q45); ask about ranges instead.
**Worked example:** 3 offers, each 80% likely to be accepted: P(0, 1, 2, 3 acceptances) = 0.008, 0.096, 0.384, 0.512, which sum to 1. For salary, P(45,000 to 55,000) = 0.3829.
**Excel / Python:**
```python
from scipy import stats

# Discrete: probability of 0, 1, 2 or 3 acceptances out of 3 offers
for acceptances in range(4):
    print(acceptances, round(stats.binom.pmf(acceptances, 3, 0.8), 3))

# Continuous: probability a salary lies between 45,000 and 55,000
probability_in_range = stats.norm.cdf(55000, 50000, 10000) - stats.norm.cdf(45000, 50000, 10000)
print(round(probability_in_range, 4))
```
Output: `0 0.008`, `1 0.096`, `2 0.384`, `3 0.512`, then `0.3829`. The four discrete probabilities add to 1.
**Likely follow-ups:** 1) *Is age discrete or continuous?* Measured exactly it is continuous; recorded in whole years it is treated as discrete. 2) *Which function gives the discrete probabilities?* The PMF (Q33).
**Common mistakes:** Asking for the probability of an exact continuous value; forgetting probabilities sum to 1.

### Q11 ⭐⭐ 🟢 What is kurtosis, and what does excess kurtosis tell you?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it describes tail weight (outlier-proneness) and that normal is the baseline?
**Say this in the interview:** "Kurtosis describes how heavy the tails of a distribution are, meaning how prone it is to extreme values. Excess kurtosis is kurtosis minus 3, so the normal distribution has 0. Positive excess means heavier tails and more outliers than a normal; negative means lighter tails."
**Explain simply:**
- Kurtosis of a normal = 3, so most software reports **excess kurtosis** = kurtosis − 3, with normal = 0.
- Positive excess ("leptokurtic"): more extreme values than normal.
- Negative excess ("platykurtic"): fewer extremes, such as a flat uniform distribution (−1.2).
- Many analysts say "peakedness", but tail weight is the correct reading (Q48).
**Formula in plain words:** Average of ((x − mean)/SD) raised to the fourth power, minus 3. Raising to the 4th makes extreme values dominate.
**Worked example:** Theoretical excess kurtosis: normal 0, uniform −1.2, t-distribution with 5 degrees of freedom 6, Laplace 3. A simulated t(5) sample gave 5.19 (samples are noisy for heavy tails).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Exact excess kurtosis for four distributions
print("normal", stats.norm.stats(moments='k'))
print("uniform", stats.uniform.stats(moments='k'))
print("t with 5 df", stats.t(5).stats(moments='k'))

# Sample check: 100,000 normal values and 100,000 heavy-tailed values
random_generator = np.random.default_rng(3)
normal_values = random_generator.normal(0, 1, 100000)
heavy_tailed_values = random_generator.standard_t(5, 100000)
print(round(stats.kurtosis(normal_values), 2), round(stats.kurtosis(heavy_tailed_values), 2))
```
Output: `normal 0.0`, `uniform -1.2`, `t with 5 df 6.0`, then `-0.01 5.19`. Excel: `=KURT(A2:A101)` returns the sample excess kurtosis (not run in Excel here).
**Likely follow-ups:** 1) *Why does it matter?* Heavy tails mean outliers are more common than normal-based rules predict. 2) *Does Excel's KURT give excess?* Yes.
**Common mistakes:** Forgetting the "minus 3"; calling kurtosis "peakedness".

### Q12 ⭐⭐ 🟢 What is a Bernoulli trial, and how does it relate to the binomial distribution?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know binomial is a count of successes across repeated Bernoulli trials?
**Say this in the interview:** "A Bernoulli trial is a single experiment with two outcomes, success or failure, with a fixed success probability p, like one candidate accepting or declining an offer. A binomial variable is the number of successes in n independent Bernoulli trials."
**Explain simply:**
- One offer: accept (1) with probability 0.8, decline (0) with probability 0.2. That is a Bernoulli trial.
- Make 5 independent offers and count acceptances: that count is binomial(n = 5, p = 0.8).
- Bernoulli is just binomial with n = 1.
**Formula in plain words:** Chance of exactly k successes = (number of ways to choose which k succeed) × p to the k × (1−p) to the (n−k). Symbols: C(n,k)·pᵏ·(1−p)ⁿ⁻ᵏ.
**Worked example:** P(exactly 4 of 5 accept) = 5 × 0.8⁴ × 0.2 = 0.4096. A simulation of 100,000 batches gave 0.4099.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Exact chance that exactly 4 of 5 offers are accepted
exact_probability = stats.binom.pmf(4, 5, 0.8)
print(round(exact_probability, 4))

# Check by simulation: 100,000 batches of 5 Bernoulli trials
random_generator = np.random.default_rng(7)
accepts_per_batch = random_generator.binomial(1, 0.8, (100000, 5)).sum(axis=1)
print("sim P(4 of 5)", round(np.mean(accepts_per_batch == 4), 4))
```
Output: `0.4096` and `sim P(4 of 5) 0.4099`. Theory and simulation agree.
**Likely follow-ups:** 1) *Mean of a Bernoulli?* p. 2) *Variance?* p(1−p).
**Common mistakes:** Forgetting the "number of ways" factor and just multiplying probabilities.

### Q13 ⭐⭐ 🟢 What conditions must hold for a binomial distribution to apply?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you list the conditions and spot when they fail in real HR data?
**Say this in the interview:** "Four conditions: a fixed number of trials, each trial has only two outcomes, the success probability is the same every time, and the trials are independent. If those fail, binomial is only a rough model."
**Explain simply:**
- Fixed n (for example 10 candidates).
- Two outcomes (join or not).
- Constant p (every candidate has the same 70% chance).
- Independent trials (one candidate's decision does not affect another's).
- Where it breaks: candidates from one referral batch who talk to each other, or offers with different salaries, so p differs.
**Worked example:** Ten candidates each 70% likely to join: P(exactly 7) = 0.2668 (Q18). If p really varied by candidate, this number would not be reliable.
**Excel / Python:**
```python
from scipy import stats

# Valid binomial: 10 independent candidates, same 70% chance each
print(round(stats.binom.pmf(7, 10, 0.7), 4))
```
Output: `0.2668`. About a 27% chance that exactly 7 of the 10 join, under the four conditions above.
**Likely follow-ups:** 1) *What if p differs per person?* Model p separately per group (a "Poisson-binomial" model handles unequal chances, but that is rarely needed in an interview). 2) *What if trials are linked?* Counts vary more than binomial predicts.
**Common mistakes:** Assuming independence without thinking; ignoring that p differs between groups.

### Q14 ⭐⭐ 🟢 Which distribution would you use to model the number of employee resignations in a month, and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you pick Poisson for event counts over time and justify it?
**Say this in the interview:** "Poisson, because resignations are counts of events in a fixed time window, they occur roughly independently, and there is no firm upper limit. I would estimate the average monthly rate from history and check that the variance is close to the mean."
**Explain simply:**
- Counts of events per month, per hour, per page: Poisson territory.
- Needs a roughly constant average rate λ and independent events.
- Caveat: resignations cluster (a bad appraisal cycle, a team leader leaving), which breaks independence. Then variance exceeds mean (Q22). A binomial (n = headcount, p = monthly attrition) is a fair alternative if headcount is small and fixed.
**Worked example:** Average 3 resignations a month: P(0) = 0.0498, P(exactly 3) = 0.2240, P(6 or more) = 0.0839, so a month with 6 or more is a roughly 1-in-12 event.
**Excel / Python:**
```python
from scipy import stats

average_resignations_per_month = 3

# Chance of zero and of exactly three resignations
chance_of_zero = stats.poisson.pmf(0, average_resignations_per_month)
chance_of_three = stats.poisson.pmf(3, average_resignations_per_month)

# Chance of six or more = 1 minus chance of five or fewer
chance_of_six_or_more = 1 - stats.poisson.cdf(5, average_resignations_per_month)

print(round(chance_of_zero, 4), round(chance_of_three, 4), round(chance_of_six_or_more, 4))
```
Output: `0.0498 0.224 0.0839`. Excel: `=POISSON.DIST(0,3,FALSE)` (2010+, not run in Excel here).
**Likely follow-ups:** 1) *How do you check the fit?* Compare variance with mean. 2) *Binomial instead?* If headcount is small and fixed.
**Common mistakes:** Ignoring clustering of resignations; using Poisson for a count with a hard cap.

### Q15 ⭐⭐ 🟢 Which distribution would you use to model whether a candidate accepts a job offer, and the number of acceptances out of 50 offers?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Bernoulli for one yes/no, binomial for the count out of a fixed number.
**Say this in the interview:** "One candidate's accept or decline is a Bernoulli trial. The number of acceptances out of 50 offers is binomial with n = 50 and p equal to the acceptance probability, as long as offers are independent and p is similar for everyone."
**Explain simply:**
- Single yes/no: Bernoulli(p).
- Count out of 50: Binomial(50, p), counts from 0 to 50.
- Expected acceptances = n × p; SD = square root of n·p·(1−p).
**Worked example:** With p = 0.8 and 50 offers: expected 40 acceptances, SD 2.83; P(exactly 40) = 0.1398; P(35 or fewer) = 0.0607; P(45 or more) = 0.0480. So planning for 40 joiners is right, but a shortfall to 35 happens about 6% of the time.
**Excel / Python:**
```python
from scipy import stats

number_of_offers = 50
acceptance_probability = 0.8

# Expected acceptances and spread
expected_acceptances = number_of_offers * acceptance_probability
spread = stats.binom.std(number_of_offers, acceptance_probability)

# Specific chances
chance_exactly_40 = stats.binom.pmf(40, number_of_offers, acceptance_probability)
chance_35_or_fewer = stats.binom.cdf(35, number_of_offers, acceptance_probability)
chance_45_or_more = stats.binom.sf(44, number_of_offers, acceptance_probability)

print(expected_acceptances, round(spread, 2), round(chance_exactly_40, 4), round(chance_35_or_fewer, 4), round(chance_45_or_more, 4))
```
Output: `40.0 2.83 0.1398 0.0607 0.048`. (`sf(44)` means "more than 44", that is 45 or more.) Excel: `=BINOM.DIST(35,50,0.8,TRUE)` (2010+, not run in Excel here).
**Likely follow-ups:** 1) *Where do you get p?* From past acceptance rates. 2) *What if offers go to different seniority levels?* Model groups separately.
**Common mistakes:** Using Poisson for a capped count; ignoring that p varies by role.

### Q16 ⭐⭐ 🟢 Why is the normal distribution so important in statistics?
**Asked at:** commonly asked (no company-specific report found); CLT appears in standard prep lists (DataCamp snippet, not read in full).
**What the interviewer is checking:** Do you know the Central Limit Theorem (CLT) and its practical use?
**Say this in the interview:** "Mainly because of the Central Limit Theorem: averages of many independent observations are approximately normal even when the original data is not. That lets us build confidence intervals and tests for sample means using normal-based rules, whatever the shape of the raw data."
**Explain simply:**
- CLT: the **sample mean** (average of a random sample) tends to a normal shape as the sample grows, and its SD (the standard error) is the data SD divided by the square root of the sample size.
- Many natural measures are sums of small effects, so they look normal.
- Normal maths is tidy: tables, z-scores and closed-form formulas.
- It is a good approximation, not a law of nature for raw data.
**Worked example:** Salaries are strongly right-skewed (skew 2.27). Averages of random samples of 2, 30 and 200 employees have skew 1.50, 0.45 and 0.18, and their SD shrinks as 1/√n, matching theory (22,461, 5,799, 2,246).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

random_generator = np.random.default_rng(5)

# A skewed salary population of 200,000 people
population_salaries = random_generator.lognormal(10.6, 0.6, 200000)
print("pop skew", round(stats.skew(population_salaries), 2))

for sample_size in (2, 30, 200):
    # Draw 5,000 random samples and take each sample's average
    samples = random_generator.choice(population_salaries, (5000, sample_size))
    sample_means = samples.mean(axis=1)
    theory_sd = population_salaries.std() / sample_size ** 0.5
    print(sample_size, "skew of means", round(stats.skew(sample_means), 2), "sd of means", round(sample_means.std()), "theory", round(theory_sd))
```
Output: `pop skew 2.27`, `2 skew of means 1.5 sd of means 22369 theory 22461`, `30 skew of means 0.45 sd of means 5912 theory 5799`, `200 skew of means 0.18 sd of means 2248 theory 2246`. Averages become more symmetric and tighter as samples grow.
**Likely follow-ups:** 1) *How large must n be?* Often 30 is a rule of thumb; more for very skewed data. 2) *Does CLT make raw data normal?* No.
**Common mistakes:** Saying "the data becomes normal"; the sample mean does.

### Q17 ⭐⭐ 🟢 Explain to a non-technical manager what a bell curve means when HR rates employee performance.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you explain a statistical idea simply, and flag its limits?
**Say this in the interview:** "A bell curve means most employees are rated around the middle, and fewer get very high or very low ratings, with the two ends roughly balanced. About two thirds sit within one standard deviation (one typical step) of average. It describes how ratings tend to spread, but it should not force managers to fit people into set percentages."
**Explain simply:**
- Picture a hill: the highest point is the typical rating, the slopes are the less common ratings.
- Example scale 1 to 5 with average 3.0 and SD 0.8: about 16% rate below 2.2, 68% between 2.2 and 3.8, and 16% above 3.8.
- Warning: a bell curve is a pattern in many ratings, not a rule. Forced distribution (making exactly X% "low performers") can be unfair for small teams, because small groups do not follow it.
- If a team has many 4s and 5s because they truly performed, that is fine, and the curve will be skewed.
**Worked example:** Of 200 employees, expect about 32 below 2.2, 137 between 2.2 and 3.8, and 32 above 3.8; only about 4% (8 people) above 4.4.
**Excel / Python:**
```python
from scipy import stats

average_rating = 3.0
rating_sd = 0.8

# Share of employees rated below 2.2
share_low = stats.norm.cdf(2.2, average_rating, rating_sd) * 100

# Share between 2.2 and 3.8
share_middle = (stats.norm.cdf(3.8, average_rating, rating_sd) - stats.norm.cdf(2.2, average_rating, rating_sd)) * 100

# Share above 3.8
share_high = stats.norm.sf(3.8, average_rating, rating_sd) * 100

# Share above 4.4
share_very_high = stats.norm.sf(4.4, average_rating, rating_sd) * 100

print(round(share_low, 1), round(share_middle, 1), round(share_high, 1), round(share_very_high, 1))
```
Output: `15.9 68.3 15.9 4.0`. Roughly 16% / 68% / 16%, with only 4% above 4.4.
**Likely follow-ups:** 1) *Should ratings be forced onto a bell curve?* Not strictly; check the real distribution. 2) *What if ratings pile up at 4?* The data is skewed; report percentages per rating band.
**Common mistakes:** Presenting the bell curve as a quota; forgetting it needs a large group to show up.

### Q18 ⭐⭐ 🟡 Ten candidates each have a 70% chance of joining. What is the probability exactly 7 join?
**Asked at:** commonly asked (no company-specific report found); a standard binomial calculation in generic prep lists.
**What the interviewer is checking:** Can you spot a binomial setting and plug numbers into the formula without freezing?
**Say this in the interview:** "This is binomial: 10 independent candidates, each joins with probability 0.7. P(exactly 7) is the number of ways to pick which 7 join, times 0.7 to the power 7, times 0.3 to the power 3. That comes to about 26.7%."
**Explain simply:**
- **Binomial** means counting successes in a fixed number of independent yes/no tries with the same chance each time.
- "Which 7 of the 10" can happen in many ways; that count is "10 choose 7" = 120.
- Each specific pattern (7 joins, 3 do not) has probability 0.7^7 x 0.3^3.
**Formula in plain words:** probability = (number of ways to choose the joiners) x (chance of joining)^(joiners) x (chance of not joining)^(non-joiners). In symbols: C(n,k) x p^k x (1-p)^(n-k).
**Worked example:** 120 x 0.0823543 x 0.027 = 0.2668, so about a 26.7% chance. The most likely outcome is 7 (the mean is 10 x 0.7 = 7), yet it is still only about one time in four.
**Excel / Python:**
```python
from math import comb
from scipy import stats

number_of_candidates = 10
chance_of_joining = 0.70
joining_count = 7

# Step 1: how many different groups of 7 joiners are possible
ways_to_choose = comb(number_of_candidates, joining_count)

# Step 2: chance that those 7 join, and the other 3 do not
chance_of_7_joining = chance_of_joining ** 7
chance_of_3_not_joining = (1 - chance_of_joining) ** 3

# Step 3: multiply the three pieces
probability = ways_to_choose * chance_of_7_joining * chance_of_3_not_joining
print(ways_to_choose, round(probability, 4))

# Cross-check with the ready-made function
print(round(stats.binom.pmf(7, 10, 0.70), 4))
```
Output:
```
120 0.2668
0.2668
```
The hand calculation and the library agree: about 26.7%.
Excel (2010+; not run in Excel here, matched to Python): `=BINOM.DIST(7,10,0.7,FALSE)` returns 0.2668 (FALSE means "exactly 7", not "7 or fewer").
**Likely follow-ups:** 1) *Probability at least 7 join?* Add P(7)+P(8)+P(9)+P(10), or `=1-BINOM.DIST(6,10,0.7,TRUE)`. 2) *Which assumption could fail?* Independence: friends joining together are not independent.
**Common mistakes:** Forgetting the "10 choose 7" ways term (you would get 0.0022); using TRUE in `BINOM.DIST` and getting "7 or fewer".

### Q19 ⭐⭐ 🟡 You make 100 offers and each has an 80% chance of acceptance. What are the expected number of acceptances and the standard deviation?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the shortcut formulas for a binomial's mean and spread?
**Say this in the interview:** "Expected acceptances are n times p: 100 x 0.8 = 80. The standard deviation is the square root of n x p x (1-p), which is the square root of 16, so 4. So I would plan for about 80, and usually somewhere between 72 and 88."
**Explain simply:**
- **Expected value (mean):** the long-run average number of acceptances if you repeated this hiring round many times.
- **Standard deviation (SD):** the typical distance of a real outcome from that average.
- Assumes each offer is independent with the same 80% chance.
**Formula in plain words:** mean = offers x chance of acceptance; variance = offers x chance of acceptance x chance of refusal; SD = square root of variance. Symbols: np, np(1-p), sqrt(np(1-p)).
**Worked example:** mean 100 x 0.8 = 80; variance 100 x 0.8 x 0.2 = 16; SD = 4. About 95% of the time the count lands within 2 SDs: 72 to 88 (rough rule, see the empirical rule).
**Excel / Python:**
```python
from math import sqrt

offers_made = 100
chance_of_acceptance = 0.80

# Expected number of acceptances
expected_acceptances = offers_made * chance_of_acceptance

# Variance, then standard deviation
variance = offers_made * chance_of_acceptance * (1 - chance_of_acceptance)
standard_deviation = sqrt(variance)
print(expected_acceptances, round(variance, 2), round(standard_deviation, 2))

# A typical range: mean plus or minus 2 standard deviations
print(expected_acceptances - 2 * standard_deviation, expected_acceptances + 2 * standard_deviation)
```
Output:
```
80.0 16.0 4.0
72.0 88.0
```
Plan for 80 joiners, and do not be surprised by anything from 72 to 88. Excel: `=100*0.8` and `=SQRT(100*0.8*0.2)` (any version).
**Likely follow-ups:** 1) *Why does SD matter for planning?* It tells HR how much buffer (extra offers) to hold. 2) *When does it break?* If acceptance chances differ by candidate or are linked.
**Common mistakes:** Giving the variance (16) as the SD; forgetting the (1-p) term.

### Q20 ⭐⭐ 🟡 An HR team averages 3 resignations a month. Assuming Poisson, what is the probability of zero resignations next month?
**Asked at:** commonly asked (no company-specific report found); Poisson count problems are standard in prep lists.
**What the interviewer is checking:** Can you use the Poisson formula, and do you know e to the minus lambda for "zero events"?
**Say this in the interview:** "With a Poisson average of 3, the chance of zero is e to the power minus 3, about 0.05, so roughly a 5% chance of a month with no resignations."
**Explain simply:**
- **Poisson distribution** counts how many times a random event happens in a fixed window (a month, an hour) when we only know the average rate.
- The average rate is called **lambda** (here 3 per month).
- For zero events the formula collapses to e^(-lambda), where e is about 2.718.
**Formula in plain words:** probability of k events = (average^k x e^(-average)) divided by k factorial. For k = 0 this is just e^(-average). Symbols: P(k) = lambda^k e^(-lambda) / k!.
**Worked example:** e^(-3) = 0.0498. So a resignation-free month is rare (about 1 month in 20). Chance of at least one resignation = 1 - 0.0498 = 0.9502.
**Excel / Python:**
```python
from math import exp
from scipy import stats

average_resignations = 3

# Chance of zero resignations: e to the power minus the average
chance_of_zero = exp(-average_resignations)
print(round(chance_of_zero, 4))

# Cross-check with the library
print(round(stats.poisson.pmf(0, 3), 4))
```
Output:
```
0.0498
0.0498
```
About a 5% chance. Excel (2010+; not run in Excel here): `=POISSON.DIST(0,3,FALSE)` returns 0.0498.
**Likely follow-ups:** 1) *Chance of exactly 1?* 3 x e^(-3) = 0.1494. 2) *Chance of at least 1?* 1 - 0.0498 = 0.9502.
**Common mistakes:** Using the binomial without a number of trials; forgetting that "exactly 0" and "at most 0" are the same only here.

### Q21 ⭐⭐ 🟡 A support desk gets 15 tickets per hour on average. How do you get the rate for 30 minutes, and what is the probability of no tickets in that time?
**Asked at:** commonly asked (no company-specific report found); rate rescaling appears in textbook-style call-centre problems.
**What the interviewer is checking:** Do you match the rate to the time window before using Poisson?
**Say this in the interview:** "The Poisson rate scales with time. 15 per hour becomes 7.5 per half hour. The chance of zero tickets is e to the minus 7.5, about 0.0006, so almost never."
**Explain simply:**
- The rate (lambda) must always describe the same window as the question.
- Half the time means half the expected tickets: 15 x 0.5 = 7.5.
- Then use the "zero events" shortcut e^(-lambda).
**Formula in plain words:** new rate = old rate x (new window / old window). Then P(zero) = e^(-new rate).
**Worked example:** 7.5 tickets expected in 30 minutes; P(0) = 0.000553, about 1 in 1,800 half-hours.
**Excel / Python:**
```python
from math import exp

tickets_per_hour = 15
hours_in_window = 30 / 60

# Rescale the rate to a 30-minute window
tickets_in_30_minutes = tickets_per_hour * hours_in_window

# Chance of zero tickets in that window
chance_of_zero = exp(-tickets_in_30_minutes)
print(tickets_in_30_minutes, round(chance_of_zero, 6))
```
Output:
```
7.5 0.000553
```
A silent half hour is extremely unlikely under this model. Excel (2010+; not run in Excel here): `=POISSON.DIST(0,15*30/60,FALSE)` returns 0.000553.
**Likely follow-ups:** 1) *What if I used 15 for 30 minutes?* You get e^-15, wrong by a huge factor. 2) *Does the rate stay constant all day?* Often not (peak hours); see Q34.
**Common mistakes:** Not rescaling lambda; mixing hours and minutes.

### Q22 ⭐⭐ 🟡 For a Poisson distribution mean equals variance. What does it mean if your data's variance is much larger than its mean?
**Asked at:** commonly asked (no company-specific report found); the mean-equals-variance property is a standard Poisson check.
**What the interviewer is checking:** Do you know the Poisson assumptions can fail, and what the name for that is?
**Say this in the interview:** "That is called overdispersion. It tells me a plain Poisson is too simple: events cluster, or the rate varies between periods. I would consider a negative binomial model or split the data by the factor that changes the rate."
**Explain simply:**
- **Variance** measures spread. A true Poisson has spread exactly equal to its average.
- **Overdispersion:** variance bigger than mean, so counts are more bunched or erratic than Poisson allows.
- Typical causes: bursts (events arriving in clusters), rates that change by day or team, or a mix of different groups.
- Practical effect: Poisson-based probabilities understate the chance of extreme counts.
**Formula in plain words:** ratio = variance / mean. About 1 fits Poisson; clearly above 1 means overdispersion.
**Worked example:** A simulated true Poisson with mean 5 gave mean 4.94 and variance 5.04 (ratio about 1.02). A 30-day absence log (Q34) had mean 4.57 and variance 16.19 (ratio 3.5), so Poisson is a poor fit.
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(42)

# 1000 days of counts from a true Poisson with average 5
poisson_counts = random_generator.poisson(5, 1000)

# Mean and variance should be close to each other
print(poisson_counts.mean().round(2), poisson_counts.var().round(2))
```
Output:
```
4.94 5.04
```
Mean and variance are close, as expected for real Poisson data. Excel: compare `=AVERAGE(range)` with `=VAR.S(range)` (VAR.S needs 2010+; not run in Excel here).
**Likely follow-ups:** 1) *Underdispersion?* Variance below mean: events more regular than random. 2) *Fix?* Negative binomial, or model the changing rate.
**Common mistakes:** Calling a ratio of 1.3 "wildly off" with no sample-size thought; ignoring it and trusting Poisson tail probabilities.

### Q23 ⭐⭐ 🟡 Exam scores have a mean of 70 and an SD of 10. What is the z-score of 85, and roughly what percentile is it?
**Asked at:** commonly asked (no company-specific report found); z-score questions appear in every stats list we found.
**What the interviewer is checking:** Can you standardise a value and read a percentile off the normal curve?
**Say this in the interview:** "z = (85 - 70) / 10 = 1.5, so 1.5 standard deviations above the mean. Assuming roughly normal scores, that is about the 93rd percentile."
**Explain simply:**
- **z-score:** how many standard deviations a value sits above (+) or below (-) the mean.
- **Percentile:** the share of people scoring below. The normal curve table (or function) converts z to that share.
- Rule of thumb: z = 1 is about the 84th percentile, z = 2 about the 98th, so 1.5 falls between.
**Formula in plain words:** z = (value minus mean) divided by standard deviation.
**Worked example:** (85 - 70)/10 = 1.5; the area below z = 1.5 is 0.9332, so about 93.3% score lower.
**Excel / Python:**
```python
from scipy import stats

score = 85
class_mean = 70
class_sd = 10

# Distance from the mean in standard deviations
z_score = (score - class_mean) / class_sd

# Share of people scoring below this z-score
percentile_share = stats.norm.cdf(z_score)
print(z_score, round(percentile_share, 4))
```
Output:
```
1.5 0.9332
```
The score beats about 93% of the group. Excel (2010+; not run in Excel here): `=NORM.S.DIST(1.5,TRUE)` returns 0.9332, or `=NORM.DIST(85,70,10,TRUE)`.
**Likely follow-ups:** 1) *What if scores are skewed?* The percentile is then unreliable; count real ranks (`PERCENTRANK`). 2) *z of -1.5?* About the 7th percentile.
**Common mistakes:** Dividing by variance; saying 93% scored "equal to" instead of below; applying it to non-normal data.

### Q24 ⭐⭐ 🟡 Scores are normal with a mean of 60 and an SD of 12. What cut-off marks the top 10% of employees?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you run the normal curve backwards: from a probability to a score?
**Say this in the interview:** "Top 10% means the 90th percentile, where z is about 1.28. The cut-off is 60 + 1.28 x 12, about 75.4. So roughly anyone above 75 is in the top tenth."
**Explain simply:**
- Going from a score to a percentage uses the CDF (Q33); going from a percentage to a score uses its inverse (the "quantile" or "percent point" function).
- Find the z for the 90th percentile (1.2816), then convert back to marks.
**Formula in plain words:** cut-off = mean + z x standard deviation.
**Worked example:** z = 1.2816; cut-off = 60 + 1.2816 x 12 = 75.38. Check: share above 75.38 is 10.0%.
**Excel / Python:**
```python
from scipy import stats

mean_score = 60
sd_score = 12

# z-score that has 90% of the curve below it
z_for_top_10 = stats.norm.ppf(0.90)

# Convert that z-score back into marks
cutoff_score = mean_score + z_for_top_10 * sd_score
print(round(z_for_top_10, 4), round(cutoff_score, 2))

# Check: share of employees scoring above the cut-off
print(round(1 - stats.norm.cdf(cutoff_score, mean_score, sd_score), 4))
```
Output:
```
1.2816 75.38
0.1
```
About 75.4 marks and above is the top 10%. Excel (2010+; not run in Excel here): `=NORM.INV(0.9,60,12)` returns 75.38.
**Likely follow-ups:** 1) *Bottom 10%?* 60 - 15.38 = 44.62. 2) *Top 5%?* z = 1.645, cut-off 79.7.
**Common mistakes:** Using 0.10 instead of 0.90 in the inverse function; using z = 1.96 (that is for the middle 95%).

### Q25 ⭐⭐ 🟡 How do you check whether a dataset is normally distributed?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you combine pictures and numbers, and avoid trusting one test blindly?
**Say this in the interview:** "First a histogram and a Q-Q plot to see the shape, then skewness and kurtosis numbers, and a Shapiro-Wilk test as a formal check. I treat the picture as primary, because tests get overly strict with large samples."
**Explain simply:**
- **Histogram:** bars showing how values spread; a normal one is a symmetric bell.
- **Q-Q plot:** plots your sorted data against what a normal would give; points on a straight line mean normal-like.
- **Skewness near 0 and excess kurtosis near 0** support normality (Q11).
- **Shapiro-Wilk test:** a p-value below 0.05 suggests the data is not normal. Needs care: large samples flag tiny, harmless differences.
**Worked example:** 200 simulated scores (mean 60, SD 12) versus 200 simulated salaries (a right-skewed, lognormal type):
**Excel / Python:**
```python
import numpy as np
from scipy import stats

random_generator = np.random.default_rng(42)

# Two samples: bell-shaped scores and right-skewed salaries
scores = random_generator.normal(loc=60, scale=12, size=200)
salaries = random_generator.lognormal(mean=10.5, sigma=0.6, size=200)

for label, values in [("scores", scores), ("salaries", salaries)]:
    # Measure of lopsidedness and of tail heaviness
    skewness = stats.skew(values)
    excess_kurtosis = stats.kurtosis(values)

    # Formal test: small p-value means "not normal"
    shapiro_p_value = stats.shapiro(values).pvalue
    print(label, "skew", round(skewness, 2), "excess kurt", round(excess_kurtosis, 2),
          "Shapiro p", round(shapiro_p_value, 4))
```
Output:
```
scores skew 0.26 excess kurt -0.01 Shapiro p 0.4893
salaries skew 1.98 excess kurt 5.85 Shapiro p 0.0
```
Scores look normal (p well above 0.05, small skew). Salaries fail clearly (high skew, p effectively 0). For the plot: `scipy.stats.probplot` or Excel histogram plus a normal-curve overlay. Excel has no built-in normality test; use `=SKEW(range)` and `=KURT(range)`.
**Likely follow-ups:** 1) *Is the test enough alone?* No: look at the plot. 2) *What if not normal?* Transform (log), use medians, or non-parametric methods.
**Common mistakes:** Trusting p > 0.05 as proof of normality on tiny samples; relying only on skewness.

### Q26 ⭐⭐ 🟡 Why does the mean get pulled toward the tail in skewed data, and what do you do about it?
**Asked at:** commonly asked (no company-specific report found); mean vs median under skew is in standard lists (e.g. DataCamp).
**What the interviewer is checking:** Do you understand that the mean uses every value's size, while the median uses only position?
**Say this in the interview:** "The mean adds up actual values, so a few very large ones drag it upward. The median only cares about the middle position. So for skewed data like salaries I report the median, or show both, or log-transform before modelling."
**Explain simply:**
- The mean is the balance point; one huge value far out forces the balance point toward it.
- The median ignores how big the extremes are; it only needs them to be above or below the middle.
- Options: report median; trim or winsorise outliers (after checking they are real); log-transform; show the full distribution.
**Worked example:** Salaries 25k to 100k (Q27): mean 45,000 and median 38,000. Drop the 100k person and the mean falls to 38,125 while the median only moves to 36,000. The mean was the sensitive one.
**Excel / Python:**
```python
import pandas as pd

monthly_salaries = pd.Series([25000, 28000, 30000, 34000, 38000, 42000, 48000, 60000, 100000])
print(monthly_salaries.mean(), monthly_salaries.median())

# Remove the single highest salary and compare again
without_top_earner = monthly_salaries.drop(monthly_salaries.idxmax())
print(without_top_earner.mean(), without_top_earner.median())
```
Output:
```
45000.0 38000.0
38125.0 36000.0
```
One person shifted the mean by almost 7,000 but the median by only 2,000. Excel: `=AVERAGE(range)`, `=MEDIAN(range)`.
**Likely follow-ups:** 1) *Delete the outlier?* Only if it is an error; a real CEO salary is real data. 2) *Best single number?* Median plus a spread measure such as IQR.
**Common mistakes:** Reporting the mean salary as "typical"; deleting outliers just because they are big.

### Q27 ⭐⭐ 🟡 Mean salary is 45,000 and median is 38,000. What does this say about the shape, and what would you tell the manager?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you read shape from mean versus median and translate it for a manager?
**Say this in the interview:** "Mean above median means right-skewed: a few high earners pull the average up. The typical employee earns closer to 38,000. I would give the manager the median, and mention that the mean is inflated by top salaries."
**Explain simply:**
- Mean > median: right (positive) skew. Mean < median: left skew. About equal: roughly symmetric.
- The 7,000 gap shows how much the high earners lift the average.
- Half of employees earn less than 38,000 (the median), and more than half earn less than the 45,000 mean, which is typical of right skew.
**Worked example:** Nine salaries: 25k, 28k, 30k, 34k, 38k, 42k, 48k, 60k, 100k. Mean 45,000, median 38,000; 6 of 9 (67%) earn less than the mean. Sample skewness is +1.92 (positive means right skew).
**Excel / Python:**
```python
import pandas as pd

monthly_salaries = pd.Series([25000, 28000, 30000, 34000, 38000, 42000, 48000, 60000, 100000])

average_salary = monthly_salaries.mean()
median_salary = monthly_salaries.median()
skewness = monthly_salaries.skew()
below_mean_count = (monthly_salaries < average_salary).sum()
print(average_salary, median_salary, round(skewness, 2), below_mean_count)
```
Output:
```
45000.0 38000.0 1.92
6
```
Six of nine people earn below the "average", a clear sign of right skew. Excel: `=SKEW(range)` (all versions).
**Likely follow-ups:** 1) *Which would you report?* Median, plus a range or percentiles. 2) *Does this prove skew?* It is a strong hint; confirm with a histogram.
**Common mistakes:** Telling the manager "the average employee earns 45,000"; assuming mean > median always means skew (small samples can mislead).

### Q28 ⭐⭐ 🟡 Does zero skewness mean the data is normally distributed?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a single number cannot prove a shape?
**Say this in the interview:** "No. Zero skewness only says the data is balanced left and right. Many symmetric shapes, like uniform or a two-humped bimodal, have zero skew but are not normal. I would also check kurtosis and a histogram or Q-Q plot."
**Explain simply:**
- **Skewness** measures lopsidedness only; symmetric does not mean bell-shaped.
- A uniform distribution (flat) is symmetric with skew 0 but has negative excess kurtosis (-1.2).
- Normal data should have both skew near 0 and excess kurtosis near 0, and also look right on a Q-Q plot.
**Worked example:** The numbers 1 to 100 each appearing once (a flat, uniform spread) have skew 0.0 but excess kurtosis about -1.2.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Flat spread: every value from 1 to 100 once
flat_values = np.arange(1, 101)
print(round(stats.skew(flat_values), 2), round(stats.kurtosis(flat_values), 2))
```
Output:
```
0.0 -1.2
```
Perfectly symmetric (skew 0) but clearly not bell-shaped (kurtosis -1.2).
**Likely follow-ups:** 1) *What else to check?* Kurtosis, Q-Q plot, Shapiro-Wilk. 2) *Reverse: normal implies zero skew?* Yes.
**Common mistakes:** Saying skew 0 is proof of normality.

### Q29 ⭐⭐ 🟡 Student A scored 80 (class mean 70, SD 5) and Student B scored 85 (class mean 80, SD 10). Who performed better relative to their class?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you compare using z-scores rather than raw marks?
**Say this in the interview:** "I convert both to z-scores. A: (80-70)/5 = 2.0. B: (85-80)/10 = 0.5. A is two standard deviations above their class, B only half, so A did better relatively even though B's raw score is higher."
**Explain simply:**
- Raw marks are not comparable across groups with different averages and spreads.
- z-scores put everyone on one scale: "how unusual is this score within its own group?"
- Same idea for comparing employees across teams with different rating habits.
**Worked example:** A's z = 2.0 (about the 97.7th percentile); B's z = 0.5 (about the 69th percentile), assuming roughly normal scores.
**Excel / Python:**
```python
from scipy import stats

# z-score for each student within their own class
z_student_a = (80 - 70) / 5
z_student_b = (85 - 80) / 10

# Rough percentile if scores are normal
percentile_a = stats.norm.cdf(z_student_a)
percentile_b = stats.norm.cdf(z_student_b)
print(z_student_a, z_student_b, round(percentile_a, 4), round(percentile_b, 4))
```
Output:
```
2.0 0.5 0.9772 0.6915
```
A beats about 97.7% of their class, B about 69.1%. Excel: `=STANDARDIZE(80,70,5)` and `=STANDARDIZE(85,80,10)`.
**Likely follow-ups:** 1) *What if the classes are not normal?* Compare ranks or percentiles instead. 2) *Other uses?* Standardising KPIs across departments.
**Common mistakes:** Comparing raw marks; comparing raw distances from the mean without dividing by SD.

### Q30 ⭐⭐ 🟡 There are 20 employees and each has a 5% chance of leaving this quarter. What is the probability at least one leaves?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured binomial scenario.
**What the interviewer is checking:** Do you know the complement trick: "at least one" = 1 minus "none"?
**Say this in the interview:** "Chance nobody leaves is 0.95 to the power 20, about 0.36. So the chance at least one leaves is 1 minus that, about 64%."
**Explain simply:**
- "At least one" covers 1, 2, 3 ... 20 leavers; adding all is tedious.
- Easier: find the one outcome that is not included (zero leavers) and subtract from 1.
- Assumes employees decide independently with the same 5% chance.
**Formula in plain words:** P(at least one) = 1 - (chance of staying)^(number of people).
**Worked example:** 0.95^20 = 0.3585; 1 - 0.3585 = 0.6415. Even with a low 5% individual risk, a team of 20 has a 64% chance of at least one departure.
**Excel / Python:**
```python
number_of_employees = 20
chance_of_leaving = 0.05

# Chance that all 20 stay
chance_nobody_leaves = (1 - chance_of_leaving) ** number_of_employees

# Complement: at least one leaves
chance_at_least_one_leaves = 1 - chance_nobody_leaves
print(round(chance_nobody_leaves, 4), round(chance_at_least_one_leaves, 4))
```
Output:
```
0.3585 0.6415
```
Roughly two quarters in three will see at least one exit. Excel (2010+; not run in Excel here): `=1-BINOM.DIST(0,20,0.05,TRUE)` returns 0.6415.
**Likely follow-ups:** 1) *Expected leavers?* 20 x 0.05 = 1. 2) *Independence?* Team morale makes leaving correlated, so reality can be lumpier.
**Common mistakes:** Computing 20 x 5% = 100%; adding probabilities for each person.

### Q31 ⭐⭐ 🟡 A data point lies 4 standard deviations from the mean. What do you conclude, and what would you do next?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you flag it as unusual without automatically deleting it, and investigate?
**Say this in the interview:** "If the data is roughly normal, a point 4 SD out is extremely rare: about 1 in 16,000. So it is either a data error, a different kind of record, or the data has heavier tails than normal. I would check the source, then decide, not delete it blindly."
**Explain simply:**
- Under a normal curve, only about 0.006% of values fall beyond 4 SD on either side (1 in 15,787).
- In a dataset of 1,000 employees you would expect 0.06 such points, so seeing one is a red flag.
- Next steps: verify it is not a typo (an extra zero in salary), check if it belongs to another group (a director among analysts), and if real, keep it and use robust methods (median, log scale).
- For non-normal data, Chebyshev's inequality still guarantees at most 1/16 (6.25%) beyond 4 SD, so "rare" is weaker without normality.
**Worked example:** two-sided probability 2 x 0.0000317 = 0.0000633, i.e. one in 15,787. Expected count in 1,000 employees: 0.063.
**Excel / Python:**
```python
from scipy import stats

# Chance of a value at least 4 SD away on either side (normal curve)
two_sided_probability = 2 * stats.norm.sf(4)
one_in = 1 / two_sided_probability

# Expected number of such points among 1,000 employees
expected_count_in_1000 = 1000 * two_sided_probability
print(two_sided_probability, round(one_in), round(expected_count_in_1000, 3))
```
Output:
```
6.334248366623973e-05 15787 0.063
```
Very rare under normality, so investigate. Excel (2010+; not run in Excel here): `=2*(1-NORM.S.DIST(4,TRUE))`.
**Likely follow-ups:** 1) *Remove it?* Only if it is an error. 2) *Common outlier rule?* 3 SD or 1.5 x IQR; both are guides, not laws.
**Common mistakes:** Deleting without checking; assuming the 68-95-99.7 rule works for skewed data.

### Q32 ⭐⭐ 🟡 When can a normal distribution approximate a binomial distribution?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the rule of thumb and the continuity correction?
**Say this in the interview:** "When n is large enough that both n x p and n x (1-p) are at least 10. Then the binomial looks bell-shaped with mean np and SD sqrt(np(1-p)). I add a continuity correction of 0.5 for better accuracy."
**Explain simply:**
- Binomial counts are whole numbers; the normal is smooth. With enough tries and a probability not too close to 0 or 1, the steps blend into a bell.
- **Continuity correction:** to find P(X <= 55), ask the normal for P(X <= 55.5), since 55 "occupies" 54.5 to 55.5.
- If p is tiny (rare events) the Poisson is a better approximation (Q49).
**Worked example:** 100 offers, 50% accept. P(55 or fewer accept) exactly = 0.8644. Normal (mean 50, SD 5): without correction 0.8413; with 55.5, 0.8643. Bad case: n = 10, p = 0.1 (np = 1): exact P(2 or fewer) = 0.9298 versus normal 0.9431.
**Excel / Python:**
```python
from math import sqrt
from scipy import stats

number_of_offers = 100
chance_of_acceptance = 0.5
mean_acceptances = number_of_offers * chance_of_acceptance
sd_acceptances = sqrt(number_of_offers * chance_of_acceptance * (1 - chance_of_acceptance))

# Exact binomial answer
exact = stats.binom.cdf(55, number_of_offers, chance_of_acceptance)
# Normal approximation without and with the 0.5 correction
normal_plain = stats.norm.cdf(55, mean_acceptances, sd_acceptances)
normal_corrected = stats.norm.cdf(55.5, mean_acceptances, sd_acceptances)
print(round(exact, 4), round(normal_plain, 4), round(normal_corrected, 4))

# Small, rare-event case where the rule of thumb fails
exact_small = stats.binom.cdf(2, 10, 0.1)
normal_small = stats.norm.cdf(2.5, 10 * 0.1, sqrt(10 * 0.1 * 0.9))
print(round(exact_small, 4), round(normal_small, 4))
```
Output:
```
0.8644 0.8413 0.8643
0.9298 0.9431
```
The corrected normal is nearly exact when n x p and n x (1-p) are large; it is off when they are small.
**Likely follow-ups:** 1) *Why does it work?* Central Limit Theorem: a binomial is a sum of many 0/1 trials. 2) *Why bother when software exists?* Hand calculation and large-n speed.
**Common mistakes:** Skipping the continuity correction; using it when np is tiny.

### Q33 ⭐⭐ 🟡 What is the difference between a probability mass function, a probability density function and a cumulative distribution function?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know which function gives exact-value probability, which gives a curve height, and which gives "up to" totals?
**Say this in the interview:** "PMF is for discrete data and gives the probability of an exact value. PDF is for continuous data; its height is not a probability, but the area under it between two points is. CDF works for both and gives the probability of being at or below a value."
**Explain simply:**
- **PMF (probability mass function):** discrete counts like 0, 1, 2 resignations; each count has a probability, and they add to 1.
- **PDF (probability density function):** continuous values like salary; the chance of one exact value is zero (Q45), so you read areas under the curve.
- **CDF (cumulative distribution function):** running total of probability up to a value; always rises from 0 to 1.
- Link: CDF = adding up the PMF (discrete) or area under the PDF (continuous).
**Worked example:** 5 coin tosses (binomial, p = 0.5): PMF P(exactly 3 heads) = 0.3125; CDF P(3 or fewer) = 0.8125. For the standard normal: PDF at 0 = 0.3989 (a height, not a probability); CDF at 0 = 0.5; area between -1 and 1 = 0.6827.
**Excel / Python:**
```python
from scipy import stats

# Discrete: PMF (exactly) and CDF (this many or fewer)
exactly_3_heads = stats.binom.pmf(3, 5, 0.5)
three_or_fewer_heads = stats.binom.cdf(3, 5, 0.5)
print(round(exactly_3_heads, 4), round(three_or_fewer_heads, 4))

# Continuous: PDF (curve height), CDF, and area between two points
height_at_zero = stats.norm.pdf(0)
half_below_zero = stats.norm.cdf(0)
area_within_one_sd = stats.norm.cdf(1) - stats.norm.cdf(-1)
print(round(height_at_zero, 4), round(half_below_zero, 4), round(area_within_one_sd, 4))
```
Output:
```
0.3125 0.8125
0.3989 0.5 0.6827
```
Excel (2010+; not run in Excel here): `=BINOM.DIST(3,5,0.5,FALSE)` is the PMF, `=BINOM.DIST(3,5,0.5,TRUE)` the CDF; `=NORM.DIST(0,0,1,FALSE)` the PDF, `=NORM.DIST(0,0,1,TRUE)` the CDF. The last argument FALSE/TRUE switches between them.
**Likely follow-ups:** 1) *Can a PDF exceed 1?* Yes, a narrow curve can be taller than 1; only area must total 1. 2) *Which for percentiles?* The CDF or its inverse.
**Common mistakes:** Reading PDF height as probability; using PMF for continuous data.

### Q34 ⭐⭐ 🟡 What assumptions does a Poisson model make, and would daily absenteeism counts satisfy them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you state the assumptions and test them against a realistic HR example?
**Say this in the interview:** "Poisson assumes events are independent, happen at a constant average rate, occur one at a time, and in a fixed window. Daily absenteeism often breaks these: Mondays, festivals, flu and team outbreaks create clusters and changing rates. So I would test mean versus variance and probably need a richer model."
**Explain simply:**
- **Independent:** one absence does not make another more likely. (Infection, shared events break this.)
- **Constant rate:** same average on every day. (Mondays and festival weeks differ.)
- **Events one at a time:** two absences do not occur at exactly the same instant (usually fine for counts per day).
- **Fixed window:** per day, per month, with a known length.
- **Check:** compare variance with mean (Q22).
**Worked example:** A 30-day absence log (illustrative, made-up numbers) has mean 4.57 and variance 16.19 (ratio 3.54). Five days had 12 or more absentees, yet a Poisson with mean 4.57 gives only a 0.27% chance (about 0.08 days in 30) of 12 or more. Not Poisson.
**Excel / Python:**
```python
import pandas as pd
from scipy import stats

# 30 days of illustrative absence counts, with a few spike days
daily_absences = pd.Series([2, 3, 2, 4, 3, 12, 14, 3, 2, 3, 4, 3, 13, 2, 3,
                            1, 2, 3, 15, 4, 3, 2, 3, 4, 12, 3, 2, 3, 4, 3])
mean_absences = daily_absences.mean()
variance_absences = daily_absences.var()
print(round(mean_absences, 2), round(variance_absences, 2), round(variance_absences / mean_absences, 2))

# Chance of 12 or more absences on a day if Poisson held, and spike days actually seen
chance_12_or_more = stats.poisson.sf(11, mean_absences)
spike_days_seen = (daily_absences >= 12).sum()
print(round(chance_12_or_more, 5), spike_days_seen)
```
Output:
```
4.57 16.19 3.54
0.0027 5
```
Spikes occur far more often than Poisson predicts (5 days observed versus about 0.08 expected), so the model fails. A better approach is a negative binomial or modelling weekday and season. Excel: `=VAR.S(range)/AVERAGE(range)`.
**Likely follow-ups:** 1) *What would you do instead?* Negative binomial, or separate rates by weekday. 2) *When does Poisson work?* Rare, independent events such as ticket arrivals in steady periods.
**Common mistakes:** Assuming any count data is Poisson; ignoring clustering and seasonality.

### Q35 ⭐ 🟢 What is a uniform distribution? Give a business example.
**Asked at:** commonly asked (no company-specific report found); a standard item in generic distribution lists.
**What the interviewer is checking:** Do you know the "every value equally likely" shape and can you name a real case?
**Say this in the interview:** "A uniform distribution means every value in a range is equally likely, so the graph is a flat rectangle. For example, if a shuttle leaves every 20 minutes and I arrive at a random moment, my wait is uniform between 0 and 20 minutes."
**Explain simply:**
- Continuous uniform: any value between a minimum and a maximum (like the wait time). Discrete uniform: a fixed list of outcomes with equal chance (a fair die, each face 1 in 6).
- Because the rectangle is flat, a probability is just "width of my window divided by total width".
- Real data is rarely uniform. It is used for random assignment (picking employees for a survey at random) and for simulations.
**Formula in plain words:** Chance of landing in a window = window width divided by total width. Mean = halfway point = (a+b)/2. SD = (b-a)/√12.
**Worked example:** Shuttle wait is uniform from 0 to 20 minutes. Chance of waiting 5 minutes or less = 5/20 = 0.25.
**Excel / Python:**
```python
from scipy import stats

# Shuttle leaves every 20 minutes, so wait is uniform from 0 to 20
shortest_wait = 0
longest_wait = 20
wait_distribution = stats.uniform(loc=shortest_wait, scale=longest_wait - shortest_wait)

# Chance of waiting 5 minutes or less
chance_wait_5_or_less = wait_distribution.cdf(5)

# Chance of waiting between 10 and 15 minutes
chance_wait_10_to_15 = wait_distribution.cdf(15) - wait_distribution.cdf(10)

average_wait = wait_distribution.mean()
spread_of_wait = wait_distribution.std()
print("P(wait <= 5 min):", chance_wait_5_or_less)
print("P(10 to 15 min):", chance_wait_10_to_15)
print("mean wait:", average_wait)
print("SD of wait:", round(spread_of_wait, 2))
```
Output: `P(wait <= 5 min): 0.25`, `P(10 to 15 min): 0.25`, `mean wait: 10.0`, `SD of wait: 5.77`. Equal-width windows always have equal chance.
**Likely follow-ups:** 1) *What does RAND() in Excel give?* A uniform number between 0 and 1. 2) *Is a uniform graph a bell?* No, it is flat with no peak.
**Common mistakes:** Assuming "random" means uniform (it only means uniform if every value is equally likely); forgetting the edges are hard limits.

### Q36 ⭐ 🟡 What is a lognormal distribution, and why do salaries and sales often follow it?
**Asked at:** commonly asked (no company-specific report found); log transform for right-skewed data is a standard topic.
**What the interviewer is checking:** Can you connect a skewed real-world variable to a log transform?
**Say this in the interview:** "A variable is lognormal when its logarithm is normally distributed. The raw values are right-skewed with a long tail, but after taking logs they look like a bell. Salaries and sales behave this way because they grow by percentages, not fixed amounts."
**Explain simply:**
- Logarithm (log): the power you raise a base to; it turns multiplying into adding and squeezes big numbers.
- Pay rises, price changes and sales growth multiply (a 10% raise, then 8%), and multiplied effects give a lognormal shape.
- Values cannot go below zero, but have no upper limit: a few very high earners stretch the right tail.
- Practical use: take the log of the column, then use normal-based tools on the log values.
**Worked example:** Simulated salaries with median about 40,000 (made up for illustration).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

random_generator = np.random.default_rng(42)

# Make 10,000 salaries whose logs are normal (this is what lognormal means)
log_of_salaries = random_generator.normal(loc=np.log(40000), scale=0.5, size=10000)
salaries = np.exp(log_of_salaries)

print("mean salary:", round(salaries.mean()))
print("median salary:", round(np.median(salaries)))
print("skewness of salaries:", round(stats.skew(salaries), 2))
print("skewness of log(salaries):", round(stats.skew(np.log(salaries)), 2))
```
Output: mean 45168, median 39738, skewness 1.79, skewness of the logs -0.0. The mean sits above the median (right skew) and the logs are symmetric. In Excel, add a helper column `=LN(B2)` and chart that (not run in Excel here).
**Likely follow-ups:** 1) *Why median for salaries?* The tail drags the mean up. 2) *What if values include zero?* Log of zero is undefined; use log(1+x) or handle zeros separately.
**Common mistakes:** Saying the log of the data is lognormal (it is the other way round); forgetting to convert results back with exp.

### Q37 ⭐ 🟡 How does a t-distribution differ from the normal distribution, and when is it used?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know small samples need wider, safer cut-offs?
**Say this in the interview:** "The t-distribution looks like a bell curve but with fatter tails. I use it when the sample is small and I do not know the true standard deviation, so I estimate it from the sample. With more data it becomes almost identical to the normal."
**Explain simply:**
- Estimating the SD from a small sample adds extra uncertainty, so the t-curve leaves more probability in the tails.
- Shape depends on degrees of freedom (df), roughly sample size minus 1. Small df means fatter tails; large df means nearly normal (about 30 or more is close).
- Used for confidence intervals and t-tests on means, for example comparing average engagement scores of two small teams.
**Worked example:** Cut-offs for a 95% interval, using real numbers below. With 5 employees (df 4) you multiply by 2.776, not 1.96, so the interval is wider.
**Excel / Python:**
```python
from scipy import stats

# 97.5th percentile cut-off for a 95% confidence interval, by sample size
for degrees_of_freedom in [4, 9, 29, 1000]:
    cutoff = stats.t.ppf(0.975, df=degrees_of_freedom)
    print("df =", degrees_of_freedom, "t cut-off =", round(cutoff, 3))

normal_cutoff = stats.norm.ppf(0.975)
print("normal cut-off =", round(normal_cutoff, 3))

# Chance of being more than 2.5 away from the centre, both sides
print("normal  P(|Z|>2.5):", round(2 * stats.norm.sf(2.5), 4))
print("t df=4  P(|T|>2.5):", round(2 * stats.t.sf(2.5, df=4), 4))
```
Output: 2.776, 2.262, 2.045, 1.962 versus 1.96 for normal; tail chance 0.0124 (normal) versus 0.0668 (t, df 4). Small samples need bigger cut-offs. Excel (2010+): `=T.INV.2T(0.05, 9)` returns 2.262 (not run in Excel here).
**Likely follow-ups:** 1) *When does t equal normal?* As df grows large. 2) *Is the data itself t-distributed?* No, it is the sample mean's standardised value.
**Common mistakes:** Using 1.96 for tiny samples; thinking t is only for "non-normal" data.

### Q38 ⭐ 🟡 What is the exponential distribution, and how is it related to the Poisson distribution?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you see Poisson as "how many events" and exponential as "how long until the next one"?
**Say this in the interview:** "If events happen at a steady average rate, Poisson counts how many occur in a period, and the exponential models the waiting time between them. They describe the same process from two angles, and share the same rate."
**Explain simply:**
- Rate (lambda): average events per unit time, e.g. 3 resignations per month.
- Average wait between events = 1 divided by the rate (1/3 month, about 10 days).
- Memoryless: if no one has resigned for 20 days, the chance of one in the next 5 days is unchanged.
- Link: "no events in a period" for Poisson is the same as "waiting time longer than the period" for exponential.
**Formula in plain words:** Chance wait is longer than t = e raised to minus (rate times t), i.e. P(T > t) = e^(-λt).
**Worked example:** 3 resignations a month. Chance of no resignation in a month = e^-3 = 0.0498 by either route.
**Excel / Python:**
```python
from scipy import stats

resignations_per_month = 3

# Poisson: chance of zero resignations in one month
chance_zero_in_month = stats.poisson.pmf(0, mu=resignations_per_month)

# Exponential: chance the wait for the next resignation exceeds one month
average_wait_months = 1 / resignations_per_month
chance_wait_over_month = stats.expon.sf(1, scale=average_wait_months)

print("Poisson P(0 in a month):", round(chance_zero_in_month, 4))
print("Exponential P(wait > 1 month):", round(chance_wait_over_month, 4))
print("average wait in days (30-day month):", round(average_wait_months * 30, 1))
print("P(wait <= 10 days):", round(stats.expon.cdf(10 / 30, scale=average_wait_months), 4))
```
Output: both 0.0498; average wait 10.0 days; 63.21% chance the next resignation comes within 10 days. Excel: `=EXPON.DIST(1, 3, TRUE)` gives 0.9502, which is 1 minus 0.0498 (not run in Excel here).
**Likely follow-ups:** 1) *Why is the average wait not the median?* The exponential is right-skewed; the median is about 0.69 times the mean. 2) *Memoryless meaning?* Past waiting does not change the future.
**Common mistakes:** Mixing up rate and mean wait (one is the inverse of the other); using it when events cluster (e.g. resignations after bonus day).

### Q39 ⭐ 🟡 What is a bimodal distribution, and what might it mean for HR data such as employee tenure or salary?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you notice two peaks and know the average is misleading there?
**Say this in the interview:** "Bimodal means the histogram has two peaks. It usually signals two different groups mixed together, for example a wave of recent hires and a group of long-serving staff. I would split the data by group before summarising."
**Explain simply:**
- Mode: the most common value or range. Two humps give two modes.
- Typical causes in HR: hiring waves, junior and senior bands, two job families (support and engineering), two locations.
- The mean can land in the valley where almost nobody sits, so "average tenure" describes nobody.
**Worked example:** 300 recent hires near 1.5 years and 200 veterans near 9 years (simulated).
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(1)

# Two groups: recent hires around 1.5 years, long-serving staff around 9 years
recent_hires = random_generator.normal(1.5, 0.6, 300)
long_serving = random_generator.normal(9, 1.5, 200)
tenure_years = np.concatenate([recent_hires, long_serving])

print("mean tenure:", round(tenure_years.mean(), 1))
print("median tenure:", round(np.median(tenure_years), 1))

# Count people near the mean
near_mean = (tenure_years > 4.5) & (tenure_years < 6.5)
print("people with 4.5 to 6.5 years:", int(near_mean.sum()), "of", len(tenure_years))

# Text histogram, bars of 2 years
counts, edges = np.histogram(tenure_years, bins=range(0, 14, 2))
for count, start in zip(counts, edges[:-1]):
    print(f"{start:>2}-{start + 2:<2} years: {'#' * (count // 5)} {count}")
```
Output: mean 4.5 years, median 1.9, only 7 of 500 people within 4.5 to 6.5 years; the bars show humps at 0-2 (258) and 8-10 (108) with a gap at 4-6 (3). The mean 4.5 describes almost no one.
**Likely follow-ups:** 1) *What do you do next?* Segment by hire year, department or grade and describe each group. 2) *Could bin width hide it?* Yes (Q42).
**Common mistakes:** Reporting one mean; assuming a fitted normal curve is fine.

### Q40 ⭐ 🟡 How do you use Pearson's skewness coefficient? If mean 52, median 48 and SD 8, calculate it.
**Asked at:** commonly asked (no company-specific report found); skewness with mean and median appears in standard stats lists.
**What the interviewer is checking:** Can you turn "mean above median" into a single, signed number?
**Say this in the interview:** "Pearson's second coefficient is 3 times (mean minus median) divided by the SD. Here that is 3 times 4 divided by 8, which is 1.5: strongly right-skewed. Positive means right tail, negative means left tail, near zero means roughly symmetric."
**Explain simply:**
- It measures how far the mean is pulled from the median, in SD units.
- Rough guide: between -0.5 and 0.5 close to symmetric; beyond 1 or below -1 strongly skewed.
- There is a first coefficient too: (mean minus mode) divided by SD, but the mode is unstable, so the median version is more common.
- Software usually reports a moment-based skewness instead; signs agree, sizes differ slightly.
**Formula in plain words:** Skewness = 3 times (mean minus median) divided by standard deviation; Sk = 3(mean - median)/SD.
**Worked example:** Mean 52, median 48, SD 8: 3 x (52 - 48) / 8 = 12 / 8 = 1.5.
**Excel / Python:**
```python
mean_value = 52
median_value = 48
standard_deviation = 8

# Pearson's second skewness coefficient
pearson_skewness = 3 * (mean_value - median_value) / standard_deviation
print("Pearson median skewness:", pearson_skewness)
```
Output: `1.5`, a clear right skew. In Excel: `=3*(AVERAGE(A2:A100)-MEDIAN(A2:A100))/STDEV.S(A2:A100)`, or `=SKEW(A2:A100)` for the moment-based version (not run in Excel here).
**Likely follow-ups:** 1) *What would -1.5 mean?* Left skew. 2) *Is 1.5 the maximum?* The median version is bounded between -3 and 3.
**Common mistakes:** Forgetting the factor 3; mixing SD of the population with the sample SD without saying; reading it as "percent skewed".

### Q41 ⭐ 🟡 Why can you not use the empirical rule on skewed data?
**Asked at:** commonly asked (no company-specific report found); the empirical rule appears in standard stats lists.
**What the interviewer is checking:** Do you know the 68-95-99.7 percentages belong to the bell shape only?
**Say this in the interview:** "The 68-95-99.7 percentages are derived from the symmetric normal curve. In skewed data one tail is long and the other short, so the same SD bands cover different shares, and the bands can even go into impossible values."
**Explain simply:**
- Empirical rule: about 68% within 1 SD of the mean, 95% within 2, 99.7% within 3, but only for normal-like data.
- Skewed data is lopsided: mean minus 1 SD can fall below zero for a variable like days to hire.
- Result: bands wrong in both directions, too many near the middle, and almost nothing on the short side.
**Worked example:** Days to fill a vacancy, right-skewed with mean 30 (simulated, 100,000 values).
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(7)

# Right-skewed data: days to fill a vacancy, mean about 30
days_to_fill = random_generator.exponential(scale=30, size=100000)
mean_days = days_to_fill.mean()
sd_days = days_to_fill.std()

for k in [1, 2, 3]:
    inside = np.mean(np.abs(days_to_fill - mean_days) <= k * sd_days)
    print(f"within {k} SD: {inside * 100:.1f}%")

print("mean - 1 SD =", round(mean_days - sd_days, 1), "days")
print("share above mean + 2 SD:", round(np.mean(days_to_fill > mean_days + 2 * sd_days) * 100, 1), "%")
print("share below mean - 2 SD:", round(np.mean(days_to_fill < mean_days - 2 * sd_days) * 100, 1), "%")
```
Output: 85.8%, 95.0%, 98.2% (not 68, 95, 99.7); mean minus 1 SD is 0.2 days; 5.0% above mean + 2 SD but 0.0% below mean - 2 SD. The one-SD band is far off and the tails are completely one-sided.
**Likely follow-ups:** 1) *What instead?* Percentiles, or Chebyshev (Q47). 2) *Can you transform?* Yes, take logs (Q36).
**Common mistakes:** Applying "mean plus or minus 2 SD" outlier rules to skewed data; thinking the 95% match proves the rule works.

### Q42 ⭐ 🟡 How does the choice of histogram bin width change the shape you see?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a chart is a choice, not a fact?
**Say this in the interview:** "Too wide and the bars hide detail, even two peaks. Too narrow and the histogram turns into noise with gaps. I try a few widths and pick the one that shows the stable shape."
**Explain simply:**
- Bin: a range of values (say 10,000 to 20,000) whose count becomes one bar.
- Wide bins smooth everything out; narrow bins make every small fluctuation look like a feature.
- Rules of thumb exist (Sturges, Freedman-Diaconis), but a quick visual check across 2-3 widths is practical.
- Excel histogram charts let you set "bin width" in Format Axis.
**Worked example:** 200 salaries (in thousands) from two groups, centred about 35 and 70 (simulated).
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(3)

# 200 salary values in thousands: 120 junior, 80 senior
salaries_k = np.concatenate([random_generator.normal(35, 5, 120), random_generator.normal(70, 8, 80)])

for bin_width in [40, 10, 2]:
    edges = np.arange(0, 120 + bin_width, bin_width)
    counts, _ = np.histogram(salaries_k, bins=edges)
    bars_with_data = int((counts > 0).sum())
    print("bin width", bin_width, "-> bars with data:", bars_with_data)
    if bin_width >= 10:
        print("   counts:", counts.tolist())
```
Output: width 40 gives only 3 bars (100, 90, 10), so the two groups blur; width 10 shows two clear humps (81 near 30-40, 33 and 34 near 60-80); width 2 gives 33 thin bars, noisy. Width 10 is the good choice here.
**Likely follow-ups:** 1) *Which width is right?* The one where the shape stays similar if you nudge it. 2) *Alternative?* A density plot or box plot.
**Common mistakes:** Accepting the default bins; reading gaps in a narrow histogram as real.

### Q43 ⭐ 🟡 How do you describe the distribution of employee tenure to a manager, using a histogram and summary numbers?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you turn a chart and numbers into one plain sentence?
**Say this in the interview:** "I show a histogram, then say three things: the typical value (median), the spread (middle 50% range), and the shape, for example 'most people have under 4 years, with a smaller group of long-serving staff'. For skewed data I lead with the median, not the mean."
**Explain simply:**
- Shape first: one hump or two, symmetric or tail on one side.
- Centre: median for skewed data; mean only if roughly symmetric.
- Spread: IQR (interquartile range, the distance from the 25th to the 75th percentile, i.e. the middle half of people) or min-max.
- Close with the so-what: "attrition risk is highest in years 2 to 4" or similar.
**Worked example:** 400 employees, tenure in years (simulated).
**Excel / Python:**
```python
import numpy as np
import pandas as pd

random_generator = np.random.default_rng(5)

# Tenure in years for 400 employees (right-skewed)
tenure_years = pd.Series(np.round(random_generator.gamma(shape=2.0, scale=2.0, size=400), 1))
print(tenure_years.describe().round(2))

# Middle half of employees
lower_quartile = tenure_years.quantile(0.25)
upper_quartile = tenure_years.quantile(0.75)
print("IQR:", round(upper_quartile - lower_quartile, 2))
print("skewness:", round(tenure_years.skew(), 2))

# Counts per band, for the histogram
counts, edges = np.histogram(tenure_years, bins=[0, 2, 4, 6, 8, 10, 12, 30])
for count, start, end in zip(counts, edges[:-1], edges[1:]):
    print(f"{start:>2.0f}-{end:<2.0f} yrs: {count}")
```
Output: mean 4.08, median 3.5, middle half 2.0 to 5.6 years (IQR 3.6), skewness 1.08; bands 93, 137, 88, 39, 21, 18, 4. Manager sentence: "Typical tenure is 3.5 years; half of staff are between 2 and 5.6 years; a small tail goes beyond 10 years. Mean (4.1) is pulled up by long-serving staff."
**Likely follow-ups:** 1) *Why median?* Right skew. 2) *Add anything?* A cohort split (by hire year or department).
**Common mistakes:** Reading out only the mean; giving numbers without the shape.

### Q44 ⭐ 🟡 What does a 3-sigma control limit or Six Sigma defect rate mean in terms of the normal distribution?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you link the sigma idea to tail probabilities?
**Say this in the interview:** "Sigma is the standard deviation. A 3-sigma control limit sits 3 SDs from the mean; for a stable normal process only about 0.27% of points fall outside by chance, so a point outside is a signal to investigate. Six Sigma aims for no more than 3.4 defects per million."
**Explain simply:**
- Control chart: a line chart of a process (e.g. daily payroll errors) with an upper and lower limit at mean plus or minus 3 SD.
- Outside the limits: probably a real change, not normal noise.
- Six Sigma: the nearest spec limit is 6 SD from the mean. The industry convention allows the mean to drift by 1.5 SD, so the closest limit is effectively 4.5 SD away, which gives 3.4 per million. Without that drift assumption the rate would be about 0.002 per million.
**Worked example:** 1,000 monthly readings of a stable process: expect about 2.7 beyond the 3-sigma limits by chance.
**Excel / Python:**
```python
from scipy import stats

# Share of a normal process outside plus or minus 3 SD
outside_both_sides = 2 * stats.norm.sf(3)
outside_one_side = stats.norm.sf(3)
print("outside +-3 SD:", round(outside_both_sides, 5), "=", round(outside_both_sides * 1e6), "per million")
print("beyond +3 SD only:", round(outside_one_side * 1e6), "per million")

# Six Sigma: 6 SD limit with the 1.5 SD drift allowance leaves 4.5 SD on one side
six_sigma_defects = stats.norm.sf(4.5) * 1e6
print("Six Sigma defects per million (1.5 shift):", round(six_sigma_defects, 1))
print("Six Sigma, no shift, both sides, per million:", round(2 * stats.norm.sf(6) * 1e6, 4))
print("false alarms per 1000 readings:", round(outside_both_sides * 1000, 1))
```
Output: 0.0027 (2,700 per million); 1,350 per million one side; Six Sigma 3.4 per million; 0.002 per million without the shift; 2.7 false alarms per 1,000. Excel: `=2*(1-NORM.S.DIST(3,TRUE))` (not run in Excel here).
**Likely follow-ups:** 1) *Why is 3.4 not 0.002?* The 1.5 SD drift convention. 2) *Skewed process?* Limits need adjusting.
**Common mistakes:** Quoting 3.4 per million as the plain 6-sigma tail; assuming 3-sigma means "never wrong".

### Q45 ⭐ 🔴 What is the probability that a continuous variable takes exactly one value?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand probability as area under a curve?
**Say this in the interview:** "Zero. For a continuous variable, probability is the area under the density curve over a range, and a single point has no width, so its area is zero. We only ask about intervals, like salary between 49,000 and 51,000."
**Explain simply:**
- Continuous: can take any value in a range, with infinite decimals (exact time, exact weight).
- Zero chance does not mean impossible: some exact value must occur, but no specific one carries measurable probability.
- Real measurements are rounded, so "exactly 50,000" really means a small interval such as 49,999.5 to 50,000.5.
- The height of the density curve is not a probability; it can even exceed 1.
**Worked example:** Salaries normal with mean 50,000 and SD 10,000: the chance of landing near 50,000 shrinks as the window shrinks.
**Excel / Python:**
```python
from scipy import stats

salary_distribution = stats.norm(loc=50000, scale=10000)

# Chance of a salary inside narrower and narrower windows around 50,000
for half_width in [1000, 100, 1, 0.01]:
    upper = salary_distribution.cdf(50000 + half_width)
    lower = salary_distribution.cdf(50000 - half_width)
    print("within +-", half_width, ":", f"{upper - lower:.8f}")
```
Output: 0.07965567, 0.00797871, 0.00007979, 0.00000080. The chance falls towards 0 as the window narrows.
**Likely follow-ups:** 1) *Does this apply to counts?* No, discrete variables can have a chance at exact values. 2) *Does P(X<=50) differ from P(X<50)?* Not for continuous variables.
**Common mistakes:** Saying "impossible"; treating density height as probability.

### Q46 ⭐ 🔴 If two independent normal variables are added, what are the mean and variance of the sum?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know means add, variances add (not SDs), and the sum stays normal?
**Say this in the interview:** "The sum is also normal. Its mean is the sum of the means, and its variance is the sum of the variances, as long as the two are independent. SDs do not add; I take the square root of the total variance."
**Explain simply:**
- Variance: the SD squared; it measures spread.
- Independent: one variable gives no information about the other.
- Subtracting: means subtract, but variances still add, because uncertainty from both pieces piles up.
- If they are not independent, a covariance term is needed.
**Formula in plain words:** Mean of sum = mean A + mean B. Variance of sum = variance A + variance B. SD of sum = square root of that.
**Worked example:** Onboarding task A takes mean 30, SD 4 minutes; task B mean 20, SD 3. Total: mean 50, variance 16 + 9 = 25, SD 5 (not 7). Chance total exceeds 60 minutes = 0.0228.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

random_generator = np.random.default_rng(11)

# Two independent task times in minutes
task_a = random_generator.normal(30, 4, 1000000)
task_b = random_generator.normal(20, 3, 1000000)
total_time = task_a + task_b
time_gap = task_a - task_b

print("sum mean:", round(total_time.mean(), 2), "variance:", round(total_time.var(), 2), "SD:", round(total_time.std(), 2))
print("difference mean:", round(time_gap.mean(), 2), "variance:", round(time_gap.var(), 2), "SD:", round(time_gap.std(), 2))
print("theory: sum variance =", 4**2 + 3**2, "SD =", (4**2 + 3**2) ** 0.5)
print("P(total > 60):", round(stats.norm.sf(60, loc=50, scale=5), 4))
```
Output: simulation matches theory: sum mean 50.0, variance 25.03, SD 5.0; difference mean 10.0 with variance 25.0; P(total > 60) = 0.0228.
**Likely follow-ups:** 1) *And the average of n such values?* Variance of the mean is variance divided by n. 2) *Not independent?* Add 2 x covariance.
**Common mistakes:** Adding SDs (3 + 4 = 7); subtracting variances for differences.

### Q47 ⭐ 🔴 What is Chebyshev's inequality, and when do you use it instead of the empirical rule?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a distribution-free guarantee exists, and that it is cautious?
**Say this in the interview:** "Chebyshev says that for any distribution, at least 1 minus 1 over k squared of the data lies within k SDs of the mean. So at least 75% within 2 SDs and at least 88.9% within 3. I use it when the data is not bell-shaped, accepting that it is a minimum, not a precise value."
**Explain simply:**
- Works for any shape (skewed, bimodal) if mean and SD exist; only a lower bound, so real data is usually much better.
- Only meaningful for k above 1 (at k = 1 it says 0%).
- Empirical rule: precise but requires a normal shape. Chebyshev: safe but loose.
**Formula in plain words:** Share within k SDs is at least 1 - 1/k²; the share outside is at most 1/k².
**Worked example:** Days-to-fill data (skewed, mean 30) checked against the rule (simulated).
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(7)

# Right-skewed days-to-fill data
days_to_fill = random_generator.exponential(scale=30, size=100000)
mean_days = days_to_fill.mean()
sd_days = days_to_fill.std()

normal_shares = {1.5: 0.8664, 2: 0.9545, 3: 0.9973}
for k in [1.5, 2, 3]:
    chebyshev_minimum = 1 - 1 / k**2
    actual_share = np.mean(np.abs(days_to_fill - mean_days) < k * sd_days)
    print(f"k={k}: Chebyshev at least {chebyshev_minimum * 100:.1f}% | actual {actual_share * 100:.1f}% | normal {normal_shares[k] * 100:.1f}%")
```
Output: k=1.5: at least 55.6%, actual 91.7%; k=2: at least 75.0%, actual 95.0%; k=3: at least 88.9%, actual 98.2%. The guarantee holds, but is conservative.
**Likely follow-ups:** 1) *Why not always use it?* It is weak when data is close to normal. 2) *Is it exact for any data?* Yes as a bound; some contrived data hits it exactly.
**Common mistakes:** Reading it as an estimate rather than a floor; using k below 1.

### Q48 ⭐ 🔴 Is high kurtosis the same as a sharply peaked distribution?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know kurtosis measures tail weight and outliers, not just peak shape?
**Say this in the interview:** "Not exactly. Kurtosis mostly reflects how heavy the tails are, meaning how often extreme values occur. A high-kurtosis distribution often looks peaked, but the peak is not what drives the number; a handful of outliers can raise it a lot."
**Explain simply:**
- Excess kurtosis = kurtosis minus 3, so the normal curve scores 0. Positive: heavier tails than normal. Negative: lighter tails.
- It is calculated from fourth powers of deviations, so a single extreme value dominates.
- A flat uniform distribution has no tails at all, and a negative excess kurtosis (-1.2).
- Practical meaning in HR: high kurtosis in salary changes means a few extreme jumps, so treat averages with care.
**Worked example:** Same type of check on four datasets (simulated).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

random_generator = np.random.default_rng(2)

# Bell-shaped scores
normal_scores = random_generator.normal(70, 10, 1000)
print("normal data excess kurtosis:", round(stats.kurtosis(normal_scores), 2))

# Same scores plus 3 extreme values
with_outliers = np.append(normal_scores, [150, 160, 5])
print("after adding 3 extreme values:", round(stats.kurtosis(with_outliers), 2))

# Flat data: no tails
flat_data = random_generator.uniform(0, 100, 100000)
print("uniform:", round(stats.kurtosis(flat_data), 2))

# Heavy-tailed t distribution, 5 degrees of freedom
heavy_tailed = random_generator.standard_t(5, 100000)
print("t, 5 df:", round(stats.kurtosis(heavy_tailed), 2), "(theory 6)")

beyond_3sd = np.abs(heavy_tailed - heavy_tailed.mean()) > 3 * heavy_tailed.std()
print("t5 share beyond 3 SD:", round(np.mean(beyond_3sd) * 100, 2), "%  (normal: about 0.27%)")
```
Output: normal -0.0; with 3 outliers 7.65 (three values out of 1,003 jumped it from 0); uniform -1.2; t5 5.3 (theory 6; sample estimates of heavy tails are unstable); t5 has 1.18% beyond 3 SD versus about 0.27% normal. Excel: `=KURT(range)` returns excess kurtosis.
**Likely follow-ups:** 1) *Why can't you see it from the peak?* Peak height and tail weight can move separately. 2) *What to do?* Look at a box plot or check outliers.
**Common mistakes:** Calling it "peakedness"; forgetting Excel and scipy report excess kurtosis (normal = 0, not 3) by default.

### Q49 ⭐ 🔴 How does the Poisson distribution arise as a limit of the binomial distribution?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand the "many trials, tiny chance" link?
**Say this in the interview:** "If I have a binomial with a very large number of trials n and a very small chance p, with n times p staying fixed at lambda, the binomial probabilities converge to the Poisson with mean lambda. Think of a big workforce where each person has a tiny chance of leaving this month."
**Explain simply:**
- Binomial counts successes in n trials; Poisson counts events with no fixed number of trials.
- Split the month into many tiny slices, each holding an event or not; the more slices, the closer it matches Poisson.
- Rule of thumb: n at least about 100 and p at most about 0.01 (or n x p below about 10).
- Convenient because Poisson needs only one number (lambda).
**Formula in plain words:** Binomial chance of k, C(n,k) p^k (1-p)^(n-k), becomes e^(-λ) λ^k / k! when n gets large, p gets small and λ = n x p.
**Worked example:** 1,000 employees, each with a 0.3% monthly chance to leave, so lambda = 3.
**Excel / Python:**
```python
from scipy import stats

# 1000 employees, 0.3% chance each leaves this month, so mean is 3
number_of_employees = 1000
chance_each_leaves = 0.003
average_leavers = number_of_employees * chance_each_leaves
print("mean:", average_leavers)

print("leavers  binomial  poisson")
for leavers in range(0, 7):
    binomial_chance = stats.binom.pmf(leavers, number_of_employees, chance_each_leaves)
    poisson_chance = stats.poisson.pmf(leavers, average_leavers)
    print(leavers, "      ", f"{binomial_chance:.4f}   {poisson_chance:.4f}")

# Poor match with few trials
print("n=10, p=0.3, k=3 binomial:", round(stats.binom.pmf(3, 10, 0.3), 4), "poisson:", round(stats.poisson.pmf(3, 3), 4))
```
Output: the two columns agree to about 3 decimals (e.g. k=3: 0.2244 vs 0.2240). With only 10 trials the approximation is off (0.2668 vs 0.2240). Excel: `=BINOM.DIST(3,1000,0.003,FALSE)` and `=POISSON.DIST(3,3,FALSE)` (Excel 2010+, not run in Excel here).
**Likely follow-ups:** 1) *Binomial mean and variance versus Poisson?* np and np(1-p) versus lambda and lambda; they match when p is tiny. 2) *Which to use in practice?* Binomial if you know n and p.
**Common mistakes:** Applying it with a large p; forgetting that lambda stays fixed while n grows.

### Q50 ⭐ 🔴 What are heavy-tailed distributions such as the Pareto (80/20), and why do they break the normal-based rules of thumb?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you recognise data where a few values dominate, and know to avoid mean, SD and 3-sigma there?
**Say this in the interview:** "A heavy-tailed distribution has far more extreme values than a normal one. The Pareto is the classic: roughly 80% of the effect comes from 20% of the cases, like revenue from top customers. In that data the mean is dominated by a few giants and SD and 3-sigma rules are misleading, so I use medians, percentiles and log scales."
**Explain simply:**
- Normal tails shrink very fast; heavy tails shrink slowly, so extremes happen regularly.
- Pareto: a power law with shape parameter alpha. About 1.16 gives the 80/20 split; for alpha below 2 the variance is theoretically infinite, so sample SDs keep jumping with each new extreme.
- Consequences: the mean is far above the median, most cases are below the mean, "within 2 SD" covers almost everything yet says nothing, and outlier rules flag the wrong things.
- HR examples: a few employees handle most cases; bonus payouts concentrated in a few leaders.
**Worked example:** Customer revenue drawn from a Pareto with alpha 1.161 (simulated, 200,000 customers).
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(4)

# Shape value that gives the 80/20 rule
alpha = np.log(5) / np.log(4)
print("alpha for 80/20:", round(alpha, 3))

# Revenue per customer (in thousands), Pareto with minimum value 1
revenue = random_generator.pareto(alpha, 200000) + 1

# Share of total revenue from the top 20% of customers
sorted_revenue = np.sort(revenue)[::-1]
top_20_percent_count = int(0.2 * len(sorted_revenue))
top_share = sorted_revenue[:top_20_percent_count].sum() / sorted_revenue.sum()
print("share of revenue from top 20% of customers:", round(top_share * 100, 1), "%")

mean_revenue = revenue.mean()
sd_revenue = revenue.std()
print("mean:", round(mean_revenue, 2), "median:", round(np.median(revenue), 2), "max:", round(revenue.max()))
print("share within mean +- 2 SD:", round(np.mean(np.abs(revenue - mean_revenue) <= 2 * sd_revenue) * 100, 1), "%")
print("share of customers below the mean:", round(np.mean(revenue < mean_revenue) * 100, 1), "%")
```
Output: alpha 1.161; top 20% hold 77.2% of revenue (close to 80; sample noise from extreme draws); mean 6.33 versus median 1.82; the largest customer is 76,444 (about 42,000 times the median of 1.82); 88.3% of customers are below the mean; 99.9% fall within mean +- 2 SD, which sounds safe but hides the tail.
**Likely follow-ups:** 1) *How to summarise?* Median, percentiles, share held by top 10%, log scale. 2) *How to detect?* Log-log plot, or max far above the 99th percentile.
**Common mistakes:** Reporting an average revenue per customer as typical; treating the 80/20 as an exact law (it is a rule of thumb).

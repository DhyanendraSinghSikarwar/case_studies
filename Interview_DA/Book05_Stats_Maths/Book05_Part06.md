# Book 5 — Statistics & Maths for Data Analysts | Part 6: Hypothesis Testing: p-value, t-test, Chi-square, ANOVA, Errors 🟡

**Target:** 70 questions | **Actual:** 74 questions
**Scope:** Interview-style hypothesis testing for 0-3 year analysts: null/alternative, p-value, errors, power, t-test, chi-square, ANOVA, test selection and common misreadings (A/B testing is Part 8).

### Q1 ⭐⭐⭐ 🟢 What is hypothesis testing, in simple words?
**Asked at:** commonly asked (no company-specific report found); the sources list it first in every statistics prep list, and Tiger Analytics is reported (third-party prep sites, unverified) to cover hypothesis testing.
**What the interviewer is checking:** Whether you can explain the idea of "testing a claim with sample data" without jargon.
**Say this in the interview:** "Hypothesis testing is a structured way to check a claim using a sample. I assume the claim 'nothing special is going on' is true, then ask how surprising my sample would be if that were so. If it would be very surprising, I stop believing the claim."
**Explain simply:**
- We rarely see everyone (all employees, all applicants), only a **sample**, so results wobble by luck.
- A hypothesis test asks: is the gap I see real, or could it just be luck of the draw?
- The default claim ("no change, no difference") is the **null hypothesis**. We only drop it when the data clearly disagree.
- The answer is a **p-value**: how surprising the data would be if the default claim were true.
**Worked example:** HR says average engagement score is 65. A survey of 20 employees gives a mean of 67.1. Is 67.1 a real improvement or luck? The test below says the surprise level (p) is 0.065, so the evidence is not strong enough at the usual 5% bar.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Engagement scores from 20 surveyed employees
engagement_scores = np.array([62,70,68,75,58,66,72,64,69,61,73,67,65,71,60,74,63,68,70,66])

# Compare their average against the claimed value of 65
test_result = stats.ttest_1samp(engagement_scores, 65)

print("Sample mean:", engagement_scores.mean())
print("t statistic:", round(test_result.statistic, 3))
print("p-value:", round(test_result.pvalue, 4))
```
Output: `Sample mean: 67.1`, `t statistic: 1.961`, `p-value: 0.0647`. The mean is above 65, but with only 20 people luck could plausibly explain it.
**Likely follow-ups:** 1) *Does it prove anything?* No, it measures evidence, not certainty. 2) *Why start by assuming no difference?* Because it gives a clear, testable baseline.
**Common mistakes:** Treating the test as proof; forgetting that the sample is only a slice of the population.

### Q2 ⭐⭐⭐ 🟢 What are the null hypothesis and the alternative hypothesis? Give an HR example.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you turn a business question into two precise, opposite statements?
**Say this in the interview:** "The null hypothesis, H0, is the 'no effect, no difference' position. The alternative, H1, is what I suspect is true. The test tries to see whether the data give enough evidence to reject H0 in favour of H1."
**Explain simply:**
- H0 always contains an equals idea: no difference, no change, no link.
- H1 is the opposite: there is a difference (two-sided), or it is higher or lower (one-sided).
- We never "prove" H1; we only reject or fail to reject H0.
- Write both as statements about the **population** (all employees), not about the sample.
**Worked example (HR):** Question: "Did the new wellness programme change average monthly sick days?"
- H0: average sick days after the programme = average before (difference is 0).
- H1: the averages are different (difference is not 0).
If the question was "did it reduce sick days?", H1 becomes "average after is lower" (one-sided).
**Likely follow-ups:** 1) *Which one carries the burden of proof?* H1; H0 stays unless the evidence is strong. 2) *Can H0 use a "not equal" sign?* No, H0 holds the equals.
**Common mistakes:** Writing hypotheses about the sample mean (e.g. "sample mean = 65") instead of the population; swapping H0 and H1; choosing H1 after seeing the data.

### Q3 ⭐⭐⭐ 🟢 What is a p-value? Explain it to a non-technical manager.
**Asked at:** commonly asked (no company-specific report found); the Glassdoor snippet in the sources lists p-value with chi-square and Type I/II error (company not stated).
**What the interviewer is checking:** Whether you can define it correctly and avoid the classic wrong definitions.
**Say this in the interview:** "The p-value is the chance of seeing a result at least as extreme as ours if nothing is really going on. A small p-value means our result would be rare under 'no effect', so we doubt 'no effect'. It is not the chance that we are right."
**Explain simply:**
- Imagine the claim "attrition is 15%" is true. Take many random teams of 200. Some will show 20% by luck. How often?
- The p-value is that "how often": the share of lucky-looking outcomes as extreme as ours.
- Small p (like 0.03) means "this would only happen about 3 times in 100 by luck alone".
- It always depends on a starting assumption (H0).
**Worked example:** Claimed attrition is 15%. In our team of 200, 40 left (20%). We simulate 100,000 teams where the true rate is 15%.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

claimed_rate = 0.15
team_size = 200
observed_leavers = 40

# Simulate 100,000 teams of 200 where the true leaving rate is 15%
rng = np.random.default_rng(42)
simulated_leavers = rng.binomial(team_size, claimed_rate, size=100000)

# Share of simulated teams with 40 or more leavers
share_as_extreme = (simulated_leavers >= observed_leavers).mean()

# Exact calculation of the same thing
exact_probability = stats.binom.sf(observed_leavers - 1, team_size, claimed_rate)

print("Simulated:", share_as_extreme)
print("Exact:", round(exact_probability, 4))
```
Output: `Simulated: 0.03347`, `Exact: 0.0335`. Only about 3.4% of lucky teams show 40+ leavers (this is a one-sided p-value; a two-sided test also counts the low end and gives a larger p, about 0.059 with the exact method).
**Likely follow-ups:** 1) *Is p the chance H0 is true?* No (Q10, Q47). 2) *One-sided or two-sided?* Depends on the question (Q16).
**Common mistakes:** Saying "p is the probability the null is true"; forgetting the "if H0 is true" part.

### Q4 ⭐⭐⭐ 🟢 What is the significance level (alpha), and why is 0.05 commonly used?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know alpha is a chosen threshold, not a law of nature?
**Say this in the interview:** "Alpha is the false-alarm rate I accept: the chance of rejecting a true null. I fix it before the test, usually 0.05, and reject H0 if the p-value is below it. 0.05 is a convention, popularised by R. A. Fisher, not a magic number."
**Explain simply:**
- Alpha = 0.05 means: if there is truly no effect, I will wrongly claim one in about 1 test out of 20.
- Pick it **before** looking at data (Q41).
- Stricter (0.01) when a false alarm is costly; looser (0.10) when missing a real effect is costly.
- 0.05 is a compromise that stuck by habit; many fields use other values.
**Worked example:** HR wants to roll out a costly new bonus scheme only if the evidence is strong, so it uses alpha = 0.01. For a cheap pilot reminder email, alpha = 0.10 is acceptable.
**Likely follow-ups:** 1) *Is 0.049 very different from 0.051?* No, the evidence is nearly the same (Q40). 2) *Alpha vs p?* Alpha is your threshold; p comes from the data.
**Common mistakes:** Thinking 0.05 is a rule of nature; changing alpha after seeing p.

### Q5 ⭐⭐⭐ 🟢 What are Type I and Type II errors?
**Asked at:** commonly asked; Type I/II questions appear in several prep sources and an EXL Dataford page, and in the Glassdoor snippet listed in the sources (company not stated).
**What the interviewer is checking:** Can you name both mistakes and give a plain example?
**Say this in the interview:** "Type I is a false alarm: rejecting a null that is actually true. Type II is a miss: failing to reject a null that is actually false. Alpha controls Type I; beta is the chance of Type II."
**Explain simply:**

| | H0 is really true | H0 is really false |
|---|---|---|
| Reject H0 | **Type I error** (false alarm), chance = alpha | Correct (power = 1 - beta) |
| Do not reject H0 | Correct | **Type II error** (miss), chance = beta |

**Worked example (HR):** H0: the new interview process does not change quality of hire.
- Type I: we conclude it improves hiring, but it does not, so we spend money for nothing.
- Type II: it truly helps, but our small sample is inconclusive and we drop a good process.
**Likely follow-ups:** 1) *Can you shrink both?* Yes, with a larger sample. 2) *Which is worse?* Depends on cost (Q17).
**Common mistakes:** Mixing them up; forgetting that Type II depends on sample size and effect size.

### Q6 ⭐⭐⭐ 🟢 If the p-value is 0.03 and alpha is 0.05, what is your conclusion?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic decision rule, stated in plain words and with the right caution.
**Say this in the interview:** "Since 0.03 is below 0.05, I reject the null hypothesis. The result is statistically significant: it would be unusual if there were really no effect. I would also report how big the effect is."
**Explain simply:**
- Rule: p less than or equal to alpha, reject H0; p greater than alpha, fail to reject H0.
- 0.03 means about 3% chance of data this extreme if H0 were true.
- It does not mean H1 is 97% likely true, and it does not say the effect is big.
**Worked example:** Test of "average training hours equals 20" gives p = 0.03. Conclusion: evidence that average training hours differ from 20; then check by how much (e.g. 22 vs 20 hours) to judge if it matters.
**Likely follow-ups:** 1) *What if alpha were 0.01?* Then fail to reject. 2) *Is the effect large?* The p-value cannot tell you (Q9).
**Common mistakes:** Saying "we proved H1"; ignoring the effect size.

### Q7 ⭐⭐⭐ 🟢 What is a t-test and when do you use it?
**Asked at:** commonly asked; a Glassdoor report in the sources lists a Fractal question on t-test versus z-test (title only).
**What the interviewer is checking:** Do you know it compares means and which flavour fits?
**Say this in the interview:** "A t-test checks whether an average differs from a target value or whether two averages differ, when I have a numeric variable and a fairly small sample with the population spread unknown. There are three types: one-sample, two-sample and paired."
**Explain simply:**
- It compares **means** of a numeric measure (salary, score, days).
- t = (difference in means) divided by (typical sampling noise, the standard error). Big t means the gap is large compared with noise.
- Used when the population standard deviation is unknown, which is almost always.
- It needs roughly normal data or a decent sample (Q28).
**Formula in plain words:** one-sample t = (sample mean minus claimed mean) / (sample SD / square root of n).
**Worked example:** Q1 data: mean 67.1, SD 4.79, n = 20, claimed 65. t = 2.1 / (4.79 / 4.472) = 1.961, p = 0.0647. At alpha 0.05, not significant.
**Excel / Python:** Excel 2010+: `=T.TEST(range1, range2, 2, 3)` (two-tailed, unequal variance), not run in Excel here. Python code is in Q1.
**Likely follow-ups:** 1) *Z vs t?* Q21. 2) *More than two groups?* ANOVA (Q18).
**Common mistakes:** Using it for categories (use chi-square); using an independent test on paired data.

### Q8 ⭐⭐⭐ 🟢 What is the chi-square test and when do you use it?
**Asked at:** commonly asked; appears in the Glassdoor snippet in the sources with p-value and Type I/II (company not stated).
**What the interviewer is checking:** Do you know it is for categories and counts, not averages?
**Say this in the interview:** "The chi-square test compares counts. The independence version checks whether two categorical variables are related, for example department and leaving or staying. It compares the counts I see with the counts I would expect if there were no link."
**Explain simply:**
- Variables like department, gender, left/stayed are **categories**.
- Build a table of counts. Work out **expected counts** assuming no relationship.
- Chi-square adds up (observed minus expected) squared, divided by expected, over all cells. Big number means counts are far from "no link".
**Formula in plain words:** chi-square = sum of (observed - expected)^2 / expected.
**Worked example:** Sales: 30 left, 170 stayed. Support: 10 left, 190 stayed. Overall 20% left, so we would expect 20 leavers in each (of 200).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Rows: Sales, Support. Columns: left, stayed
observed_counts = np.array([[30, 170],
                            [10, 190]])

# Run the test without the small-table correction to match the hand formula
result = stats.chi2_contingency(observed_counts, correction=False)

print("Expected counts:", result.expected_freq.tolist())
print("Chi-square:", round(result.statistic, 3))
print("p-value:", round(result.pvalue, 5))
```
Output: `Expected counts: [[20.0, 180.0], [20.0, 180.0]]`, `Chi-square: 11.111`, `p-value: 0.00086`. Attrition is clearly linked with department. (Excel: `=CHISQ.TEST(observed_range, expected_range)`, 2010+, not run in Excel here.)
**Likely follow-ups:** 1) *Does it say which cell differs?* No; compare observed vs expected. 2) *Small counts?* Fisher's exact test (Q56).
**Common mistakes:** Feeding percentages instead of counts; using it for numeric averages.

### Q9 ⭐⭐⭐ 🟢 What is the difference between statistical significance and practical significance?
**Asked at:** commonly asked; a Dataford "significant but not meaningful" page is listed in the sources.
**What the interviewer is checking:** Can you see beyond p less than 0.05 to business value?
**Say this in the interview:** "Statistical significance says the effect is probably not just luck. Practical significance asks whether it is big enough to matter for cost, people and decisions. With a big sample, even a tiny, useless difference can be statistically significant."
**Explain simply:**
- Significance depends on sample size; importance depends on the size of the effect and the context.
- Always report the size of the difference alongside p.
**Worked example:** Two offices, 20,000 employees each (simulated). Average pay differs by about 441 rupees on a salary of about 50,000 (under 1%).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Simulate 20,000 salaries for each office (true means 50,000 and 50,400, SD 10,000)
rng = np.random.default_rng(1)
office_a_salaries = rng.normal(50000, 10000, 20000)
office_b_salaries = rng.normal(50400, 10000, 20000)

# Welch t-test (does not assume equal spread)
test_result = stats.ttest_ind(office_a_salaries, office_b_salaries, equal_var=False)

# Effect size: gap measured in standard deviations (Cohen's d)
average_gap = office_b_salaries.mean() - office_a_salaries.mean()
pooled_spread = np.sqrt((office_a_salaries.var(ddof=1) + office_b_salaries.var(ddof=1)) / 2)

print("Average gap:", round(average_gap, 1))
print("p-value:", test_result.pvalue)
print("Cohen's d:", round(average_gap / pooled_spread, 3))
```
Output: `Average gap: 441.1`, `p-value: 9.075935740608802e-06`, `Cohen's d: 0.044`. Highly significant, yet the gap is under 5% of one standard deviation: almost no practical meaning.
**Likely follow-ups:** 1) *How to judge practical?* Compare with cost, a pre-agreed minimum useful change, effect size (Q44). 2) *Opposite case?* Small sample, big effect, p above 0.05: not significant, but worth more data.
**Common mistakes:** Celebrating p less than 0.05 without checking size; dismissing a large but noisy effect.

### Q10 ⭐⭐⭐ 🟡 What does a p-value NOT tell you? What are the common misinterpretations?
**Asked at:** commonly asked; misreading of p-values is covered by the Statsig and Statology pages listed in the sources (search snippets only).
**What the interviewer is checking:** Whether you know the traps behind the most abused number in statistics.
**Say this in the interview:** "A p-value is not the probability that the null is true, not the probability my result is a fluke, not the size or importance of the effect, and not the chance of repeating the result. It only says how surprising the data are if the null is true."
**Explain simply:**
- Not P(H0 is true). It is P(data this extreme | H0 true), the reverse of what people want.
- Not effect size: tiny effects can have tiny p in big samples.
- Not proof: p = 0.04 is not 96% certainty; p = 0.2 is not proof of no effect.
- Not a pass/fail for truth: 0.049 and 0.051 are nearly the same evidence.
- Not valid after cherry-picking tests (Q42).
**Worked example:** Attrition test gives p = 0.04. Wrong: "96% chance the new policy works." Right: "If the policy had no effect, results like ours would show up about 4% of the time."
**Likely follow-ups:** 1) *What would give P(H0 true)?* A Bayesian analysis (Q67). 2) *Does a small p mean a large effect?* No.
**Common mistakes:** All the above, especially "1 minus p is the chance I'm right".

### Q11 ⭐⭐⭐ 🟡 What does 'fail to reject the null hypothesis' mean, and why do we not say 'accept the null'?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Understanding that "no evidence" is not "evidence of none".
**Say this in the interview:** "Failing to reject means the data were not strong enough to rule out 'no effect'. It does not prove there is no effect; maybe my sample was too small or noisy. So I say 'insufficient evidence', not 'the null is true'."
**Explain simply:**
- Courtroom: "not guilty" does not mean "innocent", only "not proven".
- A small sample has low power (Q26), so real effects can slip through.
- Absence of evidence is not evidence of absence.
**Worked example:** Q1's engagement test gave p = 0.065 with n = 20. We fail to reject "mean = 65". We do not claim the true mean is exactly 65; the 67.1 might be real, and a larger survey could settle it.
**Likely follow-ups:** 1) *How to support "no difference"?* Equivalence tests or a narrow confidence interval around zero (Q65). 2) *What next?* More data.
**Common mistakes:** Writing "the null is accepted/proven" in reports.

### Q12 ⭐⭐⭐ 🟡 What are the steps of a hypothesis test from start to finish?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you run the whole process in order, in plain language?
**Say this in the interview:** "Define the question, state H0 and H1, choose alpha, pick the test and check its assumptions, compute the test statistic and p-value, decide, then explain the result in business terms with the effect size."
**Explain simply:**
1. **Question and hypotheses:** H0: mean engagement = 65; H1: mean is different.
2. **Alpha:** 0.05, set before looking at data.
3. **Choose the test:** numeric average vs a target, so one-sample t-test; check data shape and independence.
4. **Compute:** t = 1.961, p = 0.0647 (Q1 data).
5. **Decide:** p greater than 0.05, so fail to reject H0.
6. **Communicate:** "Average is 67.1, about 2 points above target, but with 20 responses this could be chance; collect more data."
**Likely follow-ups:** 1) *Where does the confidence interval fit?* Alongside step 6. 2) *Where does sample size planning fit?* Before step 1 (Q49).
**Common mistakes:** Picking the test or alpha after seeing the data; stopping at "significant" without a business conclusion.

### Q13 ⭐⭐⭐ 🟡 What is the difference between a one-sample, two-sample and paired t-test?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you match the design of the data to the right t-test?
**Say this in the interview:** "One-sample compares one group's average with a fixed number. Two-sample compares the averages of two separate groups. Paired compares two measurements on the same people, like before and after training, by testing the differences."
**Explain simply:**
- **One-sample:** one group vs a target (mean tenure vs 3 years).
- **Two-sample (independent):** two different groups (Sales vs Support salaries).
- **Paired:** same people twice, or matched pairs. It analyses each person's change, which removes person-to-person variation.
**Worked example:** 10 employees' training scores before and after:
**Excel / Python:**
```python
import numpy as np
from scipy import stats

scores_before = np.array([55,60,48,70,65,52,58,63,67,50])
scores_after = np.array([60,66,50,74,70,55,64,66,72,53])

# Correct for before/after on the same people: paired test
paired_result = stats.ttest_rel(scores_before, scores_after)

# Wrong here: treats the two columns as unrelated groups
independent_result = stats.ttest_ind(scores_before, scores_after)

print("Average improvement:", (scores_after - scores_before).mean())
print("Paired p-value:", round(paired_result.pvalue, 6))
print("Independent p-value:", round(independent_result.pvalue, 4))
```
Output: `Average improvement: 4.2`, `Paired p-value: 5e-06`, `Independent p-value: 0.2488`. Everyone improved a little; the paired test sees that, while the independent test drowns it in person-to-person differences. (Excel: `=T.TEST(before, after, 2, 1)`; type 1 = paired, 2 = equal variance, 3 = unequal variance.)
**Likely follow-ups:** 1) *Do paired groups need equal size?* Yes, pairs must match. 2) *Assumption for paired?* Differences roughly normal (Q28).
**Common mistakes:** Running an independent test on paired data (loses power, as above).

### Q14 ⭐⭐⭐ 🟡 Which test would you use to compare the average salary of two departments, and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Test selection logic, plus awareness of skew and unequal spread.
**Say this in the interview:** "Salary is numeric and the two departments are separate groups, so a two-sample (independent) t-test, preferably Welch's version because spreads usually differ. If salaries are heavily skewed with outliers, I would check the shape or use Mann-Whitney."
**Explain simply:**
- Numeric outcome + two independent groups = two-sample t-test.
- Welch's version does not require equal variances, so it is the safe default.
- Check for outliers and skew first (Q63).
**Worked example:** Monthly salary (thousand rupees) for 12 people in each department.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

sales_salaries = np.array([45,52,48,60,55,47,58,50,62,53,49,57])
support_salaries = np.array([38,42,40,45,39,44,41,47,36,43,40,46])

# Welch t-test: two separate groups, spreads may differ
test_result = stats.ttest_ind(sales_salaries, support_salaries, equal_var=False)

print("Sales mean:", sales_salaries.mean())
print("Support mean:", support_salaries.mean())
print("t:", round(test_result.statistic, 3))
print("p-value:", test_result.pvalue)
```
Output: `Sales mean: 53.0`, `Support mean: 41.75`, `t: 6.091`, `p-value: 8.661868427845476e-06`. Sales earns about 11,250 more on average; the gap is unlikely to be luck.
**Likely follow-ups:** 1) *Three or more departments?* ANOVA (Q18). 2) *Skewed salaries?* Mann-Whitney (Q54).
**Common mistakes:** Using a paired test; using chi-square on salaries; ignoring outliers (a few executives can distort the mean).

### Q15 ⭐⭐⭐ 🟡 Which test would you use to check whether attrition is related to department, and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you pick chi-square for two categorical variables?
**Say this in the interview:** "Both attrition (left or stayed) and department are categories, so I use the chi-square test of independence on the table of counts. If counts in some cells are very small, I switch to Fisher's exact test."
**Explain simply:**
- Build a department-by-outcome table of counts.
- H0: attrition is independent of department; H1: they are related.
- Significant result says "related", but not which department is the problem; compare observed vs expected per cell.
**Worked example:** Q8 table: Sales 30 of 200 left (15%), Support 10 of 200 (5%). Chi-square = 11.11, p = 0.00086, so attrition is related to department. Excel: `=CHISQ.TEST(observed_range, expected_range)` (2010+, not run in Excel here); code in Q8.
**Likely follow-ups:** 1) *Strength of link?* Cramer's V. 2) *Cause?* Association is not causation.
**Common mistakes:** Using a t-test on 0/1 data; using percentages instead of counts; reading "related" as "department causes attrition".

### Q16 ⭐⭐⭐ 🟡 What is the difference between a one-tailed and a two-tailed test?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know when direction matters and how it changes p?
**Say this in the interview:** "A two-tailed test asks 'is it different?' and looks at both directions. A one-tailed test asks 'is it higher' (or lower) and looks at one direction only. I default to two-tailed unless I decided on a single direction before seeing the data and a change the other way would not matter."
**Explain simply:**
- Two-tailed: H1 is "not equal"; rejection area split across both ends of the curve.
- One-tailed: H1 is "greater than" or "less than"; all the rejection area is on one end.
- For the same data, the one-tailed p is half the two-tailed p, if the result lies in the predicted direction.
- Switching to one-tailed to get under 0.05 is cheating.
**Worked example:** Q1 data, H1: mean engagement is greater than 65.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

engagement_scores = np.array([62,70,68,75,58,66,72,64,69,61,73,67,65,71,60,74,63,68,70,66])

# Two-sided: is the average different from 65?
two_sided = stats.ttest_1samp(engagement_scores, 65, alternative='two-sided')

# One-sided: is the average greater than 65?
one_sided = stats.ttest_1samp(engagement_scores, 65, alternative='greater')

print("Two-tailed p:", round(two_sided.pvalue, 4))
print("One-tailed p:", round(one_sided.pvalue, 4))
```
Output: `Two-tailed p: 0.0647`, `One-tailed p: 0.0324`. Same data, different question; the one-tailed answer would be "significant", which is why the direction must be fixed in advance. (Excel `T.TEST` tails argument: 1 or 2.)
**Likely follow-ups:** 1) *When is one-tailed fair?* Pre-registered direction with no interest in the other side. 2) *Link to CI?* Two-tailed matches a two-sided interval (Q64).
**Common mistakes:** Choosing the tail after seeing the data.

### Q17 ⭐⭐⭐ 🟡 Which is worse, a Type I or a Type II error? Give a business example for each.
**Asked at:** commonly asked; business-example framing appears on the PracHub, Prepfully and Dataford EXL pages in the sources.
**What the interviewer is checking:** Can you reason about costs of mistakes instead of reciting a rule?
**Say this in the interview:** "Neither is always worse; it depends on which mistake costs more. I decide that with the business before the test, then set alpha and sample size to match."
**Explain simply:**
- **Type I (false alarm):** acting on an effect that is not real. Costly when the action is expensive or hard to reverse.
- **Type II (miss):** ignoring a real effect. Costly when the opportunity or risk is large.
- To cut both, get more data.
**Worked example (HR):**
- Type I costly: company rolls out a company-wide Rs 5 crore retention bonus because a noisy test said it lowers attrition, but it does not. Use a strict alpha like 0.01.
- Type II costly: a screening test truly catches burnout early, but the pilot is too small to show it, and burnout-driven resignations continue. Use a larger sample and accept alpha 0.05 or 0.10.
**Likely follow-ups:** 1) *Which does alpha control?* Type I only. 2) *How to lower Type II?* Larger sample, bigger effect, lower noise, higher alpha.
**Common mistakes:** Saying "Type I is always worse".

### Q18 ⭐⭐⭐ 🟡 What is ANOVA and why not run many t-tests instead?
**Asked at:** commonly asked; the "why ANOVA not pairwise t-tests" follow-up appears in the DataCamp course page listed in the sources.
**What the interviewer is checking:** Do you understand ANOVA as one overall test and the multiple-comparison danger?
**Say this in the interview:** "ANOVA tests whether three or more group means are all equal using a single test. Running many t-tests instead inflates the chance of a false alarm, because every extra test is another chance to get lucky."
**Explain simply:**
- One-way ANOVA: H0 all group means equal; H1 at least one differs.
- F-statistic = variation between group means / variation within groups. A large F means groups differ more than random noise.
- Three groups need 3 pairwise t-tests; at alpha 0.05, the overall false-alarm chance is about 1 - 0.95^3 = 14.3%. With 5 groups (10 tests) it is about 40%.
**Worked example:** Engagement scores for low, mid and high-tenure staff.
**Excel / Python:**
```python
from scipy import stats

low_tenure_scores = [50,52,48,55,53,49]
mid_tenure_scores = [54,58,56,60,57,55]
high_tenure_scores = [59,62,64,61,66,63]

# One-way ANOVA across the three groups
anova_result = stats.f_oneway(low_tenure_scores, mid_tenure_scores, high_tenure_scores)

# Chance of at least one false alarm with 3 tests and 10 tests at alpha 0.05
false_alarm_three_tests = 1 - 0.95 ** 3
false_alarm_ten_tests = 1 - 0.95 ** 10

print("F:", round(anova_result.statistic, 2))
print("p-value:", anova_result.pvalue)
print("3 tests:", round(false_alarm_three_tests, 3))
print("10 tests:", round(false_alarm_ten_tests, 3))
```
Output: `F: 32.98`, `p-value: 3.2287550303309574e-06`, `3 tests: 0.143`, `10 tests: 0.401`. At least one group differs; a post-hoc test (Q36) says which. (The 14.3% and 40% assume independent tests; pairwise tests overlap, so treat them as a guide.)
**Likely follow-ups:** 1) *Significant ANOVA, then what?* Tukey post-hoc (Q36). 2) *Only two groups?* ANOVA equals a t-test.
**Common mistakes:** Running repeated t-tests; thinking a significant F says which group differs.

### Q19 ⭐⭐⭐ 🟡 How does sample size affect the p-value and the conclusion of a test?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know bigger samples make small differences detectable, and what that means for interpretation?
**Say this in the interview:** "A larger sample reduces random noise, so the same difference gives a bigger test statistic and a smaller p-value. With a small sample, a real effect may not reach significance; with a huge sample, trivial effects will. So I always look at effect size too."
**Explain simply:**
- Noise (standard error) shrinks with the square root of n.
- Same average gap, more people: more convincing.
- Small n: low power, risk of a Type II error. Huge n: significant but maybe meaningless (Q50).
**Worked example:** The same 0.5-point gap in engagement scores (SD 5), two groups of equal size:
**Excel / Python:**
```python
import numpy as np
from scipy import stats

average_gap = 0.5
standard_deviation = 5

for people_per_group in [20, 100, 500, 2000]:
    # Standard error of the difference between two group means
    standard_error = np.sqrt(2 * standard_deviation**2 / people_per_group)
    t_statistic = average_gap / standard_error
    p_value = 2 * (1 - stats.t.cdf(t_statistic, 2 * people_per_group - 2))
    print(people_per_group, round(t_statistic, 2), round(p_value, 4))
```
Output: `20 0.32 0.7536`, `100 0.71 0.4803`, `500 1.58 0.1141`, `2000 3.16 0.0016`. The gap never changed; only n did.
**Likely follow-ups:** 1) *How to plan n?* Power analysis (Q49). 2) *Does a large n fix bias?* No.
**Common mistakes:** Thinking significance proves importance; running a tiny pilot and concluding "no effect".

### Q20 ⭐⭐ 🟢 What is a test statistic?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand that a test turns your sample into one number you can judge against chance.
**Say this in the interview:** "A test statistic is a single number that measures how far my sample result is from what the null hypothesis claims, counted in units of normal sampling noise. The bigger it is, the harder the result is to blame on luck."
**Explain simply:**
- The **null hypothesis** is the "nothing is going on" claim (for example, average absence is 2 days).
- The test statistic is the gap between what you saw and that claim, divided by the **standard error** (the typical wobble of a sample average from sample to sample).
- Different tests have different statistics: z, t, chi-square, F. All do the same job: shrink the data into one number, then convert it to a p-value.
- Rough rule: a t or z far beyond about 2 (either direction) is unusual if the null is true.
**Formula in plain words:** (what you observed minus what the null claims) divided by the standard error. In symbols: t = (x̄ − μ₀) / (s / √n).
**Worked example:** HR claims average absence is 2.0 days. A sample of 36 employees shows an average of 2.5 days with SD 1.2. The standard error is 1.2 / 6 = 0.2, so the test statistic is 0.5 / 0.2 = 2.5: the sample is 2.5 standard errors above the claim.
**Excel / Python:**
```python
import math

# Sample facts: 36 employees, average 2.5 absence days, SD 1.2 days
sample_size = 36
sample_mean_absence = 2.5
sample_sd_absence = 1.2
claimed_mean_absence = 2.0

# Standard error: how much a sample average typically wobbles
standard_error = sample_sd_absence / math.sqrt(sample_size)

# Test statistic: gap from the claim, measured in standard errors
test_statistic = (sample_mean_absence - claimed_mean_absence) / standard_error

print("Standard error:", round(standard_error, 3))
print("Test statistic (t):", round(test_statistic, 3))
```
Output:
```
Standard error: 0.2
Test statistic (t): 2.5
```
The sample average sits 2.5 standard errors above the claim, which is quite far.
**Likely follow-ups:**
- *What do you do with it next?* Convert it to a p-value, or compare it with a critical value (Q22).
- *Is a bigger statistic always better?* It means stronger evidence against the null, not a bigger real-world effect.
**Common mistakes:** Treating the test statistic as the p-value; forgetting that it depends on sample size (the same gap gives a bigger statistic with more data).

### Q21 ⭐⭐ 🟢 What is the difference between a z-test and a t-test?
**Asked at:** A Glassdoor candidate report lists "explain the difference between t-test and z-test" for Fractal (seen as a snippet title only, not read in full); otherwise commonly asked.
**What the interviewer is checking:** Whether you know when you may use the population SD and why small samples need the t distribution.
**Say this in the interview:** "A z-test is used when the population standard deviation is known or the sample is very large. A t-test is used when I only have the sample's SD, which is almost always the case in real HR data. The t distribution has fatter tails to allow for that extra uncertainty, and it becomes the same as z as the sample grows."
**Explain simply:**
- **z-test:** uses the normal curve; needs a known population SD (rare), or is used as an approximation for proportions and very large samples.
- **t-test:** uses the t distribution, which depends on **degrees of freedom** (Q23, roughly sample size minus 1).
- With small samples the t cut-off is bigger, so you need stronger evidence before claiming a difference.
- With around 100+ observations the two give nearly identical answers.
**Formula in plain words:** Both are (sample mean minus claimed mean) divided by standard error. z uses the true population SD; t uses the sample SD.
**Worked example:** For a two-sided 5% test the z cut-off is always 1.96, but the t cut-off shrinks towards it as n grows.
**Excel / Python:**
```python
from scipy import stats

# Cut-off for a two-sided 5% test: z is fixed, t depends on sample size
z_cutoff = stats.norm.ppf(0.975)
print("z cut-off:", round(z_cutoff, 3))

for sample_size in [5, 10, 30, 100, 1000]:
    degrees_of_freedom = sample_size - 1
    t_cutoff = stats.t.ppf(0.975, degrees_of_freedom)
    print("n =", sample_size, " t cut-off:", round(t_cutoff, 3))
```
Output:
```
z cut-off: 1.96
n = 5  t cut-off: 2.776
n = 10  t cut-off: 2.262
n = 30  t cut-off: 2.045
n = 100  t cut-off: 1.984
n = 1000  t cut-off: 1.962
```
With 5 people you need a gap of 2.78 standard errors; with 1000 people almost the same as z (1.96).
**Likely follow-ups:**
- *Which would you use for a proportion?* A z-test (Q30), because the SD is determined by the proportion itself.
- *Does t need normal data?* Roughly normal data for small samples; the central limit theorem helps for large ones.
**Common mistakes:** Saying "z for large samples, t for small" without mentioning the known-SD condition; using z just because n is above 30 when the SD is estimated (t is still technically correct).

### Q22 ⭐⭐ 🟢 What is a critical value and what is the rejection region?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can make a test decision without a p-value, and link it to alpha.
**Say this in the interview:** "The critical value is the cut-off on the test statistic. If my statistic goes beyond it, it lands in the rejection region, the zone of results so extreme that I would reject the null. The cut-off is chosen so that the null would only land there alpha percent of the time by chance."
**Explain simply:**
- Pick **alpha** (for example 5%) first.
- The critical value marks the edge of the extreme zone on the test statistic's curve.
- Two-tailed test: alpha is split, 2.5% in each tail, so there are two cut-offs (plus and minus).
- One-tailed test: all 5% sits in one tail, so the cut-off is closer to zero (Q16).
- Decision: statistic inside the rejection region means reject the null; otherwise fail to reject. This gives the same decision as comparing p-value with alpha.
**Formula in plain words:** The critical value is the point on the curve that leaves alpha of the area in the tail(s). Reject if |t| is greater than the critical value (two-tailed).
**Worked example:** 36 employees means 35 degrees of freedom. The observed t from Q20 is 2.5.
**Excel / Python:**
```python
from scipy import stats

alpha = 0.05
degrees_of_freedom = 35   # 36 employees minus 1
observed_t = 2.5

# Two-tailed: split alpha into 2.5% in each tail
critical_value_two_tailed = stats.t.ppf(1 - alpha / 2, degrees_of_freedom)

# One-tailed (testing "higher" only): all 5% in the right tail
critical_value_one_tailed = stats.t.ppf(1 - alpha, degrees_of_freedom)

print("Two-tailed critical value: +/-", round(critical_value_two_tailed, 3))
print("One-tailed critical value:", round(critical_value_one_tailed, 3))

# Decision: is the observed t inside the rejection region?
if abs(observed_t) > critical_value_two_tailed:
    print("t = 2.5 is in the rejection region: reject the null")
else:
    print("t = 2.5 is not in the rejection region: fail to reject")
```
Output:
```
Two-tailed critical value: +/- 2.03
One-tailed critical value: 1.69
t = 2.5 is in the rejection region: reject the null
```
Excel (2010+; not run in Excel here): `=T.INV.2T(0.05, 35)` returns 2.03, the same cut-off.
**Likely follow-ups:**
- *Critical value or p-value, which is better?* Same decision; p-value also shows how strong the evidence is.
- *What changes the critical value?* Alpha, one or two tails, and degrees of freedom.
**Common mistakes:** Using the two-tailed cut-off for a one-tailed question (or the reverse); thinking the rejection region is where the null is "true".

### Q23 ⭐⭐ 🟢 What are degrees of freedom?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can explain a notoriously confusing idea without just saying "n minus 1".
**Say this in the interview:** "Degrees of freedom are the number of values in your data that are genuinely free to vary once you have fixed the things you already estimated from the data, like the mean. With five values and a fixed average, only four can be chosen freely; the fifth is forced."
**Explain simply:**
- If five employees must average 4 years of tenure and you pick four of the tenures, the fifth is locked in.
- Every quantity you estimate from the data (such as the mean) uses up one degree of freedom.
- It tunes the t, chi-square and F distributions: fewer degrees of freedom means fatter tails and a stricter cut-off.
- It is also why the sample SD divides by n minus 1 instead of n.
- Common cases: one-sample t has n − 1; pooled two-sample t has n₁ + n₂ − 2; chi-square test of independence has (rows − 1) × (columns − 1); one-way ANOVA has (groups − 1) and (total − groups).
**Formula in plain words:** degrees of freedom = number of data points minus number of things estimated from them.
**Worked example:** Tenure for five people: 2, 3, 4, 5, 6 (average 4).
**Excel / Python:**
```python
import numpy as np

# Five employees' tenure in years; their average is 4
tenure_years = np.array([2, 3, 4, 5, 6])
average_tenure = tenure_years.mean()

# Gaps from the average always add up to zero, so the last gap is not free
gaps_from_average = tenure_years - average_tenure
print("Average:", average_tenure)
print("Gaps:", gaps_from_average)
print("Sum of gaps:", gaps_from_average.sum())

# Spread uses n - 1 (ddof=1) because only 4 gaps are free to vary
sd_dividing_by_n = tenure_years.std(ddof=0)
sd_dividing_by_n_minus_1 = tenure_years.std(ddof=1)
print("SD dividing by n:", round(sd_dividing_by_n, 3))
print("SD dividing by n-1:", round(sd_dividing_by_n_minus_1, 3))
```
Output:
```
Average: 4.0
Gaps: [-2. -1.  0.  1.  2.]
Sum of gaps: 0.0
SD dividing by n: 1.414
SD dividing by n-1: 1.581
```
The gaps must sum to zero, so once four are known the fifth is fixed. Dividing by n − 1 gives a slightly larger SD, correcting for this.
**Likely follow-ups:**
- *Why n minus 1 for the SD?* The sample mean is closer to the sample points than the true mean would be, so dividing by n would understate the spread.
- *Degrees of freedom for a 3x4 chi-square table?* (3 − 1) × (4 − 1) = 6.
**Common mistakes:** Memorising "n − 1" with no reason; using n instead of n − 1 for the sample SD.

### Q24 ⭐⭐ 🟢 How are alpha and the probability of a Type I error related?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you see alpha as a risk you choose, not a result you calculate.
**Say this in the interview:** "Alpha is the Type I error rate I am willing to accept: the chance of rejecting a null hypothesis that is actually true. If I set alpha at 5% and the null is true, I will wrongly raise a false alarm in about 1 test out of 20."
**Explain simply:**
- **Type I error:** a false alarm, rejecting the null when it is true (Q5).
- Alpha is set **before** the test; it is the upper limit on that risk.
- It only applies when the null is true; it says nothing about how often you are right when there really is an effect.
- Lowering alpha means fewer false alarms but more missed real effects (Type II errors).
**Formula in plain words:** alpha = probability of rejecting the null, given that the null is true.
**Worked example:** Simulate 10,000 samples of 25 employees from a company whose true average tenure is exactly 3.0 years (so the null "average = 3.0" is true), and test each at alpha 0.05.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

np.random.seed(42)
alpha = 0.05
number_of_simulations = 10000
false_alarms = 0

# Make the null TRUE: true average tenure really is 3.0 years
for simulation in range(number_of_simulations):
    sample_of_tenures = np.random.normal(loc=3.0, scale=1.5, size=25)
    test_result = stats.ttest_1samp(sample_of_tenures, popmean=3.0)
    if test_result.pvalue < alpha:
        false_alarms = false_alarms + 1

print("Share of false alarms:", false_alarms / number_of_simulations)
```
Output:
```
Share of false alarms: 0.0528
```
About 5% of tests cried wolf even though nothing was going on, which is exactly what alpha = 0.05 promises (the small gap from 0.05 is simulation noise).
**Likely follow-ups:**
- *Is alpha the probability my result is wrong?* No; it is the false-alarm rate across tests when the null is true (Q47).
- *What if I run many tests?* The overall false-alarm chance grows (Q45).
**Common mistakes:** Treating alpha as the p-value; picking alpha after seeing the data.

### Q25 ⭐⭐ 🟢 What is a confidence interval and how does it relate to a hypothesis test?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can connect interval and test, and interpret an interval correctly.
**Say this in the interview:** "A confidence interval is a range of plausible values for the true number, built so that the method captures the truth 95% of the time. It matches a two-sided test: if the claimed value falls outside the 95% interval, the test at 5% rejects it; if inside, it does not."
**Explain simply:**
- A single sample average is a guess; the interval shows how precise that guess is.
- Correct reading: "if I repeated this study many times, about 95% of such intervals would contain the true value." Casually, "plausible range for the true value".
- Wrong reading: "there is a 95% chance the true value is in this one interval".
- Wider interval means less precision (small sample, high variation).
- Bonus over a p-value: it shows the size of the effect, not just yes or no.
**Formula in plain words:** sample estimate plus or minus (critical value times standard error). In symbols: x̄ ± t × s / √n.
**Worked example:** 25 employees, average tenure 3.4 years, SD 1.5; the claimed average is 3.0.
**Excel / Python:**
```python
import math
from scipy import stats

sample_size = 25
sample_mean = 3.4
sample_sd = 1.5
claimed_mean = 3.0
degrees_of_freedom = sample_size - 1

# Standard error and the 95% multiplier from the t table
standard_error = sample_sd / math.sqrt(sample_size)
t_multiplier = stats.t.ppf(0.975, degrees_of_freedom)

# Interval = average +/- multiplier x standard error
margin_of_error = t_multiplier * standard_error
lower_limit = sample_mean - margin_of_error
upper_limit = sample_mean + margin_of_error

print("95% CI:", round(lower_limit, 2), "to", round(upper_limit, 2))
print("Claimed mean inside interval?", lower_limit <= claimed_mean <= upper_limit)
```
Output:
```
95% CI: 2.78 to 4.02
Claimed mean inside interval? True
```
3.0 is inside the interval, so we cannot reject a true average of 3.0 at 5%, matching the t-test in Q29 (p = 0.195).
**Likely follow-ups:**
- *Does a 99% interval come out wider?* Yes; more confidence needs a wider net.
- *Why prefer the interval?* It shows the plausible size of the difference, not just significant or not.
**Common mistakes:** Saying "95% probability the true mean is in this interval"; confusing the interval for individual values (it is about the mean, not about where 95% of employees lie).

### Q26 ⭐⭐ 🟡 What is statistical power, and what affects it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand that a non-significant result can simply mean the study was too small.
**Say this in the interview:** "Power is the chance that a test detects a real effect when one exists. It is 1 minus beta, and 80% is the usual target. It goes up with a larger sample, a bigger true effect, lower variation, and a higher alpha."
**Explain simply:**
- Think of a smoke alarm: power is the chance it rings when there really is a fire.
- Low power means real differences are often missed (Type II error).
- Four levers: **sample size** (more data), **effect size** (bigger real gap is easier to see), **variability** (noisy data hides gaps), **alpha** (a looser alpha detects more but allows more false alarms).
- You usually fix alpha at 0.05 and the target power at 0.80, then solve for the sample size you need (Q49).
**Formula in plain words:** power = probability of rejecting the null when the alternative is true = 1 − beta.
**Worked example:** Comparing two groups with a t-test at alpha 0.05, effect size Cohen's d (gap measured in SDs): small 0.2, medium 0.5, large 0.8.
**Excel / Python:**
```python
from statsmodels.stats.power import TTestIndPower

power_calculator = TTestIndPower()

# Power of a two-group t-test; effect_size is Cohen's d (gap in SD units)
for effect_size in [0.2, 0.5, 0.8]:
    for group_size in [20, 64, 200]:
        power = power_calculator.power(effect_size=effect_size, nobs1=group_size, alpha=0.05)
        print("effect", effect_size, " n per group", group_size, " power", round(power, 2))
```
Output:
```
effect 0.2  n per group 20  power 0.09
effect 0.2  n per group 64  power 0.2
effect 0.2  n per group 200  power 0.51
effect 0.5  n per group 20  power 0.34
effect 0.5  n per group 64  power 0.8
effect 0.5  n per group 200  power 1.0
effect 0.8  n per group 20  power 0.69
effect 0.8  n per group 64  power 0.99
effect 0.8  n per group 200  power 1.0
```
A medium effect (0.5) needs about 64 people per group to reach 80% power; with 20 per group you would catch it only 34% of the time.
**Likely follow-ups:**
- *Why does a small study often give "not significant"?* Low power, not necessarily no effect.
- *Can power be too high?* With huge samples even trivial effects become significant (Q50).
**Common mistakes:** Calling power the probability the null is false; calculating power after the fact from the observed result.

### Q27 ⭐⭐ 🟡 What is the relationship between alpha, beta and power?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand the trade-off between the two error types.
**Say this in the interview:** "Alpha is the false-alarm rate, beta is the missed-effect rate, and power is 1 minus beta. For a fixed sample size they trade off: making alpha stricter lowers false alarms but raises beta and lowers power. The only way to improve both at once is more data."
**Explain simply:**
- Alpha = P(Type I error); beta = P(Type II error); power = 1 − beta.
- They are not simple mirror images of each other: alpha and beta are about two different situations (null true versus null false).
- Tighten the rule for rejecting (smaller alpha) and you reject less often, including when you should have.
- Break the trade-off with larger samples or less noisy data.
**Formula in plain words:** power = 1 − beta; for fixed data, smaller alpha leads to larger beta.
**Worked example:** Fixed design: 50 people per group, medium effect (d = 0.5), changing only alpha.
**Excel / Python:**
```python
from statsmodels.stats.power import TTestIndPower

power_calculator = TTestIndPower()

# Same data situation, only alpha changes
for alpha in [0.10, 0.05, 0.01]:
    power = power_calculator.power(effect_size=0.5, nobs1=50, alpha=alpha)
    beta = 1 - power
    print("alpha", alpha, " power", round(power, 3), " beta", round(beta, 3))
```
Output:
```
alpha 0.1  power 0.799  beta 0.201
alpha 0.05  power 0.697  beta 0.303
alpha 0.01  power 0.453  beta 0.547
```
Going from alpha 0.10 to 0.01 cuts false alarms but drops power from 80% to 45%.
**Likely follow-ups:**
- *Which do you set first?* Alpha and target power; sample size comes out of them.
- *If both errors matter?* Increase the sample size.
**Common mistakes:** Saying beta = 1 − alpha (false); thinking lower alpha is always better.

### Q28 ⭐⭐ 🟡 What are the assumptions of the t-test?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know when the test can be trusted and how to check it.
**Say this in the interview:** "The t-test assumes independent observations, data that is roughly normal (or a large enough sample), no extreme outliers, and for the classic two-sample version, similar spread in both groups. If the spreads differ I use Welch's t-test, and if the data is badly skewed with a small sample I use a rank-based test."
**Explain simply:**
- **Independence:** one employee's value must not influence another's (the same person counted twice breaks it; before/after on the same person needs the paired test, Q37).
- **Normality:** the sample averages should be roughly bell-shaped; matters mainly for small samples (under about 30) because of the central limit theorem.
- **No extreme outliers:** one CEO salary can swamp an average.
- **Equal variance** (two-sample only): Welch's t-test removes this need.
- Data should be numeric on an interval scale (a real average makes sense).
**Formula in plain words:** Not a formula question; the checks are Shapiro-Wilk (normality), Levene (equal spread), and plots.
**Worked example:** Made-up monthly salaries (in thousands) for 30 employees in Sales and 30 in Finance.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

np.random.seed(7)
# Made-up monthly salaries (in thousands) for two departments
sales_salaries = np.random.normal(loc=52, scale=6, size=30)
finance_salaries = np.random.normal(loc=56, scale=6, size=30)

# Check 1: roughly normal? (p above 0.05 means no clear sign of trouble)
print("Shapiro Sales p:", round(stats.shapiro(sales_salaries).pvalue, 3))
print("Shapiro Finance p:", round(stats.shapiro(finance_salaries).pvalue, 3))

# Check 2: similar spread in both groups?
print("Levene p:", round(stats.levene(sales_salaries, finance_salaries).pvalue, 3))

# Run the test; equal_var=False is the safe Welch version
result = stats.ttest_ind(sales_salaries, finance_salaries, equal_var=False)
print("Welch t:", round(result.statistic, 3), " p:", round(result.pvalue, 4))
```
Output:
```
Shapiro Sales p: 0.666
Shapiro Finance p: 0.817
Levene p: 0.383
Welch t: -2.639  p: 0.0107
```
Both checks pass (p above 0.05), so the test is trustworthy; the department averages differ significantly.
**Likely follow-ups:**
- *What if data is skewed?* Large samples are fine; small ones, use Mann-Whitney (Q54) or a transformation.
- *Do you test assumptions with p-values only?* No, also plot a histogram; formal tests are too sensitive with big samples.
**Common mistakes:** Ignoring independence (the most damaging assumption); believing the raw data must be perfectly normal for any n.

### Q29 ⭐⭐ 🟡 Calculate a one-sample t-statistic: a sample of 25 employees has mean tenure 3.4 years and SD 1.5 years; the claimed mean is 3.0. What is t and is it significant at 5%?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can do the arithmetic by hand and reach a decision.
**Say this in the interview:** "The standard error is 1.5 over the square root of 25, which is 0.3. So t is 0.4 divided by 0.3, about 1.33. With 24 degrees of freedom the 5% two-sided cut-off is about 2.06, so it is not significant; the p-value is roughly 0.19."
**Explain simply:**
- Hypotheses: H0 mean tenure = 3.0; H1 mean tenure is not 3.0 (two-sided).
- Step 1: standard error = s / √n = 1.5 / 5 = 0.3.
- Step 2: t = (3.4 − 3.0) / 0.3 = 1.333.
- Step 3: degrees of freedom = 25 − 1 = 24; critical value 2.064.
- Step 4: 1.333 is smaller than 2.064, so fail to reject. The 0.4-year gap is within normal sampling wobble.
**Formula in plain words:** t = (sample mean − claimed mean) / (SD / √n).
**Worked example:** As above; p-value is about 0.19, so there is roughly a 19% chance of a gap this big or bigger if the true average is 3.0.
**Excel / Python:**
```python
import math
from scipy import stats

sample_size = 25
sample_mean = 3.4
sample_sd = 1.5
claimed_mean = 3.0
alpha = 0.05
degrees_of_freedom = sample_size - 1

# Standard error = SD / square root of n
standard_error = sample_sd / math.sqrt(sample_size)

# t = (sample mean - claimed mean) / standard error
t_statistic = (sample_mean - claimed_mean) / standard_error

# Two-sided p-value and critical value
p_value = 2 * stats.t.sf(abs(t_statistic), degrees_of_freedom)
critical_value = stats.t.ppf(1 - alpha / 2, degrees_of_freedom)

print("Standard error:", round(standard_error, 3))
print("t:", round(t_statistic, 3))
print("Critical value:", round(critical_value, 3))
print("p-value:", round(p_value, 4))
```
Output:
```
Standard error: 0.3
t: 1.333
Critical value: 2.064
p-value: 0.1949
```
t is below the cut-off and p is above 0.05, so not significant. Excel (2010+; not run in Excel here): with t in cell B1, `=T.DIST.2T(ABS(B1), 24)` returns 0.1949 and `=T.INV.2T(0.05, 24)` returns 2.064.
**Likely follow-ups:**
- *Would a one-sided test change it?* p would be about 0.097, still above 0.05.
- *What would make it significant?* More data or a bigger gap (about 0.62 years with the same SD and n).
**Common mistakes:** Using 1.96 (z) instead of 2.064 (t); dividing by n instead of √n; saying "accept H0" instead of "fail to reject" (Q11).

### Q30 ⭐⭐ 🟡 Calculate a z-test for proportions: 120 of 400 employees say they would leave; the claimed rate is 25%. What is z and what do you conclude?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you use the claimed rate in the standard error and give a clear business conclusion.
**Say this in the interview:** "The observed rate is 30%. The standard error under the claim is the square root of 0.25 times 0.75 over 400, about 0.0217. So z is 0.05 divided by 0.0217, about 2.31, and the two-sided p-value is about 0.021. At 5% I reject the claim: the data suggests intent to leave is higher than 25%."
**Explain simply:**
- H0: true rate = 0.25; H1: true rate is not 0.25.
- The standard error uses the **claimed** 25% because we assume H0 is true while testing.
- Condition check: 400 × 0.25 = 100 and 400 × 0.75 = 300, both well above 10, so the normal approximation is fine.
- Business reading: the 5-point gap is unlikely to be luck. This is about stated intent, not actual exits.
**Formula in plain words:** z = (observed proportion − claimed proportion) / √(claimed × (1 − claimed) / n).
**Worked example:** 120/400 = 30%.
**Excel / Python:**
```python
import math
from scipy import stats

employees_surveyed = 400
would_leave = 120
claimed_rate = 0.25

# Observed share who would leave
observed_rate = would_leave / employees_surveyed

# Standard error uses the CLAIMED rate, because the null is assumed true
standard_error = math.sqrt(claimed_rate * (1 - claimed_rate) / employees_surveyed)

# z = (observed - claimed) / standard error
z_statistic = (observed_rate - claimed_rate) / standard_error

# Two-sided p-value from the normal curve
p_value = 2 * stats.norm.sf(abs(z_statistic))

print("Observed rate:", observed_rate)
print("Standard error:", round(standard_error, 4))
print("z:", round(z_statistic, 3))
print("p-value:", round(p_value, 4))
```
Output:
```
Observed rate: 0.3
Standard error: 0.0217
z: 2.309
p-value: 0.0209
```
z of 2.31 passes the 1.96 cut-off, and p is below 0.05, so reject. Excel (2010+; not run in Excel here): with z in B1, `=2*(1-NORM.S.DIST(ABS(B1), TRUE))` returns 0.0209.
**Likely follow-ups:**
- *One-sided?* If you only test "higher than 25%", p is about 0.010 (set the direction before looking).
- *Confidence interval?* It would be about 25.5% to 34.5%, which excludes 25% (this CI uses the observed rate in the standard error).
**Common mistakes:** Using the observed 30% in the standard error for the test (that is for the CI); forgetting the sample-size condition; reading "would leave" as actual attrition.

### Q31 ⭐⭐ 🟡 How do you calculate and interpret the chi-square statistic for a 2x2 table of gender versus promotion?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand expected counts and can interpret a non-significant result honestly.
**Say this in the interview:** "I compare what I observed in each cell with what I would expect if gender and promotion were unrelated. For each cell I take observed minus expected, square it, divide by expected, and add them all up. A big total means the pattern is unlikely under independence. With 1 degree of freedom, a statistic above 3.84 is significant at 5%."
**Explain simply:**
- H0: gender and promotion are independent (promotion rate is the same for both). H1: they are related.
- Expected count for a cell = (row total × column total) / grand total.
- Observed (men 30 promoted, 170 not; women 20 promoted, 180 not): 50 promoted of 400 overall, so we expect 25 promoted in each gender group.
- Chi-square = sum of (O − E)² / E = 1 + 1 + 0.143 + 0.143 = 2.286; df = (2 − 1)(2 − 1) = 1; p = 0.131.
- Conclusion: promotion rates of 15% (men) and 10% (women) look different, but with 200 per group the gap could be chance. Not significant; it does not prove fairness either.
**Formula in plain words:** add up (observed − expected)² / expected over all cells. In symbols: χ² = Σ (O − E)² / E.
**Worked example:** The table above.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Rows: men, women. Columns: promoted, not promoted
observed_counts = np.array([[30, 170],
                            [20, 180]])

# Plain chi-square (no continuity correction) and the corrected version
plain = stats.chi2_contingency(observed_counts, correction=False)
corrected = stats.chi2_contingency(observed_counts, correction=True)

print("Expected counts if gender and promotion are unrelated:")
print(plain.expected_freq)
print("Chi-square:", round(plain.statistic, 3), " df:", plain.dof, " p:", round(plain.pvalue, 4))
print("With Yates correction: chi-square", round(corrected.statistic, 3), " p:", round(corrected.pvalue, 4))
```
Output:
```
Expected counts if gender and promotion are unrelated:
[[ 25. 175.]
 [ 25. 175.]]
Chi-square: 2.286  df: 1  p: 0.1306
With Yates correction: chi-square 1.851  p: 0.1736
```
Not significant either way. Excel (2010+; not run in Excel here): put observed counts in A1:B2 and expected counts in D1:E2, then `=CHISQ.TEST(A1:B2, D1:E2)` returns 0.1306 (no continuity correction).
**Likely follow-ups:**
- *What is the Yates correction?* A small adjustment for 2x2 tables that makes the test slightly more cautious.
- *Which group drives the result?* Look at observed versus expected per cell.
**Common mistakes:** Using percentages instead of counts; concluding "no discrimination" from a non-significant result (low power, Q26); mixing up row and column totals when computing expected counts.

### Q32 ⭐⭐ 🟡 What are the assumptions of the chi-square test of independence?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the expected-count rule and the independence-of-observations rule.
**Say this in the interview:** "Both variables must be categorical, observations must be independent (each employee appears once), categories must not overlap, the data must be raw counts, and the expected count in each cell should be at least 5. If expected counts are too small, I use Fisher's exact test or merge categories."
**Explain simply:**
- **Counts, not percentages or averages.**
- **Independent observations:** one row per employee; repeated measures on the same person break it.
- **Mutually exclusive categories:** each person lands in exactly one cell.
- **Expected counts at least 5** (a common rule of thumb; some use "at least 80% of cells with 5 or more, none below 1").
- Random or representative sample. Note: it is the expected counts that matter, not the observed ones.
**Formula in plain words:** Expected count = row total × column total / grand total. Check that every expected count is at least 5.
**Worked example:** A small company: 20 employees, only 4 promoted.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# A small table: 20 employees, only 4 promoted
observed_counts = np.array([[3, 7],
                            [1, 9]])

result = stats.chi2_contingency(observed_counts)
print("Expected counts:")
print(result.expected_freq)
print("Smallest expected count:", result.expected_freq.min())

# Expected counts below 5, so use Fisher's exact test instead
fisher_result = stats.fisher_exact(observed_counts)
print("Fisher exact p-value:", round(fisher_result.pvalue, 4))
```
Output:
```
Expected counts:
[[2. 8.]
 [2. 8.]]
Smallest expected count: 2.0
Fisher exact p-value: 0.582
```
Expected counts of 2 break the rule, so chi-square is unreliable here and Fisher's exact test is the right tool (Q56).
**Likely follow-ups:**
- *Does the test show causation?* No, only association.
- *Large samples?* Then everything tiny becomes significant; check effect size (Q44).
**Common mistakes:** Checking observed rather than expected counts; running it on percentages; counting the same employee in multiple rows.

### Q33 ⭐⭐ 🟡 What is the chi-square goodness-of-fit test? Give an example with attendance by weekday.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can test one categorical variable against an expected pattern.
**Say this in the interview:** "Goodness-of-fit checks whether the counts in one categorical variable match a pattern I expected, such as 'absences are spread equally across weekdays'. I compare observed counts with expected counts using the chi-square statistic, with categories minus 1 degrees of freedom."
**Explain simply:**
- One variable (weekday), several categories; independence tests use two variables.
- H0: the counts follow the expected distribution (here: equal across 5 days). H1: they do not.
- Expected = total × the expected share for that category.
- df = number of categories − 1 = 4.
- Worked result: Monday has 38 absences against 26 expected, but overall p = 0.065, so we cannot claim a weekday pattern at 5%. This is a borderline signal worth tracking for another quarter.
**Formula in plain words:** χ² = Σ (observed − expected)² / expected, over the weekdays.
**Worked example:** 130 absences in a quarter: Mon 38, Tue 22, Wed 20, Thu 21, Fri 29.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Absences recorded on each weekday over a quarter
observed_absences = np.array([38, 22, 20, 21, 29])

# If absences were spread evenly, each day would get the same count
total_absences = observed_absences.sum()
expected_absences = np.full(5, total_absences / 5)

result = stats.chisquare(f_obs=observed_absences, f_exp=expected_absences)

print("Total absences:", total_absences)
print("Expected per day:", expected_absences[0])
print("Chi-square:", round(result.statistic, 3), " df: 4", " p:", round(result.pvalue, 4))
```
Output:
```
Total absences: 130
Expected per day: 26.0
Chi-square: 8.846  df: 4  p: 0.0651
```
The Monday spike looks big, but the test says it is within what chance could produce at the 5% level. Excel (2010+; not run in Excel here): `=CHISQ.TEST(observed_range, expected_range)` returns 0.0651.
**Likely follow-ups:**
- *Expected shares not equal?* Use your own shares, for example 25% Monday if five-day staffing differs.
- *How does it differ from the independence test?* One variable versus a pattern, not two variables versus each other (Q57).
**Common mistakes:** Using percentages instead of counts; wrong degrees of freedom; assuming "equal" is the only possible null.

### Q34 ⭐⭐ 🟡 What are the null and alternative hypotheses in one-way ANOVA, and how do you read the F-statistic?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can state the hypotheses correctly and explain F as a ratio.
**Say this in the interview:** "The null says all group means are equal; the alternative says at least one group mean is different, not that all are different. F is the variation between group averages divided by the variation within groups. If F is much bigger than 1, the groups differ more than ordinary individual variation would explain."
**Explain simply:**
- H0: μ_A = μ_B = μ_C. H1: at least one mean differs.
- **Between-group variation:** how far the team averages sit from the overall average.
- **Within-group variation:** how much people differ inside their own team (the noise).
- F near 1 means the team differences are no bigger than noise; large F means real differences. The p-value comes from the F distribution.
- ANOVA only says "somewhere there is a difference"; follow-up tests find where (Q36).
**Formula in plain words:** F = (between-group variance) / (within-group variance), each being a sum of squares divided by its degrees of freedom.
**Worked example:** Engagement scores (out of 10), 6 employees in each of 3 teams.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Engagement scores (out of 10) for 6 employees in each of three teams
team_a = np.array([6, 7, 6, 8, 7, 6])
team_b = np.array([7, 8, 8, 9, 7, 8])
team_c = np.array([5, 6, 5, 6, 7, 5])
all_teams = [team_a, team_b, team_c]

all_scores = np.concatenate(all_teams)
grand_mean = all_scores.mean()

# Between-group variation: how far each team average is from the grand mean
between_sum_squares = sum(len(team) * (team.mean() - grand_mean) ** 2 for team in all_teams)
# Within-group variation: spread of people around their own team average
within_sum_squares = sum(((team - team.mean()) ** 2).sum() for team in all_teams)

df_between = len(all_teams) - 1
df_within = len(all_scores) - len(all_teams)

# F = between mean square / within mean square
f_by_hand = (between_sum_squares / df_between) / (within_sum_squares / df_within)

# Same answer from scipy, plus the p-value
scipy_result = stats.f_oneway(team_a, team_b, team_c)

print("Team averages:", team_a.mean().round(2), team_b.mean().round(2), team_c.mean().round(2))
print("F by hand:", round(f_by_hand, 3))
print("F from scipy:", round(scipy_result.statistic, 3), " p:", round(scipy_result.pvalue, 4))
```
Output:
```
Team averages: 6.67 7.83 5.67
F by hand: 11.14
F from scipy: 11.14  p: 0.0011
```
F = 11.1 with p = 0.001 means the team averages (6.7, 7.8, 5.7) differ by more than chance would explain. Excel: Data tab, Data Analysis (ToolPak), "Anova: Single Factor" (not run in Excel here).
**Likely follow-ups:**
- *Can F be negative?* No; it is a ratio of variances, so zero or higher.
- *Which team differs?* Post-hoc test (Q36).
**Common mistakes:** Writing H1 as "all means differ"; reading a significant F as "every pair differs"; ignoring that it compares means, not spread.

### Q35 ⭐⭐ 🟡 What are the assumptions of ANOVA?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can list the assumptions, check them, and say what to do if they fail.
**Say this in the interview:** "Observations are independent, the data within each group is roughly normal, and the groups have similar variance. ANOVA is fairly robust to mild departures when group sizes are equal. If variances differ I use Welch's ANOVA, and if the data is clearly non-normal I use the Kruskal-Wallis test."
**Explain simply:**
- **Independence:** each person appears once, in one group.
- **Normality** of the values (really, of the leftovers after removing each group's average) in every group.
- **Homogeneity of variance:** similar spread across groups; check with Levene's test.
- Numeric outcome, categorical grouping.
- Balanced group sizes make ANOVA more forgiving.
**Formula in plain words:** Not a formula question; use Levene (spread), Shapiro-Wilk or a Q-Q plot (normality).
**Worked example:** The engagement scores from Q34. Scores are whole numbers from a rating scale, so the Shapiro test is picky here.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

team_a = np.array([6, 7, 6, 8, 7, 6])
team_b = np.array([7, 8, 8, 9, 7, 8])
team_c = np.array([5, 6, 5, 6, 7, 5])

# Equal spread check (p above 0.05 means no clear problem)
print("Levene p:", round(stats.levene(team_a, team_b, team_c).pvalue, 3))

# Normality check on the leftovers after removing each team average
leftovers = np.concatenate([team_a - team_a.mean(),
                            team_b - team_b.mean(),
                            team_c - team_c.mean()])
print("Shapiro p on leftovers:", round(stats.shapiro(leftovers).pvalue, 3))

# Fallback if assumptions fail: rank-based Kruskal-Wallis
print("Kruskal-Wallis p:", round(stats.kruskal(team_a, team_b, team_c).pvalue, 4))
```
Output:
```
Levene p: 0.772
Shapiro p on leftovers: 0.008
Kruskal-Wallis p: 0.0059
```
Spread is fine. The Shapiro test flags non-normality, which is common with whole-number ratings and tiny groups, so I would look at a plot too. The rank-based Kruskal-Wallis reaches the same conclusion (significant), so the finding does not depend on the assumption.
**Likely follow-ups:**
- *What if variances differ?* Welch's ANOVA.
- *Does the outcome variable need to be normal overall?* No, within groups (or residuals).
**Common mistakes:** Testing normality on the pooled data instead of per group or residuals; forgetting independence; over-trusting Shapiro with huge samples.

### Q36 ⭐⭐ 🟡 If ANOVA is significant, how do you find which groups differ?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know about post-hoc tests and multiple-comparison control.
**Say this in the interview:** "A significant ANOVA only says at least one mean differs. I follow with a post-hoc test such as Tukey's HSD, which compares every pair while keeping the overall false-alarm rate at 5%. If I use plain pairwise t-tests instead, I adjust the threshold, for example with Bonferroni."
**Explain simply:**
- Only run post-hoc tests after a significant overall F.
- **Tukey HSD:** all pairwise comparisons, controls the family-wide error rate (the standard choice).
- **Bonferroni:** divide alpha by the number of comparisons (0.05 / 3 = 0.0167 for three pairs); simple but conservative.
- Report the differences and their confidence intervals, not just the p-values.
**Formula in plain words:** Compare each pair of group means, but judge each pair against a stricter cut-off than 5% so the overall error stays at 5%.
**Worked example:** The three teams from Q34.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

team_a = np.array([6, 7, 6, 8, 7, 6])
team_b = np.array([7, 8, 8, 9, 7, 8])
team_c = np.array([5, 6, 5, 6, 7, 5])

# Tukey's test compares every pair and controls the overall error rate
tukey_result = stats.tukey_hsd(team_a, team_b, team_c)
pair_names = [("A", "B", 0, 1), ("A", "C", 0, 2), ("B", "C", 1, 2)]

for name_one, name_two, i, j in pair_names:
    print("Team", name_one, "vs", name_two, " p:", round(tukey_result.pvalue[i][j], 4))
```
Output:
```
Team A vs B  p: 0.0558
Team A vs C  p: 0.108
Team B vs C  p: 0.0008
```
Only Team B versus Team C is clearly different; the gap between B and A is borderline. Excel has no built-in Tukey; the ToolPak gives only the overall ANOVA.
**Likely follow-ups:**
- *Why not just run three t-tests?* The error rate inflates (Q18, Q39).
- *Tukey versus Bonferroni?* Tukey is less conservative for all pairs.
**Common mistakes:** Running post-hoc tests when ANOVA was not significant; ignoring the adjustment.

### Q37 ⭐⭐ 🟡 When would you use a paired t-test? Give an example such as training scores before and after.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can spot paired data and explain why pairing helps.
**Say this in the interview:** "I use a paired t-test when the two sets of measurements come from the same people, or from naturally matched pairs, such as scores before and after training. It works on each person's difference, which removes the person-to-person variation and makes it much more sensitive."
**Explain simply:**
- Paired situations: before/after on the same employees, two ratings of the same person, matched pairs.
- H0: the average difference is zero. H1: it is not.
- It is just a one-sample t-test on the differences.
- Assumptions: differences are roughly normal; pairs are independent of each other.
**Formula in plain words:** t = (average difference) / (SD of differences / √n).
**Worked example:** 10 employees take an assessment before and after training. Average improvement 4.4 points.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Same 10 employees tested before and after a training programme
scores_before = np.array([62, 55, 70, 48, 66, 59, 73, 51, 64, 58])
scores_after = np.array([68, 57, 74, 55, 65, 66, 78, 56, 70, 61])

# Improvement for each person
improvements = scores_after - scores_before
print("Average improvement:", improvements.mean())

# Paired t-test works on the improvements
paired_result = stats.ttest_rel(scores_after, scores_before)
print("Paired t:", round(paired_result.statistic, 3), " p:", round(paired_result.pvalue, 4))

# Wrong choice for comparison: treating them as two separate groups
independent_result = stats.ttest_ind(scores_after, scores_before)
print("Independent t:", round(independent_result.statistic, 3), " p:", round(independent_result.pvalue, 4))
```
Output:
```
Average improvement: 4.4
Paired t: 5.558  p: 0.0004
Independent t: 1.246  p: 0.2288
```
The paired test sees that nearly everyone improved (p = 0.0004). The wrong independent test misses it (p = 0.23) because person-to-person differences drown the signal. Excel (2010+; not run in Excel here): `=T.TEST(after_range, before_range, 2, 1)` (type 1 = paired) returns the same p-value as Python.
**Likely follow-ups:**
- *Limitation of a before/after design?* No control group, so other changes over time could explain the gain.
- *Non-normal differences?* Wilcoxon signed-rank test.
**Common mistakes:** Using the independent test on paired data (loses power); using the paired test on unrelated groups of equal size.

### Q38 ⭐⭐ 🟡 How do you decide which statistical test to use for a given problem?
**Asked at:** commonly asked (no company-specific report found); the PracHub "choose and explain a classical hypothesis test" listing in the sources file covers this theme (snippet-level only).
**What the interviewer is checking:** Whether you reason from the data type and the design, not from memory.
**Say this in the interview:** "I ask three questions. What type is my outcome: a number or a category? How many groups am I comparing? Are the groups independent or the same people measured twice? Then I check assumptions and fall back to a non-parametric test if they fail."
**Explain simply:**
- Step 1: outcome type (numeric average, or categories and proportions).
- Step 2: number of groups and whether they are paired.
- Step 3: sample size and assumption checks (normality, equal spread, expected counts).
- Step 4: name the hypotheses first, then the test.

| Question (HR example) | Outcome | Groups | Test |
|---|---|---|---|
| Is average tenure different from the claimed 3.0? | number | 1 vs a value | one-sample t-test |
| Salary in two departments | number | 2 independent | two-sample t-test (Welch) |
| Scores before and after training | number | 2 paired | paired t-test |
| Engagement across 3+ teams | number | 3+ independent | one-way ANOVA |
| Is the leaving rate different from 25%? | proportion | 1 vs a value | z-test for one proportion |
| Acceptance rates of two recruiters | proportion | 2 independent | two-proportion z-test or chi-square |
| Attrition versus department | category | 2 categorical variables | chi-square test of independence |
| Absences spread across weekdays | category | 1 variable vs a pattern | chi-square goodness-of-fit |
| Skewed salaries, small sample | number | 2 or 3+ | Mann-Whitney or Kruskal-Wallis |
| Small counts in a 2x2 | category | 2 | Fisher's exact test |

**Worked example:** "Does attrition differ across 4 departments?" The outcome is a category (left or stayed), the groups are independent, so chi-square test of independence. "Is the salary of men and women different?" Number, 2 independent groups: Welch t-test.
**Likely follow-ups:**
- *What if normality fails?* Non-parametric alternative (Q53).
- *Two numeric variables?* That is correlation or regression, not these tests.
**Common mistakes:** Picking a test by name recognition; running a t-test on categories or chi-square on averages; skipping the paired versus independent question.

### Q39 ⭐⭐ 🟡 What is the multiple comparisons problem, and how do you handle it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that running many tests produces false alarms, and that you can correct for it?
**Say this in the interview:** "Every test carries a 5% chance of a false alarm, so if I run many tests, some will look significant by luck. I handle it by limiting the number of tests, naming my main question in advance, and adjusting the p-values with Bonferroni, Holm or a false-discovery-rate method."
**Explain simply:**
- Alpha (0.05) is the false-alarm rate for one test. Run 10 tests with no real effect anywhere and the chance of at least one "significant" result is about 40%.
- This happens when you compare many metrics, many departments, or many sub-groups.
- Fixes: decide the main metric beforehand; use Bonferroni (divide alpha by the number of tests), Holm (a slightly sharper version), or Benjamini-Hochberg (controls the share of false discoveries, not the chance of any).
- Report how many tests you ran, so readers can judge.
**Formula in plain words:** Chance of at least one false alarm = 1 minus (1 minus alpha) raised to the number of tests. Bonferroni: new alpha = alpha divided by the number of tests.
**Worked example:** HR compares two sites on 8 metrics (attrition, absence, engagement and so on). Five p-values are below 0.05. After correction only the smallest one (0.003) survives.
**Excel / Python:**
```python
from statsmodels.stats.multitest import multipletests

# p-values from 8 different HR metrics compared between two sites
p_values = [0.003, 0.012, 0.020, 0.041, 0.049, 0.30, 0.55, 0.80]

# Bonferroni: multiply each p-value by the number of tests (cap at 1)
bonferroni_flags, bonferroni_p, _, _ = multipletests(p_values, alpha=0.05, method="bonferroni")

# Holm: a step-down method that is never weaker than Bonferroni
holm_flags, holm_p, _, _ = multipletests(p_values, alpha=0.05, method="holm")

print("Significant before correction:", sum(p < 0.05 for p in p_values))
print("Significant after Bonferroni :", bonferroni_flags.sum(), [round(float(p), 3) for p in bonferroni_p])
print("Significant after Holm       :", holm_flags.sum(), [round(float(p), 3) for p in holm_p])
```
Output: `Significant before correction: 5`, `Significant after Bonferroni : 1 [0.024, 0.096, 0.16, 0.328, 0.392, 1.0, 1.0, 1.0]`, `Significant after Holm : 1 [0.024, 0.084, 0.12, 0.205, 0.205, 0.9, 1.0, 1.0]`. Five "wins" shrink to one once we admit we ran eight tests.
**Likely follow-ups:** 1) *Is Bonferroni too strict?* It can miss real effects when there are many tests; Holm or FDR are less strict. 2) *When is correction not needed?* One pre-planned main test.
**Common mistakes:** Testing many things and reporting only the significant ones; applying no correction; correcting after choosing which tests to report.

### Q40 ⭐⭐ 🟡 Your p-value is 0.051. Do you reject the null hypothesis? How do you explain this to a manager?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you treat 0.05 as a guide and not a magic cliff, while still following the rule you set?
**Say this in the interview:** "By the rule I set, alpha 0.05, I do not reject the null at 0.051. But 0.051 and 0.049 are practically the same evidence, so I would show the manager the size of the difference and its confidence interval and say the result is borderline, not 'no effect'."
**Explain simply:**
- Null hypothesis: the "nothing is going on" assumption. Alpha: the cut-off you pick before testing.
- Rule followed: p above alpha means "not enough evidence to reject", not "proven no difference".
- Do not move alpha after seeing the result; that is cheating the test.
- Useful advice for a manager: the estimate, the interval, and what more data could do.
**Worked example:** New onboarding: 81 of 400 hires left in 90 days under the old process (20.25%) and 60 of 400 under the new (15%). The p-value is 0.0513. The 95% interval for the drop is -0.02 to 10.5 percentage points: mostly positive, just touching zero.
**Excel / Python:**
```python
from statsmodels.stats.proportion import proportions_ztest
import numpy as np

# 90-day leavers out of 400 hires in each group
leavers = np.array([81, 60])
hires = np.array([400, 400])

# Two-proportion z-test (is the leaving rate different?)
z_statistic, p_value = proportions_ztest(leavers, hires)

rate_old = leavers[0] / hires[0]
rate_new = leavers[1] / hires[1]
difference = rate_old - rate_new

# 95% confidence interval for the difference (unpooled standard error)
standard_error = np.sqrt(rate_old*(1-rate_old)/hires[0] + rate_new*(1-rate_new)/hires[1])
lower = difference - 1.96 * standard_error
upper = difference + 1.96 * standard_error

print("rates:", rate_old, rate_new)
print("p-value:", round(p_value, 4))
print("difference:", round(difference, 4), "95% CI:", round(lower, 4), round(upper, 4))
```
Output: `rates: 0.2025 0.15`, `p-value: 0.0513`, `difference: 0.0525 95% CI: -0.0002 0.1052`. The interval only just includes zero, which is why the p-value sits just above 0.05.
**Likely follow-ups:** 1) *Would you collect more data?* Yes, if planned properly and not by testing repeatedly until significant. 2) *Would you call it 'trending'?* Better to say "borderline, evidence is suggestive but not conclusive".
**Common mistakes:** Rounding 0.051 down to 0.05; saying "almost significant" without numbers; changing alpha to 0.10 after the fact.

### Q41 ⭐⭐ 🟡 Why should we state the hypotheses and alpha before looking at the data?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that test results are only trustworthy if the question is fixed before the answer is seen?
**Say this in the interview:** "If I pick the hypothesis or alpha after seeing the data, I can steer the test towards the result I like. The 5% false-alarm promise only holds if the question and the cut-off were fixed first."
**Explain simply:**
- Hypothesis: the claim being tested. Alpha: the false-alarm rate you accept.
- Looking first lets you pick the direction (higher, lower, different), the group, or the metric that happens to look best.
- A test chosen after the data was seen is really many tests in disguise, so the real false-alarm rate is much higher than 5%.
- Good habit: write the plan (metric, groups, test, alpha, sample size) in a short note before pulling the data.
**Worked example:** An HR analyst sees that attrition fell more for women than men and then tests only women. She has implicitly run two tests (men and women) but reports one; her real false-alarm chance is nearer 10% than 5%. Pre-stating "overall attrition, all hires" avoids this.
**Likely follow-ups:** 1) *Is exploring data wrong?* No; explore freely, but treat findings as ideas to confirm on new data. 2) *What is pre-registration?* Writing the plan down publicly before the study.
**Common mistakes:** Choosing a one-sided test after seeing which way the data points; adjusting alpha to fit the p-value; presenting exploration as confirmation.

### Q42 ⭐⭐ 🟡 What is p-hacking and how can an analyst avoid it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you spot and avoid fishing for significance?
**Say this in the interview:** "P-hacking means trying many tests, groups, metrics or data cuts until something gives p below 0.05, then reporting only that. I avoid it by fixing the plan in advance, reporting every test I ran, correcting for multiple tests, and confirming surprises on fresh data."
**Explain simply:**
- Each extra try is another lottery ticket for a false alarm.
- Common forms: dropping "outliers" until the result works, testing many sub-groups, stopping data collection the moment p dips below 0.05, switching metrics.
- Defences: pre-plan, correct for multiple tests (Q39), report effect size and interval, hold out data for confirmation, be open about everything tried.
**Worked example:** Simulation: two groups with no real difference, and the analyst checks 20 metrics. The best-looking metric reaches p below 0.05 in about 65% of such experiments.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

random_generator = np.random.default_rng(seed=1)
number_of_experiments = 2000
metrics_per_experiment = 20
experiments_with_a_false_win = 0

for experiment in range(number_of_experiments):
    # Two groups with NO real difference, 20 different metrics measured
    smallest_p_value = 1.0
    for metric in range(metrics_per_experiment):
        group_a = random_generator.normal(50, 10, 40)
        group_b = random_generator.normal(50, 10, 40)
        p_value = stats.ttest_ind(group_a, group_b).pvalue
        smallest_p_value = min(smallest_p_value, p_value)
    # Analyst reports only the best-looking metric
    if smallest_p_value < 0.05:
        experiments_with_a_false_win += 1

print("Share of no-effect experiments with at least one 'significant' metric:",
      experiments_with_a_false_win / number_of_experiments)
```
Output: `0.6515`. Theory says 1 - 0.95^20 = 0.64; the simulation agrees. Fishing turns a 5% risk into about 65%.
**Likely follow-ups:** 1) *Is peeking at results every day p-hacking?* Yes, unless the test is designed for repeated looks. 2) *Is removing outliers p-hacking?* Only if decided after seeing the effect on the p-value; set the rule beforehand.
**Common mistakes:** Believing p-hacking needs bad intent (it often happens innocently); reporting only the winning test.

### Q43 ⭐⭐ 🟡 What is the Central Limit Theorem and why does it matter for hypothesis tests?
**Asked at:** commonly asked (no company-specific report found); the sources list CLT as a common basic question.
**What the interviewer is checking:** Do you know why we can use bell-curve-based tests even on messy data?
**Say this in the interview:** "The Central Limit Theorem says that the average of a reasonably large random sample behaves like a bell curve around the true average, even if the raw data is skewed. That is why t-tests and z-tests work for means with decent sample sizes."
**Explain simply:**
- Sample mean: the average of the people you sampled. Different samples give slightly different means.
- Those means cluster around the true mean, and their spread (the standard error) is the data's standard deviation divided by the square root of the sample size.
- Rule of thumb: about 30 or more observations is often enough; very skewed data needs more.
- It lets us say how unusual our sample average is, which is the core of a test.
**Formula in plain words:** Standard error = standard deviation divided by the square root of sample size. SE = s / √n.
**Worked example:** Salaries (in thousands) are skewed: mean 45.5, SD 42.6. Taking 5,000 samples of 50 employees, the sample means have SD 6.16, close to the predicted 42.6 / √50 = 6.02.
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(seed=7)

# A skewed 'salary' population: many modest salaries, a few very high ones (in thousands of rupees)
population_salaries = random_generator.lognormal(mean=3.5, sigma=0.8, size=100000)
print("Population mean:", round(population_salaries.mean(), 2), " SD:", round(population_salaries.std(), 2))

# Draw 5000 random samples of 50 employees and record each sample's mean
sample_means = []
for draw in range(5000):
    sample = random_generator.choice(population_salaries, size=50)
    sample_means.append(sample.mean())
sample_means = np.array(sample_means)

print("Mean of sample means:", round(sample_means.mean(), 2))
print("SD of sample means  :", round(sample_means.std(), 2))
print("Predicted SD (population SD / sqrt(50)):", round(population_salaries.std() / np.sqrt(50), 2))
```
Output: `Population mean: 45.47  SD: 42.6`, `Mean of sample means: 45.47`, `SD of sample means  : 6.16`, `Predicted SD: 6.02`. Averages are far tighter than individual salaries.
**Likely follow-ups:** 1) *Does CLT make the data normal?* No, only the sample mean. 2) *Does it hold for tiny samples?* Not reliably; with n of 10 and skewed data, use a non-parametric or bootstrap method.
**Common mistakes:** Saying "the data becomes normal"; applying it to medians or maxima without care; ignoring that outliers slow the effect.

### Q44 ⭐⭐ 🟡 What is effect size, and why report it along with the p-value?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you separate "is it real" from "does it matter"?
**Say this in the interview:** "The p-value says whether a difference is likely real; effect size says how big it is. With a huge sample even a trivial difference gets a tiny p-value, so I always report both."
**Explain simply:**
- Effect size: the size of the difference, either in real units (3 points of engagement, 6 percentage points of attrition) or standardised.
- Cohen's d: difference in means divided by the standard deviation. Rough guide: 0.2 small, 0.5 medium, 0.8 large.
- The p-value depends on sample size; effect size does not.
- Managers act on size, so effect size is the headline.
**Formula in plain words:** Cohen's d = (mean of group 2 minus mean of group 1) divided by the pooled standard deviation.
**Worked example:** Small study, 40 per group: engagement rises 6 points, d = 0.36, p = 0.115 (not significant, but not small). Huge study, 20,000 per group: gap is 0.5 points, d = 0.045, p = 8e-06 (significant, but trivial).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Engagement scores (0-100) before and after a new manager programme
random_generator = np.random.default_rng(seed=3)
small_sample_before = random_generator.normal(70, 12, 40)
small_sample_after = random_generator.normal(76, 12, 40)

def cohens_d(first_group, second_group):
    # Difference in means divided by the pooled standard deviation
    n1, n2 = len(first_group), len(second_group)
    pooled_variance = ((n1-1)*first_group.var(ddof=1) + (n2-1)*second_group.var(ddof=1)) / (n1+n2-2)
    return (second_group.mean() - first_group.mean()) / np.sqrt(pooled_variance)

print("Small study: p =", round(stats.ttest_ind(small_sample_after, small_sample_before).pvalue, 4),
      " d =", round(cohens_d(small_sample_before, small_sample_after), 2))

# Huge study with a tiny real gap of 0.5 points
big_before = random_generator.normal(70, 12, 20000)
big_after = random_generator.normal(70.5, 12, 20000)
print("Huge study : p =", round(stats.ttest_ind(big_after, big_before).pvalue, 6),
      " d =", round(cohens_d(big_before, big_after), 3))
```
Output: `Small study: p = 0.1154  d = 0.36`, `Huge study : p = 8e-06  d = 0.045`. The small study has the bigger effect but the weaker p-value. (Random data with a fixed seed; your numbers shift with another seed.)
**Likely follow-ups:** 1) *Effect size for proportions?* Simply the difference in rates (or odds ratio). 2) *Are Cohen's cut-offs absolute?* No, only a rough guide; judge by business context.
**Common mistakes:** Reporting only "significant"; treating d of 0.2 as always unimportant; forgetting units.

### Q45 ⭐⭐ 🟡 What is a Type I error rate if you run 20 independent tests at alpha 0.05?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you do the quick probability behind multiple testing?
**Say this in the interview:** "Each test has a 5% chance of a false alarm, so the chance that none of 20 independent tests raises one is 0.95 to the power 20, about 36%. The chance of at least one false alarm is about 64%, and I would expect one false alarm on average."
**Explain simply:**
- Type I error: rejecting the null when it is actually true (a false alarm).
- Per-test rate stays 5%; the family-wise rate (at least one false alarm across all tests) climbs.
- Premise note: "independent" matters; correlated tests give a somewhat lower combined rate.
- Bonferroni divides alpha by 20 (0.0025) to pull the family-wise rate back to about 5%.
**Formula in plain words:** P(at least one false alarm) = 1 minus (1 minus alpha) raised to the number of tests.
**Worked example:** 1 - 0.95^20 = 0.6415. Expected false alarms = 20 x 0.05 = 1.
**Excel / Python:** In Excel: `=1-(1-0.05)^20` returns 0.6415 (any version; checked in Python, not run in Excel here).
```python
alpha = 0.05
number_of_tests = 20

# Chance that NONE of the 20 tests gives a false alarm
chance_no_false_alarm = (1 - alpha) ** number_of_tests

# Chance of at least one false alarm
chance_at_least_one = 1 - chance_no_false_alarm

# Bonferroni-adjusted alpha for each test
adjusted_alpha = alpha / number_of_tests
chance_at_least_one_after_fix = 1 - (1 - adjusted_alpha) ** number_of_tests

print("P(at least one false alarm):", round(chance_at_least_one, 4))
print("Expected false alarms:", alpha * number_of_tests)
print("Per-test alpha after Bonferroni:", adjusted_alpha)
print("P(at least one false alarm) after fix:", round(chance_at_least_one_after_fix, 4))
```
Output: `0.6415`, `1.0`, `0.0025`, `0.0488`. After the fix the combined risk is back near 5%.
**Likely follow-ups:** 1) *Why not just 20 x 5% = 100%?* Probabilities do not simply add; use the "none happens" route. 2) *Cost of Bonferroni?* Lower power.
**Common mistakes:** Saying the rate is 100%; saying it stays 5%; forgetting the independence assumption.

### Q46 ⭐⭐ 🟡 How do you test whether two proportions differ, for example the offer acceptance rate of two recruiters?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you pick and run the right test for a yes/no outcome in two groups?
**Say this in the interview:** "I use a two-proportion z-test, or the equivalent chi-square test on the 2 by 2 table. The null is that both recruiters have the same true acceptance rate; I compare the observed gap to what luck alone would produce."
**Explain simply:**
- Proportion: share of "yes" outcomes (offers accepted out of offers made).
- Under the null we pool both groups to get one overall rate, and measure how many standard errors apart the two observed rates are.
- Conditions: independent offers, and enough expected yes and no counts (about 5 or more in each cell). Otherwise use Fisher's exact test (Q56).
- Report the difference and its interval, not just the p-value.
**Formula in plain words:** z = (rate 1 minus rate 2) divided by sqrt(pooled rate x (1 - pooled rate) x (1/n1 + 1/n2)).
**Worked example:** Recruiter A: 66 of 100 offers accepted. Recruiter B: 48 of 100. Gap is 18 points; z = 2.571; p = 0.0101, so the difference is unlikely to be luck.
**Excel / Python:**
```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats

# Offers accepted out of offers made, by recruiter
accepted = np.array([66, 48])
offers_made = np.array([100, 100])

# Two-proportion z-test
z_statistic, p_value = proportions_ztest(accepted, offers_made)
print("Acceptance rates:", accepted / offers_made)
print("z =", round(z_statistic, 3), " p =", round(p_value, 4))

# Same question as a chi-square test on a 2x2 table (no continuity correction)
table = np.array([[66, 34],
                  [48, 52]])
chi_square, chi_p, degrees_of_freedom, _ = stats.chi2_contingency(table, correction=False)
print("chi-square =", round(chi_square, 3), " p =", round(chi_p, 4), " (z squared =", round(z_statistic**2, 3), ")")
```
Output: `Acceptance rates: [0.66 0.48]`, `z = 2.571  p = 0.0101`, `chi-square = 6.61  p = 0.0101  (z squared = 6.61 )`. The z-test and chi-square give the same answer for a 2 by 2 table.
**Likely follow-ups:** 1) *Why might the gap be misleading?* Recruiters may handle different roles; check for mix differences. 2) *Excel?* No single built-in; compute z by hand with the formula, then `=2*(1-NORM.S.DIST(ABS(z),TRUE))` (2010+; not run in Excel here).
**Common mistakes:** Comparing percentages without sample sizes; using a t-test on yes/no data; ignoring role mix.

### Q47 ⭐⭐ 🟡 A manager says 'the p-value is 0.04 so there is a 96% chance our hypothesis is right.' How do you respond?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you correct the most common p-value misreading politely and clearly?
**Say this in the interview:** "Not quite. A p-value of 0.04 means: if there were truly no effect, we would see a result this extreme only about 4% of the time. It does not tell us the probability that our idea is right; that also depends on how plausible the idea was to begin with."
**Explain simply:**
- The p-value answers "how surprising is this data if the null were true?", not "how likely is my hypothesis true?".
- Flipping that needs the prior plausibility (how likely such ideas are to work) and the test's power.
- If most ideas tested do not work, many "significant" results are false alarms.
- A good reply to a manager: stay friendly, give the correct sentence, then give the estimate and interval.
**Worked example:** Test 1,000 ideas where only 100 truly work. With 80% power, 80 real ones are detected; of the 900 useless ones, 5% (45) look significant. So only 80 of 125 significant results (64%) are real, not 95%.
**Excel / Python:**
```python
# Imagine 1000 ideas tested. Suppose only 10% (100) are truly effective.
ideas_tested = 1000
truly_effective = 100
truly_useless = ideas_tested - truly_effective

power = 0.80   # chance a real effect is detected
alpha = 0.05   # chance a useless idea looks significant

real_wins = truly_effective * power
false_wins = truly_useless * alpha

share_of_wins_that_are_real = real_wins / (real_wins + false_wins)
print("Real wins:", real_wins, " False wins:", false_wins)
print("Share of significant results that are real:", round(share_of_wins_that_are_real, 3))
```
Output: `Real wins: 80.0  False wins: 45.0`, `Share of significant results that are real: 0.64`. The 10% base rate is an assumption for illustration.
**Likely follow-ups:** 1) *Which method gives the probability the hypothesis is true?* Bayesian methods, with a prior. 2) *Is 0.04 weak evidence?* Moderate at best; look at the effect size.
**Common mistakes:** Agreeing with the manager to avoid friction; saying "p is the chance the result is due to chance" (also slightly wrong).

### Q48 ⭐⭐ 🔴 Explain a hypothesis test to a business stakeholder using a courtroom analogy.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you explain statistics to a non-technical person in a memorable, accurate way?
**Say this in the interview:** "Think of a trial. The null hypothesis is 'the defendant is innocent', meaning the new programme changes nothing. We only convict, meaning claim an effect, if the evidence would be very unlikely under innocence. Not enough evidence means 'not guilty', which is not the same as proven innocent."
**Explain simply:**
- Null hypothesis = presumption of innocence (no effect). Alternative = the claim we want proven.
- Evidence = the data. P-value = how surprising the evidence would be if the defendant were innocent.
- Alpha = the bar for "beyond reasonable doubt" (5% means we accept a 1-in-20 risk of convicting an innocent party).
- Type I error = convicting an innocent person (claiming an effect that is not real). Type II error = letting a guilty person go (missing a real effect).
- Verdict wording: "reject the null" (guilty) or "fail to reject" (not enough evidence).
**Worked example:** New onboarding, 90-day attrition 21% versus 15%. Innocent assumption: the programme does nothing. Evidence: a 6-point gap, p = 0.027, below our 0.05 bar, so we conclude the programme likely helps. Had p been 0.30, we would say "not enough evidence yet", not "the programme is useless".
**Likely follow-ups:** 1) *Where does the analogy break?* Courts also weigh the cost of errors differently; and a p-value is not the probability of guilt. 2) *Why a 5% bar?* A convention, not a law of nature; pick it by the cost of a wrong decision.
**Common mistakes:** Saying "we prove the null"; mixing up Type I and Type II; skipping the plain-English conclusion.

### Q49 ⭐⭐ 🔴 How do you choose the sample size for a test?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you plan the study before collecting data, using alpha, power and the smallest effect that matters?
**Say this in the interview:** "I fix four things: the alpha I accept, the power I want (usually 80%), the baseline rate or variability, and the smallest difference that would matter to the business. A power calculation then gives the required sample per group."
**Explain simply:**
- Power: the chance of detecting a real effect of the size you care about. 80% is a common target.
- Smaller effects, noisier data, stricter alpha or higher power all need more people.
- Halving the effect you want to detect needs about four times as many people.
- If the sample you can get is too small, say so before the test, not after.
**Formula in plain words:** For two proportions, n per group grows with (variance of the outcome) divided by (smallest difference squared); software does the arithmetic.
**Worked example:** Attrition at 90 days is 20%; we want to detect a fall to 15%. At alpha 0.05 and power 80%, we need about 902 hires per group; for 90% power, 1,208; for a smaller drop to 18%, about 6,036 per group.
**Excel / Python:**
```python
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Current 90-day attrition 20%; we want to detect a drop to 15%
effect_size = proportion_effectsize(0.20, 0.15)

power_calculator = NormalIndPower()
for power in [0.80, 0.90]:
    people_per_group = power_calculator.solve_power(effect_size=effect_size, alpha=0.05,
                                                    power=power, ratio=1.0, alternative="two-sided")
    print("power", power, "-> people per group:", round(people_per_group))

# Detecting a smaller drop (20% to 18%) needs far more people
small_effect = proportion_effectsize(0.20, 0.18)
people_small = power_calculator.solve_power(effect_size=small_effect, alpha=0.05, power=0.80)
print("20% -> 18% at power 0.80:", round(people_small))
```
Output: `power 0.8 -> people per group: 902`, `power 0.9 -> people per group: 1208`, `20% -> 18% at power 0.80: 6036`. A small company hiring 100 people a year cannot detect a 2-point drop.
**Likely follow-ups:** 1) *What if I cannot get that many?* Accept lower power, test a bigger change, or use a longer period. 2) *Does a bigger sample fix bias?* No.
**Common mistakes:** Choosing sample size after peeking; using "30 is enough" for every test; ignoring baseline rates.

### Q50 ⭐⭐ 🔴 How do you interpret a very small p-value from a very large sample?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that with huge data nearly everything becomes "significant"?
**Say this in the interview:** "A tiny p-value with a huge sample tells me the difference is probably real, not that it is big. I immediately look at the effect size and ask whether the gap matters in practice."
**Explain simply:**
- With a very large sample the test can detect extremely small differences.
- So "statistically significant" and "worth acting on" are two different questions.
- Check: effect size, confidence interval, cost of acting, and whether the data may have systematic bias (a huge biased sample is still biased).
**Worked example:** Two sites, 50,000 employees each, average salary Rs 60,000 versus Rs 60,300, SD 15,000. The p-value is 0.0016, yet the gap is Rs 300 (0.5%), Cohen's d = 0.02. Real, but not a reason to restructure pay.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Average monthly salary (rupees) at two big sites, 50,000 employees each
# Summary numbers: means, SD, group size
mean_site_a, mean_site_b = 60000, 60300
standard_deviation = 15000
people_per_site = 50000

result = stats.ttest_ind_from_stats(mean_site_b, standard_deviation, people_per_site,
                                    mean_site_a, standard_deviation, people_per_site)
cohens_d = (mean_site_b - mean_site_a) / standard_deviation
print("p-value:", result.pvalue)
print("difference in rupees:", mean_site_b - mean_site_a)
print("Cohen's d:", cohens_d)
```
Output: `p-value: 0.0015658698273104104`, `difference in rupees: 300`, `Cohen's d: 0.02`. Small p, tiny effect.
**Likely follow-ups:** 1) *What would you report?* The difference with its interval and a plain statement on business relevance. 2) *Opposite case?* Small sample, large effect, high p: likely under-powered.
**Common mistakes:** Calling it "highly significant, so important"; reporting only the p-value; ignoring data quality.

### Q51 ⭐⭐ 🔴 Walk through a full hypothesis test: does a new onboarding programme change 90-day attrition? Use numbers.
**Asked at:** commonly asked (no company-specific report found). One secondary Glassdoor summary mentions a hypothesis-test example in Tiger Analytics interviews (not verified).
**What the interviewer is checking:** Can you run the full process: hypotheses, alpha, test, p-value, decision, plain-English conclusion?
**Say this in the interview:** "I state the null as no change in the 90-day attrition rate, the alternative as a change, set alpha at 0.05, run a two-proportion z-test, and interpret the p-value together with the size of the change."
**Explain simply:**
- Step 1, hypotheses: H0 (null): the true attrition rates of old and new onboarding are equal. H1: they differ (two-sided, because we would want to know if the new one is worse too).
- Step 2, alpha = 0.05, set before looking.
- Step 3, data: old process 84 leavers of 400 (21%); new process 60 of 400 (15%).
- Step 4, test statistic: how many standard errors the observed gap is from zero, using the pooled rate (18%) under H0.
- Step 5, p-value and decision. Step 6, conclusion in plain words, with caveats (were hires randomly assigned or just different cohorts?).
**Formula in plain words:** z = (new rate minus old rate) divided by the standard error built from the pooled rate. p-value = chance of a gap at least this large either way if H0 were true.
**Worked example:** Gap is 6 points; z = -2.209; p = 0.0272 below 0.05, so reject H0. 95% interval for the change: -11.3 to -0.7 percentage points. Conclusion: the new programme is associated with lower 90-day attrition, plausibly by 1 to 11 points; the estimate is imprecise, and without random assignment we cannot be sure the programme caused it.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Hires who left within 90 days
old_leavers, old_hires = 84, 400      # old onboarding
new_leavers, new_hires = 60, 400      # new onboarding

old_rate = old_leavers / old_hires
new_rate = new_leavers / new_hires

# Pooled rate: the overall leaving rate if the programme made no difference (H0)
pooled_rate = (old_leavers + new_leavers) / (old_hires + new_hires)
standard_error = np.sqrt(pooled_rate * (1 - pooled_rate) * (1/old_hires + 1/new_hires))

# z statistic and two-sided p-value
z_statistic = (new_rate - old_rate) / standard_error
p_value = 2 * (1 - stats.norm.cdf(abs(z_statistic)))

# 95% confidence interval for the difference (new minus old)
unpooled_se = np.sqrt(old_rate*(1-old_rate)/old_hires + new_rate*(1-new_rate)/new_hires)
difference = new_rate - old_rate
lower, upper = difference - 1.96*unpooled_se, difference + 1.96*unpooled_se

print("old rate:", old_rate, " new rate:", new_rate, " pooled:", round(pooled_rate, 4))
print("z =", round(z_statistic, 3), " p =", round(p_value, 4))
print("difference:", round(difference, 3), " 95% CI:", round(lower, 3), "to", round(upper, 3))
```
Output: `old rate: 0.21  new rate: 0.15  pooled: 0.18`, `z = -2.209  p = 0.0272`, `difference: -0.06  95% CI: -0.113 to -0.007`. Negative means attrition fell.
**Likely follow-ups:** 1) *One-sided or two-sided?* Two-sided unless you decided in advance that only a drop matters. 2) *What if the groups were different periods?* Seasonal hiring could explain it; compare like with like.
**Common mistakes:** Saying "proves the programme works"; skipping the interval; ignoring how groups were chosen.

### Q52 ⭐ 🟢 What is a Z-score and how is it used in hypothesis testing?
**Asked at:** commonly asked (no company-specific report found). A reported Fractal question was "t-test versus z-test" (Glassdoor title only; not read in full).
**What the interviewer is checking:** Do you understand z as "distance from the expected value, in standard-deviation units"?
**Say this in the interview:** "A Z-score tells me how many standard deviations a value is from the mean. In a test, it measures how far my sample result is from what the null predicts, in standard errors; the further away, the smaller the p-value."
**Explain simply:**
- Standard deviation (SD): the typical spread of individual values. Standard error: the typical spread of a sample average.
- Z near 0: ordinary. Beyond about plus or minus 2: unusual (p about 0.05).
- A z-test is used when the SD is known or the sample is large; with an unknown SD and small sample, a t-test is used.
**Formula in plain words:** z = (observed value minus expected value) divided by the standard deviation (or standard error for a sample mean).
**Worked example:** HR claims average tenure is 36 months (SD 12). A sample of 64 employees averages 39. Standard error = 12/√64 = 1.5; z = 2.0; two-sided p = 0.0455. Separately, an employee paid 72,000 when the average is 60,000 and SD 8,000 has z = 1.5.
**Excel / Python:** Excel: `=STANDARDIZE(39,36,1.5)` returns 2 (all versions); `=2*(1-NORM.S.DIST(2,TRUE))` returns about 0.0455 (2010+). Not run in Excel here.
```python
from scipy import stats

# Average tenure claimed by HR: 36 months. Known SD: 12 months.
claimed_mean = 36
known_sd = 12
sample_size = 64
sample_mean = 39

# Z-score of the sample mean: distance from the claim in standard-error units
standard_error = known_sd / sample_size ** 0.5
z_score = (sample_mean - claimed_mean) / standard_error
p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
print("standard error:", standard_error, " z:", z_score, " p:", round(p_value, 4))

# Z-score of a single employee: salary 72,000 when average is 60,000 and SD is 8,000
print("single employee z:", (72000 - 60000) / 8000)
```
Output: `standard error: 1.5  z: 2.0  p: 0.0455`, `single employee z: 1.5`. Sample is two standard errors above the claim, just inside the unusual zone.
**Likely follow-ups:** 1) *Z versus t?* t has heavier tails to allow for estimating the SD from small samples. 2) *Critical z for 5%?* 1.96 two-sided.
**Common mistakes:** Dividing by SD instead of standard error for a sample mean; using z with a tiny sample and unknown SD.

### Q53 ⭐ 🟡 What is the difference between a parametric and a non-parametric test?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know when assumptions about the data's shape are needed?
**Say this in the interview:** "Parametric tests, like the t-test, assume the data follows a known shape, usually roughly normal, and compare means. Non-parametric tests, like Mann-Whitney, use ranks and make fewer assumptions, so they suit skewed data, outliers, small samples or ordinal scales."
**Explain simply:**
- Parameter: a summary of a population, like its mean. Parametric tests estimate such parameters under a shape assumption.
- Non-parametric: ranks the values (1st, 2nd, 3rd) and works with the ranks, so extreme values have limited influence.
- Trade-off: when assumptions hold, parametric tests are a little more powerful; when they fail, non-parametric tests are safer.
- Pairs: t-test and Mann-Whitney (two groups); paired t-test and Wilcoxon signed-rank (before and after); ANOVA and Kruskal-Wallis (3+ groups).
**Worked example:** Comparing time-to-hire for two teams with a couple of extreme delays: use Mann-Whitney (see Q54). Comparing average satisfaction across 300 employees in two branches with symmetric scores: a t-test is fine.
**Likely follow-ups:** 1) *Do non-parametric tests assume nothing?* They still need independent observations. 2) *Which compares medians?* Roughly, Mann-Whitney compares overall ranking, which is often read as a shift in medians.
**Common mistakes:** Thinking non-parametric means "no assumptions"; using a t-test on heavy-tailed data by habit.

### Q54 ⭐ 🟡 When would you use the Mann-Whitney U test instead of a t-test?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you pick a robust two-group test for messy data?
**Say this in the interview:** "When the data is skewed, has outliers, is a small sample, or is ordinal like a 1-to-5 rating. Mann-Whitney ranks all values together and checks whether one group tends to sit higher, so one extreme value cannot dominate."
**Explain simply:**
- Two independent groups, no pairing.
- It asks: "if I pick one person from each group at random, is one more likely to be higher?"
- Looks at ranks, so it is not thrown off by a 150-day vacancy.
- Interpret together with medians and a plain description of the gap.
**Worked example:** Days to close vacancies. Team A median 33.5 days, Team B 51.5 days, but each team has one very slow hire (120 and 150 days). The t-test is thrown off by the extremes (p = 0.18, no evidence); Mann-Whitney finds the consistent gap (p = 0.011).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Days taken to close a vacancy (skewed, with two very slow hires)
team_a_days = np.array([21, 25, 28, 30, 32, 35, 38, 41, 45, 120])
team_b_days = np.array([34, 40, 44, 47, 50, 53, 58, 62, 70, 150])

t_result = stats.ttest_ind(team_a_days, team_b_days)
u_result = stats.mannwhitneyu(team_a_days, team_b_days, alternative="two-sided")

print("Medians:", np.median(team_a_days), np.median(team_b_days))
print("t-test p-value       :", round(t_result.pvalue, 4))
print("Mann-Whitney p-value :", round(u_result.pvalue, 4), " U =", u_result.statistic)
```
Output: `Medians: 33.5 51.5`, `t-test p-value : 0.1794`, `Mann-Whitney p-value : 0.0113  U = 16.0`. Outliers inflated the spread and hid the pattern for the t-test. Excel has no built-in Mann-Whitney; use Python or rank the data manually.
**Likely follow-ups:** 1) *Paired data?* Wilcoxon signed-rank. 2) *Does it need normality?* No.
**Common mistakes:** Running both and picking the better p-value (decide in advance); saying it tests "medians" without caveat.

### Q55 ⭐ 🟡 What is Welch's t-test and when is it preferred?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the standard t-test's equal-spread assumption and the safe default?
**Say this in the interview:** "Welch's t-test compares two means without assuming the groups have equal variance, which is the spread of values. When group sizes or spreads differ, it keeps the false-alarm rate honest, so many analysts use it by default."
**Explain simply:**
- The classic (Student) t-test pools the two spreads, which is only fair if they are similar.
- Welch's version keeps each group's spread separate and adjusts the degrees of freedom (the effective sample information).
- If the spreads are equal, Welch loses almost nothing.
- Use it especially when one group is small and much more variable than the other.
**Worked example:** Overtime hours: a steady team (n = 8, mean 11.88, SD 1.25) and a variable team (n = 20, mean 21.2, SD 11.9). Student p = 0.038, Welch p = 0.0025 (Welch is more reliable here, and the pooled version actually understated the evidence).
**Excel / Python:** Excel: Data Analysis ToolPak "t-Test: Two-Sample Assuming Unequal Variances", or `=T.TEST(range1,range2,2,3)` (type 3 = unequal variance; 2010+). Not run in Excel here.
```python
import numpy as np
from scipy import stats

# Monthly overtime hours: a small steady team and a large, very variable team
steady_team = np.array([10, 11, 12, 12, 13, 14, 12, 11])
variable_team = np.array([8, 20, 35, 5, 28, 40, 12, 30, 25, 3, 38, 15, 22, 9, 33, 18, 27, 6, 36, 14])

student_result = stats.ttest_ind(steady_team, variable_team, equal_var=True)
welch_result = stats.ttest_ind(steady_team, variable_team, equal_var=False)

print("Means:", round(steady_team.mean(), 2), round(variable_team.mean(), 2))
print("SDs  :", round(steady_team.std(ddof=1), 2), round(variable_team.std(ddof=1), 2))
print("Student p:", round(student_result.pvalue, 4), " t:", round(student_result.statistic, 3))
print("Welch p  :", round(welch_result.pvalue, 4), " t:", round(welch_result.statistic, 3))
```
Output: `Means: 11.88 21.2`, `SDs  : 1.25 11.9`, `Student p: 0.038  t: -2.187`, `Welch p  : 0.0025  t: -3.457`. Because the small group is the less variable one, the pooled test misjudges the uncertainty.
**Likely follow-ups:** 1) *Should I test equal variances first (Levene)?* Many statisticians say just use Welch. 2) *Does Welch fix non-normality?* No.
**Common mistakes:** Assuming equal variances by default; thinking the direction of the error is always "too many false alarms" (it can go either way).

### Q56 ⭐ 🟡 What is Fisher's exact test and when is it used instead of chi-square?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know chi-square's small-count limit and the exact alternative?
**Say this in the interview:** "Fisher's exact test checks the link between two yes/no variables in a 2 by 2 table without relying on a large-sample approximation. I use it when expected counts in any cell are below about 5, for example with small teams."
**Explain simply:**
- Chi-square compares observed counts with expected counts using an approximation that is poor when counts are small.
- Fisher calculates the exact probability of tables at least as extreme, given the row and column totals.
- It is mostly used for 2 by 2 tables; software can extend it to larger tables.
- Expected count: the number you would see in a cell if there were no link (row total x column total / grand total).
**Worked example:** A small leadership batch of 20: 1 of 10 women promoted, 6 of 10 men promoted. Expected counts are 3.5 and 6.5 (under 5), so chi-square (p = 0.019) is unreliable. Fisher's exact gives p = 0.057, a more cautious, correct result: not quite significant at 0.05.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Rows: women, men in a small senior-leadership batch. Columns: promoted, not promoted
table = np.array([[1, 9],
                  [6, 4]])

chi_square, chi_p, _, expected_counts = stats.chi2_contingency(table, correction=False)
odds_ratio, fisher_p = stats.fisher_exact(table, alternative="two-sided")

print("Expected counts if no link:", expected_counts.round(2).tolist())
print("Chi-square p:", round(chi_p, 4))
print("Fisher exact p:", round(fisher_p, 4))
```
Output: `Expected counts if no link: [[3.5, 6.5], [3.5, 6.5]]`, `Chi-square p: 0.0191`, `Fisher exact p: 0.0573`. Same data, different verdicts; Fisher is the valid one here. Excel has no built-in Fisher test.
**Likely follow-ups:** 1) *Can I use it for big samples?* Yes, but chi-square is fine and quicker. 2) *Chi-square with continuity correction?* A partial fix; Fisher is cleaner.
**Common mistakes:** Running chi-square on tiny counts; ignoring that small samples also mean low power.

### Q57 ⭐ 🟡 What is the difference between the chi-square test of independence and the test of homogeneity?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that the same calculation answers questions framed differently by how data was collected?
**Say this in the interview:** "The arithmetic is identical. Independence: one sample, two categorical variables, are they linked? Homogeneity: separate samples from several groups, do they share the same distribution of one category? The difference is how the data was sampled and how I phrase the conclusion."
**Explain simply:**
- Independence: take 500 employees at random and record department and whether they left. Question: is leaving related to department?
- Homogeneity: pick 100 people from each department on purpose, then record whether they left. Question: is the leaving rate the same in every department?
- Both use observed versus expected counts, the same chi-square statistic and the same degrees of freedom: (rows minus 1) x (columns minus 1).
- Practical effect: only the wording of the null differs.
**Worked example:** 100 employees sampled per department: leavers 30 (Sales), 20 (Support), 10 (Finance). Chi-square = 12.5, df = 2, p = 0.0019: leaving rates are not the same across departments (homogeneity framing). The same table under random sampling of 300 employees would be read as "leaving and department are linked".
**Excel / Python:** Excel: `=CHISQ.TEST(observed_range, expected_range)` (2010+; not run in Excel here).
```python
import numpy as np
from scipy import stats

# Left within a year (yes, no) by department
table = np.array([[30, 70],    # Sales
                  [20, 80],    # Support
                  [10, 90]])   # Finance

chi_square, p_value, degrees_of_freedom, expected = stats.chi2_contingency(table)
print("chi-square =", round(chi_square, 3), " df =", degrees_of_freedom, " p =", round(p_value, 4))
print("Expected counts:", expected.round(1).tolist())
```
Output: `chi-square = 12.5  df = 2  p = 0.0019`, `Expected counts: [[20.0, 80.0], [20.0, 80.0], [20.0, 80.0]]`. Sales leaves more and Finance less than the overall 20% average.
**Likely follow-ups:** 1) *Goodness-of-fit?* One variable against a fixed expected split. 2) *Which department differs?* Look at residuals or run pairwise tests with correction.
**Common mistakes:** Saying they use different formulas; claiming chi-square proves cause; ignoring small expected counts.

### Q58 ⭐ 🟡 What is a two-way ANOVA?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** Do you know it studies two grouping factors at once, plus their interaction?
**Say this in the interview:** "A two-way ANOVA compares average outcomes across two categorical factors together, for example salary by department and by gender, and also checks whether the two factors interact. It gives one F-test and p-value for each factor and one for the interaction."
**Explain simply:**
- **One-way ANOVA** (Q18) uses one factor; **two-way** uses two.
- Three questions are answered: does department matter, does gender matter, and does the effect of one depend on the other?
- An **interaction** means the gap changes by group, for example a pay gap that exists in Tech but not in HR.
- Same assumptions as ANOVA: independent observations, roughly normal residuals, similar spread in every cell.
**Worked example:** 120 made-up employees (20 per department and gender cell). Department is clearly significant, gender is not at 5%, and there is no interaction.
**Excel / Python:** Excel has "Anova: Two-Factor With Replication" in the Data Analysis ToolPak (not run in Excel here).
```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Build 20 made-up salaries for every department and gender combination
random_generator = np.random.default_rng(1)
rows = []
for department, base_salary in [("Sales", 40000), ("Tech", 50000), ("HR", 42000)]:
    for gender, extra in [("F", 0), ("M", 1000)]:
        for salary in random_generator.normal(base_salary + extra, 4000, 20):
            rows.append((department, gender, salary))
salary_table = pd.DataFrame(rows, columns=["department", "gender", "salary"])

# Fit the two-way model; the * adds the interaction term
model = smf.ols("salary ~ C(department) * C(gender)", data=salary_table).fit()

# Print the ANOVA table (only the F and p columns matter here)
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table[["df", "F", "PR(>F)"]].round(3))
```
Reading it: department has p near 0 (salaries really differ by department); gender p = 0.081 (not significant at 5%); the interaction p = 0.862 (the gender gap is similar in every department).
**Likely follow-ups:** 1) *What if the interaction is significant?* Interpret the factors together, not separately. 2) *What does "replication" mean in Excel?* More than one observation per cell.
**Common mistakes:** Reading the main effects while ignoring a significant interaction; running it with very unequal group sizes without care.

### Q59 ⭐ 🟡 How do you test whether data is normally distributed before using a t-test?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you check assumptions both visually and with a test, and know that sample size matters?
**Say this in the interview:** "I look at a histogram or Q-Q plot first, check skewness, and then run a Shapiro-Wilk test, where a small p-value means the data is not normal. But with larger samples the t-test is fairly forgiving because of the Central Limit Theorem, so I use judgement, not just the p-value."
**Explain simply:**
- **Histogram**: should look like a symmetric bell.
- **Q-Q plot**: points should hug a straight line; curves mean skew.
- **Skewness** near 0 is good; salaries are usually skewed to the right.
- **Shapiro-Wilk test**: null hypothesis is "data is normal", so a small p-value is bad news for normality.
- With about 30+ per group, the t-test usually holds up; with tiny or very skewed samples use a rank-based test (Q63).
**Worked example:** Two made-up samples of 40. Tenure looks normal; salary is right-skewed.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

random_generator = np.random.default_rng(7)

# Two made-up samples of 40: one roughly bell-shaped, one right-skewed like salaries
tenure_years = random_generator.normal(3.4, 1.5, 40)
monthly_salaries = random_generator.lognormal(10.5, 0.7, 40)

# Shapiro-Wilk test: a small p-value says "not normal"
for name, values in [("tenure", tenure_years), ("salary", monthly_salaries)]:
    w_statistic, p_value = stats.shapiro(values)
    print(name, "skew", round(stats.skew(values), 2), "p-value", round(p_value, 4))
```
Tenure: p = 0.95, no sign of non-normality. Salary: skew 1.38 and p = 0.0004, clearly not normal, so I would use a log transform or a rank test.
**Likely follow-ups:** 1) *Do we test normality of the raw data?* For t-tests, the sample means or residuals matter; raw data is the usual quick check. 2) *Large sample, tiny p in Shapiro?* It detects trivial departures; look at the plot.
**Common mistakes:** Saying "p > 0.05 proves it is normal" (it only fails to show otherwise); relying on the test alone with huge samples.

### Q60 ⭐ 🟡 What is a paired test versus an independent test, and what goes wrong if you pick the wrong one?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you spot whether the same people were measured twice, and do you know the cost of the wrong choice?
**Say this in the interview:** "A paired test compares two measurements on the same people, such as before and after training. An independent test compares two separate groups. If I use an independent test on paired data, I throw away the pairing and lose power, so real effects get missed."
**Explain simply:**
- **Paired**: each row in one column is linked to a row in the other (same employee).
- **Independent**: different people in each group.
- The paired test works on each person's difference, which removes the person-to-person variation (some people always score high).
- Wrong the other way (paired test on independent groups) is also invalid, because there is no real pairing.
**Worked example:** 15 employees scored before and after a training. Average gain is about 4.9 points (SD of the gains 2.5), but scores vary a lot between people (from 34 to 93).
**Excel / Python:** Excel: "t-Test: Paired Two Sample for Means" versus "Two-Sample Assuming Equal/Unequal Variances".
```python
import numpy as np
from scipy import stats

# 15 employees: test score before and after the same training
random_generator = np.random.default_rng(3)
scores_before = random_generator.normal(60, 10, 15).round(0)
scores_after = (scores_before + random_generator.normal(4, 3, 15)).round(0)

# Right test: paired (same people twice)
paired_result = stats.ttest_rel(scores_after, scores_before)
print("paired      t", round(paired_result.statistic, 2), "p", round(paired_result.pvalue, 6))

# Wrong test here: treats the two columns as different people
independent_result = stats.ttest_ind(scores_after, scores_before)
print("independent t", round(independent_result.statistic, 2), "p", round(independent_result.pvalue, 3))
```
Paired: t = 7.76, p about 0.000002, a clear gain. Independent: t = 0.97, p = 0.338, the gain is drowned out by differences between people. Same data, opposite conclusions.
**Likely follow-ups:** 1) *Do paired groups need the same size?* Yes, every person needs two values. 2) *Which assumption for the paired test?* Differences roughly normal.
**Common mistakes:** Using an independent test on before/after data; forgetting to drop people missing one of the two measurements.

### Q61 ⭐ 🟡 What is the F-test for comparing two variances?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it compares spread, and its weakness with non-normal data?
**Say this in the interview:** "The F-test for two variances checks whether two groups are equally spread out. The statistic is the larger sample variance divided by the smaller; if it is far above 1, the spreads differ. It is very sensitive to non-normal data, so many analysts use Levene's test instead."
**Explain simply:**
- **Variance** is the average squared distance from the mean (the SD squared).
- Null hypothesis: both groups have the same variance. F near 1 supports it.
- Used to decide between the equal-variance and Welch version of the t-test, though many just use Welch by default.
- Excel has it: Data Analysis "F-Test Two-Sample for Variances" (not run in Excel here).
**Formula in plain words:** F = larger variance divided by smaller variance. Symbols: F = s1² / s2², with n1-1 and n2-1 degrees of freedom.
**Worked example:** Weekly overtime hours of two teams of 10: team A is erratic, team B is steady.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Weekly overtime hours: team A is erratic, team B is steady
overtime_team_a = np.array([48, 52, 55, 40, 61, 45, 58, 50, 43, 66])
overtime_team_b = np.array([50, 51, 52, 49, 53, 50, 51, 52, 50, 49])

# Sample variances (ddof=1 means divide by n-1)
variance_a = overtime_team_a.var(ddof=1)
variance_b = overtime_team_b.var(ddof=1)

# F statistic = bigger variance / smaller variance
f_statistic = variance_a / variance_b

# Two-sided p-value from the F distribution (9 and 9 degrees of freedom)
p_value = 2 * stats.f.sf(f_statistic, 9, 9)

print("variances", round(variance_a, 2), round(variance_b, 2))
print("F", round(f_statistic, 2), "p", round(p_value, 6))
```
F = 38.2, p = 0.000008: team A's overtime is far more variable than team B's.
**Likely follow-ups:** 1) *Better alternative?* Levene's test, less sensitive to non-normality. 2) *If variances differ?* Use Welch's t-test.
**Common mistakes:** Using it on skewed data; putting the smaller variance on top and forgetting to adjust the tails.

### Q62 ⭐ 🟡 What is the Bonferroni correction? Give an example.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand why many tests inflate false alarms, and the simplest fix?
**Say this in the interview:** "Bonferroni divides the significance level by the number of tests. With 5 tests at 0.05, each must have p below 0.01. It keeps the chance of even one false alarm across all tests at about 5%, but it is conservative."
**Explain simply:**
- Each extra test gives another chance of a false positive (Q39, Q45).
- Bonferroni makes the bar stricter for every test: adjusted alpha = alpha / number of tests.
- Equivalent: multiply each p-value by the number of tests and compare with 0.05.
- Downside: it can miss real effects, especially with many tests (see FDR, Q68).
**Formula in plain words:** New alpha = original alpha divided by the number of tests. Symbols: α* = α / m.
**Worked example:** Attrition compared across 5 departments with these p-values: 0.004, 0.020, 0.030, 0.200, 0.600. Unadjusted, three look significant. Adjusted alpha is 0.05/5 = 0.01, so only the first survives.
**Excel / Python:**
```python
# Five p-values from five separate HR comparisons
p_values = [0.004, 0.020, 0.030, 0.200, 0.600]
number_of_tests = len(p_values)

# Bonferroni: divide alpha by the number of tests
adjusted_alpha = 0.05 / number_of_tests
print("adjusted alpha", adjusted_alpha)

# Check each p-value against the stricter bar
for p_value in p_values:
    print(p_value, "significant" if p_value < adjusted_alpha else "not significant")
```
Only p = 0.004 passes. The 0.02 and 0.03 results could easily be luck given five looks.
**Likely follow-ups:** 1) *Drawback?* Loses power. 2) *Less strict options?* Holm, or Benjamini-Hochberg.
**Common mistakes:** Applying it to just one test; forgetting to state how many tests were really run, including ones you dropped.

### Q63 ⭐ 🟡 How do you handle a hypothesis test when the data has outliers?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you investigate outliers before choosing a method, rather than deleting them blindly?
**Say this in the interview:** "First I check whether the outlier is an error or a real value. If it is an error I fix or remove it with a note; if it is real, I run a robust method such as a Mann-Whitney test or a trimmed mean, and I report results with and without it."
**Explain simply:**
- An **outlier** is a value far from the rest (a typo like 250 instead of 50, or a real executive salary).
- The mean and t-test are sensitive to outliers because they inflate the SD and shift the mean.
- **Robust options**: Mann-Whitney (works on ranks), median-based comparison, trimmed mean, log transform, bootstrap (Q72).
- Always document what you did.
**Worked example:** Overtime hours for two teams. Team B has a data-entry error of 250.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Monthly overtime hours for two teams; team B has one data-entry error (250)
team_a = np.array([42, 45, 47, 44, 46, 43, 48, 45, 44, 46])
team_b_clean = np.array([46, 48, 50, 47, 49, 45, 51, 48, 47, 49])
team_b_outlier = team_b_clean.copy()
team_b_outlier[-1] = 250

# Welch t-test on clean data, then with the outlier
print("t-test clean   p", round(stats.ttest_ind(team_b_clean, team_a, equal_var=False).pvalue, 4))
print("t-test outlier p", round(stats.ttest_ind(team_b_outlier, team_a, equal_var=False).pvalue, 4))

# Rank-based Mann-Whitney test barely notices one extreme value
print("Mann-Whitney   p", round(stats.mannwhitneyu(team_b_outlier, team_a).pvalue, 4))

# Mean is dragged up, median is not
print("mean", team_b_outlier.mean(), "median", np.median(team_b_outlier))
```
The clean t-test finds a real difference (p = 0.0017). One bad value turns it into p = 0.283 and the mean to 68 while the median stays 48. Mann-Whitney still finds the difference (p = 0.0043).
**Likely follow-ups:** 1) *When to delete an outlier?* Only with a documented reason (error), not because it is inconvenient. 2) *Does Mann-Whitney compare medians?* Roughly; strictly, whether one group tends to be higher.
**Common mistakes:** Deleting outliers until the p-value is significant; ignoring them completely.

### Q64 ⭐ 🟡 How are the confidence interval and the two-sided test linked? If the 95% CI for a mean difference excludes zero, what is the p-value?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you see the CI and the test as two views of the same evidence?
**Say this in the interview:** "If a 95% confidence interval for the difference excludes zero, the two-sided test at 5% is significant, so p is below 0.05. If the interval includes zero, p is above 0.05. The interval is more useful because it also shows the size and the uncertainty."
**Explain simply:**
- A **confidence interval** (CI) is a range of plausible values for the true difference.
- Zero means "no difference". If zero is outside the 95% range, no-difference is not plausible at the 5% level.
- This match holds for a two-sided test with the same confidence and alpha (95% with 0.05, 99% with 0.01).
- The CI does not give the exact p-value, only whether it is above or below alpha.
**Worked example:** Engagement scores for two groups of 60 (made up).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Engagement scores for two groups of 60 employees
random_generator = np.random.default_rng(11)
group_a = random_generator.normal(52, 8, 60)
group_b = random_generator.normal(47, 8, 60)

# Two-sample t-test and its 95% confidence interval for the difference
result = stats.ttest_ind(group_a, group_b)
interval = result.confidence_interval(0.95)

print("difference in means", round(group_a.mean() - group_b.mean(), 2))
print("95% CI", round(interval.low, 2), "to", round(interval.high, 2))
print("p-value", round(result.pvalue, 4))
```
The 95% interval (0.71 to 6.22) excludes zero and p = 0.0143, below 0.05. Consistent.
**Likely follow-ups:** 1) *CI includes zero, so is there no effect?* No, only that the data cannot rule it out (Q65). 2) *Does it work for one-sided tests?* Only with a one-sided interval.
**Common mistakes:** Saying a 95% CI means 95% chance the true value is inside this one interval; comparing two separate CIs for overlap instead of testing the difference.

### Q65 ⭐ 🟡 Does a high p-value prove the two groups are the same?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know "no evidence of a difference" is not "evidence of no difference"?
**Say this in the interview:** "No. A high p-value only says the data did not give strong enough evidence of a difference. It could be that the groups really are the same, or that the sample was too small to see a real difference. To claim similarity you need a confidence interval that is narrow around zero or an equivalence test."
**Explain simply:**
- We only "fail to reject" the null (Q11), we never prove it.
- Low **power** (Q26) means a real gap often goes unnoticed.
- The confidence interval shows what is still possible: a wide interval is a warning sign.
- To show similarity on purpose, use an **equivalence test** (TOST) with a margin that you define as "close enough".
**Worked example:** Six employees per group; the gap is 8.7 points, but p = 0.075.
**Excel / Python:**
```python
import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower

# Six employees per group: an apparent 8.7 point gap in scores
group_x = np.array([61, 70, 52, 75, 58, 66])
group_y = np.array([55, 48, 66, 50, 59, 52])

result = stats.ttest_ind(group_x, group_y)
interval = result.confidence_interval(0.95)
print("difference", round(group_x.mean() - group_y.mean(), 2), "p", round(result.pvalue, 3))
print("95% CI", round(interval.low, 1), "to", round(interval.high, 1))

# Power: the chance this test would catch a gap of this size with n=6 per group
pooled_sd = np.sqrt((group_x.var(ddof=1) + group_y.var(ddof=1)) / 2)
effect_size = (group_x.mean() - group_y.mean()) / pooled_sd
power = TTestIndPower().power(effect_size=effect_size, nobs1=6, alpha=0.05)
print("power", round(power, 2))
```
The interval runs from -1.0 to 18.4, so a gap as large as 18 points is still possible. Power is only 0.44, so the test would miss a gap like this more than half the time. The groups are not shown to be the same.
**Likely follow-ups:** 1) *What would you do?* Collect more data (Q49). 2) *How to prove equivalence?* TOST.
**Common mistakes:** Telling a manager "the training had no effect" from a p of 0.075 on six people.

### Q66 ⭐ 🟡 What is the difference between a Z-test and a t-test for proportions in practice, and which do analysts usually run?
**Asked at:** commonly asked (no company-specific report found) Premise note: analysts do not use a t-test for proportions; the z-test (or the chi-square test) is the standard, so I answer that.
**What the interviewer is checking:** Do you know proportions use a z-test, and that it matches the 2x2 chi-square?
**Say this in the interview:** "For proportions, such as offer acceptance rates, the usual test is the z-test, which uses the normal curve because the standard deviation of a proportion follows from the proportion itself. A t-test is for averages of measured values. In practice, analysts run the two-proportion z-test or the equivalent chi-square test, and the answers agree."
**Explain simply:**
- A t-test needs a mean and an estimated SD from the data. A proportion has its SD built in: sqrt(p x (1-p) / n), so z is used.
- For a 2x2 table, z squared equals the chi-square statistic (without continuity correction).
- Needs enough counts in each cell (a common rule: at least 5 to 10 successes and failures). Otherwise use Fisher's exact test.
**Formula in plain words:** z = (difference in the two rates) / (standard error of that difference, using the combined rate). Symbols: z = (p1 - p2) / sqrt(p(1-p)(1/n1 + 1/n2)).
**Worked example:** Recruiter 1 got 45 of 100 offers accepted, recruiter 2 got 30 of 100.
**Excel / Python:**
```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

# Offer accepted: recruiter 1 got 45 of 100, recruiter 2 got 30 of 100
accepted = np.array([45, 30])
offers = np.array([100, 100])

# Z-test for two proportions
z_statistic, z_p_value = proportions_ztest(accepted, offers)
print("z", round(z_statistic, 3), "p", round(z_p_value, 4))

# Same data as a chi-square test (no continuity correction)
table = np.array([[45, 55], [30, 70]])
chi_result = stats.chi2_contingency(table, correction=False)
print("z squared", round(z_statistic ** 2, 2), "chi-square", round(chi_result.statistic, 2), "p", round(chi_result.pvalue, 4))
```
z = 2.19, p = 0.0285, so the acceptance rates differ at 5%. z squared (4.8) equals the chi-square value: same test in two forms.
**Likely follow-ups:** 1) *Small counts?* Fisher's exact test. 2) *Many categories?* Chi-square.
**Common mistakes:** Running a t-test on 0/1 data by habit (it usually gives similar results, but it is not the standard); testing percentages without the underlying counts.

### Q67 ⭐ 🔴 What is the Bayesian view of hypothesis testing, and how does it differ from the p-value approach?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** Can you contrast "probability of data given the null" with "probability of the hypothesis given the data"?
**Say this in the interview:** "The p-value approach asks how surprising the data would be if the null were true. The Bayesian approach starts with a prior belief, updates it with the data, and gives a direct probability for the hypothesis, such as an 85% chance that the true rate is above 40%. It answers the question managers actually ask, but it needs a prior."
**Explain simply:**
- **Prior**: what we believed before the data. **Posterior**: belief after seeing it.
- A **credible interval** really does mean "95% probability the value lies here", unlike a confidence interval.
- The p-value never gives the probability that your hypothesis is true (Q47).
- Results can depend on the prior, especially with little data.
**Formula in plain words:** Posterior belief is proportional to prior belief times how well the data fits. Symbols: P(H | data) is proportional to P(data | H) x P(H).
**Worked example:** 45 of 100 offers accepted. Does the true acceptance rate beat 40%?
**Excel / Python:**
```python
from scipy import stats

# 45 of 100 candidates accepted. Start with a flat prior Beta(1, 1).
accepted, offers = 45, 100
posterior = stats.beta(1 + accepted, 1 + offers - accepted)

# Posterior: mean, 95% credible interval, and probability the true rate beats 40%
print("posterior mean", round(posterior.mean(), 3))
low, high = posterior.interval(0.95)
print("95% credible interval", round(low, 3), "to", round(high, 3))
print("P(rate > 0.40)", round(posterior.sf(0.40), 3))

# Frequentist p-value for the same data against H0: rate = 0.40
print("p-value", round(stats.binomtest(accepted, offers, 0.40).pvalue, 3))
```
Bayesian: an 85% probability the rate is above 40%, with a 95% credible interval of 0.356 to 0.548. The p-value (0.309) answers a different question: how likely a result this far from 40% would be if the rate were exactly 40%.
**Likely follow-ups:** 1) *Which do you use at work?* Frequentist is common; Bayesian is popular in A/B testing. 2) *Prior choice?* A flat prior is neutral, but state it.
**Common mistakes:** Reading a p-value as the probability the hypothesis is true; hiding the prior.

### Q68 ⭐ 🔴 What is the false discovery rate, and how does it differ from the family-wise error rate?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know there are two ways to control errors across many tests?
**Say this in the interview:** "The family-wise error rate is the chance of at least one false positive among all tests; Bonferroni controls it. The false discovery rate is the expected share of false positives among the results I flag. FDR is more lenient, so it finds more real effects when I run hundreds of tests."
**Explain simply:**
- **FWER**: strict, "no false alarms at all, 95% of the time". Good when one mistake is costly.
- **FDR**: "of the things I flag, about 5% may be false". Good for screening many candidates.
- The Benjamini-Hochberg procedure controls FDR.
- HR use: screening 100 survey questions or 100 branches for something unusual.
**Worked example:** 100 checks, 20 truly real and 80 pure noise (simulated).
**Excel / Python:**
```python
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

# 100 checks: 20 have a real effect, 80 are pure noise
random_generator = np.random.default_rng(4)
real_p_values = [stats.ttest_1samp(random_generator.normal(0.6, 1, 30), 0).pvalue for _ in range(20)]
noise_p_values = [stats.ttest_1samp(random_generator.normal(0, 1, 30), 0).pvalue for _ in range(80)]
all_p_values = np.array(real_p_values + noise_p_values)

# Count discoveries and false discoveries under three rules
raw_flags = all_p_values < 0.05
print("no correction  found", raw_flags.sum(), "false", raw_flags[20:].sum())
for label, method in [("Bonferroni (FWER)", "bonferroni"), ("Benjamini-Hochberg (FDR)", "fdr_bh")]:
    flags = multipletests(all_p_values, alpha=0.05, method=method)[0]
    print(label, "found", flags.sum(), "false", flags[20:].sum())
```
With no correction: 21 flagged, 3 of them false. Bonferroni flags 8 (all real, but misses 12). Benjamini-Hochberg flags 14 (all real here), finding more at an accepted small share of false hits.
**Likely follow-ups:** 1) *When Bonferroni?* A small number of important tests. 2) *Is FDR a guarantee per run?* No, it is controlled on average.
**Common mistakes:** Treating FDR 5% as "5% chance each result is wrong"; skipping correction entirely.

### Q69 ⭐ 🔴 What is the difference between a Type S and Type M error?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic (Gelman and Carlin's terms).
**What the interviewer is checking:** Do you understand how small, underpowered studies mislead even when significant?
**Say this in the interview:** "A Type S (sign) error is concluding the effect goes in the wrong direction. A Type M (magnitude) error is overstating its size. Both are worse in low-power studies: the only results that reach significance are the lucky exaggerated ones."
**Explain simply:**
- Type I/II (Q5) are about whether an effect exists; S and M are about what a **significant** result tells you.
- With a noisy small sample, only big estimates pass p < 0.05, so significant results overstate the truth.
- Some significant results even point the wrong way.
- Remedy: bigger samples, report intervals, and do not over-trust a surprising finding from a small study.
**Worked example:** True gap is only 1 point (SD 10, 20 people per group). I simulated 20,000 studies.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# True gap is only 1 point (SD 10, 20 people per group): an underpowered study
random_generator = np.random.default_rng(8)
true_gap = 1
significant_gaps = []
for _ in range(20000):
    group_a = random_generator.normal(true_gap, 10, 20)
    group_b = random_generator.normal(0, 10, 20)
    if stats.ttest_ind(group_a, group_b).pvalue < 0.05:
        significant_gaps.append(group_a.mean() - group_b.mean())
significant_gaps = np.array(significant_gaps)

print("share of studies significant", round(len(significant_gaps) / 20000, 3))
print("average gap among significant ones", round(np.abs(significant_gaps).mean(), 1))
print("share with the wrong sign (Type S)", round((significant_gaps < 0).mean(), 2))
```
Only 6% of studies were significant, and those reported an average gap of 7.3 points (7 times too big, Type M). About 22% of the significant ones had the wrong sign (Type S).
**Likely follow-ups:** 1) *How to avoid?* Plan for adequate power (Q49, Q70). 2) *Does it affect large studies?* Much less.
**Common mistakes:** Treating a significant result from a tiny sample as the true effect size.

### Q70 ⭐ 🔴 What is the minimum detectable effect, and how does it connect to power?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you link sample size, power and the smallest effect worth detecting?
**Say this in the interview:** "The minimum detectable effect is the smallest true difference my test would reliably catch, usually with 80% power at alpha 0.05. A bigger sample lowers it. I choose it from the business side: the smallest change that would matter, then I compute the sample size needed."
**Explain simply:**
- **Power** (Q26) is the chance of detecting a real effect, commonly set at 80%.
- Fix alpha, power and sample size, and the MDE follows; fix MDE and you get the needed sample size.
- Halving the MDE needs about 4 times the sample, because precision grows with the square root of n.
- Used in A/B test planning (Part 8).
**Worked example:** Test scores with an SD of 10 points.
**Excel / Python:**
```python
from statsmodels.stats.power import TTestIndPower

power_calculator = TTestIndPower()

# Smallest standardised effect detectable with 80% power at alpha 0.05
for people_per_group in [50, 100, 200, 400]:
    effect = power_calculator.solve_power(nobs1=people_per_group, alpha=0.05, power=0.8)
    # With an SD of 10 score points, convert to points
    print(people_per_group, "per group: effect size", round(effect, 2), "= about", round(effect * 10, 1), "points")

# Reverse question: people needed per group to detect effect size 0.5
needed = power_calculator.solve_power(effect_size=0.5, alpha=0.05, power=0.8)
print("needed per group for 0.5:", round(needed))
```
With 100 people per group the test can only reliably detect a gap of about 4 points; to detect 2 points you need about 400 per group. To detect half an SD (effect size 0.5) you need 64 per group.
**Likely follow-ups:** 1) *Is MDE the expected effect?* No, it is the smallest you care to catch. 2) *What if the sample is fixed?* Compute the MDE and decide if it is acceptable.
**Common mistakes:** Picking the MDE from what the data later shows; forgetting that a result smaller than MDE can easily be missed.

### Q71 ⭐ 🔴 How do you run and read a hypothesis test in Excel (Data Analysis ToolPak) at a high level?
**Asked at:** commonly asked (no company-specific report found); the ToolPak is a standard Excel add-in, steps below from standard Excel usage and not run in Excel here.
**What the interviewer is checking:** Can you run a test without code and read the output table?
**Say this in the interview:** "I enable the Analysis ToolPak, open Data, Data Analysis, pick the test such as t-Test: Two-Sample Assuming Unequal Variances, select the two columns and alpha, and read the output: the t Stat, the p-value (P two-tail) and whether t Stat is beyond the t Critical value."
**Explain simply:**
- Enable: File, Options, Add-ins, Manage Excel Add-ins, Go, tick "Analysis ToolPak" (Excel 2010 and later).
- Pick the test: t-Test (paired, equal variances, unequal variances), z-Test, F-Test, Anova (single or two-factor).
- Rule: if P(T<=t) two-tail is below alpha, or the absolute t Stat exceeds t Critical two-tail, reject the null.
- Use the **two-tail** line for "is there any difference"; one-tail only if you decided direction beforehand.
- The output is static numbers, not a formula, so it does not update when data changes.
**Worked example:** Tenure in years for two branches, 12 employees each, columns A and B. The table I expect, rebuilt in Python. As far as I know, the ToolPak rounds the degrees of freedom to a whole number (17.7 becomes 18).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Tenure in years for two branches (the two columns you would paste into Excel)
tenure_a = np.array([2.1, 3.5, 1.8, 4.2, 2.9, 3.1, 5.0, 2.4, 3.8, 2.2, 4.6, 3.3])
tenure_b = np.array([1.5, 2.8, 1.9, 2.2, 3.0, 1.7, 2.5, 2.1, 3.4, 1.6, 2.0, 2.7])

# The numbers the ToolPak table reports
variance_a, variance_b = tenure_a.var(ddof=1), tenure_b.var(ddof=1)
standard_error = np.sqrt(variance_a / 12 + variance_b / 12)
t_statistic = (tenure_a.mean() - tenure_b.mean()) / standard_error
degrees_of_freedom = (variance_a / 12 + variance_b / 12) ** 2 / (
    (variance_a / 12) ** 2 / 11 + (variance_b / 12) ** 2 / 11)
df_rounded = round(degrees_of_freedom)

print("Mean", round(tenure_a.mean(), 3), round(tenure_b.mean(), 3))
print("Variance", round(variance_a, 3), round(variance_b, 3))
print("t Stat", round(t_statistic, 3), "df", df_rounded)
print("P one-tail", round(stats.t.sf(t_statistic, df_rounded), 4), "t Critical one-tail", round(stats.t.ppf(0.95, df_rounded), 3))
print("P two-tail", round(2 * stats.t.sf(t_statistic, df_rounded), 4), "t Critical two-tail", round(stats.t.ppf(0.975, df_rounded), 3))
```
Mean A 3.242 vs B 2.283; t Stat 2.798 with 18 df; P two-tail 0.0119, below 0.05, and 2.798 exceeds 2.101, so branch A has longer tenure. Equivalent in a cell: `=T.TEST(A2:A13,B2:B13,2,3)` (Excel 2010+; type 3 is unequal variance) returns the p-value, close to 0.012 (it uses unrounded df, so not run here).
**Likely follow-ups:** 1) *Equal or unequal variances?* Default to unequal (Welch). 2) *Where is the effect size?* Not given; compute the difference and SD yourself.
**Common mistakes:** Choosing the one-tail p-value to get significance; ranges including the header row without ticking "Labels".

### Q72 ⭐ 🔴 What is bootstrapping and how can it be used for hypothesis testing?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** Do you grasp resampling from your own data when formulas are hard or assumptions fail?
**Say this in the interview:** "Bootstrapping means repeatedly resampling my data with replacement to see how much a statistic, like a mean difference, varies. The middle 95% of those results is a confidence interval; if it excludes zero, that supports a real difference. It needs few assumptions, which is handy for skewed data or medians."
**Explain simply:**
- **Resampling with replacement**: draw n values from your n values, so some repeat and some are missed.
- Repeat thousands of times and record the statistic each time.
- The spread of those results approximates the sampling variation.
- Works for medians, ratios, and other statistics with no easy formula.
- Weak with very small samples, because resampling cannot invent information that is not there.
**Worked example:** Tenure for two branches (12 each). Observed gap in mean tenure: 0.958 years.
**Excel / Python:**
```python
import numpy as np

# Tenure in years for two branches
tenure_a = np.array([2.1, 3.5, 1.8, 4.2, 2.9, 3.1, 5.0, 2.4, 3.8, 2.2, 4.6, 3.3])
tenure_b = np.array([1.5, 2.8, 1.9, 2.2, 3.0, 1.7, 2.5, 2.1, 3.4, 1.6, 2.0, 2.7])
observed_gap = tenure_a.mean() - tenure_b.mean()

# Redraw each branch 10,000 times WITH replacement and record the gap each time
random_generator = np.random.default_rng(10)
bootstrap_gaps = []
for _ in range(10000):
    resample_a = random_generator.choice(tenure_a, size=len(tenure_a), replace=True)
    resample_b = random_generator.choice(tenure_b, size=len(tenure_b), replace=True)
    bootstrap_gaps.append(resample_a.mean() - resample_b.mean())
bootstrap_gaps = np.array(bootstrap_gaps)

# 95% bootstrap interval: the middle 95% of the gaps
low, high = np.percentile(bootstrap_gaps, [2.5, 97.5])
print("observed gap", round(observed_gap, 3))
print("95% bootstrap interval", round(low, 2), "to", round(high, 2))
```
The bootstrap interval for the gap is 0.32 to 1.62 years. It excludes zero, so the gap is unlikely to be luck. (For comparison, the Welch t-test p-value on this data is 0.012.)
**Likely follow-ups:** 1) *How many resamples?* Typically 1,000 to 10,000. 2) *Bootstrap versus permutation?* Bootstrap gives intervals; permutation gives a p-value under the null (Q73).
**Common mistakes:** Resampling without replacement; bootstrapping a sample that is not representative.

### Q73 ⭐ 🔴 What is a permutation test and when would you use it?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** Can you describe a test built by shuffling labels?
**Say this in the interview:** "A permutation test asks: if branch made no difference, shuffling the branch labels at random should give gaps like the one I saw. I shuffle many times and see how often the fake gap is as large as the real one; that share is the p-value. I use it when assumptions like normality are doubtful or the statistic is unusual."
**Explain simply:**
- The null hypothesis says the labels are interchangeable, so shuffling them is allowed.
- Count the shuffles where the gap is at least as extreme as the real gap.
- p-value = that count divided by the number of shuffles.
- Works for small samples and any statistic (mean, median, correlation).
**Worked example:** The same tenure data: observed gap 0.958 years.
**Excel / Python:**
```python
import numpy as np

tenure_a = np.array([2.1, 3.5, 1.8, 4.2, 2.9, 3.1, 5.0, 2.4, 3.8, 2.2, 4.6, 3.3])
tenure_b = np.array([1.5, 2.8, 1.9, 2.2, 3.0, 1.7, 2.5, 2.1, 3.4, 1.6, 2.0, 2.7])
observed_gap = tenure_a.mean() - tenure_b.mean()

# Pool everyone, shuffle the branch labels, and re-measure the gap 10,000 times
random_generator = np.random.default_rng(10)
everyone = np.concatenate([tenure_a, tenure_b])
as_extreme_count = 0
for _ in range(10000):
    shuffled = random_generator.permutation(everyone)
    fake_gap = shuffled[:12].mean() - shuffled[12:].mean()
    if abs(fake_gap) >= abs(observed_gap):
        as_extreme_count += 1

# Share of shuffles with a gap at least as big as the real one = p-value
print("observed gap", round(observed_gap, 3))
print("permutation p-value", as_extreme_count / 10000)
```
Only about 0.9% of random shuffles gave a gap as big as the real one, so p is about 0.009, in line with the t-test (0.012).
**Likely follow-ups:** 1) *Difference from bootstrap?* Shuffles labels under the null instead of resampling. 2) *Disadvantage?* Needs exchangeable data and computation.
**Common mistakes:** Using it for paired data without shuffling within pairs; too few shuffles (the p-value then jumps around).

### Q74 ⭐ 🔴 Why can we reject the null with statistical significance yet see no business impact? Give an HR example.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you separate "unlikely to be chance" from "big enough to matter"?
**Say this in the interview:** "With a very large sample, even a tiny gap becomes statistically significant, because the test can detect almost any difference. But significance says the effect is probably not zero, not that it is useful. I check the effect size and the cost and benefit before recommending anything."
**Explain simply:**
- The p-value shrinks as the sample grows, even if the effect stays tiny (Q19, Q50).
- **Practical significance** asks if the change is big enough to justify the cost.
- Report the effect size and the confidence interval, not only the p-value (Q44).
- Agree beforehand what "meaningful" means, for example a 3-point rise.
**Worked example:** A wellness app for a big company: 50,000 employees in each group, engagement on a 0-100 scale (made up).
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Engagement score (0-100) before and after a new wellness app: 50,000 employees per group
random_generator = np.random.default_rng(21)
scores_old = random_generator.normal(72.0, 12, 50000)
scores_new = random_generator.normal(72.3, 12, 50000)

result = stats.ttest_ind(scores_new, scores_old)
gap = scores_new.mean() - scores_old.mean()
print("gap in points", round(gap, 2), "p-value", round(result.pvalue, 5))
print("effect size (gap / SD)", round(gap / 12, 3))
```
The gain of 0.27 points is highly significant (p = 0.00045), but the effect size of 0.022 SD is negligible. If the app costs crores to run, it is not worth it for that.
**Likely follow-ups:** 1) *What would you recommend?* Do not roll out on this evidence. 2) *What is the opposite case?* A big effect that is not significant because of small samples (Q65).
**Common mistakes:** Celebrating "p < 0.05" in a report with no effect size.

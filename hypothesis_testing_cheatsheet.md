# Hypothesis Testing Cheat Sheet for Data Science Interviews

**Prepared for:** Dhyanendra Singh
**How to use this file:** Each test follows the same layout so you can compare them easily. Notes marked with a star are your own counter questions from practice. They are the points you found tricky, so revise them first.

---

## The Universal Logic of Every Test

1. Assume the **null hypothesis (H0)** is true. It always says "no difference" or "no relationship".
2. The **alternative hypothesis (H1)** says there is a difference or relationship.
3. Compute a **test statistic**: the actual gap divided by the gap you would expect from pure chance.
4. Convert the test statistic into a **p-value**: the probability of seeing a result at least this extreme if H0 were true.
5. Decide:
   - **p-value below 0.05 (smaller):** the result is unlikely under H0, so **reject H0** and conclude there is a statistically significant difference.
   - **p-value above 0.05 (larger):** the evidence is not strong enough, so **fail to reject H0**. This does not prove there is no difference.

**Wording tips**
- Say "reject the null", not "accept the alternative".
- Say "fail to reject the null", not "accept the null".
- "Significant" means unlikely to be random. It does not mean large or useful, so always report the size of the gap too.

> **★ Important (your question):** The p-value is the probability of seeing a difference this large if there were truly no difference. It is not the probability that H0 is true.

---

## Quick Decision Guide

| Situation | Test to use |
|---|---|
| One group of numbers vs a fixed target | One-sample t-test (or Wilcoxon signed-rank if not normal) |
| Two independent groups, numeric outcome | Two-sample t-test, preferably Welch (or Mann-Whitney U if not normal) |
| Same subjects measured twice, numeric outcome | Paired t-test (or Wilcoxon signed-rank if not normal) |
| Three or more groups, numeric outcome | ANOVA (or Welch ANOVA, or Kruskal-Wallis if not normal) |
| Two independent groups, yes/no outcome | Two-proportion z-test (or Fisher's exact if counts are small) |
| Two categorical variables, are they related? | Chi-square test of independence (or Fisher's exact if small) |
| Same subjects, yes/no outcome measured twice | McNemar's test |
| Is my data normal? | Shapiro-Wilk test and Q-Q plot |
| Do my groups have equal variance? | Levene's test |
| Do two distributions differ? | Kolmogorov-Smirnov test |
| Relationship between two numeric variables | Pearson or Spearman correlation |
| Many tests at once | Bonferroni or Benjamini-Hochberg correction |
| No assumptions wanted | Bootstrap or permutation test |

---

# PART A: Tests for Numeric Outcomes

---

## 1. One-Sample t-test

**When to use:** You have one group of continuous measurements and want to know whether its true average differs from a known or target value.

**Hypotheses**
- H0: the true average equals the target value.
- H1: the true average does not equal the target value.

**How it works:** It measures how far your sample average is from the target, in units of standard errors. A big distance means the gap is unlikely to be luck.

**Formula**
- t = (sample mean minus target) divided by (s divided by square root of n)
- s is the sample standard deviation, n is the sample size.
- Degrees of freedom = n minus 1.

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| Data is continuous | Look at the data type |
| Observations are independent | Think about how the data was collected |
| Data is roughly normal, or sample is large (30 or more) | Shapiro-Wilk test, Q-Q plot |
| No extreme outliers | Box plot |

**If assumptions fail:** Use the **Wilcoxon signed-rank test**, or a bootstrap test.

**Example**
Your salary detection pipeline is promised to take 200 ms per transaction on average. You time 50 random transactions and get an average of 215 ms, with a standard deviation of 30.
- Standard error = 30 / square root of 50 = about 4.24
- t = (215 minus 200) / 4.24 = about 3.5
- A t of 3.5 is far from zero, so the p-value is tiny. Reject H0: the true average is probably not 200.

**What the p-value tells you**
- Below 0.05: the true average differs from the target.
- Above 0.05: not enough evidence of a difference.

> **★ Important (your question):** The 200 ms is the average time for a **single transaction**. It is not "how many transactions are processed per time period". That would be throughput, a different metric.

> **★ Important (your question):** "One sample" does not mean one transaction. It means **one group of measurements compared with one fixed number**. Taking another 50 would give a slightly different average, but you do not need to repeat the experiment. The standard error already measures that wiggle, estimated from the spread of your single sample.

> **★ Important (your question):** You are not testing whether your 50 transactions averaged 200 (you can see they averaged 215). You are testing whether the **true average across all transactions** is 200, given what the 50 show.

---

## 2. Two-Sample t-test (Welch's version preferred)

**When to use:** You compare the averages of two **independent** groups on a continuous measure. There is no fixed target. Both sides are estimated from data.

**Hypotheses**
- H0: the two groups have the same true average.
- H1: the two groups have different true averages.

**How it works:** It divides the gap between the two sample averages by the expected random gap, which combines the uncertainty of both groups.

**Formula (Welch)**
- t = (mean1 minus mean2) divided by square root of (s1 squared / n1 plus s2 squared / n2)

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| Continuous data | Data type |
| Independent observations, and groups independent of each other | Study design (watch for transactions from the same customer) |
| Roughly normal in each group, or large samples | Shapiro-Wilk, Q-Q plot |
| Similar variance in both groups (for the standard version) | Levene's test |
| No extreme outliers | Box plot |

**If assumptions fail**
- Unequal variance: use **Welch's t-test** (many people use it by default).
- Not normal with small samples: use the **Mann-Whitney U test**, or a bootstrap test.

**Example**
You time 50 transactions on the old pipeline (average 215 ms) and 50 different transactions on the new one (average 190 ms). Is the 25 ms gap real? If the t-statistic is large and p is below 0.05, the new version is truly faster.

**What the p-value tells you**
- Below 0.05: the group averages truly differ.
- Above 0.05: the gap could easily be random variation.

> **★ Important (your question):** One-sample vs two-sample. In one-sample, one side is a fixed number with no uncertainty. In two-sample, **both sides are estimated from data**, so both carry uncertainty.

> **★ Important (your question):** "If the data is not normal, can I still use a t-test?" With a large sample (30 or more per group), mostly yes, because of the central limit theorem. With small, clearly skewed samples or heavy outliers, no. Use Mann-Whitney U instead.

---

## 3. Paired t-test

**When to use:** The **same subjects** are measured twice (before and after), so each value has a natural partner.

**Hypotheses**
- H0: the true average difference is zero.
- H1: the true average difference is not zero.

**How it works:** Compute the difference within each pair, then run a one-sample t-test on those differences against zero.

**Formula**
- d = value 1 minus value 2 for each pair
- t = mean of d divided by (standard deviation of d / square root of n)

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| The differences are roughly normal | Shapiro-Wilk on the differences, Q-Q plot |
| Pairs are independent of each other | Study design |
| Continuous data | Data type |

**If assumptions fail:** Use the **Wilcoxon signed-rank test**.

**Example**
You time the same 50 transactions on the old and the new pipeline. Compute old minus new for each transaction and test whether the average difference is zero. Another example: the same customers' spending before and after a campaign.

**What the p-value tells you**
- Below 0.05: there is a real average change.
- Above 0.05: no convincing evidence of change.

> **★ Important (your question): Why not a two-sample t-test for paired data?**
> - Some transactions are naturally slow (large or complex), others fast. That big spread makes both groups noisy, and a small real saving (say 10 ms) gets buried, so the p-value stays high.
> - In the paired version each transaction is compared with itself. The size effect cancels out, leaving a clean, consistent 10 ms saving. The test is much more powerful.
> - A two-sample test also assumes independent groups. Measuring the same transactions twice makes them dependent, which breaks that assumption.
> - **Rule:** same subjects measured twice means paired. Different subjects in each group means two-sample.

---

## 4. One-Way ANOVA (Analysis of Variance)

**When to use:** You compare the averages of **three or more independent groups** on a continuous measure.

**Hypotheses**
- H0: all group averages are equal.
- H1: at least one group average is different.

**How it works:** It compares the spread **between** group averages with the natural spread **within** each group. The ratio is the F-statistic. If groups truly differ, between-group spread is large relative to within-group spread, so F is big.

**Formula**
- F = (variation between groups / degrees of freedom between) divided by (variation within groups / degrees of freedom within)
- Equivalent: F = mean square between divided by mean square within.

**Why not many t-tests?** Each test has a 5% chance of a false alarm. Running several piles those chances up, so you find fake differences too often. ANOVA tests everything in one go.

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| Independent observations | Study design |
| Roughly normal within each group | Shapiro-Wilk, Q-Q plot |
| Equal variance across groups | Levene's test |

**If assumptions fail**
- Unequal variance: **Welch's ANOVA**, with **Games-Howell** as the follow-up.
- Not normal and small samples: **Kruskal-Wallis test**.

**Example**
You compare average call duration across leads from LinkedIn, referral, and organic. ANOVA tells you whether at least one source differs.

**What the p-value tells you**
- Below 0.05: at least one group differs. It does **not** tell you which one. Follow up with a post-hoc test such as **Tukey's**.
- Above 0.05: no evidence the group averages differ.

---

## 5. Mann-Whitney U Test (Wilcoxon Rank-Sum)

**When to use:** Two independent groups, numeric or ordinal data, but the data is skewed, has big outliers, or the sample is too small to trust normality. It is the non-parametric alternative to the two-sample t-test.

**Hypotheses**
- H0: a randomly picked value from one group is equally likely to be higher or lower than one from the other group.
- H1: one group tends to have larger values.

**How it works**
1. **Pool all values from both groups into one combined list** and sort smallest to largest.
2. Assign ranks 1, 2, 3, ... across everyone (ties share the average rank).
3. Add up the ranks within each group (the **rank sum**).
4. Compare each group's rank sum with what you would expect if the groups were identical.
5. Convert the statistic to a z-score and p-value.

**Formula**
- U1 = R1 minus n1(n1 + 1)/2, where R1 is the rank sum of group 1 and n1 its size.
- Expected rank sum for group 1 under H0 = n1 times (N + 1)/2, where N is the total number of observations.
- Example: a group of 40 among 100 total is expected to have a rank sum of 40 times 50.5 = 2,020.

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| Independent observations | Study design |
| Numeric or ordinal data | Data type |
| Similar distribution shapes (if you want to interpret it as a difference in medians) | Histograms |
| No normality assumption | Not needed |

**If assumptions fail:** If shapes differ a lot, interpret it only as "one group tends to be larger", or use a permutation or bootstrap test.

**Example**
Compare transaction amounts of salaried customers (steady amounts) with freelancers (spiky amounts, a few huge transfers). Ranking means one giant transfer is just "the highest rank", not a distortion.

**What the p-value tells you**
- Below 0.05: one group tends to have larger values.
- Above 0.05: no evidence the groups differ.

> **★ Important (your question):** Ranking is done on the **pooled** list from both groups together, **not** by sorting each group separately.

> **★ Important (your question):** We use the **sum** of ranks, not the average. This is fine because the expected rank sum depends only on group size and total count, and it handles unequal group sizes cleanly (a bigger group naturally has a bigger sum, so we compare against the expected sum for that size).

> **★ Important (your question):** The trade-off: it is slightly less powerful than the t-test when the data really is normal. If the data were normal, use the **two-sample t-test (Welch)** instead.

---

## 6. Wilcoxon Signed-Rank Test

**When to use:** Paired measurements (or one sample vs a target) where the differences are skewed or have outliers. It is the non-parametric alternative to the paired t-test and the one-sample t-test.

**Hypotheses**
- H0: the typical (median) difference is zero.
- H1: the typical difference is not zero.

**How it works**
1. Compute the difference for each pair. Drop pairs with a difference of exactly zero.
2. Ignore signs and rank the differences by absolute size (smallest gets rank 1, ties share the average rank).
3. Put the signs back on the ranks.
4. Add up the positive ranks and the negative ranks separately.
5. If nothing changed, the two sums should be about equal. If one side dominates, the p-value gets small.

**Formula**
- W = the smaller of (sum of positive ranks, sum of negative ranks), then converted to a z-score for larger samples.

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| Pairs are independent | Study design |
| Differences are roughly symmetric around their median | Histogram of differences |
| Numeric or ordinal data | Data type |

**If assumptions fail:** Use the **sign test**, which only needs the direction of each change, or a bootstrap test.

**Simple worked example**
Old times: 100, 120, 90, 110, 105. New times: 95, 118, 85, 100, 106.
- Differences (old minus new): 5, 2, 5, 10, negative 1.
- Ranks by size: 1 gets rank 1, 2 gets rank 2, the two 5s share ranks 3 and 4 so each gets 3.5, and 10 gets rank 5.
- Signed: only the negative 1 is negative.
- Positive rank sum = 2 + 3.5 + 3.5 + 5 = 14. Negative rank sum = 1.
- The positive side dominates, suggesting the new version is faster. With only five pairs the p-value is borderline, but that is the idea.

**What the p-value tells you**
- Below 0.05: there is a real shift between the paired measurements.
- Above 0.05: no convincing evidence of change.

> **★ Important (your question):** Mann-Whitney ranks **pooled values from two independent groups**. Wilcoxon signed-rank ranks the **paired differences within the same subjects**. If the differences were normal, use the **paired t-test** instead.

---

## 7. Kruskal-Wallis Test

**When to use:** Three or more independent groups, skewed data, outliers, or small samples. It is the non-parametric alternative to one-way ANOVA, and Mann-Whitney extended to many groups.

**Hypotheses**
- H0: all groups come from the same distribution (no group tends to be larger).
- H1: at least one group tends to have larger or smaller values.

**How it works**
1. Pool all values from all groups and rank them.
2. Compute the rank sum (or average rank) within each group.
3. Compare each group's rank sum with what you would expect if groups were identical.
4. Combine the gaps into one statistic, **H**, and convert to a p-value using the chi-square distribution.

**Formula**
- H = [12 / (N(N + 1))] times the sum over groups of (Ri squared / ni), minus 3(N + 1)
- Ri is the rank sum of group i, ni its size, and N the total number of observations. H is compared with a chi-square distribution with (number of groups minus 1) degrees of freedom.

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| Independent observations | Study design |
| Numeric or ordinal data | Data type |
| Similar shapes if you interpret as medians | Histograms |

**If assumptions fail:** Use a permutation test. If the data turns out to be normal with equal variance, use ANOVA.

**Example**
Compare transaction amounts across salaried, freelancers, and business owners. The amounts are heavily skewed, so ANOVA assumptions are shaky.

**What the p-value tells you**
- Below 0.05: at least one group differs. Follow up with **Dunn's test** to find which pairs differ.
- Above 0.05: no evidence of difference.

---

# PART B: Tests for Yes/No and Category Data

---

## 8. Two-Proportion z-test

**When to use:** You compare the rate of a yes/no outcome between **two independent groups**, like A/B test conversion.

**Hypotheses**
- H0: both groups have the same true rate.
- H1: the true rates differ.

**How it works (three steps to get the statistic)**
1. **Pool** both groups to get one shared rate. This is what H0 assumes.
2. Use that shared rate and the two sample sizes to compute the **expected random gap** (the standard error).
3. Divide the **actual gap** by the expected random gap. That is the **z-score**.
Then convert the z-score to a p-value using the standard normal curve.

**Formula**
- Pooled rate p = (x1 + x2) / (n1 + n2)
- Standard error = square root of [ p(1 minus p) times (1/n1 + 1/n2) ]
- z = (p1 minus p2) / standard error

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| Independent groups, each lead counted once | Study design |
| Large enough samples: about 10 or more expected successes and 10 or more expected failures per group | Compute expected counts |

**If assumptions fail:** Small counts: **Fisher's exact test**. Same subjects in both groups: **McNemar's test**.

**Example**
Old manual scoring: 5,000 leads, 600 convert (12%). New model: 5,000 leads, 700 convert (14%).
- Pooled rate = 1,300 / 10,000 = 13%.
- The standard error from that pooled rate and the sample sizes is about 0.67 percentage points.
- z = 2 points / 0.67 = about 3. The p-value is about 0.003, so reject H0: the new model truly converts better.

**What the p-value tells you**
- Below 0.05: the rates truly differ.
- Above 0.05: the gap could be luck.

> **★ Important (your question): Why pool and get 13%?** Under H0 both groups share one true rate, so the best estimate of it is the combined data. We do **not** compare 12% or 14% with 13%. We use 13% only to calculate how big a gap pure chance would create (the standard error). Then we compare the **actual gap between the two groups** (2 points) with that expected random gap.

> **★ Important (your question): Why not a t-test for conversion?** A t-test is for continuous measurements where spread varies freely. Conversion is a one or a zero per lead, so you are comparing rates, and the spread is fixed by the rate itself. The proportion test builds that in. With very large samples a t-test on zeros and ones gives almost the same answer, but the proportion test is cleaner and more defensible.

> **★ Important (your question):** Three steps recap: pool to get the shared rate, compute the expected random gap, divide the actual gap by it to get z. Then convert z to a p-value and compare with 0.05.

---

## 9. Chi-Square Test of Independence

**When to use:** You have **two categorical variables** and want to know whether they are related.

**Hypotheses**
- H0: the two variables are independent.
- H1: they are related.

**How it works**
1. Build a cross table (contingency table) of **observed** counts.
2. Compute the **expected** counts: what you would see if the variables were unrelated.
3. For each cell, compute (observed minus expected) squared, divided by expected. Add them all up to get the chi-square statistic.
4. Convert it to a p-value using the chi-square distribution.

**Formula**
- Expected count for a cell = (row total times column total) / grand total
- Chi-square = sum over all cells of (O minus E) squared / E
- Degrees of freedom = (rows minus 1) times (columns minus 1)

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| Independent observations | Study design |
| Expected counts at least about 5 in each cell | Compute expected counts |
| Data are counts, not percentages | Data type |

**If assumptions fail:** Use **Fisher's exact test** (small counts) or **McNemar's test** (paired data).

**Example**
3,000 leads: website 1,000 leads with 100 conversions, referral 1,000 with 200, ads 1,000 with 120. Overall, 420 out of 3,000 converted, which is 14%.
- Expected conversions per source if source did not matter: 14% of 1,000 = 140.
- Observed: 100, 200, 120 versus expected 140 each. Large gaps mean a large chi-square and a small p-value, so source and conversion are related.

**What the p-value tells you**
- Below 0.05: the variables are related.
- Above 0.05: no evidence of a relationship.

> **★ Important (your question): How exactly do we get the expected value?**
> - Overall conversion rate = 420 / 3,000 = 14%. This ignores source completely.
> - If source has no effect, every source should convert at the same 14%.
> - LinkedIn with 1,000 leads: expected conversions = 14% of 1,000 = 140, expected non-conversions = 860.
> - If LinkedIn actually had 200 conversions, that is the **observed** value. The gap between 200 and 140 is the evidence that LinkedIn behaves differently.
> - Shortcut formula: row total times column total divided by grand total. For LinkedIn conversions: 1,000 times 420 divided by 3,000 = 140.

> **★ Important (your question):** The related **G-test** uses a likelihood ratio instead and is used in the same situations. It is sometimes preferred with small counts.

---

## 10. Fisher's Exact Test

**When to use:** Two categorical variables with a **small sample**, where chi-square's approximation breaks down (expected counts below 5).

**Hypotheses**
- H0: the two variables are independent.
- H1: they are related.

**How it works:** It skips the approximation. Given fixed row and column totals, it counts exactly how many possible tables could occur, and calculates the exact probability of getting a table as lopsided as yours (or more) by chance.

**Formula (2 by 2 table)**
- The probability of a specific table is a hypergeometric probability: (a+b choose a) times (c+d choose c) divided by (n choose a+c). The p-value sums this over all tables as extreme or more extreme.

**Assumptions and how to check them:** Independent observations, fixed margins. No expected-count rule, which is the whole point.

**If assumptions fail:** Paired data: **McNemar's test**. For large samples it agrees with chi-square anyway.

**Example**
A pilot of a new outreach script: 20 leads get the new script (8 convert, 12 do not), 20 get the old script (2 convert, 18 do not). With so few leads, Fisher's test checks whether such a lopsided table could easily happen by luck.

**What the p-value tells you**
- Below 0.05: the script and conversion are related.
- Above 0.05: could easily be luck.

---

## 11. McNemar's Test

**When to use:** A **yes/no outcome measured twice on the same subjects** (paired). It is the paired version of the two-proportion test.

**Hypotheses**
- H0: the rate of "yes" is the same before and after (the two disagreement counts are equal).
- H1: the rates differ.

**How it works:** Build a 2 by 2 table of paired results. Cases where both said yes or both said no tell you nothing. Only the **disagreements** matter. If the models were equivalent, disagreements would split about 50-50.

**Formula**
- Chi-square = (b minus c) squared / (b + c), where b and c are the two disagreement counts. Compared with a chi-square distribution with 1 degree of freedom.

**Assumptions and how to check them:** Paired yes/no data, independent pairs, and enough disagreements (b + c of about 25 or more, otherwise use the exact version).

**If assumptions fail:** With few disagreements, use the **exact binomial version** of McNemar's test.

**Example**
200 transactions, each classified by the old and the new model. Only the new model flagged 30, only the old model flagged 10. Chi-square = (30 minus 10) squared / 40 = 400 / 40 = 10. That gives p well below 0.05, so the models flag differently.

**What the p-value tells you**
- Below 0.05: the two models' flag rates differ.
- Above 0.05: no evidence they differ.

> **★ Important (your question):** McNemar's works only on **binary (yes/no)** outcomes, and **always with two paired answers per subject** (old model says yes/no, new model says yes/no). It is not like a one-sample test. A single set of yes/no answers compared with a fixed rate (like 10%) would be a **one-sample proportion test**.

> **★ Important (your question):** Rule of thumb. Yes/no, two independent groups: two-proportion z-test. Yes/no, same subjects twice: McNemar's. More than two categories in the same paired setup: Stuart-Maxwell test (rare).

---

# PART C: Assumption-Checking Tests

---

## 12. Shapiro-Wilk Test (Normality Check)

**When to use:** Before a t-test or ANOVA, to check whether data (or paired differences) look normally distributed.

**Hypotheses**
- H0: the data comes from a normal distribution.
- H1: it does not.

**How it works:** It compares the sorted data with what perfectly normal data would look like. The statistic W is close to 1 for normal data.

**What the p-value tells you (note the reversed logic)**
- **Above 0.05: good news.** No strong evidence against normality, so the t-test is reasonable.
- **Below 0.05:** the data is not normal. Switch to Mann-Whitney, Wilcoxon, or Kruskal-Wallis.

**Cautions**
- Very large samples (thousands of rows): flags tiny, harmless deviations, so it keeps rejecting.
- Very small samples: little power to detect non-normality.
- Always pair it with a **Q-Q plot**, where normal data falls along a straight line.

**Example:** 40 call durations from one source. Shapiro-Wilk p = 0.30 means the t-test is reasonable. p = 0.01 means switch to a non-parametric test.

---

## 13. Levene's Test (Equal Variance Check)

**When to use:** Before a two-sample t-test or ANOVA, to confirm that groups have a similar spread.

**Hypotheses**
- H0: all groups have the same variance.
- H1: at least one group has a different variance.

**How it works:** It measures how far each value is from its own group's center, then tests whether those distances differ between groups.

**What the p-value tells you (reversed logic again)**
- **Above 0.05: good news.** Equal variance looks fine, so use the standard t-test or ANOVA.
- **Below 0.05:** variances are unequal. Use **Welch's t-test** (two groups) or **Welch's ANOVA** (three or more), with **Games-Howell** as the follow-up.

**Notes:** Many practitioners skip the check and use Welch's by default. Levene's is more robust than **Bartlett's test**, which breaks easily when data is not normal.

**Example:** Call durations from source A are consistently 4 to 6 minutes, while source B ranges from 1 to 15 minutes. The averages may look similar, but the spreads differ. Levene's test flags that.

> **★ Important (your question):** If the equal variance assumption fails, you cannot use the **standard** two-sample t-test or ANOVA, but you can still use their Welch versions. If normality **also** fails with small samples, move to Mann-Whitney U (two groups) or Kruskal-Wallis (three or more).

---

# PART D: More Tests Used in Industry

*These tests are not discussed yet in practice, so there are no starred notes here. Add your counter questions after we cover each one.*

---

## 14. Kolmogorov-Smirnov (KS) Test

**When to use:** Compare two samples of a continuous feature (for example training data vs last month's data), or compare one sample with a reference distribution. Very common for **data drift** detection in deployed models.

**Hypotheses**
- H0: both samples come from the same distribution.
- H1: the distributions differ (in location, spread, or shape).

**How it works:** For each sample, build the cumulative distribution curve (the share of values at or below each point). Find the **largest vertical gap** between the two curves. That maximum gap is the KS statistic. A big gap means the samples are unlikely to come from the same distribution.

**Formula**
- D = the maximum over all x of the absolute difference between F1(x) and F2(x), where F1 and F2 are the two empirical cumulative distribution functions.
- The p-value comes from the known distribution of D under H0, which depends on the two sample sizes.

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| Continuous data (few or no ties) | Look at the data type and count repeated values |
| Independent observations | Study design (watch for the same customer appearing many times) |
| The two samples are independent of each other | Study design |
| No normality assumption | Not needed |

**If assumptions fail**
- Categorical or discrete features: use the **Population Stability Index (PSI)** or the **chi-square test**.
- Very large samples, where tiny harmless shifts become significant: also report an effect size such as the KS statistic D itself, or use PSI.
- Want a test more sensitive to the tails: use the **Anderson-Darling test**.

**Examples**
1. Your salary detection model was trained on transaction amounts from years ago. You compare them with last month's amounts. A large D with p below 0.05 says the amount feature has drifted, so consider retraining.
2. You compare time-to-first-call between two lead sources to see if the whole distribution differs, not just the average.

**What the p-value tells you**
- **Below 0.05 (smaller):** the distributions differ, so there is evidence of drift.
- **Above 0.05 (larger):** no evidence of a difference.
- With huge samples the p-value is almost always tiny, so look at D as well. A small D means the shift is real but minor.

**PSI quick reference (for drift monitoring):** Bin the feature into about 10 buckets, then compare the percentage of data per bucket. Below 0.1 is stable, 0.1 to 0.2 is a moderate shift, above 0.2 is significant drift.

---

## 15. Correlation Tests (Pearson and Spearman)

**When to use:** Test whether two numeric variables are related, for example whether time-to-first-call is related to lead score.

**Hypotheses (for both)**
- H0: the true correlation is zero (no relationship).
- H1: the true correlation is not zero.

**How it works**
- **Pearson** measures the strength of a **linear** relationship, from negative 1 (perfect downhill line) through 0 (no linear relationship) to positive 1 (perfect uphill line).
- **Spearman** first replaces each value by its rank, then computes Pearson on the ranks. It measures any **monotonic** relationship, meaning consistently rising or consistently falling, even if curved.

**Formulas**
- Pearson r = covariance of X and Y divided by (standard deviation of X times standard deviation of Y).
- Test statistic: t = r times square root of (n minus 2), divided by square root of (1 minus r squared), with n minus 2 degrees of freedom.
- Spearman rho = Pearson r computed on the ranks. For no ties, rho = 1 minus [6 times the sum of squared rank differences] / [n times (n squared minus 1)].

**Assumptions and how to check them**

| Assumption | Pearson | Spearman | How to check |
|---|---|---|---|
| Numeric (continuous) data | Yes | Numeric or ordinal | Data type |
| Independent observations | Yes | Yes | Study design |
| Linear relationship | Yes | Not needed (monotonic is enough) | Scatter plot |
| Roughly normal variables, for the p-value | Yes | Not needed | Shapiro-Wilk, Q-Q plot |
| No extreme outliers | Sensitive | Robust | Box plot, scatter plot |

**If assumptions fail:** Use **Spearman** instead of Pearson. For very small samples or many ties, use **Kendall's tau**. For a categorical variable against a numeric one, use a t-test or ANOVA instead. For two categorical variables, use chi-square.

**Examples**
1. Hours until first call vs lead score: r = negative 0.45 with p below 0.05 says faster calls go with higher scores, and the link is moderately strong.
2. Transaction amount vs account age, where amounts are heavily skewed: use Spearman, so a few giant transfers do not distort the answer.

**What the p-value tells you**
- **Below 0.05 (smaller):** the correlation is unlikely to be exactly zero, so a relationship exists.
- **Above 0.05 (larger):** no evidence of a relationship.
- The p-value says nothing about **strength** (look at r) and nothing about **causation**. With big samples, a tiny r like 0.03 can be "significant" but useless.

---

## 16. Multiple Testing Corrections (Bonferroni and Benjamini-Hochberg)

**When to use:** You run **many tests at once**, for example checking 50 features against a target, or comparing many pairs of groups after ANOVA. At a 5% threshold, about 1 in 20 tests looks significant purely by chance.

**Hypotheses:** Each individual test keeps its own H0 and H1. The correction changes the **threshold** you compare the p-values against (or adjusts the p-values themselves).

**How it works**
- **Bonferroni:** divide your threshold by the number of tests. It is simple and very strict, and it controls the chance of even **one** false positive (the family-wise error rate).
- **Benjamini-Hochberg (BH):** controls the **false discovery rate**, meaning the expected share of false positives among the results you call significant. It is less strict and more powerful, so it is popular for feature screening and genomics.

**Formulas**
- Bonferroni: adjusted threshold = alpha / m, where m is the number of tests. Equivalent: adjusted p = p times m (capped at 1).
- Benjamini-Hochberg:
  1. Sort the m p-values from smallest to largest, so the smallest has rank 1.
  2. For each p-value at rank i, compute the critical value (i / m) times q, where q is your accepted false discovery rate (for example 0.05).
  3. Find the largest rank where the p-value is at or below its critical value. That test and all tests with smaller p-values are called significant.

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| Each underlying test is valid | Check each test's own assumptions |
| Bonferroni: none beyond that, but it is conservative when tests are correlated | Look at correlation among your features |
| BH: tests are independent or positively dependent | Think about how tests are related |

**If assumptions fail**
- Bonferroni too strict and you lose real findings: use **Holm's method** (always at least as powerful as Bonferroni) or **Benjamini-Hochberg**.
- Tests with unusual dependence: use **Benjamini-Yekutieli**.

**Examples**
1. You test 20 features and one has p = 0.03. Without correction it looks significant. With Bonferroni the threshold is 0.05 / 20 = 0.0025, so it is not significant.
2. You screen 1,000 features and want a manageable list with at most about 5% false leads. Use Benjamini-Hochberg.

**What the p-value tells you**
- **Below the corrected threshold (smaller):** still significant after accounting for the number of tests.
- **Above the corrected threshold (larger):** could easily be a fluke from running many tests, even if it was below 0.05 on its own.

---

## 17. Bootstrap and Permutation Tests

**When to use:** When assumptions of the standard tests fail, when the statistic is unusual (a median, a ratio, an F1 score, a percentile), or when you simply want a test with almost no distribution assumptions. Very popular in modern A/B testing.

**Hypotheses**
- Same as the test they replace. For comparing two groups, H0: the groups do not differ. H1: they do.

**How it works**
- **Permutation test (for hypothesis tests):** Under H0 the group labels do not matter. So shuffle the labels randomly thousands of times, recompute the difference each time, and see how often a gap as large as the real one appears. That fraction is the p-value.
- **Bootstrap (for confidence intervals and uncertainty):** Resample your own data **with replacement** thousands of times, compute the statistic each time, and use the spread of those results to build a confidence interval.

**Formulas**
- Permutation p-value = (number of shuffles with a statistic at least as extreme as the real one + 1) / (number of shuffles + 1).
- Bootstrap 95% confidence interval: take the 2.5th and 97.5th percentiles of the bootstrapped statistics.
- If the 95% interval for a difference does not contain zero, that is evidence of a real difference.

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| Observations are independent (or resampling respects the dependence structure) | Study design |
| The sample is representative of the population | Sampling method |
| Enough data to represent the population (very tiny samples are fragile) | Sample size, stability across repeated runs |
| No normality assumption | Not needed |

**If assumptions fail**
- Dependent data such as time series or repeated customers: use a **block bootstrap** or resample by customer (**cluster bootstrap**).
- Very small samples: results are unreliable with any method, so collect more data or use an exact test.

**Examples**
1. Compare the **median** transaction amount of two segments. Shuffle segment labels 10,000 times. If a gap as big as the real one appears in only 1% of shuffles, p = 0.01.
2. Report a confidence interval for your model's F1 score: resample the test set 5,000 times, compute F1 each time, and take the 2.5th and 97.5th percentiles.

**What the p-value tells you**
- **Below 0.05 (smaller):** a gap this large rarely appears by shuffling, so the groups truly differ.
- **Above 0.05 (larger):** such gaps appear easily by chance, so no evidence of a difference.
- More shuffles give a more stable p-value (10,000 is a common choice).

---

## 18. Power Analysis and Sample Size Calculation

**When to use:** **Before** running an experiment such as an A/B test, to decide how many observations you need. It is a planning tool, not a test run on the results.

**Hypotheses:** It uses the H0 and H1 of the test you plan to run. For a two-proportion test, H0: both rates are equal. H1: they differ by at least the effect size you care about.

**How it works:** Four linked quantities. Fix three and solve for the fourth.
- **Significance level (alpha):** the false positive rate you accept, usually 0.05.
- **Power:** the chance of detecting a real effect if it exists, usually 80%.
- **Effect size:** the smallest difference you care about detecting, for example 12% to 14% conversion.
- **Sample size:** how many observations per group.

**Formula (two proportions, per group)**
- n = [ (z for alpha/2 + z for power) squared times (p1(1 minus p1) + p2(1 minus p2)) ] / (p1 minus p2) squared
- With alpha = 0.05 (z = 1.96) and power = 80% (z = 0.84), the sum of the two z values squared is about 7.85.
- For two means: n = 2 times (z for alpha/2 + z for power) squared times sigma squared / (difference) squared, where sigma is the standard deviation.

**Assumptions and how to check them**

| Assumption | How to check |
|---|---|
| A realistic baseline rate or standard deviation | Use historical data |
| A meaningful minimum effect size, decided with the business | Discuss with stakeholders |
| The planned test's own assumptions hold | Check that test's assumptions |

**If assumptions fail:** If you are unsure of the baseline or variance, run a small pilot to estimate them, or use **simulation-based power analysis**, where you generate fake data with the assumed effect many times and count how often your test detects it.

**Example**
You want to detect a lift from 12% to 14% conversion with 80% power at 5% significance.
- p1(1 minus p1) = 0.12 times 0.88 = 0.1056. p2(1 minus p2) = 0.14 times 0.86 = 0.1204. Sum = 0.226.
- n = 7.85 times 0.226 / (0.02 squared) = 1.774 / 0.0004 = about 4,435 leads per group.
- So you need roughly 4,400 or more leads in each group. With only 500 per group the test would likely miss a real lift.

**What the results tell you**
- **Larger required sample size:** happens when the effect you want to detect is smaller, the baseline variance is higher, or you want more power. Halving the effect size roughly **quadruples** the sample needed.
- **Smaller required sample size:** happens with larger effects, lower variance, or lower power requirements.
- After the test: an underpowered test that finds "no significant difference" does **not** prove there is no difference. It may simply have been too small to detect one.

---

# Interview One-Liners

- "I check independence from how the data was collected, normality with a Q-Q plot or Shapiro-Wilk, equal variance with Levene's test, and if those fail I switch to Welch's or a non-parametric test."
- "Since conversion is binary, I would use a two-proportion z-test, after checking the sample size is large enough for the approximation to hold."
- "Same subjects measured twice means a paired test. Different subjects in each group means a two-sample test."
- "A p-value below 0.05 means I reject the null. A p-value above 0.05 means I fail to reject it, which is not the same as proving no difference."
- "I would run a power analysis before the A/B test so the experiment can actually detect a meaningful lift."

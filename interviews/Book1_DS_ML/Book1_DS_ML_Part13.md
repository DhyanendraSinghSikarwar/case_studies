# Book 1 - Part 13: Statistics Deep Dive I (Distributions, Estimation, Inference)

**Topic:** distributions, sampling, estimators, CLT/LLN, CIs, p-values, hypothesis tests, power, multiple comparisons, bootstrap, correlation
**Target:** 50 questions
**Actual:** 61 questions
**Stars:** 20 x ⭐⭐⭐ (Q1-Q20), 27 x ⭐⭐ (Q21-Q47), 14 x ⭐ (Q48-Q61)
**Date:** 2026-10-20

**Scope note:** probability puzzles, Bayes, Markov chains, regression diagnostics, Bayesian stats, sequential testing, CUPED and simulation are in Part 14; A/B design and causal inference are in Part 10.

---

### Q1 ⭐⭐⭐ 🟢 Explain a p-value in plain words. What does it NOT mean?
**Asked at:** Flipkart, Amazon, Walmart, Microsoft IDC, Spotify; near-universal
**Say this first (1 line):** The p-value is the probability of seeing data at least as extreme as ours, *if the null hypothesis were true*. It is not the probability that the null is true.

**Then explain:**
- Start by assuming "no effect" (H0). Ask: how surprising is my result under that assumption? Small p = surprising = evidence against H0.
- It is a statement about the data given H0: P(data | H0). People read it as P(H0 | data), which is a different thing and needs a prior (Bayes).
- What it does NOT mean:
  - Not "probability the result is due to chance".
  - Not the probability the finding will replicate.
  - Not the effect size or its importance. A tiny effect with a huge sample gives a tiny p.
  - p = 0.06 vs 0.04 is not a real difference in evidence; 0.05 is just a convention.
- If H0 is true, p-values are uniformly distributed, so you get p < 0.05 about 5% of the time by design.

**Example:** A/B test, checkout time 10.0 vs 10.5 min, p = 0.14. If the two versions were truly identical, a gap this big (or bigger) would show up about 14% of the time just from sampling noise. That is not enough to call it real. It does not say "86% chance the new version is better".

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
a = rng.normal(10.0, 2, 200); b = rng.normal(10.5, 2, 200)
print(stats.ttest_ind(a, b).pvalue)                 # 0.1429

# p-value by brute force: how often does pure chance give a gap this big?
obs = abs(a.mean() - b.mean())
sims = [rng.normal(10,2,200).mean() - rng.normal(10,2,200).mean() for _ in range(5000)]
print(np.mean(np.abs(sims) >= obs))                 # ~0.144, matches

# when H0 is true, p < 0.05 happens ~5% of the time
ps = [stats.ttest_ind(rng.normal(0,1,50), rng.normal(0,1,50)).pvalue for _ in range(5000)]
print(np.mean(np.array(ps) < 0.05))                 # 0.045
```

**Follow-ups:**
- *Why not just report P(H0 is true)?* That needs a prior; frequentist tests do not give it. Bayesian methods do.
- *p = 0.03 means 97% chance the effect is real?* No. The chance depends on the prior plausibility and power; many p = 0.03 results are false positives when most tested ideas are null.

**Common mistakes:** saying "probability the null is true", "probability result was due to chance", treating p < 0.05 as "important", and treating p > 0.05 as "proved no effect".

### Q2 ⭐⭐⭐ 🟢 Explain Type I and Type II errors. How are they related to alpha, beta and power, and which is costlier in practice?
**Asked at:** Amazon, Flipkart, Swiggy, JPMC, Booking; near-universal
**Say this first (1 line):** Type I = false positive (reject a true null), its rate is alpha. Type II = false negative (miss a real effect), its rate is beta, and power = 1 - beta.

**Then explain:**

| | H0 true (no effect) | H0 false (real effect) |
|---|---|---|
| Reject H0 | Type I error, prob = alpha | Correct, prob = power = 1 - beta |
| Don't reject | Correct, prob = 1 - alpha | Type II error, prob = beta |

- Alpha is chosen by you (commonly 0.05). Beta depends on effect size, sample size, noise and alpha.
- Trade-off: at fixed n, lowering alpha raises beta. The only free lunch is more data (or less noise).
- Which is costlier depends on the business:
  - Shipping a bad feature / approving a bad drug / flagging an innocent customer as fraud: Type I hurts.
  - Missing a real fraud ring, a disease, or a winning feature: Type II hurts.
  - In A/B tests, we usually fix alpha = 5% and size the test for 80% power, so Type II is roughly 4x more tolerated.

**Example:** Fraud model flagging transactions. False positive = a good customer blocked (support cost, churn). False negative = fraud goes through (direct loss). The bank sets thresholds from these two costs, not from a rule of thumb.

**Code:**
```python
import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower
rng = np.random.default_rng(0)

def rejection_rate(delta, n=50, sims=4000):
    rej = 0
    for _ in range(sims):
        x = rng.normal(0, 1, n); y = rng.normal(delta, 1, n)
        rej += stats.ttest_ind(x, y).pvalue < 0.05
    return rej / sims

print(rejection_rate(0.0))   # 0.049 -> Type I rate (alpha)
pw = rejection_rate(0.5)     # power; beta = 1 - pw
print(pw, 1 - pw)             # 0.7035 0.2965
print(TTestIndPower().power(effect_size=0.5, nobs1=50, alpha=0.05))  # 0.697 (theory)
```

**Follow-ups:**
- *How do you reduce both errors?* Increase sample size, reduce variance (CUPED, better metric), or test a larger effect.
- *Is alpha the probability that a significant result is wrong?* No. That is the false discovery rate, which also depends on power and the share of true effects.

**Common mistakes:** thinking alpha and beta must sum to 1; calling non-significance "no effect" (that ignores Type II); never stating power.

### Q3 ⭐⭐⭐ 🟢 What is the difference between standard deviation and standard error?
**Asked at:** Product cos, GCCs, analytics cos
**Say this first (1 line):** Standard deviation (SD) measures how spread out individual data points are; standard error (SE) measures how much a *statistic* (like the sample mean) would vary from sample to sample. SE of the mean = SD / sqrt(n).

**Then explain:**
- SD describes the data. It does not shrink as you collect more data; it just becomes a better estimate of the true spread.
- SE describes the precision of an estimate. It shrinks with sqrt(n): 4x the data halves the SE.
- SE is what goes into confidence intervals and t-tests: CI = mean +/- t * SE.
- Different statistics have different SEs (mean, proportion sqrt(p(1-p)/n), median, regression coefficient).

**Example:** Order values have SD = Rs 400. With n = 100 orders, SE of the mean = 400 / 10 = Rs 40. With n = 10,000, SE = Rs 4. Individual orders still vary by about Rs 400, but we know the average very precisely.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
x = rng.normal(100, 15, 400)
sd = x.std(ddof=1); se = sd / np.sqrt(len(x))
print(round(sd, 2), round(se, 2), round(stats.sem(x), 2))  # 14.95 0.75 0.75
```

**Follow-ups:**
- *When do you report which?* SD to describe variability of the data; SE (or a CI) to report uncertainty of an estimate.
- *Does SE assume independence?* Yes. With clustered data (many rows per user), the naive SE is too small; use cluster-robust SE or aggregate to user level.

**Common mistakes:** using SE to describe spread of the data, using SD in a CI, and forgetting SE assumes independent observations.

### Q4 ⭐⭐⭐ 🟢 State the Central Limit Theorem. Why does it matter for data science, and when does it break down?
**Asked at:** Amazon, Flipkart, Microsoft IDC, Walmart, Zalando
**Say this first (1 line):** For independent, identically distributed data with finite variance, the distribution of the sample mean approaches a normal distribution as n grows, whatever the shape of the original data, with mean mu and SD sigma/sqrt(n).

**Then explain:**
- Why it matters: it lets us build CIs and run z/t tests on means even when the raw data is skewed (order values, session length). It is why A/B testing on averages works.
- "Large enough n" depends on skew: roughly n = 30 for mild skew, thousands for heavy tails or rare events (conversion of 0.1%).
- When it breaks down:
  - Infinite variance (Cauchy; very heavy Pareto tails with alpha <= 2). The mean never settles.
  - Strong dependence (time series, clustered users): effective sample size is much smaller than n.
  - Not identically distributed with a few dominating terms (one whale customer).
  - Statistics other than means (max, min) have different limits.
- CLT is about the *sampling distribution of the mean*, not about the data becoming normal.

**Example:** Exponential data has skew 2.0. Means of n = 2 samples are still skewed (1.43); n = 30 gives 0.36; n = 500 gives 0.11, and the SD of the mean tracks 1/sqrt(n).

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
pop = rng.exponential(1.0, 1_000_000)
print("pop skew", round(stats.skew(pop), 2))                     # 2.01
for n in (2, 30, 500):
    means = rng.choice(pop, (10000, n)).mean(axis=1)
    print(n, round(stats.skew(means), 2), round(means.std(), 3), round(1/np.sqrt(n), 3))
# n, skew of mean, SD of mean, 1/sqrt(n):  2 1.43 0.707 0.707 | 30 0.36 0.185 0.183 | 500 0.11 0.045 0.045

c = rng.standard_cauchy((10000, 500)).mean(axis=1)               # Cauchy: no CLT
print(np.subtract(*np.percentile(c, [75, 25])).round(2))         # IQR ~2 (a single obs has IQR 2): no shrinkage
```

**Follow-ups:**
- *Does the CLT mean my data is normal?* No, only the mean's distribution.
- *Would you trust it for revenue per user?* Check skew and n; if heavy tails, use bootstrap or trimmed/log metrics.

**Common mistakes:** "n >= 30 always works", saying the data becomes normal, and ignoring dependence between observations.

### Q5 ⭐⭐⭐ 🟢 How do you correctly interpret a 95% confidence interval? Why is 'there is a 95% chance the true mean lies in it' wrong?
**Asked at:** Product cos, GCCs, Europe product cos
**Say this first (1 line):** If we repeated the whole experiment many times and built an interval each time, about 95% of those intervals would contain the true value. The 95% belongs to the method, not to one interval.

**Then explain:**
- The true mean is a fixed number (frequentist view). Our interval is random, because it depends on the sample. Once computed, it either contains the truth or it does not; there is no probability left.
- So "95% chance the true mean is in [46.9, 54.7]" is the wrong reading. The right one: "this interval came from a procedure with 95% coverage".
- Practical reading: the range of effect sizes that are plausible/compatible with the data. Width shows precision.
- A Bayesian credible interval does allow the "95% probability" statement, but under a prior.

**Example:** Average delivery time estimated as 32 min, 95% CI [30, 34]. Values like 30 or 34 are compatible with data; 40 is not. We do not say "95% sure it is between 30 and 34" as a probability statement about the parameter.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
true_mu, n, hits = 50, 25, 0
for _ in range(10000):
    s = rng.normal(true_mu, 10, n)
    lo, hi = stats.t.interval(0.95, n-1, loc=s.mean(), scale=stats.sem(s))
    hits += lo <= true_mu <= hi
print(hits / 10000)    # 0.95 -> about 95% of intervals cover the truth
```

**Follow-ups:**
- *What changes the width?* Higher confidence, smaller n, and larger variance widen it; width scales as 1/sqrt(n).
- *If CIs of two groups overlap, is the difference insignificant?* Not necessarily; compare using the CI of the difference.

**Common mistakes:** the "95% probability" reading, thinking 95% of the data lies in the CI (that is a prediction interval), and ignoring the sampling assumptions.

### Q6 ⭐⭐⭐ 🟢 One-tailed vs two-tailed tests: when do you use each and what is the cost of choosing one-tailed?
**Asked at:** Product cos, analytics cos
**Say this first (1 line):** Two-tailed tests for "is there any difference", one-tailed only when a difference in the other direction would be treated exactly like no difference and you decided that before seeing data. The cost is that you cannot detect an effect in the unexpected direction.

**Then explain:**
- Two-tailed: H1: mu1 != mu2. Alpha is split 2.5% / 2.5% across tails. Default in experiments and papers.
- One-tailed: H1: mu1 > mu2. All 5% in one tail, so it needs a smaller statistic to reject, which gives more power for that direction (p is half the two-sided p when the effect is in the predicted direction).
- Cost: a big harmful effect in the "wrong" direction can never be flagged. Also it invites cheating: picking the tail after seeing the data doubles the real Type I rate.
- One-tailed is legitimate for non-inferiority tests ("is the new model not worse by more than X?") and some pre-registered tests.

**Example:** New checkout design. If it hurts conversion we also want to know and roll back, so the test is two-sided. A one-sided test would just say "not better" and hide a real drop.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
a = rng.normal(0.3, 1, 40); b = rng.normal(0, 1, 40)
print(stats.ttest_ind(a, b).pvalue)                          # two-sided
print(stats.ttest_ind(a, b, alternative='greater').pvalue)   # half of it (effect is in that direction)
print(stats.ttest_ind(a, b, alternative='less').pvalue)      # ~1 - half: wrong direction
```
Output from my run: 0.0205, 0.0103, 0.9897.

**Follow-ups:**
- *Can I switch to one-tailed when p = 0.07 two-sided?* No, that is p-hacking.
- *Do CIs differ?* A one-sided test pairs with a one-sided bound, not a two-sided interval.

**Common mistakes:** choosing the tail after peeking, using one-tailed because "we only expect improvement", and ignoring that harm in the opposite direction is invisible.

### Q7 ⭐⭐⭐ 🟢 What is the difference between covariance and correlation? Why is correlation preferred for comparing relationships?
**Asked at:** Product cos, GCCs, analytics cos
**Say this first (1 line):** Covariance shows the direction of a linear relationship but its size depends on the units; correlation is covariance divided by both standard deviations, so it is unit-free and always between -1 and +1.

**Then explain:**
- Cov(X,Y) = E[(X - mu_x)(Y - mu_y)]. Positive: they move together. Negative: opposite. The magnitude is hard to read.
- Corr = Cov / (sd_x * sd_y). Changing height from cm to metres changes covariance 100x but leaves correlation unchanged.
- Correlation lets you compare strength across pairs of variables with different scales.
- Both measure only *linear* association, are sensitive to outliers, and say nothing about causation. Zero correlation does not mean independence.
- Covariance still matters: covariance matrices drive PCA, portfolio variance, Mahalanobis distance, Gaussian models.

**Example:** Height (cm) vs weight (kg): covariance 51.7, correlation 0.74. Change height to metres: covariance 0.517, correlation still 0.74.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
h = rng.normal(170, 10, 500); w = 0.5*h + rng.normal(0, 5, 500)
print(np.cov(h, w)[0,1].round(2), np.corrcoef(h, w)[0,1].round(3))          # 51.72  0.736
print(np.cov(h/100, w)[0,1].round(3), np.corrcoef(h/100, w)[0,1].round(3))  # 0.517 0.736
```

**Follow-ups:**
- *Is correlation = 0 independence?* No; y = x^2 on symmetric x has zero correlation but full dependence (see Q32).
- *Is the covariance matrix always PSD?* Yes.

**Common mistakes:** comparing raw covariances across variable pairs, reading correlation as causation, and forgetting outliers can dominate.

### Q8 ⭐⭐⭐ 🟢 Describe the normal distribution: properties, the 68-95-99.7 rule, z-scores and standardisation. How do you check if data is normal?
**Asked at:** Product cos, GCCs, analytics cos
**Say this first (1 line):** The normal is the symmetric bell curve defined entirely by its mean and SD; about 68%, 95% and 99.7% of values fall within 1, 2 and 3 SDs of the mean; a z-score says how many SDs a value is from the mean.

**Then explain:**
- Properties: symmetric, mean = median = mode, skew 0, kurtosis 3, fully described by mu and sigma. Sums of independent normals are normal.
- Rule: within 1/2/3 SD = 68.27% / 95.45% / 99.73%. And 1.96 SD = 95% (two-sided).
- z = (x - mean) / sd. Standardising gives mean 0, SD 1, so values on different scales become comparable and we can use standard normal tables. It does not change the shape.
- Checking normality:
  - Plot: histogram and Q-Q plot (points near the straight line = normal; curved ends = heavy tails; S/bow shapes = skew).
  - Numbers: skewness, kurtosis; tests such as Shapiro-Wilk (best small/medium n), Anderson-Darling, KS (needs known parameters).
  - Tests get oversensitive at large n, so rely on the Q-Q plot plus practical judgement.

**Example:** Exam scores mean 60, SD 8. A score of 76 has z = 2: top ~2.5%.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
print([round(stats.norm.cdf(k) - stats.norm.cdf(-k), 4) for k in (1, 2, 3)])  # [0.6827, 0.9545, 0.9973]
x = rng.normal(60, 8, 300)
z = (x - x.mean()) / x.std(ddof=1)
print(z.mean().round(6), z.std(ddof=1).round(3))                 # ~0 1.0
print(stats.shapiro(x).pvalue.round(3))                          # 0.757 -> consistent with normal
print(stats.shapiro(rng.lognormal(0, 1, 300)).pvalue)            # ~1e-20 -> not normal
print(stats.probplot(x, dist='norm')[1][2].round(4))             # Q-Q straightness r = 0.9981
```

**Follow-ups:**
- *Why is the normal so common?* CLT: sums/averages of many small independent effects.
- *Which transformation fixes right skew?* log, sqrt, Box-Cox.

**Common mistakes:** believing standardising makes data normal, using Shapiro-Wilk p-value alone on huge n, and applying 68-95-99.7 to non-normal data.

### Q9 ⭐⭐⭐ 🟡 t-test vs z-test: when do you use which? What are the assumptions of a t-test?
**Asked at:** Flipkart (reported Nov 2025), Amazon, GCCs
**Say this first (1 line):** Use a z-test when the population SD is known or n is very large; use a t-test when you estimate the SD from the sample, which is almost always. The t-distribution has fatter tails to pay for that extra uncertainty.

**Then explain:**
- t = (mean - mu0) / (s / sqrt(n)), with n - 1 degrees of freedom. As df grows, t converges to the normal, so with n in the hundreds the two give nearly the same answer.
- Critical values (95%, two-sided): df 5: 2.571, df 20: 2.086, df 100: 1.984, df 10000: 1.960 (z = 1.96).
- t-test assumptions:
  - Independent observations (the big one).
  - Data roughly normal, or n large enough for the CLT on the mean. Matters mostly for small n or heavy skew.
  - Two-sample: similar variances (pooled) or use Welch which does not need it.
  - Continuous/interval scale, no extreme outliers.
- z-tests are standard for proportions (the SD comes from p itself) and large-sample A/B tests.

**Example:** 20 baskets sampled, claimed average Rs 50, sample SD about 10, sample mean very close to 50. t = 0.09, p = 0.93: no evidence the claim is wrong.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
x = rng.normal(52, 10, 20)
t = (x.mean() - 50) / (x.std(ddof=1) / np.sqrt(20))
print(round(t, 3), round(2 * stats.t.sf(abs(t), 19), 4))   # 0.086 0.9322
print(stats.ttest_1samp(x, 50))                             # same
print(stats.t.ppf(0.975, [5, 20, 100, 10000]).round(3), stats.norm.ppf(0.975).round(3))
```

**Follow-ups:**
- *Is the t-test robust to non-normality?* Quite, for moderate n and mild skew; not for tiny n or heavy tails.
- *Which t-test for two groups?* Welch by default (Q25).

**Common mistakes:** using z when the SD is estimated on small n, claiming the t-test needs the *data* to be normal (it is the mean), and ignoring dependence.

### Q10 ⭐⭐⭐ 🟡 Statistical significance vs practical significance: a result has p = 0.001 but a tiny effect. What do you do?
**Asked at:** Amazon, Spotify, Booking, Swiggy
**Say this first (1 line):** A small p only says the effect is unlikely to be exactly zero; it says nothing about whether the effect is big enough to matter. I look at the effect size and its confidence interval and compare it with the minimum change that pays for the cost of shipping.

**Then explain:**
- With a very large n, even trivial differences become significant, because SE shrinks like 1/sqrt(n).
- I report: absolute difference, relative lift, CI, standardised effect (Cohen's d), and translate to money/users.
- Decision rule: define a *minimum detectable / practically important effect* (MDE) before the test. Ship only if the CI lies mostly above that threshold.
- Consider cost of the change (engineering, complexity, long-term maintenance), risk, and other metrics (guardrails).
- Opposite case: a large effect with p = 0.2 on a small sample may be important but underpowered; collect more data rather than discard.

**Example:** Avg order value Rs 100.0 vs Rs 100.39 with 200,000 users per arm: p = 9e-10, but d = 0.019 and the CI is [0.26, 0.51] rupees. If the feature costs more than that per order to run, do not ship.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
n = 200000
a = rng.normal(100, 20, n); b = rng.normal(100.4, 20, n)
r = stats.ttest_ind(b, a)
d = (b.mean() - a.mean()) / np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
diff = b.mean() - a.mean(); se = np.sqrt(a.var(ddof=1)/n + b.var(ddof=1)/n)
print(r.pvalue, round(d, 3), round(diff, 3), np.round([diff - 1.96*se, diff + 1.96*se], 3))
# 8.5e-10  0.019  0.387  [0.264 0.511]
```

**Follow-ups:**
- *How do you set the practical threshold?* From business: revenue per user x users, cost of change, or what past launches moved.
- *Can the reverse happen?* Yes, "not significant" with a wide CI that includes big effects means inconclusive, not "no effect".

**Common mistakes:** shipping on p alone, reporting only p, and ignoring the CI width.

### Q11 ⭐⭐⭐ 🟡 What is statistical power and what factors affect it? How would you increase it?
**Asked at:** Amazon, Spotify, Booking, Klarna, Swiggy
**Say this first (1 line):** Power is the probability that the test detects a real effect of a given size (1 - beta). Usual target is 80%.

**Then explain:** Power goes up with:
- Larger sample size (SE falls with sqrt(n)).
- Larger true effect size.
- Lower noise (SD): use cleaner metrics, stratification, CUPED, paired designs.
- Higher alpha (e.g. 0.10) or a one-sided test (costs more false positives or loses a direction).
- Better design: equal arm sizes, less dilution (only include users who saw the change).

Ways to increase it in practice: run longer, reduce variance, pick a more sensitive metric, test a bigger change, or accept a larger MDE.

**Example:** Two groups of 50, true effect d = 0.5: power is only about 70%. With 100 per group power is 0.94. For a small effect d = 0.2, you need about 393 per group for 80%.

**Code:**
```python
from statsmodels.stats.power import TTestIndPower
p = TTestIndPower()
for d in (0.2, 0.5):
    print(d, round(p.power(d, 50, 0.05), 3), round(p.solve_power(d, power=0.8, alpha=0.05)))
# 0.2 -> power 0.168, n needed 393 ; 0.5 -> power 0.697, n needed 64
print(round(p.power(0.5, 100, 0.05), 3), round(p.power(0.5, 50, 0.01), 3))  # 0.94 (more n), 0.453 (lower alpha)
```

**Follow-ups:**
- *Why is 80% the standard?* Convention balancing cost of data vs missed effects; use higher (90%) when misses are costly.
- *What is post-hoc power?* Computing power from the observed effect is circular and uninformative; do power analysis beforehand.

**Common mistakes:** running tests without a power calculation, saying "not significant so no effect", and quoting observed (post-hoc) power.

### Q12 ⭐⭐⭐ 🟡 How do you compute the required sample size for a two-proportion (conversion-rate) test? Show it in scipy/statsmodels.
**Asked at:** Amazon, Swiggy, Booking, Spotify
**Say this first (1 line):** Decide baseline rate, the minimum lift worth detecting, alpha and power; then solve for n per arm. For 10% to 11% at alpha 5%, power 80%, you need about 14,700 users per arm.

**Then explain:**
- Inputs: baseline p1, target p2 = p1 + MDE, alpha (two-sided), power, allocation ratio.
- Formula (normal approximation): n per arm = (z_{1-alpha/2} + z_{power})^2 * [p1(1-p1) + p2(1-p2)] / (p2 - p1)^2.
- Halving the MDE roughly quadruples n. That is why small lifts on low conversion need huge traffic.
- Divide by the share of eligible traffic and convert to days. Remember weekly seasonality (run full weeks).
- Total sample = 2 x n per arm.

**Example:** 10% baseline, detect +1 percentage point (10% relative lift). About 14,745 per arm, ~29,500 total.

**Code:**
```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower

es = proportion_effectsize(0.11, 0.10)            # Cohen's h, 0.0326
n = NormalIndPower().solve_power(es, power=0.8, alpha=0.05, ratio=1, alternative='two-sided')
print(round(es, 4), int(np.ceil(n)))              # 0.0326 14745

# by hand
p1, p2 = 0.10, 0.11; za, zb = stats.norm.ppf(0.975), stats.norm.ppf(0.8)
print(int(np.ceil((za + zb)**2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)**2)))   # 14749
```

**Follow-ups:**
- *Why do the two answers differ slightly?* statsmodels uses the arcsine (Cohen's h) transform; the hand formula uses unpooled variances. Both are fine.
- *Unequal split?* Use ratio != 1; total needed rises.
- *What if I peek?* Fixed-horizon sample sizes assume one look; use sequential methods (Part 14).

**Common mistakes:** using relative instead of absolute difference, forgetting two arms, ignoring the traffic eligible, and computing n after the test.

### Q13 ⭐⭐⭐ 🟡 What is the multiple comparisons problem? Explain Bonferroni and Benjamini-Hochberg and when to use each.
**Asked at:** Product cos, Databricks-style teams, Europe product cos
**Say this first (1 line):** Every extra test adds a chance of a false positive, so with many tests you will find "significant" results by luck. Bonferroni controls the chance of *any* false positive (strict); Benjamini-Hochberg controls the *share* of false discoveries among your findings (more power).

**Then explain:**
- With m independent tests at alpha 0.05, P(at least one false positive) = 1 - 0.95^m. For m = 20 that is 64%.
- **Bonferroni:** reject if p <= alpha/m. Controls FWER (family-wise error rate). Simple, valid under any dependence, but very conservative when m is large.
- **Benjamini-Hochberg (BH):** sort p-values, find the largest k with p_(k) <= (k/m) * q, reject the first k. Controls FDR (expected proportion of false discoveries) at q.
- When to use:
  - Few tests, or a false positive is very costly (confirmatory, one decision per family, e.g. clinical endpoints, several variants vs control): Bonferroni/Holm.
  - Many tests, exploratory, you can tolerate some false leads (many metrics, segments, genomics, feature screening): BH.

**Example:** 1,000 metrics, 10 truly moved (p tiny). Bonferroni threshold is 0.00005 and finds only 1 of the 10; BH finds all 10 with 0 false ones.

**Code:**
```python
import numpy as np
from statsmodels.stats.multitest import multipletests
rng = np.random.default_rng(1)
pv = np.concatenate([rng.uniform(0, 0.0005, 10), rng.uniform(0, 1, 990)])  # first 10 are real
print((pv < 0.05).sum())                       # uncorrected: many false hits
for m in ('bonferroni', 'holm', 'fdr_bh'):
    rej = multipletests(pv, alpha=0.05, method=m)[0]
    print(m, rej.sum(), 'true found:', rej[:10].sum(), 'false:', rej[10:].sum())
print(1 - 0.95**20)                            # 0.64
```

**Follow-ups:**
- *Is Holm better than Bonferroni?* Yes, it controls FWER too and is never less powerful.
- *Is BH valid under dependence?* For independent or positively dependent tests (PRDS); otherwise use Benjamini-Yekutieli (Q58).

**Common mistakes:** correcting after picking the best result, running 20 segment cuts with no correction, and using Bonferroni for 10,000 tests.

### Q14 ⭐⭐⭐ 🟡 Explain the chi-squared test (independence and goodness of fit). What are its assumptions?
**Asked at:** Flipkart, Amazon, analytics cos, GCCs
**Say this first (1 line):** Chi-squared compares observed counts with the counts expected under a null hypothesis: sum of (O - E)^2 / E. Goodness of fit asks "do counts follow this distribution?"; independence asks "are two categorical variables unrelated?".

**Then explain:**
- **Independence:** build a contingency table. E_ij = (row total x column total) / grand total. df = (r - 1)(c - 1).
- **Goodness of fit:** compare observed category counts with expected proportions. df = k - 1 (minus estimated parameters).
- Assumptions: independent observations (each unit counted once), counts not percentages, and expected counts large enough (rule of thumb >= 5 in most cells). Otherwise use Fisher's exact (Q27) or merge categories.
- It tells you *that* there is an association, not how strong or which direction; add Cramer's V and look at residuals.

**Example:** 200 users per variant; clicks 90 vs 60. Chi-squared = 9.6, df = 1, p = 0.0019: click-through depends on variant.

**Code:**
```python
import numpy as np
from scipy import stats
obs = np.array([[90, 110], [60, 140]])      # rows = variants A, B; cols = clicked, not clicked
chi2, p, dof, exp = stats.chi2_contingency(obs, correction=False)
print(round(chi2, 3), round(p, 4), dof)     # 9.6 0.0019 1
print(exp)                                   # [[75 125], [75 125]]
print(stats.chisquare([18, 22, 20, 25, 15], f_exp=[20]*5))   # fair die? stat 2.9, p 0.575
```

**Follow-ups:**
- *Yates correction?* A continuity correction for 2x2 tables; scipy applies it by default (`correction=True`), conservative for large n.
- *Chi-squared on percentages?* No, always raw counts.

**Common mistakes:** small expected counts, using it on non-independent rows (repeat visits by the same user), and reading p as strength of association.

### Q15 ⭐⭐⭐ 🟡 Parametric vs non-parametric tests: when would you use Mann-Whitney U instead of a t-test?
**Asked at:** Amazon, GCCs, product cos
**Say this first (1 line):** Parametric tests assume a distribution shape (e.g. normal) and compare parameters such as means; non-parametric tests like Mann-Whitney use ranks and make fewer assumptions. I use Mann-Whitney for small samples, ordinal data, or heavy outliers/skew where the mean is a poor summary.

**Then explain:**
- Mann-Whitney U: pools both groups, ranks values, checks whether one group tends to have higher ranks. It tests P(X > Y) = 0.5 (stochastic dominance), not strictly medians (Q55).
- Use it when: ordinal ratings, tiny n with clearly non-normal data, extreme outliers you cannot remove.
- Cost: slightly lower power than the t-test when the data really is normal (about 95% efficient), and it answers a different question than "difference in means".
- With large n the t-test is usually fine via the CLT; if you care about *revenue* (a mean), a rank test may be the wrong target.

**Example:** Time-on-page for two designs, lognormal data (n = 60 per group, true log-mean 3.0 vs 3.4) with a few huge values. In one simulated run (the code below, seed 1) the Welch t-test gives p = 0.048 because the extreme values inflate the variance; Mann-Whitney sees the systematic shift in ranks (p = 0.0074). One run only, not a general rule: on skewed data the rank test is often, not always, more powerful. They answer different questions; decide based on the metric you care about.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
x = rng.lognormal(3, 1, 60); y = rng.lognormal(3.4, 1, 60)
print(stats.ttest_ind(x, y, equal_var=False).pvalue)                 # Welch t-test
print(stats.mannwhitneyu(x, y, alternative='two-sided').pvalue)      # rank test
```

**Follow-ups:**
- *Paired non-parametric version?* Wilcoxon signed-rank (Q49).
- *Several groups?* Kruskal-Wallis.

**Common mistakes:** saying "non-parametric = no assumptions" (it assumes independence; for a median interpretation it assumes equal shapes), and using it when the business metric is the mean.

### Q16 ⭐⭐⭐ 🟡 What is the bootstrap? Explain how to get a confidence interval with it and implement it in NumPy.
**Asked at:** Google-style, Amazon, Spotify, Zalando; GCCs
**Say this first (1 line):** The bootstrap resamples your data with replacement many times, recomputes the statistic each time, and uses the spread of those values to approximate the sampling distribution, so you get SEs and CIs without a formula.

**Then explain:**
- Treat the sample as a stand-in for the population. Draw n values *with replacement*, compute the statistic, repeat B times (1,000-10,000).
- Percentile CI: take the 2.5th and 97.5th percentiles of the bootstrap statistics. SE = SD of the bootstrap statistics.
- Works for medians, ratios, quantiles, AUC, any statistic without a simple SE.
- Limits: needs an iid sample, struggles with tiny n, extremes (max/min) and very heavy tails (Q56); for dependent data use block bootstrap.

**Example:** Revenue per user is right-skewed (n = 80, mean 33.4). Bootstrap CI for the mean is [25.4, 42.9], and the bootstrap SE matches the analytic SE (4.47 vs 4.52).

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
data = rng.exponential(30, 80)
boots = np.array([rng.choice(data, data.size, replace=True).mean() for _ in range(10000)])
print(np.percentile(boots, [2.5, 97.5]).round(2), data.mean().round(2))   # CI and mean
print(boots.std().round(2), stats.sem(data).round(2))                      # bootstrap SE vs formula SE
res = stats.bootstrap((data,), np.mean, n_resamples=9999, random_state=0, method='percentile')
print(res.confidence_interval)                                             # scipy cross-check
```

**Follow-ups:**
- *How many resamples?* 1,000+ for SE, 5,000-10,000 for percentile CIs.
- *Bootstrap vs permutation test?* Bootstrap estimates uncertainty; permutation tests a null of exchangeability (Q48).

**Common mistakes:** resampling without replacement, bootstrapping dependent rows (resample users, not events), and trusting it for the max or tiny samples.

### Q17 ⭐⭐⭐ 🟡 Binomial vs Poisson: when does each apply, and when does Poisson approximate binomial?
**Asked at:** Swiggy, Flipkart, Amazon, GCCs
**Say this first (1 line):** Binomial counts successes in a fixed number n of independent yes/no trials; Poisson counts events in a fixed time or space window with no fixed upper limit. Poisson approximates binomial when n is large and p is small (n*p moderate).

**Then explain:**

| | Binomial(n, p) | Poisson(lambda) |
|---|---|---|
| Setting | n trials, each success with prob p | events at a constant average rate |
| Support | 0..n | 0, 1, 2, ... |
| Mean | np | lambda |
| Variance | np(1-p) (less than mean) | lambda (equal to mean) |

- Poisson assumptions: events independent, constant rate, no two events at exactly the same time.
- Approximation: Binomial(n, p) ~ Poisson(np) for n >= 100 and p <= 0.01 or so. Variance np(1-p) is almost np.
- Real data is often *overdispersed* (variance > mean) because rates vary, so Poisson underestimates uncertainty (Q57).

**Example:** 1,000 customers, each has a 0.3% chance of a rare complaint: Binomial P(3) = 0.2244, Poisson(3) P(3) = 0.2240. Orders per minute at a restaurant: Poisson. Number of users clicking among 1,000 shown an ad: binomial.

**Code:**
```python
import numpy as np
from scipy import stats
n, p = 1000, 0.003
k = np.arange(8)
print(np.round(stats.binom.pmf(k, n, p), 4))      # [0.0496 0.1491 0.2242 0.2244 0.1683 0.1009 0.0503 0.0215]
print(np.round(stats.poisson.pmf(k, n*p), 4))     # [0.0498 0.1494 0.224  0.224  0.168  0.1008 0.0504 0.0216]
print(stats.binom.stats(100, 0.3), stats.poisson.stats(3))   # var 21 vs mean 30; var = mean = 3
```

**Follow-ups:**
- *How do you check Poisson fit?* Compare variance to mean (dispersion), or a chi-squared goodness of fit.
- *Relation to the exponential?* Gaps between Poisson events are exponential (Q23).

**Common mistakes:** using Poisson when there is an upper limit and p is not small, ignoring overdispersion, and assuming independent events when they cluster (viral spikes).

### Q18 ⭐⭐⭐ 🟡 What is sampling bias? Give examples (selection, survivorship, non-response) and how you would detect and mitigate them.
**Asked at:** Product cos, GCCs, Spotify, Booking
**Say this first (1 line):** Sampling bias is when the way data was collected makes it systematically unrepresentative of the population you want to talk about, so more data does not fix it.

**Then explain:**
- **Selection bias:** who gets into the data is not random. Example: a survey on the app only reaches active users, so satisfaction looks high.
- **Survivorship bias:** only the survivors are visible. Example: analysing loans that were repaid, or startups that still exist; churned users have left no data. Classic: WWII planes, armour where holes are *not*.
- **Non-response bias:** the people who answer differ from those who don't (unhappy customers skip the NPS survey).
- Others: convenience sampling, self-selection (opt-in beta users), undercoverage, and time/label bias (credit models trained only on approved applicants: reject inference problem).
- Detect: compare sample vs known population on demographics/behaviour; check response rate by segment; ask "how did a row get into this table?".
- Mitigate: random sampling, stratification, follow-ups to non-responders, post-stratification/inverse probability weighting, include dropped/churned records, randomised experiments, and honest limits on generalisation.

**Example:** A model for loan default is trained on approved loans only. It never sees applicants who were rejected, so it is biased for exactly the borderline cases it will score in production.

**Follow-ups:**
- *Can big data fix it?* No, a huge biased sample gives a precisely wrong answer.
- *How would you reweight?* Weight each respondent by 1 / P(response | features), or by population share / sample share per stratum.

**Common mistakes:** confusing it with random sampling error, ignoring the data-generation process, and treating "users in the logs" as "all users".

### Q19 ⭐⭐⭐ 🟡 What makes an estimator good? Explain bias, variance, MSE, and why the sample variance divides by n-1.
**Asked at:** Product cos, GCCs, analytics cos
**Say this first (1 line):** A good estimator is accurate on average (low bias), stable across samples (low variance), and gets better with more data (consistent). MSE = bias^2 + variance combines the first two. Dividing by n-1 makes the sample variance unbiased.

**Then explain:**
- Bias = E[estimator] - true value. Variance = how much it changes sample to sample. MSE = E[(estimator - truth)^2] = bias^2 + variance.
- Other desirable properties: consistency (converges to truth as n grows), efficiency (smallest variance among unbiased estimators), sufficiency.
- Why n-1: the sample mean is fitted to the same data, so deviations from it are smaller than deviations from the true mean. Dividing by n underestimates the variance by factor (n-1)/n. Using n-1 (Bessel's correction) fixes that: you have only n-1 free pieces of information (degrees of freedom).
- Unbiased is not always best: the divide-by-n estimator is biased but has lower MSE for normal data. Shrinkage/regularisation (ridge, James-Stein) deliberately accepts bias to cut variance.

**Example:** n = 5, true variance 4. Average of divide-by-n estimates is 3.19 (about 4 x 4/5 = 3.2); divide-by-(n-1) averages 3.99. Yet MSE is lower for the biased one (5.8 vs 8.0).

**Code:**
```python
import numpy as np
rng = np.random.default_rng(1)
v0, v1 = [], []
for _ in range(100000):
    s = rng.normal(0, 2, 5)              # true variance = 4
    v0.append(s.var(ddof=0)); v1.append(s.var(ddof=1))
v0, v1 = np.array(v0), np.array(v1)
print(v0.mean().round(3), v1.mean().round(3))                      # 3.192 3.99  -> bias of ddof=0
print(((v0 - 4)**2).mean().round(3), ((v1 - 4)**2).mean().round(3))   # MSE 5.774 vs 8.002
```

**Follow-ups:**
- *Is the sample SD unbiased?* No, sqrt of an unbiased variance is slightly biased low (Jensen).
- *Does ddof matter for large n?* Hardly; it matters for small samples.

**Common mistakes:** "unbiased always means best", forgetting numpy's `var` defaults to ddof=0 while pandas' defaults to ddof=1, and explaining n-1 only as "a correction" without the degrees-of-freedom reason.

### Q20 ⭐⭐⭐ 🟡 Explain maximum likelihood estimation. Derive the MLE for a Bernoulli probability and for a normal mean and variance.
**Asked at:** Product cos, GCCs, Microsoft IDC
**Say this first (1 line):** MLE picks the parameter values that make the observed data most probable: maximise L(theta) = product of p(x_i | theta), or equivalently the log-likelihood.

**Then explain:**
- Take logs (turns a product into a sum, same maximiser), differentiate, set to zero, check it is a maximum.
- **Bernoulli(p):** data x_1..x_n with k successes. log L = k log p + (n - k) log(1 - p). Derivative: k/p - (n - k)/(1 - p) = 0, so **p_hat = k/n**, the sample proportion.
- **Normal(mu, sigma^2):** log L = -(n/2) log(2 pi sigma^2) - sum (x_i - mu)^2 / (2 sigma^2).
  - d/d mu = 0 gives **mu_hat = x_bar**.
  - d/d sigma^2 = 0 gives **sigma2_hat = (1/n) sum (x_i - x_bar)^2**, which divides by n, so it is biased (Q19) but consistent.
- MLE is consistent, asymptotically normal and efficient (Q53). Logistic regression and most neural-net losses (cross-entropy, MSE for Gaussian noise) are MLE under some model.
- No closed form usually: optimise numerically (gradient descent, Newton, EM).

**Example:** 150 purchases from 500 visitors: p_hat = 0.30.

**Code:**
```python
import numpy as np
from scipy import stats
from scipy.optimize import minimize
rng = np.random.default_rng(1)
x = rng.normal(5, 2, 1000)
nll = lambda th: -stats.norm.logpdf(x, th[0], np.exp(th[1])).sum()   # th = (mu, log sigma)
r = minimize(nll, [0, 0])
print(r.x[0].round(4), np.exp(r.x[1]).round(4))        # numeric MLE
print(x.mean().round(4), x.std(ddof=0).round(4))       # closed form: same (ddof=0!)
b = rng.binomial(1, 0.3, 500)
grid = np.linspace(0.01, 0.99, 99)
ll = b.sum()*np.log(grid) + (500 - b.sum())*np.log(1 - grid)
print(grid[ll.argmax()], b.mean())                     # grid MLE = sample proportion
```

**Follow-ups:**
- *MLE vs MAP?* MAP adds a prior; with a flat prior they coincide. Ridge = Gaussian prior, lasso = Laplace prior.
- *Why log?* Numerical stability and easier derivatives.

**Common mistakes:** thinking MLE is always unbiased, forgetting the normal variance MLE divides by n, and not checking the second-order condition.

### Q21 ⭐⭐ 🟢 What is the Law of Large Numbers and how is it different from the CLT?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** The LLN says the sample mean converges to the true mean as n grows (where it ends up). The CLT says how the sample mean fluctuates around the true mean: approximately normal with SD sigma/sqrt(n) (the shape and speed).

**Then explain:**
- LLN: x_bar -> mu. Weak LLN: in probability; strong LLN: almost surely. Needs a finite mean (iid case).
- CLT: sqrt(n)(x_bar - mu)/sigma -> N(0, 1). Needs a finite variance too.
- LLN justifies estimation, Monte Carlo and "average over many users"; CLT justifies CIs and tests.
- LLN does not say that past losses get "evened out" (gambler's fallacy): it is about the average converging, not the total balancing.

**Example:** Average of exponential(mean 1) draws: n = 10 gives 0.56, n = 100 gives 0.93, n = 10,000 gives 0.976, n = 200,000 gives 1.0004. The convergence is the LLN; the typical error ~1/sqrt(n) is the CLT.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(2)
x = rng.exponential(1, 200000)
for n in (10, 100, 10000, 200000):
    print(n, round(x[:n].mean(), 4))     # drifts toward the true mean 1
```

**Follow-ups:**
- *Does LLN hold for the Cauchy?* No, there is no mean (Q60).
- *LLN for proportions?* Observed conversion rate -> true rate.

**Common mistakes:** gambler's fallacy, mixing up "converges" with "becomes normal", and applying either to dependent or heavy-tailed data.

### Q22 ⭐⭐ 🟢 Uniform distribution: mean, variance, and how do you use it to generate samples from any distribution (inverse transform)?
**Asked at:** Product cos, GCCs, quant-leaning teams
**Say this first (1 line):** For Uniform(a, b): mean = (a + b)/2, variance = (b - a)^2/12. To sample from any distribution, draw U ~ Uniform(0,1) and return F^-1(U), the inverse CDF.

**Then explain:**
- Why it works: if U is uniform on (0,1), then X = F^-1(U) has P(X <= x) = P(U <= F(x)) = F(x), so X follows F.
- Exponential(lambda): F(x) = 1 - exp(-lambda x), so X = -ln(1 - U)/lambda.
- Needs a computable inverse CDF. If there isn't one (e.g. normal), use numerical inverse (scipy `ppf`), Box-Muller, or rejection sampling.
- For discrete distributions, find the first category whose cumulative probability exceeds U.
- Uniform(0,1) mean 0.5, variance 1/12 = 0.0833.

**Example:** Simulating customer wait times for a queue model: draw uniforms and map them through the exponential inverse CDF.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
u = rng.uniform(0, 1, 200000)
print(u.mean().round(3), u.var().round(4), round(1/12, 4))    # 0.5 0.0836 0.0833
lam = 2.0
e = -np.log(1 - u) / lam                                       # inverse transform
print(e.mean().round(3), stats.kstest(e, 'expon', args=(0, 1/lam)).pvalue.round(3))  # mean ~0.5; fits exponential
```

**Follow-ups:**
- *Reverse direction?* F(X) is Uniform(0,1) (probability integral transform); it underlies p-values and copulas.
- *Normal sampling?* `norm.ppf(u)`, or Box-Muller.

**Common mistakes:** using the PDF instead of the CDF, forgetting variance is (b-a)^2/12, and using inverse transform without a closed-form inverse and no numerical fallback.

### Q23 ⭐⭐ 🟡 Exponential distribution: what is memorylessness and how does it relate to the Poisson process?
**Asked at:** Swiggy, Flipkart, Amazon, Zalando (delivery/wait-time themes)
**Say this first (1 line):** The exponential models the waiting time until the next event at a constant rate. Memoryless means that having already waited t minutes tells you nothing about how much longer you must wait: P(T > s + t | T > s) = P(T > t). In a Poisson process, gaps between events are exponential.

**Then explain:**
- Exponential(lambda): mean 1/lambda, variance 1/lambda^2, P(T > t) = exp(-lambda t).
- Memoryless: the "remaining wait" has the same distribution however long you have waited. It is the only continuous distribution with this property.
- Poisson process with rate lambda: number of events in time t ~ Poisson(lambda t) and the gaps ~ Exponential(lambda). They are two views of the same process.
- Poor fit when the hazard is not constant: machines wear out (increasing hazard), customers churn early then stabilise (decreasing). Use Weibull or gamma.

**Example:** A cab arrives on average every 10 minutes (exponential). Even if you've been waiting 10 minutes, expected additional wait is still 10 minutes. Simulation gives 10.03 for the extra wait after already waiting 10 min, vs 10.01 overall.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(2)
t = rng.exponential(10, 500000)                  # mean wait 10 min
print((t[t > 10] - 10).mean().round(2), t.mean().round(2))      # ~10 ~10: memoryless

gaps = rng.exponential(1/5, 100000)              # 5 events per hour
arr = np.cumsum(gaps)
counts = np.bincount(np.floor(arr[arr < 20000]).astype(int))   # events per hour
print(counts.mean().round(3), counts.var().round(3))            # ~5 and ~5: Poisson
```

**Follow-ups:**
- *Inspection paradox?* Randomly arriving users see longer-than-average gaps.
- *Alternative for non-constant hazard?* Weibull.

**Common mistakes:** applying exponential to ageing or churn data, confusing rate and mean (lambda vs 1/lambda), and thinking memoryless means "events are independent of the clock".

### Q24 ⭐⭐ 🟡 Paired vs independent two-sample t-test: when is each valid and what happens if you pick wrong?
**Asked at:** Product cos, GCCs, Booking
**Say this first (1 line):** Use a paired t-test when each observation in one group is naturally matched to one in the other (same user before/after, matched pairs); use the independent t-test when the groups are separate people. Picking independent for paired data throws away the pairing, adds noise and loses power.

**Then explain:**
- Paired: compute the difference for each pair and run a one-sample t-test on differences (df = pairs - 1). Between-subject variation cancels out.
- Independent: compares two group means, assuming the observations are unrelated.
- Wrong choice 1: independent test on paired data. Variance is inflated by person-to-person differences, so you miss real effects (inflated Type II).
- Wrong choice 2: paired test on independent data (pairing arbitrary). Invalid; no meaning, with unequal sizes it can't even be done properly.
- Pairing must come from the design, not from sorting afterwards.

**Example:** Same 30 users' session time before and after redesign: improvement is +3 min on average. Paired p = 0.000007; wrongly using independent gives p = 0.34.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
before = rng.normal(100, 15, 30)
after = before + rng.normal(3, 4, 30)               # same people, small within-person change
print(stats.ttest_rel(after, before).pvalue)         # paired: tiny
print(stats.ttest_ind(after, before).pvalue)         # independent: large -> misses the effect
```

**Follow-ups:**
- *What if some pairs are missing?* Drop them or use a mixed model.
- *Non-parametric paired test?* Wilcoxon signed-rank.

**Common mistakes:** treating repeated measures as independent (also inflates false positives with clustered data), and mixing the two up when the data frame has one row per user per period.

### Q25 ⭐⭐ 🟡 What is Welch's t-test and why is it usually the default over the pooled-variance t-test?
**Asked at:** Product cos, Spotify, Booking
**Say this first (1 line):** Welch's t-test compares two means without assuming equal variances. It costs almost nothing when variances are equal and protects the Type I rate when they are not, so it is the safe default.

**Then explain:**
- Statistic: t = (x1_bar - x2_bar) / sqrt(s1^2/n1 + s2^2/n2). It uses each group's own variance.
- Degrees of freedom (Welch-Satterthwaite) are fractional and usually smaller than n1 + n2 - 2.
- Pooled t-test assumes equal variances and uses one pooled variance. If the group with the larger variance also has the larger n, it is conservative; if it has the smaller n, it is liberal (too many false positives).
- Pre-testing variances with Levene then choosing a test distorts error rates; just use Welch.

**Example:** Group A n = 15 with SD 1, group B n = 60 with SD 4, same mean (null true). Pooled test rejects only 0.1% of the time (too conservative, low power); Welch rejects 4.9% as it should.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
f = g = 0
for _ in range(4000):
    a = rng.normal(0, 1, 15); b = rng.normal(0, 4, 60)         # H0 true, unequal variances
    f += stats.ttest_ind(a, b).pvalue < 0.05                    # pooled
    g += stats.ttest_ind(a, b, equal_var=False).pvalue < 0.05   # Welch
print(f/4000, g/4000)     # pooled 0.001 vs Welch 0.049
```

**Follow-ups:**
- *Is Welch needed for equal n?* With equal n and equal-ish variances the two agree.
- *In scipy?* `equal_var=False` (the default in `ttest_ind` is True!).

**Common mistakes:** leaving scipy's default `equal_var=True`, pre-testing for equal variances, and quoting integer degrees of freedom from the pooled formula.

### Q26 ⭐⭐ 🟡 Explain one-way ANOVA and the F-statistic. What do you do after a significant ANOVA (post-hoc tests)?
**Asked at:** Analytics cos, GCCs, Microsoft IDC
**Say this first (1 line):** One-way ANOVA tests whether three or more group means are all equal. The F-statistic is the ratio of between-group variance to within-group variance; a large F says group means differ more than random noise would explain.

**Then explain:**
- F = MS_between / MS_within, with df (k - 1, N - k). Under H0 (all means equal) F ~ F-distribution.
- Why not many t-tests? k groups give k(k-1)/2 comparisons, inflating the false positive rate (Q13).
- Assumptions: independent observations, roughly normal residuals, equal variances across groups (Welch ANOVA or Kruskal-Wallis if violated).
- Significant ANOVA says "at least one group differs", not which. Post-hoc: Tukey HSD (all pairwise, controls FWER), or Bonferroni/Holm-corrected t-tests; Dunnett if comparing all to one control.
- Report effect size (eta squared) too.

**Example:** Three landing pages with true means 10, 10.5, 12. ANOVA F = 7.57, p = 0.0009; Tukey shows only A vs C differ (A vs B p = 0.07, B vs C p = 0.23).

**Code:**
```python
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
rng = np.random.default_rng(2)
g1, g2, g3 = rng.normal(10, 2, 30), rng.normal(10.5, 2, 30), rng.normal(12, 2, 30)
print(stats.f_oneway(g1, g2, g3))
vals = np.concatenate([g1, g2, g3]); lab = np.repeat(['A', 'B', 'C'], 30)
print(pairwise_tukeyhsd(vals, lab))
```

**Follow-ups:**
- *Two groups?* ANOVA F equals t squared.
- *Unequal variances?* Welch's ANOVA or Games-Howell post-hoc.

**Common mistakes:** running pairwise t-tests without correction, stopping at "significant" with no post-hoc, and doing post-hoc when ANOVA was non-significant.

### Q27 ⭐⭐ 🟡 Fisher's exact test vs chi-squared test: when do you prefer Fisher's?
**Asked at:** Analytics cos, GCCs, health/pharma-leaning teams
**Say this first (1 line):** Both test association in a contingency table, but chi-squared relies on a large-sample approximation while Fisher's computes the exact p-value from the hypergeometric distribution. Prefer Fisher's when counts are small (any expected cell count below about 5), typically for 2x2 tables.

**Then explain:**
- Fisher's conditions on the row and column totals and sums the probabilities of all tables as or more extreme. No approximation, valid for any n.
- Chi-squared's p-value is off when expected counts are small; it tends to be too liberal there.
- For large tables with large counts, chi-squared is fine. Fisher's gets computationally heavy, and scipy's `fisher_exact` handles only 2x2 tables (R handles larger ones).
- Fisher's is also valid for rare events like adverse reactions in small trials.
- Report odds ratio and CI as well.

**Example:** Small pilot: 8 of 10 users converted with the new flow vs 1 of 6 with the old. Expected counts are 2.6-5.6 (some below 5). Fisher p = 0.035; the uncorrected chi-squared says p = 0.013, which overstates the evidence.

**Code:**
```python
import numpy as np
from scipy import stats
t = np.array([[8, 2], [1, 5]])
print(stats.fisher_exact(t))                      # odds ratio 20, p = 0.035
chi2, p, dof, exp = stats.chi2_contingency(t, correction=False)
print(round(p, 4)); print(exp)                    # 0.0134 ; expected counts include 2.625 (<5)
```

**Follow-ups:**
- *Is Fisher's conservative?* Slightly, because of the discrete distribution; mid-p versions exist.
- *Fisher vs Yates-corrected chi-squared?* Fisher is the cleaner choice for small samples.

**Common mistakes:** using chi-squared with tiny expected counts, forgetting scipy's 2x2 limit, and reporting only the p-value without the odds ratio.

### Q28 ⭐⭐ 🟡 How do you test for normality (Shapiro-Wilk, Q-Q plot)? Do you actually need normality for a t-test?
**Asked at:** GCCs, analytics cos, product cos
**Say this first (1 line):** I look at a Q-Q plot and histogram first, and use Shapiro-Wilk as a supporting check for small samples. And mostly no, the t-test needs the *sampling distribution of the mean* to be approximately normal, which the CLT gives for moderate n.

**Then explain:**
- Q-Q plot: sample quantiles vs theoretical normal quantiles. Straight line = normal; heavy tails curve at the ends; skew gives a bow.
- Shapiro-Wilk: H0 = data is normal. Good power for n up to a few thousand. Small p = evidence of non-normality.
- Trap: with large n, tiny harmless deviations are "significant"; with tiny n, the test cannot detect even big deviations. So never decide only from the p-value.
- What matters for the t-test: independence first, then no extreme outliers/skew relative to n. Heavy skew with small n is the real danger. Use Welch, bootstrap, transform, or Mann-Whitney if needed.
- Normality of the *residuals* matters in regression, not of the raw y.

**Example:** Exponential data (very non-normal) with 40 per group and a true null: the t-test still rejects about 5% of the time (0.0465 in my run), so it is robust here. But Shapiro-Wilk on the same kind of data gives p ~ 6e-14.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
x = rng.exponential(1, 200)
print(stats.shapiro(x).pvalue)                       # tiny -> not normal
rej = 0
for _ in range(4000):
    a = rng.exponential(1, 40); b = rng.exponential(1, 40)
    rej += stats.ttest_ind(a, b).pvalue < 0.05
print(rej / 4000)                                    # ~0.05: t-test still holds its Type I rate
big = rng.standard_t(8, 5000)                        # mildly heavy tails, n large
print(stats.shapiro(big).pvalue)                     # very small p although practically harmless
```

**Follow-ups:**
- *Other tests?* Anderson-Darling, D'Agostino K^2, Lilliefors (KS with estimated parameters).
- *Shapiro-Wilk caveat in scipy?* p-values are less reliable above n = 5000.

**Common mistakes:** choosing the test by Shapiro-Wilk p alone, applying normality to raw data when the model needs normal residuals, and using plain KS with estimated parameters.

### Q29 ⭐⭐ 🟡 What is the Kolmogorov-Smirnov test? How do you use it for one-sample and two-sample comparisons (e.g., drift detection)?
**Asked at:** Product cos, fintech (PhonePe/Klarna-type), GCCs
**Say this first (1 line):** The KS test compares cumulative distribution functions: the statistic D is the largest vertical gap between two CDFs (sample vs a reference distribution, or sample vs sample). Large D, small p = the distributions differ.

**Then explain:**
- One-sample: empirical CDF vs a fully specified theoretical CDF (e.g. N(0,1)). If you estimate the parameters from the same data, the standard p-value is wrong (use Lilliefors).
- Two-sample: are two samples from the same distribution? No distributional assumption, works for continuous data.
- Drift detection: compare a feature's training (reference) values with recent production values using `ks_2samp`; alert when p is tiny *and* D is practically large.
- Sensitive to differences near the middle of the distribution, less in the tails. Lower power than a t-test for a pure mean shift in normal data.
- With very large n, even trivial drift is "significant", so use D (or PSI) as the effect size and set thresholds on it.

**Example:** Training feature ~ N(0,1); live feature shifted to mean 0.3. Both with 5,000 rows: D = 0.134, p ~ 9e-40 -> alert. Reference sample checked against N(0,1): D = 0.009, p = 0.76 -> consistent.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
ref = rng.normal(0, 1, 5000); live = rng.normal(0.3, 1, 5000)
print(stats.kstest(ref, 'norm'))        # one-sample: fits N(0,1)
print(stats.ks_2samp(ref, live))        # two-sample: drift detected
```

**Follow-ups:**
- *Discrete or categorical features?* Use chi-squared or PSI, not KS.
- *Alternative for drift?* PSI, Jensen-Shannon, Wasserstein distance.

**Common mistakes:** using KS on categorical/discrete data, estimating parameters then using the plain KS p-value, and alerting on p-value alone at huge n.

### Q30 ⭐⭐ 🟡 Explain sampling methods: simple random, stratified, cluster, systematic. When is stratified better?
**Asked at:** Analytics cos, GCCs, product cos
**Say this first (1 line):** Simple random picks units at random; stratified splits the population into homogeneous groups and samples from each; cluster samples whole groups; systematic takes every k-th unit. Stratified is better when the groups differ a lot on the outcome, because it removes between-group variability from the estimate.

**Then explain:**

| Method | How | Good for | Watch out |
|---|---|---|---|
| Simple random | each unit equal chance | baseline, small frames | rare groups may be missed |
| Stratified | split by strata, sample within each | heterogeneous groups, guaranteed subgroup coverage | need strata info up front |
| Cluster | randomly choose clusters (cities, stores), survey all within | cheap fieldwork, no unit list | higher variance (units inside a cluster are alike) |
| Systematic | every k-th record from a random start | simple, spread out | hidden periodicity biases it |

- Stratified allocation can be proportional or optimal (Neyman: more sample where the group is bigger or more variable).
- In ML: stratified train/test split (`stratify=y`) and stratified k-fold keep class balance, vital with rare positives.

**Example:** Revenue per user is 10, 30 and 80 in three segments making 70%, 20%, 10% of users. Estimating the average with n = 300: SD of the estimate is 1.23 with simple random sampling vs 0.29 with proportional stratification.

**Code:**
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(2)
df = pd.DataFrame({'seg': rng.choice(['A', 'B', 'C'], 100000, p=[.7, .2, .1])})
df['y'] = df.seg.map({'A': 10, 'B': 30, 'C': 80}) + rng.normal(0, 5, len(df))
srs = [df.y.sample(300, random_state=i).mean() for i in range(500)]
strat = [df.groupby('seg').sample(frac=300/len(df), random_state=i).y.mean() for i in range(500)]
print(np.std(srs).round(3), np.std(strat).round(3), df.y.mean().round(2))   # 1.234 vs 0.289; truth 21.04
```

**Follow-ups:**
- *Design effect for clusters?* Roughly 1 + (m - 1) * ICC, so clustering inflates variance.
- *Post-stratification?* Reweight an already collected sample to match known population shares.

**Common mistakes:** confusing strata with clusters (strata: sample from every group; clusters: sample some groups), ignoring clustering in standard errors, and systematic sampling on periodic data.

### Q31 ⭐⭐ 🟡 Pearson vs Spearman vs Kendall correlation: when do you use each?
**Asked at:** Product cos, GCCs, analytics cos
**Say this first (1 line):** Pearson measures linear association between numeric variables; Spearman measures monotonic association using ranks (robust to outliers and non-linear but monotonic shapes); Kendall also uses ranks, based on concordant vs discordant pairs, and works better for small samples and many ties.

**Then explain:**
- **Pearson r:** sensitive to outliers; assumes a linear relationship; best for roughly bivariate normal continuous data.
- **Spearman rho:** Pearson on the ranks. Use for ordinal data, monotonic curves, outliers.
- **Kendall tau:** (concordant - discordant pairs) / total pairs. Smaller values than Spearman for the same data, more robust, with a more direct probabilistic meaning (difference in probability that pairs are in the same vs opposite order). O(n log n) with efficient algorithms.
- None of them detect non-monotonic dependence (e.g. U-shape). None implies causation.

**Example:** y = exp(x/2) + noise is monotonic but curved: Pearson 0.876, Spearman 0.997, Kendall 0.969. Add one extreme outlier and Pearson collapses to 0.58 while Spearman stays 0.97.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
x = rng.uniform(1, 10, 200); y = np.exp(x/2) + rng.normal(0, .5, 200)
print(stats.pearsonr(x, y)[0].round(3), stats.spearmanr(x, y)[0].round(3), stats.kendalltau(x, y)[0].round(3))
x2, y2 = x.copy(), y.copy(); x2[0], y2[0] = 1, 500                  # one outlier
print(stats.pearsonr(x2, y2)[0].round(3), stats.spearmanr(x2, y2)[0].round(3))
```

**Follow-ups:**
- *Which for ordinal survey scores?* Spearman or Kendall.
- *Which for a non-monotone relation?* Mutual information or distance correlation.

**Common mistakes:** using Pearson on skewed or outlier-heavy data, treating Spearman as detecting any dependence, and equating high correlation with causation.

### Q32 ⭐⭐ 🟡 Can two variables have zero correlation and still be dependent? Give an example.
**Asked at:** Product cos, quant-leaning teams
**Say this first (1 line):** Yes. Correlation only measures linear association, so a perfect non-linear relationship like y = x² with x symmetric around zero has correlation zero but y is completely determined by x.

**Then explain:**
- Independent implies uncorrelated, but uncorrelated does **not** imply independent. The converse holds only in special cases, such as jointly normal variables.
- For y = x² with x symmetric, Cov(x, y) = E[x³] = 0 because the positive and negative sides cancel.
- Same story for U-shapes, circles and seasonal patterns: Pearson and even Spearman miss them, since both look only for a straight or monotonic trend.
- Better detectors: mutual information, distance correlation, or just plot the data.

**Example:** Price vs demand for a product that sells best at a middle price: low prices and high prices both give weak sales in a symmetric way, so the correlation is near zero, yet price clearly drives demand.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
x = rng.normal(size=100000)
y = x**2
print(np.corrcoef(x, y)[0, 1].round(3))                    # ~0 correlation
print(stats.spearmanr(x, y)[0].round(3))
print(np.corrcoef(np.abs(x), y)[0, 1].round(3))            # dependence is obvious on |x|
def dcor(a, b):                                            # distance correlation, from scratch
    A = np.abs(a[:, None]-a[None]); B = np.abs(b[:, None]-b[None])
    A = A-A.mean(0)-A.mean(1)[:, None]+A.mean(); B = B-B.mean(0)-B.mean(1)[:, None]+B.mean()
    return np.sqrt((A*B).mean()/np.sqrt((A*A).mean()*(B*B).mean()))
print(dcor(x[:2000], y[:2000]).round(3))
```
Output: Pearson 0.004, Spearman -0.007, corr(|x|, y) 0.935, distance correlation 0.538 (clearly non-zero).

**Follow-ups:**
- *Is there a case where uncorrelated means independent?* Yes, if the two are jointly (bivariate) normal.
- *Why does this matter in ML?* Dropping features with low linear correlation to the target can throw away strong non-linear signal. Tree models and mutual information catch it.

**Common mistakes:** filtering features by Pearson only, saying "r = 0 means no relationship", and forgetting that correlation is a linear measure.

### Q33 ⭐⭐ 🟡 Method of Moments vs MLE: how does MoM work, and when would you prefer one?
**Asked at:** GCCs, Microsoft IDC, research-leaning teams
**Say this first (1 line):** Method of Moments matches sample moments (mean, variance) to theoretical ones and solves for the parameters; MLE picks the parameters that make the observed data most likely. MLE is usually more efficient, MoM is simpler and a good starting point.

**Then explain:**
- **MoM:** set E[X] = sample mean, E[X²] or Var = sample variance, solve the equations. Closed form, no optimisation.
- **MLE:** maximise the likelihood. Asymptotically unbiased, consistent, efficient (reaches the Cramer-Rao bound), and invariant to reparameterisation. Often needs numerical optimisation.
- Prefer **MoM** when the likelihood is hard or you need a quick initial guess (e.g. to start an EM or optimiser). Prefer **MLE** when you want the best precision and the model is right.
- MoM can give impossible values (negative variance, estimate outside the support); MLE respects the parameter space.

**Example:** Uniform(0, θ). MoM: θ̂ = 2 × mean. MLE: θ̂ = max(x). With n = 20 and θ = 10, over 5,000 simulations the MSE is 1.67 for MoM vs 0.43 for MLE. MLE uses the information in the maximum, which MoM ignores.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(3)
x = rng.gamma(shape=3.0, scale=2.0, size=2000)       # true k=3, theta=2
m1, v = x.mean(), x.var()
print('MoM', round(m1**2/v, 3), round(v/m1, 3))      # k = mean^2/var, theta = var/mean
k, _, th = stats.gamma.fit(x, floc=0)                 # MLE
print('MLE', round(k, 3), round(th, 3))
est = np.array([(2*s.mean(), s.max()) for s in (rng.uniform(0, 10, 20) for _ in range(5000))])
print('Uniform MSE MoM, MLE:', ((est-10)**2).mean(0).round(3))
```
Output: Gamma MoM (3.098, 1.971), MLE (3.078, 1.983); uniform MSE [1.668, 0.429].

**Follow-ups:**
- *Is MLE always unbiased?* No. The uniform max underestimates θ, and the normal variance MLE divides by n (biased low). It is consistent though.
- *What is generalised method of moments?* GMM matches more moment conditions than parameters, used a lot in econometrics.

**Common mistakes:** saying MLE is always better in small samples, forgetting MoM can fall outside the parameter space, and mixing up "unbiased" with "consistent".

### Q34 ⭐⭐ 🟡 How are the t, chi-squared and F distributions related? Where does each arise?
**Asked at:** GCCs, analytics cos, Microsoft IDC
**Say this first (1 line):** All three are built from normals: chi-squared is a sum of squared standard normals, t is a normal divided by the square root of a chi-squared over its degrees of freedom, and F is a ratio of two chi-squareds each divided by its df.

**Then explain:**

| Distribution | Built as | Arises in |
|---|---|---|
| χ²(k) | Z₁² + … + Z_k² | variance estimates, goodness-of-fit, independence tests |
| t(k) | Z / √(χ²(k)/k) | mean test when σ is unknown, regression coefficients |
| F(a, b) | (χ²(a)/a) / (χ²(b)/b) | ANOVA, comparing variances, overall regression F-test |

- (n-1)s²/σ² ~ χ²(n-1), and it is independent of the sample mean. That independence is why (x̄ - μ)/(s/√n) is t(n-1).
- t² with k df equals F(1, k). A two-sided t-test and a one-way ANOVA F-test with two groups are the same test.
- As df grows, t becomes normal, and F concentrates around 1 when both dfs are large.

**Example:** 95% two-sided critical value for the mean of n = 10 is 2.262 (t with 9 df), higher than 1.96, because s itself is noisy.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(4)
n = 10; z = rng.normal(size=(200000, n))
chi = (z**2).sum(1)                                   # chi2(n)
t = z.mean(1)/(z.std(1, ddof=1)/np.sqrt(n))           # t(n-1)
f = (rng.chisquare(5, 200000)/5)/(rng.chisquare(20, 200000)/20)   # F(5,20)
print(chi.mean().round(2), chi.var().round(2), '(theory 10, 20)')
print(np.quantile(t, .975).round(3), stats.t.ppf(.975, n-1).round(3))
print(np.quantile(f, .95).round(3), stats.f.ppf(.95, 5, 20).round(3))
print(stats.t.ppf(.975, 9)**2, stats.f.ppf(.95, 1, 9))
```
Output: chi² mean 9.99, variance 20.02; t quantile 2.26 vs 2.262; F quantile 2.726 vs 2.711; t² = F(1,9) = 5.117.

**Follow-ups:**
- *Why does the t have heavier tails?* The denominator s is random, so extra uncertainty widens the tails.
- *When is the chi-squared test of independence valid?* Large expected counts (rule of thumb at least 5 per cell).

**Common mistakes:** forgetting the independence of x̄ and s², saying t is "just a normal with fatter tails" without the reason, and using t when the data are not roughly normal and n is tiny.

### Q35 ⭐⭐ 🟡 What is p-hacking? How do researchers misuse p < 0.05 and how do you guard against it?
**Asked at:** Product cos, Spotify, Booking, Amazon
**Say this first (1 line):** P-hacking is trying many analyses, metrics, segments or stopping points until something crosses p < 0.05, and then reporting only that one. The real false-positive rate is far above 5%.

**Then explain:**
- Common forms: testing many metrics or subgroups, peeking at an A/B test and stopping when significant, dropping "outliers" after seeing the result, trying several models or transformations, and HARKing (inventing the hypothesis after the result).
- Why it works: with k independent tests on pure noise, P(at least one p < 0.05) = 1 - 0.95^k. For k = 20 that is 64%.
- Guards: pre-register the primary metric, sample size and stopping rule; correct for multiple comparisons (Bonferroni, Holm, BH); use sequential tests if you must peek; hold out data or replicate; report all tests run and effect sizes with CIs.

**Example:** An A/B test checks 20 metrics, nothing is truly different, yet one shows "p = 0.03, ship it!". This is expected by chance.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(6)
sims, k, hit, best = 2000, 20, 0, []
for _ in range(sims):
    a = rng.normal(size=(k, 100)); b = rng.normal(size=(k, 100))   # 20 metrics, NO true effect
    p = stats.ttest_ind(a, b, axis=1).pvalue
    hit += (p < .05).any(); best.append(p.min())
print('P(at least one p<.05):', hit/sims, ' theory', round(1-.95**k, 3))
print('with Bonferroni:', np.mean(np.array(best) < .05/k).round(3))
rej = 0
for _ in range(2000):                                  # peek every 10 users from n=20 to 200
    a = rng.normal(size=200); b = rng.normal(size=200)
    rej += any(stats.ttest_ind(a[:n], b[:n]).pvalue < .05 for n in range(20, 201, 10))
print('peeking 19 times, false positive rate:', rej/2000)
```
Output: 0.652 (theory 0.642); Bonferroni 0.046; peeking 19 times gives 0.2165 false positives.

**Follow-ups:**
- *Is peeking always bad?* Peeking with a fixed-sample test is. Group-sequential or always-valid (mSPRT) methods let you peek safely.
- *Is a p-value of 0.049 vs 0.051 different?* Evidence-wise no. Treat p as continuous evidence, and report the CI.

**Common mistakes:** correcting only for the final reported test, not counting the forking paths, and believing a significant result in an exploratory analysis is confirmatory.

### Q36 ⭐⭐ 🟡 Confidence interval for a proportion: Wald vs Wilson. Why does Wald fail for small n or extreme p?
**Asked at:** Product cos, Booking, Spotify
**Say this first (1 line):** Wald is p̂ ± z·√(p̂(1-p̂)/n); it uses the estimated p̂ for the standard error and a normal approximation. For small n or p̂ near 0 or 1 that breaks, so use Wilson (or Clopper-Pearson), which has far better coverage.

**Then explain:**
- Wald fails because the SE is computed at p̂: if p̂ = 0, SE = 0 and the interval collapses to [0, 0], which is absurd. Coverage is also below nominal for small n and extreme p.
- Wilson inverts the score test, using the true-p variance, so it is asymmetric, stays inside [0, 1], and never has zero width.
- Wilson formula centre: (p̂ + z²/2n) / (1 + z²/n). Clopper-Pearson is exact but conservative (too wide). Agresti-Coull is a simple "add 2 successes and 2 failures" fix.
- With big n and p near 0.5 all of them agree.

**Example:** 0 conversions out of 20: Wald gives [0, 0]; Wilson gives [0, 0.161]. For 2 of 20: Wald [0, 0.231] (lower bound clipped), Wilson [0.028, 0.301].

**Code:**
```python
import numpy as np
from statsmodels.stats.proportion import proportion_confint
for x, n in [(0, 20), (2, 20), (50, 100)]:
    print(x, n, 'Wald', np.round(proportion_confint(x, n, method='normal'), 3),
          'Wilson', np.round(proportion_confint(x, n, method='wilson'), 3))
rng = np.random.default_rng(5); n, p = 20, .05
xs = rng.binomial(n, p, 100000)
for m in ['normal', 'wilson']:
    lo, hi = proportion_confint(xs, n, method=m)
    print(m, 'coverage', ((lo <= p) & (p <= hi)).mean().round(3))
```
Output: coverage for n = 20, p = 0.05 is 0.64 for Wald vs 0.923 for Wilson (target 0.95).

**Follow-ups:**
- *Rule of thumb for Wald?* n·p̂ and n·(1-p̂) both at least 10, and even then Wilson is safer.
- *What if there are zero events?* "Rule of three": the upper 95% bound is about 3/n.

**Common mistakes:** using Wald for rare-event rates (fraud, defects), reporting [0, 0] as proof of no risk, and ignoring coverage.

### Q37 ⭐⭐ 🟡 Confidence interval vs prediction interval vs tolerance interval: what is the difference?
**Asked at:** GCCs, analytics cos
**Say this first (1 line):** A confidence interval is about an unknown population parameter (like the mean); a prediction interval is about one future observation; a tolerance interval is about a proportion of the whole population. Widths go CI < PI < tolerance.

**Then explain:**

| Interval | Covers | Width shrinks with n? |
|---|---|---|
| Confidence | the true mean (parameter) | yes, to zero |
| Prediction | next single observation | no, stays near ±z·σ |
| Tolerance (95/95) | at least 95% of the population, with 95% confidence | no, tends to the population quantiles |

- CI: x̄ ± t·s/√n. PI: x̄ ± t·s·√(1 + 1/n). The extra "1" is the new observation's own noise, which more data cannot remove.
- Tolerance has two probabilities: the coverage fraction and the confidence that the interval really covers that fraction.
- In regression: confidence band for the mean line, prediction band for individual points.

**Example:** Delivery times with mean 95.6 min, SD about 13.5, n = 50: CI for average [91.8, 99.4], 95% PI for one order [68.4, 122.8], 95/95 tolerance [63.7, 127.5]. A promise to customers should use the PI or tolerance interval, not the CI.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(7)
x = rng.normal(100, 15, 50); n = len(x); m, s = x.mean(), x.std(ddof=1)
t = stats.t.ppf(.975, n-1)
print('CI :', np.round((m - t*s/np.sqrt(n), m + t*s/np.sqrt(n)), 1))
pw = t*s*np.sqrt(1+1/n); print('PI :', np.round((m - pw, m + pw), 1))
chi = stats.chi2.ppf(.05, n-1); z = stats.norm.ppf(.975)
k = np.sqrt((n-1)*(1+1/n)*z**2/chi)                  # Howe approximation, normal data
print('tol:', np.round((m - k*s, m + k*s), 1))
```
Output: CI [91.8, 99.4], PI [68.4, 122.8], tolerance [63.7, 127.5].

**Follow-ups:**
- *Do PIs need normality?* They rely on it much more than CIs do, since there is no CLT for a single observation. Use quantile or conformal prediction otherwise.
- *ML link?* Conformal prediction gives distribution-free prediction intervals.

**Common mistakes:** using a CI to say where individual values fall, thinking a 95% CI contains 95% of the data, and forgetting that PI does not shrink to zero with n.

### Q38 ⭐⭐ 🟡 FWER vs FDR: how do Bonferroni, Holm and Benjamini-Hochberg differ in what they control and in power?
**Asked at:** Product cos, Europe product cos
**Say this first (1 line):** FWER (family-wise error rate) is the probability of making even one false rejection; FDR (false discovery rate) is the expected share of rejections that are false. Bonferroni and Holm control FWER, Benjamini-Hochberg controls FDR and has much more power.

**Then explain:**
- **Bonferroni:** reject if p ≤ α/m. Simple, conservative.
- **Holm:** sort p-values, compare the i-th smallest to α/(m - i + 1), stop at the first failure. Always at least as powerful as Bonferroni, same FWER guarantee, no extra assumptions.
- **BH:** sort p-values, find the largest i with p₍ᵢ₎ ≤ (i/m)·α, reject all up to it. Controls FDR at α for independent (or positively dependent) tests.
- Use FWER when one false positive is costly (confirmatory trials, a few launch decisions). Use FDR for screening many hypotheses (genes, hundreds of A/B metrics or segments), where you accept a few false leads.

**Example:** 1,000 tests, 100 truly real (z-mean 3). Uncorrected: 126 rejections, 43 false. Bonferroni/Holm: 18 rejected, 0 false. BH: 49 rejected, 46 real and 3 false (about 6% FDR).

**Code:**
```python
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
rng = np.random.default_rng(8)
m, m1 = 1000, 100
z = np.r_[rng.normal(3, 1, m1), rng.normal(0, 1, m-m1)]
p = 2*stats.norm.sf(np.abs(z)); real = np.arange(m) < m1
for name in ['bonferroni', 'holm', 'fdr_bh']:
    rej = multipletests(p, alpha=.05, method=name)[0]
    print(f'{name:10s} rejected={rej.sum():3d} true={(rej&real).sum():3d} false={(rej&~real).sum():3d}')
print('uncorrected rejected', (p < .05).sum(), ' false', ((p < .05)&~real).sum())
```
Output: as in the example. Holm equalled Bonferroni on this run; it gains power mostly when many hypotheses are non-null.

**Follow-ups:**
- *Which does BH guarantee exactly?* FDR ≤ (m₀/m)·α for independent tests, not a per-experiment bound.
- *And for dependent tests?* See Benjamini-Yekutieli (Q58).

**Common mistakes:** applying Bonferroni to thousands of tests and finding nothing, interpreting FDR 5% as "each discovery has 5% chance to be false" (it is an average), and correcting only the tests you happened to report.

### Q39 ⭐⭐ 🟡 Your conversion rate went from 10.0% to 10.4% with 50,000 users per arm. Run the two-proportion z-test and interpret it.
**Asked at:** Swiggy, Flipkart, Amazon, PhonePe
**Say this first (1 line):** z = 2.09, two-sided p = 0.037, so it is statistically significant at 5%. But the lift is only 0.4 percentage points (4% relative), the 95% CI is [0.02, 0.78] pp, and whether it is worth shipping is a business call.

**Then explain:**
- Hypotheses: H0: p_B = p_A. Pooled p = 0.102; SE = √(p(1-p)·2/n) ≈ 0.00191; z = 0.004/0.00191.
- Use the pooled SE for the test (H0 says they are equal) and the unpooled SE for the confidence interval.
- The CI barely excludes zero: the true effect could be almost nothing or nearly 0.8 pp. Significance is borderline.
- Practical check: is 0.4 pp worth the cost, risk, novelty effect? Also check guardrail metrics, sample ratio mismatch, and whether this was the single pre-planned metric (otherwise p = 0.037 may not survive multiple-testing correction).
- This test was powered to detect roughly 0.55 pp, not 0.4: to detect 0.4 pp with 80% power you need about 90,000 per arm. So the result is on the noisy edge and may overestimate the true lift (winner's curse).

**Example:** 5,200/50,000 vs 5,000/50,000. Relative lift 4%; at 10 lakh users a year, an extra 0.4% is about 4,000 extra conversions, which you then price against the build cost.

**Code:**
```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
n = 50000; x = np.array([5200, 5000]); nn = np.array([n, n])
z, p = proportions_ztest(x, nn)
p1, p2 = x/nn
se_unp = np.sqrt(p1*(1-p1)/n + p2*(1-p2)/n); d = p1-p2
print('z, p =', round(z, 3), round(p, 4))
print('diff =', round(d, 4), ' 95% CI =', np.round((d-1.96*se_unp, d+1.96*se_unp), 4))
print('relative lift =', round(d/p2, 3))
pb = .102; print('n per arm for 80% power ~', int(2*pb*(1-pb)*((1.96+.8416)/.004)**2))
```
Output: z = 2.09, p = 0.0366, diff 0.004, CI [0.0002, 0.0078], relative lift 0.04, n per arm about 89,866.

**Follow-ups:**
- *Would you ship?* Only if the pre-registered primary metric, guardrails and cost-benefit support it. Consider a rerun or a longer test, since the CI is close to zero.
- *Why z and not t?* With 50,000 per arm they are identical; for proportions z is standard.

**Common mistakes:** saying "p < 0.05 so the lift is real and 4%", forgetting the CI, using the pooled SE for the CI, and ignoring practical significance.

### Q40 ⭐⭐ 🟡 Explain degrees of freedom intuitively. Why does the t-distribution depend on it?
**Asked at:** GCCs, analytics cos
**Say this first (1 line):** Degrees of freedom is the number of independent pieces of information left after you estimate parameters from the data. For a sample variance it is n - 1, because the deviations from the sample mean must sum to zero.

**Then explain:**
- With n numbers and the mean already fixed, once you know n - 1 of the deviations the last one is forced. So only n - 1 are "free".
- Dividing by n - 1 (Bessel's correction) makes the variance unbiased, since deviations from x̄ are smaller than deviations from the true μ.
- The t-distribution depends on df because s is estimated from n - 1 free values. Small df means a noisy s, so heavier tails and wider intervals. As df grows, s is accurate and t becomes the normal.
- In regression, df = n - number of parameters. In chi-squared tests of independence, df = (rows - 1)(columns - 1).

**Example:** With 5 df the 97.5% cutoff is 2.571, with 30 df 2.042, with 1,000 df 1.962, close to normal 1.960.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(9)
x = rng.normal(0, 1, (100000, 5))
print('divide by n  :', x.var(1, ddof=0).mean().round(3), '(biased, true 1)')
print('divide by n-1:', x.var(1, ddof=1).mean().round(3))
print('max |sum of deviations|:', np.abs((x - x.mean(1, keepdims=True)).sum(1)).max().round(10))
for df in [2, 5, 30, 1000]:
    print(df, 'df: t 97.5% =', stats.t.ppf(.975, df).round(3))
print('normal 97.5% =', stats.norm.ppf(.975).round(3))
```
Output: biased 0.802 vs unbiased 1.002 (expected 0.8 = (n-1)/n for n = 5); deviations sum to 0; t cutoffs 4.303, 2.571, 2.042, 1.962 vs normal 1.960.

**Follow-ups:**
- *Is df always an integer?* No. Welch's t-test uses a fractional df (Satterthwaite).
- *What is "residual df" in a model?* Observations minus fitted parameters. Overfitting eats df and leaves little to estimate the noise.

**Common mistakes:** thinking df is just "sample size minus one" for everything, not knowing why n - 1 appears, and treating t and z as different once n is large.

### Q41 ⭐⭐ 🟡 What is effect size (Cohen's d, relative lift) and why report it alongside a p-value?
**Asked at:** Amazon, Spotify, Booking
**Say this first (1 line):** Effect size says how big the difference is; the p-value only says whether it is distinguishable from noise. With enough users a trivial effect gets a tiny p-value, so always report both.

**Then explain:**
- **Cohen's d** = (mean₁ - mean₂) / pooled SD. Unit-free. Rough guide: 0.2 small, 0.5 medium, 0.8 large (a convention, not a law; judge by context).
- **Relative lift** = (B - A) / A. Business-friendly. Absolute difference matters too (0.4 pp on a 10% base).
- The p-value depends on n; the true effect size does not. A true d = 0.1 is usually not significant at n = 50 per arm (the run below gave p = 0.31) and gives p near zero at n = 50,000.
- Report an effect size with a confidence interval, then judge against the minimum effect worth shipping (MDE / practical threshold).

**Example:** True effect d = 0.1 (1% lift on revenue per user). At n = 50 the test is not significant (p = 0.31, d = 0.20 by chance). At n = 50,000 p = 1e-49, d = 0.094, lift 0.94%. Significance changed, the effect did not.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(10)
def cohen_d(a, b):
    sp = np.sqrt(((len(a)-1)*a.var(ddof=1) + (len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2))
    return (a.mean()-b.mean())/sp
for n in [50, 500, 50000]:
    a = rng.normal(10.1, 1, n); b = rng.normal(10.0, 1, n)    # tiny true effect, d = 0.1
    print(n, 'p=%.2g' % stats.ttest_ind(a, b).pvalue, 'd=%.3f' % cohen_d(a, b), 'lift=%.2f%%' % (100*(a.mean()/b.mean()-1)))
```
Output: n=50 p=0.31 d=0.204 lift 1.75%; n=500 p=0.26 d=0.071 lift 0.72%; n=50,000 p=1.2e-49 d=0.094 lift 0.94%.

**Follow-ups:**
- *Is Cohen's d the right measure for binary metrics?* Prefer absolute difference, relative lift, odds ratio, or Cohen's h.
- *Why does small-n d bounce around?* The estimate is noisy; in this run it came out 0.20 at n = 50 when the truth is 0.1.

**Common mistakes:** celebrating p < 0.05 without the size, treating 0.2/0.5/0.8 as universal cut-offs, and quoting a relative lift without the baseline.

### Q42 ⭐⭐ 🟡 What is the duality between confidence intervals and hypothesis tests?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** A 95% confidence interval is exactly the set of null values you would NOT reject at the 5% level. If the interval excludes a value, the two-sided test at α = 0.05 rejects that value.

**Then explain:**
- Test of H0: θ = θ₀ at level α rejects iff θ₀ is outside the (1 - α) CI. So "CI excludes 0" is the same as "p < 0.05" for H0: difference = 0.
- The CI is more informative: it shows the range of effect sizes that are compatible with the data, not just zero vs not zero.
- It also lets you test other nulls (like "lift is at most 1%") without a new test.
- The duality is exact only when the CI and the test use the same method. For example, a pooled-SE z-test and an unpooled Wald CI for proportions can disagree in borderline cases.

**Example:** Difference in mean 0.187, 95% CI [-0.193, 0.566]: includes 0, so p = 0.33 for H0: diff = 0. Testing H0: diff = 0.7 gives p = 0.008, and 0.7 is outside the CI. Testing H0: diff = 0.5 gives p = 0.105, and 0.5 is inside.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(11)
a = rng.normal(10.3, 2, 200); b = rng.normal(10.0, 2, 200)
res = stats.ttest_ind(a, b, equal_var=False)
ci = res.confidence_interval(0.95)
print('diff', round(a.mean()-b.mean(), 3), 'p', round(res.pvalue, 4), 'CI', np.round([ci.low, ci.high], 3))
for null in [0, 0.1, 0.5, 0.7]:
    p = stats.ttest_ind(a, b + null, equal_var=False).pvalue      # tests H0: diff = null
    print('H0 diff =', null, 'p =', round(p, 4), 'inside CI:', bool(ci.low <= null <= ci.high))
```
Output: diff 0.187, p 0.3341, CI [-0.193, 0.566]; p-values 0.334, 0.654, 0.105, 0.008, and the 0.7 case is the only one outside the CI.

**Follow-ups:**
- *Does the duality hold for one-sided tests?* One-sided tests match one-sided CI bounds at level α.
- *Why prefer CIs in reports?* They show magnitude and precision, and they work for equivalence and non-inferiority questions (Q59).

**Common mistakes:** reading a 95% CI as "95% chance the parameter is inside" (that is Bayesian credible-interval language), saying overlapping CIs of two groups mean no significant difference (they can overlap and still differ significantly), and mixing a one-sided test with a two-sided CI.

### Q43 ⭐⭐ 🟡 How do you choose the right distribution for real data: delivery time, number of orders per hour, conversion rate, order value?
**Asked at:** Swiggy, Flipkart, Zalando, Klarna
**Say this first (1 line):** Look at what the variable is: a positive right-skewed continuous time or amount is lognormal or gamma, a count of events per interval is Poisson (or negative binomial if overdispersed), and a yes/no rate is Bernoulli or binomial, with beta for the uncertainty about a rate.

**Then explain:**

| Data | Typical distribution | Why |
|---|---|---|
| Delivery time | lognormal / gamma / Weibull | positive, right-skewed, multiplicative delays |
| Orders per hour | Poisson (negative binomial if variance > mean) | counts of independent events |
| Conversion rate | Bernoulli per user, Binomial per day, Beta for the rate | 0/1 outcomes, bounded rate |
| Order value | lognormal (or Pareto tail), often with a spike of zeros | positive, heavy right tail |

- Check with a histogram, log-histogram, Q-Q plot, mean vs variance (Poisson has mean = variance), and goodness-of-fit (KS, AIC).
- Reason from the process: sums of many effects give normal; products give lognormal; waiting for events gives exponential/gamma; rare independent events give Poisson.
- Real data are often mixtures (zeros plus spend, peak vs off-peak), so model the pieces.

**Example:** Simulated delivery times have skew 1.23, but skew -0.01 after log, so lognormal fits (KS p = 0.935, though optimistic since the parameters were fitted on the same data). Orders per hour have mean 12.03 and variance 11.98, as Poisson implies. Order value has skew 3.02, mean 571 against median 419.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(12)
delivery = rng.lognormal(3.4, .4, 5000); orders = rng.poisson(12, 5000)
value = rng.lognormal(6, .8, 5000)
print('delivery skew %.2f' % stats.skew(delivery), ' log-skew %.2f' % stats.skew(np.log(delivery)))
print('orders mean %.2f var %.2f' % (orders.mean(), orders.var()))
print('value skew %.2f, mean %.0f > median %.0f' % (stats.skew(value), value.mean(), np.median(value)))
s, loc, sc = stats.lognorm.fit(delivery, floc=0)
print('lognorm sigma %.3f mu %.3f' % (s, np.log(sc)), ' KS p=%.3f' % stats.kstest(delivery, 'lognorm', args=(s, 0, sc)).pvalue)
```
Output: skew 1.23 to -0.01 after log; orders 12.03 vs 11.98; value skew 3.02, mean 571 vs median 419; fit sigma 0.398, mu 3.403, KS p = 0.935.

**Follow-ups:**
- *Why not just assume normal?* Skew and tails break t-based intervals for means in small samples and give impossible negative values.
- *Orders per hour, but variance is 3x the mean?* Overdispersed: use negative binomial (Q57).

**Common mistakes:** picking a distribution by looking at a histogram alone, using the KS p-value after fitting parameters on the same data (it is too optimistic), and ignoring zero-inflation.

### Q44 ⭐⭐ 🟡 How do you compute a sample size to estimate a mean (or proportion) within a given margin of error?
**Asked at:** Analytics cos, survey/market-research teams, GCCs
**Say this first (1 line):** Solve the margin-of-error formula for n: for a mean n = (z·σ/E)², for a proportion n = z²·p(1-p)/E². With 95% confidence, σ = 15 and E = 2 you need 217 people; for a proportion within 3 points use p = 0.5 and get 1,068.

**Then explain:**
- z is 1.96 for 95% confidence. E is the half-width of the interval you can tolerate.
- σ is unknown in advance: take it from a pilot, past data, or a conservative guess. For proportions p = 0.5 is the worst case (largest variance).
- Halving E needs 4x the sample, because error shrinks with √n.
- Population small (sample is more than about 5% of it)? Apply the finite population correction n' = n / (1 + (n-1)/N).
- If the data are clustered or sampled with weights, multiply by the design effect (Q61). Add extra for expected non-response.

**Example:** Customer-satisfaction survey, 95% confidence, ±3 points, p unknown: n = 1,068. If the customer base is only 5,000, correction gives 880.

**Code:**
```python
import numpy as np
from scipy import stats
z = stats.norm.ppf(.975)
n_mean = (z*15/2)**2                      # sigma=15, margin E=2
n_prop = z**2*.5*.5/.03**2                # p=0.5, margin 3 points
print('mean: n =', int(np.ceil(n_mean)), ' proportion: n =', int(np.ceil(n_prop)))
N = 5000; print('with FPC for N=5000:', int(np.ceil(n_prop/(1+(n_prop-1)/N))))
rng = np.random.default_rng(13); n = int(np.ceil(n_mean))
m = rng.normal(100, 15, (20000, n))
print('P(|xbar-mu|<=2) =', (np.abs(m.mean(1)-100) <= 2).mean().round(3))   # should be ~0.95
```
Output: n = 217 (mean), 1,068 (proportion), 880 with FPC; simulated coverage 0.946.

**Follow-ups:**
- *What if σ is unknown and n is small?* Use t quantiles iteratively, or a pilot-based σ plus a safety margin.
- *How does this differ from A/B test sample size?* Here we estimate one quantity with a given precision; A/B sizing also needs power (Q50) and an effect size.

**Common mistakes:** using σ from a different population, forgetting that 4x sample halves the error, and not rounding up.

### Q45 ⭐⭐ 🟡 Implement a two-sample (Welch) t-test from scratch in NumPy and verify against scipy.stats.ttest_ind.
**Asked at:** Live-coding rounds at product cos and GCCs
**Say this first (1 line):** Welch's t is (mean₁ - mean₂) / √(s₁²/n₁ + s₂²/n₂), with degrees of freedom from the Welch-Satterthwaite formula, so it does not assume equal variances.

**Then explain:**
- Each group's variance of the mean is s²/n. Add them, take the square root, divide the mean difference by it.
- Df: (v₁ + v₂)² / (v₁²/(n₁-1) + v₂²/(n₂-1)) where v = s²/n. It is fractional, between min(n₁, n₂) - 1 and n₁ + n₂ - 2.
- p-value: two-sided tail of t with those df, `2 * t.sf(|t|, df)`.
- Use `ddof=1` for sample variances. Default to Welch: when variances are equal it loses almost nothing, when unequal it keeps the error rate right.

**Example:** Group A: n = 40, SD about 2; group B: n = 70, SD about 5. The variances are very unequal, so pooling would be wrong. Our result t = -1.0756, df = 107.49, p = 0.2845, identical to scipy.

**Code:**
```python
import numpy as np
from scipy import stats
def welch_t(a, b):
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1)/na, b.var(ddof=1)/nb
    t = (a.mean()-b.mean())/np.sqrt(va+vb)
    df = (va+vb)**2/(va**2/(na-1) + vb**2/(nb-1))     # Welch-Satterthwaite
    return t, df, 2*stats.t.sf(abs(t), df)
rng = np.random.default_rng(14)
a = rng.normal(10, 2, 40); b = rng.normal(11, 5, 70)
print(np.round(welch_t(a, b), 5))
r = stats.ttest_ind(a, b, equal_var=False)
print(round(r.statistic, 5), round(r.df, 5), round(r.pvalue, 5))
```
Output: ours [-1.07562, 107.49256, 0.2845]; scipy -1.07562, 107.49256, 0.2845. They match.

**Follow-ups:**
- *Does Welch need normality?* Approximately, or large n via CLT. For heavy tails use bootstrap or permutation (Q47, Q48).
- *Paired data?* Use a paired t-test on differences (ttest_rel), which removes between-subject noise.

**Common mistakes:** using `ddof=0`, using pooled variance with unequal n and unequal variance, and using integer df.

### Q46 ⭐⭐ 🟡 What is regression to the mean and the winner's curse? How do they distort the analysis of top-performing segments?
**Asked at:** Product cos, Amazon, Booking
**Say this first (1 line):** Regression to the mean: an extreme measurement tends to be followed by a less extreme one, because part of what made it extreme was luck. Winner's curse: the best of many noisy estimates is biased upward, because selection picks the lucky ones.

**Then explain:**
- Observed = true quality + noise. Choosing the top by observed value selects both high quality and positive noise. A fresh measurement has fresh noise, so it falls back.
- The more noise relative to the real spread, and the more candidates you choose from, the bigger the drop.
- It distorts analysis: top-performing stores, campaigns, or A/B variants look great, then disappoint. Treating the drop as a "treatment effect" (e.g., after coaching the worst agents) is a classic fallacy.
- Fixes: use a separate validation sample for the selected winners, shrink estimates toward the overall mean (empirical Bayes / hierarchical model), use a control group, and correct for the number of comparisons.

**Example:** 1,000 segments, true quality SD 1, measurement noise SD 2. The top 50 by week 1 average 4.59. In week 2, the same 50 average only 0.60. Their true average quality is 0.84. Overall mean is about 0.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(15)
true_q = rng.normal(0, 1, 1000)                     # true quality of 1000 segments
week1 = true_q + rng.normal(0, 2, 1000)             # noisy measurement
week2 = true_q + rng.normal(0, 2, 1000)             # fresh, independent measurement
top = np.argsort(week1)[-50:]                       # top 5% in week 1
print('top-50 week1 mean   %.2f' % week1[top].mean())
print('same, week2 mean    %.2f' % week2[top].mean())
print('their true quality  %.2f' % true_q[top].mean())
print('overall mean        %.2f' % week2.mean())
```
Output: 4.59, 0.60, 0.84, -0.08.

**Follow-ups:**
- *How do you avoid it in A/B tests with many variants?* Re-test the winner, or shrink estimates; the first-round lift is inflated.
- *Is it related to overfitting?* Yes: choosing the best of many models on one validation set gives an optimistic score. Use a final untouched test set.

**Common mistakes:** attributing the improvement or decline of extreme groups to an intervention without a control, quoting the winning variant's observed lift as the expected lift, and picking the top segment on one noisy sample.

### Q47 ⭐⭐ 🔴 Revenue-per-user is heavy-tailed. Is a t-test still valid? What would you do (log transform, trimming, bootstrap, Mann-Whitney)?
**Asked at:** Amazon, Flipkart, Booking, Zalando
**Say this first (1 line):** With a large sample the Welch t-test on the mean is still roughly valid because of the CLT, but heavy tails make it slow to kick in and give low power. I would pick the method by the question: the mean revenue difference needs the mean (t-test or bootstrap, maybe capped), while Mann-Whitney and log transforms answer different questions.

**Then explain:**
- **Welch t / bootstrap on the mean:** answers the business question "did total revenue per user change?". Valid at large n; the bootstrap shows the skew in the interval. Variance can be dominated by a few whales.
- **Winsorize / cap** extreme values (say at the 99.9th percentile), decided before the test: lowers variance, but changes the metric.
- **Log transform:** compares geometric means or ratios, not the arithmetic mean. Zeros need log1p, which is sensitive to the +1 choice.
- **Mann-Whitney:** tests whether one group tends to be larger (stochastic dominance), not the mean. With 95% zeros it is dominated by ties and can be blind to what happens among payers.
- Variance reduction (CUPED with pre-period revenue) cuts noise much more than switching tests. Also consider modelling the pieces: conversion rate x revenue per payer.

**Example:** Simulated: 5% payers with lognormal order values, 3,000 users per arm. With no true effect, rejection rates are about 4% (Welch), 6% (Mann-Whitney) and 5% (log1p t-test). With a real lift in payer spend, power is about 36% in the 300-run script below (Welch; 42% in a 1,500-run check, so read it as roughly 40%), but only about 5% for Mann-Whitney and 11-13% for the log1p t-test. The bootstrap CI for the mean difference is [-0.82, 4.63] (observed 1.9), correctly showing it is too noisy to call.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(16)
def sample(n, lift):                        # 5% payers, lognormal order value, rest are zeros
    pay = rng.random(n) < .05
    return np.where(pay, rng.lognormal(4 + lift, 1.2, n), 0.0)
sims = 300
for tag, lift in [('no effect', 0), ('real lift', .4)]:
    r = dict(welch=0, mannwhitney=0, log1p_t=0)
    for _ in range(sims):
        a, b = sample(3000, lift), sample(3000, 0)
        r['welch'] += stats.ttest_ind(a, b, equal_var=False).pvalue < .05
        r['mannwhitney'] += stats.mannwhitneyu(a, b).pvalue < .05
        r['log1p_t'] += stats.ttest_ind(np.log1p(a), np.log1p(b)).pvalue < .05
    print(tag, {k: round(float(v)/sims, 3) for k, v in r.items()})
a, b = sample(3000, .4), sample(3000, 0)
bs = [rng.choice(a, 3000).mean()-rng.choice(b, 3000).mean() for _ in range(2000)]
print('diff in mean', round(a.mean()-b.mean(), 2), ' bootstrap 95% CI', np.round(np.percentile(bs, [2.5, 97.5]), 2))
```
Output: no effect {welch 0.04, mannwhitney 0.06, log1p_t 0.05}; real lift {welch 0.36, mannwhitney 0.05, log1p_t 0.127}; diff 1.9, CI [-0.82, 4.63].

**Follow-ups:**
- *Is it OK to drop outliers?* Only by a rule fixed in advance (cap/winsorize); dropping whales after seeing results is p-hacking and removes real revenue.
- *How big must n be for CLT to work?* Depends on skew; heavier tails need far more. Check by bootstrapping the sampling distribution.

**Common mistakes:** switching to Mann-Whitney and then talking about the mean, using log-revenue and reporting the lift as arithmetic, and removing top spenders after seeing the data.

### Q48 ⭐ 🟡 What is a permutation test? When is it preferable to a t-test and how do you implement it?
**Asked at:** Product cos, Spotify, Booking
**Say this first (1 line):** A permutation test builds the null distribution by shuffling the group labels many times and recomputing the statistic; the p-value is the share of shuffles at least as extreme as what you saw. It makes no distributional assumption and works for any statistic.

**Then explain:**
- Logic: if the treatment does nothing, labels are interchangeable (exchangeability), so any shuffle is equally likely under H0.
- Preferable to a t-test when n is small, data are skewed, or the statistic is odd (median, ratio, correlation, AUC difference).
- Steps: compute the observed statistic; shuffle labels B times; compute the statistic each time; p = (count + 1) / (B + 1).
- It tests the sharp null "no difference in distributions", not a pure mean-difference null. If variances differ, the p-value for a mean difference can be off.
- Cost: B recomputations. Use random shuffles rather than all permutations.

**Example:** Two skewed samples (n = 30 and 25, exponential, means 10 and 14). Observed difference -6.52; permutation p = 0.030, Welch p = 0.037, scipy's permutation_test p = 0.028. Same conclusion, fewer assumptions.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(20)
a = rng.exponential(10, 30); b = rng.exponential(14, 25)
obs = a.mean()-b.mean()
pool = np.r_[a, b]; B = 10000; cnt = 0
for _ in range(B):
    rng.shuffle(pool)
    cnt += abs(pool[:len(a)].mean()-pool[len(a):].mean()) >= abs(obs)
print('obs diff %.2f  permutation p = %.4f' % (obs, (cnt+1)/(B+1)))
print('Welch p = %.4f' % stats.ttest_ind(a, b, equal_var=False).pvalue)
r = stats.permutation_test((a, b), lambda x, y: x.mean()-y.mean(), n_resamples=9999, random_state=1)
print('scipy permutation_test p = %.4f' % r.pvalue)
```
Output: obs diff -6.52, permutation p = 0.0299, Welch p = 0.0371, scipy 0.0282.

**Follow-ups:**
- *Permutation vs bootstrap?* Permutation tests a null hypothesis (p-value). Bootstrap estimates uncertainty (CI). Different jobs.
- *When does it fail?* When data are not exchangeable: clustered, time series, or paired data (shuffle within pairs by sign flips).

**Common mistakes:** forgetting the +1 in (count + 1)/(B + 1) (p can be 0), using it on dependent data, and shuffling labels without respecting the experiment's design (blocks, pairs).

### Q49 ⭐ 🟡 Wilcoxon signed-rank and Kruskal-Wallis: what do they test and what are their assumptions?
**Asked at:** Analytics cos, GCCs
**Say this first (1 line):** Wilcoxon signed-rank is the non-parametric paired-test: it asks whether the paired differences are centred at zero. Kruskal-Wallis is the non-parametric one-way ANOVA: it asks whether k independent groups come from the same distribution.

**Then explain:**
- **Wilcoxon signed-rank:** rank the absolute paired differences, sum the ranks of the positive ones. Assumes the pairs are independent and the differences are symmetric around their median (needed to read it as a test of the median shift). Drops zero differences.
- **Kruskal-Wallis:** rank all observations together, compare mean ranks across groups. Assumes independent groups, ordinal or continuous data. To read it as a test of medians, group shapes must be similar; otherwise it tests stochastic dominance.
- Both use ranks, so they are robust to outliers and skew; they lose a little power vs t/ANOVA when data are truly normal (about 95%).
- Kruskal-Wallis only says "some group differs". Follow with post-hoc pairwise tests (Dunn) with correction.

**Example:** Before/after times for 25 users (skewed): Wilcoxon p = 0.0061, paired t p = 0.0082. Three skewed groups: Kruskal-Wallis p = 0.00083, ANOVA p = 0.00039. Same decision here.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(21)
before = rng.lognormal(3, .5, 25); after = before*rng.lognormal(-.1, .2, 25)
print('Wilcoxon p = %.4f' % stats.wilcoxon(before, after).pvalue, ' paired t p = %.4f' % stats.ttest_rel(before, after).pvalue)
g1, g2, g3 = rng.lognormal(3, .5, 30), rng.lognormal(3.2, .5, 30), rng.lognormal(3.6, .5, 30)
print('Kruskal p = %.5f' % stats.kruskal(g1, g2, g3).pvalue, ' ANOVA p = %.5f' % stats.f_oneway(g1, g2, g3).pvalue)
```
Output: Wilcoxon 0.0061 vs paired t 0.0082; Kruskal 0.00083 vs ANOVA 0.00039.

**Follow-ups:**
- *Wilcoxon signed-rank vs sign test?* The sign test uses only signs (fewer assumptions, less power); signed-rank also uses magnitudes.
- *Wilcoxon rank-sum?* That is the two-sample test, equivalent to Mann-Whitney (Q55).

**Common mistakes:** using signed-rank on independent groups, calling these "assumption-free" (they still need independence), and running Kruskal-Wallis without any post-hoc follow-up.

### Q50 ⭐ 🟡 How do you estimate power by Monte Carlo simulation when no closed-form formula exists?
**Asked at:** Amazon, Spotify, Booking, senior roles
**Say this first (1 line):** Simulate your actual data-generating process and test, many times: the share of runs that reject H0 under a real effect is the power, and under no effect it checks the false-positive rate. No formula is needed.

**Then explain:**
- Steps: (1) write a function that generates one dataset under an assumed effect, with realistic noise, skew, clustering, dropout. (2) apply the exact test you will use. (3) repeat thousands of times. (4) power = fraction with p < α.
- Run it at effect = 0 first to confirm the type I error is near 5%; then at the target effect over a grid of n and pick the smallest n reaching 80%.
- Standard error of the simulated power with S runs is about √(p(1-p)/S): 2,000 runs gives ±1 percentage point at p = 0.5.
- Use it for non-normal metrics, clustered randomisation, sequential tests, CUPED-adjusted analyses, or multiple-testing procedures.

**Example:** Revenue-like lognormal metric, Mann-Whitney test, 25% lift. Type I error 0.046 at n = 100 per arm. Power: 0.205 at n = 50, 0.330 at n = 100, 0.575 at n = 200. So you need far more than 200 per arm for 80%.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(22)
def power(n, effect, sims=2000):
    hits = 0
    for _ in range(sims):
        a = rng.lognormal(0, 1, n); b = rng.lognormal(0, 1, n)*effect   # multiplicative lift
        hits += stats.mannwhitneyu(a, b).pvalue < .05
    return hits/sims
print('type I error (effect=1):', power(100, 1.0))
for n in [50, 100, 200]:
    print(n, 'power at 25% lift:', power(n, 1.25))
```
Output: type I 0.046; power 0.205, 0.33, 0.575.

**Follow-ups:**
- *Why not a power formula?* Formulas need assumptions (normality, equal variance); simulation uses your real test and data shape.
- *Where do you get the effect size and noise?* Past experiments or bootstrap from historical data, then pick the minimum effect worth detecting.

**Common mistakes:** too few simulations, forgetting to check type I error at effect = 0, powering for an optimistic effect (see Q46), and computing "post-hoc power" from the observed effect.

### Q51 ⭐ 🟡 An LLM gives you a statistical analysis (test choice, p-value, interpretation) for your data. How do you review it for errors?
**Asked at:** AI-era rounds at product cos and GCCs
**Say this first (1 line):** I treat LLM stats output as a draft from a confident junior: I check that the test matches the study design, the assumptions hold, the numbers reproduce when I re-run the code, and the interpretation says only what a p-value can say.

**Then explain (review checklist):**
- **Design match:** paired vs independent, one vs two-sided, clustered users, repeated measures, unit of randomisation = unit of analysis?
- **Assumptions:** sample size, skew/outliers, independence, equal variance, expected counts.
- **Reproduce:** re-run it yourself with a seed; do not trust numbers the model "computed" in text. LLMs often hallucinate p-values.
- **Multiplicity and stopping:** how many metrics or segments were tried; was the test peeked at?
- **Interpretation:** p is not "probability the hypothesis is true", "not significant" is not "no effect", and an effect size and CI should be given.

**Example (buggy LLM output):** "Same 30 users measured before and after; independent t-test gives p = 0.64, so the feature has no effect. A p-value of 0.64 means a 64% chance the null is true."

Bugs: (1) before/after on the same users is paired data, and an independent test ignores the correlation, so it has too much noise; (2) the p-value is misread as the probability that H0 is true; (3) "no significant" is treated as "no effect" with no CI.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(23)
before = rng.normal(100, 20, 30)
after = before + rng.normal(3, 4, 30)                 # same users, strongly correlated
print('LLM (independent t): p = %.3f' % stats.ttest_ind(after, before).pvalue)   # wrong design
print('Correct (paired t) : p = %.2g' % stats.ttest_rel(after, before).pvalue)
```
Output: independent t p = 0.641 (misses the effect), paired t p = 0.0051.

**Follow-ups:**
- *How would you use the LLM safely?* Ask it for the analysis plan and code, run it, and validate on simulated data where you know the truth.
- *What else do LLMs commonly get wrong?* Wrong df, wrong one/two-sided, "normality tests prove normality", ignoring multiple comparisons, and inventing citations.

**Common mistakes:** pasting numbers into a report without re-running, accepting a plausible-sounding interpretation, and not checking the unit of analysis.

### Q52 ⭐ 🔴 What are consistency, efficiency and sufficiency of an estimator? State the Cramer-Rao lower bound.
**Asked at:** Research-leaning teams, Microsoft IDC, senior roles
**Say this first (1 line):** Consistent means the estimate converges to the truth as n grows; efficient means it has the smallest possible variance among unbiased estimators; sufficient means it captures all the information about the parameter in the sample. Cramer-Rao says no unbiased estimator can have variance below 1/(n·I(θ)).

**Then explain:**
- **Consistency:** θ̂ₙ → θ in probability. A basic must-have (the sample mean is consistent for the population mean, by the LLN).
- **Efficiency:** compare variance to the Cramer-Rao lower bound (CRLB). An estimator hitting the bound is efficient; the ratio bound/variance is its efficiency.
- **Sufficiency:** a statistic T(x) is sufficient if the data given T no longer depends on θ. Example: the sample mean for the normal mean; the sum for Poisson.
- **CRLB:** for an unbiased estimator, Var(θ̂) ≥ 1 / (n·I(θ)), where I(θ) = E[(∂ log f/∂θ)²] is the Fisher information per observation. Needs regularity conditions (support not depending on θ, differentiability).
- MLE is asymptotically efficient. Under the bound's conditions, it is the best you can do for large n.

**Example:** X ~ N(μ, σ² = 4), n = 50. Bound = σ²/n = 0.08. Simulation: variance of the sample mean 0.0799 (attains the bound), variance of the sample median 0.1223, an efficiency of 0.65 (theory 2/π = 0.637). The median wastes about a third of the data but resists outliers.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(24)
n, sigma, S = 50, 2.0, 40000
x = rng.normal(5, sigma, (S, n))
bound = sigma**2/n
print('CRLB             %.4f' % bound)
print('var(sample mean) %.4f' % x.mean(1).var())
print('var(sample median) %.4f  efficiency %.3f (theory 2/pi = %.3f)' % (np.median(x, 1).var(), bound/np.median(x, 1).var(), 2/np.pi))
for m in [10, 100, 10000]:                           # consistency: error shrinks with n
    print(m, 'mean abs error %.3f' % np.abs(rng.normal(5, sigma, (500, m)).mean(1)-5).mean())
```
Output: CRLB 0.0800, var(mean) 0.0799, var(median) 0.1223 (efficiency 0.654); mean abs error 0.490, 0.151, 0.016 as n goes 10, 100, 10,000.

**Follow-ups:**
- *Can a biased estimator beat the CRLB?* Yes, in MSE terms (shrinkage, ridge); the bound applies to unbiased estimators (a version exists for biased ones).
- *Does the bound apply to Uniform(0, θ)?* No: the support depends on θ, regularity fails, and the max has variance of order 1/n².

**Common mistakes:** mixing unbiased with consistent, thinking efficiency always beats robustness, and applying the CRLB where the regularity conditions fail.

### Q53 ⭐ 🔴 What is Fisher information, and why is the MLE asymptotically normal? How do you get a standard error from it?
**Asked at:** Research-leaning teams, senior roles
**Say this first (1 line):** Fisher information measures how sharply the log-likelihood peaks around the true parameter: I(θ) = -E[∂² log f/∂θ²]. The MLE is asymptotically normal with variance 1/(n·I(θ)), so SE = 1/√(n·I(θ̂)).

**Then explain:**
- At the MLE, the score (derivative of log-likelihood) is zero. A Taylor expansion shows θ̂ - θ ≈ score / (n·I), and the score is a sum of iid terms, so the CLT makes it normal with variance n·I. Hence √n(θ̂ - θ) → N(0, 1/I(θ)).
- A sharper peak (more curvature) means more information and a smaller SE.
- In practice use **observed information**: minus the second derivative of the log-likelihood at θ̂, computed numerically or from the Hessian. SE = 1/√(observed information). This is what statsmodels GLM and logit summaries report (sklearn does not report SEs).
- For several parameters, the covariance is the inverse of the information (Hessian) matrix.
- Wald CI: θ̂ ± 1.96·SE. Often better on a transformed scale (log for rates).

**Example:** Poisson with λ = 4, n = 200: I = 1/λ, so SE = √(λ/n) = 0.1414, matching the simulated SD of the MLE (0.1414). From one dataset: MLE 3.890, observed-information SE 0.1395, same as √(λ̂/n) = 0.1395.

**Code:**
```python
import numpy as np
from scipy import optimize
rng = np.random.default_rng(25)
lam, n = 4.0, 200
mles = np.array([rng.poisson(lam, n).mean() for _ in range(20000)])   # Poisson MLE = sample mean
print('sd of MLE (simulated) %.4f' % mles.std())
print('1/sqrt(n*I), I=1/lam  %.4f' % np.sqrt(lam/n))
x = rng.poisson(lam, n)
nll = lambda l: -(x*np.log(l) - l).sum()             # negative log-likelihood, constant dropped
l0 = optimize.minimize_scalar(nll, bounds=(.1, 20), method='bounded').x
h = 1e-3; obs_info = (nll(l0+h) - 2*nll(l0) + nll(l0-h))/h**2   # 2nd derivative = observed information
print('MLE %.3f  observed-info SE %.4f  formula sqrt(lam_hat/n) %.4f' % (l0, 1/np.sqrt(obs_info), np.sqrt(l0/n)))
```
Output: 0.1414 (simulated) vs 0.1414 (theory); MLE 3.890, SE 0.1395 both ways.

**Follow-ups:**
- *Expected vs observed information?* Expected is an average over data; observed uses the actual curvature. They agree for large n; observed is easier and often better.
- *When does asymptotic normality fail?* Parameter at the boundary, too few data, non-regular models (uniform max), or many parameters relative to n.

**Common mistakes:** forgetting the n factor, using the wrong sign on the second derivative, and trusting Wald intervals for small n or near-boundary parameters (Wilson/profile likelihood is better).

### Q54 ⭐ 🔴 How does the delta method give a standard error for a ratio metric (e.g., revenue per session)?
**Asked at:** Amazon, Booking, Spotify, senior roles
**Say this first (1 line):** For a ratio of two user-level averages, R = ȳ/x̄, the delta method uses a first-order Taylor expansion to get Var(R) ≈ (1/x̄²)·[Var(y) + R²·Var(x) - 2R·Cov(x, y)] / n. It accounts for numerator and denominator both being random and correlated.

**Then explain:**
- Ratio metrics (revenue per session, CTR as clicks/impressions) have the randomisation unit (user) different from the denominator unit (session or impression). So you cannot treat sessions as independent rows.
- Delta method: for a smooth function g of means, Var(g) ≈ ∇gᵀ Σ ∇g / n. For g = ȳ/x̄: partials are 1/x̄ and -ȳ/x̄².
- The covariance term matters: users with more sessions also spend more, and ignoring it gives the wrong SE.
- Use the SE in a z-test for the difference of ratios between arms. The bootstrap resampling users gives a check without formulas.
- Common alternative: linearization, replacing each user's metric with (yᵢ - R·xᵢ)/x̄ and taking its ordinary mean/SE. Same result.

**Example:** 5,000 users, sessions per user about 4, revenue correlated with sessions. Ratio R = 2.957 revenue per session. Delta SE = 0.0320, bootstrap SE = 0.0314. Ignoring the covariance gives 0.0406, an overstated SE of 27%.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(26)
n = 5000
x = (rng.poisson(3, n)+1).astype(float)           # sessions per user
y = rng.gamma(2, 1.5, n)*x                        # revenue per user, correlated with sessions
R = y.sum()/x.sum()                               # ratio metric: revenue per session
c = np.cov(y, x)
se_delta = np.sqrt((c[0, 0] + R**2*c[1, 1] - 2*R*c[0, 1])/(x.mean()**2*n))
bs = []
for _ in range(2000):
    i = rng.integers(0, n, n); bs.append(y[i].sum()/x[i].sum())    # resample USERS
print('ratio %.4f' % R)
print('delta SE %.5f   bootstrap SE %.5f' % (se_delta, np.std(bs)))
se_wrong = np.sqrt((c[0, 0] + R**2*c[1, 1])/(x.mean()**2*n))
print('SE if covariance ignored %.5f' % se_wrong)
```
Output: ratio 2.9566; delta SE 0.03197; bootstrap SE 0.03144; covariance ignored 0.04064.

**Follow-ups:**
- *Why not just take the average of per-session revenue across all sessions?* Sessions from the same user are correlated, so SE is too small and false positives rise.
- *Is delta method exact?* No: it is a large-n approximation (first-order). Check with the bootstrap if the denominator is small or noisy.

**Common mistakes:** computing the SE as if sessions were independent, dropping the covariance term, and mixing up a ratio of means (total/total) with a mean of ratios (average of per-user ratios), which are different metrics.

### Q55 ⭐ 🔴 What exactly does the Mann-Whitney U test test? Is it a test of medians? What are the pitfalls?
**Asked at:** Senior DS roles, Amazon, Spotify
**Say this first (1 line):** Mann-Whitney U tests whether a random observation from one group tends to be larger than one from the other, i.e. P(A > B) ≠ 0.5. It is a test of stochastic dominance, not of medians, unless the two distributions have the same shape and differ only by a shift.

**Then explain:**
- U counts, over all pairs, how often A beats B. U / (n₁n₂) estimates P(A > B), a useful effect size (the "common language" or probability-of-superiority measure; AUC is the same number).
- Under a pure location shift (same shape), "different P(A > B)" does mean "different medians". Otherwise it does not.
- It can reject when medians are identical (skewed vs symmetric), and fail to reject when medians differ in certain shapes.
- Pitfalls: not a test of means; different spreads can confuse interpretation; heavy ties (lots of zeros) reduce power and need the tie correction; also not transitive across three groups (non-transitive dice).
- To get an effect size with a CI, report P(A > B) or the Hodges-Lehmann shift estimate.

**Example:** A is Normal(0, 1) (median 0); B is very skewed with median forced to 0 (mean 2.4). Medians are about equal, yet Mann-Whitney gives p = 1.4e-22 with P(A > B) = 0.427. Same centre but spread 1 vs 4: p = 0.64, P = 0.503. A pure shift of 0.2 SD: p = 5.6e-11, P = 0.549 (theory 0.556).

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(27)
n = 3000
a = rng.normal(0, 1, n)                                   # symmetric, median 0
b = rng.lognormal(0, 1.5, n); b = b - np.median(b)        # very skewed, median forced to 0
print('medians %.3f %.3f | means %.2f %.2f' % (np.median(a), np.median(b), a.mean(), b.mean()))
u = stats.mannwhitneyu(a, b)
print('Mann-Whitney p = %.2g,  P(a>b) = U/(n1 n2) = %.3f' % (u.pvalue, u.statistic/n**2))
c = rng.normal(0, 1, n); d = rng.normal(0, 4, n)          # same centre, different spread
u = stats.mannwhitneyu(c, d)
print('same centre, spread 1 vs 4: p = %.2f, P(c>d) = %.3f' % (u.pvalue, u.statistic/n**2))
e = rng.normal(0, 1, n); f = rng.normal(.2, 1, n)         # pure shift
u = stats.mannwhitneyu(f, e)
print('shift 0.2: p = %.2g, P(f>e) = %.3f (theory %.3f)' % (u.pvalue, u.statistic/n**2, stats.norm.cdf(.2/np.sqrt(2))))
```
Output: medians 0.034 vs 0.000, means 0.03 vs 2.42; p = 1.4e-22, P = 0.427; p = 0.64, P = 0.503; p = 5.6e-11, P = 0.549 (theory 0.556).

**Follow-ups:**
- *Mann-Whitney vs Wilcoxon rank-sum?* Same test, different formulations.
- *What do you use if you really want to compare medians?* A bootstrap or permutation test on the difference in medians, or quantile regression.

**Common mistakes:** saying "it compares medians", using it to claim mean revenue lift, and ignoring P(A > B) as the effect size.

### Q56 ⭐ 🔴 When does the bootstrap fail? What are percentile vs BCa intervals and what is the bootstrap for dependent (time-series) data?
**Asked at:** Senior DS roles, Google-style
**Say this first (1 line):** The bootstrap resamples your data to mimic repeated sampling. It fails for non-smooth statistics (maximum, minimum), very heavy tails (infinite variance), tiny samples, and dependent data if you resample rows independently. Percentile intervals are simple; BCa corrects for bias and skew; block bootstraps handle time series.

**Then explain:**
- **When it fails:** extreme-value statistics (the resample max equals the sample max about 63% of the time, so it cannot recover the true spread); infinite-variance data; tiny n; statistics on the boundary; and dependent data (iid resampling destroys the autocorrelation, so SE is too small).
- **Percentile CI:** take the 2.5th and 97.5th percentiles of the bootstrap statistics. Simple; can be biased for skewed statistics.
- **BCa (bias-corrected and accelerated):** adjusts the percentiles using a bias constant and an acceleration constant (from jackknife skew). Better coverage, second-order accurate, but costlier and still needs enough data.
- **Dependent data:** moving-block or stationary bootstrap, resampling blocks of consecutive points (block length about n^(1/3), or larger for strong dependence); for clustered data resample whole clusters (users).
- Alternatives: parametric bootstrap, subsampling, or the m-out-of-n bootstrap.

**Example:** (1) Uniform sample n = 100: bootstrap max equals sample max 63.7% of the time (theory 63.4%). (2) CI for the SD of a lognormal, n = 40: coverage about 0.57 for percentile and 0.63 for BCa in the script below (150 runs; a 600-run check gave 0.56 and 0.66, so treat these as roughly 0.55-0.65), against a nominal 0.95. BCa helps, but both fail: SD of heavy-tailed data at n = 40 is hard. (3) AR(1) series (phi = 0.7, n = 500): true SE of the mean 0.149; iid bootstrap 0.063 (too small); block bootstrap 0.129.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(30)
x = rng.uniform(0, 1, 100)                                           # 1) bootstrap of the maximum
bmax = np.array([rng.choice(x, 100).max() for _ in range(5000)])
print('P(bootstrap max == sample max) = %.3f (theory %.3f)' % ((bmax == x.max()).mean(), 1-(1-1/100)**100))
true = np.sqrt((np.exp(1)-1)*np.exp(1)); cov = {'percentile': 0, 'BCa': 0}; R = 150   # 2) percentile vs BCa
for _ in range(R):
    s = rng.lognormal(0, 1, 40)
    for m in cov:
        ci = stats.bootstrap((s,), np.std, n_resamples=999, method=m, random_state=rng).confidence_interval
        cov[m] += bool(ci.low <= true <= ci.high)
print('coverage:', {k: round(v/R, 2) for k, v in cov.items()})
n, phi = 500, .7                                                     # 3) dependent data
e = rng.normal(size=n); y = np.zeros(n)
for t in range(1, n): y[t] = phi*y[t-1] + e[t]
true_se = 1/((1-phi)*np.sqrt(n))
iid = np.std([rng.choice(y, n).mean() for _ in range(2000)])
L = 25; nb = n//L
blk = np.std([np.concatenate([y[s:s+L] for s in rng.integers(0, n-L, nb)]).mean() for _ in range(2000)])
print('true SE %.3f | iid bootstrap %.3f | block bootstrap %.3f' % (true_se, iid, blk))
```
Output: 0.637 (theory 0.634); coverage percentile 0.57, BCa 0.63; true SE 0.149, iid 0.063, block 0.129.

**Follow-ups:**
- *How many bootstrap resamples?* About 1,000 for SEs, 5,000 to 10,000 for percentile CI tails.
- *Is the bootstrap better than a t-interval for the mean?* Not necessarily for small n; it is most useful for odd statistics (medians, ratios, AUC).

**Common mistakes:** bootstrapping rows of clustered or time-series data, bootstrapping the max/min, and expecting the bootstrap to fix a sample that is too small or unrepresentative.

### Q57 ⭐ 🔴 Count data is overdispersed relative to Poisson. How do you detect it and what do you do (negative binomial, quasi-Poisson)?
**Asked at:** Swiggy, Zalando, Booking, senior roles
**Say this first (1 line):** Check the dispersion: Pearson chi-squared / residual df should be near 1 for Poisson; if it is well above 1 the data are overdispersed and Poisson standard errors are too small. Fix with quasi-Poisson (inflate SEs) or negative binomial (model the extra variance).

**Then explain:**
- **Poisson** forces variance = mean. Real counts (orders per user, tickets per day) usually have variance > mean, because of unobserved heterogeneity or clustering.
- **Detect:** variance vs mean, dispersion statistic, a formal test (e.g. Cameron-Trivedi), or compare AIC with a negative binomial.
- **Quasi-Poisson:** same coefficients, SEs multiplied by √dispersion. Simple and robust, but not a full likelihood (no AIC).
- **Negative binomial:** adds a dispersion parameter, Var = μ + μ²/r. A proper likelihood, so AIC and prediction intervals work.
- If you see too many zeros, think zero-inflated or hurdle models. Sandwich (robust) SEs are another safeguard.

**Example:** Simulated counts, mean 2.82, variance 7.55; Pearson dispersion 2.32. Slope SE: Poisson 0.0132 (too small), quasi-Poisson 0.0202, negative binomial 0.0207. AIC: Poisson 9,396 vs NB 8,504. Poisson would report a significance that is overstated by about 1.5x on the z-score.

**Code:**
```python
import numpy as np
import statsmodels.api as sm
rng = np.random.default_rng(32)
n = 2000; x = rng.normal(size=n); mu = np.exp(1 + .3*x)
y = rng.negative_binomial(2, 2/(2+mu))                    # NB with r=2 -> var = mu + mu^2/2
X = sm.add_constant(x)
pois = sm.GLM(y, X, family=sm.families.Poisson()).fit()
print('mean %.2f var %.2f' % (y.mean(), y.var()))
print('dispersion (Pearson chi2/df) = %.2f  (Poisson expects 1)' % (pois.pearson_chi2/pois.df_resid))
quasi = sm.GLM(y, X, family=sm.families.Poisson()).fit(scale='X2')
nb = sm.NegativeBinomial(y, X).fit(disp=0)
print('slope  Poisson %.3f SE %.4f | quasi SE %.4f | NB %.3f SE %.4f (true 0.3)' % (
      pois.params[1], pois.bse[1], quasi.bse[1], nb.params[1], nb.bse[1]))
print('AIC Poisson %.0f  NB %.0f' % (pois.aic, nb.aic))
```
Output: as in the example (dispersion 2.32; SEs 0.0132, 0.0202, 0.0207).

**Follow-ups:**
- *Does overdispersion bias the coefficients?* Not if the mean model is right (Poisson MLE is still consistent), but SEs and p-values are wrong.
- *Underdispersion?* Rare; consider Conway-Maxwell-Poisson or check for structure.

**Common mistakes:** trusting default Poisson p-values, ignoring zero inflation, and comparing quasi-Poisson models by AIC.

### Q58 ⭐ 🔴 How does FDR control behave under dependent tests? Explain q-values and Benjamini-Yekutieli.
**Asked at:** Senior roles, Europe product cos
**Say this first (1 line):** Benjamini-Hochberg controls the false discovery rate for independent or positively dependent (PRDS) tests, and it is usually fine in practice. For arbitrary dependence, Benjamini-Yekutieli divides α by the harmonic sum Σ1/i and is valid but much more conservative. A q-value is the smallest FDR at which a test would be called significant.

**Then explain:**
- **FDR** = expected value of (false discoveries / all discoveries). It holds *on average*; in any one dataset the false-discovery proportion can be far from 5%, especially when tests are correlated.
- **BH under dependence:** proven for positive regression dependence (PRDS), e.g. equicorrelated normal test statistics with one-sided p-values; two-sided p-values with positive correlation behave well in simulation (as below) but are not strictly covered by the proof. It can be off under strong negative or arbitrary dependence.
- **BY:** use threshold (i/m)·α / c(m), with c(m) = Σᵢ 1/i (about ln m + 0.58). For m = 500 this is a factor of about 6.8 stricter, hence the power loss.
- **q-value (Storey):** estimates the null proportion π₀ from the p-values above λ (e.g. 0.5), then q = π₀·m·p/rank, with monotone smoothing. Gains power over BH when π₀ < 1.

**Example:** 500 tests, 50 real (z mean 3), equicorrelation 0.8. Over 300 runs: BH mean false-discovery proportion 0.024 and power 0.49, but the proportion varies hugely (SD 0.128, up to 0.90 in one run, since correlated tests tend to be right or wrong together). BY: FDP 0.004, power 0.30, safer but loses power. Storey q-value on 1,000 tests (100 real): π₀ estimate 0.91 (true 0.90); 53 tests with q < 0.05, 48 real.

**Code:**
```python
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
rng = np.random.default_rng(33)
m, m1, rho, S = 500, 50, .8, 300
fdp = {'bh': [], 'by': []}; pw = {'bh': [], 'by': []}
for _ in range(S):
    f = rng.normal(); z = np.sqrt(rho)*f + np.sqrt(1-rho)*rng.normal(size=m)   # equicorrelated tests
    z[:m1] += 3
    p = 2*stats.norm.sf(np.abs(z))
    for k, meth in [('bh', 'fdr_bh'), ('by', 'fdr_by')]:
        rej = multipletests(p, alpha=.05, method=meth)[0]
        fdp[k].append(rej[m1:].sum()/max(rej.sum(), 1)); pw[k].append(rej[:m1].mean())
for k in fdp: print(k, 'mean FDP %.3f  sd FDP %.3f  max FDP %.2f  power %.3f' % (np.mean(fdp[k]), np.std(fdp[k]), np.max(fdp[k]), np.mean(pw[k])))
def qvalues(p, lam=.5):                                                          # Storey q-values
    pi0 = min(1, (p > lam).mean()/(1-lam)); o = np.argsort(p); ps = p[o]; m = len(p)
    q = pi0*m*ps/np.arange(1, m+1); q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(m); out[o] = np.minimum(q, 1); return out, pi0
z = np.r_[rng.normal(3, 1, 100), rng.normal(0, 1, 900)]; p = 2*stats.norm.sf(np.abs(z))
q, pi0 = qvalues(p)
print('pi0 est %.2f (true 0.90); q<0.05: %d tests, true hits %d' % (pi0, (q < .05).sum(), (q[:100] < .05).sum()))
```
Output: bh FDP 0.024, SD 0.128, max 0.90, power 0.491; by FDP 0.004, SD 0.043, max 0.60, power 0.303; pi0 0.91, 53 tests with q < 0.05, 48 true.

**Follow-ups:**
- *When to use BY vs BH?* BY when dependence is unknown or negative and a guarantee is needed; BH when tests are positively related (most genomic or metric-family settings).
- *q-value vs adjusted p-value?* BH-adjusted p is basically a q-value with π₀ = 1.

**Common mistakes:** saying "FDR 5% means each discovery has 5% chance to be false" or "at most 5% of discoveries are false in this experiment", and using BY by default without realising the power cost.

### Q59 ⭐ 🔴 What is an equivalence / non-inferiority test (TOST)? When would you use it instead of a standard test?
**Asked at:** Spotify, Booking, Klarna, senior roles
**Say this first (1 line):** TOST (two one-sided tests) tests whether a difference is smaller than a pre-set margin, so you can actually show "no meaningful difference". A normal test cannot prove equality: a non-significant p only means "not enough evidence of a difference".

**Then explain:**
- Pick an equivalence margin ±δ in advance: the largest difference you would consider unimportant. This is a business or clinical decision, and the hard part.
- Two one-sided tests: H0a: diff ≤ -δ and H0b: diff ≥ +δ. Reject both, then declare equivalence. TOST p-value = the larger of the two.
- Equivalent to checking whether the 90% CI (not 95%) lies completely inside (-δ, +δ), when α = 0.05.
- **Non-inferiority** is the one-sided version: show the new thing is not worse than the old by more than δ. Typical uses: a cheaper model or a simplified checkout "not worse" than the old, migration or infra change that should not move metrics, generic vs brand.
- Needs enough sample size: wide CIs cannot fit inside the margin.

**Example:** New vs old model score: observed difference 0.069, margin ±0.3, n = 1,500 per arm. Ordinary t-test p = 0.342 (says nothing about equality). TOST p = 0.0007, 90% CI (-0.050, 0.187) is inside ±0.3, so equivalent. With only n = 100 per arm: t-test p = 0.772 (looks "same") but TOST p = 0.221 and CI (-0.38, 0.55) exceeds the margin, so equivalence is not shown.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(34)
def tost(a, b, delta):
    d = a.mean()-b.mean(); va, vb = a.var(ddof=1)/len(a), b.var(ddof=1)/len(b); se = np.sqrt(va+vb)
    df = se**4/(va**2/(len(a)-1) + vb**2/(len(b)-1))
    p_low = stats.t.sf((d+delta)/se, df)           # H0: diff <= -delta
    p_up = stats.t.cdf((d-delta)/se, df)           # H0: diff >= +delta
    tc = stats.t.ppf(.95, df)
    return d, max(p_low, p_up), (d-tc*se, d+tc*se)
a = rng.normal(10.02, 2, 1500); b = rng.normal(10.0, 2, 1500)
d, p, ci90 = tost(a, b, delta=0.3)
print('diff %.3f, TOST p = %.4f, 90%% CI = (%.3f, %.3f), margin +-0.3' % (d, p, *ci90))
print('ordinary t-test p = %.3f' % stats.ttest_ind(a, b).pvalue)
a2 = rng.normal(10.02, 2, 100); b2 = rng.normal(10.0, 2, 100)
d2, p2, ci2 = tost(a2, b2, delta=0.3)
print('n=100: t-test p = %.3f, TOST p = %.3f, 90%% CI = (%.2f, %.2f)' % (stats.ttest_ind(a2, b2).pvalue, p2, *ci2))
```
Output: as in the example.

**Follow-ups:**
- *Why a 90% CI for a 5% test?* Because each one-sided test uses a 5% tail; together they equal a 90% two-sided interval.
- *How to choose δ?* From business impact, historical noise, or a clinical or product threshold, fixed before seeing data.

**Common mistakes:** concluding "no difference" from p > 0.05, choosing the margin after seeing results, and running the test with too small a sample to ever show equivalence.

### Q60 ⭐ 🔴 Cauchy distribution: why do the LLN and CLT fail, and what does it teach about heavy tails?
**Asked at:** Quant-leaning and senior roles
**Say this first (1 line):** The Cauchy distribution has such heavy tails that its mean and variance do not exist, so the law of large numbers and the central limit theorem do not apply: the average of n Cauchy draws is itself exactly Cauchy, with no shrinkage.

**Then explain:**
- Density ∝ 1/(1 + x²): the tails decay like 1/x², too slowly for E[|X|] to be finite. The mean is undefined, and so is a finite variance (the sample variance never settles).
- The mean of n iid standard Cauchy variables is again standard Cauchy. Averaging never helps. The running mean keeps jumping whenever a huge draw appears.
- CLT needs a finite variance. LLN needs a finite mean. Neither holds.
- The median and the interquartile range are well defined, so use robust estimators (median, trimmed mean, MLE of location and scale) instead of the mean.
- Real data can behave like this: financial returns, whale spend, latency spikes, network traffic. Heavy-tailed data (not exactly Cauchy) slow down the CLT and make mean-based inference unreliable.

**Example:** 200,000 draws: running mean of the Cauchy is -4.4 at 100 draws, 0.92 at 10,000, -3.86 at 200,000 (not converging), while the normal's running mean goes to 0.002. The IQR of the sample mean is 1.95 for one draw, 2.07 for 100, 2.07 for 10,000, constant, while a normal mean would shrink to 0.01. Sample variance: 4.5e5 on the first 1,000 draws vs 2.4e6 on all 200,000 (it keeps growing).

**Code:**
```python
import numpy as np
rng = np.random.default_rng(35)
n = 200000
c = rng.standard_cauchy(n); g = rng.normal(size=n)
for k in [100, 10000, 200000]:
    print(k, 'running mean: Cauchy %7.3f  Normal %7.3f' % (c[:k].mean(), g[:k].mean()))
for m in [1, 100, 10000]:
    means = rng.standard_cauchy((2000, m)).mean(1)
    print(m, 'IQR of the sample mean: %.2f (Normal would be %.2f)' % (np.subtract(*np.percentile(means, [75, 25])), 1.349/np.sqrt(m)))
print('sample variance, first 1k vs all 200k draws: %.1f vs %.1f' % (c[:1000].var(), c.var()))
print('median is stable: %.3f' % np.median(c))
```
Output: as in the example; median -0.005.

**Follow-ups:**
- *Practical lesson?* Plot the data and its tails before choosing a mean-based method; consider medians, trimmed means, quantiles, or modelling the tail (Pareto, t with low df).
- *Is the t-distribution with 1 df the Cauchy?* Yes. That is also why a t-test with tiny df has such wide intervals.

**Common mistakes:** computing a mean and SE of a heavy-tailed metric and trusting it, thinking "large n always fixes it", and treating the sample variance as a stable estimate when it is dominated by a few points.

### Q61 ⭐ 🔴 What is the design effect for clustered or correlated observations, and how does it change standard errors and sample size?
**Asked at:** Senior roles, Booking, Zalando, Swiggy
**Say this first (1 line):** The design effect is deff = 1 + (m - 1)·ICC, where m is the cluster size and ICC the intraclass correlation. It is the factor by which the variance is inflated compared with independent observations, so SEs grow by √deff and the sample size needs to grow by deff.

**Then explain:**
- Observations in the same cluster (users in a city, students in a class, sessions of one user) are more alike than random ones. ICC = between-cluster variance / total variance.
- Effective sample size = n / deff. Fifty clusters of 20 users with ICC 0.10 behave like only about 345 independent users, not 1,000.
- Ignoring clustering gives SEs that are too small, p-values too small, and false positives well above 5%.
- Fixes: compute SEs at the cluster level, use cluster-robust (sandwich) SEs, mixed-effects models, or the delta method for ratio metrics (Q54). Plan the sample size by multiplying the independent-sample number by deff.
- Adding more units per cluster gives diminishing returns; adding clusters is what helps (variance floor is set by the number of clusters).
- Same idea with unequal weights in surveys (Kish's deff due to weighting).

**Example:** 50 clusters x 20 users, between SD 1, within SD 3, so ICC = 0.10 and deff = 2.90. The naive SE is 0.0999 but the true SD of the mean is 0.1700. Multiplying the naive SE by √2.90 gives 0.1701. To match the precision of 1,000 independent users you need 2,901 users.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(36)
K, m, S = 50, 20, 3000                       # 50 clusters x 20 users
sb, sw = 1.0, 3.0                            # between- and within-cluster SD
icc = sb**2/(sb**2+sw**2); deff = 1+(m-1)*icc
means, naive = [], []
for _ in range(S):
    y = rng.normal(0, sb, (K, 1)) + rng.normal(0, sw, (K, m))
    means.append(y.mean()); naive.append(y.std(ddof=1)/np.sqrt(K*m))
print('ICC %.2f  design effect %.2f' % (icc, deff))
print('true SD of the mean %.4f | naive SE %.4f | naive SE x sqrt(deff) %.4f' % (np.std(means), np.mean(naive), np.mean(naive)*np.sqrt(deff)))
print('effective sample size: %d users -> %.0f' % (K*m, K*m/deff))
print('n needed for same precision as 1000 independent users: %d' % np.ceil(1000*deff))
```
Output: ICC 0.10, deff 2.90; true SD 0.1700, naive SE 0.0999, corrected 0.1701; effective n 345; needed n 2,901.

**Follow-ups:**
- *How does this affect A/B tests?* If randomisation is by cluster (city, store, user) the analysis unit must be the cluster, or you must correct with deff or cluster-robust SEs.
- *How do you estimate ICC?* From a one-way ANOVA or a mixed model's variance components, or from pilot data.

**Common mistakes:** randomising by user but analysing sessions as independent, treating a bigger cluster size as free sample size, and forgetting the design effect when planning sample size.


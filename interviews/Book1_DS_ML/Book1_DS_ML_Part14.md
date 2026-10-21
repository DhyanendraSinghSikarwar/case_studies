# Book 1 — Part 14: Statistics Deep Dive II

**Topic:** Probability puzzles, conditional probability & Bayes, Markov chains, random walks, order statistics, regression diagnostics, Bayesian statistics, sequential testing, CUPED / variance reduction, Monte Carlo simulation
**Target:** >=50 questions  |  **Actual:** 62 (⭐⭐⭐ 19, ⭐⭐ 26, ⭐ 17)  |  **Date:** 2026-10-20
**Scope note:** Distributions, sampling, estimators, CLT, CIs, classical tests and power belong to Part 13; A/B and causal design belong to Part 10.

---

> Dedupe pass: removed 1 cross-part duplicate(s); renumbered Q1–Q62.

---

### Q1 ⭐⭐⭐ 🟢 You toss a fair coin twice: what is the probability of two heads in a row, and what is the expected number of tosses until the first head?
**Asked at:** Typical (prep sources): Swiggy DS (Prepfully); Indian product cos, GCCs; screening rounds
**Say this first (1 line):** P(two heads) = 1/4, and the expected number of tosses until the first head is 2.

**Then explain:**
- Tosses are independent, so P(HH) = 1/2 × 1/2 = 1/4.
- "Tosses until first head" is a geometric random variable with p = 1/2, so E = 1/p = 2.
- Quick derivation (first-step analysis): E = 1 + (1/2)·0 + (1/2)·E. You always toss once; with prob 1/2 you are done, with prob 1/2 you are back where you started. Solve: E = 2.

**Example:** A payment succeeds 20% of the time on each retry. Expected attempts until first success = 1/0.2 = 5.

**Follow-ups:**
- *Variance?* (1 − p)/p² = 2 for a fair coin.
- *Biased coin?* E = 1/p; P(two heads) = p².

**Common mistakes:** Answering 1 or 3 for the expectation; confusing "number of tosses until first head" (mean 2) with "number of tails before first head" (mean 1).

### Q2 ⭐⭐⭐ 🟢 Birthday problem: how many people until there is a >50% chance two share a birthday? Derive it and extend to hash collisions.
**Asked at:** Typical (prep sources): Quant firms, Amazon, Indian product cos; stats screening rounds
**Say this first (1 line):** 23 people give just over a 50% chance (50.7%) of a shared birthday, and in general you need about 1.18·√N draws from N possibilities.

**Then explain:**
- Easier to count "no match": P(no match) = (365/365)(364/365)…((365−n+1)/365).
- Use 1 − x ≈ e^(−x): P(no match) ≈ exp(−n(n−1)/(2·365)). Set it to 1/2, so n² ≈ 2·365·ln 2, and n ≈ 1.1774·√365 ≈ 22.5, so n = 23.
- Why so small? There are n(n−1)/2 pairs, about 253 pairs for n = 23, and each has a 1/365 chance. Pairs grow quadratically, not linearly.
- Hash collisions: with a d-bit hash (N = 2^d values) a collision is likely after about 1.18·2^(d/2) items. This is the "birthday bound": halve the bits.

**Example:** 32-bit hash: ~77,000 items already give a 50% collision chance. 64-bit: ~5×10⁹. 128-bit: ~2×10¹⁹, so collisions are not a practical concern.

**Code:**
```python
import numpy as np
n = 1
while 1 - np.prod(1 - np.arange(n) / 365) < 0.5: n += 1
print(n, 1 - np.prod(1 - np.arange(n) / 365))
for bits in (32, 64, 128): print(bits, 1.1774 * 2 ** (bits / 2))
# 23 0.5072972343239854
# 32 77162.0864
# 64 5056894494.3104
# 128 2.1719196472385626e+19
```

**Follow-ups:**
- *Chance at 57 people?* About 99%.
- *Where does it matter in DS?* Hash-based IDs, bucketing and feature hashing (collisions in hashed feature space), UUID/ID-generation, A/B bucket collisions.

**Common mistakes:** Answering 183 (365/2); computing the chance that someone shares *your* birthday (that needs ~253 people); forgetting the pairs argument.

### Q3 ⭐⭐⭐ 🟢 A disease affects 1% of people and a test is 99% sensitive and 95% specific. You test positive: what is the probability you have the disease? Why is the answer so low?
**Asked at:** Typical (prep sources): Most DS loops (Amazon, Flipkart, Microsoft IDC, Booking, Spotify)
**Say this first (1 line):** About 17% (1 in 6), because the disease is rare, so false positives from the many healthy people swamp the true positives.

**Then explain:**
- Bayes: P(D|+) = P(+|D)P(D) / [P(+|D)P(D) + P(+|¬D)P(¬D)] = 0.99·0.01 / (0.99·0.01 + 0.05·0.99) = 0.0099/0.0594 ≈ 0.167.
- Specificity 95% means a 5% false-positive rate (1 − 0.95), not 1%.
- Think in counts per 10,000 people: 100 sick, of whom 99 test positive; 9,900 healthy, of whom 495 test positive. So 99 of 594 positives are truly sick = 16.7%.
- The prior (base rate) matters as much as the test accuracy. Intuition fails because we only look at sensitivity.

**Example:** Same logic for fraud detection: if 0.1% of transactions are fraud, even a 99%-accurate model flags mostly legitimate ones. This is why precision, not accuracy, is the metric on imbalanced data.

**Follow-ups:**
- *How to raise it?* Higher specificity, or test only high-risk people (higher prior), or repeat the test (see Q19).
- *What if prevalence were 20%?* P = 0.99·0.2/(0.99·0.2 + 0.05·0.8) = 83%.

**Common mistakes:** Reporting 99% (confusing P(+|D) with P(D|+)); using 1 − 0.95 on the wrong population; ignoring the base rate.

### Q4 ⭐⭐⭐ 🟢 Monty Hall: should you switch doors? Prove it, then simulate it in Python.
**Asked at:** Typical (prep sources): Quant firms, product cos; listed classic in Analytics Vidhya / DataInterview
**Say this first (1 line):** Yes, always switch: switching wins 2/3 of the time, staying wins 1/3.

**Then explain:**
- Your first pick is the car with prob 1/3. Monty then opens a goat door, which does not change that 1/3.
- So the remaining closed door holds the car with prob 2/3 (all the probability your pick did *not* have).
- Case view: if you picked the car (1/3), switching loses. If you picked a goat (2/3), Monty must reveal the other goat, so switching wins. Switching wins iff your first pick was wrong = 2/3.
- Key assumption: Monty knows where the car is and always opens a goat door. If he opened randomly and happened to reveal a goat, switching and staying would be 50/50.

**Example:** With 100 doors, you pick one, Monty opens 98 goats: the other door has a 99% chance. Makes the intuition obvious.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0); N = 100_000
car, pick = rng.integers(0, 3, N), rng.integers(0, 3, N)
print("stay", (pick == car).mean(), "switch", (pick != car).mean())  # switching wins iff first pick was wrong
# stay 0.33168 switch 0.66832
```

**Follow-ups:**
- *Why is "50/50" wrong?* Monty's action is informed by the car's location, so the two remaining doors are not symmetric.
- *Bayes proof?* P(car behind 3 | you pick 1, Monty opens 2) = (1·1/3)/(1/2·1/3 + 1·1/3 + 0) = 2/3.

**Common mistakes:** Saying 50/50; ignoring that the host's choice is constrained.

### Q5 ⭐⭐⭐ 🟡 Expected number of rolls of a fair die until you see every face at least once (coupon collector), and how does it scale with n?
**Asked at:** Typical (prep sources): Quant puzzles, Optiver/Jane Street style, product cos (DataInterview)
**Say this first (1 line):** For a 6-sided die it is 14.7 rolls; in general n·H_n ≈ n·ln n + 0.577n, which is O(n log n).

**Then explain:**
- Split into stages. With k faces already seen, the chance a roll is new is (n−k)/n, so the wait is geometric with mean n/(n−k).
- Add the stages: E = n/n + n/(n−1) + … + n/1 = n(1 + 1/2 + … + 1/n) = n·H_n.
- For n = 6: 6(1 + 1/2 + 1/3 + 1/4 + 1/5 + 1/6) = 14.7. The last face alone costs 6 rolls on average.
- Scaling: H_n ≈ ln n + 0.5772 (Euler-Mascheroni constant), so E ≈ n ln n + 0.577n. n = 100 gives 518.7, n = 1000 gives 7485.

**Example:** How many random samples until you have seen all 1,000 distinct classes? About 7,500, i.e. 7.5× the number of classes. Relevant for coverage in sampling, random testing, and "collect all tokens" problems.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
def rolls_until_all(n):
    seen, t = set(), 0
    while len(seen) < n: seen.add(rng.integers(n)); t += 1
    return t
print(np.mean([rolls_until_all(6) for _ in range(20000)]), 6 * sum(1 / k for k in range(1, 7)))
# 14.70125 14.700000000000001
```

**Follow-ups:**
- *Variance?* Dominated by the last stages; sd is about n·π/√6.
- *Tail?* The chance you still miss a face after n(ln n + c) rolls is about 1 − exp(−e^(−c)).

**Common mistakes:** Answering 6 or 6·ln 6; forgetting that the stages have different success probabilities.

### Q6 ⭐⭐⭐ 🟡 Design a spam filter from first principles using Bayes theorem: P(spam | word) given word frequencies. What assumption makes Naive Bayes work and when does it break?
**Asked at:** Likely (expert gap-check): Flipkart, Amazon, Walmart GCC, JPMC
**Say this first (1 line):** Apply Bayes to the words, assume words are independent given the class, and multiply per-word likelihoods; that independence assumption is what makes it "naive" and tractable.

**Then explain:**
- Bayes: P(spam | words) ∝ P(spam) · ∏ P(word_i | spam). Compare it with the same quantity for ham and normalise.
- Training is just counting: P(word | spam) = (count of word in spam + 1)/(total spam words + V). The +1 is Laplace smoothing so an unseen word does not zero the product.
- Use log-probabilities in code to avoid underflow when multiplying hundreds of small numbers.
- Why it works: without independence you would need a joint distribution over 2^V word combinations. With it you only need V numbers per class. Even when it is wrong, the ranking of classes is often right.
- When it breaks: correlated features (e.g. "New" and "York" counted twice, so probabilities become over-confident and badly calibrated), features that interact, and tiny/imbalanced data. It is a good baseline, but do not trust its probabilities.

**Example:** Message "free prize meeting": "free" and "prize" push to spam, "meeting" pushes to ham; the product decides.

**Code:**
```python
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
docs = ["win free prize now", "free money win", "meeting at noon", "lunch meeting tomorrow", "free lunch offer now", "project update meeting"]
y = np.array([1, 1, 0, 0, 1, 0])                  # 1 = spam
cv = CountVectorizer(); X = cv.fit_transform(docs)
nb = MultinomialNB(alpha=1).fit(X, y)             # alpha=1 -> Laplace smoothing
print("P(ham), P(spam):", nb.predict_proba(cv.transform(["free prize meeting"]))[0].round(3))
# P(ham), P(spam): [0.394 0.606]
```

**Follow-ups:**
- *Why is it still competitive?* Low variance, so it works with little data; the decision (argmax) is robust even if probabilities are not.
- *Fix the calibration?* Calibrate (Platt/isotonic) or move to logistic regression, which handles correlated features.

**Common mistakes:** Forgetting smoothing; multiplying raw probabilities (underflow); claiming the features must truly be independent; trusting the predicted probabilities.

### Q7 ⭐⭐⭐ 🟡 Expected number of fair-coin tosses until you see HH vs HT: why are they different?
**Asked at:** Typical (prep sources): Quant firms, Jane Street style, product cos
**Say this first (1 line):** HH takes 6 tosses on average and HT only 4, because after a miss HT can reuse the toss but HH cannot.

**Then explain:**
- Use states. For HT: start (a), have an H (b). a = 1 + ½b + ½a; b = 1 + ½·0 + ½b. So b = 2, a = 2 + b = 4.
- For HH: after an H, a T sends you back to the start: b = 1 + ½·0 + ½a, a = 2 + b. Solve: b = 4, a = 6.
- Intuition: in HT, after an H, a failed attempt (another H) still leaves you in "have an H". In HH, a failed attempt (T) resets you to zero. HH overlaps with itself, so its occurrences are clumpy and the first one comes later.
- Both patterns appear at the same long-run rate (1 in 4 positions), but the *waiting time* differs. A pattern with self-overlap has a longer wait.

**Example:** Equivalent to why runs of identical results "feel" rarer: HH takes longer to show up than HT in a coin sequence.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
def wait(pattern):
    s = []
    while s[-2:] != pattern: s.append(int(rng.integers(2)))
    return len(s)
print("HH", np.mean([wait([1, 1]) for _ in range(20000)]), "HT", np.mean([wait([1, 0]) for _ in range(20000)]))
# HH 6.00405 HT 3.9885
```

**Follow-ups:**
- *Which appears first, HH or HT?* 50-50 by symmetry: after the first H, next toss decides.
- *What about HHH?* 14 (see Q45).

**Common mistakes:** Saying both are 4 because "each has probability 1/4"; not setting up the state equations.

### Q8 ⭐⭐⭐ 🟡 Boy-or-girl puzzle: a family has two children and at least one is a boy: probability both are boys? What if you know the older one is a boy?
**Asked at:** Typical (prep sources): Conditional-probability classic at product cos and trading firms
**Say this first (1 line):** 1/3 if you only know "at least one is a boy", and 1/2 if you know the older one is a boy.

**Then explain:**
- Equally likely families: BB, BG, GB, GG.
- "At least one boy" removes GG, leaving BB, BG, GB. Only BB has two boys: 1/3.
- "Older is a boy" leaves BB and BG: 1/2.
- The difference is *how* you learned the information. "At least one" is a statement about the set; "the older one" picks a specific child, which makes the other child independent.

**Example:** You meet a parent with a boy walking beside them (picked a specific child): the other child is 50% boy. You are told "at least one is a boy" by a survey: 1/3.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
k = rng.integers(0, 2, (1_000_000, 2))            # 1 = boy
print((k[k.sum(1) >= 1].sum(1) == 2).mean(), (k[k[:, 0] == 1][:, 1] == 1).mean())
# 0.3332280265373126 0.499601292651194
```

**Follow-ups:**
- *"At least one boy born on a Tuesday"?* 13/27 ≈ 0.48: more specific information moves it toward 1/2.

**Common mistakes:** Answering 1/2 for the first case; treating BG and GB as the same outcome.

### Q9 ⭐⭐⭐ 🟡 You have a biased coin with unknown bias p: how do you simulate a fair coin? Extend it to generate 7 equally likely outcomes from a biased binary source.
**Asked at:** Typical (prep sources): Swiggy DS (Prepfully), quant firms
**Say this first (1 line):** Use von Neumann's trick: toss twice, HT means 1, TH means 0, and discard HH/TT and repeat; this gives a perfectly fair bit for any unknown p.

**Then explain:**
- P(HT) = p(1−p) = P(TH), so conditional on getting a mixed pair, each is equally likely. The unknown p cancels.
- Cost: each pair succeeds with prob 2p(1−p), so on average you need 1/(p(1−p)) tosses per fair bit (6.25 tosses for p = 0.8).
- For 7 equally likely outcomes: generate 3 fair bits (values 0-7); if you get 7, reject and redo. That is rejection sampling and every kept value has prob 1/7. Expected 8/7 rounds.
- Do not use "mod 7" on 3 bits (0 and 7 both map to 0), which biases the result.

**Example:** Pick a uniformly random one of 7 engineers for an on-call rota using only a flaky bit source.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(1)
def fair_bit(p):                      # von Neumann: toss twice, HT -> 1, TH -> 0, else retry
    while True:
        a, b = rng.random() < p, rng.random() < p
        if a != b: return int(a)
def uniform7(p):                      # 3 fair bits -> 0..7, reject 7
    while True:
        v = 4 * fair_bit(p) + 2 * fair_bit(p) + fair_bit(p)
        if v < 7: return v
print(np.round(np.bincount([uniform7(0.8) for _ in range(14000)]) / 14000, 3))
# [0.136 0.141 0.148 0.143 0.14  0.147 0.144]   (each ~1/7 = 0.143)
```

**Follow-ups:**
- *Can you be more efficient?* Yes, Elias/Peres extraction reuses the discarded pairs and gets closer to the entropy limit H(p) bits per toss.
- *Why rejection for 7 outcomes?* Fair bits only give 2^k equally likely values, and 7 does not divide any power of 2, so some values must be thrown away.

**Common mistakes:** Trying to estimate p first; using modulo; not noticing that HH/TT pairs must be discarded, not counted.

### Q10 ⭐⭐⭐ 🟡 List the assumptions of OLS. Which are needed for unbiased coefficients and which only for valid standard errors / confidence intervals?
**Asked at:** Typical (prep sources): Snapchat DS (PracHub), Amazon, Microsoft IDC, Indian product cos
**Say this first (1 line):** Unbiased coefficients need correct linear specification, exogeneity (E[ε|X] = 0) and no perfect multicollinearity; valid standard errors additionally need constant variance and uncorrelated errors, and exact small-sample t/F tests need normal errors.

**Then explain:**

| Assumption | Needed for | What breaks if violated |
|---|---|---|
| Linear in parameters, correctly specified | Unbiased β | Omitted/wrong-form terms bias β |
| Exogeneity: E[ε \| X] = 0 (no omitted confounder, no reverse causality) | Unbiased, consistent β | Bias that more data does not fix |
| No perfect multicollinearity (X full rank) | β identifiable | Cannot be computed; near-collinearity just inflates SEs |
| Random sample / independent observations | SE validity | Clustered or autocorrelated errors give wrong SEs |
| Homoscedasticity: Var(ε\|X) constant | Correct classic SEs, BLUE (Gauss-Markov) | β still unbiased, SE wrong, not efficient |
| No autocorrelation | Correct SEs, efficiency | Same as above |
| Normal errors | Exact t/F in small samples | Little harm in large n (CLT) |

- Gauss-Markov: with the first six rows (everything except normality), OLS is BLUE (best linear unbiased estimator). Normality is not required for that.
- Fixes: robust (HC) or clustered SEs for variance problems; instruments/controls for endogeneity.

**Example:** Regressing sales on ad spend when ad spend is higher in good seasons: exogeneity fails, β is biased up even with a million rows, and no SE correction helps.

**Follow-ups:**
- *Does the predictor need to be normal?* No. Only the errors matter, and only for small-sample inference.
- *Is R² an assumption check?* No.

**Common mistakes:** Saying "the data must be normally distributed"; listing normality as needed for unbiasedness; forgetting exogeneity, the one that actually causes bias.

### Q11 ⭐⭐⭐ 🟡 What is heteroscedasticity? How do you detect it (residual plots, Breusch-Pagan, White) and fix it (robust SEs, log transform, WLS)?
**Asked at:** Typical (prep sources): Amazon India, banks/GCCs, Flipkart
**Say this first (1 line):** Heteroscedasticity means the error variance changes with X (e.g. a funnel in the residual plot); it leaves OLS coefficients unbiased but makes the standard errors wrong, so detect it with plots/Breusch-Pagan/White and fix with robust SEs, WLS or a transform.

**Then explain:**
- Detect: plot residuals vs fitted (a fan/funnel shape); Breusch-Pagan (regress squared residuals on X, tests for a linear link to X); White (adds squares and cross terms, so catches more forms but has less power). Null = homoscedastic.
- Fix 1, robust SEs (the HC0-HC3 family; HC3 is the safe choice in small samples): keep the same β, change only the SEs. This is the default in practice.
- Fix 2, WLS: weight each point by 1/variance. More efficient than OLS, but only if you model the variance correctly.
- Fix 3, transform y (log for multiplicative errors, e.g. income, prices) or model with a GLM.
- Consequence if ignored: confidence intervals and p-values are too narrow or too wide, but the sign of the error is unpredictable.

**Example:** House price vs size: bigger houses have much more price spread. Log-price usually makes the spread even.

**Code:**
```python
import numpy as np, statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
rng = np.random.default_rng(0)
x = rng.uniform(1, 10, 500); y = 2 + 3 * x + rng.normal(0, x)   # noise sd grows with x
X = sm.add_constant(x); m = sm.OLS(y, X).fit()
print("Breusch-Pagan p:", het_breuschpagan(m.resid, X)[1])
print("classic SE:", m.bse.round(3))
print("HC3 SE    :", m.get_robustcov_results("HC3").bse.round(3))
print("WLS SE    :", sm.WLS(y, X, weights=1 / x ** 2).fit().bse.round(3))
# Breusch-Pagan p: 6.6820655519346815e-18
# classic SE: [0.657 0.104]
# HC3 SE    : [0.449 0.106]
# WLS SE    : [0.235 0.07 ]
```
The test strongly rejects homoscedasticity; the classic intercept SE (0.657) is far off the robust one (0.449), and WLS with the right weights is tightest (0.07 on the slope).

**Follow-ups:**
- *Does it bias β?* No, only the SEs (and efficiency).
- *Why not always use HC SEs?* You can; with small n, HC3 is preferred. Cost: slightly lower power if the data were actually homoscedastic.

**Common mistakes:** Saying heteroscedasticity biases coefficients; "fixing" it by dropping outliers; using WLS with guessed weights.

### Q12 ⭐⭐⭐ 🟡 How do you read residual plots (residuals vs fitted, Q-Q, scale-location, residuals vs leverage) and what pattern signals which problem?
**Asked at:** Typical (prep sources): DS loops at product cos and consulting analytics
**Say this first (1 line):** Each of the four plots is a check for one assumption: curve = non-linearity, funnel = non-constant variance, bent Q-Q = non-normal errors, and a point far right/up in the leverage plot = influential point.

**Then explain:**

| Plot | Healthy | Pattern -> problem |
|---|---|---|
| Residuals vs fitted | Random cloud around 0 | U-shape/curve = non-linearity (add terms/transform); funnel = heteroscedasticity; clusters/trend over time = missed structure or autocorrelation |
| Normal Q-Q | Points on the diagonal | S-shape = heavy tails; curved = skew; a few far points = outliers |
| Scale-location (sqrt\|std. residual\| vs fitted) | Flat line | Upward slope = variance rising with the fitted value |
| Residuals vs leverage (with Cook's contours) | No points beyond contours | High leverage + large residual (outside the Cook's D lines) = influential point |

- Order of importance: non-linearity and influential points first (they change the model), variance second (SEs), normality last (matters mostly for small-n intervals).
- Plot, then confirm with a test (Breusch-Pagan, Shapiro/Jarque-Bera, Durbin-Watson), but trust plots at large n since tests flag trivial deviations.

**Example:** Residuals vs fitted show a smile: the true relationship is quadratic. Add x² and the curve disappears.

**Follow-ups:**
- *Residuals look fine; is the model correct?* Not necessarily: omitted variables correlated with X can still leave clean residuals.
- *Standardised vs raw residuals?* Standardised ones have comparable scale across points, better for spotting outliers (|r| > 3).

**Common mistakes:** Over-reading Q-Q wiggles in large samples; ignoring a U-shape because R² is high; treating a high-leverage point as automatically bad.

### Q13 ⭐⭐⭐ 🟡 Frequentist vs Bayesian: explain a 95% confidence interval vs a 95% credible interval in plain words, with a conversion-rate example.
**Asked at:** Likely (expert gap-check): Spotify, Booking, Zalando, Microsoft IDC, Amazon
**Say this first (1 line):** A 95% confidence interval is a statement about the *procedure* (95% of intervals built this way capture the true rate); a 95% credible interval says "given my data and prior, the rate lies in here with 95% probability".

**Then explain:**
- Frequentist: the true rate is a fixed unknown number; the interval is random. After the data, "95%" refers to the long-run hit rate of the method, not to this one interval.
- Bayesian: the rate is treated as uncertain; the posterior gives a direct probability statement about it. This is what stakeholders usually think a CI means.
- The price of the Bayesian statement: you need a prior, and the answer depends on it (more so with little data).
- With a lot of data and a weak prior the two intervals are almost identical numerically.

**Example:** 30 conversions in 200 visits (15%). Wilson CI: (0.107, 0.206). Bayesian with a flat Beta(1,1) prior gives posterior Beta(31, 171) with credible interval (0.107, 0.206). Same numbers, different interpretation: "there is a 95% probability the conversion rate is between 10.7% and 20.6%" is correct only for the credible interval.

**Follow-ups:**
- *Is a frequentist wrong to say "95% chance"?* For one specific interval, yes: it either contains the truth or not.
- *When do they differ?* Small n, informative priors, or bounded parameters near 0 or 1.

**Common mistakes:** Giving the Bayesian reading of a confidence interval; saying credible intervals need no assumptions (they need a prior); using "95% of the data lies in the interval".

### Q14 ⭐⭐⭐ 🟡 Beta-Binomial: your prior for a conversion rate is Beta(a, b) and you observe k conversions in n visits. What is the posterior, its mean, and a 95% credible interval? Show it in scipy.
**Asked at:** Likely (expert gap-check): Product cos, Europe experimentation teams (Spotify Confidence, Booking)
**Say this first (1 line):** The posterior is Beta(a + k, b + n − k), with mean (a + k)/(a + b + n); you add successes to a and failures to b.

**Then explain:**
- Beta is *conjugate* to the Binomial likelihood: prior × likelihood is again Beta, so no integration is needed.
- Read a and b as "pseudo-counts" of past successes and failures: Beta(1,1) is flat, Beta(20,180) says "about 10%, worth 200 prior visits".
- Posterior mean = weighted average of the prior mean a/(a+b) and the data k/n. More data pushes the weight to the data.
- 95% credible interval: take the 2.5% and 97.5% quantiles of the posterior (equal-tailed), or the highest-density interval.

**Example:** 30 conversions in 200 visits. Flat prior gives Beta(31, 171): mean 0.153, 95% CrI (0.107, 0.206). A Beta(20,180) prior centred on 10% pulls the mean to 0.125 with CrI (0.094, 0.159).

**Code:**
```python
import numpy as np
from scipy import stats
a, b, k, n = 1, 1, 30, 200
post = stats.beta(a + k, b + n - k)
print("flat prior    mean %.3f  95%% CrI %s" % (post.mean(), np.round(post.interval(0.95), 3)))
post2 = stats.beta(20 + k, 180 + n - k)          # informative prior centred on 10%
print("Beta(20,180)  mean %.3f  95%% CrI %s" % (post2.mean(), np.round(post2.interval(0.95), 3)))
# flat prior    mean 0.153  95% CrI [0.107 0.206]
# Beta(20,180)  mean 0.125  95% CrI [0.094 0.159]
```

**Follow-ups:**
- *What if n = 0?* The posterior equals the prior.
- *Posterior mode?* (a+k−1)/(a+b+n−2): this is the MAP estimate.
- *Other conjugates?* Gamma-Poisson (counts), Normal-Normal (means).

**Common mistakes:** Using Beta(a+k, b+k) instead of b + (n − k); forgetting that a, b are pseudo-counts so a strong prior needs a lot of data to move; calling the interval a confidence interval.

### Q15 ⭐⭐⭐ 🟡 Explain CUPED: what does it do, what is the formula, why is it unbiased, and how much variance does it remove?
**Asked at:** Typical (prep sources): Microsoft, Netflix, Spotify, Booking, Amazon; senior experimentation roles
**Say this first (1 line):** CUPED subtracts the part of the metric that a pre-experiment covariate already predicts; this keeps the treatment effect unchanged but cuts variance by a factor of (1 − ρ²), so tests need fewer users or run shorter.

**Then explain:**
- Formula: Y_cuped = Y − θ(X − X̄), with θ = Cov(Y, X)/Var(X), where X is the same metric measured *before* the experiment.
- Unbiased because assignment is random and X is measured before it, so E[X] is the same in both arms. The adjustment term averages to zero in each arm and the difference in means is unchanged in expectation.
- Variance: Var(Y_cuped) = Var(Y)(1 − ρ²). With ρ = 0.7 you cut variance by about 50%, equivalent to doubling the sample size.
- It is just regression adjustment (ANCOVA) with a single covariate (see Q52).

**Example:** Revenue per user this week, with revenue per user in the prior 4 weeks as X. Heavy spenders stay heavy spenders, so most of the noise is removed.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0); N = 20000
pre = rng.normal(10, 3, N)                       # pre-experiment metric
t = rng.integers(0, 2, N)                        # random assignment
y = 0.8 * pre + rng.normal(0, 2, N) + 0.2 * t    # true effect = 0.2
theta = np.cov(y, pre)[0, 1] / np.var(pre, ddof=1)
y_c = y - theta * (pre - pre.mean())
def est(v):
    d = v[t == 1].mean() - v[t == 0].mean()
    se = np.sqrt(v[t == 1].var(ddof=1) / (t == 1).sum() + v[t == 0].var(ddof=1) / (t == 0).sum())
    return round(float(d), 3), round(float(se), 4)
print("theta %.2f  rho^2 %.2f" % (theta, np.corrcoef(y, pre)[0, 1] ** 2))
print("raw   (effect, SE):", est(y)); print("CUPED (effect, SE):", est(y_c))
# theta 0.80  rho^2 0.59
# raw   (effect, SE): (0.237, 0.0443)
# CUPED (effect, SE): (0.213, 0.0285)
```
SE drops from 0.044 to 0.029; variance ratio ≈ 0.41 = 1 − 0.59. Both estimates are noisy versions of the true 0.2, but the CUPED one is tighter.

**Follow-ups:**
- *What if X is affected by the treatment?* Then it is biased. Use only pre-treatment data.
- *Users with no history?* Use θ = 0 / impute the mean, or CUPED on the subset with history only.

**Common mistakes:** Using a post-treatment covariate; estimating θ separately per arm without care; thinking CUPED changes the estimand (it does not).

### Q16 ⭐⭐⭐ 🟡 What is the peeking problem? Simulate how checking an A/B test daily inflates the false-positive rate, and name two valid fixes.
**Asked at:** Typical (prep sources): Spotify, Booking, Zalando, Flipkart, Swiggy experimentation roles
**Say this first (1 line):** Peeking means testing repeatedly and stopping as soon as p < 0.05; every extra look is another chance to be fooled, so the real false-positive rate climbs far above 5%.

**Then explain:**
- A p-value is only valid if the sample size is fixed in advance. Early on the z-statistic is noisy and wanders across ±1.96 easily; "stop when significant" picks the lucky moment.
- Simulation (A/A test, 14 daily looks, 200 users per arm per day): about 22% false positives with daily peeking vs 5% when you look only at the end.
- Valid fixes:
  1. Fixed horizon: decide the sample size up front and only read the result at the end.
  2. Sequential methods: group sequential designs with alpha spending (O'Brien-Fleming, Pocock) or always-valid inference (mSPRT/confidence sequences, see Q34 and Q57).
  3. (Also) Bayesian decision rules with an expected-loss threshold and a minimum runtime, though raw "P(B>A) > 95%" stopping is *not* free of the problem.

**Example:** A PM checks the dashboard every morning for two weeks and ships on the first "significant" day: the real error rate is ~4x what they believe.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
sims, days, per = 4000, 14, 200                  # A/A test: no true difference
a = rng.normal(size=(sims, days, per)); b = rng.normal(size=(sims, days, per))
n = per * np.arange(1, days + 1)                 # cumulative users per arm
ma, mb = a.sum(2).cumsum(1) / n, b.sum(2).cumsum(1) / n
va = ((a ** 2).sum(2).cumsum(1) - n * ma ** 2) / (n - 1); vb = ((b ** 2).sum(2).cumsum(1) - n * mb ** 2) / (n - 1)
sig = np.abs((ma - mb) / np.sqrt((va + vb) / n)) > 1.96
print("false positive, peek daily :", sig.any(1).mean())
print("false positive, look once  :", sig[:, -1].mean())
# false positive, peek daily : 0.2255
# false positive, look once  : 0.05275
```

**Follow-ups:**
- *Why not just use a stricter alpha like 0.01?* It helps but is arbitrary; proper alpha-spending gives the required total of 5% with better power.
- *Is monitoring for harm (guardrails) also peeking?* Yes in principle; use sequential tests designed for it.

**Common mistakes:** Saying peeking only matters with small samples; "we'll just stop if it is significant"; claiming Bayesian methods are automatically immune.

### Q17 ⭐⭐⭐ 🟡 How do you estimate a probability, an integral or pi using Monte Carlo? How many simulations do you need for a given accuracy?
**Asked at:** Typical (prep sources): Quant firms; DS rounds that ask simulation answers
**Say this first (1 line):** Simulate lots of random draws, count or average, and the error shrinks as 1/√n; to halve the error you need 4x the samples.

**Then explain:**
- Probability: P(A) ≈ fraction of simulations where A happens.
- Integral over [0,1]: ∫f(x)dx = E[f(U)] with U uniform, so average f over random points.
- Pi: throw points in the unit square, the fraction inside the quarter-circle x²+y²<1 is π/4. Multiply by 4.
- Accuracy: standard error = σ/√n. For a probability, n = (1.96)²·p(1−p)/ε² for a 95% margin ε. For p = 0.5 and ε = 0.001 you need about 960,000 draws. Worst case is p = 0.5; rare events need many more.
- Convergence rate does not depend on dimension, so MC beats grid methods in high dimensions.

**Example:** Estimate the probability that a portfolio loses >10% by simulating 100k return paths.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0); M = 1_000_000
xy = rng.random((M, 2))
hit = (xy ** 2).sum(1) < 1
print("pi ~", 4 * hit.mean(), " SE ~", 4 * hit.std() / np.sqrt(M))
print("int_0^1 exp(-x^2) ~", np.exp(-rng.random(M) ** 2).mean(), "(true 0.7468)")
print("n for +-0.001 on a p=0.5 estimate:", int((1.96 * 0.5 / 0.001) ** 2))
# pi ~ 3.141168  SE ~ 0.0016424784917240165
# int_0^1 exp(-x^2) ~ 0.7468997570965495 (true 0.7468)
# n for +-0.001 on a p=0.5 estimate: 960400
```

**Follow-ups:**
- *How do you speed up convergence?* Variance reduction: antithetic variables, control variates, importance sampling (Q58), quasi-random (Sobol) sequences.
- *Why is pi by MC a bad way to get pi?* Error ~1/√n: 6 digits needs ~10¹² points.

**Common mistakes:** Forgetting the 1/√n rate; using unseeded random numbers so results cannot be reproduced; trusting an estimate without reporting its standard error.

### Q18 ⭐⭐⭐ 🟡 Why does a Bayesian posterior depend on the prior and how do you pick one? Show how the posterior changes for an informative vs a flat prior and small vs large n.
**Asked at:** Likely (expert gap-check): Product cos, Europe experimentation teams
**Say this first (1 line):** The posterior is a compromise between prior and data; a strong prior or small n keeps it near the prior, a weak prior or large n lets the data dominate.

**Then explain:**
- Pick priors by: domain knowledge/historical data (informative), a weak regularising prior (e.g. Beta(1,1) or a mildly informative one), or an empirical prior fitted from similar past experiments. Run a sensitivity analysis with several priors.
- With a Beta prior, a + b is the prior's "sample size". The data's influence = n/(n + a + b).
- Results (true-ish rate 15%, prior mean 10% for informative ones):

| Prior | Data 3/20 | Data 300/2000 |
|---|---|---|
| Beta(1,1) flat | mean 0.182, CrI [0.055, 0.363] | mean 0.150, CrI [0.135, 0.166] |
| Beta(20,180) (n_prior=200) | mean 0.105, CrI [0.068, 0.148] | mean 0.146, CrI [0.131, 0.161] |
| Beta(200,1800) (n_prior=2000) | mean 0.101, CrI [0.088, 0.114] | mean 0.125, CrI [0.115, 0.135] |

- Small n (3/20) with a flat prior gives a very wide interval; the informative prior shrinks it toward 10%. At n = 2000 the flat and moderate priors agree; only the very strong prior (worth 2000 observations) still pulls the answer.
- "Priors wash out" only if they are not too strong relative to the data and not wrong about the support.

**Example:** New product page with 20 visitors: use a prior from the average of other pages. After 2,000 visitors, the page's own data takes over.

**Follow-ups:**
- *Is an informative prior biased?* It adds bias to reduce variance, like regularisation (see Q44).
- *Flat prior = "no information"?* Not exactly; flat in p is not flat in log-odds. Use weakly informative priors.

**Common mistakes:** Saying priors are subjective so Bayes is invalid; choosing a very strong prior without justification; not checking sensitivity.

### Q19 ⭐⭐⭐ 🔴 You test positive twice on independent tests, or the test is run on a high-risk group: how do you update the posterior? Where does the independence assumption break?
**Asked at:** Likely (expert gap-check): Follow-up to the medical-test question; senior DS loops
**Say this first (1 line):** Update in odds form: posterior odds = prior odds × likelihood ratio, repeated for each independent test; with 99%/95% a second positive takes 1% to ~80%, and high-risk people start from a higher prior so the answer is higher still.

**Then explain:**
- Likelihood ratio of a positive = sensitivity/(1 − specificity) = 0.99/0.05 = 19.8.
- Prior 1%: odds 1:99 → after one positive 0.2 (16.7%) → after two 3.96 (79.8%).
- High-risk group, prior 10%: one positive gives 68.7%, two give 97.8%.
- Independence assumption (conditional on disease status): the second test's error must not be correlated with the first. This breaks when the *same* test is repeated on the same sample, when a cross-reacting condition or the same interfering substance causes false positives each time, or when the same lab error recurs. Then the second LR is much less than 19.8, and multiplying overstates the evidence.
- Also, the prior for the high-risk group must be genuinely estimated for that group, not just assumed.

**Example:** A fraud model plus a rules engine both flag a transaction. If they use the same features, the two "independent" flags are really one piece of evidence counted twice.

**Code:**
```python
sens, spec = 0.99, 0.95
lr = sens / (1 - spec)                      # likelihood ratio of a positive test = 19.8
for prior in (0.01, 0.10):
    odds = prior / (1 - prior)
    for k in (1, 2):
        o = odds * lr ** k
        print(f"prior {prior:.2f}, {k} positive test(s): posterior {o / (1 + o):.3f}")
# prior 0.01, 1 positive test(s): posterior 0.167
# prior 0.01, 2 positive test(s): posterior 0.798
# prior 0.10, 1 positive test(s): posterior 0.687
# prior 0.10, 2 positive test(s): posterior 0.978
```

**Follow-ups:**
- *Why do tests in sequence help so much when the base rate is low?* Each multiplies the odds by ~20; you only need the odds to exceed 1.
- *What if the second test is of a different type?* Use its own LR; different mechanisms are more likely to be conditionally independent.

**Common mistakes:** Multiplying probabilities instead of odds; assuming independence when errors are systematic; using the general-population prior for a high-risk group.

### Q20 ⭐⭐ 🟢 A game pays Rs 100 if you roll a six and nothing otherwise; the entry fee is Rs 20. Should you play and what is the variance of your winnings?
**Asked at:** Typical (prep sources): Interview Kickstart style EV questions; Indian product cos
**Say this first (1 line):** No: the expected profit is −Rs 3.33 per play, and the variance of the winnings is about 1,389 (sd ≈ Rs 37).

**Then explain:**
- E[payout] = 100 × 1/6 = 16.67. Subtract the fee: 16.67 − 20 = −3.33 per game.
- Variance: the payout is 100 × Bernoulli(1/6), so Var = 100² × (1/6)(5/6) = 10,000 × 5/36 = 1,388.9. The fixed fee does not change variance.
- Over 1,000 plays you expect to lose about Rs 3,333, with sd ≈ 37.3 × √1000 ≈ Rs 1,179, so you are very likely to be down.
- You would play only if the fee were below Rs 16.67 (fair price), or for entertainment.

**Example:** The house edge is 3.33/20 = 16.7% of the stake, which is how casinos and lotteries make money.

**Follow-ups:**
- *What fee makes it fair?* Rs 16.67.
- *Does a risk-seeking person play?* Possibly, but that is a utility question, not an expected-value one.

**Common mistakes:** Forgetting to subtract the fee; computing variance on net winnings as if the fee added variance; using p(1−p) without the 100² factor.

### Q21 ⭐⭐ 🟢 Two cards are drawn from a 52-card deck without replacement: probability both are aces, probability of a pair, probability the second card is red given the first is red?
**Asked at:** Typical (prep sources): Product cos, GCCs, quant firms
**Say this first (1 line):** Both aces = 1/221 ≈ 0.45%; a pair = 3/51 ≈ 5.9%; second card red given first red = 25/51 ≈ 49%.

**Then explain:**
- Two aces: 4/52 × 3/51 = 12/2652 = 1/221.
- Pair (same rank): whatever the first card is, 3 of the remaining 51 match its rank: 3/51 = 1/17.
- Red given red: 25 reds remain among 51 cards: 25/51 = 0.490 (slightly below 1/2, since drawing without replacement removes one red).

**Example:** Poker: being dealt a pocket pair is 1 in 17.

**Follow-ups:**
- *With replacement?* Aces 1/169, red-given-red 1/2.
- *Are the two draws independent?* No: the first draw changes the deck.

**Common mistakes:** Using 4/52 × 4/52 (with replacement); using 1/13 for a pair; treating "pair" as needing two specific cards.

### Q22 ⭐⭐ 🟢 What are leverage and Cook's distance? How do you flag an influential point and what do you do with it?
**Asked at:** Typical (prep sources): Prepfully, PracHub question banks; Amazon, banks/GCCs
**Say this first (1 line):** Leverage measures how unusual a point's X values are (its potential to pull the line); Cook's distance measures how much the fit actually changes when you drop that point; a point with high leverage and a large residual is influential.

**Then explain:**
- Leverage h_ii is the diagonal of the hat matrix; it lies between 0 and 1 and averages p/n (p = number of coefficients). Flag h_ii > 2p/n (or 3p/n).
- Cook's D combines residual size and leverage. It is the overall change in fitted values when the point is removed. Flag D > 4/n (common) or D > 1 (conservative).
- High leverage with a small residual is harmless (it follows the trend); a large residual with low leverage is an outlier but moves the fit little.
- What to do: investigate first (data error? different population?). Fix a genuine error; otherwise keep it and report results with and without it, or use robust regression (Huber) / a better model. Do not delete just to improve R².

**Example/Code:** One far-out wrong point flips a slope from about 2 to about 0:
```python
import numpy as np, statsmodels.api as sm
rng = np.random.default_rng(0)
x = rng.normal(size=30); y = 1 + 2 * x + rng.normal(0, .5, 30)
x[0], y[0] = 6, -5                                # one far-out point that breaks the trend
m = sm.OLS(y, sm.add_constant(x)).fit(); inf = m.get_influence()
h, cd = inf.hat_matrix_diag, inf.cooks_distance[0]
print("leverage[0] %.2f (rule of thumb 2p/n = %.2f)" % (h[0], 2 * 2 / 30))
print("Cook D[0] %.1f, next largest %.2f (rule 4/n = %.2f)" % (cd[0], np.sort(cd)[-2], 4 / 30))
print("slope with point %.2f, without %.2f" % (m.params[1], sm.OLS(y[1:], sm.add_constant(x[1:])).fit().params[1]))
# leverage[0] 0.66 (rule of thumb 2p/n = 0.13)
# Cook D[0] 25.9, next largest 0.33 (rule 4/n = 0.13)
# slope with point 0.01, without 1.82
```

**Follow-ups:**
- *Can a point be influential without looking like an outlier in the residuals?* Yes: with high leverage the line is pulled toward it, so its residual shrinks.
- *Other measures?* DFFITS, DFBETAS (effect on one coefficient).

**Common mistakes:** Deleting every flagged point; confusing outlier (in y) with leverage (in X); using the thresholds as hard rules.

### Q23 ⭐⭐ 🟢 Explain P(A|B) vs P(B|A) with the prosecutor's fallacy. When are two events independent vs mutually exclusive?
**Asked at:** Typical (prep sources): Common screening question at product cos
**Say this first (1 line):** P(A|B) and P(B|A) are different things related by Bayes; confusing them is the prosecutor's fallacy. Independent means P(A∩B) = P(A)P(B); mutually exclusive means they cannot both happen, and exclusive events (with positive probability) are actually dependent.

**Then explain:**
- Prosecutor's fallacy: "the DNA match has a 1-in-a-million chance if the suspect is innocent" is P(match | innocent). It is not P(innocent | match). In a city of 10 million people, about 10 innocent people would match, so with no other evidence P(guilty | match) ≈ 1/11.
- Link: P(A|B) = P(B|A)P(A)/P(B). You need the prior P(A) (base rate).
- Independent: knowing B does not change A. Mutually exclusive: P(A∩B) = 0. If A and B are exclusive and both possible, knowing B occurred makes A impossible, so they are dependent.

**Example:** P(a dangerous fraud | flagged) is not P(flagged | fraud); only the first matters for what an analyst should investigate, and it depends on the fraud rate.

**Follow-ups:**
- *Defender's fallacy?* Ignoring the match because "10 people would match" without considering that the match still raises the odds from 1-in-10M to 1-in-11.
- *Same as the medical test paradox?* Yes (Q3).

**Common mistakes:** Treating "independent" and "mutually exclusive" as synonyms; reading a p-value as P(hypothesis true).

### Q24 ⭐⭐ 🟡 Expected value of the maximum of two (and of n) fair dice rolls; max of n Uniform(0,1) variables.
**Asked at:** Typical (prep sources): Quant firms (Optiver-style expected maxima)
**Say this first (1 line):** E[max of two dice] = 161/36 ≈ 4.47; for n dice use E[M] = Σ_{m=0}^{5} [1 − (m/6)^n]; for n Uniform(0,1) variables E[max] = n/(n+1).

**Then explain:**
- Use the CDF: P(M ≤ m) = (m/6)^n. For non-negative integer M, E[M] = Σ_{m≥0} P(M > m) = Σ_{m=0}^{5} [1 − (m/6)^n].
- n = 2: 6 − (0+1+4+9+16+25)/36 = 6 − 55/36 = 161/36 = 4.472.
- n = 1: 3.5; n = 3: 4.958; n = 10: 5.820. It climbs toward 6 as n grows.
- Uniform: P(M ≤ x) = x^n, density n·x^(n−1), so E[M] = ∫ x·n·x^(n−1)dx = n/(n+1). The max gets close to 1 as n grows (n = 9 gives 0.9). By symmetry E[min] = 1/(n+1).

**Example:** Max of n server latencies is what a user-facing request waits for (fan-out), and it grows with n even if each server is the same.

**Follow-ups:**
- *Distribution of the max of n uniforms?* Beta(n, 1) (see Q53).
- *Expected min of two dice?* 91/36 ≈ 2.53; check: E[max] + E[min] = 7.

**Common mistakes:** Averaging the two dice; forgetting that the CDF of the max is the product of CDFs.

### Q25 ⭐⭐ 🟡 Use linearity of expectation: expected number of fixed points in a random permutation, expected number of distinct birthdays, expected number of empty bins.
**Asked at:** Typical (prep sources): Quant firms; probability rounds at big tech
**Say this first (1 line):** Write the count as a sum of indicator variables and add their expectations; independence is not needed. Fixed points = 1, distinct birthdays among 23 ≈ 22.32, empty bins with n balls in n bins ≈ n/e.

**Then explain:**
- Linearity of expectation: E[ΣX_i] = ΣE[X_i], always true, even for dependent events.
- Fixed points in a random permutation of n: each position is fixed with prob 1/n, so E = n × 1/n = 1 for every n.
- Distinct birthdays among n people (365 days): each day is "covered" with prob 1 − (364/365)^n, so E = 365(1 − (364/365)^n); n = 23 gives 22.32.
- Empty bins: m balls into n bins: each bin is empty with prob (1 − 1/n)^m, so E = n(1 − 1/n)^m; for m = n this is ≈ n/e ≈ 0.368n.

**Example:** Hashing 100 keys into 100 buckets leaves about 37 buckets empty.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
print("fixed points (n=10):", np.mean([(rng.permutation(10) == np.arange(10)).sum() for _ in range(100000)]))
print("distinct birthdays, 23 people:", 365 * (1 - (364 / 365) ** 23))
print("empty bins, 100 balls in 100 bins:", 100 * (1 - 1 / 100) ** 100)
# fixed points (n=10): 0.99937
# distinct birthdays, 23 people: 22.319962396220888
# empty bins, 100 balls in 100 bins: 36.60323412732292
```

**Follow-ups:**
- *Variance of fixed points?* Also 1 (the count is approximately Poisson(1)).
- *Why is this trick powerful?* It avoids computing the full distribution.

**Common mistakes:** Believing you need independence; computing the full distribution instead of using indicators.

### Q26 ⭐⭐ 🟡 Gambler's ruin: you start with Rs i, bet Rs 1 on a fair coin, stop at 0 or N. What is the probability of ruin and expected duration? What changes if the coin is biased?
**Asked at:** Typical (prep sources): Optiver (random walk with absorbing barriers), Jane Street style
**Say this first (1 line):** For a fair game, P(ruin) = 1 − i/N and the expected duration is i(N − i); with a biased coin, ruin is far more likely and the formulas use r = q/p.

**Then explain:**
- Fair coin: your wealth is a martingale, so E[final] = i. Final is 0 or N, so P(reach N) = i/N and P(ruin) = 1 − i/N.
- Duration: E[T] = i(N − i), largest when you start in the middle (N/2)².
- Biased (win prob p, q = 1 − p, r = q/p ≠ 1): P(ruin) = (r^i − r^N)/(1 − r^N); E[T] = i/(q−p) − (N/(q−p))·(1 − r^i)/(1 − r^N).
- Even a small negative edge (p = 0.45) makes ruin the overwhelming outcome; as N → ∞ with p ≤ 1/2, ruin prob → 1.

**Example:** Start with Rs 3, target Rs 10. Fair: ruin 70%, 21 bets on average. With p = 0.45: ruin 87.2%, 17.2 bets.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
def sim(i, N, p, T=20000):
    ruined = steps = 0
    for _ in range(T):
        x = i; t = 0
        while 0 < x < N: x += 1 if rng.random() < p else -1; t += 1
        ruined += (x == 0); steps += t
    return ruined / T, steps / T
i, N = 3, 10
print("fair   sim:", sim(i, N, .5), " theory:", (1 - i / N, i * (N - i)))
p = .45; q = 1 - p; r = q / p
ruin = (r ** i - r ** N) / (1 - r ** N); dur = i / (q - p) - N / (q - p) * (1 - r ** i) / (1 - r ** N)
print("p=.45  sim:", sim(i, N, p), " theory:", (ruin, dur))
# fair   sim: (0.69705, 21.1381)  theory: (0.7, 21)
# p=.45  sim: (0.87325, 17.2413)  theory: (0.8717476511872477, 17.174765118724764)
```

**Follow-ups:**
- *Casino with infinite bankroll?* The gambler with finite wealth and any edge against them is ruined with prob 1 eventually.
- *Link to Kelly?* Bet sizing to avoid ruin (Q48).

**Common mistakes:** Using the fair formulas for a biased coin; forgetting the duration formula; confusing "N" (target) with number of bets.

### Q27 ⭐⭐ 🟡 Simple symmetric random walk: what is the probability of returning to the origin, expected steps to hit +a or -b, and why does it matter for stock-price modelling?
**Asked at:** Typical (prep sources): Optiver, quant-flavoured DS roles
**Say this first (1 line):** A symmetric 1D walk returns to the origin with probability 1 (recurrent), starting from 0 it hits +a before −b with probability b/(a+b), and takes ab steps on average.

**Then explain:**
- P(at 0 after 2n steps) = C(2n, n)/4^n ≈ 1/√(πn): after 100 steps it is 7.96%. It shrinks, but the sum diverges, so the walk returns infinitely often.
- Hitting: it is the gambler's ruin problem: P(hit +a before −b) = b/(a+b); E[steps] = a·b.
- Spread grows like √t: after t steps the typical distance is √t, not t.
- Stock modelling: price changes as unpredictable increments is the random-walk (efficient market) idea: variance grows linearly with time, so volatility scales with √t (annual vol ≈ daily vol × √252). Real prices are better modelled with log-returns (geometric Brownian motion, prices stay positive); real markets have fat tails and volatility clustering.
- In 2D it is still recurrent; in 3 or more dimensions it is transient.

**Example:** A trader betting Rs 1 on a fair coin with a Rs 5 profit target (a = 5) and a Rs 3 stop-loss (b = 3) reaches the target first with probability b/(a+b) = 3/8 = 37.5%, after ab = 15 bets on average (the code below uses a = 3, b = 5). The nearer barrier is hit more often, even though the game is fair.

**Code:**
```python
import numpy as np, math
rng = np.random.default_rng(0); a, b, T = 3, 5, 20000
hit_up = steps = 0
for _ in range(T):
    x = t = 0
    while -b < x < a: x += 1 if rng.random() < .5 else -1; t += 1
    hit_up += (x == a); steps += t
print("P(hit +a) sim %.3f theory %.3f | E[steps] sim %.2f theory %d" % (hit_up / T, b / (a + b), steps / T, a * b))
print("P(at 0 after 100 steps) =", math.comb(100, 50) / 2 ** 100, " approx", 1 / math.sqrt(math.pi * 50))
# P(hit +a) sim 0.631 theory 0.625 | E[steps] sim 15.09 theory 15
# P(at 0 after 100 steps) = 0.07958923738717877  approx 0.07978845608028654
```

**Follow-ups:**
- *Expected return time to the origin?* Infinite, even though return is certain.
- *Does a random walk mean you cannot predict returns?* Roughly the weak-form efficient market claim; volatility can still be forecast.

**Common mistakes:** Saying the walk drifts away linearly; stating prices (rather than log prices) are a symmetric walk; confusing "returns with prob 1" with "returns quickly".

### Q28 ⭐⭐ 🟡 What is a Markov chain? How do you find the stationary distribution of a transition matrix, and when does it exist and converge?
**Asked at:** Typical (prep sources): Jane Street style steady-state questions; Flipkart/Amazon DS theory rounds
**Say this first (1 line):** A Markov chain moves between states where the next state depends only on the current one; its stationary distribution π solves πP = π (sum to 1), exists for any finite chain, is unique if irreducible, and the chain converges to it if it is also aperiodic.

**Then explain:**
- Transition matrix P: row i holds probabilities of going from state i, each row sums to 1.
- Find π: left eigenvector of P with eigenvalue 1 (eigenvector of Pᵀ), normalised to sum 1; or solve πP = π with Σπ = 1; or just raise P to a high power.
- Irreducible = every state can reach every other; aperiodic = no fixed cycle length (e.g. a two-state flip-flop is periodic, so it never converges but still has a stationary distribution).
- Reading π: long-run fraction of time spent in each state.

**Example:** A user is Active, Casual or Lapsed each week with the transition matrix in the code below. After many weeks the user spends about 64% of weeks Active, 27% Casual and 9% Lapsed, whatever state they started in (hand-built illustrative matrix, not real data).

**Code:**
```python
import numpy as np
P = np.array([[.9, .1, 0], [.2, .7, .1], [.1, .2, .7]])
w, v = np.linalg.eig(P.T)                         # pi P = pi  <=>  P^T pi = pi (eigenvalue 1)
pi = np.real(v[:, np.argmin(abs(w - 1))]); pi /= pi.sum()
print("pi:", pi.round(4), " check pi@P == pi:", np.allclose(pi @ P, pi))
print("row of P^100:", np.linalg.matrix_power(P, 100)[0].round(4))
# pi: [0.6364 0.2727 0.0909]  check pi@P == pi: True
# row of P^100: [0.6364 0.2727 0.0909]
```

**Follow-ups:**
- *Speed of convergence?* Governed by the second-largest eigenvalue magnitude (spectral gap).
- *Where used?* PageRank, MCMC, user-state modelling, HMMs.

**Common mistakes:** Using the right eigenvector of P (gives all-ones); forgetting to normalise; claiming convergence for a periodic chain.

### Q29 ⭐⭐ 🟡 Model user states (active, dormant, churned) as a Markov chain: how do you estimate the transition matrix, compute expected lifetime, and sanity-check the Markov assumption?
**Asked at:** Likely (expert gap-check): Swiggy, Flipkart, PhonePe product analytics roles
**Say this first (1 line):** Count transitions between states per period and normalise each row to get P; expected lifetime comes from the fundamental matrix N = (I − Q)⁻¹ where Q is the transient-to-transient block; then check the Markov assumption empirically.

**Then explain:**
- States: active, dormant, churned (absorbing: once churned, stays churned). Each user-period gives one transition observation.
- Estimate: P̂_ij = count(i → j)/count(i →). It is the maximum-likelihood estimate; add smoothing for rare transitions.
- Expected lifetime: with Q the 2×2 block among transient states (active, dormant), N = (I − Q)⁻¹ has N_ij = expected periods spent in j starting from i. Row sums give the expected time to churn. In the simulation below: 11.77 months from active (truth 11.82).
- Sanity-check Markov: (1) compare next-state distribution given (current, previous) vs given current only; if previous state matters, it is not first-order Markov (here prev=active vs prev=dormant give the same row). (2) check stationarity across cohorts/time, (3) compare the model's predicted retention curve with actual cohort retention. Common failure causes: tenure effects (hazard falls with age), user heterogeneity, seasonality.

**Example:** A subscription app with monthly states Active, Dormant, Churned. If the estimated Active row is (0.80, 0.15, 0.05) and the Dormant row is (0.30, 0.50, 0.20), a new Active user is expected to stay about 11.8 months before churning (simulated, illustrative data in the code below).

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
true = np.array([[.80, .15, .05], [.30, .50, .20], [0, 0, 1.]])   # active, dormant, churned
U, T = 5000, 12; S = np.zeros((U, T), int); cum = true.cumsum(1)
for t in range(1, T): S[:, t] = (rng.random(U)[:, None] > cum[S[:, t - 1]]).sum(1)
cnt = np.zeros((3, 3)); np.add.at(cnt, (S[:, :-1].ravel(), S[:, 1:].ravel()), 1)
P = cnt / cnt.sum(1, keepdims=True); print(P.round(3))             # estimate = row-normalised counts
Q = P[:2, :2]; N = np.linalg.inv(np.eye(2) - Q)                    # fundamental matrix
print("expected months until churn, from active: %.2f (true %.2f)" % (N[0].sum(), np.linalg.inv(np.eye(2) - true[:2, :2])[0].sum()))
prev, cur, nxt = S[:, :-2].ravel(), S[:, 1:-1].ravel(), S[:, 2:].ravel()   # Markov check
for a in (0, 1):
    m = (cur == 0) & (prev == a); print("prev=%d -> P(next | now active):" % a, (np.bincount(nxt[m], minlength=3) / m.sum()).round(3))
# [[0.799 0.15  0.051]
#  [0.298 0.505 0.197]
#  [0.    0.    1.   ]]
# expected months until churn, from active: 11.77 (true 11.82)
# prev=0 -> P(next | now active): [0.801 0.148 0.051]
# prev=1 -> P(next | now active): [0.791 0.152 0.057]
```
(The small gap between 11.77 and 11.82 is sampling noise from 5,000 users; more users shrink it. Here one period = one month.)

**Follow-ups:**
- *Reactivation of churned users?* Make "churned" non-absorbing, or add a "resurrected" state.
- *Tenure dependence?* Use a semi-Markov model, or add age bucket into the state.

**Common mistakes:** Row-normalising the wrong axis; treating churned as a normal state when computing lifetime; never testing the Markov assumption.

### Q30 ⭐⭐ 🟡 How is PageRank a Markov chain? Explain the damping factor and implement power iteration in NumPy.
**Asked at:** Likely (expert gap-check): Search/recsys-flavoured DS and MLE loops
**Say this first (1 line):** PageRank is the stationary distribution of a "random surfer" Markov chain: follow a random outgoing link with probability d, or jump to a random page with probability 1 − d (d = 0.85 typically); the damping makes the chain irreducible and aperiodic so a unique answer exists.

**Then explain:**
- Transition matrix: P_ij = 1/outdegree(i) if i links to j. Pages with no outlinks (dangling) are treated as linking to all pages.
- Google matrix: G = dP + (1 − d)(1/n)·11ᵀ. Every entry is positive, so the chain is irreducible and aperiodic; the Perron-Frobenius theorem gives a unique stationary vector.
- Power iteration: start with r = uniform, repeat r ← r·G (written as d·r·P + (1 − d)/n) until it stops changing. The error shrinks by at most a factor d = 0.85 per iteration (worst case about 140 iterations for 1e-10; this small graph needs only 31). Cost per iteration O(number of links) with sparse matrices.
- d trades off fidelity to links (d → 1, slow convergence, can be dominated by traps/sinks) against uniformity (d → 0).

**Example:** In the 4-page toy web below, page 2 is linked from pages 0, 1 and 3, so it ends up with 43% of the rank; page 1 is linked only from page 0, so it gets the least (13%).

**Code:**
```python
import numpy as np
L = np.array([[0, 1, 1, 0], [0, 0, 1, 0], [1, 0, 0, 1], [0, 0, 1, 0]], float)   # L[i,j]=1: page i links to j
def pagerank(L, d=0.85, tol=1e-10):
    n = len(L); out = L.sum(1, keepdims=True)
    P = np.where(out > 0, L / np.where(out > 0, out, 1), 1 / n)      # dangling page -> jump anywhere
    r = np.ones(n) / n
    for it in range(1000):
        r_new = d * r @ P + (1 - d) / n                              # follow link w.p. d, teleport w.p. 1-d
        if np.abs(r_new - r).sum() < tol: return r_new, it
        r = r_new
    return r, it
r, it = pagerank(L); print(r.round(4), r.sum().round(6), "iterations:", it)
# [0.2199 0.131  0.4292 0.2199] 1.0 iterations: 31
```
Page index 2 receives the most links, so it gets the highest score.

**Follow-ups:**
- *Why not solve the eigenproblem directly?* Web-scale matrices are huge and sparse; power iteration only needs matrix-vector products.
- *Personalised PageRank?* Teleport to a chosen set of pages instead of uniform.

**Common mistakes:** Forgetting dangling nodes (the mass leaks); mixing up row/column orientation; thinking d is the probability of a random jump.

### Q31 ⭐⭐ 🟡 Bayesian A/B test: with Beta posteriors for A and B, how do you compute P(B > A) and expected loss? How does it differ from a p-value?
**Asked at:** Likely (expert gap-check): Spotify Confidence, Booking, Zalando, Microsoft
**Say this first (1 line):** Draw samples from each Beta posterior and compute the share of draws where B > A, plus the expected loss of each decision; this answers "how likely is B better and what do I risk" directly, which a p-value does not.

**Then explain:**
- With Beta(1,1) priors, posteriors are Beta(1+k, 1+n−k). Sample 500k from each: P(B > A) = mean(b > a).
- Expected loss of shipping B = E[max(a − b, 0)] (how much conversion you give up on average if A was actually better). Choose B if the loss is below a tolerance threshold you set (e.g. 0.1% abs).
- p-value: P(data at least this extreme | no difference). Bayesian: P(B > A | data). Different questions; the Bayesian one uses a prior and needs no null hypothesis, and the loss weighs the size of the mistakes.
- Caution: Bayesian stopping rules are still affected by peeking if you stop on "P(B>A) > 95%" without a loss threshold/minimum sample (see Q16).

**Example:** A 120/1000 (12.0%), B 140/1000 (14.0%). Two-sided z-test p = 0.184: "not significant". Bayesian: P(B > A) = 0.91; expected loss from shipping B ≈ 0.0006 (0.06 pp), from keeping A ≈ 0.021 (2.1 pp). Same data, but the Bayesian output is more useful for deciding.

**Code:**
```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
kA, nA, kB, nB = 120, 1000, 140, 1000
a = stats.beta(1 + kA, 1 + nA - kA).rvs(500_000, random_state=1)
b = stats.beta(1 + kB, 1 + nB - kB).rvs(500_000, random_state=2)
print("P(B > A)            :", (b > a).mean().round(3))
print("expected loss ship B:", np.maximum(a - b, 0).mean().round(5))
print("expected loss keep A:", np.maximum(b - a, 0).mean().round(5))
print("p-value (z-test)    :", proportions_ztest([kB, kA], [nB, nA])[1].round(3))
# P(B > A)            : 0.908
# expected loss ship B: 0.00065
# expected loss keep A: 0.02058
# p-value (z-test)    : 0.184
```

**Follow-ups:**
- *Is P(B>A) = 0.91 just 1 − p/2 (one-sided p-value)?* Here it matches (1 − 0.184/2 = 0.908), but that is a coincidence of a flat prior, large n and near-normal posteriors. With an informative prior, small n or rates near 0 or 1 the two diverge, and their meanings differ anyway.
- *What threshold?* Set on business cost: ship if expected loss < the smallest effect you care about.

**Common mistakes:** Calling P(B>A) a p-value; ignoring the prior; shipping on probability alone without effect size or expected loss.

### Q32 ⭐⭐ 🟡 Give the main ways to reduce variance in an experiment metric (CUPED/regression adjustment, stratification, post-stratification, winsorizing, control variates) and when to use which.
**Asked at:** Typical (prep sources): TechPrep, PracHub variance-reduction banks; Booking, Spotify, Netflix
**Say this first (1 line):** Use CUPED (regression adjustment on pre-experiment data) as the default, add stratification when a few categories drive the metric, winsorize heavy tails, and treat control variates as the general idea behind all of them.

**Then explain:**
| Method | What it does | Use when |
|---|---|---|
| CUPED / regression adjustment | Subtracts the part of Y predicted by a pre-period covariate X: Y − θ(X − mean X) | You have pre-experiment history correlated with the metric. Variance falls by about ρ² |
| Stratification (design time) | Randomize within strata (country, platform) so group mix is balanced | Few strong categorical drivers; you control assignment |
| Post-stratification | Reweight by strata after the fact | Same drivers, but assignment was already done |
| Winsorizing / capping | Clip extreme values at, say, the 99th percentile | Heavy tails (revenue); accept a small bias for a big variance cut (Q50) |
| Control variates | Subtract any variable with a known mean that correlates with Y | The general trick; CUPED is the special case where X is pre-period Y |
| More data / longer run | Variance falls as 1/n | Last resort; it costs time |
- They stack: stratify, then CUPED, then winsorize.
- All except winsorizing keep the effect estimate unbiased.
- Lower variance means a smaller minimum detectable effect or fewer days.

**Example:** Spend per user has ρ = 0.75 with last month's spend. CUPED cuts variance by about 56% (ρ² = 0.56), so you need about 44% of the sample.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
n = 20000
x = rng.gamma(2, 10, n)                      # pre-period spend
y = 0.8 * x + rng.normal(0, 10, n)           # in-experiment spend
theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
y_cuped = y - theta * (x - x.mean())
print("var raw  :", round(y.var(ddof=1), 1))
print("var CUPED:", round(y_cuped.var(ddof=1), 1))
print("reduction:", round(1 - y_cuped.var() / y.var(), 3), " rho^2:", round(np.corrcoef(x, y)[0, 1]**2, 3))
# var raw  : 227.9
# var CUPED: 99.2
# reduction: 0.565  rho^2: 0.565
```

**Follow-ups:**
- *Why is CUPED unbiased?* X is measured before assignment, so X has the same mean in both arms; subtracting θ(X − mean X) shifts both arms by the same expected amount.
- *Winsorizing vs trimming?* Winsorizing clips the value; trimming drops the rows. Both bias the mean (Q50).

**Common mistakes:** Using a post-treatment covariate (biases the effect); winsorizing separately per arm; expecting CUPED to help when ρ is near 0.

### Q33 ⭐⭐ 🟡 How do you choose a CUPED covariate? Why must it be pre-experiment, what happens with new users who have no history, and does CUPED work with ratio metrics?
**Asked at:** Typical (prep sources): PracHub CUPED questions; Spotify Confidence RFP
**Say this first (1 line):** Pick a pre-experiment variable that predicts the outcome strongly (ideally the same metric from the pre-period), because it must be unaffected by treatment, and handle users without history with an indicator plus imputation.

**Then explain:**
- **Why pre-experiment:** if X is measured after assignment, treatment can change it, and adjusting for it removes or distorts part of the true effect (bias). Pre-period X is independent of assignment, so adjustment is safe.
- **How to choose:** highest correlation with Y wins (variance falls by ρ²). Usually the same metric over the prior 1 to 4 weeks. Multiple covariates are fine through regression; avoid overfitting with a handful of strong ones.
- **New users:** no history. Impute with the mean (or 0) and add a "has history" flag as a second covariate. They get no variance reduction, so the overall gain is diluted by their share. Alternative: use a pre-assignment signal such as country, device or acquisition channel as a covariate.
- **Ratio metrics:** yes, but not directly. Use the delta method on the numerator and denominator, apply CUPED to each, or linearize the ratio first (Q61).
- Fit θ on pooled data from both arms (or per-arm and average), not on a post-hoc subset.

**Example:** 30% of users are new. In my simulation, CUPED cut variance by 56% on the full sample but only by about 39% overall once the new users were mean-imputed (they contribute nothing).

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
n = 20000
x = rng.gamma(2, 10, n)                      # pre-period spend
y = 0.8 * x + rng.normal(0, 10, n)           # in-experiment spend
new = rng.random(n) < 0.3                    # 30% new users: no history
x_f = np.where(new, x[~new].mean(), x)       # impute mean + add indicator
Z = np.c_[x_f, new]
Zc = Z - Z.mean(0)
theta = np.linalg.lstsq(Zc, y - y.mean(), rcond=None)[0]
y_adj = y - Zc @ theta
print("variance reduction with indicator:", round(1 - y_adj.var() / y.var(), 3))
# variance reduction with indicator: 0.388
```

**Follow-ups:**
- *Is a longer lookback always better?* Not always: correlation decays with distance; test 1, 2, 4 weeks and pick on variance reduction.
- *Does CUPED change the estimand?* No, same average treatment effect, smaller standard error.

**Common mistakes:** Using in-experiment data as the covariate; fitting θ only on the control arm after peeking at results; dropping new users (introduces selection bias).

### Q34 ⭐⭐ 🟡 Explain group sequential testing and alpha spending (Pocock, O'Brien-Fleming). Why do these boundaries control Type I error?
**Asked at:** Likely (expert gap-check): Spotify, Booking, experimentation-platform teams
**Say this first (1 line):** Group sequential testing lets you look at the data at a few pre-planned times, and alpha spending sets stricter early boundaries so the total Type I error stays at 5%.

**Then explain:**
- Each look is another chance for a false positive, so using 1.96 every time inflates alpha (Q16). Boundaries must be wider than 1.96 at each look.
- **Alpha spending** says how much of the 5% you "spend" at each look, as a function of information fraction t: α(t). Because the total spent is exactly 0.05, overall Type I error is controlled; the boundaries are computed from the joint distribution of the correlated test statistics Z_1…Z_K.
- **Pocock:** same boundary at every look (about 2.36 for 4 looks). Easy to stop early but pays a lot at the end (final cutoff 2.36, not 1.96).
- **O'Brien-Fleming:** very strict early (4.05 at look 1 of 4) and nearly 1.96 at the end (2.02). Hard to stop early, almost no cost at the final analysis. Most common in practice.
- **Lan-DeMets** spending functions let looks be at unplanned times.
- Trade-off: you gain the option to stop early for a big effect or harm; you lose a little power at the end.

**Example:** 4 equally spaced looks, two-sided alpha 5%. Pocock bound is 2.36 at all looks. OBF bounds are 4.05, 2.86, 2.34, 2.02. Naive "peek and use 1.96" rejects a true null 12.6% of the time.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
K, N = 4, 400_000
Z = np.cumsum(rng.normal(size=(N, K)), axis=1) / np.sqrt(np.arange(1, K + 1))  # Z_k under H0
def calib(shape):                           # find c so that P(any |Z_k| > c*shape_k) = 0.05
    lo, hi = 1, 5
    for _ in range(40):
        c = (lo + hi) / 2
        if (np.abs(Z) > c * shape).any(1).mean() > 0.05: lo = c
        else: hi = c
    return c
t = np.arange(1, K + 1) / K
print("naive 1.96 reject rate:", (np.abs(Z) > 1.96).any(1).mean().round(3))
print("Pocock c:", round(calib(np.ones(K)), 2))
print("OBF bounds:", (calib(1/np.sqrt(t)) / np.sqrt(t)).round(2))
# naive 1.96 reject rate: 0.126
# Pocock c: 2.36
# OBF bounds: [4.05 2.86 2.34 2.02]
```

**Follow-ups:**
- *What if the looks are unplanned?* Use a Lan-DeMets spending function on actual information fraction.
- *Can I use it for futility?* Yes, with a separate (non-binding) futility boundary.

**Common mistakes:** Treating "peek only 3 times" as safe at 1.96; changing the look schedule after seeing data; forgetting that the effect estimate after early stopping is biased upward.

### Q35 ⭐⭐ 🟡 Does multicollinearity hurt prediction? How do ridge regression and PCA regression deal with it versus dropping variables?
**Asked at:** Typical (prep sources): Prepfully multicollinearity answers; Indian product cos
**Say this first (1 line):** Multicollinearity does not hurt prediction much as long as new data has the same correlation pattern; it hurts interpretation, because coefficients and standard errors become unstable.

**Then explain:**
- Correlated predictors make X'X nearly singular, so OLS coefficients swing a lot between samples (high variance, VIF > 5 to 10), but the fitted values stay stable.
- Prediction breaks only if test data breaks the correlation (extrapolation).
- **Ridge:** adds λ‖β‖² so the matrix (X'X + λI) is well conditioned; it shares weight across correlated variables and trades a little bias for much less variance. Keeps all variables.
- **PCA regression:** regress on the top principal components (uncorrelated by construction); drops low-variance directions, but components are hard to interpret and may ignore directions that matter for y.
- **Dropping variables:** simple and interpretable, but arbitrary which of the correlated pair you drop, and you may lose signal. Lasso also picks one of a correlated group semi-randomly.
- Rule: want prediction, use ridge/elastic net; want a causal coefficient, collect better data or use domain knowledge to choose.

**Example:** x1 and x2 are near copies (VIF about 196). Over 200 resamples the OLS coefficient SD is about 1.0 for each, while ridge (α = 10) has SD 0.05. The sum x1 + x2 is stable under OLS (SD 0.07): the data identify the sum, not the split.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
def fit(seed, n=200):
    r = np.random.default_rng(seed); z = r.normal(size=n)
    X = np.c_[z + 0.05*r.normal(size=n), z + 0.05*r.normal(size=n), r.normal(size=n)]
    y = X[:, 0] + X[:, 1] + 2*X[:, 2] + r.normal(size=n)
    return LinearRegression().fit(X, y).coef_, Ridge(alpha=10).fit(X, y).coef_
ols, rd = map(np.array, zip(*[fit(s) for s in range(200)]))
print("OLS coef SD  :", ols.std(0).round(2))
print("Ridge coef SD:", rd.std(0).round(2))
print("SD of b1+b2 (OLS):", ols[:, :2].sum(1).std().round(3))
# OLS coef SD  : [1.03 1.05 0.08]
# Ridge coef SD: [0.05 0.06 0.07]
# SD of b1+b2 (OLS): 0.073
```

**Follow-ups:**
- *How do you detect it?* VIF, condition number, correlation matrix; tell-tale: high R² with insignificant coefficients.
- *Does it bias OLS?* No; OLS stays unbiased, just high variance.

**Common mistakes:** Saying multicollinearity violates OLS assumptions (only perfect collinearity does); dropping a variable then interpreting the other coefficient causally; forgetting to standardize before ridge.

### Q36 ⭐⭐ 🟡 Residuals look non-normal and right-skewed: what does it break (and not break), and when do you use a log or Box-Cox transform?
**Asked at:** Typical (prep sources): Banks/GCCs, consulting analytics, Indian product cos
**Say this first (1 line):** Non-normal residuals do not bias the coefficients and do not break the fit; they only matter for small-sample t/F tests and prediction intervals, and a log transform helps when the skew comes from a multiplicative process.

**Then explain:**
- **Not broken:** unbiasedness and consistency (need only zero-mean errors), and the BLUE property. With a large n, the central limit theorem makes the coefficient tests fine.
- **Broken:** exact small-sample t and F tests, and prediction intervals (they assume symmetric normal errors, so skew gives wrong tail coverage).
- Right-skewed residuals usually mean y is multiplicative or strictly positive (prices, revenue, durations) or has outliers. Check for outliers/leverage first (Q22).
- **Log transform:** good when y > 0, variance grows with the mean, and effects are percent changes. Coefficient reads as roughly 100·β % change in y per unit x. Predictions back on the original scale need a bias correction (smearing).
- **Box-Cox:** estimates the power λ by maximum likelihood (λ = 0 is log, 1 is no change); requires y > 0. Use Yeo-Johnson if y can be ≤ 0.
- Alternatives: GLM (Gamma with log link), quantile regression, or robust SEs.

**Example:** y = exp(0.3x + noise). Raw residual skew is 2.19; after log it is 0.11. The log-model slope is 0.299 (true 0.3) and Box-Cox picks λ = 0.0.

**Code:**
```python
import numpy as np, statsmodels.api as sm
from scipy import stats
rng = np.random.default_rng(0)
n = 2000; x = rng.uniform(1, 10, n); y = np.exp(0.3*x + rng.normal(0, 0.4, n))
X = sm.add_constant(x)
r1 = sm.OLS(y, X).fit(); r2 = sm.OLS(np.log(y), X).fit()
print("skew raw / log:", stats.skew(r1.resid).round(2), stats.skew(r2.resid).round(2))
print("log-model slope:", r2.params[1].round(3))
print("Box-Cox lambda:", round(stats.boxcox(y)[1], 3))
# skew raw / log: 2.19 0.11
# log-model slope: 0.299
# Box-Cox lambda: 0.0
```

**Follow-ups:**
- *Do you always test normality?* With large n tests like Jarque-Bera reject for trivial deviations; use a Q-Q plot instead.
- *Can I just use exp(prediction) as the mean?* No: it estimates the median, which is below the mean for right-skewed data; multiply by a smearing factor or use a Gamma GLM.

**Common mistakes:** Saying non-normal residuals make OLS biased; transforming y just to pass a normality test; log of zero values without handling them.

### Q37 ⭐⭐ 🟡 How do you detect and handle autocorrelated residuals (Durbin-Watson, Ljung-Box)? Why does it invalidate standard errors?
**Asked at:** Likely (expert gap-check): Time-series-adjacent DS interviews; JPMC/banks
**Say this first (1 line):** Autocorrelated residuals mean errors are correlated over time, which keeps OLS coefficients unbiased but makes the usual standard errors too small, so you detect it with Durbin-Watson or Ljung-Box and fix it with HAC (Newey-West) errors, lags or a time-series model.

**Then explain:**
- **Why SEs break:** OLS assumes Cov(e_i, e_j) = 0. With positive autocorrelation each new point carries less new information than n suggests (effective sample size is smaller), so the naive SE is too small and t-stats and p-values too optimistic.
- **Durbin-Watson:** DW ≈ 2(1 − ρ). About 2 means no lag-1 autocorrelation; near 0 is positive, near 4 negative. Only lag 1, and invalid if lagged y is a regressor.
- **Ljung-Box:** tests whether the first m autocorrelations are jointly zero; handles higher lags.
- **Fixes:** HAC/Newey-West SEs (keep the coefficients, correct the SEs); add lagged y or lagged x; model errors as AR (GLS/GLSAR, ARIMAX); fix omitted trend or seasonality (often the real cause); use block bootstrap.

**Example:** AR(1) errors with ρ = 0.7 (n = 300, trend regressor). In the single run below DW = 0.59 and the Ljung-Box p-value is near 0. Over 500 simulated datasets the true sampling SD of the slope is 0.685, the average naive SE is 0.274 (about 2.5 times too small) and the average HAC SE (10 lags) is 0.52. HAC helps a lot but is still somewhat short with strongly persistent errors and a trending regressor.

**Code:**
```python
import numpy as np, statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_ljungbox
rng = np.random.default_rng(0)
n = 300; e = np.zeros(n)
for t in range(1, n): e[t] = 0.7*e[t-1] + rng.normal()
x = np.arange(n) / n; y = 1 + 2*x + e
X = sm.add_constant(x)
r = sm.OLS(y, X).fit()
print("DW:", durbin_watson(r.resid).round(2))
print("Ljung-Box p:", acorr_ljungbox(r.resid, lags=[10]).lb_pvalue.values.round(6))
print("naive SE:", r.bse[1].round(3))
print("HAC SE  :", sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 10}).bse[1].round(3))
# DW: 0.59
# Ljung-Box p: [0.]
# naive SE: 0.287
# HAC SE  : 0.597
```
Output of this run: DW 0.59, Ljung-Box p 0.0, naive SE 0.287, HAC SE 0.597 (single dataset, so these differ from the 500-run averages quoted above, which come from a separate 500-dataset loop of the same data-generating process).

**Follow-ups:**
- *Does autocorrelation bias beta?* No, unless a lagged dependent variable is in the model with autocorrelated errors (then it does).
- *Which test for ARCH/volatility clustering?* Ljung-Box on squared residuals or Engle's ARCH test.

**Common mistakes:** Using DW with lagged y; saying coefficients are biased; fixing with differencing without checking for a unit root; ignoring that A/B metrics over days are also correlated.

### Q38 ⭐⭐ 🟡 Break a stick at two random points: probability the three pieces form a triangle?
**Asked at:** Typical (prep sources): Classic quant geometric probability puzzle
**Say this first (1 line):** The probability is 1/4: the pieces form a triangle exactly when no piece is longer than half the stick.

**Then explain:**
- Triangle inequality: each side must be less than the sum of the other two, which for a unit stick means each piece < 1/2.
- Pick two cut points X, Y uniformly in the unit square. The pieces are min(X,Y), |X−Y| and 1−max(X,Y).
- Bad regions (some piece > 1/2): both cuts left of 1/2 (area 1/4), both right of 1/2 (area 1/4), or the cuts more than 1/2 apart (two corner triangles, total area 1/4). They do not overlap, so P(bad) = 3/4 and P(triangle) = 1/4.
- Equivalent view: the three sorted-cut piece lengths are uniform on the simplex a + b + c = 1; the triangle condition picks the middle triangle, 1/4 of its area.

**Example:** Cutting at random gives a usable triangle only 1 time in 4, so a quick simulation of 10^6 sticks should land near 0.25 (it did: 0.2507).

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
u = np.sort(rng.random((10**6, 2)), axis=1)
a, b, c = u[:, 0], u[:, 1] - u[:, 0], 1 - u[:, 1]
print(((a < .5) & (b < .5) & (c < .5)).mean())
# 0.250681
```

**Follow-ups:**
- *Why is the pieces' vector uniform on the simplex?* Sorted uniform spacings are Dirichlet(1,1,1).
- *What if you break the stick once, then break one piece?* The answer changes, because the second cut depends on the first; set it up as a conditional integral or simulate it.

**Common mistakes:** Only checking one inequality; forgetting the sorted-cut vs unsorted-cut area scaling; assuming 1/2.

### Q39 ⭐⭐ 🟡 You flip a coin 10 times and get 10 heads: probability the next is heads? Compare the frequentist MLE, Laplace smoothing and a Beta prior.
**Asked at:** Likely (expert gap-check): Bayesian intuition question at product cos and trading firms
**Say this first (1 line):** The MLE says 100% heads, which is silly after 10 flips; a Beta prior (or Laplace smoothing, which is Beta(1,1)) gives a more sensible 11/12 ≈ 0.92, and a stronger prior pulls it even closer to 0.5.

**Then explain:**
| Method | Formula | Next-head probability |
|---|---|---|
| Frequentist MLE | k/n | 10/10 = 1.00 |
| Laplace smoothing (add-one) = posterior mean, Beta(1,1) | (k+1)/(n+2) | 11/12 = 0.917 |
| Jeffreys prior Beta(0.5, 0.5) | (k+0.5)/(n+1) | 10.5/11 = 0.955 |
| Informative Beta(5,5) (a believed-fair coin) | (k+5)/(n+10) | 15/20 = 0.75 |
- MLE has zero uncertainty at the boundary and would assign 0 probability to tails; that is dangerous in classifiers (zero-frequency problem).
- Prior = pseudo-counts: Beta(a, b) acts as a imaginary heads and b imaginary tails seen before.
- As n grows the prior washes out; with 10 flips it matters a lot.
- The honest answer reports uncertainty too: posterior Beta(11, 1) has a 95% equal-tailed interval of about 0.72 to 1.00.

**Example:** Coin from a magician's pocket vs one from your wallet. Your wallet coin gets a Beta(50,50) prior (0.5 stays near 0.5); a magician's coin gets a flat prior.

**Code:**
```python
k, n = 10, 10
print("MLE      :", k / n)
print("Laplace  :", round((k + 1) / (n + 2), 3))
print("Jeffreys :", round((k + 0.5) / (n + 1), 3))
print("Beta(5,5):", (k + 5) / (n + 10))
# MLE      : 1.0
# Laplace  : 0.917
# Jeffreys : 0.955
# Beta(5,5): 0.75
```

**Follow-ups:**
- *What is Laplace's rule of succession?* (k+1)/(n+2), derived from a uniform prior.
- *Where does this show up in ML?* Naive Bayes smoothing, CTR estimation (Q41).

**Common mistakes:** Reporting 100% with no caveat; treating the prior as "free" without stating it; confusing the posterior mean with the MAP ((k+a-1)/(n+a+b-2), which is 1.0 for a flat prior).

### Q40 ⭐⭐ 🟡 Use the laws of total expectation and total variance: a random number of customers each spends a random amount. What are the mean and variance of total revenue?
**Asked at:** Likely (expert gap-check): Quant firms, Amazon/Flipkart theory rounds
**Say this first (1 line):** For a random number N of customers each spending X, the total T has mean E[N]·E[X] and variance E[N]·Var(X) + Var(N)·E[X]^2.

**Then explain:**
- **Law of total expectation:** E[T] = E[E[T | N]] = E[N·E[X]] = E[N]E[X] (customers independent of N, X i.i.d.).
- **Law of total variance:** Var(T) = E[Var(T | N)] + Var(E[T | N]) = E[N]Var(X) + Var(N)E[X]^2.
- First term is "spend randomness"; second is "footfall randomness".
- Special case Poisson(λ) customers: Var(T) = λ·E[X^2] (compound Poisson).
- Requires N independent of the individual spends, and X i.i.d.

**Example:** N ~ Poisson(20), X with mean 50 and SD 30. Mean = 1000. Var = 20·900 + 20·2500 = 68,000 (SD ≈ 261). Simulation gives mean 1000.0 and variance 68,378 (close to 68,000; the gap is sampling noise).

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
lam, mu, s = 20, 50, 30
Ns = rng.poisson(lam, 100_000)
tot = np.array([rng.gamma((mu/s)**2, s**2/mu, m).sum() for m in Ns])   # Gamma spends, mean 50, sd 30
print("mean:", tot.mean().round(0), "theory", lam*mu)
print("var :", tot.var().round(0), "theory", lam*s**2 + lam*mu**2)
# mean: 1000.0 theory 1000
# var : 68378.0 theory 68000
```

**Follow-ups:**
- *What if daily footfall is correlated with spend (rainy days)?* Then independence fails; condition on a day type and apply the laws within each.
- *Why does it matter?* Revenue forecasting: ignoring Var(N) understates uncertainty massively.

**Common mistakes:** Using only E[N]·Var(X) (forgetting the footfall term); assuming a fixed N; mixing up Var(N) with E[N] outside the Poisson case.

### Q41 ⭐⭐ 🟡 Empirical Bayes shrinkage: how do you rank restaurants or products by CTR or rating when some have very few observations?
**Asked at:** Likely (expert gap-check): Swiggy, Zalando, Booking, Flipkart ranking and recsys teams
**Say this first (1 line):** Don't rank by raw CTR; shrink each item's rate toward the overall average with a Beta prior fitted from the data (empirical Bayes), so items with few observations are pulled in strongly and items with lots of data barely move.

**Then explain:**
- Raw rate k/n is noisy for small n: 3 clicks out of 5 impressions (60%) beats 590 of 1000 (59%) but means little.
- Fit a prior Beta(a, b) to all items (method of moments or maximum likelihood on the Beta-Binomial). This is the "empirical" part: the prior comes from the data.
- Posterior mean = (k + a)/(n + a + b) = weighted average of the item's own rate and the prior mean, with weight n/(n + a + b) on the item. Small n shrinks a lot.
- Rank by the posterior mean, or by a lower credible bound (e.g. 5th percentile) if you want to be cautious about unproven items.
- This is the Beta-Binomial analogue of the James-Stein estimator and of partial pooling (Q60); it reduces total squared error even though each estimate is biased.

**Example:** 500 items with true CTR around 11% (prior Beta(20,180)) and 5 to 2,000 impressions each. The fitted prior is about Beta(16.7, 150.2). Mean squared error vs the true CTR: raw 0.00031, shrunk 0.00011. The top 5 by raw CTR had mostly tiny n (18, 18, 62, 179, 393 impressions); after shrinkage their estimates dropped from 18 to 28% to between 11 and 17%.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(1)
m = 500
p = rng.beta(20, 180, m); n = rng.integers(5, 2000, m); k = rng.binomial(n, p)
raw = k / n
mu = raw.mean()
tau2 = raw.var() - (raw * (1 - raw) / n).mean()       # true spread = observed - sampling noise
t = mu * (1 - mu) / tau2 - 1; a0, b0 = mu * t, (1 - mu) * t
post = (k + a0) / (n + a0 + b0)
print("prior Beta(%.1f, %.1f)" % (a0, b0))
print("MSE raw %.5f  shrunk %.5f" % (((raw - p)**2).mean(), ((post - p)**2).mean()))
# prior Beta(16.7, 150.2)
# MSE raw 0.00031  shrunk 0.00011
```

**Follow-ups:**
- *Why not just filter items with n < 100?* Throws away data and creates a cliff; shrinkage is smooth.
- *Bayesian vs empirical Bayes?* Empirical Bayes estimates the prior from the same data; a fully Bayesian model puts a prior on the prior (Q60).

**Common mistakes:** Sorting by raw mean; using a fixed arbitrary prior like Beta(1,1) that is far from the real base rate; using the sample variance as tau² without subtracting sampling noise.

### Q42 ⭐⭐ 🟡 AI-era: an LLM benchmark shows 83/100 correct for model A vs 80/100 for model B. How do you give a credible interval and decide if A is better? How would you review an LLM-generated statistical analysis for errors?
**Asked at:** Likely (expert gap-check): 2025-2026 GenAI evaluation roles at product cos
**Say this first (1 line):** 83 vs 80 out of 100 is well within noise: the 95% intervals overlap a lot and P(A better) is only about 0.7, so I would say the data does not show A is better.

**Then explain:**
- Each score is a binomial proportion. With a Beta(1,1) prior the posterior is Beta(1 + k, 1 + n − k): A is Beta(84, 18), B is Beta(81, 21).
- 95% credible intervals: A is 0.744 to 0.891, B is 0.711 to 0.866. They overlap heavily, and both are about ±7 points wide.
- Compare them directly: sample both posteriors; P(A > B) ≈ 0.71 and the 95% interval for A − B is about −0.08 to +0.14, which contains zero.
- Because the same test questions are given to both models, the proper comparison is paired (McNemar or a paired bootstrap on per-question wins); it is more powerful than treating them as independent.
- To tell a 3-point gap you need roughly thousands of questions (the SE of a difference of two proportions at n = 100 is about 0.055). Also watch for contamination, prompt sensitivity and run-to-run variance.

**Example:** If the same 83% vs 80% had come from 3,000 questions per model, the SE of the difference would be about 0.010 and z ≈ 3.0, so the gap would be convincing. At 100 questions it is not (hand-computed, illustrative).

**Reviewing an LLM-generated stats analysis, I check:**
- Is it the right test for the design (paired vs independent, one vs two sided)?
- Are assumptions stated and checked, and is a p-value described as "probability the null is true"? (wrong)
- Multiple comparisons, peeking, and whether it reports effect size and an interval, not just "significant".
- Does the code run on a tiny hand example and match a library result (scipy/statsmodels)? LLMs often hallucinate formulas or off-by-one degrees of freedom.

**Code:**
```python
import numpy as np
from scipy import stats
for k in (83, 80):
    print(k, np.round(stats.beta(1 + k, 101 - k).interval(0.95), 3))
a = stats.beta(84, 18).rvs(400_000, random_state=1)
b = stats.beta(81, 21).rvs(400_000, random_state=2)
print("P(A>B):", (a > b).mean().round(3), " diff 95% CI:", np.percentile(a - b, [2.5, 97.5]).round(3))
# 83 [0.744 0.891]
# 80 [0.711 0.866]
# P(A>B): 0.706  diff 95% CI: [-0.078  0.137]
```

**Follow-ups:**
- *How many questions to detect 83 vs 80?* Roughly 2,600 per model for 80% power at two-sided 5%: n = (1.96 + 0.84)² · [0.83·0.17 + 0.80·0.20] / 0.03² ≈ 2,630 unpaired. A paired design (same questions) needs fewer when the two models' right/wrong patterns are correlated.
- *Is Wilson better than the normal interval?* Yes for proportions near 0 or 1 or small n.

**Common mistakes:** Declaring a winner from a 3-point gap; using the normal approximation at small n; ignoring that questions are shared between models; accepting LLM-written statistics without rerunning them.

### Q43 ⭐⭐ 🟡 Walk through statsmodels OLS output: R-squared vs adjusted R-squared, F-test, t-stats, condition number warning, Durbin-Watson, Jarque-Bera. What would you check next?
**Asked at:** Typical (prep sources): Banks/GCCs, Amazon, Microsoft IDC
**Say this first (1 line):** I read the table top-down: does the model fit (F-test, adjusted R²), which coefficients matter (t, CI), and whether the assumptions hold (condition number, Durbin-Watson, Jarque-Bera), then I decide what to check next.

**Then explain:**
- **R² vs adjusted R²:** R² is the share of variance explained and never falls when you add a variable; adjusted R² penalises useless variables. Use adjusted (or cross-validation) to compare models.
- **F-test:** tests that all slopes are zero together. A tiny F p-value only says the model beats a constant.
- **t-stats:** coefficient / standard error, testing each coefficient is zero given the others. Big SEs on correlated variables give small t even if they matter jointly.
- **Condition number:** large (> 30 is a rough warning, ≥ 1e3 clearly bad) means multicollinearity or unscaled variables. The warning "strong multicollinearity or other numerical problems" comes from here.
- **Durbin-Watson:** ≈ 2 is fine; far from 2 means residual autocorrelation (Q37).
- **Omnibus / Jarque-Bera:** tests residual normality (skew and kurtosis); matters for small-sample inference only (Q36).
- **Next:** residual plots for non-linearity and heteroscedasticity (robust SEs), VIFs, leverage/Cook's distance, out-of-sample error.

**Example:** x2 is a noisy copy of x1 and has a true coefficient of 0. From a seeded run: R² 0.835, adj R² 0.832, F = 330 (p ≈ 2.5e-76), DW 1.92, JB p = 0.76. But x1 has coef 1.73 (true 2) with SE 0.218 and x2 has 0.38 with SE 0.233 (p = 0.106), versus SE 0.072 for the independent x3: the correlated pair has about 3 times larger SEs.

**Code:**
```python
import numpy as np, statsmodels.api as sm
rng = np.random.default_rng(0)
n = 200
x1 = rng.normal(size=n); x2 = 0.9 * x1 + rng.normal(0, .3, n); x3 = rng.normal(size=n)
y = 1 + 2 * x1 + 0 * x2 + x3 + rng.normal(size=n)
res = sm.OLS(y, sm.add_constant(np.c_[x1, x2, x3])).fit()
print(res.summary())          # R2 0.835, adj 0.832, F 330, DW 1.924, JB p 0.762, cond no 5.72
```
Condition number here is only 5.7 (variables are on one scale and the collinearity is moderate), so no warning appears; unscaled features (income in rupees next to age) are the usual trigger.

**Follow-ups:**
- *High R², no significant t-stats?* Classic multicollinearity.
- *Does a significant F mean the model is good?* No, only better than intercept-only.

**Common mistakes:** Reading R² as accuracy or causality; ignoring the condition-number warning; trusting JB with a huge n (rejects tiny deviations).

### Q44 ⭐⭐ 🟡 Explain MLE vs MAP vs full Bayesian inference and how L2/L1 regularization map to Gaussian/Laplace priors.
**Asked at:** Likely (expert gap-check): ML-theory rounds at product cos and Europe
**Say this first (1 line):** MLE picks the parameters that maximise the likelihood, MAP maximises likelihood times prior, and full Bayesian keeps the whole posterior; L2 regularisation equals a Gaussian prior and L1 equals a Laplace prior in MAP estimation.

**Then explain:**
| | Maximises / returns | Uses prior? | Output |
|---|---|---|---|
| MLE | p(data \| θ) | No | single point |
| MAP | p(data \| θ)·p(θ) | Yes | single point |
| Full Bayesian | posterior p(θ \| data) | Yes | a distribution; predict by averaging over it |
- Take the negative log: −log posterior = −log-likelihood − log prior. So regularised loss = data loss + penalty.
- **L2 / ridge:** prior θ ~ N(0, τ²) gives penalty ‖θ‖²/(2τ²). With noise variance σ², λ = σ²/τ². Smaller τ means a stronger prior and a larger λ.
- **L1 / lasso:** Laplace prior gives penalty proportional to |θ|; the sharp peak at 0 produces exact zeros.
- MAP is a point estimate, so it does not give uncertainty; with lots of data MAP ≈ MLE.
- Note: lasso/ridge point estimates are posterior modes, not posterior means (the lasso posterior mean is not sparse).

**Example:** Linear regression with σ² = 1 and τ² = 1 gives λ = 1. Closed-form MAP (XᵀX + λI)⁻¹Xᵀy matches sklearn's Ridge(alpha=1) exactly: [2.891, 0.091, 0.054, 1.524, 0.028], versus OLS [2.932, 0.089, 0.055, 1.543, 0.031]: the prior shrinks every coefficient slightly toward 0.

**Code:**
```python
import numpy as np
from sklearn.linear_model import Ridge
rng = np.random.default_rng(0)
X = rng.normal(size=(100, 5)); b = np.array([3, 0, 0, 1.5, 0]); y = X @ b + rng.normal(size=100)
lam = 1.0                                              # sigma^2 / tau^2
map_ = np.linalg.solve(X.T @ X + lam * np.eye(5), X.T @ y)
print(map_.round(3))
print(Ridge(alpha=lam, fit_intercept=False).fit(X, y).coef_.round(3))
# [2.891 0.091 0.054 1.524 0.028]  (both lines identical)
```
(The seeded rng draws X, then y, in that order; if you change the order the numbers change slightly.)

**Follow-ups:**
- *When would you go fully Bayesian?* When uncertainty matters (small data, decisions with asymmetric costs) and you can afford MCMC/VI.
- *Does the intercept get a prior?* Usually not penalised (a very wide prior).

**Common mistakes:** Saying regularisation "just prevents overfitting" with no probabilistic reading; mixing up λ with τ² (λ = σ²/τ²); claiming lasso gives the posterior mean.

### Q45 ⭐⭐ 🔴 Expected number of tosses to see HHH (or HTH) using Markov chain states or martingales.
**Asked at:** Typical (prep sources): Jane Street / quant-firm style
**Say this first (1 line):** The expected number of tosses is 14 for HHH and 10 for HTH; the difference comes from how much of a failed attempt you can reuse (overlap).

**Then explain:**
- **Markov-chain method:** states = longest suffix matching a prefix of the target (for HHH: "", H, HH, then done). Let E_s be expected remaining tosses. E_∅ = 1 + ½E_H + ½E_∅, E_H = 1 + ½E_HH + ½E_∅, E_HH = 1 + ½·0 + ½E_∅. Solve: E_HH = 8, E_H = 12, E_∅ = 14.
- **Martingale / casino trick:** a new gambler bets 1 at every toss, betting all winnings on the next target letter at fair odds (pays 2×). Expected tosses = total money in the pot when you stop = sum of 2^k over each k for which the length-k prefix of the pattern equals its suffix.
  - HHH: overlaps of length 1, 2, 3, so 2 + 4 + 8 = 14.
  - HTH: overlaps of length 1 (H) and 3 (HTH), so 2 + 8 = 10.
  - HH: 2 + 4 = 6; HT: only the full-length overlap, so 4 (matches Q7).
- Self-overlap makes the pattern harder to find (more clumpy), so it takes longer.

**Example:** HHH vs HTH: both have probability 1/8 in any 3 tosses, yet HHH takes 14 and HTH takes 10 tosses on average.

**Code:**
```python
import numpy as np
def exp_time(pat):
    states = [pat[:i] for i in range(len(pat))]           # matched-prefix states
    idx = {s: i for i, s in enumerate(states)}
    A = np.eye(len(states)); b = np.ones(len(states))
    for s in states:
        for c in "HT":
            t = s + c
            if t == pat: continue                          # absorbed: contributes 0
            while t and not pat.startswith(t): t = t[1:]   # fall back to longest valid prefix
            A[idx[s], idx[t]] -= 0.5
    return np.linalg.solve(A, b)[0]
for p in ["HHH", "HTH", "HH", "HT"]:
    print(p, exp_time(p))
# HHH 14.0   HTH 10.0   HH 6.0   HT 4.0
```

**Follow-ups:**
- *Which pattern wins a race, HHT or HTT?* Conway's leading-number method; with fair coins you can make non-transitive choices, as in Penney's game.
- *Why 2^k?* A gambler with k consecutive wins on a fair game has turned 1 into 2^k.

**Common mistakes:** Assuming every 3-pattern takes 8 tosses; resetting to the start state after any mistake (ignores overlap); forgetting that the full pattern itself counts as an overlap.

### Q46 ⭐ 🟢 Non-transitive dice: A beats B, B beats C, C beats A. Verify it by simulation, and compute the probability that one die beats another.
**Asked at:** Typical (prep sources): Quant puzzle sets
**Say this first (1 line):** Dice A = (2,2,4,4,9,9), B = (1,1,6,6,8,8) and C = (3,3,5,5,7,7) satisfy A beats B, B beats C, C beats A, each with probability 5/9, so "beats" is not transitive.

**Then explain:**
- Compare two dice by enumerating all 36 face pairs (here 9 distinct pairs, each with weight 1/9 since faces repeat).
- A vs B: A wins with a 2 or 4 only against B's 1 (1/9 each) and with a 9 against anything (3/9): 1/9 + 1/9 + 3/9 = 5/9. B vs C and C vs A work out the same way.
- Expected value is the same for A, B and C (5), so choosing "the better die" by average is misleading.
- Lesson: pairwise preference ("wins more often") need not be transitive, like voting cycles (Condorcet). A decision rule based on win probability can cycle.
- Practical link: comparing models/variants by head-to-head win rate can produce cycles; use a score rather than pairwise wins, or a full ranking model (Bradley-Terry).

**Example:** If you let a friend pick first and you choose a die after seeing theirs, you can always pick one that beats it with probability 5/9.

**Code:**
```python
import numpy as np
A = [2, 2, 4, 4, 9, 9]; B = [1, 1, 6, 6, 8, 8]; C = [3, 3, 5, 5, 7, 7]
pw = lambda X, Y: np.mean([x > y for x in X for y in Y])
print(pw(A, B), pw(B, C), pw(C, A))
print(np.mean(A), np.mean(B), np.mean(C))
rng = np.random.default_rng(0)                         # Monte Carlo check with random rolls
roll = lambda D: rng.choice(D, 200_000)
print(np.mean(roll(A) > roll(B)).round(3), np.mean(roll(B) > roll(C)).round(3), np.mean(roll(C) > roll(A)).round(3))
# 0.5556 0.5556 0.5556
# 5.0 5.0 5.0
# 0.555 0.556 0.556
```
The first line is exact enumeration; the last line is a Monte Carlo of random rolls, which agrees up to noise.

**Follow-ups:**
- *Can you design a fourth die?* Yes; with enough dice, longer cycles exist.
- *Is this related to LLM leaderboards?* Yes: pairwise win rates can cycle, so rankings need a model such as Elo or Bradley-Terry.

**Common mistakes:** Assuming "better than" is transitive; comparing only expected values; counting ties wrongly (there are none here).

### Q47 ⭐ 🟡 Poker hand probabilities: probability of a flush, a full house, and being dealt at least one ace in five cards.
**Asked at:** Typical (prep sources): Trading firms, card puzzle sets
**Say this first (1 line):** From C(52,5) = 2,598,960 hands: a flush (any 5 of one suit) is about 0.20% (0.1965% once straight flushes are excluded, the poker-ranking definition), a full house is about 0.144%, and at least one ace in five cards is about 34%.

**Then explain:**
- **Flush (any 5 same suit):** 4 × C(13,5) = 5,148 hands; excluding the 40 straight flushes gives 5,108 "flush" hands = 0.1965% (0.198% if you include them).
- **Full house:** choose the triple rank (13), 3 of its 4 suits (C(4,3)), the pair rank (12), 2 of 4 suits (C(4,2)): 13·4·12·6 = 3,744, so 0.144%.
- **At least one ace:** complement = no aces = C(48,5)/C(52,5) = 1,712,304/2,598,960 = 0.659, so 1 − 0.659 = 0.341.
- Method: count favourable hands over total, pick the structure (ranks and suits) separately, and use complements for "at least one".

**Example:** Full house is about 1 in 694 hands; a flush is about 1 in 509.

**Code:**
```python
from math import comb
tot = comb(52, 5)
print("flush (excl. straight flush):", round((4 * comb(13, 5) - 40) / tot, 6))
print("full house:", round(13 * comb(4, 3) * 12 * comb(4, 2) / tot, 6))
print("at least one ace:", round(1 - comb(48, 5) / tot, 4))
# flush (excl. straight flush): 0.001965
# full house: 0.001441
# at least one ace: 0.3412
```

**Follow-ups:**
- *Why does a full house outrank a flush?* It is rarer (0.144% vs 0.197%); poker ranks hands by rarity.
- *P(exactly one ace)?* 4·C(48,4)/C(52,5) ≈ 0.299.

**Common mistakes:** Counting ordered hands; forgetting to remove straight flushes; double counting in full house by picking the ranks in the wrong order (the roles triple and pair are distinct, so no division by 2).

### Q48 ⭐ 🟡 St. Petersburg paradox and Kelly criterion: why is expected value not enough for decisions? How do you size a bet with positive edge?
**Asked at:** Likely (expert gap-check): Quant firms, risk-flavoured DS roles
**Say this first (1 line):** Expected value ignores risk and ruin; the St. Petersburg game has infinite expected payoff yet nobody pays much, and Kelly says bet the fraction f* = p − q/b of your bankroll to maximise long-run growth.

**Then explain:**
- **St. Petersburg:** flip until the first tail; payoff 2^k if the first tail is on flip k. EV = Σ (½)^k·2^k = ∞, but a typical outcome is tiny. Resolution: people maximise expected utility (log wealth), or the bank has finite money. With log utility the game is worth only a few units.
- **Kelly criterion:** maximise the expected log growth E[log(wealth)]. For a bet paying b-to-1 with win probability p and q = 1 − p: f* = p − q/b = (bp − q)/b. For even-money bets f* = 2p − 1.
- Betting more than Kelly increases risk without more growth and eventually loses; twice Kelly gives zero growth. Many practitioners use half-Kelly to cope with estimation error.
- Never bet when the edge is negative; EV > 0 does not mean you should bet everything (gambler's ruin, Q26).

**Example:** A coin wins even money with p = 0.55: f* = 0.10, so bet 10% of the bankroll each time. The log-growth per bet is 0.0050 at 10% and −0.089 (shrinking wealth) at 50%.

**Code:**
```python
import numpy as np
p = 0.55
f = np.linspace(0, 0.99, 1000)
g = p * np.log(1 + f) + (1 - p) * np.log(1 - f)       # expected log growth per bet
print("best f:", f[g.argmax()].round(3), " kelly 2p-1:", round(2 * p - 1, 2))
growth = lambda f: p * np.log(1 + f) + (1 - p) * np.log(1 - f)
print("growth at kelly: %.4f   at f=0.5: %.4f" % (growth(0.1), growth(0.5)))
# best f: 0.1  kelly 2p-1: 0.1
# growth at kelly: 0.0050   at f=0.5: -0.0889
```

**Follow-ups:**
- *What is the risk of ruin under Kelly?* Never exactly zero wealth (you bet a fraction), but drawdowns can be deep.
- *Why half-Kelly?* If p is estimated with error, overestimating the edge pushes you past the optimum, which costs more than undershooting.

**Common mistakes:** Maximising EV alone; treating Kelly as risk-free; using it with an estimated edge as if it were known.

### Q49 ⭐ 🟡 Thompson sampling for a Bernoulli bandit: explain it using Beta posteriors and simulate it against epsilon-greedy.
**Asked at:** Likely (expert gap-check): Recsys/ads teams at Flipkart, Zalando, Spotify
**Say this first (1 line):** Thompson sampling keeps a Beta posterior for each arm's conversion rate, draws one sample per arm each round, and plays the arm with the highest draw; it explores in proportion to how likely an arm is to be best.

**Then explain:**
- Start each arm with Beta(1,1). After a success on arm k add 1 to its a, after a failure add 1 to its b.
- Each round: sample θ_k ~ Beta(a_k, b_k) for all arms, pull argmax. Uncertain arms sometimes win the draw (exploration); clearly bad arms are rarely picked as their posterior tightens (exploitation).
- Epsilon-greedy explores a fixed share (e.g. 10%) forever, wasting traffic on bad arms; Thompson's exploration decays automatically.
- Regret (lost conversions vs always playing the best arm) of Thompson sampling grows logarithmically in T, while fixed-ε grows linearly.
- Practical: handles delayed feedback badly unless batched; non-stationary rates need discounting or sliding windows.

**Example:** Three arms with CTR 4%, 5%, 6%, 5,000 rounds, 20 seeds. Average regret: Thompson 20.5 conversions, epsilon-greedy (ε = 0.1) 29.2.

**Code:**
```python
import numpy as np
def run(alg, T=5000, seed=0):
    r = np.random.default_rng(seed); p = np.array([0.04, 0.05, 0.06])
    a = np.ones(3); b = np.ones(3); n = np.zeros(3); s = np.zeros(3); reg = 0
    for _ in range(T):
        if alg == "ts": k = np.argmax(r.beta(a, b))
        else: k = r.integers(3) if r.random() < 0.1 or n.min() == 0 else np.argmax(s / n)
        x = r.random() < p[k]
        a[k] += x; b[k] += 1 - x; n[k] += 1; s[k] += x; reg += p.max() - p[k]
    return reg
print("TS regret:", np.mean([run("ts", seed=i) for i in range(20)]).round(1))
print("eps-greedy regret:", np.mean([run("eg", seed=i) for i in range(20)]).round(1))
# TS regret: 20.5
# eps-greedy regret: 29.2
```

**Follow-ups:**
- *How would you do it with non-binary rewards?* Use a conjugate model for the reward (Gaussian, Gamma) or a sampling-based posterior.
- *Why not just A/B test?* A bandit maximises reward while learning, but gives noisier inference on the effect size.

**Common mistakes:** Choosing the arm with the highest posterior mean (that is greedy); not resetting the prior when the world changes; using a bandit when you need an unbiased effect estimate.

### Q50 ⭐ 🟡 Winsorizing, capping and trimming outliers: how do they reduce variance and what bias do they introduce?
**Asked at:** Likely (expert gap-check): Booking, Zalando, Spotify experimentation
**Say this first (1 line):** Winsorizing clips extreme values to a percentile, capping sets a fixed ceiling, and trimming drops them; all three cut variance a lot for heavy-tailed metrics but introduce a downward bias in the mean.

**Then explain:**
- **Winsorizing:** replace values above the p-th percentile (and/or below the (100−p)th) with that percentile. Keeps all rows.
- **Capping:** fixed business threshold (e.g. cap order value at Rs 50,000). Same effect, but the cutoff does not depend on the data (better for experiments since it is the same in both arms and can be pre-registered).
- **Trimming:** delete the extreme rows; changes the sample and is usually worse for A/B tests.
- **Variance:** one huge value (a whale) dominates the variance; clipping bounds its influence, so confidence intervals narrow and tests have more power.
- **Bias:** the clipped mean is lower than the true mean for right-skewed data. The bias is small for the difference between arms if both arms are clipped the same way, but the estimand is now "capped revenue", not revenue.
- Use when revenue is heavy-tailed and the treatment is not expected to change the tail; avoid when the whales are the point.

**Example:** Lognormal(1,1) data, n = 500, true mean 4.48, 3,000 simulations: raw mean bias 0.00, SD 0.265; 99th percentile winsorized bias −0.13, SD 0.244; 5% trimmed bias −0.81, SD 0.183. The trimmed estimator has the lowest variance but the most bias.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
true = np.exp(1 + 0.5)
est = {"raw": [], "winsor99": [], "trim5": []}
for _ in range(3000):
    y = rng.lognormal(1, 1, 500)
    est["raw"].append(y.mean())
    est["winsor99"].append(np.clip(y, None, np.percentile(y, 99)).mean())
    est["trim5"].append(stats.trim_mean(y, 0.05))
for k, v in est.items():
    v = np.array(v); print(k, "bias %.2f  sd %.3f" % (v.mean() - true, v.std()))
# raw bias 0.00 sd 0.265 / winsor99 bias -0.13 sd 0.244 / trim5 bias -0.81 sd 0.183
```

**Follow-ups:**
- *Which percentile?* Choose from the pre-experiment distribution, sweeping 99, 99.5, 99.9 and checking power vs bias.
- *Alternative?* Log transform, or model the purchase and the amount separately (hurdle model).

**Common mistakes:** Choosing the cap after seeing which arm wins; capping each arm at its own percentile (different thresholds); reporting capped revenue as total revenue.

### Q51 ⭐ 🟡 Hat matrix and leverage: derive H = X(X'X)^-1 X', explain h_ii, and relate leverage to Cook's distance.
**Asked at:** Likely (expert gap-check): Stats-heavy DS roles, research scientist loops
**Say this first (1 line):** The hat matrix H = X(XᵀX)⁻¹Xᵀ turns y into fitted values (ŷ = Hy), its diagonal h_ii is the leverage of point i, and Cook's distance combines leverage with the size of the residual.

**Then explain:**
- **Derivation:** minimising ‖y − Xβ‖² gives the normal equations XᵀXβ̂ = Xᵀy, so β̂ = (XᵀX)⁻¹Xᵀy and ŷ = Xβ̂ = X(XᵀX)⁻¹Xᵀy = Hy.
- H is symmetric and idempotent (H² = H), it projects y onto the column space of X.
- **Leverage h_ii:** how much y_i influences its own fitted value (ŷ_i = Σ h_ij y_j). 1/n ≤ h_ii ≤ 1, Σ h_ii = trace(H) = p (number of parameters), so the average is p/n. Flag h_ii > 2p/n or 3p/n.
- Leverage depends only on X (how far x_i is from the other x's), not on y.
- **Cook's distance:** D_i = e_i²/(p·s²) · h_ii/(1 − h_ii)². High leverage and a large residual together make a point influential; high leverage alone with a small residual is not.
- Residual variance: Var(e_i) = σ²(1 − h_ii), so high-leverage points have small raw residuals (they pull the line towards themselves); use studentised residuals.

**Example:** n = 50, p = 3, one point placed at x = (6, 6) far from the rest has h = 0.57 while the average is 0.06; trace(H) = 3.000. My manual Cook's formula matches statsmodels exactly.

**Code:**
```python
import numpy as np, statsmodels.api as sm
rng = np.random.default_rng(0)
n = 50; X = sm.add_constant(rng.normal(size=(n, 2))); X[0, 1:] = [6, 6]
y = X @ [1, 1, 1] + rng.normal(size=n)
H = X @ np.linalg.inv(X.T @ X) @ X.T; h = np.diag(H)
print("trace:", h.sum().round(3), " h0:", h[0].round(3), " mean h:", h.mean())
res = sm.OLS(y, X).fit(); e = res.resid; s2 = e @ e / (n - 3)
D = e**2 / (3 * s2) * h / (1 - h)**2
print("Cook matches statsmodels:", np.allclose(D, res.get_influence().cooks_distance[0]))
# trace: 3.0  h0: 0.571  mean h: 0.06
# Cook matches statsmodels: True
```

**Follow-ups:**
- *Why is Σh_ii = p?* trace(H) = trace((XᵀX)⁻¹XᵀX) = trace(I_p) = p.
- *What do you do with high-leverage points?* Check data errors first; if real, report with and without them or use robust regression.

**Common mistakes:** Confusing leverage (unusual x) with outlier (unusual y); deleting influential points because they hurt the fit; forgetting leverage is independent of y.

### Q52 ⭐ 🟡 Frisch-Waugh-Lovell theorem: explain it and use it to interpret a coefficient in multiple regression and to see why CUPED is regression adjustment.
**Asked at:** Likely (expert gap-check): Senior DS/economist loops
**Say this first (1 line):** Frisch-Waugh-Lovell says the coefficient on x in a multiple regression equals the slope you get after removing the effect of all other regressors from both x and y, so a coefficient means "the effect of x holding the others fixed".

**Then explain:**
- To get β_x in y ~ x + Z: (1) regress x on Z and keep the residuals x̃; (2) regress y on Z and keep the residuals ỹ; (3) regress ỹ on x̃. The slope equals the full-model β_x exactly (and so do the residuals).
- That is why a coefficient is a "partial" effect: it uses only the part of x that Z cannot explain. If x is almost explained by Z, x̃ has little variance and the SE is huge (multicollinearity, Q35).
- Regressing y on x alone without Z gives a different slope (omitted-variable bias) unless x and Z are uncorrelated.
- **CUPED link:** in an experiment, y ~ treatment + pre-period X. By FWL, the treatment effect equals the slope of (y with X removed) on (treatment with X removed). Because randomization makes treatment independent of X, removing X from y just cuts noise and does not change the estimate: that is CUPED = regression adjustment.

**Example:** Let y = 2x + 3z + noise with z correlated with x. Full-model β_x = 2.0443; FWL gives the identical 2.0443.

**Code:**
```python
import numpy as np, statsmodels.api as sm
rng = np.random.default_rng(0)
n = 500
x = rng.normal(size=n); z = 0.7 * x + rng.normal(size=n)
y = 2 * x + 3 * z + rng.normal(size=n)
full = sm.OLS(y, sm.add_constant(np.c_[x, z])).fit().params
ex = sm.OLS(x, sm.add_constant(z)).fit().resid        # x with z removed
ey = sm.OLS(y, sm.add_constant(z)).fit().resid        # y with z removed
print("full-model b_x:", full[1].round(4), " FWL b_x:", (ex @ ey / (ex @ ex)).round(4))
# full-model b_x: 2.0443  FWL b_x: 2.0443
```

**Follow-ups:**
- *Do you need to residualise y too?* No: regressing the raw y on x̃ gives the same slope, because x̃ is orthogonal to Z. Residualising y just makes the second-stage fit cleaner.
- *Use in practice?* Fixed effects (demean within groups), detrending, and partialling out confounders.

**Common mistakes:** Thinking the coefficient is the simple correlation of x with y; forgetting the SE from a manual two-step is slightly off (wrong degrees of freedom); controlling for post-treatment variables.

### Q53 ⭐ 🔴 Distribution of the k-th order statistic of n Uniform(0,1) samples: derive it (Beta) and use it to get the expected median and expected range.
**Asked at:** Typical (prep sources): Quant firms, stat theory rounds
**Say this first (1 line):** The k-th smallest of n Uniform(0,1) draws follows a Beta(k, n − k + 1) distribution, so the mean is k/(n + 1): the expected median of an odd sample is 1/2 and the expected range is (n − 1)/(n + 1).

**Then explain:**
- **Derivation:** the k-th order statistic X_(k) is ≤ x when at least k of the n points fall below x. Its density at x: choose which point is the k-th (n ways), choose k − 1 of the other n − 1 to lie below (C(n−1,k−1)), then x^(k−1)·(1−x)^(n−k): f(x) = n!/((k−1)!(n−k)!) x^(k−1)(1−x)^(n−k), which is Beta(k, n−k+1).
- Mean of Beta(a, b) is a/(a + b), so E[X_(k)] = k/(n + 1).
- **Median** (n = 2m + 1, k = m + 1): E = (m+1)/(2m+2) = 1/2.
- **Range** X_(n) − X_(1): E = n/(n+1) − 1/(n+1) = (n − 1)/(n + 1). The n points split [0,1] into n + 1 gaps of equal expected size 1/(n+1).
- Variance of X_(k) = k(n − k + 1)/((n+1)²(n+2)).

**Example:** n = 9: expected median 0.5, expected range 0.8, variance of the 3rd smallest = 3·7/(10²·11) = 0.01909. Simulation of 10⁶ samples: 0.4999, 0.8001, 0.01909.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
n = 9
x = np.sort(rng.random((1_000_000, n)), axis=1)
print("median mean:", x[:, 4].mean().round(4), "theory", 0.5)
print("range mean :", (x[:, -1] - x[:, 0]).mean().round(4), "theory", (n - 1) / (n + 1))
print("var of 3rd :", x[:, 2].var().round(5), "theory", round(3 * 7 / (10**2 * 11), 5))
# median mean: 0.4999 theory 0.5
# range mean : 0.8001 theory 0.8
# var of 3rd : 0.01909 theory 0.01909
```

**Follow-ups:**
- *Max of n uniforms?* Beta(n, 1), mean n/(n+1), as in Q24.
- *Non-uniform data?* Apply the probability integral transform: F(X_(k)) is the uniform order statistic.

**Common mistakes:** Using n instead of n + 1 in the denominator; forgetting the Beta parameters are (k, n − k + 1); assuming the median of a sample has the same distribution as the population median.

### Q54 ⭐ 🔴 Expected maximum of n i.i.d. Exponential(1) variables, and why it grows like log n.
**Asked at:** Typical (prep sources): Optiver (expected maxima), quant stat rounds
**Say this first (1 line):** The expected maximum of n i.i.d. Exp(1) variables is the harmonic number H_n = 1 + 1/2 + … + 1/n ≈ ln n + 0.577, so it grows like log n.

**Then explain:**
- Use the memoryless property: n clocks run at once; the first rings after Exp(n) time (mean 1/n). Then n − 1 clocks remain, and by memorylessness each is fresh Exp(1); the next ring comes after Exp(n − 1), mean 1/(n−1), and so on.
- So max = sum of independent Exp(n) + Exp(n−1) + … + Exp(1), and E[max] = 1/n + 1/(n−1) + … + 1 = H_n.
- H_n ≈ ln n + γ (γ ≈ 0.5772, Euler's constant), so the maximum grows only logarithmically: doubling n adds just ln 2 ≈ 0.69.
- Why it matters: the largest latency among n requests, the worst of n servers, or extreme-value limits (Gumbel) all grow slowly with n.
- Variance of the max is Σ 1/k², which converges to π²/6, so it does not grow.

**Example:** n = 1000 requests with mean latency 1 s: the slowest takes about 7.5 s on average, not 1,000 s.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
for n in (10, 100, 1000):
    m = rng.exponential(size=(20000, n)).max(1)
    H = sum(1 / k for k in range(1, n + 1))
    print(n, "sim", m.mean().round(3), " H_n", round(H, 3), " ln n + 0.577", round(np.log(n) + 0.5772, 3))
# 10   sim 2.933  H_n 2.929  ln n + 0.577 2.88
# 100  sim 5.193  H_n 5.187  ln n + 0.577 5.182
# 1000 sim 7.481  H_n 7.485  ln n + 0.577 7.485
```

**Follow-ups:**
- *Distribution of the max?* P(max ≤ x) = (1 − e^(−x))^n; max − ln n converges to a Gumbel.
- *And for heavy tails (Pareto)?* The max grows polynomially in n, not logarithmically.

**Common mistakes:** Assuming the max is n times the mean; forgetting memorylessness is what makes the spacings independent; mixing up the harmonic sum with ln n exactly (there is a +γ).

### Q55 ⭐ 🔴 Secretary problem: what is the optimal stopping rule and why 1/e?
**Asked at:** Typical (prep sources): Quant puzzle sets, Jane Street style
**Say this first (1 line):** Skip the first n/e candidates, then pick the first one better than everyone seen so far; this wins with probability about 1/e ≈ 37%.

**Then explain:**
- Setup: n candidates arrive in random order, you see their rank only relative to those seen before, you must accept or reject immediately, and you want the single best.
- Strategy: reject the first r, then accept the first candidate who beats all of the first r.
- If the best is at position i > r, you win exactly when the best of the first i − 1 sits within the first r (probability r/(i−1)). P(win) = Σ_{i=r+1}^{n} (1/n)·r/(i−1) ≈ (r/n)·ln(n/r).
- With x = r/n maximise −x ln x: derivative −ln x − 1 = 0 gives x = 1/e, with value 1/e. So the cutoff is n/e and the win probability tends to 1/e.
- Intuition: the first part builds a benchmark, and skipping too few makes the benchmark weak, while skipping too many risks skipping the best.

**Example:** n = 100: skip about 37. Simulation (20,000 trials each): skip 10 → 23.8%, skip 25 → 34.8%, skip 37 → 36.8%, skip 50 → 34.6%.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
def win_rate(n, r, T=20000):
    wins = 0
    for _ in range(T):
        p = rng.permutation(n)                       # 0 is the best candidate
        best = p[:r].min() if r else n
        pick = next((i for i in range(r, n) if p[i] < best), n - 1)
        wins += p[pick] == 0
    return wins / T
for r in (10, 25, 37, 50):
    print("skip", r, "win prob", win_rate(100, r))
print("1/e =", round(1 / np.e, 3))
# skip 10: 0.2375, skip 25: 0.3476, skip 37: 0.3678, skip 50: 0.3459, 1/e = 0.368
```

**Follow-ups:**
- *What if n is unknown?* The rule needs n or a time horizon; skip the first 37% of the available time window instead.
- *Real uses?* Hiring, house hunting, ad-slot selection; assumes no recall and unknown distribution.

**Common mistakes:** Saying 37% is the chance of hiring a good candidate (it is the best only); forgetting the rule is "better than all seen so far", not "better than the average"; ignoring that the answer is asymptotic.

### Q56 ⭐ 🔴 Absorbing Markov chains: use the fundamental matrix to find expected time to absorption and absorption probabilities.
**Asked at:** Typical (prep sources): Quant firms, OR-flavoured DS roles
**Say this first (1 line):** For an absorbing Markov chain with transient-to-transient matrix Q and transient-to-absorbing matrix R, the fundamental matrix N = (I − Q)⁻¹ gives expected visits, N·1 gives expected time to absorption, and B = N·R gives the absorption probabilities.

**Then explain:**
- Order states as transient first, absorbing last: P = [[Q, R], [0, I]].
- N_ij = expected number of visits to transient state j starting from i (because N = I + Q + Q² + …, the sum of n-step visit probabilities).
- Expected steps to absorption from i = row sum of N (t = N·1).
- Absorption probability into absorbing state a from i: B = N·R.
- Needs at least one absorbing state reachable from every transient state, so Q^n → 0 and I − Q is invertible.
- Typical uses: gambler's ruin (Q26), customer lifetime until churn (Q29), page-visit funnels.

**Example:** Gambler's ruin on {0,...,4} with a fair coin, transient states 1, 2, 3. N·1 = (3, 4, 3): from 2 the expected duration is 4 = i(N − i). B = [[0.75, 0.25], [0.5, 0.5], [0.25, 0.75]]: win probability from i is i/N.

**Code:**
```python
import numpy as np
# Gambler's ruin on {0,..,4}, fair coin; transient states 1,2,3; absorbing 0 and 4
Q = np.array([[0, .5, 0], [.5, 0, .5], [0, .5, 0]])
R = np.array([[.5, 0], [0, 0], [0, .5]])             # columns: ruin(0), win(4)
N = np.linalg.inv(np.eye(3) - Q)                      # fundamental matrix
print("expected steps:", N @ np.ones(3))
print("absorption probs (ruin, win):\n", N @ R)
# expected steps: [3. 4. 3.]
# absorption probs (ruin, win): [[0.75 0.25] [0.5 0.5] [0.25 0.75]]
```

**Follow-ups:**
- *Variance of time to absorption?* (2N − I)t − t∘t.
- *Why invertible?* Because Q^n → 0, the series I + Q + Q² + … converges to (I − Q)⁻¹.

**Common mistakes:** Mixing up the state order (Q must be the transient block); using N for probabilities instead of expected visits; inverting a singular I − Q when some transient state cannot reach absorption.

### Q57 ⭐ 🔴 Always-valid inference: explain mSPRT / confidence sequences and how they differ from group sequential designs.
**Asked at:** Likely (expert gap-check): Spotify, Netflix, experimentation-platform teams
**Say this first (1 line):** Always-valid inference gives p-values or confidence intervals that stay valid at every sample size, so you can peek continuously and stop whenever you like; group sequential designs only protect a fixed, pre-planned set of looks.

**Then explain:**
- **mSPRT (mixture sequential probability ratio test):** average the likelihood ratio over a prior on the effect (a Gaussian mixture), giving a statistic Λ_n. Under H0, Λ_n is a nonnegative martingale with mean 1, so by Ville's inequality P(Λ_n ≥ 1/α for some n) ≤ α. Reject the first time Λ_n ≥ 1/α. The always-valid p-value is p_n = min over t ≤ n of 1/Λ_t.
- **Confidence sequences:** intervals that cover the true effect at all times simultaneously with probability ≥ 1 − α (a time-uniform guarantee); they are wider than a fixed-n interval and shrink slightly slower than 1/√n (roughly √(log n / n) for mixture boundaries).
- **Versus group sequential:** group sequential needs a maximum sample size, a fixed look schedule and alpha spending (Q34), and is more powerful at the planned looks. mSPRT needs none of that, works for any stopping rule, and costs some power; its result is not tied to one planned sample size.
- Sequential testing in commercial platforms is built on this idea (the Optimizely approach follows Johari et al.); τ² is usually tuned to the effect size you expect.

**Example:** Normal data with known variance, τ² = 1, α = 0.05, 2,000 observations, 2,000 simulated tests: peeking at z > 1.96 at every step rejects a true null 56% of the time; mSPRT 3% (≤ 5%); with a true effect of 0.1 SD mSPRT detects it 85% of the time within the window.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
T, reps, tau2, alpha = 2000, 2000, 1.0, 0.05
n = np.arange(1, T + 1)
def msprt_reject(delta):
    d = rng.normal(delta, 1, (reps, T))               # per-unit difference, known variance 1
    ybar = d.cumsum(1) / n
    lam = np.sqrt(1 / (1 + n * tau2)) * np.exp(n**2 * tau2 * ybar**2 / (2 * (1 + n * tau2)))
    return (lam >= 1 / alpha).any(1).mean()           # ever crossed 1/alpha
z = rng.normal(size=(reps, T)).cumsum(1) / np.sqrt(n)
print("peeking every step, z>1.96 :", (np.abs(z) > 1.96).any(1).mean())
print("mSPRT under null           :", msprt_reject(0.0))
print("mSPRT power at delta=0.1   :", msprt_reject(0.1))
# peeking every step, z>1.96 : 0.5605
# mSPRT under null           : 0.0295
# mSPRT power at delta=0.1   : 0.8535
```

**Follow-ups:**
- *What is the price?* A somewhat larger sample for the same power than a fixed-horizon test.
- *Is it Bayesian?* The mixture looks like a prior, but the guarantee is frequentist.

**Common mistakes:** Saying "always valid" means no cost; choosing τ² far from the true effect size (hurts power); applying it to a metric with unknown variance without a proper variance estimator.

### Q58 ⭐ 🔴 Control variates and importance sampling in Monte Carlo: how do you estimate a rare-event probability with low variance? Show code.
**Asked at:** Typical (prep sources): Quant roles, simulation-heavy DS
**Say this first (1 line):** For rare events, sample from a proposal that makes the event common and reweight each draw by the density ratio (importance sampling); control variates reduce variance by subtracting a correlated quantity with a known mean.

**Then explain:**
- Naive Monte Carlo for a probability p ≈ 3e-6 needs on the order of 100/p draws (about 3×10⁷) for a 10% relative error, and with far fewer draws the estimate is usually exactly 0.
- **Importance sampling:** estimate E_p[h(X)] = E_q[h(X)·p(X)/q(X)]. Choose q to put mass where h·p is large, here a normal shifted to the threshold. The weights p/q correct the bias; variance is small if q is close to |h|·p.
- **Control variate:** to estimate E[f], find g with known mean μ_g and use f − c(g − μ_g) with c = Cov(f, g)/Var(g); the variance falls by a factor of 1 − ρ².
- Risks: if q has lighter tails than p×h, weights explode (infinite variance); check the effective sample size.

**Example:** P(Z > 4.5) = 3.40e-6. Naive MC with 100,000 draws gave 1e-5 (a single hit, 3× too high; often it returns 0); importance sampling with N(4.5, 1) gave 3.41e-6 with a standard error of 2.4e-8. Control variate for E[e^U], U ~ U(0,1), with g = U: variance falls to 1.6% of the original.

**Code:**
```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
N, t = 100_000, 4.5
print("exact P(Z>4.5):", stats.norm.sf(t))
print("naive MC      :", (rng.normal(size=N) > t).mean())
y = rng.normal(t, 1, N)                               # sample from the shifted proposal
w = np.exp(-t * y + t**2 / 2) * (y > t)               # weight = target density / proposal density
print("importance    :", w.mean(), " std err", w.std() / np.sqrt(N))
u = rng.random(N); f = np.exp(u)                      # control variate: estimate E[e^U], U~U(0,1); E[U]=0.5
c = np.cov(f, u)[0, 1] / u.var()
cv = f - c * (u - 0.5)
print("control variate: var ratio", (cv.var() / f.var()).round(4), " mean", cv.mean().round(4), " true", round(np.e - 1, 4))
# exact 3.3977e-06 | naive 1e-05 | importance 3.415e-06 (se 2.43e-08) | CV var ratio 0.0163, mean 1.7184, true 1.7183
```

**Follow-ups:**
- *Self-normalised importance sampling?* Divide by the sum of weights when p is known up to a constant; slightly biased, often lower variance.
- *Where is this used?* Tail risk (VaR), reliability, off-policy evaluation in bandits/RL.

**Common mistakes:** Forgetting the weights; using a proposal with thinner tails than the target; trusting the estimate without checking the weight spread or effective sample size.

### Q59 ⭐ 🔴 Write a Metropolis-Hastings sampler from scratch in NumPy to sample a posterior. How do you diagnose convergence (trace, R-hat, ESS)?
**Asked at:** Likely (expert gap-check): Bayesian-heavy DS and research roles
**Say this first (1 line):** Metropolis-Hastings proposes a random move, accepts it with probability min(1, posterior ratio), and the chain of accepted points converges to the posterior; you check convergence with trace plots, R-hat across chains, and effective sample size.

**Then explain:**
- **Algorithm:** from θ, propose θ' = θ + step·noise; compute log ratio = log p(θ'|data) − log p(θ|data) (the normalising constant cancels); accept if log u < ratio. Work in log space to avoid underflow.
- **Tuning:** step too small means slow, random-walk exploration; too large means most proposals are rejected. Aim for roughly 20-40% acceptance (about 23% optimal in high dimensions, around 44% in 1-d).
- **Burn-in:** discard the early draws before the chain reaches the typical set.
- **Diagnostics:** (1) trace plots of several chains from different starting points should overlap like a "hairy caterpillar"; (2) R-hat compares between-chain to within-chain variance, and should be below about 1.01; (3) effective sample size (ESS) = n / (1 + 2Σρ_k) accounts for autocorrelation, since 5,000 correlated draws are worth far fewer independent ones.
- Also check the posterior against known cases (here the conjugate normal answer).

**Example:** Normal mean with known σ = 1, prior N(0,10²), 30 observations, 4 chains from −5, 0, 5, 10. R-hat = 1.0002; posterior mean 1.875 (exact 1.878), SD 0.182 (exact 0.183); ESS of one chain ≈ 1,275 of 5,000 draws.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
data = rng.normal(2, 1, 30)                          # known sd = 1; prior mu ~ N(0, 10^2)
logp = lambda m: -0.5 * np.sum((data - m)**2) - 0.5 * m**2 / 100
def mh(start, n=6000, step=0.5, seed=0):
    r = np.random.default_rng(seed); m, lp = start, logp(start); out = np.empty(n)
    for i in range(n):
        c = m + step * r.normal(); lc = logp(c)
        if np.log(r.random()) < lc - lp: m, lp = c, lc   # accept with prob min(1, ratio)
        out[i] = m
    return out
ch = np.array([mh(s, seed=i)[1000:] for i, s in enumerate([-5, 0, 5, 10])])  # 4 chains, drop burn-in
n = ch.shape[1]
W = ch.var(1, ddof=1).mean(); B = n * ch.mean(1).var(ddof=1)
rhat = np.sqrt(((n - 1) / n * W + B / n) / W)
print("R-hat:", rhat.round(4))
print("post mean %.3f (exact %.3f)  sd %.3f (exact %.3f)" % (ch.mean(), data.sum() / (30 + .01), ch.std(), 1 / np.sqrt(30.01)))
from statsmodels.tsa.stattools import acf
rho = acf(ch[0], nlags=200)[1:]
tau = 1 + 2 * rho[:np.argmax(rho < 0.05)].sum()
print("ESS (one chain): %.0f of %d" % (n / tau, n))
# R-hat: 1.0002 | post mean 1.875 (exact 1.878) sd 0.182 (exact 0.183) | ESS (one chain): 1275 of 5000
```

**Follow-ups:**
- *Why not just use PyMC/Stan?* In practice I would (NUTS is much more efficient); writing MH shows I understand it.
- *What if the chains disagree?* Reparametrise, run longer, check multimodality or a bad model.

**Common mistakes:** Judging convergence from a single chain; forgetting burn-in; reporting 5,000 draws as 5,000 independent samples; computing the ratio on the probability scale (underflow).

### Q60 ⭐ 🔴 Hierarchical Bayesian model / partial pooling: when do you use it, for example for store- or city-level conversion rates?
**Asked at:** Likely (expert gap-check): Swiggy, Zalando, Booking, senior roles
**Say this first (1 line):** Partial pooling models each group's rate as drawn from a shared population distribution, so small groups borrow strength from the rest while large groups stay near their own data; it sits between "one rate for all" and "separate rates per group".

**Then explain:**
- **No pooling:** each store estimated alone; unbiased but noisy for small stores.
- **Full pooling:** one rate for all; stable but ignores real differences.
- **Partial pooling:** θ_j ~ Beta(a, b) (or logit θ_j ~ N(μ, τ²)), with data k_j ~ Binomial(n_j, θ_j). The estimate for store j is a weighted average of its own rate and the global mean, with weight w_j = τ²/(τ² + σ_j²): small n_j means a small weight on own data.
- τ is learned from the data: if stores are very different, τ is large and there is little shrinkage; if they are similar, shrinkage is strong. Fit with empirical Bayes (Q41) or fully Bayesian (PyMC/Stan).
- Use for: many groups with uneven sample sizes (stores, cities, doctors, schools), small-n subgroups in A/B tests, multi-level or random-effects models, and when you want sensible estimates for groups with almost no data.

**Example:** 30 stores with 20-400 visits each and true conversion varying around 12%. MSE vs truth: no pooling 0.00085, full pooling 0.00159, partial pooling 0.00062. The weight on own data ranged from 0.19 (smallest store) to 0.88 (largest).

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
J = 30
n = rng.integers(20, 400, J); p = rng.beta(6, 44, J); k = rng.binomial(n, p)   # 30 stores
raw = k / n; pool = k.sum() / n.sum()
s2 = raw * (1 - raw) / n
mu = raw.mean(); tau2 = max(raw.var(ddof=1) - s2.mean(), 1e-6)                 # between-store variance
w = tau2 / (tau2 + s2); partial = w * raw + (1 - w) * mu                       # normal-normal shrinkage
mse = lambda e: ((e - p)**2).mean()
print("MSE  no pooling %.5f  full pooling %.5f  partial %.5f" % (mse(raw), mse(pool), mse(partial)))
print("shrink weight on own data: min %.2f max %.2f" % (w.min(), w.max()))
# MSE  no pooling 0.00085  full pooling 0.00159  partial 0.00062
# shrink weight on own data: min 0.19 max 0.88
```

**Follow-ups:**
- *Why is a biased estimator better?* It trades a little bias for a large drop in variance (Stein's paradox).
- *How do you add covariates?* Put them in the mean: logit θ_j = Xβ + u_j.

**Common mistakes:** Fixed effects per store with tiny samples (no pooling); pooling when groups are truly different; ignoring that τ is itself uncertain.

### Q61 ⭐ 🔴 Delta method for ratio metrics (e.g. revenue per session) and its variance; how do you combine it with CUPED?
**Asked at:** Likely (expert gap-check): Spotify, Booking, Microsoft ExP
**Say this first (1 line):** A ratio metric like revenue per session is a ratio of two averages over users, so you can't treat per-user ratios as independent; the delta method gives its variance from the variances and covariance of numerator and denominator, and CUPED is applied to each part (or to the linearised ratio).

**Then explain:**
- Let X = revenue per user, Y = sessions per user, R = mean(X)/mean(Y). The randomisation unit is the user, so users are the independent observations.
- **Delta method** (first-order Taylor expansion of R):
  Var(R) ≈ (1/n)·[Var(X)/μ_Y² − 2μ_X·Cov(X,Y)/μ_Y³ + μ_X²·Var(Y)/μ_Y⁴].
- Equivalent trick: linearise per user, ℓ_i = (X_i − R·Y_i)/μ_Y; then Var(R) ≈ Var(ℓ)/n, and you can run ordinary t-tests or CUPED on ℓ.
- **With CUPED:** adjust X and Y with their pre-period values (or adjust the linearised ℓ with a pre-period linearised ℓ). The delta method then uses the adjusted variances and covariance.
- **Wrong approach:** averaging per-user ratios X_i/Y_i (weights light users equally and answers a different question) or treating sessions as independent when they are clustered within users (SE too small).

**Example:** 5,000 users; revenue per session = 2.95. Delta-method SE 0.0653; bootstrap SE 0.0652 (agree); the naive per-user-ratio SE 0.0602 is both a different estimand and mis-sized.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
n = 5000
s = rng.poisson(3, n) + 1                              # sessions per user (denominator)
rev = rng.gamma(2, 10, n) * s * 0.3 * (rng.random(n) < 0.5)   # revenue per user (numerator)
xb, yb = rev.mean(), s.mean(); R = xb / yb
cxy = np.cov(rev, s)[0, 1]
var = (rev.var(ddof=1) / yb**2 - 2 * xb * cxy / yb**3 + xb**2 * s.var(ddof=1) / yb**4) / n
bs = [rev[i].sum() / s[i].sum() for i in (rng.integers(0, n, n) for _ in range(2000))]
print("revenue per session:", R.round(3))
print("delta-method SE:", np.sqrt(var).round(4), "  bootstrap SE:", np.std(bs).round(4))
print("wrong (per-user ratio, then t-test) SE:", np.sqrt(np.var(rev / s, ddof=1) / n).round(4))
# revenue per session: 2.95
# delta-method SE: 0.0653   bootstrap SE: 0.0652
# wrong (per-user ratio, then t-test) SE: 0.0602
```

**Follow-ups:**
- *Why not bootstrap everything?* You can (resample users), but the delta method is fast and closed-form for large experiments.
- *Difference between arms?* Var(R_B − R_A) = Var(R_A) + Var(R_B) for independent arms.

**Common mistakes:** Treating sessions or rows as independent when randomisation is by user; ignoring the covariance term; averaging ratios instead of taking a ratio of means.

### Q62 ⭐ 🔴 Heteroscedasticity-consistent standard errors (HC0-HC3) and cluster-robust SEs: when and why?
**Asked at:** Likely (expert gap-check): Economist-style DS roles, Europe
**Say this first (1 line):** HC0-HC3 give standard errors that stay valid when the error variance is not constant, and cluster-robust SEs stay valid when errors are correlated within groups; coefficients are unchanged, only the standard errors are fixed.

**Then explain:**
- OLS coefficients stay unbiased under heteroscedasticity, but the usual SE formula σ²(XᵀX)⁻¹ is wrong. The sandwich estimator (XᵀX)⁻¹ XᵀΩ̂X (XᵀX)⁻¹ replaces Ω with squared residuals.
- **HC0** uses e_i² (White's original); **HC1** scales the HC0 variance by n/(n−p) (the 'robust' option in Stata); **HC2** divides e_i² by (1 − h_ii); **HC3** divides by (1 − h_ii)², the most conservative and recommended in small samples or with high-leverage points. In large samples, all are nearly the same.
- **Cluster-robust:** allow arbitrary correlation of errors within a cluster (users, stores, schools, repeated measures); sum the scores inside each cluster before squaring. Needs a reasonable number of clusters (rule of thumb 30-50+); with few clusters, use wild cluster bootstrap or small-sample corrections.
- Use clustering at the level of randomisation or at the level where errors are correlated (e.g. users in a session-level analysis).
- Neither fixes bias from misspecified models; they fix inference only.

**Example:** Noise SD grows with x² : the classical slope SE is 0.202 while HC0 gives 0.237, HC3 0.238 (classical SEs about 15% too small). With 40 clusters and a regressor partly cluster-level, the iid SE is 0.042 but the cluster SE is 0.180: about 4 times larger, so the iid SE hugely overstates precision.

**Code:**
```python
import numpy as np, statsmodels.api as sm
rng = np.random.default_rng(0)
n = 1000
x = rng.uniform(0, 4, n); y = 1 + 0.5 * x + rng.normal(0, 0.1 + x**2, n)        # noise grows fast with x
X = sm.add_constant(x)
for ct in ["nonrobust", "HC0", "HC1", "HC2", "HC3"]:
    print(ct.ljust(10), sm.OLS(y, X).fit(cov_type=ct).bse[1].round(4))
g = rng.integers(0, 40, n)                                                     # 40 clusters
xg = rng.normal(size=40)[g] + 0.3 * rng.normal(size=n)                         # regressor partly cluster-level
yg = rng.normal(size=40)[g] + rng.normal(size=n)                               # no true effect
Xg = sm.add_constant(xg)
print("iid SE", sm.OLS(yg, Xg).fit().bse[1].round(4), " cluster SE",
      sm.OLS(yg, Xg).fit(cov_type="cluster", cov_kwds={"groups": g}).bse[1].round(4))
# nonrobust 0.202 | HC0 0.2368 | HC1 0.2371 | HC2 0.2372 | HC3 0.2375
# iid SE 0.0423  cluster SE 0.1797
```

**Follow-ups:**
- *Why not always use robust SEs?* They are slightly noisy in small samples and unnecessary if the errors are really homoscedastic; most practitioners use HC3 or cluster by default.
- *Do robust SEs change the point estimate?* No. For efficiency, use WLS if you know the variance structure.

**Common mistakes:** Believing robust SEs fix bias; clustering at too fine a level; using cluster-robust with very few clusters; reporting HC SEs but still using a t-distribution with n − p degrees of freedom for tiny samples.

=====Q10
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

- Gauss-Markov: with the first five, OLS is BLUE (best linear unbiased estimator). Normality is not required for that.
- Fixes: robust (HC) or clustered SEs for variance problems; instruments/controls for endogeneity.

**Example:** Regressing sales on ad spend when ad spend is higher in good seasons: exogeneity fails, β is biased up even with a million rows, and no SE correction helps.

**Follow-ups:**
- *Does the predictor need to be normal?* No. Only the errors matter, and only for small-sample inference.
- *Is R² an assumption check?* No.

**Common mistakes:** Saying "the data must be normally distributed"; listing normality as needed for unbiasedness; forgetting exogeneity, the one that actually causes bias.

=====Q11
**Say this first (1 line):** Heteroscedasticity means the error variance changes with X (e.g. a funnel in the residual plot); it leaves OLS coefficients unbiased but makes the standard errors wrong, so detect it with plots/Breusch-Pagan/White and fix with robust SEs, WLS or a transform.

**Then explain:**
- Detect: plot residuals vs fitted (a fan/funnel shape); Breusch-Pagan (regress squared residuals on X, tests for a linear link to X); White (adds squares and cross terms, so catches more forms but has less power). Null = homoscedastic.
- Fix 1, robust SEs (HC3 or HC0-HC3): keep the same β, change only the SEs. This is the default in practice.
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

=====Q12
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

=====Q13
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

=====Q14
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

=====Q15
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

=====Q16
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

=====Q17
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

=====Q18
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

=====Q19
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

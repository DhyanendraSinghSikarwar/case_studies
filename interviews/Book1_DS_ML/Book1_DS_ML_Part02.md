# Book 1 — Part 02: Linear/Logistic Regression, Regularization (L1/L2/Elastic Net), Feature Engineering

**Topic:** Linear and logistic regression, regularization, feature engineering
**Target:** >=45 questions | **Actual:** 51 questions | **Date:** 2026-10-20
**Stars:** 15 x ⭐⭐⭐ (Q1-Q15), 24 x ⭐⭐ (Q16-Q39), 12 x ⭐ (Q40-Q51)
**Status:** Answers written and reviewed (Wave C)

---

> Dedupe pass: removed 4 cross-part duplicate(s); renumbered Q1–Q51.
---

### Q1 ⭐⭐⭐ 🟢 Why can't we use linear regression for a classification problem? Why logistic regression instead?
**Asked at:** Flipkart, Swiggy, GCCs, startups
**Say this first (1 line):** Linear regression predicts any real number, so for a 0/1 target it gives "probabilities" below 0 or above 1 and is thrown off by far-away points; logistic regression passes the linear score through a sigmoid so the output is always a valid probability.

**Then explain:**
- Linear regression minimises squared error. For a binary target the errors are not Gaussian, and their variance depends on x (variance is p(1-p)), so the usual assumptions break.
- Predictions are not bounded in [0, 1], so they cannot be read as probabilities and thresholds are meaningless in the tails.
- One extreme point (say a very long distance) tilts the whole line and moves the decision threshold, even though that point is "obviously" class 1.
- Logistic regression models the log-odds as linear: `log(p/(1-p)) = w·x + b`. Sigmoid squashes this to (0, 1), and we fit by maximum likelihood (log loss), which suits Bernoulli targets.
- Fair point: for ranking only, linear regression on 0/1 (the "linear probability model") is sometimes used in econometrics because coefficients read as percentage-point changes. But for prediction, use logistic.

**Example:** Predicting whether an order is cancelled from delivery distance. At a very long distance linear regression says "1.6 probability"; logistic says 0.99.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
rng = np.random.default_rng(0)
x = rng.normal(size=(200, 1)); y = (x[:, 0] + rng.normal(0, .5, 200) > 0).astype(int)
pts = np.array([[-3.], [3.]])
print(LinearRegression().fit(x, y).predict(pts).round(2))                 # [-0.64  1.61]
print(LogisticRegression().fit(x, y).predict_proba(pts)[:, 1].round(3))   # [0. 1.]
```

**Follow-ups:**
- *Why not MSE with a sigmoid?* The loss becomes non-convex and gradients vanish when the model is confidently wrong (see Q9).
- *Is logistic regression linear?* Linear in log-odds and in the decision boundary, not in the probability (see Q3).

**Common mistakes:** Saying "because the output isn't between 0 and 1" and stopping there (also mention heteroscedastic non-normal errors and outlier sensitivity); claiming logistic regression is a classifier by itself, when it outputs probabilities and the threshold is a separate choice.

### Q2 ⭐⭐⭐ 🟢 What are the assumptions of linear regression, and what happens to the model if each is violated? (interview-level)
**Asked at:** Product cos, GCCs, consulting (ZS, Accenture), Europe
**Say this first (1 line):** Five assumptions: linearity, independent errors, constant error variance (homoscedasticity), roughly normal errors, and no perfect multicollinearity (plus no endogeneity, i.e. errors uncorrelated with X). Violations hurt either the coefficients (bias) or the standard errors and p-values (inference), not always both.

**Then explain:**

| Assumption | If violated | Detect | Fix |
|---|---|---|---|
| Linearity (E[y\|x] is linear in the features) | Biased coefficients, bad predictions | Residual vs fitted plot shows a curve | Transforms, polynomials, splines, trees |
| Independent errors | Coefficients OK, SEs too small (time series, clustered data) | Durbin-Watson, ACF of residuals | Lags, clustered/HAC SEs, mixed models |
| Constant variance | Coefficients still unbiased, SEs and CIs wrong | Funnel-shaped residual plot, Breusch-Pagan | Log target, robust (HC) SEs, WLS |
| Normal errors | Only matters for small-sample p-values and CIs; prediction is fine | QQ plot | Large n (CLT), transform, bootstrap |
| No perfect multicollinearity | `XtX` singular, no unique solution; near-collinearity inflates variance | VIF, condition number | Drop/combine features, Ridge (Q8) |
| Exogeneity (error uncorrelated with X) | Biased and inconsistent coefficients (omitted variable) | Domain thinking, instruments | Add the confounder, IV, experiments |

- Key point to say: OLS is still unbiased without normality or constant variance. Only linearity and exogeneity violations bias the coefficients.
- If you only care about prediction, most of these matter much less than good validation. They matter when you interpret coefficients or report p-values.

**Example:** Predicting delivery time from distance: the spread of errors grows with distance (funnel plot). Coefficients are still fine but the default CI is wrong; use HC3 robust standard errors or model `log(time)`.

**Code:**
```python
import numpy as np, statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
rng = np.random.default_rng(0)
x = rng.uniform(1, 10, 500); y = 2*x + rng.normal(0, x*0.5)   # noise grows with x
X = sm.add_constant(x); r = sm.OLS(y, X).fit()
print("BP p-value", round(het_breuschpagan(r.resid, X)[1], 4))     # ~0.0 -> heteroscedastic
print("classic SE", r.bse.round(3), "HC3 SE", sm.OLS(y, X).fit(cov_type="HC3").bse.round(3))
# classic SE [0.329 0.052] vs HC3 [0.224 0.053]  (intercept, slope)
```

**Follow-ups:**
- *Which assumption is needed for the coefficients to be unbiased?* Linear correct form plus exogeneity. Under Gauss-Markov (add homoscedasticity and no autocorrelation) OLS is also the best linear unbiased estimator (BLUE).
- *Does the target need to be normal?* No. The errors (given X) need to be, and only for small-sample inference.

**Common mistakes:** Saying "the target and features must be normal"; forgetting that heteroscedasticity leaves coefficients unbiased; checking assumptions on raw data instead of residuals.

### Q3 ⭐⭐⭐ 🟢 What is logistic regression? Is it a linear model, and what do the sigmoid and log-odds do?
**Asked at:** Swiggy, Flipkart, Klarna, GCCs
**Say this first (1 line):** Logistic regression is a linear model for the log-odds: it computes a linear score `z = w·x + b`, and the sigmoid turns that score into a probability. It is linear in log-odds and in its decision boundary, but not linear in the probability.

**Then explain:**
- **Odds** = p/(1-p). **Log-odds (logit)** = log(p/(1-p)). The model says `logit(p) = w·x + b`.
- **Sigmoid** `p = 1/(1+e^-z)` is the inverse of the logit. It maps any real score to (0, 1), with z=0 giving p=0.5.
- Each unit increase in x_j adds `w_j` to the log-odds, i.e. multiplies the odds by `e^{w_j}` (see Q7).
- Decision boundary `w·x + b = 0` is a hyperplane, so it is a linear classifier. A threshold of 0.5 on p is the same as z > 0.
- Fit by maximum likelihood (log loss, Q9). Convex, so one global optimum, no closed form; use gradient methods or Newton/IRLS.

**Example:** z = -4, -2, 0, 2, 4 gives p = 0.018, 0.119, 0.5, 0.881, 0.982. Equal steps in z are not equal steps in p: it moves fast near 0.5 and flattens in the tails.

**Code:**
```python
import numpy as np
z = np.array([-4, -2, 0, 2, 4.]); p = 1/(1+np.exp(-z))
print(p.round(3), np.log(p/(1-p)).round(1))   # [0.018 0.119 0.5 0.881 0.982] [-4. -2. 0. 2. 4.]
```

**Follow-ups:**
- *Why log-odds and not probability?* Log-odds range over the whole real line, so a linear function can model them without bounds problems.
- *Is the model calibrated?* Usually reasonably, since log loss is a proper scoring rule, but strong regularization or class weighting distorts it.

**Common mistakes:** Saying the probability is a linear function of x; forgetting the decision boundary is linear (so XOR-style patterns need feature engineering, Q24); mixing up odds and probability in interpretation.

### Q4 ⭐⭐⭐ 🟢 What is regularization and why do we need it? How does it relate to bias-variance?
**Asked at:** All company types
**Say this first (1 line):** Regularization adds a penalty on model complexity to the loss so the model cannot fit noise; it accepts a bit more bias to buy a lot less variance, which lowers test error when the model would otherwise overfit.

**Then explain:**
- Objective becomes `loss(data) + λ · penalty(weights)`. L2 penalty = sum of squared weights, L1 = sum of absolute weights (Q5).
- **Bias-variance:** test error ≈ bias² + variance + noise. A flexible model has low bias but high variance (it changes a lot with the training sample). Shrinking weights stabilises predictions: variance falls fast at first, bias rises slowly.
- λ controls the trade: λ=0 is plain fit (can overfit), λ huge shrinks everything toward a constant (underfit). Choose λ by cross-validation (Q11, Q23).
- Needed most when features are many relative to rows, or correlated (Q8, Q41).
- Other forms of regularization: early stopping, dropout, tree depth limits, data augmentation.

**Example:** 30 training rows, 40 features, only 3 truly useful. Unregularized fit has train MSE 0 and test MSE 16. With a moderate ridge penalty, train MSE rises but test MSE drops to about 5.

**Code:**
```python
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as mse
rng = np.random.default_rng(0)
X = rng.normal(size=(60, 40)); w = np.r_[2, -1, 1.5, np.zeros(37)]; y = X @ w + rng.normal(0, 2, 60)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.5, random_state=0)
for a in [1e-4, 1, 10, 100, 1000]:
    m = Ridge(alpha=a).fit(Xtr, ytr)
    print(a, round(mse(ytr, m.predict(Xtr)), 2), round(mse(yte, m.predict(Xte)), 2))
# alpha 1e-4: train 0.0, test 16.02 | alpha 100: train 3.37, test 5.22 | alpha 1000: train 5.34, test 5.91
```
Train error only rises with λ; test error falls then rises again (U shape).

**Follow-ups:**
- *Does regularization always help?* No. With lots of data and a simple model it may do nothing or hurt.
- *Bayesian view?* L2 = Gaussian prior on weights, L1 = Laplace prior (MAP estimate, Q22).

**Common mistakes:** Saying regularization "reduces bias" (it increases it); tuning λ on the test set; forgetting to standardize features first (Q18).

### Q5 ⭐⭐⭐ 🟢 L1 vs L2 regularization: how do they differ, and why does L1 give sparse weights while L2 only shrinks?
**Asked at:** Flipkart, Swiggy, Amazon, Europe product cos
**Say this first (1 line):** L1 (Lasso) penalizes the sum of absolute weights and drives many weights exactly to zero; L2 (Ridge) penalizes the sum of squared weights and shrinks all weights smoothly but almost never to exactly zero.

**Then explain:**
- **Geometry:** the constraint region for L1 is a diamond with corners on the axes; the loss contours usually touch it at a corner, where some weights are 0. L2's region is a circle with no corners, so the touch point has all weights non-zero.
- **Gradient view:** L2 gradient is `2λw`, which shrinks as w nears 0, so a weight gets pushed less and less. L1 gradient is `λ·sign(w)`, a constant push, so a weak weight is pushed all the way to 0 and stays.
- **Soft-thresholding view:** for an orthonormal design, Lasso gives `sign(w)·max(|w|-λ,0)` (exact zeros below λ), Ridge gives `w/(1+λ)` (just scaling) (Q49, Q21).
- L1 = built-in feature selection, sparse, more interpretable; unstable when features are correlated (picks one arbitrarily, Q37). L2 handles correlated features by sharing weight; usually better prediction when most features matter.
- L1 is not differentiable at 0, so use coordinate descent or proximal methods.

**Example:** 20 standardized features, 4 truly informative. Lasso keeps about 4 and zeroes 16; Ridge keeps all 20 non-zero.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import Lasso, Ridge
X, y = make_regression(200, 20, n_informative=4, noise=10, random_state=0)
Xs = (X - X.mean(0)) / X.std(0)
for name, m in [("lasso", Lasso(alpha=5)), ("ridge", Ridge(alpha=500))]:
    m.fit(Xs, y); print(name, "zeros:", int((np.abs(m.coef_) < 1e-8).sum()), "of 20")
# lasso zeros: 16 of 20 | ridge zeros: 0 of 20
```

**Follow-ups:**
- *When Ridge over Lasso?* Many small correlated effects, prediction is the goal (Q11).
- *Can you get both?* Elastic Net (Q16).

**Common mistakes:** Saying L2 "can't" give zeros (it can in theory, with probability zero in practice); explaining sparsity only with the diamond picture and no gradient reason; forgetting to scale features before either penalty.

### Q6 ⭐⭐⭐ 🟢 What is the difference between R-squared and adjusted R-squared? Can R-squared be negative?
**Asked at:** Swiggy, consulting/analytics, GCCs
**Say this first (1 line):** R² is the fraction of variance in y explained by the model; adjusted R² corrects it for the number of features, so it does not rise just because you added junk. Yes, R² can be negative on held-out data (the model is worse than just predicting the mean).

**Then explain:**
- `R² = 1 - SS_res/SS_tot`. On the training set of an OLS model with an intercept it lies in [0, 1] and never decreases when you add a feature, even a random one.
- `Adj R² = 1 - (1-R²)(n-1)/(n-p-1)`, with n rows and p features. It penalizes extra features and rises only if a new feature helps more than chance would.
- **Negative R²:** on test data (or a model without intercept) SS_res can exceed SS_tot, i.e. worse than predicting the training mean. That is a signal of overfitting or a distribution shift.
- R² says nothing about bias, whether the model form is right, or causation; high R² with a trending time series can be spurious.
- For comparing models, prefer held-out metrics (RMSE, MAE) or cross-validated R²; adjusted R² is for in-sample comparison of nested linear models.

**Example:** 30 rows of pure noise. With 30 noise features the train R² is 1.0 but test R² is -19.95. With 5 noise features R² = 0.111 but adjusted R² = -0.074.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LinearRegression
rng = np.random.default_rng(1)
X = rng.normal(size=(60, 30)); y = rng.normal(size=60)
tr, te = slice(0, 30), slice(30, 60)
m = LinearRegression().fit(X[tr], y[tr])
print(round(m.score(X[tr], y[tr]), 2), round(m.score(X[te], y[te]), 2))   # 1.0  -19.95
m5 = LinearRegression().fit(X[tr][:, :5], y[tr]); r2 = m5.score(X[tr][:, :5], y[tr])
print(round(r2, 3), round(1 - (1-r2)*(30-1)/(30-5-1), 3))               # 0.111  -0.074
```

**Follow-ups:**
- *Is a low R² bad?* Not necessarily: noisy human-behaviour targets often have R² of 0.1-0.3 and still be useful.
- *Does R² work for logistic regression?* Not directly; use log loss, AUC, or pseudo-R² (McFadden).

**Common mistakes:** Saying R² is always between 0 and 1; using adjusted R² to compare models with different targets (e.g. y vs log y); treating high R² as proof the model is correct.

### Q7 ⭐⭐⭐ 🟡 How do you interpret the coefficients of a linear regression and of a logistic regression (odds ratio)? If one weight is larger, is that feature more important?
**Asked at:** Product cos, fintech, GCCs
**Say this first (1 line):** In linear regression a coefficient is the change in y for a one-unit change in that feature, holding the others fixed; in logistic regression it is the change in log-odds, and `e^coef` is the odds ratio. A larger raw weight does not mean a more important feature, because it depends on the feature's units.

**Then explain:**
- **Linear:** `y = 3 + 2·distance` means each extra km adds 2 units to y, other features held constant (the "all else equal" caveat matters when features are correlated).
- **Logistic:** coefficient 0.29 means log-odds up by 0.29 per unit; odds ratio `e^0.29 = 1.33`, so odds multiply by 1.33 (about +33% in odds, not +33% in probability). Negative coefficient gives OR < 1.
- The effect on probability depends on where you are on the sigmoid: it is largest near p=0.5 and tiny in the tails. For probability effects use marginal effects or predictions at chosen points.
- **Importance:** a weight of 0.0002 on income (rupees) vs 0.5 on age (years) says nothing about importance. Compare standardized coefficients (features scaled to unit variance), or permutation importance (Q32). Even then, correlated features split or flip credit (Q33).
- Coefficients are associations, not causal effects, unless the design supports it.

**Example:** Order-cancel model: `dist_km` coef 0.29 (OR 1.33), `prime_member` coef -0.81 (OR 0.44). Each extra km raises the odds of cancel by 33%; Prime members have 56% lower odds.

**Code:**
```python
import numpy as np, pandas as pd, statsmodels.api as sm
rng = np.random.default_rng(2); n = 5000
dist = rng.uniform(1, 10, n); prime = rng.integers(0, 2, n)
y = rng.random(n) < 1/(1+np.exp(-(-2 + 0.3*dist - 0.8*prime)))
X = sm.add_constant(pd.DataFrame({"dist_km": dist, "prime": prime}))
res = sm.Logit(y.astype(int), X).fit(disp=0)
print(res.params.round(2).to_dict())          # const -1.9, dist_km 0.29, prime -0.81
print(np.exp(res.params).round(2).to_dict())  # OR: dist_km 1.33, prime 0.44
```

**Follow-ups:**
- *How to make weights comparable?* Standardize features first, or use permutation importance on held-out data.
- *Interpretation when y is logged?* `100·coef` is roughly the % change in y per unit of x; if both x and y are logged, coef is an elasticity (% change in y per 1% change in x).

**Common mistakes:** Reading the odds ratio as a probability ratio; calling the largest raw weight "most important"; ignoring that interpretation changes when features are regularized (shrunk) or collinear.

### Q8 ⭐⭐⭐ 🟡 What is multicollinearity? How does it affect linear regression, how do you detect it (VIF), and how do you fix it?
**Asked at:** Product cos, GCCs, C3 AI-type, Europe
**Say this first (1 line):** Multicollinearity means features are highly correlated with each other; the model still predicts fine, but individual coefficients become unstable with huge standard errors, so you cannot trust their size, sign, or p-values.

**Then explain:**
- **Why:** OLS cannot tell which of two near-duplicate features deserves the credit, so the coefficient estimates swing wildly between samples (variance of `β̂` scales with `(XtX)^-1`, which blows up).
- **Detect:** correlation matrix (only pairwise), **VIF** = `1/(1-R²_j)` where R²_j comes from regressing feature j on the others. Rule of thumb: VIF > 5-10 is a problem. Also condition number of X, or coefficients flipping when a feature is added/removed.
- **Fix:** drop or combine redundant features (ratio, average), PCA, domain grouping, or Ridge/Elastic Net, which stabilise coefficients (Q20, Q21). If you only need predictions and the collinearity pattern holds in production, you can leave it.
- Perfect collinearity (e.g. dummy trap, Q17) makes `XtX` singular and OLS has no unique solution.
- Tree ensembles are not hurt for prediction, but feature importances get split among correlated features.

**Example:** `b = a + small noise`; true y = 2a + noise. VIFs for a and b are about 98. The coefficient on `a` has SE 0.46 instead of 0.05 once `b` is in the model; dropping `b` brings SE back to 0.05.

**Code:**
```python
import numpy as np, pandas as pd, statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
rng = np.random.default_rng(3)
a = rng.normal(size=500); b = a + rng.normal(0, .1, 500); c = rng.normal(size=500)
y = 2*a + rng.normal(size=500)
X = sm.add_constant(pd.DataFrame({"a": a, "b": b, "c": c}))
print({col: round(float(vif(X.values, i)), 1) for i, col in enumerate(X.columns) if col != "const"})  # a 97.8, b 97.8, c 1.0
print(sm.OLS(y, X).fit().bse.round(2).to_dict())                       # a SE 0.46
print(sm.OLS(y, X[["const", "a", "c"]]).fit().bse.round(2).to_dict())  # a SE 0.05
```

**Follow-ups:**
- *Does multicollinearity hurt accuracy?* Not for in-distribution prediction; it hurts interpretation and stability.
- *Why is VIF better than a correlation matrix?* It catches a feature that is a combination of several others, which pairwise correlations miss.

**Common mistakes:** Saying it biases coefficients (it inflates variance, estimates stay unbiased); dropping features by looking only at pairwise correlation; computing VIF including dummy columns from the same categorical or without the constant.

### Q9 ⭐⭐⭐ 🟡 Derive the logistic regression loss (MLE / log loss) and its gradient. Why not use MSE for logistic regression?
**Asked at:** Flipkart (DS-2 math round), Amazon, Microsoft IDC
**Say this first (1 line):** Assume y ~ Bernoulli(p) with `p = σ(w·x)`; maximizing the likelihood gives the log loss `-[y log p + (1-y) log(1-p)]`, whose gradient is simply `(p - y)·x`. MSE is a poor choice because with a sigmoid it is non-convex and its gradient vanishes when the model is confidently wrong.

**Then explain:**
- **Likelihood:** for one point, `P(y|x) = p^y (1-p)^(1-y)`. For n independent points the log-likelihood is `Σ [y_i log p_i + (1-y_i) log(1-p_i)]`. Minimizing the negative mean of this is log loss (binary cross-entropy).
- **Gradient:** use `dp/dz = p(1-p)`. Then `∂L/∂z = -(y/p - (1-y)/(1-p))·p(1-p) = p - y`. So `∇_w L = (1/n) Xᵀ(p - y)`, the same form as linear regression's gradient. The `p(1-p)` terms cancel, which is the whole trick.
- **Hessian:** `XᵀSX/n` with `S = diag(p(1-p))`, positive semi-definite, so the loss is convex (one global minimum). Newton's method on this is IRLS.
- **Why not MSE:** `(σ(z)-y)²` has gradient `2(p-y)p(1-p)·x`. When the model is very wrong (p≈0 but y=1), `p(1-p)≈0` so the gradient vanishes and learning stalls. It is also non-convex in w. Log loss also heavily penalizes confident mistakes and is the proper MLE for Bernoulli data.

**Example:** y=1, model says p=0.01. Log-loss gradient factor = -0.99 (strong push); MSE gradient factor ≈ -2·0.99·0.01·0.99 ≈ -0.02 (tiny push).

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(0); n = 500
X = rng.normal(size=(n, 3)); y = (rng.random(n) < 1/(1+np.exp(-(X @ [1.5, -2, 0] + .5)))).astype(float)
Xb = np.c_[np.ones(n), X]; sig = lambda z: 1/(1+np.exp(-z))
loss = lambda w: -np.mean(y*np.log(sig(Xb@w)) + (1-y)*np.log(1-sig(Xb@w)))
w = np.zeros(4)
for _ in range(2000): w -= 0.5 * Xb.T @ (sig(Xb@w) - y) / n          # gradient = Xt(p-y)/n
print(w.round(2))                                                      # [ 0.79  1.41 -1.86 -0.05]
print(LogisticRegression(penalty=None).fit(X, y).coef_.round(2))      # [[ 1.41 -1.86 -0.05]]
w0 = rng.normal(size=4); g = Xb.T @ (sig(Xb@w0) - y) / n               # numerical gradient check
num = np.array([(loss(w0+1e-6*e) - loss(w0-1e-6*e))/2e-6 for e in np.eye(4)])
print(np.abs(g - num).max() < 1e-6)                                    # True
```

**Follow-ups:**
- *Does it have a closed form?* No; solve iteratively (gradient descent, L-BFGS, Newton/IRLS).
- *What if classes are separable?* MLE does not exist; weights go to infinity (Q38).

**Common mistakes:** Forgetting the `p(1-p)` cancellation and writing a messy gradient; saying MSE "doesn't work" without the vanishing-gradient/non-convexity reason; mixing up the sign (minimizing negative log-likelihood vs maximizing).

### Q10 ⭐⭐⭐ 🟡 How do you handle categorical variables for linear/logistic models? One-hot vs ordinal vs target/frequency encoding, and the dummy-variable trap.
**Asked at:** Flipkart, Swiggy, Amazon, Europe
**Say this first (1 line):** Linear and logistic models need numbers, so I one-hot encode nominal categories (dropping one level), use ordinal codes only when the order is real and roughly evenly spaced, and use target or frequency encoding for high-cardinality columns, done carefully to avoid leakage.

**Then explain:**

| Method | Use when | Watch out |
|---|---|---|
| One-hot (dummy) | Nominal, low cardinality (city tier, payment type) | Width grows; drop one level or the intercept collides (dummy trap, Q17) |
| Ordinal / integer | Real order (size S/M/L, rating) | Assumes equal spacing; for unordered labels it invents a false order |
| Frequency / count | High cardinality, popularity matters | Different categories can collide on the same count |
| Target / mean encoding | High cardinality (pincode, SKU) | Leaks the label unless done out-of-fold with smoothing (Q27, Q28) |
| Group rare levels into "other" | Long tail | Pick the threshold on train data only |

- **Dummy trap:** all K dummies plus an intercept are perfectly collinear (they sum to 1). Keep K-1 and the dropped level becomes the baseline; with regularization you can keep all K.
- Handle unseen categories at inference (`handle_unknown="ignore"`), and put the encoder inside the pipeline so it is fitted on training folds only.
- Trees can use ordinal codes or native categorical support; linear models cannot (Q40).

**Example:** City with 3 values: BLR, DEL, MUM. Dropping the first gives two columns, `city_DEL` and `city_MUM`; BLR is the baseline (both 0).

**Code:**
```python
import pandas as pd
df = pd.DataFrame({"city": ["BLR", "DEL", "MUM", "BLR"]})
print(pd.get_dummies(df, drop_first=True, dtype=int))
#    city_DEL  city_MUM
# 0         0         0
# 1         1         0
# 2         0         1
# 3         0         0
```

**Follow-ups:**
- *One-hot for 10,000 categories?* Sparse matrix works for linear models; otherwise hashing, target encoding, or embeddings.
- *Is ordinal encoding ever fine for nominal data with trees?* Yes, trees can split it into groups, though one-hot or native categorical handling is usually cleaner.

**Common mistakes:** Label-encoding nominal values for a linear model; fitting the encoder on all data before the split; forgetting an "unknown" bucket for production.

### Q11 ⭐⭐⭐ 🟡 How do you choose between Lasso and Ridge for a given problem, and how do you pick the regularization strength (CV)?
**Asked at:** Swiggy, Segment/Coupang-type, product cos
**Say this first (1 line):** Use Lasso when I believe only a few features matter or I want a sparse, interpretable model; use Ridge when many features each contribute a little or are correlated; and I pick the strength λ by cross-validation on the training data, never the test set.

**Then explain:**
- **Lasso (L1):** sparse; good with many irrelevant features. Weak with groups of correlated features (picks one at random, unstable). 
- **Ridge (L2):** keeps all features, stable under correlation, usually better pure prediction when signal is dense.
- Unsure? Try both, or Elastic Net (Q16) with `l1_ratio` tuned by CV.
- **Choosing λ:** grid on a log scale (e.g. 1e-3 to 1e3), K-fold CV (use time-based/grouped CV when the data demands it), pick λ with min CV error, or the largest λ within one standard error of the min for a simpler model (Q23). Standardize inside the CV pipeline.
- Final step: refit on all training data with the chosen λ, then evaluate once on the held-out test set.

**Example:** 30 features, 5 informative, 300 rows. LassoCV picks alpha 1.16 with 9 non-zero features; the 1-SE rule picks alpha 3.29 with exactly 5. RidgeCV picks alpha 0.7, keeping all 30.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LassoCV, RidgeCV
X, y = make_regression(300, 30, n_informative=5, noise=20, random_state=0)
lc = LassoCV(cv=5, random_state=0).fit(X, y)
print(round(lc.alpha_, 3), int((lc.coef_ != 0).sum()))                      # 1.156 9
print(round(RidgeCV(alphas=np.logspace(-2, 3, 20)).fit(X, y).alpha_, 2))    # 0.7
```
(Use `make_pipeline(StandardScaler(), LassoCV())` when features are on different scales.)

**Follow-ups:**
- *Which gives better test error?* Whichever matches the truth: sparse truth favours Lasso, dense truth favours Ridge; CV decides.
- *Does a large λ always mean better generalization?* No, too large underfits.

**Common mistakes:** Picking λ on the test set; not standardizing; using Lasso's selected features and then reporting naive p-values (Q47).

### Q12 ⭐⭐⭐ 🟡 Walk me through feature engineering on a project you did. Which features moved the metric and how did you validate them?
**Asked at:** Swiggy, Flipkart, Zalando, PhonePe, all resume-drill rounds
**Say this first (1 line):** I pick one project, name the business target, then walk through feature families I built from domain reasoning, which ones moved the validation metric (with an ablation), and how I made sure none of them leaked the future.

**Then explain:** (use this skeleton, with your own project)
- **Context in one breath:** problem, target, metric, baseline score. Example: "predicting delivery time (ETA); metric MAE; baseline = restaurant average prep time + distance."
- **Feature families, from domain thinking:** (1) raw: distance, items, hour; (2) aggregates: restaurant's 7-day median prep time, rider's recent speed; (3) interactions/ratios: items per kitchen load, rain × peak hour; (4) time features: hour, weekday, cyclical encoding (Q29); (5) encodings: target/frequency for high-cardinality (Q27/Q28).
- **Validation of each feature:** time-based split (not random), add feature groups one at a time (ablation), compare on the same folds, report delta with a confidence interval (bootstrap or fold variance), check importance with permutation importance (Q32), and sanity-check on segments (new restaurants, peak hours).
- **Leakage guard:** every aggregate uses only data available before the prediction time (point-in-time correct); encoders fit on train folds only.
- **What did not work, and why:** one or two features that added nothing or hurt (shows honesty), e.g. a noisy weather feature that duplicated hour-of-day.
- **Productionizing:** same code offline and online (feature store, Q35); monitoring for drift.

**Example (shape of the answer, numbers are yours):** "Baseline MAE X min. Adding kitchen-load aggregates cut it by about Y%; rider-speed features added little once load was in. I confirmed the gain on the last two weeks held out and on new restaurants separately."

**Follow-ups:**
- *How did you know the gain wasn't noise?* Repeated/time-series CV, the metric delta vs fold-to-fold std, and a final untouched holdout.
- *How would you change it with a GBM instead of a linear model?* Fewer manual transforms (trees handle non-linearity), but aggregates, ratios and time-aware features still matter.

**Common mistakes:** Listing features without saying what moved the metric; no baseline; random split on time-dependent data; claiming a gain from a single run; features that quietly use future information.

### Q13 ⭐⭐⭐ 🟡 What feature-selection methods do you know (filter, wrapper, embedded)? Is feature selection important for linear models, and can L1/L2 do it?
**Asked at:** Product cos, GCCs, consulting
**Say this first (1 line):** Filter methods score each feature on its own (correlation, mutual information, chi-square), wrappers search subsets by repeatedly fitting a model (forward/backward, RFE), and embedded methods select during training (Lasso, tree importance). For linear models selection helps interpretability, speed, and variance, and yes, L1 does selection while L2 only shrinks.

**Then explain:**

| Type | Idea | Pros | Cons |
|---|---|---|---|
| Filter | Rank features by a statistic, keep top k | Fast, model-free | Ignores interactions and redundancy |
| Wrapper | Fit the model on candidate subsets (RFE, stepwise) | Accounts for the model | Expensive, overfits the selection |
| Embedded | Selection inside training (Lasso, elastic net, trees) | Cheap, model-aware | Tied to that model; unstable under correlation |

- **Linear models:** with many noisy features selection reduces variance and overfitting; with few good features it matters little. Ridge keeps everything; Lasso zeroes weak ones.
- **Do selection inside cross-validation.** Choosing features on the full data and then cross-validating leaks information and inflates scores (Q36).
- P-value-based stepwise selection is fragile (multiple testing, instability); prefer penalized methods plus CV.

**Example:** 300 rows, 30 features, 5 informative. Filter (`SelectKBest`), wrapper (RFE) and embedded (LassoCV) pick overlapping sets; they agree on most of the strong features but differ on the weak tail.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.feature_selection import SelectKBest, f_regression, RFE
from sklearn.linear_model import LinearRegression, LassoCV
X, y = make_regression(300, 30, n_informative=5, noise=20, random_state=0)
print(np.where(SelectKBest(f_regression, k=5).fit(X, y).get_support())[0])        # [ 3  7  8 21 22]
print(np.where(RFE(LinearRegression(), n_features_to_select=5).fit(X, y).support_)[0])  # [ 3  5  7  8 22]
print(np.where(LassoCV(cv=5, random_state=0).fit(X, y).coef_ != 0)[0])             # 9 features incl. 3 5 7 8 22
```

**Follow-ups:**
- *Why not just keep all features?* Cost, latency, interpretability, and variance when p is large relative to n.
- *Does a univariate filter miss anything?* Yes: a feature that matters only in combination with another.

**Common mistakes:** Selecting features on the whole dataset before CV; relying on univariate p-values; treating Lasso's chosen set as "the true features" (it is unstable with correlated features).

### Q14 ⭐⭐⭐ 🟡 How do you solve linear regression: normal equation vs gradient descent (batch/SGD/mini-batch)? When do you prefer which?
**Asked at:** Amazon, Microsoft IDC, Flipkart, consulting
**Say this first (1 line):** The normal equation `w = (XᵀX)⁻¹Xᵀy` gives the exact answer in one step but costs about O(n·p² + p³); gradient descent is iterative and approximate but scales to huge n and p, and works for models with no closed form.

**Then explain:**
- **Normal equation:** set gradient to zero and solve. No learning rate, no iterations. Needs `XᵀX` invertible (fails with collinearity); in practice use `np.linalg.lstsq`/QR/SVD rather than an explicit inverse. Good for p up to a few thousand.
- **Batch GD:** each step uses all n rows: cost O(n·p) per step, stable, needs a tuned learning rate and feature scaling for fast convergence.
- **SGD / mini-batch:** use one row or a small batch per step: cheap, noisy, can handle data that doesn't fit in memory and online updates; learning-rate decay is needed to converge.
- Choose: small/medium tabular, linear regression: closed form. Millions of rows or features, streaming, or logistic/neural models: GD variants.
- Linear regression loss is convex, so GD converges to the same answer as the normal equation.

**Example:** n=1,000, p=3, true weights [3, 2, -1, 0.5]. Normal equation and 500 steps of batch GD give the same coefficients.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0); n = 1000
X = rng.normal(size=(n, 3)); y = X @ [2, -1, .5] + 3 + rng.normal(0, .5, n)
Xb = np.c_[np.ones(n), X]
w_ne = np.linalg.solve(Xb.T @ Xb, Xb.T @ y)              # normal equation
w = np.zeros(4)
for _ in range(500): w -= 0.1 * (2/n) * Xb.T @ (Xb @ w - y)   # batch GD on MSE
print(w_ne.round(3), w.round(3))                         # both [ 3.018  1.975 -0.972  0.518]
```

**Follow-ups:**
- *Why not invert XᵀX?* It squares the condition number; use QR/SVD (`lstsq`) for stability.
- *Why scale features for GD?* Otherwise the loss surface is a stretched valley and GD zig-zags or diverges.
- *Why use mini-batch?* Good GPU/vectorization use with less noise than single-sample SGD.

**Common mistakes:** Saying GD finds a different (worse) solution on a convex problem; forgetting `XᵀX` is singular with perfect collinearity; ignoring that the normal equation's cubic cost in p is what limits it.

### Q15 ⭐⭐⭐ 🟡 Which regression error metric would you choose: MSE, RMSE, MAE, Huber, MAPE? How does the choice affect the model with outliers?
**Asked at:** Zalando, product cos, GCCs
**Say this first (1 line):** I choose the metric that matches the business cost: RMSE if big errors are disproportionately costly, MAE if I want a robust "typical error" in the target's units, Huber as a compromise for training, and MAPE only when relative error matters and the target is never near zero.

**Then explain:**
- **MSE/RMSE:** squares errors, so outliers dominate; training on MSE targets the conditional mean. RMSE is in target units.
- **MAE:** treats all errors linearly; robust to outliers; training on it targets the conditional median.
- **Huber:** quadratic for small errors, linear beyond a threshold δ: smooth like MSE near zero, robust like MAE in the tails.
- **MAPE:** percentage error, easy to explain, but explodes when y is near 0 and penalizes over-prediction less than under-prediction (asymmetric). Alternatives: sMAPE, WAPE, or RMSLE.
- Evaluation metric and training loss need not be the same, but a mismatch (train MSE, evaluate MAE with skewed errors) can hurt.

**Example:** actuals [10, 12, 11, 13, 12], predictions [11, 11, 12, 12, 12]: MAE 0.8, RMSE 0.9. Change the first actual to 100 (a data glitch): MAE 18.4, RMSE 39.8, so RMSE reacts about twice as strongly.

**Code:**
```python
import numpy as np
yp = np.array([11, 11, 12, 12, 12.])
for name, t in [("clean", np.array([10, 12, 11, 13, 12.])), ("outlier", np.array([100, 12, 11, 13, 12.]))]:
    e = t - yp; print(name, "MAE", np.abs(e).mean().round(1), "RMSE", np.sqrt((e**2).mean()).round(1))
# clean MAE 0.8 RMSE 0.9 | outlier MAE 18.4 RMSE 39.8
```

**Follow-ups:**
- *Why would MAE-trained models underpredict the mean on skewed data?* They estimate the median, which is below the mean for right-skewed targets.
- *Delivery-time P90 target?* Use quantile loss (Q43).

**Common mistakes:** Quoting MAPE on targets containing zeros; picking RMSE just because it is default; ignoring that data errors vs real rare events need different handling.

### Q16 ⭐⭐ 🟢 What is Elastic Net, and when would you use it over Lasso or Ridge?
**Asked at:** Product cos, GCCs, Europe
**Say this first (1 line):** Elastic Net mixes L1 and L2 penalties, so it gives sparsity like Lasso but, like Ridge, keeps groups of correlated features together instead of picking one at random.

**Then explain:**
- **Objective (sklearn):** `1/(2n)·||y - Xw||² + α·[ρ·||w||₁ + (1-ρ)/2·||w||₂²]`, where α is overall strength and ρ = `l1_ratio` (ρ=1 is Lasso, ρ→0 is Ridge-like).
- **Grouping effect:** with a block of correlated features, Lasso keeps one and drops the rest (unstable); Elastic Net spreads the weight across them, so results are more stable (Q37).
- **Also:** works when p > n (Lasso can select at most n features, Elastic Net can select more).
- Use it when features are correlated and you still want some sparsity. Tune two knobs (α and `l1_ratio`) by CV, which costs more than a single-parameter search.
- If you do not need sparsity, plain Ridge is simpler.

**Example:** Three near-copies of one signal `z` plus 3 noise columns, y = 3z + noise. Lasso gives weights [1.68, 0.33, 0.83] (arbitrary split); Elastic Net gives [0.98, 0.92, 0.94] (shared evenly), and both zero out the noise.

**Code:**
```python
import numpy as np
from sklearn.linear_model import Lasso, ElasticNet
rng = np.random.default_rng(0); z = rng.normal(size=400)
X = np.c_[z + rng.normal(0, .05, 400), z + rng.normal(0, .05, 400), z + rng.normal(0, .05, 400), rng.normal(size=(400, 3))]
y = 3*z + rng.normal(size=400)
print(Lasso(alpha=.1).fit(X, y).coef_.round(2))                      # [ 1.68  0.33  0.83 -0.01  0.  0. ]
print(ElasticNet(alpha=.1, l1_ratio=.5).fit(X, y).coef_.round(2))   # [ 0.98  0.92  0.94 -0.06  0.  0. ]
```

**Follow-ups:**
- *How do you tune it?* `ElasticNetCV` over a grid of `l1_ratio` (e.g. 0.1, 0.5, 0.9, 0.99) and an α path.
- *Any downside?* Double shrinkage biases the coefficients; the original paper rescales the naive solution.

**Common mistakes:** Not standardizing; mixing up α and `l1_ratio` between sklearn and glmnet (glmnet's λ and α correspond differently); expecting identical coefficients across runs from Lasso when features are correlated.

### Q17 ⭐⭐ 🟢 What is the dummy variable trap, and how does drop-first/intercept handling resolve it?
**Asked at:** Consulting, GCCs, analytics roles
**Say this first (1 line):** If you one-hot encode a category with K levels and keep all K dummy columns plus an intercept, the dummies sum to the intercept column, so the design matrix is perfectly collinear; dropping one level (the baseline) removes the redundancy.

**Then explain:**
- **Why it breaks:** `d1 + d2 + ... + dK = 1 = intercept column`, so `XᵀX` is singular and OLS has infinitely many solutions (you could add c to the intercept and subtract c from every dummy coefficient).
- **Fix 1: drop one level** (`drop_first=True`). Each remaining coefficient is the difference vs the dropped baseline; choose a meaningful baseline (the most common level).
- **Fix 2: keep all K and drop the intercept**; then each coefficient is that group's mean level. This is awkward when there are several categoricals.
- **Fix 3: keep all K with a Ridge/Lasso penalty**, which gives a unique solution (the baseline is then implicit and symmetric).
- Trees and regularized models do not need it; it matters for unregularized OLS/GLMs, and for p-values.

**Example:** Three cities and an intercept: the design matrix has 4 columns but rank 3. Dropping one dummy gives 3 columns, rank 3.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0); city = rng.integers(0, 3, 100); D = np.eye(3)[city]
full = np.c_[np.ones(100), D]; red = np.c_[np.ones(100), D[:, 1:]]
print(np.linalg.matrix_rank(full), full.shape[1])   # 3 4  -> rank deficient
print(np.linalg.matrix_rank(red), red.shape[1])     # 3 3  -> full rank
```

**Follow-ups:**
- *Does the choice of baseline change predictions?* No, only the coefficient interpretation.
- *Does sklearn's LinearRegression crash with the trap?* No, it uses a least-squares solver and returns a minimum-norm solution, but the coefficients are not uniquely interpretable; statsmodels may warn about singularity.

**Common mistakes:** Dropping the intercept and a level; applying `drop_first` separately on train and test with different categories; assuming Lasso/Ridge users must always drop a level.

### Q18 ⭐⭐ 🟢 Why does regularization not usually penalize the intercept, and why must features be standardized before applying a penalty?
**Asked at:** Product cos, Amazon
**Say this first (1 line):** The intercept just sets the baseline level of y, and shrinking it would make predictions depend on where y happens to be centred; features are standardized because the penalty is applied to raw weight sizes, which depend on each feature's units.

**Then explain:**
- **Intercept:** it is not a measure of complexity. If you penalized it, shifting all targets by a constant would change the fitted slopes. Centering X and y makes the intercept equal to mean(y) and takes it out of the problem (sklearn does this internally and does not penalize it).
- **Scaling:** a feature in rupees (range 50,000) needs a tiny weight, one in years needs a large weight. The penalty on `Σw²` then hits the "years" feature harder, purely because of units, not importance. After standardization (mean 0, std 1) all features are penalized on the same scale.
- Without scaling, the solution also changes if you change units (km → m), which it should not.
- Scale using train-fold statistics only, inside a pipeline.
- Exceptions: one-hot columns (already 0/1, often left unscaled or scaled by convention), and tree models (no penalty on weights).

**Example:** Income (mean 50,000, true coef 5e-5) and age (true coef 0.5). Ridge alpha=1000 on raw data barely touches the income coefficient (5e-5) but shrinks age from 0.497 to 0.480. On standardized data both are shrunk heavily: OLS 0.79, 3.73 becomes Ridge 0.27, 1.24.

**Code:**
```python
import numpy as np
from sklearn.linear_model import Ridge, LinearRegression
rng = np.random.default_rng(0); n = 500
inc = rng.normal(50000, 15000, n); age = rng.normal(35, 8, n)
y = 0.00005*inc + 0.5*age + rng.normal(0, 1, n)
X = np.c_[inc, age]; Xs = (X - X.mean(0)) / X.std(0)
print(LinearRegression().fit(X, y).coef_.round(5), Ridge(alpha=1e3).fit(X, y).coef_.round(5))
# OLS [5.e-05 4.966e-01] vs Ridge [5.e-05 4.796e-01]: income escapes the penalty
print(LinearRegression().fit(Xs, y).coef_.round(2), Ridge(alpha=1e3).fit(Xs, y).coef_.round(2))
# OLS [0.79 3.73] vs Ridge [0.27 1.24]: both shrunk on the same footing
```

**Follow-ups:**
- *In sklearn's LogisticRegression is the intercept penalized?* Not by default with lbfgs, but `liblinear` does penalize it unless `intercept_scaling` is raised.
- *Min-max vs standardization for penalties?* Either works; standardization is the usual choice (Q19).

**Common mistakes:** Fitting the scaler on the full data before the split; forgetting to scale before Lasso; penalizing the intercept by adding a column of ones and treating it as a feature.

### Q19 ⭐⭐ 🟢 Normalization vs standardization vs robust scaling: which to use when, and how do outliers affect each?
**Asked at:** Product cos, GCCs, startups
**Say this first (1 line):** Standardization (z-score) is the default for linear models, SVMs, PCA and anything gradient- or distance-based; min-max normalization is for bounded inputs like images or neural nets; robust scaling (median and IQR) is for features with heavy outliers.

**Then explain:**

| Scaler | Formula | Use when | Outlier effect |
|---|---|---|---|
| Min-max | (x - min)/(max - min), range [0, 1] | Bounded features, NN inputs, image pixels | One outlier squeezes all other values into a tiny range |
| Standardization | (x - mean)/std | Default for regularized linear, SVM, kNN, PCA | Mean and std are pulled by outliers, but less extreme than min-max |
| Robust | (x - median)/IQR | Heavy-tailed or dirty data | Median and IQR barely move; the outlier stays large but others keep their spread |

- Scaling does not remove outliers; it only changes units. For skewed data, a log transform often helps more than any scaler.
- Trees and gradient boosting do not need scaling (split thresholds are order-based).
- Fit the scaler on train only; apply the same parameters to validation, test and production.

**Example:** Values [10, 12, 11, 13, 12, 1000]. Min-max gives 0, 0, 0, 0, 0, 1 (information in the normal values is squashed). Standardization gives about -0.45 for the five normal values, 2.24 for the outlier. Robust scaling gives -1.33, 0, -0.67, 0.67, 0, 658.67: normal values stay well spread, and the outlier is visibly extreme.

**Code:**
```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
v = np.array([[10], [12], [11], [13], [12], [1000.]])
for s in [MinMaxScaler(), StandardScaler(), RobustScaler()]:
    print(type(s).__name__, s.fit_transform(v).ravel().round(2))
# MinMaxScaler [0. 0. 0. 0. 0. 1.] | StandardScaler [-0.45 -0.45 -0.45 -0.44 -0.45 2.24]
# RobustScaler [-1.33 0. -0.67 0.67 0. 658.67]
```

**Follow-ups:**
- *Does standardization change the distribution shape?* No, only location and scale.
- *Which for kNN or k-means?* Standardization (or min-max); distance is scale-sensitive.

**Common mistakes:** Saying normalization "removes outliers"; scaling before the train/test split; scaling tree models and then worrying about it; scaling the target without inverting the transform at prediction time.

### Q20 ⭐⭐ 🟡 If one column is the sum of two others (or the sum plus noise), what happens to a linear model and to its Ridge/Lasso version?
**Asked at:** Grigorev-style theory banks, product cos
**Say this first (1 line):** If c = a + b exactly, plain OLS has no unique solution (infinitely many weight combinations give identical predictions); with a little noise it has a solution but huge variance; Ridge gives a unique, stable answer that shares weight, and Lasso keeps a sparse choice.

**Then explain:**
- **Exact sum:** the matrix has rank 2 for 3 columns, so `XᵀX` is singular. Any `(w_a, w_b, w_c) = (w_a + t, w_b + t, w_c - t)` fits equally well. Software returns something arbitrary: `np.linalg.inv` fails or is garbage, `lstsq`/sklearn return the minimum-norm solution, statsmodels warns.
- **Sum plus noise:** the matrix is invertible but nearly singular (huge condition number). The weights exist but swing wildly between samples and have enormous standard errors, while predictions stay fine (Q8).
- **Ridge:** `XᵀX + λI` is always invertible. Among all equally good solutions it picks the one with the smallest weights, so credit is split across the redundant columns. Result is unique and stable.
- **Lasso:** tends to keep a sparse subset (e.g. drop a or c); which one it drops can change with data or solver (Q37).
- Practical fix: remove the redundant column if the relationship is exact (it adds no information).

**Example:** y = a + 2b + noise, c = a + b. Rank is 2. OLS (min-norm), Ridge and Lasso all give weights close to [0, 1, 1] here. Predictions are identical to the model on (a, b) only. (If c = a + b + 0.01·noise, `XᵀX` has condition number about 1e5, so OLS weights are very noise-sensitive.)

**Code:**
```python
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
rng = np.random.default_rng(0); a, b = rng.normal(size=300), rng.normal(size=300); c = a + b
y = a + 2*b + rng.normal(0, .1, 300); X = np.c_[a, b, c]
print(np.linalg.matrix_rank(X))                          # 2
print(LinearRegression().fit(X, y).coef_.round(2))       # [0. 1. 1.]   (min-norm solution)
print(Ridge(alpha=1).fit(X, y).coef_.round(2))           # [0. 1. 1.]
print(Lasso(alpha=.01).fit(X, y).coef_.round(2))         # [0.   0.99 1.  ]
```

**Follow-ups:**
- *Why does the min-norm solution have [0,1,1]?* The solutions are (1-t, 2-t, t); the smallest norm is at t=1.
- *Does it hurt prediction?* No, only the weights' interpretation and stability.

**Common mistakes:** Saying OLS "crashes" (depends on the solver); claiming Ridge recovers the "true" weights (there are none identifiable); not distinguishing exact from near collinearity.

### Q21 ⭐⭐ 🟡 Why does Ridge fix the singular XtX problem? Write the closed-form Ridge solution and explain shrinkage.
**Asked at:** Amazon, Microsoft IDC, research-leaning roles
**Say this first (1 line):** Ridge solves `min ||y - Xw||² + λ||w||²`, giving `w = (XᵀX + λI)⁻¹ Xᵀy`; adding λI lifts every eigenvalue of `XᵀX` by λ, so the matrix is invertible even when columns are collinear, and the weights are shrunk toward zero.

**Then explain:**
- **Derivation:** gradient `-2Xᵀ(y - Xw) + 2λw = 0`, so `(XᵀX + λI)w = Xᵀy`.
- **Why invertible:** `XᵀX` is positive semi-definite (eigenvalues ≥ 0, some may be 0 under collinearity). `XᵀX + λI` has eigenvalues ≥ λ > 0, so it is positive definite and invertible. It also improves the condition number.
- **Shrinkage via SVD:** with `X = UDVᵀ`, fitted values are `Σ u_i · d_i²/(d_i² + λ) · (u_iᵀy)`. Directions with large singular values (strong signal) are barely shrunk; directions with small singular values (the unstable, collinear ones) are shrunk the most. That is exactly where OLS variance comes from.
- λ→0 gives OLS; λ→∞ gives w→0. Cost is the same O(p³) as OLS; solve with a linear solver, not an explicit inverse.
- Intercept excluded from the penalty (center the data first, Q18).

**Example:** Four independent features plus an exact duplicate of the first, y ≈ 2·x₁. `XᵀX` is singular, so `np.linalg.solve(XᵀX, Xᵀy)` would fail; the Ridge system is solvable and splits the weight equally, about 0.99 on each copy (total about 1.99).

**Code:**
```python
import numpy as np
from sklearn.linear_model import Ridge
rng = np.random.default_rng(0)
X = rng.normal(size=(50, 4)); X = np.c_[X, X[:, 0]]            # last column duplicates the first
y = 2*X[:, 0] + rng.normal(size=50); lam = 1.0
w = np.linalg.solve(X.T @ X + lam*np.eye(5), X.T @ y)          # closed form
print(w.round(3))                                               # [ 0.994 -0.008  0.002  0.233  0.994]
print(Ridge(alpha=lam, fit_intercept=False).fit(X, y).coef_.round(3))   # same numbers
```

**Follow-ups:**
- *Is Ridge unbiased?* No: biased toward zero, but variance falls more (Q50).
- *Dual/kernel form?* `w = Xᵀ(XXᵀ + λI)⁻¹y`, cheaper when p > n.

**Common mistakes:** Writing `(XᵀX + λ)⁻¹` without the identity; saying Ridge makes `XᵀX` "non-singular" without the eigenvalue argument; penalizing the intercept.

### Q22 ⭐⭐ 🟡 How does L2 regularization appear in logistic regression (sklearn's C parameter, MAP view)? How does it change the gradient?
**Asked at:** Flipkart (DS-2 math round), Amazon, fintech
**Say this first (1 line):** L2-regularized logistic regression minimizes `C·Σ logloss + ½||w||²` in sklearn, so `C = 1/λ` is the inverse of the regularization strength; it is the MAP estimate under a Gaussian prior on the weights, and it adds a `λw` term to the gradient.

**Then explain:**
- **Objective (sklearn):** `min ½||w||² + C·Σᵢ logloss_i`. Small C = strong regularization (weights shrink); large C = weak. Default C=1. This is the opposite direction from Ridge's `alpha`.
- **Gradient:** `∇ = Xᵀ(p - y) + λw` (with the mean-loss form: `Xᵀ(p-y)/n + λw`). Each step pulls weights toward 0 ("weight decay"). Intercept is not penalized (except in liblinear, Q18).
- **MAP view:** posterior ∝ likelihood × prior. A Gaussian prior `w ~ N(0, σ²)` gives `-log prior = ||w||²/(2σ²)`, so L2 penalty with λ = 1/σ². Laplace prior gives L1.
- **Why it helps:** it keeps the model well-posed when classes are separable (weights would go to infinity, Q38), reduces overfitting with many features, and stabilises correlated features.
- Features must be standardized first; tune C on a log grid by CV.

**Example:** Sum of absolute weights on a 10-feature problem: C=0.001 gives 0.39 (almost everything shrunk), C=0.1 gives 2.06, C=10 gives 2.29 (approx. unregularized).

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
X, y = make_classification(500, 10, random_state=0)
for C in [0.001, 0.1, 10]:
    print(C, np.abs(LogisticRegression(C=C).fit(X, y).coef_).sum().round(2))   # 0.39, 2.06, 2.29
```

**Follow-ups:**
- *Convert between C and Ridge alpha?* λ = 1/C when the loss is summed; with a mean loss, λ = 1/(C·n).
- *Does regularization hurt calibration?* Strong shrinkage pulls probabilities toward the base rate; recalibrate if needed.

**Common mistakes:** Treating C like Ridge's alpha (bigger = stronger); forgetting to scale; claiming L2 gives sparse weights.

### Q23 ⭐⭐ 🟡 How do you choose lambda in practice (LassoCV/RidgeCV, one-standard-error rule, regularization path) and what do you do if CV curves are flat?
**Asked at:** Product cos, Europe
**Say this first (1 line):** I use LassoCV/RidgeCV (K-fold cross-validation over a log-spaced λ path), plot CV error against λ, pick the minimum or the largest λ within one standard error of the minimum for a simpler model, and if the curve is flat I take the simpler, stronger-regularized model.

**Then explain:**
- **Regularization path:** fit across many λ from large (all weights 0) to small. For Lasso, plot coefficients vs λ to see the order features enter.
- **λ_min** = lowest mean CV error. **λ_1se** = largest λ whose CV error is within one standard error of the min: a sparser, more stable model with nearly the same accuracy.
- **Flat CV curve** means many λ perform equally: the features carry little signal, or the data is small/noisy. Prefer the 1-SE (simpler) choice, check the CV standard error, use repeated CV, and consider whether the model is useful at all against a baseline.
- Do it in a pipeline so scaling is fitted per fold; use grouped/time-based folds if rows are not independent.
- Final: refit on full training data, evaluate once on the test set.

**Example:** 300 rows, 30 features (5 real). LassoCV: λ_min = 1.16 keeps 9 features; λ_1se = 3.29 keeps exactly 5.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LassoCV, Lasso
X, y = make_regression(300, 30, n_informative=5, noise=20, random_state=0)
lc = LassoCV(cv=5, random_state=0).fit(X, y)
mean = lc.mse_path_.mean(1); se = lc.mse_path_.std(1) / np.sqrt(5)
i = mean.argmin(); a_1se = lc.alphas_[np.where(mean <= mean[i] + se[i])[0].min()]   # alphas descend
print(round(lc.alpha_, 3), round(a_1se, 3))                                          # 1.156 3.292
print((lc.coef_ != 0).sum(), (Lasso(alpha=a_1se).fit(X, y).coef_ != 0).sum())        # 9 5
```

**Follow-ups:**
- *Why log-spaced grid?* Effects of λ are multiplicative.
- *Why 1-SE?* The CV minimum is itself noisy; the simpler model is nearly as good and generalizes more reliably.

**Common mistakes:** Picking λ using the test set; choosing the argmin on a flat curve and over-trusting it; forgetting that LassoCV's `alphas_` are in descending order when implementing the 1-SE rule.

### Q24 ⭐⭐ 🟡 Logistic regression decision boundary is linear. How do you capture non-linearity (interactions, polynomial features, splines, binning)?
**Asked at:** Product cos, fintech, GCCs
**Say this first (1 line):** The model stays linear in the parameters, so I add non-linear transforms of the inputs (interactions, polynomials, splines, bins) as new columns and let logistic regression fit weights on them.

**Then explain:**
- **Interactions:** `x1·x2` when the effect of one feature depends on another (distance × rain).
- **Polynomials:** `x, x²` capture a U-shape; high degrees oscillate at the edges, so keep degree low and regularize.
- **Splines:** piecewise polynomials joined smoothly at knots; flexible, smooth, more stable than high-degree polynomials. Basis of GAMs (Q48).
- **Binning:** bucket a numeric feature (and one-hot); simple, robust to outliers, interpretable (scorecards, Q39), but loses within-bin information and has jumps at the edges.
- Use regularization and CV to control the added flexibility; or switch to a tree ensemble if you need many interactions automatically.

**Example:** True log-odds depend on x² (high risk at both extremes). A plain logistic model scores AUC 0.49 (a straight line cannot do it); adding x² or splines gives 0.89.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
rng = np.random.default_rng(0); x = rng.uniform(-3, 3, (1000, 1))
y = (rng.random(1000) < 1/(1+np.exp(-(x[:, 0]**2 - 2)))).astype(int)
for name, m in [("linear", LogisticRegression()),
                ("poly2", make_pipeline(PolynomialFeatures(2), LogisticRegression())),
                ("spline", make_pipeline(SplineTransformer(n_knots=6), LogisticRegression()))]:
    print(name, cross_val_score(m, x, y, cv=5, scoring="roc_auc").mean().round(3))
# linear 0.488, poly2 0.889, spline 0.889
```

**Follow-ups:**
- *Is the model still "linear"?* Yes in the weights, so it is still convex and fit by the same methods; the boundary in the original space is curved.
- *When bins over splines?* When regulators or business users need simple step rules.

**Common mistakes:** Adding high-degree polynomials without scaling or regularization; binning on the full data (leak) or with too many tiny bins; adding all pairwise interactions blindly.

### Q25 ⭐⭐ 🟡 How do outliers affect linear regression and what robust options exist (winsorizing, Huber, quantile regression)?
**Asked at:** Product cos, GCCs, consulting
**Say this first (1 line):** OLS minimizes squared errors, so a few extreme points can drag the line a long way; I first check whether the outliers are data errors or real, then either clean/winsorize or use a robust loss such as Huber or median (quantile) regression.

**Then explain:**
- **Why OLS is sensitive:** squaring gives far points huge weight; high-leverage points (extreme in x) pull the fit most. Diagnose with residual plots, leverage, Cook's distance.
- **First step:** investigate. Data error (fix/remove), genuine rare event (keep, model it), or a different population (segment).
- **Winsorizing:** cap values at e.g. the 1st/99th percentile (percentiles computed on train only). Simple, but changes the data.
- **Huber regression:** quadratic loss for small residuals, linear for big ones; downweights outliers while staying smooth.
- **Quantile regression (median, q=0.5):** minimizes absolute error, robust in y; also lets you model other quantiles (Q43).
- Others: RANSAC, Theil-Sen, log-transform the target (Q26).

**Example:** True slope 2. Five points with +60 added to y: OLS slope falls to 1.36; Huber 1.96; median regression 1.96.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LinearRegression, HuberRegressor, QuantileRegressor
rng = np.random.default_rng(0); x = rng.uniform(0, 10, (100, 1))
y = 2*x[:, 0] + 1 + rng.normal(0, 1, 100); y[:5] += 60
print(LinearRegression().fit(x, y).coef_.round(2))                                  # [1.36]
print(HuberRegressor().fit(x, y).coef_.round(2))                                    # [1.96]
print(QuantileRegressor(quantile=.5, alpha=0, solver="highs").fit(x, y).coef_.round(2))   # [1.96]
```

**Follow-ups:**
- *Outliers in x vs in y?* Outliers in x (leverage) are more dangerous; Huber/median protect against y outliers but not necessarily leverage points.
- *Should you just delete them?* Only with a reason; deleting real extremes makes the model overconfident.

**Common mistakes:** Removing outliers by a rule without understanding them; computing winsorization limits on the full data; using Huber with unscaled features/targets (its threshold is scale-dependent; sklearn's HuberRegressor estimates scale).

### Q26 ⭐⭐ 🟡 Target is right-skewed (e.g., price, delivery time). Do you log-transform it? How do you interpret results and avoid back-transform bias?
**Asked at:** Swiggy, Flipkart, Zalando, pricing/ETA teams
**Say this first (1 line):** Often yes: modelling `log(y)` stabilises variance and makes multiplicative effects additive, and coefficients read as percentage changes; but `exp(prediction)` estimates the median, not the mean, so I correct the back-transform bias (smearing) if I need the mean.

**Then explain:**
- **Why log:** right-skewed positive targets (price, delivery time) usually have variance growing with the level; the log makes residuals more symmetric and constant-variance, and tames outliers.
- **Interpretation:** with `log(y) = a + b·x`, one unit of x changes y by about `100·b`% (exactly `e^b - 1`). If x is logged too, b is an elasticity.
- **Back-transform bias:** if `log y ~ N(μ, σ²)`, then `E[y] = e^(μ + σ²/2)`, but `e^μ` is the median. So `exp(ŷ_log)` systematically under-predicts the mean. Fixes: Duan's smearing (multiply by the mean of `exp(residuals)`), or the lognormal `e^(σ²/2)` correction, or use a Gamma/Poisson GLM with a log link, which models the mean directly (Q42).
- Only works for y > 0 (use `log1p` for zeros); evaluate in the original units.
- If the business cares about the median or a quantile, the plain exp is fine.

**Example:** y = exp(1 + 0.2x + noise with σ = 0.8). Mean of actual y is 11.98; naive `exp(pred)` averages 8.76 (too low); smearing gives 12.02.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LinearRegression
rng = np.random.default_rng(0); x = rng.uniform(0, 10, (5000, 1))
y = np.exp(1 + 0.2*x[:, 0] + rng.normal(0, .8, 5000))
m = LinearRegression().fit(x, np.log(y)); res = np.log(y) - m.predict(x)
naive = np.exp(m.predict(x)); smear = naive * np.mean(np.exp(res))      # Duan smearing
print(y.mean().round(2), naive.mean().round(2), smear.mean().round(2))   # 11.98 8.76 12.02
```

**Follow-ups:**
- *Why not just fit on y with a robust loss?* Possible, but the log also fixes heteroscedasticity and gives relative-error behaviour.
- *Zero values?* `log1p`, or a two-part/Tweedie model.

**Common mistakes:** Reporting `exp(pred)` as the mean; comparing R² or RMSE across log and raw scales; applying the smearing factor on log-scale errors from the training set only when the model overfits (use CV residuals).

### Q27 ⭐⭐ 🟡 How do you handle high-cardinality categoricals (city, pincode, SKU, user ID)? Compare target encoding, frequency encoding, hashing, embeddings, grouping rare levels.
**Asked at:** Flipkart, Swiggy, Zalando, PhonePe, Booking
**Say this first (1 line):** One-hot is out for thousands of levels, so I pick by model and by how much signal the ID carries: group rare levels, frequency or out-of-fold target encoding for trees and linear models, hashing when the vocabulary is unbounded, and learned embeddings when there is lots of data.

**Then explain:**

| Method | Idea | Good for | Watch out |
|---|---|---|---|
| Group rare levels | Levels with fewer than N rows become `"other"` | First step, always | Loses info on rare but important levels |
| Frequency encoding | Replace level by its share of rows | Trees; quick baseline | Different levels with the same count collide; drifts over time |
| Target encoding | Replace level by smoothed mean of the target | Strong signal, trees and linear | Leaks unless done out-of-fold (Q28) |
| Hashing | `hash(level) mod m` into m columns | Unbounded or streaming vocab, CTR (Q44) | Collisions; no reverse lookup; hurts interpretability |
| Embeddings | Learn a small dense vector per level | Neural nets, lots of data per level | Needs data; cold start for new IDs |

- **Cold start:** unseen levels need a default (global mean, "other" bucket). Plan for it.
- **Hierarchy helps:** pincode to city to state; encode several levels and let the model choose.
- For a **user ID** with few rows each, target encoding is risky; prefer aggregated behaviour features (counts, recency, Q29) instead of the ID itself.
- Keep the vocabulary and mappings fitted on train only and versioned (Q35).

**Example:** 20,000 orders over 2,000 cities (about 10 rows each). Grouping cities with fewer than 10 rows cuts 2,000 levels to 1,065. Hashing into 256 columns gives a fixed-width sparse matrix regardless of how many new cities appear.

**Code:**
```python
import numpy as np, pandas as pd
from sklearn.feature_extraction import FeatureHasher
rng = np.random.default_rng(0)
df = pd.DataFrame({"city": rng.integers(0, 2000, 20000)})
vc = df["city"].value_counts()
freq = df["city"].map(vc / len(df))                           # frequency encoding
grouped = df["city"].where(df["city"].map(vc) >= 10, -1)      # rare -> -1
H = FeatureHasher(n_features=256, input_type="string").transform(
    df["city"].astype(str).map(lambda s: [s]))
print(df.city.nunique(), grouped.nunique(), H.shape)          # 2000 1065 (20000, 256)
```

**Follow-ups:**
- *Trees or linear model?* Trees cope with label-like or frequency codes; linear models need target encoding or embeddings to use the signal, and regularization.
- *Hashing vs one-hot?* Hashing trades a little accuracy (collisions) for fixed memory and no vocabulary.
- *New cities at serving time?* Map to the "other"/global-mean bucket; for embeddings use a shared OOV vector.

**Common mistakes:** Label-encoding nominal IDs for a linear model (invents an order); target encoding without out-of-fold; building the rare-level threshold on the full data; ignoring unseen levels at serving.

### Q28 ⭐⭐ 🟡 How do you do target encoding without leakage (out-of-fold, smoothing)? Why does naive target encoding overfit?
**Asked at:** Product cos, Kaggle-style rounds, fintech
**Say this first (1 line):** Naive target encoding uses each row's own label to build its feature, so the model memorizes the label; I compute the encoding out-of-fold and smooth it toward the global mean, and I fit the final mapping on all training data only for test and serving.

**Then explain:**
- **Why naive overfits:** a level with 1 row gets encoding = its own label (0 or 1). The feature then equals the target on train, so the model trusts it, then fails on new data.
- **Out-of-fold (OOF):** split train into K folds; encode fold k using statistics from the other K-1 folds. A row never sees its own label.
- **Smoothing:** `enc = (sum_y + k·global_mean) / (count + k)`. Small groups are pulled to the global mean; large groups keep their own mean. `k` is a tuning knob (about 10-50).
- **At test/serving:** use the mapping fitted on the whole training set. Do the OOF step inside CV folds too, otherwise validation scores are inflated.
- Optional: add noise, or use CatBoost-style ordered target statistics.

**Example:** Pure-noise target, 1,500 city levels, 2,000 train rows. Naive encoding gives train AUC 0.92 but test AUC 0.51 (chance). OOF plus smoothing gives train AUC 0.52 and test 0.51, so it honestly reports there is no signal.

**Code:**
```python
import numpy as np, pandas as pd
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
df = pd.DataFrame({"c": rng.integers(0, 1500, 4000), "y": rng.integers(0, 2, 4000)})  # noise
tr, te = df.iloc[:2000], df.iloc[2000:]
def enc_map(d, k, g):
    s = d.groupby("c").y.agg(["sum", "count"]); return (s["sum"] + k*g)/(s["count"] + k)
def oof_encode(tr, k=20, folds=5):
    g = tr.y.mean(); oof = np.zeros(len(tr))
    for a, b in KFold(folds, shuffle=True, random_state=0).split(tr):
        oof[b] = tr.iloc[b].c.map(enc_map(tr.iloc[a], k, g)).fillna(g).values
    return oof
g = tr.y.mean()
naive_tr = tr.c.map(tr.groupby("c").y.mean()).values
for name, a, m in [("naive", naive_tr, tr.groupby("c").y.mean()), ("oof+smooth", oof_encode(tr), enc_map(tr, 20, g))]:
    b = te.c.map(m).fillna(g).values
    clf = LogisticRegression().fit(a[:, None], tr.y)
    print(name, round(roc_auc_score(tr.y, clf.predict_proba(a[:, None])[:, 1]), 3),
          round(roc_auc_score(te.y, clf.predict_proba(b[:, None])[:, 1]), 3))
```
Run output (train AUC, test AUC): `naive 0.92 0.508`, `oof+smooth 0.521 0.508`.

**Follow-ups:**
- *How to pick the smoothing k?* Tune by CV on downstream metric; larger k for noisier targets.
- *Does OOF fully remove leakage?* Almost; with time-ordered data use time-based folds so no future labels are used.
- *Alternatives?* Leave-one-out (leaks via the shift it creates), CatBoost ordered encoding, or a mixed-effects model.

**Common mistakes:** Encoding before the train/test split; evaluating CV with an encoder fitted on all folds; no smoothing for rare levels; using leave-one-out encoding, which still leaks because the encoded value shifts with the row's own label.

### Q29 ⭐⭐ 🟡 How do you engineer features from timestamps and recency/frequency data (cyclical encoding, lags, rolling aggregates, RFM)?
**Asked at:** Swiggy, Flipkart, PhonePe, Klarna, fintech
**Say this first (1 line):** I turn a timestamp into calendar parts (cyclical for hour/day), then build per-entity history features (lags, rolling windows, RFM), always using only data from before the prediction time.

**Then explain:**
- **Calendar parts:** hour, day of week, month, weekend, holiday, days to payday or festival.
- **Cyclical encoding:** hour 23 and hour 0 are neighbours, but 23 and 0 as numbers are far apart. Use `sin(2π·h/24)` and `cos(2π·h/24)` together. Trees can often just use the raw hour; linear models and neural nets need the cyclical pair.
- **Lags and rolling aggregates:** previous order amount, mean of the last 3/7/30 days, counts in windows, time since the previous event. **Shift by one** so the current row is excluded.
- **RFM:** Recency (time since last purchase), Frequency (number of purchases in the window), Monetary (total or average spend). Compute them as of a snapshot date.
- **Leakage guard:** features at time t use only events before t; split train/test by time, not randomly.

**Example:** User's orders at 05:00, 06:00, 07:00, 08:00 with amounts 86, 128, 28, 148. At 08:00 the lag-1 is 28 and the rolling-3 mean (excluding the current row) is 80.7 (hand-computed: (86+128+28)/3). Distance between hours 23 and 0 on the sin/cos circle is 0.26; between 23 and 12 it is 1.98.

**Code:**
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(0)
o = pd.DataFrame({"user": rng.integers(0, 5, 2000),
                  "ts": pd.date_range("2024-01-01", periods=2000, freq="h"),
                  "amt": rng.gamma(2, 100, 2000)})
o["hr_sin"] = np.sin(2*np.pi*o.ts.dt.hour/24); o["hr_cos"] = np.cos(2*np.pi*o.ts.dt.hour/24)
o = o.sort_values(["user", "ts"]); g = o.groupby("user")
o["lag1"] = g.amt.shift(1)
o["roll3"] = g.amt.transform(lambda s: s.shift(1).rolling(3, min_periods=1).mean())  # excludes current
o["hrs_since_prev"] = g.ts.diff().dt.total_seconds()/3600
snap = o.ts.max()
rfm = o.groupby("user").agg(recency_h=("ts", lambda s: (snap - s.max()).total_seconds()/3600),
                            frequency=("ts", "size"), monetary=("amt", "sum"))
print(rfm.round(1).head(2))
```
Output rows (user 0, 1): recency 2.0 / 0.0 hours, frequency 381 / 379, monetary 81197.3 / 76566.7.

**Follow-ups:**
- *Why sin and cos, not just sin?* Sin alone maps two different hours to the same value; the pair gives a unique point on the circle.
- *Rolling window leakage?* If the window includes the current row or future rows, the label leaks. Shift first, or use `closed="left"`.
- *Time-based CV?* Yes, expanding or rolling window splits.

**Common mistakes:** Rolling means that include the current row; random train/test split on time data; computing recency relative to today's date rather than the prediction time; treating cyclical features as plain integers in linear models.

### Q30 ⭐⭐ 🟡 Multiclass logistic regression: softmax vs one-vs-rest, and how the loss and gradients change.
**Asked at:** Amazon, Microsoft IDC, GCCs
**Say this first (1 line):** Softmax regression fits all K classes jointly with one probability vector that sums to 1 and a cross-entropy loss; one-vs-rest fits K independent binary models and normalizes afterwards.

**Then explain:**
- **Softmax:** `p_k = exp(z_k) / Σ_j exp(z_j)` with `z_k = w_k·x + b_k`. Loss = `-Σ log p_true` (cross-entropy / negative log-likelihood).
- **Gradient:** for weights of class k, `∂L/∂w_k = (1/n) Σ (p_k − y_k) x`, where `y_k` is the one-hot label. Same "prediction minus target" form as binary logistic regression.
- **OvR:** K binary logistic models, class k vs rest. Each loss is a separate binary log-loss. Scores are not guaranteed to sum to 1; sklearn normalizes them.
- **Softmax is better calibrated** and uses one coherent probability model; OvR is simple, parallel, and fine for many classes or when classes are not mutually exclusive (use multi-label: sigmoid per label).
- Softmax has redundant parameters (adding the same vector to all `w_k` changes nothing); regularization or fixing one class as reference resolves it.
- Use `softmax` stable form: subtract the max logit before `exp`.

**Example:** 4-class synthetic data. Softmax: accuracy 0.761, log loss 0.642. OvR: accuracy 0.747, log loss 0.687. Softmax gives better probabilities.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
X, y = make_classification(3000, 10, n_informative=6, n_classes=4, n_clusters_per_class=1, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
sm = LogisticRegression(max_iter=1000).fit(Xtr, ytr)                         # multinomial softmax
ovr = OneVsRestClassifier(LogisticRegression(max_iter=1000)).fit(Xtr, ytr)
print(round(log_loss(yte, sm.predict_proba(Xte)), 3), round(log_loss(yte, ovr.predict_proba(Xte)), 3))  # 0.642 0.687
# NumPy gradient: (X^T (P - Y)) / n, checked below against a finite difference
W = np.random.default_rng(0).normal(size=(10, 4)); Y = np.eye(4)[ytr]
Z = Xtr @ W; Z -= Z.max(1, keepdims=True); P = np.exp(Z) / np.exp(Z).sum(1, keepdims=True)
G = Xtr.T @ (P - Y) / len(ytr)
nll = lambda W: -np.mean(np.log((lambda Z: np.exp(Z - Z.max(1, keepdims=True)) / np.exp(Z - Z.max(1, keepdims=True)).sum(1, keepdims=True))(Xtr @ W)[np.arange(len(ytr)), ytr]))
E = np.zeros_like(W); E[0, 0] = 1e-6
print(round(G[0, 0], 6), round((nll(W + E) - nll(W - E)) / 2e-6, 6))      # analytic vs finite difference: should match
```

**Follow-ups:**
- *Which does sklearn use by default?* Multinomial softmax for most solvers (in current versions).
- *When OvR?* Huge number of classes with a linear SVM, or when you need to scale/parallelize.
- *Link to neural nets?* The last layer of a classifier is softmax regression on learned features.

**Common mistakes:** Calling softmax probabilities calibrated without checking; forgetting the one-hot target in the gradient; numerically unstable `exp` without subtracting the max; using softmax for multi-label tasks.

### Q31 ⭐⭐ 🟡 Why is logistic regression still widely used in industry (CTR, credit scoring, baseline)? When do you pick it over a tree ensemble?
**Asked at:** Fintech (Klarna, PhonePe), ads, GCCs
**Say this first (1 line):** It is fast, convex, well calibrated, interpretable, easy to audit and serve, and often within a point or two of boosted trees; I pick it when those properties matter more than the last bit of accuracy, and always run it as the baseline.

**Then explain:**
- **Interpretable:** each coefficient is a log-odds effect; regulators (credit scoring, adverse action reasons) accept it, and scorecards (Q39) are built from it.
- **Calibrated probabilities:** it optimizes log loss, so scores are usually close to true probabilities, which matters for pricing and CTR bidding.
- **Cheap and scalable:** trains on billions of sparse rows (feature crosses and hashing, Q44), tiny latency, online updates (SGD/FTRL).
- **Stable and robust:** few hyperparameters, convex so reproducible, less overfit on small data.
- **Pick a tree ensemble when:** strong non-linearities and interactions, mixed/missing data, lots of data, and accuracy beats explainability. Even then, a regularized logistic baseline tells you how much the complexity buys.
- Middle path: add splines/bins/crosses to logistic, or use a GAM with monotonic constraints (Q48).

**Example:** A bank scorecard has 20 binned features and AUC 0.78; a gradient-boosted model reaches 0.80. The 0.02 AUC may not justify losing reason codes and a model-risk review that takes months. (Illustrative numbers, not measured.)

**Follow-ups:**
- *Does logistic regression handle interactions?* Only if you add them; trees find them automatically.
- *Why is it good for CTR?* Huge sparse features, calibrated outputs, and fast online learning.
- *How do you decide objectively?* Cross-validated AUC/log loss gap, plus latency, audit and maintenance costs.

**Common mistakes:** Saying "linear models are always worse"; ignoring calibration and interpretability as selection criteria; skipping a simple baseline before a complex model.

### Q32 ⭐⭐ 🟡 How do you compute feature importance for linear/logistic models (standardized coefficients, permutation importance) and what can go wrong with correlated features?
**Asked at:** Product cos, GCCs, Europe
**Say this first (1 line):** For a linear model I scale the features and compare coefficient sizes, or measure how much the validation metric drops when I shuffle a feature (permutation importance); correlated features break both, because they share or hide each other's credit.

**Then explain:**
- **Standardized coefficients:** standardize X (mean 0, sd 1) and compare `|β|`. Now they are "effect per one standard deviation" and comparable across features. Raw coefficients are not, since they depend on units.
- **Permutation importance:** shuffle one column on validation data, record the metric drop. Model-agnostic and tied to performance.
- **With correlated features:** coefficients are unstable and split arbitrarily (or the sign flips). Permutation importance of each correlated twin is understated, because the model can lean on the other one.
- **Remedies:** group correlated features and permute the group together; drop-column importance with refits; use Lasso/Elastic Net (Q37); report importance for the group, not individuals.
- Importance is not causality, and not the same as statistical significance.

**Example:** `a` and `b` are near copies (b = a + small noise), `c` is independent; the true logit is 1.5·a + 1.0·c. Standardized coefficients: a 1.59, b 0.03, c 0.94. Permutation AUC drop: a 0.224, b about 0, c 0.115. Here `b` looks useless, though it carries exactly the same signal as `a`.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0); n = 3000
a = rng.normal(size=n); b = a + rng.normal(0, .1, n); c = rng.normal(size=n)
X = np.c_[a, b, c]; y = (rng.random(n) < 1/(1+np.exp(-(1.5*a + 1.0*c)))).astype(int)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
sc = StandardScaler().fit(Xtr); m = LogisticRegression(C=100).fit(sc.transform(Xtr), ytr)
print(m.coef_.round(2))                                                          # [[1.59 0.03 0.94]]
r = permutation_importance(m, sc.transform(Xte), yte, scoring="roc_auc", n_repeats=20, random_state=0)
print(r.importances_mean.round(3))                                               # [ 0.224 -0.001  0.115]
```

**Follow-ups:**
- *Scale for binary dummies?* Standardizing dummies is debated; compare them with caution.
- *Train or test for permutation?* Validation/test, so importance reflects generalization.
- *Why not p-values?* Significance tells you the sign is not zero, not how much the feature matters.

**Common mistakes:** Comparing raw coefficients across different units; fitting standardization on the test set; reading small importance for one of a correlated pair as "useless"; treating importance as causal effect.

### Q33 ⭐⭐ 🟡 A coefficient's sign flips or becomes insignificant after adding a variable. What are the possible reasons (collinearity, confounding, omitted variable)?
**Asked at:** Consulting, product cos, Europe
**Say this first (1 line):** A coefficient is the effect of that variable holding the others fixed, so when I add a variable, the meaning changes; the usual causes are omitted-variable bias in the old model, collinearity inflating the standard error, or a suppressor/confounder structure.

**Then explain:**
- **Omitted variable bias:** the first model's coefficient also absorbed the effect of the missing variable (confounder). Adding it corrects (or even flips) the sign.
- **Multicollinearity:** two variables carry similar information, so the model cannot separate them: standard errors blow up, coefficients become unstable, p-values go insignificant even though the pair jointly predicts well. Check VIF and the correlation matrix.
- **Suppressor / Simpson-type effects:** a variable that is positively related to y overall can have a negative partial effect once a stronger driver is controlled for.
- **Bad control:** adding a mediator or a collider can introduce bias rather than remove it, so do not just "add everything".
- **Action:** draw the causal story; check VIF; compare models by out-of-sample performance if the goal is prediction; combine or drop redundant variables; report the joint test (F-test) for the group.

**Example:** Wage = 1.0·education + 2.0·ability + noise, and education correlates with ability. Regressing wage on education alone gives 2.07 (biased up); adding ability gives 0.97. Collinearity example (true y = 2·x1, x2 = x1 + small noise): alone the x1 coefficient is 2.01 with SE 0.04; with x2 included it becomes 2.42 with SE 0.45 (about ten times larger). Suppressor example (true effect of x is −1, but x is correlated with a stronger driver z): simple slope +0.89, partial slope −0.89 once z is controlled for. All numbers come from the code below.

**Code:**
```python
import numpy as np, statsmodels.api as sm
rng = np.random.default_rng(0); n = 500
ability = rng.normal(size=n); edu = 0.8*ability + rng.normal(size=n)
wage = 1.0*edu + 2.0*ability + rng.normal(size=n)
print(sm.OLS(wage, sm.add_constant(edu)).fit().params[1].round(2),
      sm.OLS(wage, sm.add_constant(np.c_[edu, ability])).fit().params[1].round(2))   # 2.07 0.97
x1 = rng.normal(size=n); x2 = x1 + rng.normal(0, .1, n); y = 2*x1 + rng.normal(size=n)   # collinearity
a = sm.OLS(y, sm.add_constant(x1)).fit(); b = sm.OLS(y, sm.add_constant(np.c_[x1, x2])).fit()
print(a.params[1].round(2), a.bse[1].round(2), b.params[1].round(2), b.bse[1].round(2))   # 2.01 0.04 2.42 0.45
z = rng.normal(size=n); x = 0.9*z + rng.normal(0, .5, n); y = -x + 2*z + rng.normal(size=n)   # suppressor
print(sm.OLS(y, sm.add_constant(x)).fit().params[1].round(2), sm.OLS(y, sm.add_constant(np.c_[x, z])).fit().params[1].round(2))   # 0.89 -0.89
```

**Follow-ups:**
- *How do you detect collinearity?* VIF above about 5-10, condition number, unstable coefficients across resamples.
- *Does collinearity hurt prediction?* Not much, unless the correlation structure changes in production; it hurts interpretation.
- *What do you do?* Drop/merge variables, use Ridge/Elastic Net, or add domain knowledge.

**Common mistakes:** Blaming collinearity for every flip; interpreting a coefficient as a causal effect without thinking about confounders; controlling for a mediator; dropping a variable just because its p-value rose.

### Q34 ⭐⭐ 🟡 How do you build and evaluate a text-feature baseline (bag-of-words/TF-IDF + logistic regression)? What regularization works for sparse high-dimensional input?
**Asked at:** Product cos, search/e-commerce
**Say this first (1 line):** Turn text into a sparse TF-IDF matrix (words and bigrams), fit a logistic regression with L2 (or L1/Elastic Net for sparsity), tune `C` by cross-validation, and judge it with the right metric; it is a very strong, cheap baseline before any transformer.

**Then explain:**
- **Bag-of-words / TF-IDF:** count words, then down-weight words that appear in many documents. `sublinear_tf` dampens repeated words; `min_df` drops very rare tokens; add 1-2 grams.
- **Leakage:** fit the vectorizer inside a Pipeline so the vocabulary and IDF come from the training fold only.
- **Regularization:** dimensions >> samples and the data are sparse, so regularize. L2 is the default and works well; L1 gives a short word list (interpretable, smaller model); Elastic Net balances both with correlated words. Tune `C` (inverse strength).
- **Evaluation:** stratified CV; AUC / PR-AUC / F1 depending on class balance; look at top positive/negative words to sanity-check; hold out data by time if the vocabulary drifts.
- Use `liblinear` or `saga` solvers for sparse data.

**Example:** For reviews, words like "refund" and "broke" would typically get large negative weights and "love" positive; you can print the top 20 each way to explain the model to the business. The code below uses a tiny synthetic toy corpus (6 sentences repeated) only to show the pipeline; its cross-validated AUC of 1.0 is an artefact of that toy data, not a result.

**Code:**
```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
pos = ["great product loved it", "excellent quality fast delivery", "very happy works great"]
neg = ["terrible product broke quickly", "poor quality late delivery", "very unhappy stopped working"]
rng = np.random.default_rng(0)
docs = [(pos if i % 2 == 0 else neg)[rng.integers(0, 3)] + " " + " ".join(rng.choice(["the", "a", "item", "order"], 2)) for i in range(400)]
y = np.array([1 - i % 2 for i in range(400)])
p = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True),
                  LogisticRegression(C=1.0, max_iter=1000))
print(cross_val_score(p, docs, y, cv=5, scoring="roc_auc").mean().round(3))
# TOY corpus: 6 hand-written sentences repeated, trivially separable, so AUC = 1.0 means nothing.
# It only shows the pipeline runs. Real text is much harder: never quote this number as a result.
```

**Follow-ups:**
- *TF-IDF vs embeddings?* Embeddings capture meaning and synonyms; TF-IDF is transparent, quick and strong when keywords matter. Try both (Q46).
- *Why not Naive Bayes?* NB-style baselines are also good; logistic usually wins as data grows.
- *Class imbalance?* `class_weight`, PR-AUC, threshold tuning.

**Common mistakes:** Fitting TF-IDF on all data before CV; accuracy on imbalanced text; no regularization tuning; leaving tokens like IDs/names that leak the label.

### Q35 ⭐⭐ 🟡 Training-serving skew for features: how do you ensure the same transformations run offline and online?
**Asked at:** Product cos, MLE roles, Amazon
**Say this first (1 line):** Training-serving skew means the model sees differently computed features online than it saw in training; I prevent it by defining each feature once (one code path or a feature store), shipping the fitted transformer together with the model, and monitoring live feature distributions against training.

**Then explain:**
- **Causes:** two codebases (SQL/Spark offline vs Java/Python online), different null/default handling, different time windows or timezones, stale or late data, unseen categories, library version changes, and point-in-time leakage (offline uses future data that is not available online).
- **Fixes:**
  - **One definition:** a feature store (Feast, Tecton, SageMaker/Vertex feature stores) or shared feature library used by both batch and online paths.
  - **Fitted pipeline as one artifact:** scaler, encoders, imputers and model saved together (sklearn `Pipeline`, ONNX, MLflow) and versioned.
  - **Point-in-time correct joins** when building training data.
  - **Log features at serving time** and train on the logged values when possible ("log and replay").
  - **Tests:** parity test, run the same raw rows through offline and online code and assert equal features; unit tests for nulls and unseen levels.
  - **Monitoring:** per-feature drift (PSI, KS), null rates, and schema checks with alerts.
- Skew (code/data mismatch) differs from **drift** (the world changes); both are monitored but fixed differently.

**Example:** A single saved pipeline (scaler plus one-hot with `handle_unknown="ignore"` plus logistic regression) is reloaded in the "serving" process: predictions on the training rows are identical to the original (`allclose` is True), and an unseen city "Z" returns a valid probability (0.49) instead of crashing.

**Code:**
```python
import numpy as np, pandas as pd, joblib, io
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(0); n = 1000
df = pd.DataFrame({"amt": rng.gamma(2, 100, n), "city": rng.choice(["A", "B", "C"], n)})
y = (rng.random(n) < 1/(1+np.exp(-(df.amt/200 - 1 + (df.city == "A"))))).astype(int)
pipe = make_pipeline(make_column_transformer((StandardScaler(), ["amt"]),
                     (OneHotEncoder(handle_unknown="ignore"), ["city"])), LogisticRegression()).fit(df, y)
buf = io.BytesIO(); joblib.dump(pipe, buf); buf.seek(0); served = joblib.load(buf)   # ship ONE artifact
req = pd.DataFrame({"amt": [150.0], "city": ["Z"]})                                  # unseen category
print(served.predict_proba(req)[0, 1].round(3), np.allclose(pipe.predict_proba(df), served.predict_proba(df)))  # 0.49 True
```

**Follow-ups:**
- *Batch vs real-time features?* Real-time ones (last 5 minutes) are hardest; compute with streaming (Flink/Kafka) using the same logic, and keep a fallback for late data.
- *How do you detect skew?* Compare distributions of logged online features with the training set; monitor null rates and out-of-range values.
- *Library versions?* Pin them; an sklearn upgrade can change a pickled pipeline's behaviour.

**Common mistakes:** Re-implementing feature logic in a second language "by hand"; saving the model but not the preprocessor; ignoring unseen categories and nulls; training with features that use data not available at prediction time.

### Q36 ⭐⭐ 🟡 AI-era: an LLM generated this sklearn pipeline (scaler fit on full data, target encoding before split, p-value-based feature dropping). Review it and list the bugs.
**Asked at:** AI-era code-review rounds, product cos, GCCs
**Say this first (1 line):** The code has two leaks (scaler and target encoder fit before the split) and also uses p-values for feature selection, so its reported score is optimistic and its feature set is unreliable; the fix is one `Pipeline` fitted on training folds only.

**Buggy snippet (typical LLM output):**
```python
df["city_te"] = df.city.map(df.groupby("city").y.mean())            # bug 1
X = StandardScaler().fit_transform(df[["city_te", "x1", "x2"]])      # bug 2
Xtr, Xte, ytr, yte = train_test_split(X, df.y, random_state=0)
# bug 3: fit OLS/Logit on Xtr, drop features with p > 0.05, refit, report score
```

**Then explain (the bugs):**
- **Target encoding before the split:** every row's own label is inside its encoding, so test labels leak into the features (Q28).
- **Scaler fit on all data:** test mean/std leak into training. Small effect usually, but wrong in principle and in production.
- **P-value feature dropping:** p-values describe in-sample association, not predictive value; dropping after peeking at the data invalidates later p-values (Q47), is unstable with correlated features, and is not tied to a validation metric. Use CV-based selection or L1/Elastic Net inside the pipeline.
- Also check: no group/time split when rows repeat per user, no unseen-category handling, metric reported on data used for selection, `random_state` unset.

**Example:** On a target with no signal at all (random labels, 600 city levels), the buggy pipeline reports test AUC 0.763. The fixed pipeline reports CV AUC 0.504 and test AUC 0.502, which is the truth.

**Fixed code:**
```python
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, TargetEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0); n = 3000
df = pd.DataFrame({"city": rng.integers(0, 600, n).astype(str), "x1": rng.normal(size=n),
                   "x2": rng.normal(size=n), "y": rng.integers(0, 2, n)})        # no real signal
Xtr, Xte, ytr, yte = train_test_split(df[["city", "x1", "x2"]], df.y, random_state=0)
ct = make_column_transformer((TargetEncoder(smooth="auto", random_state=0), ["city"]),
                             (StandardScaler(), ["x1", "x2"]))
pipe = make_pipeline(ct, LogisticRegression())               # all fitting happens inside CV folds
print(cross_val_score(pipe, Xtr, ytr, cv=5, scoring="roc_auc").mean().round(3))   # 0.504
print(round(roc_auc_score(yte, pipe.fit(Xtr, ytr).predict_proba(Xte)[:, 1]), 3))   # 0.502
```

**Follow-ups:**
- *Does sklearn's TargetEncoder avoid leakage?* Its `fit_transform` uses internal cross-fitting; `transform` on new data uses the full-train mapping.
- *How to catch such bugs?* Sanity check with shuffled labels: a score far above chance means leakage.
- *Would you trust LLM-written pipelines?* Use them as drafts; review splits, fitted objects, and metrics.

**Common mistakes:** Only fixing the scaler and missing the target encoder; keeping p-value selection but moving it inside the pipeline without validation; reporting the tuned CV score as the final estimate.

### Q37 ⭐⭐ 🔴 How does Lasso behave with correlated features, and how do Elastic Net or stability selection address it?
**Asked at:** Product cos, C3 AI-type, research-leaning roles
**Say this first (1 line):** With a group of highly correlated features, Lasso tends to pick one arbitrarily and zero the others, and the pick changes between samples; Elastic Net spreads weight across the group, and stability selection reports how often each feature is chosen across resamples.

**Then explain:**
- **Why Lasso does this:** the L1 penalty is the same whichever twin carries the weight, so the solution is not unique or stable; it needs only one representative of the signal.
- **Elastic Net:** adds an L2 term (`α·[ρ‖β‖₁ + (1−ρ)/2·‖β‖₂²]`). The L2 part rewards sharing, giving the "grouping effect": near-identical features get near-equal coefficients. Still sparse.
- **Stability selection:** fit Lasso on many random half-samples (and possibly random penalty weights); keep features chosen in, say, more than 70-90% of fits. It controls false selections and reveals unstable choices.
- Also: Lasso picks at most n features when p > n; **irrepresentable condition** is needed for exact support recovery.
- If you want to select groups, use Group Lasso, or cluster features first.

**Example:** Three near-copies of z (true signal 3·z), plus three noise features, n = 200. Lasso: `[0, 1.17, 1.57, 0, 0, 0]`, weight on two twins. Elastic Net: `[0.89, 0.93, 0.93, 0, 0, 0]`, shared evenly. Stability selection frequencies for Lasso (100 half-samples): `[0.06, 0.90, 0.90, 0, 0, 0]`. Noise is never chosen, and the three twins are not treated alike: twin 1 is almost always dropped while twins 2 and 3 are each kept 90% of the time, yet nothing in the data says twin 1 is worse (each twin is just z plus tiny noise). A frequency well below 1 for a feature that carries the same signal is the warning that Lasso's choice within the group is arbitrary. (One simulated run, not a general law.)

**Code:**
```python
import numpy as np
from sklearn.linear_model import Lasso, ElasticNet
rng = np.random.default_rng(0); n = 200; z = rng.normal(size=n)
X = np.c_[z + rng.normal(0, .05, n), z + rng.normal(0, .05, n), z + rng.normal(0, .05, n), rng.normal(size=(n, 3))]
y = 3*z + rng.normal(0, 1, n)
print(Lasso(alpha=.3).fit(X, y).coef_.round(2))                       # [0. 1.17 1.57 0. 0. 0.]
print(ElasticNet(alpha=.3, l1_ratio=.3).fit(X, y).coef_.round(2))     # [0.89 0.93 0.93 0. 0. 0.]
sel = np.zeros(6)
for _ in range(100):                                                  # stability selection
    i = rng.choice(n, n//2, replace=False); sel += Lasso(alpha=.3).fit(X[i], y[i]).coef_ != 0
print((sel/100).round(2))                                             # [0.06 0.9 0.9 0. 0. 0.]
```

**Follow-ups:**
- *Why not just Ridge?* Ridge never zeros features; use it when you want all variables, Elastic Net when you want sparsity plus stability.
- *Which l1_ratio?* Tune by CV (`ElasticNetCV`); near 0.5 is a common start.
- *Does Lasso selection equal truth?* Not guaranteed; it is a predictive tool, see Q47 for inference.

**Common mistakes:** Interpreting "Lasso dropped it" as "irrelevant"; not standardizing features before regularization; picking `alpha` on the test set; ignoring instability across resamples.

### Q38 ⭐⭐ 🔴 What is perfect (quasi-)separation in logistic regression? What happens to the coefficients and how do you fix it?
**Asked at:** Fintech, GCCs, statistics-heavy roles
**Say this first (1 line):** Separation means some feature (or combination) splits the classes perfectly, so the likelihood keeps improving as the coefficient grows and the maximum-likelihood estimate does not exist; coefficients blow up and standard errors become meaningless, and I fix it with regularization, Firth's penalty, or by removing or coarsening the offending feature.

**Then explain:**
- **Why:** if `x > t` always means `y = 1`, pushing `β → ∞` drives predicted probabilities to exactly 0 and 1 and log loss to 0. There is no finite maximum.
- **Symptoms:** huge coefficients, enormous standard errors, warnings (non-convergence, "perfect separation"), probabilities of 0/1, Wald p-values near 1.
- **Quasi-separation:** separation except for a few tied points, or a sparse category (rare level with only one outcome). Common with one-hot rare levels and small samples.
- **Fixes:** L2 or L1 regularization (finite solution); **Firth's penalized likelihood** (bias-reduced, finite, gives sensible estimates for inference); Bayesian weakly informative prior; merge rare categories or drop/bin the feature; get more data.
- First ask whether the feature is a leak (a proxy for the label, e.g. "account closed" predicting churn).

**Example:** Two classes drawn from N(−3,1) and N(3,1), 200 points, fully separable. sklearn with `C=1`: coefficient 2.36; `C=100`: 5.49; `C=10,000`: 7.02, and it would keep growing with weaker regularization. statsmodels `Logit` (unpenalized) returns arbitrarily large estimates with astronomically large standard errors (in one run, a slope near 60 with SE around 10^12), and a perfect-separation warning or error depending on the version; the exact numbers are meaningless.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(0)
x = np.r_[rng.normal(-3, 1, 100), rng.normal(3, 1, 100)][:, None]; y = np.r_[np.zeros(100), np.ones(100)]
print("separable:", x[y == 0].max() < x[y == 1].min())                 # True
for C in [1, 1e2, 1e4]:
    print(C, LogisticRegression(C=C, max_iter=10000).fit(x, y).coef_.round(2))   # 2.36, 5.49, 7.02
```

**Follow-ups:**
- *Is it a problem for prediction?* Often not for ranking, but probabilities are overconfident and inference is invalid; also unstable out of sample.
- *Firth in Python?* Not in sklearn/statsmodels core; use the `firthlogist` package, or R's `logistf`.
- *Does it happen with many features?* Yes, when p is large relative to n, data are almost always separable; regularization is then mandatory.

**Common mistakes:** Trusting the huge coefficient and p-value; "fixing" it by raising `max_iter`; dropping the warning; not checking if the separating variable is a leak.

### Q39 ⭐⭐ 🔴 How do you do Weight of Evidence binning and Information Value for logistic scorecards, and what are the pitfalls?
**Asked at:** Klarna, JPMC, Amex, fintech GCCs
**Say this first (1 line):** I bin each feature, compute for each bin the Weight of Evidence (log of good share over bad share), replace the feature with its WoE, and use Information Value to rank how predictive the feature is; the logistic model on WoE features becomes a scorecard.

**Then explain:**
- **WoE per bin:** `ln(%good / %bad)` where `%good` is the bin's share of all goods. Positive WoE means safer than average, negative riskier. (Some teams define it as bad/good; fix the sign convention and state it.)
- **IV per feature:** `Σ (%good − %bad) · WoE`. Rule of thumb: < 0.02 useless, 0.02-0.1 weak, 0.1-0.3 medium, 0.3-0.5 strong, > 0.5 suspicious (check leakage).
- **Why WoE:** puts every feature on the log-odds scale, handles missing as its own bin, handles outliers, makes the relationship monotone and the model easy to explain.
- **Binning rules:** enough rows per bin (about 5% of data), non-zero goods and bads in each bin, monotone WoE where business logic expects it, bins stable over time.
- **Pitfalls:** fit the bins on training data only; IV favors many bins (overfits); zero-count bins give infinite WoE (add smoothing); WoE of a target-related feature leaks like target encoding (Q28); drift of bins over time (monitor PSI); IV measures univariate strength, not value after other variables.

**Example:** 20,000 loans, age in 5 equal-frequency bins. WoE goes from −0.449 (youngest, riskiest) to +0.617 (oldest). IV = 0.148, a medium-strength predictor.

**Code:**
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(0); n = 20000
age = rng.integers(18, 70, n); p = 1/(1+np.exp(-(1.2 - 0.045*(age-18))))*0.5
df = pd.DataFrame({"age": age, "y": (rng.random(n) < p).astype(int)}); df["bin"] = pd.qcut(df.age, 5)
g = df.groupby("bin", observed=True).y.agg(bad="sum", n="count"); g["good"] = g.n - g.bad
g["woe"] = np.log((g.good/g.good.sum()) / (g.bad/g.bad.sum()))
g["iv"] = (g.good/g.good.sum() - g.bad/g.bad.sum()) * g.woe
print(g[["woe", "iv"]].round(3)); print("IV", g.iv.sum().round(3))     # IV 0.148
```

**Follow-ups:**
- *Why not one-hot bins?* WoE gives one monotone column per feature and a compact scorecard, and handles rare/missing bins.
- *How is the score scaled?* Points = offset + factor · log-odds (e.g. 20 points to double the odds).
- *Monitoring?* Population Stability Index per feature and score; recalibrate on drift.

**Common mistakes:** Computing WoE/IV on the full data (leakage); too many bins; ignoring non-monotone bins; using IV above 0.5 without checking for a leak; dropping features on IV alone without looking at correlation between them.

### Q40 ⭐ 🟢 How do linear models treat ordinal, nominal and binary features differently from tree models?
**Asked at:** GCCs, analytics roles
**Say this first (1 line):** A linear model assumes numbers mean something, so it needs nominal features one-hot encoded and ordinal ones either treated as numeric (if spacing is roughly even) or as dummies; trees only compare thresholds, so they are fine with integer codes for ordinals and care about order, not spacing.

**Then explain:**

| Feature | Linear/logistic model | Tree model |
|---|---|---|
| **Binary** (0/1) | Use directly; coefficient is the shift between the two groups | Single split |
| **Nominal** (city, colour) | One-hot (drop one level or regularize); label codes invent a fake order | One-hot works; label codes work but are crude; native categorical support in LightGBM/CatBoost |
| **Ordinal** (low/med/high, rating 1-5) | Numeric code assumes equal steps; dummies or splines drop that assumption | Integer code is fine; monotone transform does not matter |
| **Numeric** | Scale for regularized models; non-linear effects need transforms | Scale-free, handles non-linearity |

- **Dummy trap:** one-hot with an intercept makes columns sum to 1 (perfect collinearity). Drop one level (reference) or use regularization.
- **Trees and one-hot of high cardinality:** splits get diluted; prefer target/frequency encodings (Q27).
- **Ordinal as numeric** is a modelling choice: check if the average outcome rises roughly linearly across levels.

**Example:** Satisfaction 1-5 vs churn. Treat as numeric if churn falls about equally per step; use 4 dummies if the biggest drop is between 1 and 2 only. A tree with the integer code finds the right split automatically.

**Follow-ups:**
- *Label encoding a nominal variable in a linear model?* It forces city 3 to be "between" city 2 and city 4. Avoid.
- *One-hot in Ridge/Lasso?* Do not drop a level if you want symmetric shrinkage; keep all and let the penalty handle it.
- *Interactions?* Linear models need them added by hand; trees get them from depth.

**Common mistakes:** Label-encoding nominal columns for logistic regression; treating ordinal as nominal and throwing away order (loses power); dummy variable trap in unregularized OLS; scaling one-hot columns without thinking about it.

### Q41 ⭐ 🟡 What is p > n (high-dimensional) regression, why does OLS fail, and what are your options?
**Asked at:** Research-leaning, genomics/health, Europe
**Say this first (1 line):** When there are more features than rows, OLS has infinitely many perfect-fit solutions, so it memorizes the training data and generalizes badly; I use regularization (Ridge, Lasso, Elastic Net), dimension reduction (PCA/PLS), or screening before modelling.

**Then explain:**
- **Why OLS fails:** `XᵀX` is p×p with rank at most n < p, so it is singular and the solution is not unique. Software returns one of many (often the minimum-norm one) that fits training data exactly (R² = 1) but has high variance.
- **Ridge:** adds `λ‖β‖²`, makes the problem well-posed, shrinks all coefficients; good when many small effects.
- **Lasso / Elastic Net:** sparse solutions; Lasso selects at most n features; Elastic Net handles correlated groups (Q37).
- **PCA / PLS:** regress on a few components (Q45).
- **Screening / domain knowledge:** pre-filter by univariate association (inside CV!), or use priors/pathway info.
- **Validate carefully:** nested CV, small n gives noisy estimates; selection must happen inside folds.

**Example:** n = 60, p = 200, only 5 features matter (coefficient 2). OLS: train R² 1.00, test R² 0.20. Ridge: test R² 0.21. Lasso (CV): test R² 0.91, with 31 non-zero coefficients.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV
from sklearn.metrics import r2_score
rng = np.random.default_rng(0); n, p = 60, 200
X = rng.normal(size=(n+500, p)); b = np.zeros(p); b[:5] = 2
y = X @ b + rng.normal(size=n+500)
Xtr, ytr, Xte, yte = X[:n], y[:n], X[n:], y[n:]
for name, m in [("ols", LinearRegression()), ("ridge", RidgeCV(alphas=np.logspace(-1, 4, 20))), ("lasso", LassoCV(cv=5, random_state=0))]:
    m.fit(Xtr, ytr); print(name, round(r2_score(ytr, m.predict(Xtr)), 2), round(r2_score(yte, m.predict(Xte)), 2))
# ols 1.0 0.2 | ridge 0.99 0.21 | lasso 0.97 0.91
```

**Follow-ups:**
- *Why does Ridge do worse than Lasso here?* The truth is sparse (5 of 200); Ridge spreads weight across all features. With many small true effects, Ridge wins.
- *Degrees of freedom?* OLS uses all n; Ridge's effective df is smaller (Q50).
- *Can you do inference?* Naive p-values are invalid after selection (Q47); use debiased Lasso or sample splitting.

**Common mistakes:** Selecting features on the full data before CV (huge optimism); trusting training R²; using OLS with `pinv` and believing the coefficients; not standardizing before penalized regression.

### Q42 ⭐ 🟡 Poisson, Tweedie and Gamma GLMs: when would you use them instead of OLS (counts, claims, ETA, demand)?
**Asked at:** Insurance, delivery/ETA, pricing, Booking
**Say this first (1 line):** Use a GLM when the target is not Gaussian: Poisson for counts, Gamma for positive skewed amounts or durations, Tweedie for non-negative data with many exact zeros (claims cost); they model the mean through a log link, so predictions stay positive and variance matches the data.

**Then explain:**
- **Poisson (log link):** counts (orders per hour, claims per policy). Variance equals the mean. If variance is bigger (overdispersion), use quasi-Poisson or negative binomial. Use an **offset** `log(exposure)` for rates.
- **Gamma (log link):** positive continuous, right-skewed, variance proportional to mean squared (constant coefficient of variation): ETA, claim severity, price.
- **Tweedie (power 1 < p < 2):** compound Poisson-Gamma; a point mass at zero plus a skewed positive part; models pure premium (frequency × severity) in one model.
- **Why not OLS:** it can predict negative values, assumes constant variance, and a log-link GLM gives multiplicative effects (`e^β`) which fit business questions ("+8% per unit").
- **Fit** by maximum likelihood (IRLS); evaluate with deviance and in original units.

**Example:** Counts with mean `exp(0.5 + 0.8x)`. Poisson recovers slope 0.78 (true 0.8), predictions always positive (min 0.08); OLS predictions go as low as −4.6. Gamma on skewed positive data: slope 0.80. Tweedie (power 1.5) with 70% zeros: slope 0.81 (simulated data, true slope 0.8; code below).

**Code:**
```python
import numpy as np
from sklearn.linear_model import PoissonRegressor, LinearRegression
rng = np.random.default_rng(0); n = 5000
x = rng.normal(size=(n, 1)); mu = np.exp(0.5 + 0.8*x[:, 0]); y = rng.poisson(mu)
po = PoissonRegressor(alpha=0).fit(x, y); ols = LinearRegression().fit(x, y)
print(po.coef_.round(2), po.predict(x).min().round(2), ols.predict(x).min().round(2))   # [0.78] 0.08 -4.6
from sklearn.linear_model import GammaRegressor, TweedieRegressor
yg = rng.gamma(2, mu/2); print(GammaRegressor(alpha=0).fit(x, yg).coef_.round(2))               # [0.8]
yt = np.where(rng.random(n) < 0.7, 0, rng.gamma(2, mu))                                        # 70% exact zeros
print(TweedieRegressor(power=1.5, link="log", alpha=0).fit(x, yt).coef_.round(2))              # [0.81]
```

**Follow-ups:**
- *How do you pick the Tweedie power?* Profile the likelihood or CV on deviance.
- *Why offset?* So that doubling exposure doubles the expected count; coefficients are then about the rate.
- *Log-transform OLS vs Gamma GLM?* Log-OLS models median-like behaviour and needs a smearing correction (Q26); Gamma GLM models the mean directly.

**Common mistakes:** Poisson on overdispersed data and trusting the standard errors; forgetting exposure; applying OLS to counts and clipping at zero; comparing GLMs by R² instead of deviance.

### Q43 ⭐ 🟡 What is quantile regression and when is it preferred to OLS (SLA, ETA P90, pricing)?
**Asked at:** Swiggy, Uber-style, Booking, Europe
**Say this first (1 line):** Quantile regression models a chosen percentile of the target given the features (for example the 90th percentile of delivery time) by minimizing the asymmetric "pinball" loss, so I use it when the business cares about the tail or the spread, not just the average.

**Then explain:**
- **Pinball loss at quantile q:** `max(q·e, (q−1)·e)` with `e = y − ŷ`. Under-predictions cost `q`, over-predictions cost `1−q`. For q = 0.5 it is absolute error, i.e. median regression.
- **Why not OLS:** OLS gives the conditional mean; if noise grows with x (heteroscedastic) or the target is skewed, the mean says little about the tail.
- **Use cases:** ETA P90 ("promise a time you meet 90% of the time"), SLA planning, inventory (safety stock), pricing bands, prediction intervals (fit q = 0.05 and 0.95), robustness (median).
- **Properties:** no distribution assumption; robust to y outliers; separate model per quantile; quantiles can **cross** (fix by sorting/monotone constraints); available in sklearn, statsmodels, LightGBM (`objective="quantile"`).
- **Check:** coverage, the share of actuals below the predicted quantile, should be close to q.

**Example:** `y = 5 + 2x + noise·0.5x`, so spread grows with x. OLS slope 1.98 (average effect). Median 1.97. The 90th-percentile line has slope 2.67 and coverage 0.90: the tail grows faster than the mean, which only quantile regression shows.

**Code:**
```python
import numpy as np
from sklearn.linear_model import QuantileRegressor
rng = np.random.default_rng(0); n = 2000
x = rng.uniform(1, 10, (n, 1)); y = 5 + 2*x[:, 0] + rng.normal(0, 1, n)*x[:, 0]*0.5
for q in [.5, .9]:
    m = QuantileRegressor(quantile=q, alpha=0, solver="highs").fit(x, y)
    print(q, m.coef_.round(2), (y <= m.predict(x)).mean().round(3))   # 0.5 [1.97] 0.5 | 0.9 [2.67] 0.9
```

**Follow-ups:**
- *Why not predict the mean and add a buffer?* Only valid if the spread is constant; here it is not.
- *Evaluation?* Pinball loss and coverage; for intervals also width (see conformal prediction for guarantees).
- *Quantile crossing?* Fit jointly or rearrange so predictions are monotone in q.

**Common mistakes:** Reporting RMSE for a quantile model; not checking coverage; assuming quantile predictions from different models are consistent; using OLS ± 1.28 sd when errors are skewed.

### Q44 ⭐ 🟡 Feature crosses and hashing at scale in linear CTR models: why do ads systems still use them?
**Asked at:** Ads teams, Flipkart, Amazon, Spotify
**Say this first (1 line):** CTR data is huge, sparse and categorical, so a logistic model over one-hot features plus hashed feature crosses trains on billions of rows, serves in microseconds, gives calibrated probabilities, and can be updated online; crosses give it the interactions it would otherwise miss.

**Then explain:**
- **Feature cross:** a new categorical feature from two or more, for example `user_city × ad_category`. A linear model on the cross learns "Pune users like this ad type", an interaction the separate features cannot express.
- **Hashing trick:** map each (cross) string to one of `2^k` buckets. No vocabulary to store, new values handled automatically, fixed memory. Cost: collisions (usually tolerable with large k) and no easy reverse lookup.
- **Why linear still wins at scale:** convex (stable), calibrated probabilities that feed auctions (bid = pCTR × value), fast online training (SGD, FTRL-Proximal with L1 for sparse weights), cheap serving, easy debugging.
- **Memorization vs generalization:** crosses memorize frequent specific combinations; deep parts (embeddings) generalize to unseen ones. Wide & Deep, DeepFM and DCN combine both, but still keep the wide/cross part.
- **Practicalities:** regularize heavily (L1 or L2), filter rare crosses, monitor calibration and drift, handle position bias.

**Example:** `user_id × ad_id` has billions of combinations. Hash into 2^24 buckets (16.7 million weights): memory is fixed at 64 MiB in float32 (16.7M x 4 bytes), and a never-seen pair still maps to some bucket.

**Follow-ups:**
- *What about collisions?* Different crosses sharing a weight add noise; use larger k, or two hash functions; the loss is small compared with the gain.
- *Why not trees?* They struggle with very high-cardinality sparse IDs and online learning at this scale.
- *Why not only deep models?* They are used, but linear/wide parts remain for memorization, latency and calibration.

**Common mistakes:** Crossing everything (explodes size, overfits); no regularization on rare crosses; using non-stable hashes between training and serving (Q35); ignoring calibration drift.

### Q45 ⭐ 🟡 Principal-component regression vs Ridge vs PLS: when would you choose each?
**Asked at:** Research-leaning, GCC analytics
**Say this first (1 line):** All three fight many correlated predictors: Ridge shrinks every direction smoothly, PCR keeps only the top-variance components (ignoring y when choosing them), and PLS picks components that also covary with y; my default is Ridge, and I reach for PLS when the signal is not in the high-variance directions and I want few components.

**Then explain:**
- **Ridge:** keeps all features, shrinks directions with small variance most. Strong default, one tuning knob (λ), no component selection.
- **PCR:** PCA first (unsupervised), then OLS on k components. Assumes the directions that vary most are the ones that predict y; it fails when the signal sits in a low-variance direction.
- **PLS:** builds components that maximize covariance with y (supervised). Needs fewer components than PCR; popular in chemometrics, with multiple correlated y's. Can overfit if k is large.
- **Choosing:** tune λ or k by CV. If you need interpretation via a few latent factors, PLS/PCR; if you need best predictions with p large, Ridge (or Elastic Net).
- Standardize features first for all three.

**Example:** 50 features generated from 5 latent factors, y driven by the 5th principal component (low variance). CV R²: PCR with 2 components -0.03, PCR with 5 components 0.90, PLS with 1 component 0.73, PLS with 2 components 0.88, Ridge 0.89. PCR needed to guess the right k; PLS found the direction by itself.

**Code:**
```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import PLSRegression
from sklearn.linear_model import RidgeCV, LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
rng = np.random.default_rng(0); n, p = 300, 50
F = rng.normal(size=(n, 5)); L = rng.normal(size=(5, p)) * np.array([[3], [2.5], [2], [1.5], [1]])
X = F @ L + rng.normal(0, .5, (n, p)); Xc = X - X.mean(0)
Vt = np.linalg.svd(Xc, full_matrices=False)[2]
y = Xc @ Vt[4] * 0.5 + rng.normal(0, 1, n)                  # signal in the 5th PC
mods = {"pcr2": make_pipeline(PCA(2), LinearRegression()), "pcr5": make_pipeline(PCA(5), LinearRegression()),
        "pls1": PLSRegression(1), "pls2": PLSRegression(2), "ridge": RidgeCV(alphas=np.logspace(-2, 3, 20))}
print({k: round(float(cross_val_score(v, X, y, cv=5, scoring="r2").mean()), 2) for k, v in mods.items()})
# {'pcr2': -0.03, 'pcr5': 0.9, 'pls1': 0.73, 'pls2': 0.88, 'ridge': 0.89}
```

**Follow-ups:**
- *Ridge as soft PCR?* Yes: Ridge shrinks component k's coefficient by `d_k²/(d_k²+λ)`; PCR keeps or drops it hard.
- *Is PCA before regression leakage?* Only if fitted on all data before CV; put it in the pipeline.
- *Interpretability?* Components are mixtures of all features; loadings help but are harder than Lasso.

**Common mistakes:** Picking PCA components by variance and assuming they predict y; not scaling features; running PCA on train+test; forgetting that PCR/PLS still need CV for k.

### Q46 ⭐ 🟡 Does feature engineering still matter in the LLM/embeddings era? How would you use embeddings as features in a regularized linear model?
**Asked at:** AI-era DS loops, Spotify, Zalando, Klarna
**Say this first (1 line):** Yes, it still matters: embeddings replace hand-crafted features for text and images, but for tabular business data the signal is in domain features (recency, ratios, aggregates, leakage-safe joins), and the best systems combine both, feeding embeddings as extra, strongly regularized features.

**Then explain:**
- **What embeddings replace:** TF-IDF, manual text/image descriptors, hand-built item similarity. They give dense semantic vectors from a pretrained model.
- **What they do not replace:** time windows, per-entity aggregates, business ratios, correct train/serve logic, target definition, leakage control. LLMs do not know your event data.
- **Using them in a linear model:** standardize, feed the vector (256-1024 dims) alongside tabular features, use strong L2 (small `C`) or Elastic Net, and tune by CV. Optionally reduce with PCA first. Cosine similarity between embeddings (query-item, user-item) is a compact, useful feature.
- **Watch:** embedding model version drift (re-embed everything on upgrade), dimension >> samples (regularize), cost/latency of embedding at serve time, privacy of text sent to external APIs.
- **Check value honestly:** compare with and without the embeddings on a time-based split.

**Example:** Synthetic random vectors (not real embeddings), 600 rows, 256 dims plus 3 tabular features, where only 10 dims carry a weak signal. With weak regularization (C = 100) CV AUC is 0.662; with strong regularization (C = 0.01) 0.709; the 3 tabular features alone give a similar 0.695. So the honest lesson of this demo is only that a high-dimensional block overfits unless regularized; it does not show that embeddings add value, and the differences are within CV noise. On a real project you must run the with/without comparison on your own data.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
rng = np.random.default_rng(0); n, d = 600, 256
E = rng.normal(size=(n, d)); w = np.zeros(d); w[:10] = .6; tab = rng.normal(size=(n, 3))
y = (rng.random(n) < 1/(1+np.exp(-(E @ w * .5 + tab[:, 0])))).astype(int)
X = np.c_[E, tab]
for C in [100, 1, .01]:
    p = make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=2000))
    print(C, cross_val_score(p, X, y, cv=5, scoring="roc_auc").mean().round(3))   # 0.662 0.667 0.709
print("tabular only", cross_val_score(make_pipeline(StandardScaler(), LogisticRegression()), tab, y, cv=5, scoring="roc_auc").mean().round(3))
```

**Follow-ups:**
- *Fine-tune the embedding model or freeze it?* Start frozen plus linear head (cheap, stable); fine-tune if you have enough labels and a gap.
- *Why not an LLM for tabular prediction?* Usually worse and costlier than gradient boosting on structured data; use it for text fields.
- *How to avoid leakage with embeddings?* Embeddings from a pretrained model are fixed; leakage comes from how you build the labels and joins.

**Common mistakes:** Dumping 1024 dims into an unregularized model; claiming embeddings make feature engineering obsolete; ignoring embedding version changes between training and serving; not comparing against a simple TF-IDF/tabular baseline.

### Q47 ⭐ 🟡 How do you do inference (p-values, CIs) after Lasso selection, and why are naive p-values invalid?
**Asked at:** Statistics-heavy roles, Europe research
**Say this first (1 line):** Naive p-values after Lasso are invalid because the data chose which features to test, so the winners look more significant than they are; valid options are sample splitting, post-selection (selective) inference, or the debiased Lasso.

**Then explain:**
- **Why naive fails:** Lasso keeps features that happen to correlate with y in this sample (selection on the outcome). Refitting OLS on them and reading the p-values ignores that selection, so p-values are too small and CIs too narrow (the "winner's curse").
- **Sample splitting:** select on half A, run OLS inference on half B. Valid, simple, loses power and depends on the random split (can repeat and aggregate p-values).
- **Selective inference:** compute p-values conditional on the selection event (Lee et al. 2016, R `selectiveInference`); exact for fixed lambda.
- **Debiased / desparsified Lasso:** correct the Lasso bias with an estimate of the inverse covariance, giving asymptotically normal estimates and CIs for each coefficient (needs sparsity and n large enough).
- **Others:** bootstrap does not fix it naively; stability selection; Bayesian spike-and-slab.
- If you only need prediction, you do not need p-values at all.

**Example:** Pure-noise data (n = 100, p = 50, no true signal). After LassoCV selection and OLS refit, at least one selected feature had p < 0.05 in 39% of 100 runs. With sample splitting this was 11%. Careful: both numbers are the fraction of runs in which at least one selected feature looked significant, not the false-positive rate of a single test. With a handful of selected features, 5% per test already gives roughly 10% per run, so 11% is about what valid testing would show, while 39% is clearly inflated.

**Code:**
```python
import numpy as np, scipy.stats as st
from sklearn.linear_model import LassoCV
def ols_p(X, y):
    X1 = np.c_[np.ones(len(y)), X]; b = np.linalg.lstsq(X1, y, rcond=None)[0]; r = y - X1@b
    se = np.sqrt(r@r/(len(y)-X1.shape[1]) * np.diag(np.linalg.inv(X1.T@X1)))
    return 2*st.t.sf(np.abs(b/se), len(y)-X1.shape[1])[1:]
rng = np.random.default_rng(0); n, p, naive, split, runs = 100, 50, 0, 0, 100
for _ in range(runs):
    X = rng.normal(size=(n, p)); y = rng.normal(size=n)                       # no true signal
    s = np.flatnonzero(LassoCV(cv=5, random_state=0).fit(X, y).coef_)
    naive += len(s) > 0 and (ols_p(X[:, s], y) < .05).any()
    a = np.arange(n) < n//2; s2 = np.flatnonzero(LassoCV(cv=5, random_state=0).fit(X[a], y[a]).coef_)
    split += len(s2) > 0 and (ols_p(X[~a][:, s2], y[~a]) < .05).any()
print(naive/runs, split/runs)   # 0.39 0.11 = share of runs with >=1 "significant" selected feature (not per-test FPR)
```

**Follow-ups:**
- *Is the bias of Lasso also an issue?* Yes: shrunk coefficients are biased toward zero; debiasing or relaxed Lasso addresses it.
- *Could you just bootstrap?* Not by itself; the selection step must be repeated inside, and even then validity is limited.
- *In industry?* Often use holdout validation and effect sizes, and reserve formal inference for experiments (A/B tests).

**Common mistakes:** Reading OLS p-values from a Lasso-selected model; selecting and testing on the same data; claiming a feature "is significant" after stepwise or Lasso selection; forgetting the multiple-testing problem.

### Q48 ⭐ 🟡 Generalized Additive Models and monotonic constraints as interpretable alternatives to plain logistic regression in credit/insurance.
**Asked at:** Fintech, regulated GCCs, Klarna
**Say this first (1 line):** A GAM models the log-odds as a sum of smooth per-feature curves, so it captures non-linearity yet stays additive and explainable (one chart per feature); monotonic constraints force a curve to only go up or down, matching business logic and regulator expectations.

**Then explain:**
- **GAM:** `logit(p) = β0 + f1(x1) + f2(x2) + ...`, each `f` a spline (or a boosted tree stump in EBMs/Explainable Boosting Machines). Plot `f` to see the effect.
- **Beats plain logistic** when effects are curved (age, utilization, income) without hand-made bins; **beats black boxes** on explainability, because there are no hidden interactions.
- **Add selected interactions** (GA²M/EBM) if needed, keeping them few and visual.
- **Monotonic constraints:** more missed payments must never lower risk; higher income must not raise default risk. Enforced in boosted trees (`monotonic_cst` in sklearn HistGradientBoosting, XGBoost, LightGBM) and in splines (constrained fits). They reduce overfit noise and make models auditable.
- **Regulated settings:** adverse-action reasons come from the per-feature contributions; constraints and shape review are part of model-risk documentation.

**Example:** Synthetic credit-like data with a saturating effect of x0, a negative effect of x1, and a wiggle in x2. Test AUC: logistic 0.747, unconstrained depth-2 boosting 0.761, boosting with monotone constraints on x0 (increasing) and x1 (decreasing) 0.762. Checking the partial-dependence curve: unconstrained model has 1 violation on x0 and 5 on x1 (wiggles going the wrong way); the constrained model has 0.

**Code:**
```python
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0); n = 4000; X = rng.normal(size=(n, 3))
logit = 1.2*np.tanh(X[:, 0]) - 0.8*X[:, 1] + 0.5*np.sin(2*X[:, 2])
y = (rng.random(n) < 1/(1+np.exp(-logit))).astype(int)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
mono = HistGradientBoostingClassifier(max_depth=2, max_iter=150, learning_rate=.05,
                                      monotonic_cst=[1, -1, 0], random_state=0).fit(Xtr, ytr)
print(round(roc_auc_score(yte, mono.predict_proba(Xte)[:, 1]), 3))        # 0.762
G = np.zeros((50, 3)); G[:, 0] = np.linspace(-3, 3, 50)
print((np.diff(mono.predict_proba(G)[:, 1]) < -1e-9).sum())                # 0 violations
from sklearn.linear_model import LogisticRegression
free = HistGradientBoostingClassifier(max_depth=2, max_iter=150, learning_rate=.05, random_state=0).fit(Xtr, ytr)
print(round(roc_auc_score(yte, LogisticRegression().fit(Xtr, ytr).predict_proba(Xte)[:, 1]), 3),   # 0.747 logistic
      round(roc_auc_score(yte, free.predict_proba(Xte)[:, 1]), 3))                                  # 0.761 unconstrained
G1 = np.zeros((50, 3)); G1[:, 1] = np.linspace(-3, 3, 50)
print([int((np.diff(free.predict_proba(g)[:, 1]) * s < -1e-9).sum()) for g, s in [(G, 1), (G1, -1)]])    # violations x0, x1: [1, 5]
```

**Follow-ups:**
- *GAM vs scorecard?* A scorecard is a GAM with step functions (WoE bins, Q39); splines give smooth curves.
- *Do constraints hurt accuracy?* Slightly or not at all when the constraint matches reality; they often help on noisy data.
- *Tools?* `pygam`, `interpret` (EBM), statsmodels GLMGam, or splines in a sklearn pipeline (Q24).

**Common mistakes:** Imposing a constraint that is false for a subgroup; reading a GAM curve causally; adding many interactions and losing interpretability; not checking curves for noise at the tails.

### Q49 ⭐ 🔴 Implement coordinate-descent Lasso (soft-thresholding) in NumPy and explain why it yields exact zeros.
**Asked at:** Research-leaning, Amazon applied science
**Say this first (1 line):** Coordinate descent updates one coefficient at a time with the other coefficients fixed; each one-dimensional Lasso problem has a closed-form answer, the soft-threshold, which sets a coefficient exactly to zero whenever its correlation with the residual is no larger than the penalty.

**Then explain:**
- **Objective:** `(1/2n)‖y − Xβ‖² + λ‖β‖₁`.
- **Update for feature j:** with partial residual `r_j = y − Σ_{k≠j} x_k β_k`, `β_j = S(x_jᵀ r_j / n, λ) / (x_jᵀ x_j / n)` where `S(z, γ) = sign(z)·max(|z| − γ, 0)`.
- **Why exact zeros:** the L1 term has a kink at 0. If `|x_jᵀ r_j / n| ≤ λ` the subgradient at 0 contains 0, so zero is the optimum. L2 has a smooth derivative at 0, so it only shrinks and never reaches exactly zero.
- **Cost:** O(np) per sweep; keep the residual updated incrementally instead of recomputing. Sweep until the coefficients stop changing. Used by `glmnet` and sklearn (with warm starts along a λ path, active sets).
- **Assumes standardized features** and a centered y (or an unpenalized intercept).

**Example:** n = 200, p = 10, true coefficients (3, −2, 1.5, then 0 × 7), λ = 0.3. My implementation gives `[2.739, -1.642, 1.115, 0, 0, 0, 0, 0, 0, 0]`, identical to sklearn (max difference 0.0 at 6 decimals), 7 exact zeros. The non-zeros are shrunk from the truth: that is the Lasso bias.

**Code:**
```python
import numpy as np
from sklearn.linear_model import Lasso
def soft(z, g): return np.sign(z) * np.maximum(np.abs(z) - g, 0)
def lasso_cd(X, y, lam, iters=200):
    n, p = X.shape; b = np.zeros(p); r = y - X @ b; col = (X**2).sum(0) / n
    for _ in range(iters):
        for j in range(p):
            r += X[:, j] * b[j]                         # remove feature j from the fit
            b[j] = soft(X[:, j] @ r / n, lam) / col[j]  # exact 1-D minimizer
            r -= X[:, j] * b[j]
    return b
rng = np.random.default_rng(0); n, p = 200, 10
X = rng.normal(size=(n, p)); X -= X.mean(0); beta = np.r_[3, -2, 1.5, np.zeros(7)]
y = X @ beta + rng.normal(size=n); y -= y.mean()
mine = lasso_cd(X, y, 0.3)
ref = Lasso(alpha=.3, fit_intercept=False, tol=1e-10, max_iter=100000).fit(X, y).coef_
print(mine.round(3), np.abs(mine - ref).max().round(6), (mine == 0).sum())   # [2.739 -1.642 1.115 0 ...] 0.0 7
```

**Follow-ups:**
- *Why does it converge?* The objective is convex and the non-smooth part is separable across coordinates.
- *How to choose λ?* CV over a descending path with warm starts; `λ_max = max|Xᵀy|/n` gives all zeros.
- *Complexity vs gradient descent?* Cheap per update and no learning rate; very effective for sparse problems.

**Common mistakes:** Forgetting to standardize or divide by the column norm; updating with a stale residual; penalizing the intercept; claiming the L1 solution is unbiased.

### Q50 ⭐ 🔴 Derive the bias and variance of the Ridge estimator and show how shrinkage trades bias for variance.
**Asked at:** Research-leaning, Amazon applied science, Europe
**Say this first (1 line):** Ridge is `β̂ = (XᵀX + λI)⁻¹Xᵀy`; it is biased toward zero by `−λ(XᵀX + λI)⁻¹β` but its variance `σ²(XᵀX+λI)⁻¹XᵀX(XᵀX+λI)⁻¹` shrinks as λ grows, and a small λ buys more variance reduction than it costs in bias, so test error can fall.

**Then explain (derivation, with y = Xβ + ε, ε ~ (0, σ²I)):**
- **Estimator:** `β̂ = A Xᵀy` with `A = (XᵀX + λI)⁻¹`.
- **Mean:** `E[β̂] = A XᵀXβ = A(XᵀX + λI − λI)β = β − λAβ`.
- **Bias:** `−λ(XᵀX + λI)⁻¹β`. Zero at λ = 0 and grows with λ.
- **Variance:** `Cov(β̂) = σ² A XᵀX A`.
- **SVD view:** with singular values `d_i`, the variance of direction i is scaled by `d_i²/(d_i²+λ)²` (shrinks, especially where `d_i` is small, i.e., the noisy collinear directions), and the bias in that direction is `λ/(d_i²+λ)` times the true component.
- **Trade-off:** total MSE = ‖bias‖² + trace(variance). The derivative of MSE at λ = 0 is negative, so some λ > 0 always has lower MSE than OLS (Hoerl-Kennard).

**Example:** n = 50, p = 5, all true β = 1, σ = 2. Theory vs simulation (4,000 repeats): λ = 0 variance 0.434 (empirical 0.440), bias² 0. λ = 10: bias² 0.122 (empirical 0.115), variance 0.283 (empirical 0.282), total MSE 0.405 which is below OLS 0.434. λ = 50: MSE 1.158; λ = 200: 2.936, so too much shrinkage hurts.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0); n, p, sig = 50, 5, 2.0
X = rng.normal(size=(n, p)); beta = np.ones(p)
def theory(lam):
    A = np.linalg.inv(X.T@X + lam*np.eye(p)); bias = -lam*A@beta
    return bias@bias, sig**2*np.trace(A@X.T@X@A)
for lam in [0, 10, 50, 200]:
    est = np.array([np.linalg.solve(X.T@X + lam*np.eye(p), X.T@(X@beta + rng.normal(0, sig, n))) for _ in range(4000)])
    emp_bias2 = ((est.mean(0) - beta)**2).sum()
    print(lam, np.round(theory(lam), 3), round(emp_bias2, 3), est.var(0).sum().round(3))
# lam=0 (0.0, 0.434) emp 0.0 0.44 | lam=10 (0.122, 0.283) emp 0.115 0.282 | lam=50 (1.061, 0.097) emp 1.056 0.098
```

**Follow-ups:**
- *Why does Ridge help with collinearity?* Adding λ lifts tiny eigenvalues of XᵀX, so the inverse stops exploding.
- *Is Ridge unbiased?* No; that is the cost. It is also not scale-invariant, so standardize.
- *Bayesian view?* Ridge is the posterior mean under a Gaussian prior `β ~ N(0, (σ²/λ)I)`.

**Common mistakes:** Saying Ridge reduces bias; forgetting the intercept is not penalized; not standardizing; picking λ on training error (always chooses 0).

### Q51 ⭐ 🔴 Marginal effects in logistic regression: why is a coefficient not a constant change in probability, and how do you report average marginal effects?
**Asked at:** Economics-flavoured DS roles, Europe, consulting
**Say this first (1 line):** A logistic coefficient is a change in log-odds, which is constant, but the change in probability depends on where you are on the S-curve (slope is `β·p(1−p)`); so I report average marginal effects, the average of those slopes (or of discrete changes for dummies) across the observed data.

**Then explain:**
- **Why not constant:** `p = σ(η)`, `∂p/∂x = β·p(1−p)`. It is largest near p = 0.5 and tiny near 0 or 1, and it also changes with the other variables, because they shift `p` along the curve.
- **Odds ratio:** `e^β` is a constant multiplier on the odds, but that is not a constant change in probability.
- **Average marginal effect (AME):** average of `β·p̂ᵢ(1−p̂ᵢ)` over all rows (continuous); for a dummy, average of `p̂(x, d=1) − p̂(x, d=0)` over rows.
- **Alternatives:** marginal effect at the mean (MEM) uses a typical row, which may not exist; marginal effects at representative values (MER) for scenarios. AME is the usual headline.
- **Uncertainty:** delta method or bootstrap for CIs (`statsmodels` `get_margeff`).
- Interpretable statement: "On average, a 1-unit increase in x raises the probability of default by about 19 percentage points".

**Example:** Fitted model has coefficients 1.01 (x) and 0.73 (dummy z). AME of x = 0.194 (19.4 percentage points per unit), AME of z = 0.142. The slope for x varies a lot by position: at x = −3 it is 0.026, at x = 0 it is 0.231, at x = 3 it is 0.075 (with z fixed at 0.5), even though the coefficient is the same 1.01.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(0); n = 20000
x = rng.normal(size=(n, 1)); z = rng.integers(0, 2, n); X = np.c_[x, z]
y = (rng.random(n) < 1/(1+np.exp(-(-1 + 1.0*x[:, 0] + 0.8*z)))).astype(int)
m = LogisticRegression(C=1e6, max_iter=1000).fit(X, y); b = m.coef_[0]      # ~unpenalized
ph = m.predict_proba(X)[:, 1]
ame_x = np.mean(b[0] * ph * (1 - ph))                                       # continuous AME
X1, X0 = X.copy(), X.copy(); X1[:, 1] = 1; X0[:, 1] = 0
ame_z = np.mean(m.predict_proba(X1)[:, 1] - m.predict_proba(X0)[:, 1])      # dummy: discrete change
print(b.round(2), ame_x.round(3), ame_z.round(3))                           # [1.01 0.73] 0.194 0.142
for xv in [-3, 0, 3]:                                                       # slope of p in x at z = 0.5
    p0 = m.predict_proba([[xv, .5]])[0, 1]; print(xv, round(b[0]*p0*(1-p0), 3))   # 0.026, 0.231, 0.075
```

**Follow-ups:**
- *AME vs odds ratio for reporting?* Odds ratios suit relative statements and are comparable across studies; AME gives intuitive percentage-point changes.
- *Effect of the baseline rate?* The same odds ratio means very different probability changes at 1% and 50% baselines.
- *In a probit model?* Same idea with the normal pdf instead of `p(1−p)`.

**Common mistakes:** Saying "a one-unit increase raises probability by β"; confusing odds ratio with risk ratio; reporting marginal effect at the mean when the mean row is unrealistic; omitting CIs for the AME.

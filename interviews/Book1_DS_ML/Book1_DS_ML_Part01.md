# Book 1 — Part 01: Stats/Probability Basics, ML Fundamentals, From-Scratch Code

**Topic:** Statistics & probability essentials, ML fundamentals (bias-variance, overfitting, CV, leakage, splits), from-scratch NumPy
**Target:** >=30 questions  |  **Actual:** 35  |  **Date:** 2026-10-20
**Lane note:** deep stats -> Parts 13-14; regression/regularization -> Part 2.

> Dedupe pass: removed 1 cross-part duplicate(s); renumbered Q1–Q35. Stars: 14 x ⭐⭐⭐ (Q1–14), 16 x ⭐⭐ (Q15–30), 5 x ⭐ (Q31–35).

---

### Q1 ⭐⭐⭐ 🟢 Explain the bias-variance tradeoff. How do you diagnose which one your model suffers from (learning curves)?
**Asked at:** Flipkart, Amazon, Fractal, product cos, GCCs
**Say this first (1 line):** Bias is error from a model that is too simple to capture the pattern; variance is error from a model so flexible that it chases noise in the particular training sample. Making a model more complex lowers bias but raises variance, so you look for the sweet spot.

**Then explain:**
- **High bias (underfit):** train error high, validation error high, and the two are close.
- **High variance (overfit):** train error very low, validation error much higher, big gap.
- **Total error = bias² + variance + irreducible noise.** Noise is the part no model can remove.
- **Learning curve** (error vs training-set size) is the diagnostic:

| Curve shape | Diagnosis | What helps |
|---|---|---|
| Both curves plateau high, close together | High bias | More features, bigger model, less regularization. More data will NOT help |
| Train low, val high, gap shrinks as data grows | High variance | More data, regularization, simpler model, bagging, early stopping |

**Example:** Fitting a straight line to `sin(2x)` data is high bias. A fully grown decision tree on the same data is high variance. Real output from `learning_curve` (MSE, 5-fold, noise variance = 0.09):

```
linear (high bias)           n=48..480  train 0.56 -> 0.53   val 0.55 -> 0.53   (flat, same, high)
deep tree (high variance)    n=48..480  train 0.00 -> 0.00   val 0.20 -> 0.17   (huge gap)
```

**Code:**
```python
import numpy as np
from sklearn.model_selection import learning_curve
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
rng = np.random.default_rng(0)
X = rng.uniform(-3, 3, (600, 1)); y = np.sin(2 * X[:, 0]) + rng.normal(0, .3, 600)
for name, m in [("linear", LinearRegression()), ("deep tree", DecisionTreeRegressor(random_state=0))]:
    n, tr, va = learning_curve(m, X, y, train_sizes=[.1, .3, .6, 1.0], cv=5,
                               scoring="neg_mean_squared_error")
    print(name, "train", np.round(-tr.mean(1), 3), "val", np.round(-va.mean(1), 3))
```

**Follow-ups:**
- *Does more data fix high bias?* No. A straight line stays a straight line. It fixes variance.
- *How does it show up in ensembles?* Bagging/random forest cut variance; boosting cuts bias.
- *Does deep learning break the tradeoff?* Big nets can interpolate the training data and still generalize (double descent), but the practical advice (regularize, validate) stands.

**Common mistakes:** Saying "more data always helps"; judging only by train error; ignoring the irreducible noise floor (a val error near the noise level means you are done, not underfit).

### Q2 ⭐⭐⭐ 🟢 What is overfitting? How do you detect it and what are your options to fix it?
**Asked at:** Swiggy, Flipkart, Amazon, Fractal, most loops
**Say this first (1 line):** Overfitting is when the model memorises the training data, noise included, so it scores well on train but badly on unseen data.

**Then explain:**
- **Detect:** large train-vs-validation gap; validation loss starts rising while train loss keeps falling; learning curve gap that doesn't close; CV score much lower than train score.
- **Fix, roughly in this order:**
  1. Get more (or more representative) data / augmentation.
  2. Simplify the model: shallower trees, fewer features, smaller net.
  3. Regularize: L1/L2, dropout, min samples per leaf, `max_depth`.
  4. Early stopping on a validation set.
  5. Ensembling (bagging/random forest) to cut variance.
  6. Check for leakage first, because leakage looks like great performance, not overfitting.
- The test set is never used to make these choices.

**Example:** Unpruned decision tree on a noisy 1000-row problem: train acc 1.00, validation 0.82. Limiting `max_depth=3` gave train 0.884, validation 0.873: lower train score, better real-world score.

**Code:**
```python
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
X, y = make_classification(1000, 20, n_informative=5, flip_y=.1, random_state=0)
Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=.3, random_state=0)
for d in [None, 3]:
    m = DecisionTreeClassifier(max_depth=d, random_state=0).fit(Xtr, ytr)
    print(d, round(m.score(Xtr, ytr), 3), round(m.score(Xva, yva), 3))
# None 1.0 0.82 | 3 0.884 0.873
```

**Follow-ups:**
- *Can you overfit the validation set?* Yes, by tuning hundreds of configurations against it. That is why a final untouched test set exists.
- *Is 100% train accuracy always overfitting?* Not necessarily on noise-free data, but on real noisy data it almost always is.

**Common mistakes:** Treating high train accuracy as success; "fixing" overfitting by tuning on the test set; adding regularization when the real problem is leakage or a train/val distribution mismatch.

### Q3 ⭐⭐⭐ 🟢 Supervised vs unsupervised vs semi/self-supervised vs reinforcement learning: differences with one example each.
**Asked at:** Zalando, Indian services/analytics firms, screening rounds
**Say this first (1 line):** It depends on what signal the model learns from: labels (supervised), no labels (unsupervised), a few labels plus many unlabeled (semi-supervised), labels it creates from the data itself (self-supervised), or rewards from interacting with an environment (reinforcement learning).

**Then explain:**

| Type | Learns from | Example |
|---|---|---|
| Supervised | (input, label) pairs | Predict loan default; delivery-time regression |
| Unsupervised | Inputs only; finds structure | Customer segmentation with k-means; anomaly detection |
| Semi-supervised | Few labels + many unlabeled | 1,000 labelled medical scans + 100,000 unlabeled, using pseudo-labels |
| Self-supervised | Labels derived from the data itself | Predict the next word (GPT) or a masked word (BERT); contrastive image learning |
| Reinforcement | Reward from actions over time | Ad bidding, game playing, dynamic pricing policy |

- Self-supervised is technically a kind of unsupervised learning, but the training loop looks supervised (there is a target), which is why it scales so well for LLMs.
- RL differs because the data depends on the model's own actions and feedback is delayed.

**Example:** Spotify: supervised (will user skip this track?), unsupervised (cluster listeners), self-supervised (embed tracks from co-listening sequences), RL/bandits (which playlist tile to show).

**Follow-ups:**
- *Where do LLMs fit?* Pretraining is self-supervised, instruction tuning is supervised, RLHF is reinforcement learning.
- *Bandit vs RL?* A bandit has no long-term state; each choice is independent.

**Common mistakes:** Calling clustering "supervised"; saying self-supervised needs manual labels; calling every recommender "unsupervised".

### Q4 ⭐⭐⭐ 🟢 Why do we split data into train / validation / test? Why must the test set stay untouched until the end?
**Asked at:** Almost all companies, screening rounds
**Say this first (1 line):** Train fits the model, validation is used to choose between models and hyperparameters, and the test set gives one honest estimate of real-world performance, which is only honest if it never influenced any decision.

**Then explain:**
- **Train (~60-80%):** learn the parameters.
- **Validation (~10-20%):** compare models, tune hyperparameters, early-stop. Every choice made on it leaks a little information into the model.
- **Test (~10-20%):** touched once, at the end. If you tune against it, your score becomes optimistic, because you have effectively picked the model that got lucky on that data.
- With small data, replace the fixed validation set with cross-validation, but still hold out a test set.
- Split the way production will see data: by time for forecasting, by user for per-user data.

**Example:** You try 200 hyperparameter settings and pick the best on the test set. Even with a useless model, the best of 200 noisy scores looks good, a form of selection bias. The reported 0.85 becomes 0.80 in production.

**Follow-ups:**
- *What if test score is bad after you finalise?* Treat it as information. Do not retune and re-test, or collect fresh data.
- *After picking the model, do you retrain on train+val?* Usually yes, with the settings already chosen.

**Common mistakes:** Fitting scalers/imputers before splitting; tuning on test; random splits on time-ordered or grouped data; reusing the test set after every experiment.

### Q5 ⭐⭐⭐ 🟢 What is cross-validation? How does k-fold work, how do you choose k, and when does it fail?
**Asked at:** Amazon, Flipkart, GCCs, Europe product cos
**Say this first (1 line):** Cross-validation estimates generalisation by repeatedly training on part of the data and scoring on the held-out part, so every row gets to be validation exactly once.

**Then explain:**
- **k-fold:** shuffle, cut into k equal folds; for each fold train on the other k-1 folds, score on it; average the k scores (and report the std).
- **Choosing k:** k=5 or 10 is the standard. Small k = more bias (less training data per fold), cheaper. Large k (LOO) = low bias, high variance in the estimate, expensive. 
- **Variants:** `StratifiedKFold` for imbalanced classes, `GroupKFold` when rows share an entity, `TimeSeriesSplit` for temporal data.
- **When it fails:** time-ordered data (random folds train on the future), grouped/duplicated rows (leak across folds), preprocessing done before the split, very small or heavily imbalanced data (high-variance scores), and tuning on the same CV you report (use nested CV).

**Example:** 5-fold stratified AUC on a 90/10 imbalanced set: folds `[0.993, 0.769, 0.921, 0.765, 0.822]`, mean 0.854, std 0.089. The std is the honest message: the score is not stable to 2 decimals.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
X, y = make_classification(500, 10, weights=[.9], random_state=0)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
s = cross_val_score(LogisticRegression(max_iter=1000), X, y, cv=cv, scoring="roc_auc")
print(np.round(s, 3), s.mean().round(3), s.std().round(3))
```

**Follow-ups:**
- *Cost?* k model fits, so k times the training time.
- *Is CV score the test score?* No, it is a validation estimate; keep a final holdout.

**Common mistakes:** Scaling before CV (put it in a `Pipeline`); no shuffling on sorted data; ignoring fold variance; using plain k-fold on time series.

### Q6 ⭐⭐⭐ 🟢 Covariance vs correlation, Pearson vs Spearman, and correlation vs causation.
**Asked at:** Amazon, Walmart GCC, analytics firms
**Say this first (1 line):** Covariance is the unit-dependent joint variation of two variables; correlation is covariance rescaled to [-1, 1]; Pearson measures linear association, Spearman measures monotonic association on ranks; and neither says anything about causation.

**Then explain:**
- **Covariance:** `cov(X,Y) = E[(X-μx)(Y-μy)]`. Sign tells direction, magnitude depends on units, so it is hard to compare.
- **Pearson r** `= cov / (σx σy)`. Unit-free, but sensitive to outliers and only sees linear relationships.
- **Spearman ρ:** Pearson on the ranks. Captures any monotonic trend, robust to outliers and non-normal data. Kendall τ is similar and better for small samples with ties.
- **r = 0 does not mean independent.** A U-shape can have r near 0.
- **Correlation is not causation:** confounders (ice-cream sales and drownings both rise with temperature), reverse causality, selection bias, and coincidence. Causation needs randomised experiments or causal methods.

**Example (real run of the code below):**
```
y = exp(x) + noise      pearson 0.87  spearman 0.99
y = x^2 + noise (U)     pearson 0.07  spearman 0.05
1 outlier added to the exp data (x=5, y=-300)   pearson 0.87 -> 0.69   spearman 0.99 -> 0.96
```

**Code:**
```python
import numpy as np
from scipy.stats import pearsonr, spearmanr
rng = np.random.default_rng(0)
x = rng.uniform(0, 5, 200); y = np.exp(x) + rng.normal(0, 1, 200)
print(pearsonr(x, y)[0], spearmanr(x, y)[0])   # 0.87 vs 0.99
x2 = rng.uniform(-3, 3, 200); y2 = x2**2 + rng.normal(0, 1, 200)       # U-shape
print(pearsonr(x2, y2)[0], spearmanr(x2, y2)[0])                         # ~0.07, ~0.05
xo, yo = np.r_[x, 5], np.r_[y, -300]                                     # one outlier
print(pearsonr(xo, yo)[0], spearmanr(xo, yo)[0])                         # ~0.69, ~0.96
```

**Follow-ups:**
- *Features with high correlation to each other?* Multicollinearity hurts coefficient stability in linear models, not tree predictions much.
- *How do you check causation?* A/B test, diff-in-diff, instrumental variables, with the assumptions stated.

**Common mistakes:** Using Pearson on skewed data with outliers; reading r=0 as no relationship; claiming "feature importance" proves cause.

### Q7 ⭐⭐⭐ 🟡 What is data leakage? Give 4 real examples (target, preprocessing, temporal, group) and how you would detect it.
**Asked at:** Amazon, Klarna, Booking, PhonePe, senior loops
**Say this first (1 line):** Data leakage is when information that would not be available at prediction time sneaks into training or validation, so offline scores look great and production scores collapse.

**Then explain (four classic types):**
- **Target leakage:** a feature is a consequence of the label. E.g. predicting loan default using "collections_calls_made", or churn using "account_closed_date".
- **Preprocessing leakage:** fitting scaler/imputer/encoder/feature-selection on the full data before splitting, so test statistics leak into training.
- **Temporal leakage:** random split of time-ordered data, or using future aggregates (e.g. "average spend this month" computed including days after the prediction date).
- **Group/duplicate leakage:** the same user, patient, or near-duplicate row is in both train and test; the model memorises the entity.
- **Detect:** suspiciously high score; one feature dominating importance; big drop on a time-based or group-based holdout; check feature definitions against "available at prediction time"; check duplicate IDs across splits.

**Example (real runs):** Pure random noise, 100 rows x 2000 features, random labels. Selecting the top 20 features on all data then cross-validating gives 0.78 accuracy. Doing selection inside a `Pipeline` gives 0.59, close to chance. For grouped data (100 users x 10 rows, label random per user, a 3-nearest-neighbour model on per-user features), random KFold gives about 1.00 accuracy and GroupKFold gives 0.54 (chance). Group code is in Q21.

**Code:**
```python
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
rng = np.random.default_rng(0)
X = rng.normal(size=(100, 2000)); y = rng.integers(0, 2, 100)      # pure noise
Xl = SelectKBest(f_classif, k=20).fit_transform(X, y)               # LEAKY
print(cross_val_score(LogisticRegression(), Xl, y, cv=5).mean())   # ~0.78
pipe = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression())
print(cross_val_score(pipe, X, y, cv=5).mean())                    # ~0.59
```

**Follow-ups:**
- *How do you prevent it?* Pipelines, point-in-time feature stores, time/group splits, a feature review asking "when is this known?".
- *Leakage vs overfitting?* Overfitting is a model problem; leakage is a data/process problem and a bigger model does not cause it.

**Common mistakes:** Only thinking of target leakage; fitting the scaler first "because it is just scaling"; trusting an AUC of 0.99 instead of investigating it.

### Q8 ⭐⭐⭐ 🟡 Do feature scaling and missing-value imputation belong before or after the split? Which models need scaling and why?
**Asked at:** Flipkart, Swiggy, GCCs, live-coding rounds
**Say this first (1 line):** After the split: learn scaling and imputation statistics from the training set only, then apply those same numbers to validation and test. Models that use distances or gradients need scaling; tree models don't.

**Then explain:**
- **Why after:** the mean/median/std of the full data contains test information. Fitting on train only mimics production, where new data arrives with unknown statistics. Do it inside a `Pipeline` so each CV fold refits it.
- **Need scaling:** KNN, k-means, SVM, PCA (distance/variance based); linear/logistic regression and neural nets with regularization or gradient descent (faster, stable convergence, fair penalty across features).
- **Don't need it:** decision trees, random forests, gradient boosting (they split on thresholds, which are invariant to monotone scaling).
- **Imputation** needs the same discipline: learn the median from train only. Optionally add a missing-indicator.

**Example (real run of the demo below):** 1000 rows, 5 informative features. KNN accuracy 0.97 drops to 0.66 when one feature is multiplied by 1000, because that feature dominates distance. A decision tree stays at 0.97 either way.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
X, y = make_classification(1000, 5, n_informative=5, n_redundant=0, random_state=0)
for sc in [1, 1000]:                       # blow up one feature's scale
    Z = X.copy(); Z[:, 0] *= sc
    a, b, c, d = train_test_split(Z, y, random_state=0)
    print(sc, KNeighborsClassifier().fit(a, c).score(b, d), DecisionTreeClassifier(random_state=0).fit(a, c).score(b, d))
# 1 0.972 0.972 | 1000 0.664 0.972

# the right way: fit preprocessing on train only, inside a Pipeline
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
pipe = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression())
pipe.fit(Xtr, ytr)          # statistics learned from train only
print(pipe.score(Xte, yte)) # test is transformed with train's numbers
```

**Follow-ups:**
- *Standardize vs min-max?* Standardize by default; min-max is outlier-sensitive but fine for bounded inputs. Use robust scaling for heavy outliers.
- *Do you scale the target?* Only if useful (e.g. log of a skewed target), and invert for predictions.

**Common mistakes:** `scaler.fit_transform(X)` on everything then splitting; scaling one-hot columns pointlessly; calling `fit` on the test set instead of `transform`.

### Q9 ⭐⭐⭐ 🟡 Walk me through how you would approach a new ML problem end to end (framing, baseline, metric, validation, iteration).
**Asked at:** Fractal, Swiggy, Zalando, Spotify, all case rounds
**Say this first (1 line):** I start from the business decision, define the metric and the validation scheme before touching a model, build a simple baseline, then iterate with error analysis, and plan for deployment and monitoring from day one.

**Then explain (the loop):**
1. **Frame:** what decision does the prediction change? Who uses it, and what is the cost of a wrong answer? Is ML even needed, and is it classification, regression, ranking?
2. **Data:** what is available at prediction time, label definition, volume, quality, leakage risks.
3. **Metric:** a business-aligned metric (e.g. precision@k, recall at fixed precision, MAE in rupees), plus guardrails.
4. **Validation:** split that mirrors production (time/group), and a locked test set.
5. **Baseline:** majority class / rule / linear model. Anything fancier must beat it.
6. **Iterate:** feature engineering, a stronger model (gradient boosting for tabular), error analysis by segment, regularize.
7. **Ship and monitor:** serving latency, train-serve skew, drift, retraining, A/B test.

**Example:** Predicting delivery delay at a food-delivery company: decision = show a longer ETA; metric = MAE in minutes plus % of orders late by >10 min; baseline = restaurant average prep + distance; model = LightGBM; split = last 2 weeks held out by time.

**Follow-ups:**
- *Why the baseline?* It tells you whether complexity is paying off and catches pipeline bugs.
- *What if the model beats the baseline only slightly?* Check whether the ceiling is in the data (noise), and weigh gain against maintenance cost.

**Common mistakes:** Jumping straight to XGBoost; picking accuracy on imbalanced data; random splits; no baseline; stopping at the offline metric without a plan for monitoring.

### Q10 ⭐⭐⭐ 🟡 Implement linear regression from scratch in NumPy (normal equation and gradient descent). What are the complexity trade-offs?
**Asked at:** Booking.com, Robinhood, Brex, Flipkart, product cos
**Say this first (1 line):** Linear regression minimises squared error; the normal equation solves it in one shot, `w = (XᵀX)⁻¹Xᵀy`, while gradient descent walks downhill iteratively and scales better to many rows and features.

**Then explain:**
- **Normal equation:** exact. Cost O(n·d² + d³): forming XᵀX costs n·d², solving costs d³. Fails or is unstable if XᵀX is singular (collinear features). Use `np.linalg.solve` (or `lstsq`), not `inv`.
- **Gradient descent:** gradient of MSE is `(2/n) Xᵀ(Xw - y)`. Cost O(n·d) per step, times the number of epochs. Needs a learning rate and scaled features. Works with huge n, and mini-batches/SGD make it streaming-friendly.
- Pick the normal equation when d is small (up to a few thousand); GD/SGD when d is large or data doesn't fit in memory.
- Add a bias column of ones (or centre the data) to learn the intercept.

**Example (real run of the code below):** data generated with true weights `[4, 2, -1, 0.5]` (intercept first) plus small noise. Normal equation and gradient descent both recover `[3.994 2.004 -0.999 0.506]`.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
n, d = 500, 3
X = rng.normal(size=(n, d))
y = X @ np.array([2.0, -1.0, 0.5]) + 4.0 + rng.normal(0, 0.1, n)

def fit_normal_eq(X, y):
    Xb = np.c_[np.ones(len(X)), X]
    return np.linalg.solve(Xb.T @ Xb, Xb.T @ y)

def fit_gd(X, y, lr=0.1, epochs=500):
    Xb = np.c_[np.ones(len(X)), X]
    w = np.zeros(Xb.shape[1])
    for _ in range(epochs):
        w -= lr * 2 / len(y) * Xb.T @ (Xb @ w - y)
    return w

print(fit_normal_eq(X, y).round(3), fit_gd(X, y).round(3))
```

**Follow-ups:**
- *Add ridge?* Solve `(XᵀX + λI)w = Xᵀy`, which also fixes singularity (do not penalise the intercept).
- *Why is MSE convex here?* The Hessian `2XᵀX/n` is positive semi-definite, so GD with a small enough step reaches the global minimum.

**Common mistakes:** Forgetting the bias term; using `inv`; unscaled features making GD crawl or diverge; mixing up `X.T @ X` dimensions.

### Q11 ⭐⭐⭐ 🟡 Implement logistic regression from scratch with gradient descent. Why clip/stabilise the sigmoid, and what happens if the learning rate is too high or low?
**Asked at:** Booking.com, Splunk, Flipkart, Amazon, MLE screens
**Say this first (1 line):** Logistic regression models `p = sigmoid(Xw)` and minimises log loss; the gradient is neatly `Xᵀ(p - y)/n`, and I clip the sigmoid input (and add epsilon inside logs) so large scores don't overflow or give `log(0)`.

**Then explain:**
- **Sigmoid:** `1/(1+e^-z)`. For very negative z, `e^-z` overflows. Clip z to about [-500, 500] or use a stable two-branch form.
- **Loss:** `-mean(y log p + (1-y) log(1-p))`. Add a tiny epsilon to avoid `log(0)`.
- **Learning rate:** too low means painfully slow progress; too high means loss oscillates or blows up. Scaling features helps a lot.
- **Separable data:** weights grow without bound unless you regularize (L2).
- Loss is convex, so GD reaches the global optimum.

**Example (real run of the code below: 500 rows, 5 standardized features, 300 epochs):** `lr=0.001` final loss 0.677 (barely moved from log 2 = 0.693); `lr=0.1` 0.480; `lr=5` 0.460 (fast); `lr=500` 10.52 (diverged/bouncing). With `lr=1`, 5000 epochs, the learned coefficients match sklearn's (near-unregularised `C=1e6`) to 2 decimals: `[1.5 0.16 -0.05 -1.24 2.91]`.

**Code:**
```python
import numpy as np
def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

def fit_logreg(X, y, lr=0.1, epochs=1000, l2=0.0):
    Xb = np.c_[np.ones(len(X)), X]
    w = np.zeros(Xb.shape[1]); losses = []
    for _ in range(epochs):
        p = sigmoid(Xb @ w)
        grad = Xb.T @ (p - y) / len(y)
        grad[1:] += l2 * w[1:] / len(y)          # don't penalise the bias
        w -= lr * grad
        eps = 1e-12
        losses.append(-np.mean(y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps)))
    return w, losses

# demo: learning-rate sweep, then compare with sklearn
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
X, y = make_classification(500, 5, n_informative=3, n_redundant=0, random_state=0)
X = StandardScaler().fit_transform(X)
for lr in [0.001, 0.1, 5, 500]:
    print(lr, round(fit_logreg(X, y, lr=lr, epochs=300)[1][-1], 3))   # 0.677 0.48 0.46 10.522
w, _ = fit_logreg(X, y, lr=1, epochs=5000)
print(w[1:].round(2), LogisticRegression(C=1e6, max_iter=5000).fit(X, y).coef_.round(2))
```

**Follow-ups:**
- *Why not MSE for classification?* With a sigmoid it makes a non-convex loss with vanishing gradients; log loss is the MLE for Bernoulli labels.
- *Decision threshold?* 0.5 is a default; choose it from the PR/ROC curve and costs.

**Common mistakes:** Forgetting the bias; unscaled features; computing `log(p)` without epsilon; penalising the intercept; reporting accuracy on imbalanced data.

### Q12 ⭐⭐⭐ 🟡 Implement k-means from scratch in NumPy (init, assignment, update, convergence, empty clusters).
**Asked at:** Booking.com, Splunk, Swiggy, MLE screens
**Say this first (1 line):** K-means alternates two steps, assign every point to its nearest centroid and move each centroid to the mean of its points, until assignments stop changing; it minimises within-cluster squared distance (inertia).

**Then explain:**
- **Init:** random points, or better **k-means++** (pick new centres with probability proportional to squared distance from existing ones) for faster, better solutions. Run several restarts and keep the lowest inertia.
- **Assign:** `(n,k)` distance matrix by broadcasting, then `argmin`.
- **Update:** mean per cluster. **Empty cluster:** re-seed to the point farthest from its centroid.
- **Converge:** centroid shift below a tolerance or max iterations. Always converges (inertia never increases) but only to a local minimum.
- **Cost:** O(n·k·d) per iteration. Needs feature scaling, assumes roughly spherical equal-size clusters, and k must be chosen (elbow, silhouette).

**Example (real run of the code below):** on 600 points from `make_blobs(600, centers=4, random_state=0)`, scratch inertia is 1043.8, equal to sklearn's `KMeans(4, n_init=10)` inertia of 1043.8.

**Code:**
```python
import numpy as np
def kmeans(X, k, n_iter=100, tol=1e-6, seed=0):
    rng = np.random.default_rng(seed)
    C = [X[rng.integers(len(X))]]                                # k-means++ init
    for _ in range(k - 1):
        d2 = np.min(((X[:, None] - np.array(C)[None]) ** 2).sum(-1), axis=1)
        C.append(X[rng.choice(len(X), p=d2 / d2.sum())])
    C = np.array(C)
    for _ in range(n_iter):
        d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(-1)       # (n, k)
        labels = d.argmin(1)
        newC = C.copy()
        for j in range(k):
            pts = X[labels == j]
            newC[j] = pts.mean(0) if len(pts) else X[d.min(1).argmax()]
        shift = np.abs(newC - C).max(); C = newC
        if shift < tol: break
    return C, labels, ((X - C[labels]) ** 2).sum()

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
X, _ = make_blobs(600, centers=4, random_state=0)
print(round(kmeans(X, 4)[2], 1), round(KMeans(4, n_init=10, random_state=0).fit(X).inertia_, 1))   # 1043.8 1043.8
```

**Follow-ups:**
- *Why does it converge?* Both steps can only lower or keep the objective, and there are finitely many partitions.
- *Large n?* Mini-batch k-means.
- *Non-spherical clusters?* Use GMM, DBSCAN, or spectral clustering.

**Common mistakes:** Not scaling features; a single random init; crashing on empty clusters (`mean` of empty slice gives NaN); choosing k by inertia alone (it always falls as k grows).

### Q13 ⭐⭐⭐ 🟡 Implement k-nearest neighbours from scratch. How does choice of k and distance metric affect bias/variance, and how do you make prediction fast?
**Asked at:** Microsoft IDC, Walmart GCC, MLE screens
**Say this first (1 line):** KNN stores the training data and predicts by majority vote (or average) of the k closest points; small k means low bias and high variance, large k means the reverse, and for speed you use vectorised distances, `argpartition`, or a KD-tree/ANN index.

**Then explain:**
- **Choice of k:** k=1 memorises (train accuracy 100%, noisy boundary). Large k smooths until it underfits. Pick k by cross-validation, use odd k for binary problems.
- **Distance metric:** Euclidean (default, needs scaling), Manhattan (more robust to outliers, better in high-d), cosine (text/embeddings). Weighted voting by 1/distance helps.
- **Cost:** training is O(1) (just stores data); each query is O(n·d). Fast ways: vectorised distance matrix, `argpartition` for top-k in O(n) instead of a sort, KD/ball trees (good for low d), approximate nearest neighbours like HNSW/FAISS for big or high-d data.
- Suffers from the curse of dimensionality and needs scaled features.

**Code (matches sklearn: both 1.0 on iris test split):**
```python
import numpy as np
from collections import Counter

class KNN:
    def __init__(self, k=5): self.k = k
    def fit(self, X, y): self.X, self.y = X, y; return self
    def predict(self, Q):
        # squared Euclidean via |q|^2 - 2 q.x + |x|^2 (no Python loop)
        d2 = (Q**2).sum(1)[:, None] - 2 * Q @ self.X.T + (self.X**2).sum(1)[None]
        idx = np.argpartition(d2, self.k, axis=1)[:, :self.k]    # top-k, no full sort
        return np.array([Counter(self.y[r]).most_common(1)[0][0] for r in idx])
```

**Example (iris, real run):** k=1 train 1.00 / test 0.978; k=5 train 0.962 / test 1.0; k=25 train 0.924 / test 0.978. Train accuracy falls as k grows, the sign of rising bias.

**Follow-ups:**
- *Ties?* Use odd k, or break by nearest neighbour/weighted vote.
- *Regression?* Average (or distance-weighted average) of neighbour targets.

**Common mistakes:** Not scaling; looping over all pairs in Python; evaluating k on the training set (k=1 always wins there); forgetting `argpartition` needs k < n.

### Q14 ⭐⭐⭐ 🟡 Explain gradient descent: batch vs stochastic vs mini-batch, learning rate, convergence, local minima.
**Asked at:** Flipkart, Amazon, Swiggy, deep-learning-leaning loops
**Say this first (1 line):** Gradient descent repeatedly steps opposite the gradient of the loss, `w ← w - lr·∇L`; batch uses all data per step, stochastic uses one sample, mini-batch uses a small chunk (the practical default).

**Then explain:**

| Variant | Gradient from | Pros | Cons |
|---|---|---|---|
| Batch | all n rows | Smooth, deterministic | Slow per step, memory heavy |
| SGD | 1 row | Very cheap, noise can escape bad regions | Noisy path |
| Mini-batch (32-512) | b rows | Vectorised on GPU, good noise/speed balance | Needs batch size tuning |

- **Learning rate:** too small is slow, too big oscillates or diverges. Use schedules/decay, warmup, or adaptive optimisers (Adam).
- **Convergence:** convex losses (linear/logistic regression) reach the global minimum. Neural nets are non-convex, but in high dimensions most trouble spots are saddle points rather than bad local minima, and SGD noise helps escape them.
- **Feature scaling** makes the loss surface rounder, so GD converges faster.
- Momentum/Adam smooth the noise and speed up progress along shallow directions.

**Example (real run, linear regression, true w = [1, 2, -3]):** batch `[1.0, 1.98, -2.97]`, SGD `[1.06, 2.01, -3.03]`, mini-batch-32 `[1.04, 2.03, -2.99]`, all MSE about 0.247 (noise floor 0.25). With lr=1.5 (batch) the weights blew up (millions after 20 steps).

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
n = 2000
X = np.c_[np.ones(n), rng.normal(size=(n, 2))]
y = X @ np.array([1., 2., -3.]) + rng.normal(0, .5, n)
def run(bs, lr, epochs=20):
    w = np.zeros(3)
    for _ in range(epochs):
        idx = rng.permutation(n)
        for i in range(0, n, bs):
            b = idx[i:i + bs]
            w -= lr * 2 / len(b) * X[b].T @ (X[b] @ w - y[b])
    return w
print(run(n, .1), run(1, .005), run(32, .05))   # batch, SGD, mini-batch
```

**Follow-ups:**
- *Why shuffle each epoch?* Avoids order-dependent bias and correlated batches.
- *Large batch problems?* Can generalise worse and needs a scaled learning rate.

**Common mistakes:** Saying "local minima are the main problem"; not scaling features; using the same lr for all batch sizes; forgetting to divide the gradient by batch size.

### Q15 ⭐⭐ 🟢 What is the difference between parameters and hyperparameters? Name examples for 3 models.
**Asked at:** Indian services/analytics firms, JPMC GCC
**Say this first (1 line):** Parameters are learned from data during training; hyperparameters are set by you before training and control how learning happens.

**Then explain:**

| Model | Parameters (learned) | Hyperparameters (chosen) |
|---|---|---|
| Linear/logistic regression | coefficients, intercept | regularization strength (C or alpha), penalty type, solver |
| Decision tree / random forest | split features and thresholds, leaf values | `max_depth`, `min_samples_leaf`, `n_estimators`, `max_features` |
| Neural network | weights, biases | learning rate, layers, width, batch size, dropout |
| KNN | none (stores the data) | k, distance metric |

- Tune hyperparameters on validation data or CV, never on test.
- Rule of thumb: if gradient descent or a closed-form solve updates it, it is a parameter.

**Example:** In ridge regression, the coefficients are parameters; `alpha=1.0` is a hyperparameter you pick via cross-validation.

**Follow-ups:**
- *How do you tune them?* Random search or Bayesian optimisation with CV; start with the few that matter most (learning rate, depth, regularization).
- *Are number of epochs and early-stopping patience hyperparameters?* Yes.

**Common mistakes:** Calling k in KNN a parameter; tuning on the test set; searching a grid too wide without a log scale for rates and penalties.

### Q16 ⭐⭐ 🟢 Explain the curse of dimensionality and its effect on KNN and distance-based methods.
**Asked at:** Flipkart, Amazon, Microsoft IDC
**Say this first (1 line):** As the number of features grows, space becomes so vast and empty that data gets sparse and distances between points stop being meaningful, which breaks KNN, k-means and other distance-based methods.

**Then explain:**
- **Sparsity:** to cover a unit cube at the same density you need exponentially more points as d grows.
- **Distance concentration:** the nearest and farthest neighbours end up at almost the same distance, so "nearest" carries little information.
- **Effects:** KNN accuracy degrades, clustering gets unstable, models overfit because there are many ways to separate few points.
- **Remedies:** feature selection, PCA/other dimensionality reduction, learned embeddings, using cosine or L1 distance, regularization, ANN indexes on embeddings, more data.

**Example (real run, 1000 uniform random points, relative spread `(max-min)/min` of distances to a query):**
```
d=2     134.62
d=10      3.48
d=100     0.39
d=1000    0.11
```
In 1000 dimensions, the farthest point is only ~11% farther than the nearest.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
for d in [2, 10, 100, 1000]:
    X = rng.uniform(size=(1000, d)); q = rng.uniform(size=d)
    dist = np.linalg.norm(X - q, axis=1)
    print(d, round((dist.max() - dist.min()) / dist.min(), 2))
```

**Follow-ups:**
- *Do trees suffer?* Less, since they pick informative features, but irrelevant features still add noise.
- *Why do embeddings still work?* Real data lies near a low-dimensional manifold, so the intrinsic dimension is small.

**Common mistakes:** Saying "more features is always better"; thinking only KNN is affected; ignoring that unscaled/irrelevant features worsen it.

### Q17 ⭐⭐ 🟢 Descriptive statistics refresher: mean vs median vs mode, variance/std, skewness; which summary would you report for skewed income data?
**Asked at:** Analytics firms, Walmart GCC, screening rounds
**Say this first (1 line):** For skewed income data I would report the median (plus percentiles), because a few very high earners drag the mean far above what a typical person earns.

**Then explain:**
- **Mean:** the average; sensitive to outliers. **Median:** middle value; robust. **Mode:** most frequent value; useful for categorical data.
- **Variance / std:** average squared / root-average-squared deviation from the mean. Also outlier-sensitive; for skewed data pair the median with IQR or percentiles.
- **Skewness:** asymmetry. Right-skewed (positive) means long upper tail and mean > median.
- For income: report median, P25/P75/P90, maybe the Gini coefficient; consider a log transform before modelling.

**Example (real run, lognormal income, 10,000 people):** mean 98,359 vs median 59,321, std 120,084, skewness 4.00. Percentiles: P25 30,762, P75 119,468, P90 215,894, P99 604,051. After `log`, skewness is -0.03 (symmetric).

**Code:**
```python
import numpy as np
from scipy.stats import skew
rng = np.random.default_rng(0)
inc = rng.lognormal(mean=11, sigma=1, size=10000)
print(inc.mean(), np.median(inc), skew(inc))         # mean >> median, skew ~4
print(np.percentile(inc, [25, 75, 90, 99]).round(0))
print(skew(np.log(inc)))                              # ~0
```

**Follow-ups:**
- *Which central measure for normal data?* All agree; use the mean.
- *Any reason to report the mean?* Yes for totals or revenue per user, where tail contributions matter.

**Common mistakes:** Reporting only the mean; interpreting std as meaningful for heavy tails; confusing mean/median ordering with skew direction.

### Q18 ⭐⭐ 🟢 Stratified, random and cluster sampling; what is sampling bias and selection bias in training data?
**Asked at:** Amazon, Walmart, Europe product cos
**Say this first (1 line):** Random sampling picks rows uniformly, stratified sampling preserves group proportions (e.g. class balance), cluster sampling picks whole groups; and bias arises when the sample doesn't represent the population the model will serve.

**Then explain:**
- **Simple random:** every row has equal chance. Fine for large, balanced data.
- **Stratified:** split into strata (class, region) and sample within each, so rare groups are guaranteed to appear. Use it for train/test splits on imbalanced labels.
- **Cluster:** randomly pick whole clusters (cities, stores, schools) and use all rows in them. Cheaper, but less precise because rows in a cluster are alike.
- **Sampling bias:** the collection method over- or under-represents part of the population (e.g. surveying only app users).
- **Selection bias:** which rows get a label or enter the data is not random. Example: loan models trained only on approved applicants never see the rejected ones (reject inference problem). Related: survivorship bias, non-response bias.
- **Fix:** reweighting, stratified collection, exploration traffic, evaluating on a representative holdout.

**Example (real run):** 2% positive rate, 500-row sample, 200 random splits. Plain random test sets had positive rate between 0.000 and 0.060; stratified splits always gave 0.020.

**Code:**
```python
from sklearn.model_selection import train_test_split
tr, te = train_test_split(df, test_size=.2, random_state=0, stratify=df["y"])
```

**Follow-ups:**
- *Stratify on what?* The label, and possibly an important segment.
- *Does stratifying fix selection bias?* No, it only controls proportions within the data you have.

**Common mistakes:** Mixing up sampling bias (collection) with selection bias (who gets in or labelled); using stratified sampling on the full data when the test distribution should mirror production; random-splitting grouped data.

### Q19 ⭐⭐ 🟡 Tell me conditional probability and Bayes' rule, then explain how Naive Bayes uses them and why 'naive'.
**Asked at:** Flipkart, Amazon, Microsoft IDC, GCCs
**Say this first (1 line):** Conditional probability is P(A|B) = P(A and B) / P(B); Bayes' rule flips it: P(A|B) = P(B|A) P(A) / P(B); Naive Bayes applies it to classify, assuming features are independent given the class, which is the "naive" part.

**Then explain:**
- **Bayes' rule in words:** posterior = likelihood x prior / evidence. Prior is what you believed before, likelihood is how well the data fits that hypothesis.
- **Naive Bayes:** `P(class | x1..xn) ∝ P(class) * Π P(xi | class)`. Pick the class with the highest score. The evidence term is the same for every class, so you drop it.
- **Why naive:** it assumes features are conditionally independent given the class. Words like "win" and "cash" are clearly correlated, so the assumption is false, but the ranking of classes is often still right.
- **Why it works anyway:** it needs few parameters (one per feature per class), trains in one pass by counting, is fast, and handles high-dimensional sparse text well. Its probabilities are usually overconfident, so calibrate them if you need real probabilities.
- **Practical details:** use Laplace smoothing (add alpha to counts) so an unseen word does not zero out the whole product; work in log space to avoid underflow. Variants: Gaussian, Multinomial (counts), Bernoulli (presence).

**Example (real run):** a disease affects 1% of people, the test catches 90% of cases and has a 5% false-positive rate. P(disease | positive) = 0.9*0.01 / (0.9*0.01 + 0.05*0.99) = **0.154**, not 0.9. The low prior dominates.

**Code:**
```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
docs = ["win cash now", "win prize now", "meeting at noon", "lunch at noon",
        "cash prize win", "project meeting today"]
y = [1, 1, 0, 0, 1, 0]                       # 1 = spam
cv = CountVectorizer(); X = cv.fit_transform(docs)
m = MultinomialNB(alpha=1).fit(X, y)         # alpha=1 is Laplace smoothing
print(m.predict_proba(cv.transform(["win cash prize"])).round(3))   # [[0.027 0.973]]
print(m.predict(cv.transform(["meeting today noon"])))              # [0]
```

**Follow-ups:**
- *Generative or discriminative?* Generative: it models P(x|class) and P(class).
- *What if two features are duplicates?* Their evidence is counted twice, so the model becomes overconfident; remove duplicates.
- *Why log space?* Multiplying hundreds of small probabilities underflows to 0; summing logs is stable.

**Common mistakes:** Forgetting smoothing (zero-probability problem); saying "naive" means the model is bad; trusting its predicted probabilities as calibrated; ignoring the base rate in the Bayes example.

### Q20 ⭐⭐ 🟡 Your model has 99% train accuracy and 70% validation accuracy. What do you check and change, in order?
**Asked at:** Fractal, Swiggy, PhonePe, scenario rounds
**Say this first (1 line):** That is overfitting, but first I rule out leakage and a broken split, then I reduce variance with more data, simpler models and regularization, and I re-check on validation after each change.

**Then explain (in order):**
1. **Is the gap real?** Check the split is clean: no duplicates or same-user rows across train and val, no preprocessing fitted on train+val, same distribution (a time or group shift can create a gap with no overfitting). Check the metric is computed the same way on both sets.
2. **Is it a leak in the other direction?** Train accuracy of 99% on noisy data is itself suspicious: a target-leaking feature or an ID-like feature lets the model memorise.
3. **Diagnose with a learning curve:** if the gap closes as data grows, more data helps; if both curves are flat, it is not a variance problem.
4. **Reduce variance:** more or better data, augmentation; fewer or cleaner features; simpler model (`max_depth`, `min_samples_leaf`, fewer parameters); regularization (L1/L2, dropout); early stopping; bagging.
5. **Tune with CV**, not the test set, and report the CV std.
6. **Accept the noise floor:** 70% may be near the Bayes error if labels are noisy.

**Example (real run):** random forest on a noisy 2,000-row problem: default gives train 1.00 / val 0.88. With `max_depth=5, min_samples_leaf=20`: train 0.855 / val 0.842. The gap shrinks from 0.12 to 0.01 but validation also drops slightly, so here the unconstrained forest was actually the better model; the lesson is to compare on validation, not on the gap.

**Code:**
```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
X, y = make_classification(2000, 30, n_informative=5, flip_y=.1, random_state=0)
Xt, Xv, yt, yv = train_test_split(X, y, test_size=.3, random_state=0)
for kw in [{}, dict(max_depth=5, min_samples_leaf=20)]:
    r = RandomForestClassifier(random_state=0, **kw).fit(Xt, yt)
    print(kw, round(r.score(Xt, yt), 3), round(r.score(Xv, yv), 3))
# {} 1.0 0.88 | {'max_depth': 5, 'min_samples_leaf': 20} 0.855 0.842
```

**Follow-ups:**
- *Train 99% is normal for a random forest, right?* Yes, trees can fit train data; judge by validation, not the gap alone.
- *What if validation is 70% because of drift?* Then regularizing will not help; split by time and add recent data.

**Common mistakes:** Jumping straight to regularization without checking leakage or split; tuning on the test set; treating a smaller gap as a better model.

### Q21 ⭐⭐ 🟡 How do you split data for time-series, grouped (user-level) or duplicated data? Why does random k-fold leak there?
**Asked at:** Klarna, Booking, Swiggy, PhonePe
**Say this first (1 line):** Split the way production will see data: by time for time series, by entity (GroupKFold) for user-level data, and deduplicate first; random k-fold leaks because near-identical or future rows land on both sides.

**Then explain:**
- **Time series:** train on the past, validate on the future. Use `TimeSeriesSplit` (expanding window) or a rolling window; leave a gap if features use lags or the label horizon overlaps.
- **Grouped data:** all rows of one user/patient/device go to the same fold (`GroupKFold`, or `StratifiedGroupKFold` with imbalance). Otherwise the model memorises the user.
- **Duplicates:** drop exact and near-duplicates (hash, fuzzy match, embedding similarity) before splitting, or treat each duplicate cluster as a group.
- **Why random k-fold leaks:** (a) rows from the same entity are correlated, so validation is easy; (b) in time series the model sees the future; (c) duplicate rows appear in both train and validation. Scores look great and production collapses.
- Always fit preprocessing inside the CV loop and keep a final holdout split the same way.

**Example (real run of the code below):** 200 users x 10 rows, label random per user, each row is its user's feature vector plus tiny noise, 3-nearest-neighbour model. Random KFold accuracy 1.00; GroupKFold 0.54 (chance is 0.5). `TimeSeriesSplit(3)` on 12 points gives train/test `[0-2]/[3-5]`, `[0-5]/[6-8]`, `[0-8]/[9-11]`: train always precedes test.

**Code:**
```python
import numpy as np
from sklearn.model_selection import KFold, GroupKFold, TimeSeriesSplit, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
rng = np.random.default_rng(0)
user_id = np.repeat(np.arange(200), 10)
y = rng.integers(0, 2, 200)[user_id]                                # label random per user
X = rng.normal(size=(200, 5))[user_id] + rng.normal(0, .05, (2000, 5))
model = KNeighborsClassifier(3)
print(cross_val_score(model, X, y, cv=KFold(5, shuffle=True, random_state=0)).mean())   # 1.0 (leaky)
print(cross_val_score(model, X, y, cv=GroupKFold(5), groups=user_id).mean())            # ~0.54
for tr, te in TimeSeriesSplit(3).split(np.arange(12)): print(tr, te)   # train always before test
```

**Follow-ups:**
- *Final test split?* Same rule: last weeks of data, or held-out users.
- *New users in production?* Then group by user; if the model only scores known users, a time split may be enough.

**Common mistakes:** Shuffling time series; GroupKFold without stratification on rare classes (empty positives in folds); splitting before deduplicating; computing lag features across the split boundary.

### Q22 ⭐⭐ 🟡 How do you handle missing values? Compare dropping, mean/median, model-based imputation and missing-indicator features; when is missingness informative?
**Asked at:** Flipkart, Swiggy, Walmart, analytics firms
**Say this first (1 line):** First understand why values are missing (MCAR, MAR, MNAR), then pick the simplest method that is fitted on train only: drop if few and random, median/mode for a baseline, model-based imputation for important features, and add a missing-indicator when missingness carries signal.

**Then explain:**

| Method | Good for | Watch out |
|---|---|---|
| Drop rows | Very few missing, completely random | Loses data; biases sample if not random |
| Drop column | >60-70% missing and low value | May lose an informative flag |
| Mean/median/mode | Fast baseline | Shrinks variance, distorts correlations; median for skewed |
| Model-based (KNN, iterative/MICE) | Features correlated with each other | Costly; fit inside CV to avoid leakage |
| Missing-indicator column | Missingness is informative | Doubles columns |
| Native handling (XGBoost, LightGBM, HistGradientBoosting) | Trees | Learns a default direction for NaN |

- **MCAR:** missing at random completely; **MAR:** depends on other observed columns; **MNAR:** depends on the missing value itself (high earners hide income).
- **Informative missingness:** "income not provided", "no previous loan" often predict the target. Do not hide it.

**Example (real run of the code below):** 2,000 rows, x predicts y (class means 0 and 1), but x is missing 52% of the time when y=1 and 5% when y=0. Median imputation alone: CV AUC 0.702. Median + missing-indicator: **0.865**.

**Code:**
```python
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
rng = np.random.default_rng(0)
y = rng.integers(0, 2, 2000); x = rng.normal(y * 1.0, 1)
miss = rng.random(2000) < np.where(y == 1, .52, .05)
X = np.where(miss, np.nan, x)[:, None]
for ind in [False, True]:   # add_indicator adds the missing flag; the pipeline fits it per fold
    p = make_pipeline(SimpleImputer(strategy="median", add_indicator=ind), LogisticRegression())
    print(ind, cross_val_score(p, X, y, cv=5, scoring="roc_auc").mean().round(3))   # 0.702, 0.865
```

**Follow-ups:**
- *Multiple imputation?* Impute several times with noise and pool results, to keep uncertainty honest.
- *Impute the target?* No; drop rows with missing labels.

**Common mistakes:** Imputing before the split; mean imputation on skewed data; ignoring why data is missing; imputing with the test set's statistics.

### Q23 ⭐⭐ 🟡 Grid search vs random search vs Bayesian optimisation. What is nested cross-validation and why use it?
**Asked at:** Amazon, Zalando, GCCs
**Say this first (1 line):** Grid search tries every combination, random search samples combinations and usually finds a good one faster, Bayesian optimisation uses past results to choose the next trial, and nested CV gives an unbiased score for the whole tuning procedure.

**Then explain:**
- **Grid:** exhaustive; cost grows exponentially with the number of hyperparameters; wastes trials on unimportant ones.
- **Random:** each trial draws every parameter independently. Since usually only a few hyperparameters matter, it tries many more distinct values of those (Bergstra & Bengio). Use log-uniform for learning rate or C.
- **Bayesian (Optuna/TPE, Gaussian-process):** builds a model of score vs params and picks promising points. Best when each trial is expensive; supports pruning bad trials early.
- **Nested CV:** outer loop estimates performance, inner loop (inside each outer training fold) does the tuning. The tuned CV score is optimistically biased because the best-of-many config was picked on those same folds; nested CV scores the *procedure* on data it never tuned on.
- Use it to compare model families or report a performance estimate on small data. For big data a fixed holdout is enough.

**Example (real run):** 100 rows, 200 features, mostly noise, SVM grid of 20 combos, 5-fold. Best flat CV score: 0.53; nested CV: 0.47 (chance is 0.5 here, so the truth is ~0.5; the flat score is the optimistic one, and with 100 rows the numbers are noisy).

**Code:**
```python
import numpy as np
from sklearn.model_selection import GridSearchCV, cross_val_score, KFold
from sklearn.svm import SVC
rng = np.random.default_rng(0)
X = rng.normal(size=(100, 200)); y = rng.integers(0, 2, 100)      # pure noise
gs = GridSearchCV(SVC(), {"C": [.01, .1, 1, 10, 100], "gamma": [1e-4, 1e-3, 1e-2, 1e-1]},
                  cv=KFold(5, shuffle=True, random_state=0))
nested = cross_val_score(gs, X, y, cv=KFold(5, shuffle=True, random_state=1))
print(nested.mean(), gs.fit(X, y).best_score_)   # 0.47 (honest) vs 0.53 (optimistic best_score_)
```

**Follow-ups:**
- *Cost of nested CV?* outer k x inner k x grid size fits.
- *Final model?* Refit the tuned procedure on all training data.

**Common mistakes:** Reporting `best_score_` as the expected performance; grid-searching a wide linear grid for the learning rate; tuning on the test set; scaling outside the CV pipeline.

### Q24 ⭐⭐ 🟡 Parametric vs non-parametric models, and generative vs discriminative models: definitions and examples.
**Asked at:** Microsoft IDC, Amazon, research-leaning roles
**Say this first (1 line):** Parametric models have a fixed number of parameters regardless of data size; non-parametric models grow their complexity with the data. Separately, generative models learn how the data is produced, P(x, y), while discriminative models learn the boundary P(y|x) directly.

**Then explain:**

| Axis | Type | Examples | Trade-off |
|---|---|---|---|
| Parametric | Fixed-size parameter vector | Linear/logistic regression, Naive Bayes, small neural nets | Fast, needs little data, but assumes a functional form (bias) |
| Non-parametric | Complexity grows with n | KNN, decision trees, kernel SVM, Gaussian processes | Flexible, needs more data, slower at prediction (KNN stores everything) |
| Generative | Models P(x|y) P(y) | Naive Bayes, LDA/QDA, GMM, HMM, VAEs, GANs, LLMs | Can sample new data, handle missing features; often less accurate for pure classification |
| Discriminative | Models P(y|x) | Logistic regression, SVM, trees, boosting, most neural classifiers | Usually higher accuracy with enough data |

- "Non-parametric" does not mean no parameters; it means no fixed number.
- Axes are independent: Naive Bayes is parametric and generative; KNN is non-parametric and discriminative; logistic regression is parametric and discriminative.
- Classic result (Ng & Jordan): the generative Naive Bayes reaches its (higher) error with fewer samples; logistic regression wins with more data.

**Example:** Spam filter with 200 labelled emails: Naive Bayes (generative) is competitive. With 2 million emails: gradient boosting or a fine-tuned transformer (discriminative) wins.

**Follow-ups:**
- *Is a neural net parametric?* Yes, fixed weights; though very wide nets behave almost non-parametrically.
- *Is an LLM generative or discriminative?* Generative (models P(next token | context)), though it can be used for classification.

**Common mistakes:** Saying non-parametric means "no parameters"; calling every classifier discriminative; saying generative = deep learning (Naive Bayes is generative).

### Q25 ⭐⭐ 🟡 Why does vectorised NumPy beat Python loops? Explain broadcasting and compute pairwise Euclidean distances without a loop.
**Asked at:** MLE live-coding, Microsoft IDC, Booking
**Say this first (1 line):** NumPy pushes the loop into compiled C code that works on contiguous memory with SIMD, so one call does a million operations without Python's per-iteration overhead; broadcasting lets arrays of different shapes combine without copying.

**Then explain:**
- **Why faster:** a Python loop pays interpreter cost (type checks, object boxing) on every element; NumPy arrays are typed and contiguous, so C/BLAS loops run at hardware speed and use the CPU cache and SIMD well.
- **Broadcasting rules:** compare shapes from the right; two dims are compatible if equal or one is 1; the size-1 dim is virtually stretched (no copy). Shape (1000,1,16) with (1,500,16) gives (1000,500,16).
- **Pairwise distances without a loop:** use `||a-b||² = ||a||² + ||b||² - 2 a·b`, which turns the work into one matrix multiplication (BLAS). It needs O(n*m) memory instead of the O(n*m*d) of the naive broadcast difference.
- **Numerical caution:** the expansion can give tiny negatives from rounding; clip at 0 before `sqrt`.

**Example (real run):** sum of squares of 1,000,000 numbers: a Python generator took about 0.3-0.4 s vs NumPy about 0.01-0.09 s across three runs on a loaded laptop (roughly 3-60x; timings are noisy, so measure with `timeit` on your machine).

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
A = rng.normal(size=(1000, 16)); B = rng.normal(size=(500, 16))
D = np.sqrt(np.maximum((A**2).sum(1)[:, None] + (B**2).sum(1)[None] - 2 * A @ B.T, 0))
D2 = np.sqrt(((A[:, None, :] - B[None, :, :]) ** 2).sum(-1))   # simple but O(n*m*d) memory
print(D.shape, np.allclose(D, D2))   # (1000, 500) True
```

**Follow-ups:**
- *Is a view or a copy made?* Broadcasting makes a view; the `A[:, None] - B[None]` result is a real new array.
- *Too big for memory?* Process in chunks; for nearest neighbours use FAISS/ANN.

**Common mistakes:** Using `np.vectorize` (it is still a Python loop); building the 3-D difference array for large n; forgetting `keepdims`/axis shapes; not clipping before `sqrt`.

### Q26 ⭐⭐ 🟡 Implement train_test_split and stratified k-fold from scratch (no sklearn). How do you guarantee reproducibility?
**Asked at:** MLE screens, GCC coding rounds
**Say this first (1 line):** Reproducibility comes from a seeded random generator creating a permutation of indices; for stratified k-fold I permute each class separately and deal its indices round-robin into folds, so every fold keeps the class ratio.

**Then explain:**
- **Split:** `rng = np.random.default_rng(seed)`, `idx = rng.permutation(n)`, first `k` indices go to test.
- **Stratified k-fold:** for each class, shuffle its indices, cut into k nearly equal parts with `np.array_split`, and add part i to fold i.
- **Reproducibility:** fix the seed everywhere (split, model, `PYTHONHASHSEED`, framework seeds), pass a local `Generator` rather than the global state, save the split indices or a data version, and pin library versions.

**Example (real run):** 90 negatives + 10 positives, 5 folds: each test fold has 20 rows with exactly 2 positives; two calls with the same seed return the same indices.

**Code:**
```python
import numpy as np

def my_split(n, test_size=.2, seed=0):
    idx = np.random.default_rng(seed).permutation(n)
    k = int(round(n * test_size))
    return idx[k:], idx[:k]                       # train_idx, test_idx

def strat_kfold(y, k=5, seed=0):
    rng = np.random.default_rng(seed)
    folds = [[] for _ in range(k)]
    for c in np.unique(y):
        idx = rng.permutation(np.where(y == c)[0])
        for i, part in enumerate(np.array_split(idx, k)):
            folds[i] += part.tolist()
    for i in range(k):
        te = np.array(sorted(folds[i]))
        yield np.setdiff1d(np.arange(len(y)), te), te

y = np.array([0] * 90 + [1] * 10)
for tr, te in strat_kfold(y):
    print(len(te), y[te].sum())                   # 20 2 on every fold
```

**Follow-ups:**
- *Group-aware version?* Shuffle group ids, assign groups to folds, and take all their rows.
- *Why not `np.random.seed`?* Global state is shared and easy to disturb; a local Generator is isolated.

**Common mistakes:** Splitting without shuffling sorted data; stratifying only on train; a class with fewer samples than k (some folds get no positives); forgetting that `random_state=None` is non-reproducible.

### Q27 ⭐⭐ 🟡 Implement softmax and cross-entropy in NumPy in a numerically stable way (log-sum-exp).
**Asked at:** Amazon, deep-learning-leaning MLE loops
**Say this first (1 line):** Subtract the row max before exponentiating, and compute cross-entropy as log-sum-exp minus the true-class logit, never as `log(softmax)`.

**Then explain:**
- **Softmax:** `p_i = exp(z_i) / Σ exp(z_j)`. It is unchanged if you subtract a constant from all logits, so subtract `max(z)`: the largest exponent becomes `exp(0)=1`, no overflow.
- **Cross-entropy for true class y:** `-log p_y = logsumexp(z) - z_y`. With `logsumexp(z) = m + log Σ exp(z - m)` this never takes `log(0)`.
- **Gradient** wrt logits: `softmax(z) - onehot(y)`, divided by batch size for the mean loss.

**Example (real run):** logits `[1000,1001,1002]`: naive softmax gives `[nan nan nan]`; the stable version gives `[0.09, 0.245, 0.665]`. With a second row `[2,1,0.1]`, true classes `[2,0]`, the mean loss is 0.4123.

**Code:**
```python
import numpy as np
def softmax(z):
    z = z - z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)

def cross_entropy(logits, y):
    m = logits.max(1, keepdims=True)
    lse = m[:, 0] + np.log(np.exp(logits - m).sum(1))
    return (lse - logits[np.arange(len(y)), y]).mean()

z = np.array([[1000., 1001., 1002.], [2., 1., .1]]); y = np.array([2, 0])
print(softmax(z).round(3).tolist(), round(cross_entropy(z, y), 4))
# [[0.09, 0.245, 0.665], [0.659, 0.242, 0.099]] 0.4123
```

**Follow-ups:**
- *Why not `np.log(softmax(z))`?* A tiny probability underflows to 0 and `log(0) = -inf`.
- *Binary case?* Same idea: sigmoid with `log1p` / `BCEWithLogits`.

**Common mistakes:** Subtracting the max over the whole matrix instead of per row; forgetting `keepdims`; passing probabilities into a loss that expects logits (double softmax).

### Q28 ⭐⭐ 🟡 Your model is great offline but poor in production. List the causes (train-serve skew, drift, leakage, label delay) and how to investigate.
**Asked at:** Swiggy, Flipkart, Spotify, Zalando, senior loops
**Say this first (1 line):** Offline-online gaps almost always come from the data the model sees in production being different from training: train-serve skew, drift, leakage, or labels that arrive late; I investigate by logging live features and comparing them to training.

**Then explain:**

| Cause | What it looks like | How to check |
|---|---|---|
| Leakage in offline eval | Too-good offline score, drops on time-based holdout | Feature "available at prediction time?" audit; time/group split |
| Train-serve skew | Same feature computed differently (SQL vs service code, units, null handling, tokenizer) | Log served features, recompute offline for the same IDs, diff |
| Data/concept drift | Input or label relationship changes over time | PSI/KS per feature, performance by week |
| Selection / feedback loop | Model only sees rows it already chose | Exploration traffic, counterfactual eval |
| Label delay | Recent performance unknown (fraud chargebacks arrive in 60 days) | Use proxy metrics, wait-and-backfill, cohort-based monitoring |
| Metric mismatch | AUC fine but business KPI poor; threshold wrong | Align metric, re-tune threshold, A/B test |
| Infra | Latency timeouts, stale features, fallback paths | Serving logs, null-rate dashboards |

- **Investigation order:** (1) is the serving pipeline healthy and the features populated? (2) replay production inputs through the offline pipeline and compare predictions; (3) compare feature distributions; (4) evaluate on a recent labelled slice; (5) segment by cohort.
- **Prevention:** shared feature code or a feature store, point-in-time joins, shadow mode, canary release, monitoring with alerts.

**Example (illustrative scenario, not a run):** A delivery-time model has MAE 4 min offline but 7 in production. Replaying logged requests shows "distance" was in km in training and metres-rounded-to-km in serving, a skew bug; fixing it restores 4.2.

**Follow-ups:**
- *Offline fine, A/B flat?* Offline metric may not track the business goal, or position/novelty effects.
- *How do you monitor without labels?* Input drift, prediction-distribution drift, proxy metrics.

**Common mistakes:** Assuming drift without checking for a pipeline bug first; retraining blindly; monitoring only accuracy and not input features.

### Q29 ⭐⭐ 🟡 Explain interpretability vs accuracy trade-off: when would you pick a simpler model, and how do you explain a model to non-technical stakeholders?
**Asked at:** Klarna, Fractal, Walmart, JPMC GCC
**Say this first (1 line):** Simpler models are easier to explain, debug and audit, complex ones often score higher; I pick the simple model when the accuracy gain is small or when regulation, trust or debugging matter, and I use explanation tools when I need the complex one.

**Then explain:**
- **Pick simple (logistic regression, small tree, GAM) when:** regulated decisions (credit, insurance, hiring) need reason codes; data is small or tabular with a strong linear signal; stakeholders must trust and act on it; the gain from a complex model is under about 1-2 points of the business metric.
- **Pick complex (boosting, deep nets) when:** the accuracy gain is worth real money (ranking, fraud, ads), interactions are strong, or data is unstructured.
- **Trade-off is not always real:** on tabular data a tuned logistic regression is often within a point of boosting. Always benchmark a simple baseline.
- **Explaining to non-technical people:** start with the decision and the business effect, not the algorithm; use 2-3 top drivers per prediction (SHAP / reason codes), a worked example customer, and a plain metric ("catches 8 of 10 fraud cases, flags 1 in 50 good customers"); show partial-dependence or "what-if" views; state limits and what the model does not know.
- **Caveats:** SHAP and feature importance show what the model uses, not causes; correlated features share credit.

**Example:** Credit scoring: a scorecard logistic regression with 12 binned features gives every rejected applicant a reason ("2 late payments in 6 months"). A boosted model adds 1 AUC point but needs SHAP and governance, so many banks keep the scorecard, or use boosting with monotonic constraints.

**Follow-ups:**
- *Post-hoc vs intrinsic interpretability?* Intrinsic (linear, tree, GAM) is faithful by construction; post-hoc (SHAP, LIME) approximates a black box.
- *What would you tell a stakeholder who asks "why this prediction"?* Top contributing factors, plus how the result changes if they change.

**Common mistakes:** Assuming complex always wins; presenting SHAP as causal; using AUC jargon with business audiences; ignoring legal requirements for explanations.

### Q30 ⭐⭐ 🟡 AI-era code review: an LLM wrote this sklearn pipeline (scaler fit on all data, random split on time-ordered data, test set used for tuning). Find the bugs.
**Asked at:** AI-era loops: Meta-style, product cos, MLE live-coding rounds
**Say this first (1 line):** There are four bugs: scaling before the split (preprocessing leakage), a random split on time-ordered data (temporal leakage), tuning on the test set (selection leakage), and the scaler not being inside a pipeline; the reported score is too optimistic.

**Buggy snippet (typical LLM output; an excerpt, not standalone; the runnable demo below has both versions):**
```python
X = StandardScaler().fit_transform(X)                         # BUG 1: fit on all data
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.2, random_state=0)   # BUG 2: random split, time data
g = GridSearchCV(RandomForestRegressor(random_state=0), {"max_depth": [None, 3, 8]}, cv=3)
g.fit(Xtr, ytr)
print(g.score(Xte, yte))                                      # BUG 3: test used to judge/choose, reported as final
```
*(A tempting variant picks the best config by test score in a loop, which is the same bug 3.)*

**Bugs and fixes:**
1. **Scaler fit on all data:** test mean/std leak into training. Put the scaler in a `Pipeline` so it is fit on training folds only.
2. **Random split on time-ordered data:** train contains the future, test sits among the past; neighbouring rows are near-duplicates. Split by time (last 20% as test) and tune with `TimeSeriesSplit`.
3. **Tuning plus reporting on test:** if config choice uses test, the test score is optimistic. Tune with CV on train only; touch test once.
4. **Also check:** `cv=3` default is not shuffled/time-aware, features computed with future aggregates, missing seed, no baseline.

**Fixed:**
```python
k = int(len(y) * .8)
pipe = make_pipeline(StandardScaler(), RandomForestRegressor(random_state=0, n_estimators=50))
gs = GridSearchCV(pipe, {"randomforestregressor__max_depth": [None, 3, 8]},
                  cv=TimeSeriesSplit(3)).fit(X[:k], y[:k])
print(gs.score(X[k:], y[k:]))
```

**Runnable demo (standalone, runs both versions):**
```python
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
rng = np.random.default_rng(0)
n = 600; t = np.arange(n)
X = np.c_[t, np.sin(2 * np.pi * t / 50), rng.normal(size=n)]      # time index, season, noise feature
y = 0.05 * t + 3 * np.sin(2 * np.pi * t / 50) + rng.normal(0, 1, n)   # trend + seasonality
# buggy
Xs = StandardScaler().fit_transform(X)
Xtr, Xte, ytr, yte = train_test_split(Xs, y, test_size=.2, random_state=0)
g = GridSearchCV(RandomForestRegressor(random_state=0), {"max_depth": [None, 3, 8]}, cv=3).fit(Xtr, ytr)
print("buggy R2", round(g.score(Xte, yte), 3))                     # 0.983
# fixed
k = int(len(y) * .8)
pipe = make_pipeline(StandardScaler(), RandomForestRegressor(random_state=0, n_estimators=50))
gs = GridSearchCV(pipe, {"randomforestregressor__max_depth": [None, 3, 8]},
                  cv=TimeSeriesSplit(3)).fit(X[:k], y[:k])
print("honest R2", round(gs.score(X[k:], y[k:]), 3))               # -1.995
```

**Example (real run of the demo above, 600 points with trend + seasonality):** buggy version test R² 0.983; time-split pipeline test R² -1.995. The buggy number looked great because the random split interpolates between neighbouring points; the honest number shows the forest cannot extrapolate the trend into the future (the future `t` values are outside anything it saw), which is the real production risk. The exact values depend on the synthetic data and seed; the gap is the point.

**Follow-ups:**
- *Is scaling leakage really that big?* Often small for scalers, huge for target encoding or feature selection; it is still wrong and trivially avoidable.
- *How do you review LLM-generated ML code?* Check the split, what is fit on what, metric choice, seeds, and whether the evaluation matches production.

**Common mistakes:** Trusting a high score from generated code; fixing only the scaler and leaving the random split; using test set for early stopping.

### Q31 ⭐ 🟡 Why does MSE pair with regression and cross-entropy with classification? Explain MLE vs MAP in one minute.
**Asked at:** Research-leaning roles, Amazon applied scientist
**Say this first (1 line):** If you assume Gaussian noise, maximising likelihood is the same as minimising MSE; if you assume Bernoulli/categorical labels, it is the same as minimising cross-entropy; MAP is MLE plus a prior, which acts as regularization.

**Then explain:**
- **Regression:** `y = f(x) + ε`, `ε ~ N(0, σ²)`. Negative log-likelihood = `Σ (y - f(x))² / (2σ²)` + constant, so MLE = least squares.
- **Classification:** with `y ~ Bernoulli(p)`, NLL = `-Σ [y log p + (1-y) log(1-p)]` = binary cross-entropy; for K classes with softmax it is categorical cross-entropy. It is also the KL divergence between true and predicted label distributions (up to a constant).
- **MLE:** `θ̂ = argmax P(data | θ)`. Uses data only.
- **MAP:** `θ̂ = argmax P(data | θ) P(θ)`. Gaussian prior on weights = L2 (ridge); Laplace prior = L1 (lasso). With lots of data, the prior matters less and MAP approaches MLE.
- **Why not MSE for classification:** with a sigmoid it gives a non-convex loss and weak gradients when the model is confidently wrong; cross-entropy penalises that heavily and has the clean gradient `p - y`.

**Example:** A coin shows 3 heads in 3 tosses. MLE says P(heads) = 1.0. MAP with a Beta(2,2) prior gives (3+1)/(3+2) = 0.8, a more sensible estimate.

**Follow-ups:**
- *Is MSE wrong if noise is not Gaussian?* With heavy tails, MAE/Huber (Laplace-like noise) is more robust.
- *Fully Bayesian?* Keeps the whole posterior rather than one point.

**Common mistakes:** Saying MSE is "just chosen because it is convex"; confusing MAP with Bayesian inference; forgetting that the L2 strength relates to the prior variance.

### Q32 ⭐ 🟡 Explain bootstrap and bagging intuition: why does resampling and averaging reduce variance?
**Asked at:** Amazon, Microsoft IDC, senior loops
**Say this first (1 line):** Bootstrap resamples the data with replacement to mimic fresh samples; bagging trains one model per resample and averages them, and because averaging noisy, partly independent estimates cancels noise, variance drops while bias stays about the same.

**Then explain:**
- **Bootstrap sample:** draw n rows with replacement. About 63.2% of unique rows appear; the other ~36.8% (`(1-1/n)^n → 1/e`) are out-of-bag (OOB) and give a free validation estimate.
- **Why averaging helps:** for B models with variance σ² and pairwise correlation ρ, the average has variance `ρσ² + (1-ρ)σ²/B`. More models kill the second term; the first term (correlation) remains, which is why random forests also randomise the features to lower ρ.
- **Works best for high-variance, low-bias learners** (deep trees). Does little for stable models (linear regression, shallow trees).
- **Bootstrap also** gives confidence intervals: resample, recompute the statistic, take percentiles.

**Example (real run of the code below):** noisy sine data (100 points, noise std 0.3), prediction at x=0.3, 100 repeated training sets: variance of a single deep tree 0.078; of a 30-tree bagged ensemble 0.045. Fraction of unique rows in a bootstrap sample (n=1000): 0.632, so out-of-bag is 0.368 = 1/e.

**Code:**
```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor
rng = np.random.default_rng(0)
def bagged_predict(x, y, x0, B=30):
    preds = []
    for _ in range(B):
        i = rng.integers(0, len(x), len(x))               # sample with replacement
        preds.append(DecisionTreeRegressor().fit(x[i], y[i]).predict(x0)[0])
    return np.mean(preds)

x0 = np.array([[0.3]]); single, bag = [], []
for _ in range(100):                                    # 100 fresh training sets
    x = rng.uniform(0, 1, (100, 1)); y = np.sin(2 * np.pi * x[:, 0]) + rng.normal(0, .3, 100)
    single.append(DecisionTreeRegressor().fit(x, y).predict(x0)[0]); bag.append(bagged_predict(x, y, x0))
print(np.var(single), np.var(bag))                      # ~0.078 vs ~0.045
n = 1000
print(np.mean([len(np.unique(rng.integers(0, n, n))) / n for _ in range(200)]))   # ~0.632
```

**Follow-ups:**
- *Bagging vs boosting?* Bagging: parallel, cuts variance. Boosting: sequential, cuts bias.
- *Why do random forests subsample features?* To decorrelate trees (lower ρ).

**Common mistakes:** Saying bagging reduces bias; thinking more trees can overfit (it plateaus); sampling without replacement and calling it bootstrap.

### Q33 ⭐ 🟡 Write a gradient check (numerical vs analytical gradient) for your from-scratch model. Why is it useful?
**Asked at:** Deep-learning-leaning MLE loops
**Say this first (1 line):** A gradient check compares my analytical gradient with a finite-difference estimate `(L(w+ε) - L(w-ε)) / 2ε`; if the relative error is around 1e-7 or smaller the backprop code is right, and a large error means a bug.

**Then explain:**
- **Why useful:** hand-written gradients are easy to get subtly wrong (missing 1/n, transposed matrix, sign). The model still "trains" a bit, so bugs hide. The check catches them before you waste days.
- **How:** perturb one parameter at a time using the central difference (error O(ε²)); use float64, ε about 1e-5; compare with relative error `||g - g_num|| / (||g|| + ||g_num||)`.
- **Practical rules:** run on a tiny model/batch; turn off dropout and randomness; don't use at kinks (ReLU at 0); it is O(#params) loss evaluations, so never use it for training.
- **Today:** autograd frameworks make this rare, but it is still the standard test for custom layers and losses.

**Example (real run, logistic regression, 50 rows):** correct gradient relative error about 3e-11; with a deliberately wrong gradient (scaled by 2) relative error 0.33.

**Code:**
```python
import numpy as np
def loss_grad(w, X, y):
    p = 1 / (1 + np.exp(-X @ w))
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)), X.T @ (p - y) / len(y)

def grad_check(fn, w, X, y, eps=1e-5):
    _, g = fn(w, X, y); num = np.zeros_like(w)
    for i in range(len(w)):
        d = np.zeros_like(w); d[i] = eps
        num[i] = (fn(w + d, X, y)[0] - fn(w - d, X, y)[0]) / (2 * eps)
    return np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num))

rng = np.random.default_rng(0)
X = rng.normal(size=(50, 3)); y = (rng.random(50) < .5).astype(float); w = rng.normal(size=3) * .5
print(grad_check(loss_grad, w, X, y))                                    # correct: ~3e-11
bad = lambda w, X, y: (loss_grad(w, X, y)[0], 2 * loss_grad(w, X, y)[1])  # deliberate bug
print(grad_check(bad, w, X, y))                                          # ~0.33
```

**Follow-ups:**
- *Why central, not forward, difference?* Error O(ε²) instead of O(ε).
- *Relative error 1e-4?* Suspicious; check ε, float precision, non-differentiable points, then the code.

**Common mistakes:** Using float32; absolute instead of relative error; checking with dropout on; leaving the check enabled in training.

### Q34 ⭐ 🟡 AI-era follow-up: how can benchmark/test contamination happen when fine-tuning or evaluating an LLM, and how is it the same as classical data leakage?
**Asked at:** GenAI-leaning DS loops, Fractal-style GenAI scenario rounds
**Say this first (1 line):** Contamination is when benchmark questions or answers were in the model's pretraining or fine-tuning data, so the score measures memorisation, not ability; it is the same as classical test-set leakage, just at web scale.

**Then explain:**
- **How it happens:** benchmarks are published on the web and get scraped into pretraining; synthetic or instruction data was generated from benchmark items; you fine-tune on data that overlaps the test set; you tune prompts or pick checkpoints on the test set; paraphrased or translated test items slip past exact-match dedup.
- **Same as classical leakage:** train/test overlap (duplicate rows), selection on the test set (tuning), and temporal leakage (events after the cutoff).
- **Different:** you often cannot see the pretraining data, and "overlap" can be semantic, not exact.
- **Detect:** n-gram or embedding overlap against the test set; check if the model can complete test items verbatim, or has suspiciously high accuracy on older vs newer benchmark versions; perplexity on test items vs rephrased versions.
- **Mitigate:** dedup training data against test sets (n-gram + embedding), use fresh held-out or private evals created after the model cutoff, rotate/refresh benchmarks, evaluate on your own task data, keep a never-tuned final test set, report contamination checks.

**Example:** A model scores 90% on a public coding benchmark but 60% on a new set of similar, post-cutoff problems. The gap suggests memorisation.

**Follow-ups:**
- *What about LLM-as-judge?* Judge bias and shared training data are a second leakage route.
- *How would you evaluate a fine-tune safely?* Split by source/document before fine-tuning, hold out a private set, test on post-cutoff data.

**Common mistakes:** Relying only on exact-match dedup; tuning prompts on the test set; treating public leaderboard numbers as proof of generalisation.

### Q35 ⭐ 🔴 Derive the bias-variance decomposition of expected squared error. Why is irreducible noise separate?
**Asked at:** Research-leaning roles, Amazon applied scientist
**Say this first (1 line):** Expected squared error at a point splits into bias² + variance + irreducible noise, and noise stands alone because it comes from the data itself, which no model trained on any sample can change.

**Then explain (derivation):** Let `y = f(x) + ε`, `E[ε]=0`, `Var(ε)=σ²`, ε independent of the training set. Let `f̂` be the model trained on a random training set; expectation is over training sets and ε.
1. `E[(y - f̂)²] = E[(f + ε - f̂)²] = E[ε²] + E[(f - f̂)²]` because the cross term `2E[ε(f - f̂)] = 0` (ε independent, mean zero). So noise = σ².
2. Add and subtract `E[f̂]`: `E[(f - f̂)²] = (f - E f̂)² + E[(f̂ - E f̂)²] + 2(f - E f̂) E[E f̂ - f̂]`, and the last term is 0 since `E[f̂ - E f̂]=0`.
3. Result: `E[(y - f̂)²] = (Bias[f̂])² + Var[f̂] + σ²`, with `Bias = E f̂ - f` and `Var = E[(f̂ - E f̂)²]`.

- **Why noise is separate:** it does not depend on `f̂` at all; it is the floor (Bayes error for squared loss).
- **Reading it:** simpler models raise bias, flexible models raise variance; the sum is often U-shaped in complexity.
- **Caveat:** the clean decomposition is for squared loss; for 0-1 loss there are several variants.

**Example (real run, `y = sin(2πx) + noise`, depth-3 trees, 30 points per training set, 2,000 training sets, predicting at x=0.3, noise std 0.5 so σ²=0.25):** bias² 0.002 (essentially zero: this point happens to be well fit by the tree, so do not read it as "trees have no bias"), variance 0.101, so predicted total 0.352; measured MSE against fresh noisy targets 0.353. They match within sampling error.

**Follow-ups:**
- *How do you lower each term?* Bias: richer model. Variance: more data, regularization, bagging. Noise: better features or labels, not the model.
- *Does it hold for deep nets?* The formula holds; the "U-shape" does not always (double descent).

**Common mistakes:** Forgetting the cross term vanishes only because ε is independent and zero-mean; treating bias as something you can measure from one fit; saying noise can be reduced by a better model.


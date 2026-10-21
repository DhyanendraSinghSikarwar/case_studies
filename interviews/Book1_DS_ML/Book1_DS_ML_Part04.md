# Book 1 — Part 04: Decision Trees, Random Forest, Boosting (XGBoost / LightGBM / CatBoost), Tuning, SHAP

**Topic:** Trees, bagging, boosting, tree-model hyperparameter tuning, feature importance and SHAP
**Target:** 45 questions | **Actual:** 53 (⭐⭐⭐ 15, ⭐⭐ 27, ⭐ 11)
**Date:** 2026-10-20 | **Status:** Answers written and reviewed (Wave C)
**Note:** Source vs gap-check marking per question is in research_notes/Book1_Part04_sources.md.

---

> Dedupe pass: removed 1 cross-part duplicate(s); renumbered Q1–Q53.

---

### Q1 ⭐⭐⭐ 🟢 How does a decision tree choose where to split? Compare Gini impurity, entropy and information gain.
**Asked at:** Product cos, GCCs, analytics/consulting firms (Amazon, Indian product cos)
**Say this first (1 line):** A tree tries every possible split on every feature and picks the one that makes the two child nodes the "purest" (least mixed classes), measured by Gini impurity or entropy; the drop in impurity is the information gain.

**Then explain:**
- **Gini** = 1 − Σpₖ². Chance that two random samples from the node have different classes. 0 = pure, 0.5 = worst for two classes.
- **Entropy** = −Σpₖ log₂ pₖ. Amount of "surprise" in the node. 0 = pure, 1 bit = worst for two classes.
- **Information gain** = impurity(parent) − weighted average impurity(children), weights = child size / parent size. Greedy: pick the split with the biggest gain, then repeat on each child.
- Gini vs entropy: almost always give the same tree. Gini is a bit cheaper (no log) and is the sklearn default; entropy penalises mixed nodes slightly harder. Don't spend interview time arguing which is better.
- Numeric features: sort values, try thresholds between neighbours. Categorical: try groupings or one-vs-rest.
- Greedy means it is not globally optimal. Finding the optimal tree is NP-hard.

**Example:** 8 customers, ages 22 to 55, labels 0,0,0,1,0,1,1,1. Parent Gini = 0.5. Split "age ≤ 30": left = 3 zeros (Gini 0), right = 1 zero + 4 ones (Gini 0.32). Weighted = 5/8 × 0.32 = 0.20, so gain = 0.30. With entropy, the same split gives gain 0.549 bits.

**Code:**
```python
import numpy as np
def gini(y):
    p = np.bincount(y)/len(y); return 1-(p**2).sum()
def entropy(y):
    p = np.bincount(y)/len(y); p = p[p>0]; return -(p*np.log2(p)).sum()
def best_split(x, y, crit=gini):
    best, parent = (None, -1), crit(y)
    for t in np.unique(x)[:-1]:
        l, r = y[x<=t], y[x>t]
        gain = parent - (len(l)*crit(l) + len(r)*crit(r))/len(y)
        if gain > best[1]: best = (t, gain)
    return best
x = np.array([22,25,30,35,40,45,50,55]); y = np.array([0,0,0,1,0,1,1,1])
print(gini(y), entropy(y))          # 0.5 1.0
print(best_split(x, y, gini))       # threshold 30, gain 0.30
print(best_split(x, y, entropy))    # threshold 30, gain 0.549
```

**Follow-ups:**
- *Does the choice change the model?* Rarely. Both pick the same split in most cases.
- *Why weighted average?* A tiny pure child should not look better than a big, mostly pure one.
- *Regression?* Replace impurity with variance / squared error (see Q17).

**Common mistakes:** Forgetting to weight children by size. Saying entropy is "better" than Gini. Forgetting the split search is greedy, so a split that looks weak now can enable a strong one later (XOR problem).

### Q2 ⭐⭐⭐ 🟢 Bagging vs boosting: what is the difference and how does each affect bias and variance?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** Bagging trains many deep trees independently on bootstrap samples and averages them to cut variance; boosting trains many shallow trees one after another, each fixing the previous errors, to cut bias.

**Then explain:**

| | Bagging (Random Forest) | Boosting (GBM, XGBoost) |
|---|---|---|
| Training | Parallel, independent | Sequential, each depends on the last |
| Base learner | Deep, low-bias high-variance trees | Shallow, high-bias low-variance trees (depth 3 to 8) |
| Main effect | Reduces **variance** | Reduces **bias** (and some variance with regularisation) |
| Combine by | Average / vote | Weighted sum |
| Overfitting | Hard to overfit by adding trees | Can overfit if too many trees / too high learning rate |
| Noise / outliers | Robust | More sensitive, since it chases hard points |
| Tuning effort | Low | Higher |

- Averaging n trees with variance σ² and pairwise correlation ρ gives variance ρσ² + (1−ρ)σ²/n. Bagging shrinks the second term. Feature subsampling lowers ρ (see Q42).
- Boosting fits the residuals (the negative gradient of the loss), so the model keeps improving on what it got wrong.

**Example:** Credit-default model. Random Forest on 500 deep trees gives a stable, decent baseline with almost no tuning. XGBoost with learning rate 0.05 and early stopping usually adds a few AUC points but needs tuning and a validation set.

**Follow-ups:**
- *Can bagging reduce bias?* Not really. The average of unbiased-ish deep trees has the same bias as one tree.
- *Which would you start with?* RF for a quick, robust baseline; boosting when I need the last bit of accuracy.

**Common mistakes:** Saying "boosting reduces variance, bagging reduces bias" (reversed). Saying boosting is parallel. Forgetting that boosting uses weak (shallow) learners while bagging wants strong, deep ones.

### Q3 ⭐⭐⭐ 🟢 What are the key hyperparameters of a Random Forest and how does each affect bias/variance?
**Asked at:** Product cos, GCCs, analytics/consulting firms (UHG-type report)
**Say this first (1 line):** The big ones are n_estimators, max_features, and the tree-complexity controls (max_depth, min_samples_leaf); more trees never hurt, while more complex trees trade lower bias for higher variance.

**Then explain:**

| Hyperparameter | Increase it → | Effect |
|---|---|---|
| `n_estimators` | more trees | Variance down, then plateaus. Only costs time. Not a real overfitting knob. |
| `max_features` | each split sees more features | Trees get more correlated → variance up, bias down (for sklearn classifiers default is √p) |
| `max_depth` | deeper trees | Bias down, variance up |
| `min_samples_leaf` / `min_samples_split` | bigger leaves | Bias up, variance down (smoother) |
| `max_samples` (bootstrap size) | bigger bootstrap | Trees more alike → variance up slightly |
| `max_leaf_nodes`, `ccp_alpha` | fewer leaves / more pruning | Bias up, variance down |
| `class_weight` | | Shifts focus to the minority class |

- Order I tune: `max_features` and `min_samples_leaf` first, then `max_depth`. Set `n_estimators` high (300 to 1000) and stop worrying.
- Use OOB score (Q18) for cheap tuning instead of full CV.

**Example (CV accuracy, 3000 rows, 20 features, noisy labels):** default 0.909; `min_samples_leaf=5` 0.904; `max_depth=4` 0.886 (too shallow, bias); `max_features=2` 0.898; 20 trees 0.900. Defaults are already strong; RF is forgiving, and only extreme settings hurt.

**Code:**
```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
X, y = make_classification(3000, 20, n_informative=8, flip_y=0.1, random_state=0)
for kw in [dict(), dict(min_samples_leaf=5), dict(max_depth=4), dict(max_features=2), dict(n_estimators=20)]:
    m = RandomForestClassifier(**{"n_estimators": 200, "random_state": 0, **kw})
    print(kw, cross_val_score(m, X, y, cv=5).mean().round(3))
```

**Follow-ups:**
- *Can you overfit by adding trees?* No, variance only falls. You can overfit by deep trees on very noisy data, though.
- *Why √p for classification and p/3 for regression?* Rule-of-thumb defaults from Breiman that balance tree strength against correlation.

**Common mistakes:** Tuning `n_estimators` as if it were a regularizer. Using `max_features=1.0` (that is plain bagging; trees become highly correlated). Not setting `min_samples_leaf` on noisy data.

### Q4 ⭐⭐⭐ 🟢 Why does a Random Forest overfit less than a single decision tree? Explain bootstrap sampling and feature subsampling.
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** A single deep tree memorises noise (high variance); a Random Forest averages many de-correlated deep trees, and averaging cancels the random errors while keeping the low bias.

**Then explain:**
- **Bootstrap sampling:** each tree trains on n rows drawn *with replacement*. About 63.2% of unique rows appear (1 − 1/e); the other ~36.8% are out-of-bag. So each tree sees a slightly different dataset and makes different mistakes.
- **Feature subsampling:** at *each split*, only a random subset of features (e.g. √p) is considered. Without it, one strong feature dominates every tree's top split and trees stay similar, so averaging helps little.
- **Why averaging works:** variance of the average = ρσ² + (1−ρ)σ²/n. More trees kill the second term; feature subsampling lowers ρ, the correlation between trees (derivation in Q42).
- Each tree is still deep, so individual bias stays low. The forest is "many overfit models whose overfitting points in different directions".

**Example:** 2000 rows, noisy labels. Single tree 5-fold CV accuracy 0.78; 300-tree forest 0.87. Same data, same base learner, only the averaging differs. Check: drawing 10,000 bootstrap indices from 10,000 rows gave 63.5% unique rows.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
X, y = make_classification(2000, 20, n_informative=8, flip_y=0.1, random_state=0)
for n, m in [("tree", DecisionTreeClassifier(random_state=0)),
             ("RF", RandomForestClassifier(300, random_state=0))]:
    print(n, cross_val_score(m, X, y, cv=5).mean().round(3))     # 0.78 vs 0.87
print(len(np.unique(np.random.default_rng(0).integers(0, 10000, 10000)))/10000)  # ~0.635
```

**Follow-ups:**
- *Does a forest still overfit?* Training accuracy is ~100%, but the gap to test is much smaller. Use `min_samples_leaf` if the data is very noisy.
- *Is bootstrapping necessary?* Feature subsampling alone also decorrelates; Extra Trees (Q21) even drops the bootstrap.

**Common mistakes:** Saying RF reduces bias. Saying more trees can overfit. Forgetting that feature subsampling happens per split, not per tree.

### Q5 ⭐⭐⭐ 🟢 What is the difference between Random Forest and XGBoost, and when would you pick each?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Intuit, Amazon, Digitas-type, Tredence, Applied Cloud Computing)
**Say this first (1 line):** Random Forest averages many independent deep trees (bagging, variance reduction); XGBoost adds many shallow trees sequentially, each correcting the last (boosting, bias reduction) with built-in regularisation, and usually wins on accuracy but needs tuning.

**Then explain:**

| | Random Forest | XGBoost |
|---|---|---|
| Idea | Bagging, parallel | Gradient boosting, sequential |
| Trees | Deep, unpruned | Shallow (3 to 8) |
| Accuracy ceiling | Good | Usually higher on tabular data |
| Tuning | Little needed | Learning rate, depth, trees, subsample, regularisation, early stopping |
| Overfit risk | Low | Higher, needs early stopping |
| Missing values | Not native in older sklearn (supported in newer versions) | Native, learns default direction |
| Noisy labels | More robust | Can chase noise |
| Extras | OOB score for free | Custom loss, monotonic constraints, GPU |

- Pick **RF** for a fast, robust baseline, noisy data, little time to tune, or when OOB estimates and parallel training are handy.
- Pick **XGBoost** (or LightGBM) when accuracy matters, data is clean enough, and I can run proper validation with early stopping.
- In practice: start with RF as a baseline, then beat it with a tuned boosted model.

**Example:** Fraud scoring with 200 features and 1M rows. RF gets AUC 0.90 in minutes. Tuned XGBoost gets 0.92 and supports `scale_pos_weight`, custom loss and monotonic constraints, so it ships.

**Follow-ups:**
- *Why is XGBoost more accurate?* It optimises the loss directly, uses second-order information, and shrinks each tree's contribution.
- *Can RF beat XGBoost?* Yes, on small noisy data or when XGBoost is badly tuned.

**Common mistakes:** Claiming XGBoost always wins. Forgetting early stopping. Calling XGBoost "a bigger Random Forest".

### Q6 ⭐⭐⭐ 🟡 How do you prevent overfitting in a decision tree? Explain pre-pruning, post-pruning and cost-complexity pruning.
**Asked at:** Product cos, GCCs, analytics/consulting firms (Swiggy-type)
**Say this first (1 line):** An unrestricted tree grows until every leaf is pure and memorises noise, so I limit its growth up front (pre-pruning), cut it back afterwards (post-pruning), and in practice I use cost-complexity pruning with the strength chosen by cross-validation.

**Then explain:**
- **Pre-pruning (early stopping):** stop growing using `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_leaf_nodes`, `min_impurity_decrease`. Cheap and simple, but can stop too early, since a weak split might unlock a good one below it.
- **Post-pruning:** grow the full tree, then remove branches that do not help on validation data (reduced-error pruning).
- **Cost-complexity pruning (weakest-link, `ccp_alpha`):** minimise R(T) + α·|leaves|. Each leaf costs α. Bigger α gives a smaller tree. `cost_complexity_pruning_path` gives the sequence of candidate α values; pick α by CV.
- Alternative: skip pruning and use an ensemble (Q4).

**Example:** 2000 rows with 15% label noise. Full tree: 171 leaves, train accuracy 1.00, test 0.763. CV-chosen `ccp_alpha`≈0.0045: 13 leaves, train 0.852, test 0.817. Train accuracy fell but test accuracy rose, which is the point.

**Code:**
```python
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
X, y = make_classification(2000, 20, n_informative=6, flip_y=0.15, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
full = DecisionTreeClassifier(random_state=0).fit(Xtr, ytr)
alphas = full.cost_complexity_pruning_path(Xtr, ytr).ccp_alphas[::5]
g = GridSearchCV(DecisionTreeClassifier(random_state=0), {"ccp_alpha": alphas}, cv=5).fit(Xtr, ytr)
m = g.best_estimator_
print(full.get_n_leaves(), round(full.score(Xte, yte), 3))   # 171 leaves, 0.763
print(m.get_n_leaves(), round(m.score(Xte, yte), 3))         # 13 leaves, 0.817
```

**Follow-ups:**
- *Why choose α on CV and not on the test set?* Choosing on test leaks information and inflates the score.
- *Which would you use at work?* `min_samples_leaf` plus `ccp_alpha`, tuned with CV.

**Common mistakes:** Tuning the pruning level on the test set. Saying pruning increases training accuracy (it lowers it). Mixing up pre- and post-pruning.

### Q7 ⭐⭐⭐ 🟡 Explain gradient boosting step by step. Why is it called gradient boosting?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Intuit, interview-prep banks)
**Say this first (1 line):** Gradient boosting builds a model in stages, where each new small tree is fit to the errors of the current model; it is "gradient" boosting because those errors are the negative gradient of the loss, so it is gradient descent in function space.

**Then explain:**
1. Start with a constant prediction F₀ (the mean for squared loss, log-odds for classification).
2. For m = 1…M: compute pseudo-residuals rᵢ = −∂L(yᵢ, F(xᵢ))/∂F(xᵢ) at the current model.
3. Fit a shallow tree hₘ to these residuals.
4. Update: Fₘ = Fₘ₋₁ + η·hₘ, with learning rate η (e.g. 0.1) as shrinkage.
5. Final model = F₀ + η·Σhₘ.
- For squared loss, the negative gradient is exactly the residual y − F. For log loss it is y − p. For other losses, the same recipe works, which is why GBM supports custom losses.
- Small η and many trees generalise better than big steps.

**Example:** Fit y = sin(x)+noise with depth-2 trees, η = 0.1. Train MSE: 0.453 after 1 tree, 0.123 after 10, 0.027 after 100 (noise variance is 0.04, so by 100 trees it is starting to fit noise, hence early stopping).

**Code:**
```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor
rng = np.random.default_rng(0)
X = rng.uniform(0, 6, (300, 1)); y = np.sin(X[:, 0]) + rng.normal(0, 0.2, 300)
lr, F = 0.1, np.full_like(y, y.mean())
for m in range(100):
    resid = y - F                                  # negative gradient of 0.5*(y-F)^2
    t = DecisionTreeRegressor(max_depth=2).fit(X, resid)
    F += lr * t.predict(X)
    if m in (0, 9, 99): print(m+1, round(np.mean((y-F)**2), 4))   # 0.4528, 0.123, 0.0266
```

**Follow-ups:**
- *Difference from AdaBoost?* AdaBoost reweights samples; GBM fits gradients (Q20).
- *Why shallow trees?* They are weak learners with low variance; boosting adds up the bias reduction.
- *What does XGBoost add?* Second-order gradients and explicit regularisation (Q8, Q38).

**Common mistakes:** Saying trees are fit to the *labels* each round (they fit residuals/gradients). Forgetting the learning rate. Thinking the "gradient" is with respect to model parameters rather than predictions.

### Q8 ⭐⭐⭐ 🟡 What makes XGBoost different from classic gradient boosting (GBM)?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** XGBoost is gradient boosting plus a regularised objective, second-order (Newton) updates, and a lot of systems engineering (histogram/parallel split search, sparsity handling, caching), which makes it more accurate, faster and harder to overfit.

**Then explain:**
- **Regularised objective:** loss + γ·(number of leaves) + ½λ·Σ(leaf weights)². Penalises complex trees. Classic GBM has only shrinkage and depth limits.
- **Second-order optimisation:** uses gradient g *and* hessian h. Optimal leaf weight = −G/(H+λ), and split gain is computed from G and H (Q38). Gives better steps than gradient-only.
- **Sparsity-aware splits:** learns a default direction for missing/zero values at each split, so NaNs are handled natively (Q48).
- **Speed:** column-block structure, parallel split finding across features, histogram/approximate split finding, cache-aware access, out-of-core and distributed/GPU support. Tree building is sequential, but the split search inside a tree is parallel.
- **Extras:** built-in row/column subsampling, early stopping, `min_child_weight` (minimum hessian sum), custom objectives, monotonic constraints.

**Example:** On a 5M-row click dataset, sklearn's older GradientBoosting takes hours and ignores NaNs; XGBoost `tree_method="hist"` trains in minutes, handles missing values, and the λ/γ penalties give a smoother, less overfit model.

**Follow-ups:**
- *What does `min_child_weight` do?* A leaf must have at least that much total hessian. For log loss this is roughly "enough effective samples".
- *Is it still a different algorithm?* Same idea (additive trees on gradients), different objective optimisation and engineering.

**Common mistakes:** Listing only "it is faster". Forgetting the regularisation term and the hessian. Saying XGBoost builds trees in parallel (it parallelises within a tree).

### Q9 ⭐⭐⭐ 🟡 How would you tune XGBoost hyperparameters? Which matter most and in what order?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Walmart)
**Say this first (1 line):** I fix a sensible learning rate, let early stopping choose the number of trees, then tune tree complexity (max_depth, min_child_weight), then randomness (subsample, colsample), then regularisation (lambda, alpha, gamma), and finally lower the learning rate and retrain.

**Then explain:**
1. **Baseline + split:** train/validation/test or CV; pick the metric that matches the business (AUC, PR-AUC, logloss, RMSE).
2. **`learning_rate` 0.05 to 0.1 and `n_estimators` large (e.g. 2000) with `early_stopping_rounds` 50.** The tree count is found, not tuned.
3. **Complexity (biggest impact):** `max_depth` 3 to 8, `min_child_weight` 1 to 10, `gamma` 0 to 5.
4. **Randomness:** `subsample` 0.6 to 1, `colsample_bytree` 0.5 to 1. Reduces variance.
5. **Regularisation:** `reg_lambda` (L2), `reg_alpha` (L1).
6. **Imbalance:** `scale_pos_weight` if needed (Q24).
7. **Finish:** drop learning rate to 0.01 to 0.03 and retrain with early stopping for a small final gain.
- Use random search or Optuna (Q26) instead of grid. Tune on CV with a fixed seed; keep a final untouched test set.
- Sanity check: look at train vs validation curves. A big gap means more regularisation.

**Example:** On the synthetic set in the code, with lr 0.3 early stopping picked 19 trees (test AUC 0.950); with lr 0.05 it picked 178 trees (test AUC 0.955), both with depth 4 and no `min_child_weight` (Q19 has that run). The exact code below adds `min_child_weight=3` and `reg_lambda=1`, and stops at 67 trees with validation AUC 0.938. The point: the tree count is found by early stopping, and a smaller step is smoother and slightly better.

**Code:**
```python
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
X, y = make_classification(6000, 20, n_informative=8, flip_y=0.1, random_state=0)       # shared synthetic set used in Q9-Q26
Xtr, Xtmp, ytr, ytmp = train_test_split(X, y, test_size=0.4, random_state=0)
Xva, Xte, yva, yte = train_test_split(Xtmp, ytmp, test_size=0.5, random_state=0)       # 60/20/20 train/val/test
m = xgb.XGBClassifier(n_estimators=2000, learning_rate=0.05, max_depth=4, min_child_weight=3,
                      subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0,
                      early_stopping_rounds=50, eval_metric="auc", random_state=0)
m.fit(Xtr, ytr, eval_set=[(Xva, yva)], verbose=False)   # validation set, NOT the test set
print(m.best_iteration, m.best_score)                    # 67 trees, validation AUC 0.938
```

**Follow-ups:**
- *Why not grid search everything?* The space is big and a few parameters dominate; random/Bayesian search finds good regions faster.
- *How do you avoid overfitting the validation set?* Nested CV or a final holdout used once.

**Common mistakes:** Tuning `n_estimators` as a fixed number rather than early stopping. Early stopping on the test set. Tuning all parameters at once on a tiny validation set. Ignoring `min_child_weight`.

### Q10 ⭐⭐⭐ 🟡 Compare XGBoost, LightGBM and CatBoost: speed, categorical handling, growth strategy, when to use which.
**Asked at:** Product cos, GCCs, analytics/consulting firms (Glassdoor-reported XGBoost vs LightGBM)
**Say this first (1 line):** All three are gradient-boosted trees; XGBoost is the mature all-rounder, LightGBM is the fastest on large data thanks to histograms and leaf-wise growth, and CatBoost is best out of the box on categorical-heavy data thanks to ordered target statistics and symmetric trees.

**Then explain:**

| | XGBoost | LightGBM | CatBoost |
|---|---|---|---|
| Growth | Level-wise (depth-wise) by default; leaf-wise available (`grow_policy=lossguide`) | **Leaf-wise** (best-first) | **Symmetric (oblivious)** trees: same split per level |
| Speed on big data | Good with `hist` / GPU | Usually fastest on CPU (histograms, GOSS, EFB) | Fast on GPU; CPU slower than LightGBM |
| Categoricals | Needs encoding (experimental native support exists) | Native (optimal grouping, `categorical_feature`) | **Best**: ordered target statistics, no leakage |
| Overfitting | Level-wise is safer | Leaf-wise can overfit small data; tune `num_leaves`, `min_data_in_leaf` | Ordered boosting reduces prediction shift; strong defaults |
| Tuning needed | Medium | Medium | Little |
| Inference | Fast | Fast | Very fast (symmetric trees) |

- Use **XGBoost** as a safe default, for custom objectives and broad tooling.
- Use **LightGBM** for millions of rows, many features, or tight training time.
- Use **CatBoost** for many high-cardinality categoricals (user, merchant, city), small or medium data, or little time for tuning.
- Accuracy differences are usually small; data prep and validation matter more.

**Example:** E-commerce ranking with 50M rows: LightGBM for speed. Insurance pricing with 30 categorical columns and 200k rows: CatBoost, no one-hot encoding needed.

**Follow-ups:**
- *Why can leaf-wise overfit?* It grows deep, lopsided branches to chase the largest loss reduction (Q25).
- *Do you need to scale features?* No, for any of them.

**Common mistakes:** Claiming one is always best. Saying XGBoost cannot be leaf-wise. One-hot encoding high-cardinality columns for XGBoost without considering the blow-up (Q29).

### Q11 ⭐⭐⭐ 🟡 How do you control overfitting in boosting models? Where does early stopping fit in?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Swiggy/Flipkart-type)
**Say this first (1 line):** I use a small learning rate, shallow trees, row/column subsampling and L1/L2/gamma penalties, and let early stopping on a validation set pick the number of trees, since the training loss keeps falling forever but validation loss turns up when the model starts fitting noise.

**Then explain:**
- **Shrinkage:** small `learning_rate` (0.01 to 0.1) with more trees.
- **Limit tree complexity:** `max_depth` 3 to 6, `min_child_weight` (LightGBM: `min_data_in_leaf`), `gamma` / `min_split_gain`, `num_leaves` in LightGBM.
- **Randomness:** `subsample`, `colsample_bytree` / `colsample_bynode`. Like bagging inside boosting.
- **Regularisation:** `reg_lambda`, `reg_alpha`.
- **Early stopping:** monitor a metric on a validation set; stop if no improvement for N rounds and keep the best iteration. It is effectively tuning the number of trees automatically.
- **Careful:** early stopping uses the validation set to choose, so validation score becomes slightly optimistic. Report the final score on a separate test set.

**Example:** XGBoost, lr 0.05, depth 4, `early_stopping_rounds=50`: stopped at 178 of a possible 2000 trees, validation AUC 0.939, test AUC 0.955. Without it the model keeps adding trees that only fit noise.

**Code:**
```python
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
X, y = make_classification(6000, 20, n_informative=8, flip_y=0.1, random_state=0)       # same synthetic set as Q9
Xtr, Xtmp, ytr, ytmp = train_test_split(X, y, test_size=0.4, random_state=0)
Xva, Xte, yva, yte = train_test_split(Xtmp, ytmp, test_size=0.5, random_state=0)
m = xgb.XGBClassifier(n_estimators=2000, learning_rate=0.05, max_depth=4, subsample=0.8,
                      colsample_bytree=0.8, early_stopping_rounds=50, eval_metric="auc", random_state=0)
m.fit(Xtr, ytr, eval_set=[(Xva, yva)], verbose=False)
print(m.best_iteration)          # 178 in my run; predictions use the best iteration
```

**Follow-ups:**
- *Why not early-stop on the test set?* That is leakage: the test set picks the model, so the reported score is biased.
- *Early stopping inside CV?* Use each fold's validation part for stopping, then refit on all training data with the average best iteration (slightly scaled up).

**Common mistakes:** Early stopping on the test set. Not keeping the best iteration. Using the training metric for stopping. Making trees too deep and then relying only on early stopping.

### Q12 ⭐⭐⭐ 🟡 How is feature importance computed in tree models (split count, gain/impurity, permutation)? What are the pitfalls?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Flipkart-type, Target)
**Say this first (1 line):** Tree models give three kinds of importance: split-based (how often a feature is used), gain/impurity-based (how much loss it removes), and permutation (how much the score drops when you shuffle it); the first two are cheap but biased, permutation on held-out data is more trustworthy, and SHAP is better still for attribution.

**Then explain:**
- **Split count / weight:** number of times a feature is used to split. Favours features with many possible thresholds.
- **Gain / impurity decrease (MDI):** total loss reduction from splits on that feature. sklearn's `feature_importances_` for RF is this, computed on *training data*. XGBoost offers `weight`, `gain`, `cover`, `total_gain`. Prefer gain over weight.
- **Permutation importance:** shuffle one column on validation data, measure the drop in score. Model-agnostic, uses held-out data, but costs extra predictions.
- **Pitfalls:**
  - MDI is biased toward high-cardinality / continuous features and measured on training data, so a useless feature can look important.
  - Correlated features split or share importance (Q23).
  - Importance is not causation, and not direction.
  - Different methods can rank differently; the importance is model-specific.

**Example:** RF on 5 features + 1 pure-noise column. Training accuracy 1.00, test 0.84. MDI gave the noise column and two useless features ~0.10 each; permutation importance on test data gave them ~0.00 and gave 0.12 to 0.24 to the three real features. (Full runnable setup is in Q22.)

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0)
Xs, ys = make_classification(2000, 5, n_informative=3, n_redundant=0, flip_y=0.2, random_state=0)
Xn = np.hstack([Xs, rng.normal(size=(2000, 1))])                          # add a pure-noise column (same setup as Q22)
Xa, Xb, ya, yb = train_test_split(Xn, ys, test_size=0.3, random_state=0)
rf = RandomForestClassifier(300, random_state=0).fit(Xa, ya)
print(rf.feature_importances_.round(3))                                  # MDI (train-based)
pi = permutation_importance(rf, Xb, yb, n_repeats=10, random_state=0)    # on held-out data
print(pi.importances_mean.round(3))
```

**Follow-ups:**
- *Which would you report?* Permutation importance on validation data and SHAP, with MDI only for a quick look.
- *Does low importance mean the feature is useless?* Not if it is correlated with another one the model prefers.

**Common mistakes:** Reporting MDI as the truth. Computing permutation importance on training data. Ignoring correlated features. Reading importance as the direction of effect.

### Q13 ⭐⭐⭐ 🟡 What is SHAP? How does it differ from built-in feature importance (global vs local)?
**Asked at:** Product cos, GCCs, analytics/consulting firms, fintech/credit risk (Klarna-type), regulated GCCs
**Say this first (1 line):** SHAP splits a single prediction into per-feature contributions using Shapley values from game theory, so it gives both a local explanation (why this customer got this score) and, by averaging, a global one; built-in importance only gives one global ranking with no direction.

**Then explain:**
- **Shapley idea:** a feature's contribution = its average marginal effect on the prediction over all orders in which features could be added. Fair, and the contributions are **additive**: base value + Σ SHAP = model output.
- **TreeSHAP** computes exact Shapley values for tree ensembles in polynomial time, so it is practical for XGBoost/LightGBM/RF.
- **Local:** waterfall/force plot for one row, showing which features pushed the score up or down and by how much.
- **Global:** mean |SHAP| per feature = importance; beeswarm shows direction and spread; dependence plots show the shape of the effect and interactions.
- **vs built-in importance:** built-in is global only, computed on training splits, biased (Q22), and says nothing about direction or per-row effects. SHAP is consistent, signed, and per row.
- For classification, tree SHAP values are in log-odds space, not probabilities.

**Example:** Loan model: base log-odds −1.2. Income +0.9, previous default −2.0, short tenure −0.4 → final log-odds −2.7, a decline. For the customer you can say "mainly the previous default".

**Code:**
```python
import numpy as np, shap, xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
X, y = make_classification(6000, 20, n_informative=8, flip_y=0.1, random_state=0)       # same synthetic set as Q9
Xtr, Xtmp, ytr, ytmp = train_test_split(X, y, test_size=0.4, random_state=0)
Xva, Xte, yva, yte = train_test_split(Xtmp, ytmp, test_size=0.5, random_state=0)
m = xgb.XGBClassifier(n_estimators=100, max_depth=3, random_state=0).fit(Xtr, ytr)
sv = shap.TreeExplainer(m)(Xte)                   # values in log-odds space
row0 = sv.values[0].sum() + sv.base_values[0]
print(np.isclose(row0, m.predict(Xte[:1], output_margin=True)[0], atol=1e-3))   # True: additivity
global_imp = np.abs(sv.values).mean(0)            # mean |SHAP| = global importance
```
(Run on the 6000-row synthetic set: additivity held (`True`). Mean-|SHAP| top-3 features were [3, 16, 5] and XGBoost gain top-3 were [5, 16, 3]: same three features, but ranked differently, so the two importance measures do not always agree on order.)

**Follow-ups:**
- *Is SHAP causal?* No. It explains the model, not the world.
- *Cost?* TreeSHAP is fast for trees; KernelSHAP is slow and approximate for other models.
- *Pitfall?* Correlated features (Q41).

**Common mistakes:** Saying SHAP is "just feature importance". Treating SHAP values as probabilities or causal effects. Forgetting the base value. Mixing up log-odds and probability scale.

### Q14 ⭐⭐⭐ 🟡 How do tree-based models handle missing values, categorical variables, outliers and unscaled features?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** Trees need very little preprocessing: they need no feature scaling, are insensitive to outliers (they split on ranks/thresholds), and many implementations handle missing values natively, but categorical variables still need care.

**Then explain:**
- **Missing values:** XGBoost, LightGBM and recent sklearn trees/forests handle NaN natively by learning at each split which branch missing rows should take (default direction). CatBoost also handles them. Older sklearn trees needed imputation. Adding a "was missing" flag helps when missingness itself is informative.
- **Categoricals:** sklearn trees need encoding (ordinal or one-hot). LightGBM and CatBoost handle them natively. XGBoost has native support (`enable_categorical=True`). High cardinality needs target/ordered encoding (Q29).
- **Outliers in features:** unaffected, since a split only asks "is x ≤ t". **Outliers in the target** (regression with squared loss) do hurt, because leaf means move. Use a robust loss (Huber, MAE/quantile).
- **Unscaled features:** no problem. Monotonic transforms (log, standardise) do not change the tree structure.
- **Caveats:** trees cannot extrapolate (Q27), and heavy leakage through ID-like columns still hurts.

**Example:** I ran XGBoost with 20% of all feature values randomly set to NaN, in both train and test, with no imputation. Test AUC was still 0.933 (0.946 with complete data on the same split), so a fifth of the data missing cost about 0.01 AUC.

**Code:**
```python
import numpy as np, xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
X, y = make_classification(6000, 20, n_informative=8, flip_y=0.1, random_state=0)       # same synthetic set as Q9
Xtr, Xtmp, ytr, ytmp = train_test_split(X, y, test_size=0.4, random_state=0)
Xva, Xte, yva, yte = train_test_split(Xtmp, ytmp, test_size=0.5, random_state=0)
Xm = Xtr.copy(); Xm[np.random.default_rng(1).random(Xm.shape) < 0.2] = np.nan
Xtm = Xte.copy(); Xtm[np.random.default_rng(2).random(Xtm.shape) < 0.2] = np.nan
m = xgb.XGBClassifier(n_estimators=100, max_depth=4, random_state=0).fit(Xm, ytr)
print(roc_auc_score(yte, m.predict_proba(Xtm)[:, 1]))   # 0.933
```

**Follow-ups:**
- *Do you still do feature engineering?* Yes: ratios, aggregates, interactions, time features.
- *Why do outliers not matter?* Only the order of values affects the split.
- *Would you impute?* Often not for GBMs; for RF in older sklearn, yes.

**Common mistakes:** Standardising features "because the model needs it". Saying trees are immune to target outliers. Using label encoding for nominal variables with sklearn trees without noticing it imposes an order.

### Q15 ⭐⭐⭐ 🟡 Single decision tree vs ensemble (Random Forest / XGBoost): what are the trade-offs?
**Asked at:** Product cos, GCCs, analytics/consulting firms (practice-prompt style)
**Say this first (1 line):** A single tree is easy to explain but unstable and overfits; an ensemble trades interpretability and speed for much better accuracy and stability, so I pick based on whether the problem needs explainable rules or maximum predictive power.

**Then explain:**

| | Single tree | Random Forest | Boosted trees |
|---|---|---|---|
| Accuracy | Lowest | High | Highest (usually) |
| Variance | High (small data change → different tree) | Low | Low to medium |
| Interpretability | Excellent (draw the rules) | Poor (use importance/SHAP) | Poor (use SHAP) |
| Training / inference cost | Tiny | Medium | Medium to high |
| Tuning | Few knobs | Little | Several |
| Feature interactions | Captured, but unstable | Captured | Captured well |

- Single tree: use for a rule-based policy, a quick baseline, or when a business user must follow the logic.
- Ensemble: use for prediction quality. Explain with SHAP and partial dependence.
- A shallow tree can also be a **surrogate** to explain a black box (fit a small tree to the ensemble's predictions).

**Example:** Credit policy for branch staff: a depth-3 tree "if bureau score < 650 and income < X → decline" is auditable. The scoring engine itself runs XGBoost with SHAP reason codes.

**Follow-ups:**
- *Why is a tree unstable?* One early split changes everything below it.
- *Can a single tree be as good?* On small, simple, rule-like data, yes.

**Common mistakes:** Saying ensembles are "uninterpretable" (SHAP and PDPs help). Using a deep unpruned tree as the "interpretable" model. Ignoring latency and memory for large ensembles.

### Q16 ⭐⭐ 🟢 Work through a small table by hand: compute Gini/entropy and pick the best split.
**Asked at:** Product cos, GCCs, analytics/consulting firms, early-career / analytics
**Say this first (1 line):** For each candidate split I compute the weighted impurity of the children, subtract it from the parent's impurity, and take the split with the biggest drop; here "tenure > 12 months" beats "plan" clearly.

**Then explain:** 10 customers, 5 churn, 5 stay (parent Gini 0.5, entropy 1.0).

| Customer rows | Churn / total | Gini | Entropy |
|---|---|---|---|
| Plan = Basic | 4 / 6 | 0.444 | 0.918 |
| Plan = Premium | 1 / 4 | 0.375 | 0.811 |
| Tenure ≤ 12 | 5 / 6 | 0.278 | 0.650 |
| Tenure > 12 | 0 / 4 | 0 (pure) | 0 (pure) |

- **Plan:** weighted Gini = 0.6×0.444 + 0.4×0.375 = 0.417 → gain **0.083**. Weighted entropy 0.875 → gain **0.125** bits.
- **Tenure > 12:** weighted Gini = 0.6×0.278 + 0.4×0 = 0.167 → gain **0.333**. Weighted entropy 0.39 → gain **0.61** bits.
- The best split is **tenure > 12** under both measures (it also creates a pure child).

**Example:** the table above is the example (hand-built, illustrative data). Read it as a retention story: customers with more than 12 months of tenure in this sample never churned, so one cheap question already separates most of the risk, while plan type barely helps. Next the tree repeats the same search inside the "tenure ≤ 12" group (5 of 6 churn).

**Code:**
```python
import numpy as np
churn   = np.array([1,1,1,1,0,0, 1,0,0,0])
premium = np.array([0,0,0,0,0,0, 1,1,1,1])     # plan: 0=Basic, 1=Premium
longten = np.array([0,0,0,0,1,0, 0,1,1,1])     # tenure > 12 months
def gini(y): p = y.mean(); return 1 - p**2 - (1-p)**2
def ent(y):
    p = y.mean(); return 0 if p in (0, 1) else -(p*np.log2(p) + (1-p)*np.log2(1-p))
for name, f in [("plan", premium), ("tenure>12", longten)]:
    for cn, c in [("gini", gini), ("entropy", ent)]:
        w = sum((f == v).mean() * c(churn[f == v]) for v in (0, 1))
        print(name, cn, round(c(churn) - w, 3))
# plan gini 0.083, plan entropy 0.125, tenure gini 0.333, tenure entropy 0.61
```

**Follow-ups:**
- *What after the first split?* Repeat on each child until a stopping rule hits.
- *Ties?* Prefer the more balanced split or the first found.

**Common mistakes:** Not weighting child impurities. Using log base inconsistently. Forgetting that pure child nodes have zero impurity.

### Q17 ⭐⭐ 🟢 How does a regression tree split and what does a leaf predict?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** A regression tree picks the split that minimises the total squared error (equivalently, the weighted variance) of the two children, and each leaf predicts the mean of the training targets that fall in it.

**Then explain:**
- For each feature and threshold, compute SSE_left + SSE_right, where SSE = Σ(y − mean)² within the child. Choose the lowest. Same greedy recursion as classification, with variance instead of Gini.
- Leaf prediction = mean of y (for squared error). With absolute error (MAE) the leaf is the median; with Huber/quantile loss it differs.
- Result is a piecewise-constant function: a staircase.
- Stop with the usual rules (`max_depth`, `min_samples_leaf`, pruning). Without limits, each leaf holds one point and the tree memorises.

**Example:** x = [1,2,3,10,11,12], y = [5,6,5,20,21,19]. Total SSE = 325.3. Split at x ≤ 2.5: SSE 171.3. Split at x ≤ 6.5: SSE **2.67**, the best, with leaves predicting 5.33 and 20.0. Split at x ≤ 10.5: SSE 164.

**Code:**
```python
import numpy as np
x = np.array([1,2,3,10,11,12.]); y = np.array([5,6,5,20,21,19.])
sse = lambda v: ((v - v.mean())**2).sum()
for t in (2.5, 6.5, 10.5):
    l, r = y[x <= t], y[x > t]
    print(t, round(sse(l) + sse(r), 2), l.mean().round(2), r.mean().round(2))
# 2.5 -> 171.25, 6.5 -> 2.67 (leaf means 5.33 and 20.0), 10.5 -> 164.0
```

**Follow-ups:**
- *Why can't it extrapolate?* Leaves are averages of seen values (Q27).
- *How does GBM use regression trees?* Even for classification, each boosting tree is a regression tree fit to gradients.

**Common mistakes:** Saying a leaf predicts the "majority class". Forgetting the leaf is the mean (not a linear fit). Expecting smooth predictions.

### Q18 ⭐⭐ 🟡 What is out-of-bag (OOB) error in a Random Forest and how is it used?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** Each tree is trained on a bootstrap sample that leaves out about 36.8% of rows; I predict each row using only the trees that never saw it, and the error of those predictions is the OOB error, a free validation estimate without a separate holdout.

**Then explain:**
- A row is out-of-bag for a tree if it was not drawn in that tree's bootstrap. P(not drawn) = (1 − 1/n)ⁿ → 1/e ≈ 0.368.
- For each row, aggregate predictions from the ~37% of trees where it was OOB, then compare to the true label.
- Uses: quick generalisation estimate, tuning (`max_features`, `min_samples_leaf`) without CV, and permutation importance on OOB data.
- Limits: it is an estimate of a *smaller* forest (about a third of trees per row), so it is slightly pessimistic; it does not respect time order or groups. For time series or grouped data, use proper splits. Needs `bootstrap=True`.

**Example:** 3,600 training rows, 300 trees: OOB accuracy 0.914 vs actual test accuracy 0.920. Close, and cheaper than 5-fold CV.

**Code:**
```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
X, y = make_classification(6000, 20, n_informative=8, flip_y=0.1, random_state=0)       # same synthetic set as Q9
Xtr, Xtmp, ytr, ytmp = train_test_split(X, y, test_size=0.4, random_state=0)
Xva, Xte, yva, yte = train_test_split(Xtmp, ytmp, test_size=0.5, random_state=0)
rf = RandomForestClassifier(300, oob_score=True, random_state=0).fit(Xtr, ytr)
print(round(rf.oob_score_, 4), round(rf.score(Xte, yte), 4))   # 0.9144 0.92
```

**Follow-ups:**
- *Is OOB a replacement for CV?* Roughly, for iid data; not for leaky/grouped/temporal data.
- *Can boosting have OOB?* Only with row subsampling, and it is less common.

**Common mistakes:** Saying OOB uses a separate holdout you must set aside. Using OOB on time-series data. Forgetting it needs bootstrapping.

### Q19 ⭐⭐ 🟡 How do learning rate and number of trees trade off in boosting?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** They are inversely linked: a smaller learning rate means each tree contributes less, so you need proportionally more trees; small steps with many trees usually generalise better but cost more training time.

**Then explain:**
- Prediction = F₀ + η·Σhₘ. Halving η roughly doubles the trees needed to reach the same fit.
- **High η (0.3):** fast, few trees, but coarse steps and tends to overfit or settle on a worse optimum.
- **Low η (0.01 to 0.05):** smoother path, usually better test score, but needs hundreds to thousands of trees plus longer training and inference.
- **Practical recipe:** pick η = 0.05 to 0.1 while exploring, use early stopping to find the tree count, then at the end lower η and retrain.
- Diminishing returns below ~0.01.

**Example:** Same data and model, early stopping on validation AUC. η = 0.3 stopped at 19 trees (test AUC 0.950). η = 0.05 stopped at 178 trees (test AUC 0.955), roughly 9x more trees for a small gain.

**Code:**
```python
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
X, y = make_classification(6000, 20, n_informative=8, flip_y=0.1, random_state=0)       # same synthetic set as Q9
Xtr, Xtmp, ytr, ytmp = train_test_split(X, y, test_size=0.4, random_state=0)
Xva, Xte, yva, yte = train_test_split(Xtmp, ytmp, test_size=0.5, random_state=0)
for lr in (0.3, 0.05):
    m = xgb.XGBClassifier(n_estimators=2000, learning_rate=lr, max_depth=4, subsample=0.8,
                          colsample_bytree=0.8, early_stopping_rounds=50, eval_metric="auc", random_state=0)
    m.fit(Xtr, ytr, eval_set=[(Xva, yva)], verbose=False)
    print(lr, m.best_iteration, round(roc_auc_score(yte, m.predict_proba(Xte)[:, 1]), 4))
# 0.3 -> 19 trees, 0.9499 ; 0.05 -> 178 trees, 0.9549
```

**Follow-ups:**
- *Why does small η help?* Shrinkage acts as regularisation, like taking cautious steps in gradient descent.
- *When would you accept a larger η?* Quick experiments, huge data, tight latency.

**Common mistakes:** Fixing the number of trees while changing η. Judging η on the training loss. Ignoring inference cost of thousands of trees.

### Q20 ⭐⭐ 🟡 AdaBoost vs gradient boosting: how do they differ?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** AdaBoost reweights the training samples so the next weak learner focuses on the previously misclassified ones; gradient boosting keeps the samples the same and fits the next learner to the negative gradient (residuals) of any differentiable loss.

**Then explain:**
- **AdaBoost:** start with equal sample weights. Fit a stump (depth-1 tree), compute its weighted error ε, give it vote weight α = ½ ln((1−ε)/ε), increase weights of misclassified rows, repeat. Final = weighted vote. It is equivalent to minimising exponential loss.
- **Gradient boosting:** fit each tree to pseudo-residuals of a chosen loss (squared, log loss, quantile, custom), add it with learning rate η.
- **Differences:** AdaBoost is tied to exponential loss, very sensitive to outliers and label noise (misclassified noisy points get huge weights), mostly classification, and uses stumps. GBM is flexible (any loss, regression/ranking), more robust with shrinkage/subsampling, and is the basis for XGBoost/LightGBM.
- Both are sequential and reduce bias.

**Example:** Same synthetic data, 200 estimators: AdaBoost test AUC 0.938, sklearn GBM 0.953 (sklearn's GBM is usually the slower of the two to fit).

**Code:**
```python
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
X, y = make_classification(6000, 20, n_informative=8, flip_y=0.1, random_state=0)       # same synthetic set as Q9
Xtr, Xtmp, ytr, ytmp = train_test_split(X, y, test_size=0.4, random_state=0)
Xva, Xte, yva, yte = train_test_split(Xtmp, ytmp, test_size=0.5, random_state=0)
for n, m in [("Ada", AdaBoostClassifier(n_estimators=200, random_state=0)),
             ("GBM", GradientBoostingClassifier(n_estimators=200, random_state=0))]:
    m.fit(Xtr, ytr); print(n, round(roc_auc_score(yte, m.predict_proba(Xte)[:, 1]), 4))  # 0.9377, 0.9527
```

**Follow-ups:**
- *Is AdaBoost a special case of GBM?* Yes, gradient boosting with exponential loss gives AdaBoost-like updates.
- *Why do outliers hurt AdaBoost?* Their weights grow exponentially.

**Common mistakes:** Saying GBM reweights samples. Saying AdaBoost uses deep trees. Forgetting AdaBoost's noise sensitivity.

### Q21 ⭐⭐ 🟡 Extra Trees vs Random Forest: what is different and when is Extra Trees better?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Amazon forecasting DS, Sept 2025 report)
**Say this first (1 line):** Extra Trees picks split thresholds at random instead of searching for the best one (and by default uses the whole sample instead of a bootstrap), which makes trees more random and decorrelated, adds a little bias, cuts variance, and trains much faster.

**Then explain:**
- **Random Forest:** bootstrap rows, random feature subset per split, then the *best* threshold for each candidate feature.
- **Extra Trees:** (extremely randomised) random feature subset, *random* threshold per feature, pick the best of those random splits; sklearn default `bootstrap=False`.
- **Trade-off:** more randomness → lower variance between trees, slightly higher bias; no sorting for thresholds → faster fit.
- **When better:** noisy data, many noisy/redundant features, smooth signals (it behaves like a smoother model), large data where speed matters, or as a diverse member in a stack.
- **When worse:** a few strong features with sharp thresholds, where the optimal cut matters.

**Example:** Same data, 200 trees: RF AUC 0.9538; Extra Trees 0.9532. Almost the same accuracy, and Extra Trees fitted about 2.5 to 3 times faster in my runs (for example 22 s vs 7 s on a busy machine).

**Code:**
```python
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import roc_auc_score
import time
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
X, y = make_classification(6000, 20, n_informative=8, flip_y=0.1, random_state=0)       # same synthetic set as Q9
Xtr, Xtmp, ytr, ytmp = train_test_split(X, y, test_size=0.4, random_state=0)
Xva, Xte, yva, yte = train_test_split(Xtmp, ytmp, test_size=0.5, random_state=0)
for n, m in [("RF", RandomForestClassifier(200, random_state=0)), ("ET", ExtraTreesClassifier(200, random_state=0))]:
    t0 = time.time(); m.fit(Xtr, ytr)
    print(n, round(roc_auc_score(yte, m.predict_proba(Xte)[:, 1]), 4), round(time.time() - t0, 1), "s")   # AUC 0.9538 vs 0.9532
```
(Timings vary by machine; the ratio is what matters.)

**Follow-ups:**
- *Why does randomness help?* It lowers tree correlation ρ, so the ensemble variance falls (Q42).
- *Importance bias?* Extra Trees' MDI is still biased; use permutation importance.

**Common mistakes:** Saying Extra Trees is "random trees with no logic": it still picks the best among random candidates. Forgetting the default no-bootstrap, which means no OOB score unless enabled.

### Q22 ⭐⭐ 🟡 Why is impurity-based (MDI) importance biased, and how does permutation importance help?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** MDI is computed from impurity drops on the training data, so features with many possible split points (continuous, high-cardinality) get credit for fitting noise; permutation importance shuffles a feature on held-out data and measures the real drop in score, so noise features score about zero.

**Then explain:**
- **Why biased:** a feature with many unique values offers many candidate thresholds, so by chance some split reduces impurity. A fully grown tree fits training noise, so these chance splits get counted as "importance". Low-cardinality features have fewer chances.
- **Training-set only:** MDI says nothing about generalisation.
- **Permutation:** score on validation data, shuffle one column, rescore; importance = score drop. Measures what the model actually relies on for prediction. A feature that only helped overfit shows ~0.
- **Caveats:** correlated features (Q23), cost (repeats × features predictions), and it measures dependence of this model, not truth.

**Example:** RF with 3 informative features and 3 useless ones (one is pure Gaussian noise). Train accuracy 1.00, test 0.842. MDI gave the three useless features 0.099, 0.099, 0.096 (about 10% of the total each, nowhere near zero) against 0.177 to 0.309 for the real ones. Permutation on test: useless features 0.002, −0.003, 0.006; real ones 0.192, 0.123, 0.236.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0)
Xs, ys = make_classification(2000, 5, n_informative=3, n_redundant=0, flip_y=0.2, random_state=0)
Xn = np.hstack([Xs, rng.normal(size=(2000, 1))])            # add a pure-noise column
Xa, Xb, ya, yb = train_test_split(Xn, ys, test_size=0.3, random_state=0)
rf = RandomForestClassifier(300, random_state=0).fit(Xa, ya)
print(rf.feature_importances_.round(3))                      # [0.22 0.099 0.177 0.099 0.309 0.096]
print(permutation_importance(rf, Xb, yb, n_repeats=10, random_state=0).importances_mean.round(3))
# [ 0.192 0.002 0.123 -0.003 0.236 0.006]
```

**Follow-ups:**
- *Negative permutation importance?* Shuffling slightly helped by chance, so the feature is useless.
- *Other fix?* Conditional importance, SHAP on validation data, or drop-column importance.

**Common mistakes:** Computing permutation importance on training data (it then also rewards overfitting). Trusting MDI for feature selection.

### Q23 ⭐⭐ 🟡 How does permutation importance behave with correlated features? What would you do about it?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** With correlated features the importance gets split or hidden, because when I shuffle one, the model still gets the same information from its twin, so both look less important than they really are.

**Then explain:**
- **Dilution:** shuffling feature A barely hurts if B carries the same signal. The model may have used A and B interchangeably, so each gets a fraction.
- **Unrealistic samples:** shuffling A alone creates rows (A high, B low) that never occur in real data, so the model is evaluated off-distribution.
- **Fixes:** (1) group correlated features and permute the whole group together; (2) cluster features by Spearman correlation and keep one per cluster; (3) drop-column / refit importance; (4) conditional permutation; (5) report importance for feature *groups* and say so.
- Check correlations (heatmap, VIF) before interpreting.

**Example:** Feature 3 is a near-copy of feature 0 (noise sd 0.05). Without the copy, feature 0 importance = 0.226. With the copy, feature 0 = 0.140 and the copy = 0.052; the pair's importance is diluted and split.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0)
Xs, ys = make_classification(2000, 5, n_informative=3, n_redundant=0, flip_y=0.2, random_state=0)
rng.normal(size=(2000, 1))                       # burn the same draw as the Q22 setup so the numbers match
Xc = Xs[:, :3]; Xc = np.hstack([Xc, Xc[:, [0]] + rng.normal(0, 0.05, (2000, 1))])   # column 3 = near-copy of column 0
Xa, Xb, ya, yb = train_test_split(Xc, ys, test_size=0.3, random_state=0)
rf = RandomForestClassifier(300, min_samples_leaf=5, random_state=0).fit(Xa, ya)  # Xa has a near-duplicate column 3
print(permutation_importance(rf, Xb, yb, n_repeats=10, random_state=0).importances_mean.round(3))
# with duplicate: [0.14 -0.017 0.065 0.052]; without it, feature 0 gets 0.226
# group permutation: shuffle columns [0, 3] with the SAME row permutation and measure the drop
```

**Follow-ups:**
- *Does SHAP fix it?* Not fully; it also splits credit (Q41).
- *Is multicollinearity a problem for prediction in trees?* Not for accuracy, but for interpretation.

**Common mistakes:** Concluding "feature A is useless" because its permutation importance is low while a twin exists. Dropping a feature based on importance without checking correlations.

### Q24 ⭐⭐ 🟡 How do you handle imbalanced data in XGBoost / Random Forest (scale_pos_weight, class_weight, sampling, metric)?
**Asked at:** Product cos, GCCs, analytics/consulting firms, fintech/fraud
**Say this first (1 line):** First choose the right metric (PR-AUC, recall at a precision, cost-based), then use class weights (`scale_pos_weight` / `class_weight`) or sampling if the ranking needs help, and finally pick the decision threshold from the business cost, not 0.5.

**Then explain:**
- **Metric first:** accuracy is useless at 2% positives. Use PR-AUC, recall/precision at a threshold, F-beta, or expected cost. Keep validation data at the true class ratio.
- **XGBoost:** `scale_pos_weight ≈ n_negative / n_positive`; LightGBM `is_unbalance` or `scale_pos_weight`. **RF:** `class_weight="balanced"` or `"balanced_subsample"`, or balanced bootstrap (imbalanced-learn).
- **Sampling:** undersample the majority or oversample (SMOTE) *only inside training folds*. Trees often do fine with plain weights; SMOTE is rarely needed.
- **Threshold tuning:** choose it on validation data from the precision-recall curve and the cost of FP vs FN.
- **Calibration warning:** weighting/resampling distorts predicted probabilities. If you need real probabilities (pricing, expected loss), recalibrate (isotonic/Platt) or don't reweight.

**Example:** 2.5% positives. Plain XGBoost PR-AUC 0.559; with `scale_pos_weight=49` PR-AUC 0.559 (ranking unchanged), but mean predicted probability rose from 0.018 to 0.061 vs a true rate of 0.025, so the probabilities are inflated. For a ranking use case weights are optional; for probability use, they hurt calibration.

**Code:**
```python
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split
Xi, yi = make_classification(20000, 20, n_informative=6, weights=[0.98], flip_y=0.01, random_state=0)   # about 2.5% positives
Xa, Xb, ya, yb = train_test_split(Xi, yi, test_size=0.3, stratify=yi, random_state=0)
spw = (ya == 0).sum() / (ya == 1).sum()
m = xgb.XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.1, scale_pos_weight=spw, random_state=0).fit(Xa, ya)
print(average_precision_score(yb, m.predict_proba(Xb)[:, 1]))   # PR-AUC on an untouched, imbalanced test set
# RF: RandomForestClassifier(class_weight="balanced_subsample")
```

**Follow-ups:**
- *Why not SMOTE?* It can create unrealistic points and leaks if done before splitting.
- *How set threshold?* Maximise expected profit or F-beta on validation.

**Common mistakes:** Resampling before the split. Judging by accuracy/ROC-AUC. Using weighted probabilities as if calibrated. Resampling the test set.

### Q25 ⭐⭐ 🟡 Level-wise vs leaf-wise tree growth: what do they mean, and how do num_leaves and max_depth interact in LightGBM?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** Level-wise grows all nodes at one depth before going deeper; leaf-wise (LightGBM) always splits the single leaf with the largest loss reduction, giving deeper, lopsided trees that reach lower loss with fewer leaves but overfit more easily, so `num_leaves` is the main complexity knob and `max_depth` a safety cap.

**Then explain:**
- **Level-wise** (XGBoost default, sklearn): balanced trees, more regular, safer on small data.
- **Leaf-wise (best-first):** greedy gain-driven growth. For the same number of leaves it usually fits better, but one branch can go very deep on a few noisy points.
- **Interaction:** a depth-d tree has at most 2^d leaves, so `num_leaves` should be below 2^`max_depth` (e.g. depth 6 → at most 64 leaves; depth 5 → 32, so the default 31 just fits). If `num_leaves` > 2^`max_depth` it is effectively capped by depth.
- **Controls on small data:** lower `num_leaves`, raise `min_data_in_leaf`, set `max_depth`, add `lambda_l1/l2`, `min_gain_to_split`.

**Example:** 6000 rows, 200 trees, lr 0.05: `num_leaves=31` AUC 0.9506; `num_leaves=255` 0.9507; `num_leaves=31, max_depth=5` 0.9509. On this dataset the settings made no difference, so on small or easy data the complexity limits matter less than on noisy data; I would still cap them.

**Code:**
```python
import lightgbm as lgb
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
X, y = make_classification(6000, 20, n_informative=8, flip_y=0.1, random_state=0)       # same synthetic set as Q9
Xtr, Xtmp, ytr, ytmp = train_test_split(X, y, test_size=0.4, random_state=0)
Xva, Xte, yva, yte = train_test_split(Xtmp, ytmp, test_size=0.5, random_state=0)
m = lgb.LGBMClassifier(n_estimators=200, learning_rate=0.05, num_leaves=31, max_depth=5,
                       min_child_samples=20, verbose=-1, random_state=0).fit(Xtr, ytr)
print(round(roc_auc_score(yte, m.predict_proba(Xte)[:, 1]), 4))     # 0.9509 (the num_leaves=31, max_depth=5 run in the example)
```

**Follow-ups:**
- *Why do people say LightGBM overfits small data?* Leaf-wise growth and few samples per leaf; fix with `min_data_in_leaf`.
- *Can XGBoost do leaf-wise?* Yes, `grow_policy="lossguide"` with `max_leaves`.

**Common mistakes:** Setting `num_leaves` far above 2^`max_depth`. Treating `max_depth` as the main knob in LightGBM. Not raising `min_data_in_leaf` on small data.

### Q26 ⭐⭐ 🟡 Grid vs random vs Bayesian (Optuna) search for tree models: which do you choose and how do you cross-validate?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** I use random search for a quick broad pass and Bayesian search (Optuna/TPE) for the real tuning, since grid search wastes trials on unimportant parameters; every trial is scored with stratified (or time/group-aware) CV, and a final holdout is touched once.

**Then explain:**
- **Grid:** tries every combination; cost explodes with parameters; only for 2 to 3 parameters.
- **Random:** samples the space; with few important parameters it covers them better than a grid for the same budget (Bergstra & Bengio).
- **Bayesian (Optuna TPE):** uses past trial results to propose promising values; pruning kills bad trials early. Best for expensive models.
- **CV choice:** stratified K-fold for classification, `TimeSeriesSplit` for time data, `GroupKFold` for grouped entities. Use early stopping inside folds. Use log scale for learning rate and λ.
- **Overfitting the search:** with many trials the best CV score is optimistic. Hold out a final test set or use nested CV.
- Fix the seed and record the search space.

**Example:** on the shared synthetic set (training part only, 3-fold CV AUC), a 10-trial random search reached about 0.939 (depth 5, lr 0.069, subsample 0.61; that run is not in the code below) and the 15-trial Optuna study below reached 0.9376. Both land close together because this problem is easy and trial counts are tiny, so do not read a ranking of methods from it; the real gain from Optuna comes with larger budgets and pruning.

**Code:**
```python
import optuna, xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split
X, y = make_classification(6000, 20, n_informative=8, flip_y=0.1, random_state=0)       # same synthetic set as Q9
Xtr, Xtmp, ytr, ytmp = train_test_split(X, y, test_size=0.4, random_state=0)            # tune on the training part only
def objective(trial):
    p = dict(max_depth=trial.suggest_int("max_depth", 3, 8),
             learning_rate=trial.suggest_float("learning_rate", 0.02, 0.3, log=True),
             subsample=trial.suggest_float("subsample", 0.6, 1.0),
             colsample_bytree=trial.suggest_float("colsample_bytree", 0.5, 1.0),
             min_child_weight=trial.suggest_int("min_child_weight", 1, 10),
             reg_lambda=trial.suggest_float("reg_lambda", 1e-2, 10, log=True))
    cv = StratifiedKFold(3, shuffle=True, random_state=0)
    return cross_val_score(xgb.XGBClassifier(n_estimators=150, random_state=0, **p), Xtr, ytr, cv=cv, scoring="roc_auc").mean()
study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=0))
study.optimize(objective, n_trials=15)
print(study.best_value, study.best_params)    # best CV AUC 0.9376 in my run (depth 5, lr 0.04, ...)
```

**Follow-ups:**
- *How many trials?* 50 to 200 for GBMs, fewer with a good prior.
- *Hyperparameter search leakage?* Do feature engineering/target encoding inside the CV folds.

**Common mistakes:** Reporting the best CV score as the test estimate. Plain K-fold on time series. Linear scale for learning rate.

### Q27 ⭐⭐ 🟡 Why can't tree-based models extrapolate, and what do you do when you need to?
**Asked at:** Product cos, GCCs, analytics/consulting firms, forecasting/pricing teams
**Say this first (1 line):** A tree predicts the mean of training targets in a leaf, so outside the training range it just repeats the edge leaf's value (a flat line); to extrapolate I model the trend separately, predict differences/ratios, or use a model with linear leaves.

**Then explain:**
- Prediction is piecewise constant, so for x beyond the max seen, you get the last leaf's value. Forests and GBMs average such steps, so they also flatten.
- **Fixes:**
  - Detrend: fit a linear model (or a growth curve) and let the tree model the residuals.
  - Predict a stationary target: differences, growth rates, or ratios to a baseline, then rebuild.
  - Linear trees: LightGBM `linear_tree=True` or Cubist-style leaves.
  - Use a model that extrapolates (linear, GAM, NN) or combine it with the tree in an ensemble.
  - Add features such as time index only if the trend is handled elsewhere.
- Important for time series, pricing and anything with growth.

**Example:** y = 2x + noise, trained on x in [0, 10], tested at x = 12 and 15 (truth 24, 30). Tree: 19.7, 19.7. Linear: 23.9, 29.9. LightGBM `linear_tree`: 23.9, 29.9. Linear + tree on residuals: 23.9, 29.9.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
xt = np.linspace(0, 10, 200)[:, None]; yt = 2*xt[:, 0] + np.random.default_rng(0).normal(0, 0.5, 200)
xo = np.array([[12.], [15.]])
print(DecisionTreeRegressor(max_depth=5).fit(xt, yt).predict(xo).round(1))        # [19.7 19.7]
lin = LinearRegression().fit(xt, yt)
tree = DecisionTreeRegressor(max_depth=3).fit(xt, yt - lin.predict(xt))
print((lin.predict(xo) + tree.predict(xo)).round(1))                                # [23.9 29.9]
```

**Follow-ups:**
- *Is a tree bad for time series?* Not if the target is detrended or differenced.
- *Does boosting help?* No, still piecewise constant.

**Common mistakes:** Feeding a raw time index to a GBM and expecting a trend continuation. Validating inside the training range only; use a split that extrapolates (time-based).

### Q28 ⭐⭐ 🟡 How do you read SHAP plots (summary/beeswarm, dependence, waterfall) and what decisions do they support?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** SHAP splits each prediction into one contribution per feature that adds up exactly to the model output; the beeswarm shows which features matter and in what direction (global), the dependence plot shows the shape of one feature's effect, and the waterfall explains one prediction (local).

**Then explain:**
- **Units:** for a tree classifier SHAP values are in log-odds (the raw margin), not probability. `base value + sum of SHAP values = model output` for that row.
- **Summary / beeswarm:** one dot per row per feature. Rows are features sorted by mean |SHAP|. Horizontal position = push on the prediction (right = raises it). Colour = feature value (red high, blue low). Read it like this: "high `n_calls` (red) sits on the right, so more calls raise churn risk". A wide spread means the feature acts differently across rows, which hints at interactions.
- **Dependence plot:** x = feature value, y = its SHAP value. It shows the shape: linear, threshold, U-shape. Vertical scatter at the same x means interactions. Colour by a second feature to see which one.
- **Waterfall (local):** starts at the base value, adds each feature's push, ends at this row's prediction. Use it for a customer-level "why".
- **Decisions it supports:** sanity-check direction against domain knowledge, catch leakage (one absurdly dominant feature), choose features to drop, write reason codes for a rejected loan, spot where to add a monotonic constraint, compare train vs live SHAP for drift.

**Example:** churn model, one customer: base -1.0, `n_calls=9` adds +1.4, `tenure=2` adds +0.6, `plan=basic` subtracts 0.3, output +0.7 log-odds, about 67% churn probability. The retention team sees "calls and short tenure drive this".

**Code:**
```python
import numpy as np, pandas as pd, shap, xgboost as xgb
from sklearn.datasets import make_classification
X, y = make_classification(2000, 6, n_informative=4, random_state=0)
X = pd.DataFrame(X, columns=[f"f{i}" for i in range(6)])
model = xgb.XGBClassifier(n_estimators=100, max_depth=3, random_state=0).fit(X, y)
exp = shap.TreeExplainer(model)(X)            # Explanation: values are in log-odds
print("global importance (mean |SHAP|):")
print(pd.Series(np.abs(exp.values).mean(0), X.columns).sort_values(ascending=False).round(3).to_string())
row = 0
print("base + sum(SHAP) =", round(float(exp.base_values[row] + exp.values[row].sum()), 4),
      "| model margin =", round(float(model.predict(X.iloc[[row]], output_margin=True)[0]), 4))
# shap.plots.beeswarm(exp); shap.plots.scatter(exp[:, "f0"], color=exp); shap.plots.waterfall(exp[row])
```
Output from my run: top feature f1 (mean |SHAP| 1.142), then f5 0.926, f3 0.849; `base + sum(SHAP) = -2.0548`, equal to the model margin `-2.0548` (additivity check passes).

**Follow-ups:**
- *Does SHAP show causation?* No. It explains what the model does, not what happens if you change the feature.
- *How do I show probability instead of log-odds?* Use `model_output="probability"` with an interventional explainer and a background set, or convert at the end.
- *Is mean |SHAP| the same as gain importance?* Related but not the same; SHAP is consistent and signed per row, gain is not.

**Common mistakes:** Reading SHAP as causal. Reading the beeswarm colour as "importance". Forgetting values are log-odds. Explaining correlated features one by one (see Q41).

### Q29 ⭐⭐ 🟡 How do you handle high-cardinality categorical features with tree models? Why can one-hot encoding hurt?
**Asked at:** Product cos, GCCs, analytics/consulting firms, e-commerce/fintech
**Say this first (1 line):** For high-cardinality categories I use out-of-fold smoothed target encoding, or the library's native categorical handling (LightGBM/CatBoost), or frequency/embedding encodings; one-hot explodes into thousands of sparse columns where each column is too weak for a tree to split on.

**Then explain:**
- **Why one-hot hurts trees:** a city with 2,000 levels becomes 2,000 columns. Each one is 1 for a tiny slice of rows, so a split on it gives almost no gain; the tree needs many splits to carve out a group. Memory and training time go up, and the signal gets spread thin (so importance is diluted across the dummies).
- **Why plain label encoding is risky:** arbitrary integer codes impose a fake order; the tree can only split "code <= 700", which groups unrelated cities.
- **Target encoding:** replace the category by a smoothed mean of the target, `(sum + m*prior)/(count + m)`. Must be computed **out-of-fold**, otherwise a row sees its own label (leakage; CatBoost fixes this with ordered statistics, see Q40).
- **Native categorical:** LightGBM sorts categories by gradient statistics and finds the best grouped split. CatBoost does ordered target stats. XGBoost has `enable_categorical=True` (hist). All need enough rows per level and regularisation (`cat_smooth`, `min_data_per_group`).
- **Others:** frequency encoding, hashing, grouping rare levels into "other", or learned embeddings.

**Example:** 20,000 rows, 2,000 cities, about 7 rows per city; the city effect is real. With LightGBM defaults: integer code AUC 0.529, native categorical 0.502, out-of-fold smoothed target encoding 0.72 (one synthetic run).

**Code:**
```python
import numpy as np, pandas as pd, lightgbm as lgb
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
n, K = 20000, 2000
city = rng.integers(0, K, n)
eff = rng.normal(0, 1.2, K)
y = (rng.random(n) < 1/(1+np.exp(-(eff[city] - 0.3)))).astype(int)
df = pd.DataFrame({"city": city, "noise": rng.normal(size=n)})
tr, te = train_test_split(np.arange(n), test_size=0.3, random_state=0)
def enc_map(d, yv, smooth, prior):
    s = pd.DataFrame({"c": d.city.values, "y": yv}).groupby("c").y.agg(["sum", "count"])
    return (s["sum"] + smooth*prior) / (s["count"] + smooth)          # smoothed mean toward the prior
def oof_te(d_tr, y_tr, d_te, smooth=20):
    prior = y_tr.mean(); out = np.zeros(len(d_tr))
    for a, b in KFold(5, shuffle=True, random_state=0).split(d_tr):   # encode each fold using the OTHER folds
        out[b] = d_tr.iloc[b].city.map(enc_map(d_tr.iloc[a], y_tr[a], smooth, prior)).fillna(prior).values
    return out, d_te.city.map(enc_map(d_tr, y_tr, smooth, prior)).fillna(prior).values
P = dict(n_estimators=200, learning_rate=0.05, num_leaves=15, verbose=-1, random_state=0)
d_tr, d_te, y_tr, y_te = df.iloc[tr], df.iloc[te], y[tr], y[te]
a = lgb.LGBMClassifier(**P).fit(d_tr, y_tr)
print("raw int code       AUC", round(roc_auc_score(y_te, a.predict_proba(d_te)[:, 1]), 3))
cats = d_tr.city.astype("category").cat.categories
dc_tr, dc_te = d_tr.assign(city=pd.Categorical(d_tr.city, categories=cats)), d_te.assign(city=pd.Categorical(d_te.city, categories=cats))
b = lgb.LGBMClassifier(**P, cat_smooth=20).fit(dc_tr, y_tr)
print("native categorical AUC", round(roc_auc_score(y_te, b.predict_proba(dc_te)[:, 1]), 3))
e_tr, e_te = oof_te(d_tr, y_tr, d_te)
c = lgb.LGBMClassifier(**P).fit(pd.DataFrame({"te": e_tr, "noise": d_tr.noise.values}), y_tr)
print("OOF target encoding AUC", round(roc_auc_score(y_te, c.predict_proba(pd.DataFrame({"te": e_te, "noise": d_te.noise.values}))[:, 1]), 3))
print("one-hot would create", K, "sparse columns")
```
The native result is poor here only because there are about 7 rows per level and defaults like `min_data_per_group=100` block most splits; that is itself a good interview point (native handling needs enough data per level or tuning).

**Follow-ups:**
- *Unseen category at inference?* Map to the global prior (target encoding) or an "unknown" bucket; LightGBM sends unseen levels to the "other" side.
- *When is one-hot fine?* Low cardinality (say under 10 to 15), or for linear models.
- *Time-dependent data?* Compute the encoding with past data only, not random folds.

**Common mistakes:** Target encoding on the full training set then cross-validating (leakage; CV looks great, production fails). No smoothing, so rare levels get 0 or 1. Fitting the encoder before the train/test split.

### Q30 ⭐⭐ 🟡 Code: implement a best-split finder (or a small decision tree) from scratch in NumPy.
**Asked at:** Product cos, GCCs, analytics/consulting firms (live coding)
**Say this first (1 line):** For every feature, sort the values, try each midpoint between neighbours as a threshold, compute the weighted child impurity, and keep the best; then recurse on the two halves until a stop rule fires.

**Then explain:**
- **Gini** of a node = `1 - sum(p_k^2)`. Split score = weighted average of the two children's Gini. Lower is better.
- **Candidates:** only midpoints between distinct sorted values matter (about n-1 per feature).
- **Cost:** this naive version recomputes the impurity per candidate, O(n^2 d) per node. Real libraries sort once and update class counts incrementally with a running sum, giving O(n log n * d) per node (and histograms make it faster still, see Q47).
- **Stop rules:** max depth, minimum samples, or a pure node. The leaf predicts the majority class.

**Example:** data where the label is `x0 > 0.2 and x1 > -0.5`. The finder picks feature 0 at threshold 0.195 at the root, which is right.

**Code:**
```python
import numpy as np
def gini(y):
    p = np.bincount(y, minlength=2) / len(y); return 1 - (p**2).sum()
def best_split(X, y):
    n, d = X.shape; best = (None, None, gini(y))            # (feature, threshold, weighted impurity)
    for j in range(d):
        order = np.argsort(X[:, j]); xs, ys = X[order, j], y[order]
        for i in range(1, n):                                # candidate between sorted i-1 and i
            if xs[i] == xs[i-1]: continue
            l, r = ys[:i], ys[i:]
            imp = (len(l)*gini(l) + len(r)*gini(r)) / n
            if imp < best[2]: best = (j, (xs[i-1] + xs[i]) / 2, imp)
    return best
def build(X, y, depth=0, max_depth=3, min_samples=5):
    if depth == max_depth or len(y) < min_samples or gini(y) == 0: return int(np.bincount(y).argmax())
    j, t, _ = best_split(X, y)
    if j is None: return int(np.bincount(y).argmax())
    m = X[:, j] <= t
    return (j, t, build(X[m], y[m], depth+1, max_depth, min_samples), build(X[~m], y[~m], depth+1, max_depth, min_samples))
def predict_one(node, x):
    while isinstance(node, tuple): node = node[2] if x[node[0]] <= node[1] else node[3]
    return node
rng = np.random.default_rng(0)
X = rng.normal(size=(400, 3)); y = ((X[:, 0] > 0.2) & (X[:, 1] > -0.5)).astype(int)
tree = build(X[:300], y[:300])
pred = np.array([predict_one(tree, x) for x in X[300:]])
print("root split (feature, threshold):", tree[0], round(tree[1], 3))
print("test accuracy:", (pred == y[300:]).mean())
from sklearn.tree import DecisionTreeClassifier
print("sklearn depth-3 accuracy:", DecisionTreeClassifier(max_depth=3, random_state=0).fit(X[:300], y[:300]).score(X[300:], y[300:]))
```
Output: root split `(0, 0.195)`, test accuracy 1.0, same as sklearn depth-3 (1.0).

**Follow-ups:**
- *How would you make it faster?* Sort once per feature and keep running class counts; use histogram bins.
- *Regression?* Replace Gini by variance (SSE) and the leaf by the mean (Q17).
- *Categorical features?* Try subsets of categories, or order categories by target mean first.

**Common mistakes:** Not weighting child impurities by size. Using the raw value instead of the midpoint, or splitting between equal values. Forgetting the "no valid split" case, which leads to infinite recursion.

### Q31 ⭐⭐ 🟡 Code: implement a Random Forest from scratch (bootstrap + feature subsampling + voting).
**Asked at:** Product cos, GCCs, analytics/consulting firms (live coding)
**Say this first (1 line):** A forest is a loop: draw a bootstrap sample, grow a deep tree that looks at a random subset of features at every split, and at the end average the trees' votes; the OOB rows give a free validation score.

**Then explain:**
- **Bootstrap:** sample n rows with replacement. Each tree sees about 63% unique rows (1 - 1/e); the rest are out-of-bag (OOB).
- **Feature subsampling:** `max_features` (sqrt of d for classification) is chosen at each split, not once per tree. It decorrelates trees (Q42).
- **Voting:** average class probabilities (soft vote, what sklearn does) or take a majority vote.
- **OOB score:** predict each row only with trees that never saw it; no extra holdout needed.
- To keep the code short I reuse sklearn's `DecisionTreeClassifier` with `max_features`; the from-scratch tree is in Q30.

**Example:** on a 2,000-row, 20-feature problem: single tree 0.866, my forest 0.906, sklearn forest 0.908.

**Code:**
```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
class MyForest:
    def __init__(self, n_trees=100, max_features="sqrt", max_depth=None, seed=0):
        self.n_trees, self.mf, self.md, self.seed = n_trees, max_features, max_depth, seed
    def fit(self, X, y):
        rng = np.random.default_rng(self.seed); n = len(X); self.trees = []; self.oob = np.zeros((n, 2))
        for _ in range(self.n_trees):
            idx = rng.integers(0, n, n)                                   # bootstrap: sample with replacement
            t = DecisionTreeClassifier(max_features=self.mf, max_depth=self.md,
                                       random_state=int(rng.integers(1 << 30))).fit(X[idx], y[idx])
            oob = np.setdiff1d(np.arange(n), idx)                         # rows this tree never saw
            self.oob[oob] += t.predict_proba(X[oob]); self.trees.append(t)
        self.oob_acc_ = (self.oob.argmax(1) == y)[self.oob.sum(1) > 0].mean()
        return self
    def predict(self, X):
        return (np.mean([t.predict_proba(X) for t in self.trees], 0)).argmax(1)   # soft vote
X, y = make_classification(2000, 20, n_informative=8, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
f = MyForest(100).fit(Xtr, ytr)
print("mine    test acc", round((f.predict(Xte) == yte).mean(), 3), "| OOB acc", round(f.oob_acc_, 3))
print("sklearn test acc", round(RandomForestClassifier(100, random_state=0).fit(Xtr, ytr).score(Xte, yte), 3))
print("single tree      ", round(DecisionTreeClassifier(random_state=0).fit(Xtr, ytr).score(Xte, yte), 3))
```
Output: mine 0.906 (OOB 0.918), sklearn 0.908, single tree 0.866. The code assumes binary labels 0/1.

**Follow-ups:**
- *Why is OOB close to test accuracy?* Each OOB prediction uses trees that never saw that row, so it is an honest estimate (slightly pessimistic since only about 37% of the trees vote).
- *Parallelise?* Trees are independent, so `n_jobs` scales almost linearly.
- *Why a deep tree per bootstrap?* Deep trees have low bias; averaging removes the variance.

**Common mistakes:** Sampling features once per tree instead of per split. Bootstrapping without replacement. Using hard votes when probabilities are needed (poor calibration, ties).

### Q32 ⭐⭐ 🟡 AI-era: an LLM generated this XGBoost training pipeline. Review it and find the bugs (leakage, early stopping on test set, encoding, metrics).
**Asked at:** Product cos, GCCs, analytics/consulting firms, AI-assisted code-review rounds
**Say this first (1 line):** I would reject this pipeline: it leaks a post-outcome column, early-stops on the test set, encodes the city with arbitrary integer codes, scales for no reason, and reports accuracy on a 14% positive problem; fixed, the honest AUC is about 0.70, not 1.0.

**Then explain (bugs in the LLM's code):**

| # | Bug | Why it is wrong | Fix |
|---|---|---|---|
| 1 | `days_since_cancel` kept as a feature | It exists only after the customer churned (target leakage). That is why accuracy and AUC are 1.0 | Drop it; ask "would I know this at prediction time?" |
| 2 | `eval_set=[(Xte, yte)]` with early stopping | The test set picks the number of trees, so it is no longer unbiased | Train / validation / test split; early stop on validation only |
| 3 | `city.cat.codes` | Fake order for a nominal feature; the tree can only split on "code <= k" | `category` dtype with `enable_categorical=True`, or target encoding in-fold |
| 4 | `StandardScaler` fit on all data | Useless for trees, and fitting on all rows is leakage in principle | Remove it; if scaling is ever needed, put it in a Pipeline |
| 5 | Accuracy as the metric | A model that says "no churn" gets 86% | ROC-AUC, PR-AUC, recall at a threshold; compare with the base rate |
| 6 | No `stratify`, no time-aware split | Positive rate can drift between splits; if data is a time series, random split leaks the future | Stratified split or time-based split |

**Example:** the synthetic churn table in the code below has 6,000 customers (age, income, city, number of calls) with about 14% churners, plus the leaky `days_since_cancel` column. The buggy pipeline scores a perfect 1.0, which is the red flag. The fixed pipeline scores a modest AUC of about 0.70, and that is the honest number.

**Code (one runnable script: synthetic data, the buggy version, then the fixed version):**
```python
import numpy as np, pandas as pd, xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.preprocessing import StandardScaler
rng = np.random.default_rng(0)
n = 6000
df = pd.DataFrame({"age": rng.integers(18, 70, n), "income": rng.lognormal(10, 0.6, n),
                   "city": rng.choice(list("ABCDEFGH"), n), "n_calls": rng.poisson(3, n)})
logit = -4 + 0.02*df.age + 0.35*df.n_calls + (df.city == "C")*0.8
df["churn"] = (rng.random(n) < 1/(1+np.exp(-logit))).astype(int)
df["days_since_cancel"] = np.where(df.churn == 1, rng.integers(0, 30, n), np.nan)     # LEAK: only exists after churn
# ---------- BUGGY (what the LLM wrote) ----------
X = df.drop(columns="churn").copy()
X["city"] = X.city.astype("category").cat.codes                          # bug: arbitrary order codes
X[["age", "income"]] = StandardScaler().fit_transform(X[["age", "income"]])   # bug: pointless, fit on ALL data
Xtr, Xte, ytr, yte = train_test_split(X, df.churn, test_size=0.2, random_state=0)
m = xgb.XGBClassifier(n_estimators=500, learning_rate=0.1, eval_metric="logloss", early_stopping_rounds=20, random_state=0)
m.fit(Xtr, ytr, eval_set=[(Xte, yte)], verbose=False)                    # bug: early stopping on the TEST set
print("BUGGY  accuracy", round((m.predict(Xte) == yte).mean(), 3), "| AUC", round(roc_auc_score(yte, m.predict_proba(Xte)[:, 1]), 3))
# ---------- FIXED ----------
X = df.drop(columns=["churn", "days_since_cancel"]).copy()                # drop the leaky column
X["city"] = X.city.astype("category")
Xtmp, Xte, ytmp, yte = train_test_split(X, df.churn, test_size=0.2, stratify=df.churn, random_state=0)
Xtr, Xva, ytr, yva = train_test_split(Xtmp, ytmp, test_size=0.25, stratify=ytmp, random_state=0)
m = xgb.XGBClassifier(n_estimators=500, learning_rate=0.05, eval_metric="aucpr", early_stopping_rounds=30,
                      enable_categorical=True, tree_method="hist", random_state=0)
m.fit(Xtr, ytr, eval_set=[(Xva, yva)], verbose=False)                     # early stop on validation only
p = m.predict_proba(Xte)[:, 1]
print("FIXED  AUC", round(roc_auc_score(yte, p), 3), "| PR-AUC", round(average_precision_score(yte, p), 3),
      "| baseline PR-AUC", round(yte.mean(), 3), "| best_iteration", m.best_iteration)
```
Output: buggy accuracy 1.0 and AUC 1.0 (too good to be true); fixed AUC 0.701, PR-AUC 0.281 against a 0.139 base rate, best iteration 56.

**Follow-ups:**
- *How would you spot the leak without knowing the column?* A feature with extreme importance or SHAP, a near-perfect score, missing values that match the label exactly.
- *Who should review LLM-generated ML code?* Always check split order, what each `fit` saw, the metric, and feature availability at serving time.

**Common mistakes:** Trusting a score of 1.0. Treating the early-stopped test score as final. Using accuracy on imbalanced data. Letting an LLM "tidy" preprocessing that quietly fits on all data.

### Q33 ⭐⭐ 🟡 Why do GBDTs still often beat deep learning on tabular data? When would you pick a neural net or a tabular foundation model instead?
**Asked at:** Product cos, GCCs, analytics/consulting firms, Europe product cos
**Say this first (1 line):** On medium-sized, heterogeneous tabular data, GBDTs usually match or beat neural nets because their inductive bias fits tabular structure and they need almost no tuning; I would pick a neural net when the data is huge, multimodal, needs embeddings or joint training, and a tabular foundation model when data is small.

**Then explain:**
- **Why trees win (Grinsztajn et al., 2022 benchmark of medium-sized tabular data):**
  - Tabular targets are often **irregular functions** (sharp thresholds); trees cut at thresholds, MLPs prefer smooth functions.
  - **Uninformative features** hurt MLPs more; trees just ignore them.
  - Features are **not rotation invariant** (age and income mean different things); MLPs treat input space symmetrically, trees do not.
  - Mixed types, missing values and skewed scales need little preprocessing for trees.
  - Tuning cost: a default GBM is already strong; NNs need architecture, scaling, regularisation and many seeds.
- **When a neural net is the right pick:**
  - Millions of rows plus high-cardinality IDs where **embeddings** help (recommenders, ads).
  - **Multimodal** input (text/image + tabular) trained end to end.
  - Need for **multi-task learning**, transfer learning, online/streaming updates, or differentiable components.
- **Tabular foundation models (for example TabPFN):** a transformer pre-trained on many synthetic datasets that predicts in one forward pass without training. Strong on **small** data (up to roughly thousands of rows), no tuning. Limits: row/feature scale, inference cost, less mature tooling.
- **Practical answer:** start with a GBM baseline, then try an NN or a blend only if it adds measurable lift; blends of GBM + NN often win Kaggle-style.

**Example:** 5,000-row churn dataset with 30 mixed features: LightGBM with defaults in minutes. 200M-row ad-click data with user/item IDs: an embedding NN (or GBM + NN) because ID embeddings carry the signal.

**Follow-ups:**
- *Is it true GBDTs always win?* No; the claim is for medium data. At large scale or with rich structure the gap closes or reverses.
- *How to compare fairly?* Same CV, same tuning budget, several seeds.
- *Would you deploy a tabular foundation model?* For small-data problems as a baseline or ensemble member, after checking latency, licence and data-size limits.

**Common mistakes:** Claiming "deep learning is always better" or "trees always win". Comparing a tuned GBM with an untuned NN (or the reverse). Ignoring serving cost and maintainability.

### Q34 ⭐⭐ 🟡 How do you do feature selection with tree models (importance thresholds, RFE, Boruta) and what can go wrong?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Flipkart MLE guide-type)
**Say this first (1 line):** I rank features with a tree model (preferably permutation or SHAP importance), drop the weak ones by a threshold, RFE or Boruta, and always do the selection inside cross-validation, because selecting on the full data leaks and correlated features make importances unstable.

**Then explain:**
- **Importance threshold:** keep features above the median or above a cut-off (`SelectFromModel`). Fast, but one pass only.
- **RFE / RFECV:** repeatedly fit, drop the weakest few, refit; `RFECV` picks the count by CV. Better, but costs many fits.
- **Boruta:** add shuffled "shadow" copies of every feature; keep a real feature only if it beats the best shadow importance repeatedly (statistical test). Good at finding all relevant features, not a minimal set.
- **What can go wrong:**
  - **Biased importance:** MDI favours high-cardinality and continuous features (Q22); use permutation or SHAP.
  - **Correlated features:** importance is split between them, so each looks weak and both may be dropped (Q23).
  - **Selection leakage:** choosing features on all data, then cross-validating, inflates the score.
  - **Instability:** the selected set changes with the seed; check across folds.
  - Dropping features that matter only through interactions.
- **Often not needed:** GBMs tolerate extra features; select mainly for cost, latency, interpretability, or cleaner data pipelines.

**Example:** 30 features, only columns 0 to 4 are real. A median threshold kept 15 features (all 5 real ones); `RFECV` kept exactly 5 (all real). CV AUC with selection inside the folds: 0.968.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV, SelectFromModel
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
X, y = make_classification(1500, 30, n_informative=5, n_redundant=0, shuffle=False, random_state=0)  # columns 0-4 are the real ones
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
rf = RandomForestClassifier(100, n_jobs=2, random_state=0)
sel = SelectFromModel(rf, threshold="median").fit(Xtr, ytr)               # importance threshold
print("median threshold kept:", sel.get_support().sum(), "| real features kept:", sel.get_support()[:5].sum(), "of 5")
rfe = RFECV(RandomForestClassifier(50, max_depth=8, n_jobs=2, random_state=0), step=5, cv=3, scoring="roc_auc").fit(Xtr, ytr)
print("RFECV kept:", rfe.n_features_, "| real features kept:", rfe.support_[:5].sum(), "of 5")
# selection must live INSIDE the CV loop (Pipeline), otherwise the CV score is optimistic
pipe = make_pipeline(SelectFromModel(RandomForestClassifier(50, random_state=0), max_features=5, threshold=-np.inf),
                     RandomForestClassifier(50, random_state=0))
print("CV AUC with selection inside folds:", cross_val_score(pipe, Xtr, ytr, cv=3, scoring="roc_auc").mean().round(3))
```
This took about 80 seconds on my machine because of RFECV (machine-specific); use fewer trees for a quick test. Boruta is in the `boruta_py` package (not run here).

**Follow-ups:**
- *Remove correlated features first?* Cluster them and keep one per cluster, or use SHAP on grouped features.
- *Do you need selection for XGBoost?* Rarely for accuracy; yes for cost, stability and explainability.

**Common mistakes:** Selecting on the full dataset before CV. Trusting a single MDI ranking. Dropping one of two correlated features based on its low importance without checking the pair.

### Q35 ⭐⭐ 🟡 How would you explain a gradient boosting model's decision to a non-technical stakeholder or regulator?
**Asked at:** Product cos, GCCs, analytics/consulting firms, regulated GCCs, fintech
**Say this first (1 line):** I explain it at two levels: globally, "these are the factors the model relies on and how each moves the score", and locally, "these are the top reasons for this customer's score", using SHAP plus plain-language reason codes, and I back it with validation evidence and guardrails.

**Then explain:**
- **Do not explain 500 trees.** Say "the model is many small decision rules added together, each fixing the previous mistakes", then move to behaviour.
- **Global view:** top 5 to 10 drivers (mean |SHAP|), with direction ("more missed payments raise risk"), shown as a bar chart and a few dependence/partial-dependence plots.
- **Local view:** a waterfall or "top 3 reasons" per decision, translated to business words ("high credit utilisation", not `f17`).
- **Trust evidence:** performance on a holdout, calibration, stability over time, fairness checks across groups, comparison to a simple baseline.
- **Guardrails regulators like:** monotonic constraints so effects have sensible direction (Q49), no proxy features for protected attributes, documentation (model card, data lineage, validation report), human override and monitoring.
- **Be honest about limits:** SHAP explains the model, not causes; for correlated features attribution is shared (Q41). If a hard rule is required, use a simpler model (scorecard, GAM) or a surrogate and state the accuracy cost.

**Example:** loan declined. Script: "The score was 0.74 against an approval cut-off of 0.50. The three biggest factors pushing it up were credit utilisation of 92%, two missed payments in 6 months, and a short credit history. Reducing utilisation below 50% would move the score toward approval" (a counterfactual, checked by re-scoring, not read from SHAP).

**Follow-ups:**
- *Is a GBM "a black box" for a regulator?* It is opaque internally, but explainable through attributions, monotonic constraints and testing; some regulators or risk teams still prefer a GAM or a scorecard for high-stakes decisions.
- *Global vs local mismatch?* A feature can be globally minor but decisive for one person; show both.
- *What if the stakeholder asks "what should the customer change?"* Use counterfactual explanations and only actionable features.

**Common mistakes:** Showing raw SHAP plots with technical feature names. Implying causality. Overselling an explanation without validating the model. Giving reason codes from a different model than the one that scored.

### Q36 ⭐⭐ 🟡 Stacking / blending vs a single Random Forest or GBM: when is an ensemble of ensembles worth it?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** Stacking trains a meta-model on the out-of-fold predictions of several base models; it usually adds a small lift over the best single GBM, so it is worth it only when that lift is valuable (competitions, high-value decisions) and the extra complexity and latency are acceptable.

**Then explain:**
- **Blending:** average (or weighted average) the base predictions; simple, no leakage risk if weights are fit on a holdout.
- **Stacking:** base models make **out-of-fold** predictions on the training set; a meta-model (often logistic or ridge regression) learns how to combine them. In-fold predictions would leak and give the meta-model overconfident inputs.
- **Why it works:** different model families make different errors; averaging uncorrelated errors cuts variance (same logic as Q42). Gains vanish when models are similar (XGB + LightGBM + CatBoost often agree).
- **Cost:** k times the training, more serving latency, harder monitoring and debugging, more places for leakage.
- **When worth it:** the metric is directly tied to money and 0.2 to 0.5% matters; models are diverse (GBM + linear + NN); you have time to maintain it. **Otherwise** a tuned single GBM plus better features beats a fancy stack.

**Example:** 6,000 rows, noisy binary problem, test AUC: XGBoost 0.921, Random Forest 0.938, logistic regression 0.794, stack of all three 0.941. A gain of 0.003 over the best single model.

**Code:**
```python
import numpy as np, xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
X, y = make_classification(6000, 25, n_informative=10, flip_y=0.1, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
xg = xgb.XGBClassifier(n_estimators=300, max_depth=3, learning_rate=0.05, random_state=0)
rf = RandomForestClassifier(300, n_jobs=-1, random_state=0)
lr = LogisticRegression(max_iter=2000)
auc = lambda m: round(roc_auc_score(yte, m.fit(Xtr, ytr).predict_proba(Xte)[:, 1]), 4)
print("xgb", auc(xg), "| rf", auc(rf), "| logreg", auc(lr))
st = StackingClassifier([("xgb", xg), ("rf", rf), ("lr", lr)], final_estimator=LogisticRegression(), cv=5)   # OOF preds feed the meta-model
print("stack", auc(st))
```
Output: xgb 0.9214, rf 0.9375, logreg 0.7938, stack 0.9407.

**Follow-ups:**
- *Why not train the meta-model on training predictions?* Base models have seen those labels, so their predictions are too good and the meta-model over-trusts them.
- *Is a Random Forest an ensemble of ensembles?* No, it is one bagged ensemble; stacking combines different model types.

**Common mistakes:** In-fold predictions for the meta-model. Stacking near-identical GBMs and expecting a jump. Ignoring that production must run every base model, with the same features, every time.

### Q37 ⭐⭐ 🟡 How do you use learning curves and validation curves to diagnose under/overfitting in a boosted model?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** A learning curve (score vs training size) tells me whether more data would help; a validation curve (score vs one hyperparameter) tells me where capacity tips into overfitting; for boosting I also plot validation loss against the number of rounds.

**Then explain:**
- **Reading a learning curve:**
  - Both train and validation scores low and close: **underfitting (high bias)**; more data will not help, add capacity or better features.
  - Train high, validation lower, gap that shrinks as n grows: **overfitting (high variance)**; more data, regularisation, or a smaller model helps.
  - Validation curve still rising at full size: more data would help.
- **Validation curve:** vary `max_depth`, `min_child_weight`, `reg_lambda`, etc. Pick the value where validation peaks; if train keeps rising while validation is flat or falls, you are past the sweet spot.
- **Round curve:** evaluate train and validation loss after each tree. Validation loss minimum is the right number of trees (early stopping, Q11). Use log loss, because AUC can look flat while probabilities get worse.
- **Mind the split:** use the same CV as in tuning (time/group aware when needed).

**Example (synthetic 4,000 rows, XGBoost depth 4):** train AUC 1.000 vs val 0.902 at 266 rows (gap 0.098); at 2,666 rows train 0.994 vs val 0.932 (gap 0.062), so the gap closes slowly and more data would still help. Depth curve: val AUC 0.919 (depth 1), 0.930 (2), 0.932 (4), 0.933 (8), while train goes 0.932 to 1.000, so depth beyond 2 to 4 buys nothing. Round curve (depth 6, lr 0.1): validation log loss is lowest at round 65 (0.302) and worsens to 0.368 by round 400, even though AUC barely moves.

**Code:**
```python
import numpy as np, xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import learning_curve, validation_curve, StratifiedKFold
X, y = make_classification(4000, 20, n_informative=8, flip_y=0.1, random_state=0)
cv = StratifiedKFold(3, shuffle=True, random_state=0)
m = xgb.XGBClassifier(n_estimators=150, max_depth=4, learning_rate=0.1, random_state=0)
sizes, tr, va = learning_curve(m, X, y, cv=cv, scoring="roc_auc", train_sizes=[0.1, 0.3, 0.6, 1.0])
for s, a, b in zip(sizes, tr.mean(1), va.mean(1)): print(f"n={s:5d}  train AUC {a:.3f}  val AUC {b:.3f}  gap {a-b:.3f}")
depths = [1, 2, 4, 8, 12]
tr, va = validation_curve(m, X, y, param_name="max_depth", param_range=depths, cv=cv, scoring="roc_auc")
for k, a, b in zip(depths, tr.mean(1), va.mean(1)): print(f"max_depth={k:2d}  train {a:.3f}  val {b:.3f}")
Xtr, Xva, ytr, yva = X[:3000], X[3000:], y[:3000], y[3000:]            # boosting-round curve from a single fit
r = xgb.XGBClassifier(n_estimators=400, max_depth=6, learning_rate=0.1, eval_metric="logloss", random_state=0
                      ).fit(Xtr, ytr, eval_set=[(Xtr, ytr), (Xva, yva)], verbose=False).evals_result()
v = np.array(r["validation_1"]["logloss"]); print("val logloss min at round", v.argmin()+1, "=", v.min().round(3), "| at round 400 =", v[-1].round(3))
```

**Follow-ups:**
- *Train score is 1.0, is that a problem?* Not by itself for GBMs; look at the validation score and the gap.
- *Flat curves both low?* Add features or interactions, a richer model; check label noise.

**Common mistakes:** Judging by train score. Using AUC alone to detect overfitting in rounds (use log loss). Reading a learning curve from a single noisy split.

### Q38 ⭐⭐ 🔴 Derive the XGBoost objective: second-order Taylor expansion, optimal leaf weight and the split-gain formula.
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
**Say this first (1 line):** XGBoost adds one tree per round by minimising a regularised loss approximated to second order; that gives a closed-form leaf weight `w = -G/(H+λ)` and a split gain that compares the children's `G²/(H+λ)` with the parent's, minus a penalty γ per extra leaf.

**Then explain (derivation, in the order I would write it on a board):**
1. **Objective at round t** (ŷ is the current prediction, f_t the new tree):
   `L = Σ_i l(y_i, ŷ_i + f_t(x_i)) + Ω(f_t)`, with `Ω = γT + ½λ Σ_j w_j²` (T leaves, leaf weights w_j).
2. **Second-order Taylor** around ŷ: `l(y, ŷ+f) ≈ l(y, ŷ) + g f + ½ h f²`, where `g = ∂l/∂ŷ` and `h = ∂²l/∂ŷ²`. Drop the constant `l(y, ŷ)`.
3. **Group by leaf.** If leaf j holds set I_j, define `G_j = Σ_{i∈I_j} g_i`, `H_j = Σ_{i∈I_j} h_i`:
   `L ≈ Σ_j [ G_j w_j + ½ (H_j + λ) w_j² ] + γT`.
4. **Optimal weight:** set derivative to 0: `w_j* = -G_j / (H_j + λ)`.
5. **Optimal objective:** `L* = -½ Σ_j G_j² / (H_j + λ) + γT`. Lower is better, so a "good" leaf has large `G²/(H+λ)`.
6. **Split gain** (parent splits into left L and right R):
   `Gain = ½ [ G_L²/(H_L+λ) + G_R²/(H_R+λ) - (G_L+G_R)²/(H_L+H_R+λ) ] - γ`.
   Split only if Gain > 0. γ is the minimum improvement; λ shrinks weights; `min_child_weight` is a floor on H.
- **g and h for common losses:** squared error `½(y-ŷ)²`: `g = ŷ - y`, `h = 1`. Logistic loss (ŷ = raw score, p = sigmoid): `g = p - y`, `h = p(1-p)`.
- **Why second order:** using the curvature h gives a Newton step (better step size per leaf, regularisation `λ` enters naturally), versus classic GBM's first-order fit of the residual.

**Example (squared loss):** with ŷ = 0, g = -y, h = 1, so `w* = Σy / (n + λ)`: the leaf mean, shrunk toward 0 by λ. With λ = 0 it is exactly the leaf average of the residuals, which is plain gradient boosting.

**Code (numeric check of the closed form against brute force):**
```python
import numpy as np
rng = np.random.default_rng(0); y = rng.normal(5, 1, 8); pred = np.zeros(8)
g, h = pred - y, np.ones(8); lam = 1.0                      # squared loss: g = pred - y, h = 1
w = -g.sum() / (h.sum() + lam); obj = -0.5 * g.sum()**2 / (h.sum() + lam)
ws = np.linspace(0, 6, 60001); f = g.sum()*ws + 0.5*(h.sum() + lam)*ws**2   # one-leaf objective over a grid of weights
print("closed form w* =", round(w, 4), "| brute force w* =", round(ws[f.argmin()], 4), "| obj", round(obj, 4), round(f.min(), 4))
```
Output: both give `w* = 4.7573`, objective `-101.8448`.

**Follow-ups:**
- *How is the tree structure found?* Greedily: for each node, try candidate splits and pick the one with the highest Gain; for a fixed structure the leaf weights are optimal in closed form.
- *What does λ = 0, γ = 0 reduce to?* Splits that maximise the usual variance reduction in the gradient.
- *Why must h be positive?* Otherwise the quadratic is not convex and `H+λ` could be zero or negative; custom objectives clip h (Q50).

**Common mistakes:** Forgetting the ½ factors or the sign (`w = -G/(H+λ)`). Saying XGBoost "fits the residual"; it fits a Newton step using g and h. Mixing up γ (per-leaf penalty) with λ (L2 on weights).

### Q39 ⭐⭐ 🔴 Code: implement gradient boosting regression from scratch (squared loss) using shallow trees.
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior live coding)
**Say this first (1 line):** Start from the mean, then repeat: compute residuals (the negative gradient of squared loss), fit a shallow tree to them, and add it to the model with a small learning rate.

**Then explain:**
- **Initial model:** `F0 = mean(y)`, the best constant for squared loss.
- **Each round:** `r = y - F` (equals the negative gradient of `½(y-F)²`), fit a depth-3 tree to `r`, update `F += lr * tree(x)`.
- **Prediction:** `F0 + lr * sum of trees`.
- **Knobs:** `n_trees`, `lr` (smaller = needs more trees, generalises better, Q19), tree depth (interaction order, Q44).
- For other losses, replace `r` with the negative gradient (and optionally re-fit leaf values); this is the "gradient" in gradient boosting (Q7).

**Example:** target `sin(x0) + 0.5*x1² + noise`, 1,000 train and 500 test rows. My model: test RMSE 0.227; sklearn `GradientBoostingRegressor` with the same settings: 0.227; predicting the mean: 1.591.

**Code:**
```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
class MyGBR:
    def __init__(self, n_trees=200, lr=0.1, max_depth=3):
        self.n, self.lr, self.d = n_trees, lr, max_depth
    def fit(self, X, y):
        self.f0 = y.mean(); F = np.full(len(y), self.f0); self.trees = []
        for _ in range(self.n):
            r = y - F                                   # negative gradient of 1/2 (y-F)^2
            t = DecisionTreeRegressor(max_depth=self.d).fit(X, r)
            F += self.lr * t.predict(X); self.trees.append(t)
        return self
    def predict(self, X):
        return self.f0 + self.lr * sum(t.predict(X) for t in self.trees)
rng = np.random.default_rng(0)
X = rng.uniform(-3, 3, (1500, 3)); y = np.sin(X[:, 0]) + 0.5*X[:, 1]**2 + rng.normal(0, 0.2, 1500)
m = MyGBR().fit(X[:1000], y[:1000])
rmse = lambda p: np.sqrt(((p - y[1000:])**2).mean())
print("mine    test RMSE", round(rmse(m.predict(X[1000:])), 3))
print("sklearn test RMSE", round(rmse(GradientBoostingRegressor(n_estimators=200, max_depth=3, learning_rate=0.1, random_state=0).fit(X[:1000], y[:1000]).predict(X[1000:])), 3))
print("mean-only baseline", round(rmse(np.full(500, y[:1000].mean())), 3))
```

**Follow-ups:**
- *Add early stopping?* Track validation RMSE each round; keep the best round count.
- *Add subsampling?* Fit each tree on a random 50 to 80% of rows (stochastic gradient boosting).
- *Classification?* Use log-loss: `r = y - p` with `p = sigmoid(F)`, and Newton-step leaf values `sum(r)/sum(p(1-p))`.

**Common mistakes:** Fitting trees to `y` instead of the residual. Forgetting the learning rate in `predict`. Deep trees (they overfit the residuals quickly). Starting from 0 rather than the mean.

### Q40 ⭐⭐ 🔴 How does CatBoost avoid target leakage (ordered target statistics, ordered boosting)?
**Asked at:** Product cos, GCCs, analytics/consulting firms, Europe product cos
**Say this first (1 line):** CatBoost encodes each categorical value using only the rows that come before it in a random permutation (ordered target statistics), and computes each row's boosting residual from a model that has not seen that row (ordered boosting), so a row's label never leaks into its own feature or its own gradient.

**Then explain:**
- **The leak in plain target encoding:** if the encoding of row i uses the mean of y over all rows of its category, that mean includes y_i. For rare categories the feature almost equals the label. The model learns "this feature predicts the label" on train and fails on test (target leakage).
- **Ordered target statistics:** shuffle the rows. For row i, encode its category as `(sum of y over earlier rows in the same category + a*prior) / (count of earlier rows + a)`. The row's own label is never used. Several permutations are used to reduce the variance of early rows (which have little history).
- **Prediction shift in boosting:** in standard boosting, the gradient for row i comes from a model trained on row i itself, so training residuals are biased (smaller than they would be on new data). This is a second, subtler leakage.
- **Ordered boosting:** conceptually, keep models M_i trained only on rows before i; use M_{i-1} to compute row i's residual. CatBoost approximates it with permutations and cheap supporting models. Combined with symmetric (oblivious) trees it also acts as a regulariser.
- Also builds **categorical feature combinations** greedily and is strong on small to medium data with many categories.

**Example:** 4,000 rows, a 1,500-level category with no signal (true AUC 0.5). Naive in-fold target encoding + GBM: train AUC 0.883, test AUC 0.501 (pure memorisation of the leak). CatBoost with `cat_features`: train AUC 0.628, test AUC 0.499. The test score is honest in both; CatBoost simply does not fabricate a signal.

**Code:**
```python
import numpy as np, pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
rng = np.random.default_rng(0)
n = 4000
df = pd.DataFrame({"id_like": rng.integers(0, 1500, n).astype(str)})      # high-card category with NO real signal
y = rng.integers(0, 2, n)
tr, te = train_test_split(np.arange(n), random_state=0)
# naive target encoding (mean of y per category, computed on train incl. own row) = leakage
naive = pd.Series(y[tr]).groupby(df.id_like.iloc[tr].values).transform("mean")
te_naive = df.id_like.iloc[te].map(pd.Series(y[tr]).groupby(df.id_like.iloc[tr].values).mean()).fillna(y[tr].mean())
g = GradientBoostingClassifier(random_state=0).fit(naive.values[:, None], y[tr])
print("naive TE   train AUC", round(roc_auc_score(y[tr], g.predict_proba(naive.values[:, None])[:, 1]), 3),
      "| test AUC", round(roc_auc_score(y[te], g.predict_proba(te_naive.values[:, None])[:, 1]), 3), "(truth: 0.5)")
cb = CatBoostClassifier(iterations=200, verbose=0, random_seed=0, thread_count=2).fit(df.iloc[tr], y[tr], cat_features=["id_like"])
print("CatBoost   train AUC", round(roc_auc_score(y[tr], cb.predict_proba(df.iloc[tr])[:, 1]), 3),
      "| test AUC", round(roc_auc_score(y[te], cb.predict_proba(df.iloc[te])[:, 1]), 3))
```
(About 2.5 minutes on my machine, mostly CatBoost import and fit; machine-specific.)

**Follow-ups:**
- *Cost of ordered boosting?* Slower, so `boosting_type="Ordered"` is mainly worth it on small data; on large data the plain mode is used (check the docs for the default in your version).
- *How is it different from K-fold target encoding?* K-fold removes the row's fold; ordered stats uses only earlier rows, a single consistent permutation scheme that is also used inside boosting.

**Common mistakes:** Believing CatBoost makes any category useful (it does not create signal). Mixing CatBoost's internal encoding with your own target encoding. Not passing `cat_features`.

### Q41 ⭐⭐ 🔴 What are the limitations of SHAP with correlated features? Explain path-dependent vs interventional TreeSHAP.
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
**Say this first (1 line):** With correlated features, SHAP splits credit between them in a way that depends on which one the model happened to use, and the "remove a feature" step either follows the tree paths (path-dependent TreeSHAP) or plugs in values from a background set that can create unrealistic rows (interventional TreeSHAP); so I treat attributions as "how the model behaves", not causal truth.

**Then explain:**
- **The core problem:** SHAP asks "what is the prediction if feature j is unknown?". For correlated features there is more than one way to answer, and each answer gives different numbers.
- **Path-dependent TreeSHAP (default, no data needed):** when a split uses a missing feature, follow both branches weighted by the training row counts (cover) in each. Fast. It reflects the correlations seen in training only through how the trees were built, so it is "true to the model's structure" but credit can leak to features the model barely uses.
- **Interventional TreeSHAP (needs a background dataset):** replace the missing features by values drawn from the background, breaking their correlation with the known ones. It matches the causal-style "intervene on the input" view of the model and an unused feature gets exactly zero; but it evaluates the model on **off-distribution points** (high income with tiny spend) where the model has no data, and it costs more.
- **Practical consequences:**
  - Credit for a pair of near-duplicates is shared **arbitrarily**; it changes with seed, `colsample`, or tuning.
  - Each feature can look unimportant while the pair is important.
  - Remedies: group correlated features (sum their SHAP), drop redundant ones, report importance by feature group, and check stability across seeds.
- Cannot be "fixed" by choosing a method; it is a property of the question.

**Example:** `x2 = x1 + small noise`; the truth is `y = 3*x1` only. XGBoost with `colsample_bynode=0.5`, three seeds, mean |SHAP| for [x1, x2]: path-dependent [1.53, 0.91], [1.10, 1.34], [1.95, 0.51]; interventional [1.95, 0.51], [1.70, 0.75], [2.24, 0.22]. The same data and same truth give different credit to x2 for each seed. Off-manifold check: the model predicts 5.28 for the impossible row (x1=2, x2=-2) against 6.17 for (2, 2), so interventional SHAP has to evaluate the model in places with no data.

**Code:**
```python
import numpy as np, pandas as pd, shap, xgboost as xgb
rng = np.random.default_rng(0)
n = 3000
x1 = rng.normal(size=n); x2 = x1 + 0.1*rng.normal(size=n)      # near-duplicate features
X = pd.DataFrame({"x1": x1, "x2": x2})
y = 3*x1 + 0.2*rng.normal(size=n)                               # truth depends on x1 only
bg = X.sample(200, random_state=0)
for seed in (0, 1, 2):
    m = xgb.XGBRegressor(n_estimators=200, max_depth=3, colsample_bynode=0.5, random_state=seed).fit(X, y)
    pp = shap.TreeExplainer(m)(X[:500]).values                  # path-dependent (default)
    iv = shap.TreeExplainer(m, data=bg, feature_perturbation="interventional")(X[:500]).values
    print(f"seed {seed}  mean|SHAP| [x1, x2]  path-dep {np.abs(pp).mean(0).round(2)}  interventional {np.abs(iv).mean(0).round(2)}")
Xo = pd.DataFrame({"x1": [2.0], "x2": [-2.0]})                  # impossible combination in the data
print("off-manifold prediction for (x1=2, x2=-2):", m.predict(Xo).round(2), "| on-manifold (2, 2):", m.predict(pd.DataFrame({"x1": [2.0], "x2": [2.0]})).round(2))
```
(The last line uses the seed-2 model.)

**Follow-ups:**
- *Which one do you use?* Interventional when you want "what does the model do if I change this input" and have a good background; path-dependent for speed or when off-manifold points worry you. State the choice.
- *Alternative?* Conditional/on-manifold SHAP variants, or grouping features.
- *Does PDP have the same issue?* Yes, partial dependence also averages over unrealistic combinations; ALE plots are designed to avoid it.

**Common mistakes:** Presenting SHAP shares of correlated features as causal importance. Comparing runs without checking seed stability. Using a tiny or unrepresentative background set for interventional SHAP.

### Q42 ⭐⭐ 🔴 Derive the variance of an average of correlated trees; why does reducing correlation between trees matter?
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior/quant-leaning)
**Say this first (1 line):** For B trees, each with variance σ² and pairwise correlation ρ, the variance of the average is `ρσ² + (1-ρ)σ²/B`; adding trees kills only the second term, so the floor ρσ² is set by how correlated the trees are, which is why Random Forest decorrelates them with feature subsampling.

**Then explain (derivation):**
- Let the tree predictions be X_1…X_B, each `Var(X_i) = σ²`, `Corr(X_i, X_j) = ρ`, so `Cov(X_i, X_j) = ρσ²`.
- `Var( (1/B) Σ X_i ) = (1/B²) [ Σ Var(X_i) + Σ_{i≠j} Cov(X_i, X_j) ] = (1/B²) [ Bσ² + B(B-1)ρσ² ]`
- `= σ²/B + ((B-1)/B) ρσ² = ρσ² + (1-ρ) σ²/B`.
- **Cases:** ρ = 0: variance `σ²/B` (goes to 0 as B grows). ρ = 1: stays σ² (averaging does nothing). As B goes to infinity: variance goes to `ρσ²`, so **more trees cannot beat the correlation floor**.
- **Why trees are correlated:** bootstrap samples of the same data overlap heavily, and one strong feature gets chosen at the top of every tree. So ρ is high for plain bagging.
- **What RF does:** at each split only `max_features` randomly chosen features are allowed, so the trees look different (ρ falls). The cost is that each tree is slightly weaker (a bit more bias and higher σ²); the net effect is usually a win. This is the trade-off behind tuning `max_features` (Q3).
- (The variance formula treats the bias as unchanged: averaging does not change the bias of the individual trees.)

**Example:** B = 100, σ² = 1. ρ = 0.8 gives `0.8 + 0.2/100 = 0.802`; ρ = 0.3 gives `0.307`; ρ = 0 gives `0.01`. Going from 100 to 1,000 trees at ρ = 0.8 moves variance from 0.802 to only 0.8002.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
B, sigma2, trials = 100, 1.0, 20000
for rho in [0.0, 0.3, 0.8]:
    shared = rng.normal(size=(trials, 1)); own = rng.normal(size=(trials, B))
    P = np.sqrt(rho)*shared + np.sqrt(1-rho)*own            # each var 1, pairwise corr rho
    print(f"rho={rho}: simulated {P.mean(1).var():.3f}  theory {rho*sigma2 + (1-rho)*sigma2/B:.3f}")
```
Output: ρ=0.0 simulated 0.010, theory 0.010; ρ=0.3: 0.305 vs 0.307; ρ=0.8: 0.801 vs 0.802.

**Follow-ups:**
- *Why not just use a tiny `max_features`?* ρ drops but each tree gets weaker and misses informative features; tune it.
- *Does boosting use this logic?* No. Boosting reduces bias sequentially; variance control comes from the learning rate, subsampling and regularisation.
- *Is bagging helpful for low-variance models?* Little; it helps unstable, high-variance models like deep trees.

**Common mistakes:** Saying "more trees means zero variance" (the floor is ρσ²). Forgetting that bootstrap trees are correlated. Claiming feature subsampling reduces each tree's own variance (it reduces correlation, at some cost in tree strength).

### Q43 ⭐ 🟡 How are multi-class problems handled in XGBoost/LightGBM (softmax objective, one tree per class)?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** For K classes the model keeps K separate raw scores, builds K trees per boosting round (one per class), converts the K scores to probabilities with softmax, and uses the softmax cross-entropy loss for the gradients.

**Then explain:**
- **Objective:** XGBoost `multi:softprob` (probabilities) or `multi:softmax` (class label); LightGBM `multiclass`. Set `num_class=K` (the sklearn wrappers infer it).
- **Per round:** compute `p = softmax(F)` where `F` is the K raw scores. For class k the gradient is `g_k = p_k - y_k` (y_k is 1 for the true class, else 0) and the hessian is about `p_k(1-p_k)` (XGBoost uses a scaled version of this). Grow one tree on each class's (g, h), add to that class's score.
- **Size:** `n_estimators * K` trees in total, so training time and model size scale with K.
- **Alternatives:** one-vs-rest (`multiclassova` in LightGBM, or `OneVsRestClassifier`) trains K independent binary models; probabilities do not sum to 1 unless renormalised.
- **Imbalance and metrics:** use `mlogloss`, macro-F1, per-class recall; class weights if a class is rare.
- **Early stopping** works on `mlogloss`.

**Example:** 3 classes, 20 rounds, depth 3: the fitted XGBoost model contains 60 trees. For one test row the raw scores pass through softmax to give `[0.7238, 0.1028, 0.1734]`, exactly equal to `predict_proba`. Accuracy on the held-out set was 0.816.

**Code:**
```python
import numpy as np, xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
X, y = make_classification(1500, 10, n_informative=6, n_classes=3, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
m = xgb.XGBClassifier(n_estimators=20, max_depth=3, random_state=0).fit(Xtr, ytr)   # multi:softprob
print("classes:", m.n_classes_, "| trees in model:", len(m.get_booster().get_dump()), "(20 rounds x 3 classes)")
raw = m.predict(Xte[:1], output_margin=True)[0]
e = np.exp(raw - raw.max())
print("softmax(raw) =", (e/e.sum()).round(4), "| predict_proba =", m.predict_proba(Xte[:1])[0].round(4))
print("accuracy", round(m.score(Xte, yte), 3))
```

**Follow-ups:**
- *Why not a single tree with K outputs?* Standard XGBoost/LightGBM use one scalar-output tree per class. Vector-leaf (multi-output) trees exist as an option in newer XGBoost.
- *1,000 classes?* Training cost explodes (1,000 trees per round); use embeddings, hierarchical classification or a neural net.

**Common mistakes:** Forgetting `num_class` with the native API. Evaluating a 3-class model with binary AUC. Not realising model size and training time scale with K.

### Q44 ⭐ 🟡 What does tree depth mean for feature interactions? How do you detect interactions in a GBM?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** A tree of depth d can combine at most d features along one path, so `max_depth` caps the interaction order the model can learn: depth 1 (stumps) is a purely additive model, depth 2 captures pairwise interactions, and so on; I detect interactions with SHAP interaction values, H-statistic, or by comparing depth-1 vs depth-2 models.
 
**Then explain:**
- **Depth and interactions:** a split on x0 then x1 inside one path means the effect of x1 depends on x0. Stumps cannot do this, so boosted stumps give a GAM-like additive model.
- **Practical rule:** most tabular problems need depth 3 to 8; if depth 1 or 2 performs as well as deeper, interactions are weak, and a simpler/explainable model may do.
- **Detection methods:**
  - **Depth ablation:** train with `max_depth=1` vs `2` vs deeper; a large jump means interactions.
  - **SHAP interaction values** (`TreeExplainer.shap_interaction_values`): a matrix per row; off-diagonal entries are pairwise interaction effects. Cost grows as O(features squared).
  - **Friedman's H-statistic** (via partial dependence): share of the joint effect not explained by the individual effects; expensive.
  - **Dependence plot coloured by another feature**: vertical spread that follows the colour signals an interaction.
  - XGBoost feature interaction tools (`xgbfir`) count co-occurrence along paths.
- **Controlling interactions:** XGBoost `interaction_constraints` limits which features may appear together (also helps explainability).

**Example:** `y = x0*x1 + x2 + noise` (x0*x1 is a pure interaction). Depth-1 boosting: test R2 0.435 (it only learns x2). Depth-2: test R2 0.816. SHAP interaction mean |value| for the (x0, x1) pair is 0.31 against 0.02 or less for all other pairs.

**Code:**
```python
import numpy as np, xgboost as xgb, shap
rng = np.random.default_rng(0)
X = rng.normal(size=(4000, 4)); y = X[:, 0]*X[:, 1] + X[:, 2] + 0.1*rng.normal(size=4000)   # x0*x1 is a pure interaction
for d in [1, 2]:
    m = xgb.XGBRegressor(n_estimators=200, max_depth=d, learning_rate=0.1, random_state=0).fit(X[:3000], y[:3000])
    print(f"max_depth={d}  test R2 = {m.score(X[3000:], y[3000:]):.3f}")
m = xgb.XGBRegressor(n_estimators=200, max_depth=3, random_state=0).fit(X, y)
inter = shap.TreeExplainer(m).shap_interaction_values(X[:500])
off = np.abs(inter).mean(0); np.fill_diagonal(off, 0)
print("mean |SHAP interaction| (off-diagonal):"); print(off.round(3))
```
Output: R2 0.435 (depth 1), 0.816 (depth 2); pair (0,1) 0.31, all other off-diagonal values at most 0.02.

**Follow-ups:**
- *Does leaf-wise growth change this?* Interaction order is limited by the depth of the path, so cap `max_depth` in LightGBM too.
- *Deeper always better?* No, deeper trees fit noise; tune depth with `min_child_weight` and regularisation.

**Common mistakes:** Thinking boosting with stumps captures interactions. Reading a feature's SHAP value as independent of other features. Setting a huge depth "to catch interactions" and overfitting.

### Q45 ⭐ 🟡 What are DART, row subsampling and column subsampling in boosting and why use them?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** Row subsampling and column subsampling train each tree on a random part of the data or features to decorrelate trees and reduce overfitting; DART goes further by randomly dropping some earlier trees when fitting each new one, so later trees cannot just fix the first few trees' leftovers.

**Then explain:**
- **Row subsampling (`subsample`, LightGBM `bagging_fraction` + `bagging_freq`):** each tree sees a random 50 to 90% of rows (stochastic gradient boosting). Less overfitting, faster, small noise added.
- **Column subsampling (`colsample_bytree`, `colsample_bylevel`, `colsample_bynode`; LightGBM `feature_fraction`):** each tree/level/split sees a random subset of features, like Random Forest. Helps with correlated features and speed.
- **DART (`booster="dart"`):** in each round, a random fraction (`rate_drop`) of existing trees is dropped, the new tree is fit to the residual of the remaining ones, then weights are rescaled (`normalize_type`). Inspired by dropout in neural nets.
  - Why: in plain boosting the first trees dominate and later trees make tiny corrections ("over-specialisation").
  - Cost: slower training (needs recomputing predictions with dropped trees), early stopping is less clean, more hyperparameters; predictions need all trees.
- **When to use:** subsampling is nearly always worth trying (0.6 to 0.9). DART is worth a trial when the model overfits despite tuning, or when you suspect over-specialised early trees; do not expect it to always win.

**Example:** 4,000 rows, 25 features, XGBoost depth 5, lr 0.2, 200 trees, test AUC: plain 0.9214, subsample 0.7 + colsample 0.6: 0.9235, DART on top: 0.9246. Differences are small and from one split; the interview point is to know the mechanism and to validate on your data.

**Code:**
```python
import numpy as np, xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
X, y = make_classification(4000, 25, n_informative=8, flip_y=0.1, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
for name, kw in [("plain", {}), ("subsample+colsample", dict(subsample=0.7, colsample_bytree=0.6)),
                 ("dart", dict(booster="dart", rate_drop=0.1, skip_drop=0.5, subsample=0.7, colsample_bytree=0.6))]:
    m = xgb.XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.2, random_state=0, **kw).fit(Xtr, ytr)
    print(f"{name:20s} test AUC {roc_auc_score(yte, m.predict_proba(Xte)[:, 1]):.4f}")
```

**Follow-ups:**
- *Does subsampling make results random?* Yes, so fix the seed (Q46).
- *`bagging_freq=0` in LightGBM?* Then `bagging_fraction` is ignored; set `bagging_freq` to 1 to bag every iteration.

**Common mistakes:** Setting `bagging_fraction` in LightGBM without `bagging_freq`. Very small `colsample` when only a few features matter. Using DART with early stopping as if it behaved like gbtree.

### Q46 ⭐ 🟡 Why can Random Forest / XGBoost results differ between runs, and how do you make training reproducible?
**Asked at:** Product cos, GCCs, analytics/consulting firms
**Say this first (1 line):** Results differ because training uses randomness (bootstrap rows, feature subsets, subsampling) and sometimes non-deterministic parallel arithmetic; I fix every seed, pin library versions and data order, turn on the deterministic flags, and save the trained model rather than expecting a re-train to match bit for bit.

**Then explain:**
- **Sources of randomness:**
  - Bootstrap and feature subsampling (Random Forest `random_state`, XGBoost `subsample`/`colsample_*`, LightGBM `bagging_*`, `feature_fraction`).
  - Tie-breaking between equal-gain splits.
  - **Parallelism:** floating-point addition order changes with thread count, giving tiny differences that can flip a split; GPU atomics add more.
  - Data order (shuffled input), a different CV split, library or version changes.
- **How to control it:**
  - Set the seed everywhere (`random_state`, `seed`, numpy seed, CV splitters).
  - LightGBM: `deterministic=True`, `force_row_wise=True` (or `force_col_wise`), fixed `seed`, same `num_threads`.
  - XGBoost: fixed `random_state` and `n_jobs`; the CPU `hist` method is generally reproducible with the same thread count; GPU runs may not be bit-exact.
  - Pin package versions (`requirements.txt`/lockfile), pin data snapshots, log params.
  - Persist the model file; for decisions, reproducibility of the artifact matters more than of retraining.
- **Evaluate with several seeds:** report mean and std, to see if a +0.002 AUC gain is real or noise.

**Example (my run, 2,000 rows):** Random Forest seed 0 twice gives identical probabilities `[0.94 1. 0.]`; seed 1 gives `[0.96 0.98 0.]`. XGBoost with subsampling, seed 0 twice: identical `[0.9993 0.9984 0.0085]`; seed 1: `[0.9961 0.9991 0.001]`. LightGBM with `deterministic=True`: identical twice.

**Code:**
```python
import numpy as np, xgboost as xgb, lightgbm as lgb
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
X, y = make_classification(2000, 20, random_state=0)
p = lambda s: RandomForestClassifier(50, random_state=s).fit(X, y).predict_proba(X[:3])[:, 1].round(3)
print("RF seed 0:", p(0), "| seed 0 again:", p(0), "| seed 1:", p(1))
q = lambda s: xgb.XGBClassifier(n_estimators=50, subsample=0.7, colsample_bytree=0.7, random_state=s, n_jobs=1).fit(X, y).predict_proba(X[:3])[:, 1].round(4)
print("XGB seed 0:", q(0), "| seed 0 again:", q(0), "| seed 1:", q(1))
l = lambda: lgb.LGBMClassifier(n_estimators=50, subsample=0.7, subsample_freq=1, random_state=0, deterministic=True, force_row_wise=True, n_jobs=1, verbose=-1).fit(X, y).predict_proba(X[:3])[:, 1].round(4)
print("LGBM deterministic:", l(), l())
```

**Follow-ups:**
- *Identical seed but different results on another machine?* Different CPU/thread count, library version, or BLAS build.
- *Should the production model be retrained to the same result?* Better: version the data, code and model; retrain with tolerance checks rather than exact equality.

**Common mistakes:** Seeding only numpy. Comparing two models with one seed. Changing `n_jobs` and expecting identical results. Forgetting that CV splits also need seeds.

### Q47 ⭐ 🔴 Explain LightGBM's GOSS, EFB and histogram-based splitting.
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
**Say this first (1 line):** LightGBM speeds up training three ways: histograms (bin each feature into at most about 255 buckets so split search scans buckets, not rows), GOSS (train each tree on all large-gradient rows plus a sample of small-gradient rows), and EFB (merge sparse features that are never non-zero together into one column).

**Then explain:**
- **Histogram-based splitting:**
  - Bin each feature once (default `max_bin=255`). For a node, build a histogram of the sum of gradients and hessians per bin, one pass over its rows: O(rows x features). Then find the best split by scanning bins: O(bins x features), not O(rows).
  - **Histogram subtraction:** build the histogram only for the smaller child; the sibling = parent minus child. Roughly halves the work.
  - Less memory (bins stored as small ints) and better cache use; slight approximation of exact thresholds.
- **GOSS (Gradient-based One-Side Sampling):**
  - Rows with large |gradient| are the ones the model gets wrong, so they carry most of the information.
  - Keep the top `a` fraction by |gradient|; randomly sample a fraction `b` of the rest; multiply the sampled small-gradient rows' weights by `(1-a)/b` so the gradient sum stays unbiased. Fewer rows per tree gives speed with little accuracy loss. (Enabled with `data_sample_strategy="goss"` in LightGBM 4.)
- **EFB (Exclusive Feature Bundling):**
  - In sparse data (one-hot columns, TF-IDF), many features are rarely non-zero at the same time ("mutually exclusive").
  - Bundle them into one feature by offsetting their bin values so they occupy different ranges; the histogram has the same information with far fewer columns. Finding the best bundles is a graph-colouring problem solved greedily (allowing a small conflict rate).
- **Net result:** training cost goes from O(rows x features) per tree toward O(sampled rows x bundles). This is why LightGBM is typically faster than classic exact-split GBMs, though XGBoost `hist` closes much of the gap (Q10, Q48).

**Example:** 1M rows, 500 one-hot columns made from 5 categorical fields. EFB can bundle the columns of each field into one, going from 500 to about 5 histogram columns; GOSS with a=0.2, b=0.1 processes 30% of rows per tree (all 20% high-gradient + 10% sampled), weighting the sampled ones by 0.8/0.1 = 8.

**Follow-ups:**
- *Does histogram binning hurt accuracy?* Rarely; 255 bins is usually enough. Increase `max_bin` for features needing fine thresholds.
- *Why does GOSS not bias the gradient sum?* The re-weighting factor compensates for under-sampling the small-gradient rows.
- *Is GOSS always used?* No; the default is plain GBDT, and GOSS is not combined with row bagging.

**Common mistakes:** Saying histograms make splits "exact but faster" (they are approximate). Forgetting the `(1-a)/b` re-weighting in GOSS. Thinking EFB changes the model's features (it only compresses the representation).

### Q48 ⭐ 🔴 How does XGBoost find splits: exact vs approximate vs hist; what is sparsity-aware split finding?
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
**Say this first (1 line):** XGBoost can enumerate every threshold (exact), propose candidate thresholds from a weighted quantile sketch (approx), or bin features into histograms (hist, the modern default); in all of them, sparsity-aware split finding learns a default direction for missing values at every split.

**Then explain:**
- **Exact greedy (`tree_method="exact"`):** sort each feature (pre-sorted once), scan all distinct values and compute the gain from running sums of G and H. Most precise, but slow and memory-heavy for big data, single machine only.
- **Approximate (`approx`):** build candidate split points from **weighted quantiles**, where each row is weighted by its hessian h_i (the loss curvature, so rows that matter more get finer resolution). Candidates are proposed once globally or re-proposed per node (local); the sketch is mergeable, so it works in distributed settings. Candidate count is about 1/ε.
- **Histogram (`hist`):** bin each feature once into up to `max_bin=256` buckets, accumulate G/H per bucket, scan buckets; uses the subtraction trick (sibling = parent - child) like LightGBM (Q47). Fast, supports GPU (`device="cuda"`), and is the default `tree_method` in current XGBoost versions.
- **Sparsity-aware splitting:**
  - Missing values (and zeros in sparse input) are handled by learning a **default direction** per split.
  - For a candidate split, compute the gain twice using only the non-missing rows: once sending missing rows left and once right; keep the better direction.
  - Cost is linear in the number of non-missing entries, so sparse data (one-hot, TF-IDF) is cheap. At inference, a missing value follows the learned direction. This is also why XGBoost needs no imputation (Q14).
- **Which to use:** `hist` for almost everything; `exact` for small data when you need exact thresholds; `approx` mainly historical or in some distributed setups.

**Example:** a feature has 1M values but only 10,000 are non-missing. Sparsity-aware split finding scans 10,000 entries, and tries missing->left and missing->right once. If customers with missing "last purchase date" are mostly churners, the learned direction sends them to the high-risk branch with no imputation.

**Follow-ups:**
- *Why weight the quantile sketch by hessian?* The objective is a weighted squared error where h_i is the weight, so equal-weight quantiles would be miscalibrated for classification.
- *What happens if missing never occurred in training for a feature?* In that case missing values are sent to the default (left) direction at prediction time.
- *Do exact and hist give the same model?* Not exactly; hist thresholds are bin edges, so tiny differences appear.

**Common mistakes:** Imputing missing values blindly and losing the "missingness is informative" signal. Using `exact` on millions of rows. Believing the default direction is chosen randomly (it is chosen by gain).

### Q49 ⭐ 🔴 What are monotonic constraints in GBMs and when would you use them (e.g. credit scoring, pricing)?
**Asked at:** Product cos, GCCs, analytics/consulting firms, fintech/regulated
**Say this first (1 line):** A monotonic constraint forces the model's output to only go up (or only go down) as a chosen feature increases, so it matches business logic, stops noise-driven wiggles, and is often required for credit scoring and pricing.

**Then explain:**
- **What it does:** in XGBoost `monotone_constraints=(1, 0, -1)` (increasing, none, decreasing per feature); LightGBM `monotone_constraints=[1, 0, -1]`. During training, a split on that feature is only allowed if the left child's value is not above the right child's (for increasing), and leaf values are bounded so the property holds across the whole tree ensemble.
- **When to use:**
  - **Credit:** more missed payments must never reduce risk; higher income should not raise it.
  - **Pricing / demand:** price up should not raise demand (if it does in data, it is probably confounded).
  - Any regulated or explainable setting where a stakeholder says "that curve makes no sense".
- **Benefits:** explainability, regulator acceptance, robustness to noise and to sparse regions where the unconstrained model would zig-zag, and often equal or slightly better test accuracy when the truth really is monotone.
- **Costs / caveats:** if the true relationship is not monotone you lose accuracy; constraints apply per feature, ceteris paribus (other features fixed), not to feature combinations; they do not fix biased data; pair with SHAP dependence plots to verify.
- Related: `interaction_constraints` restrict which features may interact.

**Example:** `y = 2*log(1+x0) + 0.3*x1 + big noise`; x0's true effect is increasing. Over 400 grid points the free model's prediction decreases at 98 steps (zig-zag), the constrained one at 0. Test R2: free 0.289, monotone 0.317 (so the constraint helped slightly here).

**Code:**
```python
import numpy as np, xgboost as xgb
rng = np.random.default_rng(0)
def make(n):
    X = rng.uniform(0, 10, (n, 2))                                   # x0 = e.g. income (more is never worse), x1 = other
    y = 2*np.log1p(X[:, 0]) + 0.3*X[:, 1] + rng.normal(0, 1.5, n)    # true effect of x0 is increasing; noise is large
    return X, y
X, y = make(1500); Xt, yt = make(5000)
grid = np.c_[np.linspace(0, 10, 400), np.full(400, 5.0)]
free = xgb.XGBRegressor(n_estimators=300, max_depth=4, random_state=0).fit(X, y)
mono = xgb.XGBRegressor(n_estimators=300, max_depth=4, random_state=0, monotone_constraints=(1, 0)).fit(X, y)
drops = lambda m: int((np.diff(m.predict(grid)) < -1e-9).sum())
print("grid steps where prediction DEcreases | free:", drops(free), "| monotone:", drops(mono))
print("test R2 | free:", round(free.score(Xt, yt), 3), "| monotone:", round(mono.score(Xt, yt), 3))
```

**Follow-ups:**
- *How do you decide which features to constrain?* Domain knowledge; then compare validation score with and without. A big drop means the assumption is wrong or the data has confounding.
- *Does it guarantee monotonic behaviour in production?* For the constrained feature with others fixed, yes; check at serving with test cases.
- *Alternatives?* Scorecards with WoE binning, GAMs with monotone splines.

**Common mistakes:** Constraining features that are truly non-monotone (like age for risk). Assuming constraints remove proxy bias. Forgetting that the sign convention is per feature and per model API.

### Q50 ⭐ 🔴 How do you write a custom objective in XGBoost/LightGBM (gradient and hessian)? Example: focal or asymmetric loss.
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
**Say this first (1 line):** A custom objective is just a function that takes the current raw predictions and labels and returns the first derivative (gradient) and second derivative (hessian) of your loss with respect to the raw score; the booster does everything else.

**Then explain:**
- **Interface:** XGBoost `xgb.train(..., obj=fn)` where `fn(preds, dtrain) -> (grad, hess)`; or sklearn API `XGBClassifier(objective=fn)` with `fn(y_true, y_pred)`. LightGBM: `objective=fn(y_true, y_pred) -> (grad, hess)`.
- **Raw scores:** `preds` are log-odds (margin), not probabilities, with a custom binary objective; apply the sigmoid yourself for probabilities. Set `base_score` sensibly (0 for log-odds) or the starting point is off.
- **Gradient/hessian examples:** squared error `g = pred - y, h = 1`; logistic `g = p - y, h = p(1-p)`.
- **Hessian rules:** must be positive (clip at a small epsilon); if the loss is not convex (focal loss can have negative curvature) clip or use a constant hessian.
- **When useful:** class imbalance with focal loss, asymmetric costs (under-predicting demand costs more than over-predicting), ranking or business-specific losses.
- **Check it:** compare analytic derivatives with numerical ones, test on a standard loss first (reproduces the built-in), and monitor a proper custom metric (`custom_metric`/`feval`), since the built-in eval metric is not tied to your loss.

**Example (focal loss):** `FL = -alpha_t (1 - p_t)^gamma log(p_t)` down-weights easy examples. On a 95/5 imbalanced set, my custom focal objective gives test AUC 0.8693 against 0.8722 for built-in logistic loss: no gain here, which is typical; focal loss is worth trying, not a guarantee. The point is that the plumbing works.

**Code:** (numeric derivatives of the loss keep the code short; replace them with analytic ones for speed)
```python
import numpy as np, xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
def make_obj(alpha=0.25, gamma=2.0):
    def focal(preds, dtrain):                                 # preds are raw scores (log-odds)
        y = dtrain.get_label(); eps = 1e-9
        def L(z):
            p = 1/(1+np.exp(-z)); pt = np.where(y == 1, p, 1-p); a = np.where(y == 1, alpha, 1-alpha)
            return -a*(1-pt)**gamma*np.log(pt+eps)
        h = 1e-4                                              # numeric 1st/2nd derivative of the loss wrt the raw score
        g = (L(preds+h) - L(preds-h)) / (2*h)
        hs = (L(preds+h) - 2*L(preds) + L(preds-h)) / h**2
        return g, np.maximum(hs, 1e-6)                        # hessian must stay positive
    return focal
X, y = make_classification(6000, 20, n_informative=6, weights=[0.95], flip_y=0.02, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, random_state=0)
dtr, dte = xgb.DMatrix(Xtr, ytr), xgb.DMatrix(Xte, yte)
b = xgb.train({"max_depth": 4, "eta": 0.1, "base_score": 0.0, "seed": 0}, dtr, 150, obj=make_obj())
print("focal custom obj AUC:", round(roc_auc_score(yte, b.predict(dte)), 4))      # raw scores (rank is enough for AUC)
b2 = xgb.train({"max_depth": 4, "eta": 0.1, "objective": "binary:logistic", "seed": 0}, dtr, 150)
print("built-in logistic AUC:", round(roc_auc_score(yte, b2.predict(dte)), 4))
```

**Follow-ups:**
- *Calibration with focal loss?* Probabilities are distorted; recalibrate (isotonic/Platt) if you need probabilities.
- *Asymmetric loss?* Use different multipliers on g and h for over vs under-prediction (e.g. pinball/quantile or a weighted squared error).
- *Why is the hessian needed?* XGBoost's leaf weight is `-G/(H+λ)` (Q38).

**Common mistakes:** Returning the gradient with the wrong sign. Treating raw scores as probabilities. Zero or negative hessian causing NaNs or no learning. Not setting a matching evaluation metric, so early stopping tracks the wrong thing.

### Q51 ⭐ 🔴 How do you get prediction intervals from GBMs (quantile loss, conformal prediction)?
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
**Say this first (1 line):** Train quantile models (for example the 10th and 90th percentile with pinball loss) to get adaptive-width intervals, then use conformal calibration on a held-out set to correct them so that coverage is actually guaranteed; plain residual-based conformal around a mean model is the simpler baseline.

**Then explain:**
- **Quantile loss (pinball):** for quantile q, loss = `q*(y-ŷ)` if `y>ŷ` else `(1-q)*(ŷ-y)`. LightGBM `objective="quantile", alpha=q`; XGBoost `reg:quantileerror` (`quantile_alpha`). Fit one model per quantile (or XGBoost's multi-quantile). Intervals widen where noise is larger (heteroscedastic data).
- **Weakness:** raw quantile models are often miscalibrated (coverage 80% only nominally), may cross (lower > upper), and have no finite-sample guarantee.
- **Split conformal prediction:**
  - Fit on a training set; on a separate calibration set compute scores; take the `ceil((n+1)(1-α))`-th smallest score as `q̂`; interval = prediction ± `q̂`. Guarantees marginal coverage at least 1-α if calibration and test data are exchangeable. Model-agnostic and cheap, but the width is constant.
  - **Conformalized quantile regression (CQR):** score = `max(lower(x) - y, y - upper(x))`; widen or shrink the quantile band by `q̂`. Keeps adaptive width and gets the guarantee.
- **Caveats:** the guarantee is marginal (average over x), not conditional for each x; breaks under distribution shift or time-series dependence (use adaptive/rolling conformal); needs held-out data.
- **Alternatives:** NGBoost/distributional models, bootstrap or ensemble spread (underestimates), Jackknife+.

**Example:** noise grows with x. Target 80% coverage on 1,500 test rows. Raw quantile 10-90: coverage 0.806. CQR: coverage 0.809 (adjustment q̂ = 0.014, so the band was already close). Split conformal around a mean model: coverage 0.801 but with a constant width of 6.03, against 5.83 average width for CQR, which is narrower where noise is low and wider where it is high.

**Code:**
```python
import numpy as np, lightgbm as lgb
rng = np.random.default_rng(0)
n = 6000
X = rng.uniform(0, 10, (n, 1)); y = 2*X[:, 0] + rng.normal(0, 0.3 + 0.4*X[:, 0], n)    # noise grows with x
Xtr, ytr, Xca, yca, Xte, yte = X[:3000], y[:3000], X[3000:4500], y[3000:4500], X[4500:], y[4500:]
P = dict(n_estimators=150, learning_rate=0.05, num_leaves=8, verbose=-1, random_state=0)
q = {a: lgb.LGBMRegressor(objective="quantile", alpha=a, **P).fit(Xtr, ytr) for a in (0.1, 0.5, 0.9)}
lo, hi = q[0.1].predict(Xte), q[0.9].predict(Xte)
print("quantile 10-90 coverage:", round(((yte >= lo) & (yte <= hi)).mean(), 3), "(target 0.80)")
# Conformalized quantile regression (CQR): widen/narrow using a calibration set
s = np.maximum(q[0.1].predict(Xca) - yca, yca - q[0.9].predict(Xca))              # conformity score
k = int(np.ceil((len(s)+1)*0.8)); qhat = np.sort(s)[k-1]
print("CQR coverage:", round(((yte >= lo-qhat) & (yte <= hi+qhat)).mean(), 3), "| qhat", round(qhat, 3))
# split conformal around a mean model: constant width
m = lgb.LGBMRegressor(**P).fit(Xtr, ytr); r = np.abs(yca - m.predict(Xca)); qh = np.sort(r)[k-1]
pr = m.predict(Xte); print("split-conformal coverage:", round(((yte >= pr-qh) & (yte <= pr+qh)).mean(), 3), "| width", round(2*qh, 2), "vs CQR mean width", round((hi-lo+2*qhat).mean(), 2))
```

**Follow-ups:**
- *Which to ship?* CQR when noise varies with x; split conformal as a simple, robust baseline.
- *Time series?* Exchangeability fails; use rolling calibration windows or adaptive conformal.
- *Calibrated vs sharp?* Coverage is the guarantee; narrower intervals at the same coverage are better ("sharpness").

**Common mistakes:** Calibrating on training data. Calling a quantile band "a 90% confidence interval" without checking coverage. Ignoring quantile crossing. Reporting average coverage and ignoring that it can be poor for subgroups.

### Q52 ⭐ 🔴 How do you serve tree ensembles in production: latency, model size, ONNX/Treelite, GPU, distributed training?
**Asked at:** Product cos, GCCs, analytics/consulting firms (MLE roles)
**Say this first (1 line):** Tree ensembles are cheap to serve but not free: prediction cost grows with number of trees times depth, so I measure single-row and batch latency, shrink the model if needed, move to a compiled runtime (Treelite, ONNX, lleaves) or GPU for heavy batch loads, and make sure the training-time feature pipeline is exactly what runs in production.

**Then explain (compact framework):**
- **Requirements:** online (p99 latency of a few ms, QPS) or batch (throughput, nightly)? Model refresh frequency?
- **Latency drivers:** `n_trees x depth`, feature computation (usually the real bottleneck), Python overhead per call, cold start, serialisation. Predict in batches where possible; avoid per-row Python calls.
- **Model size:** thousands of trees at 30 to 60 leaves are a few MB; reduce with fewer trees plus higher learning rate, smaller depth/leaves, pruning by early stopping, float32 thresholds, or distillation into a smaller model.
- **Runtimes:**
  - **Native** (`booster.predict`) is fine for modest load.
  - **Treelite / TL2cgen** compiles trees into C code/shared libraries; **lleaves** compiles LightGBM models via LLVM.
  - **ONNX / ONNX Runtime** (`onnxmltools`, `skl2onnx`, `hummingbird`) gives a portable format and a language-independent server, with care for operator support and float precision.
  - **GPU:** XGBoost `device="cuda"`, RAPIDS FIL for high-throughput batch inference; usually not worth it for single-row online calls (transfer overhead).
- **Training at scale:** XGBoost on Dask/Spark or multi-GPU; LightGBM data-parallel/feature-parallel/voting-parallel modes; histogram methods communicate small histograms, not rows. Often a big single machine plus `hist` is enough.
- **Reliability:** version model + feature code + data schema together; validate predictions of the converted model against the original on a test set (tolerance 1e-6); shadow deployment; monitor feature drift, prediction drift, latency, and error rate.
- **Trade-offs:** accuracy vs latency (fewer trees), simplicity vs speed (compiled runtimes add build and debugging steps), cost vs throughput (GPU).

**Example (machine-specific timings on my laptop, LightGBM, 500 trees, 63 leaves, 50 features, 20,000 training rows):** model file about 3.4 MB; one-row `predict` about 2.6 ms; 10,000 rows in one batch call about 152 ms, i.e. roughly 15 microseconds per row, so batching is about 170 times cheaper per row than single-row calls. The single-row figure is mostly call overhead, which is why compiled runtimes help online serving.

**Code:**
```python
import numpy as np, time, lightgbm as lgb, os, tempfile
from sklearn.datasets import make_classification
X, y = make_classification(20000, 50, n_informative=15, random_state=0)
m = lgb.LGBMClassifier(n_estimators=500, num_leaves=63, verbose=-1, random_state=0).fit(X, y)
f = os.path.join(tempfile.gettempdir(), "m.txt"); m.booster_.save_model(f); print("model file KB:", round(os.path.getsize(f)/1024))
x1 = X[:1]
t = time.perf_counter()
for _ in range(200): m.predict(x1)
print("single-row latency (ms, this machine):", round((time.perf_counter()-t)/200*1000, 2))
t = time.perf_counter(); m.predict(X[:10000]); print("batch 10k rows (ms, this machine):", round((time.perf_counter()-t)*1000))
```
Output on my machine: 3,414 KB; 2.57 ms; 152 ms. These numbers depend on hardware, thread count and library version. I did not benchmark Treelite or ONNX here.

**Follow-ups:**
- *How would you cut latency 10 times?* Precompute features, batch requests, compile the model, reduce trees/depth, and check thread settings.
- *Train-serve skew?* Same feature code or a feature store, and a replay test comparing offline and online predictions.
- *Do tree models need GPU for inference?* Only for very large batch scoring.

**Common mistakes:** Optimising the model when feature fetching dominates the latency. Benchmarking with one row only (or batch only) and generalising. Converting to ONNX and not validating output parity. Different categorical encoding or missing-value handling online than in training.

### Q53 ⭐ 🔴 What is the GBDT + logistic regression approach (leaf-index features) and when is it useful?
**Asked at:** Product cos, GCCs, analytics/consulting firms (ads/ranking teams)
**Say this first (1 line):** Train a GBDT, then use "which leaf did this row land in, in each tree" as a one-hot feature vector for a logistic regression; the trees do automatic feature crossing and the linear model on top is fast to train, update and serve (the Facebook ads CTR approach, He et al. 2014).

**Then explain:**
- **How:** with T trees, each row activates exactly one leaf per tree, so the encoding has T ones and many zeros. Each leaf is a learned rule such as "age < 30 and clicks > 5". Logistic regression learns a weight per rule.
- **Why it can help:**
  - Trees create non-linear, interaction features without manual crossing.
  - LR on sparse features is easy to retrain frequently (online learning) while trees are refreshed less often. This was the key trick in the original ad-click system.
  - It can combine leaf features with other sparse features (user ID, ad ID) in the LR.
  - Small accuracy gains on top of a GBDT are possible.
- **Caveats:**
  - Overfitting: if the same rows train the trees and the LR, the leaf features are too good. Use separate data (trees on A, LR on B) or at least regularise strongly.
  - Today, a well-tuned GBDT alone is often as good; deep models with embeddings have replaced this in large ad systems.
  - Feature dimension = total leaves, so keep trees small and few.
- **When useful:** very large sparse CTR/ranking problems, models that need cheap frequent updates, or when linear serving/explanation of rules is wanted.

**Example:** 8,000 rows, 20 features, test AUC: GBDT alone 0.9670; GBDT leaves + LR 0.9694; LR on raw features 0.9608. A small gain on a dataset where the GBDT is already strong. Treat the lift as an empirical question.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
X, y = make_classification(8000, 20, n_informative=8, flip_y=0.05, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
Xa, Xb, ya, yb = train_test_split(Xtr, ytr, test_size=0.5, random_state=0)       # trees on A, LR on B (reduces overfit)
gb = GradientBoostingClassifier(n_estimators=50, max_depth=3, random_state=0).fit(Xa, ya)
leaf = lambda X_: gb.apply(X_)[:, :, 0]                                          # (n_samples, n_trees) leaf index per tree
oh = OneHotEncoder(handle_unknown="ignore").fit(leaf(Xa))
lr = LogisticRegression(max_iter=2000, C=0.5).fit(oh.transform(leaf(Xb)), yb)
print("GBDT alone       AUC", round(roc_auc_score(yte, gb.predict_proba(Xte)[:, 1]), 4))
print("GBDT leaves + LR AUC", round(roc_auc_score(yte, lr.predict_proba(oh.transform(leaf(Xte)))[:, 1]), 4))
print("LR on raw        AUC", round(roc_auc_score(yte, LogisticRegression(max_iter=2000).fit(Xtr, ytr).predict_proba(Xte)[:, 1]), 4))
```
Note the GBDT-alone line uses the half-data model (trained on A only), so the comparison is fair on data used for the trees.

**Follow-ups:**
- *XGBoost/LightGBM version?* `pred_leaf=True` (XGBoost) or `pred_leaf=True` in LightGBM `predict` returns leaf indices.
- *Why not feed leaf IDs straight into a neural net?* You can: embed the leaf indices; that is the bridge to modern deep CTR models.
- *Why split the data?* To avoid the LR trusting leaf features that were fit on its own labels.

**Common mistakes:** Training trees and LR on the same rows without regularisation. Using too many deep trees (huge, sparse, overfit encoding). Not refreshing the trees when the data drifts while only retraining the LR.



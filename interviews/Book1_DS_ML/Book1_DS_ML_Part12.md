# Book 1 — Part 12: NumPy / pandas / sklearn Live-Coding & AI-Code-Review Rounds

**Topic:** pandas wrangling, NumPy vectorization, sklearn Pipelines/CV, leakage bugs, from-scratch metrics, debugging and reviewing LLM-generated ML code (SQL -> Book 3, DSA -> Book 5)
**Target:** 45
**Actual:** 51 (⭐⭐⭐ 18, ⭐⭐ 23, ⭐ 10)
**Date:** 2026-10-20

### Q1 ⭐⭐⭐ 🟢 Given a transactions DataFrame (user_id, ts, amount, category), use groupby with named aggregation to get per-user total, mean, count and last-transaction date, then return the top 3 categories by spend for each user.
**Asked at:** Product cos, fintech, GCC; pandas live rounds (Pinterest, Bloomberg, Voleon reports)
**Say this first (1 line):** One `groupby().agg()` with named aggregation gives the per-user stats; for the top 3 categories I sum spend per (user, category), sort, and take `head(3)` per user.

**Then explain:**
- Named aggregation (`out_name=("column", "func")`) gives clean column names and no MultiIndex to flatten.
- Top-N per group is a two-step job: first aggregate to (user, category) totals, then sort descending and take `groupby("user_id").head(3)`.
- `head(3)` keeps ties arbitrarily; use `rank(method="first")` (or `"min"` if you want ties kept) if the interviewer cares about ties.
- Use `nlargest` inside `apply` only for small data; sort + `head` is faster and simpler.

**Example:** User 1 spent 627 on books, 351 on food, 218 on games, so those three rows come back in that order.

**Code:**
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(0)
n = 20
tx = pd.DataFrame({
    "user_id": rng.integers(1, 4, n),
    "ts": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 60, n), unit="D"),
    "amount": rng.integers(50, 500, n).astype(float),
    "category": rng.choice(["food", "travel", "books", "games"], n),
})
summary = tx.groupby("user_id").agg(
    total=("amount", "sum"), mean=("amount", "mean"),
    n_tx=("amount", "count"), last_tx=("ts", "max"))

top3 = (tx.groupby(["user_id", "category"], as_index=False)["amount"].sum()
          .sort_values(["user_id", "amount"], ascending=[True, False])
          .groupby("user_id").head(3))
print(summary.round(1))
print(top3)
```
Output (run): user 1 -> total 1301.0, mean 216.8, 6 transactions, last 2025-02-21; top3 for user 1 = books 627, food 351, games 218.

**Follow-ups:**
- *Why not `apply`?* It runs a Python function per group; the sort + `head` version stays in C.
- *How to put the 3 categories in one row per user?* `top3.assign(rk=top3.groupby("user_id").cumcount()).pivot(index="user_id", columns="rk", values="category")`.
- *`count` vs `size`?* `count` skips NaN, `size` counts rows.

**Common mistakes:** Sorting before aggregating (the sort is wasted), forgetting `as_index=False` so the keys vanish into the index, using `agg` with a dict of lists and then fighting the MultiIndex columns.

### Q2 ⭐⭐⭐ 🟢 Write code to audit missing values in a DataFrame (count, percent, pattern by group) and impute numeric and categorical columns sensibly. Why must the imputation statistics come from the training split only?
**Asked at:** Product cos, GCC, consulting-style DS (TCS, ION reports)
**Say this first (1 line):** I first measure how much is missing and whether it depends on another column, then impute using statistics computed on the training split only, because any statistic computed on test data leaks test information.

**Then explain:**
- Audit three things: count, percent, and pattern by group (`df.isna().groupby(df["segment"]).mean()`). If missingness differs by group it is not random (MAR/MNAR), and a plain mean/median can bias results.
- Numeric: median (robust to outliers) plus a `was_missing` indicator column, since the fact that a value is missing is often a signal. Categorical: most frequent, or an explicit `"missing"` level.
- Why train-only: the median/mode is a learned parameter. If it is computed on all rows, test values influence the training features. The score looks slightly better than reality, and in production you will not have the future batch anyway.
- Best practice: put `SimpleImputer` in a `Pipeline` so each CV fold refits it automatically.

**Example (run):** in 200 synthetic rows `age` has 9.5% missing, `city` 17%, and `city` is missing 33% of the time when `segment == "y"` but 0% for `x`. That pattern says "do not just drop rows"; add an indicator.

**Code:**
```python
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0)
df = pd.DataFrame({"age": rng.normal(40, 10, 200),
                   "city": rng.choice(["A", "B", "C"], 200),
                   "segment": rng.choice(["x", "y"], 200)})
df.loc[rng.random(200) < 0.15, "age"] = np.nan
df.loc[(df.segment == "y") & (rng.random(200) < 0.3), "city"] = None

audit = pd.DataFrame({"n_missing": df.isna().sum(),
                      "pct": (df.isna().mean() * 100).round(1)})
print(audit)
print(df.drop(columns="segment").isna().groupby(df["segment"]).mean().round(2))

tr, te = train_test_split(df, test_size=0.25, random_state=0)
num, cat = ["age"], ["city"]
med, mode = tr[num].median(), tr[cat].mode().iloc[0]      # train only
tr, te = tr.copy(), te.copy()
for d in (tr, te):
    d["age_was_na"] = d["age"].isna().astype(int)
    d[num] = d[num].fillna(med)                            # same train values for both
    d[cat] = d[cat].fillna(mode)
print(med.to_dict(), mode.to_dict(), te.isna().sum().sum())
```
Output (run): age 19 missing (9.5%), city 34 (17.0%); city missing rate by segment x = 0.00, y = 0.33; train median age 40.83, mode city A; zero NaN left in test.

**Follow-ups:**
- *When is mean/median imputation bad?* When missingness is informative or you need correct variances; use indicators, group-wise medians, or model-based imputation (`IterativeImputer`, or tree models that handle NaN natively like HistGradientBoosting).
- *What about the test set having a new NaN pattern?* Use the train statistics; never refit.

**Common mistakes:** Calling `fillna(df.mean())` before the split, imputing the target, dropping rows blindly, and not adding a missing-indicator.

### Q3 ⭐⭐⭐ 🟢 Explain and demonstrate .loc vs .iloc vs boolean masking, and fix a SettingWithCopyWarning / chained-assignment bug (df[df.a>0]['b'] = 1). What changes with copy-on-write?
**Asked at:** Product cos, GCC, general pandas rounds
**Say this first (1 line):** `.loc` selects by label (end-inclusive), `.iloc` by integer position (end-exclusive), and a boolean mask filters rows; `df[mask]["b"] = 1` writes to a temporary copy, so the fix is a single `df.loc[mask, "b"] = 1`.

**Then explain:**
| Tool | Uses | Slice end |
|---|---|---|
| `.loc[rows, cols]` | labels or boolean mask | inclusive |
| `.iloc[rows, cols]` | integer positions | exclusive |
| `df[mask]` | boolean filtering | n/a |

- Chained indexing is two calls: `df[mask]` (may return a copy) and then `["b"] = 1` on that. Whether the original changes depends on internals, which is why pandas warns with `SettingWithCopyWarning`.
- `df.loc[mask, "b"] = 1` is one call to `__setitem__`, so it is unambiguous.
- Copy-on-write (opt-in in pandas 2.x with `pd.options.mode.copy_on_write = True`, default in pandas 3): any result of an indexing operation behaves as a copy, so a chained assignment can never change the parent. It does not raise an error; it just silently does nothing to the original (newer pandas emits a `ChainedAssignmentError` warning). The warning-based ambiguity is gone, and many defensive `.copy()` calls become unnecessary.

**Example:** With index `[10, 11, 12, 13]`, `df.loc[10:12]` returns 3 rows, `df.iloc[0:2]` returns 2 rows.

**Code:**
```python
import pandas as pd, warnings
df = pd.DataFrame({"a": [-1, 2, 3, 0], "b": [0, 0, 0, 0]}, index=[10, 11, 12, 13])
print(df.loc[11, "a"], df.iloc[1, 0], df.loc[10:12].shape, df.iloc[0:2].shape)

d2 = df.copy()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    d2[d2.a > 0]["b"] = 99                       # BUG: writes to a temporary copy
    print("changed original:", (d2.b == 99).any(), w[0].category.__name__)

df.loc[df.a > 0, "b"] = 1                         # FIX
print(df)
```
Output (run, pandas 2.3): `2 2 (3, 2) (2, 2)`, `changed original: False SettingWithCopyWarning`, and rows 11 and 12 get `b = 1`.

**Follow-ups:**
- *Why does `.loc[10:12]` include 12?* Labels have no natural "next" label, so label slices include the end.
- *Is `.loc[mask]["b"] = 1` safe if I called `.copy()` first?* Yes, but then you are modifying a new frame, not the original.

**Common mistakes:** Assuming the warning always means the original is unchanged (sometimes it is changed, sometimes not; that is the problem), silencing the warning with `pd.options.mode.chained_assignment = None`, and mixing `.iloc` and labels after a sort or filter.

### Q4 ⭐⭐⭐ 🟡 Merge a 1M-row orders table with a customers table and the row count unexpectedly grows. Write code to find the cause (duplicate keys), prevent it (validate=, indicator=) and fix it.
**Asked at:** Product cos, e-commerce (Flipkart/Amazon style), GCC
**Say this first (1 line):** Row growth after a left join means the right table has duplicate keys; I find them with `duplicated`, prevent the problem with `validate="many_to_one"`, and fix it by deduplicating the lookup table with a clear rule.

**Then explain:**
- Each left row matches every right row with the same key, so 1 order with 2 customer rows becomes 2 rows (a join "fan-out"). Duplicating rows also double-counts revenue downstream.
- Check key uniqueness before joining: `cust.cust_id.is_unique`, `cust[cust.cust_id.duplicated(keep=False)]`.
- `validate="many_to_one"` makes pandas raise `MergeError` if the right keys are not unique. `indicator=True` adds `_merge` (`both`, `left_only`, `right_only`) so you can count unmatched rows.
- Fix: deduplicate with a business rule (latest record, non-null, a surrogate key) rather than a blind `drop_duplicates`. Also assert `len(out) == len(orders)` after the merge.

**Example:** 6 orders merged with a customer table where customer 2 appears twice gives 7 rows.

**Code:**
```python
import pandas as pd
orders = pd.DataFrame({"order_id": range(6), "cust_id": [1, 1, 2, 3, 4, 9]})
cust = pd.DataFrame({"cust_id": [1, 2, 2, 3, 5], "city": list("ABCDE")})
m = orders.merge(cust, on="cust_id", how="left")
print(len(orders), len(m))                                  # 6 7
print(cust[cust.cust_id.duplicated(keep=False)])             # the culprit rows
try:
    orders.merge(cust, on="cust_id", validate="many_to_one")
except Exception as e:
    print(type(e).__name__, e)
cust_u = cust.sort_values("city").drop_duplicates("cust_id", keep="last")  # business rule here
m2 = orders.merge(cust_u, on="cust_id", how="left", validate="many_to_one", indicator=True)
assert len(m2) == len(orders)
print(m2["_merge"].value_counts())
```
Output (run): `6 7`; `MergeError Merge keys are not unique in right dataset; not a many-to-one merge`; after the fix 6 rows, 4 `both`, 2 `left_only`.

**Follow-ups:**
- *At 1M rows, how do you find duplicates fast?* `cust.cust_id.value_counts().loc[lambda s: s > 1]`.
- *What if NaN keys exist?* pandas matches NaN to NaN in merges, which can create a huge fan-out; drop or handle NaN keys first.

**Common mistakes:** Only checking row count after the damage is done, using `drop_duplicates()` with no sort order (keeps an arbitrary row), and not validating in production code.

### Q5 ⭐⭐⭐ 🟡 This iterrows/apply(axis=1) code takes 10 minutes on 5M rows. Rewrite it vectorized (np.where / np.select / map / merge) and explain why it is faster.
**Asked at:** Product cos, Amazon India, Walmart GCC, startups
**Say this first (1 line):** `iterrows` and `apply(axis=1)` run a Python function once per row, while vectorized code does the whole column in compiled C loops, which is typically 100-1000x faster.

**Then explain:**
- Per-row cost: `apply(axis=1)` builds a `Series` for every row (allocation, type checks, interpreter overhead). Vectorized ops work on contiguous arrays, with no per-row Python.
- Replace patterns: if/elif chain -> `np.select`; two-way if/else -> `np.where`; dictionary lookup -> `Series.map`; lookup from another table -> `merge`; string ops -> `.str` methods.
- Verify equality of old and new output (`np.allclose`, `assert (a == b).all()`) before you trust the rewrite.
- Memory trade-off: vectorized code creates temporaries; for huge data use chunking or `numexpr`/`eval`.

**Example (run):** On 20k rows my (slow, busy) laptop took 12.6 s with `apply(axis=1)` and 6 ms vectorized, about 2000x; the exact ratio depends on the machine. Extrapolation, not measured: apply cost grows roughly linearly with rows, so 5M rows would be tens of minutes for the slow version and a second or two for the vectorized one.

**Code:**
```python
import time
import numpy as np, pandas as pd
rng = np.random.default_rng(0)
n = 20_000
df = pd.DataFrame({"amount": rng.gamma(2, 500, n),
                   "country": rng.choice(["IN", "DE", "US"], n),
                   "is_prime": rng.random(n) < 0.3})

RATE = {"IN": 0.18, "DE": 0.19, "US": 0.07}
def slow_row(r):                                   # the slow version: one Python call per row
    tier = "high" if r.amount > 2000 else "mid" if r.amount > 500 else "low"
    disc = 0.1 if r.is_prime else 0.0
    return pd.Series({"tier": tier, "net": r.amount * (1 - disc) * (1 + RATE[r.country])})

def fast(d):                                       # vectorized version
    tier = np.select([d.amount > 2000, d.amount > 500], ["high", "mid"], default="low")
    rate = d.country.map(RATE)
    disc = np.where(d.is_prime, 0.1, 0.0)
    return pd.DataFrame({"tier": tier, "net": d.amount * (1 - disc) * (1 + rate)}, index=d.index)

t0 = time.perf_counter(); a = df.apply(slow_row, axis=1); t1 = time.perf_counter()
b = fast(df); t2 = time.perf_counter()
print(f"apply(axis=1): {t1 - t0:.2f}s   vectorized: {t2 - t1:.4f}s")      # 12.56s vs 0.0064s here
assert (a.tier == b.tier).all() and np.allclose(a.net.astype(float), b.net)  # outputs identical
```
The assert is the "verify equality" step: the tiers match exactly and `net` matches with `np.allclose`.

**Follow-ups:**
- *When is `apply` fine?* Small data, or logic that truly cannot be vectorized (then try `numba`, or `groupby` + `transform`).
- *Is `itertuples` better than `iterrows`?* Yes, it is much faster (no Series per row) but still a Python loop.

**Common mistakes:** Thinking `apply` is vectorized, not checking that the new output equals the old, and chaining many boolean masks that each copy the data.

### Q6 ⭐⭐⭐ 🟡 Review this snippet: StandardScaler is fit on the full dataset before train_test_split. Identify the leakage, explain the impact, and rewrite it correctly with a Pipeline.
**Asked at:** Nearly all DS/MLE loops; Flipkart, Swiggy, JPMC GCC, Zalando, Booking
**Say this first (1 line):** Fitting `StandardScaler` on the full data lets the test rows influence the mean and std used to transform the training rows, which is leakage; the fix is to split first and put the scaler inside a `Pipeline` so it is fit on training data only.

**Then explain:**
- Buggy snippet: `X = StandardScaler().fit_transform(X)` then `train_test_split(X, y)`. The test set's mean and variance are baked into the training features.
- Impact: for plain scaling the optimistic bias is usually small, but it is a process bug. With heavier "learned" steps (PCA, feature selection, imputation, target encoding, SMOTE) the same pattern can inflate scores a lot. Interviewers want to hear that you know the rule, not that you can size this one effect.
- Fix: `Pipeline` fits each step on the training fold only and only calls `transform` on the validation or test fold. This also keeps cross-validation honest, because every fold refits the scaler.
- In production the scaler is saved with the model, so you scale a single new row with the training mean and std. You never have the "full dataset" statistics.

**Example (run):** 300 rows, 20 features, 20% test. A scaler fitted on all rows has means that differ from the train-only scaler's means by 0.025 on average (std by 0.016), so test-set information is already inside the scale. Tiny here, which is why plain scaling leaks only slightly; the process is still wrong. Correct approach: scale test columns with train statistics, so their means are whatever the test data really looks like.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

X, y = make_classification(n_samples=300, n_features=20, random_state=0)

# BUGGY: scaler sees test rows
# X_all = StandardScaler().fit_transform(X); Xtr, Xte, ... = train_test_split(X_all, y)

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0)
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(Xtr, ytr)
print("test acc:", round(pipe.score(Xte, yte), 3))                 # 0.917
print("5-fold CV:", cross_val_score(pipe, X, y, cv=5).mean().round(3))  # 0.933, scaler refit per fold
leak, ok = StandardScaler().fit(X), StandardScaler().fit(Xtr)         # size of the leak in the statistics
print("mean shift:", np.abs(leak.mean_ - ok.mean_).mean().round(3))   # 0.025
```

**Follow-ups:**
- *Does tree-based modelling need scaling?* No, trees are invariant to monotonic scaling, so this leak does not apply to them; but imputers and encoders still can leak.
- *What about time series?* Split by time, fit on the past only.

**Common mistakes:** Saying "scaling does not leak because it is unsupervised" (it still uses test data), scaling inside the CV loop by hand and forgetting a step, and leaving `fit_transform` on the test set.

### Q7 ⭐⭐⭐ 🟡 Build an sklearn Pipeline with ColumnTransformer (median imputer + scaler for numeric; most-frequent imputer + OneHotEncoder(handle_unknown='ignore') for categorical) feeding a classifier, and evaluate it with cross_val_score.
**Asked at:** Product cos, fintech, GCC, Spotify/Zalando-type DS
**Say this first (1 line):** I wrap numeric and categorical branches in a `ColumnTransformer`, chain it with the classifier in a `Pipeline`, and pass the raw DataFrame to `cross_val_score`, so every fold refits imputers, scaler and encoder on its own training part.

**Then explain:**
- Numeric branch: median imputer (robust to outliers) then `StandardScaler`. Categorical branch: most-frequent imputer then `OneHotEncoder(handle_unknown="ignore")`, which gives an all-zero row for a category not seen in training instead of crashing.
- `ColumnTransformer` picks columns by name, so column order in new data does not matter. By default it drops unlisted columns (`remainder="drop"`), so list everything you want.
- Use a probability-aware metric (`roc_auc`) for classifiers when classes are imbalanced; accuracy hides problems.
- One object fits, saves and serves, so there is no training/serving skew.

**Example:** 500 rows, 10% missing in `age` and `city`; 5-fold ROC-AUC is about 0.88.

**Code:**
```python
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
rng = np.random.default_rng(0); m = 500
d = pd.DataFrame({"age": rng.normal(40, 10, m), "income": rng.lognormal(10, 0.5, m),
                  "city": rng.choice(["A", "B", "C"], m), "plan": rng.choice(["free", "pro"], m)})
y = ((d.age > 42) ^ (d.city == "A") | (rng.random(m) < 0.1)).astype(int)
d.loc[rng.random(m) < 0.1, "age"] = np.nan
d.loc[rng.random(m) < 0.1, "city"] = np.nan
pre = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), ["age", "income"]),
    ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"),
                          OneHotEncoder(handle_unknown="ignore")), ["city", "plan"])])
clf = make_pipeline(pre, RandomForestClassifier(200, random_state=0))
sc = cross_val_score(clf, d, y, cv=5, scoring="roc_auc")
print(sc.round(3), sc.mean().round(3))
```
Output (run): `[0.888 0.848 0.843 0.914 0.892] 0.877`.

**Follow-ups:**
- *Why scale for a random forest?* You do not; it is there to show the pattern. It matters for linear models, SVM, kNN.
- *How do you tune it?* `GridSearchCV` with names like `columntransformer__num__simpleimputer__strategy`.

**Common mistakes:** Preprocessing the full DataFrame before CV, forgetting `handle_unknown="ignore"` (production crashes on a new city), and relying on `remainder="drop"` without noticing a column was dropped.

### Q8 ⭐⭐⭐ 🟡 Use groupby transform vs agg vs apply: add a column with each row's group mean, z-score within group, and share of group total. When is each the right tool?
**Asked at:** Product cos, GCC, pandas live rounds
**Say this first (1 line):** `agg` collapses each group to one row, `transform` returns one value per original row (same shape, aligned to the index), and `apply` is the flexible fallback that is slower; for group mean, z-score and share I use `transform`.

**Then explain:**
| Tool | Output shape | Use for |
|---|---|---|
| `agg` | one row per group | summary tables |
| `transform` | same length as input | add group stats as a column (mean, z-score, share, fill with group median) |
| `apply` | anything | custom logic that needs the whole group frame (last resort) |

- `transform("mean")` with a built-in string is fast (Cython). A `lambda` works but runs per group in Python.
- A group with 1 row has std 0, so the z-score is 0/0 = NaN; handle it with `fillna(0)` or a minimum group size.

**Example:** Team `a` sales 10 and 20 -> group mean 15, z-scores -1 and +1, shares 0.33 and 0.67.

**Code:**
```python
import pandas as pd
g = pd.DataFrame({"team": list("aabbbc"), "sales": [10., 20, 5, 15, 40, 7]})
grp = g.groupby("team")["sales"]
g["grp_mean"] = grp.transform("mean")
g["z"] = (g["sales"] - g["grp_mean"]) / grp.transform(lambda s: s.std(ddof=0))
g["share"] = g["sales"] / grp.transform("sum")
print(g.round(2))
```
Output (run): team `b` rows get z = -1.02, -0.34, 1.36; team `c` (one row) gets NaN z and share 1.00.

**Follow-ups:**
- *`agg` + `merge` back vs `transform`?* Same result; `transform` is shorter and cannot misalign rows.
- *Percent of total across the whole frame?* `g.sales / g.sales.sum()`, no groupby.

**Common mistakes:** Using `apply` for something `transform` does, getting a shape error because `agg` returned fewer rows than the frame, and forgetting the single-row group NaN.

### Q9 ⭐⭐⭐ 🟡 Review this LLM-generated training script for bugs: it applies SMOTE before CV, evaluates on the training set, uses shuffled KFold on time-ordered data and reports accuracy on a 2% positive class. List and fix every issue.
**Asked at:** AI-allowed coding rounds (2026 trend); product cos, fintech
**Say this first (1 line):** The script has four serious bugs (SMOTE outside CV, scoring on the train set, shuffled folds on time data, accuracy on a 2% positive class), and each one makes the model look better than it is.

**Then explain:**
| # | Bug | Why it is wrong | Fix |
|---|---|---|---|
| 1 | SMOTE before CV | Synthetic points are built from rows that end up in validation folds, so validation sees near-copies of training rows | `imblearn.pipeline.Pipeline([SMOTE, model])` so only training folds are resampled |
| 2 | Evaluating on the training set | Measures memorisation | Hold-out set or CV on unseen rows |
| 3 | Shuffled `KFold` on time-ordered data | Future rows train the model that predicts the past | `TimeSeriesSplit`, or a time-based hold-out with a gap |
| 4 | Accuracy at 2% positives | "Always negative" gets 98% | PR-AUC / average precision, recall at fixed precision, a cost-based threshold |
- Also check: the resampled data must never reach the validation fold, set seeds, and report the prevalence baseline (the PR-AUC of a random model equals the positive rate).

**Example (run):** 4,000 rows, 2.9% positives. Always-negative accuracy is 0.971. Average precision with SMOTE applied before CV: **0.999**. With SMOTE inside the pipeline: **0.072** (prevalence baseline 0.029). The 0.999 is pure leakage; the honest model is barely better than chance on this data.

**Code:**
```python
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as IPipe
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.datasets import make_classification
X, y = make_classification(4000, 20, n_informative=3, weights=[0.98], flip_y=0.02, random_state=0)
cv = StratifiedKFold(5, shuffle=True, random_state=0)        # for time-ordered data use TimeSeriesSplit
Xr, yr = SMOTE(random_state=0).fit_resample(X, y)            # BUG: resample before CV
rf = RandomForestClassifier(100, random_state=0)
print("leaky   :", cross_val_score(rf, Xr, yr, cv=cv, scoring="average_precision").mean().round(3))   # 0.999
pipe = IPipe([("smote", SMOTE(random_state=0)),
              ("rf", RandomForestClassifier(100, random_state=0))])
print("pipeline:", cross_val_score(pipe, X, y, cv=cv, scoring="average_precision").mean().round(3))   # 0.072
```

**Follow-ups:**
- *Is SMOTE even needed?* Often `class_weight` or threshold tuning gets the same result; always compare to a no-resampling baseline.
- *Would you resample the validation set?* Never; it must reflect real class balance.

**Common mistakes:** Fixing only the SMOTE bug, reporting AUC-ROC (optimistic with rare positives) instead of PR-AUC, and not mentioning calibration or the decision threshold.

### Q10 ⭐⭐⭐ 🟡 Create 7-day and 30-day rolling mean/count features per customer from an event log without leaking future information (shift, closed='left', time-based windows).
**Asked at:** Fintech (PhonePe, Klarna), e-commerce, time-aware feature rounds
**Say this first (1 line):** I compute rolling windows over a time-based index per customer with `closed="left"`, which excludes the current event, so a row's feature only uses strictly earlier events.

**Then explain:**
- Time-based windows ("7D", "30D") need a sorted datetime index. They count calendar days, not rows, so gaps are handled correctly.
- `closed="left"` means the window is `[t-7D, t)`: the current row is excluded. Without it the current amount (often the target or a same-time event) sneaks in.
- For row-based windows use `shift(1).rolling(n)`, the same idea.
- Validate: pick a row and recompute the feature manually from rows with `ts < t`.
- Always sort by `(customer, ts)` first; unsorted data silently gives wrong windows.

**Example (run):** Customer 0's event on Jan 26 (amount 87) has 7D mean 27.0 and count 2 (the two earlier events, not the 87 itself). Their Feb 8 event has no events in the previous 7 days, so its 7D features are NaN (an empty window comes back as NaN, not 0).

**Code:**
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(0)
ev = pd.DataFrame({"cust": rng.integers(0, 3, 40),
                   "ts": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 60 * 24, 40), unit="h"),
                   "amt": rng.integers(10, 100, 40).astype(float)}
                  ).sort_values(["cust", "ts"]).reset_index(drop=True)

def add_roll(df, win):
    out = []
    for c, g in df.groupby("cust"):
        r = g.set_index("ts")["amt"].rolling(win, closed="left")   # excludes current row
        out.append(pd.DataFrame({f"mean_{win}": r.mean().values,
                                 f"cnt_{win}": r.count().values}, index=g.index))
    return pd.concat(out)

feat = ev.join(add_roll(ev, "7D")).join(add_roll(ev, "30D"))

# invariant: recompute one row by hand from strictly earlier events
row = feat.loc[6]
past = ev[(ev.cust == row.cust) & (ev.ts < row.ts) & (ev.ts >= row.ts - pd.Timedelta("7D"))]
assert np.isclose(past.amt.mean(), row["mean_7D"]) and len(past) == row["cnt_7D"]
```
(Run: manual and feature value agree, mean 27.0 over 2 events.)

**Follow-ups:**
- *Why a loop over customers?* `groupby().rolling("7D", on="ts")` also works but needs index alignment care; the loop is explicit and easy to verify.
- *What about training/serving?* In production compute the same window over events before the scoring time; share the code.

**Common mistakes:** Default `closed="right"` (includes today), rolling over unsorted data, using row counts where days are needed, and computing features after the train/test split on the test table alone (history is lost).

### Q11 ⭐⭐⭐ 🟡 Write code for correct cross-validation when rows are grouped (multiple rows per user) or time-ordered: use GroupKFold / TimeSeriesSplit / StratifiedGroupKFold and show how naive KFold inflates the score.
**Asked at:** Product cos, fintech, Booking/Spotify-type loops
**Say this first (1 line):** Plain shuffled `KFold` puts rows from the same user (or the future) in both train and validation, so the model memorises users or sees the future and the score is inflated; use `GroupKFold` for grouped rows and `TimeSeriesSplit` for time order.

**Then explain:**
- Grouped data: `GroupKFold(groups=user_id)` keeps every user wholly in one fold. `StratifiedGroupKFold` does the same while roughly preserving class balance (needs `shuffle=True` with a seed for randomness).
- Time-ordered data: `TimeSeriesSplit` trains on the past and validates on the later block (expanding window). Add `gap=` if features use windows that look ahead or labels mature late.
- Rule of thumb: validation must mimic how the model will be used. New users at serving time -> split by user. Future data at serving time -> split by time.

**Example (run):** 200 users x 20 rows; features identify the user, labels are random per user (so the true AUC is 0.5). Naive `KFold` AUC **0.999**; `GroupKFold` **0.55**; `StratifiedGroupKFold` **0.51** (noise around 0.5). On a drifting series (1,000 points of trend + slow cycle + noise, random-forest regressor, second snippet below), shuffled KFold R2 was **0.97** vs `TimeSeriesSplit` R2 **-1.76**: shuffling lets the model interpolate between neighbouring points and hides the drift (the forest cannot extrapolate the trend into the future).

**Code:**
```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, GroupKFold, StratifiedGroupKFold, cross_val_score
rng = np.random.default_rng(0)
n_users, per = 200, 20
uid = np.repeat(np.arange(n_users), per)
X = rng.normal(size=(n_users, 5)).repeat(per, axis=0) + 0.1 * rng.normal(size=(n_users * per, 5))
y = rng.integers(0, 2, n_users)[uid]                 # label depends on user only
rf = RandomForestClassifier(100, random_state=0)
auc = lambda cv, **kw: cross_val_score(rf, X, y, cv=cv, scoring="roc_auc", **kw).mean().round(3)
print("naive:", auc(KFold(5, shuffle=True, random_state=0)))              # 0.999
print("group:", auc(GroupKFold(5), groups=uid))                           # 0.552
print("strat-group:", auc(StratifiedGroupKFold(5, shuffle=True, random_state=0), groups=uid))  # 0.51
```
Time-ordered data (separate standalone snippet):
```python
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, TimeSeriesSplit, cross_val_score
rng = np.random.default_rng(0)
t = np.arange(1000)
y = 0.02 * t + 3 * np.sin(t / 30) + rng.normal(0, 1, t.size)   # trend + slow cycle + noise
X = np.c_[t, t % 7]                                            # time index and weekday
rf = RandomForestRegressor(100, random_state=0)
r2 = lambda cv: cross_val_score(rf, X, y, cv=cv, scoring="r2").mean().round(2)
print("shuffled KFold  R2:", r2(KFold(5, shuffle=True, random_state=0)))   # 0.97
print("TimeSeriesSplit R2:", r2(TimeSeriesSplit(5)))                       # -1.76
```

**Follow-ups:**
- *Does GroupKFold shuffle?* Not by default; it balances group sizes deterministically. Use `StratifiedGroupKFold(shuffle=True)` for randomness.
- *Time plus groups?* Split by time first, and make sure the same entity is handled consistently (often also by group).

**Common mistakes:** Forgetting to pass `groups=`, using `KFold(shuffle=True)` on time data, and shuffling a time series "to make it random".

### Q12 ⭐⭐⭐ 🟡 Implement out-of-fold target encoding for a high-cardinality categorical feature in pandas/NumPy, with smoothing, and show why naive target encoding leaks.
**Asked at:** Product cos, fintech, Kaggle-style rounds
**Say this first (1 line):** Naive target encoding replaces each category with its mean target computed on the same rows, so a row's own label leaks into its feature; out-of-fold encoding with smoothing computes each row's value from the other folds only.

**Then explain:**
- Smoothed encoding: `(sum_y + m * prior) / (count + m)`. A category with few rows is pulled toward the global prior; `m` controls how strongly.
- Out-of-fold (OOF): split train into K folds; encode fold k using stats from the other K-1 folds. The train feature never contains the row's own label.
- For validation or test rows and for serving, use statistics from the whole training set; unseen categories get the prior.
- The leak is worst for high cardinality: with about 2 rows per level, the "encoded" value is almost the label itself.

**Example (run):** 1,500 levels, labels pure noise. Naive encoding: train AUC **0.921** (fake), test AUC **0.477**. OOF with smoothing: train AUC **0.521**, test **0.478**. Honest encoding shows there is no signal, as it should.

**Code:**
```python
import numpy as np, pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
df = pd.DataFrame({"cat": rng.integers(0, 1500, 3000), "y": rng.integers(0, 2, 3000)})

def te_fit(train, m=10):
    prior = train.y.mean()
    s = train.groupby("cat").y.agg(["sum", "count"])
    return (s["sum"] + m * prior) / (s["count"] + m), prior
def te_apply(cat, enc, prior):
    return cat.map(enc).fillna(prior)                       # unseen -> prior
def te_oof(train, k=5, m=10, seed=0):
    out = pd.Series(np.nan, index=train.index)
    for a, b in KFold(k, shuffle=True, random_state=seed).split(train):
        enc, prior = te_fit(train.iloc[a], m)
        out.iloc[b] = te_apply(train.iloc[b]["cat"], enc, prior).values
    return out

tr, te = df.iloc[:2000].copy(), df.iloc[2000:].copy()
enc, prior = te_fit(tr, m=0.001)                             # ~ naive, almost raw mean
print("naive  train/test AUC:", round(roc_auc_score(tr.y, te_apply(tr.cat, enc, prior)), 3),
      round(roc_auc_score(te.y, te_apply(te.cat, enc, prior)), 3))     # 0.921 0.477
oof = te_oof(tr); enc, prior = te_fit(tr)
print("OOF    train/test AUC:", round(roc_auc_score(tr.y, oof), 3),
      round(roc_auc_score(te.y, te_apply(te.cat, enc, prior)), 3))     # 0.521 0.478
```

**Follow-ups:**
- *Why not just drop rare levels?* You can group them as "other"; smoothing does it softly.
- *Library option?* `sklearn.preprocessing.TargetEncoder` (since 1.3) does cross-fitted encoding inside `fit_transform`; use it inside a `Pipeline`.

**Common mistakes:** Encoding before the split, applying OOF to test (test should use full-train stats), no smoothing, and encoding inside CV by hand with the whole dataset.

### Q13 ⭐⭐⭐ 🟡 Implement AUC-ROC and average precision from scratch in NumPy (handle tied scores) and verify against sklearn.metrics.
**Asked at:** Product cos, GCC, ML-from-scratch coding rounds
**Say this first (1 line):** Sort by score, walk down the distinct thresholds collecting TP and FP counts (grouping ties into one point), then integrate ROC with the trapezoid rule and sum precision times recall increments for average precision.

**Then explain:**
- AUC-ROC = probability a random positive scores above a random negative (ties count half). Trapezoid over a tie group is a diagonal line, which gives exactly that half credit.
- Ties are the trap: handle thresholds on **distinct** scores, not on each row; otherwise the order of tied rows changes the answer.
- Average precision (sklearn's definition) = `sum((R_n - R_{n-1}) * P_n)`, a step-wise sum, not trapezoid, which would be optimistic.
- Cross-check with the rank (Mann-Whitney U) formula.
- Complexity: O(n log n) from the sort.

**Example (run):** 1,000 rows with 63 distinct scores (many ties). My AUC = sklearn AUC = 0.745972947862495; AP = 0.74857 in both.

**Code:**
```python
import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score

def _curve(y, s):
    y = np.asarray(y); s = np.asarray(s, dtype=float)
    order = np.argsort(-s, kind="mergesort")
    s, y = s[order], y[order]
    last = np.r_[np.where(np.diff(s))[0], len(s) - 1]     # last row of each tie group
    tp = np.cumsum(y)[last]
    fp = (last + 1) - tp
    return tp, fp

def auc_roc(y, s):
    tp, fp = _curve(y, s)
    tpr = np.r_[0, tp / tp[-1]]; fpr = np.r_[0, fp / fp[-1]]
    return np.trapezoid(tpr, fpr)

def avg_precision(y, s):
    tp, fp = _curve(y, s)
    prec, rec = tp / (tp + fp), tp / tp[-1]
    return np.sum(np.diff(np.r_[0, rec]) * prec)

rng = np.random.default_rng(0)
y = rng.integers(0, 2, 1000)
s = np.round(rng.normal(y * 0.8, 1), 1)                    # rounding creates ties
assert np.isclose(auc_roc(y, s), roc_auc_score(y, s))
assert np.isclose(avg_precision(y, s), average_precision_score(y, s))
```
(`np.trapezoid` is the NumPy 2 name; on older NumPy use `np.trapz`.)

**Follow-ups:**
- *Edge cases?* Only one class present -> undefined (division by zero); raise an error.
- *When prefer AP over ROC-AUC?* Rare positives; ROC-AUC can look great while precision is poor.

**Common mistakes:** One threshold per row (tie-order dependent), trapezoid for AP, forgetting the (0,0) start point, and using `argsort` that is not stable when you need reproducible output.

### Q14 ⭐⭐⭐ 🟡 A model shows 99% test accuracy. Given this broken notebook (fit_transform on test, duplicated rows across the split, an ID-like feature, a target-derived column), debug it step by step.
**Asked at:** Product cos, Microsoft IDC, GCCs, debug-this-code rounds
**Say this first (1 line):** 99% is a red flag, not a win; I remove leaks one at a time and watch the score fall to its honest level: fix preprocessing leakage, drop the target-derived column, drop the ID-like column, then deduplicate and split by entity.

**Then explain:**
- Step 0: check the baseline. With about 11% positives, "always negative" already gets about 89% accuracy, so judge with AUC.
- Step 1, target-derived column (`refund_flag`, only exists after churn): highest feature importance gives it away. Drop it, it would not exist at prediction time.
- Step 2, ID-like column (`row_id`): trees can use it to memorise row positions or time order. Drop it.
- Step 3, duplicated rows across the split plus `fit_transform` on test: deduplicate, then split by customer (`GroupKFold`), and fit transformers on train only (Pipeline).
- Sanity tools: feature importances, a shuffled-label test (the score should drop to chance), compare to a trivial baseline.

**Example (run):** random forest on synthetic data where the label has no true signal beyond the leaks.
| Stage | Accuracy | AUC |
|---|---|---|
| As-is | 0.990 | 0.977 |
| Drop target-derived | 0.898 | 0.862 |
| Drop ID-like | 0.889 | 0.697 |
| Dedupe + group split | 0.885 | 0.547 |

The final 0.547 AUC is the honest figure; accuracy 0.885 is no better than the 0.891 always-negative baseline. (The synthetic label is pure noise, so ideally AUC would be 0.5; the remainder is small-sample noise.) The data are synthetic and built to contain these leaks, so the exact numbers are illustrative; the pattern is the point.

**Code:**
```python
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
rng = np.random.default_rng(0)

# synthetic "broken notebook": 1500 customers x 4 rows, label is pure noise per customer
n_cust, per = 1500, 4
cid = np.repeat(np.arange(n_cust), per)
churn_c = (rng.random(n_cust) < 0.116).astype(int)                 # ~11% positives, no real signal
base = rng.normal(size=(n_cust, 3)).repeat(per, axis=0)            # customer-level traits (identify the customer)
df = pd.DataFrame(base + 0.3 * rng.normal(size=(n_cust * per, 3)), columns=["f1", "f2", "f3"])
df["customer_id"] = cid
df["churn"] = churn_c[cid]
df["refund_flag"] = ((df.churn == 1) & (rng.random(len(df)) < 0.9)).astype(int)   # only exists AFTER churn
df = pd.concat([df, df.sample(600, random_state=0)])               # exact duplicates
df = df.sample(frac=1, random_state=0).reset_index(drop=True)
df["row_id"] = df.groupby("customer_id").ngroup() + rng.normal(0, 5, len(df))     # ID-like column
print("positive rate:", df.churn.mean().round(3), "baseline acc:", (1 - df.churn.mean()).round(3))

def score(X, y, tr, te):
    rf = RandomForestClassifier(200, random_state=0, n_jobs=-1).fit(X.iloc[tr], y.iloc[tr])
    p = rf.predict_proba(X.iloc[te])[:, 1]
    return round(accuracy_score(y.iloc[te], p > 0.5), 3), round(roc_auc_score(y.iloc[te], p), 3)

y = df.churn
tr, te = train_test_split(np.arange(len(df)), test_size=0.25, random_state=0)      # random row split
cols_all = ["f1", "f2", "f3", "refund_flag", "row_id"]
Xs = pd.DataFrame(StandardScaler().fit_transform(df[cols_all]), columns=cols_all)  # BUG: scaler sees test rows
print("as-is           ", score(Xs, y, tr, te))                                    # (0.99, 0.977)
print("drop refund_flag", score(Xs.drop(columns="refund_flag"), y, tr, te))        # (0.898, 0.862)
print("drop row_id     ", score(Xs.drop(columns=["refund_flag", "row_id"]), y, tr, te))  # (0.889, 0.697)

# FIX: dedupe, split by customer, scale inside the training part only
d3 = df.drop_duplicates(subset=["f1", "f2", "f3", "customer_id", "churn"]).reset_index(drop=True)
tr, te = next(GroupShuffleSplit(1, test_size=0.25, random_state=0).split(d3, d3.churn, groups=d3.customer_id))
X3 = d3[["f1", "f2", "f3"]]
sc = StandardScaler().fit(X3.iloc[tr])
X3s = pd.DataFrame(sc.transform(X3), columns=X3.columns)
print("dedupe+group    ", score(X3s, d3.churn, tr, te), "baseline acc", round(1 - d3.churn.iloc[te].mean(), 3))  # (0.885, 0.547) 0.891
```

**Follow-ups:**
- *How to find a leaky feature fast?* One feature with absurdly high importance or single-feature AUC near 1.
- *Is a customer ID always bad?* It is not a feature; it is a grouping key for splitting.

**Common mistakes:** Celebrating before checking the baseline, removing only one leak, deduplicating after the split, and treating the ID as a feature "because it improves CV".

### Q15 ⭐⭐⭐ 🟡 Clean a messy CSV: mixed date formats, numeric columns stored as strings with currency symbols and commas, inconsistent category spellings, duplicates, and impossible values. Show your code and your checks.
**Asked at:** Product cos, GCC, live data-cleaning/take-home (Voleon, Pinterest reports)
**Say this first (1 line):** Read everything as strings, clean each column explicitly (strip symbols, parse, map categories), flag instead of silently fix impossible values, and finish with assertions that prove the cleaned frame is valid.

**Then explain:**
- Read with `dtype=str` so nothing is mangled on load.
- Prices: strip every non-digit/dot character, then `astype(float)`. Note Indian lakh formatting `1,00,000` is handled the same way. Currency itself (Rs, rupee symbol, $) should become a separate column if mixed currencies matter, never silently summed.
- Dates: `pd.to_datetime(format="mixed", errors="coerce")` and count the NaT. Ambiguous strings like `05/02/2025` are parsed month-first by default (May 2); agree on `dayfirst` with the data owner.
- Categories: strip, lowercase, then map through an explicit dictionary; unmapped values become NaN and get counted, not hidden.
- Impossible values (negative or >100 age): set to NaN and report the count.
- Checks: row counts before/after, key uniqueness, NaN counts, `describe()`.

**Example (run):** 7 raw rows -> 6 after removing 1 exact duplicate; 1 bad date (`not a date`), 2 impossible ages (-5 and 230), all 4 category spellings of "home and kitchen" collapsed to `home_kitchen`; `N/A` price becomes NaN.

**Code:**
```python
import numpy as np, pandas as pd, io
raw = io.StringIO('''order_id,order_date,price,qty,category,age
1,2025-01-05,"Rs 1,200.50",2,Electronics,34
2,05/02/2025,"₹ 99",1,electronics ,29
3,"March 3, 2025","2,450",1,ELECTRONICS,-5
4,2025-03-09,"₹1,00,000",1,Home & Kitchen,41
4,2025-03-09,"₹1,00,000",1,Home & Kitchen,41
5,2025-04-01,N/A,3,home and kitchen,230
6,not a date,"$ 15.5",1,Home-Kitchen,38
''')
d = pd.read_csv(raw, dtype=str)
n0 = len(d); d = d.drop_duplicates()
d["price"] = d.price.str.replace(r"[^\d.]", "", regex=True).replace("", np.nan).astype(float)
d["qty"] = pd.to_numeric(d.qty, errors="coerce")
d["age"] = pd.to_numeric(d.age, errors="coerce")
d["order_date"] = pd.to_datetime(d.order_date, format="mixed", errors="coerce")
cat_map = {"electronics": "electronics", "home & kitchen": "home_kitchen",
           "home and kitchen": "home_kitchen", "home-kitchen": "home_kitchen"}
d["category"] = d.category.str.strip().str.lower().map(cat_map)
bad_age = ~d.age.between(0, 100)
d.loc[bad_age, "age"] = np.nan
print(n0, "->", len(d), "| bad dates:", d.order_date.isna().sum(), "| impossible ages:", int(bad_age.sum()))
assert d.order_id.is_unique and d.category.notna().all()
```

**Follow-ups:**
- *Drop or fix impossible values?* Set to NaN and let the imputer/model handle it; dropping rows can bias the sample. Always report counts.
- *Duplicates that are not exact?* Define a business key and a keep-rule (latest, most complete).

**Common mistakes:** `pd.to_numeric` without cleaning (everything becomes NaN), silently coercing dates, fixing typos with ad-hoc `replace` calls and no unmapped-value check, and mixing currencies in one numeric column.

### Q16 ⭐⭐⭐ 🟡 Write a custom sklearn transformer (BaseEstimator, TransformerMixin) that clips outliers at train-set quantiles and works inside a Pipeline and GridSearchCV. What goes in fit vs transform?
**Asked at:** Product cos, MLE rounds, Zalando/Booking-type teams
**Say this first (1 line):** `__init__` only stores hyperparameters, `fit` learns the quantile bounds from training data and stores them with a trailing underscore, and `transform` only applies those stored bounds, so the transformer is safe in a `Pipeline` and `GridSearchCV`.

**Then explain:**
| Method | What goes in it |
|---|---|
| `__init__(lower, upper)` | just `self.lower = lower`, no logic, no validation; `GridSearchCV` uses `set_params`/`clone` |
| `fit(X, y=None)` | compute `lo_`, `hi_` from **train** data; return `self` |
| `transform(X)` | `np.clip(X, lo_, hi_)`; no refitting, no mutating the input |
- `TransformerMixin` gives `fit_transform` for free; `BaseEstimator` gives `get_params`/`set_params`.
- Learned attributes end with `_` and `check_is_fitted` guards against calling `transform` too early.
- Clipping at train quantiles means test outliers are capped at the training boundary, exactly like production.

**Example (run):** with outliers injected into feature 0 and `fit` on the first 400 rows (default 1%/99% quantiles), the bounds for feature 0 are about [-3.07, 3.26]; transforming the 100 unseen rows never exceeds 3.26 even though their raw max is 21.48.

**Code:**
```python
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted, check_array
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import make_classification

class QuantileClipper(BaseEstimator, TransformerMixin):
    def __init__(self, lower=0.01, upper=0.99):
        self.lower = lower; self.upper = upper
    def fit(self, X, y=None):
        X = check_array(X, dtype=float, ensure_all_finite=False)
        self.lo_ = np.nanquantile(X, self.lower, axis=0)
        self.hi_ = np.nanquantile(X, self.upper, axis=0)
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self, X):
        check_is_fitted(self, ["lo_", "hi_"])
        X = check_array(X, dtype=float, ensure_all_finite=False)
        return np.clip(X, self.lo_, self.hi_)
    def get_feature_names_out(self, input_features=None):
        return np.asarray(input_features, dtype=object)

X, y = make_classification(500, 5, random_state=0)
X[::50, 0] *= 30                                            # inject outliers
pipe = make_pipeline(QuantileClipper(), LogisticRegression(max_iter=1000))
gs = GridSearchCV(pipe, {"quantileclipper__upper": [0.9, 0.99, 0.999],
                         "quantileclipper__lower": [0.001, 0.1]}, cv=3).fit(X, y)
print(gs.best_params_, round(gs.best_score_, 3))   # lower 0.1, upper 0.9, 0.84
qc = QuantileClipper().fit(X[:400])                # learn bounds on the first 400 rows only
print(qc.lo_[0].round(2), qc.hi_[0].round(2),      # -3.07 3.26
      qc.transform(X[400:])[:, 0].max().round(2), X[400:, 0].max().round(2))   # 3.26 vs raw max 21.48
```
(`ensure_all_finite` is the sklearn >= 1.6 spelling; older versions call it `force_all_finite`.)

**Follow-ups:**
- *Why not clip in `__init__`?* `clone` re-runs `__init__` with the same params; logic there breaks `set_params`.
- *Why not compute quantiles in `transform`?* That would use test data (leak) and give different bounds per batch.

**Common mistakes:** Computing bounds in `transform`, forgetting `return self` in `fit`, mutating `X` in place, and putting derived values in `__init__`.

### Q17 ⭐⭐⭐ 🔴 Compute the pairwise Euclidean distance matrix and k-NN predictions for 10k x 50 data with no Python loops, using broadcasting and the (a-b)^2 expansion. Discuss memory and numerical issues.
**Asked at:** Product cos, Amazon India, MLE rounds
**Say this first (1 line):** Expand `||a-b||^2 = ||a||^2 - 2 a.b + ||b||^2`, so all distances come from one matrix multiplication plus two broadcasted norm vectors, then `argpartition` picks the k nearest without a full sort.

**Then explain:**
- Naive broadcasting `(A[:,None]-B[None])**2` builds an `n x m x d` tensor: for 1000 x 10000 x 50 float64 that is **4 GB**. The expansion form only makes an `n x m` matrix (80 MB here).
- Matrix multiply uses optimised BLAS, which is why this is fast. Cost O(n m d).
- Numerical issue: subtracting nearly equal large numbers (catastrophic cancellation) can give tiny negative squared distances or big relative error. Clip at 0 with `np.maximum`, and centre the data (subtract the mean) first; use float64 for safety.
- Memory: process queries in chunks (for example 250 rows at a time) so the distance block stays small.
- k-NN: `np.argpartition(D, k, axis=1)[:, :k]` is O(m) per row; sort only those k if you need order.

**Example (run):** 10,000 x 50 training points, 1,000 queries: 0.55 s on my laptop for the distance matrix, 80 MB, predictions agree 100% with sklearn brute-force k-NN. With a +1e8 offset on the data, the expansion form's relative error was about 3 (completely wrong; about 3e-16 when centred), because large numbers cancel. So centre your data.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
n, d = 10_000, 50
Xtr = rng.normal(size=(n, d)); ytr = (Xtr[:, 0] > 0).astype(int)
Xq = rng.normal(size=(1000, d))

def sqdist(A, B):
    d2 = (A**2).sum(1)[:, None] - 2 * A @ B.T + (B**2).sum(1)[None, :]
    return np.maximum(d2, 0)                       # rounding can give tiny negatives

def knn_predict(Q, T, yT, k=5, bs=250):            # chunked: bounded memory
    out = []
    for i in range(0, len(Q), bs):
        D = sqdist(Q[i:i + bs], T)
        idx = np.argpartition(D, k, axis=1)[:, :k]
        out.append((yT[idx].mean(1) > 0.5).astype(int))
    return np.concatenate(out)

pred = knn_predict(Xq, Xtr, ytr)
from sklearn.neighbors import KNeighborsClassifier
sk = KNeighborsClassifier(5, algorithm="brute").fit(Xtr, ytr).predict(Xq)
print((pred == sk).mean())                         # 1.0

import time
t = time.perf_counter(); D = sqdist(Xq, Xtr); print(round(time.perf_counter() - t, 2), "s,", D.nbytes // 10**6, "MB")  # ~0.55 s, 80 MB
exact = ((Xq[:5, None, :] - Xtr[None, :200, :]) ** 2).sum(-1)        # direct (slow, exact) distances for a small block
rel = lambda A, B: np.abs(sqdist(A, B) - exact).max() / exact.max()
print("rel err centred:", rel(Xq[:5], Xtr[:200]))                    # ~3e-16
print("rel err +1e8   :", rel(Xq[:5] + 1e8, Xtr[:200] + 1e8))        # ~3 (wrong): cancellation
```
(The outer loop is over chunks of queries, not per-sample Python loops.)

**Follow-ups:**
- *Ties/odd k?* Use odd k for binary classification; for ties in distance the result depends on `argpartition` order.
- *Scale beyond RAM?* ANN indexes (FAISS, HNSW) trade exactness for speed.

**Common mistakes:** Building the 3-D broadcast tensor, not clipping negatives before `sqrt`, a full `argsort` (O(m log m) per row), and ignoring chunking.

### Q18 ⭐⭐⭐ 🔴 Set up hyperparameter tuning with GridSearchCV/RandomizedSearchCV over a Pipeline and explain nested CV. Write code for an unbiased estimate of generalisation performance.
**Asked at:** Product cos, GCC, senior DS
**Say this first (1 line):** `GridSearchCV` over a Pipeline picks hyperparameters using inner CV, but the best inner score is optimistic because the same folds picked the winner; nested CV wraps the whole search inside an outer CV so the outer scores are an unbiased estimate.

**Then explain:**
- Inner loop: choose hyperparameters (e.g., `GridSearchCV`, or `RandomizedSearchCV` when the grid is big; it samples N settings, often almost as good, much cheaper).
- Outer loop: for each outer fold the search is re-run on the training part only, then scored on the held-out part, which never took part in selection.
- The search must contain the preprocessing (Pipeline), so scaling and so on are refit in every fold.
- Cost: outer_k x inner_k x grid size fits, so use `n_jobs` and smaller grids.
- The final model is refit on all data with the best params found by a normal `GridSearchCV`; the nested score only reports expected performance.

**Example (run):** noisy data (30 features, 3 informative, 30% label flips), SVC grid of 25 settings. The best inner CV AUC is **0.604**; the nested outer mean is **0.577** (scores 0.672, 0.453, 0.602, 0.621, 0.539). The gap is the selection optimism, and the spread across folds shows that this small dataset is noisy.

**Code:**
```python
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
X, y = make_classification(300, 30, n_informative=3, flip_y=0.3, random_state=0)
pipe = make_pipeline(StandardScaler(), SVC())
grid = {"svc__C": [0.01, 0.1, 1, 10, 100], "svc__gamma": [1e-4, 1e-3, 1e-2, 0.1, 1]}
inner = StratifiedKFold(5, shuffle=True, random_state=1)
outer = StratifiedKFold(5, shuffle=True, random_state=2)
gs = GridSearchCV(pipe, grid, cv=inner, scoring="roc_auc")
print("best inner:", round(gs.fit(X, y).best_score_, 3))          # 0.604 (optimistic)
nested = cross_val_score(gs, X, y, cv=outer, scoring="roc_auc")    # search re-run per outer fold
print(nested.round(3), nested.mean().round(3))                     # mean 0.577
```

**Follow-ups:**
- *Is nested CV always needed?* For model comparison on small data, yes; with a large separate test set a plain hold-out is enough.
- *Time series?* Use `TimeSeriesSplit` for both loops.

**Common mistakes:** Quoting `best_score_` as the generalisation estimate, searching on the test set, leaving preprocessing outside the Pipeline, and forgetting `random_state` on the splitters.

### Q19 ⭐⭐ 🟢 Reshape data: pivot_table, melt, stack/unstack and crosstab. Build a monthly cohort retention table from a signup and activity log.
**Asked at:** Product cos, growth/analytics DS (Swiggy, Spotify)
**Say this first (1 line):** Cohort retention is: tag every user with their signup month, compute each activity's month offset from signup, count distinct active users per (cohort, offset), and divide by cohort size.

**Then explain:**
- `pivot_table` aggregates and reshapes (wide); `melt` is the reverse (wide to long); `stack`/`unstack` move an index level between rows and columns; `crosstab` is a quick frequency table of two columns.
- Offset in months: `(year_act - year_signup) * 12 + (month_act - month_signup)`; do not subtract month numbers alone.
- Count `nunique` users, not events, or one busy user inflates retention.
- Month 0 should be 100% when the signup month has activity; divide by the cohort size from the users table (not from the activity table, which only has active users).

**Example (run):** Jan cohort has 3 users: month-0 active 3, month-1 active 1, month-2 active 1 -> retention 1.00, 0.33, 0.33. Feb cohort has 3 users: 1.00, 0.67, 0.00.

**Code:**
```python
import pandas as pd
users = pd.DataFrame({"user_id": range(6), "signup": pd.to_datetime(
    ["2025-01-03", "2025-01-20", "2025-01-25", "2025-02-02", "2025-02-10", "2025-02-15"])})
act = pd.DataFrame({"user_id": [0, 0, 1, 2, 2, 3, 3, 4, 5, 5], "ts": pd.to_datetime(
    ["2025-01-05", "2025-02-10", "2025-01-22", "2025-01-28", "2025-03-01",
     "2025-02-03", "2025-03-15", "2025-02-12", "2025-02-16", "2025-03-02"])})
a = act.merge(users, on="user_id")
a["cohort"] = a.signup.dt.to_period("M")
a["age_m"] = (a.ts.dt.year - a.signup.dt.year) * 12 + (a.ts.dt.month - a.signup.dt.month)
active = a.groupby(["cohort", "age_m"]).user_id.nunique().unstack(fill_value=0)
size = users.groupby(users.signup.dt.to_period("M")).user_id.nunique()
print(active.div(size, axis=0).round(2))
long = active.reset_index().melt(id_vars="cohort", var_name="age_m", value_name="active")   # back to long
```

**Follow-ups:**
- *Right-censoring?* Recent cohorts have fewer months observed; mask cells beyond today.
- *Retention by day/week?* Same code with `dt.days // 7` offset.

**Common mistakes:** Counting events instead of users, dividing by active users instead of cohort size, subtracting month numbers across year boundaries, and including cells that have not happened yet as 0.

### Q20 ⭐⭐ 🟢 Find and drop duplicates keeping the latest record per entity (sort_values + drop_duplicates vs groupby.tail/idxmax) and explain the differences.
**Asked at:** Product cos, GCC, pandas live rounds
**Say this first (1 line):** Sort by the timestamp and `drop_duplicates(subset, keep="last")` is the simplest way to keep the latest record; `groupby.idxmax` and `groupby.tail(1)` give similar results but differ on ties and NaN.

**Then explain:**
| Method | Ties | All-NaN timestamp group | Note |
|---|---|---|---|
| `sort_values(ts).drop_duplicates(id, keep="last")` | keeps the last in sort order | keeps the row | simple, O(n log n) |
| `groupby(id).ts.idxmax()` then `.loc` | first occurrence | group dropped/NaN | needs unique index |
| `sort_values(ts).groupby(id).tail(1)` | last in sort order | keeps | same as the first |
- Make ties deterministic: sort by `[ts, tiebreaker]` (e.g. an update sequence number), not just `ts`.
- Use a stable sort (`kind="stable"`) when you rely on the original row order for ties.

**Example (run):** id 2 has two rows at the same timestamp (values `c` and `d`) plus an older `e`. Sort+drop_duplicates keeps `d`; `idxmax` keeps `c`. id 3 has a missing timestamp: the sort approach keeps it, `idxmax` loses it.

**Code:**
```python
import pandas as pd
df = pd.DataFrame({"id": [1, 1, 2, 2, 2, 3],
                   "upd": pd.to_datetime(["2025-01-01", "2025-01-05", "2025-01-02", "2025-01-02", "2025-01-01", None]),
                   "v": list("abcdef")})
r1 = df.sort_values("upd", kind="stable").drop_duplicates("id", keep="last")
r2 = df.loc[df.groupby("id")["upd"].idxmax().dropna()]
r3 = df.sort_values("upd", kind="stable").groupby("id").tail(1)
print(r1.sort_values("id")[["id", "v"]].values.tolist())   # [[1,'b'], [2,'d'], [3,'f']]
print(r2.sort_values("id")[["id", "v"]].values.tolist())   # [[1,'b'], [2,'c']]
```

**Follow-ups:**
- *Which is fastest on big data?* Sort + drop_duplicates is usually fine; `idxmax` avoids a global sort but needs unique index handling.
- *Keep the full history instead?* Use `cumcount(ascending=False) == 0` flags.

**Common mistakes:** `drop_duplicates` with the default `keep="first"` after sorting ascending (keeps the oldest), no tiebreaker, and `idxmax` on a non-unique index.

### Q21 ⭐⭐ 🟡 Use pandas window-style operations per group: rank, cumsum, pct_change, lag/lead via shift, expanding and rolling aggregates. Compute 'days since previous order' and 'running spend'.
**Asked at:** Product cos, e-commerce, Amazon India
**Say this first (1 line):** I sort by customer and time, then use `groupby` with `diff`, `cumsum`, `shift`, `pct_change`, `rank`, and `transform` with `expanding`/`rolling` so every calculation restarts for each customer.

**Then explain:**
- Sort first (`sort_values(["cust", "ts"])`); window functions follow row order, not time.
- `groupby.diff()` on a datetime column gives a Timedelta; `.dt.days` turns it into a number. First order per customer is NaN (no previous order).
- `shift(1)` = previous value (lag), `shift(-1)` = next value (lead). Using lead as a feature is lookahead leakage, so use it only for labels.
- `cumsum` gives running spend; `pct_change` is change relative to the previous order; `rank(ascending=False)` ranks within customer.
- `rolling`/`expanding` through `transform(lambda s: ...)` keep the original row index; use `min_periods` to avoid early NaNs.

**Example (run):** Customer 1 orders on Jan 1, 10, 12 with amounts 100, 50, 70 -> days since previous: NaN, 9, 2; running spend 100, 150, 220; pct change NaN, -0.5, +0.4.

**Code:**
```python
import pandas as pd
o = pd.DataFrame({"cust": [1, 1, 1, 2, 2],
                  "ts": pd.to_datetime(["2025-01-01", "2025-01-10", "2025-01-12", "2025-01-03", "2025-01-04"]),
                  "amt": [100, 50, 70, 20, 30]}).sort_values(["cust", "ts"])
g = o.groupby("cust")
o["days_since_prev"] = g.ts.diff().dt.days
o["running_spend"] = g.amt.cumsum()
o["prev_amt"], o["next_amt"] = g.amt.shift(1), g.amt.shift(-1)
o["pct_chg"] = g.amt.pct_change()
o["rank_amt"] = g.amt.rank(ascending=False)
o["exp_mean"] = g.amt.transform(lambda s: s.expanding().mean())
o["roll2"] = g.amt.transform(lambda s: s.rolling(2, min_periods=1).mean())
print(o.to_string())
```

**Follow-ups:**
- *Is `running_spend` leaky as a feature?* It includes the current order; for a feature predicting the current order use `cumsum() - amt`.
- *Rolling by time instead of rows?* `rolling("7D", on="ts")` after setting the index.

**Common mistakes:** Not sorting, using `shift(-1)` as a feature, applying `rolling` to the whole frame so windows cross customers, and forgetting the first-row NaN.

### Q22 ⭐⭐ 🟡 Sessionize a clickstream: start a new session when the gap between consecutive events per user exceeds 30 minutes, using groupby, diff and cumsum.
**Asked at:** Swiggy/Flipkart/Spotify-type event data, product cos
**Say this first (1 line):** Within each user, sort by time, take the gap to the previous event with `diff`, flag a new session where the gap is missing or over 30 minutes, and `cumsum` the flags to get a session number.

**Then explain:**
- `diff()` is NaN on a user's first event; `isna() | (gap > 30min)` treats that as a session start too.
- `groupby(user)["flag"].cumsum()` numbers sessions per user; combine with the user id for a global session id.
- The boundary rule matters: "exceeds 30 minutes" means a gap of exactly 30 min stays in the same session (`>` not `>=`). State this assumption.
- Then session metrics are simple: `groupby("session_id")` for duration, event count, first/last event.
- Complexity: sort O(n log n), the rest O(n); fully vectorised, no Python loop.

**Example (run):** User `a` has events at 10:00, 10:20, 11:30, 11:40 and next day 09:00 -> sessions 1, 1, 2, 2, 3. User `b`: 10:00, 10:31 (31 min gap, new session), 10:40 -> 1, 2, 2.

**Code:**
```python
import pandas as pd
e = pd.DataFrame({"user": ["a"] * 5 + ["b"] * 3,
                  "ts": pd.to_datetime(["2025-01-01 10:00", "2025-01-01 10:20", "2025-01-01 11:30",
                                        "2025-01-01 11:40", "2025-01-02 09:00",
                                        "2025-01-01 10:00", "2025-01-01 10:31", "2025-01-01 10:40"])}
                 ).sort_values(["user", "ts"])
gap = e.groupby("user").ts.diff()
new = gap.isna() | (gap > pd.Timedelta("30min"))
e["session"] = new.groupby(e.user).cumsum()
e["session_id"] = e.user + "_" + e.session.astype(str)
print(e.groupby("session_id").ts.agg(["min", "max", "count"]))
```

**Follow-ups:**
- *Add a max session length too?* Also start a new session when `ts - session_start > 4h`; that needs a second pass or a loop.
- *Duplicate timestamps?* Gap is 0 so they stay together; fine.

**Common mistakes:** Not sorting, forgetting the first-event NaN, doing `cumsum` over the whole frame (session numbers do not restart, which is fine only if you combine with user id), and using `>=`.

### Q23 ⭐⭐ 🟡 Load a 5 GB CSV on an 8 GB laptop: use dtypes, category, usecols, chunksize, Parquet, and compare with Polars/DuckDB. Show memory before and after.
**Asked at:** Product cos, startups, GCC
**Say this first (1 line):** I never load it whole with default dtypes: I read only needed columns, use small dtypes and `category`, process in chunks or via an out-of-core engine, and convert to Parquet so later reads are fast and small.

**Then explain:**
- `usecols`: skip columns you do not need. `dtype`: `int32`/`int8`/`float32` instead of 64-bit; `category` for low-cardinality strings (stored as small integer codes).
- `chunksize`: stream the file and aggregate per chunk (works for sums, counts, group-bys where partial results can be combined).
- Parquet: columnar and compressed; you can read only the columns you need. Convert once, reuse many times.
- DuckDB (SQL over the file) and Polars (lazy `scan_csv`) are multithreaded and only read what the query needs, so they can handle data bigger than RAM for many queries.
- Measure with `df.memory_usage(deep=True)`; the `deep=True` matters for strings.

**Example (run, scaled down):** a synthetic 2M-row, 6-column, 96.5 MB CSV (generated in the code below).
| Approach | Result |
|---|---|
| default `read_csv` | **400 MB** in RAM (string columns are huge) |
| dtypes + category + `usecols` (4 columns) | **20 MB** |
| Parquet file (4 columns) | 14.5 MB on disk; reading 2 columns 0.86 s |
| Chunked sum over 500k-row chunks (float32) | 200,037,500 vs 200,037,515.84 for the full float64 load |
| DuckDB group-by straight on CSV / Polars lazy | 2.0 s / 1.1 s on my slow laptop (timings are machine-specific, not a benchmark) |

In this run default pandas used about 4x the CSV size in RAM. Extrapolation, not measured: a 5 GB CSV with the same shape could therefore want roughly 20 GB in RAM with default dtypes, which is why you plan before loading.

**Code:**
```python
import numpy as np, pandas as pd, duckdb, polars as pl      # duckdb/polars/pyarrow need pip install
rng = np.random.default_rng(0)
n = 2_000_000                                                # make a stand-in for the big file
pd.DataFrame({"user_id": rng.integers(0, 500_000, n),
              "country": rng.choice(["India", "Germany", "United States", "Brazil", "Japan"], n),
              "device": rng.choice(["android-phone", "ios-phone", "web-desktop"], n),
              "note": rng.choice(["promo applied", "no promo", "gift wrap requested", "none"], n),
              "amount": rng.gamma(2, 50, n).round(2),
              "qty": rng.integers(1, 6, n)}).to_csv("big.csv", index=False)

mb = lambda d: round(d.memory_usage(deep=True).sum() / 1e6)
a = pd.read_csv("big.csv"); print(mb(a))                                   # 400
dt = {"user_id": "int32", "country": "category", "amount": "float32", "qty": "int8"}
b = pd.read_csv("big.csv", dtype=dt, usecols=list(dt)); print(mb(b))      # 20
tot = sum(ch.amount.sum() for ch in pd.read_csv("big.csv", usecols=["amount"],
          dtype={"amount": "float32"}, chunksize=500_000))
print(tot, a.amount.sum())                                                 # 2.0003752e+08 vs 200037515.84
b.to_parquet("big.parquet")                                                 # needs pyarrow
print(duckdb.sql("select country, sum(amount) from 'big.csv' group by 1").df())
print(pl.scan_csv("big.csv").group_by("country").agg(pl.col("amount").sum()).collect())
```
(`float32` summing across chunks loses precision: the chunked total above is off from the float64 total by about 16 out of 200 million. Small here, but use `float64` for money.) On Windows, printing the Polars table may need `PYTHONIOENCODING=utf8` because of its box-drawing characters.

**Follow-ups:**
- *Chunking limits?* Anything needing all rows at once (median, joins, sorts) does not chunk directly; use DuckDB/Polars or a sample.
- *When Parquet vs CSV?* Always Parquet for repeated analytics; CSV only as an exchange format.

**Common mistakes:** Loading all columns as strings/float64, not using `deep=True`, using `float32` for money, and concatenating all chunks back into one frame (defeats the purpose).

### Q24 ⭐⭐ 🟡 Spot the bug: a function has a mutable default argument (def add_feature(df, cols=[])) and mutates its input DataFrame. Explain the symptom and fix it. Also show list-sharing and in-place mutation pitfalls in ML helper code.
**Asked at:** AI-code-review rounds, MLE loops
**Say this first (1 line):** A mutable default (`cols=[]`) is created once when the function is defined and shared by every call, and `df["new"] = ...` modifies the caller's DataFrame; fix with `cols=None` and work on a copy.

**Then explain:**
- Symptom: the list keeps growing across calls (`add_feature.__defaults__` becomes `(['new', 'new'],)`), and the caller's `df` suddenly has a new column.
- Why: default values are evaluated at definition time, not at each call. Passing a DataFrame into a function passes a reference, so in-place assignment changes the original.
- Fix: `cols=None` then `cols = [] if cols is None else list(cols)`; `out = df.copy()` (or `df.assign(...)`) and return `out`.
- Same family: `[[0]*3]*2` makes two references to one list; build with a comprehension. Also `df.sort_values(inplace=True)` inside helpers, and sharing `X_train` between experiments.
- Make mutation explicit in the name and the docstring, or return new objects (functional style); add a test that the input is unchanged.

**Example (run):** After `add_feature(d)` the caller's `d` has columns `['a', 'new']` although it never asked for it. The fixed version leaves `d` as `['a']` and returns a new frame with `['a', 'new']`.

**Code:**
```python
import pandas as pd
def add_feature(df, cols=[]):              # BUGGY
    cols.append("new")
    df["new"] = df.iloc[:, 0] * 2
    return df

def add_feature_ok(df, cols=None):         # FIXED
    cols = [] if cols is None else list(cols)
    out = df.copy()
    out["new"] = out.iloc[:, 0] * 2
    return out

d = pd.DataFrame({"a": [1, 2, 3]}); o = add_feature_ok(d)
print(list(d.columns), list(o.columns))    # ['a'] ['a', 'new']

grid = [[0] * 3] * 2; grid[0][0] = 1; print(grid)                       # [[1,0,0],[1,0,0]] shared row
grid = [[0] * 3 for _ in range(2)]; grid[0][0] = 1; print(grid)         # [[1,0,0],[0,0,0]]
```

**Follow-ups:**
- *Is `df.copy()` expensive?* It copies data; for huge frames use `assign` or document the in-place contract. With copy-on-write it is cheaper.
- *Where else do defaults bite?* Dataclasses (use `field(default_factory=list)`), `dict` defaults, class attributes.

**Common mistakes:** Thinking the default is re-created each call, fixing it with `if not cols: cols = []` (an empty list passed by the caller is replaced), and mutating inputs "for speed" without telling the caller.

### Q25 ⭐⭐ 🟡 Find the off-by-one / lookahead bug: labels are built with shift(-1) and rolling windows include the current day, so training features see the target. Fix it and add a test.
**Asked at:** Time-series/fintech loops, code-review rounds
**Say this first (1 line):** The label is built from the future, which is fine, but every feature must be computable using only information up to the prediction time; centred windows, forward returns, or windows that include the target day break that, so I fix the windows and add a perturbation test.

**Then explain:**
- Label for "tomorrow goes up" is `close.shift(-1) > close`, built on purpose with the future. The last row has no label (NaN), so drop it instead of letting `False` become 0.
- Leaks to look for: `rolling(5, center=True)` (sees future days); `shift(-1)` used in a feature; a feature built on the next day's return; fitting scalers on the whole series.
- Off-by-one: if you predict at today's close, a feature including today's close is allowed; if you predict at today's open it is not. Decide the prediction time and use `shift(1)` when in doubt.
- Test idea: corrupt all prices from day `t` onwards; features for rows before `t` must not change. A leaky feature fails the test.

**Example (run):** The test passes for `pct_change()` and `shift(1).rolling(5).mean()`, and fails for the centred rolling mean, because the corrupted future days change old rows.

**Code:**
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(0)
px = pd.DataFrame({"close": 100 + rng.normal(0, 1, 60).cumsum()})

# label: made from the future on purpose; last row stays NaN
y = (px.close.shift(-1) > px.close).astype(float).where(px.close.shift(-1).notna())

def good_feats(p):
    return pd.DataFrame({"ret_1": p.close.pct_change(), "ma5_prev": p.close.shift(1).rolling(5).mean()})
def bad_feats(p):
    return pd.DataFrame({"ma_c": p.close.rolling(5, center=True).mean()})   # sees the future

def test_no_lookahead(feats, t=30):
    corrupted = px.copy(); corrupted.loc[t:, "close"] += 1000
    pd.testing.assert_frame_equal(feats(px).iloc[:t], feats(corrupted).iloc[:t])

test_no_lookahead(good_feats)                       # passes
try:
    test_no_lookahead(bad_feats)
except AssertionError:
    print("buggy feature caught")
```

**Follow-ups:**
- *How else do you detect leakage?* Suspiciously high CV score, one dominant feature, or a score that collapses on a later out-of-time test set.
- *Embargo?* If the label spans several days, leave a gap between train and validation.

**Common mistakes:** Not knowing when the prediction is made, `center=True`, dropping NaN labels incorrectly (or turning them into 0), and random splits on time series.

### Q26 ⭐⭐ 🟡 Implement K-fold and stratified K-fold splitting from scratch in NumPy (seeded, no leakage) and check class proportions per fold.
**Asked at:** Product cos, ML-from-scratch rounds
**Say this first (1 line):** Shuffle the indices with a seeded generator, split into k nearly equal chunks with `np.array_split`, and use each chunk once as validation; for the stratified version I do this separately inside each class so every fold gets the same class proportion.

**Then explain:**
- K-fold guarantee: every row appears in validation exactly once and is never in train and validation of the same fold. Check both with asserts.
- Stratified: split each class's shuffled indices into k parts and merge part i of each class into fold i. Rotate which fold receives the larger parts so the extra rows do not pile up in fold 0.
- Use a `default_rng(seed)` object so results are reproducible without touching the global state.
- Class proportions per fold should be within one sample of the overall rate; plain k-fold can drift a lot with rare classes.

**Example (run):** 200 rows, 23 positives (11.5%). Plain 5-fold positive rates per fold: 0.075, 0.10, 0.15, 0.175, 0.075. Stratified: 0.10, 0.122, 0.125, 0.125, 0.103.

**Code:**
```python
import numpy as np

def kfold_idx(n, k, seed=0):
    idx = np.random.default_rng(seed).permutation(n)
    folds = np.array_split(idx, k)
    for i in range(k):
        yield np.concatenate(folds[:i] + folds[i + 1:]), folds[i]

def stratified_kfold_idx(y, k, seed=0):
    rng = np.random.default_rng(seed)
    folds = [[] for _ in range(k)]
    for c in np.unique(y):
        idx = rng.permutation(np.where(y == c)[0])
        for i, part in enumerate(np.array_split(idx, k)):
            folds[(i + c) % k].append(part)          # rotate so leftovers spread out
    folds = [np.concatenate(f) for f in folds]
    for i in range(k):
        yield np.concatenate(folds[:i] + folds[i + 1:]), folds[i]

y = np.r_[np.ones(23, int), np.zeros(177, int)]
for name, gen in [("plain", kfold_idx(200, 5)), ("strat", stratified_kfold_idx(y, 5))]:
    rates = []
    for tr, va in gen:
        assert not set(tr) & set(va) and len(tr) + len(va) == 200      # no leakage
        rates.append(round(float(y[va].mean()), 3))
    print(name, rates)
```
The strat rotation uses the class label `c` as an integer offset, which works for labels 0..K-1; map other labels first.

**Follow-ups:**
- *Why does fold size differ by one?* `array_split` gives the first `n % k` folds one extra item.
- *Stratified + groups?* Use `StratifiedGroupKFold`.

**Common mistakes:** Forgetting to shuffle sorted data, no seed, stratifying after the split, and not checking that fold union equals the full index set.

### Q27 ⭐⭐ 🟡 Implement numerically stable softmax, log-softmax and cross-entropy in NumPy (batch-wise), and show what breaks without the max-subtraction trick.
**Asked at:** Product cos, DL-leaning MLE rounds
**Say this first (1 line):** Subtract each row's maximum logit before exponentiating (the softmax does not change), and compute cross-entropy through log-softmax in log-sum-exp form instead of `log(softmax(z))`.

**Then explain:**
- `exp(1000)` overflows to `inf`, so naive softmax gives `inf/inf = nan`. After subtracting the max, the largest value is `exp(0)=1`, so nothing overflows and the denominator is at least 1.
- Softmax is shift-invariant: `exp(z-c)/sum(exp(z-c)) = exp(z)/sum(exp(z))`.
- The second failure is underflow: a tiny probability becomes exactly 0, `log(0) = -inf`, and the loss or gradient blows up. Log-softmax, `z - max - log(sum(exp(z - max)))`, never forms the tiny probability.
- Do it batch-wise with `axis=1, keepdims=True` so each row is handled independently.
- In frameworks, use the fused op (cross-entropy on logits, `log_softmax`) and never feed a softmax output into your own log.

**Example (run):** logits `[1000, 1001, 1002]`: naive gives `[nan, nan, nan]`, stable gives `[0.090, 0.245, 0.665]`. For logits `[0, -2000]`, naive `log(softmax)` gives `[0, -inf]`, stable gives `[0, -2000]`.

**Code:**
```python
import numpy as np

def softmax_naive(z):
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)

def log_softmax(z):
    z = z - z.max(axis=1, keepdims=True)           # shift: largest logit becomes 0
    return z - np.log(np.exp(z).sum(axis=1, keepdims=True))

def softmax(z):
    return np.exp(log_softmax(z))

def cross_entropy(z, y):                            # y = integer class labels
    return -log_softmax(z)[np.arange(len(y)), y].mean()

z = np.array([[1000., 1001., 1002.], [2., 1., 0.1]])
y = np.array([2, 0])
with np.errstate(all="ignore"):
    print("naive :", softmax_naive(z)[0])
print("stable:", softmax(z)[0])
print("CE    :", cross_entropy(z, y))
big = np.array([[0., -2000.]])
with np.errstate(all="ignore"):
    print("naive log:", np.log(softmax_naive(big))[0], " stable:", log_softmax(big)[0])
```
Output: `naive : [nan nan nan]`, `stable: [0.09003057 0.24472847 0.66524096]`, `CE : 0.4123...`, `naive log: [0. -inf] stable: [0. -2000.]`.

**Follow-ups:**
- *Gradient of softmax + CE?* `p - onehot(y)`, divided by batch size for the mean loss. Simple and stable, which is why the fused form is preferred.
- *Does the shift change the answer?* No, it is mathematically identical; it only changes floating-point behaviour.
- *Binary case?* Same idea: `log(1+exp(-x))` computed with `np.logaddexp(0, -x)`.

**Common mistakes:** Computing `np.log(softmax(z))`, subtracting the global max instead of the per-row max, forgetting `keepdims` (silent wrong broadcasting), and adding `1e-9` inside the log as a patch instead of fixing the formula.

### Q28 ⭐⭐ 🟡 Do feature selection correctly: this code runs SelectKBest on all data and then cross-validates. Show the leakage with random noise features and rewrite with a Pipeline.
**Asked at:** Product cos, healthcare/genomics-style DS, GCC
**Say this first (1 line):** Feature selection looks at the labels, so it must be fitted inside each training fold; if I run it before CV, the validation rows have already voted on which features to keep, and I get a fake high score even on pure noise.

**Then explain:**
- With 2,000 noise features and 100 rows, some features correlate with `y` by luck. `SelectKBest` on all rows picks exactly those, and CV then "confirms" them on rows that were used to pick them.
- The fix is structural: put the selector in a `Pipeline` so `cross_val_score` refits it on the training part of each fold only.
- Same rule for any supervised step: target encoding, label-aware dimensionality reduction, SMOTE, threshold tuning.
- Leakage is worst when features >> rows (genomics, text, wide logs).
- Good sanity check: shuffle `y` and see whether the full workflow still scores above chance. If it does, something leaks.

**Example (run):** random features and random labels, so the true AUC is 0.5. Leaky version: 0.881. Pipeline version: 0.540 (noise around 0.5).

**Code:**
```python
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(0)
X = rng.normal(size=(100, 2000))          # pure noise
y = rng.integers(0, 2, 100)               # random labels -> true AUC is 0.5
cv = StratifiedKFold(5, shuffle=True, random_state=0)

# WRONG: select on all rows, then CV
Xs = SelectKBest(f_classif, k=20).fit_transform(X, y)
bad = cross_val_score(LogisticRegression(), Xs, y, cv=cv, scoring="roc_auc").mean()

# RIGHT: selection is a pipeline step, refit inside every training fold
pipe = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression())
good = cross_val_score(pipe, X, y, cv=cv, scoring="roc_auc").mean()
print(f"leaky AUC {bad:.3f} | pipeline AUC {good:.3f}")
```

**Follow-ups:**
- *Is unsupervised selection (drop constant or highly correlated columns) also leaky?* Much less, since labels are not used, but fit it on train anyway for consistency.
- *What if I also tune `k`?* Put `k` in `GridSearchCV` over the pipeline; for an honest final estimate use nested CV.
- *Better alternatives?* L1-regularised models or tree importances inside the pipeline (`SelectFromModel`).

**Common mistakes:** Selecting features on the full dataset "just to explore" and then reporting CV, reporting the best score over many values of `k`, and checking only the final model instead of the whole workflow.

### Q29 ⭐⭐ 🟡 Handle class imbalance in code: class_weight vs RandomOverSampler/SMOTE inside an imblearn Pipeline and CV folds, and explain why resampling before the split is wrong.
**Asked at:** Fintech, fraud teams (PhonePe, Klarna)
**Say this first (1 line):** I try `class_weight` first because it is the cheapest, and if I resample, I do it inside an `imblearn` Pipeline so only the training part of each fold is resampled and the validation fold stays untouched and imbalanced.

**Then explain:**
- `class_weight="balanced"`: reweights the loss, adds no rows, has no leakage risk, and works in a normal sklearn pipeline.
- `RandomOverSampler`: duplicates minority rows. `SMOTE`: creates synthetic minority points by interpolating between neighbours (numeric features only, scale first; poor for categorical data).
- Why resampling before the split is wrong: copies of the same row land on both sides, so the model is scored on rows it has already seen. The validation set also no longer has the real class ratio.
- Resampling distorts predicted probabilities (over-confident for the minority). Recalibrate if probabilities matter, and judge on PR-AUC or recall at fixed precision, never accuracy.
- Often the better lever is threshold tuning and the right metric; resampling rarely improves ranking metrics.

**Example (run):** 3,000 rows, about 3% positives, 5-fold CV average precision. Logistic regression plain 0.274, balanced 0.200, SMOTE in pipeline 0.198. Random forest: resample before CV 1.000 (pure leakage), resample inside the pipeline 0.333.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.pipeline import Pipeline            # NOT sklearn's Pipeline

X, y = make_classification(n_samples=3000, n_features=20, n_informative=4,
                           weights=[0.97, 0.03], flip_y=0.02, random_state=0)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
def ap(m, Xx=X, yy=y):
    return cross_val_score(m, Xx, yy, cv=cv, scoring="average_precision").mean()

lr = LogisticRegression(max_iter=1000)
print("plain   ", round(ap(lr), 3))
print("balanced", round(ap(LogisticRegression(max_iter=1000, class_weight="balanced")), 3))
print("SMOTE   ", round(ap(Pipeline([("s", SMOTE(random_state=0)), ("m", lr)])), 3))

# WRONG: oversample first, then CV (duplicates leak into validation)
Xo, yo = RandomOverSampler(random_state=0).fit_resample(X, y)
rf = RandomForestClassifier(n_estimators=100, random_state=0)
print("RF resample BEFORE cv:", round(ap(rf, Xo, yo), 3))
print("RF resample in pipe  :", round(ap(Pipeline([("s", RandomOverSampler(random_state=0)), ("m", rf)])), 3))
```
Values come from my run with sklearn 1.8 and imblearn 0.14; they can shift slightly with versions.

**Follow-ups:**
- *Why imblearn's Pipeline?* Sklearn's Pipeline cannot call `fit_resample`; the imblearn one applies samplers only during `fit`, never at predict time.
- *Why did class weights not help AP here?* Reweighting mostly shifts the decision threshold; ranking quality (AP/AUC) changes little. That is a common, honest finding.
- *Other options?* Focal loss, undersampling the majority, cost-sensitive thresholds.

**Common mistakes:** Resampling before the split, evaluating on a resampled test set, using accuracy, and assuming SMOTE always helps.

### Q30 ⭐⭐ 🟡 Detect and cap outliers per group (IQR, z-score, winsorisation) in pandas and explain how doing it before the split can leak.
**Asked at:** Product cos, GCC
**Say this first (1 line):** I compute the bounds per group from the training data only, store them, and apply the same bounds to train, validation and live data; bounds computed on everything let the test rows influence what the model sees.

**Then explain:**
- IQR rule: cap at `Q1 - 1.5*IQR` and `Q3 + 1.5*IQR`. Robust, no normality assumption.
- Z-score rule: flag `|z| > 3`. Fragile, because outliers inflate the mean and std they are measured against; use it on roughly bell-shaped data.
- Winsorisation: clip to chosen percentiles (say 1% and 99%) instead of deleting rows.
- Per group matters when scales differ: a 500 order is normal in city B and extreme in city A, so a global rule flags the wrong group.
- Leak: bounds from the full data use test statistics, a mild but real leak. Fit bounds on train and `map` them onto any data. An unseen group gives NaN, so decide a fallback (for example a global bound).
- Capping is a modelling choice. If extremes are the signal (fraud), flag them as a feature instead of capping.

**Example (run):** 1,000 orders in two cities with 10 injected spikes. Train-fitted bounds: city A (-5.2, 45.9), city B (-34.5, 348.9). Capping touched 35 train rows and 19 test rows. Winsorising at 1%/99% brought the max from 1939 to 567.

**Code:**
```python
import numpy as np, pandas as pd

rng = np.random.default_rng(0)
df = pd.DataFrame({"city": rng.choice(["A", "B"], 1000)})
df["amt"] = np.where(df.city == "A", rng.lognormal(3, .5, 1000), rng.lognormal(5, .5, 1000))
df.loc[rng.choice(1000, 10, replace=False), "amt"] *= 8          # inject outliers

def fit_bounds(d, col="amt", by="city", k=1.5):
    q = d.groupby(by)[col].quantile([.25, .75]).unstack()
    iqr = q[.75] - q[.25]
    return pd.DataFrame({"lo": q[.25] - k * iqr, "hi": q[.75] + k * iqr})

def cap(d, b, col="amt", by="city"):
    lo, hi = d[by].map(b["lo"]), d[by].map(b["hi"])     # unseen group -> NaN -> no clipping
    return d[col].clip(lo, hi)

train, test = df.iloc[:700], df.iloc[700:]
b = fit_bounds(train)                                     # bounds from TRAIN only
print(b.round(1))
print("capped train:", int((cap(train, b) != train.amt).sum()),
      "test:", int((cap(test, b) != test.amt).sum()))

g = df.groupby("city")["amt"]                             # z-score flag, per group
z = (df.amt - g.transform("mean")) / g.transform("std")
print("z>3 flags:", df[z.abs() > 3].city.value_counts().to_dict())
w = g.transform(lambda s: s.clip(s.quantile(.01), s.quantile(.99)))
print("max before/after winsorise:", round(df.amt.max(), 1), round(w.max(), 1))
```
The last lines use the full data only to illustrate EDA. In a model, always go through `fit_bounds` on train.

**Follow-ups:**
- *Remove or cap?* Cap for model inputs; remove only clear data errors (negative age). Never drop outliers from the test set.
- *Do trees need this?* Trees are insensitive to feature outliers; linear models and distance methods are not.
- *Put it in a Pipeline?* Yes, as a custom transformer whose `fit` learns the bounds (see Q16).

**Common mistakes:** Global bounds on multi-scale data, computing quantiles on train+test, z-scores on heavy-tailed data, and dropping rows so features and labels misalign.

### Q31 ⭐⭐ 🟡 Make an experiment reproducible: control random_state in splits, models and np.random.default_rng, avoid global-state bugs, and explain why results still differ across machines or with n_jobs.
**Asked at:** MLE rounds, code-review rounds
**Say this first (1 line):** I set one seed at the top, pass it explicitly to every splitter and model, use a `default_rng` object instead of the global `np.random`, and accept that bit-for-bit equality across machines is not guaranteed because floating-point addition depends on the order of operations.

**Then explain:**
- Seed every random source: `train_test_split(random_state=)`, `KFold(shuffle=True, random_state=)`, each model's `random_state`, and any data generation. `random_state=None` means a different result every run.
- Prefer `rng = np.random.default_rng(seed)` and pass `rng` into functions. Global `np.random.seed` makes results depend on what else ran before, and any library call that draws numbers shifts it.
- For parallel work use `SeedSequence(seed).spawn(n)` so each worker gets an independent stream, not the same seed or overlapping seeds.
- `n_jobs`: for sklearn forests, each tree gets its seed up front, so `n_jobs` does not change results (I checked). For some libraries (GPU kernels, multithreaded boosting, parallel reductions) thread scheduling changes the order of float additions, so tiny differences appear.
- Across machines: different CPU, BLAS library (MKL vs OpenBLAS), thread count, library versions, or OS can change the last digits, and tree splits on near-ties can then flip. Pin versions, record the environment, and compare metrics with a tolerance, not with `==`.

**Example (run):** summing 1M float32 numbers in two different orders gives 998.57056 and 998.57074. Same data, different answer, because addition is not associative.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

SEED = 42
X, y = make_classification(500, 10, random_state=SEED)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.2, random_state=SEED, stratify=y)

def fit_score(n_jobs):
    m = RandomForestClassifier(100, random_state=SEED, n_jobs=n_jobs).fit(Xtr, ytr)
    return m.predict_proba(Xte)[:, 1]
print("RF n_jobs 1 vs 4 identical:", np.array_equal(fit_score(1), fit_score(4)))

children = [np.random.default_rng(s) for s in np.random.SeedSequence(SEED).spawn(3)]
print([round(c.random(), 4) for c in children])          # independent streams per worker

def noisy_bad(x): return x + np.random.normal(size=x.shape)      # hidden global state
def noisy_ok(x, rng): return x + rng.normal(size=x.shape)        # explicit generator
x = np.zeros(2)
np.random.seed(0); noisy_bad(x); np.random.rand(); b = noisy_bad(x)
np.random.seed(0); noisy_bad(x); b2 = noisy_bad(x)
print("global state: same call, different output:", not np.allclose(b, b2))

v = np.random.default_rng(0).normal(size=1_000_000).astype(np.float32)
s2 = v[np.random.default_rng(1).permutation(len(v))].sum()
print("float32 sum, two orders:", v.sum(), s2, "equal:", v.sum() == s2)
```
Output: `True`, `[0.9167, 0.4675, 0.0712]`, `True`, `998.57056 998.57074 equal: False`.

**Follow-ups:**
- *Is seeding enough for a deep-learning run?* No: also seed the framework, set deterministic kernels, and fix data-loader worker seeds; some GPU ops stay non-deterministic.
- *One seed or many?* For reporting, run several seeds and give mean and spread; a single lucky seed is not evidence.
- *Why `SeedSequence.spawn` and not seed+1, seed+2?* It is designed to give statistically independent streams.

**Common mistakes:** Seeding only the split, leaving `random_state=None` in a model, calling `np.random.seed` inside a library function, comparing floats with `==`, and picking the best seed after seeing the test score.

### Q32 ⭐⭐ 🟡 Save and load a trained pipeline with joblib, then write an inference function that validates columns, order, dtypes and unseen categories. What breaks in production if you only pickle the model?
**Asked at:** MLE rounds, Microsoft IDC, GCCs
**Say this first (1 line):** I save the whole fitted Pipeline (preprocessing and model together) plus metadata like column list and library version, and I wrap inference in a function that checks the input before calling `predict`; pickling only the model loses the preprocessing and every assumption about the input.

**Then explain:**
- `joblib.dump(pipeline, path)` stores the fitted imputer medians, scaler stats, encoder categories and model in one object, so train and serve apply identical transforms.
- If you pickle only the model, production must re-implement the encoding by hand, and any drift between the two versions silently gives wrong scores.
- Inference checks: required columns present, reorder to training order, drop extras, coerce dtypes (reject text in numeric columns), allow nulls only where the pipeline imputes them, `handle_unknown="ignore"` for unseen categories.
- Store the sklearn version; unpickling under another version can break or, worse, change behaviour. Pin versions in the serving image.
- Security: never `joblib.load` or `pickle.load` a file from an untrusted source, it can execute code.

**Example (run):** a record with reordered keys and an extra field scores fine; unseen city "Mumbai", income as string `"52000"` and a null age also scores (imputed, all-zero one-hot); a record missing `income` raises `missing columns: ['income']`; `age="abc"` raises a clear error.

**Code:**
```python
import tempfile, os, joblib, numpy as np, pandas as pd, sklearn
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

rng = np.random.default_rng(0)
df = pd.DataFrame({"age": rng.integers(18, 70, 300).astype(float),
                   "income": rng.lognormal(10, .5, 300),
                   "city": rng.choice(["Pune", "Delhi", "Oslo"], 300)})
y = (df.income > df.income.median()).astype(int)

NUM, CAT = ["age", "income"], ["city"]
pre = ColumnTransformer([("n", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), NUM),
                         ("c", OneHotEncoder(handle_unknown="ignore"), CAT)])
pipe = make_pipeline(pre, LogisticRegression(max_iter=500)).fit(df[NUM + CAT], y)

path = os.path.join(tempfile.gettempdir(), "model_v1.joblib")
joblib.dump({"pipeline": pipe, "columns": NUM + CAT, "sklearn": sklearn.__version__}, path)

def predict(records, path=path):
    art = joblib.load(path)
    if art["sklearn"] != sklearn.__version__:
        raise RuntimeError(f"trained on sklearn {art['sklearn']}, running {sklearn.__version__}")
    X = pd.DataFrame(records)
    missing = set(art["columns"]) - set(X.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    X = X[art["columns"]].copy()                              # fixes column order, drops extras
    for c in NUM:
        parsed = pd.to_numeric(X[c], errors="coerce")
        if (parsed.isna() & X[c].notna()).any():              # present but not a number, e.g. "abc"
            raise ValueError(f"column {c!r} has non-numeric values")
        X[c] = parsed                                         # real nulls stay NaN -> imputed
    X["city"] = X["city"].astype("string")
    return art["pipeline"].predict_proba(X)[:, 1]

print(predict([{"city": "Oslo", "income": 40000, "age": 30, "extra": 1}]))
print(predict([{"city": "Mumbai", "income": "52000", "age": None}]))
for bad in ([{"city": "Oslo", "age": 30}], [{"city": "Oslo", "age": "abc", "income": 1}]):
    try: predict(bad)
    except ValueError as e: print("rejected:", e)
```

**Follow-ups:**
- *joblib vs pickle?* Same security caveat; joblib is more efficient for large NumPy arrays.
- *Safer formats?* ONNX or skops for sharing models; they avoid arbitrary code execution on load.
- *What else belongs in the artifact?* Training date, data version, metrics, feature schema, and the decision threshold.

**Common mistakes:** Saving only the model, relying on column position instead of names, loading the model on every request, no version pinning, and assuming unseen categories "just work" without `handle_unknown`.

### Q33 ⭐⭐ 🟡 Join an events table to the most recent price/feature snapshot at or before each event time (merge_asof) without lookahead.
**Asked at:** Fintech, pricing teams, Booking
**Say this first (1 line):** Use `pd.merge_asof` with `direction="backward"` and `by=` the entity key; it attaches, to each event, the latest snapshot at or before the event time, so nothing from the future leaks in.

**Then explain:**
- Both tables must be sorted by the `on` key, otherwise pandas raises an error.
- `by="sym"` matches within the same entity (stock, user, product) before matching on time.
- `direction="backward"` is the leak-free choice. `"forward"` or `"nearest"` look into the future and are leakage for training features.
- `allow_exact_matches`: if a snapshot is stamped at the same instant as the event but is only published after it, set it to `False`.
- `tolerance`: a snapshot that is too old becomes NaN instead of a stale value. Keep the snapshot timestamp as a column so you can compute "age of feature".
- Real feature stores do the same "point-in-time join".

**Example (run):** Event A at 10:00:20 gets price 101.0 (snapshot 10:00:10), not 102.0 stamped 10:00:25, which is still in the future. Event B at 10:01:30 gets NaN because its latest snapshot is 30 s old and the tolerance is 15 s.

**Code:**
```python
import pandas as pd

events = pd.DataFrame({"ts": pd.to_datetime(["2024-01-01 10:00:05", "2024-01-01 10:00:20",
                                             "2024-01-01 10:01:30", "2024-01-01 09:59:00"]),
                       "sym": ["A", "A", "B", "A"], "qty": [10, 5, 7, 3]})
prices = pd.DataFrame({"ts": pd.to_datetime(["2024-01-01 10:00:00", "2024-01-01 10:00:10",
                                             "2024-01-01 10:01:00", "2024-01-01 10:00:25"]),
                       "sym": ["A", "A", "B", "A"], "px": [100.0, 101.0, 50.0, 102.0]})

events = events.sort_values("ts")                    # both sides sorted by the 'on' key
prices = prices.sort_values("ts").assign(px_ts=lambda d: d.ts)
out = pd.merge_asof(events, prices, on="ts", by="sym",
                    direction="backward",            # at or before the event: no lookahead
                    allow_exact_matches=True,        # False if the snapshot is published after its stamp
                    tolerance=pd.Timedelta("15s"))   # older than 15 s -> NaN
out["age_s"] = (out.ts - out.px_ts).dt.total_seconds()
print(out)
```
Output rows: (09:59:00, A) NaN; (10:00:05, A) 100.0, age 5 s; (10:00:20, A) 101.0, age 10 s; (10:01:30, B) NaN.

**Follow-ups:**
- *Why not a normal merge?* Timestamps rarely match exactly, and a plain merge on rounded times can pick a future row.
- *Sort error?* `merge_asof` needs sorted keys; with `by`, sort globally by the time column.
- *Publication delay?* Add the delay to the snapshot time (`available_at = ts + lag`) and join on `available_at`.

**Common mistakes:** Using `nearest` or `forward`, joining on a daily date when features are only final at end of day, no tolerance (stale values look fresh), and forgetting that the right table's timestamp may differ from when the data was actually available.

### Q34 ⭐⭐ 🟡 Use cross_validate with multiple scorers, a custom scorer (F-beta or a business-cost metric via make_scorer) and return train and validation scores to diagnose overfitting.
**Asked at:** Product cos, GCC
**Say this first (1 line):** `cross_validate` takes a dict of scorers and, with `return_train_score=True`, gives train and validation scores per fold; a big gap between them means overfitting, and a custom `make_scorer` lets me optimise a business cost instead of a generic metric.

**Then explain:**
- Scorers dict: `{"auc": "roc_auc", "f2": make_scorer(fbeta_score, beta=2), "cost": make_scorer(cost, greater_is_better=False)}`.
- F-beta with `beta=2` weights recall more than precision; use it when a miss is costlier than a false alarm.
- Business cost: put real money in a function (for example a missed fraud costs 50, a false alarm costs 5). sklearn always maximises scores, so `greater_is_better=False` flips the sign, and the reported values come out negative.
- Normalise cost per row so train and validation numbers are comparable (train folds are 4x larger than validation folds in 5-fold CV).
- Diagnosis: train high and validation much lower = overfit (more regularisation, simpler model, more data). Both low and close = underfit.

**Example (run):** 2,000 rows, 10% positive, 5-fold CV. Logistic regression: test AUC 0.831 vs train 0.848 (small gap, fine). Random forest, no depth limit: test AUC 0.864 vs train 1.000, and train cost 0.0 vs test cost 3.23 per row. Same test cost as logistic regression's 3.22, so the forest's AUC edge did not become business value at the default threshold.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import fbeta_score, make_scorer, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_validate

X, y = make_classification(2000, 20, n_informative=5, weights=[.9], flip_y=.05, random_state=0)
cv = StratifiedKFold(5, shuffle=True, random_state=0)

def cost(y_true, y_pred, c_fn=50, c_fp=5):          # a missed positive costs 10x a false alarm
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return (c_fn * fn + c_fp * fp) / len(y_true)    # cost per row, so train and val are comparable

scoring = {"auc": "roc_auc",
           "f2": make_scorer(fbeta_score, beta=2),
           "cost": make_scorer(cost, greater_is_better=False)}   # sign flipped: closer to 0 is better

for name, m in [("logreg", LogisticRegression(max_iter=1000)),
                ("rf(depth=None)", RandomForestClassifier(200, random_state=0))]:
    r = cross_validate(m, X, y, cv=cv, scoring=scoring, return_train_score=True)
    print(name, {k: round(float(np.mean(r[k])), 3) for k in r if k.startswith(("train_", "test_"))})
```

**Follow-ups:**
- *Scorer for probabilities (log-loss, Brier)?* Use the built-in `"neg_log_loss"` or `"neg_brier_score"`; they score predicted probabilities.
- *Why not just tune the threshold?* Better: fit the threshold on out-of-fold probabilities to minimise cost, then freeze it for the test set.
- *Why report the std across folds?* A gain smaller than the fold-to-fold spread is noise.

**Common mistakes:** Forgetting the sign flip (reading -3.2 as "bad"), comparing summed train and validation costs, scoring with accuracy on imbalanced data, and tuning on the same CV folds used for the final estimate.

### Q35 ⭐⭐ 🟡 Review LLM-generated pandas code that uses inplace=True, chained indexing, apply(axis=1), a hidden copy and silent dtype coercion. Point out correctness and performance bugs and rewrite it.
**Asked at:** AI-code-review rounds (2026)
**Say this first (1 line):** The code has four problems: `inplace=True` and chained indexing that silently do nothing or write to a copy, a global `fillna(0)` that invents fake values, a row-wise `apply` that is slow, and unchecked type coercion; I would rewrite it with explicit assignments and vectorised operations.

**Then explain (the buggy snippet, which I ran):**
```python
d = df.copy()
d["price"] = pd.to_numeric(d["price"], errors="coerce")
d.fillna(0, inplace=True)                                  # 1
d[d.qty > 1]["flag"] = 1                                   # 2
d["total"] = d.apply(lambda r: r["price"] * r["qty"], axis=1)   # 3
d["region"].replace({"N": "North"}, inplace=True)          # 4
```
- Bug 1 (correctness): `errors="coerce"` turned the bad price `"x"` into NaN, then `fillna(0)` turned it into a price of 0. The model now sees a free item, and the missing-ness is lost. Keep NaN, add an `is_missing` flag, and impute later using train statistics only.
- Bug 2 (correctness): `d[mask]["flag"] = 1` assigns into a temporary copy. In my run the `flag` column was never created. Use `d["flag"] = (d.qty > 1).astype("int8")` or `d.loc[mask, "flag"] = 1`.
- Bug 3 (performance): `apply(axis=1)` runs a Python function per row, around 10 to 100 times slower than `d.price * d.qty` (see Q5).
- Bug 4: `inplace=True` on `d["region"]` works on a temporary object. In pandas 2.3 it still happened to change the frame (with a FutureWarning), but under copy-on-write (default in pandas 3) it does nothing. Assign back: `d["region"] = d["region"].replace(...)`.
- Dtype coercion: `to_numeric(errors="coerce")` hides bad data. Count how many values failed and raise or log if it is more than a threshold.
- `inplace=True` rarely saves memory and breaks method chaining; avoid it.

**Example (run):** buggy output has no `flag` column and price of the bad row is 0.0; the fixed version gives price NaN, `total` NaN, `price_missing=True`.

**Code (fixed):**
```python
import numpy as np, pandas as pd

df = pd.DataFrame({"id": [1, 2, 3, 4], "price": ["10", "20", "x", "40"],
                   "qty": [1, 2, 3, 4], "region": ["N", "S", "N", "S"]})
f = df.assign(price=pd.to_numeric(df["price"], errors="coerce"))
f["price_missing"] = f["price"].isna()                    # keep the information
f["flag"] = (f["qty"] > 1).astype("int8")                  # one explicit assignment
f["total"] = f["price"] * f["qty"]                         # NaN stays NaN
f["region"] = f["region"].replace({"N": "North"})          # assign back
print(f)
```

**Follow-ups:**
- *How do you review LLM pandas code in general?* Run it on a tiny frame, check row count, dtypes, NaN counts before and after, and compare against a hand-computed answer.
- *`.loc` vs chained?* One `.loc[row_mask, col] = value` call is a single, defined operation.
- *Would `copy()` fix a hidden copy?* Only if you then keep and use the copy; the real fix is to assign to the object you keep.

**Common mistakes:** Trusting that the code "ran without error", silencing warnings instead of fixing them, filling NaN with 0 globally, and not checking shape and dtypes after each step.

### Q36 ⭐⭐ 🟡 Compute running mean, variance and moving average in NumPy efficiently (cumsum, convolve, Welford's one-pass algorithm) and discuss catastrophic cancellation.
**Asked at:** MLE rounds, product cos
**Say this first (1 line):** A running mean and a moving average use `cumsum` (one pass, O(n)) or `np.convolve`, and for variance I use Welford's one-pass update, not the `E[x^2] - E[x]^2` shortcut, because that shortcut subtracts two huge nearly equal numbers and loses all precision.

**Then explain:**
- Running mean: `cumsum(x) / arange(1, n+1)`.
- Moving average with window `w`: `(cs[w-1:] - cs[:-w] with a leading 0) / w`, or `np.convolve(x, np.ones(w)/w, mode="valid")`. Convolve is O(n*w) in direct form but simple and accurate; the cumsum trick is O(n) but its running total grows, so rounding error accumulates on long, large-magnitude series.
- Welford: keep `n`, `mean`, `M2`. For each value: `d = v - mean; mean += d/n; M2 += d*(v - mean)`; variance is `M2/(n-1)`. Works on streams, needs O(1) memory, and is stable.
- Catastrophic cancellation: subtracting two nearly equal floats leaves only the noisy low digits. In `sum(x^2) - sum(x)^2/n` both terms are about 1e23 when x is about 1e9, while the true answer is about 1e5.
- Cheap fix for the shortcut: subtract a shift (for example the first value) before squaring.

**Example (run):** 100,000 values from a normal distribution with mean 1e9 and true variance about 1. Two-pass `np.var`: 1.00027. Welford: 1.00027. Naive shortcut: 335.5 (completely wrong). The cumsum and convolve moving averages differ by up to 0.006 on this data.

**Code:**
```python
import numpy as np

rng = np.random.default_rng(0)
x = rng.normal(1e9, 1.0, 100_000)                    # big mean, small spread (true var ~ 1)

cs = np.cumsum(x)
run_mean = cs / np.arange(1, len(x) + 1)             # running mean, O(n)

w = 7                                                # moving average, window w
ma_cumsum = (cs[w - 1:] - np.r_[0, cs[:-w]]) / w
ma_conv = np.convolve(x, np.ones(w) / w, mode="valid")
print("moving avg agree:", np.allclose(ma_cumsum, ma_conv))

def welford(a):
    n, mean, m2 = 0, 0.0, 0.0
    for v in a:                                      # one pass, numerically stable
        n += 1
        d = v - mean
        mean += d / n
        m2 += d * (v - mean)
    return mean, m2 / (n - 1)

naive_var = (np.sum(x**2) - np.sum(x)**2 / len(x)) / (len(x) - 1)
print("two-pass:", np.var(x, ddof=1))
print("welford :", welford(x)[1])
print("naive   :", naive_var)
print("max |cumsum MA - conv MA|:", np.abs(ma_cumsum - ma_conv).max())
```
The loop-based Welford is slow in pure Python; in practice use `np.var` on arrays, and Welford (or Chan's parallel merge) for streams or chunks.

**Follow-ups:**
- *How do you combine variances from chunks?* Chan's formula merges `(n, mean, M2)` triples; this is how `StandardScaler.partial_fit` works.
- *Why does `np.var` do well?* It subtracts the mean first (two-pass) and uses pairwise summation.
- *Exponential moving average?* `ema_t = a*x_t + (1-a)*ema_{t-1}`; pandas `ewm`.

**Common mistakes:** Using `E[x^2]-E[x]^2` on large-offset data, forgetting `ddof=1` for sample variance, off-by-one in the cumsum window, and assuming float32 is enough for long cumulative sums.

### Q37 ⭐⭐ 🟡 Handle a high-cardinality categorical feature (10k levels) in sklearn: frequency encoding, hashing, OrdinalEncoder with unknown_value, native categorical support in HistGradientBoosting. Write code and compare.
**Asked at:** Product cos, e-commerce
**Say this first (1 line):** For 10k levels I never one-hot encode; I pick between frequency encoding, hashing, target encoding (cross-fitted), or native categorical support after grouping rare levels, and I compare them with CV on the actual data.

**Then explain:**
- One-hot with 10k levels creates 10k columns, mostly zeros; fine for linear models with sparse output, bad for trees.
- Frequency encoding: replace the level by its train frequency. Simple, handles unseen levels (0), but loses level identity (two levels with equal counts look the same).
- Hashing (`FeatureHasher`): map levels into a fixed number of buckets. Fixed size, no vocabulary to store, but collisions mix levels together.
- `OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)`: integer codes. Trees can use them but the order is arbitrary, so splits are crude.
- `TargetEncoder` (sklearn 1.3+): encodes by the target mean with smoothing, and `fit_transform` uses internal cross-fitting so the training rows do not see their own label. Usually strongest on high cardinality.
- Native categorical in `HistGradientBoosting`: **limited to 255 levels** per feature (I tested: 10k levels raises a ValueError). The fix is to keep the top 254 levels from train and bucket the rest as "other".
- Premise note: my synthetic data has a 10k-level universe but a skewed draw, so only 2,589 levels actually appear in 20k rows; the ranking of methods is what matters, not the exact scores.

**Example (run):** 5-fold CV AUC, `HistGradientBoostingClassifier` as the model: frequency 0.800, hashing(64) 0.796, ordinal 0.793, target encoder 0.814, native with top-254 + other 0.812. Differences are small; target encoding and native-with-grouping are best here, and the cost of getting it wrong is leakage, not AUC.

**Code:**
```python
import numpy as np, pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.feature_extraction import FeatureHasher
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, OrdinalEncoder, TargetEncoder

rng = np.random.default_rng(0)
n, L = 20_000, 10_000
lvl = rng.zipf(1.3, n) % L                             # skewed: few common levels, long tail
eff = rng.normal(0, 1.5, L)                            # each level has its own true effect
x1 = rng.normal(size=n)
y = (rng.random(n) < 1 / (1 + np.exp(-(eff[lvl] + x1 - 1)))).astype(int)
df = pd.DataFrame({"x1": x1, "cat": "L" + pd.Series(lvl).astype(str)})
cv = StratifiedKFold(5, shuffle=True, random_state=0)
def auc(pipe): return round(cross_val_score(pipe, df, y, cv=cv, scoring="roc_auc").mean(), 3)
hgb = lambda **kw: HistGradientBoostingClassifier(random_state=0, **kw)

class Freq:                                            # frequency encoding, fit on train only
    def fit(self, X, y=None): self.m_ = X.iloc[:, 0].value_counts(normalize=True); return self
    def transform(self, X): return X.iloc[:, 0].map(self.m_).fillna(0).to_frame()
    def get_params(self, deep=True): return {}
    def set_params(self, **p): return self
    def fit_transform(self, X, y=None): return self.fit(X).transform(X)
    def set_output(self, **k): return self

def with_pre(cat_tf):
    return make_pipeline(ColumnTransformer([("c", cat_tf, ["cat"])], remainder="passthrough"), hgb())

print("frequency      ", auc(with_pre(Freq())))
hasher = FunctionTransformer(lambda X: FeatureHasher(64, input_type="string")
         .transform(X.iloc[:, [0]].astype(str).values.tolist()).toarray())
print("hashing (64)   ", auc(with_pre(hasher)))
print("ordinal+unknown", auc(with_pre(OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))))
print("target (sklearn)", auc(with_pre(TargetEncoder(random_state=0))))

try:                                                   # native categorical: max 255 levels
    d2 = df.assign(cat=df.cat.astype("category"))
    HistGradientBoostingClassifier(categorical_features="from_dtype").fit(d2, y)
except Exception as e: print("native, all levels ->", type(e).__name__)

class TopK(BaseEstimator, TransformerMixin):          # keep 254 most frequent TRAIN levels, rest -> "other"
    def fit(self, X, y=None):
        self.keep_ = X["cat"].value_counts().index[:254]
        self.cats_ = list(self.keep_) + ["other"]
        return self
    def transform(self, X):
        c = X["cat"].where(X["cat"].isin(self.keep_), "other")
        return X.assign(cat=pd.Categorical(c, categories=self.cats_))
print("native top-254+other", auc(make_pipeline(TopK(), hgb(categorical_features="from_dtype"))))
```
This takes a few minutes on my laptop (machine-specific), mostly from the 5-fold target encoder and boosting.

**Follow-ups:**
- *Why does naive target encoding leak?* Each row's own label is in its category mean; with rare levels the encoding nearly equals the label (see Q12).
- *When is hashing right?* Streaming or huge vocabularies where storing a dictionary is costly, and with linear models on sparse text-like features.
- *Embeddings?* For neural models, learn a dense vector per level; rare levels share an "unknown" vector.

**Common mistakes:** One-hot on 10k levels with trees, target encoding without cross-fitting, learning the frequency map on all data, no plan for unseen levels at serving time, and assuming native categorical support has no cardinality limit.

### Q38 ⭐⭐ 🟡 Write a data-validation function for incoming scoring data (schema, ranges, null rates, PSI drift vs training) that raises clear errors before the model is called.
**Asked at:** MLE rounds, GCCs, Zalando/Booking-type teams
**Say this first (1 line):** I write one `validate()` that runs before the model, checks schema, dtypes, ranges, null rates, unseen categories and drift (PSI against training), collects every problem, and raises one clear error instead of letting bad data produce a quiet wrong score.

**Then explain:**
- Schema: required columns exist; numeric columns are really numeric.
- Ranges and nulls: min/max from domain knowledge or training quantiles, plus a maximum null rate per column.
- Categories: values never seen in training are reported (the encoder may ignore them, but a spike is a data-pipeline signal).
- PSI (population stability index): bin the training values into deciles, compare the share of the new batch falling in each bin. `PSI = sum((a - e) * ln(a / e))`. Rule of thumb: below 0.1 stable, 0.1 to 0.25 moderate shift, above 0.25 large shift. It is a rule of thumb, not a statistical test, and needs enough rows per batch.
- Collect all errors in a list so the on-call person sees everything at once. Decide per check whether to reject (schema, ranges) or only alert (drift).
- Keep bin edges and the reference spec saved with the model so the check is the same in production.

**Example (run):** clean batch: passes. Corrupted batch: `age: null rate 10.0% > 5%; age: 12 values outside [18, 90]; age: PSI 2.98 > 0.25; city: unseen categories ['C']`.

**Code:**
```python
import numpy as np, pandas as pd

class DataValidationError(ValueError):
    pass

def psi(expected, actual, bins=10):
    edges = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))   # bins from TRAINING data
    edges[0], edges[-1] = -np.inf, np.inf
    e = np.histogram(expected, edges)[0] / len(expected)
    a = np.histogram(actual, edges)[0] / len(actual)
    e, a = np.clip(e, 1e-4, None), np.clip(a, 1e-4, None)                    # avoid log(0)
    return float(np.sum((a - e) * np.log(a / e)))

def validate(df, spec, train_ref=None, psi_max=0.25):
    errs = []
    missing = [c for c in spec if c not in df.columns]
    if missing:
        raise DataValidationError(f"missing columns: {missing}")
    for c, s in spec.items():
        col = df[c]
        if s["kind"] == "num" and not pd.api.types.is_numeric_dtype(col):
            errs.append(f"{c}: expected numeric, got {col.dtype}"); continue
        rate = col.isna().mean()
        if rate > s["max_null"]:
            errs.append(f"{c}: null rate {rate:.1%} > {s['max_null']:.0%}")
        if s["kind"] == "num":
            bad = ((col < s["min"]) | (col > s["max"])).sum()
            if bad: errs.append(f"{c}: {bad} values outside [{s['min']}, {s['max']}]")
            if train_ref is not None and col.notna().sum() >= 200:
                p = psi(train_ref[c].dropna().to_numpy(), col.dropna().to_numpy())
                if p > psi_max: errs.append(f"{c}: PSI {p:.2f} > {psi_max}")
        elif s["kind"] == "cat":
            unseen = set(col.dropna()) - set(s["allowed"])
            if unseen: errs.append(f"{c}: unseen categories {sorted(unseen)[:5]}")
    if errs:
        raise DataValidationError("; ".join(errs))
    return df

rng = np.random.default_rng(0)
train = pd.DataFrame({"age": rng.normal(40, 10, 5000).clip(18, 90), "city": rng.choice(["A", "B"], 5000)})
spec = {"age": {"kind": "num", "min": 18, "max": 90, "max_null": .05},
        "city": {"kind": "cat", "allowed": ["A", "B"], "max_null": 0}}

ok = pd.DataFrame({"age": rng.normal(40, 10, 1000).clip(18, 90), "city": rng.choice(["A", "B"], 1000)})
validate(ok, spec, train); print("clean batch passed")
bad = pd.DataFrame({"age": np.r_[rng.normal(60, 10, 990), [-5] * 10].clip(-5, 120),
                    "city": rng.choice(["A", "B", "C"], 1000)})
bad.loc[:99, "age"] = np.nan
try: validate(bad, spec, train)
except DataValidationError as e: print("rejected:", e)
```

**Follow-ups:**
- *PSI vs KS test?* KS gives a p-value but flags tiny, harmless shifts on big samples; PSI gives an effect size that is easier to threshold.
- *Existing tools?* Pandera or Great Expectations for declarative schemas; the logic is the same.
- *Reject or alert on drift?* Usually alert (the model may still be fine); reject on schema and range violations.

**Common mistakes:** Validating after the model has already run, deriving PSI bins from the new batch instead of training, computing PSI on tiny batches, stopping at the first error, and letting `pd.to_numeric(errors="coerce")` hide bad values.

### Q39 ⭐⭐ 🔴 Debug this 'works on my machine' sklearn notebook: results change after reordering columns, a ColumnTransformer silently drops a column (remainder), and get_feature_names_out fails. Fix it.
**Asked at:** MLE rounds, code-review rounds
**Say this first (1 line):** Three separate bugs: positional column selection and raw arrays make results depend on column order, `remainder="drop"` (the default) silently throws away any column I forgot, and custom or function steps do not declare output names, so `get_feature_names_out` fails; the fix is names everywhere, an explicit completeness check, and `feature_names_out`.

**Then explain:**
- Reordering: select columns by name, not by position (`["age", "income"]`, not `[0, 1]`). Modern sklearn keeps column names from a DataFrame and checks them, so DataFrame reordering is mostly caught or handled. The silent failure appears when someone passes `.values` / `.to_numpy()` to `fit` or `predict`: the names are gone and column 0 is simply column 0.
- Silent drop: `ColumnTransformer` drops every column not listed (`remainder="drop"`). A forgotten `tenure` produces no warning, only a worse model. Either list every column, set `remainder="passthrough"` deliberately, or assert that the used columns equal the input columns.
- Feature names: `FunctionTransformer(np.log1p)` gives no output names. Pass `feature_names_out="one-to-one"` (or a function). Custom transformers need `get_feature_names_out`, or inherit `OneToOneFeatureMixin`.
- Debug order I follow: print `get_feature_names_out()` first, compare to the expected list, then check order-dependence with a shuffled-column copy, then check the array path.

**Example (run):** buggy transformer uses `['num__age', 'num__income', 'cat__city_A', 'cat__city_B']`, so `tenure` is gone with no warning. Fixed one uses `['num__age', 'num__tenure', 'log__income', 'cat__city_A', 'cat__city_B']`. With raw arrays, accuracy drops from 0.99 to 0.50 when I swap the two columns at predict time; a DataFrame with swapped columns gives identical predictions.

**Code:**
```python
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

rng = np.random.default_rng(0)
df = pd.DataFrame({"age": rng.normal(40, 10, 200), "income": rng.lognormal(10, .5, 200),
                   "tenure": rng.integers(0, 10, 200).astype(float), "city": rng.choice(["A", "B"], 200)})
y = (df.income > df.income.median()).astype(int)

# --- buggy: positional selection, silent drop of 'tenure', custom step without names ---
bad = ColumnTransformer([("num", StandardScaler(), [0, 1]), ("cat", OneHotEncoder(), [3])])
make_pipeline(bad, LogisticRegression()).fit(df, y)
print("buggy uses:", bad.get_feature_names_out().tolist())          # tenure is missing, no warning
ct = ColumnTransformer([("l", FunctionTransformer(np.log1p), ["income"])]).fit(df)
try: ct.get_feature_names_out()
except AttributeError as e: print("names fail:", str(e)[:60])

# --- fixed: names, explicit names for custom steps, handle_unknown, completeness check ---
NUM, CAT = ["age", "tenure"], ["city"]
good = ColumnTransformer(
    [("num", StandardScaler(), NUM),
     ("log", FunctionTransformer(np.log1p, feature_names_out="one-to-one"), ["income"]),
     ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)], remainder="drop")
pipe = make_pipeline(good, LogisticRegression()).fit(df, y)
print("fixed uses:", good.get_feature_names_out().tolist())
used = {c for _, _, cols in good.transformers_ if cols != "drop" for c in cols}
assert used == set(df.columns), set(df.columns) - used             # fail loudly if a column is unhandled
swapped = df[["income", "age", "tenure", "city"]]
print("DataFrame reorder safe:", np.allclose(pipe.predict_proba(df)[:, 1], pipe.predict_proba(swapped)[:, 1]))

# --- reorder bug that really bites: raw arrays carry no names ---
num = df[["age", "income"]]
m = make_pipeline(StandardScaler(), LogisticRegression()).fit(num.to_numpy(), y)
sw = num[["income", "age"]].to_numpy()
print("array acc original / reordered:", (m.predict(num.to_numpy()) == y).mean(), (m.predict(sw) == y).mean())
```
Note on the premise: in sklearn 1.8 a DataFrame with reordered columns did not change my predictions for a `ColumnTransformer`; the damaging case is arrays. If a notebook really changes with reordering, look for `.values`, positional indices, or an old sklearn.

**Follow-ups:**
- *Why not `remainder="passthrough"` always?* It can pass IDs or target-derived columns into the model; list columns on purpose.
- *`set_output(transform="pandas")`?* Keeps DataFrames and names through the pipeline (see Q51).
- *Name collisions?* `verbose_feature_names_out=True` (default) prefixes each name with its transformer to avoid clashes.

**Common mistakes:** Passing `.values` into pipelines, trusting the default `remainder`, never printing the final feature list, and hard-coding column indices from an old notebook.

### Q40 ⭐⭐ 🔴 Given an LLM-written function to compute precision@k and NDCG@k, find the off-by-one, ties and empty-group bugs, fix it and write tests with known answers.
**Asked at:** Search/recsys teams, AI-code-review rounds
**Say this first (1 line):** The usual bugs are sorting ascending instead of descending, ranks starting at 0 so `log2(0 + 1) = 0`, an unstated choice for groups with fewer than `k` items (divide by `k` or by the number returned), no handling of groups with no relevant items, and tie order that depends on the sort; I fix each one and pin them with hand-computed tests.

**Then explain (the buggy code, which I ran):**
```python
import numpy as np
def precision_at_k_bad(y_true, scores, k):
    order = np.argsort(scores)[:k]                 # BUG 1: ascending, picks the LOWEST scores
    return y_true[order].sum() / k

def ndcg_at_k_bad(y_true, scores, k):
    order = np.argsort(-scores)[:k]
    dcg = sum(y_true[i] / np.log2(r + 1) for r, i in enumerate(order))   # BUG 2: r starts at 0
    ideal = sorted(y_true, reverse=True)[:k]
    idcg = sum(g / np.log2(r + 1) for r, g in enumerate(ideal))
    return dcg / idcg                              # BUG 3: idcg == 0 when nothing is relevant
```
- Bug 1: ascending sort. On my example it returns precision@3 = 0.333 instead of 0.667.
- Bug 2: with a 0-based rank, the first discount is `1/log2(1)`, which is a division by zero. The discount for 1-based rank `r` is `1/log2(r + 1)`, so ranks 1..k use `log2(2..k+1)`.
- Bug 3: a group with no relevant items has `idcg = 0`, giving NaN. Define it (usually 0, or skip the group) and say so.
- Ties: `argsort` is not stable by default; with equal scores the metric can change between runs. Use a stable, documented tie-break (original position here), or average over tie permutations.
- Fewer than `k` items: slice safely (`[:k]` is fine in NumPy) and decide whether to divide by `k` or by the number returned; the common convention is `k`.
- Formulas: `P@k = (relevant in top k) / k`; `DCG@k = sum_{i=1..k} rel_i / log2(i+1)`; `NDCG@k = DCG@k / IDCG@k`, where IDCG is the DCG of the best possible ordering.

**Example (hand-computed, checked by the tests below):** relevance `y = [1, 0, 1, 0, 0]` with model scores `[.9, .8, .7, .6, .5]`, so the model ranks the items in the order given. Top 3 contain 2 relevant items: precision@3 = 2/3 = 0.667 (the ascending-sort bug returns 0.333). DCG@3 = 1 + 0 + 1/log2(4) = 1.5; the ideal order 1, 1, 0 gives IDCG@3 = 1 + 1/log2(3) = 1.631; so NDCG@3 = 0.920.

**Code (fixed, with tests):**
```python
import numpy as np
from sklearn.metrics import ndcg_score

def _order(scores):                                  # high score first, ties by original position
    return np.lexsort((np.arange(len(scores)), -scores))

def precision_at_k(y_true, scores, k):
    y_true, scores = np.asarray(y_true), np.asarray(scores, float)
    kk = min(k, len(y_true))
    if kk == 0: return 0.0
    return float(y_true[_order(scores)[:kk]].astype(bool).sum() / k)

def ndcg_at_k(y_true, scores, k):
    y_true, scores = np.asarray(y_true, float), np.asarray(scores, float)
    disc = 1.0 / np.log2(np.arange(2, k + 2))          # ranks 1..k -> log2(2..k+1)
    top = y_true[_order(scores)[:k]]
    dcg = (top * disc[:len(top)]).sum()
    ideal = np.sort(y_true)[::-1][:k]
    idcg = (ideal * disc[:len(ideal)]).sum()
    return float(dcg / idcg) if idcg > 0 else 0.0       # no relevant item: defined as 0

y = np.array([1, 0, 1, 0, 0]); s = np.array([.9, .8, .7, .6, .5])
assert precision_at_k(y, s, 3) == 2 / 3
assert abs(ndcg_at_k(y, s, 3) - (1 + 1/np.log2(4)) / (1 + 1/np.log2(3))) < 1e-12   # hand-computed
assert precision_at_k(np.array([1]), np.array([.5]), 5) == 1 / 5                    # fewer items than k
assert ndcg_at_k(np.zeros(4), np.arange(4.), 3) == 0.0                              # empty group
assert ndcg_at_k(y, np.full(5, .9), 2) == ndcg_at_k(y, np.ones(5), 2)               # ties deterministic
g = np.array([3, 2, 0, 1, 0.]); sc = np.array([.1, .9, .5, .7, .2])
assert abs(ndcg_at_k(g, sc, 4) - ndcg_score([g], [sc], k=4)) < 1e-12                # matches sklearn (no ties)
print("all tests pass")
```
The hand-computed value: top 3 are items with gains 1, 0, 1, so DCG = 1 + 1/log2(4) = 1.5; ideal is 1, 1, 0 so IDCG = 1 + 1/log2(3) = 1.631; NDCG = 0.920.

**Follow-ups:**
- *Per query or global?* Compute per group (query/user), then average; a global sort across all users is a common bug.
- *Gain form?* Some use `2^rel - 1` instead of `rel`; sklearn uses linear gains. State which one you use.
- *Why test against sklearn only without ties?* Tie handling differs; sklearn averages over ties by default.

**Common mistakes:** Sorting the wrong way, 0-based ranks in the discount, NaN from empty groups silently dropped from the mean, mixing the `rel` and `2^rel-1` gain conventions, and evaluating on the training queries.

### Q41 ⭐⭐ 🔴 Check for duplicates and near-duplicates across train/test (same user, session, image or text) and write code that splits so no entity appears in both. Quantify the score inflation.
**Asked at:** Product cos, Spotify/Booking-type DS
**Say this first (1 line):** I check overlap on the entity key (user, session, image hash, text fingerprint), then split with `GroupShuffleSplit` or `GroupKFold` so no entity is on both sides, and I quantify the damage by comparing a row-level split with a group split on the same data.

**Then explain:**
- Exact duplicates: hash the row (or the text/image bytes) and intersect the hash sets of train and test.
- Near-duplicates: for tabular or embedding data use nearest-neighbour distance from each test row to the train set; for text use MinHash or TF-IDF cosine above a threshold; for images use perceptual hashes or embeddings.
- Same entity, different rows (a user's 10 sessions) is the sneakiest case: the model memorises the user, not the pattern.
- Fix: split on the group id. Use `GroupShuffleSplit` for one split, `GroupKFold` / `StratifiedGroupKFold` for CV. Dedupe before splitting, otherwise copies straddle the split.
- Quantify: report score with row-split and group-split side by side. The gap is the inflation.
- Choose the group to match how the model is used: if it will score new users, group by user; if new sessions of known users, a row split can be legitimate.

**Example (run):** 300 users with 10 near-identical rows each; the label depends only on the user (not on features), so the honest AUC is 0.5. Row-level split: 288 users appear on both sides and random forest AUC is 1.000. Group split: 0 shared users, mean AUC over 8 splits 0.587 (close to chance; the remaining 0.09 is sampling noise from only 300 users). Also 100% of test rows have a train neighbour within distance 0.5.

**Code:**
```python
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.neighbors import NearestNeighbors

rng = np.random.default_rng(0)
n_users, per = 300, 10
uid = np.repeat(np.arange(n_users), per)
user_fp = rng.normal(size=(n_users, 8))                       # user-specific fingerprint features
label_u = rng.integers(0, 2, n_users)                         # label depends on the user only
X = user_fp[uid] + rng.normal(0, .05, (len(uid), 8))          # rows of one user are near-duplicates
df = pd.DataFrame(X, columns=[f"f{i}" for i in range(8)]).assign(user=uid, y=label_u[uid])

def score(tr, te):
    m = RandomForestClassifier(200, random_state=0, n_jobs=-1).fit(df.loc[tr, df.columns[:8]], df.y[tr])
    return roc_auc_score(df.y[te], m.predict_proba(df.loc[te, df.columns[:8]])[:, 1])

i_tr, i_te = train_test_split(df.index, test_size=.25, random_state=0)               # row-level split
gss = list(GroupShuffleSplit(8, test_size=.25, random_state=0).split(df, groups=df.user))
g_tr, g_te = gss[0]
print("row split   : users in both =", len(set(df.user[i_tr]) & set(df.user[i_te])), "AUC", round(score(i_tr, i_te), 3))
print("group split : users in both =", len(set(df.user[g_tr]) & set(df.user[g_te])),
      "mean AUC over 8 splits", round(np.mean([score(a, b) for a, b in gss]), 3))

nn = NearestNeighbors(n_neighbors=1).fit(df.loc[i_tr].iloc[:, :8])      # near-duplicate check
d = nn.kneighbors(df.loc[i_te].iloc[:, :8])[0].ravel()
print("test rows with a train neighbour closer than 0.5:", f"{(d < .5).mean():.0%}")
```

**Follow-ups:**
- *Time also matters?* If data is time-ordered, split by time and group; a group split alone can still leak the future.
- *Images or text at scale?* Use locality-sensitive hashing (MinHash, perceptual hash) instead of all-pairs distances.
- *Dedupe training data too?* Yes; duplicates inside train overweight those rows and make CV optimistic.

**Common mistakes:** Splitting rows when the unit is a user, deduping after the split, only checking exact matches, never measuring the row-vs-group gap, and using a global threshold for near-duplicates without eyeballing examples.

### Q42 ⭐ 🟡 Implement permutation feature importance from scratch in NumPy for any fitted estimator, with repeated shuffles and a held-out set, and compare with sklearn.inspection.
**Asked at:** Product cos, interpretability-minded teams
**Say this first (1 line):** Permutation importance shuffles one feature column at a time on held-out data, re-scores the fitted model, and reports the drop in the metric; a big drop means the model relies on that feature.

**Then explain:**
- Works for any fitted model (model-agnostic): the only thing I need is a predict function and a metric.
- Shuffle one column, leave the rest: this keeps the feature's distribution but breaks its link with the target.
- Repeat several times and report mean and std; one shuffle is noisy.
- Use held-out (validation) data. On training data, an overfit model looks like it relies on noise features too.
- Limitations: with correlated features, shuffling one creates unrealistic rows and importance gets shared or hidden (the twin feature still carries the signal); also it is a statement about this model, not about the world. Importance can be slightly negative from noise.
- Cost: `n_features * n_repeats` scorings. Fine for tabular data.

**Example (run):** 6 features, first 3 informative. Mine vs sklearn (AUC drop): feature 0 0.304 vs 0.306, feature 1 0.135 vs 0.131, feature 2 0.260 vs 0.248, noise features about 0. Differences come from different random shuffles. On the training set the ranking is distorted (0.238, 0.147, 0.184).

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

X, y = make_classification(1500, 6, n_informative=3, n_redundant=0, shuffle=False, random_state=0)
Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=.4, random_state=0)
model = RandomForestClassifier(200, random_state=0).fit(Xtr, ytr)

def perm_importance(model, X, y, metric, n_repeats=10, seed=0):
    rng = np.random.default_rng(seed)
    base = metric(y, model.predict_proba(X)[:, 1])
    out = np.zeros((X.shape[1], n_repeats))
    for j in range(X.shape[1]):
        Xp = X.copy()
        for r in range(n_repeats):
            Xp[:, j] = rng.permutation(X[:, j])          # break the link between feature j and y
            out[j, r] = base - metric(y, model.predict_proba(Xp)[:, 1])
    return out.mean(1), out.std(1)

m, s = perm_importance(model, Xva, yva, roc_auc_score)
ref = permutation_importance(model, Xva, yva, scoring="roc_auc", n_repeats=10, random_state=0)
print("mine   :", np.round(m, 3))
print("sklearn:", np.round(ref.importances_mean, 3))
mt, _ = perm_importance(model, Xtr, ytr, roc_auc_score)          # on TRAIN data: the forest has memorised it
print("on train:", np.round(mt, 3))
```

**Follow-ups:**
- *Correlated features?* Permute them together as a group, or use drop-column importance (retrain without the feature, slower but handles redundancy).
- *Vs impurity importance?* Impurity importance is computed on training data and favours high-cardinality features; permutation on validation data is more trustworthy.
- *Vs SHAP?* SHAP explains individual predictions and global attributions; permutation importance measures reliance in terms of the metric.

**Common mistakes:** Computing it on training data, a single shuffle, reading importance as causal, ignoring correlated twins, and shuffling the target instead of the feature.

### Q43 ⭐ 🟡 Implement a non-parametric bootstrap confidence interval for a metric (e.g. AUC or median) in vectorised NumPy and state its limitations.
**Asked at:** Product cos, experimentation teams
**Say this first (1 line):** Resample the rows with replacement B times, recompute the metric on each resample, and take the 2.5th and 97.5th percentiles of those B values as a 95% interval; in NumPy I draw all resamples at once as an index matrix and compute the metric along axis 1.

**Then explain:**
- Resample (score, label) pairs together, as rows; never resample scores and labels separately.
- Vectorise: `idx = rng.integers(0, n, (B, n))`, then `y[idx]`, `s[idx]` have shape `(B, n)`. AUC via ranks: `(sum of positive ranks - n1(n1+1)/2) / (n1*n0)`.
- Use a few thousand resamples; the percentile interval is simple and good enough for most metrics.
- Limitations: it assumes rows are independent, so for grouped or time-series data you must resample whole groups or blocks. It is unreliable for tiny samples, for statistics like the max or a very rare-class metric, and it only captures test-set sampling noise, not variation from retraining the model. Memory is `B * n`, so chunk it for big `n`. My rank-AUC ignores ties; use average ranks if scores have many ties.
- Better still for model comparison: bootstrap the *difference* in the metric on the same resamples (paired).

**Example (run):** 400 rows, one score per row. AUC 0.788 (the vectorised formula matches sklearn: 0.788), 95% CI [0.741, 0.830]. Median of the scores: estimate 0.492, CI [0.361, 0.625].

**Code:**
```python
import numpy as np
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(0)
n = 400
y = rng.integers(0, 2, n)
s = rng.normal(y * 1.0, 1.0)                             # scores with some signal

B = 2000
idx = rng.integers(0, n, (B, n))                         # B resamples at once (rows with replacement)
yb, sb = y[idx], s[idx]                                  # shape (B, n)
r = sb.argsort(axis=1).argsort(axis=1) + 1.0             # ranks within each resample
n1 = yb.sum(1); n0 = n - n1
aucs = ((r * yb).sum(1) - n1 * (n1 + 1) / 2) / (n1 * n0)
lo, hi = np.percentile(aucs, [2.5, 97.5])
print(f"AUC {roc_auc_score(y, s):.3f}  95% CI [{lo:.3f}, {hi:.3f}]")

med = np.median(sb, axis=1)
print("median CI:", np.percentile(med, [2.5, 97.5]).round(3), "estimate", round(float(np.median(s)), 3))
```

**Follow-ups:**
- *Percentile vs BCa?* BCa corrects bias and skew; scipy has `scipy.stats.bootstrap`.
- *Grouped data?* Resample group ids, then take all rows of the chosen groups.
- *What does 95% mean?* If I repeated the whole study many times, about 95% of such intervals would contain the true value; it is not a 95% probability for this one interval.

**Common mistakes:** Resampling the model's training data and calling it the test CI, resampling scores and labels independently, too few resamples, ignoring dependence between rows, and treating a CI on a single split as covering model-retraining variance.

### Q44 ⭐ 🟡 Write pytest unit tests for a data-processing function: pandas.testing.assert_frame_equal, edge cases (empty, all-null, duplicate keys), and a check that the transform never changes row count.
**Asked at:** MLE rounds, GCCs, Microsoft IDC
**Say this first (1 line):** I test the function against a small hand-computed expected frame with `assert_frame_equal`, then add edge-case tests (empty input, all-null column, duplicate keys, zero denominators), an invariant test that row count does not change, and a check that the input is not mutated.

**Then explain:**
- `pandas.testing.assert_frame_equal` compares values, dtypes, index and column order, and reports the first difference. Use `check_dtype=False` or `check_like=True` only when you mean it.
- Known-answer test: 2 or 3 rows I can compute by hand; this catches wrong formulas.
- Edge cases: empty frame (columns and dtypes still correct), all-NaN column, zero totals (0/0 should be NaN, not inf), unknown keys, duplicate keys in the lookup table.
- Invariants: `len(out) == len(in)` after a left join; no mutation of the input.
- `pytest.fixture` for shared data, `pytest.raises(..., match=...)` for expected errors, and `@pytest.mark.parametrize` for many small cases.
- Tests should fail when the code breaks: remove the duplicate check and `validate="m:1"` and the duplicate-key test fails.

**Example (run):** the 6 tests below pass (`6 passed`; runtime is machine-specific).

**Code:** (save as `test_features.py`, run `pytest -q`)
```python
import numpy as np, pandas as pd, pytest
from pandas.testing import assert_frame_equal

def add_features(orders, customers):
    """Left-join customer tier and add spend_share = amount / customer total amount."""
    if customers["customer_id"].duplicated().any():
        raise ValueError("duplicate customer_id")
    out = orders.merge(customers[["customer_id", "tier"]], on="customer_id", how="left", validate="m:1")
    total = out.groupby("customer_id")["amount"].transform("sum")
    out["spend_share"] = out["amount"] / total.where(total != 0)     # no division by zero
    return out

@pytest.fixture
def customers():
    return pd.DataFrame({"customer_id": [1, 2], "tier": ["gold", "basic"]})

def test_known_answer(customers):
    orders = pd.DataFrame({"customer_id": [1, 1, 2], "amount": [10.0, 30.0, 5.0]})
    expected = pd.DataFrame({"customer_id": [1, 1, 2], "amount": [10.0, 30.0, 5.0],
                             "tier": ["gold", "gold", "basic"], "spend_share": [.25, .75, 1.0]})
    assert_frame_equal(add_features(orders, customers), expected)

def test_row_count_never_changes(customers):
    orders = pd.DataFrame({"customer_id": [1, 2, 2, 3], "amount": [1., 2., 3., 4.]})   # 3 is unknown
    assert len(add_features(orders, customers)) == len(orders)

def test_duplicate_keys_rejected(customers):
    dup = pd.concat([customers, customers])
    with pytest.raises(ValueError, match="duplicate"):
        add_features(pd.DataFrame({"customer_id": [1], "amount": [1.]}), dup)

def test_empty_input(customers):
    empty = pd.DataFrame({"customer_id": pd.Series(dtype="int64"), "amount": pd.Series(dtype="float64")})
    out = add_features(empty, customers)
    assert len(out) == 0 and list(out.columns) == ["customer_id", "amount", "tier", "spend_share"]

def test_all_null_and_zero_amount(customers):
    orders = pd.DataFrame({"customer_id": [1, 1], "amount": [np.nan, np.nan]})
    assert add_features(orders, customers)["spend_share"].isna().all()
    zeros = pd.DataFrame({"customer_id": [2], "amount": [0.0]})
    assert add_features(zeros, customers)["spend_share"].isna().all()           # 0/0 -> NaN, not inf

def test_input_not_mutated(customers):
    orders = pd.DataFrame({"customer_id": [1], "amount": [2.0]})
    before = orders.copy()
    add_features(orders, customers)
    assert_frame_equal(orders, before)
```

**Follow-ups:**
- *Float comparison?* `assert_frame_equal` uses a small tolerance by default (`rtol=1e-5`); tighten or loosen it deliberately.
- *Property-based tests?* `hypothesis` can generate frames and check invariants like row count.
- *Testing ML code?* Also test no-leakage (fit only on train), output shapes, and that a tiny dataset can be overfit.

**Common mistakes:** Testing only the happy path, asserting with `==` on frames, tests with no known answer (they just re-run the code), forgetting dtype and column order, and not testing that the input stays unchanged.

### Q45 ⭐ 🟡 Use sparse matrices in an sklearn pipeline (OneHotEncoder sparse output, TF-IDF + numeric features via ColumnTransformer) and avoid accidentally densifying.
**Asked at:** NLP/search teams, product cos
**Say this first (1 line):** Keep the matrix sparse from the encoder to the model: use sparse-aware steps (`OneHotEncoder`, `TfidfVectorizer`), a sparse-friendly estimator (linear models, linear SVM, Naive Bayes), and never call `.toarray()` or a step that needs dense input.

**Then explain:**
- One-hot of a 300-level column or TF-IDF over 2,000 words is almost all zeros. A sparse CSR matrix stores only the non-zeros: here 0.6% of the cells.
- `ColumnTransformer` stacks the blocks side by side and returns a sparse matrix if the overall density is below `sparse_threshold` (default 0.3). A dense block (one scaled numeric column) mixed in is fine.
- What densifies or breaks: centring (`StandardScaler()` with mean subtraction refuses sparse input; use `with_mean=False` or `MaxAbsScaler`), `PCA` (use `TruncatedSVD` instead), `GaussianNB`, `.toarray()` / `.todense()`, and `OneHotEncoder(sparse_output=False)`.
- Estimators that take sparse input directly: `LogisticRegression`, `SGDClassifier`, `LinearSVC`, `MultinomialNB`, `Ridge`.
- Check with `scipy.sparse.issparse(Xt)` and compare `nnz` to `rows * cols`.

**Example (run):** 5,000 rows with text, a 300-level city and a numeric amount give a 5000 x 2301 matrix. Sparse: 0.86 MB. If dense: 92 MB. Logistic regression CV AUC 0.993 on a synthetic keyword target. `StandardScaler().fit(Xt)` on the sparse result raises a ValueError.

**Code:**
```python
import numpy as np, pandas as pd, scipy.sparse as sp
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

rng = np.random.default_rng(0)
n = 5000
words = np.array([f"w{i}" for i in range(2000)])
df = pd.DataFrame({"text": [" ".join(rng.choice(words, 12)) for _ in range(n)],
                   "city": rng.choice([f"c{i}" for i in range(300)], n),
                   "amount": rng.lognormal(3, 1, n)})
y = (df.text.str.contains("w1 ") | df.text.str.contains("w7 ")).astype(int).to_numpy()

pre = ColumnTransformer([("t", TfidfVectorizer(min_df=3), "text"),                    # sparse
                         ("c", OneHotEncoder(handle_unknown="ignore"), ["city"]),     # sparse by default
                         ("n", StandardScaler(), ["amount"])],                        # 1 dense column: fine
                        sparse_threshold=0.3)       # output stays sparse if overall density < 30%
Xt = pre.fit_transform(df)
print("sparse output:", sp.issparse(Xt), Xt.shape, "| nnz fraction", round(Xt.nnz / np.prod(Xt.shape), 4))
print("MB sparse :", round((Xt.data.nbytes + Xt.indices.nbytes + Xt.indptr.nbytes) / 1e6, 2),
      "| MB if dense:", round(np.prod(Xt.shape) * 8 / 1e6, 1))
print("CV AUC:", round(cross_val_score(make_pipeline(pre, LogisticRegression(max_iter=1000)),
                                       df, y, cv=3, scoring="roc_auc").mean(), 3))
try: StandardScaler().fit(Xt)
except ValueError: print("StandardScaler on sparse -> ValueError (use with_mean=False)")
```

**Follow-ups:**
- *Why not just `sparse_output=False`?* On wide one-hot data the dense array can be hundreds of times larger and slows every step.
- *Scale sparse features?* `MaxAbsScaler` or `StandardScaler(with_mean=False)` keep zeros as zeros.
- *Which format?* CSR for row slicing and model input, CSC for column slicing; avoid LIL/DOK for computation.

**Common mistakes:** Calling `.toarray()` to "make it work", centring sparse data, converting the full matrix to a DataFrame for inspection, using an estimator that silently densifies, and not checking memory at realistic data size.

### Q46 ⭐ 🟡 Explain views vs copies, strides and broadcasting rules in NumPy, then fix a bug where modifying a slice silently changes the original array.
**Asked at:** Product cos, MLE rounds
**Say this first (1 line):** A basic slice (`a[:, :2]`) is a view that shares memory with the original, so writing to it changes the original; fancy indexing and boolean masks make copies; when I need an independent array I call `.copy()` explicitly.

**Then explain:**
- Strides: an array is a block of memory plus shape and strides (bytes to jump per axis). For a `(3, 4)` int64 array, strides are `(32, 8)`: one row down is 32 bytes, one column right is 8. Transpose just swaps the strides `(8, 32)`, no data moves, so `a.T` is a view.
- Views: basic slices, `reshape` (when possible), `.T`, `ravel` (when contiguous). Copies: fancy indexing (`a[[0, 2]]`), boolean masks (`a[a > 5]`), `.copy()`, `flatten()`.
- Check with `np.shares_memory(a, b)` (exact) or `b.base is not None` (hint only).
- Bug pattern: a helper takes a row or slice and does an in-place operation (`row -= row.mean()`, `x[:] = ...`) and silently changes the caller's data, often the training set.
- Broadcasting: line the shapes up from the right; each pair of dimensions must be equal or one of them 1; missing leading dimensions count as 1. `(3,1) + (4,)` gives `(3,4)`; `(3,2) + (3,)` fails because 2 and 3 do not match; fix with `(3,1)`.

**Example (run):** `s = a[:, :2]; s[0, 0] = 99` changed `a[0, 0]` to 99 (shared memory True). `b[[0, 2]][0, 0] = -1` did not touch `b`. The buggy helper turned `[1, 2, 3]` into `[-1, 0, 1]` in the caller's array; the fixed one left it as `[1, 2, 3]`.

**Code:**
```python
import numpy as np

a = np.arange(12).reshape(3, 4)
print("strides:", a.strides, "| transpose strides:", a.T.strides, "| T shares memory:", np.shares_memory(a, a.T))

s = a[:, :2]                                   # basic slice -> VIEW
s[0, 0] = 99
print("view changed original:", a[0, 0], "| shares memory:", np.shares_memory(a, s))

b = np.arange(12).reshape(3, 4)
f = b[[0, 2]]                                  # fancy index -> COPY
f[0, 0] = -1
print("fancy copy changed original:", b[0, 0] == -1)

def normalise_bad(x):
    row = x[0]                                 # view
    row -= row.mean()                          # in-place: mutates the caller's array
    return row
def normalise_ok(x):
    row = x[0].copy()                          # explicit copy
    return row - row.mean()
d = np.array([[1., 2., 3.], [4., 5., 6.]]); normalise_bad(d); print("after bad:", d[0])
d = np.array([[1., 2., 3.], [4., 5., 6.]]); normalise_ok(d);  print("after ok :", d[0])

col = np.arange(3).reshape(3, 1); row = np.arange(4)
print("(3,1)+(4,) ->", (col + row).shape)
try: np.ones((3, 2)) + np.ones(3)
except ValueError: print("(3,2)+(3,) -> ValueError")
print("(3,2)+(3,1) ->", (np.ones((3, 2)) + np.ones((3, 1))).shape)
```

**Follow-ups:**
- *Why views at all?* Speed and memory: slicing a huge array is O(1) and allocates nothing.
- *`reshape` view or copy?* A view when the strides allow, otherwise a copy; do not rely on either.
- *In pandas?* Same confusion, solved by copy-on-write in pandas 3 (see Q3).

**Common mistakes:** Assuming a slice is a copy, mutating function arguments in place, using `b.base` to prove sharing, and relying on broadcasting that silently expands the wrong axis (for example `(n,) - (n,1)` gives an `(n,n)` matrix).

### Q47 ⭐ 🔴 Implement groupby-sum/mean/count from scratch in NumPy with np.unique(return_inverse) and np.bincount, then benchmark against pandas.
**Asked at:** Product cos, MLE rounds, senior DS
**Say this first (1 line):** `np.unique(keys, return_inverse=True)` turns arbitrary keys into group numbers 0..G-1, and then `np.bincount(inverse, weights=values)` sums per group in one pass; count is `bincount(inverse)` and mean is sum divided by count.

**Then explain:**
- `return_inverse` gives, for each row, the index of its group in the sorted unique-key array. That is a label-encoding step.
- `bincount(inv)` = count per group; `bincount(inv, weights=v)` = sum per group; mean = sum / count. All O(n) after the encoding.
- `np.unique` sorts, so the encoding costs O(n log n); that is the dominant cost. If keys are already small non-negative integers, skip it and call `bincount` directly (much faster).
- Other stats need more work: min/max use `np.minimum.at` or sort by group and `reduceat`; variance uses `sum(x^2)` per group with the cancellation caveat from Q36, or a two-pass version.
- NaN values: `bincount` with NaN weights gives NaN; mask them first and count only non-NaN.
- pandas does hashing in optimised C and handles many dtypes and NaN keys, so it is rarely slower in practice; the exercise shows what groupby does underneath.

**Example (run, this machine):** 2M rows, 50k groups. NumPy unique + bincount took about 2 to 2.5x as long as pandas `groupby(...).agg(["sum","mean","count"])` (for example 0.84 s vs 0.33 s in one busy re-run; absolute times vary a lot by machine), and `bincount` alone on pre-encoded keys was about 0.05 s there. Results agree. So the honest finding: my from-scratch version is slower than pandas because of the sort, and the real win comes from avoiding the sort.

**Code:**
```python
import time, numpy as np, pandas as pd

rng = np.random.default_rng(0)
n = 2_000_000
keys = rng.integers(0, 50_000, n)
vals = rng.normal(size=n)

def group_stats(keys, vals):
    uniq, inv = np.unique(keys, return_inverse=True)          # inv[i] = group index of row i
    cnt = np.bincount(inv)
    s = np.bincount(inv, weights=vals)                        # sum per group, O(n)
    return uniq, s, s / cnt, cnt

t = time.perf_counter(); u, s, m, c = group_stats(keys, vals); t_np = time.perf_counter() - t
t = time.perf_counter()
g = pd.DataFrame({"k": keys, "v": vals}).groupby("k")["v"].agg(["sum", "mean", "count"])
t_pd = time.perf_counter() - t
print("same keys:", np.array_equal(u, g.index.to_numpy()))
print("sum/mean/count match:", np.allclose(s, g["sum"]), np.allclose(m, g["mean"]), np.array_equal(c, g["count"]))
print(f"numpy {t_np:.3f}s  pandas {t_pd:.3f}s (this machine)")

t = time.perf_counter(); s2 = np.bincount(keys, weights=vals, minlength=50_000); t_bc = time.perf_counter() - t
print(f"bincount only {t_bc:.4f}s")        # keys already small ints: no sort needed
```

**Follow-ups:**
- *Why does `bincount` need non-negative ints?* It indexes into an array of that size; negative values or huge ints are invalid or wasteful, so encode first.
- *Group max?* `np.maximum.at(out, inv, vals)` (slowish) or sort once and use `np.maximum.reduceat`.
- *When use Polars or DuckDB?* When the data is large or multi-threaded speed matters (see Q48).

**Common mistakes:** Looping over groups in Python, using `np.unique` on every call in a hot path, forgetting `minlength` when some group ids are absent, and benchmarking once without warm-up or on tiny data.

### Q48 ⭐ 🔴 Translate a pandas pipeline to Polars (lazy) or DuckDB and explain when and why you would; what do pandas 2/3 features (Arrow dtypes, copy-on-write) change?
**Asked at:** Product cos, data-platform-minded teams
**Say this first (1 line):** Polars lazy and DuckDB describe the whole query first and then run it, so they can read only the needed columns, push filters into the Parquet scan and use all cores; I reach for them when data is large or the pandas job is slow, and keep pandas for small data and sklearn hand-off.

**Then explain:**
- Polars lazy: `scan_parquet(...)` builds a plan; `.collect()` runs it. The optimiser does projection pushdown (read 2 of 4 columns) and predicate pushdown (filter at scan). The plan printed by `.explain()` showed `PROJECT 2/4 COLUMNS` and `SELECTION: amt > 20`.
- DuckDB: run SQL straight on a Parquet file or a pandas DataFrame, in process, multi-threaded, and it can spill to disk for larger-than-memory work. Great if the team already thinks in SQL.
- pandas: eager, mostly single-threaded, every step materialises a full intermediate, and memory is often 5 to 10x the file size. Best for small data, rich ecosystem, quick exploration.
- Mapping: `query/filter` to `filter`, `assign` to `with_columns`, `groupby.agg` to `group_by().agg`, `merge` to `join`, `sort_values` to `sort`. Polars has no index, which removes a class of alignment bugs.
- What pandas 2/3 changed: Arrow-backed dtypes (`dtype_backend="pyarrow"`) give nullable types, less memory for strings and faster I/O. Copy-on-write (opt-in in 2.x, default in pandas 3) means any derived object behaves like a copy, which ends chained-assignment bugs and removes defensive copies. These narrow the gap but pandas is still eager and mostly single-threaded.
- Trade-offs: smaller ecosystem and API changes in Polars; SQL strings are harder to test in DuckDB; converting to pandas or NumPy at the model boundary costs a copy.

**Example (run, this machine, pandas 2.3.3):** 3M rows, filter, monthly spend per user, keep users with at least 2 rows, top 5. pandas 4.69 s, Polars lazy 0.46 s, DuckDB 0.81 s in the latest run (an earlier run gave 2.65 / 0.53 / 0.28 s, so DuckDB vs Polars order is noise; the gap to pandas is the stable part); all three returned the same top totals (1151.74, 1099.73, 1037.99). Timings are machine-specific and include reading the Parquet file.

**Code:**
```python
import numpy as np, pandas as pd, polars as pl, duckdb, os, tempfile

rng = np.random.default_rng(0)
n = 3_000_000
df = pd.DataFrame({"user": rng.integers(0, 100_000, n), "cat": rng.choice(["a", "b", "c", "d"], n),
                   "amt": rng.gamma(2, 30, n),
                   "ts": pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 365 * 86400, n), "s")})
path = os.path.join(tempfile.gettempdir(), "tx_demo.parquet"); df.to_parquet(path)

def pandas_way():
    d = pd.read_parquet(path)
    d = d[d.amt > 20]
    d["month"] = d.ts.dt.to_period("M")
    return (d.groupby(["user", "month"]).agg(total=("amt", "sum"), n=("amt", "size")).reset_index()
              .query("n >= 2").sort_values(["total", "user", "month"], ascending=[False, True, True])
              .head(5).reset_index(drop=True))

def polars_way():
    return (pl.scan_parquet(path).filter(pl.col("amt") > 20)                 # lazy: nothing read yet
            .with_columns(month=pl.col("ts").dt.truncate("1mo"))
            .group_by(["user", "month"]).agg(total=pl.col("amt").sum(), n=pl.len())
            .filter(pl.col("n") >= 2).sort(["total", "user", "month"], descending=[True, False, False])
            .head(5).collect().to_pandas())

def duckdb_way():
    p = path.replace(chr(92), "/")
    return duckdb.sql(f"""
        SELECT user, date_trunc('month', ts) AS month, SUM(amt) AS total, COUNT(*) AS n
        FROM '{p}' WHERE amt > 20 GROUP BY 1, 2 HAVING COUNT(*) >= 2
        ORDER BY total DESC, user, month LIMIT 5""").df()

import time
for name, f in [("pandas", pandas_way), ("polars lazy", polars_way), ("duckdb", duckdb_way)]:
    t0 = time.perf_counter(); r = f()
    print(name, r.total.round(2).tolist()[:3], f"{time.perf_counter() - t0:.2f}s")   # same top 3 totals each time
print(pl.scan_parquet(path).filter(pl.col("amt") > 20).select("user", "amt").explain())  # shows the pushed-down plan
```

**Follow-ups:**
- *Do you switch the whole stack?* No: do heavy joins and aggregations in Polars or DuckDB, then convert the result (`.to_pandas()`, `.to_numpy()`) for sklearn.
- *Eager vs lazy in Polars?* Eager is fine for exploration; lazy for pipelines and big files.
- *Data larger than RAM?* DuckDB spills to disk; Polars can stream (`collect(engine="streaming")` in recent versions); otherwise partition the Parquet files.

**Common mistakes:** Rewriting everything for a 100 MB file, benchmarking with different logic (different filters or sort ties), forgetting that Polars has no index so row alignment must be explicit, and converting back and forth to pandas inside loops.

### Q49 ⭐ 🔴 You may use an AI assistant in this round. Walk through how you would prompt it to write a feature pipeline, then verify it: what tests, invariants, leakage checks and baselines do you run before trusting the output?
**Asked at:** AI-allowed interviews (an increasingly common format; not tied to a specific survey); AI-native startups
**Say this first (1 line):** I treat the AI as a fast junior who writes the first draft: I give it a precise spec, then I do not trust the output until it passes my own tests for correctness, leakage and a simple baseline, and I say out loud that I am responsible for every line.

**Then explain:**
- **Prompt:** state the prediction time ("features available at 00:00 on day t"), the target definition, the input schema with dtypes, what is forbidden (no future data, no fitting on full data, no `inplace`, no `iterrows`), the expected output shape and column names, and ask for a `Pipeline` plus a function with a docstring and a tiny example. Ask it to list its assumptions.
- **Read it first:** check time boundaries (`shift`, windows, `closed=`), where `fit` is called, joins (row counts, key uniqueness), NaN handling, and any global state or random seeds.
- **Invariants (asserts):** row count in equals out; keys unique; no unexpected NaN or inf; dtypes as specified.
- **Leakage checks:** (1) a lookahead test: change a future row and confirm earlier rows' features do not change; (2) fit transformers only inside `Pipeline` and CV; (3) a shuffled-label canary, which should score about chance; (4) suspiciously high scores (AUC near 1) mean a leak, not a great model; (5) a time or group split, not a random one.
- **Baselines:** constant or prior, a one-feature rule, and a plain logistic regression. If the fancy model barely beats them, the pipeline is not adding value.
- **Hand-check:** compute 2 or 3 rows by hand and compare. Then run on a tiny and a large sample for speed.
- **Be transparent:** tell the interviewer which parts the AI drafted and which checks I added; reviewing is the skill being tested.

**Example (run):** for an AI-written feature function (previous amount and rolling mean per user), my checks gave: invariants pass; features of earlier rows unchanged after editing future rows (True); baseline AUC 0.500; model AUC 0.483; shuffled-label canary 0.490. Here the target is random, so all three sitting near 0.5 is the correct result, and a high score would have signalled a leak.

**Code:**
```python
import numpy as np, pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import cross_val_score, TimeSeriesSplit

def build_features(raw):                                    # stand-in for the AI-written function
    d = raw.sort_values(["user", "ts"]).copy()
    d["prev_amt"] = d.groupby("user")["amt"].shift(1)       # past only
    d["roll3"] = d.groupby("user")["amt"].transform(lambda s: s.shift(1).rolling(3, min_periods=1).mean())
    return d.sort_values("ts")

rng = np.random.default_rng(0)
raw = pd.DataFrame({"user": rng.integers(0, 50, 3000), "ts": pd.date_range("2024-01-01", periods=3000, freq="h"),
                    "amt": rng.gamma(2, 20, 3000)})
raw["y"] = (rng.random(3000) < 0.2).astype(int)             # label unrelated to the features here
feat = build_features(raw)

assert len(feat) == len(raw) and not feat.duplicated(["user", "ts"]).any()      # invariants

cut = raw.ts.iloc[2000]                                     # lookahead test
raw2 = raw.copy(); raw2.loc[raw2.ts >= cut, "amt"] += 1000
feat2 = build_features(raw2)
cols = ["prev_amt", "roll3"]; past = feat.ts < cut
print("features of earlier rows unchanged:", feat.loc[past, cols].equals(feat2.loc[past, cols]))

X, y = feat[cols], feat["y"]                                # baseline, time-ordered CV, canary
cv = TimeSeriesSplit(4)
def auc(m, yy): return round(cross_val_score(m, X, yy, cv=cv, scoring="roc_auc").mean(), 3)
print("baseline:", auc(DummyClassifier(), y))
print("model   :", auc(HistGradientBoostingClassifier(random_state=0), y))
print("shuffled-label canary:", auc(HistGradientBoostingClassifier(random_state=0),
                                    pd.Series(rng.permutation(y), index=y.index)))
```

**Follow-ups:**
- *What if the AI's code passes everything but is slow?* Profile, then ask it to vectorise with a test that the output is unchanged.
- *Would you let it write the tests?* Yes for boilerplate, but I write the known-answer cases and invariants myself, because tests written by the same model share its misunderstanding.
- *Privacy?* No real customer data or secrets in prompts; use synthetic or masked samples.

**Common mistakes:** Accepting code because it runs, not stating the prediction time in the prompt, trusting a high CV score, letting the AI write both the code and its tests, and not being able to explain every line in the interview.

### Q50 ⭐ 🔴 Review a complete 150-line LLM-generated ML script end to end (train/test handling, CV, metric choice, threshold, seeds, logging, hidden global state) and produce a prioritised list of review comments with fixes.
**Asked at:** AI-allowed code-review rounds, senior DS/MLE
**Say this first (1 line):** I review in priority order: first anything that makes the reported number untrustworthy (leakage and a wrong split), then metric and threshold choices, then reproducibility and engineering hygiene; each comment gets a severity, the reason, and a concrete fix.

**Then explain (condensed from the 150-line script, run):**
```python
Xs = StandardScaler().fit_transform(df.drop(columns="y"))              # A
Xr, yr = RandomOverSampler().fit_resample(Xs, df.y)                    # B
Xtr, Xte, ytr, yte = train_test_split(Xr, yr, test_size=.2)            # C
rf = RandomForestClassifier(300).fit(Xtr, ytr)                         # D
print(accuracy_score(yte, rf.predict(Xte)))                            # E
best = max([0.3, 0.4, 0.5, 0.6],
           key=lambda t: accuracy_score(yte, rf.predict_proba(Xte)[:, 1] > t))   # G
```

| Priority | Comment | Fix |
|---|---|---|
| P0 | **B + C: oversampling before the split.** Copies of the same minority row land in train and test. My run printed accuracy 1.000. | Split first; resample only inside the training fold (imblearn `Pipeline`). |
| P0 | **A: scaler fitted on all rows** (including test). | `StandardScaler` inside the pipeline, fitted on train only. |
| P0 | **C: random split on time-ordered data** lets the model see the future. | Time-based holdout or `TimeSeriesSplit`; group split if entities repeat. |
| P0 | **G: threshold chosen on the test set.** The test score is now tuned. | Choose the threshold on a validation slice (out-of-time), freeze it, then score the test once. |
| P1 | **E: accuracy on ~3% positives**: predicting all negatives gives 97%. | PR-AUC, recall at a precision target, or a cost metric; always show the prevalence baseline. |
| P1 | **No baseline**, no confidence interval, one split. | Add a dummy and a logistic regression; report CV mean and spread or a bootstrap CI. |
| P2 | **D and B: no `random_state`, no seed anywhere.** Results change every run. | Seed splits, resampler and model; log the seed (see Q31). |
| P2 | **Hidden global state**: module-level DataFrames mutated by functions, `np.random.seed` in helpers, `inplace=True`. | Pass data in and out of functions, use `default_rng`, avoid in-place ops. |
| P2 | **Model saved without the preprocessing**, no version. | Save the whole pipeline plus column list and library versions (see Q32). |
| P3 | **`print` instead of logging**, magic numbers, no config, no tests. | `logging` with run id, a config dict or file, a few asserts and unit tests. |

**Example (run, this machine):** the buggy path scores accuracy 1.000. The reviewed path (time-ordered holdout, pipeline with scaler, oversampler and seeded forest inside, threshold chosen on a validation slice) gives PR-AUC 0.529 against a prevalence baseline of 0.038, and recall 0.435 at the chosen threshold 0.363. A perfect score on a rare-class task should trigger suspicion, not celebration.

**Code (fixed core):**
```python
import numpy as np, pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, precision_recall_curve
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline as ImbPipeline

X, y = make_classification(6000, 15, n_informative=4, weights=[.97], flip_y=.03, random_state=1)
df = pd.DataFrame(X); df["y"] = y                                   # assume rows are in time order
cut = int(len(df) * .8)
train, test = df.iloc[:cut], df.iloc[cut:]                          # time-ordered holdout
Xtr, ytr, Xte, yte = train.drop(columns="y"), train.y, test.drop(columns="y"), test.y
pipe = ImbPipeline([("sc", StandardScaler()), ("ros", RandomOverSampler(random_state=0)),
                    ("m", RandomForestClassifier(300, random_state=0, n_jobs=-1))])

v = int(len(train) * .75)                                           # threshold from a validation slice
pipe.fit(Xtr.iloc[:v], ytr.iloc[:v])
p, r, th = precision_recall_curve(ytr.iloc[v:], pipe.predict_proba(Xtr.iloc[v:])[:, 1])
f1 = 2 * p * r / np.maximum(p + r, 1e-9); thr = th[np.argmax(f1[:-1])]

pipe.fit(Xtr, ytr)                                                  # refit on all train, score test once
ps = pipe.predict_proba(Xte)[:, 1]
print("PR-AUC:", round(average_precision_score(yte, ps), 3), "| prevalence:", round(yte.mean(), 3),
      "| recall at thr:", round(((ps > thr) & (yte == 1)).sum() / yte.sum(), 3))
```

**Follow-ups:**
- *How do you deliver the review?* Lead with the two or three issues that invalidate results, then the rest as a short checklist; offer to pair on the fix instead of a long list of nitpicks.
- *What do you ask the author?* What is the prediction time, how will the model be used, what does a false positive cost?
- *Could an LLM do this review?* It can draft comments, but I verify each against the code, since it can miss subtle leakage or invent issues.

**Common mistakes:** Reporting style nits before leakage, fixing symptoms (lower the score by tuning) instead of the split, accepting accuracy on imbalanced data, and giving comments with no concrete fix.

### Q51 ⭐ 🔴 Use ColumnTransformer with set_output(transform='pandas'), feature names and custom column selectors to build a pipeline that survives schema evolution, and show how you would test that.
**Asked at:** Senior MLE rounds
**Say this first (1 line):** I select columns by dtype with `make_column_selector` (resolved once at fit and remembered by name), keep names through the pipeline with `set_output(transform="pandas")`, and write tests that feed the fitted pipeline frames with extra, missing, reordered, null and unseen values so I know which schema changes pass silently and which fail loudly.

**Then explain:**
- `make_column_selector(dtype_include="number")` picks columns when `fit` runs. At predict time the transformer uses the stored names, so an extra column in new data is ignored and column order does not matter.
- Side effect: when I retrain on a new schema, a newly added numeric column is automatically included as a feature. To avoid surprise features, assert the fitted feature list against an expected list in a test (or select by explicit name lists for sensitive models).
- `set_output(transform="pandas")` makes every step return a DataFrame with names, so I can inspect `pre.transform(X).columns`. Caveat: pandas output does not support sparse data, so set `OneHotEncoder(sparse_output=False)` (I hit this exact ValueError).
- `remainder="drop"` plus `verbose_feature_names_out=False` gives clean names like `city_A`; if two steps could emit the same name, keep the prefix on.
- Policy per change: extra column = ignore; missing required column = raise a clear error; unseen category = `handle_unknown="ignore"`; nulls = imputer; wrong text in a numeric column = raise.
- Also store `pipe.feature_names_in_` with the model and validate incoming frames against it (see Q32 and Q38).

**Example (run):** fitted feature list `['age', 'income', 'city_A', 'city_B', 'plan_x', 'plan_y']`. Test results: extra column ignored (True); unseen city handled (True); missing column `plan` raises ValueError; nulls in age imputed (True); reversed column order gives identical predictions (True); `income="abc"` raises ValueError; transform output names are the same as `get_feature_names_out()` (True).

**Code:**
```python
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector as selector
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

rng = np.random.default_rng(0)
train = pd.DataFrame({"age": rng.normal(40, 10, 300), "income": rng.lognormal(10, .5, 300),
                      "city": rng.choice(["A", "B"], 300), "plan": rng.choice(["x", "y"], 300)})
y = (train.income > train.income.median()).astype(int)

pre = ColumnTransformer(
    [("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), selector(dtype_include="number")),
     ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False),
      selector(dtype_include=["object", "category"]))],
    remainder="drop", verbose_feature_names_out=False).set_output(transform="pandas")
pipe = make_pipeline(pre, LogisticRegression(max_iter=500)).fit(train, y)
assert pre.get_feature_names_out().tolist() == ["age", "income", "city_A", "city_B", "plan_x", "plan_y"]

def score(frame): return pipe.predict_proba(frame)[:, 1]
new = train.sample(50, random_state=0)
def raises(frame):
    try: score(frame); return None
    except Exception as e: return type(e).__name__

print("1 extra column ignored    :", raises(new.assign(new_col=1.0)) is None)
print("2 unseen category handled :", np.isfinite(score(new.assign(city="Z"))).all())
print("3 missing column raises   :", raises(new.drop(columns="plan")))
print("4 nulls imputed           :", np.isfinite(score(new.assign(age=np.where(np.arange(50) % 2, np.nan, new.age)))).all())
print("5 column order irrelevant :", np.allclose(score(new), score(new[new.columns[::-1]])))
print("6 bad numeric text raises :", raises(new.assign(income="abc")))
```
In a real repo, turn each line into a pytest test (see Q44) and run them in CI against a saved sample of production data.

**Follow-ups:**
- *Do selectors help when a column changes dtype?* Fitting picks by dtype, so if `age` arrives as strings the stored name still goes to the numeric branch; a numeric string converts, text like "abc" raises. Validate dtypes before the model (Q38).
- *Why not `remainder="passthrough"`?* New or ID-like columns would flow into the model unnoticed.
- *Does `set_output` cost anything?* A little speed and memory (DataFrames instead of arrays), and no sparse output.

**Common mistakes:** Assuming a selector re-evaluates at predict time, relying on automatic inclusion of new columns when retraining, using positional indices, forgetting `sparse_output=False` with pandas output, and having no test that fails when the schema changes.

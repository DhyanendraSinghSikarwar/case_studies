### Q21 ⭐⭐ 🟡 Data validation tests as code. Write a validate(df) function (using pydantic, plain pandas or pandera, your choice, say why) that checks columns and dtypes, non-null keys, a value range, allowed category values and uniqueness of an id, and reports all violations at once instead of stopping at the first. Test it on a good frame and a frame with four planted problems, and say where in the pipeline it runs (ingest, before training, before serving) and what happens on failure.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** I write one `validate(df)` function in plain pandas that checks every rule, collects the problems in a list and returns them all, so the team fixes the data once instead of five times.

**Then explain:**
- Why plain pandas: no extra dependency, I control the messages, and it is easy to explain. pandera is the better pick when many people share schemas (declare once, `lazy=True` collects all failures, I cross-check it below). pydantic validates row by row, which is slow and clumsy for a big frame, so I keep it for configs and API payloads.
- Rules, in order: columns exist, dtype family is right, key not null, key unique, value in range, category in the allowed set. If a column is missing, I report it and skip the other checks on that column.
- Where it runs: at ingest (reject or quarantine the file), before training (hard stop, do not train on bad data), before serving (cheap schema check on each batch or request). Same function, different strictness.
- On failure: the job exits non-zero, an alert goes out with the violation list, and the pipeline keeps using the last good dataset or model. I never silently fill or drop rows in the validator.
- Two traps from my own run: one null turns an integer id column into float, so I use nullable `Int64` and check dtype families; and pandas 3 shows text as `str`, not `object`, so exact string dtype checks break across versions.

**Example:** The bad frame has 4 rows. `loan_id = [1, 1, NA, 4]` gives a null key and a duplicate id 1. `age = [25, 17, 130, 40]` puts rows 1 and 2 out of range. `segment` has `vip`, which is not allowed. That is four planted problems and the function reports exactly four lines. The good frame returns an empty list.

**Code:** `python3 -I q21.py`
```python
# Q21: validate(df) that reports ALL violations at once (plain pandas), plus a pandera lazy cross-check.
import pandas as pd
import pandera.pandas as pa

from pandas.api import types as T
# dtype FAMILIES, not exact strings: pandas 3 uses "str" for text, older pandas used "object"
EXPECTED = {"loan_id": ("integer", T.is_integer_dtype), "age": ("integer", T.is_integer_dtype),
            "income": ("float", T.is_float_dtype), "segment": ("string", T.is_string_dtype)}
SEGMENTS = {"retail", "sme", "corporate"}

def validate(df: pd.DataFrame) -> list[str]:
    """Return a list of human-readable violations. Empty list = valid."""
    errs = []
    # 1) columns and dtypes: if a column is missing we cannot check it further
    missing = [c for c in EXPECTED if c not in df.columns]
    errs += [f"missing column: {c}" for c in missing]
    for c, (family, is_ok) in EXPECTED.items():
        if c in df.columns and not is_ok(df[c].dtype):
            errs.append(f"dtype of {c}: expected {family}, got {df[c].dtype}")
    # 2) non-null key
    if "loan_id" in df.columns:
        n = int(df["loan_id"].isna().sum())
        if n:
            errs.append(f"loan_id has {n} null(s)")
        # 3) uniqueness of the id (ignore nulls, already reported)
        dup = df["loan_id"].dropna()
        dup = dup[dup.duplicated(keep=False)].unique().tolist()
        if dup:
            errs.append(f"loan_id not unique: {sorted(dup)}")
    # 4) value range
    if "age" in df.columns:
        bad = df.index[(df["age"] < 18) | (df["age"] > 100)].tolist()
        if bad:
            errs.append(f"age outside [18, 100] at rows {bad}")
    # 5) allowed categories
    if "segment" in df.columns:
        bad = sorted(set(df["segment"].dropna()) - SEGMENTS)
        if bad:
            errs.append(f"segment has unknown values: {bad}")
    return errs

good = pd.DataFrame({"loan_id": [1, 2, 3], "age": [25, 40, 61],
                     "income": [5.0, 7.5, 6.1], "segment": ["retail", "sme", "corporate"]})
# four planted problems: null key, duplicate id, age 17 / 130, unknown segment 'vip'
bad = pd.DataFrame({"loan_id": pd.array([1, 1, None, 4], dtype="Int64"), "age": [25, 17, 130, 40],
                    "income": [5.0, 7.5, 6.1, 4.0], "segment": ["retail", "vip", "sme", "sme"]})
print("good frame ->", validate(good))
errs = validate(bad)
print("bad frame  ->", len(errs), "violations")
for e in errs:
    print("  -", e)

# same idea with pandera, lazy=True collects every failure (version printed below)
schema = pa.DataFrameSchema({
    "loan_id": pa.Column("Int64", nullable=False, unique=True),
    "age": pa.Column(int, pa.Check.in_range(18, 100)),
    "income": pa.Column(float),
    "segment": pa.Column(str, pa.Check.isin(sorted(SEGMENTS))),
})
try:
    schema.validate(bad, lazy=True)
except pa.errors.SchemaErrors as e:
    print("pandera lazy failure cases:", len(e.failure_cases))
    print(e.failure_cases[["column", "check", "failure_case"]].to_string(index=False))
import importlib.metadata as md
print("pandera", md.version("pandera"), "pandas", pd.__version__)
assert validate(good) == [] and len(errs) == 4
```

**Output (my run):** pandas 3.0.5, pandera 0.35.0 (pandera also reports 6 failure cases because it lists duplicates and each bad age separately).
```text
good frame -> []
bad frame  -> 4 violations
  - loan_id has 1 null(s)
  - loan_id not unique: [1]
  - age outside [18, 100] at rows [1, 2]
  - segment has unknown values: ['vip']
pandera lazy failure cases: 6
 column                                check failure_case
loan_id                         not_nullable         <NA>
loan_id                     field_uniqueness            1
loan_id                     field_uniqueness            1
    age                    in_range(18, 100)           17
    age                    in_range(18, 100)          130
segment isin(['corporate', 'retail', 'sme'])          vip
pandera 0.35.0 pandas 3.0.5
```

**Follow-ups:**
- *Hard rule or warning?* Keys, schema and categories are hard rules. Distribution checks (mean shifted) are warnings with thresholds, and they belong to monitoring, not to this function.
- *Why not Great Expectations?* It is fine for big teams, but it is heavier. For a small pipeline a 30-line function plus tests is easier to own (check current docs if the team already uses it).
- *How do you test the validator?* With the good frame and one frame per rule, each asserting the exact message. A validator without tests is itself untested code.

**Common mistakes:**
- Raising on the first problem, so the data team fixes one issue per run.
- Checking `dtype == "object"` or `"int64"` as strings and breaking after a pandas upgrade or after one null appears.
- Validating after `fillna`, which hides the nulls.
- Forgetting uniqueness of the id, then joining and silently duplicating rows.

### Q22 ⭐⭐ 🟡 Write tests that catch data leakage. Using seeded data, show a leaky pipeline (scaler fitted on all rows, or duplicate rows across train and test, or a target-derived feature) and the tests that expose each: no id overlap between train and test, scaler statistics equal to train-only statistics, and an unrealistically high score alarm. Run the leaky and fixed versions with scikit-learn and report both scores.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Leakage tests check the split and the preprocessing, not just the score: no shared ids between train and test, scaler statistics equal to train-only statistics, and an alarm when the score is too good.

**Then explain:**
- Three classic leaks: fit a scaler or imputer on all rows before splitting; the same entity in both train and test (duplicates, or several rows per customer); a feature built from the target or from the future.
- Test 1, id overlap: `set(train.id) & set(test.id)` must be empty. If rows from one customer can appear twice, split by customer group, not by row.
- Test 2, scaler stats: after fitting, `scaler.mean_` must equal the train mean. Scale-before-split leaks only a little, so the score barely moves (my run shows 0.708 vs 0.708). The stats test still catches it. A score alarm would not.
- Test 3, score alarm: if AUC is far above what this problem allows, stop and look for leakage. The ceiling is a judgement per problem; mine is 0.90 for a weak-signal task.
- Best fix is structural: put the scaler inside a `Pipeline` and use `GroupKFold` or a split by id, so the leak cannot be written by accident.

**Example:** Seed 0, 400 rows, `x1` weakly predicts `y`. I duplicate 100 rows before the split, so 41 ids land in both train and test; a RandomForest memorises them and reports AUC 0.841 against an honest 0.576. A feature `leak = 5*y + noise` gives AUC 1.000 against an honest 0.708. All of this is in the output below.

**Code:** `python3 -I q22.py`
```python
# Q22: leaky vs fixed pipelines, plus tests that expose each leak. Seeded, scikit-learn.
import numpy as np, pandas as pd, sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

SEED = 0
rng = np.random.default_rng(SEED)
n = 400
df = pd.DataFrame({"id": np.arange(n), "x1": rng.normal(size=n), "x2": rng.normal(10, 5, size=n)})
df["y"] = (0.3 * df.x1 + rng.normal(size=n) > 0).astype(int)   # weak signal on purpose
FEATS = ["x1", "x2"]

def auc(tr, te, feats):
    m = LogisticRegression().fit(tr[feats], tr["y"])
    return roc_auc_score(te["y"], m.predict_proba(te[feats])[:, 1])

# ---- tests (plain functions that return None or raise AssertionError) ----
def test_no_id_overlap(tr, te):
    both = set(tr["id"]) & set(te["id"])
    assert not both, f"{len(both)} ids in both train and test"

def test_scaler_uses_train_only(scaler, tr):
    assert np.allclose(scaler.mean_, tr[FEATS].mean().to_numpy()), "scaler mean != train mean"

def test_score_not_suspicious(score, ceiling=0.90):
    assert score < ceiling, f"AUC {score:.3f} >= {ceiling}: too good for this problem, look for leakage"

def run(name, checks):
    bad = []
    for label, fn in checks:
        try: fn()
        except AssertionError as e: bad.append(f"{label}: {e}")
    print(f"  {name}: " + ("all tests pass" if not bad else f"{len(bad)} test(s) FAIL"))
    for b in bad: print("     -", b)

# ---- leak 1: scaler fitted on ALL rows before the split ----
tr, te = train_test_split(df, test_size=0.25, random_state=SEED)
leaky_sc = StandardScaler().fit(df[FEATS])                      # sees test rows
good_sc = StandardScaler().fit(tr[FEATS])
print("1) scaler fitted before the split")
run("leaky", [("scaler stats", lambda: test_scaler_uses_train_only(leaky_sc, tr))])
run("fixed", [("scaler stats", lambda: test_scaler_uses_train_only(good_sc, tr))])

# ---- leak 2: duplicate rows across train and test (same id appears twice before split) ----
dup = pd.concat([df, df.sample(100, random_state=SEED)], ignore_index=True)   # 100 rows duplicated
tr_d, te_d = train_test_split(dup, test_size=0.25, random_state=SEED)
tr_f, te_f = train_test_split(df, test_size=0.25, random_state=SEED)           # dedupe first = split by id
# a flexible model memorises duplicates, so use a tree to show the effect
from sklearn.ensemble import RandomForestClassifier
def auc_rf(tr_, te_, feats):
    m = RandomForestClassifier(n_estimators=100, random_state=SEED).fit(tr_[feats], tr_["y"])
    return roc_auc_score(te_["y"], m.predict_proba(te_[feats])[:, 1])
s_leak, s_fix = auc_rf(tr_d, te_d, FEATS), auc_rf(tr_f, te_f, FEATS)
print("2) duplicate rows across train/test")
run("leaky", [("id overlap", lambda: test_no_id_overlap(tr_d, te_d))])
run("fixed", [("id overlap", lambda: test_no_id_overlap(tr_f, te_f))])
print(f"   RandomForest AUC leaky={s_leak:.3f} fixed={s_fix:.3f}")

# ---- leak 3: a target-derived feature (e.g. 'refund_amount' only exists when y = 1) ----
df3 = df.assign(leak=df["y"] * 5 + rng.normal(0, 0.1, size=n))
tr3, te3 = train_test_split(df3, test_size=0.25, random_state=SEED)
s3_leak = auc(tr3, te3, FEATS + ["leak"]); s3_fix = auc(tr3, te3, FEATS)
print("3) target-derived feature")
run("leaky", [("score alarm", lambda: test_score_not_suspicious(s3_leak))])
run("fixed", [("score alarm", lambda: test_score_not_suspicious(s3_fix))])
print(f"   LogisticRegression AUC leaky={s3_leak:.3f} fixed={s3_fix:.3f}")

# ---- leak 1 score effect (small, honest): scaling leak rarely changes AUC much ----
def auc_scaled(sc):
    Xtr, Xte = sc.transform(tr[FEATS]), sc.transform(te[FEATS])
    m = LogisticRegression().fit(Xtr, tr["y"]); return roc_auc_score(te["y"], m.predict_proba(Xte)[:, 1])
print(f"1b) scaler-leak AUC leaky={auc_scaled(leaky_sc):.3f} fixed={auc_scaled(good_sc):.3f}  (the stats test catches it even when the score barely moves)")
print("seed", SEED, "numpy", np.__version__, "pandas", pd.__version__, "sklearn", sklearn.__version__)
```

**Output (my run):** Python 3.13, scikit-learn 1.9.1, numpy 2.5.3, pandas 3.0.5, seed 0.
```text
1) scaler fitted before the split
  leaky: 1 test(s) FAIL
     - scaler stats: scaler mean != train mean
  fixed: all tests pass
2) duplicate rows across train/test
  leaky: 1 test(s) FAIL
     - id overlap: 41 ids in both train and test
  fixed: all tests pass
   RandomForest AUC leaky=0.841 fixed=0.576
3) target-derived feature
  leaky: 1 test(s) FAIL
     - score alarm: AUC 1.000 >= 0.9: too good for this problem, look for leakage
  fixed: all tests pass
   LogisticRegression AUC leaky=1.000 fixed=0.708
1b) scaler-leak AUC leaky=0.708 fixed=0.708  (the stats test catches it even when the score barely moves)
seed 0 numpy 2.5.3 pandas 3.0.5 sklearn 1.9.1
```

**Follow-ups:**
- *Time series?* Split by time (train on past, test on future) and add a test that `max(train.date) < min(test.date)`.
- *Cross-validation?* Put preprocessing inside the `Pipeline` passed to `cross_val_score`, so each fold refits it on its own training part.
- *Is a high score always a leak?* No. It is a reason to investigate. Some tasks are easy. The alarm triggers a human, not an automatic failure of the model.

**Common mistakes:**
- Fitting `StandardScaler`, `SimpleImputer` or target encoding on the whole dataset first.
- Random row split when the same customer has many rows.
- Tuning hyperparameters on the test set and then calling it unbiased.
- Trusting a good score without a baseline to compare against.

### Q23 ⭐⭐ 🟡 Property-based testing with Hypothesis for ML utilities. Write properties for a min-max scaler and a train/test splitter (output in [0,1] when the input is non-constant, order of rows preserved or not, sizes add up, no row lost or duplicated) and let Hypothesis find a failing edge case in a deliberately naive implementation (constant column, a single row, NaN or inf). Run it and show the shrunk counterexample. Say when this is worth the effort versus example tests.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Property-based testing states a rule that must hold for all inputs (output in [0, 1], sizes add up, no row lost), and Hypothesis generates many inputs, finds one that breaks the rule and shrinks it to the smallest example.

**Then explain:**
- Properties for a min-max scaler: same length out, every value in [0, 1] for finite input, bigger input never gives smaller output, and a defined behaviour for constant columns and NaN or inf (raise or return zeros, but never silent NaN).
- Properties for a splitter: train plus test sizes equal n, every index appears exactly once (no loss, no duplicate), both sides non-empty when n >= 2, same seed gives the same split.
- In my run the naive scaler failed on `[0.0]` (a single row is also a constant column: 0/0 gives NaN) and on `[nan]`. The naive splitter sampled with replacement and truncated with `int()`, so it failed on `n=15` (9 + 7 rows is not 15, and index 4 is duplicated) and on `n=2` (empty test set).
- The monotone property passed for both, which is a useful result too: it tells me that part is safe.
- Worth it for pure functions with clear rules: scalers, splitters, encoders, metric code, parsers. Not worth it for plumbing, IO, or model training. Example tests stay for known regression cases.

**Example:** Hand-check the shrunk case: `minmax([0.0])` computes `(0 - 0) / (0 - 0) = 0/0 = nan`, and `nan >= 0` is False, so the property fails. For the splitter, `n=2, frac=0.25`: `int(2 * 0.25) = 0`, so the test set is empty.

**Code:** `IMPL=impl_naive` or `IMPL=impl_fixed` picks which implementation the same tests run against. `derandomize=True` makes the run repeatable.
```python
# ===== file: impl_naive.py =====
import numpy as np

def minmax(x):
    x = np.asarray(x, dtype=float)
    return (x - x.min()) / (x.max() - x.min())          # constant column -> 0/0

def split_idx(n, test_frac, seed):
    rng = np.random.default_rng(seed)
    n_test = int(n * test_frac)                          # truncates: n=2, 0.2 -> 0 test rows
    test = rng.integers(0, n, size=n_test)               # sampling WITH replacement -> duplicates
    train = np.setdiff1d(np.arange(n), test)
    return train, test

# ===== file: impl_fixed.py =====
import numpy as np

def minmax(x):
    x = np.asarray(x, dtype=float)
    if x.size == 0 or not np.isfinite(x).all():
        raise ValueError("minmax needs a non-empty array of finite numbers")
    lo, hi = x.min(), x.max()
    if hi == lo:
        return np.zeros_like(x)                          # documented choice: constant column -> all 0.0
    return (x - lo) / (hi - lo)

def split_idx(n, test_frac, seed):
    if n < 2:
        raise ValueError("need at least 2 rows to split")
    n_test = min(max(round(n * test_frac), 1), n - 1)    # both sides non-empty
    perm = np.random.default_rng(seed).permutation(n)    # without replacement
    return np.sort(perm[n_test:]), np.sort(perm[:n_test])

# ===== file: test_props.py =====
import importlib, os
import numpy as np
from hypothesis import assume, given, settings, strategies as st

impl = importlib.import_module(os.environ["IMPL"])
S = settings(derandomize=True, database=None, max_examples=200)   # same run every time
finite = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False)
arrays = st.lists(finite, min_size=1, max_size=20)

@S
@given(arrays)
def test_minmax_in_unit_interval(xs):
    out = impl.minmax(xs)
    assert out.shape == (len(xs),)
    assert np.all((out >= 0) & (out <= 1)), out          # also fails on NaN

@S
@given(arrays)
def test_minmax_is_monotone(xs):
    assume(len(set(xs)) > 1)                              # constant columns are a separate rule
    x, out = np.asarray(xs), impl.minmax(xs)
    order = np.argsort(x, kind="stable")
    assert (np.diff(out[order]) >= 0).all()               # bigger input never gives smaller output

@S
@given(st.lists(st.sampled_from([float("nan"), float("inf"), -float("inf"), 1.0, 2.0]), min_size=1, max_size=5))
def test_minmax_rejects_non_finite_or_returns_finite(xs):
    try:
        out = impl.minmax(xs)
    except ValueError:
        return
    assert np.isfinite(out).all(), out                  # never hand NaN downstream silently

split_args = dict(n=st.integers(2, 50), frac=st.floats(0.05, 0.95), seed=st.integers(0, 2**32 - 1))

@S
@given(**split_args)
def test_split_sizes_add_up_no_loss_no_dup(n, frac, seed):
    tr, te = impl.split_idx(n, frac, seed)
    assert len(tr) + len(te) == n, (len(tr), len(te))
    assert sorted(np.concatenate([tr, te]).tolist()) == list(range(n))   # every row exactly once

@S
@given(**split_args)
def test_split_both_sides_non_empty(n, frac, seed):
    tr, te = impl.split_idx(n, frac, seed)
    assert len(tr) > 0 and len(te) > 0

@S
@given(**split_args)
def test_split_is_deterministic(n, frac, seed):
    a, b = impl.split_idx(n, frac, seed), impl.split_idx(n, frac, seed)
    assert all(np.array_equal(p, q) for p, q in zip(a, b))
```
```bash
IMPL=impl_naive python3 -I -m pytest -q -p no:cacheprovider --tb=short test_props.py
IMPL=impl_fixed python3 -I -m pytest -q -p no:cacheprovider --tb=short test_props.py
```

**Output (my run):** naive output is trimmed (warnings and long assertion helpers removed); hypothesis 6.170.11, pytest 9.1.1, numpy 2.5.3. The `n=15` split case did not shrink further because that failure depends on the random draw.
```text
$ IMPL=impl_naive python3 -I -m pytest -q -p no:cacheprovider --tb=short test_props.py
F.FFF.                                                                   [100%]
=================================== FAILURES ===================================
_________________________ test_minmax_in_unit_interval _________________________
test_props.py:11: in test_minmax_in_unit_interval
test_props.py:15: in test_minmax_in_unit_interval
    assert np.all((out >= 0) & (out <= 1)), out          # also fails on NaN
E   AssertionError: array([nan])
E   assert np.False_
E   Failing test case: test_minmax_in_unit_interval(
E       xs=[0.0],
E   )
_______________ test_minmax_rejects_non_finite_or_returns_finite _______________
test_props.py:26: in test_minmax_rejects_non_finite_or_returns_finite
test_props.py:32: in test_minmax_rejects_non_finite_or_returns_finite
    assert np.isfinite(out).all(), out                  # never hand NaN downstream silently
E   AssertionError: array([nan])
E   assert np.False_
E   Failing test case: test_minmax_rejects_non_finite_or_returns_finite(
E       xs=[nan],
E   )
____________________ test_split_sizes_add_up_no_loss_no_dup ____________________
test_props.py:37: in test_split_sizes_add_up_no_loss_no_dup
test_props.py:40: in test_split_sizes_add_up_no_loss_no_dup
    assert len(tr) + len(te) == n, (len(tr), len(te))
E   AssertionError: (9, 7)
E   assert (9 + 7) == 15
E   Failing test case: test_split_sizes_add_up_no_loss_no_dup(
E       n=15,
E       frac=0.5,
E       seed=0,
E   )
_______________________ test_split_both_sides_non_empty ________________________
test_props.py:44: in test_split_both_sides_non_empty
test_props.py:47: in test_split_both_sides_non_empty
    assert len(tr) > 0 and len(te) > 0
E   assert (2 > 0 and 0 > 0)
E   Failing test case: test_split_both_sides_non_empty(
E       n=2,
E       frac=0.25,
E       seed=0,  # or any other generated value
E   )
=========================== short test summary info ============================
FAILED test_props.py::test_minmax_in_unit_interval - AssertionError: array([n...
FAILED test_props.py::test_minmax_rejects_non_finite_or_returns_finite - Asse...
FAILED test_props.py::test_split_sizes_add_up_no_loss_no_dup - AssertionError...
FAILED test_props.py::test_split_both_sides_non_empty - assert (2 > 0 and 0 > 0)
4 failed, 2 passed, 38 warnings in 2.60s
hypothesis 6.170.11 pytest 9.1.1 numpy 2.5.3

$ IMPL=impl_fixed python3 -I -m pytest -q -p no:cacheprovider --tb=short test_props.py
......                                                                   [100%]
6 passed in 1.78s
hypothesis 6.170.11 pytest 9.1.1 numpy 2.5.3
```

**Follow-ups:**
- *Why does Hypothesis try NaN and inf?* Because real data has them. That is the point: it explores the places I forgot.
- *How do I replay a failure?* Hypothesis keeps a database of failing examples locally and prints a reproduce hint. I also turn a found case into a normal example test so the regression stays pinned.
- *Float roundoff?* Compare with `pytest.approx` or `np.isclose`. Also note that tiny differences can collapse into the same scaled value, so I test "non-decreasing", not "strictly increasing".

**Common mistakes:**
- Writing a property that just re-implements the function, so it can never fail.
- Unbounded floats, which find overflow in every function and bury the real rules (I bounded floats to +/- 1e6 on purpose).
- Leaving the test random in CI with no seed policy, then being unable to reproduce.
- Using Hypothesis everywhere. It costs run time and thinking time.

### Q24 ⭐⭐ 🟡 Test coverage in ML repos. A repo reports 92 percent line coverage but a bad scaling bug shipped. Explain line versus branch coverage, why coverage does not measure assertions or data coverage, what a sensible target and a diff-coverage rule look like, and how to run coverage with pytest-cov and fail under a threshold. Show a tiny function where 100 percent line coverage still misses a bug, with the run.
**Asked at:** ML testing write-ups (Eugene Yan 'How to Test Machine Learning Code and Systems', Marvelous MLOps 'How to test ML code?', MLOps Zoomcamp testing notes, the Breck et al. ML Test Score paper; search snippets only, not opened); educational articles, not interview reports; ML engineer and MLOps code-quality and testing rounds
**Say this first (1 line):** Coverage only tells me which lines ran during tests, not whether the tests checked anything or used the right data, so 92 percent coverage can still ship a scaling bug.

**Then explain:**
- Line coverage: was this line executed. Branch coverage: was each side of every `if` taken. Branch is stricter and I turn it on (`--cov-branch`).
- What it cannot see: missing assertions, wrong expected values, and data coverage. A scaler tested only with `lo = 0` runs every line and never notices a wrong formula.
- Sensible target: a floor around the team's current level (often 70-85 percent; no magic number), a fail-under so it never drops, and a diff-coverage rule: new or changed lines in a PR must be covered (for example 80 percent or more). Diff coverage punishes new untested code and does not force teams to chase old code.
- Honest use: coverage finds untested code. It does not prove tested code is right. Pair it with property tests, regression tests on real examples, and review.
- In ML repos watch for the big blind spots: data issues, training loops marked `# pragma: no cover`, and notebooks that are not measured at all.

**Example:** `scale(x, lo, hi)` returns `(x - lo) / hi`; it should divide by `hi - lo`. One test, `scale(5, 0, 10, clip=True) == 0.5`, passes because `lo = 0` hides the bug. Line coverage is 100 percent, branch coverage is 86 percent (the `clip=False` path was never taken), and the bug is still there. A second test with `lo = 10` fails: expected 0.5, got 0.25. The bug was found by a better test, not by any coverage number.

**Code:** the function and tests, the commands, and the diff-coverage demo (temp git repo).
```python
# ===== file: scaling.py =====
def scale(x, lo, hi, clip=False):
    out = (x - lo) / hi              # BUG: should divide by (hi - lo)
    if clip:
        out = min(max(out, 0.0), 1.0)
    return out

# ===== file: test_scaling.py =====
from scaling import scale

def test_scale_clip():
    assert scale(5, 0, 10, clip=True) == 0.5     # lo = 0 hides the bug

# ===== file: test_scaling_more.py =====
from scaling import scale

def test_scale_nonzero_lo():
    assert scale(15, 10, 20) == 0.5              # (15-10)/(20-10); the buggy code gives 0.25
```
```bash
# line coverage, then branch coverage, both failing under 100
python3 -I -m pytest -q -p no:cacheprovider --cov=scaling --cov-report=term-missing --cov-fail-under=100 test_scaling.py
python3 -I -m pytest -q -p no:cacheprovider --cov=scaling --cov-branch --cov-report=term-missing --cov-fail-under=100 test_scaling.py
# diff coverage in a throwaway git repo (needs: pip install diff-cover)
python3 -I -m pytest -q --cov=lib --cov-report=xml test_lib.py
diff-cover coverage.xml --compare-branch=main~1 --fail-under=80
```

**Output (my run):** coverage 7.17.0, pytest-cov 7.1.0, diff-cover 10.6.0. First the three runs, then the diff-coverage run: the PR added a 4-line function with no test, so 1 of 4 new lines is covered (25 percent) and the gate fails.
```text
$ python3 -I -m pytest -q -p no:cacheprovider --cov=scaling --cov-report=term-missing --cov-fail-under=100 test_scaling.py   # line coverage only
.                                                                        [100%]
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.13.17-final-0 _______________

Name         Stmts   Miss  Cover   Missing
------------------------------------------
scaling.py       5      0   100%
------------------------------------------
TOTAL            5      0   100%
Required test coverage of 100% reached. Total coverage: 100.00%
1 passed in 0.16s
exit=0

$ ... --cov-branch   # same tests, branch coverage on
.
ERROR: Coverage failure: total of 86 is less than fail-under=100
                                                                         [100%]
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.13.17-final-0 _______________

Name         Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------
scaling.py       5      0      2      1    86%   3->5
--------------------------------------------------------
TOTAL            5      0      2      1    86%
FAIL Required test coverage of 100% not reached. Total coverage: 85.71%
1 passed in 0.13s
exit=1

$ add a test with lo != 0 -> the bug shows up (coverage was never the thing that could catch it)
.F                                                                       [100%]
=================================== FAILURES ===================================
E   assert 0.25 == 0.5
     +  where 0.25 = scale(15, 10, 20)
/home/user/case_studies/interviews/scratch/B4P01_Q21-30/code/q24/test_scaling_more.py:4: assert 0.25 == 0.5
=========================== short test summary info ============================
FAILED test_scaling_more.py::test_scale_nonzero_lo - assert 0.25 == 0.5
1 failed, 1 passed in 0.13s
exit=1
coverage 7.17.0 pytest-cov 7.1.0


Coverage XML written to file coverage.xml
1 passed in 0.14s
$ diff-cover coverage.xml --compare-branch=main~1 --fail-under=80
-------------
Diff Coverage
Diff: main~1...HEAD, staged and unstaged changes
-------------
lib.py (25.0%): Missing lines 5-7
-------------
Total:   4 lines
Missing: 3 lines
Coverage: 25%
-------------

Failure. Coverage is below 80%.
exit=1
```

**Follow-ups:**
- *Is 100 percent a good target?* No. It pushes people to write assertion-free tests. A fail-under floor plus a diff rule works better.
- *How do you measure test quality instead?* Mutation testing (tools like mutmut; concept, not run here) changes the code and checks that a test fails. That catches the `/ hi` bug.
- *Where does the threshold live?* In `pyproject.toml` or CI config, so it is the same on every laptop and in CI.

**Common mistakes:**
- Treating the coverage percent as a quality score.
- Counting tests that call the function but assert nothing.
- Only using the easy input (`lo = 0`, no NaN, balanced classes).
- Excluding hard code with `# pragma: no cover` until the number looks good.

### Q25 ⭐⭐ 🟡 Use git bisect to find the commit that broke the model. Accuracy dropped between a good tag v1.0 and the current HEAD across 12 commits. Show a throwaway repo with a deterministic test script, then run git bisect start/good/bad and git bisect run to locate the first bad commit and count the steps. Say how you handle commits that cannot build (git bisect skip) and why a flaky test breaks bisect.
**Asked at:** Editorial Git interview lists (GoLinuxCloud, Naukri Code360, Vskills, PhoenixNAP and DataCamp merge-vs-rebase pages; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** I give Git one good commit and one bad commit plus a script that exits 0 for good and 1 for bad, and `git bisect run` finds the first bad commit by binary search in about log2 of N steps.

**Then explain:**
- Setup: `git bisect start HEAD v1.0`. The first commit is bad, the second is good. Git checks out the middle commit, runs my script, reads the exit code, and halves the range.
- Exit codes: 0 means good, 1 to 127 (except 125) means bad, 125 means "cannot test this commit, skip it". A commit that does not compile or install is a skip, not a bad.
- Steps: 12 commits after the tag means about 4 tests instead of 12. My run tested 5 commits because one of them was a skip.
- The script must be deterministic: seeded data, fixed threshold on the metric, no network. A threshold like "accuracy >= 0.85" is better than "accuracy equals 0.885".
- A flaky test breaks bisect, because one wrong answer sends Git into the wrong half and it names a confident, wrong commit. My demo makes the check lie once and Git blames c8 instead of c9. Fix: make it deterministic, or run it several times in the script and only exit 1 when it fails every time.

**Example:** A tag `v1.0` has accuracy 0.885. Twelve commits later HEAD has 0.615. Commit c6 does not compile (syntax error), c7 fixes it, and c9 changes `scale` from 1.0 to 0.6 in `cfg.json`. Bisect skips c6 and returns `c9` as the first bad commit. Hand-check: with scale 0.6 a class-1 point needs x >= 0.833 to pass the 0.5 threshold, so most class-1 rows are wrong and accuracy falls from 0.885 to 0.615 (the HEAD line in the output).

**Code:** the whole demo, run in a temp repo with fixed commit dates, so the hashes and the bisect path are the same every run.
```bash
set -e
D=$(mktemp -d); cd "$D"
export GIT_AUTHOR_DATE="2026-01-01T00:00:00+0000" GIT_COMMITTER_DATE="2026-01-01T00:00:00+0000"   # fixed dates: same hashes every run
git init -q -b main; git config user.email a@b.c; git config user.name demo
# the "model": threshold classifier on 200 seeded points; accuracy must stay >= 0.85
cat > train.py <<'PY'
import random, json
random.seed(0)
cfg = json.load(open("cfg.json"))
pts = [(random.random() * 0.55, 0) for _ in range(100)] + [(0.45 + random.random() * 0.55, 1) for _ in range(100)]
# class 0 lives in [0,0.55), class 1 in [0.45,1): a little overlap, so ~0.9 accuracy at threshold 0.5
hits = sum((x * cfg["scale"] >= cfg["threshold"]) == bool(y) for x, y in pts)
print(f"accuracy={hits/len(pts):.3f}")
PY
cat > check.sh <<'SH'
#!/bin/sh
# exit 0 = good, 1 = bad, 125 = cannot test this commit (skip)
python3 -I -m py_compile train.py 2>/dev/null || exit 125
acc=$(python3 -I train.py | sed 's/accuracy=//')
python3 -I -c "import sys; sys.exit(0 if float('$acc') >= 0.85 else 1)"
SH
chmod +x check.sh
echo '{"threshold": 0.5, "scale": 1.0}' > cfg.json
git add .; git commit -qm "v1.0 baseline"; git tag v1.0
echo "baseline: $(python3 -I train.py)"
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
  case $i in
    6) echo 'def broken(:' >> train.py ;;                                   # c6: does not even compile
    7) sed -i '$d' train.py ;;                                              # c7: fixes the syntax error
    9) echo '{"threshold": 0.5, "scale": 0.6}' > cfg.json ;;               # c9: the real culprit (bad scale)
    *) echo "# note $i" >> README.md ;;
  esac
  git add -A; git commit -qm "c$i"
done
echo "HEAD:     $(python3 -I train.py)"
echo; echo '$ git bisect start HEAD v1.0 && git bisect run ./check.sh'
git bisect start HEAD v1.0 >/dev/null
git bisect run ./check.sh > run.log 2>&1 || true
grep -E "^(Bisecting|running)|is the first bad commit|^    c[0-9]+$" run.log | sed -E 's#^running .*check.sh.*#running ./check.sh#; s/^[0-9a-f]{40} is/<sha> is/'
echo "commits tested by the script (one of them skipped): $(git bisect log | grep -c "^git bisect \(good\|bad\|skip\)")"
git bisect log | grep -E "^(# (good|bad|skip)|git bisect (good|bad|skip))" | sed -E 's/\[[0-9a-f]{40}\]//; s/git bisect (good|bad|skip) [0-9a-f]{40}/git bisect \1 <sha>/' | grep '^#' 
git bisect reset >/dev/null 2>&1
echo; echo '--- a flaky check blames the wrong commit (deterministic demo: it lies once, on its 3rd call) ---'
cat > flaky.sh <<'SH'
#!/bin/sh
n=$(cat /tmp/_flaky_count 2>/dev/null || echo 0); n=$((n+1)); echo $n > /tmp/_flaky_count
[ "$n" -eq 3 ] && exit 1          # lies once: reports 'bad' for a good commit
exec ./check.sh
SH
chmod +x flaky.sh; rm -f /tmp/_flaky_count
git bisect start HEAD v1.0 >/dev/null
git bisect run ./flaky.sh > flaky.log 2>&1 || true
grep -E "first bad|could be any|^[0-9a-f]{40} |^    c[0-9]+$" flaky.log | sed -E "s/^[0-9a-f]{40} /<sha> /"
git bisect reset >/dev/null 2>&1; rm -f /tmp/_flaky_count
git --version
```

**Output (my run):** git 2.43.0. Five commits tested (c6 skipped, c3 good, c8 good, c10 bad, c9 bad), culprit c9. Short hashes are replaced with `<sha>`.
```text
baseline: accuracy=0.885
HEAD:     accuracy=0.615

$ git bisect start HEAD v1.0 && git bisect run ./check.sh
running ./check.sh
Bisecting: 5 revisions left to test after this (roughly 3 steps)
running ./check.sh
Bisecting: 3 revisions left to test after this (roughly 2 steps)
running ./check.sh
Bisecting: 1 revision left to test after this (roughly 1 step)
running ./check.sh
Bisecting: 0 revisions left to test after this (roughly 0 steps)
running ./check.sh
<sha> is the first bad commit
    c9
commits tested by the script (one of them skipped): 5
# bad:  c12
# good:  v1.0 baseline
# skip:  c6
# good:  c3
# good:  c8
# bad:  c10
# bad:  c9

--- a flaky check blames the wrong commit (deterministic demo: it lies once, on its 3rd call) ---
<sha> is the first bad commit
    c8
bisect found first bad commit
git version 2.43.0
```

**Follow-ups:**
- *What if the tag is not good?* Bisect only works if the good commit is really good. Check it first by running the script on it.
- *Can I bisect a metric, not a pass/fail?* Yes: the script computes the metric and exits 1 below a threshold. Pick the threshold with margin so noise cannot flip it.
- *How do I finish?* `git bisect reset` returns to where I started. Then I write a regression test so the fix stays.

**Common mistakes:**
- Using an unseeded training run as the check, so results flip between runs.
- Marking a broken build as bad instead of skipping it, so Git blames the build break.
- Forgetting `git bisect reset` and committing on a detached HEAD.
- Not saving the real culprit: after bisect, add a regression test, or the bug can return.

### Q26 ⭐⭐ 🟡 Git hooks and the pre-commit framework for data science teams. Configure hooks that strip notebook outputs, block files larger than 5 MB, detect obvious secrets in staged changes (a regex-based hook, hedge on tools) and run ruff. Show the .pre-commit-config.yaml, a commit that gets blocked and one that passes, and explain how the same checks must also run in CI because local hooks can be bypassed.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** I put the checks in `.pre-commit-config.yaml` so they run on every `git commit` (strip notebook outputs, block big files, block obvious secrets, lint with ruff), and I run the same config in CI because anyone can skip local hooks.

**Then explain:**
- pre-commit runs each hook on the staged files only, so it is fast. If a hook modifies files (nbstripout, ruff `--fix`) the commit fails once, and I `git add` and commit again.
- My four hooks: `nbstripout` cleans notebooks (small diffs, no leaked data in outputs); a 5 MB size check points to DVC or Git LFS; a regex secrets check; `ruff check`.
- The regex secrets hook is a tripwire, not a scanner. It misses many leaks and gives false alarms. Real teams use a maintained secret scanner (for example detect-secrets or gitleaks; check current docs) and also rotate any key that ever reached a commit.
- Hooks can be bypassed (`git commit --no-verify`) or never installed. So CI runs `pre-commit run --all-files`, and branch protection (hosted-service setting, check current docs) makes that check required.
- For a demo that runs offline I used `repo: local` hooks. In a real repo most teams pin published hook repos with `rev:` and keep the versions updated.

**Example:** My first commit adds a notebook with an output, a 6 MB file, `API_KEY = "sk_live_abcdef123456"` and a script with an unused import. All four hooks fail: nbstripout rewrites the notebook, the size check names `big.bin` (6.0 MB), the secrets check flags `config.py:1`, and ruff reports F401 for `train.py`. After removing the big file, reading the key from the environment, deleting the import and re-adding the cleaned notebook, the second commit passes all four.

**Code:** config, the two hook scripts, and the demo run in a temp git repo.
```yaml
# .pre-commit-config.yaml  (all hooks are "local" so this demo runs offline)
# In a real repo you would normally pin published hook repos with rev: (check current docs).
repos:
  - repo: local
    hooks:
      - id: nbstripout
        name: strip notebook outputs
        entry: nbstripout
        language: system
        files: \.ipynb$
      - id: no-big-files
        name: block files larger than 5 MB
        entry: python3 -I tools/check_big_files.py
        language: system
        pass_filenames: true
      - id: no-secrets
        name: block obvious secrets (regex, not a real scanner)
        entry: python3 -I tools/check_secrets.py
        language: system
        pass_filenames: true
      - id: ruff
        name: ruff lint
        entry: ruff check --isolated --select E,F
        language: system
        types: [python]
        exclude: ^tools/
```
```python
# ===== file: check_big_files.py =====
import os, sys
LIMIT = 5 * 1024 * 1024
bad = [f for f in sys.argv[1:] if os.path.getsize(f) > LIMIT]
for f in bad:
    print(f"{f}: {os.path.getsize(f)/1024/1024:.1f} MB > 5 MB (use DVC or Git LFS instead)")
sys.exit(1 if bad else 0)

# ===== file: check_secrets.py =====
import re, sys
# deliberately small; real teams use a maintained scanner (detect-secrets, gitleaks, ...). Check current docs.
PATTERNS = [r"AKIA[0-9A-Z]{16}", r"(?i)(api[_-]?key|secret|password|token)\s*[=:]\s*['\"][^'\"]{8,}['\"]",
            r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"]
bad = 0
for f in sys.argv[1:]:
    try: text = open(f, errors="ignore").read()
    except OSError: continue
    for i, line in enumerate(text.splitlines(), 1):
        if any(re.search(p, line) for p in PATTERNS):
            print(f"{f}:{i}: looks like a secret"); bad = 1
sys.exit(bad)
```
```bash
set -e
D=$(mktemp -d); cd "$D"
git init -q -b main; git config user.email a@b.c; git config user.name demo
cp "$1/pre-commit-config.yaml" .pre-commit-config.yaml; cp -r "$1/tools" tools
git add -A; git commit -qm "add hooks" --no-verify
pre-commit install | sed "s#$D#<repo>#"
# a notebook with an output, a 6 MB file, a fake key, and a lint error
python3 -I - <<'PY'
import json
nb = {"cells":[{"cell_type":"code","execution_count":1,"metadata":{},"source":["print(1)"],
       "outputs":[{"output_type":"stream","name":"stdout","text":["1\n"]}]}],
      "metadata":{},"nbformat":4,"nbformat_minor":5}
json.dump(nb, open("eda.ipynb","w"))
open("big.bin","wb").write(b"0"*(6*1024*1024))
open("config.py","w").write('API_KEY = "sk_live_abcdef123456"\n')
open("train.py","w").write("import os\nprint('hi')\n")      # unused import -> ruff F401
PY
git add -A
echo '$ git commit -m "add eda"      # should be BLOCKED'
git commit -m "add eda" 2>&1 | sed -E 's/^(.{0,100}).*/\1/' | grep -v -e '^$' -e 'MissingIDField' -e '_validate(nbdict' || true
echo; echo "--- fix each problem ---"
git rm -q --cached big.bin; rm big.bin
printf 'import os\nAPI_KEY = os.environ["API_KEY"]\n' > config.py
printf 'print("hi")\n' > train.py
git add -A            # nbstripout already cleaned eda.ipynb in the working tree during the failed run
echo '$ git commit -m "add eda"      # second try'
git commit -m "add eda" 2>&1 | sed -E 's/^(.{0,100}).*/\1/' | grep -v -e '^$' -e 'MissingIDField' -e '_validate(nbdict' || true
echo; echo '--- bypass is possible: git commit --no-verify. So CI runs the same hooks: ---'
echo '$ pre-commit run --all-files   # same config, run in CI'
pre-commit run --all-files 2>&1 | grep -v -e '^$' -e 'MissingIDField' -e '_validate(nbdict' || true
git log --oneline | cat
git show --stat --format=%s HEAD | head -5
python3 -I -c "import json,subprocess; nb=json.loads(subprocess.check_output(['git','show','HEAD:eda.ipynb'])); print('outputs in the committed notebook:', nb['cells'][0]['outputs'])"
```

**Output (my run):** pre-commit 4.7.0, ruff 0.16.9, nbstripout 0.9.1. The config also parses with pyyaml (4 hooks). Warnings from nbstripout about missing cell ids are filtered out. The commit hash is from this run.
```text
pre-commit installed at .git/hooks/pre-commit
$ git commit -m "add eda"      # should be BLOCKED
strip notebook outputs...................................................Failed
- hook id: nbstripout
- files were modified by this hook
block files larger than 5 MB.............................................Failed
- hook id: no-big-files
- exit code: 1
big.bin: 6.0 MB > 5 MB (use DVC or Git LFS instead)
block obvious secrets (regex, not a real scanner)........................Failed
- hook id: no-secrets
- exit code: 1
config.py:1: looks like a secret
ruff lint................................................................Failed
- hook id: ruff
- exit code: 1
F401 [*] `os` imported but unused
 --> train.py:1:8
  |
1 | import os
  |        ^^
2 | print('hi')
  |
help: Remove unused import: `os`
  |
  - import os
1 | print('hi')
  |
Found 1 error.
[*] 1 fixable with the `--fix` option.

--- fix each problem ---
$ git commit -m "add eda"      # second try
strip notebook outputs...................................................Passed
block files larger than 5 MB.............................................Passed
block obvious secrets (regex, not a real scanner)........................Passed
ruff lint................................................................Passed
[main 6772647] add eda
 3 files changed, 20 insertions(+)
 create mode 100644 config.py
 create mode 100644 eda.ipynb
 create mode 100644 train.py

--- bypass is possible: git commit --no-verify. So CI runs the same hooks: ---
$ pre-commit run --all-files   # same config, run in CI
strip notebook outputs...................................................Passed
block files larger than 5 MB.............................................Passed
block obvious secrets (regex, not a real scanner)........................Passed
ruff lint................................................................Passed
6772647 add eda
3f5b50f add hooks
add eda

 config.py |  2 ++
 eda.ipynb | 17 +++++++++++++++++
 train.py  |  1 +
outputs in the committed notebook: []
```

**Follow-ups:**
- *Hook too slow?* Run only fast checks locally (format, lint, size, secrets) and move tests to CI.
- *What about a key already committed?* Rotate it first. Removing it from history (git filter-repo) comes second, because clones and forks may still have it.
- *Big files that are really needed?* Version them with DVC or Git LFS (Part 4 covers DVC), not plain Git.

**Common mistakes:**
- Relying on local hooks only, with no CI check.
- Believing a regex hook catches all secrets.
- Committing notebooks with outputs, so a customer table sits in Git history.
- Not telling new team members to run `pre-commit install`.

### Q27 ⭐⭐ 🟡 Versioning and tagging a model package. Explain semantic versioning for a library that wraps a model (what is a major, minor and patch change when the feature set or the output scale changes), how you tag a release in Git, how the model artifact version is linked to the code tag and the data version, and how you roll back. Show git tag -a, a version string read at runtime from package metadata (importlib.metadata) and a changelog entry, run in a temp repo.
**Asked at:** Python packaging references (PEP 660, Xebia setuptools and pyproject guide, editables docs; snippets only) plus Bangalore job postings that list Git, CI/CD, Docker and Python (Cognizant, CommBank, JPMorgan Chase; snippets); postings show required skills, not interview questions; MLOps and ML platform roles
**Say this first (1 line):** I use semantic versioning MAJOR.MINOR.PATCH for the package, tag each release with `git tag -a vX.Y.Z`, read the version at runtime from package metadata, and store the code tag and data version next to the model artifact so I can roll back by installing the previous tag.

**Then explain:**
- PATCH: bug fix, same contract (clamp negative income). MINOR: new feature that old callers can ignore (an optional `tenure_years` argument). MAJOR: anything that can break a caller, and a change of output scale is exactly that (0-1 to 0-100 breaks every threshold downstream).
- A retrained model with the same features and scale is usually a patch or minor, but I also record a separate model version in the registry. Code version and model version are different things, and both must be traceable.
- Link them: the model card or registry entry stores code tag, data version (a DVC revision, snapshot id or hash) and metrics. From any prediction I can get to code, data and model.
- Single source of truth: the version lives in `pyproject.toml`, and the code reads it with `importlib.metadata.version`, so no second copy can drift.
- Rollback: the previous tag is still installable. Check it out or reinstall that version, and the model card shows the old version and old output scale. The old model artifact stays in the registry, so I do not retrain in an emergency.

**Example:** Releases: 1.0.0 (first), 1.1.0 (optional argument, backward compatible), 1.1.1 (clamp negatives), 2.0.0 (output 0-100, BREAKING). Hand-check the scale: `score(40)` gives 0.4 on 1.1.1 and 40 on 2.0.0, and the output below shows exactly that after the rollback.

**Code:** run in a temp repo with fixed commit dates; installed into a venv with the hatchling build backend (installed locally, no network needed).
```bash
set -e
export GIT_AUTHOR_DATE="2026-01-01T00:00:00+0000" GIT_COMMITTER_DATE="2026-01-01T00:00:00+0000"
D=$(mktemp -d); cd "$D"
git init -q -b main; git config user.email a@b.c; git config user.name demo
mkdir -p src/credit_model
pyproject() { cat > pyproject.toml <<T
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "credit-model"
version = "$1"
dependencies = []

[tool.hatch.build.targets.wheel]
packages = ["src/credit_model"]
T
}
code() { cat > src/credit_model/__init__.py <<P
from importlib.metadata import version

__version__ = version("credit-model")   # single source of truth: the installed package metadata

def score(income$1):
    """Risk score in $2."""
    return $3

def model_card():
    return {"code_version": __version__, "data_version": "loans-2026-01", "output_scale": "$4"}
P
}
release() { git add -A; git commit -qm "release $1"; git tag -a "v$1" -m "credit-model $1 $2"; }

pyproject 1.0.0; code "" "[0, 1]" "min(income / 100.0, 1.0)" "0-1"
printf '# Changelog\n\n## 1.0.0\n- First release. score() returns a value in [0, 1].\n' > CHANGELOG.md
release 1.0.0 "(data loans-2026-01)"

pyproject 1.1.0; code ", tenure_years=0" "[0, 1]" "min(income / 100.0, 1.0)" "0-1"          # new optional arg: MINOR
printf '# Changelog\n\n## 1.1.0\n- Added optional tenure_years argument (backward compatible).\n%s\n' "$(tail -n +3 CHANGELOG.md)" > C.tmp; mv C.tmp CHANGELOG.md
release 1.1.0 ""

pyproject 1.1.1; code ", tenure_years=0" "[0, 1]" "max(min(income / 100.0, 1.0), 0.0)" "0-1"   # clamp negatives: PATCH
printf '# Changelog\n\n## 1.1.1\n- Fix: negative income no longer gives a negative score.\n%s\n' "$(tail -n +3 CHANGELOG.md)" > C.tmp; mv C.tmp CHANGELOG.md
release 1.1.1 ""

pyproject 2.0.0; code ", tenure_years=0" "[0, 100]" "max(min(income, 100.0), 0.0)" "0-100"        # scale change: MAJOR
printf '# Changelog\n\n## 2.0.0 (BREAKING)\n- score() now returns 0-100 instead of 0-1. Update your thresholds.\n%s\n' "$(tail -n +3 CHANGELOG.md)" > C.tmp; mv C.tmp CHANGELOG.md
release 2.0.0 "(output scale 0-100)"

echo '$ git tag -n1'; git tag -n1
echo; echo '$ head -9 CHANGELOG.md'; head -9 CHANGELOG.md

python3 -m venv --system-site-packages "$D/.venv" >/dev/null
PIP="$D/.venv/bin/pip install -q --no-build-isolation --no-deps --disable-pip-version-check"
echo; echo "--- install the latest tag, read version at runtime ---"
git checkout -q v2.0.0; $PIP .
"$D/.venv/bin/python" -I -c "import credit_model as m; print(m.__version__, m.score(40), m.model_card())"
echo "--- rollback: check out the previous good tag and reinstall ---"
git checkout -q v1.1.1; $PIP --force-reinstall .
"$D/.venv/bin/python" -I -c "import credit_model as m; print(m.__version__, m.score(40), m.model_card())"
echo; echo '$ git describe --tags   # one commit after v2.0.0'
git checkout -q main; echo "" >> CHANGELOG.md; git commit -qam "docs"; git describe --tags | sed -E 's/g[0-9a-f]+$/g<sha>/'
```

**Output (my run):** git 2.43.0, Python 3.13, hatchling 1.32.4. `git describe` hash replaced with `<sha>`.
```text
$ git tag -n1
v1.0.0          credit-model 1.0.0 (data loans-2026-01)
v1.1.0          credit-model 1.1.0
v1.1.1          credit-model 1.1.1
v2.0.0          credit-model 2.0.0 (output scale 0-100)

$ head -9 CHANGELOG.md
# Changelog

## 2.0.0 (BREAKING)
- score() now returns 0-100 instead of 0-1. Update your thresholds.
## 1.1.1
- Fix: negative income no longer gives a negative score.
## 1.1.0
- Added optional tenure_years argument (backward compatible).
## 1.0.0

--- install the latest tag, read version at runtime ---
2.0.0 40 {'code_version': '2.0.0', 'data_version': 'loans-2026-01', 'output_scale': '0-100'}
--- rollback: check out the previous good tag and reinstall ---
1.1.1 0.4 {'code_version': '1.1.1', 'data_version': 'loans-2026-01', 'output_scale': '0-1'}

$ git describe --tags   # one commit after v2.0.0
v2.0.0-1-g<sha>
```

**Follow-ups:**
- *Annotated or lightweight tags?* Annotated (`-a`): they carry author, date and message, and show in `git describe`. I use them for releases.
- *Do I need to bump for a retrain?* My rule: new model artifact always gets a registry version. The package version moves only if the code or contract changed.
- *Calendar versioning?* Some teams use dates for data-heavy projects. Pick one scheme, write it down, and automate the bump.

**Common mistakes:**
- Version number hard-coded in two places (`pyproject.toml` and `__init__.py`).
- Changing the output scale in a patch release.
- Shipping a model file with no record of the code and data that made it.
- Moving or re-using a tag after release instead of making a new one.

### Q28 ⭐⭐ 🟡 Configuration management for ML code. A training script has learning rate, paths and feature lists hard-coded. Move them to a YAML file validated by a pydantic model, with environment overrides and a CLI flag, and fail fast on unknown keys or wrong types. Show the code with a good and a bad config run, say how you log the resolved config with each run, and when a config framework such as Hydra is worth it (hedge, concept only).
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** I move every knob into one YAML file, load it into a pydantic model that forbids unknown keys and checks types and ranges, apply overrides in a fixed order (file, then environment, then CLI), and log the resolved config with the run.

**Then explain:**
- Precedence is easy to explain: defaults, then YAML, then `TRAIN_*` environment variables, then CLI flags. The last one wins. The run output below shows each layer winning.
- Fail fast: `extra="forbid"` turns a typo like `epoch` into an error instead of a silent default, and `Field(gt=0, le=1)` stops `learning_rate: fast` or `epochs: 0` before any compute starts.
- All problems are reported together (pydantic collects them), so one run shows both mistakes.
- Log the resolved config (after all overrides) as JSON plus a short hash with each run, in MLflow params or a file next to the model. The YAML file alone is not enough, because the env and CLI values may differ.
- Secrets do not go in YAML. Read them from the environment or a secret manager.
- Hydra (hedge, not run here) is worth it when I need config composition, sweeps over many parameters, or many experiment variants. For one script with ten keys, YAML plus pydantic is enough.

**Example:** `config.yaml` says `epochs: 5`. With `TRAIN_EPOCHS=20` it becomes 20. With `TRAIN_EPOCHS=20 --epochs 3` it becomes 3. The bad file has `learning_rate: fast` and the typo `epoch: 5`; both are reported and the exit code is 2.

**Code:** `python3 -I train.py --config config.yaml`
```yaml
# ===== file: config.yaml =====
learning_rate: 0.01
epochs: 5
data_path: data/train.csv
features: [age, income, tenure]
seed: 42

# ===== file: bad_config.yaml =====
learning_rate: fast        # wrong type
epoch: 5                   # typo: unknown key (and 'epochs' is missing -> default used, which is the danger)
data_path: data/train.csv
features: [age, income]
```
```python
"""Config: defaults < YAML file < env vars (TRAIN_*) < CLI flags. Unknown keys and wrong types fail fast."""
import argparse, hashlib, json, os, sys
import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")            # a typo like 'epoch' is an error, not silently ignored
    learning_rate: float = Field(0.1, gt=0, le=1)
    epochs: int = Field(10, ge=1)
    data_path: str = "data/train.csv"
    features: list[str] = Field(min_length=1)
    seed: int = 0

def load(path, cli_overrides):
    raw = yaml.safe_load(open(path)) or {}
    for key in Config.model_fields:                      # env: TRAIN_LEARNING_RATE=0.05 etc.
        env = os.environ.get("TRAIN_" + key.upper())
        if env is not None:
            raw[key] = yaml.safe_load(env)               # parse "0.05" -> float, "[a,b]" -> list
    raw.update({k: v for k, v in cli_overrides.items() if v is not None})
    return Config(**raw)                                 # validation happens here

def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--learning-rate", type=float)
    p.add_argument("--epochs", type=int)
    a = p.parse_args(argv)
    try:
        cfg = load(a.config, {"learning_rate": a.learning_rate, "epochs": a.epochs})
    except ValidationError as e:
        print(f"CONFIG ERROR ({e.error_count()} problem(s)):")
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc']))}: {err['msg']} (got {err.get('input')!r})")
        return 2
    resolved = cfg.model_dump()
    blob = json.dumps(resolved, sort_keys=True)
    print("resolved config:", blob)
    print("config hash:", hashlib.sha256(blob.encode()).hexdigest()[:12], "(log this with the run, e.g. as an MLflow param or a JSON file)")
    # ... training would start here, using only cfg.*
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

**Output (my run):** pydantic 2.13.5, pyyaml 6.0.1.
```text
$ python3 -I train.py --config config.yaml
resolved config: {"data_path": "data/train.csv", "epochs": 5, "features": ["age", "income", "tenure"], "learning_rate": 0.01, "seed": 42}
config hash: ac04e83152fd (log this with the run, e.g. as an MLflow param or a JSON file)
exit=0

$ TRAIN_EPOCHS=20 python3 -I train.py --config config.yaml   # env overrides file
resolved config: {"data_path": "data/train.csv", "epochs": 20, "features": ["age", "income", "tenure"], "learning_rate": 0.01, "seed": 42}
config hash: 92680eff27c1 (log this with the run, e.g. as an MLflow param or a JSON file)
exit=0

$ TRAIN_EPOCHS=20 python3 -I train.py --config config.yaml --epochs 3 --learning-rate 0.5   # CLI wins
resolved config: {"data_path": "data/train.csv", "epochs": 3, "features": ["age", "income", "tenure"], "learning_rate": 0.5, "seed": 42}
config hash: 37d87f7fbb73 (log this with the run, e.g. as an MLflow param or a JSON file)
exit=0

$ python3 -I train.py --config bad_config.yaml
CONFIG ERROR (2 problem(s)):
  - learning_rate: Input should be a valid number, unable to parse string as a number (got 'fast')
  - epoch: Extra inputs are not permitted (got 5)
exit=2

$ TRAIN_EPOCHS=0 python3 -I train.py --config config.yaml
CONFIG ERROR (1 problem(s)):
  - epochs: Input should be greater than or equal to 1 (got 0)
exit=2
pydantic 2.13.5 pyyaml 6.0.1
```

**Follow-ups:**
- *Why not argparse only?* Twenty flags are hard to review and repeat. A file can be committed, diffed and reused.
- *Different environments (dev, prod)?* One base file plus a small override file per environment, or env vars for the few values that change (paths, endpoints).
- *Typed config at runtime?* Pass the `Config` object around, not a dict, so a misspelled attribute fails in the IDE and in mypy.

**Common mistakes:**
- Silently ignoring unknown keys.
- Parsing env vars as strings, so `"False"` is truthy.
- Logging only the YAML, not the final values.
- Putting passwords or API keys in the committed config.

### Q29 ⭐⭐ 🟡 Logging and error handling in ML pipelines. Replace print debugging in a batch scoring function with the logging module: levels, a structured JSON log line with run id and row counts, raising specific exceptions on bad input versus logging and continuing, and never swallowing exceptions in a bare except. Show the code, its output on a good and a bad batch, and what you would alert on.
**Asked at:** Editorial MLOps interview guides (DataCamp MLOps interview questions, Devinterview-io mlops-interview-questions on GitHub, wecreateproblems, a DEV Community list; search snippets only, not opened); guides, not verified candidate reports; MLOps and ML engineer rounds at product companies, GCCs and IT-services firms
**Say this first (1 line):** I replace `print` with the `logging` module, log JSON lines that carry a run id and row counts, raise a specific exception when the whole batch is unusable, log a warning and continue when only a few rows are bad, and never use a bare `except`.

**Then explain:**
- Levels: DEBUG for detail, INFO for normal milestones (batch received, batch scored), WARNING for something odd but handled (dropped rows), ERROR for a failed batch. Production runs at INFO.
- Structured logs (one JSON object per line) can be searched and counted: filter by `run_id`, plot `rows_bad`. Free text cannot.
- Decision rule: a bad row is a data problem, so warn, drop, count it, and continue until a limit (my rule is 20 percent). A missing column or an empty batch is a pipeline problem, so raise `BadInputError`, which the caller catches by type.
- Never `except: pass` or `except Exception: pass`. It hides real bugs and the job "succeeds" with no output. Catch the specific error, log with `exc_info`, then re-raise or return a non-zero exit code so the scheduler marks the run failed.
- Do not log secrets or raw personal data. Log ids and counts. In real code the run id is generated per run (for example `uuid.uuid4().hex[:8]`); I fixed it here so the output is repeatable.

**Example:** Four batches. Good (5 rows): two INFO lines. Ragged (10 rows, 1 bad, 10 percent): a WARNING with `bad_ids: [2]`, then scored 9 rows. Bad (5 rows, 3 bad, 60 percent): a WARNING, then an ERROR and `BadInputError`. No `income` column: ERROR immediately. Process exit code is 1 because at least one batch was rejected.

**Code:** `python3 -I score_batch.py`
```python
import json, logging, sys
import pandas as pd

class JsonFormatter(logging.Formatter):
    def format(self, record):
        d = {"level": record.levelname, "logger": record.name, "msg": record.getMessage(), "run_id": RUN_ID}
        d.update(getattr(record, "ctx", {}))              # structured extras: row counts etc.
        if record.exc_info:
            d["exc"] = repr(record.exc_info[1])
        return json.dumps(d, sort_keys=True)

RUN_ID = "run-0001"     # fixed here so the output is reproducible; use uuid.uuid4().hex[:8] in real code
log = logging.getLogger("scoring")
h = logging.StreamHandler(sys.stdout); h.setFormatter(JsonFormatter())
log.addHandler(h); log.setLevel(logging.INFO); log.propagate = False

class BadInputError(ValueError):
    """The batch itself is unusable (missing column, empty). Stop the job."""

def score_batch(df: pd.DataFrame, max_bad_frac: float = 0.2) -> pd.DataFrame:
    log.info("batch received", extra={"ctx": {"rows_in": len(df)}})
    if "income" not in df.columns:
        raise BadInputError("missing column: income")        # specific exception, caller can alert on it
    if df.empty:
        raise BadInputError("empty batch")
    ok = df["income"].notna() & (df["income"] >= 0)
    n_bad = int((~ok).sum())
    if n_bad:
        log.warning("dropping bad rows", extra={"ctx": {"rows_bad": n_bad, "bad_ids": df.loc[~ok, "id"].tolist()}})
    if n_bad / len(df) > max_bad_frac:                        # a few bad rows: continue. Too many: stop.
        raise BadInputError(f"{n_bad}/{len(df)} bad rows exceeds limit {max_bad_frac:.0%}")
    out = df[ok].assign(score=lambda d: (d["income"] / 100).clip(upper=1.0))
    log.info("batch scored", extra={"ctx": {"rows_in": len(df), "rows_out": len(out), "rows_bad": n_bad}})
    return out

def main():
    batches = {
      "good":   pd.DataFrame({"id": range(1, 6), "income": [10., 50., 80., 120., 30.]}),
      "ragged": pd.DataFrame({"id": range(1, 11), "income": [10., None, 80., 120., 30., 5., 6., 7., 8., 9.]}),   # 1 bad of 10
      "bad":    pd.DataFrame({"id": range(1, 6), "income": [None, -5., None, 120., 30.]}),                        # 3 bad of 5
      "nocol":  pd.DataFrame({"id": [1, 2], "salary": [1., 2.]}),
    }
    code = 0
    for name, df in batches.items():
        print(f"--- batch: {name}")
        try:
            score_batch(df)
        except BadInputError as e:
            log.error("batch rejected", extra={"ctx": {"reason": str(e)}}, exc_info=True)
            code = 1                       # non-zero exit lets the scheduler mark the job failed
        # NOT: except Exception: pass   (hides real bugs, the job 'succeeds' with no output)
    return code

if __name__ == "__main__":
    sys.exit(main())
```

**Output (my run):** pandas 3.0.5.
```text
--- batch: good
{"level": "INFO", "logger": "scoring", "msg": "batch received", "rows_in": 5, "run_id": "run-0001"}
{"level": "INFO", "logger": "scoring", "msg": "batch scored", "rows_bad": 0, "rows_in": 5, "rows_out": 5, "run_id": "run-0001"}
--- batch: ragged
{"level": "INFO", "logger": "scoring", "msg": "batch received", "rows_in": 10, "run_id": "run-0001"}
{"bad_ids": [2], "level": "WARNING", "logger": "scoring", "msg": "dropping bad rows", "rows_bad": 1, "run_id": "run-0001"}
{"level": "INFO", "logger": "scoring", "msg": "batch scored", "rows_bad": 1, "rows_in": 10, "rows_out": 9, "run_id": "run-0001"}
--- batch: bad
{"level": "INFO", "logger": "scoring", "msg": "batch received", "rows_in": 5, "run_id": "run-0001"}
{"bad_ids": [1, 2, 3], "level": "WARNING", "logger": "scoring", "msg": "dropping bad rows", "rows_bad": 3, "run_id": "run-0001"}
{"exc": "BadInputError('3/5 bad rows exceeds limit 20%')", "level": "ERROR", "logger": "scoring", "msg": "batch rejected", "reason": "3/5 bad rows exceeds limit 20%", "run_id": "run-0001"}
--- batch: nocol
{"level": "INFO", "logger": "scoring", "msg": "batch received", "rows_in": 2, "run_id": "run-0001"}
{"exc": "BadInputError('missing column: income')", "level": "ERROR", "logger": "scoring", "msg": "batch rejected", "reason": "missing column: income", "run_id": "run-0001"}
exit=1
pandas 3.0.5
```

**Follow-ups:**
- *What do you alert on?* Job failed (exit code or ERROR count above 0), rows_bad fraction above the normal level, rows_out much lower than rows_in, and no `batch scored` line at all in the expected time window (silence is a failure too).
- *print vs logging in containers?* Log to stdout in JSON; the platform collects it. Logging handlers and formats stay in one place.
- *How do you trace one request?* The run id (batch) or request id (online) is on every line.

**Common mistakes:**
- `except Exception: pass` or `except: print("error")`.
- Logging inside a tight loop for each row, which floods the log and slows the job.
- Using ERROR for expected conditions, so the alert is always on and everyone ignores it.
- Logging free text with no ids, so you cannot link a message to a run.

### Q30 ⭐⭐ 🟡 Type hints and mypy for data and ML code. Explain what type hints buy you in a pandas and NumPy codebase (documentation, catching wrong arguments, IDE help) and what they cannot check (DataFrame columns, array shapes). Annotate a small feature function with typing and numpy.typing, run mypy on a version with a planted type error, and mention gradual adoption (strict only for new modules) and runtime checking with pydantic at the boundaries.
**Asked at:** Python packaging references (PEP 660, Xebia setuptools and pyproject guide, editables docs; snippets only) plus Bangalore job postings that list Git, CI/CD, Docker and Python (Cognizant, CommBank, JPMorgan Chase; snippets); postings show required skills, not interview questions; MLOps and ML platform roles
**Say this first (1 line):** Type hints document what a function takes and returns and let mypy catch wrong calls before runtime, but they cannot check DataFrame column names or array shapes, so I add runtime validation (pydantic or schema checks) at the boundaries.

**Then explain:**
- What they buy: a self-checking signature, IDE autocomplete and rename help, and mypy errors for calls like passing a list where an array is needed or a string where a float is needed.
- What they cannot check: which columns a `DataFrame` has, the shape or length of an array, value ranges, or NaN. `NDArray[np.float64]` checks dtype only. My run shows both `add_features(df_without_income)` and a 2-D array going through type checking and failing or misbehaving at runtime.
- Practical setup: install `pandas-stubs` (without it mypy complains about missing stubs for pandas, which my first run showed), and use `numpy.typing.NDArray`.
- Gradual adoption: start with loose settings on the old code (no failures from missing annotations), and use `--strict` or per-module strict overrides only for new modules. Fix errors as files are touched. Do not try to annotate everything in one week.
- Boundaries: validate config, API payloads and incoming data with pydantic or the validation function, then pass trusted typed objects inside the code.

**Example:** `features_bad.py` has four planted errors. mypy reports all four with exit code 1: `floor="1"` to `add_features`, a Python list to `log_income`, `floor="1"` to `log_income`, and assigning an array to an `int` variable. The good file passes, also under `--strict`.

**Code:** the typed module, the module with planted errors, and a script for what the type checker cannot see.
```python
# ===== file: features.py =====
import numpy as np
import numpy.typing as npt
import pandas as pd

FloatArray = npt.NDArray[np.float64]

def log_income(income: FloatArray, floor: float = 1.0) -> FloatArray:
    """log of income with a floor, so zeros do not give -inf."""
    return np.log(np.maximum(income, floor))

def add_features(df: pd.DataFrame, floor: float = 1.0) -> pd.DataFrame:
    out = df.copy()
    out["log_income"] = log_income(out["income"].to_numpy(dtype=np.float64), floor)
    return out

def mean_log_income(df: pd.DataFrame) -> float:
    return float(add_features(df)["log_income"].mean())

# ===== file: features_bad.py =====
import numpy as np
import numpy.typing as npt
import pandas as pd
from features import add_features

FloatArray = npt.NDArray[np.float64]

def log_income(income: FloatArray, floor: float = 1.0) -> FloatArray:
    return np.log(np.maximum(income, floor))

def run(df: pd.DataFrame) -> None:
    add_features(df, floor="1")             # ERROR: str where float expected
    log_income([1.0, 2.0])                  # ERROR: list is not an ndarray
    log_income(np.array([1.0]), floor="1")  # ERROR: str where float expected
    x: int = log_income(np.array([1.0]))    # ERROR: array assigned to int

# ===== file: runtime_traps.py =====
# things the type checker cannot see: both lines type-check, both fail or mislead at runtime
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I removes the script dir from sys.path
import numpy as np
import pandas as pd
from features import add_features, log_income

df = pd.DataFrame({"salary": [10.0, 20.0]})        # wrong column name: mypy is happy
try:
    add_features(df)
except KeyError as e:
    print("KeyError at runtime (mypy cannot see DataFrame columns):", e)
a = np.ones((3, 2))                               # wrong shape / dtype is also invisible to NDArray[float64]
print("2-D array accepted by a function meant for 1-D income:", log_income(a).shape)
```
```bash
python3 -I -m mypy features.py
python3 -I -m mypy features_bad.py
python3 -I -m mypy --strict features.py
python3 -I runtime_traps.py
```

**Output (my run):** mypy 2.4.0, numpy 2.5.3, pandas 3.0.5, pandas-stubs 3.0.5.260914. Error message wording and stub coverage change between versions (check current docs).
```text
$ mypy features.py
Success: no issues found in 1 source file
exit=0

$ mypy features_bad.py
features_bad.py:12: error: Argument "floor" to "add_features" has incompatible type "str"; expected "float"  [arg-type]
features_bad.py:13: error: Argument 1 to "log_income" has incompatible type "list[float]"; expected "ndarray[tuple[Any, ...], dtype[float64]]"  [arg-type]
features_bad.py:14: error: Argument "floor" to "log_income" has incompatible type "str"; expected "float"  [arg-type]
features_bad.py:15: error: Incompatible types in assignment (expression has type "ndarray[tuple[Any, ...], dtype[float64]]", variable has type "int")  [assignment]
Found 4 errors in 1 file (checked 1 source file)
exit=1

$ mypy --strict features.py   # what "strict for new modules" means
Success: no issues found in 1 source file
exit=0

$ python3 -I runtime_traps.py
KeyError at runtime (mypy cannot see DataFrame columns): 'income'
2-D array accepted by a function meant for 1-D income: (3, 2)
mypy 2.4.0 numpy 2.5.3 pandas 3.0.5
pandas-stubs              3.0.5.260914
```

**Follow-ups:**
- *Do hints slow code down?* No. Python ignores them at runtime. mypy is a separate step in CI or in pre-commit.
- *How do you type DataFrame columns?* mypy cannot. Options are a pandera schema or a pydantic or dataclass row type at the boundary. Treat them as runtime checks.
- *What about `Any`?* It switches checking off. Use it sparingly and mark it with a comment. A pile of `Any` gives false comfort.

**Common mistakes:**
- Adding hints and not running mypy in CI, so they rot.
- Believing `NDArray[np.float64]` checks shape.
- Forgetting pandas-stubs and ignoring all pandas errors with `ignore_missing_imports`.
- Turning on strict for the whole old codebase at once, then switching mypy off in frustration.

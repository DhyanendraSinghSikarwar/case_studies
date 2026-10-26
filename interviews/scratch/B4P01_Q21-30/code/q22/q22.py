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

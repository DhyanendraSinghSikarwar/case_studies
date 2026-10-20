# Project 01 — Credit Risk Scorecard & Credit-Limit Engine

| | |
|---|---|
| Domain | FinTech lending (credit cards) |
| Difficulty / effort | ★★ · about 25–30 hours over 1 week |
| Repo name | `ampba-01-credit-scorecard` |
| Python package (`PKG`) | `credit` |
| Data | UCI "Default of Credit Card Clients" (30,000 rows). Details and fallbacks in [DATA.md](DATA.md) |
| Shared setup | [../00-COMMON-SETUP.md](../00-COMMON-SETUP.md) |

---

## 1. What you are building

A card issuer wants to (a) predict whether a customer defaults next month (PD), (b) turn PD into a 300–900 bureau-style score with risk bands A–F, and (c) pick an approve/decline cut-off and limit actions that maximise expected profit. You will build a WOE/logistic **scorecard** (the regulator-friendly model), an **XGBoost/LightGBM challenger**, an **economics layer** (expected loss, optimal cut-off, sensitivity), a **fairness audit**, **reason codes**, a **drift monitor** and a 4-tab Streamlit app.

**Targets (from the master plan):** ROC-AUC ≥ 0.78 · KS ≥ 0.42 · Gini ≥ 0.56 · Brier ≤ 0.14 · calibration slope 0.9–1.1. Primary business KPI: expected portfolio profit (₹) at the chosen cut-off versus approve-everyone.

Realistic expectations before you start: a plain logistic regression on this file typically lands around AUC 0.72–0.73; boosted trees with engineered repayment features are typically around 0.78. Reference repo R1 reports AUC 0.783 / KS 0.424. If your champion is at 0.77, say so honestly in the README rather than tuning on the test set.

## 2. Read first (design inspiration only — do not copy code)

| Repo | Look at |
|---|---|
| [Abhinav19-isb/credit-risk-scorecard](https://github.com/Abhinav19-isb/credit-risk-scorecard) | README results table, how it presents scorecard + SHAP + Streamlit + CI. Note its benchmark (AUC 0.783, KS 0.424) and that it drops 35 duplicate rows — you will decide and document your own choice |
| [RishabhBansal2409/Predicting_Credit_Card_Approvals](https://github.com/RishabhBansal2409/Predicting_Credit_Card_Approvals) | A simple baseline logistic regression, to see what "naive" looks like |

## 3. Step 0 — project setup

```powershell
cd "C:\Users\11624\OneDrive - Indian School of Business\Documents\personal\isb_ampba\projects\01-credit-risk-scorecard"
py -3.11 -m venv C:\venvs\ampba-01
C:\venvs\ampba-01\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel
pip install -r requirements.in          # provided in this folder; optbinning pulls in ortools/cvxpy (large, takes a few minutes)
$pkg = "credit"
mkdir config, data\raw, data\interim, data\processed, notebooks, "src\$pkg", analysis, outputs, figures, models, app, tests\fixtures, docs, .github\workflows
New-Item "src\$pkg\__init__.py", tests\__init__.py -ItemType File
git init
```
Then create `.gitignore`, `pyproject.toml`, `config/config.yaml`, `src/credit/config.py`, `tasks.py`, CI file and `Dockerfile` exactly as in the common setup (§3–§8), set `PKG = "credit"` in `tasks.py`, run `pip install -e .`, and make the first commit.

Put this in `config/config.yaml` (it holds every assumption; the business assumptions are swept later):

```yaml
seed: 42
paths: {raw: data/raw, interim: data/interim, processed: data/processed, outputs: outputs, figures: figures, models: models}

data:
  uci_id: 350
  zip_url: https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip
  raw_cache: data/raw/uci350.parquet
  split: {train: 0.6, valid: 0.2, test: 0.2}
  exclude_features: [SEX]          # stays in the frame for the fairness audit, never fed to a model

scorecard:
  base_score: 600
  base_odds: 50                    # good:bad odds at base_score
  pdo: 20                          # points to double the odds
  clip: [300, 900]
  iv_min: 0.02
  corr_max: 0.70
  band_pd_edges: [0.08, 0.12, 0.20, 0.35, 0.60]   # A <8%, B 8-12%, C 12-20%, D 20-35%, E 35-60%, F >=60%

models:
  optuna_trials: 30
  cv_folds: 3

economics:
  fx_ntd_inr: 2.6
  margin: 0.18                     # annual net margin on exposure for a performing account
  lgd: 0.65
  cutoff_grid: {start: 0.05, stop: 0.60, step: 0.01}
  sensitivity:
    lgd: [0.45, 0.55, 0.65, 0.75, 0.85]
    margin: [0.10, 0.14, 0.18, 0.22, 0.26]

limits:                            # band -> action; pd_mult = assumed PD change after the action
  A: {action: increase, limit_change: 0.20, pd_mult: 1.10}
  B: {action: increase, limit_change: 0.10, pd_mult: 1.05}
  C: {action: hold,     limit_change: 0.00, pd_mult: 1.00}
  D: {action: decrease, limit_change: -0.20, pd_mult: 0.95}
  E: {action: decline,  limit_change: -1.00, pd_mult: 1.00}
  F: {action: decline,  limit_change: -1.00, pd_mult: 1.00}

monitoring:
  psi_alert: 0.2
  drift_limit_shift: -0.20
```

Write `docs/PROBLEM_STATEMENT.md` now (objective, KPIs above, constraints: SEX never a model input; success criteria = the acceptance checklist in §8).

---

## 4. Data (summary — see DATA.md)

30,000 customers of a Taiwanese card issuer, 23 features (limit, demographics, 6 months of repayment status, bill amounts, payment amounts), target = default next month (22.12%). Month alignment: `BILL_AMT1`/`PAY_AMT1`/`PAY_0` are **September** (latest). Amounts are NT$; convert to ₹ only in business outputs.

---

## 5. Milestones

### M1 — Data, validation, EDA (about 5 h)

**Goal:** a cached, validated, split dataset and an EDA notebook with six figures.

1. **`src/credit/data.py`** — loader with cache and fallback, cleaning, split.

```python
"""Load, clean and split the UCI 'Default of Credit Card Clients' data (id 350)."""
from __future__ import annotations
import io, zipfile
import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from .config import ROOT, get_logger, load_config

log = get_logger(__name__)
TARGET = "default"
PAY_COLS = ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]     # PAY_0 = most recent month (Sep)
BILL_COLS = [f"BILL_AMT{i}" for i in range(1, 7)]
PAYAMT_COLS = [f"PAY_AMT{i}" for i in range(1, 7)]
RAW_FEATURES = ["LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE"] + PAY_COLS + BILL_COLS + PAYAMT_COLS
RAW_COLUMNS = RAW_FEATURES + [TARGET]


def _from_zip(url: str) -> pd.DataFrame:
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=120)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        name = [n for n in z.namelist() if n.lower().endswith((".xls", ".xlsx"))][0]
        df = pd.read_excel(z.open(name), header=1)        # row 0 holds X1..X23,Y; row 1 holds the names
    return df.drop(columns=["ID"]).rename(columns={"default payment next month": TARGET})


def _from_ucimlrepo(uci_id: int) -> pd.DataFrame:
    from ucimlrepo import fetch_ucirepo
    d = fetch_ucirepo(id=uci_id)
    X, y = d.data.features.copy(), d.data.targets.copy()
    if list(X.columns) == [f"X{i}" for i in range(1, 24)]:
        X.columns = ["LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE"] + PAY_COLS + BILL_COLS + PAYAMT_COLS
    df = X.copy()
    df[TARGET] = y.iloc[:, 0].to_numpy()
    return df


def load_raw(cfg: dict | None = None, refresh: bool = False) -> pd.DataFrame:
    cfg = cfg or load_config()
    cache = ROOT / cfg["data"]["raw_cache"]
    if cache.exists() and not refresh:
        return pd.read_parquet(cache)
    try:
        df = _from_ucimlrepo(cfg["data"]["uci_id"])
    except Exception as e:                                 # the ucimlrepo API is sometimes flaky
        log.warning("ucimlrepo failed (%s); falling back to the zip download", e)
        df = _from_zip(cfg["data"]["zip_url"])
    cache.parent.mkdir(parents=True, exist_ok=True)
    df = df[RAW_COLUMNS].astype("int64")
    df.to_parquet(cache, index=False)
    log.info("cached %s rows to %s", len(df), cache)
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """EDUCATION {0,5,6} -> 4 (others); MARRIAGE 0 -> 3 (others). Keeps every row."""
    out = df.copy()
    out["EDUCATION"] = out["EDUCATION"].replace({0: 4, 5: 4, 6: 4})
    out["MARRIAGE"] = out["MARRIAGE"].replace({0: 3})
    return out


def split(df: pd.DataFrame, cfg: dict | None = None):
    """Stratified 60/20/20; the original index is preserved."""
    cfg = cfg or load_config()
    s, seed = cfg["data"]["split"], cfg["seed"]
    train, rest = train_test_split(df, train_size=s["train"], stratify=df[TARGET], random_state=seed)
    valid, test = train_test_split(rest, test_size=s["test"] / (s["valid"] + s["test"]),
                                   stratify=rest[TARGET], random_state=seed)
    return train, valid, test


def build_splits(cfg: dict | None = None, raw: pd.DataFrame | None = None, save: bool = True):
    cfg = cfg or load_config()
    df = clean(load_raw(cfg) if raw is None else raw)
    train, valid, test = split(df, cfg)
    if save:
        out = ROOT / cfg["paths"]["processed"]
        out.mkdir(parents=True, exist_ok=True)
        for name, part in zip(["train", "valid", "test"], [train, valid, test]):
            part.to_parquet(out / f"{name}.parquet")
    return train, valid, test


if __name__ == "__main__":
    tr, va, te = build_splits()
    log.info("train/valid/test = %s/%s/%s", len(tr), len(va), len(te))
```

2. **`src/credit/validate.py`** — fail loudly on bad data.

```python
from __future__ import annotations
import pandas as pd
from .data import BILL_COLS, PAY_COLS, PAYAMT_COLS, RAW_COLUMNS, TARGET


def validate_raw(df: pd.DataFrame, expected_rows: int | None = 30000) -> dict:
    missing = [c for c in RAW_COLUMNS if c not in df.columns]
    assert not missing, f"missing columns: {missing}"
    if expected_rows is not None:
        assert len(df) == expected_rows, f"expected {expected_rows} rows, got {len(df)}"
    assert df[RAW_COLUMNS].isna().sum().sum() == 0, "unexpected nulls"
    assert set(df[TARGET].unique()) <= {0, 1}, "target must be in {0,1}"
    assert df["LIMIT_BAL"].gt(0).all(), "LIMIT_BAL must be positive"
    assert df["AGE"].between(18, 100).all(), "AGE out of range"
    assert df["SEX"].isin([1, 2]).all(), "SEX must be 1 or 2"
    assert df[PAY_COLS].apply(lambda s: s.between(-2, 9)).all().all(), "PAY_* out of [-2, 9]"
    assert df[PAYAMT_COLS].ge(0).all().all(), "PAY_AMT must be >= 0"
    # BILL_AMT can legitimately be negative (credit balance): report, do not fail
    return {"rows": int(len(df)), "default_rate": float(df[TARGET].mean()),
            "neg_bill_rows": int((df[BILL_COLS] < 0).any(axis=1).sum()),
            "duplicate_rows": int(df.duplicated().sum())}
```

3. Run it and compare with the check table in DATA.md §2:
```powershell
python -m src.credit.data
python -c "from credit.data import load_raw; from credit.validate import validate_raw; print(validate_raw(load_raw()))"
```
**Expected:** 30,000 rows, default rate 0.2212, 590 rows with a negative `BILL_AMT1`, 35 duplicates, splits 18,000 / 6,000 / 6,000.

4. **Decide on duplicates and write the decision into the README "Decisions" section** (this plan keeps them; 35 rows out of 30,000 is immaterial).
5. **`notebooks/01_eda.ipynb`** (thin: import from `credit.data`). Produce and save these six figures to `figures/`: default rate by `PAY_0`; default rate by `LIMIT_BAL` decile; default rate by `EDUCATION`; correlation heat-map; average-utilisation histogram by outcome; default rate by months delayed (needs the features below, so do this one after step 6 of M2 or compute `n_months_delayed` inline). You will regenerate all of them from `analysis/run_analysis.py` in M5 — write the plotting code there and call it from the notebook if you prefer.
6. **`src/credit/features.py`** — engineered features (written now, used from M2). Note the month alignment: the payment made in month *i* settles the bill of month *i+1*.

```python
from __future__ import annotations
import numpy as np
import pandas as pd
from .data import BILL_COLS, PAY_COLS, PAYAMT_COLS, TARGET

ENGINEERED = ([f"util_{i}" for i in range(1, 7)] + [f"pay_ratio_{i}" for i in range(1, 6)]
              + ["avg_util", "util_volatility", "max_delay", "n_months_delayed", "delay_trend",
                 "bill_growth", "avg_pay_ratio"])


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    lim = out["LIMIT_BAL"].astype(float)
    for i in range(1, 7):
        out[f"util_{i}"] = out[f"BILL_AMT{i}"] / lim
    for i in range(1, 6):                                  # payment in month i settles bill of month i+1
        owed = out[f"BILL_AMT{i + 1}"].astype(float)
        ratio = np.where(owed > 0, out[f"PAY_AMT{i}"] / owed.where(owed > 0, 1.0), 1.0)
        out[f"pay_ratio_{i}"] = np.clip(ratio, 0.0, 1.0)
    util = out[[f"util_{i}" for i in range(1, 7)]]
    out["avg_util"] = util.mean(axis=1)
    out["util_volatility"] = util.std(axis=1, ddof=0)
    delays = out[PAY_COLS].clip(lower=0)                   # -2 / -1 / 0 all mean "no delay"
    out["max_delay"] = delays.max(axis=1)
    out["n_months_delayed"] = (delays > 0).sum(axis=1)
    y = delays[PAY_COLS[::-1]].to_numpy(dtype=float)       # oldest -> newest
    xc = np.arange(y.shape[1], dtype=float) - (y.shape[1] - 1) / 2
    out["delay_trend"] = (xc * (y - y.mean(axis=1, keepdims=True))).sum(axis=1) / (xc ** 2).sum()  # OLS slope
    out["bill_growth"] = (out["BILL_AMT1"] - out["BILL_AMT6"]) / lim
    owed_all = out[BILL_COLS[1:]].clip(lower=0).sum(axis=1)
    paid_all = out[PAYAMT_COLS[:5]].sum(axis=1)
    out["avg_pay_ratio"] = np.clip(np.where(owed_all > 0, paid_all / owed_all.where(owed_all > 0, 1.0), 1.0), 0, 1)
    return out


def feature_cols(df: pd.DataFrame, cfg: dict) -> list[str]:
    """Every column except the target and the fairness-excluded ones (SEX)."""
    drop = set(cfg["data"]["exclude_features"]) | {TARGET}
    return [c for c in df.columns if c not in drop]
```

7. Save a 1,500-row stratified sample as `tests/fixtures/uci350_sample.csv` (`df.groupby("default", group_keys=False).sample(frac=0.05, random_state=42)` on the raw frame) — the tests in §7 use only this.
8. `docs/data_quality.md`: 10 lines on nulls, undocumented codes, negative bills, duplicates, month alignment.

**Pitfalls:** `header=1` for the `.xls`; `PAY_0` then `PAY_2` (no `PAY_1`); do not drop negative bills; do not fit anything on the full data before the split.

```powershell
git add -A; git commit -m "M1: data load+validate+split, features, EDA (30k rows, 22.1% default)"
```
README row: M1 ✔ (rows, default rate, split sizes).

---

### M2 — Baseline and WOE scorecard (about 6 h)

**Goal:** a baseline AUC, a monotonic-WOE logistic scorecard, a points table you can score with by hand.

1. **Baseline** (`models.py`): logistic regression on the 23 raw features, standardised. Record valid/test AUC in `metrics.json`. This is the number every other model must beat.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def fit_baseline_logit(X, y, seed=42):
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=seed)).fit(X, y)
```

2. **`woe.py`** — monotonic optimal binning with `optbinning`. Fit on **train only**; variables with IV below `iv_min` are marked not selected.

```python
from __future__ import annotations
import numpy as np
import pandas as pd
from optbinning import BinningProcess


def fit_binning(X_train, y_train, iv_min=0.02, seed=42) -> BinningProcess:
    cols = list(X_train.columns)
    bp = BinningProcess(
        variable_names=cols, max_n_prebins=20, min_prebin_size=0.05,
        selection_criteria={"iv": {"min": iv_min}},
        binning_fit_params={c: {"monotonic_trend": "auto_asc_desc"} for c in cols})
    return bp.fit(X_train, np.asarray(y_train))


def iv_table(bp) -> pd.DataFrame:
    s = bp.summary()[["name", "n_bins", "iv", "gini", "selected"]]
    return s.sort_values("iv", ascending=False).reset_index(drop=True)


def selected_variables(bp) -> list[str]:
    return [str(n) for n in bp.summary().query("selected")["name"]]


def woe_transform(bp, X) -> pd.DataFrame:
    arr = bp.transform(X, metric="woe")
    return pd.DataFrame(np.asarray(arr), columns=selected_variables(bp), index=X.index)


def woe_is_monotonic(bp, var: str) -> bool:
    t = bp.get_binned_variable(var).binning_table.build()
    t = t.loc[[i for i in t.index if str(i) not in ("Special", "Missing", "Totals")]]
    d = np.diff(t["WoE"].to_numpy(dtype=float))
    return bool(np.all(d >= -1e-12) or np.all(d <= 1e-12))
```

   Check the API once in a Python shell: `help(BinningProcess)`; docs: https://gnpalencia.org/optbinning/ . **Expected:** the six `PAY_*` columns, `max_delay`, `n_months_delayed`, `avg_pay_ratio` have the highest IV (PAY_0 alone is typically > 0.8). Columns like `AGE`, `MARRIAGE`, `EDUCATION` should be weak.

3. **`scorecard.py`** — scaling, WOE logistic with sign and correlation control, points table.

   The scaling (this is standard credit-scoring maths): `factor = pdo / ln 2`, `offset = base_score − factor × ln(base_odds)`, `score = offset + factor × ln((1 − PD) / PD)`. Higher score = safer. With base 600 at 50:1 odds and PDO 20, every +20 points halve the PD odds.

```python
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

BAND_LETTERS = list("ABCDEF")


def factor_offset(base_score=600, base_odds=50, pdo=20):
    factor = pdo / np.log(2)
    return float(factor), float(base_score - factor * np.log(base_odds))


def pd_to_score(p, base=600, odds=50, pdo=20, clip=(300, 900)):
    p = np.clip(np.asarray(p, dtype=float), 1e-6, 1 - 1e-6)
    factor, offset = factor_offset(base, odds, pdo)
    return np.clip(offset + factor * np.log((1 - p) / p), clip[0], clip[1])


def assign_band(p, edges):
    """A = lowest PD. 5 ascending edges -> 6 bands A..F."""
    return np.array(BAND_LETTERS)[np.searchsorted(np.asarray(edges), np.asarray(p), side="right")]


def fit_logit_scorecard(Xw, y, iv, corr_max=0.7, seed=42):
    """1) drop one of each pair with |corr| > corr_max (keep higher IV);
       2) refit, dropping any variable with a POSITIVE coefficient (WOE = ln(good/bad), so the sign must be negative)."""
    cols = list(Xw.columns)
    corr = Xw.corr().abs()
    for a in list(cols):
        for b in list(cols):
            if a < b and a in cols and b in cols and corr.loc[a, b] > corr_max:
                cols.remove(a if iv[a] < iv[b] else b)
    while True:
        lr = LogisticRegression(C=1.0, max_iter=1000, random_state=seed).fit(Xw[cols], y)
        bad = [(c, b) for c, b in zip(cols, lr.coef_[0]) if b > 0]
        if not bad:
            return lr, cols
        cols.remove(max(bad, key=lambda t: t[1])[0])


def build_points_table(bp, lr, cols, sc_cfg) -> pd.DataFrame:
    """points(var, bin) = -factor * coef * WOE + (offset - factor * intercept) / n_vars"""
    factor, offset = factor_offset(sc_cfg["base_score"], sc_cfg["base_odds"], sc_cfg["pdo"])
    b0, n = float(lr.intercept_[0]), len(cols)
    rows = []
    for c, coef in zip(cols, lr.coef_[0]):
        t = bp.get_binned_variable(c).binning_table.build()
        t = t.loc[[i for i in t.index if str(i) != "Totals"]]
        for idx, r in t.iterrows():
            woe = 0.0 if pd.isna(r["WoE"]) else float(r["WoE"])
            rows.append({"variable": c, "bin_index": idx, "bin": str(r["Bin"]), "woe": woe,
                         "points": round(-factor * float(coef) * woe + (offset - factor * b0) / n, 2)})
    return pd.DataFrame(rows)


def score_with_table(bp, X, table, cols):
    """Score rows by LOOKING UP points (what a business user does by hand)."""
    names = [str(n) for n in bp.summary().query("selected")["name"]]
    idx = pd.DataFrame(np.asarray(bp.transform(X, metric="indices")), index=X.index, columns=names)
    total = np.zeros(len(X))
    for c in cols:
        lut = table[table["variable"] == c].set_index("bin_index")["points"]
        total += idx[c].map(lut).to_numpy(dtype=float)
    return total
```

4. Train the scorecard and write `outputs/scorecard_points.csv` and `outputs/iv_table.csv` (this happens in `train.py`, M3 step 5; for now run it in the notebook `notebooks/02_features_scorecard.ipynb`):
```python
from credit.data import build_splits, TARGET
from credit.features import add_features, feature_cols
from credit import woe, scorecard as sc
from credit.config import load_config
cfg = load_config()
tr, va, te = [add_features(d) for d in build_splits()]
cols = feature_cols(tr, cfg)
bp = woe.fit_binning(tr[cols], tr[TARGET], cfg["scorecard"]["iv_min"])
iv = woe.iv_table(bp).set_index("name")["iv"]
lr, sc_cols = sc.fit_logit_scorecard(woe.woe_transform(bp, tr[cols]), tr[TARGET], iv)
```
5. **Hand-check:** pick one customer, look up each bin's points in the table, add them, and compare with `pd_to_score` of the model PD. They must agree within ±1 point (rounding to 2 dp per bin). This is acceptance criterion #3.

**Pitfalls:** fitting the binner on all data (leakage — your valid AUC will look too good); keeping a variable with the wrong-sign coefficient (the loop above removes it); `pd_to_score` direction (higher score = lower PD — test it).

```powershell
git add -A; git commit -m "M2: baseline logit + WOE scorecard with points table; test AUC <fill from metrics.json>"
```

---

### M3 — ML challengers, calibration, SHAP (about 6 h) → **Mid-review**

**Goal:** XGBoost and LightGBM tuned on train only, isotonic calibration on valid, champion chosen on valid, SHAP reason codes.

1. **`models.py`** (add to the baseline) — Optuna TPE maximising 3-fold CV AUC **on train only**:

```python
import numpy as np, optuna
from lightgbm import LGBMClassifier
from sklearn.isotonic import IsotonicRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from xgboost import XGBClassifier

optuna.logging.set_verbosity(optuna.logging.WARNING)

def _xgb(params, seed):  return XGBClassifier(tree_method="hist", eval_metric="auc", n_jobs=-1, random_state=seed, **params)
def _lgbm(params, seed): return LGBMClassifier(subsample_freq=1, n_jobs=-1, random_state=seed, verbose=-1, **params)

def _space(trial, kind):
    p = {"n_estimators": trial.suggest_int("n_estimators", 150, 600),
         "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1, log=True),
         "subsample": trial.suggest_float("subsample", 0.6, 1.0),
         "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
         "reg_lambda": trial.suggest_float("reg_lambda", 0.1, 20.0, log=True)}
    if kind == "xgb":
        p["max_depth"] = trial.suggest_int("max_depth", 2, 6)
        p["min_child_weight"] = trial.suggest_float("min_child_weight", 1, 50, log=True)
    else:
        p["num_leaves"] = trial.suggest_int("num_leaves", 8, 64)
        p["min_child_samples"] = trial.suggest_int("min_child_samples", 20, 200)
    return p

def tune_and_fit(kind, X, y, n_trials=30, cv_folds=3, seed=42):
    make = _xgb if kind == "xgb" else _lgbm
    cv = StratifiedKFold(cv_folds, shuffle=True, random_state=seed)
    obj = lambda t: cross_val_score(make(_space(t, kind), seed), X, y, cv=cv, scoring="roc_auc").mean()
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=seed))
    study.optimize(obj, n_trials=n_trials)
    return make(study.best_params, seed).fit(X, y), study.best_params, float(study.best_value)

def fit_isotonic(p_valid, y_valid):
    """Monotone map raw probability -> calibrated PD, fitted on VALID only."""
    return IsotonicRegression(out_of_bounds="clip", y_min=1e-4, y_max=1 - 1e-4).fit(np.asarray(p_valid), np.asarray(y_valid))

def predict_pd(model, X, calibrator=None):
    p = model.predict_proba(X)[:, 1]
    return calibrator.predict(p) if calibrator is not None else p
```

2. **`evaluate.py`** — metrics. KS = max gap between score distributions of defaulters and non-defaulters; calibration slope = coefficient from `Logit(y ~ logit(p))`; PSI with quantile bins of the *expected* sample.

```python
import numpy as np, pandas as pd, statsmodels.api as sm
from scipy.stats import ks_2samp
from sklearn.metrics import brier_score_loss, roc_auc_score

auc   = lambda y, p: float(roc_auc_score(y, p))
gini  = lambda y, p: 2 * auc(y, p) - 1
brier = lambda y, p: float(brier_score_loss(y, p))

def ks(y, p):
    y, p = np.asarray(y), np.asarray(p)
    return float(ks_2samp(p[y == 1], p[y == 0]).statistic)

def calibration_slope(y, p, eps=1e-6):
    p = np.clip(np.asarray(p, dtype=float), eps, 1 - eps)
    z = np.log(p / (1 - p))
    return float(sm.Logit(np.asarray(y), sm.add_constant(z)).fit(disp=0).params[1])

def metrics(y, p):
    return {"auc": auc(y, p), "gini": gini(y, p), "ks": ks(y, p), "brier": brier(y, p), "cal_slope": calibration_slope(y, p)}

def calibration_table(y, p, n_bins=10):
    df = pd.DataFrame({"y": np.asarray(y), "p": np.asarray(p)})
    df["bin"] = pd.qcut(df["p"].rank(method="first"), n_bins, labels=False)
    return df.groupby("bin").agg(mean_pred=("p", "mean"), obs_rate=("y", "mean"), n=("y", "size")).reset_index()

def decile_table(y, p, n=10):
    df = pd.DataFrame({"y": np.asarray(y), "p": np.asarray(p)})
    df["decile"] = pd.qcut(df["p"].rank(method="first", ascending=False), n, labels=range(1, n + 1))   # 1 = riskiest
    t = df.groupby("decile", observed=True).agg(n=("y", "size"), bads=("y", "sum"), bad_rate=("y", "mean"), avg_pd=("p", "mean"))
    t["cum_bad_capture"] = t["bads"].cumsum() / t["bads"].sum()
    t["lift"] = t["bad_rate"] / df["y"].mean()
    return t.reset_index()

def psi(expected, actual, bins=10, eps=1e-4):
    expected, actual = np.asarray(expected, dtype=float), np.asarray(actual, dtype=float)
    edges = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    e = np.clip(np.histogram(expected, edges)[0] / len(expected), eps, None)
    a = np.clip(np.histogram(actual, edges)[0] / len(actual), eps, None)
    return float(np.sum((a - e) * np.log(a / e)))
```

3. **`explain.py`** — SHAP on the XGBoost model (log-odds contributions; positive = pushes PD up) and plain-English reason codes (top-4 features that *increase* this customer's risk).

```python
import numpy as np, shap

TEMPLATES = {"avg_util": "High average utilisation ({v:.0%})", "util_1": "High utilisation last month ({v:.0%})",
             "max_delay": "Worst payment delay of {v:.0f} month(s)", "n_months_delayed": "{v:.0f} of last 6 months delayed",
             "delay_trend": "Delinquency getting worse (trend {v:+.2f})", "PAY_0": "Latest repayment status code {v:.0f} (1+ = late)",
             "avg_pay_ratio": "Pays only {v:.0%} of the amount billed", "pay_ratio_1": "Last payment covered only {v:.0%} of the previous bill",
             "LIMIT_BAL": "Low credit limit (NT$ {v:,.0f})", "bill_growth": "Outstanding bill rising ({v:+.0%} of limit)",
             "util_volatility": "Unstable utilisation (sd {v:.0%})"}

def shap_values(model, X):
    sv = shap.TreeExplainer(model).shap_values(X)
    return np.asarray(sv[1] if isinstance(sv, list) else sv)

def reason_codes(row, sv_row, cols, k=4):
    out = []
    for j in np.argsort(-sv_row):
        if sv_row[j] <= 0 or len(out) == k:
            break
        out.append(TEMPLATES.get(cols[j], "{n} = {v:.2f}").format(n=cols[j], v=row[cols[j]]))
    return out
```
   Compute SHAP on a 1,000-row sample (full-test SHAP is slow and unnecessary). Do not use SHAP on the isotonic-calibrated output — explain the raw tree model.

4. **`train.py`** — orchestration. One function `run(trials=None)` that: loads/splits; fits baseline; fits scorecard; tunes XGB and LGBM; fits isotonic on valid; **picks the champion by valid AUC among the non-baseline models**; computes metrics for valid and test exactly once; writes `outputs/metrics.json`, `outputs/scorecard_points.csv`, `outputs/test_predictions.csv`, `models/{xgb,lgbm,scorecard}.joblib`. Skeleton:

```python
def run(trials=None):
    cfg = load_config(); seed = cfg["seed"]; np.random.seed(seed); random.seed(seed)
    tr, va, te = [add_features(d) for d in build_splits(cfg)]
    cols = feature_cols(tr, cfg); raw_cols = [c for c in cols if c in RAW_FEATURES]
    ytr, yva, yte = (d[TARGET].to_numpy() for d in (tr, va, te))
    pds = {}                                                   # model -> split -> PD
    base = fit_baseline_logit(tr[raw_cols], ytr, seed)
    pds["logit_raw"] = {"valid": base.predict_proba(va[raw_cols])[:, 1], "test": base.predict_proba(te[raw_cols])[:, 1]}
    bp = woe.fit_binning(tr[cols], ytr, cfg["scorecard"]["iv_min"], seed)
    iv = woe.iv_table(bp).set_index("name")["iv"]
    lr, sc_cols = sc.fit_logit_scorecard(woe.woe_transform(bp, tr[cols]), ytr, iv, cfg["scorecard"]["corr_max"], seed)
    pds["scorecard"] = {s: lr.predict_proba(woe.woe_transform(bp, d[cols])[sc_cols])[:, 1] for s, d in [("valid", va), ("test", te)]}
    for kind in ["xgb", "lgbm"]:
        model, params, cv_auc = tune_and_fit(kind, tr[cols], ytr, trials or cfg["models"]["optuna_trials"], cfg["models"]["cv_folds"], seed)
        iso = fit_isotonic(model.predict_proba(va[cols])[:, 1], yva)
        pds[kind] = {"valid": predict_pd(model, va[cols], iso), "test": predict_pd(model, te[cols], iso)}
        joblib.dump({"model": model, "calibrator": iso, "features": cols}, MODELS / f"{kind}.joblib")
    valid_auc = {k: ev.auc(yva, v["valid"]) for k, v in pds.items() if k != "logit_raw"}
    champion = max(valid_auc, key=valid_auc.get)               # chosen on VALID, never on test
    metrics = {k: {"valid": ev.metrics(yva, v["valid"]), "test": ev.metrics(yte, v["test"])} for k, v in pds.items()}
    metrics["champion"] = champion
    json.dump(metrics, open(OUT / "metrics.json", "w"), indent=2)
    # ... also save test_predictions.csv (y, pd of every model, score, band) and the scorecard bundle
```
   Run: `python -m src.credit.train --trials 30` (about 5–10 minutes on a laptop; use `--trials 5` while debugging).

5. Review the numbers: baseline vs scorecard vs xgb vs lgbm, valid and test. Compare with the targets in §1. **Sanity:** valid and test AUC within about 0.01 of each other; calibrated Brier ≈ 0.13–0.14 (Brier of always predicting the base rate is 0.172, so the models must be clearly below that); calibration slope near 1.0 for the isotonic-calibrated models.
6. **Mid-review deck** (outline in §9) and `notebooks/03_models.ipynb` with ROC, calibration and SHAP plots.

**Pitfalls:** tuning on valid and then reporting valid (report test); calibrating on train (use valid); SHAP on the calibrated output; `sv` being a list for older SHAP versions (handled by the `isinstance` line).

```powershell
git add -A; git commit -m "M3: tuned XGB/LGBM + isotonic calibration + SHAP; champion <name>, test AUC <x>, KS <y>"
```

---

### M4 — Economics, limit engine, fairness (about 5 h)

**Goal:** the ₹ answer — optimal cut-off, approval rate, bad rate, profit vs approve-all, sensitivity — and a fairness audit.

1. **`economics.py`** — all parameters come from `config.yaml`.

   - Expected loss per account `EL = PD × LGD × EAD`.
   - Expected profit per approved account `(1 − PD) × margin × EAD − PD × LGD × EAD`.
   - `EAD = LIMIT_BAL × avg_util` (floored at 5% so a zero-balance customer is not "free"), converted to ₹ with `fx_ntd_inr`.
   - Policy: approve customers with `PD ≤ cutoff`; sweep the cutoff 0.05–0.60; pick the maximum.

```python
import numpy as np, pandas as pd

def make_ead(limit_bal, avg_util, fx=1.0, floor_util=0.05):
    util = np.clip(np.asarray(avg_util, dtype=float), floor_util, 1.5)
    return np.asarray(limit_bal, dtype=float) * util * fx

def unit_profit(pd_, ead, margin, lgd):
    pd_, ead = np.asarray(pd_, dtype=float), np.asarray(ead, dtype=float)
    return (1 - pd_) * margin * ead - pd_ * lgd * ead

def realised_profit(y, ead, margin, lgd):                      # uses the actual outcome
    y, ead = np.asarray(y, dtype=float), np.asarray(ead, dtype=float)
    return (1 - y) * margin * ead - y * lgd * ead

def profit_curve(pd_, ead, y, margin, lgd, grid):
    pd_, ead, y = map(np.asarray, (pd_, ead, y))
    up, rp = unit_profit(pd_, ead, margin, lgd), realised_profit(y, ead, margin, lgd)
    rows = []
    for c in grid:
        m = pd_ <= c; n = int(m.sum())
        rows.append({"cutoff": float(c), "approval_rate": n / len(pd_),
                     "bad_rate_approved": float(y[m].mean()) if n else np.nan,
                     "exp_profit": float(up[m].sum()), "real_profit": float(rp[m].sum())})
    return pd.DataFrame(rows)

def find_optimal_cutoff(curve, col="exp_profit"):
    return curve.loc[curve[col].idxmax()]

def sensitivity_grid(pd_, ead, y, lgds, margins, grid):
    rows = []
    for lgd in lgds:
        for mg in margins:
            best = find_optimal_cutoff(profit_curve(pd_, ead, y, mg, lgd, grid))
            approve_all = float(unit_profit(pd_, ead, mg, lgd).sum())
            rows.append({"lgd": lgd, "margin": mg, "opt_cutoff": best["cutoff"], "exp_profit": best["exp_profit"],
                         "approve_all": approve_all, "uplift": best["exp_profit"] - approve_all})
    return pd.DataFrame(rows)

def limit_engine_value(bands, pd_, ead, margin, lgd, limits_cfg):
    """Profit change per band if the config's limit action is applied (EAD scales with the limit change, PD with pd_mult)."""
    df = pd.DataFrame({"band": np.asarray(bands), "pd": np.asarray(pd_), "ead": np.asarray(ead)})
    out = []
    for b, g in df.groupby("band"):
        a = limits_cfg[b]
        before = unit_profit(g["pd"], g["ead"], margin, lgd).sum()
        after = 0.0 if a["action"] == "decline" else unit_profit(np.clip(g["pd"] * a["pd_mult"], 0, 1), g["ead"] * (1 + a["limit_change"]), margin, lgd).sum()
        out.append({"band": b, "n": len(g), "action": a["action"], "profit_before": before, "profit_after": after, "delta": after - before})
    return pd.DataFrame(out).sort_values("band").reset_index(drop=True)
```

   **Sanity:** the optimum sits near the break-even PD `margin / (margin + lgd)` = 0.18 / 0.83 ≈ 0.22 *for a calibrated model on a customer-by-customer basis* — your cut-off should be in that neighbourhood. If it is at the edge of the grid (0.05 or 0.60), your EAD or margin units are wrong.

2. **Sensitivity:** LGD ∈ {0.45…0.85} × margin ∈ {0.10…0.26}; save `outputs/sensitivity_lgd_margin.csv` and a heat-map of profit uplift vs approve-all. In the memo, quote the **range** of optimal cut-offs and uplifts, not just the base case.

3. **Fairness (`fairness.py`)** — `SEX` is excluded from the model; audit outcomes by SEX and by age bucket (`<30`, `30-39`, `40-49`, `50+`): n, approval rate, bad rate among approved, default rate, AUC; disparate-impact ratio = group approval rate ÷ highest group approval rate (the "four-fifths rule" flag is a screening heuristic, not a legal finding).

```python
def group_report(y, p, approved, groups):
    df = pd.DataFrame({"y": np.asarray(y), "p": np.asarray(p), "approved": np.asarray(approved).astype(bool), "g": np.asarray(groups)})
    rows = []
    for g, d in df.groupby("g", observed=True):
        rows.append({"group": g, "n": len(d), "approval_rate": d["approved"].mean(),
                     "bad_rate_approved": d.loc[d["approved"], "y"].mean() if d["approved"].any() else np.nan,
                     "default_rate": d["y"].mean(), "auc": auc(d["y"], d["p"]) if d["y"].nunique() == 2 else np.nan})
    return pd.DataFrame(rows)

def disparate_impact(report):
    ref = report.loc[report["approval_rate"].idxmax(), "group"]
    out = report.copy()
    out["di_ratio"] = out["approval_rate"] / report.loc[report["group"] == ref, "approval_rate"].iloc[0]
    out["passes_80pct"] = out["di_ratio"] >= 0.8
    return out
```

4. **Monitoring (`monitor.py`)** — CSI per feature (same maths as PSI), and a drift simulation: scale `LIMIT_BAL` by 0.8 **on raw data and then recompute features** (utilisation depends on the limit — shifting a derived column would be wrong). Alert when PSI > 0.2.

```python
def csi_table(train, new, cols, alert=0.2):
    out = pd.DataFrame([{"feature": c, "psi": psi(train[c], new[c])} for c in cols]).sort_values("psi", ascending=False).reset_index(drop=True)
    out["status"] = pd.cut(out["psi"], [-1, 0.1, alert, 1e9], labels=["stable", "watch", "ALERT"])
    return out

def simulate_limit_shift(df_raw, shift=-0.20):
    d = df_raw.copy(); d["LIMIT_BAL"] = (d["LIMIT_BAL"] * (1 + shift)).round()
    return add_features(d)
```
   **Expected:** `LIMIT_BAL` PSI far above 0.2 under the shift; PSI of every feature between train and the untouched test < 0.1.

5. **`analysis/run_analysis.py`** — one script that reloads the splits and models and writes **everything**: the six EDA figures, ROC, calibration, lift, score distribution, profit curve, sensitivity heat-map, SHAP global bar, fairness CSVs, drift CSVs, reason-code sample, and **`outputs/summary.json`** with keys such as `auc_test, gini_test, ks_test, brier_test, cal_slope_test, auc_logit_raw, auc_scorecard, opt_cutoff, approval_rate, bad_rate_approved, bad_rate_all, profit_opt_inr, profit_approve_all_inr, uplift_inr, profit_opt_per_1000_inr, sens_cutoff_min/max, sens_uplift_min/max, fairness_di_min_sex/age, psi_limit_drift, psi_max_no_drift, top_shap_features`. Every number in the memo must come from this file.

   Evaluate economics on the **test** set only, with the champion's calibrated PD, and report both expected profit (model PD) and realised profit (actual outcomes `y`) — if they disagree wildly, the calibration is off.

```powershell
python analysis/run_analysis.py
git add -A; git commit -m "M4: economics (cutoff <x>, uplift Rs<y>), sensitivity, fairness, drift sim; summary.json"
```

---

### M5 — App, tests, CI, memo (about 5 h) → **Final review**

1. **`app/streamlit_app.py`** — four tabs, reading precomputed artifacts (no training in the app):

| Tab | Content |
|---|---|
| Score a customer | Form with the 23 raw inputs (prefill from a sample row) → `add_features` → champion PD → score, band, limit action (from `config.yaml`), top-4 reason codes (SHAP on the XGBoost model) |
| Portfolio | Score histogram, band table (`band_table.csv`), approval-rate vs bad-rate curve (`profit_curve.csv`) |
| Cut-off simulator | Sliders for LGD and margin → recompute `profit_curve` from `test_predictions.csv` → profit curve and optimal cut-off |
| Model health | PSI/CSI table (`csi_drift_sim.csv`), calibration plot, lift deciles |

   Load models with `@st.cache_resource` (`joblib.load(models/xgb.joblib)`), CSVs with `@st.cache_data`. Add a limitations caption: *Taiwan 2005 data, random split (no out-of-time test), margin/LGD are assumptions.*

   Since `models/*.joblib` is git-ignored, either commit a small `models/champion.joblib` for the deployed app (remove it from `.gitignore` explicitly) or generate it at app start from the cached data.

2. **Tests** — see §7. Run `pytest -q` and `ruff check .`.
3. **README** — problem → data → approach (mermaid) → results table (baseline logit, scorecard, XGB, LGBM; test AUC/Gini/KS/Brier) → benchmark R1 (0.783 / 0.424) → business impact → limitations → how to run (`python tasks.py all`).
4. **`docs/DECISION_MEMO.md`** and **`docs/MODEL_CARD.md`** — templates below.
5. Push to GitHub (check the no-reply address first) and deploy on Streamlit Community Cloud.

```powershell
git add -A; git commit -m "M5: Streamlit app, tests, CI, memo and model card"
```

---

## 6. Business layer — decision memo (fill from `outputs/summary.json`)

```markdown
# Decision memo — Card approval cut-off and limit policy
**Decision requested:** Approve the PD cut-off and limit actions below for new/review decisions on the card book.
**Recommendation:** Approve customers with PD ≤ {{opt_cutoff}} (score ≥ {{opt_cutoff_score}}); apply the band actions A–F in the limit table.
**Impact (test set, {{n_test}} customers, assumptions margin {{margin}}, LGD {{lgd}}, NT$→₹ {{fx}}):**
- Approval rate {{approval_rate}}; bad rate among approved {{bad_rate_approved}} vs {{bad_rate_all}} for approve-all.
- Expected profit ₹{{profit_opt_inr}} vs ₹{{profit_approve_all_inr}} approve-all → uplift ₹{{uplift_inr}} (₹{{uplift_per_1000_inr}} per 1,000 applicants).
- Across LGD 0.45–0.85 × margin 0.10–0.26 the optimal cut-off ranges {{sens_cutoff_min}}–{{sens_cutoff_max}}; the uplift stays positive in every cell ({{sens_uplift_min_inr}} minimum).  <-- only write this if it is true
**Evidence:** champion {{champion}} test AUC {{auc_test}}, KS {{ks_test}}, Gini {{gini_test}} vs baseline logit AUC {{auc_logit_raw}}; calibration slope {{cal_slope_test}}; top drivers {{top_shap_features}}.
**Risks & limitations:** Taiwan 2005 data and random split, so no out-of-time validation; margin and LGD are assumptions, not observed; fairness: disparate-impact minimum {{fairness_di_min_sex}} (sex) and {{fairness_di_min_age}} (age) — review before use.
**Next steps:** 3-month shadow run on recent data; PSI monitor with alert at 0.2 (limit shift of −20% gives PSI {{psi_limit_drift}}); recalibrate quarterly.
```

## 7. Tests (≥ 10; run offline on `tests/fixtures/uci350_sample.csv`)

`tests/conftest.py` provides `cfg`, `raw` (fixture CSV) and `splits` (clean → split → `add_features`) fixtures.

| Test | Asserts |
|---|---|
| `test_clean_maps_education_and_marriage` | After `clean`, EDUCATION ∈ {1,2,3,4}, MARRIAGE ∈ {1,2,3}; row count unchanged |
| `test_split_is_stratified_and_disjoint` | Index sets of train/valid/test are disjoint, union = all; default rate in each within 1 pp |
| `test_validate_rejects_bad_target` | Setting one target to 2 raises `AssertionError` |
| `test_utilisation_identity` | `util_1 * LIMIT_BAL == BILL_AMT1` (allclose) |
| `test_pay_ratio_bounds_and_delay_trend` | `pay_ratio_*` in [0, 1]; a customer with delays [0,0,0,1,2,3] oldest→newest has positive `delay_trend` |
| `test_no_target_leakage` | `TARGET` not in `feature_cols`; `SEX` not in `feature_cols`; no engineered column correlates \|r\| > 0.99 with the target |
| `test_woe_monotonic` | `woe_is_monotonic` true for every selected variable (fit on the fixture) |
| `test_iv_filter_drops_noise` | Add a pure-noise column; it is not selected |
| `test_pd_to_score_monotonic` | Higher PD → lower or equal score over a grid |
| `test_pd_to_score_anchor_points` | PD for odds 50:1 gives 600; PD for odds 100:1 gives 620 (±1e-6) |
| `test_points_table_reproduces_score` | `score_with_table` equals `pd_to_score` of the scorecard PD within ±1 point (before clipping) |
| `test_assign_band_is_ordered` | Increasing PD never moves to an earlier band letter |
| `test_ks_perfect_and_random` | KS = 1 for perfectly separated scores; near 0 for random |
| `test_calibration_slope_near_one_for_calibrated_scores` | Simulated y ~ Bernoulli(p) gives slope within 0.9–1.1 |
| `test_psi_zero_for_identical_and_positive_for_shift` | PSI(x, x) = 0; PSI(x, x + 1) > 0.2 |
| `test_profit_is_maximised_near_breakeven_pd` | With calibrated simulated PDs, optimal cut-off is within 0.05 of margin/(margin+lgd) |
| `test_approve_all_equals_sum_of_unit_profit` | Curve at cut-off 1.0 equals `unit_profit.sum()` |
| `test_limit_action_follows_config` | Bands A, E return the actions in the config |
| `test_disparate_impact_ratio` | Known two-group example gives the expected ratio |
| `test_drift_simulation_triggers_psi_alert` | −20% `LIMIT_BAL` shift gives PSI(`LIMIT_BAL`) > 0.2 |
| `test_end_to_end_smoke` | `train.run(trials=2, raw=fixture, out_dir=tmp_path, model_dir=tmp_path)` writes `metrics.json` with all four models (give `run` those optional arguments so tests never touch real outputs) |

## 8. Acceptance checklist

- [ ] `python tasks.py all` passes; `outputs/metrics.json` has auc/gini/ks/brier for logit, scorecard, xgb, lgbm.
- [ ] Champion test AUC ≥ 0.78 and KS ≥ 0.42 (if not, report the honest numbers and what you tried).
- [ ] Scorecard points-table sums reproduce the score within ±1 point.
- [ ] `DECISION_MEMO.md` states optimal cut-off, approval %, bad rate %, ₹ profit vs approve-all — all from `summary.json`.
- [ ] ≥ 10 tests including `test_pd_to_score_monotonic`, `test_woe_monotonic`, `test_no_target_leakage`.
- [ ] README has baseline-vs-model table, limitations, and the R1 benchmark comparison.
- [ ] Streamlit app runs locally with 4 tabs; CI is green.

## 9. Review slide outlines (10 slides each)

**Mid-review (after M3):** 1 Business problem and KPI · 2 Data (source, size, default rate, month alignment) · 3 EDA: the three strongest signals · 4 Cleaning and split decisions · 5 Feature engineering (utilisation, delay trend, pay ratio) · 6 Baseline AUC · 7 WOE scorecard: IV table and one binned variable · 8 Challengers: tuning setup, valid metrics · 9 Calibration and SHAP · 10 Plan for economics, fairness, app and risks.

**Final review (after M5):** 1 Recap and results table · 2 Score scale and bands · 3 Economics set-up and assumptions · 4 Profit vs cut-off and optimum · 5 Sensitivity heat-map · 6 Limit engine value by band · 7 Fairness audit · 8 Reason codes and demo screenshots · 9 Monitoring and drift alert · 10 Recommendation, ₹ impact, limits, next steps.

## 10. Stretch goals and interview talking points

**Stretch:** (1) Run the same pipeline on *Give Me Some Credit* (DATA.md) as a second portfolio and report separate metrics. (2) Reject-inference discussion (you only observe outcomes of approved customers in real life). (3) Monotonic constraints in XGBoost (`monotone_constraints`) so the challenger respects business logic. (4) Compare LGD assumptions to LendingClub charge-offs (DATA.md §4). (5) Temporal drift test by training on early `ID` chunks (not a true time order — state that).

**Likely questions:**
1. *Why WOE/logistic when XGBoost is better?* — Regulators and credit committees need an additive points table, monotonic bins and stable reason codes; the gap in AUC is the price of explainability, and you measured it.
2. *How did you avoid leakage?* — Split first; binning, scaling, calibration and tuning fitted on train/valid only; champion chosen on valid; test touched once.
3. *Why isotonic calibration, and what does the slope tell you?* — Tree probabilities are distorted; economics needs true PDs. Slope near 1 means the spread of predicted risk matches reality.
4. *How sensitive is the profit answer?* — State the LGD × margin grid range of cut-offs and that uplift stays positive (if it does); the assumptions are not in the data.
5. *Is it fair?* — SEX excluded from the model, audited by outcome; disparate-impact ratios reported; proxies (age, limit) still exist, so monitor and review.

## 11. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `fetch_ucirepo` fails or hangs | Loader falls back to the zip; or load the OpenML/HF mirror (DATA.md §4) |
| `ImportError: xlrd` | `pip install xlrd` (only for the `.xls` fallback) |
| All columns are `object` after `read_excel` | Use `header=1` |
| `optbinning` install is slow / fails | Large dependency tree (ortools, cvxpy); use Python 3.11 and `--only-binary :all:`; as a fallback bin with `pd.qcut` + manual WOE and enforce monotonicity by merging bins |
| Optuna run takes too long | `--trials 5`, or `n_jobs=4` in the model constructors |
| Scorecard sign loop removes many variables | Variables are highly correlated (the `PAY_*` family); that is expected — keep the one or two strongest |
| Calibration slope far from 1 on test | Calibrator fitted on a small valid set; try Platt scaling (`LogisticRegression` on the logit) and compare |
| Profit optimum at grid edge | Check EAD units (₹ vs NT$) and that PD is a probability, not a score |
| SHAP shape error | Older SHAP returns a list for binary models; the `isinstance(sv, list)` line handles it |

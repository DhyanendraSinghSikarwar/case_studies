# Project 07 — Churn Prediction + Uplift-based Retention

| | |
|---|---|
| Domain | E-commerce / subscription retention |
| Difficulty / effort | ★★★ · about 35–40 hours over 1.5 weeks |
| Repo name | `ampba-07-churn-uplift` |
| Python package (`PKG`) | `churnx` |
| Data | UCI Online Retail II (churn, real) + simulated offer pilot (Track A) + Hillstrom email RCT (Track B, real treatment data). See [DATA.md](DATA.md) |
| Shared setup | [../00-COMMON-SETUP.md](../00-COMMON-SETUP.md) |

---

## 1. What you are building

Retention budgets are wasted on customers who would stay anyway or who cannot be saved. You will (1) predict who will **churn** in the next 90 days, (2) choose a **cost-optimal contact threshold**, (3) estimate **who actually responds to an offer** (uplift) from randomised data, and (4) compare six targeting policies in ₹ — including why "target the highest-risk customers" can lose money.

Two tracks, because no public dataset has *both* churn history and a randomised retention offer with a known true effect:

| Track | Data | What it gives |
|---|---|---|
| **A — master-plan path** | Online Retail II churn labels + a **simulated** 50/50 offer pilot whose true effect τ you define | The full policy-vs-**oracle** comparison (only possible because τ is known) |
| **B — real treatment data** | **Hillstrom email RCT** (64,000 customers, 3 arms, outcomes visit/conversion/spend) | Qini/uplift on a *real* experiment, and an honest **oracle-free** policy evaluation (IPW) with confidence intervals |

State clearly in the README which results come from simulated treatment (A) and which from real treatment (B).

**KPIs (master plan):** churn AUC ≥ 0.75; Qini coefficient > 0; incremental profit of uplift policy > risk-only policy > random; uplift policy ≥ 70% of the oracle; `test_features_before_asof` passes.

## 2. Read first

| Repo | Look at |
|---|---|
| [akash-sood97/partner-retention-system](https://github.com/akash-sood97/partner-retention-system) | Cost-optimal threshold; uplift targeting from a randomised pilot (their ₹1.17M vs ₹1.33M ceiling story; risk-only losing money) |
| scikit-uplift docs: https://www.uplift-modeling.com/ | Metric definitions (Qini, uplift@k) to cross-check your hand-rolled versions |

## 3. Step 0 — project setup

```powershell
cd "C:\Users\11624\OneDrive - Indian School of Business\Documents\personal\isb_ampba\projects\07-churn-uplift-retention"
py -3.11 -m venv C:\venvs\ampba-07
C:\venvs\ampba-07\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel
pip install -r requirements.in
$pkg = "churnx"
mkdir config, data\raw, data\interim, data\processed, notebooks, "src\$pkg", analysis, outputs, figures, models, app, tests\fixtures, docs, .github\workflows
New-Item "src\$pkg\__init__.py", tests\__init__.py -ItemType File
git init
```
Follow common setup §3–§8 and `pip install -e .`. `config/config.yaml`:

```yaml
seed: 42
paths: {raw: data/raw, interim: data/interim, processed: data/processed, outputs: outputs, figures: figures, models: models}
snapshots:
  train: ["2011-03-01", "2011-04-01", "2011-05-01"]
  test: "2011-08-01"
  lookback_days: 180          # eligibility + feature window
  min_orders: 2               # eligible = >= 2 distinct invoices in the lookback window
  horizon_days: 90            # churn = no purchase in the next 90 days
business:                     # ALL assumptions live here and are swept in sensitivity tables
  gbp_to_inr: 105.0           # assumption - update to the current rate
  gross_margin: 0.30
  clv_months: 12              # months of margin credited to a saved customer
  offer_cost_inr: 250.0       # cost per customer who receives the offer
  save_rate: 0.20             # risk-only policy: P(offer saves a would-be churner), assumed constant
pilot:
  treat_share: 0.5
  extra_snapshots: ["2010-12-01", "2011-01-01", "2011-02-01"]   # more history for the pilot training cohorts
hillstrom:
  email_cost_usd: 0.10        # assumption: cost of one e-mail
  margin_on_spend: 0.30       # assumption: gross margin on the recorded spend
```
Write `docs/PROBLEM_STATEMENT.md` and a `docs/SIMULATOR.md` stub (filled in M3).

## 4. Data (summary — see DATA.md)

Online Retail II: UK online retailer, 2009-12-01 → 2011-12-09, 1,067,371 raw invoice lines (per the UCI metadata). Convert the Excel file to parquet once (it takes minutes to read). Hillstrom: one CSV, 64,000 rows, columns `recency, history_segment, history, mens, womens, zip_code, newbie, channel, segment, visit, conversion, spend`.

---

## 5. Milestones

### M1 — Snapshots and churn labels (about 8 h)

**Goal:** a leak-free, point-in-time feature table per snapshot date with a 90-day churn label.

1. **`data.py`** — download the UCI zip, extract `online_retail_II.xlsx`, read **both sheets** (`pd.read_excel(path, sheet_name=None)`), stack, rename columns to `invoice, stock_code, description, quantity, invoice_date, unit_price, customer_id, country`, and cache as `data/interim/transactions.parquet`. Download Hillstrom to `data/raw/hillstrom.csv`.

```python
UCI_ZIP_URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
HILLSTROM_URL = "http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv"
TX_COLS = {"Invoice": "invoice", "StockCode": "stock_code", "Description": "description", "Quantity": "quantity",
           "InvoiceDate": "invoice_date", "Price": "unit_price", "Customer ID": "customer_id", "Country": "country"}

def load_transactions(force=False):
    cache = ROOT / cfg["paths"]["interim"] / "transactions.parquet"
    if cache.exists() and not force:
        return pd.read_parquet(cache)
    sheets = pd.read_excel(fetch_uci502(), sheet_name=None)           # dict: sheet name -> DataFrame (about 1-3 minutes)
    tx = pd.concat(sheets.values(), ignore_index=True).rename(columns=TX_COLS)
    tx["invoice"] = tx["invoice"].astype(str); tx["stock_code"] = tx["stock_code"].astype(str)
    tx["customer_id"] = tx["customer_id"].astype("Int64")
    tx.to_parquet(cache, index=False)
    return tx
```
2. **Clean (`snapshot.clean_sales`)** — split into `sales` and `returns`: drop rows without a customer ID; cancellations are invoices starting with `C`; drop non-product stock codes (`POST, D, DOT, M, BANK CHARGES, S, AMAZONFEE, ADJUST, ADJUST2, CRUK`); sales require `quantity > 0` and `unit_price > 0`; `revenue = quantity × unit_price`.
3. **Features (`build_features(sales, returns, asof)`)** — **only rows with `invoice_date < asof`**:

| Feature | Definition |
|---|---|
| `recency_days` | `asof` − last order date |
| `frequency_6m`, `monetary_6m`, `aov_6m` | orders, revenue and revenue/order in the last 180 days |
| `ipt_mean`, `ipt_std` | mean and std of days between consecutive orders (all history; ignore same-timestamp invoices) |
| `spend_trend` | `(spend last 90d − spend previous 90d) / (sum + 1)` — bounded in (−1, 1) |
| `n_returns` | cancellation invoices in the window |
| `n_skus_6m`, `items_per_order` | category breadth and basket size |
| `is_uk`, `tenure_days` | country and days since first order |

   Eligible customers at `asof`: ≥ `min_orders` distinct invoices in the last `lookback_days` days. Fill missing `ipt_mean` with the median and missing `ipt_std` with 0 (customers with a single gap).
4. **Label (`make_label`)** — churn = 1 if the customer has **no** sales invoice in `[asof, asof + 90 days)`. Assert that the label window ends before the last date in the data.
```python
def make_label(sales, customers, asof, horizon_days=90):
    asof = pd.Timestamp(asof); end = asof + pd.Timedelta(days=horizon_days)
    assert end <= sales["invoice_date"].max() + pd.Timedelta(days=1), "label window runs past end of data"
    bought = set(sales[(sales["invoice_date"] >= asof) & (sales["invoice_date"] < end)]["customer_id"].unique())
    return pd.Series((~customers.isin(bought)).astype(int).to_numpy(), index=customers.to_numpy(), name="churn")
```
5. Build three training snapshots (2011-03-01, 04-01, 05-01) and one test snapshot (2011-08-01). The last training label window ends 2011-07-30 < 2011-08-01, so **train and test labels do not overlap in time**. Print rows and churn rate per snapshot.
6. Save a ~2,000-row fixture of transactions to `tests/fixtures/` for tests.

**Sanity (measured with exactly this definition on the real file):**

| Snapshot | Eligible customers | Churn rate |
|---|---|---|
| 2010-12-01 / 2011-01-01 / 2011-02-01 (pilot history) | 1,999 / 1,962 / 1,863 | 48.6% / 48.2% / 46.2% |
| 2011-03-01 (train) | 1,822 | 42.7% |
| 2011-04-01 (train) | 1,758 | 41.2% |
| 2011-05-01 (train) | 1,551 | 35.7% |
| 2011-08-01 (test) | 1,471 | 28.5% |

Your numbers should match these closely (small differences come from the exact non-product code list). Notice that the churn rate **drifts from 49% to 28%** across snapshots: the August window (August–October) includes the pre-Christmas buying season, so the test churn rate is much lower than in training. A model's AUC can be fine while its *calibration* is off on the test snapshot — check the mean predicted probability against 28.5% and say so (this is why isotonic calibration on a later snapshot, or a recalibration step, matters). About 1,126 customers appear in both the training and the test snapshots; that is unavoidable in customer panels — keep group-aware folds inside training and keep the test snapshot strictly later. Feature columns have no NaNs after filling; `recency_days` is in [0, 179].

**Pitfalls:** any feature using `invoice_date ≥ asof` (the leak the test below catches); labelling customers as churned when the data simply ends (the assertion); counting returns as sales; using `Customer ID` as a float (precision loss).

```powershell
git add -A; git commit -m "M1: transactions parquet, point-in-time features, 90-day churn labels (3 train snapshots + test)"
```

---

### M2 — Churn models and cost-optimal threshold (about 7 h)

**Goal:** four models on a **temporal** split, calibration, lift, and the profit-maximising contact threshold.

1. Stack the three training snapshots (a customer appears up to three times — use **group-aware** folds on `customer_id` whenever you cross-validate or calibrate). Test on the 2011-08-01 snapshot.
2. **Baseline:** predict the training churn rate for everyone (AUC 0.5) — report it.
3. **Models (`models.py`):** logistic regression on signed-log1p + standardised features; RandomForest (400 trees, `min_samples_leaf=10`); XGBoost (300 trees, depth 3, lr 0.05); LightGBM (300 trees, 15 leaves, lr 0.05). Metrics: ROC-AUC, PR-AUC, KS (`max(tpr − fpr)`), Brier.
```python
def make_models(seed=42):
    from lightgbm import LGBMClassifier; from xgboost import XGBClassifier
    return {"logit": make_pipeline(FunctionTransformer(_signed_log1p), StandardScaler(), LogisticRegression(max_iter=2000, C=0.5)),
            "rf": RandomForestClassifier(n_estimators=400, min_samples_leaf=10, n_jobs=-1, random_state=seed),
            "xgb": XGBClassifier(n_estimators=300, max_depth=3, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, eval_metric="logloss", random_state=seed),
            "lgbm": LGBMClassifier(n_estimators=300, num_leaves=15, learning_rate=0.05, min_child_samples=30, subsample=0.8, subsample_freq=1, colsample_bytree=0.8, random_state=seed, verbose=-1)}
```
4. **Calibration** — `CalibratedClassifierCV(model, method="isotonic", cv=list(GroupKFold(3).split(X, y, groups)))` so a customer never sits in both the calibrator's train and validation folds. Plot a calibration curve and the **lift table** (deciles; churn rate, lift and cumulative capture).
5. **SHAP** for the champion tree model (summary plot; 3 sentences in the README on what drives churn).
6. **Cost-optimal threshold (`threshold.py`):**
   - value of saving a customer (₹) = `monetary_6m / 6 × clv_months × gross_margin × gbp_to_inr` (pre-snapshot spend only);
   - expected profit of contacting customer *i* = `p_i × save_rate × value_i − offer_cost`;
   - sweep the threshold 0–0.95; pick the maximum; report customers contacted and profit vs "contact nobody" and "contact everybody".
```python
def expected_profit(p, value, cost, save_rate): return np.asarray(p) * save_rate * np.asarray(value) - cost
def sweep_thresholds(p, value, cost, save_rate, grid=None):
    p, value = np.asarray(p), np.asarray(value); grid = np.linspace(0.0, 0.95, 96) if grid is None else grid
    return pd.DataFrame([{"threshold": float(t), "n_contacted": int((p >= t).sum()),
                          "profit_inr": float(expected_profit(p[p >= t], value[p >= t], cost, save_rate).sum())} for t in grid])
```
   Note the hidden assumption: `save_rate` is **constant** across customers — exactly what uplift modelling will challenge in M3. Add a sensitivity table over `save_rate ∈ {0.05, 0.10, 0.20, 0.30}` × `offer_cost ∈ {100, 250, 500}`.
7. Optional: Kaplan-Meier and Cox PH on time-to-next-purchase with `lifelines` (stretch).

**Targets / sanity:** champion AUC ≥ 0.75 on the test snapshot (the master plan target). Features are strongly time-aware (recency, inter-purchase time), so AUC in the 0.70s–0.80s is plausible; if it is above 0.95 you have a leak — run the test below. Compare train-snapshot CV AUC with the test AUC; a big gap means non-stationarity (Christmas seasonality moves the August snapshot's behaviour) — say so.

**Pitfalls:** random split across snapshots (leaks the same customer); calibrating on the same rows the model was fit on; counting the contact cost for customers below the threshold.

```powershell
git add -A; git commit -m "M2: churn models (test AUC <x>), isotonic calibration, cost-optimal threshold <t>"
```

---

### M3 — Pilot data and uplift models (about 10 h) → **Mid-review**

#### Track A — simulated randomised pilot with a known τ

**Why simulate:** to compare any targeting policy with the *oracle* you must know each customer's true response. The simulator uses **real baseline churn labels** and an **invented** treatment effect; document it in `docs/SIMULATOR.md`.

1. Build pilot cohorts from the training snapshots plus `extra_snapshots` (more history), and the test snapshot. Get an **out-of-fold** baseline churn probability `p0` for the training cohorts (group-aware 3-fold LightGBM) and the calibrated churn probability for the test cohort; clip to [0.01, 0.99].
2. **True save rate** (probability that the offer saves a would-be churner):
```python
def true_save_rate(df, rng):
    f = df["frequency_6m"].rank(pct=True).to_numpy()            # 0..1 within the cohort
    a = df["aov_6m"].rank(pct=True).to_numpy()                  # low = price sensitive
    mid_freq = np.exp(-((f - 0.5) / 0.25) ** 2)                 # bump centred on mid frequency
    base = 0.05 + 0.55 * mid_freq * (1.0 - a)
    base = np.where(f > 0.85, 0.0, base)                        # Champions do not respond
    base = np.where(df["recency_days"].to_numpy() > 100, base * 0.2, base)   # Hibernating rarely respond
    return np.clip(base + rng.normal(0, 0.03, len(df)), 0.0, 0.8)
```
3. **Randomise** `w ~ Bernoulli(0.5)`; a would-be churner who receives the offer is saved with probability `save_rate_true`; outcome `y = churn × (1 − saved)` if treated, else `churn`. Model **retention** (`retained = 1 − y`, higher is better). Ground truth: `tau_true = p0 × save_rate_true` (the effect on P(churn); equals the effect on retention). Keep `saved` and `tau_true` out of every feature set (a test asserts it).
```python
def simulate_pilot(df, p0, seed, treat_share=0.5):
    rng = np.random.default_rng(seed); out = df.copy(); out["p0"] = np.asarray(p0)
    out["w"] = (rng.random(len(out)) < treat_share).astype(int)
    out["save_rate_true"] = true_save_rate(out, rng)
    out["tau_true"] = out["p0"] * out["save_rate_true"]
    saved = (rng.random(len(out)) < out["save_rate_true"]) & (out["churn"] == 1)
    out["saved"] = saved.astype(int)
    out["y"] = np.where(out["w"] == 1, out["churn"] * (1 - out["saved"]), out["churn"])
    out["retained"] = 1 - out["y"]
    return out
```
   **Sanity:** the observed difference in retention between treated and control (`retained[w==1].mean() − retained[w==0].mean()`) should be close to `tau_true.mean()`.

#### Uplift learners (hand-rolled with scikit-learn/LightGBM)
Convention: `w ∈ {0,1}` (1 = treated), `y` higher is better, `tau_hat` = predicted incremental outcome from treating.

```python
class MetaLearner:                       # learner in {'S','T','X','TO'}
    def fit(self, X, w, y):
        X, w, y = np.asarray(X, float), np.asarray(w), np.asarray(y); self.e_ = float(w.mean()) if self.e is None else self.e
        if self.learner == "S":   self.m_ = clone(self.base).fit(np.column_stack([X, w]), y)
        elif self.learner == "T": self.m1_ = clone(self.base).fit(X[w == 1], y[w == 1]); self.m0_ = clone(self.base).fit(X[w == 0], y[w == 0])
        elif self.learner == "X":
            self.m1_ = clone(self.base).fit(X[w == 1], y[w == 1]); self.m0_ = clone(self.base).fit(X[w == 0], y[w == 0])
            d1 = y[w == 1] - _pred(self.m0_, X[w == 1], self.kind)          # imputed effect, treated
            d0 = _pred(self.m1_, X[w == 0], self.kind) - y[w == 0]          # imputed effect, control
            reg = default_base("continuous", self.seed)                     # stage 2 is always a regression
            self.t1_ = clone(reg).fit(X[w == 1], d1); self.t0_ = clone(reg).fit(X[w == 0], d0)
        elif self.learner == "TO":                                          # transformed outcome (needs known e)
            ystar = y * (w - self.e_) / (self.e_ * (1 - self.e_))           # E[ystar | x] = tau(x)
            self.m_ = clone(default_base("continuous", self.seed)).fit(X, ystar)
        return self
    def predict(self, X):
        X = np.asarray(X, float)
        if self.learner == "S": return _pred(self.m_, np.column_stack([X, np.ones(len(X))]), self.kind) - _pred(self.m_, np.column_stack([X, np.zeros(len(X))]), self.kind)
        if self.learner == "T": return _pred(self.m1_, X, self.kind) - _pred(self.m0_, X, self.kind)
        if self.learner == "X": return self.e_ * self.t0_.predict(X) + (1 - self.e_) * self.t1_.predict(X)
        return self.m_.predict(X)
```
(Base learner: a small LightGBM with 200 trees, 8 leaves, `min_child_samples=40`; `_pred` returns `predict_proba[:, 1]` for a binary outcome. X-learner stage 2 is always a regressor; its final blend is weighted by the propensity.)

**Evaluation metrics (hand-rolled, then cross-checked with `scikit-uplift`):**

```python
def qini_curve_manual(y, w, score):      # Q(k) = Y_T(k) - Y_C(k) * N_T(k) / N_C(k) for the top-k scored
    order = np.argsort(-np.asarray(score), kind="mergesort"); y, w = np.asarray(y)[order], np.asarray(w)[order]
    cy_t, cy_c = np.cumsum(y * (w == 1)), np.cumsum(y * (w == 0)); n_t, n_c = np.cumsum(w == 1), np.cumsum(w == 0)
    with np.errstate(divide="ignore", invalid="ignore"):
        q = cy_t - np.where(n_c > 0, cy_c * n_t / n_c, 0.0)
    return np.arange(1, len(y) + 1), q

def qini_auc_manual(y, w, score):        # area between the Qini curve and the random-targeting line
    n, q = qini_curve_manual(y, w, score); n = np.r_[0, n]; q = np.r_[0.0, q]
    rand = q[-1] * n / n[-1]
    return float(np.trapz(q, n) - np.trapz(rand, n))     # use np.trapezoid on numpy >= 2.0

def uplift_at_k(y, w, score, k=0.3):
    top = np.argsort(-np.asarray(score), kind="mergesort")[: int(len(y) * k)]
    y, w = np.asarray(y)[top], np.asarray(w)[top]
    return float(y[w == 1].mean() - y[w == 0].mean())
```
Cross-check: `from sklift.metrics import qini_auc_score, uplift_at_k` (check the argument order with `help(qini_auc_score)`: it takes `y_true, uplift, treatment`). Tiny numerical differences are expected because of tie-handling; the **ranking of learners** should agree. Include `tau_recovery(tau_hat, tau_true)` (Pearson, Spearman, RMSE) for Track A only.

Run S, T, X and transformed-outcome learners on the pilot; report Qini, uplift@30%, and τ-recovery; compare with an **oracle** score (`tau_true`) and a **random** score. Expect the oracle Qini to be the largest and random near 0; if a learner's Qini is negative it is worse than random targeting — report it.

#### Track B — Hillstrom (real randomised data)
```python
df = pd.read_csv("data/raw/hillstrom.csv")
df["w"] = (df.segment != "No E-Mail").astype(int)         # either e-mail vs none; also try Mens vs none, Womens vs none
X = pd.get_dummies(df[["recency", "history", "mens", "womens", "newbie", "zip_code", "channel"]], dtype=float)
tr, te = train_test_split(df.index, test_size=0.5, random_state=42, stratify=df.segment)
```
Check randomisation first: balance table of covariates by arm (means should match within noise). Then S/T/X/TO learners for `visit`, `conversion` and `spend`; Qini and uplift@30% on the held-out half; compare with `sklift`; plot Qini curves vs random. Hillstrom is a small, noisy effect (conversion rates around 0.6–1.3% across arms), so expect small Qini values and wide uncertainty — bootstrap them (500 resamples) and say so.

#### Mid-review
Build the deck (§9).

**Pitfalls:** fitting uplift models on test rows; using calibrated churn probabilities as `p0` computed on the same rows the pilot labels came from (use out-of-fold); a Qini curve with the sign flipped (higher score must mean "treat first"); using the *transformed outcome* learner without the correct propensity (it must be the randomisation probability).

```powershell
git add -A; git commit -m "M3: simulated pilot (known tau), S/T/X/TO uplift learners, Qini, Hillstrom real-RCT track"
```

---

### M4 — Policy comparison in ₹ (about 7 h)

**Goal:** six policies, evaluated exactly (Track A) and without an oracle (Track B).

**Policies** on the test cohort, each with a 30% contact budget unless noted:
`random`, `all` (no budget), `risk_top_k` (highest churn probability), `clv_top_k` (highest value), `uplift_top_k` (highest `tau_hat`), `profit_optimal` (contact iff `tau_hat × value − cost > 0`, no budget).

```python
def select_policies(cohort, tau_hat, p_churn, value_inr, budget_frac, cost, seed):
    n = len(cohort); k = int(round(budget_frac * n)); rng = np.random.default_rng(seed)
    def top_k(score):
        m = np.zeros(n, bool); m[np.argsort(-np.asarray(score), kind="mergesort")[:k]] = True; return m
    rnd = np.zeros(n, bool); rnd[rng.permutation(n)[:k]] = True
    return {"random": rnd, "all": np.ones(n, bool), "risk_top_k": top_k(p_churn), "clv_top_k": top_k(value_inr),
            "uplift_top_k": top_k(tau_hat), "profit_optimal": (np.asarray(tau_hat) * np.asarray(value_inr) - cost) > 0}

def exact_value(mask, tau_true, value_inr, cost):          # Track A only: uses the TRUE effect
    return float(((tau_true * value_inr - cost) * mask).sum())
oracle = (tau_true * value_inr - cost) > 0                  # perfect-hindsight policy: the ceiling
```
Track A table: policy, customers treated, profit (₹), % of oracle. **Target: uplift-based policy ≥ 70% of the oracle; uplift > risk-only > random.** Show that `risk_top_k` can be *negative* when high-risk customers are the ones who do not respond (price-insensitive "Hibernating" and Champions in the simulator) — this is the memo's headline, but it holds *by construction of your simulator*, so say so, and show what happens when you change the response pattern (sensitivity: re-run with the response bump centred on high frequency).

Track B (oracle-free, real data) — **inverse-propensity-weighted policy value:**
```python
def ipw_value(mask, w, y_money, e, cost):
    """Incremental profit if `mask` were treated: sum_i pi_i * y_i * (w_i/e - (1-w_i)/(1-e)) - cost * sum_i pi_i."""
    pi, w = np.asarray(mask, float), np.asarray(w, float)
    return float((pi * np.asarray(y_money, float) * (w / e - (1 - w) / (1 - e))).sum() - cost * pi.sum())

def bootstrap_ci(fn, n, n_boot=500, seed=0, alpha=0.05):
    rng = np.random.default_rng(seed); vals = np.array([fn(rng.integers(0, n, n)) for _ in range(n_boot)])
    return float(np.quantile(vals, alpha / 2)), float(np.quantile(vals, 1 - alpha / 2))
```
Use `y_money = spend × margin_on_spend`, `e = P(w=1)` of the experiment (≈ 2/3 for "any e-mail"), cost per e-mail from config. Evaluate on the held-out half only. Report each policy's profit per 1,000 customers with a bootstrap 95% CI; honest takeaway: the CI will often be wide, and a policy is only "better" if the intervals separate.

**Sanity checks:** profits are in the right sign and scale (if `all` contacts 6,000 customers at ₹250 each the cost alone is ₹1.5M); oracle ≥ every policy; `random` ≈ budget × average per-customer value.

```powershell
git add -A; git commit -m "M4: six-policy comparison (exact vs oracle, IPW on Hillstrom), uplift = <x>% of oracle"
```

---

### M5 — App, tests, CI, memo (about 5 h) → **Final review**

1. `analysis/run_analysis.py` writes `outputs/summary.json`: churn metrics, threshold and profit, uplift metrics per learner, policy table, % of oracle, Hillstrom Qini and IPW values with CIs.
2. **`app/streamlit_app.py`** tabs: **Churn risk** (score table, lift chart, threshold slider with profit curve) · **Uplift** (Qini curves, learner comparison) · **Policy simulator** (budget, offer cost, margin sliders → profit by policy) · **Hillstrom (real RCT)** (IPW table with CIs) · **About** (assumptions, what is simulated).
3. Tests (§7), CI, README (diagram, tables, limitations), `DECISION_MEMO.md`, `MODEL_CARD.md`.

```powershell
git add -A; git commit -m "M5: Streamlit app, tests, CI, memo"
```

---

## 6. Business layer — decision memo

```markdown
# Decision memo — Who should get the retention offer?
**Decision requested:** Replace "contact the highest-risk customers" with "contact customers with the highest expected incremental profit".
**Recommendation:** Run a 50/50 randomised pilot, fit an uplift model, then contact customers with predicted uplift × value > offer cost.
**Impact (simulated pilot; assumptions: margin {{margin}}, offer cost ₹{{cost}}, value horizon {{clv_months}} months):**
- Risk-only targeting earns ₹{{profit_risk}} ({{pct_risk}}% of the oracle); uplift targeting earns ₹{{profit_uplift}} ({{pct_uplift}}% of the oracle); random ₹{{profit_random}}.
- Churn model AUC {{auc}}; best contact threshold {{threshold}} contacts {{n_contacted}} customers.
**Evidence on real treatment data (Hillstrom e-mail test, {{n_hill}} customers):** Qini {{qini_hill}} (95% CI {{qini_lo}}–{{qini_hi}}); IPW profit per 1,000 customers: uplift top-30% {{ipw_uplift}} vs random {{ipw_random}} (CIs in the README).
**Why high-risk is not high-value:** customers most likely to churn are often those the offer cannot move; contacting them spends budget with no return. (This depends on the response pattern; in the simulator it is built in, in the Hillstrom data it is measured.)
**Risks & limitations:** pilot results are simulated; Hillstrom is an e-mail experiment for a different business; effects are small and noisy; margin and cost are assumptions; seasonality moves churn between snapshots.
**Next steps:** run the real pilot, log offers and outcomes, refit quarterly, monitor Qini on holdout.
```

## 7. Tests (≥ 10)

| Test | Asserts |
|---|---|
| `test_clean_sales_removes_cancellations_and_non_products` | No `C…` invoices, no `POST/M/D` codes, quantity and price > 0 |
| `test_features_before_asof` | Add a huge purchase on `asof + 1 day` to the fixture: features for `asof` are unchanged |
| `test_label_window_matches_horizon` | A customer buying on day 89 is not churned; buying on day 90 is churned |
| `test_label_window_assertion` | `make_label` raises when the window runs past the data |
| `test_eligibility_requires_min_orders` | A one-order customer is absent from the snapshot |
| `test_snapshots_do_not_overlap_in_label_time` | Last training label window ends before the test `asof` |
| `test_model_has_no_future_columns` | No feature name contains `churn`, `w`, `saved`, `tau`, `retained` |
| `test_group_calibration_never_splits_customers` | Customer IDs in each calibration train fold and validation fold are disjoint |
| `test_threshold_profit_is_maximal_on_grid` | `best_threshold` equals the argmax of the sweep; contacting nobody gives 0 |
| `test_expected_profit_sign` | Negative when `p × save_rate × value < cost` |
| `test_simulator_is_reproducible` | Same seed → identical `w`, `saved`, `y` |
| `test_pilot_ate_close_to_true_mean_tau` | Observed difference in retention within 3 standard errors of `tau_true.mean()` |
| `test_uplift_features_exclude_truth` | `tau_true`, `save_rate_true`, `saved`, `p0` are not in the uplift feature matrix |
| `test_qini_oracle_beats_random` | Oracle Qini > 0 and random-score Qini near 0 on simulated data |
| `test_qini_matches_sklift` | `qini_auc_manual` and `sklift.metrics.qini_auc_score` agree within tolerance on a simulated sample (skip if `sklift` is not installed) |
| `test_policy_masks_respect_budget` | Budgeted policies treat exactly `round(0.3 n)` customers |
| `test_oracle_is_ceiling` | Oracle profit ≥ every policy's exact profit |
| `test_ipw_value_unbiased_on_simulated_rct` | Averaged over many simulated experiments, IPW estimate ≈ exact value (within tolerance) |

## 8. Acceptance checklist

- [ ] Temporal split; `test_features_before_asof` passes.
- [ ] Churn AUC ≥ 0.75 on the test snapshot.
- [ ] Qini > 0 for the uplift learners on the pilot (and reported with CI on Hillstrom).
- [ ] Policy table with oracle ceiling; uplift policy ≥ 70% of the oracle; uplift > risk-only > random in the base case.
- [ ] Memo explains why "target highest-risk" can lose money and states which numbers are simulated.
- [ ] README distinguishes Track A (simulated treatment) from Track B (real treatment).

## 9. Review slide outlines

**Mid-review (after M3):** 1 Problem: wasted retention spend · 2 Data and the two tracks · 3 Churn definition and snapshots (no leakage) · 4 Features · 5 Model comparison and calibration · 6 Cost-optimal threshold and its constant-save-rate assumption · 7 Pilot design and simulator (what is invented) · 8 Uplift learners and Qini · 9 Hillstrom real-RCT results · 10 Policy evaluation plan.

**Final review (after M5):** 1 Recap · 2 Policy table vs oracle · 3 Why risk ≠ uplift (segments) · 4 Real-data evidence (IPW with CIs) · 5 Sensitivity to margin, cost and response pattern · 6 App demo · 7 Monitoring and refit cadence · 8 Limitations · 9 Pilot design · 10 Recommendation.

## 10. Stretch goals and interview talking points

**Stretch:** `causalml` comparison; Criteo uplift dataset (DATA.md) for scale; Cox PH time-to-churn; budget-constrained knapsack (maximise Σ tau × value − cost subject to a budget); Qini with confidence bands.

**Likely questions:**
1. *Why is the highest-risk customer not the best target?* — Churn probability measures baseline risk, not responsiveness; incremental profit needs `tau × value − cost`.
2. *How do you evaluate an uplift model when you only observe one outcome per customer?* — Qini/AUUC on randomised data; policy value via IPW; in simulation, exact value against a known τ.
3. *What is the Qini coefficient?* — Area between the cumulative incremental-outcome curve of your ranking and the random-targeting line.
4. *What are the limits of a simulated pilot?* — The conclusion depends on the invented response function; hence the sensitivity analysis and the real Hillstrom track.
5. *How did you prevent leakage?* — Point-in-time features (`< asof`), label windows that never overlap the test snapshot, group-aware folds, temporal validation.

## 11. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `read_excel` takes minutes | Expected; convert to parquet once |
| `np.trapz` AttributeError | NumPy ≥ 2 renamed it `np.trapezoid`; use `getattr(np, "trapezoid", None) or np.trapz` |
| `scikit-uplift` install fails | Skip the cross-check (tests skip) — the hand-rolled metrics are the deliverable |
| AUC above 0.95 | Leakage — run `test_features_before_asof` and `test_model_has_no_future_columns` |
| Qini negative for every learner | Sign convention: score = predicted incremental *retention* (higher = treat), outcome higher is better |
| Policy profits all negative | Offer cost too high relative to value; check `gbp_to_inr`, margin, `clv_months` in config |
| Hillstrom learners near zero Qini | The effect is small; use more bootstrap resamples and report uncertainty rather than tuning |

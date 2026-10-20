# Project 08 — Two-sided Marketplace Dynamic Pricing

| | |
|---|---|
| Domain | Home-services / quick-commerce / gig platforms |
| Difficulty / effort | ★★★★ · about 40–45 hours over 2 weeks |
| Repo name | `ampba-08-two-sided-pricing` |
| Python package (`PKG`) | `mkt` |
| Data | Simulator with known truth (contract path) + NYC TLC ride-hailing trips for calibration. See [DATA.md](DATA.md) |
| Shared setup | [../00-COMMON-SETUP.md](../00-COMMON-SETUP.md) |

---

## 1. What you are building

A platform sets a **customer price** and a **partner payout** for each segment (city × service × time-slot). Raise the price and demand falls; cut the payout and fewer partners accept jobs, so more orders go unfulfilled. You will (1) simulate a marketplace with known true parameters and a history that includes randomised price/payout experiments, (2) **estimate** customer elasticity and partner acceptance from that history only, (3) **optimise** (price, payout) per segment under a fulfilment target and a payout floor, and (4) **validate** three policies — static, demand-only, two-sided — on a held-out period, with placebo tests and 400 parameter draws.

```mermaid
flowchart LR
  S[Simulator<br/>truth + 52-week log<br/>20% randomised +-10% experiments] --> E[Estimation<br/>elasticity: FE log-log<br/>acceptance: logistic GLM]
  E --> O[Optimiser<br/>grid over price x payout<br/>fulfilment >= 90%, floor Rs220]
  O --> P[3 policies<br/>static / demand-only / two-sided]
  P --> V[Validation on the TRUE market<br/>holdout, placebo, 400 draws]
  T[(TLC real trips)] -. calibrates shapes .-> S
```

**KPIs (master plan):** contribution uplift vs current pricing; fulfilment rate; partner earnings per hour. **Acceptance:** estimated elasticities within ±20% of the simulator truth; two-sided > demand-only > static on holdout contribution with fulfilment ≥ 90%; two-sided wins in ≥ 80% of 400 parameter draws.

## 2. Read first

| Repo | Look at |
|---|---|
| [akash-sood97/two-sided-pricing-engine](https://github.com/akash-sood97/two-sided-pricing-engine) | Two-sided demand (customer elasticity + partner drop-off), per-segment optimiser with a ₹220 payout floor and 90% fulfilment, +7.1% contribution vs +3.2% for demand-only, holdout/placebo/400-draw robustness |

## 3. Step 0 — project setup

```powershell
cd "C:\Users\11624\OneDrive - Indian School of Business\Documents\personal\isb_ampba\projects\08-two-sided-marketplace-pricing"
py -3.12 -m venv C:\venvs\ampba-08
C:\venvs\ampba-08\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel
pip install -r requirements.in
$pkg = "mkt"
mkdir config, data\raw, data\interim, data\processed, data\truth, notebooks, "src\$pkg", analysis, outputs, figures, models, app, tests\fixtures, docs, .github\workflows
New-Item "src\$pkg\__init__.py", tests\__init__.py -ItemType File
mkdir C:\ampba_data\08            # big TLC files go here, outside OneDrive
git init
```
Follow common setup §3–§8; add `data/truth/` to `.gitignore` is **not** needed (tiny), but keep it separate from features. `config/config.yaml`:

```yaml
seed: 42
paths: {raw: data/raw, interim: data/interim, processed: data/processed, outputs: outputs, figures: figures, models: models}
data_dir: C:/ampba_data/08
sim:
  n_weeks: 52
  holdout_weeks: 12
  cities: [Mumbai, Delhi NCR, Bengaluru, Hyderabad, Pune, Chennai]
  city_demand_mult: [1.30, 1.25, 1.20, 0.95, 0.80, 0.75]
  city_price_idx: [1.12, 1.10, 1.10, 1.00, 0.96, 0.94]
  services: [cleaning, plumbing, electrician, salon_at_home, ac_service]
  service_p0: [499, 399, 399, 899, 699]
  service_d0: [900, 500, 550, 600, 450]
  service_season_phase: [0, 10, 20, 30, 14]
  eps_mean: -3.2
  eps_service_shift: [0.0, 0.5, 0.5, -0.4, -0.2]
  eps_city_sd: 0.15
  eps_slot_sd: 0.10
  eps_seg_sd: 0.15
  eps_clip: [-4.5, -1.2]
  slots: [morning, afternoon, evening, night]
  slot_weight_tlc: [0.2014, 0.2266, 0.3424, 0.2296]     # measured on TLC 2023-01 (DATA.md); recompute in M1
  night_factor: 0.45
  take_rate_mean: 0.35
  take_rate_sd: 0.03
  var_cost_share: 0.06
  var_cost_fixed: 15.0
  weekly_noise_sd: 0.06
  season_amp: 0.15
  festival_week: 43
  festival_amp: 0.25
  partner_jobs_per_week: 8
  cap_ratio_range: [0.95, 1.35]
  accept_alpha: 0.5
  accept_beta: 0.018
  reservation_share: 0.55
  reservation_sd: 0.04
  churn_base: 0.02
  churn_extra: 0.06
  churn_threshold_share: 0.65
  recruit_rate: 0.03
  experiment_share: 0.20
  experiment_step: 0.10
business:
  payout_floor: 220
  fulfil_target: 0.90
  fulfil_buffer: 0.02
  earnings_keep: 0.95
  price_bounds: [0.85, 1.25]
  payout_bounds: [0.90, 1.25]
  grid_n_price: 26
  grid_n_payout: 24
```
Write `docs/PROBLEM_STATEMENT.md` and start `docs/SIMULATOR.md` (every row of the DATA.md §3 table, with the assumption flagged).

## 4. Data (summary — see DATA.md)

Real: NYC TLC HVFHV trips (rider fare + driver pay per trip). Synthetic: a 120-segment, 52-week marketplace log; a separate **answer key** (`truth`) used only for testing and final evaluation.

---

## 5. Milestones

### M1 — Real-data calibration + simulator (about 10 h)

**Step A — real-data look (about 2 h).** Read January 2023 HVFHV with DuckDB (code in DATA.md §2). Compute: (1) trip share by slot (check against the four numbers in the config), (2) take rate `1 − driver_pay/base_passenger_fare` by company — median, quartiles (robust: ignore rows with non-positive fare/pay), (3) zone-hour panel: trips, mean fare per mile; (4) **the identification demo:** within each zone, the correlation of `ln(trips)` and `ln(fare per mile)` across hours — expect a clearly **positive** median (≈ 0.57 was measured), which is surge, not elasticity. Save `figures/tlc_surge_confounding.png` (scatter for the busiest zone) and `outputs/tlc_calibration.json`.

**Step B — truth table (`sim.make_truth`)**: one row per segment with the true parameters.

```python
def make_truth(cfg, rng):
    s = cfg["sim"]; rows = []
    city_eff = rng.normal(0, s["eps_city_sd"], len(s["cities"]))
    slot_eff = rng.normal(0, s["eps_slot_sd"], len(s["slots"]))
    slot_w = np.array(s["slot_weight_tlc"]) * 4.0; slot_w[3] *= s["night_factor"]      # night is quiet for home services
    for (ci, c), (si, sv), (ti, sl) in itertools.product(enumerate(s["cities"]), enumerate(s["services"]), enumerate(s["slots"])):
        p0 = s["service_p0"][si] * s["city_price_idx"][ci]
        d0 = s["service_d0"][si] * s["city_demand_mult"][ci] * slot_w[ti] * rng.lognormal(0, 0.15)
        eps = float(np.clip(s["eps_mean"] + s["eps_service_shift"][si] + city_eff[ci] + slot_eff[ti] + rng.normal(0, s["eps_seg_sd"]), *s["eps_clip"]))
        take = float(np.clip(rng.normal(s["take_rate_mean"], s["take_rate_sd"]), 0.15, 0.45))
        w0 = (1 - take) * p0                                         # static payout
        r = s["reservation_share"] * p0 * (1 + rng.normal(0, s["reservation_sd"]))    # partner reservation payout
        cap0 = rng.uniform(*s["cap_ratio_range"]) * d0
        rows.append(dict(seg=len(rows), city=c, service=sv, slot=sl, p0=p0, d0=d0, eps=eps, w0=w0, take0=take,
                         reservation=r, cap0=cap0, n0=cap0 / s["partner_jobs_per_week"],
                         var_cost=s["var_cost_share"] * p0 + s["var_cost_fixed"]))
    truth = pd.DataFrame(rows); truth.attrs["alpha"], truth.attrs["beta"] = s["accept_alpha"], s["accept_beta"]
    return truth
```

**Step C — weekly dynamics (`simulate_history`)**: for each of the 52 weeks and every segment:
- draw an experiment flag (20%) and independent ±10% signs for price and payout; the **static policy** holds price `p0` and payout `w0` otherwise;
- demand `λ = d0 × season × (price/p0)^ε × η` with `η` lognormal noise and `season` = service annual wave × a festival bump near week 43; `requests ~ Poisson(λ)`;
- supply: `cap = round(N × 8)` job offers; acceptance `A = sigmoid(α + β (payout − reservation))`; `accepted ~ Binomial(cap, A)`; `fulfilled = min(requests, accepted)`;
- partner earnings per partner `= payout × fulfilled / N`; contribution `= fulfilled × (price − payout − var_cost)`;
- partner churn: `leave ~ Binomial(N, 0.02 + 0.06 × [earnings < θ])` with `θ = 0.65 × w0 × 8`; recruitment `Poisson(0.03 × n0)`.
```python
def season_index(cfg, truth, weeks):
    s = cfg["sim"]; phase = dict(zip(s["services"], s["service_season_phase"])); out = np.ones((len(truth), len(weeks)))
    for i, sv in enumerate(truth["service"]):
        wave = 1 + s["season_amp"] * np.sin(2 * np.pi * (weeks - phase[sv]) / 52)
        fest = 1 + s["festival_amp"] * np.exp(-0.5 * ((weeks - s["festival_week"]) / 1.5) ** 2)
        out[i] = wave * fest
    return out
```
Write `simulate_history` yourself from the bullets (about 35 lines). The log columns: `week, seg, price, payout, experiment, requests, offers, accepted, fulfilled, partners, earn_per_partner, contribution`. `build_dataset(cfg)` returns `(log, truth, meta)` where `meta = truth[["seg","city","service","slot","p0","w0","reservation","var_cost"]]` — what an analyst would know. **Write `truth` to `data/truth/` and the log to `data/processed/`; the estimation module must never import `make_truth`.**

**Step D — optional Online Retail II analogy (2 h):** re-use Project 05's log-log regression to see what an elasticity from a retail dataset looks like; document why it is not used as the prior (DATA.md §3).

**Sanity checks:** experiment share ≈ 0.20; overall fulfilment rate high but with a visible minority of segment-weeks below 90% (that is what creates something to optimise); partner counts drift but do not collapse; total contribution positive in every segment under the static policy.

```powershell
python -m src.mkt.data
git add -A; git commit -m "M1: TLC real-data calibration + two-sided marketplace simulator (120 segments x 52 weeks)"
```

---

### M2 — Estimation and recovery tests (about 9 h)

**Goal:** estimate the demand elasticity and the partner acceptance curve from the log **training weeks only** (weeks 1–40) and show they match the truth.

1. **Prep:** `ln_req = ln(requests.clip(1))`, relative price `ln_p = ln(price/p0)` (zero outside experiments), `x_w = payout − reservation`, a `svc_week` key.
2. **Service elasticity** with two sets of fixed effects (segment and service×week) absorbed by alternating demeaning, using only price variation from the randomised experiments (+ robust HC1 standard errors):
```python
def _demean2(df, cols, g1, g2, iters=50):
    out = df[cols].astype(float).copy()
    for _ in range(iters):
        before = out.values.copy()
        out = out - out.groupby(df[g1]).transform("mean"); out = out - out.groupby(df[g2]).transform("mean")
        if np.abs(out.values - before).max() < 1e-10: break
    return out

def fit_service_elasticity(d):
    services = sorted(d["service"].unique())
    X = pd.DataFrame({f"lnp_{sv}": d["ln_p"] * (d["service"] == sv) for sv in services})
    Z = pd.concat([d[["ln_req"]], X], axis=1).assign(seg=d["seg"].values, svc_week=d["svc_week"].values)
    Zd = _demean2(Z, ["ln_req"] + list(X.columns), "seg", "svc_week")
    m = sm.OLS(Zd["ln_req"], Zd[list(X.columns)]).fit(cov_type="HC1")
    return m, pd.DataFrame({"eps_hat": [m.params[f"lnp_{sv}"] for sv in services], "se": [m.bse[f"lnp_{sv}"] for sv in services]}, index=services)
```
3. **Segment elasticity** (one slope per segment, same FE) followed by **empirical-Bayes shrinkage** toward the service estimate: `tau² = max(var(raw − service) − mean(se²), 1e-4)`, weight `B = tau²/(tau² + se²)`, `eps_hat = eps_service + B × (eps_raw − eps_service)`.
4. **Acceptance:** binomial GLM of `(accepted, offers − accepted)` on `x_w` (spec A, with the reservation proxy) via `sm.GLM(y, sm.add_constant(d[["x_w"]]), family=sm.families.Binomial())`. Also run spec B (experiment rows only, segment dummies, slope on `payout − w0`) as a robustness check — it should recover β without needing the reservation proxy.
5. **De-priced demand level** `d0_hat` per segment: average over the last 8 training weeks of `requests / (price/p0)^eps_hat`.
6. **Recovery table (this is the test):** compare `eps_hat` with the truth. Service-level absolute % error and the **share of segments within ±20% of true ε** (raw vs shrunk); `alpha_hat, beta_hat` vs `0.5, 0.018`. **Acceptance:** service-level elasticities within ±20% of truth; report the segment-level share honestly (shrinkage should improve it).
7. **Placebo estimation:** shuffle `ln_p` within segment across weeks and re-estimate: the estimated elasticities should collapse toward zero. This proves the estimates come from the experiments, not from model artefacts.

**Pitfalls:** including non-experiment weeks as if they had price variation (they have `ln_p = 0`, fine, but the FE structure matters); regressing on raw price instead of relative price; using `truth` to pick the reservation proxy; ignoring that elasticities estimated near −1 make the optimiser degenerate (clip at −1.05 when optimising).

```powershell
git add -A; git commit -m "M2: FE elasticity + EB shrinkage + acceptance GLM; recovery within <x>% of truth"
```

---

### M3 — Market model, optimiser, three policies (about 9 h) → **Mid-review**

1. **Expected-value market model (`model.py`)** used by both the optimiser (with estimated parameters) and the evaluator (with true parameters): demand `d0 × season × (p/p0)^ε`; capacity `A(w) × N × 8`; fulfilled `= min(demand, capacity)`; contribution `= fulfilled × (p − w − var_cost)`; optional churn dynamics over a horizon.
```python
def evaluate(P, price, payout, season=None, eta=None, churn=False):
    s = P["cfg"]["sim"]; n = len(price); T = 12 if season is None else season.shape[1]
    season = np.ones((n, T)) if season is None else season; eta = np.ones((n, T)) if eta is None else eta
    N = P["N0"].copy(); out = {k: np.zeros((n, T)) for k in ["req", "ful", "contrib", "earn", "N"]}; A = acceptance(P, payout)
    for t in range(T):
        req = demand(P, price, season[:, t], eta[:, t]); acc = A * N * P["J"]; ful = np.minimum(req, acc)
        earn = payout * ful / np.maximum(N, 1e-9)
        out["req"][:, t], out["ful"][:, t], out["earn"][:, t], out["N"][:, t] = req, ful, earn, N
        out["contrib"][:, t] = ful * (price - payout - P["c"])
        if churn:
            q = s["churn_base"] + s["churn_extra"] * (earn < P["theta"])
            N = np.maximum(N * (1 - q) + s["recruit_rate"] * P["N0"], 1.0)
    return out
```
2. **Optimiser (`optimise.py`)** — vectorised grid over price multipliers (0.85–1.25, 26 points) × payout multipliers (0.90–1.25, 24 points) for every segment:
   - maximise `min(D(p), A(w) N J) × (p − w − c)`;
   - subject to fulfilment `min(1, A N J / D) ≥ 0.90 + 0.02 buffer`, payout ≥ ₹220, and partner earnings per partner-week ≥ 95% of the static earnings (so the policy cannot "win" by squeezing partners);
   - a segment with no feasible cell keeps its current price and payout.
```python
def grid_search(P, cfg, supply_aware=True, earnings_keep=0.95):
    b = cfg["business"]; n = len(P["p0"])
    mp, mw = np.linspace(*b["price_bounds"], b["grid_n_price"]), np.linspace(*b["payout_bounds"], b["grid_n_payout"])
    p = np.broadcast_to(P["p0"][:, None, None] * mp[None, :, None], (n, len(mp), len(mw)))
    w = np.broadcast_to(np.maximum(P["w0"][:, None, None] * mw[None, None, :], b["payout_floor"]), p.shape)
    PP = {**P, **{k: P[k][:, None, None] for k in ("p0", "eps", "d0", "r", "c")}}
    D = demand(PP, p); cap = acceptance(PP, w) * P["N0"][:, None, None] * P["J"]; ful = np.minimum(D, cap)
    if not supply_aware:                                    # demand-only: payout frozen at w0, supply ignored
        obj = D * (p - P["w0"][:, None, None] - P["c"][:, None, None])
        obj = np.where(np.arange(len(mw))[None, None, :] == 0, obj, -np.inf); feas = np.ones_like(obj, bool)
    else:
        obj = ful * (p - w - P["c"][:, None, None]); feas = ful / D >= b["fulfil_target"] + b["fulfil_buffer"]
        if earnings_keep is not None:
            ful0 = np.minimum(demand(PP, P["p0"][:, None, None]), acceptance(PP, P["w0"][:, None, None]) * P["N0"][:, None, None] * P["J"])
            feas &= (w * ful / P["N0"][:, None, None] >= earnings_keep * (P["w0"][:, None, None] * ful0 / P["N0"][:, None, None]))
    obj = np.where(feas, obj, -np.inf); flat = obj.reshape(n, -1); idx = flat.argmax(1); ok = np.isfinite(flat[np.arange(n), idx])
    ip, iw = np.unravel_index(idx, (len(mp), len(mw)))
    price = np.where(ok, P["p0"] * mp[ip], P["p0"]); payout = np.where(ok, np.maximum(P["w0"] * mw[iw], b["payout_floor"]), P["w0"])
    return price, (P["w0"].copy() if not supply_aware else payout), ok
```
   (The demand-only branch uses only the first payout column, which is why the demand-only policy keeps payout at `w0`. Write a unit test that the demand-only policy never changes payout.)
3. **Policies (`policies.py`):** `static` (price `p0`, payout `w0`), `demand_only` (optimise price on the demand curve alone, supply ignored), `two_sided` (joint optimisation under constraints).
4. **First holdout evaluation (weeks 41–52)** on the **true** market (`P_true` from the truth table, same start partner counts, common random numbers for `eta`, seasonality for those weeks, churn dynamics on): contribution, fulfilment, share of segments ≥ 90% fulfilment, partner earnings per partner-week, uplift vs static in %. **Target ordering: two-sided > demand-only > static on contribution with two-sided fulfilment ≥ 90%.** Demand-only usually raises price and hurts fulfilment — show the fulfilment gap.
5. **Mid-review deck** (§9).

**Pitfalls:** evaluating policies with the *estimated* parameters (circular — always evaluate against truth, optimise on estimates); forgetting the payout floor in the grid; elasticities above −1 in the optimiser (clip to ≤ −1.05); an infeasible segment silently getting a nonsense price (the code keeps the current price).

```powershell
git add -A; git commit -m "M3: market model, grid optimiser, three policies; two-sided +<x>% vs static on holdout"
```

---

### M4 — Validation: holdout, placebo, 400 draws (about 8 h)

1. **Temporal holdout table** — already produced in M3; finalise with confidence from 200 simulated demand-noise paths (vary `eta` seeds) and report mean and P10 of uplift.
2. **Placebo policy:** keep the two-sided *multipliers* but **shuffle them across segments within a service** (200 permutations). A recommendation without segment-specific information should earn ~no gain. Report real gain vs the placebo distribution and a permutation p-value.
3. **Full-pipeline placebo:** shuffle `ln_p` within segment, re-estimate, re-optimise, evaluate on truth — the gain should vanish (this tests the whole chain).
4. **400 parameter draws:** sample elasticities (service-level covariance from the OLS fit plus segment-level noise), acceptance `(α, β)` from the GLM covariance, and a small noise on `d0`; for each draw evaluate static / demand-only / two-sided against the **drawn** market and record whether two-sided beats both and meets 90% fulfilment. **Target: ≥ 80% of draws.** Report also with standard errors inflated ×3 and ×8 (stress test); say honestly where the 80% fails.
```python
def draw_robustness(P_hat, policies, draws, target=0.90):
    rows = []
    for Pd in draws:
        r = {n: M.summarise(M.evaluate(Pd, *policies[n], None, None, churn=False)) for n in ["static", "demand_only", "two_sided"]}
        rows.append(dict(beats_demand=r["two_sided"]["contribution"] > r["demand_only"]["contribution"],
                         beats_static=r["two_sided"]["contribution"] > r["static"]["contribution"],
                         fulfil_ok=r["two_sided"]["fulfilment"] >= target,
                         gain_vs_static_pct=100 * (r["two_sided"]["contribution"] / r["static"]["contribution"] - 1)))
    out = pd.DataFrame(rows); out["wins"] = out["beats_demand"] & out["beats_static"] & out["fulfil_ok"]
    return out
```
5. **Sensitivity (config sweeps):** payout floor ₹220/260/300; fulfilment target 85/90/95%; earnings-keep 0.90/0.95/1.00; take rate mean 0.23 (TLC median) vs 0.35. For each, re-run the policies and record uplift and whether the floor binds.

**Pitfalls:** drawing parameters independently when estimates are correlated (use the covariance); evaluating the draws with the *estimated* market instead of the drawn one; forgetting to keep `eps ≤ −1.05` in draws.

```powershell
git add -A; git commit -m "M4: holdout, placebo, full-pipeline placebo, 400-draw robustness (<x>% wins), sensitivities"
```

---

### M5 — App, tests, CI, memo (about 6 h) → **Final review**

1. `analysis/run_analysis.py` → `outputs/summary.json` (recovery errors, holdout table, placebo p-value, draw win-rate, sensitivity grid, TLC calibration numbers) and all figures.
2. **`app/streamlit_app.py`**: segment selector; sliders for price and payout multipliers; live demand, fulfilment and contribution (heat-map of contribution over the grid with the feasibility region and the optimum marked, `plotly.graph_objects.Heatmap`); policy comparison table; "real data" tab with the TLC surge-confounding chart.
3. Tests (§7), CI, README, `DECISION_MEMO.md`, `MODEL_CARD.md`, finish `docs/SIMULATOR.md`.
4. Optional static explorer (`stlite`).

```powershell
git add -A; git commit -m "M5: Streamlit explorer, tests, CI, memo"
```

---

## 6. Business layer — decision memo

```markdown
# Decision memo — Joint price and payout optimisation
**Decision requested:** Replace static price/payout with per-segment two-sided optimisation, starting with a pilot in {{n_pilot_segments}} segments.
**Recommendation:** Adopt two-sided optimisation with a ₹{{floor}} payout floor and a {{target}}% fulfilment guardrail.
**Impact (simulated market, 12-week holdout):** contribution {{uplift_two_sided}}% vs static (demand-only: {{uplift_demand_only}}%); fulfilment {{fulfil_two_sided}} vs {{fulfil_demand_only}} for demand-only; partner earnings per partner-week {{earn_ratio}} of static.
**Evidence:** estimated elasticities within {{max_svc_err}}% of truth; placebo gain {{placebo_mean}}% (p = {{placebo_p}}); two-sided wins in {{win_rate}}% of 400 parameter draws.
**Why demand-only fails:** it raises price without checking partner supply; unfilled orders and partner churn eat the gain.
**Risks & limitations:** the market is simulated; the true market has no randomised experiments unless you run them; elasticity −3.2 and the acceptance slope are assumptions; the TLC data shows price and demand rising together (surge), so elasticities cannot be read from observational data.
**Next steps:** run randomised ±10% price/payout tests in {{n_pilot_segments}} segments for 4–6 weeks, re-estimate, then expand.
```

## 7. Tests (≥ 10)

| Test | Asserts |
|---|---|
| `test_simulator_is_reproducible` | Same seed → identical log and truth |
| `test_experiment_share` | Share of experiment rows within 0.20 ± 0.02 |
| `test_experiment_prices_are_plus_minus_ten_percent` | In experiment rows `price/p0` ∈ {0.9, 1.1} and `payout/w0` ∈ {0.9, 1.1} |
| `test_log_has_no_truth_columns` | `eps`, `d0`, `alpha`, `beta`, `take0` not in the log or `meta` |
| `test_estimate_module_does_not_import_truth` | Source of `estimate.py` contains no reference to `make_truth` or `truth` |
| `test_elasticity_recovery` | Service-level estimates within ±20% of the mean true ε per service (fixed seed; 120 segments) |
| `test_acceptance_recovery` | `beta_hat` within 25% of 0.018 |
| `test_placebo_estimation_collapses` | After shuffling `ln_p`, `|eps_hat|` is below 1 for every service |
| `test_demand_only_never_changes_payout` | `demand_only_policy` payout equals `w0` |
| `test_two_sided_respects_constraints` | Payout ≥ floor; planned fulfilment ≥ target on feasible segments; price within bounds |
| `test_infeasible_segment_keeps_current_terms` | A crafted infeasible segment returns `p0, w0` |
| `test_evaluate_conserves_flows` | `fulfilled ≤ min(requests, capacity)` everywhere; contribution identity holds |
| `test_policy_ordering_on_holdout` | Two-sided > demand-only > static (fixed seed) |
| `test_placebo_policy_gain_below_real` | Real gain exceeds the 95th percentile of the shuffled-multiplier gains |
| `test_draw_robustness_win_rate` | Win rate ≥ 0.80 (marked slow; use 100 draws in CI) |

## 8. Acceptance checklist

- [ ] Estimated elasticities within ±20% of simulator truth (recovery test).
- [ ] Two-sided > demand-only > static on holdout contribution with fulfilment ≥ 90%.
- [ ] Robustness: % of 400 draws where two-sided wins ≥ 80% (and the stress-test results shown).
- [ ] Placebo tests reported (policy and estimation).
- [ ] README states the simulator is synthetic and the TLC data cannot identify elasticity.
- [ ] Segment explorer app runs; CI green.

## 9. Review slide outlines

**Mid-review (after M3):** 1 Two-sided pricing problem · 2 Why a simulator + what TLC shows (surge confounding) · 3 Simulator design and calibration · 4 Experiments that identify elasticity · 5 Estimation method (FE + shrinkage) · 6 Recovery vs truth · 7 Optimiser and constraints · 8 Three policies · 9 First holdout results · 10 Validation plan.

**Final review (after M5):** 1 Recap · 2 Holdout table · 3 Why demand-only fails · 4 Placebo tests · 5 400-draw robustness and stress tests · 6 Sensitivity to floor, target, take rate · 7 Explorer demo · 8 Limitations · 9 Pilot design · 10 Recommendation.

## 10. Stretch goals and interview talking points

**Stretch:** convex optimisation instead of a grid; time-varying (weekly) pricing; Bayesian elasticity with hierarchical priors; a bandit that keeps experimenting; competitor reaction; fairness constraints on partner earnings by city.

**Likely questions:**
1. *How do you identify elasticity?* — From randomised price experiments; observational data (including the TLC trips) shows price and demand rising together because of surge.
2. *Why two-sided?* — Price changes demand, payout changes supply; optimising one ignores unfulfilled orders and partner churn.
3. *How do you know it is not luck?* — Holdout on the true market, placebo with shuffled recommendations, 400 parameter draws.
4. *What if elasticity were −0.8?* — Revenue-maximising price is unbounded; the optimiser needs `|ε| > 1` and bounds — hence the clip and the price bounds.
5. *What would change with real data?* — Run the randomised tests first; parameters will be noisier; widen the guardrails.

## 11. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| DuckDB `httpfs` install fails | Download the Parquet with `curl -L -o ...` and read the local path |
| TLC read uses too much memory | Select only the six columns; never `pd.read_parquet` the whole file |
| Elasticity estimates biased toward 0 | Using all weeks without relative price; check `ln_p` is zero outside experiments and FE are included |
| Optimiser picks the grid corner everywhere | Elasticity near −1 or constraints too loose; clip ε and check bounds |
| Two-sided loses to static in draws | Estimates too noisy: widen the earnings guardrail or shrink segment estimates harder; report honestly |
| Fulfilment far below 90% for all policies | Capacity ratio too low in the simulator (`cap_ratio_range`) |

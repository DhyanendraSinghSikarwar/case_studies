"""
SYNTHETIC DATA GENERATOR - CASE STUDY 22 (budget-constrained personalised coupon allocation, Meituan Bike style)
==============================================================================================================
THIS DATA IS SYNTHETIC. The company data (200+ features, ~3 million random-traffic users) is confidential.

Documented context (Dai, Li, Zhu, Lin, Huang, arXiv:2406.05987v3, 2024): subscription coupons for a bike-sharing
platform; a random-traffic group (20% of traffic) is used to train a conversion (CVR) model; the model is calibrated
(isotonic regression, PCOC 0.971-0.982, AUC 0.891); coupons are chosen by a Lagrangian-dual argmax with lambda found by
trisection; a PID controller keeps the average offered price near the budget. Reported random-arm CVR in one city: 12.93%.

Simulation (all numbers below are OUR assumptions, calibrated only to the ~13% random-arm CVR):
  * Price ladder (Rs per month): 59, 69, 79, 89, 99. Offered price = price after the coupon.
  * Each user has 12 observed features and two hidden quantities: baseline purchase propensity a(x) and price
    sensitivity beta(x) (partly explained by the features, partly hidden).
  * True CVR(x, p) = sigmoid(a - beta * (p - 79) / 10). Hidden truth columns are prefixed "_".
  * Three populations:  random_traffic (price drawn uniformly, outcome logged = the training data),
                        logged_policy (price set by a targeting rule that favours high-propensity users: confounded data),
                        online (the population used for policy evaluation and the simulated A/B test; carries an arrival hour).
  * Data-quality defects in random_traffic: duplicate rows, missing features, impossible values, invalid price codes.

Outputs: data/cs22/random_traffic.csv.gz, logged_policy.csv.gz, online_features.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.optimize import brentq

SEED = 42
LADDER = np.array([59.0, 69.0, 79.0, 89.0, 99.0]); P_REF = 79.0
N_RANDOM, N_LOGGED, N_ONLINE = 200_000, 80_000, 240_000
FEATS = ["tenure_days", "rides_last30", "rides_last90", "avg_ride_min", "city_tier", "age", "prev_subscriber",
         "days_since_last_ride", "coupons_redeemed_90d", "sessions_7d", "weekend_share", "spend_90d"]
TARGET_CVR = 0.13


def _sig(z):
    return 1 / (1 + np.exp(-z))


def _population(n, rng, intercept=None):
    e = rng.normal(0, 1, n)                                    # engagement (hidden driver of many features)
    tier = rng.choice([1, 2, 3], n, p=[0.35, 0.40, 0.25])
    sens = -0.45 * e + 0.35 * (tier == 3) - 0.25 * (tier == 1) + rng.normal(0, 0.8, n)   # price sensitivity driver
    lam30 = np.exp(1.5 + 0.55 * e)
    r30 = rng.poisson(lam30); r90 = r30 + rng.poisson(2 * lam30)
    df = pd.DataFrame({
        "tenure_days": np.round(rng.lognormal(5.3, 0.9, n)).astype(int),
        "rides_last30": r30, "rides_last90": r90,
        "avg_ride_min": np.round(rng.lognormal(2.4, 0.35, n), 1),
        "city_tier": tier,
        "age": np.clip(np.round(rng.normal(28, 7, n)), 16, 65).astype(int),
        "prev_subscriber": rng.binomial(1, _sig(-0.7 + 0.55 * e)),
        "days_since_last_ride": np.minimum(90, np.round(rng.exponential(6 * np.exp(-0.5 * e)))).astype(int),
        "coupons_redeemed_90d": rng.poisson(np.exp(-0.2 + 0.45 * sens)),
        "sessions_7d": rng.poisson(np.exp(1.3 + 0.5 * e)),
        "weekend_share": np.round(rng.beta(2, 3, n), 3),
        "spend_90d": np.round(r90 * rng.lognormal(np.log(14), 0.3, n) * (1 + 0.1 * (tier == 1)), 0),
    })
    a_raw = 0.55 * e + 0.45 * df.prev_subscriber - 0.03 * df.days_since_last_ride + 0.12 * np.log1p(df.sessions_7d) + rng.normal(0, 0.45, n)
    beta = 0.20 * np.exp(0.60 * (sens + rng.normal(0, 0.35, n)))   # true price sensitivity (hidden), per Rs 10
    return df, a_raw.values, beta


def _cvr(a, beta, price):
    return _sig(a[:, None] - beta[:, None] * (np.asarray(price)[None, :] - P_REF) / 10)


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    parts = {}
    sizes = {"random": N_RANDOM, "logged": N_LOGGED, "online": N_ONLINE}
    raw = {k: _population(n, rng) for k, n in sizes.items()}
    # intercept so that the mean CVR over the uniform ladder in the random population is TARGET_CVR
    a0, b0 = raw["random"][1], raw["random"][2]
    c = brentq(lambda c: _cvr(a0 + c, b0, LADDER).mean() - TARGET_CVR, -6, 6)
    for k, (df, a, beta) in raw.items():
        a = a + c; df = df.copy(); df["user_id"] = np.arange(len(df)) + {"random": 0, "logged": 10_000_000, "online": 20_000_000}[k]
        P = _cvr(a, beta, LADDER)
        for j, p in enumerate(LADDER): df[f"_cvr_{int(p)}"] = P[:, j]
        df["_a"] = a; df["_beta"] = beta
        parts[k] = df
    # random traffic: uniform coupon, logged outcome
    r = parts["random"]; j = rng.integers(0, 5, len(r)); r["offered_price"] = LADDER[j]; pc = r[[f"_cvr_{int(p)}" for p in LADDER]].values[np.arange(len(r)), j]
    r["converted"] = rng.binomial(1, pc)
    # logged policy: confounded targeting. Higher-propensity users are offered HIGHER prices (fewer coupons for people likely to buy anyway)
    l = parts["logged"]; z = np.argsort(np.argsort(l["_a"].values + rng.normal(0, 0.35, len(l)))) / len(l)
    jl = np.minimum(4, (z * 5).astype(int)); l["offered_price"] = LADDER[jl]; pcl = l[[f"_cvr_{int(p)}" for p in LADDER]].values[np.arange(len(l)), jl]; l["converted"] = rng.binomial(1, pcl)
    # online population: arrival hour with a compositional drift (committers ride in commute hours)
    o = parts["online"]; eng = (o["rides_last30"].values - o["rides_last30"].mean()) / o["rides_last30"].std()
    hours = np.arange(24); base = np.array([1, 1, 1, 1, 1.5, 2.5, 4, 6, 6, 4.5, 3.5, 3.5, 4, 4, 3.5, 3.5, 4.5, 6, 6.5, 5, 4, 3, 2, 1.5]); hour = np.zeros(len(o), int)
    commute = np.isin(hours, [6, 7, 8, 9, 17, 18, 19]); w_c = _sig(1.2 * eng); h_commute = rng.random(len(o)) < w_c * 0.7 + 0.15
    pc_, po_ = base * commute, base * ~commute; pc_ = pc_ / pc_.sum(); po_ = po_ / po_.sum()
    hour = np.where(h_commute, rng.choice(24, len(o), p=pc_), rng.choice(24, len(o), p=po_)); o["arrival_hour"] = hour
    # data-quality defects in random_traffic
    dup = r.sample(n=3000, random_state=seed)
    r = pd.concat([r, dup], ignore_index=True)
    for col, frac in (("avg_ride_min", 0.03), ("spend_90d", 0.02), ("days_since_last_ride", 0.015)):
        r.loc[rng.random(len(r)) < frac, col] = np.nan
    bad = rng.random(len(r)) < 0.001; r.loc[bad, "age"] = rng.choice([0, 3, 118, 150], bad.sum())
    bad = rng.random(len(r)) < 0.0008; r.loc[bad, "rides_last30"] = rng.integers(400, 1500, bad.sum())
    bad = rng.random(len(r)) < 0.0015; r.loc[bad, "spend_90d"] = -r.loc[bad, "spend_90d"].abs()
    bad = rng.random(len(r)) < 0.0012; r.loc[bad, "offered_price"] = 0.0
    parts["random"] = r
    return parts, dict(ladder=LADDER, p_ref=P_REF, intercept_shift=c)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, "cs22"); os.makedirs(out, exist_ok=True)
    parts, tp = generate()
    parts["random"].to_csv(os.path.join(out, "random_traffic.csv.gz"), index=False)
    parts["logged"].to_csv(os.path.join(out, "logged_policy.csv.gz"), index=False)
    parts["online"][["user_id", "arrival_hour"] + FEATS].to_csv(os.path.join(out, "online_features.csv.gz"), index=False)
    r = parts["random"]; r = r[r.offered_price > 0]
    print("random CVR", r.converted.mean().round(4), "| by price", r.groupby("offered_price").converted.mean().round(4).to_dict())
    o = parts["online"]; C = o[[f"_cvr_{int(p)}" for p in LADDER]].values; rev = C * LADDER
    print("online mean CVR at uniform ladder", C.mean().round(4), "| revenue per user at uniform random", rev.mean().round(3))
    print("share users whose revenue-max price is 59:", (rev.argmax(1) == 0).mean().round(3), "99:", (rev.argmax(1) == 4).mean().round(3), "| unconstrained avg price", LADDER[rev.argmax(1)].mean().round(2))
    # oracle at avg price >= 79 via Lagrangian bisection
    def alloc(lam): return (rev + lam * LADDER[None, :]).argmax(1)
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if LADDER[alloc(mid)].mean() < 79: lo = mid
        else: hi = mid
    j = alloc(hi); print("oracle lambda", round(hi, 4), "avg price", LADDER[j].mean().round(2), "revenue/user", rev[np.arange(len(o)), j].mean().round(3), "gain vs random", (rev[np.arange(len(o)), j].mean() / rev.mean() - 1).round(4), "CVR", C[np.arange(len(o)), j].mean().round(4))
    print("beta quantiles", np.quantile(o["_beta"], [.05, .25, .5, .75, .95]).round(3))

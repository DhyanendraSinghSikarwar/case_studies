"""
SYNTHETIC DATA GENERATOR - CASE STUDY 19 (A/B testing, interference and switchback experiments)
================================================================================================
THIS DATA IS SYNTHETIC. No company experiment logs are public.

Documented context (reference file, Case 19): Cabify (4 Mar 2026) explains that user-level A/B tests are biased for
marketplace-wide metrics because treated and control users draw on the same driver pool ("cannibalization"); its
switchback design makes the time slot the unit, uses a prime interval (53 minutes; alternatives 58, 112, 29), and
handles carryover with washout periods. Flipkart (CIO India, 2012) routed 10% of traffic to a new design and rolled
back if sales dipped. No lift figures, test statistics or variance estimators are public (ND).

Two simulated worlds:
  1. A user-level A/B test of a homepage redesign on an ecommerce site (120,000 users, 50/50, 14 days, 8 metrics,
     pre-period covariates for CUPED, built-in defects: duplicates, missing values, revenue outliers, and a logging
     outage that causes a sample-ratio mismatch).
  2. A ride-hailing style marketplace at minute level (28 days) with a shared supply pool. A message change raises
     requests by TAU = 6% for treated users. Success probability falls when total demand rises against fixed supply, so
     treated users cannibalise control users. The hidden truth is the effect of a GLOBAL rollout (everyone treated).
     Carryover: the behavioural effect builds up with a 12-minute exponential time constant after a switch.
     Supply has a 120-minute cycle (shift/batching pattern), which a 60-minute alternating design would alias with.
Hidden ground-truth columns / values are prefixed with "_".

Outputs: data/cs19/users_ab.csv.gz, market_switchback.csv.gz, market_userab.csv.gz, truth.json
"""
import json
import os
import numpy as np
import pandas as pd
from scipy.signal import lfilter

SEED = 42
N_USERS = 120_000; EXP_DAYS = 14
DAYS_M = 28; TAU = 0.06; CARRY_TC = 12.0; K_SUCC = 1.8; P_MAX = 0.97


def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


# ------------------------------------------------------------------ world 1: user-level A/B
def generate_users(rng, n=N_USERS):
    new = rng.random(n) < 0.30; plat = np.where(rng.random(n) < 0.62, "app", "web"); tier = rng.choice(["metro", "tier2", "tier3"], n, p=[0.40, 0.35, 0.25])
    z = rng.normal(0, 1, n)                                              # latent engagement
    pre_orders = np.where(new, 0, rng.poisson(1.1 * np.exp(1.3 * z - 0.6)))
    pre_sessions = np.where(new, rng.poisson(1.0, n), rng.poisson(4.0 * np.exp(0.5 * z)))
    pre_spend = np.where(pre_orders > 0, np.round(pre_orders * np.exp(rng.normal(6.4 + 0.2 * z, 0.5)), 0), 0.0)
    day = rng.integers(0, EXP_DAYS, n); arm = (rng.random(n) < 0.5).astype(int)
    # true relative lifts (hidden): conversion +15% for new users, +3% for existing; orders follow; wishlist no effect
    lift = np.where(new, 0.15, 0.03)
    logit0 = -3.4 + 1.4 * z + 0.25 * (plat == "app") - 0.15 * (tier == "tier3")
    p0 = _sigmoid(logit0); p1 = np.clip(p0 * (1 + lift), 0, 0.95); conv = (rng.random(n) < np.where(arm == 1, p1, p0)).astype(int)
    extra = rng.poisson(0.35 * np.exp(0.3 * z)) * conv; orders = conv + extra
    aov = np.exp(rng.normal(6.35, 0.75, n))
    revenue = np.where(orders > 0, orders * aov * np.exp(rng.normal(0, 0.25, n)), 0.0)
    cart = ((rng.random(n) < _sigmoid(-1.5 + 0.6 * z + 0.9 * conv + 0.05 * arm)) | (conv == 1)).astype(int)
    wish = rng.poisson(0.5 * np.exp(0.3 * z), n)
    bounce = (rng.random(n) < _sigmoid(-0.9 - 0.4 * z + 0.0 * arm)).astype(int)
    load = np.round(np.exp(rng.normal(np.log(1900), 0.35, n)) * np.where(plat == "web", 1.25, 1.0) * np.where(arm == 1, 1.012, 1.0), 0)
    support = (rng.random(n) < _sigmoid(-3.6 - 0.2 * z + 0.05 * (arm == 1) + 0.3 * conv)).astype(int)
    df = pd.DataFrame({"user_id": np.arange(n), "arm": arm, "day": day, "platform": plat, "city_tier": tier, "new_user": new.astype(int), "pre_orders_28d": pre_orders,
                       "pre_sessions_28d": pre_sessions, "pre_spend_28d": pre_spend, "converted": conv, "orders": orders, "revenue_inr": np.round(revenue, 0),
                       "add_to_cart": cart, "wishlist_adds": wish, "bounced": bounce, "page_load_ms": load, "support_contact": support,
                       "_true_rel_lift_conv": lift, "_latent_engagement": np.round(z, 3)})
    # defects
    out = rng.choice(n, 25, replace=False); df.loc[out, "revenue_inr"] = np.round(rng.uniform(150_000, 600_000, 25), 0); df.loc[out, "converted"] = 1; df.loc[out, "orders"] = np.maximum(df.loc[out, "orders"], 1)
    df.loc[rng.choice(n, int(0.03 * n), replace=False), "pre_spend_28d"] = np.nan
    df.loc[rng.choice(n, int(0.01 * n), replace=False), "page_load_ms"] = np.nan
    outage = (df.platform == "web") & df.day.isin([5, 6]) & (df.arm == 1) & (rng.random(n) < 0.5)           # logging outage: treated web rows lost on days 5-6
    df = df[~outage]
    df = pd.concat([df, df.sample(n=1500, random_state=SEED)], ignore_index=True).sample(frac=1, random_state=SEED).reset_index(drop=True)
    return df


# ------------------------------------------------------------------ world 2: marketplace with shared supply
def market_paths(rng, days=DAYS_M):
    T = days * 1440; t = np.arange(T); h = (t % 1440) / 60.0; dow = (t // 1440) % 7
    shape = 0.55 + 0.45 * np.exp(-((h - 8.5) / 1.8) ** 2) + 0.60 * np.exp(-((h - 18.5) / 2.2) ** 2)
    weekly = np.where(dow >= 5, 0.90, 1.0)
    ar = lambda phi, sd: lfilter([sd * np.sqrt(1 - phi ** 2)], [1, -phi], rng.normal(0, 1, T))
    lam = 100 * shape * weekly * np.exp(ar(0.99, 0.05))
    sup = 76 * (0.8 + 0.35 * shape) * (1 + 0.10 * np.sin(2 * np.pi * t / 120)) * np.exp(ar(0.995, 0.07))
    return dict(t=t, hour=h, day=t // 1440, lam=lam, sup=sup)


def p_succ(sup, demand):
    return P_MAX * (1 - np.exp(-K_SUCC * sup / np.maximum(demand, 1e-9)))


def ewma(a, tc=CARRY_TC):
    al = np.exp(-1 / tc); return lfilter([1 - al], [1, -al], a, zi=[a[0] * al])[0] if tc > 0 else a


def truth_global(paths):
    """Hidden truth for a GLOBAL rollout: relative lift in completed trips and change in success rate (pp)."""
    d0 = paths["lam"]; d1 = d0 * (1 + TAU); c0 = (d0 * p_succ(paths["sup"], d0)).sum(); c1 = (d1 * p_succ(paths["sup"], d1)).sum()
    return dict(_rel_lift_completed=c1 / c0 - 1, _success_pp=100 * (c1 / d1.sum() - c0 / d0.sum()), _naive_ab_rel_lift=TAU)


def simulate_market(rng, paths, a_raw, tau=TAU):
    """a_raw: per-minute treatment indicator or fraction (0..1). Returns minute-level DataFrame."""
    a = ewma(np.asarray(a_raw, float)); mu = paths["lam"] * (1 + tau * a); req = rng.poisson(mu); p = p_succ(paths["sup"], np.maximum(req, 1)); comp = rng.binomial(req, np.clip(p, 0, 1))
    return pd.DataFrame({"minute": paths["t"], "day": paths["day"], "hour": paths["hour"], "treat": np.asarray(a_raw, float), "requests": req, "completed": comp, "supply": paths["sup"]})


def interval_assignment(rng, T, length, mode):
    """Per-minute 0/1 assignment. mode: 'alternate', 'random', 'block' (paired random order of consecutive intervals)."""
    k = int(np.ceil(T / length)); n = k + (k % 2)
    if mode == "alternate": a = np.arange(n) % 2
    elif mode == "random": a = rng.integers(0, 2, n)
    elif mode == "block": a = np.concatenate([rng.permutation([0, 1]) for _ in range(n // 2)])
    else: raise ValueError(mode)
    return np.repeat(a, length)[:T].astype(float), np.repeat(np.arange(n), length)[:T]


def user_level_market_ab(rng, paths, n_users=50_000):
    arm = (rng.random(n_users) < 0.5).astype(int); rate = rng.gamma(0.9, 3.0 / 0.9, n_users); req = rng.poisson(rate * (1 + TAU * arm))
    m = simulate_market(rng, paths, np.full(len(paths["t"]), 0.5)); p_bar = m.completed.sum() / m.requests.sum(); comp = rng.binomial(req, p_bar)
    return pd.DataFrame({"user_id": np.arange(n_users), "arm": arm, "requests": req, "completed": comp}), p_bar


def generate(seed=SEED):
    ss = np.random.SeedSequence(seed).spawn(4); r1, r2, r3, r4 = [np.random.default_rng(s) for s in ss]
    users = generate_users(r1)
    paths = market_paths(r2); T = len(paths["t"]); a_raw, interval = interval_assignment(r3, T, 53, "block")
    sb = simulate_market(r3, paths, a_raw); sb["interval"] = interval
    sb.loc[sb.sample(frac=0.002, random_state=seed).index, ["requests", "completed"]] = np.nan                      # missing minutes
    sb.loc[sb.sample(n=15, random_state=seed + 1).index, "supply"] *= 4                                         # sensor spikes
    sb = pd.concat([sb, sb.sample(n=300, random_state=seed)], ignore_index=True).sort_values("minute", kind="stable").reset_index(drop=True)
    uab, p_bar = user_level_market_ab(r4, paths)
    tr = truth_global(paths); tr["_ab_success_rate"] = p_bar
    return users, sb, uab, tr, paths


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, "cs19"); os.makedirs(out, exist_ok=True)
    users, sb, uab, tr, _ = generate()
    users.to_csv(os.path.join(out, "users_ab.csv.gz"), index=False); sb.to_csv(os.path.join(out, "market_switchback.csv.gz"), index=False); uab.to_csv(os.path.join(out, "market_userab.csv.gz"), index=False)
    json.dump({k: float(v) for k, v in tr.items()}, open(os.path.join(out, "truth.json"), "w"))
    u = users.drop_duplicates("user_id")
    print(len(users), "user rows |", len(u), "unique | treated share", round(u.arm.mean(), 4), "| conv", round(u.converted.mean(), 4), "| corr(pre_spend, revenue)", round(u[["pre_spend_28d", "revenue_inr"]].corr().iloc[0, 1], 3))
    print("conv by arm", u.groupby("arm").converted.mean().round(4).to_dict(), "| rev by arm", u.groupby("arm").revenue_inr.mean().round(1).to_dict())
    print("truth", {k: round(v, 4) for k, v in tr.items()})
    ab = uab.groupby("arm").agg(req=("requests", "mean"), comp=("completed", "mean")); print(ab, "naive ratio", ab.comp[1] / ab.comp[0])
    m = sb.dropna(subset=["requests"]); print("market: success rate", round(m.completed.sum() / m.requests.sum(), 3), "| mean requests/min", round(m.requests.mean(), 1))

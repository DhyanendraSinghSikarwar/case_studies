"""
SYNTHETIC DATA GENERATOR - CASE STUDY 21 (paid food-delivery membership: Zomato Gold style)
===========================================================================================
THIS DATA IS SYNTHETIC. Customer order histories and membership data are confidential, and no public method is
documented for how Zomato or Flipkart measured their programmes.

Documented context only (see the reference file): Zomato relaunched Gold in January 2023 at Rs 149 for three months
(introductory price), with free delivery within 10 km or above Rs 199 and on-time-guarantee coupons; over nine lakh
members within a month of relaunch (company-reported via press). Everything else below is our assumption.

Simulation: 40,000 customers x 24 months. The programme launches in month 12.
  * Each customer has a base order rate, a hidden momentum term u (a customer whose eating-out/ordering is growing),
    a fee-sensitivity feature and a hidden true treatment effect tau (log-rate lift from membership).
  * Customers choose to join: the probability rises with RECENT realised orders, recent growth, fee sensitivity,
    coupon use and the hidden momentum u. That is self-selection on levels, on trend and on something unobserved.
  * Members order more (log-rate lift tau, about +11 percent on average), lapse less, but each member order costs a
    delivery subsidy, and the member pays Rs 149 per three months.
  * A randomised pilot: half of the customers got a one-month free-trial invitation at launch (offer = 1), which
    raises the chance of joining in month 12 only.
Hidden truth (columns starting with an underscore): counterfactual orders and contribution if nobody joined (computed
with common random numbers), the hidden momentum u and the true effect tau. They are used only to grade the estimators.

Outputs: data/cs21/panel.csv.gz (customer-month), data/cs21/customers.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import poisson

SEED = 42
N, T, L = 40_000, 24, 12
FEE_PER_MONTH = 149 / 3
MARGIN_RATE = 0.13


def _sig(x):
    return 1 / (1 + np.exp(-x))


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    tier = rng.choice([1, 2, 3], N, p=[0.45, 0.35, 0.20])
    za = rng.normal(0, 1, N)
    a = np.log(2.0) + 0.65 * za + 0.15 * (tier == 1)
    aov = np.exp(rng.normal(np.log(400), 0.30, N) + 0.10 * (tier == 1))
    fee = np.clip(rng.beta(2, 3, N), 0, 1)
    coupon = np.clip(rng.beta(2, 5, N) + 0.05 * fee, 0, 1)
    tenure = np.round(rng.exponential(14, N) + 1).astype(int)
    u = rng.normal(0, 1, N)
    g = 0.22 * u
    offer = (rng.random(N) < 0.5).astype(int)
    tau = np.clip(0.11 + 0.05 * (fee - 0.4) / 0.2 - 0.03 * za + rng.normal(0, 0.03, N), -0.02, 0.40)
    subsidy = 18 + 25 * fee
    margin = MARGIN_RATE * aov
    season = 0.08 * np.sin(2 * np.pi * np.arange(T) / 12)
    Ul, Up = rng.random((N, T)), rng.random((N, T))
    Ug = rng.lognormal(0, 0.10, (N, T))

    orders = np.zeros((N, T), int); cf = np.zeros((N, T), int); mem = np.zeros((N, T), int)
    act = np.ones(N, bool); act_cf = np.ones(N, bool); member = np.zeros(N, bool); join = np.full(N, -1)
    hist_log = np.zeros((N, T))
    for t in range(T):
        lr = a + g * (t - 11) / 12 + season[t]
        haz0 = _sig(-3.9 - 0.45 * za - 0.30 * u)
        mu = np.exp(lr + tau * member)
        haz = _sig(-3.9 - 0.45 * za - 0.30 * u - 0.40 * member)
        act = act & (Ul[:, t] > haz); act_cf = act_cf & (Ul[:, t] > haz0)
        orders[:, t] = np.where(act, poisson.ppf(Up[:, t], mu), 0)
        cf[:, t] = np.where(act_cf, poisson.ppf(Up[:, t], np.exp(lr)), 0)
        mem[:, t] = member
        hist_log[:, t] = np.log1p(orders[:, t])
        # joining happens at the start of month t+1 (t >= L-1): uses realised history through t
        if t >= L - 1 and t < T - 1:
            recent = hist_log[:, max(0, t - 2):t + 1].mean(1); prior = hist_log[:, max(0, t - 5):max(1, t - 2)].mean(1)
            z_recent = (recent - 1.0) / 0.7; growth = (recent - prior) / 0.4
            first = (t == L - 1)
            logit = (-3.5 if not first else -2.4) + 0.45 * z_recent + 0.55 * growth + 0.45 * u + 0.30 * (tier == 1) \
                + 0.9 * (fee - 0.4) / 0.2 * 0.25 + 0.6 * (coupon - 0.3) / 0.15 * 0.25 + (1.8 * offer if first else 0.0)
            p = _sig(logit) * act * (~member)
            new = rng.random(N) < p
            join[new] = t + 1; member = member | new
    mu_gov = Ug * aov[:, None] * (1 + 0.03 * mem)
    gov = np.round(orders * mu_gov, 0)
    sub = orders * mem * subsidy[:, None]
    contrib = orders * margin[:, None] - sub + mem * FEE_PER_MONTH
    contrib_cf = cf * margin[:, None]
    cid = np.repeat(np.arange(N), T); mo = np.tile(np.arange(T), N)
    panel = pd.DataFrame({"customer_id": cid, "month": mo, "orders": orders.ravel(), "gov_inr": gov.ravel(), "member": mem.ravel(),
                          "delivery_subsidy_inr": np.round(sub.ravel(), 1), "contribution_inr": np.round(contrib.ravel(), 1),
                          "_orders_cf": cf.ravel(), "_contribution_cf": np.round(contrib_cf.ravel(), 1)})
    cust = pd.DataFrame({"customer_id": np.arange(N), "city_tier": tier, "fee_paid_share": np.round(fee, 3), "coupon_share": np.round(coupon, 3),
                         "tenure_months": tenure, "offer": offer, "join_month": np.where(join >= 0, join, np.nan),
                         "_u": np.round(u, 3), "_tau": np.round(tau, 4), "_subsidy_per_order": np.round(subsidy, 1), "_margin_per_order": np.round(margin, 1)})
    # messy-data defects
    dup = panel.sample(n=1500, random_state=seed)
    cust.loc[cust.sample(frac=0.05, random_state=seed).index, "city_tier"] = np.nan
    staff = pd.DataFrame({"customer_id": np.repeat(np.arange(N, N + 25), T), "month": np.tile(np.arange(T), 25)})
    staff["orders"] = rng.integers(60, 140, len(staff)); staff["gov_inr"] = staff.orders * 380.0; staff["member"] = (staff.month >= L).astype(int)
    staff["delivery_subsidy_inr"] = 0.0; staff["contribution_inr"] = 0.0; staff["_orders_cf"] = staff.orders; staff["_contribution_cf"] = 0.0
    panel = pd.concat([panel, dup, staff], ignore_index=True).sort_values(["customer_id", "month"]).reset_index(drop=True)
    return panel, cust


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs21"), exist_ok=True)
    p, c = generate(); p.to_csv(os.path.join(here, "cs21", "panel.csv.gz"), index=False); c.to_csv(os.path.join(here, "cs21", "customers.csv.gz"), index=False)
    print(len(p), len(c), c.join_month.value_counts().sort_index().to_dict())

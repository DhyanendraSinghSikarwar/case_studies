"""
SYNTHETIC DATA GENERATOR - CASE STUDY 21 (Paytm Labs-style Bayesian trend filtering for homepage personalisation)
=================================================================================================================
THIS DATA IS SYNTHETIC. Super-app click logs are confidential.

50,000 users click service categories on the homepage over 8 weeks. Each user has a stable personal
AFFINITY over 12 categories; platform-wide TRENDS move category popularity (a blockbuster weekend lifts
movie tickets, Diwali lifts flights and trains, Dhanteras lifts digital gold, a FASTag mandate lifts FASTag).
Users differ in how much they follow trends (responsiveness r in [0, 1]).
On a visit, P(click category c) is proportional to affinity_u(c) * trend_c(day) ** r_u.
Activity is heavy-tailed: many users visit rarely (cold start), a few visit daily.

Calibration anchors (reference file, Case Study 21): "hundreds of service icons and banners for 400M+ users";
category-level Bayesian update p_next(c|click) = p(c|click) * p_next(c) / p(c); no A/B results disclosed.
Rates are our assumptions (decision.md D-21-02). The generator also exports the TRUE click probabilities
(`true_probs`) for a digital-twin A/B.

Outputs: data/cs21/daily_clicks.csv.gz (user, day, category, clicks), data/cs21/users_hidden.csv.gz, data/cs21/trend_hidden.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
CATS = ["mobile_recharge", "electricity_bill", "dth", "movie_tickets", "flights", "train_tickets", "bus_tickets", "digital_gold", "insurance", "loans", "gift_vouchers", "fastag"]
BASE = np.array([0.24, 0.16, 0.08, 0.07, 0.05, 0.08, 0.05, 0.04, 0.04, 0.04, 0.06, 0.09])
DAYS = 56


def trend_matrix():
    t = np.ones((DAYS, len(CATS)))
    d = np.arange(DAYS)
    t[:, 3] *= 1 + 2.5 * ((d >= 28) & (d <= 34)) + 1.2 * ((d >= 48) & (d <= 50))        # blockbuster weekends
    t[:, 4] *= 1 + 2.0 * np.clip((d - 38) / 6, 0, 1) * (d <= 50)                            # Diwali travel build-up
    t[:, 5] *= 1 + 1.6 * np.clip((d - 36) / 8, 0, 1) * (d <= 50)
    t[:, 7] *= 1 + 4.0 * ((d >= 44) & (d <= 46))                                            # Dhanteras gold spike
    t[:, 10] *= 1 + 1.5 * ((d >= 45) & (d <= 49))                                           # Diwali gifting
    t[:, 11] *= 1 + 0.02 * d                                                                # steady FASTag growth
    t[:, 1] *= 1 + 0.35 * ((d % 30) < 5)                                                    # bill-pay cycle at month start
    return t


def true_probs(aff, r, day, T=None):
    T = trend_matrix() if T is None else T
    w = aff * T[day][None, :] ** r[:, None]; return w / w.sum(1, keepdims=True)


def generate(seed=SEED, n=50_000):
    rng = np.random.default_rng(seed)
    conc = rng.gamma(1.0, 1.0, n) + 0.3                                                       # how concentrated a user's tastes are
    aff = np.vstack([rng.dirichlet(BASE * 12 / c) for c in conc])
    r = rng.beta(2, 2, n)                                                                   # trend responsiveness
    lam = rng.lognormal(np.log(0.25), 1.1, n).clip(0.01, 3)                                 # visits per day
    T = trend_matrix(); rows = []
    for day in range(DAYS):
        visits = rng.poisson(lam * (1 + 0.3 * (day % 7 >= 5)))                             # weekends busier
        act = np.flatnonzero(visits > 0)
        if len(act) == 0: continue
        P = true_probs(aff[act], r[act], day, T)
        for k in range(visits[act].max()):
            sub = act[visits[act] > k]; Ps = P[np.isin(act, sub)]
            u = rng.random(len(sub))[:, None]; c = (Ps.cumsum(1) < u).sum(1).clip(0, len(CATS) - 1)
            rows.append(np.c_[sub, np.full(len(sub), day), c])
    ev = pd.DataFrame(np.vstack(rows), columns=["user_idx", "day", "cat_idx"])
    clicks = ev.groupby(["user_idx", "day", "cat_idx"]).size().rename("clicks").reset_index()
    clicks["user_id"] = "U" + clicks.user_idx.astype(str).str.zfill(6); clicks["category"] = np.array(CATS)[clicks.cat_idx]
    users = pd.DataFrame({"user_idx": np.arange(n), "_r": r, "_lam": lam}).join(pd.DataFrame(aff, columns=[f"_aff_{c}" for c in CATS]))
    trend = pd.DataFrame(T, columns=CATS); trend.insert(0, "day", np.arange(DAYS))
    # data-quality defects: bot user with absurd clicks; duplicated log rows; a logging outage on day 20 (half the events lost)
    bot = pd.DataFrame({"user_idx": n, "day": np.repeat(np.arange(DAYS), len(CATS)), "cat_idx": np.tile(np.arange(len(CATS)), DAYS), "clicks": 400})
    bot["user_id"] = "U_BOT01"; bot["category"] = np.array(CATS)[bot.cat_idx]
    out = clicks[["user_id", "user_idx", "day", "category", "cat_idx", "clicks"]]
    drop = out[(out.day == 20)].sample(frac=0.5, random_state=seed).index
    out = pd.concat([out.drop(drop), bot[out.columns], out.sample(n=3000, random_state=seed + 1)], ignore_index=True)
    return out, users, trend


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs21"), exist_ok=True)
    c, u, t = generate(); c.to_csv(os.path.join(here, "cs21", "daily_clicks.csv.gz"), index=False)
    u.to_csv(os.path.join(here, "cs21", "users_hidden.csv.gz"), index=False); t.to_csv(os.path.join(here, "cs21", "trend_hidden.csv.gz"), index=False)
    print(len(c), "rows |", c.clicks.sum(), "clicks |", c.user_id.nunique(), "users")
    print(c[c.user_id != "U_BOT01"].groupby("category").clicks.sum().sort_values(ascending=False).to_dict())

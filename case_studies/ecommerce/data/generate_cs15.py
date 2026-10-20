"""
SYNTHETIC DATA GENERATOR - CASE STUDY 15 (Amazon-style item-to-item collaborative filtering)
===========================================================================================
THIS DATA IS SYNTHETIC. Marketplace purchase logs are confidential.

Documented context (Linden, Smith & York, IEEE Internet Computing 2003): >29 million customers, several million
items, very sparse customer-item vectors, item-to-item similarity computed offline and looked up online, works
"from as few as two or three items". Prior CF was tested on MovieLens-size data (35,000 customers, 3,000 items).

Simulation: 15,000 customers x 2,500 items in 25 categories over 180 days.
  * Taste: each customer has a 12-dim latent taste vector, each item a latent vector near its category centre.
  * Popularity: a long-tailed item popularity term (a few best-sellers; most items rarely bought).
  * Complements: 120 "accessory" pairs (phone -> case) bought within a week with probability 0.18.
  * Purchases per customer ~ negative binomial (mean 11), so many customers have only 2-4 purchases (cold start).
Hidden truth for a DIGITAL-TWIN online test: true click probability = sigmoid(taste affinity + popularity effect).

Outputs: data/cs15/purchases.csv.gz, data/cs15/items.csv.gz, data/cs15/true_params.npz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
START = pd.Timestamp("2026-01-01"); DAYS = 180
N_U, N_I, N_CAT, K = 15_000, 2_500, 25, 12


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    cat = rng.integers(0, N_CAT, N_I); centre = rng.normal(0, 1.0, (N_CAT, K))
    V = centre[cat] + rng.normal(0, 0.45, (N_I, K)); pop = rng.pareto(1.3, N_I) + 1; logpop = np.log(pop); logpop = (logpop - logpop.mean()) / logpop.std()
    U = np.zeros((N_U, K)); fav = rng.integers(0, N_CAT, (N_U, 2)); U = 0.75 * centre[fav[:, 0]] + 0.45 * centre[fav[:, 1]] + rng.normal(0, 0.55, (N_U, K))
    n_p = np.maximum(1, rng.negative_binomial(2.2, 2.2 / (2.2 + 11), N_U)); n_p = np.minimum(n_p, 80)
    acc_src = rng.choice(N_I, 120, replace=False); acc_dst = rng.choice(N_I, 120, replace=False)
    rows = []; ratio = 0.9
    for lo in range(0, N_U, 1500):
        hi = min(N_U, lo + 1500); S = 1.1 * (U[lo:hi] @ V.T) / np.sqrt(K) + ratio * logpop[None, :]; S -= S.max(1, keepdims=True); P = np.exp(S); P /= P.sum(1, keepdims=True)
        for k, u in enumerate(range(lo, hi)):
            items = rng.choice(N_I, size=n_p[u], replace=False, p=P[k]); times = np.sort(rng.integers(0, DAYS, n_p[u]))
            for it, t in zip(items, times): rows.append((u, it, t, 0))
    df = pd.DataFrame(rows, columns=["user", "item", "day", "complement"])
    # complement purchases: after buying an accessory source, buy its partner within a week with probability 0.18
    m = dict(zip(acc_src, acc_dst)); add = []
    for u, it, t in zip(df.user.values, df.item.values, df.day.values):
        if it in m and rng.random() < 0.18: add.append((u, m[it], min(DAYS - 1, t + rng.integers(0, 7)), 1))
    df = pd.concat([df, pd.DataFrame(add, columns=df.columns)], ignore_index=True).drop_duplicates(["user", "item"]).sort_values(["user", "day"]).reset_index(drop=True)
    df["order_ts"] = START + pd.to_timedelta(df.day, unit="D") + pd.to_timedelta(rng.integers(8 * 3600, 23 * 3600, len(df)), unit="s")
    items = pd.DataFrame({"item": np.arange(N_I), "category": cat, "list_price_inr": np.round(np.exp(rng.normal(np.log(700), 1.0, N_I)), 0), "_log_pop_z": logpop})
    # data-quality defects
    dup = df.sample(n=4000, random_state=seed); bots = pd.DataFrame({"user": N_U, "item": rng.choice(N_I, 800, replace=False), "day": rng.integers(0, DAYS, 800), "complement": 0}); bots["order_ts"] = START + pd.to_timedelta(bots.day, unit="D")
    df = pd.concat([df, dup, bots], ignore_index=True)
    return df, items, dict(U=U, V=V, logpop=logpop, acc_src=acc_src, acc_dst=acc_dst, ratio=ratio)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs15"), exist_ok=True)
    d, it, tp = generate(); d.to_csv(os.path.join(here, "cs15", "purchases.csv.gz"), index=False); it.to_csv(os.path.join(here, "cs15", "items.csv.gz"), index=False); np.savez(os.path.join(here, "cs15", "true_params.npz"), **tp)
    dd = d.drop_duplicates(["user", "item"]); c = dd.groupby("user").size(); print(len(dd), "interactions |", c.describe()[["mean", "50%", "max"]].round(1).to_dict(), "| density", round(len(dd) / (N_U * N_I), 5), "| users with <=3", (c <= 3).mean().round(3))
    print("top-1% items share of purchases", dd.item.value_counts().head(25).sum() / len(dd))

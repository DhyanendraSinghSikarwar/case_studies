"""
SYNTHETIC DATA GENERATOR - CASE STUDY 27 (Flipkart-style rating-fraud detection, BIRDNEST)
=========================================================================================
THIS DATA IS SYNTHETIC. Marketplace ratings with fraud labels are confidential.

Documented context (arXiv:1511.06030, Hooi, Shah, Beutel, Gunnemann, Akoglu, Kumar, Makhija, Faloutsos):
Flipkart data had 1.1M users, 550K products, 3.3M ratings (about 3 ratings per user); features per user are the
count of each star level and counts of log-bucketed gaps between consecutive ratings; Flipkart domain experts found
users "spamming 4/5 star ratings to multiple products from a single seller (boosting seller's ratings), or spamming
1/2 star ratings to multiple products from another seller (defaming the competition)".

Simulation (80,000 users, 30,000 products, 1,500 sellers, 365 days, about 3 ratings per user):
  * Honest users: per-user star distribution ~ Dirichlet around a J-shaped global mix; timestamps come in sessions.
      - 2% "enthusiasts" (many ratings, mostly 5 stars, genuine)  -> false-positive trap for the rating signal
      - 6% "batch raters" (rate everything in one sitting, genuine) -> false-positive trap for the time signal
  * Fraud accounts (1.3%), five behaviours:
      boost       4/5 stars to many products of ONE seller, in bursts
      defame      1/2 stars to many products of a competitor seller, in bursts
      burst_only  honest-looking star mix, but rated in bursts (paid reviewers)
      skew_only   5-star spam spread over time (slow drip, no burst)
      stealth     only 2-4 ratings, boost style, in a burst (very little evidence)
Hidden truth: users_truth._is_fraud, ._fraud_type, ._style; ratings._fake.

Outputs: data/cs27/ratings.csv.gz, products.csv.gz, users_truth.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
START = pd.Timestamp("2025-04-01"); DAYS = 365; WIN = DAYS * 86400
N_U, N_P, N_S = 80_000, 30_000, 1_500
FRAUD_RATE = 0.013
BASE = np.array([0.08, 0.06, 0.10, 0.24, 0.52])          # global star mix (assumed J shape)
FTYPES = ["boost", "defame", "burst_only", "skew_only", "stealth"]; FPROB = [0.40, 0.20, 0.16, 0.14, 0.10]


def _times(rng, n, kind, b=0.3):
    """Timestamps (seconds from window start) for one user. kind: 'normal', 'batch', 'burst', 'drip'."""
    if kind == "batch":
        t0 = rng.uniform(0, WIN - 86400); return np.sort(t0 + np.cumsum(np.r_[0, rng.lognormal(7.0, 1.3, n - 1)]))
    if kind == "burst":
        ns = min(n, rng.integers(1, 4)); starts = rng.uniform(0, WIN - 86400, ns); lab = rng.integers(0, ns, n)
        return np.sort(starts[lab] + np.cumsum(rng.lognormal(5.0, 1.3, n)) * (np.arange(n) > 0))
    if kind == "drip":
        return np.sort(rng.uniform(0, WIN, n))
    g = np.where(rng.random(n - 1) < b, rng.lognormal(7.0, 1.3, n - 1), rng.lognormal(13.5, 1.2, n - 1))
    return np.sort((rng.uniform(0, WIN) + np.r_[0, np.cumsum(g)]) % WIN)       # a gap running past the window wraps around


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    # catalogue: products -> sellers (Pareto-sized sellers), long-tailed product popularity
    sw = rng.pareto(1.6, N_S) + 1; seller_of = rng.choice(N_S, N_P, p=sw / sw.sum()); popw = rng.pareto(1.2, N_P) + 1; popw /= popw.sum()
    by_seller = [np.where(seller_of == s)[0] for s in range(N_S)]; big = np.array([s for s in range(N_S) if len(by_seller[s]) >= 8])
    boost_targets = rng.choice(big, 150, replace=False); defame_targets = rng.choice(np.setdiff1d(big, boost_targets), 100, replace=False)
    # users
    is_fraud = rng.random(N_U) < FRAUD_RATE; ftype = np.where(is_fraud, rng.choice(FTYPES, N_U, p=FPROB), "")
    style = np.where(is_fraud, "fraud", np.where(rng.random(N_U) < 0.02, "enthusiast", np.where(rng.random(N_U) < 0.0612, "batch", "normal")))
    n_h = 1 + rng.negative_binomial(1.2, 1.2 / (1.2 + 2.0), N_U); n_h = np.minimum(n_h, 40)
    n_h = np.where(style == "enthusiast", np.minimum(60, 6 + rng.negative_binomial(2, 0.2, N_U)), n_h)
    n_h = np.where(style == "batch", np.maximum(n_h, 2), n_h)
    users, prods, stars, ts, fake = [], [], [], [], []
    # --- honest users: products drawn in one vectorised call
    hon = np.where(~is_fraud)[0]; tot = int(n_h[hon].sum()); hp = rng.choice(N_P, tot, p=popw); off = 0
    theta = rng.dirichlet(7 * BASE, N_U); ent = np.where(style == "enthusiast")[0]; theta[ent] = rng.dirichlet([0.3, 0.3, 0.5, 1.5, 10.0], len(ent))
    bu = rng.beta(2, 5, N_U)
    for u in hon:
        n = int(n_h[u]); kind = "batch" if style[u] == "batch" else "normal"
        t = _times(rng, n, kind, bu[u]); s = (rng.random(n)[:, None] > np.cumsum(theta[u])[:4]).sum(1) + 1
        users.append(np.full(n, u)); prods.append(hp[off:off + n]); stars.append(s); ts.append(t); fake.append(np.zeros(n, bool)); off += n
    # --- fraud accounts
    for u in np.where(is_fraud)[0]:
        ft = ftype[u]; n = int(rng.integers(2, 5)) if ft == "stealth" else int(np.clip(5 + rng.negative_binomial(3, 0.2), 5, 45))
        if ft in ("boost", "stealth"): tgt = rng.choice(boost_targets); pool = by_seller[tgt]
        elif ft == "defame": tgt = rng.choice(defame_targets); pool = by_seller[tgt]
        else: tgt = None; pool = None
        if pool is not None:
            n = min(n, len(pool)); pr = rng.choice(pool, n, replace=False)
        else:
            pr = rng.choice(N_P, n, p=popw)
        if ft in ("boost", "stealth", "skew_only"): s = np.where(rng.random(n) < 0.8, 5, 4)
        elif ft == "defame": s = np.where(rng.random(n) < 0.75, 1, 2)
        else: s = rng.choice(5, n, p=rng.dirichlet(7 * BASE)) + 1
        kind = "drip" if ft == "skew_only" else "burst"
        users.append(np.full(n, u)); prods.append(pr); stars.append(s); ts.append(_times(rng, n, kind)); fake.append(np.ones(n, bool))
    df = pd.DataFrame({"user": np.concatenate(users), "product": np.concatenate(prods), "stars": np.concatenate(stars), "_ts": np.concatenate(ts), "_fake": np.concatenate(fake)})
    df["seller"] = seller_of[df["product"].values]; df["ts"] = START + pd.to_timedelta(df["_ts"].astype(int), unit="s"); df = df.drop(columns="_ts")
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True); df.insert(0, "rating_id", np.arange(len(df)))
    # --- data-quality defects (documented-style messiness)
    dup = df.sample(n=1500, random_state=seed); df = pd.concat([df, dup], ignore_index=True)
    bad = rng.choice(len(df), 60, replace=False); df.loc[bad, "stars"] = rng.choice([0, 6], 60)
    miss = rng.choice(len(df), 80, replace=False); df.loc[miss, "ts"] = pd.NaT
    prod_df = pd.DataFrame({"product": np.arange(N_P), "seller": seller_of})
    truth = pd.DataFrame({"user": np.arange(N_U), "_is_fraud": is_fraud, "_fraud_type": ftype, "_style": style})
    return df[["rating_id", "user", "product", "seller", "stars", "ts", "_fake"]], prod_df, truth


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs27"), exist_ok=True)
    d, p, t = generate(); d.to_csv(os.path.join(here, "cs27", "ratings.csv.gz"), index=False); p.to_csv(os.path.join(here, "cs27", "products.csv.gz"), index=False)
    t.to_csv(os.path.join(here, "cs27", "users_truth.csv.gz"), index=False)
    print(len(d), "ratings |", d.user.nunique(), "users |", "fraud users", int(t._is_fraud.sum()), "| fake ratings", int(d._fake.sum()))

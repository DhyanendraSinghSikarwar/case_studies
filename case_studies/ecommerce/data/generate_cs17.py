"""
SYNTHETIC DATA GENERATOR - CASE STUDY 17 (Flipkart-style unified ranking of sponsored and organic products)
===========================================================================================================
THIS DATA IS SYNTHETIC. Flipkart's impression logs, bids and models are confidential, and the company has not disclosed
the exact scoring formula or auction mechanism.

Documented context (Flipkart Tech blog, 4 Nov 2025, "The Science of Unified Ranking"): the "Similar Products" widget pinned
sponsored items at fixed slots 2 and 5; organic feedback is "multi-fold" larger than ads feedback; one training set with an
isAds flag plus crosses of key features with isAds; separate CTR and CVR models; a circuit breaker back to pinned slots; a
default score of 0.5 as a failure mode; an online A/B with cumulative exposures above 100 million.

Simulation (a calibrated stand-in, NOT Flipkart's data):
  * A request = a viewer on a product page with 12 organic and 4 sponsored candidates. The request has a category type
    (0 = high ad relevance such as electronics, 1 = neutral, 2 = low ad relevance such as low-consideration accessories).
  * Hidden affinity drives clicks and conversions; the model sees only noisy proxies (relevance score, co-browse strength),
    popularity, price ratio, rating, category type and (for ads) the bid in rupees per click.
  * Click probability = slot examination (position bias) x sigmoid(attribute logit). Ads have a lower base rate and a weaker
    relevance dependence than organic items, so the two populations have different base rates and different slopes.
  * Logging policy: 6 organic items (legacy relevance order) with 2 ads pinned at slots 2 and 5 (so 75% of logged impressions
    are organic), except for a 20% random-slotting exploration bucket (our assumption, so every candidate type gets coverage).
  * Click -> order with a conversion probability that differs for ads and organic.
Hidden truth columns are prefixed "_": _aff, _p_ctr_attr (position-free CTR), _p_cvr.
Built-in data defects: duplicate impression rows, missing ratings, impossible bids, orders recorded without a click.

Outputs: data/cs17/impressions.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
K = 8                                             # slots shown
N_ORG, N_ADS = 12, 4
EXAM = np.array([1.0, 0.72, 0.55, 0.43, 0.35, 0.28, 0.23, 0.19])
PIN = (1, 4)                                      # 0-based slots 2 and 5
N_REQ, DAYS, EXPLORE = 80_000, 14, 0.20
B = dict(org_int=-3.65, org_aff=1.05, org_pop=0.30, org_pr=-0.55, org_rat=0.40, ad_int=-3.35, ad_aff=0.65, ad_pop=0.12, ad_pr=-0.25, ad_rat=0.20, ad_bid=0.08,
         cv_org_int=-3.20, cv_org_aff=0.45, cv_org_rat=0.30, cv_ad_int=-3.10, cv_ad_aff=0.30, cv_ad_rat=0.15)


def sigmoid(z): return 1 / (1 + np.exp(-z))


def make_candidates(n_req, rng, req0=0):
    """Candidate sets: n_req x (12 organic + 4 sponsored) with observed features and hidden truth."""
    n = N_ORG + N_ADS; req = np.repeat(np.arange(req0, req0 + n_req), n); is_ads = np.tile(np.r_[np.zeros(N_ORG, int), np.ones(N_ADS, int)], n_req)
    cat_r = rng.choice(3, n_req, p=[0.25, 0.50, 0.25]); cat = np.repeat(cat_r, n); shift = np.array([0.7, 0.0, -1.1])[cat]
    aff = np.where(is_ads == 1, -0.35 + shift, 0.40) + rng.normal(0, 1.0, len(req))
    x_rel = aff + rng.normal(0, 0.55, len(req)); cobrowse = np.clip(0.8 * aff + rng.normal(0, 0.8, len(req)), -3, 3)
    pop = rng.normal(0, 1, len(req)); lpr = rng.normal(0, 0.5, len(req)) + 0.25 * is_ads; rating = np.clip(rng.normal(4.1, 0.4, len(req)) - 0.08 * is_ads, 1.0, 5.0)
    bid = np.where(is_ads == 1, np.exp(rng.normal(np.log(3.0), 0.5, len(req)) + 0.35 * lpr), 0.0)
    rz = (rating - 4.1) / 0.4
    z_org = B["org_int"] + B["org_aff"] * aff + B["org_pop"] * pop + B["org_pr"] * np.abs(lpr) + B["org_rat"] * rz * 0.5
    z_ad = B["ad_int"] + B["ad_aff"] * aff + B["ad_pop"] * pop + B["ad_pr"] * np.abs(lpr) + B["ad_rat"] * rz * 0.5 + B["ad_bid"] * np.log(np.maximum(bid, 0.01))
    p_attr = sigmoid(np.where(is_ads == 1, z_ad, z_org))
    cv = sigmoid(np.where(is_ads == 1, B["cv_ad_int"] + B["cv_ad_aff"] * aff + B["cv_ad_rat"] * rz, B["cv_org_int"] + B["cv_org_aff"] * aff + B["cv_org_rat"] * rz))
    return pd.DataFrame({"request_id": req, "cand": np.tile(np.arange(n), n_req), "is_ads": is_ads, "cat": cat, "x_rel": np.round(x_rel, 3), "cobrowse": np.round(cobrowse, 3), "pop": np.round(pop, 3),
                         "log_price_ratio": np.round(lpr, 3), "rating": np.round(rating, 2), "bid": np.round(bid, 2), "_aff": aff, "_p_ctr_attr": p_attr, "_p_cvr": cv})


def legacy_slate(c, rng):
    """Legacy pinned policy: organics by noisy relevance, ads ranked by bid x relevance proxy and pinned at slots 2 and 5. Returns (n_req, 8) candidate indices (0-11 organic, 12-15 ads)."""
    n_req = len(c) // (N_ORG + N_ADS); n = N_ORG + N_ADS
    org = c[c.is_ads == 0]; ads = c[c.is_ads == 1]
    so = (org.x_rel.values + 0.3 * org["pop"].values + rng.normal(0, 0.35, len(org))).reshape(n_req, N_ORG)
    sa = (ads.bid.values * sigmoid(ads.x_rel.values + rng.normal(0, 0.35, len(ads)))).reshape(n_req, N_ADS)
    oi = np.argsort(-so, axis=1)[:, :K - 2]; ai = np.argsort(-sa, axis=1)[:, :2] + N_ORG
    slate = np.zeros((n_req, K), int); org_slots = [s for s in range(K) if s not in PIN]
    for j, s in enumerate(org_slots): slate[:, s] = oi[:, j]
    slate[:, PIN[0]] = ai[:, 0]; slate[:, PIN[1]] = ai[:, 1]
    return slate


def random_slate(n_req, rng):
    return np.argsort(rng.random((n_req, N_ORG + N_ADS)), axis=1)[:, :K]


def log_requests(rng, n_req=N_REQ):
    c = make_candidates(n_req, rng); n = N_ORG + N_ADS
    slate = legacy_slate(c, rng); expl = rng.random(n_req) < EXPLORE; slate[expl] = random_slate(int(expl.sum()), rng)
    rows = (np.arange(n_req)[:, None] * n + slate).ravel(); imp = c.iloc[rows].reset_index(drop=True)
    imp["slot"] = np.tile(np.arange(1, K + 1), n_req); imp["explore"] = np.repeat(expl.astype(int), K); imp["day"] = np.repeat(rng.integers(0, DAYS, n_req), K)
    p_click = EXAM[imp.slot.values - 1] * imp._p_ctr_attr.values; imp["click"] = (rng.random(len(imp)) < p_click).astype(int)
    imp["order"] = ((imp.click.values == 1) & (rng.random(len(imp)) < imp._p_cvr.values)).astype(int)
    return imp.sort_values(["day", "request_id", "slot"]).reset_index(drop=True)


def generate(seed=SEED):
    rng = np.random.default_rng(seed); imp = log_requests(rng)
    d = imp.sample(n=2000, random_state=seed)                                              # duplicate impression rows
    imp.loc[imp.sample(n=1500, random_state=seed + 1).index, "rating"] = np.nan             # missing ratings
    bad = imp[imp.is_ads == 1].sample(n=300, random_state=seed + 2).index; imp.loc[bad, "bid"] = -1.0   # impossible bids
    orphan = imp[imp.click == 0].sample(n=250, random_state=seed + 3).index; imp.loc[orphan, "order"] = 1   # orders without a click
    imp = pd.concat([imp, d], ignore_index=True).sort_values(["day", "request_id", "slot"]).reset_index(drop=True)
    return imp


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs17"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs17", "impressions.csv.gz"), index=False); u = d.drop_duplicates(["request_id", "slot"]); u = u[(u.order <= u.click) & (u.bid >= 0)]
    print(len(d), "rows |", u.request_id.nunique(), "requests | CTR organic", round(u[u.is_ads == 0].click.mean(), 4), "ads", round(u[u.is_ads == 1].click.mean(), 4),
          "| orders/request", round(u.order.sum() / u.request_id.nunique(), 4), "| CVR|click organic", round(u[(u.is_ads == 0) & (u.click == 1)].order.mean(), 3), "ads", round(u[(u.is_ads == 1) & (u.click == 1)].order.mean(), 3), "| ads share of impressions", round(u.is_ads.mean(), 3))

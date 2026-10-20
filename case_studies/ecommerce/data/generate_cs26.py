"""
SYNTHETIC DATA GENERATOR - CASE STUDY 26 (Flipkart-style size and fit prediction with customer reviews)
======================================================================================================
THIS DATA IS SYNTHETIC. Flipkart's purchase, returns and review data are confidential.

Documented context (Chatterjee, Tej, Dasaraju, SIGIR eCom'22, arXiv:2208.06261): four fashion categories, labels
derived from return reason codes ("Size smaller" -> small, "Size larger" -> large, everything else -> fit), heavy class
imbalance (Table 1: Women Jacket 4.52% small / 1.68% large, Women Kurta and Kurti 2.40 / 1.30, Men's Jean 2.92 / 2.35,
Men's Polo T-shirt 3.14 / 2.76), review text as an extra signal, cold-start customers, public ModCloth data used for transfer.

Simulation (mechanism is OURS, not the paper's):
  * Each customer has a hidden body size b (continuous). They order a size s = round(b + noise).
  * Each product has a hidden "runs" offset r (brand component + fabric + product-specific): r > 0 means it runs large.
  * Gap g = s + r - b + eps. g < -t_small: garment too small; g > t_large: garment too large.
    Thresholds are calibrated per category so that (mismatch AND returned) reproduces the Table 1 shares.
  * Only a share RHO of mismatched customers return the item; the rest keep it and are labelled "fit" (label noise).
    4% of size returns carry the wrong direction reason code (agent mistake). 6% of orders return for other reasons.
  * Reviews: reviewers perceive small / fit / large from r plus their own noise; ~70% of text mentions fit (English,
    Hinglish, some generic filler); 8% carry the platform's own fit tag. A separate public labelled set (English only,
    different products) plays the role of ModCloth.
  * Customers have a prior-period history (orders, size returns, usual size = mean size of orders kept) except cold-start ones.
Hidden truth (prefixed _) allows a digital-twin test: what would the return reason have been if the tip had changed the size?

Outputs: data/cs26/{customers,products,purchases,reviews,public_fit_reviews}.csv.gz, true_params.npz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
N_CUST, N_PURCH, DAYS = 160_000, 480_000, 180
RHO = 0.5                       # share of mismatched orders actually returned
CATS = ["Women Jacket", "Women Kurta and Kurti", "Men's Jean", "Men's Polo T-shirt"]
GENDER = {0: "F", 1: "F", 2: "M", 3: "M"}
TARGET = {0: (0.0452, 0.0168), 1: (0.0240, 0.0130), 2: (0.0292, 0.0235), 3: (0.0314, 0.0276)}   # documented Table 1
N_PROD = {0: 1200, 1: 3000, 2: 1500, 3: 1300}
N_BRAND = 15
SIZES = ["S-", "S", "M", "L", "XL", "XXL"]
FABRICS = ["cotton", "polyester blend", "stretch denim", "rigid denim", "knit", "wool blend"]
FAB_EFF = {"cotton": 0.0, "polyester blend": -0.12, "stretch denim": 0.05, "rigid denim": -0.18, "knit": 0.10, "wool blend": -0.08}

SMALL_EN = ["runs small", "too tight", "order one size up", "size is smaller than expected", "very snug", "tight fit, go a size larger"]
LARGE_EN = ["runs large", "too loose", "order one size down", "size is bigger than expected", "very baggy", "loose fit, go a size smaller"]
FIT_EN = ["true to size", "perfect fit", "fits as expected", "size is just right", "fit is perfect"]
SMALL_HI = ["size chhota hai", "bahut tight hai", "ek size bada lena", "fitting chhoti aayi"]
LARGE_HI = ["size bada hai", "bahut dheela hai", "ek size chhota lena", "fitting badi aayi"]
FIT_HI = ["size ekdum sahi hai", "fitting badhiya hai", "size perfect aaya"]
FILLER = ["nice fabric", "good colour", "value for money", "delivery was quick", "stitching is decent", "looks good", "packaging was fine", "not bad for the price", "colour slightly different from picture"]
SPAM = ["Awesome product", "Super", "Nice", "Good", "Highly recommended"]


def _phrase(rng, lab, hindi):
    pools = {0: (SMALL_HI, SMALL_EN), 1: (FIT_HI, FIT_EN), 2: (LARGE_HI, LARGE_EN)}
    hi, en = pools[lab]
    return hi[rng.integers(len(hi))] if hindi else en[rng.integers(len(en))]


def _make_reviews(rng, prod_ids, run_lookup, counts, day_lo, day_hi, hindi_share, tag_share):
    pid = np.repeat(prod_ids, counts); n = len(pid); r = run_lookup[pid]
    percept = r + rng.normal(0, 0.7, n); lab = np.where(percept < -0.6, 0, np.where(percept > 0.6, 2, 1))
    flip = rng.random(n) < 0.08; lab = np.where(flip, rng.integers(0, 3, n), lab)          # sloppy reviewers
    hindi = rng.random(n) < hindi_share; has_fit = rng.random(n) < 0.70; texts = []
    for i in range(n):
        parts = [FILLER[rng.integers(len(FILLER))]]
        if has_fit[i]:
            parts.append(_phrase(rng, lab[i], hindi[i]))
        if rng.random() < 0.4:
            parts.append(FILLER[rng.integers(len(FILLER))])
        rng.shuffle(parts); texts.append(", ".join(parts))
    tag = np.where(rng.random(n) < tag_share, np.array(["small", "ok", "large"])[lab], "")
    return pd.DataFrame({"product_id": pid, "day": rng.integers(day_lo, day_hi, n), "review_text": texts, "fit_tag": tag, "rating": np.clip(np.round(rng.normal(4.0 - 0.5 * (lab != 1), 0.9, n)), 1, 5).astype(int), "_perceived": lab})


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    # ---- customers
    female = rng.random(N_CUST) < 0.55
    body = np.clip(np.where(female, rng.normal(2.2, 1.0, N_CUST), rng.normal(2.6, 1.0, N_CUST)), -0.4, 5.4)
    activity = rng.pareto(2.2, N_CUST) + 1; activity /= activity.sum()
    # ---- products
    prod = []; run = []; pid0 = 0
    brand_eff = {c: rng.normal(0, 0.35, N_BRAND) for c in range(4)}
    for c in range(4):
        n = N_PROD[c]; br = rng.integers(0, N_BRAND, n); fab = rng.choice(FABRICS if c != 2 else ["stretch denim", "rigid denim", "cotton"], n)
        if c == 2: pass
        r = brand_eff[c][br] + np.array([FAB_EFF[f] for f in fab]) + rng.normal(0, 0.35, n)
        newp = rng.random(n) < 0.20; launch = np.where(newp, rng.integers(10, 150, n), -1)
        price = np.round(np.exp(rng.normal(np.log([1700, 600, 1300, 650][c]), 0.45, n)), 0)
        prod.append(pd.DataFrame({"product_id": np.arange(pid0, pid0 + n), "category": CATS[c], "brand": [f"B{c}{b:02d}" for b in br], "fabric": fab, "price_inr": price,
                                  "launch_day": launch, "avg_rating_snapshot": np.clip(np.round(rng.normal(4.0, 0.35, n), 1), 2.5, 5.0), "_runs": r, "_cat": c}))
        pid0 += n
    products = pd.concat(prod, ignore_index=True); run_all = products._runs.values; cat_of = products._cat.values
    # ---- in-window purchases
    cust = rng.choice(N_CUST, N_PURCH, p=activity); is_f = female[cust]
    cat = np.where(is_f, np.where(rng.random(N_PURCH) < 0.28, 0, 1), np.where(rng.random(N_PURCH) < 0.55, 2, 3))
    day = rng.integers(0, DAYS, N_PURCH); prod_idx = np.zeros(N_PURCH, int)
    for c in range(4):
        m = cat == c; ids = products.index[products._cat == c].values; w = rng.pareto(1.4, len(ids)) + 1; w /= w.sum()
        prod_idx[m] = rng.choice(ids, m.sum(), p=w)
    launch = products.launch_day.values[prod_idx]; day = np.where(launch >= 0, np.minimum(DAYS - 1, np.maximum(day, launch + rng.integers(0, 30, N_PURCH))), day)
    size = np.clip(np.round(body[cust] + rng.normal(0, 0.7, N_PURCH)), 0, 5).astype(int)
    g = size + run_all[prod_idx] - body[cust] + rng.normal(0, 0.35, N_PURCH); ret_u = rng.random(N_PURCH)
    ts = np.zeros(4); tl = np.zeros(4)
    for c in range(4):
        m = cat == c; ts[c] = -np.quantile(g[m], TARGET[c][0] / RHO); tl[c] = np.quantile(g[m], 1 - TARGET[c][1] / RHO)
    def reason(g_, u_, c_, rng_):
        mis_s = g_ < -ts[c_]; mis_l = g_ > tl[c_]; ret = u_ < RHO; out = np.full(len(g_), "none", dtype=object)
        out[mis_s & ret] = "size_smaller"; out[mis_l & ret] = "size_larger"; return out
    true_reason = reason(g, ret_u, cat, rng); other = (true_reason == "none") & (rng.random(N_PURCH) < 0.06); obs = true_reason.copy(); obs[other] = "other"
    swap = np.isin(obs, ["size_smaller", "size_larger"]) & (rng.random(N_PURCH) < 0.04)
    obs[swap] = np.where(obs[swap] == "size_smaller", "size_larger", "size_smaller")
    purchases = pd.DataFrame({"order_id": np.arange(N_PURCH), "customer_id": cust, "product_id": products.product_id.values[prod_idx], "category": np.array(CATS)[cat], "day": day,
                              "size_ordered_idx": size, "return_reason": obs, "_gap": g, "_ret_u": ret_u, "_true_reason": true_reason, "_cat": cat}).sort_values(["day", "order_id"]).reset_index(drop=True)
    # ---- prior-period history (customers without any are cold-start)
    n_pre = np.where(rng.random(N_CUST) < 0.40, 0, np.maximum(1, rng.negative_binomial(1.6, 1.6 / (1.6 + 3.2), N_CUST))); n_pre = np.minimum(n_pre, 40)
    cu = np.repeat(np.arange(N_CUST), n_pre); m_ = len(cu); cat_p = np.where(female[cu], np.where(rng.random(m_) < 0.28, 0, 1), np.where(rng.random(m_) < 0.55, 2, 3))
    s_p = np.clip(np.round(body[cu] + rng.normal(0, 0.7, m_)), 0, 5).astype(int); r_p = rng.normal(0, 0.55, m_)
    g_p = s_p + r_p - body[cu] + rng.normal(0, 0.35, m_); u_p = rng.random(m_); rs = reason(g_p, u_p, cat_p, rng)
    dfp = pd.DataFrame({"c": cu, "s": s_p, "small": (rs == "size_smaller").astype(int), "large": (rs == "size_larger").astype(int), "kept": (rs == "none").astype(int)})
    agg = dfp.groupby("c").agg(pre_orders=("s", "size"), pre_small_returns=("small", "sum"), pre_large_returns=("large", "sum"))
    kept = dfp[dfp.kept == 1].groupby("c").s.mean().rename("usual_size")
    customers = pd.DataFrame({"customer_id": np.arange(N_CUST), "gender": np.where(female, "F", "M"), "age_band": rng.choice(["18-24", "25-34", "35-44", "45+"], N_CUST, p=[0.30, 0.38, 0.22, 0.10]),
                              "city_tier": rng.choice([1, 2, 3], N_CUST, p=[0.35, 0.35, 0.30]), "_body": body}).set_index("customer_id").join(agg).join(kept).fillna({"pre_orders": 0, "pre_small_returns": 0, "pre_large_returns": 0}).reset_index()
    for c in ("pre_orders", "pre_small_returns", "pre_large_returns"):
        customers[c] = customers[c].astype(int)
    customers["usual_size"] = customers.usual_size.round(2)
    # ---- reviews (existing products only; day -120..-1 relative to the purchase window)
    existing = products.product_id.values[products.launch_day.values < 0]
    cnt = np.where(rng.random(len(existing)) < 0.18, 0, rng.negative_binomial(0.9, 0.9 / (0.9 + 10), len(existing)))
    reviews = _make_reviews(rng, existing, run_all, cnt, -120, 0, 0.30, 0.08)
    # spam: 2% bulk "Awesome product" duplicates with no fit information
    k = int(0.02 * len(reviews)); sp = reviews.sample(k, random_state=seed).copy(); sp["review_text"] = rng.choice(SPAM, k); sp["fit_tag"] = ""; reviews = pd.concat([reviews, sp], ignore_index=True)
    reviews.insert(0, "review_id", np.arange(len(reviews)))
    # public labelled set (ModCloth-like): English only, 6,000 reviews, other products
    pub_runs = rng.normal(0, 0.55, 3000); pub = _make_reviews(rng, np.arange(3000), pub_runs, np.full(3000, 2), 0, 1, 0.0, 1.0)
    pub = pub.rename(columns={"product_id": "item_id"}).assign(label=lambda d: np.array(["small", "fit", "large"])[d._perceived])[["item_id", "review_text", "label"]]
    # ---- data-quality defects
    dup = purchases.sample(n=1500, random_state=seed); purchases = pd.concat([purchases, dup], ignore_index=True).sort_values(["day", "order_id"]).reset_index(drop=True)
    miss = rng.random(len(purchases)) < 0.008; purchases["size_ordered_idx"] = purchases.size_ordered_idx.astype(float).where(~miss)
    products.loc[rng.random(len(products)) < 0.01, "brand"] = None
    purchases["size_ordered"] = purchases.size_ordered_idx.map(lambda v: SIZES[int(v)] if v == v else None)
    params = dict(ts=ts, tl=tl, rho=RHO)
    return dict(customers=customers, products=products.drop(columns=["_cat"]), purchases=purchases.drop(columns=["_cat"]), reviews=reviews, public=pub, params=params, cat_of_order=None)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, "cs26"); os.makedirs(out, exist_ok=True)
    d = generate(); p = d["purchases"]
    for k, f in (("customers", "customers"), ("products", "products"), ("purchases", "purchases"), ("reviews", "reviews"), ("public", "public_fit_reviews")):
        d[k].to_csv(os.path.join(out, f + ".csv.gz"), index=False)
    print(len(p), "orders |", p.return_reason.value_counts(normalize=True).round(4).to_dict(), "| reviews", len(d["reviews"]))

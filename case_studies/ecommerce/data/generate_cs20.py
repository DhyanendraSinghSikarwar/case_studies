"""
SYNTHETIC DATA GENERATOR - CASE STUDY 20 (predicted lifetime value of new customers for bid optimisation)
========================================================================================================
THIS DATA IS SYNTHETIC. Swiggy's customer data is confidential.

Documented context (InfoQ report of Swiggy's own post, 2 Sep 2026; the original post was not readable): predict
long-term value of NEW customers across Food and Instamart BEFORE the first order, from 350+ pre-first-order features
(acquisition channel, device and fraud signals, geography, complaint history, Instamart category affinity, payment
patterns, socio-economic indicators). Many new users place no order within 30 days while a small group generates much
higher lifetime value (zero-inflated, long tail). Model: multi-task MLP, 3 shared hidden layers, heads for Food and
Instamart; evaluated by decile ranking (Spearman > 0.75, diagonal coverage 70-80%); output feeds Google tROAS bidding.
Dataset size, time range, split scheme, layer sizes and lift figures are NOT public (ND).

Simulation: 60,000 new customers over 52 weekly signup cohorts, about 60 pre-first-order features (a handful drive
value, most are weak or pure noise), 180-day gross order value (GOV) for Food and Instamart, hurdle structure
(P(no order) about one third; heavy-tailed value given active). The channel mix drifts over time (more influencer
traffic late in the year). An ad-auction side table gives the competing clearing price per acquired customer,
priced from COARSE signals only (channel, city tier, OS, device tier), so a model with richer pre-order features
has an information edge. Hidden ground-truth columns are prefixed with "_".

Outputs: data/cs20/customers.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
N = 60_000; WEEKS = 52
CHANNELS = ["organic", "google_uac", "meta", "referral", "influencer", "cashback_affiliate"]
CH_ACT = np.array([0.35, 0.10, 0.00, 0.45, -0.20, -0.55]); CH_FREQ = np.array([0.20, 0.05, -0.05, 0.25, -0.10, -0.35])


def _sig(x):
    return 1 / (1 + np.exp(-x))


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    week = np.sort(rng.integers(0, WEEKS, N)); frac = week / (WEEKS - 1)
    p_ch = np.array([0.30 - 0.12 * frac, 0.25 + 0.0 * frac, 0.20 - 0.02 * frac, 0.10 + 0.0 * frac, 0.05 + 0.12 * frac, 0.10 + 0.02 * frac]).T; p_ch = p_ch / p_ch.sum(1, keepdims=True)
    ch = (p_ch.cumsum(1) < rng.random(N)[:, None]).sum(1)
    os_ios = (rng.random(N) < np.where(ch == 2, 0.35, 0.22)).astype(int); city = rng.choice([1, 2, 3], N, p=[0.45, 0.33, 0.22]); e = rng.normal(0, 1, N); a = rng.normal(0, 1, N)
    aff = np.clip(55 - 9 * (city - 1) + 8 * os_ios + rng.normal(0, 14, N), 0, 100); aff_z = (aff - 50) / 18
    tier = np.clip(np.rint(2 + 0.6 * aff_z + 0.5 * os_ios + rng.normal(0, 0.7, N)), 1, 3).astype(int)
    fraud = np.clip(_sig(-2.4 + 1.6 * (ch == 5) + 0.9 * (ch == 4) + rng.normal(0, 1.1, N)), 0, 1)
    coupon = (rng.random(N) < _sig(-0.4 + 0.9 * (ch == 5) + 0.5 * (ch == 2) + 0.2 * e)).astype(int); referral = (ch == 3).astype(int) | (rng.random(N) < 0.03)
    hour = np.clip(np.rint(rng.normal(19, 4.5, N)), 0, 23).astype(int); dow = rng.integers(0, 7, N); dist = np.exp(rng.normal(np.log(2.2), 0.55, N)) * np.where(city == 3, 1.5, 1.0)
    sessions = rng.poisson(np.exp(1.0 + 0.5 * e)); searches = rng.poisson(np.exp(0.4 + 0.6 * e)); cart = rng.poisson(np.exp(-0.2 + 0.7 * e)); cart_val = np.round(cart * np.exp(rng.normal(5.7 + 0.2 * aff_z, 0.5, N)), 0)
    first_min = np.exp(rng.normal(1.2 + 0.3 * e, 0.6)); food_share = _sig(-0.4 * a + rng.normal(0, 0.8, N)); rest_view = rng.poisson(np.exp(1.2 + 0.4 * e - 0.2 * a)); rest_price = np.exp(rng.normal(np.log(320) + 0.18 * aff_z, 0.25, N))
    insta_cat = {c: rng.poisson(np.exp(-0.4 + 0.55 * a + 0.2 * e + off)) for c, off in (("grocery", 0.5), ("fresh", 0.2), ("snacks", 0.1), ("personal_care", -0.3), ("electronics", -0.9))}
    complaints = rng.poisson(np.exp(-2.2 + 0.25 * (city == 3) + 0.2 * fraud * 3 - 0.2 * e)); pp = np.column_stack([0.55 - 0.1 * (city - 1), 0.20 + 0.1 * os_ios, 0.10 + 0.1 * (city - 1), np.full(N, 0.15)]); pp = pp / pp.sum(1, keepdims=True)
    payment = np.array(["upi", "card", "cod", "wallet"])[np.minimum((pp.cumsum(1) < rng.random(N)[:, None]).sum(1), 3)]
    notif = (rng.random(N) < _sig(0.8 + 0.3 * e)).astype(int); loc_prec = (rng.random(N) < _sig(0.9 + 0.2 * e)).astype(int); contacts = np.exp(rng.normal(5.2 + 0.2 * e, 0.8, N)); density = np.exp(rng.normal(3.0 - 0.4 * (city - 1), 0.5, N))
    install_gap = np.exp(rng.normal(2.0 - 0.3 * e, 1.0, N)); app_ver = rng.integers(0, 4, N)
    # ---- hidden value structure
    logit_act = 0.55 + 0.85 * e + 0.35 * coupon + 0.30 * referral + CH_ACT[ch] - 2.6 * fraud - 0.18 * (dist - 2.2) + 0.25 * aff_z + 0.18 * notif + 0.12 * loc_prec - 0.12 * np.minimum(complaints, 3) + 0.02 * np.minimum(cart, 5)
    p_act = _sig(logit_act); active180 = rng.random(N) < p_act; active30 = active180 & (rng.random(N) < 0.80)
    frailty = rng.normal(0, 0.75, N); log_mu = np.log(2.2) + 0.50 * e + 0.30 * a + CH_FREQ[ch] + 0.25 * aff_z + 0.10 * (tier - 2) - 0.10 * (dist - 2.2) / 2 + frailty
    mu = np.exp(log_mu); k = 1.6; n_extra = rng.negative_binomial(k, k / (k + mu)); n_ord = np.where(active180, 1 + n_extra, 0)
    q_ins = _sig(-1.3 + 0.9 * a + 0.2 * aff_z + 0.6 * np.log1p(insta_cat["grocery"] + insta_cat["fresh"]) * 0.3)
    uid = np.repeat(np.arange(N), n_ord); is_ins = rng.random(len(uid)) < q_ins[uid]
    base_food = np.exp(np.log(340) + 0.15 * aff_z + 0.06 * (tier - 2)); base_ins = np.exp(np.log(560) + 0.20 * aff_z + 0.06 * (tier - 2))
    val = np.where(is_ins, base_ins[uid], base_food[uid]) * np.exp(rng.normal(0, 0.45, len(uid)))
    food = np.bincount(uid, weights=np.where(is_ins, 0, val), minlength=N); ins = np.bincount(uid, weights=np.where(is_ins, val, 0), minlength=N); o30 = np.bincount(uid, weights=(rng.random(len(uid)) < np.where(active30[uid], 0.45, 0.0)).astype(float), minlength=N)
    orders30 = np.where(active30, np.minimum(np.maximum(1, np.rint(o30)), n_ord), 0).astype(int)
    ltv = food + ins
    # ---- competitor clearing price (auction), from COARSE signals only
    coarse = np.exp(0.9 * CH_ACT[ch] + 0.6 * CH_FREQ[ch] + 0.18 * (3 - city) + 0.12 * os_ios + 0.08 * (tier - 2)); coarse = coarse / coarse.mean() * 1500
    clearing = 0.040 * coarse * np.exp(rng.normal(0, 0.55, N))
    df = pd.DataFrame({
        "customer_id": np.arange(N), "signup_week": week, "channel": np.array(CHANNELS)[ch], "os_ios": os_ios, "device_price_tier": tier, "city_tier": city, "signup_hour": hour, "signup_dow": dow,
        "payment_pref": payment, "referral_used": referral.astype(int), "coupon_first_session": coupon, "notification_opt_in": notif, "location_precise": loc_prec, "app_version_bucket": app_ver,
        "first_session_minutes": np.round(first_min, 2), "sessions_pre": sessions, "searches_pre": searches, "cart_adds_pre": cart, "cart_value_pre_inr": cart_val, "food_browse_share": np.round(food_share, 3),
        "restaurants_viewed": rest_view, "avg_restaurant_price_viewed": np.round(rest_price, 0), **{f"insta_views_{c}": v for c, v in insta_cat.items()}, "distance_nearest_store_km": np.round(dist, 2),
        "pincode_affluence_index": np.round(aff, 1), "pincode_order_density": np.round(density, 2), "fraud_score": np.round(fraud, 3), "complaints_pre": complaints, "contacts_book_size": np.round(contacts, 0), "install_to_signup_hours": np.round(install_gap, 2),
        **{f"noise_{i:02d}": rng.normal(0, 1, N).round(3) for i in range(1, 21)},
        "orders_30d": orders30, "orders_180d": n_ord, "food_ltv_180d": np.round(food, 0), "insta_ltv_180d": np.round(ins, 0), "ltv_180d": np.round(ltv, 0),
        "_latent_intent": np.round(e, 3), "_p_active": np.round(p_act, 4), "_active180": active180.astype(int), "_clearing_price_inr": np.round(clearing, 1), "_coarse_value_inr": np.round(coarse, 0)})
    # data-quality defects
    big = rng.choice(N, 36, replace=False); bulk = np.round(rng.uniform(150_000, 600_000, 36), 0); df.loc[big, "ltv_180d"] = bulk; df.loc[big, "food_ltv_180d"] = bulk     # bulk / corporate accounts
    bad = rng.choice(N, 14, replace=False); df.loc[bad, "ltv_180d"] = -np.abs(df.loc[bad, "ltv_180d"]) - 100                                                 # refunds booked as negative
    df.loc[rng.choice(N, int(0.06 * N), replace=False), "device_price_tier"] = np.nan; df.loc[rng.choice(N, int(0.04 * N), replace=False), "pincode_affluence_index"] = np.nan
    df.loc[rng.choice(N, int(0.02 * N), replace=False), "fraud_score"] = np.nan
    df = pd.concat([df, df.sample(n=600, random_state=seed)], ignore_index=True).sample(frac=1, random_state=seed).reset_index(drop=True)
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs20"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs20", "customers.csv.gz"), index=False)
    c = d.drop_duplicates("customer_id"); c = c[(c.ltv_180d >= 0) & (c.ltv_180d < 100_000)]
    print(len(d), "rows |", len(c), "clean | zero in 30d", round((c.orders_30d == 0).mean(), 3), "| zero in 180d", round((c.ltv_180d == 0).mean(), 3), "| mean ltv", round(c.ltv_180d.mean()), "| median", c.ltv_180d.median(), "| P90", c.ltv_180d.quantile(0.9).round())
    s = c.ltv_180d.sort_values(ascending=False); print("top10% share", round(s.head(len(s) // 10).sum() / s.sum(), 3), "| top1% share", round(s.head(len(s) // 100).sum() / s.sum(), 3), "| insta share of value", round(c.insta_ltv_180d.sum() / (c.food_ltv_180d.sum() + c.insta_ltv_180d.sum()), 3))
    print("ltv by channel", c.groupby("channel").ltv_180d.mean().round().to_dict()); print("channel mix wk<10", c[c.signup_week < 10].channel.value_counts(normalize=True).round(3).to_dict(), "wk>=42", c[c.signup_week >= 42].channel.value_counts(normalize=True).round(3).to_dict())
    from scipy.stats import spearmanr
    print("spearman(ltv, p_active)", round(spearmanr(c.ltv_180d, c._p_active)[0], 3), "| spearman(ltv, ltv-coarse)", round(spearmanr(c.ltv_180d, c._coarse_value_inr)[0], 3), "| mean clearing", round(c._clearing_price_inr.mean(), 1), "| corr(orders30, ltv) spearman", round(spearmanr(c.orders_30d, c.ltv_180d)[0], 3))

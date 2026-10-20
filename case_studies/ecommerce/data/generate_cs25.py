"""
SYNTHETIC DATA GENERATOR - CASE STUDY 25 (COD return-to-origin prediction, Flipkart / IIIT research)
===================================================================================================
THIS DATA IS SYNTHETIC. Flipkart's order data and the profile data used in the paper are confidential/private.

Documented context (Hitkul et al., "Social Re-Identification Assisted RTO Detection for E-Commerce", WWW '23 Companion):
COD orders only; a 5% randomised, un-intervened control set gives clean labels; past-trend features (RTO ratio for user,
product, seller, category, pin code over 3 months and 1 year); social-profile features obtained by re-identifying the user
on a public professional network (name + city, candidate found for 1,091 of 2,121 users, exact match 68.9% / multiple 17.7% /
no match 13.4% at threshold 0.6); 32% of the final orders were RTO; Nov 2021 - Apr 2022 with the first 5 months as train and
the last month as test.

Simulation (our assumptions; only the 32% RTO rate, 51% candidate coverage and ~87% matched-at-0.6 are calibrated to the paper):
  * 14,000 users, 600 pin codes, 300 sellers, 20 categories, 40,000 COD orders in the randomised control set (days 0-179).
  * RTO propensity = user effect + pin-code effect (drifting by month) + seller + category + order features.
    The user effect is partly driven by a hidden socio-economic "reliability" r_u and a hidden occupation type (6 types).
  * Past-trend features are noisy: counts drawn from the entities' true rates (users have few past orders, so their trend is thin).
  * Social features exist only for users with a found profile, and a wrong candidate is matched sometimes (its profile is someone else's).
  * A second dataset ("legacy_logged") has the same distribution but an old rule blocks risky COD orders, so their outcome is never observed.
Hidden truth columns are prefixed "_".

Outputs: data/cs25/control_orders.csv.gz, data/cs25/legacy_logged_orders.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.optimize import brentq

SEED = 42
N_USERS, N_PIN, N_SELLER, N_CAT, N_ORD, DAYS = 14_000, 600, 300, 20, 40_000, 180
N_TYPES, EMB = 6, 8
TYPE_NAMES = ["student", "early career", "mid-career professional", "self-employed / business", "senior manager", "other / not stated"]
TYPE_EFF = np.array([0.50, 0.30, -0.30, 0.20, -0.50, 0.60])
TARGET_RTO = 0.32


def _sig(z):
    return 1 / (1 + np.exp(-z))


def _world(rng):
    """Users, entities and their hidden effects."""
    typ = rng.choice(N_TYPES, N_USERS, p=[0.14, 0.26, 0.22, 0.16, 0.08, 0.14])
    r = rng.normal(0, 1, N_USERS)                                           # hidden reliability
    user_eff = -1.30 * r + 1.10 * TYPE_EFF[typ] + rng.normal(0, 0.40, N_USERS)
    users = pd.DataFrame({"user_id": np.arange(N_USERS), "_type": typ, "_reliability": r, "_user_effect": user_eff})
    # profile (what a re-identified public profile would show)
    users["is_student"] = (typ == 0).astype(int)
    users["n_jobs"] = rng.poisson(np.array([0.3, 1.2, 2.5, 2.0, 3.5, 1.0])[typ])
    users["n_degrees"] = 1 + rng.poisson(np.array([0.3, 0.5, 0.7, 0.4, 0.8, 0.3])[typ])
    users["friends"] = np.round(np.exp(rng.normal(5.0 + 0.5 * r, 0.7) + 0.2 * (typ == 4))).astype(int)
    users["followers"] = np.round(np.exp(rng.normal(4.6 + 0.6 * r, 0.8) + 0.2 * (typ >= 3))).astype(int)
    users["years_working"] = np.round(np.clip(rng.normal(np.array([0.3, 3, 9, 8, 16, 4])[typ], 2.5), 0, 40), 1)
    users["years_education"] = np.round(np.clip(rng.normal(np.array([13, 16, 17, 15, 17, 14])[typ] + 0.8 * r, 1.2), 8, 24), 1)
    cent = np.random.default_rng(7).normal(0, 1, (N_TYPES, EMB))            # embedding centroid per occupation type
    emb = cent[typ] + rng.normal(0, 1.1, (N_USERS, EMB))
    for k in range(EMB): users[f"emb_{k}"] = np.round(emb[:, k], 3)
    ent = dict(pin_eff=rng.normal(0, 1.0, N_PIN), pin_drift=rng.normal(0, 0.18, (N_PIN, 7)).cumsum(1), seller_eff=rng.normal(0, 0.70, N_SELLER), cat_eff=rng.normal(0, 0.45, N_CAT))
    # re-identification outcome per user
    found = rng.random(N_USERS) < 0.51
    correct = rng.random(N_USERS) < 0.88
    score = np.where(correct, rng.beta(9, 2, N_USERS), rng.beta(2.5, 4, N_USERS))
    users["found_profile"] = found.astype(int); users["match_score"] = np.where(found, np.round(score, 3), np.nan); users["_true_match"] = np.where(found, correct.astype(int), -1)
    wrong_src = rng.integers(0, N_USERS, N_USERS)                           # a wrong candidate shows someone else's profile
    prof_cols = ["is_student", "n_jobs", "n_degrees", "friends", "followers", "years_working", "years_education"] + [f"emb_{k}" for k in range(EMB)]
    shown = users[prof_cols].copy(); wrong = found & ~correct; shown.loc[wrong] = users.loc[wrong_src[wrong], prof_cols].values
    users[prof_cols] = shown
    users["user_activity"] = rng.lognormal(np.log(1.6), 0.8, N_USERS)       # expected orders per year before the study (thin for many)
    users["_order_weight"] = rng.lognormal(0, 0.9, N_USERS)
    return users, ent, prof_cols


def _orders(rng, users, ent, n, c0, scale_c):
    uid = rng.choice(N_USERS, n, p=users["_order_weight"] / users["_order_weight"].sum())
    day = np.sort(rng.integers(0, DAYS, n)); month = np.minimum(day // 30, 5)
    pin = rng.integers(0, N_PIN, n); seller = rng.integers(0, N_SELLER, n); cat = rng.integers(0, N_CAT, n)
    hour = np.clip(np.round(rng.normal(15, 5.5, n)), 0, 23).astype(int); weekday = (day + 1) % 7
    value = np.round(np.exp(rng.normal(np.log(700), 0.8, n)), 0)
    night = ((hour >= 23) | (hour <= 4)).astype(int)
    o = pd.DataFrame({"user_id": uid, "day": day, "hour": hour, "weekday": weekday, "category": cat, "seller_id": seller, "pincode_id": pin, "order_value_inr": value})
    pin_now = ent["pin_eff"][pin] + ent["pin_drift"][pin, month + 1]
    logit = c0 + users["_user_effect"].values[uid] + pin_now + ent["seller_eff"][seller] + ent["cat_eff"][cat] + 0.40 * (np.log(value) - np.log(700)) + 0.25 * night + 0.12 * (weekday >= 5)
    o["_p_rto"] = _sig(logit)
    # past-trend features: noisy counts from the entities' own rates (information available at checkout)
    def trend(rate_3m, rate_1y, n3, n1):
        k3 = rng.binomial(n3, rate_3m); k1 = rng.binomial(n1, rate_1y)
        return np.where(n3 > 0, k3 / np.maximum(n3, 1), np.nan), n3, np.where(n1 > 0, k1 / np.maximum(n1, 1), np.nan), n1
    ur = _sig(c0 * scale_c + users["_user_effect"].values[uid]); n1 = rng.poisson(users["user_activity"].values[uid] * 1.2); n3 = rng.binomial(n1, 0.3)
    o["user_rto_3m"], o["user_n_3m"], o["user_rto_1y"], o["user_n_1y"] = trend(ur, ur, n3, n1)
    for name, eff_now, eff_old, nn in (("pin", pin_now, ent["pin_eff"][pin] + ent["pin_drift"][pin, np.maximum(month - 1, 0)], 90), ("seller", ent["seller_eff"][seller], ent["seller_eff"][seller], 160), ("cat", ent["cat_eff"][cat], ent["cat_eff"][cat], 900)):
        n1y = rng.poisson(nn * 4, n); n3m = rng.binomial(n1y, 0.28)
        r3 = _sig(c0 * scale_c + 0.9 * eff_old); r1 = _sig(c0 * scale_c + 0.9 * eff_old * 0.8)
        o[f"{name}_rto_3m"], _, o[f"{name}_rto_1y"], _ = trend(r3, r1, n3m, n1y)
    o["pin_rto_3m"] = o["pin_rto_3m"].round(3)
    for col in [c for c in o.columns if c.endswith(("_3m", "_1y")) and "_n_" not in c]: o[col] = o[col].round(3)
    soc = users.drop(columns=[c for c in users.columns if c in ("_order_weight", "user_activity")])
    o = o.merge(soc, on="user_id", how="left")
    o.insert(0, "order_id", np.arange(n)); o["rto"] = (rng.random(n) < o["_p_rto"]).astype(int)
    return o


def generate(seed=SEED):
    rng = np.random.default_rng(seed); users, ent, prof_cols = _world(rng)
    # intercept calibrated to the documented 32% RTO share
    probe = _orders(np.random.default_rng(seed + 1), users, ent, 12_000, 0.0, 0.0)
    c0 = brentq(lambda c: _sig(np.log(probe["_p_rto"] / (1 - probe["_p_rto"])) + c).mean() - TARGET_RTO, -4, 4)
    control = _orders(rng, users, ent, N_ORD, c0, 1.0)
    legacy = _orders(rng, users, ent, N_ORD, c0, 1.0)
    blocked = ((legacy.user_n_3m >= 1) & (legacy.user_rto_3m >= 0.9)) | (legacy.pin_rto_3m >= 0.46) | ((legacy.user_n_1y >= 3) & (legacy.user_rto_1y >= 0.6))
    legacy["legacy_blocked"] = blocked.astype(int); legacy["_rto_if_shipped"] = legacy["rto"]; legacy.loc[blocked, "rto"] = np.nan
    control["legacy_blocked"] = 0
    # data-quality defects (control only)
    dup = control.sample(n=600, random_state=seed); control = pd.concat([control, dup], ignore_index=True)
    control.loc[rng.random(len(control)) < 0.01, "order_value_inr"] = np.nan
    bad = rng.random(len(control)) < 0.002; control.loc[bad, "order_value_inr"] = 9_999_999
    bad = rng.random(len(control)) < 0.003; control.loc[bad, "hour"] = 25
    return control, legacy, dict(prof_cols=prof_cols, c0=c0, type_names=TYPE_NAMES)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, "cs25"); os.makedirs(out, exist_ok=True)
    ctl, leg, tp = generate()
    ctl.to_csv(os.path.join(out, "control_orders.csv.gz"), index=False); leg.to_csv(os.path.join(out, "legacy_logged_orders.csv.gz"), index=False)
    print("control rows", len(ctl), "RTO rate", ctl.rto.mean().round(4), "| legacy blocked share", leg.legacy_blocked.mean().round(3), "| observed-label RTO rate (legacy)", leg.rto.mean().round(4))
    print("found profile share (orders)", ctl.found_profile.mean().round(3), "| thin history (n_1y<=1) share", (ctl.user_n_1y <= 1).mean().round(3))

"""
SYNTHETIC DATA GENERATOR - CASE STUDY 2 (Zomato food preparation time and rider dispatch)
========================================================================================
THIS DATA IS SYNTHETIC. Kitchen-level order timestamps are confidential.

Documented context (Zomato blog, Feb 2020; Swiggy Bytes 2019, 2023): FPT label was restaurant-accepted to rider
pick-up, so it includes rider behaviour; a restaurant-marked "Food Order Ready" (FOR) button gives a cleaner label
(company-claimed 9% gain in within-5-minutes accuracy); features are order items, restaurant, kitchen state (running
orders, last completed orders); naive just-in-time dispatch delays assignment by (prep time - first-mile time).

Simulation: 250 restaurants, ~150,000 orders over 60 days.
  * True food-ready time (hidden) = dish base time x restaurant type x restaurant speed x load x peak x noise.
  * Old label (pick-up) = max(food ready, rider arrival under dispatch-at-once) + handover: censored below by the rider.
  * FOR label: pressed on only part of the orders (compliance falls with kitchen load); some presses are made at pick-up.
  * Rider first-mile (incl. assignment) is random and larger in rain and at peaks.
Outputs: orders.csv.gz, restaurants.csv.gz (columns starting with "_" are hidden truth, for the digital twin only).
"""
import numpy as np
import pandas as pd

SEED = 42
N_R, DAYS, N_ORD = 250, 60, 150_000
START = pd.Timestamp("2026-03-01")
TYPES = ["cloud kitchen", "quick service", "casual dining", "fine dining"]
TYPE_MULT = {"cloud kitchen": 0.90, "quick service": 0.85, "casual dining": 1.05, "fine dining": 1.20}
TYPE_CAP = {"cloud kitchen": (3, 6), "quick service": (2, 5), "casual dining": (2, 4), "fine dining": (1, 3)}
TYPE_FOR = {"cloud kitchen": 0.75, "quick service": 0.55, "casual dining": 0.35, "fine dining": 0.22}
GROUPS = ["beverage", "snacks", "roll/wrap", "burger", "pizza", "biryani", "north indian", "chinese", "south indian", "dessert", "thali", "grill"]
BASE_MIN = np.array([4, 8, 9, 10, 15, 14, 16, 15, 11, 6, 17, 22], float)


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    typ = rng.choice(len(TYPES), N_R, p=[0.30, 0.30, 0.28, 0.12]); tname = np.array(TYPES)[typ]
    cap = np.array([rng.integers(*TYPE_CAP[t]) for t in tname]); speed = np.exp(rng.normal(0, 0.18, N_R)); sigma = rng.uniform(0.12, 0.30, N_R)
    comp = np.clip(np.array([TYPE_FOR[t] for t in tname]) + rng.normal(0, 0.12, N_R), 0.03, 0.95); gaming = rng.beta(1.2, 6, N_R)
    cuis = rng.choice(len(GROUPS), (N_R, 2), p=np.array([0.04, 0.10, 0.08, 0.09, 0.09, 0.10, 0.14, 0.09, 0.08, 0.04, 0.08, 0.07]))
    vol = np.exp(rng.normal(0, 1.05, N_R)) * np.array([1.3 if t == "cloud kitchen" else 1.0 for t in tname]); vol /= vol.sum()
    rest = pd.DataFrame({"restaurant_id": np.arange(N_R), "rest_type": tname, "kitchen_capacity": cap, "cuisine_group": [GROUPS[c] for c in cuis[:, 0]],
                         "_speed": speed, "_noise_sigma": sigma, "_for_compliance": comp, "_for_gaming_rate": gaming})
    r = rng.choice(N_R, N_ORD, p=vol); day = rng.integers(0, DAYS, N_ORD)
    hw = np.array([1, 0.5, 0.3, 0.2, 0.2, 0.4, 1, 2, 3, 3, 3, 5, 9, 9, 6, 3, 2, 3, 5, 8, 10, 9, 6, 3], float); hw = hw / hw.sum()
    hour = rng.choice(24, N_ORD, p=hw); sec = hour * 3600 + rng.integers(0, 3600, N_ORD); dow = day % 7; rain_day = rng.random(DAYS) < 0.2; rain = rain_day[day].astype(int)
    ts = START + pd.to_timedelta(day, unit="D") + pd.to_timedelta(sec, unit="s")
    df = pd.DataFrame({"restaurant_id": r, "day": day, "hour": hour, "dow": dow, "rain": rain, "order_ts": ts, "_sec": day * 86400 + sec}).sort_values(["restaurant_id", "_sec"]).reset_index(drop=True)
    key = df.restaurant_id.values.astype(np.int64) * 10**8 + df._sec.values; idx = np.arange(N_ORD); q = idx - np.searchsorted(key, key - 900, side="left")
    df["_qlen"] = q; df["running_orders"] = np.minimum(q, 5)
    rr = df.restaurant_id.values; grp = np.where(rng.random(N_ORD) < 0.7, cuis[rr, 0], cuis[rr, 1]); n_items = np.minimum(1 + rng.poisson(1.1, N_ORD), 8)
    df["rest_type"] = tname[rr]; df["kitchen_capacity"] = cap[rr]; df["cuisine_group"] = rest.cuisine_group.values[rr]
    df["dish_group"] = np.array(GROUPS)[grp]; df["n_items"] = n_items; df["order_value_inr"] = np.round(np.maximum(40, n_items * np.exp(rng.normal(np.log(190), 0.35, N_ORD)) * (1 + 0.35 * (tname[rr] == "fine dining"))), 0)
    peak = ((hour >= 12) & (hour <= 14)) | ((hour >= 19) & (hour <= 22)); df["_peak"] = peak.astype(int)
    mu = BASE_MIN[grp] * np.array([TYPE_MULT[t] for t in tname])[rr] * speed[rr] * (1 + 0.14 * (n_items - 1) ** 0.8) * (1 + 0.16 * q / cap[rr]) * (1 + 0.08 * peak) * (1 + 0.04 * rain) * (1 + 0.03 * (dow >= 5))
    df["_true_fpt_min"] = np.maximum(2.0, mu * np.exp(rng.normal(0, 1, N_ORD) * sigma[rr] - sigma[rr] ** 2 / 2) + 0.8)
    fm_det = 6.0 * (1 + 0.15 * peak) * (1 + 0.20 * rain); df["_first_mile_min"] = fm_det * np.exp(rng.normal(0, 0.45, N_ORD)) + 1.0
    df["est_first_mile_min"] = np.round((fm_det * np.exp(0.1) + 1.0) * np.exp(rng.normal(0, 0.12, N_ORD)), 1)
    pick = np.maximum(df._true_fpt_min.values, df._first_mile_min.values) + rng.exponential(0.7, N_ORD); df["pickup_label_min"] = pick
    p_press = comp[rr] * (1 - 0.07 * np.minimum(q, 5)); pressed = rng.random(N_ORD) < np.clip(p_press, 0, 1); gm = rng.random(N_ORD) < gaming[rr]
    honest = np.maximum(1.0, df._true_fpt_min.values + rng.normal(0, 1.0, N_ORD)); df["for_label_min"] = np.where(pressed, np.where(gm, pick, honest), np.nan); df["_for_gamed"] = (pressed & gm).astype(int)
    # data-quality defects: glitchy timestamps, duplicates, missing values
    g = rng.random(N_ORD) < 0.004; df.loc[g, "pickup_label_min"] = rng.choice([0.2, 0.5, 150.0, 240.0, 600.0], g.sum())
    miss = rng.random(N_ORD) < 0.015; df.loc[miss, "order_value_inr"] = np.nan
    df = df.drop(columns="_sec"); df = pd.concat([df, df.sample(n=800, random_state=seed)], ignore_index=True).sort_values(["order_ts", "restaurant_id"]).reset_index(drop=True)
    df.insert(0, "order_id", np.arange(len(df)))
    for c in ("pickup_label_min", "for_label_min", "_true_fpt_min", "_first_mile_min"): df[c] = df[c].round(2)
    return df, rest

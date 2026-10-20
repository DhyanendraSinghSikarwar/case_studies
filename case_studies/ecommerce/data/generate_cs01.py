"""
SYNTHETIC DATA GENERATOR - CASE STUDY 1 (Swiggy-style multi-stage ETA / delivery-time promise)
============================================================================================
THIS DATA IS SYNTHETIC. Swiggy order logs are confidential.

Structure follows what Swiggy's engineering posts document (Bytes 2018 and 2023):
  Delivery time = max(assignment delay + first mile, prep time) + last mile
  O2A (order->assigned) + FM (first mile) + WT (wait at restaurant) + LM (last mile) = O2R (order->reached customer)
Cart sessions show a promised delivery time (pSLA). The legacy promise here is a restaurant x hour historical
average plus a safety buffer. Swiggy disclosed no absolute errors, so scales are our assumptions.

Hidden drivers: restaurant prep speed and kitchen stress, delivery-executive (DE) supply vs orders (rain and dinner
peak reduce supply), city traffic, distance. Orders in 28 days across 3 cities, 600 restaurants.
A RANDOMISED promise perturbation (+-3 min on the shown promise for 20% of sessions) lets us measure how conversion
responds to the promised time (a design we add; Swiggy documents the Goldilocks trade-off but no experiment).
Late deliveries raise customer-care contacts and cancellations.

Output: data/cs01/sessions.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
START = pd.Timestamp("2026-03-02"); DAYS = 28


def generate(seed=SEED, n_sessions=220_000):
    rng = np.random.default_rng(seed)
    n_rest = 600
    city_of = rng.choice(["Bengaluru", "Mumbai", "Delhi"], n_rest, p=[0.4, 0.3, 0.3])
    prep_mean = np.exp(rng.normal(np.log(13), 0.35, n_rest)) * np.where(rng.random(n_rest) < 0.18, 0.7, 1.0)    # 18% cloud kitchens are faster
    prep_cv = np.where(prep_mean < 11, 0.18, 0.32)
    cap = rng.uniform(8, 30, n_rest)                                                                      # orders per hour a kitchen can absorb
    pop = rng.gamma(0.9, 1.0, n_rest); pop /= pop.sum()
    day = rng.integers(0, DAYS, n_sessions); hr = np.clip(np.round(rng.choice([8, 9, 10, 12, 13, 14, 15, 17, 19, 20, 21, 22, 23], n_sessions, p=np.array([2, 2, 2, 12, 14, 6, 3, 5, 14, 16, 12, 8, 4]) / 100.0)), 0, 23).astype(int)
    ts = START + pd.to_timedelta(day, unit="D") + pd.to_timedelta(hr * 3600 + rng.integers(0, 3600, n_sessions), unit="s")
    wd = ts.dayofweek.values; rid = rng.choice(n_rest, n_sessions, p=pop); city = city_of[rid]
    rain = (rng.random(DAYS) < 0.22)[day] & (rng.random(n_sessions) < 0.8)
    items = 1 + rng.poisson(1.6, n_sessions); dist = np.clip(np.exp(rng.normal(np.log(3.2), 0.55, n_sessions)), 0.3, 12.0)             # restaurant -> customer km
    peak = np.isin(hr, [12, 13, 19, 20, 21]).astype(float)
    # kitchen stress: orders placed recently vs capacity
    load = (peak * 1.2 + 0.4) * (1 + 0.15 * (wd >= 5)) * rng.uniform(0.7, 1.3, n_sessions) * 10
    stress = np.clip(load / cap[rid], 0.2, 3.0)
    supply = np.clip(rng.normal(1.15 - 0.45 * peak - 0.25 * rain + 0.05 * (hr < 11), 0.18, n_sessions), 0.25, 2.0)                      # DEs per active order
    traffic = pd.Series(city).map({"Bengaluru": 1.15, "Mumbai": 1.05, "Delhi": 1.0}).values * (1 + 0.25 * peak) * (1 + 0.2 * rain)
    # true legs (minutes)
    prep = prep_mean[rid] * (1 + 0.07 * (items - 2)) * (0.8 + 0.25 * stress) * np.exp(rng.normal(0, prep_cv[rid]))
    o2a = np.clip(rng.exponential(0.8 + 5.5 * np.clip(1.25 - supply, 0, None) ** 1.2 + 0.4, n_sessions), 0.2, 30)
    reject = rng.random(n_sessions) < (0.04 + 0.10 * peak + 0.08 * rain); o2a = o2a + reject * rng.exponential(3.0, n_sessions)
    de_dist = np.clip(np.exp(rng.normal(np.log(1.1 / np.clip(supply, 0.4, 2.0)), 0.5)), 0.1, 6.0)
    fm = np.clip(de_dist / (22.0 / traffic) * 60 + rng.normal(0, 0.8, n_sessions), 0.5, 40)
    wt = np.clip(prep - (o2a + fm), 0, None)
    lm = np.clip(dist / (21.0 / traffic) * 60 * np.exp(rng.normal(0, 0.18, n_sessions)) + 2.5 + rng.exponential(1.2, n_sessions), 2, 60)             # includes gate-to-door
    o2r = o2a + fm + wt + lm
    # legacy promise: noisy historical average + buffer (Goldilocks)
    hist = np.exp(np.log(o2r) - rng.normal(0.02, 0.12, n_sessions))                                         # legacy only knows an average-like value, built below
    legacy_base = pd.Series(o2r).groupby([rid, hr // 3]).transform("mean").values
    offset = rng.choice([-3, 0, 3], n_sessions, p=[0.10, 0.80, 0.10])
    promise = np.round(legacy_base + 4 + offset)
    # conversion: customers dislike longer promises (randomised offset identifies the effect)
    place_p = expit(1.25 - 0.045 * (promise - 30) - 0.12 * np.log(dist) - 0.2 * rain + 0.1 * (hr >= 19) * 0 + rng.normal(0, 0.15, n_sessions))
    placed = rng.random(n_sessions) < place_p
    late = np.clip(o2r - promise, 0, None)
    contact = rng.random(n_sessions) < expit(-3.0 + 0.16 * np.minimum(late, 25)); cancel = rng.random(n_sessions) < expit(-4.6 + 0.12 * np.minimum(late, 25))
    df = pd.DataFrame({"session_id": [f"S{i:07d}" for i in range(n_sessions)], "ts": ts, "city": city, "restaurant_id": [f"R{r:04d}" for r in rid], "hour": hr, "weekday": wd,
                       "n_items": items, "distance_km": dist.round(2), "rain": rain.astype(int), "kitchen_orders_vs_capacity": stress.round(3), "de_per_order": supply.round(3),
                       "shown_promise_min": promise, "promise_offset_min": offset, "placed": placed.astype(int),
                       "o2a_min": np.where(placed, o2a.round(2), np.nan), "fm_min": np.where(placed, fm.round(2), np.nan), "wt_min": np.where(placed, wt.round(2), np.nan),
                       "lm_min": np.where(placed, lm.round(2), np.nan), "o2r_min": np.where(placed, o2r.round(2), np.nan),
                       "care_contact": np.where(placed, contact, np.nan), "cancelled_after_place": np.where(placed, cancel, np.nan),
                       "_prep_true": prep.round(2), "_rest_prep_mean": prep_mean[rid].round(2)})
    # data-quality defects
    df.loc[df.sample(n=1200, random_state=seed).index, "distance_km"] = np.nan                       # geocoding failures
    df.loc[df[df.placed == 1].sample(n=300, random_state=seed + 1).index, "o2r_min"] = df.o2r_min.max() * 4         # stuck app: delivered flag set hours later
    df = pd.concat([df, df.sample(n=1500, random_state=seed + 2)], ignore_index=True)
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs01"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs01", "sessions.csv.gz"), index=False)
    dd = d.drop_duplicates("session_id"); o = dd[(dd.placed == 1) & (dd.o2r_min < 200)]
    print(len(dd), "sessions | placed", dd.placed.mean().round(3), "| O2R median", o.o2r_min.median().round(1), "P90", o.o2r_min.quantile(.9).round(1))
    print(o[["o2a_min", "fm_min", "wt_min", "lm_min"]].median().round(1).to_dict(), "| late>5 share", ((o.o2r_min - o.shown_promise_min) > 5).mean().round(3))
    print("placed by offset", dd.groupby("promise_offset_min").placed.mean().round(4).to_dict())

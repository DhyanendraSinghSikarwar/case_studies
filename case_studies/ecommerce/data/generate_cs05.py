"""
SYNTHETIC DATA GENERATOR - CASE STUDY 5 (Myntra-style customer promise date with breach control)
================================================================================================
THIS DATA IS SYNTHETIC. Myntra order and logistics data are confidential.

Documented context (Preethi, Sundaram, Tallamraju, arXiv:2105.00315, 2021): promise date = order time + warehouse
(or vendor-procurement) time + shipping time; shipping through hubs to a last-mile centre; 3PL courier partners with
limited visibility; pendency at linehaul and last-mile centres; regional holiday calendars; high revenue days (HRD)
with higher variability and cut-offs not adhered to; a rule-based model with static configured times as the baseline;
breach (delivered after the promised date) to be kept below a business limit; training on recent weeks, test on the
next order day. The paper's BAU levels (baseline accuracy 36.6% / breach 5.6%) are only used as an order of magnitude.

Simulation: ~60 days, ~2,000 orders/day on business-as-usual (BAU) days, ~2.6x on sale days (HRD).
  * 6 warehouses, 60 last-mile centres in three zones (metro, tier-2, remote), lane = (warehouse, centre).
  * Warehouse backlog and centre backlog are hidden AR(1) processes; the model sees only yesterday's noisy reading.
  * Orders: 1-6 items, 12% contain a vendor-procured item (long wait), cut-off at 16:00, 3PL for remote zones mostly.
  * Shipping: distance-based linehaul with hub handling, last-mile time by zone, weekend/holiday deferral,
    3PL stalls (heavy tail), and HRD pressure (higher mean AND higher variance).
  * Target: delivery day offset D = delivery calendar date minus order calendar date (integer days).
Hidden truth (prefix _): realised processing hours, shipping hours, stall flag, true backlogs.

Outputs: data/cs05/orders.csv.gz, data/cs05/centres.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
START = pd.Timestamp("2026-08-03")  # a Monday
DAYS = 60
N_WH, N_C = 6, 60
HRD_DAYS = (14, 15, 16, 46, 47, 48)      # prior sale event (usable as proxy) and the test-period sale event
POST_HRD = (17, 49, 50)
NATIONAL_HOLIDAYS = (12, 29)             # days (Aug 15 falls on day 12; day 29 is an illustrative festival)


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    # --- network ---------------------------------------------------------------------------------------------
    wh_xy = np.array([[19.2, 72.9], [12.9, 77.6], [28.4, 77.0], [22.6, 88.4], [17.4, 78.5], [13.1, 80.3]])
    wh_xy = wh_xy + rng.normal(0, 0.05, wh_xy.shape)
    zone = rng.choice(["metro", "tier2", "remote"], N_C, p=[0.30, 0.45, 0.25])
    c_xy = np.column_stack([rng.uniform(9, 31, N_C), rng.uniform(70, 92, N_C)])
    centres = pd.DataFrame({"centre": np.arange(N_C), "zone": zone, "lat": c_xy[:, 0].round(2), "lon": c_xy[:, 1].round(2)})
    dist = np.sqrt(((c_xy[:, None, :] - wh_xy[None, :, :]) ** 2).sum(2)) * 111 * 1.25     # km, road factor (N_C, N_WH)
    # nearest warehouse is the usual source (fashion has low SKU depth, so 35% are shipped from another one)
    near = dist.argmin(1)
    w_share = rng.dirichlet(np.ones(N_WH) * 4)
    # --- daily backlog processes ----------------------------------------------------------------------------
    hrd = np.zeros(DAYS, bool); hrd[list(HRD_DAYS)] = True
    post = np.zeros(DAYS, bool); post[list(POST_HRD)] = True
    hol = np.zeros(DAYS, bool); hol[list(NATIONAL_HOLIDAYS)] = True
    wh_bl = np.zeros((DAYS, N_WH)); c_bl = np.zeros((DAYS, N_C))
    for d in range(DAYS):
        prev_w = wh_bl[d - 1] if d else np.zeros(N_WH); prev_c = c_bl[d - 1] if d else np.zeros(N_C)
        shock_w = 1.1 * hrd[d] + 0.5 * post[d]; shock_c = 0.8 * hrd[d] + 0.7 * post[d]
        wh_bl[d] = 0.65 * prev_w + rng.normal(0, 0.35, N_WH) + shock_w
        c_bl[d] = 0.60 * prev_c + rng.normal(0, 0.45, N_C) + shock_c + (zone == "remote") * 0.25
    # centre-level regional holidays (known calendar)
    c_hol = rng.random((DAYS, N_C)) < 0.03
    # --- orders ----------------------------------------------------------------------------------------------
    n_day = np.where(hrd, rng.poisson(5200, DAYS), rng.poisson(2000, DAYS))
    n_day = np.where(post, rng.poisson(2800, DAYS), n_day)
    day = np.repeat(np.arange(DAYS), n_day); n = len(day)
    c_pop = rng.dirichlet(np.ones(N_C) * 1.5)
    centre = rng.choice(N_C, n, p=c_pop)
    own = near[centre]
    other = rng.random(n) < 0.35
    wh = np.where(other, rng.choice(N_WH, n, p=w_share), own)
    km = dist[centre, wh]
    z = zone[centre]
    n_items = np.minimum(6, 1 + rng.geometric(0.55, n) - 1 + (rng.random(n) < 0.15))
    n_items = np.maximum(1, n_items)
    vendor = rng.random(n) < (0.10 + 0.04 * hrd[day])
    hour = np.minimum(23.99, np.maximum(0, rng.normal(15.5, 5.0, n))); hour = np.where(rng.random(n) < 0.04, rng.uniform(0, 24, n), hour)
    hour = np.clip(hour, 0, 23.99)
    wd = (START.dayofweek + day) % 7   # 0 Mon ... 6 Sun
    p3pl = np.where(z == "remote", 0.75, np.where(z == "tier2", 0.30, 0.08))
    third = rng.random(n) < p3pl
    # -- hidden state for each order
    bw = wh_bl[day, wh]; bc = c_bl[day, centre]
    pressure = hrd[day] * 1.0 + post[day] * 0.5
    # warehouse processing hours
    cutoff_miss = hour >= 16
    wait_cut = np.where(cutoff_miss, (24 - hour) + 8.0, 0.0)
    # on HRD cut-offs are not adhered to: some pre-cutoff orders also slip
    slip = (hrd[day] & (hour >= 13) & (hour < 16) & (rng.random(n) < 0.35))
    wait_cut = wait_cut + np.where(slip, (24 - hour) + 8.0, 0.0)
    proc = np.exp(rng.normal(np.log(7.0) + 0.14 * bw + 0.07 * (n_items > 1) + 0.04 * (n_items > 3), 0.30 + 0.12 * pressure, n))
    proc = proc + np.where(vendor, rng.gamma(2.0, 20.0, n), 0.0) + wait_cut
    # shipping hours
    hops = 1 + np.ceil(km / 700.0)
    linehaul = km / 60.0 + 6.0 * hops
    lastmile = np.where(z == "metro", 7.0, np.where(z == "tier2", 13.0, 26.0))
    ship = linehaul + lastmile + np.exp(rng.normal(np.log(3.0) + 0.55 * bc, 0.45 + 0.18 * pressure, n)) * (1 + 0.6 * pressure)
    stall = rng.random(n) < (0.015 + 0.035 * third + 0.03 * (z == "remote") + 0.04 * pressure)
    ship = ship + np.where(stall, rng.gamma(2.5, 22.0, n), 0.0) + np.where(third, rng.gamma(2.0, 4.0, n), 0.0)
    # delivery timestamp with weekday/holiday deferral; deliveries only 09:00-21:00
    start = day * 24.0 + hour
    t = start + proc + ship
    for _ in range(3):
        dd = np.floor(t / 24).astype(int); hh = t - dd * 24
        wdd = (START.dayofweek + dd) % 7
        dd_c = np.minimum(dd, DAYS - 1)
        blocked = (wdd == 6) | np.isin(dd, NATIONAL_HOLIDAYS) | (c_hol[dd_c, centre] & (dd < DAYS))
        t = np.where(blocked, (dd + 1) * 24.0 + 10.0, t)
        late = (hh >= 21) & ~blocked
        t = np.where(late, (dd + 1) * 24.0 + 10.0, t)
        early = (hh < 9) & ~blocked
        t = np.where(early, dd * 24.0 + 10.0, t)
    D = np.floor(t / 24).astype(int) - day
    # --- observed features -------------------------------------------------------------------------------------
    prev_w = np.where(day[:, None] > 0, wh_bl[np.maximum(day - 1, 0)], 0)[np.arange(n), wh]
    prev_c = np.where(day > 0, c_bl[np.maximum(day - 1, 0), centre], 0.0)
    orders = pd.DataFrame({
        "order_id": np.arange(n), "order_ts": START + pd.to_timedelta(day * 86400 + (hour * 3600).astype(int), unit="s"),
        "day": day, "hour": hour.round(2), "weekday": wd, "is_national_holiday": hol[day].astype(int),
        "is_hrd": hrd[day].astype(int), "is_post_hrd": post[day].astype(int),
        "warehouse": wh, "centre": centre, "zone": z, "distance_km": km.round(0), "n_items": n_items,
        "vendor_item": vendor.astype(int), "carrier_3pl": third.astype(int),
        "pend_wh_prev_day": (prev_w + rng.normal(0, 0.15, n)).round(3), "pend_centre_prev_day": (prev_c + rng.normal(0, 0.15, n)).round(3),
        "centre_holiday_next2": 0,
        "planned_volume_ratio": np.where(hrd[day], rng.normal(2.6, 0.2, n), np.where(post[day], 1.4, 1.0)).round(2),
        "delivery_days": D, "delivery_ts": START + pd.to_timedelta((t * 3600).astype(np.int64), unit="s"),
        "_proc_hours": proc.round(1), "_ship_hours": ship.round(1), "_stall": stall.astype(int),
        "_wh_backlog": bw.round(3), "_centre_backlog": bc.round(3),
    })
    # centre regional holiday known for the next two days after the order
    h2 = np.zeros(n, int)
    for k in (1, 2):
        dk = np.minimum(day + k, DAYS - 1); h2 |= c_hol[dk, centre].astype(int)
    orders["centre_holiday_next2"] = h2
    # defects: delivered orders after the data cut-off are unobserved (right-censoring) and a few bad timestamps
    orders = orders.drop(columns=[])
    bad = rng.choice(n, 150, replace=False); orders.loc[bad, "delivery_days"] = np.nan
    dupl = orders.sample(n=400, random_state=seed)
    orders = pd.concat([orders, dupl], ignore_index=True)
    wr = rng.choice(len(orders), 60, replace=False); orders.loc[wr, "distance_km"] = orders.loc[wr, "distance_km"] * 100   # unit error
    return orders, centres


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs05"), exist_ok=True)
    o, c = generate(); o.to_csv(os.path.join(here, "cs05", "orders.csv.gz"), index=False); c.to_csv(os.path.join(here, "cs05", "centres.csv.gz"), index=False)
    print(len(o), o.delivery_days.describe().round(2).to_dict())

"""
SYNTHETIC DATA GENERATOR - CASE STUDY 3 (Instamart-style dark-store demand PLANNING and PICKING)
===============================================================================================
THIS DATA IS SYNTHETIC. Dark-store inventory and picker logs are confidential.

Documented context (Swiggy Bytes, May 2023 and Jul 2024): pods plan demand k days ahead, a second model adds a buffer for
forecast error and vendor fill rate, business sets availability and wastage targets by category, sales are censored by
stock-outs, hourly sales exist for many SKUs, "6-7 pods form a cluster". Picking: free pickers get orders round-robin;
the proposal batches up to 2 similar orders when free pickers are fewer than unassigned orders.

PART A - planning (focus: ordering policy, availability vs wastage, perishability, offline metric alignment)
  48 pods (8 clusters of 6) x 120 SKUs (6 categories, shelf life 1 / 2 / 3 days or non-perishable) x 84 days.
  True demand = Poisson(gamma-mixed rate) drawn hour by hour (16 open hours). Stock is tracked by age (FIFO), received units
  expire at their shelf life. A LEGACY ordering rule (trailing 14-day mean of SALES x a category buffer) runs in the log;
  vendor short-shipments reduce received units. Observed: opening stock, units sold, availability share, wasted units,
  hourly sales. Hidden truth: _true_demand, _lost_sales and the hourly demand (used by a counterfactual replay).
PART B - picking: order log for 6 pods x 14 days (arrival time, items, zones, weight) plus a discrete-event simulator
  of pickers with FIFO assignment (round-robin) or batching of up to 2 orders by zone similarity.

Outputs: data/cs03/pod_sku_days.csv.gz, hourly_sales.npz, sku_master.csv.gz, pick_orders.csv.gz
"""
import os
import heapq
import numpy as np
import pandas as pd

SEED = 42
START = pd.Timestamp("2026-02-02"); DAYS = 84
N_PODS, N_SKU, PER_CLUSTER = 48, 120, 6
OPEN_H = 16
INTRADAY = np.array([0.02, 0.03, 0.04, 0.05, 0.05, 0.06, 0.06, 0.07, 0.07, 0.06, 0.06, 0.06, 0.07, 0.09, 0.11, 0.10]); INTRADAY /= INTRADAY.sum()
# name, shelf life (days; 999 = non-perishable), median price, gross margin share, demand dispersion r, mean units/pod/day, availability target
CATS = [("Bakery and ready-to-eat", 1, 80, 0.30, 6, 14.0, 0.85), ("Fresh produce", 2, 60, 0.25, 8, 12.0, 0.90), ("Dairy and eggs", 3, 70, 0.18, 10, 12.0, 0.93),
        ("Packaged food", 999, 120, 0.20, 12, 6.0, 0.97), ("Snacks and beverages", 999, 55, 0.22, 12, 9.0, 0.97), ("Home and personal care", 999, 220, 0.28, 5, 2.5, 0.95)]
CAT_NAMES = [c[0] for c in CATS]
LEGACY_BUFFER = np.array([1.25, 1.20, 1.15, 1.10, 1.10, 1.10])
GOODWILL = 0.50          # extra cost of a lost sale (customer goodwill) as a share of price
HOLD = 0.004             # daily holding cost as a share of unit cost


def simulate(H, T, L, nonper, fillu, collect_hourly=False):
    """Replay inventory with FIFO ageing. H: true hourly demand [N,D,16]; T: order-up-to levels [N,D] or callable(d, sold_so_far);
    L: shelf life in days (int, capped at 3 for perishables); nonper: bool; fillu: vendor fill factor [N,D]."""
    N, D, _ = H.shape; st = np.zeros((N, 4)); rows = np.arange(N); per_rows = np.where(~nonper)[0]; Lp = L[per_rows].astype(int)
    out = {k: np.zeros((N, D)) for k in ("opening", "ordered", "received", "sold", "avail", "wasted", "lost")}; sold_hist = out["sold"]
    hourly = np.zeros((N, D, OPEN_H), np.int16) if collect_hourly else None
    for d in range(D):
        new = np.zeros_like(st); new[:, 1:] = st[:, :-1]; new[nonper, 3] += st[nonper, 3]
        w = new[per_rows, Lp].copy(); new[per_rows, Lp] = 0; out["wasted"][per_rows, d] = w
        tgt = T(d, sold_hist) if callable(T) else T[:, d]
        order = np.maximum(np.ceil(tgt) - new.sum(1), 0); recv = np.floor(order * fillu[:, d] + 0.5); new[:, 0] += recv
        out["opening"][:, d] = new.sum(1); out["ordered"][:, d] = order; out["received"][:, d] = recv
        for h in range(OPEN_H):
            dh = H[:, d, h].astype(float); tot = new.sum(1); sell = np.minimum(tot, dh)
            out["avail"][:, d] += np.where(dh > 0, np.minimum(tot / np.maximum(dh, 1), 1.0), (tot > 0).astype(float))
            rem = sell.copy()
            for a in (3, 2, 1, 0):
                take = np.minimum(new[:, a], rem); new[:, a] -= take; rem -= take
            out["sold"][:, d] += sell
            if collect_hourly: hourly[:, d, h] = sell
        out["lost"][:, d] = H[:, d, :].sum(1) - out["sold"][:, d]; st = new
    out["avail"] /= OPEN_H
    if collect_hourly: out["hourly"] = hourly
    return out


def oneday_truth(H, T):
    """Counterfactual for one day with starting stock = T (no carry-over): true sold, availability share, leftover."""
    cum = np.cumsum(H, axis=-1).astype(float); prev = cum - H; Tn = np.asarray(T, float)[..., None]
    sb = np.maximum(Tn - prev, 0); frac = np.where(H > 0, np.minimum(sb / np.maximum(H, 1), 1.0), (sb > 0).astype(float))
    sold = np.minimum(cum[..., -1], np.asarray(T, float)); return sold, frac.mean(-1), np.asarray(T, float) - sold


def generate(seed=SEED):
    rng = np.random.default_rng(seed); N = N_PODS * N_SKU
    sku_cat = np.repeat(np.arange(6), N_SKU // 6); cat_n = np.tile(sku_cat, N_PODS)       # category per row
    Lc = np.array([c[1] for c in CATS]); L_sku = Lc[sku_cat]; L_row = np.tile(L_sku, N_PODS); nonper = L_row > 100; Lcap = np.where(nonper, 3, L_row)
    price_sku = np.round(np.array([c[2] for c in CATS])[sku_cat] * np.exp(rng.normal(0, 0.45, N_SKU)), 0); price_sku = np.maximum(price_sku, 10)
    margin_sku = np.array([c[3] for c in CATS])[sku_cat] * np.exp(rng.normal(0, 0.15, N_SKU)); margin_sku = np.clip(margin_sku, 0.08, 0.45)
    cost_sku = np.round(price_sku * (1 - margin_sku), 1)
    base_sku = np.array([c[5] for c in CATS])[sku_cat] * np.exp(rng.normal(0, 0.6, N_SKU) - 0.18); r_sku = np.array([c[4] for c in CATS])[sku_cat].astype(float)
    pod_size = np.exp(rng.normal(0, 0.35, N_PODS) - 0.06); cluster = np.arange(N_PODS) // PER_CLUSTER; n_cl = cluster.max() + 1
    pod_sku_re = np.exp(rng.normal(0, 0.2, (N_PODS, N_SKU)))
    base = (pod_size[:, None] * base_sku[None, :] * pod_sku_re)                            # [pod, sku]
    dates = START + pd.to_timedelta(np.arange(DAYS), unit="D"); dow = dates.dayofweek.values
    dow_f = np.array([0.95, 0.93, 0.95, 0.98, 1.05, 1.15, 1.12])[dow]
    fest = np.zeros(DAYS, int); fest[[20, 47]] = 1; fest_f = 1 + 0.30 * fest
    rain_mm = np.where(rng.random((n_cl, DAYS)) < 0.25, rng.gamma(2, 6, (n_cl, DAYS)), 0.0); rain_fc = rain_mm * np.exp(rng.normal(0, 0.35, rain_mm.shape))
    rain_eff = np.array([0.004, 0.003, 0.002, 0.001, 0.003, 0.0])      # +x per mm for each category
    shock = np.exp(rng.normal(0, 0.06, (n_cl, DAYS)))
    promo = (rng.random((N_PODS, N_SKU, DAYS)) < 0.03)
    trend = 1 + 0.0012 * np.arange(DAYS)
    mu = (base[:, :, None] * dow_f[None, None, :] * fest_f[None, None, :] * trend[None, None, :] * (1 + 0.4 * promo)
          * (1 + rain_eff[sku_cat][None, :, None] * rain_mm[cluster][:, None, :]) * shock[cluster][:, None, :])
    mu = mu.reshape(N, DAYS)
    rr = np.tile(r_sku, N_PODS)[:, None]
    lam = mu * rng.gamma(rr, 1.0 / rr, (N, DAYS))
    H = rng.poisson(lam[:, :, None] * INTRADAY[None, None, :]).astype(np.int16)           # true hourly demand
    # vendor fill: SKU reliability, short-shipment factor
    p_short = np.tile(rng.beta(2, 25, N_SKU), N_PODS)[:, None]; fillu = np.where(rng.random((N, DAYS)) < p_short, rng.uniform(0.3, 0.9, (N, DAYS)), 1.0)
    buf = LEGACY_BUFFER[cat_n][:, None]; mu_prior = mu[:, :14].mean(1)

    def legacy(d, sold):
        m = mu_prior if d < 14 else sold[:, d - 14:d].mean(1)
        return np.maximum(np.ceil(m * buf[:, 0]), 1)
    sim = simulate(H, legacy, Lcap, nonper, fillu, collect_hourly=True)
    pod = np.repeat(np.arange(N_PODS), N_SKU); sku = np.tile(np.arange(N_SKU), N_PODS)
    df = pd.DataFrame({"row_id": np.arange(N * DAYS), "pod_id": np.repeat(pod, DAYS), "cluster_id": np.repeat(cluster[pod], DAYS), "sku_id": np.repeat(sku, DAYS), "day": np.tile(np.arange(DAYS), N)})
    df["date"] = START + pd.to_timedelta(df.day, unit="D"); df["category"] = np.array(CAT_NAMES)[np.repeat(sku_cat[sku], DAYS)]
    df["shelf_life_days"] = np.repeat(L_row, DAYS); df["price_inr"] = np.repeat(price_sku[sku], DAYS); df["unit_cost_inr"] = np.repeat(cost_sku[sku], DAYS)
    df["promo"] = promo.reshape(-1).astype(int); df["festival"] = fest[df.day.values]; df["rain_forecast_mm"] = np.round(rain_fc[df.cluster_id.values, df.day.values], 1)
    df["po_qty"] = sim["ordered"].reshape(-1).astype(int); df["received_qty"] = sim["received"].reshape(-1).astype(int); df["opening_stock"] = sim["opening"].reshape(-1).astype(int)
    df["units_sold"] = sim["sold"].reshape(-1).astype(int); df["avail_share"] = np.round(sim["avail"].reshape(-1), 4); df["wasted_units"] = sim["wasted"].reshape(-1).astype(int)
    df["_true_demand"] = H.sum(2).reshape(-1).astype(int); df["_lost_sales"] = sim["lost"].reshape(-1).astype(int)
    sku_master = pd.DataFrame({"sku_id": np.arange(N_SKU), "category": np.array(CAT_NAMES)[sku_cat], "shelf_life_days": L_sku, "price_inr": price_sku, "unit_cost_inr": cost_sku,
                               "target_availability": np.array([c[6] for c in CATS])[sku_cat], "_vendor_short_prob": np.round(p_short[:N_SKU, 0], 3)})
    # data-quality defects (applied to the delivered table only; hourly array stays aligned by row_id)
    drop_pod = (df.pod_id == 17) & df.day.isin([30, 31]); df = df[~drop_pod]
    df.loc[rng.random(len(df)) < 0.008, "avail_share"] = np.nan
    glitch = (rng.random(len(df)) < 0.002) & (df.units_sold > 0); df.loc[glitch, "opening_stock"] = 0
    dup = df.sample(frac=0.003, random_state=seed); df = pd.concat([df, dup], ignore_index=True)
    truth = dict(H=H, mu=mu, L=Lcap, nonper=nonper, fillu=fillu, cat_n=cat_n, pod=pod, sku=sku, cluster=cluster, hourly=sim["hourly"], sku_master=sku_master)
    return df, truth


# ----------------------------------------------------------------------------------------------- PART B: picking
ZONES = 10; SETUP, T_ITEM, T_ZONE, SORT, PACK = 20.0, 10.0, 24.0, 10.0, 18.0
PICK_RATE = np.array([0.03, 0.03, 0.03, 0.04, 0.05, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.07, 0.08, 0.10, 0.11, 0.10]); PICK_RATE /= PICK_RATE.sum()


def gen_orders(rng, n_orders=700):
    """One pod-day of orders: arrival second, items, zone bitmask, weight."""
    hour = rng.choice(OPEN_H, n_orders, p=PICK_RATE); arr = np.sort(hour * 3600 + rng.uniform(0, 3600, n_orders))
    items = 1 + rng.negative_binomial(2.5, 2.5 / (2.5 + 4.2), n_orders); mission = rng.integers(0, 4, n_orders)   # four basket 'missions'
    prefs = np.array([[.28, .22, .06, .04, .04, .06, .06, .08, .08, .08], [.04, .06, .26, .22, .06, .06, .10, .08, .06, .06], [.06, .06, .06, .06, .26, .22, .08, .08, .06, .06], [.08, .06, .06, .06, .06, .06, .24, .20, .08, .10]])
    masks = np.zeros(n_orders, int); nz = np.zeros(n_orders, int)
    for i in range(n_orders):
        zs = rng.choice(ZONES, min(items[i], 12), p=prefs[mission[i]]); m = 0
        for z in zs: m |= 1 << int(z)
        masks[i] = m; nz[i] = bin(m).count("1")
    weight = np.round(items * 0.35 * np.exp(rng.normal(0, 0.35, n_orders)), 2)
    return dict(arr=arr, items=items, mask=masks, nz=nz, weight=weight, noise=np.exp(rng.normal(0, 0.2, n_orders)))


def _jac(a, b): return bin(a & b).count("1") / max(bin(a | b).count("1"), 1)


def sim_picking(o, K, theta=None, cap_items=14, cap_weight=12.0, speed=None):
    """Discrete-event picking. theta=None: one order per picker, FIFO. Else batch up to 2 when free pickers < unassigned orders,
    partner = most similar of the next 8 queued orders with zone Jaccard >= theta and item/weight caps."""
    n = len(o["arr"]); speed = np.ones(K) if speed is None else speed; heap = [(0.0, k) for k in range(K)]; heapq.heapify(heap)
    arr, items, mask, nz, wt, noise = o["arr"], o["items"], o["mask"], o["nz"], o["weight"], o["noise"]
    assign = np.zeros(n); ready = np.zeros(n); batched = np.zeros(n, bool); err = np.zeros(n); busy = 0.0; i = 0; queue = []; rr = np.random.default_rng(7).random(n)
    while i < n or queue:
        tf, k = heapq.heappop(heap)
        t = max(tf, arr[queue[0]]) if queue else max(tf, arr[i])
        while i < n and arr[i] <= t: queue.append(i); i += 1
        free = 1 + sum(1 for x, _ in heap if x <= t); a = queue.pop(0); partner = None
        if theta is not None and len(queue) >= free and len(queue) > 0:
            best = -1.0
            for q in queue[:8]:
                if items[a] + items[q] > cap_items or wt[a] + wt[q] > cap_weight: continue
                j = _jac(mask[a], mask[q])
                if j >= theta and j > best: best, partner = j, q
            if partner is not None: queue.remove(partner)
        if partner is None:
            dur = (SETUP + T_ITEM * items[a] + T_ZONE * nz[a] + PACK) * noise[a] * speed[k]; assign[a] = t; ready[a] = t + dur; err[a] = float(rr[a] < 0.004)
        else:
            uz = bin(mask[a] | mask[partner]).count("1"); dur = (SETUP + SORT + T_ITEM * (items[a] + items[partner]) + T_ZONE * uz + 2 * PACK) * 0.5 * (noise[a] + noise[partner]) * speed[k]
            for q in (a, partner): assign[q] = t; ready[q] = t + dur; batched[q] = True; err[q] = float(rr[q] < 0.004 + 0.012 * (1 - _jac(mask[a], mask[partner])))
        busy += dur; heapq.heappush(heap, (t + dur, k))
    return dict(assign_wait=assign - arr, order_to_ready=ready - arr, batched=batched, error=err, busy=busy, pick_dur=ready - assign)


def generate_picking(seed=SEED, pods=6, days=14, K=5):
    rng = np.random.default_rng(seed + 1); rows = []
    for p in range(pods):
        speed = np.exp(rng.normal(0, 0.12, K))
        for d in range(days):
            o = gen_orders(rng, int(rng.normal(700, 60))); s = sim_picking(o, K, None, speed=speed)
            rows.append(pd.DataFrame({"pod_id": p, "day": d, "order_in_day": np.arange(len(o["arr"])), "arrival_sec": o["arr"].round(1), "n_items": o["items"], "n_zones": o["nz"], "zone_mask": o["mask"],
                                      "weight_kg": o["weight"], "assign_wait_sec": s["assign_wait"].round(1), "order_to_ready_sec": s["order_to_ready"].round(1), "pick_pack_sec": s["pick_dur"].round(1)}))
    return pd.concat(rows, ignore_index=True)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs03"), exist_ok=True)
    d, tr = generate(); d.to_csv(os.path.join(here, "cs03", "pod_sku_days.csv.gz"), index=False)
    np.savez_compressed(os.path.join(here, "cs03", "hourly_sales.npz"), hourly=tr["hourly"]); tr["sku_master"].to_csv(os.path.join(here, "cs03", "sku_master.csv.gz"), index=False)
    po = generate_picking(); po.to_csv(os.path.join(here, "cs03", "pick_orders.csv.gz"), index=False)
    print(len(d), "rows | availability", d.avail_share.mean().round(3), "| fill", (d.received_qty.sum() / d.po_qty.sum()).round(3), "| orders", len(po), "| median order-to-ready", po.order_to_ready_sec.median().round(0))

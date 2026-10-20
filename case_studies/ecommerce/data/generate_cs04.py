"""
SYNTHETIC DATA GENERATOR - CASE STUDY 4 (Swiggy Instamart-style delivery-executive assignment and batching)
==========================================================================================================
THIS DATA IS SYNTHETIC. Swiggy's order, rider and route data are confidential.

Documented context (Swiggy Bytes 2019 and 2022): orders come from dark stores (depots) to customers; delivery
executives (DEs) are shared across stores; the system re-plans every few seconds on a rolling horizon; time
predictions (first mile, last mile, wait) feed an optimiser. Scale and promise slots here are OUR assumptions.

Simulation: one 9 km x 9 km zone, 6 dark stores, 40 housing clusters (customers sit in clusters, which is what makes
batching possible), 30 independent evening-peak days of orders (3 hours each), a fleet of DEs that start near stores.
Per order we store the pick-and-pack time actually taken (hidden) and standard-normal noise draws used to turn it
into a predicted ready time and to perturb actual travel time (hidden truth, prefixed _).

Outputs: data/cs04/orders.csv.gz, stores.csv, clusters.csv, riders_start.csv.gz (the notebook writes them)
"""
import os
import numpy as np
import pandas as pd

SEED = 42
ZONE = 9.0; N_STORES = 6; N_CLUSTERS = 40; N_DAYS = 30; HORIZON_MIN = 180; N_RIDERS = 62
PROMISE_MIN = 25.0
RATE_PROFILE = np.array([0.75, 0.9, 1.05, 1.2, 1.35, 1.45, 1.4, 1.2, 1.05, 0.9, 0.8, 0.7])   # 12 slots of 15 min
MEAN_ORDERS = 560


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    st_xy = np.column_stack([rng.uniform(1.5, ZONE - 1.5, N_STORES), rng.uniform(1.5, ZONE - 1.5, N_STORES)])
    # keep stores at least 2.2 km apart (redraw)
    for _ in range(200):
        d = np.sqrt(((st_xy[:, None] - st_xy[None]) ** 2).sum(-1)) + np.eye(N_STORES) * 99
        i = np.argmin(d.min(1))
        if d.min() >= 2.2: break
        st_xy[i] = rng.uniform(1.5, ZONE - 1.5, 2)
    stores = pd.DataFrame({"store": np.arange(N_STORES), "x_km": st_xy[:, 0].round(3), "y_km": st_xy[:, 1].round(3), "demand_weight": rng.dirichlet(np.full(N_STORES, 6.0)).round(4), "_pack_mean_min": rng.uniform(3.6, 5.8, N_STORES).round(2)})
    cl_xy = np.column_stack([rng.uniform(0.3, ZONE - 0.3, N_CLUSTERS), rng.uniform(0.3, ZONE - 0.3, N_CLUSTERS)])
    clusters = pd.DataFrame({"cluster": np.arange(N_CLUSTERS), "x_km": cl_xy[:, 0].round(3), "y_km": cl_xy[:, 1].round(3), "size_weight": rng.dirichlet(np.full(N_CLUSTERS, 2.5)).round(4)})
    # store -> cluster choice probabilities: nearer clusters more likely (catchment ~3 km)
    dsc = np.sqrt(((st_xy[:, None] - cl_xy[None]) ** 2).sum(-1)); P = np.exp(-dsc / 1.6) * clusters.size_weight.values[None]; P[dsc > 4.5] = 0; P /= P.sum(1, keepdims=True)
    rows = []; riders = []; oid = 0
    for day in range(N_DAYS):
        drng = np.random.default_rng(np.random.SeedSequence([seed, day]))
        lam = RATE_PROFILE * MEAN_ORDERS * drng.uniform(0.9, 1.1) / RATE_PROFILE.sum()   # orders per 15-min slot
        n_slot = drng.poisson(lam)
        t = np.concatenate([drng.uniform(k * 15, (k + 1) * 15, n) for k, n in enumerate(n_slot)]); t.sort(); n = len(t)
        s = drng.choice(N_STORES, n, p=stores.demand_weight.values / stores.demand_weight.sum())
        c = np.array([drng.choice(N_CLUSTERS, p=P[k]) for k in s])
        cxy = cl_xy[c] + drng.normal(0, 0.28, (n, 2))
        pack = np.maximum(1.0, stores._pack_mean_min.values[s] * np.exp(drng.normal(-0.5 * 0.35 ** 2, 0.35, n)))
        items = np.minimum(1 + drng.poisson(3.2, n), 25); weight = np.round(np.minimum(items * drng.uniform(0.15, 0.6, n), 14), 2)
        for i in range(n):
            rows.append((day, oid, round(t[i], 2), s[i], c[i], round(cxy[i, 0], 3), round(cxy[i, 1], 3), items[i], weight[i], PROMISE_MIN, round(pack[i], 2), drng.normal(), drng.normal()))
            oid += 1
        base = st_xy[drng.choice(N_STORES, N_RIDERS)] + drng.normal(0, 0.6, (N_RIDERS, 2))
        for r in range(N_RIDERS): riders.append((day, r, round(float(np.clip(base[r, 0], 0, ZONE)), 3), round(float(np.clip(base[r, 1], 0, ZONE)), 3)))
    orders = pd.DataFrame(rows, columns=["day", "order_id", "t_min", "store", "cluster", "cust_x_km", "cust_y_km", "n_items", "weight_kg", "promise_min", "_pack_min", "_z_pack", "_z_speed"])
    riders = pd.DataFrame(riders, columns=["day", "rider", "x_km", "y_km"])
    # data-quality defects: duplicated retry rows, wrong coordinates, zero pack times
    rng2 = np.random.default_rng(seed + 1)
    dup = orders.sample(frac=0.015, random_state=seed)
    orders = pd.concat([orders, dup], ignore_index=True).sort_values(["day", "t_min"], kind="stable").reset_index(drop=True)
    bad = rng2.choice(len(orders), int(0.008 * len(orders)), replace=False)
    orders.loc[bad, "cust_x_km"] = orders.loc[bad, "cust_x_km"] + rng2.choice([-1, 1], len(bad)) * rng2.uniform(9, 20, len(bad))
    z = rng2.choice(len(orders), int(0.004 * len(orders)), replace=False); orders.loc[z, "_pack_min"] = 0.0
    return orders, stores, clusters, riders


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs04"), exist_ok=True)
    o, s, c, r = generate(); o.to_csv(os.path.join(here, "cs04", "orders.csv.gz"), index=False); s.to_csv(os.path.join(here, "cs04", "stores.csv"), index=False)
    c.to_csv(os.path.join(here, "cs04", "clusters.csv"), index=False); r.to_csv(os.path.join(here, "cs04", "riders_start.csv.gz"), index=False)
    print(len(o), "orders |", o.groupby("day").size().describe()[["mean", "min", "max"]].round(0).to_dict())

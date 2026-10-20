import itertools, numpy as np, pandas as pd
from scipy.optimize import linear_sum_assignment

KMIN = 1.3 / (20 / 60)          # minutes per straight-line km (20 km/h, 1.3 detour factor)
PICK_SVC, DROP_SVC, SPEED_SD = 1.0, 2.0, 0.12
W_FM, W_WAIT, W_DELAY, W_AGE = 1.5, 1.2, 2.0, 0.4          # assignment-cost weights (rupee-equivalents per minute)
PAY_BASE, PAY_KM, PAY_EXTRA, WAIT_COST, LATE_COST = 20.0, 7.0, 10.0, 1.0, 1.5   # money accounting

def _route(store_xy, cxy, zs, start):
    """Best visiting order (<=3 stops) minimising the sum of drop times; returns order, drop times (arrival), end time, km."""
    best = None
    for perm in itertools.permutations(range(len(cxy))):
        t, p, tot, km, drops = start, store_xy, 0.0, 0.0, {}
        for k in perm:
            d = float(np.hypot(*(cxy[k] - p))); t += d * KMIN * np.exp(SPEED_SD * zs[k]); drops[k] = t; tot += t; km += d * 1.3; t += DROP_SVC; p = cxy[k]
        if best is None or tot < best[0]: best = (tot, perm, drops, t, km, p)
    return best[1], best[2], best[3], best[4], best[5]

def simulate(od, rd, stores_xy, mode="global", jit=False, batch=False, cron=0.5, sigma=0.25, margin=1.0, batch_window=4.0, batch_radius=1.8, tol=3.0, max_batch=3, n_riders=None, bias=0.0):
    n = len(od); t_arr = od.t_min.values; st = od.store.values; cx = od[["cust_x_km", "cust_y_km"]].values; pack = od._pack_min.values; zp = od._z_pack.values; zsp = od._z_speed.values; prom = od.promise_min.values
    act_ready = t_arr + pack; pred_ready = t_arr + pack * np.exp(sigma * zp + bias); due = t_arr + prom
    rxy = rd[["x_km", "y_km"]].values.copy(); R = len(rxy) if n_riders is None else n_riders; rxy = rxy[:R]; free_at = np.zeros(R)
    assigned = np.zeros(n, bool); drop = np.full(n, np.nan); a_t = np.full(n, np.nan); bsize = np.zeros(int(n)); bs = np.zeros(n, int); wait_tot = np.zeros(n); cost_trip = np.zeros(n); fm_km = np.zeros(n)
    nxt = 0; t = 0.0; trips = 0
    while not assigned.all():
        t += cron
        while nxt < n and t_arr[nxt] <= t: nxt += 1
        pend = [i for i in range(nxt) if not assigned[i]]
        free = np.where(free_at <= t)[0]
        if not pend or len(free) == 0: continue
        groups = []
        if mode == "nearest":
            fr = list(free)
            for o in pend:
                if not fr: break
                d = np.hypot(*(rxy[fr] - stores_xy[st[o]]).T); k = int(np.argmin(d)); groups.append(([o], fr.pop(k)))
            todo = groups
        else:
            fmmin = {s: float(np.hypot(*(rxy[free] - stores_xy[s]).T).min()) * KMIN for s in set(st[pend])}
            pend_sorted = sorted(pend, key=lambda i: due[i]); used = set(); G = []
            cache = {}
            def offs(members):
                key = tuple(members)
                if key not in cache:
                    _, dr, _, _, _ = _route(np.zeros(2), cx[members] - stores_xy[st[members[0]]], np.zeros(len(members)), 0.0)
                    cache[key] = np.array([dr[k] for k in range(len(members))])
                return cache[key]
            def pred_drops(members, fm):
                start = max(t + fm, pred_ready[members].max()) + PICK_SVC
                return start, start + offs(members)
            for o in pend_sorted:
                if o in used: continue
                g = [o]; used.add(o)
                if batch:
                    while len(g) < max_batch:
                        s0 = st[o]; fm = fmmin[s0]; best = None
                        for c in pend_sorted:
                            if c in used or st[c] != s0 or abs(pred_ready[c] - pred_ready[o]) > batch_window: continue
                            if min(np.hypot(*(cx[c] - cx[m])) for m in g) > batch_radius: continue
                            mem = g + [c]; _, dr = pred_drops(mem, fm)
                            ok = True
                            for j, m in enumerate(mem):
                                _, d1 = pred_drops([m], fm)
                                if dr[j] - due[m] > max(0.0, d1[0] - due[m]) + tol: ok = False; break
                            if ok:
                                sc = dr.max()
                                if best is None or sc < best[0]: best = (sc, c)
                        if best is None: break
                        g.append(best[1]); used.add(best[1])
                G.append(g)
            elig = []
            for g in G:
                s0 = st[g[0]]; fm = fmmin[s0]; pr = pred_ready[g].max(); start, dr = pred_drops(g, fm)
                ok = True
                if jit:
                    ok = (t + fm + margin >= pr) or (t >= (due[g].min() - (fm + (dr.max() - start) + PICK_SVC + 5.0)))
                if ok: elig.append(g)
            if not elig: continue
            C = np.zeros((len(free), len(elig)))
            for j, g in enumerate(elig):
                s0 = st[g[0]]; fmv = np.hypot(*(rxy[free] - stores_xy[s0]).T) * KMIN; pr = pred_ready[g].max(); age = t - t_arr[g].min()
                start = np.maximum(t + fmv, pr) + PICK_SVC; dr = start[:, None] + offs(g)[None, :]; wait = np.maximum(0.0, pr - (t + fmv)); delay = np.maximum(0, dr - due[g][None, :]).sum(1)
                C[:, j] = W_FM * fmv + W_WAIT * wait + W_DELAY * delay - W_AGE * age
            ri, ci = linear_sum_assignment(C); todo = [(elig[j], int(free[i])) for i, j in zip(ri, ci)]
        for g, r in todo:
            s0 = st[g[0]]; sxy = stores_xy[s0]; fmd = float(np.hypot(*(rxy[r] - sxy))); arrive = t + fmd * KMIN * np.exp(SPEED_SD * zsp[g[0]])
            start = max(arrive, act_ready[g].max()); wait = start - arrive
            perm, dr, end, km, p = _route(sxy, cx[g], zsp[g], start + PICK_SVC)
            for k, o in enumerate(g):
                assigned[o] = True; drop[o] = dr[k]; a_t[o] = t; bs[o] = len(g); wait_tot[o] = wait / len(g)
                cost_trip[o] = (PAY_BASE + PAY_KM * (fmd * 1.3 + km) + PAY_EXTRA * (len(g) - 1) + WAIT_COST * wait) / len(g); fm_km[o] = fmd * 1.3 / len(g)
            free_at[r] = end; rxy[r] = p; trips += 1
    out = od[["day", "order_id", "t_min", "store"]].copy(); out["assign_t"] = a_t; out["drop_t"] = drop; out["total_min"] = drop - t_arr; out["delay_min"] = np.maximum(0, drop - due)
    out["late"] = (drop > due).astype(int); out["o2a_min"] = a_t - t_arr; out["batch_size"] = bs; out["rider_wait_min"] = wait_tot; out["delivery_cost"] = cost_trip; out["cx_cost"] = LATE_COST * out.delay_min; out["fm_km"] = fm_km
    out["total_cost"] = out.delivery_cost + out.cx_cost
    return out

def summarise(o):
    return dict(orders=len(o), late_pct=100 * o.late.mean(), mean_delay=o.delay_min.mean(), p90_total=o.total_min.quantile(0.9), mean_total=o.total_min.mean(), o2a=o.o2a_min.mean(), wait=o.rider_wait_min.sum() / o.batch_size.rdiv(1).sum(), batch_pct=100 * (o.batch_size >= 2).mean(), cpd=o.delivery_cost.mean(), cx=o.cx_cost.mean(), total=o.total_cost.mean(), fm_km=o.fm_km.mean())

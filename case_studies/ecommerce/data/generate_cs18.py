"""
SYNTHETIC DATA GENERATOR - CASE STUDY 18 (Meesho cold-start feeds + Myntra bandit exploration)
=============================================================================================
THIS DATA IS SYNTHETIC. Neither company publishes logs; Meesho's post has no numbers at all.

Documented context (see the reference file, Case Study 18):
  * Meesho: new users give "no second chances"; features are demographics (gender, location), early behaviour
    (clicks, interaction sequences) and user state (login, activity, lifecycle); models progress DemoRec -> ESPM -> CWN
    (cold expert + warm expert blended by a gate). Item labels: sub_category, price_decile.
  * Myntra (arXiv 2309.14046): widgets are added and removed over time (item cold start), LinUCB / linear Thompson
    sampling with delayed batch feedback and a forgetting factor, DPP diversity re-ranking; +0.24% clicks per user over XGBoost.

Part A (new-user cold start): 40,000 new users x 24 sub-categories. Taste = global popularity + cohort effect
  (gender, city tier, region, age band) + individual favourites. Early clicks come from the taste with noise (more noise
  when anonymous). Held-out future clicks are drawn from the true taste.
Part B (widget bandit): 80 widgets over 60 days (30 live at the start, 3 retire and 3 launch every 4 days), 8 widget types,
  8-dim user context, logistic click model with slowly drifting weights and a satiation penalty for repeating a widget type
  on the same page (so diversity has a true value).

Outputs: users, early_events, widgets (CSV.gz) and true_params.npz (hidden truth).
"""
import os
import numpy as np
import pandas as pd

SEED = 42
N_U, N_C = 40_000, 24
N_W, N_TYPES, D_CTX, DAYS, SLOTS = 80, 8, 8, 60, 5
GENDER = np.array(["F", "M"]); REGION = np.array(["North", "South", "East", "West", "Central"]); AGE = np.array(["18-24", "25-34", "35-44", "45+"])


def _softmax(z):
    z = z - z.max(1, keepdims=True); e = np.exp(z); return e / e.sum(1, keepdims=True)


def generate_users(rng):
    g = (rng.random(N_U) > 0.62).astype(int); tier = rng.choice(3, N_U, p=[0.20, 0.35, 0.45]); reg = rng.integers(0, 5, N_U); age = rng.choice(4, N_U, p=[0.28, 0.40, 0.22, 0.10])
    logged = (rng.random(N_U) < 0.55).astype(int)
    pop_logit = rng.normal(0, 0.8, N_C)
    Bg, Bt, Br, Ba = rng.normal(0, 0.55, (2, N_C)), rng.normal(0, 0.45, (3, N_C)), rng.normal(0, 0.40, (5, N_C)), rng.normal(0, 0.30, (4, N_C))
    cohort = pop_logit[None, :] + Bg[g] + Bt[tier] + Br[reg] + Ba[age]
    fav = rng.integers(0, N_C, (N_U, 2)); indiv = rng.normal(0, 0.8, (N_U, N_C)); indiv[np.arange(N_U), fav[:, 0]] += 1.5; indiv[np.arange(N_U), fav[:, 1]] += 0.9
    P = _softmax(cohort + indiv)
    n_early = np.where(rng.random(N_U) < 0.22, 0, np.minimum(1 + rng.negative_binomial(1.5, 1.5 / (1.5 + 4.0), N_U), 25))
    bots = rng.choice(N_U, 80, replace=False); n_early[bots] = rng.integers(150, 300, 80)
    noise_share = np.where(logged == 1, 0.15, 0.35); gp = _softmax(pop_logit[None, :])[0]
    ev = []
    for u in range(N_U):
        n = n_early[u]
        if n == 0: continue
        q = (1 - noise_share[u]) * P[u] + noise_share[u] * gp; cats = rng.choice(N_C, n, p=q / q.sum())
        dwell = np.round(np.exp(rng.normal(2.0 + 1.0 * (P[u][cats] > 1.5 / N_C), 0.6)), 1)
        ev.extend(zip(np.full(n, u), np.arange(n), cats, dwell))
    ev = pd.DataFrame(ev, columns=["user", "seq", "sub_category", "dwell_s"])
    fut = np.array([rng.choice(N_C, 3, p=P[u]) for u in range(N_U)])
    users = pd.DataFrame({"user": np.arange(N_U), "gender": GENDER[g], "city_tier": tier + 1, "region": REGION[reg], "age_band": AGE[age], "logged_in": logged, "n_early_clicks": n_early,
                          "future_cat_1": fut[:, 0], "future_cat_2": fut[:, 1], "future_cat_3": fut[:, 2]})
    miss = rng.random(N_U) < 0.04; users.loc[miss, "region"] = None; users.loc[rng.random(N_U) < 0.04, "age_band"] = None
    ev = pd.concat([ev, ev.sample(frac=0.02, random_state=SEED)], ignore_index=True)       # duplicate-event defect
    return users, ev, dict(P=P, pop_logit=pop_logit)


def generate_bandit(rng):
    typ = rng.integers(0, N_TYPES, N_W); emb = np.eye(N_TYPES)[typ] * 1.0 + rng.normal(0, 0.25, (N_W, N_TYPES)); emb /= np.linalg.norm(emb, axis=1, keepdims=True)
    theta = rng.normal(0, 0.55, (N_W, D_CTX)); base = rng.normal(-3.7, 0.40, N_W)
    start = np.zeros(N_W, int); end = np.full(N_W, DAYS + 1)
    order = rng.permutation(N_W); live0 = order[:30]; pend = list(order[30:]); alive = list(live0); wave = 0
    for d in range(4, DAYS, 4):
        if len(pend) < 3: break
        out = rng.choice(alive, 3, replace=False)                                  # retire 3 random live widgets
        for w in out: end[w] = d; alive.remove(w)
        for _ in range(3):
            w = pend.pop(0); start[w] = d; alive.append(w)
    for w in pend: start[w] = DAYS + 5; end[w] = DAYS + 6                         # never launched
    wid = pd.DataFrame({"widget": np.arange(N_W), "widget_type": typ, "launch_day": start, "retire_day": np.minimum(end, DAYS + 1)})
    return wid, dict(typ=typ, emb=emb, theta=theta, base=base, start=start, end=end)


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    users, ev, tpa = generate_users(rng); wid, tpb = generate_bandit(rng)
    return users, ev, wid, dict(**tpa, **{"b_" + k: v for k, v in tpb.items()})


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs18"), exist_ok=True)
    u, e, w, tp = generate()
    u.to_csv(os.path.join(here, "cs18", "users.csv.gz"), index=False); e.to_csv(os.path.join(here, "cs18", "early_events.csv.gz"), index=False); w.to_csv(os.path.join(here, "cs18", "widgets.csv.gz"), index=False)
    np.savez(os.path.join(here, "cs18", "true_params.npz"), **tp); print(len(u), len(e), len(w), u.n_early_clicks.describe().round(1).to_dict())

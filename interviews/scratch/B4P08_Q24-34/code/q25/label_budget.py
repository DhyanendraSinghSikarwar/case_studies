import math
import numpy as np
from scipy.stats import norm

# 1. sample size for a +/-3 point margin on a proportion (normal approximation)
def n_needed(p, margin, conf):
    z = norm.ppf(0.5 + conf / 2)
    return math.ceil(z * z * p * (1 - p) / margin ** 2)
for conf in (0.90, 0.95):
    print(f"conf {conf:.2f}: p=0.90 -> n={n_needed(0.90, 0.03, conf)}   worst case p=0.50 -> n={n_needed(0.5, 0.03, conf)}")

# 2. simulated population of flagged cases (score >= 0.5 means 'flag'); true label ~ Bernoulli(p_true)
rng = np.random.default_rng(25)
N = 50_000
score = np.clip(rng.beta(5, 1.2, N) * 0.5 + 0.5, 0.5, 1.0)       # flagged cases only
p_true = np.clip(0.55 + 0.9 * (score - 0.5), 0, 0.99)           # real precision rises with score
y = (rng.random(N) < p_true).astype(int)
truth = y.mean()
print(f"flagged N={N}, full-label precision = {truth:.4f}")

bins = np.array([0.5, 0.7, 0.85, 0.95, 1.0001])
stratum = np.digitize(score, bins) - 1
Nh = np.bincount(stratum)
print("stratum sizes", Nh.tolist())

def srs(n, r):
    idx = r.choice(N, n, replace=False)
    p = y[idx].mean(); se = math.sqrt(p * (1 - p) / n * (1 - n / N))
    return p, se

def strat(nh, r):
    # inverse-probability weight = Nh / nh ; estimate = sum(Nh * ph) / N
    est, var = 0.0, 0.0
    for h, k in enumerate(nh):
        idx = r.choice(np.flatnonzero(stratum == h), k, replace=False)
        ph = y[idx].mean(); w = Nh[h] / N
        est += w * ph
        var += w * w * (1 - k / Nh[h]) * ph * (1 - ph) / (k - 1)
    return est, math.sqrt(var)

budget = 600
prop = np.maximum(10, np.round(budget * Nh / N)).astype(int)        # proportional allocation
# score-weighted: more labels where the label is least certain (low-score strata), Neyman-like using a pilot guess of p
pilot = np.array([0.6, 0.75, 0.9, 0.97])
neyman = Nh * np.sqrt(pilot * (1 - pilot)); neyman = np.maximum(10, np.round(budget * neyman / neyman.sum())).astype(int)
print("proportional alloc", prop.tolist(), " neyman-like alloc", neyman.tolist())

z = norm.ppf(0.975)
r = np.random.default_rng(250)
for name, f in (("simple random", lambda: srs(budget, r)), ("stratified proportional", lambda: strat(prop, r)), ("stratified neyman-like", lambda: strat(neyman, r))):
    est, se = f()
    print(f"{name:24s} est {est:.4f}  95% CI [{est - z * se:.4f}, {est + z * se:.4f}]  covers truth: {est - z * se <= truth <= est + z * se}")

# 3. repeat 1000 times: bias, spread, coverage
res = {k: [] for k in ("srs", "prop", "neyman")}
r2 = np.random.default_rng(251)
cov = dict.fromkeys(res, 0)
for _ in range(1000):
    for k, f in (("srs", lambda: srs(budget, r2)), ("prop", lambda: strat(prop, r2)), ("neyman", lambda: strat(neyman, r2))):
        e, se = f(); res[k].append(e); cov[k] += (abs(e - truth) <= z * se)
for k in res:
    a = np.array(res[k]); print(f"{k:7s} mean {a.mean():.4f} sd {a.std():.4f} coverage {cov[k]/1000:.3f}")

# 4. WRONG: label only the stratum that is cheapest (the top scores) and do not reweight
top = np.flatnonzero(stratum == 3)
print(f"biased (top stratum only): {y[top].mean():.4f}  vs truth {truth:.4f}")

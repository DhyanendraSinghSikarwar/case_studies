import numpy as np
from scipy import stats
rng = np.random.default_rng(8)

# 1) The prompt's pooled (per-impression) z-test, recomputed
N = 2_000_000
pc, pt = 0.0400, 0.0405
pool = (pc + pt) / 2
se = np.sqrt(pool * (1 - pool) * 2 / N)
z = (pt - pc) / se
p_naive = 2 * stats.norm.sf(z)
print(f"pooled impression-level z = {z:.2f}, p = {p_naive:.4f}")
assert round(p_naive, 2) == 0.01 and round(z, 2) == 2.54 

# 2) Back out the design effect implied by the user-level p = 0.12
z_user = stats.norm.isf(0.12 / 2)
deff = (z / z_user) ** 2
m = 20
rho = (deff - 1) / (m - 1)
print(f"user-level z for p = 0.12: {z_user:.2f}; implied design effect = {deff:.2f}; implied intra-user correlation = {rho:.3f}")

# 3) A/A simulation (no true effect): 20 impressions per user, user CTRs vary (Beta, mean 4%),
#    intra-user correlation as implied above. 20,000 users per arm, 1,000 experiments.
users, m, sims = 20_000, 20, 1_000
ab = 1 / rho - 1                      # Beta(a, b) with icc = 1 / (a + b + 1)
a_, b_ = 0.04 * ab, 0.96 * ab
rej_naive = rej_user = 0
for _ in range(sims):
    cc = rng.binomial(m, rng.beta(a_, b_, users))
    ct = rng.binomial(m, rng.beta(a_, b_, users))
    Nn = users * m
    xc, xt = cc.sum(), ct.sum()
    pl = (xc + xt) / (2 * Nn)
    zn = (xt / Nn - xc / Nn) / np.sqrt(pl * (1 - pl) * 2 / Nn)
    zu = (ct.mean() - cc.mean()) / np.sqrt(ct.var(ddof=1) / users + cc.var(ddof=1) / users)
    rej_naive += abs(zn) > 1.96
    rej_user += abs(zu) > 1.96
print(f"A/A false-positive rate: impression-level z-test = {rej_naive/sims:.3f}; user-level test = {rej_user/sims:.3f}")
assert rej_naive / sims > 0.15 and 0.03 < rej_user / sims < 0.08

# 4) Delta-method test for the ratio when impressions per user differ (one realistic data set)
users = 100_000
def make(mean):
    imp = rng.poisson(20, users).clip(1)
    ctr = rng.beta(mean * ab, (1 - mean) * ab, users)
    return rng.binomial(imp, ctr), imp
clk_c, imp_c = make(0.0400); clk_t, imp_t = make(0.0405)
def ratio_var(clk, imp):
    r = clk.sum() / imp.sum()
    resid = clk - r * imp
    return r, resid.var(ddof=1) / (len(clk) * imp.mean() ** 2)
r_c, v_c = ratio_var(clk_c, imp_c); r_t, v_t = ratio_var(clk_t, imp_t)
zd = (r_t - r_c) / np.sqrt(v_c + v_t)
Nc, Nt = imp_c.sum(), imp_t.sum()
pl = (clk_c.sum() + clk_t.sum()) / (Nc + Nt)
zn = (r_t - r_c) / np.sqrt(pl * (1 - pl) * (1 / Nc + 1 / Nt))
print(f"same data: impression-level z = {zn:.2f}, delta-method z = {zd:.2f}")
assert abs(zn) > abs(zd)

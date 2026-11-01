# Q12: PSI alert with unchanged AUC (illustrative simulation, seeded, numpy+scipy only)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(12)

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def psi(ref, cur, edges):
    e = np.histogram(ref, edges)[0] / len(ref)
    a = np.histogram(cur, edges)[0] / len(cur)
    e = np.clip(e, 1e-4, None); a = np.clip(a, 1e-4, None)
    return float(np.sum((a - e) * np.log(a / e)))

# PSI by hand on 3 bins: expected 50/30/20, actual 30/30/40
exp, act = np.array([.5, .3, .2]), np.array([.3, .3, .4])
hand = float(np.sum((act - exp) * np.log(act / exp)))
print(f"hand-check PSI = {hand:.4f}")
assert abs(hand - (-0.2*np.log(.6) + 0.2*np.log(2))) < 1e-12 and 0.10 < hand < 0.25

# Fixed "model": score driven by x1, x2 (strong) and weakly by age and city tier
def make(n, age_mean, tier_p):
    age = rng.normal(age_mean, 8, n)
    tier = rng.choice([1, 2, 3], n, p=tier_p)
    x1, x2 = rng.normal(size=n), rng.normal(size=n)
    logit = -1.0 + 1.3 * x1 + 0.9 * x2 + 0.01 * (age - 35) + 0.05 * (tier - 2)
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    return age, tier, x1, x2, y
def score(age, tier, x1, x2):
    return -1.0 + 1.3 * x1 + 0.9 * x2 + 0.01 * (age - 35) + 0.05 * (tier - 2)

ref = make(60000, 35, [.5, .3, .2])
cur = make(60000, 42, [.2, .3, .5])          # older users, more tier-3 cities, same relationship
age_edges = np.quantile(ref[0], np.linspace(0, 1, 11)); age_edges[0], age_edges[-1] = -1e9, 1e9
p_age = psi(ref[0], cur[0], age_edges)
p_city = psi(ref[1], cur[1], np.array([0.5, 1.5, 2.5, 3.5]))
s_ref, s_cur = score(*ref[:4]), score(*cur[:4])
sc_edges = np.quantile(s_ref, np.linspace(0, 1, 11)); sc_edges[0], sc_edges[-1] = -1e9, 1e9
p_score = psi(s_ref, s_cur, sc_edges)
a_ref, a_cur = auc(ref[4], s_ref), auc(cur[4], s_cur)
print(f"PSI age={p_age:.3f} city={p_city:.3f} score={p_score:.3f}")
print(f"AUC reference={a_ref:.3f} current={a_cur:.3f}")
assert p_age > 0.25 and p_city > 0.25 and abs(a_ref - a_cur) < 0.01

# Does the shift matter? Reweight the reference to the NEW age/tier mix and recompute expected AUC
age_bin = lambda a: np.digitize(a, np.quantile(ref[0], np.linspace(0, 1, 11))[1:-1])
cell = lambda a, t: age_bin(a) * 3 + (t - 1)
c_ref, c_cur = cell(ref[0], ref[1]), cell(cur[0], cur[1])
w_cell = np.bincount(c_cur, minlength=30) / len(c_cur) / (np.bincount(c_ref, minlength=30) / len(c_ref))
w = w_cell[c_ref]
def wauc(y, s, w):
    o = np.argsort(s); y, s, w = y[o], s[o], w[o]
    wp, wn = w * (y == 1), w * (y == 0)
    cn = np.cumsum(wn) - wn
    return float(np.sum(wp * cn) / (wp.sum() * wn.sum()))
a_rw = wauc(ref[4], s_ref, w)
print(f"reweighted-reference AUC (expected under new mix) = {a_rw:.3f}; observed current = {a_cur:.3f}")
assert abs(a_rw - a_cur) < 0.01

# Contrast: concept drift with NO input shift (PSI ~ 0) but AUC falls
x1c, x2c = rng.normal(size=60000), rng.normal(size=60000)
agec, tierc = rng.normal(35, 8, 60000), rng.choice([1, 2, 3], 60000, p=[.5, .3, .2])
lg = -1.0 + 0.4 * x1c + 0.9 * x2c                 # x1 matters much less now
yc = (rng.random(60000) < 1 / (1 + np.exp(-lg))).astype(int)
sc = score(agec, tierc, x1c, x2c)
print(f"concept drift contrast: PSI age={psi(ref[0], agec, age_edges):.3f}, AUC={auc(yc, sc):.3f}")
assert psi(ref[0], agec, age_edges) < 0.02 and auc(yc, sc) < a_ref - 0.03

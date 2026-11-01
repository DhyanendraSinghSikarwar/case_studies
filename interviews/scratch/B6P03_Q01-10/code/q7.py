# Q7 loan income 30% missing, defaults 9% vs 4%: median fill vs fill + missing flag (illustrative simulation)
import numpy as np
from scipy.stats import norm, rankdata

# Prompt arithmetic
n_all, n_miss = 50_000, 15_000
d_miss, d_obs = 0.09 * n_miss, 0.04 * (n_all - n_miss)
print(f"missing: {n_miss} rows, defaults {d_miss:.0f}; reported: {n_all-n_miss} rows, defaults {d_obs:.0f}; overall default rate {(d_miss+d_obs)/n_all:.3%}")
assert n_miss / n_all == 0.30 and d_miss == 1350 and d_obs == 1400 and abs((d_miss + d_obs) / n_all - 0.055) < 1e-12
p1, p2 = d_miss / n_miss, d_obs / (n_all - n_miss)
pp = (d_miss + d_obs) / n_all
z = (p1 - p2) / np.sqrt(pp * (1 - pp) * (1 / n_miss + 1 / (n_all - n_miss)))
print(f"two-proportion z for 9% vs 4%: {z:.1f}  (p={2*norm.sf(z):.1e})")
assert z > 15

rng = np.random.default_rng(4)
def sig(x): return 1 / (1 + np.exp(-x))
def fit(A, y, iters=25, ridge=1e-6):
    b = np.zeros(A.shape[1])
    for _ in range(iters):
        p = sig(A @ b); g = A.T @ (p - y); H = (A * (p * (1 - p))[:, None]).T @ A + ridge * np.eye(len(b))
        b -= np.linalg.solve(H, g)
    return b
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def make(n, rng):
    inc = rng.normal(size=n)                          # standardised log-income
    other = rng.normal(size=n)
    lat = rng.normal(size=n)                          # unobserved stress that drives both default and hiding income
    default = rng.random(n) < sig(-3.4 - 0.5 * inc + 0.4 * other + 1.0 * lat)
    miss = rng.random(n) < sig(-1.3 + 1.2 * lat)      # riskier applicants more often leave income blank
    return inc, other, default.astype(float), miss
n = n_all
inc, oth, y, miss = make(n, rng)
print(f"simulated: missing share={miss.mean():.2%}, default rate missing={y[miss].mean():.2%} vs reported={y[~miss].mean():.2%}")
assert 0.25 < miss.mean() < 0.35 and y[miss].mean() > y[~miss].mean() * 1.5

tr = np.arange(n) < 35_000; te = ~tr
med = np.median(inc[tr & ~miss])                      # imputation statistic from the TRAIN fold only
filled = np.where(miss, med, inc)
def design(flag):
    cols = [np.ones(n), filled, oth] + ([miss.astype(float)] if flag else [])
    return np.c_[tuple(cols)]
res = {}
for flag in (False, True):
    A = design(flag); b = fit(A[tr], y[tr]); pr = sig(A[te] @ b)
    res[flag] = (auc(y[te], pr), pr)
    print(f"median fill{' + missing flag' if flag else '              '}: test AUC={res[flag][0]:.4f}")
assert res[True][0] > res[False][0] + 0.01

# Serving bug: the fill still happens but the missing flag is lost on the serving path (always 0)
A_flag = design(True); b = fit(A_flag[tr], y[tr])
bug = A_flag[te].copy(); m_te = miss[te]
bug[:, 3] = 0.0
p_ok = sig(A_flag[te] @ b); p_bug = sig(bug @ b)
print(f"rows with missing income: mean predicted default correct pipeline={p_ok[m_te].mean():.3f}, with lost flag={p_bug[m_te].mean():.3f}, actual={y[te][m_te].mean():.3f}")
print(f"AUC correct={auc(y[te], p_ok):.4f}, with bug={auc(y[te], p_bug):.4f}")
assert abs(p_ok[m_te].mean() - y[te][m_te].mean()) < 0.01 and p_bug[m_te].mean() < p_ok[m_te].mean() - 0.02

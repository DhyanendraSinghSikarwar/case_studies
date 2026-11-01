import numpy as np
from scipy import stats, optimize
rng = np.random.default_rng(7)
cost, price, mu, sd = 4.0, 10.0, 100.0, 20.0
def plan(salvage):
    cu, co = price - cost, cost - salvage
    cr = cu / (cu + co)
    q = mu + stats.norm.ppf(cr) * sd
    return cu, co, cr, q
cu, co, cr, q = plan(2.0)
print(f"salvage 2: underage {cu:.0f}, overage {co:.0f}, critical ratio {cr:.2f}, z {stats.norm.ppf(cr):.4f}, bake {q:.1f}")
assert cr == 0.75 and abs(q - 113.49) < 0.01
cu0, co0, cr0, q0 = plan(0.0)
print(f"salvage 0: overage {co0:.0f}, critical ratio {cr0:.2f}, bake {q0:.1f}")
assert abs(cr0 - 0.6) < 1e-12 and abs(q0 - 105.07) < 0.01
# expected profit by integer Q on a big sample of demand (rounded, non-negative)
D = np.maximum(np.round(rng.normal(mu, sd, 400_000)), 0)
def profit(Q, salvage=2.0):
    return (price * np.minimum(D, Q) + salvage * np.maximum(Q - D, 0) - cost * Q).mean()
best = max(range(80, 140), key=profit)
print(f"best integer Q by simulation {best}; profit at 100: {profit(100):.1f}, at {best}: {profit(best):.1f}")
assert abs(best - 113.5) <= 1.5
# censoring: bake Q, observe sales = min(D, Q); naive plan uses mean/sd of sales
def naive_round(Q, days=365):
    d = rng.normal(mu, sd, days)
    s = np.minimum(d, Q)
    return s, d
Q = 100.0
path = [Q]
for r in range(6):
    s, _ = naive_round(Q)
    Q = s.mean() + stats.norm.ppf(0.75) * s.std()
    path.append(Q)
path = [float(x) for x in path]
print("naive plan path of Q:", [round(x, 1) for x in path])
assert all(abs(x - 100) < 4 for x in path)   # stuck near 100, never finds 113.5
# fix: Tobit-style maximum likelihood with censoring at Q (Q=100 for a year)
Qc = 100.0
d = rng.normal(mu, sd, 365); s = np.minimum(d, Qc); cens = d >= Qc
def nll(th):
    m, ls = th; sg = np.exp(ls)
    return -(stats.norm.logpdf(s[~cens], m, sg).sum() + stats.norm.logsf(Qc, m, sg) * cens.sum())
res = optimize.minimize(nll, [s.mean(), np.log(s.std())], method="Nelder-Mead")
m_hat, s_hat = res.x[0], np.exp(res.x[1])
print(f"sold out on {cens.mean():.0%} of days; naive mean {s.mean():.1f}, sd {s.std():.1f}; censored-MLE mean {m_hat:.1f}, sd {s_hat:.1f}")
assert s.mean() < 95 and 92 < m_hat < 108 and 14 < s_hat < 26
q_fix = m_hat + stats.norm.ppf(0.75) * s_hat
print(f"plan from censored estimate: bake {q_fix:.1f} (true optimum 113.5)")
assert abs(q_fix - 113.5) < 10

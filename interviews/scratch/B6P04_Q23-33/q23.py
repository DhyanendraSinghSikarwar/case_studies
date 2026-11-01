# Q23: 4 variants vs one control, winner at p=0.03 (illustrative simulation, seeded)
import numpy as np
from scipy import stats

rng = np.random.default_rng(23)
K, ALPHA = 4, 0.05
print("Bonferroni threshold:", ALPHA / K, "; family-wise error if each test is run at 5%:", round(1 - 0.95**K, 4))
assert abs(ALPHA / K - 0.0125) < 1e-12 and abs((1 - 0.95**K) - 0.1855) < 1e-3

# Holm with the prompt's p-values: C = 0.03, the other three are above 0.05 (use 0.06, 0.20, 0.50)
p = np.array([0.03, 0.06, 0.20, 0.50])
order = np.argsort(p)
holm_ok = [p[i] <= ALPHA / (K - rank) for rank, i in enumerate(order)]
print("Holm: smallest p 0.03 vs threshold", ALPHA / K, "->", "reject" if holm_ok[0] else "do not reject")
assert not holm_ok[0]

# 1) all four variants are truly identical to control: how often does at least one 'win'?
n, base, reps = 5000, 0.10, 20000
ctrl = rng.binomial(n, base, reps) / n
var = rng.binomial(n, base, (reps, K)) / n
se = np.sqrt(2 * base * (1 - base) / n)
z = (var - ctrl[:, None]) / se
pv = 2 * (1 - stats.norm.cdf(np.abs(z)))
any5 = (pv.min(axis=1) < ALPHA).mean()
anyb = (pv.min(axis=1) < ALPHA / K).mean()
print(f"all-null sims: P(any variant p<0.05)={any5:.3f}  P(any p<0.0125)={anyb:.3f}")
assert 0.14 < any5 < 0.185 and 0.04 < anyb < 0.05   # below 18.55% / 5%: the four tests share one control, so they are positively correlated

# 2) winner's curse: every variant has the SAME small true lift (+0.2 points on a 10% base), best significant one is reported
n2, true = 20000, 0.002
c2 = rng.binomial(n2, base, reps) / n2
v2 = rng.binomial(n2, base + true, (reps, K)) / n2
se2 = np.sqrt(2 * base * (1 - base) / n2)
d2 = v2 - c2[:, None]
p2 = 2 * (1 - stats.norm.cdf(np.abs(d2 / se2)))
best = d2.argmax(axis=1)
sel = p2[np.arange(reps), best] < ALPHA
est = d2[np.arange(reps), best][sel].mean()
print(f"true lift {true*100:.2f} pts; mean estimate of the best significant variant {est*100:.2f} pts (n={sel.sum()} of {reps} sims)")
assert est > 1.5 * true

# 3) a fresh confirmation test of a null winner: only 5% pass again
conf = rng.binomial(n, base, (reps, 2))
zc = (conf[:, 1] - conf[:, 0]) / n / se
print("null winner re-tested alone, P(p<0.05 again) =", round((np.abs(zc) > 1.96).mean(), 3))
assert abs((np.abs(zc) > 1.96).mean() - 0.05) < 0.01

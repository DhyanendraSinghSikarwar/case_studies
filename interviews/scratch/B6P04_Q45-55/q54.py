# Q54: two experiments sharing a hash salt (illustrative simulation of the stated counts)
import numpy as np
from scipy import stats
rng = np.random.default_rng(54)
# stated counts
tab = np.array([[45_000, 5_000],      # row A control:   B control 45,000 | B treatment 5,000 (B only)
                [5_000, 45_000]])     # row A treatment: B control 5,000 (A only) | B treatment 45,000 (both)
assert tab.sum() == 100_000 and tab[1].sum() == 50_000 and tab[:, 1].sum() == 50_000     # each looks 50/50 alone
chi2, p, *_ = stats.chi2_contingency(tab, correction=False)
phi = (tab[0,0]*tab[1,1] - tab[0,1]*tab[1,0]) / np.sqrt(tab.sum(0).prod() * tab.sum(1).prod())
print("independent assignment would give 25,000 per cell. chi-square", round(chi2, 0), "p =", p, " phi =", round(phi, 2))
assert abs(phi - 0.8) < 1e-9
print("P(B treated | A treated) =", tab[1,1]/tab[1].sum(), " P(B treated | A control) =", tab[0,1]/tab[0].sum())
# build users and outcomes: true effects A=+1.0, B=+2.0 (additive), noise sd 10
cells = np.repeat([0, 1, 2, 3], [45_000, 5_000, 5_000, 45_000])        # 0 ctrl/ctrl, 1 B only, 2 A only, 3 both
a = np.isin(cells, [2, 3]); b = np.isin(cells, [1, 3])
y = 50 + 1.0*a + 2.0*b + rng.normal(0, 10, 100_000)
def diff(g):
    d = y[g].mean() - y[~g].mean(); se = np.sqrt(y[g].var()/g.sum() + y[~g].var()/(~g).sum()); return d, 1.96*se
print("naive readout A: %.2f +/- %.2f (true 1.0)   naive readout B: %.2f +/- %.2f (true 2.0)" % (*diff(a), *diff(b)))
assert abs(diff(a)[0] - (1.0 + 0.8*2.0)) < 0.5 and abs(diff(b)[0] - (2.0 + 0.8*1.0)) < 0.5      # a + 0.8 b, b + 0.8 a
# recover with the 2x2 cells (regression on both flags)
X = np.column_stack([np.ones(len(y)), a, b]).astype(float)
beta, *_ = np.linalg.lstsq(X, y, rcond=None); r = y - X@beta
se = np.sqrt(np.diag((r@r/(len(y)-3)) * np.linalg.inv(X.T@X)))
print("joint regression: A %.2f +/- %.2f, B %.2f +/- %.2f" % (beta[1], 1.96*se[1], beta[2], 1.96*se[2]))
assert abs(beta[1]-1.0) < 2*1.96*se[1] and abs(beta[2]-2.0) < 2*1.96*se[2]
print("CI width of A, naive vs joint:", round(2*diff(a)[1], 2), "vs", round(2*1.96*se[1], 2))

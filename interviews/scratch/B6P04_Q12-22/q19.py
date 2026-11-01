# Q19: A/A test with 40 metrics: 3 hits at 5%. Is the platform broken? (simulation)
import numpy as np
from scipy.stats import binom, kstest, ttest_ind

m, a = 40, 0.05
print(f"expected hits by chance = {m * a:.1f}")
p_ge3 = binom.sf(2, m, a)
print(f"P(3 or more hits among 40 independent null metrics) = {p_ge3:.3f}")
print(f"P(exactly 3) = {binom.pmf(3, m, a):.3f}; P(0 hits) = {binom.pmf(0, m, a):.3f}")
assert abs(m * a - 2.0) < 1e-12 and 0.31 < p_ge3 < 0.33

# One A/A run is weak evidence. Run many A/A tests on one metric: p-values should be uniform.
rng = np.random.default_rng(19)
pvals = np.array([ttest_ind(rng.normal(10, 3, 2000), rng.normal(10, 3, 2000)).pvalue for _ in range(3000)])
ks = kstest(pvals, "uniform")
print(f"3000 A/A runs, one metric: false positive rate {np.mean(pvals < 0.05):.3f}; KS test vs uniform p = {ks.pvalue:.2f}")
assert abs(np.mean(pvals < 0.05) - 0.05) < 0.015 and ks.pvalue > 0.01

# Correlated metrics: hits come in clumps (clicks, sessions, pageviews move together)
def hits(corr, reps=4000):
    cov = np.full((m, m), corr); np.fill_diagonal(cov, 1)
    L = np.linalg.cholesky(cov)
    z = rng.standard_normal((reps, m)) @ L.T
    return (np.abs(z) > 1.96).sum(axis=1)
for c in (0.0, 0.5, 0.9):
    h = hits(c)
    print(f"corr {c}: mean hits {h.mean():.2f}, P(>=3) {np.mean(h >= 3):.3f}, P(0 hits) {np.mean(h == 0):.3f}")
h0, h9 = hits(0.0), hits(0.9)
assert abs(h0.mean() - 2.0) < 0.1 and abs(h9.mean() - 2.0) < 0.2 and np.mean(h9 == 0) > np.mean(h0 == 0)

# A faulty platform shows up in repeated runs: a broken variance estimate (SE too small by 30%) gives too many hits
bad = np.mean(np.abs(rng.standard_normal(200_000) / 0.7) > 1.96)
print(f"if the SE were understated by 30%, the false positive rate would be {bad:.3f} (not 0.05)")
assert bad > 0.15
from scipy.stats import norm
n_needed = (norm.isf(0.025) * np.sqrt(0.05 * 0.95) + norm.isf(0.2) * np.sqrt(0.07 * 0.93)) ** 2 / 0.02 ** 2
print(f"run-metric pairs to tell a 5% rate from 7% (one-sample, 80% power): {n_needed:,.0f}")
assert 950 < n_needed < 1100
print("all asserts passed")

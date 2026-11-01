import numpy as np
from scipy import stats
rng = np.random.default_rng(11)

m, alpha = 20, 0.05
print("P(at least one false positive in 20 independent tests) =", round(1 - (1 - alpha) ** m, 4))
assert round(1 - (1 - alpha) ** m, 2) == 0.64

# Simulate: 20 independent null metrics, 20,000 experiments
sims = 20_000
p = rng.uniform(size=(sims, m))                 # null p-values are uniform
any_fp = (p < alpha).any(axis=1).mean()
mean_fp = (p < alpha).sum(axis=1).mean()
print(f"simulated P(any p<0.05) = {any_fp:.3f}; mean number of false positives = {mean_fp:.2f}")
assert abs(any_fp - 0.64) < 0.01 and abs(mean_fp - 1.0) < 0.03

# Correlated metrics (rho = 0.6 between metrics) -> fewer independent chances
rho = 0.6
cov = np.full((m, m), rho) + (1 - rho) * np.eye(m)
zs = rng.multivariate_normal(np.zeros(m), cov, size=sims)
pc = 2 * stats.norm.sf(np.abs(zs))
any_fp_c = (pc < alpha).any(axis=1).mean()
print(f"correlated metrics (rho=0.6): P(any p<0.05) = {any_fp_c:.3f}")
assert any_fp_c < any_fp

# Corrections: the one p = 0.04 among 20
p_obs = 0.04
print("Bonferroni threshold:", alpha / m, "-> significant?", p_obs < alpha / m)
print("Bonferroni-adjusted p:", min(1.0, p_obs * m))
assert p_obs >= alpha / m and min(1.0, p_obs * m) == 0.8

# Family-wise error with Bonferroni and with a pre-registered single primary metric
fw_bonf = (p < alpha / m).any(axis=1).mean()
fw_primary = (p[:, 0] < alpha).mean()
print(f"family-wise error: Bonferroni = {fw_bonf:.3f}; one pre-registered primary = {fw_primary:.3f}")
assert fw_bonf < 0.06 and abs(fw_primary - 0.05) < 0.01

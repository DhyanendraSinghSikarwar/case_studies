import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower
rng = np.random.default_rng(0)

def rejection_rate(delta, n=50, sims=4000):
    rej = 0
    for _ in range(sims):
        x = rng.normal(0, 1, n); y = rng.normal(delta, 1, n)
        rej += stats.ttest_ind(x, y).pvalue < 0.05
    return rej / sims

print(rejection_rate(0.0))   # ~0.052 -> Type I rate (alpha)
pw = rejection_rate(0.5)     # ~0.71  -> power; beta = 1 - pw ~ 0.29
print(pw, 1 - pw)
print(TTestIndPower().power(effect_size=0.5, nobs1=50, alpha=0.05))  # 0.697 (theory)

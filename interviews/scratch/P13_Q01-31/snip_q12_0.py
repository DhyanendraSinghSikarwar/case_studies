import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower

es = proportion_effectsize(0.11, 0.10)            # Cohen's h, 0.0326
n = NormalIndPower().solve_power(es, power=0.8, alpha=0.05, ratio=1, alternative='two-sided')
print(round(es, 4), int(np.ceil(n)))              # 0.0326 14745

# by hand
p1, p2 = 0.10, 0.11; za, zb = stats.norm.ppf(0.975), stats.norm.ppf(0.8)
print(int(np.ceil((za + zb)**2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)**2)))   # 14749

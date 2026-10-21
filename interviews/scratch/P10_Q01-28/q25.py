import numpy as np
from scipy.stats import ttest_ind
rng = np.random.default_rng(0)
a = rng.lognormal(3, 1, 20000)
b = rng.lognormal(3, 1, 20000)          # no true effect
b[:3] = 200_000                          # three whale orders land in treatment
cap = np.quantile(np.r_[a, b], 0.999)    # same cap for both arms
for name, (x, y) in {"raw": (a, b),
                     "capped at 99.9th pct": (np.minimum(a, cap), np.minimum(b, cap)),
                     "log1p": (np.log1p(a), np.log1p(b))}.items():
    r = ttest_ind(y, x, equal_var=False)
    print(f"{name:22s} diff={y.mean()-x.mean():8.2f} p={r.pvalue:.3f}")

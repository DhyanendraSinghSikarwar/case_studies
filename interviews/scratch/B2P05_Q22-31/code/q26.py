import numpy as np
rng = np.random.default_rng(3)
# SYNTHETIC. Each attack has a latent "hardness"; layer i misses it if hardness_i > its strength.
# Independence assumption: layers' hardness draws are independent. Correlation rho shares a common factor.
miss = [0.10, 0.20, 0.30]     # individual layer miss rates
from math import erf, sqrt
def ppf(p):  # inverse normal cdf by bisection (no scipy)
    lo, hi = -8, 8
    for _ in range(80):
        m = (lo+hi)/2
        if 0.5*(1+erf(m/sqrt(2))) < p: lo = m
        else: hi = m
    return (lo+hi)/2
N = 400000
print("product of miss rates (independent):", round(float(np.prod(miss)), 4))
for rho in [0.0, 0.3, 0.6, 0.9]:
    common = rng.standard_normal(N)
    all_miss = np.ones(N, bool)
    for m in miss:
        z = np.sqrt(rho)*common + np.sqrt(1-rho)*rng.standard_normal(N)
        all_miss &= z > ppf(1-m)       # this layer misses with prob m
    print(f"rho={rho:.1f}: simulated all-layers-miss {all_miss.mean():.4f}")

from scipy.stats import norm
import numpy as np
def n_per_arm(p, mde_rel, alpha=0.05, power=0.8):
    p2 = p*(1+mde_rel); pb=(p+p2)/2
    za, zb = norm.ppf(1-alpha/2), norm.ppf(power)
    return int(np.ceil(2*pb*(1-pb)*(za+zb)**2/(p2-p)**2))
n = n_per_arm(0.10, 0.05)
print(n, "per arm;", "days at 20k users/day total:", np.ceil(2*n/20000))

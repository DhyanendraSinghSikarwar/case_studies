import numpy as np
def psi(a, b, bins=10):
    edges = np.quantile(a, np.linspace(0, 1, bins+1)); edges[0], edges[-1] = -np.inf, np.inf
    pa = np.histogram(a, edges)[0]/len(a); pb = np.histogram(b, edges)[0]/len(b)
    pa, pb = np.clip(pa,1e-6,None), np.clip(pb,1e-6,None)
    return float(np.sum((pb-pa)*np.log(pb/pa)))
rng = np.random.default_rng(0)
ref = rng.normal(0,1,50000)
print(round(psi(ref, rng.normal(0,1,50000)),4), round(psi(ref, rng.normal(0.5,1,50000)),3))

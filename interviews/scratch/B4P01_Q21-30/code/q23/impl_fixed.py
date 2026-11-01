import numpy as np

def minmax(x):
    x = np.asarray(x, dtype=float)
    if x.size == 0 or not np.isfinite(x).all():
        raise ValueError("minmax needs a non-empty array of finite numbers")
    lo, hi = x.min(), x.max()
    if hi == lo:
        return np.zeros_like(x)                          # documented choice: constant column -> all 0.0
    return (x - lo) / (hi - lo)

def split_idx(n, test_frac, seed):
    if n < 2:
        raise ValueError("need at least 2 rows to split")
    n_test = min(max(round(n * test_frac), 1), n - 1)    # both sides non-empty
    perm = np.random.default_rng(seed).permutation(n)    # without replacement
    return np.sort(perm[n_test:]), np.sort(perm[:n_test])

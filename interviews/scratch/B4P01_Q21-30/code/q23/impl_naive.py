import numpy as np

def minmax(x):
    x = np.asarray(x, dtype=float)
    return (x - x.min()) / (x.max() - x.min())          # constant column -> 0/0

def split_idx(n, test_frac, seed):
    rng = np.random.default_rng(seed)
    n_test = int(n * test_frac)                          # truncates: n=2, 0.2 -> 0 test rows
    test = rng.integers(0, n, size=n_test)               # sampling WITH replacement -> duplicates
    train = np.setdiff1d(np.arange(n), test)
    return train, test

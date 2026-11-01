import random
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def make_df(n=300, seed=0):
    rng = np.random.default_rng(seed)               # local generator: no hidden global state
    x = rng.normal(size=(n, 3))
    y = (x[:, 0] + 0.5 * x[:, 1] + rng.normal(scale=1.0, size=n) > 0).astype(int)
    return pd.DataFrame(x, columns=["a", "b", "c"]).assign(y=y)


def train_test_split_and_fit(df, seed=None):
    """seed=None reproduces the original problem: the split changes every call."""
    if seed is not None:
        random.seed(seed); np.random.seed(seed)      # only matters for third-party code using the globals
    Xtr, Xte, ytr, yte = train_test_split(df[["a", "b", "c"]], df["y"], test_size=0.3, random_state=seed)
    m = LogisticRegression(random_state=seed).fit(Xtr, ytr)
    return float(m.score(Xte, yte))

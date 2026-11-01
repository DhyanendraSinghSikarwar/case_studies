import warnings; warnings.filterwarnings("ignore")
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=3000, n_features=10, n_informative=5, flip_y=0, class_sep=1.7, random_state=7)
THRESH = 0.90

def acc(seed, n_test=200, fit_seed=0):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=n_test, random_state=seed)
    return LogisticRegression(max_iter=500, random_state=fit_seed).fit(Xtr, ytr).score(Xte, yte)

REPS = 200
a = np.array([acc(s) for s in range(REPS)])                       # "unseeded": a different split each run
print(f"typical accuracy (mean over {REPS} splits): {a.mean():.3f}   sd across splits: {a.std():.4f}")
print(f"binomial SE on 200 rows at p={a.mean():.3f}: {np.sqrt(a.mean()*(1-a.mean())/200):.4f}")
def rate(v, thr): return (v < thr).mean() * 100
print(f"\n{'variant':58} fail rate")
print(f"{'A. assert acc > 0.90, split differs each run (200 runs)':58} {rate(a,THRESH):5.1f}%")
fixed = np.array([acc(42) for _ in range(REPS)])
print(f"{'B. same seed 42 every run (200 runs)':58} {rate(fixed,THRESH):5.1f}%   (accuracy {fixed[0]:.3f} every time: all-or-nothing)")
p_hat = a.mean()
se = np.sqrt(p_hat*(1-p_hat)/200)
thr_w = p_hat - 3*se
print(f"{f'C. widen: assert acc > p_hat - 3*SE = {thr_w:.3f}, split differs':58} {rate(a,thr_w):5.1f}%")
big = np.array([acc(s, n_test=1000) for s in range(REPS)])
print(f"{'D. larger test set (1000 rows), same 0.90 threshold':58} {rate(big,THRESH):5.1f}%   sd {big.std():.4f}")
# E: property not number: model beats majority-class baseline by a margin
base = np.array([max(np.mean(y), 1-np.mean(y))]*REPS)
print(f"{'E. property: acc > majority baseline + 0.10':58} {rate(a, base[0]+0.10):5.1f}%   (baseline {base[0]:.3f})")

# Q44: upstream embedding upgrade breaks consumers. Illustrative simulation.
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(44)
d, n = 16, 6000
Z = rng.normal(size=(n, d))                      # "true" semantic factors
w_true = rng.normal(size=d)
y = (Z@w_true + rng.normal(0, 1.0, n) > 0).astype(float)
E_old = Z + rng.normal(0, 0.3, (n, d))           # v1 embedding

from scipy.linalg import expm
def new_space(E, theta, rng):
    # v2 = v1 rotated by a random rotation of size theta (a different, equally good space)
    A = rng.normal(size=(d, d)); A = A - A.T
    A = A/np.linalg.norm(A, 2)
    return E@expm(theta*A)

def fit(X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    f = lambda b: np.mean(np.logaddexp(0, X1@b) - y*(X1@b))
    return minimize(f, np.zeros(X1.shape[1]), method="L-BFGS-B").x
def acc(b, X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    return np.mean(((X1@b) > 0) == (y == 1))

tr, te = slice(0, 4000), slice(4000, n)
b = fit(E_old[tr], y[tr])
a0 = acc(b, E_old[te], y[te])
print(f"consumer on v1 vectors: accuracy {a0:.3f}")
res = {}
for frac in (0.4, 0.8, 1.2, 3.0):
    E_new = new_space(E_old, frac, np.random.default_rng(7))
    res[frac] = acc(b, E_new[te], y[te])
    print(f"v2 = {frac} rotation, old consumer unchanged: accuracy {res[frac]:.3f}")
assert res[0.4] > res[0.8] > res[1.2] > res[3.0]      # the bigger the change, the bigger the loss
assert a0 - res[3.0] > 0.15                   # full re-spacing is near-chance
# alignment on a small paired sample (orthogonal Procrustes) recovers most of it, without retraining
E_new = new_space(E_old, 3.0, np.random.default_rng(7))
idx = slice(0, 500)
U, _, Vt = np.linalg.svd(E_new[idx].T@E_old[idx]); R = U@Vt          # maps new -> old
acc_aligned = acc(b, (E_new@R)[te], y[te])
print(f"after Procrustes alignment from 500 paired items: accuracy {acc_aligned:.3f}")
assert a0 - acc_aligned < 0.01
# canary gate: per-consumer accuracy drop vs frozen eval set, block above 1 point
gate = 0.01
for frac in (0.4, 1.2):
    E_new = new_space(E_old, frac, np.random.default_rng(7))
    drop = a0 - acc(b, E_new[te], y[te])
    print(f"gate at {gate:.0%}: rotation {frac} -> drop {drop:.3f} -> {'BLOCK' if drop > gate else 'pass'}")

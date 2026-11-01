import numpy as np
from scipy.stats import norm

# Check the prompt: can bias 0 -> +15% and MAPE 11% -> 18% both be true?
# Percentage error e = (forecast - actual)/actual ~ Normal(mu, s). E|e| for a folded normal:
def mape_fold(mu, s): return s * np.sqrt(2 / np.pi) * np.exp(-mu**2 / (2 * s**2)) + mu * (1 - 2 * norm.cdf(-mu / s))
s = 0.11 / np.sqrt(2 / np.pi)                  # s that gives MAPE 11% at zero bias
print(f"spread giving MAPE 11% at zero bias: {s:.3f}; MAPE with +15% bias: {mape_fold(0.15, s):.3f}")
assert abs(mape_fold(0, s) - 0.11) < 1e-9 and 0.16 < mape_fold(0.15, s) < 0.19   # consistent with the prompt's 18%

# Simulation: 120 weekly points, break at week 60 (price cut; model does not see price)
rng = np.random.default_rng(24)
W, BREAK = 120, 60
actual = 1000 * (1 + 0.1 * np.sin(np.arange(W) * 2 * np.pi / 52)) * 1.0
actual[BREAK:] *= 1 / 1.15                      # demand ends up 1/1.15 of what the old pattern implies
fc = 1000 * (1 + 0.1 * np.sin(np.arange(W) * 2 * np.pi / 52)) * np.exp(rng.normal(0, s, W))
act = actual * np.exp(rng.normal(0, 0.02, W))
err = (fc - act) / act
pre, post = err[:BREAK], err[BREAK:]
print(f"before: bias {pre.mean():+.3f} MAPE {np.abs(pre).mean():.3f} | after: bias {post.mean():+.3f} MAPE {np.abs(post).mean():.3f}")

# CUSUM on the percentage error: flag when cumulative positive drift passes a limit
k, h = 0.08, 0.50
c, flag = 0.0, None
for t in range(W):
    c = max(0.0, c + err[t] - k)
    if c > h and flag is None: flag = t
print("break at week", BREAK, "| CUSUM alarm at week", flag)
assert flag is not None and BREAK <= flag <= BREAK + 6

# Interim patch: multiply forecast by a bias correction learned from the last 4 matured weeks (lag 2)
adj = fc.copy()
for t in range(BREAK, W):
    lo, hi = max(0, t - 6), t - 2
    ratio = (fc[lo:hi] / act[lo:hi]).mean()      # recent forecast-to-actual ratio
    adj[t] = fc[t] / ratio
err_adj = (adj - act) / act
print(f"after, with rolling ratio patch: bias {err_adj[BREAK:].mean():+.3f} MAPE {np.abs(err_adj[BREAK:]).mean():.3f}")
assert np.abs(err_adj[BREAK + 8:]).mean() < np.abs(post[8:]).mean()
print("asserts passed")

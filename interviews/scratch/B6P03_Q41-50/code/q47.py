# Q47: partial pooling for short-history stores. Illustrative simulation of weekly log-sales.
import numpy as np
rng = np.random.default_rng(47)
S, SHORT = 2_000, 600
assert SHORT / S == 0.30
n_hist = np.concatenate([rng.integers(8, 30, SHORT), np.full(S - SHORT, 104)])   # weeks of history
tau, sigma, m = 0.30, 0.80, 5.0           # store-level spread, weekly noise, grand mean (log scale)
mu = rng.normal(m, tau, S)                # true store level (what we want to forecast)
means = np.array([rng.normal(mu[i], sigma, n_hist[i]).mean() for i in range(S)])

# method-of-moments estimates of the variance components, from the data only
# weekly noise: pooled within-store variance of 300 long-history stores (fresh draws stand in for their weekly data)
long_i = np.where(n_hist == 104)[0]
sig2_hat = np.mean([rng.normal(mu[i], sigma, 104).var(ddof=1) for i in long_i[:300]])
grand = np.average(means, weights=n_hist)
tau2_hat = max(np.var(means, ddof=1) - np.mean(sig2_hat / n_hist), 1e-6)
print(f"sigma_hat {np.sqrt(sig2_hat):.3f} (true {sigma})   tau_hat {np.sqrt(tau2_hat):.3f} (true {tau})")
assert abs(np.sqrt(tau2_hat) - tau) < 0.06 and abs(np.sqrt(sig2_hat) - sigma) < 0.05

w = n_hist / (n_hist + sig2_hat / tau2_hat)          # shrinkage weight on the store's own mean
pooled = w * means + (1 - w) * grand
k = sig2_hat / tau2_hat
print(f"k = sigma^2/tau^2 = {k:.2f}; weight on own mean: 8 weeks {8/(8+k):.2f}, 29 weeks {29/(29+k):.2f}, 104 weeks {104/(104+k):.2f}")
assert 6 < k < 9

def mse(est, idx): return float(np.mean((est[idx] - mu[idx]) ** 2))
sh = np.arange(SHORT); lg = np.arange(SHORT, S)
print(f"{'':22s}{'short (600)':>12s}{'long (1400)':>12s}")
for name, est in [("store mean only", means), ("global mean only", np.full(S, grand)), ("partial pooling", pooled)]:
    print(f"{name:22s}{mse(est, sh):12.4f}{mse(est, lg):12.4f}")
assert mse(pooled, sh) < mse(means, sh) and mse(pooled, sh) < mse(np.full(S, grand), sh)
assert mse(pooled, sh) <= mse(means, sh) * 0.8
# 8-week stores: standard error of own mean vs shrunk
print(f"SE of own mean at 8 weeks: {sigma/np.sqrt(8):.3f}; at 104 weeks: {sigma/np.sqrt(104):.3f}; tau = {tau}")
assert abs(sigma / np.sqrt(8) - tau) < 0.03 and sigma / np.sqrt(104) < tau / 3

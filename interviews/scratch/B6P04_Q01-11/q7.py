import numpy as np
rng = np.random.default_rng(31)

base, new = 1.00, 1.08
print("relative p95 degradation (%):", round((new / base - 1) * 100, 1), "vs allowed 5%")
assert round((new / base - 1) * 100, 1) == 8.0

# Illustrative latency data: lognormal, p95 of control = 1.00 s; treatment is 8% slower at every quantile
sigma = 0.5
z95 = 1.6449
mu_c = np.log(1.0) - sigma * z95
n = 200_000
ctrl = rng.lognormal(mu_c, sigma, n)
treat = rng.lognormal(mu_c + np.log(1.08), sigma, n)
p95c, p95t = np.percentile(ctrl, 95), np.percentile(treat, 95)
print(f"sample p95: control {p95c:.3f}, treatment {p95t:.3f}, ratio {p95t/p95c:.3f}")

# Bootstrap CI for the relative p95 degradation (200 resamples)
B = 200
ratios = np.empty(B)
for b in range(B):
    ic = rng.integers(0, n, n); it = rng.integers(0, n, n)
    ratios[b] = np.percentile(treat[it], 95) / np.percentile(ctrl[ic], 95) - 1
lo, hi = np.percentile(ratios, [2.5, 97.5])
print(f"bootstrap 95% CI for relative p95 change: {lo*100:.1f}% to {hi*100:.1f}%")
assert lo > 0.05              # the whole interval is beyond the 5% limit
print("breach of the 5% limit is clear:", lo > 0.05)

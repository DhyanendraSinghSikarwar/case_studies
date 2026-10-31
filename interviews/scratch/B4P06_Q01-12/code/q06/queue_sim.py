"""Single server, Poisson arrivals, exponential service (mean 10 ms). Shows p99 vs utilisation."""
import numpy as np
rng = np.random.default_rng(0)
n, service_mean = 200_000, 0.010
S = rng.exponential(service_mean, n)
for rho in (0.3, 0.5, 0.7, 0.8, 0.9, 0.95):
    A = rng.exponential(service_mean / rho, n)          # inter-arrival gaps
    w = np.zeros(n)                                      # waiting time (Lindley recursion)
    for i in range(1, n):
        w[i] = max(0.0, w[i-1] + S[i-1] - A[i])
    lat = (w + S) * 1000
    print(f"utilisation {rho:4.2f}: p50 {np.percentile(lat,50):6.1f} ms  p99 {np.percentile(lat,99):7.1f} ms")

import numpy as np
# hand check: 10 timings in ms, sorted: 1..9 and 100
t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
print("mean", np.mean(t), "p50", np.percentile(t, 50), "p90", np.percentile(t, 90), "p99", np.percentile(t, 99))
# numpy's default 'linear' rule: rank = p/100*(n-1) = 0.5*9 = 4.5 -> between 5 and 6 -> 5.5
# p90: rank 8.1 -> 9 + 0.1*(100-9) = 18.1 ; p99: rank 8.91 -> 9 + 0.91*91 = 91.81
assert np.percentile(t, 50) == 5.5 and abs(np.percentile(t, 90) - 18.1) < 1e-9 and abs(np.percentile(t, 99) - 91.81) < 1e-9
# tail amplification: a page makes k calls; P(at least one call is slower than its own p99) = 1 - 0.99**k
for k in (1, 10, 50, 100):
    print(f"page with {k:3d} calls: {100*(1-0.99**k):5.1f}% of pages see at least one call beyond p99")
# Little's law: concurrency = throughput x latency
print("Little: 200 req/s x 0.050 s =", 200 * 0.050, "requests in flight")

import time, sys, httpx, numpy as np
url = sys.argv[1]; body = {"features": [6.7, 3.0, 5.2, 2.3]}
with httpx.Client() as c:
    for _ in range(20): c.post(url, json=body)            # warm-up, not measured
    t = []
    for _ in range(200):
        s = time.perf_counter(); r = c.post(url, json=body); t.append((time.perf_counter() - s) * 1000)
        assert r.status_code == 200
p = np.percentile(t, [50, 95, 99])
print(f"200 sequential calls: mean {np.mean(t):.2f} ms  p50 {p[0]:.2f}  p95 {p[1]:.2f}  p99 {p[2]:.2f}  max {max(t):.2f} (this sandbox only)")

# SYNTHETIC traffic: 100 requests/min, baseline error rate 1%, incident error rate 3% (both ASSUMED).
# Alert rule: errors in the last W minutes >= k, with k chosen so a baseline window false-alarms with prob <= 1e-3.
import math
import numpy as np
rng = np.random.default_rng(7)
RPM, P0, P1 = 100, 0.01, 0.03
def tail(n, p, k):                      # exact P(X >= k) for Binomial(n, p)
    return sum(math.exp(math.lgamma(n+1)-math.lgamma(i+1)-math.lgamma(n-i+1)+i*math.log(p)+(n-i)*math.log1p(-p)) for i in range(k, n + 1))
def pick_k(n, alpha):
    k = 0
    while tail(n, P0, k) > alpha: k += 1
    return k
# check the closed form against brute-force simulation for one window
n, k = RPM * 5, 10
sim = (rng.binomial(n, P0, 400000) >= k).mean()
print(f"check: exact P(X>=10 | n=500,p=.01)={tail(n, P0, k):.5f}  simulated={sim:.5f}")
def rolling(counts, W):
    c = np.concatenate([[0], np.cumsum(counts)])
    return c[W:] - c[:-W]                # sum over each W-minute window
DAY = 1440
print("window  k  baseline min over k per day  median minutes to alert after 1%->3% (200 runs)")
for W in (1, 5, 15, 60):
    k = pick_k(RPM * W, 1e-3)
    base = rng.binomial(RPM, P0, 30 * DAY)
    fa = (rolling(base, W) >= k).sum() / 30
    delays = []
    for _ in range(200):
        inc = rng.binomial(RPM, P1, 3 * 60)          # incident starts at minute 0, watch 3 h
        hit = np.nonzero(np.concatenate([np.zeros(W - 1), rolling(inc, W)]) >= k)[0]
        # windows ending before minute W-1 mix nothing: pad zeros so early windows cannot fire
        delays.append(hit[0] + 1 if len(hit) else np.inf)
    print(f"{W:4d}m {k:3d}  {fa:8.2f}                    {np.median(delays):6.1f}  (never alerted in {int(np.isinf(delays).sum())}/200)")

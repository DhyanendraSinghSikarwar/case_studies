import numpy as np
# Stream: daily error rate-like metric, baseline mean 0.10, sd 0.02; step to 0.12 at t=300 (1 sd).
MU, SD, T, STEP_AT, STEP = 0.10, 0.02, 600, 300, 0.02

def cusum(x, k=0.5, h=5.0):
    """Upper CUSUM on standardised values. k = drift allowance (in sd), h = threshold (in sd). Returns first alarm index or None."""
    s = 0.0
    for i, v in enumerate(x):
        z = (v - MU) / SD
        s = max(0.0, s + z - k)
        if s > h: return i
    return None

def page_hinkley(x, delta=0.5, lam=8.0):
    """Page-Hinkley for an increase. delta = tolerated drift (in sd), lam = threshold (in sd). Running mean as the reference."""
    m, cum, cum_min = 0.0, 0.0, 0.0
    for i, v in enumerate(x):
        z = (v - MU) / SD
        m += (z - m) / (i + 1)
        cum += z - m - delta
        cum_min = min(cum_min, cum)
        if cum - cum_min > lam: return i
    return None

def run(detector, **kw):
    delays, fa_noise, pre = [], 0, 0
    for seed in range(200):
        r = np.random.default_rng(seed)
        noise = r.normal(MU, SD, T)
        fa_noise += detector(noise, **kw) is not None       # noise-only stream: any alarm is false
        shifted = noise.copy(); shifted[STEP_AT:] += STEP    # same noise plus a step at t=300
        a = detector(shifted, **kw)
        if a is not None and a < STEP_AT: pre += 1           # alarmed before the step: false alarm
        elif a is not None: delays.append(a - STEP_AT)
    return np.median(delays), len(delays), fa_noise, pre

print("noise-only: 600 points. step run: +1 sd (0.02) at t=300. 200 seeds.")
for name, det, kws in [("CUSUM k=0.5 h=5", cusum, dict(k=0.5, h=5.0)),
                       ("CUSUM k=0.5 h=8", cusum, dict(k=0.5, h=8.0)),
                       ("PageHinkley d=0.5 lam=8", page_hinkley, dict(delta=0.5, lam=8.0)),
                       ("PageHinkley d=0.5 lam=15", page_hinkley, dict(delta=0.5, lam=15.0))]:
    med, n, fa, pre = run(det, **kws)
    print(f"{name:26s} false alarms (noise-only)={fa:3d}/200  alarmed before step={pre:3d}/200  detected after step={n:3d}/200  median delay={med:.1f} points")

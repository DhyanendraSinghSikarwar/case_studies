# Q22: automatic canary rollback criteria. Seeded simulation plus exact binomial; illustrative numbers.
import math
import numpy as np
from scipy.stats import binom
rng = np.random.default_rng(22)
p0, n = 0.02, 10_000
se_known = math.sqrt(p0 * (1 - p0) / n)
print(f"SE of 2% on 10,000 = {se_known*100:.3f} points; z for 2.5% against a KNOWN 2% baseline = {0.005/se_known:.2f}")
assert abs(se_known * 100 - 0.14) < 0.001 and round(0.005 / se_known, 1) == 3.6
def z2(x1, n1, x2, n2):                         # pooled two-proportion z (canary x1/n1 vs control x2/n2)
    p = (x1 + x2) / (n1 + n2)
    return (x1 / n1 - x2 / n2) / math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
for label, nc in [("control also 10,000", 10_000), ("control 190,000 (5% canary split)", 190_000)]:
    z = z2(250, n, round(0.02 * nc), nc)
    print(f"z for 2.5% vs measured 2.0%, {label}: {z:.2f}")
z_eq, z_big = z2(250, n, 200, 10_000), z2(250, n, 3800, 190_000)
assert round(z_eq, 1) == 2.4 and round(z_big, 1) == 3.5
# --- peeking: check every 1,000 canary requests; control is 19x larger; stop if z >= Z
def sim(p_canary, Z, trials=2000, peek=1000, total=10_000, ctrl_factor=19, p_ctrl=0.02, min_err=5):
    hits = 0
    for _ in range(trials):
        c = rng.binomial(peek, p_canary, total // peek).cumsum()
        k = ctrl_factor * peek * np.arange(1, total // peek + 1)
        x = rng.binomial(k, p_ctrl)
        fired = False
        for i in range(total // peek):
            nn = peek * (i + 1)
            if c[i] >= min_err and z2(int(c[i]), nn, int(x[i]), int(k[i])) >= Z: fired = True; break
        hits += fired
    return hits / trials
rows = {}
for Z in (2.0, 3.0, 4.0):
    rows[Z] = (sim(0.02, Z), sim(0.025, Z), sim(0.03, Z))
    print(f"threshold z>={Z}: false rollback {rows[Z][0]:.1%} | catches 2.5% {rows[Z][1]:.0%} | catches 3.0% {rows[Z][2]:.0%} (checked every 1,000 requests)")
assert rows[2.0][0] > 0.10                          # peeking at z=2 rolls back far too often
assert rows[3.0][0] < 0.02                          # z=3 keeps false rollback small
assert rows[3.0][2] > rows[3.0][1] > 0.4            # bigger harm is caught more often
# hard guard: absolute cap, error rate above 4% (2 points above baseline) once 500 requests are in
cap_fp = 1 - binom.cdf(math.floor(0.04 * 500), 500, 0.02)
print(f"hard cap 4% at 500 requests: false trigger at true 2% = {cap_fp:.4f}")
assert cap_fp < 0.005
# --- small segments: a segment with 2% of traffic has 200 canary requests
seg = 200
k = int(binom.isf(0.001, seg, p0)) + 1               # smallest count with false chance below 0.1% at a true 2% rate
print(f"segment of {seg} requests: expect {seg*p0:.0f} errors at 2%; rule 'errors >= {k}' has false chance {binom.sf(k-1, seg, p0):.5f}")
for pt in (0.05, 0.10, 0.20):
    print(f"   chance to catch a segment error rate of {pt:.0%}: {binom.sf(k-1, seg, pt):.2f}")
assert binom.sf(k - 1, seg, 0.02) < 0.001 and binom.sf(k - 1, seg, 0.20) > 0.99 and 0.2 < binom.sf(k - 1, seg, 0.05) < 0.4 and binom.sf(k - 1, seg, 0.10) > 0.9
# volume needed to see a 5% segment rate (vs 2%) with the same 3 sigma idea, one-sided: n = (z*sqrt(p0 q0)+...)^2
z, power_z = 3.0, 0.84
need = ((z * math.sqrt(0.02 * 0.98) + power_z * math.sqrt(0.05 * 0.95)) / 0.03) ** 2
print(f"requests needed in a segment to catch 2% -> 5% (z 3.0, 80% power): about {need:,.0f}")
assert 350 < need < 450

# Q2: roll back now? Illustrative numbers; seeded.
import math
import numpy as np
from scipy import stats

# prompt arithmetic
assert round((240 - 180) / 180, 3) == 0.333                 # 33% relative to 180 ms
n = 12_000
x_new, x_old = round(0.042 * n), round(0.043 * n)           # 504 and 516 conversions
assert (x_new, x_old) == (504, 516) and x_old - x_new == 12

# two-proportion z test (pooled), two-sided
p_pool = (x_new + x_old) / (2 * n)
se_pool = math.sqrt(p_pool * (1 - p_pool) * 2 / n)
z = (x_new / n - x_old / n) / se_pool
p_val = 2 * stats.norm.sf(abs(z))
print(f"conversion gap -0.1 pt: z={z:.2f}, p={p_val:.2f}")
assert abs(z) < 1 and p_val > 0.3                            # indistinguishable from noise

# 95% CI of the difference (unpooled)
se = math.sqrt(0.042*0.958/n + 0.043*0.957/n)
lo, hi = (0.042 - 0.043) - 1.96*se, (0.042 - 0.043) + 1.96*se
print(f"95% CI of difference: [{lo*100:.2f}, {hi*100:.2f}] points")
assert lo < -0.004 and hi > 0.002                            # about +/- 0.5 points: a 0.4-point loss is still possible

# smallest drop this sample could detect (80% power, alpha 0.05, two-sided)
mde = (1.96 + 0.8416) * se
print(f"smallest detectable drop at 12,000 vs 12,000 = {mde*100:.2f} points ({mde/0.043:.0%} relative)")
assert 0.006 < mde < 0.008

# is the latency rise real? bootstrap CI of p95 with simulated latencies (lognormal, sigma 0.4)
rng = np.random.default_rng(8)
sigma = 0.4
def sample(p95, m): return rng.lognormal(math.log(p95) - 1.645*sigma, sigma, m)
old, new = sample(180, n), sample(240, n)
def boot_p95(a, B=300): return np.percentile([np.percentile(rng.choice(a, len(a)), 95) for _ in range(B)], [2.5, 97.5])
print("p95 old CI", boot_p95(old).round(1), "| p95 new CI", boot_p95(new).round(1))
assert boot_p95(old)[1] < boot_p95(new)[0]                   # intervals do not overlap: latency rise is real

# the pre-agreed rule, as code (thresholds illustrative)
def decide(p95_ms, base_ms, minutes_over, err_rate):
    if err_rate > 0.01: return "ROLLBACK (errors)"
    if p95_ms > 1.5 * base_ms and minutes_over >= 10: return "ROLLBACK (latency)"
    if p95_ms > 1.2 * base_ms: return "HOLD (freeze other changes), page owner, decide in 30 min"
    return "CONTINUE"
print(decide(240, 180, 40, 0.001))   # 240 is 1.33x: above 1.2x, below 1.5x
print(decide(280, 180, 12, 0.001))   # 280 is 1.56x for 12 min
assert decide(240, 180, 40, 0.001).startswith("HOLD") and decide(280, 180, 12, 0.001).startswith("ROLLBACK")

# follow-up claim: per-arm sample to detect a 0.3-point drop from 4.3% (80% power, alpha 0.05)
n_need = 2 * (1.96 + 0.8416)**2 * 0.043 * 0.957 / 0.003**2
print("per-arm sessions to detect 0.3 points:", round(n_need))
assert 60_000 < n_need < 80_000

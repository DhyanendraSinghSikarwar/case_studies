# Q29 identity verification (illustrative; 0.1% is a projection, 95% is a sample on known attacks)
from math import sqrt
checks, spoof_rate, catch = 40_000, 0.001, 0.95
spoofs = round(checks * spoof_rate)
caught = spoofs * catch
passed = spoofs - caught
assert spoofs == 40 and caught == 38 and abs(passed - 2) < 1e-9
print(f"spoofs/day={spoofs}, caught={caught:.0f}, pass liveness={passed:.0f} (best case: known attacks only)")

# Sensitivity to the catch rate on new attack types
for r in (0.95, 0.80, 0.50, 0.20):
    print(f"  catch {r:.0%}: {spoofs*(1-r):.0f} spoofs pass a day")
assert abs(spoofs * (1 - 0.2) - 32) < 1e-9
assert spoofs * (1 - 0.5) == 20 and abs(spoofs * (1 - 0.8) - 8) < 1e-9

# The 95% is from a test set; invented size 200 attacks, 190 caught -> Wilson interval
n, k, z = 200, 190, 1.96
p = k / n
den = 1 + z * z / n
centre = (p + z * z / (2 * n)) / den
half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
lo, hi = centre - half, centre + half
assert abs(lo - 0.9104) < 0.002 and abs(hi - 0.9727) < 0.002
print(f"95% from 190/200: interval {lo:.1%} to {hi:.1%} -> {spoofs*(1-hi):.1f} to {spoofs*(1-lo):.1f} pass")

# Cost on genuine users: invented 1% fall back to human review
genuine = checks - spoofs
fallback = genuine * 0.01
assert genuine == 39_960 and abs(fallback - 399.6) < 1e-9
print(f"genuine users sent to fallback at 1%: {fallback:.1f} a day")
# Queue that a review team must handle: fallback plus caught spoofs
queue = fallback + caught
assert abs(queue - 437.6) < 1e-9
print(f"daily human-review queue ~ {queue:.1f} cases")
# Precision of the fallback queue
prec = caught / queue
assert abs(prec - 0.0868) < 1e-3
print(f"share of that queue that are real spoofs ~ {prec:.1%}")

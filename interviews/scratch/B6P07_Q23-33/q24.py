# Citation audit: shares of each outcome, Wilson intervals, and a simple projection (illustrative).
import math
def wil(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
n = 150
ok, unsup, fab = 120, 15, 15
assert ok + unsup + fab == n
for name, k in [("supported", ok), ("exists but unsupported", unsup), ("fabricated", fab)]:
    lo, hi = wil(k, n)
    print(f"{name}: {k}/{n} = {k/n:.1%}, 95% Wilson {lo:.1%} to {hi:.1%}")
assert ok/n == 0.8 and unsup/n == 0.1 and fab/n == 0.1
lo, hi = wil(15, 150)
assert round(lo, 3) == 0.062 and round(hi, 3) == 0.158, (lo, hi)
# Resolver check alone catches only the fabricated kind: share of bad citations it can see
bad = unsup + fab
print("bad citations", bad, "share of citations", bad/n, "resolver-visible share of bad", fab/bad)
assert bad == 30 and bad/n == 0.2 and fab/bad == 0.5
# Illustrative target: after a fix, fabricated 15 -> 0 by resolver filter, unsupported 15 -> 9 by claim check
after_ok = n - 0 - 9
print("after fix (illustrative): supported", after_ok, f"{after_ok/n:.0%}", "bad", 9, f"{9/n:.0%}")
assert after_ok == 141 and 9/n == 0.06
# Sample size to see 5% vs 10% unsupported-rate with a 95% half-width of about 2.5 points
n_need = math.ceil(1.96**2 * 0.05*0.95 / 0.025**2)
print("n for half-width 2.5 points at p=0.05:", n_need)
assert n_need == 292

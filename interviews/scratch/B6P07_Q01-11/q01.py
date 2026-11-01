import math
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
# Illustrative audit of 100 FAILED answers (the denominator is failures, not all traffic)
audit = {"gold chunk not in top 5": 55, "in top 5, model ignored it": 20,
         "outdated doc retrieved": 15, "other": 10}
assert sum(audit.values()) == 100
for k, v in audit.items():
    lo, hi = wilson(v, 100)
    print(f"{k:28} {v:3d}%  95% Wilson {lo:.1%} to {hi:.1%}")
lo, hi = wilson(55, 100); assert round(lo, 3) == 0.452 and round(hi, 3) == 0.644
lo2, hi2 = wilson(20, 100); assert hi2 < lo   # 20% interval sits fully below the 55% interval
# retrieval-side total = miss + stale
ret = 55 + 15; print("retrieval-side causes:", ret, "of 100")
assert ret == 70
# What if the fix wins back 60% of the misses and 80% of the stale cases?
fixed = 0.6*55 + 0.8*15; print("failures removed by that fix:", fixed, "of 100")
assert fixed == 45.0
# Failure rate needs the denominator: if 8% of all answers fail, the fix moves 8% -> 8% * (1 - .45)
print(f"overall failure rate 8.0% -> {8*(1-fixed/100):.1f}%")
assert round(8*(1-fixed/100), 1) == 4.4
# Sample size to pin the miss share to +/-5 points (normal approx, worst case p=0.5)
n = math.ceil((1.96*0.5/0.05)**2); print("n for +/-5 points:", n); assert n == 385

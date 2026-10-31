# Reranker: gain, intervals, and a paired test on ILLUSTRATIVE discordant counts. Seeded.
import math
from scipy.stats import binomtest
n = 300
a, b = 186, 222
print("recall@5", a/n, b/n, "gain points", (b-a)/n*100, "relative", round((b-a)/a, 3))
assert a/n == 0.62 and b/n == 0.74 and b - a == 36 and round((b-a)/a, 3) == 0.194
def wil(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h, c+h
print("Wilson before", [round(x, 3) for x in wil(a, n)], "after", [round(x, 3) for x in wil(b, n)])
# Unpaired difference interval (conservative; the paired one is usually tighter)
se = math.sqrt(.62*.38/n + .74*.26/n)
print("unpaired SE", round(se, 4), "95% interval for gain", round(.12-1.96*se, 3), round(.12+1.96*se, 3))
assert round(se, 4) == 0.0378 and round(.12-1.96*se, 3) == 0.046
# Paired: net +36 = rescued - lost. Illustrative: 42 rescued, 6 lost (exact sign test)
rescued, lost = 42, 6
assert rescued - lost == 36
p = binomtest(rescued, rescued+lost, 0.5).pvalue
print("exact McNemar p (illustrative 42 vs 6):", f"{p:.2e}")
assert p < 1e-6
# Worst plausible split with the same net: 80 rescued, 44 lost -> still net 36, test weaker but still small p, yet 44 users get worse
p2 = binomtest(80, 124, 0.5).pvalue
print("exact McNemar p (80 vs 44):", round(p2, 4))
assert 0.001 < p2 < 0.002
# Latency
base, add, budget = 900, 120, 1200
total = base + add
print("latency", total, "headroom", budget-total, "added share", round(add/base, 3))
assert total == 1020 and budget - total == 180 and round(add/base, 3) == 0.133
# If 900 is a mean and p95 is 1.4x mean (illustrative), p95 after = 1.4*900+120*? ; flag the budget risk
p95_after = 1.4*base + 1.5*add
print("illustrative p95 after (rerank p95 1.5x)", p95_after, "vs budget", budget)
assert p95_after == 1440 > budget
# per 1,000 queries
print("extra queries with the right chunk in top 5 per 1,000:", round(1000*(b-a)/n))
assert round(1000*(b-a)/n) == 120

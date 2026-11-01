from statistics import NormalDist
import math
mu, sd, cu, co = 100, 20, 30, 20
cr = cu / (cu + co)
z = NormalDist().inv_cdf(cr)
q = mu + sd * z
print("critical ratio", cr, "z", round(z, 4), "stock", round(q, 2))
assert cr == 0.6 and round(z, 4) == 0.2533 and round(q, 2) == 105.07
# integer stock: the smallest integer with P(D <= Q) >= 0.6 (continuous normal)
Q = math.ceil(q)
print("integer stock (continuous rule rounds up)", Q, "P(D<=Q)", round(NormalDist(mu, sd).cdf(Q), 4))
assert NormalDist(mu, sd).cdf(105) < 0.6 <= NormalDist(mu, sd).cdf(106)
# expected profit-loss (cost) at a few stocks by Monte Carlo-free numeric integration
nd = NormalDist(mu, sd)
def exp_cost(Q):
    lo, hi = mu - 6 * sd, mu + 6 * sd
    n = 20000; h = (hi - lo) / n; tot = 0.0
    for i in range(n):
        d = lo + (i + 0.5) * h
        tot += nd.pdf(d) * h * (co * max(Q - d, 0) + cu * max(d - Q, 0))
    return tot
for s in (100, 105, 106, 110):
    print("stock", s, "expected cost", round(exp_cost(s), 2))
assert exp_cost(105) < exp_cost(100) and exp_cost(105) < exp_cost(110)
c100, c105 = exp_cost(100), exp_cost(105)
print("saving per day vs stocking the mean", round(c100 - c105, 2), "rupees (illustrative)")
assert round(c100 - c105, 1) == 12.6
# demand sd matters: if the true sd is 30 (stockout-censored history), stock moves
q30 = mu + 30 * z
print("stock if sd were 30:", round(q30, 2))
assert round(q30, 2) == 107.6

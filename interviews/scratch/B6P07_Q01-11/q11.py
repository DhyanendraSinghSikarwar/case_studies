import math
from scipy import stats
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
k1, n1, k0, n0 = 15, 1000, 36, 9000
p1, p0 = k1/n1, k0/n0
assert (p1, p0) == (0.015, 0.004)
pp = (k1 + k0) / (n1 + n0)
se = math.sqrt(pp*(1-pp)*(1/n1 + 1/n0))
z = (p1 - p0) / se
p_two = 2*(1 - stats.norm.cdf(z))
print(f"v12 {p1:.2%} (Wilson {wilson(k1,n1)[0]:.2%} to {wilson(k1,n1)[1]:.2%}); v11 {p0:.2%} (Wilson {wilson(k0,n0)[0]:.2%} to {wilson(k0,n0)[1]:.2%})")
print(f"difference {p1-p0:+.2%}; pooled SE {se:.4f}; z = {z:.2f}; two-sided p = {p_two:.1e}")
assert round(se, 4) == 0.0024 and round(z, 2) == 4.63 and p_two < 1e-4
# Exact check: Fisher
odds, pf = stats.fisher_exact([[k1, n1-k1], [k0, n0-k0]])
print(f"Fisher exact p = {pf:.1e}; odds ratio {odds:.2f}"); assert pf < 1e-3
# If v12 were as good as v11, expected failures in 1,000 requests and chance of seeing 15 or more
exp = n1*p0; tail = stats.binom.sf(k1-1, n1, p0)
print(f"expected {exp:.1f} failures if equal; P(>=15) = {tail:.1e}"); assert round(exp, 1) == 4.0 and tail < 1e-4
# Sequential peeking: how large must the difference be after only 100 canary requests to roll back? Using z >= 3 as a stop rule
# Pre-registered rule (illustrative): checkpoints every 250 requests; roll back if z >= 3 vs v11 AND v12 rate >= 0.4% + 0.5 points
def decide(kv, nv, kb=36, nb=9000):
    p_v = kv/nv; p_b = kb/nb; pooled = (kv+kb)/(nv+nb)
    s = math.sqrt(pooled*(1-pooled)*(1/nv+1/nb)); zz = (p_v-p_b)/s if s else 0
    return round(zz, 2), (zz >= 3 and p_v - p_b >= 0.005)
for kv, nv in [(4, 250), (7, 500), (11, 750), (15, 1000)]:
    print(f"checkpoint {nv:4d}: v12 failures {kv:2d} -> z, rollback = {decide(kv, nv)}")
assert decide(15, 1000)[1] is True and decide(4, 250)[1] is False
# Extra bad outputs if v12 went to 100% of 200,000 requests/day
extra = (p1 - p0) * 200_000
print(f"extra parse failures per day at 100% rollout of 200,000/day: {extra:,.0f}"); assert round(extra) == 2200

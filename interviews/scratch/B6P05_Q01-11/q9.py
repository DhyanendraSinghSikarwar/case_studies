import math
from scipy import stats
n = 20_000
arms = {"99": (99.0, 1000), "129": (129.0, 760)}
serve = 30.0
res = {}
for k, (price, subs) in arms.items():
    conv = subs / n
    rev = price * conv
    con = (price - serve) * conv
    res[k] = (conv, rev, con)
    print(f"price {k}: conversion {conv:.1%}, revenue/visitor {rev:.3f}, contribution/visitor {con:.3f}")
assert abs(res["99"][1] - 4.95) < 1e-9 and abs(res["129"][1] - 4.902) < 1e-9
assert abs(res["99"][2] - 3.45) < 1e-9 and abs(res["129"][2] - 3.762) < 1e-9
print(f"revenue difference (129 - 99) {res['129'][1]-res['99'][1]:+.3f}; contribution difference {res['129'][2]-res['99'][2]:+.3f} ({res['129'][2]/res['99'][2]-1:+.1%})")
def diff_test(m_a, p_a, m_b, p_b):
    d = m_b * p_b - m_a * p_a
    se = math.sqrt(m_a**2 * p_a * (1 - p_a) / n + m_b**2 * p_b * (1 - p_b) / n)
    return d, se, d / se, 2 * stats.norm.sf(abs(d / se))
pa, pb = 0.05, 0.038
d, se, z, p = diff_test(69, pa, 99, pb)
print(f"contribution: diff {d:.3f}, SE {se:.3f}, 95% CI {d-1.96*se:.3f} to {d+1.96*se:.3f}, z {z:.2f}, p {p:.3f}")
assert p > 0.05 and d - 1.96 * se < 0
d2, se2, z2, p2 = diff_test(99, pa, 129, pb)
print(f"revenue: diff {d2:.3f}, SE {se2:.3f}, z {z2:.2f}, p {p2:.2f}")
assert p2 > 0.5
# conversion difference itself
pp = (pa + pb) / 2
zc = (pa - pb) / math.sqrt(2 * pp * (1 - pp) / n)
print(f"conversion 5.0% vs 3.8%: z {zc:.1f}, p {2*stats.norm.sf(zc):.1e}")
assert zc > 5
# lifetime: higher price may churn faster. Margin per subscriber per month 69 vs 99.
for c99, c129 in ((0.06, 0.06), (0.06, 0.09), (0.06, 0.12)):
    l99 = 69 * pa / c99; l129 = 99 * pb / c129
    print(f"monthly churn {c99:.0%} vs {c129:.0%}: lifetime contribution/visitor {l99:.1f} vs {l129:.1f}")
c_be = 99 * pb / (69 * pa) * 0.06
print(f"129 stays better only if its churn is below {c_be:.1%} when 99 churns 6.0%")
assert abs(c_be - 0.0654) < 1e-3
# visitors needed per arm to see a 0.312 difference with SD about 0.17*sqrt(20000)
sd_pooled = se * math.sqrt(n) / math.sqrt(2)
need = 2 * ((1.96 + 0.84) * sd_pooled / d) ** 2
print(f"visitors per arm for 80% power at the observed difference: {need:,.0f}")
assert 40_000 < need < 100_000

# Q34 ad load up: ad revenue per user +9%, sessions per user -2%, ratings down (illustrative numbers)
import numpy as np
rng = np.random.default_rng(34)

# 1) Is the -2% sessions move real? simulate 200k users per arm, sessions/user/week
n = 200_000
ctrl = rng.poisson(10.0, n)
trt = rng.poisson(9.8, n)
d = trt.mean() - ctrl.mean()
se = np.sqrt(trt.var(ddof=1)/n + ctrl.var(ddof=1)/n)
rel = d / ctrl.mean()
lo, hi = (d - 1.96*se)/ctrl.mean(), (d + 1.96*se)/ctrl.mean()
print(f"sessions/user rel change {rel:+.2%}  95% CI [{lo:+.2%}, {hi:+.2%}]")
assert hi < -0.01          # even the optimistic end is worse than -1%

# 2) Cumulative revenue per starting user over weeks: control vs treatment
# revenue per ACTIVE user per week: 1.00 control, 1.09 treatment; weekly retention 97.0% vs 96.5% (invented)
def cum(rev, ret, weeks):
    alive, total = 1.0, 0.0
    for _ in range(weeks):
        total += alive * rev
        alive *= ret
    return total
cross = None
for w in range(1, 105):
    if cum(1.09, 0.965, w) < cum(1.00, 0.970, w):
        cross = w
        break
print("cumulative revenue crossover week:", cross)
for w in (4, 12, 26, 52):
    c, t = cum(1.00, 0.970, w), cum(1.09, 0.965, w)
    print(f"week {w:3d}: control {c:6.2f}  treatment {t:6.2f}  ratio {t/c:.3f}")
assert cum(1.09, 0.965, 4) > cum(1.00, 0.970, 4)
assert cross is not None and 20 <= cross <= 80
# 3) break-even weekly retention drop: treatment per-week revenue gain 9% is wiped out when
# (0.965/0.97)^t * 1.09 < 1 -> t > ln(1/1.09)/ln(0.965/0.97)
t_even = np.log(1/1.09)/np.log(0.965/0.97)
print(f"per-week revenue per starting user falls below control after {t_even:.1f} weeks")
assert 16 < t_even < 17.5
# 4) guardrail rule example
rule_ok = bool(hi > -0.01)    # CI upper bound must stay above -1%
print("guardrail 'sessions not worse than -1%' passes:", rule_ok)
assert not rule_ok

# Q37: LLM judge 620/1000, humans agree on 71% of 200 audited pairs, new answers 35% longer. Illustrative, seeded.
import numpy as np
from scipy import stats

n, w = 1000, 620
assert w / n == 0.62
def wilson(k, n, z=1.96):
    p = k / n; c = (p + z*z/(2*n)) / (1 + z*z/n)
    h = z * np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return c - h, c + h
lo, hi = wilson(w, n)
print(f"judge win rate 62.0%, 95% CI [{lo:.1%}, {hi:.1%}] (sampling noise only)")
assert 0.58 < lo < 0.60 and 0.64 < hi < 0.66

# invented audit table of 200 pairs: judge says new wins (Jn) / old wins (Jo); human says new (Hn) / old (Ho)
Jn_Hn, Jn_Ho, Jo_Hn, Jo_Ho = 80, 38, 20, 62
assert Jn_Hn + Jn_Ho + Jo_Hn + Jo_Ho == 200
agree = (Jn_Hn + Jo_Ho) / 200
print(f"agreement {agree:.0%}")
assert agree == 0.71
po = agree
pj = (Jn_Hn + Jn_Ho) / 200; ph = (Jn_Hn + Jo_Hn) / 200
pe = pj * ph + (1 - pj) * (1 - ph)
kappa = (po - pe) / (1 - pe)
print(f"Cohen kappa {kappa:.2f}")
tpr = Jn_Hn / (Jn_Hn + Jo_Hn)       # P(judge says new | human says new)
fpr = Jn_Ho / (Jn_Ho + Jo_Ho)       # P(judge says new | human says old)
print(f"judge says 'new' when humans say new: {tpr:.0%}; when humans say old: {fpr:.0%}")
# correct the 62% for judge error (Rogan-Gladen), bootstrap over the audit
def corrected(j, tpr, fpr): return (j - fpr) / (tpr - fpr)
h_hat = corrected(0.62, tpr, fpr)
print(f"error-corrected human-preference rate ~ {h_hat:.1%}")
rng = np.random.default_rng(37)
cells = np.array([Jn_Hn, Jn_Ho, Jo_Hn, Jo_Ho]); hs = []
for _ in range(4000):
    a, b, c, d = rng.multinomial(200, cells / 200)
    t, f = a / max(a + c, 1), b / max(b + d, 1)
    j = rng.binomial(n, 0.62) / n
    if t - f > 0.1: hs.append(corrected(j, t, f))
ci = np.percentile(hs, [2.5, 97.5])
print(f"bootstrap 95% interval for the corrected rate: [{ci[0]:.1%}, {ci[1]:.1%}]")
assert ci[0] < 0.5 < ci[1]   # the interval reaches 50%: no preference not ruled out
# length bias: a judge that adds a bonus for length prefers longer answers even at equal quality
rng = np.random.default_rng(371)
quality_diff = rng.normal(0, 1, 100_000)          # new minus old, true mean 0
for bonus in (0.0, 0.3, 0.8):
    wins = np.mean(quality_diff + bonus + rng.normal(0, 1, 100_000) > 0)
    print(f"true quality equal, judge length bonus {bonus:.1f} -> judge win rate {wins:.1%}")

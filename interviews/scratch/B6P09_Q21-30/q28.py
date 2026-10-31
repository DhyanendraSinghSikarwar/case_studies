# Q28 colour attribute filling (illustrative numbers; audit accuracies treated as projections)
from math import sqrt
total, missing = 2_000_000, 400_000
assert missing / total == 0.20
conf_n, low_n = 280_000, 120_000
assert conf_n + low_n == missing
acc_c, acc_l = 0.97, 0.78
wrong_c = conf_n * (1 - acc_c)
wrong_l = low_n * (1 - acc_l)
assert round(wrong_c) == 8_400 and round(wrong_l) == 26_400 and round(wrong_c + wrong_l) == 34_800
print(f"fill confident only: {wrong_c:,.0f} wrong of {conf_n:,}; fill all: {wrong_c+wrong_l:,.0f} wrong of {missing:,}")
print(f"the extra {low_n:,} fills add {wrong_l:,.0f} wrong ({1-acc_l:.0%} wrong) and {low_n-wrong_l:,.0f} right")

# Audit uncertainty: 1,000 items per audit, 95% normal-approx half-width
def hw(p, n=1000): return 1.96 * sqrt(p * (1 - p) / n)
hc, hl = hw(acc_c), hw(acc_l)
print(f"audit half-widths: confident +-{hc:.1%} -> wrong range {conf_n*(1-acc_c-hc):,.0f} to {conf_n*(1-acc_c+hc):,.0f}; "
      f"rest +-{hl:.1%} -> {low_n*(1-acc_l-hl):,.0f} to {low_n*(1-acc_l+hl):,.0f}")
assert 0.010 < hc < 0.012 and 0.025 < hl < 0.027

# Decision: fill only where accuracy exceeds C/(B+C). Invented values: benefit of a right fill B=1, cost of a wrong fill C=5
B, C = 1.0, 5.0
be = C / (B + C)
assert abs(be - 5/6) < 1e-12
for name, a in (("confident", acc_c), ("rest", acc_l)):
    gain = a * B - (1 - a) * C
    print(f"{name}: accuracy {a:.0%}, net value per fill {gain:+.2f} (break-even accuracy {be:.1%})")
assert 0.97 * B - 0.03 * C > 0 and 0.78 * B - 0.22 * C < 0
# Human review of the rest: what accuracy after review if a reviewer fixes 80% of its errors (invented)?
fixed = low_n * (1 - acc_l) * 0.8
print(f"review of the rest at 80% error catch: wrong falls from {wrong_l:,.0f} to {wrong_l-fixed:,.0f}")
assert round(wrong_l - fixed) == 5_280

# Q24: streaming LTV and CAC payback (illustrative)
import numpy as np
rev, gm, churn, cac = 10.0, 0.70, 0.05, 60.0
margin = rev * gm                       # 7.0 per subscriber-month
ltv = margin / churn
print(f"margin/month {margin:.2f}  LTV (margin/churn) {ltv:.1f}  LTV/CAC {ltv/cac:.2f}  simple payback {cac/margin:.2f} months  mean lifetime {1/churn:.0f} months")
assert abs(margin - 7) < 1e-9 and abs(ltv - 140) < 1e-9 and abs(ltv / cac - 2.3333) < 1e-3 and abs(cac / margin - 8.5714) < 1e-3

# payback WITH churn: cumulative margin per acquired subscriber, month m collects margin * survival
months = np.arange(1, 400)
surv = (1 - churn) ** (months - 1)      # first month paid in full
cum = np.cumsum(margin * surv)
pay = int(months[np.argmax(cum >= cac)])
print("payback with 5% constant churn: month", pay, f"(cumulative margin {cum[pay-1]:.1f})")
assert pay == 11 and cum[pay - 2] < cac <= cum[pay - 1]
assert abs(cum[-1] - ltv) < 1e-6        # the sum of margin x survival converges to margin/churn

# churn that falls with tenure: 12% in months 1-3, 3% afterwards
def cohort_ltv(hazards, n=2000):
    s, tot = 1.0, 0.0
    for m in range(1, n + 1):
        tot += margin * s
        s *= 1 - hazards(m)
    return tot
h = lambda m: 0.12 if m <= 3 else 0.03
true_ltv = cohort_ltv(h)
# the cohort-average churn = churn events / subscriber-months, i.e. weighted by survival
s, base, w = 1.0, [], []
for m in range(1, 3000):
    base.append(h(m)); w.append(s); s *= 1 - h(m)
blend = float(np.average(base, weights=w))
print(f"hazard 12% for 3 months then 3%: true cohort LTV {true_ltv:.1f}")
for name, c in (("first-month churn 12%", 0.12), ("late-tenure churn 3%", 0.03), (f"cohort-average churn {blend:.4f}", blend)):
    print(f"  formula with {name}: {margin/c:.1f}")
assert abs(margin / blend - true_ltv) < 0.01
assert margin / 0.12 < true_ltv < margin / 0.03
assert abs(true_ltv - (margin * (1 + .88 + .88**2) + margin * .88**3 / 0.03)) < 1e-6

# discounting at 1% a month (a monthly rate of about 12.7% a year) with the plain 5% churn
d = 0.01
ltv_d = margin * (1 + d) / (churn + d)      # first month undiscounted
print(f"with 1%/month discounting, constant 5% churn: LTV {ltv_d:.1f}")
assert 110 < ltv_d < 120

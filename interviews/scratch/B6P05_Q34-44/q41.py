r3 = 0.70
r1 = r3 ** (1 / 3)
churn = 1 - r1
r12 = r3 ** 4
ltv = 10 / churn
print(f"monthly retention {r1:.4f}; churn {churn:.4f}; 12-month retention {r12:.4f}; LTV {ltv:.1f}")
assert abs(churn - 0.1121) < 5e-4 and abs(r12 - 0.2401) < 1e-9 and abs(ltv - 89.2) < 0.1
old = 0.40
print(f"old cohorts hold {old:.0%} at 12 months vs {r12:.1%} predicted: {old/r12:.2f}x")
# hazard between month 3 and 12 implied by the two points
r_late = (old / r3) ** (1 / 9)
churn_late = 1 - r_late
print(f"implied churn months 3-12: {churn_late:.4f} (first 3 months {churn:.4f})")
assert churn_late < churn
# LTV with early churn then late churn, same convention as margin/churn (sum of survival from t=0)
first = sum(r1 ** t for t in range(3))
tail = r3 / (1 - r_late)
ltv2 = 10 * (first + tail)
print(f"two-stage LTV (tail to infinity) {ltv2:.1f}")
# 12-month capped LTV (months 0..11 active-start) for both curves
cap_const = 10 * sum(r1 ** t for t in range(12))
cap_two = 10 * (first + sum(r3 * r_late ** k for k in range(9)))
print(f"12-month margin per sign-up: constant-churn {cap_const:.1f}; two-stage {cap_two:.1f}")
assert cap_const < cap_two < ltv2
assert ltv2 > ltv

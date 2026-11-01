import math
spend, cust, m, churn = 1_200_000, 6000, 25.0, 0.05
cac = spend / cust
simple = cac / m
ltv = m / churn
print(f"CAC {cac:.0f}; simple payback {simple:.1f} months; LTV {ltv:.0f}; LTV/CAC {ltv/cac:.2f}")
assert cac == 200 and simple == 8 and ltv == 500 and abs(ltv / cac - 2.5) < 1e-12
# churn-adjusted payback: customer pays month 1 in full; each later month with survival 0.95^(k-1)
cum = 0.0; month = 0
while cum < cac:
    month += 1
    cum += m * (1 - churn) ** (month - 1)
    if month in (8, 9, 10): print(f"  month {month}: cumulative margin per acquired customer {cum:.2f}")
print(f"payback with churn: {month} months")
assert month == 10
closed = math.log(1 - cac * churn / m) / math.log(1 - churn)
print(f"closed form n = ln(1 - CAC*churn/margin)/ln(1-churn) = {closed:.2f}")
assert abs(closed - 9.96) < 0.01
# cohort view: 6,000 customers, cash back after 8 and 10 months
alive = [cust * (1 - churn) ** k for k in range(12)]
cash8 = sum(a * m for a in alive[:8]); cash10 = sum(a * m for a in alive[:10])
print(f"cohort margin after 8 months {cash8:,.0f}; after 10 months {cash10:,.0f}; spend {spend:,}")
assert cash8 < spend < cash10
# the limit: payback is impossible if CAC*churn >= margin
print(f"never pays back if CAC > margin/churn = {ltv:.0f}")
# sensitivity: churn 7% instead of 5%
c2 = 0.07
n2 = math.log(1 - cac * c2 / m) / math.log(1 - c2)
print(f"at 7% churn: LTV {m/c2:.0f}, LTV/CAC {m/c2/cac:.2f}, payback {math.ceil(n2)} months")
assert math.ceil(n2) == 12 and abs(m / c2 / cac - 1.786) < 0.001

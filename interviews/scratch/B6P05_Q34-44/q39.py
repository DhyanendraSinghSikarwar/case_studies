import math
tickets, resolved = 100_000, 45_000
saving = resolved * (6.00 - 0.80)
extra_churn = 0.005 * resolved
churn_cost = extra_churn * 400
net = saving - churn_cost - 60_000
print(f"saving {saving:,.0f}; extra churners {extra_churn:,.0f}; churn cost {churn_cost:,.0f}; net {net:,.0f}")
assert round(saving) == 234_000 and round(extra_churn) == 225 and round(churn_cost) == 90_000 and round(net) == 84_000
be_gap = (saving - 60_000) / (resolved * 400)
print(f"churn gap that wipes out the value: {be_gap*100:.2f} points")
assert abs(be_gap - 174_000 / 18_000_000) < 1e-12
# is 3.0% vs 2.5% distinguishable? holdout size is NOT given; try sizes (45,000 in agent arm assumed)
for h in (2_000, 5_000, 20_000):
    se = math.sqrt(0.03 * 0.97 / resolved + 0.025 * 0.975 / h)
    z = 0.005 / se
    lo, hi = 0.005 - 1.96 * se, 0.005 + 1.96 * se
    net_hi = saving - 60_000 - hi * resolved * 400
    net_lo = saving - 60_000 - lo * resolved * 400
    print(f"holdout {h:>6,}: z {z:.2f}; gap CI {lo*100:.2f}..{hi*100:.2f} pts; net CI {net_hi:,.0f}..{net_lo:,.0f}")
se5 = math.sqrt(0.03 * 0.97 / resolved + 0.025 * 0.975 / 5_000)
assert 2.0 < 0.005 / se5 < 2.3

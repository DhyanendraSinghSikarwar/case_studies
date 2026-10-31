# Q30: delivery promise, median vs 80th percentile (illustrative)
orders, margin, late_cost = 100_000, 1.50, 3.00
# A: median promise
lateA = 0.50 * orders
netA = orders * margin - lateA * late_cost
# B: 80th percentile promise, 1% fewer orders
ordersB = orders * 0.99
lateB_exact = 0.20 * ordersB          # 20% of the orders that remain = 19,800
for name, lb in (("20% of 99,000 = 19,800", lateB_exact),):
    netB = ordersB * margin - lb * late_cost
    print(f"B with {name}: margin {ordersB*margin:,.0f} - refunds {lb*late_cost:,.0f} = {netB:,.0f}; A = {netA:,.0f}; B - A = {netB-netA:+,.0f}")
assert netA == 0 and ordersB * margin == 148_500
assert abs(lateB_exact - 19_800) < 1e-9
assert abs((ordersB * margin - lateB_exact * late_cost) - 89_100) < 1e-6

# per-order view
print(f"per order: A {margin-0.5*late_cost:.2f}; B {margin-0.2*late_cost:.2f}")
assert abs((margin - 0.5 * late_cost)) < 1e-12 and abs(margin - 0.2 * late_cost - 0.9) < 1e-12

# sensitivity to the late cost c and the order loss d
def net(share_late, d, c): 
    o = orders * (1 - d)
    return o * (margin - share_late * c)
print("late cost c: B-A")
for c in (3.0, 1.0, 0.5, 0.05, 0.0):
    print(f"  c={c:4.2f}: {net(0.2, 0.01, c) - net(0.5, 0.0, c):+,.0f}")
c_flip = (margin - margin * 0.99) / (0.5 - 0.2 * 0.99)
print(f"break-even late cost {c_flip:.4f}")
assert abs(c_flip - 0.0497) < 1e-3
print("order loss d: B-A at c=3.00 and at c=1.00")
for d in (0.01, 0.10, 0.30, 0.50):
    print(f"  d={d:.0%}: c=3.00 {net(0.2, d, 3.0) - net(0.5, 0, 3.0):+,.0f}; c=1.00 {net(0.2, d, 1.0) - net(0.5, 0, 1.0):+,.0f}")
d_flip = 1 - net(0.5, 0, 1.0) / net(0.2, 0, 1.0)
print(f"order loss that wipes out the gain at c=1.00: {d_flip:.1%}")
assert abs(d_flip - 0.2308) < 1e-3 and net(0.2, 0.30, 3.0) > net(0.5, 0, 3.0)

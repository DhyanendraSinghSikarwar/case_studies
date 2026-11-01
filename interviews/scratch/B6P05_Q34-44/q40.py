import math
v = 100_000
c5, c3 = 0.06 * v, 0.09 * v
rev5, rev3 = c5 * 5, c3 * 3
con5, con3 = c5 * (5 - 1), c3 * (3 - 1)
print(f"price 5: subs {c5:,.0f}, revenue {rev5:,.0f}, contribution {con5:,.0f}")
print(f"price 3: subs {c3:,.0f}, revenue {rev3:,.0f}, contribution {con3:,.0f}")
assert round(c5) == 6_000 and round(c3) == 9_000
assert round(rev5) == 30_000 and round(rev3) == 27_000
assert round(con5) == 24_000 and round(con3) == 18_000
assert abs(0.09 / 0.06 - 1 - 0.5) < 1e-9
leak = 1_000 * (5 - 3)
net = con3 - con5 - leak
print(f"leakage {leak:,.0f}; contribution change {con3-con5:,.0f}; after leakage {net:,.0f}")
assert leak == 2_000 and net == -8_000
print(f"break-even conversion at price 3: contribution {24_000/(2*v):.1%}, revenue {30_000/(3*v):.1%}")
assert abs(24_000 / (2 * v) - 0.12) < 1e-9 and abs(30_000 / (3 * v) - 0.10) < 1e-9
# the 6% vs 9% gap is not noise
p = 0.075
z = 0.03 / math.sqrt(2 * p * (1 - p) / v)
print(f"z for conversion gap {z:.1f}")
assert z > 20
# leakage size that would not matter: how many switchers keep the price-3 plan equal to price 5?
print(f"gap before leakage is {con3-con5:,.0f}; negative already, so no leakage level rescues it")

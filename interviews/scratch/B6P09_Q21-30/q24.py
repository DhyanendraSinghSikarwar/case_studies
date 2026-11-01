# Q24 cart reminder with 10% code (illustrative numbers)
from math import sqrt
n = 10_000
t_buy, c_buy = 600, 500
assert t_buy / n == 0.06 and c_buy / n == 0.05
incr = t_buy - c_buy
assert incr == 100
aov, margin = 800, 0.25
unit_margin = aov * margin
assert unit_margin == 200
incr_margin = incr * unit_margin
assert incr_margin == 20_000
disc_each = 0.10 * aov
discount_all = t_buy * disc_each
assert disc_each == 80 and discount_all == 48_000
net = incr_margin - discount_all
assert net == -28_000
print(f"incremental orders {incr}, margin on them {incr_margin:,.0f}, discount if all 600 use code {discount_all:,.0f}, net {net:,.0f}")

# Is 6.0% vs 5.0% a real lift? two-proportion z
p = (t_buy + c_buy) / (2 * n)
se = sqrt(p * (1 - p) * 2 / n)
z = (0.06 - 0.05) / se
assert 3.0 < z < 3.2
print(f"z = {z:.2f}")

# Break-even incremental orders x with all buyers using the code: x*200 = (500+x)*80
x = 500 * disc_each / (unit_margin - disc_each)
assert abs(x - 333.333) < 0.01
print(f"break-even incremental orders per 10,000: {x:.0f} (purchase rate {(500+x)/n:.2%} vs 5.00% baseline)")

# Net per 10,000 if only a share of purchasers redeem (invented redemption rates)
for r in (1.0, 0.7, 0.5):
    cost = r * t_buy * disc_each
    print(f"redemption {r:.0%}: discount {cost:,.0f}, net {incr_margin - cost:,.0f}")
assert incr_margin - 0.5 * t_buy * disc_each == -4_000
be = incr_margin / (t_buy * disc_each)
assert abs(be - 0.41667) < 1e-4
print(f"break-even redemption (same 100 extra orders): {be:.1%}")
# Smaller offer: 5% off with the same 100 incremental (only if lift held, a big if)
small = 0.05 * aov * t_buy
print(f"5% code, same lift, 100% redemption: discount {small:,.0f}, net {incr_margin - small:,.0f}")
assert small == 24_000 and incr_margin - small == -4_000

import math
from scipy import stats
n = 10_000
t_orders, c_orders = 3000, 2000
basket, margin, disc = 50, 20, 10
t_profit = t_orders * (margin - disc)
c_profit = c_orders * margin
print(f"treated margin after coupons {t_profit:,}; control margin {c_profit:,}; campaign effect {t_profit - c_profit:+,}")
assert (t_profit, c_profit, t_profit - c_profit) == (30000, 40000, -10000)
inc = t_orders - c_orders
print(f"incremental orders {inc:,} ({inc/c_orders:+.0%} relative); coupon cost {t_orders*disc:,}; margin on incremental orders {inc*margin:,}")
assert inc == 1000 and t_orders * disc == 30000 and inc * margin == 20000
print(f"loss per incremental order {(c_profit - t_profit)/inc:.1f}; give-away to would-have-ordered customers {c_orders*disc:,}")
be = c_profit / (n * (margin - disc))
print(f"break-even order rate in coupon group {be:.0%} (observed 30%)")
assert abs(be - 0.40) < 1e-12
# is the lift real? two-proportion z test
p = (t_orders + c_orders) / (2 * n)
z = (0.30 - 0.20) / math.sqrt(2 * p * (1 - p) / n)
print(f"z for 30% vs 20%: {z:.1f}  p = {2*stats.norm.sf(z):.2g}")
assert z > 15
# what would the discount need to be to break even at 30% vs 20%?
d_star = margin - c_profit / t_orders
print(f"largest break-even discount at these order rates: {d_star:.2f} per order")
assert abs(d_star - 6.6667) < 1e-3

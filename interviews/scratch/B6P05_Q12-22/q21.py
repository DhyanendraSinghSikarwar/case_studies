import math
# Illustrative numbers.
hh, n, k = 2_000_000, 1000, 300
p = k / n
users = hh * p
orders = users * 3
value = orders * 12
print(f"users {users:,.0f}; orders {orders:,.0f}; market value {value:,.0f}")
assert (users, orders, value) == (600_000, 1_800_000, 21_600_000)
entrant_orders = 0.25 * orders; entrant_value = 0.25 * value
print(f"25% share: {entrant_orders:,.0f} orders, {entrant_value:,.0f} a month")
assert (entrant_orders, entrant_value) == (450_000, 5_400_000)
se = math.sqrt(p * (1 - p) / n); moe = 1.96 * se
print(f"standard error {se:.4f}; 95% margin of error {moe:.2%} points; interval {p-moe:.2%}-{p+moe:.2%}")
assert round(moe, 4) == 0.0284
lo, hi = (p - moe) * hh, (p + moe) * hh
print(f"user households {lo:,.0f}-{hi:,.0f}; market value {lo*3*12:,.0f}-{hi*3*12:,.0f} ({moe/p:.1%} either way)")
# Finite population correction is negligible
fpc = math.sqrt((hh - n) / (hh - 1)); print("finite-population factor", round(fpc, 5))
assert fpc > 0.9997
# Design effect: a clustered or phone survey with deff 2 widens the margin
moe2 = 1.96 * math.sqrt(2) * se
print(f"with design effect 2: margin {moe2:.2%}")
assert round(moe2, 3) == 0.040
# Which input moves the answer most? Plausible ranges for each, one at a time, around 21.6M market value.
base = value
sens = {
 "usage share (survey margin)":      (0.2716 * hh * 3 * 12, 0.3284 * hh * 3 * 12),
 "orders per user 2 to 4":           (users * 2 * 12, users * 4 * 12),
 "order value 10 to 14":             (orders * 10, orders * 14),
}
for kk, (a, b) in sens.items():
    print(f"{kk:30} {a:>12,.0f} to {b:>12,.0f}  (spread {(b-a)/base:.0%} of base)")
assert round((sens["orders per user 2 to 4"][1] - sens["orders per user 2 to 4"][0]) / base, 2) == 0.67
# The entrant's own 25% target: what it implies in users at equal frequency
print("25% of orders at equal frequency = 25% of the 600,000 users =", 0.25 * users)
assert 0.25 * users == 150_000

searches = 10_000_000
moved = (0.08 - 0.06) * searches
conv_gain = 0.030 - 0.005
orders = moved * conv_gain
margin = orders * 4.00
print(f"searches moved to useful {moved:,.0f}; extra orders {orders:,.0f}; extra margin {margin:,.0f} per day")
assert round(moved) == 200_000 and round(orders) == 5_000 and round(margin) == 20_000
assert abs((0.08 - 0.06) / 0.08 - 0.25) < 1e-9
# upper bound: what if the rescued searches only convert part of the 3.0% (illustrative)
for share in (1.0, 0.6, 0.4, 0.2):
    c = 0.005 + share * conv_gain
    m = moved * (c - 0.005) * 4.00
    print(f"rescued searches reach {c:.2%} conversion -> {m:,.0f} per day")
m40 = moved * (0.4 * conv_gain) * 4.00
assert round(m40) == 8_000
# the same arithmetic, on the share of searches rather than as a rate
base_orders = searches * (0.08 * 0.005 + 0.92 * 0.030)
new_orders = searches * (0.06 * 0.005 + 0.94 * 0.030)
print(f"total orders {base_orders:,.0f} -> {new_orders:,.0f}; difference {new_orders-base_orders:,.0f}")
assert round(new_orders - base_orders) == 5_000

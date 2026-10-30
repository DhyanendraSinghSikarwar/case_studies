import math
price, fee, fixed = 4.00, 0.12, 90_000
c1 = price - 1.10 - fee
c2 = price - 2.50 - fee
n1, n2 = fixed / c1, fixed / c2
print(f"contribution {c1:.2f} -> break-even {n1:,.1f} -> {math.ceil(n1):,} subscribers")
print(f"contribution {c2:.2f} -> break-even {n2:,.1f} -> {math.ceil(n2):,} subscribers")
assert abs(c1 - 2.78) < 1e-9 and math.ceil(n1) == 32_375
assert abs(c2 - 1.38) < 1e-9 and math.ceil(n2) == 65_218
print(f"ratio {n2/n1:.2f}x; inference cost at which contribution is zero: {price-fee:.2f}")
assert abs(n2 / n1 - 2.0144) < 1e-3
# a mix: 80% light users at 0.90, 20% heavy at 6.20 gives mean 2.14
mean = 0.8 * 1.00 + 0.2 * 8.50
print(f"example mix (80% at 1.00, 20% at 8.50) has mean {mean:.2f}; a heavy user alone makes {price-8.50-fee:.2f} per month")
assert abs(mean - 2.50) < 1e-9
assert price - 8.50 - fee < 0

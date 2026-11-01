import math
api_per_m, fixed = 0.60, 6000.0
volume = 3000.0                       # million tokens a month
api_now = api_per_m * volume
be = fixed / api_per_m
print(f"API bill now {api_now:,.0f}; self-host fixed {fixed:,.0f}; break-even {be:,.0f} million tokens a month ({be/volume:.2f}x today)")
assert abs(api_now - 1800) < 1e-9 and abs(be - 10000) < 1e-9
print(f"at today's volume the API is cheaper by {fixed - api_now:,.0f} a month")
assert fixed - api_now == 4200
# sensitivity of break-even to API price and to the self-host bill (illustrative scenarios)
for price, fx in [(0.60, 6000), (0.30, 6000), (0.60, 9000), (0.60, 12000)]:
    print(f"  price {price:.2f}, self-host {fx:,}: break-even {fx/price:,.0f}M tokens")
assert 6000/0.30 == 20000 and abs(9000/0.60 - 15000) < 1e-9
# how long to grow into break-even at an illustrative 10% monthly growth
months = math.log(be/volume) / math.log(1.10)
print(f"months to reach break-even at 10% monthly growth: {months:.1f} -> {math.ceil(months)}")
assert math.ceil(months) == 13
# cumulative cost over 12 months at 10% growth
api_tot = sum(api_per_m*volume*1.1**m for m in range(12)); self_tot = fixed*12
print(f"12-month totals at 10% growth: API {api_tot:,.0f} vs self-host {self_tot:,.0f}")
assert api_tot < self_tot

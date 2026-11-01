# Q28 delivery fee Rs 20 -> Rs 30 on small orders (illustrative numbers)
small0, large0 = 60_000, 40_000        # weekly orders before
small_aov, large_aov = 150, 375
commission = 0.20
fee0, fee1 = 20, 30
small1 = 54_000                        # small orders fall 10%; large unchanged -> total falls 6%
large1 = 40_000

def rev(small, large, fee):
    return small * (small_aov * commission + fee) + large * (large_aov * commission)

r0, r1 = rev(small0, large0, fee0), rev(small1, large1, fee1)
print("orders before/after:", small0 + large0, small1 + large1, " change:", round((small1 + large1) / (small0 + large0) - 1, 3))
print("revenue before/after:", r0, r1, " change:", round(r1 / r0 - 1, 3))
assert small0 + large0 == 100_000 and small1 + large1 == 94_000
assert r0 == 6_000_000 and r1 == 6_240_000 and round(r1 / r0 - 1, 3) == 0.04

# contribution after a rider cost of Rs 60 per small order
rider = 60
c0 = small0 * (small_aov * commission + fee0 - rider)
c1 = small1 * (small_aov * commission + fee1 - rider)
print("small-order contribution before/after (Rs):", c0, c1)
assert c0 == -600_000 and c1 == 0

# halo: how many large orders can be lost before the revenue gain is gone?
gain = r1 - r0
large_order_rev = large_aov * commission
breakeven_orders = gain / large_order_rev
print("revenue gain:", gain, " breakeven lost large orders:", breakeven_orders, " as share of large:", breakeven_orders / large0)
assert gain == 240_000 and breakeven_orders == 3200 and breakeven_orders / large0 == 0.08

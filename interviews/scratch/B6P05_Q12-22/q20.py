# Illustrative numbers. Assumption: commission is on the basket before the platform-funded discount.
basket = 20.0
commission = 0.18 * basket
fee = 2.00
revenue = commission + fee
costs = {"courier": 3.50, "discounts": 1.50, "payment fees": 0.40, "support": 0.30}
total_cost = sum(costs.values())
contrib = revenue - total_cost
print(f"commission {commission:.2f} + fee {fee:.2f} = revenue {revenue:.2f}; costs {total_cost:.2f}; contribution {contrib:+.2f}")
assert round(commission, 2) == 3.60 and round(revenue, 2) == 5.60 and round(total_cost, 2) == 5.70 and round(contrib, 2) == -0.10
# Break-even commission rate holding all else fixed
be_rate = (total_cost - fee) / basket
print(f"break-even commission rate {be_rate:.2%}")
assert round(be_rate, 4) == 0.185
# Lever table (each applied alone). Illustrative sizes of the move.
levers = {
 "targeted discounts: cut 1.50 to 1.00":        0.50,
 "batching: courier cost 3.50 to 3.00":         0.50,
 "delivery fee 2.00 to 2.50":                   0.50,
 "commission 18% to 19%":                       0.01 * basket,
 "basket 20 to 22 (more items per order)":      0.18 * 2.0,
}
for k, v in levers.items():
    print(f"{k:45} {v:+.2f} per order -> contribution {contrib+v:+.2f}")
assert round(contrib + 0.50, 2) == 0.40 and round(contrib + 0.20, 2) == 0.10 and round(contrib + 0.36, 2) == 0.26
# Volume risk: if a 0.50 fee rise cuts orders by 10%, per-1,000-orders result
before = 1000 * contrib; after = 900 * (contrib + 0.50)
print(f"per 1,000 orders: {before:+.0f} before; fee rise with 10% fewer orders {after:+.0f}")
assert round(before) == -100 and round(after) == 360

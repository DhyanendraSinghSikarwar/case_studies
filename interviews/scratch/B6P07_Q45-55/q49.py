users, heavy, light = 100_000, 5_000, 95_000
price, per_call = 5.0, 0.012
calls = heavy*1500 + light*60
cost = calls*per_call
rev = users*price
print(f"calls = {calls:,}, cost = {cost:,.0f}, revenue = {rev:,.0f}, margin = {rev-cost:,.0f} ({(rev-cost)/rev:.1%})")
assert calls == 13_200_000 and abs(cost-158_400) < 1e-6 and rev == 500_000
h_cost = 1500*per_call; l_cost = 60*per_call
print(f"heavy user cost {h_cost:.2f}, margin {price-h_cost:.2f} ({(price-h_cost)/price:.0%} of revenue)")
print(f"light user cost {l_cost:.2f}, margin {price-l_cost:.2f}")
assert abs(h_cost-18) < 1e-9 and abs(price-h_cost+13) < 1e-9 and abs(l_cost-0.72) < 1e-9
print(f"heavy users: {heavy} x {price-h_cost:.0f} = {heavy*(price-h_cost):,.0f}; light users: {light*(price-l_cost):,.0f}")
assert abs(heavy*(price-h_cost) + 65_000) < 1e-6 and abs(light*(price-l_cost) - 406_600) < 1e-6
print(f"heavy share of calls (and cost) = {heavy*1500/calls:.1%}, share of users = {heavy/users:.0%}")
assert round(heavy*1500/calls, 3) == 0.568
be = price/per_call
print(f"break-even calls per user per month at price 5 = {be:.1f}")
assert round(be, 1) == 416.7
# option A: 400 included calls, overage 0.02 per call
inc, over = 400, 0.02
def user_margin(c):
    rev_u = price + max(0, c-inc)*over
    return rev_u - c*per_call
print(f"option A (400 included, overage 0.02): heavy margin {user_margin(1500):.2f}, light margin {user_margin(60):.2f}")
assert abs(user_margin(1500) - 9.0) < 1e-9
# option B: hard cap at 400 calls, no overage, heavy users stay at 5
print(f"option B (hard cap 400): heavy cost {400*per_call:.2f}, margin {price-400*per_call:.2f}")
assert abs(price-400*per_call-0.2) < 1e-9
# option C: route heavy usage to a model costing 40% less per call
c2 = 0.012*0.6
print(f"option C (cheaper model for calls above 400, -40% cost): heavy cost {400*per_call+1100*c2:.3f}")
assert abs(400*per_call+1100*c2 - 12.72) < 1e-9
print(f"average cost per user = {cost/users:.3f}")
assert abs(cost/users - 1.584) < 1e-9
assert abs(5 - 18 + 27 - 18 - 9 + 13) < 1e-9 and 5 + 1100*0.02 == 27

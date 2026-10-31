# Q22 size widget claim (illustrative numbers)
orders, ret = 100_000, 12_000
w_n, o_n = 20_000, 80_000
w_rate, o_rate = 0.08, 0.13
w_ret, o_ret = w_n * w_rate, o_n * o_rate
assert w_ret == 1_600 and o_ret == 10_400 and w_ret + o_ret == ret
assert ret / orders == 0.12 and w_n + o_n == orders

gap_pts = o_rate - w_rate
avoided_claim = o_n * gap_pts
saving_claim = avoided_claim * 150
assert abs(gap_pts - 0.05) < 1e-12 and round(avoided_claim) == 4_000 and round(saving_claim) == 600_000
print(f"claimed: {avoided_claim:.0f} avoided returns, saving {saving_claim:,.0f}")

# Haircut 1: only some of the 80,000 will use the widget (today 20%)
use = w_n / orders
assert use == 0.2
# Haircut 2: only part of the 5-point gap is causal (invented: 2 points among users)
causal = 0.02
avoided_adj = o_n * use * causal
saving_adj = avoided_adj * 150
assert round(avoided_adj) == 320 and round(saving_adj) == 48_000
print(f"adjusted (20% use, 2-pt causal effect among users): {avoided_adj:.0f} avoided, saving {saving_adj:,.0f}")

# Selection story: if widget users were already lower-return, gap with zero causal effect
# Invented: engaged shoppers return 8% by themselves, others 13%: widget does nothing.
print(f"gap with zero causal effect is still {gap_pts*100:.0f} points in that world")

# Sample size for a randomized test to detect a 1-point drop from 13% (alpha 0.05, power 0.8), per arm
from statistics import NormalDist
z = NormalDist().inv_cdf
p1, p2 = 0.13, 0.12
n = (z(0.975) + z(0.8)) ** 2 * (p1*(1-p1) + p2*(1-p2)) / (p1 - p2) ** 2
assert 17_000 < n < 18_000
print(f"orders per arm to detect 13% -> 12%: {n:,.0f}")

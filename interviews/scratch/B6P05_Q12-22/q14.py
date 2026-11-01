import math
# Illustrative numbers. Randomized test: offer vs control, 10,000 each per risk group.
n = 10_000; cost = 3.0; value = 120.0
groups = {"high-risk": (0.30, 0.32), "mid-risk": (0.10, 0.14)}   # (churn offered, churn control)
be = cost / value
print(f"break-even uplift (absolute churn reduction) = {be:.2%}")
assert round(be, 4) == 0.025
for g, (po, pc) in groups.items():
    up = pc - po
    se = math.sqrt(po * (1 - po) / n + pc * (1 - pc) / n)
    lo, hi = up - 1.96 * se, up + 1.96 * se
    net = up * value - cost
    net_lo, net_hi = lo * value - cost, hi * value - cost
    print(f"{g:10} uplift {up:.2%} (95% {lo:.2%} to {hi:.2%}, z={up/se:.1f})  net per offered {net:+.2f} "
          f"(95% {net_lo:+.2f} to {net_hi:+.2f})  total {net*n:+,.0f}")
    groups[g] = (po, pc, up, se, net, net_lo, net_hi)
assert round(groups["high-risk"][4], 2) == -0.60 and round(groups["mid-risk"][4], 2) == 1.80
assert round(groups["high-risk"][4] * n) == -6000 and round(groups["mid-risk"][4] * n) == 18000
# The high-risk loss is NOT statistically established: its interval includes break-even.
assert groups["high-risk"][5] < 0 < groups["high-risk"][6]
assert groups["mid-risk"][5] > 0           # the mid-risk gain is clearly positive
# Who would each model pick? Propensity ranks by churn probability; uplift ranks by uplift.
prop_order = sorted(groups, key=lambda g: -groups[g][1])     # control churn = natural churn risk
upl_order = sorted(groups, key=lambda g: -groups[g][2])
print("propensity picks first:", prop_order[0], "| uplift picks first:", upl_order[0])
assert prop_order[0] == "high-risk" and upl_order[0] == "mid-risk"
# Budget view: 10,000 coupons only. Propensity model spends them on high-risk, uplift on mid-risk.
print("10,000 coupons: propensity", round(groups["high-risk"][4] * n), "uplift", round(groups["mid-risk"][4] * n))

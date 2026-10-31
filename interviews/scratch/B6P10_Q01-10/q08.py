# Q8 notification targeting: illustrative numbers from the prompt
users, cap, budget, price = 3_000_000, 3, 120_000, 0.02
pushes = round(budget / price)
cap_total = users * cap
assert_binds = pushes < cap_total
hi_share, g_hi, g_lo = 0.30, 0.015, 0.003      # opens per push (percentage points / 100)
hi, lo = int(users * hi_share), int(users * (1 - hi_share))
# A: spread evenly
each = pushes / users
even = hi * each * g_hi + lo * each * g_lo
# B: 3 pushes to every high-uplift user first, remainder to the others (under the cap)
hi_push = hi * cap
rest = pushes - hi_push
lo_each = rest / lo
targeted = hi_push * g_hi + rest * g_lo
print(f"pushes {pushes:,} vs cap total {cap_total:,}; budget binds: {assert_binds}")
print(f"high {hi:,}, low {lo:,}; even each {each:.1f}")
print(f"even: high {hi*each*g_hi:,.0f} + low {lo*each*g_lo:,.0f} = {even:,.0f}")
print(f"targeted: high {hi_push*g_hi:,.0f} + low {rest*g_lo:,.0f} = {targeted:,.0f}; low users get {lo_each:.3f} each")
print(f"gain {targeted-even:,.0f} extra opens/week = {targeted/even-1:.1%} more")
# illustrative sampling error on the 1.5-point estimate (assumed 10% base open rate, 22,500 per arm)
import math
n_arm, p = 22_500, 0.10
se = math.sqrt(2 * p * (1 - p) / n_arm)
print(f"illustrative SE of a difference {se*100:.2f} points, 95% half-width {1.96*se*100:.2f}")
# if the true high-uplift gain were 1.0 point instead of 1.5
t2 = hi_push * 0.010 + rest * g_lo
e2 = hi * each * 0.010 + lo * each * g_lo
print(f"if high gain is 1.0 point: targeted {t2:,.0f} vs even {e2:,.0f}, gain {t2-e2:,.0f}")
assert pushes == 6_000_000 and cap_total == 9_000_000 and assert_binds
assert hi == 900_000 and lo == 2_100_000 and each == 2.0
assert round(even) == 39_600 and hi_push == 2_700_000 and rest == 3_300_000
assert round(lo_each, 3) == 1.571 and lo_each < cap
assert round(targeted) == 50_400 and round(targeted - even) == 10_800 and round(targeted / even - 1, 3) == 0.273
assert round(se * 100, 2) == 0.28 and round(1.96 * se * 100, 2) == 0.55 and round(t2 - e2) == 6_300

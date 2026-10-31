# Q2: bill-splitting feature, four-week read (illustrative numbers)
import math

eligible = 500_000          # active UPI users in the treatment group
saw_entry = 120_000         # saw the split entry point
started = 30_000            # started a split
settled = 21_000            # split where at least one friend paid back within 7 days
print(f"exposure {saw_entry/eligible:.0%}  start {started/saw_entry:.0%}  settle {settled/started:.0%}")
assert saw_entry / eligible == 0.24 and started / saw_entry == 0.25 and settled / started == 0.70

# north star: weekly users with a settled split, among eligible
week4_settlers = 12_000
print(f"north star (week 4 settled splitters / eligible): {week4_settlers/eligible:.1%}")
assert round(week4_settlers / eligible, 3) == 0.024

# input: repeat. week-1 settlers who settle another split in weeks 2-4
w1, w1_repeat = 6_000, 2_100
print(f"4-week repeat among week-1 settlers: {w1_repeat/w1:.0%}")
assert w1_repeat / w1 == 0.35

# guardrail: core UPI payment success, treatment vs holdout (same size)
n = 500_000
p_c, p_t = 0.9820, 0.9815
pool = (p_c + p_t) / 2
se = math.sqrt(pool * (1 - pool) * (2 / n))
z = (p_t - p_c) / se
print(f"payment success: holdout {p_c:.2%} treatment {p_t:.2%} diff {(p_t-p_c)*100:.2f}pp z={z:.2f}")
assert abs(z) < 1.96   # not a significant move

# guardrail: unwanted collect-request complaints per 100k requests
print(f"complaints per 100k requests: before 40 after 42 -> {42/40-1:.0%} relative")
assert round(42/40 - 1, 2) == 0.05

import math

# Illustrative numbers from the prompt (not vendor prices)
N = 100_000
share_small = 0.70
c_small, c_large = 0.002, 0.012
pass_small, pass_large_same = 0.90, 0.94

n_small = round(N * share_small)
n_large = N - n_small
cost_router = n_small * c_small + n_large * c_large
cost_all_large = N * c_large
saving = cost_all_large - cost_router
print(f"routed to small: {n_small}, to large: {n_large}")
print(f"router cost/day: {cost_router:.1f}; all-large cost/day: {cost_all_large:.1f}; saving: {saving:.1f} ({saving/cost_all_large:.1%})")
assert n_small == 70_000 and n_large == 30_000
assert round(cost_router, 6) == 500.0 and round(cost_all_large, 6) == 1200.0 and round(saving, 6) == 700.0

fail_small = n_small * (1 - pass_small)
fail_large_same = n_small * (1 - pass_large_same)
extra = fail_small - fail_large_same
print(f"failures on routed slice: small {fail_small:.0f} vs large {fail_large_same:.0f}; extra per day: {extra:.0f} ({extra/N:.1%} of all traffic)")
assert round(fail_small) == 7000 and round(fail_large_same) == 4200 and round(extra) == 2800

# What a failure must cost for the router to stop paying off
be = saving / extra
print(f"break-even cost per extra failure: {be:.2f} (saving {saving:.0f} / extra failures {extra:.0f})")
assert round(be, 2) == 0.25

# Precision of a labelled audit of the small model's routed traffic (Wilson 95%)
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
lo, hi = wilson(450, 500)
print(f"audit 450/500 passed -> Wilson 95% [{lo:.3f}, {hi:.3f}]")
assert 0.87 < lo < 0.88 and 0.92 < hi < 0.93   # +/- about 3 points, too wide to confirm a 4-point gap alone

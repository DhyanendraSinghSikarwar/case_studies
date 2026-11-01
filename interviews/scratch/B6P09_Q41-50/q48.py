# Q48: serial returners (prompt numbers, illustrative)
import math
cust, flagged_n, returns, flagged_ret = 2_000_000, 20_000, 400_000, 48_000
assert flagged_n / cust == 0.01 and flagged_ret / returns == 0.12
print("returns per flagged customer:", flagged_ret / flagged_n, " per other customer:", round((returns - flagged_ret) / (cust - flagged_n), 3))
assert flagged_ret / flagged_n == 2.4
print("ratio:", round((flagged_ret / flagged_n) / ((returns - flagged_ret) / (cust - flagged_n)), 1))

k, n = 150, 200
p = k / n
print("sample share abusing:", p, " legitimate:", 1 - p)
proj = p * flagged_n
print("projected abusers among 20,000:", proj, " projected legitimate heavy buyers:", flagged_n - proj)
assert proj == 15_000 and flagged_n - proj == 5_000

def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h
lo, hi = wilson(k, n)
print(f"95% Wilson interval for the share: [{lo:.3f}, {hi:.3f}] -> abusers [{lo*flagged_n:,.0f}, {hi*flagged_n:,.0f}], legitimate [{(1-hi)*flagged_n:,.0f}, {(1-lo)*flagged_n:,.0f}]")
assert 0.68 < lo < 0.70 and 0.80 < hi < 0.81
# only valid if the 200 were a random draw from the 20,000; a top-scored 200 would overstate
# action example (invented): friction (e.g. return-window check) for flagged; cost of wrongly hitting a legit heavy buyer
legit = flagged_n - proj
cost_wrong, saving_right = 40, 25      # invented per-customer figures
print("expected net per flagged customer (invented):", p * saving_right - (1 - p) * cost_wrong)
assert p * saving_right - (1 - p) * cost_wrong == 8.75
print("breakeven abusing share:", cost_wrong / (cost_wrong + saving_right))
assert round(cost_wrong / (cost_wrong + saving_right), 3) == 0.615

# Q8 flat aggregate accuracy hides a new-user drop (numbers from the prompt)
w_old, w_new = 0.80, 0.20
before = (0.90, 0.88)       # existing, new
after = (0.92, 0.80)
agg_b = w_old * before[0] + w_new * before[1]
agg_a = w_old * after[0] + w_new * after[1]
print(f"aggregate before {agg_b:.3f}, after {agg_a:.3f}")
assert round(agg_b, 3) == 0.896 and round(agg_a, 3) == 0.896

# Errors as a share of all traffic (percentage points of traffic)
err_old_b, err_old_a = w_old * (1 - before[0]), w_old * (1 - after[0])
err_new_b, err_new_a = w_new * (1 - before[1]), w_new * (1 - after[1])
print(f"existing-user errors {err_old_b*100:.1f} -> {err_old_a*100:.1f} pts of traffic; new-user errors {err_new_b*100:.1f} -> {err_new_a*100:.1f} pts")
assert round(err_old_b * 100, 1) == 8.0 and round(err_old_a * 100, 1) == 6.4
assert round(err_new_b * 100, 1) == 2.4 and round(err_new_a * 100, 1) == 4.0
assert round((err_old_a + err_new_a) * 100, 1) == round((err_old_b + err_new_b) * 100, 1) == 10.4

# Error rate of new users rose by two thirds in relative terms even though the aggregate error is unchanged
print(f"new-user error rate: {1-before[1]:.0%} -> {1-after[1]:.0%} (x{(1-after[1])/(1-before[1]):.2f})")
assert abs((1 - after[1]) / (1 - before[1]) - 1.667) < 0.001

# If the new-user share grows, the aggregate falls even with no further change
for share in (0.20, 0.30, 0.40):
    agg = (1 - share) * after[0] + share * after[1]
    print(f"new-user share {share:.0%}: aggregate {agg:.3f}")
assert round(0.7 * 0.92 + 0.3 * 0.80, 3) == 0.884

# Is the 8-point drop noise? Say 400,000 scored cases a month -> 80,000 new-user cases
n_new = 80_000
se = (0.80 * 0.20 / n_new) ** 0.5
print(f"standard error of new-user accuracy: {se*100:.2f} pts, so 88% to 80% is a {(0.88-0.80)/se:.0f}-sigma move")
assert (0.88 - 0.80) / se > 50

# Monitoring rule: alert when a segment's lower confidence bound falls below its baseline floor
def seg_alert(acc, n, floor, z=1.96):
    se = (acc * (1 - acc) / n) ** 0.5
    return acc + z * se < floor          # even the upper bound is under the floor
print("new-user alert fires:", seg_alert(0.80, n_new, 0.86))
print("aggregate alert fires:", seg_alert(agg_a, 400_000, 0.88))
assert seg_alert(0.80, n_new, 0.86) and not seg_alert(agg_a, 400_000, 0.88)

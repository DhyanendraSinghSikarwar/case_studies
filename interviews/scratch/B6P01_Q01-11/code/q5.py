# Q5: post-sale week, three baselines (illustrative orders per week, thousands)
pre_sale = [100, 101, 102]            # three normal weeks before the sale
sale_week = 150
post_weeks = [120, 108, 103]          # post-sale week 1, 2, 3
print(f"post-sale week vs sale week: {post_weeks[0]/sale_week-1:.0%}")
assert round(post_weeks[0] / sale_week - 1, 2) == -0.20

pre_avg = sum(pre_sale) / 3
print(f"pre-sale average {pre_avg:.1f}; post-sale week 1 vs pre-sale: {post_weeks[0]/pre_avg-1:+.1%}")
assert round(pre_avg, 1) == 101.0

# baseline 2: same event last year, same shape
ly_sale, ly_post1 = 100, 78
print(f"last year post-sale vs sale week: {ly_post1/ly_sale-1:.0%}")
assert round(ly_post1 / ly_sale - 1, 2) == -0.22

# baseline 3: trend plus pull-forward.
# extra sale-week orders over trend = 150 - 103 = 47. Assume 20% of that was pulled from the next 3 weeks.
trend = [103, 104, 105]
pulled = 0.20 * (sale_week - 103)
expected = [t - pulled / 3 for t in trend]
print(f"pull-forward estimate {pulled:.1f}k over 3 weeks; expected weeks {[round(e,1) for e in expected]}")
print(f"actual  {post_weeks}")
gap = [a - e for a, e in zip(post_weeks, expected)]
print(f"actual minus expected: {[round(g,1) for g in gap]}")
assert round(pulled, 1) == 9.4
assert all(g > 0 for g in gap)          # no shortfall versus expectation: a normal hangover
# a real decline would look like actual falling BELOW pre-sale level and staying there
print("weeks 2-3 settle back to pre-sale level (108, 103 vs 101): hangover, not decline")

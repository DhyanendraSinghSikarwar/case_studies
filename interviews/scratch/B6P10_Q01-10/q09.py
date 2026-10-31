import math
# Q9 moderation: illustrative numbers from the prompt
uploads, rate, audit_n = 2_000_000, 0.004, 50_000
review_cap, recall_goal = 12_000, 0.90
viol = uploads * rate
must_flag = viol * recall_goal
min_prec = must_flag / review_cap
print(f"violating/day {viol:,.0f}; must flag {must_flag:,.0f}; min precision of queue {min_prec:.0%}")
# the 0.4% is a sample estimate: 200 violations in 50,000 audited
k = round(audit_n * rate)
se = math.sqrt(rate * (1 - rate) / audit_n)
lo_r, hi_r = rate - 1.96 * se, rate + 1.96 * se
print(f"audit violations {k}; 95% interval {lo_r:.3%} to {hi_r:.3%}")
for lab, r in (("low", lo_r), ("base", rate), ("high", hi_r)):
    v = uploads * r
    print(f"{lab}: {v:,.0f} violations, flag {v*recall_goal:,.0f}, min precision {v*recall_goal/review_cap:.1%}")
# queue size when precision is lower: how many true violations reach reviewers
for p in (0.5, 0.6, 0.7):
    tp = review_cap * p
    print(f"precision {p:.0%}: {tp:,.0f} true found, recall {tp/viol:.1%}")
# alternative: auto-remove very confident cases to free reviewers (illustrative 3,000 auto at 99% precision)
auto, auto_p = 3_000, 0.99
tp_total = auto * auto_p + review_cap * 0.5
print(f"with 3,000 auto-actions at 99% and 12,000 reviewed at 50%: recall {tp_total/viol:.1%}")
assert viol == 8_000 and must_flag == 7_200 and min_prec == 0.60
assert k == 200 and round(lo_r, 5) == 0.00345 and round(hi_r, 5) == 0.00455
assert round(uploads * lo_r * 0.9 / review_cap, 3) == 0.518 and round(uploads * hi_r * 0.9 / review_cap, 3) == 0.683
assert round(review_cap * 0.5 / viol, 3) == 0.75 and round(review_cap * 0.6 / viol, 2) == 0.90
assert round(tp_total / viol, 3) == 1.1 * 0 + round((2970 + 6000) / 8000, 3)

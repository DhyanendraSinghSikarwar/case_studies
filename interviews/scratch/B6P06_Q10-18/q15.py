import math
vol, acc, cost = 500_000, 0.94, 20
wrong = round(vol * (1 - acc))
print("wrong", wrong, "cost", wrong * cost)
assert wrong == 30_000 and wrong * cost == 600_000
# how sure is 94%? if the pilot sampled 500 questions (invented), Wilson 95% interval
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
lo, hi = wilson(470, 500)
print("Wilson for 470/500: %.3f - %.3f" % (lo, hi))
print("monthly wrong at those bounds:", round(vol * (1 - hi)), "-", round(vol * (1 - lo)))
assert 0.91 < lo < 0.92 and 0.95 < hi < 0.96
# segments (invented): the average hides where the cost sits
seg = {  # name: (questions, error rate, cost per wrong answer)
    "exploratory": (350_000, 0.04, 5),
    "routine reporting": (100_000, 0.06, 20),
    "decision / finance / external": (50_000, 0.20, 41),
}
tw = tc = 0
for k, (q, e, c) in seg.items():
    w = round(q * e); tw += w; tc += w * c
    print(f"{k:32s} wrong {w:6d} cost {w*c:8d}")
print("total wrong", tw, "total cost", tc)
assert tw == 30_000 and tc == 600_000
# review the high-stakes tier only: 3 per review (invented), catches 80% of its errors (invented)
q, e, c = seg["decision / finance / external"]
review_cost = q * 3
saved = 0.8 * round(q * e) * c
net = saved - review_cost
print("review cost", review_cost, "saved", saved, "net", net, "| residual monthly cost", tc - saved + review_cost)
assert review_cost == 150_000 and saved == 328_000 and net == 178_000

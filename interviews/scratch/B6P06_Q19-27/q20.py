from itertools import combinations
weeks_each, overhead = 10, 0.20
cap6 = 6 * weeks_each * (1 - overhead)
cap4 = 4 * weeks_each * (1 - overhead)
backlog = 72
print(f"capacity 6 people {cap6:.0f}, 4 people {cap4:.0f}, backlog {backlog}")
print(f"coverage: 6 people {cap6/backlog:.1%}, 4 people {cap4/backlog:.1%}; unfunded weeks: {backlog-cap6:.0f} -> {backlog-cap4:.0f}")
assert cap6 == 48 and cap4 == 32 and abs(cap6/backlog - 2/3) < 1e-12 and abs(cap4/backlog - 4/9) < 1e-12
assert backlog - cap6 == 24 and backlog - cap4 == 40
# overhead lever: cutting meetings/support from 20% to 15% with 4 people
cap4_lean = 4 * weeks_each * 0.85
print(f"4 people at 15% overhead: {cap4_lean:.0f} weeks")
assert abs(cap4_lean - 34) < 1e-9
# illustrative backlog: (name, person-weeks, value score) ; weeks sum to 72
items = [("churn model refresh", 10, 90), ("ad-hoc asks (bundle)", 8, 25), ("pricing analysis", 6, 60),
         ("self-serve dashboard", 12, 55), ("fraud rules review", 9, 70), ("new forecasting model", 14, 50),
         ("experiment platform fixes", 7, 45), ("LLM pilot", 6, 20)]
assert sum(w for _, w, _ in items) == 72
best = (0, None)
for r in range(len(items) + 1):
    for c in combinations(items, r):
        w = sum(x[1] for x in c); v = sum(x[2] for x in c)
        if w <= cap4 and v > best[0]:
            best = (v, c)
v4, chosen = best
total_v = sum(v for _, _, v in items)
print(f"best set for 32 weeks: value {v4} of {total_v} ({v4/total_v:.0%}), weeks {sum(x[1] for x in chosen)}")
print("keep :", [n for n, _, _ in chosen])
print("defer:", [n for n, _, _ in items if n not in [c[0] for c in chosen]])
assert sum(x[1] for x in chosen) <= 32
# value per week is only a heuristic; show it
for n, w, v in sorted(items, key=lambda x: -x[2]/x[1]):
    print(f"  {n:28s} {w:3d} wk  value {v:3d}  value/wk {v/w:5.2f}")

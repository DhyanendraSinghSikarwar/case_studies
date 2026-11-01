from itertools import combinations
cost = {"A": 20, "B": 14, "C": 10, "D": 8, "E": 6}
ben = {"A": 40, "B": 30, "C": 16, "D": 14, "E": 12}
cap = 3 * 12
assert cap == 36 and sum(cost.values()) == 58 and sum(ben.values()) == 112
def best(capacity):
    res = []
    for r in range(1, 6):
        for s in combinations(cost, r):
            c = sum(cost[x] for x in s)
            if c <= capacity:
                res.append((sum(ben[x] for x in s), c, "".join(s)))
    return sorted(res, reverse=True)
top = best(cap)[:4]
print("capacity 36 top subsets (benefit, weeks, projects):", top)
assert top[0] == (70, 34, "AB") and top[1] == (68, 36, "ACE")
# buffer: plan to 80% of capacity (28.8 person-weeks)
buf = cap * 0.8
t2 = best(buf)[:3]
print("planned to", buf, "->", t2)
assert t2[0] == (56, 28, "BDE")
# benefit per person-week
for k in cost: print(k, round(ben[k] / cost[k], 2))
assert round(40 / 20, 2) == 2.0 and round(30 / 14, 2) == 2.14
# risk sensitivity: if A's benefit is really 40 * 0.5 (half the projection)
ben2 = dict(ben); ben2["A"] = 20
res = sorted(((sum(ben2[x] for x in s), sum(cost[x] for x in s), "".join(s))
              for r in range(1, 6) for s in combinations(cost, r) if sum(cost[x] for x in s) <= cap), reverse=True)[0]
print("if A delivers half:", res)
assert res == (60, 32, "BCD")
# feasibility: nobody can do more than 12 person-weeks on a calendar of 12 weeks
print("A needs at least", -(-20 // 12), "people; B needs at least", -(-14 // 12))
assert -(-20 // 12) == 2 and -(-14 // 12) == 2

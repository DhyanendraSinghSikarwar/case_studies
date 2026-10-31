from itertools import combinations
P = {"A": (280, 6), "B": (200, 2), "C": (150, 3), "D": (120, 5)}   # value (thousands), weeks
cap = 10
ratio = {k: v / w for k, (v, w) in P.items()}
rank = sorted(ratio, key=ratio.get, reverse=True)
print("value per week:", {k: round(ratio[k], 1) for k in rank}, "rank", rank)
assert rank == ["B", "C", "A", "D"] and round(ratio["A"], 1) == 46.7
# greedy by ratio
used = val = 0; picked = []
for k in rank:
    if used + P[k][1] <= cap:
        used += P[k][1]; val += P[k][0]; picked.append(k)
print("greedy by ratio:", picked, "weeks", used, "value", val)
assert (picked, used, val) == (["B", "C", "D"], 10, 470)
# exhaustive search
best = (0, ())
for r in range(1, 5):
    for c in combinations(P, r):
        w = sum(P[k][1] for k in c); v = sum(P[k][0] for k in c)
        if w <= cap and v > best[0]: best = (v, c)
        if w <= cap: print(" ", "+".join(c), "weeks", w, "value", v)
print("best:", best)
assert best == (480, ("A", "B")) and sum(P[k][1] for k in best[1]) == 8
print("spare weeks with best:", cap - 8, "-> C (3 weeks) does not fit; value lost to greedy:", 480 - 470)

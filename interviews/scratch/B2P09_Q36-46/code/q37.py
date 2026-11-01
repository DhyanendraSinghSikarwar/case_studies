# Elo (online, order-dependent) vs Bradley-Terry (batch MLE, order-free) on synthetic pairwise battles.
import math, random
def elo(battles, K=16, base=1000.0):
    r = {}
    for a, b, w in battles:                     # w = 1 if a wins, 0 if b wins
        ra, rb = r.setdefault(a, base), r.setdefault(b, base)
        ea = 1 / (1 + 10 ** ((rb - ra) / 400))
        r[a] = ra + K * (w - ea); r[b] = rb + K * ((1 - w) - (1 - ea))
    return r
def bt_fit(battles, iters=500):
    """MM algorithm (Zermelo/Hunter). strengths p_i; P(i beats j)=p_i/(p_i+p_j). Returns Elo-scale ratings, mean 1000."""
    models = sorted({m for a, b, _ in battles for m in (a, b)})
    wins = {m: 0 for m in models}; n = {}
    for a, b, w in battles:
        wins[a if w else b] += 1
        k = tuple(sorted((a, b))); n[k] = n.get(k, 0) + 1
    p = {m: 1.0 for m in models}
    for _ in range(iters):
        new = {}
        for i in models:
            den = sum(n[tuple(sorted((i, j)))] / (p[i] + p[j]) for j in models if j != i and tuple(sorted((i, j))) in n)
            new[i] = wins[i] / den
        g = math.exp(sum(math.log(v) for v in new.values()) / len(new))
        p = {m: v / g for m, v in new.items()}
    r = {m: 400 * math.log10(v) for m, v in p.items()}
    mu = sum(r.values()) / len(r)
    return {m: 1000 + r[m] - mu for m in models}, p, wins, n
# 1) two battles, hand-checkable: same data, two orders
print("two battles, K=32:")
for order in ([("A", "B", 1), ("B", "A", 1)], [("B", "A", 1), ("A", "B", 1)]):
    r = elo(order, K=32); print("  ", [(a, b, 'first wins') for a, b, _ in order], "->", {k: round(v, 2) for k, v in r.items()})
# 2) 600 synthetic battles, true strengths known (assumed inputs)
random.seed(11)
true = {"A": 1.8, "B": 1.2, "C": 1.0, "D": 0.5}
pairs = [(a, b) for a in true for b in true if a < b]
battles = []
for _ in range(600):
    a, b = random.choice(pairs)
    battles.append((a, b, int(random.random() < true[a] / (true[a] + true[b]))))
bt, p, wins, n = bt_fit(battles)
print("\nBT ratings (original order):", {k: round(v, 1) for k, v in bt.items()})
orders = {"original": battles[:], "reversed": battles[::-1],
          "A-wins-last": sorted(battles, key=lambda x: (x[2] == 1 and x[0] == 'A')),
          "A-wins-first": sorted(battles, key=lambda x: (x[2] == 0 or x[0] != 'A'))}
print("\norder           Elo(A) Elo(B) Elo(C) Elo(D)  BT(A)   BT(B)   BT(C)   BT(D)")
for name, o in orders.items():
    e = elo(o); b2 = bt_fit(o)[0]
    print(f"{name:14} " + " ".join(f"{e[m]:6.1f}" for m in "ABCD") + "  " + " ".join(f"{b2[m]:6.1f}" for m in "ABCD"))
# 3) check BT: gradient of log-likelihood is ~0 at the solution (MLE), and a closed form for 2 models
g = max(abs(wins[i] - sum(n[tuple(sorted((i, j)))] * p[i] / (p[i] + p[j]) for j in p if j != i)) for i in p)
print("\nmax |wins_i - expected wins_i| at BT solution:", f"{g:.2e}")
two = [("X", "Y", 1)] * 30 + [("X", "Y", 0)] * 10
r2 = bt_fit(two)[0]
print("two models, X wins 30 of 40: BT gap", round(r2["X"] - r2["Y"], 3), " closed form 400*log10(30/10) =", round(400 * math.log10(3), 3))

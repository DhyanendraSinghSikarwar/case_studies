import random
from itertools import product


def days_needed(weights, c):
    # greedy loading in order; None when a package is heavier than c
    if any(w > c for w in weights):
        return None
    days, load = 1, 0
    for w in weights:
        if load + w > c:
            days += 1
            load = 0
        load += w
    return days


def pred_exact(weights, d, c):
    return days_needed(weights, c) == d


def pred_atmost(weights, d, c):
    t = days_needed(weights, c)
    return t is not None and t <= d


def has_sub_sum(arr, L, target):
    return any(sum(arr[i:i + L]) >= target for i in range(len(arr) - L + 1))


def is_monotone(seq):
    # True...True/False...False in either direction: at most one flip
    return sum(1 for a, b in zip(seq, seq[1:]) if a != b) <= 1


w = [1, 2, 3]
a = [pred_exact(w, 2, c) for c in range(1, 8)]
print("(a) exactly 2 days, c=1..7:", a, " monotone?", is_monotone(a))
assert a == [False, False, True, True, True, False, False]
print("    days by capacity:", [days_needed(w, c) for c in range(1, 8)])
a2 = [pred_atmost(w, 2, c) for c in range(1, 8)]
print("(a) at most 2 days, c=1..7:", a2, " monotone?", is_monotone(a2))
assert a2 == [False, False, True, True, True, True, True]

arr = [5, -10, 5, 5]
b = [has_sub_sum(arr, L, 10) for L in range(1, 5)]
print("(b) arr=[5,-10,5,5], L=1..4:", b, " monotone?", is_monotone(b))
assert b == [False, True, False, False]

# at-most-d predicate is monotone in c: exhaustive over small package lists
checked = 0
for n in range(1, 6):
    for ws in product(range(1, 5), repeat=n):
        for d in range(1, n + 1):
            seq = [pred_atmost(list(ws), d, c) for c in range(1, sum(ws) + 2)]
            assert is_monotone(seq) and (not seq or seq[-1]), (ws, d)
            checked += 1
print("at-most-d monotone in capacity: checked", checked, "(weights, d) cases")

# how often is the exact-d predicate NOT monotone? (random seeded)
rng = random.Random(33)
nonmono = 0
for _ in range(500):
    ws = [rng.randint(1, 6) for _ in range(rng.randint(2, 6))]
    d = rng.randint(1, len(ws))
    seq = [pred_exact(ws, d, c) for c in range(1, sum(ws) + 2)]
    nonmono += not is_monotone(seq)
print("exact-d predicate non-monotone in", nonmono, "of 500 random cases")
assert nonmono > 0

# (b) non-negative lists: 'some window of length L has sum >= T' is monotone in L (exhaustive small)
cnt = 0
for n in range(1, 6):
    for xs in product(range(0, 4), repeat=n):
        for T in range(0, 12):
            seq = [has_sub_sum(list(xs), L, T) for L in range(1, n + 1)]
            # larger L can only add non-negative amounts to a best window, so once True stays True
            assert all(not (a and not b) for a, b in zip(seq, seq[1:])), (xs, T)
            cnt += 1
print("non-negative: once True stays True for larger L, checked", cnt, "cases")
# with negatives it fails
neg_fail = 0
for _ in range(500):
    xs = [rng.randint(-5, 5) for _ in range(rng.randint(2, 6))]
    T = rng.randint(1, 6)
    seq = [has_sub_sum(xs, L, T) for L in range(1, len(xs) + 1)]
    neg_fail += any(a and not b for a, b in zip(seq, seq[1:]))
print("with negatives, True then False happened in", neg_fail, "of 500 random cases")
assert neg_fail > 0
print("all checks passed")

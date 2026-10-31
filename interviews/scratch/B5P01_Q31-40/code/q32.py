import random
from collections import Counter


def brute(t):
    n = len(t)
    return sum(1 for i in range(n) for j in range(i + 1, n) if (t[i] + t[j]) % 60 == 0)


def pairs_div60(t):
    """One pass: for x, partners are earlier values with remainder (60 - x%60) % 60."""
    cnt = [0] * 60
    total = 0
    for x in t:
        r = x % 60
        total += cnt[(60 - r) % 60]   # r=0 -> looks up 0, r=30 -> looks up 30
        cnt[r] += 1
    return total


def pairs_div60_counts(t):
    """Same answer from final counts: r<30 pairs with 60-r, 0 and 30 pair with themselves."""
    c = Counter(x % 60 for x in t)
    total = c[0] * (c[0] - 1) // 2 + c[30] * (c[30] - 1) // 2
    total += sum(c[r] * c[60 - r] for r in range(1, 30))
    return total


ex1 = [30, 20, 150, 100, 40]
ex2 = [60, 60, 60]
print(ex1, "->", pairs_div60(ex1), "| counts form:", pairs_div60_counts(ex1))
print(ex2, "->", pairs_div60(ex2), "| counts form:", pairs_div60_counts(ex2))
assert pairs_div60(ex1) == 3 and pairs_div60(ex2) == 3

# Trap: forgetting the % 60 on the complement gives 60 - 0 = 60 (a slot that never fills)
def buggy(t):
    cnt = [0] * 61
    total = 0
    for x in t:
        r = x % 60
        total += cnt[60 - r]
        cnt[r] += 1
    return total
print("buggy (no outer %60) on [60,60,60]:", buggy(ex2), "(should be 3)")

# Edge cases
assert pairs_div60([]) == 0
assert pairs_div60([60]) == 0
assert pairs_div60([30, 30]) == 1
assert pairs_div60([30, 30, 30]) == 3
assert pairs_div60([1, 59]) == 1
assert pairs_div60([60, 120, 180, 240]) == 6
assert pairs_div60([1, 2, 3]) == 0
assert pairs_div60([500] * 4) == 0       # 500 % 60 == 20, 20+20 != 60

rng = random.Random(32)
for _ in range(1500):
    t = [rng.randint(1, 500) for _ in range(rng.randint(0, 25))]
    b = brute(t)
    assert pairs_div60(t) == b == pairs_div60_counts(t), t
print("cross-check passed: 1500 random lists (three implementations agree)")

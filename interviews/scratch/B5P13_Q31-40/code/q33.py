import itertools
import math
import random
from collections import Counter

random.seed(3301)


def run(stream, k, draws):
    """Algorithm R with fixed draws. Slots hold positions so we can count, values are read at the end."""
    n = len(stream)
    slots = list(range(k))                       # slot s holds the position of an item
    for i, d in zip(range(k + 1, n + 1), draws):  # i = 1-based index of the new item, d in 0..i-1
        if d < k:
            slots[d] = i - 1
    return slots


def solve(stream, k, draws):
    n = len(stream)
    reservoir = [stream[p] for p in run(stream, k, draws)]
    inclusion = [0] * n
    subsets = Counter()
    seqs = 0
    for ds in itertools.product(*[range(i) for i in range(k + 1, n + 1)]):   # ALL draw sequences
        slots = run(stream, k, ds)
        seqs += 1
        subsets[frozenset(slots)] += 1
        for p in slots:
            inclusion[p] += 1
    return [reservoir, inclusion, seqs, len(subsets), min(subsets.values()), max(subsets.values())]


def brute(stream, k, draws):
    n = len(stream)
    res = list(stream[:k])
    for idx, d in enumerate(draws):
        if d < k:
            res[d] = stream[k + idx]
    acc = []

    def rec(i, r):                               # recursion over the item number, tries every d in 0..i-1
        if i > n:
            acc.append(tuple(r))
            return
        for d in range(i):
            r2 = list(r)
            if d < k:
                r2[d] = i - 1
            rec(i + 1, r2)
    rec(k + 1, list(range(k)))
    cnt = [sum(p in r for r in acc) for p in range(n)]
    subs = Counter(frozenset(r) for r in acc)
    return [res, cnt, len(acc), len(subs), min(subs.values()), max(subs.values())]


# dry run on the first example: stream [10, 20, 30, 40], k = 2, draws [1, 3]
stream, k, draws = [10, 20, 30, 40], 2, [1, 3]
res = list(stream[:k])
print("start reservoir", res)
for i, d in zip(range(k + 1, len(stream) + 1), draws):
    item = stream[i - 1]
    if d < k:
        res[d] = item
    print(f"item {i} = {item}, draw d = {d} (0..{i - 1}): {'d < k, slot ' + str(d) + ' <- ' + str(item) if d < k else 'd >= k, ignore'} -> {res}")

for st, kk, dr, want in [([10, 20, 30, 40], 2, [1, 3], [[10, 30], [6, 6, 6, 6], 12, 6, 2, 2]),
                         ([7, 8], 2, [], [[7, 8], [1, 1], 1, 1, 1, 1]),
                         ([5, 6, 7], 1, [0, 2], [[6], [2, 2, 2], 6, 3, 2, 2])]:
    got = solve(st, kk, dr)
    assert got == want == brute(st, kk, dr), (st, kk, got)
    print(st, "k =", kk, "draws", dr, "->", got)

# exact uniformity for EVERY n <= 7 and k <= n: inclusion = k * seqs / n, all C(n,k) subsets, each seqs / C(n,k) times
print("\n n k  sequences  inclusion per item        subsets  per subset")
for n in range(1, 8):
    for kk in range(1, n + 1):
        r = solve(list(range(n)), kk, [0] * (n - kk))
        seqs = r[2]
        assert seqs == math.factorial(n) // math.factorial(kk)          # prod_{i=k+1..n} i
        assert set(r[1]) == {kk * seqs // n} and kk * seqs % n == 0      # every item kept k/n of the time
        assert r[3] == math.comb(n, kk) and r[4] == r[5] == seqs // math.comb(n, kk)
        if n in (5, 7) or (n == 4 and kk in (1, 2)):
            print(f"{n:>2} {kk} {seqs:>10}  {str(r[1][:1]) + ' x ' + str(n):<22}  {r[3]:>5}  {r[4]:>6}")
print("all n <= 7, all k <= n: each item is held in k/n of the sequences, all C(n,k) subsets occur equally often")

# seeded random cross-check against the recursive enumeration
for _ in range(300):
    n = random.randint(1, 6)
    kk = random.randint(1, n)
    st = [random.randint(0, 9) for _ in range(n)]
    dr = [random.randint(0, i - 1) for i in range(kk + 1, n + 1)]
    assert solve(st, kk, dr) == brute(st, kk, dr)
print("300 seeded random cases match the recursive enumeration")

# edge cases
assert solve([4], 1, [])[:3] == [[4], [1], 1]                 # n = 1
assert solve([1, 2, 3], 3, [])[0] == [1, 2, 3]                # k = n: no draws, nothing is replaced
assert solve([1, 2, 3], 1, [0, 0])[0] == [3]                  # d = 0 each time replaces slot 0
print("edge asserts ok")

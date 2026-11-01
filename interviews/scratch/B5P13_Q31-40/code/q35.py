import itertools
import math
import random

random.seed(3501)


def solve(nums, target, draws):
    """One scan, O(1) extra space for the pick itself. counts/sequences are the exact enumeration."""
    held, j = -1, 0
    for i, v in enumerate(nums):
        if v == target:                       # the j-th occurrence (0-based)
            if draws[j] == 0:                 # draws[j] in 0..j: replace with probability 1/(j+1)
                held = i
            j += 1
    c = j
    occ = [i for i, v in enumerate(nums) if v == target]
    counts = [0] * c
    seqs = 0
    for ds in itertools.product(*[range(jj + 1) for jj in range(c)]):   # ALL c! draw sequences
        last = -1
        for jj, d in enumerate(ds):
            if d == 0:
                last = jj
        counts[last] += 1                      # draws[0] is always 0, so last >= 0
        seqs += 1
    return [held, counts, seqs]


def brute(nums, target, draws):
    occ = [i for i, v in enumerate(nums) if v == target]
    c = len(occ)

    def rec(j, held, acc):                     # recursion over the occurrence number
        if j == c:
            acc[held] = acc.get(held, 0) + 1
            return
        for d in range(j + 1):
            rec(j + 1, occ[j] if d == 0 else held, acc)
    acc = {}
    rec(0, -1, acc)
    last = max(jj for jj, d in enumerate(draws) if d == 0)
    return [occ[last], [acc[o] for o in occ], sum(acc.values())]


# dry run on the first example: nums = [1, 2, 3, 3, 3], target 3, draws [0, 1, 0]
nums, target, draws = [1, 2, 3, 3, 3], 3, [0, 1, 0]
held, j = None, 0
for i, v in enumerate(nums):
    if v != target:
        print(f"index {i} value {v}: not the target, skip")
        continue
    d = draws[j]
    print(f"index {i} value {v}: occurrence {j}, draw {d} in 0..{j}, {'replace' if d == 0 else 'keep'}", end="")
    if d == 0:
        held = i
    print(f" -> held {held}")
    j += 1

for nm, tg, dr, want in [([1, 2, 3, 3, 3], 3, [0, 1, 0], [4, [2, 2, 2], 6]),
                         ([9, 9], 9, [0, 1], [0, [1, 1], 2]),
                         ([4, 5, 6], 5, [0], [1, [1], 1])]:
    got = solve(nm, tg, dr)
    assert got == want == brute(nm, tg, dr), (nm, got)
    print(nm, tg, dr, "->", got)

# exact uniformity for every number of occurrences c = 1..8: counts all (c-1)!, total c!
print("\n c   sequences  count per occurrence")
for c in range(1, 9):
    r = solve([7] * c, 7, [0] * c)
    assert r[2] == math.factorial(c) and set(r[1]) == {math.factorial(c - 1)} and len(r[1]) == c
    print(f"{c:>2} {r[2]:>11}  {r[1][0]:>6} x {c}")

# the probability argument as exact fractions: P(j-th held) = 1/(j+1) * prod_{i>j} (1 - 1/(i+1)) = 1/c
from fractions import Fraction
for c in range(1, 12):
    for jj in range(c):
        p = Fraction(1, jj + 1)
        for i in range(jj + 1, c):
            p *= 1 - Fraction(1, i + 1)
        assert p == Fraction(1, c)
print("telescoping product equals 1/c for c = 1..11, every j")

# seeded random cross-check against enumeration of all draw sequences
for _ in range(300):
    nm = [random.randint(1, 3) for _ in range(random.randint(1, 8))]
    tg = random.choice(nm)
    c = nm.count(tg)
    dr = [random.randint(0, jj) for jj in range(c)]
    assert solve(nm, tg, dr) == brute(nm, tg, dr)
    assert nm[solve(nm, tg, dr)[0]] == tg
print("300 seeded random cases match the recursive enumeration; the held index always holds the target")

# the dictionary alternative: O(n) build, O(1) per pick, O(n) memory
def build(nums):
    pos = {}
    for i, v in enumerate(nums):
        pos.setdefault(v, []).append(i)
    return pos
pos = build([1, 2, 3, 3, 3])
assert pos[3] == [2, 3, 4] and pos[3][2 % 3] in (2, 3, 4)
print("dict of positions:", pos)

# edge cases
assert solve([5], 5, [0]) == [0, [1], 1]                       # single occurrence: first draw is always 0
assert solve([3, 3, 3, 3], 3, [0, 0, 0, 0])[0] == 3            # all zeros: always replace, last wins
assert solve([3, 3, 3, 3], 3, [0, 1, 2, 3])[0] == 0            # only the forced first draw is 0: first stays
print("edge asserts ok")

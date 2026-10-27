import random
import time
import tracemalloc
from array import array
from collections import defaultdict
from itertools import groupby


# ---------- 1. duplicate detection ----------
def dup_brute(a):
    return any(a[i] == a[j] for i in range(len(a)) for j in range(i + 1, len(a)))

def dup_hash(a):                      # O(n) avg time, O(n) extra space, input untouched
    seen = set()
    for x in a:
        if x in seen:
            return True
        seen.add(x)
    return False

def dup_sort(a):                      # O(n log n) time, sorted() copy = O(n) space (list.sort() in place = O(1) extra but mutates)
    b = sorted(a)
    return any(b[i] == b[i + 1] for i in range(len(b) - 1))

def dup_partition(arr, parts):        # memory-limited: `parts` passes, each holds only ~n/parts values in a set
    for p in range(parts):
        seen = set()
        for x in arr:
            if x % parts == p:
                if x in seen:
                    return True
                seen.add(x)
    return False


# ---------- 2. pair-sum existence ----------
def pair_brute(a, t):
    return any(a[i] + a[j] == t for i in range(len(a)) for j in range(i + 1, len(a)))

def pair_hash(a, t):
    seen = set()
    for x in a:
        if t - x in seen:
            return True
        seen.add(x)
    return False

def pair_sort(a, t):                  # sort + two pointers; loses original indices unless you sort (value, index) pairs
    b = sorted(a)
    i, j = 0, len(b) - 1
    while i < j:
        s = b[i] + b[j]
        if s == t:
            return True
        if s < t:
            i += 1
        else:
            j -= 1
    return False


# ---------- 3. anagram grouping ----------
def group_hash(words):
    g = defaultdict(list)
    for w in words:
        g["".join(sorted(w))].append(w)
    return sorted(sorted(v) for v in g.values())

def group_sort(words):                # sort (key, word) pairs, then cut runs of equal keys
    keyed = sorted(("".join(sorted(w)), w) for w in words)
    return sorted(sorted(w for _, w in run) for _, run in groupby(keyed, key=lambda kw: kw[0]))

def group_brute(words):
    groups = []
    for w in words:
        for g in groups:
            if sorted(g[0]) == sorted(w):
                g.append(w)
                break
        else:
            groups.append([w])
    return sorted(sorted(g) for g in groups)


# ---------- edge cases ----------
assert dup_hash([]) is False and dup_sort([]) is False and dup_partition(array('q'), 4) is False
assert dup_hash([5]) is False and dup_sort([5]) is False
assert dup_hash([-3, 7, -3]) and dup_sort([-3, 7, -3]) and dup_partition(array('q', [-3, 7, -3]), 4)
assert pair_hash([], 0) is False and pair_sort([], 0) is False
assert pair_hash([5], 10) is False and pair_sort([5], 10) is False      # one element must not pair with itself
assert pair_hash([5, 5], 10) and pair_sort([5, 5], 10)
assert group_hash([]) == group_sort([]) == []
assert group_hash(['', '']) == group_sort(['', '']) == [['', '']]

# ---------- seeded cross-checks ----------
rng = random.Random(40)
for _ in range(1500):
    a = [rng.randint(-8, 8) for _ in range(rng.randint(0, 10))]
    t = rng.randint(-10, 10)
    d = dup_brute(a)
    assert dup_hash(a) == dup_sort(a) == dup_partition(array('q', a), 3) == d, a
    p = pair_brute(a, t)
    assert pair_hash(a, t) == pair_sort(a, t) == p, (a, t)
    w = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 4))) for _ in range(rng.randint(0, 8))]
    assert group_hash(w) == group_sort(w) == group_brute(w), w
print("cross-check passed: 1500 random cases across dup / pair-sum / anagram (hash, sort, brute agree)")

# ---------- sandbox-only memory and time at n = 10^6 (extrapolate by reasoning, not by trusting numbers) ----------
n = 1_000_000
arr = array('q', random.Random(1).sample(range(10**9), n))      # all distinct: no early exit, worst case for both
lst = list(arr)

def peak_extra(fn):
    tracemalloc.start()
    base = tracemalloc.get_traced_memory()[0]
    tracemalloc.reset_peak()
    fn()
    peak = tracemalloc.get_traced_memory()[1] - base
    tracemalloc.stop()
    return peak / 1e6

print(f"\nsandbox-only, n = {n:,} distinct ints, extra peak memory beyond the input (MB):")
print(f"  set-based         : {peak_extra(lambda: dup_hash(lst)):7.1f}")
print(f"  sorted() copy     : {peak_extra(lambda: dup_sort(lst)):7.1f}")
print(f"  8-pass partition  : {peak_extra(lambda: dup_partition(arr, 8)):7.1f}")
print(f"  (input as list of ints: {(len(lst) * 8 + sum(x.__sizeof__() for x in lst)) / 1e6:.0f} MB; as array('q'): {arr.itemsize * len(arr) / 1e6:.0f} MB)")

def best(fn, reps=3):
    out = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        out.append(time.perf_counter() - t0)
    return min(out)

print(f"\nsandbox-only timings, seconds, n = {n:,} (a single machine, not proof of big-O):")
print(f"  set-based dup check : {best(lambda: dup_hash(lst)):.3f}")
print(f"  sorted + scan       : {best(lambda: dup_sort(lst)):.3f}")
print(f"  8-pass partition    : {best(lambda: dup_partition(arr, 8), 1):.3f}")

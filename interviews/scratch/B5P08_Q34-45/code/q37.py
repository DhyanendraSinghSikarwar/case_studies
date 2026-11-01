import heapq
import itertools
import random

random.seed(37)

def top_names(records, k):
    return [name for name, score in heapq.nlargest(k, records, key=lambda r: r[1])]

def top_names_brute(records, k):
    """Explicit rule: higher score first, earlier position first on ties."""
    order = sorted(range(len(records)), key=lambda i: (-records[i][1], i))
    return [records[i][0] for i in order[:k]]

# ---- examples
for rec, k, want in [([['ann', 90], ['bob', 85], ['cy', 90], ['di', 70]], 3, ['ann', 'cy', 'bob']),
                     ([['a', 1], ['b', 1], ['c', 1]], 2, ['a', 'b']),
                     ([['a', 5]], 3, ['a']),
                     ([], 2, [])]:
    assert top_names(rec, k) == top_names_brute(rec, k) == want, (rec, k)
    print(rec, k, '->', top_names(rec, k))

# ---- exhaustive equivalence with sorted(..., reverse=True)[:k] on small lists with heavy ties
cases = 0
for n in range(0, 6):
    for scores in itertools.product(range(3), repeat=n):
        rec = [[chr(97 + i), s] for i, s in enumerate(scores)]
        for k in range(1, n + 3):
            a = heapq.nlargest(k, rec, key=lambda r: r[1])
            b = sorted(rec, key=lambda r: r[1], reverse=True)[:k]
            assert a == b
            assert top_names(rec, k) == top_names_brute(rec, k)
            cases += 1
print('nlargest == sorted(reverse=True)[:k] on', cases, 'tie-heavy (list, k) cases')

# ---- where the tie rule comes from: reverse=True does NOT reverse equal elements
print(sorted([['a', 1], ['b', 1], ['c', 1]], key=lambda r: r[1], reverse=True))
print('reversed(sorted(...)) would give', list(reversed(sorted([['a', 1], ['b', 1], ['c', 1]], key=lambda r: r[1]))))

# ---- the same job with a hand-written heap needs explicit tie info, or ties compare names (or crash)
def top_names_manual(records, k):
    h = []                                    # min-heap of (score, -position, name): smallest = worst kept
    for i, (name, score) in enumerate(records):
        item = (score, -i, name)              # -i: earlier position counts as larger on a tie
        if len(h) < k:
            heapq.heappush(h, item)
        elif item > h[0]:
            heapq.heapreplace(h, item)
    return [name for score, negpos, name in sorted(h, reverse=True)]
for _ in range(500):
    rec = [[str(i), random.randint(0, 3)] for i in range(random.randint(0, 9))]
    k = random.randint(1, 6)
    assert top_names_manual(rec, k) == top_names(rec, k) == top_names_brute(rec, k)
print('manual size-k heap with (score, -position, name) agrees on 500 random lists')
try:
    h = [(1, {'x': 1})]; heapq.heappush(h, (1, {'x': 2}))
except TypeError as e:
    print('payload without a tie-breaker -> TypeError:', e)

# ---- edge asserts
assert top_names([['a', 5]], 3) == ['a']
assert top_names([], 2) == []
assert top_names([['a', -1], ['b', -1]], 1) == ['a']
assert top_names([['a', 1], ['b', 2]], 1) == ['b'] == [max([['a', 1], ['b', 2]], key=lambda r: r[1])[0]]
big = [[str(i), random.randint(0, 50)] for i in range(10 ** 4)]
assert top_names(big, 10 ** 4) == [r[0] for r in sorted(big, key=lambda r: r[1], reverse=True)]
assert top_names(big, 5) == top_names_brute(big, 5)
print('size 10^4 checks ok; k == n result equals a stable descending sort')

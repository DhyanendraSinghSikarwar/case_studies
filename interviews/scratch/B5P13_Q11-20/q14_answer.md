### Q14 ⭐⭐⭐ 🟡 Python sort stability, key= and reverse=. `records` is a list of 1 to 1000 items [name, dept, score] (name and dept lowercase strings, score an integer with |score| <= 1000; names may repeat). Return four lists of NAMES, each in the order of the records after the sort described: A = one `sorted` call with `key=lambda r: (r[1], -r[2])` (department ascending, score descending); B = two stable passes, first `sort(key=score, reverse=True)` then `sort(key=dept)`; C = `sorted(records, key=dept, reverse=True)`; D = `sorted(records, key=dept)[::-1]`. Return `[A, B, C, D]`. Explain: Python's sort is stable, so records with equal keys keep their input order; that is why two passes (least significant key first) equal the single tuple key and why this is the way to sort by a string descending (strings cannot be negated); and that `reverse=True` preserves the original order of equal elements (it behaves as if the comparisons were reversed, not as if the result were reversed), so C and D differ whenever two records share a department. Mention `functools.cmp_to_key` as the general fallback. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an index-aware manual comparison (original position as the final tie-break) on small inputs. Example: records=[['ann', 'hr', 5], ['bob', 'it', 7], ['cat', 'hr', 5], ['dan', 'it', 9], ['eve', 'hr', 8]] -> [['eve', 'ann', 'cat', 'dan', 'bob'], ['eve', 'ann', 'cat', 'dan', 'bob'], ['bob', 'dan', 'ann', 'cat', 'eve'], ['dan', 'bob', 'eve', 'cat', 'ann']]; records=[['x', 'a', 1]] -> [['x'], ['x'], ['x'], ['x']]; records=[['p', 'b', 2], ['q', 'a', 2], ['r', 'b', 2], ['s', 'a', 3]] -> [['s', 'q', 'p', 'r'], ['s', 'q', 'p', 'r'], ['p', 'r', 'q', 's'], ['r', 'p', 's', 'q']].
**Asked at:** Python Sorting HOWTO (search-result snippets only; the docs.python.org fetch failed with ENOTFOUND, so behaviour was verified by running Python 3.13)

**Pattern:** Python sort stability, `key=`, `reverse=`, and multi-key sorting by passes.

**Say this first (1 line):** "Python's sort is stable, so equal keys keep input order. That makes two passes, least significant key first, equal to one tuple key. `reverse=True` keeps equal items in their original order, so it is not the same as reversing the sorted list."

**Brute force:** Write an explicit comparison that finishes with the original index as a tie-break and sort the indices with `cmp_to_key`. It does not depend on stability at all, and I use it as the reference. Cost: O(n log n) comparisons, each a Python call.

**Optimal:**
- A: `sorted(records, key=lambda r: (r[1], -r[2]))`. One pass, tuple key: dept ascending, score descending. Negating works for numbers only.
- B: sort by score with `reverse=True` first, then by dept. The second pass is stable, so inside each dept the earlier score order survives. Result equals A.
- Strings cannot be negated (`-'hr'` raises TypeError, shown below). For dept DESCENDING with score ascending use two passes: score first, then dept with `reverse=True`. General fallback: `functools.cmp_to_key` with a comparator.
- C: `sorted(records, key=dept, reverse=True)`. Departments descending, and records with the same dept stay in input order, because `reverse=True` behaves as if the comparisons were reversed, not as if the result list were flipped.
- D: `sorted(records, key=dept)[::-1]`. Flips everything, so equal-dept records come out in reverse input order. C and D differ whenever two records share a department (331 of my 400 random cases).
- Pass order matters: least significant key first. Sorting by dept first and score last gives a different list (in the output).

**Complexity:** Each sort is O(n log n) time and O(n) extra space (Timsort). Two passes cost twice that, same big-O. Key functions are called once per record, not per comparison.

**Dry run:** example 1, records ann(hr,5), bob(it,7), cat(hr,5), dan(it,9), eve(hr,8).
- A: keys ann (hr,-5), bob (it,-7), cat (hr,-5), dan (it,-9), eve (hr,-8). hr: eve, ann, cat (ann and cat tie, ann is first in input); it: dan, bob. A = eve, ann, cat, dan, bob.
- B: pass 1 (score desc): dan 9, eve 8, bob 7, ann 5, cat 5. Pass 2 (dept): hr: eve, ann, cat; it: dan, bob. Same as A.
- C: dept desc, input order inside: it: bob, dan; hr: ann, cat, eve.
- D: dept asc gives ann, cat, eve, bob, dan; flipped: dan, bob, eve, cat, ann.

**Code:**
```python
import functools
import random

random.seed(1314)

def four_sorts(records):
    name, dept, score = (lambda r: r[0]), (lambda r: r[1]), (lambda r: r[2])
    A = [r[0] for r in sorted(records, key=lambda r: (r[1], -r[2]))]
    t = list(records)
    t.sort(key=score, reverse=True)        # least significant key first
    t.sort(key=dept)                       # then the most significant key; stability keeps the score order inside a dept
    B = [r[0] for r in t]
    C = [r[0] for r in sorted(records, key=dept, reverse=True)]
    D = [r[0] for r in sorted(records, key=dept)[::-1]]
    return [A, B, C, D]

def brute(records):
    """Index-aware comparison: original position is the final tie-break, so no stability is assumed."""
    idx = list(range(len(records)))
    def cmp_a(i, j):                                   # dept asc, score desc, then position asc
        a, b = records[i], records[j]
        return (a[1] > b[1]) - (a[1] < b[1]) or (b[2] > a[2]) - (b[2] < a[2]) or (i > j) - (i < j)
    def cmp_c(i, j):                                   # dept DESC, position ASC (equal depts keep input order)
        a, b = records[i], records[j]
        return (b[1] > a[1]) - (b[1] < a[1]) or (i > j) - (i < j)
    def cmp_d(i, j):                                   # dept DESC, position DESC (the reversed result)
        a, b = records[i], records[j]
        return (b[1] > a[1]) - (b[1] < a[1]) or (j > i) - (j < i)
    pick = lambda c: [records[i][0] for i in sorted(idx, key=functools.cmp_to_key(c))]
    A = pick(cmp_a)
    return [A, A, pick(cmp_c), pick(cmp_d)]

examples = [
    ([['ann', 'hr', 5], ['bob', 'it', 7], ['cat', 'hr', 5], ['dan', 'it', 9], ['eve', 'hr', 8]],
     [['eve', 'ann', 'cat', 'dan', 'bob'], ['eve', 'ann', 'cat', 'dan', 'bob'],
      ['bob', 'dan', 'ann', 'cat', 'eve'], ['dan', 'bob', 'eve', 'cat', 'ann']]),
    ([['x', 'a', 1]], [['x'], ['x'], ['x'], ['x']]),
    ([['p', 'b', 2], ['q', 'a', 2], ['r', 'b', 2], ['s', 'a', 3]],
     [['s', 'q', 'p', 'r'], ['s', 'q', 'p', 'r'], ['p', 'r', 'q', 's'], ['r', 'p', 's', 'q']]),
]
for rec, exp in examples:
    got = four_sorts(rec)
    print(got)
    assert got == exp and brute(rec) == exp

# C vs D: reverse=True keeps equal records in input order, [::-1] reverses them
two = [['a', 'x', 0], ['b', 'x', 0]]
C, D = four_sorts(two)[2:]
print('two records, same dept: C =', C, ' D =', D)
assert C == ['a', 'b'] and D == ['b', 'a']

# strings cannot be negated: -r[1] raises, so the two-pass trick is the way to get dept DESC + score ASC
try:
    sorted(examples[0][0], key=lambda r: (-r[1], r[2]))
except TypeError as e:
    print('negating a str:', type(e).__name__)
t = list(examples[0][0]); t.sort(key=lambda r: r[2]); t.sort(key=lambda r: r[1], reverse=True)
print('dept desc then score asc via two passes:', [r[0] for r in t])
# the same with cmp_to_key
def cmp(a, b):
    return (b[1] > a[1]) - (b[1] < a[1]) or (a[2] > b[2]) - (a[2] < b[2])
assert [r[0] for r in sorted(examples[0][0], key=functools.cmp_to_key(cmp))] == [r[0] for r in t]

# the pass ORDER matters: dept first then score gives a different answer
wrong = list(examples[0][0]); wrong.sort(key=lambda r: r[1]); wrong.sort(key=lambda r: r[2], reverse=True)
print('wrong pass order:', [r[0] for r in wrong], '(A is', examples[0][1][0], ')')
assert [r[0] for r in wrong] != examples[0][1][0]

# key= is called once per record, not once per comparison
calls = [0]
def counting_key(r):
    calls[0] += 1
    return r[1]
sorted(examples[0][0], key=counting_key)
print('key calls for 5 records:', calls[0])
assert calls[0] == 5

# seeded random cross-check: A == B, all four equal the index-aware comparison
tie_seen = 0
for _ in range(400):
    n = random.randint(1, 12)
    rec = [[random.choice('abcde'), random.choice(['hr', 'it', 'ops']), random.randint(-3, 3)] for _ in range(n)]
    r = four_sorts(rec)
    assert r == brute(rec) and r[0] == r[1]
    if r[2] != r[3]:
        tie_seen += 1
print('random cross-check ok: 400 cases; C != D in', tie_seen, 'of them')

# edge asserts
assert four_sorts([['x', 'a', 1]]) == [['x']] * 4
assert four_sorts([['a', 'z', 1], ['b', 'z', 1]])[0] == ['a', 'b']   # all keys equal: input order survives in A
print('edge asserts ok')
```

**Output (my run):**
```
[['eve', 'ann', 'cat', 'dan', 'bob'], ['eve', 'ann', 'cat', 'dan', 'bob'], ['bob', 'dan', 'ann', 'cat', 'eve'], ['dan', 'bob', 'eve', 'cat', 'ann']]
[['x'], ['x'], ['x'], ['x']]
[['s', 'q', 'p', 'r'], ['s', 'q', 'p', 'r'], ['p', 'r', 'q', 's'], ['r', 'p', 's', 'q']]
two records, same dept: C = ['a', 'b']  D = ['b', 'a']
negating a str: TypeError
dept desc then score asc via two passes: ['bob', 'dan', 'ann', 'cat', 'eve']
wrong pass order: ['dan', 'eve', 'bob', 'ann', 'cat'] (A is ['eve', 'ann', 'cat', 'dan', 'bob'] )
key calls for 5 records: 5
random cross-check ok: 400 cases; C != D in 331 of them
edge asserts ok
```

**Edge cases:**
- Single record: all four lists equal.
- All keys equal: A keeps input order; D reverses it.
- Duplicate names are fine, since only the sort keys decide order.
- Negative scores: `-r[2]` is fine for ints (not for strings, or `bool`/`None` mixes).

**Follow-ups:**
- Why is the key function better than `cmp`? Called once per item, and Python 3 dropped `cmp=`. `cmp_to_key` wraps an old comparison when no key exists.
- Does `list.sort` guarantee stability? Yes, it is documented. The HOWTO page itself could not be fetched, so I verified the behaviour by running 3.13 (the documentation claim is editor knowledge).
- Sort descending but keep ties stable? `sort(key=..., reverse=True)` does that. Do not flip with `[::-1]`.

**Common mistakes:**
- Doing the passes in the wrong order (most significant key first).
- Using `[::-1]` and expecting stability for equal items.
- Trying `-r[1]` on a string key.
- Assuming a stable sort needs `(key, index)` pairs. It does not in Python, and this answer's reference uses them only to avoid assuming it.

### Q13 ⭐⭐⭐ 🟡 Random pick with weights, using prefix sums and bisect. `w` is a list of 1 to 10^4 positive integers with sum(w) <= 10^6, and `rs` is a list of integers with 0 <= r < sum(w). The generator behind the picker produces an integer r uniformly from 0 to sum(w) - 1; the picker must return the index i whose block of numbers contains r, where index i owns the w[i] consecutive values after those owned by the earlier indices. Return `[picks, counts]`: `picks[t]` is the index for `rs[t]`, and `counts[i]` is the number of values r in 0..sum(w)-1 that your rule maps to index i (so a correct rule gives `counts == w`, which is what makes the pick probability w[i] / sum(w) exactly). Build the inclusive prefix sums once and answer each pick with a binary search in O(log n). State exactly which bisect function applies when r is in 0..total-1 (the first index whose prefix sum is strictly greater than r) and why the other one (`bisect_left`) assigns the boundary values to the wrong index, and what changes if r is drawn from 1..total instead. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a linear scan that subtracts weights one by one on small inputs. Example: w=[1, 3], rs=[0, 1, 2, 3] -> [[0, 1, 1, 1], [1, 3]]; w=[5], rs=[0, 4] -> [[0, 0], [5]]; w=[2, 1, 3], rs=[0, 1, 2, 3, 5] -> [[0, 0, 1, 2, 2], [2, 1, 3]].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Prefix sums plus binary search. Map a uniform integer to a weighted index (inverse CDF on integers).

**Say this first (1 line):** "Build inclusive prefix sums once. Draw r uniformly in 0..total-1 and return `bisect_right(prefix, r)`: the first index whose prefix sum is strictly greater than r. Index i then owns exactly w[i] values of r."

**Brute force:** For every pick, walk the weights and subtract: `for i, x in enumerate(w): if r < x: return i; r -= x`. O(n) per pick. Correct and the reference here.

**Optimal:**
- Block i covers the values from prefix[i-1] up to prefix[i]-1 (prefix[-1] taken as 0), which is w[i] numbers. Example w = [2,1,3]: prefix [2,3,6], blocks {0,1}, {2}, {3,4,5}.
- r lands in block i when prefix[i-1] <= r < prefix[i]. The first prefix strictly greater than r is prefix[i]. That is `bisect_right(prefix, r)`.
- Why not `bisect_left`: it returns the first prefix >= r. When r equals a prefix value (r = 2 or 3 above) it returns the previous index, so each boundary value is given to the wrong block. For w = [2,1,3] it counts [3,1,2] instead of [2,1,3].
- If r is drawn from 1..total instead, the blocks are (prefix[i-1], prefix[i]] and `bisect_left` is the right call. Match the function to the range.
- Correctness is shown by counts: for all r in 0..total-1, count how many map to each index; the result equals w, so P(i) = w[i]/total exactly.

**Complexity:** Build O(n). Each pick O(log n) by binary search. Space O(n) for the prefix list. (The counts loop in my code is a checker, O(total log n), not part of the picker.)

**Dry run:** w = [1,3], prefix [1,4], total 4. r=0: first prefix > 0 is 1, index 0. r=1: 1 is not > 1, next prefix 4 > 1, index 1. r=2 and r=3: index 1. Picks [0,1,1,1], counts [1,3] = w.

**Code:**
```python
import bisect
import itertools
import random

random.seed(1313)

def weighted_pick(w, rs):
    """Inclusive prefix sums once, then bisect_right per pick: first index whose prefix sum is > r."""
    pre = list(itertools.accumulate(w))
    total = pre[-1]
    picks = [bisect.bisect_right(pre, r) for r in rs]
    # counts[i] = how many r in 0..total-1 land on i (loop over r only for the check; real pick is O(log n))
    counts = [0] * len(w)
    for r in range(total):
        counts[bisect.bisect_right(pre, r)] += 1
    return [picks, counts]

def brute(w, rs):
    """Linear scan: subtract weights one by one until r falls inside a block."""
    def pick(r):
        for i, x in enumerate(w):
            if r < x:
                return i
            r -= x
    counts = [0] * len(w)
    for r in range(sum(w)):
        counts[pick(r)] += 1
    return [[pick(r) for r in rs], counts]

examples = [
    ([1, 3], [0, 1, 2, 3], [[0, 1, 1, 1], [1, 3]]),
    ([5], [0, 4], [[0, 0], [5]]),
    ([2, 1, 3], [0, 1, 2, 3, 5], [[0, 0, 1, 2, 2], [2, 1, 3]]),
]
for w, rs, exp in examples:
    got = weighted_pick(w, rs)
    print(w, rs, '->', got)
    assert got == exp and brute(w, rs) == exp

# why bisect_left is wrong for r in 0..total-1: boundary values go to the previous index
w = [2, 1, 3]
pre = list(itertools.accumulate(w))
left = [0] * 3
for r in range(sum(w)):
    left[bisect.bisect_left(pre, r)] += 1
print('prefix', pre, 'bisect_left counts', left, '(want', w, ')')
assert left != w and left == [3, 1, 2]

# if r is drawn from 1..total instead, bisect_left is the right one
alt = [0] * 3
for r in range(1, sum(w) + 1):
    alt[bisect.bisect_left(pre, r)] += 1
assert alt == w
print('r in 1..total with bisect_left gives', alt)

# seeded random cross-check against the linear scan
for _ in range(300):
    w = [random.randint(1, 6) for _ in range(random.randint(1, 6))]
    rs = [random.randrange(sum(w)) for _ in range(random.randint(0, 10))]
    assert weighted_pick(w, rs) == brute(w, rs) and weighted_pick(w, rs)[1] == w
print('random cross-check ok: 300 cases (counts == w every time)')

# maximum size: n = 10^4, sum <= 10^6; one prefix build, picks cost O(log n) each
w = [random.randint(1, 100) for _ in range(10 ** 4)]
assert sum(w) <= 10 ** 6
pre = list(itertools.accumulate(w))
assert bisect.bisect_right(pre, 0) == 0 and bisect.bisect_right(pre, sum(w) - 1) == len(w) - 1
print('max size ok: n =', len(w), 'total =', sum(w))

# edge asserts
assert weighted_pick([1], [0]) == [[0], [1]]
assert weighted_pick([1, 1, 1], [0, 1, 2])[0] == [0, 1, 2]
assert weighted_pick([4, 1], [3, 4])[0] == [0, 1]       # r = 3 is the last value of block 0, r = 4 the first of block 1
print('edge asserts ok')
```

**Output (my run):**
```
[1, 3] [0, 1, 2, 3] -> [[0, 1, 1, 1], [1, 3]]
[5] [0, 4] -> [[0, 0], [5]]
[2, 1, 3] [0, 1, 2, 3, 5] -> [[0, 0, 1, 2, 2], [2, 1, 3]]
prefix [2, 3, 6] bisect_left counts [3, 1, 2] (want [2, 1, 3] )
r in 1..total with bisect_left gives [2, 1, 3]
random cross-check ok: 300 cases (counts == w every time)
max size ok: n = 10000 total = 510843
edge asserts ok
```

**Edge cases:**
- Single weight: always index 0.
- r = 0 goes to index 0; r = total-1 goes to the last index (checked at the max size).
- Weights all equal: the picker is uniform.
- Zero weights are excluded by the prompt (positive integers).

**Follow-ups:**
- Update a weight between picks? The prefix list goes stale; a Fenwick tree (Part 14, named only) gives O(log n) update and pick.
- Faster than O(log n) per pick? The alias method gives O(1) per pick after O(n) setup; mention only.
- Float weights? Use `random.random() * total` with `bisect_right`, accept tiny rounding at boundaries, or `random.choices(w_cumulative)`.

**Common mistakes:**
- `bisect_left` with r in 0..total-1 (boundary values go to the previous index, shown above).
- Drawing r in 1..total with `bisect_right`: r = total would return n, out of range.
- Recomputing prefix sums on every pick, which makes it O(n) again.

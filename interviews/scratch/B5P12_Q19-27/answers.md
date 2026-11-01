### Q19 ⭐⭐ 🟡 Permutations with duplicates. `nums` has 0 <= len <= 8 integers and may repeat values. Return every DISTINCT arrangement once, as lists, with the outer list sorted ascending with Python's list comparison; `nums = []` returns `[[]]`. State the number of results as n! divided by the product of the factorials of the multiplicities. Sort first, keep a `used` array and skip a value when it equals its left neighbour and that neighbour is NOT used (`not used[i-1]`); explain why that rule keeps equal values in their original relative order, and why testing `used[i-1]` instead gives the same count but is a different (wasteful) pruning. The distinct-values version is Q6. Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the set of tuples from itertools.permutations on small inputs. Example: nums=[2, 1, 2] -> [[1, 2, 2], [2, 1, 2], [2, 2, 1]]; nums=[5] -> [[5]]; nums=[] -> [[]]; nums=[3, 3, 1, 1] -> [[1, 1, 3, 3], [1, 3, 1, 3], [1, 3, 3, 1], [3, 1, 1, 3], [3, 1, 3, 1], [3, 3, 1, 1]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking over positions with a `used` array, plus a sort-then-skip rule to stop equal values from producing the same arrangement twice. Same skeleton as Q6 (distinct values); only the skip line is new.

**Say this first (1 line):** "Sort, then at each position try each unused value, but skip a value if its equal left neighbour is not used: that forces equal values to be placed in their original left-to-right order, so each distinct arrangement appears exactly once."

**Brute force:** Generate all `n!` permutations with `itertools.permutations`, drop repeats with a set, sort. Time O(n * n!) even when there are few distinct results (for `[1]*8` it builds 40320 tuples to return one). Used as the oracle.

**Optimal:**
- Sort `nums`. Keep `used[i]` and a `cur` list. At each level loop over indices `i` in order.
- Skip rule: `if i and a[i] == a[i-1] and not used[i-1]: continue`.
- Why it works: call equal values twins, tagged in sorted order (1a, 1b). The rule lets 1b be placed only when 1a is already placed. So in every leaf 1a sits to the left of 1b, 1b left of 1c, and so on. Each distinct arrangement corresponds to exactly one tagged arrangement with the twins in that order, so it is produced once. Tested in the code by tagging the twins.
- Count of results: `n! / (m1! * m2! * ...)` where `m` are the multiplicities (a multinomial). `[3,3,1,1]` gives `4!/(2!*2!) = 6`.
- The other rule, `used[i-1]` (skip when the twin IS used), is also correct: it forces the reverse order (1b before 1a). The count is the same. But it only notices the clash after the twin has already been placed, so it walks into whole sub-trees and cuts them late. On `[1,1,2,2]` it makes 33 calls against 19. Correct, but wasteful.

**Complexity:** Output size alone is `n!/prod(m!)` lists of length `n`, so time is O(n * n!/prod(m!)) for the copies; the work inside the tree is within a factor of `n` of that because with the tight rule every call leads to at least one result (no dead branches). Extra space O(n) for `cur`, `used`, and the recursion (depth `n <= 8`, far below CPython's limit of 1000). The sorted-input trick makes the outer list come out in ascending list order without a final sort.

**Dry run:** `nums = [2, 1, 2]`, sorted `[1, 2, 2]` at indices 0, 1, 2. The code prints this tree (indent is depth).
- Level 1: pick index 0 (value 1) -> `[1]`; pick index 1 (value 2) -> `[2]`; index 2 is skipped: its twin at index 1 is not used.
- Under `[1]`: pick index 1 -> `[1,2]`, then index 2 -> leaf `[1,2,2]`. Index 2 at that level is skipped (twin 1 not used).
- Under `[2]` (index 1): pick index 0 -> `[2,1]` -> pick index 2 -> leaf `[2,1,2]`; pick index 2 -> `[2,2]` -> pick index 0 -> leaf `[2,2,1]`. Here index 2 is allowed because its twin (index 1) IS used.
- Three leaves, in ascending order: `[1,2,2]`, `[2,1,2]`, `[2,2,1]`. Multinomial `3!/2! = 3`.
- Node counts (calls): plain `used`-array search 16 for 6 leaves (3 distinct after dedupe); tight rule 9; the other rule 12.

**Code:**
```python
import itertools, random, math, collections

random.seed(19)

def perms_dup(nums, rule='left_unused'):
    """Distinct permutations. rule 'left_unused': skip a[i] if a[i]==a[i-1] and NOT used[i-1] (correct, tight).
    rule 'left_used': skip if a[i]==a[i-1] and used[i-1] (also correct, but prunes late). Returns (result, calls)."""
    a = sorted(nums); n = len(a); used = [False] * n; cur = []; out = []; calls = 0
    def go():
        nonlocal calls
        calls += 1
        if len(cur) == n:
            out.append(cur[:]); return
        for i in range(n):
            if used[i]: continue
            if i and a[i] == a[i - 1]:
                if rule == 'left_unused' and not used[i - 1]: continue
                if rule == 'left_used' and used[i - 1]: continue
            used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
    go()
    return out, calls

def no_skip(nums):
    """Plain permutations with a used array and no duplicate rule: n! leaves, many repeated. Returns (list, calls)."""
    a = sorted(nums); n = len(a); used = [False] * n; cur = []; out = []; calls = 0
    def go():
        nonlocal calls
        calls += 1
        if len(cur) == n: out.append(cur[:]); return
        for i in range(n):
            if not used[i]:
                used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
    go(); return out, calls

def permutations_dup(nums):
    return perms_dup(nums)[0]          # already in ascending order because the input is sorted and we try indices in order

def brute(nums):
    return sorted(map(list, set(itertools.permutations(nums))))

def multinomial(nums):
    c = collections.Counter(nums); r = math.factorial(len(nums))
    for v in c.values(): r //= math.factorial(v)
    return r

# examples
for nums, exp in [([2, 1, 2], [[1, 2, 2], [2, 1, 2], [2, 2, 1]]), ([5], [[5]]), ([], [[]]),
                  ([3, 3, 1, 1], [[1, 1, 3, 3], [1, 3, 1, 3], [1, 3, 3, 1], [3, 1, 1, 3], [3, 1, 3, 1], [3, 3, 1, 1]])]:
    got = permutations_dup(nums)
    assert got == exp == brute(nums), nums
    print('example', nums, '->', got)

# decision tree of [1, 1, 2] under the correct rule (indent = depth; X = skipped by the rule)
def show_tree(nums):
    a = sorted(nums); n = len(a); used = [False] * n; cur = []
    def go(d):
        if len(cur) == n:
            print('  ' * d + '-> leaf', cur); return
        for i in range(n):
            if used[i]: continue
            if i and a[i] == a[i - 1] and not used[i - 1]:
                print('  ' * d + f'skip index {i} (value {a[i]}): twin at {i-1} not used'); continue
            used[i] = True; cur.append(a[i]); print('  ' * d + f'pick index {i} -> {cur}'); go(d + 1); cur.pop(); used[i] = False
    go(0)
print('decision tree for [2, 1, 2] (sorted: [1, 2, 2]):')
show_tree([2, 1, 2])

# node counts: no rule vs correct rule vs the other rule, on [1, 1, 2, 2]
for nums in ([1, 2, 2], [1, 1, 2, 2], [1, 1, 1, 2, 2, 3]):
    r0, c0 = no_skip(nums); r1, c1 = perms_dup(nums, 'left_unused'); r2, c2 = perms_dup(nums, 'left_used')
    assert sorted(r1) == brute(nums) and sorted(r2) == brute(nums)
    print(f'{nums}: results={len(r1)} (multinomial {multinomial(nums)}); calls no-rule={c0} (leaves {len(r0)}), left-unused rule={c1}, left-used rule={c2}')

# claim 1: count = multinomial; both rules correct and left-unused never more calls (all multisets of 5 values from {1,2,3}, plus length 0..4)
worse = 0; total = 0
for L in range(0, 7):
    for nums in itertools.product([1, 2, 3], repeat=L):
        if L > 5 and sum(nums) % 7: continue       # thin the length-6 family to keep it quick
        total += 1
        r1, c1 = perms_dup(list(nums), 'left_unused'); r2, c2 = perms_dup(list(nums), 'left_used')
        assert len(r1) == multinomial(nums) and r1 == sorted(r1) and len(set(map(tuple, r1))) == len(r1)
        assert sorted(r2) == r1
        assert c1 <= c2
        worse += c1 < c2
print('inputs checked', total, '| count == multinomial and both rules right on all; left-unused fewer calls on', worse)

# claim 2: equal values keep their ORIGINAL relative order (tag the twins and look at the generated order)
a = [(1, 'a'), (1, 'b'), (2, 'c')]
tagged = []
used = [False] * 3; cur = []
def go():
    if len(cur) == 3: tagged.append([t[1] for t in cur]); return
    for i in range(3):
        if used[i]: continue
        if i and a[i][0] == a[i - 1][0] and not used[i - 1]: continue
        used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
go()
print('tagged twins 1a, 1b, 2c; each leaf lists tags in order:', tagged)
assert all(t.index('a') < t.index('b') for t in tagged)

# seeded random cross-check against set(itertools.permutations)
for _ in range(400):
    n = random.randint(0, 7); nums = [random.randint(0, 3) for _ in range(n)]
    assert permutations_dup(nums) == brute(nums), nums
print('400 seeded random cases agree')

# edge asserts
assert permutations_dup([]) == [[]] and permutations_dup([7, 7, 7]) == [[7, 7, 7]]
assert permutations_dup([-1, 0, -1]) == [[-1, -1, 0], [-1, 0, -1], [0, -1, -1]]
assert len(permutations_dup([1, 2, 3, 4, 5, 6, 7, 8])) == 40320 and len(permutations_dup([1] * 8)) == 1
print('edge asserts passed; 8 distinct values ->', len(permutations_dup(list(range(8)))), 'results; recursion depth <= 8')
```

**Output (my run):**
```
example [2, 1, 2] -> [[1, 2, 2], [2, 1, 2], [2, 2, 1]]
example [5] -> [[5]]
example [] -> [[]]
example [3, 3, 1, 1] -> [[1, 1, 3, 3], [1, 3, 1, 3], [1, 3, 3, 1], [3, 1, 1, 3], [3, 1, 3, 1], [3, 3, 1, 1]]
decision tree for [2, 1, 2] (sorted: [1, 2, 2]):
pick index 0 -> [1]
  pick index 1 -> [1, 2]
    pick index 2 -> [1, 2, 2]
      -> leaf [1, 2, 2]
  skip index 2 (value 2): twin at 1 not used
pick index 1 -> [2]
  pick index 0 -> [2, 1]
    pick index 2 -> [2, 1, 2]
      -> leaf [2, 1, 2]
  pick index 2 -> [2, 2]
    pick index 0 -> [2, 2, 1]
      -> leaf [2, 2, 1]
skip index 2 (value 2): twin at 1 not used
[1, 2, 2]: results=3 (multinomial 3); calls no-rule=16 (leaves 6), left-unused rule=9, left-used rule=12
[1, 1, 2, 2]: results=6 (multinomial 6); calls no-rule=65 (leaves 24), left-unused rule=19, left-used rule=33
[1, 1, 1, 2, 2, 3]: results=60 (multinomial 60); calls no-rule=1957 (leaves 720), left-unused rule=189, left-used rule=517
inputs checked 460 | count == multinomial and both rules right on all; left-unused fewer calls on 444
tagged twins 1a, 1b, 2c; each leaf lists tags in order: [['a', 'b', 'c'], ['a', 'c', 'b'], ['c', 'a', 'b']]
400 seeded random cases agree
edge asserts passed; 8 distinct values -> 40320 results; recursion depth <= 8
```

Reading the output:
- All four examples match the `set(itertools.permutations)` oracle.
- Calls on `[1,1,1,2,2,3]`: 1957 with no rule (720 leaves, 60 distinct), 517 with the `used[i-1]` rule, 189 with the tight rule. The tight rule's calls scale with the answer, not with `n!`.
- Over 460 small inputs (every list of values from {1,2,3} of length 0 to 5, plus a thinned set of length 6) the count equals the multinomial, both rules return the right set, and the tight rule never makes more calls (fewer on 444; equal on the all-distinct ones).
- Tagged twins: every leaf has `a` before `b`, as the argument says.
- 400 seeded random lists agree with the oracle.

**Edge cases:**
- `[]` returns `[[]]`.
- One value, or all values equal: one result.
- Negative numbers and zero: sorting handles them.
- 8 distinct values: 40320 results, the largest output here.

**Follow-ups:**
- "Swap-in-place variant?" Possible, but sorting plus a `used` array is simpler for duplicates. In-place swapping needs a per-level set of values already tried at that position.
- "Next permutation instead of listing?" Part 1 Q34 steps to the next arrangement in this same order in O(n) with no recursion; it also handles duplicates.
- "Count only?" Use the multinomial formula, no search.

**Common mistakes:**
- Not sorting first: equal values are then not adjacent and the neighbour test misses them.
- Testing `a[i] == a[i-1]` without the `used` condition: kills valid results such as `[2,2,1]`.
- Using `i > 0` with `used[i-1]` backwards and thinking it is wrong: both directions are correct, one is just slower.
- Appending `cur` instead of a copy `cur[:]`.
- Putting the results in a set of tuples to dedupe afterwards: correct, but it throws away the pruning.

### Q20 ⭐⭐ 🟡 Combinations n choose k. `n` and `k` are integers with 1 <= k <= n <= 20. Return every k-element subset of 1..n as an ascending list; the outer list is sorted ascending with Python's list comparison (so the first is [1, 2, ..., k]). The number of results is C(n, k) (at most 184756). Use a start index so each combination is built once, and add the pruning bound: from start `s` you need at least `k - len(path)` more numbers, so the loop can stop at `n - (k - len(path)) + 1`; explain how much work this saves with a node count on one example. Depth is k <= 20. In the answer include a dry run on the first example and a seeded random cross-check of your solution against itertools.combinations on small inputs. Example: n=5, k=3 -> [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5], [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5], [3, 4, 5]]; n=3, k=3 -> [[1, 2, 3]]; n=4, k=1 -> [[1], [2], [3], [4]]; n=1, k=1 -> [[1]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with a start index (choose in increasing order, so each subset is built once) and a feasibility bound on the loop (do not start a branch that cannot finish).

**Say this first (1 line):** "Build the subset in ascending order with a start index; and stop the loop early at `n - (k - len(path)) + 1`, because past that point there are not enough numbers left to reach size `k`."

**Brute force:** `itertools.combinations(range(1, n+1), k)`, which is also the oracle. Or, the unpruned recursion: same start-index tree but the loop always runs to `n`. It finds the same `C(n, k)` answers but visits many dead nodes whose path can never reach length `k`.

**Optimal:**
- `go(start)`: if `len(path) == k`, record a copy. Otherwise loop `v` from `start` to `hi`, push `v`, call `go(v + 1)`, pop.
- Start index: after choosing `v`, only larger numbers follow, so `[1,3]` is built but `[3,1]` never is. Each subset is built exactly once, already ascending, and the outer list comes out in ascending list order for free.
- Pruning rule: we still need `need = k - len(path)` numbers, all from `v..n`. The last value that leaves room is `v = n - need + 1`. So `hi = n - (k - len(path)) + 1`. Every node visited with this rule leads to at least one answer, so there are no dead nodes.
- Node count: the number of nodes at depth `d` is the number of valid prefixes, `C(n-k+d, d)`. So calls are `sum_{d=0..k} C(n-k+d, d)`. Checked for all `1 <= k <= n <= 8` in the code.

**Complexity:** Output is `C(n, k)` lists of length `k`, so time O(k * C(n, k)) for the copies. With pruning, the tree has `sum_d C(n-k+d, d)` nodes, which is O(k * C(n, k)) at worst, no wasted exponential. Without pruning the tree can be far larger than the output (see the table below). Space O(k) for the path and recursion (depth `k <= 20`, far below the limit of 1000), apart from the output. Largest case: `C(20, 10) = 184756` results.

**Dry run:** `n = 5, k = 3`. The bound `hi` is 3 at depth 0, 4 at depth 1, 5 at depth 2.
- Root: `v` runs 1..3 (4 and 5 cannot leave room for two more numbers).
- Pick 1: next `v` runs 2..4. Pick 2, then 3..5 gives `[1,2,3]`, `[1,2,4]`, `[1,2,5]`. Pick 3, then 4..5 gives `[1,3,4]`, `[1,3,5]`. Pick 4, then 5 gives `[1,4,5]`. (5 is not tried at this level: nothing would follow.)
- Pick 2: `[2,3,4]`, `[2,3,5]`, `[2,4,5]`. Pick 3: `[3,4,5]`.
- 10 results. Calls: 1 + 3 + 6 + 10 = 20 nodes (`C(2,0)+C(3,1)+C(4,2)+C(5,3)`). Without the bound the loop runs to 5 everywhere and visits 26 nodes, 6 of them dead (for instance `[4]` and `[5]` at the top, and `[1,5]`).
- The code also prints the full pruned tree for `n=4, k=2`.

**Code:**
```python
import itertools, random, math

random.seed(20)

def combinations(n, k, prune=True):
    """All k-subsets of 1..n ascending. Returns (result, calls). prune=True stops the loop at n-(k-len(path))+1."""
    out = []; path = []; calls = 0
    def go(start):
        nonlocal calls
        calls += 1
        if len(path) == k:
            out.append(path[:]); return
        hi = n - (k - len(path)) + 1 if prune else n      # last value that still leaves room for the rest
        for v in range(start, hi + 1):
            path.append(v); go(v + 1); path.pop()
    go(1)
    return out, calls

def solve(n, k): return combinations(n, k)[0]
def brute(n, k): return sorted(map(list, itertools.combinations(range(1, n + 1), k)))

for n, k, exp in [(5, 3, [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5], [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5], [3, 4, 5]]),
                  (3, 3, [[1, 2, 3]]), (4, 1, [[1], [2], [3], [4]]), (1, 1, [[1]])]:
    got = solve(n, k)
    assert got == exp == brute(n, k)
    print('example', (n, k), '->', got)

# decision tree for n=4, k=2 with pruning (X = value cut by the bound)
def tree(n, k):
    path = []
    def go(start, d):
        if len(path) == k: print('  ' * d + '-> leaf', path); return
        hi = n - (k - len(path)) + 1
        for v in range(start, hi + 1):
            path.append(v); print('  ' * d + f'pick {v} -> {path}'); go(v + 1, d + 1); path.pop()
        if hi < n: print('  ' * d + f'(loop stops at {hi}; values {hi + 1}..{n} cannot leave room for {k - len(path)} number(s))')
    go(1, 0)
print('decision tree n=4, k=2 (pruned):'); tree(4, 2)

# node counts: pruned vs unpruned
print('calls (nodes visited), pruned vs unpruned:')
for n, k in [(5, 3), (6, 4), (10, 8), (12, 10), (20, 19), (20, 10)]:
    r1, c1 = combinations(n, k, True); r0, c0 = combinations(n, k, False)
    assert r1 == r0 and len(r1) == math.comb(n, k)
    print(f'  n={n:2d} k={k:2d}: results={len(r1):6d}  pruned={c1:7d}  unpruned={c0:7d}  dead nodes removed={c0 - c1}')

# claim: pruned search has no dead nodes: every call is on a path to a result, calls = sum over depth of C(n, depth)-ish. Check exact formula
# number of calls at depth d = number of valid prefixes of length d = C(n-k+d, d) ... verify by counting
for n in range(1, 9):
    for k in range(1, n + 1):
        r1, c1 = combinations(n, k, True)
        assert c1 == sum(math.comb(n - k + d, d) for d in range(k + 1)), (n, k)
print('pruned calls == sum_d C(n-k+d, d) for all 1 <= k <= n <= 8')
# and unpruned never fewer than pruned
for n in range(1, 11):
    for k in range(1, n + 1):
        assert combinations(n, k, True)[1] <= combinations(n, k, False)[1]
print('pruned calls <= unpruned calls for all 1 <= k <= n <= 10')

# size claim
big = solve(20, 10)
assert len(big) == 184756 == math.comb(20, 10) and big[0] == list(range(1, 11)) and big[-1] == list(range(11, 21))
print('C(20, 10) =', len(big), ' first', big[0], ' last', big[-1])
assert max(math.comb(20, k) for k in range(1, 21)) == 184756

# seeded random cross-check vs itertools.combinations
for _ in range(300):
    n = random.randint(1, 9); k = random.randint(1, n)
    assert solve(n, k) == brute(n, k) == sorted(solve(n, k))
print('300 seeded random cases agree; also exhaustive over 1 <= k <= n <= 10')
for n in range(1, 11):
    for k in range(1, n + 1): assert solve(n, k) == brute(n, k)
assert solve(1, 1) == [[1]] and solve(4, 4) == [[1, 2, 3, 4]]
print('edge asserts passed; depth is k <= 20, recursion limit 1000 is no problem')
```

**Output (my run):**
```
example (5, 3) -> [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5], [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5], [3, 4, 5]]
example (3, 3) -> [[1, 2, 3]]
example (4, 1) -> [[1], [2], [3], [4]]
example (1, 1) -> [[1]]
decision tree n=4, k=2 (pruned):
pick 1 -> [1]
  pick 2 -> [1, 2]
    -> leaf [1, 2]
  pick 3 -> [1, 3]
    -> leaf [1, 3]
  pick 4 -> [1, 4]
    -> leaf [1, 4]
pick 2 -> [2]
  pick 3 -> [2, 3]
    -> leaf [2, 3]
  pick 4 -> [2, 4]
    -> leaf [2, 4]
pick 3 -> [3]
  pick 4 -> [3, 4]
    -> leaf [3, 4]
(loop stops at 3; values 4..4 cannot leave room for 2 number(s))
calls (nodes visited), pruned vs unpruned:
  n= 5 k= 3: results=    10  pruned=     20  unpruned=     26  dead nodes removed=6
  n= 6 k= 4: results=    15  pruned=     35  unpruned=     57  dead nodes removed=22
  n=10 k= 8: results=    45  pruned=    165  unpruned=   1013  dead nodes removed=848
  n=12 k=10: results=    66  pruned=    286  unpruned=   4083  dead nodes removed=3797
  n=20 k=19: results=    20  pruned=    210  unpruned=1048575  dead nodes removed=1048365
  n=20 k=10: results=184756  pruned= 352716  unpruned= 616666  dead nodes removed=263950
pruned calls == sum_d C(n-k+d, d) for all 1 <= k <= n <= 8
pruned calls <= unpruned calls for all 1 <= k <= n <= 10
C(20, 10) = 184756  first [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  last [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
300 seeded random cases agree; also exhaustive over 1 <= k <= n <= 10
edge asserts passed; depth is k <= 20, recursion limit 1000 is no problem
```

Reading the output:
- All four examples match `itertools.combinations`.
- The pruned tree for `n=4, k=2` shows the bound cutting the top-level loop at 3.
- Node counts are exact counts of calls. For `n=20, k=19` the answer has 20 lists, the pruned search makes 210 calls, the unpruned search makes 1,048,575 (it walks through every ascending subset of 1..20). For `n=20, k=10` the saving is smaller (352,716 against 616,666) because most nodes there are useful anyway.
- The formula for the pruned call count holds for all `k <= n <= 8`, and pruned is never above unpruned for `n <= 10`.
- 300 seeded random cases plus an exhaustive sweep to `n = 10` agree with the oracle.

**Edge cases:**
- `k = n`: one result, `[1..n]`; the loop bound is tight at every level.
- `k = 1`: `n` singletons.
- `n = k = 1`: `[[1]]`.
- Largest outputs: `n = 20`, `k = 10`, 184756 lists. The memory is for the answer itself.

**Follow-ups:**
- "Where does the pruning matter most?" When `k` is close to `n`: the unpruned tree explores every ascending subset (up to `2^n`) while the answer has only `C(n, k)` lists.
- "Do it without recursion?" Keep an index array `c[0..k-1]` and advance it like an odometer (find the rightmost index that can still grow), or use `itertools.combinations`.
- "With duplicates in the input?" Sort and skip equal neighbours at the same level, as in Q21.

**Common mistakes:**
- Recursing with `go(v)` instead of `go(v + 1)`: reuses numbers.
- Looping from 1 each time instead of `start`: builds permutations, each subset `k!` times.
- Bound off by one: `n - need + 1` is inclusive, so the `range` end is `n - need + 2`.
- Appending `path` instead of `path[:]`; every result becomes the same (empty) list.

### Q21 ⭐⭐ 🟡 Combination sum II (each number used once, duplicates in the input). `candidates` has 1 <= len <= 14 positive integers (each <= 30, repeats allowed) and `target` is 1 <= target <= 40. Return every combination that sums to `target` using each INPUT ELEMENT at most once; two combinations with the same values count once. Each combination is a non-decreasing list and the outer list is sorted ascending with Python's list comparison; return an empty list if none exists. Sort, recurse with `start = j + 1`, skip a value equal to its left neighbour at the same level (`j > start and c[j] == c[j-1]`), and break when `c[j] > remaining`. Say how this differs from Q8 (reuse allowed, so recurse with `j`). In the answer include a dry run on the first example and a seeded random cross-check of your solution against the set of sorted tuples from a bitmask over all subsets on small inputs. Example: candidates=[3, 1, 1, 2, 4, 2], target=6 -> [[1, 1, 2, 2], [1, 1, 4], [1, 2, 3], [2, 4]]; candidates=[2, 2, 2], target=4 -> [[2, 2]]; candidates=[5, 6], target=3 -> []; candidates=[4], target=4 -> [[4]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with a start index that moves forward (`j + 1`, each input element at most once), a sort so equal values sit together, a same-level skip for duplicates, and a `break` once the number is too big.

**Say this first (1 line):** "Sort, recurse with `j + 1` because each element is used once, skip a value equal to its left neighbour at the same level (`j > start`), and break when the number exceeds what is left."

**Brute force:** Try all `2^n` subsets with a bitmask (`n <= 14`, at most 16384), keep the ones summing to `target`, put each into a set as a sorted tuple, sort. Correct, always `O(n * 2^n)`. Used as the oracle.

**Optimal:**
- `go(start, rem)`: if `rem == 0`, record. Else for `j` from `start`: if `c[j] > rem` break (sorted, so all later values are too big); if `j > start` and `c[j] == c[j-1]` continue; take `c[j]`, call `go(j + 1, rem - c[j])`, undo.
- Why `j > start` and not `j > 0`: at a given level, the first copy of a value (`j == start`) is allowed, because its left neighbour was used at a shallower level and is legitimately in the path. Only a second copy tried at the SAME level would repeat a combination already found. The code shows that `j > 0` loses `[1,1,2]` for input `[1,1,2]`, target 4.
- Why the skip is right: choosing the first or the second 2 as "the" 2 at one level leads to the same set of combinations below, so one is enough.
- Difference from Q8 (reuse allowed): there the next call is `go(j, ...)` (same index) and the candidates are distinct; here it is `go(j + 1, ...)` and the skip rule is needed because the input has repeats.

**Complexity:** Worst case still exponential, O(2^n) nodes (all elements distinct, target large) with `n <= 14`. The two prunings only cut: the skip removes whole repeated sub-trees (it takes `[1]*7 + [2]*7` with target 14 from 14920 calls to 48) and the break cuts loop steps. Each result costs O(n) to copy. Space O(n) for the path and recursion depth (at most 14, far below the limit of 1000), plus the output.

**Dry run:** sorted candidates `[1, 1, 2, 2, 3, 4]`, target 6. The code prints the whole tree; the main branches:
- Take `c[0]=1` (remaining 5), then `c[1]=1` (remaining 4), then `c[2]=2` (remaining 2), then `c[3]=2`: hit `[1,1,2,2]`. Next `c[4]=3 > 2`: break.
- Back at the level after `[1,1]`: `c[3]=2` is skipped (same as the left neighbour at this level). Take `3` -> remaining 1, break; take `4` -> hit `[1,1,4]`.
- Under `[1]` take `c[2]=2`: `[1,2,2]` has remaining 1, break; `[1,2,3]` hit. Skip `c[3]=2` at that level. Take 3 and 4: no hits.
- Top level: `c[1]=1` is skipped (twin of `c[0]` at the same level). Take `c[2]=2`: `[2,4]` hit. Skip `c[3]`. Take 3 and 4: none.
- Four hits, in ascending order: `[1,1,2,2]`, `[1,1,4]`, `[1,2,3]`, `[2,4]`. Calls: 18 with both rules; 32 with no skip rule (the repeated twins re-explore the same sub-trees).

**Code:**
```python
import itertools, random

random.seed(21)

def comb_sum2(candidates, target, skip=True, brk=True):
    """Each input element at most once; each distinct combination once. Returns (result, calls)."""
    c = sorted(candidates); out = []; cur = []; calls = 0; iters = 0
    def go(start, rem):
        nonlocal calls, iters
        calls += 1
        if rem == 0:
            out.append(cur[:]); return
        for j in range(start, len(c)):
            iters += 1
            if c[j] > rem:
                if brk: break
                continue
            if skip and j > start and c[j] == c[j - 1]: continue     # same value already tried at this level
            cur.append(c[j]); go(j + 1, rem - c[j]); cur.pop()
    go(0, target)
    comb_sum2.iters = iters
    return out, calls

def solve(candidates, target): return sorted(comb_sum2(candidates, target)[0])

def brute(candidates, target):
    n = len(candidates); res = set()
    for mask in range(1, 1 << n):
        sub = tuple(sorted(candidates[i] for i in range(n) if mask >> i & 1))
        if sum(sub) == target: res.add(sub)
    return sorted(map(list, res))

for cand, t, exp in [([3, 1, 1, 2, 4, 2], 6, [[1, 1, 2, 2], [1, 1, 4], [1, 2, 3], [2, 4]]),
                     ([2, 2, 2], 4, [[2, 2]]), ([5, 6], 3, []), ([4], 4, [[4]])]:
    got = solve(cand, t)
    assert got == exp == brute(cand, t)
    print('example', cand, t, '->', got)

def tree(cand, target):
    c = sorted(cand); cur = []
    def go(start, rem, d):
        if rem == 0: print('  ' * d + '-> hit', cur); return
        for j in range(start, len(c)):
            if c[j] > rem: print('  ' * d + f'break: c[{j}]={c[j]} > remaining {rem}'); break
            if j > start and c[j] == c[j - 1]: print('  ' * d + f'skip c[{j}]={c[j]} (same as left neighbour at this level)'); continue
            cur.append(c[j]); print('  ' * d + f'take c[{j}]={c[j]} -> {cur}, remaining {rem - c[j]}'); go(j + 1, rem - c[j], d + 1); cur.pop()
    go(0, target, 0)
print('decision tree, sorted candidates [1, 1, 2, 2, 3, 4], target 6:'); tree([3, 1, 1, 2, 4, 2], 6)

# node counts: all four combinations of the two prunings on the first example and a larger one
def compare(cand, t):
    row = {}
    for skip in (False, True):
        for brk in (False, True):
            r, calls = comb_sum2(cand, t, skip, brk); row[(skip, brk)] = (calls, comb_sum2.iters)
            assert len(set(map(tuple, r))) == len(solve(cand, t)) and sorted(set(map(tuple, r))) == sorted(map(tuple, solve(cand, t)))
    return row
for cand, t in [([3, 1, 1, 2, 4, 2], 6), ([1] * 7 + [2] * 7, 14), ([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5], 20)]:
    row = compare(cand, t)
    print(f'{len(cand)} candidates, target {t}, answers {len(solve(cand, t))}: (calls, loop steps): neither={row[(False, False)]}, break only={row[(False, True)]}, skip only={row[(True, False)]}, both={row[(True, True)]}')

# without the skip rule duplicates appear:
r, _ = comb_sum2([2, 2, 2], 4, skip=False)
print('no skip rule on [2, 2, 2], target 4:', r, '(three copies of [2, 2])')
# with j > 0 instead of j > start the valid [1, 1, 2] is lost for [1, 1, 2], target 4
def wrong_skip(candidates, target):
    c = sorted(candidates); out = []; cur = []
    def go(start, rem):
        if rem == 0: out.append(cur[:]); return
        for j in range(start, len(c)):
            if c[j] > rem: break
            if j > 0 and c[j] == c[j - 1]: continue            # WRONG: compares with the global left neighbour
            cur.append(c[j]); go(j + 1, rem - c[j]); cur.pop()
    go(0, target); return out
print('wrong test j > 0 on [1, 1, 2], target 4 ->', wrong_skip([1, 1, 2], 4), ' correct ->', solve([1, 1, 2], 4))
assert wrong_skip([1, 1, 2], 4) == [] and solve([1, 1, 2], 4) == [[1, 1, 2]]

# Q8 difference: recursing with j reuses an element
def reuse(candidates, target):
    c = sorted(set(candidates)); out = []; cur = []
    def go(start, rem):
        if rem == 0: out.append(cur[:]); return
        for j in range(start, len(c)):
            if c[j] > rem: break
            cur.append(c[j]); go(j, rem - c[j]); cur.pop()
    go(0, target); return out
print('Q8 style (reuse, recurse with j) on [3, 1, 2, 4], target 6:', reuse([3, 1, 2, 4], 6))
print('once-each (this question) on [3, 1, 2, 4], target 6:', solve([3, 1, 2, 4], 6))

# properties and seeded random cross-check vs bitmask
for _ in range(400):
    n = random.randint(1, 10); cand = [random.randint(1, 6) for _ in range(n)]; t = random.randint(1, 20)
    got = solve(cand, t)
    assert got == brute(cand, t), (cand, t)
    assert got == sorted(got) and len({tuple(x) for x in got}) == len(got)
    assert all(x == sorted(x) and sum(x) == t for x in got)
print('400 seeded random cases agree (sorted, no duplicates, each sums to target)')

# edge and max size asserts
assert solve([4], 4) == [[4]] and solve([5, 6], 3) == [] and solve([1], 2) == []
big = solve([1] * 14, 14); assert big == [[1] * 14]
print('14 ones, target 14 ->', len(big), 'combination; depth up to 14, well under the recursion limit of 1000')
print('edge asserts passed')
```

**Output (my run):**
```
example [3, 1, 1, 2, 4, 2] 6 -> [[1, 1, 2, 2], [1, 1, 4], [1, 2, 3], [2, 4]]
example [2, 2, 2] 4 -> [[2, 2]]
example [5, 6] 3 -> []
example [4] 4 -> [[4]]
decision tree, sorted candidates [1, 1, 2, 2, 3, 4], target 6:
take c[0]=1 -> [1], remaining 5
  take c[1]=1 -> [1, 1], remaining 4
    take c[2]=2 -> [1, 1, 2], remaining 2
      take c[3]=2 -> [1, 1, 2, 2], remaining 0
        -> hit [1, 1, 2, 2]
      break: c[4]=3 > remaining 2
    skip c[3]=2 (same as left neighbour at this level)
    take c[4]=3 -> [1, 1, 3], remaining 1
      break: c[5]=4 > remaining 1
    take c[5]=4 -> [1, 1, 4], remaining 0
      -> hit [1, 1, 4]
  take c[2]=2 -> [1, 2], remaining 3
    take c[3]=2 -> [1, 2, 2], remaining 1
      break: c[4]=3 > remaining 1
    take c[4]=3 -> [1, 2, 3], remaining 0
      -> hit [1, 2, 3]
    break: c[5]=4 > remaining 3
  skip c[3]=2 (same as left neighbour at this level)
  take c[4]=3 -> [1, 3], remaining 2
    break: c[5]=4 > remaining 2
  take c[5]=4 -> [1, 4], remaining 1
skip c[1]=1 (same as left neighbour at this level)
take c[2]=2 -> [2], remaining 4
  take c[3]=2 -> [2, 2], remaining 2
    break: c[4]=3 > remaining 2
  take c[4]=3 -> [2, 3], remaining 1
    break: c[5]=4 > remaining 1
  take c[5]=4 -> [2, 4], remaining 0
    -> hit [2, 4]
skip c[3]=2 (same as left neighbour at this level)
take c[4]=3 -> [3], remaining 3
  break: c[5]=4 > remaining 3
take c[5]=4 -> [4], remaining 2
6 candidates, target 6, answers 4: (calls, loop steps): neither=(32, 51), break only=(32, 46), skip only=(18, 32), both=(18, 29)
14 candidates, target 14, answers 4: (calls, loop steps): neither=(14920, 15647), break only=(14920, 15471), skip only=(48, 232), both=(48, 226)
14 candidates, target 20, answers 40: (calls, loop steps): neither=(8728, 12572), break only=(8728, 11041), skip only=(404, 989), both=(404, 890)
no skip rule on [2, 2, 2], target 4: [[2, 2], [2, 2], [2, 2]] (three copies of [2, 2])
wrong test j > 0 on [1, 1, 2], target 4 -> []  correct -> [[1, 1, 2]]
Q8 style (reuse, recurse with j) on [3, 1, 2, 4], target 6: [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 2], [1, 1, 1, 3], [1, 1, 2, 2], [1, 1, 4], [1, 2, 3], [2, 2, 2], [2, 4], [3, 3]]
once-each (this question) on [3, 1, 2, 4], target 6: [[1, 2, 3], [2, 4]]
400 seeded random cases agree (sorted, no duplicates, each sums to target)
14 ones, target 14 -> 1 combination; depth up to 14, well under the recursion limit of 1000
edge asserts passed
```

Reading the output:
- All four examples match the bitmask oracle.
- Node counts: "calls" is the number of recursive calls and "loop steps" is how often the inner loop body starts. The skip rule is the big saver in calls (14920 down to 48 on the two-value input); the break only saves loop steps (15647 down to 15471 without the skip rule, 232 down to 226 with it). They do different jobs.
- Without the skip rule `[2,2,2]` target 4 returns `[2,2]` three times; with `j > 0` the valid `[1,1,2]` is lost.
- The Q8 contrast on `[3,1,2,4]`, target 6: reuse gives 9 combinations including `[1,1,1,1,1,1]`; once-each gives only `[1,2,3]` and `[2,4]`.
- 400 seeded random inputs agree, each output sorted, duplicate-free, with every combination summing to the target.

**Edge cases:**
- No combination (`[5,6]`, target 3): `[]`.
- All equal (`[2,2,2]`, target 4): one result.
- A single element equal to the target: one result.
- Target bigger than the total sum: the search ends with no result; a cheap pre-check on the total would skip the search.
- `14` ones with target 14: depth 14, one result.

**Follow-ups:**
- "Why not use a set of tuples to remove duplicates?" It is right but explores every duplicate sub-tree first; the skip rule never builds them.
- "Count instead of list?" Group equal values with counts and do a bounded knapsack DP over the target (Part 10 style); no list needed.
- "Reuse allowed but duplicates in the input?" Deduplicate first, then it is Q8.

**Common mistakes:**
- Forgetting to sort: neighbours are not equal, so the skip never triggers.
- `j > 0` instead of `j > start`.
- `go(j, ...)` instead of `go(j + 1, ...)`: reuses an element.
- Using `continue` instead of `break` on `c[j] > rem`: correct but slower.
- Appending the live `cur` instead of a copy.

### Q22 ⭐⭐ 🟡 Palindrome partitioning (list all). `s` is a lowercase string with 1 <= len <= 16. Return every way to cut `s` into consecutive pieces that are all palindromes: each partition is a list of the pieces in order, and the outer list is sorted ascending with Python's list comparison. For 'aaa' the single piece 'aaa' counts as a partition. Recurse over the cut position and test each piece with `t == t[::-1]`; then precompute an `is_pal[i][j]` table so each test is O(1) and say what that changes (the number of partitions can be 2^(n-1), so listing them stays exponential). Part 11 Q19 asks the optimisation version (fewest cuts) as a DP instead of a list. Depth is at most 16. In the answer include a dry run on the first example and a seeded random cross-check of your solution against trying all 2^(n-1) sets of cut positions on small inputs. Example: s='abba' -> [['a', 'b', 'b', 'a'], ['a', 'bb', 'a'], ['abba']]; s='xyz' -> [['x', 'y', 'z']]; s='aaa' -> [['a', 'a', 'a'], ['a', 'aa'], ['aa', 'a'], ['aaa']]; s='a' -> [['a']].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking over cut positions: at position `i`, try every piece `s[i:j]`, and only recurse when the piece is a palindrome. The palindrome test is the pruning.

**Say this first (1 line):** "At each position I try each possible next piece, keep only the palindromic ones, and recurse after it. Dead ends are cut the moment a piece is not a palindrome, and a precomputed table makes that test O(1)."

**Brute force:** Try all `2^(n-1)` sets of cut positions (each gap between letters is cut or not), build the pieces, keep the sets where every piece is a palindrome. `n <= 16` gives at most 32768 sets, each checked in O(n). Used as the oracle. It does the full exponential work even for `'abcdefghijklmnop'`, whose only answer is the all-singles split.

**Optimal:**
- `go(i)`: if `i == n`, record the partition. Else for `j` from `i + 1` to `n`: `t = s[i:j]`; if `t == t[::-1]`, push `t`, call `go(j)`, pop.
- The pruning rule is "only recurse on a palindromic piece". A non-palindromic piece is never extended, so none of the partitions built from it are visited. Every single letter is a palindrome, so every call can finish: no dead nodes beyond the failed piece tests.
- Table version: `is_pal[i][j] = s[i] == s[j] and (j - i < 2 or is_pal[i+1][j-1])`, filled with `i` going down. O(n^2) once. Then each test is one lookup instead of a slice, a reverse and a compare (O(piece length)).
- What the table changes and what it does not: it cuts the cost of each test from O(L) to O(1), so the work between recursive calls drops. It does NOT change how many partitions exist, nor how many calls are made (same counts in the output). For `a^n` the answer has `2^(n-1)` partitions, so listing is exponential whatever the test costs.
- Order: pieces are tried short to long, so the output is already ascending in Python's list order (`['a','b','b','a']` before `['a','bb','a']` before `['abba']`); sorting is only a safety net, and the code checks it is unnecessary.

**Complexity:** Output: up to `2^(n-1)` partitions of total length `n` each, so O(n * 2^(n-1)) in the worst case (`'aaaa...'`). Search with the table: each call does up to `n` constant-time tests, so time is O(n * number of calls) plus the O(n^2) table; calls are at most about `2^n`. Space: table O(n^2) (256 cells here), path and recursion depth at most 16, plus the output.

**Dry run:** `s = 'abba'` (printed as a tree by the code).
- Position 0: piece `'a'` is a palindrome. Position 1: `'b'` ok; position 2: `'b'` ok; position 3: `'a'` ok; position 4 = end: record `['a','b','b','a']`.
- Back at position 2: piece `'ba'` is not a palindrome: pruned.
- Back at position 1: piece `'bb'` ok; position 3: `'a'`: record `['a','bb','a']`. Piece `'bba'`: pruned.
- Back at position 0: `'ab'` and `'abb'` pruned. `'abba'` ok: record `['abba']`.
- Three partitions. The recursion makes 8 calls and 11 piece tests; the unpruned search would try all `2^3 = 8` cut sets and check each one.

**Code:**
```python
import itertools, random

random.seed(22)

def partition_slice(s):
    """Recurse over the cut position; test each piece with t == t[::-1]. Returns (result, calls, piece_tests, char_compares_upper_bound)."""
    out = []; cur = []; st = {'calls': 0, 'tests': 0}
    def go(i):
        st['calls'] += 1
        if i == len(s):
            out.append(cur[:]); return
        for j in range(i + 1, len(s) + 1):
            t = s[i:j]; st['tests'] += 1
            if t == t[::-1]:
                cur.append(t); go(j); cur.pop()
    go(0)
    return out, st['calls'], st['tests']

def partition_table(s):
    """Same recursion, but each piece test is a lookup in is_pal[i][j] (inclusive ends), built once in O(n^2)."""
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            is_pal[i][j] = s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1])
    out = []; cur = []; st = {'calls': 0, 'tests': 0}
    def go(i):
        st['calls'] += 1
        if i == n:
            out.append(cur[:]); return
        for j in range(i, n):
            st['tests'] += 1
            if is_pal[i][j]:
                cur.append(s[i:j + 1]); go(j + 1); cur.pop()
    go(0)
    return out, st['calls'], st['tests']

def solve(s): return sorted(partition_table(s)[0])

def brute(s):
    n = len(s); out = []
    for mask in range(1 << (n - 1)):                       # bit i set = cut after position i
        cuts = [i + 1 for i in range(n - 1) if mask >> i & 1]; ed = [0] + cuts + [n]
        parts = [s[ed[i]:ed[i + 1]] for i in range(len(ed) - 1)]
        if all(p == p[::-1] for p in parts): out.append(parts)
    return sorted(out)

for s, exp in [('abba', [['a', 'b', 'b', 'a'], ['a', 'bb', 'a'], ['abba']]), ('xyz', [['x', 'y', 'z']]),
               ('aaa', [['a', 'a', 'a'], ['a', 'aa'], ['aa', 'a'], ['aaa']]), ('a', [['a']])]:
    got = solve(s)
    assert got == exp == brute(s) == sorted(partition_slice(s)[0])
    print('example', repr(s), '->', got)

def tree(s):
    cur = []
    def go(i, d):
        if i == len(s): print('  ' * d + '-> partition', cur); return
        for j in range(i + 1, len(s) + 1):
            t = s[i:j]
            if t == t[::-1]:
                cur.append(t); print('  ' * d + f'cut piece {t!r} -> {cur}'); go(j, d + 1); cur.pop()
            else: print('  ' * d + f'piece {t!r} is not a palindrome: pruned')
    go(0, 0)
print("decision tree for 'abba':"); tree('abba')

# node counts: palindrome-pruned search vs trying every cut set (2^(n-1) leaves, each with n-1 cut bits)
print('calls / piece tests for the recursion (slice test vs table), and the unpruned number of cut sets 2^(n-1):')
for s in ['abba', 'aaaaaaaa', 'abcdefgh', 'abababab', 'a' * 16, 'abcdefghijklmnop']:
    r1, c1, t1 = partition_slice(s); r2, c2, t2 = partition_table(s)
    assert r1 == r2 and r1 == sorted(r1)
    print(f'  {s:18s} partitions={len(r1):6d} calls={c1:6d} piece tests={t1:7d} (table: {t2}) unpruned cut sets={2 ** (len(s) - 1)}')

# claim: all-equal letters give 2^(n-1) partitions (n <= 12 exhaustive), so listing stays exponential even with the table
for n in range(1, 13): assert len(solve('a' * n)) == 2 ** (n - 1)
print('a^n has exactly 2^(n-1) partitions for n = 1..12; a^16 ->', len(solve('a' * 16)))

# the table builds in O(n^2) and the recursion does a bounded number of table lookups per call (n at most)
# seeded random cross-check vs all 2^(n-1) cut sets
for _ in range(300):
    n = random.randint(1, 12); s = ''.join(random.choice('ab') if random.random() < .8 else random.choice('abc') for _ in range(n))
    assert solve(s) == brute(s), s
    assert partition_slice(s)[0] == sorted(partition_slice(s)[0]) == solve(s)
print('300 seeded random strings (length 1..12) agree; both versions return the list already sorted')

# edge asserts
assert solve('a') == [['a']] and solve('ab') == [['a', 'b']] and solve('aa') == [['a', 'a'], ['aa']]
assert len(solve('abcdefghijklmnop')) == 1
print('edge asserts passed; depth <= 16, recursion limit 1000 is no issue')
```

**Output (my run):**
```
example 'abba' -> [['a', 'b', 'b', 'a'], ['a', 'bb', 'a'], ['abba']]
example 'xyz' -> [['x', 'y', 'z']]
example 'aaa' -> [['a', 'a', 'a'], ['a', 'aa'], ['aa', 'a'], ['aaa']]
example 'a' -> [['a']]
decision tree for 'abba':
cut piece 'a' -> ['a']
  cut piece 'b' -> ['a', 'b']
    cut piece 'b' -> ['a', 'b', 'b']
      cut piece 'a' -> ['a', 'b', 'b', 'a']
        -> partition ['a', 'b', 'b', 'a']
    piece 'ba' is not a palindrome: pruned
  cut piece 'bb' -> ['a', 'bb']
    cut piece 'a' -> ['a', 'bb', 'a']
      -> partition ['a', 'bb', 'a']
  piece 'bba' is not a palindrome: pruned
piece 'ab' is not a palindrome: pruned
piece 'abb' is not a palindrome: pruned
cut piece 'abba' -> ['abba']
  -> partition ['abba']
calls / piece tests for the recursion (slice test vs table), and the unpruned number of cut sets 2^(n-1):
  abba               partitions=     3 calls=     8 piece tests=     11 (table: 11) unpruned cut sets=8
  aaaaaaaa           partitions=   128 calls=   256 piece tests=    255 (table: 255) unpruned cut sets=128
  abcdefgh           partitions=     1 calls=     9 piece tests=     36 (table: 36) unpruned cut sets=128
  abababab           partitions=    21 calls=    55 piece tests=     87 (table: 87) unpruned cut sets=128
  aaaaaaaaaaaaaaaa   partitions= 32768 calls= 65536 piece tests=  65535 (table: 65535) unpruned cut sets=32768
  abcdefghijklmnop   partitions=     1 calls=    17 piece tests=    136 (table: 136) unpruned cut sets=32768
a^n has exactly 2^(n-1) partitions for n = 1..12; a^16 -> 32768
300 seeded random strings (length 1..12) agree; both versions return the list already sorted
edge asserts passed; depth <= 16, recursion limit 1000 is no issue
```

Reading the output:
- All four examples agree with the cut-set oracle.
- Node counts: on `'abcdefghijklmnop'` the pruned search makes 17 calls (one per position plus the end) against 32768 cut sets unpruned. On `'abababab'`: 55 calls against 128. On `'a'*16` there is no pruning to be had: 65536 calls, 32768 partitions (every cut set is valid).
- The slice test and the table test give identical call and test counts: the table only makes each test cheaper.
- `a^n` gives `2^(n-1)` partitions for `n = 1..12` (exhaustive), and 32768 at `n = 16`.
- 300 seeded random strings of length 1 to 12 over `a`, `b`, `c` agree with the oracle.

**Edge cases:**
- Single letter: `[['a']]`.
- No repeated letters: only the all-singles split.
- All equal letters: `2^(n-1)` partitions, the worst case for output size.
- Whole string a palindrome: the one-piece partition is included (`'aaa'` gives `['aaa']`).

**Follow-ups:**
- "Fewest cuts instead of a list?" That is a DP: Part 11 Q19. It counts in O(n^2) and never lists.
- "Count the partitions?" Also a DP, `ways[i]` over suffixes using the same `is_pal` table.
- "Expand-around-centre instead of the table?" Same O(n^2) total, no table; each centre expands while it matches.

**Common mistakes:**
- Using `i` to `j` inclusive in one place and exclusive in another when building `is_pal`.
- Forgetting the piece of the whole remaining string (`j` must reach `n`).
- Appending `cur` without copying.
- Thinking the table makes the whole thing polynomial. It cannot: the output itself can have `2^(n-1)` lists.

### Q23 ⭐⭐ 🟡 Restore IP addresses. `s` is a string of digits with 0 <= len <= 12. Return every valid IPv4 address (four parts separated by '.') you can make by inserting three dots into `s` without reordering or removing digits. A part is valid if it is an integer 0..255 written without a leading zero ('0' alone is fine, '01' and '00' are not). Return the addresses sorted ascending as strings, an empty list if none exists (also for len < 4 or len > 12). Recurse over the part index with part lengths 1, 2, 3, and say why the search tree has at most 3^4 = 81 leaves, so it is O(1) in the length. In the answer include a dry run on the first example and a seeded random cross-check of your solution against choosing three cut positions with itertools.combinations on small inputs. Example: s='1921681' -> ['1.9.216.81', '1.92.16.81', '1.92.168.1', '19.2.16.81', '19.2.168.1', '19.21.6.81', '19.21.68.1', '19.216.8.1', '192.1.6.81', '192.1.68.1', '192.16.8.1']; s='0000' -> ['0.0.0.0']; s='010010' -> ['0.10.0.10', '0.100.1.0']; s='111' -> []; s='' -> [].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Fixed-depth backtracking: four parts, each of length 1, 2 or 3, validity checked per part, so the tree is tiny whatever the input.

**Say this first (1 line):** "Four parts, each 1 to 3 digits, so the tree has at most 3^4 = 81 leaves. I recurse over the part index, reject a part with a leading zero or a value above 255, and accept only when four parts use up the whole string."

**Brute force:** Choose three cut positions from the `n - 1` gaps with `itertools.combinations`, split, and validate all four parts. That is `C(11, 3) = 165` choices at `n = 12`, each checked in constant time. Also O(1) in practice; it is the oracle.

**Optimal:**
- `go(i, parts)`: if four parts are placed, accept only when `i == len(s)`. Else try lengths 1, 2, 3.
- A part `t` is valid when `len(t) == L` (enough characters), it has no leading zero unless it is exactly `'0'` (`L > 1 and t[0] == '0'` rejects `'01'`, `'00'`), and `int(t) <= 255`.
- Extra length prune (optional): with `left` parts to place and `rest` characters, give up unless `left <= rest <= 3 * left`. It cuts the long strings and the short strings at the root.
- Why at most 81 leaves: four levels, three choices at each level, `3^4 = 81`. The whole tree has at most `1 + 3 + 9 + 27 + 81 = 121` calls. This does not grow with `len(s)`; `len(s)` only decides which paths are valid, and a string longer than 12 or shorter than 4 has no address.
- Order: the code sorts the strings at the end, which is the order the question asks for (plain string order, where `'.'` sorts before the digits, so `'1.9.216.81'` comes before `'1.92.16.81'`).

**Complexity:** O(1) with respect to `len(s)`: at most 121 calls, each doing O(1) work (slices of at most 3 characters), plus a sort of the addresses. Since `len(s) <= 12` can give at most 81 leaf choices, there are at most 81 addresses (in fact far fewer: the most in the examples is 11). Space O(1): recursion depth 4.

**Dry run:** `'010010'`; the code prints the tree.
- Part 1 can only be `'0'` (`'01'` and `'010'` have a leading zero).
- After `'0'` the rest is `10010`, so part 2 is `'1'`, `'10'` or `'100'`.
  - `'1'`: then part 3 `'0'`, part 4 `'0'` leaves 2 characters (`'10'`): dead. Part 3 `'00'`/`'001'`: leading zero.
  - `'10'`: part 3 `'0'`: part 4 `'1'` leaves 1 character (dead) or `'10'` finishes: `0.10.0.10`. Part 3 `'01'`, `'010'`: leading zero.
  - `'100'`: part 3 `'1'`: part 4 `'0'` finishes: `0.100.1.0`. Part 3 `'10'`: the length prune stops it (0 characters left for 1 part).
- Two addresses: `0.10.0.10` and `0.100.1.0`.

**Code:**
```python
import itertools, random

random.seed(23)

def restore(s, prune_len=True):
    """Returns (sorted addresses, calls). Part lengths 1, 2, 3 tried in that order; no leading zero; value <= 255.
    prune_len=True also stops when the remaining characters cannot fit the remaining parts."""
    out = []; calls = 0
    def go(i, parts):
        nonlocal calls
        calls += 1
        left = 4 - len(parts)
        if left == 0:
            if i == len(s): out.append('.'.join(parts))
            return
        rest = len(s) - i
        if prune_len and not (left <= rest <= 3 * left): return
        for L in (1, 2, 3):
            t = s[i:i + L]
            if len(t) < L or (L > 1 and t[0] == '0') or int(t) > 255: continue
            go(i + L, parts + [t])
    go(0, [])
    return sorted(out), calls

def solve(s): return restore(s)[0]

def brute(s):
    n = len(s); out = []
    if n < 4: return out
    for cuts in itertools.combinations(range(1, n), 3):
        ps = [s[a:b] for a, b in zip((0,) + cuts, cuts + (n,))]
        if all(str(int(p)) == p and int(p) <= 255 for p in ps): out.append('.'.join(ps))
    return sorted(out)

for s, exp in [('1921681', ['1.9.216.81', '1.92.16.81', '1.92.168.1', '19.2.16.81', '19.2.168.1', '19.21.6.81', '19.21.68.1', '19.216.8.1', '192.1.6.81', '192.1.68.1', '192.16.8.1']),
               ('0000', ['0.0.0.0']), ('010010', ['0.10.0.10', '0.100.1.0']), ('111', []), ('', [])]:
    got = solve(s)
    assert got == exp == brute(s)
    print('example', repr(s), '->', got)

def tree(s):
    def go(i, parts, d):
        left = 4 - len(parts)
        if left == 0:
            print('  ' * d + ('-> address ' + '.'.join(parts) if i == len(s) else f'-> parts full but {len(s) - i} char(s) left: dead')); return
        rest = len(s) - i
        if not (left <= rest <= 3 * left): print('  ' * d + f'prune: {rest} char(s) cannot fill {left} part(s)'); return
        for L in (1, 2, 3):
            t = s[i:i + L]
            if len(t) < L: continue
            if L > 1 and t[0] == '0': print('  ' * d + f'{t!r}: leading zero'); continue
            if int(t) > 255: print('  ' * d + f'{t!r}: > 255'); continue
            print('  ' * d + f'part {t!r}'); go(i + L, parts + [t], d + 1)
    go(0, [], 0)
print("decision tree for '010010':"); tree('010010')

# node counts
print('calls: length-pruned vs basic (validity only), 3^4 = 81 leaf choices at most:')
for s in ['1921681', '010010', '0000', '111', '255255255255', '999999999999', '1' * 12, '1' * 13]:
    a, ca = restore(s, True); b, cb = restore(s, False)
    assert a == b
    print(f'  {s:14s} answers={len(a):3d} calls pruned={ca:4d} basic={cb:4d}')

# claim: tree has at most 3^4 = 81 leaves, so at most 1 + 3 + 9 + 27 + 81 = 121 calls
mx = 0; seen = 0
for L in range(0, 9):
    for tup in itertools.product('012', repeat=L):
        s = ''.join(tup); seen += 1
        r, c = restore(s, False); assert c <= 121 and r == brute(s); mx = max(mx, c)
for _ in range(3000):
    s = ''.join(random.choice('0123456789' if random.random() < .5 else '1250') for _ in range(random.randint(0, 12)))
    r, c = restore(s, False); assert c <= 121 and r == brute(s); mx = max(mx, c)
print('basic search never made more than', mx, 'calls (bound 121) over', seen, 'exhaustive strings (digits 0,1,2, length <= 8) + 3000 random ones')

# seeded random cross-check against three-cut-position oracle, with lengths 0..12
for _ in range(400):
    s = ''.join(random.choice('0012559') for _ in range(random.randint(0, 12)))
    assert solve(s) == brute(s), s
print('400 seeded random strings agree with itertools.combinations of cut positions')

# edge asserts
assert solve('') == [] and solve('111') == [] and solve('1' * 13) == [] and solve('0000') == ['0.0.0.0']
assert solve('25525511135') == ['255.255.11.135', '255.255.111.35']
assert solve('256256256256') == [] and solve('255255255255') == ['255.255.255.255'] and solve('00000') == []
assert solve('101023') == sorted(['1.0.10.23', '1.0.102.3', '10.1.0.23', '10.10.2.3', '101.0.2.3'])
print('edge asserts passed')
```

**Output (my run):**
```
example '1921681' -> ['1.9.216.81', '1.92.16.81', '1.92.168.1', '19.2.16.81', '19.2.168.1', '19.21.6.81', '19.21.68.1', '19.216.8.1', '192.1.6.81', '192.1.68.1', '192.16.8.1']
example '0000' -> ['0.0.0.0']
example '010010' -> ['0.10.0.10', '0.100.1.0']
example '111' -> []
example '' -> []
decision tree for '010010':
part '0'
  part '1'
    part '0'
      part '0'
        -> parts full but 2 char(s) left: dead
      '01': leading zero
      '010': leading zero
    '00': leading zero
    '001': leading zero
  part '10'
    part '0'
      part '1'
        -> parts full but 1 char(s) left: dead
      part '10'
        -> address 0.10.0.10
    '01': leading zero
    '010': leading zero
  part '100'
    part '1'
      part '0'
        -> address 0.100.1.0
    part '10'
      prune: 0 char(s) cannot fill 1 part(s)
'01': leading zero
'010': leading zero
calls: length-pruned vs basic (validity only), 3^4 = 81 leaf choices at most:
  1921681        answers= 11 calls pruned=  51 basic=  55
  010010         answers=  2 calls pruned=  13 basic=  13
  0000           answers=  1 calls pruned=   5 basic=   5
  111            answers=  0 calls pruned=   1 basic=   8
  255255255255   answers=  1 calls pruned=  13 basic=  69
  999999999999   answers=  0 calls pruned=   3 basic=  31
  111111111111   answers=  1 calls pruned=  13 basic= 121
  1111111111111  answers=  0 calls pruned=   1 basic= 121
basic search never made more than 104 calls (bound 121) over 9841 exhaustive strings (digits 0,1,2, length <= 8) + 3000 random ones
400 seeded random strings agree with itertools.combinations of cut positions
edge asserts passed
```

Reading the output:
- All five examples agree with the three-cut oracle.
- Node counts (calls). With the length prune: `'1921681'` takes 51 calls for 11 addresses; `'111'` takes 1 call (rejected at the root) against 8 without it; `'1'*13` takes 1 call against 121. Without the prune the largest tree is 121, the bound derived above; over 9841 exhaustive short strings and 3000 random ones the maximum seen was 104.
- 400 seeded random strings of length 0 to 12 (digits from `0,1,2,5,9`) agree with the oracle.
- Edge asserts include `'25525511135'` (two addresses), `'256256256256'` (none: 256 is too big) and `'00000'` (none: five digits but a `'0'` part uses exactly one).

**Edge cases:**
- `''`, length below 4 or above 12: `[]` straight away.
- `'0000'`: only `0.0.0.0`; every part is `'0'`.
- Leading zeros: `'01'`, `'00'`, `'010'` are rejected, `'0'` is fine.
- `'255255255255'`: one address; `'256256256256'`: none.
- A leading `'0'` forces a one-digit first part.

**Follow-ups:**
- "IPv6?" Eight groups of hex, up to 4 digits: the same shape with 8 levels and 4 choices; still a bounded tree.
- "Count only?" The same recursion with a counter, or a small DP over (position, parts placed).
- "Validate an address instead?" Split on `'.'` and apply the same part test.

**Common mistakes:**
- Rejecting `'0'` itself along with `'00'`.
- Using `int(t) > 255` without the leading-zero test: `'01'` converts to 1.
- Accepting four parts that do not consume the whole string.
- Not checking `len(t) == L`: a slice past the end is shorter and gets accepted as a part.
- Treating this as O(3^n): the depth is fixed at four.

### Q24 ⭐⭐ 🟡 Autocomplete with counts. `entries` is a list of 1 to 2000 pairs `[word, count]` (distinct lowercase words of length 1 to 20, count a positive integer) and `queries` is a list of 1 to 2000 non-empty lowercase prefixes. For each query return up to the 3 best words that start with the prefix, ordered by count descending and, for equal counts, by word ascending; fewer than 3 if fewer words match, an empty list if none. Build the trie once and store at every node the best 3 `(count, word)` pairs of the words below it (updated while inserting), so a query is O(L) plus 3 copies; compare with collecting every word under the prefix and sorting, whose cost grows with the size of the subtree. Say what happens to the stored lists when a count changes later (they must be updated along the whole path). In the answer include a dry run on the first example and a seeded random cross-check of your solution against filtering all words by `startswith` and sorting on small inputs. Example: entries=[['car', 5], ['cart', 9], ['care', 9], ['cat', 2], ['dog', 7]], queries=['ca', 'car', 'd', 'x', 'cat'] -> [['care', 'cart', 'car'], ['care', 'cart', 'car'], ['dog'], [], ['cat']]; entries=[['a', 1]], queries=['a', 'ab'] -> [['a'], []]; entries=[['ab', 3], ['ac', 3], ['ad', 3], ['ae', 3]], queries=['a'] -> [['ab', 'ac', 'ad']].
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened)

**Pattern:** Trie with a cached answer at every node: the best 3 `(count, word)` pairs below it. Pay a little on insert to make each query a walk down the prefix plus a copy.

**Say this first (1 line):** "Walk the prefix in O(L), then read the top 3 already stored at that node. Insert pushes each word's (count, word) onto every node of its path and keeps only the best 3 there."

**Brute force:** For each query, filter all words with `startswith(prefix)`, sort by `(-count, word)`, take 3. O(W * L) to filter per query (`W` words) plus the sort of the matches. A trie-only variant (walk to the prefix node, collect every word below it, sort) skips the filter but still touches the whole subtree, which for a short prefix is most of the dictionary.

**Optimal:**
- Node: children dict, optional count of a word ending here, and `top`: a list of at most 3 `(-count, word)` pairs.
- Insert `(word, count)`: walk or create nodes; at every node on the path (not the root: prefixes are non-empty) add `(-count, word)` to `top`, sort, keep 3. Storing `-count` makes the sort order exactly "count descending, then word ascending".
- Query `prefix`: walk; if a step is missing return `[]`; else return the words of `top`.
- Why 3 per node is enough: the best 3 words below a node are the best 3 among the best 3 of its children and the word ending at the node itself. So a node never needs more than the top 3 of each child.
- Count changes later: every node on the word's path holds a copy of the old count, so all of them must be refreshed. A RAISE is a simple merge. A LOWER is harder: the word may drop out of a node's list and a word that was not stored (the fourth best) must come back. Rebuild each list on the path bottom-up from the node's own count and its children's lists. The code does this, and the last demo shows it: lowering `ab` brings back `ae`, which no node stored for `'a'`.

**Complexity:** Query O(L) to walk + O(1) to copy 3 words (against O(subtree size * log) for collect-and-sort, or O(W * L) for the filter). Insert O(L * K log K) with `K = 3`: constant per node. Update O(L * (alphabet * K)) with the rebuild. Space: one node per distinct prefix (5435 nodes for 2000 random words in the run), each with a list of at most 3 pairs: O(total letters * K) in the worst case. Memory is the price of the fast query.

**Dry run:** `entries = car 5, cart 9, care 9, cat 2, dog 7`.
- Insert `car` (5): nodes `c`, `ca`, `car` each get `[(5,'car')]`.
- Insert `cart` (9): `c`, `ca`, `car`, `cart` get it; `car`'s list is now `[(9,'cart'),(5,'car')]`.
- Insert `care` (9): lists at `c`, `ca`, `car` become `[(9,'care'),(9,'cart'),(5,'car')]` (equal counts break by word, `'care' < 'cart'`).
- Insert `cat` (2): `c`'s list is full, `cat` is the 4th best and drops out; `ca` too; node `cat` holds `[(2,'cat')]`. Insert `dog`: node `d` holds `[(7,'dog')]`.
- Queries: `'ca'` reads the list at `ca`: `care, cart, car`. `'car'`: same list. `'d'`: `dog`. `'x'`: no child, `[]`. `'cat'`: `cat`. The code prints the stored lists.

**Code:**
```python
import random, string, heapq

random.seed(24)
K = 3

class AutoTrie:
    """Trie with, at every node, the best K (-count, word) pairs of the words at or below that node."""
    def __init__(self):
        self.root = {'c': {}, 'top': [], 'cnt': None}      # 'cnt' is the count if a word ends here
        self.nodes = 1
    def insert(self, word, count):
        nd = self.root
        path = [nd]
        for ch in word:
            if ch not in nd['c']:
                nd['c'][ch] = {'c': {}, 'top': [], 'cnt': None}; self.nodes += 1
            nd = nd['c'][ch]; path.append(nd)
        nd['cnt'] = count
        for p in path[1:]:                                  # update the whole path (the root list is never queried: prefixes are non-empty)
            p['top'] = sorted([e for e in p['top'] if e[1] != word] + [(-count, word)])[:K]
    def set_count(self, word, count):
        """Change a count later. Raising is a merge; LOWERING may need words that were not stored, so rebuild each list on the path from the children's lists."""
        nd = self.root; path = [nd]
        for ch in word:
            nd = nd['c'][ch]; path.append(nd)
        nd['cnt'] = count
        for p, w in zip(reversed(path[1:]), reversed(range(1, len(path)))):
            cand = [] if p['cnt'] is None else [(-p['cnt'], word[:w])]
            for child in p['c'].values(): cand += child['top']
            p['top'] = sorted(cand)[:K]
    def query(self, prefix):
        nd = self.root
        for ch in prefix:
            nd = nd['c'].get(ch)
            if nd is None: return []
        return [w for _, w in nd['top']]

def solve(entries, queries):
    t = AutoTrie()
    for w, c in entries: t.insert(w, c)
    return [t.query(p) for p in queries]

def brute(entries, queries):
    return [[w for c, w in sorted((-c, w) for w, c in entries if w.startswith(p))[:K]] for p in queries]

for ent, qs, exp in [([['car', 5], ['cart', 9], ['care', 9], ['cat', 2], ['dog', 7]], ['ca', 'car', 'd', 'x', 'cat'],
                       [['care', 'cart', 'car'], ['care', 'cart', 'car'], ['dog'], [], ['cat']]),
                     ([['a', 1]], ['a', 'ab'], [['a'], []]),
                     ([['ab', 3], ['ac', 3], ['ad', 3], ['ae', 3]], ['a'], [['ab', 'ac', 'ad']])]:
    got = solve(ent, qs)
    assert got == exp == brute(ent, qs)
    print('example', ent, qs, '->', got)

# what is stored along the path for example 1
t = AutoTrie()
for w, c in [['car', 5], ['cart', 9], ['care', 9], ['cat', 2], ['dog', 7]]: t.insert(w, c)
print('stored top-3 per node, example 1:')
for pre in ['c', 'ca', 'car', 'cat', 'care', 'cart', 'd']:
    nd = t.root
    for ch in pre: nd = nd['c'][ch]
    print(f'  {pre!r:7}: {[(-c, w) for c, w in nd["top"]]}')

# work comparison on a larger set: words visited by "collect everything under the prefix and sort" versus stored lists
rnd = random.Random(240)
words = set()
while len(words) < 2000: words.add(''.join(rnd.choice('abc') for _ in range(rnd.randint(1, 8))) if rnd.random() < .5 else ''.join(rnd.choice(string.ascii_lowercase) for _ in range(rnd.randint(1, 8))))
big = [[w, rnd.randint(1, 100)] for w in sorted(words)]
def subtree_size(trie, prefix):
    nd = trie.root
    for ch in prefix:
        nd = nd['c'].get(ch)
        if nd is None: return 0
    seen = 0; stack = [nd]
    while stack:
        x = stack.pop(); seen += x['cnt'] is not None; stack += x['c'].values()
    return seen
bt = AutoTrie()
for w, c in big: bt.insert(w, c)
print('2000 words; words below prefix (what the collect-and-sort baseline must examine) versus stored entries read by a query:')
for p in ['a', 'ab', 'abc', 'q', 'zz']:
    print(f'  {p!r:6}: words below = {subtree_size(bt, p):4d}   query reads at most {K} stored entries after {len(p)} steps')
print('trie nodes for the 2000 words:', bt.nodes)

# seeded random cross-check vs startswith + sort
for _ in range(300):
    n = random.randint(1, 25)
    ws = sorted({''.join(random.choice('abc') for _ in range(random.randint(1, 5))) for _ in range(n)})
    ent = [[w, random.randint(1, 6)] for w in ws]; random.shuffle(ent)
    qs = [''.join(random.choice('abc') for _ in range(random.randint(1, 4))) for _ in range(8)]
    assert solve(ent, qs) == brute(ent, qs), (ent, qs)
print('300 seeded random cases agree with the filter-and-sort baseline (ties by word ascending)')

# later count changes: up and down, rebuilt along the path
bad = 0
for _ in range(200):
    ws = sorted({''.join(random.choice('abc') for _ in range(random.randint(1, 5))) for _ in range(20)})
    cur = {w: random.randint(1, 6) for w in ws}
    tr = AutoTrie()
    for w, c in cur.items(): tr.insert(w, c)
    for _ in range(15):
        w = random.choice(ws); cur[w] = random.randint(1, 6); tr.set_count(w, cur[w])
        qs = [''.join(random.choice('abc') for _ in range(random.randint(1, 3))) for _ in range(5)]
        assert [tr.query(p) for p in qs] == brute(list(cur.items()), qs)
print('200 x 15 random count changes (up and down) keep every answer equal to the baseline')
# showing why only "merge" is not enough when a count goes down
tr = AutoTrie()
for w, c in [['ab', 9], ['ac', 5], ['ad', 4], ['ae', 3]]: tr.insert(w, c)
before = tr.query('a'); tr.set_count('ab', 1); after = tr.query('a')
print("top-3 of 'a' before:", before, " after lowering 'ab' to 1:", after, "(ae was not stored; it had to come back from the children)")
assert before == ['ab', 'ac', 'ad'] and after == ['ac', 'ad', 'ae']

# edge asserts
assert solve([['a', 1]], ['a', 'ab', 'b']) == [['a'], [], []]
assert solve([['z' * 20, 5]], ['z' * 20, 'z' * 19]) == [['z' * 20], ['z' * 20]]
assert solve([['ab', 3], ['ac', 3], ['ad', 3], ['ae', 3]], ['a']) == [['ab', 'ac', 'ad']]
print('edge asserts passed')
```

**Output (my run):**
```
example [['car', 5], ['cart', 9], ['care', 9], ['cat', 2], ['dog', 7]] ['ca', 'car', 'd', 'x', 'cat'] -> [['care', 'cart', 'car'], ['care', 'cart', 'car'], ['dog'], [], ['cat']]
example [['a', 1]] ['a', 'ab'] -> [['a'], []]
example [['ab', 3], ['ac', 3], ['ad', 3], ['ae', 3]] ['a'] -> [['ab', 'ac', 'ad']]
stored top-3 per node, example 1:
  'c'    : [(9, 'care'), (9, 'cart'), (5, 'car')]
  'ca'   : [(9, 'care'), (9, 'cart'), (5, 'car')]
  'car'  : [(9, 'care'), (9, 'cart'), (5, 'car')]
  'cat'  : [(2, 'cat')]
  'care' : [(9, 'care')]
  'cart' : [(9, 'cart')]
  'd'    : [(7, 'dog')]
2000 words; words below prefix (what the collect-and-sort baseline must examine) versus stored entries read by a query:
  'a'   : words below =  295   query reads at most 3 stored entries after 1 steps
  'ab'  : words below =   85   query reads at most 3 stored entries after 2 steps
  'abc' : words below =   23   query reads at most 3 stored entries after 3 steps
  'q'   : words below =   47   query reads at most 3 stored entries after 1 steps
  'zz'  : words below =    0   query reads at most 3 stored entries after 2 steps
trie nodes for the 2000 words: 5435
300 seeded random cases agree with the filter-and-sort baseline (ties by word ascending)
200 x 15 random count changes (up and down) keep every answer equal to the baseline
top-3 of 'a' before: ['ab', 'ac', 'ad']  after lowering 'ab' to 1: ['ac', 'ad', 'ae'] (ae was not stored; it had to come back from the children)
edge asserts passed
```

Reading the output:
- All three examples agree with the filter-and-sort oracle; the stored lists printed match the dry run.
- On 2000 random words, the baseline would examine 295 words under `'a'`, 85 under `'ab'`, and 47 under `'q'`; the trie query reads at most 3 stored entries after walking the prefix. (These counts are about work, not timings.)
- 300 seeded random cases (ties included, since counts are drawn from 1..6) agree with the baseline.
- 200 sequences of 15 random count changes, up and down, keep every query equal to the baseline, so the rebuild along the path is right.
- The lowering demo shows why a pure "merge" on the path is not enough.

**Edge cases:**
- Prefix not present: `[]`.
- Prefix equal to a whole word: that word competes with its extensions (`'car'` returns `care, cart, car`).
- Fewer than 3 matches: fewer than 3 returned.
- All counts equal: word order decides (`ab, ac, ad` out of four).
- Length-20 words: depth 20, no recursion used.

**Follow-ups:**
- "Large dictionary memory?" Store word ids (or indexes into a list) instead of strings in the per-node lists, or keep `K` small; a compressed (radix) trie reduces the node count.
- "Counts change often?" Updates cost more than reads here; if writes dominate, compute at query time with a heap over the subtree instead, or batch the rebuilds.
- "Why not a sorted list and `bisect`?" It gives the range of words with the prefix in O(log W) but not the top 3 by count in that range without scanning it (Part 3 Q36 compares those two for prefix queries).

**Common mistakes:**
- Sorting by `(count, word)` ascending: the order is wrong (reversed). Store `-count`.
- Storing only the best 3 at the leaf and forgetting the inner nodes.
- Updating only the leaf when a count changes, leaving stale copies on the path.
- Mutating the stored list when answering (return a copy of the words).
- Keeping every word at every node: that is one entry per word per prefix (about `W * L` entries) instead of at most 3 per node.

### Q25 ⭐⭐ 🔴 Sudoku solver. `board` is a list of 9 strings of 9 characters each: '1'..'9' for a given digit and '.' for an empty cell. The puzzle has exactly one solution. Return the solved board in the same format (list of 9 strings of digits). Fill empty cells by backtracking, keeping a bitmask per row, per column and per 3 x 3 box (`rows[r]`, `cols[c]`, `boxes[(r // 3) * 3 + c // 3]`), compute the candidates of a cell as the digits not set in the OR of its three masks, extract a candidate with `low = m & -m` and its digit with `low.bit_length() - 1`, and choose the empty cell with the fewest candidates first. Explain why the search is exponential in theory but fast on real puzzles, and what each of the three masks prunes. (Part 1 Q15 only validates a partly filled board; this question solves it.) The recursion depth equals the number of empty cells, at most 81. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a plain cell-by-cell solver without the heuristic, plus a validity check of the result on small inputs. Example: board=['.1....3..', '.586.3.24', '..92..5..', '.4.1...5.', '..6.24.17', '.8...94.2', '8.5...74.', '471...2..', '.....7..5'] -> ['214785369', '758693124', '639241578', '342178956', '596324817', '187569432', '865932741', '471856293', '923417685'].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with constraint propagation by bitmasks and a most-constrained-cell-first rule (fail-first). Three integers per row, column and box replace three scans.

**Say this first (1 line):** "One 9-bit mask per row, column and box records the digits used; a cell's candidates are the digits not set in the OR of its three masks; I always fill the empty cell with the fewest candidates, so dead ends show up early."

**Brute force:** Cell by cell in reading order, try `'1'..'9'`, check the row, column and box by scanning (about 27 comparisons per try), recurse, undo on failure. Correct, and exponential in theory. It can run for millions of nodes on a puzzle with few givens. Used as the oracle (it also counts solutions, to check that test puzzles are unique).

**Optimal:**
- Masks: digit `d` is bit `d` (bits 1..9, so `FULL = 0x3FE`). `rows[r]`, `cols[c]`, `boxes[(r // 3) * 3 + c // 3]` hold the digits already placed.
- Candidates of a cell: `~(rows[r] | cols[c] | boxes[b]) & FULL`. Python integers are unbounded and `~x` is `-x - 1`, a NEGATIVE number with infinitely many leading 1 bits (observed: `~m = -39` for `m = 0b100110`). So the `& FULL` mask is not optional: without it you would get candidates for bit 0 and for bits 10 and above, and `while m:` would never terminate on a negative number.
- Extract a candidate: `low = m & -m` isolates the lowest set bit (for positive `m`, `-m` is two's complement in Python's infinite-width view, so `m & -m` is exactly the lowest 1). The digit is `low.bit_length() - 1`. Clear it with `m ^= low`. Place and undo by `|= low` and `^= low`.
- Choose the empty cell with the fewest candidates (`m.bit_count()`; `bin(m).count('1')` on older Python; `int.bit_count` was added in 3.10, editor knowledge). Stop scanning at a cell with 0 or 1 candidates. Zero candidates means this branch is dead: return at once.
- What each mask prunes: the row mask removes digits already in that row, the column mask the same for the column, the box mask for the 3 x 3 box. A candidate must pass all three, so the OR is the set of forbidden digits.
- Why exponential in theory but fast in practice: Sudoku solving is NP-complete when generalised to `n^2 x n^2` boards, and a 9 x 9 board with few givens can still need many guesses. On real puzzles propagation (forced single candidates) plus fail-first leaves very few real choices: the example below needs 54 calls for 48 empty cells.

**Complexity:** Worst case exponential: up to 9 branches per empty cell, so O(9^k) for `k` empty cells (a loose bound; real puzzles are far smaller). Each call costs O(k) to scan for the best cell (k <= 81) and O(1) for the mask work per candidate. Space O(k) for the recursion (depth = empty cells, at most 81, far below the limit of 1000) and the masks.

**Dry run:** the first example has 48 empty cells. The code prints the first choices:
- Cell `(1, 0)` has exactly one candidate, 7: forced; place it.
- Then `(0, 0)` has candidates 2 and 6 (two options): try 2 first.
- Then `(0, 2)` has one candidate, 4; `(0, 5)` has 5 and 8; `(1, 4)` has 1 and 9; `(1, 6)` has only 9.
- Whenever some cell has no candidate the search backs out immediately (the `bk == 0` return).
- It finishes after 54 calls for 48 empty cells: a call is made per placement plus one at the end, so at most a few calls went into undone guesses. Reading order with the same masks needs 522 calls on the same board.

**Code:**
```python
import random

random.seed(25)
FULL = 0x3FE            # bits 1..9 set: digit d is bit d. Python's ~ gives a NEGATIVE number, so we always mask with FULL.

def digits_of(m):
    return [i for i in range(1, 10) if m >> i & 1]

def solve_mrv(board, trace=None):
    """Bitmask backtracking, most-constrained empty cell first. Returns (solution rows, nodes)."""
    g = [[0 if ch == '.' else int(ch) for ch in row] for row in board]
    rows = [0] * 9; cols = [0] * 9; boxes = [0] * 9; empties = []
    for r in range(9):
        for c in range(9):
            if g[r][c]:
                b = 1 << g[r][c]; rows[r] |= b; cols[c] |= b; boxes[r // 3 * 3 + c // 3] |= b
            else: empties.append((r, c))
    nodes = 0
    def solve():
        nonlocal nodes
        nodes += 1
        if not empties: return True
        best = -1; bm = 0; bk = 10
        for idx, (r, c) in enumerate(empties):
            m = ~(rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3]) & FULL        # candidates of this cell
            k = m.bit_count()
            if k < bk:
                best, bm, bk = idx, m, k
                if k <= 1: break                                                 # a forced cell (or a dead end) cannot be beaten
        if bk == 0: return False                                                 # some cell has no candidate: prune
        empties[best], empties[-1] = empties[-1], empties[best]
        r, c = empties.pop(); bi = r // 3 * 3 + c // 3
        if trace is not None and len(trace) < 6: trace.append(((r, c), digits_of(bm)))
        while bm:
            low = bm & -bm; bm ^= low; v = low.bit_length() - 1                   # lowest candidate bit, then its digit
            g[r][c] = v; rows[r] |= low; cols[c] |= low; boxes[bi] |= low
            if solve(): return True
            rows[r] ^= low; cols[c] ^= low; boxes[bi] ^= low; g[r][c] = 0
        empties.append((r, c)); empties[best], empties[-1] = empties[-1], empties[best]
        return False
    assert solve(), 'no solution'
    return [''.join(map(str, row)) for row in g], nodes

def solve_fixed_order(board, cap=None):
    """Same masks, same candidate extraction, but cells in reading order (no heuristic). Returns (rows or None, nodes)."""
    g = [[0 if ch == '.' else int(ch) for ch in row] for row in board]
    rows = [0] * 9; cols = [0] * 9; boxes = [0] * 9; empties = []
    for r in range(9):
        for c in range(9):
            if g[r][c]:
                b = 1 << g[r][c]; rows[r] |= b; cols[c] |= b; boxes[r // 3 * 3 + c // 3] |= b
            else: empties.append((r, c))
    nodes = 0
    def go(i):
        nonlocal nodes
        nodes += 1
        if cap and nodes > cap: raise OverflowError
        if i == len(empties): return True
        r, c = empties[i]; bi = r // 3 * 3 + c // 3
        m = ~(rows[r] | cols[c] | boxes[bi]) & FULL
        while m:
            low = m & -m; m ^= low; v = low.bit_length() - 1
            g[r][c] = v; rows[r] |= low; cols[c] |= low; boxes[bi] |= low
            if go(i + 1): return True
            rows[r] ^= low; cols[c] ^= low; boxes[bi] ^= low
        return False
    try: ok = go(0)
    except OverflowError: return None, nodes
    return ([''.join(map(str, row)) for row in g] if ok else None), nodes

def plain(board, limit=1):
    """Oracle: cell by cell, tries '1'..'9', checks row, column and box by scanning; counts solutions up to `limit`."""
    g = [list(r) for r in board]; found = []
    def ok(r, c, ch):
        if any(g[r][k] == ch or g[k][c] == ch for k in range(9)): return False
        br, bc = r // 3 * 3, c // 3 * 3
        return all(g[br + i][bc + j] != ch for i in range(3) for j in range(3))
    def go(pos):
        if len(found) >= limit: return
        while pos < 81 and g[pos // 9][pos % 9] != '.': pos += 1
        if pos == 81: found.append([''.join(r) for r in g]); return
        r, c = divmod(pos, 9)
        for ch in '123456789':
            if ok(r, c, ch): g[r][c] = ch; go(pos + 1); g[r][c] = '.'
    go(0); return found

def valid(rows):
    if len(rows) != 9 or any(len(r) != 9 for r in rows): return False
    want = set('123456789')
    for i in range(9):
        if set(rows[i]) != want or set(rows[j][i] for j in range(9)) != want: return False
        if {rows[3 * (i // 3) + a][3 * (i % 3) + b] for a in range(3) for b in range(3)} != want: return False
    return True

EX = ['.1....3..', '.586.3.24', '..92..5..', '.4.1...5.', '..6.24.17', '.8...94.2', '8.5...74.', '471...2..', '.....7..5']
EXP = ['214785369', '758693124', '639241578', '342178956', '596324817', '187569432', '865932741', '471856293', '923417685']
trace = []
sol, n_mrv = solve_mrv(EX, trace)
assert sol == EXP == plain(EX, 2)[0] and len(plain(EX, 2)) == 1 and valid(sol)
print('example solved:', sol)
print('empty cells:', sum(r.count('.') for r in EX), '| search calls with most-constrained cell first:', n_mrv)
for (rc, cands) in trace: print(f'  step: choose cell {rc} with candidates {cands}')

# the Python negative-integer point, as observed on Python 3.13
m = 0b0000100110
print('~m =', ~m, '(negative); ~m & FULL =', bin(~m & FULL), '-> digits', digits_of(~m & FULL))
x = 0b101000
print('x & -x =', bin(x & -x), '(lowest set bit);  (x & -x).bit_length() - 1 =', (x & -x).bit_length() - 1)
print('digit d as a bit: 1 << 7 =', bin(1 << 7), '; row mask with 5 and 9 set =', bin((1 << 5) | (1 << 9)))

# search cost of the heuristic: same masks, reading-order cells
sol2, n_fixed = solve_fixed_order(EX)
assert sol2 == EXP
print('same example, reading-order cells with the same masks:', n_fixed, 'calls (against', n_mrv, 'with the heuristic)')

# a puzzle with 17 givens and an empty first row: hard for reading order
HARD = ['.........', '.....3.85', '..1.2....', '...5.7...', '..4...1..', '.9.......', '5......73', '..2.1....', '....4...9']
h_sol, n_h = solve_mrv(HARD)
assert valid(h_sol) and all(a == '.' or a == b for ra, rb in zip(HARD, h_sol) for a, b in zip(ra, rb))
r_fixed, n_f = solve_fixed_order(HARD, cap=3_000_000)
print('hard puzzle (17 givens):', 'heuristic', n_h, 'calls;', ('reading order ' + str(n_f) + ' calls') if r_fixed else 'reading order gave up after ' + str(n_f) + ' calls (cap 3,000,000)')
assert r_fixed is None or r_fixed == h_sol

# seeded random puzzles with a unique solution; compare with the plain oracle and check validity
def random_full(rnd):
    g = [['.'] * 9 for _ in range(9)]
    def ok(r, c, ch):
        if any(g[r][k] == ch or g[k][c] == ch for k in range(9)): return False
        br, bc = r // 3 * 3, c // 3 * 3
        return all(g[br + i][bc + j] != ch for i in range(3) for j in range(3))
    def go(pos):
        if pos == 81: return True
        r, c = divmod(pos, 9); ds = list('123456789'); rnd.shuffle(ds)
        for ch in ds:
            if ok(r, c, ch):
                g[r][c] = ch
                if go(pos + 1): return True
                g[r][c] = '.'
        return False
    go(0); return [''.join(r) for r in g]
def make_puzzle(rnd, remove):
    full = random_full(rnd); g = [list(r) for r in full]
    cells = [(r, c) for r in range(9) for c in range(9)]; rnd.shuffle(cells); removed = 0
    for r, c in cells:
        if removed >= remove: break
        keep = g[r][c]; g[r][c] = '.'
        if len(plain([''.join(x) for x in g], 2)) == 1: removed += 1
        else: g[r][c] = keep
    return [''.join(x) for x in g], full
rnd = random.Random(250)
nm = []; nf = []
for i in range(40):
    puz, full = make_puzzle(rnd, rnd.randint(30, 50))
    s1, a = solve_mrv(puz); assert s1 == full == plain(puz, 1)[0] and valid(s1)
    assert all(p == '.' or p == q for rp, rq in zip(puz, s1) for p, q in zip(rp, rq))
    s2, b = solve_fixed_order(puz); assert s2 == full
    nm.append(a); nf.append(b)
print('40 seeded random puzzles with a unique solution: all agree with the plain solver and are valid grids')
print('  calls with heuristic: total', sum(nm), 'max', max(nm), '| reading order: total', sum(nf), 'max', max(nf))

# edge asserts: an already solved board, one empty cell
assert solve_mrv(EXP)[0] == EXP
one = [EXP[0][:4] + '.' + EXP[0][5:]] + EXP[1:]
assert solve_mrv(one)[0] == EXP
print('edge asserts passed (solved board; one empty cell); recursion depth = empty cells <= 81')
```

**Output (my run):**
```
example solved: ['214785369', '758693124', '639241578', '342178956', '596324817', '187569432', '865932741', '471856293', '923417685']
empty cells: 48 | search calls with most-constrained cell first: 54
  step: choose cell (1, 0) with candidates [7]
  step: choose cell (0, 0) with candidates [2, 6]
  step: choose cell (0, 2) with candidates [4]
  step: choose cell (0, 5) with candidates [5, 8]
  step: choose cell (1, 4) with candidates [1, 9]
  step: choose cell (1, 6) with candidates [9]
~m = -39 (negative); ~m & FULL = 0b1111011000 -> digits [3, 4, 6, 7, 8, 9]
x & -x = 0b1000 (lowest set bit);  (x & -x).bit_length() - 1 = 3
digit d as a bit: 1 << 7 = 0b10000000 ; row mask with 5 and 9 set = 0b1000100000
same example, reading-order cells with the same masks: 522 calls (against 54 with the heuristic)
hard puzzle (17 givens): heuristic 17918 calls; reading order gave up after 3000001 calls (cap 3,000,000)
40 seeded random puzzles with a unique solution: all agree with the plain solver and are valid grids
  calls with heuristic: total 1629 max 67 | reading order: total 18763 max 9383
edge asserts passed (solved board; one empty cell); recursion depth = empty cells <= 81
```

Reading the output:
- The solved board equals the expected one, and the plain solver finds exactly one solution for it.
- The mask demo shows `~m` negative and the `& FULL` result giving digits 3, 4, 6, 7, 8, 9 for a row that has 1, 2 and 5 placed. `x & -x` isolates bit 3 and `bit_length() - 1` turns it into 3. Observed on Python 3.13.
- Node counts: 54 calls with the heuristic against 522 with the same masks in reading order. On a 17-given puzzle with an empty first row the heuristic needs 17,918 calls while reading order did not finish within a cap of 3,000,000 calls (a limit of the demo, not a proof it could not finish).
- 40 seeded random puzzles (each with a unique solution, checked by the plain solver) give valid grids that keep all the givens and match the oracle. Total calls: 1629 with the heuristic (max 67) against 18,763 in reading order (max 9,383).

**Edge cases:**
- Already solved board: no empties, returns at once.
- One empty cell: forced.
- A puzzle with no solution: the search ends with `False` (the prompt guarantees exactly one solution, so the code asserts).
- Several solutions: returns the first found (the prompt rules this out).
- Contradictory givens: some mask makes a cell's candidates empty and the search fails at the root.

**Follow-ups:**
- "Validity only?" Part 1 Q15 validates a partly filled board with the same row, column and box idea.
- "Count solutions or prove uniqueness?" Do not return at the first solution; stop at two.
- "Faster?" Add naked and hidden singles propagation, or exact cover with dancing links. The idea here is already the dominant gain.

**Common mistakes:**
- Using `~mask` without `& FULL`: negative numbers and bit 0 give phantom candidates and the loop does not end.
- Box index `r // 3 + c // 3` instead of `(r // 3) * 3 + c // 3`.
- Forgetting to undo all three masks and the grid cell on backtrack.
- Mixing digit `d` and bit `d - 1` conventions between placing and reading.
- Picking the first empty cell (no fail-first rule): same answer, far more calls.

### Q26 ⭐⭐ 🔴 Maximum XOR of two numbers (binary trie). `nums` has 2 <= len <= 3*10^4 integers in 0..2^31 - 1. Return the maximum of `nums[i] ^ nums[j]` over pairs i < j. Build a binary trie of the 31-bit patterns (bit 30 first), and for each number walk the trie choosing, at each bit, the child with the OPPOSITE bit when it exists (greedy: a higher bit outweighs all lower bits together). Insert each number after querying so that i < j holds. State the cost O(31 * n) against O(n^2) for all pairs, and the memory of the trie (up to 31 * n nodes). A hash-set-of-prefixes approach is the follow-up. Note that Python integers are not capped at 31 bits, so the bit width is a constraint of this question, not of the language. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an O(n^2) loop over all pairs on small inputs. Example: nums=[12, 5, 9, 21, 7] -> 28; nums=[0, 0] -> 0; nums=[7, 7, 7] -> 0; nums=[2147483647, 0] -> 2147483647; nums=[8, 1] -> 9.
**Asked at:** A Teamblind discussion of a bit-based trie question, plus the techinterview.org trie posts (search snippets only, not opened)

**Pattern:** Binary trie over fixed-width bit patterns, with a greedy walk that prefers the opposite bit at each level.

**Say this first (1 line):** "A higher bit outweighs all the lower bits together, so for each number I walk the trie from bit 30 down and take the child with the opposite bit whenever it exists. That is the best partner among the stored numbers, found in 31 steps."

**Brute force:** XOR every pair `i < j` and take the maximum: O(n^2). At `n = 30000` that is 449,985,000 pairs, far too slow in Python. It is the oracle for small `n`.

**Optimal:**
- The trie has one level per bit, bit 30 first (31 levels, matching values in `0..2^31 - 1`). A number is a path of 31 edges, each labelled 0 or 1. The code stores the two children in parallel lists `c0`, `c1` (index 0 means missing; node 0 is the root).
- Query for `x`: at bit `b`, if the child for `1 - bit_b(x)` exists, go there and set bit `b` of the result; otherwise follow the child for `bit_b(x)`, which must exist (every stored number is a full-length path), and the result bit stays 0.
- Why greedy is right: the XOR bit at position `b` is worth `2^b`, and `2^b` is greater than the sum of all lower bits `2^b - 1`. So whenever a partner can give a 1 at bit `b`, every partner that gives 0 there is worse, whatever happens below.
- Order: for each number, query first, then insert, so only numbers earlier in the list are partners (`i < j`). (Inserting first would also give the correct answer: the extra self-pair gives 0, which never beats a real pair; the code checks this.)
- The bit width: Python integers are not capped at 31 bits. The width 31 is a rule of this question. A negative input would read sign bits forever (`(-1 >> 30) & 1 == 1`, and the same for every higher bit in Python 3.13), so the walk would be meaningless; the constraints rule negatives out. If they were allowed you would have to mask to a width first (`x & 0xFFFFFFFF`).
- Follow-up approach, a hash set of prefixes: build the answer bit by bit from the top; at bit `b` the candidate answer is `ans | 1 << b`; collect the set of all `x >> b`; the candidate is possible if some `p` in the set has `p ^ candidate_prefix` also in the set. 31 passes of O(n), no trie memory. The code implements it and checks it.

**Complexity:** Time O(31 * n) = O(n * B) for `B = 31` bits: one insert and one query per number, 31 steps each. Against O(n^2) for all pairs. Space: up to `31 * n + 1` nodes (930,001 at `n = 30000`; the random test built 516,727 nodes because the top bits are shared). Each node is two list slots in this encoding. The prefix-set approach uses O(n) space.

**Dry run:** `nums = [12, 5, 9, 21, 7]`, 5-bit view so the paths fit on a line (the real code uses 31 bits; the leading zeros do not change the answer).
- Insert 12 (`01100`).
- Query 5 (`00101`) against `{12}`: the only partner is 12, xor 9. Query 9 (`01001`) against `{12, 5}`: at bit 3 take the child with a 0 (that is 5), and at bit 2 take the child with a 1 (5 again), so the xor is `01100` = 12, partner 5.
- Query 21 (`10101`) against `{12, 5, 9}`: bit 4: x has 1, opposite child 0 exists (all three stored numbers have 0 at bit 4), take it; bit 3: x has 0, take 1 (12 and 9 have it); bit 2: x has 1, take 0 (only 9 remains with 0 here); bit 1 and bit 0: no choice. Partner 9, xor `11100` = 28.
- Query 7 (`00111`) against `{12, 5, 9, 21}`: best is 21, xor 18.
- Results 9, 12, 28, 18. Maximum 28.

**Code:**
```python
import random, itertools, time

random.seed(26)
BITS = 31                                   # the question's width: values are in 0..2^31 - 1, bit 30 is the top bit

def max_xor(nums, bits=BITS, stats=None):
    """Binary trie in two parallel lists (child 0, child 1). Query each number, THEN insert it, so only i < j pairs are seen."""
    c0 = [0]; c1 = [0]                      # node 0 is the root; child index 0 means 'missing'
    children = (c0, c1)
    best = 0
    def insert(x):
        nd = 0
        for b in range(bits - 1, -1, -1):
            bit = x >> b & 1
            nxt = children[bit][nd]
            if not nxt:
                c0.append(0); c1.append(0); nxt = len(c0) - 1; children[bit][nd] = nxt
            nd = nxt
    def query(x):
        nd = 0; got = 0
        for b in range(bits - 1, -1, -1):
            bit = x >> b & 1
            want = children[bit ^ 1][nd]    # the child with the OPPOSITE bit
            if want: got |= 1 << b; nd = want
            else: nd = children[bit][nd]    # forced to follow the same bit (it must exist: the trie is a union of full paths)
        return got
    insert(nums[0])
    for x in nums[1:]:
        best = max(best, query(x)); insert(x)
    if stats is not None: stats['nodes'] = len(c0)
    return best

def prefix_set(nums, bits=BITS):
    """Follow-up: hash set of prefixes. Grow the answer bit by bit; keep a bit if two prefixes XOR to the candidate."""
    ans = 0
    for b in range(bits - 1, -1, -1):
        pref = {x >> b for x in nums}
        cand = (ans >> b) | 1
        if any(p ^ cand in pref for p in pref): ans |= 1 << b
    return ans

def brute(nums): return max(a ^ b for a, b in itertools.combinations(nums, 2))

for nums, exp in [([12, 5, 9, 21, 7], 28), ([0, 0], 0), ([7, 7, 7], 0), ([2147483647, 0], 2147483647), ([8, 1], 9)]:
    a, b, c = max_xor(nums), brute(nums), prefix_set(nums)
    assert a == b == c == exp, nums
    print('example', nums, '->', a)

# the greedy walk for 21 against {12, 5, 9} using 5 bits so the path fits on a line
def show_walk(x, stored, bits=5):
    print(f'query {x} = {x:0{bits}b}, stored {stored} = {[format(y, "0%db" % bits) for y in stored]}')
    path = 0; got = 0
    for b in range(bits - 1, -1, -1):
        bit = x >> b & 1
        have = {y >> b for y in stored if (y >> (b + 1)) == path}        # next-bit prefixes present below the current node
        want = path << 1 | (bit ^ 1)
        if want in have: got |= 1 << b; path = want; print(f'  bit {b}: x has {bit}, opposite child exists -> take {bit ^ 1}, xor bit = 1')
        else: path = path << 1 | bit; print(f'  bit {b}: x has {bit}, opposite child missing -> take {bit}, xor bit = 0')
    print('  xor =', got, f'= {got:0{bits}b}, partner = {path}')
    return got
show_walk(5, [12], 5); show_walk(9, [12, 5], 5)
g = show_walk(21, [12, 5, 9], 5); assert g == 28
g2 = show_walk(7, [12, 5, 9, 21], 5); assert max(9, 12, 28, 18) == 28; print('results of the four queries: 9, 12, 28, 18 -> maximum 28')

# trie size: nodes <= 31 * n + 1
st = {}; nums = [random.randrange(1 << 31) for _ in range(30000)]
r = max_xor(nums, stats=st)
print('30000 random 31-bit numbers: trie nodes', st['nodes'], '<= bound 31 * 30000 + 1 =', 31 * 30000 + 1)
assert st['nodes'] <= 31 * 30000 + 1
st2 = {}; max_xor(list(range(1000)), stats=st2); print('1000 consecutive numbers 0..999: nodes', st2['nodes'], '(shared prefixes: far fewer than 31000)')
t0 = time.time(); max_xor(nums); t1 = time.time() - t0
t0 = time.time(); r2 = prefix_set(nums); t2 = time.time() - t0
assert r == r2
print(f'sandbox timing only: trie {t1:.2f} s, prefix-set {t2:.2f} s for n = 30000 (not a proof of big-O)')

# n^2 for n = 30000 would be about 4.5 * 10^8 pair XORs: not run
print('pairs at the maximum size:', 30000 * 29999 // 2)

# claim: inserting BEFORE querying would also be right here, because the self-pair x ^ x = 0 never beats a real pair
def insert_first(nums):
    return max(x ^ y for x in nums for y in nums)           # includes i == j pairs
for _ in range(300):
    nums = [random.randrange(64) for _ in range(random.randint(2, 8))]
    assert max_xor(nums) == brute(nums) == insert_first(nums)
print('300 random lists: the maximum over i <= j equals the maximum over i < j (the self-pair only adds 0)')

# negative numbers are outside the constraints; show what Python does so nobody 'fixes' it with a 31-bit loop
print('Python 3.13: (-1 >> 30) & 1 =', (-1 >> 30) & 1, ' (-1 >> 31) & 1 =', (-1 >> 31) & 1, ' -> a negative input reads sign bits forever; the 31-bit width is the question\'s rule, not the language')
print('Python ints are not capped: (2**31 - 1) ^ 0 =', (2**31 - 1) ^ 0, ', 2**40 ^ 1 =', 2**40 ^ 1)

# seeded random cross-check
for _ in range(400):
    n = random.randint(2, 12); hi = random.choice([2, 8, 100, 2 ** 31])
    nums = [random.randrange(hi) for _ in range(n)]
    assert max_xor(nums) == brute(nums) == prefix_set(nums), nums
print('400 seeded random cases agree (trie, prefix-set, O(n^2))')

# edge asserts
assert max_xor([7, 7]) == 0 and max_xor([0, 2147483647]) == 2147483647 and max_xor([5, 5, 5, 5]) == 0
assert max_xor([1, 2]) == 3 and max_xor([2 ** 30, 2 ** 30 - 1]) == 2 ** 31 - 1
print('edge asserts passed')
```

**Output (my run):**
```
example [12, 5, 9, 21, 7] -> 28
example [0, 0] -> 0
example [7, 7, 7] -> 0
example [2147483647, 0] -> 2147483647
example [8, 1] -> 9
query 5 = 00101, stored [12] = ['01100']
  bit 4: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 3: x has 0, opposite child exists -> take 1, xor bit = 1
  bit 2: x has 1, opposite child missing -> take 1, xor bit = 0
  bit 1: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 0: x has 1, opposite child exists -> take 0, xor bit = 1
  xor = 9 = 01001, partner = 12
query 9 = 01001, stored [12, 5] = ['01100', '00101']
  bit 4: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 3: x has 1, opposite child exists -> take 0, xor bit = 1
  bit 2: x has 0, opposite child exists -> take 1, xor bit = 1
  bit 1: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 0: x has 1, opposite child missing -> take 1, xor bit = 0
  xor = 12 = 01100, partner = 5
query 21 = 10101, stored [12, 5, 9] = ['01100', '00101', '01001']
  bit 4: x has 1, opposite child exists -> take 0, xor bit = 1
  bit 3: x has 0, opposite child exists -> take 1, xor bit = 1
  bit 2: x has 1, opposite child exists -> take 0, xor bit = 1
  bit 1: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 0: x has 1, opposite child missing -> take 1, xor bit = 0
  xor = 28 = 11100, partner = 9
query 7 = 00111, stored [12, 5, 9, 21] = ['01100', '00101', '01001', '10101']
  bit 4: x has 0, opposite child exists -> take 1, xor bit = 1
  bit 3: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 2: x has 1, opposite child missing -> take 1, xor bit = 0
  bit 1: x has 1, opposite child exists -> take 0, xor bit = 1
  bit 0: x has 1, opposite child missing -> take 1, xor bit = 0
  xor = 18 = 10010, partner = 21
results of the four queries: 9, 12, 28, 18 -> maximum 28
30000 random 31-bit numbers: trie nodes 516727 <= bound 31 * 30000 + 1 = 930001
1000 consecutive numbers 0..999: nodes 2022 (shared prefixes: far fewer than 31000)
sandbox timing only: trie 0.33 s, prefix-set 0.07 s for n = 30000 (not a proof of big-O)
pairs at the maximum size: 449985000
300 random lists: the maximum over i <= j equals the maximum over i < j (the self-pair only adds 0)
Python 3.13: (-1 >> 30) & 1 = 1  (-1 >> 31) & 1 = 1  -> a negative input reads sign bits forever; the 31-bit width is the question's rule, not the language
Python ints are not capped: (2**31 - 1) ^ 0 = 2147483647 , 2**40 ^ 1 = 1099511627777
400 seeded random cases agree (trie, prefix-set, O(n^2))
edge asserts passed
```

Reading the output:
- All five examples agree across the trie, the prefix-set method and the O(n^2) loop. Note `[7, 7, 7]` gives 0: every pair is equal.
- The printed walks follow the dry run bit by bit; the last walk (`21`) shows three consecutive opposite-bit takes giving `11100`.
- Node counts: 516,727 nodes for 30,000 random 31-bit numbers, under the bound of 930,001. For the numbers 0..999 only 2,022 nodes: shared prefixes cost nothing.
- Timings (sandbox only): the trie takes a fraction of a second for `n = 30000`, the prefix-set method is faster in Python because it uses sets and no per-bit node walking. Not a proof of big-O.
- 400 seeded random lists (value ranges 2, 8, 100 and 2^31) agree, and 300 more confirm that the `i <= j` maximum equals the `i < j` maximum.

**Edge cases:**
- Two numbers: one query.
- All equal (`[7,7,7]`, `[0,0]`): answer 0.
- Largest value with 0: `2^31 - 1`.
- Two numbers differing at the top bit only (`2^30` and `2^30 - 1`): all 31 bits set.
- Duplicates inside a larger list: they share the whole path, no extra nodes.

**Follow-ups:**
- "Memory?" Use the prefix-set method, or compress the trie. Or a sorted array with two pointers on the top bit and recursion on groups.
- "Maximum XOR of a number with a subarray XOR?" Combine with prefix XORs (Part 1 Q36 uses prefix XORs for counting).
- "Queries with a limit (XOR with `x` while the partner is at most `m`)?" Offline: sort queries by `m`, insert numbers up to `m`, then query.

**Common mistakes:**
- Starting at bit 31 or at 32: extra levels of zeros, harmless but wasteful; starting at 29 loses the top bit.
- Following the SAME bit by default, which finds the minimum XOR instead of the maximum.
- Taking `bit ^ 1` without checking the child exists (`None` or index 0 error).
- Using the same walk on negative numbers: infinite sign bits (see the output); mask first or rule them out.
- Rebuilding the trie per query.

### Q27 ⭐ 🟡 Map sum pairs. Implement a key-value store over lowercase string keys. `ops` is a list (1 <= len <= 5000) of `['insert', key, val]` (set `key` to the integer `val`, 0 <= val <= 1000, replacing any earlier value of that key, key length 1 to 20) or `['sum', prefix]` (the sum of the values of all keys that currently start with the non-empty `prefix`; 0 if none). Return one entry per operation: `null` (None) for insert and the sum for sum. Keep a running sum at every trie node and, on insert, add `new - old` along the whole path (this is why a replaced key does not double count); compare with scanning every key for every `sum`. State the cost per operation in terms of the key length. The trie itself is Q3. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a plain dict scanned with `startswith` on small inputs. Example: ops=[['insert', 'apple', 3], ['sum', 'ap'], ['insert', 'app', 2], ['sum', 'ap'], ['insert', 'apple', 5], ['sum', 'app'], ['sum', 'b']] -> [null, 3, null, 5, null, 7, 0]; ops=[['sum', 'a']] -> [0]; ops=[['insert', 'a', 0], ['sum', 'a'], ['insert', 'a', 7], ['sum', 'a']] -> [null, 0, null, 7].
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened)

**Pattern:** Trie with an aggregate at every node (a running sum of the values below it), kept right on updates by adding the difference `new - old`. The plain trie is Q3; the new idea is the aggregate.

**Say this first (1 line):** "Each node stores the sum of all values under that prefix. Insert walks the key and adds `new - old` at every node, so replacing a key does not double count; sum walks the prefix and reads one number."

**Brute force:** Keep a dict `key -> value`; for each `sum(prefix)`, scan every key with `startswith(prefix)` and add the values. Insert is O(1), but each sum costs O(K * L) for `K` live keys of length up to `L`, so a few thousand sums over a few thousand keys is millions of comparisons. Used as the oracle.

**Optimal:**
- Keep a plain dict `vals` (key to current value) and a trie whose nodes (dicts of children) carry a `'#'` sum.
- `insert(key, val)`: `delta = val - vals.get(key, 0)`; set `vals[key] = val`; walk the key and add `delta` to the `'#'` of every node on the path (every proper prefix and the whole key). A new key has old value 0, so `delta = val`. A repeated key adds only the change.
- `sum(prefix)`: walk; a missing child gives 0; otherwise return the node's `'#'`.
- Why it is right: node `n` for prefix `p` always holds the sum of `vals[k]` over keys with prefix `p`; an insert changes exactly one key's value by `delta`, and exactly the nodes of the prefixes of that key include that key.
- Value 0 and no-op replacements are fine: a key with value 0 adds 0, and `delta = 0` changes nothing.

**Complexity:** Each insert and each sum is O(L), the key (or prefix) length, independent of the number of keys: at most 20 steps here, 5000 operations at most. A scan costs O(K * L) per sum. Space: one node per distinct prefix, at most the total letters of the distinct keys (20 * 5000 = 100,000 nodes worst case), plus the `vals` dict.

**Dry run:** example 1 (the code prints the node sums after each insert).
- `insert apple 3`: `a`, `ap`, `app`, `appl`, `apple` all become 3. `sum ap` = 3.
- `insert app 2` (new key, delta 2): `a`, `ap`, `app` become 5; `appl` and `apple` stay 3. `sum ap` = 5.
- `insert apple 5` (old value 3, delta +2, not +5): `a`, `ap`, `app` become 7; `appl`, `apple` become 5. `sum app` = 7. `sum b`: no child `b`, so 0.
- Outputs: `[null, 3, null, 5, null, 7, 0]`. The demo of the bug (adding `val` instead of the delta) gives 10 for `sum app`, which counts `apple` as 3 + 5.

**Code:**
```python
import random

random.seed(27)

class MapSum:
    """Trie where every node keeps the sum of the values of all keys at or below it."""
    def __init__(self):
        self.root = {}            # node: dict of child letter -> node, plus the key '#' holding the running sum
        self.vals = {}            # key -> current value (needed to compute new - old)
        self.steps = 0            # trie steps taken, to compare with a scan
    def insert(self, key, val):
        delta = val - self.vals.get(key, 0)           # replacing a key adds only the DIFFERENCE
        self.vals[key] = val
        nd = self.root
        for ch in key:
            nd = nd.setdefault(ch, {}); self.steps += 1
            nd['#'] = nd.get('#', 0) + delta
    def sum(self, prefix):
        nd = self.root
        for ch in prefix:
            nd = nd.get(ch); self.steps += 1
            if nd is None: return 0
        return nd['#']

def solve(ops):
    m = MapSum(); res = []
    for op in ops:
        if op[0] == 'insert': m.insert(op[1], op[2]); res.append(None)
        else: res.append(m.sum(op[1]))
    return res

def brute(ops):
    d = {}; res = []
    for op in ops:
        if op[0] == 'insert': d[op[1]] = op[2]; res.append(None)
        else: res.append(sum(v for k, v in d.items() if k.startswith(op[1])))
    return res

def wrong_add_not_delta(ops):
    """The tempting bug: add val instead of new - old, so a replaced key counts twice."""
    m = MapSum(); res = []
    for op in ops:
        if op[0] == 'insert':
            nd = m.root
            for ch in op[1]:
                nd = nd.setdefault(ch, {}); nd['#'] = nd.get('#', 0) + op[2]
            res.append(None)
        else: res.append(m.sum(op[1]))
    return res

N = None
for ops, exp in [([['insert', 'apple', 3], ['sum', 'ap'], ['insert', 'app', 2], ['sum', 'ap'], ['insert', 'apple', 5], ['sum', 'app'], ['sum', 'b']], [N, 3, N, 5, N, 7, 0]),
                 ([['sum', 'a']], [0]),
                 ([['insert', 'a', 0], ['sum', 'a'], ['insert', 'a', 7], ['sum', 'a']], [N, 0, N, 7])]:
    got = solve(ops)
    assert got == exp == brute(ops)
    print('example ->', got)

# trace of example 1: node sums after each insert
m = MapSum()
def snap(label):
    parts = []
    for pre in ['a', 'ap', 'app', 'appl', 'apple']:
        nd = m.root
        for ch in pre: nd = nd[ch]
        parts.append(f'{pre}={nd["#"]}')
    print(f'  after {label}: ' + ', '.join(parts))
m.insert('apple', 3); snap("insert apple 3")
m.insert('app', 2); snap("insert app 2")
m.insert('apple', 5); snap("insert apple 5 (delta +2, not +5)")
print('  sum(ap) =', m.sum('ap'), ' sum(app) =', m.sum('app'), ' sum(b) =', m.sum('b'))
ops1 = [['insert', 'apple', 3], ['sum', 'ap'], ['insert', 'app', 2], ['sum', 'ap'], ['insert', 'apple', 5], ['sum', 'app'], ['sum', 'b']]
print('the add-val-not-delta bug on example 1 gives', wrong_add_not_delta(ops1), '(expected 3, 5, 7, 0 at the sum positions)')
assert wrong_add_not_delta(ops1) != solve(ops1)

# cost: trie steps vs keys scanned by the baseline
rnd = random.Random(270)
keys = [''.join(rnd.choice('abcd') for _ in range(rnd.randint(1, 12))) for _ in range(1500)]
ops = []
for i in range(5000):
    if rnd.random() < .5: ops.append(['insert', rnd.choice(keys), rnd.randint(0, 1000)])
    else: ops.append(['sum', rnd.choice(keys)[:rnd.randint(1, 6)]])
mm = MapSum(); got = []
scanned = 0; live = {}
for op in ops:
    if op[0] == 'insert': mm.insert(op[1], op[2]); live[op[1]] = op[2]
    else: got.append(mm.sum(op[1])); scanned += len(live)
assert [x for x in solve(ops) if x is not None] == got
print('5000 mixed operations, keys of length <= 12: trie steps in total', mm.steps, '| keys a scan-per-sum would have examined', scanned)

# seeded random cross-check vs dict + startswith, including repeated replacement and value 0
for _ in range(500):
    ks = [''.join(random.choice('ab') for _ in range(random.randint(1, 4))) for _ in range(5)]
    ops = []
    for _ in range(random.randint(1, 30)):
        if random.random() < .55: ops.append(['insert', random.choice(ks), random.randint(0, 5)])
        else: ops.append(['sum', ''.join(random.choice('ab') for _ in range(random.randint(1, 3)))])
    assert solve(ops) == brute(ops), ops
print('500 seeded random operation lists agree with the dict scanned with startswith')

# edge asserts
assert solve([['sum', 'a']]) == [0]
assert solve([['insert', 'a', 5], ['insert', 'a', 5], ['sum', 'a']]) == [None, None, 5]
assert solve([['insert', 'ab', 9], ['insert', 'ab', 0], ['sum', 'a'], ['sum', 'ab'], ['sum', 'abc']]) == [None, None, 0, 0, 0]
assert solve([['insert', 'z' * 20, 1000], ['sum', 'z'], ['sum', 'z' * 20], ['sum', 'z' * 21]]) == [None, 1000, 1000, 0]
print('edge asserts passed')
```

**Output (my run):**
```
example -> [None, 3, None, 5, None, 7, 0]
example -> [0]
example -> [None, 0, None, 7]
  after insert apple 3: a=3, ap=3, app=3, appl=3, apple=3
  after insert app 2: a=5, ap=5, app=5, appl=3, apple=3
  after insert apple 5 (delta +2, not +5): a=7, ap=7, app=7, appl=5, apple=5
  sum(ap) = 7  sum(app) = 7  sum(b) = 0
the add-val-not-delta bug on example 1 gives [None, 3, None, 5, None, 10, 0] (expected 3, 5, 7, 0 at the sum positions)
5000 mixed operations, keys of length <= 12: trie steps in total 23558 | keys a scan-per-sum would have examined 1531573
500 seeded random operation lists agree with the dict scanned with startswith
edge asserts passed
```

Reading the output:
- All three examples match the dict-and-`startswith` oracle (insert prints `None`, the Python form of `null`).
- The printed node sums are the ones in the dry run. The bug demo returns 10 where 7 is right.
- Cost: on 5000 mixed operations over 1500 keys of length up to 12, the trie made 23,558 steps in total; a scan per `sum` would have examined 1,531,573 keys. (Step counts, not timings.)
- 500 seeded random operation lists (small alphabet so keys collide and are replaced often, values 0..5) agree with the oracle.

**Edge cases:**
- `sum` before any insert: 0.
- Insert with value 0, then `sum`: 0, and a later replacement by 7 gives 7.
- Same key inserted twice with the same value: unchanged.
- Prefix longer than any key (`'z' * 21`): 0.
- Prefix equal to a whole key: that key's value counts.
- Replacing a value with a smaller one: `delta` is negative, which is fine.

**Follow-ups:**
- "Delete a key?" `insert(key, 0)` leaves a zero-valued key; to really delete, subtract its value along the path and drop empty nodes.
- "Count of keys under a prefix?" A second counter, or the same code with `val = 1` for new keys (Part 7 Q41 counts words per prefix).
- "Memory of dict nodes?" Each dict is heavy (Q33 measures it); use arrays of 26 or a compressed trie if memory matters.

**Common mistakes:**
- Adding `val` instead of `new - old`: a replaced key counts twice.
- Not storing the old values separately (a trie holds sums, not per-key values), so `old` cannot be found.
- Returning `None` instead of 0 for a missing prefix.
- Scanning all keys for every `sum`.

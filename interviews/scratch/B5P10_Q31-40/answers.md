### Q31 ⭐ 🟢 The `[[0]*n]*m` aliasing trap. For 1 <= m, n <= 6 build two tables: `bug = [[0]*n]*m` and `ok = [[0 for _ in range(n)] for _ in range(m)]`, apply the assignments `ops` (a list of [r, c, v]; 0 <= r < m, 0 <= c < n) to both with `table[r][c] = v` in order, and return `[bug, ok, distinct_rows_bug, distinct_rows_ok]`, where the last two are the numbers of distinct row objects (by `id`) in each table. Explain, from what `*` does to a list, why one write shows up in every row of `bug`, why `[0]*n` itself is safe (the elements are immutable ints) and what DP bug this creates (all rows alias, so a DP table gives wrong answers whenever a cell reads a value from a row it did not just write, such as a diagonal neighbour; a table whose cells read only the cell above and the cell to the left can look right by accident, because the single shared row then acts like a rolling array). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a hand-written model of the aliasing on small inputs. Example: m=2, n=3, ops=[[0, 1, 5]] -> [[[0, 5, 0], [0, 5, 0]], [[0, 5, 0], [0, 0, 0]], 1, 2]; m=3, n=2, ops=[[0, 0, 1], [2, 1, 7], [1, 0, 9]] -> [[[9, 7], [9, 7], [9, 7]], [[1, 0], [9, 0], [0, 7]], 1, 3]; m=1, n=1, ops=[] -> [[[0]], [[0]], 1, 1].
**Asked at:** Python caching and recursion notes (functools documentation: fetch failed, not opened; a function-caching tutorial seen as a search snippet only; behaviour verified by running Python 3.13) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Python object identity, not an algorithm. It is the first DP bug people hit, because every 2D DP table starts with an allocation line.

**Say this first (1 line):** "`[[0]*n]*m` makes m references to one row list, so a write to any row is a write to all of them; `[0]*n` is fine because the ints are immutable, and the fix is a comprehension that builds a fresh row per iteration."

**Brute force:** There is nothing to optimise. The "brute force" is to build both tables, apply the writes, and compare them with a hand model of what aliasing should do. That is the cross-check below.

**Optimal:** The mechanism, step by step.
- `[0]*n` builds a list of n slots that all point to the one int object `0`. That is safe: `row[c] = v` rebinds one slot to a new object. It never changes the int `0` (ints cannot be mutated).
- `x * m` for a list `x` copies the element REFERENCES, not the elements. So `[row]*m` is a list of m slots pointing to the same list object `row`. No row is copied.
- `bug[r][c] = v` first fetches `bug[r]` (the one shared row), then rebinds slot `c` of that row. Every `bug[i]` is that row, so column `c` changes in all m rows at once.
- `ok = [[0 for _ in range(n)] for _ in range(m)]` runs the inner expression m times, so there are m separate lists.
- `distinct_rows_bug` is 1 for every m >= 1, because all m slots hold the same `id`. `distinct_rows_ok` is m.
- The DP consequence: a table filled row by row has only ONE row of storage when aliased. Whatever you write for row r overwrites row r-1 at the same time. Reads of the previous row then return the new values, which are wrong.
- Honest nuance (I tested it): the bug does not always change the final answer. For unique paths with right/down moves, each cell reads `dp[r-1][c]` and `dp[r][c-1]`. In the shared row those are exactly the old value and the new value, so the aliased table accidentally acts like the rolling 1D array and gives the right answer. It breaks as soon as a cell reads `dp[r-1][c-1]` (diagonal move, LCS, edit distance): that slot was already overwritten. The code shows 17 versus the correct 13. So "silently wrong" is true in general but not for every DP; never rely on luck.
- Safe patterns: `[[0]*n for _ in range(m)]` (inner `*` is fine, outer must be a comprehension), or `[[0 for _ in range(n)] for _ in range(m)]`. Do NOT use `copy.copy` on the outer list (shallow, same problem).

**Complexity:** Time O(m*n) to build and O(len(ops)) to apply writes. Space O(m*n) for `ok`, O(n) for `bug` (which is the whole problem: it has far less storage than you think).

**Dry run (first example):** `m=2, n=3, ops=[[0,1,5]]`.
- Start: `bug` is `[R, R]` where `R = [0,0,0]`. `ok` is `[A, B]` with `A = [0,0,0]`, `B = [0,0,0]` (separate lists).
- Apply `table[0][1] = 5`.

| step | table | `table[0]` | `table[1]` |
|---|---|---|---|
| before | bug | `[0,0,0]` (R) | `[0,0,0]` (the same R) |
| before | ok | `[0,0,0]` (A) | `[0,0,0]` (B) |
| after | bug | `[0,5,0]` (R) | `[0,5,0]` (the same R) |
| after | ok | `[0,5,0]` (A) | `[0,0,0]` (B) |

- Distinct rows: bug 1 (`id(R)`), ok 2. Result `[[[0,5,0],[0,5,0]], [[0,5,0],[0,0,0]], 1, 2]`. This matches the prompt.
- Second example: writes to column 0 (values 1, then 9) and column 1 (value 7). In `bug` the last write per column wins everywhere: `[9,7]` in all three rows. In `ok` each row keeps its own write: `[1,0]`, `[9,0]`, `[0,7]`.

**Code:**
```python
import random

random.seed(31)

def alias_trap(m, n, ops):
    bug = [[0] * n] * m                                   # m references to ONE row list
    ok = [[0 for _ in range(n)] for _ in range(m)]        # m separate row lists
    for r, c, v in ops:
        bug[r][c] = v
        ok[r][c] = v
    return [bug, ok, len({id(row) for row in bug}), len({id(row) for row in ok})]

def model(m, n, ops):
    """Hand model: bug has ONE row, so a write at (r, c) changes column c everywhere."""
    one_row = [0] * n
    real = [[0] * n for _ in range(m)]
    for r, c, v in ops:
        one_row[c] = v          # the single shared row
        real[r][c] = v          # a real, independent cell
    return [[one_row[:] for _ in range(m)], real, 1, m]

# ---- examples from the prompt
assert alias_trap(2, 3, [[0, 1, 5]]) == [[[0, 5, 0], [0, 5, 0]], [[0, 5, 0], [0, 0, 0]], 1, 2]
assert alias_trap(3, 2, [[0, 0, 1], [2, 1, 7], [1, 0, 9]]) == [[[9, 7], [9, 7], [9, 7]], [[1, 0], [9, 0], [0, 7]], 1, 3]
assert alias_trap(1, 1, []) == [[[0]], [[0]], 1, 1]
print('examples ok')

# ---- show the mechanism: * copies the reference, not the list
row = [0] * 3
t = [row] * 2
print('t[0] is t[1]:', t[0] is t[1], '| [0]*3 elements share one int object:', row[0] is row[1])
row[0] = 5   # rebinding a slot never mutates the int 0, so [0]*n is safe
print('after row[0] = 5:', row)

# ---- DPs filled row by row on the aliased table. The shared row acts like a rolling array.
def grid(m, n, diagonal, aliased):
    dp = [[0] * n] * m if aliased else [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if r == 0 or c == 0:
                dp[r][c] = 1
            else:
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1] + (dp[r - 1][c - 1] if diagonal else 0)
    return dp[m - 1][n - 1]
print('unique paths 3x3 (right/down moves): aliased =', grid(3, 3, False, True), ' correct =', grid(3, 3, False, False))
print('paths with a diagonal move 3x3:      aliased =', grid(3, 3, True, True), ' correct =', grid(3, 3, True, False))
assert grid(3, 3, False, True) == grid(3, 3, False, False) == 6      # the bug hides: reads of row r-1 see the old value
assert grid(3, 3, True, False) == 13 and grid(3, 3, True, True) != 13  # dp[r-1][c-1] was already overwritten

# ---- seeded cross-check: solution vs the hand model (and an exhaustive sweep of tiny shapes)
cases = 0
for _ in range(1000):
    m, n = random.randint(1, 6), random.randint(1, 6)
    ops = [[random.randrange(m), random.randrange(n), random.randint(-9, 9)] for _ in range(random.randint(0, 8))]
    assert alias_trap(m, n, ops) == model(m, n, ops), (m, n, ops)
    cases += 1
for m in range(1, 4):
    for n in range(1, 4):
        for r in range(m):
            for c in range(n):
                assert alias_trap(m, n, [[r, c, 7]]) == model(m, n, [[r, c, 7]])
                cases += 1
print('cross-check passed on', cases, 'cases')

# ---- edge cases
assert alias_trap(1, 3, [[0, 2, 4]])[0] == alias_trap(1, 3, [[0, 2, 4]])[1]   # m = 1: no visible bug
assert alias_trap(4, 1, [[3, 0, 8]])[0] == [[8]] * 4
print('edge cases ok')
```

**Output (my run):**
```
examples ok
t[0] is t[1]: True | [0]*3 elements share one int object: True
after row[0] = 5: [5, 0, 0]
unique paths 3x3 (right/down moves): aliased = 6  correct = 6
paths with a diagonal move 3x3:      aliased = 17  correct = 13
cross-check passed on 1036 cases
edge cases ok
```

**Edge cases:**
- m = 1: the aliased table has one row either way, so the bug is invisible. Do not conclude that it is safe; it breaks at m = 2.
- n = 1: still aliased (the rows are lists of length 1 pointing to one list).
- Empty `ops`: both tables are all zeros and equal, but the id counts still differ (1 versus m).
- Writing the same cell twice in `bug`: the last write wins in every row.

**Follow-ups:**
- *Same trap with other types?* `[[]]*m` for adjacency lists, `[{}]*m` for dicts, `[set()]*m`. Any mutable element. Use comprehensions.
- *Same trap with default arguments?* `def f(x, memo={})` shares one dict across calls. Related idea: one object, many names.
- *Why does `[0]*n` not bite?* Slot assignment rebinds, and ints have no in-place mutation. `[x]*n` with a mutable `x` bites only when you MUTATE `x` (`row.append`, `row[i] = ...`), not when you rebind the outer slot.

**Common mistakes:**
- Fixing it with `copy.copy` or `list(...)` on the outer list: still shallow.
- Using `deepcopy` of the aliased table after the fact; the damage is done when the writes happen before the copy.
- Believing a passing test proves the table is fine: unique paths passes by accident.
- Testing only m = 1 (no visible bug).

### Q32 ⭐ 🟡 `functools.cache`, mutable arguments and `cache_clear`. `nums` is a list of 0 <= len <= 15 integers (|value| <= 20) and `target` an integer (|target| <= 100). Write a memoised recursive function `f(i, rem)` that counts the subsets (chosen by position) of `nums` with sum `target`: `f(i, rem)` returns 1 if i == len(nums) and rem == 0, 0 if i == len(nums) otherwise, and else `f(i + 1, rem) + f(i + 1, rem - nums[i])` (no pruning of negative `rem`); decorate it with `@functools.cache`, keep `nums` as a tuple captured from the enclosing scope (a list passed as an argument would raise `TypeError: unhashable type: 'list'`). Call f(0, target) once and return `[answer, hits, misses, currsize_after_clear]` from `f.cache_info()` taken right after that call and after `f.cache_clear()`. Explain why misses equals the number of cached entries, why a list argument cannot be used as a cache key, and the options (convert to a tuple, use indices). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a hand-written dict memo that counts hits and misses itself on small inputs. Example: nums=[1, 2, 3], target=3 -> [2, 1, 14, 0]; nums=[], target=0 -> [1, 0, 1, 0]; nums=[0, 0], target=0 -> [4, 2, 3, 0]; nums=[2, 2, 2, 2], target=4 -> [6, 6, 15, 0].
**Asked at:** Python caching and recursion notes (functools documentation: fetch failed, not opened; a function-caching tutorial seen as a search snippet only; behaviour verified by running Python 3.13) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Top-down memoisation with `functools.cache`. The state is `(i, rem)`: positions decided so far and the sum still needed. Cache keys must be hashable.

**Say this first (1 line):** "`cache` keys on the call arguments, so arguments must be hashable; I keep `nums` as a tuple in the closure and pass only the ints `i` and `rem`, and the cache then holds one entry per distinct state, which is exactly the miss count."

**Brute force:** Enumerate all 2^n subsets and test the sum: O(2^n * n). With n <= 15 that is 32768 subsets and fine. It is one of the cross-checks (the other is a hand-written dict memo that counts hits and misses itself).

**Optimal:**
- State: `f(i, rem)` = the number of ways to choose from `nums[i:]` (by position) so that the chosen sum is `rem`.
- Base: `i == len(nums)`: 1 if `rem == 0`, else 0 (the empty choice is the only one left).
- Transition: `f(i, rem) = f(i+1, rem)` (skip `nums[i]`) `+ f(i+1, rem - nums[i])` (take it). There is no pruning, so `rem` may go negative and zeros and negatives are counted correctly (two zeros give 4 subsets for target 0).
- `@functools.cache` is `lru_cache(maxsize=None)`. The key is built from the arguments `(i, rem)`. Each distinct key is computed once (a miss); each repeat is a hit.
- Misses equal the number of cached entries: every miss stores exactly one new entry, there is no size limit so nothing is evicted, and a recursion that raises would store nothing. (With a `maxsize` limit this would stop being true.) I checked `misses == currsize == len(dict memo)` on all 500 random cases.
- Hits plus misses equals the number of calls to `f`, including the first call.
- Why a list cannot be a key: the key is hashed, and lists are mutable so `list.__hash__` is `None`; `f([1,2])` raises `TypeError: unhashable type: 'list'`. A mutable key could also change after being stored, which would corrupt the cache.
- Options: (1) pass a tuple (`tuple(nums)`), O(len) to hash on every call so only OK for small tuples; (2) pass indices and keep the data in a closure, as here (best); (3) your own `dict` memo with `(i, rem)` tuple keys.
- `cache_clear()` empties the cache and resets hits, misses and currsize to 0. Use it between tests when the function is module-level, because a stale cache is shared state; here `f` is rebuilt per call so it matters less, and the clear makes the last item of the answer 0.
- Recursion depth is len(nums) + 1 <= 16 here, so no recursion-limit issue (see Q33 for that).

**Complexity:** Time O(S) where S = the number of distinct states visited, at most (n+1) * (number of reachable sums) and at most 2^(n+1) - 1 without any collisions; each state costs O(1). Space O(S) for the cache plus O(n) stack. Here n <= 15 and |value| <= 20 so rem stays in a small range.

**Dry run (first example):** `nums=[1,2,3], target=3`. Calls in depth-first order, M = miss, H = hit.

| call | result | note |
|---|---|---|
| f(0,3) M | 2 | root |
| f(1,3) M | 1 | skip 1 |
| f(2,3) M | 1 | skip 2 |
| f(3,3) M | 0 | end, rem != 0 |
| f(3,0) M | 1 | end, take 3, rem 0 |
| f(2,1) M | 0 | take 2 |
| f(3,1) M, f(3,-2) M | 0, 0 | |
| f(1,2) M | 1 | take 1 |
| f(2,2) M | 0 | skip 2 |
| f(3,2) M, f(3,-1) M | 0, 0 | |
| f(2,0) M | 1 | take 2 |
| f(3,0) **H** | 1 | already stored |
| f(3,-3) M | 0 | |

- Total: 14 misses, 1 hit, answer 2 (subsets {3} and {1,2}), cache size 14 before the clear and 0 after: `[2, 1, 14, 0]`.

**Code:**
```python
import functools
import random

random.seed(32)

def solve(nums, target):
    ns = tuple(nums)          # hashable, captured by the closure (not a cache key)
    n = len(ns)

    @functools.cache
    def f(i, rem):
        if i == n:
            return 1 if rem == 0 else 0
        return f(i + 1, rem) + f(i + 1, rem - ns[i])

    ans = f(0, target)
    info = f.cache_info()
    entries = info.currsize          # entries held right before the clear
    f.cache_clear()
    return [ans, info.hits, info.misses, f.cache_info().currsize], entries

def oracle(nums, target):
    """Hand-written dict memo that counts hits and misses itself."""
    n = len(nums)
    memo, hits, misses = {}, 0, 0
    def f(i, rem):
        nonlocal hits, misses
        if (i, rem) in memo:
            hits += 1
            return memo[(i, rem)]
        misses += 1
        v = (1 if rem == 0 else 0) if i == n else f(i + 1, rem) + f(i + 1, rem - nums[i])
        memo[(i, rem)] = v
        return v
    a = f(0, target)
    return [a, hits, misses, 0], len(memo)

def brute_count(nums, target):
    n = len(nums)
    return sum(1 for mask in range(1 << n) if sum(nums[i] for i in range(n) if mask >> i & 1) == target)

# ---- examples from the prompt
assert solve([1, 2, 3], 3)[0] == [2, 1, 14, 0]
assert solve([], 0)[0] == [1, 0, 1, 0]
assert solve([0, 0], 0)[0] == [4, 2, 3, 0]
assert solve([2, 2, 2, 2], 4)[0] == [6, 6, 15, 0]
print('examples ok')

# ---- why a list argument cannot be a cache key
@functools.cache
def g(lst):
    return sum(lst)
try:
    g([1, 2])
except TypeError as e:
    print('TypeError:', e)
print('tuple key works:', g((1, 2)))

# ---- misses == entries stored; hits + misses == number of calls
ex, entries = solve([1, 2, 3], 3)
print('example 1: misses', ex[2], 'entries before clear', entries, 'currsize after clear', ex[3])

# ---- seeded cross-check against the dict memo and a plain subset enumeration
cases = 0
for _ in range(500):
    nums = [random.randint(-20, 20) for _ in range(random.randint(0, 9))]
    target = random.randint(-100, 100) if random.random() < 0.3 else sum(random.sample(nums, random.randint(0, len(nums))))
    got, entries = solve(nums, target)
    exp, entries2 = oracle(nums, target)
    assert got == exp, (nums, target, got, exp)
    assert got[2] == entries == entries2          # misses == cached entries
    assert got[0] == brute_count(nums, target)
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- cache_clear matters: a closure cache is rebuilt per call here, but a module-level one grows across tests
@functools.cache
def h(i):
    return i * 2
h(1); h(2); h(1)
print('module-level cache:', h.cache_info())
h.cache_clear()
print('after cache_clear:', h.cache_info())
assert h.cache_info().currsize == 0

# ---- edge cases
assert solve([], 5)[0] == [0, 0, 1, 0]
assert solve([20] * 15, 100)[0][0] == 3003          # C(15, 5)
print('edge cases ok')
```

**Output (my run):**
```
examples ok
TypeError: unhashable type: 'list'
tuple key works: 3
example 1: misses 14 entries before clear 14 currsize after clear 0
cross-check passed on 500 cases
module-level cache: CacheInfo(hits=1, misses=2, maxsize=None, currsize=2)
after cache_clear: CacheInfo(hits=0, misses=0, maxsize=None, currsize=0)
edge cases ok
```

**Edge cases:**
- `nums = []`: one miss, answer 1 if `target == 0` else 0.
- Zeros and negatives: no pruning on `rem`, otherwise `[0, 0]` target 0 would count 1 instead of 4.
- Duplicate values count as different positions (2,2,2,2 target 4 gives 6).
- Calling `info = f.cache_info()` after `cache_clear()` shows zeros; take it BEFORE the clear.

**Follow-ups:**
- *Why not decorate a function that takes `nums` as an argument?* Lists are unhashable; passing a tuple works but hashes the whole tuple per call.
- *`cache` versus `lru_cache(maxsize=128)`?* The default `lru_cache` evicts, so misses no longer equal entries and a DP can become exponential again. Use `maxsize=None` or `cache` for DP.
- *Memory leak?* A module-level cache keeps arguments alive (and every state) until `cache_clear()`. Methods on instances also keep `self` alive.

**Common mistakes:**
- Putting a list or dict in the signature of a cached function.
- Reading `cache_info()` after `cache_clear()` and wondering why everything is 0.
- Forgetting that a decorated function defined inside a loop or per-call has a fresh cache each time.
- Pruning `rem < 0` when negatives exist.

### Q33 ⭐ 🟡 Memoised recursion versus bottom-up: the recursion limit. Count the ways to climb `n` stairs with steps 1, 2 or 3 modulo 10^9 + 7 (f(0) = 1, f(k) = f(k-1) + f(k-2) + f(k-3), f(negative) = 0), for n in 0..500 or 2000..10^5. Return `[ways, memo_outcome]` where `ways` is the correct answer from your bottom-up loop and `memo_outcome` is the string 'ok' if a `@functools.cache` top-down version `f(n)` called in a fresh Python 3.13 interpreter at the default recursion limit returns normally, or 'RecursionError' if it raises. Explain why the depth is about n, why raising `sys.setrecursionlimit` is not a fix to rely on in an interview, and how bottom-up avoids it. (Part 7 Q35 shows the same limit on deep trees.) In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against the memoised top-down function itself, run in try/except (the oracle returns the outcome and, when it succeeds, the value) on small inputs. Example: n=0 -> [1, 'ok']; n=10 -> [274, 'ok']; n=500 -> [283701821, 'ok']; n=2000 -> [78591238, 'RecursionError']; n=100000 -> [111787461, 'RecursionError'].
**Asked at:** Python caching and recursion notes (functools documentation: fetch failed, not opened; a function-caching tutorial seen as a search snippet only; behaviour verified by running Python 3.13) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Tabulation (bottom-up) versus memoisation (top-down) for a linear counting DP, and what the Python recursion limit does to the top-down one.

**Say this first (1 line):** "The recurrence is f(k) = f(k-1) + f(k-2) + f(k-3); top-down recursion goes about n frames deep and dies at n of about 1000 under the default limit, so I write it bottom-up with three rolling variables."

**Brute force:** Plain recursion with no cache: T(n) = T(n-1) + T(n-2) + T(n-3), which grows like 1.84^n. Hopeless past n of about 35. The memoised version fixes the time but not the depth.

**Optimal:**
- State: `f(k)` = number of ordered step sequences (steps 1, 2 or 3) that sum to exactly k, modulo 10^9 + 7.
- Base: `f(0) = 1` (the empty sequence), `f(negative) = 0`. So `f(1) = 1`, `f(2) = 2`, `f(3) = 4`.
- Transition: the LAST step is 1, 2 or 3, so `f(k) = f(k-1) + f(k-2) + f(k-3)`. Apply the modulus at every addition so numbers stay small (Python ints would not overflow, but they would become huge and slow).
- Bottom-up: keep `(f(k-3), f(k-2), f(k-1))` in three variables and roll them n times. O(n) time, O(1) space, no recursion.
- Top-down with `@functools.cache`: `f(n)` calls `f(n-1)` first, which calls `f(n-2)`... down to `f(0)` before anything returns. The chain is about n frames deep (one frame per level; the cache wrapper is C code and adds no Python frame, but the calls still nest).
- Default limit: `sys.getrecursionlimit()` is 1000. The oracle run says the largest working n at module level here is 997 (the script's own frames take a few). So n in 0..500 is `'ok'` and n >= 1000 raises `RecursionError`. That matches the prompt: n = 2000 and 10^5 both raise.
- Why not `sys.setrecursionlimit(10**6)`: the limit is a guard, not extra stack. Python frames for pure-Python calls are cheap in 3.13, but this function reaches through the C `lru_cache` wrapper, and I measured that even with the limit at 10^6 it still raises at n = 5000 in Python 3.13.17 here (n = 3000 passed). In an older CPython or a different build the same code can crash the interpreter with a segfault instead of raising. Behaviour depends on the build, so it is unsafe to rely on in an interview or in production. Bottom-up has no such failure.
- Other fixes: an explicit stack (iterative DFS), or just bottom-up. For this recurrence bottom-up is simplest.
- Cross-reference: Part 7 Q35 shows the same limit on deep trees.

**Complexity:** Bottom-up: time O(n), space O(1). Top-down memoised: time O(n) but space O(n) for the cache plus an O(n) call stack, and it fails for n above about 1000 at the default limit. Plain recursion: exponential (about 1.84^n).

**Dry run (first example family, n = 10):** `f(0)=1`, `f(-1)=f(-2)=0`.

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| f(k) | 1 | 1 | 2 | 4 | 7 | 13 | 24 | 44 | 81 | 149 | 274 |

- Check one cell: `f(4) = f(3) + f(2) + f(1) = 4 + 2 + 1 = 7`. `f(10) = f(9) + f(8) + f(7) = 149 + 81 + 44 = 274`. Matches the prompt.
- The three rolling variables hold `(f(k-3), f(k-2), f(k-1))`: start `(0, 0, 1)` for k = 1, then `(0, 1, 1)`, `(1, 1, 2)`, `(1, 2, 4)`, `(2, 4, 7)`... the last value is the answer.
- Top-down trace for n = 3: `f(3)` calls `f(2)` calls `f(1)` calls `f(0)` (depth 4); the values then return upward, and `f(-1)`, `f(-2)` return 0 immediately.

**Code:**
```python
import functools
import random
import sys

random.seed(33)
MOD = 10**9 + 7
assert sys.getrecursionlimit() == 1000          # the default; the claims below are about this limit

def bottom_up(n):
    """f(0)=1, f(k)=f(k-1)+f(k-2)+f(k-3), f(negative)=0, three rolling variables, no recursion."""
    if n == 0:
        return 1
    a, b, c = 0, 0, 1                           # f(-2), f(-1), f(0)
    for _ in range(n):
        a, b, c = b, c, (a + b + c) % MOD
    return c

@functools.cache
def top_down(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    return (top_down(n - 1) + top_down(n - 2) + top_down(n - 3)) % MOD

def memo_outcome(n):
    """The oracle: run the memoised recursion in try/except. Returns (outcome, value or None)."""
    top_down.cache_clear()
    try:
        return 'ok', top_down(n)
    except RecursionError:
        return 'RecursionError', None

def solve(n):
    # 'ways' from the loop; 'memo_outcome' is reported by running top_down in this interpreter
    return [bottom_up(n), memo_outcome(n)[0]]

# ---- examples from the prompt
assert solve(0) == [1, 'ok']
assert solve(10) == [274, 'ok']
assert solve(500) == [283701821, 'ok']
assert solve(2000) == [78591238, 'RecursionError']
assert solve(100000) == [111787461, 'RecursionError']
print('examples ok')

# ---- where exactly does the default limit bite? (the depth is about n, one frame per level)
top = 0
for n in range(1, 1000):
    if memo_outcome(n)[0] == 'ok':
        top = n
    else:
        break
print('largest n that works at limit 1000 (this interpreter, called from module level):', top)

# ---- every n in 0..500 is fine, so the prompt's 'ok' range is correct
assert all(memo_outcome(n)[0] == 'ok' for n in range(0, 501))
print('n = 0..500 all ok')

# ---- seeded cross-check: bottom-up value against the memoised oracle, outcome as well
cases = 0
for _ in range(300):
    n = random.randint(0, 500)
    out, val = memo_outcome(n)
    assert out == 'ok' and val == bottom_up(n)
    cases += 1
for n in (1000, 1500, 2000, 5000, 10**5):
    out, val = memo_outcome(n)
    assert out == 'RecursionError' and val is None and solve(n)[1] == out
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- raising the limit: a stopgap, not a plan
old = sys.getrecursionlimit()
sys.setrecursionlimit(10**6)
for n in (2000, 3000, 5000):
    out, val = memo_outcome(n)
    print('limit raised, n =', n, '->', out, '| bottom-up agrees:', val is None or val == bottom_up(n))
sys.setrecursionlimit(old)
print('limit restored to', sys.getrecursionlimit())

# ---- bottom-up at the full size, and the space-optimised form is O(1)
print('bottom-up n = 10**5:', bottom_up(10**5))
assert bottom_up(1) == 1 and bottom_up(2) == 2 and bottom_up(3) == 4
```

**Output (my run):**
```
examples ok
largest n that works at limit 1000 (this interpreter, called from module level): 997
n = 0..500 all ok
cross-check passed on 305 cases
limit raised, n = 2000 -> ok | bottom-up agrees: True
limit raised, n = 3000 -> ok | bottom-up agrees: True
limit raised, n = 5000 -> RecursionError | bottom-up agrees: True
limit restored to 1000
bottom-up n = 10**5: 111787461
```

**Edge cases:**
- n = 0: one way (do nothing); n = 1: 1; n = 2: 2.
- The modulus comes after the SUM of three terms, not on each term separately only; either is correct as long as every stored value is reduced.
- The first top-down call is the deepest; calling `f(500)` first and then `f(900)` works for that reason (the cache holds the lower values), but a fresh `f(2000)` still fails. Warm-up loops (`for k in range(n): f(k)`) are a hack to dodge the limit; bottom-up is the honest version.
- `RecursionError` is raised, not a wrong answer, so it is loud. Mention it in a code review.

**Follow-ups:**
- *Can you do n = 10^18?* Yes: matrix exponentiation of the 3x3 companion matrix, O(27 log n).
- *Why is the cache wrapper not adding frames?* `lru_cache` is implemented in C; the Python function frame is the only one per level. Still, I will not rely on that.
- *Climbing stairs with steps 1 and 2?* The same code with two variables (Fibonacci).

**Common mistakes:**
- Raising the recursion limit and calling it fixed.
- Forgetting `cache_clear()` between tests, so a warm cache hides the error for large n.
- Leaving out the modulus (answers become enormous big ints) or applying it only at the end.
- Off-by-one in the base: `f(0) = 1`, not 0.

### Q34 ⭐ 🟡 Longest increasing subsequence: recover one (with a tie rule). `nums` has 0 <= len <= 2000 integers (|value| <= 10^6). Among all strictly increasing subsequences of maximum length, return the VALUES of the one whose index list is lexicographically smallest (compare the position lists element by element); return [] for an empty list. Explain why the `tails` array of the bisect method (Q7) is not the answer, how to rebuild from the O(n^2) table, and how the patience-sorting method can recover a subsequence with predecessor pointers (which may return a different optimal subsequence unless you follow the tie rule). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsequences with the same tie rule (len <= 12) on small inputs. Example: nums=[10, 9, 2, 5, 3, 7, 101, 18] -> [2, 5, 7, 101]; nums=[0, 1, 0, 3, 2, 3] -> [0, 1, 2, 3]; nums=[3, 3, 3] -> [3]; nums=[] -> []; nums=[1, 3, 2, 4] -> [1, 3, 4].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** LIS with reconstruction. Compute the table from the right, then walk it left to right picking the smallest valid index each time.

**Say this first (1 line):** "`tails` only gives the length, not a subsequence; for the answer I take the O(n^2) table `f[i]` = longest increasing subsequence starting at i, then scan left to right picking the first index with the needed `f` and a larger value than the last pick, which gives the lexicographically smallest index list."

**Brute force:** Enumerate all subsets by index, keep the strictly increasing ones, take the longest, and among those the smallest index tuple. O(2^n * n); fine for n <= 12. It is the oracle.

**Optimal:**
- State: `f[i]` = length of the longest strictly increasing subsequence that STARTS at index i.
- Base: `f[i] = 1` (just `nums[i]`).
- Transition, filled for i from n-1 down to 0: `f[i] = 1 + max(f[j])` over `j > i` with `nums[j] > nums[i]` (default 1).
- Why from the right: then "starts at i" lets me read forward. The first element of the answer is the smallest index i with `f[i] = L` (L = max f). The next element is the smallest `j > i` with `nums[j] > nums[i]` and `f[j] = L - 1`, and one exists by the definition of `f[i]`. Repeat.
- Why this is the lexicographically smallest INDEX list: at every step I take the smallest index that can still be extended to full length L, and every shorter prefix choice is forced by that. The scan keeps going to the right, so indices are increasing automatically; the check `nums[i] > last` enforces the strictness.
- Ties: equal values are distinct positions. `[3,3,3]` has L = 1 and the answer `[3]` is index 0.
- Why `tails` is not the answer: `tails[k]` is the smallest possible LAST value of an increasing subsequence of length k + 1, taken over different subsequences. Entries come from different subsequences and may even sit in the wrong order of positions. Example: `[3, 4, 1]` gives `tails = [1, 4]`, but 1 comes after 4, so `[1, 4]` is not a subsequence.
- Patience sorting with predecessor pointers: when `x` lands at pile p, remember `pred[i]` = the index on top of pile p - 1 at that moment. Follow pred from the top of the last pile. It always yields a valid optimal subsequence in O(n log n), but not the tie-rule one. On the first example it returns `[2, 3, 7, 18]` (indices 2, 4, 5, 7) while the tie rule gives `[2, 5, 7, 101]` (indices 2, 3, 5, 6). Both have length 4. On 600 seeded small lists the two index lists differed on 368. If the question says "any one", patience is enough; with a tie rule use the table.
- Space: the O(n^2) approach needs only the 1D table `f` (O(n)); no 2D table.

**Complexity:** Table: time O(n^2) (n = 2000 gives 2 million pair checks), space O(n). Walk: O(n). Patience with pred: O(n log n) time, O(n) space (tails, tails_idx, pred).

**Dry run (first example):** `nums = [10, 9, 2, 5, 3, 7, 101, 18]`, fill `f` from the right.

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| nums | 10 | 9 | 2 | 5 | 3 | 7 | 101 | 18 |
| f (starts here) | 2 | 2 | 4 | 3 | 3 | 2 | 1 | 1 |

- Check: `f[5]` (value 7): later larger values 101 and 18 both have f = 1, so f = 2. `f[3]` (value 5): larger later values are 7 (f 2), 101, 18, so f = 3. `f[2]` (value 2): best is `f[3] = 3`, so 4.
- L = 4. Walk: the first index with f = 4 is index 2 (value 2). Need 3: first index after it with f = 3 and value > 2 is index 3 (value 5). Need 2: index 4 has f = 3, not 2; index 5 has f = 2 and 7 > 5, take it. Need 1: index 6 (value 101), f = 1 and 101 > 7. Result `[2, 5, 7, 101]`.

**Code:**
```python
import bisect
import itertools
import random

random.seed(34)

def lis_table(nums):
    """f[i] = length of the longest strictly increasing subsequence that STARTS at index i. O(n^2)."""
    n = len(nums)
    f = [1] * n
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if nums[j] > nums[i] and f[j] + 1 > f[i]:
                f[i] = f[j] + 1
    return f

def lis_lex_min(nums):
    """Values of the max-length strictly increasing subsequence with the lexicographically smallest index list."""
    n = len(nums)
    if n == 0:
        return []
    f = lis_table(nums)
    need, last, out = max(f), None, []
    for i in range(n):                       # scanning left to right = smallest next index first
        if f[i] == need and (last is None or nums[i] > last):
            out.append(nums[i])
            last = nums[i]
            need -= 1
            if need == 0:
                break
    return out

def lis_patience(nums):
    """O(n log n) with predecessor pointers. A valid LIS, but NOT necessarily the lexicographically smallest."""
    tails_val, tails_idx, pred = [], [], [-1] * len(nums)
    for i, x in enumerate(nums):
        p = bisect.bisect_left(tails_val, x)
        if p == len(tails_val):
            tails_val.append(x); tails_idx.append(i)
        else:
            tails_val[p] = x; tails_idx[p] = i
        pred[i] = tails_idx[p - 1] if p else -1
    out, k = [], tails_idx[-1] if tails_idx else -1
    while k != -1:
        out.append(k)
        k = pred[k]
    out.reverse()
    return out, tails_val                    # index list, tails

def lis_brute(nums):
    n = len(nums)
    for L in range(n, 0, -1):
        cands = [c for c in itertools.combinations(range(n), L)
                 if all(nums[c[t]] < nums[c[t + 1]] for t in range(L - 1))]
        if cands:
            return [nums[i] for i in min(cands)]       # tuples compare lexicographically
    return []

# ---- examples from the prompt
assert lis_lex_min([10, 9, 2, 5, 3, 7, 101, 18]) == [2, 5, 7, 101]
assert lis_lex_min([0, 1, 0, 3, 2, 3]) == [0, 1, 2, 3]
assert lis_lex_min([3, 3, 3]) == [3]
assert lis_lex_min([]) == []
assert lis_lex_min([1, 3, 2, 4]) == [1, 3, 4]
print('examples ok')

# ---- the tables for the first example
ex = [10, 9, 2, 5, 3, 7, 101, 18]
print('nums     :', ex)
print('f (start):', lis_table(ex))
idx, tails = lis_patience(ex)
print('tails    :', tails, '(length 4 is right; here the content happens to be valid too)')
print('patience (pred pointers):', [ex[i] for i in idx], 'indices', idx, '| tie rule:', lis_lex_min(ex))
assert [ex[i] for i in idx] != lis_lex_min(ex)      # both are optimal, different answers
bad = [3, 4, 1]
print('tails for', bad, '=', lis_patience(bad)[1], 'but no increasing subsequence of nums reads 1 then 4: tails is not the answer')

# ---- seeded cross-check against the enumeration with the same tie rule
cases = diff_patience = 0
for _ in range(600):
    n = random.randint(0, 12)
    nums = [random.randint(-4, 8) for _ in range(n)]
    assert lis_lex_min(nums) == lis_brute(nums), nums
    pidx, _t = lis_patience(nums)
    pv = [nums[i] for i in pidx]
    assert len(pv) == len(lis_lex_min(nums))                          # same length
    assert all(pv[t] < pv[t + 1] for t in range(len(pv) - 1))         # a valid strictly increasing subsequence
    assert pidx == sorted(pidx)
    # indices of the tie-rule answer, for comparison of INDEX lists
    f = lis_table(nums); need = max(f, default=0); last = None; li = []
    for i in range(n):
        if need and f[i] == need and (last is None or nums[i] > last):
            li.append(i); last = nums[i]; need -= 1
    if pidx != li:
        diff_patience += 1
    cases += 1
print('cross-check passed on', cases, 'cases; patience index list differs from the tie rule on', diff_patience)

# ---- edge cases
assert lis_lex_min([5]) == [5]
assert lis_lex_min([5, 4, 3, 2, 1]) == [5]                  # all equal length 1: smallest index
assert lis_lex_min([1, 2, 3, 4]) == [1, 2, 3, 4]
assert lis_lex_min([2, 2, 3, 3]) == [2, 3]
assert len(lis_lex_min(list(range(2000)))) == 2000
print('edge cases ok')
```

**Output (my run):**
```
examples ok
nums     : [10, 9, 2, 5, 3, 7, 101, 18]
f (start): [2, 2, 4, 3, 3, 2, 1, 1]
tails    : [2, 3, 7, 18] (length 4 is right; here the content happens to be valid too)
patience (pred pointers): [2, 3, 7, 18] indices [2, 4, 5, 7] | tie rule: [2, 5, 7, 101]
tails for [3, 4, 1] = [1, 4] but no increasing subsequence of nums reads 1 then 4: tails is not the answer
cross-check passed on 600 cases; patience index list differs from the tie rule on 368
edge cases ok
```

**Edge cases:**
- Empty list: return `[]` (L would be undefined).
- All equal: length 1, the first element.
- Strictly decreasing: length 1, the first element (index 0).
- Already increasing: the whole list.
- Duplicates in the middle (`[2,2,3,3]` gives `[2,3]` using the first 2 and the first 3).

**Follow-ups:**
- *Count them?* Keep a parallel count table (Part 10 Q28).
- *Any one LIS is enough?* Then patience sorting with predecessor pointers is O(n log n) and valid. The tie rule is what forces the table walk in this question.
- *Why from the right?* So `f[i]` means "starts at i" and the answer can be read forward, smallest index first.

**Common mistakes:**
- Returning `tails`.
- Building `f` ending at i and then scanning backwards, which yields the lexicographically LARGEST index list.
- Using `>=` and returning a non-decreasing subsequence.
- Forgetting the empty input.

### Q35 ⭐ 🟡 Longest non-decreasing subsequence and the bisect_left versus bisect_right choice. `nums` has 0 <= len <= 10^5 integers (|value| <= 10^9). Return `[nondecreasing_length, tails, strict_length]`: the length of the longest non-decreasing subsequence, the final patience-sorting `tails` array for that variant, and the length of the longest strictly increasing subsequence. Explain which of `bisect_left` and `bisect_right` each variant uses (see Part 5 Q11), and what answer you get if you use `bisect_left` for the non-decreasing variant (it silently computes the strict length). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsequences (len <= 12) on small inputs. Example: nums=[1, 3, 3, 2, 3] -> [4, [1, 2, 3, 3], 3]; nums=[5, 5, 5] -> [3, [5, 5, 5], 1]; nums=[2, 1] -> [1, [1], 1]; nums=[] -> [0, [], 0]; nums=[4, 4, 2, 9, 9, 1] -> [4, [1, 4, 9, 9], 2].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** LIS in O(n log n) by patience sorting: `tails[k]` is the smallest possible last value of a valid subsequence of length k + 1. The only change between strict and non-decreasing is which bisect you call.

**Say this first (1 line):** "Strict increasing uses `bisect_left` (an equal value replaces the equal one), non-decreasing uses `bisect_right` (an equal value goes after the equals); using `bisect_left` for non-decreasing silently returns the strict length."

**Brute force:** Enumerate all 2^n subsequences, test sortedness, and for each length keep the smallest last value. O(2^n * n), n <= 12 only. It gives the lengths and also the `tails` array, so the cross-check compares all three outputs.

**Optimal:**
- Invariant: after processing a prefix, `tails` is sorted (non-decreasing for the variant, strictly increasing for strict), and `tails[k]` is the minimum last value over all valid subsequences of length k + 1 in that prefix. The length of `tails` is the answer.
- For each `x`: find the position `p` where `x` belongs; if `p == len(tails)` append, else overwrite `tails[p] = x` (a smaller or equal tail of the same length is never worse).
- Non-decreasing: `p = bisect_right(tails, x)` = first index with `tails[p] > x`. An equal tail does NOT block `x`, so `x` extends the equal run. For `[5,5,5]`: every 5 goes to the end, `tails = [5,5,5]`.
- Strict: `p = bisect_left(tails, x)` = first index with `tails[p] >= x`. An equal tail blocks (x cannot follow an equal value), so `x` replaces it. For `[5,5,5]`: `tails = [5]`.
- Using `bisect_left` for non-decreasing gives exactly the strict length (I checked on 600 random lists: equal always; it was wrong for non-decreasing on 284 of them). Silent, no error. See Part 5 Q11 for `bisect_left` versus `bisect_right` semantics.
- The `tails` for the non-decreasing variant is not itself an answer subsequence either; only its length is. It is the same idea as Q34.
- Return value: `[len(nd_tails), nd_tails, len(strict_tails)]`, two passes of the same loop with different bisects.

**Complexity:** Time O(n log n): n elements, one binary search each (an overwrite or an append is O(1)). Space O(n) for `tails`. For n = 10^5 that is about 1.7 million comparisons.

**Dry run (first example):** `nums = [1, 3, 3, 2, 3]`.

| x | non-decreasing tails (`bisect_right`) | strict tails (`bisect_left`) |
|---|---|---|
| 1 | [1] | [1] |
| 3 | [1, 3] | [1, 3] |
| 3 | [1, 3, 3] (right of the equal 3) | [1, 3] (replaces the 3) |
| 2 | [1, 2, 3] (`bisect_right` at 2 is 1, replace the first 3) | [1, 2] (replace 3) |
| 3 | [1, 2, 3, 3] (append) | [1, 2, 3] (append) |

- Answer `[4, [1, 2, 3, 3], 3]`. A real non-decreasing subsequence of length 4 is `[1, 3, 3, 3]` (indices 0, 1, 2, 4); note `tails` ends in `[1,2,3,3]`, which is NOT a subsequence of `nums` in that order, because 2 sits after the first 3. That is normal: tails is not the subsequence.

**Code:**
```python
import bisect
import itertools
import random

random.seed(35)

def patience(nums, strict):
    """tails[k] = smallest possible last value of a valid subsequence of length k + 1."""
    find = bisect.bisect_left if strict else bisect.bisect_right
    tails = []
    for x in nums:
        p = find(tails, x)
        if p == len(tails):
            tails.append(x)
        else:
            tails[p] = x
    return tails

def solve(nums):
    nd = patience(nums, strict=False)      # bisect_right: an equal value goes AFTER the equals
    st = patience(nums, strict=True)       # bisect_left: an equal value REPLACES the equal
    return [len(nd), nd, len(st)]

def brute(nums):
    """Enumerate every subsequence; for each length keep the smallest last value."""
    n = len(nums)
    best_nd, best_st = {}, {}
    for L in range(1, n + 1):
        for c in itertools.combinations(range(n), L):
            v = [nums[i] for i in c]
            if all(v[t] <= v[t + 1] for t in range(L - 1)):
                best_nd[L] = min(best_nd.get(L, v[-1]), v[-1])
            if all(v[t] < v[t + 1] for t in range(L - 1)):
                best_st[L] = min(best_st.get(L, v[-1]), v[-1])
    return [len(best_nd), [best_nd[k] for k in sorted(best_nd)], len(best_st)]

def nondecreasing_with_bisect_left(nums):
    return len(patience(nums, strict=True))          # the classic slip

# ---- examples from the prompt
assert solve([1, 3, 3, 2, 3]) == [4, [1, 2, 3, 3], 3]
assert solve([5, 5, 5]) == [3, [5, 5, 5], 1]
assert solve([2, 1]) == [1, [1], 1]
assert solve([]) == [0, [], 0]
assert solve([4, 4, 2, 9, 9, 1]) == [4, [1, 4, 9, 9], 2]
print('examples ok')

# ---- step trace of the first example
nums = [1, 3, 3, 2, 3]
tr, tl = [], []
for x in nums:
    tr.append(x)
    tl.append((x, patience(tr, False), patience(tr, True)))
for x, a, b in tl:
    print(f'x={x}: non-decreasing tails (bisect_right) {a} | strict tails (bisect_left) {b}')

# ---- seeded random cross-check against the enumeration, plus an exhaustive sweep
cases = 0
for _ in range(500):
    nums = [random.randint(-5, 5) for _ in range(random.randint(0, 12))]
    assert solve(nums) == brute(nums), nums
    cases += 1
for n in range(0, 7):
    for nums in itertools.product(range(4), repeat=n):
        assert solve(list(nums)) == brute(list(nums)), nums
        cases += 1
print('cross-check passed on', cases, 'cases')

# ---- what bisect_left gives for the non-decreasing variant: the strict length, always
wrong = same = 0
for _ in range(600):
    nums = [random.randint(0, 5) for _ in range(random.randint(0, 10))]
    assert nondecreasing_with_bisect_left(nums) == solve(nums)[2]
    if nondecreasing_with_bisect_left(nums) != solve(nums)[0]:
        wrong += 1
print('bisect_left for non-decreasing equals the strict length on all 600; it is wrong for non-decreasing on', wrong)
print('example [5, 5, 5]: bisect_left gives', nondecreasing_with_bisect_left([5, 5, 5]), 'instead of 3')

# ---- edge cases and size
assert solve([7]) == [1, [7], 1]
assert solve([3, 2, 1]) == [1, [1], 1]
assert solve([1, 1, 2, 2]) == [4, [1, 1, 2, 2], 2]
big = [random.randint(-10**9, 10**9) for _ in range(10**5)]
r = solve(big)
assert 1 <= r[2] <= r[0] <= len(big)
print('n = 10**5 random lengths (non-decreasing, strict):', r[0], r[2])
```

**Output (my run):**
```
examples ok
x=1: non-decreasing tails (bisect_right) [1] | strict tails (bisect_left) [1]
x=3: non-decreasing tails (bisect_right) [1, 3] | strict tails (bisect_left) [1, 3]
x=3: non-decreasing tails (bisect_right) [1, 3, 3] | strict tails (bisect_left) [1, 3]
x=2: non-decreasing tails (bisect_right) [1, 2, 3] | strict tails (bisect_left) [1, 2]
x=3: non-decreasing tails (bisect_right) [1, 2, 3, 3] | strict tails (bisect_left) [1, 2, 3]
cross-check passed on 5961 cases
bisect_left for non-decreasing equals the strict length on all 600; it is wrong for non-decreasing on 284
example [5, 5, 5]: bisect_left gives 1 instead of 3
n = 10**5 random lengths (non-decreasing, strict): 628 628
```

**Edge cases:**
- Empty list: `[0, [], 0]`.
- All equal: non-decreasing is n, strict is 1.
- Strictly decreasing: 1 and 1.
- Large values (10^9) and negatives are fine; only comparisons are used.
- If the problem says "non-increasing", negate the values (or reverse the list) and reuse the same routine.

**Follow-ups:**
- *Longest non-increasing subsequence?* Negate every value and run the non-decreasing version.
- *Why does overwriting with an equal value not matter in strict mode?* Same value, same position, nothing changes; replacing the equal is a no-op for the length and keeps the strict invariant.
- *Russian dolls?* A sort trick plus the strict version (Q40).

**Common mistakes:**
- `bisect_left` for the non-decreasing variant (the classic bug).
- `bisect_right` for strict, which counts equal values as extending.
- Returning `tails` as if it were the subsequence.
- Starting with `tails = [nums[0]]` and crashing on the empty list.

### Q36 ⭐ 🟡 Number of dice rolls with a target sum (counting with a modulus). You roll `n` dice, each with faces 1..k (1 <= n, k <= 30), and `target` is 0 <= target <= 1000. Return the number of ordered outcomes (sequences of n faces) whose sum is exactly `target`, modulo 10^9 + 7; 0 if impossible. Roll the table over dice with a single 1D array (a new array per die, no in-place hazards), say what the state is and why the answer is 0 outside n..n*k, and where the modulus is applied. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all k^n outcomes (k^n <= 10^5) on small inputs. Example: n=1, k=6, target=3 -> 1; n=2, k=6, target=7 -> 6; n=30, k=30, target=500 -> 222616187; n=2, k=5, target=1 -> 0.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Counting DP over a rolling 1D array. The state is "dice thrown so far, sum so far", and one die is one layer.

**Say this first (1 line):** "`dp[s]` is the number of ordered outcomes of the dice thrown so far with sum s; each die builds a new array by adding faces 1..k, and I take the modulus on every addition."

**Brute force:** Enumerate all k^n sequences of faces and count those with the right sum. Exponential; fine only when k^n <= 10^5. It is the oracle.

**Optimal:**
- State: after j dice, `dp_j[s]` = the number of ordered sequences of j faces (each 1..k) that add to s.
- Base: `dp_0[0] = 1` (the empty sequence), every other `dp_0[s] = 0`.
- Transition: `dp_j[s] = sum over f = 1..k of dp_{j-1}[s - f]` (the last die shows f). Written "forward": for each s with `dp[s] != 0`, for each f, add `dp[s]` into `new[s + f]`.
- Answer: `dp_n[target]`, modulo 10^9 + 7.
- Rolling: only `dp_{j-1}` is needed for `dp_j`, so two 1D arrays of length `target + 1`. A NEW array per die is the safe form: updating one array in place would let a die's contribution be read again by the same die (the same hazard that breaks the upward 0/1 knapsack loop in Q37; here it would let one die show several faces).
- Why 0 outside n..n*k: each die contributes at least 1 and at most k, so n dice give a sum in `[n, n*k]`. Nothing can reach a target below n or above n*k, and the table never gets a nonzero entry there. I checked this for 4 dice with 6 faces: zero outside 4..24, positive inside. Target 0 gives 0 because n >= 1.
- Where the modulus goes: on every addition into `new[s + f]`, so every stored value stays below 10^9 + 7. Reducing only at the end also gives the right value in Python (big ints), but the numbers grow to about 43 digits for n = k = 30 (I measured) and larger for bigger inputs. In a fixed-width language the per-step reduction is mandatory.
- Faster: the sum over f is a sliding window of width k over `dp_{j-1}`, so one die costs O(target) instead of O(target * k). The code has that version and it matches on every case.
- Why no `dp[s]` for `s > target`: a partial sum above target can never come back down (faces are positive), so I do not store them.

**Complexity:** Time O(n * target * k) for the plain version, up to 30 * 1000 * 30 = 900000 steps (about 10^6); O(n * target) with the sliding window. Space O(target) for two arrays.

**Dry run (n = 1, k = 6, target = 3, then the table for n = 2):**
- One die: `dp_0 = [1,0,0,0]`; the die adds 1..6 but only sums up to 3 matter: `dp_1 = [0,1,1,1]`. `dp_1[3] = 1`. Matches the prompt.
- n = 2, k = 6, target = 7 (columns are sums 0..7):

| dice | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| 2 | 0 | 0 | 1 | 2 | 3 | 4 | 5 | 6 |

- Row 2, sum 7: `dp_2[7] = dp_1[1] + ... + dp_1[6] = 6` (the six pairs (1,6) ... (6,1)). Row 1, sum 7 is 0 because one six-sided die cannot show 7.
- n = 2, k = 5, target = 1: row 2, sum 1 is 0 (two dice sum to at least 2).

**Code:**
```python
import itertools
import random

random.seed(36)
MOD = 10**9 + 7

def dice(n, k, target):
    """dp[s] = number of ordered outcomes of the dice thrown so far with sum s (s <= target)."""
    dp = [0] * (target + 1)
    dp[0] = 1                                   # zero dice: the empty sequence has sum 0
    for _ in range(n):
        nd = [0] * (target + 1)                 # a NEW array per die: no in-place hazard
        for s in range(target + 1):
            if dp[s]:
                for f in range(1, min(k, target - s) + 1):
                    nd[s + f] = (nd[s + f] + dp[s]) % MOD
        dp = nd
    return dp[target]

def dice_prefix(n, k, target):
    """Same answer in O(n * target) with a sliding window sum instead of the inner loop over faces."""
    dp = [1] + [0] * target
    for _ in range(n):
        nd = [0] * (target + 1)
        window = 0
        for s in range(1, target + 1):
            window += dp[s - 1]
            if s - 1 - k >= 0:
                window -= dp[s - 1 - k]
            nd[s] = window % MOD
            window %= MOD
        dp = nd
    return dp[target]

def brute(n, k, target):
    return sum(1 for r in itertools.product(range(1, k + 1), repeat=n) if sum(r) == target) % MOD

# ---- examples from the prompt
assert dice(1, 6, 3) == 1
assert dice(2, 6, 7) == 6
assert dice(30, 30, 500) == 222616187
assert dice(2, 5, 1) == 0
print('examples ok')

# ---- table for n = 2, k = 6, target = 7 (rows = dice thrown, columns = sums 0..7)
dp = [1] + [0] * 7
print('sum:      ', list(range(8)))
print('0 dice:   ', dp)
for d in (1, 2):
    nd = [0] * 8
    for s in range(8):
        for f in range(1, 7):
            if s + f <= 7:
                nd[s + f] += dp[s]
    dp = nd
    print(f'{d} dice:   ', dp)
assert dp[7] == 6

# ---- seeded cross-check against the enumeration of all k^n outcomes (k^n <= 10^5)
cases = 0
for _ in range(400):
    k = random.randint(1, 8)
    n = random.randint(1, 30)
    while k ** n > 10**5:
        n -= 1
    n = max(n, 1)
    t = random.randint(0, n * k + 3)
    exp = brute(n, k, t)
    assert dice(n, k, t) == exp == dice_prefix(n, k, t), (n, k, t)
    cases += 1
for n in range(1, 6):                      # exhaustive tiny sweep
    for k in range(1, 6):
        for t in range(0, n * k + 3):
            assert dice(n, k, t) == brute(n, k, t) == dice_prefix(n, k, t)
            cases += 1
print('cross-check passed on', cases, 'cases')

# ---- 0 outside n..n*k, and the modulus matters at the full size
assert all(dice(4, 6, t) == 0 for t in list(range(0, 4)) + list(range(25, 40)))
assert all(dice(4, 6, t) > 0 for t in range(4, 25))
assert dice(30, 30, 1000) == 0 and dice(30, 30, 30) == 1 and dice(30, 30, 900) == 1
big = dice(30, 30, 465)
exact = [1] + [0] * 465
for _ in range(30):                          # same DP with Python big ints and no modulus
    nd = [0] * 466
    for t in range(466):
        for f in range(1, 31):
            if t - f >= 0:
                nd[t] += exact[t - f]
    exact = nd
print('n=30, k=30, target=465: mod answer', big, '| exact count has', len(str(exact[465])), 'digits')
assert exact[465] % MOD == big and exact[465] > MOD
assert dice_prefix(30, 30, 465) == big
print('edge cases ok')
```

**Output (my run):**
```
examples ok
sum:       [0, 1, 2, 3, 4, 5, 6, 7]
0 dice:    [1, 0, 0, 0, 0, 0, 0, 0]
1 dice:    [0, 1, 1, 1, 1, 1, 1, 0]
2 dice:    [0, 0, 1, 2, 3, 4, 5, 6]
cross-check passed on 700 cases
n=30, k=30, target=465: mod answer 252370474 | exact count has 43 digits
edge cases ok
```

**Edge cases:**
- `target < n` or `target > n*k`: 0, with no special-case code needed.
- `k = 1`: exactly one outcome, the sum n.
- `target = 0`: 0 (n >= 1).
- Large n, k with the modulus: the exact count has 43 digits for n = k = 30, target 465, so the modulus really does bite.
- Use `[0] * (target + 1)` per die, not `[[0]*...]*...` aliasing (Q31).

**Follow-ups:**
- *Remove the factor k?* Sliding-window or prefix sums, as in the code, O(n * target).
- *Probability instead of a count?* Divide by k^n (use floats, or modular inverse for a modulus).
- *n up to 10^9?* Use the generating function `(x + ... + x^k)^n` with polynomial exponentiation (outside this part).

**Common mistakes:**
- Updating one array in place.
- Forgetting the modulus inside the inner loop (correct in Python but slow and unsafe elsewhere).
- Indexing `new[s + f]` past `target` (IndexError) without a bound.
- Using `dp[0] = 0` as the base, which makes everything 0.

### Q37 ⭐ 🟡 0/1 knapsack: which items (reconstruction with a tie rule). `weights` and `values` have equal length 1 <= len <= 100 (1 <= weight <= 100, 1 <= value <= 1000) and `cap` is 0 <= cap <= 1000. Return `[best, items]`: the maximum value and the list of chosen item indices in ascending order. If several subsets reach the maximum, return the one whose ascending index list is lexicographically smallest (a list that is a prefix of another is smaller). Explain why a 1D table cannot rebuild the items (you need the 2D table, or a bit per item and capacity) and how the table is read backwards. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsets with the same tie rule (len <= 12) on small inputs. Example: weights=[1, 3, 4, 5], values=[1, 4, 5, 7], cap=7 -> [9, [1, 2]]; weights=[5], values=[10], cap=4 -> [0, []]; weights=[2, 2, 3], values=[3, 3, 5], cap=4 -> [6, [0, 1]]; weights=[1, 1, 1], values=[4, 4, 4], cap=2 -> [8, [0, 1]].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** 0/1 knapsack with reconstruction. Value-only needs a 1D array; recovering the items needs the full 2D table (or a bit per item and capacity).

**Say this first (1 line):** "I build `f[i][c]` = best value from items i..n-1 with capacity c, from the right, then walk it left to right taking item i whenever taking it still reaches `f[i][c]`; that gives the lexicographically smallest index list."

**Brute force:** Try all 2^n subsets, keep those within capacity, take the highest value and, among ties, the smallest index list (Python list comparison, where a prefix is smaller). O(2^n * n), n <= 12. It is the oracle.

**Optimal:**
- State: `f[i][c]` = maximum value using only items `i..n-1` with capacity c.
- Base: `f[n][c] = 0` for all c (no items left).
- Transition: `f[i][c] = max(f[i+1][c], values[i] + f[i+1][c - weights[i]])` where the second option exists only if `weights[i] <= c`. Skip or take.
- Answer value: `f[0][cap]`.
- Why from the right: so the walk goes forward through the items, and "the smallest index first" is just "decide item 0 first".
- Reconstruction walk: with `c = cap`, for i from 0: if `f[i][c] == 0` stop (all values are at least 1, so nothing more is worth taking, and stopping gives the shorter prefix); else if `weights[i] <= c` and `values[i] + f[i+1][c - weights[i]] == f[i][c]`, take i and reduce c. Otherwise skip.
- Why the tie rule works: among optimal subsets, the one with the smallest first index takes the first item that can start an optimal set. Taking i when it is feasible for the optimum gives a list starting with i, which beats every list starting with a larger index; the skip branch can only produce lists starting with larger indices. Same argument at every later step.
- Why a 1D table cannot rebuild: `dp[c]` after the last item says only the best value for capacity c. Each cell was overwritten by earlier items, so which item caused it is lost. Choices: keep the 2D table (O(n*cap) memory, here 100 * 1000 = 10^5 cells, fine), or store one bit per (item, capacity) saying whether item i was taken at c (the same size in bits).
- The 1D value-only version has the capacity loop DOWNWARD (`for c in range(cap, w-1, -1)`): `dp[c]` reads `dp[c - w]`, which must still hold the value from before this item. Going upward would reuse the item (unbounded knapsack). The code uses it only to cross-check the value.

**Complexity:** Time O(n * cap) (100 * 1001 about 10^5). Space O(n * cap) for the 2D table; the value alone needs O(cap). The enumeration oracle is O(2^n).

**Dry run (first example):** weights `[1,3,4,5]`, values `[1,4,5,7]`, cap 7. Row i uses items i..3.

| from item \ cap | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 1 | 4 | 5 | 7 | 8 | 9 |
| 1 | 0 | 0 | 0 | 4 | 5 | 7 | 7 | 9 |
| 2 | 0 | 0 | 0 | 0 | 5 | 7 | 7 | 7 |
| 3 | 0 | 0 | 0 | 0 | 0 | 7 | 7 | 7 |
| 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

- Value `f[0][7] = 9`.
- Walk: c = 7. i = 0: take it? `1 + f[1][6] = 1 + 7 = 8`, not 9: skip. i = 1: `4 + f[2][4] = 4 + 5 = 9`, equals `f[1][7] = 9`: take, c = 4. i = 2: `5 + f[3][0] = 5`, equals `f[2][4] = 5`: take, c = 0. i = 3: `f[3][0] = 0`, stop. Items `[1, 2]`, value 9.
- Tie check, third example `[2,2,3]` values `[3,3,5]`, cap 4: items 0 and 1 give 6 and item 2 alone gives 5, so `[0, 1]`.

**Code:**
```python
import itertools
import random

random.seed(37)

def best_1d(weights, values, cap):
    """Value only, O(cap) space. Capacity loop goes DOWNWARD so each item is used at most once."""
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack(weights, values, cap):
    """f[i][c] = best value using items i..n-1 with capacity c. Built from the right so the walk reads left to right."""
    n = len(weights)
    f = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for c in range(cap + 1):
            f[i][c] = f[i + 1][c]                                   # skip item i
            if weights[i] <= c:
                f[i][c] = max(f[i][c], values[i] + f[i + 1][c - weights[i]])   # take item i
    items, c = [], cap
    for i in range(n):
        if f[i][c] == 0:                      # values >= 1: nothing more is worth taking; stop (shorter prefix wins)
            break
        if weights[i] <= c and values[i] + f[i + 1][c - weights[i]] == f[i][c]:
            items.append(i)                   # taking i can still reach the optimum; i is the smallest such index
            c -= weights[i]
    return [f[0][cap], items], f

def brute(weights, values, cap):
    n = len(weights)
    cands = []
    for L in range(n + 1):
        for comb in itertools.combinations(range(n), L):
            if sum(weights[i] for i in comb) <= cap:
                cands.append((sum(values[i] for i in comb), list(comb)))
    mv = max(v for v, _ in cands)
    return [mv, min(c for v, c in cands if v == mv)]       # list comparison: prefix is smaller

def solve(weights, values, cap):
    return knapsack(weights, values, cap)[0]

# ---- examples from the prompt
assert solve([1, 3, 4, 5], [1, 4, 5, 7], 7) == [9, [1, 2]]
assert solve([5], [10], 4) == [0, []]
assert solve([2, 2, 3], [3, 3, 5], 4) == [6, [0, 1]]
assert solve([1, 1, 1], [4, 4, 4], 2) == [8, [0, 1]]
print('examples ok')

# ---- the table of the first example (rows i = items i..n-1 allowed, columns = capacity 0..7)
res, f = knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7)
print('cap       ', list(range(8)))
for i in range(5):
    print(f'from item {i}', f[i])
print('result', res)

# ---- seeded cross-check against the subset enumeration with the same tie rule
cases = 0
for _ in range(600):
    n = random.randint(1, 10)
    ws = [random.randint(1, 6) for _ in range(n)]
    vs = [random.randint(1, 9) for _ in range(n)]
    cap = random.randint(0, 20)
    got = solve(ws, vs, cap)
    assert got == brute(ws, vs, cap), (ws, vs, cap, got)
    assert best_1d(ws, vs, cap) == got[0]
    assert sum(ws[i] for i in got[1]) <= cap and sum(vs[i] for i in got[1]) == got[0]
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- why the 1D table cannot rebuild the items: dp[c] forgets which items made it
dp = [0] * 8
for w, v in zip([1, 3, 4, 5], [1, 4, 5, 7]):
    for c in range(7, w - 1, -1):
        dp[c] = max(dp[c], dp[c - w] + v)
print('1D table after all items:', dp, '-> value', dp[7], 'but nothing says WHICH items')

# ---- edge cases and full size
assert solve([3], [5], 3) == [5, [0]]
assert solve([1, 1], [1, 1], 0) == [0, []]
assert solve([2, 2], [3, 3], 2) == [3, [0]]                  # tie: smallest index list
W = [random.randint(1, 100) for _ in range(100)]
V = [random.randint(1, 1000) for _ in range(100)]
r = solve(W, V, 1000)
assert r[0] == best_1d(W, V, 1000) and sum(W[i] for i in r[1]) <= 1000
print('n = 100, cap = 1000 ok: value', r[0], 'with', len(r[1]), 'items')
```

**Output (my run):**
```
examples ok
cap        [0, 1, 2, 3, 4, 5, 6, 7]
from item 0 [0, 1, 1, 4, 5, 7, 8, 9]
from item 1 [0, 0, 0, 4, 5, 7, 7, 9]
from item 2 [0, 0, 0, 0, 5, 7, 7, 7]
from item 3 [0, 0, 0, 0, 0, 7, 7, 7]
from item 4 [0, 0, 0, 0, 0, 0, 0, 0]
result [9, [1, 2]]
cross-check passed on 600 cases
1D table after all items: [0, 1, 1, 4, 5, 7, 8, 9] -> value 9 but nothing says WHICH items
n = 100, cap = 1000 ok: value 27115 with 42 items
```

**Edge cases:**
- `cap = 0` or every weight above cap: `[0, []]`.
- Ties between equal-value subsets (`[1,1,1]` values 4, cap 2): `[0, 1]`, not `[1, 2]`.
- Exact fit (`weight == cap`) must be allowed (`<=`, not `<`).
- All items fit: every index in ascending order.
- Zero value does not occur (values >= 1); if it could, the stop-at-zero rule would need changing.

**Follow-ups:**
- *Memory-lean reconstruction?* Store one bitmask per capacity (the same information as the 2D table, packed).
- *Unbounded version?* Loop capacity upward, one 1D array (Q20 in this part).
- *Space for value only?* One array with a downward loop, as in `best_1d`.

**Common mistakes:**
- Looping capacity upward in the 1D table (reuses items).
- Building the table from item 0 and walking back, where the tie rule is awkward to get right; building from the right makes it a simple left-to-right scan.
- Not stopping at `f == 0`, then adding useless items that happen to fit.
- Returning item values instead of indices.

### Q38 ⭐ 🟡 Minimum cost for tickets. You will travel on the days listed in `days` (1 <= len <= 365, strictly increasing integers in 1..365). A 1-day pass costs `costs[0]`, a 7-day pass `costs[1]` and a 30-day pass `costs[2]` (1 <= each <= 1000); a d-day pass bought on day t covers days t..t+d-1. Return the minimum total cost to cover every travel day. Define `dp[d]` over calendar days (cost to cover all travel days up to d) and give the transition for travel and non-travel days. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over the next uncovered travel day on small inputs. Example: days=[1, 4, 6, 7, 8, 20], costs=[2, 7, 15] -> 11; days=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], costs=[2, 7, 15] -> 17; days=[5], costs=[3, 2, 1] -> 1; days=[1, 30], costs=[5, 6, 7] -> 7.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D DP over calendar days with "buy a pass that ends today" choices. Think of it as a small unbounded-style cover problem on a line.

**Say this first (1 line):** "`dp[d]` is the cheapest cost to cover every travel day up to day d; a non-travel day copies `dp[d-1]`, and a travel day takes the best of a 1-day, 7-day or 30-day pass ending today, looking back 1, 7 or 30 days (clamped at 0)."

**Brute force:** Recursion over the next uncovered travel day: from travel day `days[i]`, try each pass, skip to the first travel day it does not cover, add its cost. Without a cache it is up to 3^n. With n <= 9 in the cross-check it is fine; with a cache on `i` it becomes O(n) states times 3 choices, the second DP form.

**Optimal:**
- State: `dp[d]` = minimum cost to cover all travel days that are `<= d`, for calendar day d in 0..last travel day.
- Base: `dp[0] = 0`.
- Non-travel day d: `dp[d] = dp[d-1]` (nothing needs covering on d, and any pass that covered up to d-1 is enough).
- Travel day d: `dp[d] = min(dp[d-1] + costs[0], dp[max(0, d-7)] + costs[1], dp[max(0, d-30)] + costs[2])`.
- Why the look-back is right: a pass that covers day d and is bought as late as possible covers `d-d_len+1 .. d`. Everything before that window must be covered by something else, and `dp[d - d_len]` is exactly the cost for everything up to `d - d_len`. The `max(0, ...)` clamp handles windows that start before day 1.
- Why "the pass ends today" is enough: when the pass covering day d is chosen, the days it can usefully cover are those up to d (anything later is handled by later states). Among the passes that cover d, the one that covers the most earlier days is the one ending on d. A pass that really ends later covers the same earlier days, so the DP loses nothing by pretending it ends on d.
- Answer: `dp[last]` where `last = days[-1]`.
- Costs need not be monotone (a 7-day pass may cost more than a 30-day pass). The min over the three options handles that; I tested random costs in 1..12 without forcing order.
- Space: `dp` is O(last) = O(365). A sliding window of 30 values would also do, but 365 is tiny.
- Variant on the days list: the same DP indexed by travel day (`dp[i]` and a pointer for each pass length) is O(n); the calendar form is simpler to explain.

**Complexity:** Time O(last) = O(365) steps, each with three lookups. Space O(last). The recursion oracle is up to O(3^n).

**Dry run (first example):** `days = [1,4,6,7,8,20]`, costs `[2,7,15]`.

| day | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9..19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| travel? | | yes | | | yes | | yes | yes | yes | | yes |
| dp | 0 | 2 | 2 | 2 | 4 | 4 | 6 | 7 | 9 | 9 | 11 |

- Day 1: `min(0+2, 0+7, 0+15) = 2`. Days 2, 3: copy 2. Day 4: `min(2+2, dp[0]+7, dp[0]+15) = 4`. Day 5: copy 4. Day 6: `min(4+2, 0+7, 0+15) = 6`.
- Day 7: `min(6+2 = 8, dp[0]+7 = 7, ...) = 7`: one 7-day pass bought on day 1 covers days 1, 4, 6, 7.
- Day 8: `min(7+2 = 9, dp[1]+7 = 9, dp[0]+15 = 15) = 9`. Days 9..19 copy 9.
- Day 20: `min(9+2 = 11, dp[13]+7 = 16, dp[0]+15 = 15) = 11`. Answer 11.

**Code:**
```python
import random
import sys

random.seed(38)

def min_cost(days, costs):
    """dp[d] = minimum cost to cover every travel day <= d. Calendar days 0..last."""
    travel = set(days)
    last = days[-1]
    dp = [0] * (last + 1)                       # dp[0] = 0: nothing to cover yet
    for d in range(1, last + 1):
        if d not in travel:
            dp[d] = dp[d - 1]                   # a non-travel day costs nothing extra
        else:
            dp[d] = min(dp[d - 1] + costs[0],              # 1-day pass covers d only
                        dp[max(0, d - 7)] + costs[1],      # 7-day pass covers d-6..d
                        dp[max(0, d - 30)] + costs[2])     # 30-day pass covers d-29..d
    return dp[last], dp

def rec(days, costs):
    """Plain recursion over the next uncovered travel day (index into days)."""
    n = len(days)
    def f(i):
        if i >= n:
            return 0
        best = float('inf')
        for span, c in zip((1, 7, 30), costs):
            j = i
            while j < n and days[j] < days[i] + span:    # the pass bought on days[i] covers these
                j += 1
            best = min(best, c + f(j))
        return best
    return f(0)

# ---- examples from the prompt
assert min_cost([1, 4, 6, 7, 8, 20], [2, 7, 15])[0] == 11
assert min_cost([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15])[0] == 17
assert min_cost([5], [3, 2, 1])[0] == 1
assert min_cost([1, 30], [5, 6, 7])[0] == 7
print('examples ok')

# ---- table for the first example
ans, dp = min_cost([1, 4, 6, 7, 8, 20], [2, 7, 15])
print('day :', list(range(len(dp))))
print('dp  :', dp)
print('answer', ans)

# ---- seeded cross-check against the plain recursion
cases = 0
for _ in range(600):
    n = random.randint(1, 9)
    days = sorted(random.sample(range(1, random.choice([10, 40, 80]) + 1), n))
    costs = [random.randint(1, 12) for _ in range(3)]          # not forced to be monotone
    assert min_cost(days, costs)[0] == rec(days, costs), (days, costs)
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- edge cases and full size
assert min_cost([1], [1, 1, 1])[0] == 1
assert min_cost([365], [1000, 1000, 1000])[0] == 1000
full = min_cost(list(range(1, 366)), [2, 7, 15])[0]
print('every day of the year with costs [2, 7, 15]:', full)
assert full == 12 * 15 + 7                                  # twelve 30-day passes (360 days) + one 7-day pass for 5 days
assert min_cost([1, 8, 15], [10, 1, 1])[0] == 1              # one cheap 30-day pass covers all three
assert min_cost([1, 8, 15], [10, 5, 1])[0] == 1
print('edge cases ok')
```

**Output (my run):**
```
examples ok
day : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
dp  : [0, 2, 2, 2, 4, 4, 6, 7, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11]
answer 11
cross-check passed on 600 cases
every day of the year with costs [2, 7, 15]: 187
edge cases ok
```

**Edge cases:**
- One travel day: the cheapest of the three costs (`days=[5]`, costs `[3,2,1]` gives 1: a 30-day pass is the cheapest ticket).
- Look-back below day 1: clamp with `max(0, ...)`, otherwise a negative index silently reads the END of the list.
- Day 365 with the longest pass: no day beyond 365 is needed; the pass just covers extra days.
- Costs not monotone: take the min over all three, do not assume the longer pass is cheaper per day.
- Every day of the year with costs [2,7,15]: twelve 30-day passes (360 days) plus a 7-day pass for the last 5 days, 187 (checked in the code).

**Follow-ups:**
- *Why not greedy (always the cheapest per day)?* The pass cost per day is not enough: partial coverage and gaps matter, and the DP shows 7 beating 2+2+2+2 at day 7.
- *More pass types?* Add another term to the min; time O(last * types).
- *Very large day range?* Index by travel day and use pointers, O(n).

**Common mistakes:**
- `dp[d-7]` with d < 7 (negative index) instead of the clamp.
- Forgetting the non-travel copy case, which makes the min apply to every day and overcounts.
- Reading "7-day pass bought on day t covers t..t+6" and looking back 6 or 8 days; the window ending at d is `d-6..d`, so the look-back is `dp[d-7]`.

### Q39 ⭐ 🔴 Ones and zeroes (a knapsack with two capacities). `strs` is a list of 1 <= len <= 100 non-empty binary strings (each of length <= 100), and `m`, `n` are 0 <= m, n <= 100. Return the size of the largest subset of strings that uses at most m zeros and at most n ones in total. The table has two capacity axes and each string is an item taken at most once, so both loops run downward. This is the concept edge of 2D DP (grids and strings are Part 11); say what the state is, the transition, and the time O(len * m * n). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsets (len <= 12) on small inputs. Example: strs=['10', '0001', '111001', '1', '0'], m=5, n=3 -> 4; strs=['10', '0', '1'], m=1, n=1 -> 2; strs=['0'], m=0, n=5 -> 0.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 0/1 knapsack with TWO capacities (zeros and ones), each string an item of weight `(zeros, ones)` and value 1. This is the concept edge of 2D DP; grids and string DPs are Part 11.

**Say this first (1 line):** "`dp[a][b]` is the most strings I can take using at most a zeros and b ones; for each string I update the table with both loops going downward, so a string is used at most once; time is O(len * m * n)."

**Brute force:** Try all 2^len subsets, keep those whose total zeros are at most m and total ones at most n, return the largest size. O(2^len * total length). len <= 12 in the cross-check.

**Optimal:**
- State: after processing some strings, `dp[a][b]` = the maximum number of those strings that can be chosen with total zeros `<= a` and total ones `<= b`. The table has `(m + 1) x (n + 1)` cells and it is "at most", so `dp[a][b]` is non-decreasing in both a and b.
- Base: all zeros (the empty subset is always allowed).
- Transition for a string with `z` zeros and `o` ones: `dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)` for `a >= z` and `b >= o`. Skip (keep the old value) or take (one more string, paying `z` and `o`).
- Why both loops go downward: `dp[a - z][b - o]` must still be the value from BEFORE this string. In the downward order, cell `(a - z, b - o)` is smaller in both coordinates, so it has not been updated yet for this string. In the upward order it has, and the string is counted again. A string with `z = 0` or `o = 0` makes it obvious: the code shows `['0']`, m = 3, n = 0 gives 3 with the upward loops, but the true answer is 1. The upward version was wrong on 329 of 500 random cases.
- Order of the two loops among themselves does not matter (any order where each inner index goes down is fine), as long as both are downward and the item loop is outermost.
- Same idea as the 1D 0/1 knapsack (Q37 value-only form), one dimension more.
- The state cannot be a single number because two budgets can bind independently; both must be tracked.

**Complexity:** Time O(len * m * n) = up to 100 * 100 * 100 = 10^6 updates. Space O(m * n) = 10^4 cells (the item dimension is rolled away by the downward loops). Counting zeros per string is O(total length).

**Dry run (first example):** strings `10, 0001, 111001, 1, 0`, m = 5 zeros, n = 3 ones. Items as `(zeros, ones)`: `(1,1)`, `(3,1)`, `(2,4)`, `(0,1)`, `(1,0)`.
- `111001` has 4 ones, more than n = 3, so it can never be taken: the table does not change for it (the loop range for b is empty).
- After `10` (1,1): every cell with `a >= 1`, `b >= 1` is 1.
- After `0001` (3,1): cells with `a >= 4`, `b >= 2` become 2 (take both): for example `dp[4][2] = dp[1][1] + 1 = 2`.
- After `1` (0,1): `dp[4][3]` becomes `dp[4][2] + 1 = 3`.
- After `0` (1,0): `dp[5][3] = dp[4][3] + 1 = 4`.
- Answer `dp[5][3] = 4`: take `10`, `0001`, `1`, `0` (zeros 1 + 3 + 0 + 1 = 5, ones 1 + 1 + 1 + 0 = 3). The printed table after each string is in the output below (rows are zeros allowed 0..5, columns ones allowed 0..3).

**Code:**
```python
import itertools
import random

random.seed(39)

def ones_zeroes(strs, m, n):
    """dp[a][b] = largest subset of the strings seen so far using at most a zeros and b ones."""
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        z = s.count('0')
        o = len(s) - z
        for a in range(m, z - 1, -1):              # both loops DOWNWARD: each string is used at most once
            for b in range(n, o - 1, -1):
                dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)
    return dp[m][n]

def upward_bug(strs, m, n):
    """WRONG: upward loops let a string be reused (it behaves like an unbounded item)."""
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        z = s.count('0')
        o = len(s) - z
        for a in range(z, m + 1):
            for b in range(o, n + 1):
                dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)
    return dp[m][n]

def brute(strs, m, n):
    k, best = len(strs), 0
    for mask in range(1 << k):
        ch = [strs[i] for i in range(k) if mask >> i & 1]
        if sum(s.count('0') for s in ch) <= m and sum(s.count('1') for s in ch) <= n:
            best = max(best, len(ch))
    return best

# ---- examples from the prompt
assert ones_zeroes(['10', '0001', '111001', '1', '0'], 5, 3) == 4
assert ones_zeroes(['10', '0', '1'], 1, 1) == 2
assert ones_zeroes(['0'], 0, 5) == 0
print('examples ok')

# ---- table for the first example: dp after each string (rows a = zeros allowed 0..5, columns b = ones allowed 0..3)
strs = ['10', '0001', '111001', '1', '0']
m, n = 5, 3
dp = [[0] * (n + 1) for _ in range(m + 1)]
for s in strs:
    z = s.count('0'); o = len(s) - z
    for a in range(m, z - 1, -1):
        for b in range(n, o - 1, -1):
            dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)
    print(f'after {s!r} (zeros {z}, ones {o}):', dp)
assert dp[m][n] == 4

# ---- seeded cross-check against the enumeration of all subsets (len <= 12)
cases = diff_upward = 0
for _ in range(500):
    k = random.randint(1, 12)
    strs = [''.join(random.choice('01') for _ in range(random.randint(1, 5))) for _ in range(k)]
    m, n = random.randint(0, 8), random.randint(0, 8)
    assert ones_zeroes(strs, m, n) == brute(strs, m, n), (strs, m, n)
    if upward_bug(strs, m, n) != ones_zeroes(strs, m, n):
        diff_upward += 1
    cases += 1
print('cross-check passed on', cases, 'cases; the upward-loop version was wrong on', diff_upward)
print("upward on ['0'], m=3, n=0:", upward_bug(['0'], 3, 0), '(true answer', ones_zeroes(['0'], 3, 0), ')')

# ---- edge cases and full size
assert ones_zeroes(['0'], 0, 5) == 0 and ones_zeroes(['1'], 5, 0) == 0 and ones_zeroes(['01'], 1, 1) == 1
assert ones_zeroes(['0', '0', '0'], 2, 0) == 2
big = [''.join(random.choice('01') for _ in range(random.randint(1, 100))) for _ in range(100)]
print('len = 100, m = n = 100:', ones_zeroes(big, 100, 100))
print('edge cases ok')
```

**Output (my run):**
```
examples ok
after '10' (zeros 1, ones 1): [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1]]
after '0001' (zeros 3, ones 1): [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 2, 2], [0, 1, 2, 2]]
after '111001' (zeros 2, ones 4): [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 2, 2], [0, 1, 2, 2]]
after '1' (zeros 0, ones 1): [[0, 1, 1, 1], [0, 1, 2, 2], [0, 1, 2, 2], [0, 1, 2, 2], [0, 1, 2, 3], [0, 1, 2, 3]]
after '0' (zeros 1, ones 0): [[0, 1, 1, 1], [1, 2, 2, 2], [1, 2, 3, 3], [1, 2, 3, 3], [1, 2, 3, 3], [1, 2, 3, 4]]
cross-check passed on 500 cases; the upward-loop version was wrong on 329
upward on ['0'], m=3, n=0: 3 (true answer 1 )
len = 100, m = n = 100: 20
edge cases ok
```

**Edge cases:**
- A string with more ones than n or more zeros than m can never be taken; the loop range is empty and the table is untouched.
- `m = 0` or `n = 0`: only strings made entirely of the other digit can be taken (`['0']`, m = 0, n = 5 gives 0; with m = 1 it gives 1).
- Identical strings are separate items (`['0','0','0']`, m = 2 gives 2).

**Follow-ups:**
- *Memory?* Already O(m * n); the item dimension is gone.
- *Maximise total length instead of count?* Use value `len(s)` instead of 1.
- *Why is this a Part 11 concept?* Two capacity axes make the table 2D; Part 11 covers grids, strings and intervals, where the table axes are positions rather than budgets.

**Common mistakes:**
- Upward loops on either axis (reuses strings).
- Putting the item loop inside the capacity loops (the table then mixes items; the item loop must be outermost).
- Counting ones as `s.count('1')` and zeros as `len(s) - ones` is fine; mixing the two up swaps m and n.
- Forgetting that `dp` is "at most", so the answer is `dp[m][n]`, not a max over cells.

### Q40 ⭐ 🔴 Russian doll envelopes (LIS with a sort trick). `envelopes` is a list of 0 <= len <= 10^5 pairs [w, h] (1 <= w, h <= 10^9). One envelope fits inside another only if BOTH its width and its height are strictly smaller. Return the maximum number of envelopes in a nesting chain (0 for an empty list). Sort by width ascending and, for equal widths, height DESCENDING, then take the strict LIS of the heights with `bisect_left` (Part 5 Q11); explain why the descending tie-break stops two envelopes of equal width from chaining. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an O(n^2) DP over pairs that checks both dimensions strictly on small inputs. Example: envelopes=[[5, 4], [6, 4], [6, 7], [2, 3]] -> 3; envelopes=[[1, 1], [1, 1], [1, 1]] -> 1; envelopes=[] -> 0; envelopes=[[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]] -> 4.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** A two-dimensional "both strictly smaller" chain reduced to a 1D strict LIS by sorting one dimension. The tie-break on the sorted dimension is the whole trick.

**Say this first (1 line):** "Sort by width ascending and, for equal widths, height DESCENDING, then take the strict LIS of the heights with `bisect_left`; the descending tie-break makes it impossible to pick two envelopes of the same width in one increasing run."

**Brute force:** Sort, then `dp[i]` = longest chain ending at envelope i = 1 + the best `dp[j]` over earlier `j` with BOTH width and height strictly smaller. O(n^2) time, O(n) space. Correct, but 10^10 pair checks at n = 10^5. It is the oracle.

**Optimal:**
- After sorting by width, widths never decrease along the list, so the width condition holds automatically between envelopes with different widths (earlier is smaller or equal). What remains is the height condition and the equal-width exception.
- Take the heights in sorted order and compute the strictly increasing LIS with the patience method (Q7): `tails[k]` is the smallest possible last height of a chain of length k + 1; `bisect_left` finds the position, so an equal height replaces rather than extends.
- Why heights DESCENDING on equal width: two envelopes with the same width cannot nest (width must be strictly smaller). If the equal-width group were sorted ascending by height, say `(4,5)` then `(4,6)`, the heights `5, 6` would form an increasing step and the LIS could use both. Sorted descending, `6` comes before `5`, and no strictly increasing run can take two heights from one descending group, so at most one envelope per width is picked.
- Why that loses nothing: if a chain uses one envelope of width w, any envelope of width w with the same or better height works equally; the LIS picks the best one on its own.
- Counterexample (verified): `[[4,5],[4,6],[6,7],[2,3],[1,1]]`. Ascending tie-break gives heights `1,3,5,6,7` and LIS 5, which is wrong. The true answer is 4 (for example `(1,1),(2,3),(4,5),(6,7)`). Descending gives heights `1,3,6,5,7`, strict LIS 4. On 600 random small inputs the ascending tie-break was wrong 282 times (the exact count varies with the seed).
- Equal envelopes `[[1,1],[1,1],[1,1]]`: same width, so they are in one group and a chain of 1 results. And with `bisect_left`, equal heights from different widths do not chain either (height must be strictly smaller): `[[1,5],[2,5],[3,5]]` gives 1.

**Complexity:** Time O(n log n): the sort is O(n log n) and each of the n heights does one binary search. Space O(n) for the sorted copy and `tails`. For n = 10^5 that is about 1.7 million binary-search steps plus the sort.

**Dry run (first example):** `[[5,4],[6,4],[6,7],[2,3]]`.
- Sort by (width asc, height desc): `[2,3], [5,4], [6,7], [6,4]`. Heights: `3, 4, 7, 4`.

| h | `bisect_left(tails, h)` | action | tails |
|---|---|---|---|
| 3 | 0 | append | [3] |
| 4 | 1 | append | [3, 4] |
| 7 | 2 | append | [3, 4, 7] |
| 4 | 1 | replace the 4 | [3, 4, 7] |

- Answer 3: `[2,3] -> [5,4] -> [6,7]`. The last 4 (width 6) could not extend anything, and it cannot follow `[5,4]` because the height 4 is not strictly larger than 4.

**Code:**
```python
import bisect
import random

random.seed(40)

def lis_strict(heights):
    tails = []
    for h in heights:
        p = bisect.bisect_left(tails, h)       # strict: an equal height replaces, never extends
        if p == len(tails):
            tails.append(h)
        else:
            tails[p] = h
    return len(tails)

def russian_doll(envelopes):
    order = sorted(envelopes, key=lambda e: (e[0], -e[1]))     # width up, height DOWN on equal width
    return lis_strict([h for _, h in order])

def ascending_tiebreak_bug(envelopes):
    order = sorted(envelopes, key=lambda e: (e[0], e[1]))      # WRONG tie-break
    return lis_strict([h for _, h in order])

def brute(envelopes):
    """O(n^2) DP over pairs, checking BOTH dimensions strictly."""
    es = sorted(envelopes)
    n = len(es)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if es[j][0] < es[i][0] and es[j][1] < es[i][1]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp, default=0)

# ---- examples from the prompt
assert russian_doll([[5, 4], [6, 4], [6, 7], [2, 3]]) == 3
assert russian_doll([[1, 1], [1, 1], [1, 1]]) == 1
assert russian_doll([]) == 0
assert russian_doll([[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]]) == 4
print('examples ok')

# ---- walk-through of the first example
env = [[5, 4], [6, 4], [6, 7], [2, 3]]
order = sorted(env, key=lambda e: (e[0], -e[1]))
print('sorted (w asc, h desc):', order)
tails = []
for _, h in order:
    p = bisect.bisect_left(tails, h)
    tails[p:p + 1] = [h]
    print(f'  h={h}: position {p}, tails = {tails}')
print('answer', len(tails))

# ---- why descending: with an ascending tie-break equal widths chain
E2 = [[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]]
print('ascending tie-break on', E2, '->', ascending_tiebreak_bug(E2), '| correct', russian_doll(E2))
assert ascending_tiebreak_bug(E2) == 5 and brute(E2) == 4

# ---- seeded cross-check against the O(n^2) pair DP
cases = bad_asc = 0
for _ in range(600):
    n = random.randint(0, 14)
    es = [[random.randint(1, 6), random.randint(1, 6)] for _ in range(n)]
    got = russian_doll(es)
    assert got == brute(es), es
    if ascending_tiebreak_bug(es) != got:
        bad_asc += 1
    cases += 1
print('cross-check passed on', cases, 'cases; the ascending tie-break was wrong on', bad_asc)

# ---- edge cases and full size
assert russian_doll([[3, 3]]) == 1
assert russian_doll([[1, 5], [1, 6], [1, 7]]) == 1             # same width never nests
assert russian_doll([[1, 5], [2, 5], [3, 5]]) == 1             # same height never nests
assert russian_doll([[i, i] for i in range(1, 101)]) == 100
big = [[random.randint(1, 10**9), random.randint(1, 10**9)] for _ in range(10**5)]
print('n = 10**5 random envelopes, chain length:', russian_doll(big))
print('edge cases ok')
```

**Output (my run):**
```
examples ok
sorted (w asc, h desc): [[2, 3], [5, 4], [6, 7], [6, 4]]
  h=3: position 0, tails = [3]
  h=4: position 1, tails = [3, 4]
  h=7: position 2, tails = [3, 4, 7]
  h=4: position 1, tails = [3, 4, 7]
answer 3
ascending tie-break on [[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]] -> 5 | correct 4
cross-check passed on 600 cases; the ascending tie-break was wrong on 282
n = 10**5 random envelopes, chain length: 611
edge cases ok
```

**Edge cases:**
- Empty list: 0.
- All identical envelopes: 1.
- Same width, many heights: 1 (descending tie-break).
- Same height, many widths: 1 (`bisect_left` replaces equal heights).
- A perfect chain `(i, i)`: n.
- Widths and heights up to 10^9: only comparisons are used.

**Follow-ups:**
- *Recover the actual chain?* Keep predecessor pointers as in Q34; the descending tie-break does not change that.
- *Three dimensions (boxes)?* This sort trick does not extend directly; the usual answer is the O(n^2) DP over sorted triples or a CDQ divide and conquer (beyond this part).
- *Can the sort be by height instead?* Yes, by symmetry.

**Common mistakes:**
- Ascending tie-break on height (counts equal-width envelopes as nesting).
- `bisect_right` for the LIS (counts equal heights as nesting).
- Sorting by width only, leaving the order of equal widths arbitrary.
- Applying the O(n^2) DP at n = 10^5 and timing out.

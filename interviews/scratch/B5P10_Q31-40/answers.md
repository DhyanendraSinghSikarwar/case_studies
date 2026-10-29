### Q31 ⭐ 🟢 The `[[0]*n]*m` aliasing trap. For 1 <= m, n <= 6 build two tables: `bug = [[0]*n]*m` and `ok = [[0 for _ in range(n)] for _ in range(m)]`, apply the assignments `ops` (a list of [r, c, v]; 0 <= r < m, 0 <= c < n) to both with `table[r][c] = v` in order, and return `[bug, ok, distinct_rows_bug, distinct_rows_ok]`, where the last two are the numbers of distinct row objects (by `id`) in each table. Explain, from what `*` does to a list, why one write shows up in every row of `bug`, why `[0]*n` itself is safe (the elements are immutable ints) and what DP bug this creates (all rows alias, so a DP table filled row by row is silently wrong). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a hand-written model of the aliasing on small inputs. Example: m=2, n=3, ops=[[0, 1, 5]] -> [[[0, 5, 0], [0, 5, 0]], [[0, 5, 0], [0, 0, 0]], 1, 2]; m=3, n=2, ops=[[0, 0, 1], [2, 1, 7], [1, 0, 9]] -> [[[9, 7], [9, 7], [9, 7]], [[1, 0], [9, 0], [0, 7]], 1, 3]; m=1, n=1, ops=[] -> [[[0]], [[0]], 1, 1].
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

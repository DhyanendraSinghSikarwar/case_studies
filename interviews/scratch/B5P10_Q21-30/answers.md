### Q21 ⭐⭐ 🟡 Combination sum IV: order matters versus order does not matter. `nums` is a list of 1 <= len <= 10 distinct positive integers (each <= 100) and `target` is 0 <= target <= 2000. Return `[ordered, unordered]`: `ordered` is the number of sequences (so [1, 2] and [2, 1] are different) of numbers from `nums`, reuse allowed, that sum to `target`; `unordered` is the number of multisets with that sum (Q10). Target 0 gives [1, 1]. Python integers are unbounded, so return exact values. Explain how swapping the two loops turns one count into the other, and which loop is outer in each. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a recursion that enumerates every sequence (ordered) and every multiset (unordered), target <= 10 on small inputs. Example: nums=[1, 2, 3], target=4 -> [7, 4]; nums=[9], target=3 -> [0, 0]; nums=[2, 5], target=0 -> [1, 1]; nums=[1, 2], target=6 -> [13, 4].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D counting DP, unbounded knapsack flavour. `dp[t]` counts ways to reach sum `t`. The only thing that changes between "ordered" and "unordered" is which loop is outer.

**Say this first (1 line):** "Same recurrence, two loop orders: target outside and coins inside counts sequences; coins outside and target inside counts multisets."

**Brute force:** Recurse on the remaining sum and enumerate. For sequences: try every coin at every step, record the whole sequence. For multisets: decide per coin how many copies to take (or keep only sorted sequences). Exponential: the ordered count for `[1,2,3]` grows like the tribonacci numbers (it has 530 digits at target 2000), so enumeration only works for target <= 10 or so. That is the oracle, not the answer.

**Optimal:**
- State, ordered: `o[t]` = number of sequences from `nums` (reuse allowed) with sum `t`. Condition on the LAST element: `o[t] = sum(o[t - x] for x in nums if x <= t)`. Base `o[0] = 1` (the empty sequence). Different last elements give different sequences, and the same multiset in a different order is a different sequence, so nothing is merged.
- State, unordered: `u[t]` = number of multisets with sum `t`, using only the coins processed so far. Process coins one at a time: `u[t] += u[t - x]` for `t` from `x` up. Base `u[0] = 1`.
- Why the loop order matters: with the coin loop OUTER, each coin gets a "turn" and is never revisited, so a multiset is built in one fixed order of coin types (all 1s, then all 2s, ...) and counted once. With the target loop OUTER, at every `t` every coin is allowed as the last element, so `1,2` and `2,1` are both reached, and counted twice.
- Which loop is outer: ordered = target outer, coins inner. Unordered = coins outer, target inner.
- Target 0: both are 1 (the empty sequence). Check: `[2, 5]`, target 0 gives `[1, 1]`.
- Exact integers: Python ints are unbounded, so there is no modulo. The ordered count for `[1,2,3]`, target 2000 has 530 digits (printed below). Cost: O(target * len(nums)) big-int additions.

**Complexity:** Time O(target * len(nums)) additions for each count (big ints make each add O(digits), which grows with target; say that if asked). Space O(target). Both can be done in one pass each, no 2D table needed.

**Dry run:** `nums=[1,2,3]`, target 4.
- Ordered, `t=1..4`: `o[1]=o[0]=1`; `o[2]=o[1]+o[0]=2`; `o[3]=o[2]+o[1]+o[0]=4`; `o[4]=o[3]+o[2]+o[1]=7`. Table `[1,1,2,4,7]`.
- Unordered: after coin 1 every cell is 1 (`1+1+1+1`). After coin 2: `[1,1,2,2,3]` (e.g. `u[4] = u[4] + u[2] = 1 + 2`). After coin 3: `[1,1,2,3,4]`. Answer 4: `{1111, 112, 22, 13}`.
- Answer `[7, 4]`. The 7 sequences: 1111, 112, 121, 211, 22, 13, 31. The 3 extra are the re-orderings of `112` (2 more) and `13` (1 more).

**Code:**
```python
import random, sys
from functools import cache

random.seed(21)

def count_both(nums, target):
    """Bottom-up. ordered: target loop OUTER, coin loop inner. unordered: coin loop OUTER, target inner."""
    ordered = [1] + [0] * target
    for t in range(1, target + 1):
        for x in nums:
            if x <= t:
                ordered[t] += ordered[t - x]
    unordered = [1] + [0] * target
    for x in nums:
        for t in range(x, target + 1):
            unordered[t] += unordered[t - x]
    return [ordered[target], unordered[target]]

def swapped(nums, target):
    """The classic swap: each loop order with the other count's name."""
    a = [1] + [0] * target            # coin outer, target inner -> this is the UNORDERED count
    for x in nums:
        for t in range(x, target + 1):
            a[t] += a[t - x]
    b = [1] + [0] * target            # target outer, coin inner -> this is the ORDERED count
    for t in range(1, target + 1):
        for x in nums:
            if x <= t:
                b[t] += b[t - x]
    return a[target], b[target]

def memo_ordered(nums, target):
    @cache
    def f(rem):
        if rem == 0:
            return 1
        return sum(f(rem - x) for x in nums if x <= rem)
    return f(target)

def brute(nums, target):
    """Enumerate every sequence (ordered) and every non-decreasing sequence = multiset (unordered)."""
    seqs = []
    def rec(rem, cur):
        if rem == 0:
            seqs.append(tuple(cur)); return
        for x in nums:
            if x <= rem:
                cur.append(x); rec(rem - x, cur); cur.pop()
    rec(target, [])
    ms = set()
    for s in seqs:
        ms.add(tuple(sorted(s)))        # a multiset is a sorted sequence
    sets2 = []
    sn = sorted(nums)
    def rec2(i, rem, cur):
        if rem == 0:
            sets2.append(tuple(cur)); return
        if i == len(sn): return
        k = 0
        while k * sn[i] <= rem:
            rec2(i + 1, rem - k * sn[i], cur + [sn[i]] * k); k += 1
    rec2(0, target, [])
    assert set(sets2) == ms and len(sets2) == len(ms)   # two independent ways to enumerate multisets agree
    return [len(seqs), len(sets2)]

# examples
for nums, t, exp in [([1, 2, 3], 4, [7, 4]), ([9], 3, [0, 0]), ([2, 5], 0, [1, 1]), ([1, 2], 6, [13, 4])]:
    got = count_both(nums, t); assert got == exp == brute(nums, t), (nums, t, got)
    print('example', nums, t, '->', got)

# hand table for the first example
nums, t = [1, 2, 3], 4
o = [1] + [0] * t
for tt in range(1, t + 1):
    o[tt] = sum(o[tt - x] for x in nums if x <= tt)
print('ordered   t=0..4:', o)
u = [1] + [0] * t
for x in nums:
    for tt in range(x, t + 1):
        u[tt] += u[tt - x]
    print('unordered after coin', x, ':', u)

# seeded cross-check
n_cases = diff = swap_ok = 0
for _ in range(600):
    k = random.randint(1, 4)
    nums = random.sample(range(1, 7), k)
    target = random.randint(0, 10)
    got = count_both(nums, target)
    assert got == brute(nums, target), (nums, target)
    a, b = swapped(nums, target)
    assert (a, b) == (got[1], got[0])     # coin-outer gives unordered, target-outer gives ordered, always
    n_cases += 1; diff += got[0] != got[1]
    swap_ok += got[0] >= got[1]  # ordered count >= unordered count always
print('cross-check cases', n_cases, '| ordered != unordered on', diff, '| ordered >= unordered on', swap_ok)
for _ in range(100):
    nums = random.sample(range(1, 30), random.randint(1, 6)); target = random.randint(0, 120)
    assert count_both(nums, target)[0] == memo_ordered(nums, target)
print('memo (depth <= 120) equals bottom-up on 100 random cases')

# big sizes: bottom-up is fine, memo recursion is not
big = count_both([1, 2, 3], 2000)
print('target 2000, nums [1,2,3]: ordered has', len(str(big[0])), 'digits, unordered =', big[1])
print('limit =', sys.getrecursionlimit())
for n in (500, 2000):
    try:
        v = memo_ordered([1, 2, 3], n); print('memo target', n, 'ok', v == count_both([1, 2, 3], n)[0])
    except RecursionError:
        print('memo target', n, 'RecursionError')
def memo_ok(n):
    try:
        memo_ordered([1, 2, 3], n); return True
    except RecursionError:
        return False
lo, hi = 1, 2000          # largest n that works in a fresh cache (the sum(...) generator costs a second frame per level)
while lo < hi:
    mid = (lo + hi + 1) // 2
    if memo_ok(mid): lo = mid
    else: hi = mid - 1
print('largest target the memo handles at limit 1000 (this layout, called from module level):', lo)
assert count_both([1], 2000) == [1, 1]
assert count_both([100] * 1, 2000) == [1, 1] and count_both([100, 99], 1) == [0, 0]
print('edge asserts passed')
```

**Output (my run):**
```
example [1, 2, 3] 4 -> [7, 4]
example [9] 3 -> [0, 0]
example [2, 5] 0 -> [1, 1]
example [1, 2] 6 -> [13, 4]
ordered   t=0..4: [1, 1, 2, 4, 7]
unordered after coin 1 : [1, 1, 1, 1, 1]
unordered after coin 2 : [1, 1, 2, 2, 3]
unordered after coin 3 : [1, 1, 2, 3, 4]
cross-check cases 600 | ordered != unordered on 220 | ordered >= unordered on 600
memo (depth <= 120) equals bottom-up on 100 random cases
target 2000, nums [1,2,3]: ordered has 530 digits, unordered = 334334
limit = 1000
memo target 500 RecursionError
memo target 2000 RecursionError
largest target the memo handles at limit 1000 (this layout, called from module level): 498
edge asserts passed
```

Reading the output:
- All four examples match both the DP and the enumeration. Ordered count is >= unordered on all 600 cases and strictly larger on 220 of them.
- The swapped loop order gave the other count on all 600 cases: target-outer always equals the ordered count and coin-outer the unordered count.
- The recursion limit result is the honest surprise. At the default limit of 1000, the memoised top-down function failed already at target 500, not only at 2000. The reason: `sum(f(rem - x) for x ...)` runs inside a generator frame, so each level costs two Python frames. The largest target that worked here was 498 (sandbox figure, depends on how deep the caller already is). Moral: the limit hits earlier than the "depth = n" rule of thumb suggests.

**Edge cases:**
- Target 0: `[1, 1]` (empty sequence).
- Target below the smallest coin, or no coin divides into it: `[0, 0]`.
- `nums=[1]`: always `[1, 1]` (one way, any order).
- Large target: exact big ints, no modulo. Do not convert to float.
- Coins larger than `t` must be skipped (`if x <= t`), or `dp[t - x]` indexes negative and silently wraps around in Python. That is a real Python-specific bug.

**Follow-ups:**
- "Return the answer modulo 10^9+7?" Reduce each addition: `o[t] = (o[t] + o[t-x]) % M`. Same loops.
- "How do you count sequences if negatives are allowed?" Infinite counts are possible (a cycle of +1, -1), so you need a bound on length. Then add a length dimension.
- "Why not top-down?" It is correct but needs depth about target (two frames per level here); at target 2000 it raises `RecursionError` at the default limit. Raising the limit is fragile; use the loop.

**Common mistakes:**
- Putting the coin loop outer for the "number of sequences" count. It silently returns the multiset count. Example `[1,2,3]`, 4 gives 4 instead of 7.
- Forgetting `o[0] = 1`, so every count is 0.
- No `x <= t` guard (negative index wraps around).
- Memoising with a `sum(generator)` and assuming the recursion depth is just `target`.

### Q22 ⭐⭐ 🟡 Maximum subarray with its position (reconstruction with a tie rule). `nums` has 1 <= len <= 10^5 integers (|value| <= 10^4). Return `[best, l, r]` where `best` is the largest sum of a non-empty contiguous subarray and nums[l..r] (inclusive, 0-indexed) is the subarray achieving it; when several subarrays reach the maximum, return the one with the smallest l, and among those the smallest r. Say how you carry the start index through Kadane, and why 'restart when the running sum is negative' needs care on ties (a running sum of exactly 0). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an O(n^2) enumeration of every subarray with the same tie rule, plus an exhaustive check over every list of length <= 6 with values in -2..2 on small inputs. Example: nums=[-2, 1, -3, 4, -1, 2, 1, -5, 4] -> [6, 3, 6]; nums=[0, 0, 0] -> [0, 0, 0]; nums=[3, -3, 3] -> [3, 0, 0]; nums=[-5, -2, -9] -> [-2, 1, 1]; nums=[2, -2, 2, -2, 5] -> [5, 0, 4].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D DP, "best subarray ending at i" (Kadane), plus reconstruction by carrying the start index.

**Say this first (1 line):** "`run` is the best sum of a subarray ending here; I extend it unless it is strictly negative, and I carry its start index so I can report `[best, l, r]`."

**Brute force:** Try every `(l, r)` with a running sum, keep the best by key `(-sum, l, r)`. O(n^2) time, O(1) space. Fine at n = 10^4, too slow at 10^5. This is the oracle.

**Optimal:**
- State: `run[i]` = largest sum of a non-empty subarray that ends exactly at `i`. Transition: `run[i] = max(nums[i], run[i-1] + nums[i])`. Base: `run[0] = nums[0]`. Answer: `max(run)`.
- Why only the previous value matters: any subarray ending at `i` is either just `nums[i]` or a subarray ending at `i-1` plus `nums[i]`. The best of the second kind uses the best `run[i-1]`.
- Space: only the last `run` is needed, so O(1).
- Carrying the start: keep `start[i]`. If we restart, `start = i`; if we extend, `start` stays. Keep `(best, l, r)` and update whenever `run > best`.
- The tie care, exactly: when `run[i-1] == 0`, extending and restarting give the same sum, but extending keeps the SMALLER start. The rule wants the smallest `l`, so restart only when `run[i-1] < 0` (strictly). Restarting on `<= 0` is wrong.
- Why updating only on a strictly greater sum then also gives the smallest `r` for the chosen `l`: the first time the best is reached we freeze `r`.
- Do we also need an "equal sum but smaller l" update? Argue it is never needed: suppose an earlier candidate `(l', r')` ties the global maximum with `l' > L` and `r' < R`, where `(L, R)` is the answer. Then `S(L..r') = S(L..l'-1) + best <= best`, and `S(l'..R) = best - S(L..l'-1) <= best`, so `S(L..l'-1) = 0` and `(L, r')` is also optimal with `r' < R`, contradicting the smallest `r` for `L`. My code has the extra check as a flag and the exhaustive test shows the plain `>` rule alone gives the same answers (count 0 wrong), so the claim holds on the tested range.
- All-negative lists: `run` restarts every time, so the answer is the largest single element (examples: `[-5,-2,-9] -> [-2,1,1]`). Do not initialise `best = 0`; that would allow an empty subarray.

**Complexity:** Time O(n), space O(1). It is already a loop, so there is no recursion limit issue at n = 10^5. (A memoised "best ending at i" recursion would nest n deep and raise `RecursionError` at the default limit of 1000, so loop.)

**Dry run:** `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` (table printed below).
- i=0: restart, run -2, start 0, best -2 at [0,0].
- i=1: previous run -2 < 0 so restart: run 1, start 1, best 1 [1,1].
- i=2: run 1-3 = -2, start 1; best stays.
- i=3: previous -2 < 0 so restart: run 4, start 3, best 4 [3,3].
- i=4..6: run 3, 5, 6, start 3; best 6 [3,6].
- i=7,8: run 1, 5; no improvement. Answer `[6, 3, 6]`.

**Code:**
```python
import random, itertools

random.seed(22)

def kadane_pos(nums, restart_on_zero=False, update_on_smaller_l=True):
    """Kadane with the start index carried. Returns [best, l, r] with the tie rule smallest l, then smallest r.
    run = best sum of a subarray ENDING at i, start = its leftmost start."""
    best, bl, br = None, 0, 0
    run, start = 0, 0
    for i, x in enumerate(nums):
        if i == 0 or run < 0 or (restart_on_zero and run == 0):
            run, start = x, i            # restart: the old prefix cannot help (strictly hurts)
        else:
            run += x                     # run == 0 keeps the older start: same sum, smaller l
        if best is None or run > best or (update_on_smaller_l and run == best and start < bl):
            best, bl, br = run, start, i
    return [best, bl, br]

def brute(nums):
    """O(n^2): every subarray, key = (-sum, l, r)."""
    n = len(nums); cand = []
    for l in range(n):
        s = 0
        for r in range(l, n):
            s += nums[r]; cand.append((-s, l, r))
    s, l, r = min(cand)
    return [-s, l, r]

for nums, exp in [([-2, 1, -3, 4, -1, 2, 1, -5, 4], [6, 3, 6]), ([0, 0, 0], [0, 0, 0]), ([3, -3, 3], [3, 0, 0]),
                  ([-5, -2, -9], [-2, 1, 1]), ([2, -2, 2, -2, 5], [5, 0, 4])]:
    assert kadane_pos(nums) == brute(nums) == exp, nums
    print('example', nums, '->', exp)

# hand table, first example
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
run, start, best = 0, 0, None
print('i  x  run start best[l,r]')
bl = br = 0
for i, x in enumerate(nums):
    if i == 0 or run < 0: run, start = x, i
    else: run += x
    if best is None or run > best or (run == best and start < bl): best, bl, br = run, start, i
    print(f'{i}  {x:2d}  {run:3d}  {start:3d}   {best} [{bl},{br}]')

# exhaustive: all lists of length 1..6 over -2..2
total = bad_zero = bad_strict = bad_main = 0
for n in range(1, 7):
    for t in itertools.product(range(-2, 3), repeat=n):
        l = list(t); want = brute(l); total += 1
        bad_main += kadane_pos(l) != want
        bad_zero += kadane_pos(l, restart_on_zero=True) != want
        bad_strict += kadane_pos(l, update_on_smaller_l=False) != want
print('exhaustive lists checked:', total)
print('main version wrong on', bad_main)
print('restart when run <= 0 wrong on', bad_zero)
print('update only on strictly greater sum (no smaller-l check) wrong on', bad_strict)
assert bad_main == 0 and total == 19530

# seeded random cross-check, longer lists
for _ in range(500):
    n = random.randint(1, 40); l = [random.randint(-6, 6) for _ in range(n)]
    assert kadane_pos(l) == brute(l)
print('500 random lists (len <= 40) agree with the O(n^2) enumeration')

# max size, runs in one pass
big = [random.randint(-10**4, 10**4) for _ in range(10**5)]
b = kadane_pos(big)
P = 0; s = sum(big[b[1]:b[2] + 1]); assert s == b[0]
print('n = 10^5 result', b)
assert kadane_pos([7]) == [7, 0, 0] and kadane_pos([-3]) == [-3, 0, 0]
print('edge asserts passed')
```

**Output (my run):**
```
example [-2, 1, -3, 4, -1, 2, 1, -5, 4] -> [6, 3, 6]
example [0, 0, 0] -> [0, 0, 0]
example [3, -3, 3] -> [3, 0, 0]
example [-5, -2, -9] -> [-2, 1, 1]
example [2, -2, 2, -2, 5] -> [5, 0, 4]
i  x  run start best[l,r]
0  -2   -2    0   -2 [0,0]
1   1    1    1   1 [1,1]
2  -3   -2    1   1 [1,1]
3   4    4    3   4 [3,3]
4  -1    3    3   4 [3,3]
5   2    5    3   5 [3,5]
6   1    6    3   6 [3,6]
7  -5    1    3   6 [3,6]
8   4    5    3   6 [3,6]
exhaustive lists checked: 19530
main version wrong on 0
restart when run <= 0 wrong on 4503
update only on strictly greater sum (no smaller-l check) wrong on 0
500 random lists (len <= 40) agree with the O(n^2) enumeration
n = 10^5 result [2992853, 12608, 74008]
edge asserts passed
```

Reading the output:
- The "restart when run <= 0" variant is wrong on 4503 of the 19530 lists (it gives a larger `l`); the claim in the prompt is correct.
- The plain `>` rule without the smaller-`l` check is also right on all 19530 lists, matching the argument above.

**Edge cases:**
- All negative: single largest element, `l == r`.
- All zeros: `[0, 0, 0]` (first position wins both ties).
- Zero running sum in the middle (`[3,-3,3] -> [3,0,0]`): extending to index 2 ties at 3, but `r` stays 0 because we update only on strictly greater.
- Single element.
- n = 10^5: values up to 10^4 give sums up to 10^9, no overflow in Python.

**Follow-ups:**
- "Return all optimal subarrays?" Keep a list and reset it when a strictly larger sum appears; with ties you need the prefix-min formulation (`best ending at r = P[r+1] - min P[l]`), tracking every minimising index.
- "Maximum product subarray?" Track both max and min ending here, because a negative flips them.
- "Circular?" See Q26.

**Common mistakes:**
- `best = 0` initial value (empty subarray) on all-negative input.
- Restarting when `run <= 0`, which moves `l` to the right on ties.
- Updating `(l, r)` on `>=`, which moves `r` to the right on ties.
- Resetting `start` on every step instead of only on restart.

### Q23 ⭐⭐ 🟡 Coin change with the coins themselves (reconstruction with a tie rule). `coins` has 1 <= len <= 8 distinct positive integers (each <= 100) and `amount` is 0 <= amount <= 1000. Return the list of coins (in non-decreasing order, repeats listed) of a minimum-size multiset summing to `amount`; if several minimum-size multisets exist return the lexicographically smallest list; return [] for amount 0 and null (None) if the amount cannot be made. Explain how to rebuild the answer from the `dp` table (which coin was used last) and how to follow the tie rule, and why storing a parent pointer per amount gives some optimal answer but not necessarily this one unless you choose carefully. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all multisets with the same tie rule (amount <= 15) on small inputs. Example: coins=[1, 2, 5], amount=11 -> [1, 5, 5]; coins=[2], amount=3 -> null; coins=[3, 5], amount=0 -> []; coins=[1, 3, 4], amount=6 -> [3, 3]; coins=[2, 3], amount=7 -> [2, 2, 3].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** 1D DP, unbounded knapsack (minimise count), with reconstruction under a tie rule.

**Say this first (1 line):** "`dp[a]` is the fewest coins for amount `a`; to get the coins I walk back from `amount` and, at each step, take the smallest coin `c` with `dp[a-c] == dp[a]-1`."

**Brute force:** Enumerate every multiset: for each coin (in sorted order) choose how many copies, keep those with sum `amount`, then take the minimum size and, among those, the lexicographically smallest list. Exponential, fine for amount <= 15. This is the oracle.

**Optimal:**
- State: `dp[a]` = minimum number of coins summing to `a`, or infinity. Base: `dp[0] = 0`. Transition on the last coin: `dp[a] = min(dp[a - c] + 1)` over coins `c <= a`.
- Answer exists iff `dp[amount]` is finite; otherwise return `None`. Amount 0 gives `[]`.
- Rebuild: from `a = amount`, scan coins in ascending order and take the first `c <= a` with `dp[a - c] == dp[a] - 1`. Append it, set `a -= c`, repeat.
- Why this follows the tie rule: the output list is sorted, so its first element is the smallest coin in the multiset. If the smallest coin of some optimal multiset is `m`, then `dp[a - m] == dp[a] - 1`, so `m` is a candidate; the smallest candidate `c` therefore satisfies `c <= m`. And `c` is actually usable as the smallest member: if the optimal rest for `a - c` contained a coin `d < c`, then removing `d` from `{c} + rest` leaves a multiset for `a - d` of size `dp[a] - 1`, so `d` is a smaller candidate, contradicting that `c` was the smallest candidate. So `c` is the smallest possible first element, and the argument repeats on `a - c` (coins taken later are always >= `c`, so the list comes out non-decreasing). Check: the code asserts the output is sorted.
- Why a parent pointer is not enough by itself: `par[a]` stores the coin that first achieved `dp[a]` in the loop order. If you loop coins in the INPUT order, you get some optimal answer but not necessarily the lexicographically smallest. In the run below that differs from the rule on 38 of 2000 cases (e.g. coins `[4,6,5,3]`, amount 9: parent pointer gives `[4,5]`, the rule gives `[3,6]`). Looping coins in ascending order with strict `<` is the same as the rebuild above and matched on all 2000 cases (it picks the smallest coin attaining the minimum). Looping descending differed on 3 of 2000.

**Complexity:** Time O(amount * len(coins)) for the table, O(amount) for the rebuild (each step removes at least 1). Space O(amount). Top-down memoised recursion needs depth up to `amount / min(coin)`; with coin 1 and amount 1000 that is about 1000 frames and it raises `RecursionError` at the default limit (shown below). Bottom-up avoids that.

**Dry run:** `coins=[1,2,5]`, amount 11.
- `dp[0..11] = [0,1,1,2,2,1,2,2,3,3,2,3]` (e.g. `dp[7] = dp[2]+1 = 2` via coin 5).
- Rebuild: `a=11`, `dp=3`: coin 1: `dp[10]=2 == 2`, take 1. `a=10`, `dp=2`: coin 1: `dp[9]=3` no; coin 2: `dp[8]=3` no; coin 5: `dp[5]=1` yes, take 5. `a=5`: coin 1: `dp[4]=2` no; coin 2: `dp[3]=2` no; coin 5: `dp[0]=0` yes, take 5. Result `[1,5,5]`.

**Code:**
```python
import random, sys
from functools import cache

random.seed(23)
INF = float('inf')

def min_table(coins, amount):
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp

def coin_list(coins, amount):
    """Bottom-up table, then rebuild: at each amount take the SMALLEST coin c with dp[a-c] == dp[a]-1."""
    dp = min_table(coins, amount)
    if dp[amount] == INF:
        return None
    out, a = [], amount
    cs = sorted(coins)
    while a:
        for c in cs:
            if c <= a and dp[a - c] == dp[a] - 1:
                out.append(c); a -= c
                break
    return out                      # already non-decreasing (argued in the text, asserted below)

def naive_parent(coins, amount, order='input'):
    """Plain parent pointer: remember the first coin (in the given loop order) that achieves dp[a], rebuild, sort."""
    dp = [0] + [INF] * amount
    par = [0] * (amount + 1)
    cs = {'input': list(coins), 'asc': sorted(coins), 'desc': sorted(coins, reverse=True)}[order]
    for a in range(1, amount + 1):
        for c in cs:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1; par[a] = c
    if dp[amount] == INF:
        return None
    out, a = [], amount
    while a:
        out.append(par[a]); a -= par[a]
    return sorted(out)

def memo_len(coins, amount):
    @cache
    def f(a):
        if a == 0: return 0
        best = INF
        for c in coins:
            if c <= a:
                best = min(best, f(a - c) + 1)
        return best
    return f(amount)

def brute(coins, amount):
    """Enumerate every multiset with sum amount (k copies of each coin), pick min size then lexicographically smallest."""
    cs = sorted(coins); found = []
    def rec(i, rem, cur):
        if rem == 0:
            found.append(list(cur)); return
        if i == len(cs): return
        k = 0
        while k * cs[i] <= rem:
            rec(i + 1, rem - k * cs[i], cur + [cs[i]] * k); k += 1
    rec(0, amount, [])
    if not found: return None
    m = min(map(len, found))
    return min(f for f in found if len(f) == m)

for coins, amt, exp in [([1, 2, 5], 11, [1, 5, 5]), ([2], 3, None), ([3, 5], 0, []), ([1, 3, 4], 6, [3, 3]), ([2, 3], 7, [2, 2, 3])]:
    got = coin_list(coins, amt); assert got == brute(coins, amt) == exp, (coins, amt, got)
    print('example', coins, amt, '->', got)

# hand table for the first example
dp = min_table([1, 2, 5], 11)
print('dp[0..11] =', dp)
a, steps = 11, []
while a:
    for c in [1, 2, 5]:
        if c <= a and dp[a - c] == dp[a] - 1:
            steps.append((a, c)); a -= c; break
print('rebuild (amount, coin taken):', steps)

# seeded cross-check, amount <= 15
n = mism_in = mism_asc = mism_desc = none_cnt = 0
ex = None
for _ in range(2000):
    coins = random.sample(range(1, 10), random.randint(2, 4)); amt = random.randint(0, 15)
    got = coin_list(coins, amt); want = brute(coins, amt)
    assert got == want, (coins, amt, got, want)
    if got is not None: assert got == sorted(got)
    n += 1; none_cnt += got is None
    for key in ('input', 'asc', 'desc'):
        bad = naive_parent(coins, amt, key) != want
        if key == 'input':
            mism_in += bad
            if bad and ex is None: ex = (coins, amt)
        elif key == 'asc': mism_asc += bad
        else: mism_desc += bad
print('cross-check cases', n, '(of which unreachable:', none_cnt, ')')
print('naive parent pointer, coins looped in INPUT order, differs from the tie rule on', mism_in)
print('naive parent pointer, coins looped ascending, differs on', mism_asc)
print('naive parent pointer, coins looped descending, differs on', mism_desc)
print('example of a miss (input order):', ex, 'naive', naive_parent(ex[0], ex[1]), 'rule', brute(*ex))

# memo version agrees on small, recursion limit at large
for _ in range(100):
    coins = random.sample(range(1, 20), random.randint(1, 5)); amt = random.randint(0, 60)
    d = min_table(coins, amt)[amt]
    assert memo_len(coins, amt) == d
big = coin_list([1, 5, 10, 25, 100], 1000)
print('amount 1000, coins [1,5,10,25,100] ->', big, 'size', len(big))
assert sum(big) == 1000
print('limit =', sys.getrecursionlimit())
try:
    memo_len([1, 7], 1000); print('memo amount 1000 ok')
except RecursionError:
    print('memo amount 1000 with coin 1: RecursionError')
assert coin_list([1], 1000) == [1] * 1000
assert coin_list([7, 3], 2) is None and coin_list([4, 6], 0) == []
print('edge asserts passed')
```

**Output (my run):**
```
example [1, 2, 5] 11 -> [1, 5, 5]
example [2] 3 -> None
example [3, 5] 0 -> []
example [1, 3, 4] 6 -> [3, 3]
example [2, 3] 7 -> [2, 2, 3]
dp[0..11] = [0, 1, 1, 2, 2, 1, 2, 2, 3, 3, 2, 3]
rebuild (amount, coin taken): [(11, 1), (10, 5), (5, 5)]
cross-check cases 2000 (of which unreachable: 471 )
naive parent pointer, coins looped in INPUT order, differs from the tie rule on 38
naive parent pointer, coins looped ascending, differs on 0
naive parent pointer, coins looped descending, differs on 3
example of a miss (input order): ([4, 6, 5, 3], 9) naive [4, 5] rule [3, 6]
amount 1000, coins [1,5,10,25,100] -> [100, 100, 100, 100, 100, 100, 100, 100, 100, 100] size 10
limit = 1000
memo amount 1000 with coin 1: RecursionError
edge asserts passed
```

**Edge cases:**
- Amount 0: `[]` (not `None`). Unreachable (e.g. `[2]`, 3): `None`.
- Compare to infinity before using `dp[amount]`; a float `inf` or a large sentinel both work, but do not return `-1` here, the prompt says `None`.
- A coin of 1 makes everything reachable.
- Amount 1000 with coin 1 and nothing else: a list of 1000 ones.
- Coins arrive unsorted: sort them before rebuilding (the table does not care).

**Follow-ups:**
- "Count the ways instead?" Coins outer, amount inner (Q10).
- "Why does greedy fail?" Coins `[1,3,4]`, amount 6: greedy takes 4+1+1 (three coins) but 3+3 uses two (Part 8 Q33).
- "Memory for reconstruction?" Storing a coin per amount (`par`) is O(amount) too; the rebuild from `dp` alone costs a coin scan per step but no extra array.

**Common mistakes:**
- Taking the last-found coin (`<=` instead of `<`, or input order) and getting a different optimal multiset.
- Forgetting to sort the output or the coin order, so the list is not non-decreasing.
- `dp` initialised to 0 instead of infinity, so unreachable amounts look free.
- Returning `[]` for unreachable and `None` for 0: swapped.

### Q24 ⭐⭐ 🟡 Jump game as DP versus greedy. `nums` has 1 <= len <= 10^4 non-negative integers; from index i you may jump to any index in i+1..i+nums[i] (clipped at the last index). Return `[can_reach_end, reachable_count]`: whether index len-1 is reachable from index 0, and how many indices (index 0 included) are reachable from 0. Write the DP first (`reach[j]` is True if some reachable i < j has i + nums[i] >= j; O(n^2)), then show the O(n) furthest-reach version and the fact that the reachable set is always a prefix of the indices, which is why the greedy works; the greedy O(n) solution itself is Part 8 Q12 and the minimum-jumps version Part 8 Q13. A DP over jumps of at most k with a monotonic deque is Part 4 Q35. Your submitted solution must be O(n). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a graph search over indices (a stack of reachable indices) and your own O(n^2) DP on small inputs. Example: nums=[2, 3, 1, 1, 4] -> [True, 5]; nums=[3, 2, 1, 0, 4] -> [False, 4]; nums=[0] -> [True, 1]; nums=[1, 0, 5] -> [False, 2]; nums=[2, 0, 0] -> [True, 3].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D reachability DP that collapses to a greedy "furthest reach" scan.

**Say this first (1 line):** "`reach[j]` is true if some reachable `i < j` can hop that far; because everything between a reachable index and its furthest hop is also reachable, I only need to track the single furthest reachable index `R`."

**Brute force:** Graph search over indices: an edge from `i` to every `j` in `i+1..i+nums[i]`; DFS with a stack and a `seen` set from index 0. O(n^2) worst case (each node scans up to `nums[i]` neighbours). That is one oracle; the O(n^2) DP below is the second.

**Optimal:**
- DP definition: `reach[j]` = True if index `j` can be reached from 0. Base `reach[0] = True`. Transition: `reach[j] = any(reach[i] and i + nums[i] >= j for i < j)`. That is O(n^2) time, O(n) space. Answers: `reach[n-1]` and `sum(reach)`.
- Key fact: the reachable set is always a prefix `0..R`. Proof: if `i` is reachable and `nums[i] = k`, every index in `i+1..i+k` is reachable, so there is no gap between a reachable index and the furthest hop taken from it. By induction the set is `{0..R}` where `R` is the largest `i + nums[i]` over reachable `i` (clipped to `n-1`). I tested this on every list of length <= 6 with values 0..3 (5460 lists): the prefix property held on all of them.
- Therefore replace the whole table with one number: scan `i = 0, 1, ...` while `i <= R`; update `R = max(R, i + nums[i])`. Stuck when `i > R`.
- Answers: `can_reach_end = R >= n-1`, `reachable_count = min(R, n-1) + 1`.
- This is the DP with its inner loop collapsed by the prefix property. The greedy solution on its own is Part 8 Q12, the minimum number of jumps is Part 8 Q13, and a DP over jumps of at most `k` with a monotonic deque is Part 4 Q35.

**Complexity:** Time O(n), space O(1). The O(n^2) DP is only used as an oracle. A memoised `can_reach(i)` recursion could nest n = 10^4 deep and raise `RecursionError` at the default limit of 1000, but the loop never recurses.

**Dry run:** `[2,3,1,1,4]`.
- DP table `reach = [T,T,T,T,T]`: `reach[1]` from index 0 (0+2 >= 1), `reach[2]` from 0, `reach[3]` from 1 (1+3 >= 3), `reach[4]` from 1 (1+3 >= 4).
- Greedy: i=0: `R = 2`; i=1: `R = 4`; i=2,3: no change; i=4: `R = 8`, loop ends. `R >= 4` so True, count `min(8, 4) + 1 = 5`.
- `[3,2,1,0,4]`: `R` becomes 3 at i=0 and stays 3. At i=4, `i > R`, stuck: `[False, 4]` (indices 0..3 reachable, the zero at index 3 is the trap).

**Code:**
```python
import random, itertools, sys

random.seed(24)

def dp_reach(nums):
    """O(n^2) DP: reach[j] is True if some reachable i < j has i + nums[i] >= j."""
    n = len(nums); reach = [False] * n; reach[0] = True
    for j in range(1, n):
        reach[j] = any(reach[i] and i + nums[i] >= j for i in range(j))
    return reach

def solve(nums):
    """O(n): furthest reach R. Everything up to R is reachable (prefix), so count = min(R, n-1) + 1."""
    n = len(nums); R = 0; i = 0
    while i <= R and i < n:
        R = max(R, i + nums[i]); i += 1
    return [R >= n - 1, min(R, n - 1) + 1]

def graph_search(nums):
    n = len(nums); seen = {0}; stack = [0]
    while stack:
        i = stack.pop()
        for j in range(i + 1, min(n - 1, i + nums[i]) + 1):
            if j not in seen:
                seen.add(j); stack.append(j)
    return [n - 1 in seen, len(seen)]

def from_dp(nums):
    r = dp_reach(nums); return [r[-1], sum(r)]

for nums, exp in [([2, 3, 1, 1, 4], [True, 5]), ([3, 2, 1, 0, 4], [False, 4]), ([0], [True, 1]), ([1, 0, 5], [False, 2]), ([2, 0, 0], [True, 3])]:
    assert solve(nums) == graph_search(nums) == from_dp(nums) == exp, nums
    print('example', nums, '->', exp)

# walk-through on the first example
nums = [2, 3, 1, 1, 4]
print('DP table reach[j] for', nums, '=', dp_reach(nums))
R = 0
for i, x in enumerate(nums):
    if i > R: break
    R = max(R, i + x); print(f'greedy i={i} nums[i]={x} -> furthest R={R}')
print('answer', solve(nums))
nums = [3, 2, 1, 0, 4]; R = 0
for i, x in enumerate(nums):
    if i > R: print(f'greedy i={i}: i > R={R}, stuck'); break
    R = max(R, i + x); print(f'greedy i={i} nums[i]={x} -> furthest R={R}')

# claim: the reachable set is a prefix of the indices; exhaustive, length <= 6, values 0..3
cnt = 0
for n in range(1, 7):
    for t in itertools.product(range(4), repeat=n):
        l = list(t); r = dp_reach(l)
        k = sum(r)
        assert r == [True] * k + [False] * (n - k), l           # prefix
        assert solve(l) == graph_search(l) == [r[-1], k], l
        cnt += 1
print('exhaustive lists (len <= 6, values 0..3):', cnt, '- reachable set is a prefix on all, greedy = DP = graph search on all')

# seeded random cross-check
for _ in range(600):
    n = random.randint(1, 14); l = [random.choice([0, 0, 1, 1, 2, 3, 5]) for _ in range(n)]
    assert solve(l) == graph_search(l) == from_dp(l), l
print('600 seeded random lists: O(n) == graph search == O(n^2) DP')

# max size (O(n) only)
big = [random.randint(1, 3) for _ in range(10**4)]
print('n = 10^4 result', solve(big))
assert solve([0]) == [True, 1] and solve([1]) == [True, 1] and solve([0, 5]) == [False, 1] and solve([100, 0, 0]) == [True, 3]
print('limit', sys.getrecursionlimit(), '- top-down reach(j) recursion would be up to n = 10^4 deep, so loop')
print('edge asserts passed')
```

**Output (my run):**
```
example [2, 3, 1, 1, 4] -> [True, 5]
example [3, 2, 1, 0, 4] -> [False, 4]
example [0] -> [True, 1]
example [1, 0, 5] -> [False, 2]
example [2, 0, 0] -> [True, 3]
DP table reach[j] for [2, 3, 1, 1, 4] = [True, True, True, True, True]
greedy i=0 nums[i]=2 -> furthest R=2
greedy i=1 nums[i]=3 -> furthest R=4
greedy i=2 nums[i]=1 -> furthest R=4
greedy i=3 nums[i]=1 -> furthest R=4
greedy i=4 nums[i]=4 -> furthest R=8
answer [True, 5]
greedy i=0 nums[i]=3 -> furthest R=3
greedy i=1 nums[i]=2 -> furthest R=3
greedy i=2 nums[i]=1 -> furthest R=3
greedy i=3 nums[i]=0 -> furthest R=3
greedy i=4: i > R=3, stuck
exhaustive lists (len <= 6, values 0..3): 5460 - reachable set is a prefix on all, greedy = DP = graph search on all
600 seeded random lists: O(n) == graph search == O(n^2) DP
n = 10^4 result [True, 10000]
limit 1000 - top-down reach(j) recursion would be up to n = 10^4 deep, so loop
edge asserts passed
```

**Edge cases:**
- `[0]`: already at the end, `[True, 1]`.
- Zero at the start with `n > 1`: `[False, 1]`.
- A huge `nums[i]` is clipped by `min(R, n-1)`; count is not `R + 1`.
- `[1, 0, 5]`: reaches index 1 and stops at the zero: `[False, 2]` (the 5 is unreachable, it does not help).
- Loop condition is `i <= R and i < n`: stop when stuck (`i > R`) or off the end. Do not stop early when `R >= n-1` and then forget that `R` may exceed `n-1` (clip it).

**Follow-ups:**
- "Minimum jumps?" BFS by levels or greedy window (Part 8 Q13).
- "Jumps of at most k with weights/maximise score?" DP plus a monotonic deque (Part 4 Q35).
- "Why can the prefix property fail in other problems?" If you may only jump exactly `nums[i]`, reachable indices have gaps, and the greedy no longer works; use DP or BFS.

**Common mistakes:**
- Treating `nums[i]` as an exact jump length.
- Counting reachable indices as `R + 1` without clipping to `n`.
- Running the O(n^2) DP at n = 10^4 as the submission (the prompt requires O(n)).

### Q25 ⭐⭐ 🟡 Best time to buy and sell stock with a cooldown. `prices` has 0 <= len <= 5000 non-negative integers (price on each day, <= 1000). You may make as many transactions as you like (hold at most one share, buy again only after selling), but after you sell you cannot buy the next day. Return the maximum profit (0 for an empty list). Define the three states holding, just-sold and free-to-buy, give the transitions per day, and say what changes if you drop the cooldown (the three states collapse to two, and the problem becomes unlimited transactions, a variant of the one-transaction problem of Q4). Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over the day and a holding flag (len <= 10) on small inputs. Example: prices=[1, 2, 3, 0, 2] -> 3; prices=[1] -> 0; prices=[] -> 0; prices=[6, 1, 3, 2, 4, 7] -> 6.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Stock-trading state-machine write-ups (techinterview.org DP state machine patterns, labuladong stock guide, system.design state-machine notes, a LeetCode Discuss single-template post; search snippets only, not opened)

**Pattern:** State-machine DP over days (three states), O(1) rolling space.

**Say this first (1 line):** "Each day I am in one of three states: holding, just sold today, or free to buy; the cooldown is just that 'sold' cannot go straight to 'hold'."

**Brute force:** Plain recursion `f(day, holding)`: do nothing; or if holding, sell and jump to `day + 2` (the next day is the cooldown); or if not holding, buy and go to `day + 1`. Exponential without a cache, fine for len <= 10. It is the oracle.

**Optimal:**
- States at the end of day `i`: `hold[i]` = best profit ending the day holding a share; `sold[i]` = best profit if I sold today; `free[i]` = best profit ending the day with no share and allowed to buy tomorrow.
- Transitions with price `p`: `hold = max(hold, free - p)` (keep holding, or buy today from the free state); `sold = hold_prev + p` (sell the share I held yesterday); `free = max(free, sold_prev)` (stay free, or the cooldown day just ended).
- Why buying only from `free`: a share bought the day after selling would come from `sold`, which is exactly the cooldown. `sold` must pass through `free` first.
- Base: `hold = -inf`, `sold = -inf`, `free = 0` before day 1. Answer `max(sold, free)` at the end (ending while holding is never better). Empty list: 0.
- Rolling variables: the three new values depend only on the three old ones, so update them in one tuple assignment (the right-hand side uses the old values). Space O(1).
- Dropping the cooldown: `sold` and `free` merge into one state "not holding" (`cash = max(cash, hold + p)`), so two states, and the problem is unlimited transactions. The answer is then the sum of positive day-to-day rises, which is the unlimited-transactions variant of the one-transaction problem in Q4. I checked on all 800 random cases that the two-state value equals that sum, and that it was strictly larger than the cooldown answer on 254 of them (never smaller).

**Complexity:** Time O(n), space O(1). The memoised `f(day, holding)` has about 2n states but nests up to n deep. At 5000 days it raises `RecursionError` at the default limit of 1000 (shown in the run), so bottom-up is required.

**Dry run:** `[1, 2, 3, 0, 2]` (table printed below).
- Day 1 (p=1): hold -1 (buy), free 0.
- Day 2 (p=2): sold = -1 + 2 = 1; hold stays -1; free 0.
- Day 3 (p=3): sold = -1 + 3 = 2; free = max(0, sold_prev 1) = 1.
- Day 4 (p=0): hold = max(-1, free_prev 1 - 0) = 1; sold = -1 + 0 = -1; free = max(1, 2) = 2.
- Day 5 (p=2): sold = 1 + 2 = 3; free = max(2, -1) = 2. Answer `max(3, 2) = 3`: buy 1, sell 2, cooldown, buy 0, sell 2.

**Code:**
```python
import random, sys
from functools import cache

random.seed(25)
NEG = float('-inf')

def cooldown(prices):
    """Bottom-up, O(1) space. States at the END of each day:
    hold = best profit while holding a share; sold = best profit if I sold today; free = best profit, no share, free to buy."""
    hold, sold, free = NEG, NEG, 0
    for p in prices:
        hold, sold, free = max(hold, free - p), hold + p, max(free, sold)
    return max(sold, free)

def cooldown_table(prices):
    """Same thing with full arrays, to print the walk-through."""
    hold, sold, free = [NEG], [NEG], [0]
    for p in prices:
        hold.append(max(hold[-1], free[-1] - p)); sold.append(hold[-2] + p); free.append(max(free[-1], sold[-2]))
    return hold, sold, free

def no_cooldown(prices):
    """Drop the cooldown: sold and free merge into one 'not holding' state."""
    hold, cash = NEG, 0
    for p in prices:
        hold, cash = max(hold, cash - p), max(cash, hold + p)
    return cash

def rises(prices):
    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))

def memo(prices):
    n = len(prices)
    @cache
    def f(i, holding):
        if i >= n: return 0
        best = f(i + 1, holding)                                 # do nothing today
        if holding: best = max(best, prices[i] + f(i + 2, False))   # sell today; day i+1 is the cooldown day
        else: best = max(best, -prices[i] + f(i + 1, True))        # buy today
        return best
    return f(0, False)

def brute(prices):
    """Plain recursion over (day, holding), no cache."""
    n = len(prices)
    def f(i, holding):
        if i >= n: return 0
        best = f(i + 1, holding)
        if holding: best = max(best, prices[i] + f(i + 2, False))
        else: best = max(best, -prices[i] + f(i + 1, True))
        return best
    return f(0, False)

for pr, exp in [([1, 2, 3, 0, 2], 3), ([1], 0), ([], 0), ([6, 1, 3, 2, 4, 7], 6)]:
    assert cooldown(pr) == brute(pr) == memo(pr) == exp, pr
    print('example', pr, '->', exp)

h, s, f = cooldown_table([1, 2, 3, 0, 2])
print('day  price  hold  sold  free')
print('  0      -    ', h[0], s[0], f[0])
for i, p in enumerate([1, 2, 3, 0, 2], 1):
    print(f'  {i}    {p:3d}   {h[i]:4}  {s[i]:4}  {f[i]:4}')
print('answer = max(sold, free) at the end =', max(s[-1], f[-1]))

n_cases = 0; cd_lt = 0
for _ in range(800):
    n = random.randint(0, 10); pr = [random.randint(0, 9) for _ in range(n)]
    want = brute(pr)
    assert cooldown(pr) == want == memo(pr), pr
    nc = no_cooldown(pr)
    assert nc == rises(pr) and nc >= want       # without the cooldown it is the sum of positive daily rises
    n_cases += 1; cd_lt += nc > want
print('cross-check cases', n_cases, '| no-cooldown value strictly larger on', cd_lt, '| no-cooldown == sum of positive rises on all')

# max size: bottom-up fine, memo recursion not
big = [random.randint(0, 1000) for _ in range(5000)]
print('n = 5000 profit', cooldown(big))
print('limit =', sys.getrecursionlimit())
try:
    memo(big); print('memo n=5000 ok')
except RecursionError:
    print('memo n=5000: RecursionError')
assert cooldown([5, 4, 3]) == 0 and cooldown([1, 5]) == 4 and cooldown([2, 2, 2]) == 0
print('edge asserts passed')
```

**Output (my run):**
```
example [1, 2, 3, 0, 2] -> 3
example [1] -> 0
example [] -> 0
example [6, 1, 3, 2, 4, 7] -> 6
day  price  hold  sold  free
  0      -     -inf -inf 0
  1      1     -1  -inf     0
  2      2     -1     1     0
  3      3     -1     2     1
  4      0      1    -1     2
  5      2      1     3     2
answer = max(sold, free) at the end = 3
cross-check cases 800 | no-cooldown value strictly larger on 254 | no-cooldown == sum of positive rises on all
n = 5000 profit 665818
limit = 1000
memo n=5000: RecursionError
edge asserts passed
```

**Edge cases:**
- Empty list or one price: 0.
- Strictly decreasing prices: 0.
- Prices equal: 0.
- Two days `[1, 5]`: 4.
- Do not allow ending with a negative: `max(sold, free)` handles it, `hold` is never the answer.

**Follow-ups:**
- "Add a transaction fee?" Subtract the fee when selling (or buying); the states stay the same.
- "At most k transactions?" See Q29.
- "Cooldown of c days?" Track the last c days of `sold` (or add c rest states).

**Common mistakes:**
- Letting `buy` read `sold` of the previous day (no cooldown at all).
- Using already-updated values inside the same day (writing the three updates as separate statements).
- Starting `hold` at 0 instead of -infinity (a free share).
- Returning `hold` at the end.

### Q26 ⭐⭐ 🟡 Maximum sum circular subarray. `nums` has 1 <= len <= 10^5 integers (|value| <= 10^4) arranged in a circle. A subarray is non-empty and contiguous around the circle; it may wrap from the end to the start but may use each element at most once (it can be the whole list). Return its maximum sum. Explain the two cases (a normal subarray, or a wrapping one equal to the total minus a minimum middle subarray) and the all-negative edge case where the wrapping formula would wrongly allow an empty subarray. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an O(n^2) enumeration of every circular subarray on small inputs. Example: nums=[1, -2, 3, -2] -> 3; nums=[5, -3, 5] -> 10; nums=[-3, -2, -3] -> -2; nums=[3, -1, 2, -1] -> 4; nums=[4] -> 4.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Kadane twice (max and min), the circular case as "total minus the minimum middle".

**Say this first (1 line):** "Either the best subarray does not wrap, which is plain Kadane, or it wraps, and then what is left out is a contiguous middle block, so the wrapped sum is the total minus the minimum subarray."

**Brute force:** Every start `s` and every length `L` from 1 to `n`, summing `nums[(s+k) % n]`. O(n^2) with a running sum. It is the oracle.

**Optimal:**
- Case 1 (no wrap): the best subarray lies inside the list, so it is the ordinary Kadane maximum `mx`. State: `cur[i]` = best sum ending at `i`, `cur[i] = max(x, cur[i-1] + x)`.
- Case 2 (wrap): the chosen arc uses a suffix and a prefix. What it leaves out is a contiguous block in the middle. Its sum is `total - leftover`, so to maximise it, minimise the leftover: `total - mn` where `mn` is the minimum-sum subarray (second Kadane with `min`).
- Answer: `max(mx, total - mn)`.
- The all-negative trap: if every element is negative, the minimum subarray is the whole list, so `total - mn = 0`, which corresponds to taking NOTHING, an empty subarray that is not allowed. The formula would then return 0, higher than every legal answer. Fix: if `mx < 0` (all elements negative), return `mx`. (If `mx >= 0`, the value `total - mn` is at most the total of a non-empty arc whenever the minimum block is not the whole list, and when it is the whole list the term is 0 which does not beat `mx >= 0`.)
- I checked exactly this: on all 19607 lists of length 1..5 with values -3..3, the fixed version matches the circular enumeration; the naive formula `max(mx, total - mn)` is wrong on 363 of them and every one of those is an all-negative list.
- Space O(1), single pass possible.

**Complexity:** Time O(n), space O(1). Loops only; no recursion.

**Dry run:** `[5, -3, 5]`: total 7. Normal Kadane gives 7 (the whole list, which is a legal arc). Minimum subarray is `[-3]` with sum -3. Wrap value: `7 - (-3) = 10`, which is the arc `5, 5` going around the end back to the start. Answer 10. For `[-3, -2, -3]`: `mx = -2`, `mn = -8`, `total - mn = 0` would be empty, so return `-2`.

**Code:**
```python
import random, itertools

random.seed(26)

def kadane_max_min(nums):
    mx = cur = mn = curm = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x); mx = max(mx, cur)
        curm = min(x, curm + x); mn = min(mn, curm)
    return mx, mn

def circular(nums):
    """max(best normal subarray, total - min subarray), except when every element is negative (then the
    minimum subarray is the whole list and total - mn = 0 would be an EMPTY subarray)."""
    mx, mn = kadane_max_min(nums)
    if mx < 0:
        return mx
    return max(mx, sum(nums) - mn)

def naive(nums):
    mx, mn = kadane_max_min(nums)
    return max(mx, sum(nums) - mn)

def brute(nums):
    n = len(nums); best = None
    for s in range(n):
        tot = 0
        for L in range(1, n + 1):
            tot += nums[(s + L - 1) % n]
            if best is None or tot > best: best = tot
    return best

for nums, exp in [([1, -2, 3, -2], 3), ([5, -3, 5], 10), ([-3, -2, -3], -2), ([3, -1, 2, -1], 4), ([4], 4)]:
    assert circular(nums) == brute(nums) == exp, nums
    print('example', nums, '->', exp)

nums = [5, -3, 5]
mx, mn = kadane_max_min(nums)
print('walk-through', nums, ': total', sum(nums), '| best normal', mx, '| min middle', mn, '| wrap =', sum(nums), '-', mn, '=', sum(nums) - mn, '| answer', circular(nums))
nums = [-3, -2, -3]
mx, mn = kadane_max_min(nums)
print('all-negative', nums, ': best normal', mx, '| min', mn, '| total - min =', sum(nums) - mn, '(empty subarray!) | answer', circular(nums))

# exhaustive: every list of length 1..5 with values -3..3, plus seeded random
cnt = bad_naive = 0
for n in range(1, 6):
    for t in itertools.product(range(-3, 4), repeat=n):
        l = list(t); assert circular(l) == brute(l), l
        cnt += 1; bad_naive += naive(l) != brute(l)
print('exhaustive lists', cnt, '| naive formula wrong on', bad_naive)
allneg_bad = 0
for n in range(1, 6):
    for t in itertools.product(range(-3, 4), repeat=n):
        l = list(t)
        if naive(l) != brute(l):
            assert max(l) < 0; allneg_bad += 1
print('every naive failure is an all-negative list:', allneg_bad == bad_naive)
for _ in range(500):
    n = random.randint(1, 12); l = [random.randint(-9, 9) for _ in range(n)]
    assert circular(l) == brute(l), l
print('500 seeded random lists agree with the O(n^2) circular enumeration')

big = [random.randint(-10**4, 10**4) for _ in range(10**5)]
print('n = 10^5 answer', circular(big))
assert circular([4]) == 4 and circular([-1]) == -1 and circular([2, 2]) == 4 and circular([-1, 5, -1]) == 5
print('edge asserts passed')
```

**Output (my run):**
```
example [1, -2, 3, -2] -> 3
example [5, -3, 5] -> 10
example [-3, -2, -3] -> -2
example [3, -1, 2, -1] -> 4
example [4] -> 4
walk-through [5, -3, 5] : total 7 | best normal 7 | min middle -3 | wrap = 7 - -3 = 10 | answer 10
all-negative [-3, -2, -3] : best normal -2 | min -8 | total - min = 0 (empty subarray!) | answer -2
exhaustive lists 19607 | naive formula wrong on 363
every naive failure is an all-negative list: True
500 seeded random lists agree with the O(n^2) circular enumeration
n = 10^5 answer 2416709
edge asserts passed
```

**Edge cases:**
- Single element: itself (`[4] -> 4`, `[-1] -> -1`).
- All negative: the largest element.
- Mixed with total negative: the answer is a normal subarray; the wrap term is smaller.
- The whole list is allowed (each element at most once), so Kadane's whole-list case is legal.
- Zeros: no special handling.

**Follow-ups:**
- "Do it without a second Kadane?" Use prefix sums and a deque for sliding-window minimum on a doubled array (O(n), more code).
- "Maximum product circular?" Not the same trick; negatives flip.
- "Return the arc too?" Carry start indexes (Q22) and, for the wrap case, the complement of the min block.

**Common mistakes:**
- Forgetting the all-negative case and returning 0.
- Checking `total == mn` instead of `mx < 0` (the `mx < 0` test is the clean one).
- Letting the wrapped arc use an element twice (doubled array with window length > n).
- Initialising `mx = 0` or `mn = 0` instead of `nums[0]`.

### Q27 ⭐⭐ 🟡 Delete and earn. `nums` has 0 <= len <= 2*10^4 integers in 1..10^4. In one move pick a value x present in the list: you earn x points for EVERY copy of x, and then every copy of x - 1 and x + 1 is deleted (the other copies of x are consumed by the move). Moves repeat until nothing is left that you want. Return the maximum points (0 for an empty list). Show the reduction to house robber (Q5) over a table indexed by value and why copies of the same value always go together. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all sets of distinct values with no two consecutive integers on small inputs. Example: nums=[3, 4, 2] -> 6; nums=[2, 2, 3, 3, 3, 4] -> 9; nums=[] -> 0; nums=[1, 1, 1, 2, 4, 5, 5, 5, 6] -> 18.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Reduction to House Robber (Q5) on a table indexed by value.

**Say this first (1 line):** "Pick value `x` and you take all copies and lose `x-1` and `x+1`, so build `tot[v] = v * count(v)` and the question becomes: choose values with no two adjacent, maximise the sum. That is House Robber."

**Brute force:** Enumerate every subset of the distinct values with no two consecutive integers, score `sum(v * count(v))`. O(2^d) for d distinct values. A second oracle simulates the game itself on small lists (pick a value, remove it and its neighbours, recurse).

**Optimal:**
- Why copies go together: choosing `x` once earns `x` for every copy, and the rule consumes all other copies of `x` in the same move. So there is no case where taking only some copies is possible or better, and after taking `x` the same neighbours `x-1`, `x+1` are gone either way. Each distinct value is a take-all or skip decision.
- Table: `tot[v] = v * count(v)` for `v = 0..max(nums)`; missing values have 0.
- State: `best[v]` = best total using values `<= v`. Transition: `best[v] = max(best[v-1], best[v-2] + tot[v])` (skip v, or take v and so skip v-1). Base `best[0] = 0` (and `best[-1] = 0`).
- Rolling form: `take, skip = skip + tot[v], max(take, skip)`. Answer `max(take, skip)`. Space O(max value) for the table, O(1) beyond it.
- Gaps are harmless: a value with `tot = 0` is simply never needed, and two values differing by 2 or more do not conflict, which the recurrence reflects since it only links `v` to `v-1`.
- Empty list: 0.

**Complexity:** Time O(n + M) where M = max value (10^4 here), space O(M). Memoised recursion `f(v)` nests M = 10^4 deep: it raises `RecursionError` at the default limit of 1000 (shown in the run), so use the loop.

**Dry run:** `[2, 2, 3, 3, 3, 4]`: `tot = [0, 0, 4, 9, 4]`.
- v=2: take 4, skip 0.
- v=3: take = skip_prev + 9 = 9; skip = max(4, 0) = 4.
- v=4: take = skip_prev 4 + 4 = 8; skip = max(9, 4) = 9.
- Answer 9: take all three 3s, losing the 2s and the 4.

**Code:**
```python
import random, sys
from collections import Counter
from functools import cache

random.seed(27)

def delete_and_earn(nums):
    """Reduce to house robber over values: tot[v] = v * count(v); picking v forbids v-1 and v+1."""
    if not nums: return 0
    tot = [0] * (max(nums) + 1)
    for x in nums: tot[x] += x
    take, skip = 0, 0                    # take = best with the previous value taken, skip = best with it not taken
    for v in range(len(tot)):
        take, skip = skip + tot[v], max(take, skip)
    return max(take, skip)

def rob(a):
    """House robber, rolling: prev2, prev1."""
    p2 = p1 = 0
    for v in a: p2, p1 = p1, max(p1, p2 + v)
    return p1

def via_robber(nums):
    if not nums: return 0
    tot = [0] * (max(nums) + 1)
    for x in nums: tot[x] += x
    return rob(tot)

def memo(nums):
    if not nums: return 0
    tot = [0] * (max(nums) + 1)
    for x in nums: tot[x] += x
    @cache
    def f(i):
        if i < 0: return 0
        return max(f(i - 1), f(i - 2) + tot[i])
    return f(len(tot) - 1)

def brute(nums):
    """All sets of distinct values with no two consecutive integers."""
    c = Counter(nums); vals = sorted(c); best = 0
    for m in range(1 << len(vals)):
        ch = [vals[i] for i in range(len(vals)) if m >> i & 1]
        if all(ch[i + 1] - ch[i] > 1 for i in range(len(ch) - 1)):
            best = max(best, sum(v * c[v] for v in ch))
    return best

def simulate(nums):
    """Direct simulation of the game on small lists (picks one value at a time), to justify the reduction."""
    @cache
    def g(state):
        best = 0
        for v in set(state):
            rest = tuple(sorted(y for y in state if y != v and y != v - 1 and y != v + 1))
            best = max(best, v * state.count(v) + g(rest))
        return best
    return g(tuple(sorted(nums)))

for nums, exp in [([3, 4, 2], 6), ([2, 2, 3, 3, 3, 4], 9), ([], 0), ([1, 1, 1, 2, 4, 5, 5, 5, 6], 18)]:
    assert delete_and_earn(nums) == brute(nums) == via_robber(nums) == memo(nums) == simulate(nums) == exp, nums
    print('example', nums, '->', exp)

nums = [2, 2, 3, 3, 3, 4]
tot = [0] * (max(nums) + 1)
for x in nums: tot[x] += x
print('tot by value 0..4 =', tot)
take, skip = 0, 0
for v in range(len(tot)):
    take, skip = skip + tot[v], max(take, skip)
    print(f'value {v}: tot={tot[v]:2d}  best if value {v} taken={take:2d}  best if not taken={skip:2d}')
print('answer', max(take, skip))

for _ in range(800):
    n = random.randint(0, 9); l = [random.randint(1, 8) for _ in range(n)]
    want = brute(l)
    assert delete_and_earn(l) == want == via_robber(l) == memo(l), l
    assert simulate(l) == want, l
print('800 seeded random lists: DP == subset enumeration == game simulation == memo')

big = [random.randint(1, 10**4) for _ in range(2 * 10**4)]
print('n = 2*10^4, values <= 10^4 answer', delete_and_earn(big))
print('limit =', sys.getrecursionlimit())
try:
    memo([10**4]); print('memo ok')
except RecursionError:
    print('memo over a value table of 10^4 slots: RecursionError')
assert delete_and_earn([1]) == 1 and delete_and_earn([5, 5, 5]) == 15 and delete_and_earn([1, 2]) == 2
print('edge asserts passed')
```

**Output (my run):**
```
example [3, 4, 2] -> 6
example [2, 2, 3, 3, 3, 4] -> 9
example [] -> 0
example [1, 1, 1, 2, 4, 5, 5, 5, 6] -> 18
tot by value 0..4 = [0, 0, 4, 9, 4]
value 0: tot= 0  best if value 0 taken= 0  best if not taken= 0
value 1: tot= 0  best if value 1 taken= 0  best if not taken= 0
value 2: tot= 4  best if value 2 taken= 4  best if not taken= 0
value 3: tot= 9  best if value 3 taken= 9  best if not taken= 4
value 4: tot= 4  best if value 4 taken= 8  best if not taken= 9
answer 9
800 seeded random lists: DP == subset enumeration == game simulation == memo
n = 2*10^4, values <= 10^4 answer 60911434
limit = 1000
memo over a value table of 10^4 slots: RecursionError
edge asserts passed
```

**Edge cases:**
- Empty list: 0 (guard `max(nums)`; `max([])` raises `ValueError`).
- One distinct value with many copies: `v * count`.
- All values consecutive (`[1,2]`): 2, not 3.
- Large gaps: the table is mostly zeros; fine at M = 10^4. If values were up to 10^9, sort the distinct values and compare only with the previous distinct value (check `v - prev == 1`).

**Follow-ups:**
- "Values up to 10^9?" Work over sorted distinct values and keep the two previous states, resetting when the gap is > 1.
- "House Robber on a circle?" Run twice, excluding the first or the last (Part 7 Q45 is the tree version).
- "Why not greedy (take the largest value first)?" On `[2,2,3,3,3,4]` it takes the 4 (4 points), loses the 3s, then takes the 2s (4): 8, but the best is 9 (all the 3s).

**Common mistakes:**
- Counting `v` once instead of `v * count(v)`.
- Linking `v` to `v-1` in the list index of the sorted array instead of the value table (gaps then break adjacency).
- Calling `max(nums)` on an empty list.
- Memoised recursion over a 10^4-slot table.

### Q28 ⭐⭐ 🔴 Number of longest increasing subsequences. `nums` has 0 <= len <= 2000 integers (|value| <= 10^6, repeats allowed). Return `[L, count]`: L is the length of the longest strictly increasing subsequence and `count` the number of index sets (subsequences chosen by position, so equal values at different positions count separately) that achieve it; return [0, 0] for an empty list. Keep two arrays per index (best length ending here, how many ways) and explain the update when a longer length is found and when an equal one is found. State the time (O(n^2)) and how the O(n log n) bisect method (Q7) differs: it gives the length but not the count without extra bookkeeping. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsequences (len <= 12) on small inputs. Example: nums=[1, 3, 5, 4, 7] -> [4, 2]; nums=[2, 2, 2, 2, 2] -> [1, 5]; nums=[] -> [0, 0]; nums=[1, 2, 4, 3, 5, 4, 7, 2] -> [5, 3]; nums=[5, 4, 3] -> [1, 3].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** O(n^2) LIS DP carrying a second array (counts), the "count the optimal solutions" DP.

**Say this first (1 line):** "For each index I store the longest increasing run ending there and how many runs achieve it; a longer predecessor replaces the count, an equally long one adds to it."

**Brute force:** Enumerate all 2^n subsets by position, keep the strictly increasing ones, track the longest length and how many reach it. O(2^n * n); fine for n <= 12. It is the oracle.

**Optimal:**
- State: `length[i]` = length of the longest strictly increasing subsequence ending at index `i`; `ways[i]` = number of such subsequences of that length ending at `i` (counted by position, so equal values at different positions are different).
- Base: `length[i] = 1`, `ways[i] = 1` (the element alone).
- Transition: for each `j < i` with `nums[j] < nums[i]`, the candidate length is `length[j] + 1`.
  - If it is strictly greater than `length[i]`: set `length[i] = length[j] + 1` and `ways[i] = ways[j]` (the old count described shorter runs and is thrown away).
  - If it equals `length[i]`: `ways[i] += ways[j]` (a second family of equally long runs).
  - If smaller: ignore.
- Answer: `L = max(length)`, `count = sum(ways[i] for i with length[i] == L)`. A run of length `L` ends somewhere, and the ends are distinct positions, so we add over all of them. Empty list: `[0, 0]`.
- Why the counts are right: a longest run ending at `i` has a unique predecessor position `j`, and its first `length-1` elements form a longest run ending at `j`. So the runs ending at `i` split by predecessor, and each class has `ways[j]` members.
- Equal values: `nums[j] < nums[i]` is strict, so equal values never chain; `[2,2,2,2,2]` gives `[1, 5]`.
- Versus the O(n log n) bisect method (Q7): `tails` only keeps the smallest tail per length, so it throws away how many ways there were. It gives `L` (my run shows it equals `L` on all 700 cases) but not the count unless you extend each pile with counts (more bookkeeping).

**Complexity:** Time O(n^2) (n = 2000 means about 2 million inner steps), space O(n). Recursion limit: the top-down memo over `(index)` nests as deep as the dependency chain. In the run, on the increasing list `0..1999` the version whose inner loop runs `j` descending raised `RecursionError` at the default limit of 1000, while the ascending-`j` version computed the small indices first and did not (a fragile accident of loop order). The prompt does not force bottom-up, but I use the loops because their depth is always 1.

**Dry run:** `[1, 3, 5, 4, 7]` (table printed below).
- 1: length 1, ways 1.
- 3: from 1: length 2, ways 1.
- 5: from 1 (length 2, replace), from 3 (length 3 > 2, replace): length 3, ways 1.
- 4: from 1: 2; from 3: 3 (replace): length 3, ways 1.
- 7: from 1: 2; from 3: 3; from 5: 4 (replace, ways 1); from 4: 4 equals, add ways 1: length 4, ways 2.
- `L = 4`, count 2 (`1,3,5,7` and `1,3,4,7`).

**Code:**
```python
import random, sys, bisect
from functools import cache

random.seed(28)

def count_lis(nums):
    """O(n^2). length[i] = longest strictly increasing subsequence ENDING at i, ways[i] = how many (by position)."""
    n = len(nums)
    if n == 0: return [0, 0]
    length = [1] * n; ways = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i], ways[i] = length[j] + 1, ways[j]      # strictly longer: replace the count
                elif length[j] + 1 == length[i]:
                    ways[i] += ways[j]                               # equally long: add the counts
    L = max(length)
    return [L, sum(w for l, w in zip(length, ways) if l == L)]

def tables(nums):
    n = len(nums); length = [1] * n; ways = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]: length[i], ways[i] = length[j] + 1, ways[j]
                elif length[j] + 1 == length[i]: ways[i] += ways[j]
    return length, ways

def lis_len_bisect(nums):
    tails = []
    for x in nums:
        k = bisect.bisect_left(tails, x)
        if k == len(tails): tails.append(x)
        else: tails[k] = x
    return len(tails)

def memo(nums):
    n = len(nums)
    @cache
    def f(i):                       # (length ending at i, ways)
        best, w = 1, 1
        for j in range(i):
            if nums[j] < nums[i]:
                l, c = f(j)
                if l + 1 > best: best, w = l + 1, c
                elif l + 1 == best: w += c
        return best, w
    if n == 0: return [0, 0]
    res = [f(i) for i in range(n)]       # forward order keeps the recursion shallow in this test; see text
    L = max(l for l, _ in res)
    return [L, sum(c for l, c in res if l == L)]

def brute(nums):
    n = len(nums); best = 0; cnt = 0
    for m in range(1, 1 << n):
        v = [nums[i] for i in range(n) if m >> i & 1]
        if all(v[i] < v[i + 1] for i in range(len(v) - 1)):
            if len(v) > best: best, cnt = len(v), 1
            elif len(v) == best: cnt += 1
    return [best, cnt] if n else [0, 0]

for nums, exp in [([1, 3, 5, 4, 7], [4, 2]), ([2, 2, 2, 2, 2], [1, 5]), ([], [0, 0]),
                  ([1, 2, 4, 3, 5, 4, 7, 2], [5, 3]), ([5, 4, 3], [1, 3])]:
    assert count_lis(nums) == brute(nums) == memo(nums) == exp, nums
    print('example', nums, '->', exp)

nums = [1, 3, 5, 4, 7]
ln, wy = tables(nums)
print('i   x  length ways')
for i, x in enumerate(nums): print(f'{i}  {x:2d}  {ln[i]:5d} {wy[i]:4d}')
print('L =', max(ln), '| count = sum of ways where length == L =', sum(w for l, w in zip(ln, wy) if l == max(ln)))

cases = 0; bisect_agree = 0
for _ in range(700):
    n = random.randint(0, 12); l = [random.randint(-4, 6) for _ in range(n)]
    assert count_lis(l) == brute(l) == memo(l), l
    assert lis_len_bisect(l) == count_lis(l)[0]
    cases += 1
print('cross-check cases', cases, '| bisect_left length equals L on all (it gives the length, not the count)')

big = [random.randint(-10**6, 10**6) for _ in range(2000)]
print('n = 2000 random:', count_lis(big))
inc = list(range(2000))
print('n = 2000 increasing:', count_lis(inc))
print('n = 2000 all equal:', count_lis([7] * 2000))
print('limit =', sys.getrecursionlimit())
def top_down(seq, order):
    @cache
    def g(i):
        best, w = 1, 1
        for j in order(i):
            if seq[j] < seq[i]:
                l, c = g(j)
                if l + 1 > best: best, w = l + 1, c
                elif l + 1 == best: w += c
        return best, w
    return g
for name, order in (('j ascending', lambda i: range(i)), ('j descending', lambda i: reversed(range(i)))):
    try:
        top_down(inc, order)(1999); print('top-down, inner loop', name, ': ok on 0..1999 increasing')
    except RecursionError:
        print('top-down, inner loop', name, ': RecursionError on 0..1999 increasing')
assert count_lis([9]) == [1, 1] and count_lis([1, 2]) == [2, 1]
print('edge asserts passed')
```

**Output (my run):**
```
example [1, 3, 5, 4, 7] -> [4, 2]
example [2, 2, 2, 2, 2] -> [1, 5]
example [] -> [0, 0]
example [1, 2, 4, 3, 5, 4, 7, 2] -> [5, 3]
example [5, 4, 3] -> [1, 3]
i   x  length ways
0   1      1    1
1   3      2    1
2   5      3    1
3   4      3    1
4   7      4    2
L = 4 | count = sum of ways where length == L = 2
cross-check cases 700 | bisect_left length equals L on all (it gives the length, not the count)
n = 2000 random: [87, 9256960]
n = 2000 increasing: [2000, 1]
n = 2000 all equal: [1, 2000]
limit = 1000
top-down, inner loop j ascending : ok on 0..1999 increasing
top-down, inner loop j descending : RecursionError on 0..1999 increasing
edge asserts passed
```

**Edge cases:**
- Empty list: `[0, 0]` (not `[0, 1]`).
- All equal: `[1, n]`.
- Strictly decreasing: `[1, n]`.
- Strictly increasing: `[n, 1]`.
- Counts can be huge in other variants; here Python integers are exact (a random 2000-list gave 9256960).

**Follow-ups:**
- "Count in O(n log n)?" Use a Fenwick tree or segment tree over values storing `(length, count)` pairs and merge by max length (adding counts on ties).
- "Non-decreasing?" Change `<` to `<=`; equal values then chain.
- "Return one LIS?" Q34 (tie rule and rebuild).

**Common mistakes:**
- Setting `ways[i] += ways[j]` when the length is greater instead of replacing.
- Summing `ways` over all `i` instead of only those with `length == L`.
- Counting distinct value sequences instead of index sets.
- Returning `[0, 1]` for the empty list.

### Q29 ⭐⭐ 🔴 Best time to buy and sell stock with at most k transactions. `prices` has 0 <= len <= 1000 non-negative integers (<= 1000) and `k` is 0 <= k <= 10^9; a transaction is one buy and the later sell of that share, and you hold at most one share at a time. Return the maximum profit. Define the states (buy[j], sell[j] for j transactions), give the O(n * k) table with O(k) space, and say why k >= len // 2 can be treated as 'unlimited transactions' (sum of positive day-to-day rises), which also keeps the table small when k is huge. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over day, transactions left and holding flag (len <= 8) on small inputs. Example: k=2, prices=[3, 2, 6, 5, 0, 3] -> 7; k=1, prices=[7, 6, 4, 3, 1] -> 0; k=1000000000, prices=[1, 5, 2, 8, 3, 9] -> 16; k=0, prices=[1, 9] -> 0.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Stock-trading state-machine write-ups (techinterview.org DP state machine patterns, labuladong stock guide, system.design state-machine notes, a LeetCode Discuss single-template post; search snippets only, not opened)

**Pattern:** State-machine DP with a transaction counter (buy[j], sell[j]), plus a cap on useful `k`.

**Say this first (1 line):** "`buy[j]` is the best profit while holding the share of my j-th transaction, `sell[j]` after finishing j transactions; each day updates both, and if `k >= n // 2` the limit never binds, so it is just the sum of positive rises."

**Brute force:** Recursion over `(day, transactions left, holding)`: skip, sell if holding, buy if not holding and a transaction is left. Exponential without a cache; I use it for len <= 8. A memoised version has `n * k * 2` states.

**Optimal:**
- State: `buy[j]` = max profit so far if I currently hold a share bought as my j-th transaction; `sell[j]` = max profit so far having completed j transactions and holding nothing. Counting a transaction at the buy keeps the bookkeeping simple.
- Base: `sell[0] = 0`, `buy[j] = -inf` and `sell[j] = 0` for `j >= 1` (doing fewer transactions is always allowed, so 0 is right).
- Transition, for each price `p` and `j = 1..k`: `buy[j] = max(buy[j], sell[j-1] - p)`; `sell[j] = max(sell[j], buy[j] + p)`. Answer `sell[k]`.
- Space: only the previous day's values are needed, and the arrays are indexed by `j`, so O(k) (the code overwrites in place; updating `buy[j]` before `sell[j]` on the same day can only allow a buy and a sell at the same price, which adds 0 profit and is harmless).
- Why `k >= n // 2` means unlimited: a transaction needs a buy day and a later sell day, so at most `n // 2` disjoint transactions fit in `n` days. With `k >= n // 2` the limit never binds, so the answer equals the unlimited answer, the sum of positive day-to-day rises. Exhaustively checked: on all 21845 lists of length <= 7 with values 0..3, `table(k) == unlimited` for every k from `n // 2` up. The bound is also tight: for `[0, 1, 0, 1]`, `k = 1` gives 1 but unlimited gives 2.
- Why it keeps the table small when `k = 10^9`: without the cap the `buy`/`sell` arrays would have 10^9 entries. With the cap `k` is replaced by the shortcut, and when `k < n // 2` the arrays have at most 500 entries here.
- Degenerate cases: `k = 0` or fewer than 2 days: 0.

**Complexity:** Time O(n * min(k, n // 2)) = at most 1000 * 500 here, space O(min(k, n // 2)). Memoised recursion over days nests n = 1000 deep and raises `RecursionError` at the default limit of 1000 (shown in the run), so bottom-up is the answer.

**Dry run:** `k=2`, `[3, 2, 6, 5, 0, 3]` (table printed below).
- Best first trade: buy 2, sell 6 (+4); second: buy 0, sell 3 (+3). Total 7.
- In the table `buy1` ends at 0 (the share bought at price 0 costs `-0`), `sell1 = 4`, `buy2 = sell1 - 0 = 4`, `sell2 = 4 + 3 = 7`.

**Code:**
```python
import random, sys
from functools import cache

random.seed(29)
NEG = float('-inf')

def table_k(k, prices):
    """O(n*k) time, O(k) space. buy[j] = best profit holding a share during the j-th transaction,
    sell[j] = best profit after completing j transactions."""
    buy = [NEG] * (k + 1); sell = [0] * (k + 1)
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]

def unlimited(prices):
    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))

def solve(k, prices):
    n = len(prices)
    if n < 2 or k == 0: return 0
    if k >= n // 2: return unlimited(prices)     # at most n // 2 transactions can ever be useful
    return table_k(k, prices)

def memo(k, prices):
    n = len(prices)
    @cache
    def f(i, t, hold):
        if i == n: return 0
        best = f(i + 1, t, hold)
        if hold: best = max(best, prices[i] + f(i + 1, t, 0))
        elif t > 0: best = max(best, -prices[i] + f(i + 1, t - 1, 1))
        return best
    return f(0, k, 0)

def brute(k, prices):
    n = len(prices)
    def f(i, t, hold):
        if i == n: return 0
        best = f(i + 1, t, hold)
        if hold: best = max(best, prices[i] + f(i + 1, t, 0))
        elif t > 0: best = max(best, -prices[i] + f(i + 1, t - 1, 1))
        return best
    return f(0, k, 0)

for k, pr, exp in [(2, [3, 2, 6, 5, 0, 3], 7), (1, [7, 6, 4, 3, 1], 0), (10**9, [1, 5, 2, 8, 3, 9], 16), (0, [1, 9], 0)]:
    assert solve(k, pr) == brute(k, pr) == exp, (k, pr)
    print('example k =', k, pr, '->', exp)

# walk-through for the first example
k, pr = 2, [3, 2, 6, 5, 0, 3]
buy = [NEG] * (k + 1); sell = [0] * (k + 1)
print('day price | buy1 sell1 buy2 sell2')
for d, p in enumerate(pr):
    for j in range(1, k + 1):
        buy[j] = max(buy[j], sell[j - 1] - p); sell[j] = max(sell[j], buy[j] + p)
    print(f' {d}   {p}   | {buy[1]:4} {sell[1]:4} {buy[2]:4} {sell[2]:4}')
print('answer sell[2] =', sell[2])

# the k >= n // 2 claim: full table vs unlimited, exhaustive over small price lists
cnt = 0; first_k_needed = {}
import itertools
for n in range(0, 8):
    for t in itertools.product(range(0, 4), repeat=n):
        pr = list(t); u = unlimited(pr)
        for kk in range(0, n + 3):
            full = table_k(kk, pr) if kk else 0
            if kk >= n // 2: assert full == u, (kk, pr)
            if kk < n // 2: assert full <= u
        cnt += 1
print('exhaustive price lists (len <= 7, values 0..3):', cnt, '- table(k) == unlimited for every k >= n // 2')
# is n // 2 tight? find a list where k = n // 2 - 1 is strictly worse
ex = None
for n in (4, 6):
    for t in itertools.product(range(0, 3), repeat=n):
        pr = list(t)
        if table_k(n // 2 - 1, pr) < unlimited(pr): ex = pr; break
    if ex: break
print('k = n // 2 - 1 is not enough on e.g.', ex, ':', table_k(len(ex) // 2 - 1, ex), '<', unlimited(ex))

# seeded cross-check against the recursion over (day, transactions left, holding)
n_cases = 0
for _ in range(600):
    n = random.randint(0, 8); pr = [random.randint(0, 9) for _ in range(n)]; kk = random.randint(0, 5)
    want = brute(kk, pr)
    assert solve(kk, pr) == want == memo(kk, pr) == (table_k(kk, pr) if kk else 0), (kk, pr)
    n_cases += 1
print('cross-check cases', n_cases, '(table, shortcut and memo all equal the recursion)')

big = [random.randint(0, 1000) for _ in range(1000)]
print('n = 1000, k = 10^9 ->', solve(10**9, big), '| k = 50 ->', solve(50, big))
print('limit =', sys.getrecursionlimit())
try:
    memo(3, big); print('memo n=1000 ok')
except RecursionError:
    print('memo n=1000: RecursionError')
assert solve(0, [1, 2]) == 0 and solve(5, []) == 0 and solve(5, [4]) == 0 and solve(1, [1, 2]) == 1
print('edge asserts passed')
```

**Output (my run):**
```
example k = 2 [3, 2, 6, 5, 0, 3] -> 7
example k = 1 [7, 6, 4, 3, 1] -> 0
example k = 1000000000 [1, 5, 2, 8, 3, 9] -> 16
example k = 0 [1, 9] -> 0
day price | buy1 sell1 buy2 sell2
 0   3   |   -3    0   -3    0
 1   2   |   -2    0   -2    0
 2   6   |   -2    4   -2    4
 3   5   |   -2    4   -1    4
 4   0   |    0    4    4    4
 5   3   |    0    4    4    7
answer sell[2] = 7
exhaustive price lists (len <= 7, values 0..3): 21845 - table(k) == unlimited for every k >= n // 2
k = n // 2 - 1 is not enough on e.g. [0, 1, 0, 1] : 1 < 2
cross-check cases 600 (table, shortcut and memo all equal the recursion)
n = 1000, k = 10^9 -> 166382 | k = 50 -> 46152
limit = 1000
memo n=1000: RecursionError
edge asserts passed
```

**Edge cases:**
- `k = 0`: 0. Empty or single price: 0.
- `k = 10^9`: take the shortcut, never allocate `k + 1` slots.
- Always falling prices: 0.
- `k >= n // 2` with `n` odd (e.g. n = 5, k = 2): shortcut applies, `n // 2 = 2`.

**Follow-ups:**
- "k = 2 exactly?" Four scalar variables (the table with k = 2 unrolled).
- "Cooldown instead of a limit?" Q25.
- "Fee per transaction?" Subtract it at the sell; the shortcut changes to a greedy-with-fee form.

**Common mistakes:**
- Allocating arrays of size `k + 1` for huge `k` (memory error).
- Using `k >= n` as the cap and wasting time, or `k > n // 2` and missing the `==` case.
- Initialising `buy` to 0 (free share) instead of `-inf`.
- Starting the `sell[j]` array at `-inf`, which wrongly forbids doing fewer than `j` trades.

### Q30 ⭐⭐ 🔴 Last stone weight II (any smash order). `stones` has 1 <= len <= 30 integers in 1..100. Repeatedly choose ANY two stones x <= y and smash them: both vanish if equal, otherwise a stone of weight y - x remains. At most one stone is left at the end (or none). Return the smallest possible weight of the last stone (0 if none is left). Part 8 Q18 smashes the two heaviest and answers a different question (that order is fixed); here you choose the order. Show the reduction to splitting the stones into two groups with the smallest difference of sums, then subset sums up to total // 2. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an exhaustive search over every sequence of smashes (len <= 7) and over all sign assignments on small inputs. Example: stones=[2, 7, 4, 1, 8, 1] -> 1; stones=[31, 26, 33, 21, 40] -> 5; stones=[5] -> 5; stones=[3, 3] -> 0; stones=[1, 2, 5] -> 2.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 0/1 knapsack as subset sum ("split into two groups with the smallest difference"). Any smash order is free, so this is not the greedy of Part 8 Q18.

**Say this first (1 line):** "Whatever order I smash in, the last stone is the absolute value of some plus/minus sum of the stones, so I want the two-group split with the smallest difference, which is subset sums up to `total // 2`."

**Brute force:** Try every sequence of smashes: pick any two stones, replace them by their difference (drop it if 0), recurse on the sorted tuple with a cache. Exponential; I use it for len <= 7. Also all `2^n` sign assignments, taking the minimum of `|sum|`.

**Optimal:**
- Reduction, direction 1: after any smash, the new stone `y - x` is a signed combination of the two original groups of stones. By induction, every stone in the pile is `+/-` a signed sum of original stones, and the last stone is `|sum of s_i * stone_i|` for some signs `s_i`. So the answer is at least `min |signed sum|`.
- Direction 2: take signs with minimum `d = |signed sum|`, plus-group P and minus-group N. Smash a plus stone against a minus stone repeatedly (the difference joins the heavier side); each step keeps the signed sum the same. This ends when one side is empty, leaving stones that sum to `d` on one side. If two or more were left, smashing two of them `u <= v` would make a smash order whose result has signed sum `d - 2u < d`, contradicting minimality of `d` (`d >= u + v >= 2u`). So exactly one stone (or none) remains with weight `d`. So the answer equals `min |signed sum|`. All checked by brute force: the smash search, the sign enumeration and the DP agree on 500 seeded lists of length <= 7.
- Signed sum = `sum(P) - sum(N) = total - 2 * sum(N)`. Minimise `|total - 2a|` over subset sums `a`; the best is the largest achievable `a <= total // 2`. Answer `total - 2a`.
- State: `can[s]` = True if some subset of the stones seen so far sums to `s`, for `s = 0..total // 2`. Base `can[0] = True`. Transition per stone `x`: for `s` from `half` DOWN to `x`: `can[s] |= can[s - x]`. Downward so each stone is used once (an upward loop would be the unbounded version, Q20).
- Bitset alternative: `bits |= bits << x`, then walk down from `total // 2` to the first set bit. Same answers on every test.
- Space: O(total // 2), at most 30 * 100 / 2 = 1500 slots.

**Complexity:** Time O(n * total / 2) = about 30 * 1500 = 45,000 steps; space O(total / 2). Memoised recursion over `(i, cap)` nests at most `n = 30` deep, far below the recursion limit of 1000, so the limit is not a problem here; I still prefer the table (and a memo has up to n * half = 45,000 states, so the table is cheaper).

**Dry run:** `[2, 7, 4, 1, 8, 1]`, total 23, half 11 (the printed table lists the reachable sums after each stone).
- After 2: {0, 2}. After 7: {0, 2, 7, 9}. After 4: {0, 2, 4, 6, 7, 9, 11}. After 1: every sum 0..11.
- Largest `a <= 11` is 11. Last stone `23 - 22 = 1`. (Total is odd, so 0 is impossible.)

**Code:**
```python
import random, itertools, sys
from functools import cache

random.seed(30)
INF = float('inf')

def last_stone_ii(stones):
    """Split into two groups with sums a <= b: last stone = b - a = total - 2a. Maximise a <= total // 2 by subset sums."""
    total = sum(stones); half = total // 2
    can = [True] + [False] * half               # can[s]: some subset sums to s
    for x in stones:
        for s in range(half, x - 1, -1):         # downward: each stone used at most once
            if can[s - x]: can[s] = True
    a = max(s for s in range(half + 1) if can[s])
    return total - 2 * a

def bitset(stones):
    total = sum(stones); bits = 1
    for x in stones: bits |= bits << x
    h = total // 2
    while not bits >> h & 1: h -= 1
    return total - 2 * h

def memo_subset(stones):
    total = sum(stones); half = total // 2; n = len(stones)
    @cache
    def best(i, cap):                            # largest subset sum <= cap using stones[i:]
        if i == n: return 0
        r = best(i + 1, cap)
        if stones[i] <= cap: r = max(r, stones[i] + best(i + 1, cap - stones[i]))
        return r
    return total - 2 * best(0, half)

def signs(stones):
    n = len(stones); best = INF
    for mask in range(1 << n):
        s = sum(x if mask >> i & 1 else -x for i, x in enumerate(stones))
        best = min(best, abs(s))
    return best

def smashes(stones):
    """Every sequence of smashes (choose any two stones each time)."""
    @cache
    def f(state):
        if len(state) <= 1: return state[0] if state else 0
        best = INF
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                rest = list(state[:i] + state[i + 1:j] + state[j + 1:])
                d = state[j] - state[i]
                if d: rest.append(d)
                best = min(best, f(tuple(sorted(rest))))
        return best
    return f(tuple(sorted(stones)))

for st, exp in [([2, 7, 4, 1, 8, 1], 1), ([31, 26, 33, 21, 40], 5), ([5], 5), ([3, 3], 0), ([1, 2, 5], 2)]:
    assert last_stone_ii(st) == bitset(st) == memo_subset(st) == signs(st) == smashes(st) == exp, st
    print('example', st, '->', exp)

st = [2, 7, 4, 1, 8, 1]; total = sum(st); half = total // 2
can = [True] + [False] * half
print('total', total, 'half', half, '; reachable subset sums 0..', half, 'after each stone:')
for x in st:
    for s in range(half, x - 1, -1):
        if can[s - x]: can[s] = True
    print(f'  after {x}:', [s for s in range(half + 1) if can[s]])
a = max(s for s in range(half + 1) if can[s])
print('best group sum a =', a, '-> last stone =', total, '-', 2 * a, '=', total - 2 * a)

n_cases = 0
for _ in range(500):
    n = random.randint(1, 7); st = [random.randint(1, 12) for _ in range(n)]
    want = smashes(st)
    assert last_stone_ii(st) == bitset(st) == memo_subset(st) == want == signs(st), st
    n_cases += 1
print('cross-check cases (len <= 7)', n_cases, ': subset-sum DP == bitset == memo == every smash order == all sign assignments')
for _ in range(200):
    st = [random.randint(1, 30) for _ in range(random.randint(1, 14))]
    assert last_stone_ii(st) == signs(st) == bitset(st)
print('200 more (len <= 14) against all sign assignments')

big = [random.randint(1, 100) for _ in range(30)]
print('n = 30, values <= 100 ->', last_stone_ii(big), '(total', sum(big), ')')
print('limit', sys.getrecursionlimit(), '- memo recursion depth is len(stones) <= 30, far below it')
assert last_stone_ii([100] * 30) == 0 and last_stone_ii([1]) == 1 and last_stone_ii([1, 100]) == 99
print('edge asserts passed')
```

**Output (my run):**
```
example [2, 7, 4, 1, 8, 1] -> 1
example [31, 26, 33, 21, 40] -> 5
example [5] -> 5
example [3, 3] -> 0
example [1, 2, 5] -> 2
total 23 half 11 ; reachable subset sums 0.. 11 after each stone:
  after 2: [0, 2]
  after 7: [0, 2, 7, 9]
  after 4: [0, 2, 4, 6, 7, 9, 11]
  after 1: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
  after 8: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
  after 1: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
best group sum a = 11 -> last stone = 23 - 22 = 1
cross-check cases (len <= 7) 500 : subset-sum DP == bitset == memo == every smash order == all sign assignments
200 more (len <= 14) against all sign assignments
n = 30, values <= 100 -> 1 (total 1779 )
limit 1000 - memo recursion depth is len(stones) <= 30, far below it
edge asserts passed
```

**Edge cases:**
- One stone: itself (`[5] -> 5`).
- Two equal stones: 0.
- One huge stone and small ones: the small ones cannot cancel it (`[1, 100] -> 99`).
- Total odd: answer is at least 1.
- Loop direction: `range(half, x - 1, -1)`; forgetting `x - 1` lower bound would index negative.

**Follow-ups:**
- "Return the groups?" Keep a parent array or a 2D boolean table and walk back.
- "Why not smash the two heaviest?" That is a fixed order (Part 8 Q18), and it can give a larger last stone than the best order.
- "Values up to 10^9?" Subset sums no longer fit in a table; meet in the middle for n <= 40.

**Common mistakes:**
- Using the upward loop (items reusable).
- Searching up to `total` instead of `total // 2` and picking the wrong `a`.
- Answering `total % 2` (parity only), which ignores whether the sum is reachable.
- Simulating greedy smashes of the two largest stones.

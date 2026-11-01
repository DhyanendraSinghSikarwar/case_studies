### Q11 ⭐⭐⭐ 🟡 Partition equal subset sum. `nums` has 1 <= len <= 200 positive integers (each <= 100). Return True if the list can be split into two groups with equal sums, else False. Reduce it to subset sum with target total/2 (False at once if the total is odd) and give both the boolean table and the Python big-int bitset trick `bits |= bits << x`. Say why iterating the capacity downward matters in the 1D table. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsets (len <= 12) on small inputs. Example: nums=[1, 5, 11, 5] -> True; nums=[1, 2, 3, 5] -> False; nums=[2] -> False; nums=[3, 3] -> True.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Subset sum on a 1D boolean table (0/1 knapsack, decision form). Two equal halves means one half sums to total/2.

**Say this first (1 line):** "If the total is odd, answer False. Otherwise I ask: can some subset reach total/2? That is a boolean 0/1 knapsack, and the capacity loop must go downward."

**Brute force:** Try all 2^n subsets and test 2 * sum == total. Fine for n <= 12 (the oracle), hopeless for n = 200.

**Optimal:**
- State: `dp[t]` = True if some subset of the items seen so far sums to exactly t. Size total/2 + 1.
- Base: `dp[0] = True` (the empty subset).
- Transition for item x: `dp[t] = dp[t] or dp[t - x]`, for t from target down to x.
- Why downward: `dp[t - x]` must still mean "before this item". Going upward, `dp[t - x]` may already have used x, so one item is counted many times. Example `[1, 5]`: total 6, target 3. Upward says True (1+1+1). Truth is False.
- Bitset: bit t of a Python int means "sum t reachable". `bits |= bits << x` does the whole row in one big-int operation, and the shift reads the old `bits` first, so it is naturally "downward". Answer is bit total/2.
- Top-down (memoised): `go(i, rem)`; depth is len(nums) <= 200, so the default recursion limit of 1000 is safe here. (At large n, memoised recursion raises RecursionError; see Q12.)
- Space: 1D table is O(total/2); the 2D table (item x sum) is not needed.

**Complexity:** Table: O(n * total/2) time, O(total/2) space. Max size: 200 items, total <= 20000, so about 2 million cell updates. Bitset: n shift-or operations on an integer of up to total bits, so about n * total / 64 word operations in theory.

**Dry run:** `[1, 5, 11, 5]`, total 22, target 11 (T = reachable, columns t = 0..11).
| after | row |
|---|---|
| start | `T...........` |
| item 1 | `TT..........` |
| item 5 | `TT...TT.....` |
| item 11 | `TT...TT....T` |
| item 5 | `TT...TT...TT` |
- dp[11] is True after item 11 (0 + 11). The other split is 1 + 5 + 5 = 11.

**Code:**
```python
import random
from functools import lru_cache

random.seed(11)

def can_partition(nums):
    """Optimal: boolean 1D table, capacity looped DOWNWARD. O(n * total/2) time, O(total/2) space."""
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [True] + [False] * target            # dp[t]: some subset of the items seen so far sums to t
    for x in nums:
        for t in range(target, x - 1, -1):     # downward: dp[t - x] is still the value from BEFORE this item
            if dp[t - x]:
                dp[t] = True
    return dp[target]

def can_partition_bits(nums):
    """Bitset: bit t of `bits` is set when sum t is reachable. One shift-or per item."""
    total = sum(nums)
    if total % 2:
        return False
    bits = 1
    for x in nums:
        bits |= bits << x
    return bool(bits >> (total // 2) & 1)

def can_partition_memo(nums):
    """Top-down: depth is len(nums) (<= 200 here), so the default recursion limit is fine for this one."""
    total = sum(nums)
    if total % 2:
        return False
    @lru_cache(maxsize=None)
    def go(i, rem):
        if rem == 0:
            return True
        if i == len(nums) or rem < 0:
            return False
        return go(i + 1, rem - nums[i]) or go(i + 1, rem)
    return go(0, total // 2)

def can_partition_upward_bug(nums):
    """Same table, capacity loop UPWARD: an item can be reused, so it answers a different question."""
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [True] + [False] * target
    for x in nums:
        for t in range(x, target + 1):
            if dp[t - x]:
                dp[t] = True
    return dp[target]

def brute(nums):
    """Oracle: enumerate every subset, test 2 * sum == total."""
    n, total = len(nums), sum(nums)
    return any(2 * sum(nums[i] for i in range(n) if m >> i & 1) == total for m in range(1 << n))

# prompt examples
for nums, want in [([1, 5, 11, 5], True), ([1, 2, 3, 5], False), ([2], False), ([3, 3], True)]:
    assert can_partition(nums) is want and can_partition_bits(nums) is want and can_partition_memo(nums) is want and brute(nums) is want
print('4 prompt examples ok')

# table walk-through on the first example: total 22, target 11
nums = [1, 5, 11, 5]
target = sum(nums) // 2
dp = [True] + [False] * target
print('target =', target, '  columns t = 0..%d' % target)
print('start    ', ''.join('T' if v else '.' for v in dp))
for x in nums:
    for t in range(target, x - 1, -1):
        if dp[t - x]:
            dp[t] = True
    print('item %-4d' % x, ''.join('T' if v else '.' for v in dp))
bits = 1
for x in [1, 5, 11, 5]:
    bits |= bits << x
    print('bitset after item %-3d (bit 0 on the right): %s' % (x, bin(bits)[2:]))

# why DOWNWARD: [1, 5] has total 6, target 3, and no subset sums to 3
print('nums=[1, 5]: correct', can_partition([1, 5]), ' upward-loop', can_partition_upward_bug([1, 5]), ' (the upward loop used the 1 three times)')

# seeded cross-check against subset enumeration (len <= 12)
trues = 0
wrong_upward = 0
for _ in range(600):
    nums = [random.randint(1, 12) for _ in range(random.randint(1, 12))]
    b = brute(nums)
    assert can_partition(nums) == b == can_partition_bits(nums) == can_partition_memo(nums), nums
    trues += b
    wrong_upward += can_partition_upward_bug(nums) != b
print('600 random cases agree (table = bitset = memo = enumeration); True in', trues, 'of them; upward-loop bug wrong in', wrong_upward)

# edge cases
assert can_partition([1]) is False and can_partition([1, 1]) is True and can_partition([100] * 200) is True
assert can_partition([100] * 199 + [99]) is False          # odd total
assert can_partition_bits([100] * 200) is True
big = [random.randint(1, 100) for _ in range(200)]
assert can_partition(big) == can_partition_bits(big) == can_partition_memo(big)
print('edge cases ok; max-size random input ->', can_partition(big))
```

**Output (my run):**
```
4 prompt examples ok
target = 11   columns t = 0..11
start     T...........
item 1    TT..........
item 5    TT...TT.....
item 11   TT...TT....T
item 5    TT...TT...TT
bitset after item 1   (bit 0 on the right): 11
bitset after item 5   (bit 0 on the right): 1100011
bitset after item 11  (bit 0 on the right): 110001100001100011
bitset after item 5   (bit 0 on the right): 11000110001110001100011
nums=[1, 5]: correct False  upward-loop True  (the upward loop used the 1 three times)
600 random cases agree (table = bitset = memo = enumeration); True in 202 of them; upward-loop bug wrong in 46
edge cases ok; max-size random input -> True
```

**Edge cases:**
- Odd total: False at once.
- Single item: False (total/2 is not reachable), `[3, 3]` True.
- All items bigger than target: the inner loop does nothing; the answer comes from the initial state.
- 200 items of 100: target 10000, works, bitset has 20001 bits.

**Follow-ups:**
- Print the split? Keep the 2D table (or parent pointers) and walk back, or see the reconstruction in Q37.
- Faster? Bitset: Python's big-int shift is C-speed. Complexity in theory O(n * total / 64).
- Min difference of two groups? Same table; scan the reachable sums nearest to total/2 (Q30).

**Common mistakes:**
- Upward capacity loop (reuses an item).
- Forgetting the odd-total shortcut.
- Using `bits << x` into a new variable and then discarding it.
- Putting the whole total, not total/2, as the table size (wastes time, not wrong).

### Q12 ⭐⭐⭐ 🟡 House robber II (circular street). `nums` has 1 <= len <= 10^5 non-negative integers (each <= 400) arranged in a circle, so the first and last houses are adjacent (a single house is just itself). You cannot take two adjacent houses; return the maximum total. Reduce it to two linear problems and say which two ranges, and why every valid choice is covered. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a subset enumeration with the circular no-two-adjacent rule (len <= 12) on small inputs. Example: nums=[2, 3, 2] -> 3; nums=[1, 2, 3, 1] -> 4; nums=[7] -> 7; nums=[5, 1] -> 5; nums=[4, 1, 1, 4] -> 5.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Linear house robber (1D DP) run twice, because a circle breaks the problem into two lines.

**Say this first (1 line):** "In a circle, house 0 and house n-1 are neighbours, so I never take both. I solve two linear problems, houses 0..n-2 and houses 1..n-1, and take the max."

**Brute force:** Enumerate all 2^n subsets, reject any with two circular neighbours. Fine up to n = 12 (the oracle).

**Optimal:**
- Linear state: `best[i]` = best total using houses 0..i. Transition: `best[i] = max(best[i-1], best[i-2] + nums[i])` (skip i, or take i and skip i-1). Base: `best[-1] = best[-2] = 0`.
- Circular: answer = max(rob_line(nums[:-1]), rob_line(nums[1:])). Single house: return it (the two ranges would be empty).
- Why it covers everything: a valid circular selection cannot contain both house 0 and house n-1, so it lies inside one of the two ranges. Conversely, any linear-valid choice inside a range is circular-valid, because each range excludes one of the two end houses. So the max of the two is exactly the circular answer. I checked n = 2..12 exhaustively.
- Bottom-up with two variables: O(1) space.
- Recursion limit: the memoised top-down `best(i)` nests about n deep. At n = 10^5 it raises RecursionError under the default limit of 1000. Bottom-up is required.

**Complexity:** Time O(n) (two passes). Space O(1) for the bottom-up version (slices cost O(n), use index bounds to avoid them).

**Dry run:** `[2, 3, 2]`.
- Range A = houses 0..1 = `[2, 3]`: best = `[2, 3]`, so 3.
- Range B = houses 1..2 = `[3, 2]`: best = `[3, 3]`, so 3.
- Answer max(3, 3) = 3. The linear answer on all three would be 4 (2 + 2), which takes both ends: illegal on a circle.

**Code:**
```python
import random
import itertools
from functools import lru_cache

random.seed(12)

def rob_line(nums):
    """Linear house robber, bottom-up, O(1) space: best[i] = max(best[i-1], best[i-2] + nums[i])."""
    prev2, prev1 = 0, 0                 # best for the prefixes of length i-2 and i-1
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1

def rob_circle(nums):
    """Circular: house 0 and house n-1 are neighbours, so one of them is skipped. Try both ranges."""
    if len(nums) == 1:
        return nums[0]
    return max(rob_line(nums[:-1]), rob_line(nums[1:]))

def rob_circle_memo(nums):
    """Top-down version of the same thing. Fine for small n; nests ~n deep, so it breaks past the recursion limit."""
    def solve(arr):
        @lru_cache(maxsize=None)
        def best(i):                    # best total using houses 0..i of arr
            if i < 0:
                return 0
            return max(best(i - 1), best(i - 2) + arr[i])
        return best(len(arr) - 1)
    if len(nums) == 1:
        return nums[0]
    return max(solve(tuple(nums[:-1])), solve(tuple(nums[1:])))

def brute(nums):
    """Oracle: every subset, valid only if no two chosen houses are neighbours around the circle."""
    n, best = len(nums), 0
    for mask in range(1 << n):
        if n > 1 and any(mask >> i & 1 and mask >> ((i + 1) % n) & 1 for i in range(n) if (i + 1) % n != i):
            continue
        best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best

for nums, want in [([2, 3, 2], 3), ([1, 2, 3, 1], 4), ([7], 7), ([5, 1], 5), ([4, 1, 1, 4], 5)]:
    assert rob_circle(nums) == rob_circle_memo(nums) == brute(nums) == want, nums
print('5 prompt examples ok')

# table walk-through on [2, 3, 2]: range A = houses 0..1 = [2, 3], range B = houses 1..2 = [3, 2]
def table(arr):
    best = []
    for i, x in enumerate(arr):
        best.append(max(best[i - 1] if i >= 1 else 0, (best[i - 2] if i >= 2 else 0) + x))
    return best
nums = [2, 3, 2]
print('range A nums[:-1] =', nums[:-1], 'best =', table(nums[:-1]))
print('range B nums[1:]  =', nums[1:], 'best =', table(nums[1:]))
print('answer = max(%d, %d) = %d' % (table(nums[:-1])[-1], table(nums[1:])[-1], rob_circle(nums)))
print('the (wrong) line answer 2+2 on [2,3,2] would be', rob_line(nums), '- it takes both ends, which are neighbours in a circle')

# claim: every valid circular choice skips house 0 or skips house n-1 (so the two ranges cover everything)
for n in range(2, 13):
    for mask in range(1 << n):
        valid = all(not (mask >> i & 1 and mask >> ((i + 1) % n) & 1) for i in range(n))
        if valid:
            assert not (mask & 1 and mask >> (n - 1) & 1)
print('claim checked for n = 2..12: no valid circular selection holds both house 0 and house n-1')

# exhaustive: every list of length 1..6 with values 0..3
count = 0
for n in range(1, 7):
    for nums in itertools.product(range(4), repeat=n):
        assert rob_circle(list(nums)) == brute(list(nums)), nums
        count += 1
print('exhaustive small inputs agree:', count)

# seeded random cross-check, len <= 12
for _ in range(500):
    nums = [random.randint(0, 400) for _ in range(random.randint(1, 12))]
    assert rob_circle(nums) == rob_circle_memo(nums) == brute(nums), nums
print('500 random cases agree (bottom-up = memo = subset enumeration)')

# recursion limit: memoised top-down at large n
big = [random.randint(0, 400) for _ in range(10**5)]
try:
    rob_circle_memo(big)
    print('memo at n=10^5: no error (unexpected)')
except RecursionError:
    print('memo at n=10^5: RecursionError under the default limit')
print('bottom-up at n=10^5 ->', rob_circle(big))

# edge cases
assert rob_circle([0]) == 0 and rob_circle([0, 0]) == 0 and rob_circle([9, 9, 9]) == 9
assert rob_circle([1, 2, 3, 4, 5, 6]) == brute([1, 2, 3, 4, 5, 6]) == 12
print('edge cases ok')
```

**Output (my run):**
```
5 prompt examples ok
range A nums[:-1] = [2, 3] best = [2, 3]
range B nums[1:]  = [3, 2] best = [3, 3]
answer = max(3, 3) = 3
the (wrong) line answer 2+2 on [2,3,2] would be 4 - it takes both ends, which are neighbours in a circle
claim checked for n = 2..12: no valid circular selection holds both house 0 and house n-1
exhaustive small inputs agree: 5460
500 random cases agree (bottom-up = memo = subset enumeration)
memo at n=10^5: RecursionError under the default limit
bottom-up at n=10^5 -> 11717802
edge cases ok
```

**Edge cases:**
- One house: itself. Two houses: the larger one (each range is one house).
- All zeros: 0.
- n = 10^5: bottom-up is fine, memo raises RecursionError.

**Follow-ups:**
- Tree-shaped street? That is House Robber III, Part 7 Q45.
- Return which houses? Keep `best` as a list and walk back in the winning range.
- Why not "rob_line(nums) minus something"? You cannot patch a line answer; rerun on the two ranges.

**Common mistakes:**
- Forgetting the single-house case (both slices are empty, answer 0).
- Taking `max(nums[0], ...)` hacks instead of two clean ranges.
- Relying on `sys.setrecursionlimit` for n = 10^5 (can crash the interpreter).

### Q13 ⭐⭐⭐ 🟡 Maximum product subarray. `nums` has 1 <= len <= 2*10^4 integers (|value| <= 10, zeros and negatives allowed). Return the largest product of a non-empty contiguous subarray (Python integers do not overflow). Keep both the maximum and the minimum product ending at each index and say why the minimum is needed (a negative number flips them) and what a zero does. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an O(n^2) enumeration of every subarray on small inputs. Example: nums=[2, 3, -2, 4] -> 6; nums=[-2, 0, -1] -> 0; nums=[-3] -> -3; nums=[-2, 3, -4] -> 24; nums=[0, 2] -> 2.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Kadane-style 1D DP with two states (max and min product ending at i).

**Say this first (1 line):** "A negative number flips max and min, so I keep both the largest and smallest product of a subarray ending at i. A zero resets them."

**Brute force:** For every start, extend with a running product and track the best. O(n^2) time, O(1) space. It is the oracle.

**Optimal:**
- State: `hi[i]` / `lo[i]` = max / min product of a subarray that ends exactly at i.
- Transition: candidates are `x` (start fresh), `hi[i-1] * x`, `lo[i-1] * x`. Then `hi = max(cands)`, `lo = min(cands)`.
- Why the min: a big negative `lo` times a negative x becomes the new max. Max-only fails on `[-2, 3, -4]` (gives 3, truth 24); over all lists of length <= 6 with values -3..3 the max-only version was wrong on 76246 of 137256.
- Zero: candidates are 0, 0, 0 so hi = lo = 0, and the next element starts fresh via the candidate `x`.
- Base: `hi = lo = best = nums[0]` (non-empty subarray, so all-negative lists return the least negative number).
- Python ints do not overflow (the 2*10^4-element answer has 81 digits here).
- Memoised version: `ending(i)` nests n deep; at n = 2*10^4 it raises RecursionError under the default limit. Bottom-up is required.

**Complexity:** O(n) time, O(1) space.

**Dry run:** `[2, 3, -2, 4]`.
| i | x | max_end | min_end | best |
|---|---|---|---|---|
| 0 | 2 | 2 | 2 | 2 |
| 1 | 3 | 6 | 3 | 6 |
| 2 | -2 | -2 | -12 | 6 |
| 3 | 4 | 4 | -48 | 6 |
- At i=2 the old max 6 times -2 is -12, which becomes the min; the max is just -2 (fresh start).
- Zero trace `[-2, 0, -1]`: both states become 0 at the zero, best stays 0.

**Code:**
```python
import random
import itertools
from functools import lru_cache

random.seed(13)

def max_product(nums):
    """Optimal: keep the max AND min product of a subarray ending here. O(n) time, O(1) space."""
    best = hi = lo = nums[0]
    for x in nums[1:]:
        cands = (x, hi * x, lo * x)      # start fresh at x, or extend the old max / old min
        hi, lo = max(cands), min(cands)
        best = max(best, hi)
    return best

def max_product_no_min(nums):
    """The tempting bug: track only the maximum."""
    best = hi = nums[0]
    for x in nums[1:]:
        hi = max(x, hi * x)
        best = max(best, hi)
    return best

def max_product_memo(nums):
    """Top-down: (max, min) ending at i. Nests n deep."""
    @lru_cache(maxsize=None)
    def ending(i):
        if i == 0:
            return nums[0], nums[0]
        hi, lo = ending(i - 1)
        c = (nums[i], hi * nums[i], lo * nums[i])
        return max(c), min(c)
    ending(len(nums) - 1)                # ask for the LAST index first: the recursion goes n deep
    return max(ending(i)[0] for i in range(len(nums)))

def brute(nums):
    """Oracle: every subarray, O(n^2) with a running product."""
    best = nums[0]
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            best = max(best, p)
    return best

for nums, want in [([2, 3, -2, 4], 6), ([-2, 0, -1], 0), ([-3], -3), ([-2, 3, -4], 24), ([0, 2], 2)]:
    assert max_product(nums) == max_product_memo(nums) == brute(nums) == want, nums
print('5 prompt examples ok')

# table walk-through on [2, 3, -2, 4]
nums = [2, 3, -2, 4]
print('i  x   max_end  min_end  best')
best = hi = lo = nums[0]
print('0  %-3d %-8d %-8d %d' % (nums[0], hi, lo, best))
for i in range(1, len(nums)):
    x = nums[i]
    c = (x, hi * x, lo * x)
    hi, lo = max(c), min(c)
    best = max(best, hi)
    print('%d  %-3d %-8d %-8d %d' % (i, x, hi, lo, best))
print('zero resets both: trace on [-2, 0, -1]')
hi = lo = best = -2
print('  i=0 x=-2 max_end=-2 min_end=-2')
for i, x in enumerate([0, -1], start=1):
    c = (x, hi * x, lo * x)
    hi, lo = max(c), min(c)
    best = max(best, hi)
    print('  i=%d x=%-2d max_end=%d min_end=%d best=%d' % (i, x, hi, lo, best))
print('[-2, 3, -4]: with min ->', max_product([-2, 3, -4]), ' max-only ->', max_product_no_min([-2, 3, -4]))

# exhaustive: all lists of length 1..6 with values -3..3
count = bad_no_min = 0
for n in range(1, 7):
    for nums in itertools.product(range(-3, 4), repeat=n):
        nums = list(nums)
        assert max_product(nums) == brute(nums), nums
        bad_no_min += max_product_no_min(nums) != brute(nums)
        count += 1
print('exhaustive small inputs agree:', count, '; max-only variant wrong on', bad_no_min)

# seeded random cross-check
for _ in range(500):
    nums = [random.randint(-6, 6) for _ in range(random.randint(1, 12))]
    assert max_product(nums) == max_product_memo(nums) == brute(nums), nums
print('500 random cases agree (bottom-up = memo = O(n^2) enumeration)')

# recursion limit at large n
big = [random.randint(-10, 10) for _ in range(2 * 10**4)]
try:
    max_product_memo(big)
    print('memo at n=2*10^4: no error (unexpected)')
except RecursionError:
    print('memo at n=2*10^4: RecursionError under the default limit')
print('bottom-up at n=2*10^4 has', len(str(max_product(big))), 'digit answer (Python ints do not overflow)')
assert max_product([-1] * 3) == 1 and max_product([0]) == 0 and max_product([-2, -3]) == 6 and max_product([0, 0, -1]) == 0
print('edge cases ok')
```

**Output (my run):**
```
5 prompt examples ok
i  x   max_end  min_end  best
0  2   2        2        2
1  3   6        3        6
2  -2  -2       -12      6
3  4   4        -48      6
zero resets both: trace on [-2, 0, -1]
  i=0 x=-2 max_end=-2 min_end=-2
  i=1 x=0  max_end=0 min_end=0 best=0
  i=2 x=-1 max_end=0 min_end=-1 best=0
[-2, 3, -4]: with min -> 24  max-only -> 3
exhaustive small inputs agree: 137256 ; max-only variant wrong on 76246
500 random cases agree (bottom-up = memo = O(n^2) enumeration)
memo at n=2*10^4: RecursionError under the default limit
bottom-up at n=2*10^4 has 81 digit answer (Python ints do not overflow)
edge cases ok
```

**Edge cases:**
- Single negative: itself. Single zero: 0.
- Two negatives: product positive (`[-2, -3]` -> 6).
- Zeros split the array into independent segments.

**Follow-ups:**
- Why not prefix products? Zeros and sign flips break division; the two-state DP avoids it.
- Max sum instead? That is Kadane (Q3).
- Circular? Not defined for products in the usual form; the sum version is Q26.

**Common mistakes:**
- Overwriting `hi` before computing `lo` from the old `hi` (use a tuple of candidates).
- Initialising `best = 0` (wrong for all-negative lists).
- Max-only tracking.

### Q14 ⭐⭐ 🟢 Fibonacci three ways: plain recursion, memoisation, bottom-up. Define fib(0) = 0, fib(1) = 1, fib(k) = fib(k-1) + fib(k-2), for 0 <= n <= 25. Return `[fib(n), naive_calls, memo_calls]` where `naive_calls` is the number of calls (counting the first) made by the plain recursive function, and `memo_calls` is the number of calls (counting the first and the ones answered from the cache) made by this memoised function: `def fib(k): count += 1; if k < 2: return k; if k in memo: return memo[k]; memo[k] = fib(k-1) + fib(k-2); return memo[k]` (the check of memo happens after the base case). Then explain the O(1)-space bottom-up loop and why naive calls grow exponentially while memo calls grow linearly. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against the counted recursive functions themselves (n <= 20) on small inputs. Example: n=0 -> [0, 1, 1]; n=1 -> [1, 1, 1]; n=2 -> [1, 3, 3]; n=10 -> [55, 177, 19]; n=25 -> [75025, 242785, 49].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Overlapping subproblems made visible: plain recursion versus memoisation versus bottom-up.

**Say this first (1 line):** "Plain recursion recomputes the same fib(k) exponentially often; a cache makes it linear; a two-variable loop makes it linear with O(1) space."

**Brute force:** The plain recursive function `fib(k-1) + fib(k-2)`. Calls: c(0) = c(1) = 1, c(k) = 1 + c(k-1) + c(k-2). This equals 2*fib(k+1) - 1 (checked for k = 0..25), and grows by the golden ratio 1.618 per step: exponential.

**Optimal:**
- Memoised function from the prompt (base case checked first, then the cache). Count: m(0) = m(1) = 1. For k >= 2 the call does one call chain for k-1 (which fills the cache down to the bottom) and then one call for k-2, which is answered from the cache or is a base case: m(k) = m(k-1) + 2, so m(n) = 2n - 1 for n >= 1.
- Bottom-up: `a, b = 0, 1; repeat n times: a, b = b, a + b`. O(n) time, O(1) space, no recursion.
- Recursion limit: the memoised version is O(n) calls but also n deep. At n = 5000 it raises RecursionError under the default limit; bottom-up does not.
- The answer is `[fib(n), naive_calls, memo_calls]`; I get naive_calls from its recurrence and memo_calls from 2n - 1, and the cross-check runs the actual counted functions.

**Complexity:** My function: O(n) time, O(1) space. The plain recursion is O(phi^n) time, O(n) stack. The memo is O(n) time and O(n) space (cache and stack).

**Dry run:** n = 0: one call, base case: `[0, 1, 1]`. n = 2: fib(2) calls fib(1) and fib(0), both base: 3 calls either way. n = 4: naive 9 calls (fib(2) is computed twice, fib(1) three times), memo 7. The table in the output shows k = 0..10, ending `55, 177, 19`.

**Code:**
```python
import random

random.seed(14)

def fib_three(n):
    """Optimal: bottom-up for the value (O(1) space) and recurrences for the two call counts."""
    a, b = 0, 1                       # fib(0), fib(1)
    for _ in range(n):
        a, b = b, a + b
    # naive calls: c(0) = c(1) = 1, c(k) = 1 + c(k-1) + c(k-2)
    c_prev, c_cur = 1, 1
    for _ in range(n - 1):
        c_prev, c_cur = c_cur, 1 + c_prev + c_cur
    naive = 1 if n < 2 else c_cur
    # memo calls: the first call is 1; each new k >= 2 makes two child calls; derived below, equals 2n - 1 for n >= 1
    memo = 1 if n == 0 else 2 * n - 1
    return [a, naive, memo]

def counted_recursions(n):
    """Oracle: run the two functions from the prompt and count their calls."""
    count = [0]
    def naive(k):
        count[0] += 1
        return k if k < 2 else naive(k - 1) + naive(k - 2)
    value = naive(n)
    naive_calls = count[0]
    count[0] = 0
    memo = {}
    def memoised(k):
        count[0] += 1
        if k < 2:
            return k
        if k in memo:
            return memo[k]
        memo[k] = memoised(k - 1) + memoised(k - 2)
        return memo[k]
    assert memoised(n) == value
    return [value, naive_calls, count[0]]

for n, want in [(0, [0, 1, 1]), (1, [1, 1, 1]), (2, [1, 3, 3]), (10, [55, 177, 19]), (25, [75025, 242785, 49])]:
    assert fib_three(n) == want, n
    assert counted_recursions(n) == want, n
print('5 prompt examples ok')

# walk-through: n = 2 (first call fib(2) -> fib(1), fib(0))
print('n=2 naive: fib(2) -> fib(1) base, fib(0) base = 3 calls; memo: same 3 calls, nothing cached yet')
# and n = 5 call table
print('k   fib(k)  naive_calls  memo_calls')
for k in range(0, 11):
    v, nv, mm = fib_three(k)
    print('%-3d %-7d %-12d %d' % (k, v, nv, mm))

# growth: naive ratio tends to the golden ratio, memo grows by 2 per step
ratios = [fib_three(k)[1] / fib_three(k - 1)[1] for k in (10, 20, 25)]
print('naive_calls(k)/naive_calls(k-1) at k=10,20,25:', [round(r, 4) for r in ratios], '(golden ratio 1.6180)')
print('naive_calls(k) = 2*fib(k+1) - 1 ?', all(fib_three(k)[1] == 2 * fib_three(k + 1)[0] - 1 for k in range(0, 26)))

# seeded random cross-check, n <= 20, plus every n
for n in range(0, 21):
    assert fib_three(n) == counted_recursions(n), n
for _ in range(300):
    n = random.randint(0, 20)
    assert fib_three(n) == counted_recursions(n)
print('all n in 0..20 and 300 random draws agree with the counted recursive functions')

# recursion limit: the memoised function is O(n) calls but also O(n) DEEP
def deep_memo(n):
    memo = {}
    def f(k):
        if k < 2:
            return k
        if k in memo:
            return memo[k]
        memo[k] = f(k - 1) + f(k - 2)
        return memo[k]
    return f(n)
try:
    deep_memo(5000)
    print('memo fib(5000): no error (unexpected)')
except RecursionError:
    print('memo fib(5000): RecursionError under the default limit; bottom-up gives', len(str(fib_three(5000)[0])), 'digits')
assert fib_three(0)[0] == 0 and fib_three(1)[0] == 1
print('edge cases ok')
```

**Output (my run):**
```
5 prompt examples ok
n=2 naive: fib(2) -> fib(1) base, fib(0) base = 3 calls; memo: same 3 calls, nothing cached yet
k   fib(k)  naive_calls  memo_calls
0   0       1            1
1   1       1            1
2   1       3            3
3   2       5            5
4   3       9            7
5   5       15           9
6   8       25           11
7   13      41           13
8   21      67           15
9   34      109          17
10  55      177          19
naive_calls(k)/naive_calls(k-1) at k=10,20,25: [1.6239, 1.6181, 1.618] (golden ratio 1.6180)
naive_calls(k) = 2*fib(k+1) - 1 ? True
all n in 0..20 and 300 random draws agree with the counted recursive functions
memo fib(5000): RecursionError under the default limit; bottom-up gives 1045 digits
edge cases ok
```

**Edge cases:**
- n = 0 and n = 1: one call each.
- n = 25: 242785 naive calls versus 49 memo calls.
- Large n: Python ints are exact (fib(5000) has 1045 digits).

**Follow-ups:**
- Faster than O(n)? Matrix power or fast doubling gives O(log n) big-int steps.
- Modulo? Reduce each addition.
- Climbing stairs (Q1) is the same recurrence shifted by one.

**Common mistakes:**
- Checking the cache before the base case (changes the call count by the prompt's definition).
- Forgetting the first call in the count.
- Claiming memoisation is O(1) space: it is O(n).

### Q15 ⭐⭐ 🟡 Paint fence (counting with a modulus). There are `n` posts (1 <= n <= 10^5) and `k` colours (1 <= k <= 10^9). Paint every post so that no three consecutive posts share a colour. Return the number of ways modulo 10^9 + 7. Use the two states 'last two posts the same' and 'last two posts different'. State the answer for k = 1 (1 for n = 1 or 2, else 0). Say where the modulus is applied (after every multiplication and addition) and why you may not take the modulus of the inputs mid-way in a comparison. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all colourings (n <= 7, k <= 4) on small inputs. Example: n=1, k=5 -> 5; n=3, k=2 -> 6; n=7, k=2 -> 42; n=3, k=1 -> 0; n=100000, k=1000000000 -> 910929812.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Counting DP with two states (same as previous, different from previous), modulus.

**Say this first (1 line):** "At each post the last two are either the same or different; same can only follow different, and different has k-1 choices after anything."

**Brute force:** Enumerate all k^n colourings and reject any with three equal in a row (n <= 7, k <= 4 here).

**Optimal:**
- State: `same[i]` = ways for posts 1..i where posts i and i-1 share a colour; `diff[i]` = ways where they differ.
- Base: post 1: `same = 0`, `diff = k`.
- Transition: `same[i] = diff[i-1]` (copy the previous colour; allowed only if i-1 and i-2 differed, else three in a row). `diff[i] = (same[i-1] + diff[i-1]) * (k - 1)`.
- Answer: `same[n] + diff[n]`, modulo 10^9+7.
- k = 1 falls out of the recurrence: n = 1 -> 1, n = 2 -> 1, n >= 3 -> 0.
- One-state form: `total[i] = (k-1) * (total[i-1] + total[i-2])`; I checked it agrees.
- Modulus: reduce after every multiplication and addition (the exact count has about 30 bits more per post: 59795 bits at n = 2000). Use reduced numbers only inside arithmetic. Never use a reduced value in a comparison or ordering (a count of M+5 reduces to 5).
- Recursion limit: top-down `go(i)` nests n deep; at n = 10^5 it raises RecursionError. Bottom-up is required.

**Complexity:** O(n) time, O(1) space.

**Dry run:** n = 3, k = 2.
| post | same | diff | total |
|---|---|---|---|
| 1 | 0 | 2 | 2 |
| 2 | 2 | 2 | 4 |
| 3 | 2 | 4 | 6 |
- Total 6 = 8 colourings minus AAA and BBB.

**Code:**
```python
import random
import itertools
from functools import lru_cache

random.seed(15)
M = 10**9 + 7

def paint_fence(n, k):
    """Optimal: two states per post. O(n) time, O(1) space, modulus after every product/sum."""
    same, diff = 0, k                 # post 1: it cannot be 'same as previous'; k choices, all 'different'
    for _ in range(2, n + 1):
        same, diff = diff, (same + diff) * (k - 1) % M
        # same[i] = diff[i-1]            (copy the colour of post i-1, allowed only if i-1 and i-2 differed)
        # diff[i] = total[i-1] * (k-1)   (pick any colour except the previous post's)
    return (same + diff) % M

def paint_fence_memo(n, k):
    """Top-down, same recurrence. Nests n deep."""
    @lru_cache(maxsize=None)
    def go(i):                        # returns (same, diff) for posts 1..i
        if i == 1:
            return 0, k % M
        same, diff = go(i - 1)
        return diff, (same + diff) * (k - 1) % M
    s, d = go(n)
    return (s + d) % M

def brute(n, k):
    """Oracle: enumerate all k^n colourings and reject three equal in a row."""
    c = 0
    for col in itertools.product(range(k), repeat=n):
        if all(not (col[i] == col[i + 1] == col[i + 2]) for i in range(n - 2)):
            c += 1
    return c % M

for (n, k), want in [((1, 5), 5), ((3, 2), 6), ((7, 2), 42), ((3, 1), 0), ((100000, 10**9), 910929812)]:
    assert paint_fence(n, k) == want, (n, k)
    if n <= 7:
        assert brute(n, k) == want
print('5 prompt examples ok')

# table walk-through on n=1,k=5 and n=3,k=2
def rows(n, k):
    same, diff = 0, k
    out = [(1, same, diff, same + diff)]
    for i in range(2, n + 1):
        same, diff = diff, (same + diff) * (k - 1)
        out.append((i, same, diff, same + diff))
    return out
print('n=3, k=2 (no modulus needed at this size)')
print('post  same  diff  total')
for r in rows(3, 2):
    print('%-5d %-5d %-5d %d' % r)
print('n=1, k=5 -> total', rows(1, 5)[0][3], '(just k)')

# k = 1: 1 for n = 1 or 2, then 0
print('k=1, n=1..5 ->', [paint_fence(n, 1) for n in range(1, 6)])

# exhaustive over n <= 7, k <= 4, all three methods
count = 0
for n in range(1, 8):
    for k in range(1, 5):
        assert paint_fence(n, k) == paint_fence_memo(n, k) == brute(n, k), (n, k)
        count += 1
print('exhaustive n<=7, k<=4:', count, 'cases agree (bottom-up = memo = enumeration)')
for _ in range(200):
    n, k = random.randint(1, 7), random.randint(1, 4)
    assert paint_fence(n, k) == brute(n, k)

# alternative one-state recurrence: total[i] = (k-1) * (total[i-1] + total[i-2])
def alt(n, k):
    t1, t2 = k, k * k
    if n == 1:
        return t1 % M
    for _ in range(3, n + 1):
        t1, t2 = t2, (k - 1) * (t1 + t2) % M
    return t2 % M
assert all(alt(n, k) == paint_fence(n, k) for n in range(1, 40) for k in (1, 2, 3, 10**9))
print('one-state recurrence total[i] = (k-1)*(total[i-1] + total[i-2]) agrees')

# modulus: the exact big-int answer reduced once at the end equals the answer reduced after every step
def exact(n, k):
    same, diff = 0, k
    for _ in range(2, n + 1):
        same, diff = diff, (same + diff) * (k - 1)
    return same + diff
assert exact(2000, 10**9) % M == paint_fence(2000, 10**9)
print('n=2000, k=10^9: exact big int mod M equals the in-loop reduction:', exact(2000, 10**9) % M == paint_fence(2000, 10**9))
print('bits of the exact count at n=2000, k=10^9:', exact(2000, 10**9).bit_length(), '(why we reduce: it grows by about 30 bits per post)')
# the loop has no comparison on reduced values; a reduced number says nothing about order or equality of the true number
print('true value M+5 reduces to', (M + 5) % M, '-> a test like "if count_mod > other_mod" or "if count_mod == 5" would be wrong')

# recursion limit
try:
    paint_fence_memo(10**5, 10**9)
    print('memo at n=10^5: no error (unexpected)')
except RecursionError:
    print('memo at n=10^5: RecursionError under the default limit')
print('bottom-up n=10^5, k=10^9 ->', paint_fence(10**5, 10**9))
assert paint_fence(1, 1) == 1 and paint_fence(2, 1) == 1 and paint_fence(2, 3) == 9
print('edge cases ok')
```

**Output (my run):**
```
5 prompt examples ok
n=3, k=2 (no modulus needed at this size)
post  same  diff  total
1     0     2     2
2     2     2     4
3     2     4     6
n=1, k=5 -> total 5 (just k)
k=1, n=1..5 -> [1, 1, 0, 0, 0]
exhaustive n<=7, k<=4: 28 cases agree (bottom-up = memo = enumeration)
one-state recurrence total[i] = (k-1)*(total[i-1] + total[i-2]) agrees
n=2000, k=10^9: exact big int mod M equals the in-loop reduction: True
bits of the exact count at n=2000, k=10^9: 59795 (why we reduce: it grows by about 30 bits per post)
true value M+5 reduces to 5 -> a test like "if count_mod > other_mod" or "if count_mod == 5" would be wrong
memo at n=10^5: RecursionError under the default limit
bottom-up n=10^5, k=10^9 -> 910929812
edge cases ok
```

**Edge cases:**
- n = 1: k. n = 2: k^2 (no rule applies yet).
- k = 1: 1, 1, 0, 0, ...
- n = 10^5, k = 10^9: 910929812.

**Follow-ups:**
- No two adjacent the same? `k * (k-1)^(n-1)`; no DP needed.
- O(log n)? Matrix power of the 2x2 transition.
- Why not three states? Runs of three are forbidden, so run length 1 or 2 is all you track.

**Common mistakes:**
- Starting the loop at post 1 instead of post 2 (n = 1 must return k).
- Missing the `% M` on one of the two operations.
- Letting `same[i]` copy `same[i-1]` too (that allows three equal in a row).

### Q16 ⭐⭐ 🟡 Perfect squares (fewest squares summing to n). Given 1 <= n <= 10^4, return the minimum number of perfect squares (1, 4, 9, ...) that add up to n. Define `dp[i]`, the transition over squares j*j <= i, and the base case. This is coin change (Q6) with the coins 1, 4, 9, ...; state the time (the double loop is about n * sqrt(n) steps). Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion with no memo (n <= 25) on small inputs. Example: n=12 -> 3; n=13 -> 2; n=1 -> 1; n=7 -> 4; n=9999 -> 4.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Unbounded min-count DP (coin change, Q6, with the coins 1, 4, 9, ...).

**Say this first (1 line):** "dp[i] is the fewest squares that sum to i; I try every square j*j <= i as the last piece."

**Brute force:** Plain recursion `1 + min(f(m - j*j))` with no cache. Exponential; used as the oracle for n <= 25.

**Optimal:**
- State: `dp[i]` = fewest squares summing to exactly i.
- Base: `dp[0] = 0`.
- Transition: `dp[i] = min(dp[i - j*j] + 1)` over all j with j*j <= i. Every i >= 1 has an answer (1 + 1 + ... uses dp[i-1]).
- Bottom-up in increasing i, so smaller states are done.
- Recursion limit: the memoised version tries j = 1 first, so the first descent is n deep. At n = 10^4 it raises RecursionError under the default limit. Bottom-up is required.
- Facts checked for every n in 1..10^4: the answer is at most 4 (Lagrange), and equals 4 exactly when n = 4^a * (8b + 7) (Legendre). That gives an O(sqrt n) solution but is not needed in an interview.

**Complexity:** About n * sqrt(n) steps: the inner loop runs floor(sqrt(i)) times at i; the exact count at n = 10^4 is 661750 (about (2/3) n^1.5). Space O(n).

**Dry run:** n = 12.
| i | dp[i] | choices |
|---|---|---|
| 4 | 1 | dp[0]+1 |
| 8 | 2 | dp[4]+1 |
| 11 | 3 | dp[10]+1 = 3, dp[2]+1 = 3 |
| 12 | 3 | dp[11]+1 = 4, dp[8]+1 = 3, dp[3]+1 = 4 |
- Answer 3 = 4 + 4 + 4. The full table is in the output.

**Code:**
```python
import random
from functools import lru_cache

random.seed(16)
INF = float('inf')

def perfect_squares(n):
    """Optimal: dp[i] = fewest squares summing to i. Bottom-up, O(n sqrt n) time, O(n) space."""
    dp = [0] + [INF] * n              # dp[0] = 0: the empty sum
    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            if dp[i - j * j] + 1 < dp[i]:
                dp[i] = dp[i - j * j] + 1
            j += 1
    return dp[n]

def perfect_squares_memo(n):
    """Top-down: tries j = 1 first, so the first descent goes n deep."""
    @lru_cache(maxsize=None)
    def f(m):
        if m == 0:
            return 0
        return 1 + min(f(m - j * j) for j in range(1, int(m ** 0.5) + 1))
    return f(n)

def brute(n):
    """Oracle: plain recursion, no cache."""
    if n == 0:
        return 0
    return 1 + min(brute(n - j * j) for j in range(1, int(n ** 0.5) + 1))

for n, want in [(12, 3), (13, 2), (1, 1), (7, 4), (9999, 4)]:
    assert perfect_squares(n) == want, n
    if n < 900:
        assert perfect_squares_memo(n) == want
    if n <= 25:
        assert brute(n) == want
print('5 prompt examples ok')

# walk-through, n = 12
dp = [0] + [INF] * 12
print('i   dp[i]  best choice (j*j subtracted)')
print('0   0      base')
for i in range(1, 13):
    cands = [(dp[i - j * j] + 1, j * j) for j in range(1, int(i ** 0.5) + 1)]
    dp[i] = min(c[0] for c in cands)
    print('%-3d %-6d %s' % (i, dp[i], ', '.join('dp[%d]+1=%d' % (i - s, v) for v, s in cands)))
print('dp[12] = 3 : 4 + 4 + 4')

# step count of the double loop at n = 10^4 versus n^2/2 for a plain 1..n coin loop
steps = sum(int(i ** 0.5) for i in range(1, 10**4 + 1))
print('inner-loop steps at n=10^4:', steps, '(about n * sqrt(n) * 2/3 = 666667)')

# seeded cross-check against the plain recursion
for n in range(1, 26):
    assert perfect_squares(n) == brute(n) == perfect_squares_memo(n), n
for _ in range(300):
    n = random.randint(1, 25)
    assert perfect_squares(n) == brute(n)
print('all n in 1..25 and 300 random draws agree with the plain recursion')

# claims: answer never exceeds 4 (Lagrange); 4 exactly when n = 4^a (8b + 7) (Legendre)
def legendre4(n):
    while n % 4 == 0:
        n //= 4
    return n % 8 == 7
dp_all = [0] + [INF] * 10**4
for i in range(1, 10**4 + 1):
    j = 1
    while j * j <= i:
        dp_all[i] = min(dp_all[i], dp_all[i - j * j] + 1)
        j += 1
assert max(dp_all[1:]) == 4
assert all((dp_all[i] == 4) == legendre4(i) for i in range(1, 10**4 + 1))
print('for every n in 1..10^4 the answer is <= 4, and equals 4 exactly when n = 4^a * (8b + 7)')

# recursion limit
try:
    perfect_squares_memo(10**4)
    print('memo at n=10^4: no error (unexpected)')
except RecursionError:
    print('memo at n=10^4: RecursionError under the default limit')
print('bottom-up n=10^4 ->', perfect_squares(10**4))
assert perfect_squares(1) == 1 and perfect_squares(4) == 1 and perfect_squares(2) == 2
print('edge cases ok')
```

**Output (my run):**
```
5 prompt examples ok
i   dp[i]  best choice (j*j subtracted)
0   0      base
1   1      dp[0]+1=1
2   2      dp[1]+1=2
3   3      dp[2]+1=3
4   1      dp[3]+1=4, dp[0]+1=1
5   2      dp[4]+1=2, dp[1]+1=2
6   3      dp[5]+1=3, dp[2]+1=3
7   4      dp[6]+1=4, dp[3]+1=4
8   2      dp[7]+1=5, dp[4]+1=2
9   1      dp[8]+1=3, dp[5]+1=3, dp[0]+1=1
10  2      dp[9]+1=2, dp[6]+1=4, dp[1]+1=2
11  3      dp[10]+1=3, dp[7]+1=5, dp[2]+1=3
12  3      dp[11]+1=4, dp[8]+1=3, dp[3]+1=4
dp[12] = 3 : 4 + 4 + 4
inner-loop steps at n=10^4: 661750 (about n * sqrt(n) * 2/3 = 666667)
all n in 1..25 and 300 random draws agree with the plain recursion
for every n in 1..10^4 the answer is <= 4, and equals 4 exactly when n = 4^a * (8b + 7)
memo at n=10^4: RecursionError under the default limit
bottom-up n=10^4 -> 1
edge cases ok
```

**Edge cases:**
- n = 1: 1. n a perfect square: 1.
- n = 7: 4 (4+1+1+1). n = 9999: 4.
- Greedy "largest square first" fails (n = 12 gives 9+1+1+1 = 4, answer 3).

**Follow-ups:**
- Faster? Four-square theorem plus the three-square test: O(sqrt n).
- BFS version? Levels = number of squares; same answer, O(n sqrt n).
- Coin change? Q6.

**Common mistakes:**
- `dp[0] = INF` or forgetting `dp[0] = 0`.
- Looping j up to `n` instead of `sqrt(i)`.
- Using floats for sqrt with large n (`int(i ** 0.5)` is fine here; `isqrt` is safer).

### Q17 ⭐⭐ 🟡 0/1 knapsack (maximum value). `weights` and `values` are lists of equal length 1 <= len <= 100 (1 <= weight <= 100, 1 <= value <= 1000) and `cap` is the capacity 0 <= cap <= 1000. Each item is used at most once. Return the maximum total value with total weight <= cap (0 if nothing fits). Give the 2D table, then the 1D table that iterates the capacity DOWNWARD, and explain what the upward loop computes instead (it lets an item be reused, so it answers the unbounded problem of Q20). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsets (len <= 12) on small inputs. Example: weights=[1, 3, 4, 5], values=[1, 4, 5, 7], cap=7 -> 9; weights=[5], values=[10], cap=4 -> 0; weights=[2, 2, 3], values=[3, 3, 5], cap=4 -> 6; weights=[3, 4], values=[5, 6], cap=0 -> 0.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** 0/1 knapsack: each item once, maximise value under a weight cap.

**Say this first (1 line):** "dp[c] is the best value with capacity c; for each item I go through capacities from high to low so the item is used at most once."

**Brute force:** Try all 2^n subsets (the oracle, n <= 12); O(2^n * n).

**Optimal:**
- 2D state: `dp[i][c]` = best value from the first i items with capacity c. Base: row 0 all zeros.
- Transition: `dp[i][c] = max(dp[i-1][c], dp[i-1][c - w] + v)` (the second only if c >= w). Skip item i, or take it once on top of the row above.
- 1D: only row i-1 is needed, so keep one row and loop c from cap down to w. Downward, `dp[c - w]` is still the previous row.
- Upward loop: `dp[c - w]` may already contain this item, so it can be taken again. It computes the unbounded knapsack (Q20). Checked on 500 random cases: it equalled the unbounded answer every time and differed from the 0/1 answer in 438 of them. (`weights=[2], values=[5], cap=6`: 0/1 gives 5, upward gives 15.)
- Memoised top-down `go(i, rem)`: depth len(weights) <= 100, safe under the default recursion limit. At large depth it would raise RecursionError.

**Complexity:** Time O(n * cap), space O(n * cap) for 2D, O(cap) for 1D. (Pseudo-polynomial: polynomial in the value of cap, not its bit length.)

**Dry run:** weights `[1, 3, 4, 5]`, values `[1, 4, 5, 7]`, cap 7 (columns 0..7).
| row | values |
|---|---|
| none | 0 0 0 0 0 0 0 0 |
| w1 v1 | 0 1 1 1 1 1 1 1 |
| w3 v4 | 0 1 1 4 5 5 5 5 |
| w4 v5 | 0 1 1 4 5 6 6 9 |
| w5 v7 | 0 1 1 4 5 7 8 9 |
- Answer dp[7] = 9 (weights 3 + 4, values 4 + 5). The 1D row after each item is identical to the matching 2D row.

**Code:**
```python
import random
from functools import lru_cache

random.seed(17)

def knapsack_2d(weights, values, cap):
    """2D table: dp[i][c] = best value using the first i items with capacity c. O(n * cap) time and space."""
    n = len(weights)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]          # row 0: no items, value 0 for every capacity
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for c in range(cap + 1):
            dp[i][c] = dp[i - 1][c]                        # skip item i
            if c >= w:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)   # take item i once
    return dp

def knapsack_1d(weights, values, cap):
    """Optimal: one row, capacity looped DOWNWARD. O(n * cap) time, O(cap) space."""
    dp = [0] * (cap + 1)                                   # dp[c] = best value with weight <= c
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack_upward(weights, values, cap):
    """The classic bug: capacity looped UPWARD. dp[c - w] may already include this item, so it can be taken again."""
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(w, cap + 1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def unbounded(weights, values, cap):
    dp = [0] * (cap + 1)
    for c in range(1, cap + 1):
        for w, v in zip(weights, values):
            if w <= c:
                dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack_memo(weights, values, cap):
    """Top-down: state (i, remaining capacity); depth is len(weights) <= 100, safe under the default limit."""
    @lru_cache(maxsize=None)
    def go(i, rem):
        if i == len(weights):
            return 0
        best = go(i + 1, rem)
        if weights[i] <= rem:
            best = max(best, go(i + 1, rem - weights[i]) + values[i])
        return best
    return go(0, cap)

def brute(weights, values, cap):
    """Oracle: every subset."""
    n, best = len(weights), 0
    for m in range(1 << n):
        if sum(weights[i] for i in range(n) if m >> i & 1) <= cap:
            best = max(best, sum(values[i] for i in range(n) if m >> i & 1))
    return best

for (w, v, c), want in [(([1, 3, 4, 5], [1, 4, 5, 7], 7), 9), (([5], [10], 4), 0), (([2, 2, 3], [3, 3, 5], 4), 6), (([3, 4], [5, 6], 0), 0)]:
    assert knapsack_2d(w, v, c)[-1][c] == knapsack_1d(w, v, c) == knapsack_memo(w, v, c) == brute(w, v, c) == want
print('4 prompt examples ok')

# walk-through on weights=[1,3,4,5], values=[1,4,5,7], cap=7
w, v, cap = [1, 3, 4, 5], [1, 4, 5, 7], 7
print('2D table, columns c = 0..7')
print('no items ', knapsack_2d([], [], cap)[0])
dp2 = knapsack_2d(w, v, cap)
for i in range(1, 5):
    print('item %d (w=%d,v=%d)' % (i, w[i - 1], v[i - 1]), dp2[i])
print('1D table, same final row; each line is the single row after one item (downward loop)')
dp = [0] * (cap + 1)
for wi, vi in zip(w, v):
    for c in range(cap, wi - 1, -1):
        dp[c] = max(dp[c], dp[c - wi] + vi)
    print('after w=%d' % wi, dp)
assert dp == dp2[-1]
print('answer', dp[cap], '= items weight 3 + 4 (values 4 + 5)')

# what the upward loop computes: a different problem
print('upward loop on the same input:', knapsack_upward(w, v, cap), '; unbounded answer:', unbounded(w, v, cap), '; true 0/1 answer:', knapsack_1d(w, v, cap))
print('example where it breaks: one item weight 2, value 5, cap 6 -> 0/1', knapsack_1d([2], [5], 6), 'upward', knapsack_upward([2], [5], 6))

# seeded cross-check against subset enumeration (len <= 12)
diff = 0
for _ in range(500):
    n = random.randint(1, 12)
    w = [random.randint(1, 9) for _ in range(n)]
    v = [random.randint(1, 30) for _ in range(n)]
    cap = random.randint(0, 40)
    b = brute(w, v, cap)
    assert knapsack_1d(w, v, cap) == knapsack_2d(w, v, cap)[-1][cap] == knapsack_memo(w, v, cap) == b, (w, v, cap)
    assert knapsack_upward(w, v, cap) == unbounded(w, v, cap)
    diff += knapsack_upward(w, v, cap) != b
print('500 random cases agree (1D = 2D = memo = enumeration); upward loop equals the unbounded answer every time and differs from 0/1 in', diff)

# edge cases and max size
assert knapsack_1d([100], [1000], 99) == 0 and knapsack_1d([100], [1000], 100) == 1000
big_w = [random.randint(1, 100) for _ in range(100)]
big_v = [random.randint(1, 1000) for _ in range(100)]
assert knapsack_1d(big_w, big_v, 1000) == knapsack_memo(big_w, big_v, 1000) == knapsack_2d(big_w, big_v, 1000)[-1][1000]
print('edge cases ok; max-size random input ->', knapsack_1d(big_w, big_v, 1000))
```

**Output (my run):**
```
4 prompt examples ok
2D table, columns c = 0..7
no items  [0, 0, 0, 0, 0, 0, 0, 0]
item 1 (w=1,v=1) [0, 1, 1, 1, 1, 1, 1, 1]
item 2 (w=3,v=4) [0, 1, 1, 4, 5, 5, 5, 5]
item 3 (w=4,v=5) [0, 1, 1, 4, 5, 6, 6, 9]
item 4 (w=5,v=7) [0, 1, 1, 4, 5, 7, 8, 9]
1D table, same final row; each line is the single row after one item (downward loop)
after w=1 [0, 1, 1, 1, 1, 1, 1, 1]
after w=3 [0, 1, 1, 4, 5, 5, 5, 5]
after w=4 [0, 1, 1, 4, 5, 6, 6, 9]
after w=5 [0, 1, 1, 4, 5, 7, 8, 9]
answer 9 = items weight 3 + 4 (values 4 + 5)
upward loop on the same input: 9 ; unbounded answer: 9 ; true 0/1 answer: 9
example where it breaks: one item weight 2, value 5, cap 6 -> 0/1 5 upward 15
500 random cases agree (1D = 2D = memo = enumeration); upward loop equals the unbounded answer every time and differs from 0/1 in 438
edge cases ok; max-size random input -> 23637
```

**Edge cases:**
- cap = 0 or every item too heavy: 0.
- Item exactly equal to cap: allowed (`c >= w`).
- Max size 100 items, cap 1000: 100,000 updates.

**Follow-ups:**
- Which items? Q37 (reconstruction with a tie rule).
- Exactly cap? Initialise dp[0] = 0 and others -inf.
- Unbounded? Q20: flip the loop direction.

**Common mistakes:**
- Upward capacity loop.
- Loop bound `range(cap, w, -1)` (misses `c == w`).
- Defining dp as "exactly c" but initialising to zeros.

### Q18 ⭐⭐ 🟡 Subset sum (decision). `nums` has 1 <= len <= 200 positive integers (each <= 500) and `target` is 0 <= target <= 10^4. Return True if some subset (possibly empty, so target 0 is True) sums to `target`. Give the boolean 1D table with the downward capacity loop and the big-int bitset version; state the time O(n * target) for the table and O(n * target / 64) word operations for the bitset in theory (not a measured claim). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsets (len <= 12), and your two methods against each other on small inputs. Example: nums=[3, 34, 4, 12, 5, 2], target=9 -> True; nums=[3, 34, 4, 12, 5, 2], target=30 -> False; nums=[7], target=0 -> True; nums=[5, 5], target=5 -> True.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Subset sum, decision form of 0/1 knapsack (boolean table or bitset).

**Say this first (1 line):** "dp[t] says whether sum t is reachable; for each number I update t from high to low. In Python the same thing is `bits |= bits << x`."

**Brute force:** Enumerate all 2^n subsets (n <= 12, the oracle).

**Optimal:**
- State: `dp[t]` = True if some subset of the items so far sums to exactly t. Base: `dp[0] = True`, so target 0 is True via the empty subset.
- Transition: for x in nums, for t from target down to x: `dp[t] |= dp[t - x]`. Downward so x is used once.
- Bitset: `bits |= (bits << x) & mask`, with `mask = (1 << (target + 1)) - 1` so the integer never grows beyond target + 1 bits. The answer is bit `target`.
- Memoised top-down `go(i, rem)`: depth <= len(nums) + 1, safe under the default limit.
- Table time O(n * target), space O(target). Bitset: n shift-or operations on an integer of target + 1 bits, so O(n * target / 64) word operations in theory (a statement about word size, not a measured claim).

**Complexity:** Table: O(n * target) time, O(target) space. At the maximum (n = 200, target = 10^4) that is at most 2,000,000 cell updates; the bitset does 200 shift-or operations on a 10001-bit integer (about 157 64-bit words).

**Dry run:** `[3, 34, 4, 12, 5, 2]`, target 9 (T = reachable, t = 0..9).
| after | row |
|---|---|
| start | `T.........` |
| 3 | `T..T......` |
| 34 | `T..T......` (too big) |
| 4 | `T..TT..T..` |
| 12 | `T..TT..T..` (too big) |
| 5 | `T..TTT.TTT` |
| 2 | `T.TTTTTTTT` |
- dp[9] True (4 + 5). The bitset rows in the output show the same bits.

**Code:**
```python
import random
from functools import lru_cache

random.seed(18)

def subset_sum(nums, target):
    """Boolean 1D table, capacity DOWNWARD. O(n * target) time, O(target) space."""
    dp = [True] + [False] * target                  # dp[t]: some subset of the items so far sums to exactly t
    for x in nums:
        for t in range(target, x - 1, -1):
            if dp[t - x]:
                dp[t] = True
    return dp[target]

def subset_sum_bits(nums, target):
    """Big-int bitset: bit t set means sum t reachable. Mask to target+1 bits so the int never grows past the target."""
    mask = (1 << (target + 1)) - 1
    bits = 1
    for x in nums:
        bits |= (bits << x) & mask
    return bool(bits >> target & 1)

def subset_sum_memo(nums, target):
    """Top-down over (i, remaining). Depth <= len(nums) + 1, safe under the default limit."""
    @lru_cache(maxsize=None)
    def go(i, rem):
        if rem == 0:
            return True
        if i == len(nums) or rem < 0:
            return False
        return go(i + 1, rem - nums[i]) or go(i + 1, rem)
    return go(0, target)

def brute(nums, target):
    n = len(nums)
    return any(sum(nums[i] for i in range(n) if m >> i & 1) == target for m in range(1 << n))

for (nums, t), want in [(([3, 34, 4, 12, 5, 2], 9), True), (([3, 34, 4, 12, 5, 2], 30), False), (([7], 0), True), (([5, 5], 5), True)]:
    assert subset_sum(nums, t) is want and subset_sum_bits(nums, t) is want and subset_sum_memo(nums, t) is want and brute(nums, t) is want
print('4 prompt examples ok')

# walk-through: nums=[3,34,4,12,5,2], target=9; items bigger than the target do nothing (34, 12)
nums, target = [3, 34, 4, 12, 5, 2], 9
dp = [True] + [False] * target
print('columns t = 0..9')
print('start   ', ''.join('T' if x else '.' for x in dp))
for x in nums:
    for t in range(target, x - 1, -1):
        if dp[t - x]:
            dp[t] = True
    print('item %-3d' % x, ''.join('T' if y else '.' for y in dp))
print('dp[9] =', dp[9], '(4 + 5, or 4 + 3 + 2)')

bits = 1
mask = (1 << 10) - 1
print('bitset after each item (bit 0 on the right, masked to 10 bits):')
for x in nums:
    bits |= (bits << x) & mask
    print('  item %-3d %s' % (x, format(bits, '010b')))

# seeded cross-check: table vs bitset vs memo vs enumeration (len <= 12)
t_true = 0
for _ in range(600):
    nums = [random.randint(1, 15) for _ in range(random.randint(1, 12))]
    target = random.randint(0, sum(nums) + 3)
    b = brute(nums, target)
    assert subset_sum(nums, target) == subset_sum_bits(nums, target) == subset_sum_memo(nums, target) == b, (nums, target)
    t_true += b
print('600 random cases agree (table = bitset = memo = enumeration); True in', t_true)

# edge cases and max size, table against bitset
assert subset_sum([7], 0) and not subset_sum([7], 3) and subset_sum([1] * 200, 200) and not subset_sum([2] * 200, 399)
for _ in range(5):
    nums = [random.randint(1, 500) for _ in range(200)]
    target = random.randint(0, 10**4)
    assert subset_sum(nums, target) == subset_sum_bits(nums, target) == subset_sum_memo(nums, target)
print('edge cases ok; five max-size random inputs: table = bitset = memo')
print('table cell updates at max size (n=200, target=10^4): at most', 200 * 10**4, '; bitset: 200 shift-or operations on a', 10**4 + 1, 'bit integer (about', (10**4 + 1 + 63) // 64, '64-bit words each)')
```

**Output (my run):**
```
4 prompt examples ok
columns t = 0..9
start    T.........
item 3   T..T......
item 34  T..T......
item 4   T..TT..T..
item 12  T..TT..T..
item 5   T..TTT.TTT
item 2   T.TTTTTTTT
dp[9] = True (4 + 5, or 4 + 3 + 2)
bitset after each item (bit 0 on the right, masked to 10 bits):
  item 3   0000001001
  item 34  0000001001
  item 4   0010011001
  item 12  0010011001
  item 5   1110111001
  item 2   1111111101
600 random cases agree (table = bitset = memo = enumeration); True in 391
edge cases ok; five max-size random inputs: table = bitset = memo
table cell updates at max size (n=200, target=10^4): at most 2000000 ; bitset: 200 shift-or operations on a 10001 bit integer (about 157 64-bit words each)
```

**Edge cases:**
- target = 0: True. target above the sum: False.
- Items larger than target are skipped.
- Duplicates are fine (`[5, 5]`, target 5: True).

**Follow-ups:**
- Count the subsets? Replace `|=` with `+=` (Q19).
- Which subset? Keep a 2D table or parent pointers.
- Large values, few items? Meet in the middle, O(2^(n/2)).

**Common mistakes:**
- Upward loop (reuses an item).
- Not masking the bitset (the int grows to the total sum; harmless but wasteful).
- Treating target 0 as False.

### Q19 ⭐⭐ 🟡 Target sum (count sign assignments). `nums` has 1 <= len <= 20 non-negative integers with sum <= 1000 (zeros allowed). Put a + or a - in front of every number and count the assignments whose total equals `target` (-1000 <= target <= 1000). Return the count. Reduce it to counting subsets with sum (S + target) / 2, where S is the total; say when the answer is 0 at once (|target| > S or S + target odd), and explain what each zero in the list does to the count (it doubles it). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all 2^n sign assignments (len <= 12) on small inputs. Example: nums=[1, 1, 1, 1, 1], target=3 -> 5; nums=[1], target=1 -> 1; nums=[0, 0, 1], target=1 -> 4; nums=[1, 2], target=4 -> 0.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Count subsets with a given sum (counting 0/1 knapsack), after an algebra reduction.

**Say this first (1 line):** "Plus-group P and minus-group N: P - N = target and P + N = S, so P = (S + target) / 2. I count subsets with sum P."

**Brute force:** All 2^n sign assignments (n <= 12 as the oracle). A direct DP over signed running totals (a dict) also works and is the version I give first if I do not see the trick.

**Optimal:**
- Reduction: need = (S + target) / 2. The answer is 0 at once if |target| > S or S + target is odd.
- State: `dp[w]` = number of subsets (by index) with sum w. Base: `dp[0] = 1`.
- Transition: for x in nums, for w from need down to x: `dp[w] += dp[w - x]`. Downward, each item once.
- Zeros: for x = 0 the loop runs w = need..0 and does `dp[w] += dp[w]`, doubling every cell. So each zero doubles the count (a zero can take + or - without changing the total). Verified exhaustively for all lists of length <= 6 with values 0..3: `count(with z zeros) = 2^z * count(without)` and the DP equals the 2^n enumeration.
- Memoised top-down over (i, running total): depth len(nums) <= 20.

**Complexity:** O(n * need) time, O(need) space, with need <= (S + |target|)/2 <= 1000.

**Dry run:** `[1,1,1,1,1]`, target 3: S = 5, need = 4. Row after each item (w = 0..4):
`[1,0,0,0,0]` -> `[1,1,0,0,0]` -> `[1,2,1,0,0]` -> `[1,3,3,1,0]` -> `[1,4,6,4,1]` -> `[1,5,10,10,5]`.
- dp[4] = 5 = C(5, 4): choose which four numbers get a plus.
- With `[0, 0, 1]`, target 1 (need 1): `[1,0]` -> `[2,0]` -> `[4,0]` -> `[4,4]`: answer 4.

**Code:**
```python
import random
import itertools
from functools import lru_cache

random.seed(19)

def target_sum(nums, target):
    """Optimal: signs = split into P (plus) and N (minus). P - N = target, P + N = S, so P = (S + target) / 2.
    Count subsets with sum P. O(n * P) time, O(P) space."""
    s = sum(nums)
    if abs(target) > s or (s + target) % 2:
        return 0
    need = (s + target) // 2
    dp = [1] + [0] * need                           # dp[w]: number of subsets (by index) with sum w
    for x in nums:
        for w in range(need, x - 1, -1):            # downward; for x = 0 this runs w = need..0 and doubles every cell
            dp[w] += dp[w - x]
    return dp[need]

def target_sum_memo(nums, target):
    """Top-down over (i, running signed total). Depth = len(nums) <= 20."""
    @lru_cache(maxsize=None)
    def go(i, total):
        if i == len(nums):
            return 1 if total == target else 0
        return go(i + 1, total + nums[i]) + go(i + 1, total - nums[i])
    return go(0, 0)

def target_sum_dict(nums, target):
    """Direct DP over signed totals (no reduction), the version you give first if you do not see the trick."""
    ways = {0: 1}
    for x in nums:
        nxt = {}
        for t, c in ways.items():
            nxt[t + x] = nxt.get(t + x, 0) + c
            nxt[t - x] = nxt.get(t - x, 0) + c
        ways = nxt
    return ways.get(target, 0)

def brute(nums, target):
    """Oracle: all 2^n sign assignments."""
    return sum(1 for signs in itertools.product((1, -1), repeat=len(nums)) if sum(a * b for a, b in zip(signs, nums)) == target)

for (nums, t), want in [(([1, 1, 1, 1, 1], 3), 5), (([1], 1), 1), (([0, 0, 1], 1), 4), (([1, 2], 4), 0)]:
    assert target_sum(nums, t) == target_sum_memo(nums, t) == target_sum_dict(nums, t) == brute(nums, t) == want
print('4 prompt examples ok')

# walk-through on [1,1,1,1,1], target 3: S = 5, P = (5 + 3) / 2 = 4
nums, target = [1, 1, 1, 1, 1], 3
s = sum(nums); need = (s + target) // 2
dp = [1] + [0] * need
print('S =', s, ' need P =', need, ' columns w = 0..%d' % need)
print('start   ', dp)
for x in nums:
    for w in range(need, x - 1, -1):
        dp[w] += dp[w - x]
    print('item %d  ' % x, dp)
print('dp[4] =', dp[need], '= C(5,4) ways to pick which four numbers get a plus')

# zero check on [0,0,1], target 1: S=1, need=1
dp = [1, 0]
print('[0,0,1] target 1: need = 1')
print('start   ', dp)
for x in [0, 0, 1]:
    for w in range(1, x - 1, -1):
        dp[w] += dp[w - x]
    print('item %d  ' % x, dp)

# immediate zeros
print('|target| > S  ->', target_sum([1, 2], 4), ';  S + target odd ->', target_sum([1, 2], 2), ' (S=3, 5 is odd)')

# claim: every zero doubles the count (exhaustive)
count = 0
for n in range(1, 7):
    for nums in itertools.product(range(0, 4), repeat=n):
        nums = list(nums)
        for target in range(-sum(nums) - 1, sum(nums) + 2):
            got = target_sum(nums, target)
            assert got == brute(nums, target), (nums, target)
            nz = [x for x in nums if x]
            z = n - len(nz)
            if nz:
                assert got == 2 ** z * target_sum(nz, target)
            count += 1
print('exhaustive (all lists len<=6, values 0..3, every target in range):', count, 'checks; each zero doubles the count, and the DP matches the 2^n enumeration')

# seeded random cross-check, len <= 12
for _ in range(500):
    nums = [random.randint(0, 6) for _ in range(random.randint(1, 12))]
    target = random.randint(-sum(nums) - 2, sum(nums) + 2)
    b = brute(nums, target)
    assert target_sum(nums, target) == target_sum_memo(nums, target) == target_sum_dict(nums, target) == b, (nums, target)
print('500 random cases agree (reduction = memo = signed-total dict = enumeration)')

# edge cases / max size
assert target_sum([0], 0) == 2 and target_sum([0] * 20, 0) == 2**20 and target_sum([0] * 20, 1) == 0
assert target_sum([50] * 20, 0) == target_sum_dict([50] * 20, 0) == 184756
assert target_sum([1000], -1000) == 1 and target_sum([1000], 0) == 0
print('edge cases ok: twenty zeros -> 2^20 =', target_sum([0] * 20, 0), '; twenty 50s, target 0 ->', target_sum([50] * 20, 0))
```

**Output (my run):**
```
4 prompt examples ok
S = 5  need P = 4  columns w = 0..4
start    [1, 0, 0, 0, 0]
item 1   [1, 1, 0, 0, 0]
item 1   [1, 2, 1, 0, 0]
item 1   [1, 3, 3, 1, 0]
item 1   [1, 4, 6, 4, 1]
item 1   [1, 5, 10, 10, 5]
dp[4] = 5 = C(5,4) ways to pick which four numbers get a plus
[0,0,1] target 1: need = 1
start    [1, 0]
item 0   [2, 0]
item 0   [4, 0]
item 1   [4, 4]
|target| > S  -> 0 ;  S + target odd -> 0  (S=3, 5 is odd)
exhaustive (all lists len<=6, values 0..3, every target in range): 109224 checks; each zero doubles the count, and the DP matches the 2^n enumeration
500 random cases agree (reduction = memo = signed-total dict = enumeration)
edge cases ok: twenty zeros -> 2^20 = 1048576 ; twenty 50s, target 0 -> 184756
```

**Edge cases:**
- `[0]`, target 0: 2. Twenty zeros, target 0: 2^20.
- |target| > S: 0. S + target odd: 0.
- Negative target: symmetric to its absolute value.

**Follow-ups:**
- Why not a dict DP? It works (target range is small); the reduction is faster and 1D.
- Large values? Same table, still bounded by the sum limit.
- Min number of sign flips? Different DP; keep counts of items too.

**Common mistakes:**
- Skipping the parity check (non-integer need).
- Looping `w` down to `x` with `range(need, x, -1)` and missing `w == x`.
- Treating zeros as ignorable (the answer is off by a factor 2 per zero).

### Q20 ⭐⭐ 🟡 Unbounded knapsack (maximum value). `weights` and `values` have equal length 1 <= len <= 50 (1 <= weight <= 100, 1 <= value <= 1000) and each item can be used any number of times; `cap` is 0 <= cap <= 10^4. Return the maximum total value with total weight <= cap (0 if nothing fits). Give the 1D table (capacity upward) and say how it differs from the 0/1 version (Q17) by one loop direction only. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over the remaining capacity (cap <= 10) on small inputs. Example: weights=[2, 3, 4], values=[3, 5, 7], cap=8 -> 14; weights=[5], values=[10], cap=4 -> 0; weights=[1, 5], values=[1, 8], cap=11 -> 17; weights=[3], values=[7], cap=9 -> 21.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** Unbounded knapsack (items reusable), 1D table, capacity upward.

**Say this first (1 line):** "dp[c] is the best value with weight at most c; for each c I try every item as the last one added. It is the 0/1 knapsack with the capacity loop flipped to upward."

**Brute force:** Plain recursion over the remaining capacity: `f(c) = max(0, f(c - w) + v)` over items that fit. Exponential; the oracle for cap <= 10.

**Optimal:**
- State: `dp[c]` = best value with total weight <= c. Base: `dp[0] = 0`, and all zeros means "capacity left over is fine".
- Transition: `dp[c] = max(dp[c - w] + v)` over items with w <= c (or leave it at 0).
- Loop order: capacity outer, items inner; or items outer, capacity upward. Both give the same answer (checked in 500 cases) because for max the order of use does not matter.
- Versus 0/1 (Q17): the only difference is the capacity direction. Upward lets `dp[c - w]` already contain the item, which is exactly "reuse". Example `weights=[3], values=[7], cap=9`: 0/1 gives 7, unbounded gives 21.
- Recursion limit: the memoised top-down `f(c)` descends up to cap deep (a weight-1 item gives depth 10^4). It raises RecursionError under the default limit of 1000. Bottom-up is required.

**Complexity:** O(n * cap) time, O(cap) space. Max: 50 * 10^4 = 500,000 updates.

**Dry run:** weights `[2,3,4]`, values `[3,5,7]`, cap 8.
| c | dp[c] | best candidate |
|---|---|---|
| 1 | 0 | nothing fits |
| 2 | 3 | w2: dp[0]+3 |
| 3 | 5 | w3: dp[0]+5 |
| 4 | 7 | w4: dp[0]+7 |
| 5 | 8 | w2: dp[3]+3 = 8 |
| 6 | 10 | dp[4]+3 = 10 |
| 7 | 12 | w3: dp[4]+5 = 12 |
| 8 | 14 | w4: dp[4]+7 = 14 |
- Answer 14 (two weight-4 items).

**Code:**
```python
import random
from functools import lru_cache

random.seed(20)

def unbounded_knapsack(weights, values, cap):
    """Optimal: dp[c] = best value with total weight <= c, items reusable. O(n * cap) time, O(cap) space."""
    dp = [0] * (cap + 1)
    for c in range(1, cap + 1):
        for w, v in zip(weights, values):
            if w <= c and dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return dp[cap]

def unbounded_item_outer(weights, values, cap):
    """Same answer, items outer and capacity UPWARD: the 0/1 code with one loop direction flipped."""
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(w, cap + 1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack01(weights, values, cap):
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def unbounded_memo(weights, values, cap):
    """Top-down over the remaining capacity. Depth can reach cap (weight-1 items), so it breaks past ~1000."""
    @lru_cache(maxsize=None)
    def f(c):
        return max([0] + [f(c - w) + v for w, v in zip(weights, values) if w <= c])
    return f(cap)

def brute(weights, values, cap):
    """Oracle: plain recursion over the remaining capacity, no cache."""
    def f(c):
        return max([0] + [f(c - w) + v for w, v in zip(weights, values) if w <= c])
    return f(cap)

for (w, v, c), want in [(([2, 3, 4], [3, 5, 7], 8), 14), (([5], [10], 4), 0), (([1, 5], [1, 8], 11), 17), (([3], [7], 9), 21)]:
    assert unbounded_knapsack(w, v, c) == unbounded_item_outer(w, v, c) == brute(w, v, c) == unbounded_memo(tuple(w), tuple(v), c) == want
print('4 prompt examples ok')

# walk-through on weights=[2,3,4], values=[3,5,7], cap=8
w, v, cap = [2, 3, 4], [3, 5, 7], 8
dp = [0] * (cap + 1)
print('c   dp[c]  candidates dp[c-w]+v for each item that fits')
print('0   0      base: nothing fits in capacity 0')
for c in range(1, cap + 1):
    cands = ['w=%d:dp[%d]+%d=%d' % (wi, c - wi, vi, dp[c - wi] + vi) for wi, vi in zip(w, v) if wi <= c]
    dp[c] = max([0] + [dp[c - wi] + vi for wi, vi in zip(w, v) if wi <= c])
    print('%-3d %-6d %s' % (c, dp[c], ', '.join(cands) if cands else 'nothing fits'))
print('dp[8] =', dp[8], '= 7 + 7 (two weight-4 items)')

# 0/1 versus unbounded: one loop direction
print('weights=[3], values=[7], cap=9 -> 0/1', knapsack01([3], [7], 9), ' unbounded', unbounded_knapsack([3], [7], 9))

# seeded cross-check against the plain recursion (cap <= 10)
for _ in range(500):
    n = random.randint(1, 4)
    w = [random.randint(1, 7) for _ in range(n)]
    v = [random.randint(1, 20) for _ in range(n)]
    cap = random.randint(0, 10)
    b = brute(w, v, cap)
    assert unbounded_knapsack(w, v, cap) == unbounded_item_outer(w, v, cap) == unbounded_memo(tuple(w), tuple(v), cap) == b, (w, v, cap)
print('500 random cases agree (capacity-outer = item-outer = memo = plain recursion)')

# recursion limit
try:
    unbounded_memo((1,), (1,), 10**4)
    print('memo at cap=10^4 with a weight-1 item: no error (unexpected)')
except RecursionError:
    print('memo at cap=10^4 with a weight-1 item: RecursionError under the default limit')
print('bottom-up cap=10^4, weights=[1] ->', unbounded_knapsack([1], [1], 10**4))

# edge cases and max size
assert unbounded_knapsack([5], [10], 0) == 0 and unbounded_knapsack([100], [1000], 99) == 0
big_w = [random.randint(1, 100) for _ in range(50)]
big_v = [random.randint(1, 1000) for _ in range(50)]
assert unbounded_knapsack(big_w, big_v, 10**4) == unbounded_item_outer(big_w, big_v, 10**4)
print('edge cases ok; max-size random input ->', unbounded_knapsack(big_w, big_v, 10**4))
```

**Output (my run):**
```
4 prompt examples ok
c   dp[c]  candidates dp[c-w]+v for each item that fits
0   0      base: nothing fits in capacity 0
1   0      nothing fits
2   3      w=2:dp[0]+3=3
3   5      w=2:dp[1]+3=3, w=3:dp[0]+5=5
4   7      w=2:dp[2]+3=6, w=3:dp[1]+5=5, w=4:dp[0]+7=7
5   8      w=2:dp[3]+3=8, w=3:dp[2]+5=8, w=4:dp[1]+7=7
6   10     w=2:dp[4]+3=10, w=3:dp[3]+5=10, w=4:dp[2]+7=10
7   12     w=2:dp[5]+3=11, w=3:dp[4]+5=12, w=4:dp[3]+7=12
8   14     w=2:dp[6]+3=13, w=3:dp[5]+5=13, w=4:dp[4]+7=14
dp[8] = 14 = 7 + 7 (two weight-4 items)
weights=[3], values=[7], cap=9 -> 0/1 7  unbounded 21
500 random cases agree (capacity-outer = item-outer = memo = plain recursion)
memo at cap=10^4 with a weight-1 item: RecursionError under the default limit
bottom-up cap=10^4, weights=[1] -> 10000
edge cases ok; max-size random input -> 8640000
```

**Edge cases:**
- cap = 0 or all items heavier than cap: 0.
- One item of weight 3, cap 9: three copies, 21.
- cap = 10^4: bottom-up is instant; memo raises RecursionError.

**Follow-ups:**
- Exactly cap? Initialise others to -inf.
- Count ways? Coin change II (Q10); combinations versus sequences is a loop-order choice.
- Bounded copies? Binary splitting of the counts into 0/1 items.

**Common mistakes:**
- Using the downward loop (gives the 0/1 answer).
- Raising the recursion limit instead of going bottom-up.
- Initialising `dp` with -inf and then reading dp[cap] when it should be "at most".

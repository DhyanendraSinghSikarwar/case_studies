### Q21 ⭐⭐ 🟢 Running sum and pivot index. `nums` has 1 <= len <= 10^4 integers (|value| <= 1000). Return `[pivot, running]`: `running` is the list of running sums (`running[i] = nums[0] + ... + nums[i]`, what `itertools.accumulate` gives), and `pivot` is the smallest index i such that the sum of the items strictly to its left equals the sum of the items strictly to its right (an empty side sums to 0), or -1 if there is no such index. Do it in O(n) time with the total and the running sum: the left sum is `running[i] - nums[i]` and the right sum is `total - running[i]`. Explain why negative values do not break this (unlike a sliding window) and why you must return the leftmost index when several qualify. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the O(n^2) rescanning of each side on small inputs. Example: nums=[1, 7, 3, 6, 5, 6] -> [3, [1, 8, 11, 17, 22, 28]]; nums=[1, 2, 3] -> [-1, [1, 3, 6]]; nums=[2, 1, -1] -> [0, [2, 3, 2]]; nums=[0] -> [0, [0]].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)

**Pattern:** Prefix sums. One running total turns "sum of everything on one side" into an O(1) subtraction.

**Say this first (1 line):** "Left sum is `running[i] - nums[i]`, right sum is `total - running[i]`; scan once and return the first index where they are equal, else -1."

**Brute force:** For each index i, add up `nums[:i]` and `nums[i+1:]` and compare. O(n) per index, O(n^2) overall. With n = 10^4 that is about 10^8 additions in the worst case. It is the oracle in the cross-check.

**Optimal:**
- Build `running` with `itertools.accumulate`. `total = running[-1]`.
- For each i: `left = running[i] - nums[i]` (everything before i), `right = total - running[i]` (everything after i). Compare.
- Scan left to right and return at the first match. That gives the leftmost pivot for free.
- Invariant: `left + nums[i] + right == total` for every i. So the test `left == right` is the same as `2 * left + nums[i] == total`.
- Negatives are fine because we only test equality at each index. We never move a window and never assume the sum only grows. A sliding window needs the sum to change monotonically when you shrink or grow it. With negatives that breaks. A prefix sum does not care about signs.
- Leftmost matters because several indexes can qualify. In `[0, 0]` index 0 (left 0, right 0) and index 1 (left 0, right 0) both work. The answer must be 0. The exhaustive check below finds 2795 such lists out of 19530.

**Complexity:** Time O(n): one accumulate pass plus one scan. Space O(n) for `running`, which the question asks us to return anyway. If you only needed the pivot, keep a single integer `left` and use O(1) space.

**Dry run:** `[1, 7, 3, 6, 5, 6]`, total 28. At i=3, x=6: `running[3] = 17`, left = 17 - 6 = 11, right = 28 - 17 = 11. Equal, so the pivot is 3. Indexes 0 to 2 fail (left 0, 1, 8 against right 27, 20, 17). The program prints each step.

**Code:**
```python
import itertools
import random

random.seed(2101)

def pivot_index(nums):
    """O(n): returns [leftmost pivot or -1, running sums]."""
    running = list(itertools.accumulate(nums))
    total = running[-1]
    for i, x in enumerate(nums):
        left = running[i] - x            # sum of nums[:i]
        right = total - running[i]       # sum of nums[i+1:]
        if left == right:
            return [i, running]          # first hit = leftmost
    return [-1, running]

def brute(nums):
    run, s = [], 0
    for v in nums:
        s += v
        run.append(s)
    for i in range(len(nums)):
        if sum(nums[:i]) == sum(nums[i + 1:]):   # rescan both sides: O(n^2)
            return [i, run]
    return [-1, run]

examples = [([1, 7, 3, 6, 5, 6], [3, [1, 8, 11, 17, 22, 28]]),
            ([1, 2, 3], [-1, [1, 3, 6]]),
            ([2, 1, -1], [0, [2, 3, 2]]),
            ([0], [0, [0]])]
for nums, want in examples:
    assert pivot_index(nums) == want == brute(nums)
    print(nums, '->', pivot_index(nums))

# dry run on the first example
nums = [1, 7, 3, 6, 5, 6]
run = list(itertools.accumulate(nums)); total = run[-1]
for i, x in enumerate(nums):
    print(f'  i={i} x={x} left={run[i] - x} right={total - run[i]}')

# seeded random cross-check
for _ in range(3000):
    nums = [random.randint(-4, 4) for _ in range(random.randint(1, 9))]
    assert pivot_index(nums) == brute(nums)
print('random cross-check ok: 3000 cases')

# exhaustive: every list of length 1..6 over -2..2
total_lists = several = 0
for n in range(1, 7):
    for nums in itertools.product(range(-2, 3), repeat=n):
        nums = list(nums)
        assert pivot_index(nums) == brute(nums)
        total_lists += 1
        all_piv = [i for i in range(n) if sum(nums[:i]) == sum(nums[i + 1:])]
        if len(all_piv) > 1:
            several += 1
            assert pivot_index(nums)[0] == all_piv[0]     # leftmost wins
print('exhaustive ok:', total_lists, 'lists; with 2+ valid pivots:', several)
print('example with 2 pivots:', [0, 0], '->', pivot_index([0, 0])[0], '(index 1 also qualifies)')

# edge asserts
assert pivot_index([5])[0] == 0                      # both sides empty
assert pivot_index([-1, 3, -1])[0] == 1             # negatives are fine: -1 on both sides
assert pivot_index([1, -1])[0] == -1
big = [1000] * 10**4
assert pivot_index(big)[0] == -1 and pivot_index(big)[1][-1] == 10**7
print('edge asserts ok')
```

**Output (my run):**
```
[1, 7, 3, 6, 5, 6] -> [3, [1, 8, 11, 17, 22, 28]]
[1, 2, 3] -> [-1, [1, 3, 6]]
[2, 1, -1] -> [0, [2, 3, 2]]
[0] -> [0, [0]]
  i=0 x=1 left=0 right=27
  i=1 x=7 left=1 right=20
  i=2 x=3 left=8 right=17
  i=3 x=6 left=11 right=11
  i=4 x=5 left=17 right=6
  i=5 x=6 left=22 right=0
random cross-check ok: 3000 cases
exhaustive ok: 19530 lists; with 2+ valid pivots: 2795
example with 2 pivots: [0, 0] -> 0 (index 1 also qualifies)
edge asserts ok
```

**Edge cases:**
- One element: both sides are empty, so the pivot is 0 (`[0]` and `[5]`).
- Pivot at the first index: `[2, 1, -1]` gives 0 because left is 0 and right is 1 - 1 = 0.
- Pivot at the last index: needs the whole left side to sum to 0.
- No pivot: `[1, 2, 3]` and `[1, -1]` give -1.
- All 1000s with n = 10^4: total is 10^7, no pivot. Python ints cannot overflow, but in a 32-bit language the sums still fit (at most 10^7).

**Follow-ups:**
- *Return all pivots?* Collect instead of returning at the first match. Same O(n).
- *Many range-sum queries?* The same `running` array answers any `sum(l..r)` as `running[r] - running[l-1]`.
- *Why not two pointers here?* There is no monotone rule that says which pointer to move once negatives are allowed.

**Common mistakes:**
- Including `nums[i]` in the left sum (off by one). `running[i]` already contains it, so subtract it.
- Forgetting that an empty side is 0 (first and last index).
- Returning the last match, or the one nearest the middle, instead of the leftmost.
- Using a window or early `break` when the running sum passes half the total. That only works for non-negative numbers.

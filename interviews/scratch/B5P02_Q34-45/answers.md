### Q34 ⭐ 🟡 Why a window breaks with negatives. Show with a concrete failing case that the shrink-while-too-big window gives the wrong answer for 'longest subarray with sum at most k' when `nums` may contain negatives, then give the correct way for 'longest subarray with sum exactly k' when negatives are allowed (prefix sums in a dict of first index; the counting version is Part 1 Q13). Your answer must state the missing property (monotonicity of the window sum) and say where deep prefix-sum material continues (Part 13). Example: nums=[4,-3,1], k=2: the true longest subarray with sum <= 2 is the whole array (length 3) but the naive shrinking window returns 2; and for 'sum exactly k': nums=[1,-1,5,-2,3], k=3 -> 4; nums=[-2,-1,2,1], k=1 -> 2.
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution)
**Pattern:** Sliding window needs a monotone window sum. With negatives that property is gone, so switch to prefix sums plus a dict (exact) or prefix sums plus binary search (at most).

**Say this first (1 line):** A shrink-when-too-big window assumes that dropping an element never raises the sum and adding one never lowers it; negatives break both, so I move to prefix sums.

**Brute force:** Try every start and extend the end, keeping the longest valid one. O(n^2) time, O(1) space. Correct for any values.

**Optimal:**
- The missing property is monotonicity of the window sum. With non-negatives, a bigger window never has a smaller sum, so "too big" can be fixed only by shrinking from the left.
- With negatives, a window that is too big can become valid by extending right (a negative arrives), and shrinking can make the sum bigger. The left pointer would discard starts that were still useful.
- Exact sum k: let P[i] be the prefix sum. A subarray (i, j] has sum k when P[j] - P[i] = k. Scan j, look up P[j] - k in a dict that stores the FIRST index each prefix value was seen. Never overwrite it, because the earliest start gives the longest subarray. Counting version: Part 1 Q13 (Subarray sum equals k).
- At most k (extra, so you have a correct reference): for each j we need the smallest i with P[i] >= P[j] - k. That i is always a prefix-maximum record, so keep records in increasing order and use `bisect_left`. O(n log n).
- Deep prefix-sum material continues in Part 13.

**Complexity:** Exact: one pass, O(1) average per dict operation, so O(n) time and O(n) space. At most k: O(n log n) time (one bisect per index), O(n) space. Naive window: O(n), but wrong with negatives.

**Dry run:** nums = [4, -3, 1], k = 2, naive shrinking window.
- r=0: sum 4 > 2, drop 4, window empty, length 0.
- r=1: sum -3, length 1.
- r=2: sum -2, length 2. Returns 2.
- Truth: the whole array sums to 2, length 3. The left pointer threw away the 4 too early, and the -3 would have repaired it.

Exact sum, nums = [1, -1, 5, -2, 3], k = 3. Prefixes: 0, 1, 0, 5, 3, 6, first = {0:-1}.
- i=0 (p=1): need -2, absent. Store 1 at 0.
- i=1 (p=0): need -3, absent. 0 already stored, keep -1.
- i=2 (p=5): need 2, absent. Store 5 at 2.
- i=3 (p=3): need 0, found at -1, length 3-(-1) = 4. Store 3 at 3.
- i=4 (p=6): need 3, found at 3, length 1. Best = 4.

**Code:**
```python
import random
from bisect import bisect_left

def brute_le(nums, k):
    best = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s <= k:
                best = max(best, j - i + 1)
    return best

def naive_window_le(nums, k):
    # shrink-while-too-big: only valid for non-negative values
    l = s = best = 0
    for r, v in enumerate(nums):
        s += v
        while s > k and l <= r:
            s -= nums[l]; l += 1
        best = max(best, r - l + 1)
    return best

def correct_le(nums, k):
    # prefix sums P; want smallest i<=j with P[i] >= P[j]-k.
    # Smallest such i is always a prefix-maximum record, so binary search the records.
    rec_idx, rec_val, p = [0], [0], 0
    best = 0
    for j, v in enumerate(nums, 1):
        p += v
        # records have strictly increasing values; first record with value >= p-k
        pos = bisect_left(rec_val, p - k)
        if pos < len(rec_val):
            best = max(best, j - rec_idx[pos])
        if p > rec_val[-1]:
            rec_idx.append(j); rec_val.append(p)
    return best

def brute_eq(nums, k):
    best = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s == k:
                best = max(best, j - i + 1)
    return best

def longest_eq(nums, k):
    first = {0: -1}          # prefix sum -> FIRST index seen (earliest start = longest)
    p = best = 0
    for i, v in enumerate(nums):
        p += v
        if p - k in first:
            best = max(best, i - first[p - k])
        first.setdefault(p, i)   # never overwrite
    return best

# prompt examples
assert brute_le([4, -3, 1], 2) == 3 and correct_le([4, -3, 1], 2) == 3
print("nums=[4,-3,1] k=2: true", brute_le([4, -3, 1], 2), "| naive window", naive_window_le([4, -3, 1], 2), "| prefix+bisect", correct_le([4, -3, 1], 2))
assert naive_window_le([4, -3, 1], 2) == 2
for nums, k, exp in [([1, -1, 5, -2, 3], 3, 4), ([-2, -1, 2, 1], 1, 2)]:
    assert longest_eq(nums, k) == brute_eq(nums, k) == exp
    print("exact", nums, k, "->", longest_eq(nums, k))
# edge cases
assert longest_eq([], 0) == 0 and longest_eq([5], 5) == 1 and longest_eq([5], 4) == 0
assert longest_eq([0, 0, 0], 0) == 3 and longest_eq([1, -1, 1, -1], 0) == 4
assert correct_le([], 5) == 0 and correct_le([-5], -6) == 0 and correct_le([-5], -5) == 1

random.seed(34)
bad_neg = bad_nonneg = 0
for _ in range(1500):
    n = random.randint(0, 9)
    nums = [random.randint(-5, 5) for _ in range(n)]
    k = random.randint(-6, 8)
    assert longest_eq(nums, k) == brute_eq(nums, k), (nums, k)
    assert correct_le(nums, k) == brute_le(nums, k), (nums, k)
    if naive_window_le(nums, k) != brute_le(nums, k): bad_neg += 1
    pos = [abs(x) for x in nums]
    kk = abs(k)
    if naive_window_le(pos, kk) != brute_le(pos, kk): bad_nonneg += 1
print("random cases with negatives where naive window is wrong:", bad_neg, "of 1500")
print("random cases with non-negatives where naive window is wrong:", bad_nonneg)
assert bad_neg > 0 and bad_nonneg == 0
print("all checks passed")
```

**Output (my run):**
```text
nums=[4,-3,1] k=2: true 3 | naive window 2 | prefix+bisect 3
exact [1, -1, 5, -2, 3] 3 -> 4
exact [-2, -1, 2, 1] 1 -> 2
random cases with negatives where naive window is wrong: 401 of 1500
random cases with non-negatives where naive window is wrong: 0
all checks passed
```

Both prompt examples are right: the naive window returns 2 against a true answer of 3, and the exact-sum answers are 4 and 2. In my random run the naive window was wrong on 401 of 1500 cases with negatives and on none with non-negatives (sandbox run, seeded).

**Edge cases:**
- Empty array: 0.
- Prefix 0 must be pre-seeded at index -1, otherwise subarrays starting at index 0 are missed.
- Zeros and +1/-1 alternation: many equal prefixes, so keep the first index only.
- No valid subarray: return 0 (state the convention, or -1 if the interviewer prefers).
- k negative: fine for the dict version.

**Follow-ups:**
- Does the naive window work for "sum exactly k" with positives? Yes, strictly positive values make the sum strictly increasing in the window length, so one shrink rule is enough.
- Can I get "at most k" with negatives in O(n)? There are monotonic-deque style versions; the bisect version is simpler to defend in an interview. Part 13 goes deeper.
- What if the interviewer wants the count of subarrays? Store counts in the dict instead of first indices (Part 1 Q13).

**Common mistakes:**
- Overwriting the dict value with a later index (shortens the answer).
- Forgetting the `{0: -1}` seed.
- Calling it a sliding-window problem because the statement says "subarray".
- Claiming the window works if "most numbers are positive". One negative is enough to break it.

---

### Q35 ⭐ 🟡 When a sliding window works and when it does not. For each task decide, with the one property you rely on, whether a two-pointer window gives O(n): (a) longest subarray with sum <= k, non-negative values; (b) the same with negative values; (c) count of subarrays with at most k distinct values; (d) longest subarray with exactly k distinct values (length only); (e) shortest subarray with sum >= k, non-negative values. Name the monotone predicate (extending the window never turns a bad window good, shrinking never turns a good one bad) and give a tiny failing case for the 'no' answers. Example: for (b) with nums=[4,-3,1], k=2 -> true answer 3, shrinking window returns 2; for (a) with nums=[1,2,3], k=3 -> 2.
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports
**Pattern:** Decide before coding whether the validity predicate is monotone. A window gives O(n) only when it is.

**Say this first (1 line):** I ask one question: if the window is bad, does extending never fix it, and if it is good, does shrinking never break it; if yes, two pointers, if no, prefix sums or another tool.

**Brute force:** For each task, test every (i, j) pair: O(n^2) pairs times an O(1) prefix-sum or O(n) set check. Fine as a reference only.

**Optimal:** The monotone predicate: extending the window never turns a bad window good, shrinking never turns a good window bad (for a "bad = too big" constraint). Verdicts:

| Task | Window O(n)? | Property relied on | Failing case if no |
|---|---|---|---|
| (a) longest, sum <= k, values >= 0 | Yes | sum never decreases when extending | none |
| (b) longest, sum <= k, negatives | No | sum is not monotone in the window | [4,-3,1], k=2: true 3, shrinking window 2 |
| (c) count subarrays with at most k distinct | Yes | distinct count never decreases when extending | none |
| (d) longest with exactly k distinct (length only) | Yes, with a trick | "at most k" is monotone; exactly k is read off it | see below |
| (e) shortest, sum >= k, values >= 0 | Yes | sum never decreases when extending, so shrink while still valid | none |

- (d) detail: "exactly k" itself is not monotone (adding a new value can break it, removing can break it). But for each right end, the leftmost start that keeps at most k distinct gives the longest candidate. If that window has exactly k distinct, it is the longest exactly-k window ending there. If it has fewer, then every shorter window ending there has fewer too, so nothing qualifies. So length-only works; the COUNT of exactly-k windows does not (use at_most(k) minus at_most(k-1), as in Q33 in this part).
- (e) flips the direction: here the window is shrunk while it is still good, recording the length each time.

**Complexity:** For the yes cases each element enters and leaves the window at most once, so O(n) time; space O(1) for the sum tasks and O(k) for the distinct tasks (a Counter with at most k+1 keys). The inner `while` loops do not make it quadratic, since the left pointer only moves forward.

**Dry run:** (a) nums = [1, 2, 3], k = 3.
- r=0: sum 1, length 1. r=1: sum 3, length 2 (best 2).
- r=2: sum 6 > 3, drop 1 (5), drop 2 (3), window [3], length 1.
- Answer 2. (b) nums = [4, -3, 1], k = 2 gives 2 from the window, 3 from brute force (see Q34).

**Code:**
```python
import random
from collections import defaultdict

# (a) longest subarray with sum <= k, non-negative values
def a_brute(nums, k):
    return max([j - i for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if sum(nums[i:j]) <= k] or [0])
def a_window(nums, k):
    l = s = best = 0
    for r, v in enumerate(nums):
        s += v
        while s > k and l <= r:
            s -= nums[l]; l += 1
        best = max(best, r - l + 1)
    return best

# (c) count subarrays with at most k distinct
def c_brute(nums, k):
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if len(set(nums[i:j])) <= k)
def c_window(nums, k):
    if k < 0: return 0
    cnt = defaultdict(int); l = total = 0
    for r, v in enumerate(nums):
        cnt[v] += 1
        while len(cnt) > k:
            cnt[nums[l]] -= 1
            if cnt[nums[l]] == 0: del cnt[nums[l]]
            l += 1
        total += r - l + 1
    return total

# (d) longest subarray with exactly k distinct (length only)
def d_brute(nums, k):
    return max([j - i for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if len(set(nums[i:j])) == k] or [0])
def d_window(nums, k):
    cnt = defaultdict(int); l = best = 0
    for r, v in enumerate(nums):
        cnt[v] += 1
        while len(cnt) > k:
            cnt[nums[l]] -= 1
            if cnt[nums[l]] == 0: del cnt[nums[l]]
            l += 1
        if len(cnt) == k:           # the at-most-k window is also the longest exactly-k one ending at r
            best = max(best, r - l + 1)
    return best

# (e) shortest subarray with sum >= k, non-negative values
def e_brute(nums, k):
    return min([j - i for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if sum(nums[i:j]) >= k] or [0])
def e_window(nums, k):
    l = s = 0; best = 0
    for r, v in enumerate(nums):
        s += v
        while s >= k and l <= r:
            best = r - l + 1 if best == 0 else min(best, r - l + 1)
            s -= nums[l]; l += 1
    return best

# (b) the same as (a) but with negatives: the window is wrong
print("(b) nums=[4,-3,1], k=2: true", a_brute([4, -3, 1], 2), "window", a_window([4, -3, 1], 2))
assert a_brute([4, -3, 1], 2) == 3 and a_window([4, -3, 1], 2) == 2
print("(a) nums=[1,2,3], k=3:", a_window([1, 2, 3], 3))
assert a_window([1, 2, 3], 3) == a_brute([1, 2, 3], 3) == 2
# (d) failing case for the NAIVE idea "shrink while distinct != k" (not monotone): shows why we shrink on > k only
print("(d) [1,2,1,2,3], k=2 ->", d_window([1, 2, 1, 2, 3], 2), "; (c) at most 2 ->", c_window([1, 2, 1, 2, 3], 2))
assert d_window([1, 2, 1, 2, 3], 2) == 4 and c_window([1, 2, 1, 2, 3], 2) == 12
# (c) exactly-k COUNT with one window is not possible: a window with exactly k can start in many places
assert d_window([], 1) == 0 and e_window([], 1) == 0 and d_window([7], 2) == 0 and d_window([7], 1) == 1

random.seed(35)
for _ in range(1500):
    n = random.randint(0, 9)
    nn = [random.randint(0, 5) for _ in range(n)]
    k = random.randint(1, 12)
    assert a_window(nn, k) == a_brute(nn, k), (nn, k)
    assert e_window(nn, max(k, 1)) == e_brute(nn, max(k, 1)), (nn, k)
    vals = [random.randint(1, 4) for _ in range(n)]
    kd = random.randint(1, 4)
    assert c_window(vals, kd) == c_brute(vals, kd), (vals, kd)
    assert d_window(vals, kd) == d_brute(vals, kd), (vals, kd)
print("(a), (c), (d), (e) match brute force on 1500 seeded cases each")
```

**Output (my run):**
```text
(b) nums=[4,-3,1], k=2: true 3 window 2
(a) nums=[1,2,3], k=3: 2
(d) [1,2,1,2,3], k=2 -> 4 ; (c) at most 2 -> 12
(a), (c), (d), (e) match brute force on 1500 seeded cases each
```

The prompt examples hold: (b) true 3 versus window 2, and (a) gives 2. The check also confirms (a), (c), (d), (e) against brute force on 1500 seeded cases each.

**Edge cases:**
- k larger than any sum: (a) returns n; (e) returns 0 (none).
- (a) with a single element larger than k: window becomes empty, length 0.
- (d) with fewer than k distinct values in the whole array: 0.
- All values zero in (a)/(e): sums do not grow, but the logic still works (monotone, not strict).

**Follow-ups:**
- Why not shrink while distinct != k for (d)? A window with fewer than k distinct would be shrunk wrongly; shrink only on "more than k".
- (e) with negatives? Prefix sums plus a deque (Q43).
- Strictly positive versus non-negative: only monotone is needed, strict is not.

**Common mistakes:**
- Applying the window to (b) because it "looks like" (a).
- Counting exactly-k windows with one pointer.
- Forgetting that in (e) the update happens inside the shrink loop, not after it.
- Letting `l` run past `r` without a `l <= r` guard when the sum is already bad for a single element.

---

### Q36 ⭐ 🟡 Invariants and off-by-one patterns in windows. For a window `[l, r]` (inclusive) versus `[l, r)` (half-open) state the length formula, the number of fixed-size windows in a list of length n and window k, the index at which the first full window is complete, and when `l` may pass `r`. Then compute all fixed-window sums for nums=[1,3,2,6,-1,4,1,8,2], k=5 using add-one-drop-one with your formulas stated first, and name the three bugs you check last (window count n-k+1, dropping `nums[r-k]` not `nums[r-k+1]`, and an empty window). Example: window sums -> [11, 14, 12, 18, 14] (max 18).
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports
**Pattern:** Fixed-size sliding window: add the new element, drop the one that left. The whole question is index discipline.

**Say this first (1 line):** I fix the convention first, inclusive `[l, r]` has length `r - l + 1`, then derive the count and the drop index from it.

**Brute force:** Recompute `sum(nums[i:i+k])` for every start: O(n * k) time.

**Optimal:** Sum the first k elements, then for each new right index r, add `nums[r]` and subtract `nums[r - k]`. O(n) time, O(1) extra space (excluding the output list).

Formulas for a list of length n and window k (0 < k <= n):
| Quantity | Inclusive `[l, r]` | Half-open `[l, r)` |
|---|---|---|
| length | r - l + 1 | r - l |
| number of fixed windows | n - k + 1 | n - k + 1 |
| first full window completes at | r = k - 1 | r = k |
| window ending at r starts at | l = r - k + 1 | l = r - k |
| element that leaves when r arrives | nums[r - k] | nums[r - k] |

- `l` may pass `r` only for the empty window: inclusive `l = r + 1` means length 0; half-open `l = r` means length 0. A variable-size window can reach this after shrinking; a fixed window never does.
- If k > n there are zero windows, not a negative count.

**Complexity:** O(n) time, each index added once and dropped once. Space O(1) beyond the n-k+1 outputs.

**Dry run:** nums = [1, 3, 2, 6, -1, 4, 1, 8, 2], k = 5, n = 9, so n-k+1 = 5 windows.
- First window [1,3,2,6,-1] = 11 (completes at r = 4).
- r=5: +4, -nums[0]=1 gives 14.
- r=6: +1, -nums[1]=3 gives 12.
- r=7: +8, -nums[2]=2 gives 18.
- r=8: +2, -nums[3]=6 gives 14.
- Sums [11, 14, 12, 18, 14], max 18.

**Code:**
```python
import random

def window_sums(nums, k):
    n = len(nums)
    if k <= 0 or k > n:
        return []
    s = sum(nums[:k])                 # first full window: indices 0..k-1, complete at r = k-1
    out = [s]
    for r in range(k, n):             # r enters, r-k leaves
        s += nums[r] - nums[r - k]
        out.append(s)
    return out

def brute(nums, k):
    return [sum(nums[i:i + k]) for i in range(len(nums) - k + 1)] if 0 < k <= len(nums) else []

nums, k = [1, 3, 2, 6, -1, 4, 1, 8, 2], 5
ws = window_sums(nums, k)
print("n =", len(nums), "k =", k, "windows =", len(ws), "(n-k+1 =", len(nums) - k + 1, ")")
print("window sums:", ws, "max:", max(ws))
assert ws == [11, 14, 12, 18, 14] and max(ws) == 18 and len(ws) == len(nums) - k + 1
# formulas
l, r = 3, 7
print("inclusive [3,7] length", r - l + 1, "| half-open [3,8) length", 8 - 3)
# the three bugs, each shown
wrong_drop = []  # bug: drop nums[r-k+1] instead of nums[r-k]
s = sum(nums[:k]); wrong_drop.append(s)
for r in range(k, len(nums)):
    s += nums[r] - nums[r - k + 1]
    wrong_drop.append(s)
print("bug (drop nums[r-k+1]) gives", wrong_drop, "-> wrong")
assert wrong_drop != ws
# edges
assert window_sums([], 3) == [] and window_sums([5], 1) == [5] and window_sums([1, 2], 3) == [] and window_sums([1, 2], 2) == [3]
assert window_sums([2, 2, 2], 0) == []
random.seed(36)
for _ in range(1000):
    a = [random.randint(-9, 9) for _ in range(random.randint(0, 12))]
    kk = random.randint(0, 14)
    assert window_sums(a, kk) == brute(a, kk)
print("1000 seeded random cases match brute force; edges pass")
```

**Output (my run):**
```text
n = 9 k = 5 windows = 5 (n-k+1 = 5 )
window sums: [11, 14, 12, 18, 14] max: 18
inclusive [3,7] length 5 | half-open [3,8) length 5
bug (drop nums[r-k+1]) gives [11, 12, 11, 13, 16] -> wrong
1000 seeded random cases match brute force; edges pass
```

The prompt's example is correct. The run also shows the off-by-one bug producing a wrong list.

**Edge cases:**
- k > n: return an empty list.
- k = 0: define as empty list (or ask).
- k = n: exactly one window.
- Negatives are fine, nothing here needs monotonicity.
- Empty input: empty list.

**Follow-ups:**
- Maximum average of k consecutive values? Same sums, divide the max by k.
- Variable k? Then it is not fixed-window; use prefix sums (O(1) per range).
- Very large arrays? Use a generator, yield each sum, keep O(1) memory.

**Common mistakes:**
- Number of windows as n - k (off by one).
- Dropping `nums[r - k + 1]` (this keeps a k-1 sized window and gives wrong sums, see the run).
- Using `sum(nums[r-k+1:r+1])` inside the loop and calling it O(n).
- Not handling k > n, which makes `range(k, n)` silently empty while the first sum covers a short slice.

---

### Q37 ⭐ 🟡 Boats to save people. `people[i]` is a weight (len <= 5*10^4, each weight <= limit). Each boat carries at most two people and total weight at most `limit`. Return the minimum number of boats. Sort, then pair the lightest remaining with the heaviest if they fit, else the heaviest goes alone; prove the greedy by an exchange argument. Example: people=[3,2,2,1], limit=3 -> 3; people=[3,5,3,4], limit=5 -> 4; people=[1,2], limit=3 -> 1.
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports
**Pattern:** Sort, then two pointers from both ends: pair the lightest remaining with the heaviest if they fit. It is a greedy proved by exchange.

**Say this first (1 line):** The heaviest person needs a boat anyway; if the lightest can share it, that is never worse, otherwise nobody can, so the heaviest goes alone.

**Brute force:** Try every way to group people into boats of at most two with a bitmask DP: O(2^n * n) time. Good as a checker for n <= 10, useless at n = 5*10^4.

**Optimal:**
- Sort ascending. `l` = lightest unplaced, `r` = heaviest unplaced.
- If `p[l] + p[r] <= limit`, they share a boat: `l += 1`.
- Either way the heaviest leaves: `r -= 1`, boat count +1.
- Invariant: everything outside `[l, r]` is already seated optimally.

Exchange argument:
- If even the lightest cannot ride with the heaviest h, nobody can (everyone else is heavier), so h rides alone. Forced.
- If the lightest `x` fits with h, take any optimal plan.
  - If h is alone: move x into h's boat. x's old boat only loses a person, so it still fits and the count does not go up.
  - If h is with some `y`, and x is in another boat with `z` (or alone): swap y and x. The boat with h now holds h + x <= h + y <= limit. The other boat holds y + z (or just y); since h is the heaviest, z <= h, so y + z <= y + h <= limit. It fits.
- So some optimal plan has h and x together. Repeat on the rest.

**Complexity:** Sorting O(n log n) dominates; the loop is O(n); space O(n) for the sorted copy (O(1) extra if sorting in place).

**Dry run:** people = [3, 2, 2, 1], limit 3, sorted [1, 2, 2, 3].
- l=0 (1), r=3 (3): 4 > 3, 3 alone. Boats 1.
- l=0, r=2 (2): 1 + 2 = 3, share. Boats 2, l=1.
- l=1, r=1 (2): single person, boat 3. Done: 3 boats.

**Code:**
```python
import random
from functools import lru_cache

def brute(people, limit):
    n = len(people)
    @lru_cache(maxsize=None)
    def go(mask):
        if mask == (1 << n) - 1: return 0
        i = next(b for b in range(n) if not mask >> b & 1)
        best = 1 + go(mask | 1 << i)                      # i rides alone
        for j in range(i + 1, n):
            if not mask >> j & 1 and people[i] + people[j] <= limit:
                best = min(best, 1 + go(mask | 1 << i | 1 << j))
        return best
    return go(0)

def boats(people, limit):
    p = sorted(people)
    l, r, cnt = 0, len(p) - 1, 0
    while l <= r:
        if p[l] + p[r] <= limit:
            l += 1               # lightest rides with heaviest
        r -= 1                   # heaviest always leaves in this boat
        cnt += 1
    return cnt

for ppl, lim, exp in [([3, 2, 2, 1], 3, 3), ([3, 5, 3, 4], 5, 4), ([1, 2], 3, 1)]:
    assert boats(ppl, lim) == brute(tuple(ppl), lim) == exp
    print(ppl, "limit", lim, "->", boats(ppl, lim))
assert boats([], 5) == 0 and boats([5], 5) == 1 and boats([2, 2, 2, 2], 4) == 2 and boats([5, 5, 5], 5) == 3
random.seed(37)
for _ in range(600):
    lim = random.randint(1, 10)
    ppl = [random.randint(1, lim) for _ in range(random.randint(0, 9))]
    assert boats(ppl, lim) == brute(tuple(ppl), lim), (ppl, lim)
print("600 seeded cases match the bitmask brute force; edges pass")
```

**Output (my run):**
```text
[3, 2, 2, 1] limit 3 -> 3
[3, 5, 3, 4] limit 5 -> 4
[1, 2] limit 3 -> 1
600 seeded cases match the bitmask brute force; edges pass
```

All three prompt examples are right (3, 4, 1).

**Edge cases:**
- Empty list: 0 boats.
- One person: 1 boat.
- Everyone weighs exactly `limit`: each alone.
- Everyone fits in pairs: ceil(n/2) boats.
- `l == r` (one person left): `p[l] + p[r]` double counts that person, but both branches end the loop with one boat, so it is harmless.

**Follow-ups:**
- What if a boat carries any number of people? That is bin packing (NP-hard); this greedy is only for at most two.
- Can you avoid sorting? Counting sort if weights are bounded by a small limit: O(n + limit).
- What if the problem asks for pairing indices? Keep `(weight, index)` pairs.

**Common mistakes:**
- Pairing the two lightest, or greedily pairing each person with the best fit in an unsorted pass.
- Moving `l` and `r` both every step, losing the "heaviest goes alone" case.
- Forgetting to sort.
- Using `while l < r` and then missing the last single person.

---

### Q38 ⭐ 🟡 Longest mountain in an array. A mountain is a run of length >= 3 that strictly rises to a peak then strictly falls. Return the length of the longest mountain subarray in `arr` (len <= 10^4) or 0, in one pass and O(1) space by expanding left and right from each peak and jumping the scan to the end of the found mountain. Example: [2,1,4,7,3,2,5] -> 5; [2,2,2] -> 0.
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports
**Pattern:** One-pass scan with expand-from-peak. Each mountain is expanded once and the scan then jumps past it.

**Say this first (1 line):** Find a peak (strictly bigger than both neighbours), walk left while rising and right while falling, record the length, and continue after the mountain's end.

**Brute force:** Check every subarray of length >= 3 for "strictly up then strictly down": O(n^3) naive, O(n^2) with a smarter check.

**Optimal:**
- Index i is a peak if `arr[i-1] < arr[i] > arr[i+1]`.
- From the peak, go left while `arr[l-1] < arr[l]`, right while `arr[r] > arr[r+1]`. Length = `r - l + 1`, at least 3 by construction.
- Then set `i = r + 1`. Two mountains share at most a valley point, and a valley is not a peak, so no peak is skipped. Each index is walked a constant number of times.
- O(1) extra space, no left/right arrays.

**Complexity:** Time O(n): the outer pointer only increases; each inner walk covers the mountain once and then the outer pointer jumps over it. Space O(1).

**Dry run:** arr = [2, 1, 4, 7, 3, 2, 5].
- i=1: 2 > 1 < 4, not a peak. i=2: 1 < 4 < 7, not a peak.
- i=3: 4 < 7 > 3, peak. Left: arr[1]=1 < arr[2]=4 so l=2... then arr[0]=2 < arr[1]=1 is false, so l stops at 1. Right: 7 > 3 > 2 so r=5; 2 > 5 is false, stop. Length 5-1+1 = 5.
- Jump to i = 6, the last index; the loop ends. Answer 5.

**Code:**
```python
import random

def brute(arr):
    best = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 2, n):
            seg = arr[i:j + 1]
            p = 0
            while p + 1 < len(seg) and seg[p] < seg[p + 1]: p += 1
            if p == 0 or p == len(seg) - 1: continue
            q = p
            while q + 1 < len(seg) and seg[q] > seg[q + 1]: q += 1
            if q == len(seg) - 1: best = max(best, len(seg))
    return best

def longest_mountain(arr):
    n, best, i = len(arr), 0, 1
    while i < n - 1:
        if arr[i - 1] < arr[i] > arr[i + 1]:        # i is a peak
            l = i - 1
            while l > 0 and arr[l - 1] < arr[l]: l -= 1
            r = i + 1
            while r < n - 1 and arr[r] > arr[r + 1]: r += 1
            best = max(best, r - l + 1)
            i = r + 1                                # jump past the mountain: each index scanned O(1) times
        else:
            i += 1
    return best

for a, exp in [([2, 1, 4, 7, 3, 2, 5], 5), ([2, 2, 2], 0)]:
    assert longest_mountain(a) == brute(a) == exp
    print(a, "->", longest_mountain(a))
assert longest_mountain([]) == 0 and longest_mountain([1]) == 0 and longest_mountain([1, 2]) == 0
assert longest_mountain([1, 2, 3]) == 0 and longest_mountain([3, 2, 1]) == 0 and longest_mountain([1, 3, 2]) == 3
assert longest_mountain([1, 3, 3, 2]) == 0 and longest_mountain([0, 1, 0, 1, 0]) == 3
random.seed(38)
for _ in range(1500):
    a = [random.randint(0, 4) for _ in range(random.randint(0, 11))]
    assert longest_mountain(a) == brute(a), a
print("1500 seeded cases match brute force; edges pass")
```

**Output (my run):**
```text
[2, 1, 4, 7, 3, 2, 5] -> 5
[2, 2, 2] -> 0
1500 seeded cases match brute force; edges pass
```

Both prompt examples are right (5 and 0).

**Edge cases:**
- Length < 3: 0.
- Strictly increasing or strictly decreasing: 0 (no peak).
- Plateau at the top (1,3,3,2): not a mountain, 0.
- Equal neighbours on a slope break the mountain (strictness).
- Two mountains sharing a valley: [0,1,0,1,0] gives 3.

**Follow-ups:**
- Do it with two arrays (up[i], down[i])? Simpler, O(n) space. The one-pass version trades that for O(1).
- Return the mountain itself? Keep the best `l` and `r`.
- Allow a flat peak? Change the comparisons; define the rules first.

**Common mistakes:**
- Using `<=` and accepting plateaus.
- Counting a pure ascent as a mountain.
- Not jumping `i`, which makes long slopes quadratic when a start is rescanned.
- Off-by-one on the `l` and `r` bounds (`l > 0`, `r < n - 1`).

---

### Q39 ⭐ 🟡 Minimum operations to reduce x to zero. Given positive integers `nums` and a target x, each operation removes the leftmost or rightmost element and subtracts it from x. Return the fewest operations to reach exactly 0, or -1. Convert to 'find the longest middle window with sum total - x' using a positive-values window. Example: nums=[1,1,4,2,3], x=5 -> 2; nums=[5,6,7,8,9], x=4 -> -1; nums=[3,2,20,1,1,3], x=10 -> 5.
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports
**Pattern:** Reformulate. Removing from both ends leaves a contiguous middle block, so the problem becomes "longest window with sum total - x". Values are positive, so a window works.

**Say this first (1 line):** What I remove is a prefix and a suffix; what stays is a middle subarray with sum `total - x`, and I want that middle as long as possible.

**Brute force:** Try every split (a from the left, b from the right) and check the sum: O(n^2) pairs (my checker also recomputes each sum, so it is slower; fine for tiny n).

**Optimal:**
- `target = sum(nums) - x`. If target < 0, answer -1 (cannot remove more than the total).
- Window with sum exactly target: expand right; while the sum exceeds target, shrink left. Valid because all values are positive (monotone, see Q34 and Q35).
- Track the longest window whose sum equals target. Answer is `n - longest`, or -1 if none.
- Special case target = 0: x equals the total, so the middle is empty (length 0) and all n elements are removed.

**Complexity:** O(n) time, each pointer moves forward only; O(1) space.

**Dry run:** nums = [1, 1, 4, 2, 3], x = 5. total = 11, target = 6.
- r=0: 1. r=1: 2. r=2: 6 equals target, window [1,1,4], longest 3.
- r=3: 8 > 6, drop 1 (7), drop 1 (6), window [4,2] sums 6, length 2 (longest stays 3).
- r=4: 9, drop 4 (5), window [2,3] sums 5, not equal.
- Longest 3, answer 5 - 3 = 2 (remove 3 and 2 from the right).

**Code:**
```python
import random

def brute(nums, x):
    n, best = len(nums), -1
    for a in range(n + 1):                # take a from the left
        for b in range(n - a + 1):        # take b from the right
            taken = sum(nums[:a]) + (sum(nums[n - b:]) if b else 0)
            if taken == x and (best == -1 or a + b < best):
                best = a + b
    return best

def min_ops(nums, x):
    target = sum(nums) - x
    if target < 0: return -1
    l = s = 0
    longest = -1                           # -1: no middle window found
    for r, v in enumerate(nums):
        s += v
        while s > target and l <= r:       # valid shrink because values are positive
            s -= nums[l]; l += 1
        if s == target:
            longest = max(longest, r - l + 1)
    if target == 0: longest = max(longest, 0)
    return -1 if longest == -1 else len(nums) - longest

for nums, x, exp in [([1, 1, 4, 2, 3], 5, 2), ([5, 6, 7, 8, 9], 4, -1), ([3, 2, 20, 1, 1, 3], 10, 5)]:
    assert min_ops(nums, x) == brute(nums, x) == exp
    print(nums, "x =", x, "->", min_ops(nums, x))
assert min_ops([1, 2, 3], 6) == 3 and min_ops([1, 2, 3], 7) == -1 and min_ops([5], 5) == 1 and min_ops([5], 3) == -1
assert min_ops([1, 1, 1, 1], 4) == 4 and min_ops([2, 3], 3) == 1
random.seed(39)
for _ in range(1500):
    nums = [random.randint(1, 5) for _ in range(random.randint(1, 8))]
    x = random.randint(1, 25)
    assert min_ops(nums, x) == brute(nums, x), (nums, x)
print("1500 seeded cases match brute force; edges pass")
```

**Output (my run):**
```text
[1, 1, 4, 2, 3] x = 5 -> 2
[5, 6, 7, 8, 9] x = 4 -> -1
[3, 2, 20, 1, 1, 3] x = 10 -> 5
1500 seeded cases match brute force; edges pass
```

All three prompt examples are right (2, -1, 5).

**Edge cases:**
- x larger than the total: -1.
- x equals the total: n.
- No middle window hits the target: -1.
- Single element equal to x: 1.
- Zeros in `nums` (not allowed by the prompt): the window still finds a longest window, since sums are non-decreasing, but say that you assumed positive.

**Follow-ups:**
- Why not greedy "take the larger end"? Counter-example: [3,2,20,1,1,3], x=10 needs 3+2 from the left and 3+1+1 from the right; no end-greedy rule finds that reliably.
- With negatives allowed? Prefix sums with a dict of first index (Q34).
- Why longest and not shortest middle? Fewest removals means most kept.

**Common mistakes:**
- Trying a greedy or recursion over both ends (wrong or exponential).
- Searching for the shortest window instead of the longest.
- Forgetting the target = 0 case.
- Returning the window length instead of `n - length`.

---

### Q40 ⭐ 🟡 K-th smallest in the union of two sorted lists by a merge walk. `a` and `b` are sorted non-decreasing; k is 1-based and counts duplicates (1 <= k <= len(a)+len(b)). Return the k-th smallest of all elements by advancing two pointers k steps without building the merged list, in O(k) time and O(1) space. Mention that Part 5 covers the O(log(min(m,n))) version, and that merging in place from the back is Part 1 Q22. Example: a=[1,3,5,7], b=[2,4,6], k=5 -> 5; a=[1,1,2], b=[1,2,2], k=4 -> 2.
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports
**Pattern:** Two-pointer merge walk, stopped after k steps. It is the merge step of merge sort without building the output.

**Say this first (1 line):** I advance whichever list has the smaller front, k times, and the last value I took is the answer.

**Brute force:** Concatenate and sort, then index `k - 1`: O((m+n) log(m+n)) time, O(m+n) space. It is my checker.

**Optimal:**
- Pointers i on `a`, j on `b`. Each step takes `a[i]` if `b` is exhausted or `a[i] <= b[j]`, else `b[j]`.
- After k steps the last taken value is the k-th smallest, duplicates counted separately.
- O(k) time, which is O(m+n) in the worst case. O(1) space.
- Part 5 covers the O(log(min(m, n))) partition-by-binary-search version. Merging in place from the back is Part 1 Q22.

**Complexity:** k iterations of O(1) work, so O(k) time (at most m+n). Space O(1).

**Dry run:** a = [1, 3, 5, 7], b = [2, 4, 6], k = 5.
- Take 1 (a), 2 (b), 3 (a), 4 (b), 5 (a). The fifth taken value is 5.

a = [1, 1, 2], b = [1, 2, 2], k = 4.
- Take 1 (a), 1 (a), then a[2]=2 > b[0]=1 so take 1 (b), then a[2]=2 <= b[1]=2 so take 2 (a). Fourth is 2.

**Code:**
```python
import random

def brute(a, b, k):
    return sorted(a + b)[k - 1]

def kth_union(a, b, k):
    i = j = 0
    cur = None
    for _ in range(k):
        if j >= len(b) or (i < len(a) and a[i] <= b[j]):
            cur = a[i]; i += 1
        else:
            cur = b[j]; j += 1
    return cur

for a, b, k, exp in [([1, 3, 5, 7], [2, 4, 6], 5, 5), ([1, 1, 2], [1, 2, 2], 4, 2)]:
    assert kth_union(a, b, k) == brute(a, b, k) == exp
    print(a, b, "k =", k, "->", kth_union(a, b, k))
assert kth_union([], [4], 1) == 4 and kth_union([4], [], 1) == 4
assert kth_union([1, 2], [3, 4], 4) == 4 and kth_union([5, 6], [1, 2], 3) == 5
assert kth_union([2, 2], [2, 2], 3) == 2 and kth_union([-3, 0], [-5, 1], 2) == -3
random.seed(40)
for _ in range(1500):
    a = sorted(random.randint(-5, 5) for _ in range(random.randint(0, 7)))
    b = sorted(random.randint(-5, 5) for _ in range(random.randint(0, 7)))
    if not a and not b: continue
    k = random.randint(1, len(a) + len(b))
    assert kth_union(a, b, k) == brute(a, b, k), (a, b, k)
print("1500 seeded cases match sorted(a + b)[k-1]; edges pass")
```

**Output (my run):**
```text
[1, 3, 5, 7] [2, 4, 6] k = 5 -> 5
[1, 1, 2] [1, 2, 2] k = 4 -> 2
1500 seeded cases match sorted(a + b)[k-1]; edges pass
```

Both prompt examples are right (5 and 2).

**Edge cases:**
- One list empty: the `j >= len(b)` and `i < len(a)` guards handle it.
- k = 1 and k = m + n.
- All duplicates: they count, so k=3 of [2,2] and [2,2] is 2.
- Negative values: no effect.
- k out of range: I assume 1 <= k <= m + n as the prompt states; raise otherwise.

**Follow-ups:**
- Faster? Binary search on the partition, O(log(min(m, n))), Part 5.
- Median of two sorted arrays? Use the k-th element (twice for an even total), or the Part 5 method.
- Streams or iterators? `heapq.merge` does the same walk lazily.

**Common mistakes:**
- Merging whole lists, using O(m+n) memory when the prompt asked for O(1).
- Indexing `a[i]` after `a` is exhausted (IndexError).
- Treating k as 0-based.
- Removing duplicates (the prompt counts them).

---

### Q41 ⭐ 🔴 Substring with concatenation of all words. Given a string `s` and a list `words` of equal-length strings (word length <= 30, up to 5000 words, repeats allowed), return all start indices (ascending) where `s` contains each word exactly the required number of times back to back in some order. Slide a window in word-sized steps for each of the L offsets, with a Counter of words and a count of words matched, giving O(L * n) word steps instead of re-checking every start. Example: s='barfoothefoobarman', words=['foo','bar'] -> [0, 9]; s='wordgoodgoodgoodbestword', words=['word','good','best','word'] -> []; s='barfoofoobarthefoobarman', words=['bar','foo','the'] -> [6, 9, 12].
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Company-tagged prep pages (a Jointaro interview-question page files this problem under an Uber path and Educative and NeetCode solution pages cover it; snippets only, not opened; company tags on such pages are unverified)
**Pattern:** Word-sized sliding window with a Counter. Every word has the same length L, so a valid window is a run of whole words, and there are only L possible alignments.

**Say this first (1 line):** For each of the L offsets I slide a window one whole word at a time, keeping a count of words inside and shrinking from the left when a word appears too often.

**Brute force:** For every start index, cut `m` chunks of length L, build a Counter, compare to the target Counter. O(n * m * L) time. That is my checker.

**Optimal:**
- Let m = number of words, `need = Counter(words)`.
- For each offset `off` in `0..L-1`, scan positions `off, off+L, off+2L, ...`.
- Take the word `w` at `right`.
  - If `w` is not in `need`: no window across it can match. Clear the window, move `left` past it.
  - Else add it. While `have[w] > need[w]`, pop the left word and move `left` by L.
  - If the window holds m words (all counts within need and total m), then `left` is an answer. Pop one word from the left and continue.
- Collect answers from all offsets and sort.
- Invariant: inside the window every count is at most its need. So m words means exact match.

**Complexity:** Each offset visits about n/L words, and each word is added once and removed at most once. Over all L offsets that is about n word operations in total. Each operation slices and hashes L characters, so O(n * L) character work, which is the prompt's O(L * n) bound. A bad version that re-checks every start costs O(n * m * L). Space O(m * L) for the Counters.

**Dry run:** s = 'barfoothefoobarman', words = ['foo', 'bar'], L = 3, m = 2. Offset 0.
- right 0 'bar': have {bar:1}, matched 1.
- right 3 'foo': matched 2 = m, record 0. Drop 'bar', left = 3, matched 1.
- right 6 'the': not a word, clear, left = 9.
- right 9 'foo': matched 1. right 12 'bar': matched 2, record 9. Drop 'foo'.
- right 15 'man': clear. Offsets 1 and 2 only see chunks like 'arf', 'oot', none in `need`. Answer [0, 9].

**Code:**
```python
import random
from collections import Counter

def brute(s, words):
    if not words: return []
    L, m = len(words[0]), len(words)
    need = Counter(words)
    out = []
    for i in range(len(s) - L * m + 1):
        chunks = [s[i + t * L: i + (t + 1) * L] for t in range(m)]
        if Counter(chunks) == need:
            out.append(i)
    return out

def find_concat(s, words):
    if not words or not s: return []
    L, m, n = len(words[0]), len(words), len(s)
    need = Counter(words)
    out = []
    for off in range(L):                       # L independent word-aligned scans
        have = Counter()
        left, matched = off, 0                 # matched = number of words inside the window
        for right in range(off, n - L + 1, L):
            w = s[right:right + L]
            if w not in need:                  # a foreign word breaks every window across it
                have.clear(); matched = 0; left = right + L
                continue
            have[w] += 1; matched += 1
            while have[w] > need[w]:           # too many copies of w: drop from the left
                have[s[left:left + L]] -= 1
                matched -= 1; left += L
            if matched == m:
                out.append(left)
                have[s[left:left + L]] -= 1    # slide one word so the scan continues
                matched -= 1; left += L
    return sorted(out)

for s, ws, exp in [("barfoothefoobarman", ["foo", "bar"], [0, 9]),
                   ("wordgoodgoodgoodbestword", ["word", "good", "best", "word"], []),
                   ("barfoofoobarthefoobarman", ["bar", "foo", "the"], [6, 9, 12])]:
    assert find_concat(s, ws) == brute(s, ws) == exp
    print(repr(s), ws, "->", find_concat(s, ws))
assert find_concat("", ["a"]) == [] and find_concat("aaa", []) == [] and find_concat("a", ["ab"]) == []
assert find_concat("aaaa", ["a", "a"]) == [0, 1, 2] and find_concat("abab", ["ab", "ab"]) == [0] and find_concat("abbaab", ["ab", "ba"]) == [0, 2]
assert find_concat("lingmindraboofooowingdingbarrwingmonkeypoundcake", ["fooo", "barr", "wing", "ding", "wing"]) == [13]
random.seed(41)
for _ in range(1500):
    L = random.randint(1, 3)
    pool = ["".join(random.choice("ab") for _ in range(L)) for _ in range(3)]
    words = [random.choice(pool) for _ in range(random.randint(1, 4))]
    s = "".join(random.choice(pool) for _ in range(random.randint(0, 9)))
    if random.random() < 0.3 and s:
        i = random.randrange(len(s)); s = s[:i] + random.choice("abc") + s[i + 1:]
    assert find_concat(s, words) == brute(s, words), (s, words)
print("1500 seeded cases match brute force; edges pass")
```

**Output (my run):**
```text
'barfoothefoobarman' ['foo', 'bar'] -> [0, 9]
'wordgoodgoodgoodbestword' ['word', 'good', 'best', 'word'] -> []
'barfoofoobarthefoobarman' ['bar', 'foo', 'the'] -> [6, 9, 12]
1500 seeded cases match brute force; edges pass
```

All three prompt examples are right ([0, 9], [], [6, 9, 12]).

**Edge cases:**
- Empty `s` or empty `words`: return [] (state the convention).
- `len(s) < L * m`: no windows, the loop simply never completes.
- Repeated words: `need` holds counts, and the `while have[w] > need[w]` shrink handles surplus.
- A word absent from `need`: reset the window.
- Overlapping matches (aaaa with a, a gives [0, 1, 2]).

**Follow-ups:**
- Why L offsets? A match can start at any character, but within one residue class mod L the word boundaries line up, so each class is one independent scan.
- Could you re-hash instead of slicing? Rolling hash per word, with collision risk; slicing is simpler and safe.
- Words of different lengths? This approach fails; that is a different problem (trie or DP).

**Common mistakes:**
- Checking only start 0, L, 2L, ... and missing offsets.
- Not shrinking when a word is over-counted, then counting duplicates wrongly.
- Rebuilding a Counter per start (the brute force).
- Not clearing the window after a foreign word.
- Forgetting to sort the answer when merging offsets.

---

### Q42 ⭐ 🔴 Minimum window subsequence. Given strings `s` and `t`, return the shortest contiguous substring of `s` in which `t` is a subsequence (letters in order, not necessarily adjacent), or '' if none; on ties return the leftmost. Scan forward to complete a match, then walk back from the end to tighten the left edge, then restart one past that left edge; give the O(len(s)*len(t)) bound. Example: s='abcdebdde', t='bde' -> 'bcde'; s='jmeqksfrsdcmsiwvaovztaqenprpvnbstl', t='u' -> ''.
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Company-tagged prep pages (a Jointaro interview-question page files this problem under an Uber path and Educative and NeetCode solution pages cover it; snippets only, not opened; company tags on such pages are unverified)
**Pattern:** Two-phase window: forward scan to complete a subsequence match, backward scan to tighten the left edge. The window is not monotone in the usual sense, so there is no plain shrink rule.

**Say this first (1 line):** Scan forward until t is fully matched at some end, walk back from that end matching t in reverse to find the tightest start, record it, and restart just after that start.

**Brute force:** For every start i, extend j until `t` is a subsequence of `s[i:j]`, keep the shortest. O(len(s)^2 * len(t)) naive. It is my checker.

**Optimal:**
- Forward: pointer `i` over `s`, pointer `j` over `t`. When `s[i] == t[j]` advance `j`. When `j == len(t)`, the window ends at `i`.
- Backward: from that end, walk `i` left matching `t` from its last character to its first. The position where the first character matches is the tightest start for this end.
- Record length. Restart at `start + 1`, not at `end + 1`: a later start can give a shorter window that ends before the next forward match would.
- Strict `<` on length keeps the leftmost window on ties.
- Why the backward walk gives the shortest window for this end: greedy matching from the right takes the latest possible position for each character, so the start is as large as possible.

**Complexity:** Each forward-plus-backward round costs O(window length), and the restart moves at least one step. Worst case O(len(s) * len(t)) (for example s = 'aaaa...', t = 'aaa...'). Space O(1) beyond the answer slice.

**Dry run:** s = 'abcdebdde', t = 'bde'.
- Forward from 0: b at 1, d at 3, e at 4. End = 4.
- Backward from 4: e (4), d (3), skip c, b (1). Start = 1. Window 'bcde', length 4. Restart at 2.
- Forward from 2: b at 5, d at 6, skip d at 7, e at 8. End = 8.
- Backward from 8: e (8), d (7), skip d (6), b (5). Start = 5, window 'bdde', length 4, not shorter than 4. Keep the leftmost, 'bcde'.

**Code:**
```python
import random

def is_subseq(t, w):
    it = iter(w)
    return all(c in it for c in t)

def brute(s, t):
    best = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            if is_subseq(t, s[i:j]) and (best == "" or j - i < len(best)):
                best = s[i:j]
                break                      # shortest from this i; strict < keeps leftmost on ties
    return best

def min_window_subseq(s, t):
    if not t: return ""
    n, m = len(s), len(t)
    i = 0
    best_start, best_len = -1, n + 1
    while i < n:
        j = 0
        while i < n:                       # forward: complete the match
            if s[i] == t[j]:
                j += 1
                if j == m: break
            i += 1
        if i == n: break                   # could not finish a match
        end = i
        j = m - 1
        while j >= 0:                      # backward: tighten the left edge
            if s[i] == t[j]: j -= 1
            i -= 1
        i += 1
        if end - i + 1 < best_len:
            best_start, best_len = i, end - i + 1
        i += 1                             # restart one past the tightened left edge
    return "" if best_start < 0 else s[best_start:best_start + best_len]

for s, t, exp in [("abcdebdde", "bde", "bcde"), ("jmeqksfrsdcmsiwvaovztaqenprpvnbstl", "u", "")]:
    assert min_window_subseq(s, t) == brute(s, t) == exp
    print(repr(s), repr(t), "->", repr(min_window_subseq(s, t)))
assert min_window_subseq("", "a") == "" and min_window_subseq("abc", "") == "" and min_window_subseq("a", "a") == "a"
assert min_window_subseq("abc", "abcd") == "" and min_window_subseq("aaab", "ab") == "ab" and min_window_subseq("cnhczmccqouqadqtmjjzl", "mm") == "mccqouqadqtm"
assert min_window_subseq("abab", "ab") == "ab"          # tie: leftmost
random.seed(42)
for _ in range(2000):
    s = "".join(random.choice("abc") for _ in range(random.randint(0, 12)))
    t = "".join(random.choice("abc") for _ in range(random.randint(0, 4)))
    if t == "": continue
    assert min_window_subseq(s, t) == brute(s, t), (s, t)
print("2000 seeded cases match brute force; edges pass")
```

**Output (my run):**
```text
'abcdebdde' 'bde' -> 'bcde'
'jmeqksfrsdcmsiwvaovztaqenprpvnbstl' 'u' -> ''
2000 seeded cases match brute force; edges pass
```

Both prompt examples are right ('bcde' and '').

**Edge cases:**
- `t` not a subsequence of `s`: return ''.
- `t` empty: I return '' (state the convention).
- `len(t) == 1`: window of length 1 at the first match.
- Ties: leftmost (strict `<`).
- Repeated letters in `t` ('mm' in 'cnhczmccqouqadqtmjjzl' gives 'mccqouqadqtm').

**Follow-ups:**
- Why not restart at `end + 1`? You might skip a shorter window that starts after the tightened left edge but before `end`.
- Faster than O(n * m)? A DP over (position in s, position in t) has the same bound; precomputed next-occurrence tables help for repeated queries on the same `s`.
- How is it different from minimum window substring (the Counter-window question earlier in this part)? That one is order-free and uses a Counter; this one is order-sensitive.

**Common mistakes:**
- Using a Counter (ignores order).
- Restarting at `end + 1`.
- Forgetting the backward pass, so windows are too long.
- Using `<=` and returning the rightmost tie.

---

### Q43 ⭐ 🔴 Shortest subarray with sum at least k, with negatives allowed. Given integers `nums` (len <= 10^5, values may be negative) and k >= 1, return the length of the shortest non-empty contiguous subarray with sum >= k, or -1. A plain window fails, so use prefix sums and a deque of candidate start indices with increasing prefix values: pop from the front while the front satisfies the target, pop from the back while the back prefix is not smaller than the newcomer. Explain both pops. (Only the deque idea is covered here; the full monotonic queue family is Part 4 and deep prefix sums Part 13.) Example: nums=[1], k=1 -> 1; nums=[1,2], k=4 -> -1; nums=[2,-1,2], k=3 -> 3.
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Company-tagged prep pages (a Jointaro interview-question page files this problem under an Uber path and Educative and NeetCode solution pages cover it; snippets only, not opened; company tags on such pages are unverified)
**Pattern:** Prefix sums plus a monotonic deque of candidate start indices. A plain window fails because the sum is not monotone with negatives (Q34).

**Say this first (1 line):** With prefix sums the question is the smallest j - i with P[j] - P[i] >= k, and a deque keeps only starts that can still win.

**Brute force:** For every start, extend until the sum reaches k, keep the shortest. O(n^2) time, O(1) space.

**Optimal:**
- P[0] = 0, P[i] = sum of the first i numbers. For each end j we want the LARGEST i < j with P[j] - P[i] >= k.
- Keep a deque of indices whose prefix values are strictly increasing.
- Pop from the front while `P[j] - P[front] >= k`: record `j - front`. This start is done: any later end gives a longer window with the same start, so it can never improve the answer.
- Pop from the back while `P[back] >= P[j]`: the new index j is later (shorter windows) and has a prefix no larger (bigger differences), so j beats the back start for every future end.
- Append j.
- Each index is pushed once and popped once, so O(n).
- Only the deque idea is covered here; the full monotonic queue family is Part 4 and deep prefix sums Part 13.

**Complexity:** O(n) time (amortised, each index enters and leaves the deque once), O(n) space for P and the deque.

**Dry run:** nums = [2, -1, 2], k = 3. P = [0, 2, 1, 3].
- j=0: deque [0].
- j=1 (P=2): 2 - 0 = 2 < 3. Back P[0]=0 >= 2? No. Deque [0, 1].
- j=2 (P=1): 1 - 0 = 1 < 3. Back P[1]=2 >= 1, pop. Deque [0, 2].
- j=3 (P=3): 3 - 0 = 3 >= 3, record 3, pop 0. 3 - P[2]=2 < 3. Append: [2, 3].
- Answer 3.

**Code:**
```python
import random
from collections import deque

def brute(nums, k):
    best = -1
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s >= k:
                if best == -1 or j - i + 1 < best: best = j - i + 1
                break
    return best

def shortest(nums, k):
    n = len(nums)
    P = [0] * (n + 1)
    for i, v in enumerate(nums): P[i + 1] = P[i] + v
    dq = deque()                     # indices with strictly increasing prefix values
    best = n + 1
    for j in range(n + 1):
        while dq and P[j] - P[dq[0]] >= k:      # front start is good: record it, and it can never help later (any later end is longer)
            best = min(best, j - dq.popleft())
        while dq and P[dq[-1]] >= P[j]:         # back start is dominated: later AND not larger prefix means longer-never, sum-never-worse
            dq.pop()
        dq.append(j)
    return best if best <= n else -1

for nums, k, exp in [([1], 1, 1), ([1, 2], 4, -1), ([2, -1, 2], 3, 3)]:
    assert shortest(nums, k) == brute(nums, k) == exp
    print(nums, "k =", k, "->", shortest(nums, k))
assert shortest([], 1) == -1 and shortest([-5], 1) == -1 and shortest([84, -37, 32, 40, 95], 167) == 3
assert shortest([5, -10, 7], 7) == 1 and shortest([1, 1, 1], 3) == 3 and shortest([-1, -1], 1) == -1
random.seed(43)
for _ in range(2500):
    nums = [random.randint(-4, 6) for _ in range(random.randint(0, 10))]
    k = random.randint(1, 10)
    assert shortest(nums, k) == brute(nums, k), (nums, k)
print("2500 seeded cases match brute force; edges pass")
```

**Output (my run):**
```text
[1] k = 1 -> 1
[1, 2] k = 4 -> -1
[2, -1, 2] k = 3 -> 3
2500 seeded cases match brute force; edges pass
```

All three prompt examples are right (1, -1, 3).

**Edge cases:**
- Empty list or all negative: -1.
- A single element >= k: answer 1.
- k >= 1 is assumed. With k <= 0 the empty window semantics change; ask.
- Large values (Python ints do not overflow).
- Equal prefix values: pop with `>=` so the deque stays strictly increasing.

**Follow-ups:**
- Why not two pointers? Extending can lower the sum and shrinking can raise it, so no pointer rule is safe.
- Why pop the front only once per j? You pop repeatedly while the condition holds, and each start is popped at most once overall.
- Longest instead of shortest with sum >= k? Different structure (prefix-maximum records plus bisect), Part 13.

**Common mistakes:**
- Forgetting P[0] = 0 (windows starting at index 0).
- Popping the back with `>` instead of `>=`.
- Using a list with `pop(0)` (O(n) each). Use `collections.deque`.
- Returning n + 1 instead of -1 when nothing is found.

---

### Q44 ⭐ 🔴 Circular array loop. `nums` is a list of non-zero integers where each value is a jump forward (positive) or backward (negative) with indices taken modulo n. A cycle needs length > 1 and all its jumps in the same direction. Decide whether a cycle exists in O(n) time and O(1) space using fast and slow pointers on each start, abandoning a path as soon as the direction changes or a self-loop appears, and marking visited indices. Example: [2,-1,1,2,2] -> True; [-1,-2,-3,-4,-5,6] -> False; [1,-1,5,1,4] -> True (the cycle is indices 3, 4).
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports
**Pattern:** Fast and slow pointers on a functional graph (each index points to exactly one next index), with direction checking and visited marking for O(1) space.

**Say this first (1 line):** From each start I run Floyd's slow and fast pointers, but I abandon the path whenever the direction flips or a step lands on itself, and I mark dead indices so they are never walked again.

**Brute force:** Build `next[i] = (i + nums[i]) % n`. For every start follow the chain, find its cycle, and check it has length > 1 and all jumps in one direction. O(n^2) time (worst case), O(n) space. It is my checker.

**Optimal:**
- Each start: direction = sign of `nums[start]`.
- slow moves 1 step, fast moves 2 steps. Before each move, check the landing index: if it is already marked 0, or has the opposite sign, stop (the path is dead).
- If slow == fast: a cycle exists on this path. If one more step from slow returns to slow it is a self-loop (length 1), so it does not count; otherwise return True.
- After a failed run, walk the same path again and set each index with that direction to 0 so later starts skip it. Marking makes the total O(n): every index is walked a constant number of times.
- I copy the input because the algorithm writes zeros (say that out loud, or note it mutates).

**Complexity:** Time O(n), since each index is on at most one abandoned path and each path costs time proportional to its length. Space O(1) extra (O(n) if you copy the list as I do; the in-place version mutates the caller's list).

**Dry run:** nums = [2, -1, 1, 2, 2], n = 5. next = 0 to 2, 1 to 0, 2 to 3, 3 to 0, 4 to 1.
- Start 0, direction positive. slow=fast=0.
- Round 1: slow 2, fast 3 (two steps: 0 to 2 to 3). Not equal.
- Round 2: slow 3, fast 2 (3 to 0 to 2). Not equal.
- Round 3: slow 0, fast 0 (2 to 3 to 0). Equal, and one step from 0 is 2, not itself. Cycle 0, 2, 3, all positive: True.

**Code:**
```python
import random

def brute(nums):
    # exact definition on the functional graph i -> (i + nums[i]) % n
    n = len(nums)
    nxt = [(i + nums[i]) % n for i in range(n)]
    for start in range(n):
        seen = {}
        cur, step = start, 0
        while cur not in seen:
            seen[cur] = step; cur = nxt[cur]; step += 1
        cyc = [c for c, st in seen.items() if st >= seen[cur]]      # nodes on the cycle reached from start
        if len(cyc) > 1 and (all(nums[c] > 0 for c in cyc) or all(nums[c] < 0 for c in cyc)):
            return True
    return False

def circular_loop(nums_in):
    nums = list(nums_in)                         # we mark visited with 0, so work on a copy
    n = len(nums)
    def step(i):
        return (i + nums[i]) % n
    for s in range(n):
        if nums[s] == 0: continue
        direction = nums[s] > 0
        slow = fast = s
        while True:
            ns = step(slow)
            if nums[ns] == 0 or (nums[ns] > 0) != direction: break
            nf = step(fast)
            if nums[nf] == 0 or (nums[nf] > 0) != direction: break
            nf2 = step(nf)
            if nums[nf2] == 0 or (nums[nf2] > 0) != direction: break
            slow, fast = ns, nf2
            if slow == fast:
                if step(slow) == slow: break     # self-loop, length 1: not a cycle
                return True
        i = s                                    # abandon: zero out the whole dead path
        while nums[i] != 0 and (nums[i] > 0) == direction:
            nxt = step(i); nums[i] = 0; i = nxt
    return False

for a, exp in [([2, -1, 1, 2, 2], True), ([-1, -2, -3, -4, -5, 6], False), ([1, -1, 5, 1, 4], True)]:
    assert circular_loop(a) == brute(a) == exp
    print(a, "->", circular_loop(a))
assert circular_loop([1]) is False and circular_loop([-1, -1]) is True and circular_loop([2, 2]) is False
assert circular_loop([1, -1]) is False and circular_loop([3, 1, 2]) is True and circular_loop([-2, 1, -1, -2, -2]) is False
data = [2, -1, 1, 2, 2]; circular_loop(data); assert data == [2, -1, 1, 2, 2]   # input not mutated
random.seed(44)
for _ in range(4000):
    n = random.randint(1, 8)
    a = [random.choice([-1, 1]) * random.randint(1, 9) for _ in range(n)]
    assert circular_loop(a) == brute(a), a
print("4000 seeded cases match the functional-graph brute force; edges pass")
```

**Output (my run):**
```text
[2, -1, 1, 2, 2] -> True
[-1, -2, -3, -4, -5, 6] -> False
[1, -1, 5, 1, 4] -> True
4000 seeded cases match the functional-graph brute force; edges pass
```

All three prompt examples are right (True, False, True), and the third cycle is indices 3 and 4 as the prompt states: 3 to 3+1=4, 4 to 4+4=8 mod 5 = 3. For the second example, the 6 at index 5 lands on itself, a self-loop, so it fails; the negative run dies on the sign flip.

**Edge cases:**
- n = 1: any value lands on itself, so False.
- Jump that is a multiple of n: self-loop, not a cycle.
- Two elements pointing to each other with the same sign: valid (length 2).
- Mixed signs inside a cycle: invalid.
- Mutating the input: copy first if the caller needs it intact (my test asserts it stays unchanged).

**Follow-ups:**
- Why check direction on every step, not only at the start? A cycle needs all jumps the same sign, and a path can change sign midway.
- Why mark zero? To avoid re-walking dead paths and to keep O(n) total time.
- Without O(1) space? A visited-state array per start (0 unvisited, 1 in progress, 2 done) does the same walk with O(n) memory.

**Common mistakes:**
- Counting a self-loop as a cycle.
- Not normalising with `% n` (Python's `%` is already non-negative for a positive n, which makes this easy; in C or Java you must fix negatives).
- Not abandoning on sign change.
- Not marking dead nodes, which gives O(n^2).
- Mutating the caller's list unannounced.

---

### Q45 ⭐ 🔴 Longest subarray with max minus min at most limit. Given integers `nums` (len <= 10^5) and a limit >= 0, return the length of the longest contiguous subarray in which the largest and smallest values differ by at most `limit`. Slide a window with two deques (one decreasing for the max, one increasing for the min) and shrink while the gap exceeds the limit; say why a sorted container is the O(n log n) alternative. (Only the deque idea; the wider family is Part 4.) Example: nums=[8,2,4,7], limit=4 -> 2; nums=[10,1,2,4,7,2], limit=5 -> 4; nums=[4,2,2,2,4,4,2,2], limit=0 -> 3.
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports
**Pattern:** Variable sliding window with two monotonic deques, one tracking the window max and one the window min.

**Say this first (1 line):** The window is valid while max minus min is at most limit; extending can only widen the gap, so I shrink from the left whenever it breaks, reading max and min from the deque fronts.

**Brute force:** For every start, extend right while max - min <= limit, tracking both. O(n^2) time, O(1) space. It is my checker.

**Optimal:**
- `maxd` holds indices with decreasing values (front = window max). `mind` holds indices with increasing values (front = window min).
- For each new `v = nums[r]`: pop `maxd` from the back while the back value <= v, then push r. Pop `mind` from the back while the back value >= v, then push r.
- While `nums[maxd[0]] - nums[mind[0]] > limit`: advance `l`. If a front index is now left of `l`, pop it.
- Answer is the largest `r - l + 1`.
- Why it works: the predicate "gap <= limit" is monotone in the window. A wider window has a gap at least as large, so shrinking only helps and `l` never needs to move back.
- Sorted container alternative: a `SortedList` (third-party, `sortedcontainers`) or a `heapq` with lazy deletion gives max and min with O(log n) updates, so O(n log n) total. Deques are O(n) because each index enters and leaves each deque once. A plain `heapq` cannot delete from the middle, so it needs the lazy trick.
- Only the deque idea here; the wider monotonic family is Part 4.

**Complexity:** O(n) time (each index is pushed and popped at most once in each deque; `l` only increases), O(n) space worst case (a monotone input fills a deque).

**Dry run:** nums = [8, 2, 4, 7], limit = 4.
- r=0 (8): maxd [0], mind [0], gap 0, length 1.
- r=1 (2): maxd [0, 1]; mind pops 0 (8 >= 2), [1]. Gap 8 - 2 = 6 > 4: l = 1, pop index 0 from maxd. Gap 0. Length 1.
- r=2 (4): maxd pops 1 (2 <= 4), [2]; mind [1, 2]. Gap 4 - 2 = 2. Length 2, best 2.
- r=3 (7): maxd pops 2, [3]; mind [1, 2, 3]. Gap 7 - 2 = 5 > 4: l = 2, pop index 1 from mind, [2, 3]. Gap 7 - 4 = 3. Length 2.
- Answer 2.

**Code:**
```python
import random
from collections import deque

def brute(nums, limit):
    best = 0
    for i in range(len(nums)):
        lo = hi = nums[i]
        for j in range(i, len(nums)):
            lo, hi = min(lo, nums[j]), max(hi, nums[j])
            if hi - lo <= limit: best = max(best, j - i + 1)
            else: break
    return best

def longest(nums, limit):
    maxd, mind = deque(), deque()      # store (index); maxd values decreasing, mind values increasing
    l = best = 0
    for r, v in enumerate(nums):
        while maxd and nums[maxd[-1]] <= v: maxd.pop()
        maxd.append(r)
        while mind and nums[mind[-1]] >= v: mind.pop()
        mind.append(r)
        while nums[maxd[0]] - nums[mind[0]] > limit:
            l += 1
            if maxd[0] < l: maxd.popleft()      # drop indices that left the window
            if mind[0] < l: mind.popleft()
        best = max(best, r - l + 1)
    return best

for a, lim, exp in [([8, 2, 4, 7], 4, 2), ([10, 1, 2, 4, 7, 2], 5, 4), ([4, 2, 2, 2, 4, 4, 2, 2], 0, 3)]:
    assert longest(a, lim) == brute(a, lim) == exp
    print(a, "limit", lim, "->", longest(a, lim))
assert longest([], 3) == 0 and longest([5], 0) == 1 and longest([1, 5, 9], 0) == 1 and longest([1, 5, 9], 100) == 3
assert longest([7, 7, 7], 0) == 3 and longest([-5, -1, -3], 4) == 3
random.seed(45)
for _ in range(3000):
    a = [random.randint(-6, 6) for _ in range(random.randint(0, 12))]
    lim = random.randint(0, 8)
    assert longest(a, lim) == brute(a, lim), (a, lim)
print("3000 seeded cases match brute force; edges pass")
```

**Output (my run):**
```text
[8, 2, 4, 7] limit 4 -> 2
[10, 1, 2, 4, 7, 2] limit 5 -> 4
[4, 2, 2, 2, 4, 4, 2, 2] limit 0 -> 3
3000 seeded cases match brute force; edges pass
```

All three prompt examples are right (2, 4, 3).

**Edge cases:**
- Empty array: 0.
- limit = 0: longest run of equal values.
- Very large limit: the whole array.
- Equal values: the pops use `<=` and `>=`, so duplicates replace older ones; the front is still correct.
- Negative values: no effect.

**Follow-ups:**
- Why store indices, not values? To know when a front has left the window.
- Why can the deque front pop only once per shrink step? `l` moves by one, and at most one index equals `l - 1` in each deque.
- Count such subarrays instead? Add `r - l + 1` per r (every suffix of a valid window is valid, the same counting idea as at-most-k).

**Common mistakes:**
- Using a single Counter or heap without deleting expired entries.
- Keeping values only, so you cannot expire the front.
- Popping with strict `<` and breaking the monotone order on ties.
- Shrinking with an `if` instead of a `while`.

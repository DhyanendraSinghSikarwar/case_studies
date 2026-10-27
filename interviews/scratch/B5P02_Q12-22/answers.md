### Q12 ⭐⭐⭐ 🟡 Minimum size subarray with sum at least target. Given positive integers `nums` (1 <= len <= 10^5) and a positive `target`, return the length of the shortest contiguous subarray whose sum is >= target, or 0 if none exists. Shrink-while-valid sliding window in O(n); explain why positivity is what makes it correct. Example: target=7, nums=[2,3,1,2,4,3] -> 2 (the block [4,3]); target=4, nums=[1,4,4] -> 1; target=11, nums=[1,1,1,1,1,1,1,1] -> 0.
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution) | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports

**Pattern:** Variable-size sliding window, shrink while valid. Two pointers move only right. It works because every element is positive, so the window sum is monotone: adding grows it, removing shrinks it.

**Say this first (1 line):** I grow the right end until the sum reaches the target, then shrink from the left as long as it still does, recording the smallest width, and it is O(n) because each index enters and leaves once.

**Brute force:** Try every start, extend until the sum hits the target, keep the shortest. O(n^2) time, O(1) space. Too slow at n = 10^5.

**Optimal:**
- Keep `left`, a running `total`, and `best` (0 means none yet).
- For each `right`: add `nums[right]`.
- While `total >= target`: record `right - left + 1`, subtract `nums[left]`, move `left` up.
- Invariant after the while loop: `total < target`, so the window `[left..right]` is the longest-from-the-left window that is not yet valid.
- Why positivity matters: if the window `[l..r]` is valid, then any longer window starting at `l` is valid too, so we never need a bigger `r` for that `l`. Once we shrink past `l`, no shorter window ending at a later `r` is missed. With negatives the sum is not monotone: shrinking can raise the sum, so the "drop `left` and never look back" step loses answers. Negatives need prefix sums plus a monotonic deque (Q43 in this part, not this question).

**Complexity:** Time O(n). `right` moves n times, `left` moves at most n times in total, and each `while` iteration moves `left`. Space O(1).

**Dry run:** `target=7, nums=[2,3,1,2,4,3]`
- right=0..2: total 2, 5, 6. Not valid.
- right=3 (2): total 8 >= 7. width 4, best=4. Drop 2, total 6, left=1.
- right=4 (4): total 10. width 4 (left=1..4), best stays 4. Drop 3, total 7, left=2. Still >= 7: width 3, best=3. Drop 1, total 6, left=3.
- right=5 (3): total 9. width 3, best 3. Drop 2, total 7, left=4. width 2, best=2. Drop 4, total 3, left=5.
- Answer 2 (the block [4,3]).

**Code:**
```python
import random

def brute(nums, target):
    n, best = len(nums), 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s >= target:
                if best == 0 or j - i + 1 < best:
                    best = j - i + 1
                break
    return best

def optimal(nums, target):
    best = 0
    left = 0
    total = 0
    for right, x in enumerate(nums):
        total += x                      # expand
        while total >= target:          # shrink while still valid
            width = right - left + 1
            if best == 0 or width < best:
                best = width
            total -= nums[left]
            left += 1
    return best

assert optimal([2, 3, 1, 2, 4, 3], 7) == 2
assert optimal([1, 4, 4], 4) == 1
assert optimal([1] * 8, 11) == 0
assert optimal([], 5) == 0
assert optimal([5], 5) == 1
assert optimal([5], 6) == 0
assert optimal([1, 1, 1, 1], 4) == 4          # whole array
assert optimal([10, 1, 1], 3) == 1            # target already met by one element
assert optimal([3, 3, 3], 1) == 1             # tiny target

rng = random.Random(12)
for _ in range(600):
    a = [rng.randint(1, 6) for _ in range(rng.randint(0, 10))]
    t = rng.randint(1, 25)
    assert optimal(a, t) == brute(a, t), (a, t)
print("600 random cases agree with brute force")
print(optimal([2, 3, 1, 2, 4, 3], 7), optimal([1, 4, 4], 4), optimal([1] * 8, 11))
# why positivity matters: with a negative the window answer can be wrong
neg = [-3, 1]
true_len = min(j - i + 1 for i in range(len(neg)) for j in range(i, len(neg)) if sum(neg[i:j + 1]) >= 1)
print("with a negative", neg, "target 1: window says", optimal(neg, 1), "true answer", true_len)
```

**Output (my run):**
```
600 random cases agree with brute force
2 1 0
with a negative [-3, 1] target 1: window says 0 true answer 1
```

**Edge cases:**
- No valid window: return 0, not infinity. All eight 1s with target 11 gives 0.
- A single element already meets the target: answer 1.
- Whole array needed: answer n.
- Empty list: 0.
- Zeros: the algorithm also works with non-negative values. Only negatives break it.

**Follow-ups:**
- *What if there are negatives?* Window fails. Use prefix sums and a monotonic deque of indices (Q43 in this part; Q34 shows the failing case) in O(n).
- *Can you do it in O(n log n) another way?* Yes: prefix sums are increasing, so for each `i` binary search the smallest `j` with `prefix[j] - prefix[i] >= target`. Good as a second solution.
- *Exactly target instead of at least?* Positives: same window with `==` check, or a hashmap of prefix sums (Part 1).

**Common mistakes:**
- Using `if` instead of `while` for the shrink, so only one element leaves per step.
- Returning `float('inf')` or a huge number when nothing is found.
- Updating `best` after shrinking instead of before the subtraction.
- Claiming this works with negatives.

---

### Q13 ⭐⭐⭐ 🟡 Sort colors (Dutch national flag). `nums` holds only 0, 1 and 2 (len <= 300). Sort it in place in one pass with O(1) extra space and without calling a sort routine, using three pointers (low, mid, high). State the loop invariant for the four regions and why `mid` does not advance after a swap with `high`. Example: [2,0,2,1,1,0] -> [0,0,1,1,2,2]; [2,0,1] -> [0,1,2].
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution)

**Pattern:** Three-way partition with three pointers (Dutch national flag). One pass, in place. It applies because there are only three distinct values and the order is fixed: 0s, then 1s, then 2s.

**Say this first (1 line):** I keep three regions with `low`, `mid`, `high`, send 0s left and 2s right as `mid` scans, and leave 1s in the middle, all in one pass with no sort call.

**Brute force:** Call `sorted` or count the 0s, 1s and 2s and overwrite. Counting is two passes, O(n) time and O(1) space, and is fine in real life. Sorting is O(n log n). The prompt wants one pass and no sort routine.

**Optimal:**
- Start `low = mid = 0`, `high = n - 1`.
- Loop invariant (four regions):
  - `nums[0:low]` are all 0.
  - `nums[low:mid]` are all 1.
  - `nums[mid:high+1]` are unknown.
  - `nums[high+1:]` are all 2.
- Look at `nums[mid]`:
  - 0: swap with `nums[low]`, then `low += 1`, `mid += 1`. What comes back from `low` is always a 1 (or `low == mid`), so it is safe to step over.
  - 1: just `mid += 1`.
  - 2: swap with `nums[high]`, `high -= 1`. Do NOT advance `mid`.
- Why `mid` stays after a swap with `high`: the value that arrived from `high` has never been looked at. It could be a 0, 1 or 2, so it must be examined. After a swap with `low`, the arriving value is already known to be a 1, so we can move on.
- Stop when `mid > high`: the unknown region is empty.

**Complexity:** Time O(n): each step either moves `mid` right or moves `high` left, so at most n steps. Space O(1): three integers.

**Dry run:** `[2,0,2,1,1,0]` (low=0, mid=0, high=5)
- mid=0 sees 2: swap with idx 5 -> [0,0,2,1,1,2], high=4.
- mid=0 sees 0: swap with idx 0 (self), low=1, mid=1.
- mid=1 sees 0: swap with idx 1 (self), low=2, mid=2.
- mid=2 sees 2: swap with idx 4 -> [0,0,1,1,2,2], high=3.
- mid=2 sees 1: mid=3. mid=3 sees 1: mid=4. mid=4 > high=3, stop.
- Result [0,0,1,1,2,2].

**Code:**
```python
import random

def brute(nums):
    return sorted(nums)

def optimal(nums):
    low, mid, high = 0, 0, len(nums) - 1
    # [0, low) = 0s, [low, mid) = 1s, [mid, high] = unknown, (high, end) = 2s
    while mid <= high:
        v = nums[mid]
        if v == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif v == 1:
            mid += 1
        else:  # 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1          # do NOT advance mid: the swapped-in value is unseen
    return nums

def run(a):
    a = list(a)
    optimal(a)
    return a

assert run([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]
assert run([2, 0, 1]) == [0, 1, 2]
assert run([]) == []
assert run([1]) == [1]
assert run([2, 2, 2]) == [2, 2, 2]
assert run([0, 0, 0]) == [0, 0, 0]
assert run([2, 1, 0]) == [0, 1, 2]
assert run([1, 1, 1]) == [1, 1, 1]
assert run([2, 0]) == [0, 2]
# the in-place function really mutates its argument and returns the same object
x = [1, 0, 2]
assert optimal(x) is x and x == [0, 1, 2]

rng = random.Random(13)
for _ in range(800):
    a = [rng.randint(0, 2) for _ in range(rng.randint(0, 12))]
    assert run(a) == brute(a), a
print("800 random cases agree with sorted()")
print(run([2, 0, 2, 1, 1, 0]), run([2, 0, 1]))
# what goes wrong if mid advances after the swap with high
def buggy(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]; low += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]; high -= 1; mid += 1
    return nums
print("buggy on [1, 2, 0]:", buggy([1, 2, 0]))
```

**Output (my run):**
```
800 random cases agree with sorted()
[0, 0, 1, 1, 2, 2] [0, 1, 2]
buggy on [1, 2, 0]: [1, 0, 2]
```

**Edge cases:**
- Empty or single element: loop does not run or does nothing.
- All the same value: pointers just slide, no harm.
- Already sorted and reverse sorted.
- Self-swaps (`low == mid`) are harmless.
- The function must mutate the input; return value is optional.

**Follow-ups:**
- *Two passes with counts?* Also O(n) and simpler to get right. Mention it, but the one-pass is the ask.
- *Four or k colours?* Counting sort for small k, or repeated partitions. The Dutch flag trick is for three.
- *Is it stable?* No. Swaps reorder equal values, which does not matter for plain integers.
- *Same idea elsewhere?* Quicksort three-way partition for many duplicates.

**Common mistakes:**
- Advancing `mid` after swapping with `high` (the code above prints a wrong answer for `[1, 2, 0]`).
- Looping `while mid < high` and skipping the last unknown cell.
- Forgetting that the 0 branch must advance both `low` and `mid`.

---

### Q14 ⭐⭐⭐ 🔴 Trapping rain water. `height` is a list of n non-negative integers (n <= 2*10^4), each an elevation bar of width 1. Return the total units of water trapped between bars after rain. Give the prefix/suffix max arrays version (O(n) space) and the two-pointer version with O(1) space, and explain why the side with the smaller running max is the safe side to finalise. Example: [0,1,0,2,1,0,1,3,2,1,2,1] -> 6; [4,2,0,3,2,5] -> 9.
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution)

**Pattern:** Two pointers from both ends, with running maxima. (The same problem can be done with prefix/suffix max arrays or a monotonic stack; this part covers the two-pointer form.)

**Say this first (1 line):** Water above a bar equals min(tallest on its left, tallest on its right) minus its height, and with two pointers I always finalise the side whose running max is smaller, because the other side is guaranteed to have a wall at least that tall.

**Brute force:** For each bar scan left and right for the two maxima. O(n^2) time, O(1) space.

**Optimal (two versions):**
- Prefix/suffix arrays: `lm[i]` = max of `h[0..i]`, `rm[i]` = max of `h[i..n-1]`. Water at i = `min(lm[i], rm[i]) - h[i]`. O(n) time, O(n) space. Easy to explain first.
- Two pointers, O(1) space:
  - `l = 0`, `r = n-1`, `lmax = rmax = 0`.
  - If `h[l] < h[r]`: the left side is the limiting side. Update `lmax`, add `lmax - h[l]`, move `l`.
  - Otherwise do the mirror image on the right.
- Why the smaller side is safe: say `h[l] < h[r]`. Then the tallest bar anywhere right of `l` is at least `h[r]`, which is taller than `h[l]`. Every bar already passed on the left was finalised only because some right bar was taller than it, and that right bar is still right of `l`. So the true right max for `l` is at least `lmax`, and the left side is the bottleneck: water at `l` is exactly `lmax - h[l]` (after `lmax` includes `h[l]`). We never need the exact right max, only that it is big enough.

**Complexity:** Time O(n): each step moves one pointer inward. Space O(1) for two pointers, O(n) for prefix/suffix arrays.

**Dry run:** `[4,2,0,3,2,5]` (l=0, r=5)
- h[0]=4 < h[5]=5: lmax=4, add 0, l=1.
- h[1]=2 < 5: lmax=4, add 2 (total 2), l=2.
- h[2]=0 < 5: add 4 (total 6), l=3.
- h[3]=3 < 5: add 1 (total 7), l=4.
- h[4]=2 < 5: add 2 (total 9), l=5. Stop since l == r.
- Answer 9.

**Code:**
```python
import random

def brute(h):
    # for each bar: water = min(max to left incl, max to right incl) - h[i]
    total = 0
    for i in range(len(h)):
        total += min(max(h[:i + 1]), max(h[i:])) - h[i]
    return total

def prefix_suffix(h):
    n = len(h)
    if n == 0:
        return 0
    lm = [0] * n
    rm = [0] * n
    lm[0] = h[0]
    for i in range(1, n):
        lm[i] = max(lm[i - 1], h[i])
    rm[-1] = h[-1]
    for i in range(n - 2, -1, -1):
        rm[i] = max(rm[i + 1], h[i])
    return sum(min(lm[i], rm[i]) - h[i] for i in range(n))

def optimal(h):
    l, r = 0, len(h) - 1
    lmax = rmax = 0
    water = 0
    while l < r:
        if h[l] < h[r]:
            # a right wall at least as tall as h[l] exists, so the left max decides
            lmax = max(lmax, h[l])
            water += lmax - h[l]
            l += 1
        else:
            rmax = max(rmax, h[r])
            water += rmax - h[r]
            r -= 1
    return water

cases = [([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6), ([4, 2, 0, 3, 2, 5], 9),
         ([], 0), ([5], 0), ([3, 3], 0), ([1, 2, 3, 4], 0), ([4, 3, 2, 1], 0),
         ([3, 0, 3], 3), ([2, 0, 2], 2), ([0, 0, 0], 0), ([5, 4, 1, 2], 1)]
for h, want in cases:
    assert brute(h) == prefix_suffix(h) == optimal(h) == want, (h, want)

rng = random.Random(14)
for _ in range(800):
    h = [rng.randint(0, 6) for _ in range(rng.randint(0, 12))]
    assert optimal(h) == brute(h) == prefix_suffix(h), h
print("800 random cases: two-pointer, prefix/suffix and brute force agree")
print(optimal([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), optimal([4, 2, 0, 3, 2, 5]))
big = [(i * 7919) % 1000 for i in range(20000)]
assert optimal(big) == prefix_suffix(big)
print("n = 20000 two-pointer equals prefix/suffix:", optimal(big))
```

**Output (my run):**
```
800 random cases: two-pointer, prefix/suffix and brute force agree
6 9
n = 20000 two-pointer equals prefix/suffix: 9976140
```

**Edge cases:**
- Fewer than 3 bars: 0 water. Empty list must not crash the prefix/suffix version (guarded above).
- Monotone increasing or decreasing: 0 water.
- Equal heights at both ends: the `else` branch handles ties, either side is safe.
- A single deep valley between two tall bars: `[3,0,3]` gives 3.
- Bars of height 0 everywhere: 0.

**Follow-ups:**
- *Monotonic stack version?* Keep a stack of decreasing heights; when a taller bar arrives, pop the valley and add `(min(left wall, new) - valley) * width`. O(n) time, O(n) space; the stack family is Part 4.
- *Container with most water is similar?* Different goal: there you pick two lines and maximise area, moving the shorter line. Here every bar holds water.
- *2D trapping rain water?* Needs a min-heap flood from the border (a heap-based flood, outside this part).

**Common mistakes:**
- Deciding the side by comparing `lmax` and `rmax` in a half-updated state. Compare the current heights `h[l]` and `h[r]`, as above.
- Adding water before updating the running max, producing negative water.
- Forgetting that the prefix/suffix maxima include the bar itself.

---

### Q15 ⭐⭐⭐ 🔴 Minimum window substring. Given strings `s` and `t` (1 <= len <= 10^5, ASCII, `t` may repeat letters), return the shortest substring of `s` that contains every character of `t` with at least the required multiplicity, or '' if none exists; if several windows tie, return the leftmost. Use an expand-then-shrink window with a need counter and a single 'still missing' integer so each step is O(1). Example: s='ADOBECODEBANC', t='ABC' -> 'BANC'; s='a', t='aa' -> ''; s='a', t='a' -> 'a'.
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Company-tagged prep pages (a Jointaro interview-question page files this problem under an Uber path and Educative and NeetCode solution pages cover it; snippets only, not opened; company tags on such pages are unverified) | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution)

**Pattern:** Variable sliding window with a frequency map, expand then shrink. It applies because once a window contains all of `t`, any larger window from the same left end also does, so validity is monotone in the window size.

**Say this first (1 line):** I expand `right` until the window covers `t`, then shrink `left` as far as it stays valid, recording the best window each time, and a single `missing` counter tells me in O(1) whether the window is valid.

**Brute force:** For every start, extend the end until the window covers `t`, comparing counters each time. Up to O(n^2) windows and each cover check costs O(n), so O(n^2) to O(n^3). Fine for a sanity check only.

**Optimal:**
- `need[c]` = how many copies of `c` the window still needs. It may go negative, which means surplus copies in the window.
- `missing` = number of needed characters still absent, counted with multiplicity. It starts at `len(t)`.
- Adding `s[right]`: if `need[ch] > 0`, a needed copy arrived, so `missing -= 1`. Always `need[ch] -= 1`.
- While `missing == 0`: record the window if strictly shorter (strict `<` keeps the leftmost on ties). Remove `s[left]`: `need += 1`; if it is now `> 0` we lost a needed copy, so `missing += 1`. Then `left += 1`.
- Invariant: after the shrink loop, the window `[left..right]` is not valid (`missing > 0`), and every earlier `left` has been tried against the smallest `right` that made it valid.
- Characters not in `t` start at 0 in the Counter, so they go negative on entry and never reach `> 0` on exit. No special case.

**Complexity:** Time O(n + m): `right` and `left` each move at most n steps, every step is O(1), and building the counter is O(m) where m = len(t). Space O(k) for k distinct characters (at most 128 for ASCII).

**Dry run:** `s='ADOBECODEBANC'`, `t='ABC'`, so `missing=3`.
- right=0 A: missing 2. right=3 B: missing 1. right=5 C: missing 0. Window `ADOBEC` (length 6), best=6. Shrink: drop A, missing 1, left=1.
- right=9 B: surplus, no change. right=10 A: missing 0. Window `DOBECODEBA` (length 10), not better. Shrink while valid: lengths 9, 8, 7, 6 (`CODEBA`, not strictly better) until C leaves at left=5, missing 1.
- right=12 C: missing 0. Window `ODEBANC` (7). Shrink: drop O, D (window `EBANC` length 5, best=5), drop E, window `BANC` length 4, best=4. Dropping B makes missing 1.
- Answer `BANC`.

**Code:**
```python
import random
from collections import Counter

def brute(s, t):
    need = Counter(t)
    best = ''
    for i in range(len(s)):
        for j in range(i + len(t), len(s) + 1):
            if not (Counter(s[i:j]) & need) == need:
                continue
            if best == '' or j - i < len(best):
                best = s[i:j]
            break              # first j for this i is the shortest from i
    return best

def optimal(s, t):
    if not t or len(t) > len(s):
        return ''
    need = Counter(t)
    missing = len(t)               # characters still missing, counted with multiplicity
    left = 0
    best_len, best_start = len(s) + 1, 0
    for right, ch in enumerate(s):
        if need[ch] > 0:           # a still-needed copy arrives
            missing -= 1
        need[ch] -= 1              # may go negative: surplus copy
        while missing == 0:        # window valid: shrink
            if right - left + 1 < best_len:      # strict < keeps the leftmost tie
                best_len, best_start = right - left + 1, left
            need[s[left]] += 1
            if need[s[left]] > 0:  # we gave up a needed copy
                missing += 1
            left += 1
    return '' if best_len > len(s) else s[best_start:best_start + best_len]

assert optimal('ADOBECODEBANC', 'ABC') == 'BANC'
assert optimal('a', 'aa') == ''
assert optimal('a', 'a') == 'a'
assert optimal('', 'a') == ''
assert optimal('abc', '') == ''
assert optimal('aa', 'aa') == 'aa'
assert optimal('abcabc', 'cba') == 'abc'      # leftmost among ties
assert optimal('xyz', 'q') == ''
assert optimal('aabdec', 'abc') == 'abdec'
assert optimal('bba', 'ab') == 'ba'

rng = random.Random(15)
for _ in range(1000):
    s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 12)))
    t = ''.join(rng.choice('abc') for _ in range(rng.randint(1, 4)))
    assert optimal(s, t) == brute(s, t), (s, t)
print("1000 random cases agree with brute force")
print(repr(optimal('ADOBECODEBANC', 'ABC')), repr(optimal('a', 'aa')), repr(optimal('a', 'a')))
big = 'ab' * 50000
print("n = 100000:", len(optimal(big, 'ba' * 2)))
```

**Output (my run):**
```
1000 random cases agree with brute force
'BANC' '' 'a'
n = 100000: 4
```

**Edge cases:**
- `len(t) > len(s)`: return `''` immediately.
- `t` with repeated letters (`s='a'`, `t='aa'`): multiplicity matters, so answer `''`. This is why `missing` counts copies, not distinct letters.
- `t` empty: the prompt says len >= 1; the code returns `''` anyway.
- Ties: keep the leftmost (strict `<`).
- Whole string is the answer, or answer is length 1.

**Follow-ups:**
- *Why not a set of distinct letters?* It loses multiplicity. Use a distinct-letters-satisfied counter instead if you prefer: increment when `need[ch]` hits 0, decrement when it goes above 0.
- *Smaller `s` after filtering?* If `t` is tiny and `s` huge, build a list of (index, char) for characters in `t` only and slide over that. Helps when most of `s` is irrelevant.
- *Subsequence instead of substring?* That is the minimum window subsequence problem (Q42), which needs DP or a forward/backward scan, not this window.

**Common mistakes:**
- Using `if` instead of `while` for the shrink.
- Counting `missing` by distinct letters while the counts are by copies.
- Using `<=` when comparing lengths, which returns the rightmost tie.
- Slicing a new string for every candidate (O(n) each). Only record indices and slice once.
- Updating `need` for left before checking validity, so the record uses a stale window.

---

### Q16 ⭐⭐⭐ 🔴 Sliding window maximum. Given integers `nums` (1 <= len <= 10^5) and window size k (1 <= k <= len), return the maximum of every window of k consecutive elements, in O(n). Use a deque of indices kept in decreasing order of value; explain why elements that are smaller than a newcomer can be dropped forever and why each index enters and leaves once. (This question covers only the window use; the wider monotonic stack and queue family is Part 4.) Example: nums=[1,3,-1,-3,5,3,6,7], k=3 -> [3,3,5,5,6,7]; nums=[1], k=1 -> [1].
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Company-tagged prep pages (a Jointaro interview-question page files this problem under an Uber path and Educative and NeetCode solution pages cover it; snippets only, not opened; company tags on such pages are unverified)

**Pattern:** Fixed-size window with a monotonic deque of indices. The deque keeps only elements that could still become a window maximum. (Only the window use is covered here; the wider monotonic stack and queue family is Part 4.)

**Say this first (1 line):** I keep a deque of indices whose values decrease from front to back, so the front is always the current window maximum, and each index is pushed once and popped once.

**Brute force:** For each window take `max` of k elements. O((n-k+1)*k), which is O(n^2) when k is about n/2. A heap with lazy deletion gives O(n log n). Both are beaten by the deque.

**Optimal:**
- For each new index `i` with value `x`:
  - Pop from the back while `nums[back] <= x`. Why they can go: they are older (will leave the window sooner) AND not larger than `x`. So they can never be the maximum of any window that also contains `x`, and every window that contains them from now on also contains `x`. Dropped forever.
  - Push `i` at the back.
  - If the front index is `<= i - k`, it has left the window: pop it from the front.
  - Once `i >= k - 1`, the answer for this window is `nums[front]`.
- Invariant: indices in the deque are increasing, values at those indices are decreasing, all are inside the window.
- Storing indices (not values) is what lets us expire the front.

**Complexity:** Time O(n): every index is appended once and popped at most once (from the back or the front), so the total pops are at most n even though the `while` is nested. Space O(k): the deque never holds more than k indices.

**Dry run:** `nums=[1,3,-1,-3,5,3,6,7]`, `k=3`. Deque shown as values.
- i=0 (1): [1]. i=1 (3): pop 1, [3]. i=2 (-1): [3,-1]. Window full: out [3].
- i=3 (-3): [3,-1,-3]. Front idx 1 is inside (1 > 0). out [3,3].
- i=4 (5): pop -3,-1,3, [5]. out [3,3,5].
- i=5 (3): [5,3]. out [3,3,5,5].
- i=6 (6): pop 3, pop 5, [6]. out [...,6].
- i=7 (7): pop 6, [7]. out [3,3,5,5,6,7].

**Code:**
```python
import random
from collections import deque

def brute(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]

def optimal(nums, k):
    dq = deque()          # indices; values nums[dq[0]] >= nums[dq[1]] >= ... (decreasing)
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:    # smaller-or-equal elements can never be a max again
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:                 # front slid out of the window
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out

assert optimal([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
assert optimal([1], 1) == [1]
assert optimal([4, 2, 12, 3], 1) == [4, 2, 12, 3]
assert optimal([4, 2, 12, 3], 4) == [12]
assert optimal([5, 5, 5, 5], 2) == [5, 5, 5]
assert optimal([-3, -2, -1], 2) == [-2, -1]
assert optimal([9, 8, 7, 6], 2) == [9, 8, 7]        # decreasing: deque keeps everything
assert optimal([1, 2, 3, 4], 2) == [2, 3, 4]        # increasing: deque has one element

rng = random.Random(16)
for _ in range(1000):
    n = rng.randint(1, 12)
    a = [rng.randint(-5, 5) for _ in range(n)]
    k = rng.randint(1, n)
    assert optimal(a, k) == brute(a, k), (a, k)
print("1000 random cases agree with brute force")
print(optimal([1, 3, -1, -3, 5, 3, 6, 7], 3), optimal([1], 1))
big = [(i * 31337) % 10007 for i in range(100000)]
assert optimal(big[:3000], 500) == brute(big[:3000], 500)
print("n = 100000, k = 500 windows:", len(optimal(big, 500)))
```

**Output (my run):**
```
1000 random cases agree with brute force
[3, 3, 5, 5, 6, 7] [1]
n = 100000, k = 500 windows: 99501
```

**Edge cases:**
- `k = 1`: every element is its own window.
- `k = n`: single answer.
- Equal values: pop on `<=` (not `<`) keeps the deque small; popping only on `<` also works but holds duplicates. Either is correct, as the equal-values test shows.
- Strictly decreasing input: the deque grows to k.
- Strictly increasing input: deque length stays 1.
- Negative values: nothing special.

**Follow-ups:**
- *Heap alternative?* A max-heap of (value, index), lazily discard entries with index outside the window. O(n log n), simpler to write, uses more memory.
- *Window minimum?* Flip the comparison.
- *Why not a sorted container?* Insert and remove cost O(log k), so O(n log k); the deque is O(n).
- *Max minus min within a limit?* Two deques at once (Q45).

**Common mistakes:**
- Storing values, so you cannot tell when the front expired.
- Checking expiry with `dq[0] < i - k` (off by one); the window is `[i-k+1, i]`, so expire `<= i - k`.
- Emitting an answer before the first full window (`i < k - 1`).
- Using `list.pop(0)` instead of a deque: `list.pop(0)` is O(n) and turns the solution into O(n*k).

---

### Q17 ⭐⭐ 🟢 Is subsequence. Given strings `s` and `t` (len(s) <= 100, len(t) <= 10^4), decide whether `s` can be obtained from `t` by deleting some characters without reordering. Use one pointer into each string. Then answer the follow-up: if there are billions of different `s` queries against one `t`, what would you precompute? Example: s='ace', t='abcde' -> True; s='aec', t='abcde' -> False; s='', t='x' -> True.
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports

**Pattern:** Two pointers over two sequences (a "greedy match"). Matching each character of `s` at its earliest possible place in `t` can never hurt.

**Say this first (1 line):** I walk through `t` once and advance a pointer in `s` each time the characters match; if the `s` pointer reaches the end, it is a subsequence.

**Brute force:** Recursion: either match `s[i]` with `t[j]` or skip `t[j]`. Exponential without memo, O(len(s) * len(t)) with memo. Used below only as the checker.

**Optimal:**
- `i` points into `s`. Loop over each `ch` in `t`.
- If `i < len(s)` and `s[i] == ch`, do `i += 1`.
- Answer: `i == len(s)`.
- Greedy is safe because taking the earliest match leaves the longest possible remainder of `t` for the rest of `s`. An exchange argument: any valid matching can be shifted left to the earliest one without losing validity.
- Follow-up, billions of queries on one `t`: build `pos[ch]` = sorted list of indices of `ch` in `t` once. For each query keep `prev` (index of the last matched char) and binary search `pos[ch]` for the first index `> prev`. Query cost O(len(s) * log len(t)) instead of O(len(t)). (Part 5 owns binary search; here it is just `bisect_left`.) You can also build a `next[i][c]` table of size len(t)*26 for O(len(s)) per query, trading memory for speed.

**Complexity:** Single query: time O(len(t)) (one pass over `t`, a pointer into `s`), space O(1). Indexed version: preprocessing O(len(t)), each query O(len(s) log len(t)), space O(len(t)).

**Dry run:** `s='ace'`, `t='abcde'`
- ch='a': matches s[0], i=1.
- ch='b': s[1]='c' no.
- ch='c': match, i=2.
- ch='d': s[2]='e' no.
- ch='e': match, i=3. i == 3 == len(s): True.
- For `'aec'`: a matches (i=1), then 'e' is needed but t gives b, c, d first (no match), then e matches (i=2), end of t with s[2]='c' unmatched: False.

**Code:**
```python
import random
from bisect import bisect_left
from collections import defaultdict

def brute(s, t):
    # try every way: recursive match
    def go(i, j):
        if i == len(s):
            return True
        if j == len(t):
            return False
        return (s[i] == t[j] and go(i + 1, j + 1)) or go(i, j + 1)
    return go(0, 0)

def optimal(s, t):
    i = 0
    for ch in t:
        if i < len(s) and s[i] == ch:
            i += 1
    return i == len(s)

class Index:
    """Follow-up: many queries against one t. Precompute positions per letter."""
    def __init__(self, t):
        self.pos = defaultdict(list)
        for i, ch in enumerate(t):
            self.pos[ch].append(i)

    def is_subsequence(self, s):
        prev = -1                      # index in t of the last matched character
        for ch in s:
            lst = self.pos.get(ch)
            if not lst:
                return False
            k = bisect_left(lst, prev + 1)     # first occurrence strictly after prev
            if k == len(lst):
                return False
            prev = lst[k]
        return True

assert optimal('ace', 'abcde') is True
assert optimal('aec', 'abcde') is False
assert optimal('', 'x') is True
assert optimal('', '') is True
assert optimal('a', '') is False
assert optimal('abc', 'abc') is True
assert optimal('abcd', 'abc') is False      # s longer than t
assert optimal('aa', 'a') is False          # each char of t used once
assert optimal('aa', 'aba') is True

rng = random.Random(17)
for _ in range(1000):
    s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 5)))
    t = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 9)))
    want = brute(s, t)
    assert optimal(s, t) == want, (s, t)
    assert Index(t).is_subsequence(s) == want, (s, t)
print("1000 random cases: two pointers, binary-search index and brute force agree")
idx = Index('abcde')
print(optimal('ace', 'abcde'), optimal('aec', 'abcde'), optimal('', 'x'))
print([idx.is_subsequence(q) for q in ('ace', 'aec', '', 'z')])
```

**Output (my run):**
```
1000 random cases: two pointers, binary-search index and brute force agree
True False True
[True, False, True, False]
```

**Edge cases:**
- Empty `s` is always a subsequence (even of an empty `t`).
- Non-empty `s` and empty `t`: False.
- `s` longer than `t`: False (the code gets there naturally, or return early).
- Repeated letters: each character of `t` can be used once, so `'aa'` is not a subsequence of `'a'`.
- Subsequence is not substring: gaps are allowed.

**Follow-ups:**
- *Billions of queries?* Precompute letter positions (or a next-occurrence table) once and answer each query with binary search. Shown above.
- *Early exit?* Stop when `i == len(s)`. Also reject if `len(s) > len(t)`.
- *Which one is it if it is a stream?* Same pointer, update per arriving character of `t`.

**Common mistakes:**
- Advancing the `s` pointer when it does not match, or advancing both always.
- Forgetting the `i < len(s)` guard, which raises IndexError once `s` is fully matched.
- In the indexed version, searching from `prev` instead of `prev + 1`, which reuses the same character.

---

### Q18 ⭐⭐ 🟢 Partition an array by parity. Rearrange the list `nums` in place so every even value comes before every odd value, in O(n) time and O(1) space with opposite-ends pointers; any order within each group is acceptable, so a test must check the property, not one exact output. Say how this differs from the stable version in Part 1 Q5 (Move zeroes), and why swapping gives fewer writes but loses order. Example: [3,1,2,4] -> one valid result is [4,2,1,3] (evens 4,2 first, odds 1,3 after).
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution)

**Pattern:** Two pointers from opposite ends, partition in place. It applies because we only need a split into two classes, not a full order.

**Say this first (1 line):** One pointer from the left skips evens, one from the right skips odds, and when the left sits on an odd and the right on an even I swap them, so everything is placed with at most n/2 swaps in one pass.

**Brute force:** Build two lists (evens, odds) and concatenate: O(n) time, O(n) space, and it is stable. Or sort with a parity key: O(n log n). The prompt wants O(1) space.

**Optimal:**
- `l = 0`, `r = n - 1`.
- While `l < r`:
  - `nums[l]` even: `l += 1`.
  - else `nums[r]` odd: `r -= 1`.
  - else (left odd, right even): swap, `l += 1`, `r -= 1`.
- Invariant: `nums[:l]` all even, `nums[r+1:]` all odd, `nums[l..r]` unchecked. When the pointers meet, the unchecked region is empty (or one element, which is already in an acceptable place).
- Testing the property (a test must check this, not one exact output): same multiset as before, and once an odd appears no even follows.

**Complexity:** Time O(n): each iteration moves at least one pointer inward. Space O(1). Swaps: at most n/2, each swap fixes two positions.

**Dry run:** `[3,1,2,4]`
- l=0 (3 odd), r=3 (4 even): swap -> [4,1,2,3], l=1, r=2.
- l=1 (1 odd), r=2 (2 even): swap -> [4,2,1,3], l=2, r=1. Stop.
- Result `[4,2,1,3]`: evens first, then odds. A different valid answer is `[2,4,1,3]`.

**Code:**
```python
import random
from collections import Counter

def brute(nums):
    # stable reference: evens then odds, any order inside is allowed so only the property is checked
    return [x for x in nums if x % 2 == 0] + [x for x in nums if x % 2 == 1]

def optimal(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        if nums[l] % 2 == 0:
            l += 1
        elif nums[r] % 2 == 1:
            r -= 1
        else:                      # left is odd, right is even: swap them
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
    return nums

def valid(before, after):
    if Counter(before) != Counter(after):
        return False
    seen_odd = False
    for x in after:
        if x % 2 == 1:
            seen_odd = True
        elif seen_odd:
            return False
    return True

def run(a):
    b = list(a)
    optimal(b)
    assert valid(a, b), (a, b)
    return b

print("example result:", run([3, 1, 2, 4]))
run([]); run([7]); run([2]); run([2, 4, 6]); run([1, 3, 5]); run([1, 2]); run([2, 1])
run([0, 0, 1]); run([-3, -2, 5, 8])      # negatives: use x % 2 (Python gives 0 or 1 for negatives)
run([3, 1, 2, 4])
rng = random.Random(18)
for _ in range(1000):
    a = [rng.randint(-6, 9) for _ in range(rng.randint(0, 12))]
    run(a)
    assert valid(a, brute(a))
print("1000 random cases satisfy the parity property")
print("order change example:", run([1, 2, 3, 4]), "(stable would give [2, 4, 1, 3])")
```

**Output (my run):**
```
example result: [4, 2, 1, 3]
1000 random cases satisfy the parity property
order change example: [4, 2, 3, 1] (stable would give [2, 4, 1, 3])
```

**Edge cases:**
- Empty, single element: loop never runs.
- All even or all odd: no swaps.
- Negatives: use `x % 2` in Python (always 0 or 1). In C or Java `-3 % 2` is -1, so test `!= 0` there.
- Zero is even.
- Duplicates: no issue.

**Follow-ups:**
- *Difference from Part 1 Q5 (Move zeroes)?* Move zeroes must keep the order of the non-zeros, so it uses a write pointer that copies forward (stable, more writes). Here order inside each group is free, so swapping from both ends does fewer writes but is not stable.
- *Need it stable?* Use the write-pointer approach for one class and keep the order of the other, or stable partition in O(n log n) in place, or O(n) extra space.
- *Three classes?* That is the Dutch flag (Q13).

**Common mistakes:**
- Checking one exact expected output in a test, when many answers are valid.
- Swapping when both are the same parity.
- Using `while l <= r`, which can swap an element with itself or miscount.
- Assuming `x % 2 == 1` identifies odds in languages where negatives give -1.

---

### Q19 ⭐⭐ 🟢 Intersection of two sorted lists, keeping multiplicity. `a` and `b` are sorted non-decreasing integer lists. Return, as a sorted list, each value as many times as it appears in both (the minimum of its two counts) using two pointers and no hash map, in O(len(a)+len(b)). Compare with the hash-map approach when one list is far smaller than the other. Example: a=[1,2,2,3,4], b=[2,2,2,4,5] -> [2,2,4]; a=[1,3], b=[2,4] -> [].
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports

**Pattern:** Two pointers merging two sorted lists. Sortedness lets us decide, by comparing the two current values, which pointer can safely move.

**Say this first (1 line):** Walk both lists together: move the pointer with the smaller value, and when the values are equal emit one copy and move both, which gives exactly the minimum count of each value.

**Brute force:** For each element of `a`, search `b` for an unused equal value: O(len(a) * len(b)). Or count both lists in dictionaries and take the minimum per key: O(len(a) + len(b)) time, O(distinct) space. The prompt bans the hash map to show the pointer version.

**Optimal:**
- `i = j = 0`.
- `a[i] < b[j]`: `a[i]` has no partner at or after `j` (everything in `b` from `j` on is >= `b[j]`), so `i += 1`.
- `a[i] > b[j]`: symmetric, `j += 1`.
- Equal: output the value, `i += 1`, `j += 1`. Using up one copy from each side is what makes the count the minimum of the two counts. For `[2,2]` vs `[2,2,2]` it matches twice, then `a` runs out.
- Output is sorted because inputs are.

**Complexity:** Time O(len(a) + len(b)): each step advances at least one pointer. Space O(1) beyond the output.

**Dry run:** `a=[1,2,2,3,4]`, `b=[2,2,2,4,5]`
- 1 < 2: i=1. 2 == 2: out [2], i=2, j=1. 2 == 2: out [2,2], i=3, j=2.
- 3 > 2 is false: a[3]=3 > b[2]=2, so j=3. 3 < 4: i=4. 4 == 4: out [2,2,4], i=5. Stop.
- Result `[2, 2, 4]`.

**Code:**
```python
import random
from bisect import bisect_left
from collections import Counter

def brute(a, b):
    ca, cb = Counter(a), Counter(b)
    out = []
    for v in sorted(ca):
        out += [v] * min(ca[v], cb.get(v, 0))
    return out

def optimal(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        elif a[i] > b[j]:
            j += 1
        else:                  # equal: take it once, advance both (this keeps min count)
            out.append(a[i])
            i += 1
            j += 1
    return out

def by_search(small, big):
    # when small is far shorter: for each value binary search in big, resuming after the last hit
    out, lo = [], 0
    for x in small:
        k = bisect_left(big, x, lo)
        if k < len(big) and big[k] == x:
            out.append(x)
            lo = k + 1
        else:
            lo = k
    return out

assert optimal([1, 2, 2, 3, 4], [2, 2, 2, 4, 5]) == [2, 2, 4]
assert optimal([1, 3], [2, 4]) == []
assert optimal([], [1, 2]) == []
assert optimal([1, 2], []) == []
assert optimal([2, 2], [2, 2]) == [2, 2]
assert optimal([5], [5]) == [5]
assert optimal([1, 1, 1], [1]) == [1]
assert optimal([-3, -3, 0, 7], [-3, 0, 0, 9]) == [-3, 0]
assert optimal([1, 2, 3], [4, 5, 6]) == []

rng = random.Random(19)
for _ in range(1000):
    a = sorted(rng.randint(-4, 5) for _ in range(rng.randint(0, 10)))
    b = sorted(rng.randint(-4, 5) for _ in range(rng.randint(0, 10)))
    assert optimal(a, b) == brute(a, b), (a, b)
    assert by_search(a, b) == brute(a, b), (a, b)
print("1000 random cases: two pointers and binary-search variant agree with the Counter reference")
print(optimal([1, 2, 2, 3, 4], [2, 2, 2, 4, 5]), optimal([1, 3], [2, 4]))
```

**Output (my run):**
```
1000 random cases: two pointers and binary-search variant agree with the Counter reference
[2, 2, 4] []
```

**Edge cases:**
- Either list empty: empty result.
- No common values: empty result.
- Heavy duplicates on one side only: the minimum count rule handles it.
- Negatives and zero: nothing special.
- Identical lists: result equals the input.

**Follow-ups:**
- *One list is tiny?* Use the hash map of the small list or, since both are sorted, binary search each small value in the big one: O(small * log big), better than O(small + big) when small is very small. Shown as `by_search` above. If `b` is on disk and cannot fit in memory, stream `b` with the two-pointer walk and keep only `a` in memory (or the reverse, keep the smaller one).
- *Unsorted input?* Sort first (O(n log n)) or use the Counter approach.
- *Distinct intersection only?* Skip duplicates after a match, or use sets.
- *Both huge and on disk?* External sort, then the same merge walk.

**Common mistakes:**
- On a match, advancing only one pointer, which reports too many copies.
- Using a set, which drops multiplicity.
- Not skipping with the right comparison direction (moving the larger pointer).

---

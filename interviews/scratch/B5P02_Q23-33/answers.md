### Q23 ⭐⭐ 🟡 Max consecutive ones with k flips. Given a 0/1 list `nums` (len <= 10^5) and k >= 0, return the longest run of 1s you can get by flipping at most k zeros to ones. Frame it as the longest window containing at most k zeros and state the shrink condition. Example: nums=[1,1,1,0,0,0,1,1,1,1,0], k=2 -> 6; nums=[0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k=3 -> 10.
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports

**Pattern:** Variable sliding window with a budget. "At most k flips" means "window holds at most k zeros". Flipping is only a story; I never change the array.

**Say this first (1 line):** "Longest window with at most k zeros. Right edge expands every step, left edge moves only while zeros exceed k. O(n) time, O(1) space."

**Brute force:** For each start, extend right while zeros <= k, track the best. O(n^2) time, O(1) space. Fine for n = 20, too slow at 10^5.

**Optimal:**
- Walk `right` over the list. If `nums[right]` is 0, `zeros += 1`.
- Shrink condition: `while zeros > k`, drop `nums[left]` (if it is 0, `zeros -= 1`) and `left += 1`.
- Invariant: after the shrink, `[left, right]` holds at most k zeros. So all its zeros can be flipped, and the whole window becomes 1s.
- Answer is the maximum `right - left + 1`.
- Why O(n): `left` never moves back, so each index enters once and leaves once.

**Complexity:** Time O(n): two pointers, each moves forward at most n times. Space O(1): two ints and a counter.

**Dry run:** `nums=[1,1,1,0,0,0,1,1,1,1,0]`, `k=2`
| right | zeros after add | shrink? | window | length |
|---|---|---|---|---|
| 0-2 | 0 | no | [0..2] | 3 |
| 3 | 1 | no | [0..3] | 4 |
| 4 | 2 | no | [0..4] | 5 |
| 5 | 3 | yes, drop the 0 at index 3, left=4 | [4..5] | 2 |
| 6-9 | 2 | no | grows to [4..9] | 6 |
| 10 | 3 | yes, drop the 0 at index 4, left=5 | [5..10] | 6 |
Best is 6.

**Code:**
```python
import random


def ones_brute(nums, k):
    best = 0
    for i in range(len(nums)):
        zeros = 0
        for j in range(i, len(nums)):
            zeros += nums[j] == 0
            if zeros > k:
                break
            best = max(best, j - i + 1)
    return best


def ones_window(nums, k):
    left = zeros = best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:  # shrink until the window has at most k zeros
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


a = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
b = [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1]
print("example 1:", ones_window(a, 2), "(expected 6)")
print("example 2:", ones_window(b, 3), "(expected 10)")

random.seed(23)
for _ in range(1000):
    n = random.randint(0, 12)
    nums = [random.randint(0, 1) for _ in range(n)]
    k = random.randint(0, 4)
    assert ones_window(nums, k) == ones_brute(nums, k), (nums, k)
print("cross-check: 1000 seeded cases agree")

assert ones_window([], 3) == 0
assert ones_window([0], 0) == 0
assert ones_window([0], 1) == 1
assert ones_window([1, 1, 1], 0) == 3
assert ones_window([0, 0, 0], 0) == 0
assert ones_window([0, 0, 0], 5) == 3  # k larger than the zero count: whole list
assert ones_window([1, 0, 1, 0, 1], 0) == 1
big = [random.randint(0, 1) for _ in range(10 ** 5)]
assert ones_window(big, 10) >= 11
assert ones_window([1] * 10 ** 5, 0) == 10 ** 5
print("edge asserts passed")
```

**Output (my run):**
```text
example 1: 6 (expected 6)
example 2: 10 (expected 10)
cross-check: 1000 seeded cases agree
edge asserts passed
```

Both prompt examples are correct as written.

**Edge cases:**
- Empty list: 0.
- k = 0: longest run of 1s, no flips allowed.
- k at least the number of zeros: the whole list.
- All zeros, k = 0: 0. All ones: n.
- Flipping zero is not required to be done: "at most k" is the key.

**Follow-ups:**
- Return the start index too? Record `left` whenever you improve the best.
- What if the stream is huge and you cannot index back? Keep a queue of the zero positions (at most k+1 of them); the new left is just after the oldest zero. O(k) memory.
- Flip exactly k instead of at most k? If the list has at least k zeros the answer is the same, because a spare flip never shortens a run; ask the interviewer which they mean.

**Common mistakes:**
- Using `if zeros > k` instead of `while`. With a single step per right the window can stay invalid in other variants.
- Forgetting to decrement `zeros` only when the dropped element is 0.
- Computing length as `right - left` (forgets the +1).
- Counting ones instead of zeros and getting the shrink test backwards.

### Q24 ⭐⭐ 🟡 Fruit into baskets. A row of trees holds fruit types `fruits[i]` (len <= 10^5). You walk right from any start, picking one fruit per tree, with two baskets that each hold one type only; you must stop when a tree's fruit fits neither basket. Return the maximum fruits you can pick, i.e. the longest contiguous run with at most two distinct values. Use a Counter or dict window and delete keys whose count hits zero. Example: [1,2,1] -> 3; [0,1,2,2] -> 3; [1,2,3,2,2] -> 4.
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution)

**Pattern:** Variable sliding window with a distinct-count limit, state kept in a Counter. "Two baskets" is "at most 2 distinct values".

**Say this first (1 line):** "Longest contiguous run with at most two distinct fruit types. Counter window, shrink while it has more than two keys, delete keys at zero. O(n)."

**Brute force:** For each start, extend right while the set of types has size <= 2. O(n^2) time, O(1) space.

**Optimal:**
- Add `fruits[right]` to the Counter.
- While `len(count) > 2`, remove `fruits[left]`: decrement it, and `del` the key when it reaches 0. Then `left += 1`.
- Invariant: after the shrink, the window has at most 2 distinct types, and `len(count)` equals the number of distinct types in it.
- Track the max of `right - left + 1`.
- The window is monotone: shrinking never adds a type, extending never removes one. That is why one pass works.

**Complexity:** Time O(n): each index is added once and removed once. Space O(1): the Counter never holds more than 3 keys.

**Dry run:** `[1,2,3,2,2]`
| right | window | Counter | action | length |
|---|---|---|---|---|
| 0 | [0..0] | {1:1} | - | 1 |
| 1 | [0..1] | {1:1, 2:1} | - | 2 |
| 2 | [0..2] | 3 keys | remove type 1 (deleted), left=1 | 2 |
| 3 | [1..3] | {2:2, 3:1} | - | 3 |
| 4 | [1..4] | {2:3, 3:1} | - | 4 |
Answer 4.

**Code:**
```python
import random
from collections import Counter


def fruit_brute(fruits):
    best = 0
    for i in range(len(fruits)):
        seen = set()
        for j in range(i, len(fruits)):
            seen.add(fruits[j])
            if len(seen) > 2:
                break
            best = max(best, j - i + 1)
    return best


def fruit_window(fruits, baskets=2):
    count = Counter()
    left = best = 0
    for right, f in enumerate(fruits):
        count[f] += 1
        while len(count) > baskets:
            g = fruits[left]
            count[g] -= 1
            if count[g] == 0:
                del count[g]  # without this, len(count) never shrinks
            left += 1
        best = max(best, right - left + 1)
    return best


print("[1,2,1]:", fruit_window([1, 2, 1]), "(expected 3)")
print("[0,1,2,2]:", fruit_window([0, 1, 2, 2]), "(expected 3)")
print("[1,2,3,2,2]:", fruit_window([1, 2, 3, 2, 2]), "(expected 4)")

# what happens if you forget to delete zero-count keys
def fruit_buggy(fruits):
    count = Counter()
    left = best = 0
    for right, f in enumerate(fruits):
        count[f] += 1
        while len(count) > 2:
            count[fruits[left]] -= 1  # key stays with value 0
            left += 1
        best = max(best, right - left + 1)
    return best


try:
    print("buggy (no delete):", fruit_buggy([1, 2, 3, 2, 2]))
except IndexError:
    print("buggy (no delete) on [1,2,3,2,2]: IndexError (len(count) stays 3, left runs off the end)")

random.seed(24)
for _ in range(1000):
    n = random.randint(0, 12)
    fr = [random.randint(0, 3) for _ in range(n)]
    assert fruit_window(fr) == fruit_brute(fr), fr
print("cross-check: 1000 seeded cases agree")

assert fruit_window([]) == 0
assert fruit_window([5]) == 1
assert fruit_window([7, 7, 7, 7]) == 4
assert fruit_window([1, 2, 3]) == 2
assert fruit_window([1, 2, 1, 2, 1, 2]) == 6
assert fruit_window(list(range(10 ** 5))) == 2
assert fruit_window([1, 2] * 50000) == 10 ** 5
print("edge asserts passed")
```

**Output (my run):**
```text
[1,2,1]: 3 (expected 3)
[0,1,2,2]: 3 (expected 3)
[1,2,3,2,2]: 4 (expected 4)
buggy (no delete) on [1,2,3,2,2]: IndexError (len(count) stays 3, left runs off the end)
cross-check: 1000 seeded cases agree
edge asserts passed
```

All three prompt examples are correct as written. The `buggy` line shows what happens if you skip the delete: `len(count)` stays at 3 forever, so the shrink loop walks `left` off the end of the list.

**Edge cases:**
- Empty list: 0.
- One type only: n.
- Two types only: n.
- All different: 2.
- n = 10^5: fine, O(n).

**Follow-ups:**
- Three baskets, or k baskets? Same code, change the 2 to k (that is Q25).
- Return the actual segment? Store `left` at the best.
- Why not a set? Duplicates: when you drop one copy of type 2 the type may still be in the window. You need counts.

**Common mistakes:**
- Not deleting zero-count keys, so the distinct count is wrong (and with `while` it can crash or loop wrongly).
- Using `if` instead of `while` for the shrink. One removal does not always remove a whole type.
- Thinking the picking order matters. The walk is contiguous, so it is a window question.

### Q25 ⭐⭐ 🟡 Longest substring with at most k distinct characters. Given a string `s` (len <= 5*10^4) and an integer k >= 0, return the length of the longest substring with at most k distinct characters. Maintain a Counter window and shrink while the number of keys exceeds k; explain why the distinct count must be read from the keys that have positive count. Example: s='eceba', k=2 -> 3 (the substring 'ece'); s='aa', k=1 -> 2; s='abc', k=0 -> 0.
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Company-tagged prep pages (a Jointaro interview-question page files this problem under an Uber path and Educative and NeetCode solution pages cover it; snippets only, not opened; company tags on such pages are unverified)

**Pattern:** Same window as fruit baskets (Q24) with a general limit k. Counter window, shrink while distinct count is over k.

**Say this first (1 line):** "Counter of the window, `len(count)` is the distinct count, shrink while it exceeds k, delete keys at zero. k = 0 returns 0. O(n)."

**Brute force:** For each start, extend right with a set until the set exceeds k. O(n^2) time (worst case), O(k) space.

**Optimal:**
- Handle `k <= 0` first: no characters allowed, so 0.
- Add `s[right]`. While `len(count) > k`, decrement `s[left]`, delete the key when it hits 0, `left += 1`.
- The distinct count must come from keys with a positive count. A key with value 0 is a character that has left the window. If it stays in the dict, `len(count)` over-counts.
- Invariant: after the shrink, `len(count) <= k` and equals the true distinct count of `s[left..right]`.

**Complexity:** Time O(n): each character enters and leaves once. Space O(min(k, alphabet)); the Counter holds at most k+1 keys.

**Dry run:** `s='eceba'`, `k=2`
| right | char | Counter after shrink | window | length |
|---|---|---|---|---|
| 0 | e | {e:1} | e | 1 |
| 1 | c | {e:1, c:1} | ec | 2 |
| 2 | e | {e:2, c:1} | ece | 3 |
| 3 | b | 3 keys, drop e (e:1), still 3, drop c (deleted) -> {e:1, b:1} | eb | 2 |
| 4 | a | 3 keys, drop e (deleted) -> {b:1, a:1} | ba | 2 |
Best 3 ('ece').

**Code:**
```python
import random
from collections import Counter


def kdistinct_brute(s, k):
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            seen.add(s[j])
            if len(seen) > k:
                break
            best = max(best, j - i + 1)
    return best


def kdistinct_window(s, k):
    if k <= 0:
        return 0
    count = Counter()
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            out = s[left]
            count[out] -= 1
            if count[out] == 0:
                del count[out]
            left += 1
        best = max(best, right - left + 1)
    return best


print("eceba, 2:", kdistinct_window("eceba", 2), "(expected 3)")
print("aa, 1:", kdistinct_window("aa", 1), "(expected 2)")
print("abc, 0:", kdistinct_window("abc", 0), "(expected 0)")

# the stale-key bug: len(count) counts keys with value 0 too
def kdistinct_buggy(s, k):
    count = Counter()
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


try:
    print("buggy on eceba,2 ->", kdistinct_buggy("eceba", 2))
except IndexError:
    print("buggy on eceba,2 -> IndexError (zero-count keys keep len(count) above k, left runs off the end)")

random.seed(25)
for _ in range(1000):
    n = random.randint(0, 12)
    s = "".join(random.choice("abcd") for _ in range(n))
    k = random.randint(0, 4)
    assert kdistinct_window(s, k) == kdistinct_brute(s, k), (s, k)
print("cross-check: 1000 seeded cases agree")

assert kdistinct_window("", 3) == 0
assert kdistinct_window("a", 1) == 1
assert kdistinct_window("abc", 5) == 3  # k above the alphabet size: whole string
assert kdistinct_window("aaaa", 1) == 4
assert kdistinct_window("abcabc", 3) == 6
big = "".join(random.choice("abcdefgh") for _ in range(50000))
assert kdistinct_window(big, 8) == 50000
assert kdistinct_window(big, 1) >= 1
print("edge asserts passed")
```

**Output (my run):**
```text
eceba, 2: 3 (expected 3)
aa, 1: 2 (expected 2)
abc, 0: 0 (expected 0)
buggy on eceba,2 -> IndexError (zero-count keys keep len(count) above k, left runs off the end)
cross-check: 1000 seeded cases agree
edge asserts passed
```

All prompt examples are correct as written. The `buggy` line is the stale-key bug on purpose.

**Edge cases:**
- k = 0: 0 (the code returns early; without it the loop would try to remove from an empty window).
- Empty string: 0.
- k at least the alphabet size: the whole string.
- One repeated letter, k = 1: n.

**Follow-ups:**
- Exactly k distinct, length only? The same answer, as long as the string has at least k distinct letters: if the longest at-most-k window had fewer than k distinct and was not the whole string, you could extend it by one character and stay within k, which contradicts "longest". With fewer than k distinct letters overall, no such substring exists.
- Counting substrings with exactly k distinct: see Q33.
- Unicode? Counter keys are code points; nothing changes. A 26-slot array would.

**Common mistakes:**
- Counting keys that have value 0.
- Using `if len(count) > k` once instead of a `while`.
- Forgetting `k = 0`.
- Off-by-one in the length: `right - left + 1`.

### Q26 ⭐⭐ 🟡 Subarrays with product less than k. Given positive integers `nums` (len <= 3*10^4) and an integer k >= 0, count contiguous non-empty subarrays whose product is strictly less than k. Slide a window with a running product and add `right - left + 1` for each right end; explain why that increment counts exactly the subarrays ending at `right`, and handle k <= 1. Example: nums=[10,5,2,6], k=100 -> 8; nums=[1,2,3], k=0 -> 0.
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports

**Pattern:** Variable window with a monotone predicate. All values are positive, so the product only grows when the window grows. That is what makes the window valid.

**Say this first (1 line):** "Positive numbers, so for each right end the valid starts form one contiguous range ending at `right`. I keep a running product, shrink while it is at least k, and add the window length. O(n)."

**Brute force:** For each start, multiply forward and count while the product is below k. O(n^2) time, O(1) space.

**Optimal:**
- If `k <= 1`, return 0. Every product is at least 1, and nothing is strictly below 1.
- `prod *= nums[right]`. While `prod >= k`, `prod //= nums[left]`, `left += 1`.
- Then add `right - left + 1`.
- Why that count: every subarray that ends at `right` and starts anywhere in `[left, right]` has a product below k, because shrinking a window of positive numbers can only lower the product (each factor is at least 1). The start `left - 1` was already rejected. So there are exactly `right - left + 1` of them. Each subarray is counted once, at its own right end.
- The integer division is exact because `prod` is a product that contains `nums[left]`.

**Complexity:** Time O(n): both pointers only move forward. Space O(1). Python ints do not overflow, but the product stays below k times one element, so it stays small anyway.

**Dry run:** `[10,5,2,6]`, `k=100`
| right | prod after shrink | left | add | total |
|---|---|---|---|---|
| 0 | 10 | 0 | 1 | 1 |
| 1 | 50 | 0 | 2 | 3 |
| 2 | 100 >= 100, so divide by 10 -> 10 | 1 | 2 | 5 |
| 3 | 60 | 1 | 3 | 8 |
Answer 8: [10], [5], [2], [6], [10,5], [5,2], [2,6], [5,2,6].

**Code:**
```python
import random


def prod_brute(nums, k):
    total = 0
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            if p < k:
                total += 1
    return total


def prod_window(nums, k):
    if k <= 1:  # every product is >= 1, so none is < 1
        return 0
    left = total = 0
    prod = 1
    for right, x in enumerate(nums):
        prod *= x
        while prod >= k:
            prod //= nums[left]  # exact: prod is a multiple of nums[left]
            left += 1
        total += right - left + 1  # subarrays ending at right
    return total


print("[10,5,2,6], 100:", prod_window([10, 5, 2, 6], 100), "(expected 8)")
print("[1,2,3], 0:", prod_window([1, 2, 3], 0), "(expected 0)")

random.seed(26)
for _ in range(1000):
    n = random.randint(0, 9)
    nums = [random.randint(1, 6) for _ in range(n)]
    k = random.randint(0, 60)
    assert prod_window(nums, k) == prod_brute(nums, k), (nums, k)
print("cross-check: 1000 seeded cases agree")

assert prod_window([], 10) == 0
assert prod_window([1], 1) == 0
assert prod_window([1], 2) == 1
assert prod_window([1, 1, 1], 2) == 6  # all 3+2+1 subarrays have product 1
assert prod_window([5], 5) == 0  # strictly less
assert prod_window([100], 100) == 0
assert prod_window([10 ** 6, 1], 10 ** 6) == 1  # only [1] qualifies
n = 3 * 10 ** 4
assert prod_window([1] * n, 2) == n * (n + 1) // 2
# big k: Python ints never overflow, the running product just stays below k
assert prod_window([2] * 60, 2 ** 70) == 60 * 61 // 2
print("edge asserts passed")
```

**Output (my run):**
```text
[10,5,2,6], 100: 8 (expected 8)
[1,2,3], 0: 0 (expected 0)
cross-check: 1000 seeded cases agree
edge asserts passed
```

Both prompt examples are correct as written.

**Edge cases:**
- k = 0 or 1: 0.
- Strictly less: an element equal to k is not counted.
- All ones with k >= 2: every subarray, n(n+1)/2.
- If the shrink empties the window (a single element at least k), `left` becomes `right + 1` and the add is 0. With `prod = 1` after dividing, this is consistent.

**Follow-ups:**
- Zeros or negatives allowed? The monotone property is gone, the window fails. Zeros need a split at zeros; negatives need a different idea (sign tracking, not a window).
- Use logs to avoid big products? Floating point risks wrong ties. With Python ints just multiply.
- Return the subarrays? Output size can be O(n^2), so say that.

**Common mistakes:**
- Not handling `k <= 1`; the `while` loop then divides until `left` passes `right` and `nums[left]` goes out of range.
- Using `>` instead of `>=` in the shrink test (strictly less means shrink on equal).
- Adding 1 per step instead of `right - left + 1`.
- Using float division `/` and getting a float product.

### Q27 ⭐⭐ 🟡 3Sum closest. Given integers `nums` (3 <= len <= 500) and an integer `target`, return the sum of three distinct-position elements that is closest to the target (a unique answer is guaranteed). Sort, fix one index and run opposite-ends pointers, moving by whether the current sum is below or above the target and exiting early on an exact hit. Example: nums=[-1,2,1,-4], target=1 -> 2; nums=[0,0,0], target=1 -> 0.
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports

**Pattern:** Sort, fix one index, opposite-ends two pointers on the rest (the 3Sum idea, Q8), but track the closest sum instead of equality.

**Say this first (1 line):** "Sort, fix i, move lo and hi by comparing the sum to the target, remember the closest sum, return at once on an exact hit. O(n^2)."

**Brute force:** All triples of distinct positions, keep the sum closest to the target. O(n^3) time, O(1) space. With n = 500 that is about 2 * 10^7 triples, slow in Python.

**Optimal:**
- Sort. For each `i`, set `lo = i+1`, `hi = n-1`.
- `s = a[i] + a[lo] + a[hi]`. If `abs(s - target)` beats the best, update.
- If `s == target`, return. If `s < target`, `lo += 1` (a bigger sum is the only way to get closer from below). Otherwise `hi -= 1`.
- Why moving is safe: with `i` fixed and the list sorted, if `s < target` then pairing `a[lo]` with any `hi'` below `hi` gives a sum no larger than `s`, so it is no closer. So `a[lo]` is done and can be dropped.
- Skipping repeated first values is only a speed-up; it does not change the answer.

**Complexity:** Time O(n^2) after the O(n log n) sort: n values of `i`, each with a linear two-pointer pass. Space O(n) for the sorted copy in my code (O(1) extra if you sort in place; Python's sort uses up to O(n) temporary space).

**Dry run:** `[-1,2,1,-4]`, `target=1`; sorted `[-4,-1,1,2]`; start best = -4.
| i | lo, hi | sum | distance | action |
|---|---|---|---|---|
| -4 | -1, 2 | -3 | 4 | best=-3, sum<1 so lo up |
| -4 | 1, 2 | -1 | 2 | best=-1, lo up, pointers meet |
| -1 | 1, 2 | 2 | 1 | best=2, sum>1 so hi down, meet |
Answer 2.

**Code:**
```python
import random
from itertools import combinations


def closest_brute(nums, target):
    best = None
    for a, b, c in combinations(nums, 3):  # distinct positions
        s = a + b + c
        if best is None or abs(s - target) < abs(best - target):
            best = s
    return best


def closest_two_pointers(nums, target):
    a = sorted(nums)
    n = len(a)
    best = a[0] + a[1] + a[2]
    for i in range(n - 2):
        if i and a[i] == a[i - 1]:
            continue  # same first value gives the same triples
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if abs(s - target) < abs(best - target):
                best = s
            if s == target:
                return s
            if s < target:
                lo += 1
            else:
                hi -= 1
    return best


print("[-1,2,1,-4], 1:", closest_two_pointers([-1, 2, 1, -4], 1), "(expected 2)")
print("[0,0,0], 1:", closest_two_pointers([0, 0, 0], 1), "(expected 0)")

random.seed(27)
for _ in range(1000):
    n = random.randint(3, 8)
    nums = [random.randint(-6, 6) for _ in range(n)]
    t = random.randint(-15, 15)
    got, want = closest_two_pointers(nums, t), closest_brute(nums, t)
    # ties (equally close sums) are possible in random data, so compare distance
    assert abs(got - t) == abs(want - t), (nums, t, got, want)
print("cross-check: 1000 seeded cases agree (on distance to target)")

assert closest_two_pointers([1, 1, 1], 5) == 3
assert closest_two_pointers([1, 1, 1, 0], -100) == 2
assert closest_two_pointers([-5, -4, -3], 0) == -12
assert closest_two_pointers([1, 2, 3, 4], 6) == 6  # exact hit
assert closest_two_pointers([0, 0, 0], 0) == 0
assert closest_two_pointers([1000, -1000, 0, 5], 7) == 5
nums = [random.randint(-1000, 1000) for _ in range(500)]
r = closest_two_pointers(nums, 123)
assert isinstance(r, int)
print("edge asserts passed")
```

**Output (my run):**
```text
[-1,2,1,-4], 1: 2 (expected 2)
[0,0,0], 1: 0 (expected 0)
cross-check: 1000 seeded cases agree (on distance to target)
edge asserts passed
```

Both prompt examples are correct as written. In the cross-check I compare the distance to the target, not the sum itself, because random data can have two sums equally close; the problem promises a unique answer, random data does not.

**Edge cases:**
- Exactly 3 numbers: the only triple.
- Exact hit: return early.
- Target far above or below everything: the max or min triple sum.
- Duplicates and negatives: handled by sorting.

**Follow-ups:**
- What if two sums tie? Ask which to return; the code keeps the first found.
- Closest to target but not above (largest sum at most target)? Update only when `s <= target`.
- Faster than O(n^2)? Not in general; 3Sum-type problems are believed to need about n^2.

**Common mistakes:**
- Comparing signed difference instead of `abs`.
- Initialising `best` to 0 (can be wrong) rather than the first triple.
- Reusing the same position twice (`lo` must start at `i+1`).
- Forgetting to sort.

### Q28 ⭐⭐ 🟡 Maximum points from cards at the two ends. `cardPoints` is a list of non-negative integers (len <= 10^5) and you take exactly k cards, each time from the left end or the right end. Return the maximum total. Rewrite it as 'minimise the sum of a fixed window of len - k that stays in the middle', or equivalently slide a prefix/suffix split; state both views and the edge case k = len. Example: cardPoints=[1,2,3,4,5,6,1], k=3 -> 12; cardPoints=[2,2,2], k=2 -> 4; cardPoints=[9,7,7,9,7,7,9], k=7 -> 55.
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Company-tagged prep pages (a Jointaro interview-question page files this problem under an Uber path and Educative and NeetCode solution pages cover it; snippets only, not opened; company tags on such pages are unverified)

**Pattern:** Fixed-size window in disguise. Taking k cards from the two ends means leaving one contiguous block of n - k cards in the middle.

**Say this first (1 line):** "I take total minus the smallest sum of any middle block of length n-k. One fixed window, O(n)."

**Brute force:** For every split (i from the left, k-i from the right), sum both parts. O(k^2) if you re-sum each time, O(k) with running sums.

**Optimal (two equivalent views):**
- View 1, the middle window: let `m = n - k`. Slide a window of size m over the list with add-one-drop-one, keep the minimum sum, answer is `total - min`. When `k = n`, `m = 0`, the window sum is 0 and the answer is the total.
- View 2, prefix/suffix split: start with the first k cards. Then trade one card at a time: remove `cards[k-i]` from the left group and add `cards[-i]` from the right end, for `i = 1..k`. Keep the best.
- Why it works: any choice "i from the left, k-i from the right" leaves exactly the block from index i to n-k+i-1, which is a window of length n-k.

**Complexity:** Time O(n) for view 1, O(k) for view 2. Space O(1). Both beat re-summing.

**Dry run:** `[1,2,3,4,5,6,1]`, `k=3`, so `m=4`, total 22.
| window | sum |
|---|---|
| [1,2,3,4] | 10 |
| [2,3,4,5] | 14 |
| [3,4,5,6] | 18 |
| [4,5,6,1] | 16 |
Min is 10, so the answer is 22 - 10 = 12.
View 2: start with 1+2+3 = 6. Trade the 3 for the last card 1 -> 4. Trade the 2 for the next card 6 -> 8. Trade the 1 for the next card 5 -> 12. Best 12 (the cards 5, 6, 1 from the right end).

**Code:**
```python
import random


def cards_brute(cards, k):
    # i cards from the left, k-i from the right
    best = 0
    for i in range(k + 1):
        left = sum(cards[:i])
        right = sum(cards[len(cards) - (k - i):]) if k - i else 0
        best = max(best, left + right)
    return best


def cards_window(cards, k):
    # view 1: the cards left behind form one window of size n-k; minimise it
    n = len(cards)
    m = n - k
    window = sum(cards[:m])
    low = window
    for r in range(m, n):
        window += cards[r] - cards[r - m]
        low = min(low, window)
    return sum(cards) - low


def cards_split(cards, k):
    # view 2: start with k from the left, then trade one left card for one right card
    cur = sum(cards[:k])
    best = cur
    for i in range(1, k + 1):
        cur += cards[-i] - cards[k - i]
        best = max(best, cur)
    return best


print("[1,2,3,4,5,6,1], 3:", cards_window([1, 2, 3, 4, 5, 6, 1], 3), cards_split([1, 2, 3, 4, 5, 6, 1], 3), "(expected 12)")
print("[2,2,2], 2:", cards_window([2, 2, 2], 2), cards_split([2, 2, 2], 2), "(expected 4)")
print("[9,7,7,9,7,7,9], 7:", cards_window([9, 7, 7, 9, 7, 7, 9], 7), cards_split([9, 7, 7, 9, 7, 7, 9], 7), "(expected 55)")

random.seed(28)
for _ in range(1000):
    n = random.randint(1, 10)
    cards = [random.randint(0, 9) for _ in range(n)]
    k = random.randint(1, n)
    b = cards_brute(cards, k)
    assert cards_window(cards, k) == b == cards_split(cards, k), (cards, k)
print("cross-check: 1000 seeded cases agree")

assert cards_window([5], 1) == 5
assert cards_split([5], 1) == 5
assert cards_window([1, 2, 3], 3) == 6  # k = n: empty middle window, take everything
assert cards_split([1, 2, 3], 3) == 6
assert cards_window([1, 2, 3], 1) == 3
assert cards_window([0, 0, 0], 2) == 0
big = [random.randint(0, 10 ** 4) for _ in range(10 ** 5)]
assert cards_window(big, 10 ** 5) == sum(big)
assert cards_window(big, 5 * 10 ** 4) == cards_split(big, 5 * 10 ** 4)
print("edge asserts passed")
```

**Output (my run):**
```text
[1,2,3,4,5,6,1], 3: 12 12 (expected 12)
[2,2,2], 2: 4 4 (expected 4)
[9,7,7,9,7,7,9], 7: 55 55 (expected 55)
cross-check: 1000 seeded cases agree
edge asserts passed
```

All three prompt examples are correct as written.

**Edge cases:**
- k = n: take everything; the middle window is empty (sum 0).
- n = 1: that card.
- All zeros: 0.
- Large n: both views are linear.

**Follow-ups:**
- Why not greedy "take the larger end each time"? Counter example: `[1,100,1,2]`, k=2. Greedy takes 2 then 1 = 3, but 1 + 100 = 101 from the left is better. Use the window.
- Cards may be negative? The window view still works (min of a fixed-length window); the answer logic is unchanged because you must take exactly k.
- Need the actual cards? Record the best split i.

**Common mistakes:**
- Greedy by the bigger end.
- Window size k instead of n - k.
- Crashing on k = n (an empty window): guard it, or let the sum of an empty slice be 0 as the code does.
- Off-by-one in the drop index (`r - m`).

### Q29 ⭐⭐ 🟡 Longest subarray of 1s after deleting one element. Given a 0/1 list `nums` (len <= 10^5), you must delete exactly one element; return the length of the longest non-empty run of 1s left in the result (0 if there are no 1s possible, e.g. a single element). Use a window with at most one zero and subtract one for the forced deletion. Example: [1,1,0,1] -> 3; [0,1,1,1,0,1,1,0,1] -> 5; [1,1,1] -> 2 (you still must delete one).
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports

**Pattern:** Variable window with at most one zero. The forced deletion is a one-off subtraction at the end.

**Say this first (1 line):** "Longest window with at most one zero, minus one for the element I must delete. That also covers an all-ones list. O(n)."

**Brute force:** Try deleting each index, then scan for the longest run of 1s in what is left. O(n^2) time, O(n) space for the copies.

**Optimal:**
- Keep `[left, right]` with at most one zero (shrink while `zeros > 1`).
- Candidate length is `right - left`, which is the window length minus one.
- Why minus one: if the window has a zero, deleting it joins the ones around it. If the window has no zero, you still must delete something, and deleting one of its ones loses one. Either way the length of 1s left is window length - 1.
- Shortcut: `right - left` is `(right - left + 1) - 1`.

**Complexity:** Time O(n): each index enters and leaves once. Space O(1).

**Dry run:** `[1,1,0,1]`
| right | window | zeros | right-left |
|---|---|---|---|
| 0 | [0..0] | 0 | 0 |
| 1 | [0..1] | 0 | 1 |
| 2 | [0..2] | 1 | 2 |
| 3 | [0..3] | 1 | 3 |
Answer 3 (delete the 0, run of three 1s).

**Code:**
```python
import random


def del_brute(nums):
    best = 0
    for d in range(len(nums)):
        rest = nums[:d] + nums[d + 1:]
        run = 0
        for x in rest:
            run = run + 1 if x == 1 else 0
            best = max(best, run)
    return best


def del_window(nums):
    left = zeros = best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > 1:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left)  # window length minus the one forced deletion
    return best


print("[1,1,0,1]:", del_window([1, 1, 0, 1]), "(expected 3)")
print("[0,1,1,1,0,1,1,0,1]:", del_window([0, 1, 1, 1, 0, 1, 1, 0, 1]), "(expected 5)")
print("[1,1,1]:", del_window([1, 1, 1]), "(expected 2)")

random.seed(29)
for _ in range(1000):
    n = random.randint(1, 12)
    nums = [random.randint(0, 1) for _ in range(n)]
    assert del_window(nums) == del_brute(nums), nums
print("cross-check: 1000 seeded cases agree")

assert del_window([0]) == 0
assert del_window([1]) == 0  # delete the only element, nothing left
assert del_window([0, 0, 0]) == 0
assert del_window([1, 0]) == 1
assert del_window([1, 0, 1]) == 2
assert del_window([1, 1, 1, 1]) == 3
assert del_window([1] * 10 ** 5) == 10 ** 5 - 1
assert del_window([0] * 10 ** 5) == 0
print("edge asserts passed")
```

**Output (my run):**
```text
[1,1,0,1]: 3 (expected 3)
[0,1,1,1,0,1,1,0,1]: 5 (expected 5)
[1,1,1]: 2 (expected 2)
cross-check: 1000 seeded cases agree
edge asserts passed
```

All three prompt examples are correct as written.

**Edge cases:**
- All ones: n - 1 (the forced delete).
- Single element: 0, whatever its value.
- All zeros: 0.
- Two elements `[1, 0]`: 1.
- n = 10^5: linear.

**Follow-ups:**
- Delete at most k elements instead? Keep a window with at most k zeros and count the ones left: `window length - zeros`, but you must still delete exactly k if the problem insists.
- Need the index to delete? Record the zero position in the best window.
- Alternative: count ones before and after each zero with two passes (prefix/suffix of consecutive ones).

**Common mistakes:**
- Forgetting the forced deletion on an all-ones list (returning n).
- Using `right - left + 1`.
- Treating "no zero in the window" as free to keep all.
- Shrinking with `if` rather than `while`.

### Q30 ⭐⭐ 🟡 Count nice subarrays. Given integers `nums` (len <= 5*10^4) and k >= 1, count contiguous subarrays containing exactly k odd numbers. Show the 'at most k minus at most k-1' decomposition with a helper that slides one window, explain why exact-k cannot be done with a single shrink rule, and name the prefix-count alternative (see Part 1 Q13, Subarray sum equals k). Example: nums=[1,1,2,1,1], k=3 -> 2; nums=[2,4,6], k=1 -> 0; nums=[2,2,2,1,2,2,1,2,2,2], k=2 -> 16.
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Company-tagged prep pages (a Jointaro interview-question page files this problem under an Uber path and Educative and NeetCode solution pages cover it; snippets only, not opened; company tags on such pages are unverified)

**Pattern:** Counting with "at most" minus "at most one less". The exact-k count is the difference of two at-most counts, and "at most" has a clean window.

**Say this first (1 line):** "exactly(k) = at_most(k) - at_most(k-1). The helper is one sliding window that adds `right - left + 1` per right end. O(n)."

**Brute force:** For each start, extend and count how many ends have exactly k odd numbers. O(n^2) time, O(1) space.

**Optimal:**
- `at_most(k)`: slide a window; shrink while odds > k; add `right - left + 1` (the number of subarrays ending at `right` with at most k odds).
- Then `at_most(k) - at_most(k-1)` removes the ones with fewer than k odds.
- Why exact-k has no single shrink rule: when the window has exactly k odds you cannot tell whether to shrink (to look for more starts) or extend. Valid starts for one right end form a range, not a prefix, so one pointer cannot track both ends of it. At most k is monotone: shrinking keeps it valid.
- Alternative: prefix counts. `odds` so far; add `seen[odds - k]` to the total; this is Part 1 Q13 (Subarray sum equals k) with each element mapped to its parity. It is O(n) time and O(n) space, and it also works when values change meaning (negatives).

**Complexity:** Time O(n) (two linear window passes). Space O(1) for the window; O(n) for the prefix-count dict.

**Dry run:** `nums=[1,1,2,1,1]`, `k=3`
- Total subarrays: 15. The array has 4 odds.
- `at_most(3)`: everything except the whole array (4 odds) = 14.
- `at_most(2)`: remove those with 3 or more odds: [1,1,2,1], [1,2,1,1], [1,1,2,1,1] = 3, so 12.
- Answer 14 - 12 = 2: the two blocks [1,1,2,1] and [1,2,1,1].

**Code:**
```python
import random
from collections import Counter


def nice_brute(nums, k):
    total = 0
    for i in range(len(nums)):
        odds = 0
        for j in range(i, len(nums)):
            odds += nums[j] & 1
            total += odds == k
    return total


def at_most(nums, k):
    # number of subarrays with at most k odd numbers; one shrink rule works here
    if k < 0:
        return 0
    left = odds = total = 0
    for right, x in enumerate(nums):
        odds += x & 1
        while odds > k:
            odds -= nums[left] & 1
            left += 1
        total += right - left + 1
    return total


def nice_window(nums, k):
    return at_most(nums, k) - at_most(nums, k - 1)


def nice_prefix(nums, k):
    # alternative: count prefix odd-counts (the Part 1 'subarray sum equals k' idea)
    seen = Counter({0: 1})
    odds = total = 0
    for x in nums:
        odds += x & 1
        total += seen[odds - k]
        seen[odds] += 1
    return total


print("[1,1,2,1,1], 3:", nice_window([1, 1, 2, 1, 1], 3), "(expected 2)")
print("[2,4,6], 1:", nice_window([2, 4, 6], 1), "(expected 0)")
t = [2, 2, 2, 1, 2, 2, 1, 2, 2, 2]
print("[2,2,2,1,2,2,1,2,2,2], 2:", nice_window(t, 2), nice_prefix(t, 2), "(expected 16)")

random.seed(30)
for _ in range(1000):
    n = random.randint(0, 12)
    nums = [random.randint(-5, 5) for _ in range(n)]  # negatives: x & 1 still gives parity
    k = random.randint(1, 4)
    b = nice_brute(nums, k)
    assert nice_window(nums, k) == b == nice_prefix(nums, k), (nums, k)
print("cross-check: 1000 seeded cases agree")

assert nice_window([], 1) == 0
assert nice_window([1], 1) == 1
assert nice_window([2], 1) == 0
assert nice_window([1, 1, 1], 1) == 3
assert nice_window([1, 1, 1], 4) == 0  # k above the number of odds
assert nice_window([2, 2, 2], 1) == 0
assert nice_window([1, 2, 3, 4, 5], 2) == nice_brute([1, 2, 3, 4, 5], 2)
big = [random.randint(1, 100) for _ in range(5 * 10 ** 4)]
assert nice_window(big, 3) == nice_prefix(big, 3)
print("edge asserts passed")
```

**Output (my run):**
```text
[1,1,2,1,1], 3: 2 (expected 2)
[2,4,6], 1: 0 (expected 0)
[2,2,2,1,2,2,1,2,2,2], 2: 16 16 (expected 16)
cross-check: 1000 seeded cases agree
edge asserts passed
```

All three prompt examples are correct as written (the third, 16, was also confirmed by both the window and the prefix versions).

**Edge cases:**
- k above the number of odds: 0.
- No odds at all: 0.
- `at_most(-1)` must return 0 (the guard in the helper), for k = 0 callers.
- Negative numbers: `x & 1` gives the parity in Python for negatives (`-3 & 1 == 1`). `x % 2` also works.

**Follow-ups:**
- Binary subarrays with sum goal? Same problem with 0/1 values.
- Why is the prefix version also correct for exact-k? Each subarray is a pair of prefix positions whose odd counts differ by k.
- Which is better? Window uses O(1) space; the prefix map is shorter to write and generalises.

**Common mistakes:**
- Trying to count exact-k with one `while odds > k` window.
- Forgetting the `k < 0` guard in the helper.
- Checking `x % 2 == 1`, which misses negative odd numbers in other languages (not in Python, but say it).
- Adding 1 per step instead of `right - left + 1`.

### Q31 ⭐⭐ 🟡 Count substrings containing a, b and c. Given a string `s` over the letters a, b, c only (len <= 5*10^4), count substrings that contain at least one of each. For each right end, find how many left starts still work (the leftmost valid start moves only forward) and add that count, giving O(n). Example: 'abcabc' -> 10; 'aaacb' -> 3; 'abc' -> 1.
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports

**Pattern:** Counting with a "once valid, stays valid when you extend" property. For each right end, the valid starts are a prefix of the positions, `0..m`, so you add `m + 1`.

**Say this first (1 line):** "For each right end, the valid starts are everything up to the minimum of the last positions of a, b and c. Add `min(last) + 1`. O(n), O(1)."

**Brute force:** Check every substring with a set. O(n^2) substrings, and building each set costs O(length), so O(n^3) in total. Fine for tiny input only.

**Optimal (last-seen version):**
- Keep `last[a]`, `last[b]`, `last[c]` (start at -1).
- At index `i`, set `last[s[i]] = i`.
- A substring `[start, i]` contains all three iff `start <= min(last)`. So there are `min(last) + 1` valid starts (and 0 while any letter is still missing, since `-1 + 1 = 0`).
- Sum these over `i`.
- Why O(n) and why "left moves only forward": `min(last)` never decreases, since every `last` only grows.

**Optimal (window version, same idea):** when the window `[left, right]` has all three letters, every longer window with the same left (ending at `right`, `right+1`, ..., `n-1`) is valid too, so add `n - right`, then drop `s[left]` and advance `left`. Same answer, counted from the left side.

**Complexity:** Time O(n). Space O(1) (three counters).

**Dry run:** `'abcabc'` with the last-seen version
| i | char | last (a,b,c) | min+1 | running total |
|---|---|---|---|---|
| 0 | a | 0,-1,-1 | 0 | 0 |
| 1 | b | 0,1,-1 | 0 | 0 |
| 2 | c | 0,1,2 | 1 | 1 |
| 3 | a | 3,1,2 | 2 | 3 |
| 4 | b | 3,4,2 | 3 | 6 |
| 5 | c | 3,4,5 | 4 | 10 |
Answer 10.

**Code:**
```python
import random


def abc_brute(s):
    total = 0
    for i in range(len(s)):
        for j in range(i + 3, len(s) + 1):
            if {"a", "b", "c"} <= set(s[i:j]):
                total += 1
    return total


def abc_window(s):
    # for each right end, count the starts that are still valid; left only moves forward
    cnt = {"a": 0, "b": 0, "c": 0}
    left = total = 0
    n = len(s)
    for right, ch in enumerate(s):
        cnt[ch] += 1
        while cnt["a"] and cnt["b"] and cnt["c"]:
            # window [left, right] is valid, and so is every longer window to the right
            total += n - right
            cnt[s[left]] -= 1
            left += 1
    return total


def abc_lastseen(s):
    # simplest: starts 0..min(last a, last b, last c) all work for this right end
    last = {"a": -1, "b": -1, "c": -1}
    total = 0
    for i, ch in enumerate(s):
        last[ch] = i
        total += min(last.values()) + 1  # -1 + 1 = 0 until all three have appeared
    return total


for s, want in (("abcabc", 10), ("aaacb", 3), ("abc", 1)):
    print(repr(s), abc_window(s), abc_lastseen(s), f"(expected {want})")

random.seed(31)
for _ in range(1000):
    n = random.randint(0, 12)
    s = "".join(random.choice("abc") for _ in range(n))
    b = abc_brute(s)
    assert abc_window(s) == b == abc_lastseen(s), s
print("cross-check: 1000 seeded cases agree")

assert abc_window("") == 0 == abc_lastseen("")
assert abc_window("a") == 0
assert abc_window("ab") == 0
assert abc_window("aaaa") == 0
assert abc_window("abc") == 1
assert abc_window("cba") == 1
big = "".join(random.choice("abc") for _ in range(5 * 10 ** 4))
assert abc_window(big) == abc_lastseen(big)
n = 3 * 10 ** 4
assert abc_window("abc" * (n // 3)) == abc_lastseen("abc" * (n // 3))
print("edge asserts passed")
```

**Output (my run):**
```text
'abcabc' 10 10 (expected 10)
'aaacb' 3 3 (expected 3)
'abc' 1 1 (expected 1)
cross-check: 1000 seeded cases agree
edge asserts passed
```

All three prompt examples are correct as written.

**Edge cases:**
- Fewer than 3 characters: 0.
- A missing letter anywhere: only counts after it appears.
- The same letter repeated: 0.
- n = 5 * 10^4: the answer is about n^2 / 2, about 1.25 * 10^9, a plain Python int.

**Follow-ups:**
- Generalise to k letters? Keep a dict of last positions and take the min once all k have appeared.
- Why not "at most" minus "at most"? You could, but "at least one of each" has the direct monotone form, so the last-seen trick is shorter.
- Which version is easier to explain? The window one matches the pattern; the last-seen one has the least code.

**Common mistakes:**
- Adding 1 when the window becomes valid, instead of the count of all valid starts (or ends).
- Resetting `left` to 0 at every step (O(n^2)).
- Counting only substrings that start at the window's left edge.
- Starting `last` at 0 rather than -1, which counts a letter as seen.

### Q32 ⭐⭐ 🟡 4Sum. Given integers `nums` (len <= 200, values up to 10^9 in magnitude) and a `target`, return all unique quadruplets of values (each as a sorted list, the whole answer sorted) that sum to the target. Sort, fix two indices and run opposite-ends pointers for the rest, skipping duplicates at every level; give the O(n^3) bound and show how to generalise to k-sum with recursion. Example: nums=[1,0,-1,0,-2,2], target=0 -> [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]; nums=[2,2,2,2,2], target=8 -> [[2,2,2,2]].
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports

**Pattern:** Sort, fix the first two values (or recurse), then opposite-ends two pointers for the last two. It is 3Sum (Q8) with one more layer; k-sum generalises it.

**Say this first (1 line):** "Sort, two nested loops with duplicate skips, then two pointers for the last pair. O(n^3). For general k, recurse down to the k = 2 case."

**Brute force:** All 4-element combinations, sort each, put in a set. O(n^4) time, up to O(n^4) space for the set if many match. At n = 200 that is about 6.5 * 10^7 combinations, too slow here.

**Optimal:**
- Sort once. Loop `i`, skipping `a[i] == a[i-1]` (after the first). Loop `j > i`, same skip.
- For the rest, `lo = j+1`, `hi = n-1`: if the sum is below the target, `lo += 1`; above, `hi -= 1`; equal, record it, move both, and skip repeated values on both sides.
- Duplicates are skipped at all four positions, so each unique quadruplet appears once. Because the array is sorted and the loops go in increasing order, the answer is already in sorted order, which is what the prompt asks for.
- k-sum recursion: `k_sum(a, start, k, target)`; for k = 2 do two pointers; otherwise loop `i` from `start`, skip duplicates, recurse with `k-1` and `target - a[i]`. Pruning: break if the smallest k values from `i` already exceed the target; skip if `a[i]` plus the largest k-1 values is below the target.

**Complexity:** Time O(n^3) for k = 4 (two loops, one linear pass); O(n^(k-1)) in general. Space O(1) extra besides the sort and the answer (recursion depth k).

**Dry run:** `[1,0,-1,0,-2,2]`, target 0; sorted `[-2,-1,0,0,1,2]`
- i = -2, j = -1: need a pair summing to 3: (1, 2) -> [-2,-1,1,2].
- i = -2, j = 0 (first 0): need 2: (0, 2) -> [-2,0,0,2]. The second 0 as `j` is skipped as a duplicate.
- i = -1, j = 0: need 1: lo=0, hi=2 gives 2 (too big), hi=1 gives 1 -> [-1,0,0,1].
- The later `i` values have no room or no match.

**Code:**
```python
import random
from itertools import combinations


def four_brute(nums, target):
    res = set()
    for q in combinations(nums, 4):
        if sum(q) == target:
            res.add(tuple(sorted(q)))
    return sorted(list(t) for t in res)


def k_sum(a, start, k, target):
    # a is sorted; returns unique k-tuples from a[start:] summing to target
    n = len(a)
    res = []
    if k == 2:
        lo, hi = start, n - 1
        while lo < hi:
            s = a[lo] + a[hi]
            if s < target:
                lo += 1
            elif s > target:
                hi -= 1
            else:
                res.append([a[lo], a[hi]])
                lo += 1
                hi -= 1
                while lo < hi and a[lo] == a[lo - 1]:
                    lo += 1
                while lo < hi and a[hi] == a[hi + 1]:
                    hi -= 1
        return res
    for i in range(start, n - k + 1):
        if i > start and a[i] == a[i - 1]:
            continue
        # prune: smallest possible sum too big, or largest possible too small
        if sum(a[i:i + k]) > target:
            break
        if a[i] + sum(a[n - k + 1:]) < target:
            continue
        for rest in k_sum(a, i + 1, k - 1, target - a[i]):
            res.append([a[i]] + rest)
    return res


def four_sum(nums, target):
    return k_sum(sorted(nums), 0, 4, target)


def four_sum_loops(nums, target):
    # the explicit two-loop version most people write on a whiteboard
    a = sorted(nums)
    n = len(a)
    res = []
    for i in range(n - 3):
        if i and a[i] == a[i - 1]:
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and a[j] == a[j - 1]:
                continue
            lo, hi = j + 1, n - 1
            while lo < hi:
                s = a[i] + a[j] + a[lo] + a[hi]
                if s < target:
                    lo += 1
                elif s > target:
                    hi -= 1
                else:
                    res.append([a[i], a[j], a[lo], a[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and a[lo] == a[lo - 1]:
                        lo += 1
                    while lo < hi and a[hi] == a[hi + 1]:
                        hi -= 1
    return res


e1 = four_sum([1, 0, -1, 0, -2, 2], 0)
e2 = four_sum([2, 2, 2, 2, 2], 8)
print("example 1:", e1)
print("example 2:", e2)
assert e1 == [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
assert e2 == [[2, 2, 2, 2]]
print("3-sum via k_sum:", k_sum(sorted([-1, 0, 1, 2, -1, -4]), 0, 3, 0))

random.seed(32)
for _ in range(1000):
    n = random.randint(0, 9)
    nums = [random.randint(-4, 4) for _ in range(n)]
    t = random.randint(-8, 8)
    b = four_brute(nums, t)
    assert four_sum(nums, t) == b, (nums, t)
    assert four_sum_loops(nums, t) == b, (nums, t)
print("cross-check: 1000 seeded cases agree (k_sum, explicit loops, brute)")

assert four_sum([], 0) == []
assert four_sum([1, 2, 3], 6) == []
assert four_sum([0, 0, 0, 0], 0) == [[0, 0, 0, 0]]
assert four_sum([0] * 200, 0) == [[0, 0, 0, 0]]
big = 10 ** 9
assert four_sum([big, big, big, big], 4 * big) == [[big, big, big, big]]
assert four_sum([-big, -big, big, big], 0) == [[-big, -big, big, big]]
assert four_sum([big, big, big, big], 0) == []
nums = [random.randint(-10 ** 9, 10 ** 9) for _ in range(200)]
r = four_sum(nums, 0)
assert r == sorted(r)
print("edge asserts passed")
```

**Output (my run):**
```text
example 1: [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
example 2: [[2, 2, 2, 2]]
3-sum via k_sum: [[-1, -1, 2], [-1, 0, 1]]
cross-check: 1000 seeded cases agree (k_sum, explicit loops, brute)
edge asserts passed
```

Both prompt examples are correct as written. Values up to 10^9 in magnitude cause no overflow in Python (in C++ or Java you would cast to a 64-bit type before adding).

**Edge cases:**
- Fewer than 4 numbers: empty.
- All equal: one quadruplet if `4 * v == target`.
- Large magnitudes: Python ints; mention the 64-bit cast in other languages.
- Negative target.

**Follow-ups:**
- Count of quadruplets, with no uniqueness? The hash-map on pair sums approach is O(n^2) (four separate lists, that is the "4Sum II" style problem).
- Why the pruning? It cuts many branches, but worst-case stays O(n^3).
- Can you do 4Sum without sorting? Use a hash map of pair sums, but then deduplicating the answer is messier.

**Common mistakes:**
- Skipping duplicates with `a[j] == a[j-1]` when `j == i+1` (that wrongly skips valid reuse of a value used at `i`). The guard is `j > i + 1`.
- Not moving both pointers after a hit.
- Forgetting the inner skips after a hit, so duplicate triples appear.
- Using a set of tuples as a crutch and then claiming O(n^3) without noting the hashing.

### Q33 ⭐⭐ 🔴 Subarrays with exactly k distinct integers. Given positive integers `nums` (len <= 2*10^4) and k, count contiguous subarrays having exactly k distinct values. Implement `at_most(k)` with one Counter window that adds `right - left + 1` per right end, then return `at_most(k) - at_most(k-1)`; explain why a single window cannot count 'exactly' directly and how you would keep memory O(k). Example: nums=[1,2,1,2,3], k=2 -> 7; nums=[1,2,1,3,4], k=3 -> 3.
**Asked at:** Company-tagged prep pages (a Jointaro interview-question page files this problem under an Uber path and Educative and NeetCode solution pages cover it; snippets only, not opened; company tags on such pages are unverified) | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports

**Pattern:** Counting with "at most k minus at most k-1", the same trick as Q30, now with a Counter window for the distinct count.

**Say this first (1 line):** "exactly(k) = at_most(k) - at_most(k-1). The helper is one Counter window, adds `right - left + 1` per right end. O(n) time, O(k) space."

**Brute force:** For each start, extend right with a set and count the ends where the set size is k. O(n^2) time, O(k) space.

**Optimal:**
- `at_most(k)`: add `nums[right]` to a Counter. While `len(count) > k`, remove `nums[left]` (delete the key at 0), `left += 1`. Then add `right - left + 1`: that many subarrays end at `right` with at most k distinct values (shrinking keeps validity).
- Answer: `at_most(k) - at_most(k-1)`.
- Why one window cannot count "exactly" directly: for a fixed right end, the starts that give exactly k distinct values form a range, and both ends of the range move. A single left pointer finds only one of them. At most k is monotone, so one pointer is enough.
- Memory: the Counter holds at most k+1 keys at any moment (we add first, then shrink), so space is O(k), not O(n).

**Complexity:** Time O(n) (two linear passes). Space O(k).

**Dry run:** `[1,2,1,2,3]`, `k=2`
- `at_most(2)`: right 0 adds 1, right 1 adds 2, right 2 adds 3, right 3 adds 4 (all within 2 distinct, windows of length 1, 2, 3, 4). At right 4 the value 3 makes 3 distinct: drop the 1 at index 0, the 2 at index 1, the 1 at index 2 (its key finally disappears), so left = 3, window [2,3], add 2. Total 1+2+3+4+2 = 12.
- `at_most(1)`: no two neighbours are equal, so each end adds 1: total 5.
- Answer 12 - 5 = 7.

**Code:**
```python
import random
from collections import Counter


def exact_brute(nums, k):
    total = 0
    for i in range(len(nums)):
        seen = set()
        for j in range(i, len(nums)):
            seen.add(nums[j])
            total += len(seen) == k
    return total


def at_most(nums, k):
    if k <= 0:
        return 0
    count = Counter()
    left = total = 0
    for right, x in enumerate(nums):
        count[x] += 1
        while len(count) > k:
            y = nums[left]
            count[y] -= 1
            if count[y] == 0:
                del count[y]  # keeps len(count) = distinct values, so memory stays O(k)
            left += 1
        total += right - left + 1
    return total


def exact_window(nums, k):
    return at_most(nums, k) - at_most(nums, k - 1)


print("[1,2,1,2,3], 2:", exact_window([1, 2, 1, 2, 3], 2), "(expected 7)")
print("[1,2,1,3,4], 3:", exact_window([1, 2, 1, 3, 4], 3), "(expected 3)")

random.seed(33)
for _ in range(1000):
    n = random.randint(0, 12)
    nums = [random.randint(1, 4) for _ in range(n)]
    k = random.randint(1, 5)
    assert exact_window(nums, k) == exact_brute(nums, k), (nums, k)
print("cross-check: 1000 seeded cases agree")

assert exact_window([], 1) == 0
assert exact_window([1], 1) == 1
assert exact_window([1, 1, 1], 1) == 6
assert exact_window([1, 1, 1], 2) == 0
assert exact_window([1, 2, 3], 3) == 1
assert exact_window([1, 2, 3], 4) == 0  # k above the distinct count
assert exact_window([1, 2], 1) == 2
big = [random.randint(1, 50) for _ in range(2 * 10 ** 4)]
assert exact_window(big, 5) > 0
assert exact_window(list(range(1, 20001)), 2) == 19999
print("edge asserts passed")
```

**Output (my run):**
```text
[1,2,1,2,3], 2: 7 (expected 7)
[1,2,1,3,4], 3: 3 (expected 3)
cross-check: 1000 seeded cases agree
edge asserts passed
```

Both prompt examples are correct as written.

**Edge cases:**
- k above the number of distinct values: 0.
- `k = 1` with all equal values: n(n+1)/2.
- `at_most(0)` must be 0 (guard).
- Empty list: 0.
- n = 2 * 10^4: fast.

**Follow-ups:**
- Do it in one pass? Possible with a second left pointer (track the start range for exact-k), but the difference-of-two version is easier to get right under pressure.
- The same trick solves Count nice subarrays (Q30) and binary subarrays with a given sum.
- Values not positive or not hashable? Counter needs hashable values; sign does not matter here (distinct count only).

**Common mistakes:**
- Not deleting zero-count keys, so `len(count)` is wrong.
- Forgetting `at_most(0) = 0`; the shrink loop would then misbehave on an empty window.
- Adding 1 instead of `right - left + 1`.
- Subtracting `at_most(k)` from itself or using `k+1` instead of `k-1` in the second call.

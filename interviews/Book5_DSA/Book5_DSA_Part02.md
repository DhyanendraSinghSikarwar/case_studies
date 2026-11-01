# Book 5 — Part 2: Two pointers and sliding window

**Topic:** Python DSA for product-company interviews: opposite-ends two pointers (sorted two-sum, container with most water, 3Sum, 3Sum closest, 4Sum, trapping rain water, palindrome variants), same-direction and partition pointers on arrays (remove duplicates keeping at most two, parity partition, Dutch national flag), merging and walking sorted lists, fixed-size windows (maximum average, anagram and permutation windows, cards from the ends), variable windows (longest substring without repeats, minimum window substring, at most k distinct, minimum size subarray sum, character replacement, fruit baskets, flips), counting subarrays with 'at most k minus at most k-1', Counter-state windows, why windows break with negatives and when to switch to prefix sums, the monotonic-deque window maximum, fast and slow pointers on arrays, and invariants and off-by-one patterns

**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 16, ⭐⭐ 17, ⭐ 12)  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns two pointers (opposite ends, same direction, partition, fast and slow on arrays) and sliding windows (fixed, variable, counting, Counter state). Part 1 already owns hashing, prefix sums with a hashmap, and the in-place keep-one remove-duplicates, move-zeroes and merge-into-array tasks (cross-referenced here only as 'Part 1 Q3, Q5, Q6, Q13, Q22', each checked against its heading); Part 3 owns string algorithms proper (KMP, Z, rolling hash, palindromic substrings), so string questions here are windows and pointers only; Part 4 owns stacks, queues and the monotonic stack and queue family (the two window-maximum questions here use the deque idea only); Part 5 owns binary search (including the O(log) two-sorted-arrays selection); Part 6 linked-list two pointers; Part 8 heaps, intervals and greedy (boats-style pairing appears here only as the sort plus two-pointer step); Part 13 owns deep prefix sums. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example in every prompt was run against brute-force reference code (scratch/B5P02_wavea/check_examples.py, python3 -I) before freezing. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for neetcode.io) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part02_sources.md). Searches for TCS NQT, Infosys, Wipro and for Amazon, Google and other company frequency returned only generic pattern guides, so 'Asked at' tags name source types (public pattern lists, pattern guides, Indian placement-style prep sheets, company-tagged prep pages), not verified company reports; company tags on community pages are unverified. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only (sortedcontainers only where a question says so).

---

### Q1 ⭐⭐⭐ 🟢 Valid palindrome. Given a string `s` (0 <= len <= 2*10^5, printable ASCII), decide whether it reads the same forwards and backwards after you drop every non-alphanumeric character and ignore letter case. Use two pointers from the ends in O(1) extra space (do not build a cleaned copy) and say how the pointers skip junk characters. Example: 'A man, a plan, a canal: Panama' -> True; 'race a car' -> False; ' ' -> True (nothing left to compare); '0P' -> False.
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports

**Pattern:** Opposite-ends two pointers. A palindrome check compares the first and last useful characters and moves inward, so one pointer from each end fits.

**Say this first (1 line):** "Two pointers from both ends; each skips non-alphanumeric characters, compares lowercased, and moves in. O(n) time, O(1) space, no cleaned copy."

**Brute force:** Build `cleaned = [c.lower() for c in s if c.isalnum()]` and compare it with its reverse. O(n) time but O(n) extra space. Fine as a first answer and as my checker.

**Optimal:**
- `i = 0`, `j = len(s) - 1`.
- Move `i` right while it points at junk. Move `j` left while it points at junk. Keep `i < j` in those inner loops so they cannot cross.
- Compare `s[i].lower()` and `s[j].lower()`. Mismatch means False.
- Otherwise step both in. When they meet or cross, return True.
- Invariant: everything outside `[i, j]` has already been matched or skipped as junk.

**Complexity:** Time O(n): each pointer only moves one way, so at most n steps in total. Space O(1).

**Dry run:** `s = "0P"`
| step | i, j | chars | action |
|---|---|---|---|
| 1 | 0, 1 | '0' vs 'p' | both alphanumeric, lowercased they differ |
| 2 | | | return False |

`s = " "`: `i = 0 = j`, the loop never runs, so True. Nothing is left to compare.

**Code:**
```python
import random


def pal_brute(s):
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]


def pal_two_pointers(s):
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and not s[i].isalnum():
            i += 1
        while i < j and not s[j].isalnum():
            j -= 1
        if s[i].lower() != s[j].lower():
            return False
        i += 1
        j -= 1
    return True


examples = [("A man, a plan, a canal: Panama", True), ("race a car", False),
            (" ", True), ("0P", False)]
for s, want in examples:
    got = pal_two_pointers(s)
    assert got == pal_brute(s) == want, (s, got, want)
    print(repr(s), "->", got)

assert pal_two_pointers("") is True
assert pal_two_pointers(".,") is True          # only junk
assert pal_two_pointers("a") is True
assert pal_two_pointers("ab") is False
assert pal_two_pointers("a.") is True
assert pal_two_pointers("Aa") is True          # case ignored
assert pal_two_pointers("0P0") is True         # digits count
assert pal_two_pointers("a" * 200000) is True  # max size, no recursion

rng = random.Random(5)
alphabet = "aAbB1 ,.:"
cases = 0
for _ in range(3000):
    s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 9)))
    assert pal_two_pointers(s) == pal_brute(s), s
    cases += 1
# force palindromes too, so True is well covered
for _ in range(1000):
    half = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 5)))
    s = half + rng.choice(["", "x", " "]) + half[::-1].swapcase()
    assert pal_two_pointers(s) == pal_brute(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
'A man, a plan, a canal: Panama' -> True
'race a car' -> False
' ' -> True
'0P' -> False
random cross-check passed: 4000 cases
```
All four examples in the prompt are correct.

**Edge cases:**
- Empty string or only junk (`".,"`): True.
- Digits count as characters, so `"0P"` is False.
- Single character: True.
- Length 2*10^5: iterative, so no recursion limit problem.

**Follow-ups:**
- *Why not `s = ''.join(...)` and compare?* It works but uses O(n) space; the question asked for O(1).
- *Unicode input?* `str.isalnum()` already handles Unicode letters, but `lower()` can be wrong for some scripts; use `casefold()` and mention normalisation.
- *Allow one deletion?* That is Valid palindrome II (Part 2 Q20).

**Common mistakes:**
- Forgetting `i < j` in the inner skip loops, which gives an index error on a string like `".,"`.
- Using `isalpha()` and dropping digits.
- Forgetting to lowercase before comparing.
- Using `str.isalnum` through a regex strip first and calling it "O(1) space".

### Q2 ⭐⭐⭐ 🟢 Two Sum on a sorted array. `numbers` is sorted in non-decreasing order (2 <= len <= 3*10^4, values may be negative) and exactly one pair of different positions sums to `target`. Return that pair of 0-based indices (i, j) with i < j using O(1) extra space. Explain why moving the left pointer up or the right pointer down is safe (the exchange argument). Example: numbers=[2,7,11,15], target=9 -> (0, 1); numbers=[2,3,4], target=6 -> (0, 2); numbers=[-1,0], target=-1 -> (0, 1).
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution)

**Pattern:** Opposite-ends two pointers on a sorted array. Sorting gives a direction: a sum that is too small needs a bigger number, too big needs a smaller one.

**Say this first (1 line):** "Left pointer at the start, right at the end; if the sum is too small move left up, if too big move right down. O(n) time, O(1) space."

**Brute force:** Try every pair `(i, j)`. O(n^2) time, O(1) space. 3*10^4 elements means about 4.5*10^8 pairs, too slow in Python.

**Optimal:**
- Start `i = 0`, `j = n - 1`.
- `s = nums[i] + nums[j]`. Equal to target: return `(i, j)`.
- `s < target`: `i += 1`. `s > target`: `j -= 1`.
- Why that is safe (exchange argument): if `s < target`, then `nums[i]` paired with anything at or left of `j` is at most `s`, so `nums[i]` can never be part of the answer with a partner inside the range. Discarding it loses nothing. The `s > target` case is symmetric for `nums[j]`.
- Invariant: if the answer exists, both its indices are inside `[i, j]`.

**Complexity:** Time O(n): every step removes one index from the range. Space O(1). It does not need the sort cost because the input is already sorted.

**Dry run:** `numbers = [2, 3, 4]`, `target = 6`
| i, j | sum | action |
|---|---|---|
| 0, 2 | 2 + 4 = 6 | equal, return (0, 2) |

`numbers = [2, 7, 11, 15]`, `target = 9`: sum 2 + 15 = 17 too big, so `j = 2`; 2 + 11 = 13, `j = 1`; 2 + 7 = 9, return (0, 1).

**Code:**
```python
import random


def two_sum_brute(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum_sorted(nums, target):
    i, j = 0, len(nums) - 1
    while i < j:
        s = nums[i] + nums[j]
        if s == target:
            return (i, j)
        if s < target:
            i += 1
        else:
            j -= 1
    return None


for nums, t in [([2, 7, 11, 15], 9), ([2, 3, 4], 6), ([-1, 0], -1)]:
    print(nums, t, "->", two_sum_sorted(nums, t))
assert two_sum_sorted([2, 7, 11, 15], 9) == (0, 1)
assert two_sum_sorted([2, 3, 4], 6) == (0, 2)
assert two_sum_sorted([-1, 0], -1) == (0, 1)
assert two_sum_sorted([3, 3], 6) == (0, 1)             # duplicates, different positions
assert two_sum_sorted([-5, -3, -1], -8) == (0, 1)      # all negative
assert two_sum_sorted([1, 2], 100) is None             # no pair (outside the promise)

rng = random.Random(11)
cases = 0
for _ in range(2000):
    n = rng.randint(2, 9)
    nums = sorted(rng.randint(-6, 6) for _ in range(n))
    # pick a target; keep only inputs with exactly one valid pair (the promise)
    i, j = sorted(rng.sample(range(n), 2))
    t = nums[i] + nums[j]
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if nums[a] + nums[b] == t]
    if len(pairs) != 1:
        continue
    assert two_sum_sorted(nums, t) == two_sum_brute(nums, t) == pairs[0]
    cases += 1
print("random cross-check passed:", cases, "unique-pair cases")
```

**Output (my run):**
```
[2, 7, 11, 15] 9 -> (0, 1)
[2, 3, 4] 6 -> (0, 2)
[-1, 0] -1 -> (0, 1)
random cross-check passed: 1049 unique-pair cases
```
All three prompt examples are correct. The random check keeps only inputs that have exactly one valid pair, because that is the promise in the prompt.

**Edge cases:**
- Negative numbers work, since only the sorted order is used.
- Duplicate values (`[3, 3]`, target 6): different positions, so (0, 1) is valid.
- Length exactly 2.
- If no pair existed the loop would end with `i == j`; the prompt promises one, so I return None only for safety.

**Follow-ups:**
- *Unsorted input?* Use a hash map of value to index in O(n) (Part 1 Two Sum), or sort first if I do not need original indices.
- *Return 1-based indices?* Add 1 to each.
- *Many pairs, return all?* Skip duplicates after each hit; this is the building block of 3Sum (Q8).

**Common mistakes:**
- Using `i <= j`, which lets one element pair with itself.
- Using a `for` loop and binary searching for the partner: valid but O(n log n).
- Returning values instead of indices.
- Applying this to unsorted data.

### Q3 ⭐⭐⭐ 🟢 Maximum average of a fixed-size window. Given integers `nums` (1 <= k <= len <= 10^5, values may be negative) and k, return the largest average over all contiguous blocks of exactly k elements, as a float. Slide a running sum instead of re-summing each block. Example: nums=[1,12,-5,-6,50,3], k=4 -> 12.75; nums=[5], k=1 -> 5.0.
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution) | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports

**Pattern:** Fixed-size sliding window. Neighbouring windows share k-1 elements, so update the sum instead of recomputing it.

**Say this first (1 line):** "Sum the first k, then slide: add the entering element, subtract the leaving one, keep the best sum, divide by k once at the end. O(n) time, O(1) space."

**Brute force:** For every start, `sum(nums[i:i+k])`. O(n*k) time. With n = k = 10^5 half that is already 2.5*10^9 operations.

**Optimal:**
- `s = sum(nums[:k])`, `best = s`.
- For `r` from k to n-1: `s += nums[r] - nums[r-k]`, then `best = max(best, s)`.
- Compare sums, not averages: the divisor k is the same for every window, so the largest sum has the largest average. Divide once at the end.
- Invariant: after step r, `s` is the sum of `nums[r-k+1 .. r]`.

**Complexity:** Time O(n): one pass for the first window (k steps) plus n-k slides. Space O(1).

**Dry run:** `nums = [1, 12, -5, -6, 50, 3]`, `k = 4`
| r | add | drop | window sum |
|---|---|---|---|
| start | | | 1 + 12 - 5 - 6 = 2 |
| 4 | +50 | -1 | 51 |
| 5 | +3 | -12 | 42 |
Best sum 51, 51 / 4 = 12.75.

**Code:**
```python
import random


def max_avg_brute(nums, k):
    return max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1)) / k


def max_avg_window(nums, k):
    s = sum(nums[:k])
    best = s
    for r in range(k, len(nums)):
        s += nums[r] - nums[r - k]     # add entering, drop leaving
        if s > best:
            best = s
    return best / k


print(max_avg_window([1, 12, -5, -6, 50, 3], 4))
print(max_avg_window([5], 1))
assert max_avg_window([1, 12, -5, -6, 50, 3], 4) == 12.75
assert max_avg_window([5], 1) == 5.0
assert max_avg_window([-3, -1, -2], 2) == -1.5          # all negative: do not start best at 0
assert max_avg_window([4, 4, 4], 3) == 4.0              # k == len
assert max_avg_window([0, 0], 1) == 0.0
big = list(range(100000))
assert max_avg_window(big, 100000) == sum(big) / 100000  # max size, k == len

rng = random.Random(3)
cases = 0
for _ in range(1500):
    n = rng.randint(1, 12)
    nums = [rng.randint(-9, 9) for _ in range(n)]
    k = rng.randint(1, n)
    assert max_avg_window(nums, k) == max_avg_brute(nums, k)
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
12.75
5.0
random cross-check passed: 1500 cases
```
Both prompt examples are correct. The random cross-check compares floats with `==` and is safe because both versions divide the same integer by the same k.

**Edge cases:**
- All negative values: start `best` from the first window, not from 0.
- `k == len`: the loop body never runs and the answer is the whole average.
- `k == 1`: the answer is the maximum element.
- Large input: Python integers do not overflow.

**Follow-ups:**
- *Average at least some threshold?* Same window, count windows with `s >= threshold * k`.
- *Windows of every size?* Different problem; prefix sums.
- *Float error worry?* Keep the sum as an integer, which is what I do.

**Common mistakes:**
- Initialising `best = 0` (breaks for negatives) or `float('-inf')` and then also forgetting the first window.
- Dropping `nums[r-k+1]` instead of `nums[r-k]`.
- Dividing every window instead of once.

### Q4 ⭐⭐⭐ 🟢 Best time to buy and sell stock once. `prices[i]` is the price on day i (1 <= len <= 10^5). Choose one day to buy and a strictly later day to sell to maximise profit; return 0 if no profit is possible. Present it as a single pass that tracks the lowest price so far (a window whose left edge only moves to a new minimum) and say why O(n^2) pairs is unnecessary. Example: [7,1,5,3,6,4] -> 5; [7,6,4,3,1] -> 0.
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports

**Pattern:** One pass tracking a running minimum. It is a window `[buy, today]` whose left edge only jumps when a lower price appears.

**Say this first (1 line):** "Walk forward keeping the lowest price so far; at each day the best sale is price minus that lowest, keep the maximum. One pass, O(n) time, O(1) space."

**Brute force:** Check every buy day `i` against every later sell day `j`. O(n^2) time. For 10^5 days that is about 5*10^9 pairs.

**Optimal:**
- `lowest = prices[0]`, `best = 0`.
- For each later price `p`: if `p < lowest`, set `lowest = p`. Otherwise `best = max(best, p - lowest)`.
- Why it is enough: the best trade selling on day j buys at the minimum of days before j. So we only need that minimum, not every earlier day.
- Invariant: `lowest` is the minimum of the prefix, `best` is the best profit within the prefix.

**Complexity:** Time O(n), space O(1). The pair loop is unnecessary because for each sell day only one buy day (the prefix minimum) can be optimal.

**Dry run:** `[7, 1, 5, 3, 6, 4]`
| price | lowest | best |
|---|---|---|
| 7 | 7 | 0 |
| 1 | 1 | 0 |
| 5 | 1 | 4 |
| 3 | 1 | 4 |
| 6 | 1 | 5 |
| 4 | 1 | 5 |
Answer 5.

**Code:**
```python
import random


def profit_brute(prices):
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best


def profit_one_pass(prices):
    lowest = prices[0]
    best = 0
    for p in prices[1:]:
        if p < lowest:
            lowest = p             # new buy candidate (left edge jumps here)
        elif p - lowest > best:
            best = p - lowest      # selling today beats the best so far
    return best


print(profit_one_pass([7, 1, 5, 3, 6, 4]))
print(profit_one_pass([7, 6, 4, 3, 1]))
assert profit_one_pass([7, 1, 5, 3, 6, 4]) == 5
assert profit_one_pass([7, 6, 4, 3, 1]) == 0
assert profit_one_pass([5]) == 0                 # single day
assert profit_one_pass([3, 3, 3]) == 0           # all equal
assert profit_one_pass([1, 2]) == 1
assert profit_one_pass([2, 1]) == 0
assert profit_one_pass([2, 4, 1]) == 2           # min comes after the peak: must not use it
assert profit_one_pass(list(range(100000))) == 99999

rng = random.Random(8)
cases = 0
for _ in range(3000):
    n = rng.randint(1, 10)
    prices = [rng.randint(0, 12) for _ in range(n)]
    assert profit_one_pass(prices) == profit_brute(prices), prices
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
5
0
random cross-check passed: 3000 cases
```
Both prompt examples are correct.

**Edge cases:**
- Falling prices: 0, never negative.
- One day: 0.
- All equal: 0.
- The minimum after the maximum (`[2, 4, 1]`): the answer is 2, not 1 - 4.

**Follow-ups:**
- *Unlimited transactions?* Add up every positive day-to-day rise (greedy).
- *At most two transactions?* Track four states (buy1, sell1, buy2, sell2); a DP topic.
- *Also return the days?* Remember the index of `lowest` and update the pair when `best` improves.

**Common mistakes:**
- Taking `max(prices) - min(prices)`, which ignores order.
- Initialising `best` to a negative number and returning a loss.
- Updating `best` before `lowest` on the same day in a way that lets you buy and sell on one day; harmless for profit but wrong if you report days.

### Q5 ⭐⭐⭐ 🟢 Squares of a sorted array. `nums` is sorted non-decreasing and may hold negatives (1 <= len <= 10^4). Return the squares in non-decreasing order in O(n) time with two pointers from the ends filling the output from the back, and explain why the largest square is always at one of the two ends. Example: [-4,-1,0,3,10] -> [0,1,9,16,100]; [-7,-3,2,3,11] -> [4,9,9,49,121].
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution)

**Pattern:** Opposite-ends two pointers, filling the output from the back. After squaring, the sequence is "big, small, big": the largest value is at one of the two ends.

**Say this first (1 line):** "Compare the squares at both ends, put the larger at the back of the result, move that pointer inward. O(n) time instead of the O(n log n) sort."

**Brute force:** `sorted(x * x for x in nums)`. O(n log n) time, O(n) output. Simple, and I use it as the checker.

**Optimal:**
- Why the largest square is at an end: the biggest absolute value in a sorted list is either the first element (most negative) or the last (most positive).
- `i = 0`, `j = n - 1`, write index `w = n - 1` going down.
- Compare `nums[i]^2` and `nums[j]^2`. Put the larger at `out[w]`, move its pointer inward, `w -= 1`.
- Invariant: `out[w+1:]` holds the largest squares in order, and all remaining values lie in `[i, j]`.

**Complexity:** Time O(n): each step consumes one element. Space O(n) for the output (the required result), O(1) extra.

**Dry run:** `[-4, -1, 0, 3, 10]`
| i, j | squares | write | out |
|---|---|---|---|
| 0, 4 | 16 vs 100 | out[4] = 100, j=3 | ..., 100 |
| 0, 3 | 16 vs 9 | out[3] = 16, i=1 | ..., 16, 100 |
| 1, 3 | 1 vs 9 | out[2] = 9, j=2 | 9, 16, 100 |
| 1, 2 | 1 vs 0 | out[1] = 1, i=2 | 1, 9, 16, 100 |
| 2, 2 | 0 vs 0 | out[0] = 0 | 0, 1, 9, 16, 100 |

**Code:**
```python
import random


def squares_brute(nums):
    return sorted(x * x for x in nums)


def squares_two_pointers(nums):
    n = len(nums)
    out = [0] * n
    i, j = 0, n - 1
    for w in range(n - 1, -1, -1):          # fill from the back, largest first
        a, b = nums[i] * nums[i], nums[j] * nums[j]
        if a > b:
            out[w] = a
            i += 1
        else:
            out[w] = b
            j -= 1
    return out


print(squares_two_pointers([-4, -1, 0, 3, 10]))
print(squares_two_pointers([-7, -3, 2, 3, 11]))
assert squares_two_pointers([-4, -1, 0, 3, 10]) == [0, 1, 9, 16, 100]
assert squares_two_pointers([-7, -3, 2, 3, 11]) == [4, 9, 9, 49, 121]
assert squares_two_pointers([5]) == [25]
assert squares_two_pointers([-5]) == [25]
assert squares_two_pointers([-3, -2, -1]) == [1, 4, 9]     # all negative
assert squares_two_pointers([1, 2, 3]) == [1, 4, 9]        # all non-negative
assert squares_two_pointers([-2, -2, 2, 2]) == [4, 4, 4, 4]  # ties
assert squares_two_pointers([0, 0, 0]) == [0, 0, 0]

rng = random.Random(21)
cases = 0
for _ in range(2000):
    n = rng.randint(1, 10)
    nums = sorted(rng.randint(-8, 8) for _ in range(n))
    assert squares_two_pointers(nums) == squares_brute(nums), nums
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
[0, 1, 9, 16, 100]
[4, 9, 9, 49, 121]
random cross-check passed: 2000 cases
```
Both prompt examples are correct.

**Edge cases:**
- One element, negative or not.
- All negative: the result is the reverse order of the squares.
- All non-negative: pointer `j` does all the moving.
- Ties (`-2` and `2`): either branch is fine.

**Follow-ups:**
- *Why not fill from the front?* The smallest square is in the middle, so we would have to find the sign boundary first.
- *Other sorted-by-function transforms?* Same trick for sorting `a*x^2 + b*x + c` of a sorted array: the parabola gives the same two-ended shape.
- *Cheaper alternative?* Find where the sign changes and merge two lists outward; same O(n).

**Common mistakes:**
- Writing from the front, which gives descending order.
- Using `abs` comparisons and forgetting to square the value that is written.
- Running the loop on `i < j`, which skips the final element.

### Q6 ⭐⭐⭐ 🟡 Longest substring without repeating characters. Given a string `s` (0 <= len <= 5*10^4, any ASCII), return the length of the longest contiguous substring with all distinct characters. Give the variable sliding window with a last-seen index map (jump the left edge past the previous occurrence) and the set-based shrink version; state the invariant that holds after every step. Example: 'abcabcbb' -> 3; 'bbbbb' -> 1; 'pwwkew' -> 3; '' -> 0; 'abba' -> 2 (the last-seen jump must never move the left edge backwards).
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution)

**Pattern:** Variable-size sliding window. The window `[left, r]` always has distinct characters; the right edge expands, the left edge jumps or shrinks to keep it valid.

**Say this first (1 line):** "Keep a window with no repeats and a map of each character's last index; on a repeat, move left just past the old occurrence. One pass, O(n) time."

**Brute force:** For each start, extend until a repeat appears, tracking a set. O(n^2) time worst case, O(k) space where k is the alphabet size.

**Optimal (last-seen map):**
- `last[c]` is the latest index of `c`. `left` is the window start.
- At `r`, if `c` is in `last` and `last[c] >= left`, set `left = last[c] + 1`.
- Always `last[c] = r`, then `best = max(best, r - left + 1)`.
- The `>= left` test matters: an old occurrence left of the window is irrelevant. Without it, `left` could move backwards (`'abba'`).

**Optimal (set version):** On each new `c`, `while c in seen: seen.remove(s[left]); left += 1`, then add `c`. Same O(n), because `left` only moves forward and each index is removed at most once.

**Invariant after every step:** `s[left..r]` has all distinct characters, `left` has never decreased, and `best` is the longest such window seen so far.

**Complexity:** Time O(n): both pointers only move right. Space O(min(n, alphabet size)).

**Dry run:** `'abba'`
| r | c | last | left | window | best |
|---|---|---|---|---|---|
| 0 | a | a:0 | 0 | a | 1 |
| 1 | b | b:1 | 0 | ab | 2 |
| 2 | b | b:2 | 2 | b | 2 |
| 3 | a | last[a] = 0 < left 2, so no jump | 2 | ba | 2 |
Answer 2. If I had jumped to `last['a'] + 1 = 1`, left would go backwards and give a wrong length 3.

**Code:**
```python
import random


def longest_brute(s):
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
            best = max(best, j - i + 1)
    return best


def longest_last_seen(s):
    last = {}              # char -> index of its latest occurrence
    left = best = 0
    for r, c in enumerate(s):
        if c in last and last[c] >= left:   # the >= left test stops the left edge going backwards
            left = last[c] + 1
        last[c] = r
        best = max(best, r - left + 1)
    return best


def longest_set(s):
    seen = set()
    left = best = 0
    for r, c in enumerate(s):
        while c in seen:               # shrink until c is free
            seen.remove(s[left])
            left += 1
        seen.add(c)
        best = max(best, r - left + 1)
    return best


for s, want in [("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3), ("", 0), ("abba", 2)]:
    a, b = longest_last_seen(s), longest_set(s)
    assert a == b == longest_brute(s) == want, (s, a, b, want)
    print(repr(s), "->", a)

assert longest_last_seen("a") == 1
assert longest_last_seen("abcdef") == 6            # all distinct
assert longest_last_seen("tmmzuxt") == 5           # old 't' is left of the window: do not move left back
assert longest_last_seen("dvdf") == 3
assert longest_last_seen("ab" * 25000) == 2        # max size
assert longest_set("ab" * 25000) == 2
assert longest_last_seen("a b a") == 3

rng = random.Random(14)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 12)))
    want = longest_brute(s)
    assert longest_last_seen(s) == want and longest_set(s) == want, s
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
'abcabcbb' -> 3
'bbbbb' -> 1
'pwwkew' -> 3
'' -> 0
'abba' -> 2
random cross-check passed: 3000 cases
```
All five prompt examples are correct.

**Edge cases:**
- Empty string: 0.
- All distinct: the whole length.
- All same: 1.
- `'tmmzuxt'` is a classic for the backwards-jump bug: the answer is 5.
- Length 5*10^4: linear, so fine.

**Follow-ups:**
- *Return the substring?* Remember the `left` where `best` improved.
- *Unicode?* The dict handles any hashable character; a 128-slot array would not.
- *At most k distinct?* Q25.

**Common mistakes:**
- `left = last[c] + 1` without `max` or the `>= left` check.
- Updating `last` before checking.
- Using `len(set(s))` as a shortcut; that counts distinct characters, not a substring.
- Calling the set version O(n^2): each element enters and leaves once.

### Q7 ⭐⭐⭐ 🟡 Container with most water. `height` holds n >= 2 non-negative integers, line i standing at x=i with that height. Pick two lines; the water they hold is (distance between them) * (the shorter height). Return the maximum, in O(n) with two pointers; prove why moving the pointer at the shorter line never loses the optimum. Example: [1,8,6,2,5,4,8,3,7] -> 49; [1,1] -> 1.
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports

**Pattern:** Opposite-ends two pointers with a greedy move. Start with the widest container and give up the shorter wall each step.

**Say this first (1 line):** "Pointers at both ends; compute the area, then move the pointer at the shorter line inward, since keeping it can only get worse. O(n) time, O(1) space."

**Brute force:** Try every pair of lines. O(n^2) time, O(1) space.

**Optimal:**
- Area of `(i, j)` is `(j - i) * min(h[i], h[j])`.
- Move the pointer at the shorter line. Proof: say `h[i] <= h[j]`. For any partner `k` with `i < k < j`, the width is smaller than `j - i` and the height is still at most `h[i]`, so the area is at most the current one. So every pair that uses `i` with a narrower partner is no better than what we just measured. Line `i` is finished and can be dropped.
- Move the other pointer when `h[j] < h[i]` by the mirror argument. On a tie either move is safe.
- Invariant: the optimal pair lies within `[i, j]` or its value has already been recorded.

**Complexity:** Time O(n): each step removes one line. Space O(1).

**Dry run:** `[1, 8, 6, 2, 5, 4, 8, 3, 7]`
| i, j | area | move |
|---|---|---|
| 0, 8 | 8 * 1 = 8 | h[0]=1 shorter, i=1 |
| 1, 8 | 7 * 7 = 49 | h[8]=7 shorter, j=7 |
| 1, 7 | 6 * 3 = 18 | j=6 |
| 1, 6 | 5 * 8 = 40 | heights tie (8 and 8), move j |
| 1, 5 and on | 4 * 4 = 16 and smaller | nothing beats 49 |
Best 49.

**Code:**
```python
import random


def water_brute(h):
    best = 0
    for i in range(len(h)):
        for j in range(i + 1, len(h)):
            best = max(best, (j - i) * min(h[i], h[j]))
    return best


def water_two_pointers(h):
    i, j = 0, len(h) - 1
    best = 0
    while i < j:
        best = max(best, (j - i) * min(h[i], h[j]))
        if h[i] < h[j]:
            i += 1          # shorter line cannot do better with any narrower partner
        else:
            j -= 1
    return best


print(water_two_pointers([1, 8, 6, 2, 5, 4, 8, 3, 7]))
print(water_two_pointers([1, 1]))
assert water_two_pointers([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
assert water_two_pointers([1, 1]) == 1
assert water_two_pointers([0, 0]) == 0              # zero heights
assert water_two_pointers([5, 5, 5, 5]) == 15       # all equal: widest wins
assert water_two_pointers([1, 2, 3, 4]) == 4        # rising
assert water_two_pointers([4, 3, 2, 1]) == 4        # falling
assert water_two_pointers([2, 0, 0, 0, 2]) == 8
assert water_two_pointers([3] * 100000) == 3 * 99999

rng = random.Random(2)
cases = 0
for _ in range(3000):
    n = rng.randint(2, 10)
    h = [rng.randint(0, 9) for _ in range(n)]
    assert water_two_pointers(h) == water_brute(h), h
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
49
1
random cross-check passed: 3000 cases
```
Both prompt examples are correct.

**Edge cases:**
- Two lines: one area.
- Zero heights: area 0.
- All equal: the widest pair wins.
- Monotonic rising or falling heights.
- Width counts the distance, not the number of lines.

**Follow-ups:**
- *Why not move the taller one?* The area cannot improve (width shrinks, the limiting height stays the same or drops), and we could skip the better shorter-side partner.
- *Trapping rain water?* Different goal, same two-pointer shape (Q14).
- *Unsorted heights, why is this still fine?* The argument uses only min and width, not sorting.

**Common mistakes:**
- Moving both pointers.
- Using the max instead of the min height.
- Using `j - i + 1` for width.
- Claiming it is "just greedy" without the exchange argument.

### Q8 ⭐⭐⭐ 🟡 3Sum. Given integers `nums` (3 <= len <= 3000), return all unique triplets (as sorted lists of values) that sum to 0, with no duplicate triplets in the answer. Sort, fix the first element and run opposite-ends two pointers, skipping duplicates at all three positions; give the O(n^2) bound and say what changes if you may not sort. Example: [-1,0,1,2,-1,-4] -> [[-1,-1,2],[-1,0,1]]; [0,0,0] -> [[0,0,0]]; [1,2,3] -> [].
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution)

**Pattern:** Sort, fix one element, then opposite-ends two pointers on the rest (reduces 3Sum to repeated sorted Two Sum, Q2).

**Say this first (1 line):** "Sort, fix `nums[i]`, then two pointers on the right part looking for `-nums[i]`, skipping duplicates at all three positions. O(n^2) time."

**Brute force:** Three nested loops with a set of sorted tuples. O(n^3) time. n = 3000 gives about 4.5*10^9 triples.

**Optimal:**
- Sort. For each `i`: stop if `nums[i] > 0` (every later value is also positive, so no zero sum). Skip if `nums[i] == nums[i-1]`.
- `lo = i + 1`, `hi = n - 1`. Sum too small: `lo += 1`. Too big: `hi -= 1`.
- Hit: record it, move both, then skip `lo` forward past equal values and `hi` backward past equal values.
- Duplicates are skipped at three places: the first element (outer loop), the second (after a hit), the third (after a hit).
- Invariant: for the current `i`, no triple using `nums[i]` with partners outside `[lo, hi]` is missing.

**Complexity:** Time O(n log n) for the sort plus O(n^2) for the scan. Space O(1) extra apart from the output (and the sort in Python is O(n) space).

**Without sorting:** use a hash set per first element (the `three_sum_hash` function): O(n^2) time, O(n) extra space, and I must dedupe by storing sorted tuples in a set. Sorting makes duplicate skipping cheap, so I prefer it.

**Dry run:** `[-1, 0, 1, 2, -1, -4]` sorted is `[-4, -1, -1, 0, 1, 2]`
| i | lo, hi | sum | action |
|---|---|---|---|
| -4 | -1, 2 | -3 | lo up ... never reaches 0 |
| -1 (idx 1) | -1, 2 | 0 | record [-1, -1, 2]; lo=3, hi=4 |
| | 0, 1 | 0 | record [-1, 0, 1] |
| -1 (idx 2) | | | skipped, equals previous |
| 0 | 1, 2 | 3 | too big, then done |
Answer `[[-1, -1, 2], [-1, 0, 1]]`.

**Code:**
```python
import random
from itertools import combinations


def three_sum_brute(nums):
    out = set()
    for a, b, c in combinations(nums, 3):
        if a + b + c == 0:
            out.add(tuple(sorted((a, b, c))))
    return sorted(list(t) for t in out)


def three_sum(nums):
    nums = sorted(nums)
    n = len(nums)
    res = []
    for i in range(n - 2):
        if nums[i] > 0:
            break                              # smallest is positive: no zero sum left
        if i > 0 and nums[i] == nums[i - 1]:
            continue                           # skip duplicate first element
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1                    # skip duplicate second element
                while lo < hi and nums[hi] == nums[hi + 1]:
                    hi -= 1                    # skip duplicate third element
    return res


def three_sum_hash(nums):
    # no-sort variant: set of sorted tuples, O(n^2) time, O(n) extra space
    seen_triples = set()
    n = len(nums)
    for i in range(n):
        seen = set()
        for j in range(i + 1, n):
            need = -nums[i] - nums[j]
            if need in seen:
                seen_triples.add(tuple(sorted((nums[i], nums[j], need))))
            seen.add(nums[j])
    return sorted(list(t) for t in seen_triples)


for nums in ([-1, 0, 1, 2, -1, -4], [0, 0, 0], [1, 2, 3]):
    print(nums, "->", three_sum(nums))
assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
assert three_sum([0, 0, 0]) == [[0, 0, 0]]
assert three_sum([1, 2, 3]) == []
assert three_sum([0, 0, 0, 0, 0]) == [[0, 0, 0]]              # many duplicates, one answer
assert three_sum([-2, 0, 0, 2, 2]) == [[-2, 0, 2]]
assert three_sum([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]) == three_sum_brute(
    [-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6])
assert three_sum([-1, -2, -3]) == []                          # all negative

rng = random.Random(9)
cases = 0
for _ in range(2000):
    n = rng.randint(3, 10)
    nums = [rng.randint(-5, 5) for _ in range(n)]
    want = three_sum_brute(nums)
    assert three_sum(nums) == want, nums
    assert three_sum_hash(nums) == want, nums
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
[-1, 0, 1, 2, -1, -4] -> [[-1, -1, 2], [-1, 0, 1]]
[0, 0, 0] -> [[0, 0, 0]]
[1, 2, 3] -> []
random cross-check passed: 2000 cases
```
All three prompt examples are correct. The cross-check also compares the sort-free version.

**Edge cases:**
- `[0, 0, 0]`: one triple. `[0, 0, 0, 0, 0]`: still one.
- All positive or all negative: empty.
- Many duplicates mixed in.
- The output order here is lexicographic because of the sorted scan; if the interviewer allows any order, say so.

**Follow-ups:**
- *3Sum closest?* Q27.
- *4Sum / k-Sum?* Q32.
- *Why `break` on `nums[i] > 0`?* Sorted, so all three values would be positive.

**Common mistakes:**
- Skipping duplicates of `i` with `nums[i] == nums[i+1]`, which loses `[-1, -1, 2]`.
- Forgetting the skips after a hit, producing repeated triples.
- Dedupe by `set` of lists (lists are unhashable) instead of tuples.
- Skipping duplicates before recording instead of after.

### Q9 ⭐⭐⭐ 🟡 Permutation in string. Given lowercase strings `s1` and `s2` (1 <= len <= 10^4), decide whether some contiguous substring of `s2` is a rearrangement of `s1`. Use a fixed window of length len(s1) with count arrays or a running 'letters matching' counter so each slide is O(1), and state what total work is. Example: s1='ab', s2='eidbaooo' -> True; s1='ab', s2='eidboaoo' -> False.
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports

**Pattern:** Fixed-size sliding window over `s2` with a count comparison. A permutation of `s1` is a window of the same length with the same letter counts.

**Say this first (1 line):** "Slide a window of length len(s1) over s2 keeping letter counts; a 'matching letters' counter makes each slide O(1). Total O(len(s2))."

**Brute force:** For each start, sort the substring and compare with `sorted(s1)`. O(n * k log k). Counting each window from scratch is O(n * k).

**Optimal:**
- `need[26]` holds counts for `s1`. `have[26]` holds the current window.
- `matches` = number of letters (of 26) where `have == need`. Start with the letters that have `need == 0` counted as matching.
- Adding a character: if `have[i] == need[i]` before the change, `matches -= 1`; apply the change; if equal afterwards, `matches += 1`. Same for removal.
- Return True the moment `matches == 26`.
- Invariant: after step r, `have` describes `s2[r-k+1 .. r]` (or the shorter prefix before the window fills).

**Complexity:** Time O(26 + n) where n = len(s2): each step does two O(1) updates. Space O(26) = O(1). Comparing two 26-slot arrays each step would be O(26 n); also fine but not O(1) per slide.

**Dry run:** `s1 = 'ab'`, `s2 = 'eidbaooo'`
| r | window | have vs need |
|---|---|---|
| 0-1 | e, ei | not matching |
| 2 | id | no |
| 3 | db | b ok, d extra, a missing |
| 4 | ba | a=1, b=1 match, all other 24 zeros match: matches 26 |
True at r = 4.

**Code:**
```python
import random
from collections import Counter


def perm_brute(s1, s2):
    k = len(s1)
    want = sorted(s1)
    return any(sorted(s2[i:i + k]) == want for i in range(len(s2) - k + 1))


def perm_window(s1, s2):
    k = len(s1)
    if k > len(s2):
        return False
    need = [0] * 26
    have = [0] * 26
    for c in s1:
        need[ord(c) - 97] += 1
    matches = 0                         # how many of the 26 letters have have == need

    def bump(idx, delta):
        nonlocal matches
        if have[idx] == need[idx]:
            matches -= 1                # was matching, about to change
        have[idx] += delta
        if have[idx] == need[idx]:
            matches += 1                # matches after the change

    for i in range(26):
        if need[i] == 0:
            matches += 1                # 0 == 0 matches at the start
    for r, c in enumerate(s2):
        bump(ord(c) - 97, 1)
        if r >= k:
            bump(ord(s2[r - k]) - 97, -1)
        if matches == 26:
            return True
    return False


print(perm_window("ab", "eidbaooo"))
print(perm_window("ab", "eidboaoo"))
assert perm_window("ab", "eidbaooo") is True
assert perm_window("ab", "eidboaoo") is False
assert perm_window("a", "a") is True
assert perm_window("ab", "a") is False                 # s1 longer than s2
assert perm_window("abc", "abc") is True               # whole string
assert perm_window("aab", "abab") is True              # repeats: counts matter
assert perm_window("aab", "abba") is False
assert perm_window("z" * 5000, "z" * 10000) is True    # max size

rng = random.Random(17)
cases = 0
for _ in range(3000):
    s1 = "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
    s2 = "".join(rng.choice("abc") for _ in range(rng.randint(1, 9)))
    assert perm_window(s1, s2) == perm_brute(s1, s2), (s1, s2)
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
True
False
random cross-check passed: 3000 cases
```
Both prompt examples are correct.

**Edge cases:**
- `len(s1) > len(s2)`: False at once.
- Equal length: one window.
- Repeated letters: counts must match, not just presence (`'aab'` vs `'abba'`).
- Early exit on the first match.

**Follow-ups:**
- *All start positions?* That is Q10.
- *Unicode or large alphabet?* Use a Counter and track `diff` count of unequal keys.
- *Why not just sort each window?* O(n k log k).

**Common mistakes:**
- Checking presence instead of counts.
- Shrinking the window before it reaches size k (`r >= k`, not `r > k`).
- Starting `matches` at 0 and forgetting zero-count letters.
- Updating `matches` after changing the array, so it is off by one.

### Q10 ⭐⭐⭐ 🟡 Find all anagram start positions. Given lowercase strings `s` and `p` (1 <= len <= 3*10^4), return every start index i, in increasing order, such that `s[i:i+len(p)]` is a rearrangement of `p`. Slide one window, adding the entering and removing the leaving character; contrast comparing two 26-length arrays per step with an O(1) matches counter. (Part 1 Q3, Valid anagram, is plain hashing; here the point is the window update.) Example: s='cbaebabacd', p='abc' -> [0, 6]; s='abab', p='ab' -> [0, 1, 2].
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Company-tagged prep pages (a Jointaro interview-question page files this problem under an Uber path and Educative and NeetCode solution pages cover it; snippets only, not opened; company tags on such pages are unverified)

**Pattern:** Fixed-size sliding window with a letter-count balance; every window whose counts equal `p`'s is an anagram (see Part 1 Q3 for plain hashing; here the point is the window update).

**Say this first (1 line):** "One window of length len(p): add the entering character, remove the leaving one, and keep a count of letters that still differ; a zero means an anagram starts here. O(n) time."

**Brute force:** For each start, sort `s[i:i+k]` and compare with `sorted(p)`. O(n * k log k).

**Optimal:**
- `cnt[x] = window count - need count`. Initially it is minus the counts of `p`.
- `diff` = number of letters with `cnt != 0`.
- On each step, add `s[r]`, and once the window is full also remove `s[r-k]`; update `diff` only when a count crosses zero.
- When `r >= k - 1` and `diff == 0`, record `r - k + 1`.
- The array comparison version (`have == need`) is simpler and costs 26 per step, so O(26 n). The `diff` version is O(1) per step.

**Complexity:** Time O(n + 26), space O(26) = O(1). The result list is the output.

**Dry run:** `s = 'abab'`, `p = 'ab'`
| r | window | diff | record |
|---|---|---|---|
| 0 | a | 1 | none (not full) |
| 1 | ab | 0 | 0 |
| 2 | ba | 0 | 1 |
| 3 | ab | 0 | 2 |
Answer `[0, 1, 2]`.

**Code:**
```python
import random


def anagram_starts_brute(s, p):
    k = len(p)
    want = sorted(p)
    return [i for i in range(len(s) - k + 1) if sorted(s[i:i + k]) == want]


def anagram_starts_arrays(s, p):
    # compare two 26-length lists each step: O(26 * n)
    k = len(p)
    if k > len(s):
        return []
    need, have = [0] * 26, [0] * 26
    for c in p:
        need[ord(c) - 97] += 1
    out = []
    for r, c in enumerate(s):
        have[ord(c) - 97] += 1
        if r >= k:
            have[ord(s[r - k]) - 97] -= 1
        if r >= k - 1 and have == need:
            out.append(r - k + 1)
    return out


def anagram_starts(s, p):
    # O(1) per step: 'diff' = number of letters whose counts differ
    k = len(p)
    if k > len(s):
        return []
    cnt = [0] * 26                      # cnt[x] = window count - needed count
    for c in p:
        cnt[ord(c) - 97] -= 1
    diff = sum(1 for v in cnt if v != 0)
    out = []

    def bump(idx, delta):
        nonlocal diff
        if cnt[idx] == 0:
            diff += 1                   # was equal, about to differ
        cnt[idx] += delta
        if cnt[idx] == 0:
            diff -= 1                   # became equal

    for r, c in enumerate(s):
        bump(ord(c) - 97, 1)
        if r >= k:
            bump(ord(s[r - k]) - 97, -1)
        if r >= k - 1 and diff == 0:
            out.append(r - k + 1)
    return out


print(anagram_starts("cbaebabacd", "abc"))
print(anagram_starts("abab", "ab"))
assert anagram_starts("cbaebabacd", "abc") == [0, 6]
assert anagram_starts("abab", "ab") == [0, 1, 2]
assert anagram_starts("a", "ab") == []                 # p longer than s
assert anagram_starts("aaaa", "aa") == [0, 1, 2]       # overlapping matches
assert anagram_starts("abc", "abc") == [0]
assert anagram_starts("abc", "d") == []
assert anagram_starts("a" * 30000, "a" * 30000) == [0]
assert anagram_starts_arrays("abab", "ab") == [0, 1, 2]

rng = random.Random(4)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 10)))
    p = "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
    want = anagram_starts_brute(s, p)
    assert anagram_starts(s, p) == want and anagram_starts_arrays(s, p) == want, (s, p)
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
[0, 6]
[0, 1, 2]
random cross-check passed: 3000 cases
```
Both prompt examples are correct.

**Edge cases:**
- `len(p) > len(s)`: empty list.
- Overlapping matches (`'aaaa'`, `'aa'`): `[0, 1, 2]`.
- No match: empty list.
- Equal lengths: at most one match.
- Length 3*10^4: linear.

**Follow-ups:**
- *Just a yes/no?* Q9, early exit.
- *Bigger alphabet?* Use a dict and delete keys that reach zero, tracking the count of non-zero keys.
- *Compare two arrays or use the counter?* Say both; the counter is O(1) per slide but the arrays are easier to get right.

**Common mistakes:**
- Removing `s[r-k+1]` instead of `s[r-k]`.
- Recording `r` instead of `r - k + 1`.
- Updating `diff` after changing the count rather than before.
- Not handling `len(p) > len(s)`.

### Q11 ⭐⭐⭐ 🟡 Longest repeating character replacement. Given an uppercase string `s` (1 <= len <= 10^5) and an integer k >= 0, you may replace at most k characters by any uppercase letter. Return the length of the longest substring that can become all one letter. Use a variable window with validity test 'window length - count of its most frequent letter <= k', and explain why the max-frequency value may be left stale (never decreased) without breaking the answer. Example: s='AABABBA', k=1 -> 4; s='ABAB', k=2 -> 4.
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports

**Pattern:** Variable sliding window with a validity test: a window is fixable if `length - (count of its most frequent letter) <= k`.

**Say this first (1 line):** "Keep the count of the most frequent letter in the window; if length minus that count exceeds k, slide the left edge one step. The answer is the final window length. O(n)."

**Brute force:** For every substring, count letters and test `length - max_count <= k`. O(n^2) with incremental counts (O(n^3) if you recount).

**Optimal:**
- `cnt[26]`, `left`, `max_f`.
- For each `r`: `cnt[s[r]] += 1`, `max_f = max(max_f, cnt[s[r]])`.
- If `(r - left + 1) - max_f > k`: remove `s[left]`, `left += 1`. This is a single `if`, not a `while`, so the window slides rather than shrinks.
- Return `len(s) - left` (the window size never decreases).
- Why `max_f` may go stale: the window only ever needs to grow to beat the best answer. To grow it needs a larger `max_f` than any earlier one, and `max_f` only increases when a truly larger count appears. A stale (too big) `max_f` can keep the window the same size but never makes it grow wrongly, so the length is never over-reported. Invariant: window length is the best length seen so far.

**Complexity:** Time O(n): `left` and `r` each move at most n times. Space O(26). A version recomputing `max(cnt)` is O(26 n), which I include as a check.

**Dry run:** `s = 'AABABBA'`, `k = 1`
| r | window | max_f | length - max_f | action |
|---|---|---|---|---|
| 0-2 | AAB | 2 | 1 | ok |
| 3 | AABA | 3 | 1 | ok, size 4 |
| 4 | AABAB (left=0) | 3 | 2 | invalid: left=1, size stays 4 |
| 5 | window grows to 5 first | 3 | 2 | invalid: left=2, size 4 |
| 6 | window grows to 5 first | 3 | 2 | invalid: left=3, size 4 |
Answer 4.

**Code:**
```python
import random
from collections import Counter


def replace_brute(s, k):
    best = 0
    for i in range(len(s)):
        cnt = Counter()
        for j in range(i, len(s)):
            cnt[s[j]] += 1
            if (j - i + 1) - max(cnt.values()) <= k:
                best = max(best, j - i + 1)
    return best


def replace_window(s, k):
    cnt = [0] * 26
    left = max_f = 0
    for r, c in enumerate(s):
        i = ord(c) - 65
        cnt[i] += 1
        max_f = max(max_f, cnt[i])          # stale: never lowered on shrink
        if (r - left + 1) - max_f > k:      # window invalid: slide by one (do not grow)
            cnt[ord(s[left]) - 65] -= 1
            left += 1
    return len(s) - left                    # window never shrinks in size once it grew


def replace_window_exact(s, k):
    # same idea but recomputes the real max each step (O(26 n)), to compare with the stale version
    cnt = [0] * 26
    left = best = 0
    for r, c in enumerate(s):
        cnt[ord(c) - 65] += 1
        while (r - left + 1) - max(cnt) > k:
            cnt[ord(s[left]) - 65] -= 1
            left += 1
        best = max(best, r - left + 1)
    return best


print(replace_window("AABABBA", 1))
print(replace_window("ABAB", 2))
assert replace_window("AABABBA", 1) == 4
assert replace_window("ABAB", 2) == 4
assert replace_window("A", 0) == 1
assert replace_window("ABC", 0) == 1                # k = 0: longest run
assert replace_window("AAAA", 0) == 4
assert replace_window("ABCD", 10) == 4              # k >= len: whole string
assert replace_window("AAAB" * 25000, 1) == replace_window_exact("AAAB" * 25000, 1)

rng = random.Random(12)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("ABC") for _ in range(rng.randint(1, 11)))
    k = rng.randint(0, 4)
    want = replace_brute(s, k)
    assert replace_window(s, k) == want, (s, k)
    assert replace_window_exact(s, k) == want, (s, k)
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
4
4
random cross-check passed: 3000 cases
```
Both prompt examples are correct. The stale and exact versions agree with the brute force on 3000 seeded cases.

**Edge cases:**
- `k = 0`: longest run of one letter.
- `k >= len(s)`: the whole string.
- One character: 1.
- All different letters: `k + 1` (capped at the length).

**Follow-ups:**
- *Why not recompute max_f on shrink?* Not needed, as above; it saves the 26 factor.
- *Lowercase and uppercase mixed?* A 128 or 256 sized array, or a Counter.
- *Return the substring?* Track the start where the window last grew.

**Common mistakes:**
- Using `while` with the stale `max_f`, which can shrink the window below the true best.
- Returning the last window length without understanding that it equals the best (it does, since the window never shrinks).
- Using `k` replacements per letter instead of in total.

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
- a[3]=3 > b[2]=2: j=3. a[3]=3 < b[3]=4: i=4. a[4]=4 == b[3]=4: out [2,2,4], i=5. Stop.
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

### Q20 ⭐⭐ 🟡 Valid palindrome II. Given a lowercase string `s` (len <= 10^5), decide whether it can become a palindrome by deleting at most one character. Walk two pointers inward; at the first mismatch try skipping the left or the right character and check the rest with plain palindrome checks. Say why trying both skips is enough and why the total is still O(n). Example: 'aba' -> True; 'abca' -> True; 'abc' -> False.
**Asked at:** Public pattern lists (NeetCode 150 style 'Two Pointers' and 'Sliding Window' sections as mirrored in a LeetCode discuss post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports

**Pattern:** Two pointers moving inward, with one allowed "repair" at the first mismatch. After the repair it is just two plain palindrome checks.

**Say this first (1 line):** I walk inward from both ends; at the first mismatch I try dropping the left character or the right one and check whether the rest is a palindrome, and the whole thing is O(n).

**Brute force:** Try deleting each index, build the string, test it: O(n) deletions times O(n) check = O(n^2) time and O(n) extra for each copy. Too slow at 10^5.

**Optimal:**
- `l = 0`, `r = n - 1`. While `l < r` and `s[l] == s[r]`, move inward.
- At the first mismatch return `is_pal(s, l+1, r) or is_pal(s, l, r-1)`.
- Why both skips are needed: we do not know which of the two mismatching characters is the "extra" one. `deeee` needs the left one removed; `eeeed` needs the right one.
- Why trying only these two is enough: any palindrome obtained by one deletion must delete either `s[l]` or `s[r]`. Deleting some other character leaves the same mismatched pair facing each other. The prefix and suffix already matched are unchanged.
- No deeper recursion: the "one deletion" budget is spent at the first mismatch, so the two checks are plain.

**Complexity:** Time O(n): the outer walk is at most n/2 steps, then at most two more scans of at most n characters. Space O(1) (indices only, no slicing).

**Dry run:** `'abca'`
- l=0 (a), r=3 (a): equal, l=1, r=2.
- l=1 (b), r=2 (c): mismatch.
- Skip left: check `s[2..2]` = 'c', a palindrome, so True. (Skip right would check 'b' as well.)
- Answer True (delete 'b' or 'c' gives 'aca' or 'aba').
- For `'abc'`: mismatch at l=0, r=2: skip left -> 'bc' not palindrome; skip right -> 'ab' not. False.

**Code:**
```python
import random

def brute(s):
    if s == s[::-1]:
        return True
    return any((t := s[:i] + s[i + 1:]) == t[::-1] for i in range(len(s)))

def is_pal(s, l, r):
    while l < r:
        if s[l] != s[r]:
            return False
        l += 1
        r -= 1
    return True

def optimal(s):
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            # one deletion allowed: skip the left char or the right char
            return is_pal(s, l + 1, r) or is_pal(s, l, r - 1)
        l += 1
        r -= 1
    return True

assert optimal('aba') is True
assert optimal('abca') is True
assert optimal('abc') is False
assert optimal('') is True
assert optimal('a') is True
assert optimal('ab') is True
assert optimal('abca') is True
assert optimal('deeee') is True            # delete the leading d
assert optimal('eeeed') is True            # delete the trailing d
assert optimal('abcdeba') is False

rng = random.Random(20)
for _ in range(1500):
    s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 9)))
    assert optimal(s) == brute(s), s
print("1500 random cases agree with brute force")
print(optimal('aba'), optimal('abca'), optimal('abc'))
# the greedy trap: only skipping one side is wrong
def left_only(s):
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return is_pal(s, l + 1, r)
        l += 1; r -= 1
    return True
print("skip-left-only on 'eeeed':", left_only('eeeed'), "(true answer True)")
```

**Output (my run):**
```
1500 random cases agree with brute force
True True False
skip-left-only on 'eeeed': False (true answer True)
```

**Edge cases:**
- Already a palindrome: zero deletions is within "at most one", so True.
- Empty or single character: True.
- Two characters: always True (delete one).
- Mismatch at the very ends (`deeee`, `eeeed`): both skips matter.
- A string that needs two deletions: False.

**Follow-ups:**
- *At most k deletions?* Then it becomes DP (longest palindromic subsequence, n - LPS <= k), Part 11.
- *Why not slice and compare?* Slicing copies, O(n) each; index-based check keeps O(1) space.
- *Return the index to delete?* Return which skip worked.

**Common mistakes:**
- Trying only the left skip (the demo above shows the wrong answer for `'eeeed'`).
- Using `s[l+1:r+1]` slices inside the helper, which is correct but hides copying cost.
- Recursing with a counter and re-entering the mismatch loop, which can blow up if not limited to one deletion.
- Off-by-one in the helper bounds (`l+1..r` versus `l..r-1`, both inclusive).

---

### Q21 ⭐⭐ 🟡 Remove duplicates from a sorted array, allowing at most two copies. `nums` is sorted non-decreasing. Rewrite it in place so each value appears at most twice, keep the order, and return the new length k; only the first k slots matter. Use a write pointer and compare with the element two slots behind the write position, and say how this generalises to 'at most m copies'. (Part 1 Q6 covers the keep-one version.) Example: [1,1,1,2,2,3] -> k=5, first 5 slots [1,1,2,2,3]; [0,0,1,1,1,1,2,3,3] -> k=7, first 7 slots [0,0,1,1,2,3,3].
**Asked at:** Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports | Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Indian online-assessment style prep (a search for TCS NQT, Infosys and Wipro sliding-window questions returned only generic guides, nothing company-specific; the fixed-window max-sum and 'longest subarray with sum <= k' tasks are the typical easy-tier shape in such sheets; indicative only, no company attribution)

**Pattern:** Read pointer and write pointer (fast and slow) over a sorted array, in place. Sortedness puts equal values side by side, so "how many copies have I kept" can be read off one slot behind the write head.

**Say this first (1 line):** I scan once with a write index `k`, and I keep a value only if fewer than two items are kept yet or it differs from the value two slots behind the write position.

**Brute force:** Build a new list, keeping a value only if its count in the output is below two (`out.count(v)` each time is O(n), so O(n^2)), or a Counter for O(n) time and O(n) space. The prompt wants it in place.

**Optimal:**
- `k = 0` is the next write slot. For each value `x` in order:
  - If `k < 2` or `x != nums[k - 2]`: write `nums[k] = x`, `k += 1`.
  - Otherwise skip it.
- Why compare with `nums[k-2]` (the output, not the input): the first `k` slots already hold the result so far, sorted. If `x == nums[k-2]` then, because the output is sorted and `x` is not smaller than anything in it, `nums[k-2] == nums[k-1] == x`: two copies are already kept, so `x` would be a third.
- Generalising to at most `m` copies: `if k < m or x != nums[k - m]`. `m = 1` is the keep-one version in Part 1 Q6.
- Only the first `k` slots matter; the tail is garbage and the caller must not read it.

**Complexity:** Time O(n): one pass. Space O(1): one index.

**Dry run:** `[1,1,1,2,2,3]`, `m = 2`
- x=1: k=0 < 2, write, k=1. x=1: k=1 < 2, write, k=2.
- x=1: k=2, `nums[0]=1 == x`, skip.
- x=2: `nums[0]=1 != 2`, write at 2, k=3. x=2: `nums[1]=1 != 2`, write, k=4.
- x=3: `nums[2]=2 != 3`, write, k=5.
- Result k=5, first 5 slots `[1,1,2,2,3]`.

**Code:**
```python
import random

def brute(nums, m=2):
    out = []
    for v in nums:
        if out.count(v) < m:        # keeps first m copies; O(n) count per element
            out.append(v)
    return len(out), out

def optimal(nums, m=2):
    k = 0                                    # write position
    for x in nums:
        if k < m or x != nums[k - m]:        # compare with the slot m behind the write head
            nums[k] = x
            k += 1
    return k

def run(a, m=2):
    b = list(a)
    k = optimal(b, m)
    return k, b[:k]

assert run([1, 1, 1, 2, 2, 3]) == (5, [1, 1, 2, 2, 3])
assert run([0, 0, 1, 1, 1, 1, 2, 3, 3]) == (7, [0, 0, 1, 1, 2, 3, 3])
assert run([]) == (0, [])
assert run([7]) == (1, [7])
assert run([5, 5, 5, 5, 5]) == (2, [5, 5])
assert run([1, 2, 3]) == (3, [1, 2, 3])
assert run([-1, -1, -1, 0, 0, 0]) == (4, [-1, -1, 0, 0])
assert run([1, 1, 1, 2, 2, 3], m=1) == (3, [1, 2, 3])        # generalises to m = 1
assert run([1, 1, 1, 1, 2], m=3) == (4, [1, 1, 1, 2])         # and m = 3

rng = random.Random(21)
for _ in range(1000):
    a = sorted(rng.randint(-3, 3) for _ in range(rng.randint(0, 12)))
    for m in (1, 2, 3):
        assert run(a, m) == brute(a, m), (a, m)
print("1000 random sorted lists, m in (1, 2, 3): agree with brute force")
print(run([1, 1, 1, 2, 2, 3]), run([0, 0, 1, 1, 1, 1, 2, 3, 3]))
```

**Output (my run):**
```
1000 random sorted lists, m in (1, 2, 3): agree with brute force
(5, [1, 1, 2, 2, 3]) (7, [0, 0, 1, 1, 2, 3, 3])
```

**Edge cases:**
- Empty list: return 0.
- Length one or two: everything kept.
- All equal: keep exactly `m` of them.
- No duplicates: nothing skipped.
- Negatives: no issue (compare by equality only).
- Unsorted input breaks the logic; the problem guarantees sorted.

**Follow-ups:**
- *At most m copies?* Replace 2 with m, as above (tested for m = 1 and 3).
- *Can it be unsorted?* Then use a Counter and a write pointer, O(n) space.
- *Why compare against the output slot, not the input?* The input slot `nums[i-2]` may have been overwritten. Comparing with `nums[k-2]` uses the result built so far, which is always valid.

**Common mistakes:**
- Mixing up the read index `i` and the write index `k`: the check is against `nums[k - 2]`.
- Returning the list instead of the length, or reading past `k`.
- Starting the check at index 2 but leaving `k` at 0.

---

### Q22 ⭐⭐ 🟡 Backspace string compare in O(1) space. Two strings `s` and `t` consist of lowercase letters and '#', where '#' deletes the previous typed character (it does nothing on an empty text). Decide whether the final texts are equal without building the two results, by scanning both strings from the right with a skip counter. Example: s='ab#c', t='ad#c' -> True (both 'ac'); s='a#c', t='b' -> False; s='a##c', t='#a#c' -> True (both 'c').
**Asked at:** Standard-problem lists and solution sites (Educative and Grokking-style pattern courses, algo.monster and similar solution libraries; search snippets only, not opened); problem lists, not verified company reports | Pattern guides (techinterview.org two-pointer and sliding-window guides, a LeetCode discuss 'Summary of Sliding Window Patterns' post and a '10 Variations of Two Pointers' post, Hello Interview two-pointers page; search snippets only, not opened); prep content, not company reports

**Pattern:** Two pointers scanning from the right with a skip counter. A '#' only affects characters to its left, so processing right to left tells us at once whether a letter is erased.

**Say this first (1 line):** Scanning right to left, a '#' adds one to a skip counter and each letter either consumes a skip (it is erased) or survives; I advance both strings to their next surviving letter and compare, using O(1) extra space.

**Brute force:** Build both final texts with a stack (push letters, pop on '#', ignore '#' on empty), then compare. O(n + m) time, O(n + m) space. Correct, and it is the checker in the code.

**Optimal:**
- Helper `next_valid(x, i)`: `skip = 0`; walk `i` leftwards. On '#': `skip += 1`. On a letter: if `skip > 0`, `skip -= 1` (erased), else return `i` (it survives). Return -1 when we run off the start.
- Main loop: `i = len(s) - 1`, `j = len(t) - 1`. Find the next surviving index in each. Both -1: equal, True. Exactly one -1: different lengths, False. Different letters: False. Else step both left and repeat.
- Each string is scanned once, right to left, so the skip counter state never has to be shared.

**Complexity:** Time O(n + m): every index of each string is visited once (the helper resumes from where it stopped, because `i` is moved past the returned index). Space O(1): a few integers.

**Dry run:** `s='ab#c'`, `t='ad#c'`
- s: from i=3, 'c' survives, index 3. t: from j=3, 'c', index 3. Equal. Step to i=2, j=2.
- s: i=2 is '#', skip 1; i=1 'b' erased (skip 0); i=0 'a' survives, index 0. t: '#', 'd' erased, 'a' survives, index 0. Equal. Step to -1, -1.
- Both exhausted: True (both texts are `ac`).
- For `'a#c'` vs `'b'`: s gives 'c', t gives 'b', not equal: False.

**Code:**
```python
import random

def brute(s, t):
    def build(x):
        st = []
        for ch in x:
            if ch == '#':
                if st:
                    st.pop()
            else:
                st.append(ch)
        return st
    return build(s) == build(t)

def next_valid(x, i):
    """Index of the next surviving character at or left of i, or -1."""
    skip = 0
    while i >= 0:
        if x[i] == '#':
            skip += 1
        elif skip > 0:
            skip -= 1          # this letter is erased by a later '#'
        else:
            return i           # a surviving letter
        i -= 1
    return -1

def optimal(s, t):
    i, j = len(s) - 1, len(t) - 1
    while True:
        i = next_valid(s, i)
        j = next_valid(t, j)
        if i < 0 and j < 0:
            return True
        if i < 0 or j < 0:
            return False
        if s[i] != t[j]:
            return False
        i -= 1
        j -= 1

assert optimal('ab#c', 'ad#c') is True
assert optimal('a#c', 'b') is False
assert optimal('a##c', '#a#c') is True
assert optimal('', '') is True
assert optimal('#', '') is True
assert optimal('###', 'a#') is True
assert optimal('a', 'a#') is False
assert optimal('ab', 'a') is False           # different lengths after deletion
assert optimal('abc', 'abc') is True
assert optimal('bxj##tw', 'bxj###tw') is False
assert optimal('xy#z', 'xzz#') is True

rng = random.Random(22)
for _ in range(2000):
    s = ''.join(rng.choice('ab#') for _ in range(rng.randint(0, 9)))
    t = ''.join(rng.choice('ab#') for _ in range(rng.randint(0, 9)))
    assert optimal(s, t) == brute(s, t), (s, t)
print("2000 random cases agree with the stack brute force")
print(optimal('ab#c', 'ad#c'), optimal('a#c', 'b'), optimal('a##c', '#a#c'))
```

**Output (my run):**
```
2000 random cases agree with the stack brute force
True False True
```

**Edge cases:**
- '#' on empty text does nothing: leading `#` characters are skipped with a skip count that never meets a letter (`'###'` equals `''`).
- All characters erased on one side: that side returns -1 first, the other must also be -1.
- Extra '#' beyond the letters (`'a##c'` vs `'#a#c'`) both reduce to `'c'`.
- Equal raw strings: True quickly.
- Empty strings: True.

**Follow-ups:**
- *Why not scan left to right?* A letter's fate depends on later '#' characters, so you would need a stack, which is O(n) space.
- *Same trick elsewhere?* Any "later marker cancels earlier item" problem, such as removing adjacent pairs (Part 4 stack family) when the structure is simple.
- *Cursor keys, not just backspace?* Then the right-to-left skip counter no longer works; use a stack or a gap structure.

**Common mistakes:**
- Treating each '#' as deleting exactly one letter when the previous character is also '#': the counter must accumulate.
- Not resetting `skip` between the two strings or between helper calls (it is local to the helper).
- Comparing characters without first moving both pointers to survivors.
- Returning False when only one side is exhausted but not checking the other for a survivor.

---

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


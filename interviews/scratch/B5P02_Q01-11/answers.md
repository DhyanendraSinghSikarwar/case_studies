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

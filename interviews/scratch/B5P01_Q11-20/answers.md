### Q11 ⭐⭐⭐ 🟡 Product of array except self. For each index i return the product of all other elements without using division and in O(n) time; extra space beyond the output list should be O(1). Handle zeros. Example: [1,2,3,4] -> [24,12,8,6]; [-1,1,0,-3,3] -> [0,0,9,0,0].
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Prefix and suffix products (two passes). The answer for i is "everything left of i" times "everything right of i". No division needed, so zeros are harmless.

**Say this first (1 line):** One left-to-right pass writes the product of everything before each index into the output; one right-to-left pass multiplies in the product of everything after, using a single running variable.

**Brute force:** For each i, multiply all other elements. O(n^2) time, O(1) extra. Too slow for large n.

**Optimal:**
- Pass 1: `out[i] = product of nums[0..i-1]`. Keep a running `left`, start at 1.
- Pass 2 from the right: `out[i] *= product of nums[i+1..]`. Keep a running `right`, start at 1.
- The output list does not count as extra space, so this is O(1) extra.
- Division approach (total product / nums[i]) is banned, and it breaks on zeros anyway.
- Zeros need no special case: a zero lands inside `left` or `right` for every other index and zeroes them. The index of the zero itself gets the product of the rest.

**Complexity:** Time O(n): two passes. Extra space O(1) beyond the output: two scalars. (The brute force is O(n^2).)

**Dry run:** `[1,2,3,4]`
- Pass 1 (left products): out = [1, 1, 2, 6].
- Pass 2 (right running value 1, then 4, 12, 24): i=3: 6*1=6, right=4. i=2: 2*4=8, right=12. i=1: 1*12=12, right=24. i=0: 1*24=24.
- Result [24, 12, 8, 6].

**Code:**
```python
import random
from math import prod

def brute(nums):
    return [prod(nums[:i] + nums[i + 1:]) for i in range(len(nums))]

def optimal(nums):
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):          # out[i] = product of everything left of i
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):   # multiply in product of everything right of i
        out[i] *= right
        right *= nums[i]
    return out

assert optimal([1, 2, 3, 4]) == [24, 12, 8, 6]
assert optimal([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
assert optimal([0, 0, 2]) == [0, 0, 0]
assert optimal([5]) == [1]          # empty product is 1
assert optimal([2, 3]) == [3, 2]
assert optimal([0, 4]) == [4, 0]
assert optimal([]) == []

rng = random.Random(11)
for _ in range(500):
    a = [rng.randint(-4, 4) for _ in range(rng.randint(0, 8))]
    assert optimal(a) == brute(a), a
print("500 random cases agree with brute force")
print(optimal([1, 2, 3, 4]), optimal([-1, 1, 0, -3, 3]), optimal([0, 0, 2]), optimal([5]))
```

**Output (my run):**
```
500 random cases agree with brute force
[24, 12, 8, 6] [0, 0, 9, 0, 0] [0, 0, 0] [1]
```

**Edge cases:**
- Single element: answer is `[1]` (empty product). Say it out loud.
- One zero: only that index is non-zero. Two or more zeros: everything is 0 (`[0,0,2]` gives all zeros).
- Negatives: sign handled naturally by multiplication.
- Large values: Python ints do not overflow. In fixed-width languages mention overflow.

**Follow-ups:**
- *Why not division?* Banned by the prompt, and zeros make it fail. You would need to count zeros separately.
- *Can you do it with prefix and suffix arrays?* Yes, simpler to explain but O(n) extra. The running-variable version removes it.
- *What if only a modulus of the product is wanted?* Same two passes with `% m`; division would need a modular inverse and fails for zero residues.

**Common mistakes:**
- Updating `left` before writing `out[i]` (off by one: includes nums[i]).
- Starting the running products at 0 instead of 1.
- Using the total product divided by nums[i] and crashing on zero.
- Claiming O(1) space but allocating separate prefix and suffix lists.

---

### Q12 ⭐⭐⭐ 🟡 Longest consecutive sequence. Given an unsorted list of integers, return the length of the longest run of values that are consecutive integers (x, x+1, x+2, ...), regardless of position, in O(n) expected time. Explain why starting only from values whose predecessor is absent keeps it linear. Example: [100,4,200,1,3,2] -> 4 (the run 1,2,3,4); [0,3,7,2,5,8,4,6,0,1] -> 9.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Hash set membership. A set gives O(1) "is x present", so you can walk a run without sorting. The trick is to start walks only at run starts.

**Say this first (1 line):** Put everything in a set; for each value whose predecessor x-1 is not in the set, count upward x+1, x+2 while present; each run is walked once, so it is linear.

**Brute force:**
- Sort and scan, tracking the current run: O(n log n).
- Or from every value walk upward in a set: O(n) per start, O(n^2) worst case (for a fully consecutive list, every start re-walks its tail).

**Optimal:**
- Build `s = set(nums)`. Duplicates vanish.
- For each x in s: if `x-1 in s`, skip. It is inside a run that another value will start.
- Otherwise x is a run start. Walk `x+1, x+2, ...` while in s. Length = end - x.
- Why linear: a value is walked over only as part of the run whose start is unique, since every run has exactly one start. Total inner-loop steps across all starts is at most the number of distinct values. Outer loop is n. Total O(n) expected (hash lookups are O(1) on average).

**Complexity:** Time O(n) expected: set build n, outer loop n, inner steps sum to at most n. Space O(n) for the set. Sorting alternative is O(n log n) time, O(1) to O(n) space depending on whether you may modify the input.

**Dry run:** `[100,4,200,1,3,2]`, set = {100,4,200,1,3,2}.
- 100: 99 absent, start. 101 absent, length 1.
- 4: 3 present, skip.
- 200: 199 absent, start, length 1.
- 1: 0 absent, start. 2,3,4 present, 5 absent. Length 4.
- 3 and 2: predecessor present, skip.
- Answer 4.

**Code:**
```python
import random

def brute(nums):
    s = set(nums)
    best = 0
    for x in s:                      # try every value as a start, walk up
        y = x
        while y in s:
            y += 1
        best = max(best, y - x)
    return best

def optimal(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 in s:               # not a run start, skip
            continue
        y = x + 1
        while y in s:
            y += 1
        best = max(best, y - x)
    return best

assert optimal([100, 4, 200, 1, 3, 2]) == 4
assert optimal([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert optimal([]) == 0
assert optimal([7]) == 1
assert optimal([5, 5, 5]) == 1
assert optimal([-2, -1, 0, 1]) == 4
assert optimal([10**9, -10**9]) == 1
assert optimal([1, 3, 5, 7]) == 1
assert optimal(list(range(100000))) == 100000

rng = random.Random(12)
for _ in range(500):
    a = [rng.randint(-10, 10) for _ in range(rng.randint(0, 15))]
    assert optimal(a) == brute(a), a
# independent oracle: sort and scan
def by_sort(nums):
    u = sorted(set(nums))
    best = cur = 0
    for i, v in enumerate(u):
        cur = cur + 1 if i and v == u[i - 1] + 1 else 1
        best = max(best, cur)
    return best
for _ in range(500):
    a = [rng.randint(-10, 10) for _ in range(rng.randint(0, 15))]
    assert optimal(a) == by_sort(a)
print("1000 random cases agree")
print(optimal([100, 4, 200, 1, 3, 2]), optimal([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))
```

**Output (my run):**
```
1000 random cases agree
4 9
```

**Edge cases:**
- Empty list gives 0. Single value gives 1.
- Duplicates must not inflate the count (`[5,5,5]` is 1). The set handles it.
- Negatives and large values (`-2..1` is length 4; 10^9 and -10^9 are not consecutive).
- Iterate over the set, not the list, so a list with many duplicates does not repeat work.

**Follow-ups:**
- *Union-find version?* Union x with x+1 if present and track the biggest component. Also near-linear, more code.
- *Why is the skip check enough?* Each maximal run has exactly one element with no predecessor.
- *Worst-case hash behaviour?* Expected O(n) assumes a decent hash spread; with many colliding keys a set degrades toward O(n) per lookup. Mention it, do not dwell on it.

**Common mistakes:**
- Skipping the predecessor check: it still passes small tests but is O(n^2) on a long run. Tell the interviewer you know this.
- Looping over `nums` with duplicates and re-walking.
- Sorting and forgetting to de-duplicate (a repeat resets or double-counts the run).
- Returning the largest value in the run rather than its length.

---

### Q13 ⭐⭐⭐ 🟡 Subarray sum equals k. Given integers `nums` (negatives allowed, len up to 2*10^4) and an integer k, count the contiguous subarrays whose sum is exactly k. Use prefix sums with a hashmap of how many times each prefix has occurred and explain why a sliding window fails with negatives. Example: nums=[1,1,1], k=2 -> 2; nums=[1,2,3], k=3 -> 2.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Prefix sum plus hashmap of counts. Subarray `(i, j]` sums to k exactly when `prefix[j] - prefix[i] = k`.

**Say this first (1 line):** Keep a running prefix sum and a dict of how many times each prefix has occurred; at every position add `seen[prefix - k]` to the answer, then record the current prefix.

**Brute force:** Two loops over start and end with a running sum. O(n^2) time, O(1) space. With n up to 2*10^4 that is about 2*10^8 steps, too slow in Python.

**Optimal:**
- Seed `seen[0] = 1`: the empty prefix, so subarrays that start at index 0 are counted.
- For each x: `pref += x`; `ans += seen[pref - k]`; then `seen[pref] += 1`.
- Look up before inserting, so a subarray of length zero is never counted (matters when k = 0).
- Why a count and not a set: several earlier starts can share a prefix value and each is a different subarray.
- Why sliding window fails with negatives: it assumes extending the window only increases the sum and shrinking only decreases it. With negatives that is false, so you cannot decide whether to move the left or the right edge. Example below: `[1,-1,1]`, k=1.

**Complexity:** Time O(n): one pass, average O(1) dict operations. Space O(n) for the dict in the worst case (all prefixes distinct).

**Dry run:** `[1,2,3]`, k=3. seen={0:1}, pref=0, ans=0.
- x=1: pref=1, seen[-2]=0, ans=0. seen={0:1,1:1}.
- x=2: pref=3, seen[0]=1, ans=1 (that is [1,2]). seen has 3:1.
- x=3: pref=6, seen[3]=1, ans=2 (that is [3]). Answer 2.

**Code:**
```python
import random
from collections import defaultdict

def brute(nums, k):
    n, cnt = len(nums), 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s == k:
                cnt += 1
    return cnt

def optimal(nums, k):
    seen = defaultdict(int)
    seen[0] = 1                      # empty prefix
    pref = cnt = 0
    for x in nums:
        pref += x
        cnt += seen[pref - k]        # look up BEFORE inserting current prefix
        seen[pref] += 1
    return cnt

def sliding_window_wrong(nums, k):   # valid only for non-negative values
    lo = s = cnt = 0
    for hi, x in enumerate(nums):
        s += x
        while s > k and lo <= hi:
            s -= nums[lo]; lo += 1
        if s == k:
            cnt += 1
    return cnt

assert optimal([1, 1, 1], 2) == 2
assert optimal([1, 2, 3], 3) == 2
assert optimal([], 0) == 0
assert optimal([0, 0, 0], 0) == 6          # all subarrays of zeros
assert optimal([1, -1, 0], 0) == 3
assert optimal([5], 5) == 1
assert optimal([-1, -1, 1], 0) == 1
assert optimal([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4

rng = random.Random(13)
for _ in range(500):
    a = [rng.randint(-3, 3) for _ in range(rng.randint(0, 10))]
    k = rng.randint(-4, 4)
    assert optimal(a, k) == brute(a, k), (a, k)
print("500 random cases agree with brute force")
print("sliding window on [1,-1,1], k=1:", sliding_window_wrong([1, -1, 1], 1), "but truth is", optimal([1, -1, 1], 1))
print(optimal([1, 1, 1], 2), optimal([1, 2, 3], 3))
```

**Output (my run):**
```
500 random cases agree with brute force
sliding window on [1,-1,1], k=1: 2 but truth is 3
2 2
```

**Edge cases:**
- Empty list: 0 (even for k = 0, no non-empty subarray).
- All zeros with k = 0: n(n+1)/2 subarrays, `[0,0,0]` gives 6. Needs the count dict, not a set.
- Negative k and negative values are fine.
- Single element equal to k.

**Follow-ups:**
- *Non-negative values only?* A sliding window works in O(1) space. State why it relies on monotonic sums.
- *Return the longest such subarray?* Store the first index of each prefix instead of a count.
- *Why defaultdict reads are safe here?* Reading `seen[pref-k]` inserts a zero entry in a defaultdict. It does not change the answer, but it grows memory; `seen.get(pref-k, 0)` avoids it.

**Common mistakes:**
- Forgetting `seen[0] = 1`.
- Inserting the current prefix before the lookup (breaks k = 0).
- Using a set, which loses multiplicities.
- Trying sliding window with negatives.

---

### Q14 ⭐⭐⭐ 🟡 Rotate array in place. Rotate `nums` to the right by k steps (k can exceed len) using O(1) extra space. Give the three-reversal method, state why k must be reduced modulo n, and mention the slice-assignment one-liner and its extra space. Example: nums=[1,2,3,4,5,6,7], k=3 -> [5,6,7,1,2,3,4].
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only) | Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** In-place array transformation by reversal. Rotating right by k is the same as reverse all, reverse the first k, reverse the rest.

**Say this first (1 line):** Reduce k modulo n, then reverse the whole list, reverse the first k items, reverse the remaining n-k: O(n) time, O(1) extra space.

**Brute force:** Rotate by one step k times (pop the last, insert at front): O(n*k) time. Or copy into a new list at index `(i+k) % n`: O(n) time but O(n) space.

**Optimal:**
- `k %= n`. Rotating by n returns the original list, so only k mod n matters; this also stops k > n from indexing out of range, and avoids pointless work when k is huge.
- Reverse everything: `[1..7]` becomes `[7,6,5,4,3,2,1]`.
- Reverse positions 0..k-1: `[5,6,7,4,3,2,1]`. Reverse positions k..n-1: `[5,6,7,1,2,3,4]`.
- Why it works: the last k items must go to the front in their original order. The full reversal puts them in front but backwards; the second reversal fixes their order, the third fixes the rest.
- Guard n = 0 before the modulo (modulo by zero raises ZeroDivisionError).

**Complexity:** Time O(n): every element is swapped a constant number of times (about 2 writes each). Space O(1): two indices. Slice one-liner `nums[:] = nums[-k:] + nums[:-k]` is also O(n) time but builds temporary lists, so O(n) extra space; and the `nums[:] =` part matters, because `nums = ...` rebinds the local name and does not change the caller's list.

**Dry run:** `[1,2,3,4,5,6,7]`, k=3.
- Reverse all: [7,6,5,4,3,2,1].
- Reverse first 3: [5,6,7,4,3,2,1].
- Reverse last 4: [5,6,7,1,2,3,4].

**Code:**
```python
import random

def brute(nums, k):
    n = len(nums)
    if n == 0:
        return []
    k %= n
    out = nums[:]
    for _ in range(k):               # rotate one step at a time
        out.insert(0, out.pop())
    return out

def rev(a, i, j):
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1; j -= 1

def optimal(nums, k):                # in place, returns the same list
    n = len(nums)
    if n == 0:
        return nums
    k %= n
    rev(nums, 0, n - 1)
    rev(nums, 0, k - 1)
    rev(nums, k, n - 1)
    return nums

def slice_version(nums, k):          # builds a temp copy: O(n) extra space
    n = len(nums)
    if n:
        k %= n
        nums[:] = nums[-k:] + nums[:-k] if k else nums[:]
    return nums

a = [1, 2, 3, 4, 5, 6, 7]
assert optimal(a, 3) == [5, 6, 7, 1, 2, 3, 4]
assert optimal([1, 2], 5) == [2, 1]          # k > n
assert optimal([1, 2, 3], 3) == [1, 2, 3]    # k == n
assert optimal([1, 2, 3], 0) == [1, 2, 3]
assert optimal([], 4) == []
assert optimal([9], 100) == [9]
assert slice_version([1, 2, 3, 4, 5, 6, 7], 3) == [5, 6, 7, 1, 2, 3, 4]
# the classic bug: nums[-k:] when k == 0 returns the WHOLE list
print("nums[-0:] =", [1, 2, 3][-0:], "so the k == 0 guard matters")

rng = random.Random(14)
for _ in range(500):
    arr = [rng.randint(0, 9) for _ in range(rng.randint(0, 9))]
    k = rng.randint(0, 25)
    assert optimal(arr[:], k) == brute(arr, k) == slice_version(arr[:], k), (arr, k)
print("500 random cases agree")
print(optimal([1, 2, 3, 4, 5, 6, 7], 3))
```

**Output (my run):**
```
nums[-0:] = [1, 2, 3] so the k == 0 guard matters
500 random cases agree
[5, 6, 7, 1, 2, 3, 4]
```

**Edge cases:**
- k = 0, k = n, k a multiple of n: list unchanged.
- k > n (`[1,2]`, k=5 gives `[2,1]`).
- Empty and single-element list.
- The slice trap: `nums[-0:]` is the whole list, so slice code needs a guard for `k == 0` (shown in the run).

**Follow-ups:**
- *Rotate left instead?* Reverse the first k, reverse the rest, reverse all. Or use `k = n - k % n`.
- *Cycle-leader method?* Move elements along gcd(n,k) cycles, one write per element, also O(1) space.
- *Use `collections.deque.rotate`?* Fine if the data lives in a deque already; O(k).

**Common mistakes:**
- Skipping `k %= n`.
- Returning a new list when the prompt says in place.
- Off-by-one on the reversal boundaries (k-1 and k).
- `nums = nums[-k:] + nums[:-k]` which does not mutate the caller's list.

---

### Q15 ⭐⭐⭐ 🟡 Valid Sudoku. Given a 9x9 board of characters (digits 1-9 or '.' for empty), decide whether the filled cells so far break no rule: no repeated digit in any row, column or 3x3 box (you do not have to solve it). Show how to key sets by (row), (col) and (row//3, col//3) in one pass. Example: a board with two '5' in the first row -> False.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports

**Pattern:** Set-per-group membership in one pass. A cell is a clash if its digit is already in its row set, column set or box set.

**Say this first (1 line):** Walk the 81 cells once, keep 9 row sets, 9 column sets and a dict of box sets keyed by `(r//3, c//3)`, and return False the moment a digit is already in any of its three sets.

**Brute force:** For each of 9 rows, 9 columns and 9 boxes extract the cells and compare `len(digits)` to `len(set(digits))`. Three separate sweeps, 243 cell reads. Also correct and still O(1) because the board is fixed at 81 cells.

**Optimal:**
- Skip '.' cells.
- Box key `(r // 3, c // 3)` maps the 9 cells of a 3x3 box to one key (or use `r//3*3 + c//3`).
- Check all three sets before adding, then add to all three.
- The board size is fixed, so the time is O(81) = O(1); for an N x N generalisation it is O(N^2) time and O(N^2) space.
- You are only validating the filled cells; a valid board may still be unsolvable.

**Complexity:** Time O(81), constant (O(N^2) for the general board). Space O(81) for the sets, constant.

**Dry run:** Take the classic puzzle row 0 `5 3 . . 7 . . . .` then change cell (0,2) to '5'.
- (0,0)='5': row0={5}, col0={5}, box(0,0)={5}.
- (0,1)='3': added to its sets.
- (0,2)='5': `'5' in rows[0]` is True, return False.

**Code:**
```python
import random

def brute(board):
    def ok(cells):
        d = [c for c in cells if c != '.']
        return len(d) == len(set(d))
    for i in range(9):
        if not ok(board[i]) or not ok([board[r][i] for r in range(9)]):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            if not ok([board[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)]):
                return False
    return True

def optimal(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = {}
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == '.':
                continue
            b = boxes.setdefault((r // 3, c // 3), set())
            if v in rows[r] or v in cols[c] or v in b:
                return False
            rows[r].add(v); cols[c].add(v); b.add(v)
    return True

base = ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
        "7...2...6", ".6....28.", "...419..5", "....8..79"]
good = [list(r) for r in base]
assert optimal(good) and brute(good)

bad_row = [list(r) for r in base]; bad_row[0][2] = '5'          # two 5s in row 0
bad_col = [list(r) for r in base]; bad_col[8][0] = '5'          # 5 twice in col 0
assert not optimal(bad_row) and not optimal(bad_col)
empty = [['.'] * 9 for _ in range(9)]
assert optimal(empty)

# the example in the prompt: a board with two '5' in the first row
assert optimal(bad_row) is False
# ok-looking trap: a rows-and-cols-only check misses a box clash
box_only = [['.'] * 9 for _ in range(9)]
box_only[0][0] = '7'; box_only[1][1] = '7'
assert optimal(box_only) is False

rng = random.Random(15)
agree = 0
for _ in range(500):
    b = [['.'] * 9 for _ in range(9)]
    for _ in range(rng.randint(0, 30)):
        b[rng.randrange(9)][rng.randrange(9)] = str(rng.randint(1, 9))
    assert optimal(b) == brute(b)
    agree += 1
print(agree, "random boards agree with brute force")
print(optimal(good), optimal(bad_row), optimal(bad_col), optimal(box_only))
```

**Output (my run):**
```
500 random boards agree with brute force
True False False False
```

**Edge cases:**
- All empty board is valid.
- Clash only inside a box (two 7s at (0,0) and (1,1)), which a rows-and-columns-only check misses.
- A clash only in a column.
- Digits are characters, so `'5'` and `5` differ if you mix types.

**Follow-ups:**
- *Solve it?* Backtracking with the same three structures, usually with bitmasks per row, column and box (Book 5 backtracking part).
- *Use bitmasks?* One integer per group, `mask & (1 << d)`; faster, less readable.
- *Why not one set of tuples?* Store `(row, d)`, `(col, d)`, `(box, d)` in one set; it works and is a neat single-set trick.

**Common mistakes:**
- Wrong box key (`r//3 + c//3` collides: (0,3) and (3,0) both give 1).
- Treating '.' as a digit and reporting duplicate dots.
- Checking only rows and columns.
- Believing a valid board is solvable.

---

### Q16 ⭐⭐⭐ 🔴 First missing positive. Given an unsorted integer list (negatives and duplicates allowed), return the smallest positive integer that is not in it, in O(n) time and O(1) extra space beyond the input (you may modify it). Explain the answer is in 1..n+1 and the place-each-value-at-its-own-index trick. Example: [3,4,-1,1] -> 2; [1,2,0] -> 3; [7,8,9,11,12] -> 1.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Index as hash (cyclic placement). Use the array itself as the "set" of which small positive values are present.

**Say this first (1 line):** The answer is always in 1..n+1, so swap each value v in 1..n into slot v-1, then the first slot i where `nums[i] != i+1` gives answer i+1; if none, answer n+1.

**Brute force:**
- Put everything in a set, then test 1, 2, 3, ... until one is missing: O(n) time, O(n) space (this is the easy, standard answer and is fine if extra space is allowed).
- Sort and scan for the first gap above zero: O(n log n).

**Optimal:**
- Why 1..n+1: n values can fill at most 1..n. If they are exactly 1..n the answer is n+1; otherwise some value in 1..n is missing and the smallest missing is at most n. Anything <= 0 or > n can be ignored.
- Loop i from 0. While `nums[i]` is in 1..n and the slot it belongs in does not already hold it, swap it home: `j = nums[i]-1; swap(nums[i], nums[j])`.
- The condition `nums[j] != nums[i]` is what stops infinite loops on duplicates.
- Then scan for the first `nums[i] != i+1`.
- Each swap puts at least one value in its final slot, so there are at most n swaps in total. The inner `while` looks nested but is amortised O(n).

**Complexity:** Time O(n): at most n successful swaps plus two scans. Space O(1) extra (it modifies the input, which the prompt allows).

**Dry run:** `[3,4,-1,1]` (n=4). Output below shows it.
- i=0: 3 goes to slot 2: [-1,4,3,1]. -1 is out of range, stop.
- i=1: 4 goes to slot 3: [-1,1,3,4]. Now 1 goes to slot 0: [1,-1,3,4]. -1 stops.
- i=2, i=3: already home.
- Scan: slot 1 holds -1, not 2, so the answer is 2.

**Code:**
```python
import random

def brute(nums):
    s = set(nums)
    i = 1
    while i in s:
        i += 1
    return i

def optimal(nums):                    # modifies nums; O(1) extra space
    n = len(nums)
    for i in range(n):
        # keep swapping until slot i holds a value that cannot go home
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1

assert optimal([3, 4, -1, 1]) == 2
assert optimal([1, 2, 0]) == 3
assert optimal([7, 8, 9, 11, 12]) == 1
assert optimal([]) == 1
assert optimal([1]) == 2
assert optimal([2]) == 1
assert optimal([1, 1]) == 2              # duplicates must not loop forever
assert optimal([2, 2, 2, 2]) == 1
assert optimal([-5, 0]) == 1
assert optimal(list(range(1, 1001))) == 1001
assert optimal([10**9, 1]) == 2

# a tracing helper for the dry run
def trace(nums):
    nums = nums[:]
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
        print(" after i =", i, nums)
    return nums
print("dry run [3,4,-1,1]:")
trace([3, 4, -1, 1])

rng = random.Random(16)
for _ in range(1000):
    a = [rng.randint(-3, 9) for _ in range(rng.randint(0, 8))]
    assert optimal(a[:]) == brute(a), a
print("1000 random cases agree")
print(optimal([3, 4, -1, 1]), optimal([1, 2, 0]), optimal([7, 8, 9, 11, 12]))
```

**Output (my run):**
```
dry run [3,4,-1,1]:
 after i = 0 [-1, 4, 3, 1]
 after i = 1 [1, -1, 3, 4]
 after i = 2 [1, -1, 3, 4]
 after i = 3 [1, -1, 3, 4]
1000 random cases agree
2 3 1
```

**Edge cases:**
- Empty list gives 1. `[1]` gives 2. `[2]` gives 1.
- Duplicates (`[1,1]`, `[2,2,2,2]`): the equality check prevents a swap loop.
- Huge or negative values are ignored by the range check.
- Already a full 1..n permutation returns n+1.

**Follow-ups:**
- *Can you avoid mutating?* Not in O(1) space for this problem. If you must restore, copy first (O(n) space).
- *Sign-marking version?* Replace out-of-range values with n+1, mark presence by negating `nums[v-1]`; same complexity.
- *Why not sum or XOR tricks?* They solve "one missing in 0..n", not arbitrary values with duplicates.

**Common mistakes:**
- Swapping with `nums[i]-1` written in the wrong order in the tuple assignment, so the index changes mid-swap. Compute `j` first.
- Using `if` instead of `while` for the swap.
- No duplicate check, so `[1,1]` loops forever.
- Forgetting the n+1 case.

---

### Q17 ⭐⭐ 🟢 Number of good pairs. Given `nums`, count index pairs (i, j) with i < j and nums[i] == nums[j]. Do it in O(n) by counting how many equal values were seen before, then show the closed form c*(c-1)/2 per value. Example: [1,2,3,1,1,3] -> 4; [1,1,1,1] -> 6.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Frequency counting. Equal values form groups, and pairs inside a group of size c number c choose 2.

**Say this first (1 line):** Loop once, and for each element add how many equal values came before it; equivalently count each value and add c*(c-1)/2.

**Brute force:** Two loops over i < j and compare: O(n^2) time, O(1) space.

**Optimal:**
- Running count: keep `seen[x]`. When x arrives, every earlier equal value forms one new pair with it, so `ans += seen[x]`, then increment.
- Closed form: a value that appears c times contributes c*(c-1)/2 pairs (choose 2 of c). Sum over `Counter(nums).values()`.
- Both are the same count; the running version is one pass, the closed form is clearer.
- Use `//` (integer division); c*(c-1) is always even so it is exact.

**Complexity:** Time O(n), average O(1) dict operations. Space O(d) where d is the number of distinct values.

**Dry run:** `[1,2,3,1,1,3]`.
- 1: seen 0, ans 0. 2: 0. 3: 0.
- 1: seen[1]=1, ans 1. 1: seen[1]=2, ans 3.
- 3: seen[3]=1, ans 4.
- Closed form: 1 appears 3 times (3 pairs), 3 appears 2 times (1 pair), 2 once (0). Total 4.

**Code:**
```python
import random
from collections import Counter

def brute(nums):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] == nums[j])

def running(nums):                   # count equal values seen before
    seen = {}
    ans = 0
    for x in nums:
        ans += seen.get(x, 0)
        seen[x] = seen.get(x, 0) + 1
    return ans

def closed_form(nums):
    return sum(c * (c - 1) // 2 for c in Counter(nums).values())

assert running([1, 2, 3, 1, 1, 3]) == closed_form([1, 2, 3, 1, 1, 3]) == 4
assert running([1, 1, 1, 1]) == closed_form([1, 1, 1, 1]) == 6
assert running([]) == closed_form([]) == 0
assert running([5]) == closed_form([5]) == 0
assert running([1, 2, 3]) == closed_form([1, 2, 3]) == 0
assert closed_form([7] * 100000) == 100000 * 99999 // 2     # no overflow in Python

rng = random.Random(17)
for _ in range(500):
    a = [rng.randint(-3, 3) for _ in range(rng.randint(0, 12))]
    assert running(a) == closed_form(a) == brute(a), a
print("500 random cases agree")
print(running([1, 2, 3, 1, 1, 3]), closed_form([1, 1, 1, 1]), closed_form([7] * 100000))
```

**Output (my run):**
```
500 random cases agree
4 6 4999950000
```

**Edge cases:**
- Empty or one element: 0.
- All equal: n(n-1)/2, so `[1,1,1,1]` gives 6.
- All distinct: 0.
- Large n: Python ints do not overflow; in fixed-width languages use 64 bits (n = 10^5 gives about 5*10^9, which exceeds 32 bits, as the run shows: 4,999,950,000).

**Follow-ups:**
- *Count bad pairs?* Total pairs minus good pairs of a transformed key (Q44 in this part).
- *Space O(1)?* Sort first, count runs: O(n log n).
- *Ordered pairs or i != j?* Multiply by 2.

**Common mistakes:**
- Using `c*(c-1)/2` with `/`, which gives a float.
- Using c*c/2 or c choose 2 off by one.
- Adding after incrementing the count, which double counts.

---

### Q18 ⭐⭐ 🟢 Ransom note. Given strings `note` and `magazine` of lowercase letters, decide whether note can be built using each magazine letter at most once. Use Counter subtraction and a manual-count version and explain a pitfall of Counter subtraction (non-positive counts). Example: note='aa', magazine='aab' -> True; note='aa', magazine='ab' -> False.
**Asked at:** Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only)

**Pattern:** Frequency counting with a budget: the magazine is a supply of letters, the note is demand.

**Say this first (1 line):** Count the magazine's letters, then consume one per note letter; if any count would go below zero, the note cannot be built.

**Brute force:** For every note letter, find it in the magazine list and remove it. `list.remove` and `in` are O(m) each, so O(n*m) time.

**Optimal:**
- Manual: 26-slot (or dict) count of the magazine; for each note letter decrement and return False if it drops below 0. O(n+m).
- Counter: `Counter(note) - Counter(magazine)`; the note is buildable if the result is empty (no letter is still needed).
- The pitfall: Counter subtraction with `-` keeps only positive counts. Negative and zero results are dropped silently. That is exactly why the empty-result check works here, but it makes `-` the wrong tool when you need to see surpluses (magazine leftovers) or negative balances. `Counter.subtract()` keeps all counts including zero and negative. The direction also matters: `magazine - note` tells you about leftover magazine letters, not whether the note can be built.

**Complexity:** Time O(n + m). Space O(1) for lowercase letters (26 slots), O(k) for k distinct characters in general.

**Dry run:** note `aa`, magazine `aab`.
- Magazine counts: a=2, b=1.
- Note letter a: a becomes 1. Note letter a: a becomes 0. Never negative, so True.
- For `aa` vs `ab`: a=1, b=1. First note a makes a=0. Second note a makes a=-1, below zero, so False.

**Code:**
```python
import random
from collections import Counter

def brute(note, magazine):
    mag = list(magazine)
    for ch in note:
        if ch in mag:
            mag.remove(ch)           # O(len(magazine)) each time
        else:
            return False
    return True

def counter_version(note, magazine):
    need = Counter(note) - Counter(magazine)   # keeps only POSITIVE leftovers
    return not need                             # empty Counter means nothing missing

def manual(note, magazine):
    have = [0] * 26
    for ch in magazine:
        have[ord(ch) - 97] += 1
    for ch in note:
        i = ord(ch) - 97
        have[i] -= 1
        if have[i] < 0:
            return False
    return True

for f in (brute, counter_version, manual):
    assert f('aa', 'aab') is True
    assert f('aa', 'ab') is False
    assert f('', '') is True
    assert f('', 'abc') is True
    assert f('a', '') is False
    assert f('abc', 'cba') is True
    assert f('aab', 'baa') is True

# the pitfall: subtraction silently drops non-positive counts
d = Counter('aa') - Counter('aab')
print("Counter('aa') - Counter('aab') =", d, "(b:-1 is gone, a:0 is gone)")
d2 = Counter('aa'); d2.subtract(Counter('aab'))
print("subtract() keeps them:", d2)
# wrong direction: magazine - note is NOT the check
print("wrong direction magazine - note:", Counter('aab') - Counter('aa'), "(leftover b, says nothing about note)")

rng = random.Random(18)
for _ in range(1000):
    note = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 6)))
    mag = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 9)))
    assert brute(note, mag) == counter_version(note, mag) == manual(note, mag), (note, mag)
print("1000 random cases agree")
print(manual('aa', 'aab'), manual('aa', 'ab'))
```

**Output (my run):**
```
Counter('aa') - Counter('aab') = Counter() (b:-1 is gone, a:0 is gone)
subtract() keeps them: Counter({'a': 0, 'b': -1})
wrong direction magazine - note: Counter({'b': 1}) (leftover b, says nothing about note)
1000 random cases agree
True False
```

**Edge cases:**
- Empty note is always True, even with an empty magazine.
- Empty magazine with a non-empty note is False.
- Note longer than the magazine is False immediately (early exit `len(note) > len(magazine)`).
- Uppercase or Unicode: use a dict instead of the 26-slot array.

**Follow-ups:**
- *Why does the Counter version work at all?* Positive leftovers are exactly the unmet demand.
- *Arbitrary characters?* Use `Counter` or a dict, the 26-slot array only fits lowercase letters.
- *Faster for repeated queries on one magazine?* Build the magazine Counter once and test each note by looping its letters.

**Common mistakes:**
- Reversing the subtraction.
- Checking `Counter(note) <= Counter(magazine)`: it works on Python 3.10+ (multiset comparison), but not on older versions; know the version.
- Using a set, which ignores repeated letters.
- Assuming Counter subtraction keeps negative counts.

---

### Q19 ⭐⭐ 🟢 First non-repeating element. Given a list of integers, return the first element (by position) that occurs exactly once, or -1 if none. Do it in two passes with a Counter and then discuss a single-pass variant with a dict that keeps insertion order. Example: [4,5,1,2,0,4] -> 5; [7,7] -> -1.
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only)

**Pattern:** Frequency count, then first-match scan in original order. Counting tells you "which", the original list tells you "first".

**Say this first (1 line):** Count every value, then walk the list again and return the first value whose count is 1; if none, return -1.

**Brute force:** For each element call `nums.count(x)`, which is O(n), so O(n^2) overall.

**Optimal:**
- Two passes: `Counter(nums)`, then scan `nums` in order and return the first with count 1. O(n) time, O(d) space for d distinct values.
- Single-pass variant: since Python 3.7 a dict remembers first-insertion order. While reading, set `uniq[x] = x not in uniq` (True first time, False on any repeat). Then iterate `uniq.items()` and return the first True. Re-assigning an existing key keeps its original position, which is what makes this work.
- It is still two traversals in practice (one over the input, one over the dict), but the second one is over distinct values only, and it is the right shape for streaming: the dict can answer "first unique so far" at any moment.

**Complexity:** Time O(n) average for both versions. Space O(d), d distinct values.

**Dry run:** `[4,5,1,2,0,4]`.
- Counts: 4:2, 5:1, 1:1, 2:1, 0:1.
- Scan in order: 4 has count 2, skip. 5 has count 1, return 5.
- `[7,7]`: 7 has count 2, nothing else, return -1.

**Code:**
```python
import random
from collections import Counter

def brute(nums):
    for i, x in enumerate(nums):
        if nums.count(x) == 1:       # O(n) each -> O(n^2)
            return x
    return -1

def two_pass(nums):
    c = Counter(nums)
    for x in nums:
        if c[x] == 1:
            return x
    return -1

def one_pass(nums):
    # dict keeps first-seen order; value True = still unique, False = seen again
    uniq = {}
    for x in nums:
        uniq[x] = x not in uniq      # first time True, any repeat False
    for x, ok in uniq.items():       # scans distinct values, not the whole list
        if ok:
            return x
    return -1

for f in (brute, two_pass, one_pass):
    assert f([4, 5, 1, 2, 0, 4]) == 5
    assert f([7, 7]) == -1
    assert f([]) == -1
    assert f([3]) == 3
    assert f([1, 1, 2, 2, 3]) == 3
    assert f([-1, 2, -1, 2]) == -1
    assert f([0, 0, 9]) == 9         # a 0 answer must not be confused with falsy 'none'
    assert f([5, 6, 5]) == 6
assert one_pass([0, 1, 1]) == 0      # unique value 0 is a valid answer
print("sentinel clash: [-1,2,2] returns", two_pass([-1, 2, 2]), "which is a real answer AND the 'none' marker")

rng = random.Random(19)
for _ in range(1000):
    a = [rng.randint(-3, 5) for _ in range(rng.randint(0, 10))]
    assert brute(a) == two_pass(a) == one_pass(a), a
print("1000 random cases agree")
print(two_pass([4, 5, 1, 2, 0, 4]), two_pass([7, 7]))
```

**Output (my run):**
```
sentinel clash: [-1,2,2] returns -1 which is a real answer AND the 'none' marker
1000 random cases agree
5 -1
```

**Edge cases:**
- Empty list returns -1.
- A unique value of 0 is a valid answer (do not test truthiness).
- The sentinel clash: if -1 is itself a legitimate value (`[-1,2,2]`), the return value -1 is ambiguous. Ask the interviewer, or return `None` or an index.
- All duplicates returns -1. Single element returns that element.

**Follow-ups:**
- *Return the index?* Scan with `enumerate`.
- *Streaming?* Keep an ordered dict (or a queue plus counts) and drop duplicates lazily from the front.
- *Memory?* O(d); if the stream is huge you cannot do it exactly in less (a sketch can only approximate).

**Common mistakes:**
- Iterating the Counter and assuming order matches positions (it does in modern Python for insertion order, but be explicit and scan the list).
- Using `if value:` to test the answer, which breaks on 0.
- Calling `list.count` in a loop.

---

### Q20 ⭐⭐ 🟢 Isomorphic strings and word pattern. Two strings s and t of equal length are isomorphic if you can map each character of s to a character of t consistently and one-to-one. Decide it using two dicts (or one dict and a set) and explain why one direction alone is wrong. Example: 'egg','add' -> True; 'foo','bar' -> False; 'badc','baba' -> False.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports

**Pattern:** Bijection check with two hash maps. A consistent one-to-one map needs both directions to hold.

**Say this first (1 line):** Walk both strings together, keep s-to-t and t-to-s maps, and fail on any pair that contradicts either map.

**Brute force:** Convert each string to a canonical "first-occurrence pattern" (`egg` becomes 0,1,1; `add` becomes 0,1,1) and compare the patterns. Also O(n); the two-map version is just the direct version.

**Optimal:**
- Different lengths: return False first.
- For each pair (a, b): `s2t.setdefault(a, b) != b` means a was already mapped to something else. `t2s.setdefault(b, a) != a` means b was already claimed by another letter.
- Why one direction is wrong: with only s-to-t, `badc` vs `baba` passes. b->b, a->a, d->b, c->a is a consistent function, but b and d both map to b, and a and c both map to a. Two source letters sharing one target breaks one-to-one. The run shows the one-direction check returns True while the truth is False.
- Equivalent: one dict plus a set of used targets.
- Word pattern is the same logic with a pattern letter on one side and a whole word on the other (split the sentence, check the lengths match).

**Complexity:** Time O(n). Space O(k) for k distinct characters (O(1) for a fixed alphabet).

**Dry run:** `badc` vs `baba`.
- b-b: s2t {b:b}, t2s {b:b}.
- a-a: s2t {b:b, a:a}, t2s {b:b, a:a}.
- d-b: s2t gets d:b fine, but `t2s[b]` is already b, and b != d, so return False.

**Code:**
```python
import random
from itertools import product

def brute(s, t):
    # isomorphic iff a consistent one-to-one map exists: check via canonical pattern
    def pat(x):
        first = {}
        return [first.setdefault(ch, len(first)) for ch in x]
    return len(s) == len(t) and pat(s) == pat(t)

def optimal(s, t):
    if len(s) != len(t):
        return False
    s2t, t2s = {}, {}
    for a, b in zip(s, t):
        if s2t.setdefault(a, b) != b or t2s.setdefault(b, a) != a:
            return False
    return True

def one_direction_only(s, t):        # the classic wrong answer
    m = {}
    for a, b in zip(s, t):
        if m.setdefault(a, b) != b:
            return False
    return True

def word_pattern(pattern, sentence):
    words = sentence.split()
    if len(pattern) != len(words):
        return False
    p2w, w2p = {}, {}
    for p, w in zip(pattern, words):
        if p2w.setdefault(p, w) != w or w2p.setdefault(w, p) != p:
            return False
    return True

assert optimal('egg', 'add') is True
assert optimal('foo', 'bar') is False
assert optimal('badc', 'baba') is False
assert optimal('paper', 'title') is True
assert optimal('', '') is True
assert optimal('a', 'a') is True
assert optimal('ab', 'aa') is False
assert optimal('ab', 'abc') is False
print("one direction only on ('badc','baba'):", one_direction_only('badc', 'baba'), "(wrong, truth False)")
assert word_pattern('abba', 'dog cat cat dog') is True
assert word_pattern('abba', 'dog cat cat fish') is False
assert word_pattern('abba', 'dog dog dog dog') is False
assert word_pattern('aaaa', 'dog cat cat dog') is False
assert word_pattern('a', 'dog cat') is False

rng = random.Random(20)
for _ in range(1000):
    s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 6)))
    t = ''.join(rng.choice('xyz') for _ in range(len(s)))
    assert optimal(s, t) == brute(s, t), (s, t)
# exhaustive on a tiny alphabet and length 4
for s in map(''.join, product('ab', repeat=4)):
    for t in map(''.join, product('xy', repeat=4)):
        assert optimal(s, t) == brute(s, t)
print("1000 random + 256 exhaustive cases agree")
print(optimal('egg', 'add'), optimal('foo', 'bar'), optimal('badc', 'baba'))
```

**Output (my run):**
```
one direction only on ('badc','baba'): True (wrong, truth False)
1000 random + 256 exhaustive cases agree
True False False
```

**Edge cases:**
- Empty strings are isomorphic.
- Unequal lengths are not.
- A letter may map to itself; the same letter may repeat as long as it keeps the same target.
- Word pattern: `'abba'` with `'dog dog dog dog'` is False (two pattern letters, one word); `'aaaa'` with distinct words is False.

**Follow-ups:**
- *Single-dict approach?* Compare `s.index(a)` with `t.index(b)` at each position; correct but O(n^2).
- *Group isomorphic strings together?* Use the canonical first-occurrence pattern as the dict key.
- *Why setdefault?* It inserts on first sight and returns the stored value, so one call does the check and the store.

**Common mistakes:**
- Checking one direction only.
- Forgetting the length check (zip silently truncates).
- In word pattern, using `list(sentence)` instead of `sentence.split()`.

---

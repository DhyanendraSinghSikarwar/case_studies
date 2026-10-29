### Q41 ⭐ 🟡 Hoare partition, one call. `nums` has 2 <= len <= 50 integers (duplicates allowed). Run exactly this partition with pivot `p = nums[0]`: `i = -1; j = len(nums)`; loop: `i += 1` then keep doing `i += 1` while `a[i] < p`; `j -= 1` then keep doing `j -= 1` while `a[j] > p`; if `i >= j` return j; otherwise swap `a[i]` and `a[j]` and repeat. Return `[array_after, j]`. Explain what the result guarantees (every item at positions 0..j is <= p and every item at positions j+1..end is >= p, and 0 <= j < len - 1, so recursing on [0, j] and [j + 1, end] always shrinks), why the pivot is NOT placed in its final position (unlike Lomuto), why the recursion must use j and j + 1 (not j - 1 and j + 1), why choosing the LAST element as the pivot with this exact loop can return j = len - 1 (and recurse forever), and why Hoare's scheme handles many equal keys better than Lomuto (both pointers stop on equal keys, so they meet near the middle). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a version written with while True loops and checking the guarantees on small inputs. Example: nums=[5, 3, 8, 1, 9, 2] -> [[2, 3, 1, 8, 9, 5], 2]; nums=[2, 1] -> [[1, 2], 0]; nums=[1, 2] -> [[1, 2], 0]; nums=[4, 4, 4, 4] -> [[4, 4, 4, 4], 1].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)
**Pattern:** Two pointers walking toward each other (Hoare partition, the original quicksort partition). It applies because we only need "small stuff left, big stuff right", not one exact final spot for the pivot.

**Say this first (1 line):** "Two pointers start outside the array and move inward; each stops on anything that is on the wrong side or equal to the pivot, I swap, and when they cross I return j, so [0..j] is all <= pivot and [j+1..] is all >= pivot."

**Brute force:** Build the answer from a definition: copy the array, then check the contract by scanning (every item at 0..j is <= p, every item after is >= p). There is no simple brute force that reproduces the exact same swaps, so the cross-check is a second implementation (while True loops, pointers moved after a swap) plus the contract check on every array of length 2 to 7 over small values.

**Optimal:**
- `p = a[0]`, `i = -1`, `j = n`. Each round: move i right past items `< p`, move j left past items `> p`.
- If `i >= j`, return j. Otherwise swap `a[i]`, `a[j]` and go on.
- Both pointers stop on items equal to p. That looks wasteful (extra swaps) but it keeps the split balanced.
- Guarantee: everything left of i is <= p, everything right of j is >= p. When they meet or cross, j is the last position of the "<= p" side.
- Why `0 <= j < n - 1` with pivot a[0]: in the first round i stops at index 0 (the pivot is not `< p`), so j is at most n - 1 there. Either they meet at j = 0 (return 0), or we swap, and then j is decremented again before it is returned, so j <= n - 2. The exhaustive run below confirms it. So [0, j] and [j + 1, end] are both non-empty and both shorter than the input.
- Why the pivot is not placed: Hoare only separates the two sides. The pivot may be swapped around and ends somewhere in [0..j] or even on the right (see the first example, the 5 moved to the end). Lomuto puts the pivot at its final index and recurses on both sides excluding it.
- Why recurse on j and j + 1: index j still belongs to the left side and may not be the pivot's final place. Using `j - 1` drops an element that has not been placed: in my run that left 305 of 500 small arrays unsorted.
- Why a last-element pivot can break: with `p = a[-1]` the first i-scan can stop at the last index, then j stops at the same index and the function returns j = n - 1. Recursing on [0, j] is then the full range again: infinite recursion. Example [1, 2].
- Equal keys: with all keys equal both pointers stop at once every round, swap, and meet in the middle (j = 49 for n = 100). Lomuto with `<` sends every equal key to one side and gets n - 1 (quadratic quicksort).

**Complexity:** One call is O(n) time (each pointer only moves inward, so at most n + 1 steps in total) and O(1) extra space. At most n / 2 swaps. A full quicksort with it is O(n log n) on average, O(n^2) on bad pivots, as usual.

**Dry run:** nums = [5, 3, 8, 1, 9, 2], p = 5.
| step | i | j | action |
|---|---|---|---|
| start | -1 | 6 | |
| round 1 | 0 (5 is not < 5) | 5 (2 is not > 5) | i < j, swap -> [2, 3, 8, 1, 9, 5] |
| round 2 | 2 (3 < 5, then 8 stops) | 3 (1 is not > 5) | i < j, swap -> [2, 3, 1, 8, 9, 5] |
| round 3 | 3 (8 stops at once) | 2 (j steps from 3 to 2, where 1 is not > 5) | i = 3 >= j = 2, return 2 |
Result [[2, 3, 1, 8, 9, 5], 2]. Left part [2, 3, 1] all <= 5, right part [8, 9, 5] all >= 5. The pivot 5 ended up in the right part.

**Code:**
```python
import random, itertools
random.seed(41)

# ---- the exact partition from the question (pivot = a[lo], returns the new array and j)
def hoare(nums):
    a = list(nums); p = a[0]; i, j = -1, len(a)
    while True:
        i += 1
        while a[i] < p: i += 1
        j -= 1
        while a[j] > p: j -= 1
        if i >= j: return [a, j]
        a[i], a[j] = a[j], a[i]

# ---- the examples
assert hoare([5, 3, 8, 1, 9, 2]) == [[2, 3, 1, 8, 9, 5], 2]
assert hoare([2, 1]) == [[1, 2], 0]
assert hoare([1, 2]) == [[1, 2], 0]
assert hoare([4, 4, 4, 4]) == [[4, 4, 4, 4], 1]
print('examples ok:', hoare([5, 3, 8, 1, 9, 2]), hoare([2, 1]), hoare([1, 2]), hoare([4, 4, 4, 4]))

def guarantees(orig, a, j):
    p = orig[0]
    return (sorted(a) == sorted(orig) and 0 <= j < len(a) - 1
            and all(x <= p for x in a[:j + 1]) and all(x >= p for x in a[j + 1:]))

# ---- exhaustive check: every array of length 2..7 over values 0..3 (and 0..4 for length <= 5)
cnt = 0
for n in range(2, 8):
    for t in itertools.product(range(4 if n > 5 else 5), repeat=n):
        a, j = hoare(t)
        assert guarantees(t, a, j), t
        cnt += 1
print('guarantees hold for', cnt, 'arrays (all arrays of length 2..7 over small value sets)')

# ---- seeded random cross-check against the while-True version (same i/j walk, different loop shape)
def hoare_alt(nums):
    a = list(nums); p = a[0]; i, j = 0, len(a) - 1
    while True:
        while a[i] < p: i += 1
        while a[j] > p: j -= 1
        if i >= j: return [a, j]
        a[i], a[j] = a[j], a[i]
        i += 1; j -= 1
for _ in range(2000):
    t = [random.randint(-5, 5) for _ in range(random.randint(2, 50))]
    assert hoare(t) == hoare_alt(t)
    a, j = hoare(t); assert guarantees(t, a, j)
print('2000 random arrays: both loop shapes agree and the guarantees hold')

# ---- recursion on [lo, j] and [j+1, hi] sorts; j-1 / j+1 (Lomuto style) does not
def part_range(a, lo, hi, pivot_index):
    p = a[pivot_index]; i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < p: i += 1
        j -= 1
        while a[j] > p: j -= 1
        if i >= j: return j
        a[i], a[j] = a[j], a[i]
def qs(a, lo, hi, wrong=False, depth=0):
    if depth > 200: raise RecursionError('no progress')
    if lo >= hi: return
    j = part_range(a, lo, hi, lo)
    if wrong: qs(a, lo, j - 1, True, depth + 1); qs(a, j + 1, hi, True, depth + 1)
    else: qs(a, lo, j, False, depth + 1); qs(a, j + 1, hi, False, depth + 1)
for _ in range(500):
    t = [random.randint(0, 9) for _ in range(random.randint(0, 12))]
    a = list(t); qs(a, 0, len(a) - 1); assert a == sorted(t)
bad = 0
for _ in range(500):
    t = [random.randint(0, 9) for _ in range(random.randint(2, 12))]
    a = list(t); qs(a, 0, len(a) - 1, wrong=True); bad += a != sorted(t)
print('recursing on [lo, j] and [j+1, hi]: 500/500 sorted; on [lo, j-1] and [j+1, hi]:', bad, '/ 500 left unsorted')

# ---- last element as pivot with the same loop: j can be len-1, so [lo, j] is the whole range
a = [1, 2]; j = part_range(a, 0, 1, 1)
print('pivot = last element, [1, 2] -> j =', j, '(= len - 1, so recursing on [0, j] never shrinks)')
try:
    b = [1, 2, 3]
    def qs_last(a, lo, hi, depth=0):
        if depth > 50: raise RecursionError('stuck: same range again and again')
        if lo >= hi: return
        j = part_range(a, lo, hi, hi); qs_last(a, lo, j, depth + 1); qs_last(a, j + 1, hi, depth + 1)
    qs_last(b, 0, 2)
except RecursionError as e: print('last-element pivot quicksort:', e)
# count how often the last-element pivot can return len-1 on small arrays
hits = sum(1 for t in itertools.product(range(3), repeat=4) if (lambda a: part_range(a, 0, 3, 3))(list(t)) == 3)
print('last-element pivot returned j = n-1 for', hits, 'of 81 arrays of length 4 over {0,1,2}')

# ---- equal keys: both pointers stop on equal keys, so j lands in the middle; Lomuto (last pivot) would give n-1
for n in (8, 100):
    a, j = hoare([7] * n); print('all equal, n =', n, '-> j =', j, '(middle); Lomuto with all equal puts the pivot at', n - 1)
swaps = []
for n in (8, 100):
    a = [7] * n; p = a[0]; i, j, s = -1, n, 0
    while True:
        i += 1
        while a[i] < p: i += 1
        j -= 1
        while a[j] > p: j -= 1
        if i >= j: break
        a[i], a[j] = a[j], a[i]; s += 1
    swaps.append(s)
print('swaps on all-equal input of size 8 and 100:', swaps, '(useless swaps, but the split is balanced)')

# ---- edge asserts
assert hoare([3, 3]) == [[3, 3], 0]
assert hoare([9, 1]) == [[1, 9], 0]
assert hoare([1, 9, 1]) == [[1, 9, 1], 0]
assert hoare([2, 2, 1]) == [[1, 2, 2], 1]
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [[2, 3, 1, 8, 9, 5], 2] [[1, 2], 0] [[1, 2], 0] [[4, 4, 4, 4], 1]
guarantees hold for 24380 arrays (all arrays of length 2..7 over small value sets)
2000 random arrays: both loop shapes agree and the guarantees hold
recursing on [lo, j] and [j+1, hi]: 500/500 sorted; on [lo, j-1] and [j+1, hi]: 305 / 500 left unsorted
pivot = last element, [1, 2] -> j = 1 (= len - 1, so recursing on [0, j] never shrinks)
last-element pivot quicksort: stuck: same range again and again
last-element pivot returned j = n-1 for 9 of 81 arrays of length 4 over {0,1,2}
all equal, n = 8 -> j = 3 (middle); Lomuto with all equal puts the pivot at 7
all equal, n = 100 -> j = 49 (middle); Lomuto with all equal puts the pivot at 99
swaps on all-equal input of size 8 and 100: [4, 50] (useless swaps, but the split is balanced)
edge asserts ok
```

**Edge cases:**
- Length 2: [2, 1] gives j = 0, [1, 2] gives j = 0. Both halves have size 1.
- All equal: j in the middle.
- Pivot is the unique maximum at index 0: i stops at the first item, j walks left to 0 and meets it, j = 0 (left side is only the pivot's slot).
- Pivot is the unique minimum: every other item is larger, so j walks all the way left to index 0 and the call returns j = 0.
- Duplicates of the pivot on both sides: they are swapped around but stay on valid sides.

**Follow-ups:**
- Can I pick a random pivot? Yes: swap the random item to a[0] first, then run the same loop. Never use the last element with this exact loop (or switch to the `i = lo, j = hi` do-while form with matching rules).
- Which is faster in practice, Lomuto or Hoare? The usual textbook claim is that Hoare does fewer swaps on random data and handles duplicates better. I did not measure that here.
- Does Hoare quicksort need the pivot to end in place? No, that is why the recursion ranges overlap on j.

**Common mistakes:**
- Recursing on (lo, j - 1) and (j + 1, hi). It loses an element.
- Using the last element as pivot with this loop and getting an infinite recursion.
- Stopping the scans on `<=` / `>=` instead of strict `<` / `>`: the pointers then run off the array on equal keys.
- Expecting the pivot to sit at index j.

---

### Q42 ⭐ 🟡 Three-way partition quicksort versus Lomuto on duplicates. `nums` has 1 <= len <= 2000 integers with many repeats allowed. Return `[sorted_list, lomuto_comparisons, three_way_comparisons]`. `lomuto_comparisons` is the total number of `a[j] < p` tests of the Lomuto quicksort defined in Q16 (last element as pivot). The three-way quicksort partitions a range [lo, hi] around `p = a[hi]` with `lt = lo, i = lo, gt = hi` and `while i <= gt:` ONE comparison of `a[i]` with p: if `a[i] < p` swap `a[lt]` and `a[i]` and do `lt += 1; i += 1`; if `a[i] > p` swap `a[i]` and `a[gt]` and do `gt -= 1`; if equal do `i += 1`. Then it sorts [lo, lt - 1] and [gt + 1, hi] and skips ranges with fewer than 2 items. Both must be iterative (an all-equal input makes the Lomuto recursion about n deep, above CPython's recursion limit for n near 1000 and over). Explain why all-equal input costs n * (n - 1) / 2 comparisons for Lomuto but n for three-way, that this is the Dutch national flag partition, and that the equal block is never touched again. The same partition idea drives quickselect (Part 8 Q36). In the answer include a dry run on the first example and a seeded random cross-check of your solution against recursive versions of both partition schemes on small inputs on small inputs. Example: nums=[2, 2, 2, 2] -> [[2, 2, 2, 2], 6, 4]; nums=[3, 1, 2, 3, 1] -> [[1, 1, 2, 3, 3], 8, 8]; nums=[1, 2, 3, 4, 5] -> [[1, 2, 3, 4, 5], 10, 14].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)
**Pattern:** Quicksort partitioning, and duplicates. Three-way partition is the Dutch national flag idea: one pass splits a range into `< p`, `== p`, `> p`.

**Say this first (1 line):** "Lomuto puts all equal keys on one side so all-equal input costs n(n-1)/2; three-way partition parks every key equal to the pivot in the middle block and never looks at it again, so all-equal input is one pass of n."

**Brute force:** Lomuto quicksort with the last element as pivot (Q16), counting every `a[j] < p` test. It is correct, but with many equal keys the pivot lands at the end of its range every time, so recursion peels one item per level: about n levels deep and n^2 / 2 comparisons. Recursive code would also crash on an all-equal input of around 1000 items (default recursion limit 1000; my run raised RecursionError at 1500).

**Optimal:**
- Keep three pointers on the range [lo, hi] with `p = a[hi]`: `a[lo..lt-1] < p`, `a[lt..i-1] == p`, `a[i..gt] unknown`, `a[gt+1..hi] > p`.
- Look at `a[i]` once: smaller, swap to `lt` and advance both; larger, swap to `gt` and shrink gt (do not advance i, the swapped-in item is unseen); equal, just advance i.
- Stop when `i > gt`. Then sort only [lo, lt-1] and [gt+1, hi]. The block `[lt..gt]` holds the pivot value and is already in its final place.
- Iterative: push the two ranges on a list used as a stack, pop, skip ranges with fewer than 2 items. No recursion, so no recursion-limit problem whatever the input.
- All-equal input: every item is equal, so one pass of n comparisons and both sub-ranges are empty. Lomuto: n - 1, n - 2, ... 1 comparisons = n(n-1)/2 (checked for n = 1, 2, 3, 10, 57, 2000).
- Quickselect (Part 8 Q36) uses the same partition and then recurses into only the side that holds the wanted rank.

**Complexity:**
- Lomuto: O(n log n) on average with distinct keys, O(n^2) when the pivot is an extreme (sorted input, all equal). Space O(n) for the stack in the worst case.
- Three-way: the same on distinct keys; on k distinct values it is O(n log k) with a good pivot. With only a few distinct values it is close to linear (see the run: 6102 comparisons against 205321 for 2000 items from 10 values).
- Honest warning: the three-way scheme with the last element as pivot is NOT immune to sorted input. On 1..n the pivot is the maximum, one pass of n comparisons peels one item, and the total is n(n+1)/2 - 1 (14 for n = 5, higher than Lomuto's 10; asserted in the code). A random or median-of-three pivot fixes that; three-way only fixes duplicates.

**Dry run:** nums = [3, 1, 2, 3, 1], three-way, p = a[4] = 1.
| i | a | lt | gt | action |
|---|---|---|---|---|
| 0 | [3,1,2,3,1] | 0 | 4 | 3 > 1: swap a[0], a[4] -> [1,1,2,3,3], gt = 3 |
| 0 | [1,1,2,3,3] | 0 | 3 | 1 == 1: i = 1 |
| 1 | | 0 | 3 | 1 == 1: i = 2 |
| 2 | | 0 | 3 | 2 > 1: swap a[2], a[3] -> [1,1,3,2,3], gt = 2 |
| 2 | | 0 | 2 | 3 > 1: swap a[2], a[2], gt = 1; now i > gt, stop |
5 comparisons. Equal block = [0..1], so ranges [0..-1] (empty) and [2..4] = [3,2,3] remain. Sorting that range with p = 3 takes 3 more comparisons (3 == p, then 2 < p swaps to the front, then 3 == p) and gives [2,3,3]; the leftover ranges have fewer than 2 items and are skipped. Total 8 comparisons, sorted [1,1,2,3,3]. Lomuto also costs 8 on this input.

**Code:**
```python
import random, itertools, sys
random.seed(42)

# ---- optimal: both quicksorts iterative (explicit stack of ranges), with comparison counters
def lomuto_iter(nums):
    a = list(nums); cmps = 0
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi: continue
        p = a[hi]; i = lo
        for j in range(lo, hi):
            cmps += 1                                  # one test a[j] < p
            if a[j] < p: a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]                      # pivot to its final index i
        stack.append((lo, i - 1)); stack.append((i + 1, hi))
    return a, cmps

def three_way_iter(nums):
    a = list(nums); cmps = 0
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if hi - lo < 1: continue                       # fewer than 2 items
        p = a[hi]; lt, i, gt = lo, lo, hi
        while i <= gt:
            cmps += 1                                  # ONE comparison, three outcomes (<, >, ==)
            if a[i] < p: a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] > p: a[i], a[gt] = a[gt], a[i]; gt -= 1
            else: i += 1
        stack.append((lo, lt - 1)); stack.append((gt + 1, hi))   # the block [lt..gt] == p is never touched again
    return a, cmps

def solve(nums):
    s, cl = lomuto_iter(nums); s3, c3 = three_way_iter(nums)
    assert s == s3
    return [s, cl, c3]

# ---- recursive versions, written separately, as the cross-check
def rec_versions(nums):
    c = [0, 0]; a = list(nums); b = list(nums)
    def rl(lo, hi):
        if lo >= hi: return
        p = a[hi]; i = lo
        for j in range(lo, hi):
            c[0] += 1
            if a[j] < p: a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]; rl(lo, i - 1); rl(i + 1, hi)
    def r3(lo, hi):
        if hi - lo < 1: return
        p = b[hi]; lt, i, gt = lo, lo, hi
        while i <= gt:
            c[1] += 1
            if b[i] < p: b[lt], b[i] = b[i], b[lt]; lt += 1; i += 1
            elif b[i] > p: b[i], b[gt] = b[gt], b[i]; gt -= 1
            else: i += 1
        r3(lo, lt - 1); r3(gt + 1, hi)
    rl(0, len(a) - 1); r3(0, len(b) - 1)
    assert a == b == sorted(nums)
    return [a, c[0], c[1]]

# ---- examples
assert solve([2, 2, 2, 2]) == [[2, 2, 2, 2], 6, 4]
assert solve([3, 1, 2, 3, 1]) == [[1, 1, 2, 3, 3], 8, 8]
assert solve([1, 2, 3, 4, 5]) == [[1, 2, 3, 4, 5], 10, 14]
print('examples ok:', solve([2, 2, 2, 2]), solve([3, 1, 2, 3, 1]), solve([1, 2, 3, 4, 5]))

# ---- seeded random cross-check (small value ranges give many repeats)
for _ in range(3000):
    n = random.randint(1, 30); k = random.choice([1, 2, 3, 5, 50])
    t = [random.randint(0, k) for _ in range(n)]
    assert solve(t) == rec_versions(t) and solve(t)[0] == sorted(t)
print('3000 random inputs: iterative == recursive (sorted list and both counters)')

# ---- exact claims, checked
for n in (1, 2, 3, 10, 57, 2000):
    s, cl, c3 = solve([7] * n)
    assert cl == n * (n - 1) // 2 and c3 == (n if n >= 2 else 0)
print('all equal, n = 2000: Lomuto', solve([7] * 2000)[1], '= n(n-1)/2 ; three-way', solve([7] * 2000)[2], '= n')
# sorted input is bad for Lomuto (last element = maximum) and fine-ish for three-way only by luck of the pivot rule
print('sorted 1..2000: Lomuto', solve(list(range(2000)))[1], ' three-way', solve(list(range(2000)))[2])
d = [random.randint(0, 9) for _ in range(2000)]
print('2000 random items from 10 distinct values: Lomuto', solve(d)[1], ' three-way', solve(d)[2])

# ---- why iterative: the recursive Lomuto on all-equal input of size n is about n frames deep
try:
    rec_versions([7] * 1500)
except RecursionError:
    print('recursive version on 1500 equal items: RecursionError (limit', sys.getrecursionlimit(), ')')
print('iterative version on 2000 equal items worked (no recursion at all)')

# ---- edge asserts
assert solve([]) == [[], 0, 0]
assert solve([5]) == [[5], 0, 0]
assert solve([2, 1]) == [[1, 2], 1, 2]
assert solve([1, 1, 1, 2, 2, 2]) [0] == [1, 1, 1, 2, 2, 2]
assert solve([-3, -3, 0, -3])[0] == [-3, -3, -3, 0]
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [[2, 2, 2, 2], 6, 4] [[1, 1, 2, 3, 3], 8, 8] [[1, 2, 3, 4, 5], 10, 14]
3000 random inputs: iterative == recursive (sorted list and both counters)
all equal, n = 2000: Lomuto 1999000 = n(n-1)/2 ; three-way 2000 = n
sorted 1..2000: Lomuto 1999000  three-way 2000999
2000 random items from 10 distinct values: Lomuto 205321  three-way 6102
recursive version on 1500 equal items: RecursionError (limit 1000 )
iterative version on 2000 equal items worked (no recursion at all)
edge asserts ok
```

**Edge cases:**
- Empty and single item: 0 comparisons for both.
- Two items: Lomuto 1, three-way 2 (the pivot is compared with itself once).
- All equal: 6 vs 4 for four items; n(n-1)/2 vs n in general.
- Already sorted with a last-element pivot: quadratic for both.
- Negative numbers and a mix: nothing special, comparisons only.

**Follow-ups:**
- How do you avoid the sorted-input worst case? Random pivot or median of three; for adversarial input, introsort (fall back to heap sort at depth 2 log n).
- Why does the equal block never get touched again? Everything left of it is smaller and everything right is larger, so those items are in final place.
- Which sort does Python use? Timsort, not quicksort (Q43, Q44).

**Common mistakes:**
- Advancing i after swapping with gt: the swapped-in item has not been examined.
- Looping while `i < gt` instead of `i <= gt` and missing the last item.
- Recursing on [lo, lt] or [gt, hi] and re-sorting the equal block.
- Writing the recursive version and trusting it on sorted or all-equal input of size 1000 and over.
- Claiming three-way is O(n log n) in the worst case with a bad pivot.

---

### Q43 ⭐ 🟡 Adaptive sorting: nearly sorted inputs. `nums` has 0 <= len <= 300 integers. Return `[timsort, insertion, shifts, inversions, merge]`: `timsort` is the number of `<` comparisons CPython's `list.sort` performs on the list (measured by sorting objects whose `__lt__` increments a counter; this is the observed behaviour of CPython 3.13 and the checker accepts exactly that count); `insertion` is the number of comparisons `a[j - 1] > x` made by plain insertion sort (for each i from 1, take x = a[i], and while j > 0 compare a[j - 1] with x and shift while it is greater); `shifts` is the number of element moves that insertion sort makes; `inversions` is the number of pairs i < j with nums[i] > nums[j]; `merge` is the number of comparisons of the top-down merge sort of Q15 on keys = the values. Explain why `shifts == inversions`, why insertion sort costs about n + inversions comparisons (so it is O(n) on nearly sorted data and O(n^2) on reversed data), why merge sort does not adapt, and why Timsort needs only n - 1 comparisons on an already sorted list and on a strictly descending one (it finds one natural run, reversing it if it descends strictly) while it still guarantees O(n log n) on any input. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a separately written counting wrapper class and the O(n^2) inversion count on small inputs. Example: nums=[1, 2, 3, 4, 5] -> [4, 4, 0, 0, 5]; nums=[5, 4, 3, 2, 1] -> [4, 10, 10, 10, 7]; nums=[1, 2, 4, 3, 5, 6] -> [10, 6, 1, 1, 8]; nums=[2, 2, 1, 1] -> [5, 6, 4, 4, 4]; nums=[] -> [0, 0, 0, 0, 0].
**Asked at:** Python Sorting HOWTO (search-result snippets only; the docs.python.org fetch failed with ENOTFOUND, so behaviour was verified by running Python 3.13) | Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)
**Pattern:** Adaptive sorting and inversion counting. The cost of insertion sort is "n plus the number of inversions"; a sort is adaptive if it gets cheaper on input that is already nearly in order.

**Say this first (1 line):** "Every shift in insertion sort removes exactly one inversion, so shifts equal inversions and comparisons are about n plus inversions; merge sort ignores the order; Timsort looks for runs first, so a sorted or strictly descending list costs n - 1 comparisons."

**Brute force:** Count inversions with the double loop (O(n^2)); simulate each algorithm with a counter. The `Timsort` count is not simulated: it is measured by sorting objects whose `__lt__` increments a counter (this is observed CPython 3.13 behaviour, and a plain int list may use a faster internal comparison that bypasses `__lt__`, which is why wrapper objects are used).

**Optimal:**
- Insertion sort: for each i take x = a[i] and shift larger items to the right until a smaller or equal one appears. The array keeps a sorted prefix.
- `shifts == inversions`: a shift moves one larger item past x, which fixes exactly one pair (that item, x) that was out of order, and an inversion is only ever fixed by a shift. Sorted at the end means zero inversions left. It was also checked on 3280 small lists.
- Comparisons: each i makes one comparison per shift plus one failed comparison, unless x travels all the way to the front (then the loop ends on `j == 0` with no failed comparison). So comparisons = inversions + (n - 1) - (number of items that become a strict new minimum of the prefix). That is between inversions and inversions + n - 1: O(n) on nearly sorted data, O(n^2) on reversed data (n(n-1)/2).
- Merge sort (Q15 version): it always splits and merges, so it does not adapt: 1180 comparisons for a sorted list of 300 and 1308 for the reversed one, within the same n log n band.
- Timsort: first finds a natural run at the start (the longest non-decreasing stretch, or a strictly descending one, which it reverses in place). A fully sorted or strictly descending list is one run, found with n - 1 comparisons and no merging. Checked for every length 1..299. Ties break it: [2, 2, 1, 1] is not strictly descending, and costs 5. Why strictly: reversing a non-strictly descending run would swap equal items and break stability.
- It still guarantees O(n log n) for any input because short runs are extended by binary insertion sort and runs are merged under balance rules (details in Q44).
- Honest note: adaptive does not mean best everywhere. On my 300-item list with 5 adjacent swaps, Timsort used 541 comparisons while plain insertion sort used 304. Insertion sort is the cheapest when the displacement is tiny. Timsort's promise is "never much worse than n log n, linear on the common easy shapes".

**Complexity:**
- Insertion sort O(n + inversions) time, O(1) space, stable.
- Inversion counting by merge sort O(n log n) (used here only as a check; the brute force O(n^2) is also in the code).
- Top-down merge sort always about n log2 n comparisons, O(n) extra space.
- Timsort O(n) best case (one run), O(n log n) worst case, O(n) extra space.

**Dry run:** nums = [1, 2, 4, 3, 5, 6], insertion sort.
| i | x | compare | result |
|---|---|---|---|
| 1 | 2 | 1 > 2? no | 1 comparison |
| 2 | 4 | 2 > 4? no | 1 |
| 3 | 3 | 4 > 3 yes (shift), 2 > 3 no | 2 comparisons, 1 shift |
| 4 | 5 | 4 > 5? no | 1 |
| 5 | 6 | 5 > 6? no | 1 |
Total 6 comparisons, 1 shift, 1 inversion (the pair 4, 3). Formula: 1 inversion + 5 - 0 new minima = 6. Merge sort: 8 comparisons (observed from the counter, independent of order). Timsort: 10 observed on CPython 3.13 (a short list is handled by finding the run [1, 2, 4] then binary insertion of the remaining items; I report the measured number, not a hand derivation).

**Code:**
```python
import random, itertools, functools, math
random.seed(43)

# ---- Timsort: count the '<' calls CPython's list.sort makes, by sorting objects that count them
class Cnt:
    n = 0
    __slots__ = ('v',)
    def __init__(self, v): self.v = v
    def __lt__(self, o): Cnt.n += 1; return self.v < o.v
def timsort_cmps(nums):
    Cnt.n = 0; sorted(Cnt(v) for v in nums); return Cnt.n

# ---- plain insertion sort: comparisons a[j-1] > x, element moves
def insertion(nums):
    a = list(nums); cmps = shifts = 0
    for i in range(1, len(a)):
        x = a[i]; j = i
        while j > 0:
            cmps += 1
            if a[j - 1] > x: a[j] = a[j - 1]; shifts += 1; j -= 1
            else: break
        a[j] = x
    assert a == sorted(nums)
    return cmps, shifts

# ---- inversions in O(n log n) by merge counting; (the brute force below is O(n^2))
def inversions(nums):
    a = list(nums)
    def go(lo, hi):
        if hi - lo < 2: return 0
        mid = (lo + hi) // 2; inv = go(lo, mid) + go(mid, hi)
        L, R = a[lo:mid], a[mid:hi]; i = j = 0; k = lo
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: a[k] = L[i]; i += 1
            else: a[k] = R[j]; j += 1; inv += len(L) - i
            k += 1
        a[k:hi] = L[i:] + R[j:]
        return inv
    return go(0, len(a))

# ---- top-down merge sort of Q15: split at n // 2, take from the left on ties (<=), count comparisons
def merge_cmps(nums):
    c = 0
    def sort(x):
        nonlocal c
        if len(x) <= 1: return x
        m = len(x) // 2; L, R = sort(x[:m]), sort(x[m:]); out = []; i = j = 0
        while i < len(L) and j < len(R):
            c += 1
            if L[i] <= R[j]: out.append(L[i]); i += 1
            else: out.append(R[j]); j += 1
        return out + L[i:] + R[j:]
    sort(list(nums)); return c

def solve(nums):
    ic, sh = insertion(nums)
    return [timsort_cmps(nums), ic, sh, inversions(nums), merge_cmps(nums)]

# ---- examples
ex = {(1, 2, 3, 4, 5): [4, 4, 0, 0, 5], (5, 4, 3, 2, 1): [4, 10, 10, 10, 7], (1, 2, 4, 3, 5, 6): [10, 6, 1, 1, 8],
      (2, 2, 1, 1): [5, 6, 4, 4, 4], (): [0, 0, 0, 0, 0]}
for k, v in ex.items(): assert solve(list(k)) == v, (k, solve(list(k)))
print('examples ok:', [solve(list(k)) for k in ex])

# ---- cross-check: separate counting wrapper (cmp_to_key counts calls of the comparison function) and O(n^2) inversions
def tim_alt(nums):
    c = [0]
    def cmp(x, y): c[0] += 1; return -1 if x < y else (1 if x > y else 0)
    sorted(nums, key=functools.cmp_to_key(cmp)); return c[0]
for _ in range(1500):
    n = random.randint(0, 40); k = random.choice([2, 5, 100])
    t = [random.randint(0, k) for _ in range(n)]
    inv2 = sum(t[i] > t[j] for i in range(n) for j in range(i + 1, n))
    r = solve(t)
    assert r[0] == tim_alt(t) and r[3] == inv2 and r[2] == inv2
print('1500 random lists: Timsort count == cmp_to_key counter, merge-count inversions == O(n^2) count == insertion shifts')

# ---- exhaustive claims for small n (all lists over 0..2, lengths <= 7)
tested = 0
for n in range(0, 8):
    for t in itertools.product(range(3), repeat=n):
        ic, sh = insertion(t); inv = sum(t[i] > t[j] for i in range(n) for j in range(i + 1, n))
        assert sh == inv                                            # each shift removes exactly one inversion
        minima = sum(1 for i in range(1, n) if all(t[p] > t[i] for p in range(i)))   # items that go all the way to the front
        assert ic == inv + (n - 1 if n else 0) - minima             # exact comparison count
        tested += 1
print('shifts == inversions and comparisons == inversions + (n-1) - (strict new prefix minima) for', tested, 'lists')

# ---- Timsort on already sorted / strictly descending lists: n - 1 comparisons (CPython 3.13, observed)
for n in range(1, 300):
    assert timsort_cmps(list(range(n))) == max(n - 1, 0)
    assert timsort_cmps(list(range(n, 0, -1))) == max(n - 1, 0)
print('sorted and strictly descending lists of every length 1..299: exactly n - 1 comparisons')
print('descending with ties [2,2,1,1]:', timsort_cmps([2, 2, 1, 1]), '(not strictly descending, so not one run)')

# ---- n = 300: nearly sorted versus random versus reversed
base = list(range(300))
near = list(base)
for _ in range(5):
    i = random.randrange(299); near[i], near[i + 1] = near[i + 1], near[i]
rnd = random.sample(base, 300)
print('n = 300  (timsort, insertion, shifts, inversions, merge)')
for name, t in (('sorted', base), ('5 adjacent swaps', near), ('reversed', base[::-1]), ('random', rnd)):
    print(f'  {name:17}', solve(t))

# ---- edge asserts
assert solve([7]) == [0, 0, 0, 0, 0]
assert solve([1, 1, 1, 1]) == [3, 3, 0, 0, 4]
assert solve([2, 1]) == [1, 1, 1, 1, 1]
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [[4, 4, 0, 0, 5], [4, 10, 10, 10, 7], [10, 6, 1, 1, 8], [5, 6, 4, 4, 4], [0, 0, 0, 0, 0]]
1500 random lists: Timsort count == cmp_to_key counter, merge-count inversions == O(n^2) count == insertion shifts
shifts == inversions and comparisons == inversions + (n-1) - (strict new prefix minima) for 3280 lists
sorted and strictly descending lists of every length 1..299: exactly n - 1 comparisons
descending with ties [2,2,1,1]: 5 (not strictly descending, so not one run)
n = 300  (timsort, insertion, shifts, inversions, merge)
  sorted            [299, 299, 0, 0, 1180]
  5 adjacent swaps  [541, 304, 5, 5, 1182]
  reversed          [299, 44850, 44850, 44850, 1308]
  random            [2083, 22710, 22418, 22418, 2089]
edge asserts ok
```

**Edge cases:**
- Empty list and one item: all counts 0.
- All equal: insertion makes n - 1 comparisons and 0 shifts because the test is `>` (strict), which is also why it is stable. Merge sort still makes about n log n.
- Reversed: insertion sort's worst case, n(n-1)/2 for all three counters, while Timsort only needs n - 1.
- Ties in a descending list ([2, 2, 1, 1]): not one strict run.
- Wrapper objects versus plain ints: counting is only possible with objects; the ordering result is the same.

**Follow-ups:**
- Why is insertion sort used inside Timsort? It is the fastest option for tiny ranges (low overhead, adaptive); Timsort uses a binary-search variant for ranges below minrun (Q44).
- Does `sorted` call `__gt__`? CPython's list sort asks only for `<` (that is why the counter only defines `__lt__`).
- How would you count inversions in O(n log n)? During the merge: when a right item goes out before a left item, add the number of left items still waiting. The code does this.

**Common mistakes:**
- Saying insertion sort is O(n) on nearly sorted data without saying how nearly (it is O(n + inversions)).
- Forgetting the last failed comparison per item, so comparisons are not exactly the number of shifts.
- Using `>=` in the insertion loop: it moves equal items and loses stability.
- Claiming Timsort always beats insertion sort.
- Reading a Timsort count from a plain int list and assuming `__lt__` is called.

---

### Q44 ⭐ 🟡 Timsort ingredients: minrun and natural runs (editor-level description of CPython's algorithm, labelled as such: this exact description was not checked against the CPython source here). `nums` has 1 <= len <= 10^5 integers. Let n = len(nums). Compute `minrun(n)`: `r = 0; while n >= 64: r |= n & 1; n >>= 1` and return `n + r` (so for n < 64 it returns n). A natural run starting at position lo is the longest stretch that is either non-decreasing (a[i] >= a[i-1]) or strictly descending (a[i] < a[i-1]), decided by comparing a[lo + 1] with a[lo]; a run starting at the last position has length 1. Timsort scans from the left: the next run starts at lo and has length max(natural run length at lo, min(minrun, n - lo)) (short runs are extended to minrun by insertion sort), and the following run starts right after it. Return `[minrun, runs]`: the minrun value for n = len(nums) and the list of these run lengths in order. Explain why minrun lies between 32 and 64 for n >= 64 (and why, with s the number of right shifts the loop performs, n <= minrun * 2^s and minrun * 2^(s-1) < n, so n / minrun is never above a power of two and the merges stay balanced), why a strictly descending run is reversed (and why it must be STRICTLY descending to keep stability), and what the merge step with galloping adds. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a recursive scan that rebuilds the run boundaries on small inputs. Example: nums=[30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133] -> [32, [32, 32]]; nums=[9] -> [1, [1]]; nums=[4, 4, 4, 3] -> [4, [4]]; nums=[1, 2, 3, 2, 1, 0, 5, 6] -> [8, [8]].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)
**Label (read this first):** this is an editor-level description of CPython's Timsort. I tested my own implementation of the description (minrun and run scan) and claims about minrun for every n up to 10^5, but I did NOT check the description against the CPython source (`listobject.c`). Treat the galloping and merge-stack remarks below as interview-level knowledge, not verified facts.

**Pattern:** Run detection plus a minimum run length, the first stage of Timsort: find the existing order in the data, pad short runs, then merge runs of balanced size.

**Say this first (1 line):** "Timsort scans for natural runs, a non-decreasing stretch or a strictly descending one it can reverse; anything shorter than minrun, a value between 32 and 64 chosen from n, is padded up to minrun by insertion sort; then runs are merged so that the number of runs is about a power of two."

**Brute force:** A recursive scan that rebuilds the run boundaries from scratch (the code's `solve_rec`): at each start find the natural run, pad to min(minrun, remaining), recurse on the rest. It is the same logic written differently; there is no independent definition to test it against except the description in the question.

**Optimal:** (a single left-to-right scan, O(n))
- `minrun(n)`: while n >= 64, shift right and remember if any 1 bit fell off (`r |= n & 1`); return `n + r`. For n < 64 it returns n: the whole list is one insertion-sort job.
- Natural run at lo: if `a[lo+1] < a[lo]` the run is strictly descending and extends while `a[i] < a[i-1]`; otherwise it is non-decreasing and extends while `a[i] >= a[i-1]`. A run at the last position has length 1.
- Run length = `max(natural, min(minrun, n - lo))`; the next run starts right after it.
- Why 32 <= minrun <= 64 for n >= 64: the loop stops when the shifted value k is below 64, and it only ever shifts a value that was >= 64, so k >= 32. Then minrun = k or k + 1 is at most 64. Checked for every n up to 10^5.
- Why merges stay balanced: with s the number of shifts, `n <= minrun * 2^s` and `minrun * 2^(s-1) < n`. So n / minrun is at most the power of two 2^s and more than 2^(s-1): the runs, each about minrun long, can be merged pairwise like a balanced tree of depth s with no leftover tiny run. The sticky bit `r` rounds minrun up whenever a 1 bit was dropped, so that n / minrun does not creep just above a power of two (which would leave one tiny extra run to merge). Also verified for every n up to 10^5.
- Why a descending run is reversed: reversing makes it ascending in O(length) without comparisons. It must be STRICTLY descending: if equal items were allowed in a descending run, reversing would flip their original order and break stability. Equal neighbours therefore end the descending run. With `[4, 4, 4, 3]` the scan sees a non-decreasing run of three 4s then a 3: the run is length 3, padded to 4.
- Merge step (editor-level): runs go on a stack and are merged when their lengths break an invariant (each run longer than the sum of the next two, in the usual description), using a temporary array of the smaller run. Galloping mode: if one run keeps winning, the merge switches to exponential search ("gallop") to skip many items at once, which makes merging two runs where one dominates close to linear in the smaller run. That is why nearly-sorted data is cheap.

**Complexity:**
- Scan: O(n) time, O(number of runs) space for the run list. The number of runs is at most about n / minrun for random data (2041 runs for 10^5 random items with minrun 49) and 1 for sorted data.
- Whole Timsort (editor knowledge): O(n) best case, O(n log n) worst case, O(n) extra space, stable.

**Dry run:** the first example has 64 items: 30, 29, ..., 1, then 100, 101, ..., 133.
- n = 64: the loop `while n >= 64` runs once (64 >> 1 = 32, remembered bit 0), so minrun = 32.
- lo = 0: `a[1] = 29 < 30`, strictly descending. It continues down to the item 1 at index 29, then `a[30] = 100` is not below 1, stop: natural length 30. `max(30, min(32, 64)) = 32`, so the run is padded by 2 items (100 and 101), and insertion sort puts them in place after the reversal.
- lo = 32: `a[33] = 103 >= a[32] = 102`, non-decreasing to the end: length 32. `max(32, min(32, 32)) = 32`.
- Result `[32, [32, 32]]`.

**Code:**
```python
import random
random.seed(44)
# Editor-level description of Timsort's run detection (NOT checked against the CPython source here).

def minrun(n):
    r = 0
    while n >= 64:
        r |= n & 1                 # remember if any 1 bit was shifted out
        n >>= 1
    return n + r

def solve(nums):
    n = len(nums); mr = minrun(n); runs = []; lo = 0
    while lo < n:
        i = lo + 1
        if i < n:
            if nums[i] < nums[lo]:                              # strictly descending run
                while i < n and nums[i] < nums[i - 1]: i += 1
            else:                                               # non-decreasing run
                while i < n and nums[i] >= nums[i - 1]: i += 1
        length = max(i - lo, min(mr, n - lo))                   # short runs are padded to minrun by insertion sort
        runs.append(length); lo += length
    return [mr, runs]

# ---- recursive scan that rebuilds the run boundaries, written separately
def solve_rec(nums):
    n = len(nums)
    k, r = n, 0
    while k >= 64: r |= k & 1; k >>= 1
    m = k + r
    def natural(lo):
        if lo == n - 1: return 1
        desc = nums[lo + 1] < nums[lo]
        e = lo + 1
        while e < n and ((nums[e] < nums[e - 1]) if desc else (nums[e] >= nums[e - 1])): e += 1
        return e - lo
    def go(lo):
        if lo >= n: return []
        rl = max(natural(lo), min(m, n - lo))
        return [rl] + go(lo + rl)            # depth = number of runs: keep the lists small
    return [m, go(0)]

# ---- examples
ex1 = list(range(30, 0, -1)) + list(range(100, 134))
assert solve(ex1) == [32, [32, 32]]
assert solve([9]) == [1, [1]]
assert solve([4, 4, 4, 3]) == [4, [4]]
assert solve([1, 2, 3, 2, 1, 0, 5, 6]) == [8, [8]]
print('examples ok:', solve(ex1), solve([9]), solve([4, 4, 4, 3]), solve([1, 2, 3, 2, 1, 0, 5, 6]))

# ---- seeded random cross-check (short inputs so the recursion in solve_rec stays shallow)
for _ in range(3000):
    n = random.randint(1, 120)
    mode = random.choice(['rand', 'runs', 'few'])
    if mode == 'rand': t = [random.randint(0, 30) for _ in range(n)]
    elif mode == 'few': t = [random.randint(0, 2) for _ in range(n)]
    else:
        t = []
        while len(t) < n:
            L = random.randint(1, 40); s = random.randint(0, 100); d = random.choice([-1, 1, 0])
            t += [s + d * k for k in range(L)]
        t = t[:n]
    assert solve(t) == solve_rec(t), t
    mr, runs = solve(t); assert sum(runs) == n and all(r >= min(mr, n) or r == runs[-1] for r in runs)
print('3000 random inputs: scan == recursive rebuild; run lengths sum to n; every run but the last is >= minrun')

# ---- claims about minrun, checked for EVERY n up to 10^5
for n in range(1, 100001):
    m = minrun(n)
    if n < 64: assert m == n; continue
    k, s = n, 0
    while k >= 64: k >>= 1; s += 1
    assert 32 <= m <= 64
    assert n <= m * 2 ** s and m * 2 ** (s - 1) < n
print('every n in 1..100000: n < 64 -> minrun = n; n >= 64 -> 32 <= minrun <= 64, n <= minrun * 2^s and minrun * 2^(s-1) < n')
print('examples of minrun:', {n: minrun(n) for n in (63, 64, 65, 127, 128, 1000, 2048, 2049, 100000)})
print('n / minrun for some n (always <= the next power of two, here 2, 2, 16, 64, 2048):',
      {n: round(n / minrun(n), 3) for n in (65, 127, 1000, 2049, 100000)})

# ---- a run-structure demonstration at the maximum size
big = [random.randint(0, 10**9) for _ in range(100000)]
mr, runs = solve(big)
print('random 100000 items: minrun', mr, ', number of runs', len(runs), ', first runs', runs[:3], ', last run', runs[-1])
inc = list(range(100000)); mr, runs = solve(inc)
print('sorted 100000 items: runs', runs)

# ---- edge asserts
assert solve([2, 1]) == [2, [2]]
assert solve([3, 3, 3]) == [3, [3]]
assert minrun(64) == 32 and minrun(65) == 33 and minrun(127) == 64 and minrun(128) == 32
n = 130; t = list(range(100, 0, -1)) + list(range(30))       # 100..1 then 0..29
assert solve(t) == [33, [101, 29]]     # the 0 after 1 continues the strict descent
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [32, [32, 32]] [1, [1]] [4, [4]] [8, [8]]
3000 random inputs: scan == recursive rebuild; run lengths sum to n; every run but the last is >= minrun
every n in 1..100000: n < 64 -> minrun = n; n >= 64 -> 32 <= minrun <= 64, n <= minrun * 2^s and minrun * 2^(s-1) < n
examples of minrun: {63: 63, 64: 32, 65: 33, 127: 64, 128: 32, 1000: 63, 2048: 32, 2049: 33, 100000: 49}
n / minrun for some n (always <= the next power of two, here 2, 2, 16, 64, 2048): {65: 1.97, 127: 1.984, 1000: 15.873, 2049: 62.091, 100000: 2040.816}
random 100000 items: minrun 49 , number of runs 2041 , first runs [49, 49, 49] , last run 40
sorted 100000 items: runs [100000]
edge asserts ok
```

**Edge cases:**
- n = 1: minrun 1, one run of length 1.
- n < 64: always a single run [n]; Timsort is then just binary insertion sort after the first run.
- All equal: non-decreasing, one run.
- n = 64 gives minrun 32 (not 64); n = 65 gives 33 (the dropped bit is remembered); n = 127 gives 64.
- Strictly descending whole list: one run, reversed.
- Non-strict descent such as [4, 4, 3] is not a descending run (it is non-decreasing for 2 items, then breaks).

**Follow-ups:**
- Why not minrun = 64 always? Then n = 65 would give runs 64 + 1 and an unbalanced merge. The rounding rule keeps n / minrun at or below a power of two.
- Why a minimum run at all? Insertion sort on 32..64 items is cheaper than merging tiny runs, and it uses cache well.
- Is Timsort quicksort-like? No. It is a merge sort with run detection and insertion sort for short runs (Q43, Q16).

**Common mistakes:**
- Letting the descending run be non-strict, which breaks stability after the reversal.
- Treating `n // 64` as minrun.
- Forgetting the last item can be a run of length 1.
- Presenting galloping thresholds or the merge-stack invariant as verified facts; they are described from memory here.

---

### Q45 ⭐ 🟡 Big integers: Fibonacci by fast doubling. `n` is an integer with 0 <= n <= 10^5 (F(0) = 0, F(1) = 1). Return `[mod, digits, lead]`: F(n) modulo 10^9 + 7, the number of decimal digits of F(n) (F(n) itself has up to about 21000 digits), and the string of its first min(5, digits) decimal digits. Compute F(n) exactly with the doubling identities F(2k) = F(k) * (2 * F(k+1) - F(k)) and F(2k+1) = F(k)^2 + F(k+1)^2 (O(log n) big multiplications, recursion depth about 17), and compare with the O(n) additions of the simple loop. Python integers have unlimited size, but in recent Python versions (the limit appeared in 3.11, editor knowledge, not checked against a page; the default of 4300 digits is observed on 3.13) converting an int with more than 4300 decimal digits to a string with `str()` or `int(s)` raises ValueError by default (`sys.set_int_max_str_digits` changes the limit; the limit does not apply to power-of-two bases such as `hex`); state how you get the digit count and the leading digits for large n despite this (for example by raising the limit, or from the bit length and `math.log10`) and what the checker accepts: exact values only. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the O(n) addition loop with the digits counted by chunked division on small inputs. Example: n=10 -> [55, 2, '55']; n=0 -> [0, 1, '0']; n=100 -> [687995182, 21, '35422']; n=30000 -> [393965141, 6270, '19042'].
**Asked at:** Python documentation for int, float, Decimal and Fraction (docs.python.org fetch failed with ENOTFOUND, not opened; behaviour verified by running Python 3.13)
**Pattern:** Fast doubling (a divide and conquer on the exponent, like fast power) on Python's unbounded integers. It applies because F(2k) and F(2k+1) can be computed from F(k) and F(k+1) alone.

**Say this first (1 line):** "Python ints never overflow, so I compute F(n) exactly with the doubling identities in O(log n) big multiplications, take it mod 10^9 + 7 at the end, and get the digit count and leading digits without calling str() on a huge int, because that has a default limit of 4300 digits."

**Brute force:** Loop n additions: `a, b = b, a + b`. It is exact and simple, but O(n) big additions, each O(size of the number), so O(n^2) bit operations overall (F(10^5) is about 69,000 bits, 20899 digits). The code uses it as the checker, with digits counted by chunked division.

**Optimal:**
- `fib_pair(n)` returns `(F(n), F(n+1))`. Recurse on `n >> 1` to get `(a, b) = (F(k), F(k+1))`.
- `F(2k) = a * (2b - a)` and `F(2k+1) = a^2 + b^2`. If n is odd return `(F(2k+1), F(2k) + F(2k+1))`, else `(F(2k), F(2k+1))`.
- Depth is the bit length of n, 17 for n = 10^5: safe for the recursion limit. Base case `(0, 1)`.
- Mod 10^9 + 7: take `% MOD` of the exact value at the end. (If you only wanted the modulus, you could reduce at every step and keep numbers small; here the exact value is needed for the digits.)
- Digit count without `str()`: estimate `bit_length * log10(2)` (a float estimate), then correct it with exact comparisons against powers of ten (`x >= 10**d` raise, `x < 10**(d-1)` lower). Leading digits: `x // 10**(d - 5)` is an int below 10^5, so `str()` of it is safe.
- The limit: from Python 3.11 (editor knowledge, not checked against a page), `str(int)` and `int(str)` raise ValueError above 4300 digits by default. On 3.13 I observed the 4300 default and the ValueError for F(30000) (6270 digits) and for `int('9' * 5000)`. `sys.set_int_max_str_digits(0)` lifts it (the code does that once as a check and restores the old value); `hex()` is not affected because the limit applies to non-power-of-two bases. Exact values only are accepted, so no float estimate is the final answer: the float is used only as a starting guess and fixed by exact comparisons.

**Complexity:**
- Doubling: O(log n) multiplications of numbers up to about 0.694 * n bits. Each big multiplication is subquadratic (Karatsuba in CPython, editor knowledge), so the total is dominated by the last few steps, about O(M(n)) where M is the cost of one multiplication of n-bit numbers.
- Addition loop: n additions of numbers up to 0.694 n bits, O(n^2) bit operations overall.
- Space: O(n) bits for the result, O(log n) recursion frames.
- Sandbox timings, not proof: at n = 10^5 the doubling took about 0.002 s and the loop about 0.1 s.

**Dry run:** n = 10, binary 1010.
| call | k = n >> 1 | (F(k), F(k+1)) | result |
|---|---|---|---|
| fib_pair(0) | | | (0, 1) |
| fib_pair(1) | 0 | (0, 1) | F(0) = 0*(2*1-0) = 0, F(1) = 0 + 1 = 1; n odd -> (1, 0 + 1) = (1, 1) |
| fib_pair(2) | 1 | (1, 1) | F(2) = 1*(2-1) = 1, F(3) = 1 + 1 = 2; even -> (1, 2) |
| fib_pair(5) | 2 | (1, 2) | F(4) = 1*(4-1) = 3, F(5) = 1 + 4 = 5; odd -> (5, 3 + 5) = (5, 8) |
| fib_pair(10) | 5 | (5, 8) | F(10) = 5*(16-5) = 55, F(11) = 25 + 64 = 89; even -> (55, 89) |
F(10) = 55: mod 55, 2 digits, lead '55'.

**Code:**
```python
import sys, math, random, time
random.seed(45)
MOD = 10**9 + 7

# ---- fast doubling: returns (F(n), F(n+1)); depth = bit length of n (about 17 for 10^5)
def fib_pair(n):
    if n == 0: return 0, 1
    a, b = fib_pair(n >> 1)                 # a = F(k), b = F(k+1), k = n // 2
    c = a * (2 * b - a)                     # F(2k)
    d = a * a + b * b                       # F(2k+1)
    return (d, c + d) if n & 1 else (c, d)

def fib_loop(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a

# ---- digit count and leading digits WITHOUT calling str() on a huge int:
#      estimate from the bit length, then fix by an exact comparison with a power of ten
def digits_and_lead(x):
    if x == 0: return 1, '0'
    d = max(1, int(x.bit_length() * 0.30102999566398114))      # a lower estimate of the digit count
    while x >= 10 ** d: d += 1                                 # exact: d is the smallest with x < 10^d
    while d > 1 and x < 10 ** (d - 1): d -= 1
    k = max(0, d - 5)
    lead = x // 10 ** k                                        # the first min(5, d) digits, as an int < 10^5 (str is safe)
    return d, str(lead)

def solve(n):
    f = fib_pair(n)[0]
    dg, lead = digits_and_lead(f)
    return [f % MOD, dg, lead]

# ---- examples
assert solve(10) == [55, 2, '55']
assert solve(0) == [0, 1, '0']
assert solve(100) == [687995182, 21, '35422']
assert solve(30000) == [393965141, 6270, '19042']
print('examples ok:', solve(10), solve(0), solve(100), solve(30000))

# ---- cross-check: O(n) addition loop; digits counted by chunked division (no str on a big int)
def digits_chunked(x):
    if x == 0: return 1
    chunk = 10 ** 1000; count = 0
    while x >= chunk: x //= chunk; count += 1000
    return count + len(str(x))                  # the remainder has < 1001 digits, so str() is safe
for n in list(range(0, 400)) + [random.randint(400, 20000) for _ in range(60)]:
    f = fib_loop(n)
    assert fib_pair(n)[0] == f
    dg, lead = digits_and_lead(f)
    assert dg == digits_chunked(f)
    # leading digits independent check: divide away the low digits in 1000-digit chunks, then use str on the small rest
    y, rest = f, dg
    while rest > 1000: y //= 10 ** 1000; rest -= 1000
    assert lead == str(y)[:5], (n, lead)
    assert solve(n) == [f % MOD, dg, lead]
print('460 values of n (0..399 and 60 random up to 20000): doubling == addition loop; digits and leading digits agree with chunked division')

# ---- the int-to-str digit limit (observed on this Python; the 3.11 introduction is editor knowledge)
big = fib_pair(30000)[0]
print('default limit:', sys.get_int_max_str_digits(), '; F(30000) has', digits_and_lead(big)[0], 'digits')
try: str(big)
except ValueError as e: print('str(F(30000)) ->', type(e).__name__)
try: int('9' * 5000)
except ValueError as e: print("int('9' * 5000) ->", type(e).__name__)
print('hex works (power-of-two base):', len(hex(big)), 'characters; bit_length', big.bit_length())
old = sys.get_int_max_str_digits(); sys.set_int_max_str_digits(0)
assert len(str(big)) == 6270 and str(big)[:5] == '19042'
sys.set_int_max_str_digits(old)
print('with the limit lifted str() gives the same 6270 digits and lead 19042; limit restored to', sys.get_int_max_str_digits())

# ---- maximum size and the cost shape (sandbox timings, not proof of big-O)
t = time.perf_counter(); r = solve(100000); t1 = time.perf_counter() - t
t = time.perf_counter(); f = fib_loop(100000); t2 = time.perf_counter() - t
assert f == fib_pair(100000)[0] and r[0] == f % MOD
print('n = 100000:', r, ', digits by length-estimate method;  (sandbox timing) doubling %.4f s, addition loop %.4f s' % (t1, t2))

# ---- Binet's formula in floats: where does it first go wrong?
a = 0
for n in range(200):
    if round(((1 + 5 ** 0.5) / 2) ** n / 5 ** 0.5) != fib_pair(n)[0]: break
print('float Binet first differs from the exact value at n =', n)

# ---- edge asserts
assert solve(1) == [1, 1, '1'] and solve(2) == [1, 1, '1'] and solve(5) == [5, 1, '5']
assert solve(12) == [144, 3, '144'] and solve(20) == [6765, 4, '6765']
assert fib_pair(0) == (0, 1) and fib_pair(1) == (1, 1)
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [55, 2, '55'] [0, 1, '0'] [687995182, 21, '35422'] [393965141, 6270, '19042']
460 values of n (0..399 and 60 random up to 20000): doubling == addition loop; digits and leading digits agree with chunked division
default limit: 4300 ; F(30000) has 6270 digits
str(F(30000)) -> ValueError
int('9' * 5000) -> ValueError
hex works (power-of-two base): 5209 characters; bit_length 20827
with the limit lifted str() gives the same 6270 digits and lead 19042; limit restored to 4300
n = 100000: [911435502, 20899, '25974'] , digits by length-estimate method;  (sandbox timing) doubling 0.0028 s, addition loop 0.1340 s
float Binet first differs from the exact value at n = 71
edge asserts ok
```

**Edge cases:**
- n = 0: F = 0, which has 1 digit and lead '0'. n = 1 and 2: F = 1.
- Fewer than 5 digits: the lead is the whole number (`10**0 = 1` divisor).
- Digit count near a power of ten: the estimate can be off by one, which is why the comparisons with `10**d` are exact.
- Doing `str(F(30000))` directly: ValueError on the default setting.
- Applying `% MOD` inside the identities: `2*b - a` can go negative when reduced, fix with `+ MOD` (not needed here because the exact value is used).

**Follow-ups:**
- Fibonacci mod m only, for huge n (10^18)? Same doubling with every product reduced mod m. Or the matrix power of [[1, 1], [1, 0]].
- Why not Binet's formula? Floats lose precision: the float version first gives a wrong value at n = 71 in my run.
- Is the pisano period relevant? For a single known modulus it can shorten n, but doubling is already O(log n).

**Common mistakes:**
- Calling `str()` on a 6000-digit number and getting ValueError.
- Using `len(str(...))` after setting the limit to 0 for untrusted input (the limit exists to stop denial of service on parsing).
- Using floats for the digit count and trusting them without an exact check.
- Reducing mod in the middle and then trying to read digits from the reduced value.

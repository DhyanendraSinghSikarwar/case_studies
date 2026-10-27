### Q34 ⭐⭐ 🔴 Candy. `ratings` (1 <= len <= 2*10^4, values in [0, 2*10^4]) are the ratings of children in a row. Give each child at least one candy so that a child with a strictly higher rating than an adjacent child gets strictly more candy than that neighbour (equal ratings impose nothing). Return the minimum total number of candies. Give the two-pass greedy (left to right for the rising constraint, right to left taking the max for the falling one), say why the max keeps the first pass valid, and mention that O(1) extra space is possible by counting slope lengths. Exercise the plateau case [1, 2, 2] and the valley case [3, 2, 1, 2, 3]. Example: ratings=[1, 0, 2] -> 5; ratings=[1, 2, 2] -> 4; ratings=[3, 2, 1, 2, 3] -> 11; ratings=[5] -> 1.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy with two independent one-directional constraints. Each pass fixes one neighbour relation; combining them with `max` satisfies both.

**Say this first (1 line):** "Everyone starts with 1. Left to right I satisfy 'higher than the left neighbour', right to left I satisfy 'higher than the right neighbour' and keep the max, so it is O(n) and minimal."

**Brute force:** Try every candy vector with values 1..n and keep the cheapest valid one. That is n^n vectors, so it only runs for n <= 6. It is the cross-check, not an answer.

**Optimal:**
- Pass 1, left to right: if `r[i] > r[i-1]` then `c[i] = c[i-1] + 1`, else it stays 1. Rising runs get 1, 2, 3...
- Pass 2, right to left: if `r[i] > r[i+1]` then `c[i] = max(c[i], c[i+1] + 1)`.
- Why the max keeps pass 1 valid: pass 2 only ever raises a value or leaves it. A pair `(i-1, i)` that was fine because `c[i] > c[i-1]` stays fine when `c[i]` goes up. If pass 2 raises `c[i-1]` it does so only when `r[i-1] > r[i]`, and then the pair needs nothing from the rising side. Overwriting instead of taking the max could lower a value pass 1 needed.
- Why it is minimal: the value at `i` is the larger of two forced chain lengths (strict rises ending at `i` from the left, strict falls from `i` to the right); nothing forces more.
- Plateau: equal ratings impose nothing, so the run resets (`[1, 2, 2]` gets `1, 2, 1`).
- O(1) extra space: walk the slopes. Keep `up` (current rising length), `down` (current falling length) and `peak` (the rise that led into the current fall). A rise adds `1 + up`. A plateau adds 1 and resets all three. A fall adds `down`, plus 1 more when the fall becomes longer than the rise (the peak child must exceed both sides).

**Complexity:** Time O(n): two linear passes (one for the slope version). Space O(n) for the candy array, O(1) extra for the slope version. Brute force is O(n^n * n).

**Dry run:** `[3, 2, 1, 2, 3]`.
- Pass 1 (rising only): `[1, 1, 1, 2, 3]`.
- Pass 2 from the right: index 3 (2) is not above index 4 (3): unchanged. Index 2 (1) is not above index 3: unchanged. Index 1 (2) is above index 2 (1): `max(1, 1+1) = 2`. Index 0 (3) is above index 1: `max(1, 2+1) = 3`.
- Candies `[3, 2, 1, 2, 3]`, total 11. The valley child gets 1 and both sides climb.

**Code:**
```python
import itertools
import random

random.seed(34)

def candy_brute(r):
    """Try every candy vector with values 1..n (n <= 6 only)."""
    n, best = len(r), None
    for c in itertools.product(range(1, n + 1), repeat=n):
        if all((r[i + 1] <= r[i] or c[i + 1] > c[i]) and (r[i] <= r[i + 1] or c[i] > c[i + 1]) for i in range(n - 1)):
            if best is None or sum(c) < best:
                best = sum(c)
    return best

def candy_two_pass(r):
    n = len(r)
    c = [1] * n
    for i in range(1, n):                      # pass 1: rising constraint
        if r[i] > r[i - 1]:
            c[i] = c[i - 1] + 1
    for i in range(n - 2, -1, -1):             # pass 2: falling constraint, keep the max
        if r[i] > r[i + 1]:
            c[i] = max(c[i], c[i + 1] + 1)
    return sum(c)

def candy_o1(r):
    """O(1) extra space: walk slopes. up = current rising run, down = current falling run, peak = up at the top."""
    n = len(r)
    total = 1
    up = down = peak = 0
    for i in range(1, n):
        if r[i] > r[i - 1]:
            up += 1; peak = up; down = 0
            total += 1 + up
        elif r[i] == r[i - 1]:
            up = down = peak = 0
            total += 1
        else:
            up = 0; down += 1
            # new bottom child gets 1 and every child above it on the slope gets +1 (that is `down`);
            # once the fall is longer than the rise, the peak child needs one more too
            total += down + (0 if down <= peak else 1)
    return total

# ---- examples
assert candy_two_pass([1, 0, 2]) == 5
assert candy_two_pass([1, 2, 2]) == 4          # plateau: the second 2 only needs 1
assert candy_two_pass([3, 2, 1, 2, 3]) == 11   # valley: 3+2+1+2+3
assert candy_two_pass([5]) == 1
for r in ([1, 0, 2], [1, 2, 2], [3, 2, 1, 2, 3], [5]):
    print(r, candy_two_pass(r), candy_o1(r))

# ---- why the max: pass 1 alone breaks the falling side, pass 2 alone breaks the rising side
r = [1, 3, 2, 1]
p1 = [1] * 4
for i in range(1, 4):
    if r[i] > r[i - 1]: p1[i] = p1[i - 1] + 1
print('after pass 1 only', p1, 'falling pair 2>1 satisfied?', p1[2] > p1[3])
# the peak 3 gets max(2, 3) = 3 in pass 2, never less than what pass 1 gave it
print('two-pass total', candy_two_pass(r))

# ---- exhaustive: all rating arrays of length <= 6 over {0,1,2}, plus seeded random of ratings 0..3
checked = 0
for n in range(1, 7):
    for r in itertools.product(range(3), repeat=n):
        r = list(r)
        a = candy_two_pass(r)
        assert a == candy_brute(r) == candy_o1(r), r
        checked += 1
for _ in range(300):
    r = [random.randint(0, 3) for _ in range(random.randint(1, 6))]
    assert candy_two_pass(r) == candy_brute(r) == candy_o1(r), r
    checked += 1
print('cross-checked', checked, 'arrays')

# ---- bigger: O(1) variant agrees with two-pass on large random and structured inputs
for _ in range(200):
    r = [random.randint(0, 20000) for _ in range(random.randint(1, 300))]
    assert candy_two_pass(r) == candy_o1(r)
n = 2 * 10 ** 4
assert candy_two_pass(list(range(n))) == n * (n + 1) // 2        # strictly rising: 1+2+...+n
assert candy_two_pass(list(range(n, 0, -1))) == n * (n + 1) // 2  # strictly falling
assert candy_two_pass([7] * n) == n                                # all equal: one each
assert candy_o1(list(range(n))) == n * (n + 1) // 2 and candy_o1([7] * n) == n
print('max-size edge cases ok, rising total', candy_two_pass(list(range(n))))
```

**Output (my run):**
```
[1, 0, 2] 5 5
[1, 2, 2] 4 4
[3, 2, 1, 2, 3] 11 11
[5] 1 1
after pass 1 only [1, 2, 1, 1] falling pair 2>1 satisfied? False
two-pass total 7
cross-checked 1392 arrays
max-size edge cases ok, rising total 200010000
```

**Edge cases:**
- One child: 1.
- All equal: n candies.
- Strictly rising or strictly falling: n(n+1)/2, which is 200,010,000 for n = 20,000. Python integers do not overflow.
- Plateau beside a peak: `[1, 2, 2]` is 4, not 5.
- Valley with unequal sides: the max in pass 2 must not lower a pass-1 value.
- Zero ratings are fine; only comparisons matter.

**Follow-ups:**
- *Why not one pass with the array?* A fall's height is only known once you see where it ends, so one left-to-right array pass cannot fix the peak. The slope-count version is one pass because it repairs the peak by adding 1 when the fall outgrows the rise.
- *Circular row?* Start from a child whose rating is not above either neighbour (a global minimum): that child can have 1, then unroll the circle from there and run the same method.
- *Different rule: equal ratings must get equal candy?* Different problem. Ask before assuming; the plain two-pass is not guaranteed correct for it.

**Common mistakes:**
- Overwriting in pass 2 instead of taking `max`: `[1, 2, 3, 1]` would lose the 3 the rise needed.
- Treating equal ratings as needing more candy, or as needing equal candy. Neither is stated.
- Starting everyone at 0, or running pass 2 from `n-1` and reading `c[n]`.
- In the O(1) version, forgetting the extra 1 for the peak when `down > peak`, or not resetting on a plateau.

### Q35 ⭐⭐ 🔴 Employee free time. `schedule` is a list with one entry per employee (1 <= employees <= 50); each entry is a list of that employee's busy CLOSED intervals [start, end] (integers, start < end), sorted by start and disjoint within the employee, at most 50 per employee. Return the list of intervals during which EVERY employee is free: gaps of positive length strictly between the merged busy periods of all employees, sorted; the unbounded time before the earliest start and after the latest end is NOT reported, and two busy intervals that touch at a point leave no gap. Merge by flattening and sorting (O(N log N)) or by a heap of (next start, employee, index) over the k sorted lists (O(N log k)); say which you pick and why the heap version is the one this part's pattern points to. Example: schedule=[[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]] -> [[3, 4]]; schedule=[[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]] -> [[5, 6], [7, 9]]; schedule=[[[1, 5]], [[5, 8]]] -> []; schedule=[[[1, 2]]] -> [].
**Asked at:** Interval pattern guides on techinterview.org (merge, insert, meeting rooms, employee free time, interval scheduling; search snippets only, not opened; the site's own 'asked at' lists were not verified) | Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Merge k sorted lists (heap of heads), then fold into merged busy time and report the gaps. Closed intervals: touching means no gap.

**Say this first (1 line):** "Everyone's free time is the gaps in the union of all busy intervals. I merge the k sorted lists with a heap of next starts, keep the running end of the busy block, and every time the next start is strictly after that end I report a gap."

**Brute force:** Mark every unit cell between the earliest start and the latest end as busy or free, then read off runs of free cells. It is O(range * N) and breaks when times are huge. It is the cross-check in the code.

**Optimal:**
- Two ways to get the intervals in start order:
  - Flatten and sort: O(N log N), where N is the total number of intervals. Simple, and fine for N <= 2500 here.
  - Heap of `(next start, employee, index)` over k sorted lists: O(N log k). It uses the fact that each employee's list is already sorted.
- I pick the heap version when asked, because it is this part's merge-k pattern and it scales when k is small and N is huge. I would say the sort is shorter to write and, with k <= 50 and N <= 2500 here, equally fast in practice.
- Fold: keep `end` = the furthest end so far. For the next interval `[s, e]`: if `s > end` there is a gap `[end, s]`. Then `end = max(end, e)`. Use `>`, not `>=`: closed intervals that touch at a point leave no gap of positive length.
- The time before the first start and after the last end is not reported, so there is nothing to add at the ends.
- Heap tie-breaking: when two employees start at the same time, the tuple compares the employee index next, which is an int and unique. Never put an unorderable object (a dict, a custom class) in the tuple without a unique int before it; the code shows the `TypeError`.

**Complexity:** Heap version: each of the N intervals is pushed and popped once at O(log k), so O(N log k) time, O(k) heap space plus the output. Sort version: O(N log N) time, O(N) space.

**Dry run:** `[[[1,3],[6,7]], [[2,4]], [[2,5],[9,12]]]`.
- Heap starts: `(1,0,0)`, `(2,1,0)`, `(2,2,0)`. Pop `(1,0,0)`: end = 3. Push `(6,0,1)`.
- Pop `(2,1,0)`: 2 <= 3, end = 4. Pop `(2,2,0)`: 2 <= 4, end = 5. Push `(9,2,1)`.
- Pop `(6,0,1)`: 6 > 5, gap `[5, 6]`, end = 7. Pop `(9,2,1)`: 9 > 7, gap `[7, 9]`, end = 12.
- Answer `[[5, 6], [7, 9]]`.

**Code:**
```python
import heapq
import random

random.seed(35)

def free_brute(schedule):
    """Unit-cell sweep: cell [t, t+1] is free if no busy interval covers it."""
    iv = [x for emp in schedule for x in emp]
    lo = min(s for s, e in iv); hi = max(e for s, e in iv)
    free = [not any(s <= t and t + 1 <= e for s, e in iv) for t in range(lo, hi)]
    out, t = [], 0
    while t < len(free):
        if free[t]:
            u = t
            while u < len(free) and free[u]:
                u += 1
            out.append([lo + t, lo + u]); t = u
        else:
            t += 1
    return out

def free_sort(schedule):
    iv = sorted(x for emp in schedule for x in emp)       # O(N log N), ignores that each list is already sorted
    out, end = [], iv[0][1]
    for s, e in iv[1:]:
        if s > end:
            out.append([end, s])
        end = max(end, e)
    return out

def free_heap(schedule):
    """k-way merge: heap holds (next start, employee, index). Employee index is unique, so the tuple never ties past it."""
    h = [(emp[0][0], i, 0) for i, emp in enumerate(schedule) if emp]
    heapq.heapify(h)
    out, end = [], None
    while h:
        s, i, j = heapq.heappop(h)
        e = schedule[i][j][1]
        if end is None:
            end = e
        else:
            if s > end:
                out.append([end, s])
            end = max(end, e)
        if j + 1 < len(schedule[i]):
            heapq.heappush(h, (schedule[i][j + 1][0], i, j + 1))
    return out

# ---- examples
ex = [
    ([[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]], [[3, 4]]),
    ([[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]], [[5, 6], [7, 9]]),
    ([[[1, 5]], [[5, 8]]], []),
    ([[[1, 2]]], []),
]
for sch, want in ex:
    assert free_sort(sch) == free_heap(sch) == free_brute(sch) == want, (sch, want)
    print(sch, '->', free_heap(sch))

# ---- tie-breaking: two employees start at the same time. (start, employee, index) is always orderable.
h = []
heapq.heappush(h, (1, 0, 0)); heapq.heappush(h, (1, 1, 0))
print('ties resolved by employee index:', heapq.heappop(h), heapq.heappop(h))
try:                                   # what goes wrong if the payload is an unorderable object
    h = []
    heapq.heappush(h, (1, {'emp': 0})); heapq.heappush(h, (1, {'emp': 1}))
except TypeError as e:
    print('TypeError on tied start with dict payload:', e)

# ---- random cross-check: valid schedule = per employee sorted, disjoint, start < end (touching allowed)
def rand_schedule():
    sch = []
    for _ in range(random.randint(1, 4)):
        t, emp = random.randint(0, 3), []
        for _ in range(random.randint(0, 3)):
            s = t + random.randint(0, 3); e = s + random.randint(1, 4)
            emp.append([s, e]); t = e + random.randint(0, 2)     # 0 gap = touching intervals inside one employee
        sch.append(emp)
    return sch if any(sch) else [[[0, 1]]]
for _ in range(1500):
    sch = rand_schedule()
    assert free_sort(sch) == free_heap(sch) == free_brute(sch), sch
print('1500 random schedules agree (sort, heap, unit-cell brute force)')

# ---- edge asserts
assert free_heap([[[1, 4]], [[2, 3]]]) == []                         # nested
assert free_heap([[[1, 2]], [[3, 4]], [[5, 6]]]) == [[2, 3], [4, 5]]
assert free_heap([[], [[1, 2], [4, 5]]]) == [[2, 4]]                 # an employee with no busy time
assert free_heap([[[1, 2], [2, 3]]]) == []                           # touching inside one employee
# size: 50 employees x 50 intervals
big = [[[100 * j + 10 * i, 100 * j + 10 * i + 5] for j in range(50)] for i in range(50)]
assert free_heap(big) == free_sort(big) == free_brute(big)
print('50x50 intervals gaps:', len(free_heap(big)), 'same as sort version:', free_heap(big) == free_sort(big))
```

**Output (my run):**
```
[[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]] -> [[3, 4]]
[[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]] -> [[5, 6], [7, 9]]
[[[1, 5]], [[5, 8]]] -> []
[[[1, 2]]] -> []
ties resolved by employee index: (1, 0, 0) (1, 1, 0)
TypeError on tied start with dict payload: '<' not supported between instances of 'dict' and 'dict'
1500 random schedules agree (sort, heap, unit-cell brute force)
50x50 intervals gaps: 539 same as sort version: True
```

**Edge cases:**
- One employee with one interval: no gaps, empty list.
- Touching `[1,5]` and `[5,8]`: no gap.
- A nested interval (`[2,3]` inside `[1,4]`): the `max` on `end` stops it from shrinking the busy block.
- Intervals of different employees that overlap heavily: the running end only grows.
- An employee with no busy intervals at all: the code skips that employee (the prompt does not promise lists are non-empty).
- Time before the earliest start and after the latest end is never reported.

**Follow-ups:**
- *Why not just merge each employee separately and then intersect free times?* It works but is more code. Merging all busy time and reading the gaps is one pass.
- *Open or half-open intervals?* The test changes: for half-open `[s, e)` touching also leaves no gap, but a zero-length gap is never reported anyway. State the convention first.
- *Unsorted inner lists?* Then the heap trick is invalid; sort each list first or just flatten and sort.

**Common mistakes:**
- `s >= end` instead of `s > end`: reports zero-width gaps or, for touching intervals, a false gap.
- Setting `end = e` instead of `end = max(end, e)`, which breaks on nested intervals.
- Reporting the time before the earliest start or after the latest end.
- Pushing `(start, interval_list)` or `(start, object)` to the heap: tied starts compare the second item and can raise `TypeError`.

### Q36 ⭐ 🟡 Quickselect with three-way partitioning: exact rounds. Given integers `nums` (1 <= len <= 10^5) and 1 <= k <= len, find the k-th largest value (duplicates counted) with this exact scheme: the pivot is the FIRST element of the current list; build three lists in order, gt (strictly greater than the pivot), eq (equal) and lt (strictly smaller); if k <= len(gt) continue in gt, else if k <= len(gt) + len(eq) the pivot is the answer, else continue in lt with k reduced by len(gt) + len(eq). Every pivot choice is one round. Return [value, rounds]. Explain why the all-equal input finishes in exactly 1 round with three-way partitioning (a two-way Lomuto scheme would need n), why an ascending list with k = 1 takes len rounds (quadratic work) with this first-element pivot, and why a random pivot makes the expected work O(n). Example: nums=[3, 2, 1, 5, 6, 4], k=2 -> [5, 2]; nums=[5, 5, 5, 5], k=3 -> [5, 1]; nums=[1, 2, 3, 4, 5], k=1 -> [5, 5]; nums=[9], k=1 -> [9, 1].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Selection by partitioning (quickselect). It is the heap-free way to answer "k-th largest" and sits next to the size-k heap in this part.

**Say this first (1 line):** "Pick the first element as pivot, split into greater, equal and smaller, and recurse into only the one side that holds rank k. Three-way splitting makes duplicates cheap; a random pivot makes the expected work linear."

**Brute force:** Sort descending and take index `k-1`: O(n log n). A size-k min-heap is O(n log k). Both are fine answers; quickselect is the O(n) expected one.

**Optimal:**
- One round: `p = seg[0]`, then `gt`, `eq`, `lt` in order of appearance. Let `g = len(gt)` and `e = len(eq)`.
- If `k <= g`: the answer is among the larger values, continue in `gt`.
- Else if `k <= g + e`: the answer is `p`. Stop and return `[p, rounds]`.
- Else: continue in `lt` with `k -= g + e`.
- Loop, not recursion, so no recursion-limit issue at n = 10^5.
- All-equal input: `gt` and `lt` are empty and `eq` is everything, so `k <= g + e` on the first round. One round for any n and k. A two-way partition has no `eq` list: with equals sent to one side, the pivot only gets rid of itself. The code measures this at n = 3000: with equals on the small side it takes 1, 1500, 3000 rounds for k = 1, n/2, n (and 3000, 1501, 1 with equals on the big side). So "n rounds" is the worst k, not every k.
- Ascending list, k = 1, first-element pivot: the pivot is the minimum, so `gt` is everything else. Sizes go n, n-1, ..., 1 and the round count is n; work is about n(n+1)/2 element visits per list scan, which is O(n^2). The prompt allows n = 10^5, so this input would be about 5 * 10^9 visits: too slow, which is the reason to randomise.
- Random pivot: with probability at least 1/2 the pivot lands in the middle half of the ranks, so the next segment is at most 3/4 of the current one. Expected sizes shrink geometrically: n + 3n/4 + (3/4)^2 n ... = O(n) expected. Worst case stays O(n^2) with negligible probability; median-of-medians gives worst-case O(n) but is rarely worth writing in an interview.

**Complexity:** Time: O(n) per round (three list scans). First-element pivot: O(n) expected on random data, O(n^2) worst (sorted input). Random pivot: expected O(n), worst O(n^2). Space O(n) for the three lists (an in-place version is O(1) extra).

**Dry run:** `[3, 2, 1, 5, 6, 4]`, k = 2.
- Round 1: pivot 3. `gt = [5, 6, 4]`, `eq = [3]`, `lt = [2, 1]`. k = 2 <= 3, continue in `gt`.
- Round 2: pivot 5. `gt = [6]`, `eq = [5]`. k = 2 > 1 and k <= 2: answer 5.
- Result `[5, 2]`.

**Code:**
```python
import random

random.seed(36)

def quickselect_rounds(nums, k):
    """k-th largest by first-element pivot and three-way partition. Returns [value, rounds]."""
    seg = list(nums)
    rounds = 0
    while True:
        p = seg[0]
        rounds += 1
        gt = [x for x in seg if x > p]
        eq = [x for x in seg if x == p]
        lt = [x for x in seg if x < p]
        if k <= len(gt):
            seg = gt
        elif k <= len(gt) + len(eq):
            return [p, rounds]
        else:
            k -= len(gt) + len(eq)
            seg = lt

def kth_brute(nums, k):
    return sorted(nums, reverse=True)[k - 1]

def two_way_rounds(nums, k, equals_go_small):
    """Two-way partition with the first element as pivot: only 'big' and 'small' lists, so equal keys cannot be
    finished off together. Equals go to the small side (or the big side). Returns [value, rounds]."""
    seg, rounds = list(nums), 0
    while True:
        p, rest = seg[0], seg[1:]
        rounds += 1
        if equals_go_small:
            big = [x for x in rest if x > p]; small = [x for x in rest if x <= p]
        else:
            big = [x for x in rest if x >= p]; small = [x for x in rest if x < p]
        if k == len(big) + 1:
            return [p, rounds]
        if k <= len(big):
            seg = big
        else:
            k -= len(big) + 1; seg = small

def quickselect_random(nums, k, rng):
    """Same scheme with a random pivot; returns [value, rounds]."""
    seg = list(nums)
    rounds = 0
    while True:
        p = seg[rng.randrange(len(seg))]
        rounds += 1
        gt = [x for x in seg if x > p]
        eq = [x for x in seg if x == p]
        lt = [x for x in seg if x < p]
        if k <= len(gt):
            seg = gt
        elif k <= len(gt) + len(eq):
            return [p, rounds]
        else:
            k -= len(gt) + len(eq)
            seg = lt

# ---- examples
for nums, k, want in [([3, 2, 1, 5, 6, 4], 2, [5, 2]), ([5, 5, 5, 5], 3, [5, 1]),
                      ([1, 2, 3, 4, 5], 1, [5, 5]), ([9], 1, [9, 1])]:
    got = quickselect_rounds(nums, k)
    assert got == want, (nums, k, got, want)
    print(nums, k, '->', got)

# ---- seeded cross-check against sorting (heavy duplicates)
for _ in range(2000):
    nums = [random.randint(0, 6) for _ in range(random.randint(1, 12))]
    k = random.randint(1, len(nums))
    v, r = quickselect_rounds(nums, k)
    assert v == kth_brute(nums, k) and 1 <= r <= len(nums), (nums, k)
    assert quickselect_random(nums, k, random.Random(1))[0] == v
print('2000 random lists agree with sorted()')

# ---- the claims
for n in (1, 5, 50, 500, 5000):
    assert quickselect_rounds([7] * n, max(1, n // 2)) == [7, 1]          # all equal: 1 round, any n
n = 3000
for k in (1, n // 2, n):
    assert quickselect_rounds([7] * n, k)[1] == 1
print('all-equal n=3000: three-way rounds for k=1, n/2, n:', [quickselect_rounds([7] * n, k)[1] for k in (1, n // 2, n)])
print('two-way (equals to small side) rounds for k=1, n/2, n:', [two_way_rounds([7] * n, k, True)[1] for k in (1, n // 2, n)])
print('two-way (equals to big side) rounds for k=1, n/2, n:  ', [two_way_rounds([7] * n, k, False)[1] for k in (1, n // 2, n)])
for _ in range(500):   # two-way version is still correct, just not duplicate-proof
    nums = [random.randint(0, 4) for _ in range(random.randint(1, 10))]; k = random.randint(1, len(nums))
    assert two_way_rounds(nums, k, True)[0] == two_way_rounds(nums, k, False)[0] == kth_brute(nums, k)
print('all-equal input: three-way always 1 round for any n and k')
for n in (1, 5, 50, 500, 2000):
    assert quickselect_rounds(list(range(1, n + 1)), 1) == [n, n]         # ascending, k=1: n rounds
print('ascending, k=1: rounds == n for n = 1..2000')

n = 2000
asc = list(range(1, n + 1))
rng = random.Random(7)
rounds_random = [quickselect_random(asc, 1, rng)[1] for _ in range(200)]
print('n=2000 ascending, k=1: first-element pivot rounds =', quickselect_rounds(asc, 1)[1],
      '| random pivot rounds avg =', round(sum(rounds_random) / 200, 1), 'max =', max(rounds_random))

# n = 10^5 random data: first-element pivot is fine on random input
data = [random.randint(0, 10 ** 9) for _ in range(10 ** 5)]
v, r = quickselect_rounds(data, 10 ** 5 // 2)
assert v == kth_brute(data, 10 ** 5 // 2)
print('n=1e5 random values, median: rounds =', r, '(round count only; no timing claim)')
```

**Output (my run):**
```
[3, 2, 1, 5, 6, 4] 2 -> [5, 2]
[5, 5, 5, 5] 3 -> [5, 1]
[1, 2, 3, 4, 5] 1 -> [5, 5]
[9] 1 -> [9, 1]
2000 random lists agree with sorted()
all-equal n=3000: three-way rounds for k=1, n/2, n: [1, 1, 1]
two-way (equals to small side) rounds for k=1, n/2, n: [1, 1500, 3000]
two-way (equals to big side) rounds for k=1, n/2, n:   [3000, 1501, 1]
all-equal input: three-way always 1 round for any n and k
ascending, k=1: rounds == n for n = 1..2000
n=2000 ascending, k=1: first-element pivot rounds = 2000 | random pivot rounds avg = 8.2 max = 16
n=1e5 random values, median: rounds = 18 (round count only; no timing claim)
```

**Edge cases:**
- Single element: 1 round.
- k = 1 (maximum) and k = n (minimum): both work; ascending/descending input decides the round count.
- Heavy duplicates: the `eq` list ends the search the moment k falls inside it.
- Negative numbers: only comparisons are used.
- Mixed `k` with all-equal values: still 1 round.

**Follow-ups:**
- *Why not just `heapq.nlargest`?* It is O(n log k), simple and stable. Quickselect is O(n) expected but mutates or copies, is unstable in terms of identity, and has a quadratic tail.
- *Does it need the whole array in memory?* Yes. For a stream or data bigger than memory use the size-k heap.
- *How to guarantee worst-case linear time?* Median-of-medians pivot. The constants are large, so it is mostly theory in interviews.

**Common mistakes:**
- Two-way partition with duplicates: slow on all-equal input.
- Forgetting `k -= len(gt) + len(eq)` when going into `lt`.
- Mixing up k-th largest and k-th smallest: here `gt` (larger values) is checked first.
- Claiming first-element pivot is O(n) because it is on random data. Sorted input is the counter-example.

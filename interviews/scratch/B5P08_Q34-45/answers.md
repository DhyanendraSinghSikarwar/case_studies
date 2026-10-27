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

### Q36 ⭐ 🟡 Quickselect with three-way partitioning: exact rounds. Given integers `nums` (1 <= len <= 10^5) and 1 <= k <= len, find the k-th largest value (duplicates counted) with this exact scheme: the pivot is the FIRST element of the current list; build three lists in order, gt (strictly greater than the pivot), eq (equal) and lt (strictly smaller); if k <= len(gt) continue in gt, else if k <= len(gt) + len(eq) the pivot is the answer, else continue in lt with k reduced by len(gt) + len(eq). Every pivot choice is one round. Return [value, rounds]. Explain why the all-equal input finishes in exactly 1 round with three-way partitioning (a two-way scheme that sends every equal value to the same side needs up to n rounds, depending on k and on which side takes the equals), why an ascending list with k = 1 takes len rounds (quadratic work) with this first-element pivot, and why a random pivot makes the expected work O(n). Example: nums=[3, 2, 1, 5, 6, 4], k=2 -> [5, 2]; nums=[5, 5, 5, 5], k=3 -> [5, 1]; nums=[1, 2, 3, 4, 5], k=1 -> [5, 5]; nums=[9], k=1 -> [9, 1].
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
- Ascending list, k = 1, first-element pivot: the pivot is the minimum, so `gt` is everything else. Sizes go n, n-1, ..., 1 and the round count is n; each round scans its whole segment, so the total is about n(n+1)/2 element visits per scan, which is O(n^2). The prompt allows n = 10^5, so this input would be about 5 * 10^9 visits: too slow, which is the reason to randomise.
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
- *Why not just `heapq.nlargest`?* It is O(n log k), simple and stable. Quickselect is O(n) expected, but it needs the whole array in memory, copies (or mutates) it, and has a quadratic worst case.
- *Does it need the whole array in memory?* Yes. For a stream or data bigger than memory use the size-k heap.
- *How to guarantee worst-case linear time?* Median-of-medians pivot. The constants are large, so it is mostly theory in interviews.

**Common mistakes:**
- Two-way partition with duplicates: slow on all-equal input.
- Forgetting `k -= len(gt) + len(eq)` when going into `lt`.
- Mixing up k-th largest and k-th smallest: here `gt` (larger values) is checked first.
- Claiming first-element pivot is O(n) because it is on random data. Sorted input is the counter-example.

### Q37 ⭐ 🟡 heapq.nlargest and stability. `records` is a list of [name, score] (0 <= len <= 10^4, names are distinct strings, scores integers) and k >= 1. Return the names of the k highest scores (fewer if there are fewer records), highest first, with ties between equal scores broken by earlier position in `records` first. Use `heapq.nlargest(k, records, key=...)` and justify the tie rule: the documentation says it is equivalent to sorted(records, key=key, reverse=True)[:k], and sorted with reverse=True keeps equal elements in their original order. The checker verifies the equivalence exhaustively on small lists with heavy ties. Also say when nlargest is the wrong tool (k close to n, where sorted is faster; k == 1, where max is) and what its cost is (O(n log k)). Example: records=[['ann', 90], ['bob', 85], ['cy', 90], ['di', 70]], k=3 -> ['ann', 'cy', 'bob']; records=[['a', 1], ['b', 1], ['c', 1]], k=2 -> ['a', 'b']; records=[['a', 5]], k=3 -> ['a']; records=[], k=2 -> [].
**Asked at:** The Python heapq documentation recipe on entry counters, removed-task markers and wrapper classes (search snippets of docs.python.org pages; WebFetch of docs.python.org failed with getaddrinfo ENOTFOUND, so the page was not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Top-k with a size-k heap, here through `heapq.nlargest` with a `key`. The interesting part is the tie rule.

**Say this first (1 line):** "`heapq.nlargest(k, records, key=score)` gives the k best in O(n log k), and the docs say it equals `sorted(records, key=score, reverse=True)[:k]`, so equal scores come out in their original order."

**Brute force:** `sorted(records, key=lambda r: r[1], reverse=True)[:k]`: O(n log n). The explicit version sorts by `(-score, position)`, which spells the tie rule out and is used as the checker in the code.

**Optimal:**
- `heapq.nlargest(k, records, key=lambda r: r[1])`, then take the names.
- Tie rule: `sorted(..., reverse=True)` keeps equal elements in their original order (it does not simply reverse the list; the code prints both). The docs state `nlargest` is equivalent to that sorted slice, so the earlier record wins a tie. Internally CPython decorates each item with its position to get this.
- The code checks the equivalence on every list of length 0 to 5 with scores in {0, 1, 2} and every k from 1 to n + 2: no failure.
- Hand-written alternative: a size-k min-heap of `(score, -position, name)`. The negated position makes the earlier record the larger tuple on ties, and the unique position means the name is never compared. Without the unique tie-breaker, equal scores fall through to comparing the next item, which for names is wrong order and for dicts or objects is a `TypeError` (the code shows it).
- When `nlargest` is the wrong tool:
  - k close to n: sorting once is faster; CPython itself falls back to `sorted` when k >= n.
  - k == 1: `max(records, key=...)` is simpler. `max` also returns the first maximal item, the same tie rule.
  - You need the full order anyway: sort.

**Complexity:** `nlargest`: time O(n log k), space O(k) for the heap. Sorting: O(n log n) time, O(n) space. For k = 1, `max` is O(n) time and O(1) space.

**Dry run:** `[['ann',90], ['bob',85], ['cy',90], ['di',70]]`, k = 3.
- Scores 90, 85, 90, 70. The three largest are the two 90s and 85.
- Ann and Cy tie at 90; Ann is earlier, so she comes first. Result `['ann', 'cy', 'bob']`.

**Code:**
```python
import heapq
import itertools
import random

random.seed(37)

def top_names(records, k):
    return [name for name, score in heapq.nlargest(k, records, key=lambda r: r[1])]

def top_names_brute(records, k):
    """Explicit rule: higher score first, earlier position first on ties."""
    order = sorted(range(len(records)), key=lambda i: (-records[i][1], i))
    return [records[i][0] for i in order[:k]]

# ---- examples
for rec, k, want in [([['ann', 90], ['bob', 85], ['cy', 90], ['di', 70]], 3, ['ann', 'cy', 'bob']),
                     ([['a', 1], ['b', 1], ['c', 1]], 2, ['a', 'b']),
                     ([['a', 5]], 3, ['a']),
                     ([], 2, [])]:
    assert top_names(rec, k) == top_names_brute(rec, k) == want, (rec, k)
    print(rec, k, '->', top_names(rec, k))

# ---- exhaustive equivalence with sorted(..., reverse=True)[:k] on small lists with heavy ties
cases = 0
for n in range(0, 6):
    for scores in itertools.product(range(3), repeat=n):
        rec = [[chr(97 + i), s] for i, s in enumerate(scores)]
        for k in range(1, n + 3):
            a = heapq.nlargest(k, rec, key=lambda r: r[1])
            b = sorted(rec, key=lambda r: r[1], reverse=True)[:k]
            assert a == b
            assert top_names(rec, k) == top_names_brute(rec, k)
            cases += 1
print('nlargest == sorted(reverse=True)[:k] on', cases, 'tie-heavy (list, k) cases')

# ---- where the tie rule comes from: reverse=True does NOT reverse equal elements
print(sorted([['a', 1], ['b', 1], ['c', 1]], key=lambda r: r[1], reverse=True))
print('reversed(sorted(...)) would give', list(reversed(sorted([['a', 1], ['b', 1], ['c', 1]], key=lambda r: r[1]))))

# ---- the same job with a hand-written heap needs explicit tie info, or ties compare names (or crash)
def top_names_manual(records, k):
    h = []                                    # min-heap of (score, -position, name): smallest = worst kept
    for i, (name, score) in enumerate(records):
        item = (score, -i, name)              # -i: earlier position counts as larger on a tie
        if len(h) < k:
            heapq.heappush(h, item)
        elif item > h[0]:
            heapq.heapreplace(h, item)
    return [name for score, negpos, name in sorted(h, reverse=True)]
for _ in range(500):
    rec = [[str(i), random.randint(0, 3)] for i in range(random.randint(0, 9))]
    k = random.randint(1, 6)
    assert top_names_manual(rec, k) == top_names(rec, k) == top_names_brute(rec, k)
print('manual size-k heap with (score, -position, name) agrees on 500 random lists')
try:
    h = [(1, {'x': 1})]; heapq.heappush(h, (1, {'x': 2}))
except TypeError as e:
    print('payload without a tie-breaker -> TypeError:', e)

# ---- edge asserts
assert top_names([['a', 5]], 3) == ['a']
assert top_names([], 2) == []
assert top_names([['a', -1], ['b', -1]], 1) == ['a']
assert top_names([['a', 1], ['b', 2]], 1) == ['b'] == [max([['a', 1], ['b', 2]], key=lambda r: r[1])[0]]
big = [[str(i), random.randint(0, 50)] for i in range(10 ** 4)]
assert top_names(big, 10 ** 4) == [r[0] for r in sorted(big, key=lambda r: r[1], reverse=True)]
assert top_names(big, 5) == top_names_brute(big, 5)
print('size 10^4 checks ok; k == n result equals a stable descending sort')
```

**Output (my run):**
```
[['ann', 90], ['bob', 85], ['cy', 90], ['di', 70]] 3 -> ['ann', 'cy', 'bob']
[['a', 1], ['b', 1], ['c', 1]] 2 -> ['a', 'b']
[['a', 5]] 3 -> ['a']
[] 2 -> []
nlargest == sorted(reverse=True)[:k] on 2369 tie-heavy (list, k) cases
[['a', 1], ['b', 1], ['c', 1]]
reversed(sorted(...)) would give [['c', 1], ['b', 1], ['a', 1]]
manual size-k heap with (score, -position, name) agrees on 500 random lists
payload without a tie-breaker -> TypeError: '<' not supported between instances of 'dict' and 'dict'
size 10^4 checks ok; k == n result equals a stable descending sort
```

**Edge cases:**
- Empty `records`: `[]`.
- `k` larger than the number of records: all names, in sorted order.
- All scores equal: the first k names in input order.
- Negative scores work unchanged.
- Distinct names are promised, so names are only for output, never for ordering.

**Follow-ups:**
- *Lowest scores, earliest first on ties?* `heapq.nsmallest(k, records, key=...)` is the matching call and is equivalent to `sorted(records, key=key)[:k]`, also stable.
- *Tie rule: later position first?* Sort by `(-score, -position)`, or use `reversed` on a stable ascending sort; do not rely on `reverse=True`.
- *Data too big for memory?* Stream through a size-k min-heap (the manual version), O(k) space.

**Common mistakes:**
- Assuming `reverse=True` reverses ties. It does not; stability is kept.
- Using `heapq.nlargest(k, records)` without `key` and getting an ordering by name on ties.
- Hand-rolled heap with `(score, name)` tuples: the tie order comes from the names, not from position.
- Using `nlargest` when k is about n, or for k = 1.

### Q38 ⭐ 🟡 A priority queue with changing priorities and no decrease-key. `heapq` cannot lower an entry's priority in place; the standard fix is to push a new entry and ignore the stale one later (lazy invalidation; the indexed-heap variant used for Dijkstra belongs to Part 9). `ops` is a list of ['add', task, priority], ['update', task, priority] (same effect as add: it sets the task's current priority, creating the task if absent), ['remove', task], ['pop'] and ['size']; the priority is an integer, smaller is served first, and tasks with equal priority are served in order of the last time their priority was set (an update re-queues the task behind existing equals). Return the outputs of every non-add, non-update operation in order: remove gives True if the task was present else False, pop gives the served task name (and removes it) or None if empty, size gives the number of live tasks. 0 <= len(ops) <= 10^5. Show the entry (priority, stamp, task) with a current-version dict, and why the heap can hold at most one entry per add or update call. Example: ops=[['add', 'a', 5], ['add', 'b', 3], ['update', 'a', 1], ['pop'], ['size'], ['add', 'c', 3], ['update', 'b', 3], ['pop'], ['remove', 'z'], ['pop'], ['pop']] -> ['a', 1, 'c', False, 'b', null]; ops=[['pop'], ['add', 'x', 1], ['remove', 'x'], ['pop'], ['size']] -> [null, True, null, 0].
**Asked at:** The Python heapq documentation recipe on entry counters, removed-task markers and wrapper classes (search snippets of docs.python.org pages; WebFetch of docs.python.org failed with getaddrinfo ENOTFOUND, so the page was not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Lazy invalidation. The heap invariant forbids changing an entry in place, so push a new version and ignore the stale ones when they reach the top.

**Say this first (1 line):** "`heapq` has no decrease-key, so every add or update pushes `(priority, stamp, task)` and records the live version in a dict; a pop discards entries that no longer match the dict."

**Brute force:** Keep a dict `task -> (priority, stamp)` and on each pop take `min` over the dict: O(n) per pop, O(n^2) worst for 10^5 operations. It is the cross-check.

**Optimal:**
- State: `heap` of `(priority, stamp, task)`, `current` dict `task -> (priority, stamp)`, a global counter `stamp`.
- `add` and `update` are the same: `stamp += 1`, `current[task] = (priority, stamp)`, push `(priority, stamp, task)`. The old entry, if any, is now stale because its stamp no longer matches.
- `remove`: `current.pop(task, None)`; answer True if it existed. The heap entry stays and becomes stale. No heap work at all.
- `pop`: loop `heappop`; an entry is live only if `current.get(task) == (priority, stamp)`. Stale entries are dropped. If the heap empties, answer `None`. On a hit, delete the task from `current`.
- `size`: `len(current)`, not `len(heap)`: the heap contains stale entries.
- Why the stamp does two jobs:
  - Tie rule: equal priorities pop in order of the last time the priority was set, because the stamp increases with each call and is compared second.
  - Safety: stamps are unique, so the tuple comparison never reaches `task`. Without a stamp, two tied entries compare the task objects, which raises `TypeError` for unorderable ones (the code shows it with a plain class). With strings it would silently order by name, which breaks the stated tie rule.
- Bound: every add or update pushes exactly one entry and nothing else pushes, so the heap holds at most one entry per add or update call. Each entry is popped at most once, so total work is O(n log n).
- Caveat: the heap does not shrink on `remove` or `update`. The code shows 1000 updates of one task leaving 1000 physical entries and 1 live task. If memory matters, rebuild the heap from `current` when `len(heap) > 2 * len(current)`; this keeps the amortised cost the same.

**Complexity:** Time O(log n) per add/update (one push), O(1) per remove and size, O(log n) amortised per pop (each stale entry is discarded once). Space O(number of add/update calls) until a compaction.

**Dry run:** First example.
- add a5, add b3, update a1: heap `(1,3,a) (3,2,b) (5,1,a)`; `current = {a: (1,3), b: (3,2)}`.
- pop: `(1,3,a)` matches, answer `a`. size: 1 (only b).
- add c3 (stamp 4), update b3 (stamp 5): b is re-queued behind c at the same priority.
- pop: `(3,2,b)` is stale (b is now `(3,5)`), dropped; `(3,4,c)` matches: answer `c`.
- remove z: False. pop: `(3,5,b)` matches: `b`. pop: `(5,1,a)` is stale and the heap empties: `None`.
- Output `['a', 1, 'c', False, 'b', None]`.

**Code:**
```python
import heapq
import random

random.seed(38)

def run_lazy(ops, check=False):
    heap = []          # entries (priority, stamp, task); stale ones are skipped when popped
    current = {}       # task -> (priority, stamp) of its live version
    stamp = pushes = 0
    out = []
    for op in ops:
        kind = op[0]
        if kind in ('add', 'update'):
            stamp += 1                                    # strictly increasing: unique, so the task is never compared
            current[op[1]] = (op[2], stamp)
            heapq.heappush(heap, (op[2], stamp, op[1]))
            pushes += 1
        elif kind == 'remove':
            out.append(current.pop(op[1], None) is not None)
        elif kind == 'pop':
            res = None
            while heap:
                pr, st, task = heapq.heappop(heap)
                if current.get(task) == (pr, st):         # still the live version?
                    del current[task]
                    res = task
                    break                                 # otherwise stale: drop and keep looking
            out.append(res)
        else:                                             # 'size'
            out.append(len(current))                      # live tasks, NOT len(heap)
        if check:
            assert len(heap) <= pushes
    return out

def run_brute(ops):
    cur, stamp, out = {}, 0, []
    for op in ops:
        if op[0] in ('add', 'update'):
            stamp += 1; cur[op[1]] = (op[2], stamp)
        elif op[0] == 'remove':
            out.append(cur.pop(op[1], None) is not None)
        elif op[0] == 'pop':
            if cur:
                t = min(cur, key=lambda x: cur[x]); del cur[t]; out.append(t)
            else:
                out.append(None)
        else:
            out.append(len(cur))
    return out

# ---- examples
ex = [
    ([['add', 'a', 5], ['add', 'b', 3], ['update', 'a', 1], ['pop'], ['size'], ['add', 'c', 3], ['update', 'b', 3],
      ['pop'], ['remove', 'z'], ['pop'], ['pop']], ['a', 1, 'c', False, 'b', None]),
    ([['pop'], ['add', 'x', 1], ['remove', 'x'], ['pop'], ['size']], [None, True, None, 0]),
]
for ops, want in ex:
    assert run_lazy(ops, check=True) == run_brute(ops) == want
    print(run_lazy(ops))

# ---- why the stamp: ties on priority must never compare the task objects
class Task:                      # unorderable payload
    def __init__(self, n): self.n = n
h = []
heapq.heappush(h, (1, Task('p')))
try:
    heapq.heappush(h, (1, Task('q')))
except TypeError as e:
    print('without a stamp, tied priority ->', e)
h = []
for i, name in enumerate('pqr'):
    heapq.heappush(h, (1, i, Task(name)))                  # (priority, stamp, task): ties resolved by stamp
print('with a stamp, equal priorities pop in insertion order:', [heapq.heappop(h)[2].n for _ in range(3)])

# ---- the heap never holds more entries than add/update calls; a hot update loop grows it though
heap_demo, cur, st = [], {}, 0
for i in range(1000):
    st += 1; cur['t'] = (i, st); heapq.heappush(heap_demo, (i, st, 't'))
print('1000 updates of ONE task: live size =', len(cur), ', physical heap entries =', len(heap_demo))

# ---- random cross-check
def rand_ops():
    ops = []
    for _ in range(random.randint(0, 25)):
        r = random.random(); t = random.choice('abcd')
        if r < 0.3: ops.append(['add', t, random.randint(0, 3)])
        elif r < 0.5: ops.append(['update', t, random.randint(0, 3)])
        elif r < 0.65: ops.append(['remove', t])
        elif r < 0.9: ops.append(['pop'])
        else: ops.append(['size'])
    return ops
for _ in range(3000):
    ops = rand_ops()
    assert run_lazy(ops, check=True) == run_brute(ops), ops
print('3000 random op sequences agree with the O(n)-per-pop brute force')

# ---- edge asserts
assert run_lazy([]) == []
assert run_lazy([['pop']]) == [None]
assert run_lazy([['add', 'a', 1], ['remove', 'a'], ['add', 'a', 1], ['pop']]) == [True, 'a']      # re-add after remove
assert run_lazy([['add', 'a', 1], ['add', 'b', 1], ['update', 'a', 1], ['pop'], ['pop']]) == ['b', 'a']  # update re-queues behind
assert run_lazy([['add', 'a', 1], ['remove', 'a'], ['remove', 'a']]) == [True, False]
n = 10 ** 5
ops = [['add', str(i % 500), random.randint(0, 1000)] for i in range(n // 2)] + [['pop']] * (n // 2)
res = run_lazy(ops, check=True)
assert len(res) == n // 2 and res.count(None) == n // 2 - 500
print('10^5 ops ok; pops answered:', n // 2, 'of which None:', res.count(None))
```

**Output (my run):**
```
['a', 1, 'c', False, 'b', None]
[None, True, None, 0]
without a stamp, tied priority -> '<' not supported between instances of 'Task' and 'Task'
with a stamp, equal priorities pop in insertion order: ['p', 'q', 'r']
1000 updates of ONE task: live size = 1 , physical heap entries = 1000
3000 random op sequences agree with the O(n)-per-pop brute force
10^5 ops ok; pops answered: 50000 of which None: 49500
```

**Edge cases:**
- Pop on an empty queue: `None`, and the `while` loop must end when the heap is empty, not only on a hit.
- Remove a task that was never added or was already removed: False.
- Re-add after remove: the old entry is stale (different stamp) even if the priority is the same.
- Update to the same priority: still a new stamp, so the task goes behind its equals.
- `size` after many updates: still the live count.

**Follow-ups:**
- *Why not remove from the middle of the list?* `list.remove` is O(n) and breaks the heap invariant; you would have to `heapify` again.
- *Indexed heap with a real decrease-key?* It keeps a position map and sifts in place, O(log n) with no stale entries. That is the Dijkstra variant and belongs to Part 9.
- *Memory growth?* Compact by rebuilding from `current` when stale entries outnumber live ones.

**Common mistakes:**
- `len(heap)` for size.
- Checking only `task in current` on pop: a stale older entry of a still-live task would be served at the wrong priority. Compare the stamp or priority too.
- No stamp: `TypeError` on ties of unorderable tasks, or wrong tie order for strings.
- Reusing a counter that is reset or not strictly increasing.

### Q39 ⭐ 🟡 The greedy feasibility check inside a binary search on the answer. Part 5 Q8 (capacity to ship packages) binary-searches the capacity and uses a check in the inner loop; here you write and justify only that check. `weights` (1 <= len <= 5*10^4, 1 <= weights[i] <= 500) must be shipped in the given order, each day carrying a contiguous block whose total is at most `cap`. Return the minimum number of days needed for the capacity `cap`, or -1 if some weight exceeds cap. The greedy is: keep loading the current day until the next package would exceed cap, then start a new day. Prove it by exchange (any schedule can be shifted so each day takes as much as possible without using more days; the checker compares the greedy against an exhaustive DP over all contiguous splits), and tie it to Part 5 Q33: the day count is non-increasing in cap, which is exactly the monotone predicate that makes the outer binary search legal. Example: weights=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], cap=15 -> 5; weights=[3, 2, 2, 4, 1, 4], cap=6 -> 3; weights=[5, 5], cap=4 -> -1; weights=[7], cap=7 -> 1.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy feasibility check, the inner loop of binary search on the answer. Here only the check is the question.

**Say this first (1 line):** "Load each day until the next package would overflow, then open a new day. Taking as much as possible each day never costs a day, so this count is the minimum for that capacity, and it only falls as the capacity grows."

**Brute force:** DP over all contiguous splits: `d[i] = min(d[j] + 1)` over every `j < i` whose block `weights[j:i]` sums to at most `cap`. That is O(n^2) states and transitions (O(n^3) with naive block sums in the code), too slow for n = 5 * 10^4. It is the checker.

**Optimal:**
- If `max(weights) > cap`, return -1: that package cannot be carried on any day.
- Otherwise scan once with `days = 1`, `load = 0`. For each weight `w`: if `load + w > cap`, `days += 1; load = 0`. Then `load += w`.
- Exchange argument:
  - Take any optimal schedule. Look at its first day. If it ends before the greedy's first day ends, move the first package of day 2 into day 1: it fits (greedy says so), and day 2 only gets lighter, so still valid and not worse.
  - Repeat. Day 1 now equals the greedy's day 1. The rest is the same problem on the remaining packages, so induction finishes it.
  - The point: ending a day earlier than necessary can only push work to later days, never remove a day.
- Monotone in `cap`: a schedule valid for capacity `c` is valid for `c + 1`, so the minimum number of days cannot go up. That is exactly the "monotone predicate" of Part 5 Q33: `days(cap) <= D` is false, false, ..., true, true. So the outer binary search over `cap` in `[max(weights), sum(weights)]` is legal. The code runs that search and compares it with exhaustive search.

**Complexity:** One check: time O(n), space O(1). The whole search would add a factor of log(sum - max): about log2(2.5 * 10^7) = 25 checks here. The DP is O(n^2) states and transitions.

**Dry run:** `weights=[3, 2, 2, 4, 1, 4]`, cap = 6.
- Day 1: 3, then 2 (5), then 2 would make 7 > 6: close. Day 1 = `[3, 2]`.
- Day 2: 2, then 4 (6), then 1 would make 7: close. Day 2 = `[2, 4]`.
- Day 3: 1, then 4 (5). End. 3 days.

**Code:**
```python
import random

random.seed(39)

def days_greedy(weights, cap):
    if max(weights) > cap:
        return -1
    days, load = 1, 0
    for w in weights:
        if load + w > cap:       # next package would overflow today: close the day, start a new one
            days += 1
            load = 0
        load += w
    return days

def days_dp(weights, cap):
    """Exhaustive: d[i] = fewest days for the first i packages over ALL contiguous splits."""
    if max(weights) > cap:
        return -1
    n, INF = len(weights), float('inf')
    d = [0] + [INF] * n
    for i in range(1, n + 1):
        for j in range(i):
            if sum(weights[j:i]) <= cap:
                d[i] = min(d[i], d[j] + 1)
    return d[n]

def min_cap(weights, limit_days):
    """The outer binary search (Part 5 Q8 style) that uses days_greedy as its predicate."""
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_greedy(weights, mid) <= limit_days:
            hi = mid
        else:
            lo = mid + 1
    return lo

# ---- examples
for w, cap, want in [([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 15, 5), ([3, 2, 2, 4, 1, 4], 6, 3), ([5, 5], 4, -1), ([7], 7, 1)]:
    assert days_greedy(w, cap) == days_dp(w, cap) == want, (w, cap)
    print(w, 'cap', cap, '->', days_greedy(w, cap))

# ---- greedy vs exhaustive DP, then monotonic in capacity, on seeded small inputs
for _ in range(1500):
    w = [random.randint(1, 6) for _ in range(random.randint(1, 8))]
    cap = random.randint(1, 14)
    assert days_greedy(w, cap) == days_dp(w, cap), (w, cap)
print('1500 random (weights, cap) agree with the exhaustive DP')

mono = 0
for _ in range(500):
    w = [random.randint(1, 9) for _ in range(random.randint(1, 9))]
    ds = [days_greedy(w, c) for c in range(max(w), sum(w) + 3)]       # all capacities that are feasible
    assert all(ds[i] >= ds[i + 1] for i in range(len(ds) - 1)), (w, ds)
    assert ds[0] >= 1 and ds[-1] == 1
    mono += 1
print('days(cap) is non-increasing on', mono, 'weight lists (so "days <= D" is a monotone predicate for binary search)')

# ---- the check inside the binary search: smallest cap for D days, against brute force over every cap
for _ in range(500):
    w = [random.randint(1, 8) for _ in range(random.randint(1, 8))]
    D = random.randint(1, len(w))
    brute = next(c for c in range(max(w), sum(w) + 1) if days_dp(w, c) <= D)
    assert min_cap(w, D) == brute, (w, D)
print('binary search over cap with the greedy check matches exhaustive search on 500 cases;',
      'sample: weights 1..10, 5 days ->', min_cap(list(range(1, 11)), 5))

# ---- edge asserts and maximum size
assert days_greedy([1], 1) == 1
assert days_greedy([5, 5], 5) == 2 and days_greedy([5, 5], 10) == 1 and days_greedy([5, 5], 9) == 2
assert days_greedy([500] * 3, 499) == -1
big = [random.randint(1, 500) for _ in range(5 * 10 ** 4)]
assert days_greedy(big, 500) >= 1 and days_greedy(big, sum(big)) == 1
print('size 5*10^4 ok; days at cap 500 =', days_greedy(big, 500), ', at sum(big) =', days_greedy(big, sum(big)))
```

**Output (my run):**
```
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] cap 15 -> 5
[3, 2, 2, 4, 1, 4] cap 6 -> 3
[5, 5] cap 4 -> -1
[7] cap 7 -> 1
1500 random (weights, cap) agree with the exhaustive DP
days(cap) is non-increasing on 500 weight lists (so "days <= D" is a monotone predicate for binary search)
binary search over cap with the greedy check matches exhaustive search on 500 cases; sample: weights 1..10, 5 days -> 15
size 5*10^4 ok; days at cap 500 = 33273 , at sum(big) = 1
```

**Edge cases:**
- One package, `cap == weight`: 1 day.
- `cap` below the heaviest package: -1, checked first.
- `cap >= sum(weights)`: 1 day.
- `cap == max(weights)`: valid, at most n days.
- A package exactly fills the cap: `load + w > cap` is strict, so an exact fit stays on the day.
- All weights equal: `cap // w` packages per day.

**Follow-ups:**
- *Why must the order be kept?* If packages could be reordered, this becomes bin packing, which is NP-hard; the greedy would no longer be optimal. Order is what makes contiguous splitting and the exchange argument work.
- *Why start the search at `max(weights)`?* Below it the check returns -1 and the predicate is undefined.
- *Is the greedy a DP in disguise?* It is the DP with the observation that only the farthest `j` matters, because `d` is non-decreasing in `i`.

**Common mistakes:**
- `load + w >= cap` for the new-day test: wastes capacity on exact fits.
- Forgetting to reset `load` to 0 and then adding `w` (resetting to `w` and adding again, or dropping `w`).
- Starting `days` at 0 and never counting the last day.
- Forgetting the `-1` guard, then looping forever or overcounting.

### Q40 ⭐ 🟡 Huffman coding at concept level. `freqs` is a list of positive integers (1 <= len <= 10^5), the frequency of each symbol. Return a list `lengths` with the code length of every symbol, in the same order, for an optimal prefix code. Build it by repeatedly merging the two smallest frequencies with a min-heap (each merge adds one bit to every symbol under the two nodes; for a single symbol return [0]). The codes themselves and even the length lists are NOT unique when frequencies tie; what is unique is the total cost sum(freqs[i] * lengths[i]). The checker accepts any list whose Kraft sum is exactly 1 (so a full prefix tree with those depths exists) and whose cost equals the true optimum found by an exhaustive search over all full binary trees. Say what the exchange argument is (the two rarest symbols can be assumed to be deepest siblings) and tie it to the sticks question above. Example: freqs=[5, 9, 12, 13, 16, 45] -> [4, 4, 3, 3, 3, 1]; freqs=[1, 1, 1, 1] -> [2, 2, 2, 2]; freqs=[7] -> [0]; freqs=[1, 2] -> [1, 1]; freqs=[3, 3, 3, 3, 3] -> [3, 3, 2, 2, 2].
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy with a min-heap: always merge the two cheapest items. It is the same loop as Part 8 Q20 (connecting sticks), with the tree kept so each symbol gets a depth.

**Say this first (1 line):** "Repeatedly merge the two rarest symbols; each merge pushes everything below them one bit deeper. The result is an optimal prefix code; code lengths can tie, but the total cost cannot."

**Brute force:** Try every full binary tree over the symbols and take the cheapest weighted depth. With subsets: `best(S) = min over splits (A, S minus A) of best(A) + best(S minus A) + weight(S)`. That is about 3^n work, so only n <= 7 here. It is the checker in the code.

**Optimal:**
- Heap of `(frequency, node id)`. Leaves are ids `0..n-1`; each merge creates id `n, n+1, ...`.
- Pop two smallest `(f1, a)`, `(f2, b)`; set `parent[a] = parent[b] = new id`; push `(f1 + f2, new id)`. Repeat until one node is left.
- Depth of a leaf is the number of merges above it. A parent always has a larger id than its children, so one backward loop over ids computes every depth with no recursion. A skewed tree (Fibonacci-like frequencies) reaches depth n - 1, which would break a recursive walk at n = 10^5.
- One symbol: no merge, code length 0 (return `[0]`).
- Exchange argument, in words:
  - In some optimal tree the two rarest symbols are siblings at the deepest level. If a rarer symbol sat higher than a more frequent one, swapping them lowers (or keeps) the cost, because the cost is the sum of `frequency * depth`.
  - So merge them into one super-symbol whose weight is their sum. An optimal code for the smaller problem, with the super-symbol expanded back into two leaves, is optimal for the original (the cost differs by exactly `f1 + f2`, the merged weight).
  - Induction on the number of symbols finishes.
- Why the cost is unique but the lengths are not: with ties the heap may pick either of two equal-weight nodes. Both choices cost the same, but the length lists differ. The code shows `[3,3,2,2,2]`, `[2,2,2,3,3]` both valid for five equal frequencies, and `[2,2,2,2,2]` rejected because its Kraft sum is 5/4 (no prefix code has those lengths).
- Heap ties: `(frequency, node)` tuples would compare the nodes on equal frequency and raise `TypeError` for an unorderable class (shown). The unique node id as the second item stops the comparison there, and also makes the run deterministic.
- Link to Q20: the total merge cost in "connect sticks" equals `sum(freq * length)` here, since each merge adds the merged weight and each symbol's weight is counted once per level it sits below. The code asserts it on 500 random lists.

**Complexity:** Time O(n log n): n - 1 merges, each two pops and a push at O(log n). Space O(n) for the heap, parent and depth arrays (2n - 1 nodes).

**Dry run:** `[5, 9, 12, 13, 16, 45]`.
- Merge 5 + 9 = 14. Heap: 12, 13, 14, 16, 45.
- Merge 12 + 13 = 25. Heap: 14, 16, 25, 45.
- Merge 14 + 16 = 30. Heap: 25, 30, 45.
- Merge 25 + 30 = 55. Heap: 45, 55.
- Merge 45 + 55 = 100. Done.
- Depths: 45 is 1; 12, 13, 16 are 3; 5, 9 are 4 (under 14, under 30, under 55, under 100). Lengths `[4, 4, 3, 3, 3, 1]`, cost 224 (the code prints it).

**Code:**
```python
import heapq
import random
from fractions import Fraction
from functools import lru_cache

random.seed(40)

def huffman_lengths(freqs):
    """Merge the two smallest repeatedly. Nodes 0..n-1 are leaves, n.. are merged nodes. parent[] gives depths with no recursion."""
    n = len(freqs)
    if n == 1:
        return [0]
    parent = [-1] * (2 * n - 1)
    heap = [(f, i) for i, f in enumerate(freqs)]      # (frequency, node id): ids are unique, so ties never reach anything else
    heapq.heapify(heap)
    nxt = n
    while len(heap) > 1:
        f1, a = heapq.heappop(heap)
        f2, b = heapq.heappop(heap)
        parent[a] = parent[b] = nxt
        heapq.heappush(heap, (f1 + f2, nxt))
        nxt += 1
    depth = [0] * (2 * n - 1)                          # root is nxt - 1; parents always have bigger ids than children
    for v in range(2 * n - 3, -1, -1):
        depth[v] = depth[parent[v]] + 1
    return depth[:n]

def cost_of(freqs, lengths):
    return sum(f * l for f, l in zip(freqs, lengths))

def optimal_cost_brute(freqs):
    """Exhaustive over all full binary trees on the symbols: best split of every subset into two non-empty parts."""
    n = len(freqs)
    tot = [0] * (1 << n)
    for m in range(1, 1 << n):
        tot[m] = sum(freqs[i] for i in range(n) if m >> i & 1)
    @lru_cache(None)
    def best(m):
        if m & (m - 1) == 0:
            return 0                                   # one symbol: no more bits
        res, sub = float('inf'), (m - 1) & m
        while sub:
            res = min(res, best(sub) + best(m ^ sub) + tot[m])   # every bit of the merge adds the subtree weight once
            sub = (sub - 1) & m
        return res
    return best((1 << n) - 1)

def valid_code(freqs, lengths):
    """Accepted if the lengths form a full prefix tree (Kraft sum exactly 1; a single symbol uses [0]) with the optimal cost."""
    if len(lengths) != len(freqs):
        return False
    if len(freqs) == 1:
        return lengths == [0]
    return sum(Fraction(1, 2 ** l) for l in lengths) == 1 and cost_of(freqs, lengths) == optimal_cost_brute(freqs)

# ---- examples
for fr, want in [([5, 9, 12, 13, 16, 45], [4, 4, 3, 3, 3, 1]), ([1, 1, 1, 1], [2, 2, 2, 2]), ([7], [0]),
                 ([1, 2], [1, 1]), ([3, 3, 3, 3, 3], [3, 3, 2, 2, 2])]:
    got = huffman_lengths(fr)
    assert valid_code(fr, got) and valid_code(fr, want), (fr, got, want)
    print(fr, '->', got, 'cost', cost_of(fr, got), '| prompt answer cost', cost_of(fr, want))

# ---- the lengths are not unique, only the cost is: any permutation of the lengths among tied symbols is also optimal
fr = [3, 3, 3, 3, 3]
print('tied frequencies', fr, ': [3,3,2,2,2] valid:', valid_code(fr, [3, 3, 2, 2, 2]), '| [2,2,2,3,3] valid:', valid_code(fr, [2, 2, 2, 3, 3]),
      '| [2,2,2,2,2] valid:', valid_code(fr, [2, 2, 2, 2, 2]), '(Kraft sum 5/4, not a prefix code)')

# ---- the tie-breaker matters for the heap, not for the optimal cost
class Node:
    def __init__(self, f): self.f = f
h = []
heapq.heappush(h, (2, Node(2)))
try:
    heapq.heappush(h, (2, Node(2)))
except TypeError as e:
    print('heap of (freq, Node) with tied freq ->', e)
print('so each node carries a unique id as the second tuple item')

# ---- random cross-check against the exhaustive optimum (n <= 7), including all-equal and tiny frequencies
for _ in range(600):
    fr = [random.randint(1, 9) for _ in range(random.randint(1, 7))]
    assert valid_code(fr, huffman_lengths(fr)), fr
print('600 random frequency lists: Kraft sum == 1 and cost == exhaustive optimum')

# ---- same number as "minimum cost to connect sticks" (Part 8 Q20): the merge costs add up to the weighted path length
def sticks_cost(sticks):
    h = list(sticks); heapq.heapify(h); tot = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h); tot += a + b; heapq.heappush(h, a + b)
    return tot
for _ in range(500):
    fr = [random.randint(1, 20) for _ in range(random.randint(1, 12))]
    assert sticks_cost(fr) == cost_of(fr, huffman_lengths(fr)), fr
print('Huffman weighted length == sticks merge cost on 500 random lists')

# ---- edge and size
assert huffman_lengths([7]) == [0]
assert huffman_lengths([1, 2]) == [1, 1]
fib = [1, 1]
for _ in range(30): fib.append(fib[-1] + fib[-2])
fl = huffman_lengths(fib)
assert max(fl) == len(fib) - 1 and sum(Fraction(1, 2 ** l) for l in fl) == 1       # skewed: depth n-1, still no recursion
n = 10 ** 5
big = [random.randint(1, 10 ** 6) for _ in range(n)]
bl = huffman_lengths(big)
assert len(bl) == n and sum(Fraction(1, 2 ** l) for l in bl) == 1
print('n=10^5: max code length', max(bl), '; Fibonacci frequencies give depth', max(fl), '= n - 1 for n =', len(fib))
```

**Output (my run):**
```
[5, 9, 12, 13, 16, 45] -> [4, 4, 3, 3, 3, 1] cost 224 | prompt answer cost 224
[1, 1, 1, 1] -> [2, 2, 2, 2] cost 8 | prompt answer cost 8
[7] -> [0] cost 0 | prompt answer cost 0
[1, 2] -> [1, 1] cost 3 | prompt answer cost 3
[3, 3, 3, 3, 3] -> [3, 3, 2, 2, 2] cost 36 | prompt answer cost 36
tied frequencies [3, 3, 3, 3, 3] : [3,3,2,2,2] valid: True | [2,2,2,3,3] valid: True | [2,2,2,2,2] valid: False (Kraft sum 5/4, not a prefix code)
heap of (freq, Node) with tied freq -> '<' not supported between instances of 'Node' and 'Node'
so each node carries a unique id as the second tuple item
600 random frequency lists: Kraft sum == 1 and cost == exhaustive optimum
Huffman weighted length == sticks merge cost on 500 random lists
n=10^5: max code length 32 ; Fibonacci frequencies give depth 31 = n - 1 for n = 32
```

**Edge cases:**
- One symbol: `[0]`.
- Two symbols: `[1, 1]`.
- All frequencies equal and n a power of two: all lengths `log2(n)`.
- Skewed (Fibonacci) frequencies: depth n - 1.
- Ties: valid answers differ; compare cost and Kraft sum, never the list.
- n = 10^5: the loop is iterative, no recursion.

**Follow-ups:**
- *How to produce the actual bit strings?* Keep left and right child per merged node and walk from the root with an explicit stack, appending 0 or 1. Or assign canonical codes from the lengths: sort by (length, symbol) and count upward.
- *Why not sort once and merge two at a time with a queue?* If the frequencies are already sorted, two queues (leaves and merged nodes) give O(n) because merged weights come out non-decreasing.
- *Is Huffman optimal for any code?* Only for prefix codes that give each symbol an integer number of bits.

**Common mistakes:**
- Pushing `(freq, node)` and hitting `TypeError` on ties.
- Returning length 1 for a single symbol (the prompt wants 0).
- Merging the two largest, or merging in input order.
- Comparing length lists for equality in tests instead of cost and Kraft sum.
- Recursing over a skewed tree.

### Q41 ⭐ 🔴 Sliding window median. Given integers `nums` (1 <= len <= 10^5, |value| <= 10^9) and a window size 1 <= k <= len, return the median of every window of k consecutive elements as floats (the middle value for odd k, the mean of the two middle values for even k). Use two heaps with lazy deletion (the element that leaves the window is only marked, tracked by its index, and discarded when it reaches a heap top) and keep the live sizes of both heaps balanced separately from the heaps' physical lengths. State the cost (O(n log n) worst case, because stale entries buried below the heap tops can let the heaps grow to O(n) entries; O(n log k) in the usual case or with periodic compaction; O(n) space for the stale entries) and compare with the sliding window maximum in Part 2 Q16, where a monotonic deque is enough because only one extreme is needed. Example: nums=[1, 3, -1, -3, 5, 3, 6, 7], k=3 -> [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]; nums=[1, 2, 3, 4, 2, 3, 1, 4, 2], k=3 -> [2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]; nums=[1, 4, 2, 3], k=4 -> [2.5]; nums=[5, 5, 5], k=2 -> [5.0, 5.0].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two heaps (max-heap for the lower half, min-heap for the upper half) plus lazy deletion for the element that leaves the window.

**Say this first (1 line):** "Keep the smaller half in a max-heap and the larger half in a min-heap, balanced to differ by at most one live element. A heap cannot delete from the middle, so the leaving element is only marked dead and thrown away when it reaches a top."

**Brute force:** Sort each window: O(k log k) per window, O(n k log k) total. At n = 10^5 and k = 5 * 10^4 that is far too slow. It is the cross-check.

**Optimal:**
- `lo`: max-heap by storing `(-value, index)`. `hi`: min-heap of `(value, index)`. The index makes ties orderable (equal values pop by index) and names the exact element to delete.
- `side[index]` says which heap holds a live element; `dead` is the set of indices that left the window.
- Live sizes `lsz`, `hsz` are tracked separately, because `len(heap)` counts dead entries too. Balance rule: `lsz == (lsz + hsz + 1) // 2`, so `lo` has the extra element when the window size is odd.
- Per step:
  - Insert: if `x <= top of lo` push to `lo`, else push to `hi`. Update live sizes.
  - Leave (after the first k elements): mark `i - k` dead and decrement the live size of its side.
  - Rebalance: while one side has too many live elements, prune dead tops, move the top across (negating when changing heaps), and update `side` and sizes.
  - Prune both tops so `lo[0]` and `hi[0]` are live.
  - Median: `-lo[0][0]` for odd k, `(-lo[0][0] + hi[0][0]) / 2` for even k.
- Why lazy deletion is safe: a dead entry only matters when it is at a top, and `prune` removes it before any read or pop. Dead entries buried below do not affect the heap order or the median.
- Compare with Part 2 Q16 (sliding window maximum): a monotonic deque works there because only one extreme matters, so smaller elements behind a larger one can never become the maximum. A median needs the middle rank, so every element in the window can matter and you need a structure that tracks order statistics, here two heaps.

**Complexity:** Each element is pushed once, popped at most once (either rebalanced or pruned), and moved between heaps O(1) times per step, so there are O(n) heap operations. Each costs O(log m) where m is the physical heap size. Live elements are only k, but stale entries sitting below the top are not removed until they surface, so m can reach O(n) in the worst case. Honest bound: O(n log n) time; it is O(n log k) in the usual case where stale entries surface quickly (and strictly so if you rebuild the heaps whenever stale entries outnumber live ones). Space: O(n) worst case for stale entries plus `side` and `dead`, O(k) live.

**Dry run:** `nums=[1, 3, -1, -3, 5, 3, 6, 7]`, k = 3.
- Insert 1: goes to `lo`. Insert 3: 3 > top of `lo` (1), goes to `hi`. Insert -1: -1 <= 1, goes to `lo`. Live: `lo` = {1, -1} (top 1), `hi` = {3}. Median 1.0.
- Next x = -3 arrives: -3 <= 1, goes to `lo`, and index 0 (the value 1) leaves, so it is marked dead and `lsz` drops back to 2. Balance holds; `prune(lo)` pops the dead 1 off the top. Live `lo` = {-1, -3} (top -1), `hi` = {3}. Median -1.0.
- Continue the same way: medians `[1.0, -1.0, -1.0, 3.0, 5.0, 6.0]`.

**Code:**
```python
import heapq
import random

random.seed(41)

def median_brute(nums, k):
    out = []
    for i in range(len(nums) - k + 1):
        w = sorted(nums[i:i + k])
        out.append(float(w[k // 2]) if k % 2 else (w[k // 2 - 1] + w[k // 2]) / 2)
    return out

def median_two_heaps(nums, k):
    """lo = max-heap (negated) of the smaller half, hi = min-heap of the larger half. Entries are (value, index):
    the index makes ties orderable and identifies the exact element to delete lazily."""
    lo, hi = [], []
    side = {}                 # index -> 'lo' or 'hi' for elements currently in the window
    dead = set()              # indices that left the window but may still sit inside a heap
    lsz = hsz = 0             # LIVE sizes (heap lengths include dead entries)
    out = []

    def prune(h):             # discard dead entries from the top so h[0] is a live element
        while h and h[0][1] in dead:
            dead.discard(h[0][1])
            heapq.heappop(h)

    for i, x in enumerate(nums):
        prune(lo)
        if lo and x <= -lo[0][0]:
            heapq.heappush(lo, (-x, i)); side[i] = 'lo'; lsz += 1
        else:
            heapq.heappush(hi, (x, i)); side[i] = 'hi'; hsz += 1
        if i >= k:                                   # element i-k leaves: mark only, fix the live count
            j = i - k
            dead.add(j)
            if side.pop(j) == 'lo': lsz -= 1
            else: hsz -= 1
        while lsz > (lsz + hsz + 1) // 2:            # lo may hold at most one more than hi
            prune(lo); v, j = heapq.heappop(lo); heapq.heappush(hi, (-v, j)); side[j] = 'hi'; lsz -= 1; hsz += 1
        while lsz < (lsz + hsz + 1) // 2:
            prune(hi); v, j = heapq.heappop(hi); heapq.heappush(lo, (-v, j)); side[j] = 'lo'; hsz -= 1; lsz += 1
        prune(lo); prune(hi)
        if i >= k - 1:
            out.append(float(-lo[0][0]) if k % 2 else (-lo[0][0] + hi[0][0]) / 2)
    return out

# ---- examples
for nums, k, want in [([1, 3, -1, -3, 5, 3, 6, 7], 3, [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]),
                      ([1, 2, 3, 4, 2, 3, 1, 4, 2], 3, [2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]),
                      ([1, 4, 2, 3], 4, [2.5]), ([5, 5, 5], 2, [5.0, 5.0])]:
    got = median_two_heaps(nums, k)
    assert got == median_brute(nums, k) == want, (nums, k, got)
    print(nums, k, '->', got)

# ---- tie behaviour: equal values in the heap, tuple (value, index) keeps them orderable
h = []
heapq.heappush(h, (5, 0)); heapq.heappush(h, (5, 1))
print('equal values pop by index:', heapq.heappop(h), heapq.heappop(h))
try:
    h2 = [(5, [1])]
    heapq.heappush(h2, (5, {'i': 2}))
except TypeError as e:
    print('payload without a unique int:', e)

# ---- random cross-check: heavy duplicates, odd and even k, k == 1, k == n
for _ in range(3000):
    n = random.randint(1, 14)
    nums = [random.randint(-3, 3) for _ in range(n)]
    k = random.randint(1, n)
    assert median_two_heaps(nums, k) == median_brute(nums, k), (nums, k)
print('3000 random lists agree with sort-each-window')

# ---- extremes and size
assert median_two_heaps([7], 1) == [7.0]
assert median_two_heaps([10 ** 9, 10 ** 9], 2) == [1e9]
assert median_two_heaps([-10 ** 9, 10 ** 9], 2) == [0.0]
assert median_two_heaps([1, 2, 3, 4], 1) == [1.0, 2.0, 3.0, 4.0]
nums = [random.randint(-10 ** 9, 10 ** 9) for _ in range(10 ** 5)]
for k in (1, 2, 3, 100, 1001):
    got = median_two_heaps(nums[:3000], k)
    assert got == median_brute(nums[:3000], k), k
assert len(median_two_heaps(nums, 1000)) == 10 ** 5 - 999
asc = list(range(10 ** 5))
assert median_two_heaps(asc, 5000)[:2] == [2499.5, 2500.5]
print('size 10^5 ok (ascending input, window 5000: first medians', median_two_heaps(asc, 5000)[:2], ')')
```

**Output (my run):**
```
[1, 3, -1, -3, 5, 3, 6, 7] 3 -> [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
[1, 2, 3, 4, 2, 3, 1, 4, 2] 3 -> [2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]
[1, 4, 2, 3] 4 -> [2.5]
[5, 5, 5] 2 -> [5.0, 5.0]
equal values pop by index: (5, 0) (5, 1)
payload without a unique int: '<' not supported between instances of 'dict' and 'list'
3000 random lists agree with sort-each-window
size 10^5 ok (ascending input, window 5000: first medians [2499.5, 2500.5] )
```

**Edge cases:**
- k = 1: each window is one element; k = n: one window.
- Even k: the mean of two middles may end in .5; return floats.
- Heavy duplicates: tuples `(value, index)` keep ties orderable.
- Extremes `+-10^9`: Python integers do not overflow; the mean of two ints is a float.
- Sorted or reverse-sorted input: many moves between heaps, still fine.
- Never use `len(heap)` for balance; use the live counts.

**Follow-ups:**
- *Can you avoid lazy deletion?* Yes with a sorted list and `bisect` (insert and delete by value, O(k) per step with a C-speed memmove, fine for moderate k) or `sortedcontainers.SortedList` for O(log k).
- *Do you need `(value, index)`?* Alternatives are a dict of pending deletions by value. Index is simpler to reason about when duplicates exist.
- *Streaming median without a window?* Part 8 Q17, the same two heaps without deletion.

**Common mistakes:**
- Using `len(heap)` after lazy deletion for the balance.
- Not pruning before reading `heap[0]`: the median can be an element that has left.
- Putting only `value` in the heap and deleting by value: with duplicates you may mark the wrong copy.
- Forgetting to negate when moving from `lo` to `hi`.
- Integer division for even k: the median can be `x.5`.

### Q42 ⭐ 🔴 Meeting rooms III (tie rules matter). There are rooms numbered 0..n-1 (1 <= n <= 100) and `meetings` are [start, end) pairs with all start times distinct (1 <= len <= 10^5, 0 <= start < end <= 5*10^5). Process meetings in increasing start time. A meeting takes the free room with the smallest number if any room is free at its start (a room whose meeting ends exactly at the start is free); otherwise it waits for the room that becomes free first, preferring the smallest room number among rooms that free up at the same time, and keeps its original duration, so it ends at (that room's free time) + (end - start). Return the number of the room that hosted the most meetings, the smallest such number on a tie. Keep two heaps (free room numbers, and busy rooms as (free time, room number)). Say which comparison is wrong if you forget the room number in the busy tuple. Example: n=2, meetings=[[0, 10], [1, 5], [2, 7], [3, 4]] -> 0; n=3, meetings=[[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]] -> 1; n=1, meetings=[[0, 1], [5, 6]] -> 0; n=2, meetings=[[0, 5], [1, 2], [2, 3]] -> 1.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Event simulation with two heaps: free rooms by number, busy rooms by `(free time, room number)`. The tie rules are the question.

**Say this first (1 line):** "Sort meetings by start. A min-heap of free room numbers gives the smallest free room; a min-heap of `(free time, room)` tells me which room frees first, and the room number in the tuple breaks ties."

**Brute force:** Keep an array `avail[room]`. For each meeting scan all n rooms for the smallest one with `avail <= start`; if none, take the smallest room with the minimum `avail`. O(m * n) for m meetings, which is 10^7 at the limits and fine as a check, but the heaps are the point.

**Optimal:**
- Sort meetings by start. Starts are distinct, so there is no tie among meetings.
- Before each meeting, move every busy room with `free time <= start` to the free heap (`<=`, because a meeting ending exactly at this start leaves the room free).
- If a room is free: pop the smallest number `r`, push `(end, r)` to busy.
- If none is free: pop the busy room with the earliest free time `t` (smallest room number on a tie, from the tuple), and push `(t + (end - start), r)`. The meeting waited, so it keeps its duration.
- Count meetings per room. Answer: `cnt.index(max(cnt))` (`index` returns the smallest room among equal counts).
- What goes wrong without the room number in the busy tuple:
  - If the tuple is only `(free time,)` you cannot tell which room freed.
  - If you add something else second (a meeting index, in the code's buggy variant), then rooms freeing at the same time come out in the order their meetings started, not in room-number order. The code finds a failing case (n = 2) where that variant answers 1 and the correct answer is 0.
  - If you put a room object there, a tie raises `TypeError` (shown). A plain int room number is the right second element: unique and exactly the tie-break the problem states.
- Delay can push ends past 5 * 10^5; Python integers do not overflow, and no clamping is wanted.

**Complexity:** Time O(m log m) for the sort plus O((m + n) log n) for heap work: each meeting causes at most one pop and one push on `busy` and each room moves between heaps once per meeting. Space O(n) for heaps and counts (plus the sorted copy of the meetings).

**Dry run:** `n=2, [[0,10],[1,5],[2,7],[3,4]]`.
- Meeting [0,10]: room 0 free, takes it, busy `(10, 0)`.
- Meeting [1,5]: nothing frees by 1; free has room 1: busy `(5, 1)`, `(10, 0)`.
- Meeting [2,7]: no free room. Earliest busy is `(5, 1)`; the meeting runs from 5 to 5 + 5 = 10. Room 1 now `(10, 1)`. cnt = [1, 2].
- Meeting [3,4]: no free room. Earliest: `(10, 0)` before `(10, 1)` on the tie (smaller room). It ends at 10 + 1 = 11 in room 0. cnt = [2, 2].
- Tie on count: smallest room, 0.

**Code:**
```python
import heapq
import random

random.seed(42)

def rooms_brute(n, meetings):
    """Simulate with a plain array of 'room free at time t' values; scan all rooms per meeting."""
    avail, cnt = [0] * n, [0] * n
    for s, e in sorted(meetings):
        free = [r for r in range(n) if avail[r] <= s]
        if free:
            r = free[0]; avail[r] = e                      # smallest free room number
        else:
            t = min(avail); r = avail.index(t)             # earliest free time, smallest room number among equals
            avail[r] = t + (e - s)                         # keeps its duration
        cnt[r] += 1
    return cnt.index(max(cnt))                             # index() = smallest room number among ties

def rooms_heaps(n, meetings, busy_key=None):
    """free: min-heap of room numbers. busy: min-heap of (free_time, room). Two heaps, one pass over sorted meetings."""
    free = list(range(n)); heapq.heapify(free)
    busy, cnt = [], [0] * n
    for s, e in sorted(meetings):
        while busy and busy[0][0] <= s:                    # <=: a room freed exactly at s is available
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            r = heapq.heappop(free)
            heapq.heappush(busy, (e, r))
        else:
            t, r = heapq.heappop(busy)                     # ties on t resolved by the smaller room number
            heapq.heappush(busy, (t + e - s, r))
        cnt[r] += 1
    return cnt.index(max(cnt))

def rooms_wrong_tiebreak(n, meetings):
    """Bug: busy tuple (free_time, meeting_index, room): on equal free times the earliest-STARTED meeting's room wins, not the smallest room."""
    free = list(range(n)); heapq.heapify(free)
    busy, cnt = [], [0] * n
    for idx, (s, e) in enumerate(sorted(meetings)):
        while busy and busy[0][0] <= s:
            heapq.heappush(free, heapq.heappop(busy)[2])
        if free:
            r = heapq.heappop(free)
            heapq.heappush(busy, (e, idx, r))
        else:
            t, i, r = heapq.heappop(busy)
            heapq.heappush(busy, (t + e - s, idx, r))
        cnt[r] += 1
    return cnt.index(max(cnt))

# ---- examples
for n, m, want in [(2, [[0, 10], [1, 5], [2, 7], [3, 4]], 0),
                   (3, [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]], 1),
                   (1, [[0, 1], [5, 6]], 0),
                   (2, [[0, 5], [1, 2], [2, 3]], 1)]:
    assert rooms_heaps(n, m) == rooms_brute(n, m) == want, (n, m)
    print('n =', n, m, '->', rooms_heaps(n, m))

# ---- tie behaviour of heap tuples: (free_time, room) breaks ties by smaller room
h = []
heapq.heappush(h, (10, 2)); heapq.heappush(h, (10, 0)); heapq.heappush(h, (10, 1))
print('busy rooms that free at the same time pop in room order:', [heapq.heappop(h) for _ in range(3)])
try:
    h = []
    heapq.heappush(h, (10, {'room': 2})); heapq.heappush(h, (10, {'room': 0}))
except TypeError as e:
    print('storing a room object instead of its number ->', e)

# ---- random cross-check; meetings with distinct starts (the prompt's guarantee)
def rand_case():
    n = random.randint(1, 4)
    starts = random.sample(range(0, 14), random.randint(1, 8))
    return n, [[s, s + random.randint(1, 6)] for s in starts]
bug_found = None
for _ in range(4000):
    n, m = rand_case()
    random.shuffle(m)
    assert rooms_heaps(n, m) == rooms_brute(n, m), (n, m)
    if bug_found is None and rooms_wrong_tiebreak(n, m) != rooms_brute(n, m):
        bug_found = (n, sorted(m))
print('4000 random cases agree with the brute-force simulation')
print('forgetting the room number as the tie-break (using meeting index) fails, e.g.:', bug_found,
      'wrong =', rooms_wrong_tiebreak(*bug_found), 'right =', rooms_heaps(*bug_found))

# ---- edge asserts
assert rooms_heaps(1, [[0, 1]]) == 0
assert rooms_heaps(3, [[0, 1]]) == 0                      # only one meeting: room 0, ties resolved to the smallest
assert rooms_heaps(2, [[0, 5], [5, 6]]) == 0              # end == next start: room 0 is free again (end is exclusive)
assert rooms_heaps(2, [[0, 5], [1, 3], [3, 4]]) == 1      # room 1 frees at 3 exactly when the third starts
n = 100
LIM = 5 * 10 ** 5
big = [[s0, random.randint(s0 + 1, LIM)] for s0 in random.sample(range(0, LIM), 10 ** 5)]   # distinct starts, start < end <= LIM
assert len(big) == 10 ** 5 and all(0 <= a < b <= LIM for a, b in big)
r = rooms_heaps(n, big)
assert 0 <= r < n
print('n=100, 10^5 meetings: busiest room', r)
```

**Output (my run):**
```
n = 2 [[0, 10], [1, 5], [2, 7], [3, 4]] -> 0
n = 3 [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]] -> 1
n = 1 [[0, 1], [5, 6]] -> 0
n = 2 [[0, 5], [1, 2], [2, 3]] -> 1
busy rooms that free at the same time pop in room order: [(10, 0), (10, 1), (10, 2)]
storing a room object instead of its number -> '<' not supported between instances of 'dict' and 'dict'
4000 random cases agree with the brute-force simulation
forgetting the room number as the tie-break (using meeting index) fails, e.g.: (2, [[3, 7], [4, 6], [5, 7], [7, 13], [8, 10], [10, 16], [12, 15], [13, 18]]) wrong = 1 right = 0
n=100, 10^5 meetings: busiest room 54
```

**Edge cases:**
- One room: everything queues; room 0 wins.
- More rooms than meetings: unused rooms have count 0; the busiest is still found.
- `end == next start`: room is free (`<=`, end exclusive).
- Equal free times in the waiting case: smallest room number first.
- Tie in counts: smallest room.
- Large delays: sums can exceed the input range; ints are fine.

**Follow-ups:**
- *Why distinct starts?* It removes ties among meetings; with equal starts you must also fix the order of those meetings (say, by shorter first or input order).
- *Meeting rooms II uses one heap of end times; why two here?* Here the room identity matters (numbers, counts), not just how many are busy.
- *Faster for large n?* Not needed at n <= 100; the heaps scale to any n.

**Common mistakes:**
- `<` instead of `<=` when freeing rooms.
- Delayed meeting starts at its original start instead of the room's free time; it must end at `free time + duration`.
- Forgetting that the free heap must be keyed by room number so the smallest is chosen.
- Using `max(cnt)` as the answer; it is the room index.
- Counting a delayed meeting in the room it did not use (count the room you popped).

### Q43 ⭐ 🔴 Smallest range covering elements from k lists. `lists` holds k sorted (non-decreasing) non-empty integer lists (1 <= k <= 3500, total length N <= 10^5, |value| <= 10^5). Return the range [a, b] with the smallest b - a that contains at least one element from every list; if several ranges have the same width, return the one with the smaller a. Keep a min-heap with one current element per list and track the maximum of the heap's elements: the current range is [heap min, tracked max]; advance the list that supplied the minimum and stop when one list runs out. State the cost (O(N log k)) and why stopping at the first exhausted list is correct. Example: lists=[[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]] -> [20, 24]; lists=[[1, 2, 3], [1, 2, 3], [1, 2, 3]] -> [1, 1]; lists=[[1], [5]] -> [1, 5]; lists=[[1, 5], [2]] -> [1, 2].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** K-way merge with a min-heap that holds one current element per list, plus a tracked maximum. The window is `[heap min, tracked max]`.

**Say this first (1 line):** "Put the first element of every list in a min-heap and remember the largest of them. That pair is a valid range. To shrink it I must move the minimum forward, so I replace it with the next element of its own list and update the maximum."

**Brute force:** For every pair of values `(a, b)`, check that each list has an element in `[a, b]` and keep the narrowest, smaller `a` on a tie. Roughly V^2 * N work for V distinct values. Only usable on tiny inputs; it is the checker.

**Optimal:**
- Heap entries `(value, list index, position)`; `hi` = max of the current elements.
- Loop:
  - The current range is `[heap[0][0], hi]`. It has one element from every list, so it is valid. Keep it if narrower, or equal width with a smaller start.
  - Take the minimum's list `i`, position `j`. If `j` is the last position of that list, stop.
  - Otherwise `heapreplace` the minimum with `(lists[i][j+1], i, j+1)` and set `hi = max(hi, new value)`.
- Why stop when a list runs out: the minimum is that list's last element. Any later range must start above the current minimum (we only ever move minimums up), so it would contain no element of that list and could not be valid. Every remaining range is therefore invalid.
- Why moving only the minimum is right: for the current set of candidates, `hi` is fixed by the largest element, so no range with this minimum can be narrower than `[min, hi]`. The only way to improve is to drop the minimum, and the next candidate from its list is the smallest replacement that keeps that list covered.
- Tie breaking: equal values from different lists compare the list index next. This is why the tuple has the list index: it is an int, always orderable, and keeps the run deterministic. Pushing `(value, the list)` can raise `TypeError` for unorderable payloads, or silently compare list contents on lists (the code shows both).
- Widths: equal-width ranges come out in increasing start order, so the first one found is the smaller-`a` answer; the condition still checks `lo < best[0]` for safety. The checker compares with the brute force on duplicates and negatives.

**Complexity:** Time O(N log k): each of the N elements is replaced into the heap once, at O(log k). Space O(k) for the heap (the lists themselves are input).

**Dry run:** `[[4,10,15,24,26], [0,9,12,20], [5,18,22,30]]`.
- Start heap 0, 4, 5; hi = 5; range [0, 5] width 5.
- Replace 0 with 9: heap 4, 5, 9; hi = 9; [4, 9] width 5, not narrower.
- Replace 4 with 10: 5, 9, 10; [5, 10] width 5. Replace 5 with 18: 9, 10, 18; [9, 18] width 9.
- Replace 9 with 12: 10, 12, 18; [10, 18]. Replace 10 with 15: 12, 15, 18; [12, 18] width 6.
- Replace 12 with 20: 15, 18, 20; [15, 20] width 5. Replace 15 with 24: 18, 20, 24; [18, 24] width 6.
- Replace 18 with 22: 20, 22, 24; [20, 24] width 4, the new best. The next minimum 20 is the last element of its list: stop. Answer `[20, 24]`.

**Code:**
```python
import heapq
import random

random.seed(43)

def range_brute(lists):
    """Try every pair (a, b) of values; keep the narrowest valid one, smaller a on a tie."""
    vals = sorted({x for l in lists for x in l})
    best = None
    for a in vals:
        for b in vals:
            if b >= a and all(any(a <= x <= b for x in l) for l in lists):
                if best is None or (b - a, a) < (best[1] - best[0], best[0]):
                    best = [a, b]
    return best

def range_heap(lists):
    """Heap of (value, list index, position): one current element per list. The index is unique per list, so ties never
    compare anything unorderable. hi = max of the current elements, tracked as we push."""
    heap = [(l[0], i, 0) for i, l in enumerate(lists)]
    heapq.heapify(heap)
    hi = max(v for v, _, _ in heap)
    best = [heap[0][0], hi]
    while True:
        lo, i, j = heap[0]
        if hi - lo < best[1] - best[0] or (hi - lo == best[1] - best[0] and lo < best[0]):
            best = [lo, hi]
        if j + 1 == len(lists[i]):            # the list that supplied the minimum is exhausted: no window can cover it any more
            return best
        nxt = lists[i][j + 1]
        heapq.heapreplace(heap, (nxt, i, j + 1))     # pop min and push its successor in one O(log k) step
        hi = max(hi, nxt)

# ---- examples
for lists, want in [([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]], [20, 24]),
                    ([[1, 2, 3], [1, 2, 3], [1, 2, 3]], [1, 1]),
                    ([[1], [5]], [1, 5]),
                    ([[1, 5], [2]], [1, 2])]:
    assert range_heap(lists) == range_brute(lists) == want, (lists, range_heap(lists))
    print(lists, '->', range_heap(lists))

# ---- tie behaviour: equal values from different lists
h = [(5, 2, 0), (5, 0, 3), (5, 1, 1)]
heapq.heapify(h)
print('equal values pop by list index, then position:', [heapq.heappop(h) for _ in range(3)])
try:
    h = []
    heapq.heappush(h, (5, [1, 2])); heapq.heappush(h, (5, [1, 3]))
    print('(value, the list itself) happens to work for lists: a tie compares list CONTENTS, O(len) per tie and not an intended order')
    heapq.heappush(h, (5, {'a': 1}))
except TypeError as e:
    print('but any unorderable payload on a tie fails ->', e)
print('so push (value, list index, position), not (value, the list)')

# ---- random cross-check: duplicates, negatives, equal-width ranges (smaller a must win)
for _ in range(2500):
    k = random.randint(1, 4)
    lists = [sorted(random.randint(-5, 8) for _ in range(random.randint(1, 5))) for _ in range(k)]
    assert range_heap(lists) == range_brute(lists), lists
print('2500 random list sets agree with the all-pairs brute force (width then smaller a)')

# ---- why stopping at the first exhausted list is correct: a window must contain an element of that list; every unused one is
# larger than the heap minimum already tried, so any further window starts higher AND misses the exhausted list's last element.
# a tie example where the later range has the same width: smaller a must be kept
assert range_heap([[1, 5], [2, 6]]) == [1, 2] == range_brute([[1, 5], [2, 6]])
assert range_heap([[1, 3], [2, 4]]) == [1, 2] == range_brute([[1, 3], [2, 4]])
print('tie on width [[1,3],[2,4]] ->', range_heap([[1, 3], [2, 4]]), '(widths 1 at [1,2], [2,3], [3,4]: smallest a wins)')

# ---- edge asserts and size
assert range_heap([[7]]) == [7, 7]
assert range_heap([[-10 ** 5, 10 ** 5]]) == [-10 ** 5, -10 ** 5]            # k = 1: any single element has width 0, smallest a
assert range_heap([[0], [0], [0]]) == [0, 0]
N, K = 10 ** 5, 3500
lists = [[random.randint(-10 ** 5, 10 ** 5)] for _ in range(K)]          # every list non-empty
for _ in range(N - K):
    lists[random.randrange(K)].append(random.randint(-10 ** 5, 10 ** 5))
lists = [sorted(l) for l in lists]
assert sum(map(len, lists)) == N
res = range_heap(lists)
assert res[0] <= res[1] and all(any(res[0] <= x <= res[1] for x in l) for l in lists)
print('k=3500, N=10^5: range', res, 'covers every list')
```

**Output (my run):**
```
[[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]] -> [20, 24]
[[1, 2, 3], [1, 2, 3], [1, 2, 3]] -> [1, 1]
[[1], [5]] -> [1, 5]
[[1, 5], [2]] -> [1, 2]
equal values pop by list index, then position: [(5, 0, 3), (5, 1, 1), (5, 2, 0)]
(value, the list itself) happens to work for lists: a tie compares list CONTENTS, O(len) per tie and not an intended order
but any unorderable payload on a tie fails -> '<' not supported between instances of 'dict' and 'list'
so push (value, list index, position), not (value, the list)
2500 random list sets agree with the all-pairs brute force (width then smaller a)
tie on width [[1,3],[2,4]] -> [1, 2] (widths 1 at [1,2], [2,3], [3,4]: smallest a wins)
k=3500, N=10^5: range [-51474, -5053] covers every list
```

**Edge cases:**
- One list: width 0, the smallest element, `[a, a]`.
- All lists identical: `[x, x]` for the smallest common value.
- A single-element list pins its element into every range (example `[[1],[5]]`).
- Negative values and duplicates inside a list: fine, order is by value.
- Equal-width ranges: smaller `a` wins (checked by brute force).
- k = 3500 and N = 10^5: the heap stays at 3500 entries.

**Follow-ups:**
- *Sliding-window alternative?* Merge all `(value, list id)` pairs, sort, and slide a window until every list id is covered (shrink from the left while still covered). O(N log N) for the sort, simple to write.
- *Why `heapreplace` and not pop then push?* One sift instead of two; same result.
- *What if some list may be empty?* Then no range exists; return an empty answer up front.

**Common mistakes:**
- Advancing the maximum's list instead of the minimum's.
- Forgetting to update `hi` after pushing a new element.
- Continuing after a list is exhausted (pushing past its end).
- Pushing `(value, list)` and relying on tuple comparison for ties.
- Using `<=` on width with a start check inverted, returning the larger `a` on ties.

### Q44 ⭐ 🔴 Maximise capital with at most k projects (IPO). You start with capital `w`; project i needs capital[i] to start and adds profits[i] to your capital once finished (0 <= profits[i] <= 10^4, 0 <= capital[i] <= 10^9, 1 <= len <= 10^5, 0 <= k <= 10^5, 0 <= w <= 10^9). You may finish at most k projects, one after another, each at most once, and can start a project only when your current capital is at least its requirement. Return the maximum final capital. Sort projects by required capital, push the profits of every newly affordable project into a max-heap (negated), and take the best one each round; explain why taking the largest available profit is optimal (it only enlarges the set of affordable projects) and what happens when the heap is empty (stop early). Example: k=2, w=0, profits=[1, 2, 3], capital=[0, 1, 1] -> 4; k=3, w=0, profits=[1, 2, 3], capital=[0, 1, 2] -> 6; k=1, w=0, profits=[5], capital=[1] -> 0; k=0, w=4, profits=[9], capital=[0] -> 4.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy with a max-heap: among everything currently affordable, take the largest profit. Sorting by required capital unlocks projects in order.

**Say this first (1 line):** "Sort projects by required capital. Each round, push the profits of every project I can now afford into a max-heap and take the biggest; if the heap is empty I stop, because capital will never grow."

**Brute force:** Try every order of at most k distinct affordable projects (depth-first, capital updated as you go). That is up to n!/(n-k)! orders, so only tiny inputs. It is the cross-check.

**Optimal:**
- `projects = sorted(zip(capital, profit))`; pointer `i`; max-heap of profits (negated values, because `heapq` is a min-heap).
- Repeat up to k times:
  - While `projects[i]` needs capital `<= w`, push its profit and advance `i`.
  - If the heap is empty: break (nothing is affordable and capital can only grow by finishing a project, so it is stuck).
  - Otherwise pop the largest profit and add it to `w`.
- Why the largest profit is optimal: every project has a fixed gain, and finishing a project never lowers capital, so the only effect of a choice is how much capital you have afterwards, which decides which projects unlock. Exchange argument: take any optimal plan; if at some step it picks a smaller profit `p'` while a larger affordable `p` exists, swap them. After the swap capital is at least as large at every later point (you hold `p` sooner and `p'` is still affordable later because capital is larger), so the rest of the plan stays feasible and the final total does not drop. So there is an optimal plan that always takes the largest affordable profit.
- Cheapest-capital-first is a different greedy that is wrong: the code finds `k=1, w=4, profits=[0, 4], capital=[0, 1]` where it takes the zero-profit project (final 4) and the right answer is 8.
- Zero profits are allowed: they never help, but taking one does not hurt; the loop still terminates after k rounds.
- Heap tie-breaking: the heap holds only negated ints, so equal profits tie with nothing to compare. If you push `(-profit, project_object)`, equal profits compare the objects and raise `TypeError` (shown). The sort of `(capital, profit)` pairs compares ints, so it is safe.

**Complexity:** Time O(n log n): one sort, each project is pushed at most once and popped at most once (at most min(k, n) pops). Space O(n) for the sorted copy and the heap.

**Dry run:** `k=2, w=0, profits=[1,2,3], capital=[0,1,1]`.
- Sorted by capital: `(0,1), (1,2), (1,3)`.
- Round 1: w = 0 affords `(0,1)`: push 1. Pop 1, w = 1.
- Round 2: w = 1 now affords `(1,2)` and `(1,3)`: push 2, 3. Pop 3, w = 4.
- k used up. Answer 4.

**Code:**
```python
import heapq
import random

random.seed(44)

def ipo_brute(k, w, profits, capital):
    """Exhaustive search over every order of at most k distinct projects (tiny inputs only)."""
    best = w
    def go(w, used, left):
        nonlocal best
        best = max(best, w)
        if left == 0:
            return
        for i in range(len(profits)):
            if not used >> i & 1 and capital[i] <= w:
                go(w + profits[i], used | 1 << i, left - 1)
    go(w, 0, k)
    return best

def ipo_greedy(k, w, profits, capital):
    projects = sorted(zip(capital, profits))             # by required capital; ties compare profit, which is fine (ints)
    heap = []                                            # max-heap of profits of affordable projects (negated)
    i = 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(heap, -projects[i][1])        # unlock everything now affordable
            i += 1
        if not heap:
            break                                        # nothing affordable and capital cannot grow: stop early
        w -= heapq.heappop(heap)                         # take the biggest profit (w - (-p) = w + p)
    return w

def ipo_wrong_cheapest(k, w, profits, capital):
    """Counter-example rule: always take the lowest-capital affordable project (not the most profitable)."""
    ps = sorted(zip(capital, profits)); used = [False] * len(ps)
    for _ in range(k):
        pick = next((j for j in range(len(ps)) if not used[j] and ps[j][0] <= w), None)
        if pick is None: break
        used[pick] = True; w += ps[pick][1]
    return w

# ---- examples
for k, w, pr, cp, want in [(2, 0, [1, 2, 3], [0, 1, 1], 4), (3, 0, [1, 2, 3], [0, 1, 2], 6), (1, 0, [5], [1], 0), (0, 4, [9], [0], 4)]:
    got = ipo_greedy(k, w, pr, cp)
    assert got == ipo_brute(k, w, pr, cp) == want, (k, w, pr, cp, got)
    print('k =', k, 'w =', w, pr, cp, '->', got)

# ---- heap tie behaviour: only ints are pushed (negated profits), so equal profits tie harmlessly. A (profit, project) tuple with
# a non-comparable payload is where it would break.
class P:
    def __init__(self, n): self.n = n
h = []
heapq.heappush(h, (-3, P('a')))
try:
    heapq.heappush(h, (-3, P('b')))
except TypeError as e:
    print('heap of (-profit, project object) on equal profits ->', e)
h = [-3, -3, -5]
heapq.heapify(h)
print('heap of plain negated ints, equal profits are harmless:', [-heapq.heappop(h) for _ in range(3)])

# ---- random cross-check against the exhaustive search (n <= 6)
beaten = None
for _ in range(2500):
    n = random.randint(1, 6)
    pr = [random.randint(0, 6) for _ in range(n)]
    cp = [random.randint(0, 8) for _ in range(n)]
    k, w = random.randint(0, 5), random.randint(0, 4)
    g = ipo_greedy(k, w, pr, cp)
    assert g == ipo_brute(k, w, pr, cp), (k, w, pr, cp)
    if beaten is None and ipo_wrong_cheapest(k, w, pr, cp) < g:
        beaten = (k, w, pr, cp)
print('2500 random cases agree with exhaustive search')
print('cheapest-capital-first is not optimal, e.g. (k, w, profits, capital) =', beaten,
      'wrong =', ipo_wrong_cheapest(*beaten), 'right =', ipo_greedy(*beaten))

# ---- edge asserts and size
assert ipo_greedy(3, 0, [4, 4], [1, 2]) == 0                     # nothing affordable: heap empty, stop
assert ipo_greedy(10, 0, [0, 0], [0, 0]) == 0                    # zero profits, k larger than the project count
assert ipo_greedy(1, 10 ** 9, [10 ** 4], [10 ** 9]) == 10 ** 9 + 10 ** 4
n = 10 ** 5
pr = [random.randint(0, 10 ** 4) for _ in range(n)]
cp = [random.randint(0, 10 ** 9) for _ in range(n)]
r = ipo_greedy(n, 0, pr, cp)
assert r >= 0
r2 = ipo_greedy(n, 10 ** 9, pr, cp)
assert r2 == 10 ** 9 + sum(pr)                                    # capital covers everything: take every project
print('n=10^5 ok; with w = 10^9 every project is affordable, final capital', r2)
```

**Output (my run):**
```
k = 2 w = 0 [1, 2, 3] [0, 1, 1] -> 4
k = 3 w = 0 [1, 2, 3] [0, 1, 2] -> 6
k = 1 w = 0 [5] [1] -> 0
k = 0 w = 4 [9] [0] -> 4
heap of (-profit, project object) on equal profits -> '<' not supported between instances of 'P' and 'P'
heap of plain negated ints, equal profits are harmless: [5, 3, 3]
2500 random cases agree with exhaustive search
cheapest-capital-first is not optimal, e.g. (k, w, profits, capital) = (1, 4, [0, 4], [0, 1]) wrong = 4 right = 8
n=10^5 ok; with w = 10^9 every project is affordable, final capital 1499726129
```

**Edge cases:**
- `k = 0`: return `w` unchanged.
- Nothing affordable at the start: heap empty, stop, answer `w`.
- `k` larger than the number of projects: the heap empties and the loop breaks.
- Capital up to 10^9 and profits up to 10^4: no overflow in Python.
- Many projects with equal capital: all unlocked together, the best is taken first.
- Finishing a project is optional but never harmful, since profits are non-negative.

**Follow-ups:**
- *Why does the prompt need non-negative profits?* With negative profits you would stop early rather than take them; the loop would then need a `if best <= 0: break`.
- *What if k is huge?* The loop stops as soon as the heap is empty, so it never does more than n rounds.
- *Is sorting needed if capital values are small?* A bucket by capital would give O(n + C), but sorting is simpler.

**Common mistakes:**
- Using a min-heap of profits without negating.
- Re-scanning all projects each round (O(n k)) instead of a pointer.
- Not breaking when the heap is empty, so the loop adds from an empty heap and crashes.
- Choosing the cheapest-capital project instead of the most profitable.
- Pushing `(-profit, object)` and hitting `TypeError` on ties.

### Q45 ⭐ 🔴 Rearrange a string so equal letters are at least k apart. Given a lowercase string `s` (0 <= len <= 3*10^4) and an integer 0 <= k <= len(s), rearrange the letters so that any two equal letters are at index distance at least k, and return the result, or '' if impossible (k = 0 and k = 1 impose nothing, so return s itself). Several answers can be valid, and the checker accepts any permutation of `s` with the distance property (and requires '' exactly when none exists, tested exhaustively on short strings). Use a max-heap of remaining counts plus a queue that holds each used letter out for k steps; say why the heap pop order (largest count first) is the right greedy, and when the queue holds fewer than k items at the end. Example: s='aabbcc', k=3 -> 'abcabc'; s='aaabc', k=3 -> ''; s='aaadbbcc', k=2 -> 'abacabcd'; s='abc', k=0 -> 'abc'.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy with a max-heap of remaining counts plus a cooldown queue (the same idea as Part 8 Q11, the task scheduler, and Q15, reorganize string, with a general distance k).

**Say this first (1 line):** "Always place the letter with the most remaining copies that is allowed right now; once placed, hold it out in a queue for k steps so it cannot be reused too soon. If the heap runs dry with letters still waiting, it is impossible."

**Brute force:** Try every distinct permutation and test the distance rule: O(n! * n), only for n <= 8. It is the exhaustive checker for both the validity of the output and the claim that `''` appears exactly when no arrangement exists.

**Optimal:**
- If `k <= 1`, there is no constraint: return `s` (this also covers the empty string).
- `heap` holds `(-remaining count, letter)`; `wait` is a deque of letters used recently.
- Repeat while the heap is not empty:
  - Pop the top `(negc, ch)`. Append `ch` to the output.
  - Append `(negc + 1, ch)` to `wait` (one fewer to place).
  - When `len(wait) >= k`, pop the left item of `wait`: that letter was used exactly k steps ago, so it may be used again. If its remaining count is not zero, push it back on the heap.
- If the output has fewer letters than `s`, return `''`.
- Why the largest count first: think of the output as blocks of k positions; within a block every letter must be different (distance >= k), so a block takes k distinct letters. The letters with the most copies left have the least slack (they need the most blocks), so they must be used in every block while others can wait. The code checks this against exhaustive search on every multiset of up to 7 letters over `abc` and up to 5 over `abcd` for every k: no mismatch. This is a verification, not a proof.
- When `''` happens: the heap is empty but the queue still holds letters with copies left. Because the loop moves a letter out of the queue as soon as `len(wait) == k`, the queue never holds k items at that moment, so those letters are still cooling, and there is nothing allowed to place. Success means all letters are placed; the queue may still hold up to `k - 1` finished letters with count zero, which is fine.
- Heap tie-breaking: tuples `(-count, letter)`: equal counts compare the letters (strings are orderable), so the output is deterministic (the code shows alphabetical order). With an unorderable payload instead of a letter, equal counts raise `TypeError`. Any valid arrangement is accepted, so the tie order does not affect correctness, only which valid answer you get.

**Complexity:** Time O(n log m) where m is the number of distinct letters (at most 26): each of the n placements is one pop and at most one push. Space O(m) for the heap plus O(k) for the queue (at most min(k, n) items) and the O(n) output.

**Dry run:** `s='aabbcc'`, k = 3.
- Heap: a2, b2, c2. Pop a: out `a`, wait [a1]. Pop b: out `ab`, wait [a1, b1]. Pop c: out `abc`, wait [a1, b1, c1]; length 3 = k, so pop a1 and push it back.
- Pop a: out `abca`, wait [b1, c1, a0]; length 3, pop b1 and push it.
- Pop b: out `abcab`, wait [c1, a0, b0]; pop c1 and push it.
- Pop c: out `abcabc`, wait [a0, b0, c0]; pop a0, nothing to push. Heap empty. Length 6 = len(s): success.

**Code:**
```python
import heapq
import itertools
import random
from collections import Counter, deque

random.seed(45)

def ok(s, k, got):
    """Valid if got is a permutation of s and equal letters are at index distance >= k."""
    if sorted(got) != sorted(s):
        return False
    last = {}
    for i, ch in enumerate(got):
        if ch in last and i - last[ch] < k:
            return False
        last[ch] = i
    return True

def feasible_brute(s, k):
    """Exhaustive: does ANY permutation of s keep equal letters at distance >= k?"""
    return any(ok(s, k, ''.join(p)) for p in set(itertools.permutations(s)))

def rearrange(s, k):
    if k <= 1:
        return s                                          # no constraint (also handles s == '')
    heap = [(-c, ch) for ch, c in Counter(s).items()]     # max-heap on remaining count; letter breaks ties (str is orderable)
    heapq.heapify(heap)
    wait = deque()                                        # letters used in the last k-1 steps, held out of the heap
    out = []
    while heap:
        negc, ch = heapq.heappop(heap)                    # most remaining letter that is allowed now
        out.append(ch)
        wait.append((negc + 1, ch))                       # one fewer to place
        if len(wait) >= k:                                # this letter's cooling period is over exactly k steps later
            c2, ch2 = wait.popleft()
            if c2:
                heapq.heappush(heap, (c2, ch2))
    return ''.join(out) if len(out) == len(s) else ''     # heap ran dry with letters still waiting: impossible

# ---- examples (any valid arrangement is accepted; the prompt's string is one of them)
for s, k, want in [('aabbcc', 3, 'abcabc'), ('aaabc', 3, ''), ('aaadbbcc', 2, 'abacabcd'), ('abc', 0, 'abc')]:
    got = rearrange(s, k)
    assert (got == '') == (want == '') and (got == '' or ok(s, k, got)) and (want == '' or ok(s, k, want)), (s, k, got)
    print(repr(s), k, '->', repr(got), '| prompt answer', repr(want), 'also valid' if want and ok(s, k, want) else '')

# ---- tie behaviour in the heap: equal counts are broken by the letter, so the output is deterministic
h = [(-2, 'b'), (-2, 'a'), (-1, 'c')]
heapq.heapify(h)
print('equal counts pop alphabetically:', [heapq.heappop(h) for _ in range(3)])
try:
    h = []
    heapq.heappush(h, (-2, {'ch': 'a'})); heapq.heappush(h, (-2, {'ch': 'b'}))
except TypeError as e:
    print('with an unorderable payload instead of a letter ->', e)

# ---- exhaustive: every string over {a,b,c} up to length 7 (and 'abcd' up to 6), every k from 0 to len
cases = infeasible = 0
for alpha, maxlen in (('abc', 7), ('abcd', 5)):
    for n in range(0, maxlen + 1):
        for t in itertools.product(alpha, repeat=n):
            s = ''.join(t)
            if s != ''.join(sorted(s)):
                continue                                  # sorted representatives cover every multiset
            for k in range(0, n + 1):
                got = rearrange(s, k)
                if s == '':
                    assert got == ''                      # empty input: the empty string is the (valid) answer
                elif got:
                    assert ok(s, k, got), (s, k, got)
                else:
                    assert s == '' or k > 1, (s, k)
                    assert not feasible_brute(s, k), ('claimed impossible but a rearrangement exists', s, k)
                    infeasible += 1
                cases += 1
print('exhaustive over all multisets up to the sizes above:', cases, 'cases;', infeasible, "returned '' and brute force confirms none exists")

# ---- random cross-check on longer strings (validity only, plus feasibility by the known counting argument is NOT assumed)
for _ in range(1000):
    s = ''.join(random.choice('abcde') for _ in range(random.randint(1, 8)))
    k = random.randint(0, len(s))
    got = rearrange(s, k)
    assert (got != '' and ok(s, k, got)) or (got == '' and not feasible_brute(s, k)), (s, k)
print('1000 random strings (len <= 8) agree with exhaustive feasibility')

# ---- edge asserts and size
assert rearrange('', 0) == '' and rearrange('', 5) == ''
assert rearrange('a', 1) == 'a'
assert rearrange('aa', 2) == '' and rearrange('ab', 2) == 'ab'
assert rearrange('aab', 2) in ('aba',)
big = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3 * 10 ** 4))
for k in (0, 1, 2, 5, 20):
    g = rearrange(big, k); assert g and ok(big, k, g)
big2 = 'a' * 15000 + 'b' * 15000
assert rearrange(big2, 2) and ok(big2, 2, rearrange(big2, 2)) and rearrange(big2, 3) == ''
print('size 3*10^4 ok; strings of two letters with k=2 feasible, k=3 impossible')
```

**Output (my run):**
```
'aabbcc' 3 -> 'abcabc' | prompt answer 'abcabc' also valid
'aaabc' 3 -> '' | prompt answer '' 
'aaadbbcc' 2 -> 'abacabcd' | prompt answer 'abacabcd' also valid
'abc' 0 -> 'abc' | prompt answer 'abc' also valid
equal counts pop alphabetically: [(-2, 'a'), (-2, 'b'), (-1, 'c')]
with an unorderable payload instead of a letter -> '<' not supported between instances of 'dict' and 'dict'
exhaustive over all multisets up to the sizes above: 1380 cases; 704 returned '' and brute force confirms none exists
1000 random strings (len <= 8) agree with exhaustive feasibility
size 3*10^4 ok; strings of two letters with k=2 feasible, k=3 impossible
```

**Edge cases:**
- `k = 0` or `k = 1`: return `s` unchanged (even if it has equal neighbours).
- Empty string: `''` is the valid answer (so `''` can also mean "fine", not only "impossible"; the prompt's rule is for non-empty input).
- One letter repeated more than once with `k >= 2`: impossible, `''`.
- `k = len(s)`: possible only if all letters are distinct.
- Many distinct letters: the queue holds at most k items, so memory stays small.
- 3 * 10^4 characters: one pass, no recursion.

**Follow-ups:**
- *Why not the simple "interleave by sorted frequency" trick from reorganize string?* It works for k = 2 only. General k needs the cooldown queue.
- *What if k can exceed len(s)?* The prompt bounds it at len(s). Larger k works the same way: only an all-distinct string can succeed and the queue simply never reaches k.
- *Task scheduler (Part 8 Q11) is the counting version of this.* There you only need the length with idle slots, not the arrangement.

**Common mistakes:**
- Putting the letter back on the heap immediately (distance becomes 1).
- Releasing from the queue at `len(wait) > k` instead of `>= k`, giving distance k + 1 and rejecting feasible inputs.
- Pushing back letters whose count is zero.
- Forgetting the `k <= 1` shortcut: the prompt wants `s` itself back, while the heap path would return a regrouped permutation.
- Returning the partial output instead of `''` when the heap runs dry.

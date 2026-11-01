### Q1 ⭐⭐⭐ 🟢 Python heapq basics and the max-heap trick. `heapq` is a binary min-heap stored in a plain list. Given a list `vals` of integers (0 <= len <= 50), return `[pushed, heapified, three_pops, top_three_desc]` where `pushed` is the list you get after calling `heapq.heappush` for each value in order on an empty list, `heapified` is the list `heapq.heapify` produces from a copy of `vals`, `three_pops` is the first (up to) three values `heappop` returns from the `pushed` heap, and `top_three_desc` is the (up to) three largest values in descending order obtained from a max-heap built by pushing negated values. The two layouts are exactly what CPython 3.13's heapq produces. Also state the parent and child index formulas, the cost of heappush, heappop, heapify and peeking `h[0]`, and why the list is not sorted. Example: vals=[5, 3, 8, 1, 9, 2] -> [[1, 3, 2, 5, 9, 8], [1, 3, 2, 5, 9, 8], [1, 2, 3], [9, 8, 5]]; vals=[4, 4, 1] -> [[1, 4, 4], [1, 4, 4], [1, 4, 4], [4, 4, 1]]; vals=[] -> [[], [], [], []]; vals=[9, 8, 7, 6, 5, 4, 3, 2, 1] -> [[1, 2, 4, 3, 7, 8, 5, 9, 6], [1, 2, 3, 6, 5, 4, 7, 8, 9], [1, 2, 3], [9, 8, 7]].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Binary heap on a list. `heapq` gives you a min-heap on a plain Python list; a max-heap is the same thing with negated values.

**Say this first (1 line):** "heapq is a min-heap stored in a list. The root `h[0]` is the smallest, the list is only partly ordered, and for a max-heap I push negatives."

**Brute force:** Keep a sorted list. Insert with `bisect.insort` (O(n) shift) and take the min or max from the ends. Reading is O(1) but every insert is O(n), so n inserts are O(n^2) in the worst case.

**Optimal:**
- Heap rule: every parent is `<=` its children. Nothing is promised between siblings or cousins.
- Index maths for 0-based arrays: parent of `i` is `(i - 1) // 2`; children are `2*i + 1` and `2*i + 2`.
- `heappush`: append at the end, sift up. O(log n).
- `heappop`: take the root, move the last item to the root, sift down. O(log n).
- `heapify`: bottom-up build in place. O(n), not O(n log n), because most nodes are near the leaves and sift only a short way.
- Peek `h[0]`: O(1).
- Why the list is not sorted: the heap only orders along root-to-leaf paths. `[1, 3, 2, 5, 9, 8]` is a valid heap, but 3 sits before 2.
- Pushing one by one and `heapify` can give different valid lists for the same input (see the last example). Both are heaps.
- Max-heap: push `-v`, pop and negate. This works for numbers only; for strings use a wrapper class (see Q8).

**Complexity:** Building by pushes is O(n log n); by `heapify` it is O(n). `k` pops cost O(k log n). Space O(n) for the list (heapify is in place).

**Dry run:** Push 5, 3, 8, 1, 9, 2.
- `[5]`. Push 3: `[5, 3]`, 3 < parent 5, swap: `[3, 5]`.
- Push 8: `[3, 5, 8]`. Push 1: index 3, parent is index 1 (5): swap, then parent index 0 (3): swap: `[1, 3, 8, 5]`.
- Push 9: `[1, 3, 8, 5, 9]`. Push 2: index 5, parent index 2 (8): swap: `[1, 3, 2, 5, 9, 8]`.
- Three pops give 1, 2, 3. Negated pushes, three pops give 9, 8, 5.

**Code:**
```python
import heapq
import random

random.seed(1)

def layouts(vals):
    pushed = []
    for v in vals:
        heapq.heappush(pushed, v)            # O(log n) each: append, then sift up
    heapified = list(vals)
    heapq.heapify(heapified)                 # O(n) total, in place on the copy
    h = list(pushed)
    pops = [heapq.heappop(h) for _ in range(min(3, len(h)))]   # O(log n) each
    neg = []
    for v in vals:
        heapq.heappush(neg, -v)              # max-heap trick: store negatives
    top = [-heapq.heappop(neg) for _ in range(min(3, len(neg)))]
    return [pushed, heapified, pops, top]

def is_heap(a):
    # parent of i is (i-1)//2, children of i are 2i+1 and 2i+2
    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))

def brute(vals):
    """Independent check: only properties, since the layout itself is CPython's."""
    pushed, heapified, pops, top = layouts(vals)
    assert is_heap(pushed) and is_heap(heapified)
    assert sorted(pushed) == sorted(vals) == sorted(heapified)
    assert pops == sorted(vals)[:3]
    assert top == sorted(vals, reverse=True)[:3]
    return True

# the four examples from the prompt (layouts are exactly CPython 3.13's)
assert layouts([5, 3, 8, 1, 9, 2]) == [[1, 3, 2, 5, 9, 8], [1, 3, 2, 5, 9, 8], [1, 2, 3], [9, 8, 5]]
assert layouts([4, 4, 1]) == [[1, 4, 4], [1, 4, 4], [1, 4, 4], [4, 4, 1]]
assert layouts([]) == [[], [], [], []]
assert layouts([9, 8, 7, 6, 5, 4, 3, 2, 1]) == [[1, 2, 4, 3, 7, 8, 5, 9, 6], [1, 2, 3, 6, 5, 4, 7, 8, 9], [1, 2, 3], [9, 8, 7]]

# push-built and heapify-built layouts differ on the last example: both are valid heaps
a = layouts([9, 8, 7, 6, 5, 4, 3, 2, 1])
print('push layout    ', a[0])
print('heapify layout ', a[1])
print('same heap, different lists:', a[0] != a[1], '| both valid:', is_heap(a[0]) and is_heap(a[1]))

# the list is NOT sorted: only parent <= child holds
h = [1, 3, 2, 5, 9, 8]
print('h[0] is the min:', h[0], '| sorted?', h == sorted(h), '| 3 comes before 2 in the list')

# randomised cross-check, 600 seeded lists of size 0..50
for _ in range(600):
    vals = [random.randint(-20, 20) for _ in range(random.randint(0, 50))]
    brute(vals)
print('600 random lists ok')

# ties: tuples compare element by element, so a tie falls through to the next field
h = []
heapq.heappush(h, (1, 'b'))
heapq.heappush(h, (1, 'a'))
print('tie on priority broken by the 2nd field:', heapq.heappop(h))
h = []
heapq.heappush(h, (1, {'x': 1}))
try:
    heapq.heappush(h, (1, {'y': 2}))         # tie on 1, then dict < dict
except TypeError as e:
    print('TypeError on tie with unorderable payload:', e)

# max-heap trick edge: negation works for ints, not for strings
try:
    heapq.heappush([], -'abc')
except TypeError as e:
    print('cannot negate a str:', e)
print('done')
```

**Output (my run):**
```
push layout     [1, 2, 4, 3, 7, 8, 5, 9, 6]
heapify layout  [1, 2, 3, 6, 5, 4, 7, 8, 9]
same heap, different lists: True | both valid: True
h[0] is the min: 1 | sorted? False | 3 comes before 2 in the list
600 random lists ok
tie on priority broken by the 2nd field: (1, 'a')
TypeError on tie with unorderable payload: '<' not supported between instances of 'dict' and 'dict'
cannot negate a str: bad operand type for unary -: 'str'
done
```

**Edge cases:**
- Empty input: every output is `[]`, and `heappop` on an empty list raises `IndexError`.
- Duplicates: `[4, 4, 1]` is fine, nothing needs to be unique.
- Fewer than three elements: pop only `min(3, len)` times.
- Ties in tuples fall through to the next field; an unorderable second field raises `TypeError`.

**Follow-ups:**
- *Why is heapify O(n)?* Half the nodes are leaves and need no work; a quarter sift at most 1 level, and so on. The sum of heights is below n.
- *How do I peek the max in a max-heap?* `-h[0]`.
- *Is there `heappush` with a key?* No. Push tuples `(key, tiebreak, item)`.

**Common mistakes:**
- Calling `sorted(h)` and thinking the list is already sorted, or reading `h[1]` as the second smallest (it may be `h[2]`).
- Treating `heapq.heapify(h)` as returning something. It returns `None` and works in place.
- Using `h.pop(0)` or `min(h)` instead of `heappop`.
- Forgetting to negate back when popping from a negated max-heap.

### Q2 ⭐⭐⭐ 🟢 Kth largest element in a stream. Build a class `KthLargest(k, nums)` with `add(val)` that adds a value and returns the k-th largest value among all values seen so far (counting duplicates; the 1st largest is the maximum). Constraints: 1 <= k <= 10^4, 0 <= len(nums) <= 10^4, up to 10^4 calls to add, and len(nums) + 1 >= k so an answer always exists after the first add. Keep a min-heap of size k: say why its root is the answer, what each add costs (O(log k)), and why a max-heap of everything would be the wrong tool. The example gives the constructor arguments and the list of added values, and the expected output is the list of values add returns. Example: k=3, nums=[4, 5, 8, 2], adds=[3, 5, 10, 9, 4] -> [4, 5, 5, 8, 8]; k=1, nums=[], adds=[-3, -2, -4, 0] -> [-3, -2, -2, 0]; k=2, nums=[0], adds=[-1, 1, -2, -4, 3] -> [-1, 0, 0, 0, 1].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Top-k with a size-k min-heap. The heap keeps the k largest values; its root is the smallest of those, which is the k-th largest overall.

**Say this first (1 line):** "I keep a min-heap of the k largest values seen. The root is the k-th largest. A new value only matters if it beats the root."

**Brute force:** Keep a list, append each value, sort, and read index `-k`. That is O(n log n) per add. Better: `insort`, still O(n) per add.

**Optimal:**
- Constructor: heapify `nums`, pop until only `k` remain (or push directly with the same rule).
- `add(val)`: if the heap has fewer than k items, push. Else if `val > h[0]`, `heapreplace` (pop the root and push `val` in one sift). Otherwise ignore it.
- Return `h[0]`.
- Invariant: the heap always holds the k largest values seen so far (with duplicates). Anything smaller than the root can never become the k-th largest later, because values only get added, never removed.
- Why the constraint `len(nums) + 1 >= k`: after the first add the heap has k items, so `h[0]` is a real k-th largest.
- Why not a max-heap of everything: the k-th largest needs k pops per query, and the pops destroy the heap.

**Complexity:** Each add is O(log k). Construction is O(n) for heapify plus O((n - k) log n) to trim (or O(n log k) by streaming). Space O(k) after trimming.

**Dry run:** k=3, nums=[4, 5, 8, 2]. Heap after trim: `[4, 5, 8]`.
- add 3: 3 < 4, ignore, answer 4.
- add 5: 5 > 4, replace: `[5, 5, 8]`, answer 5.
- add 10: replace: `[5, 8, 10]`, answer 5.
- add 9: replace: `[8, 9, 10]`, answer 8.
- add 4: ignore, answer 8. Output `[4, 5, 5, 8, 8]`.

**Code:**
```python
import heapq
import random

random.seed(2)

class KthLargest:
    """Min-heap holding the k largest values seen so far; its root is the k-th largest."""
    def __init__(self, k, nums):
        self.k = k
        self.h = list(nums)
        heapq.heapify(self.h)                    # O(n)
        while len(self.h) > k:
            heapq.heappop(self.h)                # keep only the k largest

    def add(self, val):
        if len(self.h) < self.k:
            heapq.heappush(self.h, val)          # heap not full yet
        elif val > self.h[0]:
            heapq.heapreplace(self.h, val)       # pop the root, push val: one sift, O(log k)
        return self.h[0]                         # k-th largest (valid once len == k)

class KthLargestBrute:
    def __init__(self, k, nums):
        self.k, self.a = k, list(nums)
    def add(self, val):
        self.a.append(val)
        return sorted(self.a, reverse=True)[self.k - 1]   # O(n log n) per add

def run(cls, k, nums, adds):
    obj = cls(k, nums)
    return [obj.add(v) for v in adds]

assert run(KthLargest, 3, [4, 5, 8, 2], [3, 5, 10, 9, 4]) == [4, 5, 5, 8, 8]
assert run(KthLargest, 1, [], [-3, -2, -4, 0]) == [-3, -2, -2, 0]
assert run(KthLargest, 2, [0], [-1, 1, -2, -4, 3]) == [-1, 0, 0, 0, 1]

# randomised cross-check, honouring len(nums) + 1 >= k
for _ in range(500):
    n = random.randint(0, 8)
    k = random.randint(1, n + 1)
    nums = [random.randint(-5, 5) for _ in range(n)]
    adds = [random.randint(-5, 5) for _ in range(random.randint(1, 12))]
    assert run(KthLargest, k, nums, adds) == run(KthLargestBrute, k, nums, adds)
print('500 random streams ok')

# heap size never exceeds k, and k == len(nums)+1 is the tightest legal case
obj = KthLargest(4, [1, 2, 3])
assert obj.add(0) == 0 and len(obj.h) == 4       # first add fills the heap
assert obj.add(10) == 1 and len(obj.h) == 4
# duplicates count separately
assert run(KthLargest, 2, [5, 5], [5]) == [5]
# k larger than len(nums)+1 is outside the constraint: the root is then NOT the k-th largest
bad = KthLargest(5, [1])
print('outside the constraint, add(2) returns', bad.add(2), '(only 2 values exist, so no 5th largest)')

# why not a max-heap of everything: finding the k-th needs k pops each time
mx = [-x for x in [4, 5, 8, 2, 3]]
heapq.heapify(mx)
tmp = [heapq.heappop(mx) for _ in range(3)]
print('3rd largest via max-heap of all:', -tmp[-1], '(cost k log n per query, and it destroys the heap)')
print('size-k min-heap root:', run(KthLargest, 3, [4, 5, 8, 2], [3])[0], '(O(log k) per add)')
```

**Output (my run):**
```
500 random streams ok
outside the constraint, add(2) returns 1 (only 2 values exist, so no 5th largest)
3rd largest via max-heap of all: 4 (cost k log n per query, and it destroys the heap)
size-k min-heap root: 4 (O(log k) per add)
```

**Edge cases:**
- `k = 1`: the heap holds just the maximum.
- `nums` empty with `k = 1`: the first add fills the heap.
- Duplicates count separately: `k=2, nums=[5, 5], add(5)` returns 5.
- `k` too big (outside the constraint): the root is not a k-th largest, so the class must not be used there.

**Follow-ups:**
- *What if values can be deleted?* A heap cannot find an arbitrary value. Use a sorted container, or lazy deletion with a counter (the lazy-deletion idea appears in Part 4 Q38).
- *What if k changes?* Rebuild or grow: raising k means keeping more values than you saved, so you need to have kept everything.
- *Smallest k-th instead?* Use a max-heap of size k with negated values.

**Common mistakes:**
- Using a max-heap of everything. That is O(n) memory and O(k log n) per query.
- Pushing every value and never trimming, so the heap grows to n and its root is the minimum of everything, not the k-th largest.
- Returning `h[0]` before the heap has k items.
- Comparing with `>=` and replacing equal values: harmless but wasteful.

### Q3 ⭐⭐⭐ 🟢 Can one person attend all meetings. Intervals are lists [start, end] of integers with start < end; unless a question says otherwise they are half-open [start, end), so a meeting ending at 5 does not clash with one starting at 5. Given `intervals` (0 <= len <= 10^4, 0 <= start < end <= 10^6), return True when no two meetings overlap. Sort by start time and compare neighbours; say why comparing only neighbours is enough after sorting, what the cost is, and why the pairwise O(n^2) check is the brute force. Example: intervals=[[0, 30], [5, 10], [15, 20]] -> False; intervals=[[7, 10], [2, 4]] -> True; intervals=[[1, 5], [5, 8]] -> True; intervals=[] -> True.
**Asked at:** Interval pattern guides on techinterview.org (merge, insert, meeting rooms, employee free time, interval scheduling; search snippets only, not opened; the site's own 'asked at' lists were not verified) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval sweep after sorting by start. Sorting turns "any two clash" into "some neighbouring pair clashes".

**Say this first (1 line):** "Sort by start. If any meeting starts before the previous one ends, there is a clash. Touching at one time is fine because the intervals are half-open."

**Brute force:** Check all pairs: `a.start < b.end and b.start < a.end`. O(n^2) time, O(1) space. With n = 10^4 that is 5 * 10^7 pair checks, too slow in Python.

**Optimal:**
- Sort by start (ties by end, which `sorted` does for lists).
- Scan: if `iv[i].end > iv[i+1].start`, return False.
- Why neighbours are enough: suppose some pair `(i, j)` with `i < j` clashes, so `start[j] < end[i]`. Then `start[i+1] <= start[j] < end[i]`, so the pair `(i, i+1)` already clashes. A clash anywhere implies a neighbour clash.
- Half-open rule: `end == start` is allowed, so the test is strict `>` for a clash (`<=` for OK).

**Complexity:** Time O(n log n) for the sort, O(n) for the scan. Space O(n) for the sorted copy (O(1) extra if sorting in place is allowed).

**Dry run:** `[[0, 30], [5, 10], [15, 20]]` sorted is the same. Pair `[0, 30], [5, 10]`: 30 > 5, clash, return False. For `[[7, 10], [2, 4]]`: sorted `[[2, 4], [7, 10]]`, 4 <= 7 fine, True. For `[[1, 5], [5, 8]]`: 5 <= 5 fine, True.

**Code:**
```python
import random
from itertools import combinations

random.seed(3)

def can_attend(intervals):
    iv = sorted(intervals)                       # by start (then end)
    return all(iv[i][1] <= iv[i + 1][0] for i in range(len(iv) - 1))

def can_attend_brute(intervals):
    # half-open [s, e): two meetings clash when each starts before the other ends
    return not any(a[0] < b[1] and b[0] < a[1] for a, b in combinations(intervals, 2))

assert can_attend([[0, 30], [5, 10], [15, 20]]) is False
assert can_attend([[7, 10], [2, 4]]) is True
assert can_attend([[1, 5], [5, 8]]) is True      # touching is fine for half-open
assert can_attend([]) is True
assert can_attend([[3, 4]]) is True
assert can_attend([[1, 4], [1, 4]]) is False     # duplicates clash
assert can_attend([[1, 10], [2, 3], [11, 12]]) is False   # sorted neighbours [1,10],[2,3] clash

for _ in range(3000):
    n = random.randint(0, 7)
    iv = []
    for _ in range(n):
        s = random.randint(0, 10)
        iv.append([s, random.randint(s + 1, 11)])
    assert can_attend(iv) == can_attend_brute(iv), iv
print('3000 random cases ok')

# why neighbours suffice: after sorting by start, if the meeting after i starts before end[i] we already clash;
# if no neighbour clashes then end[i] <= start[i+1] <= start[j] for every j > i, so ends are ordered too.
iv = sorted([[1, 4], [2, 3], [6, 7]])
print('sorted:', iv, '-> neighbour pair [1,4],[2,3] clashes:', iv[0][1] > iv[1][0])
# a classic bug: comparing with strict < treats touching meetings as clashes
wrong = lambda ivs: all(sorted(ivs)[i][1] < sorted(ivs)[i + 1][0] for i in range(len(ivs) - 1))
print('wrong strict check on [[1,5],[5,8]]:', wrong([[1, 5], [5, 8]]), '(should be True)')
```

**Output (my run):**
```
3000 random cases ok
sorted: [[1, 4], [2, 3], [6, 7]] -> neighbour pair [1,4],[2,3] clashes: True
wrong strict check on [[1,5],[5,8]]: False (should be True)
```

**Edge cases:**
- Empty list or one meeting: True.
- Duplicate meetings clash.
- Touching meetings (`end == next start`) do not clash here.
- One long meeting containing others: caught by the first neighbour pair after sorting.

**Follow-ups:**
- *Return the clashing pair?* Return `iv[i], iv[i+1]` at the first failure.
- *How many rooms do I need?* That is Q7.
- *Closed intervals?* Use `>=` for a clash.

**Common mistakes:**
- Strict `<` in the OK test, which wrongly rejects touching meetings.
- Not sorting, or sorting by end and comparing the wrong fields.
- Thinking you must compare each meeting with all later ones after sorting. You do not (proof above).

### Q4 ⭐⭐⭐ 🟡 Kth largest element in an array. Given integers `nums` (1 <= len <= 10^5, values in [-10^9, 10^9], duplicates allowed) and 1 <= k <= len, return the k-th largest value in sorted order, so in [3, 2, 2, 1] the 2nd and 3rd largest are both 2. Give three solutions and compare them: sort (O(n log n)), a min-heap of size k (O(n log k) time, O(k) space) and quickselect (expected O(n), worst O(n^2) with a bad pivot, and it rearranges the input). Say when each one wins: k small and data streaming, k close to n, input may be modified, worst-case guarantee needed. Example: nums=[3, 2, 1, 5, 6, 4], k=2 -> 5; nums=[3, 2, 3, 1, 2, 4, 5, 5, 6], k=4 -> 4; nums=[7], k=1 -> 7; nums=[2, 2, 2], k=3 -> 2.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Candidate-reported rounds on Naukri Code360 (a Flipkart August 2022 write-up with merge intervals, an Amazon August 2021 online round with merge intervals, a Flipkart May 2021 SDE-1 online test with merge k sorted arrays; snippets only, not opened; self-reported, unverified) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Selection (top-k). Three tools: full sort, size-k heap, quickselect. The pattern is "I only need one order statistic, not the whole order".

**Say this first (1 line):** "Sorting is the safe answer at O(n log n). A size-k min-heap gives O(n log k) and works on streams. Quickselect gives expected O(n) but rearranges the array and has an O(n^2) worst case."

**Brute force:** `sorted(nums, reverse=True)[k - 1]`. O(n log n) time, O(n) space for the copy (or O(1) extra with an in-place sort).

**Optimal:**
- Heap: keep a min-heap of the k largest. Push until it has k, then `heapreplace` when a value beats the root. The root is the answer. O(n log k) time, O(k) space.
- Quickselect: pick a pivot, split into greater / equal / smaller (three-way), then continue in the one part that contains index `k - 1`. Expected O(n); a random pivot makes the bad case unlikely, a fixed pivot on sorted input gives O(n^2).
- Three-way split matters for duplicates: an all-equal input falls in the "equal" block at once, so no deep recursion and no O(n^2).
- When each wins:

| Situation | Pick |
|---|---|
| Streaming data, k small | size-k heap |
| k close to n | sort, or a heap of size n - k + 1 on the other side |
| Input may be modified, one-shot, large n | quickselect |
| Worst-case guarantee needed | heap or sort (or median-of-medians, which is complex) |
| Need the full top-k list too | `heapq.nlargest` |

**Complexity:** Sort O(n log n). Heap O(n log k) time, O(k) space. Quickselect expected O(n), worst O(n^2), O(n) space for the copy (O(1) if you may modify the input). Reasoning for quickselect: each round does a linear pass and, with a random pivot, the expected remaining size shrinks by a constant factor, so the passes add up to about a constant times n.

**Dry run:** `[3, 2, 1, 5, 6, 4]`, k=2. Heap of size 2: push 3, 2 -> `[2, 3]`. 1 < 2 skip. 5 > 2: replace -> `[3, 5]`. 6 > 3: replace -> `[5, 6]`. 4 < 5 skip. Root is 5. Correct: sorted descending is 6, 5, 4, ...

**Code:**
```python
import heapq
import random

random.seed(4)

def kth_sort(nums, k):
    return sorted(nums, reverse=True)[k - 1]            # O(n log n), O(n) copy

def kth_heap(nums, k):
    h = []                                              # min-heap of the k largest so far
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heapreplace(h, x)                     # O(log k)
    return h[0]                                         # O(n log k) time, O(k) space

def kth_quickselect(nums, k, rng=random):
    """Iterative three-way quickselect on a COPY. Expected O(n), worst O(n^2)."""
    a = list(nums)
    target = k - 1                                      # index in descending order
    lo, hi = 0, len(a) - 1
    while True:
        pivot = a[rng.randint(lo, hi)]                  # random pivot defeats sorted inputs
        # Dutch flag, descending: [lo..lt) > pivot, [lt..i) == pivot, (gt..hi] < pivot
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if a[i] > pivot:
                a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] < pivot:
                a[i], a[gt] = a[gt], a[i]; gt -= 1
            else:
                i += 1
        if target < lt:
            hi = lt - 1
        elif target > gt:
            lo = gt + 1
        else:
            return pivot                                # target falls in the == block

def kth_nlargest(nums, k):
    return heapq.nlargest(k, nums)[-1]                  # same size-k heap idea, in C

for fn in (kth_sort, kth_heap, kth_quickselect, kth_nlargest):
    assert fn([3, 2, 1, 5, 6, 4], 2) == 5
    assert fn([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert fn([7], 1) == 7
    assert fn([2, 2, 2], 3) == 2
    assert fn([3, 2, 2, 1], 2) == 2 and fn([3, 2, 2, 1], 3) == 2   # duplicates count
    assert fn([-5, -1, -3], 3) == -5

# randomised cross-check including heavy duplicates
for _ in range(1500):
    n = random.randint(1, 12)
    hi = random.choice([2, 5, 50])
    nums = [random.randint(-hi, hi) for _ in range(n)]
    k = random.randint(1, n)
    want = kth_sort(nums, k)
    snapshot = list(nums)
    assert kth_heap(nums, k) == want == kth_quickselect(nums, k) == kth_nlargest(nums, k)
    assert nums == snapshot                              # none of them modifies the input
print('1500 random cases ok (input never modified)')

# large: all equal and already sorted inputs (quickselect with a bad fixed pivot would be O(n^2))
big = [7] * 100000
assert kth_quickselect(big, 50000) == 7
srt = list(range(100000))
assert kth_quickselect(srt, 1) == 99999 and kth_quickselect(srt, 100000) == 0
assert kth_heap(srt, 10) == 99990
print('n = 10^5 all-equal and sorted inputs ok')

# comparison counts: how many elements does the heap actually replace?
rnd = random.sample(range(10**6), 10**5)
h, repl = [], 0
for x in rnd:
    if len(h) < 10: heapq.heappush(h, x)
    elif x > h[0]: heapq.heapreplace(h, x); repl += 1
print('random order, k=10: heap replacements =', repl, 'of', len(rnd), '(sorted ascending input would replace every one)')
```

**Output (my run):**
```
1500 random cases ok (input never modified)
n = 10^5 all-equal and sorted inputs ok
random order, k=10: heap replacements = 85 of 100000 (sorted ascending input would replace every one)
```

**Edge cases:**
- `k = 1` (maximum) and `k = n` (minimum).
- All equal values: quickselect must use a three-way split.
- Duplicates count: in `[3, 2, 2, 1]` the 2nd and 3rd largest are both 2.
- Negative values and the input is not modified by the code above (quickselect works on a copy).

**Follow-ups:**
- *Why is the heap faster than sort for small k?* It touches a log k-sized heap, and most elements fail the `x > h[0]` test and cost O(1). Random order replaces only about k ln(n/k) elements, so the heap rarely moves.
- *Worst-case O(n)?* Median of medians, which is rarely worth it in interviews.
- *Kth smallest?* Use `k' = n - k + 1`, or flip the heap direction.

**Common mistakes:**
- Using a max-heap of size n: O(n log n) and no better than sorting.
- Quickselect with a two-way split and many duplicates (slow or infinite loops).
- Off-by-one: index `k - 1` in descending order, or `len - k` in ascending order.
- Deduplicating: "k-th distinct largest" is a different question.

### Q5 ⭐⭐⭐ 🟡 Merge intervals. This question uses CLOSED intervals [start, end] with start <= end, so [1, 4] and [4, 5] touch at 4 and must be merged. Given an unsorted list `intervals` (1 <= len <= 10^4, 0 <= start <= end <= 10^6), return the minimal list of disjoint closed intervals covering exactly the same points, sorted by start. Sort by start, then fold each interval into the last merged one when its start is <= the last end, taking the max of the two ends (explain why a contained interval must not shrink the end). State the complexity (O(n log n), dominated by the sort). Example: intervals=[[1, 3], [2, 6], [8, 10], [15, 18]] -> [[1, 6], [8, 10], [15, 18]]; intervals=[[1, 4], [4, 5]] -> [[1, 5]]; intervals=[[1, 4], [0, 4]] -> [[0, 4]]; intervals=[[1, 10], [2, 3], [4, 5]] -> [[1, 10]]; intervals=[[3, 3]] -> [[3, 3]].
**Asked at:** Interval pattern guides on techinterview.org (merge, insert, meeting rooms, employee free time, interval scheduling; search snippets only, not opened; the site's own 'asked at' lists were not verified) | Candidate-reported rounds on Naukri Code360 (a Flipkart August 2022 write-up with merge intervals, an Amazon August 2021 online round with merge intervals, a Flipkart May 2021 SDE-1 online test with merge k sorted arrays; snippets only, not opened; self-reported, unverified) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Sort by start, then fold. A single pass keeps one "current" merged interval.

**Say this first (1 line):** "Sort by start. If the next interval starts at or before the current end, merge them and take the max end. Otherwise start a new one."

**Brute force:** Repeatedly look for any pair that overlaps, merge it, and restart until none do. O(n^2) or worse per pass. Another brute force (used in the code to check) marks every covered point on a grid and reads off runs, which only works for tiny coordinates.

**Optimal:**
- Sort by start.
- Walk the list with `out` as the answer so far. If `out` is non-empty and `s <= out[-1][1]` (closed intervals, so touching counts), set `out[-1][1] = max(out[-1][1], e)`. Otherwise append `[s, e]`.
- Why `max`: a contained interval like `[2, 3]` inside `[1, 10]` has a smaller end. Overwriting would shrink the merged interval.
- Invariant: after processing the first i intervals (sorted), `out` is the minimal disjoint cover of them, and the last interval has the largest start so far.
- Closed intervals: `[1, 4]` and `[4, 5]` share the point 4, so they merge. `[1, 4]` and `[5, 6]` do not (integer 4 and 5 are different points, as the code's grid check confirms).

**Complexity:** O(n log n) for the sort, O(n) for the fold. Space O(n) for the output.

**Dry run:** `[[1, 3], [2, 6], [8, 10], [15, 18]]` is sorted. Start `[[1, 3]]`. `[2, 6]`: 2 <= 3, end becomes max(3, 6) = 6. `[8, 10]`: 8 > 6, append. `[15, 18]`: 15 > 10, append. Result `[[1, 6], [8, 10], [15, 18]]`. For `[[1, 10], [2, 3], [4, 5]]`: 2 <= 10, max(10, 3) = 10; 4 <= 10, max(10, 5) = 10. One interval.

**Code:**
```python
import random

random.seed(5)

def merge(intervals):
    out = []
    for s, e in sorted(intervals):                      # by start, then end
        if out and s <= out[-1][1]:                     # closed: touching (s == last end) merges
            out[-1][1] = max(out[-1][1], e)             # max, so a contained interval cannot shrink it
        else:
            out.append([s, e])                          # fresh list: caller's input is untouched
    return out

def merge_buggy(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = e                              # BUG: overwrites with e even when e is smaller
        else:
            out.append([s, e])
    return out

def merge_brute(intervals):
    """Mark every covered point on a doubled grid (so the gap between 4 and 5 is visible), then read runs."""
    pts = set()
    for s, e in intervals:
        pts.update(range(2 * s, 2 * e + 1))
    out, cur = [], None
    for p in sorted(pts):
        if cur and p == cur[1] + 1:
            cur[1] = p
        else:
            if cur: out.append(cur)
            cur = [p, p]
    if cur: out.append(cur)
    return [[a // 2, b // 2] for a, b in out]

assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
assert merge([[1, 4], [4, 5]]) == [[1, 5]]
assert merge([[1, 4], [0, 4]]) == [[0, 4]]
assert merge([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]
assert merge([[3, 3]]) == [[3, 3]]
assert merge([[1, 4], [5, 6]]) == [[1, 4], [5, 6]]   # integers 4 and 5 are different points: NOT merged

for _ in range(3000):
    n = random.randint(1, 7)
    iv = []
    for _ in range(n):
        s = random.randint(0, 12)
        iv.append([s, random.randint(s, 12)])
    snap = [list(x) for x in iv]
    assert merge(iv) == merge_brute(iv), iv
    assert iv == snap                                   # input untouched
print('3000 random cases ok')

print('buggy on [[1,10],[2,3],[4,5]]:', merge_buggy([[1, 10], [2, 3], [4, 5]]), '(shrunk the end, wrong)')
# sort key note: sorted() on lists compares start then end; duplicates and ties are fine
print('merge of 3 equal points:', merge([[2, 2], [2, 2], [2, 2]]))
# a sorted() on tuples of mixed types would raise TypeError; ints only here
try:
    sorted([[1, 'a'], [1, 2]])
except TypeError as e:
    print('TypeError on tied start with mixed ends:', e)
```

**Output (my run):**
```
3000 random cases ok
buggy on [[1,10],[2,3],[4,5]]: [[1, 3], [4, 5]] (shrunk the end, wrong)
merge of 3 equal points: [[2, 2]]
TypeError on tied start with mixed ends: '<' not supported between instances of 'int' and 'str'
```

**Edge cases:**
- Single interval, including a point `[3, 3]`.
- Touching (closed): merge. Contained: keep the larger end.
- Identical duplicates collapse to one.
- Unsorted input: sorting is the whole trick. Sorting does not modify the intervals themselves, but the code builds fresh lists so the caller's data is untouched.

**Follow-ups:**
- *Half-open intervals?* Use `s < out[-1][1]` instead of `<=`.
- *Already sorted?* Skip the sort, O(n).
- *Insert one interval?* Q6.

**Common mistakes:**
- `out[-1][1] = e` instead of `max`.
- Sorting by end instead of by start.
- Mutating the caller's interval lists by appending the original object to `out`.
- Using `<` for closed intervals and missing the touching merge.

### Q6 ⭐⭐⭐ 🟡 Insert interval. This question uses CLOSED intervals [start, end] with start <= end, where touching intervals count as overlapping. `intervals` is already sorted by start and pairwise disjoint (0 <= len <= 10^4), and `new` is one more interval. Return the sorted disjoint list after inserting `new` and merging everything it overlaps or touches. Do it in one O(n) pass in three phases (copy the intervals that end before `new` starts, merge the overlapping ones into `new`, copy the rest) without re-sorting, and say why the binary-search variant still costs O(n) in a Python list. Example: intervals=[[1, 3], [6, 9]], new=[2, 5] -> [[1, 5], [6, 9]]; intervals=[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], new=[4, 8] -> [[1, 2], [3, 10], [12, 16]]; intervals=[], new=[5, 7] -> [[5, 7]]; intervals=[[1, 5]], new=[6, 8] -> [[1, 5], [6, 8]]; intervals=[[1, 5]], new=[5, 6] -> [[1, 6]].
**Asked at:** Interval pattern guides on techinterview.org (merge, insert, meeting rooms, employee free time, interval scheduling; search snippets only, not opened; the site's own 'asked at' lists were not verified) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Three-phase linear scan over sorted disjoint intervals: before, overlapping, after.

**Say this first (1 line):** "The list is already sorted and disjoint, so I never re-sort. I copy everything that ends before the new interval, merge everything that overlaps it, and copy the rest."

**Brute force:** Append `new` and run the merge-intervals algorithm from Q5: O(n log n) because of the sort. It works but ignores the sorted input.

**Optimal:**
- Phase 1: while `intervals[i].end < new.start`, copy (strictly before; touching is NOT before).
- Phase 2: while `intervals[i].start <= new.end`, widen `new` to `min(starts)` and `max(ends)`.
- Append the merged `new`, then phase 3: copy the rest.
- Invariant: after phase 1 every copied interval is entirely left of `new`; after phase 2 nothing remaining can touch the merged `new` because the next start is `> new.end` and the list is sorted and disjoint.
- Binary search can find where phase 1 ends and phase 3 begins in O(log n) (`bisect_left` on ends, `bisect_right` on starts), but building a new list from slices copies O(n) items, and inserting into a Python list shifts O(n) items. So the total is still O(n); the code shows this variant and it matches.

**Complexity:** O(n) time, O(n) space for the output.

**Dry run:** `[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]`, new `[4, 8]`. Phase 1: `[1, 2]` ends at 2 < 4, copy. `[3, 5]`: 5 < 4? No, stop. Phase 2: `[3, 5]` starts 3 <= 8, new = [3, 8]. `[6, 7]`: 6 <= 8, new = [3, 8]. `[8, 10]`: 8 <= 8, new = [3, 10]. `[12, 16]`: 12 > 10 stop. Output `[[1, 2], [3, 10], [12, 16]]`.

**Code:**
```python
import random
from bisect import bisect_left, bisect_right

random.seed(6)

def insert_interval(intervals, new):
    out, i, n = [], 0, len(intervals)
    s, e = new
    while i < n and intervals[i][1] < s:                # phase 1: strictly before new (touching is NOT before)
        out.append(list(intervals[i])); i += 1
    while i < n and intervals[i][0] <= e:               # phase 2: overlaps or touches new
        s = min(s, intervals[i][0]); e = max(e, intervals[i][1]); i += 1
    out.append([s, e])
    while i < n:                                        # phase 3: strictly after
        out.append(list(intervals[i])); i += 1
    return out

def insert_bisect(intervals, new):
    """Binary search finds the window in O(log n), but the slice copies are still O(n)."""
    starts = [x[0] for x in intervals]                  # O(n) to build; a persistent list would avoid it
    ends = [x[1] for x in intervals]
    lo = bisect_left(ends, new[0])                      # first interval whose end >= new start
    hi = bisect_right(starts, new[1])                   # first interval whose start > new end
    s, e = new
    if lo < hi:
        s, e = min(s, intervals[lo][0]), max(e, intervals[hi - 1][1])
    return [list(x) for x in intervals[:lo]] + [[s, e]] + [list(x) for x in intervals[hi:]]

def brute(intervals, new):
    pts = set()
    for s, e in list(intervals) + [new]:
        pts.update(range(2 * s, 2 * e + 1))
    out, cur = [], None
    for p in sorted(pts):
        if cur and p == cur[1] + 1: cur[1] = p
        else:
            if cur: out.append(cur)
            cur = [p, p]
    if cur: out.append(cur)
    return [[a // 2, b // 2] for a, b in out]

for fn in (insert_interval, insert_bisect):
    assert fn([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert fn([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
    assert fn([], [5, 7]) == [[5, 7]]
    assert fn([[1, 5]], [6, 8]) == [[1, 5], [6, 8]]
    assert fn([[1, 5]], [5, 6]) == [[1, 6]]
    assert fn([[1, 5]], [0, 0]) == [[0, 0], [1, 5]]           # new before everything
    assert fn([[1, 5], [7, 8]], [0, 20]) == [[0, 20]]         # swallows everything

def random_disjoint(rng):
    out, x = [], rng.randint(0, 2)
    for _ in range(rng.randint(0, 5)):
        s = x; e = s + rng.randint(0, 3)
        out.append([s, e]); x = e + rng.randint(1, 3)         # gap >= 1: disjoint closed intervals do not touch
    return out

for _ in range(3000):
    iv = random_disjoint(random)
    s = random.randint(0, 20); new = [s, random.randint(s, 21)]
    want = brute(iv, new)
    assert insert_interval(iv, new) == want == insert_bisect(iv, new), (iv, new)
print('3000 random cases ok')

# the common bug: using < instead of <= in phase 2 misses a touching interval
def buggy(intervals, new):
    out, i, n = [], 0, len(intervals); s, e = new
    while i < n and intervals[i][1] < s: out.append(intervals[i]); i += 1
    while i < n and intervals[i][0] < e: s = min(s, intervals[i][0]); e = max(e, intervals[i][1]); i += 1
    out.append([s, e]); out += intervals[i:]
    return out
print('buggy (< not <=) on [[6,7]] + [5,6]:', buggy([[6, 7]], [5, 6]), '(should be [[5, 7]])')
```

**Output (my run):**
```
3000 random cases ok
buggy (< not <=) on [[6,7]] + [5,6]: [[5, 6], [6, 7]] (should be [[5, 7]])
```

**Edge cases:**
- Empty list: return `[new]`.
- `new` entirely before or entirely after everything.
- `new` swallows every interval.
- Touching at an endpoint merges (closed intervals); that is why phase 1 uses `<` and phase 2 uses `<=`.

**Follow-ups:**
- *Can it be O(log n)?* Only with a structure that supports inserting and deleting ranges in O(log n), such as a balanced tree. A Python list cannot.
- *Half-open intervals?* Phase 1 uses `<=`, phase 2 uses `<`.
- *Remove an interval?* Same three phases, with splitting.

**Common mistakes:**
- `<` in phase 2, which misses an interval that starts exactly at `new.end` (the code prints a failing case).
- Forgetting `min` on the start of `new`.
- Re-sorting the whole list.
- Appending the original inner lists and sharing them with the caller.

### Q7 ⭐⭐⭐ 🟡 Meeting rooms II (minimum number of rooms). Intervals are lists [start, end] of integers with start < end; unless a question says otherwise they are half-open [start, end), so a meeting ending at 5 does not clash with one starting at 5. Given `intervals` (0 <= len <= 10^5, 0 <= start < end <= 10^9), return the minimum number of rooms needed so that no two overlapping meetings share a room (0 when there are no meetings). Solve it with a min-heap of end times after sorting by start (reuse a room when the earliest end is <= the new start, which is the half-open rule), then with a sweep over sorted +1/-1 events, and say which tie order at equal times makes the sweep correct. Example: intervals=[[0, 30], [5, 10], [15, 20]] -> 2; intervals=[[7, 10], [2, 4]] -> 1; intervals=[[1, 5], [5, 8], [8, 9]] -> 1; intervals=[[1, 10], [2, 3], [3, 4], [4, 5]] -> 2; intervals=[] -> 0.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Interval pattern guides on techinterview.org (merge, insert, meeting rooms, employee free time, interval scheduling; search snippets only, not opened; the site's own 'asked at' lists were not verified) | Candidate-reported rounds on Naukri Code360 (a Flipkart August 2022 write-up with merge intervals, an Amazon August 2021 online round with merge intervals, a Flipkart May 2021 SDE-1 online test with merge k sorted arrays; snippets only, not opened; self-reported, unverified) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Min-heap of end times after sorting by start (or a +1/-1 event sweep). Both answer "how many are alive at once".

**Say this first (1 line):** "Sort by start. A min-heap holds the end time of each room in use. If the earliest end is at or before the new start, reuse that room; otherwise open one. The heap size is the answer."

**Brute force:** For every start time, count meetings alive at that time (`s <= t < e`). The maximum overlap is always reached at some start. O(n^2).

**Optimal:**
- Heap version:
- Sort by start.
- For each meeting: if `h[0] <= start`, `heapreplace(h, end)` (same room, new end time); else `heappush(h, end)`.
- Half-open rule: `end == start` means the room is free, so the test is `<=`.
- The heap only grows when every room is busy, and never shrinks, so `len(h)` at the end equals the peak.

- Sweep version:
- Make events `(start, +1)` and `(end, -1)`, sort, keep a running sum, take the maximum.
- Tie order at the same time: the tuple sort puts `-1` before `+1`, so an ending meeting frees its room before the next one starts. Putting starts first would count `[1,5]` and `[5,8]` as 2 rooms (the code shows it).

**Complexity:** Heap: O(n log n) sort plus O(n log n) heap work, O(n) space. Sweep: O(n log n) for sorting 2n events, O(n) space. The heap holds only ints, so ties on end time never compare anything else.

**Dry run:** `[[0, 30], [5, 10], [15, 20]]`. Heap `[30]`. Start 5: 30 > 5, push: `[10, 30]`. Start 15: 10 <= 15, replace: `[20, 30]`. Size 2. For `[[1, 5], [5, 8], [8, 9]]`: heap `[5]`; start 5: 5 <= 5, replace `[8]`; start 8: 8 <= 8, replace `[9]`. Size 1.

**Code:**
```python
import heapq
import random

random.seed(7)

def rooms_heap(intervals):
    h = []                                              # min-heap of end times, one per room in use
    for s, e in sorted(intervals):                      # by start
        if h and h[0] <= s:                             # earliest-ending room is free (half-open: end == start is fine)
            heapq.heapreplace(h, e)                     # reuse it: pop old end, push new end
        else:
            heapq.heappush(h, e)                        # open a new room
    return len(h)                                       # rooms never close, so size = max rooms needed

def rooms_sweep(intervals):
    events = [(s, 1) for s, e in intervals] + [(e, -1) for s, e in intervals]
    events.sort()                                       # at equal time, -1 sorts before +1: ends free rooms first
    cur = best = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best

def rooms_sweep_wrong_order(intervals):
    events = [(s, 1) for s, e in intervals] + [(e, -1) for s, e in intervals]
    events.sort(key=lambda ev: (ev[0], -ev[1]))         # BUG: starts before ends at equal time
    cur = best = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best

def rooms_brute(intervals):
    # max number of meetings alive at any start time (the max overlap is always attained at some start)
    return max((sum(s <= t < e for s, e in intervals) for t in {s for s, e in intervals}), default=0)

for fn in (rooms_heap, rooms_sweep, rooms_brute):
    assert fn([[0, 30], [5, 10], [15, 20]]) == 2
    assert fn([[7, 10], [2, 4]]) == 1
    assert fn([[1, 5], [5, 8], [8, 9]]) == 1
    assert fn([[1, 10], [2, 3], [3, 4], [4, 5]]) == 2
    assert fn([]) == 0
    assert fn([[1, 3], [1, 3], [1, 3]]) == 3            # identical meetings all clash

for _ in range(4000):
    n = random.randint(0, 8)
    iv = []
    for _ in range(n):
        s = random.randint(0, 10)
        iv.append([s, random.randint(s + 1, 11)])
    want = rooms_brute(iv)
    assert rooms_heap(iv) == rooms_sweep(iv) == want, iv
print('4000 random cases ok')

print('wrong tie order on [[1,5],[5,8]]:', rooms_sweep_wrong_order([[1, 5], [5, 8]]), '(should be 1)')
# the heap holds only ints, so ties never compare anything else; if you stored (end, name) a tie would compare names
h = [(5, 'room-a')]
heapq.heappush(h, (5, 'room-b'))
print('heap with (end, name) tuples breaks the tie by name:', heapq.heappop(h))
# size check on 10^5 meetings (sandbox only, timing is not a proof)
big = []
for _ in range(100000):
    s = random.randint(0, 10**9 - 1)
    big.append([s, random.randint(s + 1, min(10**9, s + 10**6))])
print('10^5 meetings, rooms:', rooms_heap(big), '== sweep:', rooms_sweep(big))
```

**Output (my run):**
```
4000 random cases ok
wrong tie order on [[1,5],[5,8]]: 2 (should be 1)
heap with (end, name) tuples breaks the tie by name: (5, 'room-a')
10^5 meetings, rooms: 87 == sweep: 87
```

**Edge cases:**
- Empty list: 0.
- Back-to-back meetings share a room.
- Identical meetings need separate rooms.
- A long meeting containing many short ones: 2 rooms in the example.

**Follow-ups:**
- *Return the assignment?* Store `(end, room_id)` in the heap; ties on end then compare ints, never anything unorderable.
- *Heap or sweep?* Sweep is often easier to explain; the heap extends to "which room".
- *A fixed number of rooms, assign each meeting the lowest free room?* Different problem: it needs a second heap of free room ids.

**Common mistakes:**
- `h[0] < start` instead of `<=`, which wastes a room on touching meetings.
- Sorting events with starts before ends at equal time.
- Not sorting by start before the heap loop.
- Returning the maximum heap size seen but then popping the heap too (the heap never needs popping).

### Q8 ⭐⭐⭐ 🟡 Top K frequent words. Given a list of lowercase `words` (1 <= len <= 10^5) and an integer k (1 <= k <= number of distinct words), return the k most frequent words ordered by frequency descending, and alphabetically ascending among words with equal frequency. The answer is unique under this rule. Use a Counter and a heap (not a full sort) and show the tie-breaking trick: push (-count, word) so the tuple ordering yields count descending and word ascending in one min-heap, which works because the word part is only compared when counts tie. Compare with the integer version in Part 1 Q10 (there any order is accepted and bucket counting gives O(n)); say why bucket counting does not remove the tie-break work here. Example: words=['i', 'love', 'leetcode', 'i', 'love', 'coding'], k=2 -> ['i', 'love']; words=['the', 'day', 'is', 'sunny', 'the', 'the', 'the', 'sunny', 'is', 'is'], k=4 -> ['the', 'is', 'sunny', 'day']; words=['a', 'b', 'c'], k=3 -> ['a', 'b', 'c'].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Count, then heap with a composite key. The tuple `(-count, word)` encodes "count descending, word ascending" in a min-heap.

**Say this first (1 line):** "Counter first. Then a min-heap of `(-count, word)` tuples: tuples compare field by field, so the biggest count comes out first and ties fall to the alphabetically smaller word."

**Brute force:** `sorted(counter, key=lambda w: (-c[w], w))[:k]`. O(d log d) for d distinct words. It is correct and short, and it is the oracle in the code. It does more work than needed when k is much smaller than d.

**Optimal:**
- `Counter(words)`: O(n).
- Build `[(-n, w) for w, n in c.items()]` and `heapify` it: O(d). Pop k times: O(k log d). Total O(n + d + k log d).
- Size-k variant (O(d log k) memory O(k)): keep a min-heap of the k best so far; the root must be the worst kept word. "Worst" means lowest count, and among equal counts the alphabetically LARGER word. A tiny wrapper class with a reversed `__lt__` on the word does it (in the code as `Worse`).
- Why the tuple works: the word is compared only when the counts tie, and words are strings, which are always comparable. Negate the count, never the word (`-'abc'` raises `TypeError`).
- Compare with Part 1 Q10 (integer version): there any order of ties is accepted, so bucket counting (index by count) gives O(n). Here ties must be sorted alphabetically, so within each bucket you still sort the words; bucket counting does not remove that tie-break work.

**Complexity:** Counting O(n) time and O(d) space. Heap-all version O(d + k log d). Size-k version O(d log k) time, O(k) heap space. Sorting version O(d log d).

**Dry run:** `['i', 'love', 'leetcode', 'i', 'love', 'coding']`, k=2. Counts: i 2, love 2, leetcode 1, coding 1. Tuples: `(-2, 'i')`, `(-2, 'love')`, `(-1, 'leetcode')`, `(-1, 'coding')`. Pop 1: `(-2, 'i')` (tie on -2, 'i' < 'love'). Pop 2: `(-2, 'love')`. Answer `['i', 'love']`.

**Code:**
```python
import heapq
import random
from collections import Counter

random.seed(8)

def top_k_heap(words, k):
    c = Counter(words)
    h = [(-n, w) for w, n in c.items()]                 # smaller tuple = better: bigger count, then smaller word
    heapq.heapify(h)                                    # O(d), d = distinct words
    return [heapq.heappop(h)[1] for _ in range(k)]      # k pops, O(k log d)

class Worse:
    """Wrapper so a min-heap of size k keeps the k best: its root is the WORST kept word."""
    __slots__ = ('n', 'w')
    def __init__(self, n, w): self.n, self.w = n, w
    def __lt__(self, other):                            # self is "smaller" (worse) if fewer count, or same count and later word
        return (self.n, other.w) < (other.n, self.w)

def top_k_heap_k(words, k):
    h = []
    for w, n in Counter(words).items():
        item = Worse(n, w)
        if len(h) < k: heapq.heappush(h, item)
        elif h[0] < item: heapq.heapreplace(h, item)    # item beats the worst kept word
    out = [heapq.heappop(h) for _ in range(len(h))]     # worst first
    return [x.w for x in reversed(out)]                 # O(d log k) overall

def top_k_sort(words, k):
    c = Counter(words)
    return sorted(c, key=lambda w: (-c[w], w))[:k]      # the oracle: O(d log d)

for fn in (top_k_heap, top_k_heap_k, top_k_sort):
    assert fn(['i', 'love', 'leetcode', 'i', 'love', 'coding'], 2) == ['i', 'love']
    assert fn(['the', 'day', 'is', 'sunny', 'the', 'the', 'the', 'sunny', 'is', 'is'], 4) == ['the', 'is', 'sunny', 'day']
    assert fn(['a', 'b', 'c'], 3) == ['a', 'b', 'c']
    assert fn(['z'], 1) == ['z']

for _ in range(3000):
    words = [random.choice('abcdef') + random.choice(['', 'x', 'y']) for _ in range(random.randint(1, 25))]
    d = len(set(words)); k = random.randint(1, d)
    want = top_k_sort(words, k)
    assert top_k_heap(words, k) == want == top_k_heap_k(words, k), (words, k)
print('3000 random cases ok')

# what goes wrong without the trick
words = ['b', 'a', 'c', 'a', 'b', 'c']                  # all three tie with count 2
print('Counter.most_common (ties keep first-seen order):', [w for w, _ in Counter(words).most_common(3)])
print('heapq.nlargest on (count, word) (ties give LARGER word first):', [w for n, w in heapq.nlargest(3, [(n, w) for w, n in Counter(words).items()])])
print('heap of (-count, word) (what the question wants):', top_k_heap(words, 3))

# the word part is only compared on a count tie; if the payload is unorderable a tie raises TypeError
h = []
heapq.heappush(h, (-2, {'w': 'x'}))
try:
    heapq.heappush(h, (-2, {'w': 'y'}))
except TypeError as e:
    print('TypeError on tied count with dict payload:', e)
# negating the string instead of the count does not work
try:
    heapq.heappush([], (-'abc', 1))
except TypeError as e:
    print('cannot negate a str (so negate the count, not the word):', e)
```

**Output (my run):**
```
3000 random cases ok
Counter.most_common (ties keep first-seen order): ['b', 'a', 'c']
heapq.nlargest on (count, word) (ties give LARGER word first): ['c', 'b', 'a']
heap of (-count, word) (what the question wants): ['a', 'b', 'c']
TypeError on tied count with dict payload: '<' not supported between instances of 'dict' and 'dict'
cannot negate a str (so negate the count, not the word): bad operand type for unary -: 'str'
```

**Edge cases:**
- All words tie: the answer is alphabetical.
- `k` equals the number of distinct words: the whole sorted list.
- A single word repeated.
- `most_common` does NOT sort ties alphabetically (it keeps first-seen order), and `nlargest` on `(count, word)` gives the LARGER word first on ties. The code prints both.

**Follow-ups:**
- *Why not push `(count, word)`?* A min-heap would put the smallest count first, the opposite of what you need.
- *Payload not orderable?* Add an integer tie-break field (an insertion counter) before the payload so a tie never reaches it; the code shows the `TypeError` otherwise.
- *Streaming top-k?* Keep counts in a dict and a heap with lazy updates; the count can change, so stale entries must be skipped when popped.

**Common mistakes:**
- Using `Counter.most_common(k)` and assuming alphabetical ties.
- Negating the string, or negating nothing and using `nlargest` with the wrong tie order.
- Sorting the whole list when only k are needed (fine for correctness, costs time).
- Returning `(count, word)` pairs instead of words.

### Q9 ⭐⭐⭐ 🟡 K closest points to the origin. Given `points` as [x, y] integer pairs (1 <= len <= 10^5, |x|, |y| <= 10^4, duplicates allowed) and 1 <= k <= len, return k points with the smallest Euclidean distance to (0, 0). Compare squared distances, never take square roots. The checker accepts any k points whose squared distances are the k smallest (as a multiset), in any order, so when several points tie at the k-th distance any of them may be returned; the examples show one accepted answer. Give a max-heap of size k (O(n log k)) and a quickselect on squared distance (expected O(n)), and say why heapq.nsmallest with a key is the short answer and when it is not (large k). Example: points=[[1, 3], [-2, 2]], k=1 -> [[-2, 2]]; points=[[3, 3], [5, -1], [-2, 4]], k=2 -> [[3, 3], [-2, 4]]; points=[[1, 1], [-1, -1], [2, 2], [0, 3]], k=2 -> [[1, 1], [-1, -1]].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Top-k with a max-heap of size k (keep the k closest; the root is the farthest of them), or quickselect on the distance.

**Say this first (1 line):** "Squared distance, no square root. A max-heap of size k keeps the k closest; when a new point is closer than the farthest kept, swap it in."

**Brute force:** Sort all points by squared distance and slice `[:k]`. O(n log n), O(n) space. Fine, but more than needed for small k.

**Optimal:**
- Squared distance `x*x + y*y` is exact integer arithmetic. The order is the same as with the real distance, so the square root is never needed (and floats could round).
- Heap: keep tuples `(-d2, index)`. Python's heap is a min-heap, so the negated distance makes the farthest point sit at the root. Replace the root when the new point is strictly closer.
- Put the point's index in the tuple instead of the point: on a distance tie the next field is an int, so comparisons never touch the payload. With plain objects a tie raises `TypeError` (the code shows it).
- Quickselect: three-way partition of indices by squared distance, keep going in the part that contains the k boundary. Expected O(n), worst O(n^2) without a random pivot. The result is k points in no particular order.
- `heapq.nsmallest(k, points, key=d2)` is the short answer. It uses a size-k heap (and plain sorting only when k >= n). For large k the heap does O(n log k) work with real constant factors, so `sorted(...)[:k]` or quickselect is the honest choice there.
- Ties at the k-th distance: several answers are valid. The checker accepts any k points whose squared distances are the k smallest as a multiset, so the code validates instead of comparing lists.

**Complexity:** Heap O(n log k) time, O(k) space. Quickselect expected O(n) time, O(n) for the index array. Sorting O(n log n).

**Dry run:** `[[3, 3], [5, -1], [-2, 4]]`, k=2. Squared distances 18, 26, 20. Heap fills with 18 and 26: root is the farthest (26). Third point 20 < 26: replace, heap holds 18 and 20. Answer `[[3, 3], [-2, 4]]`.

**Code:**
```python
import heapq
import random
from collections import Counter

random.seed(9)

def d2(p):
    return p[0] * p[0] + p[1] * p[1]                    # squared distance: exact ints, no sqrt

def k_closest_heap(points, k):
    h = []                                              # max-heap of size k via negated distance
    for i, p in enumerate(points):
        item = (-d2(p), i)                              # index i breaks ties with ints, never compares points
        if len(h) < k:
            heapq.heappush(h, item)
        elif item > h[0]:                               # strictly closer than the farthest kept
            heapq.heapreplace(h, item)
    return [list(points[i]) for _, i in h]              # O(n log k)

def k_closest_nsmallest(points, k):
    return [list(p) for p in heapq.nsmallest(k, points, key=d2)]

def k_closest_quickselect(points, k, rng=random):
    """Iterative three-way quickselect on indices by squared distance. Expected O(n)."""
    idx = list(range(len(points)))
    dist = [d2(p) for p in points]
    lo, hi = 0, len(idx) - 1
    while lo < hi:
        pivot = dist[idx[rng.randint(lo, hi)]]
        lt, i, gt = lo, lo, hi
        while i <= gt:
            v = dist[idx[i]]
            if v < pivot:
                idx[lt], idx[i] = idx[i], idx[lt]; lt += 1; i += 1
            elif v > pivot:
                idx[i], idx[gt] = idx[gt], idx[i]; gt -= 1
            else:
                i += 1
        if k <= lt:
            hi = lt - 1                                 # all k wanted are strictly closer than pivot
        elif k > gt + 1:
            lo = gt + 1                                 # whole < and == blocks are in, keep searching right
        else:
            break                                       # the k-th boundary is inside the == block
    return [list(points[i]) for i in idx[:k]]

def valid(points, k, got):
    """Accept any k input points (as a multiset) whose squared distances are the k smallest."""
    if len(got) != k: return False
    if Counter(map(tuple, got)) - Counter(map(tuple, points)): return False
    return sorted(map(d2, got)) == sorted(map(d2, points))[:k]

fns = (k_closest_heap, k_closest_nsmallest, k_closest_quickselect)
cases = [([[1, 3], [-2, 2]], 1), ([[3, 3], [5, -1], [-2, 4]], 2), ([[1, 1], [-1, -1], [2, 2], [0, 3]], 2),
         ([[0, 0]], 1), ([[2, 2]] * 5, 3), ([[1, 0], [0, 1], [-1, 0], [0, -1]], 2), ([[10000, -10000], [0, 0]], 2)]
for pts, k in cases:
    for fn in fns:
        assert valid(pts, k, fn(pts, k)), (fn.__name__, pts, k)
assert sorted(k_closest_heap([[1, 3], [-2, 2]], 1)) == [[-2, 2]]
assert sorted(k_closest_heap([[3, 3], [5, -1], [-2, 4]], 2)) == [[-2, 4], [3, 3]]

for _ in range(3000):
    n = random.randint(1, 10)
    pts = [[random.randint(-3, 3), random.randint(-3, 3)] for _ in range(n)]
    k = random.randint(1, n)
    for fn in fns:
        assert valid(pts, k, fn(pts, k)), (fn.__name__, pts, k)
print('3000 random cases ok (validator: multiset of k smallest squared distances)')

# ties at the k-th distance: several answers are valid, so never compare outputs literally
pts = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
print('four points tie at d2=2, k=2 ->', k_closest_heap(pts, 2), 'and', k_closest_quickselect(pts, 2))

# why the index in the heap tuple: tuples of (distance, payload) tie on distance, then compare payloads
class P:
    def __init__(self, x, y): self.x, self.y = x, y
h = [(2, P(1, 1))]
try:
    heapq.heappush(h, (2, P(-1, 1)))
except TypeError as e:
    print('TypeError on tie with unorderable point objects:', e)
big = [[random.randint(-10**4, 10**4), random.randint(-10**4, 10**4)] for _ in range(100000)]
assert valid(big, 1000, k_closest_heap(big, 1000)) and valid(big, 1000, k_closest_quickselect(big, 1000))
print('n = 10^5, k = 1000 ok for heap and quickselect')
```

**Output (my run):**
```
3000 random cases ok (validator: multiset of k smallest squared distances)
four points tie at d2=2, k=2 -> [[1, -1], [-1, -1]] and [[1, 1], [-1, 1]]
TypeError on tie with unorderable point objects: '<' not supported between instances of 'P' and 'P'
n = 10^5, k = 1000 ok for heap and quickselect
```

**Edge cases:**
- Duplicate points: both can be returned.
- A point at the origin (distance 0).
- Ties at the k-th distance: any of the tied points is valid.
- `k == n`: return everything.

**Follow-ups:**
- *Why not a min-heap of all n?* It also works (n heapify, k pops, O(n + k log n)) but needs O(n) memory; the size-k heap uses O(k).
- *Points arrive as a stream?* The size-k max-heap is the natural fit.
- *Distance to an arbitrary query point?* Same code with the difference vector.

**Common mistakes:**
- Taking `math.sqrt` (slower, and float comparisons can mislead).
- A min-heap of size k (keeps the k farthest).
- Pushing `(d, point)` with unorderable points.
- Comparing the output lists literally when ties exist.

### Q10 ⭐⭐⭐ 🟡 Merge k sorted arrays with a heap. `lists` holds k sorted (non-decreasing) integer lists, 0 <= k <= 100, each of length 0 to 500, total length N <= 10^4 (the same list length bound as the linked-list version in Part 6 Q12, which uses the heap only as a merge tool; here the heap is the subject). Return one sorted list. Keep a heap of (value, list index, position) so the heap never holds more than k entries and ties never compare anything but integers; each pop is followed by at most one push. State the cost (O(N log k) time, O(k) extra heap space), compare with concatenating and sorting (O(N log N)) and with pairwise divide and conquer merging (also O(N log k)), and say why `heapq.merge` is the library version and what it returns (an iterator). Example: lists=[[1, 4, 5], [1, 3, 4], [2, 6]] -> [1, 1, 2, 3, 4, 4, 5, 6]; lists=[[], [1], []] -> [1]; lists=[] -> []; lists=[[2, 2], [2], [1, 2, 3]] -> [1, 2, 2, 2, 2, 3].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Candidate-reported rounds on Naukri Code360 (a Flipkart August 2022 write-up with merge intervals, an Amazon August 2021 online round with merge intervals, a Flipkart May 2021 SDE-1 online test with merge k sorted arrays; snippets only, not opened; self-reported, unverified) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** k-way merge with a heap holding one head per list. This is the "merge k sorted" heap pattern; the linked-list version is Part 6 Q12.

**Say this first (1 line):** "Put the first element of every list in a min-heap as (value, list index, position). Pop the smallest, then push the next element of that same list."

**Brute force:** Concatenate everything and sort: O(N log N), ignores that the lists are already sorted. Merging one list at a time into a growing result is O(N * k) in the worst case.

**Optimal:**
- Heap entries `(value, list_index, position)`. The heap holds at most one entry per list, so size is at most k.
- Pop the minimum, append the value, push the next element of that list if there is one (at most one push per pop).
- Tie on equal values: the next field is the list index, an int, so nothing unorderable is ever compared. Equal values come out in list order (a stable merge). Putting a list iterator in the tuple instead would raise `TypeError` on a tie, which the code shows.
- Invariant: the heap contains the smallest not-yet-output element of every non-exhausted list, so its root is the smallest remaining overall.
- Comparison: pairwise divide and conquer (merge pairs, repeat) is also O(N log k): log2(k) rounds, each touching N items. Concatenate-and-sort is O(N log N); on a nearly merged input Timsort may be fast, but it gives no worst-case guarantee.
- `heapq.merge(*lists)` is the library version. It returns an iterator (a generator in CPython), so wrap it in `list(...)` and note it works lazily on huge inputs.

**Complexity:** Time O(N log k): N pops and at most N pushes, each O(log k). Extra space O(k) for the heap (plus O(N) for the output).

**Dry run:** `[[1, 4, 5], [1, 3, 4], [2, 6]]`. Heap `[(1,0,0), (1,1,0), (2,2,0)]`. Pop `(1,0,0)`: out `[1]`, push `(4,0,1)`. Pop `(1,1,0)`: out `[1, 1]`, push `(3,1,1)`. Pop `(2,2,0)`: out `[1,1,2]`, push `(6,2,1)`. Pop `(3,1,1)`: push `(4,1,2)`. Pop `(4,0,1)` (tie with `(4,1,2)` goes to list 0): push `(5,0,2)`. Pop `(4,1,2)`, then 5, then 6. Output `[1, 1, 2, 3, 4, 4, 5, 6]`.

**Code:**
```python
import heapq
import random

random.seed(10)

def merge_heap(lists):
    h = [(l[0], i, 0) for i, l in enumerate(lists) if l]   # one head per non-empty list: (value, list index, position)
    heapq.heapify(h)
    out, peak = [], len(h)
    while h:
        v, i, j = heapq.heappop(h)
        out.append(v)
        if j + 1 < len(lists[i]):                       # at most one push per pop
            heapq.heappush(h, (lists[i][j + 1], i, j + 1))
        peak = max(peak, len(h))
    assert peak <= len(lists)                           # heap never holds more than k entries
    return out                                          # O(N log k) time, O(k) heap space

def merge_two(a, b):
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if b[j] < a[i]: out.append(b[j]); j += 1        # strict <: ties take from a first, stable
        else: out.append(a[i]); i += 1
    out.extend(a[i:]); out.extend(b[j:])
    return out

def merge_pairwise(lists):
    """Bottom-up divide and conquer, iterative: log2(k) rounds, each touching N items -> O(N log k)."""
    cur = [list(l) for l in lists]
    if not cur: return []
    while len(cur) > 1:
        nxt = [merge_two(cur[i], cur[i + 1]) for i in range(0, len(cur) - 1, 2)]
        if len(cur) % 2: nxt.append(cur[-1])
        cur = nxt
    return cur[0]

def merge_library(lists):
    return list(heapq.merge(*lists))                    # heapq.merge returns an ITERATOR, wrap it in list()

def merge_sort_all(lists):
    return sorted(x for l in lists for x in l)          # O(N log N), the brute force

fns = (merge_heap, merge_pairwise, merge_library, merge_sort_all)
for fn in fns:
    assert fn([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert fn([[], [1], []]) == [1]
    assert fn([]) == []
    assert fn([[2, 2], [2], [1, 2, 3]]) == [1, 2, 2, 2, 2, 3]
    assert fn([[], []]) == []
    assert fn([[-3, -3], [-3]]) == [-3, -3, -3]

for _ in range(2000):
    k = random.randint(0, 6)
    lists = [sorted(random.randint(-5, 5) for _ in range(random.randint(0, 6))) for _ in range(k)]
    want = merge_sort_all(lists)
    for fn in fns:
        assert fn(lists) == want, (fn.__name__, lists)
print('2000 random cases ok')

# max constraints: k = 100 lists, N = 10^4
big = [sorted(random.randint(-10**9, 10**9) for _ in range(100)) for _ in range(100)]
assert merge_heap(big) == merge_sort_all(big) == merge_pairwise(big)
print('k = 100, N = 10^4 ok; heapq.merge type:', type(heapq.merge([1], [2])).__name__)

# tie-breaking: without the list index, a tie on value would compare the NEXT tuple field
it_a, it_b = iter([1]), iter([1])
try:
    heapq.heappush([(1, it_a)], (1, it_b))               # (value, iterator): tie on value, then iterator < iterator
except TypeError as e:
    print('TypeError on tied value with iterator payload:', e)
# with the index the first field that differs is always an int, and equal values come out in list order
h = [(2, 0, 0), (2, 1, 0), (2, 2, 0)]
heapq.heapify(h)
print('equal values pop in list-index order:', [heapq.heappop(h)[1] for _ in range(3)])

# a lazily consumed merge: heapq.merge never builds the full output
gen = heapq.merge([1, 5, 9], [2, 6], [3])
print('first three from the iterator:', [next(gen) for _ in range(3)])
```

**Output (my run):**
```
2000 random cases ok
k = 100, N = 10^4 ok; heapq.merge type: generator
TypeError on tied value with iterator payload: '<' not supported between instances of 'list_iterator' and 'list_iterator'
equal values pop in list-index order: [0, 1, 2]
first three from the iterator: [1, 2, 3]
```

**Edge cases:**
- `lists = []`, or all lists empty: `[]`.
- Empty lists mixed with non-empty ones: skip them when building the heap.
- Heavy duplicates and negatives.
- One huge list and many tiny ones: still O(N log k).

**Follow-ups:**
- *k = 2?* The two-pointer merge, O(N).
- *Only the first m results?* Stop after m pops: O(k + m log k).
- *Linked lists?* Same idea with node pointers (Part 6 Q12); in Python push `(val, i, node)` so ties never compare nodes.

**Common mistakes:**
- Pushing `(value, list)` or `(value, node)` with no index: `TypeError` on equal values.
- Pushing the whole list again instead of only the next element, which makes the heap O(N).
- Forgetting empty lists (`l[0]` raises `IndexError`).
- Assuming `heapq.merge` returns a list.

### Q11 ⭐⭐⭐ 🟡 Task scheduler with cooldown. `tasks` is a string of uppercase letters (1 <= len <= 10^4), one task per letter, each taking one time slot; a CPU runs one task or idles per slot, and two runs of the same letter must have at least n other slots (idle or other tasks) between them (0 <= n <= 100). Return the minimum number of slots to finish all tasks, in any order. Solve it with a max-heap of remaining counts plus a cooldown queue, then with the closed form max(len(tasks), (max_count - 1) * (n + 1) + number_of_letters_with_max_count), and explain why the formula is a lower bound that the schedule always meets. Example: tasks='AAABBB', n=2 -> 8; tasks='AAABBB', n=0 -> 6; tasks='AAAAAABCDEFG', n=2 -> 16; tasks='AABC', n=1 -> 4; tasks='A', n=50 -> 1.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy by most remaining count, with a cooldown queue. The most frequent task is the bottleneck, so it must always be scheduled as early as allowed.

**Say this first (1 line):** "The most frequent letter sets the frame: (max_count - 1) full frames of n + 1 slots, plus one last slot for every letter that ties for the max. If there are enough other tasks, no idle is needed, so the answer is also at least len(tasks)."

**Brute force:** BFS over states (remaining counts, cooldown left per letter), with a slot that either runs a ready letter or idles. Exponential in the number of letters; the code uses it on tiny inputs as the oracle.

**Optimal:**
- Heap simulation: max-heap of remaining counts (negated ints). Each time slot: move letters whose cooldown ended back into the heap; if the heap is non-empty, run the largest count; if copies remain, park it in a deque with its ready time `t + n + 1`. If the heap is empty but the deque is not, the slot is idle. The heap holds only ints, so ties never compare anything else.
- Closed form: `max(len(tasks), (mx - 1) * (n + 1) + k)` where `mx` is the highest count and `k` the number of letters having that count.
- Why it is a lower bound: the `mx` copies of one letter need `mx - 1` gaps of at least n other slots between them, so at least `(mx - 1) * (n + 1) + 1` slots. All `k` letters tied at the max each need their last copy, which fit in the final frame, giving `+ k`. Every task needs a slot, so `len(tasks)` is a bound too.
- Why the schedule meets it: lay the max letters out as columns of frames of width n + 1, fill each frame with other letters or idles. If the frames cannot absorb all the other tasks, nothing is idle and the tasks just run back to back, length `len(tasks)`. The code checks heap, formula and BFS agree on every multiset of A-C up to length 7 with n = 0 to 3.

**Complexity:** Formula: O(len(tasks)) to count, O(1) space beyond 26 counters. Heap simulation: each slot costs O(log 26), and total slots can be up to about `len * (n + 1)` in the worst case (one letter repeated), so O(len * n) worst time, which is about 10^6 here. That is why the formula is the better final answer.

**Dry run:** `'AAABBB'`, n=2. Counts A 3, B 3, so mx=3, k=2. Formula: (3 - 1) * 3 + 2 = 8, and `len` is 6, so 8. Schedule: A B idle A B idle A B (8 slots). Heap: slot 1 runs A (2 left, ready at 4), slot 2 runs B (ready at 5), slot 3 heap empty, idle. Slot 4: A returns, run it, and so on.

**Code:**
```python
import heapq
import random
from collections import Counter, deque

random.seed(11)

def schedule_heap(tasks, n):
    h = [-c for c in Counter(tasks).values()]           # max-heap of remaining counts (negated ints)
    heapq.heapify(h)
    cool = deque()                                      # (time when usable again, remaining count)
    t = 0
    while h or cool:
        t += 1                                          # one slot per loop pass, idle or not
        while cool and cool[0][0] <= t:
            heapq.heappush(h, cool.popleft()[1])        # cooled down: back into the heap
        if h:
            left = heapq.heappop(h) + 1                 # run the task with most left
            if left:                                    # still has copies: cool for n slots
                cool.append((t + n + 1, left))
    return t

def schedule_formula(tasks, n):
    c = Counter(tasks)
    mx = max(c.values())
    k = sum(1 for v in c.values() if v == mx)
    return max(len(tasks), (mx - 1) * (n + 1) + k)

def schedule_brute(tasks, n):
    """BFS over states (remaining counts, cooldown left per letter): each slot runs a ready letter or idles."""
    letters = sorted(set(tasks))
    start = (tuple(tasks.count(l) for l in letters), (0,) * len(letters))
    seen, dq = {start}, deque([(start, 0)])
    while dq:
        (cnt, cd), t = dq.popleft()
        if not any(cnt): return t
        base = tuple(max(x - 1, 0) for x in cd)
        nxt = [(cnt, base)]                             # idle
        for i in range(len(cnt)):
            if cnt[i] and cd[i] == 0:
                c2, d2 = list(cnt), list(base)
                c2[i] -= 1; d2[i] = n
                nxt.append((tuple(c2), tuple(d2)))
        for s in nxt:
            if s not in seen:
                seen.add(s); dq.append((s, t + 1))

for fn in (schedule_heap, schedule_formula, schedule_brute):
    assert fn('AAABBB', 2) == 8
    assert fn('AAABBB', 0) == 6
    assert fn('AAAAAABCDEFG', 2) == 16
    assert fn('AABC', 1) == 4
    assert fn('A', 50) == 1

# exhaustive: every multiset of letters A-C (as sorted strings) up to length 7, n in 0..3
import itertools
count = 0
for L in range(1, 8):
    for combo in itertools.combinations_with_replacement('ABC', L):
        s = ''.join(combo)
        for n in range(4):
            b = schedule_brute(s, n)
            assert schedule_heap(s, n) == schedule_formula(s, n) == b, (s, n)
            assert b >= len(s) and b >= (max(Counter(s).values()) - 1) * (n + 1) + 1   # lower bounds
            count += 1
print('exhaustive over', count, 'multisets x n: heap == formula == BFS')

for _ in range(300):
    s = ''.join(random.choice('ABCD') for _ in range(random.randint(1, 8)))
    n = random.randint(0, 4)
    assert schedule_heap(s, n) == schedule_formula(s, n) == schedule_brute(s, n)
print('300 random strings ok')

big = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(10**4))
assert schedule_heap(big, 100) == schedule_formula(big, 100)
print('n = 10^4 tasks, cooldown 100: heap == formula =', schedule_formula(big, 100))

# the formula is a lower bound: the max letters form (mx-1) full frames of n+1 slots plus a last partial frame
print('AAABBB n=2 frame:  A B _ | A B _ | A B  -> (3-1)*(2+1) + 2 =', (3 - 1) * 3 + 2)
# when many distinct letters exist, no idle is ever needed and the answer is len(tasks)
print('ABCDEFGH n=2:', schedule_formula('ABCDEFGH', 2), '| AAABBBCCC n=1:', schedule_formula('AAABBBCCC', 1))
# heap tie-breaking: the heap holds bare ints, so ties never compare anything else.
# if you pushed (-count, letter) and later (-count, task_object) ties would compare the second field
h = []
heapq.heappush(h, (-2, {'t': 'A'}))
try:
    heapq.heappush(h, (-2, {'t': 'B'}))
except TypeError as e:
    print('TypeError if you store (count, unorderable task):', e)
```

**Output (my run):**
```
exhaustive over 476 multisets x n: heap == formula == BFS
300 random strings ok
n = 10^4 tasks, cooldown 100: heap == formula = 42522
AAABBB n=2 frame:  A B _ | A B _ | A B  -> (3-1)*(2+1) + 2 = 8
ABCDEFGH n=2: 8 | AAABBBCCC n=1: 9
TypeError if you store (count, unorderable task): '<' not supported between instances of 'dict' and 'dict'
```

**Edge cases:**
- `n = 0`: the answer is `len(tasks)` (the formula gives `mx` at most, so the `len` term wins).
- One distinct letter: `(mx - 1) * (n + 1) + 1`.
- Many distinct letters: no idles, answer `len(tasks)`.
- A single task with a large n: 1 slot, there is nothing to wait for.

**Follow-ups:**
- *Also return the schedule?* Use the heap simulation and record the letter or `idle` each slot.
- *Why does the largest-first choice work?* An exchange argument: swapping a smaller-count letter in for a larger-count one earlier never helps the bottleneck letter.
- *Reorganise a string so no two equal letters are adjacent?* The same heap idea with n = 1.

**Common mistakes:**
- Forgetting the `+ k` for ties at the max count.
- Forgetting `max(len(tasks), ...)`, which undercounts when no idle is needed.
- Using the cooldown as `n` instead of `n + 1` in the frame width.
- Running the heap simulation and forgetting the idle slots when only the cooldown queue is non-empty.

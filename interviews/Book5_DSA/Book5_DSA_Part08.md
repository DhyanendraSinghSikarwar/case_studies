# Book 5 — Part 8: Heaps, Intervals and Greedy

**Topic:** Python DSA for product-company interviews: heapq as a binary min-heap on a list and the max-heap negation trick, heap internals (parent and child indices, sift up and sift down, the O(n) build-heap argument), kth largest and smallest (sort versus a size-k heap versus quickselect), kth largest in a stream, top-k frequent words with tie-breaking, k closest points, merging k sorted arrays with a heap, task scheduler, reorganize string and its k-distance variant, last stone weight, minimum cost to connect sticks, median of a data stream (two heaps) and sliding-window median with lazy deletion, meeting rooms I, II and III, merge and insert intervals, non-overlapping intervals, minimum arrows to burst balloons, employee free time, interval list intersections, maximum events attended, smallest range covering k lists, furthest building and IPO as heap-greedy problems, k pairs with smallest sums, the greedy classics (jump game I and II, gas station, assign cookies, partition labels, candy, queue reconstruction by height, activity selection), exchange-argument proofs and the counter-examples for wrong greedy rules, when greedy fails (the coin counter-example and the hand-off to dynamic programming), the greedy feasibility check inside a binary search on the answer, Huffman coding at concept level, heapq with tuples and tie-breaking (entry counters, FIFO among equals), custom orderings and wrapper classes (a string cannot be negated), lazy deletion, and priority updates without decrease-key

**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 17, ⭐⭐ 18, ⭐ 10)  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns heaps, interval problems and greedy algorithms. Part 1 owns hashing and the counting-based top-k (cross-referenced as 'Part 1 Q10'), Part 2 owns sliding windows and two pointers (the sliding-window maximum and the boats two-pointer greedy are cross-referenced as 'Part 2 Q16' and 'Part 2 Q37'; boats is not repeated here), Part 4 owns stacks, queues and monotonic structures (the max stack, which uses the same lazy-deletion idea, as 'Part 4 Q38'), Part 5 owns binary search (the binary-search-on-answer wrapper and the monotone-predicate discussion are cross-referenced as 'Part 5 Q8' and 'Part 5 Q33', and the sorted-matrix kth smallest as 'Part 5 Q26'; this part writes only the greedy check inside them), Part 6 owns linked lists ('Part 6 Q12' merges k linked lists and uses the heap only as a merge tool, while here the heap is the subject and the data are arrays); each of these references was checked against its heading by build.py. Part 7 owns trees, Part 9 graphs (Dijkstra and minimum spanning trees; the indexed heap and lazy invalidation used for Dijkstra are only previewed here by the priority-update question), Parts 10 and 11 dynamic programming (the coin and the candy-style counter-examples hand off to them by part number only), Part 13 sorting internals and Part 14 design problems (rate limiters, schedulers as systems). Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Conventions: intervals are lists [start, end]; unless a prompt says otherwise they are half-open, so a meeting that ends at 5 does not clash with one starting at 5, and the merge, insert, intersection, balloon and employee-free-time questions say explicitly that they use closed intervals; a heap here is Python's heapq (a min-heap on a list), so every max-heap is written with negated values or a wrapper class; every solution is iterative, so no prompt depends on CPython's recursion limit of 1000, and the stated sizes (up to 10^5) were chosen for iterative heap and sorting solutions. Questions whose output is not unique say what the checker accepts: k closest points, reorganize string, k pairs with smallest sums, Huffman code lengths and the k-distance rearrangement are validated by property (same multiset, adjacency or distance rule, optimal sums or cost), and the examples show one accepted answer; the others state their tie rules (top-k words by count then alphabet, gas station smallest start, smallest range by width then start, meeting rooms III smallest room, FIFO among equal priorities, stable ties in nlargest). Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example below is rendered from the same data that scratch/B5P08_wavea/check_examples.py executes (python3 -I) against reference solutions, so no example can differ from what was run. Cross-checks: each reference against an independent brute force on thousands of random small inputs (sorted-list simulation, all subsets, all permutations, breadth-first search over schedules, exhaustive assignment, all contiguous splits, all subsets of a coordinate range) for kth largest and the stream, merge intervals (checked on a doubled-coordinate point set), insert, meeting rooms I and II (heap against sweep against point counting), non-overlapping intervals, intersections, maximum events (bipartite matching), balloons (hitting sets), employee free time (unit slots), top-k words, merge k arrays, median stream, last stone, cookies, sticks (all merge orders), furthest building (all brick and ladder choices), IPO (all project orders), smallest range, sliding median (including 3000 tie-heavy values and window sizes 1 to 3000), greedy days (all splits), meeting rooms III, candy (every rating array with values 0 to 2 up to length 4, plus random length 6), partition labels (all cut sets) and jump games (reachability dynamic programme). Claims tested exhaustively: the textbook bottom-up build-heap never exceeds n - popcount(n) swaps and reaches it, checked over every permutation of up to 8 distinct values, and the node heights of an n-node complete tree sum to n - popcount(n) for every n up to 2000, while CPython's own heapify layout differs from the textbook sift-down layout on about 14 percent of random lists (so the heap-internals prompt defines the textbook procedure exactly); the one-by-one build equals heappush layouts; the task-scheduler formula equals a heap simulation equals a breadth-first search over schedules for every sorted multiset of up to 7 tasks over three letters and cooldowns 0 to 3; reorganize string is possible exactly when the maximum letter count is at most (len + 1) // 2 for all 3^L strings up to length 7 over three letters (582 infeasible ones), and the k-distance rearrangement returns the empty string exactly when no permutation works (all those strings, k from 0 to 5); the gas-station answer equals the smallest valid start, and unique starts are not guaranteed (about a third of random small inputs have several valid starts, so the prompt asks for the smallest index); queue reconstruction recovers the original queue and the pairs of any queue are distinct and determine it uniquely for every queue of up to 6 people with heights 1 to 3; in activity selection earliest-finish matches brute force while shortest-first and earliest-start-first both first fail at exactly 3 activities and never with 1 or 2 (times 0 to 6); the largest-coin-first counter-example search needs only amounts below coins[-1] + coins[-2], checked for all 2047 coin systems with largest coin up to 12 (1854 non-canonical) against amounts up to 200, plus 300 random systems with a larger top coin; the day count of the greedy feasibility check is non-increasing in capacity; Huffman cost is the same for random tie-breaking, equals an exhaustive search over all full binary trees and equals the sticks answer; heapq.nlargest and nsmallest equal the stable sorted slices for every list of up to 6 scores with heavy ties; quickselect with first-element pivot and three-way partitions finishes in 1 round on all-equal input and needs len rounds on an ascending list with k = 1; lazy deletion never holds more heap entries than pushes and never pops more than pushes; pushing (priority, dict) tuples raises TypeError on ties while (priority, id) silently orders ties alphabetically instead of by arrival; a string cannot be negated. All solutions run at the stated limits (kth largest, sliding median and a 100-way merge over 10^5 values) without recursion. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part08_sources.md). Searches returned heap-pattern guides (igotanoffer, a LeetCode discuss post on four heap patterns, techinterview.org, DesignGurus), techinterview.org interval and greedy pattern pages, snippets of the heapq documentation recipe on entry counters and removed-task markers, Naukri Code360 candidate-reported entries (a Flipkart August 2022 write-up and an Amazon August 2021 online round with merge intervals, a Flipkart May 2021 online test with merge k sorted arrays) and canonical coin-system papers (Kozen and Zaks); nothing was found tying kth-largest, meeting rooms, task scheduler, median of a stream, candy, jump game or the other items to a named company beyond those entries, so 'Asked at' tags name source types (pattern guides, candidate-reported snippets, editor knowledge of standard lists), not verified company reports. The snippets did not cover partition labels, queue reconstruction, furthest building, IPO, smallest range or meeting rooms III, which come from editor knowledge. The bounds and uniqueness claims above were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---

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

### Q12 ⭐⭐⭐ 🟡 Jump game (can you reach the end). `nums` holds non-negative integers (1 <= len <= 10^4), where nums[i] is the maximum jump length from index i (any length from 0 to nums[i] is allowed). Starting at index 0, return True if you can reach the last index. Give the O(n) greedy that tracks the farthest reachable index and returns False when the scan reaches an index beyond it, state the invariant, and say why the DP and the BFS versions are O(n^2) in the worst case. Example: nums=[2, 3, 1, 1, 4] -> True; nums=[3, 2, 1, 0, 4] -> False; nums=[0] -> True; nums=[1, 0, 1] -> False.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy with an invariant: track the farthest reachable index while scanning left to right.

**Say this first (1 line):** "I scan once and keep `far`, the farthest index I can reach from the indices I have already visited. If the scan hits an index bigger than `far`, I am stuck, so False. Otherwise True."

**Brute force:**
- DP or BFS: from every reachable index `i`, mark all of `i+1 .. i+nums[i]` reachable.
- Worst case is `nums = [n, n, ..., n]`. Every index is reachable and each one marks about n - i cells, so the total is n(n-1)/2 marks. That is O(n^2) time (the run below counts 1,999,000 marks for n = 2000).
- BFS has the same count: each index is queued once, but each pop scans its whole jump range, so the edge scans add up to the same O(n^2).

**Optimal:**
- One pass. `far = 0`. For each `i`: if `i > far`, return False. Else `far = max(far, i + nums[i])`.
- **Invariant:** before step `i`, every index in `0..far` is reachable, and nothing beyond `far` is. Reachable set is always a prefix, because from any reachable index you can take any shorter jump too (lengths 0 to `nums[i]`). That prefix property is why one number is enough.
- If the scan gets through the last index, it was reachable. Early exit when `far >= n - 1` is optional.
- Failure is exactly "some index `i` has `i > far`": a block of zeros (or small values) that no earlier jump clears.

**Complexity:** Time O(n), one pass. Space O(1). The DP and BFS are O(n) space and O(n^2) time.

**Dry run:** `[3, 2, 1, 0, 4]`.
| i | nums[i] | i > far? | far after |
|---|---|---|---|
| 0 | 3 | no (0 > 0 is false) | 3 |
| 1 | 2 | no | 3 |
| 2 | 1 | no | 3 |
| 3 | 0 | no (3 > 3 is false) | 3 |
| 4 | 4 | yes (4 > 3) | return False |

Every path lands on index 3, which has a 0, so index 4 is out of reach.

**Code:**
```python
import random
import itertools

random.seed(12)

def can_reach_greedy(nums):
    far = 0                                  # farthest index reachable so far
    for i, x in enumerate(nums):
        if i > far:                          # index i is out of reach: stuck
            return False
        far = max(far, i + x)
        if far >= len(nums) - 1:             # early exit, optional
            return True
    return True

def can_reach_dp(nums):                      # forward marking, O(n^2) worst case
    n = len(nums)
    ok = [False] * n
    ok[0] = True
    for i in range(n):
        if ok[i]:
            for j in range(i + 1, min(n, i + nums[i] + 1)):
                ok[j] = True
    return ok[-1]

def can_reach_bfs(nums):                     # explicit queue, also O(n^2) worst case
    from collections import deque
    n = len(nums)
    seen = [False] * n
    seen[0] = True
    q = deque([0])
    while q:
        i = q.popleft()
        if i == n - 1:
            return True
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if not seen[j]:
                seen[j] = True
                q.append(j)
    return False

# --- the four examples in the prompt
for nums, exp in [([2, 3, 1, 1, 4], True), ([3, 2, 1, 0, 4], False), ([0], True), ([1, 0, 1], False)]:
    assert can_reach_greedy(nums) == can_reach_dp(nums) == can_reach_bfs(nums) == exp
    print(nums, '->', can_reach_greedy(nums))

# --- exhaustive: every list of length 1..6 with values 0..4 (5^1 + ... + 5^6 = 19530 lists)
cnt = 0
for n in range(1, 7):
    for nums in itertools.product(range(5), repeat=n):
        nums = list(nums)
        g = can_reach_greedy(nums)
        assert g == can_reach_dp(nums) == can_reach_bfs(nums), nums
        cnt += 1
print('exhaustive ok:', cnt, 'lists')

# --- seeded random
for _ in range(500):
    nums = [random.randint(0, 6) for _ in range(random.randint(1, 30))]
    assert can_reach_greedy(nums) == can_reach_dp(nums)
print('random ok: 500 lists')

# --- worst case for the DP: huge jumps, every index reachable, n inner steps each
n = 2000
big = [n] * n
ops = sum(min(n, i + big[i] + 1) - (i + 1) for i in range(n))
print('DP inner steps on n=2000 all-big jumps:', ops, '(about n^2 / 2); greedy scans', n)
assert ops == n * (n - 1) // 2

# --- edge cases
assert can_reach_greedy([0]) is True
assert can_reach_greedy([0, 1]) is False       # stuck at index 0
assert can_reach_greedy([1, 0]) is True        # a 0 on the last index is fine
assert can_reach_greedy([5, 0, 0, 0, 0, 0]) is True
assert can_reach_greedy([1, 1, 0, 1]) is False
assert can_reach_greedy([0] * 10000) is False
assert can_reach_greedy([1] * 10000) is True
print('edge cases ok')
```

**Output (my run):**
```
[2, 3, 1, 1, 4] -> True
[3, 2, 1, 0, 4] -> False
[0] -> True
[1, 0, 1] -> False
exhaustive ok: 19530 lists
random ok: 500 lists
DP inner steps on n=2000 all-big jumps: 1999000 (about n^2 / 2); greedy scans 2000
edge cases ok
```

**Edge cases:**
- `[0]`: one element, already at the end, True. `[0, 1]`: stuck at 0, False.
- A zero on the LAST index is fine (`[1, 0]` is True). A zero in the middle is only fatal if `far` equals that index.
- Ten thousand zeros: False at i = 1. Ten thousand ones: True.
- Large `nums[i]` just saturates `far`; Python ints cannot overflow, so `i + nums[i]` is safe.

**Follow-ups:**
- Minimum number of jumps? Q13 in this part: same `far`, but count level ends.
- Backward version? Keep `goal = n - 1`; for `i` from the end, if `i + nums[i] >= goal` then `goal = i`. True if `goal == 0`. Same O(n).
- Return the path? Store the parent of each index when `far` improves, or use the DP version.

**Common mistakes:**
- Using `<` instead of `<=` for the stuck test: `i > far` is the stuck condition, `i == far` is still reachable.
- Taking `nums[i]` as the exact jump length (it is the maximum).
- Greedy "always jump the maximum": fails on `[2, 3, 1, 1, 4]`-style inputs where a shorter jump lands on a bigger number.
- Calling it DP-with-memoised-recursion on n = 10^4: recursion depth hits the limit.

### Q13 ⭐⭐⭐ 🟡 Jump game II (minimum jumps). Same moves as the reachability version: nums[i] is the maximum jump length from index i, 1 <= len <= 10^4, and the last index is guaranteed reachable. Return the minimum number of jumps from index 0 to the last index (0 when len is 1). Give the O(n) greedy that treats the reachable indices as BFS levels (current level end, farthest next reach, count a jump when the scan hits the level end), and say why this is BFS without a queue and why the scan stops before the last index. Example: nums=[2, 3, 1, 1, 4] -> 2; nums=[2, 3, 0, 1, 4] -> 2; nums=[0] -> 0; nums=[1, 1, 1, 1] -> 3.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** BFS levels without a queue. The set of indices reachable in k jumps is always a contiguous prefix, so a level is just an index range.

**Say this first (1 line):** "It is BFS where level k is the range of indices reachable in exactly k jumps. I scan the level, track the farthest index the next level can reach, and when I finish the level I count a jump."

**Brute force:**
- BFS (queue) or DP: `d[j] = min(d[j], d[i] + 1)` for every `j` in `i+1 .. i+nums[i]`.
- Correct, but each index scans its whole jump range: O(n^2) on `[n, n, ..., n]`. I use both as oracles in the code.

**Optimal:**
- Three variables: `jumps`, `level_end` (last index of the current level), `far` (farthest index reachable from anything scanned so far).
- For each `i`: `far = max(far, i + nums[i])`. When `i == level_end` the level is finished, so `jumps += 1` and `level_end = far`.
- Why it is BFS: level k is `(end of level k-1, end of level k]`. Everything in it was first reached by jump k. `far` while scanning level k is the end of level k+1.
- Why the scan stops before the last index: once `level_end >= n - 1` the last index is already inside the next level and we have counted the jump that gets there. If we scanned index `n - 1` itself and it happened to equal `level_end`, we would count one phantom jump (`[0]` would give 1, `[2, 3, 1, 1, 4]` would give 3; the code prints both).
- Guaranteed reachable means `far` never gets stuck below `n - 1`, so `level_end` always advances.

**Complexity:** Time O(n), one pass. Space O(1).

**Dry run:** `[2, 3, 1, 1, 4]`, `jumps = end = far = 0`.
| i | far | i == end? | jumps | end |
|---|---|---|---|---|
| 0 | 2 | yes | 1 | 2 |
| 1 | 4 | no | 1 | 2 |
| 2 | 4 | yes | 2 | 4 |
| 3 | 4 | no | 2 | 4 |

The loop stops at i = 3 (before index 4). Answer 2: jump 0 -> 1 (length 1), then 1 -> 4 (length 3).

**Code:**
```python
import random
import itertools
from collections import deque

random.seed(13)

def min_jumps_greedy(nums):
    jumps = 0
    level_end = 0                            # last index of the current BFS level
    far = 0                                  # farthest index reachable from the current level
    for i in range(len(nums) - 1):           # stop BEFORE the last index
        far = max(far, i + nums[i])
        if i == level_end:                   # finished scanning this level: one more jump
            jumps += 1
            level_end = far
    return jumps

def min_jumps_bfs(nums):                     # real BFS, O(n^2) worst case
    n = len(nums)
    dist = [-1] * n
    dist[0] = 0
    q = deque([0])
    while q:
        i = q.popleft()
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if dist[j] < 0:
                dist[j] = dist[i] + 1
                q.append(j)
    return dist[-1]

def min_jumps_dp(nums):                      # forward relaxation, O(n^2)
    n = len(nums)
    INF = 10 ** 9
    d = [INF] * n
    d[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            d[j] = min(d[j], d[i] + 1)
    return d[-1]

def reachable(nums):
    far = 0
    for i, x in enumerate(nums):
        if i > far:
            return False
        far = max(far, i + x)
    return True

for nums, exp in [([2, 3, 1, 1, 4], 2), ([2, 3, 0, 1, 4], 2), ([0], 0), ([1, 1, 1, 1], 3)]:
    assert min_jumps_greedy(nums) == min_jumps_bfs(nums) == min_jumps_dp(nums) == exp
    print(nums, '->', min_jumps_greedy(nums))

# exhaustive: every list of length 1..6 over 0..4 whose last index is reachable
cnt = 0
for n in range(1, 7):
    for t in itertools.product(range(5), repeat=n):
        nums = list(t)
        if not reachable(nums):
            continue
        assert min_jumps_greedy(nums) == min_jumps_bfs(nums) == min_jumps_dp(nums), nums
        cnt += 1
print('exhaustive ok:', cnt, 'reachable lists')

# seeded random, longer lists (force reachability by lifting zeros to 1)
for _ in range(500):
    nums = [random.randint(1, 6) if random.random() < 0.7 else 1 for _ in range(random.randint(1, 40))]
    assert min_jumps_greedy(nums) == min_jumps_bfs(nums)
print('random ok: 500 lists')

# why the scan stops before the last index: with range(len(nums)) a final level end would add a phantom jump
def min_jumps_no_stop(nums):                 # WRONG on purpose
    jumps = end = far = 0
    for i in range(len(nums)):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
    return jumps
print('no-stop variant on [2, 3, 1, 1, 4]:', min_jumps_no_stop([2, 3, 1, 1, 4]), '(wrong, answer is 2)')
print('no-stop variant on [0]:', min_jumps_no_stop([0]), '(wrong, answer is 0)')
assert min_jumps_no_stop([0]) == 1 and min_jumps_greedy([0]) == 0
assert min_jumps_no_stop([2, 3, 1, 1, 4]) == 3

# edge cases and a big input (iterative, no recursion)
assert min_jumps_greedy([7]) == 0
assert min_jumps_greedy([1] * 10000) == 9999
assert min_jumps_greedy([10000] + [1] * 9999) == 1
assert min_jumps_greedy([5, 4, 3, 2, 1, 1, 1]) == 2
print('edge cases ok')
```

**Output (my run):**
```
[2, 3, 1, 1, 4] -> 2
[2, 3, 0, 1, 4] -> 2
[0] -> 0
[1, 1, 1, 1] -> 3
exhaustive ok: 13635 reachable lists
random ok: 500 lists
no-stop variant on [2, 3, 1, 1, 4]: 3 (wrong, answer is 2)
no-stop variant on [0]: 1 (wrong, answer is 0)
edge cases ok
```

**Edge cases:**
- `[x]`: length 1 gives 0 jumps, because the loop body never runs.
- `[10000] + [1] * 9999`: one jump.
- `[1] * 10000`: 9999 jumps. Iterative, no recursion limit problem.
- Zeros in the middle are fine as long as an earlier jump clears them (`[2, 3, 0, 1, 4]` is 2).

**Follow-ups:**
- What if the end may be unreachable? Run the Q12 reachability check first, or return -1 when `far <= i` at `level_end`.
- Why not DP? Same answer, O(n^2). Say the greedy is BFS in disguise and the DP is the same BFS with a table.
- Why is "jump to the cell with the biggest `i + nums[i]`" also correct? It is the same greedy seen from the other side, but harder to prove.

**Common mistakes:**
- Looping to `len(nums)` and counting a phantom jump.
- Counting a jump every time `far` improves (that counts too many).
- Returning `jumps + 1` or starting `jumps` at 1 without handling length 1.
- Forgetting `max`: `far = i + nums[i]` loses a better earlier reach.

### Q14 ⭐⭐⭐ 🟡 Gas station on a circle. There are n stations in a circle (1 <= n <= 10^5); `gas[i]` is the fuel at station i and `cost[i]` the fuel needed to drive from i to i+1 (mod n); the tank is empty at the start and unlimited. Return the smallest starting index from which you can complete one full lap clockwise (arriving at a station with exactly 0 fuel is fine), or -1 if no start works. Give the O(n) one-pass greedy (if total gas < total cost return -1; otherwise reset the candidate to i + 1 whenever the running tank goes negative) and prove it with the two facts: a failure at j from start s means every station between s and j also fails, and total gas >= total cost implies a start exists. Note that some formulations promise a unique answer; for general input it is not unique (for example gas = [1, 1], cost = [1, 1] works from both stations), which is why this prompt asks for the smallest index. Example: gas=[1, 2, 3, 4, 5], cost=[3, 4, 5, 1, 2] -> 3; gas=[2, 3, 4], cost=[3, 4, 3] -> -1; gas=[1, 1], cost=[1, 1] -> 0; gas=[5], cost=[4] -> 0.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** One-pass greedy with a reset: the running tank decides when a start candidate is dead.

**Say this first (1 line):** "If total gas is less than total cost, answer -1. Otherwise I walk once keeping a tank; whenever the tank goes negative, the start was wrong, and everything up to here is wrong too, so the new candidate is the next station."

**Brute force:**
- Try every start, simulate the lap, stop at the first start that never goes negative.
- O(n^2): a lap costs n and there are n starts. With n up to 10^5 that is 10^10, too slow.

**Optimal:**
- `if sum(gas) < sum(cost): return -1`.
- `tank = 0; start = 0`. For `i` in `0..n-1`: `tank += gas[i] - cost[i]`. If `tank < 0`: `start = i + 1`, `tank = 0`.
- Return `start`.
- Proof, two facts (both checked by the code on thousands of random circuits):
  1. **Failure fact.** Say the trip from `s` first goes negative at `j`. Then every station `k` between `s` and `j` also fails. Reason: the tank on reaching `k` from `s` was >= 0, so starting fresh at `k` has no more fuel than coming from `s`, and it still goes negative at `j`. So after a reset we can skip all of `s..j` at once, not just `s`.
  2. **Existence fact.** If total gas >= total cost, some start works. Reason: take the final candidate `start`. The pass proved the stretch `start..n-1` never goes negative. The sum of all legs is >= 0, and the stretches before `start` summed to a negative amount (each reset segment ended negative), so the stretch `start..n-1` has a surplus that covers the whole wrap-around part `0..start-1`.
- Smallest index: the greedy result is the smallest valid start. By the failure fact every station before the final `start` fails, so nothing smaller works. The brute force (first valid start in order) agrees on all 69,904 exhaustive inputs below.
- Not unique in general: `gas = [1, 1]`, `cost = [1, 1]` works from 0 and 1. Of the 69,904 small inputs, 30,940 have two or more valid starts, which is why this prompt asks for the smallest. The prompt that promises a unique answer is a different, narrower problem.

**Complexity:** Time O(n), one pass plus the two sums. Space O(1).

**Dry run:** `gas=[1,2,3,4,5]`, `cost=[3,4,5,1,2]`. Total gas 15, total cost 15, so go on.
| i | gas-cost | tank | action |
|---|---|---|---|
| 0 | -2 | -2 | negative, start = 1, tank = 0 |
| 1 | -2 | -2 | negative, start = 2, tank = 0 |
| 2 | -2 | -2 | negative, start = 3, tank = 0 |
| 3 | +3 | 3 | ok |
| 4 | +3 | 6 | ok |

Return 3. Check by hand: from 3 the tank goes 4-1=3, 3+5-2=6, 6+1-3=4, 4+2-4=2, 2+3-5=0. Never negative, ends at exactly 0, which is allowed.

**Code:**
```python
import random
import itertools

random.seed(14)

def gas_greedy(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    tank = 0
    start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                         # cannot get from start to i + 1
            start = i + 1                    # so no station in start..i works
            tank = 0
    return start

def completes(gas, cost, s):
    t = 0
    n = len(gas)
    for k in range(n):
        i = (s + k) % n
        t += gas[i] - cost[i]
        if t < 0:
            return False
    return True

def gas_brute(gas, cost):                    # O(n^2): try every start in order
    for s in range(len(gas)):
        if completes(gas, cost, s):
            return s
    return -1

cases = [
    ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3),
    ([2, 3, 4], [3, 4, 3], -1),
    ([1, 1], [1, 1], 0),
    ([5], [4], 0),
]
for gas, cost, exp in cases:
    assert gas_greedy(gas, cost) == gas_brute(gas, cost) == exp
    print('gas =', gas, 'cost =', cost, '->', gas_greedy(gas, cost))

# exhaustive: every gas and cost list with n 1..4 and values 0..3
total = multi = 0
for n in range(1, 5):
    for gas in itertools.product(range(4), repeat=n):
        for cost in itertools.product(range(4), repeat=n):
            g = gas_greedy(gas, cost)
            assert g == gas_brute(gas, cost), (gas, cost)
            total += 1
            if sum(completes(gas, cost, s) for s in range(n)) > 1:
                multi += 1
print('exhaustive ok:', total, 'inputs; with 2 or more valid starts:', multi)

for _ in range(2000):
    n = random.randint(1, 12)
    gas = [random.randint(0, 6) for _ in range(n)]
    cost = [random.randint(0, 6) for _ in range(n)]
    assert gas_greedy(gas, cost) == gas_brute(gas, cost)
print('random ok: 2000 inputs')

# fact 1: if a trip from s first fails at j, every station k in s..j also fails
facts = 0
for _ in range(3000):
    n = random.randint(2, 8)
    gas = [random.randint(0, 5) for _ in range(n)]
    cost = [random.randint(0, 5) for _ in range(n)]
    for s in range(n):
        t = 0
        for k in range(n):
            i = (s + k) % n
            t += gas[i] - cost[i]
            if t < 0:
                # failure at offset k: stations s, s+1, ..., s+k (mod n) all fail
                for m in range(k + 1):
                    assert not completes(gas, cost, (s + m) % n)
                facts += 1
                break
print('fact 1 checked on', facts, 'failing starts')

# fact 2: sum(gas) >= sum(cost) implies some start exists
for _ in range(3000):
    n = random.randint(1, 8)
    gas = [random.randint(0, 5) for _ in range(n)]
    cost = [random.randint(0, 5) for _ in range(n)]
    if sum(gas) >= sum(cost):
        assert gas_brute(gas, cost) != -1
    else:
        assert gas_brute(gas, cost) == -1
print('fact 2 ok: total gas >= total cost iff a start exists')

# edge cases
assert gas_greedy([0], [0]) == 0
assert gas_greedy([0, 0, 5], [0, 0, 5]) == 0     # zero-cost legs
assert gas_greedy([3, 1, 1], [1, 2, 2]) == 0
assert gas_greedy([1, 1, 1, 10], [2, 2, 2, 2]) == 3
big_n = 10 ** 5
assert gas_greedy([1] * big_n, [1] * big_n) == 0
assert gas_greedy([0] * (big_n - 1) + [big_n], [1] * big_n) == big_n - 1
print('edge cases ok')
```

**Output (my run):**
```
gas = [1, 2, 3, 4, 5] cost = [3, 4, 5, 1, 2] -> 3
gas = [2, 3, 4] cost = [3, 4, 3] -> -1
gas = [1, 1] cost = [1, 1] -> 0
gas = [5] cost = [4] -> 0
exhaustive ok: 69904 inputs; with 2 or more valid starts: 30940
random ok: 2000 inputs
fact 1 checked on 10367 failing starts
fact 2 ok: total gas >= total cost iff a start exists
edge cases ok
```

**Edge cases:**
- One station: `gas=[5], cost=[4]` is 0; `gas=[3], cost=[4]` is -1 (total check).
- Zero-cost legs and zero gas: `[0], [0]` is 0.
- Arriving with exactly 0 fuel is allowed: the test is `tank < 0`, not `tank <= 0`.
- All equal (`[1]*n`, `[1]*n`): returns 0, the smallest of n valid starts.
- n = 10^5: iterative, one pass, fine.

**Follow-ups:**
- Why is the total check needed? Without it the loop returns a candidate that fails on the wrap-around part.
- Unique-answer wording? If the statement guarantees uniqueness, the same code returns it; do not rely on the guarantee for general input.
- Return all valid starts? Then use prefix sums on the doubled array with a sliding-window minimum (a monotonic deque, as in Part 2 Q16); the one-pass trick only finds one.

**Common mistakes:**
- Resetting `start = i` instead of `i + 1`.
- Forgetting the total check and returning `start` for an impossible circuit.
- Using `tank <= 0` to reset (rejects exact-zero arrivals).
- Resetting only the one failing start and re-simulating (quadratic again).

### Q15 ⭐⭐⭐ 🟡 Reorganize string. Given a string `s` of lowercase letters (1 <= len <= 500), rearrange its characters so that no two adjacent characters are equal, and return the result, or the empty string if that is impossible. Several answers can be valid, and the checker accepts any rearrangement that is a permutation of `s` with no equal neighbours (and requires '' exactly when none exists); the examples show one accepted answer. Give the max-heap solution (pop the most frequent letter, hold it back one step) and the closed condition for feasibility, max_count <= (len + 1) // 2, with a short proof of necessity (an arrangement of length L has at most ceil(L / 2) slots for any one letter). Example: s='aab' -> 'aba'; s='aaab' -> ''; s='vvvlo' -> 'vlvov'; s='a' -> 'a'; s='aabbcc' -> 'abcabc'.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Max-heap of counts with a one-step hold-back (always place the most frequent letter that is not the one just placed).

**Say this first (1 line):** "First the quick test: if the most frequent letter appears more than (len + 1) // 2 times, it is impossible. Otherwise I use a max-heap of (count, letter), pop the biggest, place it, hold it back for one step, and push it back after the next placement."

**Brute force:**
- Try all distinct permutations and keep one with no equal neighbours. That is up to n! permutations. I use it for strings of length up to 7 as the oracle (also to prove the feasibility test is exact).

**Optimal:**
- Count letters. If `max_count > (len + 1) // 2` return `''`.
- Heap of `(-count, letter)`. Loop: pop the top, append its letter, decrement its count. If a letter was held from the last step, push it back now. If the popped letter still has copies, hold it (do not push yet).
- The hold-back is what guarantees no equal neighbours: the letter just used is not in the heap on the next pop.
- Necessity: a letter with count c in a string of length L needs c positions with no two adjacent. At most ceil(L/2) = (L+1)//2 positions can be pairwise non-adjacent, so c <= (L+1)//2.
- Sufficiency (sketch): taking the most frequent letter keeps the invariant "max remaining count <= ceil(remaining / 2)". The code checks the claim exhaustively on every string of length <= 7 over 'abc' (the heap alone never fails when the condition holds).
- Several answers are valid. I wrote my own checker: any permutation of `s` with no equal neighbours, and `''` exactly when brute force says none exists. The heap happens to return the same strings the prompt shows.
- **heapq tie-breaking:** the heap holds tuples `(-count, letter)`. Equal counts fall through to the letter, so ties are broken alphabetically and never raise. If the payload were something unorderable (a dict), two equal counts would raise `TypeError`; the code shows it.

**Complexity:** Time O(n log k), k = distinct letters (at most 26), so O(n) in practice. Space O(k).

**Dry run:** `s = 'aab'`. Counts a:2, b:1. Test: 2 <= (3+1)//2 = 2, fine. Heap `[(-2,'a'), (-1,'b')]`.
- Pop `(-2,'a')`: out `a`; count becomes -1, held `(-1,'a')`.
- Pop `(-1,'b')`: out `ab`; count 0, nothing held; push back held `(-1,'a')`.
- Pop `(-1,'a')`: out `aba`; count 0.
Result `aba`.

**Code:**
```python
import heapq
import itertools
import random
from collections import Counter

random.seed(15)

def reorganize(s):
    cnt = Counter(s)
    if max(cnt.values()) > (len(s) + 1) // 2:         # closed feasibility test
        return ''
    heap = [(-c, ch) for ch, c in cnt.items()]         # (negated count, letter): ties on count compare letters
    heapq.heapify(heap)
    out = []
    held = None                                        # last letter used, held back one step
    while heap or held:
        if not heap:                                   # cannot happen when feasible
            return ''
        neg, ch = heapq.heappop(heap)
        out.append(ch)
        neg += 1                                       # one copy used (counts are negative)
        if held:
            heapq.heappush(heap, held)                 # the letter held last step may be used again
            held = None
        if neg:
            held = (neg, ch)
    return ''.join(out)

def reorganize_heap_only(s):                           # same heap logic, without the closed test
    cnt = Counter(s)
    heap = [(-c, ch) for ch, c in cnt.items()]
    heapq.heapify(heap)
    out, held = [], None
    while heap:
        neg, ch = heapq.heappop(heap)
        out.append(ch)
        neg += 1
        if held:
            heapq.heappush(heap, held)
            held = None
        if neg:
            held = (neg, ch)
    return ''.join(out) if len(out) == len(s) else ''

def valid(s, got):
    """Own checker: any permutation of s with no equal neighbours; '' exactly when none exists."""
    if got == '':
        return not exists_arrangement(s)
    return sorted(got) == sorted(s) and all(a != b for a, b in zip(got, got[1:]))

def exists_arrangement(s):                             # brute force over distinct permutations (small s)
    return any(all(a != b for a, b in zip(p, p[1:])) for p in set(itertools.permutations(s)))

for s, accepted in [('aab', 'aba'), ('aaab', ''), ('vvvlo', None), ('a', 'a'), ('aabbcc', None)]:
    got = reorganize(s)
    assert valid(s, got), (s, got)
    if accepted is not None and accepted in ('', 'aba', 'a'):
        assert got == accepted
    print(repr(s), '->', repr(got))

# exhaustive: all strings over 'abc' of length 1..7 (3+9+...+2187 = 3279 strings), brute-force feasibility
checked = infeasible = 0
for n in range(1, 8):
    for t in itertools.product('abc', repeat=n):
        s = ''.join(t)
        got = reorganize(s)
        feasible = max(Counter(s).values()) <= (n + 1) // 2
        assert feasible == exists_arrangement(s), s     # the closed condition is exact
        assert (got != '') == feasible and valid(s, got), (s, got)
        assert reorganize_heap_only(s) == got           # the heap alone already finds it whenever feasible
        checked += 1
        infeasible += not feasible
print('exhaustive ok:', checked, 'strings; infeasible:', infeasible)

for _ in range(300):
    s = ''.join(random.choice('abcdefg') for _ in range(random.randint(1, 200)))
    got = reorganize(s)
    assert valid(s, got) if got else max(Counter(s).values()) > (len(s) + 1) // 2
print('random ok: 300 strings up to length 200')

# heapq tie-breaking: tuples compare element by element
h = [(-2, 'b'), (-2, 'a'), (-1, 'z')]
heapq.heapify(h)
print('ties on count break by letter:', heapq.heappop(h))       # (-2, 'a')
# a tuple whose second item cannot be ordered raises TypeError as soon as the counts tie
try:
    bad = []
    heapq.heappush(bad, (-2, {'x': 1}))
    heapq.heappush(bad, (-2, {'y': 2}))
    print('no error (unexpected)')
except TypeError as e:
    print('TypeError on tied count with dict payload:', e)
heapq.heappush(bad, (-3, {'z': 3}))                              # different counts never reach the payload
print('heap of 3 after a distinct count:', len(bad))

# edge cases
assert reorganize('a') == 'a'
assert reorganize('aa') == ''
assert reorganize('ab') in ('ab', 'ba')
assert reorganize('aaabb') == 'ababa'
assert reorganize('a' * 250 + 'b' * 250) != '' and valid('a' * 250 + 'b' * 250, reorganize('a' * 250 + 'b' * 250))
assert reorganize('a' * 251 + 'b' * 249) == ''
print('edge cases ok')
```

**Output (my run):**
```
'aab' -> 'aba'
'aaab' -> ''
'vvvlo' -> 'vlvov'
'a' -> 'a'
'aabbcc' -> 'abcabc'
exhaustive ok: 3279 strings; infeasible: 582
random ok: 300 strings up to length 200
ties on count break by letter: (-2, 'a')
TypeError on tied count with dict payload: '<' not supported between instances of 'dict' and 'dict'
heap of 3 after a distinct count: 3
edge cases ok
```

**Edge cases:**
- `'a'` gives `'a'`. `'aa'` gives `''`.
- Exactly at the limit: 250 a + 250 b is feasible; 251 a + 249 b is not (251 > 250).
- Odd length with one dominant letter: `'aaabb'` -> `'ababa'`, the only arrangement.
- All distinct letters: any order works.

**Follow-ups:**
- Same letters must be at least k apart? Hold each used letter for k steps with a queue (the cooldown pattern from Q11 in this part, and k-distance rearrange).
- O(n) without a heap? Sort letters by frequency and fill even indices first, then odd indices.
- Return the lexicographically smallest valid answer? The plain heap is not enough; you need a feasibility check at each step.

**Common mistakes:**
- Pushing the popped letter straight back (equal neighbours).
- Skipping the feasibility test and returning a short string.
- Using the count alone as the heap item with letters in a dict (ties then compare dicts: TypeError).
- Forgetting heapq is a min-heap: store negative counts.

### Q16 ⭐⭐⭐ 🟡 Non-overlapping intervals (fewest removals). Intervals are half-open [start, end) with start < end, so [1, 2) and [2, 3) do not overlap. Given `intervals` (1 <= len <= 10^5, values in [-5*10^4, 5*10^4]), return the minimum number of intervals to remove so that the rest are pairwise non-overlapping. Sort by END time and keep an interval whenever its start is >= the last kept end (the earliest-finish greedy); give the exchange argument in two lines, show a counter-example for sorting by start time, and say why the answer equals len minus the activity-selection maximum. Example: intervals=[[1, 2], [2, 3], [3, 4], [1, 3]] -> 1; intervals=[[1, 2], [1, 2], [1, 2]] -> 2; intervals=[[1, 2], [2, 3]] -> 0; intervals=[[1, 100], [11, 22], [1, 11], [2, 12]] -> 2.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Interval pattern guides on techinterview.org (merge, insert, meeting rooms, employee free time, interval scheduling; search snippets only, not opened; the site's own 'asked at' lists were not verified) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval scheduling (activity selection): sort by end time, keep whatever fits. Greedy with an exchange argument.

**Say this first (1 line):** "Removals equal n minus the biggest set of non-overlapping intervals. I sort by END and keep an interval whenever its start is at least the last kept end; the one that finishes earliest leaves the most room."

**Brute force:**
- Try every subset, keep those with no overlapping pair, take the biggest. O(2^n * n^2). Fine as an oracle for n <= 10, useless beyond.

**Optimal:**
- Sort by end. `last_end = None`. For each `(s, e)`: if `last_end is None or s >= last_end`, keep it and set `last_end = e`. Otherwise count a removal.
- `s >= last_end` (not `>`) because intervals are half-open: `[1, 2)` and `[2, 3)` do not overlap.
- **Exchange argument (two lines):** take any optimal solution and swap its first interval for the one with the earliest end. It ends no later, so everything else in the solution still fits. So an optimal solution exists that starts with the earliest-ending interval; repeat on the rest.
- **Why the answer is n minus the activity-selection maximum:** a set can be kept without conflicts exactly when it is pairwise non-overlapping. Removing the fewest means keeping the most, so removals = n - max kept.
- **Counter-example for sorting by start:** `[[1, 10], [2, 3], [4, 5]]`. By start you keep `[1, 10]` first and must remove the other two (2 removals). The right answer is 1: drop `[1, 10]`, keep the two small ones. The code finds 8 such failing triples among small inputs (and the end-sorted greedy matches brute force on all of them).
- Ties in the end value do not matter (checked: reversing input order never changes the count).

**Complexity:** Time O(n log n) for the sort, O(n) for the scan. Space O(n) for the sorted copy (O(1) extra if sorted in place).

**Dry run:** `[[1, 100], [11, 22], [1, 11], [2, 12]]`. Sorted by end: `[1,11] [2,12] [11,22] [1,100]`.
- `[1,11]`: first, keep, `last_end = 11`.
- `[2,12]`: 2 < 11, remove (1).
- `[11,22]`: 11 >= 11, keep, `last_end = 22`.
- `[1,100]`: 1 < 22, remove (2).
Answer 2.

**Code:**
```python
import itertools
import random

random.seed(16)

def erase_overlap(intervals):                          # sort by END, keep when start >= last kept end
    kept = 0
    last_end = None
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if last_end is None or s >= last_end:          # half-open: touching is fine
            kept += 1
            last_end = e
    return len(intervals) - kept

def max_non_overlapping(intervals):                    # activity selection size
    return len(intervals) - erase_overlap(intervals)

def overlap(a, b):                                     # half-open [s, e)
    return a[0] < b[1] and b[0] < a[1]

def brute(intervals):                                  # try every subset (n <= 10)
    n = len(intervals)
    best = 0
    for mask in range(1 << n):
        sel = [intervals[i] for i in range(n) if mask >> i & 1]
        if all(not overlap(a, b) for a, b in itertools.combinations(sel, 2)):
            best = max(best, len(sel))
    return n - best

def by_start(intervals):                               # WRONG greedy: sort by start
    kept = 0
    last_end = None
    for s, e in sorted(intervals):
        if last_end is None or s >= last_end:
            kept += 1
            last_end = e
    return len(intervals) - kept

for iv, exp in [([[1, 2], [2, 3], [3, 4], [1, 3]], 1), ([[1, 2], [1, 2], [1, 2]], 2),
                ([[1, 2], [2, 3]], 0), ([[1, 100], [11, 22], [1, 11], [2, 12]], 2)]:
    assert erase_overlap(iv) == brute(iv) == exp
    print(iv, '->', erase_overlap(iv))

# exhaustive: all multisets of up to 4 intervals with endpoints in 0..4 (10 possible intervals)
pool = [[a, b] for a in range(5) for b in range(a + 1, 5)]
cnt = 0
for k in range(1, 5):
    for combo in itertools.combinations_with_replacement(pool, k):
        iv = [list(x) for x in combo]
        assert erase_overlap(iv) == brute(iv), iv
        assert erase_overlap(iv[::-1]) == erase_overlap(iv)          # input order does not matter
        cnt += 1
print('exhaustive ok:', cnt, 'multisets')

for _ in range(500):
    n = random.randint(1, 10)
    iv = []
    for _ in range(n):
        a = random.randint(-8, 8)
        iv.append([a, random.randint(a + 1, a + 6)])
    assert erase_overlap(iv) == brute(iv)
    assert max_non_overlapping(iv) == len(iv) - brute(iv)
print('random ok: 500 inputs')

# counter-example for sort-by-start
cx = [[1, 10], [2, 3], [4, 5]]
print('sort by start on', cx, '->', by_start(cx), '(wrong); by end ->', erase_overlap(cx), '; brute ->', brute(cx))
assert by_start(cx) == 2 and erase_overlap(cx) == 1 == brute(cx)
bad = 0
for combo in itertools.combinations_with_replacement(pool, 3):
    iv = [list(x) for x in combo]
    bad += by_start(iv) != erase_overlap(iv)
print('3-interval multisets where sort-by-start is wrong:', bad)
assert bad > 0

# edge cases and a large input
assert erase_overlap([[0, 1]]) == 0
assert erase_overlap([[-50000, 50000], [-50000, -49999]]) == 1
assert erase_overlap([[1, 2], [2, 3], [3, 4]]) == 0               # touching endpoints do not overlap
assert erase_overlap([[1, 3], [1, 3]]) == 1
big = [[i, i + 2] for i in range(-50000, 49998)]                  # chain of overlaps, n about 10^5
assert erase_overlap(big) == len(big) - ((len(big) + 1) // 2)
print('edge cases ok; big n =', len(big))
```

**Output (my run):**
```
[[1, 2], [2, 3], [3, 4], [1, 3]] -> 1
[[1, 2], [1, 2], [1, 2]] -> 2
[[1, 2], [2, 3]] -> 0
[[1, 100], [11, 22], [1, 11], [2, 12]] -> 2
exhaustive ok: 1000 multisets
random ok: 500 inputs
sort by start on [[1, 10], [2, 3], [4, 5]] -> 2 (wrong); by end -> 1 ; brute -> 1
3-interval multisets where sort-by-start is wrong: 8
edge cases ok; big n = 99998
```

**Edge cases:**
- One interval: 0 removals.
- Identical intervals: `[[1,2]] * 3` keeps one, removes 2.
- Touching intervals `[1,2),[2,3)`: 0 removals. If the statement made them closed, the test becomes `s > last_end`; always ask.
- Values at the extremes (-50000, 50000): no overflow in Python; a language with fixed ints needs care only if you subtract.
- A chain of ~10^5 overlapping intervals: the answer is len minus ceil(len / 2), checked in the code.

**Follow-ups:**
- Minimum rooms needed instead? That is meeting rooms II (heap of end times or a sweep).
- Weighted intervals (maximise total value)? Greedy fails; sort by end and use DP with binary search (Parts 10-11).
- Minimum arrows to burst balloons? Q21 in this part: same sort by end, closed intervals.

**Common mistakes:**
- Sorting by start (the counter-example above) or by length.
- `s > last_end` for half-open intervals (counts touching as overlapping).
- Counting kept intervals and forgetting to subtract from n.
- Mutating the caller's list with `intervals.sort()` when the caller still needs the order.

### Q17 ⭐⭐⭐ 🔴 Median of a data stream. Maintain a running median: process `adds` (1 <= len <= 10^5, integers in [-10^6, 10^6]) one value at a time and return the list of medians after each insertion as floats (the middle value when the count is odd, the mean of the two middle values when it is even, so [1, 2] gives 1.5). Use two heaps, a max-heap `lo` (negated values) for the smaller half and a min-heap `hi` for the larger half, keep the invariant len(lo) == len(hi) or len(lo) == len(hi) + 1, and describe the push-then-rebalance step that keeps every element of lo <= every element of hi. State the cost (O(log n) per add, O(1) per median query) and compare with keeping a sorted list and using bisect.insort (O(n) per insert because of the memmove, but fast for small n). Example: adds=[1, 2, 3] -> [1.0, 1.5, 2.0]; adds=[5, 15, 1, 3] -> [5.0, 10.0, 5.0, 4.0]; adds=[-1, -2, -3, -4, -5] -> [-1.0, -1.5, -2.0, -2.5, -3.0]; adds=[2, 2, 2, 2] -> [2.0, 2.0, 2.0, 2.0]; adds=[7] -> [7.0].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two heaps split the data at the median: a max-heap for the lower half, a min-heap for the upper half.

**Say this first (1 line):** "I keep the smaller half in a max-heap `lo` (negated, since heapq is a min-heap) and the larger half in a min-heap `hi`, sized so `lo` has the same count as `hi` or one more. The median is the top of `lo` or the mean of the two tops."

**Brute force:**
- Re-sort the whole prefix after every add and read the middle: O(n^2 log n) over the stream. Used as the oracle.
- Better baseline: keep one sorted list and `bisect.insort`. Finding the spot is O(log n), but the insert shifts elements (a memmove), so each add is O(n). The memmove is fast in C, so this is fine for small n and often wins in practice up to a few tens of thousands, but it is O(n^2) overall.

**Optimal:**
- Invariants: (1) `len(lo) == len(hi)` or `len(lo) == len(hi) + 1`; (2) every element of `lo` <= every element of `hi`.
- **Push-then-rebalance step** for each `x`:
  1. push `-x` onto `lo`;
  2. pop the max of `lo` and push it onto `hi` (this guarantees invariant 2, whichever half `x` belonged to);
  3. if `hi` now has more than `lo`, move `hi`'s min back to `lo` (restores invariant 1).
- Median: odd count, `-lo[0]` as a float; even count, `(-lo[0] + hi[0]) / 2`, which Python makes a float (so `[1, 2]` gives 1.5).
- Why correct: after step 2 the smaller half plus the new element is split by the max, so no element of `hi` is smaller than any in `lo`. Step 3 only moves one boundary element across, which keeps the order between halves.
- Ties and heapq: the heaps hold plain ints, so equal values never raise. The negation trick on ints is exact (no precision issue).

**Complexity:** Each add is a constant number of heap operations: O(log n). Median query O(1). Total O(n log n) for n adds. Space O(n).

**Dry run:** `[5, 15, 1, 3]`.
| x | lo (real values) | hi | median |
|---|---|---|---|
| 5 | {5} | {} | 5.0 |
| 15 | {5} | {15} | (5 + 15) / 2 = 10.0 |
| 1 | {5, 1} | {15} | 5.0 |
| 3 | {3, 1} | {5, 15} | (3 + 5) / 2 = 4.0 |

For x = 3: push into `lo` giving {5, 3, 1}, move the max 5 to `hi` giving {5, 15}, sizes 2 and 2, so no rebalance.

**Code:**
```python
import bisect
import heapq
import random

random.seed(17)

def running_median(adds):
    lo = []                                  # max-heap of the smaller half, stored negated
    hi = []                                  # min-heap of the larger half
    out = []
    for x in adds:
        heapq.heappush(lo, -x)               # 1. push into lo
        heapq.heappush(hi, -heapq.heappop(lo))   # 2. move lo's max to hi so every lo <= every hi
        if len(hi) > len(lo):                # 3. rebalance: lo may have at most one extra
            heapq.heappush(lo, -heapq.heappop(hi))
        if len(lo) > len(hi):
            out.append(float(-lo[0]))        # odd count: the top of lo
        else:
            out.append((-lo[0] + hi[0]) / 2) # even count: mean of the two tops
    return out

def median_insort(adds):                     # sorted list + bisect.insort: O(n) per insert (memmove)
    a = []
    out = []
    for x in adds:
        bisect.insort(a, x)
        m = len(a)
        out.append(float(a[m // 2]) if m % 2 else (a[m // 2 - 1] + a[m // 2]) / 2)
    return out

def median_brute(adds):                      # re-sort the whole prefix each time, O(n^2 log n)
    out = []
    for i in range(1, len(adds) + 1):
        s = sorted(adds[:i])
        m = len(s)
        out.append(float(s[m // 2]) if m % 2 else (s[m // 2 - 1] + s[m // 2]) / 2)
    return out

for adds, exp in [([1, 2, 3], [1.0, 1.5, 2.0]), ([5, 15, 1, 3], [5.0, 10.0, 5.0, 4.0]),
                  ([-1, -2, -3, -4, -5], [-1.0, -1.5, -2.0, -2.5, -3.0]),
                  ([2, 2, 2, 2], [2.0, 2.0, 2.0, 2.0]), ([7], [7.0])]:
    assert running_median(adds) == median_insort(adds) == median_brute(adds) == exp
    print(adds, '->', running_median(adds))

for _ in range(1000):
    adds = [random.randint(-9, 9) for _ in range(random.randint(1, 25))]
    assert running_median(adds) == median_brute(adds), adds
print('random ok: 1000 small streams (many duplicates)')

for _ in range(20):
    adds = [random.randint(-10 ** 6, 10 ** 6) for _ in range(random.randint(100, 400))]
    assert running_median(adds) == median_insort(adds) == median_brute(adds)
print('random ok: 20 streams of 100-400 values in [-10^6, 10^6]')

# invariant check after every step: len(lo) == len(hi) or len(lo) == len(hi) + 1, and max(lo) <= min(hi)
lo, hi = [], []
for x in [random.randint(-50, 50) for _ in range(2000)]:
    heapq.heappush(lo, -x)
    heapq.heappush(hi, -heapq.heappop(lo))
    if len(hi) > len(lo):
        heapq.heappush(lo, -heapq.heappop(hi))
    assert len(lo) in (len(hi), len(hi) + 1)
    assert not hi or -lo[0] <= hi[0]
print('invariant holds for 2000 steps')

# edge cases: sorted, reverse sorted, all equal, extremes, mean of two extremes
assert running_median([1, 2]) == [1.0, 1.5]
assert running_median([-10 ** 6, 10 ** 6]) == [-1000000.0, 0.0]
assert running_median([10 ** 6, 10 ** 6 - 1]) == [1000000.0, 999999.5]
n = 20000
up = list(range(n))
assert running_median(up) == median_insort(up)
assert running_median(up[::-1]) == median_insort(up[::-1])
assert running_median([3] * n) == [3.0] * n
big = [random.randint(-10 ** 6, 10 ** 6) for _ in range(10 ** 5)]       # max size, iterative
res = running_median(big)
assert len(res) == 10 ** 5 and res[-1] == median_insort(big)[-1]
print('edge cases ok; n = 10^5 done')
```

**Output (my run):**
```
[1, 2, 3] -> [1.0, 1.5, 2.0]
[5, 15, 1, 3] -> [5.0, 10.0, 5.0, 4.0]
[-1, -2, -3, -4, -5] -> [-1.0, -1.5, -2.0, -2.5, -3.0]
[2, 2, 2, 2] -> [2.0, 2.0, 2.0, 2.0]
[7] -> [7.0]
random ok: 1000 small streams (many duplicates)
random ok: 20 streams of 100-400 values in [-10^6, 10^6]
invariant holds for 2000 steps
edge cases ok; n = 10^5 done
```

**Edge cases:**
- One value: median is that value as a float. Two values: their mean (`[1, 2]` -> 1.5).
- Duplicates (`[2, 2, 2, 2]`): fine, comparisons use `<=` across halves.
- Negatives: negation works, and `-lo[0]` restores them.
- Mean of the extremes `-10^6` and `10^6` is 0.0; values up to 10^6 mean the float mean of two ints is exact.
- Sorted or reverse-sorted input of 20,000 values, and 10^5 random values: the heaps stay balanced; the code is iterative.

**Follow-ups:**
- Sliding-window median? Two heaps plus lazy deletion (or a sorted container); each removal is marked and cleaned when it surfaces at a top.
- Median of values in a small known range? A counting array and a pointer, O(1) per query.
- Percentile other than 50? Same idea with unequal target sizes.
- Memory too large for all values? Use a quantile sketch; two heaps need all n values.

**Common mistakes:**
- Forgetting to negate when popping from `lo` (returns the min of the lower half).
- Pushing to the "right" heap by comparing with the current median; the push-pop-rebalance version avoids that case analysis.
- Integer division for the even case (returns 1 for `[1, 2]`).
- Breaking invariant 1 by rebalancing in the wrong direction (the extra element must sit in `lo`).

### Q18 ⭐⭐ 🟢 Last stone weight. `stones` holds positive integers (1 <= len <= 30, each <= 1000). Repeatedly take the two heaviest stones; if they are equal both are destroyed, otherwise the lighter is destroyed and the heavier becomes the difference. Return the weight of the last stone, or 0 if none is left. Show the max-heap via negation (heapq has no max-heap), say what happens with a single stone, and state the cost (O(n log n)). Example: stones=[2, 7, 4, 1, 8, 1] -> 1; stones=[1] -> 1; stones=[3, 3] -> 0; stones=[10, 4, 2, 10] -> 2.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Repeatedly take the largest items: a max-heap, which in Python means a min-heap of negated values.

**Say this first (1 line):** "heapq only has a min-heap, so I store negatives. Pop twice, push back the difference if it is not zero, and stop when one or zero stones remain."

**Brute force:**
- Sort, pop the two largest, put the difference back, sort again. Each re-sort is O(n log n), so O(n^2 log n) in total. Fine for n <= 30 and used here as the oracle.

**Optimal:**
- `heap = [-s for s in stones]`; `heapify` (O(n)).
- While two or more stones remain: `a = -heappop`, `b = -heappop` (so `a >= b`). If `a != b`, push `-(a - b)`.
- Return `-heap[0]` if anything is left, else 0.
- Single stone: the loop never runs, the answer is that stone.
- Each round removes at least one stone (two out, at most one in), so there are at most n - 1 rounds.
- Ties: equal weights are plain ints, so comparisons never fail. If stones carried labels, a `(-weight, label)` tuple breaks ties by label (the code shows it); an unorderable label would raise `TypeError` on a tie.

**Complexity:** Time O(n log n): heapify O(n), at most n - 1 rounds each with two pops and one push at O(log n). Space O(n) for the heap.

**Dry run:** `[2, 7, 4, 1, 8, 1]`.
| round | take | push | stones left |
|---|---|---|---|
| 1 | 8, 7 | 1 | 4, 2, 1, 1, 1 |
| 2 | 4, 2 | 2 | 2, 1, 1, 1 |
| 3 | 2, 1 | 1 | 1, 1, 1 |
| 4 | 1, 1 | nothing | 1 |

Answer 1.

**Code:**
```python
import heapq
import random

random.seed(18)

def last_stone(stones):
    heap = [-s for s in stones]              # heapq is a min-heap: store negatives to get a max-heap
    heapq.heapify(heap)
    while len(heap) > 1:
        a = -heapq.heappop(heap)             # heaviest
        b = -heapq.heappop(heap)             # second heaviest, a >= b
        if a != b:
            heapq.heappush(heap, -(a - b))   # the remainder goes back
    return -heap[0] if heap else 0

def last_stone_sorted(stones):               # oracle: re-sort after each smash, O(n^2 log n)
    a = sorted(stones)
    while len(a) > 1:
        x = a.pop()
        y = a.pop()
        if x != y:
            a.append(x - y)
            a.sort()
    return a[0] if a else 0

for st, exp in [([2, 7, 4, 1, 8, 1], 1), ([1], 1), ([3, 3], 0), ([10, 4, 2, 10], 2)]:
    assert last_stone(st) == last_stone_sorted(st) == exp
    print(st, '->', last_stone(st))

for _ in range(2000):
    st = [random.randint(1, 20) for _ in range(random.randint(1, 12))]
    assert last_stone(st) == last_stone_sorted(st), st
print('random ok: 2000 inputs')

# negation trap: popping the heap without negating gives the LIGHTEST stones
h = [2, 7, 4, 1, 8, 1]
heapq.heapify(h)
print('raw min-heap pops first:', heapq.heappop(h), heapq.heappop(h), '(the two lightest, not heaviest)')

# a different, ordered-tuple view: ties between equal weights never raise, because ints are comparable
tie = [(-5, 'a'), (-5, 'b')]
heapq.heapify(tie)
print('tuple tie on weight breaks by label:', heapq.heappop(tie))

# edge cases
assert last_stone([5]) == 5
assert last_stone([1000] * 30) == 0                # 30 equal stones cancel in pairs
assert last_stone([1000] * 29) == 1000
assert last_stone([1, 1, 1]) == 1
assert last_stone([1000, 1]) == 999
assert last_stone([1, 2, 3]) == 0
print('edge cases ok')
```

**Output (my run):**
```
[2, 7, 4, 1, 8, 1] -> 1
[1] -> 1
[3, 3] -> 0
[10, 4, 2, 10] -> 2
random ok: 2000 inputs
raw min-heap pops first: 1 1 (the two lightest, not heaviest)
tuple tie on weight breaks by label: (-5, 'a')
edge cases ok
```

**Edge cases:**
- One stone: returned unchanged. Two equal stones: 0.
- An even number of equal stones cancels to 0 (30 of them), an odd number leaves one (29 give 1000).
- Remainder pushed back may be the new heaviest: `[1000, 1]` gives 999 straight away, then one stone.
- Empty result: the `else 0` branch.

**Follow-ups:**
- Stones up to 10^9 and n up to 10^5? Same heap, still O(n log n).
- Smallest two instead of largest two? Plain min-heap without negation (that is Q20's rule).
- Why not bucket sort? With weights <= 1000 a counting array works too, but the heap is simpler to explain.

**Common mistakes:**
- Using the raw min-heap and getting the lightest stones (the code prints it).
- Forgetting to negate the pushed difference.
- Pushing `0` when the stones are equal (it would later be treated as a stone).
- Returning `heap[0]` without negating it, or indexing an empty heap.

### Q19 ⭐⭐ 🟢 Assign cookies. `g[i]` is the minimum cookie size child i will accept and `s[j]` is the size of cookie j (0 <= len(g), len(s) <= 3*10^4, sizes in [1, 2^31 - 1]). Each child gets at most one cookie and each cookie goes to at most one child; a child is content when the cookie size is >= g[i]. Return the maximum number of content children. Sort both lists and walk the cookies with a pointer over the children (smallest cookie that satisfies the least greedy unmatched child), and give the exchange argument for why using the smallest sufficient cookie never hurts. Example: g=[1, 2, 3], s=[1, 1] -> 1; g=[1, 2], s=[1, 2, 3] -> 2; g=[], s=[4] -> 0; g=[5, 6], s=[1, 2] -> 0.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy matching after sorting: give each child the smallest cookie that satisfies them.

**Say this first (1 line):** "Sort both lists. Walk the cookies from smallest to largest, and keep a pointer on the least greedy unmatched child; if the cookie is big enough, that child is content and the pointer moves on."

**Brute force:**
- Try, for every child, either no cookie or each unused cookie (bitmask over cookies with memoisation). Exponential in the number of cookies; used as the oracle for lists of up to 7.

**Optimal:**
- Sort `g` and `s`. `i = 0`. For each cookie in ascending order: `if i < len(g) and g[i] <= cookie: i += 1`.
- Return `i`.
- Exchange argument: take an optimal assignment. If the least greedy child is matched with a cookie bigger than the smallest sufficient cookie (or is unmatched while that cookie is used elsewhere), swap; the cookie that was used is at least as big as needed by whoever had it, and the child needs no more than anyone else. So using the smallest sufficient cookie on the least greedy child never reduces the count.
- Cookies that are too small for the current child are useless for every other child too (they are at least as greedy), so skipping them is safe.
- Wasteful rule (biggest cookie to the least greedy child) is wrong: `g=[1,2]`, `s=[1,2]` gives 1 instead of 2. The code counts how many tiny cases differ.

**Complexity:** Time O(g log g + s log s) for the sorts plus O(s) for the walk. Space O(1) extra apart from sorted copies.

**Dry run:** `g=[1,2,3]`, `s=[1,1]`. Sorted already. Cookie 1: `g[0]=1 <= 1`, `i=1`. Cookie 1: `g[1]=2 <= 1`? No, skip. End: `i = 1`. Answer 1.

**Code:**
```python
import itertools
import random
from functools import lru_cache

random.seed(19)

def assign_cookies(g, s):
    g = sorted(g)
    s = sorted(s)
    i = 0                                    # next unmatched child (least greedy)
    for cookie in s:                         # smallest cookie first
        if i < len(g) and g[i] <= cookie:    # smallest cookie that satisfies the least greedy child
            i += 1
    return i

def brute(g, s):                             # try every cookie for every child, bitmask of used cookies
    @lru_cache(None)
    def f(i, used):
        if i == len(g):
            return 0
        best = f(i + 1, used)                # leave child i unhappy
        for j in range(len(s)):
            if not used >> j & 1 and s[j] >= g[i]:
                best = max(best, 1 + f(i + 1, used | 1 << j))
        return best
    return f(0, 0)

for g, s, exp in [([1, 2, 3], [1, 1], 1), ([1, 2], [1, 2, 3], 2), ([], [4], 0), ([5, 6], [1, 2], 0)]:
    assert assign_cookies(g, s) == brute(tuple(g), tuple(s)) == exp
    print('g =', g, 's =', s, '->', assign_cookies(g, s))

# exhaustive: lists of length 0..4 over sizes 1..4 (sizes form a tiny alphabet)
cnt = 0
for lg in range(0, 5):
    for ls in range(0, 5):
        for g in itertools.product(range(1, 5), repeat=lg):
            for s in itertools.product(range(1, 5), repeat=ls):
                assert assign_cookies(list(g), list(s)) == brute(g, s), (g, s)
                cnt += 1
print('exhaustive ok:', cnt, 'pairs')

for _ in range(1000):
    g = [random.randint(1, 8) for _ in range(random.randint(0, 7))]
    s = [random.randint(1, 8) for _ in range(random.randint(0, 7))]
    assert assign_cookies(g, s) == brute(tuple(g), tuple(s))
print('random ok: 1000 pairs')

# a wasteful rule (biggest cookie to the least greedy child) is wrong:
def wrong_biggest_cookie_to_first_child(g, s):      # gives each child (sorted ascending) the BIGGEST cookie left
    g = sorted(g)
    s = sorted(s)
    done = 0
    for c in g:
        if s and s[-1] >= c:
            s.pop()
            done += 1
    return done
bad = []
for g in itertools.product(range(1, 4), repeat=2):
    for s in itertools.product(range(1, 4), repeat=2):
        if wrong_biggest_cookie_to_first_child(list(g), list(s)) != assign_cookies(list(g), list(s)):
            bad.append((g, s))
print('wasteful rule differs from greedy on', len(bad), 'tiny cases, e.g.', bad[0] if bad else None)
assert wrong_biggest_cookie_to_first_child([1, 3], [1, 3]) == 1 and assign_cookies([1, 3], [1, 3]) == 2

# edge cases and max size
assert assign_cookies([], []) == 0
assert assign_cookies([1], []) == 0
assert assign_cookies([2 ** 31 - 1], [2 ** 31 - 1]) == 1
assert assign_cookies([1] * 30000, [1] * 30000) == 30000
assert assign_cookies([1] * 30000, [1] * 29999) == 29999
assert assign_cookies([2, 2, 2], [1, 1, 1]) == 0
print('edge cases ok')
```

**Output (my run):**
```
g = [1, 2, 3] s = [1, 1] -> 1
g = [1, 2] s = [1, 2, 3] -> 2
g = [] s = [4] -> 0
g = [5, 6] s = [1, 2] -> 0
exhaustive ok: 116281 pairs
random ok: 1000 pairs
wasteful rule differs from greedy on 20 tiny cases, e.g. ((1, 2), (1, 2))
edge cases ok
```

**Edge cases:**
- No children or no cookies: 0.
- Sizes up to 2^31 - 1: Python ints, no overflow.
- Equal sizes: a cookie equal to the greed is enough (`<=`).
- 30,000 children and 29,999 cookies of size 1: 29,999.
- Everyone too greedy: 0.

**Follow-ups:**
- Each cookie can serve several children? Different problem; think capacity.
- Minimum cookies needed to satisfy everyone? Count by sorted greed with a heap or two pointers.
- Two-pointer view from the other end (biggest cookie to the greediest child) also works, but reasoning from the least greedy side is simpler to state.

**Common mistakes:**
- Using `<` instead of `<=`.
- Not sorting one of the lists.
- Advancing the child pointer on every cookie (lets unsatisfied cookies "use up" children).
- Handing out the biggest cookie first and wasting it on a small greed.

### Q20 ⭐⭐ 🟢 Minimum cost to connect sticks. `sticks` holds positive integers (1 <= len <= 10^4, each <= 10^4). Joining two sticks of lengths a and b costs a + b and produces one stick of length a + b; repeat until one stick remains. Return the minimum total cost (0 for a single stick). Always join the two shortest sticks with a min-heap (O(n log n)); say why this is Huffman's merge rule and why joining the longest sticks first is worse (give a three-stick counter-example). Example: sticks=[2, 4, 3] -> 14; sticks=[1, 8, 3, 5] -> 30; sticks=[5] -> 0; sticks=[1, 1, 1, 1] -> 8.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Huffman merging: always combine the two smallest with a min-heap.

**Say this first (1 line):** "Every time a stick is inside a join, its length is paid again, so short sticks should be joined early (they get paid many times, but they are small) and long sticks late. A min-heap gives me the two shortest each time."

**Brute force:**
- Try every pair at every step and take the cheapest total (memoised on the sorted multiset of lengths). Exponential; used as the oracle for up to 6 sticks.

**Optimal:**
- `heapify(sticks)`; `total = 0`. While more than one stick: pop `a`, pop `b`, `total += a + b`, push `a + b`. Return `total`.
- One stick: loop never runs, 0.
- Why it is Huffman's merge rule: the joins form a binary tree whose leaves are the original sticks. A stick of length w at depth d is included in d joins, so the total cost is the sum over leaves of `w * d`. Minimising that for fixed weights is exactly the Huffman coding problem, and merging the two lightest nodes is Huffman's greedy rule. The code builds the actual merge tree and confirms the weighted depth sum equals the heap total.
- Exchange idea: in an optimal tree the two lightest leaves can be made siblings at the deepest level; merging them is then a smaller instance of the same problem.
- Longest first is worse. Counter-example `[1, 2, 3]`: shortest first costs (1+2) + (3+3) = 9; longest first costs (3+2) + (5+1) = 11. Over all 125 triples with values 1..5, longest-first loses on 120 of them.
- Heap items are plain ints here, so ties never raise. Where a tuple carries a payload, ties on the weight compare the payload; the code shows the `TypeError` for dict payloads and uses `(weight, unique_id)` in the tree builder to avoid it.

**Complexity:** Time O(n log n): heapify O(n), n - 1 rounds with two pops and one push. Space O(n).

**Dry run:** `[2, 4, 3]`.
- Pop 2 and 3, cost 5, push 5. Heap `[4, 5]`.
- Pop 4 and 5, cost 9, push 9. Heap `[9]`.
- Total 5 + 9 = 14.

**Code:**
```python
import heapq
import itertools
import random
from functools import lru_cache

random.seed(20)

def connect_sticks(sticks):
    heap = list(sticks)
    heapq.heapify(heap)                      # min-heap of lengths
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)              # two shortest
        b = heapq.heappop(heap)
        total += a + b
        heapq.heappush(heap, a + b)
    return total

def connect_longest_first(sticks):           # WRONG on purpose: join the two LONGEST
    a = sorted(sticks)
    total = 0
    while len(a) > 1:
        x = a.pop()
        y = a.pop()
        total += x + y
        a.append(x + y)
        a.sort()
    return total

def brute(sticks):                           # try every pair at every step, memoised on the sorted multiset
    @lru_cache(None)
    def f(t):
        if len(t) == 1:
            return 0
        best = 10 ** 18
        for i, j in itertools.combinations(range(len(t)), 2):
            rest = [t[k] for k in range(len(t)) if k not in (i, j)] + [t[i] + t[j]]
            best = min(best, t[i] + t[j] + f(tuple(sorted(rest))))
        return best
    return f(tuple(sorted(sticks)))

def weighted_depth(sticks):                  # build the merge tree, then sum leaf weight * leaf depth
    heap = [(w, i) for i, w in enumerate(sticks)]        # (weight, unique id): ties never reach a non-orderable item
    heapq.heapify(heap)
    kids = {}
    nxt = len(sticks)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        kids[nxt] = (a[1], b[1])
        heapq.heappush(heap, (a[0] + b[0], nxt))
        nxt += 1
    total = 0
    stack = [(heap[0][1], 0)]                            # iterative walk from the root
    while stack:
        node, d = stack.pop()
        if node in kids:
            stack.append((kids[node][0], d + 1))
            stack.append((kids[node][1], d + 1))
        else:
            total += sticks[node] * d
    return total

for st, exp in [([2, 4, 3], 14), ([1, 8, 3, 5], 30), ([5], 0), ([1, 1, 1, 1], 8)]:
    assert connect_sticks(st) == brute(st) == weighted_depth(st) == exp
    print(st, '->', connect_sticks(st))

for _ in range(1000):
    st = [random.randint(1, 9) for _ in range(random.randint(1, 6))]
    assert connect_sticks(st) == brute(st) == weighted_depth(st), st
print('random ok: 1000 inputs')

# three-stick counter-example for longest-first
cx = [1, 2, 3]
print('longest first on', cx, '->', connect_longest_first(cx), '; shortest first ->', connect_sticks(cx), '; brute ->', brute(cx))
assert connect_longest_first(cx) == 11 and connect_sticks(cx) == 9 == brute(cx)
worse = sum(connect_longest_first(list(c)) > connect_sticks(list(c)) for c in itertools.product(range(1, 6), repeat=3))
print('triples over 1..5 where longest-first costs more:', worse, 'of 125')

# the heap of tuples: equal weights tie, so the tuple needs a unique tiebreak if the payload is not orderable
try:
    h = []
    heapq.heappush(h, (3, {'name': 'x'}))
    heapq.heappush(h, (3, {'name': 'y'}))
except TypeError as e:
    print('TypeError on tied weights with dict payload:', e)

# edge cases and max size
assert connect_sticks([7]) == 0
assert connect_sticks([1, 1]) == 2
assert connect_sticks([10 ** 4] * 4) == 80000
big = [random.randint(1, 10 ** 4) for _ in range(10 ** 4)]
assert connect_sticks(big) == weighted_depth(big)
print('edge cases ok; cost for n = 10^4 random sticks:', connect_sticks(big))
```

**Output (my run):**
```
[2, 4, 3] -> 14
[1, 8, 3, 5] -> 30
[5] -> 0
[1, 1, 1, 1] -> 8
random ok: 1000 inputs
longest first on [1, 2, 3] -> 11 ; shortest first -> 9 ; brute -> 9
triples over 1..5 where longest-first costs more: 120 of 125
TypeError on tied weights with dict payload: '<' not supported between instances of 'dict' and 'dict'
edge cases ok; cost for n = 10^4 random sticks: 645453002
```

**Edge cases:**
- Single stick: 0. Two sticks: their sum.
- All equal (`[1, 1, 1, 1]`): 8 (two joins of 2, one join of 4). `[10^4] * 4` gives 80,000.
- The total can be large: n = 10^4 random sticks gives hundreds of millions; Python ints do not overflow, a 32-bit language might.
- Duplicates are fine; the heap holds ints.

**Follow-ups:**
- Print the Huffman codes? Keep a tree of nodes, add a unique id to break ties, and walk the tree iteratively.
- Why must the heap hold the merged stick again? The merged stick can be shorter than other sticks, and it must compete for the next two shortest.
- Sort once and use two queues (originals and merged, both already sorted) for O(n) after the sort.

**Common mistakes:**
- Joining the largest sticks first.
- Adding only the new stick length rather than `a + b` to the total (same value, but people sometimes add the wrong variable).
- Forgetting to push the merged stick back.
- Not heapifying (popping from an unsorted list with `min`, O(n^2)).

### Q21 ⭐⭐ 🟡 Minimum arrows to burst balloons. Each balloon is a horizontal segment [x_start, x_end] on the x axis (closed, x_start <= x_end, integers in [-2^31, 2^31 - 1], 1 <= len <= 10^5, segments may touch). An arrow shot straight up at integer x bursts every balloon with x_start <= x <= x_end. Return the minimum number of arrows. Sort by x_end and shoot at the end of the first unburst balloon; say why sorting by x_start fails, and why comparing with a subtraction such as `a[1] - b[1]` as a sort key is an overflow trap in fixed-width languages although harmless in Python. Example: points=[[10, 16], [2, 8], [1, 6], [7, 12]] -> 2; points=[[1, 2], [3, 4], [5, 6], [7, 8]] -> 4; points=[[1, 2], [2, 3], [3, 4], [4, 5]] -> 2; points=[[3, 9], [7, 12], [3, 8], [6, 8], [9, 10], [2, 9], [0, 9], [3, 9], [0, 6], [2, 8]] -> 2.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Interval pattern guides on techinterview.org (merge, insert, meeting rooms, employee free time, interval scheduling; search snippets only, not opened; the site's own 'asked at' lists were not verified) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval greedy, same family as non-overlapping intervals (Q16): sort by end, act at the end.

**Say this first (1 line):** "Sort balloons by right end. Shoot an arrow at the end of the first unburst balloon: that is as far right as it can go while still hitting it, so it hits the most following balloons. Skip every balloon that arrow already hits."

**Brute force:**
- Try sets of integer x positions of growing size until every balloon contains one. Exponential in the coordinate range; used as the oracle for small coordinates.

**Optimal:**
- Sort by end. `shot = None`, `arrows = 0`. For each `(s, e)`: if `shot is None or s > shot`, the arrow at `shot` misses it, so `arrows += 1` and `shot = e`.
- Closed segments, so `s == shot` is a hit (`[1,5]` and `[5,9]` share one arrow at 5). That is why the test is `s > shot`, not `>=`.
- Why shooting at the first balloon's END is safe: any arrow that bursts that balloon sits at some x <= e; moving it right to e keeps it inside that balloon and cannot lose any balloon whose end is >= e (all later balloons have end >= e, and they need `x >= s`, which a larger x only helps).
- Why sorting by START fails as usually written: with `[[1, 10], [2, 3], [4, 5]]` the naive start-sorted scan sets the group end to 10 and says one arrow, but 3 < 4 so no single x hits both small balloons and the big one: the answer is 2. The code shows the naive version wrong on 332 small inputs. Sorting by start only works if you also shrink the group's end to the minimum end seen (the code includes that variant and it matches), which is more state to get wrong. Sorting by end needs none of it.
- Overflow trap: a comparator written as `a[1] - b[1]` is fine in Python, where ints never overflow and sorting should use `key=lambda p: p[1]` anyway. In a language with 32-bit ints, `2**31 - 1 - (-2**31)` wraps to -1, so the comparator says the larger value is smaller and sorts wrongly. The code emulates the wrap and prints the wrong order. Compare with `<` or `Integer.compare`, never subtract.

**Complexity:** Time O(n log n) for the sort, O(n) for the scan. Space O(n) for the sorted copy.

**Dry run:** `[[10,16],[2,8],[1,6],[7,12]]`. Sorted by end: `[1,6] [2,8] [7,12] [10,16]`.
- `[1,6]`: no arrow yet, arrows 1, `shot = 6`.
- `[2,8]`: 2 <= 6, hit.
- `[7,12]`: 7 > 6, arrows 2, `shot = 12`.
- `[10,16]`: 10 <= 12, hit.
Answer 2.

**Code:**
```python
import itertools
import random
from functools import cmp_to_key

random.seed(21)

def min_arrows(points):
    arrows = 0
    shot = None                              # x of the last arrow
    for s, e in sorted(points, key=lambda p: p[1]):      # sort by END
        if shot is None or s > shot:         # the arrow at `shot` misses this balloon (touching is a hit)
            arrows += 1
            shot = e                         # new arrow at this balloon's end
    return arrows

def by_start_naive(points):                  # WRONG: sort by start, never shrink the group's end
    arrows = 0
    end = None
    for s, e in sorted(points):
        if end is None or s > end:
            arrows += 1
            end = e
    return arrows

def by_start_shrinking(points):              # correct variant: sort by start AND shrink end to the min
    arrows = 0
    end = None
    for s, e in sorted(points):
        if end is None or s > end:
            arrows += 1
            end = e
        else:
            end = min(end, e)
    return arrows

def brute(points):                           # smallest set of integer x that hits every balloon (small coordinates)
    lo = min(p[0] for p in points)
    hi = max(p[1] for p in points)
    for r in range(1, len(points) + 1):
        for xs in itertools.combinations(range(lo, hi + 1), r):
            if all(any(s <= x <= e for x in xs) for s, e in points):
                return r

for pts, exp in [([[10, 16], [2, 8], [1, 6], [7, 12]], 2), ([[1, 2], [3, 4], [5, 6], [7, 8]], 4),
                 ([[1, 2], [2, 3], [3, 4], [4, 5]], 2),
                 ([[3, 9], [7, 12], [3, 8], [6, 8], [9, 10], [2, 9], [0, 9], [3, 9], [0, 6], [2, 8]], 2)]:
    assert min_arrows(pts) == brute(pts) == exp
    print(pts, '->', min_arrows(pts))

# exhaustive: every multiset of up to 4 balloons with endpoints in 0..4 (15 possible balloons)
pool = [[a, b] for a in range(5) for b in range(a, 5)]
cnt = naive_bad = 0
for k in range(1, 5):
    for combo in itertools.combinations_with_replacement(pool, k):
        pts = [list(x) for x in combo]
        assert min_arrows(pts) == brute(pts), pts
        assert by_start_shrinking(pts) == min_arrows(pts), pts
        naive_bad += by_start_naive(pts) != min_arrows(pts)
        cnt += 1
print('exhaustive ok:', cnt, 'multisets; naive sort-by-start wrong on', naive_bad)

for _ in range(300):
    pts = []
    for _ in range(random.randint(1, 7)):
        a = random.randint(-6, 6)
        pts.append([a, random.randint(a, a + 5)])
    assert min_arrows(pts) == brute(pts)
print('random ok: 300 inputs')

cx = [[1, 10], [2, 3], [4, 5]]
print('naive sort-by-start on', cx, '->', by_start_naive(cx), '(wrong); correct ->', min_arrows(cx), '; brute ->', brute(cx))
assert by_start_naive(cx) == 1 and min_arrows(cx) == 2 == brute(cx)

# overflow trap: emulate a 32-bit signed subtraction comparator
def wrap32(x):
    return (x + 2 ** 31) % 2 ** 32 - 2 ** 31
def cmp32(a, b):
    return wrap32(a[1] - b[1])               # what a C or Java comparator `a[1] - b[1]` would compute
lo_b, hi_b = [-2 ** 31, -2 ** 31], [2 ** 31 - 1, 2 ** 31 - 1]
print('true a-b:', hi_b[1] - lo_b[1], '| 32-bit a-b:', cmp32(hi_b, lo_b), '(negative: says hi < lo, wrong order)')
bad_order = sorted([hi_b, lo_b], key=cmp_to_key(cmp32))
print('order from 32-bit subtraction comparator:', bad_order, '| correct:', sorted([hi_b, lo_b], key=lambda p: p[1]))
assert cmp32(hi_b, lo_b) < 0 and hi_b[1] - lo_b[1] > 0
big = [[-2 ** 31, 2 ** 31 - 1], [-2 ** 31, -2 ** 31], [2 ** 31 - 1, 2 ** 31 - 1]]
assert min_arrows(big) == 2                  # Python ints: no overflow; sort by key, no subtraction

# edge cases
assert min_arrows([[5, 5]]) == 1
assert min_arrows([[1, 1], [1, 1]]) == 1
assert min_arrows([[1, 5], [5, 9]]) == 1     # touching balloons share the arrow at x = 5
assert min_arrows([[i, i] for i in range(10 ** 5)]) == 10 ** 5
assert min_arrows([[0, 10 ** 9]] * 10 ** 5) == 1
print('edge cases ok')
```

**Output (my run):**
```
[[10, 16], [2, 8], [1, 6], [7, 12]] -> 2
[[1, 2], [3, 4], [5, 6], [7, 8]] -> 4
[[1, 2], [2, 3], [3, 4], [4, 5]] -> 2
[[3, 9], [7, 12], [3, 8], [6, 8], [9, 10], [2, 9], [0, 9], [3, 9], [0, 6], [2, 8]] -> 2
exhaustive ok: 3875 multisets; naive sort-by-start wrong on 332
random ok: 300 inputs
naive sort-by-start on [[1, 10], [2, 3], [4, 5]] -> 1 (wrong); correct -> 2 ; brute -> 2
true a-b: 4294967295 | 32-bit a-b: -1 (negative: says hi < lo, wrong order)
order from 32-bit subtraction comparator: [[2147483647, 2147483647], [-2147483648, -2147483648]] | correct: [[-2147483648, -2147483648], [2147483647, 2147483647]]
edge cases ok
```

**Edge cases:**
- One balloon: 1 arrow. A zero-width balloon `[5, 5]` still needs an arrow at 5.
- Touching balloons share an arrow (`[[1,2],[2,3],[3,4],[4,5]]` needs 2, not 4).
- All identical: 1. All disjoint: n (10^5 zero-width balloons gives 10^5).
- Extreme coordinates `-2^31` and `2^31 - 1`: Python handles them; the comparator subtraction is the only danger.

**Follow-ups:**
- Same as erase-overlap? Closely related: the arrows needed equal the maximum number of pairwise-disjoint balloons (for closed segments), but the code here counts groups directly.
- Arrows may only be shot at given endpoints? Same greedy (it already shoots at ends).
- Weighted or limited arrows? No longer greedy.

**Common mistakes:**
- `s >= shot` (counts touching balloons as missed).
- Sorting by start and not shrinking the group's end.
- Subtracting in the comparator (overflow in fixed-width languages).
- Setting `shot` to the start or to the previous balloon's end instead of the current balloon's end.

### Q22 ⭐⭐ 🟡 Partition labels. Given a lowercase string `s` (1 <= len <= 500), cut it into as many contiguous parts as possible so that each letter appears in at most one part, and return the list of part lengths in order. The answer is unique (the finest valid partition is unique). Record the last index of each letter, then scan keeping the farthest last index seen in the current part and cut when the scan index reaches it; say why this is greedy (each cut is made at the earliest legal place) and why it is O(n). Example: s='ababcbacadefegdehijhklij' -> [9, 7, 8]; s='eccbbbbdec' -> [10]; s='a' -> [1]; s='abc' -> [1, 1, 1].
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy with last occurrences: a part must stretch to the last copy of every letter it contains.

**Say this first (1 line):** "I record the last index of each letter. Then I scan, keep the farthest last index of anything in the current part, and cut when my index reaches that farthest point, because nothing inside still needs anything further right."

**Brute force:**
- Try every subset of the n - 1 cut positions, keep the partitions where no letter appears in two parts, take the one with most parts. O(2^n * n), fine for n <= 8 as the oracle.

**Optimal:**
- `last = {ch: i}` for the final occurrence of each letter.
- `start = end = 0`. For each `i, ch`: `end = max(end, last[ch])`. If `i == end`, the part `start..i` is closed: record `i - start + 1`, set `start = i + 1`.
- **Why it is greedy:** each cut is made at the earliest index where it is legal (no letter seen so far reappears later). Cutting earlier is impossible; cutting later can only merge parts and lower the count.
- **Why the answer is unique:** every legal cut position is forced. A cut is legal exactly when no letter spans it, and the set of legal cut positions does not depend on any choice, so the finest partition uses all of them. The code lists all valid partitions of every string over 'abc' up to length 8 (9,840 strings) and over 'abcd' up to length 7 (21,844 strings) and confirms exactly one has the most parts, and that it equals the greedy output.
- Why `i == end` is a valid test: by then the scan has seen every letter in the part, and the farthest last occurrence is `i` itself, so no letter reaches past `i`.

**Complexity:** Time O(n): one pass to build `last`, one pass to scan. Space O(1) (at most 26 letters in the dict) plus the output list.

**Dry run:** `'ababcbacadefegdehijhklij'`. Last indices: a 8, b 5, c 7, d 14, e 15, f 11, g 13, h 19, i 22, j 23, k 20, l 21.
- Indices 0 to 8: `end` reaches 8 (from 'a'), cut at i = 8, size 9.
- Indices 9 to 15: 'd' pushes `end` to 14, 'e' pushes it to 15, cut at i = 15, size 7.
- Indices 16 to 23: 'h' 19, 'i' 22, 'j' 23, cut at i = 23, size 8.
Result `[9, 7, 8]`.

**Code:**
```python
import itertools
import random

random.seed(22)

def partition_labels(s):
    last = {ch: i for i, ch in enumerate(s)}   # last index of each letter
    sizes = []
    start = end = 0                            # current part is s[start..], end = farthest last index so far
    for i, ch in enumerate(s):
        end = max(end, last[ch])               # the part must reach the last copy of every letter seen
        if i == end:                           # nothing in the part needs anything further: cut here
            sizes.append(end - start + 1)
            start = i + 1
    return sizes

def valid_cuts(s, cuts):                       # parts: cut positions strictly inside 1..n-1
    n = len(s)
    parts = [s[a:b] for a, b in zip([0] + list(cuts), list(cuts) + [n])]
    seen = set()
    for p in parts:
        letters = set(p)
        if letters & seen:
            return None
        seen |= letters
    return parts

def brute_all(s):                              # every valid partition, as a list of part-length lists
    n = len(s)
    out = []
    for r in range(n):
        for cuts in itertools.combinations(range(1, n), r):
            parts = valid_cuts(s, cuts)
            if parts is not None:
                out.append([len(p) for p in parts])
    return out

def brute_best(s):
    allp = brute_all(s)
    m = max(len(p) for p in allp)
    best = [p for p in allp if len(p) == m]
    return best

for s, exp in [('ababcbacadefegdehijhklij', [9, 7, 8]), ('eccbbbbdec', [10]), ('a', [1]), ('abc', [1, 1, 1])]:
    assert partition_labels(s) == exp
    if len(s) <= 12:
        assert brute_best(s) == [exp]
    print(repr(s), '->', partition_labels(s))

# exhaustive: all strings over 'abc' of length 1..8 (9840 strings): the finest partition is UNIQUE and equals the greedy
cnt = 0
for n in range(1, 9):
    for t in itertools.product('abc', repeat=n):
        s = ''.join(t)
        best = brute_best(s)
        assert len(best) == 1, (s, best)                  # uniqueness claim from the prompt
        assert best[0] == partition_labels(s), s
        assert sum(best[0]) == n
        cnt += 1
print('exhaustive ok:', cnt, 'strings over abc; finest partition unique every time')

# also 4 letters, length up to 7
cnt = 0
for n in range(1, 8):
    for t in itertools.product('abcd', repeat=n):
        s = ''.join(t)
        assert brute_best(s) == [partition_labels(s)], s
        cnt += 1
print('exhaustive ok:', cnt, 'strings over abcd (length <= 7)')

for _ in range(300):
    s = ''.join(random.choice('abcdefghij') for _ in range(random.randint(1, 500)))
    sizes = partition_labels(s)
    assert sum(sizes) == len(s)
    pos = 0
    seen = set()
    for z in sizes:                                         # each letter appears in exactly one part
        part = set(s[pos:pos + z])
        assert not (part & seen)
        seen |= part
        pos += z
print('random ok: 300 strings up to length 500')

# greedy meaning: every cut is made at the EARLIEST legal index; moving any cut later only merges parts
s = 'ababcbacadefegdehijhklij'
cuts = list(itertools.accumulate(partition_labels(s)))[:-1]
print('cut positions for the long example:', cuts)

# edge cases
assert partition_labels('aaaa') == [4]
assert partition_labels('abab') == [4]
assert partition_labels('abcabc') == [6]
assert partition_labels('aabbcc') == [2, 2, 2]
assert partition_labels('abcdefghijklmnopqrstuvwxyz' * 1) == [1] * 26
assert partition_labels('a' + 'b' * 498 + 'a') == [500]
print('edge cases ok')
```

**Output (my run):**
```
'ababcbacadefegdehijhklij' -> [9, 7, 8]
'eccbbbbdec' -> [10]
'a' -> [1]
'abc' -> [1, 1, 1]
exhaustive ok: 9840 strings over abc; finest partition unique every time
exhaustive ok: 21844 strings over abcd (length <= 7)
random ok: 300 strings up to length 500
cut positions for the long example: [9, 16]
edge cases ok
```

**Edge cases:**
- One character: `[1]`. All distinct letters: all ones.
- All the same letter: one part (`'aaaa'` gives `[4]`).
- A letter at both ends (`'a' + 'b' * 498 + 'a'`) forces one part of length 500.
- Letters that interleave (`'abab'`, `'abcabc'`) cannot be separated.
- Sizes always sum to the string length.

**Follow-ups:**
- Return the parts, not the lengths? Slice with the same cut positions.
- Uppercase, digits, Unicode? Use a dict, not a 26-slot array.
- Merge-intervals view? Each letter spans `[first, last]`; the parts are the merged intervals of those spans (Part 8 merge intervals).
- Fewest parts instead? Trivial: one part.

**Common mistakes:**
- Cutting when the count of the current letter reaches zero (ignores other letters in the part).
- Resetting `end` to `last[ch]` instead of taking the max.
- Starting a new part at `i` instead of `i + 1`.
- Using `first` occurrences instead of `last`.

### Q23 ⭐⭐ 🟡 Queue reconstruction by height. `people` is a shuffled list of [h, k]: a person of height h who has exactly k people of height >= h standing in front of them (1 <= len <= 2000, 1 <= h <= 10^6, 0 <= k < len). The input is guaranteed to come from at least one real queue, and then the queue is unique (the checker verifies the uniqueness claim exhaustively on small cases). Return the queue as a list of [h, k]. Sort by height descending and k ascending, then insert each person at index k of the result list; explain why inserting taller people first means later (shorter) people never change a taller person's k, and why list.insert makes this O(n^2) in the worst case. Example: people=[[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]] -> [[5, 0], [7, 0], [5, 2], [6, 1], [4, 4], [7, 1]]; people=[[6, 0], [5, 0], [4, 0], [3, 2], [2, 2], [1, 4]] -> [[4, 0], [5, 0], [2, 2], [3, 2], [1, 4], [6, 0]]; people=[[3, 0]] -> [[3, 0]].
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Greedy with an ordering trick: place people tallest first, so each later (shorter) person can be dropped at an exact index. Needs a sort plus positional `list.insert`.

**Say this first (1 line):** "I sort by height descending, k ascending, then insert each person at index k, because everyone already placed is at least as tall, so k is exactly the index."

**Brute force:** Try every ordering of the people and keep the ones where each person's k matches. That is n! orderings times O(n^2) to check. The code does it for n <= 7 and also counts how many valid queues there are (always one).

**Optimal:**
- Sort by (-h, k).
- Walk the sorted list. For [h, k] do `out.insert(k, [h, k])`.
- Why it works: when we place a person, everyone already in `out` has height >= h. So "k people at least as tall in front" means exactly k people in front, so index k. Equal heights come in k-ascending order, so the one with the smaller k is already in place when the larger k arrives.
- Why later people never break earlier ones: an insert shifts people to the right, which only changes the k of someone standing behind the new person. A strictly shorter newcomer does not count for any taller person, so nobody's k changes. An equal-height newcomer has a larger k than the equal-height person placed before (sorted k ascending), and that earlier person sits at index k1 < k2, so the newcomer lands behind them.
- Invariant: after processing a prefix of the sorted list, `out` is the correct queue of just those people.
- Input is promised to come from a real queue. Garbage input is not detected: `insert` clamps an index that is too big to the end.

**Complexity:**
- Sort O(n log n). Each `list.insert(k, x)` shifts the tail, O(n). Total O(n^2) worst case, about n^2/2 element moves. For n <= 2000 that is about 2 million moves, fine.
- Worst case: every person inserted at index 0 (heights ascending in the real queue, all k = 0). The code prints 1,999,000 shifts for n = 2000.
- Space O(n). To get O(n log n) you place people into the k-th free slot using a Fenwick tree (Part 14 topic).

**Dry run:** people = [7,0] [4,4] [7,1] [5,0] [6,1] [5,2]. Sorted: [7,0] [7,1] [6,1] [5,0] [5,2] [4,4].
| insert | at index | queue after |
|---|---|---|
| [7,0] | 0 | [7,0] |
| [7,1] | 1 | [7,0] [7,1] |
| [6,1] | 1 | [7,0] [6,1] [7,1] |
| [5,0] | 0 | [5,0] [7,0] [6,1] [7,1] |
| [5,2] | 2 | [5,0] [7,0] [5,2] [6,1] [7,1] |
| [4,4] | 4 | [5,0] [7,0] [5,2] [6,1] [4,4] [7,1] |

**Code:**
```python
import random, itertools

def reconstruct(people):
    out = []
    for h, k in sorted(people, key=lambda p: (-p[0], p[1])):
        out.insert(k, [h, k])          # k taller-or-equal people are already placed
    return out

def pairs_of(queue):                   # the [h, k] each person would report
    return [[h, sum(1 for x in queue[:i] if x >= h)] for i, h in enumerate(queue)]

def brute(people):                     # try every ordering, keep all that are consistent
    good = set()
    for perm in itertools.permutations(map(tuple, people)):
        if all(k == sum(1 for h2, _ in perm[:i] if h2 >= h) for i, (h, k) in enumerate(perm)):
            good.add(perm)
    return good

# examples from the prompt
assert reconstruct([[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]) == [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
assert reconstruct([[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]) == [[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]]
assert reconstruct([[3,0]]) == [[3,0]]

# randomised cross-check against brute force (also checks uniqueness for each input)
rng = random.Random(23)
for _ in range(300):
    n = rng.randint(1, 7)
    heights = [rng.randint(1, 5) for _ in range(n)]
    people = pairs_of(heights)
    rng.shuffle(people)
    sols = brute(people)
    assert len(sols) == 1, people                     # unique queue
    assert [list(p) for p in next(iter(sols))] == reconstruct(people)
print("random cross-check vs brute force: 300 cases OK")

# exhaustive uniqueness: every height sequence of length <= 7 over heights 1..4
# (and length <= 5 over 1..6); the multiset of [h, k] pairs must determine the queue
total = 0
for n, H in [(n, 4) for n in range(1, 8)] + [(n, 6) for n in range(1, 6)]:
    seen = {}
    for heights in itertools.product(range(1, H + 1), repeat=n):
        q = pairs_of(list(heights))
        seen.setdefault(tuple(sorted(map(tuple, q))), set()).add(tuple(map(tuple, q)))
        total += 1
    assert all(len(v) == 1 for v in seen.values()), (n, H)
print("uniqueness: queues checked =", total, "-> no two queues share a pair multiset")

# list.insert cost: worst case, every insert at the front (n(n-1)/2 element moves)
n = 2000
people = [[i, 0] for i in range(1, n + 1)]            # valid queue: heights ascending
rng.shuffle(people)
res = reconstruct(people)
assert res == [[i, 0] for i in range(1, n + 1)]
print("worst case n=2000: elements shifted by insert =", n * (n - 1) // 2)

# garbage in: an impossible input is not detected, insert just clamps to the end
print("invalid input (no real queue):", reconstruct([[5, 3], [4, 0]]))
```

**Output (my run):**
```text
random cross-check vs brute force: 300 cases OK
uniqueness: queues checked = 31174 -> no two queues share a pair multiset
worst case n=2000: elements shifted by insert = 1999000
invalid input (no real queue): [[4, 0], [5, 3]]
```

**Edge cases:**
- Single person: [[3,0]].
- All equal heights: k values 0..n-1, the sort puts them in order, each insert is an append.
- Everyone k = 0: the result is heights ascending, every insert goes to the front (the worst case for shifts).
- Uniqueness: the code checks every height sequence up to length 7 over heights 1 to 4 and up to length 5 over heights 1 to 6 (31,174 queues): no two different queues give the same collection of [h, k] pairs, so the answer is unique.
- Input that is not a real queue: no error, wrong output.

**Follow-ups:**
- Can you beat O(n^2)? Yes, process shortest first, and give each person the (k+1)-th free slot of an empty array, found with a Fenwick tree or segment tree in O(log n). O(n log n).
- Why not `deque.insert`? It is also O(n) in the middle.
- What if the person counts people strictly taller? Then equal heights sort the other way round; redo the argument.

**Common mistakes:**
- Sorting by k first or by height ascending: shorter people then shift taller people's k.
- Sorting equal heights by k descending.
- Inserting at index `len(out) - k` instead of `k`.
- Saying `list.insert` is O(1) at index k. It is O(n - k).

---

### Q24 ⭐⭐ 🟡 Interval list intersections. `a` and `b` are lists of CLOSED integer intervals [start, end] (start <= end); within each list the intervals are sorted and pairwise disjoint (they do not even touch). 0 <= len <= 1000 each. Return the intersection of the two lists as a sorted list of closed intervals; a single shared point gives an interval such as [5, 5]. Use two pointers: intersect the current pair as [max of starts, min of ends] when that is non-empty, then advance the pointer of the interval that ends first. Say why this is O(len(a) + len(b)) and why the output has at most that many intervals. Example: a=[[0, 2], [5, 10], [13, 23], [24, 25]], b=[[1, 5], [8, 12], [15, 24], [25, 26]] -> [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]; a=[[1, 3], [5, 9]], b=[] -> []; a=[[1, 7]], b=[[3, 10]] -> [[3, 7]]; a=[[0, 2], [3, 5]], b=[[2, 3]] -> [[2, 2], [3, 3]].
**Asked at:** Interval pattern guides on techinterview.org (merge, insert, meeting rooms, employee free time, interval scheduling; search snippets only, not opened; the site's own 'asked at' lists were not verified) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Two pointers over two sorted, disjoint lists. Each step looks at one pair and drops whichever interval cannot match anything later.

**Say this first (1 line):** "I keep one pointer in each list, the overlap is [max of starts, min of ends] if that is non-empty, and I advance the pointer whose interval ends first."

**Brute force:** Compare every a-interval with every b-interval: O(len(a) x len(b)) pair checks. Or, as the checker does, mark every point (doubling coordinates so [0,2] and [3,5] stay separate) and merge runs.

**Optimal:**
- Pair (a[i], b[j]): lo = max of starts, hi = min of ends. If lo <= hi, append [lo, hi]. Closed intervals, so lo == hi is a real one-point answer such as [5, 5].
- Advance the pointer of the interval with the smaller end. If the ends tie, advancing b (the `else`) is fine: a[i] then meets the next b interval and finds nothing, since b's intervals are disjoint, and a[i] gets dropped next round.
- Why dropping is safe: the interval that ends first cannot overlap anything beyond the other list's current interval, because later intervals in that list start after the current one ends.

**Complexity:**
- Each loop step advances i or j by one, so at most len(a) + len(b) steps: O(len(a) + len(b)) time, O(1) extra space besides the output.
- Output size: each loop step appends at most one interval, and the last step of the loop always ends the walk, so at most len(a) + len(b) - 1 intervals appear when both lists are non-empty (the code asserts it on 2000 random cases and shows a case that reaches it). The picture: overlapping pairs form a path through the two lists, and a path on len(a) + len(b) nodes has at most that many minus one edges.

**Dry run:** a = [[1,3],[5,9]], b = [[2,4],[6,7],[8,12]].
| i, j | pair | overlap | advance |
|---|---|---|---|
| 0, 0 | [1,3] [2,4] | [2,3] | a (3 < 4) |
| 1, 0 | [5,9] [2,4] | lo 5, hi 4: none | b (9 >= 4) |
| 1, 1 | [5,9] [6,7] | [6,7] | b |
| 1, 2 | [5,9] [8,12] | [8,9] | a (9 < 12) |
Result [[2,3],[6,7],[8,9]].

**Code:**
```python
import random

def intersect(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if lo <= hi:
            out.append([lo, hi])
        if a[i][1] < b[j][1]:          # the one that ends first can never match anything later
            i += 1
        else:
            j += 1
    return out

def brute(a, b):                       # double the coordinates so [0,2] and [3,5] stay apart
    pa, pb = set(), set()
    for s, e in a: pa.update(range(2 * s, 2 * e + 1))
    for s, e in b: pb.update(range(2 * s, 2 * e + 1))
    out, cur = [], None
    for p in sorted(pa & pb):
        if cur and p == cur[1] + 1: cur[1] = p
        else:
            if cur: out.append(cur)
            cur = [p, p]
    if cur: out.append(cur)
    return [[x // 2, y // 2] for x, y in out]

def gen(rng):                          # sorted, pairwise disjoint (no shared point) closed intervals
    res, x = [], rng.randint(0, 3)
    for _ in range(rng.randint(0, 6)):
        s = x + rng.randint(0, 3); e = s + rng.randint(0, 4)
        res.append([s, e]); x = e + 1
    return res

assert intersect([[0,2],[5,10],[13,23],[24,25]], [[1,5],[8,12],[15,24],[25,26]]) == [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
assert intersect([[1,3],[5,9]], []) == []
assert intersect([[1,7]], [[3,10]]) == [[3,7]]
assert intersect([[0,2],[3,5]], [[2,3]]) == [[2,2],[3,3]]
assert intersect([], []) == []

rng = random.Random(24)
for _ in range(2000):
    a, b = gen(rng), gen(rng)
    got = intersect(a, b)
    assert got == brute(a, b), (a, b)
    if a and b:
        assert len(got) <= len(a) + len(b) - 1          # output size bound
print("2000 random cases match brute force; output size never above len(a)+len(b)-1")

# a tight case for the size bound: interleaved intervals that all overlap their neighbour
a = [[0, 3], [5, 8]]; b = [[1, 6]]
print("tight example:", intersect(a, b), "len(a)+len(b)-1 =", len(a) + len(b) - 1)
```

**Output (my run):**
```text
2000 random cases match brute force; output size never above len(a)+len(b)-1
tight example: [[1, 3], [5, 6]] len(a)+len(b)-1 = 2
```

**Edge cases:**
- Either list empty: loop never runs, result [].
- Touching at one point: [0,2] with [2,3] gives [2,2].
- One interval swallowing many from the other list: the big one stays while the other pointer moves.
- Adjacent integers like [0,2] and [3,5] in one list are allowed (they share no point), and [2,3] intersects both in one point.
- Equal ends: advance either pointer, both are correct.

**Follow-ups:**
- Open intervals? Use strict `lo < hi` and decide the tie case by the problem statement.
- Union instead of intersection? Merge the two sorted lists then fold, as in the merge-intervals question.
- k lists? Use a heap of the current interval of each list, O(N log k).

**Common mistakes:**
- Advancing both pointers every time: misses an interval that overlaps the next one of the other list.
- Advancing the pointer with the smaller START instead of the smaller END.
- Using `lo < hi` for closed intervals and losing single-point results.
- Forgetting the output can be [] when one list is empty.

---

### Q25 ⭐⭐ 🟡 Maximum number of events you can attend. `events[i] = [start, end]` is an event that can be attended on any single day d with start <= d <= end (inclusive, integer days, 1 <= start <= end <= 10^5, 1 <= len <= 10^5). You can attend at most one event per day and each event at most once. Return the maximum number of events attended. Sort by start day and sweep the days with a min-heap of end days: on each day add the events starting today, drop expired ones, attend the one that ends soonest; state why 'earliest end first' is the right exchange and the cost (O(n log n)). Example: events=[[1, 2], [2, 3], [3, 4]] -> 3; events=[[1, 2], [2, 3], [3, 4], [1, 2]] -> 4; events=[[1, 1], [1, 1], [1, 1]] -> 1; events=[[1, 4], [4, 4], [2, 2], [3, 4], [1, 1]] -> 4.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Greedy day-by-day sweep with a min-heap of end days. Each day, attend the open event that expires soonest.

**Say this first (1 line):** "I sort by start, sweep the days, push the end of every event starting today, throw away expired ones, and attend the one that ends soonest."

**Brute force:** This is a maximum matching of events to days. Kuhn's augmenting-path algorithm solves it exactly (used in the code for small cases). The sweep is the shortcut because these day-sets are intervals.

**Optimal:**
- Sort events by start. Keep `day` and a min-heap of end days of events that have started and are not yet attended.
- Each day: push every event with start <= day; pop expired ends (end < day); if the heap is non-empty pop the smallest end and count one.
- If the heap is empty, jump `day` to the next start (no point walking empty days).
- Exchange argument: say an optimal plan attends some other open event E2 today, and the soonest-ending open event E1 later (or never). Swap them: E1 goes to today, E2 takes E1's old day, which is no later than E1's deadline and so within E2's deadline since E2 ends no sooner than E1. If E1 was never attended, just replace E2 with E1. The count does not drop. So "soonest end today" can always be assumed.

**Complexity:**
- Sort O(n log n). Each event is pushed once and popped once, O(log n) each: O(n log n) total. The day counter only moves forward and jumps over gaps, so there are at most n attended days plus n expiries; no loop over 10^5 days that does nothing.
- Space O(n) for the heap. The loop is iterative.
- Heap items are plain ints; ties between equal end days compare equal and need no tie-breaker. If you pushed (end, event_dict) tuples, ties would reach the dicts and raise TypeError, so push ends only.

**Dry run:** events = [1,4] [4,4] [2,2] [3,4] [1,1].
| day | pushed | heap (ends) | attend |
|---|---|---|---|
| 1 | 4, 1 | 1, 4 | end 1 (count 1) |
| 2 | 2 | 2, 4 | end 2 (count 2) |
| 3 | 4 | 4, 4 | end 4 (count 3) |
| 4 | 4 | 4, 4 | end 4 (count 4) |
After day 4 the heap holds one expired 4, so nothing else. Answer 4.

**Code:**
```python
import heapq, random

def max_events(events):
    ev = sorted(events)                # by start day
    h, i, day, cnt, n = [], 0, 0, 0, len(ev)
    while i < n or h:
        if not h:
            day = max(day, ev[i][0])   # nothing open: jump to the next start
        while i < n and ev[i][0] <= day:
            heapq.heappush(h, ev[i][1]); i += 1
        while h and h[0] < day:        # expired
            heapq.heappop(h)
        if h:
            heapq.heappop(h); cnt += 1; day += 1   # attend the soonest-ending event
    return cnt

def brute(events):                     # maximum bipartite matching events -> days (Kuhn), small inputs only
    match = {}
    def try_(i, seen):
        for d in range(events[i][0], events[i][1] + 1):
            if d in seen: continue
            seen.add(d)
            if d not in match or try_(match[d], seen):
                match[d] = i; return True
        return False
    return sum(try_(i, set()) for i in range(len(events)))

assert max_events([[1,2],[2,3],[3,4]]) == 3
assert max_events([[1,2],[2,3],[3,4],[1,2]]) == 4
assert max_events([[1,1],[1,1],[1,1]]) == 1
assert max_events([[1,4],[4,4],[2,2],[3,4],[1,1]]) == 4

rng = random.Random(25)
for _ in range(1500):
    n = rng.randint(1, 8)
    ev = []
    for _ in range(n):
        s = rng.randint(1, 7); ev.append([s, rng.randint(s, 8)])
    assert max_events(ev) == brute(ev), ev
print("1500 random cases match matching brute force")

# wrong rule: each day attend the open event with the LATEST end (to show why soonest-end matters)
def latest_end_first(events):
    ev = sorted(events); h, i, day, cnt = [], 0, 0, 0
    while i < len(ev) or h:
        if not h: day = max(day, ev[i][0])
        while i < len(ev) and ev[i][0] <= day: heapq.heappush(h, -ev[i][1]); i += 1
        while h and -h[0] < day: heapq.heappop(h)
        if h: heapq.heappop(h); cnt += 1; day += 1
    return cnt
bad = [[1, 1], [1, 2]]
print("latest-end-first on", bad, ":", latest_end_first(bad), "vs soonest-end", max_events(bad))

# heap of plain ints: tied ends are fine (equal ints compare). The heap holds end days only.
h = []
for e in [4, 4, 2, 4]: heapq.heappush(h, e)
print("ties in a heap of ints are fine:", [heapq.heappop(h) for _ in range(4)])

# scale: n = 100000, sort + one push and one pop per event -> O(n log n); loop is iterative
rng = random.Random(1)
big = []
for _ in range(100000):
    s = rng.randint(1, 100000); big.append([s, min(100000, s + rng.randint(0, 50))])
print("n=100000 random events ->", max_events(big), "attended (<= 100000 days)")
```

**Output (my run):**
```text
1500 random cases match matching brute force
latest-end-first on [[1, 1], [1, 2]] : 1 vs soonest-end 2
ties in a heap of ints are fine: [2, 4, 4, 4]
n=100000 random events -> 98052 attended (<= 100000 days)
```

**Edge cases:**
- Identical events [1,1] x3: only one day, answer 1.
- Gap in days: the `if not h` jump handles it.
- Expired event still in the heap: popped by the `h[0] < day` loop, never attended.
- Single event: 1.
- n = 10^5 with days up to 10^5: fine, the code runs one.

**Follow-ups:**
- Why not sort by end and take events greedily? Each event needs a specific free day, which a single "end of last pick" cannot track.
- Free-day variant with a union-find: assign each event the earliest free day >= start, almost O(n).
- Events with a minimum duration (meeting rooms III)? A different heap structure, see the meeting-rooms questions.

**Common mistakes:**
- Not popping expired events before attending.
- Attending the event that started first or ends last (the code shows the latest-end rule failing on [[1,1],[1,2]]).
- Iterating `for day in range(1, 10**5 + 1)` with an inner push loop and forgetting `i` is shared.
- Pushing tuples with unorderable payloads.

---

### Q26 ⭐⭐ 🟡 Furthest building you can reach. `heights` (2 <= len <= 10^5, 1 <= heights[i] <= 10^6) are building heights in a row; you start on building 0 and walk right. Moving to a building of equal or lower height is free; moving up by d costs either d bricks or one ladder (a ladder covers any d). You own `bricks` bricks and `ladders` ladders (0 <= bricks <= 10^9, 0 <= ladders <= len). Return the largest 0-based index you can reach. Keep a min-heap of the climbs you have covered with ladders: when it holds more than `ladders` climbs, pay bricks for the smallest one, and stop when bricks go negative. Explain why the ladders always end up on the largest climbs seen so far (an exchange argument). Example: heights=[4, 2, 7, 6, 9, 14, 12], bricks=5, ladders=1 -> 4; heights=[4, 12, 2, 7, 3, 18, 20, 3, 19], bricks=10, ladders=2 -> 7; heights=[14, 3, 19, 3], bricks=17, ladders=0 -> 3; heights=[1, 2], bricks=0, ladders=0 -> 0.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Greedy with a min-heap of the biggest climbs so far: ladders on the biggest climbs, bricks on the rest.

**Say this first (1 line):** "I give every climb a ladder at first, and when I run out of ladders I pay bricks for the smallest climb a ladder is covering, so ladders always sit on the biggest climbs."

**Brute force:** At each climb choose bricks or a ladder: up to 2^n branches. The code does it for n <= 9 (recursion depth at most 9, so no recursion limit concern; the real solution is iterative).

**Optimal:**
- For each step i with climb d = heights[i+1] - heights[i] > 0, push d on a min-heap.
- If the heap holds more than `ladders` climbs, pop the smallest and pay `bricks -= smallest`. If bricks < 0, you cannot go on: return i.
- If the loop finishes, return the last index.
- Exchange argument: among the climbs up to the point you stand, the set covered by ladders should be the `ladders` largest ones (swapping a ladder from a smaller climb to a larger one saves bricks and never costs more). The heap holds exactly the ladders' current largest climbs; each time it overflows, the smallest becomes a brick payment.
- Why one cheap check is enough: the bricks needed to reach index i+1 is the sum of all climbs minus the ladder'd (largest) ones, which is the sum of the popped ones.

**Complexity:**
- n - 1 steps, each with a push and at most one pop on a heap of at most `ladders + 1` entries: O(n log(ladders + 1)) time, O(ladders) space.
- Heap items are plain ints so ties are harmless.

**Dry run:** heights = [4,2,7,6,9,14,12], bricks = 5, ladders = 1.
| step | climb | heap after push | action | bricks |
|---|---|---|---|---|
| 4 to 2 | none | | free | 5 |
| 2 to 7 | 5 | [5] | 1 ladder, no pop | 5 |
| 7 to 6 | none | | free | 5 |
| 6 to 9 | 3 | [3,5] | pop 3, pay | 2 |
| 9 to 14 | 5 | [5,5] | pop 5, pay 5 | -3 |
Bricks went negative while standing at index 4, so return 4.

**Code:**
```python
import heapq, random

def furthest(heights, bricks, ladders):
    h = []                                       # min-heap of the climbs a ladder currently covers
    for i in range(len(heights) - 1):
        d = heights[i + 1] - heights[i]
        if d > 0:
            heapq.heappush(h, d)
            if len(h) > ladders:                 # too many ladder climbs: pay bricks for the smallest
                bricks -= heapq.heappop(h)
                if bricks < 0:
                    return i
    return len(heights) - 1

def brute(heights, bricks, ladders):             # try every brick/ladder choice (depth <= n, small n only)
    best = 0
    def go(i, b, l):
        nonlocal best
        best = max(best, i)
        if i == len(heights) - 1: return
        d = heights[i + 1] - heights[i]
        if d <= 0: go(i + 1, b, l); return
        if b >= d: go(i + 1, b - d, l)
        if l > 0: go(i + 1, b, l - 1)
    go(0, bricks, ladders)
    return best

assert furthest([4,2,7,6,9,14,12], 5, 1) == 4
assert furthest([4,12,2,7,3,18,20,3,19], 10, 2) == 7
assert furthest([14,3,19,3], 17, 0) == 3
assert furthest([1,2], 0, 0) == 0

rng = random.Random(26)
for _ in range(2000):
    n = rng.randint(2, 9)
    hs = [rng.randint(1, 9) for _ in range(n)]
    b, l = rng.randint(0, 15), rng.randint(0, n)
    assert furthest(hs, b, l) == brute(hs, b, l), (hs, b, l)
print("2000 random cases match brute force")

# edge cases: ladders >= number of climbs -> always reach the end, bricks 0 is fine
assert furthest([1, 5, 2, 9, 3], 0, 2) == 4
assert furthest([5, 4, 3, 2, 1], 0, 0) == 4       # only descents: free
# Why not 'bricks first, ladder when out'? Greedy by order wastes a ladder on a small climb.
def bricks_first(hs, bricks, ladders):
    for i in range(len(hs) - 1):
        d = hs[i + 1] - hs[i]
        if d <= 0: continue
        if bricks >= d: bricks -= d
        elif ladders: ladders -= 1
        else: return i
    return len(hs) - 1
case = ([1, 3, 4, 5], 2, 1)
print("bricks-first on", case, "->", bricks_first(*case), "vs heap greedy", furthest(*case))

# heap holds plain ints, so ties are harmless. Size is at most ladders + 1 at all times.
n = 100000
hs = [(i * 7919) % 1000003 + 1 for i in range(n)]
print("n=100000:", furthest(hs, 10**9, 50), "(iterative, heap size <= 51)")
```

**Output (my run):**
```text
2000 random cases match brute force
bricks-first on ([1, 3, 4, 5], 2, 1) -> 2 vs heap greedy 3
n=100000: 99999 (iterative, heap size <= 51)
```

**Edge cases:**
- ladders = 0: every climb pushed then immediately popped: pure brick budget.
- ladders >= number of climbs: never pops, always reaches the end.
- No climbs at all: reaches the end with 0 bricks.
- Two buildings: [1,2] with 0 bricks, 0 ladders gives 0.
- Equal climbs: either can take the ladder.

**Follow-ups:**
- Bricks-first greedy? Fails: the code finds [1,3,4,5] with 2 bricks, 1 ladder where bricks-first stops at index 2 but the heap reaches 3.
- Can you binary search the answer? Yes, check "can I reach index m" by sorting climbs: O(n log^2 n), slower than the heap. See Part 5 Q33 for the monotone-predicate idea.
- Why not a max-heap? You need to evict the smallest ladder climb, so a min-heap.

**Common mistakes:**
- Returning i + 1 or i - 1 at the failure point (the index you stand on is i).
- Pushing zero or negative climbs.
- Checking `bricks < 0` before popping.
- Spending bricks on the first climbs and saving ladders for later.

---

### Q27 ⭐⭐ 🟡 Find k pairs with the smallest sums. `nums1` and `nums2` are sorted ascending integer lists (1 <= len <= 10^5 each, values in [-10^9, 10^9]) and 1 <= k <= min(10^4, len(nums1) * len(nums2)). A pair is (u, v) with u from nums1 and v from nums2 (pairs are counted by index, so equal value pairs from different positions are distinct). Return k pairs [u, v] with the smallest sums, in ascending order of sum. When several pairs tie at the k-th sum any of them may be returned: the checker verifies the pairs exist (with multiplicity) and that their sums are exactly the k smallest. Use a min-heap seeded with (nums1[i] + nums2[0], i, 0) for the first min(k, len(nums1)) indices and push (i, j + 1) after each pop (O(k log min(k, len(nums1)))); compare with the matrix view in Part 5 Q26, where the same 'sorted rows' structure is searched by value instead. Example: nums1=[1, 7, 11], nums2=[2, 4, 6], k=3 -> [[1, 2], [1, 4], [1, 6]]; nums1=[1, 1, 2], nums2=[1, 2, 3], k=2 -> [[1, 1], [1, 1]]; nums1=[1, 2], nums2=[3], k=2 -> [[1, 3], [2, 3]].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** K-way merge on an implicit matrix. Pair (i, j) has sum nums1[i] + nums2[j], and sums grow along each row. A min-heap holds one frontier cell per row.

**Say this first (1 line):** "Each nums1 index is a sorted row of sums; I start every row at column 0, pop the smallest, and push the next cell in that row."

**Brute force:** Build all n1 x n2 pairs, sort by sum, take k: O(n1 n2 log(n1 n2)). For 10^5 x 10^5 that is impossible.

**Optimal:**
- Heap entries (sum, i, j), initially for i in range(min(k, n1)) with j = 0. Only the first k rows can matter: the k-th pair's row index is at most k - 1.
- Pop the smallest, record [nums1[i], nums2[j]], and push (nums1[i] + nums2[j + 1], i, j + 1) if j + 1 exists.
- Repeat k times.
- Correctness: cell (i, j + 1) is at least as big as (i, j) because nums2 is sorted, and a cell enters the heap only after its left neighbour was popped. So when we pop the smallest heap entry, every cell not yet in the heap has a smaller-or-equal left neighbour still waiting inside, hence is not smaller.
- Equal sums tie: any choice is valid, which is why the checker compares the sums and the multiset of pairs, not the exact pairs.

**Complexity:**
- Initial heapify O(min(k, n1)); k pops and at most k pushes on a heap of at most min(k, n1) entries: O(k log min(k, n1)). Space O(min(k, n1)).
- With k <= 10^4 the heap is at most 10^4 entries even for n = 10^5.
- Heapq tuples: (sum, i, j) never ties completely, because each (i, j) is in the heap at most once, so the comparison never reaches anything unorderable. The code shows what happens with a dict payload: TypeError on a tie of sums.

**Dry run:** nums1 = [1,7,11], nums2 = [2,4,6], k = 3.
| step | heap (sum,i,j) | pop | output |
|---|---|---|---|
| 0 | (3,0,0) (9,1,0) (13,2,0) | (3,0,0) | [1,2], push (5,0,1) |
| 1 | (5,0,1) (9,1,0) (13,2,0) | (5,0,1) | [1,4], push (7,0,2) |
| 2 | (7,0,2) (9,1,0) (13,2,0) | (7,0,2) | [1,6] |

**Code:**
```python
import heapq, random
from collections import Counter

def k_pairs(nums1, nums2, k):
    if not nums1 or not nums2:
        return []
    h = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
    heapq.heapify(h)
    out = []
    while h and len(out) < k:
        _, i, j = heapq.heappop(h)
        out.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):
            heapq.heappush(h, (nums1[i] + nums2[j + 1], i, j + 1))
    return out

def valid(nums1, nums2, k, got):       # checker: right pairs (with multiplicity) and exactly the k smallest sums
    allp = [(x, y) for x in nums1 for y in nums2]
    return (len(got) == k and not (Counter(map(tuple, got)) - Counter(allp))
            and [x + y for x, y in got] == sorted(x + y for x, y in allp)[:k])   # ascending order of sum

def brute(nums1, nums2, k):
    return sorted(([x, y] for x in nums1 for y in nums2), key=lambda p: p[0] + p[1])[:k]

assert valid([1,7,11], [2,4,6], 3, k_pairs([1,7,11], [2,4,6], 3))
assert k_pairs([1,7,11], [2,4,6], 3) == [[1,2],[1,4],[1,6]]
assert k_pairs([1,1,2], [1,2,3], 2) == [[1,1],[1,1]]
assert k_pairs([1,2], [3], 2) == [[1,3],[2,3]]

rng = random.Random(27)
for _ in range(2000):
    a = sorted(rng.randint(-6, 6) for _ in range(rng.randint(1, 6)))
    b = sorted(rng.randint(-6, 6) for _ in range(rng.randint(1, 6)))
    k = rng.randint(1, len(a) * len(b))
    got = k_pairs(a, b, k)
    assert valid(a, b, k, got), (a, b, k, got)
    assert [x + y for x, y in got] == [x + y for x, y in brute(a, b, k)]
print("2000 random cases: valid output, sums equal brute force (pairs may differ on ties)")

# Tie-breaking: (sum, i, j) never ties completely because (i, j) is unique per state,
# so heapq never has to compare anything beyond ints. Pushing (sum, [u, v]) also works (lists compare),
# but pushing (sum, {'u':..}) with dict payloads would raise TypeError on equal sums:
h = []
heapq.heappush(h, (5, {'p': 1}))
try:
    heapq.heappush(h, (5, {'p': 2}))
except TypeError as e:
    print("TypeError on tied sums with dict payload:", e)

# Size: heap never exceeds min(k, len(nums1)) entries -> O(k log min(k, n1)); n = 100000, k = 10000
n = 100000
a = [i * 3 for i in range(n)]; b = [i * 5 - 7 for i in range(n)]
res = k_pairs(a, b, 10000)
assert [x + y for x, y in res] == sorted(x + y for x, y in res)
print("n=100000, k=10000: last sum", sum(res[-1]), "first", res[0])
```

**Output (my run):**
```text
2000 random cases: valid output, sums equal brute force (pairs may differ on ties)
TypeError on tied sums with dict payload: '<' not supported between instances of 'dict' and 'dict'
n=100000, k=10000: last sum 537 first [0, -7]
```

**Edge cases:**
- k = 1: the single smallest pair (nums1[0], nums2[0]).
- k equal to n1 x n2: all pairs, the heap drains.
- nums2 of length 1: each row has one cell, nothing is pushed back.
- Equal values in the lists: pairs are counted by index, so duplicates are distinct pairs ([1,1] twice in the second example).
- Negative values: fine, only differences between sums matter.

**Follow-ups:**
- Why seed only k rows? Pair (i, 0) for i >= k is no smaller than the k pairs (0, 0), (1, 0), ..., (k-1, 0), so with ties broken toward lower rows it is never needed; any k smallest sums are still found.
- Compare with the sorted-matrix question in Part 5 Q26: that one searches by value with a counting binary search; this one walks the first k cells with a heap.
- Three lists? Heap entries become 3-tuples of indices, or reduce two at a time.

**Common mistakes:**
- Seeding all n1 rows when n1 = 10^5 (wasteful but valid), or all cells (wrong complexity).
- Pushing both (i + 1, j) and (i, j + 1) without a visited set: duplicates.
- Stopping when the heap is empty before k pairs when k exceeds the pair count (k is guaranteed not to).
- Putting a payload that cannot be ordered after a sum that can tie.

---

### Q28 ⭐⭐ 🟡 Heap internals: sift up, sift down and the build-heap bound. For a min-heap in a list a (0-indexed), parent(i) = (i - 1) // 2 and children are 2i + 1 and 2i + 2. Given `vals` (0 <= len <= 200), simulate two constructions and return `[bottom_up_layout, bottom_up_swaps, one_by_one_layout, one_by_one_swaps]`. Bottom-up: for i from len // 2 - 1 down to 0 run sift-down(i), where sift-down repeatedly picks the smallest of a[i], a[2i + 1], a[2i + 2] (a child replaces the current only if it is STRICTLY smaller, the left child is preferred on a tie between the children, the right child needs to be strictly smaller than the left) and swaps. One by one: append each value and sift-up (swap with the parent while the parent is STRICTLY greater). Count one swap per exchange. Then explain why bottom-up is O(n): the cost of sift-down at a node is bounded by its height, and the heights of all nodes of an n-node complete tree sum to n - popcount(n) (so at most n - 1 swaps), while the one-by-one build can cost about n log n swaps (a sorted-descending input). The checker confirms over every permutation of up to 8 distinct values that the bottom-up swap count never exceeds n - popcount(n) and reaches it. Example: vals=[5, 3, 8, 1, 9, 2] -> [[1, 3, 2, 5, 9, 8], 4, [1, 3, 2, 5, 9, 8], 4]; vals=[9, 8, 7, 6, 5, 4, 3, 2, 1] -> [[1, 2, 3, 6, 5, 4, 7, 8, 9], 7, [1, 2, 4, 3, 7, 8, 5, 9, 6], 16]; vals=[1, 2, 3, 4, 5, 6, 7] -> [[1, 2, 3, 4, 5, 6, 7], 0, [1, 2, 3, 4, 5, 6, 7], 0]; vals=[2, 2, 2] -> [[2, 2, 2], 0, [2, 2, 2], 0]; vals=[] -> [[], 0, [], 0].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Heap internals. A binary heap is an array view of a complete binary tree. Two repair moves (sift-up, sift-down) and two ways to build one.

**Say this first (1 line):** "Bottom-up heapify is O(n) because most nodes are near the leaves and sift-down costs at most a node's height; one-by-one insertion is O(n log n) because most nodes are deep and sift-up costs their depth."

**Brute force:** There is no brute force for the claim itself. The check is exhaustive: run the simulation on every permutation of 1..n for n up to 8 and compare the swap counts with the bound.

**Optimal:**
- Layout: parent(i) = (i - 1) // 2, children 2i + 1 and 2i + 2. Heap property: parent <= children.
- Sift-down(i): find the smallest of a[i], left, right (child must be strictly smaller to win, left wins ties); swap and continue, else stop.
- Sift-up(i): while the parent is strictly greater, swap.
- Bottom-up build: for i from n // 2 - 1 down to 0, sift-down(i). Nodes from n // 2 on are leaves, already heaps.
- Why O(n): sift-down at node v does at most height(v) swaps. In a complete tree with n nodes the heights sum to n - popcount(n). That is below n, so at most n - 1 swaps overall. Intuition: about n/2 nodes have height 0, n/4 have height 1, n/8 have height 2, and sum of h / 2^h converges.
- One by one: a node at depth d may climb d levels, and half the nodes are at the bottom depth about log n. Descending input is the worst case: every insert climbs to the root.

**Complexity:**
- Bottom-up: O(n) time, O(1) extra. At most n - popcount(n) swaps, and the code shows that exact value is reached (max over all permutations equals the bound for n = 1..8).
- One by one: O(n log n) time. For descending input of size 4095 the code prints 40,962 swaps against 4,083 for bottom-up.
- Comparisons add a constant factor (about 2 per level for sift-down) but do not change the big-O.

**Dry run:** vals = [5,3,8,1,9,2], n = 6, bottom-up starts at i = 2.
| step | array | action |
|---|---|---|
| i=2 | 5 3 8 1 9 2 | children of index 2: only index 5 (value 2) < 8, swap |
| after | 5 3 2 1 9 8 | 1 swap |
| i=1 | 5 3 2 1 9 8 | children 1 and 9, 1 < 3, swap |
| after | 5 1 2 3 9 8 | 2 swaps |
| i=0 | 5 1 2 3 9 8 | children 1, 2: swap with 1 |
| after | 1 5 2 3 9 8 | 3 swaps; 5 has children 3 and 9, swap with 3 |
| final | 1 3 2 5 9 8 | 4 swaps |

**Code:**
```python
import heapq, itertools, random

def sift_down(a, i, n, cnt):
    while True:
        l, r, m = 2 * i + 1, 2 * i + 2, i
        if l < n and a[l] < a[m]: m = l          # child must be STRICTLY smaller
        if r < n and a[r] < a[m]: m = r          # right must be strictly smaller than the current best
        if m == i: return
        a[i], a[m] = a[m], a[i]; cnt[0] += 1; i = m

def sift_up(a, i):
    swaps = 0
    while i > 0 and a[(i - 1) // 2] > a[i]:      # swap while the parent is STRICTLY greater
        a[(i - 1) // 2], a[i] = a[i], a[(i - 1) // 2]; i = (i - 1) // 2; swaps += 1
    return swaps

def build(vals):
    a, c = list(vals), [0]
    for i in range(len(a) // 2 - 1, -1, -1):     # leaves (second half) are already heaps
        sift_down(a, i, len(a), c)
    p, c2 = [], 0
    for v in vals:
        p.append(v); c2 += sift_up(p, len(p) - 1)
    return [a, c[0], p, c2]

def is_heap(a): return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))

assert build([5,3,8,1,9,2]) == [[1,3,2,5,9,8], 4, [1,3,2,5,9,8], 4]
assert build([9,8,7,6,5,4,3,2,1]) == [[1,2,3,6,5,4,7,8,9], 7, [1,2,4,3,7,8,5,9,6], 16]
assert build([1,2,3,4,5,6,7]) == [[1,2,3,4,5,6,7], 0, [1,2,3,4,5,6,7], 0]
assert build([2,2,2]) == [[2,2,2], 0, [2,2,2], 0]
assert build([]) == [[], 0, [], 0]

# exhaustive: every permutation of 1..n, n <= 8
for n in range(1, 9):
    bound = n - bin(n).count("1")
    worst = 0
    for perm in itertools.permutations(range(1, n + 1)):
        a, sw, p, sw2 = build(perm)
        assert is_heap(a) and is_heap(p) and sorted(a) == sorted(p) == list(range(1, n + 1))
        assert sw <= bound
        worst = max(worst, sw)
    assert worst == bound                        # reached, so the bound is tight
    print(f"n={n}: max bottom-up swaps over all {n}! permutations = {worst} = n - popcount(n) = {bound}")

# the heights of an n-node complete tree sum to n - popcount(n)
for n in range(1, 301):
    def height(i):                               # longest path down from node i
        d = 0
        while 2 * i + 1 < n: i = 2 * i + 1; d += 1
        return d
    assert sum(height(i) for i in range(n)) == n - bin(n).count("1")
print("sum of node heights == n - popcount(n) for n = 1..300")

# one-by-one worst case: descending input costs about n log n swaps; bottom-up stays under n
for n in (255, 1023, 4095):
    r = build(range(n, 0, -1))
    print(f"n={n}: descending input, bottom-up swaps {r[1]}, one-by-one swaps {r[3]}")

# heapq.heappush gives the same layout as one-by-one; heapq.heapify may lay out differently
rng = random.Random(28)
push_same = heapify_same = 0
for _ in range(2000):
    v = [rng.randint(0, 50) for _ in range(rng.randint(0, 30))]
    h = []
    for x in v: heapq.heappush(h, x)
    assert h == build(v)[2]
    push_same += 1
    g = list(v); heapq.heapify(g)
    assert is_heap(g)
    heapify_same += g == build(v)[0]
print("heappush layout == one-by-one in", push_same, "of 2000; heapify layout == textbook bottom-up in", heapify_same, "of 2000 (both always valid heaps)")
```

**Output (my run):**
```text
n=1: max bottom-up swaps over all 1! permutations = 0 = n - popcount(n) = 0
n=2: max bottom-up swaps over all 2! permutations = 1 = n - popcount(n) = 1
n=3: max bottom-up swaps over all 3! permutations = 1 = n - popcount(n) = 1
n=4: max bottom-up swaps over all 4! permutations = 3 = n - popcount(n) = 3
n=5: max bottom-up swaps over all 5! permutations = 3 = n - popcount(n) = 3
n=6: max bottom-up swaps over all 6! permutations = 4 = n - popcount(n) = 4
n=7: max bottom-up swaps over all 7! permutations = 4 = n - popcount(n) = 4
n=8: max bottom-up swaps over all 8! permutations = 7 = n - popcount(n) = 7
sum of node heights == n - popcount(n) for n = 1..300
n=255: descending input, bottom-up swaps 247, one-by-one swaps 1538
n=1023: descending input, bottom-up swaps 1013, one-by-one swaps 8194
n=4095: descending input, bottom-up swaps 4083, one-by-one swaps 40962
heappush layout == one-by-one in 2000 of 2000; heapify layout == textbook bottom-up in 1555 of 2000 (both always valid heaps)
```

**Edge cases:**
- Empty or one element: loop does not run, 0 swaps.
- Equal values: strict comparisons mean no swaps, [2,2,2] costs 0.
- Already sorted ascending: both builds cost 0 swaps.
- Descending input: the separation case (7 versus 16 for nine values).
- `heapq.heapify` uses a variant of sift-down that moves a hole to a leaf and then sifts up, so its layout can differ from the textbook layout while still being a valid heap. In the run, 1555 of 2000 seeded random lists matched; both layouts always passed the heap check. `heappush` matched the one-by-one layout every time.

**Follow-ups:**
- Heap sort? Build in O(n), then n times swap the root to the end and sift-down on a shrinking heap: O(n log n), in place, not stable.
- Why is sift-up for insert O(log n) but still n inserts is O(n log n) while build is O(n)? Because the build uses the heights (small on average), the inserts use the depths (large on average).
- Why start at n // 2 - 1? Indices from n // 2 have no children (the first child of i is 2i + 1 >= n).

**Common mistakes:**
- Running the build loop from 0 up to n // 2: wrong order, higher nodes are fixed before their subtrees.
- Choosing the right child when it equals the left (breaks the "left wins ties" rule, changes the layout and swap count but not validity).
- Claiming the sum of heights is n log n (it is below n).
- Saying `heapify` and repeated `heappush` produce the same list.

---

### Q29 ⭐⭐ 🟡 heapq with tuples and tie-breaking. `tasks` is a list of [priority, payload] where priority is an integer and payload is a dict such as {'id': 'a'} (dicts cannot be ordered with <). Return the list of payload ids in the order a priority queue serves them: smaller priority first, and among equal priorities in insertion order (first in, first out). 0 <= len <= 10^4. Explain why pushing (priority, payload) raises TypeError when two priorities tie (tuples compare element by element and then fall through to the dicts), why pushing (priority, payload['id']) silently orders ties by id instead of arrival, and the fix: push (priority, counter, payload) with a strictly increasing counter so the comparison never reaches the payload. Say what the counter buys that a stable sort would give for free. Example: tasks=[[2, {'id': 'a'}], [1, {'id': 'b'}], [2, {'id': 'c'}], [1, {'id': 'd'}], [3, {'id': 'e'}]] -> ['b', 'd', 'a', 'c', 'e']; tasks=[[5, {'id': 'x'}], [5, {'id': 'y'}], [5, {'id': 'z'}]] -> ['x', 'y', 'z']; tasks=[] -> [].
**Asked at:** The Python heapq documentation recipe on entry counters, removed-task markers and wrapper classes (search snippets of docs.python.org pages; WebFetch of docs.python.org failed with getaddrinfo ENOTFOUND, so the page was not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** `heapq` tie-breaking. Heap entries are compared with `<`, and tuples compare element by element, so a tie in the first field moves on to the next.

**Say this first (1 line):** "I push (priority, counter, payload) with an increasing counter, so equal priorities come out first in first out and the payload is never compared."

**Brute force:** `sorted(tasks, key=priority)`. Python's sort is stable, so equal priorities keep arrival order. O(n log n). The code uses it as the checker.

**Optimal:**
- `heappush(h, (p, next(counter), payload))` and `heappop(h)[2]`.
- Why plain (priority, payload) fails: with distinct priorities the first element decides and the dicts are never compared. On the first tie, tuple comparison looks at the payloads, and `dict < dict` raises TypeError. It is data-dependent, so it can pass tests and crash in production.
- Why (priority, payload['id']) is a trap: no error, but ties are now served in id order (z, a, m comes out a, m, z), not arrival order. Silent wrong order.
- The counter is unique and increasing, so two entries never tie on the first two fields and the third is never read.
- Docs-recipe style: `itertools.count()` is a cheap counter.

**Complexity:**
- Push and pop O(log n) each, n of each: O(n log n). Space O(n) for the heap.
- The counter adds one int per entry and one comparison step at most.

**Dry run:** tasks (priority, id): (2,a) (1,b) (2,c) (1,d) (3,e). Entries (p, counter, id): (2,0,a) (1,1,b) (2,2,c) (1,3,d) (3,4,e).
| pop | entry | reason |
|---|---|---|
| 1 | (1,1,b) | smallest priority, smaller counter than d |
| 2 | (1,3,d) | next priority 1 |
| 3 | (2,0,a) | priority 2, counter 0 before 2 |
| 4 | (2,2,c) | |
| 5 | (3,4,e) | |
Output b d a c e.

**Code:**
```python
import heapq, itertools, random

def serve(tasks):
    h, counter = [], itertools.count()           # strictly increasing: never ties, never reaches payload
    for p, payload in tasks:
        heapq.heappush(h, (p, next(counter), payload))
    return [heapq.heappop(h)[2]['id'] for _ in range(len(h))]

def brute(tasks):                                # sorted is stable, so equal priorities keep arrival order
    return [t[1]['id'] for t in sorted(tasks, key=lambda t: t[0])]

assert serve([[2,{'id':'a'}],[1,{'id':'b'}],[2,{'id':'c'}],[1,{'id':'d'}],[3,{'id':'e'}]]) == ['b','d','a','c','e']
assert serve([[5,{'id':'x'}],[5,{'id':'y'}],[5,{'id':'z'}]]) == ['x','y','z']
assert serve([]) == []

# 1) (priority, payload): TypeError only when priorities tie
h = []
heapq.heappush(h, (1, {'id': 'a'}))
heapq.heappush(h, (2, {'id': 'b'}))              # fine: 1 < 2 decides, dicts never compared
try:
    heapq.heappush(h, (1, {'id': 'c'}))          # tie on 1 -> falls through to dict < dict
except TypeError as e:
    print("TypeError:", e)

# 2) (priority, id): no error, but ties are served by id, not by arrival
tasks = [[1, {'id': 'z'}], [1, {'id': 'a'}], [1, {'id': 'm'}]]
h = []
for p, d in tasks: heapq.heappush(h, (p, d['id']))
print("tuple (p, id) serves:", [heapq.heappop(h)[1] for _ in range(3)], "| FIFO wanted:", brute(tasks))

# 3) (priority, counter, payload): FIFO among ties
print("counter serves:     ", serve(tasks))

# randomised cross-check against stable sort
rng = random.Random(29)
for _ in range(1000):
    ts = [[rng.randint(0, 4), {'id': rng.choice('abcdefgh') + str(i)}] for i in range(rng.randint(0, 12))]
    assert serve(ts) == brute(ts)
print("1000 random cases match the stable sort")

# What the counter buys: the heap is ONLINE. Interleave pushes and pops, a one-off sort cannot.
h, c, order = [], itertools.count(), []
for p, name in [(2, 'a'), (2, 'b')]: heapq.heappush(h, (p, next(c), {'id': name}))
order.append(heapq.heappop(h)[2]['id'])          # a
for p, name in [(1, 'c'), (2, 'd')]: heapq.heappush(h, (p, next(c), {'id': name}))
order += [heapq.heappop(h)[2]['id'] for _ in range(3)]
print("interleaved push/pop order:", order)

# Same-object ties: if the payload objects ARE comparable the bug is silent. Integers never raise.
h = []
for p, v in [(1, 7), (1, 3)]: heapq.heappush(h, (p, v))
print("payload ints decide ties silently:", [heapq.heappop(h) for _ in range(2)])
```

**Output (my run):**
```text
TypeError: '<' not supported between instances of 'dict' and 'dict'
tuple (p, id) serves: ['a', 'm', 'z'] | FIFO wanted: ['z', 'a', 'm']
counter serves:      ['z', 'a', 'm']
1000 random cases match the stable sort
interleaved push/pop order: ['a', 'c', 'b', 'd']
payload ints decide ties silently: [(1, 3), (1, 7)]
```

**Edge cases:**
- Empty list: returns [].
- All equal priorities: pure FIFO, the three-task example gives x y z.
- A negative or float priority: fine, the counter only sits behind it.
- Payloads that are comparable (ints): no TypeError, but the tie then follows payload value, not arrival, so it is silent. The code shows this.
- Mixed int and str priorities would raise TypeError on every comparison between them. Keep priorities one type.

**Follow-ups:**
- What does the counter buy over a stable sort? A sort needs all the data first. A heap serves an online stream: push and pop can interleave, and the counter keeps FIFO across the whole run. The code interleaves pushes and pops to show it.
- LIFO among ties? Use a decreasing counter (`-next(counter)`).
- Can you give `heappush` a `key=`? No, it has none. Wrap the item, as in the next question.

**Common mistakes:**
- Testing only with distinct priorities and never seeing the TypeError.
- Using the payload's id or name as the tie-breaker and calling it FIFO.
- Using `len(heap)` as the counter: it shrinks after a pop and can repeat, so ties come back.
- Using `random()` as a tie-breaker, not reproducible.

---

### Q30 ⭐⭐ 🟡 Custom orderings with a wrapper class. heapq has no key= argument and a string cannot be negated, so a max-heap of strings needs a wrapper. `words` is a list of lowercase strings (0 <= len <= 10^4, duplicates allowed) and `order` is either 'lex_desc' (pop in descending lexicographic order) or 'len_desc_lex_desc' (longer strings first, and among equal lengths descending lexicographic order). Return the words in the order a heap using that ordering pops them. Write a small wrapper class with __slots__ and a reversed __lt__ (heapq only ever uses <), say what functools.total_ordering adds and why it is not needed for heapq, and explain why (-len(w), w) works as a tuple key for 'longest first then alphabetical ascending' but cannot express descending alphabetical order. Example: words=['pear', 'apple', 'fig', 'apple', 'kiwi'], order='lex_desc' -> ['pear', 'kiwi', 'fig', 'apple', 'apple']; words=['pear', 'apple', 'fig', 'kiwi', 'plum', 'date'], order='len_desc_lex_desc' -> ['apple', 'plum', 'pear', 'kiwi', 'date', 'fig']; words=[], order='lex_desc' -> [].
**Asked at:** The Python heapq documentation recipe on entry counters, removed-task markers and wrapper classes (search snippets of docs.python.org pages; WebFetch of docs.python.org failed with getaddrinfo ENOTFOUND, so the page was not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Custom ordering for `heapq` through a wrapper class with a reversed `__lt__`, since there is no `key=` and strings cannot be negated.

**Say this first (1 line):** "heapq only calls `<`, so I wrap each word in a class whose `__lt__` is reversed, and the min-heap then pops the largest first."

**Brute force:** `sorted(words, reverse=True)`, or `sorted(words, key=lambda w: (len(w), w), reverse=True)` for the second order. O(n log n) and the checker in the code.

**Optimal:**
- Wrapper: `__slots__ = ('w',)` to save memory, `__lt__(self, other): return self.w > other.w` for `lex_desc`, and compare the pair `(len, string)` the same way for `len_desc_lex_desc`.
- Heapify the wrappers, pop n times, read `.w`.
- Why only `__lt__`: heapq's sift routines use `<` and nothing else. `functools.total_ordering` would add `>`, `<=`, `>=` from `__lt__` and `__eq__`. Harmless but unused, and slower than hand-written methods; skip it here.
- Tuple keys: `(-len(w), w)` gives longest first and then ascending alphabetical. You cannot negate a string, so the second field cannot be reversed. The tempting wrong answer is shown in the code (it pops date, kiwi, pear, plum).
- A workaround exists: negate every code point, `tuple(-ord(c) for c in w) + (1,)`. The sentinel matters: without it a prefix like "ab" sorts before "abc" (shorter tuple is smaller) which is wrong for descending order. The code verifies the sentinel version on 1000 random lists.

**Complexity:**
- heapify O(n), n pops O(n log n). Each comparison costs O(string length), so add a factor of the word length for string compares.
- Space O(n) for the wrappers, each slotted object holds one reference.

**Dry run:** words = pear, apple, fig, apple, kiwi, `lex_desc`. The reversed `__lt__` makes the largest string the "smallest" item.
| pop | heap top | why |
|---|---|---|
| 1 | pear | p is the largest first letter |
| 2 | kiwi | k > f > a |
| 3 | fig | |
| 4 | apple | |
| 5 | apple | duplicate, no tie problem: `__lt__` returns False both ways and equal wrappers just come out one after another |

**Code:**
```python
import functools, heapq, random

class Rev:                                       # pops the LARGEST string first
    __slots__ = ('w',)
    def __init__(self, w): self.w = w
    def __lt__(self, other): return self.w > other.w          # reversed on purpose

class LenRev:                                    # longer first, then larger string first
    __slots__ = ('w',)
    def __init__(self, w): self.w = w
    def __lt__(self, other): return (len(self.w), self.w) > (len(other.w), other.w)

def pop_order(words, order):
    cls = Rev if order == 'lex_desc' else LenRev
    h = [cls(w) for w in words]
    heapq.heapify(h)
    return [heapq.heappop(h).w for _ in range(len(words))]

def brute(words, order):
    if order == 'lex_desc': return sorted(words, reverse=True)
    return sorted(words, key=lambda w: (len(w), w), reverse=True)

assert pop_order(['pear','apple','fig','apple','kiwi'], 'lex_desc') == ['pear','kiwi','fig','apple','apple']
assert pop_order(['pear','apple','fig','kiwi','plum','date'], 'len_desc_lex_desc') == ['apple','plum','pear','kiwi','date','fig']
assert pop_order([], 'lex_desc') == []

rng = random.Random(30)
for _ in range(1500):
    ws = [''.join(rng.choice('abc') for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(0, 12))]
    for o in ('lex_desc', 'len_desc_lex_desc'):
        assert pop_order(ws, o) == brute(ws, o), (ws, o)
print("1500 random cases x 2 orders match sorted()")

# heapq only ever uses <, so total_ordering adds nothing here
@functools.total_ordering
class RevTO:
    def __init__(self, w): self.w = w
    def __eq__(self, o): return self.w == o.w
    def __lt__(self, o): return self.w > o.w
print("total_ordering gives >, <=, >= for free:", RevTO('a') >= RevTO('b'), "(not needed by heapq)")

# tuple key (-len(w), w): longest first, then ASCENDING alphabetical, not descending
ws = ['pear', 'plum', 'date', 'fig', 'kiwi']
h = []
for w in ws: heapq.heappush(h, (-len(w), w))
print("(-len, w) pops:", [heapq.heappop(h)[1] for _ in ws], "| wanted:", brute(ws, 'len_desc_lex_desc'))
print("strings have no unary minus:", end=" ")
try: -'abc'
except TypeError as e: print(e)

# A tuple-of-negated-code-points trick DOES work for descending alphabetical, but only with a sentinel
def neg_key(w): return tuple(-ord(c) for c in w) + (1,)       # sentinel makes a longer word with the same prefix come first
def neg_key_no_sentinel(w): return tuple(-ord(c) for c in w)
ws = ['ab', 'abc', 'b', 'ba']
print("with sentinel   :", sorted(ws, key=neg_key), "| expected", sorted(ws, reverse=True))
print("without sentinel:", sorted(ws, key=neg_key_no_sentinel), "(prefix 'ab' wrongly before 'abc')")
for _ in range(1000):
    ws = [''.join(rng.choice('abc') for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(0, 10))]
    assert sorted(ws, key=neg_key) == sorted(ws, reverse=True)
print("sentinel trick verified on 1000 random lists")

# Wrapper that carries a payload: tie on the key is harmless because only the key is compared
class Item:
    __slots__ = ('w', 'payload')
    def __init__(self, w, payload): self.w, self.payload = w, payload
    def __lt__(self, o): return self.w > o.w
h = [Item('a', {'id': 1}), Item('a', {'id': 2})]
heapq.heapify(h)
print("dict payload with tied keys, no TypeError:", heapq.heappop(h).payload)
```

**Output (my run):**
```text
1500 random cases x 2 orders match sorted()
total_ordering gives >, <=, >= for free: True (not needed by heapq)
(-len, w) pops: ['date', 'kiwi', 'pear', 'plum', 'fig'] | wanted: ['plum', 'pear', 'kiwi', 'date', 'fig']
strings have no unary minus: bad operand type for unary -: 'str'
with sentinel   : ['ba', 'b', 'abc', 'ab'] | expected ['ba', 'b', 'abc', 'ab']
without sentinel: ['b', 'ba', 'ab', 'abc'] (prefix 'ab' wrongly before 'abc')
sentinel trick verified on 1000 random lists
dict payload with tied keys, no TypeError: {'id': 2}
```

**Edge cases:**
- Empty list: nothing to pop.
- Duplicates: tied wrappers are fine, only `<` is called and the heap does not need strict ordering.
- Prefix pairs ("ab", "abc") under `len_desc_lex_desc`: length decides first, so no prefix trouble. Under the negated-codes trick the sentinel is what saves you.
- A wrapper carrying a dict payload compares only the key, so ties never reach the dict (the code pops a tied pair without error). Tuples would have raised TypeError there.
- Not defining `__eq__`: heapq does not need it.

**Follow-ups:**
- Max-heap of integers? Negate: push -x, pop and negate. Works for ints, floats, not strings.
- Reverse a string key without a class? For lowercase letters only, translate each letter to its mirror letter and append a sentinel; fragile, so prefer the class.
- Speed? Tuples compare in C; a Python `__lt__` is several times slower. Use tuple keys when the order allows.

**Common mistakes:**
- Defining `__gt__` and expecting heapq to use it.
- Reversing the comparison on only one field of a composite order.
- Using `-ord(c)` tuples without a sentinel.
- Assuming `(-len(w), w)` also reverses the alphabet.

---

### Q31 ⭐⭐ 🟡 Priority queue with removal by lazy deletion. Implement a min-priority queue of integers (a multiset) that supports push(x), remove(x) (delete ONE occurrence of x if present), pop() and top() in amortised O(log n), using heapq without deleting from the middle: keep a Counter of pending deletions and discard stale heap entries when they reach the top (compare Part 4 Q38 for the same idea on a stack). `ops` is a list of ['push', x], ['remove', x], ['pop'], ['top'], ['size']; return the list of outputs of every non-push operation in order: remove gives True if an occurrence was present and False otherwise, pop gives the smallest value (and removes it) or None when empty, top gives the smallest value or None, size gives the number of live (not removed) elements. 0 <= len(ops) <= 10^5. State why the heap list never holds more entries than the number of pushes and why each stale entry is popped at most once. Example: ops=[['push', 3], ['push', 1], ['push', 2], ['remove', 1], ['top'], ['pop'], ['size'], ['remove', 9]] -> [True, 2, 2, 1, False]; ops=[['push', 5], ['push', 5], ['remove', 5], ['pop'], ['pop'], ['top']] -> [True, 5, null, null]; ops=[['pop'], ['size']] -> [null, 0].
**Asked at:** The Python heapq documentation recipe on entry counters, removed-task markers and wrapper classes (search snippets of docs.python.org pages; WebFetch of docs.python.org failed with getaddrinfo ENOTFOUND, so the page was not opened) | Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Lazy deletion. `heapq` can only remove the root cheaply, so a removal just marks the value dead and the heap throws it away when it surfaces.

**Say this first (1 line):** "I keep a Counter of pending deletions, `remove` bumps it, and `top`/`pop` discard dead entries from the root before answering, so everything is amortised O(log n)."

**Brute force:** A plain list: push is append, remove is `list.remove` O(n), top and pop find `min` O(n). O(n) per operation, O(n^2) for 10^5 operations. Also `h.remove(x); heapify(h)` is O(n) per remove (shown in the code).

**Optimal:**
- State: the heap list `h` (may contain stale values), `live[x]` live copies of x, `dead[x]` pending deletions, and `n` live count.
- push(x): `heappush`, `live[x] += 1`.
- remove(x): if `live[x] > 0`: `live[x] -= 1`, `dead[x] += 1`, return True; else False. Do not touch the heap.
- clean: while the root has `dead[root] > 0`: pop it and decrement `dead`.
- top and pop call clean first. Equal values are interchangeable, so which copy is "the dead one" does not matter.
- Why `live` as well as `dead`: removing a value that was never pushed (or was already popped) must return False and must not leave a phantom deletion that eats a later push.

**Complexity:**
- Each heap entry is pushed once and popped once, so the heap never holds more entries than the number of pushes, and the total number of stale pops over the whole run is at most the number of removes. So all operations are amortised O(log n), total O(n log n) for n operations.
- Space O(pushes), not O(live): stale entries stay until they reach the root. A removed large value can sit at the bottom for a long time. If that matters, rebuild when stale entries exceed half the heap.
- The code asserts `len(h) <= pushes` after every operation, and on a 100,000-push run shows 50,000 live pops plus 50,000 stale discards in total.

**Dry run:** push 3, push 1, push 2, remove 1, top, pop, size, remove 9.
| op | heap list | live | dead | output |
|---|---|---|---|---|
| push 3,1,2 | [1,3,2] | 1,2,3 | none | |
| remove 1 | [1,3,2] | 2,3 | 1:1 | True |
| top | clean pops 1 -> [2,3] | | | 2 |
| pop | [3] | 3 | | 2 |
| size | | | | 1 |
| remove 9 | | | | False |
Output [True, 2, 2, 1, False].

**Code:**
```python
import heapq, random
from collections import Counter

class LazyMinPQ:
    def __init__(self):
        self.h = []                  # may hold stale (already removed) values
        self.live = Counter()        # live occurrences per value
        self.dead = Counter()        # pending deletions per value (stale copies still inside the heap)
        self.n = 0                   # live count
        self.pushes = 0

    def push(self, x):
        heapq.heappush(self.h, x); self.live[x] += 1; self.n += 1; self.pushes += 1

    def remove(self, x):
        if self.live[x] > 0:         # only if a live copy exists
            self.live[x] -= 1; self.dead[x] += 1; self.n -= 1
            return True
        return False

    def _clean(self):                # drop stale entries that reached the top (each at most once)
        while self.h and self.dead[self.h[0]] > 0:
            self.dead[self.h[0]] -= 1
            heapq.heappop(self.h)

    def top(self):
        self._clean()
        return self.h[0] if self.h else None

    def pop(self):
        self._clean()
        if not self.h: return None
        x = heapq.heappop(self.h); self.live[x] -= 1; self.n -= 1
        return x

    def size(self): return self.n

def run(ops):
    pq, out = LazyMinPQ(), []
    for op in ops:
        if op[0] == 'push': pq.push(op[1])
        elif op[0] == 'remove': out.append(pq.remove(op[1]))
        elif op[0] == 'pop': out.append(pq.pop())
        elif op[0] == 'top': out.append(pq.top())
        else: out.append(pq.size())
        assert len(pq.h) <= pq.pushes                 # never more entries than pushes
    return out

def brute(ops):                                       # plain list, O(n) per operation
    a, out = [], []
    for op in ops:
        if op[0] == 'push': a.append(op[1])
        elif op[0] == 'remove':
            if op[1] in a: a.remove(op[1]); out.append(True)
            else: out.append(False)
        elif op[0] == 'pop':
            if a: m = min(a); a.remove(m); out.append(m)
            else: out.append(None)
        elif op[0] == 'top': out.append(min(a) if a else None)
        else: out.append(len(a))
    return out

assert run([['push',3],['push',1],['push',2],['remove',1],['top'],['pop'],['size'],['remove',9]]) == [True,2,2,1,False]
assert run([['push',5],['push',5],['remove',5],['pop'],['pop'],['top']]) == [True,5,None,None]
assert run([['pop'],['size']]) == [None, 0]
assert run([]) == []

rng = random.Random(31)
for _ in range(2000):
    ops = []
    for _ in range(rng.randint(0, 30)):
        r = rng.random()
        if r < .4: ops.append(['push', rng.randint(0, 5)])
        elif r < .6: ops.append(['remove', rng.randint(0, 5)])
        elif r < .75: ops.append(['pop'])
        elif r < .9: ops.append(['top'])
        else: ops.append(['size'])
    assert run(ops) == brute(ops), ops
print("2000 random op sequences match the list brute force")

# stale entries are popped at most once each: count heappop calls on a big run
big = LazyMinPQ()
n = 100000
for i in range(n): big.push(i % 1000)
for i in range(n // 2): big.remove((i * 7) % 1000)
total_pops = 0
while big.top() is not None:
    big.pop(); total_pops += 1
print("n=100000 pushes, 50000 removes ->", total_pops, "live pops; heap list ended at", len(big.h), "entries")

# why not remove-from-the-middle: heap.remove(x) is O(n) and heapify is O(n) again
h = [1, 5, 2, 9, 7]; heapq.heapify(h)
h.remove(5); heapq.heapify(h)
print("list.remove + heapify works but costs O(n) per remove:", h)
```

**Output (my run):**
```text
2000 random op sequences match the list brute force
n=100000 pushes, 50000 removes -> 50000 live pops; heap list ended at 0 entries
list.remove + heapify works but costs O(n) per remove: [1, 2, 9, 7]
```

**Edge cases:**
- Empty queue: pop and top give None, size 0.
- Duplicates: push 5 twice, remove 5 once; the first pop gives 5 and the second None.
- Removing a value then pushing it again: `live` and `dead` both reflect it and the new copy simply cancels one dead entry in the heap (equal values are interchangeable).
- Removing a value that is not present: False, no state change.
- Size counts live elements only, not `len(h)`.

**Follow-ups:**
- Update an element's priority? Same trick: mark the old entry dead, push the new one. The heapq docs recipe uses a removed-task marker for it. `heapq` has no decrease-key (Part 9 covers indexed heaps and Dijkstra).
- Part 4 Q38 (max stack) uses the same idea on a stack.
- When is lazy deletion bad? Many removals of far-from-root values: memory stays high; compact by rebuilding.

**Common mistakes:**
- Calling `h.remove(x)` and then `heapify`: O(n) per removal.
- Not cleaning before `top`, returning a dead root.
- Using only `dead` and returning True for a remove of an absent value.
- Reporting `len(h)` as the size.

---

### Q32 ⭐⭐ 🟡 Activity selection and the exchange argument. Activities are half-open [start, end) with start < end (1 <= len <= 10^5), and two activities are compatible when one ends at or before the other starts. Return the maximum number of pairwise compatible activities with the earliest-finish-first greedy. Prove it by exchange: take any optimal solution, replace its first activity by the activity with the earliest end, and the solution stays valid and no smaller. Then show the other two tempting rules fail with counter-examples: 'shortest activity first' and 'earliest start first' (each fails already with three activities, and no counter-example with two activities exists; the checker verifies both claims exhaustively over times 0 to 6). Compare with the two-pointer greedy for boats in Part 2 Q37. Example: activities=[[1, 4], [3, 5], [0, 6], [5, 7], [3, 9], [5, 9], [6, 10], [8, 11], [8, 12], [2, 14], [12, 16]] -> 4; activities=[[1, 3], [2, 4], [3, 5]] -> 2; activities=[[0, 10], [1, 2], [3, 4]] -> 2; activities=[[0, 3], [2, 4], [3, 6], [4, 7]] -> 2.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Greedy by earliest finish, justified by an exchange argument. Interval scheduling.

**Say this first (1 line):** "Sort by end time and take every activity that starts at or after the last chosen end, because finishing earliest leaves the most room."

**Brute force:** Try every subset and keep the largest one with no overlaps: 2^n subsets times O(n^2) checks. The code does it for n up to 9, bitmask style.

**Optimal:**
- Sort by end. Keep `end` = end of the last chosen activity. Take an activity if `start >= end` (half-open, touching is allowed), then set `end` to its end.
- Exchange proof: let G be the activity with the earliest end. Take any optimal set O and let X be its first activity (by end). Replace X by G. G ends no later than X, so everything else in O still starts after G ends. The set stays valid and has the same size, so some optimal set contains G. Remove G and everything overlapping it and repeat the argument on the rest.
- Why other rules fail:
  - Shortest first: [0,3] [2,4] [3,6]. The short [2,4] blocks both others, answer 1; the optimum is [0,3] and [3,6], answer 2.
  - Earliest start first: [0,10] [1,2] [3,4]. It takes [0,10], answer 1; optimum 2.
- Exhaustive facts (code, times 0 to 6, all ordered lists of 1 to 3 activities): both wrong rules fail on 0 lists of size 1 and 2, so no 2-activity counter-example exists, and fail on 34 (shortest) and 1218 (earliest start) lists of size 3. Counting only failures that happen for every input order (so no tie-break luck): earliest start has 112 such sets, shortest-first has exactly one, the set {[0,3], [2,4], [3,6]}. Earliest finish had 0 failures on the same set.

**Complexity:**
- Sort O(n log n), one pass O(n). Space O(n) for the sorted copy. No recursion, so n = 10^5 is fine.
- Ties in end time do not matter: after sorting, any choice among equal ends yields the same count (the exchange argument allows either).

**Dry run:** [1,3] [2,4] [3,5] sorted by end: same order.
| activity | start >= end? | action | end |
|---|---|---|---|
| [1,3] | 1 >= -inf | take | 3 |
| [2,4] | 2 >= 3 no | skip | 3 |
| [3,5] | 3 >= 3 yes (half-open) | take | 5 |
Answer 2.

**Code:**
```python
import itertools, random

def activity(acts):                                   # earliest finish first
    cnt, end = 0, -10**18
    for s, e in sorted(acts, key=lambda a: a[1]):
        if s >= end: cnt += 1; end = e
    return cnt

def greedy_by(acts, key):                             # generic rule: scan in key order, take if compatible with all chosen
    chosen = []
    for s, e in sorted(acts, key=key):
        if all(e <= c[0] or c[1] <= s for c in chosen): chosen.append([s, e])
    return len(chosen)

def brute(acts):
    best = 0
    for m in range(1 << len(acts)):
        sel = [acts[i] for i in range(len(acts)) if m >> i & 1]
        if all(a[1] <= b[0] or b[1] <= a[0] for a, b in itertools.combinations(sel, 2)):
            best = max(best, len(sel))
    return best

assert activity([[1,4],[3,5],[0,6],[5,7],[3,9],[5,9],[6,10],[8,11],[8,12],[2,14],[12,16]]) == 4
assert activity([[1,3],[2,4],[3,5]]) == 2
assert activity([[0,10],[1,2],[3,4]]) == 2
assert activity([[0,3],[2,4],[3,6],[4,7]]) == 2

rng = random.Random(32)
for _ in range(1500):
    acts = []
    for _ in range(rng.randint(1, 9)):
        s = rng.randint(0, 8); acts.append([s, rng.randint(s + 1, 9)])
    assert activity(acts) == brute(acts) == greedy_by(acts, key=lambda a: a[1]), acts
print("1500 random cases: earliest-finish greedy == brute force")

# Exhaustive: the two wrong rules over ALL ordered lists of 1..3 activities with times 0..6
ivs = [[s, e] for s in range(7) for e in range(s + 1, 7)]
rules = {"shortest first": lambda a: a[1] - a[0], "earliest start first": lambda a: a[0]}
for name, key in rules.items():
    fail = {1: 0, 2: 0, 3: 0}; sets3 = set()
    for n in (1, 2, 3):
        for acts in itertools.product(ivs, repeat=n):
            acts = list(map(list, acts))
            if greedy_by(acts, key) != brute(acts):
                fail[n] += 1
                if n == 3: sets3.add(tuple(sorted(map(tuple, acts))))
    # failures that survive EVERY input order (so they do not depend on how ties are broken)
    robust = sorted(s3 for s3 in sets3
                    if all(greedy_by([list(x) for x in p], key) != brute([list(x) for x in p])
                           for p in itertools.permutations(s3)))
    assert fail[1] == fail[2] == 0 and robust
    print(f"{name}: failing lists with 1, 2, 3 activities = {fail[1]}, {fail[2]}, {fail[3]}; "
          f"order-independent failing 3-sets = {len(robust)}, e.g. {[list(x) for x in robust[0]]}")
# earliest finish never fails on the same exhaustive set
for n in (1, 2, 3):
    for acts in itertools.product(ivs, repeat=n):
        acts = list(map(list, acts))
        assert activity(acts) == brute(acts)
print("earliest finish first: 0 failures on the same exhaustive set")

# the prompt's counter-examples, spelled out
print("shortest first on [[0,3],[2,4],[3,6]]:", greedy_by([[0,3],[2,4],[3,6]], rules["shortest first"]), "vs optimal", brute([[0,3],[2,4],[3,6]]))
print("earliest start on [[0,10],[1,2],[3,4]]:", greedy_by([[0,10],[1,2],[3,4]], rules["earliest start first"]), "vs optimal", brute([[0,10],[1,2],[3,4]]))

# scale: n = 100000, one sort + one pass
big = []
for _ in range(100000):
    s = rng.randint(0, 10**6); big.append([s, s + rng.randint(1, 20)])
print("n=100000 ->", activity(big), "activities")
```

**Output (my run):**
```text
1500 random cases: earliest-finish greedy == brute force
shortest first: failing lists with 1, 2, 3 activities = 0, 0, 34; order-independent failing 3-sets = 1, e.g. [[0, 3], [2, 4], [3, 6]]
earliest start first: failing lists with 1, 2, 3 activities = 0, 0, 1218; order-independent failing 3-sets = 112, e.g. [[0, 3], [1, 2], [2, 3]]
earliest finish first: 0 failures on the same exhaustive set
shortest first on [[0,3],[2,4],[3,6]]: 1 vs optimal 2
earliest start on [[0,10],[1,2],[3,4]]: 1 vs optimal 2
n=100000 -> 53755 activities
```

**Edge cases:**
- Single activity: 1.
- All identical activities: 1.
- Touching activities [1,3] [3,5]: compatible because intervals are half-open.
- One huge activity covering the rest: skipped by the end rule, as in [0,10] [1,2] [3,4].
- Equal ends with different starts: both orders give the same count.

**Follow-ups:**
- Weighted activities? Greedy fails; it needs DP with binary search (Part 10).
- Minimum number of intervals to remove to make the rest non-overlapping? n minus this answer.
- Part 2 Q37 (boats) is also an exchange-argument greedy but with two pointers on weights.

**Common mistakes:**
- Using `start > end` (strict) when touching is allowed.
- Sorting by start time.
- Choosing the shortest activity.
- Proving greedy by "it worked on my examples".

---

### Q33 ⭐⭐ 🟡 When greedy fails: coins. `coins` is a strictly increasing list of positive integers with coins[0] == 1 (1 <= len <= 10, coins[-1] <= 1000). Largest-coin-first greedy makes change for amount a by repeatedly taking the largest coin that fits. Return the smallest amount a at which greedy uses MORE coins than the optimum, or -1 if greedy is optimal for every amount. The classic counter-example is coins [1, 3, 4] and amount 6 (greedy 4 + 1 + 1 uses three coins, 3 + 3 uses two). It is enough to test amounts below coins[-1] + coins[-2] (a theorem of Kozen and Zaks; the checker tests the bound exhaustively for every coin system with largest coin <= 12 against amounts up to 200); the optimum for each tested amount comes from the DP 'fewest coins' recurrence, which is the topic of Part 10. Explain why the US system [1, 5, 10, 25] is safe and why greedy needs a proof, not a few examples. Example: coins=[1, 3, 4] -> 6; coins=[1, 5, 10, 25] -> -1; coins=[1, 5, 6, 9] -> 11; coins=[1] -> -1; coins=[1, 2, 5, 10, 20, 50, 100] -> -1.
**Asked at:** Canonical coin-system literature (Kozen and Zaks on optimal bounds for change-making, an arXiv combinatorics-of-change-making paper, Cornell and TAMU course handouts; search snippets only, not opened) | Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Greedy versus DP. Testing whether largest-coin-first is optimal needs the optimum from the fewest-coins DP, which is the topic of Part 10.

**Say this first (1 line):** "Greedy is only right for some coin systems, so I compare it with the fewest-coins DP at every amount below the two largest coins added together and return the first amount where greedy is worse."

**Brute force:** Compare greedy with the DP for every amount up to a large limit (the code uses 200 in the exhaustive run and 600 for random systems). Correct for tested ranges but with no guarantee beyond them, which is why a proven bound matters.

**Optimal:**
- Bound (Kozen and Zaks): if the system is not canonical, the smallest amount where greedy is wrong is below coins[-1] + coins[-2]. So we only test amounts below that. Check with the DP: `opt[a] = 1 + min(opt[a - c])`, and greedy by repeated division from the biggest coin.
- Return the first a with greedy count > opt count, else -1.
- The code checks the theorem's use exhaustively: all 2048 systems with largest coin up to 12 (1 plus any subset of 2..12), against amounts to 200. The bound-limited answer equals the range-200 answer in every one, and in all 1854 non-canonical ones the first failure is below c_m + c_(m-1) and above c_3 + 1 (the lower bound). 300 random bigger systems (coins up to 80, range 600) agree too.
- Why [1,5,10,25] is safe: the bound tells us to check amounts below 35, the DP finds no failure, and the theorem turns that finite check into a guarantee. A hand check on a few amounts would prove nothing.
- Why a proof, not examples: [1,5,6,9] is greedy-optimal for every amount from 1 to 10 and fails at 11 (9+1+1 is three coins, 5+6 is two). The coins 1 3 4 fail at 6.

**Complexity:**
- Amounts up to L = c_m + c_(m-1) at most 2000. The DP costs O(L x m) and greedy O(m) per amount, so O(L x m) overall: about 20,000 steps in the worst case here. Space O(L).
- Without the bound you would have no stopping point.

**Dry run:** coins [1,3,4], bound 4 + 3 = 7, test a = 1..6.
| a | greedy | optimum |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 (1+1) | 2 |
| 3 | 1 | 1 |
| 4 | 1 | 1 |
| 5 | 2 (4+1) | 2 |
| 6 | 3 (4+1+1) | 2 (3+3) |
First failure 6.

**Code:**
```python
import itertools, random

def tables(coins, limit):
    opt = [0] + [10**9] * limit; gr = [0] * (limit + 1)
    for a in range(1, limit + 1):
        opt[a] = min(opt[a - c] + 1 for c in coins if c <= a)      # fewest-coins DP (Part 10 topic)
        r, g = a, 0
        for c in reversed(coins): g += r // c; r %= c               # largest-first greedy
        gr[a] = g
    return opt, gr

def first_bad(coins):                                                # uses the Kozen-Zaks bound
    limit = coins[-1] + (coins[-2] if len(coins) > 1 else 0)
    opt, gr = tables(coins, limit)
    for a in range(1, limit + 1):
        if gr[a] > opt[a]: return a
    return -1

def brute(coins, limit=200):                                         # no theorem: test a long range
    opt, gr = tables(coins, limit)
    for a in range(1, limit + 1):
        if gr[a] > opt[a]: return a
    return -1

assert first_bad([1,3,4]) == 6
assert first_bad([1,5,10,25]) == -1
assert first_bad([1,5,6,9]) == 11
assert first_bad([1]) == -1
assert first_bad([1,2,5,10,20,50,100]) == -1

# exhaustive: every coin system with largest coin <= 12 (1 plus any subset of 2..12), amounts to 200
systems = bad = 0
lower_ok = True
for mask in range(1 << 11):
    coins = [1] + [c for c in range(2, 13) if mask >> (c - 2) & 1]
    systems += 1
    a, b = first_bad(coins), brute(coins, 200)
    assert a == b, coins
    if b != -1:
        bad += 1
        m = len(coins)
        assert b < coins[-1] + coins[-2], coins                      # Kozen-Zaks upper bound
        if m >= 3: assert b > coins[2] + 1, coins                    # lower bound c_3 + 1 (1-indexed c_3)
print(f"{systems} coin systems (largest <= 12): bound-limited check == range-200 check; {bad} non-canonical, all with first failure < c_m + c_(m-1) and > c_3 + 1")

# larger random systems: bound against a long range (amount to 600)
rng = random.Random(33)
for _ in range(300):
    coins = sorted({1} | {rng.randint(2, 80) for _ in range(rng.randint(1, 5))})
    assert first_bad(coins) == brute(coins, 600), coins
print("300 random systems (coins <= 80, amounts to 600): same answer")

# the tightness of the bound can be seen on [1, 3, 4]: first failure 6 < 4 + 3 = 7
print("[1,3,4] ->", first_bad([1,3,4]), "| [1,5,6,9] ->", first_bad([1,5,6,9]), "| US [1,5,10,25] ->", first_bad([1,5,10,25]))
opt, gr = tables([1,5,6,9], 12)
print("[1,5,6,9] amount 11: greedy", gr[11], "coins, optimum", opt[11], "coins")

# 'looks fine on a few examples': coins [1,5,6,9] is greedy-optimal for every amount below 11
print("amounts below 11 where greedy is fine:", all(gr[a] == opt[a] for a in range(1, 11)))
```

**Output (my run):**
```text
2048 coin systems (largest <= 12): bound-limited check == range-200 check; 1854 non-canonical, all with first failure < c_m + c_(m-1) and > c_3 + 1
300 random systems (coins <= 80, amounts to 600): same answer
[1,3,4] -> 6 | [1,5,6,9] -> 11 | US [1,5,10,25] -> -1
[1,5,6,9] amount 11: greedy 3 coins, optimum 2 coins
amounts below 11 where greedy is fine: True
```

**Edge cases:**
- [1]: only one coin, greedy equals the optimum, -1.
- Two coins [1, c]: always canonical, -1 (the code finds no failure in any such system within the exhaustive run).
- Coin 1 present: every amount is reachable, so `opt` is always finite.
- Powers like [1,2,4,8]: canonical.
- Systems where the first failure is far above the second-largest coin: the bound still stays below c_m + c_(m-1).

**Follow-ups:**
- Is there a quick certificate? Pearson's polynomial-time test exists in the literature; the sources I found were snippet-only, so I do not claim details.
- What do you do when greedy fails? Use DP (Part 10): `opt[a] = min(opt[a - c]) + 1`.
- Why does the US system work but [1,3,4] not? No short answer; it needs the theorem or a proof by cases.

**Common mistakes:**
- Declaring greedy optimal after testing a few amounts.
- Testing only multiples or amounts larger than the bound but not those below it.
- Forgetting that 1 must be a coin, so amounts are always reachable.
- Confusing "fewest coins" greedy with "number of ways" counting.

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


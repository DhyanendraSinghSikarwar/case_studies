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

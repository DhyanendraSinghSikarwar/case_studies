# Book 5 Part 4, Q21-Q30 answers (Wave B)


### Q21 ⭐⭐ 🟡 Car fleet. n cars drive in one direction along a one-lane road to a target at mile `target`. Car i starts at `position[i]` (distinct) with constant `speed[i]`; a car cannot pass the one ahead and instead slows to its speed and drives bumper to bumper, forming a fleet (a lone car is a fleet; a car that catches up exactly at the target joins that fleet). Return the number of fleets that arrive. Sort by start position descending, compute each car's arrival time, and keep a stack of fleet times (a car slower to arrive than the fleet ahead starts a new fleet). Example: (12,[10,8,0,5,3],[2,4,1,1,3]) -> 3; (10,[3],[3]) -> 1; (100,[0,2,4],[4,2,1]) -> 1.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Monotonic stack of arrival times. Sort by position, then the cars ahead decide whether a car is blocked.

**Say this first (1 line):** "Sort cars from the front of the road to the back, compute each car's solo arrival time, and a car starts a new fleet only if it needs strictly longer than the fleet ahead; otherwise it merges."

**Brute force:** A car's real arrival time is the maximum solo time over itself and every car ahead of it, because it can never beat any of them. Fleets are the distinct real arrival times. O(n^2) time. I also wrote an exact simulation on a time grid as a second, independent checker.

**Optimal:**
- Sort by `position` descending (closest to the target first). Time `t = (target - pos) / speed`.
- Keep a stack of fleet times. If the new car's `t` is strictly greater than the top, it never catches that fleet: push. Otherwise it catches up (or arrives exactly with it), joins the fleet, and nothing is pushed.
- Invariant: the stack is strictly increasing from bottom to top. Each entry is one fleet's real arrival time.
- Observation: only the top is ever read, so the stack can be a single variable `slowest`. I keep the stack in the code because it is the pattern the interviewer expects, and I say the shortcut out loud.
- Ties use `>` not `>=`: equal time means it catches up exactly at the target and joins.
- Floats are safe here: IEEE division is correctly rounded, so equal rationals give equal floats, and different rationals with small integers differ by far more than one ulp. The cross-check uses `Fraction` to prove it on the tested range.

**Complexity:** Sort O(n log n); the stack pass is O(n) because each car is pushed at most once. Space O(n).

**Dry run:** target 12, positions `[10,8,0,5,3]`, speeds `[2,4,1,1,3]`.
- Sorted by position descending: (10,2), (8,4), (5,1), (3,3), (0,1).
- Times: 1.0, 1.0, 7.0, 3.0, 12.0.
- 1.0: stack empty, push. Stack `[1.0]`.
- 1.0: not greater than 1.0, joins. 7.0: greater, push. `[1.0, 7.0]`.
- 3.0: not greater than 7.0, joins the 7.0 fleet.
- 12.0: greater, push. `[1.0, 7.0, 12.0]`. Answer 3.

**Code:**
```python
import random
from fractions import Fraction


def fleets_brute(target, position, speed):
    # real time of car i = max solo time over every car at or ahead of it
    n = len(position)
    solo = [Fraction(target - position[i], speed[i]) for i in range(n)]
    real = set()
    for i in range(n):
        real.add(max(solo[j] for j in range(n) if position[j] >= position[i]))
    return len(real)


def fleets_sim(target, position, speed):
    # exact time-grid simulation (small ints only): cars cannot pass, merge on touch
    n = len(position)
    order = sorted(range(n), key=lambda i: -position[i])        # front first
    pos = {i: Fraction(position[i]) for i in order}
    vel = {i: Fraction(speed[i]) for i in order}
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            a = parent[a]
        return a

    road = list(order)
    dt = Fraction(1, 60)                                        # grid hits every catch-up time
    while road:
        newpos = {}
        prev = None
        for i in road:
            p = min(pos[i] + vel[i] * dt, Fraction(target))
            if prev is not None and p >= newpos[prev]:
                p = newpos[prev]
                vel[i] = vel[prev]
                parent[find(i)] = find(prev)
            newpos[i] = p
            prev = i
        pos.update(newpos)
        road = [i for i in road if pos[i] < target]
    return len({find(i) for i in range(n)})


def car_fleet(target, position, speed):
    stack = []                                                   # strictly increasing times
    for p, s in sorted(zip(position, speed), reverse=True):
        t = (target - p) / s
        if not stack or t > stack[-1]:
            stack.append(t)
    return len(stack)


examples = [(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3], 3), (10, [3], [3], 1), (100, [0, 2, 4], [4, 2, 1], 1)]
for t, p, s, want in examples:
    got = car_fleet(t, p, s)
    assert got == fleets_brute(t, p, s) == fleets_sim(t, p, s) == want
    print((t, p, s), "->", got)

assert car_fleet(5, [], []) == 0
assert car_fleet(10, [0, 5], [1, 1]) == 2            # same speed, never meet
assert car_fleet(10, [0, 5], [5, 1]) == 1            # solo times 5.0 and 2.0: the rear car is faster and joins
assert car_fleet(10, [4, 0], [3, 6]) == 1            # solo times about 2.0 and 1.67: joins
assert car_fleet(10, [6, 0], [2, 5]) == 1            # times 2.0 and 2.0: exact tie joins
assert car_fleet(10, [6, 0], [2, 5]) == fleets_sim(10, [6, 0], [2, 5])

rng = random.Random(21)
trials = multi = 0
for _ in range(400):
    n = rng.randint(1, 6)
    target = rng.randint(2, 10)
    position = rng.sample(range(target), min(n, target))
    speed = [rng.randint(1, 5) for _ in position]
    a = car_fleet(target, position, speed)
    assert a == fleets_brute(target, position, speed) == fleets_sim(target, position, speed), (target, position, speed)
    trials += 1
    multi += a > 1
for _ in range(300):                                    # larger, brute only
    n = rng.randint(1, 60)
    target = rng.randint(n + 1, 500)
    position = rng.sample(range(target), n)
    speed = [rng.randint(1, 100) for _ in position]
    assert car_fleet(target, position, speed) == fleets_brute(target, position, speed)
    trials += 1
print("random cross-check passed:", trials, "cases;", multi, "of the small ones had 2+ fleets")
```

**Output (my run):**
```
(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]) -> 3
(10, [3], [3]) -> 1
(100, [0, 2, 4], [4, 2, 1]) -> 1
random cross-check passed: 700 cases; 307 of the small ones had 2+ fleets
```
All three examples in the prompt are correct.

**Edge cases:**
- No cars: 0 fleets.
- One car: 1 fleet.
- Same speed, different positions: they never meet, so each is its own fleet.
- Catching up exactly at the target (equal times): one fleet. That is why the comparison is `>`.
- A fast car far behind a slow car right at the front: it joins that slow fleet, and the stack never grows for it.

**Follow-ups:**
- *Can you drop the stack?* Yes. Only the top is compared, so keep one `slowest` variable and a counter.
- *Positions given unsorted?* That is why we sort. Sorting is the O(n log n) part.
- *Why not sort by time?* Order on the road matters (nobody passes), so position is the key.

**Common mistakes:**
- Sorting ascending and then processing from the back without thinking, or sorting speeds and positions separately (loses the pairing).
- Using `>=` and counting a tie as a new fleet.
- Using the speed of the car ahead after a merge instead of the max-time rule.
- Dividing with `//` and losing the fraction.


### Q22 ⭐⭐ 🟡 Design a circular queue (ring buffer). Implement a fixed-capacity FIFO of capacity k with `enQueue(x)` (False if full), `deQueue()` (False if empty), `Front()` and `Rear()` (-1 if empty), `isEmpty()`, `isFull()`, all O(1), backed by a preallocated list with a head index and a size (say why tracking size is simpler than the 'one wasted slot' trick). Example with k=3: enQueue(1), enQueue(2), enQueue(3) -> True, True, True; enQueue(4) -> False; Rear() -> 3; isFull() -> True; deQueue() -> True; enQueue(4) -> True; Rear() -> 4; Front() -> 2.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Ring buffer: a fixed array, a head index and a size, with index arithmetic modulo the capacity.

**Say this first (1 line):** "Preallocate k slots, keep `head` and `size`; the tail slot is `(head + size) % k`, so every operation is O(1) and full/empty are just `size == k` and `size == 0`."

**Brute force:** A Python `list` used as a queue with `pop(0)` and a length check. Dequeue is O(n) because every element shifts. It is my model in the cross-check (together with `collections.deque`).

**Optimal:**
- Fields: `buf = [None] * k`, `head` (index of the oldest item), `size`.
- `enQueue(x)`: if full, False; else write at `(head + size) % k`, `size += 1`.
- `deQueue()`: if empty, False; else `head = (head + 1) % k`, `size -= 1`.
- `Front()`: `buf[head]`. `Rear()`: `buf[(head + size - 1) % k]`. Both -1 when empty.
- Why track `size`: with only `head` and `tail`, `head == tail` means both empty and full. The classic fix is one wasted slot (capacity k+1, full means `(tail+1) % cap == head`), which is easy to get off by one. With a `size` counter, full and empty are unambiguous and all k slots are used.
- Invariant: the live items are exactly the `size` slots starting at `head`, wrapping around.

**Complexity:** Every method is O(1) time. Space O(k), allocated once.

**Dry run:** k = 3.
- enQueue 1, 2, 3: slots `[1,2,3]`, head 0, size 3. enQueue 4: full, False. `Rear()` is slot `(0+3-1)%3 = 2`, value 3.
- deQueue: head 1, size 2. enQueue 4: write at `(1+2)%3 = 0`, so slots `[4,2,3]`, size 3. This is the wrap-around.
- `Rear()` is slot `(1+3-1)%3 = 0`, value 4. `Front()` is slot 1, value 2.

**Code:**
```python
import random
from collections import deque


class MyCircularQueue:
    def __init__(self, k):
        self.k = k
        self.buf = [None] * k
        self.head = 0
        self.size = 0

    def enQueue(self, x):
        if self.size == self.k:
            return False
        self.buf[(self.head + self.size) % self.k] = x
        self.size += 1
        return True

    def deQueue(self):
        if self.size == 0:
            return False
        self.buf[self.head] = None                 # drop the reference
        self.head = (self.head + 1) % self.k
        self.size -= 1
        return True

    def Front(self):
        return -1 if self.size == 0 else self.buf[self.head]

    def Rear(self):
        return -1 if self.size == 0 else self.buf[(self.head + self.size - 1) % self.k]

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.k


class ListModel:                                    # brute force: list.pop(0), O(n) dequeue
    def __init__(self, k):
        self.k, self.a = k, []

    def enQueue(self, x):
        if len(self.a) == self.k:
            return False
        self.a.append(x)
        return True

    def deQueue(self):
        if not self.a:
            return False
        self.a.pop(0)
        return True

    def Front(self):
        return self.a[0] if self.a else -1

    def Rear(self):
        return self.a[-1] if self.a else -1

    def isEmpty(self):
        return not self.a

    def isFull(self):
        return len(self.a) == self.k


q = MyCircularQueue(3)
trace = [q.enQueue(1), q.enQueue(2), q.enQueue(3), q.enQueue(4), q.Rear(), q.isFull(),
         q.deQueue(), q.enQueue(4), q.Rear(), q.Front()]
print(trace)
assert trace == [True, True, True, False, 3, True, True, True, 4, 2]

e = MyCircularQueue(2)
assert e.Front() == -1 and e.Rear() == -1 and e.isEmpty() and not e.isFull() and e.deQueue() is False
one = MyCircularQueue(1)
assert one.enQueue(9) and one.isFull() and not one.enQueue(8) and one.Front() == one.Rear() == 9
assert one.deQueue() and one.isEmpty() and one.enQueue(7) and one.Front() == 7
z = MyCircularQueue(2)                              # 0 is a valid value, -1 only means empty
assert z.enQueue(0) and z.Front() == 0 and z.Rear() == 0

rng = random.Random(22)
ops_run = wraps = 0
for _ in range(300):
    k = rng.randint(1, 6)
    a, b, c = MyCircularQueue(k), ListModel(k), deque()
    for _ in range(60):
        op = rng.choice(["enQueue", "enQueue", "deQueue", "Front", "Rear", "isEmpty", "isFull"])
        if op == "enQueue":
            x = rng.randint(0, 9)
            ra, rb = a.enQueue(x), b.enQueue(x)
            if ra:
                c.append(x)
            assert ra == rb
        elif op == "deQueue":
            ra, rb = a.deQueue(), b.deQueue()
            if rb:
                c.popleft()
            assert ra == rb
        else:
            assert getattr(a, op)() == getattr(b, op)()
        assert a.size == len(b.a) == len(c) and (not c or a.Front() == c[0])
        wraps += (a.head + a.size > k)
        ops_run += 1
print("random cross-check passed:", ops_run, "operations; wrapped states seen:", wraps > 0)
```

**Output (my run):**
```
[True, True, True, False, 3, True, True, True, 4, 2]
random cross-check passed: 18000 operations; wrapped states seen: True
```
The example sequence in the prompt is correct.

**Edge cases:**
- Capacity 1: full and empty alternate.
- Dequeue on empty and enqueue on full return False and change nothing.
- The value 0 is legal; only -1 means "empty" for `Front` and `Rear`. If the problem allowed -1 as data, return `None` or raise instead.
- Wrap-around: the tail index is smaller than the head index.

**Follow-ups:**
- *Make it grow?* Allocate a double-size list and copy the items in logical order starting from `head`: amortised O(1).
- *Overwrite the oldest when full (a log buffer)?* Advance `head` instead of returning False. `deque(maxlen=k)` does this for free.
- *Thread-safe?* Add a lock, or use `queue.Queue` (see Q31 if the interviewer goes there).

**Common mistakes:**
- `Rear()` as `buf[tail - 1]` with a negative or unwrapped index.
- Forgetting `% k` when computing the write slot.
- Using `head == tail` for both full and empty without the wasted slot or a counter.
- Returning 0 instead of -1, or treating a stored 0 as "empty".


### Q23 ⭐⭐ 🟡 A monotonic queue as a data structure. Implement a class with `push(v)` (add to the back), `popLeft(v)` (the caller passes the value of the oldest element still inside, and it leaves), and `getMax()`, each amortised O(1), by keeping a deque of values in non-increasing order. Be careful with duplicates (equal values must both be kept, and `popLeft` removes the front only when it equals v). Then use it to answer window maxima over a stream. Part 2 Q16 poses the sliding-window-maximum prompt and Part 2 Q43 uses the same deque with prefix sums; here the focus is the reusable class and the duplicate rule. Example: push(3), push(1), getMax() -> 3, push(2), popLeft(3), getMax() -> 2, popLeft(1), getMax() -> 2, push(5), getMax() -> 5; separately push(2), push(2), popLeft(2), getMax() -> 2.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Monotonic deque (values kept in non-increasing order) wrapped as a reusable max-queue.

**Say this first (1 line):** "Keep a deque of candidates in non-increasing order: on push, drop strictly smaller values from the back; on popLeft, drop the front only if it equals the leaving value; the max is always the front."

**Brute force:** Keep every element in a plain list/deque and compute `max(...)` on each `getMax`. O(n) per query. It is my model in the cross-check.

**Optimal:**
- `push(v)`: while the back is strictly smaller than `v`, pop it. Then append `v`.
- `popLeft(v)`: if the deque front equals `v`, pop it from the left. Otherwise do nothing, because that value was already thrown away as a dominated candidate.
- `getMax()`: the front.
- Why a smaller element at the back can go: `v` is newer (it leaves later) and bigger, so the smaller one can never be the maximum again.
- Why equal values stay: two equal 2s leave at different times. If the older one is dropped on push, then `popLeft(2)` for the older one would remove the only copy and `getMax` would be wrong while the newer 2 is still inside.
- Invariant: the deque is non-increasing, and it is a subsequence of the live elements that contains the max of every suffix.
- Window maxima over a stream: push each new value; once the window is full, record `getMax()` and call `popLeft(oldest)`.

**Complexity:** Every element is appended once and removed at most once, so any sequence of m operations is O(m) total, amortised O(1) each. Space O(window) in the worst case (a decreasing sequence keeps everything).

**Dry run:** push 3: `[3]`. push 1: `[3,1]`. `getMax` 3. push 2: pops 1, then `[3,2]`. `popLeft(3)`: front is 3, so `[2]`. `getMax` 2. `popLeft(1)`: front is 2, not 1, so nothing (the 1 was already dropped). `getMax` 2. push 5: pops 2, `[5]`. `getMax` 5.
Duplicates: push 2, push 2: `[2,2]` (equal is not popped). `popLeft(2)`: `[2]`. `getMax` 2.

**Code:**
```python
import random
from collections import deque


class MonoQueue:
    def __init__(self):
        self.d = deque()

    def push(self, v):
        while self.d and self.d[-1] < v:            # strictly smaller only: keep equals
            self.d.pop()
        self.d.append(v)

    def popLeft(self, v):
        if self.d and self.d[0] == v:
            self.d.popleft()

    def getMax(self):
        if not self.d:
            raise ValueError("getMax on an empty queue")
        return self.d[0]


class BuggyMonoQueue(MonoQueue):                    # the duplicate bug: pops equals too
    def push(self, v):
        while self.d and self.d[-1] <= v:
            self.d.pop()
        self.d.append(v)


class Brute:
    def __init__(self):
        self.a = []

    def push(self, v):
        self.a.append(v)

    def popLeft(self, v):
        assert self.a[0] == v
        self.a.pop(0)

    def getMax(self):
        return max(self.a)


def window_max(stream, k):
    q, out = MonoQueue(), []
    for i, v in enumerate(stream):
        q.push(v)
        if i >= k - 1:
            out.append(q.getMax())
            q.popLeft(stream[i - k + 1])
    return out


def window_max_brute(stream, k):
    return [max(stream[i:i + k]) for i in range(len(stream) - k + 1)]


q = MonoQueue()
log = []
q.push(3); q.push(1); log.append(q.getMax())
q.push(2); q.popLeft(3); log.append(q.getMax())
q.popLeft(1); log.append(q.getMax())
q.push(5); log.append(q.getMax())
print(log)
assert log == [3, 2, 2, 5]

r = MonoQueue()
r.push(2); r.push(2); r.popLeft(2)
print("duplicates:", r.getMax())
assert r.getMax() == 2

b = BuggyMonoQueue()
b.push(2); b.push(2); b.popLeft(2)
print("buggy (pops equals) after the same steps, items left:", len(b.d), "(getMax would fail)")
assert len(b.d) == 0

try:
    MonoQueue().getMax()
except ValueError as e:
    print("empty:", e)

assert window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
assert window_max([5], 1) == [5]
assert window_max([2, 2, 2, 2], 2) == [2, 2, 2]
assert window_max([4, 3, 2, 1], 4) == [4]

rng = random.Random(23)
ops = 0
for _ in range(400):
    m, ref, live = MonoQueue(), Brute(), []
    for _ in range(40):
        if live and rng.random() < 0.4:
            v = live.pop(0)
            m.popLeft(v)
            ref.popLeft(v)
        else:
            v = rng.randint(0, 4)                   # tiny range: many duplicates
            live.append(v)
            m.push(v)
            ref.push(v)
        if live:
            assert m.getMax() == ref.getMax(), live
        ops += 1
for _ in range(300):
    s = [rng.randint(-5, 5) for _ in range(rng.randint(1, 12))]
    k = rng.randint(1, len(s))
    assert window_max(s, k) == window_max_brute(s, k)
print("random cross-check passed:", ops, "queue ops and 300 window runs")
```

**Output (my run):**
```
[3, 2, 2, 5]
duplicates: 2
buggy (pops equals) after the same steps, items left: 0 (getMax would fail)
empty: getMax on an empty queue
random cross-check passed: 16000 queue ops and 300 window runs
```
The examples in the prompt are correct (the sequence prints `[3, 2, 2, 5]` and the duplicate case gives 2).

**Edge cases:**
- Duplicates: the whole point of `<` versus `<=`.
- `popLeft` for a value that was already dropped: a no-op, not an error.
- `getMax` on empty: raise, or return a sentinel, and say which.
- A strictly decreasing stream: nothing is ever dropped, so space is the window size.

**Follow-ups:**
- *Why does `popLeft` take a value?* The deque holds values, not positions. Storing indices instead lets the caller say "expire everything before index i" and avoids the equality check. That is the form in Part 2 Q16.
- *What if values that leave are not the oldest?* Then this is not a queue. Use a heap with lazy deletion (Part 8).
- *Min as well?* Keep a second deque with the opposite comparison.

**Common mistakes:**
- Popping `<=` and losing duplicates.
- In `popLeft`, removing the front unconditionally.
- Storing only the max of the window, which cannot recover the next max after the max leaves.


### Q24 ⭐⭐ 🟡 Remove duplicate letters (smallest subsequence of distinct letters). Given lowercase `s` (len <= 10^4), return the lexicographically smallest string that contains every distinct letter of `s` exactly once and is a subsequence of `s`. Stack plus two tables (last index of each letter, letters already on the stack): pop a larger top only if that letter occurs again later. Explain why skipping a letter already on the stack is safe. Example: 'bcabc' -> 'abc'; 'cbacdcbc' -> 'acdb'; 'abacb' -> 'abc'; 'a' -> 'a'.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Greedy increasing stack with a "last occurrence" table and an "already on the stack" set.

**Say this first (1 line):** "Scan once; for each letter not already kept, pop bigger letters off the top as long as they appear again later, then push it."

**Brute force:** Try every subsequence, keep the ones that contain each distinct letter exactly once, take the smallest. O(2^n * n). I use it on strings up to length 10.

**Optimal:**
- `last[c]` = last index of `c`. `on_stack` = set of letters currently kept.
- For index `i`, letter `c`: if `c` is already on the stack, skip it. Else while the top is greater than `c` and `last[top] > i` (the top shows up again later), pop it and un-mark it. Then push `c` and mark it.
- Why popping is safe: the popped letter occurs again later, so it can still be placed there, and putting a smaller letter earlier makes the string smaller.
- Why skipping a repeat is safe: the stack is in the best order seen so far. A letter already on it sits at a position at least as good as the new occurrence, since every letter above it was kept because it was no larger or could not be removed. Moving it later would only put a larger letter earlier. If it had been poppable, it would already have been popped when a smaller letter arrived.
- Invariant: the stack is the lexicographically smallest valid arrangement of the letters seen so far, and every letter that does not appear later is on it.

**Complexity:** Each letter is pushed and popped at most once: O(n) time, O(26) extra space (the stack holds each letter at most once).

**Dry run:** `'cbacdcbc'`, last: a2, b6, c7, d4.
- c: push `[c]`. b: top c > b and last[c]=7 > 1, pop; push `[b]`. a: top b > a and last[b]=6 > 2, pop; `[a]`.
- c: push `[a,c]`. d: top c < d, push `[a,c,d]`. c (i=5): already on stack, skip.
- b (i=6): top d > b and last[d]=4 < 6, cannot pop. Push `[a,c,d,b]`. c (i=7): skip. Result `acdb`.

**Code:**
```python
import random
from itertools import combinations


def smallest_brute(s):
    letters = set(s)
    best = None
    n = len(s)
    for r in range(len(letters), len(letters) + 1):
        for idx in combinations(range(n), r):
            cand = "".join(s[i] for i in idx)
            if set(cand) == letters:
                if best is None or cand < best:
                    best = cand
    return best if best is not None else ""


def smallest_stack(s):
    last = {c: i for i, c in enumerate(s)}
    stack, on = [], set()
    for i, c in enumerate(s):
        if c in on:
            continue
        while stack and stack[-1] > c and last[stack[-1]] > i:
            on.discard(stack.pop())
        stack.append(c)
        on.add(c)
    return "".join(stack)


def smallest_no_last_check(s):                       # the bug: always pop bigger tops
    stack, on = [], set()
    for c in s:
        if c in on:
            continue
        while stack and stack[-1] > c:
            on.discard(stack.pop())
        stack.append(c)
        on.add(c)
    return "".join(stack)


examples = [("bcabc", "abc"), ("cbacdcbc", "acdb"), ("abacb", "abc"), ("a", "a")]
for s, want in examples:
    got = smallest_stack(s)
    assert got == smallest_brute(s) == want, (s, got)
    print(repr(s), "->", repr(got))

print("without the last-index check, 'cba' ->", smallest_no_last_check("cba"), "(wrong, c and b are lost)", "| correct:", smallest_stack("cba"))
assert smallest_no_last_check("cba") == "a" and smallest_stack("cba") == "cba"
assert smallest_stack("") == ""
assert smallest_stack("aaaa") == "a"
assert smallest_stack("abcd") == "abcd"
assert smallest_stack("dcba") == "dcba"
assert smallest_stack("ecbacba") == "eacb"
assert len(smallest_stack("zyx" * 1000)) == 3

rng = random.Random(24)
for _ in range(600):
    s = "".join(rng.choice("abcd") for _ in range(rng.randint(1, 10)))
    assert smallest_stack(s) == smallest_brute(s), s
print("random cross-check passed: 600 strings over 'abcd', length up to 10")
```

**Output (my run):**
```
'bcabc' -> 'abc'
'cbacdcbc' -> 'acdb'
'abacb' -> 'abc'
'a' -> 'a'
without the last-index check, 'cba' -> a (wrong, c and b are lost) | correct: cba
random cross-check passed: 600 strings over 'abcd', length up to 10
```
All four examples in the prompt are correct.

**Edge cases:**
- Empty string (not allowed by the prompt, but the code returns `''`).
- One repeated letter: one letter.
- Already sorted: nothing popped. Reverse sorted with each letter once: nothing can be popped either, because nothing appears later.
- A big letter that does not appear again must stay, even if a smaller letter follows (`'cba'` gives `'cba'`, not `'a'`).

**Follow-ups:**
- *Same as "smallest subsequence of distinct characters"?* Yes, same problem under another name.
- *Letters beyond a-z?* Replace the table with a dict; still O(n).
- *Remove k digits (Q20) comparison?* Same pop-bigger-top idea, but the removal budget is a count `k` there; here the budget is "a later copy exists".

**Common mistakes:**
- Forgetting to un-mark a popped letter, so it can never return.
- Not skipping letters already on the stack, which gives duplicates in the answer.
- Popping without the `last[top] > i` test and dropping a letter forever.


### Q25 ⭐⭐ 🟡 Recursion limit versus an explicit stack. `x` is a nested list of integers (for example [1,[4,[6]]]); the depth-weighted sum is the sum of each integer times its nesting depth (outer list is depth 1). Write the recursive version, show that it raises RecursionError on a chain nested 5000 deep because CPython's default limit is 1000 frames (state what `sys.getrecursionlimit()` reports in your run, and why raising it is risky: a deep C-stack crash is possible), then convert it to an explicit stack of (list, depth) frames. State the general recipe for turning recursion into a stack (push the pending work, pop, push children; for post-order work push a marker). Example: [1,[4,[6]]] -> 27; [[1,1],2,[1,1]] -> 10; a chain of 5000 lists around a single 7 -> 35000.
**Asked at:** Python container docs and explainers (docs.python.org collections mirror saying list pop(0) and insert(0, v) cost O(n) and deque gives O(1) at both ends, Real Python deque article, dev.to deque-versus-list timing post; snippets only, not opened; the queue module docs were NOT found, so queue.Queue claims rest on editor knowledge plus the sandbox run) | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Recursion depth is bounded by the interpreter, so convert deep recursion to an explicit stack of pending work.

**Say this first (1 line):** "The recursive version is clean but dies at about 1000 nested frames in CPython; I keep a stack of `(list, depth)` pairs and do the same work in a loop, so depth only costs heap memory."

**Brute force:** The recursive version: for each element, an int adds `value * depth`, a list recurses with `depth + 1`. O(total elements) time, but O(depth) Python frames. On a chain nested 5000 deep it raises `RecursionError`.

**Optimal:**
- Explicit stack: `stack = [(x, 1)]`. Pop `(lst, d)`; for each element, an int adds `e * d`; a list pushes `(e, d + 1)`. The order of visiting does not matter for a sum.
- Observed on Python 3.13: `sys.getrecursionlimit()` is 1000 and the recursive version raised `RecursionError` on the 5000-deep chain (output below).
- Why raising the limit is risky: it only moves the ceiling. Each frame uses memory, and if the limit is above what the machine can hold, the process can crash outright instead of raising a clean error. The classic danger is a C-stack overflow in recursion that passes through C code (for example recursive `repr`, `copy.deepcopy`, or `json`), which can be a hard crash. I observed that with the limit raised to 10000 the same recursive function returned the right answer on this machine; I did not try to force a crash.
- A detail I hit while testing: writing the recursion with `sum(... for ...)` costs two frames per level (the function and the generator), so it hits the limit at half the depth. A plain `for` loop costs one.
- General recipe, recursion to stack: push the initial call's arguments; loop: pop, do the work, push each child call's arguments. For pre-order work that is all. For post-order work (the answer needs the children's results), push a marker entry first, then the children; when the marker pops, all children are already done, so combine their results. Reversing the push order gives left-to-right order if order matters.

**Complexity:** Time O(N) where N is the total number of elements and lists. Space O(depth) for the explicit stack in the worst case (a chain), O(widest pending frontier) otherwise. For the recursive version the space is O(depth) of call frames, which is the limited resource.

**Dry run:** `[1,[4,[6]]]`.
- Stack `[([1,[4,[6]]], 1)]`. Pop it: 1 is an int, add 1*1 = 1. `[4,[6]]` is a list, push it at depth 2.
- Pop `([4,[6]], 2)`: 4*2 = 8, total 9. Push `([6], 3)`.
- Pop `([6], 3)`: 6*3 = 18, total 27. Stack empty. Answer 27.

**Code:**
```python
import random
import sys


def depth_sum_rec(x, depth=1):
    total = 0
    for e in x:                                      # plain loop: one frame per level
        total += e * depth if isinstance(e, int) else depth_sum_rec(e, depth + 1)
    return total


def depth_sum_stack(x):
    total = 0
    stack = [(x, 1)]
    while stack:
        lst, d = stack.pop()
        for e in lst:
            if isinstance(e, int):
                total += e * d
            else:
                stack.append((e, d + 1))
    return total


def chain(depth, value):
    x = [value]
    for _ in range(depth - 1):                       # built in a loop: no recursion needed
        x = [x]
    return x


def random_nested(rng, depth_left):
    out = []
    for _ in range(rng.randint(0, 4)):
        if depth_left > 0 and rng.random() < 0.4:
            out.append(random_nested(rng, depth_left - 1))
        else:
            out.append(rng.randint(-5, 9))
    return out


print("sys.getrecursionlimit() =", sys.getrecursionlimit(), "on Python", sys.version.split()[0])
for x, want in [([1, [4, [6]]], 27), ([[1, 1], 2, [1, 1]], 10)]:
    assert depth_sum_rec(x) == depth_sum_stack(x) == want
    print(x, "->", want)

deep = chain(5000, 7)
try:
    depth_sum_rec(deep)
    print("recursive version: no error (unexpected)")
except RecursionError as e:
    print("recursive version on depth 5000: RecursionError:", e)
print("explicit stack on depth 5000:", depth_sum_stack(deep))
assert depth_sum_stack(deep) == 35000

old = sys.getrecursionlimit()
sys.setrecursionlimit(10000)
try:
    print("recursive with the limit raised to 10000:", depth_sum_rec(deep))
finally:
    sys.setrecursionlimit(old)
print("limit restored to", sys.getrecursionlimit())

assert depth_sum_stack([]) == 0 and depth_sum_stack([[]]) == 0 and depth_sum_stack([[], [[]]]) == 0
assert depth_sum_stack([3]) == 3
assert depth_sum_stack([-1, [-1]]) == -3
assert depth_sum_stack(chain(100000, 1)) == 100000   # far beyond any recursion limit

rng = random.Random(25)
for _ in range(1000):
    x = random_nested(rng, 6)
    assert depth_sum_rec(x) == depth_sum_stack(x), x
print("random cross-check passed: 1000 random nested lists, depth up to 7")
```

**Output (my run):**
```
sys.getrecursionlimit() = 1000 on Python 3.13.17
[1, [4, [6]]] -> 27
[[1, 1], 2, [1, 1]] -> 10
recursive version on depth 5000: RecursionError: maximum recursion depth exceeded
explicit stack on depth 5000: 35000
recursive with the limit raised to 10000: 35000
limit restored to 1000
random cross-check passed: 1000 random nested lists, depth up to 7
```
The three examples in the prompt are correct (the 5000-chain gives 35000).

**Edge cases:**
- Empty list and nested empty lists: 0.
- Negative integers.
- A chain much deeper than any sane limit (100000 here): the explicit stack handles it, the recursive version cannot.
- Wide but shallow input: the stack stays small; only a chain makes it deep.

**Follow-ups:**
- *Why not just raise the limit?* It is a band-aid: memory grows per frame, and deep recursion through C code can crash the process. Use it only for a known bound.
- *Tail-call elimination?* CPython does not do it, so a tail-recursive function still uses a frame per call.
- *Post-order, for example max depth?* Push `(node, False)` then children; when `(node, True)` pops, children's results are ready. The same recipe appears in iterative tree traversals (Part 7).

**Common mistakes:**
- Using `sum(generator)` and wondering why the limit hits at half the depth.
- Setting `sys.setrecursionlimit(10**9)` and trusting it.
- Forgetting that the explicit stack needs the depth stored with each entry.
- Catching `RecursionError` and returning a wrong default.


### Q26 ⭐⭐ 🟡 Asteroid collision. `asteroids` is a list of non-zero integers (len <= 10^4) in a row: the sign is the direction (positive moves right, negative moves left, all at the same speed) and the absolute value is the size. When two meet, the smaller explodes, equal sizes both explode, and asteroids moving the same way never meet. Return the survivors in order. Use a stack: a right-mover is pushed, and a left-mover pops smaller right-movers on top until it is blocked, destroyed or the stack top is not a right-mover. Say why only a (right-mover, then left-mover) adjacency can collide. Example: [5,10,-5] -> [5,10]; [8,-8] -> []; [10,2,-5] -> [10]; [-2,-1,1,2] -> [-2,-1,1,2]; [3,5,-6,2,-1,4] -> [-6,2,4].
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Stack of survivors; a collision can only happen between a right-mover directly followed by a left-mover.

**Say this first (1 line):** "Scan left to right with a stack of survivors. A left-mover fights the right-movers on top of the stack until it dies, they die, or nothing on top moves right."

**Brute force:** Repeatedly find the first adjacent `(positive, negative)` pair, resolve it, and rescan, until no such pair remains. O(n^2) time. The result is the same regardless of which pair is resolved first, and the random check below confirms it against the stack.

**Optimal:**
- For each `a`: if `a > 0`, push. If `a < 0`, loop: while the top is positive and smaller than `|a|`, pop it (it explodes). If the top is positive and equal, pop it and discard `a` (both explode). If the top is positive and larger, discard `a`. If the stack is empty or the top is negative, push `a`.
- Why only a (right-mover, left-mover) adjacency collides: all speeds are equal, so two same-direction asteroids keep their gap, and a left-mover followed by a right-mover move apart. Only a right-mover with a left-mover to its right ever closes the distance.
- Invariant: the stack holds the survivors of the prefix: some left-movers at the bottom, then right-movers on top. A left-mover never rests above a right-mover, because it would have collided with it.

**Complexity:** Each asteroid is pushed at most once and popped at most once: O(n) time, O(n) space.

**Dry run:** `[3,5,-6,2,-1,4]`.
- 3: push. 5: push. `[3,5]`.
- -6: top 5 < 6, pop. Top 3 < 6, pop. Stack empty, push -6. `[-6]`.
- 2: push `[-6,2]`. -1: top 2 > 1, -1 dies. 4: push `[-6,2,4]`.

**Code:**
```python
import random


def collide_brute(a):
    a = list(a)
    while True:
        for i in range(len(a) - 1):
            if a[i] > 0 and a[i + 1] < 0:
                x, y = a[i], a[i + 1]
                if abs(x) > abs(y):
                    del a[i + 1]
                elif abs(x) < abs(y):
                    del a[i]
                else:
                    del a[i:i + 2]
                break
        else:
            return a


def collide(asteroids):
    st = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and st and st[-1] > 0:
            if st[-1] < -a:
                st.pop()                             # the right-mover explodes, keep fighting
            elif st[-1] == -a:
                st.pop()                             # both explode
                alive = False
            else:
                alive = False                        # the left-mover explodes
        if alive:
            st.append(a)
    return st


examples = [([5, 10, -5], [5, 10]), ([8, -8], []), ([10, 2, -5], [10]),
            ([-2, -1, 1, 2], [-2, -1, 1, 2]), ([3, 5, -6, 2, -1, 4], [-6, 2, 4])]
for a, want in examples:
    got = collide(a)
    assert got == collide_brute(a) == want, (a, got)
    print(a, "->", got)

assert collide([]) == []
assert collide([7]) == [7] and collide([-7]) == [-7]
assert collide([1, 1, 1, -1]) == [1, 1]
assert collide([-3, -3]) == [-3, -3]
assert collide([5, 5, -5, -5]) == []
assert collide([1, 2, 3, -10]) == [-10]
assert collide(list(range(1, 10001)) + [-10001]) == [-10001]    # max-size chain of pops

rng = random.Random(26)
bothdie = 0
for _ in range(1500):
    a = [rng.choice([-1, 1]) * rng.randint(1, 5) for _ in range(rng.randint(0, 9))]
    r = collide(a)
    assert r == collide_brute(a), a
    bothdie += len(r) < len(a) and any(a[i] == -a[i + 1] for i in range(len(a) - 1))
print("random cross-check passed: 1500 lists, tie-explosions exercised:", bothdie > 0)
```

**Output (my run):**
```
[5, 10, -5] -> [5, 10]
[8, -8] -> []
[10, 2, -5] -> [10]
[-2, -1, 1, 2] -> [-2, -1, 1, 2]
[3, 5, -6, 2, -1, 4] -> [-6, 2, 4]
random cross-check passed: 1500 lists, tie-explosions exercised: True
```
All five examples in the prompt are correct.

**Edge cases:**
- Equal sizes: both disappear (`[8,-8]`).
- All the same direction: nothing happens.
- Left-movers first, right-movers after: they never meet.
- One huge left-mover: it clears the stack of right-movers, then lands on the bottom.
- Long run of growing right-movers followed by one giant left-mover: n pops, still O(n) total.

**Follow-ups:**
- *Different speeds?* Then it becomes a timing problem (closer to Q21 car fleet): you would sort collisions by time, not use a plain stack.
- *Return indices of survivors?* Push indices and look values up.
- *Why not `while` with a counter instead of `alive`?* It works, but a flag keeps the three outcomes (dies, ties, wins) readable.

**Common mistakes:**
- Treating any adjacent pair as a collision, including `(negative, positive)`.
- Popping on equal size but still pushing the left-mover.
- Forgetting that after popping one right-mover the same left-mover may fight the next one.
- Comparing with the raw sign instead of `abs`.


### Q27 ⭐⭐ 🔴 Longest valid parentheses. `s` contains only '(' and ')' (len <= 3*10^4). Return the length of the longest contiguous substring that is a balanced parentheses string. Give the stack-of-indices solution (seed the stack with -1 as a base marker; on ')' pop, and if empty push the index as the new base, else the run length is i - top), then the O(1)-space two-counter scan in both directions and why it needs both passes. Example: '(()' -> 2; ')()())' -> 4; '' -> 0; '()(())' -> 6; '()(()' -> 2.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports

**Pattern:** Stack of indices with a base marker (the index just before the current valid run), plus a two-counter scan as the O(1)-space variant.

**Say this first (1 line):** "Keep a stack of indices seeded with -1. A '(' pushes its index; a ')' pops, and if the stack is then empty this ')' becomes the new base, otherwise the run length is `i - stack[-1]`."

**Brute force:** For every start, extend to the right while tracking the balance: it must never go below 0, and each time it hits 0 the substring is balanced. O(n^2) time, O(1) space. (The textbook O(n^3) check of every substring is the same idea, slower.)

**Optimal:**
- Version 1, the stack of indices.
- `stack = [-1]`. For index `i`: `'('` push `i`. `')'`: pop. If the stack is empty, push `i` (an unmatched ')' is a wall: the new base). Else `best = max(best, i - stack[-1])`.
- Why `i - stack[-1]`: after the pop, the top is the index just before the current balanced run, either an unmatched '(' still waiting, or the base marker.
- Invariant: the stack holds the index of the last unmatched ')' (or -1) at the bottom, followed by the indices of unmatched '('. Everything between consecutive stack entries is balanced.

- Version 2, two counters, O(1) space.
- Left to right, count `left` and `right`. If equal, a balanced run of length `2*right` ends here. If `right > left`, reset both to 0.
- Right to left with the roles swapped: reset when `left > right`.
- Why both passes: in `'(()'` the left-to-right scan ends with `left=2, right=1`, never equal and never reset, so it reports 0 and misses the balanced `'()'` at the end. The right-to-left pass sees it. A surplus of '(' is only visible from the right, a surplus of ')' only from the left.

**Complexity:** Both are O(n) time. The stack version is O(n) space; the counter version is O(1).

**Dry run:** `')()())'`, indices 0 to 5.
- Stack `[-1]`. i=0 ')': pop gives empty, push 0. `[0]`.
- i=1 '(': `[0,1]`. i=2 ')': pop, top 0, length 2-0 = 2.
- i=3 '(': `[0,3]`. i=4 ')': pop, top 0, length 4. Best 4.
- i=5 ')': pop gives empty, push 5. Answer 4.

**Code:**
```python
from itertools import product


def lvp_brute(s):
    best = 0
    for i in range(len(s)):
        bal = 0
        for j in range(i, len(s)):
            bal += 1 if s[j] == "(" else -1
            if bal < 0:
                break
            if bal == 0:
                best = max(best, j - i + 1)
    return best


def lvp_stack(s):
    stack = [-1]
    best = 0
    for i, c in enumerate(s):
        if c == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return best


def lvp_two_pass(s):
    best = left = right = 0
    for c in s:
        if c == "(":
            left += 1
        else:
            right += 1
        if left == right:
            best = max(best, 2 * right)
        elif right > left:
            left = right = 0
    left = right = 0
    for c in reversed(s):
        if c == "(":
            left += 1
        else:
            right += 1
        if left == right:
            best = max(best, 2 * left)
        elif left > right:
            left = right = 0
    return best


def lvp_one_pass_only(s):                            # the bug: left-to-right pass alone
    best = left = right = 0
    for c in s:
        if c == "(":
            left += 1
        else:
            right += 1
        if left == right:
            best = max(best, 2 * right)
        elif right > left:
            left = right = 0
    return best


examples = [("(()", 2), (")()())", 4), ("", 0), ("()(())", 6), ("()(()", 2)]
for s, want in examples:
    got = lvp_stack(s)
    assert got == lvp_two_pass(s) == lvp_brute(s) == want, (s, got)
    print(repr(s), "->", got)

print("left-to-right only on '(()' ->", lvp_one_pass_only("(()"), "(wrong); correct:", lvp_two_pass("(()"))
assert lvp_one_pass_only("(()") == 0 and lvp_two_pass("(()") == 2
assert lvp_stack("((((") == 0 and lvp_stack("))))") == 0
assert lvp_stack("()" * 15000) == 30000 and lvp_two_pass("()" * 15000) == 30000
assert lvp_stack("(" * 15000 + ")" * 15000) == 30000
assert lvp_stack("(" * 15000 + ")" * 14999) == 29998

total = 0
for n in range(0, 13):                               # every string up to length 12
    for t in product("()", repeat=n):
        s = "".join(t)
        want = lvp_brute(s)
        assert lvp_stack(s) == want and lvp_two_pass(s) == want, s
        total += 1
print("exhaustive check passed:", total, "strings of length 0 to 12")
```

**Output (my run):**
```
'(()' -> 2
')()())' -> 4
'' -> 0
'()(())' -> 6
'()(()' -> 2
left-to-right only on '(()' -> 0 (wrong); correct: 2
exhaustive check passed: 8191 strings of length 0 to 12
```
All five examples in the prompt are correct.

**Edge cases:**
- Empty string: 0.
- All '(' or all ')': 0.
- The best run in the middle, between two unmatched ')': the base marker moves right and handles it.
- Two adjacent balanced runs such as `'()()'` join into one run (length 4): that is why we subtract the base, not the last push.
- Maximum size: the stack version holds up to n indices.

**Follow-ups:**
- *Why seed with -1?* So that a run starting at index 0 has a base to subtract: length is `i - (-1)`.
- *Why is the two-pass scan correct?* Any maximal balanced run is either found when counts are equal in the left scan (no excess ')' broke it), or has an excess of '(' to its right that only the reverse scan can reset past.
- *DP version?* `dp[i]` = longest valid ending at i; O(n) time and space, correct but harder to explain aloud.

**Common mistakes:**
- Using only the left-to-right counter pass.
- Not pushing the index after an unmatched ')' (the base never moves).
- Returning the last run length instead of the max.
- Computing `i - top` before popping.


### Q28 ⭐⭐ 🔴 Maximal rectangle in a binary matrix. `matrix` is a list of equal-length strings of '0' and '1' (up to 200 x 200). Return the area of the largest rectangle consisting only of '1' cells. For each row build the histogram of consecutive 1s ending at that row (reset to 0 on a '0'), then run the largest-rectangle-in-histogram stack on it, giving O(rows * cols); say why this reduction is correct. Example: ['10100','10111','11111','10010'] -> 6; ['0'] -> 0; ['1'] -> 1; ['11','11'] -> 4.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Reduce to largest rectangle in a histogram (monotonic stack), once per row.

**Say this first (1 line):** "Turn each row into a histogram of consecutive 1s ending at that row, and run the largest-rectangle-in-histogram stack on it. Take the best over all rows."

**Brute force:** Try every rectangle (top-left, bottom-right) and check with a 2D prefix sum whether it is all ones. O(rows^2 * cols^2) time. It is my checker.

**Optimal:**
- `heights[j]` = number of consecutive '1' cells in column `j` ending at the current row. A '0' resets it to 0, else add 1.
- For each row, run the histogram stack: keep indices with increasing heights. When a bar `h` arrives and the top is taller, pop the top: its height is the rectangle height, its width runs from the new top + 1 to the current index - 1. A sentinel bar of height 0 at the end flushes the stack.
- Why the reduction is correct: any all-ones rectangle has a bottom row `r`. In that row, its width-w, height-h shape sits under a histogram of consecutive 1s whose bars over those columns are all at least `h`. So it is a rectangle in the histogram of row `r`. Conversely every histogram rectangle is all ones. Taking the max over all rows covers every bottom row.
- Invariant (histogram): the stack heights are strictly increasing, and when a bar is popped, everything between its neighbours on the stack is at least as tall, so the rectangle is maximal.

**Complexity:** Each row costs O(cols) for the heights update and O(cols) for the stack pass (each index is pushed and popped once). Total O(rows * cols) time, O(cols) space.

**Dry run:** `['10100','10111','11111','10010']`. Heights after row 0: `[1,0,1,0,0]`; row 1: `[2,0,2,1,1]`; row 2: `[3,1,3,2,2]`; row 3: `[4,0,0,3,0]`. Row 2 holds the answer. Histogram `[3,1,3,2,2]` plus a sentinel 0:
- i=0: push. i=1 (h 1): pop 3, width 1, area 3. Push. `[1]`.
- i=2 (h 3): push `[1,2]`. i=3 (h 2): pop h3, width 3-1-1 = 1, area 3. Push `[1,3]`.
- i=4 (h 2): top is 2, which is `>=` 2, pop, width 4-1-1 = 2, area 4. Push `[1,4]`.
- i=5 (sentinel 0): pop h2 at index 4, width 5-1-1 = 3, area 6. Pop h1, width 5, area 5.
- Best 6: height 2 across columns 2 to 4. The other rows give less, so the answer is 6.

**Code:**
```python
import random
from itertools import product


def max_rect_brute(matrix):
    r = len(matrix)
    if r == 0:
        return 0
    c = len(matrix[0])
    pre = [[0] * (c + 1) for _ in range(r + 1)]
    for i in range(r):
        for j in range(c):
            pre[i + 1][j + 1] = pre[i][j + 1] + pre[i + 1][j] - pre[i][j] + (matrix[i][j] == "1")
    best = 0
    for i1 in range(r):
        for i2 in range(i1, r):
            for j1 in range(c):
                for j2 in range(j1, c):
                    area = (i2 - i1 + 1) * (j2 - j1 + 1)
                    ones = pre[i2 + 1][j2 + 1] - pre[i1][j2 + 1] - pre[i2 + 1][j1] + pre[i1][j1]
                    if ones == area:
                        best = max(best, area)
    return best


def largest_in_histogram(h):
    stack = []                                       # indices, heights strictly increasing
    best = 0
    for i in range(len(h) + 1):
        cur = h[i] if i < len(h) else 0              # sentinel flushes the stack
        while stack and h[stack[-1]] >= cur:
            height = h[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best


def max_rect(matrix):
    if not matrix:
        return 0
    heights = [0] * len(matrix[0])
    best = 0
    for row in matrix:
        for j, ch in enumerate(row):
            heights[j] = heights[j] + 1 if ch == "1" else 0
        best = max(best, largest_in_histogram(heights))
    return best


examples = [(["10100", "10111", "11111", "10010"], 6), (["0"], 0), (["1"], 1), (["11", "11"], 4)]
for m, want in examples:
    got = max_rect(m)
    assert got == max_rect_brute(m) == want, (m, got)
    print(m, "->", got)

assert max_rect([]) == 0
assert max_rect(["1" * 200] * 200) == 40000
assert max_rect(["0" * 200] * 200) == 0
assert max_rect(["10" * 100] * 200) == 200
assert max_rect(["1111", "0000", "1111"]) == 4
assert largest_in_histogram([2, 1, 5, 6, 2, 3]) == 10

total = 0
for t in product("01", repeat=12):                   # every 3 x 4 matrix
    m = ["".join(t[0:4]), "".join(t[4:8]), "".join(t[8:12])]
    assert max_rect(m) == max_rect_brute(m), m
    total += 1
rng = random.Random(28)
for _ in range(500):
    r, c = rng.randint(1, 6), rng.randint(1, 6)
    m = ["".join(rng.choice("0111") for _ in range(c)) for _ in range(r)]
    assert max_rect(m) == max_rect_brute(m), m
    total += 1
print("cross-check passed:", total, "matrices (all 4096 of size 3x4, plus 500 random up to 6x6)")
```

**Output (my run):**
```
['10100', '10111', '11111', '10010'] -> 6
['0'] -> 0
['1'] -> 1
['11', '11'] -> 4
cross-check passed: 4596 matrices (all 4096 of size 3x4, plus 500 random up to 6x6)
```
All four examples in the prompt are correct.

**Edge cases:**
- No rows or no columns: 0.
- All zeros: 0. All ones: rows * cols.
- A '0' in the middle of a column resets the height, so rectangles never span it.
- A single row or single column: the histogram handles it as a plain run of ones.
- Matrix given as strings: compare with `'1'`, not the integer 1.

**Follow-ups:**
- *Why pop on `>=` here?* Equal heights give the same rectangle area from the later bar, so popping early is safe and keeps the stack strictly increasing.
- *Largest square instead?* A DP on the cell above-left, O(rows * cols); different pattern (Part 10).
- *Can you update the heights without rebuilding?* Yes, that is exactly the one-array update; do not store a full heights matrix.

**Common mistakes:**
- Forgetting the sentinel, so bars still on the stack are never counted.
- Not resetting the height to 0 on a '0' (adds up non-consecutive ones).
- Width computed as `i - top` instead of `i - top - 1` after the pop.
- Treating the characters as ints and adding `'1'` strings.


### Q29 ⭐⭐ 🔴 Sum of subarray minimums. `arr` has positive integers (len <= 3*10^4); return the sum of min(b) over all contiguous subarrays b, modulo 10^9+7. For each element count the subarrays in which it is the minimum as (distance to previous smaller) times (distance to next smaller-or-equal) using one monotonic stack pass, with the asymmetric tie rule so equal minimums are counted once; give the O(n^2) brute force. Example: [3,1,2,4] -> 17; [11,81,94,43,3] -> 444; [2,2,2] -> 12.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Contribution technique with a monotonic stack: count the subarrays in which each element is the minimum.

**Say this first (1 line):** "Instead of enumerating subarrays, ask for each element how many subarrays have it as the minimum: (distance to the previous smaller) times (distance to the next smaller-or-equal), times its value."

**Brute force:** For each start, extend the end and keep a running minimum; add it every step. O(n^2) time, O(1) space, then take the sum modulo 1e9+7. It is my checker.

**Optimal:**
- For element `j`, let `L` be the index of the previous strictly smaller element (or -1) and `R` the index of the next smaller-or-equal element (or n). A subarray `[a, b]` with `L < a <= j <= b < R` has `arr[j]` as its minimum. Count: `(j - L) * (R - j)`. Contribution: `arr[j] * (j - L) * (R - j)`.
- Tie rule: one side strict, the other not. With equal values, every subarray must be owned by exactly one element. Here the right side stops at an equal element, so no equal copy to the right of `j` is inside its range; copies to the left can be. So `j` owns exactly the subarrays whose rightmost minimum is `j`. If both sides were strict, a subarray with k equal minimums would be counted k times. If both were non-strict, some would be counted by nobody.
- One pass: keep a stack of indices with strictly increasing values. When index `i` arrives and the top has value `>= arr[i]`, pop `j`: then `R = i` (next smaller-or-equal is `i`) and `L` is the new top (previous strictly smaller) or -1. Add `arr[j] * (j - L) * (i - j)`. Use a sentinel `i = n` that pops everything.
- Python note: integers do not overflow, so the modulus is only there because the problem asks for it; take it once at the end or at each add.

**Complexity:** Every index is pushed once and popped once: O(n) time, O(n) space.

**Dry run:** `[2,2,2]`, expected 12 (six subarrays, each with minimum 2).
- i=0: push `[0]`. i=1: top value 2 >= 2, pop j=0: L=-1, R=1, count (0-(-1))*(1-0) = 1, adds 2. Push `[1]`.
- i=2: pop j=1: L=-1, R=2, count 2*1 = 2, adds 4. Push `[2]`.
- Sentinel i=3: pop j=2: L=-1, R=3, count 3*1 = 3, adds 6. Total 12.
- Each element owns the subarrays where it is the rightmost minimum. For example `[0,1]` is counted by j=1 (its L is -1, so starts 0 and 1 are both allowed), not by j=0. All six subarrays are counted once.

**Code:**
```python
import random

MOD = 10**9 + 7


def sum_min_brute(arr):
    total = 0
    for i in range(len(arr)):
        cur = arr[i]
        for j in range(i, len(arr)):
            cur = min(cur, arr[j])
            total += cur
    return total % MOD


def sum_min(arr):
    n = len(arr)
    stack = []                                       # indices, values strictly increasing
    total = 0
    for i in range(n + 1):
        cur = arr[i] if i < n else 0                 # sentinel below every positive value
        while stack and arr[stack[-1]] >= cur:
            j = stack.pop()
            left = stack[-1] if stack else -1        # previous strictly smaller
            total += arr[j] * (j - left) * (i - j)   # i = next smaller-or-equal
        stack.append(i)
    return total % MOD


def sum_min_both_strict(arr):                        # the bug: previous-smaller AND next-smaller, both strict
    n = len(arr)
    total = 0
    for j in range(n):
        L = j - 1
        while L >= 0 and arr[L] >= arr[j]:
            L -= 1
        R = j + 1
        while R < n and arr[R] >= arr[j]:
            R += 1
        total += arr[j] * (j - L) * (R - j)
    return total % MOD


examples = [([3, 1, 2, 4], 17), ([11, 81, 94, 43, 3], 444), ([2, 2, 2], 12)]
for a, want in examples:
    got = sum_min(a)
    assert got == sum_min_brute(a) == want, (a, got)
    print(a, "->", got)

print("tie rule broken (both sides strict) on [2,2,2] ->", sum_min_both_strict([2, 2, 2]), "(over-counts; correct is 12)")
assert sum_min_both_strict([2, 2, 2]) == 20 and sum_min([2, 2, 2]) == 12

assert sum_min([7]) == 7
assert sum_min([1, 2, 3, 4]) == sum_min_brute([1, 2, 3, 4]) == 20
assert sum_min([4, 3, 2, 1]) == sum_min_brute([4, 3, 2, 1]) == 20
assert sum_min([5] * 100) == 5 * (100 * 101 // 2) % MOD
big = [10**9] * 50                                  # forces the modulus to matter
assert sum_min(big) == sum_min_brute(big)
assert sum_min(big) != 10**9 * (50 * 51 // 2)

rng = random.Random(29)
for _ in range(600):
    a = [rng.randint(1, 5) for _ in range(rng.randint(1, 14))]
    assert sum_min(a) == sum_min_brute(a), a
for _ in range(60):
    a = [rng.randint(1, 10**9) for _ in range(rng.randint(1, 200))]
    assert sum_min(a) == sum_min_brute(a)
n_max = [rng.randint(1, 30000) for _ in range(30000)]
r = sum_min(n_max)
assert 0 <= r < MOD
print("random cross-check passed: 600 small (many ties), 60 large-valued, one n=30000 run ->", r)
```

**Output (my run):**
```
[3, 1, 2, 4] -> 17
[11, 81, 94, 43, 3] -> 444
[2, 2, 2] -> 12
tie rule broken (both sides strict) on [2,2,2] -> 20 (over-counts; correct is 12)
random cross-check passed: 600 small (many ties), 60 large-valued, one n=30000 run -> 517611528
```
All three examples in the prompt are correct.

**Edge cases:**
- One element.
- All equal: the tie rule decides everything (6 subarrays for 3 equal elements, total 12 for value 2).
- Strictly increasing or decreasing: the stack grows to n or empties each step.
- Big values: Python has no overflow, but reduce modulo 1e9+7 as the problem requires.
- n = 30000: O(n) is instant; the O(n^2) brute force is 4.5e8 steps and would be too slow.

**Follow-ups:**
- *Sum of subarray maximums?* Mirror the comparisons; sum of (max - min) over all subarrays is the difference of the two.
- *Why is the answer not just the sum of elements times something?* The count of subarrays where an element is the minimum depends on its nearest smaller neighbours on each side.
- *Could you swap which side is strict?* Yes, as long as exactly one side is strict.

**Common mistakes:**
- Making both sides strict or both non-strict, which double-counts or loses subarrays with equal minimums.
- Multiplying `(j - L)` by `(R - L)` instead of `(R - j)`.
- Forgetting the sentinel pass for elements still on the stack.
- Taking the modulus of only part of the product (fine in Python, but skipping it at the end is wrong).


### Q30 ⭐ 🟢 The BFS level-order queue idiom, at concept level. Graph algorithms belong to Part 9, so do not solve a graph problem here; instead show the queue idiom on a hand-built adjacency dict: use `collections.deque`, mark nodes visited when they are enqueued (not when dequeued), and snapshot `len(queue)` at the start of each round to separate levels. Return the nodes grouped by level and the hop distance of each node from the source, and say why a list with `pop(0)` would be wrong for large inputs. Example: graph {'A':['B','C'],'B':['D'],'C':['D','E'],'D':['F'],'E':['F'],'F':[]} from 'A' -> levels [['A'],['B','C'],['D','E'],['F']] and distance of 'F' = 3.
**Asked at:** Python container docs and explainers (docs.python.org collections mirror saying list pop(0) and insert(0, v) cost O(n) and deque gives O(1) at both ends, Real Python deque article, dev.to deque-versus-list timing post; snippets only, not opened; the queue module docs were NOT found, so queue.Queue claims rest on editor knowledge plus the sandbox run) | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Queue-driven level-order traversal (BFS idiom). The graph is only a prop; Part 9 owns graph algorithms.

**Say this first (1 line):** "Use a `deque`, mark a node visited when I enqueue it, and at the start of each round take `len(queue)` so I know how many nodes belong to this level."

**Brute force:** The same loop with a `list` and `pop(0)`. It gives the right answer but each `pop(0)` shifts the whole list, so draining n items costs O(n^2) element moves. A second plain reference below computes levels by repeatedly expanding a set of frontier nodes.

**Optimal:**
- `queue = deque([source])`, `seen = {source}`, `dist = {source: 0}`.
- While the queue is not empty: `size = len(queue)` (the snapshot), then pop exactly `size` nodes. Those are one level. For each neighbour not in `seen`: add to `seen`, set its distance to the level number + 1, append to the queue.
- Why mark on enqueue: a node reachable by two parents (D from B and from C) would otherwise be queued twice and expanded twice. Marking on dequeue is the classic bug; on a larger graph it can multiply the work badly. The code counts how often D is enqueued under each rule.
- Why the snapshot works: nodes appended during the round are for the next level, and the snapshot fixes how many to pop now.
- Why `list.pop(0)` is wrong for large inputs: removing the first item shifts all the others, O(n) per call. `deque.popleft()` is O(1). I measured both on this machine (sandbox-only, shows the trend, not a proof; the big-O reason is the shifting).
- Invariant: the queue holds nodes at distance d and then d+1, in that order, so nodes are dequeued in non-decreasing distance: first arrival is the shortest hop count.

**Complexity:** O(V + E) time (each node enqueued once, each edge looked at once) and O(V) space for `seen`, the queue and the distances.

**Dry run:** graph `A:[B,C], B:[D], C:[D,E], D:[F], E:[F], F:[]`, source A.
- Level 0: queue `[A]`. Pop A: B and C are new, enqueue. Level `[A]`.
- Level 1: queue `[B,C]`, size 2. Pop B: D new, enqueue. Pop C: D already seen (this is the mark-on-enqueue payoff), E new, enqueue. Level `[B,C]`.
- Level 2: `[D,E]`. D adds F. E sees F already seen. Level `[D,E]`.
- Level 3: `[F]`. Distances: A 0, B 1, C 1, D 2, E 2, F 3.

**Code:**
```python
import random
import time
from collections import deque


def bfs_levels(graph, source):
    queue = deque([source])
    seen = {source}
    levels, dist = [], {source: 0}
    while queue:
        size = len(queue)                            # snapshot: this round is one level
        level = []
        for _ in range(size):
            node = queue.popleft()
            level.append(node)
            for nxt in graph.get(node, []):
                if nxt not in seen:                  # mark on ENQUEUE
                    seen.add(nxt)
                    dist[nxt] = dist[node] + 1
                    queue.append(nxt)
        levels.append(level)
    return levels, dist


def bfs_list_pop0(graph, source):                    # same logic, list.pop(0): correct but O(n) pops
    queue = [source]
    seen = {source}
    dist = {source: 0}
    while queue:
        node = queue.pop(0)
        for nxt in graph.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return dist


def enqueues_mark_on_dequeue(graph, source):         # the bug: counts how many times nodes are queued
    queue = deque([source])
    seen = set()
    count = 0
    while queue:
        node = queue.popleft()
        if node in seen:
            continue
        seen.add(node)
        for nxt in graph.get(node, []):
            queue.append(nxt)
            count += 1
    return count + 1


def dist_reference(graph, source):                   # brute: expand a frontier set round by round
    dist = {source: 0}
    frontier = {source}
    d = 0
    while frontier:
        d += 1
        nxt = set()
        for u in frontier:
            for v in graph.get(u, []):
                if v not in dist:
                    nxt.add(v)
        for v in nxt:
            dist[v] = d
        frontier = nxt
    return dist


G = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["F"], "E": ["F"], "F": []}
levels, dist = bfs_levels(G, "A")
print("levels:", levels)
print("distances:", dist)
assert levels == [["A"], ["B", "C"], ["D", "E"], ["F"]]
assert dist["F"] == 3
assert bfs_list_pop0(G, "A") == dist == dist_reference(G, "A")

print("enqueues, mark on enqueue:", len(dist), "| mark on dequeue:", enqueues_mark_on_dequeue(G, "A"))
assert enqueues_mark_on_dequeue(G, "A") > len(dist)

assert bfs_levels({"X": []}, "X") == ([["X"]], {"X": 0})                    # lone node
assert bfs_levels({"A": ["A", "B"], "B": ["A"]}, "A")[0] == [["A"], ["B"]]  # self-loop and cycle
assert bfs_levels({"A": ["B"]}, "A")[0] == [["A"], ["B"]]                   # B missing from the dict
assert bfs_levels({"A": [], "Z": ["A"]}, "A")[1] == {"A": 0}                # Z unreachable

rng = random.Random(30)
for _ in range(500):
    n = rng.randint(1, 9)
    g = {i: [rng.randrange(n) for _ in range(rng.randint(0, 3))] for i in range(n)}
    src = rng.randrange(n)
    lv, d = bfs_levels(g, src)
    assert d == dist_reference(g, src) == bfs_list_pop0(g, src)
    assert [d[x] for lvl in lv for x in lvl] == sorted(d.values())          # levels in distance order
    assert all(d[x] == i for i, lvl in enumerate(lv) for x in lvl)
print("random cross-check passed: 500 random directed graphs (cycles, self-loops, duplicates)")

N = 100_000
t0 = time.perf_counter()
dq = deque(range(N))
while dq:
    dq.popleft()
t_deque = time.perf_counter() - t0
t0 = time.perf_counter()
ls = list(range(N))
while ls:
    ls.pop(0)
t_list = time.perf_counter() - t0
print(f"draining {N} items, sandbox timing (Python 3.13, one run): deque {t_deque:.3f}s, list.pop(0) {t_list:.3f}s")
assert t_list > t_deque
```

**Output (my run):**
```
levels: [['A'], ['B', 'C'], ['D', 'E'], ['F']]
distances: {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 3}
enqueues, mark on enqueue: 6 | mark on dequeue: 8
random cross-check passed: 500 random directed graphs (cycles, self-loops, duplicates)
draining 100000 items, sandbox timing (Python 3.13, one run): deque 0.006s, list.pop(0) 0.733s
```
The example in the prompt is correct (levels as given, distance of F is 3). The timing line varies from run to run; only the gap matters, and it is sandbox-only.

**Edge cases:**
- Source with no neighbours: one level, one node.
- Cycles and self-loops: `seen` stops infinite loops.
- A neighbour missing from the dict: `graph.get(node, [])` treats it as a leaf.
- Unreachable nodes never appear in the output.
- Disconnected graphs: BFS from one source covers only its component.

**Follow-ups:**
- *Do you need the level snapshot if you only want distances?* No: store the distance when enqueuing, as the code does. The snapshot is only needed to group nodes into levels.
- *Edge weights?* BFS is only right when every edge costs one hop. With weights, use Dijkstra with a heap (Part 9).
- *Python alternative to `popleft`?* Two lists (current level and next level) swapped each round also avoid `pop(0)`.

**Common mistakes:**
- Marking visited on dequeue, which enqueues the same node many times.
- Using `queue.pop(0)` on a list.
- Using `len(queue)` inside the loop condition of the level loop instead of taking the snapshot first, so the level grows while it is being processed.
- Forgetting to mark the source as seen.

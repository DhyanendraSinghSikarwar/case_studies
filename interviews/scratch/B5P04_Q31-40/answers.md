### Q31 ⭐ 🟡 queue.Queue versus collections.deque, and thread-safety. Compare them for a producer-consumer pipeline: `queue.Queue` is built for threads (internal lock, blocking `get` and `put`, optional `maxsize`, `task_done` and `join`), while `deque` has atomic single `append` and `popleft` in CPython (an implementation detail, not a blocking API) and silently drops from the opposite end when `maxlen` is set. State when each is right and why a check-then-act on a deque (`if d: d.popleft()`) is still a race across threads. Also name `asyncio.Queue` as the coroutine version. Example: `q = queue.Queue(maxsize=2)`; put(1), put(2); put_nowait(3) -> raises queue.Full; get() -> 1; `d = deque(maxlen=2)`; append 1, 2, 3 -> deque([2, 3]).
**Asked at:** Python container docs and explainers (docs.python.org collections mirror saying list pop(0) and insert(0, v) cost O(n) and deque gives O(1) at both ends, Real Python deque article, dev.to deque-versus-list timing post; snippets only, not opened; the queue module docs were NOT found, so queue.Queue claims rest on editor knowledge plus the sandbox run) | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Choosing the right queue for the job: a thread-safe blocking channel (`queue.Queue`), a fast single-thread buffer (`collections.deque`), or a coroutine channel (`asyncio.Queue`). This is a container-semantics question, not an algorithm.

**Say this first (1 line):** "For threads that must wait for each other I use `queue.Queue`, because it has a lock, blocking `get` and `put`, a size bound and `task_done`/`join`. A `deque` is a fast buffer with atomic single operations in CPython, but `if d: d.popleft()` is still a race, and `maxlen` silently drops the old end."

**Brute force:** A plain `list` guarded by your own `threading.Lock` and `Condition`. It works, but you rewrite what `Queue` already ships, and `list.pop(0)` is O(n). That is the thing `Queue` (backed by a `deque` inside) replaces.

**Optimal:** Match the tool to the situation.
| Need | Use | Why |
|---|---|---|
| Threads hand work to each other, consumers should sleep when empty | `queue.Queue` | internal lock plus condition variables; `get` blocks, `put` blocks when `maxsize` is reached (back-pressure) |
| Wait for all work to finish | `Queue.task_done()` and `Queue.join()` | `join` returns when every `put` has a matching `task_done` |
| Single thread, BFS, sliding window, undo history | `deque` | O(1) at both ends, no lock cost |
| Keep only the last k items | `deque(maxlen=k)` | a full append drops the item at the opposite end, silently |
| Many coroutines in one event loop | `asyncio.Queue` | `await put/get` suspends the coroutine, not the thread; not thread-safe |
- Facts I rely on: `deque.append` and `deque.popleft` are each atomic in CPython. That is an implementation detail of the GIL build, not a documented blocking API, so I do not design around it.
- Invariant for check-then-act: a safe sequence is one atomic call. `if d: d.popleft()` is two steps. Another thread can empty the deque between them. Write `try: d.popleft() except IndexError` instead.
- The code forces that race deterministically with a `Barrier` so the output does not depend on luck.

**Complexity:** `Queue.put` and `Queue.get` are O(1) amortised plus lock cost and any waiting time (waiting is not CPU work). `deque.append/popleft` are O(1). Space O(number of items held), bounded by `maxsize` or `maxlen` when set. The `Queue` wrapper adds a constant-factor cost per operation from locking, which is the price of safe blocking.

**Dry run:** the prompt's example.
| step | `Queue(maxsize=2)` | note |
|---|---|---|
| put(1) | [1] | |
| put(2) | [1, 2] | now full |
| put_nowait(3) | [1, 2] | raises `queue.Full` (a blocking `put(3)` would wait instead) |
| get() | [2] | returns 1 (FIFO) |

`deque(maxlen=2)`: append 1 gives [1]; append 2 gives [1, 2]; append 3 pushes 1 out, so `deque([2, 3], maxlen=2)`.

**Code:**
```python
import asyncio
import queue
import random
import sys
import threading
from collections import Counter, deque

# --- 1. The prompt's example -------------------------------------------------
q = queue.Queue(maxsize=2)
q.put(1)
q.put(2)
try:
    q.put_nowait(3)
except queue.Full:
    print("put_nowait(3) -> queue.Full")
assert q.get() == 1
print("get() ->", 1, "| full:", q.full(), "| qsize:", q.qsize())

d = deque(maxlen=2)
for v in (1, 2, 3):
    d.append(v)
print("deque(maxlen=2) after 1,2,3 ->", d)
assert list(d) == [2, 3]          # 1 was dropped silently from the opposite end

# --- 2. Blocking behaviour: Queue waits (with a timeout), deque raises -------
try:
    queue.Queue().get(timeout=0.05)
except queue.Empty:
    print("Queue().get(timeout=0.05) on empty -> queue.Empty after waiting")
try:
    deque().popleft()
except IndexError as e:
    print("deque().popleft() on empty -> IndexError immediately:", e)

# --- 3. Producer-consumer with Queue: seeded cross-check ---------------------
def run_pipeline(rng):
    n_prod, n_cons = rng.randint(1, 3), rng.randint(1, 3)
    per = [[rng.randint(0, 9) for _ in range(rng.randint(0, 6))] for _ in range(n_prod)]
    qq = queue.Queue(maxsize=rng.randint(1, 3))
    got, lock = [], threading.Lock()
    STOP = object()

    def producer(items):
        for x in items:
            qq.put(x)                 # blocks when full: natural back-pressure

    def consumer():
        while True:
            x = qq.get()              # blocks when empty
            if x is STOP:
                qq.task_done()
                return
            with lock:
                got.append(x)
            qq.task_done()

    cons = [threading.Thread(target=consumer) for _ in range(n_cons)]
    prods = [threading.Thread(target=producer, args=(p,)) for p in per]
    for t in cons + prods:
        t.start()
    for t in prods:
        t.join()
    for _ in cons:
        qq.put(STOP)                  # one stop marker per consumer
    qq.join()                         # returns when every task_done() has matched a put()
    for t in cons:
        t.join()
    sent = Counter(x for p in per for x in p)
    return Counter(got) == sent

rng = random.Random(31)
assert all(run_pipeline(rng) for _ in range(150))
print("150 seeded Queue pipelines: every item delivered exactly once")

# --- 4. Check-then-act on a deque is a race (forced deterministically) -------
dq = deque([1])
barrier = threading.Barrier(2)
outcome = []

def risky():
    if dq:                            # both threads see a non-empty deque...
        barrier.wait()                # ...before either one pops
        try:
            outcome.append(dq.popleft())
        except IndexError:
            outcome.append("IndexError")

ts = [threading.Thread(target=risky) for _ in range(2)]
for t in ts:
    t.start()
for t in ts:
    t.join()
print("two threads, if-d-then-popleft ->", sorted(map(str, outcome)))
assert sorted(map(str, outcome)) == ["1", "IndexError"]

def safe_pop(dd):
    try:
        return dd.popleft()           # one atomic call, handle failure
    except IndexError:
        return None

assert safe_pop(deque([5])) == 5 and safe_pop(deque()) is None

# --- 5. asyncio.Queue is the coroutine version -------------------------------
async def main():
    aq = asyncio.Queue(maxsize=2)
    out = []

    async def prod():
        for i in range(5):
            await aq.put(i)           # suspends the coroutine, not the thread
        await aq.put(None)

    async def cons():
        while (x := await aq.get()) is not None:
            out.append(x)

    await asyncio.gather(prod(), cons())
    return out

res = asyncio.run(main())
assert res == [0, 1, 2, 3, 4]
print("asyncio.Queue pipeline ->", res)

# --- 6. Version facts as observed --------------------------------------------
print("Python", sys.version.split()[0], "| Queue has shutdown():", hasattr(queue.Queue, "shutdown"))
```

**Output (my run):**
```text
put_nowait(3) -> queue.Full
get() -> 1 | full: False | qsize: 1
deque(maxlen=2) after 1,2,3 -> deque([2, 3], maxlen=2)
Queue().get(timeout=0.05) on empty -> queue.Empty after waiting
deque().popleft() on empty -> IndexError immediately: pop from an empty deque
150 seeded Queue pipelines: every item delivered exactly once
two threads, if-d-then-popleft -> ['1', 'IndexError']
asyncio.Queue pipeline -> [0, 1, 2, 3, 4]
Python 3.13.17 | Queue has shutdown(): True
```

Observed on Python 3.13.17 in this sandbox: the `Full` and `Empty` exceptions, the `maxlen` drop, the forced race (one thread gets the value, the other gets `IndexError`), and that `queue.Queue` has a `shutdown()` method (new in 3.13, so do not assume it on older versions). The lock-and-condition internals are stated from the standard library design, not from this run.

**Edge cases:**
- `Queue(maxsize=0)` (the default) is unbounded, so `put` never blocks and memory can grow without limit.
- `get()` on an empty `Queue` blocks forever without a timeout. A consumer needs a sentinel (as in the code) or a timeout to stop.
- One stop marker per consumer. A single sentinel would stop only one of them.
- `deque(maxlen=0)` accepts appends and keeps nothing.
- `Queue.qsize()` and `empty()` are only hints in a threaded program, because the answer can change right after you read it.

**Follow-ups:**
- "Why not use `multiprocessing.Queue`?" It crosses process boundaries by pickling items, so use it for processes, not threads.
- "Which queue gives a priority order?" `queue.PriorityQueue` (a min-heap behind the same blocking API); `LifoQueue` gives stack order.
- "Is `deque` safe if I only ever use `append` and `popleft` from different threads?" Each call is atomic in CPython, so a single producer and consumer work, but you must handle `IndexError` and you get no blocking. I would still pick `Queue` unless profiling shows lock cost matters.

**Common mistakes:**
- Writing `if d: d.popleft()` across threads.
- Forgetting `task_done()`, which makes `join()` hang.
- Using `Queue` for single-threaded BFS (pays for locks it does not need).
- Using `asyncio.Queue` from plain threads (it is not thread-safe).
- Expecting `deque(maxlen=k).append` to raise when full. It drops silently.

---

### Q32 ⭐ 🟡 Undo/redo and browser history with two stacks, at concept level (full system design belongs to Part 14). A text editor supports `type c`, `undo`, `redo`: undo moves the last typed character to the redo stack, redo moves it back, and typing a new character clears the redo stack. Return the text after each command. Then say how browser back/forward (`visit url`, `back`, `forward`) is the same two-stack idea (visiting clears the forward stack). Example: ['type a','type b','type c','undo','undo','redo','type d','redo','undo'] -> ['a','ab','abc','ab','a','ab','abd','abd','ab']; browser: visit x, visit y, visit z, back, back, forward, visit w, forward -> pages [x, y, z, y, x, y, w, w] ending on 'w'.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Two stacks as a "cursor in history". One stack holds the past, the other holds the undone future. Concept level only; the full system design is Part 14.

**Say this first (1 line):** "Undo pops the done stack onto the redo stack, redo does the reverse, and any new action clears the redo stack, because the old future no longer exists. Every command is O(1)."

**Brute force:** Keep a list of every text state and a pointer. Undo and redo move the pointer; typing cuts the list after the pointer and appends. Simple and correct, but it stores a full copy of the text per step: O(total length squared) space for typing n characters. It is my checker in the code.

**Optimal:**
- `done` is a stack of typed characters, `redo` a stack of undone ones.
- `type c`: push `c` on `done`, clear `redo`.
- `undo`: if `done` is not empty, move its top to `redo`.
- `redo`: if `redo` is not empty, move its top back to `done`.
- Text after each command is `"".join(done)`. (Joining each time is O(len); a real editor would keep the string incrementally, but the stack moves are O(1).)
- Browser: `back` stack, current page, `forward` stack. `visit u` pushes the current page on `back`, sets current to `u`, clears `forward`. `back` moves current to `forward` and pops `back`. `forward` is the mirror image.
- Invariant: `done` plus the reverse of `redo` is the full history line, and the cursor sits between them. Clearing `redo` on a new action is exactly "cut off the branch you left".

**Complexity:** Each command is O(1) for the stack moves. Space O(number of characters or pages). The per-command output string costs O(length) only because the prompt asks for the text after every step.

**Dry run:** `type a, type b, type c, undo, undo, redo, type d, redo, undo`.
| command | done | redo | text |
|---|---|---|---|
| type a | a | | a |
| type b | a b | | ab |
| type c | a b c | | abc |
| undo | a b | c | ab |
| undo | a | c b | a |
| redo | a b | c | ab |
| type d | a b d | (cleared) | abd |
| redo | a b d | | abd (nothing to redo) |
| undo | a b | d | ab |

Browser: visit x, y, z gives back = [x, y], current z. `back` gives current y, forward = [z]. `back` gives current x, forward = [z, y]. `forward` gives current y. `visit w` clears forward, current w. Last `forward` does nothing, so the page list is x, y, z, y, x, y, w, w.

**Code:**
```python
import random


class Editor:
    """Two stacks: `done` holds the typed characters, `redo` holds undone ones."""
    def __init__(self):
        self.done, self.redo = [], []

    def run(self, cmd):
        if cmd.startswith("type "):
            self.done.append(cmd[5])
            self.redo.clear()                 # a new edit kills the redo branch
        elif cmd == "undo":
            if self.done:
                self.redo.append(self.done.pop())
        elif cmd == "redo":
            if self.redo:
                self.done.append(self.redo.pop())
        return "".join(self.done)


def editor_fast(cmds):
    e = Editor()
    return [e.run(c) for c in cmds]


def editor_brute(cmds):
    # reference: keep every text state in a list plus a pointer
    states, p, out = [""], 0, []
    for c in cmds:
        if c.startswith("type "):
            states = states[:p + 1] + [states[p] + c[5]]
            p += 1
        elif c == "undo":
            p = max(0, p - 1)
        elif c == "redo":
            p = min(len(states) - 1, p + 1)
        out.append(states[p])
    return out


class Browser:
    def __init__(self):
        self.cur, self.back_s, self.fwd_s = None, [], []

    def run(self, cmd):
        if cmd.startswith("visit "):
            if self.cur is not None:
                self.back_s.append(self.cur)
            self.cur = cmd[6:]
            self.fwd_s.clear()                # visiting clears forward history
        elif cmd == "back" and self.back_s:
            self.fwd_s.append(self.cur)
            self.cur = self.back_s.pop()
        elif cmd == "forward" and self.fwd_s:
            self.back_s.append(self.cur)
            self.cur = self.fwd_s.pop()
        return self.cur


def browser_fast(cmds):
    b = Browser()
    return [b.run(c) for c in cmds]


def browser_brute(cmds):
    pages, i, out = [], -1, []
    for c in cmds:
        if c.startswith("visit "):
            pages = pages[:i + 1] + [c[6:]]
            i += 1
        elif c == "back":
            i = max(0, i - 1)
        elif c == "forward":
            i = min(len(pages) - 1, i + 1)
        out.append(pages[i])
    return out


ed = ['type a', 'type b', 'type c', 'undo', 'undo', 'redo', 'type d', 'redo', 'undo']
exp = ['a', 'ab', 'abc', 'ab', 'a', 'ab', 'abd', 'abd', 'ab']
print("editor :", editor_fast(ed))
assert editor_fast(ed) == editor_brute(ed) == exp

br = ['visit x', 'visit y', 'visit z', 'back', 'back', 'forward', 'visit w', 'forward']
exp_b = ['x', 'y', 'z', 'y', 'x', 'y', 'w', 'w']
print("browser:", browser_fast(br), "-> ends on", browser_fast(br)[-1])
assert browser_fast(br) == browser_brute(br) == exp_b

# edge cases
assert editor_fast(['undo', 'redo']) == ['', '']                   # no-ops on empty
assert editor_fast(['type a', 'undo', 'undo', 'redo', 'redo']) == ['a', '', '', 'a', 'a']
assert editor_fast([]) == []
assert browser_fast(['visit a', 'back', 'forward', 'forward']) == ['a', 'a', 'a', 'a']
assert browser_fast(['visit a', 'visit b', 'back', 'visit c', 'forward', 'back', 'back']) == \
    ['a', 'b', 'a', 'c', 'c', 'a', 'a']

# seeded randomised cross-check
rng = random.Random(32)
for _ in range(1500):
    n = rng.randint(0, 14)
    cs = [rng.choice(['type a', 'type b', 'type c', 'undo', 'redo']) for _ in range(n)]
    assert editor_fast(cs) == editor_brute(cs), cs
    bs = [rng.choice(['visit p', 'visit q', 'visit r', 'back', 'forward']) for _ in range(n)]
    bs = ['visit h'] + bs     # the brute force needs a first page to exist
    assert browser_fast(bs) == browser_brute(bs), bs
print("1500 + 1500 seeded random command lists agree with the snapshot-list reference")
```

**Output (my run):**
```text
editor : ['a', 'ab', 'abc', 'ab', 'a', 'ab', 'abd', 'abd', 'ab']
browser: ['x', 'y', 'z', 'y', 'x', 'y', 'w', 'w'] -> ends on w
1500 + 1500 seeded random command lists agree with the snapshot-list reference
```

The prompt's examples came out exactly as stated.

**Edge cases:**
- `undo` or `redo` on empty stacks is a no-op (the code returns the unchanged text).
- `back` on the first page and `forward` with an empty forward stack do nothing.
- Typing right after an undo discards the redo history (see `type d` above).
- No commands at all returns an empty list.

**Follow-ups:**
- "What if the history must be capped?" Use `deque(maxlen=limit)` for the done stack, so the oldest step falls off.
- "Undo for large edits, like pasting 1 MB?" Store the operation (insert at position, text) or its inverse, not a full snapshot of the document.
- "Multi-user editing?" That needs operational transforms or CRDTs; it is a Part 14 design topic, not a stack.

**Common mistakes:**
- Forgetting to clear `redo` on a new action. You then "redo" text that belongs to a dead branch.
- Pushing the very first (blank) page of the browser onto `back`.
- Letting `back` pop an empty stack.
- Storing snapshots and calling it O(1) space.

---

### Q33 ⭐ 🟡 Validate stack sequences. `pushed` is a list of distinct integers pushed in that order, and `popped` is a proposed pop order of the same values; pushes and pops may be interleaved arbitrarily. Return True if some interleaving produces exactly `popped` (len <= 1000). Simulate: push each value, and pop while the top equals the next wanted value; the sequence is valid iff the stack ends empty. Say why the greedy 'pop as soon as you can' is safe. Example: pushed=[1,2,3,4,5], popped=[4,5,3,2,1] -> True; pushed=[1,2,3,4,5], popped=[4,3,5,1,2] -> False.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Simulate the stack, and pop greedily. The stack is the only place a value can wait, so I can replay the process.

**Say this first (1 line):** "Push the values in order; after each push, pop while the top equals the next wanted value; the answer is True if the stack ends empty. Each value is pushed and popped once, so O(n)."

**Brute force:** Try every interleaving of pushes and pops with a recursive search. At each state either push the next value or pop the top if it matches. Worst case exponential (Catalan-sized state space). It is my checker.

**Optimal:**
- Keep `st` and a pointer `j` into `popped`.
- For each `v` in `pushed`: push it, then `while st and st[-1] == popped[j]: pop, j += 1`.
- Return `not st` (the lists have equal length, so an empty stack means every wanted value matched).
- Why greedy popping is safe: if the top equals the next wanted value, popping now is the only way to produce it next. Delaying would bury it under a later push, and a buried value cannot come out before the pushed value above it. So the choice "pop now" never loses a solution.
- Invariant: the stack holds, bottom to top, pushed values not yet popped, in push order. `popped[:j]` is already produced.

**Complexity:** Time O(n): each value is pushed once and popped at most once. Space O(n) for the stack.

**Dry run:** pushed = [1,2,3,4,5], popped = [4,5,3,2,1].
| push | stack after pops | j |
|---|---|---|
| 1 | [1] | 0 |
| 2 | [1,2] | 0 |
| 3 | [1,2,3] | 0 |
| 4 | top 4 equals popped[0], pop: [1,2,3] | 1 |
| 5 | top 5 equals popped[1], pop; then 3, 2, 1 pop | 5 |

Stack empty, True. For popped = [4,3,5,1,2]: after pushing 4 and popping it, top 3 matches, pop; push 5, pop it; stack [1,2], wanted 1 but top is 2, stuck. Non-empty, False.

**Code:**
```python
import itertools
import random


def valid_fast(pushed, popped):
    st, j = [], 0
    for v in pushed:
        st.append(v)
        while st and j < len(popped) and st[-1] == popped[j]:
            st.pop()
            j += 1
    return not st            # same length is given, so empty stack means all matched


def valid_brute(pushed, popped):
    # exhaustive search over every interleaving of pushes and pops
    n = len(pushed)
    def go(i, st, j):
        if j == n:
            return True
        if i < n and go(i + 1, st + (pushed[i],), j):
            return True
        if st and st[-1] == popped[j] and go(i, st[:-1], j + 1):
            return True
        return False
    return go(0, (), 0)


cases = [
    ([1, 2, 3, 4, 5], [4, 5, 3, 2, 1], True),
    ([1, 2, 3, 4, 5], [4, 3, 5, 1, 2], False),
    ([], [], True),
    ([7], [7], True),
    ([1, 2], [1, 2], True),
    ([1, 2], [2, 1], True),
    ([1, 2, 3], [3, 1, 2], False),
    ([2, 1, 0], [1, 2, 0], True),
]
for a, b, want in cases:
    assert valid_fast(a, b) == valid_brute(a, b) == want, (a, b)
print("valid_fast([1,2,3,4,5],[4,5,3,2,1]) ->", valid_fast([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]))
print("valid_fast([1,2,3,4,5],[4,3,5,1,2]) ->", valid_fast([1, 2, 3, 4, 5], [4, 3, 5, 1, 2]))

# exhaustive: every popped permutation for every n <= 7 (values 0..n-1 pushed in order)
tot = ok = 0
for n in range(0, 8):
    pushed = list(range(n))
    cnt = 0
    for perm in itertools.permutations(pushed):
        a = valid_fast(pushed, list(perm))
        tot += 1
        ok += a
        cnt += a
        if n <= 6:
            assert a == valid_brute(pushed, list(perm))
    print(f"n={n}: valid pop orders = {cnt}")
# the counts are the Catalan numbers 1,1,2,5,14,42,132,429 (checked via the printed rows)

# seeded random distinct values, shuffled pushed order, including popped that is not a permutation-checked case
rng = random.Random(33)
for _ in range(400):
    n = rng.randint(0, 6)
    vals = rng.sample(range(-20, 20), n)
    popped = vals[:]
    rng.shuffle(popped)
    assert valid_fast(vals, popped) == valid_brute(vals, popped)
print("400 seeded random cases agree with the exhaustive interleaving search")
```

**Output (my run):**
```text
valid_fast([1,2,3,4,5],[4,5,3,2,1]) -> True
valid_fast([1,2,3,4,5],[4,3,5,1,2]) -> False
n=0: valid pop orders = 1
n=1: valid pop orders = 1
n=2: valid pop orders = 2
n=3: valid pop orders = 5
n=4: valid pop orders = 14
n=5: valid pop orders = 42
n=6: valid pop orders = 132
n=7: valid pop orders = 429
400 seeded random cases agree with the exhaustive interleaving search
```

The counts of valid pop orders for n = 0..7 are 1, 1, 2, 5, 14, 42, 132, 429, which are the Catalan numbers (stack-sortable permutations), a nice sanity check that the simulation is exact over all 5,040 permutations of n = 7. I checked this against the exhaustive search for n up to 6; for n = 7 the Catalan counts are the cross-check. The prompt's two examples gave True and False as stated.

**Edge cases:**
- Empty lists: True.
- `popped` is exactly `pushed` (pop right after each push): True. Reversed `pushed`: True.
- A value wanted before it is reachable (such as [1,2,3] with [3,1,2]): False.
- If `popped` held values not in `pushed`, the stack would never empty, so False, but the prompt guarantees same values.

**Follow-ups:**
- "What if values repeat?" Greedy still works for matching by value, but the proof by "buried values" needs care; with duplicates I would compare by index of first occurrence or just trust the simulation, and test it against the exhaustive search.
- "Can you do it in O(1) space?" Reuse the front of `pushed` as the stack with a stack-pointer index, so the extra space is O(1) but the input is destroyed.
- "How many valid pop orders exist?" The n-th Catalan number, as the output shows.

**Common mistakes:**
- Checking `st[-1] == popped[j]` without guarding `j < len(popped)` or an empty stack.
- Popping only once after a push instead of a `while`.
- Returning True when the loop finishes without checking that the stack is empty.

---

### Q34 ⭐ 🟡 Exclusive time of functions. A single-threaded CPU runs n functions; `logs` lists strings 'id:start:t' and 'id:end:t' in time order (calls can nest; recursion allowed; a 'start' at t means the function runs from the beginning of time unit t, an 'end' at t means it runs through the end of time unit t). Return, for each function id, its exclusive time (time not spent in callees). Use a call stack with the previous timestamp: on a boundary, credit the elapsed time to the function on top. Example: n=2, ['0:start:0','1:start:2','1:end:5','0:end:6'] -> [3, 4]; n=1, ['0:start:0','0:start:2','0:end:5','0:start:6','0:end:6','0:end:7'] -> [8].
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Call stack with a "previous timestamp" marker. Time belongs to the function on top of the stack, so on every boundary I credit the elapsed slice to whoever was on top.

**Say this first (1 line):** "On start, give the caller the time since the last marker, then push the callee. On end, give the top the time through the end unit (+1), pop, and move the marker to t + 1. O(n) over the logs."

**Brute force:** Walk every time unit from 0 to the last timestamp, apply all events that happen at that unit, and credit the unit to the function on top. Correct but O(total time), which can be far larger than the number of logs (timestamps can be huge). It is my checker.

**Optimal:**
- State: `stack` of ids, `prev` (the first time unit not yet credited), `res` per function.
- `id:start:t`: if the stack is not empty, `res[top] += t - prev` (the caller ran from `prev` up to `t - 1`). Push `id`. Set `prev = t`.
- `id:end:t`: `res[top] += t - prev + 1` (through the end of unit `t`). Pop. Set `prev = t + 1`.
- The `+1` and `t + 1` come from the rule "end at t means it runs through the end of unit t". Start-at-t means starting at the beginning of unit t.
- Recursion needs no special case: the stack holds ids, and the same id can appear many times. Time is added to `res[id]` each time.
- Invariant: every unit before `prev` is already credited to exactly one function.

**Complexity:** O(n) time for n log lines, each doing O(1) work. Space O(depth of call nesting) for the stack plus O(number of functions) for the result.

**Dry run:** n = 2, `0:start:0, 1:start:2, 1:end:5, 0:end:6`.
| log | action | res | prev |
|---|---|---|---|
| 0:start:0 | stack empty, push 0 | [0,0] | 0 |
| 1:start:2 | res[0] += 2 - 0; push 1 | [2,0] | 2 |
| 1:end:5 | res[1] += 5 - 2 + 1 = 4; pop | [2,4] | 6 |
| 0:end:6 | res[0] += 6 - 6 + 1 = 1; pop | [3,4] | 7 |

Answer [3, 4], matching the prompt.

**Code:**
```python
import random


def exclusive_fast(n, logs):
    res, st, prev = [0] * n, [], 0
    for line in logs:
        i, kind, t = line.split(":")
        i, t = int(i), int(t)
        if kind == "start":
            if st:
                res[st[-1]] += t - prev      # time the caller ran before this call began
            st.append(i)
            prev = t
        else:
            res[st.pop()] += t - prev + 1    # the end unit t is included
            prev = t + 1
    return res


def exclusive_brute(n, logs):
    # reference: decide the owner of every single time unit
    res, st = [0] * n, []
    events = []
    for line in logs:
        i, kind, t = line.split(":")
        events.append((int(i), kind, int(t)))
    last_t = max(t for _, _, t in events)
    e = 0
    for unit in range(0, last_t + 1):
        while e < len(events) and events[e][1] == "start" and events[e][2] == unit:
            st.append(events[e][0]); e += 1
        if st:
            res[st[-1]] += 1                 # unit belongs to whoever is on top now
        while e < len(events) and events[e][1] == "end" and events[e][2] == unit:
            st.pop(); e += 1
    return res


def gen(rng):
    """Random valid log built from a call tree; also returns ground-truth owners."""
    n = rng.randint(1, 4)
    logs, owners, clock = [], [], [0]

    def run_units(f, k):
        owners.extend([f] * k)
        clock[0] += k

    def call(f, depth):
        logs.append(f"{f}:start:{clock[0]}")
        for _ in range(rng.randint(0, 2) if depth < 3 else 0):
            run_units(f, rng.randint(0, 3))
            call(rng.randrange(n), depth + 1)
        run_units(f, rng.randint(1, 3))
        logs.append(f"{f}:end:{clock[0] - 1}")

    call(rng.randrange(n), 0)
    truth = [owners.count(i) for i in range(n)]
    return n, logs, truth


# prompt examples
a = exclusive_fast(2, ['0:start:0', '1:start:2', '1:end:5', '0:end:6'])
b = exclusive_fast(1, ['0:start:0', '0:start:2', '0:end:5', '0:start:6', '0:end:6', '0:end:7'])
print(a, b)
assert a == [3, 4] and b == [8]
assert exclusive_brute(2, ['0:start:0', '1:start:2', '1:end:5', '0:end:6']) == [3, 4]
assert exclusive_brute(1, ['0:start:0', '0:start:2', '0:end:5', '0:start:6', '0:end:6', '0:end:7']) == [8]

# edge cases
assert exclusive_fast(1, ['0:start:0', '0:end:0']) == [1]                      # one unit
assert exclusive_fast(2, ['0:start:0', '1:start:0', '1:end:0', '0:end:0']) == [0, 1]                      # child owns the shared unit
assert exclusive_fast(3, ['0:start:5', '1:start:5', '2:start:5', '2:end:5', '1:end:5', '0:end:5']) == [0, 0, 1]
assert exclusive_fast(1, ['0:start:0', '0:end:3', '0:start:7', '0:end:9']) == [7]  # idle gap not counted

rng = random.Random(34)
for _ in range(1500):
    n, logs, truth = gen(rng)
    assert exclusive_fast(n, logs) == exclusive_brute(n, logs) == truth, (n, logs)
print("1500 seeded random call trees: stack == per-unit simulation == construction truth")
```

**Output (my run):**
```text
[3, 4] [8]
1500 seeded random call trees: stack == per-unit simulation == construction truth
```

Both prompt examples matched. In the random test the generator builds each log from a call tree and also records which function owned every unit, so the stack result, the per-unit simulation and that construction truth all agree.

**Edge cases:**
- A function that starts and ends in the same unit (`0:start:0`, `0:end:0`) gets 1 unit.
- A child that starts at the same unit as its parent: the parent gets 0 for that unit and the child owns it.
- Idle gaps between top-level calls are not counted (the second test with ids at 0..3 then 7..9 gives 7).
- Recursion: the same id on the stack several times.
- Logs are in time order, so no sorting is needed.

**Follow-ups:**
- "What if you also need inclusive time?" Keep the total of callee time in the stack frame and add it to the parent when popping, or record start times and compute `end - start + 1` per call (watch recursion double counting).
- "Multi-threaded logs?" One stack per thread id.
- "What if end logs can be missing?" Close the stack at the final timestamp.

**Common mistakes:**
- Forgetting the `+1` on end (off by one), or setting `prev = t` after an end instead of `t + 1`.
- Crediting time to the callee instead of the caller on a start.
- Using a dict keyed by id for the stack, which breaks on recursion.

---

### Q35 ⭐ 🟡 Maximum score with jumps of at most k (monotonic deque for DP). Start at index 0 of `nums` (len <= 10^5, values may be negative); from index i you may jump to any index in i+1..min(n-1, i+k); the score is the sum of the values at visited indices, and you must end at the last index. Return the maximum score. The DP is `dp[i] = nums[i] + max(dp[i-k..i-1])`; keep the window of dp values in a decreasing deque of indices for O(n), versus O(n*k) brute force. Example: nums=[1,-1,-2,4,-7,3], k=2 -> 7; nums=[10,-5,-2,4,0,3], k=3 -> 17; nums=[1,-5,-20,4,-1,3,-6,-3], k=2 -> 0.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** DP where each state needs the maximum over a sliding window of earlier states, so a monotonic (decreasing) deque replaces the O(k) scan.

**Say this first (1 line):** "dp[i] is nums[i] plus the best dp among the previous k indices. I keep those dp values in a decreasing deque of indices, so the max is at the front and every index enters and leaves once: O(n)."

**Brute force:** `dp[i] = nums[i] + max(dp[i-k..i-1])` with a direct `max` over the window. O(n * k) time, O(n) space. Fine for small k, too slow when n and k are both 10^5. A second checker enumerates every legal path (exponential, tiny inputs only).

**Optimal:**
- `dp[0] = nums[0]`. The deque holds indices whose dp values are strictly decreasing from front to back, all within the last k indices.
- For `i = 1..n-1`:
  - drop the front while its index is `< i - k` (out of reach);
  - `dp[i] = nums[i] + dp[front]`;
  - pop from the back while `dp[back] <= dp[i]`, then push `i`.
- Why popping is safe: an older index with a smaller or equal dp can never beat `i` for any later window, because `i` stays in range longer. That is the monotonic-queue invariant.
- Answer is `dp[n-1]`. Negative values are fine because the window is never empty: index `i-1` is always inside it.

**Complexity:** Time O(n): each index is pushed once and popped at most once. Space O(n) for `dp` (O(k) for the deque; `dp` could be reduced to the window but the clarity is worth it).

**Dry run:** nums = [1,-1,-2,4,-7,3], k = 2.
| i | window front | dp[i] | deque (indices) |
|---|---|---|---|
| 0 | | 1 | [0] |
| 1 | 0 (dp 1) | -1 + 1 = 0 | [0,1] |
| 2 | 0 (dp 1, index 0 >= 0) | -2 + 1 = -1 | [0,1,2] |
| 3 | drop 0 (0 < 1); front 1 (dp 0) | 4 + 0 = 4 | [3] |
| 4 | front 3 (dp 4) | -7 + 4 = -3 | [3,4] |
| 5 | front 3 (index 3 >= 3, dp 4) | 3 + 4 = 7 | [5] |

Answer 7.

**Code:**
```python
import random
from collections import deque


def max_score_fast(nums, k):
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    dq = deque([0])                      # indices, dp values decreasing front to back
    for i in range(1, n):
        while dq[0] < i - k:             # front index slid out of the window
            dq.popleft()
        dp[i] = nums[i] + dp[dq[0]]
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()                     # dominated: older and not larger
        dq.append(i)
    return dp[-1]


def max_score_brute(nums, k):
    n = len(nums)
    dp = [float("-inf")] * n
    dp[0] = nums[0]
    for i in range(1, n):
        dp[i] = nums[i] + max(dp[max(0, i - k):i])
    return dp[-1]


def max_score_paths(nums, k):
    # independent: enumerate every legal path (tiny inputs only)
    n = len(nums)
    best = float("-inf")
    def go(i, s):
        nonlocal best
        if i == n - 1:
            best = max(best, s)
            return
        for j in range(i + 1, min(n - 1, i + k) + 1):
            go(j, s + nums[j])
    go(0, nums[0])
    return best


tests = [
    ([1, -1, -2, 4, -7, 3], 2, 7),
    ([10, -5, -2, 4, 0, 3], 3, 17),
    ([1, -5, -20, 4, -1, 3, -6, -3], 2, 0),
    ([5], 1, 5),
    ([-3], 4, -3),
    ([-1, -2, -3], 1, -6),
    ([-1, -2, -3], 2, -4),
    ([2, 2, 2, 2], 4, 8),             # positives: visit everything
    ([2, -9, -9, 2], 4, 4),           # jump straight over the holes
]
for nums, k, want in tests:
    assert max_score_fast(nums, k) == max_score_brute(nums, k) == max_score_paths(nums, k) == want, (nums, k)
print([max_score_fast(a, k) for a, k, _ in tests[:3]])

rng = random.Random(35)
for _ in range(1500):
    n = rng.randint(1, 9)
    nums = [rng.randint(-6, 6) for _ in range(n)]
    k = rng.randint(1, 10)
    f = max_score_fast(nums, k)
    assert f == max_score_brute(nums, k) == max_score_paths(nums, k), (nums, k)
print("1500 seeded cases: deque DP == O(nk) DP == path enumeration")

# bigger random check of fast vs O(nk) brute, equal values stress the <= pop rule
for _ in range(300):
    n = rng.randint(1, 60)
    nums = [rng.randint(-3, 3) for _ in range(n)]
    k = rng.randint(1, 12)
    assert max_score_fast(nums, k) == max_score_brute(nums, k)
print("300 larger cases with many ties: ok")
big = [(-1) ** i * (i % 7) - 2 for i in range(3000)]
assert max_score_fast(big, 100) == max_score_brute(big, 100)
print("n=3000, k=100 deque DP == O(nk) DP:", max_score_fast(big, 100))
```

**Output (my run):**
```text
[7, 17, 0]
1500 seeded cases: deque DP == O(nk) DP == path enumeration
300 larger cases with many ties: ok
n=3000, k=100 deque DP == O(nk) DP: 2133
```

The three prompt examples gave 7, 17 and 0 as stated. The last line compares the deque DP with the O(nk) DP on a larger input (the printed number is just that shared result).

**Edge cases:**
- `n = 1`: answer `nums[0]`, no loop.
- `k >= n`: the window covers everything.
- All negative: you still must reach the end, so you pick the least bad stops (the `[-1,-2,-3]` tests with k = 1 and k = 2).
- Equal dp values: pop with `<=` to keep the deque small; keeping equals is also correct but bigger.
- Positive values: visit everything when k allows (see the `[2,2,2,2]` test).

**Follow-ups:**
- "Why not a heap?" A max-heap with lazy deletion works in O(n log n); the deque is O(n) and simpler.
- "Could a monotonic stack replace it?" No. The window has a left edge that moves, so you need pops from the front, hence a deque.
- "Same trick elsewhere?" Constrained subsequence sum, and any DP whose transition is a window max or min.

**Common mistakes:**
- Storing dp values instead of indices in the deque, so you cannot tell when the front expired.
- Expiring with `i - k` off by one (valid indices are `i-k .. i-1`).
- Updating the deque before computing `dp[i]`.
- Initialising `dp` with 0 and mishandling negatives.

---

### Q36 ⭐ 🟡 Design a circular deque. Implement a fixed-capacity double-ended queue of capacity k with `insertFront`, `insertLast` (False if full), `deleteFront`, `deleteLast` (False if empty), `getFront`, `getRear` (-1 if empty), `isEmpty`, `isFull`, all O(1) using modular arithmetic on a head index and a size (and state the index formula for the rear and for moving the head backwards without a negative modulo bug). Example with k=3: insertLast(1) -> True; insertLast(2) -> True; insertFront(3) -> True; insertFront(4) -> False; getRear() -> 2; isFull() -> True; deleteLast() -> True; insertFront(4) -> True; getFront() -> 4.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Ring buffer with modular arithmetic on `head` and `size`. Both ends can move, so the rear index is derived, not stored.

**Say this first (1 line):** "Store `head` and `size` over a fixed list. Rear slot is `(head + size) % k`, last element is `(head + size - 1) % k`, and moving the head back is `(head - 1) % k`. Every operation is O(1)."

**Brute force:** Wrap a Python `deque` and check `len(d) == k` before inserts. It is correct and O(1), and it is my reference in the code. The interview version asks for a preallocated array so you show the index math yourself.

**Optimal:**
- Arrays: `a` of length `k`, `head` (index of the front), `size`.
- `insertLast(v)`: if full, False; write at `(head + size) % k`; `size += 1`.
- `insertFront(v)`: if full, False; `head = (head - 1) % k`; write at `head`; `size += 1`.
- `deleteFront()`: if empty, False; `head = (head + 1) % k`; `size -= 1`.
- `deleteLast()`: if empty, False; `size -= 1`. The slot is simply forgotten.
- `getFront()` is `a[head]`; `getRear()` is `a[(head + size - 1) % k]`; both -1 when empty.
- Tracking `size` makes full and empty unambiguous (`head == tail` is true in both states otherwise), which is why it is simpler than sacrificing one slot.
- Negative modulo: in Python `(-1) % 3` is 2, so `(head - 1) % k` is safe. In C, Java or JavaScript `-1 % 3` is -1, so there you write `(head - 1 + k) % k`. Observed in the run on Python 3.13.17: `(-1) % 3 = 2`.

**Complexity:** Every operation is O(1) time. Space O(k) fixed.

**Dry run:** k = 3, starting with head = 0, size = 0, array [_,_,_].
| op | head | size | array | result |
|---|---|---|---|---|
| insertLast(1) | 0 | 1 | [1,_,_] | True |
| insertLast(2) | 0 | 2 | [1,2,_] | True |
| insertFront(3) | (0-1)%3 = 2 | 3 | [1,2,3] | True |
| insertFront(4) | 2 | 3 | [1,2,3] | False (full) |
| getRear() | | | slot (2+3-1)%3 = 1 holds 2 | 2 |
| isFull() | | | | True |
| deleteLast() | 2 | 2 | | True |
| insertFront(4) | 1 | 3 | [1,4,3] | True |
| getFront() | | | a[1] | 4 |

**Code:**
```python
import random
from collections import deque


class CircularDeque:
    def __init__(self, k):
        self.a = [0] * k
        self.k = k
        self.head = 0                    # index of the front element
        self.size = 0

    def insertFront(self, v):
        if self.size == self.k:
            return False
        self.head = (self.head - 1) % self.k      # Python's % is never negative
        self.a[self.head] = v
        self.size += 1
        return True

    def insertLast(self, v):
        if self.size == self.k:
            return False
        self.a[(self.head + self.size) % self.k] = v
        self.size += 1
        return True

    def deleteFront(self):
        if self.size == 0:
            return False
        self.head = (self.head + 1) % self.k
        self.size -= 1
        return True

    def deleteLast(self):
        if self.size == 0:
            return False
        self.size -= 1
        return True

    def getFront(self):
        return -1 if self.size == 0 else self.a[self.head]

    def getRear(self):
        return -1 if self.size == 0 else self.a[(self.head + self.size - 1) % self.k]

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.k


class RefDeque:
    """Brute force: a Python deque plus a capacity check."""
    def __init__(self, k):
        self.d, self.k = deque(), k

    def insertFront(self, v):
        if len(self.d) == self.k: return False
        self.d.appendleft(v); return True

    def insertLast(self, v):
        if len(self.d) == self.k: return False
        self.d.append(v); return True

    def deleteFront(self):
        if not self.d: return False
        self.d.popleft(); return True

    def deleteLast(self):
        if not self.d: return False
        self.d.pop(); return True

    def getFront(self): return self.d[0] if self.d else -1
    def getRear(self): return self.d[-1] if self.d else -1
    def isEmpty(self): return not self.d
    def isFull(self): return len(self.d) == self.k


c = CircularDeque(3)
trace = [c.insertLast(1), c.insertLast(2), c.insertFront(3), c.insertFront(4),
         c.getRear(), c.isFull(), c.deleteLast(), c.insertFront(4), c.getFront()]
print(trace)
assert trace == [True, True, True, False, 2, True, True, True, 4]
print("(-1) % 3 =", (-1) % 3, "in Python (a C-style % would give -1)")

# edge cases
c1 = CircularDeque(1)
assert c1.getFront() == -1 and c1.getRear() == -1 and not c1.deleteFront() and not c1.deleteLast()
assert c1.insertFront(7) and c1.isFull() and not c1.insertLast(8) and not c1.insertFront(8)
assert c1.getFront() == c1.getRear() == 7 and c1.deleteLast() and c1.isEmpty()
c2 = CircularDeque(3)                    # wrap-around on both ends
for v in (1, 2, 3):
    assert c2.insertFront(v)             # front-to-back: 3 2 1
assert [c2.getFront(), c2.getRear()] == [3, 1]
assert c2.deleteFront() and c2.insertLast(9) and [c2.getFront(), c2.getRear()] == [2, 9]

rng = random.Random(36)
ops = ["insertFront", "insertLast", "deleteFront", "deleteLast", "getFront", "getRear", "isEmpty", "isFull"]
for _ in range(2000):
    k = rng.randint(1, 6)
    a, b = CircularDeque(k), RefDeque(k)
    for _ in range(rng.randint(1, 40)):
        op = rng.choice(ops)
        if op.startswith("insert"):
            v = rng.randint(1, 99)
            assert getattr(a, op)(v) == getattr(b, op)(v), (k, op)
        else:
            assert getattr(a, op)() == getattr(b, op)(), (k, op)
print("2000 seeded random op sequences match the deque-based reference")
```

**Output (my run):**
```text
[True, True, True, False, 2, True, True, True, 4]
(-1) % 3 = 2 in Python (a C-style % would give -1)
2000 seeded random op sequences match the deque-based reference
```

The prompt's example trace matched exactly.

**Edge cases:**
- `k = 1`: front and rear are the same slot; insert at either end fills it.
- Wrap-around at both ends (the `c2` test fills with `insertFront` three times).
- Empty returns -1 for `getFront` and `getRear`, and False for deletes.
- Stale values left in freed slots are harmless because `size` guards every read.

**Follow-ups:**
- "Make it resizable?" Double the array when full and copy elements in logical order starting from `head`, so the head resets to 0. Amortised O(1), like `list.append`.
- "Why not a linked list?" It also gives O(1) ends, but costs a node per item and has worse cache behaviour; a ring buffer reuses fixed memory.
- "Is `collections.deque` a ring buffer?" CPython's deque is a doubly linked list of blocks, not one flat ring, which is why indexing into the middle is O(n).

**Common mistakes:**
- `(head - 1) % k` ported to a language where `%` can be negative.
- Using `head == tail` for both full and empty.
- Computing the last element as `(head + size) % k` (that is the next free slot, one past the end).
- Forgetting that `deleteLast` needs no head move.

---

### Q37 ⭐ 🔴 Basic calculator with all four operators and parentheses. `s` is a valid expression of non-negative integers, '+', '-', '*', '/', parentheses and spaces (up to 10^4 characters); '/' truncates toward zero. Evaluate it without `eval`. Use a stack of numbers with operator precedence handled by the pending operator, and a second stack (or an explicit recursion-to-stack conversion) to save the context at each '('. Part 3 Q13 covers the parenthesis-free single-pass version; here the parentheses are the point. Example: '1+1' -> 2; '6-4/2' -> 4; '2*(5+5*2)/3+(6/2+8)' -> 21; '(2+6*3+5-(3*14/7+2)*5)+3' -> -12.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Stack of numbers for precedence, plus a stack of saved contexts for parentheses. Part 3 Q13 handles the no-parentheses version with the "last term" accumulator; here the brackets are the point.

**Say this first (1 line):** "A stack of numbers with a pending operator: plus and minus push a signed number, star and slash fold into the top. At '(' I save the current stack and operator and start fresh; at ')' I sum the inner stack and treat that sum as the next number. One pass, O(n)."

**Brute force:** A recursive-descent parser with `expr`, `term` and `atom` functions. Clean and correct, but recursion depth equals bracket nesting, and CPython's default limit is 1000 frames, so a deeply nested input crashes. It is my checker (on small inputs). `eval` is not an answer: `/` gives a float and it executes arbitrary text.

**Optimal:**
- State: `stack` (terms of the current bracket level), `op` (the operator before the current number), `num`, and `ctx` (saved `(stack, op)` pairs).
- Digit: build `num`.
- Operator `+ - * /`: apply `op` to `num`: `+` pushes `num`, `-` pushes `-num`, `*` multiplies the top, `/` divides the top truncating toward zero. Then `op = this operator`, `num = 0`.
- `(`: push `(stack, op)` on `ctx`, start a new empty `stack`, `op = '+'`.
- `)`: apply `op` to `num`, set `num = sum(stack)`, restore `(stack, op)` from `ctx`. The pending `num` is now the bracket's value, waiting for the next operator.
- A sentinel `+` at the end flushes the last number. Answer `sum(stack)`.
- Truncation: Python `//` floors (`-7 // 2 = -4`), so divide absolute values and restore the sign.
- Invariant: `sum(stack)` plus the pending `op num` equals the value of everything parsed at this bracket level.

**Complexity:** Time O(n): each character is handled once, and `sum(stack)` at each `)` touches elements that are then discarded, so the total is O(n). Space O(n) for the stacks in the worst case (deep nesting or many terms). No recursion, so nesting depth is limited only by memory.

**Dry run:** `2*(3+4)-1`.
| char | action | stack | ctx | op | num |
|---|---|---|---|---|---|
| 2 | num = 2 | [] | | + | 2 |
| * | push 2; op = * | [2] | | * | 0 |
| ( | save ([2], *); new stack | [] | [([2],*)] | + | 0 |
| 3 | | [] | | + | 3 |
| + | push 3; op = + | [3] | | + | 0 |
| 4 | | [3] | | + | 4 |
| ) | push 4; num = 7; restore | [2] | [] | * | 7 |
| - | apply *: top = 14; op = - | [14] | | - | 0 |
| 1, then sentinel + | push -1 | [14,-1] | | + | 0 |

Answer 13.

**Code:**
```python
import random


def tdiv(a, b):
    q = abs(a) // abs(b)                  # Python // floors, so truncate by hand
    return q if (a >= 0) == (b > 0) else -q


def calc_fast(s):
    def apply(stack, op, num):
        if op == "+":
            stack.append(num)
        elif op == "-":
            stack.append(-num)
        elif op == "*":
            stack[-1] *= num
        else:
            stack[-1] = tdiv(stack[-1], num)

    stack, op, num, ctx = [], "+", 0, []
    for ch in s + "+":                    # sentinel flushes the last number
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "(":
            ctx.append((stack, op))       # save the outer context
            stack, op, num = [], "+", 0
        elif ch == ")":
            apply(stack, op, num)
            num = sum(stack)              # value of the bracket becomes the next operand
            stack, op = ctx.pop()
        elif ch != " ":
            apply(stack, op, num)
            op, num = ch, 0
    return sum(stack)


def calc_brute(s):
    # independent recursive-descent parser (fine for the small brute-force sizes)
    t = [c for c in s if c != " "]
    pos = 0

    def expr():
        nonlocal pos
        v = term()
        while pos < len(t) and t[pos] in "+-":
            o = t[pos]; pos += 1
            r = term()
            v = v + r if o == "+" else v - r
        return v

    def term():
        nonlocal pos
        v = atom()
        while pos < len(t) and t[pos] in "*/":
            o = t[pos]; pos += 1
            r = atom()
            v = v * r if o == "*" else tdiv(v, r)
        return v

    def atom():
        nonlocal pos
        if t[pos] == "(":
            pos += 1
            v = expr()
            pos += 1                      # ')'
            return v
        j = pos
        while j < len(t) and t[j].isdigit():
            j += 1
        v = int("".join(t[pos:j]))
        pos = j
        return v

    return expr()


tests = [("1+1", 2), ("6-4/2", 4), ("2*(5+5*2)/3+(6/2+8)", 21),
         ("(2+6*3+5-(3*14/7+2)*5)+3", -12)]
for s, want in tests:
    assert calc_fast(s) == calc_brute(s) == want, s
    print(f"{s!r} -> {calc_fast(s)}")

# edge cases
assert calc_fast("7") == 7 and calc_fast(" 42 ") == 42
assert calc_fast("((7))") == 7
assert calc_fast("(2-5)/2") == -1                 # truncates toward zero (floor would give -2)
assert calc_fast("0-7/2") == -3 and calc_fast("7/2") == 3
assert calc_fast("2*(3+4)*(5-1)") == 56
assert calc_fast("10-(2+3)*2/(1+1)") == 5
assert calc_fast("8/(3-1)/2") == 2                # left-to-right division chain
assert calc_fast("100*(1+(2*(3+(4*5))))") == 4700
assert -7 // 2 == -4 and tdiv(-7, 2) == -3
assert calc_fast("(" * 5000 + "1" + ")" * 5000) == 1   # nesting depth 5000, no recursion used
assert calc_fast("1" + "+1" * 100000) == 100001

# seeded random expressions (skip those with a zero divisor)
rng = random.Random(37)

def gen(depth):
    if depth == 0 or rng.random() < 0.3:
        return str(rng.randint(0, 12))
    a, b = gen(depth - 1), gen(depth - 1)
    o = rng.choice("+-*/")
    e = f"{a}{o}{b}"
    if rng.random() < 0.5:
        e = f"({e})"
    return e

tested = skipped = 0
for _ in range(4000):
    e = gen(rng.randint(1, 4))
    if rng.random() < 0.3:
        e = e.replace("+", " + ")
    try:
        want = calc_brute(e)
    except ZeroDivisionError:
        skipped += 1
        continue
    assert calc_fast(e) == want, e
    tested += 1
print(f"seeded random expressions: {tested} compared, {skipped} skipped (zero divisor)")
```

**Output (my run):**
```text
'1+1' -> 2
'6-4/2' -> 4
'2*(5+5*2)/3+(6/2+8)' -> 21
'(2+6*3+5-(3*14/7+2)*5)+3' -> -12
seeded random expressions: 3791 compared, 209 skipped (zero divisor)
```

All four prompt examples matched, including the nested one that gives -12. The random run skips expressions where a divisor evaluates to zero because the prompt guarantees valid input.

**Edge cases:**
- `(2-5)/2` is -1 (truncation). Floor division would give -2.
- Redundant brackets `((7))` and a bracket straight after an operator (`10-(2+3)*2`).
- Division chain `8/(3-1)/2` goes left to right.
- Spaces anywhere, including `+ ` before a bracket.
- 5000 nested brackets and 100,000 terms both pass because nothing is recursive.
- No unary minus is allowed by the prompt. If it were, treat a `-` right after `(` or at the start as `0 -`.

**Follow-ups:**
- "How would you add `^` or unary minus?" Add an operator-precedence stack (shunting-yard) with precedence and associativity, or insert a leading 0 for unary minus.
- "Why a stack per bracket and not one shared stack?" The context stack saves what to resume; the inner stack accumulates a new sub-expression independently.
- "What changes for floats?" Keep numbers as floats, parse decimal points, and drop the truncation helper.

**Common mistakes:**
- Using `//` on negatives (floor instead of truncation).
- Forgetting to flush the last number (sentinel) or the number just before `)`.
- Resetting `op` to the wrong value after `)`: it must come back from the saved context, not stay as the inner operator.
- Parsing multi-digit numbers digit by digit as separate numbers.

---

### Q38 ⭐ 🔴 Max stack. Design a stack with `push(x)`, `pop()`, `top()`, `peekMax()` and `popMax()` (removes and returns the topmost occurrence of the maximum). `top`, `peekMax` and `push` should be O(1) or O(log n); explain the two-stack solution where `popMax` pops until it finds the max and pushes the rest back (O(n)), and the O(log n) design with a doubly linked list plus a sorted structure or a heap with lazy deletion. Example: push(5), push(1), push(5), top() -> 5, popMax() -> 5, top() -> 1, peekMax() -> 5, pop() -> 1, top() -> 5.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Stack augmented with a second structure for the maximum. The hard part is `popMax`, which removes an element from the middle of a stack.

**Say this first (1 line):** "Two stacks give O(1) push, pop, top and peekMax, but popMax costs O(n) because I pop down to the max and push the rest back; for O(log n) I use a stack of ids plus a max-heap with lazy deletion."

**Brute force:** One list; `peekMax` is `max(list)` (O(n)) and `popMax` finds the topmost maximum by scanning from the end and removing it (O(n)). It is my checker.

**Optimal:** Two designs.
- Design A, two stacks (O(n) `popMax`):
  - Main stack `s` and a parallel stack `m` of running maximums (`m[-1]` is the max of everything below and including the top).
  - `popMax`: remember `mx = m[-1]`, pop from `s` into a buffer until the top equals `mx`, pop that one, then push the buffered values back in original order (which also rebuilds `m`).
- Design B, heap with lazy deletion (O(log n) amortised):
  - Give every pushed item an id. The stack holds ids; a max-heap holds `(-value, -id)` so the largest value comes first and, among equals, the newest id (the topmost one) comes first.
  - `pop` and `popMax` do not remove the item from the other structure. They put its id into a `dead` set. Before reading a stack top or a heap top, discard entries whose id is dead.
  - Each id is discarded from each structure at most once, so the total cost is amortised O(log n) per operation (the heap dominates).
- Invariant for B: the live items are exactly the ids not in `dead`; both structures contain a superset of them, in the correct order.
- A balanced alternative is a doubly linked list plus a sorted container (`sortedcontainers` is not in the standard library, so I would only mention it), which gives true O(log n) worst case.

**Complexity:**
| Design | push | pop, top | peekMax | popMax |
|---|---|---|---|---|
| Brute force | O(1) | O(1) | O(n) | O(n) |
| Two stacks | O(1) | O(1) | O(1) | O(n) |
| Heap + lazy deletion | O(log n) | O(1) amortised | O(log n) amortised | O(log n) amortised |
Space O(n) for each design. In B, dead entries linger until they reach the top of a structure, so memory is bounded by the number of pushes, not the live size.

**Dry run:** the prompt's example with design A.
| op | `s` | `m` | result |
|---|---|---|---|
| push 5 | [5] | [5] | |
| push 1 | [5,1] | [5,5] | |
| push 5 | [5,1,5] | [5,5,5] | |
| top | | | 5 |
| popMax | pop 5 (top is already max) | | 5 |
| top | [5,1] | [5,5] | 1 |
| peekMax | | | 5 |
| pop | [5] | [5] | 1 |
| top | | | 5 |

**Code:**
```python
import heapq
import random


class MaxStackTwo:
    """Two stacks: O(1) push/pop/top/peekMax, O(n) popMax."""
    def __init__(self):
        self.s, self.m = [], []

    def push(self, x):
        self.s.append(x)
        self.m.append(x if not self.m else max(x, self.m[-1]))

    def pop(self):
        self.m.pop()
        return self.s.pop()

    def top(self):
        return self.s[-1]

    def peekMax(self):
        return self.m[-1]

    def popMax(self):
        mx, buf = self.m[-1], []
        while self.s[-1] != mx:           # dig down to the topmost max
            buf.append(self.pop())
        self.pop()
        for x in reversed(buf):           # put the others back in order
            self.push(x)
        return mx


class MaxStackHeap:
    """Heap with lazy deletion: O(log n) amortised for every operation."""
    def __init__(self):
        self.stack, self.heap, self.val = [], [], {}
        self.dead, self.uid = set(), 0

    def push(self, x):
        self.uid += 1
        self.val[self.uid] = x
        self.stack.append(self.uid)
        heapq.heappush(self.heap, (-x, -self.uid))   # newest id wins ties = topmost

    def _clean_stack(self):
        while self.stack[-1] in self.dead:
            self.stack.pop()

    def _clean_heap(self):
        while -self.heap[0][1] in self.dead:
            heapq.heappop(self.heap)

    def pop(self):
        self._clean_stack()
        i = self.stack.pop()
        self.dead.add(i)
        return self.val[i]

    def top(self):
        self._clean_stack()
        return self.val[self.stack[-1]]

    def peekMax(self):
        self._clean_heap()
        return -self.heap[0][0]

    def popMax(self):
        self._clean_heap()
        x, i = heapq.heappop(self.heap)
        self.dead.add(-i)
        return -x


class MaxStackBrute:
    def __init__(self):
        self.a = []

    def push(self, x): self.a.append(x)
    def pop(self): return self.a.pop()
    def top(self): return self.a[-1]
    def peekMax(self): return max(self.a)

    def popMax(self):
        m = max(self.a)
        for i in range(len(self.a) - 1, -1, -1):     # topmost occurrence
            if self.a[i] == m:
                return self.a.pop(i)


def drive(cls, ops):
    o, out = cls(), []
    for name, *arg in ops:
        out.append(getattr(o, name)(*arg))
    return out


ex = [("push", 5), ("push", 1), ("push", 5), ("top",), ("popMax",), ("top",),
      ("peekMax",), ("pop",), ("top",)]
want = [None, None, None, 5, 5, 1, 5, 1, 5]
for cls in (MaxStackTwo, MaxStackHeap, MaxStackBrute):
    assert drive(cls, ex) == want, cls.__name__
print("example ->", drive(MaxStackHeap, ex))

# edge cases: duplicates of the max are removed topmost first, order of the rest kept
dup = [("push", 2), ("push", 7), ("push", 3), ("push", 7), ("popMax",), ("top",),
       ("popMax",), ("top",), ("pop",), ("top",)]
for cls in (MaxStackTwo, MaxStackHeap, MaxStackBrute):
    assert drive(cls, dup) == [None] * 4 + [7, 3, 7, 3, 3, 2], cls.__name__
one = [("push", -4), ("peekMax",), ("popMax",)]
for cls in (MaxStackTwo, MaxStackHeap, MaxStackBrute):
    assert drive(cls, one) == [None, -4, -4]

rng = random.Random(38)
for _ in range(3000):
    ops, size = [], 0
    for _ in range(rng.randint(1, 40)):
        r = rng.random()
        if size == 0 or r < 0.4:
            ops.append(("push", rng.randint(-4, 4))); size += 1
        else:
            name = rng.choice(["pop", "top", "peekMax", "popMax"])
            ops.append((name,))
            if name in ("pop", "popMax"):
                size -= 1
    r0 = drive(MaxStackBrute, ops)
    assert drive(MaxStackTwo, ops) == r0 and drive(MaxStackHeap, ops) == r0, ops
print("3000 seeded random op lists: two-stack == heap+lazy delete == brute force")
```

**Output (my run):**
```text
example -> [None, None, None, 5, 5, 1, 5, 1, 5]
3000 seeded random op lists: two-stack == heap+lazy delete == brute force
```

The example produced the values stated in the prompt (`None` marks the push calls, which return nothing).

**Edge cases:**
- Duplicate maximums: `popMax` removes the topmost one, so the order of the others is preserved (the `dup` test: 7 is removed from the top first).
- Single element: `popMax` and `pop` both empty the stack.
- Negative values are fine; the running maximum starts from the first element, not from 0.
- The prompt says pop, top and the max calls are never made on an empty stack, so no empty checks are needed.

**Follow-ups:**
- "Can `popMax` be O(1)?" Not with this interface in general; O(log n) is the usual target. A pure linked list of equal values per distinct maximum is a different structure.
- "What about a plain max-only stack (no `popMax`)?" The parallel running-max stack alone gives O(1) for everything, like Min Stack.
- "Why a tie-break by id in the heap?" Without it the heap could remove an older duplicate and the stack order would be wrong.

**Common mistakes:**
- Removing the first (bottom) maximum instead of the topmost one.
- Pushing the buffered values back in reverse order.
- Forgetting to clean the stack top after a `popMax` made it dead (lazy design).
- Keeping only values in the heap with no id, so you cannot tell which copy was removed.

---

### Q39 ⭐ 🔴 Number of visible people in a queue. `heights` is a list of distinct integers (len <= 10^5) for people standing in a row, left to right. Person i can see person j > i if every person strictly between them is shorter than both of them. Return, for each i, how many people to its right it can see. Use a decreasing stack from the right; count each pop as one seen person plus one more if the stack is non-empty afterwards. Example: [10,6,8,5,11,9] -> [3,1,2,1,1,0]; [5,1,2,3,10] -> [4,1,1,1,0].
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Monotonic stack scanned from the right. The stack holds the people to the right that are still visible candidates for someone further left: the nearest person is on top, and heights increase toward the bottom.

**Say this first (1 line):** "Scan from the right with a stack whose heights grow taller toward the bottom.For person i, every shorter person I pop is one I can see, and the first taller person left on the stack is one more I can see. Then push i. O(n)."

**Brute force:** For each i, for each j > i, check that every person between is shorter than both: O(n^3) as written (O(n^2) with a running maximum). Too slow for n = 10^5. It is my checker.

**Optimal:**
- Why the shorter ones are seen: person i sees j if everything between is shorter than both. Walking right from i, the people i can see are exactly the ones that set a new "tallest so far" record, until a person taller than i appears (that person is seen but blocks everything beyond).
- The stack from the right holds those record-setters relative to the current position, nearest on top, heights increasing downward.
- For each i from right to left:
  - `c = 0`; while the top is shorter than `h[i]`: pop it and `c += 1` (i sees it, and now i hides it from everyone to the left, since i is taller);
  - if the stack is not empty, the top is taller than `h[i]`: `c += 1` (i sees that blocker);
  - `ans[i] = c`; push `h[i]`.
- Distinct heights (guaranteed) mean no tie rule is needed. With equal heights you would have to decide whether an equal person blocks.
- Invariant: after processing i, the stack holds the people visible from the left edge of the suffix starting at i, heights increasing from top to bottom.

**Complexity:** Time O(n): each person is pushed once and popped at most once. Space O(n) for the stack and the answer.

**Dry run:** [10,6,8,5,11,9], from the right.
| i (height) | pops (seen shorter) | blocker seen? | ans | stack top to bottom after push |
|---|---|---|---|---|
| 5 (9) | none | no (empty) | 0 | 9 |
| 4 (11) | pop 9 | no | 1 | 11 |
| 3 (5) | none | yes (11) | 1 | 5, 11 |
| 2 (8) | pop 5 | yes (11) | 2 | 8, 11 |
| 1 (6) | none | yes (8) | 1 | 6, 8, 11 |
| 0 (10) | pop 6, 8 | yes (11) | 3 | 10, 11 |

Answer [3, 1, 2, 1, 1, 0], matching the prompt.

**Code:**
```python
import random


def visible_fast(h):
    n, ans, st = len(h), [0] * len(h), []
    for i in range(n - 1, -1, -1):
        c = 0
        while st and st[-1] < h[i]:
            st.pop()
            c += 1                  # a shorter person that i sees
        if st:
            c += 1                  # the first taller person, who blocks the rest
        ans[i] = c
        st.append(h[i])
    return ans


def visible_brute(h):
    n, ans = len(h), []
    for i in range(n):
        c = 0
        for j in range(i + 1, n):
            if all(h[m] < min(h[i], h[j]) for m in range(i + 1, j)):
                c += 1
        ans.append(c)
    return ans


a = visible_fast([10, 6, 8, 5, 11, 9])
b = visible_fast([5, 1, 2, 3, 10])
print(a, b)
assert a == visible_brute([10, 6, 8, 5, 11, 9]) == [3, 1, 2, 1, 1, 0]
assert b == visible_brute([5, 1, 2, 3, 10]) == [4, 1, 1, 1, 0]

# edge cases
assert visible_fast([]) == [] and visible_fast([7]) == [0]
assert visible_fast([1, 2]) == [1, 0] and visible_fast([2, 1]) == [1, 0]
assert visible_fast([5, 4, 3, 2, 1]) == [1, 1, 1, 1, 0]       # decreasing: only the neighbour
assert visible_fast([1, 2, 3, 4, 5]) == [1, 1, 1, 1, 0]       # increasing: only the neighbour
assert visible_fast(list(range(100000, 0, -1)))[:2] == [1, 1]  # large input, no quadratic blow-up

# seeded random check; distinct integers as the prompt states
rng = random.Random(39)
for _ in range(2000):
    n = rng.randint(0, 9)
    h = rng.sample(range(1, 30), n)
    assert visible_fast(h) == visible_brute(h), h
print("2000 seeded random permutations agree with the O(n^3) definition")

# each person is popped at most once: count pops on a random input
h = rng.sample(range(1, 10**6), 50000)
st, pops = [], 0
for x in reversed(h):
    while st and st[-1] < x:
        st.pop(); pops += 1
    st.append(x)
assert pops <= len(h)
print("n=50000: pops =", pops, "<= n")
```

**Output (my run):**
```text
[3, 1, 2, 1, 1, 0] [4, 1, 1, 1, 0]
2000 seeded random permutations agree with the O(n^3) definition
n=50000: pops = 49990 <= n
```

Both prompt examples matched. The last line counts pops on a random 50,000-person input to show the amortised bound: pops never exceed n.

**Edge cases:**
- Empty row and a single person: 0.
- Strictly increasing or strictly decreasing rows: each person sees only the neighbour.
- The last person always sees 0.
- Tallest person: sees every record-setter to the right, with no blocker added.
- Equal heights (outside the prompt): decide whether an equal person is visible and pops; test with the brute force if you change the rule.

**Follow-ups:**
- "What if heights repeat?" Define the rule first (does an equal height block?). Pop on `<=` or `<` accordingly, and adjust the blocker count.
- "Count how many people can see i instead?" Run the same scan from the left.
- "Can you do it without a stack?" Not in O(n); this is a next-greater-element variant that counts pops.

**Common mistakes:**
- Forgetting the +1 for the first taller person after the pops.
- Scanning from the left, which makes the counting awkward.
- Popping with `<=` on distinct data (harmless) but copying that habit to a duplicates version without rechecking.
- Adding 1 for the blocker even when the stack is empty.

---

### Q40 ⭐ 🔴 The 132 pattern. Given integers `nums` (len <= 2*10^5), decide whether there are indices i < j < k with nums[i] < nums[k] < nums[j]. Scan from the right, keeping a decreasing stack and a variable for the largest 'third' value popped so far (the '2'); a new element smaller than that value completes the pattern. Explain why the popped value is the best '2' to remember, and give the O(n^2) check as a reference. Example: [1,2,3,4] -> False; [3,1,4,2] -> True; [-1,3,2,0] -> True.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Monotonic stack from the right, with a remembered "best 2". The pattern asks for i < j < k with nums[i] < nums[k] < nums[j].

**Say this first (1 line):** "Scan right to left with a decreasing stack and a variable `third` for the largest value ever popped, because a popped value always has a bigger one to its left, so it is a valid '2'. If the current element is smaller than `third`, it is the '1' and I am done. O(n)."

**Brute force:** O(n^3): try every triple. An O(n^2) version keeps the running minimum before j and scans k > j for a value strictly between that minimum and `nums[j]`. Both are my checkers in the code.

**Optimal:**
- Roles: `x` is the '1' (leftmost); to its right comes a bigger '3', and after that a '2' with value strictly between `x` and the '3'.
- Scan `x` from the right. The stack holds candidates for '3' (decreasing from bottom to top, so the top is the smallest).
- While the top is smaller than `x`: pop it and set `third = popped`. Reason: `x` is to the left of that popped value and larger than it, so `x` can be its '3', and the popped value is a valid '2'.
- If `x < third`, then `x` is a valid '1'. The '2' (`third`) was popped by a bigger element, the '3', that sits to the left of the '2'. Both were scanned before `x`, so both are to the right of `x`. That gives i < j < k with `x < third < '3'`. Return True.
- Push `x`.
- Why the largest popped value is the best '2': the condition on the '1' is `x < third`, and a larger `third` accepts more candidates. Any popped value had a larger value to its left at the time, so every popped value is valid, and the maximum is the most permissive.
- Invariant: `third` is the largest value that has a strictly larger value to its left among the elements already scanned.

**Complexity:** Time O(n): each element is pushed once and popped at most once. Space O(n) for the stack.

**Dry run:** [3,1,4,2], from the right.
| x | action | stack (bottom to top) | third |
|---|---|---|---|
| 2 | not < -inf; push | [2] | -inf |
| 4 | pop 2, third = 2; push 4 | [4] | 2 |
| 1 | 1 < 2, found | | |

True (the pattern is 1, 4, 2). For [1,2,3,4]: x=4 push; x=3 push; x=2 push; x=1 never below `third`, which stays -inf: False.

**Code:**
```python
import itertools
import random


def has132_fast(nums):
    third = float("-inf")          # largest valid '2' found so far (it has a bigger '3' left of it)
    st = []                        # decreasing from bottom to top, scanning right to left
    for x in reversed(nums):
        if x < third:
            return True            # x plays the '1'
        while st and st[-1] < x:
            third = st.pop()       # popped value has x (bigger) to its left: a valid '2'
        st.append(x)
    return False


def has132_n2(nums):
    n = len(nums)
    lo = float("inf")              # smallest value strictly before j
    for j in range(n):
        for k in range(j + 1, n):
            if lo < nums[k] < nums[j]:
                return True
        lo = min(lo, nums[j])
    return False


def has132_n3(nums):
    return any(nums[i] < nums[k] < nums[j]
               for i, j, k in itertools.combinations(range(len(nums)), 3))


for a, want in [([1, 2, 3, 4], False), ([3, 1, 4, 2], True), ([-1, 3, 2, 0], True)]:
    assert has132_fast(a) == has132_n2(a) == has132_n3(a) == want, a
    print(a, "->", has132_fast(a))

# edge cases
assert has132_fast([]) is False and has132_fast([1]) is False and has132_fast([1, 2]) is False
assert has132_fast([2, 2, 2, 2]) is False          # equal values never satisfy strict <
assert has132_fast([1, 3, 2]) is True              # the minimal pattern
assert has132_fast([3, 2, 1]) is False             # strictly decreasing
assert has132_fast([1, 4, 2, 3]) is True and has132_fast([3, 4, 3, 3]) is False  # 3 is not < 3
assert has132_fast([-5, -1, -3]) is True           # negatives
assert has132_fast(list(range(200000))) is False   # increasing, max size
assert has132_fast(list(range(200000, 0, -1))) is False

# exhaustive over all sequences of length <= 6 on values 0..3, then seeded random
for n in range(0, 7):
    for t in itertools.product(range(4), repeat=n):
        assert has132_fast(list(t)) == has132_n3(list(t)), t
print("exhaustive: every sequence up to length 6 over values 0..3 agrees with the triple loop")
rng = random.Random(40)
hits = 0
for _ in range(3000):
    n = rng.randint(0, 12)
    a = [rng.randint(-5, 5) for _ in range(n)]
    r = has132_fast(a)
    assert r == has132_n2(a) == has132_n3(a), a
    hits += r
print(f"3000 seeded random arrays agree; {hits} contained a 132 pattern")
```

**Output (my run):**
```text
[1, 2, 3, 4] -> False
[3, 1, 4, 2] -> True
[-1, 3, 2, 0] -> True
exhaustive: every sequence up to length 6 over values 0..3 agrees with the triple loop
3000 seeded random arrays agree; 1663 contained a 132 pattern
```

The three prompt examples gave False, True, True as stated. The exhaustive check covers every sequence of length up to 6 over values 0..3 (including heavy duplicates) against the triple loop.

**Edge cases:**
- Fewer than 3 elements: False.
- All equal values: False, because the pattern needs strict inequalities.
- `[3,4,3,3]`: False (no value strictly between 3 and 4).
- Negative numbers and zero are ordinary.
- Strictly increasing or decreasing arrays of 200,000 elements: False.
- Initialise `third` to negative infinity, not 0, because the values can be negative.

**Follow-ups:**
- "Can you do it with a prefix-minimum array instead?" Yes: precompute the minimum before each j, then use the stack to test the '2'. The right-to-left version needs no extra array.
- "Return the indices?" Track the index of `third` and of the '3' that popped it, then search left for the '1'.
- "What about 123 or 321 patterns?" Those are easier (increasing or decreasing triples via patience-like tracking).

**Common mistakes:**
- Scanning from the left and forgetting which role a value plays.
- Using `<=` instead of `<` when comparing with `third`.
- Wrapping `third = max(third, popped)` is unnecessary: popped values only ever increase over the scan, because everything left on the stack is at least as large as the element that just popped. Plain assignment is correct.
- Initialising `third` to 0 and wrongly rejecting negatives.

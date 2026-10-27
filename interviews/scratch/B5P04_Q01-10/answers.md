### Q1 ⭐⭐⭐ 🟢 Valid parentheses. `s` contains only the characters ()[]{} (1 <= len <= 10^4). Return True if every opener is closed by the same type of bracket and in the correct nesting order. Push openers on a stack, and on each closer check that the top is its partner; say what the two failure modes are (closer on an empty stack, openers left over at the end) and why a bare counter works for one bracket type but not for three. Example: '()[]{}' -> True; '(]' -> False; '([{}])' -> True; '((' -> False; ']' -> False; '([)]' -> False.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Indian campus and IT-services style prep (a Naukri campus TCS fresher list that asks stack versus queue and LIFO versus FIFO; generic list, snippet only, not opened; no company attribution for any specific problem)

**Pattern:** Stack for nesting (last opened, first closed). The most recent unmatched opener must be the first one a closer meets. That is LIFO.

**Say this first (1 line):** "Push every opener; on a closer, the top must be its partner, otherwise return False; at the end the stack must be empty."

**Brute force:** Keep deleting adjacent matched pairs `()`, `[]`, `{}` until the string stops changing. Valid iff the result is empty. Each pass is O(n) and there can be O(n) passes, so O(n^2). I use it as the checker.

**Optimal:** One pass with a list used as a stack.
- Opener: push it.
- Closer: if the stack is empty, or the top is not its partner, return False. Otherwise pop.
- End: return `not stack`.
- Invariant: the stack holds exactly the openers that are still unmatched, oldest at the bottom. A closer can only legally match the newest one.
- Two failure modes: (1) closer arrives and the stack is empty (or top is the wrong type): `']'`, `'(]'`. (2) the loop ends with openers left over: `'(('`.
- Why a counter fails: with one bracket type, "how many are open" is the whole state. With three types the state is the sequence of open types, because the order decides which closer is legal. A counter says `'([)]'` is balanced (it is not), since it cannot tell which bracket is on top.

**Complexity:** Time O(n): each character is pushed at most once and popped at most once. Space O(n) worst case (all openers). The stack is a Python list, so `append` and `pop()` are amortised O(1).

**Dry run:** `'([)]'`
| char | action | stack after |
|---|---|---|
| `(` | push | `(` |
| `[` | push | `( [` |
| `)` | top is `[`, partner of `)` is `(`: mismatch | return False |

And `'([{}])'`: push `(`, `[`, `{`; `}` pops `{`; `]` pops `[`; `)` pops `(`; stack empty, True.

**Code:**
```python
import itertools
import random

PAIR = {")": "(", "]": "[", "}": "{"}


def valid_brute(s):
    # keep deleting adjacent matched pairs; valid iff nothing is left
    prev = None
    while prev != s:
        prev = s
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""


def valid_stack(s):
    stack = []
    for ch in s:
        if ch in PAIR:                       # a closer
            if not stack or stack[-1] != PAIR[ch]:
                return False                 # failure mode 1: empty stack or wrong partner
            stack.pop()
        else:
            stack.append(ch)                 # an opener
    return not stack                         # failure mode 2: openers left over


def valid_counter(s):
    # the tempting but wrong version: one counter for all three types
    c = 0
    for ch in s:
        c += 1 if ch in "([{" else -1
        if c < 0:
            return False
    return c == 0


examples = [("()[]{}", True), ("(]", False), ("([{}])", True),
            ("((", False), ("]", False), ("([)]", False)]
for s, want in examples:
    assert valid_brute(s) == valid_stack(s) == want, s
    print(repr(s), "->", valid_stack(s))

# why a counter is not enough
print("counter says '([)]' is", valid_counter("([)]"), "but stack says", valid_stack("([)]"))
assert valid_counter("([)]") is True and valid_stack("([)]") is False

# edge cases
assert valid_stack("") is True               # not in the prompt's range, but the natural base case
assert valid_stack("(" * 5000 + ")" * 5000)   # deep nesting is fine: explicit stack, no recursion
assert not valid_stack("(" * 5000 + ")" * 4999)
assert not valid_stack("}{")                 # counter-style balance but wrong order
assert not valid_stack(")(")

# exhaustive check: every string over the 6 characters up to length 7
total = 0
for n in range(0, 8):
    for tup in itertools.product("()[]{}", repeat=n):
        s = "".join(tup)
        assert valid_stack(s) == valid_brute(s), s
        total += 1
print("exhaustive check passed:", total, "strings (length 0..7)")

# seeded random longer strings, biased towards valid ones by building from pairs
rng = random.Random(5)
valid_seen = 0
for _ in range(2000):
    parts = []
    for _ in range(rng.randint(1, 8)):
        o, c = rng.choice(["()", "[]", "{}"])
        parts.append((o, c))
    s = "".join(o for o, _ in parts) + "".join(c for _, c in reversed(parts))
    if rng.random() < 0.5:                   # corrupt half of them
        i = rng.randrange(len(s))
        s = s[:i] + rng.choice("()[]{}") + s[i + 1:]
    assert valid_stack(s) == valid_brute(s), s
    valid_seen += valid_stack(s)
print("random check passed: 2000 cases,", valid_seen, "valid")
```

**Output (my run):**
```
'()[]{}' -> True
'(]' -> False
'([{}])' -> True
'((' -> False
']' -> False
'([)]' -> False
counter says '([)]' is True but stack says False
exhaustive check passed: 335923 strings (length 0..7)
random check passed: 2000 cases, 1153 valid
```
All six examples in the prompt are correct. The exhaustive check covers every string over the six characters up to length 7.

**Edge cases:**
- Single closer `']'` or `')('`: closer on an empty stack, False.
- Odd length: can never be valid (you can short-circuit with `len(s) % 2`).
- Openers left over `'(('`: caught by the final `not stack`.
- Deep nesting (10^4 characters): fine, the stack is a list on the heap, no recursion.
- Empty string: outside the stated range, but the code returns True. Say that out loud.

**Follow-ups:**
- *Return the index of the first error?* Push indices with the characters; on failure report the closer index, or the index left at the bottom.
- *Only one bracket type?* A counter is enough, and O(1) space.
- *Other characters mixed in (a code line)?* Skip anything that is not a bracket.

**Common mistakes:**
- Popping before checking the stack is empty (IndexError).
- Forgetting the final empty-stack check.
- Using a counter for several bracket types.
- Comparing the closer with the opener directly instead of through a partner map.

### Q2 ⭐⭐⭐ 🟢 Min stack. Design a stack with `push(x)`, `pop()`, `top()` and `getMin()`, all O(1); `pop` and `top` are never called on an empty stack. Give the version that keeps a parallel stack of running minimums, then the follow-up that stores only one extra stack entry when a new minimum arrives (or a single stack of differences) and say what breaks if duplicates of the minimum are not handled. Example: push(-2), push(0), push(-3), getMin() -> -3, pop(), top() -> 0, getMin() -> -2; then push(-2), push(-2), pop(), getMin() -> -2.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports

**Pattern:** Stack with a companion that remembers history. The minimum of a stack only changes when you push or pop, so you can store "the minimum so far" next to each element.

**Say this first (1 line):** "Each element remembers the minimum at the time it was pushed, so popping automatically restores the previous minimum."

**Brute force:** A plain list with `min(list)` in `getMin`. O(n) per `getMin`. I use it as the checker.

**Optimal:** Three versions, all O(1) per operation.
- **Parallel stack:** `mins[i]` is the minimum of everything up to position `i`. Push `min(x, mins[-1])`, pop both. `getMin` reads `mins[-1]`. Extra space O(n) always.
- **Sparse second stack:** push onto `mins` only when `x <= mins[-1]`. On `pop`, if the popped value equals `mins[-1]`, pop `mins` too. Extra space is only as big as the number of record-lows.
- **One stack of differences:** store `x - current_min`. A negative entry means "this push made a new minimum". On pop of a negative entry, the previous minimum is `min - entry`. `top` is `min` if the entry is negative, else `min + entry`. Python ints do not overflow, so differences are safe here (in a fixed-width language the difference can overflow; say so).
- Duplicates: with `<` instead of `<=` the second `2` is never recorded, so popping it removes the only copy of the minimum. The code below shows the real failure.
- Invariant: `mins[-1]` (or the variable `min`) always equals the minimum of the elements currently in the stack.

**Complexity:** Every operation is O(1) (list append and pop at the end). Space: parallel O(n) extra, sparse O(k) extra for k record-lows (still O(n) worst case, for a decreasing sequence), differences O(1) extra beyond the one stack.

**Dry run:** parallel stack, push(-2), push(0), push(-3):
| op | a | mins | getMin |
|---|---|---|---|
| push -2 | [-2] | [-2] | -2 |
| push 0 | [-2, 0] | [-2, -2] | -2 |
| push -3 | [-2, 0, -3] | [-2, -2, -3] | -3 |
| pop | [-2, 0] | [-2, -2] | -2 |
`top()` is 0, `getMin()` is -2, as in the prompt.

**Code:**
```python
import random


class BruteMinStack:
    """Reference: a plain list, getMin scans (O(n))."""
    def __init__(self): self.a = []
    def push(self, x): self.a.append(x)
    def pop(self): self.a.pop()
    def top(self): return self.a[-1]
    def getMin(self): return min(self.a)


class MinStack:
    """Parallel stack: mins[i] is the minimum of a[0..i]. O(1) all, O(n) extra."""
    def __init__(self):
        self.a, self.mins = [], []
    def push(self, x):
        self.a.append(x)
        self.mins.append(x if not self.mins else min(x, self.mins[-1]))
    def pop(self):
        self.a.pop(); self.mins.pop()
    def top(self): return self.a[-1]
    def getMin(self): return self.mins[-1]


class MinStackSparse:
    """Second stack only grows when x <= current min (the <= matters for duplicates)."""
    def __init__(self):
        self.a, self.mins = [], []
    def push(self, x):
        self.a.append(x)
        if not self.mins or x <= self.mins[-1]:
            self.mins.append(x)
    def pop(self):
        if self.a.pop() == self.mins[-1]:
            self.mins.pop()
    def top(self): return self.a[-1]
    def getMin(self): return self.mins[-1]


class MinStackBuggy(MinStackSparse):
    """Same idea with '<' : duplicates of the minimum are not recorded."""
    def push(self, x):
        self.a.append(x)
        if not self.mins or x < self.mins[-1]:
            self.mins.append(x)


class MinStackDiff:
    """One stack of differences x - min_before_push; one variable for the min."""
    def __init__(self):
        self.d, self.m = [], None
    def push(self, x):
        if not self.d:
            self.d.append(0); self.m = x
        else:
            self.d.append(x - self.m)
            if x < self.m:
                self.m = x                    # negative entry marks "new minimum"
    def pop(self):
        diff = self.d.pop()
        if diff < 0:
            self.m -= diff                    # restore the previous minimum
    def top(self):
        diff = self.d[-1]
        return self.m if diff < 0 else self.m + diff
    def getMin(self): return self.m


IMPLS = [MinStack, MinStackSparse, MinStackDiff]

# prompt example
for cls in IMPLS:
    s = cls()
    s.push(-2); s.push(0); s.push(-3)
    assert s.getMin() == -3
    s.pop()
    assert s.top() == 0 and s.getMin() == -2
    s.push(-2); s.push(-2); s.pop()
    assert s.getMin() == -2
print("prompt example passes for", [c.__name__ for c in IMPLS])

# what breaks without duplicate handling
b = MinStackBuggy()
b.push(2); b.push(2); b.pop()
print("buggy ('<') after push 2, push 2, pop: stack holds", b.a, "but mins =", b.mins)
try:
    b.getMin()
except IndexError:
    print("getMin() raised IndexError although 2 is still in the stack")

# edge cases
for cls in IMPLS:
    s = cls()
    s.push(7)
    assert s.top() == 7 and s.getMin() == 7
    s.pop()
    s.push(5); s.push(5); s.push(5)
    s.pop(); s.pop()
    assert s.getMin() == 5 and s.top() == 5          # all equal
    s.push(-2**31); s.push(2**31 - 1)
    assert s.getMin() == -2**31 and s.top() == 2**31 - 1
    s.pop()
    assert s.top() == -2**31

# seeded randomised cross-check against the brute force
rng = random.Random(42)
checked = 0
for _ in range(500):
    impls = [BruteMinStack()] + [c() for c in IMPLS]
    size = 0
    for _ in range(rng.randint(1, 40)):
        if size and rng.random() < 0.4:
            for s in impls: s.pop()
            size -= 1
        else:
            x = rng.randint(-4, 4)               # small range -> many duplicates
            for s in impls: s.push(x)
            size += 1
        if size:
            ref = impls[0]
            for s in impls[1:]:
                assert s.top() == ref.top() and s.getMin() == ref.getMin()
            checked += 1
print("random cross-check passed:", checked, "state checks")
```

**Output (my run):**
```
prompt example passes for ['MinStack', 'MinStackSparse', 'MinStackDiff']
buggy ('<') after push 2, push 2, pop: stack holds [2] but mins = []
getMin() raised IndexError although 2 is still in the stack
random cross-check passed: 9874 state checks
```
The prompt example is correct for all three versions.

**Edge cases:**
- One element: `top` and `getMin` are that element.
- All equal values: `<=` (or the parallel stack) keeps the minimum correct through pops.
- Extreme values: with Python ints the difference trick cannot overflow; in C++ or Java use a wider type.
- Popping to empty and pushing again must reset state (the difference version handles the empty case with a 0 entry).

**Follow-ups:**
- *Max stack too?* Same trick with `max`. If it also needs `popMax`, a plain stack is not enough; the max-stack question later in this part covers that.
- *Why not a heap for getMin?* Pop of an arbitrary element is O(log n) with lazy deletion, and it is overkill when removals are always LIFO.
- *Thread safety?* None here; add a lock if shared.

**Common mistakes:**
- Using `<` rather than `<=` in the sparse version.
- Storing only one variable `min` and recomputing it after pop (O(n)).
- In the difference version, forgetting that `top()` needs the decode, or restoring the minimum with the wrong sign.
- Calling `getMin` on an empty stack (the prompt rules it out; mention it).

### Q3 ⭐⭐⭐ 🟢 Implement a queue using two stacks. Support `push(x)`, `pop()`, `peek()` and `empty()` using only stack operations (append and pop at one end, peek at the top, size, is-empty). Use an input stack and an output stack that is refilled only when empty, and prove that `pop` is amortised O(1) even though one call can cost O(n) (every element moves at most once). Example: push(1), push(2), peek() -> 1, pop() -> 1, empty() -> False, pop() -> 2, empty() -> True.
**Asked at:** Candidate-reported Amazon rounds (a Glassdoor review naming stack-using-queues, a Naukri Code360 Amazon entry naming stack with two queues, a PracHub report naming queue with two stacks; snippets only, not opened; candidate-reported, unverified) | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Two stacks reverse the order twice, which gives FIFO. Amortised analysis: a rare expensive step paid for by many cheap ones.

**Say this first (1 line):** "Push onto an input stack; to pop or peek, if the output stack is empty, pour the whole input stack into it, then use the top of the output stack."

**Brute force:** On every `pop` or `peek`, pour everything from stack 1 into stack 2, read, then pour it all back. Each operation is O(n). It is correct and I use it as a checker.

**Optimal:** Keep two stacks, `inp` and `out`.
- `push(x)`: `inp.append(x)`, O(1).
- `pop` and `peek`: if `out` is empty, move every element of `inp` to `out` (this reverses them, so the oldest ends on top). Then use `out[-1]`.
- `empty`: both stacks are empty.
- Never pour while `out` is non-empty. Doing so would put newer elements under older ones and break the order.
- Invariant: `out` (top to bottom) followed by `inp` (bottom to top) is the queue from front to back.
- Amortised proof: an element moves from `inp` to `out` at most once, because it never goes back. So total moves over m operations is at most the number of pushes. Total cost O(m), so O(1) amortised per operation, even though one `pop` can cost O(n). (Potential argument: each push puts 1 coin on the element, which pays for its one future move.)

**Complexity:** `push` O(1). `pop` and `peek` O(n) worst case for a single call, O(1) amortised. `empty` O(1). Space O(n). Note the amortised bound is over a sequence of operations, not a guarantee for each call. For hard real-time use you would want a different structure.

**Dry run:** push(1), push(2), peek, pop, pop.
| op | inp | out | result |
|---|---|---|---|
| push 1 | [1] | [] | |
| push 2 | [1, 2] | [] | |
| peek | [] | [2, 1] | out is empty, pour: top is 1, returns 1 |
| pop | [] | [2] | returns 1 |
| empty | | | False |
| pop | [] | [] | returns 2 |
| empty | | | True |

**Code:**
```python
import random
from collections import deque


class BruteQueue:
    """Move everything to the second stack and back on every pop: O(n) each time."""
    def __init__(self): self.s1, self.s2 = [], []
    def push(self, x): self.s1.append(x)
    def _flip(self, src, dst):
        while src: dst.append(src.pop())
    def pop(self):
        self._flip(self.s1, self.s2)
        v = self.s2.pop()
        self._flip(self.s2, self.s1)
        return v
    def peek(self):
        self._flip(self.s1, self.s2)
        v = self.s2[-1]
        self._flip(self.s2, self.s1)
        return v
    def empty(self): return not self.s1


class MyQueue:
    """Input stack + output stack; refill output only when it is empty."""
    def __init__(self):
        self.inp, self.out = [], []
        self.moves = 0                          # instrumentation for the amortised proof
    def push(self, x): self.inp.append(x)
    def _fill(self):
        if not self.out:                        # the key condition
            while self.inp:
                self.out.append(self.inp.pop())
                self.moves += 1
    def pop(self):
        self._fill()
        return self.out.pop()
    def peek(self):
        self._fill()
        return self.out[-1]
    def empty(self): return not self.inp and not self.out


# prompt example
q = MyQueue()
q.push(1); q.push(2)
assert q.peek() == 1
assert q.pop() == 1
assert q.empty() is False
assert q.pop() == 2
assert q.empty() is True
print("prompt example passes")

# a single pop can be O(n) ...
q = MyQueue()
for i in range(1000): q.push(i)
q.pop()
print("first pop after 1000 pushes moved", q.moves, "elements")
# ... but total moves over a whole run never exceed the number of pushes
for i in range(999): q.pop()
print("after draining: total moves =", q.moves, "(pushes = 1000)")
assert q.moves == 1000

# interleaved push/pop: moves <= pushes always
rng = random.Random(3)
q, pushes = MyQueue(), 0
for _ in range(20000):
    if rng.random() < 0.55 or q.empty():
        q.push(pushes); pushes += 1
    else:
        q.pop()
    assert q.moves <= pushes
print("interleaved run: moves", q.moves, "<= pushes", pushes)

# edge cases
q = MyQueue()
assert q.empty()
q.push(9); assert q.peek() == 9 and q.pop() == 9 and q.empty()
q.push(1); q.push(2); q.pop(); q.push(3)       # push while output is non-empty
assert q.pop() == 2 and q.pop() == 3 and q.empty()
q.push(5); q.push(5)                            # duplicates
assert q.pop() == 5 and q.pop() == 5

# seeded randomised cross-check: MyQueue and BruteQueue vs collections.deque
rng = random.Random(7)
ops = 0
for _ in range(400):
    a, b, ref = MyQueue(), BruteQueue(), deque()
    for _ in range(rng.randint(1, 60)):
        r = rng.random()
        if r < 0.5 or not ref:
            x = rng.randint(-5, 5)
            a.push(x); b.push(x); ref.append(x)
        elif r < 0.7:
            assert a.peek() == b.peek() == ref[0]
        else:
            assert a.pop() == b.pop() == ref.popleft()
        assert a.empty() == b.empty() == (not ref)
        ops += 1
print("random cross-check passed:", ops, "operations")
```

**Output (my run):**
```
prompt example passes
first pop after 1000 pushes moved 1000 elements
after draining: total moves = 1000 (pushes = 1000)
interleaved run: moves 8972 <= pushes 11035
random cross-check passed: 11879 operations
```
The prompt example is correct. The counter shows the proof in action: the first pop after 1000 pushes moved 1000 elements, but over the whole run the total never exceeded the number of pushes.

**Edge cases:**
- `empty()` must check both stacks, not only `inp`.
- Push while `out` is non-empty: new elements go to `inp` and wait; the order stays right.
- Single element, duplicates: fine.
- A `peek` also triggers the pour (not only `pop`).

**Follow-ups:**
- *Is it worst-case O(1)?* No, only amortised. An adversary cannot repeat the O(n) step because after it `out` holds all the elements.
- *Stack using queues (the other direction)?* Use one queue: after `push(x)`, rotate the queue `len-1` times so `x` is at the front. Push is O(n), pop O(1). Or make pop the costly one.
- *Why does this show up in interviews?* It tests whether you can reason about amortised cost, not only write the code.

**Common mistakes:**
- Pouring on every operation (O(n) each).
- Pouring when `out` is not empty, which reverses the order.
- `empty()` that only looks at one stack.
- Calling `inp.pop(0)` or using a list as a queue; the whole point is to use only stack operations.

### Q4 ⭐⭐⭐ 🟢 Python list versus collections.deque as a stack and a queue. A queue of up to 2*10^5 integers is driven by commands 'push v' and 'pop' (pop returns the oldest value). Implement it with `list.pop(0)` and with `collections.deque.popleft`, state the cost of each (list `pop(0)` shifts every remaining element, so O(n); `deque` is O(1) at both ends but O(n) for indexing into the middle), say why a plain list is a perfectly good stack (`append` and `pop()` at the end are amortised O(1)), and when `deque(maxlen=k)` is useful. Any timing you quote is sandbox-only evidence, not proof of big-O. Example: commands ['push 1','push 2','pop','push 3','pop','pop'] -> [1, 2, 3].
**Asked at:** Python container docs and explainers (docs.python.org collections mirror saying list pop(0) and insert(0, v) cost O(n) and deque gives O(1) at both ends, Real Python deque article, dev.to deque-versus-list timing post; snippets only, not opened; the queue module docs were NOT found, so queue.Queue claims rest on editor knowledge plus the sandbox run) | Indian campus and IT-services style prep (a Naukri campus TCS fresher list that asks stack versus queue and LIFO versus FIFO; generic list, snippet only, not opened; no company attribution for any specific problem)

**Pattern:** Choosing the right container. A stack needs fast operations at one end. A queue needs fast operations at both ends (add at the back, remove at the front).

**Say this first (1 line):** "A list is a fine stack, but a bad queue because `pop(0)` shifts every element; use `collections.deque` for queues."

**Brute force:** Queue as a list: `append` to push, `pop(0)` to pop. Correct, but each `pop(0)` moves all remaining elements left, so it is O(n) and the whole run is O(n^2) for n pops.

**Optimal:** `deque.popleft()` is O(1). A deque is a linked list of fixed-size blocks, so both ends are cheap.
- List as a stack: `append` and `pop()` at the end are amortised O(1) (the array occasionally resizes). `st[-1]` is the peek.
- Deque as a queue: `append` and `popleft`. Both O(1).
- The catch: indexing into the middle of a deque, `d[i]`, is O(n) (it walks blocks). A list gives O(1) indexing. Pick by what you need.
- `deque(maxlen=k)` keeps only the last `k` items; when full, appending on one side silently drops from the other side. Use it for "last k events", a rolling window, or a bounded history. It is not a blocking queue and raises nothing when full.
- Invariant for the queue: items leave in the order they arrived.

**Complexity:** List queue: n pushes O(n), n pops O(n^2) worst case (each `pop(0)` O(remaining)). Deque queue: O(n) total. Space O(n) for both. The timings below are sandbox-only evidence on one machine, not proof of big-O; the proof is the shifting of memory in `pop(0)`. A useful sign in the output: when n doubles, the list time roughly quadruples while the deque time roughly doubles.

**Dry run:** commands `push 1, push 2, pop, push 3, pop, pop` with a deque.
| command | deque after | output so far |
|---|---|---|
| push 1 | [1] | |
| push 2 | [1, 2] | |
| pop | [2] | 1 |
| push 3 | [2, 3] | |
| pop | [3] | 1, 2 |
| pop | [] | 1, 2, 3 |

**Code:**
```python
import random
import sys
import time
from collections import deque


def run_list(cmds):
    q, out = [], []
    for c in cmds:
        if c.startswith("push"):
            q.append(int(c[5:]))
        else:
            out.append(q.pop(0))                 # O(n): shifts every remaining element
    return out


def run_deque(cmds):
    q, out = deque(), []
    for c in cmds:
        if c.startswith("push"):
            q.append(int(c[5:]))
        else:
            out.append(q.popleft())              # O(1)
    return out


def run_brute(cmds):
    # independent reference: remember all pushes and a read pointer
    pushed, head, out = [], 0, []
    for c in cmds:
        if c.startswith("push"):
            pushed.append(int(c.split()[1]))
        else:
            out.append(pushed[head]); head += 1
    return out


ex = ["push 1", "push 2", "pop", "push 3", "pop", "pop"]
assert run_list(ex) == run_deque(ex) == run_brute(ex) == [1, 2, 3]
print("prompt example ->", run_deque(ex))

# list as a stack: append/pop at the END are amortised O(1)
st = []
st.append(1); st.append(2); st.append(3)
assert st.pop() == 3 and st[-1] == 2
print("list as stack: top is st[-1], pop() returns the newest")

# deque(maxlen=k): a sliding window of the last k items, old ones fall off the left
w = deque(maxlen=3)
for v in range(1, 7):
    w.append(v)
assert list(w) == [4, 5, 6] and w.maxlen == 3
print("deque(maxlen=3) after appending 1..6 ->", list(w))

# seeded randomised cross-check of the three implementations
rng = random.Random(2024)
for _ in range(500):
    cmds, size = [], 0
    for _ in range(rng.randint(0, 30)):
        if size and rng.random() < 0.45:
            cmds.append("pop"); size -= 1
        else:
            cmds.append(f"push {rng.randint(-9, 9)}"); size += 1
    assert run_list(cmds) == run_deque(cmds) == run_brute(cmds)
assert run_deque([]) == [] and run_list(["push 5", "pop"]) == [5]   # edge cases
print("random cross-check passed: 500 command lists")


# sandbox-only timing: N pushes then N pops
def timed(fn, cmds):
    t = time.perf_counter(); fn(cmds); return time.perf_counter() - t


print("Python", sys.version.split()[0])
for n in (25_000, 50_000, 100_000, 200_000):
    cmds = [f"push {i}" for i in range(n)] + ["pop"] * n
    tl, td = timed(run_list, cmds), timed(run_deque, cmds)
    print(f"n={n:>7}: list.pop(0) {tl:7.3f}s   deque.popleft {td:7.3f}s")

# indexing into the middle of a deque is O(n); a list is O(1)
big_l = list(range(200_000)); big_d = deque(big_l)
t = time.perf_counter()
for _ in range(2000): big_l[100_000]
tl = time.perf_counter() - t
t = time.perf_counter()
for _ in range(2000): big_d[100_000]
td = time.perf_counter() - t
print(f"2000 middle lookups of 200000 items: list {tl:.4f}s   deque {td:.4f}s")
```

**Output (my run):**
```
prompt example -> [1, 2, 3]
list as stack: top is st[-1], pop() returns the newest
deque(maxlen=3) after appending 1..6 -> [4, 5, 6]
random cross-check passed: 500 command lists
Python 3.13.17
n=  25000: list.pop(0)   0.047s   deque.popleft   0.003s
n=  50000: list.pop(0)   0.202s   deque.popleft   0.008s
n= 100000: list.pop(0)   0.796s   deque.popleft   0.013s
n= 200000: list.pop(0)   2.999s   deque.popleft   0.025s
2000 middle lookups of 200000 items: list 0.0001s   deque 0.0049s
```
Observed on Python 3.13 in this sandbox. The timing lines will differ on another machine and from run to run, but at 200000 items the list version was far slower than the deque version, and the gap widened as n grew. The prompt example is correct.

**Edge cases:**
- Pop from an empty list: `IndexError: pop from empty list`. Same for `deque.popleft()` ("pop from an empty deque"). The prompt rules this out.
- Small n: the list is fine and sometimes faster, because `pop(0)` on a few items is a tiny memmove. The problem only shows at scale.
- `deque(maxlen=k)` with `maxlen=0` discards every append.
- Do not index a deque in a hot loop.

**Follow-ups:**
- *Why is `list.append` O(1) amortised, not worst-case?* The array over-allocates; an occasional append copies everything, but the cost spreads over many appends.
- *`queue.Queue` or `deque`?* `queue.Queue` is for threads: it has locking, a blocking `get`, `maxsize`, and `task_done`/`join`. That makes every operation slower. In single-threaded code use `deque`. (Named from editor knowledge, not from a page I opened.)
- *Can I fake a queue with a list and a head index?* Yes: keep an integer `head` and never delete. It is O(1) per operation, but memory is not freed until you slice, so deque is cleaner.

**Common mistakes:**
- Using `list.pop(0)` or `list.insert(0, x)` in a BFS loop and calling it O(1).
- Saying deque is better in every way; middle indexing is slower.
- Using `maxlen` and expecting an exception when it is full.
- Quoting timings as proof of complexity.

### Q5 ⭐⭐⭐ 🟢 Next greater element, subset version. `nums1` is a subset of `nums2` and both have distinct integers (len <= 1000 and 10^4 respectively). For each x in `nums1` return the first element to the right of x inside `nums2` that is larger than x, or -1. Scan `nums2` once with a decreasing stack and record each popped element's answer in a dict. Example: nums1=[4,1,2], nums2=[1,3,4,2] -> [-1,3,-1]; nums1=[2,4], nums2=[1,2,3,4] -> [3,-1].
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Monotonic stack (decreasing) plus a dictionary. "First larger element to the right" is the textbook use. Each element waits on the stack until something bigger arrives.

**Say this first (1 line):** "Scan `nums2` once; keep a stack of values that are still waiting for a bigger one; when `y` arrives, every smaller value on top gets `y` as its answer."

**Brute force:** For each `x` in `nums1`, find it in `nums2` (`index`, O(m)), then scan right until a larger value. Worst case O(n * m) for n = len(nums1), m = len(nums2); with n and m up to 10^3 and 10^4 that is about 10^7 steps. It is my checker.

**Optimal:**
- Scan `nums2` left to right with a stack kept in decreasing order from bottom to top.
- For each `y`: while the top is smaller than `y`, pop it and record `next[top] = y`. Then push `y`.
- Everything left at the end has no greater element on its right: answer -1 (use `dict.get(x, -1)`).
- The values are distinct, so a dict keyed by value is safe. With duplicates you would key by index.
- Invariant: the stack always holds, in decreasing order, exactly the elements seen so far that have not met a larger element. The first `y` that beats a value is, by scan order, the first greater element to its right.
- Then answer each query in `nums1` with one dict lookup.

**Complexity:** Time O(n + m): every element of `nums2` is pushed once and popped at most once, and each query is O(1). Space O(m) for the stack and dict. The inner `while` does not make it quadratic because of that push-once, pop-once count.

**Dry run:** `nums2 = [1, 3, 4, 2]`.
| y | pops (and recorded answer) | stack after |
|---|---|---|
| 1 | none | [1] |
| 3 | pop 1, next[1] = 3 | [3] |
| 4 | pop 3, next[3] = 4 | [4] |
| 2 | none (top 4 is not smaller) | [4, 2] |
Leftover 4 and 2 have no answer. Queries `[4, 1, 2]` give `[-1, 3, -1]`.

**Code:**
```python
import random


def nge_brute(nums1, nums2):
    res = []
    for x in nums1:
        i = nums2.index(x)
        ans = -1
        for y in nums2[i + 1:]:
            if y > x:
                ans = y
                break
        res.append(ans)
    return res


def nge_stack(nums1, nums2):
    nxt = {}                                  # value -> next greater value
    stack = []                                # decreasing values, waiting for a bigger one
    for y in nums2:
        while stack and stack[-1] < y:
            nxt[stack.pop()] = y              # y is the first greater element to the right
        stack.append(y)
    # whatever is left on the stack has no greater element: default -1
    return [nxt.get(x, -1) for x in nums1]


assert nge_stack([4, 1, 2], [1, 3, 4, 2]) == nge_brute([4, 1, 2], [1, 3, 4, 2]) == [-1, 3, -1]
assert nge_stack([2, 4], [1, 2, 3, 4]) == nge_brute([2, 4], [1, 2, 3, 4]) == [3, -1]
print("[4,1,2] in [1,3,4,2] ->", nge_stack([4, 1, 2], [1, 3, 4, 2]))
print("[2,4] in [1,2,3,4] ->", nge_stack([2, 4], [1, 2, 3, 4]))

# edge cases
assert nge_stack([1], [1]) == [-1]                       # single element
assert nge_stack([5, 4, 3], [5, 4, 3]) == [-1, -1, -1]   # decreasing: nothing greater
assert nge_stack([1, 2, 3], [1, 2, 3]) == [2, 3, -1]     # increasing
assert nge_stack([], [1, 2]) == []                       # empty nums1 (outside the limits, harmless)
assert nge_stack([-3, -1], [-3, -2, -1]) == [-2, -1]  # negatives
big = list(range(10_000, 0, -1)) + [10_001]
assert nge_stack([10_000, 1], big) == [10_001, 10_001]   # one big pop cascade (n = 10^4)

# seeded randomised cross-check
rng = random.Random(8)
for _ in range(1000):
    n = rng.randint(1, 9)
    nums2 = rng.sample(range(-10, 20), n)                # distinct values
    nums1 = rng.sample(nums2, rng.randint(1, n))
    assert nge_stack(nums1, nums2) == nge_brute(nums1, nums2), (nums1, nums2)
print("random cross-check passed: 1000 cases")
```

**Output (my run):**
```
[4,1,2] in [1,3,4,2] -> [-1, 3, -1]
[2,4] in [1,2,3,4] -> [3, -1]
random cross-check passed: 1000 cases
```
Both prompt examples are correct.

**Edge cases:**
- A decreasing array: nothing is ever popped, all answers are -1.
- An increasing array: each element is popped by the next one.
- One big element at the end pops a whole stack at once (still amortised O(1) each).
- Single element: answer -1.
- Negatives are fine; only comparisons are used.

**Follow-ups:**
- *Duplicates in `nums2`?* Key by index, not value, and use strict `<` to pop (so equal values do not pop each other).
- *Next smaller element?* Flip the comparison.
- *Circular array?* The circular-array question later in this part does it with two laps.

**Common mistakes:**
- Using `<=` when popping: for distinct values harmless, but it gives wrong answers once duplicates exist.
- Forgetting the default -1 for values left on the stack.
- Scanning `nums1` instead of `nums2` with the stack (the order that matters is `nums2`).
- Calling the nested loop O(n^2) without noticing each element is popped at most once.

### Q6 ⭐⭐⭐ 🟡 Evaluate reverse Polish notation. `tokens` is a valid postfix expression whose tokens are integer strings (possibly negative, like '-11') and the operators + - * /; division truncates toward zero, there are no division-by-zero cases and results fit in 32 bits. Use an operand stack, and state why the second popped value is the left operand and why `a // b` is wrong for negatives in Python (floor, not truncation; use `int(a / b)` or an explicit sign fix). Example: ['2','1','+','3','*'] -> 9; ['4','13','5','/','+'] -> 6; ['10','6','9','3','+','-11','*','/','*','17','+','5','+'] -> 22; ['7','-2','/'] -> -3.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Operand stack. Postfix notation puts operators after their operands, so a stack evaluates it in one pass with no parentheses and no precedence rules.

**Say this first (1 line):** "Push numbers; on an operator pop two, apply, push the result. The first value popped is the right operand, the second popped is the left."

**Brute force:** There is no natural slow version, since the stack method is already linear. My checker is a recursive evaluator that reads the token list from the end: the last token is the root operator, the next one it reads is the right subtree, then the left. It is also O(n), but the recursion depth can reach n, so it is not for large input. I do not use `eval` on a converted infix string (unsafe, and its division is floor division).

**Optimal:**
- Number token: push `int(token)`. A token like `'-11'` is a number, not the minus operator; test for the four operator strings exactly.
- Operator: `b = pop()` (the right operand, pushed last), then `a = pop()` (the left operand). Push `a op b`.
- Order matters for `-` and `/`: `['3','4','-']` means 3 - 4, so `a - b` with `a` the second popped.
- Division must truncate toward zero. Python's `//` floors: `7 // -2` is -4, but the answer is -3. Use `int(a / b)` (fine within 32-bit values, because floats carry 53 bits exactly) or a sign-aware integer version: `q = abs(a) // abs(b)` and negate if the signs differ. The code uses the second one and shows where `int(a / b)` would fail for huge integers.
- Invariant: after processing a prefix of the tokens, the stack holds the values of the completed sub-expressions, in order. A valid expression ends with exactly one value.

**Complexity:** Time O(n), each token is handled once and each op does O(1) work. Space O(n) worst case (all numbers first, then operators), at most about n/2 + 1 values on the stack.

**Dry run:** `['4','13','5','/','+']`.
| token | action | stack |
|---|---|---|
| 4 | push | [4] |
| 13 | push | [4, 13] |
| 5 | push | [4, 13, 5] |
| / | b = 5, a = 13, 13 / 5 truncates to 2 | [4, 2] |
| + | b = 2, a = 4, 4 + 2 | [6] |
Result 6.

**Code:**
```python
import random


def trunc_div(a, b):
    # truncate toward zero without floats (safe for big ints)
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def eval_rpn(tokens):
    st = []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = st.pop()                      # second popped = RIGHT operand
            a = st.pop()                      # first operand pushed = LEFT operand
            if t == "+": st.append(a + b)
            elif t == "-": st.append(a - b)
            elif t == "*": st.append(a * b)
            else: st.append(trunc_div(a, b))
        else:
            st.append(int(t))                 # int() handles '-11'
    return st[0]


# independent reference: build a tree-free recursive evaluator from the END of the list
def eval_ref(tokens):
    pos = [len(tokens) - 1]

    def go():
        t = tokens[pos[0]]
        pos[0] -= 1
        if t in "+-*/" and len(t) == 1:
            right = go()                      # the last operand comes first when reading backwards
            left = go()
            if t == "+": return left + right
            if t == "-": return left - right
            if t == "*": return left * right
            q = abs(left) // abs(right)
            return q if (left < 0) == (right < 0) else -q
        return int(t)
    return go()


examples = [
    (["2", "1", "+", "3", "*"], 9),
    (["4", "13", "5", "/", "+"], 6),
    (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], 22),
    (["7", "-2", "/"], -3),
]
for toks, want in examples:
    assert eval_rpn(toks) == eval_ref(toks) == want, toks
    print(toks, "->", eval_rpn(toks))

# the floor-division trap
print("7 // -2 =", 7 // -2, "  int(7 / -2) =", int(7 / -2), "  trunc_div(7, -2) =", trunc_div(7, -2))
print("-7 // 2 =", -7 // 2, "  int(-7 / 2) =", int(-7 / 2), "  trunc_div(-7, 2) =", trunc_div(-7, 2))
assert 7 // -2 == -4 and trunc_div(7, -2) == -3 and trunc_div(-7, 2) == -3

# int(a / b) is also unsafe beyond float precision (prompt promises 32-bit, so it is fine there)
big = 10**17 + 1
print("int(big / 1) =", int(big / 1), " trunc_div(big, 1) =", trunc_div(big, 1))
assert trunc_div(big, 1) == big and int(big / 1) != big

# edge cases
assert eval_rpn(["5"]) == 5                               # single operand
assert eval_rpn(["-11"]) == -11                           # a negative number is NOT an operator
assert eval_rpn(["3", "4", "-"]) == -1                    # operand order for '-'
assert eval_rpn(["1", "2", "/"]) == 0
assert eval_rpn(["-1", "2", "/"]) == 0                    # truncation toward zero, not -1
assert eval_rpn(["0", "3", "-"]) == -3

# seeded randomised cross-check: random expression trees -> RPN, compare with both evaluators
rng = random.Random(13)


def gen(depth):
    if depth == 0 or rng.random() < 0.3:
        return [str(rng.randint(-20, 20))]
    left, right = gen(depth - 1), gen(depth - 1)
    op = rng.choice("+-*/")
    return left + right + [op]


def safe(toks):
    # reject expressions that divide by zero (the prompt excludes them)
    st = []
    for t in toks:
        if t in ("+", "-", "*", "/"):
            b, a = st.pop(), st.pop()
            if t == "/" and b == 0:
                return False
            st.append({"+": a + b, "-": a - b, "*": a * b, "/": trunc_div(a, b) if b else 0}[t])
        else:
            st.append(int(t))
    return True


done = 0
while done < 1500:
    toks = gen(4)
    if not safe(toks):
        continue
    assert eval_rpn(toks) == eval_ref(toks), toks
    done += 1
print("random cross-check passed:", done, "expressions")
```

**Output (my run):**
```
['2', '1', '+', '3', '*'] -> 9
['4', '13', '5', '/', '+'] -> 6
['10', '6', '9', '3', '+', '-11', '*', '/', '*', '17', '+', '5', '+'] -> 22
['7', '-2', '/'] -> -3
7 // -2 = -4   int(7 / -2) = -3   trunc_div(7, -2) = -3
-7 // 2 = -4   int(-7 / 2) = -3   trunc_div(-7, 2) = -3
int(big / 1) = 100000000000000000  trunc_div(big, 1) = 100000000000000001
random cross-check passed: 1500 expressions
```
All four prompt examples are correct, including the floor-division trap `['7','-2','/']` which must be -3 (the output shows `7 // -2` is -4 in Python 3.13).

**Edge cases:**
- A single token like `['5']` or `['-11']`: answer is that number.
- Negative numbers: test the token against the four operators exactly; do not test `t[0] == '-'`.
- Truncation: `-1 / 2` is 0, not -1.
- Intermediate values can exceed 32 bits in other languages; Python ints do not overflow.
- Division by zero is excluded by the prompt; say you would raise or return an error otherwise.

**Follow-ups:**
- *Infix to postfix?* The shunting-yard algorithm: an operator stack with precedence. A later question in this part covers calculators.
- *Why no parentheses needed?* The order of tokens already encodes the evaluation order.
- *Validate the expression?* Track stack size: it must never go below 2 at an operator and must end at 1.

**Common mistakes:**
- Swapping the operands: `b - a` instead of `a - b`.
- Using `//` for division with negatives.
- Treating `'-11'` as an operator, or using `isdigit()` (it is False for `'-11'`).
- Using `eval` on the joined string.

### Q7 ⭐⭐⭐ 🟡 Daily temperatures. Given `temps` (1 <= len <= 10^5, integers), return a list where `ans[i]` is the number of days after day i until a strictly warmer day, or 0 if none. Keep a stack of indices of days still waiting for a warmer day (temperatures non-increasing down the stack) and resolve them as a warmer day arrives; show why each index is pushed and popped once (O(n)) and the right-to-left jump-pointer alternative. Example: [73,74,75,71,69,72,76,73] -> [1,1,4,2,1,1,0,0]; [30,40,50,60] -> [1,1,1,0]; [30,60,90] -> [1,1,0].
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Monotonic stack of indices (non-increasing temperatures). It answers "next strictly greater element to the right" and also needs the distance, so store indices, not values.

**Say this first (1 line):** "Keep a stack of days still waiting for a warmer day; when today is warmer than the top, pop it and its answer is today's index minus its index."

**Brute force:** For each day, scan right until a warmer day. O(n^2) worst case (a decreasing array). With n = 10^5 that is about 5 * 10^9 steps, too slow. It is my checker.

**Optimal:**
- Stack holds indices of days with no warmer day found yet. Their temperatures are non-increasing from bottom to top.
- For each day `i`: while the top day `j` has `temps[j] < temps[i]`, pop it and set `ans[j] = i - j`. Then push `i`.
- Use strict `<`: an equal temperature is not warmer, so equal days stay on the stack together.
- Days left on the stack at the end keep the default 0.
- Why O(n): each index is pushed exactly once and popped at most once. The inner `while` loop total is bounded by n, so the double loop is not O(n^2).
- **Right-to-left jump pointers (alternative, O(1) extra space beyond the answer):** for day `i`, start at `j = i + 1`. While `temps[j] <= temps[i]`, jump by `ans[j]` (day `j`'s own next warmer day; every day between `j` and there is not warmer than `j`, so not warmer than `i` either). If `ans[j]` is 0, there is no warmer day at all. This is the same chain the stack would hold, followed implicitly, so it is also O(n) amortised.

**Complexity:** Stack version: time O(n), space O(n) for the stack (worst case a non-increasing array) plus the output. Jump version: time O(n) amortised, extra space O(1) beyond the output.

**Dry run:** `[73, 74, 75, 71, 69, 72, 76, 73]`.
| i | temp | pops (answer) | stack (indices) |
|---|---|---|---|
| 0 | 73 | | [0] |
| 1 | 74 | pop 0, ans[0] = 1 | [1] |
| 2 | 75 | pop 1, ans[1] = 1 | [2] |
| 3 | 71 | | [2, 3] |
| 4 | 69 | | [2, 3, 4] |
| 5 | 72 | pop 4 (ans 1), pop 3 (ans 2) | [2, 5] |
| 6 | 76 | pop 5 (ans 1), pop 2 (ans 4) | [6] |
| 7 | 73 | | [6, 7] |
Days 6 and 7 stay 0. Result `[1, 1, 4, 2, 1, 1, 0, 0]`.

**Code:**
```python
import random


def daily_brute(temps):
    n = len(temps)
    res = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if temps[j] > temps[i]:
                res[i] = j - i
                break
    return res


def daily_stack(temps):
    n = len(temps)
    res = [0] * n
    stack = []                                 # indices; temps[stack] is non-increasing bottom to top
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:  # strictly warmer: today answers these days
            j = stack.pop()
            res[j] = i - j
        stack.append(i)
    return res                                 # indices left on the stack keep 0


def daily_jump(temps):
    # right-to-left with jump pointers: follow answers instead of a stack
    n = len(temps)
    res = [0] * n
    for i in range(n - 2, -1, -1):
        j = i + 1
        while j < n and temps[j] <= temps[i]:
            if res[j] == 0:                    # j has no warmer day, so neither does i
                j = n
                break
            j += res[j]                        # jump straight to j's next warmer day
        if j < n:
            res[i] = j - i
    return res


examples = [([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
            ([30, 40, 50, 60], [1, 1, 1, 0]),
            ([30, 60, 90], [1, 1, 0])]
for temps, want in examples:
    assert daily_brute(temps) == daily_stack(temps) == daily_jump(temps) == want, temps
    print(temps, "->", daily_stack(temps))

# edge cases
assert daily_stack([50]) == [0]
assert daily_stack([50, 50, 50]) == [0, 0, 0]          # equal is NOT warmer
assert daily_stack([90, 80, 70]) == [0, 0, 0]          # strictly decreasing
assert daily_stack([-5, -3, -4, 0]) == [1, 2, 1, 0]    # negatives
n = 100_000
assert daily_stack(list(range(n))) == [1] * (n - 1) + [0]      # max size, all pushes and pops
assert daily_jump(list(range(n, 0, -1))) == [0] * n            # max size, nothing resolves

# seeded randomised cross-check (small range => many ties)
rng = random.Random(99)
for _ in range(1500):
    temps = [rng.randint(-3, 6) for _ in range(rng.randint(1, 14))]
    want = daily_brute(temps)
    assert daily_stack(temps) == want, temps
    assert daily_jump(temps) == want, temps
print("random cross-check passed: 1500 cases")
```

**Output (my run):**
```
[73, 74, 75, 71, 69, 72, 76, 73] -> [1, 1, 4, 2, 1, 1, 0, 0]
[30, 40, 50, 60] -> [1, 1, 1, 0]
[30, 60, 90] -> [1, 1, 0]
random cross-check passed: 1500 cases
```
All three prompt examples are correct.

**Edge cases:**
- One day: `[0]`.
- All equal: all 0 (equal is not warmer).
- Strictly decreasing: all 0, stack grows to n.
- Strictly increasing: every answer 1 except the last, each element popped at once.
- Negative temperatures: only comparisons are used.
- Max size (10^5): iterative, no recursion needed.

**Follow-ups:**
- *Next warmer temperature value instead of distance?* Same loop, store `temps[i]`.
- *Previous warmer day?* Scan left to right, and the top of the stack after popping smaller-or-equal days is the answer.
- *Why store indices, not values?* The answer is a distance; the value is `temps[index]` anyway.

**Common mistakes:**
- Using `<=` when popping, which treats equal temperatures as warmer.
- Storing values instead of indices, then losing the distance.
- Forgetting that leftover indices must be 0 (initialise the result with zeros).
- Claiming O(n^2) because of the nested loop.

### Q8 ⭐⭐⭐ 🟡 Decode string. `s` is an encoded string made of lowercase letters, digits and brackets in the form k[text], where k (1..300) repeats the text, brackets may nest, and digits only appear as repeat counts; the decoded length is at most 10^5. Return the decoded string. Use a stack that saves (text so far, repeat count) at each '[' and restores it at ']'; also say how recursion would do it and where its depth limit bites. Example: '3[a]2[bc]' -> 'aaabcbc'; '3[a2[c]]' -> 'accaccacc'; '2[abc]3[cd]ef' -> 'abcabccdcdcdef'; 'ab10[c]' -> 'abcccccccccc'.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Stack of saved contexts. A bracket opens a new inner level; when it closes, you must go back to the outer level and remember what repeat count was waiting. That is nesting, so a stack.

**Say this first (1 line):** "At every `[`, push (text so far, repeat count) and start fresh; at every `]`, pop and append `inner * count` to the saved text."

**Brute force:** Use a regex to find an innermost `k[letters]` block (no brackets inside), expand it, and repeat until the string stops changing. Each round is O(length) and there are as many rounds as nesting levels. Correct, but it rescans the string every round. It is my checker.

**Optimal:**
- Walk the characters. Keep `cur` (list of pieces for the current level) and `k` (the number being read).
- Digit: `k = k * 10 + digit` (counts like `10` or `300` are several digits).
- `[`: push `(cur, k)`, then reset `cur = []`, `k = 0`.
- `]`: pop `(outer, times)`, append `''.join(cur) * times` to `outer`, and make `outer` the current level.
- Letter: append to `cur`.
- Invariant: the stack holds one saved frame per currently open bracket, and `cur` is the decoded text of the innermost open level.
- **Recursion version:** `parse()` reads until `]`, and calls itself at each `[`. It is shorter to write, but it uses one Python frame per nesting level. Python 3.13's default recursion limit is 1000 (observed below), so about 1000 levels of nesting raises `RecursionError`. With the explicit stack the depth lives on the heap and is bounded only by memory.

**Complexity:** Time O(L) in the output length L for typical inputs, since every output character is created once by a multiplication and joined. In a worst case such as a long block wrapped in many `1[...]` layers, each `]` copies the inner text again, giving O(L * d) for nesting depth d; say that if asked. Space O(L + d).

**Dry run:** `'3[a2[c]]'`.
| char | action | cur | stack | k |
|---|---|---|---|---|
| 3 | read count | [] | [] | 3 |
| [ | save ([], 3) | [] | [([],3)] | 0 |
| a | letter | [a] | [([],3)] | 0 |
| 2 | read count | [a] | same | 2 |
| [ | save ([a], 2) | [] | [([],3), ([a],2)] | 0 |
| c | letter | [c] | same | 0 |
| ] | pop ([a],2): [a, 'cc'] | [a, cc] | [([],3)] | 0 |
| ] | pop ([],3): ['acc' * 3] | [accaccacc] | [] | 0 |
Result `accaccacc`.

**Code:**
```python
import random
import re
import sys


def decode_brute(s):
    # repeatedly expand an innermost k[letters] block until none is left
    pat = re.compile(r"(\d+)\[([a-z]*)\]")
    while True:
        new = pat.sub(lambda m: m.group(2) * int(m.group(1)), s)
        if new == s:
            return s
        s = new


def decode_stack(s):
    stack = []                       # saved (text so far, repeat count) pairs
    cur, k = [], 0                   # text of the current level, number being read
    for ch in s:
        if ch.isdigit():
            k = k * 10 + int(ch)     # counts can have several digits
        elif ch == "[":
            stack.append((cur, k))   # save the outer level
            cur, k = [], 0
        elif ch == "]":
            outer, times = stack.pop()
            outer.append("".join(cur) * times)
            cur = outer              # restore the outer level
        else:
            cur.append(ch)
    return "".join(cur)


def decode_rec(s):
    i = 0

    def parse():                     # parse until ']' or the end
        nonlocal i
        out, k = [], 0
        while i < len(s):
            ch = s[i]
            if ch.isdigit():
                k = k * 10 + int(ch); i += 1
            elif ch == "[":
                i += 1
                out.append(parse() * k)   # recursion: one frame per nesting level
                k = 0
            elif ch == "]":
                i += 1
                return "".join(out)
            else:
                out.append(ch); i += 1
        return "".join(out)
    return parse()


examples = [("3[a]2[bc]", "aaabcbc"), ("3[a2[c]]", "accaccacc"),
            ("2[abc]3[cd]ef", "abcabccdcdcdef"), ("ab10[c]", "abcccccccccc")]
for s, want in examples:
    assert decode_brute(s) == decode_stack(s) == decode_rec(s) == want, s
    print(repr(s), "->", repr(decode_stack(s)))

# edge cases
assert decode_stack("abc") == "abc"                    # no brackets
assert decode_stack("1[a]") == "a"
assert decode_stack("300[a]") == "a" * 300             # multi-digit count
assert decode_stack("2[2[2[a]]]") == "a" * 8           # deep multiplication
assert decode_stack("3[]") == ""                       # empty body (outside the prompt's grammar, harmless)
assert decode_stack("2[a]b2[c]") == "aabcc"

# recursion limit: nesting depth 5000, answer is just 'a'
deep = "1[" * 5000 + "a" + "]" * 5000
print("default recursion limit:", sys.getrecursionlimit())
assert decode_stack(deep) == "a"
try:
    decode_rec(deep)
    print("recursive version: OK")
except RecursionError:
    print("recursive version at depth 5000: RecursionError; stack version returned", repr(decode_stack(deep)))

# seeded randomised cross-check on generated valid encodings
rng = random.Random(21)


def gen(depth):
    parts = []
    for _ in range(rng.randint(1, 3)):
        if depth > 0 and rng.random() < 0.5:
            parts.append(str(rng.randint(1, 12)) + "[" + gen(depth - 1) + "]")
        else:
            parts.append("".join(rng.choice("abc") for _ in range(rng.randint(1, 3))))
    return "".join(parts)


n = 0
while n < 1000:
    s = gen(3)
    want = decode_brute(s)
    assert decode_stack(s) == want and decode_rec(s) == want, s
    n += 1
print("random cross-check passed:", n, "encoded strings")
```

**Output (my run):**
```
'3[a]2[bc]' -> 'aaabcbc'
'3[a2[c]]' -> 'accaccacc'
'2[abc]3[cd]ef' -> 'abcabccdcdcdef'
'ab10[c]' -> 'abcccccccccc'
default recursion limit: 1000
recursive version at depth 5000: RecursionError; stack version returned 'a'
random cross-check passed: 1000 encoded strings
```
Observed on Python 3.13: the default recursion limit is 1000, and the recursive parser failed at nesting depth 5000 while the stack version worked. All four prompt examples are correct.

**Edge cases:**
- No brackets: return the string as is.
- Multi-digit counts (`10[c]`, `300[a]`): do not read one digit at a time.
- Nested multiplication: `2[2[2[a]]]` gives 8 letters.
- Letters after a closing bracket (`2[a]b`) belong to the outer level, which is why you restore `outer`.
- Deep nesting: the explicit stack survives; the recursive one does not (see output).

**Follow-ups:**
- *Can you raise the recursion limit?* `sys.setrecursionlimit` can, but too high a value risks a real C-stack crash. The explicit stack is the safe answer.
- *What if digits can appear as plain text?* The grammar must say; usually you require that digits are only counts.
- *Do it with O(1) extra for the stack?* Not generally; the nesting needs memory.

**Common mistakes:**
- Treating the count as one digit.
- Forgetting to reset `k` after `[`.
- Not restoring the outer text on `]` (losing the text before the bracket).
- Using string `+=` in a loop on big outputs; collect pieces in a list and join once.

### Q9 ⭐⭐⭐ 🟡 Simplify Unix path. `path` is an absolute Unix-style path (starts with '/', up to 3000 characters of letters, digits, '.', '_' and '/'). Return the canonical path: single leading '/', no trailing '/', repeated slashes collapsed, '.' dropped, '..' goes up one level (at the root it stays at the root), and a name made only of three or more dots is an ordinary name. Split on '/' and use a stack of names. Example: '/home/' -> '/home'; '/home//foo/' -> '/home/foo'; '/a/./b/../../c/' -> '/c'; '/../' -> '/'; '/.../a/../b/c/../d/./' -> '/.../b/d'.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Stack of path components. `..` means "undo the most recent directory", which is a pop.

**Say this first (1 line):** "Split on '/', skip empty and '.', pop on '..' if there is something to pop, push everything else, then join with a leading '/'."

**Brute force:** Rewrite the string until it stops changing: collapse `//`, remove `/./`, delete leading `/../`, and cancel `/name/../`. This works but rescans the whole string many times (O(n^2) worst case) and the rules are fiddly. It is my independent checker. Also note `posixpath.normpath` is not a safe shortcut: it keeps a leading double slash (`//a` stays `//a`), as the output shows.

**Optimal:**
- `path.split('/')` gives components. Empty strings come from `//` or the edges.
- Empty or `'.'`: ignore.
- `'..'`: pop if the stack is non-empty; at the root, do nothing.
- Anything else, including `'...'` and names like `'a.b'`: push. Only exactly `'.'` and `'..'` are special.
- Result: `'/' + '/'.join(stack)`. An empty stack gives `'/'` with no extra work.
- Invariant: the stack is the canonical path of everything processed so far, one component per level.

**Complexity:** Time O(n) in the path length: `split` is O(n), each component is pushed and popped at most once, and the `join` is O(n). Space O(n) for the components.

**Dry run:** `'/a/./b/../../c/'`.
| component | action | stack |
|---|---|---|
| '' | skip | [] |
| a | push | [a] |
| . | skip | [a] |
| b | push | [a, b] |
| .. | pop | [a] |
| .. | pop | [] |
| c | push | [c] |
| '' | skip | [c] |
Result `'/c'`.

**Code:**
```python
import posixpath
import random
import re


def simplify_rewrite(path):
    # reference: rewrite the string until nothing changes (independent of the stack idea)
    s = path if path.endswith("/") else path + "/"
    while True:
        t = s
        t = re.sub(r"/+", "/", t)                        # collapse repeated slashes
        t = t.replace("/./", "/")                        # drop '.'
        t = re.sub(r"^/(\.\./)+", "/", t)                # '..' at the root stays at the root
        t = re.sub(r"/(?!\.\.?/)[^/]+/\.\./", "/", t, count=1)      # name/.. cancels (name is not '.' or '..')
        if t == s:
            break
        s = t
    return s[:-1] if len(s) > 1 else s


def simplify_stack(path):
    stack = []
    for name in path.split("/"):
        if name in ("", "."):
            continue                                     # empty (from '//' or edges) and '.' do nothing
        if name == "..":
            if stack:
                stack.pop()                              # go up one level; at the root do nothing
        else:
            stack.append(name)                           # includes '...' and 'a.b'
    return "/" + "/".join(stack)


examples = [("/home/", "/home"), ("/home//foo/", "/home/foo"), ("/a/./b/../../c/", "/c"),
            ("/../", "/"), ("/.../a/../b/c/../d/./", "/.../b/d")]
for p, want in examples:
    assert simplify_stack(p) == simplify_rewrite(p) == want, (p, simplify_stack(p), simplify_rewrite(p))
    print(repr(p), "->", repr(simplify_stack(p)))

# edge cases
assert simplify_stack("/") == "/"
assert simplify_stack("////") == "/"
assert simplify_stack("/..") == "/" and simplify_stack("/../..") == "/"
assert simplify_stack("/a/..") == "/"                    # back to root, no trailing slash
assert simplify_stack("/...") == "/..."                  # three dots is a name
assert simplify_stack("/a.b/c_d/../e") == "/a.b/e"
assert simplify_stack("/" + "a/" * 1500) == "/" + "/".join(["a"] * 1500)   # about 3000 characters

# a Python-library trap: normpath keeps a leading double slash on POSIX
print("posixpath.normpath('//a') =", posixpath.normpath("//a"), "  but expected '/a':", simplify_stack("//a"))
assert posixpath.normpath("//a") == "//a" and simplify_stack("//a") == "/a"

# seeded randomised cross-check
rng = random.Random(4)
pieces = ["a", "b", "ab", ".", "..", "...", "", ""]
for _ in range(3000):
    path = "/" + "/".join(rng.choice(pieces) for _ in range(rng.randint(0, 8)))
    assert simplify_stack(path) == simplify_rewrite(path), (path, simplify_stack(path), simplify_rewrite(path))
print("random cross-check passed: 3000 paths")
```

**Output (my run):**
```
'/home/' -> '/home'
'/home//foo/' -> '/home/foo'
'/a/./b/../../c/' -> '/c'
'/../' -> '/'
'/.../a/../b/c/../d/./' -> '/.../b/d'
posixpath.normpath('//a') = //a   but expected '/a': /a
random cross-check passed: 3000 paths
```
All five prompt examples are correct. The `normpath` line is observed on Python 3.13: it returns `'//a'`, so it is not the canonical form this question asks for.

**Edge cases:**
- Only slashes (`'////'`) or `'/'`: answer `'/'`.
- `'..'` at the root (`'/../..'`): stays `'/'`.
- Going back to the root (`'/a/..'`): `'/'`, not `''` and not `'/'` plus a trailing slash.
- `'...'` is an ordinary name, so `'/...'` stays `'/...'`.
- Long path (3000 characters): linear, nothing recursive.

**Follow-ups:**
- *Relative paths?* Then `..` at an empty stack must be kept (push it), since you cannot go above an unknown current directory.
- *Symlinks?* Then the string alone is not enough; you need the filesystem.
- *Windows?* Different separators and drive letters; ask which rules apply.

**Common mistakes:**
- Treating `'...'` as a special name.
- Popping from an empty stack on `..` at the root.
- Returning `''` for the root instead of `'/'`.
- Leaving a trailing slash, or only collapsing double slashes with `replace` (which misses `///`).

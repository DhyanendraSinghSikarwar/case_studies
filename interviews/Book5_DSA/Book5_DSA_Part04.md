# Book 5 — Part 4: Stack, queue, monotonic stack

**Topic:** Python DSA for product-company interviews: bracket matching and validation (valid parentheses, minimum removals, longest valid parentheses), stacks with extra O(1) powers (min stack, max stack with popMax), stack-based parsing and evaluation (reverse Polish notation, calculators with parentheses and with all four operators, decode string, simplify path, exclusive time of functions, backspace compare, adjacent-duplicate removal), queue and stack implemented from each other (queue via two stacks, stack via queues), ring buffers (circular queue, circular deque), monotonic stack (next greater and next smaller, circular next greater, daily temperatures, stock span, previous and next smaller indices, largest rectangle in a histogram, maximal rectangle in a binary matrix, trapping rain water by layers, sum of subarray minimums, visible people, the 132 pattern), monotonic-greedy string problems (remove k digits, remove duplicate letters), car fleet and asteroid-style stack simulation, monotonic deque as a reusable class and as DP speed-up (jump game with window maximum), validate stack sequences, BFS-level queue idiom and undo/redo plus browser history at concept level only, and Python specifics (list as stack, deque versus list.pop(0), queue.Queue versus deque thread-safety, recursion limit versus explicit stack and the recursion-to-stack recipe)

**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 13, ⭐⭐ 16, ⭐ 11)  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns stacks, queues, deques and the monotonic stack and queue patterns, plus the Python specifics around them. Part 2 already owns the plain sliding-window-maximum prompt, trapping rain water by prefix/suffix maxima and two pointers, shortest subarray with sum at least k (deque over prefix sums) and the two-deque max-minus-min window (cross-referenced here only as 'Part 2 Q14, Q16, Q43', each checked against its heading; none of those prompts is repeated, and the questions here are the stack version of rain water, a reusable monotonic-queue class with the duplicate rule, and a different deque DP, the jump game with window maximum). Part 3 owns the single-pass calculator without stack design (cross-referenced as 'Part 3 Q13', checked against its heading; the calculator questions here are the stack-of-contexts versions with parentheses). Part 1 owns hashing; Part 5 binary search; Part 7 trees (iterative traversals belong there, so the explicit-stack question here uses nested lists); Part 8 heaps, intervals and greedy; Part 9 graphs (the BFS-level question here is the queue idiom on a tiny hand-built dict, concept level only); Part 14 owns design problems (undo/redo and browser history here are concept level with two stacks). Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example in every prompt was run against brute-force or independent reference code (scratch/B5P04_wavea/check_examples.py, python3 -I) before freezing, including a check that CPython's default recursion limit of 1000 raises RecursionError on a 5000-deep chain and that floor division gives -4 for 7 // -2; all examples passed on the first full run after one flawed car-fleet reference simulation (my own checker bug, not a prompt example) was rewritten. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for neetcode.io) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part04_sources.md). Searches returned monotonic-stack pattern guides, a stacks-and-queues roundup and a few candidate-reported Amazon items for the queue/stack conversion questions; the searches for TCS and Infosys returned only a generic fresher list and no stack or queue problem attributed to either, and no query surfaced Google or Microsoft reports, so 'Asked at' tags name source types (pattern guides and practice lists, prep roundups, candidate-reported snippets, Python docs mirrors, editor knowledge of standard lists), not verified company reports; company tags on community pages are unverified. The queue-module documentation was not found, so queue.Queue claims rest on editor knowledge plus the sandbox run. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---

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
n=  25000: list.pop(0)   0.057s   deque.popleft   0.003s
n=  50000: list.pop(0)   0.200s   deque.popleft   0.006s
n= 100000: list.pop(0)   0.772s   deque.popleft   0.013s
n= 200000: list.pop(0)   3.099s   deque.popleft   0.027s
2000 middle lookups of 200000 items: list 0.0001s   deque 0.0057s
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

### Q10 ⭐⭐⭐ 🟡 Next greater element in a circular array. `nums` is circular (after the last element comes the first), 1 <= len <= 10^4, values may repeat. For each index return the first strictly greater value met when walking forward around the circle at most once, or -1. Loop over indices 0..2n-1 with `i % n` while keeping a decreasing stack of indices, pushing only during the first pass; explain why one extra lap is enough and why a later pass must not push. Example: [1,2,1] -> [2,-1,2]; [1,2,3,4,3] -> [2,3,4,-1,4]; [5,5] -> [-1,-1].
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Monotonic stack, with the array treated as circular by looping over indices `0..2n-1` and using `i % n`. Same "first greater to the right" idea as the subset version, but the right side wraps around.

**Say this first (1 line):** "Walk the array twice; push indices only on the first walk; the second walk only resolves the elements that still wait."

**Brute force:** For each `i`, look at the next `n - 1` elements around the circle until one is greater. O(n^2) (n = 10^4 gives about 10^8 steps worst case). It is my checker.

**Optimal:**
- Keep a stack of indices whose values are non-increasing from bottom to top (they are the elements still waiting for a greater value).
- For `i` from 0 to `2n - 1`: let `v = nums[i % n]`. While the top index has `nums[top] < v`, pop it and set its answer to `v`. Strict `<`, so equal values do not count as greater.
- Push `i` only when `i < n`.
- Why two laps are enough: the first greater element after position `j`, going around, is at most `n - 1` steps away, so it appears before you return to `j`. Looking at positions `j+1 .. j+n-1` covers every other element once. Two laps cover that window for every start `j`.
- Why the second lap must not push: every index is already on the stack or resolved after lap one. Pushing again adds copies that can never get a new answer (the same values are seen again), costs extra memory, and if you store the raw loop index `i >= n` you would write `res[i]` out of range. The code stores only indices from the first pass, so `res[stack.pop()]` is always valid.
- Invariant: after position `i`, the stack holds the (first-pass) indices that have no greater value among elements seen so far, in non-increasing value order.

**Complexity:** Time O(n): at most n pushes, hence at most n pops, plus 2n loop steps. Space O(n) for the stack and output.

**Dry run:** `[1, 2, 1]`, `n = 3`.
| i | v | pops (answer) | stack after |
|---|---|---|---|
| 0 | 1 | | [0] |
| 1 | 2 | pop 0, ans[0] = 2 | [1] |
| 2 | 1 | | [1, 2] |
| 3 (idx 0) | 1 | none (1 < 1 is false); no push | [1, 2] |
| 4 (idx 1) | 2 | pop 2, ans[2] = 2 (the next top, index 1, has 2 < 2 false) | [1] |
| 5 (idx 2) | 1 | none | [1] |
Index 1 (value 2, the maximum) stays -1. Result `[2, -1, 2]`.

**Code:**
```python
import random


def nge_circ_brute(nums):
    n = len(nums)
    res = []
    for i in range(n):
        ans = -1
        for step in range(1, n):                 # at most one trip around, excluding i itself
            v = nums[(i + step) % n]
            if v > nums[i]:
                ans = v
                break
        res.append(ans)
    return res


def nge_circ(nums, depth=None):
    n = len(nums)
    res = [-1] * n
    stack = []                                   # indices with no greater value found yet
    for i in range(2 * n):
        v = nums[i % n]
        while stack and nums[stack[-1]] < v:
            res[stack.pop()] = v
        if i < n:                                # push only in the first pass
            stack.append(i)
        if depth is not None:
            depth.append(len(stack))
    return res


def nge_circ_pushall(nums, depth=None):
    # pushes in both passes: still correct here (duplicate entries only re-write the same value),
    # but the stack can hold up to 2n entries and the second pass resolves nothing new
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(2 * n):
        v = nums[i % n]
        while stack and nums[stack[-1] % n] < v:
            res[stack.pop() % n] = v
        stack.append(i)
        if depth is not None:
            depth.append(len(stack))
    return res


examples = [([1, 2, 1], [2, -1, 2]), ([1, 2, 3, 4, 3], [2, 3, 4, -1, 4]), ([5, 5], [-1, -1])]
for nums, want in examples:
    assert nge_circ(nums) == nge_circ_brute(nums) == want, nums
    print(nums, "->", nge_circ(nums))

# edge cases
assert nge_circ([7]) == [-1]                              # single element: itself is not greater than itself
assert nge_circ([3, 3, 3]) == [-1, -1, -1]                # all equal
assert nge_circ([3, 2, 1]) == [-1, 3, 3]                  # decreasing: wraps to the front
assert nge_circ([1, 5, 1, 1]) == [5, -1, 5, 5]            # duplicates around the maximum
n = 10_000
assert nge_circ(list(range(n, 0, -1)))[1:] == [n] * (n - 1)       # max size
assert nge_circ(list(range(n))) == list(range(1, n)) + [-1]

# why a second pass must not push: measure the stack depth on a decreasing array
dec = list(range(1000, 0, -1))
d1, d2 = [], []
nge_circ(dec, d1)
nge_circ_pushall(dec, d2)
print("max stack size, push in pass 1 only:", max(d1), "; push in both passes:", max(d2))
assert max(d1) == 1000 and max(d2) >= max(d1)
print("pushes: pass-1-only", 1000, "vs both passes", 2000, "(the extra 1000 can never resolve anything new)")

# seeded randomised cross-check (small range for many ties)
rng = random.Random(17)
for _ in range(3000):
    nums = [rng.randint(-3, 5) for _ in range(rng.randint(1, 10))]
    assert nge_circ(nums) == nge_circ_brute(nums), nums
    assert nge_circ_pushall(nums) == nge_circ_brute(nums), nums   # same answers, just wasteful
print("random cross-check passed: 3000 cases")
```

**Output (my run):**
```
[1, 2, 1] -> [2, -1, 2]
[1, 2, 3, 4, 3] -> [2, 3, 4, -1, 4]
[5, 5] -> [-1, -1]
max stack size, push in pass 1 only: 1000 ; push in both passes: 1001
pushes: pass-1-only 1000 vs both passes 2000 (the extra 1000 can never resolve anything new)
random cross-check passed: 3000 cases
```
All three prompt examples are correct. The measurement shows that pushing during the second lap only adds entries without changing the answers.

**Edge cases:**
- One element: `[-1]`. Its own value is not greater than itself.
- All equal: all -1 (strict comparison).
- The maximum value: always -1, even if it appears more than once.
- Decreasing array: after the first lap everything is on the stack; the second lap resolves all but the maximum.
- Duplicates: `[1, 5, 1, 1]` gives `[5, -1, 5, 5]`.

**Follow-ups:**
- *Why not copy the array (`nums + nums`)?* It also works, but the `i % n` trick avoids O(n) extra memory.
- *Circular daily-temperatures distance?* Same loop, store `(i - j)` for pops, and cap at `n - 1`.
- *Previous greater, circular?* Walk backwards, or run the same loop on the reversed array.

**Common mistakes:**
- Pushing during the second lap.
- Using `<=` when popping, so equal values count as greater.
- Looping only `n` times, which misses answers that wrap around.
- Forgetting `i % n` and indexing past the end.

### Q11 ⭐⭐⭐ 🔴 Basic calculator with parentheses. `s` is a valid expression of non-negative integers, '+', '-', parentheses and spaces, where '-' may also be unary right after '(' or at the start (for example '-(2+3)'); evaluate it with a stack (up to 3*10^5 characters, so no recursion). Keep a running result and a current sign; on '(' push the result and the sign and reset, on ')' pop and combine. Part 3 Q13 does the version without parentheses in one pass with no stack design; this question is the stack-of-contexts version. Example: '1 + 1' -> 2; ' 2-1 + 2 ' -> 3; '(1+(4+5+2)-3)+(6+8)' -> 23; '-(2+3)' -> -5; '2-(5-6)' -> 3.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Stack of contexts. Each `(` starts a fresh sub-expression; the stack remembers what was going on outside it (the running result and the sign in front of the bracket).

**Say this first (1 line):** "One pass, keep `result`, `sign`, `num`. On `(` push result and sign and reset. On `)` finish the inner number, then combine: inner * saved sign + saved result. O(n) time, O(depth) space, no recursion."

**Brute force:** A recursive-descent parser: `expr()` loops over tokens and calls itself on `(`. Correct and easy to read. It is my checker.
- Cost: O(n) time, but the Python call stack grows with the nesting depth. With 3 * 10^5 characters the nesting can be 1.5 * 10^5 deep, far past CPython's default limit of 1000.
- That is why the prompt says "no recursion".

**Optimal:**
- Only `+` and `-` exist, so there is no precedence. Brackets are the only structure. A bracket is just a number whose value I compute first and then add with its sign.
- Variables: `result` (finished part of the current level), `sign` (sign of the next number or bracket), `num` (digits being read).
- Digit: `num = num * 10 + d`.
- `+` or `-`: flush `result += sign * num`, reset `num = 0`, set the new `sign`.
- `(`: push `result`, push `sign`; reset `result = 0`, `sign = 1`.
- `)`: flush `result += sign * num`, `num = 0`; then `result = result * saved_sign + saved_result`.
- Space: ignore. At the end return `result + sign * num`.
- Invariant: at any moment `result` is the value of the current level up to the last operator, and the stack holds, from the outside in, one (result, sign) pair per open bracket.
- Unary minus works for free. At the start, or right after `(`, `num` is 0, so the flush adds 0 and then the sign becomes -1.
- Push order matters: push result first, sign second; pop sign first. The sign is on top.

**Complexity:** Time O(n): each character is looked at once, each push and pop is O(1). Space O(d) where d is the maximum nesting depth (two ints per open bracket), worst case O(n).
- The stack lives on the heap, so depth is bounded by memory, not by the recursion limit.

**Dry run:** `'2-(5-6)'`
| char | action | result | sign | num | stack |
|---|---|---|---|---|---|
| `2` | read digit | 0 | 1 | 2 | [] |
| `-` | flush 0 + 1*2, new sign -1 | 2 | -1 | 0 | [] |
| `(` | push result 2, push sign -1; reset | 0 | 1 | 0 | [2, -1] |
| `5` | read digit | 0 | 1 | 5 | [2, -1] |
| `-` | flush 0 + 5, new sign -1 | 5 | -1 | 0 | [2, -1] |
| `6` | read digit | 5 | -1 | 6 | [2, -1] |
| `)` | flush 5 - 6 = -1; pop sign -1, pop result 2: -1 * -1 + 2 | 3 | -1 | 0 | [] |
| end | 3 + (-1) * 0 | 3 | | | |

Answer 3.

**Code:**
```python
import random
import re
import sys


def calc_brute(s):
    # reference only: recursive-descent parser (recursion depth = nesting depth)
    pos = 0

    def expr():
        nonlocal pos
        total, sign = 0, 1
        while pos < len(s) and s[pos] != ")":
            c = s[pos]
            if c == " ":
                pos += 1
            elif c == "+":
                sign = 1
                pos += 1
            elif c == "-":
                sign = -1
                pos += 1
            elif c == "(":
                pos += 1
                total += sign * expr()
                pos += 1  # skip ')'
                sign = 1
            else:
                num = 0
                while pos < len(s) and s[pos].isdigit():
                    num = num * 10 + int(s[pos])
                    pos += 1
                total += sign * num
                sign = 1
        return total

    return expr()


def calc(s):
    result, sign, num = 0, 1, 0
    stack = []  # saved (result, sign) of the enclosing contexts
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "+" or ch == "-":
            result += sign * num
            num = 0
            sign = 1 if ch == "+" else -1
        elif ch == "(":
            stack.append(result)
            stack.append(sign)
            result, sign = 0, 1
        elif ch == ")":
            result += sign * num
            num = 0
            result = result * stack.pop() + stack.pop()  # sign first, then outer result
    return result + sign * num


examples = [("1 + 1", 2), (" 2-1 + 2 ", 3), ("(1+(4+5+2)-3)+(6+8)", 23), ("-(2+3)", -5), ("2-(5-6)", 3)]
for s, want in examples:
    got = calc(s)
    assert got == calc_brute(s) == eval(s) == want, (s, got)  # eval only as a test oracle
    print(repr(s), "->", got)

assert calc("0") == 0
assert calc("(((5)))") == 5
assert calc("-(-(2))") == 2
assert calc("2-(-3)") == 5
assert calc(" ( 0 ) + 4 ") == 4
assert calc("10-(2-(3-(4-5)))") == eval("10-(2-(3-(4-5)))")


def gen(rng, depth):
    parts = []
    if rng.random() < 0.3:
        parts.append("-")  # unary minus only at the start of a group
    for t in range(rng.randint(1, 4)):
        if t:
            parts.append(rng.choice("+-"))
        if depth < 3 and rng.random() < 0.3:
            parts.append("(" + gen(rng, depth + 1) + ")")
        else:
            parts.append(str(rng.randint(0, 120)))
    return "".join(parts)


rng = random.Random(11)
for _ in range(2000):
    e = gen(rng, 0)
    e = re.sub(r"\d+|.", lambda m: m.group() + (" " if rng.random() < 0.3 else ""), e)  # spaces between tokens
    assert calc(e) == calc_brute(e) == eval(e.replace(" ", "")), e
print("random cross-check passed: 2000 cases")

deep = "(" * 100000 + "1" + ")" * 100000 + "+" + "-(" * 50000 + "2" + ")" * 50000
print("stack version, 150000-deep nesting ->", calc(deep))
print("recursion limit on this run:", sys.getrecursionlimit())
try:
    calc_brute(deep)
    print("recursive version: ok")
except RecursionError:
    print("recursive version: RecursionError")
```

**Output (my run):**
```
'1 + 1' -> 2
' 2-1 + 2 ' -> 3
'(1+(4+5+2)-3)+(6+8)' -> 23
'-(2+3)' -> -5
'2-(5-6)' -> 3
random cross-check passed: 2000 cases
stack version, 150000-deep nesting -> 3
recursion limit on this run: 1000
recursive version: RecursionError
```
All five examples in the prompt are correct. Observed on Python 3.13: the recursive reference dies with `RecursionError` on 150000-deep nesting (limit 1000) while the stack version returns instantly. (`eval` is used only as a test oracle on safe generated strings, never in the solution.)

**Edge cases:**
- Unary minus at the start (`-(2+3)`) and right after `(` (`2-(-3)`).
- Spaces anywhere between tokens, including leading and trailing.
- Multi-digit numbers (`num * 10 + d`).
- `(((5)))`, a number wrapped in many brackets.
- A `)` right after a number needs the flush before combining, or the last number is lost.
- Nesting 1.5 * 10^5 deep: fine for the stack, fatal for recursion.

**Follow-ups:**
- *Add `*` and `/`?* Then precedence matters; see the four-operator question later in this part (it keeps a number stack plus a pending operator).
- *Without the stack?* Recursion, or a reversal trick (flip the signs inside brackets as you go). The stack is the clearest in an interview.
- *Part 3 Q13 does this without parentheses; what is new here?* There the whole state was `result`, `sign`, `num`. Brackets add a stack of saved states, one per open level.

**Common mistakes:**
- Popping in the wrong order (result before sign) and getting wrong signs inside brackets.
- Forgetting the last flush at the end of the string (`result + sign * num`).
- Forgetting to flush `num` before combining on `)`.
- Resetting `sign` to 1 on `(` but forgetting `result = 0`.
- Using recursion and hitting the limit on deep input.

### Q12 ⭐⭐⭐ 🔴 Largest rectangle in a histogram. `heights` is a list of n non-negative integers (n <= 10^5), each bar of width 1; return the area of the largest axis-aligned rectangle that fits inside the bars. Use an increasing stack of indices: when a shorter bar arrives, pop and compute the rectangle whose height is the popped bar, whose right edge is the current index and whose left edge is the new stack top; show the sentinel bar of height 0 that flushes the stack, and why each bar is the limiting height of exactly one best rectangle. Give the O(n^2) brute force (try every pair of edges) as the checker. Example: [2,1,5,6,2,3] -> 10; [2,4] -> 4; [1,1,1,1] -> 4; [0] -> 0; [6,2,5,4,5,1,6] -> 12.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Monotonic (increasing) stack, nearest smaller bar on each side. Every bar is the limiting height of exactly one best rectangle, and the stack finds that rectangle's two edges.

**Say this first (1 line):** "For each bar, the widest rectangle with that bar as the shortest runs from the nearest smaller bar on its left to the nearest smaller bar on its right. An increasing stack finds both edges in one pass, O(n)."

**Brute force:** Try every pair of edges `(i, j)`, keep the running minimum height between them, area = min * width. O(n^2) time, O(1) space. It is my checker. (Trying every bar as the limiting height and expanding outwards is also O(n^2).)

**Optimal:**
- A best rectangle can always be stretched until its shortest bar is the limit. So the answer is the max over bars `k` of `h[k] * (R - L - 1)`, where `L` is the nearest index to the left with a smaller height and `R` the nearest to the right.
- Keep a stack of indices whose heights are strictly increasing from bottom to top.
- A new bar `cur` arrives. While the top bar is `>= cur`, pop it. The popped bar `p` has `cur` as its right edge (first bar to the right that is not taller). Its left edge is the new top (the nearest bar to the left that is shorter), or -1 if the stack is empty.
- Area for the popped bar = `h[p] * (i - left - 1)`.
- Sentinel: append a bar of height 0 at the end. It is smaller than everything, so it pops every bar still waiting. No cleanup loop needed.
- Why `>=` and not `>`: with equal heights the older bar is popped with a slightly short width, but the newer equal bar later covers the full width. The maximum is still found.
- Each index is pushed once and popped once. That is the O(n) proof.

**Complexity:** Time O(n): n + 1 pushes, at most n + 1 pops, O(1) each. Space O(n) for the stack (a fully increasing input keeps everything on it until the sentinel).

**Dry run:** `[2,1,5,6,2,3]`, with sentinel `hs = [2,1,5,6,2,3,0]`.
| i | cur | pops (index, height, left, width, area) | stack after |
|---|---|---|---|
| 0 | 2 | none | [0] |
| 1 | 1 | (0, 2, -1, 1, 2) | [1] |
| 2 | 5 | none | [1,2] |
| 3 | 6 | none | [1,2,3] |
| 4 | 2 | (3, 6, 2, 1, 6), (2, 5, 1, 2, 10) | [1,4] |
| 5 | 3 | none | [1,4,5] |
| 6 | 0 | (5, 3, 4, 1, 3), (4, 2, 1, 4, 8), (1, 1, -1, 6, 6) | [6] |

Best area 10: bars 5 and 6, width 2.

**Code:**
```python
import random


def largest_brute(h):
    # try every pair of edges (i, j): width * lowest bar between them. O(n^2)
    best = 0
    for i in range(len(h)):
        low = h[i]
        for j in range(i, len(h)):
            low = min(low, h[j])
            best = max(best, low * (j - i + 1))
    return best


def largest_stack(heights):
    hs = heights + [0]          # sentinel bar of height 0 flushes the stack at the end
    stack = []                  # indices, heights strictly increasing from bottom to top
    best = 0
    for i, cur in enumerate(hs):
        while stack and hs[stack[-1]] >= cur:
            height = hs[stack.pop()]
            left = stack[-1] if stack else -1       # new top = nearest smaller bar on the left
            best = max(best, height * (i - left - 1))  # right edge is i (exclusive)
        stack.append(i)
    return best


examples = [([2, 1, 5, 6, 2, 3], 10), ([2, 4], 4), ([1, 1, 1, 1], 4), ([0], 0), ([6, 2, 5, 4, 5, 1, 6], 12)]
for h, want in examples:
    got = largest_stack(h)
    assert got == largest_brute(h) == want, (h, got)
    print(h, "->", got)

assert largest_stack([]) == 0
assert largest_stack([7]) == 7
assert largest_stack([0, 0, 0]) == 0
assert largest_stack([5, 5, 5, 5, 5]) == 25          # all equal: ties popped, still right
assert largest_stack([1, 2, 3, 4, 5]) == 9           # increasing: flushed by the sentinel
assert largest_stack([5, 4, 3, 2, 1]) == 9           # decreasing: pops on every step
assert largest_stack([2, 0, 2]) == 2                 # a zero splits the histogram
big = [10 ** 9] * 100000
assert largest_stack(big) == 10 ** 9 * 100000        # max size, no overflow in Python

rng = random.Random(12)
cases = 0
for _ in range(3000):
    n = rng.randint(0, 12)
    h = [rng.randint(0, rng.choice([2, 5, 9])) for _ in range(n)]
    assert largest_stack(h) == largest_brute(h), h
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
[2, 1, 5, 6, 2, 3] -> 10
[2, 4] -> 4
[1, 1, 1, 1] -> 4
[0] -> 0
[6, 2, 5, 4, 5, 1, 6] -> 12
random cross-check passed: 3000 cases
```
All five examples in the prompt are correct.

**Edge cases:**
- Empty list: the sentinel alone gives 0.
- A single bar; all zeros; a zero in the middle (it splits the histogram).
- All equal heights: ties get popped, the last bar still sees the full width.
- Strictly increasing: nothing pops until the sentinel. Strictly decreasing: pops on every step.
- Max size with big heights: Python ints do not overflow.

**Follow-ups:**
- *Maximal rectangle in a binary matrix?* Build the histogram per row and run this. That is the matrix question later in this part.
- *Do it without the sentinel?* Run a cleanup loop after the scan, popping the rest with right edge `n`. Same logic, more code.
- *Two passes instead?* Compute `left[]` and `right[]` smaller arrays separately, then one max loop. Simpler to reason about, same O(n).

**Common mistakes:**
- Width as `i - top - 1` after popping, using the popped index instead of the new top.
- Forgetting the empty-stack case (left edge -1, width `i`).
- Forgetting the sentinel and never flushing the last bars.
- Storing heights instead of indices, so the width cannot be computed.

### Q13 ⭐⭐⭐ 🔴 Trapping rain water with a stack. `height` is a list of n non-negative bar heights (n <= 2*10^4). Return the total water trapped, computed layer by layer with a decreasing stack of indices: when a taller bar arrives, pop the bottom of a basin, and the water above it is (min of the two walls - bottom) times the horizontal distance between the walls. Part 2 Q14 holds the prefix/suffix and two-pointer versions, which are not repeated; here say what the stack version computes differently (horizontal layers versus vertical columns) and why it is still O(n). Example: [0,1,0,2,1,0,1,3,2,1,2,1] -> 6; [4,2,0,3,2,5] -> 9; [3,0,2] -> 2; [1,2,3] -> 0.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Monotonic (non-increasing) stack of indices. The stack holds the left walls of basins that are still open; a taller bar closes the lowest open basin.

**Say this first (1 line):** "A decreasing stack of bar indices. When a taller bar arrives, pop the basin floor, and the water above it is width between the two walls times (lower wall minus floor). Each index is pushed and popped once, O(n)."

**Brute force:** Column view. For each column, water = `min(max to the left, max to the right) - height`. Recomputing both maxima per column is O(n^2) time, O(1) space. It is my checker. (Prefix and suffix arrays, or two pointers, make this O(n); those are in Part 2 Q14 and are not repeated.)

**Optimal:**
- Keep a stack of indices with non-increasing heights. A bar that is not taller than the top is just pushed: no basin closes yet.
- A bar `h` taller than the top closes a basin. Pop `bottom` (the floor). If the stack is now empty there is no left wall, so nothing is held; stop popping.
- Otherwise `left = stack[-1]` is the left wall and `i` is the right wall. The floor sits at `height[bottom]`.
- Water in this layer = `width * depth`, where `width = i - left - 1` and `depth = min(h, height[left]) - height[bottom]`.
- Repeat while `h` is still taller than the new top. Each pass peels the next horizontal layer.
- Layers versus columns: the prefix/suffix version adds water one vertical column at a time. The stack version adds it one horizontal strip at a time, between two walls, and each strip is added exactly once, at the moment the right wall appears.
- Equal heights are fine: an equal wall is not "taller", so it is pushed. When a taller bar comes later, the equal wall is popped with depth 0 and adds nothing.

**Complexity:** Time O(n): every index is pushed once and popped at most once, and each pop does O(1) arithmetic. The inner while loop does not make it O(n^2) because pops are bounded by pushes. Space O(n) worst case (a non-increasing input keeps everything on the stack).

**Dry run:** `[4,2,0,3,2,5]`
| i | h | action | total |
|---|---|---|---|
| 0, 1, 2 | 4, 2, 0 | pushed, stack [0,1,2] | 0 |
| 3 | 3 | pop floor 2 (h 0), left 1 (h 2): width 1, depth min(3,2)-0 = 2, adds 2. Pop floor 1 (h 2), left 0 (h 4): width 2, depth min(3,4)-2 = 1, adds 2. Push 3 | 4 |
| 4 | 2 | not taller, push, stack [0,3,4] | 4 |
| 5 | 5 | pop floor 4 (h 2), left 3 (h 3): width 1, depth 1, adds 1. Pop floor 3 (h 3), left 0 (h 4): width 4, depth 1, adds 4. Pop floor 0: stack empty, stop. Push 5 | 9 |

Answer 9.

**Code:**
```python
import random


def trap_brute(height):
    # column view: water above column i = min(max to its left, max to its right) - height[i]. O(n^2)
    total = 0
    for i in range(len(height)):
        left = max(height[: i + 1])
        right = max(height[i:])
        total += min(left, right) - height[i]
    return total


def trap_stack(height):
    stack = []  # indices, heights non-increasing from bottom to top
    total = 0
    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()
            if not stack:
                break                       # no left wall: nothing is held
            left = stack[-1]
            width = i - left - 1            # horizontal distance between the walls
            depth = min(h, height[left]) - height[bottom]   # one horizontal layer
            total += width * depth
        stack.append(i)
    return total


examples = [([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6), ([4, 2, 0, 3, 2, 5], 9), ([3, 0, 2], 2), ([1, 2, 3], 0)]
for h, want in examples:
    got = trap_stack(h)
    assert got == trap_brute(h) == want, (h, got)
    print(h, "->", got)

assert trap_stack([]) == 0
assert trap_stack([5]) == 0
assert trap_stack([5, 5]) == 0
assert trap_stack([3, 3, 3, 3]) == 0                 # equal walls: nothing held
assert trap_stack([5, 0, 0, 0, 5]) == 15             # one wide basin
assert trap_stack([5, 0, 5, 0, 5]) == 10             # two basins
assert trap_stack([3, 0, 3, 0, 3, 0]) == 6           # trailing basin has no right wall
assert trap_stack([5, 4, 3, 2, 1]) == 0              # decreasing: nothing held
assert trap_stack([0, 3, 0, 3]) == 3
n = 20000
assert trap_stack([n] + [0] * (n - 2) + [n]) == n * (n - 2)   # max size

rng = random.Random(13)
cases = 0
for _ in range(3000):
    n = rng.randint(0, 14)
    h = [rng.randint(0, rng.choice([2, 4, 8])) for _ in range(n)]
    assert trap_stack(h) == trap_brute(h), h
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1] -> 6
[4, 2, 0, 3, 2, 5] -> 9
[3, 0, 2] -> 2
[1, 2, 3] -> 0
random cross-check passed: 3000 cases
```
All four examples in the prompt are correct.

**Edge cases:**
- Empty list, one bar, two bars: 0.
- Non-increasing or all-equal input: nothing is ever popped with a left wall, answer 0.
- A trailing dip with no right wall (`[3,0,3,0]` tail): not counted, because no taller bar ever arrives.
- Pop to an empty stack: must `break`, otherwise `stack[-1]` raises `IndexError`.
- One huge basin at max size (`n, 0, ..., 0, n`): answer is exactly `n * (n - 2)`; Python ints do not overflow.

**Follow-ups:**
- *Why still O(n) with a loop inside a loop?* Amortised: total pops cannot exceed total pushes.
- *Which version would you write first?* Two pointers (Part 2 Q14): O(n) time, O(1) space. The stack is the one to know when the interviewer asks "what if the bars arrive as a stream" or for layer-by-layer reasoning.
- *Is the result the same?* Yes. Both add up the same water cells, just grouped differently.

**Common mistakes:**
- Using the popped bar's height as the top wall instead of `min(h, height[left])`.
- Forgetting `- height[bottom]` in the depth.
- Width as `i - bottom` instead of `i - left - 1`.
- Missing the empty-stack check after the pop.
- Using `>=` and popping equal walls with width and depth confusion (works with care, but strict `>` is simpler).

### Q14 ⭐⭐ 🟢 Implement a stack using queues. Support `push`, `pop`, `top`, `empty` using only queue operations (enqueue to back, dequeue from front, size, is-empty). Give the single-queue version (after each push rotate the n-1 older elements behind the new one, so push is O(n) and pop is O(1)), the two-queue version, and say which of push or pop you would rather make expensive and why it cannot be O(1) for both with a plain queue. Example: push(1), push(2), top() -> 2, pop() -> 2, empty() -> False, pop() -> 1, empty() -> True.
**Asked at:** Candidate-reported Amazon rounds (a Glassdoor review naming stack-using-queues, a Naukri Code360 Amazon entry naming stack with two queues, a PracHub report naming queue with two stacks; snippets only, not opened; candidate-reported, unverified) | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Data-structure conversion. A queue is first-in first-out, a stack is last-in first-out. To fake LIFO, keep the newest item at the front of the queue (reorder on push), or find the newest item at the back (drain on pop).

**Say this first (1 line):** "One queue: after each push, rotate the older items behind the new one so the newest is at the front. Push is O(n), pop and top are O(1). With a plain queue one of the two operations must be linear."

**Brute force:** There is no real brute force here; the naive approach is the design choice itself. The checker is Python's own list used as a stack (`append`, `pop`, `[-1]`), run on the same random command sequences.

**Optimal:**
- *One queue, expensive push (the one I would write):*
  - `push(x)`: enqueue x, then do `len - 1` times: dequeue the front and enqueue it again. The new item ends up at the front, older items behind it in the old order.
  - `pop()`: dequeue the front. `top()`: look at the front. `empty()`: queue is empty.
  - Invariant: the front of the queue is always the top of the stack.
- *Two queues, cheap push:*
  - `push(x)`: enqueue to queue `a`, remember `x` as `last`. O(1).
  - `pop()`: dequeue everything except the last item from `a` into `b`, dequeue and return that last item, then swap the names `a` and `b`. O(n).
  - `top()`: return `last` (updated while draining). O(1).
- Which to make expensive: usually `push`, because pops and tops are the common calls in real use and a reader expects `pop`/`top` to be cheap. If the workload is push-heavy, take the two-queue version.
- Why not both O(1): with only enqueue-at-back and dequeue-from-front, the newest item sits behind all the older ones. Either you move the older ones at push time, or you move them at pop time. This is the standard argument rather than a proof; the amortised case does not help either, because alternating push and pop on a large stack pays the linear cost on every call.
- Note on the front peek: `top()` in the one-queue version uses the queue's own "front" operation (`q[0]` on a deque). That is the ordinary queue ADT. If an interviewer bans it, the two-queue version tracks `last` itself.

**Complexity:**
| Version | push | pop | top | empty | Space |
|---|---|---|---|---|---|
| One queue | O(n) | O(1) | O(1) | O(1) | O(n) |
| Two queues | O(1) | O(n) | O(1) | O(1) | O(n) |

The O(n) in push is the n - 1 rotations, each a dequeue plus an enqueue. In the run below, a push with n items present costs 2n + 1 queue operations (1, 3, 21, 201 for n = 0, 1, 10, 100).

**Dry run:** one queue (front on the left), `push(1), push(2), top(), pop(), empty(), pop(), empty()`
| call | queue after | returns |
|---|---|---|
| push(1) | [1] | |
| push(2) | enqueue: [1,2]; rotate once: [2,1] | |
| top() | [2,1] | 2 |
| pop() | [1] | 2 |
| empty() | [1] | False |
| pop() | [] | 1 |
| empty() | [] | True |

**Code:**
```python
import random
from collections import deque


# Only queue operations are used on the internal queues:
# append (enqueue to back), popleft (dequeue from front), len (size), truthiness (is-empty)
# and q[0] as the queue's "front" peek. Never indexed elsewhere, never popped from the right.

class StackOneQueue:
    """push is O(n) (rotate), pop/top/empty are O(1)."""

    def __init__(self):
        self.q = deque()

    def push(self, x):
        self.q.append(x)
        for _ in range(len(self.q) - 1):       # move the n older items behind the new one
            self.q.append(self.q.popleft())

    def pop(self):
        return self.q.popleft()

    def top(self):
        return self.q[0]                       # peek at the FRONT: a queue's own front() operation

    def empty(self):
        return not self.q


class StackTwoQueues:
    """push is O(1), pop/top are O(n): drain all but the last item into the spare queue."""

    def __init__(self):
        self.a, self.b = deque(), deque()
        self.last = None

    def push(self, x):
        self.a.append(x)
        self.last = x

    def _shift(self):
        while len(self.a) > 1:
            self.last = self.a.popleft()
            self.b.append(self.last)
        return self.a.popleft()

    def pop(self):
        x = self._shift()
        self.a, self.b = self.b, self.a
        return x

    def top(self):
        return self.last

    def empty(self):
        return not self.a


def run(cls, ops):
    s, out = cls(), []
    for op, *arg in ops:
        if op == "push":
            s.push(arg[0])
            out.append(None)
        else:
            out.append(getattr(s, op)())
    return out


def run_list_stack(ops):
    s, out = [], []
    for op, *arg in ops:
        if op == "push":
            s.append(arg[0])
            out.append(None)
        elif op == "pop":
            out.append(s.pop())
        elif op == "top":
            out.append(s[-1])
        else:
            out.append(not s)
    return out


example = [("push", 1), ("push", 2), ("top",), ("pop",), ("empty",), ("pop",), ("empty",)]
for cls in (StackOneQueue, StackTwoQueues):
    got = run(cls, example)
    assert got == [None, None, 2, 2, False, 1, True], got
    print(cls.__name__, "->", got)

for cls in (StackOneQueue, StackTwoQueues):
    s = cls()
    assert s.empty()
    s.push(7)
    assert s.top() == 7 and not s.empty()
    assert s.pop() == 7 and s.empty()
    for v in [5, 5, 5]:                    # duplicates
        s.push(v)
    assert [s.pop(), s.pop(), s.pop()] == [5, 5, 5] and s.empty()
    for v in range(1000):
        s.push(v)
    assert [s.pop() for _ in range(1000)] == list(range(999, -1, -1))   # max size order

rng = random.Random(14)
cases = 0
for _ in range(1500):
    ops, size = [], 0
    for _ in range(rng.randint(1, 30)):
        r = rng.random()
        if size == 0 or r < 0.5:
            ops.append(("push", rng.randint(-5, 5)))
            size += 1
        elif r < 0.75:
            ops.append(("top",))
        elif r < 0.9:
            ops.append(("pop",))
            size -= 1
        else:
            ops.append(("empty",))
    want = run_list_stack(ops)
    assert run(StackOneQueue, ops) == want, ops
    assert run(StackTwoQueues, ops) == want, ops
    cases += 1
print("random cross-check passed:", cases, "operation sequences")

# operation counting: queue operations used per call, to show where the O(n) sits
class Counted(deque):
    ops = 0

    def append(self, x):
        Counted.ops += 1
        super().append(x)

    def popleft(self):
        Counted.ops += 1
        return super().popleft()


def cost_of_push(n):
    s = StackOneQueue()
    s.q = Counted()
    for v in range(n):
        s.push(v)
    Counted.ops = 0
    s.push(n)
    return Counted.ops

print("queue ops for one push when n items are present (one-queue version):",
      [(n, cost_of_push(n)) for n in (0, 1, 10, 100)])
```

**Output (my run):**
```
StackOneQueue -> [None, None, 2, 2, False, 1, True]
StackTwoQueues -> [None, None, 2, 2, False, 1, True]
random cross-check passed: 1500 operation sequences
queue ops for one push when n items are present (one-queue version): [(0, 1), (1, 3), (10, 21), (100, 201)]
```
The prompt example is correct (both classes return `[None, None, 2, 2, False, 1, True]`, where `None` is a push).

**Edge cases:**
- `empty()` on a fresh stack: True.
- One item: push, top, pop, empty.
- Duplicates: values are interchangeable, but the order of identical pops must still hold.
- `pop` and `top` on an empty stack are never called (per the prompt); a real class would raise.
- Two-queue version: after the swap, the new `last` must be the last item moved, so `top()` stays right. When only one item was in `a`, the stack is empty afterwards and `last` is not read.

**Follow-ups:**
- *Amortised O(1) possible?* Not for both calls with queue-only operations; alternating push and pop on a big stack keeps paying O(n). The reverse conversion, queue from two stacks, does get amortised O(1) (see Q3).
- *Which Python container for the queue?* `collections.deque`, so `popleft` is O(1). A list with `pop(0)` would add another O(n) per dequeue (see Q4).
- *Do it with recursion?* The call stack is a stack already, so a "queue from one stack" can use recursion; not asked here, and depth limits apply.

**Common mistakes:**
- Rotating `len` times instead of `len - 1` (the new item goes back behind the old ones, so nothing changes).
- Rotating before enqueuing the new item.
- Forgetting to swap the two queues after a pop in the two-queue version.
- Using `appendleft` or `pop()` on the deque, which breaks the "queue operations only" rule.

### Q15 ⭐⭐ 🟢 Backspace string compare. `s` and `t` are lowercase strings containing '#' (len <= 200), where '#' deletes the previous character if any (and does nothing on an empty text). Return whether the two final texts are equal. Give the stack version, then the O(1)-space version that scans both strings from the right, counting pending backspaces. Example: ('ab#c','ad#c') -> True; ('ab##','c#d#') -> True; ('a#c','b') -> False; ('a##c','#a#c') -> True.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Stack as an undo buffer, then the same idea with O(1) space by scanning from the right. A `#` is a pending deletion that only affects what is to its left, so right-to-left lets you count deletions and skip.

**Say this first (1 line):** "Build each final text with a stack: push letters, pop on `#` if the stack is not empty, compare the two stacks. O(n) time, O(n) space. For O(1) space, walk both strings from the right counting pending backspaces."

**Brute force:** Type the keystrokes into a string: for each char, append it, or on `#` drop the last character if there is one (`out[:-1]`). Compare the two strings. It is O(n^2) in the worst case because slicing copies, but at length 200 that does not matter. It is my checker.

**Optimal:**
- *Stack version:* `push` a letter; on `#` pop only if the stack is non-empty (a backspace on an empty text does nothing). Compare the two lists. O(n) time, O(n) space.
- *Two-pointer version, O(1) space:*
  - Start `i` at the end of `s`, `j` at the end of `t`.
  - `next_valid(s, i)`: walk left with a counter `skip`. A `#` does `skip += 1`. A letter with `skip > 0` is deleted, so `skip -= 1`. A letter with `skip == 0` survives; return its index.
  - Move both to their next surviving letters. Both exhausted: equal. One exhausted or letters differ: not equal. Otherwise step both left and repeat.
  - Invariant: everything to the right of `i` (and `j`) has already matched, with all its deletions applied.
- Why right to left works: a `#` only deletes characters before it, so when I reach a position from the right I already know whether it is deleted.

**Complexity:** Stack: time O(len(s) + len(t)), space O(len(s) + len(t)). Two pointers: time O(len(s) + len(t)) since each index is visited once, space O(1) (a few integers).

**Dry run:** `('ab#c', 'ad#c')`
- Stack for `s`: push a, push b, `#` pops b, push c: `[a, c]`. Stack for `t`: a, d, pop d, c: `[a, c]`. Equal: True.
- Two pointers: `i = 3`, `j = 3`: both `c`, match. Step to `i = 2`, `j = 2`. In `s`: `#` (skip 1), `b` deleted (skip 0), `a` survives at 0. In `t`: `#`, `d` deleted, `a` survives at 0. Match. Step to -1 and -1: both exhausted, True.

**Code:**
```python
import itertools


def build_brute(s):
    # reference: apply the keystrokes to a text, '#' deletes the last char if there is one
    out = ""
    for c in s:
        out = out[:-1] if c == "#" else out + c
    return out


def same_brute(s, t):
    return build_brute(s) == build_brute(t)


def build_stack(s):
    st = []
    for c in s:
        if c != "#":
            st.append(c)
        elif st:                 # '#' on an empty text does nothing
            st.pop()
    return st


def same_stack(s, t):
    return build_stack(s) == build_stack(t)


def next_valid(s, i):
    """Index of the next surviving character at or left of i (or -1), skipping deleted ones."""
    skip = 0
    while i >= 0:
        if s[i] == "#":
            skip += 1
        elif skip:
            skip -= 1            # this character is deleted by a pending '#'
        else:
            return i
        i -= 1
    return -1


def same_two_pointer(s, t):
    i, j = len(s) - 1, len(t) - 1
    while True:
        i, j = next_valid(s, i), next_valid(t, j)
        if i < 0 and j < 0:
            return True          # both exhausted together
        if i < 0 or j < 0 or s[i] != t[j]:
            return False
        i -= 1
        j -= 1


examples = [(("ab#c", "ad#c"), True), (("ab##", "c#d#"), True), (("a#c", "b"), False), (("a##c", "#a#c"), True)]
for (s, t), want in examples:
    got = same_stack(s, t)
    assert got == same_two_pointer(s, t) == same_brute(s, t) == want, (s, t)
    print((s, t), "->", got)

assert same_stack("", "") and same_two_pointer("", "")
assert same_stack("#", "") and same_two_pointer("#", "")          # '#' on empty text
assert same_stack("###", "") and same_two_pointer("###", "")
assert not same_stack("a", "") and not same_two_pointer("a", "")
assert same_stack("a#", "#") and same_two_pointer("a#", "#")
assert not same_stack("ab", "a") and not same_two_pointer("ab", "a")
assert same_stack("a" * 200, "a" * 200) and same_two_pointer("a" * 200, "a" * 200)
assert same_two_pointer("a" * 100 + "#" * 100, "")

# exhaustive over alphabet 'ab#', every string up to length 5 (364 strings, all pairs)
strings = [""]
for n in range(1, 6):
    strings += ["".join(p) for p in itertools.product("ab#", repeat=n)]
pairs = 0
for s in strings:
    for t in strings:
        want = same_brute(s, t)
        assert same_stack(s, t) == want and same_two_pointer(s, t) == want, (s, t)
        pairs += 1
print("exhaustive cross-check passed:", len(strings), "strings,", pairs, "pairs")
```

**Output (my run):**
```
('ab#c', 'ad#c') -> True
('ab##', 'c#d#') -> True
('a#c', 'b') -> False
('a##c', '#a#c') -> True
exhaustive cross-check passed: 364 strings, 132496 pairs
```
All four examples in the prompt are correct. The exhaustive check compares all 132,496 pairs of strings of length up to 5 over `a`, `b`, `#` against the brute force.

**Edge cases:**
- `#` on an empty text does nothing (`'#'` equals `''`, `'a##'` equals `''`).
- Both empty, or one empty and one all-deleted (`'a#'` versus `'#'`): equal.
- One string longer after deletions (`'ab'` versus `'a'`): the two-pointer version must detect "one exhausted, the other not".
- Many `#` in a row at the front of the string.
- Length 200: trivial for either version.

**Follow-ups:**
- *Why not process left to right in O(1) space?* A letter's fate depends on `#` signs that come later, so you cannot decide as you go.
- *What if `#` were a "delete next char" key?* Different structure; you would scan left to right with a skip counter.
- *What if `s` and `t` are huge?* The two-pointer version never builds a copy; it only keeps two indices.

**Common mistakes:**
- Popping an empty stack and getting `IndexError`.
- In the two-pointer version, returning as soon as one pointer is exhausted without checking the other.
- Resetting `skip` wrongly after a surviving character (it must already be 0 there).
- Comparing the raw strings or stack sizes only.

### Q16 ⭐⭐ 🟡 Remove adjacent duplicates. Part (a): remove any two equal adjacent letters repeatedly from lowercase `s` (len <= 10^5) until none remain, and return the result. Part (b): given an integer k >= 2, repeatedly remove k equal adjacent letters; store (letter, run count) pairs on the stack. Say why the removal order does not change the final string. Example: (a) 'abbaca' -> 'ca'; (a) 'azxxzy' -> 'ay'; (b) ('deeedbbcccbdaa', 3) -> 'aa'; (b) ('pbbcggttciiippooaais', 2) -> 'ps'.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports

**Pattern:** Stack as a "collapse as you read" buffer. The top of the stack is the only place a new letter can interact with old ones, so one left-to-right pass is enough.

**Say this first (1 line):** "A stack of letters for pairs, a stack of (letter, run length) for blocks of k. Push, and when the top run reaches k, pop it. One pass, O(n)."

**Brute force:** Repeat: scan for a block of k equal adjacent letters, delete it, start again. Each scan is O(n) and there can be O(n / k) rounds, so O(n^2) in the worst case. It is my checker, and I also run it picking a random removable block each time to test the order claim.

**Optimal:**
- *(a) pairs:* if the top equals the new letter, pop it (the pair cancels); else push.
- *(b) blocks of k:* the stack holds `[letter, count]` pairs.
  - New letter equals the top letter: `count += 1`. If `count == k`, pop that pair (the block cancels).
  - Else push `[letter, 1]`.
  - At the end, rebuild the string from the surviving pairs.
- Part (a) is just part (b) with k = 2.
- Invariant: the stack always holds the fully reduced version of the prefix read so far, with no run reaching k.
- After a pop, the new top may now be adjacent to the next letter. That is handled for free, because the next letter is compared with whatever is on top.
- A run longer than k (like `aaaa` with k = 3) works: the count hits 3, the pair pops, and the 4th `a` starts a fresh pair, leaving one `a`.
- Why the order of removals does not change the answer: if two removable blocks overlap, they lie inside one run of the same letter, and removing either leaves the same string. If they are disjoint, they can be removed in either order. Removal always shortens the string, so it terminates; local order-independence plus termination gives one final string (this is the confluence argument, Newman's lemma). My run also checks it: three random removal orders per input all gave the stack's answer.

**Complexity:** Time O(n): each letter is pushed or counted once and each pair popped at most once. Space O(n) for the stack (the output is at most n letters).

**Dry run:** (b) `('deeedbbcccbdaa', 3)`
| letter read | stack (letter, count) |
|---|---|
| d | d1 |
| e, e | d1 e2 |
| e | e hits 3, popped: d1 |
| d | d2 |
| b, b | d2 b2 |
| c, c, c | c hits 3, popped: d2 b2 |
| b | b hits 3, popped: d2 |
| d | d hits 3, popped: empty |
| a, a | a2 |

Result `'aa'`.

**Code:**
```python
import random


def remove_brute(s, k, rng=None):
    # reference: repeatedly delete a block of k equal adjacent letters.
    # With rng, pick a RANDOM removable block each time (tests order independence);
    # without rng, always take the leftmost block.
    while True:
        spots = [i for i in range(len(s) - k + 1) if s[i:i + k] == s[i] * k]
        if not spots:
            return s
        i = rng.choice(spots) if rng else spots[0]
        s = s[:i] + s[i + k:]


def remove_a(s):
    # part (a): pairs. Stack of letters.
    st = []
    for c in s:
        if st and st[-1] == c:
            st.pop()
        else:
            st.append(c)
    return "".join(st)


def remove_b(s, k):
    # part (b): stack of [letter, run length]; a run that reaches k disappears
    st = []
    for c in s:
        if st and st[-1][0] == c:
            st[-1][1] += 1
            if st[-1][1] == k:
                st.pop()
        else:
            st.append([c, 1])
    return "".join(ch * n for ch, n in st)


examples_a = [("abbaca", "ca"), ("azxxzy", "ay")]
examples_b = [(("deeedbbcccbdaa", 3), "aa"), (("pbbcggttciiippooaais", 2), "ps")]
for s, want in examples_a:
    got = remove_a(s)
    assert got == remove_b(s, 2) == remove_brute(s, 2) == want, (s, got)
    print("(a)", repr(s), "->", repr(got))
for (s, k), want in examples_b:
    got = remove_b(s, k)
    assert got == remove_brute(s, k) == want, (s, k, got)
    print("(b)", (s, k), "->", repr(got))

assert remove_a("") == "" and remove_b("", 3) == ""
assert remove_a("a") == "a" and remove_b("a", 2) == "a"
assert remove_a("aa") == "" and remove_a("aaa") == "a"
assert remove_b("aaaa", 3) == "a"            # a run longer than k leaves a remainder
assert remove_b("aaaaaa", 3) == ""           # two full blocks
assert remove_b("abcd", 2) == "abcd"
assert remove_b("abba", 2) == "" and remove_b("aabbaa", 3) == "aabbaa"
assert remove_b("a" * 100000, 2) == ""       # max size
assert remove_b("ab" * 50000, 2) == "ab" * 50000

rng = random.Random(16)
cases = 0
for _ in range(3000):
    n = rng.randint(0, 14)
    s = "".join(rng.choice("abc") for _ in range(n))
    k = rng.randint(2, 4)
    want = remove_brute(s, k)
    assert remove_b(s, k) == want, (s, k)
    for _ in range(3):                       # any removal order gives the same string
        assert remove_brute(s, k, rng) == want, (s, k)
    if k == 2:
        assert remove_a(s) == want
    cases += 1
print("random cross-check passed:", cases, "cases (3 random removal orders each)")
```

**Output (my run):**
```
(a) 'abbaca' -> 'ca'
(a) 'azxxzy' -> 'ay'
(b) ('deeedbbcccbdaa', 3) -> 'aa'
(b) ('pbbcggttciiippooaais', 2) -> 'ps'
random cross-check passed: 3000 cases (3 random removal orders each)
```
All four examples in the prompt are correct.

**Edge cases:**
- Empty string, one letter: unchanged.
- Whole string cancels (`'abba'`, `'aaaaaa'` with k = 3): result is empty.
- A run longer than k leaves a remainder (`'aaaa'`, k = 3 gives `'a'`).
- Cascading removals: removing the middle block joins two outer blocks (`'abba'`).
- No adjacent equals (`'abcd'`): unchanged.
- Max size 10^5: iterative stack, no recursion, fine.

**Follow-ups:**
- *What if k can be 1?* Every letter vanishes; the statement fixes k >= 2.
- *Can you do it in place?* Yes, with a write pointer over a list of characters and a parallel count array (the stack lives in the front of the same array).
- *Why store counts instead of repeated letters?* Comparing the top run's count is O(1); recounting equal letters on top would make a long run O(n) per step.

**Common mistakes:**
- Checking `count >= k` only at the end instead of popping the moment it reaches k.
- Rebuilding the string with the wrong multiplicity (`ch * n`, not `ch`).
- Forgetting that after a pop the previous run may continue with the next letter.
- Trying to "fix" order by processing right to left; it is not needed.

### Q17 ⭐⭐ 🟡 Minimum removals to make parentheses valid. `s` has lowercase letters and '(' and ')' (len <= 10^5). Remove the fewest parentheses so the rest is balanced and return the resulting string. Match brackets with a stack of indices: a ')' with an empty stack is dropped, and openers left on the stack at the end are dropped; the stack gives one valid answer, but several valid minimal answers can exist (for example 'lee(t(c)o)de)' has three), so any result with the minimum number of removals is accepted and only the removal count is unique. Also say how the count-only variant needs no stack, only two counters. Example: 'lee(t(c)o)de)' -> 'lee(t(c)o)de'; 'a)b(c)d' -> 'ab(c)d'; '))((' -> ''; '(a(b(c)d)' -> 'a(b(c)d)'.
**Asked at:** Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Bracket matching with a stack of indices. Match as you go; whatever cannot be matched is exactly what you must delete.

**Say this first (1 line):** "Stack of indices of `(`. On `)`: pop if the stack has one, else mark this `)` for deletion. At the end, every index still on the stack is an unmatched `(`, so delete those too. One pass, O(n). Heads-up: the minimal answer is not unique, any valid one is fine."

**Brute force:** Try deleting r parentheses for r = 0, 1, 2, ... over every subset of positions, and stop at the first r that gives a balanced string. That is exponential: C(m, r) subsets for m parentheses. It is my checker, and it also lists every valid minimal answer.

**Optimal:**
- Walk the string once. Letters are ignored.
- `(`: push its index.
- `)`: if the stack is non-empty, pop (matched with the nearest open `(`). If empty, this `)` has no opener on its left: add its index to `drop`.
- After the scan, every index left on the stack is a `(` that never found a `)`. Add all of them to `drop`.
- Build the result by skipping the dropped indices.
- Why it is minimal: each dropped bracket is provably unmatched in the greedy matching, and no valid string can keep an unmatched bracket without breaking balance, so you need at least that many deletions. The count of dropped indices equals the minimum (my brute force confirms this).
- Count-only variant, no stack: two counters. `open_` counts unmatched `(` so far; on `)` with `open_ > 0` decrement it, else increment `extra`. Minimum removals = `open_ + extra`. Same logic, you just do not remember which indices.

**A correction to the prompt:** the prompt says the dropped set is unique so the answer is unique. That is not true in general. For `'(a(b(c)d)'` three strings are valid with one deletion: `'a(b(c)d)'`, `'(ab(c)d)'` and `'(a(bc)d)'`. For `'lee(t(c)o)de)'` there are also three. What is unique is the minimum number of deletions, and what is deterministic is the stack algorithm's output (the examples in the prompt are exactly that output). In an interview, say "any valid minimal answer is accepted" and, if the problem needs one specific answer, say which tie rule you use (this one drops the unmatched closers and the leftmost-unmatched openers it finds). The prompt examples themselves are all correct as outputs of this algorithm.

**Complexity:** Time O(n): one scan, plus one pass to rebuild; set membership is O(1). Space O(n) for the stack and the drop set. Count-only variant: O(n) time, O(1) space.

**Dry run:** `'(a(b(c)d)'` (indices 0..8: `(` `a` `(` `b` `(` `c` `)` `d` `)`)
| i | char | action | stack | drop |
|---|---|---|---|---|
| 0 | `(` | push | [0] | {} |
| 2 | `(` | push | [0,2] | {} |
| 4 | `(` | push | [0,2,4] | {} |
| 6 | `)` | pop 4 | [0,2] | {} |
| 8 | `)` | pop 2 | [0] | {} |
| end | | leftover opener 0 goes to drop | [0] | {0} |

Result `'a(b(c)d)'`.

**Code:**
```python
import itertools
import random


def is_valid(t):
    bal = 0
    for c in t:
        if c == "(":
            bal += 1
        elif c == ")":
            bal -= 1
            if bal < 0:
                return False
    return bal == 0


def all_best_brute(s):
    # reference: try deleting r parentheses for r = 0, 1, 2, ...; the first r that works is minimal.
    # Returns the SET of all valid strings reachable with that minimum number of deletions.
    spots = [i for i, c in enumerate(s) if c in "()"]
    for r in range(len(spots) + 1):
        found = set()
        for drop in itertools.combinations(spots, r):
            d = set(drop)
            t = "".join(c for i, c in enumerate(s) if i not in d)
            if is_valid(t):
                found.add(t)
        if found:
            return r, found


def min_remove(s):
    stack = []                 # indices of '(' still waiting for a ')'
    drop = set()
    for i, c in enumerate(s):
        if c == "(":
            stack.append(i)
        elif c == ")":
            if stack:
                stack.pop()    # matched
            else:
                drop.add(i)    # closer with nothing to close: drop it
    drop.update(stack)         # openers never closed: drop them
    return "".join(c for i, c in enumerate(s) if i not in drop)


def min_remove_count(s):
    # count-only variant: no stack, two counters
    open_, extra = 0, 0
    for c in s:
        if c == "(":
            open_ += 1
        elif c == ")":
            if open_:
                open_ -= 1
            else:
                extra += 1
    return open_ + extra


examples = [("lee(t(c)o)de)", "lee(t(c)o)de"), ("a)b(c)d", "ab(c)d"), ("))((", ""), ("(a(b(c)d)", "a(b(c)d)")]
for s, want in examples:
    got = min_remove(s)
    r, best = all_best_brute(s)
    assert got == want and got in best and is_valid(got), (s, got)
    assert len(s) - len(got) == r == min_remove_count(s)
    print(repr(s), "->", repr(got), "| removals:", r, "| valid answers of that size:", sorted(best))

assert min_remove("") == "" and min_remove("abc") == "abc"
assert min_remove("(") == "" and min_remove(")") == ""
assert min_remove("()") == "()" and min_remove(")(") == ""
assert min_remove("((()))") == "((()))"
assert min_remove("(" * 50000 + ")" * 50000) == "(" * 50000 + ")" * 50000
assert min_remove(")" * 50000 + "(" * 50000) == ""

# exhaustive over alphabet 'a()', every string up to length 8
checked, multi = 0, 0
for n in range(0, 9):
    for tup in itertools.product("a()", repeat=n):
        s = "".join(tup)
        got = min_remove(s)
        r, best = all_best_brute(s)
        assert got in best and len(s) - len(got) == r == min_remove_count(s), s
        checked += 1
        multi += len(best) > 1
print("exhaustive check passed:", checked, "strings;", multi, "of them have more than one valid minimal answer")

rng = random.Random(17)
for _ in range(500):
    s = "".join(rng.choice("ab(()") for _ in range(rng.randint(0, 11)))
    r, best = all_best_brute(s)
    assert min_remove(s) in best and is_valid(min_remove(s))
print("random cross-check passed: 500 cases")
```

**Output (my run):**
```
'lee(t(c)o)de)' -> 'lee(t(c)o)de' | removals: 1 | valid answers of that size: ['lee(t(c)o)de', 'lee(t(c)ode)', 'lee(t(co)de)']
'a)b(c)d' -> 'ab(c)d' | removals: 1 | valid answers of that size: ['ab(c)d']
'))((' -> '' | removals: 4 | valid answers of that size: ['']
'(a(b(c)d)' -> 'a(b(c)d)' | removals: 1 | valid answers of that size: ['(a(bc)d)', '(ab(c)d)', 'a(b(c)d)']
exhaustive check passed: 9841 strings; 2615 of them have more than one valid minimal answer
random cross-check passed: 500 cases
```
All four examples in the prompt are correct as outputs of the stack algorithm. The output shows that each is one of possibly several valid minimal answers (the prompt's "answer is unique" sentence is wrong, see above). The exhaustive run over every string on the alphabet `a`, `(`, `)` up to length 8 found 2,615 of 9,841 strings with more than one valid minimal answer.

**Edge cases:**
- No parentheses: unchanged. Empty string: empty.
- Only closers, only openers: all removed.
- `')('`: both removed, result empty (order matters, not just counts).
- Already valid: unchanged.
- Letters between brackets are kept untouched.
- Max size 10^5: iterative, fine.

**Follow-ups:**
- *Can you do it with two passes and no stack of indices?* Yes: a left-to-right pass drops unmatched `)` using a counter; a right-to-left pass on the result drops unmatched `(` the same way. O(1) extra space besides the output.
- *Count only?* Two counters, shown above.
- *Why not just count and delete the last `(` characters?* The opener must be the unmatched one, not just any; deleting the wrong one can leave a `)` unmatched.

**Common mistakes:**
- Forgetting the leftover openers on the stack after the scan.
- Popping an empty stack on `)`.
- Pushing characters instead of indices, so you cannot tell what to delete.
- Building the output with `str.replace`, which removes every occurrence.
- Claiming the answer is unique and "proving" it.

### Q18 ⭐⭐ 🟡 Online stock span. Build a class with `next(price)` that is called once per day and returns the span: the number of consecutive days ending today (including today) with price at most today's price. Up to 10^4 calls. Keep a stack of (price, span) pairs and merge the spans of every smaller-or-equal pair on top; show the amortised O(1) per call and how this is the 'previous greater element' computation. Example: prices 100,80,60,70,60,75,85 -> [1,1,1,2,1,4,6]; prices 7,7,7 -> [1,2,3].
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Monotonic stack on a stream, "previous greater element" in disguise. The span of today is today's index minus the index of the nearest earlier day with a strictly higher price.

**Say this first (1 line):** "Keep a stack of (price, span) with strictly decreasing prices. A new price absorbs the spans of every smaller-or-equal price on top, then pushes itself with the total. Amortised O(1) per call."

**Brute force:** Store all prices. On each call walk backwards while the price is at most today's, counting days. O(n) per call, O(n^2) over n calls; O(n) space. It is my checker.

**Optimal:**
- Stack entries are `(price, span)`: the price, and how many consecutive days ending on that day had price at most that one.
- On `next(price)`: `span = 1`. While the top price is `<= price`, pop it and add its span to `span`. Then push `(price, span)` and return `span`.
- Why adding the popped span is right: the popped entry already says "the span-many days ending there are all `<=` its price", and its price is `<=` today's, so all those days are `<=` today's too. No need to look at them again.
- The loop stops at the first strictly greater price: that is the previous greater element, which is the left boundary of the span.
- Invariant: prices on the stack are strictly decreasing from bottom to top, and the spans on the stack add up to the number of days seen so far (the entries tile the history).
- Ties: `<=` in the pop condition, so equal prices merge. That is why `7, 7, 7` gives `1, 2, 3`.

**Complexity:** Time: each call pushes once, and each entry is popped at most once, so n calls do at most n pops. That is O(1) amortised per call (one call can cost O(n), for example a record-high price after a long decline). Space O(n) in the worst case, a strictly decreasing stream; O(1) extra per call.

**Dry run:** prices `100, 80, 60, 70, 60, 75, 85`
| call | pops | pushed (price, span) | stack after | returns |
|---|---|---|---|---|
| 100 | none | (100, 1) | [(100,1)] | 1 |
| 80 | none | (80, 1) | [(100,1),(80,1)] | 1 |
| 60 | none | (60, 1) | [(100,1),(80,1),(60,1)] | 1 |
| 70 | (60,1) | (70, 2) | [(100,1),(80,1),(70,2)] | 2 |
| 60 | none | (60, 1) | [(100,1),(80,1),(70,2),(60,1)] | 1 |
| 75 | (60,1), (70,2) | (75, 4) | [(100,1),(80,1),(75,4)] | 4 |
| 85 | (75,4), (80,1) | (85, 6) | [(100,1),(85,6)] | 6 |

**Code:**
```python
import random


class StockSpannerBrute:
    def __init__(self):
        self.prices = []

    def next(self, price):
        self.prices.append(price)
        span = 0
        for p in reversed(self.prices):      # walk back while price <= today's
            if p > price:
                break
            span += 1
        return span


class StockSpanner:
    def __init__(self):
        self.stack = []                      # (price, span), prices strictly decreasing bottom to top

    def next(self, price):
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]      # absorb the whole span of a smaller-or-equal price
        self.stack.append((price, span))
        return span


def run(cls, prices):
    s = cls()
    return [s.next(p) for p in prices]


examples = [([100, 80, 60, 70, 60, 75, 85], [1, 1, 1, 2, 1, 4, 6]), ([7, 7, 7], [1, 2, 3])]
for prices, want in examples:
    got = run(StockSpanner, prices)
    assert got == run(StockSpannerBrute, prices) == want, (prices, got)
    print(prices, "->", got)

assert run(StockSpanner, []) == []
assert run(StockSpanner, [5]) == [1]
assert run(StockSpanner, [1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]     # increasing: span grows
assert run(StockSpanner, [5, 4, 3, 2, 1]) == [1, 1, 1, 1, 1]     # decreasing: always 1
assert run(StockSpanner, [3, 3, 3, 3]) == [1, 2, 3, 4]           # ties are included
n = 10000
assert run(StockSpanner, list(range(n))) == list(range(1, n + 1))  # max calls
assert run(StockSpanner, [10 ** 5] * n)[-1] == n

# the same numbers as "distance to previous strictly greater element"
prices = [100, 80, 60, 70, 60, 75, 85]
prev_greater, st, spans = [], [], []
for i, p in enumerate(prices):
    while st and prices[st[-1]] <= p:
        st.pop()
    prev_greater.append(st[-1] if st else -1)
    st.append(i)
    spans.append(i - prev_greater[-1])
assert spans == run(StockSpanner, prices)
print("span = i - (index of previous strictly greater price):", spans)

rng = random.Random(18)
cases = 0
for _ in range(2000):
    prices = [rng.randint(1, rng.choice([3, 6, 20])) for _ in range(rng.randint(0, 25))]
    assert run(StockSpanner, prices) == run(StockSpannerBrute, prices), prices
    cases += 1
print("random cross-check passed:", cases, "price streams")
```

**Output (my run):**
```
[100, 80, 60, 70, 60, 75, 85] -> [1, 1, 1, 2, 1, 4, 6]
[7, 7, 7] -> [1, 2, 3]
span = i - (index of previous strictly greater price): [1, 1, 1, 2, 1, 4, 6]
random cross-check passed: 2000 price streams
```
Both examples in the prompt are correct. The extra line confirms the previous-greater-element view: span = `i - index of previous strictly greater price`.

**Edge cases:**
- First call: span 1.
- Equal prices: counted (`<=`), so `7, 7, 7` gives 1, 2, 3.
- Strictly increasing stream: span grows by one each day, the stack holds one entry.
- Strictly decreasing stream: every span is 1, the stack grows to n.
- 10^4 calls: trivial.

**Follow-ups:**
- *Offline version (whole array given)?* Compute the previous greater index for every position with an index stack; span = `i - prev`. See the previous/next smaller question for the same idea with the comparison flipped.
- *Strictly lower instead of at most?* Change `<=` to `<`.
- *Why store spans instead of indices?* In an online setting you do not have a global index unless you keep a counter; storing the span avoids it. An index stack works equally well if you keep `i`.

**Common mistakes:**
- Using `<` in the pop test and getting 1 instead of 2 for equal prices.
- Pushing the price without the merged span (always pushing span 1).
- Counting today twice or forgetting to start `span` at 1.
- Recomputing spans by walking back (that is the O(n) brute force).

### Q19 ⭐⭐ 🟡 Previous and next smaller element. For `a` (len <= 10^5, duplicates allowed) return two lists: `prev[i]` is the index of the nearest element to the left that is strictly smaller than a[i] (or -1), and `nxt[i]` is the index of the nearest element to the right strictly smaller than a[i] (or n). Do both in one pass with a stack of increasing values: when a[i] pops an element, i is that element's `nxt`, and the new top is i's `prev`. Say why the strict versus non-strict choice matters for duplicates (it is the tie rule used in the sum-of-subarray-minimums question). Example: [4,5,2,10,8] -> prev [-1,0,-1,2,2], nxt [2,2,5,4,5]; [3,3,3] -> prev [-1,-1,-1], nxt [3,3,3].
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Monotonic stack, nearest smaller element on both sides. An element is popped by the first smaller value on its right; the element left underneath it on the stack is its first smaller value on the left.

**Say this first (1 line):** "One pass with an increasing stack of indices. When a[i] pops j, then i is j's next smaller. After the pops, the top is i's previous smaller. Each index is pushed and popped once, O(n)."

**Brute force:** For each i, scan left until a strictly smaller value, then scan right until a strictly smaller value. O(n^2) time, O(1) extra. It is my checker.

**Optimal:**
- Keep a stack of indices whose values are strictly increasing from bottom to top.
- For each `i`, pop while the top value is `>= a[i]`. After the pops, the top (if any) is strictly smaller than `a[i]`: that is `prev[i]`, or -1 if the stack is empty. Push `i`.
- For each popped `j`:
  - If `a[j] > a[i]`: `i` is the first strictly smaller value to the right of `j`, so `nxt[j] = i`.
  - If `a[j] == a[i]` (a duplicate): `i` is not strictly smaller. But everything between `j` and `i` is larger than `a[j]` (otherwise `j` would already have been popped), so `j`'s next strictly smaller is the same as `i`'s. Record `link[j] = i`, and fill `nxt[j] = nxt[i]` in a right-to-left pass at the end (links always point right, so `nxt[i]` is final before `nxt[j]`).
- Elements never popped have no smaller value to the right: `nxt = n`.
- Why strict versus non-strict matters: this question wants strict on both sides. In sum of subarray minimums, a subarray with two equal minimums must be counted for only one of them, so one side is strict and the other is non-strict (for example previous strictly smaller, next smaller-or-equal). If both are strict, a subarray whose minimum value repeats is counted once per copy; if both are non-strict, it is counted by none. My run shows it: for `[3,3,3]` the next strictly smaller is `[3,3,3]` and the next smaller-or-equal is `[1,2,3]`.
- If the link bookkeeping feels heavy in an interview, run two separate passes (one left-to-right for `prev`, one right-to-left for `nxt`), each with its own strict test. Same O(n).

**Complexity:** Time O(n): each index pushed once and popped once; the link-resolution loop is one more O(n) pass. Space O(n): the stack, the two answers and the link array.

**Dry run:** `[4,5,2,10,8]`
| i | a[i] | pops | prev[i] | stack after |
|---|---|---|---|---|
| 0 | 4 | none | -1 | [0] |
| 1 | 5 | none | 0 | [0,1] |
| 2 | 2 | index 1 (5 > 2): nxt[1] = 2; index 0 (4 > 2): nxt[0] = 2 | -1 | [2] |
| 3 | 10 | none | 2 | [2,3] |
| 4 | 8 | index 3 (10 > 8): nxt[3] = 4 | 2 | [2,4] |

Left on the stack at the end: indices 2 and 4, so `nxt[2] = nxt[4] = 5`. Result: `prev = [-1,0,-1,2,2]`, `nxt = [2,2,5,4,5]`.

**Code:**
```python
import random


def prev_next_brute(a):
    n = len(a)
    prev, nxt = [], []
    for i in range(n):
        j = i - 1
        while j >= 0 and not a[j] < a[i]:     # nearest strictly smaller on the left
            j -= 1
        prev.append(j)
        k = i + 1
        while k < n and not a[k] < a[i]:      # nearest strictly smaller on the right
            k += 1
        nxt.append(k)
    return prev, nxt


def prev_next(a):
    n = len(a)
    prev = [-1] * n
    nxt = [n] * n                 # elements never popped keep n
    link = [-1] * n               # for an equal-value pop: "my answer is the same as that index's"
    stack = []                    # indices, values strictly increasing bottom to top
    for i, x in enumerate(a):
        while stack and a[stack[-1]] >= x:
            j = stack.pop()
            if a[j] > x:
                nxt[j] = i        # x is strictly smaller than a[j]: first one to its right
            else:
                link[j] = i       # equal: j's next strictly smaller is i's next strictly smaller
        prev[i] = stack[-1] if stack else -1   # top is strictly smaller than x
        stack.append(i)
    for j in range(n - 1, -1, -1):             # resolve links right to left (link[j] > j)
        if link[j] != -1:
            nxt[j] = nxt[link[j]]
    return prev, nxt


examples = [([4, 5, 2, 10, 8], ([-1, 0, -1, 2, 2], [2, 2, 5, 4, 5])), ([3, 3, 3], ([-1, -1, -1], [3, 3, 3]))]
for a, want in examples:
    got = prev_next(a)
    assert got == prev_next_brute(a) == want, (a, got)
    print(a, "-> prev", got[0], "nxt", got[1])

assert prev_next([]) == ([], [])
assert prev_next([7]) == ([-1], [1])
assert prev_next([1, 2, 3, 4]) == ([-1, 0, 1, 2], [4, 4, 4, 4])      # increasing
assert prev_next([4, 3, 2, 1]) == ([-1, -1, -1, -1], [1, 2, 3, 4])   # decreasing
assert prev_next([2, 2, 1, 2]) == prev_next_brute([2, 2, 1, 2])      # duplicates around a smaller value
assert prev_next([5] * 100000) == ([-1] * 100000, [100000] * 100000)  # max size, all equal
assert prev_next(list(range(100000))) == (list(range(-1, 99999)), [100000] * 100000)

# the tie rule used for "sum of subarray minimums": left strict, right non-strict (<=)
def next_smaller_or_equal(a):
    n, res, st = len(a), [len(a)] * len(a), []
    for i, x in enumerate(a):
        while st and a[st[-1]] >= x:
            res[st.pop()] = i
        st.append(i)
    return res

print("next strictly smaller        for [3,3,3]:", prev_next([3, 3, 3])[1])
print("next smaller-or-equal        for [3,3,3]:", next_smaller_or_equal([3, 3, 3]))

rng = random.Random(19)
cases = 0
for _ in range(4000):
    a = [rng.randint(0, rng.choice([2, 4, 9])) for _ in range(rng.randint(0, 16))]
    assert prev_next(a) == prev_next_brute(a), a
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
[4, 5, 2, 10, 8] -> prev [-1, 0, -1, 2, 2] nxt [2, 2, 5, 4, 5]
[3, 3, 3] -> prev [-1, -1, -1] nxt [3, 3, 3]
next strictly smaller        for [3,3,3]: [3, 3, 3]
next smaller-or-equal        for [3,3,3]: [1, 2, 3]
random cross-check passed: 4000 cases
```
Both examples in the prompt are correct.

**Edge cases:**
- Empty list, single element (`prev = [-1]`, `nxt = [1]`).
- All equal (`[3,3,3]`): nothing is strictly smaller, so prev all -1 and nxt all n. This is where a wrong tie rule shows up.
- Strictly increasing: every `prev[i] = i - 1`, every `nxt = n`. Strictly decreasing: every `prev = -1`, `nxt[i] = i + 1`.
- Duplicates around a smaller value (`[2,2,1,2]`): the link step matters here.
- Max size 10^5 and all equal: still linear.

**Follow-ups:**
- *Previous/next greater instead?* Flip the comparison (decreasing stack).
- *Use in the sum of subarray minimums?* Contribution of `a[i]` = `a[i] * (i - prev[i]) * (nxt[i] - i)`, with one side non-strict as described above.
- *Why is the top after popping the previous smaller?* Everything between it and `i` was popped, meaning each of those was `>= a[i]`, so none of them is smaller; the top is strictly smaller by the pop condition.

**Common mistakes:**
- Popping with `>` and assigning `prev[i]` from the top: then `prev` can be an equal element, which is wrong for strict.
- Popping with `>=` and setting `nxt[j] = i` for equal values: then `nxt` is "smaller or equal", wrong for strict.
- Resolving links left to right (the target is not final yet).
- Using -1 for "no next" instead of `n`, or the other way round.

### Q20 ⭐⭐ 🟡 Remove k digits. `num` is a string of digits (len <= 10^5, no leading zero unless it is '0') and k is an integer with 0 <= k <= len. Remove exactly k digits so the remaining number is as small as possible; return it without leading zeros, and '0' if nothing remains. Greedy with an increasing stack: while the top is larger than the incoming digit and removals remain, pop; afterwards trim extra from the end and strip leading zeros. Explain why a local pop is globally safe. Example: ('1432219', 3) -> '1219'; ('10200', 1) -> '200'; ('10', 2) -> '0'; ('9', 1) -> '0'; ('112', 1) -> '11'.
**Asked at:** Monotonic-stack pattern guides and practice lists (techinterview.org monotonic-stack pages, Hello Interview monotonic stack page, talentd.in monotonic-stack topic list, a Scribd stack-and-queue list; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial and list content, not verified company reports | Stack and queue question roundups (igotanoffer.com stacks-and-queues list naming bracket balancing and max stack, interviewing.io queue page, educative stack-queue chapter; search snippets only, not opened); prep content, not company reports

**Pattern:** Greedy with an increasing (non-decreasing) monotonic stack. The earliest place where a digit is bigger than the digit after it is the best digit to delete.

**Say this first (1 line):** "Scan left to right with a stack of kept digits. While I still owe deletions and the top is bigger than the new digit, pop it. Push the digit. Leftover deletions come off the end. Strip leading zeros, return '0' if empty. O(n)."

**Brute force:** Try every way to keep `len - k` digits (`itertools.combinations`), convert each to a number, take the minimum. C(n, k) candidates, exponential. It is my checker (comparing as integers handles leading zeros).

**Optimal:**
- With the same number of digits, the smaller number is the one whose first differing digit is smaller. So the leftmost digits matter most.
- Scanning left to right: if the top of the stack is bigger than the incoming digit `d`, then deleting that top makes position `top` hold something smaller (`d` or smaller) than before. That is always at least as good as any deletion further right.
- So: `while k and stack and stack[-1] > d: pop; k -= 1`. Then push `d`.
- Why a local pop is globally safe (exchange argument): suppose an optimal answer keeps the top digit `t` but deletes some digit later. Instead delete `t` and keep that later digit. The first position where the two results differ now holds `d` or smaller instead of `t`, so the new result is no larger. Repeating the swap turns any optimal answer into the greedy one.
- If the scan ends with `k > 0`, the stack is non-decreasing, so the largest digits are at the end: drop `k` digits from the end.
- Leading zeros: `lstrip("0")`; if nothing is left, the answer is `'0'`. A zero is never popped for being a zero (it is smaller than anything, so it pops bigger digits before it, never itself).
- Equal digits are not popped (`>`, not `>=`), because deleting one copy of an equal pair gains nothing.

**Complexity:** Time O(n): each digit is pushed once and popped at most once, so the inner while loop is amortised. The final strip and join are O(n). Space O(n) for the stack.

**Dry run:** `('1432219', 3)`
| digit | pops (k left) | stack after |
|---|---|---|
| 1 | none (3) | 1 |
| 4 | none (3) | 1 4 |
| 3 | pop 4 (2) | 1 3 |
| 2 | pop 3 (1) | 1 2 |
| 2 | none (1) | 1 2 2 |
| 1 | pop 2 (0) | 1 2 1 |
| 9 | none (0) | 1 2 1 9 |

`k = 0`, nothing to trim from the end. Answer `'1219'`.

**Code:**
```python
import itertools
import random


def remove_k_brute(num, k):
    # reference: try every way to keep len - k digits, take the smallest NUMBER
    keep = len(num) - k
    if keep == 0:
        return "0"
    best = min(int("".join(c)) for c in itertools.combinations(num, keep))
    return str(best)


def remove_k(num, k):
    stack = []
    for d in num:
        while k and stack and stack[-1] > d:   # a bigger digit before a smaller one: delete it
            stack.pop()
            k -= 1
        stack.append(d)
    if k:
        stack = stack[: len(stack) - k]        # still owe deletions: drop from the end
    return "".join(stack).lstrip("0") or "0"   # no leading zeros, '0' if nothing is left


examples = [(("1432219", 3), "1219"), (("10200", 1), "200"), (("10", 2), "0"), (("9", 1), "0"), (("112", 1), "11")]
for (num, k), want in examples:
    got = remove_k(num, k)
    assert got == remove_k_brute(num, k) == want, (num, k, got)
    print((num, k), "->", repr(got))

assert remove_k("0", 0) == "0"
assert remove_k("123", 0) == "123"                     # k = 0: unchanged
assert remove_k("123", 3) == "0"                       # k = len: nothing left
assert remove_k("12345", 2) == "123"                   # increasing: trim from the end
assert remove_k("54321", 2) == "321"                   # decreasing: pops everything it can
assert remove_k("100", 1) == "0"                       # leading zeros stripped
assert remove_k("1000", 2) == "0"
assert remove_k("10001", 4) == "0"
assert remove_k("22222", 2) == "222"                   # all equal: nothing pops, trim the end
assert remove_k("9" * 100000, 50000) == "9" * 50000    # max size
assert remove_k("1" + "0" * 99999, 1) == "0"

rng = random.Random(20)
cases = 0
for _ in range(3000):
    n = rng.randint(1, 9)
    num = str(rng.randint(1, 9)) + "".join(rng.choice("0123456789" if rng.random() < .5 else "0129") for _ in range(n - 1))
    if rng.random() < 0.05:
        num = "0"
    k = rng.randint(0, len(num))
    assert remove_k(num, k) == remove_k_brute(num, k), (num, k)
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
('1432219', 3) -> '1219'
('10200', 1) -> '200'
('10', 2) -> '0'
('9', 1) -> '0'
('112', 1) -> '11'
random cross-check passed: 3000 cases
```
All five examples in the prompt are correct.

**Edge cases:**
- `k = 0`: unchanged. `k = len`: nothing left, return `'0'`.
- Non-decreasing digits (`12345`, `22222`): nothing pops, so the `k` deletions come off the end.
- Leading zero after a deletion (`10200`, k = 1 gives `'0200'`, stripped to `'200'`).
- Result all zeros (`'1000'`, k = 2 gives `'00'`, stripped to empty, so return `'0'`).
- Trimming from the end with `stack[:-k]` when `k == 0` would empty the stack: use `stack[: len(stack) - k]`.
- Max size 10^5: Python ints are not used for the result, only strings.

**Follow-ups:**
- *Why not convert to int and compare?* Up to 10^5 digits; the greedy never needs it, and brute force over subsets is exponential anyway.
- *Largest number instead?* Flip the pop condition to `<`.
- *Related problem?* Remove duplicate letters (a later question in this part) uses the same pop-while-better idea, with an extra "does it occur again?" check.

**Common mistakes:**
- Forgetting to trim leftover `k` from the end.
- Using `stack[:-k]` when `k` is 0.
- Forgetting to strip leading zeros, or returning an empty string instead of `'0'`.
- Popping with `>=` (harmless for the value here, but it is not needed and hides intent).
- Popping without checking `k > 0`.

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


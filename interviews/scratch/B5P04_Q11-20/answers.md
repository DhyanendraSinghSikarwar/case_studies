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

### Q17 ⭐⭐ 🟡 Minimum removals to make parentheses valid. `s` has lowercase letters and '(' and ')' (len <= 10^5). Remove the fewest parentheses so the rest is balanced and return the resulting string. Match brackets with a stack of indices: a ')' with an empty stack is dropped, and openers left on the stack at the end are dropped; the set of dropped indices is unique, so the answer is unique. Also say how the count-only variant needs no stack, only two counters. Example: 'lee(t(c)o)de)' -> 'lee(t(c)o)de'; 'a)b(c)d' -> 'ab(c)d'; '))((' -> ''; '(a(b(c)d)' -> 'a(b(c)d)'.
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

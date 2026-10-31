### Q12 ⭐⭐⭐ 🟡 Reservoir sampling with a reservoir of size one, checked exactly. A stream has n items (`stream` is a list of 1 <= n <= 6 integers; values may repeat, so identify items by position). Process them in order keeping one held item: the first item is held at once; for the i-th item (i = 2..n, counting from 1) take the next number d from `draws` (`draws[i - 2]`, with 0 <= d <= i - 1) and replace the held item by the i-th one exactly when d == 0. Return `[held, counts, sequences]`: `held` is the VALUE held at the end for the given `draws` (which has n - 1 numbers); `sequences` is the number of possible draw sequences (1 * 2 * ... * n = n!, counting every choice of every draw); and `counts[t]` is the number of those sequences after which the item at position t (0-indexed) is held. Use the exact counts to show every item is held in (n-1)! of the n! sequences, that is with probability 1/n, and explain it with the product (1/i) * (1 - 1/(i+1)) * ... * (1 - 1/n) = 1/n. State the memory used (one item plus a counter) and why this works when n is unknown in advance. Picking a random element of a set or list you can index is Part 1 Q35 and Part 1 Q47; this question is about a one-pass stream. In the answer include a dry run on the first example and a seeded random cross-check of your solution against enumerating every draw sequence with itertools.product on small inputs. Example: stream=[10, 20, 30], draws=[0, 2] -> [20, [2, 2, 2], 6]; stream=[5], draws=[] -> [5, [1], 1]; stream=[4, 4, 9, 1], draws=[1, 0, 0] -> [1, [6, 6, 6, 6], 24].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Reservoir sampling (Algorithm R) with k = 1. One pass over a stream of unknown length, keep one item.

**Say this first (1 line):** "Keep the first item. For the i-th item, replace the held one with probability 1/i. Item t survives to the end with probability (1/t) x (1 - 1/(t+1)) x ... x (1 - 1/n) = 1/n. Memory is one item and a counter."

**Brute force:** Read the whole stream into a list, then `random.choice`. O(n) memory, and you need n (or the whole stream) first. Not possible for an unbounded stream.

**Optimal:**
- Keep `held` and the counter `i`. Item i is taken when a draw from 0..i-1 equals 0, which has probability 1/i. So item 1 is always taken, item 2 with 1/2, item 3 with 1/3.
- Invariant: after i items, each of the i items seen is held with probability 1/i. Step to i+1: the new item wins with 1/(i+1). An old item stays held with (1/i) x (i/(i+1)) = 1/(i+1). So the invariant holds.
- Exact proof by counting every draw sequence (n! of them: 1 x 2 x ... x n). Item t (counting from 1, t >= 2) must win its own draw (1 way), the earlier draws are free ((t-1)! ways) and every later draw i > t must not be 0 (i-1 ways each, (n-1)!/(t-1)! in all). That is (n-1)! sequences out of n!, so probability 1/n. The enumeration confirms it for every n <= 7.
- Works when n is unknown: nothing in the loop uses n. You can stop at any moment and the held item is uniform over what has been read.

**Complexity:** O(n) time, one pass. O(1) space: one held item and one counter (plus the random generator). The counting table is a proof aid.

**Dry run:** stream [10,20,30], draws [0,2]. Held 10. Item 2 (20): draw 0 equals 0, so held becomes 20. Item 3 (30): draw 2 is not 0, so held stays 20. Result 20. Counts: after item 2 the 2 sequences hold position 0 once and position 1 once. At item 3, old items survive in 2 of 3 draws: [1*2, 1*2] and the new item wins in 2 sequences (total before = 2): [2,2,2] of 6.

**Code:**
```python
import itertools
import math
import random
from fractions import Fraction

random.seed(1312)

def reservoir_one(stream, draws):
    """One pass, one held item plus a counter. i-th item (1-based) replaces the held one iff draw == 0, draw in 0..i-1."""
    held = stream[0]
    for i, x in enumerate(stream[1:], start=2):
        if draws[i - 2] == 0:
            held = x
    return held

def solve(stream, draws):
    n = len(stream)
    held = reservoir_one(stream, draws)
    # exact counts without enumeration: counts after item i; old items survive in (i-1) of i draws
    counts, total = [1], 1
    for i in range(2, n + 1):
        counts = [c * (i - 1) for c in counts] + [total]
        total *= i
    return [held, counts, total]

def brute(stream, draws):
    """Enumerate EVERY draw sequence with itertools.product and count which position is held."""
    n = len(stream)
    cnt, tot = [0] * n, 0
    for ds in itertools.product(*[range(i) for i in range(2, n + 1)]):
        pos = 0
        for i, d in enumerate(ds, start=2):
            if d == 0:
                pos = i - 1
        cnt[pos] += 1
        tot += 1
    pos = 0
    for i, d in enumerate(draws, start=2):
        if d == 0:
            pos = i - 1
    return [stream[pos], cnt, tot]

examples = [
    ([10, 20, 30], [0, 2], [20, [2, 2, 2], 6]),
    ([5], [], [5, [1], 1]),
    ([4, 4, 9, 1], [1, 0, 0], [1, [6, 6, 6, 6], 24]),
]
for s, d, exp in examples:
    got = solve(s, d)
    print(s, d, '->', got)
    assert got == exp and brute(s, d) == exp

# the exact table: every item held in (n-1)! of n! sequences, for every n <= 7 (enumeration, not sampling)
for n in range(1, 8):
    r = brute(list(range(n)), [1] * (n - 1))
    assert r[1] == [math.factorial(n - 1)] * n and r[2] == math.factorial(n), (n, r)
    assert solve(list(range(n)), [1] * (n - 1)) == r
    print('n =', n, 'counts =', r[1], 'of', r[2], '-> probability', Fraction(r[1][0], r[2]))

# the product: (1/i)(1-1/(i+1))...(1-1/n) = 1/n for item i, exactly
for n in range(1, 12):
    for i in range(1, n + 1):
        p = Fraction(1, i)
        for m in range(i + 1, n + 1):
            p *= 1 - Fraction(1, m)
        assert p == Fraction(1, n)
print('product telescopes to 1/n: checked exactly for n <= 11, every i')

# seeded random cross-check (values may repeat; items identified by position)
for _ in range(300):
    n = random.randint(1, 6)
    s = [random.randint(0, 3) for _ in range(n)]
    d = [random.randint(0, i - 1) for i in range(2, n + 1)]
    assert solve(s, d) == brute(s, d)
print('random cross-check ok: 300 cases')

# edge asserts
assert solve([7], []) == [7, [1], 1]
assert solve([1, 2], [0]) == [2, [1, 1], 2] and solve([1, 2], [1]) == [1, [1, 1], 2]
assert reservoir_one(list(range(6)), [1, 1, 1, 1, 1]) == 0      # no draw is 0: the first item stays
assert reservoir_one(list(range(6)), [0, 0, 0, 0, 0]) == 5      # every draw is 0: the last item wins
print('edge asserts ok')
```

**Output (my run):**
```
[10, 20, 30] [0, 2] -> [20, [2, 2, 2], 6]
[5] [] -> [5, [1], 1]
[4, 4, 9, 1] [1, 0, 0] -> [1, [6, 6, 6, 6], 24]
n = 1 counts = [1] of 1 -> probability 1
n = 2 counts = [1, 1] of 2 -> probability 1/2
n = 3 counts = [2, 2, 2] of 6 -> probability 1/3
n = 4 counts = [6, 6, 6, 6] of 24 -> probability 1/4
n = 5 counts = [24, 24, 24, 24, 24] of 120 -> probability 1/5
n = 6 counts = [120, 120, 120, 120, 120, 120] of 720 -> probability 1/6
n = 7 counts = [720, 720, 720, 720, 720, 720, 720] of 5040 -> probability 1/7
product telescopes to 1/n: checked exactly for n <= 11, every i
random cross-check ok: 300 cases
edge asserts ok
```

**Edge cases:**
- n = 1: nothing to draw, the only item is held (`draws` is empty).
- Repeated values: identify items by position. [4,4,9,1] still gives counts [6,6,6,6]; the held VALUE for a given `draws` can repeat, the probabilities are per position.
- All draws nonzero: first item is kept. All draws zero: last item wins.
- Empty stream: undefined (nothing to return); say so.

**Follow-ups:**
- Keep k items? Hold the first k, then for item i draw d in 0..i-1 and replace slot d if d < k (that is probability k/i). Every k-subset is then equally likely (stated here, not run in this answer).
- Stream is weighted? Use keys u^(1/w) and keep the largest (A-Res); out of scope here.
- Random element of a set or list you can index: Part 1 Q35 and Part 1 Q47. This question is the one-pass stream.

**Common mistakes:**
- Replacing with probability 1/n using the final n, which you do not know.
- Using `random.randint(0, i)` for the i-th item (i counted from 0 but 1-based range): off by one and biased.
- Replacing with a fixed probability like 1/2: later items would be over-weighted.

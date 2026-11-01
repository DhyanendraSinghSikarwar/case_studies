# Book 5 Part 13, answers Q11-Q20 (Wave B)

### Q11 ⭐⭐⭐ 🟡 Fisher-Yates shuffle and its exact uniformity (exhaustive check). `n` is an integer with 1 <= n <= 5 and `choices` is a list of n - 1 integers. The shuffle starts from `a = [0, 1, ..., n - 1]` and, for i = n - 1 down to 1, takes the next value j from `choices` (the k-th value, counting from 0, is used at i = n - 1 - k and satisfies 0 <= j <= i) and swaps `a[i]` with `a[j]`. Return `[perm, sequences, distinct, min_count, max_count]`: `perm` is the final list for the given `choices`, and the other four numbers come from running the shuffle on EVERY possible sequence of choices (j ranging over 0..i at each step): the number of sequences, how many different permutations they produce, and the smallest and largest number of sequences that produce one particular permutation. Use that table to prove uniformity: when the table shows every permutation produced by exactly one sequence and each sequence has the same probability 1/(n * (n-1) * ... * 2) = 1/n!, every permutation has probability 1/n!. Explain why the loop must pick j from 0..i (the part not yet fixed) and not from 0..n-1 (the next question measures that bug), and say that CPython's `random.shuffle` runs this loop with `j = randbelow(i + 1)` going from i = len - 1 down to 1. In the answer include a dry run on the first example and a seeded random cross-check of your solution against recursive enumeration of the swap tree on small inputs. Example: n=3, choices=[2, 1] -> [[0, 1, 2], 6, 6, 1, 1]; n=1, choices=[] -> [[0], 1, 1, 1, 1]; n=4, choices=[0, 0, 0] -> [[1, 2, 3, 0], 24, 24, 1, 1]; n=5, choices=[4, 3, 2, 1] -> [[0, 1, 2, 3, 4], 120, 120, 1, 1].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened) | Python random module source (random.py of the installed Python 3.13 read to check the loop; docs not opened)

**Pattern:** Randomised algorithm, uniform permutation. Shrinking "unfixed prefix" plus swap: Fisher-Yates (Knuth shuffle). Proof by counting choice sequences.

**Say this first (1 line):** "Walk i from n-1 down to 1, pick j uniformly in 0..i, swap a[i] and a[j]. That gives n x (n-1) x ... x 2 = n! equally likely choice sequences, and each permutation comes from exactly one sequence, so each has probability 1/n!."

**Brute force:** Build the swap tree: at each i branch on every j in 0..i, recurse, and count the leaves per permutation. That is n! leaves, O(n * n!) work. Fine for n <= 5, and it is the proof, not the shuffle.

**Optimal:**
- The shuffle itself is one backward pass, O(n) time, O(1) extra space, in place.
- Invariant: after the step for i, `a[i]` is final and is a uniformly random pick among the items that were still unfixed. Positions i+1..n-1 never change again.
- Why j must be in 0..i: the part 0..i is the "not yet fixed" part. Choosing from 0..n-1 would swap into the finished suffix and move a fixed item again, which breaks the counting. The sequences then number n^n, and n^n is not divisible by n! in general, so the permutations cannot all get equal counts. (For n = 3 below: 27 sequences over 6 permutations, counts 4 and 5. The next question measures the bug properly.)
- The uniformity proof from the table: the sequence count is `(i+1)` choices at each step, so n! sequences, each of probability 1/(n * (n-1) * ... * 2) = 1/n!. The enumeration shows n! distinct permutations, each from exactly one sequence (min = max = 1). Different sequences give different permutations (the last step fixes a[i], so the permutation determines every j going back), so every permutation has probability exactly 1/n!.
- CPython's `random.shuffle` is this loop: I read the installed 3.13 source, and it runs `for i in reversed(range(1, len(x)))` with `j = randbelow(i + 1)`.

**Complexity:** Shuffle: O(n) time, O(1) extra space, n-1 random draws. The exhaustive table is for proof only: n! sequences, so about n * n! steps, trivial for n <= 5.

**Dry run:** n = 4, choices [0, 0, 0], start [0,1,2,3]. i=3, j=0: swap a[3] and a[0] -> [3,1,2,0]. i=2, j=0 -> [2,1,3,0]. i=1, j=0 -> [1,2,3,0]. Answer [1,2,3,0], matching the example. For n = 3, choices [2,1] every swap is a self-swap, so the result is [0,1,2]. The sequence count is 3 * 2 = 6.

**Code:**
```python
import itertools
import inspect
import math
import random
from collections import Counter

random.seed(1311)

def shuffle_with(n, choices):
    """Fisher-Yates driven by an explicit list of choices: the k-th choice is used at i = n-1-k, 0 <= j <= i."""
    a = list(range(n))
    for k, i in enumerate(range(n - 1, 0, -1)):
        j = choices[k]
        assert 0 <= j <= i
        a[i], a[j] = a[j], a[i]
    return a

def fisher_yates(n, choices):
    """Optimal: run once for the given choices, then run on EVERY choice sequence and tabulate."""
    counts = Counter(tuple(shuffle_with(n, cs))
                     for cs in itertools.product(*[range(i + 1) for i in range(n - 1, 0, -1)]))
    return [shuffle_with(n, choices), sum(counts.values()), len(counts),
            min(counts.values()), max(counts.values())]

def brute(n, choices):
    """Brute force: recursive walk of the swap tree (a branch for every j at every step)."""
    acc = Counter()
    def rec(a, i):
        if i == 0:
            acc[tuple(a)] += 1
            return
        for j in range(i + 1):
            b = a[:]
            b[i], b[j] = b[j], b[i]
            rec(b, i - 1)
    rec(list(range(n)), n - 1)
    a, i = list(range(n)), n - 1
    for c in choices:
        a[i], a[c] = a[c], a[i]
        i -= 1
    return [a, sum(acc.values()), len(acc), min(acc.values()), max(acc.values())]

examples = [
    (3, [2, 1], [[0, 1, 2], 6, 6, 1, 1]),
    (1, [], [[0], 1, 1, 1, 1]),
    (4, [0, 0, 0], [[1, 2, 3, 0], 24, 24, 1, 1]),
    (5, [4, 3, 2, 1], [[0, 1, 2, 3, 4], 120, 120, 1, 1]),
]
for n, ch, exp in examples:
    got = fisher_yates(n, ch)
    print(n, ch, '->', got)
    assert got == exp and brute(n, ch) == exp

# the exhaustive table for every n <= 5: n! sequences, n! distinct perms, each exactly once
for n in range(1, 6):
    r = fisher_yates(n, [0] * (n - 1))
    assert r[1:] == [math.factorial(n)] * 2 + [1, 1], r
    print('n =', n, 'sequences, distinct, min, max =', r[1:])

# seeded random cross-check against the recursive swap tree
for _ in range(300):
    n = random.randint(1, 5)
    ch = [random.randint(0, i) for i in range(n - 1, 0, -1)]
    assert fisher_yates(n, ch) == brute(n, ch)
print('random cross-check ok: 300 cases')

# the wrong loop (j from 0..n-1) on n = 3: 27 equally likely sequences, 6 permutations, NOT uniform
bad = Counter()
for js in itertools.product(range(3), repeat=3):
    a = [0, 1, 2]
    for i, j in enumerate(js):
        a[i], a[j] = a[j], a[i]
    bad[tuple(a)] += 1
print('naive swap-with-any, n=3:', sorted(bad.items()))
assert sum(bad.values()) == 27 and set(bad.values()) == {4, 5}

# does CPython's random.shuffle run this loop? (read from the installed 3.13 source)
src = inspect.getsource(random.Random.shuffle)
print('loop is reversed(range(1, len(x))):', 'reversed(range(1, len(x)))' in src,
      '| uses randbelow(i + 1):', 'randbelow(i + 1)' in src)
assert 'reversed(range(1, len(x)))' in src and 'randbelow(i + 1)' in src

# edge asserts
assert fisher_yates(1, []) == [[0], 1, 1, 1, 1]
assert fisher_yates(2, [0])[0] == [1, 0] and fisher_yates(2, [1])[0] == [0, 1]
print('edge asserts ok')
```

**Output (my run):**
```
3 [2, 1] -> [[0, 1, 2], 6, 6, 1, 1]
1 [] -> [[0], 1, 1, 1, 1]
4 [0, 0, 0] -> [[1, 2, 3, 0], 24, 24, 1, 1]
5 [4, 3, 2, 1] -> [[0, 1, 2, 3, 4], 120, 120, 1, 1]
n = 1 sequences, distinct, min, max = [1, 1, 1, 1]
n = 2 sequences, distinct, min, max = [2, 2, 1, 1]
n = 3 sequences, distinct, min, max = [6, 6, 1, 1]
n = 4 sequences, distinct, min, max = [24, 24, 1, 1]
n = 5 sequences, distinct, min, max = [120, 120, 1, 1]
random cross-check ok: 300 cases
naive swap-with-any, n=3: [((0, 1, 2), 4), ((0, 2, 1), 5), ((1, 0, 2), 5), ((1, 2, 0), 5), ((2, 0, 1), 4), ((2, 1, 0), 4)]
loop is reversed(range(1, len(x))): True | uses randbelow(i + 1): True
edge asserts ok
```

**Edge cases:**
- n = 1: no steps, one sequence, one permutation.
- j == i is a legal self-swap. Leaving it out (Sattolo's variant, j in 0..i-1) gives only cyclic permutations, (n-1)! of them.
- Duplicated values do not matter here: the shuffle moves positions.
- Empty list: the loop body never runs.

**Follow-ups:**
- Shuffle a list in place with the standard library? `random.shuffle(x)`. It is the same loop (read from the 3.13 source), and `random.sample` copies.
- The forward version (i from 0, j in i..n-1) is also uniform. Same proof, mirrored.
- Is `sorted(a, key=lambda _: random.random())` uniform? Only up to ties among the random keys, and it costs O(n log n). Prefer Fisher-Yates.

**Common mistakes:**
- j = randint(0, n-1) at every step: n^n outcomes, provably biased (27 outcomes over 6 permutations for n = 3, counts 4 and 5).
- Off by one: j in 0..i-1 (Sattolo), or an off-by-one on the range of i that skips index 1.
- Proving uniformity by "run it 10000 times and look". Count the sequences instead.

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

### Q13 ⭐⭐⭐ 🟡 Random pick with weights, using prefix sums and bisect. `w` is a list of 1 to 10^4 positive integers with sum(w) <= 10^6, and `rs` is a list of integers with 0 <= r < sum(w). The generator behind the picker produces an integer r uniformly from 0 to sum(w) - 1; the picker must return the index i whose block of numbers contains r, where index i owns the w[i] consecutive values after those owned by the earlier indices. Return `[picks, counts]`: `picks[t]` is the index for `rs[t]`, and `counts[i]` is the number of values r in 0..sum(w)-1 that your rule maps to index i (so a correct rule gives `counts == w`, which is what makes the pick probability w[i] / sum(w) exactly). Build the inclusive prefix sums once and answer each pick with a binary search in O(log n). State exactly which bisect function applies when r is in 0..total-1 (the first index whose prefix sum is strictly greater than r) and why the other one (`bisect_left`) assigns the boundary values to the wrong index, and what changes if r is drawn from 1..total instead. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a linear scan that subtracts weights one by one on small inputs. Example: w=[1, 3], rs=[0, 1, 2, 3] -> [[0, 1, 1, 1], [1, 3]]; w=[5], rs=[0, 4] -> [[0, 0], [5]]; w=[2, 1, 3], rs=[0, 1, 2, 3, 5] -> [[0, 0, 1, 2, 2], [2, 1, 3]].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Prefix sums plus binary search. Map a uniform integer to a weighted index (inverse CDF on integers).

**Say this first (1 line):** "Build inclusive prefix sums once. Draw r uniformly in 0..total-1 and return `bisect_right(prefix, r)`: the first index whose prefix sum is strictly greater than r. Index i then owns exactly w[i] values of r."

**Brute force:** For every pick, walk the weights and subtract: `for i, x in enumerate(w): if r < x: return i; r -= x`. O(n) per pick. Correct and the reference here.

**Optimal:**
- Block i covers the values from prefix[i-1] up to prefix[i]-1 (prefix[-1] taken as 0), which is w[i] numbers. Example w = [2,1,3]: prefix [2,3,6], blocks {0,1}, {2}, {3,4,5}.
- r lands in block i when prefix[i-1] <= r < prefix[i]. The first prefix strictly greater than r is prefix[i]. That is `bisect_right(prefix, r)`.
- Why not `bisect_left`: it returns the first prefix >= r. When r equals a prefix value (r = 2 or 3 above) it returns the previous index, so each boundary value is given to the wrong block. For w = [2,1,3] it counts [3,1,2] instead of [2,1,3].
- If r is drawn from 1..total instead, the blocks are (prefix[i-1], prefix[i]] and `bisect_left` is the right call. Match the function to the range.
- Correctness is shown by counts: for all r in 0..total-1, count how many map to each index; the result equals w, so P(i) = w[i]/total exactly.

**Complexity:** Build O(n). Each pick O(log n) by binary search. Space O(n) for the prefix list. (The counts loop in my code is a checker, O(total log n), not part of the picker.)

**Dry run:** w = [1,3], prefix [1,4], total 4. r=0: first prefix > 0 is 1, index 0. r=1: 1 is not > 1, next prefix 4 > 1, index 1. r=2 and r=3: index 1. Picks [0,1,1,1], counts [1,3] = w.

**Code:**
```python
import bisect
import itertools
import random

random.seed(1313)

def weighted_pick(w, rs):
    """Inclusive prefix sums once, then bisect_right per pick: first index whose prefix sum is > r."""
    pre = list(itertools.accumulate(w))
    total = pre[-1]
    picks = [bisect.bisect_right(pre, r) for r in rs]
    # counts[i] = how many r in 0..total-1 land on i (loop over r only for the check; real pick is O(log n))
    counts = [0] * len(w)
    for r in range(total):
        counts[bisect.bisect_right(pre, r)] += 1
    return [picks, counts]

def brute(w, rs):
    """Linear scan: subtract weights one by one until r falls inside a block."""
    def pick(r):
        for i, x in enumerate(w):
            if r < x:
                return i
            r -= x
    counts = [0] * len(w)
    for r in range(sum(w)):
        counts[pick(r)] += 1
    return [[pick(r) for r in rs], counts]

examples = [
    ([1, 3], [0, 1, 2, 3], [[0, 1, 1, 1], [1, 3]]),
    ([5], [0, 4], [[0, 0], [5]]),
    ([2, 1, 3], [0, 1, 2, 3, 5], [[0, 0, 1, 2, 2], [2, 1, 3]]),
]
for w, rs, exp in examples:
    got = weighted_pick(w, rs)
    print(w, rs, '->', got)
    assert got == exp and brute(w, rs) == exp

# why bisect_left is wrong for r in 0..total-1: boundary values go to the previous index
w = [2, 1, 3]
pre = list(itertools.accumulate(w))
left = [0] * 3
for r in range(sum(w)):
    left[bisect.bisect_left(pre, r)] += 1
print('prefix', pre, 'bisect_left counts', left, '(want', w, ')')
assert left != w and left == [3, 1, 2]

# if r is drawn from 1..total instead, bisect_left is the right one
alt = [0] * 3
for r in range(1, sum(w) + 1):
    alt[bisect.bisect_left(pre, r)] += 1
assert alt == w
print('r in 1..total with bisect_left gives', alt)

# seeded random cross-check against the linear scan
for _ in range(300):
    w = [random.randint(1, 6) for _ in range(random.randint(1, 6))]
    rs = [random.randrange(sum(w)) for _ in range(random.randint(0, 10))]
    assert weighted_pick(w, rs) == brute(w, rs) and weighted_pick(w, rs)[1] == w
print('random cross-check ok: 300 cases (counts == w every time)')

# maximum size: n = 10^4, sum <= 10^6; one prefix build, picks cost O(log n) each
w = [random.randint(1, 100) for _ in range(10 ** 4)]
assert sum(w) <= 10 ** 6
pre = list(itertools.accumulate(w))
assert bisect.bisect_right(pre, 0) == 0 and bisect.bisect_right(pre, sum(w) - 1) == len(w) - 1
print('max size ok: n =', len(w), 'total =', sum(w))

# edge asserts
assert weighted_pick([1], [0]) == [[0], [1]]
assert weighted_pick([1, 1, 1], [0, 1, 2])[0] == [0, 1, 2]
assert weighted_pick([4, 1], [3, 4])[0] == [0, 1]       # r = 3 is the last value of block 0, r = 4 the first of block 1
print('edge asserts ok')
```

**Output (my run):**
```
[1, 3] [0, 1, 2, 3] -> [[0, 1, 1, 1], [1, 3]]
[5] [0, 4] -> [[0, 0], [5]]
[2, 1, 3] [0, 1, 2, 3, 5] -> [[0, 0, 1, 2, 2], [2, 1, 3]]
prefix [2, 3, 6] bisect_left counts [3, 1, 2] (want [2, 1, 3] )
r in 1..total with bisect_left gives [2, 1, 3]
random cross-check ok: 300 cases (counts == w every time)
max size ok: n = 10000 total = 510843
edge asserts ok
```

**Edge cases:**
- Single weight: always index 0.
- r = 0 goes to index 0; r = total-1 goes to the last index (checked at the max size).
- Weights all equal: the picker is uniform.
- Zero weights are excluded by the prompt (positive integers).

**Follow-ups:**
- Update a weight between picks? The prefix list goes stale; a Fenwick tree (Part 14, named only) gives O(log n) update and pick.
- Faster than O(log n) per pick? The alias method gives O(1) per pick after O(n) setup; mention only.
- Float weights? Use `random.random() * total` with `bisect_right`, accept tiny rounding at boundaries, or `random.choices(w_cumulative)`.

**Common mistakes:**
- `bisect_left` with r in 0..total-1 (boundary values go to the previous index, shown above).
- Drawing r in 1..total with `bisect_right`: r = total would return n, out of range.
- Recomputing prefix sums on every pick, which makes it O(n) again.

### Q14 ⭐⭐⭐ 🟡 Python sort stability, key= and reverse=. `records` is a list of 1 to 1000 items [name, dept, score] (name and dept lowercase strings, score an integer with |score| <= 1000; names may repeat). Return four lists of NAMES, each in the order of the records after the sort described: A = one `sorted` call with `key=lambda r: (r[1], -r[2])` (department ascending, score descending); B = two stable passes, first `sort(key=score, reverse=True)` then `sort(key=dept)`; C = `sorted(records, key=dept, reverse=True)`; D = `sorted(records, key=dept)[::-1]`. Return `[A, B, C, D]`. Explain: Python's sort is stable, so records with equal keys keep their input order; that is why two passes (least significant key first) equal the single tuple key and why this is the way to sort by a string descending (strings cannot be negated); and that `reverse=True` preserves the original order of equal elements (it behaves as if the comparisons were reversed, not as if the result were reversed), so C and D differ whenever two records share a department. Mention `functools.cmp_to_key` as the general fallback. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an index-aware manual comparison (original position as the final tie-break) on small inputs. Example: records=[['ann', 'hr', 5], ['bob', 'it', 7], ['cat', 'hr', 5], ['dan', 'it', 9], ['eve', 'hr', 8]] -> [['eve', 'ann', 'cat', 'dan', 'bob'], ['eve', 'ann', 'cat', 'dan', 'bob'], ['bob', 'dan', 'ann', 'cat', 'eve'], ['dan', 'bob', 'eve', 'cat', 'ann']]; records=[['x', 'a', 1]] -> [['x'], ['x'], ['x'], ['x']]; records=[['p', 'b', 2], ['q', 'a', 2], ['r', 'b', 2], ['s', 'a', 3]] -> [['s', 'q', 'p', 'r'], ['s', 'q', 'p', 'r'], ['p', 'r', 'q', 's'], ['r', 'p', 's', 'q']].
**Asked at:** Python Sorting HOWTO (search-result snippets only; the docs.python.org fetch failed with ENOTFOUND, so behaviour was verified by running Python 3.13)

**Pattern:** Python sort stability, `key=`, `reverse=`, and multi-key sorting by passes.

**Say this first (1 line):** "Python's sort is stable, so equal keys keep input order. That makes two passes, least significant key first, equal to one tuple key. `reverse=True` keeps equal items in their original order, so it is not the same as reversing the sorted list."

**Brute force:** Write an explicit comparison that finishes with the original index as a tie-break and sort the indices with `cmp_to_key`. It does not depend on stability at all, and I use it as the reference. Cost: O(n log n) comparisons, each a Python call.

**Optimal:**
- A: `sorted(records, key=lambda r: (r[1], -r[2]))`. One pass, tuple key: dept ascending, score descending. Negating works for numbers only.
- B: sort by score with `reverse=True` first, then by dept. The second pass is stable, so inside each dept the earlier score order survives. Result equals A.
- Strings cannot be negated (`-'hr'` raises TypeError, shown below). For dept DESCENDING with score ascending use two passes: score first, then dept with `reverse=True`. General fallback: `functools.cmp_to_key` with a comparator.
- C: `sorted(records, key=dept, reverse=True)`. Departments descending, and records with the same dept stay in input order, because `reverse=True` behaves as if the comparisons were reversed, not as if the result list were flipped.
- D: `sorted(records, key=dept)[::-1]`. Flips everything, so equal-dept records come out in reverse input order. C and D differ whenever two records share a department (331 of my 400 random cases).
- Pass order matters: least significant key first. Sorting by dept first and score last gives a different list (in the output).

**Complexity:** Each sort is O(n log n) time and O(n) extra space (Timsort). Two passes cost twice that, same big-O. Key functions are called once per record, not per comparison.

**Dry run:** example 1, records ann(hr,5), bob(it,7), cat(hr,5), dan(it,9), eve(hr,8).
- A: keys ann (hr,-5), bob (it,-7), cat (hr,-5), dan (it,-9), eve (hr,-8). hr: eve, ann, cat (ann and cat tie, ann is first in input); it: dan, bob. A = eve, ann, cat, dan, bob.
- B: pass 1 (score desc): dan 9, eve 8, bob 7, ann 5, cat 5. Pass 2 (dept): hr: eve, ann, cat; it: dan, bob. Same as A.
- C: dept desc, input order inside: it: bob, dan; hr: ann, cat, eve.
- D: dept asc gives ann, cat, eve, bob, dan; flipped: dan, bob, eve, cat, ann.

**Code:**
```python
import functools
import random

random.seed(1314)

def four_sorts(records):
    name, dept, score = (lambda r: r[0]), (lambda r: r[1]), (lambda r: r[2])
    A = [r[0] for r in sorted(records, key=lambda r: (r[1], -r[2]))]
    t = list(records)
    t.sort(key=score, reverse=True)        # least significant key first
    t.sort(key=dept)                       # then the most significant key; stability keeps the score order inside a dept
    B = [r[0] for r in t]
    C = [r[0] for r in sorted(records, key=dept, reverse=True)]
    D = [r[0] for r in sorted(records, key=dept)[::-1]]
    return [A, B, C, D]

def brute(records):
    """Index-aware comparison: original position is the final tie-break, so no stability is assumed."""
    idx = list(range(len(records)))
    def cmp_a(i, j):                                   # dept asc, score desc, then position asc
        a, b = records[i], records[j]
        return (a[1] > b[1]) - (a[1] < b[1]) or (b[2] > a[2]) - (b[2] < a[2]) or (i > j) - (i < j)
    def cmp_c(i, j):                                   # dept DESC, position ASC (equal depts keep input order)
        a, b = records[i], records[j]
        return (b[1] > a[1]) - (b[1] < a[1]) or (i > j) - (i < j)
    def cmp_d(i, j):                                   # dept DESC, position DESC (the reversed result)
        a, b = records[i], records[j]
        return (b[1] > a[1]) - (b[1] < a[1]) or (j > i) - (j < i)
    pick = lambda c: [records[i][0] for i in sorted(idx, key=functools.cmp_to_key(c))]
    A = pick(cmp_a)
    return [A, A, pick(cmp_c), pick(cmp_d)]

examples = [
    ([['ann', 'hr', 5], ['bob', 'it', 7], ['cat', 'hr', 5], ['dan', 'it', 9], ['eve', 'hr', 8]],
     [['eve', 'ann', 'cat', 'dan', 'bob'], ['eve', 'ann', 'cat', 'dan', 'bob'],
      ['bob', 'dan', 'ann', 'cat', 'eve'], ['dan', 'bob', 'eve', 'cat', 'ann']]),
    ([['x', 'a', 1]], [['x'], ['x'], ['x'], ['x']]),
    ([['p', 'b', 2], ['q', 'a', 2], ['r', 'b', 2], ['s', 'a', 3]],
     [['s', 'q', 'p', 'r'], ['s', 'q', 'p', 'r'], ['p', 'r', 'q', 's'], ['r', 'p', 's', 'q']]),
]
for rec, exp in examples:
    got = four_sorts(rec)
    print(got)
    assert got == exp and brute(rec) == exp

# C vs D: reverse=True keeps equal records in input order, [::-1] reverses them
two = [['a', 'x', 0], ['b', 'x', 0]]
C, D = four_sorts(two)[2:]
print('two records, same dept: C =', C, ' D =', D)
assert C == ['a', 'b'] and D == ['b', 'a']

# strings cannot be negated: -r[1] raises, so the two-pass trick is the way to get dept DESC + score ASC
try:
    sorted(examples[0][0], key=lambda r: (-r[1], r[2]))
except TypeError as e:
    print('negating a str:', type(e).__name__)
t = list(examples[0][0]); t.sort(key=lambda r: r[2]); t.sort(key=lambda r: r[1], reverse=True)
print('dept desc then score asc via two passes:', [r[0] for r in t])
# the same with cmp_to_key
def cmp(a, b):
    return (b[1] > a[1]) - (b[1] < a[1]) or (a[2] > b[2]) - (a[2] < b[2])
assert [r[0] for r in sorted(examples[0][0], key=functools.cmp_to_key(cmp))] == [r[0] for r in t]

# the pass ORDER matters: dept first then score gives a different answer
wrong = list(examples[0][0]); wrong.sort(key=lambda r: r[1]); wrong.sort(key=lambda r: r[2], reverse=True)
print('wrong pass order:', [r[0] for r in wrong], '(A is', examples[0][1][0], ')')
assert [r[0] for r in wrong] != examples[0][1][0]

# key= is called once per record, not once per comparison
calls = [0]
def counting_key(r):
    calls[0] += 1
    return r[1]
sorted(examples[0][0], key=counting_key)
print('key calls for 5 records:', calls[0])
assert calls[0] == 5

# seeded random cross-check: A == B, all four equal the index-aware comparison
tie_seen = 0
for _ in range(400):
    n = random.randint(1, 12)
    rec = [[random.choice('abcde'), random.choice(['hr', 'it', 'ops']), random.randint(-3, 3)] for _ in range(n)]
    r = four_sorts(rec)
    assert r == brute(rec) and r[0] == r[1]
    if r[2] != r[3]:
        tie_seen += 1
print('random cross-check ok: 400 cases; C != D in', tie_seen, 'of them')

# edge asserts
assert four_sorts([['x', 'a', 1]]) == [['x']] * 4
assert four_sorts([['a', 'z', 1], ['b', 'z', 1]])[0] == ['a', 'b']   # all keys equal: input order survives in A
print('edge asserts ok')
```

**Output (my run):**
```
[['eve', 'ann', 'cat', 'dan', 'bob'], ['eve', 'ann', 'cat', 'dan', 'bob'], ['bob', 'dan', 'ann', 'cat', 'eve'], ['dan', 'bob', 'eve', 'cat', 'ann']]
[['x'], ['x'], ['x'], ['x']]
[['s', 'q', 'p', 'r'], ['s', 'q', 'p', 'r'], ['p', 'r', 'q', 's'], ['r', 'p', 's', 'q']]
two records, same dept: C = ['a', 'b']  D = ['b', 'a']
negating a str: TypeError
dept desc then score asc via two passes: ['bob', 'dan', 'ann', 'cat', 'eve']
wrong pass order: ['dan', 'eve', 'bob', 'ann', 'cat'] (A is ['eve', 'ann', 'cat', 'dan', 'bob'] )
key calls for 5 records: 5
random cross-check ok: 400 cases; C != D in 331 of them
edge asserts ok
```

**Edge cases:**
- Single record: all four lists equal.
- All keys equal: A keeps input order; D reverses it.
- Duplicate names are fine, since only the sort keys decide order.
- Negative scores: `-r[2]` is fine for ints (not for strings, or `bool`/`None` mixes).

**Follow-ups:**
- Why is the key function better than `cmp`? Called once per item, and Python 3 dropped `cmp=`. `cmp_to_key` wraps an old comparison when no key exists.
- Does `list.sort` guarantee stability? Yes, it is documented. The HOWTO page itself could not be fetched, so I verified the behaviour by running 3.13 (the documentation claim is editor knowledge).
- Sort descending but keep ties stable? `sort(key=..., reverse=True)` does that. Do not flip with `[::-1]`.

**Common mistakes:**
- Doing the passes in the wrong order (most significant key first).
- Using `[::-1]` and expecting stability for equal items.
- Trying `-r[1]` on a string key.
- Assuming a stable sort needs `(key, index)` pairs. It does not in Python, and this answer's reference uses them only to avoid assuming it.

### Q15 ⭐⭐⭐ 🟡 Merge sort from scratch, stable, with exact comparison counts. `records` is a list of 0 <= len <= 10^5 items [key, tag] with integer keys (|key| <= 10^9) and any integer tag. Sort them ascending by key, keeping equal keys in input order, without `sorted` or `list.sort`. Use top-down merge sort: split a list of length n at `mid = n // 2` (left part = first n // 2 items), sort both halves, then merge: while both halves have items, make ONE comparison `left.key <= right.key` and take the left item when it is true, else the right item; when one half runs out, append the rest of the other with no comparisons. Return `[sorted_records, comparisons]`, where `comparisons` totals all those key comparisons over the whole sort. Explain why `<=` (not `<`) makes it stable, why the work is O(n log n) in every case and the extra space O(n), and why the recursion depth is about log2 n (under 20 here, so recursion is fine) while a bottom-up version needs no recursion at all (its comparison count can differ from the top-down one). State the worst-case comparison count n * ceil(log2 n) - 2^ceil(log2 n) + 1 and check it by hand for n = 5. In the answer include a dry run on the first example and a seeded random cross-check of your solution against sorted(records, key=lambda r: r[0]) for the order and a separate recursive comparison counter on small inputs. Example: records=[[3, 1], [1, 2], [3, 3], [2, 4], [1, 5]] -> [[[1, 2], [1, 5], [2, 4], [3, 1], [3, 3]], 8]; records=[] -> [[], 0]; records=[[9, 0]] -> [[[9, 0]], 0]; records=[[1, 1], [2, 2], [3, 3], [4, 4]] -> [[[1, 1], [2, 2], [3, 3], [4, 4]], 4].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)

**Pattern:** Divide and conquer: stable merge sort from scratch, with an exact comparison counter.

**Say this first (1 line):** "Split at n // 2, sort both halves, merge with one comparison `left.key <= right.key` per taken item. `<=` takes the left item on ties, which makes it stable. O(n log n) in every case, O(n) extra space."

**Brute force:** Insertion or selection sort, O(n^2) comparisons. Not good for n = 10^5.

**Optimal:**
- Base case: length 0 or 1 is sorted and costs no comparisons.
- Merge: two pointers. Each loop iteration is one comparison and moves one item. When one half is empty, append the rest of the other with no comparisons.
- Stability: on equal keys take the LEFT item, since left items came earlier in the input. With `<` the right item goes first and equal records swap (shown below).
- Every level of the recursion touches n items once, and there are about log2 n levels, so O(n log n) in the best, average and worst case. It needs a temporary list, O(n) extra space.
- Recursion depth is about log2 n, about 17 for n = 10^5, far below CPython's 1000 limit. Bottom-up (widths 1, 2, 4, ...) needs no recursion, but it splits differently (not at n // 2), so its comparison count can differ: for sorted [0,1,2] top-down uses 2 and bottom-up 3 (630 of the permutations with n <= 6 differ).
- Worst case is n * ceil(log2 n) - 2^ceil(log2 n) + 1. By hand for n = 5: 5 * 3 - 8 + 1 = 8. I checked this over all permutations for every n <= 8.

**Complexity:** Time O(n log n), at most 1,700,000 comparisons for n = 10^5 (the random run used 1,536,373). Space O(n) for the merge lists, plus O(log n) for the call stack.

**Dry run:** keys [3,1,3,2,1], split 2 | 3.
- Left half [[3,1],[1,2]]: 3<=1 is false, so the result is [[1,2],[3,1]]: 1 comparison.
- Right half [[3,3],[2,4],[1,5]] splits 1 | 2. [[2,4],[1,5]] costs 1 and gives [[1,5],[2,4]]. Merge [[3,3]] with it: 3<=1 no, 3<=2 no, then append [3,3]: 2 comparisons. Right total 3.
- Final merge of keys [1,3] with [1,2,3]: 1<=1 yes (take [1,2]), 3<=1 no (take [1,5]), 3<=2 no (take [2,4]), 3<=3 yes (take [3,1]), left empty, append [3,3]: 4 comparisons.
- Total 1 + 3 + 4 = 8, and equal keys keep input order: [1,2] before [1,5], [3,1] before [3,3].

**Code:**
```python
import itertools
import math
import random

random.seed(1315)

def merge_sort(records):
    """Top-down, split at n // 2, one comparison left.key <= right.key per taken item while both halves have items."""
    cmps = 0
    def sort(a):
        nonlocal cmps
        n = len(a)
        if n <= 1:
            return a
        mid = n // 2
        left, right = sort(a[:mid]), sort(a[mid:])
        out, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            cmps += 1
            if left[i][0] <= right[j][0]:          # <= takes the LEFT item on ties: that is stability
                out.append(left[i]); i += 1
            else:
                out.append(right[j]); j += 1
        out.extend(left[i:]); out.extend(right[j:])   # leftovers: no comparisons
        return out
    res = sort([list(r) for r in records])
    return [res, cmps]

def brute(records):
    """Reference: sorted() for the order (stable) and a separate recursive counter over index ranges."""
    recs = [list(r) for r in records]
    def go(lo, hi):
        if hi - lo <= 1:
            return recs[lo:hi], 0
        mid = lo + (hi - lo) // 2
        (L, a), (R, b) = go(lo, mid), go(mid, hi)
        c, out = a + b, []
        while L and R:
            c += 1
            out.append(L.pop(0) if L[0][0] <= R[0][0] else R.pop(0))
        return out + L + R, c
    _, c = go(0, len(recs))
    return [sorted(recs, key=lambda r: r[0]), c]

def bottom_up_cmps(keys):
    """Bottom-up (width 1, 2, 4, ...): no recursion, but a different split, so the count can differ."""
    a = [[k, 0] for k in keys]; width = 1; cmps = 0
    while width < len(a):
        nxt = []
        for lo in range(0, len(a), 2 * width):
            L, R = a[lo:lo + width], a[lo + width:lo + 2 * width]
            i = j = 0
            while i < len(L) and j < len(R):
                cmps += 1
                if L[i][0] <= R[j][0]: nxt.append(L[i]); i += 1
                else: nxt.append(R[j]); j += 1
            nxt.extend(L[i:]); nxt.extend(R[j:])
        a, width = nxt, width * 2
    return cmps

examples = [
    ([[3, 1], [1, 2], [3, 3], [2, 4], [1, 5]], [[[1, 2], [1, 5], [2, 4], [3, 1], [3, 3]], 8]),
    ([], [[], 0]),
    ([[9, 0]], [[[9, 0]], 0]),
    ([[1, 1], [2, 2], [3, 3], [4, 4]], [[[1, 1], [2, 2], [3, 3], [4, 4]], 4]),
]
for rec, exp in examples:
    got = merge_sort(rec)
    print(rec, '->', got)
    assert got == exp and brute(rec) == exp

# worst case n*ceil(log2 n) - 2^ceil(log2 n) + 1, exhaustive over all permutations for n <= 8; by hand n = 5: 5*3 - 8 + 1 = 8
for n in range(1, 9):
    worst = max(merge_sort([[v, 0] for v in p])[1] for p in itertools.permutations(range(n)))
    c = math.ceil(math.log2(n))
    assert worst == n * c - 2 ** c + 1, (n, worst)
    print('n =', n, 'worst comparisons over all', math.factorial(n), 'permutations =', worst, '= formula', n * c - 2 ** c + 1)

# bottom-up can differ from top-down (n = 3 sorted input: top-down splits 1|2, bottom-up merges 2 then 1)
diff = [(p, merge_sort([[v, 0] for v in p])[1], bottom_up_cmps(p))
        for n in range(2, 7) for p in itertools.permutations(range(n)) if merge_sort([[v, 0] for v in p])[1] != bottom_up_cmps(p)]
print('bottom-up differs from top-down for', len(diff), 'permutations with n <= 6; first:', diff[0])
assert diff

# the '<' variant is unstable: equal keys come out reversed
def merge_lt(a, b):
    out = []
    while a and b:
        out.append(a.pop(0) if a[0][0] < b[0][0] else b.pop(0))
    return out + a + b
print('with < the two 5s come out as', [r[1] for r in merge_lt([[5, 'first']], [[5, 'second']])])
assert [r[1] for r in merge_lt([[5, 'first']], [[5, 'second']])] == ['second', 'first']

# seeded random cross-check (order AND count vs the separate counter)
for _ in range(400):
    rec = [[random.randint(0, 4), random.randint(0, 9)] for _ in range(random.randint(0, 30))]
    assert merge_sort(rec) == brute(rec)
print('random cross-check ok: 400 cases')

# maximum size: n = 10^5, comparisons <= n * ceil(log2 n)
rec = [[random.randint(-10 ** 9, 10 ** 9), i] for i in range(10 ** 5)]
out, c = merge_sort(rec)
assert out == sorted(rec, key=lambda r: r[0]) and c <= 10 ** 5 * math.ceil(math.log2(10 ** 5))
print('n = 10^5: ok, comparisons', c, '<= n*ceil(log2 n) =', 10 ** 5 * 17)

# edge asserts
assert merge_sort([[2, 0], [2, 1], [2, 2]]) == [[[2, 0], [2, 1], [2, 2]], 2]   # all equal: input order kept; split 1|2 costs 1 + 1
assert merge_sort([[1, 0], [2, 1]])[1] == 1
print('edge asserts ok')
```

**Output (my run):**
```
[[3, 1], [1, 2], [3, 3], [2, 4], [1, 5]] -> [[[1, 2], [1, 5], [2, 4], [3, 1], [3, 3]], 8]
[] -> [[], 0]
[[9, 0]] -> [[[9, 0]], 0]
[[1, 1], [2, 2], [3, 3], [4, 4]] -> [[[1, 1], [2, 2], [3, 3], [4, 4]], 4]
n = 1 worst comparisons over all 1 permutations = 0 = formula 0
n = 2 worst comparisons over all 2 permutations = 1 = formula 1
n = 3 worst comparisons over all 6 permutations = 3 = formula 3
n = 4 worst comparisons over all 24 permutations = 5 = formula 5
n = 5 worst comparisons over all 120 permutations = 8 = formula 8
n = 6 worst comparisons over all 720 permutations = 11 = formula 11
n = 7 worst comparisons over all 5040 permutations = 14 = formula 14
n = 8 worst comparisons over all 40320 permutations = 17 = formula 17
bottom-up differs from top-down for 630 permutations with n <= 6; first: ((0, 1, 2), 2, 3)
with < the two 5s come out as ['second', 'first']
random cross-check ok: 400 cases
n = 10^5: ok, comparisons 1536373 <= n*ceil(log2 n) = 1700000
edge asserts ok
```

**Edge cases:**
- Empty list and single item: zero comparisons.
- Already sorted input: still about (n/2) log2 n comparisons, never O(n). This plain merge sort is not adaptive (Timsort is).
- All equal keys: order unchanged, and with n = 3 it costs 2.
- Keys at +-10^9: Python ints, no overflow.

**Follow-ups:**
- Merge sort a linked list? It is the natural fit (O(1) extra space for the merge): Part 6 Q25 (heading as given).
- Why is merge sort used for objects and quicksort for primitives in some languages? Stability and the worst case against cache-friendly in-place partitioning. General statement, not tested here.
- Count inversions during the merge: Q17 in this part.

**Common mistakes:**
- `<` in the merge, which breaks stability.
- Slicing `a[:mid]` and `a[mid:]` and calling it O(1): slicing copies, which is fine for O(n) per level, but say it.
- Counting leftovers as comparisons.
- Believing the worst case is n log2 n exactly: it is n * ceil(log2 n) - 2^ceil(log2 n) + 1.

### Q16 ⭐⭐⭐ 🟡 Quicksort with the Lomuto partition, iteratively, with exact counts. `nums` has 1 <= len <= 3000 integers (duplicates allowed). Sort them ascending in place with quicksort WITHOUT recursion (use an explicit stack; sorted input of length 1500 makes this recursion nest about 1500 frames, above CPython's default recursion limit of 1000, so a recursive solution fails with RecursionError). Partition a range [lo, hi] with the last element as the pivot: `p = a[hi]; i = lo`; for j in lo..hi-1 do ONE comparison `a[j] < p` and, if true, swap `a[i]` and `a[j]` and do `i += 1`; finally swap `a[i]` with `a[hi]` and recurse (conceptually) on [lo, i - 1] and [i + 1, hi], skipping ranges with fewer than 2 items. Return `[sorted_list, comparisons, depth]`: `comparisons` is the total number of those `a[j] < p` tests, and `depth` is the largest number of nested partition calls the recursive version would reach (the first call counts 1; both are independent of the order in which you process the stack). Explain why an already sorted or all-equal input costs n * (n - 1) / 2 comparisons with depth n - 1 for this pivot rule, why a random pivot makes that unlikely, and why quicksort is not stable. Kth-largest by quickselect is Part 8 Q36; this question is the full sort. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a recursive Lomuto quicksort (small inputs only) and sorted() on small inputs. Example: nums=[3, 1, 2] -> [[1, 2, 3], 2, 1]; nums=[1, 2, 3, 4] -> [[1, 2, 3, 4], 6, 3]; nums=[5, 5, 5] -> [[5, 5, 5], 3, 2]; nums=[4, 2, 7, 1, 9, 3] -> [[1, 2, 3, 4, 7, 9], 8, 2].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)

**Pattern:** Quicksort with the Lomuto partition, made iterative with an explicit stack. Partition around a pivot, then handle both sides.

**Say this first (1 line):** "Pivot is the last element. One pass puts everything smaller than the pivot on the left, the pivot goes to its final slot, then I sort both sides. I use an explicit stack because sorted input nests n frames, and CPython stops at 1000."

**Brute force:** Insertion sort, O(n^2). Or recursive Lomuto quicksort, same algorithm with the call stack: correct on small inputs, but it raises `RecursionError` at n = 1500 sorted (shown in my run).

**Optimal:**
- Partition [lo, hi]: `p = a[hi]`, `i = lo`. For j in lo..hi-1: one comparison `a[j] < p`; if true swap a[i], a[j] and i += 1. Finally swap a[i] and a[hi]. Invariant: a[lo..i-1] < p and a[i..j] >= p.
- Push the two sub-ranges (only if they have at least 2 items) onto a stack of (lo, hi, depth). Popping order does not change the totals: each range is partitioned exactly once, so comparisons and depth do not depend on the order.
- Comparisons per partition = size - 1. Sorted or all-equal input: every partition peels off just the pivot (all equal items are `>= p`, so none moves), so sizes n, n-1, ..., 2: n * (n-1) / 2 comparisons and depth n-1.
- A random pivot makes a bad split unlikely: expected O(n log n) comparisons. In my random run (n = 3000) it used 38,808 comparisons and depth 26 against 4,498,500 for sorted input.
- Not stable: the long-range swaps jump equal items over each other. Smallest case found by search over keys 1 and 2: [(1,'a'), (2,'b'), (2,'c')] comes out with 'c' before 'b' (see output).

**Complexity:** Average O(n log n) time with a random or typical pivot; worst case O(n^2) (sorted, reverse, all equal with this rule). Space O(1) extra beyond the explicit stack, which holds O(depth) entries: O(n) in the worst case here. (Pushing the larger side first and looping on the smaller one would bound it to O(log n); not done here.)

**Dry run:** [3,1,2], pivot 2, i = 0. j=0: 3<2 no. j=1: 1<2 yes, swap a[0],a[1] -> [1,3,2], i=1. Swap a[1],a[2] -> [1,2,3]. 2 comparisons. Both sides have one item, skipped. Depth 1. For [4,2,7,1,9,3] (pivot 3): 5 comparisons give [2,1,3,4,9,7]; the left [2,1] costs 1 and the right [4,9,7] costs 2, total 8, depth 2.

**Code:**
```python
import random
import sys

random.seed(1316)

def quicksort_iter(nums):
    """Lomuto, last element as pivot, explicit stack. depth = most nested partition calls of the recursive version."""
    a = list(nums); cmps = 0; depth = 0
    stack = [(0, len(a) - 1, 1)] if len(a) > 1 else []
    while stack:
        lo, hi, d = stack.pop()
        depth = max(depth, d)
        p, i = a[hi], lo
        for j in range(lo, hi):
            cmps += 1                              # the ONE comparison per item
            if a[j] < p:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]                  # pivot to its final place i
        if i + 1 < hi: stack.append((i + 1, hi, d + 1))   # skip ranges with fewer than 2 items
        if lo < i - 1: stack.append((lo, i - 1, d + 1))
    return [a, cmps, depth]

def brute(nums):
    """Recursive Lomuto (only safe for small inputs)."""
    a = list(nums); cmps = 0; depth = 0
    def rec(lo, hi, d):
        nonlocal cmps, depth
        if lo >= hi: return
        depth = max(depth, d)
        p, i = a[hi], lo
        for j in range(lo, hi):
            cmps += 1
            if a[j] < p:
                a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]
        rec(lo, i - 1, d + 1); rec(i + 1, hi, d + 1)
    rec(0, len(a) - 1, 1)
    return [a, cmps, depth]

examples = [
    ([3, 1, 2], [[1, 2, 3], 2, 1]),
    ([1, 2, 3, 4], [[1, 2, 3, 4], 6, 3]),
    ([5, 5, 5], [[5, 5, 5], 3, 2]),
    ([4, 2, 7, 1, 9, 3], [[1, 2, 3, 4, 7, 9], 8, 2]),
]
for nums, exp in examples:
    got = quicksort_iter(nums)
    print(nums, '->', got)
    assert got == exp and brute(nums) == exp

# sorted and all-equal input: n(n-1)/2 comparisons, depth n-1
for n in range(1, 40):
    for arr in (list(range(n)), [5] * n):
        r = quicksort_iter(arr)
        assert r[1] == n * (n - 1) // 2 and (r[2] == n - 1 if n > 1 else r[2] == 0)
print('sorted / all-equal: comparisons n(n-1)/2 and depth n-1 verified for n < 40')

# n = 3000: iterative copes, the recursive version hits the default limit (1000)
big = quicksort_iter(list(range(3000)))
assert big[0] == list(range(3000)) and big[1] == 3000 * 2999 // 2 and big[2] == 2999
print('n = 3000 sorted: comparisons', big[1], 'depth', big[2], '| recursion limit', sys.getrecursionlimit())
try:
    brute(list(range(1500)))
    print('recursive n=1500: no error')
except RecursionError:
    print('recursive version, n = 1500: RecursionError')

# random input, n = 3000
rnd = [random.randint(-10 ** 9, 10 ** 9) for _ in range(3000)]
r = quicksort_iter(rnd)
assert r[0] == sorted(rnd)
print('random n = 3000: comparisons', r[1], 'depth', r[2], '(n(n-1)/2 would be', 3000 * 2999 // 2, ')')

# not stable: tag the items and run the same Lomuto on the keys; find an input where equal keys swap order
def lomuto_tagged(items):
    a = list(items)
    def rec(lo, hi):
        if lo >= hi: return
        p, i = a[hi][0], lo
        for j in range(lo, hi):
            if a[j][0] < p:
                a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]
        rec(lo, i - 1); rec(i + 1, hi)
    rec(0, len(a) - 1)
    return a
import itertools
ex = next([(k, 'abc'[i]) for i, k in enumerate(p)] for p in itertools.product([1, 2], repeat=3)
          if [t for k, t in lomuto_tagged([(k, 'abc'[i]) for i, k in enumerate(p)]) if k == 2]
          != [t for k, t in [(k, 'abc'[i]) for i, k in enumerate(p)] if k == 2])
print('unstable example:', ex, '->', lomuto_tagged(ex))

# seeded random cross-check vs recursive Lomuto and sorted()
for _ in range(400):
    nums = [random.randint(-5, 5) for _ in range(random.randint(1, 40))]
    r = quicksort_iter(nums)
    assert r == brute(nums) and r[0] == sorted(nums)
print('random cross-check ok: 400 cases')

# edge asserts
assert quicksort_iter([7]) == [[7], 0, 0]
assert quicksort_iter([2, 1]) == [[1, 2], 1, 1]
print('edge asserts ok')
```

**Output (my run):**
```
[3, 1, 2] -> [[1, 2, 3], 2, 1]
[1, 2, 3, 4] -> [[1, 2, 3, 4], 6, 3]
[5, 5, 5] -> [[5, 5, 5], 3, 2]
[4, 2, 7, 1, 9, 3] -> [[1, 2, 3, 4, 7, 9], 8, 2]
sorted / all-equal: comparisons n(n-1)/2 and depth n-1 verified for n < 40
n = 3000 sorted: comparisons 4498500 depth 2999 | recursion limit 1000
recursive version, n = 1500: RecursionError
random n = 3000: comparisons 38808 depth 26 (n(n-1)/2 would be 4498500 )
unstable example: [(1, 'a'), (2, 'b'), (2, 'c')] -> [(1, 'a'), (2, 'c'), (2, 'b')]
random cross-check ok: 400 cases
edge asserts ok
```

**Edge cases:**
- One element: no partition, 0 comparisons, depth 0 (the first call counts only when a range of at least 2 items exists).
- Sorted, reverse sorted, all equal: the quadratic cases, n * (n-1) / 2 for sorted and all-equal.
- Many duplicates: Lomuto degrades; three-way partition fixes it (another question in this part).
- n = 3000 sorted: 4,498,500 comparisons, still fast enough here.

**Follow-ups:**
- Why not raise `sys.setrecursionlimit`? It only moves the crash (very deep recursion can kill the interpreter; editor knowledge, not tested here); the stack-based version is the safe answer.
- Hoare partition? Fewer swaps, different pivot rules, covered by another question in this part.
- Kth largest without a full sort: quickselect, Part 8 Q36.

**Common mistakes:**
- Recursing on sorted input and hitting `RecursionError`.
- Pushing ranges with 0 or 1 items.
- Using `<=` in the Lomuto test, which moves equal items and changes the counts.
- Saying quicksort is stable. It is not.

### Q17 ⭐⭐⭐ 🟡 Count inversions with merge sort. `nums` has 0 <= len <= 10^5 integers (|value| <= 10^9, duplicates allowed). An inversion is a pair of positions i < j with nums[i] > nums[j] (strictly greater, equal values do not count). Return the number of inversions in O(n log n). During the merge of two sorted halves, when the next item taken comes from the right half, it is smaller than every item still waiting in the left half, so add the number of items remaining in the left half; take from the left when `left <= right` so ties are not counted. Explain why the count over the whole array is the sum of the left-half inversions, the right-half inversions and the cross inversions found while merging, why a merge cannot change the cross count (sorted halves), the maximum n * (n - 1) / 2 (strictly decreasing input) and that this number equals the number of element shifts made by insertion sort. The recursion depth is about log2 n (under 20), so recursion is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the O(n^2) double loop on small inputs. Example: nums=[2, 4, 1, 3, 5] -> 3; nums=[5, 4, 3, 2, 1] -> 10; nums=[1, 1, 1] -> 0; nums=[] -> 0; nums=[3, 1, 2, 3, 1] -> 5.
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)

**Pattern:** Merge sort with a counter. Count cross pairs while merging.

**Say this first (1 line):** "An inversion is i < j with nums[i] > nums[j]. Merge sort counts them: when I take an item from the right half, it is smaller than every item still waiting in the left half, so I add that many. O(n log n)."

**Brute force:** Two loops over every pair, O(n^2). For n = 10^5 that is 5 x 10^9 pair checks: too slow.

**Optimal:**
- Total inversions = inversions inside the left half + inside the right half + cross pairs (one item left, one right).
- Merge two sorted halves with two pointers. If `a[i] <= a[j]` take left (no count; equal values are not inversions). Else take right and add `mid - i`: the left items from i onward are all greater than a[j], because the left half is sorted.
- A merge never changes the cross count for a higher level: the halves are sorted, and the cross pairs between two sets do not depend on the order inside each set. Sorting the halves loses nothing.
- Maximum n * (n-1) / 2, reached by a strictly decreasing array (checked for n <= 11 and at n = 10^5).
- This number equals the shifts insertion sort makes: each shift moves one item past a strictly larger earlier item, which is exactly one inversion (checked equal on 400 random cases).
- Recursion depth is about log2 n (17 for n = 10^5), fine.

**Complexity:** O(n log n) time, O(n) space for the buffer. Counts can reach about 5 x 10^9 at n = 10^5, which is fine for Python ints (in a fixed-width language you need 64 bits).

**Dry run:** [2,4,1,3,5], split [2,4] | [1,3,5]. Inside each half: no inversions. Merge: 2 vs 1: 1 is smaller, take it, add the 2 left items (2 and 4): +2. 2 vs 3: take 2. 4 vs 3: take 3, add 1 (just 4): +1. 4 vs 5: take 4. Take 5. Total 3: (2,1), (4,1), (4,3).

**Code:**
```python
import random

random.seed(1317)

def count_inversions(nums):
    """Merge sort; when the right item is taken, it beats every item still waiting on the left."""
    a = list(nums)
    buf = [0] * len(a)
    def sort(lo, hi):
        if hi - lo <= 1:
            return 0
        mid = (lo + hi) // 2
        inv = sort(lo, mid) + sort(mid, hi)
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if a[i] <= a[j]:                 # tie: take LEFT, equal values are not inversions
                buf[k] = a[i]; i += 1
            else:
                buf[k] = a[j]; j += 1
                inv += mid - i               # everything left in the left half is > a[j]
            k += 1
        while i < mid: buf[k] = a[i]; i += 1; k += 1
        while j < hi: buf[k] = a[j]; j += 1; k += 1
        a[lo:hi] = buf[lo:hi]
        return inv
    return sort(0, len(a))

def brute(nums):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] > nums[j])

def insertion_shifts(nums):
    a = list(nums); shifts = 0
    for i in range(1, len(a)):
        x, j = a[i], i - 1
        while j >= 0 and a[j] > x:          # strict >: equal items are not shifted
            a[j + 1] = a[j]; j -= 1; shifts += 1
        a[j + 1] = x
    return shifts

examples = [([2, 4, 1, 3, 5], 3), ([5, 4, 3, 2, 1], 10), ([1, 1, 1], 0), ([], 0), ([3, 1, 2, 3, 1], 5)]
for nums, exp in examples:
    got = count_inversions(nums)
    print(nums, '->', got)
    assert got == exp and brute(nums) == exp

# the '<' tie rule would count equal pairs as inversions
def wrong_tie(nums):
    n = len(nums); return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] >= nums[j])
print('counting ties too, [1, 1, 1] would give', wrong_tie([1, 1, 1]))

# max n(n-1)/2 for strictly decreasing input
for n in range(0, 12):
    assert count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2
print('strictly decreasing input gives n(n-1)/2 for n <= 11')

# inversions == insertion-sort shifts; cross-check against the double loop
for _ in range(400):
    nums = [random.randint(-6, 6) for _ in range(random.randint(0, 25))]
    c = count_inversions(nums)
    assert c == brute(nums) == insertion_shifts(nums)
print('random cross-check ok: 400 cases (merge count == double loop == insertion shifts)')

# maximum size: n = 10^5 (decreasing = worst case, random, all equal)
n = 10 ** 5
assert count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2
r = [random.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
print('n = 10^5 random:', count_inversions(r), '(about n(n-1)/4 =', n * (n - 1) // 4, ')')
assert count_inversions([7] * n) == 0

# edge asserts
assert count_inversions([1]) == 0 and count_inversions([2, 1]) == 1 and count_inversions([1, 2]) == 0
print('edge asserts ok')
```

**Output (my run):**
```
[2, 4, 1, 3, 5] -> 3
[5, 4, 3, 2, 1] -> 10
[1, 1, 1] -> 0
[] -> 0
[3, 1, 2, 3, 1] -> 5
counting ties too, [1, 1, 1] would give 3
strictly decreasing input gives n(n-1)/2 for n <= 11
random cross-check ok: 400 cases (merge count == double loop == insertion shifts)
n = 10^5 random: 2505411528 (about n(n-1)/4 = 2499975000 )
edge asserts ok
```

**Edge cases:**
- Empty and single: 0.
- All equal: 0. Using `<` in the take-left test (or counting `>=`) would count ties: [1,1,1] would give 3.
- Strictly decreasing: n * (n-1) / 2.
- Duplicates mixed with distinct values, like [3,1,2,3,1] giving 5.

**Follow-ups:**
- Count only "significant" pairs, nums[i] > 2 * nums[j]? Count before merging with a second pointer; same O(n log n).
- Same with a Fenwick tree after coordinate compression? Yes, O(n log n); Fenwick trees are Part 14 (named only).
- Minimum adjacent swaps to sort: equals the inversion count for distinct values.

**Common mistakes:**
- Adding 1 instead of `mid - i` when taking from the right.
- `<` vs `<=` on ties.
- Counting after the halves are merged back (positions are lost), instead of during the merge.
- Slicing the array every call, giving O(n) extra copies per level; use a shared buffer as in my code.

### Q18 ⭐⭐ 🟢 Happy number. For a positive integer n, repeatedly replace it by the sum of the squares of its decimal digits. `n` is an integer with 1 <= n <= 2^31 - 1. Return `[happy, steps, cycle_len]`: `happy` is True if the sequence reaches 1; `steps` is the number of replacements needed to reach 1 from n (0 when n is 1) or -1 when n is not happy; `cycle_len` is the length of the cycle the sequence eventually enters (1 for a happy number, because 1 maps to itself; for the others it is a fixed length you should find). Detect the cycle with Floyd's tortoise and hare in O(1) space (and compare it with a set of seen values). Explain why the sequence cannot grow forever (for a number with 4 or more digits the digit-square sum is smaller than the number, and for any 10-digit input it is at most 810) so it must repeat, and name the cycle every unhappy number ends in. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a dictionary of seen values to positions on small inputs. Example: n=19 -> [True, 4, 1]; n=2 -> [False, -1, 8]; n=1 -> [True, 0, 1]; n=7 -> [True, 5, 1]; n=4 -> [False, -1, 8].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Cycle detection on a number sequence (Floyd's tortoise and hare), plus a small proof that the sequence is bounded.

**Say this first (1 line):** "The map n -> sum of squared digits eventually repeats, because it shrinks large numbers. A happy number reaches the fixed point 1; every other number ends in the same 8-cycle 4, 16, 37, 58, 89, 145, 42, 20. Floyd's two pointers find it in O(1) space."

**Brute force:** Keep a dict `seen[value] = position`. Stop when a value repeats; the cycle length is the current position minus the earlier one. O(steps) time and space. Simple and what I check against.

**Optimal:**
- Floyd: slow moves one step, fast moves two. Stop when fast is 1 or slow == fast. If it stopped on 1 the number is happy. Otherwise `fast` is now inside the cycle.
- Cycle length: from that point step until you return to it, counting.
- Steps (for a happy number): just apply the map again from n until 1.
- Why it must repeat: for a number with d digits the digit-square sum is at most 81 d. For d >= 4, 81 d < 10^(d-1) <= n, so the sum is smaller than n (I checked f(n) < n for every n from 1000 to 300,000 and the inequality for d up to 39). So every value drops below 1000 and then stays under 243 (at most 3 x 81). A 10-digit input (the 2^31-1 range) gives at most 810 after one step. A finite set of values forces a repeat.
- The cycle for unhappy numbers is [4, 16, 37, 58, 89, 145, 42, 20], length 8. I checked every n < 200,000: happy implies cycle length 1, and every other number has cycle length 8.

**Complexity:** Each step costs O(digits), about 10 for the input range. The number of steps is small (the first step brings any input under 811; the output shows the longest run I measured). O(1) extra space for Floyd; the dict version is O(steps).

**Dry run:** n = 19: 1 + 81 = 82, 64 + 4 = 68, 36 + 64 = 100, 1 + 0 + 0 = 1. That is 4 steps, happy, cycle length 1 (1 maps to 1). Floyd on 19: slow 19, fast 82. Move: slow 82, fast f(f(82)) = 100. Move: slow 68, fast f(f(100)) = f(1) = 1. Stop on 1. n = 2: 4, 16, 37, 58, 89, 145, 42, 20, 4: back to 4 after 8 steps, so [False, -1, 8].

**Code:**
```python
import random

random.seed(1318)

def f(v):
    s = 0
    while v:
        v, d = divmod(v, 10)
        s += d * d
    return s

def happy(n):
    """Floyd: tortoise moves 1 step, hare 2; O(1) space. Then measure the cycle length from the meeting point."""
    slow, fast = n, f(n)
    while fast != 1 and slow != fast:
        slow, fast = f(slow), f(f(fast))
    x, c = fast, 1                          # fast is inside the cycle (or is 1)
    y = f(x)
    while y != x:
        y, c = f(y), c + 1
    steps = -1
    if fast == 1 or n == 1:
        steps, v = 0, n
        while v != 1:
            v, steps = f(v), steps + 1
    return [steps >= 0, steps, c]

def brute(n):
    """Dictionary of seen value -> position."""
    seen, v, i = {}, n, 0
    while v not in seen:
        seen[v] = i; i += 1
        v = f(v)
    return [1 in seen, seen.get(1, -1), i - seen[v]]

examples = [(19, [True, 4, 1]), (2, [False, -1, 8]), (1, [True, 0, 1]), (7, [True, 5, 1]), (4, [False, -1, 8])]
for n, exp in examples:
    got = happy(n)
    print(n, '->', got)
    assert got == exp and brute(n) == exp
print('trace of 19:', [19, f(19), f(f(19)), f(f(f(19))), f(f(f(f(19))))])

# exhaustive: every n < 200000 is happy or ends in the 8-cycle; list the cycle
for n in range(1, 200000):
    h, st, cl = happy(n)
    assert (cl == 1) if h else (cl == 8)
    assert [h, st, cl] == brute(n)
cyc, v = [], 4
while True:
    cyc.append(v); v = f(v)
    if v == 4: break
print('unhappy cycle:', cyc, '| checked every n < 200000: happy => cycle 1, unhappy => cycle of 8')

# why the sequence cannot grow: f(n) < n for n >= 1000 (checked), and the 10-digit bound
assert all(f(n) < n for n in range(1000, 300000))
assert all(81 * k < 10 ** (k - 1) for k in range(4, 40))
print('81*d < 10^(d-1) for every d >= 4; 10-digit bound 10*81 = 810; f(2^31-1) =', f(2 ** 31 - 1),
      ', f(1999999999) =', f(1999999999))
assert f(2 ** 31 - 1) <= 810 and max(f(n) for n in range(10 ** 9, 10 ** 9 + 1000)) <= 810

# longest run before a value repeats, over every n < 100000
def run_len(n):
    seen, v = set(), n
    while v not in seen:
        seen.add(v); v = f(v)
    return len(seen)
print('longest run before a repeat for n < 100000:', max(run_len(n) for n in range(1, 100000)), 'values')

# seeded random cross-check on large values too
for _ in range(500):
    n = random.choice([random.randint(1, 3000), random.randint(1, 2 ** 31 - 1)])
    assert happy(n) == brute(n)
print('random cross-check ok: 500 cases')

# edge asserts
assert happy(2 ** 31 - 1)[0] in (True, False)
assert happy(10) == [True, 1, 1] and happy(100) == [True, 1, 1] and happy(1) == [True, 0, 1]
print('edge asserts ok; 2^31-1 ->', happy(2 ** 31 - 1))
```

**Output (my run):**
```
19 -> [True, 4, 1]
2 -> [False, -1, 8]
1 -> [True, 0, 1]
7 -> [True, 5, 1]
4 -> [False, -1, 8]
trace of 19: [19, 82, 68, 100, 1]
unhappy cycle: [4, 16, 37, 58, 89, 145, 42, 20] | checked every n < 200000: happy => cycle 1, unhappy => cycle of 8
81*d < 10^(d-1) for every d >= 4; 10-digit bound 10*81 = 810; f(2^31-1) = 260 , f(1999999999) = 730
longest run before a repeat for n < 100000: 20 values
random cross-check ok: 500 cases
edge asserts ok; 2^31-1 -> [False, -1, 8]
```

**Edge cases:**
- n = 1: 0 steps, cycle 1.
- n = 10, 100: one step to 1.
- Largest input 2^31 - 1 is unhappy (result `[False, -1, 8]`).
- n = 4 (inside the unhappy cycle already): `[False, -1, 8]`.

**Follow-ups:**
- Why not just detect "reaches 4"? That works (the whole unhappy family goes through 4), but the proof that 4 is on every unhappy path is the same exhaustive check; Floyd or a set needs no such fact.
- Same technique elsewhere? Linked-list cycle (Floyd), and duplicate-number-as-cycle problems.
- Count happy numbers below N? Precompute with the map for each value; the map shrinks, so a memo works.

**Common mistakes:**
- Fast pointer started equal to slow, so the loop exits immediately.
- Assuming the sequence grows forever for big inputs.
- Forgetting n = 1 (already happy, 0 steps).
- Recomputing digits with strings in a hot loop without need (fine here, but say it).

### Q19 ⭐⭐ 🟢 Excel column titles and numbers. `title` is a column title of 1 to 7 uppercase letters whose number is at most 2^31 - 1 (A = 1, ..., Z = 26, AA = 27, AB = 28, ..., AZ = 52, BA = 53, ...), and `number` is an integer with 1 <= number <= 2^31 - 1. Return `[number_of_title, title_of_number]`. This is base 26 with digits 1..26 and no zero digit (bijective numeration). Convert a title with `r = r * 26 + (ord(ch) - 64)` and a number with the loop `n, d = divmod(n - 1, 26)` taking letter `chr(65 + d)`, then reverse; explain why the `n - 1` is needed (there is no zero digit, so plain base 26 would turn 26 into nonsense: the naive `divmod(n, 26)` with `chr(64 + d)` gives 'A@' for 26 and 'B@' for 52, not 'Z' and 'AZ') and why both directions are O(length), about log26 of the value. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an explicit table of all titles up to length 4 on small inputs. Example: title='AB', number=28 -> [28, 'AB']; title='A', number=1 -> [1, 'A']; title='ZY', number=701 -> [701, 'ZY']; title='FXSHRXW', number=2147483647 -> [2147483647, 'FXSHRXW'].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Bijective base 26 (digits 1..26, no zero). Number base conversion with an offset.

**Say this first (1 line):** "Title to number is a plain Horner loop, r = r * 26 + (ord(ch) - 64). Number to title peels letters with divmod(n - 1, 26); the minus one is there because there is no zero digit."

**Brute force:** Build a table of every title in order (A..Z, AA..ZZ, ...) and look up by position or by index. Fine for short titles; the table grows 26^L, so it cannot hold seven-letter titles. I use it for all titles up to four letters (475,254 of them).

**Optimal:**
- Title to number: each letter is a digit 1..26. Horner: r = r * 26 + digit. 'AB' = 1 * 26 + 2 = 28.
- Number to title: shift by one first. `n, d = divmod(n - 1, 26)` gives a digit 0..25, which is the letter `chr(65 + d)`. Repeat while n > 0, then reverse the collected letters.
- Why n - 1: in plain base 26 a remainder of 0 means "no letter". The titles have no zero digit, so 26 must be 'Z', not "1 then 0". Subtracting 1 turns digits 1..26 into 0..25 each round. Plain `divmod(n, 26)` gives '@' for a zero remainder (`26 -> 'A@'`, `52 -> 'B@'` in the output).
- Both directions loop once per letter: about log26 of the value. The largest allowed number 2^31 - 1 is the 7-letter title 'FXSHRXW'; the next title 'FXSHRXX' is exactly 2^31.

**Complexity:** O(L), L = number of letters (at most 7). Space O(L) for the output.

**Dry run:** number 28: divmod(27, 26) = (1, 1): letter 'B'. n = 1: divmod(0, 26) = (0, 0): letter 'A'. Collected 'BA', reversed 'AB'. Title 'AB': r = 0*26 + 1 = 1, then 1*26 + 2 = 28. Check 26: divmod(25, 26) = (0, 25), letter 'Z'.

**Code:**
```python
import itertools
import random
import string

random.seed(1319)

def title_to_number(title):
    r = 0
    for ch in title:
        r = r * 26 + (ord(ch) - 64)         # A=1 .. Z=26: digits 1..26, no zero digit
    return r

def number_to_title(n):
    out = []
    while n:
        n, d = divmod(n - 1, 26)            # shift to 0..25 first, then peel a letter
        out.append(chr(65 + d))
    return ''.join(reversed(out))

def solve(title, number):
    return [title_to_number(title), number_to_title(number)]

# brute force: an explicit table of ALL titles up to length 4, in order (shorter first, then alphabetical)
TABLE = [''.join(p) for L in range(1, 5) for p in itertools.product(string.ascii_uppercase, repeat=L)]
INDEX = {t: i + 1 for i, t in enumerate(TABLE)}
assert len(TABLE) == 26 + 26 ** 2 + 26 ** 3 + 26 ** 4

def brute(title, number):
    # for the 7-letter maximum the table is too small, so fall back to digit-by-digit counting
    if len(title) <= 4 and number <= len(TABLE):
        return [INDEX[title], TABLE[number - 1]]
    k, L = number - 1, 1
    while k >= 26 ** L:
        k -= 26 ** L; L += 1
    digs = []
    for _ in range(L):
        k, r = divmod(k, 26); digs.append(chr(65 + r))
    return [sum((ord(c) - 64) * 26 ** i for i, c in enumerate(reversed(title))), ''.join(reversed(digs))]

examples = [('AB', 28, [28, 'AB']), ('A', 1, [1, 'A']), ('ZY', 701, [701, 'ZY']),
            ('FXSHRXW', 2147483647, [2147483647, 'FXSHRXW'])]
for t, n, exp in examples:
    got = solve(t, n)
    print(t, n, '->', got)
    assert got == exp and brute(t, n) == exp

# why n - 1: plain base 26 breaks on the multiples of 26
def naive(n):
    out = []
    while n:
        n, d = divmod(n, 26); out.append(chr(64 + d))     # d == 0 gives '@'
    return ''.join(reversed(out))
print('naive divmod(n, 26): 26 ->', repr(naive(26)), ', 52 ->', repr(naive(52)), '| with n-1:', number_to_title(26), number_to_title(52))
assert naive(26) == '@' + '' or '@' in naive(26)

# round trip over the WHOLE table (475254 titles) and against the table in both directions
for i, t in enumerate(TABLE, start=1):
    assert title_to_number(t) == i and number_to_title(i) == t
print('round trip ok for all', len(TABLE), 'titles up to length 4')

# seeded random cross-check
for _ in range(500):
    L = random.randint(1, 4)
    t = ''.join(random.choice(string.ascii_uppercase) for _ in range(L))
    n = random.randint(1, len(TABLE))
    assert solve(t, n) == brute(t, n)
print('random cross-check ok: 500 cases')

# limits: 2^31 - 1 is 7 letters, and 8 letters would overflow int32 (Python has no overflow; the bound is the prompt's)
assert number_to_title(2 ** 31 - 1) == 'FXSHRXW' and len(number_to_title(2 ** 31 - 1)) == 7
assert title_to_number('FXSHRXX') > 2 ** 31 - 1
print('length of title(2^31-1) =', len(number_to_title(2 ** 31 - 1)), '; next title FXSHRXX =', title_to_number('FXSHRXX'))

# edge asserts
assert number_to_title(26) == 'Z' and number_to_title(27) == 'AA' and number_to_title(52) == 'AZ' and number_to_title(53) == 'BA'
assert number_to_title(703) == 'AAA'
assert title_to_number('Z') == 26 and title_to_number('AA') == 27 and title_to_number('ZZ') == 702 and number_to_title(702) == 'ZZ'
print('edge asserts ok')
```

**Output (my run):**
```
AB 28 -> [28, 'AB']
A 1 -> [1, 'A']
ZY 701 -> [701, 'ZY']
FXSHRXW 2147483647 -> [2147483647, 'FXSHRXW']
naive divmod(n, 26): 26 -> 'A@' , 52 -> 'B@' | with n-1: Z AZ
round trip ok for all 475254 titles up to length 4
random cross-check ok: 500 cases
length of title(2^31-1) = 7 ; next title FXSHRXX = 2147483648
edge asserts ok
```

**Edge cases:**
- 26 -> 'Z', 27 -> 'AA', 52 -> 'AZ', 53 -> 'BA', 702 -> 'ZZ', 703 -> 'AAA'.
- Single letter.
- The maximum 2^31 - 1: 'FXSHRXW'. Python has no overflow, so the only limit is the prompt's bound.
- Number 0 is not valid input; the loop would return an empty string.

**Follow-ups:**
- Why does this differ from hexadecimal? Hex has a zero digit; this system does not, so every value has a unique spelling without leading zeros.
- Add two column titles? Convert, add, convert back.
- Generalise to base b with digits 1..b: same loop with 26 replaced by b.

**Common mistakes:**
- `divmod(n, 26)` with `chr(64 + d)` and no `- 1`: '@' for multiples of 26.
- Taking the digit from n - 1 but dividing plain n by 26 (wrong at 26, 52, 702).
- Forgetting to reverse the letters.
- Using `ord(ch) - 65` for the title direction (A would be 0 and 'AA' collides with 'A').

### Q20 ⭐⭐ 🟢 Pascal's triangle. `num_rows` is an integer with 0 <= num_rows <= 30 and `row_index` is an integer with 0 <= row_index <= 200. Return `[triangle, row]`: `triangle` is the first `num_rows` rows as lists (row i has i + 1 entries, starts and ends with 1, and every inner entry is the sum of the two above it; `num_rows = 0` gives an empty list), and `row` is row number `row_index` (0-indexed) alone, built with only O(row_index) extra space by updating one list from right to left. Explain why the right-to-left order matters, give the closed form C(n, k) = n! / (k! (n - k)!) and the recurrence C(n, k) = C(n, k-1) * (n - k + 1) / k that is always an exact integer step, and say from which row on the entries stop fitting in a signed 32-bit integer (the largest entry of row 33 is below 2^31 - 1 and row 34 has an entry above it) while Python needs no change. In the answer include a dry run on the first example and a seeded random cross-check of your solution against math.comb on small inputs. Example: num_rows=5, row_index=4 -> [[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]], [1, 4, 6, 4, 1]]; num_rows=0, row_index=0 -> [[], [1]]; num_rows=1, row_index=1 -> [[[1]], [1, 1]]; num_rows=3, row_index=10 -> [[[1], [1, 1], [1, 2, 1]], [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Dynamic programming on a triangle (Pascal), with a one-row, right-to-left update for O(row) space.

**Say this first (1 line):** "Each entry is the sum of the two above it, edges are 1. For a single row I keep one list and update it from right to left, so the value I read from the left is still last row's value. That is O(row_index) space."

**Brute force:** Use the closed form C(n, k) = n! / (k! (n-k)!) per entry. Correct, but computing factorials per entry wastes work; `math.comb` is the checked reference here (`math.comb` exists since 3.8, editor knowledge).

**Optimal:**
- Triangle: row i = [1] + [prev[j-1] + prev[j] for j in 1..i-1] + [1]; row 0 is [1]; `num_rows = 0` returns [].
- Single row without keeping rows: start with row = [1] * (n + 1). For i from 1 to n, update j = i-1 down to 1 with `row[j] += row[j-1]`. Right to left: `row[j-1]` has not been touched in this round yet, so it still holds last round's value. Left to right would add an already-updated neighbour: for row 4 it gives [1, 4, 8, 9, 1] (shown in the output).
- Multiplicative recurrence: C(n, k) = C(n, k-1) * (n - k + 1) / k. Multiply first, then use integer `//`: the division is always exact (checked for every row below 200), so no floats are needed.
- Overflow: Python ints do not overflow. In a signed 32-bit integer the largest entry of row 33 is 1,166,803,110 (fits under 2,147,483,647) and row 34 has an entry 2,333,606,220 (does not), so from row 34 on you need 64 bits in other languages.

**Complexity:** Triangle: O(num_rows^2) time and space (it is the output). One row: O(n^2) time for the nested loop, O(n) space. The multiplicative way is O(n) time for the row (n big-int multiplications), also O(n) space.

**Dry run:** row_index 4: row = [1,1,1,1,1]. i=1: nothing to update. i=2: j=1: row[1] = 1 + 1 = 2 -> [1,2,1,1,1]. i=3: j=2: row[2] = 1 + 2 = 3; j=1: row[1] = 2 + 1 = 3 -> [1,3,3,1,1]. i=4: j=3: 1+3 = 4; j=2: 3+3 = 6; j=1: 3+1 = 4 -> [1,4,6,4,1].

**Code:**
```python
import math
import random

random.seed(1320)

def pascal(num_rows, row_index):
    tri = []
    for i in range(num_rows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = tri[i - 1][j - 1] + tri[i - 1][j]
        tri.append(row)
    row = [1] * (row_index + 1)
    for i in range(1, row_index + 1):
        for j in range(i - 1, 0, -1):          # RIGHT to LEFT: row[j-1] is still last row's value when we use it
            row[j] += row[j - 1]
    return [tri, row]

def brute(num_rows, row_index):
    return [[[math.comb(i, j) for j in range(i + 1)] for i in range(num_rows)],
            [math.comb(row_index, j) for j in range(row_index + 1)]]

examples = [
    (5, 4, [[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]], [1, 4, 6, 4, 1]]),
    (0, 0, [[], [1]]),
    (1, 1, [[[1]], [1, 1]]),
    (3, 10, [[[1], [1, 1], [1, 2, 1]], [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]]),
]
for nr, ri, exp in examples:
    got = pascal(nr, ri)
    print(nr, ri, '->', got)
    assert got == exp and brute(nr, ri) == exp

# left-to-right update is wrong: it re-uses a value already overwritten
def wrong_row(n):
    row = [1] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, i):
            row[j] += row[j - 1]
    return row
print('left-to-right row 4:', wrong_row(4), '(correct [1, 4, 6, 4, 1])')
assert wrong_row(4) != [1, 4, 6, 4, 1]

# the multiplicative recurrence C(n,k) = C(n,k-1) * (n-k+1) / k is ALWAYS exact: multiply first, then //
for n in range(0, 200):
    c = 1
    for k in range(1, n + 1):
        assert (c * (n - k + 1)) % k == 0
        c = c * (n - k + 1) // k
        assert c == math.comb(n, k)
print('exact-division recurrence checked for every row n < 200')

# int32 boundary: largest entry of row 33 is below 2^31 - 1, row 34 has an entry above it
mx = lambda n: max(math.comb(n, k) for k in range(n + 1))
print('max entry row 33 =', mx(33), ' row 34 =', mx(34), ' 2^31 - 1 =', 2 ** 31 - 1)
assert mx(33) < 2 ** 31 - 1 < mx(34) and all(mx(n) < 2 ** 31 - 1 for n in range(34))

# row sums are 2^n; symmetry
for n in range(0, 61):
    r = pascal(0, n)[1]
    assert sum(r) == 2 ** n and r == r[::-1]
print('row sums 2^n and symmetry ok for n <= 60')

# seeded random cross-check against math.comb
for _ in range(300):
    nr, ri = random.randint(0, 30), random.randint(0, 200)
    assert pascal(nr, ri) == brute(nr, ri)
print('random cross-check ok: 300 cases')

# edge asserts
assert pascal(0, 0) == [[], [1]] and pascal(2, 0)[1] == [1] and len(pascal(30, 200)[0]) == 30 and len(pascal(30, 200)[1]) == 201
print('edge asserts ok; C(200, 100) has', len(str(math.comb(200, 100))), 'digits')
```

**Output (my run):**
```
5 4 -> [[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]], [1, 4, 6, 4, 1]]
0 0 -> [[], [1]]
1 1 -> [[[1]], [1, 1]]
3 10 -> [[[1], [1, 1], [1, 2, 1]], [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]]
left-to-right row 4: [1, 4, 8, 9, 1] (correct [1, 4, 6, 4, 1])
exact-division recurrence checked for every row n < 200
max entry row 33 = 1166803110  row 34 = 2333606220  2^31 - 1 = 2147483647
row sums 2^n and symmetry ok for n <= 60
random cross-check ok: 300 cases
edge asserts ok; C(200, 100) has 59 digits
```

**Edge cases:**
- num_rows = 0: empty triangle; row_index = 0: [1].
- Rows are symmetric and sum to 2^n (checked for n <= 60).
- Row 200 has entries with up to 59 digits (C(200, 100)); Python handles it.
- `num_rows` and `row_index` are independent inputs here.

**Follow-ups:**
- Why is the sum 2^n? Each element in a set of n is in or out of a subset; C(n, k) counts subsets of size k.
- Row mod a prime for large n? Use the multiplicative recurrence with a modular inverse (modular inverse is another question in this part).
- Only the k-th entry? One loop of the recurrence, O(k) time, O(1) space.

**Common mistakes:**
- Updating left to right and corrupting the row.
- Writing the recurrence with float division (`/`) and getting rounding errors for large rows.
- Off-by-one: row 0 is [1] (row_index is 0-indexed).
- Forgetting that `num_rows = 0` must return `[]`, not `[[]]`.

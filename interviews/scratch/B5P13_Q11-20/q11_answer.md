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

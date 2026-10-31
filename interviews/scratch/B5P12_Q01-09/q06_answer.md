### Q6 ⭐⭐⭐ 🟡 Permutations of distinct integers. `nums` has 0 <= len <= 8 distinct integers. Return all n! orderings, each as a list, with the outer list sorted ascending with Python's list comparison (lexicographic order by value; so the order of `nums` itself does not matter). `nums = []` returns `[[]]` (one empty permutation). Use a `used` array and say how the swap-in-place variant differs; the cost is O(n * n!). Part 1 Q34 (next permutation) steps from one permutation to the next in this same order without recursion; mention that as a follow-up. Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against itertools.permutations sorted on small inputs. Example: nums=[3, 1, 2] -> [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]; nums=[] -> [[]]; nums=[9] -> [[9]]; nums=[2, 1] -> [[1, 2], [2, 1]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking, ordering a set: choose an unused element for each position.

**Say this first (1 line):** "Fill the positions left to right; at each position try every element not yet used, mark it, recurse, unmark. There are n! leaves and each costs O(n) to copy: O(n * n!). Sort the outer list at the end."

**Brute force:** `itertools.permutations(nums)` sorted. Or the unpruned recursion that tries all n values at every position and rejects repeats only at the leaves: n^n leaves. For n = 6 that is 55987 calls against 1957 for the used-array version (measured below).

**Optimal:**
- `used[i]` marks nums[i] as already on the path. `go()`: if `len(cur) == n`, append a copy. Else for every i not used: mark, push, recurse, pop, unmark.
- Pruning rule: skip any element that is in use. That cuts the n^n tree down to the tree that has n choices at depth 0, n-1 at depth 1, and so on. Number of calls = sum over k of n!/(n-k)!, which I checked equals 1, 2, 5, 16, 65, 326, 1957 for n = 0..6.
- Swap-in-place variant: no `used` array. Keep `a[:k]` as the fixed prefix; for each i >= k swap `a[k]` and `a[i]`, recurse on k + 1, swap back. It saves the array and the membership test but does not produce the lexicographic order, so you would still sort the result (the code does, and the cross-check compares it).
- Input order does not matter for the answer because the outer list is sorted at the end; the used-array version with input order `[3, 1, 2]` first produces `[3, 1, 2]`.
- Recursion depth is n <= 8 frames plus one.

**Complexity:** n! leaves, each a copy of n items: O(n * n!) time (the internal calls add at most a constant factor: sum of n!/(n-k)! is at most e * n!). Extra space O(n) plus the output O(n * n!). For n = 8 that is 40320 permutations.

**Dry run:** `[3, 1, 2]` (first lines of the tree are printed). place 3 -> place 1 -> place 2 -> leaf `[3, 1, 2]`; back, place 2 -> place 1 -> leaf `[3, 2, 1]`; then place 1 first: `[1, 3, 2]`, `[1, 2, 3]`; then 2 first: `[2, 3, 1]`, `[2, 1, 3]`. Six leaves in tree order; sorted: `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`. The `skip x (used)` lines are the pruned choices.

**Code:**
```python
import itertools
import math
import random

random.seed(1206)

def permutations_used(nums):
    """used-array version. Returns (sorted result, calls)."""
    n = len(nums); out, cur, used, calls = [], [], [False] * n, [0]
    def go():
        calls[0] += 1
        if len(cur) == n:
            out.append(cur[:]); return
        for i in range(n):
            if used[i]:
                continue                    # pruning rule: an element can be placed once
            used[i] = True; cur.append(nums[i])     # choose
            go()                                    # explore
            cur.pop(); used[i] = False              # undo
    go()
    return sorted(out), calls[0]

def permutations_swap(nums):
    """Swap-in-place variant: no used array; the prefix nums[:k] is fixed. Output order is NOT sorted, so we sort."""
    a, out, calls = list(nums), [], [0]
    def go(k):
        calls[0] += 1
        if k == len(a):
            out.append(a[:]); return
        for i in range(k, len(a)):
            a[k], a[i] = a[i], a[k]
            go(k + 1)
            a[k], a[i] = a[i], a[k]
    go(0)
    return sorted(out), calls[0]

def unpruned(nums):
    """No used check: try every element at every position, filter at the leaves. Counts calls only (n <= 6 here)."""
    n = len(nums); calls = [0]; good = [0]
    def go(seq):
        calls[0] += 1
        if len(seq) == n:
            good[0] += len(set(seq)) == n; return
        for i in range(n):
            go(seq + (i,))
    go(())
    return calls[0], good[0]

def brute(nums):
    return sorted(map(list, itertools.permutations(nums)))

examples = [([3, 1, 2], [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]), ([], [[]]), ([9], [[9]]), ([2, 1], [[1, 2], [2, 1]])]
for nums, want in examples:
    assert permutations_used(nums)[0] == want == brute(nums) == permutations_swap(nums)[0]
    print(nums, '->', permutations_used(nums)[0])

# decision tree for [3, 1, 2] (used-array order = input order; the final list is then sorted)
lines = []
def tree(nums, cur=(), depth=0):
    if len(cur) == len(nums):
        lines.append('  ' * depth + 'leaf ' + str(list(cur))); return
    for v in nums:
        if v in cur:
            lines.append('  ' * depth + f'skip {v} (used)'); continue
        lines.append('  ' * depth + f'place {v}')
        tree(nums, cur + (v,), depth + 1)
tree([3, 1, 2])
print('\n'.join(lines[:13])); print('  ...', len(lines), 'lines in all')

# node counts: used array = sum n!/(n-k)!, unpruned = sum n^k
for n in range(0, 7):
    calls = permutations_used(list(range(n)))[1]
    assert calls == sum(math.factorial(n) // math.factorial(n - k) for k in range(n + 1))
    un, good = unpruned(list(range(n))) if n else (1, 1)
    assert good == math.factorial(n) and un == sum(n ** k for k in range(n + 1))
    print(f'n={n} used-array calls={calls:6} unpruned calls={un:6} results={good}')

# seeded cross-check
for _ in range(1000):
    nums = random.sample(range(-9, 10), random.randint(0, 6))
    r = permutations_used(nums)[0]
    assert r == brute(nums) == permutations_swap(nums)[0]
print('random cross-check ok: 1000 cases')

# edge: n = 8 gives 40320 permutations, sorted, all distinct; sorted(nums) first, reversed last
r = permutations_used([5, 3, 8, 1, 9, 2, 7, 4])[0]
assert len(r) == 40320 and r[0] == sorted(r[0]) and r[-1] == sorted(r[0], reverse=True)
assert permutations_used([])[0] == [[]] and permutations_used([-1, 0])[0] == [[-1, 0], [0, -1]]
print('edge asserts ok')
```

**Output (my run):**
```
[3, 1, 2] -> [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
[] -> [[]]
[9] -> [[9]]
[2, 1] -> [[1, 2], [2, 1]]
place 3
  skip 3 (used)
  place 1
    skip 3 (used)
    skip 1 (used)
    place 2
      leaf [3, 1, 2]
  place 2
    skip 3 (used)
    place 1
      leaf [3, 2, 1]
    skip 2 (used)
place 1
  ... 36 lines in all
n=0 used-array calls=     1 unpruned calls=     1 results=1
n=1 used-array calls=     2 unpruned calls=     2 results=1
n=2 used-array calls=     5 unpruned calls=     7 results=2
n=3 used-array calls=    16 unpruned calls=    40 results=6
n=4 used-array calls=    65 unpruned calls=   341 results=24
n=5 used-array calls=   326 unpruned calls=  3906 results=120
n=6 used-array calls=  1957 unpruned calls= 55987 results=720
random cross-check ok: 1000 cases
edge asserts ok
```

**Edge cases:**
- `[]` returns `[[]]` (one empty permutation).
- One element returns `[[9]]`.
- Negative values: fine, the used array tracks indexes, not values.
- n = 8: 40320 lists, first one ascending, last one descending (asserted).
- Duplicates are out of scope for this prompt; with duplicates this code would print repeats (Q19 handles them).

**Follow-ups:**
- Next permutation (Part 1 Q34) steps from one permutation to the next in this same sorted order with O(1) extra space and no recursion: start at the sorted array and call it n! - 1 times.
- Duplicates (Q19): sort and skip `nums[i] == nums[i-1]` when `nums[i-1]` is not used.
- The k-th permutation without listing all: factorial number system, O(n^2).

**Common mistakes:**
- Marking by value (`if v in cur`) with duplicates, or O(n) membership tests inside the loop.
- Forgetting to unmark `used[i]` after the recursive call.
- Appending `cur` instead of a copy.
- Claiming the swap variant is lexicographic.

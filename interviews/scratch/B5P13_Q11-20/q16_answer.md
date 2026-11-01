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

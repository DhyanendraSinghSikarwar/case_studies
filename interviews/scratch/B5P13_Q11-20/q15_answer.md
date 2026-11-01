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

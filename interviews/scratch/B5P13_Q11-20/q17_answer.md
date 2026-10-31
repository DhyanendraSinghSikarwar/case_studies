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

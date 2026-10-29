### Q4 ⭐⭐⭐ 🟡 Subsets (power set) of distinct integers. `nums` has 0 <= len <= 10 distinct integers in any order. Return every subset exactly once. Each subset is a list that keeps the relative order of `nums`; the outer list must be sorted ascending with Python's list comparison (so the empty list comes first and `[1]` comes before `[1, 2]`). `nums = []` returns `[[]]`. Solve it with the include-or-exclude recursion and say how many leaves it has (2^n) and why the total work is O(n * 2^n). Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a bitmask loop over 0..2^n - 1 on small inputs. Example: nums=[4, 1, 7] -> [[], [1], [1, 7], [4], [4, 1], [4, 1, 7], [4, 7], [7]]; nums=[] -> [[]]; nums=[5] -> [[], [5]]; nums=[3, 1] -> [[], [1], [3], [3, 1]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking, include-or-exclude (choose, explore, undo). One binary decision per element.

**Say this first (1 line):** "At each index I either skip the element or take it, then recurse on the next index. That is a binary tree of depth n with 2^n leaves, each leaf is one subset, and copying a leaf costs O(n), so O(n * 2^n) overall."

**Brute force:** Loop `mask` from 0 to 2^n - 1 and build the subset from the set bits. Same O(n * 2^n), no recursion, and it is the oracle in the cross-check. Sorting the outer list at the end costs O(2^n * n log 2^n) comparisons of lists, fine for n <= 10.

**Optimal:**
- `go(i)`: if `i == n`, append a copy of `cur`. Otherwise: first go(i+1) without nums[i] (exclude), then `cur.append(nums[i])`, `go(i+1)`, `cur.pop()` (include, then undo).
- The undo `cur.pop()` restores `cur` so the sibling branch starts clean. Append `cur[:]`, not `cur`, or every answer becomes the same list that ends up empty.
- Each subset keeps the order of `nums` because we decide elements left to right.
- The outer list is sorted at the end with Python's list comparison: `[]` < `[1]` < `[1, 7]` < `[4]` ...
- Pruning rule: there is none. Every branch ends in a valid answer, so there is nothing to cut. The only saving is the start-index variant, where every node (not only the leaf) is an answer: it makes 2^n calls instead of 2^(n+1) - 1. Measured below for n = 0..10: include/exclude makes exactly 2^(n+1) - 1 calls (2047 for n = 10), the start-index version exactly 2^n (1024).
- Recursion depth is n <= 10 frames plus one, far below CPython's default limit of 1000.

**Complexity:** 2^n leaves; each leaf copies a list of up to n items. Time O(n * 2^n) (calls are 2^(n+1) - 1, the copying dominates). Extra space O(n) for the recursion and `cur`, plus the output itself, which is O(n * 2^n) (average n/2 items per subset).

**Dry run:** `nums = [4, 1]` (the program prints the full tree).
- at 4: exclude -> at 1: exclude -> leaf `[]`; include -> leaf `[1]`.
- at 4: include -> at 1: exclude -> leaf `[4]`; include -> leaf `[4, 1]`.
- For `[4, 1, 7]` the same tree has 8 leaves. After sorting: `[[], [1], [1, 7], [4], [4, 1], [4, 1, 7], [4, 7], [7]]`.

**Code:**
```python
import random

random.seed(1204)

def subsets_inc_exc(nums):
    """Include-or-exclude: one yes/no decision per element. Returns (sorted result, number of calls)."""
    out, cur, calls = [], [], [0]
    def go(i):
        calls[0] += 1
        if i == len(nums):
            out.append(cur[:])             # copy: cur keeps changing
            return
        go(i + 1)                           # exclude nums[i]
        cur.append(nums[i])                 # choose
        go(i + 1)                           # explore
        cur.pop()                           # undo
    go(0)
    return sorted(out), calls[0]

def subsets_start_index(nums):
    """Start-index version: every node is an answer, so only 2^n calls."""
    out, cur, calls = [], [], [0]
    def go(start):
        calls[0] += 1
        out.append(cur[:])
        for j in range(start, len(nums)):
            cur.append(nums[j]); go(j + 1); cur.pop()
    go(0)
    return sorted(out), calls[0]

def brute(nums):                           # bitmask loop
    n = len(nums)
    return sorted([nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n))

examples = [([4, 1, 7], [[], [1], [1, 7], [4], [4, 1], [4, 1, 7], [4, 7], [7]]), ([], [[]]), ([5], [[], [5]]), ([3, 1], [[], [1], [3], [3, 1]])]
for nums, want in examples:
    assert subsets_inc_exc(nums)[0] == want == brute(nums) == subsets_start_index(nums)[0]
    print(nums, '->', subsets_inc_exc(nums)[0])

# decision tree for [4, 1] (E = exclude, I = include); leaf = subset
def tree(nums, i=0, cur=(), depth=0):
    pad = '  ' * depth
    if i == len(nums):
        print(f'{pad}leaf {list(cur)}'); return
    print(f'{pad}at {nums[i]}:')
    print(f'{pad} exclude'); tree(nums, i + 1, cur, depth + 1)
    print(f'{pad} include'); tree(nums, i + 1, cur + (nums[i],), depth + 1)
tree([4, 1])

# call counts: 2^(n+1)-1 for include/exclude, 2^n for start-index; there is nothing to prune (every leaf is an answer)
for n in range(0, 11):
    nums = list(range(n))
    assert subsets_inc_exc(nums)[1] == 2 ** (n + 1) - 1
    assert subsets_start_index(nums)[1] == 2 ** n
    assert len(subsets_inc_exc(nums)[0]) == 2 ** n
print('calls for n=10: include/exclude', subsets_inc_exc(list(range(10)))[1], ' start-index', subsets_start_index(list(range(10)))[1])

# seeded cross-check
for _ in range(1500):
    nums = random.sample(range(-9, 10), random.randint(0, 8))
    r = subsets_inc_exc(nums)[0]
    assert r == brute(nums) == subsets_start_index(nums)[0]
    assert len(r) == 2 ** len(nums) and len({tuple(s) for s in r}) == len(r)
print('random cross-check ok: 1500 cases')

# edge: negative and unordered input; n = 10 gives 1024 subsets
assert subsets_inc_exc([-1, 0])[0] == [[], [-1], [-1, 0], [0]]
assert len(subsets_inc_exc(list(range(10)))[0]) == 1024
print('edge asserts ok')
```

**Output (my run):**
```
[4, 1, 7] -> [[], [1], [1, 7], [4], [4, 1], [4, 1, 7], [4, 7], [7]]
[] -> [[]]
[5] -> [[], [5]]
[3, 1] -> [[], [1], [3], [3, 1]]
at 4:
 exclude
  at 1:
   exclude
    leaf []
   include
    leaf [1]
 include
  at 1:
   exclude
    leaf [4]
   include
    leaf [4, 1]
calls for n=10: include/exclude 2047  start-index 1024
random cross-check ok: 1500 cases
edge asserts ok
```

**Edge cases:**
- `[]` returns `[[]]` (one empty subset), not `[]`.
- One element: `[[], [5]]`.
- Negative or unordered input: the elements are in input order inside each subset, only the outer list is sorted.
- n = 10 gives 1024 subsets, which the code asserts.

**Follow-ups:**
- Duplicates in the input (Q18): sort, then skip a value equal to the previous one at the same level.
- Return subsets of size k only (Q20): add a length bound and prune when too few elements remain.
- Count the subsets that sum to a target: that is the knapsack DP (Parts 10 and 11 own counting); here we list them.

**Common mistakes:**
- Appending `cur` instead of `cur[:]`.
- Forgetting the undo, so `cur` keeps growing.
- Returning `[]` for empty input.
- Saying the work is O(2^n): the copying makes it O(n * 2^n).

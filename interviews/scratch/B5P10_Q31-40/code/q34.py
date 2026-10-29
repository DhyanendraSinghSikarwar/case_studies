import bisect
import itertools
import random

random.seed(34)

def lis_table(nums):
    """f[i] = length of the longest strictly increasing subsequence that STARTS at index i. O(n^2)."""
    n = len(nums)
    f = [1] * n
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if nums[j] > nums[i] and f[j] + 1 > f[i]:
                f[i] = f[j] + 1
    return f

def lis_lex_min(nums):
    """Values of the max-length strictly increasing subsequence with the lexicographically smallest index list."""
    n = len(nums)
    if n == 0:
        return []
    f = lis_table(nums)
    need, last, out = max(f), None, []
    for i in range(n):                       # scanning left to right = smallest next index first
        if f[i] == need and (last is None or nums[i] > last):
            out.append(nums[i])
            last = nums[i]
            need -= 1
            if need == 0:
                break
    return out

def lis_patience(nums):
    """O(n log n) with predecessor pointers. A valid LIS, but NOT necessarily the lexicographically smallest."""
    tails_val, tails_idx, pred = [], [], [-1] * len(nums)
    for i, x in enumerate(nums):
        p = bisect.bisect_left(tails_val, x)
        if p == len(tails_val):
            tails_val.append(x); tails_idx.append(i)
        else:
            tails_val[p] = x; tails_idx[p] = i
        pred[i] = tails_idx[p - 1] if p else -1
    out, k = [], tails_idx[-1] if tails_idx else -1
    while k != -1:
        out.append(k)
        k = pred[k]
    out.reverse()
    return out, tails_val                    # index list, tails

def lis_brute(nums):
    n = len(nums)
    for L in range(n, 0, -1):
        cands = [c for c in itertools.combinations(range(n), L)
                 if all(nums[c[t]] < nums[c[t + 1]] for t in range(L - 1))]
        if cands:
            return [nums[i] for i in min(cands)]       # tuples compare lexicographically
    return []

# ---- examples from the prompt
assert lis_lex_min([10, 9, 2, 5, 3, 7, 101, 18]) == [2, 5, 7, 101]
assert lis_lex_min([0, 1, 0, 3, 2, 3]) == [0, 1, 2, 3]
assert lis_lex_min([3, 3, 3]) == [3]
assert lis_lex_min([]) == []
assert lis_lex_min([1, 3, 2, 4]) == [1, 3, 4]
print('examples ok')

# ---- the tables for the first example
ex = [10, 9, 2, 5, 3, 7, 101, 18]
print('nums     :', ex)
print('f (start):', lis_table(ex))
idx, tails = lis_patience(ex)
print('tails    :', tails, '(length 4 is right; here the content happens to be valid too)')
print('patience (pred pointers):', [ex[i] for i in idx], 'indices', idx, '| tie rule:', lis_lex_min(ex))
assert [ex[i] for i in idx] != lis_lex_min(ex)      # both are optimal, different answers
bad = [3, 4, 1]
print('tails for', bad, '=', lis_patience(bad)[1], 'but no increasing subsequence of nums reads 1 then 4: tails is not the answer')

# ---- seeded cross-check against the enumeration with the same tie rule
cases = diff_patience = 0
for _ in range(600):
    n = random.randint(0, 12)
    nums = [random.randint(-4, 8) for _ in range(n)]
    assert lis_lex_min(nums) == lis_brute(nums), nums
    pidx, _t = lis_patience(nums)
    pv = [nums[i] for i in pidx]
    assert len(pv) == len(lis_lex_min(nums))                          # same length
    assert all(pv[t] < pv[t + 1] for t in range(len(pv) - 1))         # a valid strictly increasing subsequence
    assert pidx == sorted(pidx)
    # indices of the tie-rule answer, for comparison of INDEX lists
    f = lis_table(nums); need = max(f, default=0); last = None; li = []
    for i in range(n):
        if need and f[i] == need and (last is None or nums[i] > last):
            li.append(i); last = nums[i]; need -= 1
    if pidx != li:
        diff_patience += 1
    cases += 1
print('cross-check passed on', cases, 'cases; patience index list differs from the tie rule on', diff_patience)

# ---- edge cases
assert lis_lex_min([5]) == [5]
assert lis_lex_min([5, 4, 3, 2, 1]) == [5]                  # all equal length 1: smallest index
assert lis_lex_min([1, 2, 3, 4]) == [1, 2, 3, 4]
assert lis_lex_min([2, 2, 3, 3]) == [2, 3]
assert len(lis_lex_min(list(range(2000)))) == 2000
print('edge cases ok')

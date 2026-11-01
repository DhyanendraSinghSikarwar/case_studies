import random
from collections import Counter


def dups_brute(nums):
    c = Counter(nums)
    return sorted(v for v, cnt in c.items() if cnt == 2)


def dups_inplace(nums):
    """Mark value v by negating nums[v-1]. A second visit sees a negative."""
    out = []
    for x in nums:
        v = abs(x)                      # x may already be negated by a marker
        if nums[v - 1] < 0:
            out.append(v)               # seen before
        else:
            nums[v - 1] = -nums[v - 1]
    for i in range(len(nums)):          # restore the input
        nums[i] = abs(nums[i])
    return out


a = [4, 3, 2, 7, 8, 2, 3, 1]
orig = a[:]
res = dups_inplace(a)
print("duplicates:", res, "| input restored:", a == orig)
assert res == [2, 3] and a == orig

# --- edge cases
assert dups_inplace([]) == []
assert dups_inplace([1]) == []
assert dups_inplace([1, 1]) == [1]
assert dups_inplace([1, 2, 3]) == []
assert dups_inplace([2, 2]) == [2]
assert sorted(dups_inplace([1, 1, 2, 2])) == [1, 2]   # stays valid: 3, 4 missing
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(27)
for _ in range(2000):
    n = rng.randint(0, 10)
    pool = list(range(1, n + 1)) * 2     # each value at most twice
    rng.shuffle(pool)
    nums = pool[:n]
    before = nums[:]
    got = sorted(dups_inplace(nums))
    assert got == dups_brute(before), before
    assert nums == before                # restored
print("2000 random cases OK")

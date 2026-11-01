import random


def remove_brute(nums, val):
    """Build a new list of kept values (extra O(n) space)."""
    return [x for x in nums if x != val]


def remove_stable(nums, val):
    """Write pointer: keeps order. Returns (k, writes)."""
    w = 0
    writes = 0
    for x in nums:
        if x != val:
            nums[w] = x
            w += 1
            writes += 1
    return w, writes


def remove_swap(nums, val):
    """Overwrite a match with the last live value. Order changes.
    Returns (k, writes). Writes == number of matches."""
    i, n = 0, len(nums)
    writes = 0
    while i < n:
        if nums[i] == val:
            nums[i] = nums[n - 1]
            n -= 1
            writes += 1
            # do NOT advance i: the swapped-in value is unchecked
        else:
            i += 1
    return n, writes


# --- the example from the prompt
a = [3, 2, 2, 3]
k, _ = remove_stable(a, 3)
print("stable  [3,2,2,3] val=3 ->", k, a[:k])
assert k == 2 and a[:k] == [2, 2]
a = [3, 2, 2, 3]
k, _ = remove_swap(a, 3)
print("swap    [3,2,2,3] val=3 ->", k, a[:k])
assert k == 2 and sorted(a[:k]) == [2, 2]

# --- writes: rare matches
big = list(range(1, 11))          # one match, at the front
s1, s2 = big[:], big[:]
k1, w1 = remove_stable(s1, 1)
k2, w2 = remove_swap(s2, 1)
print("rare match  : stable writes =", w1, " swap writes =", w2)
assert (w1, w2) == (9, 1)
# many matches: swap does more writes than stable when matches dominate
mostly = [7] * 9 + [1]
s1, s2 = mostly[:], mostly[:]
k1, w1 = remove_stable(s1, 7)
k2, w2 = remove_swap(s2, 7)
print("many matches: stable writes =", w1, " swap writes =", w2)
assert (w1, w2) == (1, 9)

# --- edge cases
for nums, val in [([], 1), ([1], 1), ([1], 2), ([2, 2, 2], 2),
                  ([2, 2, 2], 3), ([0, 0, 1], 0), ([-1, -1, 5], -1)]:
    want = remove_brute(nums, val)
    a = nums[:]
    k, _ = remove_stable(a, val)
    assert a[:k] == want
    a = nums[:]
    k, _ = remove_swap(a, val)
    assert sorted(a[:k]) == sorted(want)
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(21)
for _ in range(1000):
    n = rng.randint(0, 12)
    nums = [rng.randint(-3, 3) for _ in range(n)]
    val = rng.randint(-3, 3)
    want = remove_brute(nums, val)
    a = nums[:]
    k, wr = remove_stable(a, val)
    assert k == len(want) and a[:k] == want
    a = nums[:]
    k, wr = remove_swap(a, val)
    assert k == len(want) and sorted(a[:k]) == sorted(want)
    assert wr == nums.count(val)
print("1000 random cases OK")

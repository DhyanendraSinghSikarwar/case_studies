import random
from itertools import permutations


def brute(a):
    """Enumerate distinct permutations in order; take the one after a (wrap to the smallest)."""
    perms = sorted(set(permutations(a)))
    i = perms.index(tuple(a))
    return list(perms[(i + 1) % len(perms)])


def next_permutation(a):
    n = len(a)
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:     # >= so equal values are skipped (duplicates)
        i -= 1
    if i >= 0:
        j = n - 1
        while a[j] <= a[i]:                # rightmost value strictly greater than the pivot
            j -= 1
        a[i], a[j] = a[j], a[i]
    a[i + 1:] = a[i + 1:][::-1]            # suffix was non-increasing: reverse to ascending
    return a


for ex, want in [([1, 2, 3], [1, 3, 2]), ([3, 2, 1], [1, 2, 3]), ([1, 1, 5], [1, 5, 1])]:
    got = next_permutation(ex[:])
    print(ex, "->", got)
    assert got == want

# Trace of a longer one
a = [1, 5, 8, 4, 7, 6, 5, 3, 1]
print(a, "->", next_permutation(a[:]))
assert next_permutation(a[:]) == [1, 5, 8, 5, 1, 3, 4, 6, 7]

# Edge cases
assert next_permutation([]) == []
assert next_permutation([7]) == [7]
assert next_permutation([2, 2, 2]) == [2, 2, 2]
assert next_permutation([1, 2]) == [2, 1]
assert next_permutation([2, 1]) == [1, 2]
assert next_permutation([1, 3, 2]) == [2, 1, 3]
assert next_permutation([-1, 0, -1]) == [0, -1, -1]

# Applying it repeatedly walks every distinct permutation exactly once, then wraps
a = [1, 1, 2, 2]
seen = [tuple(a)]
for _ in range(6):
    next_permutation(a)
    seen.append(tuple(a))
print("walk of [1,1,2,2]:", seen)
assert len(set(seen[:6])) == 6 and len(seen) == 7 and seen[-1] == seen[0]

rng = random.Random(34)
for _ in range(1500):
    a = [rng.randint(0, 3) for _ in range(rng.randint(1, 7))]
    assert next_permutation(a[:]) == brute(a), a
print("cross-check passed: 1500 random lists (duplicates included)")

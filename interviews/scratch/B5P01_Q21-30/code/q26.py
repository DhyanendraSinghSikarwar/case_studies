import random


def longest_brute(nums):
    best = 0
    for i in range(len(nums)):
        bal = 0
        for j in range(i, len(nums)):
            bal += 1 if nums[j] == 1 else -1
            if bal == 0:
                best = max(best, j - i + 1)
    return best


def longest_hash(nums):
    first = {0: -1}               # balance 0 before index 0
    bal = best = 0
    for i, x in enumerate(nums):
        bal += 1 if x == 1 else -1
        if bal in first:
            best = max(best, i - first[bal])
        else:
            first[bal] = i        # earliest index gives the longest span
    return best


for arr, want in [([0, 1], 2), ([0, 1, 0], 2), ([0, 0, 1, 0, 0, 0, 1, 1], 6)]:
    got = longest_hash(arr)
    print(arr, "->", got)
    assert got == want == longest_brute(arr)

# --- edge cases
assert longest_hash([]) == 0
assert longest_hash([0]) == 0 and longest_hash([1]) == 0
assert longest_hash([0, 0, 0]) == 0
assert longest_hash([1, 1, 1, 1]) == 0
assert longest_hash([1, 0, 1, 0, 1, 0]) == 6
assert longest_hash([1, 1, 0, 0]) == 4
assert longest_hash([0, 0, 0, 1, 1]) == 4
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(26)
for _ in range(2000):
    arr = [rng.randint(0, 1) for _ in range(rng.randint(0, 14))]
    assert longest_hash(arr) == longest_brute(arr), arr
print("2000 random cases OK")

import random


def two_sum_brute(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum(nums, target):
    seen = {}  # value -> index of an earlier element
    for j, x in enumerate(nums):
        i = seen.get(target - x)
        if i is not None:
            return (i, j)
        seen[x] = j  # insert AFTER the check: an element never pairs with itself
    return None


print("example 1:", two_sum([2, 7, 11, 15], 9), "(expected (0, 1))")
print("example 2:", two_sum([3, 3], 6), "(expected (0, 1))")
print("single 3, target 6:", two_sum([3], 6), "(no pair, element not reused)")

random.seed(2)
cases = 0
for _ in range(1000):
    n = random.randint(2, 9)
    a = [random.randint(-5, 5) for _ in range(n)]
    i, j = random.sample(range(n), 2)
    t = a[i] + a[j]
    # the prompt guarantees exactly one pair; skip inputs with several valid pairs
    pairs = [(p, q) for p in range(n) for q in range(p + 1, n) if a[p] + a[q] == t]
    if len(pairs) != 1:
        continue
    cases += 1
    assert two_sum(a, t) == two_sum_brute(a, t) == pairs[0], (a, t)
print("cross-check: %d seeded unique-pair cases agree" % cases)

# with several valid pairs both may differ in WHICH pair they return, but both must be valid
for _ in range(500):
    a = [random.randint(-3, 3) for _ in range(random.randint(2, 8))]
    t = random.randint(-6, 6)
    r1, r2 = two_sum(a, t), two_sum_brute(a, t)
    assert (r1 is None) == (r2 is None)
    if r1:
        assert r1[0] != r1[1] and a[r1[0]] + a[r1[1]] == t
print("validity check on inputs with many pairs: ok")

assert two_sum([3, 3], 6) == (0, 1)
assert two_sum([3, 2, 4], 6) == (1, 2)  # 3 + 3 would reuse index 0
assert two_sum([0, 4, 3, 0], 0) == (0, 3)
assert two_sum([-1, -2, -3, -4, -5], -8) == (2, 4)
assert two_sum([5], 10) is None
print("edge asserts passed")

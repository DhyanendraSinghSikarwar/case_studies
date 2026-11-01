import random


def missing_set(nums):
    s = set(nums)
    for v in range(len(nums) + 1):
        if v not in s:
            return v


def missing_sort(nums):
    s = sorted(nums)
    for i, v in enumerate(s):
        if v != i:
            return i
    return len(s)


def missing_sum(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)


print("example 1:", missing_sum([3, 0, 1]), "(expected 2)")
print("example 2:", missing_sum([0, 1]), "(expected 2)")

random.seed(8)
for _ in range(1000):
    n = random.randint(0, 12)
    full = list(range(n + 1))
    miss = random.choice(full)
    a = [v for v in full if v != miss]
    random.shuffle(a)
    assert missing_set(a) == missing_sort(a) == missing_sum(a) == miss, a
print("cross-check: 1000 seeded cases agree")

assert missing_sum([]) == 0 and missing_set([]) == 0 and missing_sort([]) == 0
assert missing_sum([1]) == 0 and missing_sum([0]) == 1
assert missing_sort([0, 1, 2, 3]) == 4
# large n: Python ints never overflow, the sum stays exact
n = 10**6
big = list(range(n + 1))
big.remove(123456)
assert missing_sum(big) == 123456
print("n = 10**6 sum formula exact:", missing_sum(big))
# what a 32-bit language would see: n*(n+1)/2 for n=10**5 is 5000050000 > 2**31-1
n32 = 10**5
total = n32 * (n32 + 1) // 2
wrapped = (total + 2**31) % 2**32 - 2**31  # simulate signed 32-bit wrap
print("n=10**5: true sum", total, "| as signed int32", wrapped, "| int32 max", 2**31 - 1)
print("edge asserts passed")

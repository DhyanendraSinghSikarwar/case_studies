import random
from collections import Counter


def fruit_brute(fruits):
    best = 0
    for i in range(len(fruits)):
        seen = set()
        for j in range(i, len(fruits)):
            seen.add(fruits[j])
            if len(seen) > 2:
                break
            best = max(best, j - i + 1)
    return best


def fruit_window(fruits, baskets=2):
    count = Counter()
    left = best = 0
    for right, f in enumerate(fruits):
        count[f] += 1
        while len(count) > baskets:
            g = fruits[left]
            count[g] -= 1
            if count[g] == 0:
                del count[g]  # without this, len(count) never shrinks
            left += 1
        best = max(best, right - left + 1)
    return best


print("[1,2,1]:", fruit_window([1, 2, 1]), "(expected 3)")
print("[0,1,2,2]:", fruit_window([0, 1, 2, 2]), "(expected 3)")
print("[1,2,3,2,2]:", fruit_window([1, 2, 3, 2, 2]), "(expected 4)")

# what happens if you forget to delete zero-count keys
def fruit_buggy(fruits):
    count = Counter()
    left = best = 0
    for right, f in enumerate(fruits):
        count[f] += 1
        while len(count) > 2:
            count[fruits[left]] -= 1  # key stays with value 0
            left += 1
        best = max(best, right - left + 1)
    return best


try:
    print("buggy (no delete):", fruit_buggy([1, 2, 3, 2, 2]))
except IndexError:
    print("buggy (no delete) on [1,2,3,2,2]: IndexError (len(count) stays 3, left runs off the end)")

random.seed(24)
for _ in range(1000):
    n = random.randint(0, 12)
    fr = [random.randint(0, 3) for _ in range(n)]
    assert fruit_window(fr) == fruit_brute(fr), fr
print("cross-check: 1000 seeded cases agree")

assert fruit_window([]) == 0
assert fruit_window([5]) == 1
assert fruit_window([7, 7, 7, 7]) == 4
assert fruit_window([1, 2, 3]) == 2
assert fruit_window([1, 2, 1, 2, 1, 2]) == 6
assert fruit_window(list(range(10 ** 5))) == 2
assert fruit_window([1, 2] * 50000) == 10 ** 5
print("edge asserts passed")

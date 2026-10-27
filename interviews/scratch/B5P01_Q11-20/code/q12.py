import random

def brute(nums):
    s = set(nums)
    best = 0
    for x in s:                      # try every value as a start, walk up
        y = x
        while y in s:
            y += 1
        best = max(best, y - x)
    return best

def optimal(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 in s:               # not a run start, skip
            continue
        y = x + 1
        while y in s:
            y += 1
        best = max(best, y - x)
    return best

assert optimal([100, 4, 200, 1, 3, 2]) == 4
assert optimal([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert optimal([]) == 0
assert optimal([7]) == 1
assert optimal([5, 5, 5]) == 1
assert optimal([-2, -1, 0, 1]) == 4
assert optimal([10**9, -10**9]) == 1
assert optimal([1, 3, 5, 7]) == 1
assert optimal(list(range(100000))) == 100000

rng = random.Random(12)
for _ in range(500):
    a = [rng.randint(-10, 10) for _ in range(rng.randint(0, 15))]
    assert optimal(a) == brute(a), a
# independent oracle: sort and scan
def by_sort(nums):
    u = sorted(set(nums))
    best = cur = 0
    for i, v in enumerate(u):
        cur = cur + 1 if i and v == u[i - 1] + 1 else 1
        best = max(best, cur)
    return best
for _ in range(500):
    a = [rng.randint(-10, 10) for _ in range(rng.randint(0, 15))]
    assert optimal(a) == by_sort(a)
print("1000 random cases agree")
print(optimal([100, 4, 200, 1, 3, 2]), optimal([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))

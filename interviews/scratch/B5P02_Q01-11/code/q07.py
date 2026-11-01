import random


def water_brute(h):
    best = 0
    for i in range(len(h)):
        for j in range(i + 1, len(h)):
            best = max(best, (j - i) * min(h[i], h[j]))
    return best


def water_two_pointers(h):
    i, j = 0, len(h) - 1
    best = 0
    while i < j:
        best = max(best, (j - i) * min(h[i], h[j]))
        if h[i] < h[j]:
            i += 1          # shorter line cannot do better with any narrower partner
        else:
            j -= 1
    return best


print(water_two_pointers([1, 8, 6, 2, 5, 4, 8, 3, 7]))
print(water_two_pointers([1, 1]))
assert water_two_pointers([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
assert water_two_pointers([1, 1]) == 1
assert water_two_pointers([0, 0]) == 0              # zero heights
assert water_two_pointers([5, 5, 5, 5]) == 15       # all equal: widest wins
assert water_two_pointers([1, 2, 3, 4]) == 4        # rising
assert water_two_pointers([4, 3, 2, 1]) == 4        # falling
assert water_two_pointers([2, 0, 0, 0, 2]) == 8
assert water_two_pointers([3] * 100000) == 3 * 99999

rng = random.Random(2)
cases = 0
for _ in range(3000):
    n = rng.randint(2, 10)
    h = [rng.randint(0, 9) for _ in range(n)]
    assert water_two_pointers(h) == water_brute(h), h
    cases += 1
print("random cross-check passed:", cases, "cases")

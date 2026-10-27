import itertools
import random


def can_place(s, c, d):
    """Greedy on sorted stalls: put a cow at the first stall, then next stall >= d further."""
    placed, last = 1, s[0]
    for x in s[1:]:
        if x - last >= d:
            placed += 1
            last = x
            if placed == c:
                return True
    return placed >= c


def aggressive_cows(stalls, c):
    s = sorted(stalls)
    lo, hi = 1, (s[-1] - s[0]) // (c - 1)    # d=1 always works (distinct ints); d can't exceed span/(c-1)
    while lo < hi:
        mid = (lo + hi + 1) // 2              # upper-biased mid: lo = mid must make progress
        if can_place(s, c, mid):
            lo = mid                          # mid works: answer is mid or bigger
        else:
            hi = mid - 1
    return lo


def cows_brute(stalls, c):
    s = sorted(stalls)
    return max(min(b - a for a, b in zip(sub, sub[1:])) for sub in itertools.combinations(s, c))


def stuck_with_lower_mid(stalls, c, cap=50):
    """Shows why (lo+hi)//2 fails with lo = mid: counts loop turns, gives up at cap."""
    s = sorted(stalls)
    lo, hi, turns = 1, (s[-1] - s[0]) // (c - 1), 0
    while lo < hi and turns < cap:
        mid = (lo + hi) // 2
        if can_place(s, c, mid):
            lo = mid
        else:
            hi = mid - 1
        turns += 1
    return turns >= cap


examples = [([1, 2, 4, 8, 9], 3, 3), ([1, 2, 3, 4, 7], 3, 3),
            ([5, 4, 3, 2, 1, 10**9], 2, 10**9 - 1), ([1, 2], 2, 1)]
for stalls, c, exp in examples:
    got = aggressive_cows(stalls, c)
    assert got == exp == cows_brute(stalls, c)
    print(stalls, "c =", c, "->", got)

random.seed(20)
for _ in range(1500):
    n = random.randint(2, 9)
    stalls = random.sample(range(0, 30), n)
    c = random.randint(2, n)
    assert aggressive_cows(stalls, c) == cows_brute(stalls, c), (stalls, c)
print("cross-check: 1500 seeded cases agree with the brute force over all subsets")

# predicate shape: True...True False...False (opposite of Koko's False...True)
for _ in range(200):
    s = sorted(random.sample(range(0, 60), random.randint(2, 10)))
    c = random.randint(2, len(s))
    row = [can_place(s, c, d) for d in range(1, 62)]
    assert row == sorted(row, reverse=True)
print("monotone check: can_place(d) is True then False in d (200 seeded cases)")

print("lower mid + lo = mid never finishes on [1,2,3,4,9], c=2:", stuck_with_lower_mid([1, 2, 3, 4, 9], 2))
assert stuck_with_lower_mid([1, 2, 3, 4, 9], 2) is True
assert aggressive_cows([1, 2, 3, 4, 9], 2) == 8

# edge cases
assert aggressive_cows([1, 2], 2) == 1
assert aggressive_cows([1, 2, 3, 4, 5], 5) == 1          # c == n: all stalls used
assert aggressive_cows([1, 10**9], 2) == 10**9 - 1
assert aggressive_cows([0, 5, 10], 3) == 5
big = random.sample(range(0, 10**9), 10**5)
assert aggressive_cows(big, 2) == max(big) - min(big)
assert aggressive_cows(list(range(0, 10**5)), 10**5) == 1
print("edge asserts passed")

import random

MOD = 10**9 + 7


def sum_min_brute(arr):
    total = 0
    for i in range(len(arr)):
        cur = arr[i]
        for j in range(i, len(arr)):
            cur = min(cur, arr[j])
            total += cur
    return total % MOD


def sum_min(arr):
    n = len(arr)
    stack = []                                       # indices, values strictly increasing
    total = 0
    for i in range(n + 1):
        cur = arr[i] if i < n else 0                 # sentinel below every positive value
        while stack and arr[stack[-1]] >= cur:
            j = stack.pop()
            left = stack[-1] if stack else -1        # previous strictly smaller
            total += arr[j] * (j - left) * (i - j)   # i = next smaller-or-equal
        stack.append(i)
    return total % MOD


def sum_min_both_strict(arr):                        # the bug: previous-smaller AND next-smaller, both strict
    n = len(arr)
    total = 0
    for j in range(n):
        L = j - 1
        while L >= 0 and arr[L] >= arr[j]:
            L -= 1
        R = j + 1
        while R < n and arr[R] >= arr[j]:
            R += 1
        total += arr[j] * (j - L) * (R - j)
    return total % MOD


examples = [([3, 1, 2, 4], 17), ([11, 81, 94, 43, 3], 444), ([2, 2, 2], 12)]
for a, want in examples:
    got = sum_min(a)
    assert got == sum_min_brute(a) == want, (a, got)
    print(a, "->", got)

print("tie rule broken (both sides strict) on [2,2,2] ->", sum_min_both_strict([2, 2, 2]), "(over-counts; correct is 12)")
assert sum_min_both_strict([2, 2, 2]) == 20 and sum_min([2, 2, 2]) == 12

assert sum_min([7]) == 7
assert sum_min([1, 2, 3, 4]) == sum_min_brute([1, 2, 3, 4]) == 20
assert sum_min([4, 3, 2, 1]) == sum_min_brute([4, 3, 2, 1]) == 20
assert sum_min([5] * 100) == 5 * (100 * 101 // 2) % MOD
big = [10**9] * 50                                  # forces the modulus to matter
assert sum_min(big) == sum_min_brute(big)
assert sum_min(big) != 10**9 * (50 * 51 // 2)

rng = random.Random(29)
for _ in range(600):
    a = [rng.randint(1, 5) for _ in range(rng.randint(1, 14))]
    assert sum_min(a) == sum_min_brute(a), a
for _ in range(60):
    a = [rng.randint(1, 10**9) for _ in range(rng.randint(1, 200))]
    assert sum_min(a) == sum_min_brute(a)
n_max = [rng.randint(1, 30000) for _ in range(30000)]
r = sum_min(n_max)
assert 0 <= r < MOD
print("random cross-check passed: 600 small (many ties), 60 large-valued, one n=30000 run ->", r)

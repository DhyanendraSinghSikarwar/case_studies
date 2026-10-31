import random


def cut_brute(logs, k):
    # try every L from big to small; first one that gives >= k pieces wins
    for L in range(max(logs), 0, -1):
        if sum(x // L for x in logs) >= k:
            return L
    return 0


def pieces(logs, L):
    return sum(x // L for x in logs)        # non-increasing in L


def cut_logs(logs, k):
    lo, hi = 0, max(logs)                   # lo = 0 means "no valid L yet"; lo is always feasible (0 by convention)
    while lo < hi:                          # last True of: L == 0 or pieces(L) >= k
        mid = (lo + hi + 1) // 2            # upper-biased so lo = mid always makes progress
        if pieces(logs, mid) >= k:
            lo = mid
        else:
            hi = mid - 1
    return lo


for logs, k, want in [([232, 124, 456], 7, 114), ([5, 5, 5], 2, 5), ([1, 2], 10, 0), ([5, 5, 5], 3, 5), ([5, 5, 5], 4, 2)]:
    assert cut_logs(logs, k) == cut_brute(logs, k) == want, (logs, k)
    print(logs, "k =", k, "->", cut_logs(logs, k))

rng = random.Random(27)
zero = 0
for _ in range(2000):
    logs = [rng.randint(1, 30) for _ in range(rng.randint(1, 6))]
    k = rng.randint(1, 40)
    got, want = cut_logs(logs, k), cut_brute(logs, k)
    assert got == want, (logs, k, got, want)
    if got:
        assert pieces(logs, got) >= k and pieces(logs, got + 1) < k     # largest feasible L
    zero += got == 0
    # monotone: pieces never increases as L grows
    assert all(pieces(logs, L) >= pieces(logs, L + 1) for L in range(1, 31))
print("random check passed: 2000 cases,", zero, "returned 0; pieces(L) was non-increasing every time")

# edge cases
assert cut_logs([1], 1) == 1 and cut_logs([1], 2) == 0
assert cut_logs([10 ** 9], 1) == 10 ** 9 and cut_logs([10 ** 9], 10 ** 9) == 1 and cut_logs([10 ** 9], 10 ** 9 + 1) == 0
assert cut_logs([10 ** 9] * 10 ** 5, 10 ** 5) == 10 ** 9
assert cut_logs([7, 7, 7], 21) == 1 and cut_logs([7, 7, 7], 22) == 0
print("edge asserts passed")

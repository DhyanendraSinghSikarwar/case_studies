import itertools
import random

random.seed(36)
MOD = 10**9 + 7

def dice(n, k, target):
    """dp[s] = number of ordered outcomes of the dice thrown so far with sum s (s <= target)."""
    dp = [0] * (target + 1)
    dp[0] = 1                                   # zero dice: the empty sequence has sum 0
    for _ in range(n):
        nd = [0] * (target + 1)                 # a NEW array per die: no in-place hazard
        for s in range(target + 1):
            if dp[s]:
                for f in range(1, min(k, target - s) + 1):
                    nd[s + f] = (nd[s + f] + dp[s]) % MOD
        dp = nd
    return dp[target]

def dice_prefix(n, k, target):
    """Same answer in O(n * target) with a sliding window sum instead of the inner loop over faces."""
    dp = [1] + [0] * target
    for _ in range(n):
        nd = [0] * (target + 1)
        window = 0
        for s in range(1, target + 1):
            window += dp[s - 1]
            if s - 1 - k >= 0:
                window -= dp[s - 1 - k]
            nd[s] = window % MOD
            window %= MOD
        dp = nd
    return dp[target]

def brute(n, k, target):
    return sum(1 for r in itertools.product(range(1, k + 1), repeat=n) if sum(r) == target) % MOD

# ---- examples from the prompt
assert dice(1, 6, 3) == 1
assert dice(2, 6, 7) == 6
assert dice(30, 30, 500) == 222616187
assert dice(2, 5, 1) == 0
print('examples ok')

# ---- table for n = 2, k = 6, target = 7 (rows = dice thrown, columns = sums 0..7)
dp = [1] + [0] * 7
print('sum:      ', list(range(8)))
print('0 dice:   ', dp)
for d in (1, 2):
    nd = [0] * 8
    for s in range(8):
        for f in range(1, 7):
            if s + f <= 7:
                nd[s + f] += dp[s]
    dp = nd
    print(f'{d} dice:   ', dp)
assert dp[7] == 6

# ---- seeded cross-check against the enumeration of all k^n outcomes (k^n <= 10^5)
cases = 0
for _ in range(400):
    k = random.randint(1, 8)
    n = random.randint(1, 30)
    while k ** n > 10**5:
        n -= 1
    n = max(n, 1)
    t = random.randint(0, n * k + 3)
    exp = brute(n, k, t)
    assert dice(n, k, t) == exp == dice_prefix(n, k, t), (n, k, t)
    cases += 1
for n in range(1, 6):                      # exhaustive tiny sweep
    for k in range(1, 6):
        for t in range(0, n * k + 3):
            assert dice(n, k, t) == brute(n, k, t) == dice_prefix(n, k, t)
            cases += 1
print('cross-check passed on', cases, 'cases')

# ---- 0 outside n..n*k, and the modulus matters at the full size
assert all(dice(4, 6, t) == 0 for t in list(range(0, 4)) + list(range(25, 40)))
assert all(dice(4, 6, t) > 0 for t in range(4, 25))
assert dice(30, 30, 1000) == 0 and dice(30, 30, 30) == 1 and dice(30, 30, 900) == 1
big = dice(30, 30, 465)
exact = [1] + [0] * 465
for _ in range(30):                          # same DP with Python big ints and no modulus
    nd = [0] * 466
    for t in range(466):
        for f in range(1, 31):
            if t - f >= 0:
                nd[t] += exact[t - f]
    exact = nd
print('n=30, k=30, target=465: mod answer', big, '| exact count has', len(str(exact[465])), 'digits')
assert exact[465] % MOD == big and exact[465] > MOD
assert dice_prefix(30, 30, 465) == big
print('edge cases ok')

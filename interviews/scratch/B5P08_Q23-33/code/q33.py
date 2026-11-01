import itertools, random

def tables(coins, limit):
    opt = [0] + [10**9] * limit; gr = [0] * (limit + 1)
    for a in range(1, limit + 1):
        opt[a] = min(opt[a - c] + 1 for c in coins if c <= a)      # fewest-coins DP (Part 10 topic)
        r, g = a, 0
        for c in reversed(coins): g += r // c; r %= c               # largest-first greedy
        gr[a] = g
    return opt, gr

def first_bad(coins):                                                # uses the Kozen-Zaks bound
    limit = coins[-1] + (coins[-2] if len(coins) > 1 else 0)
    opt, gr = tables(coins, limit)
    for a in range(1, limit + 1):
        if gr[a] > opt[a]: return a
    return -1

def brute(coins, limit=200):                                         # no theorem: test a long range
    opt, gr = tables(coins, limit)
    for a in range(1, limit + 1):
        if gr[a] > opt[a]: return a
    return -1

assert first_bad([1,3,4]) == 6
assert first_bad([1,5,10,25]) == -1
assert first_bad([1,5,6,9]) == 11
assert first_bad([1]) == -1
assert first_bad([1,2,5,10,20,50,100]) == -1

# exhaustive: every coin system with largest coin <= 12 (1 plus any subset of 2..12), amounts to 200
systems = bad = 0
lower_ok = True
for mask in range(1 << 11):
    coins = [1] + [c for c in range(2, 13) if mask >> (c - 2) & 1]
    systems += 1
    a, b = first_bad(coins), brute(coins, 200)
    assert a == b, coins
    if b != -1:
        bad += 1
        m = len(coins)
        assert b < coins[-1] + coins[-2], coins                      # Kozen-Zaks upper bound
        if m >= 3: assert b > coins[2] + 1, coins                    # lower bound c_3 + 1 (1-indexed c_3)
print(f"{systems} coin systems (largest <= 12): bound-limited check == range-200 check; {bad} non-canonical, all with first failure < c_m + c_(m-1) and > c_3 + 1")

# larger random systems: bound against a long range (amount to 600)
rng = random.Random(33)
for _ in range(300):
    coins = sorted({1} | {rng.randint(2, 80) for _ in range(rng.randint(1, 5))})
    assert first_bad(coins) == brute(coins, 600), coins
print("300 random systems (coins <= 80, amounts to 600): same answer")

# the tightness of the bound can be seen on [1, 3, 4]: first failure 6 < 4 + 3 = 7
print("[1,3,4] ->", first_bad([1,3,4]), "| [1,5,6,9] ->", first_bad([1,5,6,9]), "| US [1,5,10,25] ->", first_bad([1,5,10,25]))
opt, gr = tables([1,5,6,9], 12)
print("[1,5,6,9] amount 11: greedy", gr[11], "coins, optimum", opt[11], "coins")

# 'looks fine on a few examples': coins [1,5,6,9] is greedy-optimal for every amount below 11
print("amounts below 11 where greedy is fine:", all(gr[a] == opt[a] for a in range(1, 11)))

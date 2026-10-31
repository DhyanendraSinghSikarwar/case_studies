import random

random.seed(3001)


def solve(items, target):
    n = len(items)
    found = []
    for mask in range(1 << n):                       # increasing mask order
        total = 0
        for i in range(n):
            if mask >> i & 1:                        # bit i set = take items[i]
                total += items[i]
        if total == target:
            found.append([items[i] for i in range(n) if mask >> i & 1])
    pairs = 0
    for mask in range(1 << n):
        sub = mask
        while sub:                                   # non-empty submasks only
            pairs += 1
            sub = (sub - 1) & mask                   # next smaller submask of mask
    return [found, pairs]


def brute(items, target):
    n = len(items)
    all_subsets = [[items[i] for i in range(n) if (m >> i) % 2 == 1] for m in range(1 << n)]
    found = [s for s in all_subsets if sum(s) == target]
    pairs = sum(1 for m in range(1 << n) for s in range(1, 1 << n) if s & m == s)   # double loop
    return [found, pairs]


# dry run: submasks of m = 0b1011 (11) in the order the loop visits them
m, sub, order = 0b1011, 0b1011, []
while sub:
    order.append(format(sub, "04b"))
    sub = (sub - 1) & m
print("submasks of 1011:", order, "count", len(order), "= 2^3 - 1")

# dry run: items [3, 1, 4, 2], target 5 -> which masks hit
items = [3, 1, 4, 2]
for mask in range(16):
    pick = [items[i] for i in range(4) if mask >> i & 1]
    if sum(pick) == 5:
        print(f"mask {mask:>2} = {mask:04b} takes {pick} sum 5")

for it, tg, want in [([3, 1, 4, 2], 5, [[[1, 4], [3, 2]], 65]), ([], 0, [[[]], 0]),
                     ([1, -1, 2], 0, [[[], [1, -1]], 19]), ([5], 3, [[], 1])]:
    got = solve(it, tg)
    assert got == want == brute(it, tg), (it, tg, got)
    print(it, tg, "->", got)

# pairs = 3^n - 2^n for every n up to 12 (runs the real loop)
for n in range(13):
    assert solve(list(range(n)), 10**9)[1] == 3**n - 2**n
print("pairs == 3^n - 2^n for n = 0..12; at n = 12 that is", 3**12 - 2**12)

# submask claim: decreasing order, each exactly once, for every m < 256
for m in range(256):
    seen, sub = [], m
    while sub:
        seen.append(sub)
        sub = (sub - 1) & m
    assert seen == sorted((s for s in range(1, 256) if s & m == s), reverse=True)

# seeded random cross-check
for _ in range(300):
    n = random.randint(0, 7)
    it = random.sample(range(-100, 101), n)
    tg = random.choice([0, random.randint(-20, 20), sum(random.sample(it, random.randint(0, n))) if n else 0])
    assert solve(it, tg) == brute(it, tg)
print("300 seeded random cases ok; submask order claim ok for every m < 256")
assert solve([], 0) == [[[]], 0] and solve([0], 0)[0] == [[], [0]]
print("edge asserts ok")

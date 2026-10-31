import random

def brute(h):
    # for each bar: water = min(max to left incl, max to right incl) - h[i]
    total = 0
    for i in range(len(h)):
        total += min(max(h[:i + 1]), max(h[i:])) - h[i]
    return total

def prefix_suffix(h):
    n = len(h)
    if n == 0:
        return 0
    lm = [0] * n
    rm = [0] * n
    lm[0] = h[0]
    for i in range(1, n):
        lm[i] = max(lm[i - 1], h[i])
    rm[-1] = h[-1]
    for i in range(n - 2, -1, -1):
        rm[i] = max(rm[i + 1], h[i])
    return sum(min(lm[i], rm[i]) - h[i] for i in range(n))

def optimal(h):
    l, r = 0, len(h) - 1
    lmax = rmax = 0
    water = 0
    while l < r:
        if h[l] < h[r]:
            # a right wall at least as tall as h[l] exists, so the left max decides
            lmax = max(lmax, h[l])
            water += lmax - h[l]
            l += 1
        else:
            rmax = max(rmax, h[r])
            water += rmax - h[r]
            r -= 1
    return water

cases = [([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6), ([4, 2, 0, 3, 2, 5], 9),
         ([], 0), ([5], 0), ([3, 3], 0), ([1, 2, 3, 4], 0), ([4, 3, 2, 1], 0),
         ([3, 0, 3], 3), ([2, 0, 2], 2), ([0, 0, 0], 0), ([5, 4, 1, 2], 1)]
for h, want in cases:
    assert brute(h) == prefix_suffix(h) == optimal(h) == want, (h, want)

rng = random.Random(14)
for _ in range(800):
    h = [rng.randint(0, 6) for _ in range(rng.randint(0, 12))]
    assert optimal(h) == brute(h) == prefix_suffix(h), h
print("800 random cases: two-pointer, prefix/suffix and brute force agree")
print(optimal([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), optimal([4, 2, 0, 3, 2, 5]))
big = [(i * 7919) % 1000 for i in range(20000)]
assert optimal(big) == prefix_suffix(big)
print("n = 20000 two-pointer equals prefix/suffix:", optimal(big))

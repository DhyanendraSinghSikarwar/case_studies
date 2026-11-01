import random

def brute(n, updates):
    a = [0] * n
    for l, r, v in updates:
        for i in range(l, r + 1):
            a[i] += v
    return a

def optimal(n, updates):
    d = [0] * (n + 1)                     # length n + 1: r + 1 may equal n
    for l, r, v in updates:
        d[l] += v
        d[r + 1] -= v
    out, run = [], 0
    for i in range(n):
        run += d[i]                       # prefix sum of d = the array
        out.append(run)
    return out

for (n, ups), want in [((5, [[1, 3, 2], [2, 4, 3], [0, 2, -2]]), [-2, 0, 3, 5, 3]),
                       ((1, [[0, 0, 5]]), [5]), ((4, []), [0, 0, 0, 0])]:
    got = optimal(n, ups)
    assert got == want == brute(n, ups)
    print(n, ups, '->', got)

random.seed(4)
for _ in range(500):
    n = random.randint(1, 12)
    ups = []
    for _ in range(random.randint(0, 8)):
        l = random.randint(0, n - 1)
        ups.append([l, random.randint(l, n - 1), random.randint(-9, 9)])
    assert optimal(n, ups) == brute(n, ups)
    shuffled = ups[:]
    random.shuffle(shuffled)
    assert optimal(n, shuffled) == optimal(n, ups)       # order does not matter
print('random cross-check ok: 500 cases, order-independence ok')

# exhaustive: every single update on n = 6 (all l, r, v in -2..2)
n = 6
for l in range(n):
    for r in range(l, n):
        for v in range(-2, 3):
            assert optimal(n, [[l, r, v]]) == brute(n, [[l, r, v]])
print('every single update on n=6 ok (incl. r = n - 1, which writes d[n])')

# a version without the extra slot fails at r = n - 1
try:
    d = [0] * 3
    d[2 + 1] -= 1
except IndexError as e:
    print('d of length n raises:', e)
# max size
import time
n = 10**5
ups = [[l, random.randint(l, n - 1), random.randint(-10**4, 10**4)] for l in (random.randint(0, n - 1) for _ in range(10**5))]
t = time.perf_counter(); res = optimal(n, ups); dt = time.perf_counter() - t
assert len(res) == n
print('max size done (sandbox timing only, not a proof):', 'under 1s' if dt < 1 else 'over 1s')

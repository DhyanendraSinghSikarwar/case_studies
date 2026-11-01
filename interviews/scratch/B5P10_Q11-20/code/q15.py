import random
import itertools
from functools import lru_cache

random.seed(15)
M = 10**9 + 7

def paint_fence(n, k):
    """Optimal: two states per post. O(n) time, O(1) space, modulus after every product/sum."""
    same, diff = 0, k                 # post 1: it cannot be 'same as previous'; k choices, all 'different'
    for _ in range(2, n + 1):
        same, diff = diff, (same + diff) * (k - 1) % M
        # same[i] = diff[i-1]            (copy the colour of post i-1, allowed only if i-1 and i-2 differed)
        # diff[i] = total[i-1] * (k-1)   (pick any colour except the previous post's)
    return (same + diff) % M

def paint_fence_memo(n, k):
    """Top-down, same recurrence. Nests n deep."""
    @lru_cache(maxsize=None)
    def go(i):                        # returns (same, diff) for posts 1..i
        if i == 1:
            return 0, k % M
        same, diff = go(i - 1)
        return diff, (same + diff) * (k - 1) % M
    s, d = go(n)
    return (s + d) % M

def brute(n, k):
    """Oracle: enumerate all k^n colourings and reject three equal in a row."""
    c = 0
    for col in itertools.product(range(k), repeat=n):
        if all(not (col[i] == col[i + 1] == col[i + 2]) for i in range(n - 2)):
            c += 1
    return c % M

for (n, k), want in [((1, 5), 5), ((3, 2), 6), ((7, 2), 42), ((3, 1), 0), ((100000, 10**9), 910929812)]:
    assert paint_fence(n, k) == want, (n, k)
    if n <= 7:
        assert brute(n, k) == want
print('5 prompt examples ok')

# table walk-through on n=1,k=5 and n=3,k=2
def rows(n, k):
    same, diff = 0, k
    out = [(1, same, diff, same + diff)]
    for i in range(2, n + 1):
        same, diff = diff, (same + diff) * (k - 1)
        out.append((i, same, diff, same + diff))
    return out
print('n=3, k=2 (no modulus needed at this size)')
print('post  same  diff  total')
for r in rows(3, 2):
    print('%-5d %-5d %-5d %d' % r)
print('n=1, k=5 -> total', rows(1, 5)[0][3], '(just k)')

# k = 1: 1 for n = 1 or 2, then 0
print('k=1, n=1..5 ->', [paint_fence(n, 1) for n in range(1, 6)])

# exhaustive over n <= 7, k <= 4, all three methods
count = 0
for n in range(1, 8):
    for k in range(1, 5):
        assert paint_fence(n, k) == paint_fence_memo(n, k) == brute(n, k), (n, k)
        count += 1
print('exhaustive n<=7, k<=4:', count, 'cases agree (bottom-up = memo = enumeration)')
for _ in range(200):
    n, k = random.randint(1, 7), random.randint(1, 4)
    assert paint_fence(n, k) == brute(n, k)

# alternative one-state recurrence: total[i] = (k-1) * (total[i-1] + total[i-2])
def alt(n, k):
    t1, t2 = k, k * k
    if n == 1:
        return t1 % M
    for _ in range(3, n + 1):
        t1, t2 = t2, (k - 1) * (t1 + t2) % M
    return t2 % M
assert all(alt(n, k) == paint_fence(n, k) for n in range(1, 40) for k in (1, 2, 3, 10**9))
print('one-state recurrence total[i] = (k-1)*(total[i-1] + total[i-2]) agrees')

# modulus: the exact big-int answer reduced once at the end equals the answer reduced after every step
def exact(n, k):
    same, diff = 0, k
    for _ in range(2, n + 1):
        same, diff = diff, (same + diff) * (k - 1)
    return same + diff
assert exact(2000, 10**9) % M == paint_fence(2000, 10**9)
print('n=2000, k=10^9: exact big int mod M equals the in-loop reduction:', exact(2000, 10**9) % M == paint_fence(2000, 10**9))
print('bits of the exact count at n=2000, k=10^9:', exact(2000, 10**9).bit_length(), '(why we reduce: it grows by about 30 bits per post)')
# the loop has no comparison on reduced values; a reduced number says nothing about order or equality of the true number
print('true value M+5 reduces to', (M + 5) % M, '-> a test like "if count_mod > other_mod" or "if count_mod == 5" would be wrong')

# recursion limit
try:
    paint_fence_memo(10**5, 10**9)
    print('memo at n=10^5: no error (unexpected)')
except RecursionError:
    print('memo at n=10^5: RecursionError under the default limit')
print('bottom-up n=10^5, k=10^9 ->', paint_fence(10**5, 10**9))
assert paint_fence(1, 1) == 1 and paint_fence(2, 1) == 1 and paint_fence(2, 3) == 9
print('edge cases ok')

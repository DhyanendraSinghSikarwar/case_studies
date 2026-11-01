import itertools
import random

random.seed(34)

def candy_brute(r):
    """Try every candy vector with values 1..n (n <= 6 only)."""
    n, best = len(r), None
    for c in itertools.product(range(1, n + 1), repeat=n):
        if all((r[i + 1] <= r[i] or c[i + 1] > c[i]) and (r[i] <= r[i + 1] or c[i] > c[i + 1]) for i in range(n - 1)):
            if best is None or sum(c) < best:
                best = sum(c)
    return best

def candy_two_pass(r):
    n = len(r)
    c = [1] * n
    for i in range(1, n):                      # pass 1: rising constraint
        if r[i] > r[i - 1]:
            c[i] = c[i - 1] + 1
    for i in range(n - 2, -1, -1):             # pass 2: falling constraint, keep the max
        if r[i] > r[i + 1]:
            c[i] = max(c[i], c[i + 1] + 1)
    return sum(c)

def candy_o1(r):
    """O(1) extra space: walk slopes. up = current rising run, down = current falling run, peak = up at the top."""
    n = len(r)
    total = 1
    up = down = peak = 0
    for i in range(1, n):
        if r[i] > r[i - 1]:
            up += 1; peak = up; down = 0
            total += 1 + up
        elif r[i] == r[i - 1]:
            up = down = peak = 0
            total += 1
        else:
            up = 0; down += 1
            # new bottom child gets 1 and every child above it on the slope gets +1 (that is `down`);
            # once the fall is longer than the rise, the peak child needs one more too
            total += down + (0 if down <= peak else 1)
    return total

# ---- examples
assert candy_two_pass([1, 0, 2]) == 5
assert candy_two_pass([1, 2, 2]) == 4          # plateau: the second 2 only needs 1
assert candy_two_pass([3, 2, 1, 2, 3]) == 11   # valley: 3+2+1+2+3
assert candy_two_pass([5]) == 1
for r in ([1, 0, 2], [1, 2, 2], [3, 2, 1, 2, 3], [5]):
    print(r, candy_two_pass(r), candy_o1(r))

# ---- why the max: pass 1 alone breaks the falling side, pass 2 alone breaks the rising side
r = [1, 3, 2, 1]
p1 = [1] * 4
for i in range(1, 4):
    if r[i] > r[i - 1]: p1[i] = p1[i - 1] + 1
print('after pass 1 only', p1, 'falling pair 2>1 satisfied?', p1[2] > p1[3])
# the peak 3 gets max(2, 3) = 3 in pass 2, never less than what pass 1 gave it
print('two-pass total', candy_two_pass(r))

# ---- exhaustive: all rating arrays of length <= 6 over {0,1,2}, plus seeded random of ratings 0..3
checked = 0
for n in range(1, 7):
    for r in itertools.product(range(3), repeat=n):
        r = list(r)
        a = candy_two_pass(r)
        assert a == candy_brute(r) == candy_o1(r), r
        checked += 1
for _ in range(300):
    r = [random.randint(0, 3) for _ in range(random.randint(1, 6))]
    assert candy_two_pass(r) == candy_brute(r) == candy_o1(r), r
    checked += 1
print('cross-checked', checked, 'arrays')

# ---- bigger: O(1) variant agrees with two-pass on large random and structured inputs
for _ in range(200):
    r = [random.randint(0, 20000) for _ in range(random.randint(1, 300))]
    assert candy_two_pass(r) == candy_o1(r)
n = 2 * 10 ** 4
assert candy_two_pass(list(range(n))) == n * (n + 1) // 2        # strictly rising: 1+2+...+n
assert candy_two_pass(list(range(n, 0, -1))) == n * (n + 1) // 2  # strictly falling
assert candy_two_pass([7] * n) == n                                # all equal: one each
assert candy_o1(list(range(n))) == n * (n + 1) // 2 and candy_o1([7] * n) == n
print('max-size edge cases ok, rising total', candy_two_pass(list(range(n))))

import math


def is_square_bs(num):
    lo, hi = 1, min(num, 46341)          # 46341^2 > 2^31 - 1, so the root is <= 46340
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == num:
            return True
        if sq < num:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def is_square_brute(num):
    r = 1
    while r * r < num:
        r += 1
    return r * r == num


def is_square_odd_sum(num):
    """1 + 3 + 5 + ... = k^2: subtract odd numbers until we hit 0 or go negative."""
    odd = 1
    while num > 0:
        num -= odd
        odd += 2
    return num == 0


examples = [(16, True), (14, False), (1, True), (2, False), (2147395600, True), (2147483647, False)]
for num, exp in examples:
    got = is_square_bs(num)
    assert got == exp, (num, got)
    print(num, "->", got)

# exhaustive over every num in 1..200000 against brute force and math.isqrt (checking tool only)
for num in range(1, 200001):
    expected = math.isqrt(num) ** 2 == num
    assert is_square_bs(num) == is_square_brute(num) == is_square_odd_sum(num) == expected, num
print("cross-check: all num in 1..200000 agree (binary search, linear scan, odd-sum, isqrt)")

# boundary of the 32-bit range: every perfect square near the top and its neighbours
for r in range(46330, 46341):
    assert is_square_bs(r * r)
    assert not is_square_bs(r * r - 1)
    if r * r + 1 <= 2**31 - 1:
        assert not is_square_bs(r * r + 1)
assert 46340 ** 2 == 2147395600 and 46341 ** 2 > 2**31 - 1
assert is_square_bs(2**31 - 1) is False
assert is_square_bs(2**30) is True          # 32768^2
print("edge asserts passed")

def kth_table(m, n, k):
    def count_le(v):
        return sum(min(n, v // i) for i in range(1, min(m, v) + 1))   # rows beyond v contribute 0
    lo, hi = 1, m * n
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_table_brute(m, n, k):
    return sorted(i * j for i in range(1, m + 1) for j in range(1, n + 1))[k - 1]


for m, n, k, want in [(3, 3, 5, 3), (2, 3, 6, 6), (1, 5, 4, 4), (3, 3, 9, 9), (3, 3, 1, 1)]:
    got = kth_table(m, n, k)
    print("m =", m, "n =", n, "k =", k, "->", got, " brute:", kth_table_brute(m, n, k))
    assert got == kth_table_brute(m, n, k) == want

# exhaustive: all m, n up to 9 and every k
cnt = 0
for m in range(1, 10):
    for n in range(1, 10):
        table = {i * j for i in range(1, m + 1) for j in range(1, n + 1)}
        for k in range(1, m * n + 1):
            v = kth_table(m, n, k)
            assert v == kth_table_brute(m, n, k), (m, n, k)
            assert v in table                          # the answer is always an entry
            cnt += 1
print("exhaustive (m, n, k) cases checked:", cnt)

# the table is not a sorted list: row-major reading of the 3 x 3 table
print("row-major 3 x 3:", [i * j for i in range(1, 4) for j in range(1, 4)])
# big sizes: no table is built
v = kth_table(3 * 10**4, 3 * 10**4, 3 * 10**4 * 3 * 10**4)
assert v == 9 * 10**8
v = kth_table(3 * 10**4, 3 * 10**4, 4 * 10**8)
print("m = n = 3*10**4, k = 4*10**8 ->", v)
# edge asserts
assert kth_table(1, 1, 1) == 1
assert kth_table(1, 7, 7) == 7 and kth_table(7, 1, 1) == 1
assert kth_table(30000, 1, 30000) == 30000
print("all checks passed")

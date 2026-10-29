import functools
import itertools
import random

random.seed(3901)


def cmp(a, b):
    """a before b (negative) when a + b > b + a as strings."""
    if a + b > b + a:
        return -1
    if a + b < b + a:
        return 1
    return 0


def solve(nums):
    strs = sorted(map(str, nums), key=functools.cmp_to_key(cmp))
    r = "".join(strs)
    return "0" if r[0] == "0" else r          # sorted first = the biggest; a leading '0' means everything is 0


def solve_key(nums):
    """Key-based alternative: repeat each string to >= 20 chars (a + b has at most 20 digits), sort descending."""
    strs = sorted(map(str, nums), key=lambda s: s * (20 // len(s) + 1), reverse=True)
    r = "".join(strs)
    return "0" if r[0] == "0" else r


def brute(nums):
    best = max("".join(map(str, p)) for p in itertools.permutations(nums))
    return "0" if best[0] == "0" else best


# dry run on [3, 30, 34, 5, 9]
print("pairs: '3' vs '30':", "330" if "330" > "303" else "303", "wins ('330' > '303'), so 3 goes first")
print("pairs: '34' vs '3':", "343 vs 334 -> 34 first")
print("plain descending strings:", "".join(sorted(map(str, [3, 30, 34, 5, 9]), reverse=True)),
      "| comparator:", solve([3, 30, 34, 5, 9]))
ss = sorted(map(str, [3, 30, 34, 5, 9]), key=functools.cmp_to_key(cmp))
print("order chosen:", ss, "-> joined", "".join(ss))
print("repeat keys :", [(s, s * (20 // len(s) + 1)) for s in map(str, [3, 30, 34, 5, 9])])

for nums, want in [([3, 30, 34, 5, 9], "9534330"), ([10, 2], "210"), ([0, 0], "0"), ([824, 8247], "8248247"), ([1], "1")]:
    got = solve(nums)
    assert got == solve_key(nums) == brute(nums) == want, (nums, got)
    print(nums, "->", repr(got))

# exact check 1: the key trick agrees with the comparator on EVERY pair of digit strings over {0,1,2,3}, length 1..4 (no leading zero)
strs = ["".join(p) for L in range(1, 5) for p in itertools.product("0123", repeat=L) if p[0] != "0" or L == 1]
key = lambda s: s * (20 // len(s) + 1)
bad = ties_split = 0
for a, b in itertools.product(strs, repeat=2):
    c = cmp(a, b)
    k = (key(a) < key(b)) - (key(a) > key(b))       # descending key: bigger key first = negative
    if c == 0:
        ties_split += (k != 0)                      # a + b == b + a, e.g. '1' and '11': the keys differ in LENGTH only
        assert a + b == b + a
    else:
        bad += (c != k)
print(f"pairs checked: {len(strs) ** 2} over {len(strs)} strings; strict disagreements: {bad}; "
      f"tied pairs (a+b == b+a) that the key still orders: {ties_split} (harmless: tied strings join to the same text)")
assert bad == 0

# exact check 2: transitivity of 'a before-or-equal b'  (a+b >= b+a) on all triples of strings over {0,1,2}, length 1..3
small = ["".join(p) for L in range(1, 4) for p in itertools.product("012", repeat=L)]
ge = lambda a, b: a + b >= b + a
viol = 0
for a, b, c in itertools.product(small, repeat=3):
    if ge(a, b) and ge(b, c) and not ge(a, c):
        viol += 1
print(f"triples checked: {len(small) ** 3}, transitivity violations: {viol}")
assert viol == 0
# total: for every pair one of a+b >= b+a, b+a >= a+b holds, trivially; ties (a+b == b+a) are equal-key strings
assert all(ge(a, b) or ge(b, a) for a, b in itertools.product(small, repeat=2))

# seeded random cross-check against all permutations (n <= 7)
for _ in range(400):
    n = random.randint(1, 7)
    nums = [random.choice([0, 1, 2, 3, 10, 30, 34, 99, 100, 824, 8247, 10 ** 9, random.randint(0, 10 ** 9)]) for _ in range(n)]
    got = solve(nums)
    assert got == brute(nums) == solve_key(nums), nums
print("400 seeded random cases match the permutation brute force and the key version")

# maximum size: 100 numbers up to 10^9
big = [random.randint(0, 10 ** 9) for _ in range(100)]
assert solve(big) == solve_key(big) and len(solve(big)) == sum(len(str(x)) for x in big)
print("n = 100 up to 10^9: comparator and key agree, length", len(solve(big)))

# edge cases
assert solve([0]) == "0" and solve([0, 0, 0]) == "0" and solve([10, 0]) == "100" and solve([0, 1]) == "10"
assert solve([121, 12]) == "12121" and solve([12, 121]) == "12121"          # a + b == b + a: a tie, any order
assert solve([10 ** 9, 10 ** 9 - 1]) == "9999999991000000000"
print("edge asserts ok")

import math, random

def euclid(a, b):
    steps = 0
    while b:
        a, b = b, a % b
        steps += 1
    return a, steps

def optimal(a, b, nums):
    g, steps = euclid(a, b)
    lcm = a // g * b                      # divide first: intermediate stays <= lcm
    ga, la = 0, 1                         # gcd(0, x) = x, lcm identity 1
    for v in nums:
        ga = euclid(ga, v)[0]
        la = la // euclid(la, v)[0] * v
    return [g, lcm, steps, ga, la]

def brute(a, b, nums):                    # library + recursive step counter
    def rsteps(x, y):
        return 0 if y == 0 else 1 + rsteps(y, x % y)
    return [math.gcd(a, b), math.lcm(a, b), rsteps(a, b), math.gcd(*nums), math.lcm(*nums)]

ex = [((48, 18, [4, 6, 10]), [6, 144, 3, 2, 60]),
      ((13, 21, [7]), [1, 273, 7, 7, 7]),
      ((5, 5, [2, 3, 5, 7, 11]), [5, 5, 1, 1, 2310]),
      ((8, 12, [1000000007, 998244353]), [4, 24, 3, 1, 998244359987710471])]
for args, want in ex:
    got = optimal(*args)
    assert got == want == brute(*args)
    print(args, '->', got)

random.seed(2)
for _ in range(500):
    a, b = random.randint(1, 200), random.randint(1, 200)
    nums = [random.randint(1, 200) for _ in range(random.randint(1, 5))]
    assert optimal(a, b, nums) == brute(a, b, nums)
print('random cross-check ok: 500 cases')

# claim: for all 1 <= a, b <= 100 the max step count is 10, reached by (55, 89)
best = max(euclid(a, b)[1] for a in range(1, 101) for b in range(1, 101))
arg = [(a, b) for a in range(1, 101) for b in range(1, 101) if euclid(a, b)[1] == best]
print('max steps for 1..100:', best, 'at', arg)
assert best == 10 and (55, 89) in arg
# (89, 55) takes one step less: smaller-first costs the extra swap
assert euclid(89, 55)[1] == 9 and euclid(55, 89)[1] == 10
# gcd * lcm == a * b exhaustively
assert all(math.gcd(a, b) * math.lcm(a, b) == a * b for a in range(1, 101) for b in range(1, 101))
print('gcd*lcm == a*b for all pairs up to 100; math.gcd(0, 0) =', math.gcd(0, 0))
# edge and size checks
assert optimal(1, 1, [1]) == [1, 1, 1, 1, 1]
big = optimal(10**18, 10**18 - 1, list(range(10**12 - 999, 10**12 + 1)))
print('max-size a,b: gcd', big[0], 'steps', big[2], 'lcm_all bits', big[4].bit_length())
assert big[0] == 1 and big[1] == 10**18 * (10**18 - 1)

import math, random

def factor(b):
    f, d = {}, 2
    while d * d <= b:
        while b % d == 0:
            f[d] = f.get(d, 0) + 1
            b //= d
        d += 1
    if b > 1:
        f[b] = f.get(b, 0) + 1
    return f

def vfact(n, p):                          # exponent of prime p in n! (Legendre)
    c = 0
    while n:
        n //= p
        c += n
    return c

def trailing(n, base):                    # zeros of n! in the given base
    return min(vfact(n, p) // e for p, e in factor(base).items())

def optimal(n, base):
    return [trailing(n, 10), trailing(n, base)]

def brute(n, base):
    f = math.factorial(n)
    def tz(x, b):
        c = 0
        while x % b == 0:
            x //= b
            c += 1
        return c
    return [tz(f, 10), tz(f, base)]

for (n, base), want in [((25, 10), [6, 6]), ((0, 2), [0, 0]), ((100, 12), [24, 48]), ((10, 16), [2, 2])]:
    got = optimal(n, base)
    assert got == want == brute(n, base)
    print(n, base, '->', got)

# exhaustive on small inputs: every n in 0..150 and every base in 2..100
for n in range(151):
    for base in range(2, 101):
        assert optimal(n, base) == brute(n, base)
print('exhaustive check ok: n in 0..150, base in 2..100')

# claim: factors of 2 never run out (n up to 10000)
assert all(vfact(n, 2) >= vfact(n, 5) for n in range(10001))
# claim: z10(n+1) != z10(n) exactly when n+1 is a multiple of 5
assert all((vfact(n + 1, 5) != vfact(n, 5)) == ((n + 1) % 5 == 0) for n in range(5000))
# 10**18: largest k with 5**k <= n, and loop rounds of `while n: n //= 5`
k = 0
while 5 ** (k + 1) <= 10**18:
    k += 1
n, rounds = 10**18, 0
while n:
    n //= 5
    rounds += 1
print('largest k with 5**k <= 10**18:', k, ' loop rounds (while n):', rounds,
      ' z10 =', vfact(10**18, 5))
assert k == 25 and rounds == 26
print('big base 97 :', optimal(10**18, 97), ' base 64:', optimal(10**18, 64))

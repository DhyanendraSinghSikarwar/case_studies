import random, math

def brute(n):                                            # trial division by every d with d*d <= x
    def is_prime(x):
        return x >= 2 and all(x % d for d in range(2, math.isqrt(x) + 1))
    count = sum(1 for x in range(n) if is_prime(x))
    marks = sum(len(range(p * p, n, p)) for p in range(2, n) if p * p < n and is_prime(p))
    return [count, marks]

def optimal(n):
    if n < 3:
        return [0, 0]
    flags = bytearray([1]) * n
    flags[0] = flags[1] = 0
    marks, p = 0, 2
    while p * p < n:
        if flags[p]:
            cnt = len(range(p * p, n, p))               # multiples p*p, p*p+p, ... below n
            marks += cnt
            flags[p * p::p] = bytes(cnt)                # slice assignment = C-speed marking
        p += 1
    return [sum(flags), marks]

def sieve_loop(n, start_sq=True):                       # plain loops, to compare start points
    flags = bytearray([1]) * n
    flags[:2] = b'\x00\x00'[:min(2, n)]
    marks, p = 0, 2
    while p * p < n:
        if flags[p]:
            for x in range(p * p if start_sq else 2 * p, n, p):
                flags[x] = 0
                marks += 1
        p += 1
    return sum(flags), marks

for n, want in [(10, [4, 4]), (2, [0, 0]), (30, [10, 21]), (100, [25, 102]), (0, [0, 0])]:
    got = optimal(n)
    assert got == want == brute(n)
    print('n =', n, '->', got)

# exhaustive over every n in 0..500 (not just seeded samples) plus a seeded random batch
for n in range(501):
    assert optimal(n) == brute(n)
random.seed(8)
for _ in range(300):
    n = random.randint(0, 3000)
    assert optimal(n) == brute(n)
print('cross-check ok: every n in 0..500 and 300 seeded n up to 3000')

# claims: starting at 2p instead of p*p gives the same primes but more marks; p*p < n bound enough
for n in range(3, 500):
    c1, k1 = sieve_loop(n, True)
    c2, k2 = sieve_loop(n, False)
    assert c1 == c2 == optimal(n)[0] and k1 == optimal(n)[1] and k2 >= k1
print('start at p*p vs 2p: same count; marks for n=499:', sieve_loop(499, True)[1], 'vs', sieve_loop(499, False)[1])
# known prime counts
assert [optimal(n)[0] for n in (10, 100, 1000, 10**6)] == [4, 25, 168, 78498]
# max size
res = optimal(5 * 10**6)
print('n = 5*10**6 ->', res)
assert res[0] == 348513
# memory: one byte per flag
print('flags bytes for n = 5*10**6:', len(bytearray(5 * 10**6)))

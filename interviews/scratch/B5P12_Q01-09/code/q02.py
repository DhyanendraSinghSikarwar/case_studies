import random

random.seed(1202)

def naive_loop(n):
    m, it = n, 0
    while m:
        m >>= 1
        it += 1
    return it

def kernighan_loop(n):
    m, it = n, 0
    while m:
        m &= m - 1       # clears the lowest set bit
        it += 1
    return it

def solve(n):
    k = kernighan_loop(n)
    return [k, naive_loop(n), k]    # popcount == kernighan iterations

def brute(n):
    s = bin(n)[2:]
    return [s.count('1'), len(s) if n else 0, s.count('1')]

examples = [(11, [3, 4, 3]), (0, [0, 0, 0]), (2147483648, [1, 32, 1]), (4294967295, [32, 32, 32]), (1, [1, 1, 1])]
for n, want in examples:
    assert solve(n) == want == brute(n)
    print(n, '->', solve(n))

# dry run of n = 11 = 0b1011
m = 11
while m:
    print(f'  m={m:04b}  m-1={m-1:04b}  m&(m-1)={m & (m-1):04b}')
    m &= m - 1

# seeded cross-check against bin().count and bit_length (and int.bit_count, present on this Python 3.13)
for _ in range(5000):
    n = random.choice([random.randrange(2**32), random.randrange(40), 2**random.randrange(32), 2**random.randrange(1, 33) - 1])
    r = solve(n)
    assert r == brute(n)
    assert r[0] == bin(n).count('1') == n.bit_count()
    assert r[1] == n.bit_length()
print('random cross-check ok: 5000 cases')
# exhaustive on 0..2**16
for n in range(2**16):
    assert solve(n) == brute(n) and n.bit_length() == solve(n)[1] and n.bit_count() == solve(n)[0]
print('exhaustive 0..65535 ok')

# why the 0 <= n < 2**32 bound matters: both loops never end for negative n in Python.
# Bounded demonstration (stop after 100 rounds):
def rounds_capped(n, step, cap=100):
    m, it = n, 0
    while m and it < cap:
        m = step(m); it += 1
    return it, m
print('naive on -1, capped at 100:', rounds_capped(-1, lambda m: m >> 1))
print('kernighan on -1, capped at 100:', rounds_capped(-1, lambda m: m & (m - 1)))
print('masked version of -1 :', kernighan_loop(-1 & 0xFFFFFFFF))
print('edge asserts ok')

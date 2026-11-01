import random

random.seed(1318)

def f(v):
    s = 0
    while v:
        v, d = divmod(v, 10)
        s += d * d
    return s

def happy(n):
    """Floyd: tortoise moves 1 step, hare 2; O(1) space. Then measure the cycle length from the meeting point."""
    slow, fast = n, f(n)
    while fast != 1 and slow != fast:
        slow, fast = f(slow), f(f(fast))
    x, c = fast, 1                          # fast is inside the cycle (or is 1)
    y = f(x)
    while y != x:
        y, c = f(y), c + 1
    steps = -1
    if fast == 1 or n == 1:
        steps, v = 0, n
        while v != 1:
            v, steps = f(v), steps + 1
    return [steps >= 0, steps, c]

def brute(n):
    """Dictionary of seen value -> position."""
    seen, v, i = {}, n, 0
    while v not in seen:
        seen[v] = i; i += 1
        v = f(v)
    return [1 in seen, seen.get(1, -1), i - seen[v]]

examples = [(19, [True, 4, 1]), (2, [False, -1, 8]), (1, [True, 0, 1]), (7, [True, 5, 1]), (4, [False, -1, 8])]
for n, exp in examples:
    got = happy(n)
    print(n, '->', got)
    assert got == exp and brute(n) == exp
print('trace of 19:', [19, f(19), f(f(19)), f(f(f(19))), f(f(f(f(19))))])

# exhaustive: every n < 200000 is happy or ends in the 8-cycle; list the cycle
for n in range(1, 200000):
    h, st, cl = happy(n)
    assert (cl == 1) if h else (cl == 8)
    assert [h, st, cl] == brute(n)
cyc, v = [], 4
while True:
    cyc.append(v); v = f(v)
    if v == 4: break
print('unhappy cycle:', cyc, '| checked every n < 200000: happy => cycle 1, unhappy => cycle of 8')

# why the sequence cannot grow: f(n) < n for n >= 1000 (checked), and the 10-digit bound
assert all(f(n) < n for n in range(1000, 300000))
assert all(81 * k < 10 ** (k - 1) for k in range(4, 40))
print('81*d < 10^(d-1) for every d >= 4; 10-digit bound 10*81 = 810; f(2^31-1) =', f(2 ** 31 - 1),
      ', f(1999999999) =', f(1999999999))
assert f(2 ** 31 - 1) <= 810 and max(f(n) for n in range(10 ** 9, 10 ** 9 + 1000)) <= 810

# longest run before a value repeats, over every n < 100000
def run_len(n):
    seen, v = set(), n
    while v not in seen:
        seen.add(v); v = f(v)
    return len(seen)
print('longest run before a repeat for n < 100000:', max(run_len(n) for n in range(1, 100000)), 'values')

# seeded random cross-check on large values too
for _ in range(500):
    n = random.choice([random.randint(1, 3000), random.randint(1, 2 ** 31 - 1)])
    assert happy(n) == brute(n)
print('random cross-check ok: 500 cases')

# edge asserts
assert happy(2 ** 31 - 1)[0] in (True, False)
assert happy(10) == [True, 1, 1] and happy(100) == [True, 1, 1] and happy(1) == [True, 0, 1]
print('edge asserts ok; 2^31-1 ->', happy(2 ** 31 - 1))

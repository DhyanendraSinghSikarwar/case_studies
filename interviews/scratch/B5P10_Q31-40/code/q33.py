import functools
import random
import sys

random.seed(33)
MOD = 10**9 + 7
assert sys.getrecursionlimit() == 1000          # the default; the claims below are about this limit

def bottom_up(n):
    """f(0)=1, f(k)=f(k-1)+f(k-2)+f(k-3), f(negative)=0, three rolling variables, no recursion."""
    if n == 0:
        return 1
    a, b, c = 0, 0, 1                           # f(-2), f(-1), f(0)
    for _ in range(n):
        a, b, c = b, c, (a + b + c) % MOD
    return c

@functools.cache
def top_down(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    return (top_down(n - 1) + top_down(n - 2) + top_down(n - 3)) % MOD

def memo_outcome(n):
    """The oracle: run the memoised recursion in try/except. Returns (outcome, value or None)."""
    top_down.cache_clear()
    try:
        return 'ok', top_down(n)
    except RecursionError:
        return 'RecursionError', None

def solve(n):
    # 'ways' from the loop; 'memo_outcome' is reported by running top_down in this interpreter
    return [bottom_up(n), memo_outcome(n)[0]]

# ---- examples from the prompt
assert solve(0) == [1, 'ok']
assert solve(10) == [274, 'ok']
assert solve(500) == [283701821, 'ok']
assert solve(2000) == [78591238, 'RecursionError']
assert solve(100000) == [111787461, 'RecursionError']
print('examples ok')

# ---- where exactly does the default limit bite? (the depth is about n, one frame per level)
top = 0
for n in range(1, 1000):
    if memo_outcome(n)[0] == 'ok':
        top = n
    else:
        break
print('largest n that works at limit 1000 (this interpreter, called from module level):', top)

# ---- every n in 0..500 is fine, so the prompt's 'ok' range is correct
assert all(memo_outcome(n)[0] == 'ok' for n in range(0, 501))
print('n = 0..500 all ok')

# ---- seeded cross-check: bottom-up value against the memoised oracle, outcome as well
cases = 0
for _ in range(300):
    n = random.randint(0, 500)
    out, val = memo_outcome(n)
    assert out == 'ok' and val == bottom_up(n)
    cases += 1
for n in (1000, 1500, 2000, 5000, 10**5):
    out, val = memo_outcome(n)
    assert out == 'RecursionError' and val is None and solve(n)[1] == out
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- raising the limit: a stopgap, not a plan
old = sys.getrecursionlimit()
sys.setrecursionlimit(10**6)
for n in (2000, 3000, 5000):
    out, val = memo_outcome(n)
    print('limit raised, n =', n, '->', out, '| bottom-up agrees:', val is None or val == bottom_up(n))
sys.setrecursionlimit(old)
print('limit restored to', sys.getrecursionlimit())

# ---- bottom-up at the full size, and the space-optimised form is O(1)
print('bottom-up n = 10**5:', bottom_up(10**5))
assert bottom_up(1) == 1 and bottom_up(2) == 2 and bottom_up(3) == 4

import itertools
import random
from functools import lru_cache

random.seed(19)

def assign_cookies(g, s):
    g = sorted(g)
    s = sorted(s)
    i = 0                                    # next unmatched child (least greedy)
    for cookie in s:                         # smallest cookie first
        if i < len(g) and g[i] <= cookie:    # smallest cookie that satisfies the least greedy child
            i += 1
    return i

def brute(g, s):                             # try every cookie for every child, bitmask of used cookies
    @lru_cache(None)
    def f(i, used):
        if i == len(g):
            return 0
        best = f(i + 1, used)                # leave child i unhappy
        for j in range(len(s)):
            if not used >> j & 1 and s[j] >= g[i]:
                best = max(best, 1 + f(i + 1, used | 1 << j))
        return best
    return f(0, 0)

for g, s, exp in [([1, 2, 3], [1, 1], 1), ([1, 2], [1, 2, 3], 2), ([], [4], 0), ([5, 6], [1, 2], 0)]:
    assert assign_cookies(g, s) == brute(tuple(g), tuple(s)) == exp
    print('g =', g, 's =', s, '->', assign_cookies(g, s))

# exhaustive: lists of length 0..4 over sizes 1..4 (sizes form a tiny alphabet)
cnt = 0
for lg in range(0, 5):
    for ls in range(0, 5):
        for g in itertools.product(range(1, 5), repeat=lg):
            for s in itertools.product(range(1, 5), repeat=ls):
                assert assign_cookies(list(g), list(s)) == brute(g, s), (g, s)
                cnt += 1
print('exhaustive ok:', cnt, 'pairs')

for _ in range(1000):
    g = [random.randint(1, 8) for _ in range(random.randint(0, 7))]
    s = [random.randint(1, 8) for _ in range(random.randint(0, 7))]
    assert assign_cookies(g, s) == brute(tuple(g), tuple(s))
print('random ok: 1000 pairs')

# a wasteful rule (biggest cookie to the least greedy child) is wrong:
def wrong_biggest_cookie_to_first_child(g, s):      # gives each child (sorted ascending) the BIGGEST cookie left
    g = sorted(g)
    s = sorted(s)
    done = 0
    for c in g:
        if s and s[-1] >= c:
            s.pop()
            done += 1
    return done
bad = []
for g in itertools.product(range(1, 4), repeat=2):
    for s in itertools.product(range(1, 4), repeat=2):
        if wrong_biggest_cookie_to_first_child(list(g), list(s)) != assign_cookies(list(g), list(s)):
            bad.append((g, s))
print('wasteful rule differs from greedy on', len(bad), 'tiny cases, e.g.', bad[0] if bad else None)
assert wrong_biggest_cookie_to_first_child([1, 3], [1, 3]) == 1 and assign_cookies([1, 3], [1, 3]) == 2

# edge cases and max size
assert assign_cookies([], []) == 0
assert assign_cookies([1], []) == 0
assert assign_cookies([2 ** 31 - 1], [2 ** 31 - 1]) == 1
assert assign_cookies([1] * 30000, [1] * 30000) == 30000
assert assign_cookies([1] * 30000, [1] * 29999) == 29999
assert assign_cookies([2, 2, 2], [1, 1, 1]) == 0
print('edge cases ok')

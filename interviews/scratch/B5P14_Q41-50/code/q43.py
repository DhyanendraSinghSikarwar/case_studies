import random, sys
from functools import lru_cache
random.seed(43)

def kuhn(L, R, edges):
    g = [[] for _ in range(L)]
    for u, v in edges:
        g[u].append(v)
    match_r = [-1] * R                        # match_r[v] = left partner of right node v

    def try_augment(u, seen):                 # recursion depth <= L <= 300
        for v in g[u]:
            if v in seen:
                continue
            seen.add(v)
            if match_r[v] == -1 or try_augment(match_r[v], seen):
                match_r[v] = u                # flip the augmenting path
                return True
        return False

    size = sum(1 for u in range(L) if try_augment(u, set()))
    return [size, size == L]

def oracle(L, R, edges):                      # exhaustive: memoised DP over bitmasks of used right nodes
    g = [set() for _ in range(L)]
    for u, v in edges:
        g[u].add(v)
    @lru_cache(None)
    def f(i, mask):
        if i == L:
            return 0
        best = f(i + 1, mask)                 # leave left node i unmatched
        for v in g[i]:
            if not mask >> v & 1:
                best = max(best, 1 + f(i + 1, mask | 1 << v))
        return best
    s = f(0, 0)
    return [s, s == L]

assert kuhn(3, 3, [[0, 0], [0, 1], [1, 0], [2, 0]]) == [2, False]
assert kuhn(2, 2, [[0, 0], [0, 1], [1, 0]]) == [2, True]
print('examples ok')

for _ in range(500):
    L, R = random.randint(1, 6), random.randint(1, 6)
    edges = [[random.randrange(L), random.randrange(R)] for _ in range(random.randint(0, 14))]
    assert kuhn(L, R, edges) == oracle(L, R, edges), (L, R, edges)
print('500 random small graphs match the bitmask oracle')

assert kuhn(1, 1, []) == [0, False]
assert kuhn(2, 2, [[0, 0], [0, 0], [1, 0]]) == [1, False]   # repeats, one right node
assert kuhn(3, 1, [[0, 0], [1, 0], [2, 0]]) == [1, False]
# greedy without re-matching is not enough: left 0 grabs right 0, then left 1 is stuck
def greedy(L, R, edges):
    used = set(); n = 0; g = [[] for _ in range(L)]
    for u, v in edges: g[u].append(v)
    for u in range(L):
        for v in g[u]:
            if v not in used: used.add(v); n += 1; break
    return n
E = [[0, 0], [0, 1], [1, 0]]
print('greedy gives', greedy(2, 2, E), 'Kuhn gives', kuhn(2, 2, E)[0])
assert greedy(2, 2, E) == 1 and kuhn(2, 2, E)[0] == 2
# max size: L = R = 300 where left i prefers right i-1 (already owned), forcing a ~300-deep augmenting path
L = 300
deep = [[0, 0]] + [[i, v] for i in range(1, L) for v in (i - 1, i)]
cur = [0, 0]                                  # current and max depth of try_augment, measured from outside
def prof(frame, event, arg):
    if frame.f_code.co_name == 'try_augment':
        if event == 'call':
            cur[0] += 1; cur[1] = max(cur[1], cur[0])
        elif event == 'return':
            cur[0] -= 1
sys.setprofile(prof); res = kuhn(L, L, deep); sys.setprofile(None)
print('300 x 300 deep case:', res, 'max recursion depth', cur[1])
assert res == [300, True] and cur[1] <= 300 < sys.getrecursionlimit()
print('first example:', kuhn(3, 3, [[0, 0], [0, 1], [1, 0], [2, 0]]))

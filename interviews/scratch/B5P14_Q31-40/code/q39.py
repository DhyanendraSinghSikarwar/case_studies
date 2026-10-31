import random
from collections import deque

random.seed(3901)


def min_time(n, relations, time):
    """Kahn's algorithm; start[v] = max finish of prerequisites; finish = start + time. Returns [total, finish]."""
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in relations:
        g[a].append(b)
        indeg[b] += 1
    start = [0] * (n + 1)
    finish = [0] * (n + 1)
    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    done = 0
    while q:
        u = q.popleft()
        done += 1
        finish[u] = start[u] + time[u - 1]
        for v in g[u]:
            start[v] = max(start[v], finish[u])      # wait for the slowest prerequisite
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if done < n:                                     # a cycle leaves some courses with indegree > 0
        return [-1, []]
    return [max(finish[1:]), finish[1:]]


def brute(n, relations, time):
    """Memoised recursion over prerequisites with its own cycle detection (small n only)."""
    pre = {v: [] for v in range(1, n + 1)}
    for a, b in relations:
        pre[b].append(a)
    memo, state = {}, {}

    def fin(v):
        if state.get(v) == 1:
            raise ValueError('cycle')
        if v in memo:
            return memo[v]
        state[v] = 1
        memo[v] = max((fin(p) for p in pre[v]), default=0) + time[v - 1]
        state[v] = 2
        return memo[v]
    try:
        f = [fin(v) for v in range(1, n + 1)]
    except ValueError:
        return [-1, []]
    return [max(f), f]


def random_case(cyclic):
    n = random.randint(1, 7)
    order = list(range(1, n + 1))
    random.shuffle(order)
    rel = [[order[i], order[j]] for i in range(n) for j in range(i + 1, n) if random.random() < 0.35]
    if cyclic and n >= 2 and rel:
        a, b = random.choice(rel)
        rel.append([b, a])
    random.shuffle(rel)
    return n, rel, [random.randint(1, 9) for _ in range(n)]


# --- the prompt's examples ---
ex = [((3, [[1, 3], [2, 3]], [3, 2, 5]), [8, [3, 2, 8]]),
      ((2, [[1, 2], [2, 1]], [1, 1]), [-1, []]),
      ((4, [], [4, 9, 1, 2]), [9, [4, 9, 1, 2]])]
for args, want in ex:
    got = min_time(*args)
    print(args, '->', got)
    assert got == want == brute(*args)

# --- random cross-check (DAGs by construction, plus injected cycles) ---
cyc = 0
for i in range(2000):
    args = random_case(cyclic=(i % 3 == 0))
    got = min_time(*args)
    assert got == brute(*args), args
    cyc += got[0] == -1
print('random cases passed: 2000 (', cyc, 'with a cycle )')

# --- edge cases ---
assert min_time(1, [], [5]) == [5, [5]]                              # one course
assert min_time(3, [[1, 2], [2, 3]], [1, 1, 1]) == [3, [1, 2, 3]]    # chain: times add
assert min_time(3, [[1, 2], [1, 3], [2, 3], [1, 3]], [2, 3, 1]) == [6, [2, 5, 6]]   # duplicate relation is harmless
assert min_time(3, [[1, 2], [2, 3], [3, 1]], [1, 1, 1]) == [-1, []]  # 3-cycle
assert min_time(4, [[1, 2], [2, 1]], [1, 1, 1, 1]) == [-1, []]       # a cycle anywhere poisons the answer
n = 5 * 10 ** 4
chain = [[i, i + 1] for i in range(1, n)]
assert min_time(n, chain, [10 ** 4] * n)[0] == n * 10 ** 4          # n = 5*10^4, longest path, no recursion needed
print('edge asserts passed')

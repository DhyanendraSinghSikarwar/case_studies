import heapq
import random

random.seed(44)

def ipo_brute(k, w, profits, capital):
    """Exhaustive search over every order of at most k distinct projects (tiny inputs only)."""
    best = w
    def go(w, used, left):
        nonlocal best
        best = max(best, w)
        if left == 0:
            return
        for i in range(len(profits)):
            if not used >> i & 1 and capital[i] <= w:
                go(w + profits[i], used | 1 << i, left - 1)
    go(w, 0, k)
    return best

def ipo_greedy(k, w, profits, capital):
    projects = sorted(zip(capital, profits))             # by required capital; ties compare profit, which is fine (ints)
    heap = []                                            # max-heap of profits of affordable projects (negated)
    i = 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(heap, -projects[i][1])        # unlock everything now affordable
            i += 1
        if not heap:
            break                                        # nothing affordable and capital cannot grow: stop early
        w -= heapq.heappop(heap)                         # take the biggest profit (w - (-p) = w + p)
    return w

def ipo_wrong_cheapest(k, w, profits, capital):
    """Counter-example rule: always take the lowest-capital affordable project (not the most profitable)."""
    ps = sorted(zip(capital, profits)); used = [False] * len(ps)
    for _ in range(k):
        pick = next((j for j in range(len(ps)) if not used[j] and ps[j][0] <= w), None)
        if pick is None: break
        used[pick] = True; w += ps[pick][1]
    return w

# ---- examples
for k, w, pr, cp, want in [(2, 0, [1, 2, 3], [0, 1, 1], 4), (3, 0, [1, 2, 3], [0, 1, 2], 6), (1, 0, [5], [1], 0), (0, 4, [9], [0], 4)]:
    got = ipo_greedy(k, w, pr, cp)
    assert got == ipo_brute(k, w, pr, cp) == want, (k, w, pr, cp, got)
    print('k =', k, 'w =', w, pr, cp, '->', got)

# ---- heap tie behaviour: only ints are pushed (negated profits), so equal profits tie harmlessly. A (profit, project) tuple with
# a non-comparable payload is where it would break.
class P:
    def __init__(self, n): self.n = n
h = []
heapq.heappush(h, (-3, P('a')))
try:
    heapq.heappush(h, (-3, P('b')))
except TypeError as e:
    print('heap of (-profit, project object) on equal profits ->', e)
h = [-3, -3, -5]
heapq.heapify(h)
print('heap of plain negated ints, equal profits are harmless:', [-heapq.heappop(h) for _ in range(3)])

# ---- random cross-check against the exhaustive search (n <= 6)
beaten = None
for _ in range(2500):
    n = random.randint(1, 6)
    pr = [random.randint(0, 6) for _ in range(n)]
    cp = [random.randint(0, 8) for _ in range(n)]
    k, w = random.randint(0, 5), random.randint(0, 4)
    g = ipo_greedy(k, w, pr, cp)
    assert g == ipo_brute(k, w, pr, cp), (k, w, pr, cp)
    if beaten is None and ipo_wrong_cheapest(k, w, pr, cp) < g:
        beaten = (k, w, pr, cp)
print('2500 random cases agree with exhaustive search')
print('cheapest-capital-first is not optimal, e.g. (k, w, profits, capital) =', beaten,
      'wrong =', ipo_wrong_cheapest(*beaten), 'right =', ipo_greedy(*beaten))

# ---- edge asserts and size
assert ipo_greedy(3, 0, [4, 4], [1, 2]) == 0                     # nothing affordable: heap empty, stop
assert ipo_greedy(10, 0, [0, 0], [0, 0]) == 0                    # zero profits, k larger than the project count
assert ipo_greedy(1, 10 ** 9, [10 ** 4], [10 ** 9]) == 10 ** 9 + 10 ** 4
n = 10 ** 5
pr = [random.randint(0, 10 ** 4) for _ in range(n)]
cp = [random.randint(0, 10 ** 9) for _ in range(n)]
r = ipo_greedy(n, 0, pr, cp)
assert r >= 0
r2 = ipo_greedy(n, 10 ** 9, pr, cp)
assert r2 == 10 ** 9 + sum(pr)                                    # capital covers everything: take every project
print('n=10^5 ok; with w = 10^9 every project is affordable, final capital', r2)

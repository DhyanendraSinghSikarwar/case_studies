import heapq, random
from bisect import insort, bisect_left

class Leaderboard:
    def __init__(self):
        self.totals = {}

    def addScore(self, player, score):      # O(1)
        self.totals[player] = self.totals.get(player, 0) + score

    def top(self, K):                       # O(P log K): heapq.nlargest keeps a heap of size K
        return sum(heapq.nlargest(K, self.totals.values()))

    def reset(self, player):                # O(1); unknown player is a no-op
        self.totals.pop(player, None)

class LeaderboardSorted:
    """For top-heavy workloads: keep a sorted list of (total, player). addScore/reset O(P) (list insert), top O(K)."""
    def __init__(self):
        self.totals = {}; self.order = []
    def addScore(self, player, score):
        old = self.totals.get(player)
        if old is not None:
            del self.order[bisect_left(self.order, (old, player))]
        new = (old or 0) + score
        self.totals[player] = new
        insort(self.order, (new, player))
    def top(self, K):
        return sum(t for t, _ in self.order[max(0, len(self.order) - K):]) if K > 0 else 0
    def reset(self, player):
        old = self.totals.pop(player, None)
        if old is not None:
            del self.order[bisect_left(self.order, (old, player))]

class Naive:
    def __init__(self): self.log = []                      # every (player, score) ever added, plus resets
    def addScore(self, player, score): self.log.append(('add', player, score))
    def reset(self, player): self.log.append(('reset', player, 0))
    def top(self, K):
        tot = {}
        for kind, p, s in self.log:
            if kind == 'add': tot[p] = tot.get(p, 0) + s
            else: tot.pop(p, None)
        return sum(sorted(tot.values(), reverse=True)[:K])

def run(cls, ops):
    obj = cls()
    return [getattr(obj, m)(*a) for m, a in ops]

ex = [['addScore', [1, 73]], ['addScore', [2, 56]], ['addScore', [3, 39]], ['addScore', [4, 51]], ['addScore', [5, 4]],
      ['top', [1]], ['reset', [1]], ['reset', [9]], ['addScore', [2, 51]], ['top', [3]], ['top', [10]]]
want = [None, None, None, None, None, 73, None, None, None, 197, 201]
for cls in (Leaderboard, LeaderboardSorted, Naive):
    assert run(cls, ex) == want, cls
print('example:', run(Leaderboard, ex))

# edge cases: empty board, K larger than players, reset then re-add starts from zero
lb = Leaderboard()
assert lb.top(5) == 0
lb.addScore(7, 10); lb.reset(7); lb.addScore(7, 3)
assert lb.top(1) == 3
lb.addScore(8, 3)
assert lb.top(2) == 6 and lb.top(100) == 6                 # ties do not matter: only the sum is returned

random.seed(27)
n_ops = 0
for _ in range(500):
    ops = []
    for _ in range(random.randint(1, 50)):
        r = random.random()
        p = random.randint(1, 6)
        if r < 0.5: ops.append(['addScore', [p, random.randint(1, 20)]])
        elif r < 0.65: ops.append(['reset', [p]])
        else: ops.append(['top', [random.randint(1, 8)]])
    a = run(Leaderboard, ops)
    assert a == run(Naive, ops) == run(LeaderboardSorted, ops), ops
    n_ops += len(ops)
print('operation-sequence oracle ok: 500 sequences,', n_ops, 'operations, 3 implementations agree')

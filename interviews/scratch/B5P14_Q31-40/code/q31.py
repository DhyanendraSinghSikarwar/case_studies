import random
from bisect import bisect_right
from collections import Counter, defaultdict

random.seed(3101)


class TopVotedCandidate:
    """Leader after each vote is precomputed; ties go to the person who voted most recently."""

    def __init__(self, persons, times):
        self.times = list(times)
        self.lead = []                      # lead[i] = leader right after vote i
        cnt = Counter()
        leader = None
        for p in persons:
            cnt[p] += 1
            if leader is None or cnt[p] >= cnt[leader]:   # >= : a tie goes to the newest voter
                leader = p
            self.lead.append(leader)

    def q(self, t):                         # O(log n)
        return self.lead[bisect_right(self.times, t) - 1]


class TopVotedSmallestId(TopVotedCandidate):
    """Variant: ties go to the smallest id. Needs the extra id comparison."""

    def __init__(self, persons, times):
        self.times = list(times)
        self.lead = []
        cnt = Counter()
        leader = None
        for p in persons:
            cnt[p] += 1
            if leader is None or cnt[p] > cnt[leader] or (cnt[p] == cnt[leader] and p < leader):
                leader = p
            self.lead.append(leader)


class Naive:
    """Rescan every vote with time <= t; tie -> the person whose last vote is latest."""

    def __init__(self, persons, times):
        self.p, self.t = list(persons), list(times)

    def q(self, t):
        cnt, last = defaultdict(int), {}
        for i, (p, tt) in enumerate(zip(self.p, self.t)):
            if tt > t:
                break
            cnt[p] += 1
            last[p] = i
        top = max(cnt.values())
        return max((last[p], p) for p in cnt if cnt[p] == top)[1]


class NaiveSmallestId:
    def __init__(self, persons, times):
        self.p, self.t = list(persons), list(times)

    def q(self, t):
        cnt = Counter(p for p, tt in zip(self.p, self.t) if tt <= t)
        top = max(cnt.values())
        return min(p for p in cnt if cnt[p] == top)


def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]


# --- the prompt's example, run through the same op format ---
init = [[0, 1, 1, 0, 0, 1, 0], [0, 5, 10, 15, 20, 25, 30]]
ops = [['q', [3]], ['q', [12]], ['q', [25]], ['q', [15]], ['q', [24]], ['q', [8]]]
got = run(TopVotedCandidate, init, ops)
print('example:', got)
assert got == [0, 1, 1, 0, 0, 1] == run(Naive, init, ops)
print('leader after each vote:', TopVotedCandidate(*init).lead)

# --- random operation-sequence oracle (both tie rules) ---
checked = 0
for _ in range(600):
    n = random.randint(1, 12)
    persons = [random.randint(0, 3) for _ in range(n)]
    times = sorted(random.sample(range(0, 40), n))
    ops = [['q', [random.randint(times[0], 45)]] for _ in range(15)]
    ops += [['q', [t]] for t in times] + [['q', [t - 1]] for t in times if t - 1 >= times[0]]   # boundaries
    assert run(TopVotedCandidate, [persons, times], ops) == run(Naive, [persons, times], ops)
    assert run(TopVotedSmallestId, [persons, times], ops) == run(NaiveSmallestId, [persons, times], ops)
    checked += len(ops)
print('random queries compared (both tie rules):', checked)

# --- the two tie rules really differ ---
persons, times = [0, 1], [1, 2]            # after time 2: 0 and 1 tied 1-1
print('tie 0 vs 1 at t=2: newest-voter ->', TopVotedCandidate(persons, times).q(2),
      '| smallest-id ->', TopVotedSmallestId(persons, times).q(2))

# --- edge cases ---
assert TopVotedCandidate([7], [3]).q(3) == 7 and TopVotedCandidate([7], [3]).q(10 ** 9) == 7   # single vote
assert TopVotedCandidate([0, 1], [1, 2]).q(1) == 0       # t exactly on a vote counts that vote
assert TopVotedCandidate([0, 1], [1, 2]).q(2) == 1       # tie 1-1 at t=2: newest voter
assert TopVotedCandidate([0, 0, 1], [1, 2, 3]).q(3) == 0  # 2-1, no tie
big = TopVotedCandidate([i % 5 for i in range(5000)], list(range(1, 5001)))
assert big.q(5000) == 4 and big.q(1) == 0                  # n = 5000: ties go to the newest voter
print('edge asserts passed')

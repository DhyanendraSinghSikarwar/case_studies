import random
from collections import deque

random.seed(30)

def neighbours(s):
    """The implicit graph: 8 neighbours computed on demand (4 wheels x up/down, with wrap-around)."""
    for i in range(4):
        d = int(s[i])
        for step in (1, 9):                               # +1 and -1 mod 10
            yield s[:i] + str((d + step) % 10) + s[i + 1:]

def open_lock(deadends, target):
    dead = set(deadends)
    if '0000' in dead:
        return -1
    seen = {'0000'}
    q = deque([('0000', 0)])
    while q:
        s, d = q.popleft()
        if s == target:
            return d
        for t in neighbours(s):
            if t not in dead and t not in seen:           # mark on PUSH so no state is queued twice
                seen.add(t)
                q.append((t, d + 1))
    return -1

def open_lock_levels(deadends, target):
    """Independent brute force: expand one whole level at a time with sets (no queue, no per-node distance)."""
    dead = set(deadends)
    if '0000' in dead:
        return -1
    level, seen, d = {'0000'}, {'0000'}, 0
    while level:
        if target in level:
            return d
        nxt = set()
        for s in level:
            for t in neighbours(s):
                if t not in dead and t not in seen:
                    nxt.add(t)
        seen |= nxt
        level, d = nxt, d + 1
    return -1

def open_lock_bidirectional(deadends, target):
    """Follow-up: grow the smaller frontier from each end; meet in the middle."""
    dead = set(deadends)
    if '0000' in dead or target in dead:
        return -1
    if target == '0000':
        return 0
    a, b, seen_a, seen_b, d = {'0000'}, {target}, {'0000'}, {target}, 0
    while a and b:
        if len(a) > len(b):
            a, b, seen_a, seen_b = b, a, seen_b, seen_a
        nxt = set()
        d += 1
        for s in a:
            for t in neighbours(s):
                if t in seen_b:
                    return d
                if t not in dead and t not in seen_a:
                    seen_a.add(t)
                    nxt.add(t)
        a = nxt
    return -1

def open_lock_no_start_check(deadends, target):
    """Bug: forget that '0000' itself may be jammed."""
    dead = set(deadends)
    seen = {'0000'}
    q = deque([('0000', 0)])
    while q:
        s, d = q.popleft()
        if s == target:
            return d
        for t in neighbours(s):
            if t not in dead and t not in seen:
                seen.add(t)
                q.append((t, d + 1))
    return -1

for de, tg, want in [(['0201', '0101', '0102', '1212', '2002'], '0202', 6), (['8888'], '0009', 1),
                     (['0000'], '8888', -1), (['8887', '8889', '8878', '8898', '8788', '8988', '7888', '9888'], '8888', -1)]:
    got = open_lock(de, tg)
    assert got == want == open_lock_levels(de, tg) == open_lock_bidirectional(de, tg), (de, tg, got, want)
    print(de, tg, '->', got)
print("forgetting the '0000' dead-end check on example 3 ->", open_lock_no_start_check(['0000'], '8888'), '(should be -1)')

# ---- the graph itself: 10^4 states, every state has exactly 8 distinct neighbours, all reachable, distance = sum of wheel distances
states = [f'{i:04d}' for i in range(10 ** 4)]
assert all(len(set(neighbours(s))) == 8 for s in states)
dist = {'0000': 0}
q = deque(['0000'])
while q:
    s = q.popleft()
    for t in neighbours(s):
        if t not in dist:
            dist[t] = dist[s] + 1
            q.append(t)
assert len(dist) == 10 ** 4
assert all(dist[s] == sum(min(int(c), 10 - int(c)) for c in s) for s in states)
print('states', len(states), '| neighbours each 8 | edges', 8 * len(states) // 2, '| farthest state', max(dist, key=dist.get), 'at', max(dist.values()), 'moves')

# ---- every possible target with no dead ends equals the wheel-distance formula
for s in states[::7]:
    assert open_lock([], s) == dist[s]
print('open_lock([], target) == sum of per-wheel distances on', len(states[::7]), 'sampled targets')

# ---- seeded random cross-check with up to 500 dead ends
def rnd():
    return f'{random.randrange(10 ** 4):04d}'
for _ in range(300):
    de = [rnd() for _ in range(random.choice([0, 5, 50, 500, 2000]))]
    tg = rnd()
    r = open_lock(de, tg)
    assert r == open_lock_levels(de, tg) == open_lock_bidirectional(de, tg), (de[:5], tg)
print('300 seeded random cases: queue BFS == level-set BFS == bidirectional BFS')

# ---- edge cases
assert open_lock([], '0000') == 0
assert open_lock(['0000'], '0000') == -1
assert open_lock(['0001'], '0001') == -1                  # target is a dead end
assert open_lock(['1000', '9000', '0100', '0900', '0010', '0090', '0001', '0009'], '5555') == -1   # all 8 neighbours of the start jammed
print('edge asserts passed')

import heapq
import random
from collections import Counter, deque

random.seed(11)

def schedule_heap(tasks, n):
    h = [-c for c in Counter(tasks).values()]           # max-heap of remaining counts (negated ints)
    heapq.heapify(h)
    cool = deque()                                      # (time when usable again, remaining count)
    t = 0
    while h or cool:
        t += 1                                          # one slot per loop pass, idle or not
        while cool and cool[0][0] <= t:
            heapq.heappush(h, cool.popleft()[1])        # cooled down: back into the heap
        if h:
            left = heapq.heappop(h) + 1                 # run the task with most left
            if left:                                    # still has copies: cool for n slots
                cool.append((t + n + 1, left))
    return t

def schedule_formula(tasks, n):
    c = Counter(tasks)
    mx = max(c.values())
    k = sum(1 for v in c.values() if v == mx)
    return max(len(tasks), (mx - 1) * (n + 1) + k)

def schedule_brute(tasks, n):
    """BFS over states (remaining counts, cooldown left per letter): each slot runs a ready letter or idles."""
    letters = sorted(set(tasks))
    start = (tuple(tasks.count(l) for l in letters), (0,) * len(letters))
    seen, dq = {start}, deque([(start, 0)])
    while dq:
        (cnt, cd), t = dq.popleft()
        if not any(cnt): return t
        base = tuple(max(x - 1, 0) for x in cd)
        nxt = [(cnt, base)]                             # idle
        for i in range(len(cnt)):
            if cnt[i] and cd[i] == 0:
                c2, d2 = list(cnt), list(base)
                c2[i] -= 1; d2[i] = n
                nxt.append((tuple(c2), tuple(d2)))
        for s in nxt:
            if s not in seen:
                seen.add(s); dq.append((s, t + 1))

for fn in (schedule_heap, schedule_formula, schedule_brute):
    assert fn('AAABBB', 2) == 8
    assert fn('AAABBB', 0) == 6
    assert fn('AAAAAABCDEFG', 2) == 16
    assert fn('AABC', 1) == 4
    assert fn('A', 50) == 1

# exhaustive: every multiset of letters A-C (as sorted strings) up to length 7, n in 0..3
import itertools
count = 0
for L in range(1, 8):
    for combo in itertools.combinations_with_replacement('ABC', L):
        s = ''.join(combo)
        for n in range(4):
            b = schedule_brute(s, n)
            assert schedule_heap(s, n) == schedule_formula(s, n) == b, (s, n)
            assert b >= len(s) and b >= (max(Counter(s).values()) - 1) * (n + 1) + 1   # lower bounds
            count += 1
print('exhaustive over', count, 'multisets x n: heap == formula == BFS')

for _ in range(300):
    s = ''.join(random.choice('ABCD') for _ in range(random.randint(1, 8)))
    n = random.randint(0, 4)
    assert schedule_heap(s, n) == schedule_formula(s, n) == schedule_brute(s, n)
print('300 random strings ok')

big = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(10**4))
assert schedule_heap(big, 100) == schedule_formula(big, 100)
print('n = 10^4 tasks, cooldown 100: heap == formula =', schedule_formula(big, 100))

# the formula is a lower bound: the max letters form (mx-1) full frames of n+1 slots plus a last partial frame
print('AAABBB n=2 frame:  A B _ | A B _ | A B  -> (3-1)*(2+1) + 2 =', (3 - 1) * 3 + 2)
# when many distinct letters exist, no idle is ever needed and the answer is len(tasks)
print('ABCDEFGH n=2:', schedule_formula('ABCDEFGH', 2), '| AAABBBCCC n=1:', schedule_formula('AAABBBCCC', 1))
# heap tie-breaking: the heap holds bare ints, so ties never compare anything else.
# if you pushed (-count, letter) and later (-count, task_object) ties would compare the second field
h = []
heapq.heappush(h, (-2, {'t': 'A'}))
try:
    heapq.heappush(h, (-2, {'t': 'B'}))
except TypeError as e:
    print('TypeError if you store (count, unorderable task):', e)

import random
from collections import defaultdict

random.seed(3401)


def find_itinerary(tickets):
    """Hierholzer, iterative. Destinations sorted DEcreasing so pop() gives the smallest."""
    g = defaultdict(list)
    for a, b in tickets:
        g[a].append(b)
    for a in g:
        g[a].sort(reverse=True)
    route = []
    stack = ['JFK']
    while stack:
        while g[stack[-1]]:                      # still an unused ticket: walk it
            stack.append(g[stack[-1]].pop())
        route.append(stack.pop())                # dead end: this airport is the LAST of what remains
    return route[::-1]


def greedy_wrong(tickets):
    """Always take the smallest unused destination, never undo. Can strand tickets."""
    g = defaultdict(list)
    for a, b in tickets:
        g[a].append(b)
    for a in g:
        g[a].sort()
    path = ['JFK']
    while g[path[-1]]:
        path.append(g[path[-1]].pop(0))
    return path


def brute(tickets):
    """Backtracking: try destinations in sorted order, keep the first complete trip."""
    m = len(tickets)
    used = [False] * m

    def dfs(path):
        if len(path) == m + 1:
            return list(path)
        cur = path[-1]
        for dest in sorted({t[1] for i, t in enumerate(tickets) if not used[i] and t[0] == cur}):
            i = next(i for i, t in enumerate(tickets) if not used[i] and t == [cur, dest])
            used[i] = True
            path.append(dest)
            res = dfs(path)
            path.pop()
            used[i] = False
            if res:
                return res
        return None
    return dfs(['JFK'])


def random_trip(m, airports):
    """A random valid trail from JFK with m tickets (so an Eulerian trip exists), shuffled."""
    cur, tickets = 'JFK', []
    for _ in range(m):
        nxt = random.choice(airports)
        tickets.append([cur, nxt])
        cur = nxt
    random.shuffle(tickets)
    return tickets


# --- the prompt's examples ---
t1 = [['JFK', 'KUL'], ['JFK', 'NRT'], ['NRT', 'JFK']]
t2 = [['JFK', 'SFO'], ['JFK', 'ATL'], ['SFO', 'ATL'], ['ATL', 'JFK'], ['ATL', 'SFO']]
r1, r2 = find_itinerary(t1), find_itinerary(t2)
print(r1)
print(r2)
assert r1 == ['JFK', 'NRT', 'JFK', 'KUL'] == brute(t1)
assert r2 == ['JFK', 'ATL', 'JFK', 'SFO', 'ATL', 'SFO'] == brute(t2)
print('greedy on example 1 (wrong):', greedy_wrong(t1), '- stranded the NRT tickets')

# --- random cross-check against the backtracking oracle ---
airports = ['JFK', 'ATL', 'LAX', 'SFO', 'NRT']
bad = 0
for _ in range(1000):
    t = random_trip(random.randint(1, 9), airports)
    want = brute(t)
    assert find_itinerary(t) == want, t
    assert len(want) == len(t) + 1
    if greedy_wrong(t) != want:
        bad += 1
print('random cases passed: 1000; plain greedy was wrong on', bad, 'of them')

# --- edge cases ---
assert find_itinerary([['JFK', 'JFK']]) == ['JFK', 'JFK']                      # self loop ticket
assert find_itinerary([['JFK', 'AAA'], ['AAA', 'JFK'], ['JFK', 'AAA']]) == ['JFK', 'AAA', 'JFK', 'AAA']  # duplicates
assert find_itinerary([['JFK', 'ZZZ']]) == ['JFK', 'ZZZ']                      # one ticket
chain = [['JFK', 'A00']] + [['A%02d' % i, 'A%02d' % (i + 1)] for i in range(0, 99)]
assert find_itinerary(chain) == ['JFK'] + ['A%02d' % i for i in range(100)]   # forced path, 100 tickets
cyc = [['JFK', 'AAA'], ['AAA', 'JFK']] * 150                                   # 300 tickets, same pair repeated
assert len(find_itinerary(cyc)) == 301
print('edge asserts passed')

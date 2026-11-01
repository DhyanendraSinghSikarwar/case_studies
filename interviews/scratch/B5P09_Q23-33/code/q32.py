import itertools
import math
from collections import Counter, deque

GOAL = (1, 2, 3, 4, 5, 0)
# neighbours of each flat position on a 2 x 3 board: index = 3 * row + col
NB = {0: (1, 3), 1: (0, 2, 4), 2: (1, 5), 3: (0, 4), 4: (1, 3, 5), 5: (2, 4)}

def sliding_puzzle(board):
    """BFS over boards. A node is the whole board flattened to a tuple (hashable, so it can live in a set)."""
    start = tuple(x for row in board for x in row)
    if start == GOAL:
        return 0
    seen = {start}
    q = deque([(start, 0)])
    while q:
        s, d = q.popleft()
        z = s.index(0)
        for j in NB[z]:                                   # slide the tile at j into the blank
            l = list(s)
            l[z], l[j] = l[j], l[z]
            t = tuple(l)
            if t not in seen:
                if t == GOAL:
                    return d + 1
                seen.add(t)
                q.append((t, d + 1))
    return -1

def distance_table():
    """Independent method: one BFS BACKWARDS from the goal over all boards. Moves are reversible, so distance is symmetric."""
    dist = {GOAL: 0}
    frontier = [GOAL]
    while frontier:
        nxt = []
        for s in frontier:
            z = s.index(0)
            for j in NB[z]:
                l = list(s)
                l[z], l[j] = l[j], l[z]
                t = tuple(l)
                if t not in dist:
                    dist[t] = dist[s] + 1
                    nxt.append(t)
        frontier = nxt
    return dist

def inversions_even(flat):
    tiles = [x for x in flat if x]
    inv = sum(1 for i in range(len(tiles)) for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j])
    return inv % 2 == 0

for b, want in [([[1, 2, 3], [4, 0, 5]], 1), ([[1, 2, 3], [5, 4, 0]], -1), ([[4, 1, 2], [5, 0, 3]], 5), ([[1, 2, 3], [4, 5, 0]], 0)]:
    got = sliding_puzzle(b)
    assert got == want, (b, got, want)
    print(b, '->', got)

# ---- all 720 boards: forward BFS equals the backward table, and exactly half are unreachable
table = distance_table()
boards = list(itertools.permutations(range(6)))
assert len(boards) == 720
res = {}
for p in boards:
    b = [list(p[:3]), list(p[3:])]
    res[p] = sliding_puzzle(b)
    assert res[p] == table.get(p, -1), p
reach = sum(v >= 0 for v in res.values())
print('boards', len(boards), '| reachable', reach, '| unreachable', len(boards) - reach, '| hardest board needs', max(res.values()), 'moves')
print('boards per distance:', sorted(Counter(v for v in res.values() if v >= 0).items()))

# ---- why exactly half: a move never changes the parity of inversions among the 5 tiles (read row by row), and the goal has 0 inversions
assert all((res[p] >= 0) == inversions_even(p) for p in boards)
print('reachable  <=>  even number of inversions among tiles 1..5: holds for all 720 boards')
# a horizontal slide keeps the reading order of the tiles; a vertical slide jumps one tile over exactly 2 others (3-wide board), an even change
unsolvable = [[1, 2, 3], [5, 4, 0]]
print('example 2 has tiles read 1 2 3 5 4: one inversion (odd) ->', sliding_puzzle(unsolvable))

# ---- the state space grows too fast for the same code on bigger boards
print('states: 2x3', math.factorial(6), 'reachable', math.factorial(6) // 2, '| 3x3', math.factorial(9), 'reachable', math.factorial(9) // 2,
      '| 4x4', math.factorial(16), 'reachable', math.factorial(16) // 2)

# ---- the same BFS code does handle the 3x3 (8-puzzle) in memory, to show where the limit starts
def bfs_count_3x3():
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    seen = {goal}
    fr = [goal]
    depth = 0
    while True:
        nxt = []
        for s in fr:
            z = s.index(0)
            r, c = divmod(z, 3)
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = r + dr, c + dc
                if 0 <= a < 3 and 0 <= b < 3:
                    j = 3 * a + b
                    l = list(s)
                    l[z], l[j] = l[j], l[z]
                    t = tuple(l)
                    if t not in seen:
                        seen.add(t)
                        nxt.append(t)
        if not nxt:
            return len(seen), depth
        fr, depth = nxt, depth + 1
n3, depth3 = bfs_count_3x3()
assert n3 == math.factorial(9) // 2
print('3x3 BFS from the goal visits', n3, 'boards, hardest needs', depth3, 'moves; 4x4 would need about 10^13 (use A* or IDA* with a heuristic)')

# ---- edge asserts
assert sliding_puzzle([[1, 2, 3], [4, 5, 0]]) == 0
assert sliding_puzzle([[1, 2, 3], [4, 0, 5]]) == 1
assert sliding_puzzle([[0, 1, 2], [3, 4, 5]]) == table[(0, 1, 2, 3, 4, 5)] == 15
print('edge asserts passed')

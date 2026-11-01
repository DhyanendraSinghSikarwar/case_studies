import random

random.seed(43)

def islands_online(m, n, positions):
    """Union-find over cells numbered r * n + c. The island count changes by +1 for a new land cell and
    by -1 for every union that really merges two different islands."""
    parent = {}
    size = {}
    count = 0
    out = []

    def find(x):                                    # iterative, path halving
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    for r, c in positions:
        x = r * n + c
        if x not in parent:                         # a repeated cell changes nothing
            parent[x] = x
            size[x] = 1
            count += 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                rr, cc = r + dr, c + dc
                if 0 <= rr < m and 0 <= cc < n and rr * n + cc in parent:
                    if union(x, rr * n + cc):
                        count -= 1
        out.append(count)
    return out

def islands_flood(m, n, positions):
    """Brute force: after every addition rebuild the grid and count islands by an iterative flood fill. O(k * m * n)."""
    land = set()
    out = []
    for r, c in positions:
        land.add((r, c))
        seen = set()
        cnt = 0
        for cell in land:
            if cell in seen:
                continue
            cnt += 1
            seen.add(cell)
            st = [cell]
            while st:
                a, b = st.pop()
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    t = (a + da, b + db)
                    if t in land and t not in seen:
                        seen.add(t)
                        st.append(t)
        out.append(cnt)
    return out

# ---- examples from the prompt
assert islands_online(3, 3, [[0, 0], [0, 1], [1, 2], [2, 1]]) == [1, 1, 2, 3]
assert islands_online(3, 3, [[0, 0], [0, 1], [1, 2], [1, 1], [1, 1]]) == [1, 1, 2, 1, 1]
assert islands_online(1, 1, [[0, 0]]) == [1]
print('examples ok')

# ---- seeded cross-check against the flood-fill rebuild (duplicates, 1-wide grids, full grids)
N = 800
for _ in range(N):
    m, n = random.randint(1, 5), random.randint(1, 5)
    pos = [[random.randrange(m), random.randrange(n)] for _ in range(random.randint(1, 15))]
    assert islands_online(m, n, pos) == islands_flood(m, n, pos), (m, n, pos)
print('cross-check on', N, 'seeded grids: union-find == flood fill after every addition')

# ---- the count is NOT monotone: it can go up (new island), stay, or go down (a bridge cell merges islands)
print('counts:', islands_online(3, 3, [[0, 0], [2, 2], [1, 1], [0, 1], [1, 2]]))

# ---- edge cases
assert islands_online(1, 5, [[0, 0], [0, 4], [0, 2], [0, 1], [0, 3]]) == [1, 2, 3, 2, 1]
assert islands_online(2, 2, [[0, 0], [0, 0], [0, 0]]) == [1, 1, 1]        # same cell again and again
assert islands_online(2, 2, [[0, 0], [1, 1], [0, 1]]) == [1, 2, 1]          # diagonal cells are NOT connected
assert islands_online(2, 2, [[0, 0], [1, 1], [0, 1], [1, 0]]) == [1, 2, 1, 1]
# max size: 100 x 100 grid and 10^4 positions with repeats; and a 1 x 10^4 strip filled so unions chain
m = n = 100
pos = [[random.randrange(m), random.randrange(n)] for _ in range(10 ** 4)]
res = islands_online(m, n, pos)
print('100 x 100 grid, 10^4 random additions: final islands', res[-1], 'max seen', max(res))
strip = [[0, c] for c in range(0, 10000, 2)] + [[0, c] for c in range(1, 10000, 2)]
res = islands_online(1, 10000, strip)
print('1 x 10000 strip, even cells then odd cells: peak', max(res), 'final', res[-1])
assert max(res) == 5000 and res[-1] == 1

# ---- why the find must be iterative and the union must not build a long chain
def find_recursive(parent, x):
    return x if parent[x] == x else find_recursive(parent, parent[x])
parent = {i: i for i in range(10000)}
for i in range(9999):
    parent[i] = i + 1                              # naive linking in the unlucky direction: a chain of depth 9999
try:
    find_recursive(parent, 0)
except RecursionError:
    print('recursive find on a 10000-long chain: RecursionError (default limit 1000); the code above uses size + halving')
print('edge cases ok')

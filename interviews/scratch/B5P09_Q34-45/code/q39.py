import random
from functools import lru_cache

random.seed(39)

def remove_stones(stones):
    """Union-find where a stone (r, c) unions the ROW node r with the COLUMN node c.
    Answer = n - (number of groups that contain at least one stone)."""
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:                      # iterative, path halving
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for r, c in stones:
        parent[find(('r', r))] = find(('c', c))    # tag the kind so row 3 and column 3 are different nodes
    groups = {find(('r', r)) for r, c in stones}
    return len(stones) - len(groups)

def remove_stones_brute(stones):
    """Try every removal order with memoisation over the set of stones still standing (n <= 12)."""
    n = len(stones)

    @lru_cache(maxsize=None)
    def best(left):
        out = 0
        for i in range(n):
            if left >> i & 1:
                ri, ci = stones[i]
                if any(j != i and left >> j & 1 and (stones[j][0] == ri or stones[j][1] == ci) for j in range(n)):
                    out = max(out, 1 + best(left & ~(1 << i)))
        return out

    return best((1 << n) - 1)

def groups_dfs(stones):
    """Second reference: connected groups by an explicit stack over stones (same row or column)."""
    n = len(stones)
    seen = [False] * n
    cnt = 0
    for s in range(n):
        if not seen[s]:
            cnt += 1
            seen[s] = True
            st = [s]
            while st:
                u = st.pop()
                for v in range(n):
                    if not seen[v] and (stones[v][0] == stones[u][0] or stones[v][1] == stones[u][1]):
                        seen[v] = True
                        st.append(v)
    return cnt

# ---- examples from the prompt
assert remove_stones([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]) == 5
assert remove_stones([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]) == 3
assert remove_stones([[0, 0]]) == 0
print('examples ok')

# ---- the claim: answer == n - groups (a group of size s loses s - 1 stones, the last one has no partner)
S = [[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]
print('second example: n =', len(S), 'groups =', groups_dfs(S), '-> removable', len(S) - groups_dfs(S))

# ---- seeded cross-check against the exhaustive removal-order search (and the DFS group count)
N = 500
for _ in range(N):
    n = random.randint(1, 10)
    side = random.randint(2, 5)
    cells = [(r, c) for r in range(side) for c in range(side)]
    n = min(n, len(cells))
    st = [list(p) for p in random.sample(cells, n)]
    a = remove_stones(st)
    assert a == remove_stones_brute(tuple(map(tuple, st))), st
    assert a == len(st) - groups_dfs(st)
print('cross-check on', N, 'seeded small stone sets: union-find == exhaustive search == n - groups')

# ---- why one union per stone (not per pair of stones) is enough: a full row of stones is ONE group
row = [[5, c] for c in range(8)]
assert remove_stones(row) == 7
# a diagonal has no shared row or column: nothing can be removed
assert remove_stones([[i, i] for i in range(8)]) == 0

# ---- edge cases: same index as row and as column must stay separate nodes
assert remove_stones([[3, 7], [7, 3]]) == 0
assert remove_stones([[0, 0], [0, 1]]) == 1
assert remove_stones([[10000, 10000], [10000, 0], [0, 10000]]) == 2       # extreme coordinates
# max size: 1000 distinct stones in the 10001 x 10001 range
big = random.sample([(r, c) for r in range(0, 10001, 7) for c in range(0, 10001, 11)], 1000)
big = [list(p) for p in big]
print('n = 1000 random stones: removable', remove_stones(big), '| groups', 1000 - remove_stones(big))
# one staircase group of 1000 stones in a chain: remove 999
chain = [[i // 2 + (i % 2), i // 2] for i in range(1000)]
print('staircase chain of 1000 stones: removable', remove_stones(chain))
print('edge cases ok')

import random
import sys

random.seed(10)
WHITE, GREY, BLACK = 0, 1, 2

def has_cycle(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    color = [WHITE] * n
    for s in range(n):
        if color[s] != WHITE:
            continue
        color[s] = GREY
        stack = [(s, iter(adj[s]))]            # iterative DFS; the stack IS the grey path
        while stack:
            u, it = stack[-1]
            for v in it:
                if color[v] == GREY:           # back edge to the current path: cycle
                    return True
                if color[v] == WHITE:
                    color[v] = GREY
                    stack.append((v, iter(adj[v])))
                    break
                # BLACK: finished earlier, cannot lead back to u (see the explanation): ignore
            else:
                color[u] = BLACK               # all neighbours done
                stack.pop()
    return False

def brute(n, edges):
    """Transitive closure: a cycle exists iff some node reaches itself."""
    r = [[False] * n for _ in range(n)]
    for u, v in edges:
        r[u][v] = True
    for k in range(n):
        for i in range(n):
            if r[i][k]:
                for j in range(n):
                    if r[k][j]:
                        r[i][j] = True
    return any(r[i][i] for i in range(n))

def recursive(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    color = [0] * n
    def go(u):
        color[u] = GREY
        for v in adj[u]:
            if color[v] == GREY or (color[v] == WHITE and go(v)):
                return True
        color[u] = BLACK
        return False
    return any(color[s] == WHITE and go(s) for s in range(n))

assert has_cycle(4, [[0, 1], [1, 2], [2, 3], [3, 1]]) is True
assert has_cycle(3, [[0, 1], [0, 2], [1, 2]]) is False
assert has_cycle(2, [[1, 1]]) is True
assert has_cycle(1, []) is False
print('4 prompt examples ok')

for _ in range(1500):
    n = random.randint(1, 6)
    e = [[random.randrange(n), random.randrange(n)] for _ in range(random.randint(0, 7))]
    assert has_cycle(n, e) == brute(n, e) == recursive(n, e), (n, e)
print('1500 seeded random digraphs: iterative == closure == recursive')

pairs = [(u, v) for u in range(3) for v in range(3)]
for mask in range(512):
    e = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
    assert has_cycle(3, e) == brute(3, e)
pairs = [(u, v) for u in range(4) for v in range(4)]
for mask in range(1 << 16):
    e = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
    assert has_cycle(4, e) == brute(4, e)
print('exhaustive: all 512 digraphs on 3 nodes and all 65536 on 4 nodes (self loops included): ok')

# BLACK edge is not a cycle: the diamond 0->1, 0->2, 1->3, 2->3 reaches 3 twice, once through a black node
assert has_cycle(4, [[0, 1], [0, 2], [1, 3], [2, 3]]) is False
# treating BLACK like GREY (a plain 'seen' set) wrongly reports a cycle
def wrong_seen(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges: adj[u].append(v)
    seen = set(); st = [0]
    while st:
        u = st.pop(); seen.add(u)
        for v in adj[u]:
            if v in seen: return True
            st.append(v)
    return False
print('diamond DAG: three-colour says', has_cycle(4, [[0, 1], [0, 2], [1, 3], [2, 3]]), '| naive "seen" check says', wrong_seen(4, [[0, 1], [0, 2], [1, 3], [2, 3]]))

n = 2 * 10 ** 5
path = [[i, i + 1] for i in range(n - 1)]
assert has_cycle(n, path) is False and has_cycle(n, path + [[n - 1, 0]]) is True
print('path of 2*10^5 nodes: False; closed into a ring: True (iterative, no RecursionError)')
try:
    recursive(5000, path[:4999])
except RecursionError:
    print('recursive three-colour DFS on a 5000-node path: RecursionError at limit', sys.getrecursionlimit())

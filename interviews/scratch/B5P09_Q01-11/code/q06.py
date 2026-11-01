import random
import sys

random.seed(6)

def deep_dfs(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    for lst in adj:
        lst.sort()                                  # ascending neighbours
    seen = [False] * n; seen[0] = True
    order = [0]; depth = [0] * n; best = 0
    stack = [(0, iter(adj[0]))]                     # (node, iterator over its neighbours): resumes where it left off
    peak = 1
    while stack:
        u, it = stack[-1]
        for v in it:                                # continues from the saved position
            if not seen[v]:
                seen[v] = True; order.append(v)
                depth[v] = depth[u] + 1
                best = max(best, depth[v])
                stack.append((v, iter(adj[v])))
                peak = max(peak, len(stack))
                break                               # go deeper; come back to the rest later
        else:
            stack.pop()                             # neighbours exhausted: backtrack
    return [order, best], peak

def brute(n, edges):
    """Recursive version: same answer while the depth stays under the recursion limit."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    for lst in adj:
        lst.sort()
    order = []; seen = set(); best = [0]
    def go(u, d):
        seen.add(u); order.append(u); best[0] = max(best[0], d)
        for v in adj[u]:
            if v not in seen:
                go(v, d + 1)
    go(0, 0)
    return [order, best[0]]

assert deep_dfs(4, [[0, 2], [0, 1], [1, 3], [2, 3]])[0] == [[0, 1, 3, 2], 3]
assert deep_dfs(1, [])[0] == [[0], 0]
assert deep_dfs(5, [[0, 1], [1, 2], [2, 3], [3, 4]])[0] == [[0, 1, 2, 3, 4], 4]
print('3 prompt examples ok')

def rand_connected(n, extra):
    es = {(random.randrange(i), i) for i in range(1, n)}      # a random tree
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n) if (u, v) not in es]
    random.shuffle(pairs); es |= set(pairs[:extra])
    out = [list(e) if random.random() < .5 else [e[1], e[0]] for e in es]
    random.shuffle(out); return out

for _ in range(800):
    n = random.randint(1, 10)
    e = rand_connected(n, random.randint(0, 4))
    assert deep_dfs(n, e)[0] == brute(n, e), (n, e)
print('800 seeded random connected graphs: iterative == recursive')

n = 2 * 10 ** 5
path = [[i, i + 1] for i in range(n - 1)]
(order, depth), peak = deep_dfs(n, path)
assert order == list(range(n)) and depth == n - 1
print('path of 2*10^5 nodes: depth', depth, '| explicit stack peaked at', peak, 'frames')
try:
    brute(5000, path[:4999])
except RecursionError:
    print('recursive DFS on a 5000-node path: RecursionError at limit', sys.getrecursionlimit())

star = [[0, i] for i in range(1, n)]
(order, depth), peak = deep_dfs(n, star)
assert order == list(range(n)) and depth == 1
print('star of 2*10^5 nodes: depth', depth, '| stack peak', peak, '(the stack tracks depth, not size)')

# a path whose labels are shuffled still gives the same shape of answer
perm = list(range(n)); random.shuffle(perm); perm.remove(0); perm = [0] + perm
sh = [[perm[i], perm[i + 1]] for i in range(n - 1)]
(order, depth), _ = deep_dfs(n, sh)
assert order == perm and depth == n - 1
print('shuffled-label path of 2*10^5 nodes: preorder is the path order, depth', depth)

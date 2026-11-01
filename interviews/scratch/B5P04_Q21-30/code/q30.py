import random
import time
from collections import deque


def bfs_levels(graph, source):
    queue = deque([source])
    seen = {source}
    levels, dist = [], {source: 0}
    while queue:
        size = len(queue)                            # snapshot: this round is one level
        level = []
        for _ in range(size):
            node = queue.popleft()
            level.append(node)
            for nxt in graph.get(node, []):
                if nxt not in seen:                  # mark on ENQUEUE
                    seen.add(nxt)
                    dist[nxt] = dist[node] + 1
                    queue.append(nxt)
        levels.append(level)
    return levels, dist


def bfs_list_pop0(graph, source):                    # same logic, list.pop(0): correct but O(n) pops
    queue = [source]
    seen = {source}
    dist = {source: 0}
    while queue:
        node = queue.pop(0)
        for nxt in graph.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return dist


def enqueues_mark_on_dequeue(graph, source):         # the bug: counts how many times nodes are queued
    queue = deque([source])
    seen = set()
    count = 0
    while queue:
        node = queue.popleft()
        if node in seen:
            continue
        seen.add(node)
        for nxt in graph.get(node, []):
            queue.append(nxt)
            count += 1
    return count + 1


def dist_reference(graph, source):                   # brute: expand a frontier set round by round
    dist = {source: 0}
    frontier = {source}
    d = 0
    while frontier:
        d += 1
        nxt = set()
        for u in frontier:
            for v in graph.get(u, []):
                if v not in dist:
                    nxt.add(v)
        for v in nxt:
            dist[v] = d
        frontier = nxt
    return dist


G = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["F"], "E": ["F"], "F": []}
levels, dist = bfs_levels(G, "A")
print("levels:", levels)
print("distances:", dist)
assert levels == [["A"], ["B", "C"], ["D", "E"], ["F"]]
assert dist["F"] == 3
assert bfs_list_pop0(G, "A") == dist == dist_reference(G, "A")

print("enqueues, mark on enqueue:", len(dist), "| mark on dequeue:", enqueues_mark_on_dequeue(G, "A"))
assert enqueues_mark_on_dequeue(G, "A") > len(dist)

assert bfs_levels({"X": []}, "X") == ([["X"]], {"X": 0})                    # lone node
assert bfs_levels({"A": ["A", "B"], "B": ["A"]}, "A")[0] == [["A"], ["B"]]  # self-loop and cycle
assert bfs_levels({"A": ["B"]}, "A")[0] == [["A"], ["B"]]                   # B missing from the dict
assert bfs_levels({"A": [], "Z": ["A"]}, "A")[1] == {"A": 0}                # Z unreachable

rng = random.Random(30)
for _ in range(500):
    n = rng.randint(1, 9)
    g = {i: [rng.randrange(n) for _ in range(rng.randint(0, 3))] for i in range(n)}
    src = rng.randrange(n)
    lv, d = bfs_levels(g, src)
    assert d == dist_reference(g, src) == bfs_list_pop0(g, src)
    assert [d[x] for lvl in lv for x in lvl] == sorted(d.values())          # levels in distance order
    assert all(d[x] == i for i, lvl in enumerate(lv) for x in lvl)
print("random cross-check passed: 500 random directed graphs (cycles, self-loops, duplicates)")

N = 100_000
t0 = time.perf_counter()
dq = deque(range(N))
while dq:
    dq.popleft()
t_deque = time.perf_counter() - t0
t0 = time.perf_counter()
ls = list(range(N))
while ls:
    ls.pop(0)
t_list = time.perf_counter() - t0
print(f"draining {N} items, sandbox timing (Python 3.13, one run): deque {t_deque:.3f}s, list.pop(0) {t_list:.3f}s")
assert t_list > t_deque

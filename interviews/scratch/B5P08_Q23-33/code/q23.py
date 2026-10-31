import random, itertools

def reconstruct(people):
    out = []
    for h, k in sorted(people, key=lambda p: (-p[0], p[1])):
        out.insert(k, [h, k])          # k taller-or-equal people are already placed
    return out

def pairs_of(queue):                   # the [h, k] each person would report
    return [[h, sum(1 for x in queue[:i] if x >= h)] for i, h in enumerate(queue)]

def brute(people):                     # try every ordering, keep all that are consistent
    good = set()
    for perm in itertools.permutations(map(tuple, people)):
        if all(k == sum(1 for h2, _ in perm[:i] if h2 >= h) for i, (h, k) in enumerate(perm)):
            good.add(perm)
    return good

# examples from the prompt
assert reconstruct([[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]) == [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
assert reconstruct([[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]) == [[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]]
assert reconstruct([[3,0]]) == [[3,0]]

# randomised cross-check against brute force (also checks uniqueness for each input)
rng = random.Random(23)
for _ in range(300):
    n = rng.randint(1, 7)
    heights = [rng.randint(1, 5) for _ in range(n)]
    people = pairs_of(heights)
    rng.shuffle(people)
    sols = brute(people)
    assert len(sols) == 1, people                     # unique queue
    assert [list(p) for p in next(iter(sols))] == reconstruct(people)
print("random cross-check vs brute force: 300 cases OK")

# exhaustive uniqueness: every height sequence of length <= 7 over heights 1..4
# (and length <= 5 over 1..6); the multiset of [h, k] pairs must determine the queue
total = 0
for n, H in [(n, 4) for n in range(1, 8)] + [(n, 6) for n in range(1, 6)]:
    seen = {}
    for heights in itertools.product(range(1, H + 1), repeat=n):
        q = pairs_of(list(heights))
        seen.setdefault(tuple(sorted(map(tuple, q))), set()).add(tuple(map(tuple, q)))
        total += 1
    assert all(len(v) == 1 for v in seen.values()), (n, H)
print("uniqueness: queues checked =", total, "-> no two queues share a pair multiset")

# list.insert cost: worst case, every insert at the front (n(n-1)/2 element moves)
n = 2000
people = [[i, 0] for i in range(1, n + 1)]            # valid queue: heights ascending
rng.shuffle(people)
res = reconstruct(people)
assert res == [[i, 0] for i in range(1, n + 1)]
print("worst case n=2000: elements shifted by insert =", n * (n - 1) // 2)

# garbage in: an impossible input is not detected, insert just clamps to the end
print("invalid input (no real queue):", reconstruct([[5, 3], [4, 0]]))

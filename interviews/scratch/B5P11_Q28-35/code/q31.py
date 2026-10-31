import itertools, random, sys, time
from functools import lru_cache

random.seed(3101)
INF = float("inf")


def assign(cost):
    """f[mask] = min cost for workers popcount(mask)..n-1 to take exactly the tasks NOT in mask.
    Filled from the full mask down to 0; then walk forward taking the smallest task that stays optimal."""
    n = len(cost)
    full = (1 << n) - 1
    f = [INF] * (1 << n)
    f[full] = 0                                       # everyone has a task: nothing left to pay
    for mask in range(full - 1, -1, -1):
        w = mask.bit_count()                          # the next worker is w
        best = INF
        for t in range(n):
            if not mask >> t & 1:                     # task t still free
                v = cost[w][t] + f[mask | 1 << t]
                if v < best:
                    best = v
        f[mask] = best
    mask, out = 0, []
    for w in range(n):
        for t in range(n):                            # ascending t -> lexicographically smallest list
            if not mask >> t & 1 and cost[w][t] + f[mask | 1 << t] == f[mask]:
                out.append(t)
                mask |= 1 << t
                break
    return [f[0], out], f


def assign_memo(cost):
    """Top-down: same state, depth n + 1 <= 16, so recursion is no problem here."""
    n = len(cost)

    @lru_cache(maxsize=None)
    def g(mask):
        w = mask.bit_count()
        if w == n:
            return 0
        return min(cost[w][t] + g(mask | 1 << t) for t in range(n) if not mask >> t & 1)

    mask, out = 0, []
    for w in range(n):
        for t in range(n):
            if not mask >> t & 1 and cost[w][t] + g(mask | 1 << t) == g(mask):
                out.append(t); mask |= 1 << t; break
    return [g(0), out]


def brute(cost):
    n = len(cost)
    return list(min((sum(cost[i][p[i]] for i in range(n)), list(p)) for p in itertools.permutations(range(n))))


# ---- prompt examples
ex = [([[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]], [13, [1, 0, 2, 3]]),
      ([[5]], [5, [0]]), ([[1, 1], [1, 1]], [2, [0, 1]]), ([[3, 1], [1, 3]], [2, [1, 0]])]
for c, want in ex:
    assert assign(c)[0] == assign_memo(c) == brute(c) == want, c
print("prompt examples OK")

# ---- hand table for the first example (bit t of the mask = task t is taken)
c = ex[0][0]
res, f = assign(c)
print("f[mask]: workers popcount(mask).. take the tasks NOT in mask")
for mask in range((1 << 4) - 1, -1, -1):
    w = mask.bit_count()
    if w == 4:
        why = "base"
    else:
        opts = [f"t{t}:{c[w][t]}+{f[mask | 1 << t]}" for t in range(4) if not mask >> t & 1]
        why = "worker %d: " % w + "  ".join(opts)
    print(f"  mask {mask:04b}  f={f[mask]:>2}   {why}")
print("walk forward:", res)

# ---- seeded cross-check against every permutation (n <= 7), lexicographic tie rule included
cnt = ties = 0
for _ in range(300):
    n = random.randint(1, 7)
    hi = random.choice([1, 3, 20])                    # tiny values make many tied optimal assignments
    cost = [[random.randint(0, hi) for _ in range(n)] for _ in range(n)]
    got, want = assign(cost)[0], brute(cost)
    assert got == assign_memo(cost) == want, (cost, got, want)
    best = want[0]
    nopt = sum(sum(cost[i][p[i]] for i in range(n)) == best for p in itertools.permutations(range(n)))
    ties += nopt > 1
    cnt += 1
print("random cross-check:", cnt, "matrices agree;", ties, "had several optimal assignments")

# ---- exhaustive: every 2x2 matrix with entries 0..3 and every 3x3 matrix with entries 0..2
ex_cnt = 0
for n, hi in ((2, 3), (3, 2)):
    for flat in itertools.product(range(hi + 1), repeat=n * n):
        cost = [list(flat[i * n:(i + 1) * n]) for i in range(n)]
        assert assign(cost)[0] == brute(cost), cost
        ex_cnt += 1
print("exhaustive:", ex_cnt, "small matrices agree")

# ---- why a naive greedy (each worker takes the cheapest free task, in order) fails
def greedy(cost):
    used, tot, out = set(), 0, []
    for w, row in enumerate(cost):
        t = min((x for x in range(len(cost)) if x not in used), key=lambda x: row[x])
        used.add(t); tot += row[t]; out.append(t)
    return [tot, out]
rg = random.Random(3102)
bad = 0
for _ in range(300):
    cost = [[rg.randint(0, 9) for _ in range(5)] for _ in range(5)]
    bad += greedy(cost)[0] != brute(cost)[0]
print("greedy gives a worse total on", bad, "of 300 random 5x5 matrices")

# ---- the size limit in the prompt: n = 15 (2^15 * 15 transitions); 18 shown for scale, timing is sandbox-only
rng = random.Random(3103)
for n in (12, 15, 18):
    cost = [[rng.randint(0, 1000) for _ in range(n)] for _ in range(n)]
    t0 = time.perf_counter()
    r = assign(cost)[0]
    dt = time.perf_counter() - t0
    assert sorted(r[1]) == list(range(n)) and sum(cost[w][t] for w, t in enumerate(r[1])) == r[0]
    print(f"n={n}: {(1 << n) * n:>9,} transitions, best {r[0]}  [sandbox time {dt:.2f}s]")
print("n=20 would be", f"{(1 << 20) * 20:,}", "transitions and a table of", f"{1 << 20:,}", "entries; n=25 gives", f"{(1 << 25) * 25:,}")

# ---- edge cases
assert assign([[0]])[0] == [0, [0]]
assert assign([[7, 7], [7, 7]])[0] == [14, [0, 1]]
assert assign([[0] * 3 for _ in range(3)])[0] == [0, [0, 1, 2]]
print("edge cases OK; limit", sys.getrecursionlimit())

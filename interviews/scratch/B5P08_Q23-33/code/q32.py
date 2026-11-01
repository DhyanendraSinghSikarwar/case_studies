import itertools, random

def activity(acts):                                   # earliest finish first
    cnt, end = 0, -10**18
    for s, e in sorted(acts, key=lambda a: a[1]):
        if s >= end: cnt += 1; end = e
    return cnt

def greedy_by(acts, key):                             # generic rule: scan in key order, take if compatible with all chosen
    chosen = []
    for s, e in sorted(acts, key=key):
        if all(e <= c[0] or c[1] <= s for c in chosen): chosen.append([s, e])
    return len(chosen)

def brute(acts):
    best = 0
    for m in range(1 << len(acts)):
        sel = [acts[i] for i in range(len(acts)) if m >> i & 1]
        if all(a[1] <= b[0] or b[1] <= a[0] for a, b in itertools.combinations(sel, 2)):
            best = max(best, len(sel))
    return best

assert activity([[1,4],[3,5],[0,6],[5,7],[3,9],[5,9],[6,10],[8,11],[8,12],[2,14],[12,16]]) == 4
assert activity([[1,3],[2,4],[3,5]]) == 2
assert activity([[0,10],[1,2],[3,4]]) == 2
assert activity([[0,3],[2,4],[3,6],[4,7]]) == 2

rng = random.Random(32)
for _ in range(1500):
    acts = []
    for _ in range(rng.randint(1, 9)):
        s = rng.randint(0, 8); acts.append([s, rng.randint(s + 1, 9)])
    assert activity(acts) == brute(acts) == greedy_by(acts, key=lambda a: a[1]), acts
print("1500 random cases: earliest-finish greedy == brute force")

# Exhaustive: the two wrong rules over ALL ordered lists of 1..3 activities with times 0..6
ivs = [[s, e] for s in range(7) for e in range(s + 1, 7)]
rules = {"shortest first": lambda a: a[1] - a[0], "earliest start first": lambda a: a[0]}
for name, key in rules.items():
    fail = {1: 0, 2: 0, 3: 0}; sets3 = set()
    for n in (1, 2, 3):
        for acts in itertools.product(ivs, repeat=n):
            acts = list(map(list, acts))
            if greedy_by(acts, key) != brute(acts):
                fail[n] += 1
                if n == 3: sets3.add(tuple(sorted(map(tuple, acts))))
    # failures that survive EVERY input order (so they do not depend on how ties are broken)
    robust = sorted(s3 for s3 in sets3
                    if all(greedy_by([list(x) for x in p], key) != brute([list(x) for x in p])
                           for p in itertools.permutations(s3)))
    assert fail[1] == fail[2] == 0 and robust
    print(f"{name}: failing lists with 1, 2, 3 activities = {fail[1]}, {fail[2]}, {fail[3]}; "
          f"order-independent failing 3-sets = {len(robust)}, e.g. {[list(x) for x in robust[0]]}")
# earliest finish never fails on the same exhaustive set
for n in (1, 2, 3):
    for acts in itertools.product(ivs, repeat=n):
        acts = list(map(list, acts))
        assert activity(acts) == brute(acts)
print("earliest finish first: 0 failures on the same exhaustive set")

# the prompt's counter-examples, spelled out
print("shortest first on [[0,3],[2,4],[3,6]]:", greedy_by([[0,3],[2,4],[3,6]], rules["shortest first"]), "vs optimal", brute([[0,3],[2,4],[3,6]]))
print("earliest start on [[0,10],[1,2],[3,4]]:", greedy_by([[0,10],[1,2],[3,4]], rules["earliest start first"]), "vs optimal", brute([[0,10],[1,2],[3,4]]))

# scale: n = 100000, one sort + one pass
big = []
for _ in range(100000):
    s = rng.randint(0, 10**6); big.append([s, s + rng.randint(1, 20)])
print("n=100000 ->", activity(big), "activities")

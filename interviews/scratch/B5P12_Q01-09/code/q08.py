import itertools
import random

random.seed(1208)

def comb_sum(candidates, target):
    """Sorted candidates, start index, break when too big. Returns (list, calls, max depth)."""
    cs = sorted(candidates)
    out, cur, st = [], [], {'calls': 0, 'depth': 0}
    def go(start, remain):
        st['calls'] += 1
        st['depth'] = max(st['depth'], len(cur))
        if remain == 0:
            out.append(cur[:]); return
        for i in range(start, len(cs)):
            if cs[i] > remain:
                break                       # sorted: every later candidate is too big as well
            cur.append(cs[i])               # choose
            go(i, remain - cs[i])           # explore: SAME index i => reuse allowed, no reordering
            cur.pop()                       # undo
    go(0, target)
    return sorted(out), st['calls'], st['depth']

def comb_sum_no_break(candidates, target):
    """Start index but no break: overshoots are visited and rejected one call later."""
    cs = sorted(candidates); out, cur, calls = [], [], [0]
    def go(start, remain):
        calls[0] += 1
        if remain < 0:
            return
        if remain == 0:
            out.append(cur[:]); return
        for i in range(start, len(cs)):
            cur.append(cs[i]); go(i, remain - cs[i]); cur.pop()
    go(0, target)
    return sorted(out), calls[0]

def comb_sum_ordered(candidates, target):
    """No start index: every ORDER is explored (permutations); dedupe by sorting at the end."""
    cs = sorted(candidates); out, cur, calls = set(), [], [0]
    def go(remain):
        calls[0] += 1
        if remain < 0:
            return
        if remain == 0:
            out.add(tuple(sorted(cur))); return
        for v in cs:
            cur.append(v); go(remain - v); cur.pop()
    go(target)
    return sorted(map(list, out)), calls[0]

def brute(candidates, target):
    out = set()
    for length in range(1, target // min(candidates) + 1):
        for combo in itertools.combinations_with_replacement(sorted(candidates), length):
            if sum(combo) == target:
                out.add(combo)
    return sorted(map(list, out))

examples = [(([3, 4, 5], 12), [[3, 3, 3, 3], [3, 4, 5], [4, 4, 4]]), (([3, 5], 2), []), (([2], 8), [[2, 2, 2, 2]]),
            (([1], 3), [[1, 1, 1]]), (([7, 2, 4], 11), [[2, 2, 7], [4, 7]])]
for (c, t), want in examples:
    assert comb_sum(c, t)[0] == want == brute(c, t) == comb_sum_no_break(c, t)[0] == comb_sum_ordered(c, t)[0]
    print(c, t, '->', comb_sum(c, t)[0])

# decision tree for candidates [2, 3], target 5 (sorted). 'X' = pruned by the break
def tree(cs, start, remain, d, cur):
    if remain == 0:
        print('  ' * d + f'{cur} sum hit: answer'); return
    for i in range(start, len(cs)):
        if cs[i] > remain:
            print('  ' * d + f'{cs[i]} > remain {remain}: break'); break
        print('  ' * d + f'take {cs[i]} (remain {remain - cs[i]}, next index {i})')
        tree(cs, i, remain - cs[i], d + 1, cur + [cs[i]])
tree([2, 3], 0, 5, 0, [])

# calls: break vs no break vs no start index (small cases; the ordered version explodes)
print('case                      answers  break  no-break  ordered')
for c, t in [([3, 4, 5], 12), ([2, 3, 6, 7], 7), ([2, 3, 5], 10), ([1, 2], 12)]:
    a, ca, _ = comb_sum(c, t); b, cb = comb_sum_no_break(c, t); o, co = comb_sum_ordered(c, t)
    assert a == b == o
    print(f'{str(c):12} t={t:<3}        {len(a):7} {ca:6} {cb:9} {co:8}')

# seeded cross-check
for _ in range(1500):
    c = random.sample(range(1, 13), random.randint(1, 5)); t = random.randint(1, 20)
    assert comb_sum(c, t)[0] == brute(c, t)
print('random cross-check ok: 1500 cases')

# edge: depth bound. candidate 1, target 40 -> 40 chosen numbers, 41 frames: far below the recursion limit of 1000
r, calls, depth = comb_sum([1], 40)
assert r == [[1] * 40] and depth == 40
r2, calls2, depth2 = comb_sum([1, 2, 3, 4, 5, 6, 7, 8], 40)
assert depth2 == 40 and all(sum(x) == 40 and x == sorted(x) for x in r2)
print('max depth (chosen numbers):', depth2, ' answers for [1..8], 40:', len(r2), ' calls:', calls2)
assert comb_sum([5], 3)[0] == [] and comb_sum([40], 40)[0] == [[40]]
print('edge asserts ok')

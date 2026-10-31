import functools
import random

random.seed(1314)

def four_sorts(records):
    name, dept, score = (lambda r: r[0]), (lambda r: r[1]), (lambda r: r[2])
    A = [r[0] for r in sorted(records, key=lambda r: (r[1], -r[2]))]
    t = list(records)
    t.sort(key=score, reverse=True)        # least significant key first
    t.sort(key=dept)                       # then the most significant key; stability keeps the score order inside a dept
    B = [r[0] for r in t]
    C = [r[0] for r in sorted(records, key=dept, reverse=True)]
    D = [r[0] for r in sorted(records, key=dept)[::-1]]
    return [A, B, C, D]

def brute(records):
    """Index-aware comparison: original position is the final tie-break, so no stability is assumed."""
    idx = list(range(len(records)))
    def cmp_a(i, j):                                   # dept asc, score desc, then position asc
        a, b = records[i], records[j]
        return (a[1] > b[1]) - (a[1] < b[1]) or (b[2] > a[2]) - (b[2] < a[2]) or (i > j) - (i < j)
    def cmp_c(i, j):                                   # dept DESC, position ASC (equal depts keep input order)
        a, b = records[i], records[j]
        return (b[1] > a[1]) - (b[1] < a[1]) or (i > j) - (i < j)
    def cmp_d(i, j):                                   # dept DESC, position DESC (the reversed result)
        a, b = records[i], records[j]
        return (b[1] > a[1]) - (b[1] < a[1]) or (j > i) - (j < i)
    pick = lambda c: [records[i][0] for i in sorted(idx, key=functools.cmp_to_key(c))]
    A = pick(cmp_a)
    return [A, A, pick(cmp_c), pick(cmp_d)]

examples = [
    ([['ann', 'hr', 5], ['bob', 'it', 7], ['cat', 'hr', 5], ['dan', 'it', 9], ['eve', 'hr', 8]],
     [['eve', 'ann', 'cat', 'dan', 'bob'], ['eve', 'ann', 'cat', 'dan', 'bob'],
      ['bob', 'dan', 'ann', 'cat', 'eve'], ['dan', 'bob', 'eve', 'cat', 'ann']]),
    ([['x', 'a', 1]], [['x'], ['x'], ['x'], ['x']]),
    ([['p', 'b', 2], ['q', 'a', 2], ['r', 'b', 2], ['s', 'a', 3]],
     [['s', 'q', 'p', 'r'], ['s', 'q', 'p', 'r'], ['p', 'r', 'q', 's'], ['r', 'p', 's', 'q']]),
]
for rec, exp in examples:
    got = four_sorts(rec)
    print(got)
    assert got == exp and brute(rec) == exp

# C vs D: reverse=True keeps equal records in input order, [::-1] reverses them
two = [['a', 'x', 0], ['b', 'x', 0]]
C, D = four_sorts(two)[2:]
print('two records, same dept: C =', C, ' D =', D)
assert C == ['a', 'b'] and D == ['b', 'a']

# strings cannot be negated: -r[1] raises, so the two-pass trick is the way to get dept DESC + score ASC
try:
    sorted(examples[0][0], key=lambda r: (-r[1], r[2]))
except TypeError as e:
    print('negating a str:', type(e).__name__)
t = list(examples[0][0]); t.sort(key=lambda r: r[2]); t.sort(key=lambda r: r[1], reverse=True)
print('dept desc then score asc via two passes:', [r[0] for r in t])
# the same with cmp_to_key
def cmp(a, b):
    return (b[1] > a[1]) - (b[1] < a[1]) or (a[2] > b[2]) - (a[2] < b[2])
assert [r[0] for r in sorted(examples[0][0], key=functools.cmp_to_key(cmp))] == [r[0] for r in t]

# the pass ORDER matters: dept first then score gives a different answer
wrong = list(examples[0][0]); wrong.sort(key=lambda r: r[1]); wrong.sort(key=lambda r: r[2], reverse=True)
print('wrong pass order:', [r[0] for r in wrong], '(A is', examples[0][1][0], ')')
assert [r[0] for r in wrong] != examples[0][1][0]

# key= is called once per record, not once per comparison
calls = [0]
def counting_key(r):
    calls[0] += 1
    return r[1]
sorted(examples[0][0], key=counting_key)
print('key calls for 5 records:', calls[0])
assert calls[0] == 5

# seeded random cross-check: A == B, all four equal the index-aware comparison
tie_seen = 0
for _ in range(400):
    n = random.randint(1, 12)
    rec = [[random.choice('abcde'), random.choice(['hr', 'it', 'ops']), random.randint(-3, 3)] for _ in range(n)]
    r = four_sorts(rec)
    assert r == brute(rec) and r[0] == r[1]
    if r[2] != r[3]:
        tie_seen += 1
print('random cross-check ok: 400 cases; C != D in', tie_seen, 'of them')

# edge asserts
assert four_sorts([['x', 'a', 1]]) == [['x']] * 4
assert four_sorts([['a', 'z', 1], ['b', 'z', 1]])[0] == ['a', 'b']   # all keys equal: input order survives in A
print('edge asserts ok')

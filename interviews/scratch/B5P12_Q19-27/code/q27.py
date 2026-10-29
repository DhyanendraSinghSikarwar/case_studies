import random

random.seed(27)

class MapSum:
    """Trie where every node keeps the sum of the values of all keys at or below it."""
    def __init__(self):
        self.root = {}            # node: dict of child letter -> node, plus the key '#' holding the running sum
        self.vals = {}            # key -> current value (needed to compute new - old)
        self.steps = 0            # trie steps taken, to compare with a scan
    def insert(self, key, val):
        delta = val - self.vals.get(key, 0)           # replacing a key adds only the DIFFERENCE
        self.vals[key] = val
        nd = self.root
        for ch in key:
            nd = nd.setdefault(ch, {}); self.steps += 1
            nd['#'] = nd.get('#', 0) + delta
    def sum(self, prefix):
        nd = self.root
        for ch in prefix:
            nd = nd.get(ch); self.steps += 1
            if nd is None: return 0
        return nd['#']

def solve(ops):
    m = MapSum(); res = []
    for op in ops:
        if op[0] == 'insert': m.insert(op[1], op[2]); res.append(None)
        else: res.append(m.sum(op[1]))
    return res

def brute(ops):
    d = {}; res = []
    for op in ops:
        if op[0] == 'insert': d[op[1]] = op[2]; res.append(None)
        else: res.append(sum(v for k, v in d.items() if k.startswith(op[1])))
    return res

def wrong_add_not_delta(ops):
    """The tempting bug: add val instead of new - old, so a replaced key counts twice."""
    m = MapSum(); res = []
    for op in ops:
        if op[0] == 'insert':
            nd = m.root
            for ch in op[1]:
                nd = nd.setdefault(ch, {}); nd['#'] = nd.get('#', 0) + op[2]
            res.append(None)
        else: res.append(m.sum(op[1]))
    return res

N = None
for ops, exp in [([['insert', 'apple', 3], ['sum', 'ap'], ['insert', 'app', 2], ['sum', 'ap'], ['insert', 'apple', 5], ['sum', 'app'], ['sum', 'b']], [N, 3, N, 5, N, 7, 0]),
                 ([['sum', 'a']], [0]),
                 ([['insert', 'a', 0], ['sum', 'a'], ['insert', 'a', 7], ['sum', 'a']], [N, 0, N, 7])]:
    got = solve(ops)
    assert got == exp == brute(ops)
    print('example ->', got)

# trace of example 1: node sums after each insert
m = MapSum()
def snap(label):
    parts = []
    for pre in ['a', 'ap', 'app', 'appl', 'apple']:
        nd = m.root
        for ch in pre: nd = nd[ch]
        parts.append(f'{pre}={nd["#"]}')
    print(f'  after {label}: ' + ', '.join(parts))
m.insert('apple', 3); snap("insert apple 3")
m.insert('app', 2); snap("insert app 2")
m.insert('apple', 5); snap("insert apple 5 (delta +2, not +5)")
print('  sum(ap) =', m.sum('ap'), ' sum(app) =', m.sum('app'), ' sum(b) =', m.sum('b'))
ops1 = [['insert', 'apple', 3], ['sum', 'ap'], ['insert', 'app', 2], ['sum', 'ap'], ['insert', 'apple', 5], ['sum', 'app'], ['sum', 'b']]
print('the add-val-not-delta bug on example 1 gives', wrong_add_not_delta(ops1), '(expected 3, 5, 7, 0 at the sum positions)')
assert wrong_add_not_delta(ops1) != solve(ops1)

# cost: trie steps vs keys scanned by the baseline
rnd = random.Random(270)
keys = [''.join(rnd.choice('abcd') for _ in range(rnd.randint(1, 12))) for _ in range(1500)]
ops = []
for i in range(5000):
    if rnd.random() < .5: ops.append(['insert', rnd.choice(keys), rnd.randint(0, 1000)])
    else: ops.append(['sum', rnd.choice(keys)[:rnd.randint(1, 6)]])
mm = MapSum(); got = []
scanned = 0; live = {}
for op in ops:
    if op[0] == 'insert': mm.insert(op[1], op[2]); live[op[1]] = op[2]
    else: got.append(mm.sum(op[1])); scanned += len(live)
assert [x for x in solve(ops) if x is not None] == got
print('5000 mixed operations, keys of length <= 12: trie steps in total', mm.steps, '| keys a scan-per-sum would have examined', scanned)

# seeded random cross-check vs dict + startswith, including repeated replacement and value 0
for _ in range(500):
    ks = [''.join(random.choice('ab') for _ in range(random.randint(1, 4))) for _ in range(5)]
    ops = []
    for _ in range(random.randint(1, 30)):
        if random.random() < .55: ops.append(['insert', random.choice(ks), random.randint(0, 5)])
        else: ops.append(['sum', ''.join(random.choice('ab') for _ in range(random.randint(1, 3)))])
    assert solve(ops) == brute(ops), ops
print('500 seeded random operation lists agree with the dict scanned with startswith')

# edge asserts
assert solve([['sum', 'a']]) == [0]
assert solve([['insert', 'a', 5], ['insert', 'a', 5], ['sum', 'a']]) == [None, None, 5]
assert solve([['insert', 'ab', 9], ['insert', 'ab', 0], ['sum', 'a'], ['sum', 'ab'], ['sum', 'abc']]) == [None, None, 0, 0, 0]
assert solve([['insert', 'z' * 20, 1000], ['sum', 'z'], ['sum', 'z' * 20], ['sum', 'z' * 21]]) == [None, 1000, 1000, 0]
print('edge asserts passed')

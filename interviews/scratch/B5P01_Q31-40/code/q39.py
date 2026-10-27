from collections import Counter, defaultdict

words = ['b', 'a', 'b', 'c', 'a', 'b']

# Idioms: all give the same counts
c1 = Counter(words)
c2 = defaultdict(int)
for w in words:
    c2[w] += 1
c3 = {}
for w in words:
    c3[w] = c3.get(w, 0) + 1
c4 = {}
for w in words:
    c4.setdefault(w, [0])[0] += 1               # setdefault is for list/set values, shown only for contrast
assert dict(c1) == dict(c2) == c3 == {k: v[0] for k, v in c4.items()}
print("idioms agree:", dict(c1))

# Trap 1: Counter arithmetic drops non-positive counts (the prompt's example)
r = Counter('aab') - Counter('abbb')
print("1) Counter('aab') - Counter('abbb') ->", r)
assert r == Counter({'a': 1})
s = Counter('aab')
s.subtract(Counter('abbb'))
print("   .subtract keeps negatives         ->", s)
assert s == {'a': 1, 'b': -2}
print("   unary + strips them               ->", +s, "| total() =", s.total())
print("   '+' also drops: Counter(a=1) + Counter(a=-3) ->", Counter(a=1) + Counter(a=-3))

# Trap 2: defaultdict inserts on a READ; Counter and plain dict do not
dd = defaultdict(int)
_ = dd['ghost']
print("2) defaultdict read inserts a key:", dict(dd), "| 'ghost' in dd:", 'ghost' in dd)
assert 'ghost' in dd
cc = Counter()
_ = cc['ghost']
print("   Counter read returns 0, no insert:", dict(cc))
assert 'ghost' not in cc
dd2 = defaultdict(int)
print("   `in` on a defaultdict never inserts:", 'x' in dd2, dict(dd2))
assert 'x' not in dd2 and dd2.get('x') is None and 'x' not in dd2   # .get also safe

# Trap 3: most_common ties follow first-insertion order (sort is stable), not key order
t = Counter('zzyyxx')
print("3) Counter('zzyyxx').most_common():", t.most_common())
assert t.most_common() == [('z', 2), ('y', 2), ('x', 2)]
print("   explicit tie-break by key        :", sorted(t.items(), key=lambda kv: (-kv[1], kv[0])))

# Trap 4: shared mutable defaults
bad = dict.fromkeys('ab', [])
bad['a'].append(1)
print("4) dict.fromkeys('ab', []) shares ONE list:", bad)
assert bad['b'] == [1]
grid = [[0]] * 3
grid[0][0] = 9
print("   [[0]] * 3 aliases rows:", grid)
assert grid == [[9], [9], [9]]
good = defaultdict(list)
good['a'].append(1)
print("   defaultdict(list) makes a fresh list per key:", dict(good), "| 'b' separate:", good['b'], dict(good))
shared = []
oops = defaultdict(lambda: shared)
oops['a'].append(1)
print("   factory returning one shared object is the same bug:", oops['b'])
assert oops['b'] == [1]

# Trap 5: defaultdict default_factory is only used by __getitem__
dd3 = defaultdict(list)
print("5) .get on missing key ->", dd3.get('k'), "| dd3['k'] ->", dd3['k'], "| now:", dict(dd3))

# Trap 6: Counter.update adds, dict.update replaces
x = Counter(a=2)
x.update({'a': 3})
y = dict(a=2)
y.update({'a': 3})
print("6) Counter.update adds:", dict(x), "| dict.update replaces:", y)
assert x['a'] == 5 and y['a'] == 3

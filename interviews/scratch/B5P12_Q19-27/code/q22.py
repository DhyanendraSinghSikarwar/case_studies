import itertools, random

random.seed(22)

def partition_slice(s):
    """Recurse over the cut position; test each piece with t == t[::-1]. Returns (result, calls, piece_tests, char_compares_upper_bound)."""
    out = []; cur = []; st = {'calls': 0, 'tests': 0}
    def go(i):
        st['calls'] += 1
        if i == len(s):
            out.append(cur[:]); return
        for j in range(i + 1, len(s) + 1):
            t = s[i:j]; st['tests'] += 1
            if t == t[::-1]:
                cur.append(t); go(j); cur.pop()
    go(0)
    return out, st['calls'], st['tests']

def partition_table(s):
    """Same recursion, but each piece test is a lookup in is_pal[i][j] (inclusive ends), built once in O(n^2)."""
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            is_pal[i][j] = s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1])
    out = []; cur = []; st = {'calls': 0, 'tests': 0}
    def go(i):
        st['calls'] += 1
        if i == n:
            out.append(cur[:]); return
        for j in range(i, n):
            st['tests'] += 1
            if is_pal[i][j]:
                cur.append(s[i:j + 1]); go(j + 1); cur.pop()
    go(0)
    return out, st['calls'], st['tests']

def solve(s): return sorted(partition_table(s)[0])

def brute(s):
    n = len(s); out = []
    for mask in range(1 << (n - 1)):                       # bit i set = cut after position i
        cuts = [i + 1 for i in range(n - 1) if mask >> i & 1]; ed = [0] + cuts + [n]
        parts = [s[ed[i]:ed[i + 1]] for i in range(len(ed) - 1)]
        if all(p == p[::-1] for p in parts): out.append(parts)
    return sorted(out)

for s, exp in [('abba', [['a', 'b', 'b', 'a'], ['a', 'bb', 'a'], ['abba']]), ('xyz', [['x', 'y', 'z']]),
               ('aaa', [['a', 'a', 'a'], ['a', 'aa'], ['aa', 'a'], ['aaa']]), ('a', [['a']])]:
    got = solve(s)
    assert got == exp == brute(s) == sorted(partition_slice(s)[0])
    print('example', repr(s), '->', got)

def tree(s):
    cur = []
    def go(i, d):
        if i == len(s): print('  ' * d + '-> partition', cur); return
        for j in range(i + 1, len(s) + 1):
            t = s[i:j]
            if t == t[::-1]:
                cur.append(t); print('  ' * d + f'cut piece {t!r} -> {cur}'); go(j, d + 1); cur.pop()
            else: print('  ' * d + f'piece {t!r} is not a palindrome: pruned')
    go(0, 0)
print("decision tree for 'abba':"); tree('abba')

# node counts: palindrome-pruned search vs trying every cut set (2^(n-1) leaves, each with n-1 cut bits)
print('calls / piece tests for the recursion (slice test vs table), and the unpruned number of cut sets 2^(n-1):')
for s in ['abba', 'aaaaaaaa', 'abcdefgh', 'abababab', 'a' * 16, 'abcdefghijklmnop']:
    r1, c1, t1 = partition_slice(s); r2, c2, t2 = partition_table(s)
    assert r1 == r2 and r1 == sorted(r1)
    print(f'  {s:18s} partitions={len(r1):6d} calls={c1:6d} piece tests={t1:7d} (table: {t2}) unpruned cut sets={2 ** (len(s) - 1)}')

# claim: all-equal letters give 2^(n-1) partitions (n <= 12 exhaustive), so listing stays exponential even with the table
for n in range(1, 13): assert len(solve('a' * n)) == 2 ** (n - 1)
print('a^n has exactly 2^(n-1) partitions for n = 1..12; a^16 ->', len(solve('a' * 16)))

# the table builds in O(n^2) and the recursion does a bounded number of table lookups per call (n at most)
# seeded random cross-check vs all 2^(n-1) cut sets
for _ in range(300):
    n = random.randint(1, 12); s = ''.join(random.choice('ab') if random.random() < .8 else random.choice('abc') for _ in range(n))
    assert solve(s) == brute(s), s
    assert partition_slice(s)[0] == sorted(partition_slice(s)[0]) == solve(s)
print('300 seeded random strings (length 1..12) agree; both versions return the list already sorted')

# edge asserts
assert solve('a') == [['a']] and solve('ab') == [['a', 'b']] and solve('aa') == [['a', 'a'], ['aa']]
assert len(solve('abcdefghijklmnop')) == 1
print('edge asserts passed; depth <= 16, recursion limit 1000 is no issue')

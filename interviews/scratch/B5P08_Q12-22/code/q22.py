import itertools
import random

random.seed(22)

def partition_labels(s):
    last = {ch: i for i, ch in enumerate(s)}   # last index of each letter
    sizes = []
    start = end = 0                            # current part is s[start..], end = farthest last index so far
    for i, ch in enumerate(s):
        end = max(end, last[ch])               # the part must reach the last copy of every letter seen
        if i == end:                           # nothing in the part needs anything further: cut here
            sizes.append(end - start + 1)
            start = i + 1
    return sizes

def valid_cuts(s, cuts):                       # parts: cut positions strictly inside 1..n-1
    n = len(s)
    parts = [s[a:b] for a, b in zip([0] + list(cuts), list(cuts) + [n])]
    seen = set()
    for p in parts:
        letters = set(p)
        if letters & seen:
            return None
        seen |= letters
    return parts

def brute_all(s):                              # every valid partition, as a list of part-length lists
    n = len(s)
    out = []
    for r in range(n):
        for cuts in itertools.combinations(range(1, n), r):
            parts = valid_cuts(s, cuts)
            if parts is not None:
                out.append([len(p) for p in parts])
    return out

def brute_best(s):
    allp = brute_all(s)
    m = max(len(p) for p in allp)
    best = [p for p in allp if len(p) == m]
    return best

for s, exp in [('ababcbacadefegdehijhklij', [9, 7, 8]), ('eccbbbbdec', [10]), ('a', [1]), ('abc', [1, 1, 1])]:
    assert partition_labels(s) == exp
    if len(s) <= 12:
        assert brute_best(s) == [exp]
    print(repr(s), '->', partition_labels(s))

# exhaustive: all strings over 'abc' of length 1..8 (9840 strings): the finest partition is UNIQUE and equals the greedy
cnt = 0
for n in range(1, 9):
    for t in itertools.product('abc', repeat=n):
        s = ''.join(t)
        best = brute_best(s)
        assert len(best) == 1, (s, best)                  # uniqueness claim from the prompt
        assert best[0] == partition_labels(s), s
        assert sum(best[0]) == n
        cnt += 1
print('exhaustive ok:', cnt, 'strings over abc; finest partition unique every time')

# also 4 letters, length up to 7
cnt = 0
for n in range(1, 8):
    for t in itertools.product('abcd', repeat=n):
        s = ''.join(t)
        assert brute_best(s) == [partition_labels(s)], s
        cnt += 1
print('exhaustive ok:', cnt, 'strings over abcd (length <= 7)')

for _ in range(300):
    s = ''.join(random.choice('abcdefghij') for _ in range(random.randint(1, 500)))
    sizes = partition_labels(s)
    assert sum(sizes) == len(s)
    pos = 0
    seen = set()
    for z in sizes:                                         # each letter appears in exactly one part
        part = set(s[pos:pos + z])
        assert not (part & seen)
        seen |= part
        pos += z
print('random ok: 300 strings up to length 500')

# greedy meaning: every cut is made at the EARLIEST legal index; moving any cut later only merges parts
s = 'ababcbacadefegdehijhklij'
cuts = list(itertools.accumulate(partition_labels(s)))[:-1]
print('cut positions for the long example:', cuts)

# edge cases
assert partition_labels('aaaa') == [4]
assert partition_labels('abab') == [4]
assert partition_labels('abcabc') == [6]
assert partition_labels('aabbcc') == [2, 2, 2]
assert partition_labels('abcdefghijklmnopqrstuvwxyz' * 1) == [1] * 26
assert partition_labels('a' + 'b' * 498 + 'a') == [500]
print('edge cases ok')

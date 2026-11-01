import heapq
import itertools
import random
from collections import Counter

random.seed(15)

def reorganize(s):
    cnt = Counter(s)
    if max(cnt.values()) > (len(s) + 1) // 2:         # closed feasibility test
        return ''
    heap = [(-c, ch) for ch, c in cnt.items()]         # (negated count, letter): ties on count compare letters
    heapq.heapify(heap)
    out = []
    held = None                                        # last letter used, held back one step
    while heap or held:
        if not heap:                                   # cannot happen when feasible
            return ''
        neg, ch = heapq.heappop(heap)
        out.append(ch)
        neg += 1                                       # one copy used (counts are negative)
        if held:
            heapq.heappush(heap, held)                 # the letter held last step may be used again
            held = None
        if neg:
            held = (neg, ch)
    return ''.join(out)

def reorganize_heap_only(s):                           # same heap logic, without the closed test
    cnt = Counter(s)
    heap = [(-c, ch) for ch, c in cnt.items()]
    heapq.heapify(heap)
    out, held = [], None
    while heap:
        neg, ch = heapq.heappop(heap)
        out.append(ch)
        neg += 1
        if held:
            heapq.heappush(heap, held)
            held = None
        if neg:
            held = (neg, ch)
    return ''.join(out) if len(out) == len(s) else ''

def valid(s, got):
    """Own checker: any permutation of s with no equal neighbours; '' exactly when none exists."""
    if got == '':
        return not exists_arrangement(s)
    return sorted(got) == sorted(s) and all(a != b for a, b in zip(got, got[1:]))

def exists_arrangement(s):                             # brute force over distinct permutations (small s)
    return any(all(a != b for a, b in zip(p, p[1:])) for p in set(itertools.permutations(s)))

for s, accepted in [('aab', 'aba'), ('aaab', ''), ('vvvlo', None), ('a', 'a'), ('aabbcc', None)]:
    got = reorganize(s)
    assert valid(s, got), (s, got)
    if accepted is not None and accepted in ('', 'aba', 'a'):
        assert got == accepted
    print(repr(s), '->', repr(got))

# exhaustive: all strings over 'abc' of length 1..7 (3+9+...+2187 = 3279 strings), brute-force feasibility
checked = infeasible = 0
for n in range(1, 8):
    for t in itertools.product('abc', repeat=n):
        s = ''.join(t)
        got = reorganize(s)
        feasible = max(Counter(s).values()) <= (n + 1) // 2
        assert feasible == exists_arrangement(s), s     # the closed condition is exact
        assert (got != '') == feasible and valid(s, got), (s, got)
        assert reorganize_heap_only(s) == got           # the heap alone already finds it whenever feasible
        checked += 1
        infeasible += not feasible
print('exhaustive ok:', checked, 'strings; infeasible:', infeasible)

for _ in range(300):
    s = ''.join(random.choice('abcdefg') for _ in range(random.randint(1, 200)))
    got = reorganize(s)
    assert valid(s, got) if got else max(Counter(s).values()) > (len(s) + 1) // 2
print('random ok: 300 strings up to length 200')

# heapq tie-breaking: tuples compare element by element
h = [(-2, 'b'), (-2, 'a'), (-1, 'z')]
heapq.heapify(h)
print('ties on count break by letter:', heapq.heappop(h))       # (-2, 'a')
# a tuple whose second item cannot be ordered raises TypeError as soon as the counts tie
try:
    bad = []
    heapq.heappush(bad, (-2, {'x': 1}))
    heapq.heappush(bad, (-2, {'y': 2}))
    print('no error (unexpected)')
except TypeError as e:
    print('TypeError on tied count with dict payload:', e)
heapq.heappush(bad, (-3, {'z': 3}))                              # different counts never reach the payload
print('heap of 3 after a distinct count:', len(bad))

# edge cases
assert reorganize('a') == 'a'
assert reorganize('aa') == ''
assert reorganize('ab') in ('ab', 'ba')
assert reorganize('aaabb') == 'ababa'
assert reorganize('a' * 250 + 'b' * 250) != '' and valid('a' * 250 + 'b' * 250, reorganize('a' * 250 + 'b' * 250))
assert reorganize('a' * 251 + 'b' * 249) == ''
print('edge cases ok')

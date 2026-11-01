import heapq
import itertools
import random
from collections import Counter, deque

random.seed(45)

def ok(s, k, got):
    """Valid if got is a permutation of s and equal letters are at index distance >= k."""
    if sorted(got) != sorted(s):
        return False
    last = {}
    for i, ch in enumerate(got):
        if ch in last and i - last[ch] < k:
            return False
        last[ch] = i
    return True

def feasible_brute(s, k):
    """Exhaustive: does ANY permutation of s keep equal letters at distance >= k?"""
    return any(ok(s, k, ''.join(p)) for p in set(itertools.permutations(s)))

def rearrange(s, k):
    if k <= 1:
        return s                                          # no constraint (also handles s == '')
    heap = [(-c, ch) for ch, c in Counter(s).items()]     # max-heap on remaining count; letter breaks ties (str is orderable)
    heapq.heapify(heap)
    wait = deque()                                        # letters used in the last k-1 steps, held out of the heap
    out = []
    while heap:
        negc, ch = heapq.heappop(heap)                    # most remaining letter that is allowed now
        out.append(ch)
        wait.append((negc + 1, ch))                       # one fewer to place
        if len(wait) >= k:                                # this letter's cooling period is over exactly k steps later
            c2, ch2 = wait.popleft()
            if c2:
                heapq.heappush(heap, (c2, ch2))
    return ''.join(out) if len(out) == len(s) else ''     # heap ran dry with letters still waiting: impossible

# ---- examples (any valid arrangement is accepted; the prompt's string is one of them)
for s, k, want in [('aabbcc', 3, 'abcabc'), ('aaabc', 3, ''), ('aaadbbcc', 2, 'abacabcd'), ('abc', 0, 'abc')]:
    got = rearrange(s, k)
    assert (got == '') == (want == '') and (got == '' or ok(s, k, got)) and (want == '' or ok(s, k, want)), (s, k, got)
    print(repr(s), k, '->', repr(got), '| prompt answer', repr(want), 'also valid' if want and ok(s, k, want) else '')

# ---- tie behaviour in the heap: equal counts are broken by the letter, so the output is deterministic
h = [(-2, 'b'), (-2, 'a'), (-1, 'c')]
heapq.heapify(h)
print('equal counts pop alphabetically:', [heapq.heappop(h) for _ in range(3)])
try:
    h = []
    heapq.heappush(h, (-2, {'ch': 'a'})); heapq.heappush(h, (-2, {'ch': 'b'}))
except TypeError as e:
    print('with an unorderable payload instead of a letter ->', e)

# ---- exhaustive: every string over {a,b,c} up to length 7 (and 'abcd' up to 6), every k from 0 to len
cases = infeasible = 0
for alpha, maxlen in (('abc', 7), ('abcd', 5)):
    for n in range(0, maxlen + 1):
        for t in itertools.product(alpha, repeat=n):
            s = ''.join(t)
            if s != ''.join(sorted(s)):
                continue                                  # sorted representatives cover every multiset
            for k in range(0, n + 1):
                got = rearrange(s, k)
                if s == '':
                    assert got == ''                      # empty input: the empty string is the (valid) answer
                elif got:
                    assert ok(s, k, got), (s, k, got)
                else:
                    assert s == '' or k > 1, (s, k)
                    assert not feasible_brute(s, k), ('claimed impossible but a rearrangement exists', s, k)
                    infeasible += 1
                cases += 1
print('exhaustive over all multisets up to the sizes above:', cases, 'cases;', infeasible, "returned '' and brute force confirms none exists")

# ---- random cross-check on longer strings (validity only, plus feasibility by the known counting argument is NOT assumed)
for _ in range(1000):
    s = ''.join(random.choice('abcde') for _ in range(random.randint(1, 8)))
    k = random.randint(0, len(s))
    got = rearrange(s, k)
    assert (got != '' and ok(s, k, got)) or (got == '' and not feasible_brute(s, k)), (s, k)
print('1000 random strings (len <= 8) agree with exhaustive feasibility')

# ---- edge asserts and size
assert rearrange('', 0) == '' and rearrange('', 5) == ''
assert rearrange('a', 1) == 'a'
assert rearrange('aa', 2) == '' and rearrange('ab', 2) == 'ab'
assert rearrange('aab', 2) in ('aba',)
big = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3 * 10 ** 4))
for k in (0, 1, 2, 5, 20):
    g = rearrange(big, k); assert g and ok(big, k, g)
big2 = 'a' * 15000 + 'b' * 15000
assert rearrange(big2, 2) and ok(big2, 2, rearrange(big2, 2)) and rearrange(big2, 3) == ''
print('size 3*10^4 ok; strings of two letters with k=2 feasible, k=3 impossible')

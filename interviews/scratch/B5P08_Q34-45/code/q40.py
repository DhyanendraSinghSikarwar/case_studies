import heapq
import random
from fractions import Fraction
from functools import lru_cache

random.seed(40)

def huffman_lengths(freqs):
    """Merge the two smallest repeatedly. Nodes 0..n-1 are leaves, n.. are merged nodes. parent[] gives depths with no recursion."""
    n = len(freqs)
    if n == 1:
        return [0]
    parent = [-1] * (2 * n - 1)
    heap = [(f, i) for i, f in enumerate(freqs)]      # (frequency, node id): ids are unique, so ties never reach anything else
    heapq.heapify(heap)
    nxt = n
    while len(heap) > 1:
        f1, a = heapq.heappop(heap)
        f2, b = heapq.heappop(heap)
        parent[a] = parent[b] = nxt
        heapq.heappush(heap, (f1 + f2, nxt))
        nxt += 1
    depth = [0] * (2 * n - 1)                          # root is nxt - 1; parents always have bigger ids than children
    for v in range(2 * n - 3, -1, -1):
        depth[v] = depth[parent[v]] + 1
    return depth[:n]

def cost_of(freqs, lengths):
    return sum(f * l for f, l in zip(freqs, lengths))

def optimal_cost_brute(freqs):
    """Exhaustive over all full binary trees on the symbols: best split of every subset into two non-empty parts."""
    n = len(freqs)
    tot = [0] * (1 << n)
    for m in range(1, 1 << n):
        tot[m] = sum(freqs[i] for i in range(n) if m >> i & 1)
    @lru_cache(None)
    def best(m):
        if m & (m - 1) == 0:
            return 0                                   # one symbol: no more bits
        res, sub = float('inf'), (m - 1) & m
        while sub:
            res = min(res, best(sub) + best(m ^ sub) + tot[m])   # every bit of the merge adds the subtree weight once
            sub = (sub - 1) & m
        return res
    return best((1 << n) - 1)

def valid_code(freqs, lengths):
    """Accepted if the lengths form a full prefix tree (Kraft sum exactly 1; a single symbol uses [0]) with the optimal cost."""
    if len(lengths) != len(freqs):
        return False
    if len(freqs) == 1:
        return lengths == [0]
    return sum(Fraction(1, 2 ** l) for l in lengths) == 1 and cost_of(freqs, lengths) == optimal_cost_brute(freqs)

# ---- examples
for fr, want in [([5, 9, 12, 13, 16, 45], [4, 4, 3, 3, 3, 1]), ([1, 1, 1, 1], [2, 2, 2, 2]), ([7], [0]),
                 ([1, 2], [1, 1]), ([3, 3, 3, 3, 3], [3, 3, 2, 2, 2])]:
    got = huffman_lengths(fr)
    assert valid_code(fr, got) and valid_code(fr, want), (fr, got, want)
    print(fr, '->', got, 'cost', cost_of(fr, got), '| prompt answer cost', cost_of(fr, want))

# ---- the lengths are not unique, only the cost is: any permutation of the lengths among tied symbols is also optimal
fr = [3, 3, 3, 3, 3]
print('tied frequencies', fr, ': [3,3,2,2,2] valid:', valid_code(fr, [3, 3, 2, 2, 2]), '| [2,2,2,3,3] valid:', valid_code(fr, [2, 2, 2, 3, 3]),
      '| [2,2,2,2,2] valid:', valid_code(fr, [2, 2, 2, 2, 2]), '(Kraft sum 5/4, not a prefix code)')

# ---- the tie-breaker matters for the heap, not for the optimal cost
class Node:
    def __init__(self, f): self.f = f
h = []
heapq.heappush(h, (2, Node(2)))
try:
    heapq.heappush(h, (2, Node(2)))
except TypeError as e:
    print('heap of (freq, Node) with tied freq ->', e)
print('so each node carries a unique id as the second tuple item')

# ---- random cross-check against the exhaustive optimum (n <= 7), including all-equal and tiny frequencies
for _ in range(600):
    fr = [random.randint(1, 9) for _ in range(random.randint(1, 7))]
    assert valid_code(fr, huffman_lengths(fr)), fr
print('600 random frequency lists: Kraft sum == 1 and cost == exhaustive optimum')

# ---- same number as "minimum cost to connect sticks" (Part 8 Q20): the merge costs add up to the weighted path length
def sticks_cost(sticks):
    h = list(sticks); heapq.heapify(h); tot = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h); tot += a + b; heapq.heappush(h, a + b)
    return tot
for _ in range(500):
    fr = [random.randint(1, 20) for _ in range(random.randint(1, 12))]
    assert sticks_cost(fr) == cost_of(fr, huffman_lengths(fr)), fr
print('Huffman weighted length == sticks merge cost on 500 random lists')

# ---- edge and size
assert huffman_lengths([7]) == [0]
assert huffman_lengths([1, 2]) == [1, 1]
fib = [1, 1]
for _ in range(30): fib.append(fib[-1] + fib[-2])
fl = huffman_lengths(fib)
assert max(fl) == len(fib) - 1 and sum(Fraction(1, 2 ** l) for l in fl) == 1       # skewed: depth n-1, still no recursion
n = 10 ** 5
big = [random.randint(1, 10 ** 6) for _ in range(n)]
bl = huffman_lengths(big)
assert len(bl) == n and sum(Fraction(1, 2 ** l) for l in bl) == 1
print('n=10^5: max code length', max(bl), '; Fibonacci frequencies give depth', max(fl), '= n - 1 for n =', len(fib))

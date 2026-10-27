import heapq
import random
from collections import Counter

random.seed(8)

def top_k_heap(words, k):
    c = Counter(words)
    h = [(-n, w) for w, n in c.items()]                 # smaller tuple = better: bigger count, then smaller word
    heapq.heapify(h)                                    # O(d), d = distinct words
    return [heapq.heappop(h)[1] for _ in range(k)]      # k pops, O(k log d)

class Worse:
    """Wrapper so a min-heap of size k keeps the k best: its root is the WORST kept word."""
    __slots__ = ('n', 'w')
    def __init__(self, n, w): self.n, self.w = n, w
    def __lt__(self, other):                            # self is "smaller" (worse) if fewer count, or same count and later word
        return (self.n, other.w) < (other.n, self.w)

def top_k_heap_k(words, k):
    h = []
    for w, n in Counter(words).items():
        item = Worse(n, w)
        if len(h) < k: heapq.heappush(h, item)
        elif h[0] < item: heapq.heapreplace(h, item)    # item beats the worst kept word
    out = [heapq.heappop(h) for _ in range(len(h))]     # worst first
    return [x.w for x in reversed(out)]                 # O(d log k) overall

def top_k_sort(words, k):
    c = Counter(words)
    return sorted(c, key=lambda w: (-c[w], w))[:k]      # the oracle: O(d log d)

for fn in (top_k_heap, top_k_heap_k, top_k_sort):
    assert fn(['i', 'love', 'leetcode', 'i', 'love', 'coding'], 2) == ['i', 'love']
    assert fn(['the', 'day', 'is', 'sunny', 'the', 'the', 'the', 'sunny', 'is', 'is'], 4) == ['the', 'is', 'sunny', 'day']
    assert fn(['a', 'b', 'c'], 3) == ['a', 'b', 'c']
    assert fn(['z'], 1) == ['z']

for _ in range(3000):
    words = [random.choice('abcdef') + random.choice(['', 'x', 'y']) for _ in range(random.randint(1, 25))]
    d = len(set(words)); k = random.randint(1, d)
    want = top_k_sort(words, k)
    assert top_k_heap(words, k) == want == top_k_heap_k(words, k), (words, k)
print('3000 random cases ok')

# what goes wrong without the trick
words = ['b', 'a', 'c', 'a', 'b', 'c']                  # all three tie with count 2
print('Counter.most_common (ties keep first-seen order):', [w for w, _ in Counter(words).most_common(3)])
print('heapq.nlargest on (count, word) (ties give LARGER word first):', [w for n, w in heapq.nlargest(3, [(n, w) for w, n in Counter(words).items()])])
print('heap of (-count, word) (what the question wants):', top_k_heap(words, 3))

# the word part is only compared on a count tie; if the payload is unorderable a tie raises TypeError
h = []
heapq.heappush(h, (-2, {'w': 'x'}))
try:
    heapq.heappush(h, (-2, {'w': 'y'}))
except TypeError as e:
    print('TypeError on tied count with dict payload:', e)
# negating the string instead of the count does not work
try:
    heapq.heappush([], (-'abc', 1))
except TypeError as e:
    print('cannot negate a str (so negate the count, not the word):', e)

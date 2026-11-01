import functools, heapq, random

class Rev:                                       # pops the LARGEST string first
    __slots__ = ('w',)
    def __init__(self, w): self.w = w
    def __lt__(self, other): return self.w > other.w          # reversed on purpose

class LenRev:                                    # longer first, then larger string first
    __slots__ = ('w',)
    def __init__(self, w): self.w = w
    def __lt__(self, other): return (len(self.w), self.w) > (len(other.w), other.w)

def pop_order(words, order):
    cls = Rev if order == 'lex_desc' else LenRev
    h = [cls(w) for w in words]
    heapq.heapify(h)
    return [heapq.heappop(h).w for _ in range(len(words))]

def brute(words, order):
    if order == 'lex_desc': return sorted(words, reverse=True)
    return sorted(words, key=lambda w: (len(w), w), reverse=True)

assert pop_order(['pear','apple','fig','apple','kiwi'], 'lex_desc') == ['pear','kiwi','fig','apple','apple']
assert pop_order(['pear','apple','fig','kiwi','plum','date'], 'len_desc_lex_desc') == ['apple','plum','pear','kiwi','date','fig']
assert pop_order([], 'lex_desc') == []

rng = random.Random(30)
for _ in range(1500):
    ws = [''.join(rng.choice('abc') for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(0, 12))]
    for o in ('lex_desc', 'len_desc_lex_desc'):
        assert pop_order(ws, o) == brute(ws, o), (ws, o)
print("1500 random cases x 2 orders match sorted()")

# heapq only ever uses <, so total_ordering adds nothing here
@functools.total_ordering
class RevTO:
    def __init__(self, w): self.w = w
    def __eq__(self, o): return self.w == o.w
    def __lt__(self, o): return self.w > o.w
print("total_ordering gives >, <=, >= for free:", RevTO('a') >= RevTO('b'), "(not needed by heapq)")

# tuple key (-len(w), w): longest first, then ASCENDING alphabetical, not descending
ws = ['pear', 'plum', 'date', 'fig', 'kiwi']
h = []
for w in ws: heapq.heappush(h, (-len(w), w))
print("(-len, w) pops:", [heapq.heappop(h)[1] for _ in ws], "| wanted:", brute(ws, 'len_desc_lex_desc'))
print("strings have no unary minus:", end=" ")
try: -'abc'
except TypeError as e: print(e)

# A tuple-of-negated-code-points trick DOES work for descending alphabetical, but only with a sentinel
def neg_key(w): return tuple(-ord(c) for c in w) + (1,)       # sentinel makes a longer word with the same prefix come first
def neg_key_no_sentinel(w): return tuple(-ord(c) for c in w)
ws = ['ab', 'abc', 'b', 'ba']
print("with sentinel   :", sorted(ws, key=neg_key), "| expected", sorted(ws, reverse=True))
print("without sentinel:", sorted(ws, key=neg_key_no_sentinel), "(prefix 'ab' wrongly before 'abc')")
for _ in range(1000):
    ws = [''.join(rng.choice('abc') for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(0, 10))]
    assert sorted(ws, key=neg_key) == sorted(ws, reverse=True)
print("sentinel trick verified on 1000 random lists")

# Wrapper that carries a payload: tie on the key is harmless because only the key is compared
class Item:
    __slots__ = ('w', 'payload')
    def __init__(self, w, payload): self.w, self.payload = w, payload
    def __lt__(self, o): return self.w > o.w
h = [Item('a', {'id': 1}), Item('a', {'id': 2})]
heapq.heapify(h)
print("dict payload with tied keys, no TypeError:", heapq.heappop(h).payload)

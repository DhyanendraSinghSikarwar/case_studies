import heapq, random
from collections import Counter

class LazyMinPQ:
    def __init__(self):
        self.h = []                  # may hold stale (already removed) values
        self.live = Counter()        # live occurrences per value
        self.dead = Counter()        # pending deletions per value (stale copies still inside the heap)
        self.n = 0                   # live count
        self.pushes = 0

    def push(self, x):
        heapq.heappush(self.h, x); self.live[x] += 1; self.n += 1; self.pushes += 1

    def remove(self, x):
        if self.live[x] > 0:         # only if a live copy exists
            self.live[x] -= 1; self.dead[x] += 1; self.n -= 1
            return True
        return False

    def _clean(self):                # drop stale entries that reached the top (each at most once)
        while self.h and self.dead[self.h[0]] > 0:
            self.dead[self.h[0]] -= 1
            heapq.heappop(self.h)

    def top(self):
        self._clean()
        return self.h[0] if self.h else None

    def pop(self):
        self._clean()
        if not self.h: return None
        x = heapq.heappop(self.h); self.live[x] -= 1; self.n -= 1
        return x

    def size(self): return self.n

def run(ops):
    pq, out = LazyMinPQ(), []
    for op in ops:
        if op[0] == 'push': pq.push(op[1])
        elif op[0] == 'remove': out.append(pq.remove(op[1]))
        elif op[0] == 'pop': out.append(pq.pop())
        elif op[0] == 'top': out.append(pq.top())
        else: out.append(pq.size())
        assert len(pq.h) <= pq.pushes                 # never more entries than pushes
    return out

def brute(ops):                                       # plain list, O(n) per operation
    a, out = [], []
    for op in ops:
        if op[0] == 'push': a.append(op[1])
        elif op[0] == 'remove':
            if op[1] in a: a.remove(op[1]); out.append(True)
            else: out.append(False)
        elif op[0] == 'pop':
            if a: m = min(a); a.remove(m); out.append(m)
            else: out.append(None)
        elif op[0] == 'top': out.append(min(a) if a else None)
        else: out.append(len(a))
    return out

assert run([['push',3],['push',1],['push',2],['remove',1],['top'],['pop'],['size'],['remove',9]]) == [True,2,2,1,False]
assert run([['push',5],['push',5],['remove',5],['pop'],['pop'],['top']]) == [True,5,None,None]
assert run([['pop'],['size']]) == [None, 0]
assert run([]) == []

rng = random.Random(31)
for _ in range(2000):
    ops = []
    for _ in range(rng.randint(0, 30)):
        r = rng.random()
        if r < .4: ops.append(['push', rng.randint(0, 5)])
        elif r < .6: ops.append(['remove', rng.randint(0, 5)])
        elif r < .75: ops.append(['pop'])
        elif r < .9: ops.append(['top'])
        else: ops.append(['size'])
    assert run(ops) == brute(ops), ops
print("2000 random op sequences match the list brute force")

# stale entries are popped at most once each: count heappop calls on a big run
big = LazyMinPQ()
n = 100000
for i in range(n): big.push(i % 1000)
for i in range(n // 2): big.remove((i * 7) % 1000)
total_pops = 0
while big.top() is not None:
    big.pop(); total_pops += 1
print("n=100000 pushes, 50000 removes ->", total_pops, "live pops; heap list ended at", len(big.h), "entries")

# why not remove-from-the-middle: heap.remove(x) is O(n) and heapify is O(n) again
h = [1, 5, 2, 9, 7]; heapq.heapify(h)
h.remove(5); heapq.heapify(h)
print("list.remove + heapify works but costs O(n) per remove:", h)

import heapq, itertools, random

def serve(tasks):
    h, counter = [], itertools.count()           # strictly increasing: never ties, never reaches payload
    for p, payload in tasks:
        heapq.heappush(h, (p, next(counter), payload))
    return [heapq.heappop(h)[2]['id'] for _ in range(len(h))]

def brute(tasks):                                # sorted is stable, so equal priorities keep arrival order
    return [t[1]['id'] for t in sorted(tasks, key=lambda t: t[0])]

assert serve([[2,{'id':'a'}],[1,{'id':'b'}],[2,{'id':'c'}],[1,{'id':'d'}],[3,{'id':'e'}]]) == ['b','d','a','c','e']
assert serve([[5,{'id':'x'}],[5,{'id':'y'}],[5,{'id':'z'}]]) == ['x','y','z']
assert serve([]) == []

# 1) (priority, payload): TypeError only when priorities tie
h = []
heapq.heappush(h, (1, {'id': 'a'}))
heapq.heappush(h, (2, {'id': 'b'}))              # fine: 1 < 2 decides, dicts never compared
try:
    heapq.heappush(h, (1, {'id': 'c'}))          # tie on 1 -> falls through to dict < dict
except TypeError as e:
    print("TypeError:", e)

# 2) (priority, id): no error, but ties are served by id, not by arrival
tasks = [[1, {'id': 'z'}], [1, {'id': 'a'}], [1, {'id': 'm'}]]
h = []
for p, d in tasks: heapq.heappush(h, (p, d['id']))
print("tuple (p, id) serves:", [heapq.heappop(h)[1] for _ in range(3)], "| FIFO wanted:", brute(tasks))

# 3) (priority, counter, payload): FIFO among ties
print("counter serves:     ", serve(tasks))

# randomised cross-check against stable sort
rng = random.Random(29)
for _ in range(1000):
    ts = [[rng.randint(0, 4), {'id': rng.choice('abcdefgh') + str(i)}] for i in range(rng.randint(0, 12))]
    assert serve(ts) == brute(ts)
print("1000 random cases match the stable sort")

# What the counter buys: the heap is ONLINE. Interleave pushes and pops, a one-off sort cannot.
h, c, order = [], itertools.count(), []
for p, name in [(2, 'a'), (2, 'b')]: heapq.heappush(h, (p, next(c), {'id': name}))
order.append(heapq.heappop(h)[2]['id'])          # a
for p, name in [(1, 'c'), (2, 'd')]: heapq.heappush(h, (p, next(c), {'id': name}))
order += [heapq.heappop(h)[2]['id'] for _ in range(3)]
print("interleaved push/pop order:", order)

# Same-object ties: if the payload objects ARE comparable the bug is silent. Integers never raise.
h = []
for p, v in [(1, 7), (1, 3)]: heapq.heappush(h, (p, v))
print("payload ints decide ties silently:", [heapq.heappop(h) for _ in range(2)])

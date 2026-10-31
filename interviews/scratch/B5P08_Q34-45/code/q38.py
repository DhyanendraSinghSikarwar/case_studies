import heapq
import random

random.seed(38)

def run_lazy(ops, check=False):
    heap = []          # entries (priority, stamp, task); stale ones are skipped when popped
    current = {}       # task -> (priority, stamp) of its live version
    stamp = pushes = 0
    out = []
    for op in ops:
        kind = op[0]
        if kind in ('add', 'update'):
            stamp += 1                                    # strictly increasing: unique, so the task is never compared
            current[op[1]] = (op[2], stamp)
            heapq.heappush(heap, (op[2], stamp, op[1]))
            pushes += 1
        elif kind == 'remove':
            out.append(current.pop(op[1], None) is not None)
        elif kind == 'pop':
            res = None
            while heap:
                pr, st, task = heapq.heappop(heap)
                if current.get(task) == (pr, st):         # still the live version?
                    del current[task]
                    res = task
                    break                                 # otherwise stale: drop and keep looking
            out.append(res)
        else:                                             # 'size'
            out.append(len(current))                      # live tasks, NOT len(heap)
        if check:
            assert len(heap) <= pushes
    return out

def run_brute(ops):
    cur, stamp, out = {}, 0, []
    for op in ops:
        if op[0] in ('add', 'update'):
            stamp += 1; cur[op[1]] = (op[2], stamp)
        elif op[0] == 'remove':
            out.append(cur.pop(op[1], None) is not None)
        elif op[0] == 'pop':
            if cur:
                t = min(cur, key=lambda x: cur[x]); del cur[t]; out.append(t)
            else:
                out.append(None)
        else:
            out.append(len(cur))
    return out

# ---- examples
ex = [
    ([['add', 'a', 5], ['add', 'b', 3], ['update', 'a', 1], ['pop'], ['size'], ['add', 'c', 3], ['update', 'b', 3],
      ['pop'], ['remove', 'z'], ['pop'], ['pop']], ['a', 1, 'c', False, 'b', None]),
    ([['pop'], ['add', 'x', 1], ['remove', 'x'], ['pop'], ['size']], [None, True, None, 0]),
]
for ops, want in ex:
    assert run_lazy(ops, check=True) == run_brute(ops) == want
    print(run_lazy(ops))

# ---- why the stamp: ties on priority must never compare the task objects
class Task:                      # unorderable payload
    def __init__(self, n): self.n = n
h = []
heapq.heappush(h, (1, Task('p')))
try:
    heapq.heappush(h, (1, Task('q')))
except TypeError as e:
    print('without a stamp, tied priority ->', e)
h = []
for i, name in enumerate('pqr'):
    heapq.heappush(h, (1, i, Task(name)))                  # (priority, stamp, task): ties resolved by stamp
print('with a stamp, equal priorities pop in insertion order:', [heapq.heappop(h)[2].n for _ in range(3)])

# ---- the heap never holds more entries than add/update calls; a hot update loop grows it though
heap_demo, cur, st = [], {}, 0
for i in range(1000):
    st += 1; cur['t'] = (i, st); heapq.heappush(heap_demo, (i, st, 't'))
print('1000 updates of ONE task: live size =', len(cur), ', physical heap entries =', len(heap_demo))

# ---- random cross-check
def rand_ops():
    ops = []
    for _ in range(random.randint(0, 25)):
        r = random.random(); t = random.choice('abcd')
        if r < 0.3: ops.append(['add', t, random.randint(0, 3)])
        elif r < 0.5: ops.append(['update', t, random.randint(0, 3)])
        elif r < 0.65: ops.append(['remove', t])
        elif r < 0.9: ops.append(['pop'])
        else: ops.append(['size'])
    return ops
for _ in range(3000):
    ops = rand_ops()
    assert run_lazy(ops, check=True) == run_brute(ops), ops
print('3000 random op sequences agree with the O(n)-per-pop brute force')

# ---- edge asserts
assert run_lazy([]) == []
assert run_lazy([['pop']]) == [None]
assert run_lazy([['add', 'a', 1], ['remove', 'a'], ['add', 'a', 1], ['pop']]) == [True, 'a']      # re-add after remove
assert run_lazy([['add', 'a', 1], ['add', 'b', 1], ['update', 'a', 1], ['pop'], ['pop']]) == ['b', 'a']  # update re-queues behind
assert run_lazy([['add', 'a', 1], ['remove', 'a'], ['remove', 'a']]) == [True, False]
n = 10 ** 5
ops = [['add', str(i % 500), random.randint(0, 1000)] for i in range(n // 2)] + [['pop']] * (n // 2)
res = run_lazy(ops, check=True)
assert len(res) == n // 2 and res.count(None) == n // 2 - 500
print('10^5 ops ok; pops answered:', n // 2, 'of which None:', res.count(None))

import heapq, random
random.seed(47)

class Scheduler:
    def __init__(self, clock):
        self.clock = clock
        self.heap = []                        # (ready, priority, seq, job_id)
        self.live = {}                        # job_id -> seq of the live submission
        self.seq = 0

    def submit(self, job_id, delay, priority):
        self.seq += 1
        self.live[job_id] = self.seq
        heapq.heappush(self.heap, (self.clock() + delay, priority, self.seq, job_id))

    def cancel(self, job_id):
        return self.live.pop(job_id, None) is not None     # lazy: the heap entry stays, poll skips it

    def poll(self, limit):
        now = self.clock(); out = []
        while self.heap and len(out) < limit and self.heap[0][0] <= now:
            ready, pr, seq, job_id = heapq.heappop(self.heap)
            if self.live.get(job_id) == seq:               # stale entries (cancelled / reused id) fail this test
                out.append(job_id); del self.live[job_id]
        return out

class Naive:
    def __init__(self, clock): self.clock = clock; self.jobs = []; self.seq = 0
    def submit(self, job_id, delay, priority):
        self.seq += 1; self.jobs.append((self.clock() + delay, priority, self.seq, job_id))
    def cancel(self, job_id):
        n = len(self.jobs); self.jobs = [j for j in self.jobs if j[3] != job_id]; return len(self.jobs) < n
    def poll(self, limit):
        now = self.clock(); ready = sorted(j for j in self.jobs if j[0] <= now)[:limit]
        for j in ready: self.jobs.remove(j)
        return [j[3] for j in ready]

class Clock:
    def __init__(self): self.t = 0
    def __call__(self): return self.t

def run(cls, ops):
    clk = Clock(); obj = cls(clk); out = []
    for t, m, a in ops:
        clk.t = t; out.append(getattr(obj, m)(*a))
    return out

ex = [[0, 'submit', ['a', 5, 2]], [0, 'submit', ['b', 5, 1]], [0, 'submit', ['c', 0, 9]], [0, 'poll', [5]], [4, 'poll', [5]],
      [5, 'cancel', ['b']], [5, 'poll', [1]], [5, 'submit', ['b', 0, 3]], [5, 'poll', [5]], [6, 'cancel', ['a']], [6, 'poll', [5]]]
got = run(Scheduler, ex)
assert got == [None, None, None, ['c'], [], True, ['a'], None, ['b'], False, []], got
print('example ->', got)

def gen_ops():                                # never submits an id that is still pending (checked with the naive model)
    clk = Clock(); probe = Naive(clk); pending = set(); ops = []; t = 0
    for _ in range(random.randint(0, 40)):
        t += random.randint(0, 3); clk.t = t; r = random.random()
        if r < .45:
            jid = 'j%d' % random.randint(1, 6)
            if jid in pending: continue
            a = [jid, random.randint(0, 5), random.randint(0, 3)]; probe.submit(*a); pending.add(jid); ops.append([t, 'submit', a])
        elif r < .7:
            a = ['j%d' % random.randint(1, 6)]
            if probe.cancel(*a): pending.discard(a[0])
            ops.append([t, 'cancel', a])
        else:
            a = [random.randint(1, 4)]
            for j in probe.poll(*a): pending.discard(j)
            ops.append([t, 'poll', a])
    return ops
for _ in range(500):
    ops = gen_ops()
    assert run(Scheduler, ops) == run(Naive, ops), ops
print('500 random sequences with an injected clock match the naive reference')

# ties: same ready time, then priority, then submission order; ready exactly at `now` is returned
tie = [[0, 'submit', ['x', 3, 1]], [0, 'submit', ['y', 3, 1]], [0, 'submit', ['z', 3, 0]], [3, 'poll', [10]]]
assert run(Scheduler, tie)[-1] == ['z', 'x', 'y']
assert run(Scheduler, [[0, 'poll', [3]], [0, 'cancel', ['q']], [0, 'submit', ['q', 1, 0]], [0, 'poll', [3]], [1, 'poll', [0]], [1, 'poll', [3]]]) == [[], False, None, [], [], ['q']]

# why seq, not just the id: cancel then resubmit the SAME id with a later ready time
class IdOnly(Scheduler):
    def poll(self, limit):
        now = self.clock(); out = []
        while self.heap and len(out) < limit and self.heap[0][0] <= now:
            ready, pr, seq, job_id = heapq.heappop(self.heap)
            if job_id in self.live: out.append(job_id); del self.live[job_id]
        return out
reuse = [[0, 'submit', ['a', 1, 0]], [0, 'cancel', ['a']], [0, 'submit', ['a', 9, 0]], [1, 'poll', [5]], [9, 'poll', [5]]]
print('seq check:', run(Scheduler, reuse)[-2:], ' id-only check:', run(IdOnly, reuse)[-2:])
assert run(Scheduler, reuse)[-2:] == [[], ['a']] and run(IdOnly, reuse)[-2:] == [['a'], []]

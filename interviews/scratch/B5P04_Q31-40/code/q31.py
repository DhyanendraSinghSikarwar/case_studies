import asyncio
import queue
import random
import sys
import threading
from collections import Counter, deque

# --- 1. The prompt's example -------------------------------------------------
q = queue.Queue(maxsize=2)
q.put(1)
q.put(2)
try:
    q.put_nowait(3)
except queue.Full:
    print("put_nowait(3) -> queue.Full")
assert q.get() == 1
print("get() ->", 1, "| full:", q.full(), "| qsize:", q.qsize())

d = deque(maxlen=2)
for v in (1, 2, 3):
    d.append(v)
print("deque(maxlen=2) after 1,2,3 ->", d)
assert list(d) == [2, 3]          # 1 was dropped silently from the opposite end

# --- 2. Blocking behaviour: Queue waits (with a timeout), deque raises -------
try:
    queue.Queue().get(timeout=0.05)
except queue.Empty:
    print("Queue().get(timeout=0.05) on empty -> queue.Empty after waiting")
try:
    deque().popleft()
except IndexError as e:
    print("deque().popleft() on empty -> IndexError immediately:", e)

# --- 3. Producer-consumer with Queue: seeded cross-check ---------------------
def run_pipeline(rng):
    n_prod, n_cons = rng.randint(1, 3), rng.randint(1, 3)
    per = [[rng.randint(0, 9) for _ in range(rng.randint(0, 6))] for _ in range(n_prod)]
    qq = queue.Queue(maxsize=rng.randint(1, 3))
    got, lock = [], threading.Lock()
    STOP = object()

    def producer(items):
        for x in items:
            qq.put(x)                 # blocks when full: natural back-pressure

    def consumer():
        while True:
            x = qq.get()              # blocks when empty
            if x is STOP:
                qq.task_done()
                return
            with lock:
                got.append(x)
            qq.task_done()

    cons = [threading.Thread(target=consumer) for _ in range(n_cons)]
    prods = [threading.Thread(target=producer, args=(p,)) for p in per]
    for t in cons + prods:
        t.start()
    for t in prods:
        t.join()
    for _ in cons:
        qq.put(STOP)                  # one stop marker per consumer
    qq.join()                         # returns when every task_done() has matched a put()
    for t in cons:
        t.join()
    sent = Counter(x for p in per for x in p)
    return Counter(got) == sent

rng = random.Random(31)
assert all(run_pipeline(rng) for _ in range(150))
print("150 seeded Queue pipelines: every item delivered exactly once")

# --- 4. Check-then-act on a deque is a race (forced deterministically) -------
dq = deque([1])
barrier = threading.Barrier(2)
outcome = []

def risky():
    if dq:                            # both threads see a non-empty deque...
        barrier.wait()                # ...before either one pops
        try:
            outcome.append(dq.popleft())
        except IndexError:
            outcome.append("IndexError")

ts = [threading.Thread(target=risky) for _ in range(2)]
for t in ts:
    t.start()
for t in ts:
    t.join()
print("two threads, if-d-then-popleft ->", sorted(map(str, outcome)))
assert sorted(map(str, outcome)) == ["1", "IndexError"]

def safe_pop(dd):
    try:
        return dd.popleft()           # one atomic call, handle failure
    except IndexError:
        return None

assert safe_pop(deque([5])) == 5 and safe_pop(deque()) is None

# --- 5. asyncio.Queue is the coroutine version -------------------------------
async def main():
    aq = asyncio.Queue(maxsize=2)
    out = []

    async def prod():
        for i in range(5):
            await aq.put(i)           # suspends the coroutine, not the thread
        await aq.put(None)

    async def cons():
        while (x := await aq.get()) is not None:
            out.append(x)

    await asyncio.gather(prod(), cons())
    return out

res = asyncio.run(main())
assert res == [0, 1, 2, 3, 4]
print("asyncio.Queue pipeline ->", res)

# --- 6. Version facts as observed --------------------------------------------
print("Python", sys.version.split()[0], "| Queue has shutdown():", hasattr(queue.Queue, "shutdown"))

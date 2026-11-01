import random
import sys
import time
from collections import deque


def run_list(cmds):
    q, out = [], []
    for c in cmds:
        if c.startswith("push"):
            q.append(int(c[5:]))
        else:
            out.append(q.pop(0))                 # O(n): shifts every remaining element
    return out


def run_deque(cmds):
    q, out = deque(), []
    for c in cmds:
        if c.startswith("push"):
            q.append(int(c[5:]))
        else:
            out.append(q.popleft())              # O(1)
    return out


def run_brute(cmds):
    # independent reference: remember all pushes and a read pointer
    pushed, head, out = [], 0, []
    for c in cmds:
        if c.startswith("push"):
            pushed.append(int(c.split()[1]))
        else:
            out.append(pushed[head]); head += 1
    return out


ex = ["push 1", "push 2", "pop", "push 3", "pop", "pop"]
assert run_list(ex) == run_deque(ex) == run_brute(ex) == [1, 2, 3]
print("prompt example ->", run_deque(ex))

# list as a stack: append/pop at the END are amortised O(1)
st = []
st.append(1); st.append(2); st.append(3)
assert st.pop() == 3 and st[-1] == 2
print("list as stack: top is st[-1], pop() returns the newest")

# deque(maxlen=k): a sliding window of the last k items, old ones fall off the left
w = deque(maxlen=3)
for v in range(1, 7):
    w.append(v)
assert list(w) == [4, 5, 6] and w.maxlen == 3
print("deque(maxlen=3) after appending 1..6 ->", list(w))

# seeded randomised cross-check of the three implementations
rng = random.Random(2024)
for _ in range(500):
    cmds, size = [], 0
    for _ in range(rng.randint(0, 30)):
        if size and rng.random() < 0.45:
            cmds.append("pop"); size -= 1
        else:
            cmds.append(f"push {rng.randint(-9, 9)}"); size += 1
    assert run_list(cmds) == run_deque(cmds) == run_brute(cmds)
assert run_deque([]) == [] and run_list(["push 5", "pop"]) == [5]   # edge cases
print("random cross-check passed: 500 command lists")


# sandbox-only timing: N pushes then N pops
def timed(fn, cmds):
    t = time.perf_counter(); fn(cmds); return time.perf_counter() - t


print("Python", sys.version.split()[0])
for n in (25_000, 50_000, 100_000, 200_000):
    cmds = [f"push {i}" for i in range(n)] + ["pop"] * n
    tl, td = timed(run_list, cmds), timed(run_deque, cmds)
    print(f"n={n:>7}: list.pop(0) {tl:7.3f}s   deque.popleft {td:7.3f}s")

# indexing into the middle of a deque is O(n); a list is O(1)
big_l = list(range(200_000)); big_d = deque(big_l)
t = time.perf_counter()
for _ in range(2000): big_l[100_000]
tl = time.perf_counter() - t
t = time.perf_counter()
for _ in range(2000): big_d[100_000]
td = time.perf_counter() - t
print(f"2000 middle lookups of 200000 items: list {tl:.4f}s   deque {td:.4f}s")

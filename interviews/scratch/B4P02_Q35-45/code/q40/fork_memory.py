"""Q40: memory cost of N workers that each hold a 'model'. Linux only.
Measures PSS (proportional set size: shared pages are split between the processes sharing them).
Run: python3 -I fork_memory.py"""
import os, sys, time
import numpy as np

N_WORKERS = 4
MB = 1024 * 1024

def pss_mb(pid="self"):
    with open(f"/proc/{pid}/smaps_rollup") as f:
        for line in f:
            if line.startswith("Pss:"):
                return int(line.split()[1]) / 1024

def make_array_model():          # one big numpy buffer, like weights; read-only after load
    return np.ones(25_000_000, dtype=np.float64)          # ~190 MB

def make_object_model():         # millions of small Python objects, like a big dict/list of floats
    return [float(i) + 0.5 for i in range(3_000_000)]     # every object has a refcount

def run(label, loader, touch):
    """Parent loads, then forks N workers. Each worker 'serves' (touch) and reports its own PSS."""
    model = loader()
    parent_before = pss_mb()
    r, w = os.pipe()
    pids = []
    for _ in range(N_WORKERS):
        pid = os.fork()
        if pid == 0:
            touch(model)                                   # simulate a request using the model
            os.write(w, f"{pss_mb():.0f}\n".encode())
            time.sleep(1.0)                                # stay alive while the parent measures
            os._exit(0)
        pids.append(pid)
    time.sleep(0.7)
    os.close(w)
    kids = [float(x) for x in os.read(r, 4096).decode().split()]
    total = pss_mb() + sum(kids)
    for pid in pids: os.waitpid(pid, 0)
    print(f"{label:<52} parent {parent_before:6.0f} MB | worker PSS {kids} | total {total:6.0f} MB")

arr_touch = lambda m: m[:1000].sum()                               # reads a few bytes of the buffer
def obj_touch(m):
    s = 0.0
    for x in m: s += x                                             # iterating bumps refcounts on every object
run("array model, fork after load, light use", make_array_model, arr_touch)
run("object model, fork after load, full pass (COW breaks)", make_object_model, obj_touch)
one = make_array_model(); print(f"one process holding the array model: {pss_mb():.0f} MB (so {N_WORKERS} separate loads would be ~{N_WORKERS*pss_mb():.0f} MB)")

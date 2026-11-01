# Illustrative numbers only. Overlap timeline, queue lag, skip-if-running cadence, and the shared-latest collision.
import math
dur, every = 7.5, 6.0                                  # hours
overlap = dur - every
assert overlap == 1.5
# 1. Timeline of 8 runs (48 hours of starts), at 1-minute resolution.
starts = [every * k for k in range(8)]
ends = [s + dur for s in starts]
horizon = int(ends[-1] * 60)
conc = [sum(1 for s, e in zip(starts, ends) if s * 60 <= m < e * 60) for m in range(horizon)]
assert max(conc) == 2
two = sum(1 for c in conc if c == 2) / 60
print('hours with 2 runs alive:', two, 'overlap windows:', len(starts) - 1)
assert two == 10.5 == (len(starts) - 1) * overlap
# In steady state the share of time with two runs alive is overlap / every.
assert overlap / every == 0.25
# 2. If the scheduler QUEUES runs one at a time instead, lag grows without bound.
lag = [(dur - every) * n for n in range(1, 17)]
print('queue lag after 8 runs (hours):', lag[7], 'after 16 runs:', lag[15])
assert lag[7] == 12.0 and lag[15] == 24.0
# 3. Skip-if-running keeps no overlap but halves the cadence: next free slot on the 6 h grid.
slot = math.ceil(dur / every) * every
print('effective interval with skip-if-running:', slot, 'h')
assert slot == 12.0
# Better: choose an interval from duration with a margin (here 20% over the 7.5 h average; use p95 in practice).
min_interval = dur * 1.2
assert min_interval == 9.0 and 9.0 > dur
# 4. Shared 'latest' checkpoint pointer: each run writes it every 30 min while alive.
def writes(s, e):
    return [s + 0.5 * i for i in range(1, int((e - s) / 0.5) + 1)]
w0 = [t for t in writes(starts[0], ends[0]) if t > starts[1]]     # run 0 after run 1 started
w1 = [t for t in writes(starts[1], ends[1]) if t <= ends[0]]       # run 1 before run 0 ended
print('latest-pointer writes by run 0 after run 1 started:', w0, 'by run 1 before run 0 ended:', w1)
assert w0 == [6.5, 7.0, 7.5] and w1 == [6.5, 7.0, 7.5]
# A new run that resumes from 'latest' at its start picks up run 0's mid-training state.
resume_state_hours = starts[1] - starts[0]
assert resume_state_hours == 6.0 and resume_state_hours < dur      # run 0 was still only 6 h into a 7.5 h job
# 5. Order of FINISH equals order of START only while durations stay close.
def inverted(d_k, d_next):
    return starts[0] + d_k > starts[1] + d_next
assert not inverted(7.5, 7.5) and inverted(13.0, 6.5)             # a run 6.5 h longer than its successor finishes AFTER it
# 6. Safe design: run-scoped paths + a lease with a fencing token; only the holder may promote.
class Lease:
    def __init__(self): self.token = 0; self.holder = None
    def acquire(self, run):
        if self.holder is None: self.token += 1; self.holder = run; return self.token
        return None
    def release(self, run): self.holder = None
L = Lease()
t0 = L.acquire('run0'); t1 = L.acquire('run1')
assert t0 == 1 and t1 is None                                       # second run refuses to start (or waits) while run0 holds the lease
promote_ok = lambda run, token, current: token == current           # a stale holder cannot promote
assert promote_ok('run0', 1, L.token) and not promote_ok('run0', 1, 2)
paths = [f'ckpt/{r}/step_{i}' for r in ('run0', 'run1') for i in range(3)]
assert len(set(paths)) == 6                                          # no shared file names
print('lease, run-scoped paths and promotion checks passed')

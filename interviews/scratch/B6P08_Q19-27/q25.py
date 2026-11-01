# Q25: backfill wall-clock time for 9 partitions. Exact scheduling arithmetic, illustrative durations.
import heapq, math
DUR, N_PART = 40, 9
def makespan(n_parts, slots, deps):
    """List scheduling: deps[i] = set of partitions that must finish before i starts. Returns (finish time, per-partition finish)."""
    done, running, t = {}, [], 0
    pending = list(range(n_parts))
    while pending or running:
        started = True
        while started:
            started = False
            for i in list(pending):
                if len(running) < slots and all(d in done and done[d] <= t for d in deps[i]):
                    heapq.heappush(running, (t + DUR, i)); pending.remove(i); started = True
        fin, i = heapq.heappop(running)
        t = fin; done[i] = fin
        while running and running[0][0] == fin:
            _, j = heapq.heappop(running); done[j] = fin
    return t, done
indep = {i: set() for i in range(N_PART)}
chain = {i: ({i - 1} if i else set()) for i in range(N_PART)}
t_ind4, _ = makespan(N_PART, 4, indep)
t_ord4, _ = makespan(N_PART, 4, chain)
print(f"independent, 4 slots: {t_ind4} min = {t_ind4/60:.1f} h   (waves: {math.ceil(N_PART/4)})")
print(f"strict chain, 4 slots: {t_ord4} min = {t_ord4/60:.1f} h   (extra slots do not help)")
assert t_ind4 == 3 * 40 == 120 and t_ord4 == 9 * 40 == 360
# live jobs need room: cap the backfill at 2 slots (independent case) or 1
t_ind2, _ = makespan(N_PART, 2, indep); t_ind1, _ = makespan(N_PART, 1, indep)
print(f"independent, capped at 2 slots: {t_ind2} min; at 1 slot: {t_ind1} min")
assert t_ind2 == 5 * 40 == 200 and t_ind1 == 360
# a rolling 7-day window computed from RAW daily data does not need the chain: compute 9 daily aggregates in parallel, then window
t_roll_cheap = 3 * DUR + 9 * 2          # 9 cheap window merges of 2 minutes each, run serially after the aggregates
print(f"two-stage plan: 9 daily aggregates (120 min) + 9 window merges of 2 min each = {t_roll_cheap} min (merge cost is an assumption)")
assert t_roll_cheap == 138
# only an INCREMENTAL feature (day d reads the stored output of day d-1) forces the chain
assert t_ord4 / t_ind4 == 3.0
# validation: partition row counts must sit inside a band around the healthy neighbours (illustrative counts)
healthy = [1_000_400, 998_900, 1_001_700, 999_300]
rebuilt = [1_000_900, 999_500, 0, 1_002_000, 7_300]          # 0 and 7,300 are suspicious
lo, hi = 0.95 * min(healthy), 1.05 * max(healthy)
bad = [i for i, n in enumerate(rebuilt) if not lo <= n <= hi]
print("partitions failing the row-count band:", bad)
assert bad == [2, 4]

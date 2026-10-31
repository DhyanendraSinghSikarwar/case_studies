# Q9: appended twice -> 2,000,000 rows for 1,000,000 customers. Illustrative; seeded.
import numpy as np
import pandas as pd

N = 1_000_000
rng = np.random.default_rng(9)
score = rng.random(N)
run_a = pd.DataFrame({"customer_id": np.arange(N), "run_date": "2026-10-31", "score": score, "run_id": "A"})
# run B is a retry: same model and features -> identical scores here; (a real retry may differ slightly)
run_b = run_a.assign(run_id="B")
table = pd.concat([run_a, run_b], ignore_index=True)

# 1) detect and size the damage
rows, distinct = len(table), table["customer_id"].nunique()
dups = rows - distinct
print(f"rows={rows:,} distinct customers={distinct:,} duplicate rows={dups:,} ({dups/rows:.0%} of the table)")
assert rows == 2_000_000 and distinct == 1_000_000 and dups == 1_000_000 and dups / rows == 0.5

# 2) before deleting anything: do the two runs agree?
m = run_a.merge(run_b, on="customer_id", suffixes=("_a", "_b"))
n_diff = int((m["score_a"] != m["score_b"]).sum())
print("customers whose two scores differ:", n_diff)
assert len(m) == N and n_diff == 0       # identical here, so keeping either row is safe. If not, pick by rule and log it.

# 3) clean up on a COPY, then swap (never delete in place first)
clean = table.sort_values(["customer_id", "run_id"]).drop_duplicates(["customer_id", "run_date"], keep="last")
assert len(clean) == N and clean["customer_id"].is_unique and (clean["run_id"] == "B").all()
print("clean table rows:", len(clean))

# 4) downstream: the campaign read 2,000,000 rows. Worst case each duplicated customer was contacted twice.
contacts_worst = rows                     # one contact per row read, if the campaign has no dedupe of its own
print("worst case contacts:", f"{contacts_worst:,}", "for", f"{N:,}", "customers -> up to", f"{contacts_worst-N:,}", "duplicate contacts")
assert contacts_worst - N == 1_000_000

# 5) redesign A: partition overwrite keyed by run date, staged then swapped (dict stands in for a table)
store = {}
def write_partition(store, run_date, df, run_id):
    staged = df.assign(run_id=run_id).drop_duplicates("customer_id")     # staged copy
    assert staged["customer_id"].is_unique
    store[run_date] = staged                                             # swap in as one step (atomic in a real system)
write_partition(store, "2026-10-31", run_a, "A")
write_partition(store, "2026-10-31", run_b, "B")                         # the duplicate run is harmless
assert len(store["2026-10-31"]) == N
print("after two runs, rows for the date:", len(store["2026-10-31"]))

# 6) redesign B: a lease with a fencing token so the old run cannot write after the retry started
class Lease:
    def __init__(self): self.token = 0
    def acquire(self): self.token += 1; return self.token
    def check(self, t): return t == self.token
lease = Lease(); t1 = lease.acquire(); t2 = lease.acquire()               # retry took the lease at minute 55
assert lease.check(t2) and not lease.check(t1)
print("old run may commit:", lease.check(t1), "| retry may commit:", lease.check(t2))

# 7) final gate: downstream checks distinct keys == expected before reading
def readiness(df, expected): return len(df) == expected and df["customer_id"].is_unique
assert not readiness(table, N) and readiness(clean, N)
print("readiness: duplicated table =", readiness(table, N), "| clean table =", readiness(clean, N))

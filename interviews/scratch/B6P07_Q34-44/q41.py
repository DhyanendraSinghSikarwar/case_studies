# Illustrative numbers from the prompt
chunks_total, chunks_user = 2_000_000, 3_000
share = chunks_user / chunks_total
print(f"share of index affected: {share:.2%} ({chunks_user} of {chunks_total})")
assert share == 0.0015

target, backup = 30, 35
gap = backup - target
print("backup retention minus target:", gap, "days")
assert gap == 5

# Honest timeline. Day 0 = request. Live stores are deleted on day d (d <= 30).
# Any backup taken up to day d still holds the data, and expires 35 days after it was taken.
for d in (1, 7, 30):
    last_copy_expires = d + backup
    print(f"live deletion on day {d:2d}: last backup copy expires on day {last_copy_expires} (target day {target}, over by {last_copy_expires - target})")
assert [d + backup for d in (1, 7, 30)] == [36, 42, 65]

# Plan table: store -> action -> day it is done (invented schedule, illustrative)
plan = [
    ("raw chat logs", "delete by user id, verify by query", 3),
    ("vector index", "delete 3,000 chunks by user id, compact index, verify by query", 7),
    ("evaluation dataset", "remove or redact the rows, re-export without them", 10),
    ("backups", "cannot edit; suppression list re-applied on any restore; expire by day d + 35", 36),
]
for s, a, day in plan:
    print(f"{s:20s} day {day:3d}  {a}")
within = [s for s, a, day in plan if day <= target]
outside = [s for s, a, day in plan if day > target]
assert within == ["raw chat logs", "vector index", "evaluation dataset"] and outside == ["backups"]

# EMULATION in pure Python. No Kafka broker was run.
log = [(0,"u1","a"),(1,"u2","b"),(2,"u1","c"),(3,"u3","d"),(4,"u2",None),(5,"u1","e"),(6,"u4","f"),(7,"u3","g")]
# (offset, key, value); value None = tombstone
def compact(log, keep_tombstones=True):
    last = {}
    for off, k, v in log: last[k] = (off, k, v)           # latest offset per key wins
    out = sorted(last.values())
    return out if keep_tombstones else [r for r in out if r[2] is not None]
print("before :", log)
c = compact(log)
print("after compaction (tombstone for u2 still present until delete.retention):")
print("        ", c)
print("after tombstone expires:", compact(log, False))
print("latest-state table:", {k: v for _, k, v in compact(log, False)})
print("offsets are NOT renumbered:", [o for o,_,_ in c])

# time retention: events older than the window are deleted whole segments at a time
rate_per_day = 2_000_000; bytes_per_event = 500; retention_days = 7
total = rate_per_day * retention_days
print(f"\nretention {retention_days}d at {rate_per_day:,} events/day -> {total:,} events kept")
print(f"approx size one replica: {total*bytes_per_event/1e9:.1f} GB (x replication factor 3 = {3*total*bytes_per_event/1e9:.1f} GB)")
for want in (3, 7, 30, 90):
    print(f"backfill {want:>2} days of features from Kafka alone:", "possible" if want <= retention_days else "NOT possible, need the lake")
print("rolling 30-day feature needs history from day -30; with 7d retention the first 23 days are missing")

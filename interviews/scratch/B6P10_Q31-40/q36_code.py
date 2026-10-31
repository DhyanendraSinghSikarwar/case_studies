cards, feats, bpv, eps, fresh = 10_000_000, 40, 8, 25_000, 5
mem = cards * feats * bpv
print("bytes", mem, "GB (decimal)", mem / 1e9, "GiB", round(mem / 2**30, 3))
assert mem == 3_200_000_000 and round(mem / 2**30, 3) == 2.980
window = eps * fresh
print("events in one 5 s window", window)
assert window == 125_000
# share of cards touched in 5 s if events spread evenly (upper bound on distinct cards)
print("max share of cards updated in a window", window / cards)
assert window / cards == 0.0125
# with 3 copies (replication) and 1.5x key/overhead allowance (assumption, measure it)
copies, overhead = 3, 1.5
print("3 copies with 1.5x overhead GB", mem * copies * overhead / 1e9)
assert mem * copies * overhead == 14_400_000_000
# per-event write fan-out: a 40-feature update at 25k/s
writes = eps * 1  # one row write per event if features are stored as one row per card
print("row writes/s", writes, "bytes/s of values", eps * feats * bpv)
assert eps * feats * bpv == 8_000_000
# window features: a 1-hour sliding count with 5 s buckets needs 720 buckets per card per counter
buckets = 3600 // 5
print("buckets per counter", buckets)
assert buckets == 720

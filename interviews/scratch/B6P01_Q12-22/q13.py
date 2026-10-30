# Reconcile client events to the finance table by order_id (illustrative, deterministic)
finance = set(range(100_000))                   # orders finance booked
events = list(range(100_000))                   # one checkout_complete per real order
events += list(range(3_000))                    # 3,000 double fires (retry / back-navigation)
events += list(range(200_000, 201_000))         # 1,000 fired before payment confirmed (failed)
raw = len(events)
dedup = set(events)
matched = dedup & finance
phantom = dedup - finance
dupes = raw - len(dedup)
print("raw client events      :", raw)
print("distinct order_ids     :", len(dedup))
print("matched to finance     :", len(matched))
print("phantom (no finance)   :", len(phantom))
print("duplicate fires        :", dupes)
assert raw == 104_000 and len(matched) == 100_000 and len(phantom) == 1_000 and dupes == 3_000
sessions = 3_000_000
print(f"conversion on raw event : {raw / sessions:.3%}")
print(f"conversion on finance   : {len(matched) / sessions:.3%}")
assert round(raw / sessions, 5) == 0.03467 and round(len(matched) / sessions, 5) == 0.03333
print(f"overstatement           : {raw / len(matched) - 1:+.1%}")
assert round(raw / len(matched) - 1, 3) == 0.040

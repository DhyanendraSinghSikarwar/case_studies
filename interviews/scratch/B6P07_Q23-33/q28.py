# Batching: throughput and cost per million output tokens. Illustrative GPU price 2.5 per GPU-hour.
per_user = {1: 50, 4: 42, 8: 35, 16: 25}
need, gpu_hr = 30, 2.5
rows = {}
for bs, tps in per_user.items():
    agg = bs * tps
    cost = gpu_hr / (agg * 3600 / 1e6)
    ok = tps >= need
    rows[bs] = (agg, cost, ok)
    print(f"batch {bs:2d}: per-user {tps}, aggregate {agg} tok/s, cost/M tokens {cost:.2f}, meets 30? {ok}")
assert [rows[b][0] for b in (1, 4, 8, 16)] == [50, 168, 280, 400]
assert [rows[b][2] for b in (1, 4, 8, 16)] == [True, True, True, False]
best = max((b for b in rows if rows[b][2]), key=lambda b: rows[b][0])
print("choice", best)
assert best == 8
assert round(rows[8][1], 2) == 2.48 and round(rows[16][1], 2) == 1.74 and round(rows[1][1], 2) == 13.89
# Utilisation sensitivity (illustrative): GPU busy only 50% of the hour
for u in (1.0, 0.5, 0.3):
    c = gpu_hr / (280 * 3600 * u / 1e6)
    print(f"utilisation {u:.0%}: cost/M tokens {c:.2f}")
assert round(gpu_hr / (280*3600*0.5/1e6), 2) == 4.96
# Headroom: batch 8 gives 35 vs need 30 -> 5 tok/s margin (14%)
print("margin", 35 - 30, f"{(35-30)/35:.1%} of per-user speed")
assert round(5/35, 3) == 0.143

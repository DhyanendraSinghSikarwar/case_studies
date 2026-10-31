import math
# Q5 search ranking: illustrative numbers from the prompt
qps, cands, rerank_k = 1_000, 2_000, 100
core_rate, util = 25_000, 0.50
items_s = qps * rerank_k
eff = core_rate * util
cores = math.ceil(items_s / eff)
print(f"rerank load {items_s:,} items/s; effective per core {eff:,.0f}; cores {items_s/eff:.2f} -> {cores}")
full = qps * cands
print(f"if the learned model scored all {cands}: {full:,} items/s -> {math.ceil(full/eff)} cores ({full/items_s:.0f}x)")
print(f"single-core compute per query for {rerank_k} items: {rerank_k/core_rate*1000:.1f} ms")
split = {"gateway+network": 20, "query understanding": 20, "retrieval (2,000)": 50, "feature fetch": 30, "rerank (100)": 30, "blend+filters+render": 20, "slack": 30}
print(split, sum(split.values()))
# label budget illustration: 50,000 judged query-item pairs at 5 pairs/min per rater
pairs, rate = 50_000, 5
hours = pairs / rate / 60
print(f"labelling {pairs:,} pairs at {rate}/min = {hours:,.0f} rater-hours")
assert items_s == 100_000 and eff == 12_500 and cores == 8 and round(items_s / eff, 2) == 8.00
assert full == 2_000_000 and math.ceil(full / eff) == 160 and full / items_s == 20
assert rerank_k / core_rate * 1000 == 4.0 and sum(split.values()) == 200
assert round(hours) == 167

import math
searches, per, cap, util = 4000, 3, 2500, 0.60
rps = searches * per
eff = cap * util
inst = math.ceil(rps / eff)
print("requests/s", rps, "effective per instance", eff, "instances", inst, "exact", rps / eff)
assert rps == 12_000 and eff == 1500 and inst == 8 and rps / eff == 8.0
# utilisation with one instance down
print("util with 7 instances", round(rps / (7 * cap), 3), "with 9 (N+1) minus one", round(rps / (8 * cap), 3))
assert round(rps / (7 * cap), 3) == 0.686 and round(rps / (8 * cap), 3) == 0.6
# debounce + prefix cache lever: if 30% of calls are cache hits, backend load falls
for hit in (0.0, 0.3, 0.5):
    load = rps * (1 - hit)
    print("cache hit", hit, "backend rps", load, "instances", math.ceil(load / eff))
assert math.ceil(rps * 0.7 / eff) == 6 and math.ceil(rps * 0.5 / eff) == 4
# if the real mean is 4 requests per search the answer moves
assert math.ceil(searches * 4 / eff) == 11
# p99 budget: 50 ms total; illustrative split
budget = {"network+gateway": 10, "normalise/transliterate": 5, "retrieve prefix/trie": 15, "rank top-k": 15, "slack": 5}
print(budget, sum(budget.values()))
assert sum(budget.values()) == 50

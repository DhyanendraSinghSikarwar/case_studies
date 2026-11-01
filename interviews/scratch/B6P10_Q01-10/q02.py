import math
# Q2 feed ranking: illustrative numbers from the prompt plus clearly labelled assumptions
dau, opens, budget_ms = 2_000_000, 5, 150
req_day = dau * opens
avg = req_day / 86_400
peak = avg * 5
cands = 500
items_s = peak * cands
print(f"requests/day {req_day:,}, avg {avg:.1f} rps, peak {peak:.1f} rps")
print(f"item scores/s at peak {items_s:,.0f}")
# assumption (illustrative): one ranker instance scores 25,000 items/s; run at 50% at peak
inst_rate, util = 25_000, 0.5
inst = math.ceil(items_s / (inst_rate * util))
print(f"instances at 50% utilisation: {items_s/(inst_rate*util):.2f} -> {inst}")
# trade-off: pre-rank cut from 500 to 100 before the heavy ranker
cut = 100
items_cut = peak * cut
inst_cut = math.ceil(items_cut / (inst_rate * util))
print(f"with a pre-rank cut to {cut}: {items_cut:,.0f} items/s -> {inst_cut} instances")
split = {"gateway+network": 10, "retrieval": 40, "feature fetch": 30, "ranker": 40, "re-rank rules+serialise": 15, "slack": 15}
print(split, sum(split.values()))
assert req_day == 10_000_000 and round(avg, 2) == 115.74 and round(peak, 1) == 578.7
assert round(items_s) == 289_352
assert inst == 24 and round(items_s / (inst_rate * util), 2) == 23.15
assert round(items_cut) == 57_870 and inst_cut == 5
assert sum(split.values()) == budget_ms

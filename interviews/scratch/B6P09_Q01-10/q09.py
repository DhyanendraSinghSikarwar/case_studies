import numpy as np
# Part A: prompt arithmetic (illustrative, measured yesterday)
early_spend, late_spend, cpa_e, cpa_l, move = 15_000, 9_000, 30, 20, 6_000
conv0 = early_spend / cpa_e + late_spend / cpa_l
lost = move / cpa_e
gained = move / cpa_l
conv1 = conv0 - lost + gained
print(f"unpaced conversions {conv0:.0f}; move {move:,}: lose {lost:.0f} at 30, gain {gained:.0f} at 20, net {gained-lost:+.0f} -> {conv1:.0f} ({(conv1/conv0-1):.1%})")
for x in (20, 25, 30, 35):
    print(f"  later marginal CPA {x}: gain {move/x:.0f}, net {move/x - lost:+.0f}")
for e in (30, 40):
    print(f"  early marginal CPA of the removed spend {e}: lose {move/e:.0f}; break-even later marginal CPA {e}")
assert conv0 == 950 and lost == 200 and gained == 300 and conv1 == 1050 and round(conv1 / conv0 - 1, 4) == 0.1053
assert round(move / 25) == 240 and round(move / 35) == 171 and move / 40 == 150 and early_spend + late_spend == 24_000

# Part B: a feedback pacing controller on an invented hourly day. Unpaced spend = 15,000 in hours 0-8 and 9,000 in hours 9-23.
budget = 24_000
base = np.array([15_000 / 9] * 9 + [9_000 / 15] * 15)
cpa_base = np.array([30.0] * 9 + [20.0] * 15)
plan = np.arange(1, 25) * budget / 24              # even-spend plan: 1,000 per hour, so 9,000 by 09:00 (6,000 moved)
def day(k_cpa, gain=0.15, k_spend=1.5):
    m = 1.0; spent = 0.0; conv = 0.0; by9 = 0.0
    for h in range(24):
        err = (plan[h] - spent) / (budget / 24)    # hours of spend we are behind plan (negative = ahead)
        m = float(np.clip(m * (1 + gain * err), 0.3, 3.0))
        s = min(base[h] * m ** k_spend, budget - spent)   # invented: spend grows as m^1.5
        c = s / (cpa_base[h] * m ** k_cpa)                # invented: CPA grows as m^k_cpa (0 = CPA never moves)
        spent += s; conv += c
        if h == 8: by9 = spent
    return by9, spent, conv
rows = {k: day(k) for k in (0.0, 0.3, 0.6, 1.0)}
for k, (b9, sp, cv) in rows.items():
    print(f"CPA elasticity {k:.1f}: spent by 09:00 {b9:,.0f}, day spend {sp:,.0f}, conversions {cv:,.0f}")
print("takeaway: the 1,050 bound needs the later CPA to stay at 20 AND the later hours to absorb 15,000; otherwise pacing can lose conversions")
assert all(8_500 < r[0] < 9_500 for r in rows.values())            # controller does hold early spend near 9,000
assert rows[0.0][2] > 950                                          # with a flat CPA, moving spend helps
assert rows[0.0][2] < 1050 + 1e-6                                  # but never above the optimistic bound
assert rows[0.0][2] > rows[0.3][2] > rows[0.6][2] > rows[1.0][2]   # a rising CPA eats the gain
assert rows[0.6][2] < 950 < 1050                                   # at this elasticity pacing loses conversions

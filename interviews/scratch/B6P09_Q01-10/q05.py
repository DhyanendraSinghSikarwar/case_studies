# Q5 delivery promise: illustrative numbers from the prompt plus invented conversion inputs
orders, on_time3 = 50_000, 44_000
late3 = orders - on_time3
rep_late, rep_ok = 0.20, 0.30
gap = rep_ok - rep_late
gap_orders = late3 * gap
late4 = round(orders * (1 - 0.97))
fewer_late = late3 - late4
gain_causal = fewer_late * gap              # repeat purchases kept if the whole gap were caused by lateness
gain_half = gain_causal / 2                 # if only half the gap is caused by lateness
print(f"late at 3 days {late3} ({late3/orders:.0%}); gap {gap:.0%} -> {gap_orders:.0f} repeat purchases")
print(f"late at 4 days {late4} ({late4/orders:.0%}); fewer late orders {fewer_late}; repeat purchases gained: causal {gain_causal:.0f}, half causal {gain_half:.0f}")
# break-even drop in checkout conversion: lost orders = gained repeat purchases (a repeat counted as worth one order, illustrative)
be_causal = gain_causal / orders
be_half = gain_half / orders
print(f"break-even relative conversion drop: {be_causal:.2%} (gap fully causal), {be_half:.2%} (half causal)")
# sample size to see a drop that small on an invented 5% checkout conversion (two-sided 5%, 80% power)
p = 0.05
for rel in (be_causal, be_half):
    delta = p * rel
    n = 2 * (1.96 + 0.84) ** 2 * p * (1 - p) / delta ** 2
    print(f"detect {rel:.2%} relative drop on {p:.0%} conversion: about {n/1e6:.1f} million sessions per arm")
n_half = 2 * (1.96 + 0.84) ** 2 * p * (1 - p) / (p * be_half) ** 2
n_causal = 2 * (1.96 + 0.84) ** 2 * p * (1 - p) / (p * be_causal) ** 2
assert (late3, late4, fewer_late) == (6000, 1500, 4500)
assert round(gap, 2) == 0.10 and round(gap_orders) == 600
assert round(gain_causal) == 450 and round(gain_half) == 225
assert round(be_causal, 4) == 0.009 and round(be_half, 4) == 0.0045
assert round(n_causal / 1e6, 1) == 3.7 and round(n_half / 1e6, 1) == 14.7

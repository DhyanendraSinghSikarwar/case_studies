rel = 1 - 18 / 22
new_ss = 300_000 * 18 / 22
saved_units = 300_000 - new_ss
saving = saved_units * 0.50
print(f"relative cut {rel:.2%}; new safety stock {new_ss:,.0f}; units freed {saved_units:,.0f}; weekly saving {saving:,.0f}")
assert abs(rel - 0.1818) < 1e-4 and round(saved_units) == 54_545 and abs(saving - 27_272.7) < 1
print(f"annual (52 weeks) {saving*52:,.0f}")
# WAPE is volume-weighted, safety stock sits where error is large (slow movers). Illustrative split:
w_fast, w_slow = 0.8, 0.2
old = w_fast * 20 + w_slow * 30
new = w_fast * 15 + w_slow * 30
print(f"overall WAPE {old:.0f} -> {new:.0f} when only fast movers improve (20 -> 15, slow stays 30)")
assert abs(old - 22) < 1e-9 and abs(new - 18) < 1e-9
fast_stock_share = 0.30   # assumed share of safety stock held on fast movers
true_cut = fast_stock_share * (1 - 15 / 20)
true_saving = 300_000 * true_cut * 0.50
print(f"stock cut {true_cut:.1%} not {rel:.1%}; weekly saving {true_saving:,.0f} not {saving:,.0f}")
assert abs(true_cut - 0.075) < 1e-9 and abs(true_saving - 11_250) < 1e-6
cost = 20_000   # illustrative weekly running cost of the model
print(f"claimed saving net of an illustrative {cost:,} running cost: {saving-cost:,.0f}; ROI {(saving-cost)/cost:.2f}")
print(f"with the realistic saving: {true_saving-cost:,.0f}")
assert abs((saving - cost) / cost - 0.3636) < 1e-3 and true_saving - cost < 0

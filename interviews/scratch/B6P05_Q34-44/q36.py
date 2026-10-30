tx = 500_000
cb = 0.008 * tx
blocked = 0.30 * cb
saved = blocked * 85
declined = 0.01 * tx
lost = declined * 3.00
net = saved - lost
print(f"chargebacks {cb:,.0f}; blocked {blocked:,.0f}; saved {saved:,.0f}; lost margin {lost:,.0f}; net {net:,.0f}")
assert round(cb) == 4_000 and round(blocked) == 1_200 and round(saved) == 102_000
assert round(declined) == 5_000 and round(lost) == 15_000 and round(net) == 87_000
before = cb / tx
after_all = (cb - blocked) / tx
after_ex = (cb - blocked) / (tx - declined)
print(f"chargeback rate before {before:.3%}; after {after_all:.3%} (all tx) or {after_ex:.3%} (declines removed)")
assert abs(before - 0.008) < 1e-12 and abs(after_all - 0.0056) < 1e-12
assert abs(after_ex - 2800 / 495_000) < 1e-12
print(f"headroom to the 1.0% limit before the rule: {0.01*tx - cb:,.0f} chargebacks")
assert round(0.01 * tx - cb) == 1_000
be = saved / 3.00
print(f"rule pays on margin alone up to {be:,.0f} declined genuine tx; ratio {be/blocked:.1f} declines per chargeback blocked (now {declined/blocked:.2f})")
assert round(be) == 34_000
# near the limit: add an assumed penalty (illustrative) of 50,000 a month if rate stays above 1.0%
cb_hot = 0.0105 * tx
print(f"if the rate were 1.05% ({cb_hot:,.0f}), blocking 30% gives {0.7*cb_hot/tx:.3%}, below 1.0%")
assert 0.7 * 0.0105 < 0.01

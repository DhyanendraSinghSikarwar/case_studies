# Q27: courier incentive at the dinner peak (illustrative)
req, cap0 = 1200, 1000
cap1 = cap0 * 1.10
print(f"fill rate {cap0/req:.1%} -> {cap1/req:.1%}; capacity {cap0} -> {cap1:.0f}")
assert abs(cap0 / req - 0.8333) < 1e-3 and cap1 == 1100

inc, m = 1.00, 2.50
cost_all = inc * cap1
extra_orders = cap1 - cap0
extra_margin = extra_orders * m
print(f"uniform incentive: cost {cost_all:.0f}/h, extra margin {extra_margin:.0f}/h, net {extra_margin-cost_all:+.0f}/h; cost per extra order {cost_all/extra_orders:.2f} vs margin {m}")
assert cost_all == 1100 and extra_margin == 250 and extra_margin - cost_all == -850 and cost_all / extra_orders == 11.0

# break-even uniform incentive and a threshold design (pay only above the 1,000 baseline)
print(f"break-even uniform incentive per delivery: {extra_margin/cap1:.3f}")
assert abs(extra_margin / cap1 - 0.2273) < 1e-3
cost_thr = inc * extra_orders
print(f"threshold design (pay 1.00 only on deliveries above 1,000): cost {cost_thr:.0f}/h, net {extra_margin-cost_thr:+.0f}/h; max rate that breaks even {m:.2f}")
assert cost_thr == 100 and extra_margin - cost_thr == 150

# if the threshold design only draws half the capacity response (50 extra orders), at the same 1.00
for resp in (100, 50, 40):
    print(f"  extra orders {resp}: margin {resp*m:.0f}, cost {inc*resp:.0f}, net {resp*(m-inc):+.0f}")
assert 100 * (m - inc) == 150 and 40 * (m - inc) == 60
# the 1.00 is paid on 1,100 in the uniform case: what share of the spend is a windfall to riders who would have worked anyway?
print(f"share of uniform spend paid on deliveries that would have happened anyway: {cap0/cap1:.1%}")
assert abs(cap0 / cap1 - 0.909) < 1e-3

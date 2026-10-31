import math

orders, rto_rate, ship, flag_share, flag_rto_share = 100_000, 0.25, 90, 0.20, 0.50
call, rescue = 6, 0.40
rto = round(orders * rto_rate)
flagged = round(orders * flag_share)
rto_flagged = round(rto * flag_rto_share)
assert (rto, flagged, rto_flagged) == (25_000, 20_000, 12_500)
precision = rto_flagged / flagged
assert precision == 0.625
cost = flagged * call
saved = rto_flagged * rescue * ship
net = saved - cost
assert cost == 120_000 and round(saved) == 450_000 and round(net) == 330_000
print("RTO orders:", rto, "| flagged:", flagged, "| RTO in flagged:", rto_flagged, "| precision:", precision)
print("call cost:", cost, "| saved:", round(saved), "| net per day:", round(net))

# Unflagged group and the marginal call
unf, unf_rto = orders - flagged, rto - rto_flagged
unf_rate = unf_rto / unf
breakeven = call / (rescue * ship)
print("unflagged orders:", unf, "RTO rate:", round(unf_rate, 4), "| break-even RTO probability for a call:", round(breakeven, 4))
assert round(unf_rate, 4) == 0.1562 and round(breakeven, 4) == 0.1667 and unf_rate < breakeven
net_all = rto * rescue * ship - orders * call
print("net if every order is called:", round(net_all), "| marginal value of calling the unflagged 80,000:", round(net_all - net))
assert round(net_all) == 300_000 and round(net_all - net) == -30_000

# The 40% rescue rate comes from a pilot sample. Pilot size 2,000; assume 25% would-be returns -> 500 (my assumption)
n_rto_pilot = round(2000 * rto_rate)
se = math.sqrt(rescue * (1 - rescue) / n_rto_pilot)
lo, hi = rescue - 1.96 * se, rescue + 1.96 * se
print("pilot would-be returns (assumed):", n_rto_pilot, "| rescue 95% interval:", round(lo, 3), "to", round(hi, 3))
for r in (lo, rescue, hi):
    print(f"  rescue {r:.3f} -> net per day {round(rto_flagged * r * ship - cost)}")
assert 0.35 < lo < 0.36 and 0.44 < hi < 0.45
assert round(rto_flagged * lo * ship - cost) < 285_000 < round(rto_flagged * hi * ship - cost)
# Rescue rate at which the flagged programme breaks even
be_rescue = cost / (rto_flagged * ship)
print("break-even rescue rate for the flagged group:", round(be_rescue, 4))
assert round(be_rescue, 4) == 0.1067

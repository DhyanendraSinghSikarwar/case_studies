import math
# Q1 fraud: illustrative numbers from the prompt
daily, fraud_rate = 5_000_000, 0.0005
peak, per_inst, headroom = 300, 120, 0.40
avg = daily / 86_400
fraud_day = daily * fraud_rate
target = peak * (1 + headroom)            # capacity to provision
raw = target / per_inst
n = math.ceil(raw)
n_plus1 = n + 1
util_at_peak = peak / (n * per_inst)
cap_after_loss = (n - 1) * per_inst
alt_util_rule = math.ceil(peak / 0.60 / per_inst)   # if "40% headroom" meant 60% target utilisation
print(f"avg {avg:.1f} rps, peak/avg {peak/avg:.2f}x, fraud/day {fraud_day:,.0f}")
print(f"target capacity {target:.0f} rps -> {raw:.2f} instances -> {n}; with N+1 {n_plus1}")
print(f"utilisation at peak with {n}: {util_at_peak:.1%}; capacity after losing one of {n_plus1}: {n*per_inst} rps")
print(f"if headroom meant 60% utilisation: {peak/0.60:.0f} rps -> {alt_util_rule} instances")
# illustrative threshold economics: missed fraud 2,000 rupees, friction per false block 40
miss_cost, fp_cost = 2000, 40
be_prec = fp_cost / (fp_cost + miss_cost)
print(f"break-even precision to block: {be_prec:.2%}")
# latency budget split of the 100 ms p99 scoring slice
split = {"gateway+network": 15, "feature fetch": 30, "model": 15, "rules+policy": 10, "serialise/log": 10, "slack": 20}
print(split, sum(split.values()))
assert round(avg, 1) == 57.9 and round(peak / avg, 2) == 5.18 and fraud_day == 2500
assert target == 420 and round(raw, 2) == 3.5 and n == 4 and n_plus1 == 5
assert round(util_at_peak, 3) == 0.625 and cap_after_loss == 360 and n * per_inst == 480
assert alt_util_rule == 5 and round(be_prec * 100, 2) == 1.96 and sum(split.values()) == 100
# the N+1 fleet of 5 still serves 4 x 120 = 480 >= 420 after losing one instance
assert (n_plus1 - 1) * per_inst >= target

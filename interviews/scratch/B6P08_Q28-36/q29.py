# Illustrative numbers only. Fallback loss, options, and a sampling check for the 3.5% fallback conversion rate.
import math
N, fb_rate = 1_000_000, 0.04
fb = round(N * fb_rate); model_n = N - fb
assert fb == 40000 and model_n == 960000
c_model, c_fb = 0.05, 0.035
rel_drop = (c_model - c_fb) / c_model
assert round(rel_drop, 2) == 0.30                      # 30% lower, relative to 5%
lost = fb * (c_model - c_fb)                            # conversions lost per hour if fallbacks converted like model traffic
assert round(lost) == 600
actual = model_n * c_model + fb * c_fb
ideal = N * c_model
assert round(actual) == 49400 and round(ideal) == 50000
print('lost/hour', round(lost), 'share of ideal', round(lost / ideal, 4))
assert round(lost / ideal, 3) == 0.012                  # 1.2% of conversions
value = 40                                              # illustrative value per conversion
print('lost value/hour', round(lost * value), 'per 30 days', round(lost * value * 24 * 30))
assert round(lost * value) == 24000
# Sampling noise on the 3.5% (measured on 40,000 hourly fallbacks): small, so the real doubt is bias, not noise.
se = math.sqrt(c_fb * (1 - c_fb) / fb)
lo, hi = c_fb - 1.96 * se, c_fb + 1.96 * se
print('95% interval for fallback rate', round(lo, 4), round(hi, 4))
assert 0.0332 <= round(lo, 4) <= 0.0333 and round(hi, 4) == 0.0368
lost_lo, lost_hi = fb * (c_model - hi), fb * (c_model - lo)
print('lost range', round(lost_lo), round(lost_hi))
assert 525 < lost_lo < 535 and 670 < lost_hi < 675
# Options (every share below is an ILLUSTRATIVE assumption to be replaced by a measured timeout-cause split).
queue_share, slow_tail_share = 0.70, 0.30               # 70% of timeouts are queueing, 30% slow requests
caught_by_200ms = 0.375                                 # share of ALL fallbacks that would finish in 150-200 ms
cap_fix = fb * queue_share * (c_model - c_fb)           # more capacity removes queueing timeouts
tmo_fix = fb * caught_by_200ms * (c_model - c_fb)       # timeout 150 -> 200 ms
fb_fix = fb * (0.042 - c_fb)                            # fallback improved from 3.5% to 4.2%
print('capacity', round(cap_fix), 'timeout', round(tmo_fix), 'better fallback', round(fb_fix))
assert (round(cap_fix), round(tmo_fix), round(fb_fix)) == (420, 225, 280)
# Capacity cost against gain: 3 extra pods at 10 units per pod-hour.
pods_cost = 3 * 10
print('capacity gain value', round(cap_fix * value), 'cost', pods_cost)
assert round(cap_fix * value) == 16800 and pods_cost == 30
# Decision rules written before the change (illustrative)
rollback = {'p99_ms_over': 400, 'total_conversion_drop_pts_over': 0.1, 'for_minutes': 15}
assert rollback['p99_ms_over'] > 150
# Why 5% vs 3.5% is not clean: slow requests are different requests. Tiny example with two request types.
heavy_share = 0.6                                       # share of fallbacks that are heavy users
c_heavy_model, c_light_model = 0.04, 0.06               # what the model would have converted
true_cf = heavy_share * c_heavy_model + (1 - heavy_share) * c_light_model
assert abs(true_cf - 0.048) < 1e-12
true_lost = fb * (true_cf - c_fb)
print('counterfactual lost if fallbacks are heavy users', round(true_lost))
assert round(true_lost) == 520 and true_lost < lost

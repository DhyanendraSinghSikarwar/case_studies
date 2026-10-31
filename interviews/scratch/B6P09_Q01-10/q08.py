import numpy as np
# Q8 ward alerts: illustrative per-day replay numbers
events, cap = 80, 100
cur_alerts, cur_tp = 600, 60
str_alerts, str_tp = 100, 40
sens_c, ppv_c = cur_tp / events, cur_tp / cur_alerts
sens_s, ppv_s = str_tp / events, str_tp / str_alerts
extra_alerts, extra_tp = cur_alerts - str_alerts, cur_tp - str_tp
ppv_extra = extra_tp / extra_alerts
print(f"current: sens {sens_c:.0%}, PPV {ppv_c:.0%}, alerts per event caught {cur_alerts/cur_tp:.0f}, over capacity by {cur_alerts/cap:.0f}x")
print(f"strict : sens {sens_s:.0%}, PPV {ppv_s:.0%}, alerts per event caught {str_alerts/str_tp:.1f}")
print(f"extra {extra_alerts} alerts hold {extra_tp} events: precision {ppv_extra:.0%}; missed events {events-cur_tp} vs {events-str_tp}")
# nurses can act on 100 of the 600 current alerts. Compare in-score-order versus arbitrary order (assumes strict alerts are the top 100 of the 600)
tp_random_order = cap * cur_tp / cur_alerts
tp_score_order = str_tp
print(f"events reached with 100 responses: arbitrary order {tp_random_order:.0f} (sens {tp_random_order/events:.1%}), score order {tp_score_order} (sens {tp_score_order/events:.0%})")
# simulate: do nurses answering a random 100 of 600 behave like a threshold at 100? (seeded)
rng = np.random.default_rng(3)
hits = []
for _ in range(2000):
    flags = np.zeros(cur_alerts, bool); flags[:cur_tp] = True
    seen = rng.permutation(cur_alerts)[:cap]
    hits.append(flags[seen].sum())
print(f"simulated events reached under random response: mean {np.mean(hits):.2f}")
assert (sens_c, sens_s) == (0.75, 0.5) and (ppv_c, ppv_s) == (0.10, 0.40)
assert (extra_alerts, extra_tp) == (500, 20) and round(ppv_extra, 2) == 0.04
assert cur_alerts / cap == 6 and cur_alerts / cur_tp == 10 and str_alerts / str_tp == 2.5
assert tp_random_order == 10 and tp_score_order == 40 and events - cur_tp == 20 and events - str_tp == 40
assert abs(np.mean(hits) - 10) < 0.3

# Q50: postmortem numbers: impact sizing and detection timeline. Illustrative numbers.
import numpy as np
rng = np.random.default_rng(50)
# impact: fraud model catch rate fell after a feature pipeline change
attempts_per_day = 1_000
avg_loss = 5_000           # Rs per missed fraud
catch_before, catch_after = 0.85, 0.70
days = 21
extra_missed_per_day = attempts_per_day*(catch_before - catch_after)
extra_loss = extra_missed_per_day*avg_loss*days
print(f"extra missed fraud/day {extra_missed_per_day:.0f}; extra direct loss over {days} days = Rs {extra_loss/1e5:.1f} lakh = Rs {extra_loss/1e7:.3f} crore")
assert round(extra_missed_per_day) == 150 and round(extra_loss) == 15_750_000
# counterfactual honesty: range of impact if catch_after was only reached gradually (linear ramp over 7 days)
ramp = np.concatenate([np.linspace(0, 0.15, 7), np.full(days-7, 0.15)])
loss_ramp = (ramp*attempts_per_day*avg_loss).sum()
print(f"if the drop ramped linearly over the first 7 days: Rs {loss_ramp/1e5:.1f} lakh")
assert loss_ramp < extra_loss
low, high = loss_ramp, extra_loss
print(f"quote a range: Rs {low/1e5:.0f} to {high/1e5:.0f} lakh direct loss, before chargeback fees and customer cost")

# detection timeline: which monitor would have fired when
label_delay = 14
t = np.arange(40)
shift = np.clip((t - 3)/1.0, 0, 1)      # pipeline change at day 3: null-rate jumps at once
null_rate = 0.005 + 0.15*shift + rng.normal(0, 0.002, t.size)
score_mean = 0.10 - 0.03*shift + rng.normal(0, 0.003, t.size)
catch = 0.85 - 0.15*shift + rng.normal(0, 0.01, t.size)
def first_alert(series, thr, above=True):
    idx = np.where(series > thr if above else series < thr)[0]
    return int(idx[0]) if len(idx) else None
d_null = first_alert(null_rate, 0.02)
d_score = first_alert(score_mean, 0.085, above=False)
d_label_visible = first_alert(catch, 0.80, above=False) + label_delay    # label-based metric only appears after delay
d_complaints = 24                         # analysts noticed in week 4 (illustrative)
print(f"change on day 3. null-rate alert day {d_null}; score-mean alert day {d_score}; labelled catch-rate alert day {d_label_visible}; humans noticed day {d_complaints}")
assert d_null == 4 and d_score is not None and d_score <= 5 and d_label_visible >= 17
print(f"time to detect: pipeline monitors {d_null-3} day(s); label-based {d_label_visible-3} days; actual {d_complaints-3} days")
assert d_complaints - 3 == 21
saved = (d_complaints - d_null)*ramp[-1]*attempts_per_day*avg_loss
print(f"loss avoided with a null-rate monitor: about Rs {saved/1e5:.0f} lakh")
assert abs(saved - 20*0.15*1000*5000) < 1  # 20 days x 150 x Rs 5,000 = Rs 150 lakh

# Q33: document-reading model loses accuracy after a new phone becomes popular (illustrative simulation)
import numpy as np

rng = np.random.default_rng(33)
weeks = 12
share_new = np.linspace(0.02, 0.30, weeks)      # share of uploads from the new phone
per_week = 5000                                    # uploads per week
acc_old, acc_new = 0.95, 0.80                   # true accuracy by device group

# 1. Overall accuracy slides while old-phone accuracy is flat
n_new = rng.binomial(per_week, share_new)
ok_new = rng.binomial(n_new, acc_new)
ok_old = rng.binomial(per_week - n_new, acc_old)
overall = (ok_new + ok_old) / per_week
old_only = ok_old / (per_week - n_new)
print("week  new-phone share  overall  old phones")
for w in (0, 5, 11):
    print(f"{w:>4}  {share_new[w]:>14.0%}  {overall[w]:>7.1%}  {old_only[w]:>10.1%}")
assert overall[0] - overall[-1] > 0.03 and abs(old_only[0] - old_only[-1]) < 0.01

# 2. Size of the problem: audit 300 labelled uploads from each group (human-checked)
a_new = rng.binomial(1, acc_new, 300); a_old = rng.binomial(1, acc_old, 300)
boot = []
for _ in range(2000):
    boot.append(rng.choice(a_old, 300).mean() - rng.choice(a_new, 300).mean())
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"audit gap old-new {a_old.mean() - a_new.mean():.3f}, bootstrap 95% [{lo:.3f}, {hi:.3f}]")
assert 0.08 < lo and hi < 0.22
# expected loss at 30% share if nothing is done: 0.30 x gap
loss = 0.30 * (acc_old - acc_new)
print(f"overall accuracy loss at 30% share: {loss:.3f}")
assert abs(loss - 0.045) < 1e-9

# 3. Threshold change versus other fixes: confidence scores differ by device
conf_old_ok = rng.beta(8, 1.2, 20000); conf_old_bad = rng.beta(3, 3, 1000)
conf_new_ok = rng.beta(5, 1.5, 16000); conf_new_bad = rng.beta(3, 3, 4000)
def at(th, ok, bad):
    kept_ok = (ok >= th).sum(); kept_bad = (bad >= th).sum()
    auto = kept_ok + kept_bad
    return auto / (len(ok) + len(bad)), kept_ok / auto
print("new-phone uploads: threshold -> share auto-processed, accuracy of auto-processed")
for th in (0.50, 0.70, 0.85):
    share, acc = at(th, conf_new_ok, conf_new_bad)
    print(f"  {th:.2f}  {share:.1%}  {acc:.1%}")
s50, a50 = at(0.50, conf_new_ok, conf_new_bad); s85, a85 = at(0.85, conf_new_ok, conf_new_bad)
assert a85 > a50 and s85 < s50             # a higher threshold buys accuracy with more manual review
print(f"going 0.50 -> 0.85 sends {s50 - s85:.1%} more of new-phone uploads to manual review")

# 4. Monitoring: alert when a new device model passes 5% of traffic or its audited accuracy is low
first_alert = int(np.argmax(share_new > 0.05))
print(f"week the new phone crosses 5% share: {first_alert}  (share {share_new[first_alert]:.1%})")
assert share_new[first_alert] > 0.05 and share_new[first_alert - 1] <= 0.05

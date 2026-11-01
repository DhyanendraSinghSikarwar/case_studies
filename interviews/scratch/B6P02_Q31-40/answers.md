### Q31 ⭐⭐ 🟡 An ads click model's predicted-to-observed click ratio drifted from 1.00 to 1.12 over a quarter, meaning it over-predicts, while AUC barely moved. Explain why this matters for bidding, what might cause it (traffic mix, auction changes, feedback effects), and how you would recalibrate without retraining everything.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
**Say this first (1 line):** A 12% over-prediction means every bid built on the click probability is about 12% too high, and AUC cannot see it because AUC only checks order; I would find which segments drifted, then fix it with a small calibration layer on top of the model, not a full retrain.

**Clarifying questions:**
- Is the 1.12 an average over all traffic, or is it the same in every slice (placement, device, advertiser, country)? Why: one slice at 1.45 and the rest at 1.00 needs a different fix from a uniform 1.12.
- Is the ratio measured on the same impressions the model scored, with clicks counted the same way (click-fraud filtering, attribution window)? Why: a changed click definition looks exactly like drift.
- How does the bid use the probability: bid = value per click x pCTR, in a first-price or second-price auction, with pacing or a budget? Why: it decides how much money the 12% costs.
- Did anything change in the auction (reserve prices, new formats, new inventory, a competitor)? Why: it points to traffic mix or auction effects instead of model decay.
- When was the model last retrained, and is a calibration layer already in the serving path? Why: it tells me whether a patch is quick or needs new plumbing.

**Approach:**
1. Confirm it is real: recompute predicted/observed on matured clicks, check the click definition and logging, and look at it by day to see slow slide versus step.
2. Say why it matters: bid = value x pCTR, so a 12% too-high pCTR is a 12% too-high bid. In a first-price auction you pay it. In a second-price auction you mostly pay the rival's price, but you win extra impressions that are worth less than the price. Pacing and ROI reporting also go wrong.
3. Slice by placement, device, advertiser, country, format and score bucket. A reliability table (predicted bucket versus observed rate) shows whether the error is uniform or sits in the tail.
4. Find causes. Traffic mix: more of a segment where the model was always high. Auction change: new placements or position effects the training data never saw. Feedback effects: the model's own wins shape which impressions it sees (it only learns from impressions it bought). Click-definition or logging change.
5. Fix without full retrain. Fit a calibration layer on the log-odds of the old score using a recent matured window: an intercept first, then a slope, then per-segment or isotonic only if slices disagree and there is enough data. Ranking stays untouched (monotone), so AUC and the downstream ordering do not move.
6. Validate on a later holdout (ratio, reliability table, spend, ROI), ship behind a canary, and alert on the ratio per slice.
7. Plan the real fix: retrain on recent data with the missing features, keep the calibration layer as the quick lever for the next drift.

**Metrics:**
- Calibration ratio = sum of predicted click probabilities / number of observed clicks, over a matured window (numerator and denominator on the same impressions).
- Reliability table: for each predicted-probability bucket, mean predicted versus observed click rate. Also log loss and Brier score.
- Business guardrails: spend, cost per click, ROI (value / spend) per campaign, win rate, pacing error.
- AUC stays as the ranking check; it is not the calibration check.

**Risks:**
- Fitting the fix on too little data: with a 2% click rate, 2,000 clicks give a ratio standard error of about 2%.
- One global factor can make a mixed problem worse (see the Code block: 1.00 and 1.45 segments end up at 0.89 and 1.29).
- Feedback loop: a recalibrated model changes which impressions are won, so the calibration data shifts again.
- Fixing the symptom and never asking why a segment drifted.
- Label delay: very recent clicks are incomplete, so the ratio looks too high just from immature data.

**What the interviewer scores:**
- Strong: states that AUC measures ranking and calibration measures level, and ties 1.12 to money (bid, win rate, ROI).
- Strong: slices before fixing, and says a single factor is only right if the error is uniform.
- Strong: proposes a cheap post-hoc recalibration on a matured window plus a validation and canary, and a retrain as the later step.
- Weak: "retrain the model" as the first and only answer, or "AUC is fine so there is no problem".
- Cross-reference: Book 1 Part 3 has "What is model calibration and why can a model with great AUC still be badly calibrated?" and Book 1 Part 7 has "Does a ranker's predicted probability need to be calibrated? When does it matter (ads, blending scores, thresholds) and how do you fix it?".

**Example:** (illustrative numbers) 1,000 impressions with predicted CTR 2.0% each give 20 expected clicks; you observe 17.9, so the ratio is 20 / 17.9 = 1.12. You value a click at Rs 10 and bid pCTR x Rs 10, so you bid Rs 0.20 where the true value is about Rs 0.18. Weak answer: "AUC is the same, so the model is fine." Strong answer: "AUC checks order, not level. The bid is 12% high, so I would slice the ratio, fit an intercept on matured clicks, canary it, and keep the retrain for later."

**Code:**
```python
# Q31: ads click model over-predicts (ratio 1.12) while AUC is unchanged (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(31)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
logit = lambda p: np.log(p / (1 - p))
sig = lambda z: 1 / (1 + np.exp(-z))

N = 1_200_000
p_true = np.clip(rng.lognormal(np.log(0.02), 0.8, N), 1e-4, 0.5)   # true CTR per impression
y = (rng.random(N) < p_true).astype(int)

# Drift = a constant shift in the log-odds. Find the shift that gives predicted/observed = 1.12.
lo, hi = 0.0, 0.5
for _ in range(60):
    mid = (lo + hi) / 2
    if sig(logit(p_true) + mid).mean() / y.mean() < 1.12: lo = mid
    else: hi = mid
shift = (lo + hi) / 2
p_pred = sig(logit(p_true) + shift)
ratio = p_pred.mean() / y.mean()
print(f"shift in log-odds: {shift:.3f}   predicted/observed: {ratio:.3f}")
assert abs(ratio - 1.12) < 0.01          # observed clicks are random, so allow 0.01

# AUC does not see a monotone shift at all
a0, a1 = auc(y, p_true), auc(y, p_pred)
print(f"AUC before drift {a0:.4f}   after drift {a1:.4f}")
assert abs(a0 - a1) < 1e-12

# Why bidding cares: bid = value_per_click * pCTR. Real value of an impression = value * true CTR.
v = 10.0                                   # Rs per click (illustrative)
rival = rng.lognormal(np.log(v * 0.02), 0.8, N)   # rival bids
rival_fp = rival * 0.6                              # rivals shade too
def second_price(p_used):                  # winner pays the rival bid
    win = v * p_used > rival
    return (v * p_true[win] - rival[win]).sum(), win.sum()
def first_price(p_used):                   # winner pays its own bid
    bid = 0.6 * v * p_used; win = bid > rival_fp   # shade the bid to 60% of value
    return (v * p_true[win] - bid[win]).sum(), win.sum(), bid[win].sum()
sp_ok, w_ok = second_price(p_true); sp_bad, w_bad = second_price(p_pred)
fp_ok, _, spend_ok = first_price(p_true); fp_bad, _, spend_bad = first_price(p_pred)
print(f"second price: won {w_ok} -> {w_bad}; profit Rs {sp_ok:,.0f} -> {sp_bad:,.0f}")
print(f"first price : profit Rs {fp_ok:,.0f} -> {fp_bad:,.0f}; spend Rs {spend_ok:,.0f} -> {spend_bad:,.0f}")
assert w_bad > w_ok and sp_bad < sp_ok     # extra wins are the unprofitable ones
assert fp_bad < 0.9 * fp_ok and 0.8 < sp_bad / sp_ok < 1 and spend_bad > 1.12 * spend_ok   # you pay your own inflated bid

# Recalibrate WITHOUT retraining: fit one intercept on the log-odds of the old score
# using a recent window (first 800k impressions), then test on the rest.
fit, test = slice(0, 800_000), slice(800_000, N)
z = logit(p_pred[fit]); b = 0.0
for _ in range(25):                         # Newton steps on the intercept only
    q = sig(z + b)
    b -= (q - y[fit]).sum() / (q * (1 - q)).sum()
p_fix = sig(logit(p_pred) + b)
r_fix = p_fix[test].mean() / y[test].mean()
print(f"fitted offset {b:.3f}   ratio on holdout after fix {r_fix:.3f}")
assert abs(b + shift) < 0.06 and abs(r_fix - 1) < 0.03
assert abs(auc(y, p_fix) - a1) < 1e-12      # ranking is untouched
fp_fix, _, _ = first_price(p_fix)
print(f"first-price profit after fix (Rs): {fp_fix:,.0f}")
assert fp_fix > fp_bad

# Segment trap: overall 1.12 can hide one bad segment, and one global factor then mis-fixes both.
share = np.array([0.65, 0.35]); seg_ratio = np.array([1.00, 1.45])
pred = np.array([0.020, 0.020]); obs = pred / seg_ratio
overall = (share * pred).sum() / (share * obs).sum()
print(f"overall ratio {overall:.3f}; segment ratios {seg_ratio}")
assert abs(overall - 1.12) < 0.005
after_global = seg_ratio / overall          # divide every prediction by the overall ratio
print("after one global factor, segment ratios:", np.round(after_global, 3))
assert after_global[0] < 0.9 and after_global[1] > 1.25
```

**Output (my run):**
```text
shift in log-odds: 0.128   predicted/observed: 1.120
AUC before drift 0.7197   after drift 0.7197
second price: won 599633 -> 652488; profit Rs 141,722 -> 140,959
first price : profit Rs 94,429 -> 80,257; spend Rs 141,644 -> 167,743
fitted offset -0.118   ratio on holdout after fix 1.007
first-price profit after fix (Rs): 93,405
overall ratio 1.122; segment ratios [1.   1.45]
after one global factor, segment ratios: [0.891 1.293]
```
The text above matches this run: the 12% drift moves AUC by nothing (0.7197 both), the second-price loss is small (about 0.5%, the extra wins are near break-even), the first-price loss is large (profit down about 15%, spend up about 18%), and one fitted intercept brings the holdout ratio to 1.007.

**Follow-ups:**
- Why not just retrain? It can take days, needs fresh labels, and the same drift can come back; a calibration layer is a fast, reversible patch, and you still retrain to fix the root cause.
- Intercept, Platt (intercept plus slope) or isotonic? Intercept if the error is a uniform level shift; Platt if the error grows with the score; isotonic if the shape is irregular and you have a lot of data.
- What if the ratio is 1.00 overall but wrong by segment? Then bids are mis-priced across segments even though the total looks right; calibrate per segment or add the segment feature.

**Common mistakes:** Saying AUC fine means model fine. Dividing every prediction by 1.12 without slicing. Fitting on immature clicks. Ignoring the auction type. Forgetting the feedback loop.

### Q32 ⭐⭐ 🟡 A support-ticket triage LLM is checked weekly by humans on 400 random tickets, and accuracy went from 91% (364 of 400) to 86% (344 of 400) after a product launch. Explain whether that sample size supports calling it a real decline, what you would segment by, and how you would decide what to do next.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** Five points on 400 tickets is borderline evidence (p about 0.03, and the 95% interval runs from under 1 point to about 9 points), so I would not call it a decline yet; I would split it by ticket type and by what the launch changed, and decide from that.

**Clarifying questions:**
- Are the 400 tickets a fresh random sample each week, labelled blind by the same reviewers with the same rubric? Why: a changed reviewer or rubric moves accuracy with no change in the model.
- What did the launch change: new ticket types, new languages, a new form, a new model or prompt? Why: it separates a coverage gap from real decay.
- What does "accuracy" mean here (exact category match, priority, routing)? Why: different errors cost different amounts.
- What are the costs: a mis-routed urgent ticket versus a mis-tagged low-priority one? Why: they decide how much evidence I need before acting.
- How many weekly checks have we looked at so far? Why: the more weeks you watch, the more false alarms you will see.

**Approach:**
1. Do the arithmetic. 364/400 = 91.0% and 344/400 = 86.0%. Pooled rate 0.885, standard error 0.0226, z = 2.22, two-sided p = 0.027. The interval for the drop is about 0.6 to 9.4 points. So: probably lower, but the size is very uncertain.
2. Say what the sample can and cannot do. To catch a 5-point drop with 80% power you need about 635 tickets a week, so 400 is slightly underpowered. And with weekly checks, about 1 week in 19 shows a "significant" drop by luck alone.
3. Do not stop at the p-value. The launch is not randomised, so ask what else changed: ticket mix, language, channel, reviewers.
4. Segment: by ticket type (especially new types), language, channel, customer tier, ticket length, model or prompt version, and reviewer. Compare accuracy inside each segment before and after. Report the mix effect and the within-segment effect separately.
5. Get more labels where they matter: stratify the next sample by the suspicious segments (oversample the new types), and add a second reviewer on a subset to measure labelling agreement.
6. Decide by cost, not by p-value: if the drop sits in one new ticket type, add examples and routing rules for it; if it is broad, check the model, prompt and retrieval versions; if urgent tickets are hit, fall back to a human queue for them now.

**Metrics:**
- Accuracy = correct triage decisions / tickets reviewed, per week and per segment, with a Wilson or normal interval.
- Difference = this week minus baseline, with a 95% interval; the baseline should be several weeks, not one.
- Mix decomposition: change = sum over segments of (share x change in accuracy) + sum of (change in share x accuracy). Both parts are reported.
- Guardrails: mis-routed urgent tickets per 1,000, time to first response, reviewer agreement rate.

**Risks:**
- Calling noise a decline, or calling a real decline noise because p is above 0.05.
- Simpson-type mix: the model is the same on old tickets but the launch added a hard new type (see Code).
- Reviewer drift or a rubric change.
- A sample that is not random: easy tickets are labelled faster.
- Looking at many segments and finding one that is "significant" by chance.

**What the interviewer scores:**
- Strong: does the arithmetic out loud (z, p, interval, power) and says what it means in words.
- Strong: separates statistics from causality: the launch is not an experiment, so segment and find the mechanism.
- Strong: links the decision to costs and offers a cheap next step (more labels in the suspect segment).
- Weak: "400 is too small" with no calculation, or "p < 0.05 so it dropped" with no cause.
- Cross-reference: Book 6 Part 1 has "A daily metric is down 2% and an alert fired. The metric usually moves 1.5% day to day, with a weekend dip..." as the same noise-versus-signal question for a product metric (Q37 in Part 1).

**Example:** (illustrative numbers) Before the launch: 400 old-type tickets, 364 right (91%). After: 300 old-type tickets, 276 right (92%), and 100 tickets of a new type the launch created, 68 right (68%). Total 344 of 400 = 86%. The old types did not get worse (they went up one point). The new type is 25% of the sample at 68%, which costs 0.25 x (0.68 - 0.91) = 5.75 points, and the old types add back 0.75 x 0.01 = 0.75 points; net -5 points. Weak answer: "The model degraded 5 points, retrain it." Strong answer: "The drop is borderline by itself, but split by type it is all one new ticket category. I would add labelled examples and a rule for that category and keep watching the old types."

**Code:**
```python
# Q32: is 91% -> 86% on 400 tickets a real decline? (numbers from the prompt, rest illustrative)
import math
import numpy as np

def phi_upper(z): return 0.5 * math.erfc(z / math.sqrt(2))     # P(Z > z)

a_ok, b_ok, n = 364, 344, 400
pa, pb = a_ok / n, b_ok / n
assert (pa, pb) == (0.91, 0.86)
pool = (a_ok + b_ok) / (2 * n)
se_pool = math.sqrt(pool * (1 - pool) * (2 / n))
z = (pa - pb) / se_pool
p_two = 2 * phi_upper(z)
se_diff = math.sqrt(pa * (1 - pa) / n + pb * (1 - pb) / n)
lo, hi = (pa - pb) - 1.96 * se_diff, (pa - pb) + 1.96 * se_diff
print(f"drop {pa - pb:.3f}  z {z:.2f}  two-sided p {p_two:.4f}  95% CI for the drop [{lo:.3f}, {hi:.3f}]")
assert round(z, 2) == 2.22 and 0.02 < p_two < 0.035 and 0.004 < lo < 0.008 and 0.09 < hi < 0.10

# Power: tickets per week needed to detect a 5-point drop from 91% (80% power, 5% two-sided)
za, zb = 1.96, 0.8416
need = (za + zb) ** 2 * (pa * (1 - pa) + pb * (1 - pb)) / (pa - pb) ** 2
print(f"tickets per week for 80% power at a 5-point drop: {need:.0f}")
assert 600 < need < 700

# Weekly checking: if the true accuracy never changes (89%), how often does a week
# look 'significantly lower' than the previous week at the 5% one-sided level?
rng = np.random.default_rng(32)
weeks = 20_000
x = rng.binomial(n, 0.89, size=weeks + 1)
p = x / n
z_w = (p[:-1] - p[1:]) / np.sqrt(2 * 0.89 * 0.11 / n)
false_alarm = (z_w > 1.645).mean()
print(f"false 'decline' weeks when nothing changed: {false_alarm:.3f}  (about 1 in {1 / false_alarm:.0f} weeks)")
assert 0.03 < false_alarm < 0.07

# Mix effect: launch added a new ticket type the model never saw. Same model, same skill on old types.
before = {"old types": (400, 364)}                    # (tickets, correct)
after = {"old types": (300, 276), "new type": (100, 68)}
acc = lambda d: sum(c for _, c in d.values()) / sum(t for t, _ in d.values())
print(f"before {acc(before):.2%}  after {acc(after):.2%}")
print(f"old types: {364 / 400:.1%} -> {276 / 300:.1%}   new type: {68 / 100:.0%}   new-type share {100 / 400:.0%}")
assert acc(before) == 0.91 and acc(after) == 0.86
assert 276 / 300 == 0.92 and 68 / 100 == 0.68
# exact decomposition of the 5-point drop (reference = old accuracy 91%)
new_part = 0.25 * (0.68 - 0.91)      # new ticket type
old_part = 0.75 * (0.92 - 0.91)      # old ticket types
print(f"new type {new_part:+.4f}  old types {old_part:+.4f}  total {new_part + old_part:+.4f}")
assert abs(new_part + old_part - (0.86 - 0.91)) < 1e-12
assert abs(new_part) > 5 * abs(old_part)
```

**Output (my run):**
```text
drop 0.050  z 2.22  two-sided p 0.0267  95% CI for the drop [0.006, 0.094]
tickets per week for 80% power at a 5-point drop: 635
false 'decline' weeks when nothing changed: 0.052  (about 1 in 19 weeks)
before 91.00%  after 86.00%
old types: 91.0% -> 92.0%   new type: 68%   new-type share 25%
new type -0.0575  old types +0.0075  total -0.0500
```

**Follow-ups:**
- Would you act at p = 0.027? Not on the p-value. If the new segment is a real coverage gap, act now with a cheap, reversible step; if no cause is found, collect another week of stratified labels before a costly change.
- How do you cut the false alarms from weekly checks? Use a baseline of several weeks, a control chart or a sequential test, and require the drop to hold for two weeks or to show in a named segment.
- What if reviewers disagree 8% of the time? Then accuracy against one reviewer is noisy by itself; measure agreement, use two reviewers on a subset, and treat accuracy changes smaller than the disagreement with care.

**Common mistakes:** Calling it a decline or noise from the headline numbers alone. Ignoring that the launch changed the ticket mix. Forgetting that repeated weekly checks produce false alarms. Using one baseline week. Skipping the cost of each error type.

### Q33 ⭐⭐ 🟡 A vision model that reads documents from phone photos has lost accuracy since a popular new phone with a different camera pipeline became common among your users. Explain how you would find this from the data, estimate its size, decide between augmentation, targeted data collection and a threshold change, and monitor for the next device shift.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** I would tag every upload with its device model, show that accuracy fell only where the new phone is common, size the gap on a small human-labelled audit, and then pick the cheapest fix that holds: a threshold change now, targeted data and augmentation next.

**Clarifying questions:**
- Do we log the device model (EXIF or user agent) and image properties (resolution, blur, HDR or night mode, compression) with each upload? Why: without it the cause is a guess.
- Do we have labels for current uploads (human review, downstream corrections, user edits)? Why: accuracy by device needs ground truth, even a small audit.
- What is the cost of an error versus a manual review? Why: it decides between a higher threshold and more training data.
- How fast can we collect and label new-phone images and ship a retrain? Why: if it takes weeks, a threshold change is the stopgap.
- Is the model's confidence calibrated and logged? Why: a threshold change only works if the score separates good from bad reads.

**Approach:**
1. Find it from data. Slice accuracy (or a proxy such as confidence, field-level agreement, user corrections) by device model and week. A rising device share with a falling overall number, while old devices stay flat, is the signature (see Code).
2. Look for the mechanism: compare image statistics between phones (resolution, sharpness, noise, colour, aggressive smoothing, HDR, a new default format such as HEIC). Look at failure examples by hand.
3. Size it: audit a few hundred labelled uploads per group, take the accuracy gap with a bootstrap interval, then overall loss = share of new phone x gap. This also says what happens as the share grows.
4. Choose the fix:
   - Threshold change (stopgap, hours): raise the confidence threshold for this device so fewer bad reads auto-process; cost is more manual review (the Code run shows the trade).
   - Augmentation (days): simulate the new pipeline's look (sharpening, denoise, colour curve, compression) on existing images; cheap but only as good as the simulation.
   - Targeted data collection (weeks): get real images from the new phone, label them, and fine-tune; best accuracy, slowest. Use it when the gap is large and the device share is growing.
5. Check the fix on a held-out set from the new phone and on the old phones (no regression), then canary.
6. Monitor for the next shift: device-model share (alert when a new model passes a small share such as 5%), per-device confidence distribution, image-quality statistics, and a rolling labelled audit sample per device group.

**Metrics:**
- Accuracy by device group = correct reads / audited uploads in the group, with an interval.
- Overall loss = (share of the group) x (accuracy of old minus accuracy of group).
- Automation rate = uploads auto-processed / all uploads; accuracy of the auto-processed set; manual-review rate.
- Drift signals: device share, PSI or distance on confidence and image statistics per device.
- Guardrails: old-device accuracy (no regression), review queue time, cost per document.

**Risks:**
- Confounding: users with the new phone may differ (documents, lighting, app version), not only the camera.
- An audit with too few labels (300 per group gives a gap interval about plus or minus 5 points wide on each side, see Code).
- Augmentation that does not look like the real pipeline can raise training metrics and change nothing in production.
- Raising the threshold quietly overloads the manual queue.
- Over-fitting to one phone and missing the next.

**What the interviewer scores:**
- Strong: starts from the data (device tag, slice, share versus accuracy) and proves it is the device.
- Strong: gives the size as share x gap and says it will grow with adoption.
- Strong: ranks the fixes by speed and durability and states the cost of each.
- Weak: "retrain with more data" with no diagnosis, or no plan for the next device.
- Cross-reference: Book 4 Part 8 has "Monitoring models on unstructured data (images, text, embeddings) at the Part 8 level" for the monitoring side.

**Example:** (illustrative numbers) 5,000 uploads a week. Old phones read correctly 95% of the time; the new phone 80%. At a 30% share, overall accuracy = 0.70 x 0.95 + 0.30 x 0.80 = 90.5%, versus about 95% with no new phone, a 4.5-point loss. At a 2% share the loss is only 0.3 points, which is why nobody noticed. Weak answer: "Accuracy is down, retrain on recent data." Strong answer: "Overall dropped because the new phone share grew; old phones are flat. It is a 15-point gap on 30% of traffic. Today I raise the threshold for that device, this week I add augmentation, and I collect labelled images from the phone for the real fix."

**Code:**
```python
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
```

**Output (my run):**
```text
week  new-phone share  overall  old phones
   0              2%    94.7%       95.2%
   5             15%    92.3%       94.5%
  11             30%    90.2%       95.2%
audit gap old-new 0.137, bootstrap 95% [0.090, 0.190]
overall accuracy loss at 30% share: 0.045
new-phone uploads: threshold -> share auto-processed, accuracy of auto-processed
  0.50  85.1%  88.1%
  0.70  60.2%  94.3%
  0.85  29.7%  98.1%
going 0.50 -> 0.85 sends 55.5% more of new-phone uploads to manual review
week the new phone crosses 5% share: 2  (share 7.1%)
```
The run shows overall accuracy sliding from about 94.7% to 90.2% while old phones stay near 95%, an audit gap near 13.7 points (interval 9 to 19), and a threshold move from 0.50 to 0.85 sending about 55% more new-phone uploads to manual review in this simulation.

**Follow-ups:**
- The device tag is not logged. What now? Use proxies (image resolution, EXIF if kept, user-agent, app version), cluster images on simple statistics, and add the tag to the logs from today.
- Why not only augment? It only works if the simulation matches the real pipeline; always verify on real labelled images from the phone.
- How do you stop this recurring? A device-share alert, a per-device audit sample, and a standing process to collect labelled images when a new model passes a small share.

**Common mistakes:** Treating the overall average as the problem. Retraining on a random recent sample that has few new-phone images. Raising the threshold without costing the manual queue. Checking only the new device and missing regressions on old ones. No device-level monitoring afterwards.

### Q34 ⭐⭐ 🟡 A summarisation feature's human rating slipped from 4.3 to 3.9 out of 5 after a developer edited the shared prompt template to fix one customer complaint, and neither the prompt nor the model version was recorded with each output. Explain how you would find out what changed, what a frozen regression set and prompt versioning would have shown, and how to ship prompt edits safely.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** I would date the drop from rating timestamps, match it against the deploy and git history of the template, rebuild the old prompt and compare old versus new on a fixed set of inputs, and from now on version every prompt and gate every edit on a frozen regression set.

**Clarifying questions:**
- How are ratings collected (human raters, users, an LLM judge), and did the rubric or raters change? Why: a rating change is not always a quality change.
- Is the template in version control, and do we have deploy timestamps and old copies (git history, config store, cached copies)? Why: it decides whether I can rebuild the old prompt exactly.
- Is the template shared by several features or customers? Why: one customer's fix can hurt the others, which is probably what happened.
- Did the base model, retrieval or input mix change in the same weeks? Why: the prompt edit is the prime suspect, not the only one.
- Do we keep inputs and outputs (with consent) so I can replay them? Why: replay is the cleanest test.

**Approach:**
1. Check the number: 4.3 to 3.9 is a 0.4-point drop (9.3% of 4.3). With a 0.9 standard deviation per rating you need about 80 ratings per group to see it, so it is detectable on normal volumes. Confirm raters and rubric are unchanged.
2. Date it. With no version logged, find the change day from the daily mean ratings with a simple two-level fit (the Code run recovers the true day). Then match the date with deploy logs, git history of the template and the model provider's release notes.
3. Rebuild both prompts (old from history, new from the repo) and replay the same fixed inputs through both with the same model and settings. Judge both with the same raters or judge. Compare paired: same input, two prompts.
4. Break the change down: by input category, length and customer. A fix for one complaint usually helps one category and hurts the others.
5. Decide: keep the edit only for the segment that needs it (a separate template or a conditional section), or revert and fix the complaint another way.
6. What a frozen regression set and versioning would have shown: the paired drop (about -0.4 with an interval below zero), plus the category that improved (the complaint) and the four that got worse, before the edit ever shipped.
7. Ship prompt edits safely: prompts in version control; a version id and model id logged with every output; a frozen regression set (150 to 300 fixed inputs across categories, including every past complaint); a gate (mean must not drop and no category may fall more than a set amount); then a canary or A/B on a share of traffic, with a one-click rollback.

**Metrics:**
- Mean rating = sum of ratings / number of rated outputs, per day, per category, per prompt version.
- Paired change = mean over regression items of (new score minus old score), with a bootstrap interval.
- Category worst-case change = the lowest category mean change (gate on it, not just the average).
- Guardrails: length, refusal rate, format-valid rate, latency and cost per output.

**Risks:**
- Judge or rater drift looks like a prompt effect; use the same judge on both prompts and a fixed rubric.
- The regression set must be frozen and must cover the long tail; if it never includes the complaint type it cannot catch it.
- Overfitting the prompt to the regression set.
- A model-provider update at the same time hides which change caused the drop.
- Replay with different temperature or model settings.

**What the interviewer scores:**
- Strong: treats the prompt like code (version, test, gate, canary, rollback) and logs prompt and model version per output.
- Strong: uses paired comparison on fixed inputs and breaks the result down by category.
- Strong: dates the change from the data when versions are missing, and treats the date as a lead.
- Weak: "ask the developer to revert" with no measurement, or "we need more data".
- Cross-reference: Book 4 Part 8 has "LLM and GenAI monitoring, only at the boundary with Book 2" for the monitoring side.

**Example:** (illustrative numbers) Frozen set: 150 inputs, 30 each in five categories. The edit lifts the complaint-type category by 0.4 and lowers the others by 0.46, 0.91, 0.51 and 0.60 points in this simulation. Average change: -0.41, interval about -0.51 to -0.32. The gate (no category below -0.3) fails, so the edit would not ship as written. Weak answer: "Ratings dropped, revert the prompt." Strong answer: "Date the drop, replay old versus new on a fixed set, show it helps one category and hurts four, then ship a category-specific fix through the gate."

**Code:**
```python
# Q34: summary rating slipped 4.3 -> 3.9 after an unversioned prompt edit (illustrative simulation)
import numpy as np

rng = np.random.default_rng(34)
assert round(4.3 - 3.9, 1) == 0.4 and round((4.3 - 3.9) / 4.3, 3) == 0.093

# 1. No version was logged: find WHEN it changed from daily mean ratings (60 days, 40 rated per day)
days, per_day, change_day = 60, 40, 33
daily_mean = []
for d in range(days):
    mu = 4.3 if d < change_day else 3.9
    r = np.clip(np.round(rng.normal(mu, 0.9, per_day)), 1, 5)
    daily_mean.append(r.mean())
daily_mean = np.array(daily_mean)
def sse(k):  # two-level fit with a break before day k
    return ((daily_mean[:k] - daily_mean[:k].mean()) ** 2).sum() + ((daily_mean[k:] - daily_mean[k:].mean()) ** 2).sum()
best = min(range(5, days - 5), key=sse)
print(f"estimated change day {best} (true {change_day});  mean before {daily_mean[:best].mean():.2f}  after {daily_mean[best:].mean():.2f}")
assert abs(best - change_day) <= 2
# the date is only a lead: match it against deploy logs / git history of the template

# 2. Frozen regression set: 150 fixed inputs in 5 categories, same judge, old vs new prompt (paired)
cats = ["complaint-type", "short", "long", "technical", "legal"]
cat_of = np.repeat(np.arange(5), 30)
base = rng.normal(4.3, 0.5, 150)                    # item difficulty carried across prompts
effect = np.array([+0.6, -0.5, -0.9, -0.7, -0.6])   # the edit helps one case, hurts four
old = np.clip(base + rng.normal(0, 0.3, 150), 1, 5)
new = np.clip(base + effect[cat_of] + rng.normal(0, 0.3, 150), 1, 5)
diff = new - old
boot = [rng.choice(diff, 150).mean() for _ in range(4000)]
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"paired mean change {diff.mean():+.2f}  95% bootstrap [{lo:+.2f}, {hi:+.2f}]")
for c in range(5):
    print(f"  {cats[c]:15} {diff[cat_of == c].mean():+.2f}")
assert hi < 0 and diff[cat_of == 0].mean() > 0 and diff[cat_of == 2].mean() < -0.5
# average of the effects: (0.6 - 0.5 - 0.9 - 0.7 - 0.6) / 5
assert abs(effect.mean() - (-0.42)) < 1e-9

# 3. Why a frozen set beats waiting for live ratings: sample sizes for a 0.4 shift
sd = 0.9
n_live = 2 * (1.96 + 0.8416) ** 2 * sd ** 2 / 0.4 ** 2    # independent groups
sd_diff = diff.std(ddof=1)                                 # paired: only the prompt effect + noise
n_paired = (1.96 + 0.8416) ** 2 * sd_diff ** 2 / 0.4 ** 2
print(f"ratings needed for 80% power at a 0.4 shift: unpaired {n_live:.0f} per group, paired {n_paired:.0f} items")
assert n_live > 4 * n_paired

# 4. Ship gate: block a prompt version if any category drops more than 0.3 or the mean drops at all
def gate(d, cat, tol=0.3):
    worst = min(d[cat == c].mean() for c in range(5))
    return bool(d.mean() >= 0 and worst >= -tol)
print("gate passes for the edited prompt:", gate(diff, cat_of))
assert gate(diff, cat_of) is False and gate(np.zeros(150), cat_of) is True
```

**Output (my run):**
```text
estimated change day 33 (true 33);  mean before 4.20  after 3.83
paired mean change -0.41  95% bootstrap [-0.51, -0.32]
  complaint-type  +0.40
  short           -0.46
  long            -0.91
  technical       -0.51
  legal           -0.60
ratings needed for 80% power at a 0.4 shift: unpaired 79 per group, paired 17 items
gate passes for the edited prompt: False
```
In this run the break day is recovered exactly (33), the paired change is about -0.41 with an interval below zero, one category rose and four fell, and the paired design needs about 17 items to see a 0.4 shift where unpaired live ratings need about 79 per group.

**Follow-ups:**
- Nothing in history, the old prompt is lost. Reconstruct it from cached requests, logs or the last good outputs; if truly gone, write a candidate and judge it against old outputs for the same inputs.
- Is an LLM judge enough? As a gate yes if you calibrate it against human ratings on a sample and watch for judge drift; keep a small human check.
- How do you stop edits for one customer hurting others? Per-customer or per-category template sections, plus the gate across all categories.

**Common mistakes:** No version logged with the output. Comparing different inputs instead of paired replay. Looking at the average only and missing the category that rose. Treating a prompt as a config tweak. Gating on a set that does not contain the complaint types.

### Q35 ⭐⭐ 🔴 A model scored an AUC of 0.95 offline, but live AUC is 0.71. A review finds one feature was only populated after the outcome happened, so it leaked at training time but is empty at serving time. Explain how you would confirm leakage, quantify the damage, rebuild the evaluation to be point-in-time correct, and handle the live system while you fix it.
**Asked at:** Training-serving skew and offline-versus-online question pages (DesignGurus 'Grokking the AI System Design Interview', techinterview.org MLOps drift and feature-store guide, a Prachub ML-serving concept page); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** An offline AUC of 0.95 that becomes 0.71 live, with one feature that only exists after the outcome, is classic target leakage; I would prove it with timestamps and an ablation, report the honest number (about the clean-model AUC), rebuild the evaluation with point-in-time joins, and switch the live system to a clean model or a rule fallback now.

**Clarifying questions:**
- Which feature is it, and which system writes it and when? Why: the write time is the proof, and it tells me what the legitimate version of the feature would be.
- What is the prediction moment (application time, transaction time, request time)? Why: every feature must be known at that moment, and nothing else counts.
- What decisions use the score today, and at what threshold? Why: an empty feature shifts every score, so the thresholds are now wrong.
- Is there a previous model or a rule set we can fall back to, and how long does a clean retrain take? Why: it decides the interim plan.
- Which other models or features share the same source table or join? Why: leakage tends to repeat through the same pipeline.

**Approach:**
1. Confirm leakage with three checks: (a) timestamps: for each row compare the feature's write time with the prediction time (in the Code run 98% of rows are written after); (b) single-feature strength: a feature that alone has AUC 0.95 for a hard problem is suspect; (c) ablation: drop it and retrain; offline AUC falls to the live level.
2. Quantify the damage. The honest performance is the clean-model AUC (0.705 in the run), not 0.95. Also compute what the live system did wrong: with the feature empty, the old model's scores collapse (mean predicted risk 0.027 versus a true rate 0.286 here), so at the old threshold almost nothing is flagged.
3. Rebuild evaluation, point-in-time correct: join features by "latest value at or before the prediction time" (an as-of join), not "latest value ever"; split by time, not at random; run a leakage test in the pipeline (feature timestamp must not be after the prediction time).
4. Handle the live system. Immediately: roll back to the last model that did not use the feature or to a rule-based fallback; or retrain without the feature and ship it behind a shadow run; recalibrate thresholds on live outcomes because the score distribution changed. Tell the business the true number and the period of exposure.
5. Fix the cause: block the post-outcome source from the feature store for training, add the leakage check to CI, and review sibling models for the same pattern.
6. Look for a legitimate substitute: a version of the signal that exists at prediction time (for example a previous-case value, or an earlier-stage field).

**Metrics:**
- Leak rate = rows where feature write time is after prediction time / all rows.
- Single-feature AUC and the offline AUC drop when the feature is removed.
- Honest AUC = AUC of a point-in-time model on a time-based holdout, and AUC on live matured labels.
- Operational: flag rate, precision and recall at the live threshold, mean score versus observed rate.

**Risks:**
- Believing the clean offline number is already good: re-check on a time split with as-of joins; other leakage may remain.
- Imputing the missing feature (zero, median) and shipping silently, which is what made the live scores collapse.
- Fixing only this feature while the join logic that caused it stays.
- Changing the threshold on the leaky model instead of replacing it.
- Late labels: live AUC is measured on matured labels only.

**What the interviewer scores:**
- Strong: proves leakage with timestamps and ablation, not only a hunch from the AUC gap.
- Strong: separates "what we reported" from "what is true" and states the exposure window.
- Strong: gives an interim plan for the live system (rollback or fallback, thresholds) before the long fix.
- Weak: "retrain the model" without recognising the feature cannot exist at serving time.
- Cross-reference: Book 4 Part 9 has "Point-in-time correct joins" for the feature-store mechanics, and Book 4 Part 1 has "Write tests that catch data leakage" for the test.

**Example:** (illustrative numbers) Offline: AUC 0.96 with the leaky feature. Without it: 0.705, the same as live (0.705 in the run). A tiny as-of join case: user 1 has feature values 100 (day 10), 200 (day 20) and 300 (day 30); the prediction is at day 22. "Latest value ever" gives 300 (a future value); as-of gives 200. Weak answer: "Retrain and hope live improves." Strong answer: "The feature is written after the outcome, so the true AUC is about 0.70. I roll back to the previous model, rebuild training with an as-of join and a time split, add a timestamp check to CI, and recalibrate thresholds."

**Code:**
```python
# Q35: a feature that exists only after the outcome leaks offline and is empty live (illustrative simulation)
import numpy as np
import pandas as pd
from scipy.stats import rankdata

rng = np.random.default_rng(35)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit_logit(X, y, l2=1e-3, steps=40):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(steps):
        p = 1 / (1 + np.exp(-Xb @ w)); g = Xb.T @ (p - y) + l2 * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + l2 * np.eye(len(w))
        w -= np.linalg.solve(H, g)
    return w
def score(w, X): return np.c_[np.ones(len(X)), X] @ w

N = 60_000
legit = rng.normal(size=(N, 3))
y = (legit @ np.array([0.9, 0.6, 0.4]) + rng.normal(0, 2.4, N) > 1.5).astype(int)
# leaky feature: written by the process that happens AFTER the outcome (e.g. a 'case closed' amount)
leak = y * rng.normal(1.0, 0.42, N) + (1 - y) * rng.normal(0.0, 0.42, N)
train, test = slice(0, 40_000), slice(40_000, N)

# 1. Offline with the leaky feature
X_all = np.c_[legit, leak]
w_all = fit_logit(X_all[train], y[train])
offline = auc(y[test], score(w_all, X_all[test]))
# 2. Live: the feature is empty (filled with 0 by the pipeline)
X_live = np.c_[legit, np.zeros(N)]
live = auc(y[test], score(w_all, X_live[test]))
# 3. Clean model, no leaky feature
w_cl = fit_logit(legit[train], y[train])
clean = auc(y[test], score(w_cl, legit[test]))
print(f"offline AUC (with leak) {offline:.3f}   live-like AUC (feature empty) {live:.3f}   clean model {clean:.3f}")
assert offline > 0.93 and 0.68 < live < 0.80 and clean > live - 0.02

# Confirm leakage: single-feature AUC, and ablation
print(f"single-feature AUC: leak {auc(y, leak):.3f}   best legit {max(auc(y, legit[:, j]) for j in range(3)):.3f}")
print(f"ablation: dropping the leaky feature changes offline AUC by {clean - offline:+.3f}")
assert auc(y, leak) > 0.85 and clean < offline - 0.15

# Time check: share of rows whose feature timestamp is after the prediction time
t_pred = rng.uniform(0, 100, N)
t_feat = np.where(rng.random(N) < 0.98, t_pred + rng.uniform(0.1, 5, N), t_pred - 1)   # 98% written later
after = (t_feat > t_pred).mean()
print(f"rows where the feature is written after the prediction time: {after:.1%}")
assert after > 0.97

# Point-in-time (as-of) join versus the leaky 'latest value' join
events = pd.DataFrame({"user": [1, 1, 1, 2, 2], "ts": [10, 20, 30, 15, 25], "val": [100, 200, 300, 50, 60]})
labels = pd.DataFrame({"user": [1, 2], "ts": [22, 20]})                       # prediction times
latest = events.sort_values("ts").groupby("user")["val"].last()               # leaky
asof = pd.merge_asof(labels.sort_values("ts"), events.sort_values("ts"), on="ts", by="user")
print("latest-value join:", latest.to_dict(), "  as-of join:", dict(zip(asof.user, asof.val)))
assert latest.to_dict() == {1: 300, 2: 60} and dict(zip(asof.user, asof.val)) == {1: 200, 2: 50}

# Live handling: the old leaky model's scores shift when the feature is empty
s_off = 1 / (1 + np.exp(-score(w_all, X_all[test]))); s_live = 1 / (1 + np.exp(-score(w_all, X_live[test])))
print(f"mean predicted risk offline {s_off.mean():.3f} vs live-like {s_live.mean():.3f}; true rate {y[test].mean():.3f}")
assert s_live.mean() < 0.5 * s_off.mean()
# decisions at the old threshold of 0.5: how many cases get flagged, and how many true cases are found
for name, s_ in (("offline", s_off), ("live-like", s_live)):
    f = s_ > 0.5
    print(f"{name:10} flagged {f.mean():.1%}  recall {(f & (y[test] == 1)).sum() / y[test].sum():.1%}")
assert (s_live > 0.5).mean() < 0.3 * (s_off > 0.5).mean()
```

**Output (my run):**
```text
offline AUC (with leak) 0.961   live-like AUC (feature empty) 0.705   clean model 0.705
single-feature AUC: leak 0.954   best legit 0.656
ablation: dropping the leaky feature changes offline AUC by -0.256
rows where the feature is written after the prediction time: 98.0%
latest-value join: {1: 300, 2: 60}   as-of join: {2: 50, 1: 200}
mean predicted risk offline 0.287 vs live-like 0.027; true rate 0.286
offline    flagged 27.2%  recall 81.3%
live-like  flagged 0.0%  recall 0.0%
```
The run shows the pattern in the prompt in a simulation: offline 0.961 and live-like 0.705, equal to the clean model; one feature with an AUC of 0.954 alone; 98% of rows where the feature is written after the prediction time; and the old model flagging 27.2% of cases offline but about none live-like.

**Follow-ups:**
- Could the live AUC still be hurt beyond the missing feature? Yes: the model gave the leaky feature most of its weight, so the other weights are not tuned for live; a clean retrain is usually better than the old model with the feature blanked.
- How do you prevent it? Event-time on every feature, as-of joins only, time-based splits, a CI check that fails if a feature timestamp is later than the label's prediction time, and a review of any feature with a suspiciously high single-feature AUC.
- Is it still useful as a signal? Only if a version exists at prediction time; otherwise drop it.

**Common mistakes:** Random train-test split on time-ordered data. "Latest value" joins. Filling the missing feature with zero and moving on. Reporting 0.95 for a month after the review. Fixing the threshold instead of the model.

### Q36 ⭐⭐ 🔴 A model trained on metro-city customers is launched in smaller cities and its precision falls from 62% to 48% in the new region, while the original cities hold steady. Explain how you would test whether covariate shift or a different relationship to the outcome is responsible, and whether you would reweight, add regional features, fine-tune or build a separate model.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** First I would check how much of 62% to 48% a lower base rate alone explains, then use a small labelled sample from the new region to test whether reweighting the metro data to look like the new region reproduces the new precision (covariate shift) or leaves a gap (a different relationship); the answer picks the fix.

**Clarifying questions:**
- Is "precision" at a fixed threshold, and are labels in the new region defined and delayed the same way as in the metro cities? Why: a different label process looks like a different relationship.
- Do we have any labelled rows from the new region, and how many? Why: without them I can only test covariate shift, not the relationship.
- What differs in the new region: customer mix, product, channels, income, language, data sources, device? Why: it suggests features that carry the shift.
- Is the base rate of the outcome different in the new region? Why: precision falls when prevalence falls even if the model is unchanged.
- How many smaller regions are planned, and are they alike? Why: it decides one regional model versus per-region handling.

**Approach:**
1. Arithmetic first. Precision odds equal (TPR / FPR) times prevalence odds. If TPR and FPR did not change, 62% to 48% means prevalence odds fell by a factor 0.566, for example a base rate of 20% falling to 12.4%. So check the base rate before blaming the model.
2. Test covariate shift. Train a domain classifier (metro versus new region) on the features. If it separates them well, the feature distributions differ. Reweight metro rows with weights p/(1-p) from that classifier and compute the reweighted metro precision.
3. Read the result. If the reweighted metro precision is close to the actual new-region precision, the cause is covariate shift (the model is fine, the mix changed). If a gap remains, the relationship between features and outcome is different (concept shift), or the labels differ. In the simulation: scenario A (covariate shift only) leaves a 1.7-point gap, scenario B (different relationship) leaves 13.4 points.
4. Choose the fix:
   - Covariate shift only: reweight training, add or recalibrate features that carry the shift, and re-pick the threshold for the new mix; no new model needed.
   - Different relationship with a few labels: add a region flag or regional offset to the shared model, or recalibrate (cheap, uses all the data).
   - Different relationship with plenty of labels: fine-tune on the new region or build a separate model; with too few rows a separate model is worse than the metro model (the run shows 200 rows lose).
5. Check on a held-out new-region sample and confirm the metro cities do not regress; then canary.
6. Monitor per region from now on: precision on a rolling label sample, base rate, score distribution.

**Metrics:**
- Precision = true positives / flagged, per region at the same threshold; also recall and flag rate.
- Base rate = positives / cases, per region.
- Domain-classifier AUC (how separable the regions are); reweighted metro precision minus actual new-region precision (the unexplained gap).
- Log loss or calibration on the new region; guardrail: metro precision.

**Risks:**
- Importance weights can explode when regions barely overlap; clip them and check the effective sample size.
- Small labelled samples in the new region: a precision of 48% from 100 flagged cases has an interval of roughly plus or minus 10 points.
- Reweighting only fixes shift in the features you observe; unobserved differences look like concept shift.
- Different labelling (a slower or stricter review) can mimic a changed relationship.
- Both effects can be present at once.

**What the interviewer scores:**
- Strong: separates prior (base rate), covariate and concept shift, and tests them in a fixed order with cheap checks.
- Strong: names a concrete test (domain classifier plus reweighted evaluation) and what each outcome means.
- Strong: picks the fix by data availability (few labels: offset or recalibration; many: fine-tune or separate model).
- Weak: "just retrain on the new region's data" with no diagnosis and no thought about how many labels exist.
- Cross-reference: Book 4 Part 8 has "Label (prior) shift versus covariate shift in practice" and "Detecting concept drift" for the monitoring side.

**Example:** (illustrative numbers) Metro base rate 20%, new region 12.4%, same TPR and FPR: precision falls from 62% to 48% with no change in model quality. Now suppose the base rates match. You label 300 flagged cases in the new region and find 49% precision; the metro cases reweighted to look like the new region's features score 62%. The 13-point gap is a different relationship, so a regional offset or fine-tune is needed. Weak answer: "Precision fell, retrain on the new region." Strong answer: "First check the base rate, then reweight and compare; if reweighted metro still beats actual by more than the noise, the relationship differs and I add a region offset or fine-tune depending on label counts."

**Code:**
```python
# Q36: precision 62% -> 48% in smaller cities: covariate shift or a different relationship? (illustrative simulation)
import numpy as np

rng = np.random.default_rng(36)

# 0. Arithmetic first: how much of 62% -> 48% could a lower base rate explain alone?
odds = lambda p: p / (1 - p)
ratio = odds(0.48) / odds(0.62)
print(f"precision odds ratio 0.48 vs 0.62: {ratio:.3f}")
# precision odds = (TPR / FPR) x (prevalence odds); if TPR and FPR are fixed, prevalence odds must fall by that ratio
prev_new = lambda prev_old: (odds(prev_old) * ratio) / (1 + odds(prev_old) * ratio)
print(f"a base rate of 20% falling to {prev_new(0.20):.1%} gives the same precision drop")
assert abs(prev_new(0.20) - 0.1239) < 0.001

def sig(z): return 1 / (1 + np.exp(-z))
def fit(X, y, steps=30, l2=1e-3):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(steps):
        p = sig(Xb @ w); g = Xb.T @ (p - y) + l2 * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + l2 * np.eye(len(w)); w -= np.linalg.solve(H, g)
    return w
pred = lambda w, X: sig(np.c_[np.ones(len(X)), X] @ w)

def world(shift_x, shift_rel, n=60_000):
    """metro: x ~ N(0,1) two features, y depends on x. new: x shifted (covariate) and/or coefficients changed (concept)."""
    beta = np.array([1.2, 0.8]); b0 = -2.2
    Xm = rng.normal(0, 1, (n, 2)); ym = rng.random(n) < sig(b0 + Xm @ beta)
    Xn = rng.normal(shift_x, 1, (n, 2))
    beta_n = beta * shift_rel[0]; b0n = b0 + shift_rel[1]
    yn = rng.random(n) < sig(b0n + Xn @ beta_n)
    return Xm, ym.astype(float), Xn, yn.astype(float)

def diagnose(name, shift_x, shift_rel, keep=False):
    Xm, ym, Xn, yn = world(shift_x, shift_rel)
    global LAST; LAST = (Xm, ym, Xn, yn)
    w = fit(Xm[:40_000], ym[:40_000]); th = 0.5
    flag_m = pred(w, Xm[40_000:]) > th; flag_n = pred(w, Xn) > th
    prec_m = ym[40_000:][flag_m].mean(); prec_n = yn[flag_n].mean()
    # domain classifier: can x tell the two regions apart?
    Xd = np.r_[Xm[:20_000], Xn[:20_000]]; yd = np.r_[np.zeros(20_000), np.ones(20_000)]
    wd = fit(Xd, yd); dp = pred(wd, Xd)
    # importance weights for metro rows, then reweighted metro precision on the flagged rows
    pm = pred(wd, Xm[40_000:]); wgt = pm / (1 - pm); wgt = np.clip(wgt, 0, 20)
    prec_rw = (wgt[flag_m] * ym[40_000:][flag_m]).sum() / wgt[flag_m].sum()
    print(f"{name:34} metro {prec_m:.1%}  new {prec_n:.1%}  metro reweighted to new covariates {prec_rw:.1%}")
    return prec_m, prec_n, prec_rw

a = diagnose("A covariate shift only", -1.0, (1.0, 0.0))
b = diagnose("B different relationship", 0.0, (0.85, -0.25))
# A: reweighting explains most of the new precision; B: reweighting does not
gap_a = abs(a[2] - a[1]); gap_b = abs(b[2] - b[1])
print(f"unexplained gap after reweighting: A {gap_a:.3f}, B {gap_b:.3f}")
assert gap_a < 0.03 and gap_b > 0.10

# Fix options for world B, using a small labelled sample from the new region (2,000 rows)
Xm, ym, Xn, yn = LAST
def logloss(y, p): p = np.clip(p, 1e-6, 1 - 1e-6); return -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()
Xn_tr, yn_tr, Xn_te, yn_te = Xn[:2000], yn[:2000], Xn[2000:], yn[2000:]
w_metro = fit(Xm, ym)
w_region = fit(np.c_[np.r_[Xm, Xn_tr], np.r_[np.zeros(len(Xm)), np.ones(2000)]], np.r_[ym, yn_tr])   # region flag
w_newonly = fit(Xn_tr, yn_tr)
w_new200 = fit(Xn_tr[:200], yn_tr[:200])
res = {
    "metro model as is": logloss(yn_te, pred(w_metro, Xn_te)),
    "metro + region flag (2,000 new rows)": logloss(yn_te, pred(w_region, np.c_[Xn_te, np.ones(len(Xn_te))])),
    "new-region only, 2,000 rows": logloss(yn_te, pred(w_newonly, Xn_te)),
    "new-region only, 200 rows": logloss(yn_te, pred(w_new200, Xn_te)),
}
for k, v in res.items(): print(f"  log loss on new region, {k:38} {v:.4f}")
assert res["metro + region flag (2,000 new rows)"] < res["metro model as is"]
assert res["new-region only, 2,000 rows"] < res["metro model as is"]
assert res["new-region only, 200 rows"] > res["metro model as is"]   # too few rows: worse than the metro model
```

**Output (my run):**
```text
precision odds ratio 0.48 vs 0.62: 0.566
a base rate of 20% falling to 12.4% gives the same precision drop
A covariate shift only             metro 64.5%  new 59.0%  metro reweighted to new covariates 60.7%
B different relationship           metro 62.6%  new 49.2%  metro reweighted to new covariates 62.6%
unexplained gap after reweighting: A 0.017, B 0.134
  log loss on new region, metro model as is                      0.3230
  log loss on new region, metro + region flag (2,000 new rows)   0.3167
  log loss on new region, new-region only, 2,000 rows            0.3156
  log loss on new region, new-region only, 200 rows              0.3370
```
In this simulation covariate shift alone moves precision by about 5 points and leaves a 1.7-point gap after reweighting, while a changed relationship moves it by about 13 points and leaves a 13.4-point gap. The metro-plus-region-flag and new-region-only models (2,000 rows) beat the metro model on new-region log loss; 200 rows are not enough.

**Follow-ups:**
- What if there are no labels from the new region? You can test covariate shift and prior shift only; collect a small labelled sample first (a few hundred reviewed cases is the start) and use a conservative threshold meanwhile.
- When a separate model? When the relationship differs a lot, there are enough labels (thousands), and you will maintain it; otherwise a shared model with regional features is simpler.
- How do you tell prior shift from the others? Compare base rates and calibration by region; prior shift changes precision but leaves TPR and FPR alone.

**Common mistakes:** Not checking the base rate first. Reweighting without clipping. Fine-tuning on 200 rows. Reading one precision number from a small sample as proof. Forgetting to check the original cities after the fix.

### Q37 ⭐⭐ 🔴 A team retrained a model on the last four weeks of data and it performed worse than the old one. Those four weeks included a payment outage and a heavy promotion. Explain how training-window choice, unusual events and label quality could explain this, and how you would design the retraining dataset and validation to avoid repeating it.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** The last four weeks were not normal weeks, so the retrain learned the outage and the promotion as if they were the new normal; I would retrain on a longer window with the outage rows removed or relabelled and the promotion marked, and validate on a time-ordered clean holdout against the old model before shipping.

**Clarifying questions:**
- How are labels defined, and what did the outage do to them (failed payments looking like defaults or abandonment)? Why: this is the likeliest way the window got corrupted.
- Which metric got worse (ranking, calibration, a business metric at a threshold), and on which holdout? Why: AUC can stay flat while the score level moves.
- How was the retrain validated: random split inside the four weeks, or a later period? Why: a random split inside the same four weeks hides the problem.
- Will promotions and outages recur (a calendar, a known event list)? Why: if the promotion recurs, the model should know about it, not forget it.
- How much older data is usable (schema, definitions stable)? Why: it sets how long the window can be.

**Approach:**
1. Diagnose before changing anything. Compare the retrain with the old model on a later clean period, by slice and by day. Check mean predicted versus observed rate, positive rate by day in the training window, feature distributions on promo and outage days.
2. Window choice. Four weeks is short and every unusual day is a large share of it. Use a longer window (for example 6 to 12 months, or all stable history), with recency weights if the relationship drifts, so one odd month cannot dominate.
3. Unusual events. Outage days: drop the rows, or relabel them if the cause is known (a failed payment is not a default). Promotion days: keep them but add a promo indicator (or an event feature), so the model can separate "promo behaviour" from "normal behaviour" and the indicator is off on normal days.
4. Label quality. Look at positive rate by day (the outage days show a spike), at label delay (recent weeks have immature labels), and at how labels are created. Only train on matured labels.
5. Validation. Time-ordered split with a clean future holdout, a second holdout that includes a past promotion, slice checks, and a champion-challenger run on live traffic. The new model must beat or match the old one on log loss, calibration and the business metric at the threshold.
6. Guardrails for the pipeline: an event calendar (outages, promos, launches), an automated check that flags days whose label rate or feature distribution is far from normal, and a rule that a retrain cannot ship if it loses to the champion.

**Metrics:**
- Log loss and Brier score (calibration-sensitive), AUC (ranking), and precision and recall at the live threshold.
- Mean predicted / mean observed rate on the holdout.
- Positive rate by day in the training window (spot corrupted days).
- Business guardrail: cost or approval rate at the live threshold.

**Risks:**
- Too long a window hides a real, recent change (concept drift): use recency weights and a drift check.
- Dropping outage days removes information about outage behaviour; mark them or relabel instead if the system must handle outages.
- A promo indicator that is set differently at serving than in training.
- The holdout shares the same unusual days (leakage in time).
- Immature labels in the most recent days.

**What the interviewer scores:**
- Strong: connects each of the three clues (window, events, labels) to a specific mechanism and shows it in data.
- Strong: a validation design that mirrors production (time split, clean future holdout, champion versus challenger).
- Strong: builds a repeatable process (event calendar, label-rate alerts), not a one-off patch.
- Weak: "use more data" with no check of label quality, or "retrain again next week".
- Cross-reference: Book 4 Part 7 has "Continuous training triggers and their guardrails" and Book 4 Part 8 has "Retraining pitfalls and feedback loops".

**Example:** (illustrative numbers) 30 weeks of data (210 days), 400 rows a day, a training window of the last 4 weeks (28 days, 11,200 rows). Five outage days in the window have a positive rate of 79%, against 31% on normal days. Those 5 days are 5/28 = 17.9% of the window (the run prints the same). The naive retrain predicts 14% too many positives on the clean test weeks (ratio 1.143) while the old model is at 0.974. Weak answer: "The new model is worse, so keep the old one forever." Strong answer: "The four-week window is dominated by an outage and a promo. I would train on 28 weeks, drop or relabel the outage days, add a promo flag, and promote only if it beats the champion on a clean later holdout."

**Code:**
```python
# Q37: retrain on the last 4 weeks, which had a payment outage and a heavy promotion (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(37)
sig = lambda z: 1 / (1 + np.exp(-z))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(X, y, steps=30, l2=1e-3):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(steps):
        p = sig(Xb @ w); g = Xb.T @ (p - y) + l2 * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + l2 * np.eye(len(w)); w -= np.linalg.solve(H, g)
    return w
pred = lambda w, X: sig(np.c_[np.ones(len(X)), X] @ w)
def logloss(y, p): p = np.clip(p, 1e-6, 1 - 1e-6); return -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()

# 30 weeks of daily data, 700 rows a day. Weeks 25-28 = the last four weeks used for the retrain.
days, per = 210, 400
beta = np.array([1.0, -0.8, 0.5]); b0 = -1.0
rows = []
for d in range(days):
    wk = d // 7
    promo = 24 <= wk <= 27 and (d % 7) in (2, 3, 4)           # promo days in the 4-week window
    outage = wk == 26 and (d % 7) in (0, 1, 2, 3, 4)                  # payment outage days
    X = rng.normal(0, 1, (per, 3))
    if promo: X[:, 0] += 1.5                                  # promo-driven shift in feature 0
    y = (rng.random(per) < sig(b0 + X @ beta)).astype(float)
    if outage:                                                # failed payments mislabelled as the positive class
        flip = rng.random(per) < 0.6
        y = np.where(flip, 1.0, y)
    rows.append((np.full(per, d), X, y, np.full(per, promo), np.full(per, outage)))
D = np.concatenate([r[0] for r in rows]); X = np.concatenate([r[1] for r in rows])
Y = np.concatenate([r[2] for r in rows]); P = np.concatenate([r[3] for r in rows]); O = np.concatenate([r[4] for r in rows])
print(f"outage days: {len(np.unique(D[O]))}, promo days: {len(np.unique(D[P]))}, share of training-window rows on outage days: {O[(D >= 168) & (D < 196)].mean():.1%}")

assert abs(O[(D >= 168) & (D < 196)].mean() - 5 / 28) < 1e-9
# Clean test: the next 2 weeks (days 196-209 are normal; train data end before day 196)
test = D >= 196; Xt, Yt = X[test], Y[test]
window = (D >= 168) & (D < 196)
old_w = fit(X[D < 168], Y[D < 168])                       # old model: weeks 1-24
models = {
    "old model (weeks 1-24)": old_w,
    "retrain: last 4 weeks, as is": fit(X[window], Y[window]),
    "retrain: last 4 weeks, outage days dropped": fit(X[window & ~O], Y[window & ~O]),
    "retrain: 28 weeks, outage dropped, promo flag": None,
}
# 28 weeks with outage days dropped, promo flag as a feature (set to 0 at serving on normal days)
tr = (D < 196) & ~O
Xf = np.c_[X, P.astype(float)]
w_flag = fit(Xf[tr], Y[tr])
res = {}; ratio_ = {}
for k, w in models.items():
    if w is None: p = pred(w_flag, np.c_[Xt, np.zeros(len(Xt))])
    else: p = pred(w, Xt)
    res[k] = (auc(Yt, p), logloss(Yt, p))
    print(f"{k:48} AUC {res[k][0]:.4f}  log loss {res[k][1]:.4f}  mean pred/observed {p.mean() / Yt.mean():.3f}")
    ratio_[k] = p.mean() / Yt.mean()
a_old = res["old model (weeks 1-24)"]; a_bad = res["retrain: last 4 weeks, as is"]
a_fix = res["retrain: 28 weeks, outage dropped, promo flag"]
assert a_bad[1] > a_old[1]                      # the naive retrain is worse than the old model on log loss
assert a_fix[1] <= a_old[1] + 0.003             # a careful retrain is at least as good
assert res["retrain: last 4 weeks, outage days dropped"][1] < a_bad[1]
print(f"naive retrain minus old model: log loss {a_bad[1] - a_old[1]:+.4f}")
assert ratio_["retrain: last 4 weeks, as is"] > ratio_["old model (weeks 1-24)"] + 0.02   # inflated base rate
# in the 4-week window the outage and promo days differ from normal days:
print(f"positive rate: normal window days {Y[window & ~O & ~P].mean():.3f}, outage days {Y[window & O].mean():.3f}, test {Yt.mean():.3f}")
assert Y[window & O].mean() > Y[window & ~O & ~P].mean() + 0.1
```

**Output (my run):**
```text
outage days: 5, promo days: 12, share of training-window rows on outage days: 17.9%
old model (weeks 1-24)                           AUC 0.7968  log loss 0.5015  mean pred/observed 0.974
retrain: last 4 weeks, as is                     AUC 0.7969  log loss 0.5082  mean pred/observed 1.143
retrain: last 4 weeks, outage days dropped       AUC 0.7969  log loss 0.5026  mean pred/observed 0.945
retrain: 28 weeks, outage dropped, promo flag    AUC 0.7968  log loss 0.5015  mean pred/observed 0.971
naive retrain minus old model: log loss +0.0068
positive rate: normal window days 0.309, outage days 0.793, test 0.330
```
In this run the ranking (AUC) is the same for every model (about 0.797); the damage is in calibration: the naive four-week retrain over-predicts by 14.3% and has the worst log loss (0.5082 versus 0.5015), and the careful retrain matches the old model.

**Follow-ups:**
- Why did AUC not move? The outage corrupted the level of the labels (the base rate), not the order of the features' effects; that is why a calibration check belongs next to AUC.
- Should the old model stay forever? No; keep it as the champion until a challenger wins a clean comparison, then retrain on a schedule with the event checks.
- What if the promotion repeats monthly? Then keep promo rows and keep the promo flag, and test the model on past promotions.

**Common mistakes:** Validating on a random split of the same four weeks. Training on rows from an outage unchanged. Dropping promo days when promos are part of normal business. Judging the retrain on AUC alone. No event calendar.

### Q38 ⭐⭐ 🔴 A moderation model only gets true labels for items a human reviewer sees, which are mostly those the model already scored as risky. Reported recall has stayed at 90% while user reports of missed harmful content are rising. Explain the selection bias in the monitoring metric and how you would obtain an unbiased estimate, for example with random sampling.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** Recall computed only on items humans reviewed is biased, because reviewers mostly see what the model already flagged, so the metric cannot see what the model misses; I would label a random (or stratified, probability-weighted) sample of all items and estimate recall from that.

**Clarifying questions:**
- How do items reach reviewers (model flag, user report, random, policy list)? Why: each path has a different selection probability, and I need them to weight correctly.
- How is "recall" computed today: harmful items the model flagged / harmful items reviewed? Why: if the denominator is reviewed items only, it is biased by construction.
- How much review capacity do we have, and what does one review cost? Why: it bounds the size of the sample.
- Is harm prevalence low (for example 1 to 3%)? Why: rare harm makes a simple random sample expensive.
- Are the new user reports about a new kind of harm? Why: it suggests the model's blind spot is a specific type or region.

**Approach:**
1. Name the bias. Reviewers see flagged items plus a few borderline ones. Among reviewed harmful items almost all were flagged, so "flagged and harmful / reviewed and harmful" is close to 1 whatever the model misses. Harmful items with low scores are rarely reviewed, so they are missing from the denominator. That is selection bias. In the simulation: reported recall 89.4%, true recall 56.5%.
2. Corroborate with independent signals: user reports of missed content, appeals, reports by trust-and-safety staff, external audits. These are also biased, but they point in a direction (rising reports plus flat recall is the contradiction).
3. Get an unbiased estimate with a random sample: draw items uniformly from everything that was posted (including unflagged), have them reviewed blind, and compute recall as flagged-and-harmful / harmful in the sample, with a confidence interval.
4. Make it cheaper with stratified sampling and inverse-probability weights: sample the strata (flagged, borderline, low score) at different rates and weight each sampled item by 1 / its sampling probability. With the same 20,000 reviews, stratified sampling gave a standard deviation of 1.8 points versus 2.5 for simple random sampling in the run.
5. Keep it running: a small standing random sample (for example a fixed daily quota) so recall is tracked over time, by content type, region and language, and so the next retrain gets unbiased labels.
6. Use the result: find which harm types sit in the missed set, add them to training, and set thresholds using the corrected recall and precision.

**Metrics:**
- True recall = harmful items the model flagged / all harmful items, estimated from a probability sample: sum of weights of flagged harmful sampled items / sum of weights of harmful sampled items.
- Precision stays measurable on flagged items (all are reviewed).
- Reviewed-only recall (the biased one) is reported alongside, labelled as a diagnostic.
- Sample size for a 95% interval of plus or minus 3 points: about 1,049 harmful items in the sample, which is about 52,000 items at a 2% prevalence for simple random sampling (the run computes this).

**Risks:**
- Reviewers who know the model's score label differently: review blind.
- Rare harm: a small random sample may contain few harmful items and give a wide interval.
- Wrong weights: if the reviewed set mixes several routes, compute each item's selection probability correctly.
- Review cost and reviewer exposure to harmful content: cap and support reviewers.
- Time delay: harm reported later changes the label of earlier items.

**What the interviewer scores:**
- Strong: explains why the denominator is biased and that the contradiction (flat recall, rising reports) is a symptom of that.
- Strong: gives an unbiased estimate and its cost (sample size computed), and improves it with stratification and weights.
- Strong: adds a standing process and uses the sample to improve the model.
- Weak: "label more data" with no sampling design, or trusting the 90% figure.
- Cross-reference: Book 4 Part 8 has "Canary labels and label budgets" and "Retraining pitfalls and feedback loops"; Book 1 Part 7 has "Selection bias and counterfactual evaluation" (inverse propensity scoring).

**Example:** (illustrative numbers) 1,000,000 items, 2% harmful = 20,000 harmful. The model catches 56.5% of them (11,300), and misses 8,700. Reviewers see all 11,300 flagged harmful items plus a slice of borderline items that contain only about 1,350 harmful ones, so reported recall is about 11,300 / (11,300 + 1,350) = 89%. A random sample of 20,000 items finds about 400 harmful, of which 56% were flagged: recall about 56% with a standard deviation of 2.5 points. Weak answer: "Recall is 90%, so users are wrong." Strong answer: "The 90% is computed on items the model already likes. I would take a random blind sample, weight it properly, and find the real recall is about 56%."

**Code:**
```python
# Q38: moderation recall measured only on reviewed items is biased (illustrative simulation)
import numpy as np

rng = np.random.default_rng(38)
N = 1_000_000
harm = rng.random(N) < 0.02                       # 2% harmful
new_type = harm & (rng.random(N) < 0.45)          # a new kind of harm the model has not seen (45% of harm)
# model score: old-type harm scores high, new-type harm scores like ordinary content, ordinary items score low
score = np.where(harm & ~new_type, rng.beta(8, 1.5, N), np.where(new_type, rng.beta(2, 4, N), rng.beta(1.2, 6, N)))
flagged = score >= 0.6
true_recall = (flagged & harm).sum() / harm.sum()

# Review policy: all flagged items go to reviewers, plus 30% of items with score 0.3-0.6 (borderline)
mid = (score >= 0.3) & (score < 0.6)
reviewed = flagged | (mid & (rng.random(N) < 0.30))
rep_recall = (reviewed & flagged & harm).sum() / (reviewed & harm).sum()
print(f"true recall {true_recall:.3f}   reported recall (reviewed items only) {rep_recall:.3f}   reviewed {reviewed.sum():,} of {N:,}")
assert rep_recall > true_recall + 0.25 and 0.88 < rep_recall < 0.91

caught = (flagged & harm).sum(); extra = (reviewed & ~flagged & harm).sum()
print(f"harmful total {harm.sum():,}  flagged harmful {caught:,}  harmful seen by reviewers but not flagged {extra:,}")
assert abs(caught - 11_300) < 300 and abs(extra - 1_350) < 150
# Unbiased estimate 1: simple random sample of 20,000 items, reviewed by humans
def srs_estimate(n, seed):
    r = np.random.default_rng(seed); idx = r.choice(N, n, replace=False)
    h = harm[idx]; f = flagged[idx]
    return (f & h).sum() / h.sum(), h.sum()
ests = [srs_estimate(20_000, s) for s in range(200)]
e = np.array([x[0] for x in ests]); nh = np.mean([x[1] for x in ests])
print(f"SRS 20,000: mean harmful found {nh:.0f}; recall estimate mean {e.mean():.3f}, sd across repeats {e.std():.3f}")
assert abs(e.mean() - true_recall) < 0.01

# Unbiased estimate 2: stratified sample with the same budget (20,000), inverse-probability weights
strata = {"flagged": flagged, "mid": mid, "low": score < 0.3}
alloc = {"flagged": 3_000, "mid": 5_000, "low": 12_000}
def strat_estimate(seed):
    r = np.random.default_rng(seed); caught = 0.0; harm_tot = 0.0
    for k, m in strata.items():
        idx = np.flatnonzero(m); take = r.choice(idx, alloc[k], replace=False)
        w = len(idx) / alloc[k]
        h = harm[take]
        harm_tot += w * h.sum()
        if k == "flagged": caught += w * h.sum()
    return caught / harm_tot
es = np.array([strat_estimate(s) for s in range(200)])
print(f"stratified 20,000: recall estimate mean {es.mean():.3f}, sd across repeats {es.std():.3f}")
assert abs(es.mean() - true_recall) < 0.01 and es.std() < e.std()

# How many items does a +-3 point 95% interval need under simple random sampling?
prev = harm.mean()
n_harm = 1.96 ** 2 * true_recall * (1 - true_recall) / 0.03 ** 2
print(f"harmful items needed {n_harm:.0f}; sampled items needed {n_harm / prev:,.0f}")
assert 1000 < n_harm < 1100
```

**Output (my run):**
```text
true recall 0.565   reported recall (reviewed items only) 0.894   reviewed 62,333 of 1,000,000
harmful total 20,038  flagged harmful 11,323  harmful seen by reviewers but not flagged 1,337
SRS 20,000: mean harmful found 399; recall estimate mean 0.566, sd across repeats 0.025
stratified 20,000: recall estimate mean 0.565, sd across repeats 0.018
harmful items needed 1049; sampled items needed 52,352
```
The run reproduces the prompt's pattern in a simulation: reported recall 0.894 against true recall 0.565; the simple random sample (20,000 items, about 399 harmful) recovers 0.566; the stratified design recovers 0.565 with a smaller spread (0.018 versus 0.025); and about 52,000 items would be needed for plus or minus 3 points by simple random sampling.

**Follow-ups:**
- Cheaper than 52,000 reviews? Stratify by model score and oversample the low-score stratum; or run the random sample only for a few strata at a time (rolling by content type).
- Can I fix the biased metric by weighting only the reviewed items? Only if every item has a known, non-zero chance of being reviewed; items with probability zero cannot be recovered, so keep some random review for everyone.
- What if the harm is very rare? Use stratification and sample size by harmful counts (about 1,000 harmful items for plus or minus 3 points), and report the interval honestly.

**Common mistakes:** Computing recall only on reviewed items. Reviewing a random sample but showing reviewers the model score. Using the sample unweighted after a stratified draw. Treating user reports as an unbiased measure. Skipping the interval.

### Q39 ⭐⭐ 🔴 In one week three things changed together: a model release, a large marketing campaign that brought in new users, and an upstream schema update. The conversion model's metric fell 5% and everyone blames a different cause. Explain how you would attribute the drop, which analyses and rollbacks you would use to isolate each cause, and how you would run the incident.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would freeze further changes, decompose the 5% by who (mix) and where (platform, version, feature), and then test each suspect with a targeted experiment: a holdback on the old model for the release, a segment comparison for the campaign, and null-rate checks for the schema change; only then roll back what the evidence blames.

**Clarifying questions:**
- What exactly fell: conversion rate, or a model metric such as AUC or precision? And is "5%" relative or percentage points? Why: it sets the arithmetic and the owner. I would treat it as conversion rate down 5% relative (4.00% to 3.80%).
- What are the exact timestamps of the three changes, and did they roll out gradually or at once? Why: staggered timing separates them; a simultaneous rollout needs a holdback.
- Is there a holdback, shadow traffic or a feature flag for the model release? Why: it is the cleanest way to isolate the model.
- How were campaign users acquired, and can I tag them (channel, campaign id, install date)? Why: mix effects need a cohort label.
- Which fields did the schema update change, and which features use them? Why: it points to a null-rate or unit check.

**Approach:**
1. Run it as an incident: one owner, a shared channel, a freeze on other changes, a timeline of the three changes, and a decision deadline. Rolling back a safe, reversible change early is fine if it is cheap.
2. Decompose the metric into who and what. Split users into existing and new (campaign) users and into platform and version. Mix effect: new users with a different base rate change the average with no change in the model. Rate effect: the same type of user converting differently. The identity is: change = rate change among existing + share of new x (new rate minus existing rate).
3. Isolate the model release: compare old versus new model on the same users in the same week, using a holdback or a shadow run. Use paired or randomised comparison, not before and after.
4. Isolate the schema update: null rate, unit and category changes per feature before and after; compare conversion for rows with and without the affected feature, and check training-serving skew on those features.
5. Isolate the campaign: compare campaign users with comparable organic users, and existing users before and after. If existing users are flat, the campaign is a mix effect, not a model failure.
6. Act on evidence: fix or roll back the schema issue, keep the model if the holdback is clean, and accept (and re-baseline) the mix change; then re-measure. Write a short blameless postmortem with the evidence table.

**Metrics:**
- Conversion = conversions / eligible sessions (or users); report overall and by segment.
- Contribution to change by cause, in percentage points, adding to the total (mix + existing-user rate; within rate, by platform).
- Model effect = conversion with new model minus conversion with old model in a concurrent holdback, with a confidence interval.
- Schema health: null rate and distribution per feature, rows with the feature versus null.
- Guardrails: revenue per session, latency, error rate.

**Risks:**
- Before-and-after comparisons confound all three changes.
- Simpson-like mix effects: every segment can look fine while the total drops.
- A holdback that is too small gives a confidence interval wide enough to blame anything (see Code).
- Rolling back several things at once: you learn nothing and may revert a good change.
- Attribution is not additive if the causes interact; say so.
- Blame culture: people defend their change instead of sharing data.

**What the interviewer scores:**
- Strong: a decomposition that adds up, with numbers, then a targeted test per suspect.
- Strong: knows a holdback or shadow run is the cleanest isolation and states the sample-size limit.
- Strong: runs the incident (owner, freeze, timeline, decision rule, postmortem).
- Weak: rolls back everything, or picks the most likely cause by gut.
- Cross-reference: Book 6 Part 1 has "A 12% drop in orders is concentrated in one metro city and started on a Tuesday" (Q15 in Part 1) for the metric-drop side, and Book 4 Part 8 has "Scenario: your drift dashboard fires an alert for feature X. What do you do, in order?".

**Example:** (illustrative numbers) Conversion fell from 4.00% to 3.80%. Before: 50% iOS at 4.40% and 50% Android at 3.60%. After: 35% existing iOS at 4.40%, 35% existing Android at 3.50%, 30% new campaign users at 3.45%. Existing users average 3.95% versus 4.00% before: a -0.05 point rate effect. New users convert 0.50 points below the existing average on 30% of traffic: -0.15 points mix effect. Total -0.20 points (75% mix, 25% rate). The whole rate effect is Android: 20% of Android rows have a null feature and convert at 3.0%; Android rows with the feature are flat at about 3.6%. A 10% holdback on the old model shows no difference (-0.02 points, interval -0.15 to +0.11). Weak answer: "The model release did it, roll it back." Strong answer: "Three quarters is campaign mix, a quarter is the schema bug on Android, the model is clean; I fix the null feature, keep the model, and set a campaign-specific baseline."

**Code:**
```python
# Q39: three changes in one week, conversion metric -5% (illustrative numbers, hand-checkable)
import numpy as np

# Segment table: (share, conversion %) before and after
before = {"existing iOS": (0.50, 4.40), "existing Android": (0.50, 3.60)}
after = {"existing iOS": (0.35, 4.40), "existing Android": (0.35, 3.50), "new campaign users": (0.30, 3.45)}
tot = lambda d: sum(s * r for s, r in d.values())
b, a = tot(before), tot(after)
print(f"overall conversion {b:.2f}% -> {a:.2f}%  ({a / b - 1:+.1%})")
assert round(b, 2) == 4.00 and round(a, 2) == 3.80 and round(a / b - 1, 3) == -0.05

# Decomposition: existing-user rate change + new-user mix effect
ex_b = (0.50 * 4.40 + 0.50 * 3.60) / 1.0
ex_a = (0.35 * 4.40 + 0.35 * 3.50) / 0.70
new = 3.45; s_new = 0.30
rate_effect = ex_a - ex_b                       # existing users, same people-type, before vs after
mix_effect = s_new * (new - ex_a)               # replacing 30% of traffic by users who convert lower
print(f"existing-user rate effect {rate_effect:+.3f} pp, new-user mix effect {mix_effect:+.3f} pp, sum {rate_effect + mix_effect:+.3f} pp")
assert abs(rate_effect + mix_effect - (a - b)) < 1e-9
assert abs(rate_effect - (-0.05)) < 1e-9 and abs(mix_effect - (-0.15)) < 1e-9
print(f"share of the drop: mix {mix_effect / (a - b):.0%}, existing-user rate {rate_effect / (a - b):.0%}")

# Where is the existing-user rate effect? By platform: iOS flat, Android -0.10 pp
android_drop = 3.50 - 3.60
print(f"existing Android change {android_drop:+.2f} pp; existing iOS change {4.40 - 4.40:+.2f} pp")
assert abs(0.5 * android_drop - rate_effect) < 1e-9     # all of it sits in Android

# Schema suspect: a feature became null for part of Android. Conversion with feature vs null rows
null_share, rate_null, rate_ok = 0.20, 3.00, 3.625
android_after = (1 - null_share) * rate_ok + null_share * rate_null
print(f"Android after = {android_after:.3f}% = 80% x {rate_ok}% + 20% null rows x {rate_null}%")
assert abs(android_after - 3.50) < 1e-9
print(f"Android rows WITH the feature: {rate_ok}% vs {3.60}% before (flat within noise); the drop sits in null rows")

# Model release: a 10% holdback of existing users stayed on the old model during the same week
rng = np.random.default_rng(39)
n_old, n_new, p = 100_000, 900_000, 0.0395             # true rate identical in both arms
c_old = rng.binomial(n_old, p) / n_old; c_new = rng.binomial(n_new, p) / n_new
se = np.sqrt(c_old * (1 - c_old) / n_old + c_new * (1 - c_new) / n_new)
d = c_new - c_old
print(f"holdback test: new model minus old model {d * 100:+.3f} pp, 95% CI [{(d - 1.96 * se) * 100:+.3f}, {(d + 1.96 * se) * 100:+.3f}] pp")
assert abs(d) < 0.001 and (d - 1.96 * se) < 0 < (d + 1.96 * se)
```

**Output (my run):**
```text
overall conversion 4.00% -> 3.80%  (-5.0%)
existing-user rate effect -0.050 pp, new-user mix effect -0.150 pp, sum -0.200 pp
share of the drop: mix 75%, existing-user rate 25%
existing Android change -0.10 pp; existing iOS change +0.00 pp
Android after = 3.500% = 80% x 3.625% + 20% null rows x 3.0%
Android rows WITH the feature: 3.625% vs 3.6% before (flat within noise); the drop sits in null rows
holdback test: new model minus old model -0.023 pp, 95% CI [-0.150, +0.105] pp
```

**Follow-ups:**
- What if there is no holdback? Use a staged rollback or a canary now (roll the model back for a random 10% of traffic), and use pre-period comparisons only as a hint.
- What if the effects interact (the new model is worse on new users)? Estimate the model effect separately for new and existing users in the holdback and report the interaction.
- What do you put in the postmortem? Timeline, evidence table, contribution by cause, what we changed in the release process (no simultaneous risky changes, holdbacks by default, schema contract tests).

**Common mistakes:** Rolling back all three. Comparing only before and after. Reading a segment's percentage change instead of its contribution. Ignoring mix. Letting each owner defend their own change without a shared dashboard.

### Q40 ⭐ 🟡 A fraud model's decisions block flagged transactions, so only the flagged ones gain a quick label. Meanwhile its apparent precision rises over time while missed fraud found by other channels also rises. Explain how to run a small randomised exploration slice to measure the truth, how large it needs to be, and how you would justify its cost to the business.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** If only flagged transactions get quick labels, the model's own metrics look better as it gets narrower, so I would add two small randomised slices: a labelled audit of unflagged traffic (to measure recall and missed fraud) and a capped release of a few flagged transactions (to measure true precision), sized by simple interval maths and priced against the fraud they uncover.

**Clarifying questions:**
- How do labels arise: analyst review of flagged items, customer disputes, chargebacks (with weeks of delay)? Why: it defines who is labelled quickly and who is not.
- Is the model's score the only gate, or do rules and other channels also block or flag? Why: it changes what "unflagged" means.
- What is the average loss per fraud transaction, the cost of one manual review, and the cost of a wrongly blocked good customer? Why: the exploration slice must be priced.
- What are the legal, risk and customer-experience limits on letting a flagged transaction through (amount caps, step-up authentication, per-customer limits)? Why: they decide the design of the release slice.
- How much traffic and how many weekly flagged cases do we have? Why: it sets how big a slice is feasible.

**Approach:**
1. Name the loop. The model is trained and judged on labels it chose, and fraud that it does not flag only shows up late through other channels. Better-looking precision on flagged cases can come with falling recall (in the run: precision 58% to 71%, recall 85% to 51%, missed fraud 768 to 2,510 a week).
2. Slice 1, audit of unflagged traffic: draw a random sample of transactions the model did not flag, label them (review, or follow-up with the customer, no extra block or release), and estimate the fraud rate among unflagged. Recall = flagged fraud / (flagged fraud + estimated unflagged fraud). This costs review time but no extra fraud loss.
3. Slice 2, capped release: for a random small share of flagged transactions, let them through (with amount caps, step-up checks or velocity limits) and record the true outcome. This gives true precision and unbiased training labels for the region the model usually blocks. It costs fraud loss, so keep it small, capped, and approved by risk.
4. Size them. Audit: n = 1.96^2 x (1-p) / (relative error^2 x p). With p = 0.25% missed-fraud rate and plus or minus 20% relative error you need about 38,000 labelled unflagged transactions. Release: n = 1.96^2 x precision x (1-precision) / 0.05^2, about 319 releases for plus or minus 5 points at 71% precision (8.6% of the 3,713 flagged that week; spread it over weeks).
5. Reduce cost: stratify the audit by score band and weight the estimate; rotate the audit across segments; start with a pilot on one segment; use step-up authentication so a released transaction still has a safety check.
6. Use the output: a recall and missed-fraud dashboard, honest thresholds, and training data that includes the unflagged and released outcomes (with their inverse sampling weights).
7. Justify the cost: compare it with the loss it measures (in the run, the slices cost about 19% of one week of missed fraud, once, and the audit can then shrink to a standing small slice).

**Metrics:**
- Audit fraud rate = fraud found in audited unflagged transactions / audited unflagged transactions; missed fraud per week = rate x unflagged volume.
- Recall = flagged fraud / (flagged fraud + estimated missed fraud).
- True precision = fraud among released flagged transactions / released flagged transactions.
- Cost of exploration = releases x precision x average loss + audited transactions x cost per review. Benefit = losses found and avoided, plus better thresholds.
- Guardrails: customer complaints, chargeback rate on the released slice, a per-customer cap.

**Risks:**
- Delay: fraud labels from disputes arrive over weeks, so recent audits are incomplete; use matured windows or follow up directly.
- Released fraud is a real loss and a regulatory and customer risk; cap amounts and use step-up checks.
- Fraudsters learn that a random slice passes; keep the sampling secret and random per transaction, not per user rule.
- Small slices give wide intervals (the sizes above are the minimum).
- Weights: forgetting to weight the exploration data when retraining re-introduces bias.

**What the interviewer scores:**
- Strong: identifies the feedback loop, with the counter-intuitive pair (precision up, recall down).
- Strong: sizes both slices with formulas and separates the cost-free audit from the costly release.
- Strong: speaks about money, risk approval and a cap, and about using the data for retraining with weights.
- Weak: "just label more data" or "retrain on more fraud", or a design with no cost estimate.
- Cross-reference: Book 4 Part 8 has "Retraining pitfalls and feedback loops" and "Design question: the monitoring system for a card-fraud model with chargeback labels that arrive 30 to 90 days late"; Book 4 Part 8 also has "Canary labels and label budgets".

**Example:** (illustrative numbers) 1,000,000 transactions a week, 0.5% fraud (about 5,000). In week 12 the model flags 3,713, of which about 2,620 are fraud (precision 70.6%) and 2,510 fraud transactions go unflagged (recall 51%). Missed-fraud rate among unflagged = 2,510 / 996,287 = 0.25%. A random audit of about 38,000 unflagged transactions finds around 96 fraud and pins the rate to within about plus or minus 20%. Weak answer: "Precision went up, so the model is improving." Strong answer: "Flagged-only labels flatter the model. I would audit a random 38,000 unflagged transactions and release a few hundred capped flagged ones, measure real recall and precision, and show that this costs about a fifth of one week of what we are missing."

**Code:**
```python
# Q40: a fraud model that only learns from what it flags; random exploration slices (illustrative simulation)
import math
import numpy as np

rng = np.random.default_rng(40)
weeks, N = 12, 1_000_000
fraud_rate = 0.005
share_B = np.linspace(0.10, 0.50, weeks)          # new evasive fraud pattern grows
fp_rate = np.linspace(0.003, 0.001, weeks)        # model gets sharper on the easy cases
catch_A, catch_B = 0.92, 0.10

rows = []
for w in range(weeks):
    n_fraud = rng.binomial(N, fraud_rate)
    nB = rng.binomial(n_fraud, share_B[w]); nA = n_fraud - nB
    tpA = rng.binomial(nA, catch_A); tpB = rng.binomial(nB, catch_B)
    fp = rng.binomial(N - n_fraud, fp_rate[w])
    tp = tpA + tpB; flagged = tp + fp
    rows.append((n_fraud, tp, fp, flagged))
rows = np.array(rows)
prec = rows[:, 1] / rows[:, 3]; rec = rows[:, 1] / rows[:, 0]
print("week  apparent precision  true recall   missed fraud")
for w in (0, 5, 11):
    print(f"{w:>4}  {prec[w]:>17.1%}  {rec[w]:>11.1%}  {rows[w, 0] - rows[w, 1]:>12,}")
assert prec[-1] > prec[0] + 0.10 and rec[-1] < rec[0] - 0.25
assert (rows[-1, 0] - rows[-1, 1]) > 2 * (rows[0, 0] - rows[0, 1])

# Exploration 1: a random audit of unflagged transactions (label only, no extra fraud loss)
w = 11
unflag = N - rows[w, 3]; missed = rows[w, 0] - rows[w, 1]; p_u = missed / unflag
def n_for_rel_error(p, rel): return 1.96 ** 2 * (1 - p) / (rel ** 2 * p)
n_aud = n_for_rel_error(p_u, 0.20)
print(f"week 12 missed-fraud rate among unflagged {p_u:.4%}; audit size for +-20% relative error: {n_aud:,.0f} labels")
assert 35_000 < n_aud < 45_000
# repeat the audit many times at that size to check the claim
est = np.array([rng.binomial(round(n_aud), p_u) / round(n_aud) for _ in range(2000)])
cover = (np.abs(est - p_u) / p_u < 0.20).mean()
print(f"share of audits within +-20% of the truth: {cover:.1%}")
assert 0.93 < cover < 0.97
# recall estimate = TP / (TP + estimated missed)
rec_hat = rows[w, 1] / (rows[w, 1] + est.mean() * unflag)
print(f"recall estimate {rec_hat:.3f} vs true {rec[w]:.3f}")
assert abs(rec_hat - rec[w]) < 0.02

# Exploration 2: release a random share of flagged transactions (with a cap) to measure true precision
flagged = rows[w, 3]; tp = rows[w, 1]
n_rel = 1.96 ** 2 * prec[w] * (1 - prec[w]) / 0.05 ** 2
print(f"flagged {flagged:,}; releases needed for +-5 points on precision: {n_rel:,.0f} ({n_rel / flagged:.1%} of flagged)")
avg_loss = 3_000                                    # Rs per fraud transaction (illustrative)
cost_release = n_rel * prec[w] * avg_loss
cost_audit_review = n_aud * 20                      # Rs 20 per review (illustrative)
loss_week = missed * avg_loss
print(f"cost of releases Rs {cost_release:,.0f}; cost of audit reviews Rs {cost_audit_review:,.0f}; weekly missed-fraud loss Rs {loss_week:,.0f}")
assert (cost_release + cost_audit_review) < 0.25 * loss_week
print(f"exploration cost is {(cost_release + cost_audit_review) / loss_week:.1%} of one week of missed fraud")
```

**Output (my run):**
```text
week  apparent precision  true recall   missed fraud
   0              58.1%        84.8%           768
   5              61.4%        68.5%         1,559
  11              70.6%        51.1%         2,510
week 12 missed-fraud rate among unflagged 0.2519%; audit size for +-20% relative error: 38,025 labels
share of audits within +-20% of the truth: 95.7%
recall estimate 0.511 vs true 0.511
flagged 3,713; releases needed for +-5 points on precision: 319 (8.6% of flagged)
cost of releases Rs 675,370; cost of audit reviews Rs 760,497; weekly missed-fraud loss Rs 7,530,000
exploration cost is 19.1% of one week of missed fraud
```

**Follow-ups:**
- Could the audit be smaller? Yes, if you accept a wider interval, or stratify by score and oversample the high-risk unflagged band; the formula shows the size is driven by the rarity of fraud.
- How do you use exploration data in retraining? Weight each item by 1 / its sampling probability, and keep a flag for "exploration" so you can check the model on it separately.
- What if risk will not allow releasing flagged transactions? Use the audit for recall, use step-up authentication or delayed settlement for the release slice, or release only low-amount, low-risk-tier flagged cases.

**Common mistakes:** Trusting precision on flagged cases alone. Sampling "randomly" by customer segment instead of by transaction. Not weighting exploration data. Pricing the slice with no comparison to the loss. Making the slice so small that the interval is useless.

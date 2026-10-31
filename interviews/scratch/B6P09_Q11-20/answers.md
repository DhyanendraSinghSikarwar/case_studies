### Q11 ⭐⭐⭐ 🟡 Healthcare: In a pilot, 1,000 high-risk alerts were raised and clinicians overrode 700 of them. Of the 700 overridden alerts, 35 were followed by a deterioration event, and of the 300 acted-on alerts, 90 were followed by one (counts from a measured pilot). Compute the share of all alerts followed by an event and the share of events that were in acted-on alerts, and explain why you should not conclude that clinicians are simply right or wrong, and what you would do about trust.
**Asked at:** Clinical-ML deployment material (a physician-oriented dataset-shift article, an arXiv paper on what clinicians want from explainable ML, a JMIR paper on alarm fatigue and a circEWS slide deck on calibration and prevalence); research and secondary sources rather than interview banks; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** 12.5% of alerts were followed by an event and 72% of those events sat in acted-on alerts, but override versus event is confounded by selection and by treatment, so I would not call clinicians right or wrong; I would compare within risk strata, read the overridden cases with clinicians, and fix the alert itself.

**Clarifying questions:**
- What counts as an event, and over what window (6, 12, 24 hours)? A longer window makes every rate larger and blurs cause.
- What does "acted on" mean (a documented intervention, a call, a bedside review)? If it is not logged, "acted" is partly inferred.
- Were events with no alert at all counted? The 72% is only among alerted events; events the model missed are not in these counts.
- Did clinicians see the risk score or a reason? An override with no information about why is hard to learn from.
- Is there a fixed threshold, or do some wards get different alerts? Alert volume per nurse drives overrides.

**Approach:**
1. Do the arithmetic. 90 + 35 = 125 events in 1,000 alerts, so 12.5% of alerts were followed by an event. 90 / 125 = 72% of those events were in acted-on alerts. Event rate was 30% in acted alerts and 5% in overridden ones.
2. Say what these do not show. Clinicians choose which alerts to act on, so acted alerts are the sicker-looking ones (selection). Acting also tries to prevent the event, so the 30% is already after treatment (contamination). Both push in opposite directions. The 5% in overridden alerts may be clinicians correctly spotting false alarms, or luck.
3. Compare like with like. Group alerts by model risk band, vital signs and ward. Within a band, compare event rate for acted versus overridden. If overridden alerts in the same band have the same event rate as acted ones, the override looks like noise. If they are clearly lower, clinicians add information the model lacks.
4. Review a sample. Have clinicians read 35 overridden alerts followed by an event (the possible misses) and a random 35 of the 665 that were not (the correct overrides). Tag the reasons: already on treatment, known patient condition, wrong patient context, alert too late.
5. Fix trust on three fronts. Show a short reason with each alert. Cut volume (see the alert-burden maths; ask the clinical safety owner for a workable alert budget). Close the loop: give each ward a monthly view of alerts, overrides and outcomes, and let them challenge it.
6. Governance. Any threshold change goes through the clinical safety group and the ward leads. Keep override reasons as a structured field, not free text only.

**Metrics:**
- Alert event rate = alerts followed by an event / all alerts = 125 / 1,000 = 12.5%.
- Share of alerted events in acted alerts = 90 / 125 = 72%.
- Event rate by action = events / alerts in that group: acted 30%, overridden 5%.
- Within-band event rate by action (the fair comparison); override rate by ward and by hour.
- Guardrails: events with no alert (the model's misses), time from alert to action, and alerts per nurse per shift.

**Risks:**
- Reading "overridden alerts rarely had an event" as "the model is wrong". It could mean clinicians were right, or that acting was not needed.
- Reading "acted alerts often had an event" as "clinicians act on the right ones". Acting may have prevented some events, which hides model value.
- Sample size: 35 events among 700 gives a wide interval, so small differences between wards are noise.
- Training the next model on "event after alert" as the label inflates the harm of treatment: treated patients look healthier.

**What the interviewer scores:**
- Strong: gets 12.5% and 72%, and notes the 72% is only among alerted events.
- Strong: names selection and treatment contamination, and proposes a within-band comparison.
- Strong: treats trust as a product problem (reasons, volume, feedback loop), with the clinical owner deciding.
- Weak: "clinicians override 70% so the model is bad", or "events were low in overrides so clinicians are right".

**Example:** Illustrative, using the question's counts. Weak versus strong:
- Weak: "Seventy per cent were overridden and only 5% of those had events, so clinicians are right and we should lower the alert count."
- Strong: "12.5% of alerts were followed by an event, and 72% of those events were in alerts that were acted on. The 30% versus 5% gap mixes two things: clinicians pick the sicker-looking patients, and acting may prevent the event. So I would compare within risk bands, have two clinicians read the 35 overridden-then-event cases, and agree an alert budget and a reason field with the clinical safety lead before touching the threshold."

**Code:**
```python
import numpy as np

# Pilot counts (measured, from the question)
alerts, overridden, acted = 1000, 700, 300
ev_over, ev_acted = 35, 90
assert overridden + acted == alerts
ev_all = ev_over + ev_acted
share_alerts_with_event = ev_all / alerts
share_events_in_acted = ev_acted / ev_all
rate_over, rate_acted = ev_over / overridden, ev_acted / acted
assert ev_all == 125 and share_alerts_with_event == 0.125
assert round(share_events_in_acted, 3) == 0.72
assert rate_over == 0.05 and rate_acted == 0.30
print("alerts followed by an event:", share_alerts_with_event)
print("events (among alerted) that were in acted-on alerts:", round(share_events_in_acted, 3))
print("event rate overridden / acted:", rate_over, rate_acted)

# Two-proportion z (large-sample): is 30% vs 5% a real gap? Yes, but it is not the question.
p = ev_all / alerts
se = np.sqrt(p * (1 - p) * (1 / overridden + 1 / acted))
z = (rate_acted - rate_over) / se
assert z > 10
print("z for acted vs overridden event rate:", round(float(z), 1))

# Why the gap does not say who is right: a simulation with an illustrative skilled clinician.
# Latent risk r; clinician sees r plus noise and acts if the signal is high; acting cuts events by 40%.
rng = np.random.default_rng(11)
n = 1000
r = rng.beta(2, 8, n)                      # latent true risk, mean 0.2
sees = r + rng.normal(0, 0.08, n)
act = sees > np.quantile(sees, 0.70)       # clinicians act on the top 30% by their own read
prevented = rng.random(n) < 0.40
event = (rng.random(n) < r) & ~(act & prevented)
print("sim: acted share", act.mean(), "event rate acted", round(float(event[act].mean()), 3),
      "overridden", round(float(event[~act].mean()), 3))
no_action_acted = (rng.random(n) < r)[act].mean()
print("sim: acted-group event rate had nobody acted (untreated risk):", round(float(no_action_acted), 3))
assert event[act].mean() > event[~act].mean()      # acted group looks worse even though clinicians are skilled
assert no_action_acted > event[act].mean()   # acting lowered events in the acted group
```

**Output (my run):**
```
alerts followed by an event: 0.125
events (among alerted) that were in acted-on alerts: 0.72
event rate overridden / acted: 0.05 0.3
z for acted vs overridden event rate: 11.0
sim: acted share 0.3 event rate acted 0.207 overridden 0.133
sim: acted-group event rate had nobody acted (untreated risk): 0.353
```

**Follow-ups:**
- Can you measure the model's value if clinicians act on the alerts? Only partly. A randomised or staggered rollout (some wards with alerts, some without) gives the effect of the whole system; ask the clinical research and safety teams whether and how that is allowed.
- What if overrides are mostly at night? That points to workload or context; look at alerts per nurse per hour and at time-of-day thresholds with the ward leads.
- What label would you train on next? A label that does not depend on treatment, such as a physiology-based deterioration definition, or use methods that account for treatment; discuss with the clinical owner.

**Common mistakes:**
- Dividing events by 700 or 300 and calling the result "accuracy".
- Quoting 72% as "share of all deterioration events" when missed events are unknown.
- Ignoring that treated patients are the ones the model flagged most strongly.
- Pushing a threshold change without the clinicians who carry the alerts.

### Q12 ⭐⭐⭐ 🟡 Ads: A publisher sends 2,000,000 clicks in a day and 200,000 of them (10% of clicks) are later classified as invalid, with the advertiser credited after 3 days. The conversion rate per click is 2.0% for valid clicks and 0% for invalid clicks, so the measured blended rate is 1.8% (rates from a measured sample). Explain how training the click and conversion models on the raw clicks distorts bids, how you would handle the 3-day delay in labels, and what you would tell the publisher account team.
**Asked at:** Ad-serving system-design material (techinterview.org ad serving and real-time bidding pages, a Dataford question on budget pacing and frequency capping, machinelearningatscale.com on frequency capping; feedback-controller pacing, per-user counters and credits for invalid clicks appear in the snippets); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Raw clicks mix real users with invalid traffic, so a model trained on them learns a blended conversion rate of 1.8% instead of the 2.0% on valid clicks, and it learns a publisher's invalid share as if it were user behaviour; I would train on valid-only labels that have matured past the 3-day delay and tell the account team which numbers are provisional.

**Clarifying questions:**
- Who pays for invalid clicks: do we pay first and get a credit after 3 days, or are they filtered before billing? It decides whether the right bid uses 1.8% or 2.0%.
- Is the invalid flag a rule, a vendor score or manual review? Late, model-based flags change over time and need versioning.
- Does the 3-day delay apply to the invalid label only, or also to conversions (which usually arrive later)? Both censor the newest data.
- Does the invalid share differ by publisher, placement or hour? A shared share is a small bias; a varying share distorts ranking between publishers.
- What is the value per conversion and the bidding rule? We need it to price the bias.

**Approach:**
1. Do the arithmetic. 10% invalid, conversion 2.0% on valid, 0% on invalid: blended = 0.9 x 2.0% = 1.8%. With an illustrative value of 50 per conversion, the raw bid per click is 0.90 and the valid-only bid is 1.00, a 10% underbid.
2. Say which direction the bias goes. If invalid clicks are credited back, we are only paying for valid ones, so the right value of a billed click is the valid rate (2.0%). A raw-trained model underbids by 10% on average. If they are not credited, the blended 1.8% is the true value of what we pay for, and the fix is to push for filtering, not to adjust the model. Ask billing which case holds.
3. Publisher differences matter more than the average. A publisher with 2% invalid shows 1.96%, one with 30% shows 1.4%, with the same real users. The raw model punishes the second publisher for traffic quality, which is acceptable if you are billed for it and wrong if you are credited.
4. Handle the delay. A click from today has no invalid flag yet, so it looks valid and unconverted when it is invalid. Recent days therefore show a lower conversion rate than matured days (in the run, 1.71% versus 1.96% on the same traffic mix). Train on matured clicks only (age at least 3 days, plus the conversion window), or train two models: P(invalid) from matured data, and P(convert | valid).
5. Combine at serving. Expected value per click = P(valid) x P(convert | valid) x value, where P(valid) comes from a publisher and placement model. Use a conservative P(valid) for new sources.
6. Tell the account team plainly: figures from the last 3 days are provisional and usually revised; we will report valid-only conversion rate, invalid share by publisher, and the credit amount; and publishers with a high invalid share may see lower bids until their traffic matures. Route any contract or billing wording through the commercial and legal owners.

**Metrics:**
- Invalid share = invalid clicks / all clicks = 200,000 / 2,000,000 = 10%.
- Valid CVR = conversions on valid clicks / valid clicks (2.0% in the sample); blended CVR = conversions / all clicks (1.8%).
- Label maturity: share of clicks older than 3 days whose flag is final; revision rate = clicks whose label changes after first being scored.
- Calibration by publisher on matured data: predicted conversions / actual conversions per decile.
- Guardrails: spend per valid conversion, credits received per week, bid change versus last week by publisher.

**Risks:**
- Training on the newest days: the recent label bias makes the model underbid just when traffic is shifting.
- Dropping unflagged recent clicks removes the very traffic whose quality is unknown, so a new bad source looks fine until day 3.
- A model that learns "publisher B converts less" when the cause is invalid traffic will keep underbidding after the publisher cleans up.
- Sample rates (2.0%, 10%) are from a sample; check their interval before quoting them to a publisher.

**What the interviewer scores:**
- Strong: derives 1.8% from 90% x 2.0% and links the bid error to the billing treatment.
- Strong: names label delay as a censoring problem and trains on matured data or models the flag.
- Strong: separates invalid-traffic share (a source property) from user conversion behaviour.
- Weak: "just remove the bots"; ignoring the delay; saying the bias is always 10% for every publisher.

**Example:** Illustrative numbers, value 50 per conversion. Weak versus strong:
- Weak: "I would filter out invalid clicks and retrain on the full data."
- Strong: "On raw clicks the model sees 1.8% and bids 0.90; the valid-only rate is 2.0%, so bid 1.00, assuming invalid clicks are credited back, which I would confirm with billing. The last 3 days are not yet flagged, so I train on matured clicks, and I model the chance a click is valid per publisher. I would tell the account team that recent numbers are provisional and that bids on a high-invalid publisher will be lower until its flags settle."

**Code:**
```python
import numpy as np

clicks, invalid = 2_000_000, 200_000
cvr_valid, cvr_invalid = 0.02, 0.0
share_invalid = invalid / clicks
blended = (1 - share_invalid) * cvr_valid + share_invalid * cvr_invalid
assert share_invalid == 0.10
assert abs(blended - 0.018) < 1e-12
print("blended CVR:", round(blended, 4))

# Bids per click if value per conversion is 50 (illustrative)
value = 50
bid_raw, bid_valid = blended * value, cvr_valid * value
assert abs(bid_raw - 0.90) < 1e-9 and abs(bid_valid - 1.00) < 1e-9
print("bid raw vs valid-only:", round(bid_raw, 2), round(bid_valid, 2), "underbid", round(1 - bid_raw / bid_valid, 3))
assert abs((1 - bid_raw / bid_valid) - 0.10) < 1e-9

# Heterogeneity: two publishers, same valid CVR, different invalid share
for name, inv in [("pub A", 0.02), ("pub B", 0.30)]:
    b = (1 - inv) * cvr_valid
    print(name, "invalid", inv, "raw CVR", round(b, 4))
assert abs((1 - 0.30) * 0.02 - 0.014) < 1e-12

# Delay: classification arrives 3 days after the click. Naive training on the last days
# treats unclassified invalid clicks as valid (or drops them), so labels differ by age.
rng = np.random.default_rng(12)
days, per_day, delay = 10, 20_000, 3
day = np.repeat(np.arange(days), per_day)
is_invalid = rng.random(day.size) < share_invalid
conv = (~is_invalid) & (rng.random(day.size) < cvr_valid)
age = days - 1 - day                                   # 0 = today
known_invalid = is_invalid & (age >= delay)            # invalid label only known after 3 days
recent = age < delay
cvr_recent_naive = conv[recent].mean()                 # all recent clicks, invalid not yet flagged
cvr_recent_true_valid = conv[recent & ~is_invalid].mean()
cvr_old_valid = conv[~recent & ~known_invalid].mean()  # matured: invalid removed
print("recent days, invalid still unflagged:", round(float(cvr_recent_naive), 4))
print("recent days, true valid only:", round(float(cvr_recent_true_valid), 4))
print("matured days, invalid removed:", round(float(cvr_old_valid), 4))
assert abs(cvr_recent_naive - 0.018) < 0.002
assert abs(cvr_old_valid - 0.02) < 0.002
assert cvr_recent_naive < cvr_old_valid               # same traffic, different apparent CVR by label age

# Fix 1: train on matured clicks only (age >= delay). Fix 2: model P(invalid) and weight.
p_valid = 1 - share_invalid
corrected = cvr_recent_naive / p_valid
print("recent naive / P(valid):", round(float(corrected), 4))
assert abs(corrected - 0.02) < 0.003
```

**Output (my run):**
```
blended CVR: 0.018
bid raw vs valid-only: 0.9 1.0 underbid 0.1
pub A invalid 0.02 raw CVR 0.0196
pub B invalid 0.3 raw CVR 0.014
recent days, invalid still unflagged: 0.0171
recent days, true valid only: 0.019
matured days, invalid removed: 0.0196
recent naive / P(valid): 0.019
```

**Follow-ups:**
- How would you use the unflagged recent data? Add a P(invalid) model trained on matured clicks and weight recent clicks by predicted P(valid); do not treat them as clean.
- What if the flag rule changes mid-quarter? Version the rule, retrain per version, and re-score history so training labels are consistent.
- What if conversions also arrive late? Use a delayed-feedback approach (train only on clicks older than the conversion window, or model the delay); the general method is the same.

**Common mistakes:**
- Training on the most recent days and treating missing flags as "valid".
- Assuming the bias is the same for every publisher.
- Reporting 1.8% to the publisher as their conversion quality without separating invalid share.
- Forgetting to ask who bears the cost of invalid clicks.

### Q13 ⭐⭐⭐ 🔴 Fintech: A lender approved 30,000 of 100,000 applicants last year (30%) and 1,200 of the approved (4%) defaulted within 12 months, measured on matured outcomes. A new model is trained only on the approved applicants and the 70,000 rejected applicants have no outcome. If rejects defaulted at 3 times the approved rate, the population default rate would be 9.6%, which is one scenario and not a measurement. Explain the bias, the reject-inference options and their limits, and what low-risk experiment would give you real outcomes on rejects.
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Training on approved applicants only teaches the model about the people the old policy liked, so it is biased and overconfident on the 70,000 rejects; reject inference can narrow the gap but not close it, and the clean fix is a small, capped, randomised approval of near-cutoff rejects to get real outcomes.

**Clarifying questions:**
- How were approvals decided: a score cutoff, rules, manual overrides? A deterministic rule on observed features is much easier to correct than a human override on unobserved information.
- Were defaults on rejects ever observed elsewhere, for example through a credit bureau record of loans they took at another lender? Whether we may use that is a question for compliance and the privacy team.
- Is the 12-month default definition fixed? A different window changes the 4% and the scenario.
- What is the downside budget: how much loss are we willing to carry for learning? It sizes the experiment.
- Which decisions will the new model drive: approve, limit, price? Each needs a different part of the risk range.

**Approach:**
1. State the arithmetic. Approved: 30,000 (30%), 1,200 defaults, 4%. If rejects defaulted at 3 times that, 12% of 70,000 = 8,400 defaults, and the population rate = (1,200 + 8,400) / 100,000 = 9.6%. That is one scenario: the ratio is not measured. With a ratio of 1 the population rate is 4%, with 5 it is 15.2% (see the run).
2. Explain the bias. The approved set is truncated on the old score, so the model sees only the low-risk end. Two consequences: its measured AUC and bad rate are for approved customers, not applicants, and it extrapolates into a region it has never seen. In the simulation a linear fit on approved applicants predicts a 6.0% default for rejects when the real rate is 10.9%.
3. List the reject-inference options and their limits. Treat rejects as bad: crude, inflates risk. Extrapolation or parcelling (score rejects with the approved-trained model and assign outcomes by band): assumes the thing you are trying to learn, so it adds no information. Augmentation or reweighting by approval probability: fixes bias only if approval depended on observed variables (a missing-at-random assumption). Use of outside outcomes (bureau data on rejects): helps if allowed and relevant. All of these need testing on a period where outcomes are known; none replaces data.
4. Run the low-risk experiment. For a small random share of near-cutoff rejects (not the riskiest), approve with a small limit and a cap on total exposure. Randomisation makes the outcomes unbiased for that band. In the run: 500 people at a limit of 1,000 is an upper bound of 500,000 of exposure and gives about +/- 1.2 points of default-rate precision at a 1.8% observed rate (illustrative).
5. Get approvals for the experiment from credit risk and compliance (fairness review, any rule on random approvals is for them to say). Pre-agree a stop rule on cumulative losses.
6. Use the results: refit on approved plus the experiment (weight the experiment by 1 / probability of selection), re-check calibration on the experimental band, and re-run the cutoff analysis. Do not extrapolate beyond the band you sampled.

**Metrics:**
- Default rate = defaults within 12 months / accounts opened, for matured cohorts only.
- Calibration by score band on the experimental slice: predicted defaults / observed defaults.
- Population AUC on a fair holdout (approved plus experimental slice, weighted), not approved-only AUC.
- Experiment guardrails: exposure = accounts x limit (upper bound, all drawn, no recovery); realised loss versus pre-agreed cap.

**Risks:**
- Treating 9.6% as the answer. It is one scenario from an assumed ratio of 3.
- The experiment covers only near-cutoff rejects; it says little about the worst 50,000.
- Selection by hidden information (an underwriter's note) cannot be corrected by reweighting on model features.
- Economic conditions change between the matured cohort and today, so a cohort result may not transfer.

**What the interviewer scores:**
- Strong: computes 9.6% and says it is one scenario with a sensitivity range.
- Strong: names truncation and extrapolation, and says inference methods rest on assumptions they cannot test alone.
- Strong: proposes a bounded, randomised exploration with a loss cap and compliance sign-off.
- Weak: "label rejects as bad" or "use the model to label rejects" without noting the circularity.

**Example:** Illustrative. Weak versus strong:
- Weak: "I would score the rejects with the model and use those as labels."
- Strong: "Scoring the rejects with a model trained on approvals just returns what the model already believes. The 9.6% is a scenario from an assumed ratio of 3; at a ratio of 1 it is 4% and at 5 it is 15.2%. I would approve a small random slice of near-cutoff rejects at a low limit, cap the total exposure at 500,000 for 500 people, and agree the design with credit risk and compliance first. Then I would refit using weights and check calibration on that slice."

**Code:**
```python
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

# Arithmetic from the question
apps, approved, defaults_appr = 100_000, 30_000, 1_200
rejected = apps - approved
rate_appr = defaults_appr / approved
assert rejected == 70_000 and abs(rate_appr - 0.04) < 1e-12
rate_rej = 3 * rate_appr
defaults_rej = rejected * rate_rej
pop_rate = (defaults_appr + defaults_rej) / apps
assert abs(rate_rej - 0.12) < 1e-12 and round(defaults_rej) == 8_400
assert abs(pop_rate - 0.096) < 1e-12
print("reject default (scenario):", rate_rej, "population default (scenario):", pop_rate)
# Sensitivity: the 9.6% depends on the ratio, which nobody has measured
for k in (1, 2, 3, 5):
    print("ratio", k, "-> population default", round((defaults_appr + rejected * k * rate_appr) / apps, 4))
assert round((defaults_appr + rejected * 1 * rate_appr) / apps, 4) == 0.04

# Simulation: a model fitted on approved only, then used on everyone
rng = np.random.default_rng(13)
n = 100_000
x = rng.normal(0, 1, n)                                   # risk driver; higher is riskier
true_logit = -3.2 + 0.9 * x + 0.35 * np.maximum(x, 0) ** 2   # risk accelerates in the tail
y = rng.random(n) < expit(true_logit)
approve = x < np.quantile(x, 0.30)                        # old policy approves the lowest-risk 30%
Xa = np.c_[np.ones(approve.sum()), x[approve]]
ya = y[approve].astype(float)

def nll(b):
    z = Xa @ b
    return np.sum(np.logaddexp(0, z) - ya * z)
b = minimize(nll, np.zeros(2), method="BFGS").x
pred_rej = expit(b[0] + b[1] * x[~approve])
actual_rej = y[~approve].mean()
print("approved actual default:", round(float(y[approve].mean()), 4))
print("rejects: model predicts", round(float(pred_rej.mean()), 4), "actual", round(float(actual_rej), 4))
assert pred_rej.mean() < actual_rej * 0.8                 # extrapolating a linear fit into the tail underpredicts

# Low-risk experiment: approve a small random slice of rejects near the cutoff, small limits
near = np.where(~approve)[0]
near = near[np.argsort(x[near])][:7_000]                    # the 7,000 rejects closest to the cutoff (10% of rejects)
pick = rng.choice(near, 500, replace=False)
exposure = 500 * 1_000                                       # 500 people x limit 1,000 (illustrative)
obs = y[pick].mean()
se = np.sqrt(obs * (1 - obs) / 500)
print("experiment: n=500, exposure upper bound", exposure, "observed default", round(float(obs), 3), "+/-", round(float(1.96 * se), 3))
assert exposure == 500_000
assert 1.96 * se < 0.04
```

**Output (my run):**
```
reject default (scenario): 0.12 population default (scenario): 0.096
ratio 1 -> population default 0.04
ratio 2 -> population default 0.068
ratio 3 -> population default 0.096
ratio 5 -> population default 0.152
approved actual default: 0.0145
rejects: model predicts 0.0599 actual 0.1088
experiment: n=500, exposure upper bound 500000 observed default 0.018 +/- 0.012
```

**Follow-ups:**
- Can you validate a reject-inference method? Only on a setting where you know the outcomes, for example a period where the cutoff was temporarily relaxed, or the experimental slice; otherwise you cannot.
- What if the experiment is not allowed? Use the approved data with a conservative, monotone model, do not extrapolate the cutoff downward, and monitor early-arrears on any new approvals.
- Does the bias affect fairness reviews? Yes, the group mix of rejects is unobserved; raise it with the compliance and model-risk teams.

**Common mistakes:**
- Reporting approved-only AUC as the model's AUC.
- Treating the 3x ratio as a measured fact.
- Running the experiment on the riskiest rejects, or with no loss cap.
- Reweighting on features when approval used information the model does not have.

### Q14 ⭐⭐⭐ 🔴 E-commerce: A product's selling window runs from 08:00 to 22:00 (14 hours) and it sold out at 18:00 on 5 of the last 7 days with 400 units sold on each of those days, while on the other 2 days it sold 560 and 540. A forecast trained on sales averages 443 units a day and next week's stock is planned from it. Assuming flat hourly demand, which is an assumption to test, estimate the uncensored daily demand on the stock-out days and the 7-day average, and explain how you would model demand from censored sales and handle a price change in the same week.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to censored demand and stock-outs in forecasting and pricing material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Sales are not demand when the shelf is empty: on the 5 stock-out days, 400 units in 10 hours implies about 560 for the full 14 hours, so true average demand is about 557 a day, not the 443 the forecast uses, and I would model demand with a censored likelihood and handle the price change as a separate effect.

**Clarifying questions:**
- Is stock-out time recorded per unit (a timestamp of the last sale and of availability), or only inferred from daily totals? Exact hours-in-stock is the key input.
- Was the product the only variant, or could customers switch to a substitute when it sold out? Substitution moves demand elsewhere.
- Was the price constant, and was it promoted on the sell-out days? A promotion explains both fast sell-out and high demand.
- Is the hourly demand shape known (for example from a similar product)? The flat assumption can be tested.
- What does the forecast drive: reorder quantity, markdown, or safety stock? The cost of overstock versus lost sales sets how much the 114-unit gap matters.

**Approach:**
1. Do the arithmetic. Stock-out at 18:00 means 10 open hours (08:00 to 18:00), so 400 / 10 = 40 units an hour and 40 x 14 = 560 for the day. The 7-day demand is (5 x 560 + 560 + 540) / 7 = 557.1; the sales average is (5 x 400 + 560 + 540) / 7 = 442.9. The forecast understates by about 20.5%.
2. Test the flat-hour assumption. The two non-stock-out days give 40.0 and 38.6 units an hour, which is consistent with 40 but does not show the shape within a day. If the last 4 hours are twice as busy, demand is 720 on a day with the same 400 sold by 18:00, so flat extrapolation says 560 and understates by 160 (see the run). Use intraday sales on non-stock-out days to estimate the hourly profile.
3. Model with censoring. Treat each day's sales as min(demand, stock). Fit demand with a likelihood that, for a censored day, contributes P(demand at least stock) and for an uncensored day the density. Use hours-in-stock as exposure in a Poisson or negative-binomial hourly model, with day-of-week, price, promotion and season terms.
4. Be careful with only 7 days. With 2 uncensored days, a censored-normal fit in the run gives mean 550 but an overconfident sd of 10; do not trust that sd. Pool across similar products or weeks (hierarchical model) to stabilise it.
5. Price change in the same week. Price and stock-out are confounded (a price cut sells out sooner). Estimate price elasticity from a model with price as a covariate and the censored likelihood, using only in-stock hours, and compare same hours across price levels. If you can, run a randomised price test across stores or customers, and flag cannibalisation of substitutes.
6. Use the forecast properly. Forecast demand, not sales; then choose stock by the newsvendor logic (cost of an unsold unit versus a lost sale), using a quantile of demand rather than the mean.

**Metrics:**
- Uncensored demand = units sold / open hours before stock-out x selling hours (560 on a stock-out day).
- Censoring rate = days with stock-out / days (5 of 7 = 71%).
- Forecast bias = (forecast - demand estimate) / demand estimate on days with a stock-out, and a lost-sales estimate = demand estimate - sales.
- Service level = share of days with no stock-out; guardrails: overstock cost and markdown rate.

**Risks:**
- Flat hourly demand is wrong for most products; an evening peak makes the estimate too low, a morning peak too high.
- Shoppers may leave the site on an out-of-stock page, so demand after the stock-out is lower than the early-hours rate would suggest, or they buy a substitute.
- Planning stock from the 443 average repeats the stock-out and trains the next forecast on even more censored data.
- A price change with a stock-out in the same week cannot be separated with 7 days of data.

**What the interviewer scores:**
- Strong: gets 560, 557 and the 20.5% gap, and labels flat demand as an assumption.
- Strong: names censoring, a likelihood that handles it, and exposure (hours in stock).
- Strong: separates the price effect and mentions substitution and the newsvendor decision.
- Weak: "average the sales" or "just fill in the missing hours with the mean".

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Average sales are 443, so I will plan 443 plus a safety margin."
- Strong: "On stock-out days we sold 40 an hour for 10 hours, so with flat demand that is 560 a day, and the true weekly average is about 557, around 20% above what the forecast uses. I would test the flat assumption on intraday data, fit demand with a censored likelihood using hours in stock, and plan stock at a high quantile, because a lost sale and an unsold unit have different costs."

**Code:**
```python
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

hours = 14                                   # 08:00 to 22:00
sold_out_at = 18 - 8                         # hours open before sell-out
assert sold_out_at == 10
rate_per_hour = 400 / sold_out_at
uncensored = rate_per_hour * hours
assert rate_per_hour == 40 and uncensored == 560
daily = [400] * 5 + [560, 540]
avg_sales = sum(daily) / 7
avg_demand = (5 * uncensored + 560 + 540) / 7
gap = 1 - avg_sales / avg_demand
print("avg sales:", round(avg_sales, 1), "avg uncensored demand:", round(avg_demand, 1), "understatement:", round(gap, 3))
assert round(avg_sales) == 443 and round(avg_demand, 1) == 557.1 and round(gap, 3) == 0.205
print("hourly rate on non-sellout days:", round(560 / 14, 1), round(540 / 14, 1))

# Test of the flat-hours assumption with a simulated evening peak
profile = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2], float)   # last 4 hours twice as busy (illustrative)
profile /= profile.sum()
total = 720                                  # illustrative true demand; 10/18 of it falls in the first 10 hours
cum = np.cumsum(profile * total)
k = int(np.argmax(cum >= 400 - 1e-9))        # index of the hour in which the stock of 400 runs out
print("peak case: stock-out after hour", k + 1, "of 14; true demand", total)
flat_est = 400 / (k + 1) * hours
print("flat extrapolation from the stock-out hour:", round(flat_est, 1))
assert (k + 1) == 10 and flat_est == 560 and flat_est < total   # evening peak: flat rule understates (560 vs 720)

# Censored model on daily data: normal demand, stock 400 on 5 days (censored), 2 uncensored days
y = np.array(daily, float); cens = np.array([True] * 5 + [False] * 2)
def nll(p):
    mu, ls = p; s = np.exp(ls)
    ll = norm.logpdf(y[~cens], mu, s).sum() + norm.logsf(400, mu, s) * cens.sum()
    return -ll
fit = minimize(nll, [450.0, np.log(80.0)], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-9, "maxiter": 5000})
mu, s = fit.x[0], float(np.exp(fit.x[1]))
print("censored-normal fit on 7 days: mean", round(float(mu), 1), "sd", round(s, 1))
assert mu > avg_sales
assert abs(mu - 550) < 1 and s < 15      # with 2 uncensored days the fit is overconfident: do not trust this sd
```

**Output (my run):**
```
avg sales: 442.9 avg uncensored demand: 557.1 understatement: 0.205
hourly rate on non-sellout days: 40.0 38.6
peak case: stock-out after hour 10 of 14; true demand 720
flat extrapolation from the stock-out hour: 560.0
censored-normal fit on 7 days: mean 550.0 sd 10.0
```

**Follow-ups:**
- What if the product sells out before 08:00 of the next day's restock? Then the day's window is shorter; use actual open and stock hours as exposure.
- How would you check the flat assumption without intraday data? You cannot fully; ask engineering for hourly order logs and check a similar product that did not sell out.
- How would you size the stock? Pick the quantile of demand where the cost of the next unit unsold equals the margin lost per unit missed; the mean is rarely right.

**Common mistakes:**
- Using sales as demand.
- Filling the stock-out hours with zeros or dropping those days.
- Ignoring that a price change and a stock-out occurred together.
- Trusting a variance estimated from two uncensored days.

### Q15 ⭐⭐⭐ 🔴 Healthcare: Two radiologists independently labelled the same 1,000 scans: both marked 150 as abnormal, both marked 750 as normal, reader A alone marked 60 as abnormal and reader B alone marked 40. The raw agreement is 90%, but the team plans to train on reader A's labels as ground truth and to quote accuracy against them. Compute Cohen's kappa, explain what it implies for the model's ceiling and evaluation, and describe how you would build a better reference standard.
**Asked at:** Clinical-ML deployment material (a physician-oriented dataset-shift article, an arXiv paper on what clinicians want from explainable ML, a JMIR paper on alarm fatigue and a circEWS slide deck on calibration and prevalence); research and secondary sources rather than interview banks; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Kappa is about 0.69, not 90%: raw agreement looks high because 79% to 81% of scans are normal, so the readers agree by chance a lot; reader A is a noisy reference, so I would build an adjudicated or outcome-based reference standard and report accuracy against that.

**Clarifying questions:**
- Were the readers blinded to each other, and to clinical history? Non-independent readers inflate agreement.
- What is the clinical task (any abnormal finding, one specific finding)? The label definition drives what disagreement means.
- Is there an outcome truth available (biopsy, follow-up imaging, clinical course)? That is a better reference than any reader.
- How were the 1,000 scans sampled? If they are enriched for abnormal, kappa and prevalence are not those of the clinic.
- What are the readers' experience levels and the site? A reference should reflect the intended users.

**Approach:**
1. Compute agreement. Matrix: both abnormal 150, both normal 750, A-only 60, B-only 40. Observed agreement = 900 / 1,000 = 0.90. A calls 210 abnormal and B 190. Chance agreement = 0.21 x 0.19 + 0.79 x 0.81 = 0.6798. Kappa = (0.90 - 0.6798) / (1 - 0.6798) = 0.688. A bootstrap interval in the run is about 0.63 to 0.74.
2. Read it correctly. Kappa near 0.69 is moderate to substantial agreement on a common scale; the thresholds are conventions, not rules. Specific agreement is more informative: positive agreement 0.75 (when one reader says abnormal, the other agrees 75% of the time) and negative agreement 0.94.
3. Say what it implies for the ceiling. If A's labels are noisy, a model cannot be reliably better than A as measured against A. In an illustrative model with 20% prevalence and readers of 90% sensitivity and 96% specificity, even a perfect model scores only about 0.947 accuracy against reader A, and two readers agree about 90% of the time (see the run). A model that is more accurate than A will look worse than it is.
4. Beware accuracy as a headline. Everything-normal scores 79% accuracy against A. Report sensitivity, specificity and positive predictive value at the intended prevalence, with intervals.
5. Build a better reference. Options in order of strength: outcome truth (pathology or follow-up), then adjudication (a third senior reader resolves the 100 disagreements, or a panel), then a consensus of three or more readers. Keep the disagreement cases as a separate set: they show where the model and humans differ.
6. Evaluate with the uncertainty. Report model versus adjudicated reference, plus model versus each reader, and compare the model's agreement with a reader to reader-reader agreement (a model agreeing with A at kappa 0.7 is performing at human level, not 70% of the way).

**Metrics:**
- Observed agreement = (both abnormal + both normal) / all = 0.90.
- Kappa = (observed - chance) / (1 - chance) = 0.688; positive and negative specific agreement = 0.75 and 0.94.
- Model sensitivity, specificity and PPV against the adjudicated reference, each with a confidence interval, and calibration at the clinic's prevalence.
- Guardrails: label-noise estimate per class, and model-reader kappa compared with reader-reader kappa.

**Risks:**
- Training on A's labels teaches the model A's habits, including bias; the model inherits A's miss rate.
- Quoting accuracy against A as accuracy in the clinic.
- Adjudicating only disagreements makes the reference depend on the readers' disagreement pattern; spot-check some agreed cases.
- Kappa depends on prevalence, so it is not comparable across sites with different mixes.

**What the interviewer scores:**
- Strong: computes kappa 0.69 with chance agreement shown, and quotes positive agreement.
- Strong: explains the ceiling and why a better-than-A model looks worse.
- Strong: proposes an adjudicated or outcome-based reference and reports against it with intervals.
- Weak: "90% agreement is great, so use A as ground truth".

**Example:** Using the question's counts. Weak versus strong:
- Weak: "The readers agree 90% of the time, so reader A's labels are reliable and we can report accuracy against them."
- Strong: "Agreement is 90% but chance alone gives 68%, so kappa is about 0.69, and when one reader says abnormal the other agrees only 75% of the time. A model cannot be shown better than A against A's own labels, and an all-normal model already scores 79%. I would have a third reader adjudicate the 100 disagreements, or use pathology or follow-up where it exists, and report sensitivity, specificity and PPV with intervals."

**Code:**
```python
import numpy as np

both_abn, both_norm, a_only, b_only = 150, 750, 60, 40
n = both_abn + both_norm + a_only + b_only
assert n == 1000
po = (both_abn + both_norm) / n
a_abn, b_abn = both_abn + a_only, both_abn + b_only
assert po == 0.90 and a_abn == 210 and b_abn == 190
pe = (a_abn / n) * (b_abn / n) + (1 - a_abn / n) * (1 - b_abn / n)
kappa = (po - pe) / (1 - pe)
assert abs(pe - 0.6798) < 1e-9 and abs(kappa - 0.6877) < 5e-4
print("raw agreement", po, "chance agreement", round(pe, 4), "kappa", round(kappa, 4))
pos_agree = 2 * both_abn / (a_abn + b_abn)
neg_agree = 2 * both_norm / (2 * both_norm + a_only + b_only)
print("positive agreement", round(pos_agree, 3), "negative agreement", round(neg_agree, 3))
assert round(pos_agree, 3) == 0.75
# Baseline: a model that says everything is normal scores this against A
print("all-normal accuracy vs reader A:", 1 - a_abn / n)
assert abs((1 - a_abn / n) - 0.79) < 1e-12

# Bootstrap interval for kappa (seeded)
rng = np.random.default_rng(15)
cells = np.array([both_abn, a_only, b_only, both_norm])
def kap(c):
    t = c.sum(); o = (c[0] + c[3]) / t
    a = (c[0] + c[1]) / t; b = (c[0] + c[2]) / t
    e = a * b + (1 - a) * (1 - b)
    return (o - e) / (1 - e)
bs = [kap(rng.multinomial(n, cells / n)) for _ in range(4000)]
lo, hi = np.percentile(bs, [2.5, 97.5])
print("bootstrap 95% interval for kappa:", round(float(lo), 3), round(float(hi), 3))
assert lo < kappa < hi

# Why accuracy against A has a ceiling. Illustrative generative model: prevalence 20%, readers independent given truth.
prev, sens, spec = 0.20, 0.90, 0.96
def reader_accuracy(): return prev * sens + (1 - prev) * spec
acc_A = reader_accuracy()
# a perfect model (equals truth) scored against reader A has accuracy = reader A's accuracy
truth = rng.random(200_000) < prev
ra = np.where(truth, rng.random(truth.size) < sens, rng.random(truth.size) > spec)
rb = np.where(truth, rng.random(truth.size) < sens, rng.random(truth.size) > spec)
print("sim: perfect model accuracy vs A:", round(float((truth == ra).mean()), 3), "reader A vs B agreement:", round(float((ra == rb).mean()), 3))
assert abs((truth == ra).mean() - acc_A) < 0.003
assert (truth == ra).mean() < 1.0 and abs((ra == rb).mean() - 0.90) < 0.02
```

**Output (my run):**
```
raw agreement 0.9 chance agreement 0.6798 kappa 0.6877
positive agreement 0.75 negative agreement 0.938
all-normal accuracy vs reader A: 0.79
bootstrap 95% interval for kappa: 0.628 0.742
sim: perfect model accuracy vs A: 0.947 reader A vs B agreement: 0.902
```

**Follow-ups:**
- How many readers do you need? Three gives a majority vote and shows which cases are contested; more adds cost with diminishing gain. Ask the clinical lead.
- Does a high kappa mean the labels are correct? No; readers can share a bias. Only outcomes can show that.
- How do you present the model's performance? Against the adjudicated reference with intervals, and next to reader performance on the same scans.

**Common mistakes:**
- Treating raw agreement as reliability.
- Calling one reader "ground truth".
- Forgetting prevalence when interpreting kappa or accuracy.
- Reporting no uncertainty on 1,000 scans, 210 of them abnormal.

### Q16 ⭐⭐⭐ 🔴 Ads: After a platform privacy change, 60% of users allow tracking and reported attributed conversions fell from 10,000 to 7,000 a day (30% lower, relative to 10,000), while first-party total orders stayed flat at 25,000 a day. Scaling the 7,000 by 1 divided by 0.6 gives about 11,667, which is 16.7% above the earlier 10,000. Explain why the naive scale-up is probably wrong, how you would estimate true conversions and recalibrate the bidding model, and which checks you would run.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to privacy changes, consent and signal loss in ads measurement; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The scale-up to 11,667 implies conversions grew 16.7% while first-party orders were flat, so it is probably wrong: users who allow tracking are not a random 60%, and the old 10,000 was never the truth either; I would estimate true conversions with a calibrated first-party anchor and a holdout test, then recalibrate the bid model to that.

**Clarifying questions:**
- What did "attributed" mean before and after (a click-through only, view-through, platform-modelled credit)? The platform may have changed its method, not only the data.
- Is the 60% consent share stable across days and segments? A moving share breaks any single scale factor.
- Do I have first-party orders by source, and a way to tie some of them to ad exposure (logged-in users, coupon codes, surveys)? These are the anchors.
- Is there any holdout or geo test running? It gives an unbiased incrementality baseline.
- What does the bid model predict and from what labels? It decides what needs recalibration.

**Approach:**
1. Do the arithmetic. 7,000 / 10,000 means a 30% drop; 7,000 / 0.6 = 11,667, which is 16.7% above 10,000.
2. Show why it is suspicious. First-party total orders are flat at 25,000 a day. Reported attribution covered 10,000 / 25,000 = 40% of orders before and 7,000 / 25,000 = 28% after. A scale-up that lands above the old figure claims advertising delivered more conversions the day privacy changed, with nothing else moving. The more likely story is a mix: consenting users convert differently from non-consenting ones, and the platform may fill some gaps with modelled credit. In the run, retention of 70% against a consent share of 60% implies consenters were 16.7% more attributable, which is exactly the 16.7% error.
3. Estimate true conversions properly. Use a first-party anchor: total orders by day, and orders from segments where exposure can be linked for all users (logged-in customers, coupon codes), to measure what share of true conversions the new reporting sees. Then divide by that share, per segment. In a simulation with consenters converting 1.4 times as often, the naive scale-up overstates by about 12%, while the logged-in-segment ratio is within 1%.
4. Validate with experiments. Run a geo holdout or randomised holdout (ask the measurement and platform teams what is allowed) to get incremental conversions independent of tracking; compare with the reconstructed number. Use marketing mix modelling only as a slow cross-check.
5. Recalibrate bidding. The bid model learned from labels that were 40% of orders; now labels are 28%. Do not simply retrain on the new, thinner labels. Add a calibration layer that maps predicted probability to estimated true conversion rate, fitted on the anchored estimate, and refit weekly with a stability guard on the bid change.
6. Checks: consent share by day and segment, ratio of attributed to first-party orders over time, an A/A comparison, sensitivity of the estimate to the anchor assumption, and a before/after comparison on a campaign with no change.

**Metrics:**
- Attributed share = attributed conversions / first-party orders (40% before, 28% after).
- Visible share = conversions seen by new reporting / true conversions in the anchor segment; true estimate = reported / visible share.
- Calibration = predicted conversions / estimated true conversions by decile; aim near 1 after the fix.
- Guardrails: spend change per day, cost per estimated true conversion, and bid change cap.

**Risks:**
- The anchor segment (logged-in users) may differ from everyone, so the estimate carries that bias; report a range.
- Assuming the old 10,000 was complete; it included its own gaps and modelled credit.
- Retraining on 28% labels without correction lowers bids and loses auctions for no reason.
- Treating consent as exogenous: whoever clicks "allow" may behave differently, which is the whole problem.
- Any rule about what data may be used under the new consent state is a question for the privacy and legal teams.

**What the interviewer scores:**
- Strong: computes 30%, 11,667 and 16.7%, and uses the flat 25,000 orders to challenge the scale-up.
- Strong: names consent selection and a first-party anchor, and states what the anchor assumes.
- Strong: proposes a holdout for incrementality and a calibration layer instead of naive retraining.
- Weak: "divide by 0.6", or "conversions fell 30%, so performance fell 30%".

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Only 60% allow tracking, so I scale up 7,000 by 1 over 0.6 and get 11,667."
- Strong: "That says conversions rose 16.7% on a day when first-party orders did not move, so it is wrong. Reporting kept 70% of volume with 60% consent, which suggests consenters convert more. I would anchor on first-party orders and a segment where we see everyone, measure the visible share, and check it with a geo holdout. Then I would add a calibration layer to the bid model and cap day-to-day bid changes."

**Code:**
```python
import numpy as np

before, after, consent, orders = 10_000, 7_000, 0.60, 25_000
drop = 1 - after / before
naive = after / consent
assert abs(drop - 0.30) < 1e-12 and round(naive) == 11_667
print("drop", drop, "naive scale-up", round(naive), "vs before", round(naive / before - 1, 3))
assert round(naive / before - 1, 3) == 0.167

# What the numbers say: first-party orders are flat, so true conversions did not rise 16.7%.
cov_before, cov_after = before / orders, after / orders
print("attributed share of orders before/after:", cov_before, cov_after)
assert cov_before == 0.40 and cov_after == 0.28
# Proportional loss would give 6,000 (60% of 10,000); we see 7,000, so reporting kept 70% of volume.
implied_factor = (after / before) / consent
print("observed retention / consent share =", round(implied_factor, 3))
assert round(implied_factor, 3) == 1.167       # consenters appear to convert 16.7% more often (or modelled credit fills the gap)

# Calibration scalar for the bid model: attributed conversions per order dropped 40% -> 28%.
# If the bid model predicts P(conversion) learned on old labels, its predictions are now ~30% too high
# relative to the new reported labels, but NOT too high relative to true conversions.
true_per_day = orders * cov_before            # assumption: old attribution was ~complete (test with a holdout!)
print("if old reporting was complete, true attributed-eligible conversions/day ~", true_per_day)
assert true_per_day == 10_000

# Simulation: consenters differ from non-consenters
rng = np.random.default_rng(16)
n = 200_000
consent_flag = rng.random(n) < consent
rate = np.where(consent_flag, 0.0467, 0.0333)    # consenters convert 1.4x more (illustrative)
conv = rng.random(n) < rate
true_total = conv.sum(); seen = conv[consent_flag].sum()
scaled = seen / consent
print("sim: true", true_total, "seen", seen, "naive scaled", round(scaled), "ratio", round(scaled / true_total, 3))
assert scaled > 1.1 * true_total               # naive scale-up overstates when consenters are better converters
# Fix with a stratified ratio: calibrate on a segment where outcomes are known for everyone (first-party logged-in users)
logged = rng.random(n) < 0.3
ratio = conv[logged & consent_flag].sum() / conv[logged].sum()   # share of true conversions visible among logged-in
est = seen / ratio
print("sim: estimate scaled by visible share in logged-in segment", round(est), "true", true_total)
assert abs(est / true_total - 1) < 0.05
```

**Output (my run):**
```
drop 0.30000000000000004 naive scale-up 11667 vs before 0.167
attributed share of orders before/after: 0.4 0.28
observed retention / consent share = 1.167
if old reporting was complete, true attributed-eligible conversions/day ~ 10000.0
sim: true 8168 seen 5482 naive scaled 9137 ratio 1.119
sim: estimate scaled by visible share in logged-in segment 8201 true 8168
```

**Follow-ups:**
- What if no first-party anchor exists? Use a holdout or geo experiment as the anchor, and mark all figures as ranges.
- Should you use the modelled conversions the platform reports? Treat them as an input to be validated against your holdout, not as truth; ask the platform team how they are produced.
- How often do you recalibrate? Weekly at first, with an alert when the visible share moves more than a set band.

**Common mistakes:**
- Scaling by consent share alone.
- Believing the old reporting was complete.
- Retraining directly on the thin labels.
- Changing bids by a large step in one day.

### Q17 ⭐⭐ 🟢 Fintech: A lender can set one of three cutoffs on a score. Cutoff A approves 40,000 of 100,000 applicants with a bad rate of 2% of approved, cutoff B approves 55,000 with 3.5% and cutoff C approves 70,000 with 6% (bad rates are projections). A good customer yields a profit of 1,000 and a bad one a loss of 6,000, so compute the total profit at each cutoff, the bad rate of the extra applicants between cutoffs and the break-even bad rate, then say which cutoff you would pick and what you would check first.
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would pick cutoff B: total profit is 41.5 million against 34.4 million for A and 40.6 million for C, because the extra applicants from A to B have a 7.5% bad rate (below the 14.3% break-even) and the extra from B to C have 15.2% (above it), and first I would check that those bad rates are calibrated on a recent, out-of-time sample.

**Clarifying questions:**
- Are the bad rates projections from a model, and how were they validated (out-of-time, reject-inference-free)? Everything below depends on them.
- Is the profit of 1,000 per good customer and the loss of 6,000 per bad customer net of funding cost, servicing and recoveries, and over what horizon? The break-even rate depends on this ratio.
- Is there a capital or exposure limit that caps the approvals? It might rule out C regardless of profit.
- Will the bad rate of the marginal band hold when the economy changes? The marginal customers are the most sensitive.
- Does the choice need fair-lending or model-risk review before changing the cutoff? That is a question for compliance and the model-risk team.

**Approach:**
1. Set up the economics. Break-even bad rate = 1,000 / (1,000 + 6,000) = 14.3%: a customer is worth taking if the chance of bad is below that.
2. Compute profit at each cutoff. Profit = (approved - bad) x 1,000 - bad x 6,000. A: 800 bad, profit 34,400,000. B: 1,925 bad, profit 41,525,000. C: 4,200 bad, profit 40,600,000 (illustrative currency units, undiscounted).
3. Use marginal bands, not averages. A to B adds 15,000 applicants and 1,125 bad, a marginal bad rate of 7.5%, profit +7,125,000. B to C adds 15,000 and 2,275 bad, 15.2%, profit -925,000. The overall bad rates of 3.5% and 6% hide that the C band is worse than break-even.
4. Test the sensitivity. If every bad rate is 20% higher, B is still best (38.8 million). At 50% higher B is still best. At double, A wins (28.8 million against 28.05 million). So B is robust to moderate error but not to a doubling.
5. Check first: that the projected rates hold on recent data. Backtest the score on the latest matured cohort, look at calibration in the 40,000 to 55,000 band in particular, and check drift since training. The B to C margin (15.2% versus 14.3%) is thin, so small error flips it.
6. Decide and monitor. Choose B, with a staged ramp (approve in tranches, watch early-arrears), and a trigger to tighten if the band's bad rate passes a pre-agreed level, say 10% (agree it with risk).

**Metrics:**
- Bad rate = accounts bad within the horizon / accounts approved, matured only.
- Marginal bad rate of a band = extra bad / extra approved.
- Profit = good x 1,000 - bad x 6,000, with a stated horizon and discounting.
- Guardrails: early-arrears rate of the new band, concentration of exposure, calibration error by band.

**Risks:**
- Projected bad rates carry model error; the marginal band is the least reliable.
- One profit figure per applicant ignores heterogeneity (limits, price, product).
- Selection: customers near the cutoff may behave differently than the model assumes (see reject inference).
- Profit-maximising cutoffs may conflict with fairness and capital constraints; neither is in the numbers.

**What the interviewer scores:**
- Strong: computes 34.4, 41.5 and 40.6 million and the 14.3% break-even.
- Strong: uses marginal bands (7.5% and 15.2%), explaining why averages mislead.
- Strong: runs a sensitivity and names validation of the projected bad rates as the first check.
- Weak: picks the lowest bad rate (A) or the largest volume (C), or compares average rates to break-even.

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "A has the lowest bad rate, so choose A. Or C because it approves the most."
- Strong: "I compute profit at each: 34.4, 41.5 and 40.6 million. Break-even is 14.3% bad. The 15,000 extra people from A to B have a 7.5% bad rate and add 7.1 million; the next 15,000 have 15.2% and lose 0.9 million. So B. Before committing I would backtest the score's calibration in that band on a recent cohort, because B beats A even at a 50% worse bad rate but loses to A at double."

**Code:**
```python
from fractions import Fraction as F

good_profit, bad_loss = 1000, 6000
cuts = {"A": (40_000, F(2, 100)), "B": (55_000, F(35, 1000)), "C": (70_000, F(6, 100))}
be = F(good_profit, good_profit + bad_loss)
print("break-even bad rate:", float(be))
assert abs(float(be) - 0.142857) < 1e-5

def profit(n, r):
    bad = n * r
    return (n - bad) * good_profit - bad * bad_loss
P, BAD = {}, {}
for k, (n, r) in cuts.items():
    BAD[k] = n * r
    P[k] = profit(n, r)
    print(k, "approved", n, "bad", int(BAD[k]), "profit", int(P[k]))
assert (int(BAD["A"]), int(BAD["B"]), int(BAD["C"])) == (800, 1925, 4200)
assert (int(P["A"]), int(P["B"]), int(P["C"])) == (34_400_000, 41_525_000, 40_600_000)

# Marginal bands
for a, b in (("A", "B"), ("B", "C")):
    extra = cuts[b][0] - cuts[a][0]
    xbad = BAD[b] - BAD[a]
    xr = xbad / extra
    delta = P[b] - P[a]
    print(a, "->", b, "extra", extra, "extra bad", int(xbad), "marginal bad rate", round(float(xr), 4), "profit change", int(delta))
    assert delta == (extra - xbad) * good_profit - xbad * bad_loss
    assert (xr < be) == (delta > 0)
assert round(float((BAD["B"] - BAD["A"]) / 15_000), 3) == 0.075
assert round(float((BAD["C"] - BAD["B"]) / 15_000), 4) == 0.1517

# Sensitivity: multiply every bad rate by a factor
best = {}
for f in (F(1), F(12, 10), F(15, 10), F(2)):
    pr = {k: profit(n, r * f) for k, (n, r) in cuts.items()}
    best[float(f)] = max(pr, key=pr.get)
    print("bad rates x", float(f), "best cutoff", best[float(f)], {k: int(v) for k, v in pr.items()})
assert best[1.0] == "B" and best[2.0] == "A"
# How far can the A->B band bad rate rise before B is worse than A?
print("A->B band can rise from 7.5% to", round(float(be), 4), "before the extra applicants lose money")
```

**Output (my run):**
```
break-even bad rate: 0.14285714285714285
A approved 40000 bad 800 profit 34400000
B approved 55000 bad 1925 profit 41525000
C approved 70000 bad 4200 profit 40600000
A -> B extra 15000 extra bad 1125 marginal bad rate 0.075 profit change 7125000
B -> C extra 15000 extra bad 2275 marginal bad rate 0.1517 profit change -925000
bad rates x 1.0 best cutoff B {'A': 34400000, 'B': 41525000, 'C': 40600000}
bad rates x 1.2 best cutoff B {'A': 33280000, 'B': 38830000, 'C': 34720000}
bad rates x 1.5 best cutoff B {'A': 31600000, 'B': 34787500, 'C': 25900000}
bad rates x 2.0 best cutoff A {'A': 28800000, 'B': 28050000, 'C': 11200000}
A->B band can rise from 7.5% to 0.1429 before the extra applicants lose money
```

**Follow-ups:**
- What if the extra band's bad rate is uncertain by +/- 3 points? B to C at 15.2% could be 12% to 18%, so C is a coin flip; stay at B and gather data.
- How would you add capital cost? Subtract a per-account cost from the good-customer profit, which lowers the break-even bad rate.
- Could you price instead of rejecting? Yes, higher rates on the riskier band can lift profit, subject to the pricing and fair-lending rules, which are for the compliance team to specify.

**Common mistakes:**
- Comparing average bad rates to the break-even instead of the marginal rate.
- Ignoring that the rates are projections.
- Forgetting the cost of 6,000 versus the profit of 1,000 asymmetry (a bad customer costs 6 good ones).
- Not checking constraints beyond profit.

### Q18 ⭐⭐ 🟢 E-commerce: An audit team hand-labelled a random sample of 500 reviews and found 60 fake (12%, a sample estimate). A classifier flagged 150 of the same 500 reviews and 54 of the flagged ones were fake. Compute its precision and recall on this sample and an approximate 95% interval for the true fake share using the normal approximation, and say what you would do with the flagged reviews before taking them down.
**Asked at:** Marketplace-trust material (a prachub Amazon fake-review question on detection signals and impact metrics, an Interview Query fake-review prompt and DoorDash and Thumbtack data scientist guides on marketplace analytics); prep-site material and one estimate-based news item, no confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** On this sample the classifier has precision 36% and recall 90%, and the fake share is about 12% (9.2% to 14.8%), so I would not take down flagged reviews automatically: two in three flagged reviews are genuine; I would use the flags to prioritise human review and graded actions.

**Clarifying questions:**
- Was the 500 a simple random sample, and were the auditors blind to the classifier flags? Otherwise the audit labels are biased toward the model.
- What is the audit's own reliability (two auditors, agreement)? 60 fake labels are only as good as the labelling.
- What is the action on a flag: removal, hiding, a badge, a lower rank? Cost of a wrong action differs for each.
- Which threshold gave 150 flags, and can it be moved? A higher threshold trades recall for precision.
- Is the 12% the same in all categories and for new versus old products? One sample may hide big differences.

**Approach:**
1. Compute from the sample. Precision = 54 / 150 = 36%. Recall = 54 / 60 = 90%. The classifier flags 150 / 500 = 30% of reviews while only 12% are fake.
2. Interval for the fake share. p = 60 / 500 = 0.12, standard error = sqrt(0.12 x 0.88 / 500) = 0.0145, so 0.12 +/- 1.96 x 0.0145 gives 9.2% to 14.8%. The normal approximation is fine here because both 60 and 440 are well above 10.
3. Add intervals for precision and recall. With only 150 flagged and 60 fake, precision is 29% to 44% and recall 80% to 95% (Wilson intervals in the run). The recall interval is wide because only 60 fakes were in the sample.
4. Spell out what a blanket takedown does. Scaled to an illustrative 1,000,000 reviews: 300,000 flagged, of which 192,000 would be genuine, and about 12,000 fake reviews would still be missed. That is a lot of wrongly removed customers' content.
5. Use the flags in tiers. Rank by score; send the top slice (higher precision) to human reviewers, with extra signals (account age, device, burst patterns, text similarity); auto-act only above a threshold where audited precision is high; for the middle, use reversible actions (lower weight in the rating, no removal) and an appeal path.
6. Keep auditing. Draw a fresh random sample each month for the base rate, and a stratified sample by score band to measure precision per band, so thresholds can be set from data.

**Metrics:**
- Precision = flagged and fake / flagged = 54 / 150 = 36%.
- Recall = flagged and fake / fake = 54 / 60 = 90%.
- Fake share = fake / sampled reviews = 12% with a 95% interval of 9.2% to 14.8%.
- Guardrails: wrongly removed genuine reviews (appeals upheld), reviewer agreement, time to action, and effect on seller ratings.

**Risks:**
- The audit sample is small for recall (60 positives).
- Fraudsters adapt; a stable precision today may fall.
- Auditors who see the model flag may anchor on it.
- Removing genuine reviews harms honest sellers and shoppers.
- Any rule on how reviews may be removed or disclosed is for the trust and legal teams to specify.

**What the interviewer scores:**
- Strong: gets 36%, 90% and 9.2% to 14.8%, and notes how the interval is built.
- Strong: sees that precision, not recall, makes automatic takedown unsafe, and quantifies it.
- Strong: proposes tiers, human review, appeals and ongoing random audits.
- Weak: "recall is 90% so it is great", or removing everything flagged.

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Ninety per cent recall is excellent, so I would remove all flagged reviews."
- Strong: "Of 150 flagged, 54 are fake, so precision is 36%. At a million reviews that would remove about 192,000 genuine ones. Fake share is 12%, with a 95% interval of 9.2% to 14.8%. I would send the highest-scoring flags to human review with extra signals, only auto-act where audited precision is high, and keep a monthly random audit so the threshold rests on measured numbers."

**Code:**
```python
import numpy as np

n, fake, flagged, tp = 500, 60, 150, 54
precision, recall = tp / flagged, tp / fake
assert precision == 0.36 and recall == 0.90
p = fake / n
se = np.sqrt(p * (1 - p) / n)
lo, hi = p - 1.96 * se, p + 1.96 * se
assert p == 0.12 and abs(se - 0.014532) < 1e-5
assert round(lo, 3) == 0.092 and round(hi, 3) == 0.148
assert n * p >= 10 and n * (1 - p) >= 10          # normal approximation is reasonable
print("fake share", p, "95% interval", round(float(lo), 3), round(float(hi), 3))
print("precision", precision, "recall", recall, "flag rate", flagged / n)

def wilson(k, m, z=1.96):
    ph = k / m
    c = (ph + z * z / (2 * m)) / (1 + z * z / m)
    h = z * np.sqrt(ph * (1 - ph) / m + z * z / (4 * m * m)) / (1 + z * z / m)
    return c - h, c + h
pl, ph_ = wilson(tp, flagged); rl, rh = wilson(tp, fake)
print("precision 95% (Wilson)", round(float(pl), 3), round(float(ph_), 3))
print("recall 95% (Wilson)", round(float(rl), 3), round(float(rh), 3))
assert pl < precision < ph_ and rl < recall < rh

# Cost of a blanket takedown of flagged reviews, scaled to an illustrative 1,000,000 reviews
reviews = 1_000_000
flag_n = reviews * flagged / n
wrong = flag_n * (1 - precision)
print("flagged", int(flag_n), "genuine reviews taken down", int(wrong), "fake reviews missed", round(reviews * 0.12 * (1 - recall)))
assert int(flag_n) == 300_000 and int(wrong) == 192_000

# Review queue: if humans check flagged reviews, how many fake per 100 checked vs random review?
print("fake per 100 reviews checked: flagged", 100 * precision, "random", 100 * p)
assert 100 * precision == 36 and abs(100 * precision / (100 * p) - 3.0) < 1e-9     # 3x lift over random
```

**Output (my run):**
```
fake share 0.12 95% interval 0.092 0.148
precision 0.36 recall 0.9 flag rate 0.3
precision 95% (Wilson) 0.288 0.439
recall 95% (Wilson) 0.799 0.953
flagged 300000 genuine reviews taken down 192000 fake reviews missed 12000
fake per 100 reviews checked: flagged 36.0 random 12.0
```

**Follow-ups:**
- How big an audit sample do you need? For a 95% interval of +/- 1 point at 12%, about 4,060 reviews (1.96^2 x 0.12 x 0.88 / 0.01^2), more for per-category estimates.
- How would you raise precision? Raise the threshold, add features, or require agreement from a second model; recall will fall, so measure both.
- Why a Wilson interval for precision? It behaves better than the simple normal one when the proportion is far from 0.5 or the sample is small.

**Common mistakes:**
- Reading recall alone.
- Assuming the 12% is exact.
- Taking down flagged reviews with no review or appeal.
- Using flagged-only data to estimate the fake share.

### Q19 ⭐⭐ 🟢 Healthcare: A model was trained on 120,000 patient records and 15,000 patients (12.5% of the records) later withdrew consent for research use. Retraining from scratch takes 3 days of compute plus a clinical re-validation, and the product team asks whether the deployed model can keep running. What do you tell them, what questions do you take to the privacy and compliance teams, and how would you design the pipeline so withdrawals are cheap to honour next time?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to consent withdrawal and data lineage in health-data privacy material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Whether the deployed model may keep running is not my call or the product team's: I would tell them it is a question for the privacy and compliance teams, bring them the facts they need (which records, which models, what retraining costs), prepare the retrain without the 15,000 patients now, and build a consent ledger so the next withdrawal is a filter, not a project.

**Clarifying questions:**
- What exactly was consented to, and what does withdrawal cover: future use, deletion of the raw records, or also models and derived data? That wording is for the privacy officer and legal to interpret.
- Does the model contain identifiable information (could it memorise records), or only aggregate patterns? It affects the risk discussion; I would ask the privacy team how they treat it.
- Where else do the 15,000 patients' data live: feature tables, embeddings, validation sets, logs, backups, vendors? We need an inventory.
- Is the 12.5% a one-off or a trend? A trend changes how we design the pipeline.
- Does the clinical safety side tolerate running the current model while the retrain is validated, or is switching it off safer for patients? That is for the clinical owner to decide.

**Approach:**
1. Do the arithmetic. 15,000 / 120,000 = 12.5%, so 105,000 records remain. The retrain is 3 days of compute plus a clinical re-validation; that is the cost of compliance, not a reason to delay the question.
2. Tell product plainly: I cannot say it is fine or not. I will take the options to privacy, compliance and the clinical owner this week, and give them a decision memo: (a) keep running until a retrained model is validated, with a stated end date; (b) switch to the previous model if one was trained without these patients; (c) pause the service. Each has a patient-safety cost and a privacy position; they choose.
3. Do the technical work in parallel. Start the retrain on the 105,000 now, in a staging area, so no time is lost whatever the decision is. Compare it with the current model on the validation set (also with withdrawn patients removed) to measure the performance change; with 87.5% of the data, a small change is plausible but must be measured.
4. Answer the data-side questions. List all copies and derived artefacts of the 15,000 patients' data, and the model versions trained on them. Questions to take to privacy and compliance: what must be deleted and by when, whether trained models count, what to tell clinicians and patients, what to record as evidence, and whether past analyses stay valid.
5. Design for cheap withdrawals. Keep a consent ledger (patient, purpose, status, effective date). Build the training table by joining that ledger at build time, record the manifest hash of each training set in the model registry, and keep lineage from raw data to features to model. A withdrawal then triggers a filter and a scheduled retrain, not an investigation.
6. Plan the retrain cadence. Retrain on a fixed schedule (for example monthly or quarterly) so that withdrawals are absorbed in routine releases, with the validation pack automated. Sharding the training data can reduce retrain work for rare withdrawals, but not for a batch like this (see the run).

**Metrics:**
- Withdrawn share = withdrawn records / training records = 12.5%.
- Time to honour = time from withdrawal request to the first deployed model without that patient (target set with the privacy team).
- Lineage coverage = records with consent status and lineage / all records (target 100%).
- Retrain performance delta = metric(retrained) - metric(current) on the same validation set, with an interval.
- Guardrails: no withdrawn id in any training manifest (checked by test), and clinical validation sign-off before release.

**Risks:**
- Assuming that removing rows from a table also removes their influence on a trained model; whether that is acceptable is a policy question.
- Missed copies: validation sets, exports and backups still containing the patients.
- Retraining quickly without re-validation, which trades a privacy risk for a safety risk.
- Hard-coding the answer ("keep running") when the rule might say otherwise.

**What the interviewer scores:**
- Strong: separates decisions (privacy, compliance, clinical) from the engineering work, and says so without stating rules as facts.
- Strong: gets 12.5% and 105,000, starts the retrain in parallel and measures the performance change.
- Strong: proposes a consent ledger joined at build time, manifest hashes and lineage.
- Weak: "it is fine, the model is anonymous", or "we must shut it down" with no questions asked.

**Example:** Illustrative. Weak versus strong:
- Weak: "The model does not store patient data, so it can keep running. I would just remove them next time."
- Strong: "I cannot decide that; the privacy and compliance teams and the clinical owner do. I will give them the options and the facts: 15,000 of 120,000 records, 12.5%, a 3-day retrain plus validation, and an inventory of every copy. I start the retrain on the 105,000 records now so we lose no time, and I will build a consent ledger joined at training time so a withdrawal is a filter and a scheduled retrain."

**Code:**
```python
import hashlib
import numpy as np

total, withdrawn = 120_000, 15_000
share = withdrawn / total
remaining = total - withdrawn
assert share == 0.125 and remaining == 105_000
print("withdrawn share", share, "remaining records", remaining)

# Consent ledger joined at training-table build time
rng = np.random.default_rng(19)
ids = np.arange(total)
w_ids = rng.choice(ids, withdrawn, replace=False)
status = np.full(total, "active", dtype=object)
status[w_ids] = "withdrawn"
train_ids = ids[status == "active"]
assert train_ids.size == remaining and not np.isin(train_ids, w_ids).any()

def manifest_hash(a):
    return hashlib.sha256(np.sort(a).tobytes()).hexdigest()[:12]
print("old manifest", manifest_hash(ids), "new manifest", manifest_hash(train_ids))
assert manifest_hash(ids) != manifest_hash(train_ids)

# Sharded training (K shards, each model trained on one shard): how many shards must be retrained?
K = 20
def expected_shards_touched(w, K=K):
    return K * (1 - (1 - 1 / K) ** w)
for w in (1, 10, 100, 15_000):
    print("withdrawals", w, "expected shards to retrain of", K, ":", round(expected_shards_touched(w), 2))
assert round(expected_shards_touched(1), 2) == 1.0
assert round(expected_shards_touched(10), 2) == 8.03
assert round(expected_shards_touched(15_000), 2) == 20.0   # a 12.5% batch touches every shard: sharding gives no saving

# Cost of waiting: retrain is 3 days compute; if withdrawals arrive weekly and we batch them
retrain_days = 3
batch_weekly_share = withdrawn / total / 52
print("if the same share arrived evenly over a year, weekly share:", round(batch_weekly_share * 100, 3), "%")
assert retrain_days == 3 and round(batch_weekly_share * 100, 3) == 0.24
```

**Output (my run):**
```
withdrawn share 0.125 remaining records 105000
old manifest be0eeae2d5b5 new manifest 4a77392a8266
withdrawals 1 expected shards to retrain of 20 : 1.0
withdrawals 10 expected shards to retrain of 20 : 8.03
withdrawals 100 expected shards to retrain of 20 : 19.88
withdrawals 15000 expected shards to retrain of 20 : 20.0
if the same share arrived evenly over a year, weekly share: 0.24 %
```

**Follow-ups:**
- Can you "unlearn" instead of retraining? Approximate unlearning methods exist in the research literature (editor knowledge, not tested here); whether any is acceptable is a question for privacy and compliance, and validation is still needed.
- What if the retrained model is clearly worse? Report the delta to the clinical owner; options include more data from consented sources, or accepting a shorter-lived model; they decide.
- What do you log for audit? The ledger entry, the manifest hash of each training set, the model version, and the date of the deployed model that excludes the patient.

**Common mistakes:**
- Treating a privacy question as an engineering call.
- Deleting rows but leaving copies in features, validation sets or backups.
- Not recording which model was trained on which manifest.
- Planning for one withdrawal, not for a flow of them.

### Q20 ⭐⭐ 🟢 Ads: For a retail campaign, the measured incremental conversion probability per user from the 1st, 2nd, 3rd and 4th impression in a week is 0.50%, 0.30%, 0.15% and 0.05%. A conversion is worth 20 and each impression costs 0.05. Compute the net value of each impression and the best weekly cap, and explain how you would check that these incremental numbers are causal.
**Asked at:** Ad-serving system-design material (techinterview.org ad serving and real-time bidding pages, a Dataford question on budget pacing and frequency capping, machinelearningatscale.com on frequency capping; feedback-controller pacing, per-user counters and credits for invalid clicks appear in the snippets); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The net value per impression is +0.05, +0.01, -0.02 and -0.04, so the best weekly cap is 2 (cumulative net 0.06 per user), but the second impression clears break-even by only 0.05 points, so I would confirm the numbers with a randomised frequency test before setting the cap.

**Clarifying questions:**
- How were the incremental probabilities measured: randomised holdout, ghost ads, or observational attribution? Only the first two are causal.
- Is a conversion worth a flat 20, or does value vary by customer? Variable value changes the break-even per user.
- Is the 0.05 cost an average? Costs may differ by placement or auction, and later impressions may be cheaper.
- Are the probabilities conditional on a user reaching that impression? Users who reach the 4th are a selected group.
- Within what window is the conversion counted (the same week, 7 or 30 days)? A longer window changes later impressions' value.

**Approach:**
1. Compute net value per impression = incremental probability x 20 - 0.05. First: 0.005 x 20 = 0.10, minus 0.05 = +0.05. Second: 0.003 x 20 = 0.06, so +0.01. Third: 0.0015 x 20 = 0.03, so -0.02. Fourth: 0.0005 x 20 = 0.01, so -0.04.
2. Choose the cap by the cumulative sum, which is 0.05, 0.06, 0.04, 0.00 per user for caps 1 to 4. The maximum is at cap 2. Equivalent rule: keep adding impressions while incremental probability exceeds cost / value = 0.05 / 20 = 0.25%. The first two impressions (0.50% and 0.30%) pass; the third (0.15%) does not.
3. Note how thin the margin is. The second impression is at 0.30% against a 0.25% threshold, so if its true effect is 17% lower it is worth nothing. Treat cap 2 as the best estimate, not a certainty. Cap 1 loses only 0.01 per user compared with cap 2, so there is a cheap fallback.
4. Check causality. The numbers should come from randomisation: assign users at random to cap 1, 2, 3 and 4 (or to a holdout), then incremental probability of the k-th impression = conversion rate under cap k minus under cap k-1. Observational comparisons are confounded: heavy-exposure users are more active and more likely to buy anyway. In a simulation with zero ad effect, users who saw 4 impressions converted at 0.83% against 0.38% for 1 and 0.28% for 0 (see the run).
5. Size the test. To separate 0.30% from 0.25% at a 1% baseline conversion takes about 620,000 users per arm (80% power, 5% two-sided, illustrative); to see the full 0.30-point effect takes about 17,000 per arm. If that is too large, test cap 1 versus cap 2 first and use the confidence interval to decide.
6. Implement and monitor. Enforce the cap with a per-user counter (including across devices where identity allows), watch spend, reach and conversions, and revisit when creative, season or audience changes; repeat the test periodically.

**Metrics:**
- Incremental probability of impression k = P(convert | cap k) - P(convert | cap k-1), from randomised arms.
- Net value per impression = incremental probability x value - cost per impression; cumulative net per user by cap.
- Break-even incremental probability = cost / value = 0.25%.
- Guardrails: reach (share of target users with at least one impression), total conversions, and spend per incremental conversion.

**Risks:**
- Confounding by user intent if the numbers are observational.
- Selection: the effect of a fourth impression is measured on those the auction reached.
- A flat value of 20 hides the mix of customers; a higher-value customer may justify a higher cap.
- Cross-device counting misses impressions, so the cap is enforced loosely.
- Cap interacts with creative fatigue and the auction; a result for one campaign may not carry over.

**What the interviewer scores:**
- Strong: gets +0.05, +0.01, -0.02, -0.04, cap 2, and the 0.25% break-even rule.
- Strong: points out the margin is thin and sets up a randomised test, with a sample-size estimate.
- Strong: explains why exposure-level comparisons are confounded.
- Weak: choosing the cap by conversion rate alone, or taking the observational lift as causal.

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Conversion keeps rising with each impression, so I would cap at 4."
- Strong: "Break-even is 0.25%, so only the first two impressions pay: +0.05 and +0.01 net, then -0.02 and -0.04. Cap 2 gives 0.06 per user. The second impression is only just above break-even, so I would run a randomised test across cap levels with several hundred thousand users per arm, because comparing heavy and light viewers measures their intent, not the ads."

**Code:**
```python
from fractions import Fraction as F
import numpy as np

inc = [F(5, 1000), F(3, 1000), F(15, 10000), F(5, 10000)]   # 0.50%, 0.30%, 0.15%, 0.05%
value, cost = 20, F(5, 100)
net = [p * value - cost for p in inc]
print("net value per impression:", [float(x) for x in net])
assert [float(x) for x in net] == [0.05, 0.01, -0.02, -0.04]
cum, run = [], F(0)
for x in net:
    run += x; cum.append(run)
print("cumulative net per user by cap 1..4:", [float(x) for x in cum])
assert [float(x) for x in cum] == [0.05, 0.06, 0.04, 0.0]
best = max(range(4), key=lambda i: cum[i]) + 1
assert best == 2
breakeven = cost / value
print("break-even incremental probability per impression:", float(breakeven))
assert float(breakeven) == 0.0025
# Margin: impression 2 clears break-even by 0.05 points; how far can its true probability fall?
margin = float(inc[1] - breakeven)
print("impression 2 margin over break-even (probability points):", round(margin * 100, 3))
assert round(margin * 100, 3) == 0.05

# Sample size to tell 0.30% from 0.25% in a two-arm randomised comparison (cap 2 vs cap 1 arms)
# Both arms convert at roughly 1% (illustrative baseline), so the variance per user is ~ p(1-p).
p0 = 0.010
za, zb = 1.96, 0.84
delta = 0.0005
n_per_arm = 2 * (za + zb) ** 2 * p0 * (1 - p0) / delta ** 2
print("users per arm to detect a 0.05-point gap at 1% baseline (80% power):", round(n_per_arm))
assert 600_000 < n_per_arm < 650_000
# And to detect the full 0.30-point effect of the 2nd impression versus zero
n_full = 2 * (za + zb) ** 2 * p0 * (1 - p0) / 0.003 ** 2
print("users per arm to detect the 0.30-point effect:", round(n_full))
assert 15_000 < n_full < 20_000

# Selection check: users who reach 4 impressions are more active. Illustrative simulation.
rng = np.random.default_rng(20)
n = 400_000
activity = rng.gamma(2, 0.5, n)                 # latent intent, mean 1
imps = np.minimum(rng.poisson(1.2 * activity), 4)
base = 0.004 * activity                        # conversion without ads depends on intent
conv = rng.random(n) < base                    # zero true ad effect
r1 = conv[imps == 1].mean(); r4 = conv[imps == 4].mean(); r0 = conv[imps == 0].mean()
print("sim with ZERO ad effect: conversion rate by impressions seen 0/1/4:", round(float(r0), 4), round(float(r1), 4), round(float(r4), 4))
assert r4 > r1 > r0                             # observational 'dose-response' appears without any causal effect
```

**Output (my run):**
```
net value per impression: [0.05, 0.01, -0.02, -0.04]
cumulative net per user by cap 1..4: [0.05, 0.06, 0.04, 0.0]
break-even incremental probability per impression: 0.0025
impression 2 margin over break-even (probability points): 0.05
users per arm to detect a 0.05-point gap at 1% baseline (80% power): 620928
users per arm to detect the 0.30-point effect: 17248
sim with ZERO ad effect: conversion rate by impressions seen 0/1/4: 0.0028 0.0038 0.0083
```

**Follow-ups:**
- What if impression costs fall for later impressions? Recompute net value with the actual cost per impression; the rule is the same (incremental probability times value above cost).
- What if conversion value varies by user? Set caps per segment, using the expected value for that segment.
- Is a cap per week the right unit? Test a per-day cap and a spacing rule too; the effect of the second impression may depend on gap.

**Common mistakes:**
- Using total conversion rate by exposure count as incremental.
- Forgetting the cost term, so every impression looks positive.
- Ignoring the 0.05-point margin of the second impression.
- Treating a cap as a purely statistical choice, not a spend and reach decision.


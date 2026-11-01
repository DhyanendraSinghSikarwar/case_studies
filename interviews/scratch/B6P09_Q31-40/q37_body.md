**Say this first (1 line):** Averaged over ages 0 to 6 the labels have seen 83.3% of eventual conversions, so the conversion rate learned is about 16.7% too low; I would fix it with a delayed-feedback model or a maturity correction, not by pretending unconverted young clicks are negatives.

**Clarifying questions:**
- Is the delay curve stable by campaign, product and day of week? A single curve is only a first approximation.
- Is the model used for bidding or ranking? Bidding needs calibrated probabilities; ranking needs order only.
- Do we get conversion events with the click ID, and how late do corrections or refunds arrive? It sets what "100% at 6 days" means.
- Are clicks equal in volume per age? The 83.3% needs equal volume; with unequal volume use a weighted average.
- How often can we retrain, and how fresh must the model be? Waiting for maturity costs freshness.

**Approach:**
1. The arithmetic: (50 + 70 + 80 + 90 + 95 + 98 + 100) / 7 = 583 / 7 = 83.29%. The relative underestimate of the conversion rate is 1 - 0.8329 = 16.7% (a true 5.0% looks like 4.16%).
2. The bias is not uniform: age-0 clicks show only half their eventual conversions (a 5% true rate looks like 2.5%), while age-6 clicks are complete. A model that sees age as a feature may learn "new clicks convert less".
3. In my simulation (200,000 clicks per age, true rate 5%), the naive training rate was 4.18% (about 0.84 of the true rate); the by-age naive rates ran from 2.53% at age 0 to 4.93% at age 6.
4. Fix A, wait: train only on clicks aged 6 days or more. Unbiased (4.93% in the run) but uses one-seventh of the clicks here and the model is a week stale.
5. Fix B, correct by maturity: divide each age bucket's conversions by the share observed at that age (the curve), estimated from older cohorts. In the run the corrected rate was 5.03%.
6. Fix C, delayed-feedback model: model P(conversion eventually) and the delay distribution separately; the observed label at age a is conversion times "delay <= a". With the curve known, the maximum-likelihood rate in my run was 4.99%. Chapelle's delayed-feedback model is the usual reference (editor knowledge; not run here).
7. Practical production rules: keep the age of the click as a training feature only if it is removed at serving time; use fresh data with corrected weights; monitor calibration on matured cohorts only (see Book 6 Part 2, Q28, on label maturation and calibration on the last seven days).
8. Report both numbers: the raw rate on young cohorts will always look low and should not trigger an alert.

**Metrics:**
- Observed share at age a = conversions seen by age a / eventual conversions (50%, 70%, ... 100%).
- Average maturity = mean of those shares over the training window = 83.29%.
- Relative underestimate = 1 - average maturity = 16.7%.
- Calibration on matured cohorts = predicted conversions / observed conversions after 6 days.
- Guardrails: freshness lag, bid error, spend efficiency.

**Risks:**
- The delay curve is itself estimated and can drift (a promotion, a payment outage).
- Late conversions that are refunded or corrected change eventual counts.
- Dividing by a small share (age 0, 50%) amplifies noise.
- Importance weights can produce huge variance; clip them.

**What the interviewer scores:**
- Strong: 83.3% and 16.7%, and the fact that age 0 is the worst.
- Strong: names the unconverted-as-negative bias, and offers wait, correct and delayed-feedback options with trade-offs.
- Strong: evaluates calibration on matured data only.
- Weak: "use more data"; "retrain more often"; no mention of delay.

**Example:** Illustrative numbers from the run. True rate 5.0%; naive training rate 4.18% (ratio 0.84); corrected 5.03%; maximum-likelihood 4.99%.
- Weak: "The conversion rate looks lower this week, so the model should predict lower."
- Strong: "Our 7-day window has only about 83% of eventual conversions, so training labels understate the rate by about 17%, and 50% of conversions are missing for the newest clicks. I would divide by the observed share per age or fit a delayed-feedback model, and I would check calibration on clicks older than 6 days."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *What if the window is 14 days?* Average maturity rises (more complete days), but the freshness cost rises too.
- *Does the bias affect ranking?* Only if the bias differs by campaign or age mix, which it often does.
- *Why not just wait 6 days?* Fine when freshness is not important; ads usually need fresher models.

**Common mistakes:**
- Treating all unconverted clicks as true negatives.
- Averaging maturity with unequal click volume per age.
- Alerting on young-cohort calibration.
- Using the age as a feature at serving time.

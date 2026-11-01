**Say this first (1 line):** Yesterday's cohort has had only a fraction of its seven days to convert, so the observed rate is low by construction; I compare the model against a maturity-adjusted expectation, or only evaluate cohorts that have finished their window, and I set alerts on matured cohorts.

**Clarifying questions:**
- What is the conversion-delay curve (share of eventual conversions by day since click)? It converts "age 1 day" into an expected share of matured conversions.
- Is the attribution window fixed at seven days for every conversion, and does the model predict conversion within seven days? The label definition must match the window.
- Is the observed 1.5% the same cohort the model scored at 5%? Cohort and prediction date must match.
- Do delays vary by channel or product? A single curve may not fit all.
- How quickly do we need an alert? The answer sets whether we adjust or wait.

**Approach:**
1. Define the label as "converted within seven days of exposure" and write down that it is only complete once seven days have passed.
2. Compute calibration by cohort age (days since exposure). Recent cohorts will look over-predicted; older ones converge to the true level.
3. Estimate the delay curve from fully matured cohorts: share of conversions by day 1, 2, ... 7.
4. Evaluate recent cohorts against a maturity-adjusted prediction: expected observed rate = predicted rate x share matured at that age. Or exclude cohorts younger than seven days.
5. Alert rules: use only matured cohorts for the main calibration alert; use a separate "early read" with the maturity adjustment and a wider band; log cohort age with every metric.
6. Check the adjusted ratio is about 1.0; if not, then look for real miscalibration (traffic mix, tracking, model).

**Metrics:**
- Calibration ratio = sum of predicted conversions / sum of observed conversions, by cohort age.
- Maturity-adjusted ratio = observed rate / (predicted rate x matured share at age).
- Matured share at age d = share of eventual conversions that happen by day d.
- Guardrails: sampling noise (standard error of a rate) so alert bands reflect cohort size.

**Risks:**
- An alert on immature cohorts fires every day and trains people to ignore it.
- The delay curve shifts over time (channel change, a product change), which makes the adjustment wrong.
- Right-censored data also biases training sets: new rows have fewer positive labels.
- Adjusting too aggressively hides a real problem in recent data.

**What the interviewer scores:**
- Strong: names right-censoring / label maturation and shows the ratio converges with age. Weak: "the model is badly calibrated, recalibrate".
- Strong: gives a maturity-adjusted metric or an age cut-off. Weak: waits without a plan.
- Strong: links it to alert design and to training data. Weak: stops at diagnosis.

**Example:** (illustrative) The model predicts 5% and the true seven-day rate is 5%. If 30% of eventual conversions happen by day 1, yesterday's cohort shows 0.05 x 0.30 = 1.5%, and the naive ratio of predicted to observed is 3.33 (5 divided by 1.5). In a seeded simulation with 200,000 users per cohort the observed rate by cohort age (days 1 to 7) is 1.55%, 2.57%, 3.22%, 3.88%, 4.43%, 4.73% and 4.93%, so the predicted-to-observed ratio goes 3.23, 1.95, 1.55, 1.29, 1.13, 1.06, 1.01. Maturity-adjusted, yesterday's ratio is 1.03. The standard error of a 5% rate on a 20,000-user cohort is 0.0015, so an alert band is about plus or minus 0.003. Weak: "Predicted 5% versus 1.5% means we are 3.3 times off." Strong: "Cohort age is one day; expected observed is 1.5%, so the model is fine."

**Code:**

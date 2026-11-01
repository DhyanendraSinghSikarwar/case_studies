**Say this first (1 line):** A 30-day-old window shows 0.12% fraud (60% of the true 0.2%) and a 90-day-old window shows 0.18% (90%), so I would never read recent label rates as truth: I would correct for maturity, train on the freshest window that is mostly matured, and use early proxy signals plus rules to cover the gap.

**Clarifying questions:**
- Is the 60% and 90% profile stable across merchants, countries and attack types? A single maturity curve is the whole basis of any correction.
- Besides chargebacks, are there faster labels (customer disputes, issuer confirmations, manual reviews)? They let me react before day 30.
- What do we do on a flagged transaction (block, step-up check, review)? Blocked fraud never produces a chargeback, so labels are censored by our own decisions.
- Is the 0.2% a measured rate or a planning figure? The question gives it as an assumption; I would check it on mature cohorts.
- What are the loss per missed fraud and the cost per false decline? They fix the threshold and the value of waiting for labels.

**Approach:**
1. Clarify and frame. State the problem: labels lag by months, the world changes weekly. Goal is a monthly retrained model, launched in 12 weeks (84 days, which is less than the 90 days needed for mostly matured labels).
2. Metrics and guardrails. Model: precision-recall at the review capacity, recall at a fixed false-decline rate, calibration. Business: fraud loss per 10,000 transactions, false-decline rate. Guardrails: review queue size, approval rate, latency.
3. Data and labels. Build a maturity table by label age. Use matured rows (about 90 days old) for the main training and evaluation; use younger rows only with a maturity correction or with fast proxy labels (disputes, confirmed review outcomes). Keep a small random "no-block" or low-friction audit slice to learn about blocked traffic, if the risk owner agrees.
4. Baseline first. Rules plus a simple model on matured data; this is what ships in week 12. Compare any complex model against it.
5. Model and trade-offs. Gradient-boosted trees on transaction, device and history features. The trade-off is freshness versus label quality: a 90-day lag keeps labels clean but the model is about 105 days behind on average between retrains (see the code); mitigate with fast-moving features, rules for new attacks and a recency-weighted loss.
6. Evaluation. Offline: out-of-time split on matured data (train on older months, test on a later matured month), never random split. Online: shadow mode first, then a small traffic slice with a champion-challenger comparison on maturity-corrected loss.
7. Launch and experiment plan. Shadow weeks 8 to 10, 5% to 25% traffic weeks 11 to 12. Decision at each stage on corrected fraud caught and false declines, not on raw label rates.
8. Monitoring, retraining and risks. Monitor score drift, feature drift, approval rate and early-label rates by age cohort; report fraud rate only per maturity cohort. Retrain monthly, and trigger an earlier retrain on an attack spike.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 8, 4, 8, 7, 5, 5.

**Metrics:**
- Apparent fraud rate at age a = chargebacks observed by age a / transactions = true rate x maturity(a): 0.2% x 0.60 = 0.12%; 0.2% x 0.90 = 0.18%.
- Maturity-corrected rate = apparent rate / maturity(a), which returns 0.2% from either window if the profile holds.
- Recall at fixed false-decline rate, precision at review capacity, expected loss per 10,000 transactions.
- Guardrails: approval rate, review queue length, p99 scoring latency, share of fraud caught by rules only.

**Risks:**
- Reading the last 30 days' 0.12% as a drop in fraud and relaxing controls.
- Training on young rows with a "not yet fraud" label for transactions that will become chargebacks (label noise that teaches the model to approve).
- Censoring: our own blocks hide fraud, so labels come mostly from approved traffic.
- The maturity profile can shift (new issuers, new attack types), so a fixed correction factor can mislead.
- Any claim about rules for chargebacks, dispute windows or customer data: ask compliance and legal.

**What the interviewer scores:**
- Strong: 0.12% and 0.18% against a true 0.2%, and the correction by dividing by maturity.
- Strong: out-of-time evaluation, fast proxy labels, and a plan for the first 12 weeks.
- Strong: names censoring from blocking and a stable-profile assumption.
- Weak: random train-test split on immature labels, or treating the recent low rate as good news.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "Fraud was only 0.12% last month, so the new model works and we can reduce reviews."
- Strong: "A 30-day-old window can only show 60% of the true 0.2%, which is 0.12%, and a 90-day-old window shows 0.18%. So I would divide by the maturity share before comparing, train on rows at least 90 days old, use disputes as an early signal, and judge the launch in shadow mode on maturity-corrected loss, with rules covering the newest attack patterns."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if the maturity curve changes? Re-estimate it every month on cohorts old enough to be nearly complete, and report the correction with a range rather than one number.
- Can you learn from blocked transactions? Only with a deliberately small unblocked audit slice, approved by the risk owner, or with methods that adjust for selection; otherwise label bias remains.
- How would you cut the 90-day wait? Use faster signals (disputes, confirmed review outcomes) as an early label with its own calibration to final chargebacks.

**Common mistakes:**
- Calling the apparent rate "the fraud rate" without the age of the window.
- Random splits that leak future patterns into training.
- Using one correction factor for all merchants and countries.
- Forgetting that blocked fraud never becomes a chargeback.

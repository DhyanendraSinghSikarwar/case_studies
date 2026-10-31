### Q31 ⭐⭐ 🟡 Fintech: A credit model declined an applicant and the lender must give up to 4 plain-language reasons. Income and employment tenure have a correlation of 0.85, so their attribution scores flip between two retrains, and for 30 of 100 reviewed declines (30% of the sample) the top reason differs between retrains. How would you produce stable reasons, validate them, and decide what to ask compliance about the wording?
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Correlated features make per-feature attributions unstable, so I would explain the decline in stable reason groups (income and tenure as one "income and job stability" reason), average attributions over many retrains, test the stability on declines before launch, and ask compliance whether the wording and grouping are acceptable.

**Clarifying questions:**
- Do the reasons have to reflect the real drivers of this model, or can they be mapped from a simpler scorecard? It decides whether grouping is enough or we need a different model form.
- Which wording is fixed by compliance (a reason-code library) and which can I change? It tells me where I can group features.
- Is the flip between two retrains, or between two runs on the same model? Retrain instability is a data issue; same-model instability is a method issue (for example sampling in the attribution).
- How was the 30 of 100 chosen (the first 100 declines, or random)? A sample of 100 gives a wide range.
- Are the 4 reasons ranked or just a set? A ranked list needs stable order; a set only needs stable membership.

**Approach:**
1. Size the problem. 30 of 100 is a sample. The 95% Wilson interval is about 22% to 40%, so the true flip rate is probably between a fifth and two fifths. Also measure the overlap of the whole 4-reason set, not only the top reason.
2. Find the cause. With a correlation of 0.85 the model can put credit on income or on tenure almost interchangeably. Check the spread of the two coefficients across bootstrap retrains: they move in opposite directions (negative correlation between the two coefficients).
3. Group correlated features into one reason group before ranking (income + tenure = "income and employment stability"). Rank groups, not single features.
4. Average attributions over many bootstrap retrains (bagging) and use the average for the reason, so one retrain does not decide the wording.
5. Map each group to a fixed reason code with plain wording written with compliance, so the text cannot change between retrains.
6. Validate: (a) stability: top-reason flip rate and 4-reason set overlap across retrains on a fixed set of reviewed declines; (b) fidelity: if you remove the named reason feature(s), does the score move in the right direction (counterfactual check); (c) human review: a reviewer reads 100 declines and says whether each reason is sensible for that applicant.
7. Put a stability gate in the retrain pipeline: do not promote a retrain if the flip rate on the reference declines is above an agreed limit.
8. Ask compliance (and legal, via the usual route) about: the exact reason wording, whether grouped reasons are acceptable, how many reasons and in what order, how reasons must relate to the model, and how long reason mappings must be kept. I do not assert any rule; I bring the evidence and ask.

**Metrics:**
- Top-reason flip rate = declines whose top reason differs between retrain A and B / declines reviewed (here 30 / 100 in the prompt).
- Set overlap = mean over declines of |A ∩ B| / |A ∪ B| for the 4-reason sets (Jaccard).
- Fidelity = share of declines where removing the cited feature group lowers risk (counterfactual check).
- Guardrails: model discrimination (AUC) must not fall when we regularise or group; reason coverage (declines with at least one valid reason).

**Risks:**
- Ranking by coefficient times deviation on a correlated pair is arbitrary; two retrains can both be "right".
- Grouping can hide a driver the applicant could act on (income versus tenure advice differs).
- Averaging over retrains gives stable but possibly less faithful reasons for a single model; document which model the reasons explain.
- Plain-language wording that sounds stable may still imply something untrue; get it reviewed.
- The 100-decline sample may not cover thin-file applicants.

**What the interviewer scores:**
- Strong: names correlated features as the cause, sizes the 30 of 100 with an interval, and proposes grouping plus averaging with a measured result.
- Strong: separates stability from fidelity and tests both.
- Strong: asks compliance about wording and does not state regulations as facts.
- Weak: "use SHAP" with no stability check; "drop one of the two features" without checking AUC; quoting legal rules from memory.

**Example:** Illustrative numbers, from the run below. A logistic model on 1,500 simulated applicants, income and tenure correlated at about 0.85, reasons for 100 highest-risk applicants from two bootstrap retrains.
- Raw top reason differs for 47 of 100 (the prompt's 30 of 100 is the same kind of number); grouped income and tenure: 12 of 100; bagged (60 resamples each): 17 of 100.
- Weak: "Income is the top reason for most people, we ship the SHAP output."
- Strong: "On 100 declines the top reason changes in 30, so the true rate could be 22% to 40%. Income and tenure are correlated at 0.85, so I would report them as one reason group and average over retrains. In my test that cut the flip rate from 47 to 12 of 100, and grouping changes only the explanation, so AUC is untouched. I would ask compliance to approve the group wording."

**Code:**
```python
import numpy as np

rng = np.random.default_rng(31)
names = ["income", "tenure", "debt_ratio", "utilisation", "inquiries", "file_age"]
n, p = 1500, len(names)
cov = np.eye(p)
cov[0, 1] = cov[1, 0] = 0.85            # income and tenure correlated at 0.85
X = rng.multivariate_normal(np.zeros(p), cov, size=n)
beta_true = np.array([-0.45, -0.45, 0.50, 0.40, 0.25, -0.20])
pd_true = 1 / (1 + np.exp(-(-2.0 + X @ beta_true)))
y = (rng.random(n) < pd_true).astype(float)
print("sample corr(income, tenure) =", round(np.corrcoef(X[:, 0], X[:, 1])[0, 1], 3))
assert abs(np.corrcoef(X[:, 0], X[:, 1])[0, 1] - 0.85) < 0.03

def fit(Xb, yb, l2=1e-3, it=25):
    A = np.c_[np.ones(len(Xb)), Xb]
    w = np.zeros(A.shape[1])
    for _ in range(it):                     # IRLS (Newton) for logistic regression
        mu = 1 / (1 + np.exp(-(A @ w)))
        W = mu * (1 - mu)
        H = A.T @ (A * W[:, None]) + l2 * np.eye(A.shape[1])
        w = w + np.linalg.solve(H, A.T @ (yb - mu) - l2 * w)
    return w

def retrain(seed):
    r = np.random.default_rng(seed)
    idx = r.integers(0, n, n)               # a retrain = a fresh resample of the same population
    return fit(X[idx], y[idx])

# 100 reviewed declines: the 100 highest-risk applicants under the reference model
w_ref = fit(X, y)
risk = np.c_[np.ones(n), X] @ w_ref
dec = np.argsort(-risk)[:100]
mu_x = X.mean(0)

def contrib(w, rows):                       # linear-logit attribution: coef * (x - mean)
    return w[1:] * (X[rows] - mu_x)

def top(w, rows, groups=None):
    c = contrib(w, rows)
    if groups is not None:
        c = np.c_[[c[:, g].sum(1) for g in groups]].T
    return c.argmax(1), np.argsort(-c, 1)[:, :4]

wa, wb = retrain(1), retrain(2)
ta, sa = top(wa, dec); tb, sb = top(wb, dec)
flip = int((ta != tb).sum())
print("raw top reason differs between two retrains:", flip, "of 100")
jac = np.mean([len(set(a) & set(b)) / len(set(a) | set(b)) for a, b in zip(sa, sb)])
print("mean Jaccard overlap of the 4-reason sets (raw):", round(jac, 3))

groups = [[0, 1], [2], [3], [4], [5]]       # income+tenure merged into one reason group
ga, _ = top(wa, dec, groups); gb, _ = top(wb, dec, groups)
gflip = int((ga != gb).sum())
print("grouped (income+tenure = one reason) top reason differs:", gflip, "of 100")

def bagged(seed0, B=60):
    return np.mean([retrain(seed0 + b) for b in range(B)], axis=0)
ba, bb = bagged(1000), bagged(2000)
tba, _ = top(ba, dec); tbb, _ = top(bb, dec)
bflip = int((tba != tbb).sum())
print("bagged coefficients (60 resamples each), raw top reason differs:", bflip, "of 100")

# validation numbers: how big is 30 of 100? Wilson interval for the prompt's sample
def wilson(k, m, z=1.96):
    ph = k / m; d = 1 + z * z / m
    c = (ph + z * z / (2 * m)) / d
    h = z * np.sqrt(ph * (1 - ph) / m + z * z / (4 * m * m)) / d
    return c - h, c + h
lo, hi = wilson(30, 100)
print("prompt: 30 of 100 =", 30 / 100, "| 95% Wilson interval", round(lo, 3), "to", round(hi, 3))
assert 30 / 100 == 0.3 and 0.21 < lo < 0.22 and 0.39 < hi < 0.40
print("coefficient sd across 60 resamples (income, tenure):",
      np.round(np.std([retrain(5000 + b)[1:3] for b in range(60)], axis=0), 3))
corr_ab = np.corrcoef(np.array([retrain(5000 + b)[1:3] for b in range(60)]).T)[0, 1]
print("corr of income and tenure coefficient across resamples:", round(corr_ab, 3))
print("true coefficients", dict(zip(names, beta_true.tolist())))
assert flip == 47 and gflip == 12 and bflip == 17 and round(jac, 3) == 0.884
assert gflip < flip and bflip < flip
assert corr_ab < -0.7
```

**Output (my run):**
```
sample corr(income, tenure) = 0.857
raw top reason differs between two retrains: 47 of 100
mean Jaccard overlap of the 4-reason sets (raw): 0.884
grouped (income+tenure = one reason) top reason differs: 12 of 100
bagged coefficients (60 resamples each), raw top reason differs: 17 of 100
prompt: 30 of 100 = 0.3 | 95% Wilson interval 0.219 to 0.396
coefficient sd across 60 resamples (income, tenure): [0.169 0.154]
corr of income and tenure coefficient across resamples: -0.819
true coefficients {'income': -0.45, 'tenure': -0.45, 'debt_ratio': 0.5, 'utilisation': 0.4, 'inquiries': 0.25, 'file_age': -0.2}
```

**Follow-ups:**
- *Why not just drop tenure?* You lose information and AUC may fall; test it. Also the applicant loses an accurate reason. Grouping keeps both.
- *Could a monotone or scorecard model make this easier?* Often yes: constrained or additive models give fixed point contributions. Test AUC cost against reason stability.
- *How do you handle the reviewer who says the reason is wrong for this person?* Counterfactual check plus a log; repeated complaints become a test case in the stability gate.

**Common mistakes:**
- Treating one retrain's ranking as the truth.
- Reporting a flip rate from 100 declines with no interval.
- Grouping features without checking that the group wording is accurate for each member.
- Quoting legal requirements as facts instead of asking compliance.

### Q32 ⭐⭐ 🟡 E-commerce: A seller-risk model flags 1,000 sellers for review, an audit of 100 randomly chosen flagged sellers confirmed 40 as fraudulent (40%, a sample), and investigators can review 200 sellers a week. Estimate the fraudulent sellers among the 1,000 flagged as a projection, the weeks to clear the queue, and the number expected in the first week if the queue is reviewed in random order. How would you order the queue instead?
**Asked at:** Marketplace-trust material (a prachub Amazon fake-review question on detection signals and impact metrics, an Interview Query fake-review prompt and DoorDash and Thumbtack data scientist guides on marketplace analytics); prep-site material and one estimate-based news item, no confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** About 400 of the 1,000 flagged sellers are fraudulent as a projection (the audit is a sample, so roughly 300 to 500), the queue takes 5 weeks at 200 a week, and random order finds about 80 in week 1; I would order by expected fraud harm per review, not at random.

**Clarifying questions:**
- Was the audit of 100 truly random among the 1,000 flagged, and who judged "fraudulent" (the same investigators)? A non-random or inconsistent audit breaks the 40%.
- Do I have the model score for each audited seller? It lets me measure how precision changes with score.
- How long does fraud keep costing us while a seller waits (daily losses, buyer harm)? It sets the value of speed.
- Can a review be cheap (auto-triage) for some sellers? Review time per seller may differ.
- What is the action on a confirmed seller (suspend, hold funds, ask for documents), and what is the cost of wrongly suspending a good seller? It sets the cost of false positives.

**Approach:**
1. Compute the projection and its range. 40 of 100 is 40%, so 0.40 x 1,000 = 400 fraudulent among the flagged. A 95% interval on 40 of 100 is 30.4% to 49.6%, so 304 to 496 sellers.
2. Weeks to clear: 1,000 / 200 = 5 weeks.
3. Random order, week 1: 200 reviews x 40% = 80 fraudulent expected (hypergeometric, standard deviation about 6.2). If the true number is 304 or 496 the week-1 mean is 60.8 or 99.2.
4. Better order: rank by expected harm avoided per review minute = P(fraud) x exposure (money at risk, buyers affected, growth rate of sales) / expected review time. Use the model score only after checking it is calibrated on the audited sample.
5. Use the audit to calibrate: tabulate fraud rate by score band. With an invented split (high band 21 of 30, middle 13 of 35, low 6 of 35) the high band is 70% and reviewing it first gives 140 expected in week 1 instead of 80.
6. Keep a random slice of each week's review (for example 10%) so the model is evaluated on a fair sample and the labels do not become biased.
7. Fast actions for the top of the queue (hold payouts or limit listings pending review) can reduce damage before the investigator arrives; ask the trust and policy team what actions are allowed.
8. Re-score the queue daily as new signals arrive; the order is not fixed for 5 weeks.

**Metrics:**
- Precision of review = confirmed fraud / sellers reviewed.
- Fraud found per investigator-hour, and expected loss prevented per week (sum of P(fraud) x exposure for reviewed sellers).
- Time to action for confirmed fraud (median days from flag to action).
- Guardrails: false-suspension rate (good sellers actioned / sellers actioned), appeals overturned, and fraud rate in the random slice.

**Risks:**
- Projection from 100 audits has a wide range, about +/- 10 points.
- Ordering by score only finds what the model already likes; sellers it misses are never audited (keep the random slice).
- If fraudsters adapt to the order, the top band becomes less pure.
- Optimising fraud counts alone can starve large exposure sellers; use harm, not count.

**What the interviewer scores:**
- Strong: 400, 5 weeks, 80 in week 1, and says "sample, projection, range".
- Strong: orders by expected harm per review and keeps a random audit slice.
- Strong: separates fraud count from money at risk.
- Weak: "review in order of arrival"; no mention of uncertainty; ignores false suspensions.

**Example:** Illustrative numbers. In the run below the projection is 400 (304 to 496), 5 weeks, 80 expected in week 1 under random order and 140 when the high-score band goes first. Ordering by probability times exposure finds fewer fraudsters in week 1 (about 110 versus 140 in my simulated exposures) but stops about 440,000 of expected loss instead of about 246,000.
- Weak: "We have 400 frauds, so we need 2 weeks of work."
- Strong: "The audit suggests about 400, plausibly 300 to 500. At 200 reviews a week that is 5 weeks, and random order finds about 80 in week 1. I would rank by fraud probability times money at risk per review minute, and keep a random 10% slice so the model stays honest."

**Code:**
```python
import numpy as np
from math import comb, sqrt

flagged, audited, fraud_s, cap = 1000, 100, 40, 200
p = fraud_s / audited
proj = flagged * p
weeks = flagged / cap
print("sample rate", p, "| projected fraudulent among flagged", proj, "| weeks to clear", weeks)
assert p == 0.4 and proj == 400 and weeks == 5

# uncertainty on the 40 of 100 (the audit is a sample)
z = 1.96
se = sqrt(p * (1 - p) / audited)
lo, hi = p - z * se, p + z * se
fpc = sqrt((flagged - audited) / (flagged - 1))
se2 = se * fpc
print("normal 95% interval:", round(lo, 3), "to", round(hi, 3), "-> sellers", round(lo * flagged), "to", round(hi * flagged),
      "| with finite-population correction", round((p - z * se2) * flagged), "to", round((p + z * se2) * flagged))
assert round(lo * flagged) == 304 and round(hi * flagged) == 496

# random review order: first week = 200 reviewed out of 1000 with K fraudulent (hypergeometric)
K = 400
mean1 = cap * K / flagged
sd1 = sqrt(cap * (K / flagged) * (1 - K / flagged) * (flagged - cap) / (flagged - 1))
print("week 1, random order: mean", mean1, "sd", round(sd1, 2))
assert mean1 == 80 and round(sd1, 2) == 6.20
for Kx in (304, 496):
    print("  if true K =", Kx, "-> week-1 mean", cap * Kx / flagged)

# ordering by score: invented audit table, 100 audited sellers split by model-score tertile
tiers = {"high score": (30, 21), "mid score": (35, 13), "low score": (35, 6)}   # (audited, fraud)
assert sum(a for a, f in tiers.values()) == 100 and sum(f for a, f in tiers.values()) == 40
rates = {k: f / a for k, (a, f) in tiers.items()}
print({k: round(v, 3) for k, v in rates.items()})
# project to 1000 flagged in the same tier shares (audited share = 30/35/35 percent)
size = {k: a * 10 for k, (a, f) in tiers.items()}
fr = {k: size[k] * rates[k] for k in tiers}
print("tier sizes", size, "| projected fraud", {k: round(v) for k, v in fr.items()}, "total", round(sum(fr.values())))
assert abs(sum(fr.values()) - 400) < 1e-9
# week 1 by score order: all 200 from high tier (300 sellers) + nothing else needed
wk1_score = cap * rates["high score"]
print("week 1 reviewing the high tier first: expected fraud found", wk1_score, "vs random", mean1)
assert wk1_score == 140
# value-ordered: add dollars at risk per seller (invented) -> expected loss per reviewer-hour
rng = np.random.default_rng(32)
exposure = rng.lognormal(7, 1, flagged)               # invented exposure per seller
pr = np.concatenate([np.full(300, .70), np.full(350, .3714), np.full(350, .1714)])
rng.shuffle(pr)
by_p = np.argsort(-pr)[:cap]
by_ev = np.argsort(-(pr * exposure))[:cap]
print("week-1 expected fraud caught: by probability", round(pr[by_p].sum(), 1), "| by probability x exposure", round(pr[by_ev].sum(), 1))
print("week-1 expected loss stopped: by probability", round((pr * exposure)[by_p].sum()), "| by probability x exposure", round((pr * exposure)[by_ev].sum()))
assert (pr * exposure)[by_ev].sum() >= (pr * exposure)[by_p].sum()
assert pr[by_p].sum() >= pr[by_ev].sum()
```

**Output (my run):**
```
sample rate 0.4 | projected fraudulent among flagged 400.0 | weeks to clear 5.0
normal 95% interval: 0.304 to 0.496 -> sellers 304 to 496 | with finite-population correction 309 to 491
week 1, random order: mean 80.0 sd 6.2
  if true K = 304 -> week-1 mean 60.8
  if true K = 496 -> week-1 mean 99.2
{'high score': 0.7, 'mid score': 0.371, 'low score': 0.171}
tier sizes {'high score': 300, 'mid score': 350, 'low score': 350} | projected fraud {'high score': 210, 'mid score': 130, 'low score': 60} total 400
week 1 reviewing the high tier first: expected fraud found 140.0 vs random 80.0
week-1 expected fraud caught: by probability 140.0 | by probability x exposure 109.7
week-1 expected loss stopped: by probability 245534 | by probability x exposure 440302
```

**Follow-ups:**
- *Is the 40% the precision of the model?* Only for the flagged group at the audit threshold; it tells nothing about unflagged sellers.
- *What if two weeks of delay matters a lot?* Add a time-decay weight, or take low-effort holds on the top band at once.
- *How do you get labels without bias if you only review the top?* The random slice plus periodic reviews of the unflagged.

**Common mistakes:**
- Saying "400 are fraudulent" as a fact.
- Reviewing in random order because it is "fair".
- Optimising count rather than harm.
- Forgetting the cost of wrongly acting on honest sellers.

### Q33 ⭐⭐ 🟡 Healthcare: An LLM drafts discharge summaries and two clinicians audited 200 of them, finding 14 with an omitted medication (7%) and 6 with an invented detail (3%), measured on that sample. Clinicians must sign every summary and say drafting saves 4 of the usual 10 minutes. Explain how you would define and measure harm, what audited error rate you would want to see before wider rollout, and what you would ask the clinical safety and compliance teams.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to LLM clinical documentation audit in 2025-2026 health-AI material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** I would define harm by clinical severity and by whether the error reached the patient record after the clinician signed, measure it with a blinded severity-graded audit compared with human-written summaries, and let clinical safety set the pass rate before wider rollout; 7% and 3% on 200 are samples with wide ranges.

**Clarifying questions:**
- What is the baseline: how often do human-written summaries omit a medication? It sets whether 7% is better or worse than today.
- Were the two clinicians blinded to source (human or LLM), and how often did they agree? Agreement shows whether the labels are reliable.
- Can one summary have both errors, and which medicines were missing? The 14 and the 6 may overlap, so any-error is between 7% and 10%.
- Did the reviewing clinicians use the same checking time as they will in production? A careful audit is slower than a busy ward sign-off.
- Who owns the decision (clinical safety officer, not the data team)? It decides who sets the threshold.

**Approach:**
1. State what the sample shows. 14 of 200 is 7.0% (95% Wilson 4.2% to 11.4%); 6 of 200 is 3.0% (1.4% to 6.4%). The "4 of 10 minutes" saving is what clinicians say; I treat it as a claim and measure it.
2. Define harm in tiers with clinical safety: omitted medication by drug class and by whether it matters (for example a stopped or new high-risk drug versus a minor supplement), invented detail by whether it changes a decision, and "reached the record" after sign-off versus caught in review. Weights belong to clinicians, not to me.
3. Measure per summary and per medication: errors / medications in the source (a per-medication denominator), and summaries with any error / summaries audited (per-summary).
4. Audit design: random sample stratified by ward and complexity, two blinded reviewers, adjudication of disagreements, human-written summaries mixed in as a baseline.
5. Rollout bar: ask clinical safety for the target. Show them what is testable: with zero errors seen, 299 clean audited summaries are needed to show the true rate is below 1% with 95% confidence, 149 for 2% and 59 for 5% (one-sided). Any error found raises the number. To pin a 7% rate within +/-1 point takes about 2,500 audits.
6. Staged rollout: shadow mode (draft not shown), then one ward with 100% audit, then widen; stop rules agreed in advance (any severe omission reaching the record pauses the rollout).
7. Product guards: show the medication list from the source side by side with the draft, flag medicines that appear in the record but not the draft, and make the clinician confirm the medication section explicitly.
8. Ask clinical safety and compliance (via their processes): who is accountable for a signed summary, how errors are reported and logged, patient-data handling for the drafting service, and what must be disclosed to patients. I make no claims about the rules.

**Metrics:**
- Medication omission rate (per summary) = summaries with at least one omitted medication / audited summaries (14 / 200).
- Per-medication omission rate = omitted medications / medications in the source (needs a count I do not have in the prompt).
- Invention rate = summaries with an invented detail / audited summaries (6 / 200), split by severity.
- Reached-the-record rate = errors still present after sign-off / audited summaries.
- Net time saved = (usual minutes - drafted-plus-review minutes) / usual minutes; compare with the claimed 4 of 10 (40%).
- Guardrails: reviewer agreement (kappa), error rate by ward and patient complexity.

**Risks:**
- Automation bias: clinicians sign what looks fluent, so signing is not a safety net by itself.
- Time saving can vanish if careful checking takes the saved minutes (4 saved minus 3 extra checking minutes leaves 1 minute, or 10%, in my illustration).
- Errors cluster in complex patients; an average hides them.
- Audit reviewers may be less careful after the first 50.

**What the interviewer scores:**
- Strong: severity-weighted harm, "reached the record" distinction, and a human baseline.
- Strong: honest about sample size and uses interval or zero-error sample sizes.
- Strong: hands the pass-rate decision to clinical safety and asks questions instead of asserting rules.
- Weak: "7% is low, ship"; "accuracy of the LLM" with no harm definition; claims about regulation.

**Example:** Illustrative numbers from the run. With the prompt's 200 audits: 7% omission (4.2% to 11.4%), 3% invention (1.4% to 6.4%). If signing clinicians catch 90% of errors, about 70 omissions and 30 inventions per 10,000 summaries reach the record; at a 50% catch rate, 350 and 150.
- Weak: "Only 3% hallucinate, and clinicians sign everything, so it is safe."
- Strong: "7% omission and 3% invention are samples with wide ranges. I would grade by severity, count what survives sign-off, compare with human summaries, and ask clinical safety for the rollout bar. To show under 1% with zero errors I would need about 300 clean audits."

**Code:**
```python
import math

def wilson(k, n, z=1.96):
    ph = k / n; d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

n = 200
for name, k in (("omitted medication", 14), ("invented detail", 6)):
    lo, hi = wilson(k, n)
    print(f"{name}: {k}/{n} = {k/n:.3f} | 95% Wilson {lo:.3f} to {hi:.3f}")
assert 14 / n == 0.07 and 6 / n == 0.03
lo14, hi14 = wilson(14, n); lo6, hi6 = wilson(6, n)
assert round(lo14, 3) == 0.042 and round(hi14, 3) == 0.114 and round(lo6, 3) == 0.014 and round(hi6, 3) == 0.064

# the two error types may overlap: summaries with any error is between 14 and 20 of 200
print("any error: between", 14 / n, "and", 20 / n, "(overlap unknown)")
assert 14 / n == 0.07 and 20 / n == 0.10

# zero-error audit sizes: how many clean summaries to show the true rate is below a target (95% one-sided)
for target in (0.05, 0.02, 0.01):
    m = math.ceil(math.log(0.05) / math.log(1 - target))
    print(f"target rate below {target:.0%}: need {m} audited summaries with zero errors (rule of three: 3/{target} = {3/target:.0f})")
assert math.ceil(math.log(0.05) / math.log(0.99)) == 299
assert math.ceil(math.log(0.05) / math.log(0.98)) == 149
assert math.ceil(math.log(0.05) / math.log(0.95)) == 59

# with the observed 7%, how big an audit to pin the rate within +-1 point?
m = math.ceil(1.96 ** 2 * 0.07 * 0.93 / 0.01 ** 2)
print("audit size for +-1 point at p=7%:", m)
assert m == 2501

# severity-weighted harm (invented weights and severity mix, to be set by clinical safety)
w = {"omitted: high-risk drug": 10, "omitted: other": 2, "invented: any": 5}
mix_omit_high = 0.2                      # assumption: 20% of omissions involve a high-risk drug
per_summary = 0.07 * (mix_omit_high * w["omitted: high-risk drug"] + (1 - mix_omit_high) * w["omitted: other"]) + 0.03 * w["invented: any"]
print("severity-weighted harm points per summary:", round(per_summary, 3))
assert round(per_summary, 3) == 0.402
# per 10,000 summaries: errors that reach the patient depend on clinician catch rate
for catch in (0.9, 0.5):
    reach_omit = 10000 * 0.07 * (1 - catch); reach_inv = 10000 * 0.03 * (1 - catch)
    print(f"if signing clinicians catch {catch:.0%} of errors: reaching the record per 10,000 summaries: omissions {reach_omit:.0f}, inventions {reach_inv:.0f}")
assert round(10000 * 0.07 * 0.1) == 70 and round(10000 * 0.07 * 0.5) == 350 and round(10000 * 0.03 * 0.5) == 150

# time: drafting 'saves 4 of 10 min' is a clinician statement, not measured; review time eats it
saved = 4 / 10
print("claimed saving", saved, "= 4 of 10 minutes; if careful checking costs 3 extra minutes the net saving is", 4 - 3, "minutes (", (4 - 3) / 10, ")")
assert (4 - 3) / 10 == 0.1
```

**Output (my run):**
```
omitted medication: 14/200 = 0.070 | 95% Wilson 0.042 to 0.114
invented detail: 6/200 = 0.030 | 95% Wilson 0.014 to 0.064
any error: between 0.07 and 0.1 (overlap unknown)
target rate below 5%: need 59 audited summaries with zero errors (rule of three: 3/0.05 = 60)
target rate below 2%: need 149 audited summaries with zero errors (rule of three: 3/0.02 = 150)
target rate below 1%: need 299 audited summaries with zero errors (rule of three: 3/0.01 = 300)
audit size for +-1 point at p=7%: 2501
severity-weighted harm points per summary: 0.402
if signing clinicians catch 90% of errors: reaching the record per 10,000 summaries: omissions 70, inventions 30
if signing clinicians catch 50% of errors: reaching the record per 10,000 summaries: omissions 350, inventions 150
claimed saving 0.4 = 4 of 10 minutes; if careful checking costs 3 extra minutes the net saving is 1 minutes ( 0.1 )
```

**Follow-ups:**
- *Is a lower error rate than humans enough?* Possibly not alone; different error types (fluent inventions) can be worse. Safety decides.
- *Why a per-medication denominator?* A summary with 15 medicines has more chances to miss one.
- *What if time savings are real but errors rise on complex patients?* Restrict to simple cases first.

**Common mistakes:**
- Treating the clinician signature as the safeguard.
- Reporting 7% and 3% as population rates without intervals.
- Adding 7% and 3% to get 10% (overlap unknown).
- Setting the acceptable threshold in the data team.

### Q34 ⭐⭐ 🔴 Fintech: A credit model's average predicted 12-month default probability is 3.0% across a portfolio of 20,000 loans, but 900 of them defaulted (4.5%, matured outcomes) while the AUC is unchanged at 0.80. Exposure is 10,000 per loan and the loss given default is assumed to be 50%. Compute the expected loss predicted, the loss from observed defaults at the assumed loss given default, and the shortfall, and explain the possible causes, whether you would recalibrate or rebuild, and how this goes through model governance.
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Predicted loss is 3,000,000 and the loss from observed defaults at the assumed 50% is 4,500,000, a shortfall of 1,500,000 (observed is 1.5 times predicted); ranking is intact (AUC 0.80), so this is a level problem, and I would first diagnose the cause, then recalibrate under model-governance sign-off unless the miss differs by segment.

**Clarifying questions:**
- Is the 4.5% measured on the same 12-month window and the same default definition used in training? A changed definition makes a model look wrong without being wrong.
- Is the portfolio mix the same as in development (new products, channels, score bands)? A mix shift changes the average PD even if the model is fine.
- Were macro conditions different this year? One year is one draw of the economy, so a common shock can move all defaults together.
- Is the 50% loss given default an assumption, a policy number or an observed value? The loss figures use it only as an input.
- What does the model feed (approval cut-off, pricing, provisioning)? It sets urgency and who has to sign off.

**Approach:**
1. Do the arithmetic. Predicted defaults = 20,000 x 3.0% = 600; observed 900 (4.5%). Expected loss predicted = 20,000 x 0.03 x 10,000 x 0.5 = 3,000,000. Loss from observed defaults at the assumed LGD = 900 x 10,000 x 0.5 = 4,500,000. Shortfall = 1,500,000 (33.3% of observed, observed is 1.5x predicted).
2. Is it noise? If defaults were independent, the standard deviation of the count at 3% is about 24, so 900 is about 12 standard deviations above 600. But defaults are not independent. With a small pairwise default correlation of 0.001 the gap is only about 2.7 design-effect units, so a common economic shock is plausible. Do not call it noise and do not call it proof of a broken model.
3. Check calibration by score band and by segment, not only the average. Plot predicted versus observed default rate by decile and by product and vintage.
4. List causes and test each: macro shock, mix shift towards riskier applicants, drift in a key feature, changed default or label definition, data pipeline change, selection effect from approvals (reject inference), seasoning (young loans default later), underwriting policy changes.
5. Decide. If the ratio is similar across bands (a level shift) and AUC holds, recalibrate: fit a new intercept (and maybe a slope) on recent matured outcomes; in a simulation with an AUC of about 0.80 recalibration leaves AUC unchanged. If some segments are far off, or a key feature drifted, rebuild or add segment-specific calibration.
6. Governance: this is a model-risk event. Write up the issue, the evidence and the proposed fix; the model validation function reviews, the owner approves, and the change is logged with before and after metrics. Ask the risk, finance and governance teams about provisioning impact, thresholds for when a recalibration needs formal approval, and documentation; I do not state the rules.
7. Interim: use a conservative overlay or tighter cut-off if the business agrees, and monitor monthly.
8. Monitoring afterwards: predicted versus observed by band monthly, population stability on key features, and a trigger (for example a ratio outside an agreed band for two quarters).

**Metrics:**
- Calibration ratio = observed default rate / mean predicted PD = 4.5% / 3.0% = 1.5.
- Expected loss = sum over loans of PD x EAD x LGD; observed-default loss = defaults x EAD x LGD at the assumed LGD (not realised losses).
- Calibration by band = observed / predicted per decile.
- Discrimination: AUC (0.80 before and after recalibration).
- Guardrails: approval rate, provisioning change, stability of ranking after recalibration.

**Risks:**
- Recalibrating on one bad year bakes the shock in; use a long-run anchor or overlay.
- A single intercept shift will not fix band-specific errors (in my simulation the ratio was 2.4 in the safest decile and 1.35 in the riskiest under a pure logit shift).
- LGD is assumed; the 4,500,000 is not a realised loss.
- Immature loans can understate defaults; confirm outcomes are matured.

**What the interviewer scores:**
- Strong: gets 3.0M, 4.5M and 1.5M, and states LGD is an assumption.
- Strong: separates ranking (AUC) from level (calibration) and checks by band.
- Strong: gives a decision rule between recalibrating and rebuilding, and a governance path.
- Weak: "AUC is fine so the model is fine"; "retrain from scratch immediately"; legal claims.

**Example:** Illustrative numbers from the run. A simulated model with AUC about 0.80 and mean PD 3.0% faced 890 defaults; after an intercept recalibration its mean PD was 4.45% and AUC stayed 0.804, with expected loss 4,450,000.
- Weak: "The model underpredicts, so we need a new model."
- Strong: "Expected loss is 3.0M predicted against 4.5M from observed defaults at an assumed 50% LGD. AUC is unchanged, so ranking works; the level is off by a factor of 1.5. I would check by decile and by vintage, recalibrate if the miss is a level shift, and take it through model validation with the finance and risk teams."

**Code:**
```python
import numpy as np
from math import sqrt, log

N, EAD, LGD = 20000, 10000, 0.5
pd_pred, defaults = 0.03, 900
pd_obs = defaults / N
el_pred = N * pd_pred * EAD * LGD
el_obs = defaults * EAD * LGD
print("observed default rate", pd_obs, "| predicted defaults", N * pd_pred, "| observed", defaults)
print("expected loss predicted", el_pred, "observed", el_obs, "shortfall", el_obs - el_pred, "=", round((el_obs - el_pred) / el_obs, 3), "of observed;", round(el_obs / el_pred, 2), "x predicted")
assert pd_obs == 0.045 and N * pd_pred == 600
assert el_pred == 3_000_000 and el_obs == 4_500_000 and el_obs - el_pred == 1_500_000

# noise check, independent defaults: sd of count under the model's own 3%
sd = sqrt(N * pd_pred * (1 - pd_pred))
z = (defaults - N * pd_pred) / sd
print("binomial sd of default count", round(sd, 1), "| z =", round(z, 1))
assert round(sd, 1) == 24.1 and round(z, 1) == 12.4
# defaults cluster (shared shocks): allow a design effect, e.g. intra-class correlation rho
for rho in (0.001, 0.005, 0.01):
    print("  pairwise default correlation rho", rho, "-> design-effect z", round(z / sqrt(1 + (N - 1) * rho), 1))
# intercept shift needed (logit scale) for the average to move from 3.0% to 4.5%
logit = lambda p: log(p / (1 - p))
shift = logit(0.045) - logit(0.03)
print("logit intercept shift", round(shift, 3))
assert round(shift, 3) == 0.421

# simulate: a model with AUC ~0.80 whose level is wrong; recalibrate the intercept; AUC does not move
rng = np.random.default_rng(34)
def auc(s, y):
    r = s.argsort().argsort() + 1
    n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
# latent score so that the model's mean PD is ~3% and AUC ~0.8
z0 = rng.normal(size=N)
def level(b):                      # find intercept so mean prob = b
    lo, hi = -12, 2
    for _ in range(60):
        mid = (lo + hi) / 2
        if (1 / (1 + np.exp(-(mid + 1.3 * z0)))).mean() > b: hi = mid
        else: lo = mid
    return mid
a_true = level(0.045); a_model = level(0.03)
p_true = 1 / (1 + np.exp(-(a_true + 1.3 * z0)))
y = (rng.random(N) < p_true).astype(int)
p_model = 1 / (1 + np.exp(-(a_model + 1.3 * z0)))
print("sim: defaults", y.sum(), "| model mean PD", round(p_model.mean(), 4), "| AUC", round(auc(p_model, y), 3))
# recalibrate on the matured outcomes: fit new intercept only (slope fixed)
a_new = level(y.mean())
p_new = 1 / (1 + np.exp(-(a_new + 1.3 * z0)))
print("after intercept recalibration: mean PD", round(p_new.mean(), 4), "| AUC", round(auc(p_new, y), 3), "| expected loss", round(p_new.sum() * EAD * LGD))
assert abs(auc(p_model, y) - auc(p_new, y)) < 1e-12
assert abs(p_new.mean() - y.mean()) < 1e-4
# calibration by band: is it a uniform shift or only some bands? (decile table)
dec = np.array_split(np.argsort(p_model), 10)
for i in (0, 4, 9):
    d = dec[i]; print(f"  decile {i+1}: predicted {p_model[d].mean():.4f} observed {y[d].mean():.4f} ratio {y[d].mean()/p_model[d].mean():.2f}")
# LGD sensitivity: the 50% is an assumption
for lgd in (0.4, 0.5, 0.6):
    print("  LGD", lgd, "-> observed-default loss", defaults * EAD * lgd, "| predicted", N * pd_pred * EAD * lgd)
assert y.sum() == 890 and round(auc(p_model, y), 3) == 0.804 and round(p_new.mean(), 4) == 0.0445
assert 2 < y[dec[0]].mean() / p_model[dec[0]].mean() < 3 and 1.2 < y[dec[9]].mean() / p_model[dec[9]].mean() < 1.5
```

**Output (my run):**
```
observed default rate 0.045 | predicted defaults 600.0 | observed 900
expected loss predicted 3000000.0 observed 4500000.0 shortfall 1500000.0 = 0.333 of observed; 1.5 x predicted
binomial sd of default count 24.1 | z = 12.4
  pairwise default correlation rho 0.001 -> design-effect z 2.7
  pairwise default correlation rho 0.005 -> design-effect z 1.2
  pairwise default correlation rho 0.01 -> design-effect z 0.9
logit intercept shift 0.421
sim: defaults 890 | model mean PD 0.03 | AUC 0.804
after intercept recalibration: mean PD 0.0445 | AUC 0.804 | expected loss 4450000
  decile 1: predicted 0.0017 observed 0.0040 ratio 2.37
  decile 5: predicted 0.0123 observed 0.0210 ratio 1.70
  decile 10: predicted 0.1374 observed 0.1855 ratio 1.35
  LGD 0.4 -> observed-default loss 3600000.0 | predicted 2400000.0
  LGD 0.5 -> observed-default loss 4500000.0 | predicted 3000000.0
  LGD 0.6 -> observed-default loss 5400000.0 | predicted 3600000.0
```

**Follow-ups:**
- *How would you tell macro from model failure?* Compare with peer portfolios or lenders, check the same-vintage behaviour across segments, and see whether the miss is uniform across bands.
- *Is a 1.5x miss bad if provisioning already covers it?* Ask finance and risk; it still needs documenting and monitoring.
- *Would you also recalibrate LGD?* Check realised recoveries separately; do not hide a PD miss inside an LGD change.
- See also Book 6 Part 2, Q14 (a classifier with stable AUC 0.82 whose probabilities have drifted) for the generic recalibration-versus-retrain argument.

**Common mistakes:**
- Calling the observed-default loss "the realised loss" when LGD is assumed.
- Declaring significance without a design effect for correlated defaults.
- Recalibrating without checking bands or segments.
- Skipping the governance step.

### Q35 ⭐⭐ 🔴 E-commerce: A price test cut the price by 10% on 1,000 items from 500 to 450 and daily units on those items rose 20% relative, from 100,000 to 120,000, while 4,000 close substitute items fell 5% relative, from 240,000 to 228,000 units a day at an unchanged price of 500 (projections from a pilot). Compute the item-level and the whole-category change in revenue per day, and explain how you would design the test to capture cannibalisation.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to price tests with substitution and interference in marketplace material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Item-level revenue rises 4,000,000 a day (+8%), but the substitutes lose 6,000,000, so the whole category falls 2,000,000 a day (-1.2%); the price cut mostly moves demand from neighbours to the discounted items, so I would test at the category level.

**Clarifying questions:**
- Are these numbers from a randomised pilot or a before/after comparison? Without randomisation the 20% and 5% could include trends and seasonality.
- Is the objective revenue, units or margin? The answer flips with unit cost (see the margin view below).
- Which items count as substitutes, and how was that list built? A wrong list hides or invents cannibalisation.
- Is there a time effect (promotion novelty, pull-forward of purchases)? A short pilot overstates a lasting lift.
- Is any inventory or fee affected by the price cut? Costs outside revenue change the decision.

**Approach:**
1. Item level. Revenue before = 100,000 x 500 = 50,000,000; after = 120,000 x 450 = 54,000,000; change +4,000,000 (+8.0%). Decomposition: -5,000,000 from the price cut on old units (100,000 x -50), +9,000,000 from the extra 20,000 units at 450.
2. Substitutes: 240,000 x 500 = 120,000,000 before, 228,000 x 500 = 114,000,000 after, change -6,000,000 (-5.0%).
3. Whole category: before 170,000,000, after 168,000,000: -2,000,000 per day (-1.18%). Units rose by 8,000 (20,000 extra on the test items minus 12,000 lost on substitutes), so units grew while revenue fell.
4. Cannibalisation share: 12,000 of the 20,000 extra units, 60%, came from substitutes. Elasticities: own -2.0, cross +0.5 (a 10% cut moved the substitutes 5% the other way).
5. Break-even: the category is revenue-neutral only if substitutes lose 8,000 units or fewer (3.3% of their units, instead of 5%).
6. Margin view (invented unit cost of 300): margin falls from 68,000,000 to 63,600,000, a loss of 4,400,000 per day, worse than the revenue figure.
7. Design to capture cannibalisation: randomise at the level where substitutes live (category, brand-by-region, or cluster of similar items), not the item. Measure outcome at the cluster level. In my toy model item-level randomisation (half the items cut) shows a +23.5% treated-versus-control lift, while cutting every item gives +3.2%, because the control items lose 9.1% of their own baseline.
8. Other designs: geo or time-based switchback tests; holdout clusters; track category total and a long window for pull-forward.

**Metrics:**
- Item-level revenue change = (units after x price after) - (units before x price before) for test items.
- Category revenue (and margin) change = test items + substitutes (+ any other affected items).
- Cannibalisation rate = units lost on substitutes / extra units on test items (60%).
- Guardrails: margin per day, conversion, returns, stock-outs, long-window repeat purchase.

**Risks:**
- Item-level randomisation shares customers between arms, so the estimate is biased (interference).
- A pilot's relative moves may not hold at scale; competitors may respond.
- Revenue can rise while margin falls.
- Substitute lists are subjective; some losses may be in non-listed items.

**What the interviewer scores:**
- Strong: computes +4M, -6M, -2M correctly and states units versus revenue.
- Strong: gives the cannibalisation share and asks about margin.
- Strong: randomises at cluster or category level and measures category totals.
- Weak: reports only the +8% item lift; ignores interference in the test design.

**Example:** Illustrative numbers from the run. Item level +4,000,000, substitutes -6,000,000, category -2,000,000 per day; 60% of the extra units are taken from neighbours.
- Weak: "The test lifted units 20% and revenue 8%, so we roll out."
- Strong: "Test items gain 4 million a day, but substitutes lose 6 million, so the category loses 2 million. Of the extra 20,000 units, 12,000 came from neighbours. I would re-run at the category level with a holdout and look at margin, not just revenue."

**Code:**
```python
items_n, subs_n = 1000, 4000
p0, p1, ps = 500, 450, 500
u0, u1 = 100_000, 120_000
s0, s1 = 240_000, 228_000
assert p1 == p0 * 0.9 and u1 == u0 * 1.2 and s1 == s0 * 0.95
rev_i0, rev_i1 = u0 * p0, u1 * p1
rev_s0, rev_s1 = s0 * ps, s1 * ps
d_i, d_s = rev_i1 - rev_i0, rev_s1 - rev_s0
print("test items revenue/day", rev_i0, "->", rev_i1, "change", d_i, f"({d_i/rev_i0:+.1%})")
print("substitutes revenue/day", rev_s0, "->", rev_s1, "change", d_s, f"({d_s/rev_s0:+.1%})")
print("category change", d_i + d_s, f"({(d_i+d_s)/(rev_i0+rev_s0):+.2%} of {rev_i0+rev_s0})")
assert d_i == 4_000_000 and d_s == -6_000_000 and d_i + d_s == -2_000_000
assert rev_i0 + rev_s0 == 170_000_000 and rev_i1 + rev_s1 == 168_000_000
# decomposition of the item-level change
price_effect = u0 * (p1 - p0)            # old units at the new price
volume_effect = (u1 - u0) * p1           # extra units at the new price
print("price effect on old units", price_effect, "| revenue from extra units", volume_effect)
assert price_effect == -5_000_000 and volume_effect == 9_000_000 and price_effect + volume_effect == d_i
# units
extra, lost = u1 - u0, s0 - s1
print("extra units on test items", extra, "| units lost on substitutes", lost, "| share of extra units that is cannibalised", lost / extra, "| net category units", extra - lost)
assert extra == 20000 and lost == 12000 and lost / extra == 0.6 and extra - lost == 8000
elas = (u1 / u0 - 1) / (p1 / p0 - 1)
cross = (s1 / s0 - 1) / (p1 / p0 - 1)
print("own elasticity", round(elas, 2), "| cross elasticity", round(cross, 2))
assert round(elas, 2) == -2.0 and round(cross, 2) == 0.5
# break-even: what substitute loss makes the category revenue-neutral?
lost_even = d_i / ps
print("category revenue-neutral if substitutes lose", lost_even, "units/day (", round(lost_even / s0 * 100, 2), "% of their units )")
assert lost_even == 8000
# margin view: invented unit cost 300 (illustrative)
c = 300
m0 = u0 * (p0 - c) + s0 * (ps - c)
m1 = u1 * (p1 - c) + s1 * (ps - c)
print("margin/day at unit cost", c, ":", m0, "->", m1, "change", m1 - m0)
assert (m1 - m0) == -4_400_000

# why item-level randomisation overstates: toy logit-share category (invented), half the items get -10%
e, eta = 2.0, 0.3                     # item share elasticity, category elasticity to the price index
def category(frac_treated, n=2000, Q0=200_000):
    w_t, w_c = 0.9 ** (-e), 1.0
    nt = int(n * frac_treated); nc = n - nt
    W = nt * w_t + nc * w_c
    pidx = (nt * 0.9 + nc * 1.0) / n   # simple average price index
    Q = Q0 * pidx ** (-eta)
    ut = Q * w_t / W if nt else 0; uc = Q * w_c / W if nc else 0
    return nt, nc, ut, uc, Q
nt, nc, ut, uc, Q = category(0.5)
base_u = 200_000 / 2000
print("item-randomised: treated item units", round(ut, 1), "control item units", round(uc, 1), "baseline", base_u)
naive = ut / uc - 1
print("naive treated-vs-control unit lift", round(naive, 3))
nt2, nc2, ut2, uc2, Q2 = category(1.0)
true_all = Q2 / 200_000 - 1
print("true category unit lift if every item were cut by 10%", round(true_all, 3), "| control items vs their own baseline", round(uc / base_u - 1, 3))
assert round(naive, 3) == 0.235 and round(true_all, 3) == 0.032 and uc / base_u - 1 < 0
```

**Output (my run):**
```
test items revenue/day 50000000 -> 54000000 change 4000000 (+8.0%)
substitutes revenue/day 120000000 -> 114000000 change -6000000 (-5.0%)
category change -2000000 (-1.18% of 170000000)
price effect on old units -5000000 | revenue from extra units 9000000
extra units on test items 20000 | units lost on substitutes 12000 | share of extra units that is cannibalised 0.6 | net category units 8000
own elasticity -2.0 | cross elasticity 0.5
category revenue-neutral if substitutes lose 8000.0 units/day ( 3.33 % of their units )
margin/day at unit cost 300 : 68000000 -> 63600000 change -4400000
item-randomised: treated item units 112.2 control item units 90.9 baseline 100.0
naive treated-vs-control unit lift 0.235
true category unit lift if every item were cut by 10% 0.032 | control items vs their own baseline -0.091
```

**Follow-ups:**
- *What if the substitute drop is only 3%?* Substitutes lose 3,600,000 and the category is +400,000; the break-even is 3.3%, so the decision is close and needs a proper interval.
- *Is a switchback test enough?* It handles shared customers over time but needs washout between periods because of pull-forward.
- See also Book 6 Part 1, Q40 (a new tab grows while the parent tab loses orders) for the same cannibalisation logic in orders.

**Common mistakes:**
- Reading item lift as category lift.
- Randomising at item level when items substitute.
- Using revenue when the goal is margin.
- Treating the pilot as a forecast.

### Q36 ⭐⭐ 🔴 Healthcare: A deterioration alert model was trained on labels of ICU transfer within 24 hours. After launch, transfers fell from 1,000 to 800 per 20,000 admissions (5.0% to 4.0%, absolute) and the measured positive predictive value of alerts is 18% in live use against 30% in a retrospective replay at the same alert volume of about 1,000 alerts per 20,000 admissions. Explain how effective alerts can look like false positives, why monitoring against the original label can mislead, and how you would evaluate and retrain safely.
**Asked at:** Clinical-ML deployment material (a physician-oriented dataset-shift article, an arXiv paper on what clinicians want from explainable ML, a JMIR paper on alarm fatigue and a circEWS slide deck on calibration and prevalence); research and secondary sources rather than interview banks; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** If clinicians act on the alerts, the patients most likely to be transferred are the ones the alert helps, so the label "ICU transfer within 24 hours" is not generated by the same process that trained the model; an effective alert looks like a false positive, so I would not judge or retrain on that label alone.

**Clarifying questions:**
- How many alerts per 20,000 admissions? The prompt gives PPV but not volume; I assume 1,000 alerts for the hand-check.
- What do clinicians do after an alert (review, extra monitoring, early treatment, escalation)? That is the intervention that changes the outcome.
- Did anything else change at launch (staffing, a rapid-response team, case mix, season)? Transfers fell 1,000 to 800 and other causes can contribute.
- Is there a record of alert response (acknowledged, action taken)? It lets me separate treated from untreated alerts.
- Is a holdout or silent period possible, and who approves it (ethics, clinical safety)? It decides how well I can measure the effect.

**Approach:**
1. Get the numbers straight. Transfers fell from 1,000 to 800 per 20,000: 5.0% to 4.0%, a 1.0 point absolute fall, 20% relative.
2. Hand-check with 1,000 alerts (illustrative): replay PPV 30% = 300 true positives, live 18% = 180, so 120 fewer. If every missing true positive were a patient the alert helped, 120 of the 200 fewer transfers is explained by alerts and 80 by other changes.
3. Prevalence alone does not explain the drop. Keep sensitivity at 30% and the replay false-positive rate; at 4.0% prevalence PPV would be about 25.3%, not 18%.
4. Simulate the mechanism: in my run alerts cut transfer risk by 45% (invented) for alerted patients; the same model had replay PPV 12.0% and live PPV 7.2%, while the untreated deterioration rate among alerted patients was 12.8%. The alerts worked and the PPV fell.
5. Why monitoring against the original label misleads: PPV, recall and calibration measured on "transfer" fall when alerts work. A dashboard would say the model is degrading and prompt a retrain.
6. A naive retrain on live labels makes it worse: the model learns that patients who look like those who were alerted rarely transfer. In my run, at the same probability cut, the alert share fell from 5.12% to 2.44% and mean predicted risk fell from 5.02% to 4.72%.
7. Safer evaluation: (a) define outcomes that survive treatment (deterioration events, rapid response calls, death, ICU transfer or critical intervention as a composite); (b) record whether the alert was acted on and when; (c) compare alerted versus matched non-alerted patients, or use a staged rollout, or a randomised or silent comparison group if clinical safety and ethics approve; (d) use the pre-launch period and the silent mode as the training source.
8. Retrain only with treatment-aware labels (for example the composite, or labels from patients with no alert action) and keep the alert threshold fixed or reviewed by clinicians; check alert burden per nurse and alarm fatigue.

**Metrics:**
- PPV = alerts followed by the outcome / alerts (18% live, 30% replay).
- Composite deterioration rate per 1,000 admissions, split by alerted and not alerted.
- Alert volume per ward per day, time-to-action, acknowledgement rate.
- Recall against the composite outcome; calibration by risk band on untreated patients.
- Guardrails: alarm fatigue (override rate), missed deteriorations, length of stay.

**Risks:**
- The label depends on the response; retraining on it creates a feedback loop.
- Randomised withholding of an alert is an ethics question; ask clinical safety and the ethics process.
- Other changes at launch can explain part of the fall in transfers.
- A model that works can be switched off because the dashboard says PPV is low.

**What the interviewer scores:**
- Strong: names treatment-contaminated labels and shows that PPV falls when alerts work.
- Strong: separates prevalence from the intervention effect with numbers.
- Strong: proposes an outcome that survives treatment and a safe evaluation design with ethics review.
- Weak: "retrain on the new data"; "PPV fell so the model is worse"; ignoring the clinical process.

**Example:** Illustrative numbers from the run. With 1,000 alerts, PPV 30% to 18% means 120 fewer true positives; prevalence alone would give PPV about 25.3%.
- Weak: "PPV fell from 30% to 18%, so the model drifted; retrain on last month."
- Strong: "Transfers also fell 20% relative. If nurses acted on alerts, the alerted patients who improved now count as false positives. Prevalence alone would take PPV to about 25%, so the rest looks like treatment. I would track a composite outcome, compare alerted and matched unalerted patients, and retrain only with treatment-aware labels."

**Code:**
```python
import numpy as np

# prompt arithmetic
adm, t0, t1 = 20000, 1000, 800
print("transfer rate", t0 / adm, "->", t1 / adm, "| absolute", round((t0 - t1) / adm, 3), "| relative", (t0 - t1) / t0)
assert t0 / adm == 0.05 and t1 / adm == 0.04 and (t0 - t1) / t0 == 0.2

# Illustrative hand-check: assume 1,000 alerts per 20,000 admissions (the prompt gives PPV, not volume)
V = 1000
tp_replay, tp_live = 0.30 * V, 0.18 * V
print("true positives among alerts: replay", tp_replay, "live", tp_live, "| missing", tp_replay - tp_live)
assert tp_replay == 300 and tp_live == 180 and tp_replay - tp_live == 120
print("recall vs transfers: replay", tp_replay / t0, "live", tp_live / t1)
assert tp_replay / t0 == 0.3 and tp_live / t1 == 0.225
# if alerts prevented X transfers among alerted patients and nothing else changed: X = 120 of the 200 fewer transfers
print("transfers fewer in total", t0 - t1, "| of which alert-saved if PPV drop is all treatment", tp_replay - tp_live, "| the other", (t0 - t1) - (tp_replay - tp_live), "from other causes or non-alerted")
assert (t0 - t1) - (tp_replay - tp_live) == 80

# prevalence alone (same sensitivity 30% and same false-positive rate as replay)
sens = tp_replay / t0
fpr = (V - tp_replay) / (adm - t0)
tp_p = sens * t1; fp_p = fpr * (adm - t1)
print("prevalence-only PPV", round(tp_p / (tp_p + fp_p), 3), "| alert volume would be", round(tp_p + fp_p))
assert round(tp_p / (tp_p + fp_p), 3) == 0.253

# simulation: alerts change outcomes, so the label (ICU transfer) understates true deterioration
rng = np.random.default_rng(36)
def make(n):
    r = rng.beta(1.0, 19, n)                       # latent risk of deterioration w/o intervention
    X = np.c_[np.log(r / (1 - r)) + rng.normal(0, 1.0, n), rng.normal(size=n)]   # noisy vital-sign score + noise
    return r, X
def fit(X, y, it=30):
    A = np.c_[np.ones(len(X)), X]; w = np.zeros(3)
    for _ in range(it):
        mu = 1 / (1 + np.exp(-(A @ w))); W = mu * (1 - mu)
        w += np.linalg.solve(A.T @ (A * W[:, None]) + 1e-6 * np.eye(3), A.T @ (y - mu))
    return w
score = lambda w, X: np.c_[np.ones(len(X)), X] @ w
n = 200_000
r0, X0 = make(n); y0 = (rng.random(n) < r0).astype(float)          # pre-launch labels
w1 = fit(X0, y0)
rep = 0.05
thr = np.quantile(score(w1, X0), 1 - rep)
alert0 = score(w1, X0) >= thr
print("replay: alert share", round(alert0.mean(), 3), "| PPV", round(y0[alert0].mean(), 3), "| prevalence", round(y0.mean(), 4))
eff = 0.45                                         # invented: intervention cuts transfer risk 45% (relative) when alerted
r1, X1 = make(n); a1 = score(w1, X1) >= thr
p1 = r1 * np.where(a1, 1 - eff, 1.0)
y1 = (rng.random(n) < p1).astype(float)
print("live  : alert share", round(a1.mean(), 3), "| PPV", round(y1[a1].mean(), 3), "| prevalence", round(y1.mean(), 4))
tp_live_ = y1[a1].mean()
print("true deterioration rate among alerted (untreated risk)", round(r1[a1].mean(), 3))
assert y1[a1].mean() < y0[alert0].mean() and y1.mean() < y0.mean()
# naive retrain on live labels: the model learns "alerted-looking patients rarely transfer"
w2 = fit(X1, y1)
sig = lambda z: 1 / (1 + np.exp(-z))
p_cut = sig(thr)                                   # the probability cut the original model used
share_orig = (sig(score(w1, X1)) >= p_cut).mean()
share_naive = (sig(score(w2, X1)) >= p_cut).mean()
print("alert share at the same probability cut: original", round(share_orig, 4), "| naive retrain on live labels", round(share_naive, 4))
print("mean predicted risk: original", round(sig(score(w1, X1)).mean(), 4), "| naive retrain", round(sig(score(w2, X1)).mean(), 4), "| mean untreated risk", round(r1.mean(), 4), "| observed live rate", round(y1.mean(), 4))
print("coefficients original", np.round(w1, 3), "naive retrain", np.round(w2, 3))
assert share_naive < share_orig
assert round(y0[alert0].mean(), 3) == 0.12 and round(y1[a1].mean(), 3) == 0.072
assert round(share_orig, 4) == 0.0512 and round(share_naive, 4) == 0.0244
```

**Output (my run):**
```
transfer rate 0.05 -> 0.04 | absolute 0.01 | relative 0.2
true positives among alerts: replay 300.0 live 180.0 | missing 120.0
recall vs transfers: replay 0.3 live 0.225
transfers fewer in total 200 | of which alert-saved if PPV drop is all treatment 120.0 | the other 80.0 from other causes or non-alerted
prevalence-only PPV 0.253 | alert volume would be 947
replay: alert share 0.05 | PPV 0.12 | prevalence 0.0501
live  : alert share 0.051 | PPV 0.072 | prevalence 0.0472
true deterioration rate among alerted (untreated risk) 0.128
alert share at the same probability cut: original 0.0512 | naive retrain on live labels 0.0244
mean predicted risk: original 0.0502 | naive retrain 0.0472 | mean untreated risk 0.0501 | observed live rate 0.0472
coefficients original [-1.579  0.453  0.014] naive retrain [-1.819  0.387 -0.009]
```

**Follow-ups:**
- *How would you measure the benefit of the alerts?* Compare the composite outcome in matched or staged groups; ask clinical safety about a holdout.
- *Could the fall in transfers be a worse miss instead?* Yes: patients may deteriorate and die on the ward without transfer. Track deaths and the composite outcome, not only transfers.
- See also Book 6 Part 3, Q23 (a rare-disease screen where PPV depends on prevalence) for the base-rate arithmetic.

**Common mistakes:**
- Reading PPV on a treated outcome as model quality.
- Retraining on the contaminated label.
- Ignoring that a positive intervention changes the labels.
- Assuming the whole PPV drop is prevalence (it is not, by the arithmetic).

### Q37 ⭐⭐ 🔴 Ads: Conversions arrive late, and the share of eventual conversions already observed is 50% for clicks 0 days old, 70% at 1 day, 80% at 2, 90% at 3, 95% at 4, 98% at 5 and 100% at 6 days. A conversion model is retrained daily on the last 7 days of clicks (ages 0 to 6 days, equal click volume per age), labelling unconverted clicks as negative. Compute the average share of conversions observed across those 7 ages and the relative underestimate of the conversion rate, and describe a delayed-feedback fix.
**Asked at:** Ads ML and calibration material (Dataford questions on CTR calibration and click-through rate at an ad-tech firm, AlgoMaster and Educative ad click prediction system-design pages with calibration-error checks by probability bin); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
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

**Code:**
```python
import numpy as np

F = np.array([0.50, 0.70, 0.80, 0.90, 0.95, 0.98, 1.00])
ages = np.arange(7)
avg = F.mean()
print("sum of shares", round(F.sum(), 2), "| average observed share", round(avg, 4), "| relative underestimate", round(1 - avg, 4))
assert round(F.sum(), 2) == 5.83 and round(avg, 4) == 0.8329 and round(1 - avg, 4) == 0.1671

# simulate: true conversion rate 5%, delay distribution implied by F; labels as seen at training time
rng = np.random.default_rng(37)
clicks_per_age, cvr = 200_000, 0.05
inc = np.diff(np.r_[0, F])                           # share of eventual conversions arriving on each delay day
obs_conv = np.zeros(7); true_conv = np.zeros(7)
for a in ages:
    conv = rng.random(clicks_per_age) < cvr
    # delay day d with probability inc[d] (d = 0..6); observed if d <= age
    d = rng.choice(7, size=clicks_per_age, p=inc)
    true_conv[a] = conv.sum()
    obs_conv[a] = (conv & (d <= a)).sum()
naive = obs_conv.sum() / (7 * clicks_per_age)
print("true rate", round(true_conv.sum() / (7 * clicks_per_age), 4), "| naive training rate", round(naive, 4), "| ratio", round(naive / cvr, 3))
assert abs(naive / cvr - avg) < 0.01
# fix A: train only on mature clicks (age 6): unbiased but only 1/7 of the volume and a week stale
print("mature-only (age 6) rate", round(obs_conv[6] / clicks_per_age, 4), "| rows used", clicks_per_age, "of", 7 * clicks_per_age)
# fix B: inverse-maturity correction per age bucket (estimating F from older cohorts, known here)
corr = (obs_conv / F).sum() / (7 * clicks_per_age)
print("rate after dividing each age bucket by its observed share", round(corr, 4))
assert abs(corr - cvr) < 0.003
# per-age naive rates: shows where the bias sits
print("naive rate by age", np.round(obs_conv / clicks_per_age, 4))
# fix C: label-time correction on click-level probabilities: p_true ~= p_seen / F(age)  (calibration intuition)
print("age-0 clicks look like", round(0.5 * cvr, 4), "instead of", cvr, "-> a model that ignores age learns", round(avg * cvr, 4), "on average")
assert round(avg * cvr, 4) == 0.0416
# a delayed-feedback style model: P(conv seen at age a) = p * F(a); fit p by maximum likelihood on (age, seen)
seen = []; ag = []
for a in ages:
    conv = rng.random(clicks_per_age) < cvr
    d = rng.choice(7, size=clicks_per_age, p=inc)
    seen.append(conv & (d <= a)); ag.append(np.full(clicks_per_age, a))
seen = np.concatenate(seen); ag = np.concatenate(ag)
grid = np.linspace(0.02, 0.08, 601)
ll = [(seen * np.log(p * F[ag]) + (~seen) * np.log(1 - p * F[ag])).sum() for p in grid]
p_hat = grid[int(np.argmax(ll))]
print("maximum-likelihood p with known F(age):", round(p_hat, 4))
assert abs(p_hat - cvr) < 0.002
```

**Output (my run):**
```
sum of shares 5.83 | average observed share 0.8329 | relative underestimate 0.1671
true rate 0.0502 | naive training rate 0.0418 | ratio 0.837
mature-only (age 6) rate 0.0493 | rows used 200000 of 1400000
rate after dividing each age bucket by its observed share 0.0503
naive rate by age [0.0253 0.0356 0.0396 0.0461 0.0476 0.0494 0.0493]
age-0 clicks look like 0.025 instead of 0.05 -> a model that ignores age learns 0.0416 on average
maximum-likelihood p with known F(age): 0.0499
```

**Follow-ups:**
- *What if the window is 14 days?* Average maturity rises (more complete days), but the freshness cost rises too.
- *Does the bias affect ranking?* Only if the bias differs by campaign or age mix, which it often does.
- *Why not just wait 6 days?* Fine when freshness is not important; ads usually need fresher models.

**Common mistakes:**
- Treating all unconverted clicks as true negatives.
- Averaging maturity with unequal click volume per age.
- Alerting on young-cohort calibration.
- Using the age as a feature at serving time.

### Q38 ⭐⭐ 🔴 Ads: After an exchange moves from second-price to first-price auctions, an impression is worth 10 to you. From logged auctions your estimated win probability is 20% at a bid of 4, 45% at 6, 60% at 7, 75% at 8, 88% at 9 and 95% at 10 (estimates). Under first price you pay your bid when you win, so compute the expected surplus (value minus bid, times win probability) at each bid, name the best bid and explain how you would break the tie, estimate the win curve and spot when it breaks.
**Asked at:** Ad-serving system-design material (techinterview.org ad serving and real-time bidding pages, a Dataford question on budget pacing and frequency capping, machinelearningatscale.com on frequency capping; feedback-controller pacing, per-user counters and credits for invalid clicks appear in the snippets); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Expected surplus at bids 4, 6, 7, 8, 9, 10 is 1.20, 1.80, 1.80, 1.50, 0.88 and 0.00, so bids 6 and 7 tie at 1.80 per auction; I would break the tie by what the campaign is short of (budget favours 6, volume favours 7), and I would keep re-estimating the win curve because it moves.

**Clarifying questions:**
- Is the budget the binding constraint, or is there a delivery commitment (a minimum number of impressions)? It decides the tie.
- Does the exchange tell us the winning price or minimum bid to win? It determines whether the win curve is censored.
- How many logged auctions sit behind each of the six estimates? With few auctions each point carries a wide range.
- Is the value of 10 per impression certain and the same on every impression? Value uncertainty changes how much to shade.
- How fast do competitors adapt after the change to first price? It sets how often the curve must be refit.

**Approach:**
1. Compute surplus = (10 - bid) x win probability: bid 4: 6 x 0.20 = 1.20; 6: 4 x 0.45 = 1.80; 7: 3 x 0.60 = 1.80; 8: 2 x 0.75 = 1.50; 9: 1 x 0.88 = 0.88; 10: 0 x 0.95 = 0.
2. Name the best bid: 6 and 7 tie at 1.80 per auction, which is 1,800 per 1,000 auctions either way.
3. Break the tie with the next constraint. Spend per auction is 6 x 0.45 = 2.70 at a bid of 6 and 7 x 0.60 = 4.20 at 7. Going from 6 to 7 buys 0.15 more win probability for 1.50 more spend, a marginal 10 per extra win (7 x 0.60 - 6 x 0.45 = 1.5, divided by 0.15), exactly the value, so it adds no surplus. If budget is binding, bid 6 (surplus per unit of spend is 0.667 versus 0.429) and use the saved spend elsewhere. If there is a volume commitment or a learning phase, bid 7 gets 600 wins per 1,000 auctions instead of 450 at no loss of surplus.
4. Do not trust the grid to the cent. The ranges at 400 auctions per point are about +/- 0.05 in win probability, which is +/- 0.20 in surplus at a bid of 6 and +/- 0.14 at 7. The tie is inside the noise. A linear guess at 6.5 gives 1.84 but that is an untested interpolation.
5. Estimate the win curve from logs: for every auction record bid, win or loss, and (if available) the winning price; fit a monotone curve (isotonic or a logistic on bid or log bid), or a censored model if only wins reveal prices. Add a small randomised bid perturbation so the curve is identified across the range you may use.
6. Spot when it breaks: compare predicted win rate with live win rate by bid bucket every day. In the run a competitor shift of one unit right makes the old 7 win like the old 6 (60% predicted, 45% live): z = -6.1 on 400 auctions. After such a shift the best bid on the shifted curve is 7 with surplus 1.35.
7. Rules for retraining: refit when the gap exceeds an agreed number of standard errors for several buckets, and always after an exchange rule change.
8. Guardrails: never bid above value (10), keep the budget pacing in view, and log the bids so the next curve can be estimated.

**Metrics:**
- Expected surplus per auction = (value - bid) x P(win | bid).
- Win rate by bid bucket, predicted versus live; spend per win; effective cost per impression won.
- Surplus per 1,000 auctions and per unit of spend.
- Guardrails: delivery against commitment, budget exhaustion time, curve gap (live minus predicted).

**Risks:**
- The win curve is estimated, not known; the best bid is a guess with an error bar.
- Censoring: if you only learn the clearing price on wins, extrapolation below your lowest logged bid is unsupported.
- Competitors change their bidding in response to yours.
- Paying your bid means any overestimate of the win curve costs money directly.
- Value per impression varies; one value for all impressions is a simplification.

**What the interviewer scores:**
- Strong: gets the six surplus numbers and sees the tie at 6 and 7.
- Strong: breaks the tie with budget versus volume and shows the marginal cost of 10 per extra win.
- Strong: explains how to estimate a censored win curve and how to detect a break.
- Weak: "bid your value" (a second-price habit); a single best bid with no uncertainty.

**Example:** Illustrative numbers from the run. Surplus 1.20, 1.80, 1.80, 1.50, 0.88, 0.00; per 1,000 auctions a bid of 6 wins 450, spends 2,700 and earns surplus 1,800; a bid of 7 wins 600, spends 4,200 and earns 1,800.
- Weak: "Bid 10, it is worth ten."
- Strong: "In first price I pay my bid, so I shade. Surplus peaks at 1.80 for both 6 and 7. Going to 7 buys 150 extra wins per 1,000 for 1,500 extra spend, 10 each, so no surplus gain. With a budget limit I bid 6; with a delivery target I bid 7. I will check the win curve daily and refit when it moves."

**Code:**
```python
from fractions import Fraction as Fr
import numpy as np

V = 10
win = {4: Fr(20, 100), 6: Fr(45, 100), 7: Fr(60, 100), 8: Fr(75, 100), 9: Fr(88, 100), 10: Fr(95, 100)}
surplus = {b: (V - b) * w for b, w in win.items()}
spend = {b: b * w for b, w in win.items()}
for b in win:
    print(f"bid {b:>2}: win {float(win[b]):.2f} | surplus {float(surplus[b]):.2f} | expected spend per auction {float(spend[b]):.2f} | surplus per unit spend {float(surplus[b]/spend[b]):.3f}")
best = max(surplus.values())
tied = [b for b, s in surplus.items() if s == best]
print("best surplus", float(best), "at bids", tied)
assert best == Fr(18, 10) and tied == [6, 7]
assert surplus[4] == Fr(6, 5) and surplus[8] == Fr(3, 2) and surplus[9] == Fr(22, 25) and surplus[10] == 0
# tie: the step from 6 to 7 buys 0.15 more win probability for 1.5 more spend per auction and adds zero surplus
dw = win[7] - win[6]; ds = spend[7] - spend[6]
print("6 -> 7: extra win prob", float(dw), "| extra spend per auction", float(ds), "| extra surplus", float(surplus[7] - surplus[6]))
assert dw == Fr(3, 20) and ds == Fr(3, 2)
# marginal cost per extra win: (7*0.6 - 6*0.45)/(0.6-0.45) = 10 -> equals the value, so zero surplus
print("marginal cost per extra win going 6 -> 7:", float(ds / dw))
assert ds / dw == 10
# volume view: 1,000 auctions
for b in (6, 7):
    print(f"1,000 auctions at bid {b}: wins {float(win[b]*1000):.0f}, spend {float(spend[b]*1000):.0f}, surplus {float(surplus[b]*1000):.0f}")
# interpolation is a guess, not data: linear win curve between 6 and 7 gives bid 6.5
w65 = (win[6] + win[7]) / 2
print("linear-interpolated bid 6.5:", float(w65), "surplus", float((V - Fr(13, 2)) * w65), "(untested; depends on the curve shape between the points)")
assert (V - Fr(13, 2)) * w65 == Fr(14700, 8000)
# estimating the win curve with noise: how uncertain is each estimate with n logged auctions near the bid?
rng = np.random.default_rng(38)
n = 400
for b in (6, 7):
    p = float(win[b]); se = (p * (1 - p) / n) ** 0.5
    print(f"bid {b}: with {n} auctions per point, win prob {p:.2f} +- {1.96*se:.3f}; surplus +- {1.96*se*(V-b):.3f}")
# drift alarm: a competitor shifts the curve right by 1 unit, so the old bid 7 now wins like the old bid 6
pred = float(win[7]); actual = float(win[6])
z = (actual - pred) / (pred * (1 - pred) / n) ** 0.5
print("bid 7 predicted win", pred, "live win", actual, "| z with", n, "live auctions:", round(z, 1))
assert round(z, 1) == -6.1
# what the shift does to the best bid: shifted curve, same value 10
sh = {b + 1: w for b, w in win.items()}              # bids 5, 7, 8, 9, 10, 11 carry the old win rates
sh_s = {b: (V - b) * w for b, w in sh.items() if b <= V}
print("shifted-curve surplus by bid:", {b: float(s_) for b, s_ in sh_s.items()})
print("best shifted bids:", [b for b, s_ in sh_s.items() if s_ == max(sh_s.values())], "with surplus", float(max(sh_s.values())))
assert max(sh_s.values()) == Fr(27, 20) and [b for b, s_ in sh_s.items() if s_ == Fr(27, 20)] == [7]
```

**Output (my run):**
```
bid  4: win 0.20 | surplus 1.20 | expected spend per auction 0.80 | surplus per unit spend 1.500
bid  6: win 0.45 | surplus 1.80 | expected spend per auction 2.70 | surplus per unit spend 0.667
bid  7: win 0.60 | surplus 1.80 | expected spend per auction 4.20 | surplus per unit spend 0.429
bid  8: win 0.75 | surplus 1.50 | expected spend per auction 6.00 | surplus per unit spend 0.250
bid  9: win 0.88 | surplus 0.88 | expected spend per auction 7.92 | surplus per unit spend 0.111
bid 10: win 0.95 | surplus 0.00 | expected spend per auction 9.50 | surplus per unit spend 0.000
best surplus 1.8 at bids [6, 7]
6 -> 7: extra win prob 0.15 | extra spend per auction 1.5 | extra surplus 0.0
marginal cost per extra win going 6 -> 7: 10.0
1,000 auctions at bid 6: wins 450, spend 2700, surplus 1800
1,000 auctions at bid 7: wins 600, spend 4200, surplus 1800
linear-interpolated bid 6.5: 0.525 surplus 1.8375 (untested; depends on the curve shape between the points)
bid 6: with 400 auctions per point, win prob 0.45 +- 0.049; surplus +- 0.195
bid 7: with 400 auctions per point, win prob 0.60 +- 0.048; surplus +- 0.144
bid 7 predicted win 0.6 live win 0.45 | z with 400 live auctions: -6.1
shifted-curve surplus by bid: {5: 1.0, 7: 1.35, 8: 1.2, 9: 0.75, 10: 0.0}
best shifted bids: [7] with surplus 1.35
```

**Follow-ups:**
- *What if the value is uncertain?* Shade on the expected value, and consider a conservative multiplier until the value model is calibrated.
- *Would you change the bid per impression?* Yes, bid is a function of predicted value and the win curve per segment.
- *Is there a bid between 6 and 7 that beats both?* Possibly, but it is not in the data; test it through randomised bid perturbation.

**Common mistakes:**
- Bidding value in first price.
- Treating a tie as a result and ignoring budget or volume.
- Extrapolating the win curve outside logged bids.
- Not monitoring the curve after the format change.

### Q39 ⭐⭐ 🔴 Ads: Total sales are 100,000,000 over a test period spread evenly across 50 regions, and last-click attribution credits online video with 1,000,000 of them (1% of sales). A geo test paused video in 10 randomly chosen regions and sales there were 4% lower than the kept regions' with-video level of 2,000,000 per region. Project the whole-country sales attributable to video if the effect is uniform, compare it with the last-click credit, and explain the assumptions and what a 10-region test can and cannot tell you.
**Asked at:** Ads measurement material (an eMarketer 2026 FAQ separating incrementality, multi-touch attribution and marketing mix modelling, Google ads-measurement data scientist postings asking for causal inference and attribution work, a Dataford incremental-lift question, a Remerge incrementality write-up); job postings and prep material rather than a confirmed interview round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** If the 4% drop is uniform, video drives about 4,000,000 of the 100,000,000 sales (4%), four times the 1,000,000 that last-click credits; this is a projection from 10 regions, so I would report a range and the assumptions, not a point.

**Clarifying questions:**
- Is the 100,000,000 the with-video level in all 50 regions, and is the 4% measured against the kept regions' level (2,000,000 each)? I read it that way; another base changes the answer slightly (4.17% of the no-video level).
- How were the 10 regions chosen, and were pre-period sales compared? Random choice helps, but 10 of 50 can still be unbalanced.
- How long was the pause, and how long do video effects last? A short test misses lagged effects.
- Do regions leak (people travel, national media, shared online audiences)? Leakage shrinks the measured gap.
- What did video cost in the period? Incremental sales alone do not say whether it paid.

**Approach:**
1. The arithmetic. Each region sells 100,000,000 / 50 = 2,000,000. A 4% drop is 80,000 per paused region, 800,000 for the 10 regions, and scaled to 50 regions 4,000,000. The observed total in the test was 99,200,000.
2. Compare with last click: 4,000,000 / 1,000,000 = 4.0 times; video is 4% of sales on this projection versus 1% credited.
3. Put a range on it with an invented noise level (relative sales noise per region after matching): with 2% noise the 95% interval for the effect is 2.6% to 5.4% (2.6M to 5.4M), at 3% it is 1.9% to 6.1%, and at 6% it is -0.2% to 8.2%, which includes zero. So the point estimate is far less informative than it looks when regions are noisy.
4. Improve the estimate: compare each region with its own pre-period (difference-in-differences) or use matched regions or synthetic controls. In my simulation of 4,000 random assignments with a true 4%, comparing levels gave a standard deviation of 16.8 points (regions differ in size), while comparing with each region's pre-period gave 1.1 points and only 0.45% of assignments came out below 1%.
5. Assumptions to state: uniform effect across regions; no spillover; stable effect over time; the 40 control regions kept normal spend; no other channel changed; the effect measured at the current spend level.
6. What a 10-region test can tell you: the average incremental effect of switching video off at the current spend, with a range. What it cannot: the shape of diminishing returns (it is an on/off test), effects by region type, long-run brand effects, interaction with other channels, or the return per unit of spend.
7. Use it: calibrate the attribution model or the marketing-mix model with the test result (a lift test as a prior); rerun with more regions, more spend levels (a dose test) or a longer window.
8. Report: incremental sales, range, cost, and incremental return, and say that last click and lift measure different things (see Book 6 Part 5, Q11 on reported versus incremental return on ad spend).

**Metrics:**
- Lift = 1 - (sales in paused regions / counterfactual sales) = 4% (paused regions sell 96% of the kept level).
- Incremental sales = lift x total sales with video = 0.04 x 100,000,000 = 4,000,000.
- Ratio to last click = incremental / credited = 4.0.
- Incremental return = incremental sales (or margin) / video spend (spend not given in the prompt).
- Guardrails: pre-period balance between arms, spillover check using neighbouring regions, test duration.

**Risks:**
- Noise: 10 regions is a small test; a 3% regional noise gives a 4% effect with a 1.9% to 6.1% range, and 6% noise makes it inconclusive.
- Random assignment can still leave unbalanced regions; use pre-period matching.
- Spillover and national media bias the gap towards zero.
- The effect at one spend level does not extend to doubling or halving spend.
- Last click and lift may both be right about different things (assist versus incremental).

**What the interviewer scores:**
- Strong: 4,000,000 versus 1,000,000, with the base stated and a range.
- Strong: pre-period adjustment and the fact that 10 regions cannot give a response curve.
- Strong: lists assumptions (uniform, no spillover, short horizon).
- Weak: "video is worth 4x last click" as fact; no uncertainty; ignores cost.

**Example:** Illustrative numbers from the run. 800,000 lost in 10 regions scales to 4,000,000; at region-level noise of 3% the 95% range is 1.9M to 6.1M.
- Weak: "Last click says 1 million, the test says 4 million, so last click is wrong."
- Strong: "If the 4% is uniform, video is about 4 million of sales, four times last click. With 10 regions the range could be roughly 2 to 6 million, so I would compare against the regions' own history, check for spillover, and weigh it against video spend. It tells me about on versus off at this spend, not the return of one more unit."

**Code:**
```python
import numpy as np
from math import sqrt

total, regions, lastclick = 100_000_000, 50, 1_000_000
per_region = total / regions
drop = 0.04
print("sales per region", per_region, "| last-click share", lastclick / total)
assert per_region == 2_000_000 and lastclick / total == 0.01
# reading A: with-video sales are the base (kept regions); paused regions sell 96% of that
inc_A = total * drop
print("A: incremental sales if 4% of with-video sales:", inc_A, "| vs last-click", inc_A / lastclick, "x")
assert inc_A == 4_000_000 and inc_A / lastclick == 4.0
# base check: the 100,000,000 is the with-video level in every region; paused regions then sell 96% of 2,000,000
observed = 40 * per_region + 10 * per_region * 0.96
print("observed total in the test period", observed, "| counterfactual with video everywhere", total, "| incremental", total - observed, "(this is the 10 paused regions only)")
print("incremental as a share of the no-video level:", round(total / (total * 0.96) - 1, 4))
assert observed == 99_200_000 and round(total / (total * 0.96) - 1, 4) == 0.0417
# the 4% measured on 10 regions: projection to 50 assumes uniform effect
print("10 paused regions lost", 10 * per_region * drop, "in the test period; scaled x5 =", 5 * 10 * per_region * drop)
assert 10 * per_region * drop == 800_000 and 5 * 10 * per_region * drop == 4_000_000
# uncertainty (invented): region-level relative noise sd after matching on pre-period
for sd in (0.02, 0.03, 0.06):
    se = sd * sqrt(1 / 10 + 1 / 40)
    lo, hi = drop - 1.96 * se, drop + 1.96 * se
    print(f"region-level sd {sd:.0%}: se {se:.4f} | 95% interval {lo:.3%} to {hi:.3%} -> {lo*total:,.0f} to {hi*total:,.0f} | z {drop/se:.1f}")
assert round(0.03 * sqrt(0.125), 4) == 0.0106
# when does the interval reach the last-click 1%? credit 1,000,000 = 1% of sales
# simulate random 10-of-50 assignments: unadjusted vs pre-period-adjusted estimate
rng = np.random.default_rng(39)
size = rng.lognormal(0, 0.5, regions); size = size / size.mean() * per_region        # unequal regions
pre = size * np.exp(rng.normal(0, 0.03, regions))
true_eff = 0.04
est_raw, est_adj = [], []
for _ in range(4000):
    t = rng.permutation(regions)[:10]; c = np.setdiff1d(np.arange(regions), t)
    post = pre * np.exp(rng.normal(0, 0.03, regions)) * (1 - true_eff * np.isin(np.arange(regions), t))
    ratio_t = post[t].sum() / pre[t].sum(); ratio_c = post[c].sum() / pre[c].sum()
    est_adj.append(1 - ratio_t / ratio_c)                                              # change vs own pre-period
    est_raw.append(1 - post[t].mean() / post[c].mean())                                # levels only
est_raw, est_adj = np.array(est_raw), np.array(est_adj)
print("simulated 4,000 random assignments, true effect 4%:")
print("  level comparison: mean", round(est_raw.mean(), 4), "sd", round(est_raw.std(), 4))
print("  versus-own-pre-period: mean", round(est_adj.mean(), 4), "sd", round(est_adj.std(), 4))
assert est_adj.std() < est_raw.std() and abs(est_adj.mean() - 0.04) < 0.003
# share of assignments in which the estimate is below the last-click 1% credit level
print("share of assignments with estimated effect below 1%:", round((est_adj < 0.01).mean(), 4), "(adjusted) |", round((est_raw < 0.01).mean(), 4), "(unadjusted)")
```

**Output (my run):**
```
sales per region 2000000.0 | last-click share 0.01
A: incremental sales if 4% of with-video sales: 4000000.0 | vs last-click 4.0 x
observed total in the test period 99200000.0 | counterfactual with video everywhere 100000000 | incremental 800000.0 (this is the 10 paused regions only)
incremental as a share of the no-video level: 0.0417
10 paused regions lost 800000.0 in the test period; scaled x5 = 4000000.0
region-level sd 2%: se 0.0071 | 95% interval 2.614% to 5.386% -> 2,614,071 to 5,385,929 | z 5.7
region-level sd 3%: se 0.0106 | 95% interval 1.921% to 6.079% -> 1,921,106 to 6,078,894 | z 3.8
region-level sd 6%: se 0.0212 | 95% interval -0.158% to 8.158% -> -157,788 to 8,157,788 | z 1.9
simulated 4,000 random assignments, true effect 4%:
  level comparison: mean 0.0373 sd 0.1683
  versus-own-pre-period: mean 0.0399 sd 0.0114
share of assignments with estimated effect below 1%: 0.0045 (adjusted) | 0.412 (unadjusted)
```

**Follow-ups:**
- *Why might last click undercount video?* It credits the final touch, and video often creates demand that later converts through search or direct.
- *Could the true effect be bigger than the test?* Yes if spillover leaks sales into the kept regions; no if the paused regions got other media.
- *What next?* A larger, longer test with matched pairs, or varying spend levels to get a response curve.

**Common mistakes:**
- Treating the 4% as exact.
- Comparing regional levels without the pre-period.
- Using one on/off test to set the budget.
- Ignoring cost.

### Q40 ⭐ 🟢 E-commerce: 6% of 1,000,000 daily searches return no results, which is 60,000 searches, and a manual review of 500 of those found 200 (40%) were spelling or synonym problems and 100 (20%) were products the catalogue genuinely lacks. Estimate the daily searches in each of those two groups as projections, and explain what you would build first, how you would measure its effect, and how you would pass the missing-product signal to sellers.
**Asked at:** E-commerce ML material (prachub lists Shopify questions on product ranking for a marketplace, package delivery time prediction and personalised product feeds, and a CleverPrep Shopify guide lists search-ranking and embedding trade-offs; Interview Query notes e-commerce promotion and behaviour modelling); candidate-reported and prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** About 24,000 of the 60,000 zero-result searches a day are spelling or synonym problems and about 12,000 are products the catalogue lacks (projections from a 500-search review); I would build spelling and synonym handling first because it is the largest fixable group, measure it with an A/B test on those searches, and give sellers an aggregated, privacy-safe demand report for the missing products.

**Clarifying questions:**
- Were the 500 searches sampled at random from the 60,000 searches, or from distinct queries? Sampling searches weights head queries correctly; sampling queries does not.
- What are the other 200 (40%): filters too narrow, out of stock, ambiguous, junk? That group is as large as the spelling group and may be cheap to fix.
- How does the current search handle typos and synonyms (any correction, stemming, a synonym list)? It sets how much is new.
- Can a search that returns results still be bad? Fixing zero results should not just replace "no results" with irrelevant results.
- Which sellers can add listings, and is there a policy team for restricted items? It shapes what we can pass on.

**Approach:**
1. Projections: 6% x 1,000,000 = 60,000 zero-result searches. Spelling or synonym: 200 / 500 = 40% x 60,000 = 24,000 a day (95% range about 21,400 to 26,600). Genuinely missing: 100 / 500 = 20% x 60,000 = 12,000 a day (range about 9,900 to 14,100). Other: 40% = 24,000.
2. Build first: query understanding for spelling and synonyms. Start from logs: zero-result queries that users reformulate within the session into a query with clicks give pairs (typo to fixed query, trainers to sneakers). Combine with a vocabulary-based corrector. In a small test, string similarity fixed "runing shoes", "wireles headphones" and "fone charger" but could not fix "kettlebell" (missing) or "trainers" (a synonym), so synonyms need a separate dictionary or learned model.
3. Roll out safely: auto-correct only above a confidence threshold, otherwise show "did you mean"; always keep the user's original query visible.
4. Size the benefit: fixing half the spelling group puts 12,000 searches a day back to having results and lowers the zero-result rate from 6.0% to 4.8%; fixing 80% gives 4.08%.
5. Measure with an A/B test on searches that would have returned zero results: randomise users, compare search-to-click, add-to-cart and orders per search, revenue per search. Zero-result rate alone is a vanity metric because a correction that returns junk lowers it too.
6. Guardrails: relevance judged by a labelled sample of corrected searches (wrong correction rate), reformulation rate, latency, and bounce or exit rate.
7. Missing-product signal for sellers: normalise and cluster the 12,000-a-day group by intent, publish only terms searched by at least K distinct users (K = 20 in my toy example, which kept three terms and dropped two small ones, one of them a one-user term that looked like a person's name), exclude personal or sensitive queries and prohibited items, and verify the product is truly missing (not out of stock or mis-categorised).
8. Present to sellers as weekly demand gaps: term cluster, searches per day, trend, and the category. Check with the trust and policy team and legal or privacy about what can be shown to sellers. Measure the effect by gaps filled and sales on newly listed items.

**Metrics:**
- Zero-result rate = searches with no results / all searches (6%).
- Recovered searches = zero-result searches that now return results and get a click / zero-result searches.
- Search-to-click rate and orders per search on the treated group; revenue per search.
- Wrong-correction rate = corrections judged irrelevant / corrections shown.
- Seller side: gaps published, gaps filled, sales on filled gaps.

**Risks:**
- Auto-correcting a rare, correct word into a common one (a brand name) hurts users.
- Sampling searches versus queries changes the shares.
- The missing-product group may include illegal, restricted or irrelevant demand.
- Small counts in seller reports can expose individual users.
- 500 reviewed searches are a sample; ranges are about +/- 4 points.

**What the interviewer scores:**
- Strong: 24,000 and 12,000, labelled projections, and notices the other 24,000.
- Strong: builds query understanding first, with confidence thresholds and an A/B test on the affected searches.
- Strong: measures revenue or conversion, not only the zero-result rate; privacy threshold for the seller report.
- Weak: "build a bigger index"; "reduce the zero-result rate" as the only goal.

**Example:** Illustrative numbers from the run. 60,000 zero-result searches; 24,000 spelling or synonym, 12,000 missing, 24,000 other. Fixing half the spelling group moves the zero-result rate from 6.0% to 4.8%.
- Weak: "We should add more products so people find results."
- Strong: "About 24,000 a day are typos or synonyms and 12,000 are real catalogue gaps, so I would build spelling and synonym handling first, with a confidence threshold, and A/B test on those searches measuring orders per search. For the 12,000 I would send sellers a weekly list of terms searched by at least 20 users, after the policy team checks the list."

**Code:**
```python
import difflib
import numpy as np
from math import sqrt
from collections import Counter

searches, zr = 1_000_000, 0.06
zero = searches * zr
n, spell_k, missing_k = 500, 200, 100
print("zero-result searches/day", zero)
assert zero == 60_000
sp, mi = spell_k / n, missing_k / n
oth = 1 - sp - mi
proj = {"spelling/synonym": zero * sp, "genuinely missing": zero * mi, "other": zero * oth}
print({k: round(v) for k, v in proj.items()}, "| other share", round(oth, 2))
assert proj["spelling/synonym"] == 24_000 and proj["genuinely missing"] == 12_000 and round(proj["other"]) == 24_000
for name, k in (("spelling/synonym", spell_k), ("missing", missing_k)):
    p = k / n; se = sqrt(p * (1 - p) / n)
    print(f"{name}: share {p:.0%} +- {1.96*se:.3f} -> searches/day {zero*(p-1.96*se):,.0f} to {zero*(p+1.96*se):,.0f}")
assert round(zero * (0.4 - 1.96 * sqrt(0.4 * 0.6 / 500))) == 21424
# effect of fixing a share of the spelling group
for fix in (0.5, 0.8):
    fixed = proj["spelling/synonym"] * fix
    print(f"fix {fix:.0%} of the spelling group -> {fixed:,.0f} searches now return results; zero-result rate {(zero-fixed)/searches:.2%}")
assert (zero - 12_000) / searches == 0.048 and (zero - 19_200) / searches == 0.0408
# a correction that helps nobody if it is wrong: precision matters. Toy vocabulary + difflib
vocab = ["running shoes", "wireless headphones", "phone charger", "yoga mat", "water bottle", "laptop stand"]
queries = ["runing shoes", "wireles headphones", "fone charger", "yoga mat", "kettlebell", "lap top stand", "trainers"]
for q in queries:
    m = difflib.get_close_matches(q, vocab, n=1, cutoff=0.8)
    print(f"{q!r:24} -> {m[0] if m else None}")
fixed = [q for q in queries if difflib.get_close_matches(q, vocab, n=1, cutoff=0.8)]
assert "runing shoes" in fixed and "fone charger" in fixed and "kettlebell" not in fixed and "trainers" not in fixed   # string similarity cannot fix a synonym or a missing product
# missing-product signal with a privacy threshold: count distinct users, publish only if >= k
rng = np.random.default_rng(40)
terms = ["kettlebell 16kg", "cast iron dutch oven", "left handed scissors", "rare vinyl X", "jane doe address"]
log = []
for t, cnt, users in (("kettlebell 16kg", 900, 600), ("cast iron dutch oven", 400, 250), ("left handed scissors", 120, 90), ("rare vinyl X", 15, 4), ("jane doe address", 6, 1)):
    uids = rng.integers(0, users, cnt)
    log += [(t, int(u)) for u in uids]
cnt = Counter(t for t, u in log); du = {t: len({u for tt, u in log if tt == t}) for t in cnt}
K = 20
pub = [t for t in cnt if du[t] >= K]
print({t: (cnt[t], du[t]) for t in cnt})
print("published to sellers (>= 20 distinct users):", pub)
assert "jane doe address" not in pub and "rare vinyl X" not in pub and len(pub) == 3
```

**Output (my run):**
```
zero-result searches/day 60000.0
{'spelling/synonym': 24000, 'genuinely missing': 12000, 'other': 24000} | other share 0.4
spelling/synonym: share 40% +- 0.043 -> searches/day 21,424 to 26,576
missing: share 20% +- 0.035 -> searches/day 9,896 to 14,104
fix 50% of the spelling group -> 12,000 searches now return results; zero-result rate 4.80%
fix 80% of the spelling group -> 19,200 searches now return results; zero-result rate 4.08%
'runing shoes'           -> running shoes
'wireles headphones'     -> wireless headphones
'fone charger'           -> phone charger
'yoga mat'               -> yoga mat
'kettlebell'             -> None
'lap top stand'          -> laptop stand
'trainers'               -> None
{'kettlebell 16kg': (900, 460), 'cast iron dutch oven': (400, 210), 'left handed scissors': (120, 71), 'rare vinyl X': (15, 4), 'jane doe address': (6, 1)}
published to sellers (>= 20 distinct users): ['kettlebell 16kg', 'cast iron dutch oven', 'left handed scissors']
```

**Follow-ups:**
- *Why not use a language model for every query?* It may help synonyms, but latency, cost and wrong corrections need an A/B test; start with logs and a dictionary.
- *How do you handle the 40% other?* Sample and classify them; filters and stock issues may need product changes rather than ML.
- *What if sellers game the demand report?* Use distinct users, a minimum history and a review step.

**Common mistakes:**
- Reporting shares from 500 searches as exact.
- Celebrating a lower zero-result rate without checking relevance.
- Publishing rare queries.
- Treating missing products and typos as the same problem.

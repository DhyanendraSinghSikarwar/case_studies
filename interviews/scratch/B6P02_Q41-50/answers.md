### Q41 ⭐ 🔴 A classifier had a validation true-positive rate of 80% and a false-positive rate of 10%. In production without labels it flags 29% of cases as positive, where at training the positive rate was 20%. Explain how you would estimate the production prior under a label-shift assumption using the confusion-matrix approach, state the estimate, and say how you would then adjust the threshold or the model.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
**Say this first (1 line):** If only the share of positives changed, the flag rate is a known mix of the true-positive and false-positive rates, so I solve 0.29 = pi x 0.80 + (1 - pi) x 0.10 and get pi = 0.19 / 0.70 = 27.1%, then I correct the threshold for that new prior.

**Clarifying questions:**
- Are the 80% TPR and 10% FPR measured on a validation set whose positive share is the 20% training prior? Why: TPR and FPR do not depend on the prior, but only if they were measured per class.
- Is the 29% a share of cases at the same threshold as validation? Why: a different cut gives a different TPR and FPR pair.
- What changed in the world (new channel, new region, a campaign)? Why: label shift assumes only the class mix moved. If the features of each class also moved, the formula is wrong.
- How many production cases is the 29% based on? Why: it sets the width of the interval around the estimate.
- Is the score calibrated? Why: it decides whether I move the threshold with the odds correction or have to recalibrate.
- Can I get a small random labelled sample now? Why: it is the only direct check of the estimate.

**Approach:**
1. Name the assumption: label shift, meaning P(y) moves and P(x | y) does not. Then the classifier's TPR and FPR stay at 0.80 and 0.10.
2. Write the flag rate as a mix: q = pi x TPR + (1 - pi) x FPR. Solve: pi = (q - FPR) / (TPR - FPR) = (0.29 - 0.10) / 0.70 = 0.271.
3. Sanity check: at the training prior 0.20 I would expect 0.20 x 0.80 + 0.80 x 0.10 = 24% flagged. I see 29%, so the extra 5 points of flags are the shift. The 20% in the prompt is the prior, not the training flag rate, so I do not compare 29% with 20%.
4. Put an interval on it. With 10,000 cases the flag rate has a standard error of 0.45 points, and dividing by TPR - FPR = 0.70 gives about 0.65 points on the prior.
5. Adjust the decisions. For a calibrated model, multiply the odds by w = (0.271 / 0.729) / (0.20 / 0.80) = 1.49. A 0.50 cut on the adjusted probability equals a 0.40 cut on the old probability.
6. Check the assumption: if I can get even a few hundred random labels, compare the estimate with the sample, and check feature drift within each predicted class.

**Metrics:**
- Estimated prior pi = (q - FPR) / (TPR - FPR); q = flagged cases / all scored cases.
- Precision at the new prior = pi x TPR / q. Recall stays at TPR under this assumption.
- Odds multiplier w = [pi / (1 - pi)] / [pi0 / (1 - pi0)].
- Guardrails: the formula needs TPR > FPR, the interval around pi, and a check that the estimate is between 0 and 1.

**Risks:**
- The formula assumes P(x | y) is unchanged. If the false-positive rate also drifted, the estimate is biased (see the code: FPR 0.14 would give 31%).
- A noisy TPR - FPR in the denominator magnifies noise when the classifier is weak.
- Treating 29% as the new prior by itself ignores the 20% FPR-driven flags.
- Moving the threshold on an uncalibrated score.

**What the interviewer scores:**
- Strong: writes the mixing equation and solves it by hand; states the label-shift assumption out loud.
- Strong: separates "estimate the prior" from "change the decision", and gives an interval.
- Strong: says what breaks the method and how to check it with a small random label sample.
- Weak: "the positive rate went from 20% to 29%", reading the flag rate as the prior.
- Weak: retrains first without asking whether the classes changed or only their mix.

**Example:** (illustrative numbers) TPR 0.80, FPR 0.10, flag rate 0.29. pi = 0.19 / 0.70 = 0.271. Precision was 0.20 x 0.80 / 0.24 = 66.7% at the old prior and is 0.271 x 0.80 / 0.29 = 74.9% now, so the model is not worse, the cases are more often positive. Weak answer: "29% are positive now." Strong answer: "About 27%, give or take a point; I would adjust the odds by 1.49 and verify on a small random labelled sample."

**Code:**
```python
# Q41: label-shift estimate (confusion-matrix / BBSE style). Illustrative numbers.
import numpy as np
tpr, fpr = 0.80, 0.10
flag_rate = 0.29          # production share flagged positive (no labels)
train_prior = 0.20

# flag_rate = pi*TPR + (1-pi)*FPR  ->  pi = (flag_rate - FPR) / (TPR - FPR)
pi = (flag_rate - fpr) / (tpr - fpr)
print(f"estimated production prior = {pi:.4f}")
assert abs(pi - 0.19/0.70) < 1e-12 and round(pi, 3) == 0.271

# naive reading would say 29% positive; flag rate at the training prior would have been:
exp_flag_train = train_prior*tpr + (1-train_prior)*fpr
print(f"expected flag rate at prior 0.20 = {exp_flag_train:.3f} (observed {flag_rate})")
assert abs(exp_flag_train - 0.24) < 1e-12

# precision before and after the shift (TPR, FPR assumed unchanged)
prec_old = train_prior*tpr/exp_flag_train
prec_new = pi*tpr/flag_rate
print(f"precision at prior 0.20 = {prec_old:.3f}, at prior {pi:.3f} = {prec_new:.3f}")
assert round(prec_old, 3) == 0.667 and round(prec_new, 3) == 0.749

# prior-odds correction for calibrated probabilities
w = (pi/(1-pi)) / (train_prior/(1-train_prior))
print(f"odds multiplier w = {w:.3f}")
assert round(w, 3) == 1.490
t_old = 0.5
# adjusted p' = p*w/(p*w+1-p); p' >= 0.5  <=>  p >= 1/(1+w)
t_equiv = 1/(1+w)
print(f"a 0.50 cut on adjusted probability = {t_equiv:.3f} on the old probability")
assert round(t_equiv, 3) == 0.402
p = t_equiv; assert abs(p*w/(p*w+1-p) - 0.5) < 1e-12

# uncertainty: n production cases, bootstrap of the flag rate
rng = np.random.default_rng(41)
n = 10_000
flags = rng.random(n) < flag_rate
boots = []
for _ in range(2000):
    fr = rng.choice(flags, n).mean()
    boots.append((fr - fpr)/(tpr - fpr))
lo, hi = np.percentile(boots, [2.5, 97.5])
print(f"n={n}: prior 95% interval ({lo:.3f}, {hi:.3f})")
se = np.sqrt(flag_rate*(1-flag_rate)/n)/(tpr-fpr)
print(f"analytic SE = {se:.4f}")
assert 0.0055 < se < 0.0075 and lo < 0.271 < hi

# check the method on simulated data where we know the truth (true prior 0.2714)
true_pi = 0.19/0.70
y = rng.random(200_000) < true_pi
pred = np.where(y, rng.random(y.size) < tpr, rng.random(y.size) < fpr)
est = (pred.mean() - fpr)/(tpr - fpr)
print(f"simulation: flag rate {pred.mean():.3f}, estimate {est:.3f}, truth {true_pi:.3f}")
assert abs(est - true_pi) < 0.01
# if the class-conditionals also moved, the estimate is wrong: FPR drifts to 0.14
pred2 = np.where(y, rng.random(y.size) < tpr, rng.random(y.size) < 0.14)
est2 = (pred2.mean() - fpr)/(tpr - fpr)
print(f"with FPR secretly 0.14 the same formula says {est2:.3f} (truth {true_pi:.3f})")
assert est2 > true_pi + 0.04
```

**Output (my run):**
```text
estimated production prior = 0.2714
expected flag rate at prior 0.20 = 0.240 (observed 0.29)
precision at prior 0.20 = 0.667, at prior 0.271 = 0.749
odds multiplier w = 1.490
a 0.50 cut on adjusted probability = 0.402 on the old probability
n=10000: prior 95% interval (0.262, 0.288)
analytic SE = 0.0065
simulation: flag rate 0.291, estimate 0.273, truth 0.271
with FPR secretly 0.14 the same formula says 0.312 (truth 0.271)
```

**Follow-ups:**
- What if the model is not calibrated? Recalibrate first on recent labels, or fit the new prior with an EM step on the scores; the odds multiplier is only right for calibrated probabilities.
- Why not retrain? Label shift changes the prior, not the relationship, so a threshold or odds correction is cheaper and reversible. See also Q9 in this part (precision fell because the fraud rate fell).

**Common mistakes:** Reading the flag rate as the prior. Forgetting that FPR flags are part of the 29%. No uncertainty on the estimate. Applying the method when the features themselves moved. Moving the cut on uncalibrated scores.

### Q42 ⭐ 🔴 A model's accuracy loses roughly 0.3 percentage points each week after training, each percentage point is worth about Rs 4 lakh per week, and a retrain costs Rs 6 lakh. Explain how you would model the cost of decay against the cost of retraining to choose a cadence, show the rough optimum, and name the assumptions (linear decay, constant stakes) that would break it.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** Add the cost of retraining to the cost of running an ageing model, divide by the cycle length, and pick the cadence that minimises cost per week; with these numbers that is about every 3 weeks, costing roughly Rs 3.8 lakh a week.

**Clarifying questions:**
- Does a retrain restore the fresh accuracy, or does it only catch part of the drop? Why: a partial reset shifts the optimum.
- Is the Rs 6 lakh all-in (compute, review, deployment, risk of a bad release)? Why: people time and incident risk are often left out.
- Is the 0.3 pp per week measured or assumed? Why: the whole answer rests on that slope.
- Is the Rs 4 lakh per point constant through the year? Why: festival weeks multiply the stakes.
- Can retraining be automated at low marginal cost? Why: cheap retraining shortens the optimal cycle.

**Approach:**
1. Loss rate: 0.3 pp per week x Rs 4 lakh per pp = Rs 1.2 lakh per week for each week of model age. Call it k.
2. In a cycle of T weeks, week j has average age j - 0.5, so decay cost = k x (0.5 + 1.5 + ... ) = k x T^2 / 2 = 0.6 T^2.
3. Cost per cycle = 6 + 0.6 T^2. Cost per week = 6 / T + 0.6 T.
4. Minimise: the two terms are equal when T = sqrt(6 / 0.6) = sqrt(10) = 3.16 weeks. Minimum cost = 2 x sqrt(6 x 0.6) = Rs 3.79 lakh per week.
5. Round to whole weeks: 3 weeks gives 3.80, 4 weeks gives 3.90, 2 weeks gives 4.20. The curve is flat near the minimum, so 3 to 4 weeks is fine; do not argue about decimals.
6. Turn it into a rule: retrain when the accumulated loss since the last retrain reaches the retrain cost, as a trigger, rather than by the calendar alone.

**Metrics:**
- Cost per week = (retrain cost + sum of decay losses in the cycle) / T.
- Decay loss in week j = k x (j - 0.5) with k = slope in pp per week x value per pp.
- Guardrails: accuracy floor, validation pass on each retrain, and the observed decay slope tracked monthly.

**Risks:**
- Decay is rarely linear: a shock (new product, outage) causes a step, so a monitored trigger beats a fixed cadence.
- Constant stakes: festival season makes k bigger; T* scales as 1 / sqrt(k), so doubling the stakes shortens the cycle by 1.41 times (to 2.2 weeks).
- Retrain cost is not flat: a 4x cost doubles the cycle (to 6.3 weeks).
- Each retrain has a risk of a worse model; that is a cost term I have left out of the Rs 6 lakh.
- The decay slope may be an artefact of label delay (see Q28 in this part).

**What the interviewer scores:**
- Strong: writes the cost per week and solves for T analytically, then rounds.
- Strong: states the assumptions and how each moves the answer (square-root rule).
- Strong: converts the optimum into a trigger.
- Weak: "retrain weekly to be safe" with no cost comparison.
- Weak: mixes up the cost per cycle and per week.

**Example:** (illustrative numbers) Retrain every 3 weeks: cost = (6 + 1.2 x (0.5 + 1.5 + 2.5)) / 3 = (6 + 5.4) / 3 = Rs 3.80 lakh per week. Every 4 weeks: (6 + 9.6) / 4 = 3.90. Every week: 6.60. Never retraining for 26 weeks averages Rs 15.6 lakh per week. Weak answer: "retrain as often as possible". Strong answer: "About every 3 to 4 weeks, and sooner if the measured decay speeds up."

**Code:**
```python
# Q42: retrain cadence from decay cost vs retrain cost. Illustrative numbers.
import numpy as np
decay_pp_per_week = 0.3
value_per_pp = 4.0      # Rs lakh per week per percentage point
retrain_cost = 6.0      # Rs lakh per retrain

k = decay_pp_per_week*value_per_pp          # loss rate grows 1.2 lakh/week each week
print(f"loss grows by Rs {k:.1f} lakh per week, per week of age")
assert abs(k - 1.2) < 1e-12

def avg_cost(T):
    # week j of a cycle is j-0.5 weeks old on average, loss = k*(j-0.5); sum_{j=1..T} = k*T^2/2
    weeks = np.arange(1, T+1)
    decay = (k*(weeks-0.5)).sum()
    assert abs(decay - k*T*T/2) < 1e-9
    return (retrain_cost + decay)/T

for T in range(1, 9):
    print(f"retrain every {T} wk: Rs {avg_cost(T):.2f} lakh/week")
best = min(range(1, 13), key=avg_cost)
T_star = (2*retrain_cost/k)**0.5
c_star = (2*retrain_cost*k)**0.5
print(f"continuous optimum T* = sqrt(2R/k) = {T_star:.2f} weeks, cost {c_star:.2f} lakh/week")
assert best == 3 and abs(T_star - 3.162) < 0.001 and abs(c_star - 3.795) < 0.001
assert round(avg_cost(3), 2) == 3.80 and round(avg_cost(4), 2) == 3.90 and round(avg_cost(2), 2) == 4.20

# never retraining: loss grows without bound; after 26 weeks
print(f"never retrain, week 26: loss that week Rs {k*25.5:.1f} lakh; average over 26 wk Rs {k*26/2:.1f} lakh/week")
assert abs(k*26/2 - 15.6) < 1e-9

# assumption breaks: decay is not linear, e.g. a step at week 5 after a shock
def cost_step(T, step_week=5, step_pp=2.0):
    w = np.arange(1, T+1)-0.5
    loss = k*w + np.where(w > step_week, step_pp*value_per_pp, 0.0)
    return (retrain_cost + loss.sum())/T
bestS = min(range(1, 13), key=cost_step)
print("with an extra 2 pp step after week 5, best cadence (whole weeks):", bestS,
      f"cost {cost_step(bestS):.2f}")
# stakes double (e.g. festival season): value_per_pp 8 -> T* shrinks by sqrt(2)
k2 = decay_pp_per_week*8.0
print(f"stakes double: T* = {(2*retrain_cost/k2)**0.5:.2f} weeks")
assert abs((2*retrain_cost/k2)**0.5 - T_star/2**0.5) < 1e-9
# cost rises 4x if retrain costs 24: T* doubles
print(f"retrain cost 4x: T* = {(2*24/k)**0.5:.2f} weeks")
assert abs((2*24/k)**0.5 - 2*T_star) < 1e-9
```

**Output (my run):**
```text
loss grows by Rs 1.2 lakh per week, per week of age
retrain every 1 wk: Rs 6.60 lakh/week
retrain every 2 wk: Rs 4.20 lakh/week
retrain every 3 wk: Rs 3.80 lakh/week
retrain every 4 wk: Rs 3.90 lakh/week
retrain every 5 wk: Rs 4.20 lakh/week
retrain every 6 wk: Rs 4.60 lakh/week
retrain every 7 wk: Rs 5.06 lakh/week
retrain every 8 wk: Rs 5.55 lakh/week
continuous optimum T* = sqrt(2R/k) = 3.16 weeks, cost 3.79 lakh/week
never retrain, week 26: loss that week Rs 30.6 lakh; average over 26 wk Rs 15.6 lakh/week
with an extra 2 pp step after week 5, best cadence (whole weeks): 3 cost 3.80
stakes double: T* = 2.24 weeks
retrain cost 4x: T* = 6.32 weeks
```

**Follow-ups:**
- What if decay is concave (fast at first, then slows)? The optimum moves later, because early weeks cost most; fit the real curve from backtests.
- How would you handle uncertainty in the slope? Take a range such as 0.2 to 0.4 pp; T* moves only by about the square root, so the cadence stays near 3 weeks.

**Common mistakes:** Forgetting the retrain cost is paid every cycle. Using end-of-cycle age instead of average age. Treating the optimum as exact. Ignoring step changes. Assuming a retrain always restores full accuracy.

### Q43 ⭐ 🔴 After a credit-scoring model was published and people learned what moves the score, applicants began gaming a few features and the score lost power. Explain this as performativity or Goodhart's law, how you would detect it, what features and monitoring are more robust, and how model transparency trades off against gaming risk.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** Once the score is used to decide things about people, people change the inputs to move the score, so the feature stops measuring what it measured (Goodhart's law); I detect it from shifts in the gameable features and a weaker link to outcomes, and I lean on features that are costly to fake.

**Clarifying questions:**
- Which features are public or easy to change, and at what cost to the applicant? Why: gameability is about cost, not visibility.
- Was the scoring logic or feature list published, or only inferred? Why: it decides how fast and how widely gaming spreads.
- Do we get outcome labels for the people who gamed? Why: without outcomes I can only see the inputs shift, not the loss of power.
- Is there a legal duty to give reasons for decisions? Why: transparency may be required, so I design around it instead of removing it.
- What does it cost the lender when the model is gamed (default loss) versus when it blocks good applicants? Why: it sets how defensive to be.

**Approach:**
1. Name it: the model is performative. Publishing it changes behaviour, so the data it later learns from is no longer the data it was built on. Goodhart: a measure that becomes a target stops being a good measure.
2. Detect from inputs: for each feature track its distribution, the share of values at "good-looking" edges, and the gap between a gameable feature and a hard-to-fake one for the same person (declared balance versus repayment history).
3. Detect from outcomes: the feature's correlation with default (or its coefficient) weakens as the cohort matures, while the score improves. A better score with worse realised defaults is the signature.
4. Respond: shift weight to features that are costly or slow to fake (verified repayment history, bureau data, cash-flow from bank statements), cap the influence of any single gameable feature, use monotone constraints and rate-of-change checks.
5. Keep a refresh rhythm and a holdout of unpublished signals, so a model that is attacked can be replaced quickly.
6. Transparency: explain reasons at the level the law needs, but not the weights; give actionable reasons that match real creditworthiness (improving them helps both sides), and use human review for edge cases.

**Metrics:**
- Per-feature PSI against the pre-publication distribution; share of applicants at a threshold edge.
- Feature-outcome link: correlation or AUC of that feature alone, by cohort month.
- Gap statistic: mean(gameable feature standardised - hard feature standardised).
- Guardrails: approval rate, default rate on matured loans, and complaint rate.

**Risks:**
- Defaults are labelled months later, so outcome evidence is slow; the input signals come first.
- Dropping a useful feature because a few people game it loses real signal.
- Hiding everything harms fairness and trust; publishing everything invites gaming.
- Tighter rules push applicants to new tricks; it is an ongoing contest.

**What the interviewer scores:**
- Strong: gives the mechanism (feedback from the score to the inputs) and both input-side and outcome-side detection.
- Strong: picks robust features by cost to fake and states the trade-off with transparency.
- Strong: notes label delay and says what to watch before labels arrive.
- Weak: "retrain on new data" (that trains on the gamed data).
- Weak: "make the model a secret", ignoring explanation duties.

**Example:** (illustrative simulation) The model's AUC for predicting default was 0.791 with two features. After 60% of applicants inflate the cheap feature, it falls to 0.705. A model on the hard-to-fake feature alone had 0.727 before and 0.730 after: weaker on day one, but it does not decay, and it wins once gaming is heavy enough. The cheap feature's mean moved from -0.01 to 1.49 and its link to default weakened (correlation -0.395 to -0.255). Weak answer: "retrain it." Strong answer: "Watch the gameable inputs and their link to outcomes, and move weight to costly-to-fake signals."

**Code:**
```python
# Q43: gaming of a published scorecard. Illustrative simulation.
import numpy as np
from scipy.optimize import minimize
from scipy.stats import rankdata
rng = np.random.default_rng(43)
n = 40_000
risk = rng.normal(size=n)                       # latent creditworthiness
default = rng.random(n) < 1/(1+np.exp(2.0 + 1.5*risk))   # higher risk value -> fewer defaults
# features: x_hard is costly to fake (repayment history), x_easy is cheap to fake (declared balance)
x_hard = risk + rng.normal(0, 1.0, n)
x_easy = risk + rng.normal(0, 0.5, n)
def feats(xh, xe): return np.column_stack([np.ones(len(xh)), xh, xe])

def fit(X, y):
    def nll(b):
        z = X@b
        return np.mean(np.logaddexp(0, z) - y*z)
    return minimize(nll, np.zeros(X.shape[1]), method="BFGS").x
def auc(score, y):   # AUC for predicting y=1
    r = rankdata(score); n1 = y.sum(); n0 = len(y)-n1
    return (r[y == 1].sum() - n1*(n1+1)/2)/(n1*n0)

b_full = fit(feats(x_hard, x_easy), default.astype(float))
b_hard = fit(feats(x_hard, np.zeros(n))[:, :2], default.astype(float))
print("weights full model (const, hard, easy):", np.round(b_full, 2))

# after publication: 60% of applicants inflate the easy feature (the model reads them as safer)
m = 40_000
risk2 = rng.normal(size=m)
d2 = rng.random(m) < 1/(1+np.exp(2.0 + 1.5*risk2))
xh2 = risk2 + rng.normal(0, 1.0, m)
xe2 = risk2 + rng.normal(0, 0.5, m)
gamers = rng.random(m) < 0.6
xe2_g = xe2 + gamers*rng.uniform(1.5, 3.5, m)    # inflation unrelated to true risk
before = auc(feats(x_hard, x_easy)@b_full, default.astype(int))
after = auc(feats(xh2, xe2_g)@b_full, d2.astype(int))
hard_only_after = auc(feats(xh2, xe2_g)[:, :2]@b_hard[:2], d2.astype(int))
hard_only_before = auc(feats(x_hard, x_easy)[:, :2]@b_hard[:2], default.astype(int))
print(f"full model AUC before {before:.3f} after gaming {after:.3f}")
print(f"hard-feature-only model AUC before {hard_only_before:.3f} after {hard_only_after:.3f}")
assert after < before - 0.03
assert hard_only_before < before        # robustness costs some power today
assert abs(hard_only_after - hard_only_before) < 0.01   # but it does not decay
assert hard_only_after > after            # and wins once gaming starts

# detection: the easy feature's distribution moves and its link to the outcome weakens
print(f"mean easy feature before {x_easy.mean():.2f}, after {xe2_g.mean():.2f}")
corr_b = np.corrcoef(x_easy, default)[0, 1]; corr_a = np.corrcoef(xe2_g, d2)[0, 1]
print(f"corr(easy, default) before {corr_b:.3f}, after {corr_a:.3f}")
assert xe2_g.mean() > x_easy.mean() + 0.5 and abs(corr_a) < abs(corr_b)
# gap between easy and hard features: gamers show easy >> hard
gap_b = (x_easy - x_hard).mean(); gap_a = (xe2_g - xh2).mean()
print(f"mean(easy - hard) before {gap_b:.2f}, after {gap_a:.2f}")
assert gap_a > gap_b + 0.5
```

**Output (my run):**
```text
weights full model (const, hard, easy): [-1.87 -0.24 -0.92]
full model AUC before 0.791 after gaming 0.705
hard-feature-only model AUC before 0.727 after 0.730
mean easy feature before -0.01, after 1.49
corr(easy, default) before -0.395, after -0.255
mean(easy - hard) before -0.00, after 1.49
```

**Follow-ups:**
- Is all gaming bad? No. If changing the feature really reduces risk (paying bills on time), gaming it helps. The problem is features that can be changed without changing risk.
- Related question in this part: Q38 (selection bias in monitoring labels) matters here too, since rejected applicants have no outcomes.

**Common mistakes:** Retraining directly on gamed data. Treating a better score as better performance. Assuming secrecy fixes it. Dropping every visible feature. Forgetting that outcomes arrive late.

### Q44 ⭐ 🔴 A shared embedding model was upgraded by the platform team, and three downstream models that consume its vectors each lost between 2 and 6 points of accuracy without any code change of their own. Explain the dependency chain problem, how you would detect it, and what versioning, contracts and canary practices the platform team should adopt.
**Asked at:** Upstream schema and silent feature-pipeline failure write-ups (Towards AI schema-migration post, RisingWave feature-pipeline observability, ActiveWizards Kafka schema-evolution post, dataexpert.io schema-drift post); practitioner posts rather than interview banks, so scenario is editor-designed; search snippets only, not opened
**Say this first (1 line):** The three models depend on the exact coordinate system of the old embedding, so a new embedding model silently changes what every input number means; I would detect it with a per-consumer regression check on a frozen set, and ask the platform team for versioned embeddings, contracts and a staged rollout.

**Clarifying questions:**
- Did the platform team replace vectors in place, or serve both versions? Why: in-place means every consumer changed on the same day.
- Did the dimension, normalisation or tokenisation change? Why: a shape change fails loudly, while a same-shape change fails silently.
- Are the three models fine-tuned on the old vectors, or do they use them as frozen inputs? Why: it decides whether a quick fix (alignment) or a retrain is needed.
- Who owns the frozen evaluation sets? Why: without consumer-owned tests, nobody sees the loss.
- Can I get a paired sample of the same items in both spaces? Why: pairs allow a cheap alignment fix.

**Approach:**
1. Frame the dependency chain: platform embedding -> feature store -> three models -> products. The platform team tested the embedding on its own benchmark and called it better. Consumers were never in that test.
2. Confirm the cause: re-score a frozen validation set using the old vectors and the new vectors, with the same model. If accuracy drops only with the new vectors, the embedding is the cause. Check the vector statistics too (norm, mean, cosine to the old vector for the same item).
3. Contain: pin the old embedding version for the three consumers (roll back the dependency, not the consumer code).
4. Repair: retrain each consumer on the new vectors, or learn a small alignment map from paired items (orthogonal Procrustes) as a bridge while retraining.
5. Prevent it: versioned embeddings with a version tag stored with every vector, side-by-side serving for a deprecation window, a compatibility contract (dimension, normalisation, a published cosine-similarity-to-previous report), and a canary with per-consumer gates.
6. Process: consumers register a frozen test with the platform team; an upgrade can only be promoted if every registered consumer stays within an agreed tolerance, for example 1 point.

**Metrics:**
- Per-consumer accuracy delta on a frozen set = accuracy(new vectors) - accuracy(old vectors).
- Mean cosine similarity between old and new vectors for the same items.
- Gate: block promotion if any consumer's delta is below -1 point.
- Guardrail: share of traffic on each embedding version.

**Risks:**
- Averaging across consumers hides one badly hit model.
- The old space may not be reproducible later if the old model is deleted; keep it.
- An alignment map only works if the new space is roughly a linear transformation of the old one.
- Mixing versions in one index is a separate failure (see Q23 in this part).

**What the interviewer scores:**
- Strong: describes this as an interface change with no interface contract.
- Strong: re-scores with old versus new vectors to isolate the cause.
- Strong: proposes consumer-owned tests, version tags and staged rollout, not "be careful".
- Weak: debugging each downstream model separately.
- Weak: blames the platform team without a process fix.

**Example:** (illustrative simulation) A consumer scores 85.6% accuracy on the old vectors. If the new space is a rotation of the old one by 0.4 (arbitrary units), the unchanged consumer scores 84.7%; at 0.8 it scores 81.7%; at 1.2 it scores 79.0%; a full re-spacing gives 67.2%. After a Procrustes alignment from 500 paired items, accuracy returns to 85.6%. This is a pure rotation, so the recovery is easy; real upgrades are not pure rotations, so alignment is a bridge only. A 1-point gate blocks the 1.2 case (drop 6.6 points) and passes the 0.4 case (drop 0.9). Weak answer: "each team should retrain." Strong answer: "Version the embedding, test each consumer before promotion, and pin until they have moved."

**Code:**
```python
# Q44: upstream embedding upgrade breaks consumers. Illustrative simulation.
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(44)
d, n = 16, 6000
Z = rng.normal(size=(n, d))                      # "true" semantic factors
w_true = rng.normal(size=d)
y = (Z@w_true + rng.normal(0, 1.0, n) > 0).astype(float)
E_old = Z + rng.normal(0, 0.3, (n, d))           # v1 embedding

from scipy.linalg import expm
def new_space(E, theta, rng):
    # v2 = v1 rotated by a random rotation of size theta (a different, equally good space)
    A = rng.normal(size=(d, d)); A = A - A.T
    A = A/np.linalg.norm(A, 2)
    return E@expm(theta*A)

def fit(X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    f = lambda b: np.mean(np.logaddexp(0, X1@b) - y*(X1@b))
    return minimize(f, np.zeros(X1.shape[1]), method="L-BFGS-B").x
def acc(b, X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    return np.mean(((X1@b) > 0) == (y == 1))

tr, te = slice(0, 4000), slice(4000, n)
b = fit(E_old[tr], y[tr])
a0 = acc(b, E_old[te], y[te])
print(f"consumer on v1 vectors: accuracy {a0:.3f}")
res = {}
for frac in (0.4, 0.8, 1.2, 3.0):
    E_new = new_space(E_old, frac, np.random.default_rng(7))
    res[frac] = acc(b, E_new[te], y[te])
    print(f"v2 = {frac} rotation, old consumer unchanged: accuracy {res[frac]:.3f}")
assert res[0.4] > res[0.8] > res[1.2] > res[3.0]      # the bigger the change, the bigger the loss
assert a0 - res[3.0] > 0.15                   # full re-spacing is near-chance
# alignment on a small paired sample (orthogonal Procrustes) recovers most of it, without retraining
E_new = new_space(E_old, 3.0, np.random.default_rng(7))
idx = slice(0, 500)
U, _, Vt = np.linalg.svd(E_new[idx].T@E_old[idx]); R = U@Vt          # maps new -> old
acc_aligned = acc(b, (E_new@R)[te], y[te])
print(f"after Procrustes alignment from 500 paired items: accuracy {acc_aligned:.3f}")
assert a0 - acc_aligned < 0.01
# canary gate: per-consumer accuracy drop vs frozen eval set, block above 1 point
gate = 0.01
for frac in (0.4, 1.2):
    E_new = new_space(E_old, frac, np.random.default_rng(7))
    drop = a0 - acc(b, E_new[te], y[te])
    print(f"gate at {gate:.0%}: rotation {frac} -> drop {drop:.3f} -> {'BLOCK' if drop > gate else 'pass'}")
```

**Output (my run):**
```text
consumer on v1 vectors: accuracy 0.856
v2 = 0.4 rotation, old consumer unchanged: accuracy 0.847
v2 = 0.8 rotation, old consumer unchanged: accuracy 0.817
v2 = 1.2 rotation, old consumer unchanged: accuracy 0.790
v2 = 3.0 rotation, old consumer unchanged: accuracy 0.672
after Procrustes alignment from 500 paired items: accuracy 0.856
gate at 1%: rotation 0.4 -> drop 0.009 -> pass
gate at 1%: rotation 1.2 -> drop 0.066 -> BLOCK
```

**Follow-ups:**
- Why not freeze embeddings forever? You can lose real quality gains; the point is controlled migration with dual serving.
- What would you put in the contract? Dimension, normalisation, version id, a changelog with similarity-to-previous, deprecation date and a named consumer list.

**Common mistakes:** Replacing vectors in place. Testing only the platform's own benchmark. No version tag on stored vectors. Rolling back consumer code that did not change. Assuming a same-shape upgrade is compatible.

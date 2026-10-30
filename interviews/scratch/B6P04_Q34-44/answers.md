### Q34 ⭐⭐ 🟡 A growth team wants a bandit rather than an A/B test to choose among 6 email subject lines for 600,000 recipients over 2 weeks, and then wants to claim a causal lift for next quarter's plan. Explain when a bandit is right, what you lose for inference and what you recommend.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
**Say this first (1 line):** A bandit is right when the goal is to earn opens during the campaign, not to learn a clean number, and here the team wants both, so I would run a bandit for the send and keep a small fixed-allocation slice (and a no-email holdout) for the causal claim.

**Clarifying questions:**
- What is the goal: maximise opens this fortnight, or learn which line to reuse next quarter? Why: the first is a bandit problem, the second is an estimation problem, and they pull in opposite directions.
- What does "causal lift" mean: line against line, or email against no email? Why: randomized lines answer the first, only a holdout answers the second.
- Can the result be read within the fortnight, or is the open delayed? Why: a bandit needs fast feedback to update; opens mostly arrive in the first day or two, which suits batches.
- Does the best line change by day or segment (a sale day, a weekday)? Why: a bandit chases a moving target and an estimate of "the" lift would not be stable.
- Is open rate the real goal, or purchases from the email? Why: opens can be inflated by privacy-proxy pre-fetching, so I would pick the outcome before the test.

**Approach:**
1. Decide the purpose. Pure "send the best line to as many people as possible, now": bandit. "Tell next quarter's plan how much this lifts revenue": A/B plus holdout.
2. If a bandit: send in daily batches (14 here), allocate each batch by Thompson sampling (draw a plausible rate for each line from its Beta posterior, send more to the line that wins most draws), and keep a floor (say 5% each) so no line is starved.
3. Log the allocation probability for every send. Randomization is still real, but the probabilities change by batch, so analyse with batch-stratified or inverse-probability weights, not a plain pooled rate.
4. Reserve a fixed slice (for example 10% of recipients, split equally over the 6 lines) that is never touched by the bandit. This slice gives clean estimates of every line.
5. Reserve a holdout that gets no email (or last quarter's default line). Only this answers "lift against what we would have done anyway".
6. Report the effect as an interval from the fixed slice, and the opens earned by the bandit as a separate, descriptive number.

**Metrics:**
- Primary for the bandit: open rate = opens / delivered emails (or click rate; pick one before the test).
- Regret = opens if every send had used the best line - opens actually earned.
- Estimate quality: width of the 95% interval for each line's rate and for line-minus-line gaps.
- Guardrails: unsubscribe rate = unsubscribes / delivered, spam-complaint rate, and revenue per recipient, per line.

**Risks:**
- Naive pooled rates from a bandit are biased: a line with an unlucky start gets fewer sends and its estimate stays noisy and low.
- Weak lines get little data, so "line 1 versus line 2" is poorly measured.
- Opens are a proxy; the best-opening line may sell less (a clickbait line raises unsubscribes).
- Taking the best-looking line's rate as next quarter's lift mixes in luck (winner's curse) and changes in audience and season.

**What the interviewer scores:**
- Strong: separates "earn while learning" from "learn", and says what each design gives up.
- Strong: names the bias and the need for allocation probabilities or a fixed slice for inference.
- Strong: asks "lift against what" and brings in a holdout.
- Weak: "bandits are always better because they waste fewer sends."
- Weak: reads the final pooled rate of the winner as the causal lift.

**Example:** (illustrative numbers) Six lines with true open rates 10.0% to 12.0% in 0.4-point steps, 600,000 recipients. Fixed A/B sends 100,000 to each line; the standard error of a gap between two lines is about 0.14 points. Thompson sampling in 14 daily batches earns about 5,300 more opens (8%) than the fixed split and sends only about 7,200 emails to the worst line. Its error on the gap between the two weakest lines is about four times larger. Weak answer: "use a bandit, it wastes fewer sends, and tell finance the winner's rate is the lift." Strong answer: "bandit for the send, a fixed slice and a no-email holdout for the number we plan on."

**Code:**
```python
# Q34: bandit vs fixed A/B for 6 subject lines. Illustrative numbers, seeded.
import numpy as np

N, K, BATCHES = 600_000, 6, 14
rates = np.array([0.100, 0.104, 0.108, 0.112, 0.116, 0.120])   # invented true open rates
assert N // K == 100_000
se_pair = np.sqrt(2 * 0.11 * 0.89 / 100_000)
print(f"fixed A/B: 100,000 per line, SE of a difference ~ {se_pair*100:.2f} points")
assert abs(se_pair - 0.00140) < 1e-4

def run_fixed(rng):
    n = np.full(K, N // K)
    s = rng.binomial(n, rates)
    return n, s

def run_ts(rng):
    n = np.zeros(K); s = np.zeros(K)
    per = N // BATCHES
    for b in range(BATCHES):
        if b == 0:
            share = np.full(K, 1 / K)
        else:
            draws = rng.beta(1 + s, 1 + n - s, size=(2000, K))
            share = np.bincount(draws.argmax(1), minlength=K) / 2000
        send = rng.multinomial(per, share)
        s += rng.binomial(send, rates); n += send
    return n, s

R = 300
rng = np.random.default_rng(34)
res = {}
for name, f in [("fixed", run_fixed), ("thompson", run_ts)]:
    clicks, best, diff_err, win_bias, worst_n = [], [], [], [], []
    for _ in range(R):
        n, s = f(rng)
        clicks.append(s.sum()); est = s / np.maximum(n, 1)
        w = est.argmax(); best.append(w == K - 1)
        win_bias.append(est[w] - rates[w])
        # error on the gap between the two lines with the lowest rates (smallest sample under a bandit)
        diff_err.append(abs((est[1] - est[0]) - (rates[1] - rates[0])))
        worst_n.append(n[0])
    res[name] = dict(clicks=np.mean(clicks), best=np.mean(best), bias=np.mean(win_bias),
                     gap_err=np.mean(diff_err), n_worst=np.mean(worst_n))
    r = res[name]
    print(f"{name:9s} opens={r['clicks']:9.0f} picked_true_best={r['best']:.0%} "
          f"bias_of_winner_estimate={r['bias']*100:+.3f} pts  abs_err_on_gap(line1-line0)={r['gap_err']*100:.3f} pts  sends_to_worst_line={r['n_worst']:.0f}")

best_possible = N * rates.max()
print("opens if every send used the best line:", int(best_possible))
assert res["thompson"]["clicks"] > res["fixed"]["clicks"]
assert res["thompson"]["n_worst"] < 0.5 * res["fixed"]["n_worst"]
assert res["thompson"]["gap_err"] > res["fixed"]["gap_err"]
extra = res["thompson"]["clicks"] - res["fixed"]["clicks"]
print(f"extra opens from the bandit: {extra:.0f} ({extra/res['fixed']['clicks']:.1%})")
```

**Output (my run):**
```text
fixed A/B: 100,000 per line, SE of a difference ~ 0.14 points
fixed     opens=    65992 picked_true_best=100% bias_of_winner_estimate=-0.007 pts  abs_err_on_gap(line1-line0)=0.103 pts  sends_to_worst_line=100000
thompson  opens=    71333 picked_true_best=100% bias_of_winner_estimate=-0.001 pts  abs_err_on_gap(line1-line0)=0.425 pts  sends_to_worst_line=7196
opens if every send used the best line: 72000
extra opens from the bandit: 5341 (8.1%)
```
The bandit picks the best line every time in this easy case (a 2-point spread over 600,000 sends), so the cost shows up as precision on the weak lines, not as a wrong winner. With closer lines or a shifting best line it can also pick wrongly.

**Follow-ups:**
- Why not just estimate lift from the bandit's data? You can, with batch or inverse-probability weights, but the weak lines stay poorly measured and an adaptive design changes the usual p-value rules. A fixed slice is simpler. See Book 1 Part 10 Q41 (multi-armed bandit).
- Could a contextual bandit help? Yes if the best line differs by segment, but then the estimate is per segment and needs even more data.

**Common mistakes:** Calling the bandit's pooled rate a causal lift. Forgetting there is no no-email control. Letting the bandit starve a line completely. Judging on opens when the business outcome is purchases. Using one number for next quarter without noting season and audience change.

### Q35 ⭐⭐ 🟡 A search ranking change raises click-through per query by 5% relative to control but raises queries per session by 8% (users reformulating) and leaves purchases per session flat. Explain how you interpret these conflicting metrics and what additional metric or cut you would build before deciding.
**Asked at:** Guardrail and ship-decision material (a Dataford 'primary vs guardrail metrics' page, a Spotify Confidence guardrail-metric glossary and blog post, PracHub analytics-and-experimentation question pages, a Dataford 'non significant test PM wants launch' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** CTR per query rose because the number of queries (the denominator) rose for the wrong reason, so I do not read it as a win; I decide on a per-session outcome (purchases or successful sessions) and build a "queries to success" view.

**Clarifying questions:**
- Is "reformulating" confirmed from logs (a second query within seconds, with an edited string) or is it a guess? Why: the whole story depends on whether extra queries are retries or genuine new intent.
- What is the business goal of search: purchases, revenue, or satisfaction? Why: it picks the primary metric.
- How wide is the interval on purchases per session? Why: "flat" can hide a real effect of a few percent either way.
- Does the change alter which results sit at the top (a ranking change) or only the snippets? Why: it tells me whether more clicks could mean better results or just more attempts.
- Are there human-rated relevance scores or a satisfaction survey I can add? Why: they separate "found it faster" from "needed more tries".

**Approach:**
1. Do the arithmetic. Clicks per session = CTR per query x queries per session = 1.05 x 1.08 = 1.134, so clicks per session are up about 13%, while purchases per session are flat. More clicks, same purchases.
2. Name the trap. CTR per query is a ratio. If users have to ask more times, the denominator grows. A higher CTR per query alongside more queries per session is the signature of retries, not of better results.
3. Pick the unit of decision: the session (or the user), because a purchase journey spans queries. Primary metric: purchases (or successful sessions) per session.
4. Build the missing metrics: reformulation rate, queries until first click or purchase, share of sessions with 3+ queries, abandonment (no click) rate, and time to first click.
5. Cut by query type (navigational, specific product, broad) and by new versus returning users. A ranking change may help broad queries and hurt specific ones.
6. Get an independent quality signal: a human-rated relevance sample, or a short "did you find it?" prompt.
7. Decide. If purchases per session are flat with a tight interval, queries per purchase go up and satisfaction is not better, then do not ship on CTR; consider iterating on the ranking.

**Metrics:**
- Primary: purchases per session = purchase count / sessions (or successful-session rate = sessions with a purchase or a long click / sessions).
- Diagnostic: reformulation rate = queries that follow another query within a short window with an edited string / all queries; queries per purchase = queries / purchases.
- Guardrails: zero-result rate, abandonment rate, latency, revenue per session.
- Ratio metrics get a delta-method or user-level interval; do not use the plain binomial formula on queries.

**Risks:**
- Optimising CTR per query rewards making the first result less satisfying (more retries, more clicks).
- A flat purchase result may still hide a few-percent change: the interval is the evidence, not the word "flat".
- Retries can be a good sign in discovery search (users exploring). Query type matters.
- Position and presentation changes alter clicks without changing relevance.

**What the interviewer scores:**
- Strong: multiplies the metrics (1.05 x 1.08 = 1.134) and spots the changing denominator.
- Strong: chooses a session or user outcome, then adds "queries to success" and a relevance check.
- Strong: asks for the interval on the flat metric.
- Weak: "CTR is up, queries are up, ship it" or "queries are up so it is bad" without checking the data.
- Weak: treats all three metrics as equally important.

**Example:** (illustrative numbers) Control: 2.00 queries per session, CTR 30.0% per query, 5.0% of sessions buy. Treatment: 2.16 queries, CTR 31.5%, 5.0% buy. In the code, clicks per session go from 0.60 to 0.68 (+13%), purchases per session differ by +0.08 points with an interval of -1.0% to +4.4% relative, queries per purchase go from 40.8 to 43.2, and the share of sessions with 3 or more queries goes from 26% to 32%. Weak answer: "CTR rose 5%, so ranking is better." Strong answer: "CTR per query rose because queries rose; purchases per session are flat, so I would not call it a win until queries-to-success and relevance agree."

**Code:**
```python
# Q35: CTR/query +5%, queries/session +8%, purchases/session flat. Illustrative, seeded.
import numpy as np
from scipy import stats

print("clicks per session ratio =", round(1.05 * 1.08, 3))
assert round(1.05 * 1.08, 3) == 1.134      # +13.4% clicks per session implied

rng = np.random.default_rng(35)
S = 200_000                                  # sessions per arm
def arm(q_mean, ctr, p_buy):
    q = rng.poisson(q_mean - 1, S) + 1       # queries per session (>=1)
    clicks = rng.binomial(q, ctr)
    buy = rng.random(S) < p_buy              # purchase does not depend on arm by construction
    first_click = (clicks > 0)
    return q, clicks, buy, first_click
qc, cc, bc, fc = arm(2.00, 0.300, 0.050)
qt, ct, bt, ft = arm(2.16, 0.315, 0.050)

print(f"queries/session  C {qc.mean():.3f}  T {qt.mean():.3f}  ({qt.mean()/qc.mean()-1:+.1%})")
ctr_c, ctr_t = cc.sum()/qc.sum(), ct.sum()/qt.sum()
print(f"CTR per query    C {ctr_c:.4f}  T {ctr_t:.4f}  ({ctr_t/ctr_c-1:+.1%})")
print(f"clicks/session   C {cc.mean():.3f}  T {ct.mean():.3f}  ({ct.mean()/cc.mean()-1:+.1%})")
assert abs(qt.mean()/qc.mean() - 1.08) < 0.01 and abs(ctr_t/ctr_c - 1.05) < 0.02

d = bt.mean() - bc.mean()
se = np.sqrt(bt.var()/S + bc.var()/S)
lo, hi = d - 1.96*se, d + 1.96*se
print(f"purchases/session diff {d*100:+.2f} pts, 95% CI [{lo*100:+.2f}, {hi*100:+.2f}] pts  = [{lo/0.05:+.1%}, {hi/0.05:+.1%}] relative")
assert lo < 0 < hi                           # flat: cannot reject zero
print(f"width of CI: +/-{1.96*se/0.05:.1%} relative -> a flat result rules out only effects bigger than that")
# extra cut: queries needed per purchase, and share of sessions with 3+ queries
print(f"queries per purchase  C {qc.sum()/bc.sum():.1f}  T {qt.sum()/bt.sum():.1f}")
print(f"sessions with 3+ queries  C {np.mean(qc>=3):.1%}  T {np.mean(qt>=3):.1%}")
assert np.mean(qt >= 3) > np.mean(qc >= 3)
```

**Output (my run):**
```text
clicks per session ratio = 1.134
queries/session  C 2.000  T 2.155  (+7.7%)
CTR per query    C 0.2999  T 0.3149  (+5.0%)
clicks/session   C 0.600  T 0.679  (+13.1%)
purchases/session diff +0.08 pts, 95% CI [-0.05, +0.22] pts  = [-1.0%, +4.4%] relative
width of CI: +/-2.7% relative -> a flat result rules out only effects bigger than that
queries per purchase  C 40.8  T 43.2
sessions with 3+ queries  C 26.4%  T 32.1%
```
In this simulation the purchase probability is identical by construction, so the "flat" is built in. The simulation shows the arithmetic and the interval width, not what real users do.

**Follow-ups:**
- What if purchases per session were up 1% but not significant? Report the interval, say the effect is small and unproven, and decide on cost and risk. See the Part 4 question on a flat result (Q5) in this part for how to read a CI that includes both zero and a useful effect.
- Why per session and not per query? A purchase belongs to a journey, and retries are part of the journey. See Book 1 Part 10 Q27 (ratio metrics, per-session versus per-user).

**Common mistakes:** Reading CTR per query as quality. Ignoring that the denominator moved. Calling "flat" "no effect". Using a binomial interval on queries from the same user. Judging a ranking change without a query-type cut.

### Q36 ⭐⭐ 🟡 A support assistant with a new model raises the share of conversations resolved without a human from 60% to 63% (3 points absolute, 5% relative to control) in a user-level test, but the same user can get different answers to the same question on a retry. Explain how nondeterminism affects the design, which unit you randomize and what you measure besides resolution.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
**Say this first (1 line):** Randomize by user, because the same user retrying must stay on one model, then analyse at user level (or with user-clustered errors), since conversations from one user are not independent and the same prompt can give different answers.

**Clarifying questions:**
- How is "resolved without a human" defined: user did not ask for an agent, did not contact again within 7 days, or confirmed by the user? Why: a reply that ends the chat is not the same as a solved problem.
- How many conversations does one user have in the test window? Why: it sets the design effect and the sample size.
- Can the model be made less random (temperature, fixed seed) and is it? Why: it tells me whether the noise is in the design or in the product.
- Do users share accounts or devices (a household, a company seat)? Why: it may need account-level randomization.
- What does a bad answer cost (refund, wrong advice, a complaint)? Why: it sets the guardrails.

**Approach:**
1. Arithmetic first: 60% to 63% is +3 percentage points, +5% relative to control. Say both.
2. Choose the unit. Randomize by user (or account): the same person must not see model A on Monday and model B on retry, or the arms contaminate each other and trust drops. Per-conversation randomization is wrong for this reason.
3. Accept that the model is random. Two things vary: between users (some users have easier problems) and within a user (the same question can resolve or not). Neither makes the test invalid; it makes the variance larger than a coin-flip formula says.
4. Analyse with the user as the unit: mean resolution per user, compare users. Or use conversation data with user-clustered standard errors. Do not treat every conversation as independent.
5. Size the test on users: independent-conversation sample size is about 4,100 per arm for this lift; with 4 conversations per user and intra-user correlation 0.2 the design effect is 1 + 3 x 0.2 = 1.6, so plan for roughly 1.6 times as many conversations, or count users accordingly.
6. Measure more than resolution (below), and sample conversations for human review of correctness.

**Metrics:**
- Primary: resolution rate per user = conversations resolved without a human / conversations, averaged over users (or total resolved / total conversations with user-clustered SE).
- Quality: human-audited correctness on a random sample (not on resolved ones only), hallucination or policy-violation rate.
- Guardrails: re-contact within 7 days of a "resolved" conversation, escalation rate, CSAT, latency (p95), cost per conversation.
- Stability: share of repeated identical questions with a different outcome.

**Risks:**
- "Resolved" can rise because users give up (they stop asking). The re-contact metric catches this.
- Treating conversations as independent gives intervals that are too narrow and p-values that are too small.
- A user who retries may be the unhappy case; excluding retries hides the problem.
- Model changes or provider updates in the middle of the test change the treatment.

**What the interviewer scores:**
- Strong: user-level randomization with a reason, and clustered or user-level analysis.
- Strong: separates between-user and within-user randomness and does the design-effect arithmetic.
- Strong: adds a quality and a re-contact metric instead of resolution alone.
- Weak: "LLM is non-deterministic so A/B tests do not work."
- Weak: randomizes per conversation or per message.

**Example:** (illustrative numbers) 3,000 users per arm, 4 conversations each, true resolution 60% versus 63%, intra-user correlation 0.2. In the simulated run the observed gap is 2.7 points; the naive standard error (all 12,000 conversations independent) is 0.63 points, the user-level one is 0.80 points, and the implied design effect is about 1.6. So the naive z of 4.4 falls to 3.5. Weak answer: "12,000 conversations per arm, so the 3 points are certain." Strong answer: "users are the unit; 3,000 users is the real sample size, and I check re-contact before believing resolution."

**Code:**
```python
# Q36: LLM support assistant, 60% -> 63% resolved. Nondeterminism, unit, clustering. Illustrative, seeded.
import numpy as np
from scipy import stats

p0, p1 = 0.60, 0.63
print(f"absolute {100*(p1-p0):.0f} points, relative {(p1/p0-1):.0%}")
assert round(p1 - p0, 2) == 0.03 and round(p1 / p0 - 1, 2) == 0.05

# sample size per arm if every conversation were independent (two-sided 5%, 80% power)
za, zb = stats.norm.ppf(0.975), stats.norm.ppf(0.80)
pbar = (p0 + p1) / 2
n_ind = 2 * pbar * (1 - pbar) * (za + zb) ** 2 / (p1 - p0) ** 2
print(f"independent conversations needed per arm: {n_ind:,.0f}")
assert 4000 < n_ind < 4400

# users have a personal resolve-propensity, and the same user retries: conversations in a user are correlated
rng = np.random.default_rng(36)
U, M = 3000, 4                      # users per arm, conversations per user
def arm(p, icc=0.2):
    a = p * (1 - icc) / icc; b = (1 - p) * (1 - icc) / icc       # Beta with intra-user correlation icc
    pu = rng.beta(a, b, U)
    y = rng.binomial(1, pu[:, None], (U, M))
    return y
yc, yt = arm(p0), arm(p1)
rc, rt = yc.mean(), yt.mean()
# naive: treat all U*M conversations as independent
se_naive = np.sqrt(rc*(1-rc)/(U*M) + rt*(1-rt)/(U*M))
# user-level: mean per user, compare users
uc, ut = yc.mean(1), yt.mean(1)
se_user = np.sqrt(uc.var(ddof=1)/U + ut.var(ddof=1)/U)
d = rt - rc
deff = (se_user / se_naive) ** 2
print(f"observed diff {d*100:+.2f} pts; naive SE {se_naive*100:.2f} pts; user-level SE {se_user*100:.2f} pts; design effect ~ {deff:.2f}")
print(f"naive z = {d/se_naive:.2f}   user-level z = {d/se_user:.2f}")
assert se_user > 1.2 * se_naive          # clustering widens the interval
rho = (deff - 1) / (M - 1)
print(f"implied intra-user correlation {rho:.2f} (built in: 0.20)")
assert 0.1 < rho < 0.3

# how much of the "same user, different answer" noise exists: same question, 5 retries, answer is right with prob q
q = 0.63
agree = q**2 + (1-q)**2
print(f"if retries were independent draws, two tries at the same question give the same outcome {agree:.0%} of the time when p(resolve)={q}")
assert round(agree, 2) == 0.53
```

**Output (my run):**
```text
absolute 3 points, relative 5%
independent conversations needed per arm: 4,130
observed diff +2.74 pts; naive SE 0.63 pts; user-level SE 0.80 pts; design effect ~ 1.62
naive z = 4.38   user-level z = 3.45
implied intra-user correlation 0.21 (built in: 0.20)
if retries were independent draws, two tries at the same question give the same outcome 53% of the time when p(resolve)=0.63
```
The intra-user correlation and the 4 conversations per user are invented. The point is the direction and size of the correction, which depends on your real data.

**Follow-ups:**
- Could you set temperature to 0 to remove the noise? It lowers within-prompt randomness but does not make the test unnecessary, and it changes the product you ship. Test the setting you will ship. See Book 1 Part 10 Q55 (non-deterministic treatment).
- What about a user who only has one conversation? They count once; the clustering matters for users with several.

**Common mistakes:** Per-conversation randomization. Intervals computed as if all conversations were independent. Reporting resolution alone. Excluding users who retried. Ignoring that "resolved" can mean "gave up".

### Q37 ⭐⭐ 🟡 An LLM judge prefers the new model in 620 of 1,000 offline pairs (62%), but humans agree with the judge on only 71% of 200 audited pairs, and the new model's answers are 35% longer. Explain how you validate the judge, what the 62% really tells you and how it connects to the online test.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
**Say this first (1 line):** The 62% is a judge's win rate on offline pairs, and with 71% agreement with humans and a 35% length gap it is weak evidence of better quality, so I validate the judge first and let only the online test decide.

**Clarifying questions:**
- How were the 200 audited pairs chosen: random, or the ones the judge was unsure about? Why: a biased audit gives biased agreement.
- Are the 1,000 pairs on the same prompts for both models and in random A/B order? Why: position bias in the judge would favour one slot.
- What does the judge see: only the answers, or also model names, and is it the same family as the new model? Why: judges often prefer their own style (self-preference).
- Were ties possible? Why: forcing a winner on tied pairs adds noise.
- What is the online decision this feeds: ship, or just pick which candidate to test? Why: a screening use needs less proof than a ship decision.

**Approach:**
1. Say what 62% is. 620 of 1,000 pairs means the judge preferred the new answer in 62% of pairs; the interval from sampling noise alone is about 59% to 65%. It says nothing about whether the judge is right.
2. Measure judge quality on the human-audited pairs. Agreement 71% is not very high for a two-answer choice; where the two sides are about equally likely, chance agreement is already about 50%, so Cohen's kappa is the better figure (about 0.42 in my invented table).
3. Break the audit down: where does the judge disagree with humans, and does the disagreement correlate with length, with answer position, or with style?
4. Correct the headline for judge error. If the judge says "new" in 80% of the cases where humans say "new" and 38% where humans say "old", the error-corrected human-preference rate is about 57%, with a wide interval (about 40% to 74%) that includes 50%.
5. Control length: compare at matched length, or add a length-penalised judge, or use pairwise comparisons where the judge is told not to reward length. Swap the order of the two answers and average.
6. Use the judge as a screen, not a verdict. Ship decisions come from the online test, with the judge as a monitoring metric whose link to online outcomes is checked.

**Metrics:**
- Judge win rate = pairs where the judge prefers new / pairs judged (62%), with an interval.
- Agreement = pairs where judge and human agree / audited pairs (71%); kappa = (agreement - chance agreement) / (1 - chance agreement).
- Per-slice agreement (by length bucket, position, topic).
- Online: task success, re-contact, CSAT, cost, latency; correlation between offline judge score and online outcome across past experiments.

**Risks:**
- Length bias: longer answers look more complete to a judge; 35% longer is a red flag.
- Self-preference when the judge shares a model family with one candidate.
- Position bias (the first answer wins too often).
- A small audit (200 pairs) gives a wide interval on agreement, about 64% to 77%.
- Optimising for the judge makes the judge a worse measure (it becomes the target).

**What the interviewer scores:**
- Strong: separates "the judge's win rate" from "truth", and quantifies judge error with an audit.
- Strong: names length, position and self-preference bias, and a control for each.
- Strong: connects to the online test and says offline only screens.
- Weak: "62% win rate, ship."
- Weak: "71% agreement is fine" with no chance-correction.

**Example:** (illustrative numbers) The invented audit has 80 pairs where both say new, 38 where the judge says new and humans say old, 20 where the judge says old and humans say new, 62 where both say old. Agreement is 142/200 = 71%, kappa 0.42. Correcting 62% for those error rates gives about 57%, interval 40% to 74%. A second simulation shows a judge that adds a small length bonus gives a 58% win rate at exactly equal quality, and 71% with a larger bonus. Weak answer: "the judge likes the new model 62% of the time, so it is better." Strong answer: "the judge is only moderately reliable and length-biased; the corrected preference could be near 50%, so I run the online test."

**Code:**
```python
# Q37: LLM judge 620/1000, humans agree on 71% of 200 audited pairs, new answers 35% longer. Illustrative, seeded.
import numpy as np
from scipy import stats

n, w = 1000, 620
assert w / n == 0.62
def wilson(k, n, z=1.96):
    p = k / n; c = (p + z*z/(2*n)) / (1 + z*z/n)
    h = z * np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return c - h, c + h
lo, hi = wilson(w, n)
print(f"judge win rate 62.0%, 95% CI [{lo:.1%}, {hi:.1%}] (sampling noise only)")
assert 0.58 < lo < 0.60 and 0.64 < hi < 0.66

# invented audit table of 200 pairs: judge says new wins (Jn) / old wins (Jo); human says new (Hn) / old (Ho)
Jn_Hn, Jn_Ho, Jo_Hn, Jo_Ho = 80, 38, 20, 62
assert Jn_Hn + Jn_Ho + Jo_Hn + Jo_Ho == 200
agree = (Jn_Hn + Jo_Ho) / 200
print(f"agreement {agree:.0%}")
assert agree == 0.71
po = agree
pj = (Jn_Hn + Jn_Ho) / 200; ph = (Jn_Hn + Jo_Hn) / 200
pe = pj * ph + (1 - pj) * (1 - ph)
kappa = (po - pe) / (1 - pe)
print(f"Cohen kappa {kappa:.2f}")
tpr = Jn_Hn / (Jn_Hn + Jo_Hn)       # P(judge says new | human says new)
fpr = Jn_Ho / (Jn_Ho + Jo_Ho)       # P(judge says new | human says old)
print(f"judge says 'new' when humans say new: {tpr:.0%}; when humans say old: {fpr:.0%}")
# correct the 62% for judge error (Rogan-Gladen), bootstrap over the audit
def corrected(j, tpr, fpr): return (j - fpr) / (tpr - fpr)
h_hat = corrected(0.62, tpr, fpr)
print(f"error-corrected human-preference rate ~ {h_hat:.1%}")
rng = np.random.default_rng(37)
cells = np.array([Jn_Hn, Jn_Ho, Jo_Hn, Jo_Ho]); hs = []
for _ in range(4000):
    a, b, c, d = rng.multinomial(200, cells / 200)
    t, f = a / max(a + c, 1), b / max(b + d, 1)
    j = rng.binomial(n, 0.62) / n
    if t - f > 0.1: hs.append(corrected(j, t, f))
ci = np.percentile(hs, [2.5, 97.5])
print(f"bootstrap 95% interval for the corrected rate: [{ci[0]:.1%}, {ci[1]:.1%}]")
assert ci[0] < 0.5 < ci[1]   # the interval reaches 50%: no preference not ruled out
# length bias: a judge that adds a bonus for length prefers longer answers even at equal quality
rng = np.random.default_rng(371)
quality_diff = rng.normal(0, 1, 100_000)          # new minus old, true mean 0
for bonus in (0.0, 0.3, 0.8):
    wins = np.mean(quality_diff + bonus + rng.normal(0, 1, 100_000) > 0)
    print(f"true quality equal, judge length bonus {bonus:.1f} -> judge win rate {wins:.1%}")
```

**Output (my run):**
```text
judge win rate 62.0%, 95% CI [59.0%, 65.0%] (sampling noise only)
agreement 71%
Cohen kappa 0.42
judge says 'new' when humans say new: 80%; when humans say old: 38%
error-corrected human-preference rate ~ 57.1%
bootstrap 95% interval for the corrected rate: [40.1%, 73.9%]
true quality equal, judge length bonus 0.0 -> judge win rate 50.1%
true quality equal, judge length bonus 0.3 -> judge win rate 58.3%
true quality equal, judge length bonus 0.8 -> judge win rate 71.5%
```
The audit table, the length bonus and the noise scale are invented for illustration. The correction formula assumes the judge's error rates are the same on the 1,000 pairs as on the audited 200.

**Follow-ups:**
- How big should the audit be? Big enough that the agreement interval is narrow relative to the decision, and stratified by length and topic; 200 pairs gives about plus or minus 6 points. See Book 1 Part 10 Q56 (validating an LLM judge).
- What if humans also disagree with each other? Then agreement with any single human is capped; measure human-human agreement first.

**Common mistakes:** Treating the judge as ground truth. Quoting raw agreement without chance correction. Ignoring length and position. Using the same model family as judge and candidate. Skipping the online test because the offline number is "significant".

### Q38 ⭐⭐ 🟡 An LLM feature raises satisfaction by 2 points but also raises 95th-percentile latency from 1.4 to 3.1 seconds and cost per query from 0.002 to 0.012 dollars (6 times). Explain how you frame the ship decision, which guardrails and budgets you set and what you propose as the next experiment.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
**Say this first (1 line):** A 2-point satisfaction gain is worth shipping only if it pays for a 6 times cost and a slower tail, so I turn the guardrails into budgets, test a routed version that keeps most of the gain, and decide on value per query minus cost per query.

**Clarifying questions:**
- How is satisfaction measured and what is its interval? Why: +2 points may be inside the noise, and it may be measured only on users who answered a survey.
- What does one satisfaction point do for the business (retention, conversion, fewer escalations)? Why: it is the only way to compare 2 points with 0.010 dollars per query.
- What is the latency budget (p95 where users give up, for example)? Why: a tail of 3.1 seconds may cross a drop-off threshold.
- Is the cost of the feature on the margin of this product, or does it scale with usage? Why: 6 times cost on millions of queries is a budget line.
- Which queries gained the most: all, or a hard subset? Why: it decides if routing can keep the gain.

**Approach:**
1. Do the arithmetic: cost 0.012 / 0.002 = 6 times; p95 latency 3.1 / 1.4 = 2.2 times. Say the +2 points has to be paid for twice.
2. Check the benefit is real: interval on satisfaction, effect on a harder outcome (task success, return rate), not only a survey.
3. Convert to money per user: extra cost per query x queries per user. With 20 queries per user per month (invented) that is 0.20 dollars, so the 2 points must be worth at least 0.10 dollars per point per user-month to break even.
4. Set budgets as guardrails before deciding: p95 latency (say at most 2.0 s), p99, timeout rate, cost per query (say at most 0.006 dollars), and a per-user cost cap. A guardrail is a bound with a decision attached, not a dashboard.
5. Look at where the cost and the tail come from. A slow path used for a minority of queries can raise p95 while the median barely moves.
6. Propose the next experiment: a routed arm (cheap model by default, large model for hard queries), a cached or shorter-answer arm, and a streaming display so users see text early. Compare satisfaction, p95, and cost per query against the budgets.
7. Ship only an arm inside the budgets; if none, decide explicitly whether the value covers the cost.

**Metrics:**
- Primary: satisfaction score (or task success), mean difference with interval.
- Latency: p50, p95, p99 and timeout rate of end-to-end time, per arm.
- Cost per query = total model spend / queries; cost per successful task = spend / successes.
- Net value per user = (value of satisfaction gain) - (extra cost per user).
- Guardrails: abandonment after slow responses, error rate, escalation rate.

**Risks:**
- Percentiles are not additive; compare them with a bootstrap or quantile interval, not by subtracting group averages.
- Satisfaction from a survey is biased to people who answer.
- The cost increase can grow with usage (longer conversations) beyond the test period.
- A novelty effect can make the 2 points shrink later.

**What the interviewer scores:**
- Strong: converts the quality gain to money and sets budgets before deciding.
- Strong: treats p95, not the mean, as the latency guardrail and asks where the tail comes from.
- Strong: proposes a routed or cheaper variant as the next test instead of a yes/no.
- Weak: "satisfaction went up so ship" or "6 times cost, so no".
- Weak: no numbers on break-even.

**Example:** (illustrative numbers) 20 queries per user per month. Extra cost is 0.010 x 20 = 0.20 dollars per user-month, so each of the 2 points must be worth about 0.10 dollars per user-month. In the code, a slow path used on 8% of queries lifts p95 from about 1.4 s to about 3.1 s while the median moves only from 0.80 s to 0.94 s. If only 30% of queries go to the large model, the blended cost is 0.005 dollars (2.5 times), and the next test checks whether it keeps most of the 2 points. Weak answer: "users are happier, ship it." Strong answer: "the gain is worth shipping only if it clears 0.20 dollars per user and a 2 s p95, so I test a routed version."

**Code:**
```python
# Q38: satisfaction +2 points, p95 latency 1.4 -> 3.1 s, cost 0.002 -> 0.012 dollars. Illustrative, seeded.
import numpy as np

print("cost multiple:", 0.012 / 0.002, " p95 multiple:", round(3.1 / 1.4, 2))
assert round(0.012 / 0.002, 6) == 6.0 and round(3.1 / 1.4, 2) == 2.21

# break-even: extra cost per user-month vs value of +2 satisfaction points (value per point is a made-up input)
q_per_user = 20                      # queries per user per month (invented)
extra_cost = (0.012 - 0.002) * q_per_user
print(f"extra cost per user-month: {extra_cost:.2f} dollars")
assert abs(extra_cost - 0.20) < 1e-9
need_per_point = extra_cost / 2
print(f"the 2 points must be worth at least {need_per_point:.2f} dollars per point per user-month to break even")

# latency: where does a p95 jump come from? a slow path for a minority of queries
rng = np.random.default_rng(38)
n = 200_000
old = rng.lognormal(np.log(0.8), 0.35, n)
slow = rng.random(n) < 0.08                         # 8% of queries go through a slow reasoning path
new = np.where(slow, rng.lognormal(np.log(3.3), 0.25, n), rng.lognormal(np.log(0.9), 0.35, n))
for name, x in (("old", old), ("new", new)):
    print(f"{name}: p50 {np.percentile(x,50):.2f}s  p95 {np.percentile(x,95):.2f}s  mean {x.mean():.2f}s")
assert np.percentile(new, 95) > 2 * np.percentile(old, 95)
assert np.percentile(new, 50) < 1.3 * np.percentile(old, 50)

# routing: send only hard queries to the expensive model
cheap, dear = 0.002, 0.012
for share in (1.0, 0.5, 0.3, 0.2):
    blended = share * dear + (1 - share) * cheap
    print(f"share of queries on the large model {share:.0%}: blended cost {blended:.4f} dollars ({blended/cheap:.1f}x)")
assert abs((0.3 * dear + 0.7 * cheap) - 0.005) < 1e-12
```

**Output (my run):**
```text
cost multiple: 6.0  p95 multiple: 2.21
extra cost per user-month: 0.20 dollars
the 2 points must be worth at least 0.10 dollars per point per user-month to break even
old: p50 0.80s  p95 1.42s  mean 0.85s
new: p50 0.94s  p95 3.06s  mean 1.15s
share of queries on the large model 100%: blended cost 0.0120 dollars (6.0x)
share of queries on the large model 50%: blended cost 0.0070 dollars (3.5x)
share of queries on the large model 30%: blended cost 0.0050 dollars (2.5x)
share of queries on the large model 20%: blended cost 0.0040 dollars (2.0x)
```
The latency mixture and the value per point are invented. The routed 2.5 times figure is blended arithmetic; whether routing keeps the gain is exactly what the next experiment must measure.

**Follow-ups:**
- Who decides the budget? Product and finance own the cost line, engineering the latency line, the data scientist writes the break-even and the experiment; the budget is agreed before the result.
- What if the gain is only for hard queries? Route those to the large model and keep the cheap path elsewhere.

**Common mistakes:** Deciding on satisfaction alone. Comparing mean latency when users feel the tail. Ignoring cost until finance asks. Treating a guardrail as a suggestion. Shipping without testing a cheaper variant.

### Q39 ⭐⭐ 🔴 A booking platform gave a pricing tool to a random half of 10,000 hosts, and treated listings average 10.8 bookings a month against 10.0 for control listings (+8% relative to control). Guest demand in each city is roughly fixed, so the two groups compete for the same bookings. Explain what the +8% measures, what the market-level effect could be and how you design a test to estimate it.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
**Say this first (1 line):** The +8% compares treated listings with control listings that lost the bookings the treated ones won, so it measures a share gain, and the effect on the whole market could be near zero; I would randomize whole cities, not hosts.

**Clarifying questions:**
- How fixed is demand: does a cheaper or better-priced listing bring in new guests, or only move them? Why: it decides whether the market effect is zero or a fraction of +8%.
- What does the tool do (lower prices, smarter prices)? Why: lower prices can grow demand, smarter prices may only reshuffle it.
- Do the 10,000 hosts sit in a few cities or many? Why: the number of independent markets is the real sample size.
- What is the outcome that matters: bookings, revenue, host earnings, guest satisfaction? Why: a booking at a lower price can be worth less.
- Is there a month or more of pre-launch data per city? Why: it lets me remove city-to-city differences.

**Approach:**
1. Say what +8% is. Treated 10.8 versus control 10.0 is +8% relative to control. If demand is fixed, the market average is the same with everyone treated, and with no-one treated: (5,000 x 10.8 + 5,000 x 10.0) / 10,000 = 10.4. Treated gained 0.4 over that average and control lost 0.4. The 0.8 gap is redistribution.
2. Name the problem: interference. A host's outcome depends on other hosts' assignment (they share guests), so the usual assumption that one unit's outcome does not depend on another's fails.
3. Set the estimand: the global effect, bookings per listing when all listings use the tool versus when none do.
4. Design: randomize at the market level (whole cities), treated cities versus control cities; add a pre-period to adjust each city for its own baseline. A middle path is mixed saturation: cities at 0%, 50% and 100% of hosts treated, which also shows how much of the host-level gap is competition.
5. Accept the cost: only a few dozen independent units, so the interval is wide; use the pre-period (a difference-in-differences or regression adjustment), pair similar cities, and run long enough.
6. Report both: the host-level gap (what a host sees) and the market-level effect (what the platform gets), and say which one the decision depends on.

**Metrics:**
- Primary (market level): bookings per listing = bookings in the city / active listings in the city, compared with the city's own pre-period.
- Also: revenue per listing, guest-side conversion, prices and occupancy, share of bookings going to treated listings within a mixed city.
- Guardrails: guest satisfaction, cancellation rate, host churn in control.
- Host-level gap = treated bookings per listing / control bookings per listing - 1 (+8% here); it is not the market effect.

**Risks:**
- Reading +8% as the platform's gain: it can overstate the market effect up to fully.
- Few clusters give a low-power test; with 40 cities and no pre-period the interval can be tens of percent wide.
- Cities differ in size and season; assignment must be balanced on those.
- Spillover across nearby cities (guests searching in two towns) can leak.

**What the interviewer scores:**
- Strong: does the "fixed pie" arithmetic (10.4) and says the +8% is mostly redistribution if demand is fixed.
- Strong: proposes cluster (city) randomization, mixed saturation, and a pre-period adjustment, and notes the power cost.
- Strong: separates the host view from the platform view.
- Weak: "randomization makes the +8% causal, so it is the effect."
- Weak: proposes more hosts as the fix, which does not remove interference.

**Example:** (illustrative numbers) In the code, 40 cities of 250 listings, guests split by attractiveness, treated listings 8% more attractive. Host-level randomization shows about +8% whether total demand is fixed (true market effect 0%) or grows a little (elasticity 0.25, true market effect +1.9%). City-level randomization with each city compared to its own pre-period recovers 0.0% and +1.9%, with a standard deviation of about 0.9 points across assignments; without the pre-period the standard deviation is about 10 points, which is useless. Weak answer: "10.8 versus 10.0 is +8%, ship." Strong answer: "that is the host-vs-host gap; I would test at city level against each city's own history."

**Code:**
```python
# Q39: host-level pricing tool in a market with roughly fixed guest demand. Illustrative, seeded.
import numpy as np

print("relative lift:", round(10.8 / 10.0 - 1, 3))
assert round(10.8 / 10.0 - 1, 3) == 0.08
tot = 5000 * 10.8 + 5000 * 10.0
print("if demand is fixed, everyone-treated or nobody-treated average =", tot / 10_000)
assert tot / 10_000 == 10.4            # market average bookings per listing is 10.4 either way
print(f"treated gain over market average {10.8-10.4:+.1f}, control loss {10.0-10.4:+.1f}: the gap of 0.8 is all redistribution")

rng = np.random.default_rng(39)
C, N_PER = 40, 250                      # 40 cities, 250 listings each = 10,000 hosts
gamma = np.log(1.08)                    # treated listings are 8% more attractive to guests

def city_bookings(frac_treated, eps, Dper, treated_mask):
    """Guests split across listings in proportion to attractiveness w; city demand grows with mean w**eps."""
    w = np.where(treated_mask, np.exp(gamma), 1.0)
    D = Dper * N_PER * (w.mean() ** eps)
    return rng.poisson(D * w / w.sum())

def host_level(eps):
    diffs = []
    for _ in range(30):
        c = []; t = []
        for _ in range(C):
            m = np.zeros(N_PER, bool); m[: N_PER // 2] = True
            b = city_bookings(0.5, eps, 10.4 * rng.lognormal(0, 0.3), m)
            t.append(b[m].mean()); c.append(b[~m].mean())
        diffs.append(np.mean(t) / np.mean(c) - 1)
    return np.mean(diffs)

def city_level(eps, reps=400):
    est, adj = [], []
    for _ in range(reps):
        treated_city = rng.permutation(C) < C // 2
        tt, cc, tt2, cc2 = [], [], [], []
        for i in range(C):
            Dper = 10.4 * rng.lognormal(0, 0.3)
            m = np.full(N_PER, bool(treated_city[i]))
            b = city_bookings(1.0, eps, Dper, m)
            pre = rng.poisson(Dper * N_PER) / N_PER          # same city, month before launch
            (tt if treated_city[i] else cc).append(b.mean())
            (tt2 if treated_city[i] else cc2).append(b.mean() / pre)
        est.append(np.mean(tt) / np.mean(cc) - 1)
        adj.append(np.mean(tt2) / np.mean(cc2) - 1)
    return np.mean(est), np.std(est), np.mean(adj), np.std(adj)

for eps in (0.0, 0.25):
    h = host_level(eps)
    m, s, ma, sa = city_level(eps)
    print(f"demand elasticity {eps}: host-level estimate {h:+.1%};  city-level estimate {m:+.1%} (sd {s:.1%});  city-level vs own pre-period {ma:+.1%} (sd {sa:.1%})")
    assert sa < s / 3
    assert abs(ma - (1.08 ** eps - 1)) < 0.01
    if eps == 0.0:
        assert abs(h - 0.08) < 0.01 and abs(m) < 0.03
    else:
        assert abs(h - 0.08) < 0.01 and 0.0 < m < 0.06      # true market effect is 1.08**0.25 - 1
print("true market effect with elasticity 0.25:", f"{1.08**0.25-1:+.1%}")
```

**Output (my run):**
```text
relative lift: 0.08
if demand is fixed, everyone-treated or nobody-treated average = 10.4
treated gain over market average +0.4, control loss -0.4: the gap of 0.8 is all redistribution
demand elasticity 0.0: host-level estimate +8.2%;  city-level estimate +0.9% (sd 10.0%);  city-level vs own pre-period -0.0% (sd 0.9%)
demand elasticity 0.25: host-level estimate +8.1%;  city-level estimate +3.6% (sd 10.3%);  city-level vs own pre-period +1.9% (sd 0.9%)
true market effect with elasticity 0.25: +1.9%
```
The elasticity, the city-demand spread and the Poisson booking noise are invented, so the numbers show the pattern (host-level gap versus market effect, and why the pre-period matters), not a real platform.

**Follow-ups:**
- Why not just use a bigger sample of hosts? More hosts shrink noise but not the bias from competition. See Book 1 Part 10 Q37 (marketplace experiments) and Q29 in this part (regional randomization with one dominant region).
- Is host-level ever fine? Yes when the market is large and the treated share is small, so each host barely affects the others, or when the question is about the host's own outcome.

**Common mistakes:** Reporting the host gap as the platform effect. Adding hosts instead of changing the unit. Ignoring that cities are the real sample size. Skipping pre-period adjustment. Forgetting guest-side outcomes.

### Q40 ⭐⭐ 🔴 Treatment raises sessions per user by 10% relative to control and lowers revenue per session by 4% relative to control, and the team reports 'revenue per session is down, so the test failed'. Revenue per user is therefore up about 5.6% relative to control (1.10 x 0.96 = 1.056). Explain which metric should drive the decision, why the ratio misleads here and what else you check.
**Asked at:** Ratio-metric, delta-method and variance-reduction material (Spotify Confidence ratio-metric RFP and variance-reduction docs, MetricGate CUPED and delta-method pages, a TechPrep '66 Variance Reduction Interview Questions' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Revenue per session fell only because sessions per user rose, so I decide on revenue per user (the product of the two), and I check that the extra sessions are real value and not low-quality traffic.

**Clarifying questions:**
- Why do sessions rise: notifications, a redesign that splits one visit into two, or real extra use? Why: split visits inflate sessions without adding value.
- Is the 5.6% revenue per user an interval or a point, and is it significant? Why: the arithmetic is only as good as its error bars.
- What was the agreed primary metric before the test? Why: switching metric after seeing the result is a bias.
- What costs go with extra sessions (support, servers, refunds)? Why: revenue is not margin.
- Does retention or return-rate change in the following weeks? Why: more sessions today may mean fewer later.

**Approach:**
1. Check the arithmetic: 1.10 x 0.96 = 1.056, so revenue per user is up 5.6%. This works as an identity when "revenue per session" is total revenue divided by total sessions (ratio of sums) and "per user" is the average over users.
2. Name the issue: revenue per session is a ratio whose denominator moves with treatment. If treatment adds sessions that are worth less than the average one, the ratio falls even when total revenue rises. Here the extra sessions bring about 1.11 per session against 2.01 for the average (in my code).
3. Pick the decision metric: revenue per user, the unit that was randomized, with the interval (about +3.5% to +7.2% in my run). Revenue per session becomes a diagnostic.
4. Analyse properly: ratio metrics with the delta method, or user-level totals. Do not treat sessions as independent rows.
5. Check quality of the extra sessions: are they bounces, accidental, double sessions after a redesign? Look at session length, conversion per session, and the share of sessions with revenue.
6. Check guardrails and the future: refund rate, cost to serve, 7-day and 28-day return rate, and revenue per user in later weeks.
7. Decide: if revenue per user is up with a clear interval, guardrails hold and the extra sessions are not artefacts, call the test a success and explain the metric move.

**Metrics:**
- Primary: revenue per user = total revenue / users in arm, mean difference with 95% interval.
- Decomposition: sessions per user = sessions / users; revenue per session = total revenue / total sessions (ratio of sums). Relative effects multiply: (1+a)(1+b) - 1.
- Guardrails: refund rate, cost per user, return rate in later weeks, session length distribution.

**Risks:**
- Mean of per-user ratios is a different quantity from the ratio of sums (-4.6% versus -3.9% in my run); say which one you report.
- Revenue is heavy-tailed; a few big spenders can swing the user-level mean.
- More sessions can come from a worse experience (users come back because the first visit failed).
- A ratio's denominator is itself an outcome, so conditioning on sessions (analysing only users with sessions) is biased.

**What the interviewer scores:**
- Strong: multiplies the effects, picks the randomization unit's metric, and explains the denominator effect.
- Strong: checks whether the extra sessions are valuable, and what happens later.
- Strong: mentions the delta method for the ratio's interval.
- Weak: "revenue per session is down, the test failed."
- Weak: "revenue per user is up so everything is fine" with no guardrail check.

**Example:** (illustrative numbers) 100,000 users per arm. Control: 5.0 sessions and 2.00 revenue per session, so 10 per user. Treatment: +10% sessions, -4% per session, about 10.56 per user. The code gives sessions per user +9.7%, revenue per session -3.9%, revenue per user +5.4% with an interval of +3.5% to +7.2%, and the extra sessions bring about 1.11 each. Weak answer: "per-session revenue fell, it failed." Strong answer: "the rate fell because the denominator grew; per user, which is what we randomized, it is up and I would check the extra sessions are real."

**Code:**
```python
# Q40: sessions/user +10%, revenue/session -4%, revenue/user +5.6%. Illustrative, seeded.
import numpy as np

print("1.10 x 0.96 =", round(1.10 * 0.96, 3))
assert round(1.10 * 0.96, 3) == 1.056

rng = np.random.default_rng(40)
U = 100_000
def arm(mean_sessions, rev_per_session):
    # users differ in activity (gamma), sessions ~ Poisson; each session's revenue is zero-inflated and skewed
    act = rng.gamma(2.0, mean_sessions / 2.0, U)
    s = rng.poisson(act)
    rev = np.array([0.0] * U)
    tot = s.sum()
    per = np.where(rng.random(tot) < 0.1, rng.exponential(rev_per_session * 10, tot), 0.0)
    idx = np.repeat(np.arange(U), s)
    rev = np.bincount(idx, weights=per, minlength=U)
    return s, rev
sc, rc = arm(5.0, 2.00)
st, rt = arm(5.5, 1.92)

spu = st.mean() / sc.mean() - 1
rps = (rt.sum() / st.sum()) / (rc.sum() / sc.sum()) - 1
rpu = rt.mean() / rc.mean() - 1
print(f"sessions/user {spu:+.1%}   revenue/session (ratio of sums) {rps:+.1%}   revenue/user {rpu:+.1%}")
assert abs(spu - 0.10) < 0.02 and abs(rps + 0.04) < 0.03
# identity: revenue/user = sessions/user x revenue/session when the ratio is a ratio of sums
assert abs((1 + rpu) - (1 + spu) * (1 + rps)) < 1e-9

# interval for revenue per user: difference in means, user is the unit
d = rt.mean() - rc.mean()
se = np.sqrt(rt.var(ddof=1) / U + rc.var(ddof=1) / U)
print(f"revenue/user diff {d:.3f}, 95% CI [{d-1.96*se:.3f}, {d+1.96*se:.3f}]  = [{(d-1.96*se)/rc.mean():+.1%}, {(d+1.96*se)/rc.mean():+.1%}] relative")
assert d - 1.96 * se > 0
# delta-method SE of the ratio-of-sums revenue/session vs naive per-session SE
def ratio_se(num, den):
    r = num.sum() / den.sum(); m = den.mean()
    z = (num - r * den) / m
    return r, np.sqrt(z.var(ddof=1) / len(num))
rr, se_delta = ratio_se(rc, sc)
# naive: treat sessions as independent draws: need per-session values
print(f"control revenue/session {rr:.3f}, delta-method SE {se_delta:.4f}")
# mean of per-user ratios is a different quantity
mask_c, mask_t = sc > 0, st > 0
mor_c = (rc[mask_c] / sc[mask_c]).mean(); mor_t = (rt[mask_t] / st[mask_t]).mean()
print(f"mean of per-user ratios: {mor_t/mor_c-1:+.1%} (a different number from the ratio of sums {rps:+.1%})")
# a mix-shift check: the extra sessions are lower value than the existing ones
extra_sessions = st.sum() - sc.sum(); extra_rev = rt.sum() - rc.sum()
print(f"extra sessions {extra_sessions:,.0f}, extra revenue {extra_rev:,.0f} -> {extra_rev/extra_sessions:.2f} per extra session vs {rc.sum()/sc.sum():.2f} existing average")
assert extra_rev > 0
```

**Output (my run):**
```text
1.10 x 0.96 = 1.056
sessions/user +9.7%   revenue/session (ratio of sums) -3.9%   revenue/user +5.4%
revenue/user diff 0.540, 95% CI [0.351, 0.728]  = [+3.5%, +7.2%] relative
control revenue/session 2.012, delta-method SE 0.0124
mean of per-user ratios: -4.6% (a different number from the ratio of sums -3.9%)
extra sessions 48,470, extra revenue 53,961 -> 1.11 per extra session vs 2.01 existing average
```
The simulated effects (about +9.7%, -3.9%, +5.4%) differ a little from the prompt's round figures because of sampling noise; the identity (1 + a)(1 + b) = 1 + c is exact for ratio of sums and is asserted in the code.

**Follow-ups:**
- When would revenue per session be the right metric? When the question is about monetization of an unchanged amount of traffic, for example ad load, and sessions do not move. See Book 1 Part 10 Q27 (ratio metrics) and Q8 in this part (CTR as clicks over impressions).
- What if the interval on revenue per user includes zero? Then I cannot claim a gain; I would look at power and run longer, not choose the favourable ratio.

**Common mistakes:** Judging on a ratio whose denominator is also moved by treatment. Computing the interval with sessions as independent. Mixing ratio of sums and mean of ratios. Declaring success without guardrails. Dropping users with zero sessions.

### Q41 ⭐⭐ 🔴 A product launched in one country, and 15 other countries are available as donors. With 8 pre-launch weeks the synthetic-control fit has an average error of 1.5% of weekly revenue, and the post-launch gap is +2.5% of weekly revenue. Explain how you judge whether +2.5% is real using placebo tests, and what could invalidate the donor pool.
**Asked at:** Causal-inference and when-you-cannot-randomize material (an Interview Query causal-inference guide on diff-in-diff and synthetic control, Codemia 'explain difference-in-differences' practice pages, NBER working paper 25532 on synthetic difference-in-differences); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A +2.5% gap on a fit that is off by 1.5% in normal weeks is not convincing by itself; I would run the same method on every donor country as a fake launch, and with only 16 countries the best p-value I can ever get is 1/16 = 6.25%.

**Clarifying questions:**
- How many post-launch weeks, and did anything else change in that country (a price move, a holiday, a competitor)? Why: synthetic control assumes only the launch differs.
- What outcome and what scale: weekly revenue, and how noisy is it week to week? Why: it sets the size of a normal gap.
- Which of the 15 donors are similar (same region, same product maturity)? Why: a donor pool that is unlike the launch country gives a poor counterfactual.
- Could any donor be affected by the launch (shared users, shared supply, cross-border spillover)? Why: contaminated donors bias the gap.
- Is the launch country special (the first market, chosen because it looked promising)? Why: selection makes the pre-trend a poor guide.

**Approach:**
1. Frame the question: gap = launch country minus its synthetic version (a weighted mix of donors that tracks the launch country before launch). The weights are non-negative and sum to 1.
2. Put the gap in context: 1.5% is the average miss in the pre period, so +2.5% is only about 1.7 times a normal miss. That is thin.
3. Run placebo tests in space: pretend each donor was the launch country, build a synthetic version for it from the other countries, and compute its post-launch gap. If many placebos show gaps as large as +2.5%, the launch result is not special.
4. Use a ratio that adjusts for fit: post-launch RMSPE (root mean squared prediction error) divided by pre-launch RMSPE. Rank the launch country among the 16 countries.
5. Read the rank honestly: the placebo p-value is rank / 16. Even rank 1 gives 0.0625; so with 16 units I can say "most extreme of 16", not "p < 0.05".
6. Run placebos in time too (pretend the launch was 4 weeks earlier), check leave-one-out donor weights, and vary the pre period.
7. Look at the donor pool: remove donors with big weights one at a time and see if the gap holds.

**Metrics:**
- Gap = (actual - synthetic) / pre-launch mean of the launch country's revenue (+2.5% here), by week and averaged.
- Pre-RMSPE = square root of the mean of squared pre-launch gaps (the 1.5% fit error).
- Ratio = post-RMSPE / pre-RMSPE; placebo p-value = (number of units with ratio at least the launch country's) / 16.
- Guardrails: donor weights (no single donor above, say, 50%), pre-period length (8 weeks is short), stability of the gap across leave-one-out fits.

**Risks:**
- With 8 pre-weeks and 15 donors the weights can overfit noise (more donors than weeks), which makes the pre fit look good and the post gap a poor guide.
- A good pre-fit does not prove the donors keep tracking after launch.
- Spillover from the launch country into donors biases the gap in an unknown direction.
- A few-unit permutation test has low power: a true effect can fail to stand out.

**What the interviewer scores:**
- Strong: compares the gap with the pre-fit error and runs placebos on every donor.
- Strong: knows the smallest p-value (1/16) and says what the test can and cannot show.
- Strong: lists donor-pool failure modes (spillover, dissimilar donors, overfit weights).
- Weak: "the gap is positive, so the launch worked."
- Weak: quotes a p-value below 0.0625 from a 16-unit permutation test.

**Example:** (illustrative numbers) In the simulation, 16 countries, 8 pre weeks and 8 post weeks, a +2.5% effect added to the launch country, weekly noise chosen so the launch country's pre-fit error is 1.5%. The estimated post gap is +1.7%, the launch country's ratio ranks 14th of 16 (placebo p = 0.875), and the largest placebo gap is 7.3%. Over 80 simulated worlds, the launch country has the top ratio in 10% of worlds when the true effect is +2.5% and also in 10% when it is zero. So this design cannot tell a real +2.5% from nothing. Weak answer: "+2.5% is a positive lift, ship." Strong answer: "the gap is smaller than normal placebo gaps; I would not claim it, and I would add pre-weeks, donors or a regional split."

**Code:**
```python
# Q41: synthetic control, 1 treated + 15 donors, 8 pre weeks, placebo-in-space test. Illustrative, seeded.
import numpy as np
from scipy.optimize import minimize

U, PRE, POST = 16, 8, 8
print("smallest possible placebo p-value with 16 units: 1/16 =", round(1 / 16, 4))
assert round(1 / 16, 4) == 0.0625          # cannot reach 0.05 however large the gap

def synth_gap(Y, i, pre):
    """Fit non-negative weights summing to 1 on the other units, return gap series (unit i minus synthetic), in % of own level."""
    others = [j for j in range(Y.shape[0]) if j != i]
    X = Y[others][:, :pre].T; y = Y[i, :pre]
    k = len(others)
    f = lambda w: np.sum((X @ w - y) ** 2)
    res = minimize(f, np.full(k, 1 / k), method="SLSQP", bounds=[(0, 1)] * k,
                   constraints={"type": "eq", "fun": lambda w: w.sum() - 1}, options={"maxiter": 200})
    w = res.x
    return (Y[i] - w @ Y[others]) / Y[i, :pre].mean()

def one_world(rng, effect):
    t = np.arange(PRE + POST)
    common = 100 * (1 + 0.004 * t + 0.02 * np.sin(t / 2.0))
    load1 = rng.normal(0, 1, U); load2 = rng.normal(0, 1, U)
    f2 = np.cumsum(rng.normal(0, 0.6, PRE + POST))
    Y = common[None, :] * (1 + 0.04 * load1[:, None] * (t[None, :] - 4) / 8 + 0.01 * load2[:, None] * f2[None, :] / 2)
    Y = Y * (1 + rng.normal(0, 0.022, Y.shape))            # weekly noise
    Y[0, PRE:] *= (1 + effect)                                # unit 0 is the launch country
    return Y

def ratios(Y):
    out = []
    for i in range(U):
        g = synth_gap(Y, i, PRE)
        pre = np.sqrt(np.mean(g[:PRE] ** 2)); post = np.sqrt(np.mean(g[PRE:] ** 2))
        out.append((pre, post, post / pre, g[PRE:].mean()))
    return np.array(out)

rng = np.random.default_rng(41)
Y = one_world(rng, 0.025)
r = ratios(Y)
rank = int((r[:, 2] >= r[0, 2]).sum())
print(f"launch country: pre-RMSPE {r[0,0]*100:.2f}%  mean post gap {r[0,3]*100:+.2f}%  post/pre ratio {r[0,2]:.1f}")
print(f"placebo countries: median pre-RMSPE {np.median(r[1:,0])*100:.2f}%, largest |mean post gap| {np.abs(r[1:,3]).max()*100:.2f}%")
print(f"rank of the launch ratio among 16: {rank}  -> placebo p = {rank}/16 = {rank/16:.3f}")
assert rank / 16 >= 0.0625

# how often would a real +2.5% effect even rank first, and how often does a zero effect rank first? (80 worlds each)
for eff in (0.025, 0.0):
    firsts = 0; sims = 80; gaps = []
    for s in range(sims):
        rr = ratios(one_world(np.random.default_rng(1000 + s), eff))
        firsts += int(rr[0, 2] >= rr[1:, 2].max()); gaps.append(rr[0, 3])
    print(f"true effect {eff:+.1%}: launch country has the top ratio in {firsts}/{sims} worlds ({firsts/sims:.0%}); mean estimated gap {np.mean(gaps)*100:+.2f}%")
    if eff == 0.0:
        assert firsts / sims < 0.2             # near 1/16 = 6%
```

**Output (my run):**
```text
smallest possible placebo p-value with 16 units: 1/16 = 0.0625
launch country: pre-RMSPE 1.51%  mean post gap +1.67%  post/pre ratio 1.7
placebo countries: median pre-RMSPE 1.55%, largest |mean post gap| 7.33%
rank of the launch ratio among 16: 14  -> placebo p = 14/16 = 0.875
true effect +2.5%: launch country has the top ratio in 8/80 worlds (10%); mean estimated gap +2.69%
true effect +0.0%: launch country has the top ratio in 8/80 worlds (10%); mean estimated gap +0.14%
```
The data-generating process (factor loadings, noise level) is invented and was tuned only so the pre-fit error is near 1.5%. The low power is a property of this simulated world; real data could be easier or harder. With 80 worlds, the 10% figures are noisy (about plus or minus 3 points).

**Follow-ups:**
- How could you get more power? More pre-weeks, more donors (regions inside countries), a longer post period, or a design like difference-in-differences with several launch markets. See Book 1 Part 10 Q49 (synthetic control) and Q28 (difference-in-differences) for the method.
- Is the placebo p-value a real p-value? It is a permutation-style rank test; it is valid if the launch country is exchangeable with the donors, which is a strong assumption.

**Common mistakes:** Reporting a gap without a pre-fit error. Skipping the placebo runs. Claiming p < 0.05 from 16 units. Letting one donor carry the weights. Forgetting spillover to donors and other launches at the same time.

### Q42 ⭐⭐ 🔴 A teammate uses sessions during the first 3 days of the experiment as the CUPED covariate because it correlates 0.9 with the outcome (28-day sessions), and the adjusted confidence interval is much tighter. Treatment changes early sessions. Explain what is wrong, which direction the bias goes and what a valid covariate would be.
**Asked at:** Ratio-metric, delta-method and variance-reduction material (Spotify Confidence ratio-metric RFP and variance-reduction docs, MetricGate CUPED and delta-method pages, a TechPrep '66 Variance Reduction Interview Questions' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The covariate is measured after treatment started and treatment changes it, so CUPED subtracts part of the real effect, pulls the estimate toward zero here, and makes the wrong answer look more certain; use pre-experiment data.

**Clarifying questions:**
- Is the 3-day window counted from each user's first exposure, and is exposure the same time as assignment? Why: even "early" data after exposure is affected by treatment.
- What is the outcome: 28-day sessions per user? Why: it fixes which pre-period metric is the matching covariate.
- Do all users have pre-experiment history? Why: new users have no pre-period data; they need a separate rule (the mean).
- Does the treatment effect on early sessions go the same way as on 28-day sessions? Why: it decides the direction of the bias.
- Is the adjusted analysis the pre-registered one? Why: picking the analysis that gives the tighter interval after seeing data is another bias.

**Approach:**
1. Recall the rule: CUPED adjusts the outcome with a covariate that is fixed before treatment, so it is independent of assignment. The adjusted outcome is Y - theta x (X - mean of X), with theta = cov(Y, X) / var(X).
2. Show why the teammate's covariate breaks it. Early sessions X are caused partly by treatment. The adjustment subtracts theta x (the treatment effect on X) from the effect on Y. With a high correlation, theta is near 1, so the adjusted effect is roughly the effect on Y minus the effect on early sessions.
3. Direction: here treatment raises both early and 28-day sessions, so the estimate is pulled toward zero (an understated effect). If treatment lowered early sessions but raised long-run ones, the effect would be overstated. In general the sign is (effect on Y) minus theta x (effect on X).
4. Why the interval looks better: the correlation of 0.9 shrinks the variance by 1 - 0.9^2 = 0.19, so the standard error is about 44% of the original. A narrow interval around a biased number means the confidence interval misses the truth most of the time.
5. Fix: use the same metric in the 28 days before the experiment (or 1 to 4 weeks, tested for correlation) as the covariate, and fix the choice before launch.
6. Check: compare the adjusted and unadjusted estimates; they should agree up to noise. A big gap between them is a red flag. Also test that the covariate is balanced across arms (it should be, for a pre-experiment covariate).

**Metrics:**
- Primary: 28-day sessions per user, with the CUPED-adjusted difference and its interval.
- Variance reduction = 1 - (SE adjusted / SE unadjusted)^2, about rho^2 for one covariate.
- Check: adjusted minus unadjusted point estimate, and covariate balance between arms.
- Guardrail: coverage in an A/A test (should be about 95%).

**Risks:**
- Post-treatment covariates (anything measured after assignment that treatment can move) break CUPED, and so does any covariate that is a proxy for the outcome.
- Early-days data can include novelty, so the early effect and the 28-day effect can differ in sign.
- Too many covariates can overfit with small samples.
- Dropping users without history changes the population.

**What the interviewer scores:**
- Strong: names the rule (covariate fixed before assignment) and explains why 0.9 correlation is not enough.
- Strong: gives the direction with reasoning (effect on Y minus theta x effect on X) and the fix.
- Strong: notes the tight interval is what makes it dangerous.
- Weak: "a higher correlation is always better."
- Weak: says the estimate stays unbiased because randomization protects it.

**Example:** (illustrative numbers) 50,000 users per arm in the code. True effect on 28-day sessions +2.0. Treatment also raises 3-day sessions by 1.5. Unadjusted estimate 1.99 (SE 0.19, interval covers the truth in 95% of runs). CUPED with early sessions: 0.62 (SE 0.07), and the interval covers the truth in 0% of runs. CUPED with pre-experiment sessions: 2.00 (SE 0.07), coverage 94%. Weak answer: "correlation 0.9 gives the biggest variance reduction." Strong answer: "that covariate is post-treatment; I would use the 28 days before launch and compare with the unadjusted number."

**Code:**
```python
# Q42: CUPED with a post-treatment covariate (first 3 days of the experiment). Illustrative, seeded.
import numpy as np

rho = 0.9
print("variance kept with covariate correlation 0.9:", round(1 - rho**2, 2), " -> SE shrinks to", round(np.sqrt(1 - rho**2), 2), "of its size")
assert round(1 - rho**2, 2) == 0.19 and round(np.sqrt(1 - rho**2), 2) == 0.44

rng = np.random.default_rng(42)
n = 50_000
TAU_Y, TAU_X = 2.0, 1.5     # true effect on 28-day sessions; treatment also raises early (3-day) sessions by 1.5

def sim(n, reps):
    out = {"naive": [], "bad": [], "good": []}
    se = {"naive": [], "bad": [], "good": []}
    for _ in range(reps):
        T = rng.integers(0, 2, n)
        L = rng.normal(100, 20, n)                           # latent engagement
        pre = L + rng.normal(0, 6, n)                        # sessions in the 28 days BEFORE the test
        early = L + rng.normal(0, 6, n) + TAU_X * T          # sessions in the first 3 days (post-treatment)
        Y = L + rng.normal(0, 6, n) + TAU_Y * T              # 28-day sessions
        for name, x in (("naive", None), ("bad", early), ("good", pre)):
            if x is None:
                a, b = Y[T == 1], Y[T == 0]
                est = a.mean() - b.mean(); s = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
            else:
                th = np.cov(Y, x)[0, 1] / x.var(ddof=1)      # pooled theta, the standard CUPED recipe
                Z = Y - th * (x - x.mean())
                a, b = Z[T == 1], Z[T == 0]
                est = a.mean() - b.mean(); s = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
            out[name].append(est); se[name].append(s)
    return {k: (np.mean(v), np.mean(se[k]), np.mean([abs(e - TAU_Y) < 1.96 * s for e, s in zip(v, se[k])])) for k, v in out.items()}

res = sim(n, 100)
Tt = rng.integers(0, 2, n); L = rng.normal(100, 20, n)
print("corr(early, 28-day) in the simulation ~",
      round(np.corrcoef(L + rng.normal(0, 6, n), L + rng.normal(0, 6, n))[0, 1], 2))
print(f"true effect on 28-day sessions: {TAU_Y}")
for k, (m, s, cov) in res.items():
    print(f"{k:6s} mean estimate {m:5.2f}   mean SE {s:.3f}   95% CI covers the truth in {cov:.0%} of runs")
assert abs(res["naive"][0] - TAU_Y) < 0.1 and abs(res["good"][0] - TAU_Y) < 0.1
assert res["bad"][0] < TAU_Y - 0.8                           # biased toward zero
assert res["bad"][1] < res["naive"][1] and res["good"][1] < res["naive"][1]
assert res["bad"][2] < 0.5 and res["naive"][2] > 0.9
```

**Output (my run):**
```text
variance kept with covariate correlation 0.9: 0.19  -> SE shrinks to 0.44 of its size
corr(early, 28-day) in the simulation ~ 0.92
true effect on 28-day sessions: 2.0
naive  mean estimate  1.99   mean SE 0.187   95% CI covers the truth in 95% of runs
bad    mean estimate  0.62   mean SE 0.074   95% CI covers the truth in 0% of runs
good   mean estimate  2.00   mean SE 0.074   95% CI covers the truth in 94% of runs
```
The latent-engagement model and noise sizes are invented. The bias formula (effect on Y minus theta times effect on X, with theta close to 0.9 in this setup) is what the output confirms: 2.0 - about 0.9 x 1.5 is about 0.65, and the run gives 0.62.

**Follow-ups:**
- Can I use first-3-days data at all? As a segmentation or novelty diagnostic, yes; as a CUPED covariate, no. See Q9 in this part (CUPED with pre-experiment spend).
- What if the pre-period is short for new users? Use pre-period data where it exists, and for users without it use a constant (the mean) with an indicator, so they get no adjustment.

**Common mistakes:** Choosing the covariate by correlation alone. Using data from after assignment. Not comparing adjusted and unadjusted estimates. Trusting a narrower interval as proof the method worked. Not A/A testing the pipeline.

### Q43 ⭐⭐ 🔴 In an experiment with 50,000 users per arm the overall split is exactly 50/50, so the SRM check passes. By platform, control has 20,000 iOS and 30,000 Android users while treatment has 16,000 iOS and 34,000 Android users. Explain what this means, why the overall check missed it, and what you do with the result.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The overall split is exactly 50/50, but the platform mix is 40% iOS in control and 32% in treatment, which is a very large sample-ratio mismatch inside platforms, so the experiment is broken and I would not read any result until I find the cause.

**Clarifying questions:**
- Wording check: do the arms hold 100,000 users each, or 50,000 each? Why: the platform numbers add to 50,000 per arm (100,000 in all), so the prompt's "100,000 users per arm" does not match; I would confirm which is true, since the logic below does not change.
- Was assignment designed to be 50/50 within each platform, or only overall? Why: it decides what the expected counts are in each cell.
- Where does a user get counted: at assignment, or at the first event after exposure? Why: counting on the first event lets a platform-specific crash or logging gap remove users from one arm.
- Did the treatment ship in a different app version, or a different build for iOS? Why: a version split is a common cause.
- Any exclusion rules (bots, eligibility filters) applied after assignment? Why: a filter that treats the arms or platforms differently creates the imbalance.

**Approach:**
1. Compute the check per platform, not just overall. iOS: 20,000 versus 16,000 has an expected 18,000 in each arm, chi-square = 444. Android: 30,000 versus 34,000, expected 32,000, chi-square = 250. Overall: 50,000 versus 50,000, chi-square = 0.
2. Explain why the overall test passed. The iOS shortfall in treatment (4,000) is exactly offset by an Android surplus (4,000), so the totals match. The SRM check on the total only sees the total. A check on a mix (platform by arm) sees the problem: chi-square about 694.
3. Treat the equality of totals as a coincidence or a symptom, not as comfort. Possible causes: iOS users in treatment are being dropped (crash, slow load, a missing event), or are being reassigned or shown on another platform, or an eligibility filter works differently by arm.
4. Quantify what it does: if iOS converts at 8% and Android at 4% in both arms and treatment does nothing, pooled conversion is 5.60% versus 5.28%, a fake drop of 0.32 points (5.7% relative), with z of about -2.2 at 50,000 per arm (it would grow with sample size). The mix shift alone makes the test look like a loser.
5. Investigate: trace the funnel per platform (assignment, exposure, first event), compare app versions, look at crash and error logs, check the assignment service by platform, and look for a bucketing change.
6. Decide: do not ship on this data. If the cause is a logging or exposure bug, fix and rerun. A within-platform comparison can be shown as a diagnostic, but it is only valid if the missing users are missing at random, which I cannot assume.

**Metrics:**
- SRM per cell = (observed - expected)^2 / expected, summed over arms, with p-value from chi-square (1 degree of freedom per two-arm cell). Use a strict threshold (for example p < 0.001) because it is a check run on many tests and many segments.
- Platform share per arm = users on the platform / users in the arm (40% versus 32% for iOS).
- Guardrails: assignment-to-exposure rate per platform and arm; crash rate; app version mix per arm.

**Risks:**
- Reweighting to the control mix hides the problem and only fixes the part you can see.
- The missing iOS users in treatment are likely not a random sample (the ones who crash or leave early), so even within iOS the arms are not comparable.
- Running SRM checks on many segments produces false alarms; use a strict threshold and look at the size of the gap, not only the p-value.
- Totals that match can create false confidence in dashboards that only check the total.

**What the interviewer scores:**
- Strong: runs the check by segment and explains why the total hid it (offsetting gaps).
- Strong: shows what the mix shift does to the metric with numbers.
- Strong: refuses to ship, finds the cause, reruns if needed.
- Weak: "SRM passed, so the test is valid."
- Weak: reweights and reports the result as if fixed.

**Example:** (illustrative numbers, from the prompt) iOS 20,000 versus 16,000: chi-square 444. Android 30,000 versus 34,000: chi-square 250. Total 50,000 versus 50,000: chi-square 0. With conversion 8% iOS and 4% Android in both arms, control pools to 5.60% and treatment to 5.28%. Weak answer: "overall split is exactly 50/50 so there is no SRM." Strong answer: "the platform mix differs by 8 points; that is a broken assignment or logging path, and the pooled result is not trustworthy."

**Code:**
```python
# Q43: overall 50/50 passes SRM but iOS and Android are lopsided. Illustrative, seeded.
import numpy as np
from scipy import stats

ctl = {"iOS": 20_000, "Android": 30_000}
trt = {"iOS": 16_000, "Android": 34_000}
nc, nt = sum(ctl.values()), sum(trt.values())
print("users per arm: control", nc, " treatment", nt, " (the prompt says 100,000 per arm; these add to 50,000 per arm, 100,000 in all)")
assert nc == 50_000 and nt == 50_000

def srm(c, t):
    exp = (c + t) / 2
    chi = (c - exp) ** 2 / exp + (t - exp) ** 2 / exp
    return chi, stats.chi2.sf(chi, 1)

print("overall: chi2 = %.1f p = %.3f" % srm(nc, nt))
for p in ctl:
    chi, pv = srm(ctl[p], trt[p])
    print(f"{p}: {ctl[p]} vs {trt[p]}  chi2 = {chi:.1f}  p = {pv:.2e}")
assert srm(nc, nt)[0] == 0
assert round(srm(20_000, 16_000)[0], 1) == 444.4 and round(srm(30_000, 34_000)[0], 1) == 250.0

# the real question: is platform mix the same in the two arms?
table = np.array([[20_000, 30_000], [16_000, 34_000]])
chi, p, dof, _ = stats.chi2_contingency(table, correction=False)
print(f"platform x arm independence: chi2 = {chi:.1f}, dof {dof}, p = {p:.1e}; iOS share control {20/50:.0%} vs treatment {16/50:.0%}")
assert round(chi, 1) == 694.4

# what it does to the pooled metric even if treatment does nothing: iOS converts 8%, Android 4% in BOTH arms
rate = {"iOS": 0.08, "Android": 0.04}
pc = sum(ctl[k] * rate[k] for k in ctl) / nc
pt = sum(trt[k] * rate[k] for k in trt) / nt
print(f"true effect 0, pooled conversion control {pc:.2%} vs treatment {pt:.2%}: fake change {pt-pc:+.2%} points ({pt/pc-1:+.1%} relative)")
assert round(pc, 4) == 0.056 and round(pt, 4) == 0.0528
se = np.sqrt(pc*(1-pc)/nc + pt*(1-pt)/nt)
print(f"z for that fake change = {(pt-pc)/se:.1f}")
assert 2.0 < abs((pt - pc) / se) < 2.5
# a platform-adjusted comparison (stratified) removes the compositional part
```

**Output (my run):**
```text
users per arm: control 50000  treatment 50000  (the prompt says 100,000 per arm; these add to 50,000 per arm, 100,000 in all)
overall: chi2 = 0.0 p = 1.000
iOS: 20000 vs 16000  chi2 = 444.4  p = 1.17e-98
Android: 30000 vs 34000  chi2 = 250.0  p = 2.60e-56
platform x arm independence: chi2 = 694.4, dof 1, p = 4.8e-153; iOS share control 40% vs treatment 32%
true effect 0, pooled conversion control 5.60% vs treatment 5.28%: fake change -0.32% points (-5.7% relative)
z for that fake change = -2.2
```
The conversion rates are invented. The SRM numbers come straight from the prompt's counts.

**Follow-ups:**
- Could this be allowed if the product behaves differently by platform? No: assignment happens before the product shows anything, so the arms should have the same platform mix. If only exposed users are counted, a platform-specific exposure change can cause it, and then the metric must be reported with the exposure rule. See Q1 in this part (an SRM on 52,000 versus 48,000) and Book 1 Part 10 Q6 (what SRM is).
- How many segments should I check? The ones that could differ by arm (platform, country, app version, new versus returning), with a strict threshold.

**Common mistakes:** Checking SRM on the total only. Reweighting instead of finding the cause. Treating a tiny p-value as the only information. Ignoring the sign and size of the imbalance. Shipping while the cause is unknown.

### Q44 ⭐ 🟡 A team ran 8 variants of a landing page against one control, picked the best (+4% conversion relative to control, p = 0.02) and shipped it, and a follow-up re-test of that variant alone shows +1.5% relative. Explain the winner's curse, how to estimate the true effect of the chosen variant and how you would design such tests.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
**Say this first (1 line):** Picking the best of 8 noisy results selects the lucky one, so +4% overstates the true effect, and a fresh re-test of +1.5% is the honest number; I would shrink the estimate, confirm on new data, and use a multiple-comparison method next time.

**Clarifying questions:**
- Was p = 0.02 corrected for 8 variants, or is it the raw p-value for the winner against control? Why: raw means it is nearly worthless as evidence after selection.
- Was the choice of variants and metric fixed before the test? Why: post-hoc picking adds more selection.
- How large was the re-test and how long? Why: its interval tells me whether +1.5% differs from +4% or from zero.
- Was the re-test on a similar period and audience? Why: seasonal or novelty differences also move the estimate.
- What is the cost of a wrong ship here (a page the team must maintain, a brand change)? Why: it sets how much evidence I need.

**Approach:**
1. Explain the winner's curse. Each estimate is true effect plus noise. The largest of 8 estimates tends to carry a big positive noise term, so the selected variant's estimate is biased upward. The more variants and the noisier each one, the larger the bias.
2. Do the arithmetic on the evidence. +4% at p = 0.02 means a standard error of about 1.7% (z = 2.33). The p-value for the best of 8 should be adjusted: 8 x 0.02 = 0.16 (Bonferroni), and with 8 true nulls the chance of at least one p below 0.05 is 1 - 0.95^8 = 34%. So "p = 0.02" does not clear the bar.
3. Read the re-test. +1.5% with the same standard error has an interval from about -1.9% to +4.9%, and the difference from +4% is about 1.0 standard errors. The two results are consistent with a modest true effect and luck in the first.
4. Estimate the true effect of the chosen variant: use the fresh re-test (unbiased because the variant was chosen before it), or shrink the first-round estimates toward the average of all 8 (empirical Bayes) and combine with the re-test.
5. Decide on the new estimate and its interval: is +1.5% (interval -1.9% to +4.9%) enough for the cost? Probably continue the re-test or collect more data.
6. Design next time: fewer, better variants; a multiple-comparison correction against a shared control (Dunnett or Holm); split the data (choose the winner on part of the traffic, confirm on the rest); pre-registered primary metric; and report shrunk estimates for all variants.

**Metrics:**
- Per variant: relative lift = (conversion variant / conversion control) - 1, with its interval.
- Family-wise error rate = probability of at least one false win across the 8 comparisons (34% unadjusted at 0.05, about 5% with Bonferroni at 0.05/8).
- Winner's-curse bias = mean (estimate of the selected variant - its true effect); in my simulation about +1.8 points.
- Guardrails: confirm on a fresh sample; track the live lift after launch.

**Risks:**
- Shipping on the selected estimate and planning revenue around +4%.
- Shrinkage needs a prior; with only 8 variants the estimated spread is itself noisy.
- A re-test run right after the first one can have its own novelty or seasonality.
- Correcting for 8 comparisons costs power: some true winners are missed.

**What the interviewer scores:**
- Strong: explains selection bias in plain words and shows the p-value is not valid after picking the max.
- Strong: gives a way to estimate the true effect (fresh re-test, shrinkage) with numbers.
- Strong: proposes a design change (correction, split-sample confirm, fewer variants).
- Weak: "the re-test is just noise, the first test was bigger."
- Weak: "regression to the mean" with no mechanism or fix.

**Example:** (illustrative numbers) 5% baseline conversion, about 128,000 users per arm gives a standard error of 1.7% on the relative lift. Simulation: true effects spread as N(0, 1.5%) across 8 variants. The selected winner's average estimate is +3.3% but its average true effect is +1.4%, an overstatement of +1.8 points; among winners whose estimate is near +4%, the mean true effect is +1.8%. Shrinking toward the group mean removes the bias (average error -0.1 points) and reduces the root mean squared error from 2.3% to 1.5%. A fresh test of the chosen variant is unbiased (+1.4%). Weak answer: "+4% with p = 0.02, ship and plan for 4%." Strong answer: "plan for about 1.5%, and confirm on fresh traffic."

**Code:**
```python
# Q44: 8 variants vs control, best looks +4% (p = 0.02), re-test says +1.5%. Illustrative, seeded.
import numpy as np
from scipy import stats

base = 0.05
z = stats.norm.isf(0.02 / 2)
se_rel = 0.04 / z                                  # SE of the relative lift implied by +4% at p = 0.02
n_arm = 2 * base * (1 - base) / (se_rel * base) ** 2
print(f"+4% at p = 0.02 implies z = {z:.2f}, SE of relative lift {se_rel:.2%}, about {n_arm:,.0f} users per arm")
assert abs(z - 2.326) < 0.01 and 120_000 < n_arm < 135_000
print(f"Bonferroni p for 8 variants: {min(1, 0.02*8):.2f};  chance of >= 1 p<0.05 among 8 true nulls: {1-0.95**8:.1%}")
assert round(0.02 * 8, 2) == 0.16 and round(1 - 0.95 ** 8, 3) == 0.337
# does the re-test contradict the first estimate?
dz = (0.04 - 0.015) / np.sqrt(2) / se_rel
print(f"re-test +1.5% with the same SE: z for the difference {dz:.2f}; the re-test 95% CI is [{(0.015-1.96*se_rel):+.1%}, {(0.015+1.96*se_rel):+.1%}]")
assert dz < 1.5

rng = np.random.default_rng(44)
R, K, TAU = 20_000, 8, 0.015                        # true relative effects ~ N(0, 1.5%)
true = rng.normal(0, TAU, (R, K))
est = true + rng.normal(0, se_rel, (R, K))
best = est.argmax(1); idx = np.arange(R)
w_est, w_true = est[idx, best], true[idx, best]
print(f"winner: mean estimate {w_est.mean():+.2%}, mean true effect {w_true.mean():+.2%}, overstatement {w_est.mean()-w_true.mean():+.2%}")
assert w_est.mean() > w_true.mean() + 0.01
# winners that look like ours
sel = (w_est > 0.035) & (w_est < 0.045)
print(f"winners with estimate near +4%: {sel.sum()}; their mean true effect {w_true[sel].mean():+.2%}")
assert 0.0 < w_true[sel].mean() < 0.025
# empirical-Bayes shrinkage: prior variance from the 8 estimates in each experiment
shr_err, raw_err = [], []
for r in range(R):
    e = est[r]; v = max(e.var(ddof=1) - se_rel ** 2, 1e-8)
    b = v / (v + se_rel ** 2)
    post = e.mean() + b * (e - e.mean())
    shr_err.append(post[best[r]] - true[r, best[r]]); raw_err.append(e[best[r]] - true[r, best[r]])
print(f"mean error of winner: raw {np.mean(raw_err):+.2%}, shrunk {np.mean(shr_err):+.2%};  RMSE raw {np.sqrt(np.mean(np.square(raw_err))):.2%} vs shrunk {np.sqrt(np.mean(np.square(shr_err))):.2%}")
assert abs(np.mean(shr_err)) < abs(np.mean(raw_err)) / 2
# share of experiments in which the winner's re-test is >= 0 and its fresh estimate vs truth
fresh = true[idx, best] + rng.normal(0, se_rel, R)
print(f"fresh re-test of the winner: mean {fresh.mean():+.2%} (unbiased for its true effect {w_true.mean():+.2%})")
assert abs(fresh.mean() - w_true.mean()) < 0.001
```

**Output (my run):**
```text
+4% at p = 0.02 implies z = 2.33, SE of relative lift 1.72%, about 128,532 users per arm
Bonferroni p for 8 variants: 0.16;  chance of >= 1 p<0.05 among 8 true nulls: 33.7%
re-test +1.5% with the same SE: z for the difference 1.03; the re-test 95% CI is [-1.9%, +4.9%]
winner: mean estimate +3.26%, mean true effect +1.42%, overstatement +1.84%
winners with estimate near +4%: 4504; their mean true effect +1.75%
mean error of winner: raw +1.84%, shrunk -0.08%;  RMSE raw 2.30% vs shrunk 1.48%
fresh re-test of the winner: mean +1.41% (unbiased for its true effect +1.42%)
```
The spread of true effects (1.5%) is invented; with a wider or narrower spread the overstatement changes. The empirical-Bayes step uses only the 8 estimates in each simulated test, as a team would have.

**Follow-ups:**
- Why is the re-test unbiased? The variant was chosen before the re-test data existed, so the noise in the new data is independent of the choice. See Q23 in this part (one control with 4 variants) and Book 1 Part 10 Q9 (multiple testing).
- Does this apply to dashboards with many metrics? Yes, picking the one metric that moved has the same selection bias.

**Common mistakes:** Treating the selected variant's p-value as if it were the only test. Planning on the first estimate. Using more variants to "find a winner". Not confirming on fresh data. Calling the gap between +4% and +1.5% a real decline in effect.

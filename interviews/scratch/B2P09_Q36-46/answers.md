### Q36 ⭐⭐ 🟡 Capability evals vs regression evals: how does an eval suite mature over time (graduating cases, saturation, adding harder tasks, eval-driven development)? See Part 8 Q14, Q39 and Q51 for agent evaluation.
**Asked at:** product, GenAI startups, senior roles
**Say this first (1 line):** A capability eval asks "what can the model not do yet?" and is expected to fail a lot; a regression eval asks "did anything that used to work break?" and is expected to pass almost always; a healthy suite moves stable cases from the first to the second and keeps adding harder cases.
**Then explain:**
- **Two jobs, two shapes.** Capability evals start at a low pass rate and give the team a hill to climb. Regression evals start near 100% and act as a smoke alarm. Anthropic's engineering post on agent evals (opened) draws the same split and also suggests starting with 20-50 tasks taken from real failures.
- **Graduation.** When a capability case passes reliably (here: 5 of 5 trials), copy it into the regression suite. Graduating on repeated trials, not one lucky pass, matters because of run variance (Part 9 Q27).
- **Saturation.** When the capability suite is nearly all passes, it no longer separates versions. The fix is new, harder cases drawn from fresh production failures, not a bigger pile of easy ones. Saturation also hurts public benchmarks (Part 9 Q21).
- **Regression gates must tolerate noise.** A strict "every case 5/5" gate will fail healthy candidates because borderline cases flicker (see the run). Gate on a drop in the aggregate, plus any case that now fails most trials; thresholds and flaky handling are in Part 9 Q14.
- **Eval-driven development.** Write the failing eval first (from a bug report or a new requirement), then change the prompt or model until it passes, then graduate it. The cases are the specification.
- **Agent suites** (trajectories, tool mocks, pass^k) are covered in Part 8 Q14, Q39 and Q51; this answer is the general lifecycle.
**Example:** (SYNTHETIC mock, no LLM). 60 cases of rising difficulty. Skill goes 1.0 to 8.0 over five versions. The capability pass rate on the remaining cases goes 0.37, 0.46, 0.67, 0.81, 0.97 while the graduated regression suite grows 7, 15, 27, 41, 57. At v5 the capability suite is at 0.97 with only a few cases left, so it is saturated and 20 harder cases are added. Then a candidate that breaks one block of 10 cases is tested: the strict 5/5 gate fails both the healthy candidate (2 flaky cases) and the broken one (12 cases, 10 of them in the broken block); the looser "any case at 2 of 5 or worse" gate passes the healthy candidate and fails the broken one (10 cases). One toy run with one seed, so read the shape, not the counts. Also, per Anthropic's post, 75% per-trial success gives about 42% pass^3, which the run confirms (0.75^3 = 0.4219).
**Code:** (run with `python3 -I`; stdlib only; mock model, synthetic cases)
```python
# TOY (synthetic) eval-suite lifecycle: capability suite -> graduate stable passes to a regression suite -> saturation -> add harder cases.
# The "model" is a mock: P(pass) = logistic(skill - difficulty). No LLM, no network.
import math, random
random.seed(7)
def p_pass(skill, diff): return 1 / (1 + math.exp(-(skill - diff)))
def run(skill, cases, trials=5):
    return {cid: sum(random.random() < p_pass(skill, d) for _ in range(trials)) for cid, d in cases.items()}
# v1 suite: 60 cases, difficulty from -1 (easy) to 5 (hard)
suite = {f"c{i:02d}": -1 + 6 * i / 59 for i in range(60)}
regression, capability = {}, dict(suite)
print("version  skill  capability_cases  mean_pass(cap)  graduated_total")
for ver, skill in [("v1", 1.0), ("v2", 2.0), ("v3", 3.5), ("v4", 5.0), ("v5", 8.0)]:
    res = run(skill, capability)
    mean = sum(res.values()) / (5 * len(capability))
    grads = [c for c, k in res.items() if k == 5]          # passed 5/5 trials -> stable -> graduate
    for c in grads: regression[c] = capability.pop(c)
    print(f"{ver}      {skill:4.1f}   {len(capability)+len(grads):3d}               {mean:5.2f}           {len(regression):3d}")
    if mean > 0.9 and len(capability) < 15:             # saturated: add harder tasks
        for j in range(20): capability[f"h{j:02d}"] = 5 + 3 * j / 19
        print(f"        capability suite near saturation (mean {mean:.2f}); added 20 harder cases")
# regression run: candidate keeps skill 8 overall; the "bad" one breaks one category (cases c10-c19). Gate = fail if any case is not 5/5.
def cand_run(cases, broken_block, trials=5):
    out = {}
    for cid, d in cases.items():
        s = 8.0 - (9.0 if broken_block and "c10" <= cid <= "c19" else 0)
        out[cid] = sum(random.random() < p_pass(s, d) for _ in range(trials))
    return out
for label, brk in [("healthy candidate", False), ("candidate that breaks c10-c19", True)]:
    res = cand_run(regression, brk)
    bad = sorted(c for c, k in res.items() if k < 5)
    in_block = sum("c10" <= c <= "c19" for c in bad)
    hard_fail = sorted(c for c, k in res.items() if k <= 2)       # looser gate: a case failing at least 3 of 5 trials
    print(f"{label:30} regression cases {len(regression)}; not 5/5: {len(bad)} (in c10-c19: {in_block}) -> strict gate {'FAIL' if bad else 'PASS'}; "
          f"cases passing <=2/5: {len(hard_fail)} -> loose gate {'FAIL' if hard_fail else 'PASS'}")
print("pass^3 check, 75% per-trial success:", round(0.75 ** 3, 4), "(0.75^3 = 0.421875)")
```
**Output (my run):**
```
version  skill  capability_cases  mean_pass(cap)  graduated_total
v1       1.0    60                0.37             7
v2       2.0    53                0.46            15
v3       3.5    45                0.67            27
v4       5.0    33                0.81            41
v5       8.0    19                0.97            57
        capability suite near saturation (mean 0.97); added 20 harder cases
healthy candidate              regression cases 57; not 5/5: 2 (in c10-c19: 0) -> strict gate FAIL; cases passing <=2/5: 0 -> loose gate PASS
candidate that breaks c10-c19  regression cases 57; not 5/5: 12 (in c10-c19: 10) -> strict gate FAIL; cases passing <=2/5: 10 -> loose gate FAIL
pass^3 check, 75% per-trial success: 0.4219 (0.75^3 = 0.421875)
```
**Follow-ups:**
- *Should graduated cases ever leave?* Yes. Retire cases whose requirement changed, and re-label cases a human finds wrong; version the suite so old runs stay comparable (Part 9 Q2).
- *How many regression cases?* Enough to cover each important behaviour and each past incident, and small enough to run on every change; tiering (fast on every commit, full nightly) is Part 9 Q14.
- *What if the capability score never moves?* Either the cases are too hard to give a signal, or the changes you try do not address the failure mode; go back to error analysis (Part 9 Q15).
**Common mistakes:** one suite for everything; graduating on a single pass; a strict all-pass gate that cries wolf and gets switched off; never adding harder cases so the dashboard shows 100% and nobody learns anything; treating a public benchmark as your capability suite.

### Q37 ⭐ 🟡 Code: implement Elo ratings and a Bradley-Terry fit from pairwise battle results, and show why order matters for Elo but not for the Bradley-Terry fit.
**Asked at:** product, big tech, research-leaning teams, live-coding rounds
**Say this first (1 line):** Elo updates ratings one battle at a time, so the final numbers depend on the order of the battles; Bradley-Terry fits all battles at once by maximum likelihood, so the order cannot matter.
**Then explain:**
- **Elo:** expected win probability for A is 1 / (1 + 10^((rB - rA)/400)); after each battle move each rating by K x (result - expected). Because every update uses the current ratings, a model that happens to win late ends higher.
- **Bradley-Terry:** each model has a strength p; P(A beats B) = pA / (pA + pB). The data are only the win counts per pair, so shuffling battles changes nothing. I fit it with the MM iteration: p_i = wins_i / sum over opponents of n_ij / (p_i + p_j), then rescale.
- **Checks I ran:** at the solution wins minus expected wins is 0 for every model (that is the likelihood condition), and for two models the fit matches the closed form 400 x log10(wins / losses).
- **When Elo is fine:** a stream where models truly change over time (a recency effect is then a feature). For a static leaderboard from a fixed pile of votes, BT is the cleaner choice. Per LMSYS blog snippets (not opened in full, check the live posts), the Arena moved from online Elo to a Bradley-Terry fit for this reason; see Part 9 Q20 for the Arena's intervals and blind spots.
**Example:** two battles, K = 32, both models start at 1000. A beats B, then B beats A: A ends at 998.53 and B at 1001.47. Swap the order and A ends at 1001.47, B at 998.53. Same two results, different ratings. On 600 synthetic battles (assumed true strengths A 1.8, B 1.2, C 1.0, D 0.5; K = 16) Elo gives A = 1112.1 on the original order, 1170.0 reversed, 1399.1 when A's wins are pushed to the end and 763.4 when they come first (those last two are deliberately adversarial orders). Bradley-Terry gives A = 1115.5, B = 1043.7, C = 999.2, D = 841.5 every time.
**Code:** (run with `python3 -I`; stdlib only; synthetic battles)
```python
# Elo (online, order-dependent) vs Bradley-Terry (batch MLE, order-free) on synthetic pairwise battles.
import math, random
def elo(battles, K=16, base=1000.0):
    r = {}
    for a, b, w in battles:                     # w = 1 if a wins, 0 if b wins
        ra, rb = r.setdefault(a, base), r.setdefault(b, base)
        ea = 1 / (1 + 10 ** ((rb - ra) / 400))
        r[a] = ra + K * (w - ea); r[b] = rb + K * ((1 - w) - (1 - ea))
    return r
def bt_fit(battles, iters=500):
    """MM algorithm (Zermelo/Hunter). strengths p_i; P(i beats j)=p_i/(p_i+p_j). Returns Elo-scale ratings, mean 1000."""
    models = sorted({m for a, b, _ in battles for m in (a, b)})
    wins = {m: 0 for m in models}; n = {}
    for a, b, w in battles:
        wins[a if w else b] += 1
        k = tuple(sorted((a, b))); n[k] = n.get(k, 0) + 1
    p = {m: 1.0 for m in models}
    for _ in range(iters):
        new = {}
        for i in models:
            den = sum(n[tuple(sorted((i, j)))] / (p[i] + p[j]) for j in models if j != i and tuple(sorted((i, j))) in n)
            new[i] = wins[i] / den
        g = math.exp(sum(math.log(v) for v in new.values()) / len(new))
        p = {m: v / g for m, v in new.items()}
    r = {m: 400 * math.log10(v) for m, v in p.items()}
    mu = sum(r.values()) / len(r)
    return {m: 1000 + r[m] - mu for m in models}, p, wins, n
# 1) two battles, hand-checkable: same data, two orders
print("two battles, K=32:")
for order in ([("A", "B", 1), ("B", "A", 1)], [("B", "A", 1), ("A", "B", 1)]):
    r = elo(order, K=32); print("  ", [(a, b, 'first wins') for a, b, _ in order], "->", {k: round(v, 2) for k, v in r.items()})
# 2) 600 synthetic battles, true strengths known (assumed inputs)
random.seed(11)
true = {"A": 1.8, "B": 1.2, "C": 1.0, "D": 0.5}
pairs = [(a, b) for a in true for b in true if a < b]
battles = []
for _ in range(600):
    a, b = random.choice(pairs)
    battles.append((a, b, int(random.random() < true[a] / (true[a] + true[b]))))
bt, p, wins, n = bt_fit(battles)
print("\nBT ratings (original order):", {k: round(v, 1) for k, v in bt.items()})
orders = {"original": battles[:], "reversed": battles[::-1],
          "A-wins-last": sorted(battles, key=lambda x: (x[2] == 1 and x[0] == 'A')),
          "A-wins-first": sorted(battles, key=lambda x: (x[2] == 0 or x[0] != 'A'))}
print("\norder           Elo(A) Elo(B) Elo(C) Elo(D)  BT(A)   BT(B)   BT(C)   BT(D)")
for name, o in orders.items():
    e = elo(o); b2 = bt_fit(o)[0]
    print(f"{name:14} " + " ".join(f"{e[m]:6.1f}" for m in "ABCD") + "  " + " ".join(f"{b2[m]:6.1f}" for m in "ABCD"))
# 3) check BT: gradient of log-likelihood is ~0 at the solution (MLE), and a closed form for 2 models
g = max(abs(wins[i] - sum(n[tuple(sorted((i, j)))] * p[i] / (p[i] + p[j]) for j in p if j != i)) for i in p)
print("\nmax |wins_i - expected wins_i| at BT solution:", f"{g:.2e}")
two = [("X", "Y", 1)] * 30 + [("X", "Y", 0)] * 10
r2 = bt_fit(two)[0]
print("two models, X wins 30 of 40: BT gap", round(r2["X"] - r2["Y"], 3), " closed form 400*log10(30/10) =", round(400 * math.log10(3), 3))
```
**Output (my run):**
```
two battles, K=32:
   [('A', 'B', 'first wins'), ('B', 'A', 'first wins')] -> {'A': 998.53, 'B': 1001.47}
   [('B', 'A', 'first wins'), ('A', 'B', 'first wins')] -> {'B': 998.53, 'A': 1001.47}

BT ratings (original order): {'A': 1115.5, 'B': 1043.7, 'C': 999.2, 'D': 841.5}

order           Elo(A) Elo(B) Elo(C) Elo(D)  BT(A)   BT(B)   BT(C)   BT(D)
original       1112.1 1029.7  969.8  888.4  1115.5 1043.7  999.2  841.5
reversed       1170.0  995.5 1031.0  803.5  1115.5 1043.7  999.2  841.5
A-wins-last    1399.1  862.2  910.7  828.0  1115.5 1043.7  999.2  841.5
A-wins-first    763.4 1132.6 1095.8 1008.2  1115.5 1043.7  999.2  841.5

max |wins_i - expected wins_i| at BT solution: 0.00e+00
two models, X wins 30 of 40: BT gap 190.849  closed form 400*log10(30/10) = 190.849
```
**Follow-ups:**
- *How do you get error bars on BT?* Bootstrap the battles (resample votes, refit) and take percentiles; Part 9 Q38 has the bootstrap machinery.
- *Ties?* Count a tie as half a win for each side, or model ties explicitly; I did not implement ties here.
- *Why 400 and 10?* Convention only; it sets the scale so a 400-point gap means 10 to 1 odds.
**Common mistakes:** quoting an Elo gap from one ordering as if it were stable; no shuffling or averaging when using Elo; forgetting BT is only identified up to a constant (so centre the ratings); fitting BT when some model has zero wins (the MLE diverges, so regularise); treating Arena-style rankings as a measure of your product's quality.

### Q38 ⭐ 🟡 Code: implement a bootstrap confidence interval for accuracy and a paired bootstrap for the difference between two systems.
**Asked at:** product, big tech, evaluation-focused rounds, live-coding rounds
**Say this first (1 line):** Resample the test cases with replacement many times, recompute accuracy each time, and take the 2.5th and 97.5th percentiles; for two systems, resample the same cases for both and bootstrap the per-case difference.
**Then explain:**
- **The unit is the test case.** Each resample draws n cases with replacement. In the paired version each drawn case carries both systems' results, so the correlation between systems is kept.
- **Why paired is tighter:** the two systems usually fail on many of the same hard cases. Only the cases where they disagree carry information about the difference, so the paired interval is narrower than an unpaired one that pretends the two samples are independent.
- **Sanity checks:** for one accuracy the bootstrap half-width should be close to 1.96 x sqrt(p(1-p)/n); for the paired difference it should be close to 1.96 x sqrt(b + c - (b-c)^2 / n) / n, with b and c the counts of cases where only one system is right.
- **Limits:** it assumes the cases are independent draws. If several test cases come from one document or one user, resample the groups instead. It also says nothing about cases you never sampled. The "evals as experiments with error bars" paper by Miller (arXiv 2411.00640, abstract only opened) argues for reporting this kind of uncertainty.
- Sample size and power are Part 9 Q26; McNemar and other tests are Part 9 Q28; the worked 82% vs 80% scenario is Part 9 Q11.
**Example:** (SYNTHETIC outcomes, 200 cases, correlated systems). A is 0.820 accurate with a bootstrap 95% CI of [0.765, 0.870]. B is 0.740. The difference is +0.080. The paired bootstrap gives [+0.030, +0.130] (width 0.100); the unpaired one gives [+0.000, +0.160] (width 0.160), whose lower end sits at zero, so it would not clearly show a win. The check numbers match: normal approximation half-width 0.053 vs bootstrap 0.052 for A; closed-form 1.96 x SE = 0.049 vs bootstrap half-width 0.050 for the difference (A only right on 21 cases, B only on 5).
**Code:** (run with `python3 -I`; stdlib only; synthetic data)
```python
# Percentile bootstrap CI for accuracy, and paired bootstrap for A-B, on synthetic per-case 0/1 outcomes.
import random, math
random.seed(5)
n = 200
# synthetic (assumed): A and B correlated (B is correct on most cases A is)
A, B = [], []
for _ in range(n):
    easy = random.random() < 0.72
    a = 1 if easy or random.random() < 0.36 else 0
    b = 1 if (easy and random.random() < 0.97) or (not easy and random.random() < 0.28) else 0
    A.append(a); B.append(b)
def boot_ci(x, B_=10000, alpha=0.05, seed=1):
    r = random.Random(seed); m = len(x)
    stats = sorted(sum(x[r.randrange(m)] for _ in range(m)) / m for _ in range(B_))
    return stats[int(alpha / 2 * B_)], stats[int((1 - alpha / 2) * B_) - 1]
def paired_boot(a, b, B_=10000, seed=2):
    r = random.Random(seed); m = len(a); d = [x - y for x, y in zip(a, b)]
    stats = sorted(sum(d[r.randrange(m)] for _ in range(m)) / m for _ in range(B_))   # resample CASES, keep pairs together
    return sum(d) / m, stats[int(0.025 * B_)], stats[int(0.975 * B_) - 1]
def unpaired_boot(a, b, B_=10000, seed=3):
    r = random.Random(seed); m = len(a)
    stats = sorted(sum(a[r.randrange(m)] for _ in range(m)) / m - sum(b[r.randrange(m)] for _ in range(m)) / m for _ in range(B_))
    return stats[int(0.025 * B_)], stats[int(0.975 * B_) - 1]
pa, pb = sum(A) / n, sum(B) / n
lo, hi = boot_ci(A)
print(f"A accuracy {pa:.3f}  bootstrap 95% CI [{lo:.3f}, {hi:.3f}]  width {hi-lo:.3f}")
print(f"  normal-approx check: +-1.96*sqrt(p(1-p)/n) = {1.96*math.sqrt(pa*(1-pa)/n):.3f}  (half-width of bootstrap: {(hi-lo)/2:.3f})")
d, plo, phi = paired_boot(A, B)
ulo, uhi = unpaired_boot(A, B)
bc = sum(1 for a, b in zip(A, B) if a == 1 and b == 0); cc = sum(1 for a, b in zip(A, B) if a == 0 and b == 1)
print(f"B accuracy {pb:.3f}; diff A-B {d:+.3f}")
print(f"paired bootstrap 95% CI   [{plo:+.3f}, {phi:+.3f}]  width {phi-plo:.3f}")
print(f"unpaired bootstrap 95% CI [{ulo:+.3f}, {uhi:+.3f}]  width {uhi-ulo:.3f}   (wrongly ignores the pairing)")
se = math.sqrt(bc + cc - (bc - cc) ** 2 / n) / n
print(f"closed-form paired SE from discordant counts (A only right {bc}, B only right {cc}): {se:.4f}; 1.96*SE = {1.96*se:.3f} vs bootstrap half-width {(phi-plo)/2:.3f}")
print("CI excludes 0 (paired)?", plo > 0 or phi < 0, "| (unpaired)?", ulo > 0 or uhi < 0)
```
**Output (my run):**
```
A accuracy 0.820  bootstrap 95% CI [0.765, 0.870]  width 0.105
  normal-approx check: +-1.96*sqrt(p(1-p)/n) = 0.053  (half-width of bootstrap: 0.052)
B accuracy 0.740; diff A-B +0.080
paired bootstrap 95% CI   [+0.030, +0.130]  width 0.100
unpaired bootstrap 95% CI [+0.000, +0.160]  width 0.160   (wrongly ignores the pairing)
closed-form paired SE from discordant counts (A only right 21, B only right 5): 0.0249; 1.96*SE = 0.049 vs bootstrap half-width 0.050
CI excludes 0 (paired)? True | (unpaired)? False
```
**Follow-ups:**
- *How many resamples?* A few thousand is usual for a 95% interval; I used 10,000, which is cheap at this size.
- *Percentile vs BCa?* Percentile is fine for a first look; for small n or skewed statistics use BCa or an exact method (from memory, check a stats reference).
- *Multiple runs per case?* Average the trials within a case first, then bootstrap the cases (this is what Part 9 Q40 does).
**Common mistakes:** resampling individual trials instead of cases; the unpaired bootstrap on paired data; bootstrapping with tiny n and trusting the edges; reporting a CI for accuracy but a bare difference for the comparison; claiming "no difference" when the interval is just wide.

### Q39 ⭐ 🟡 Code: implement Cohen's kappa to measure agreement between an LLM judge and a human labeller, with TPR and TNR, and test it on toy labels.
**Asked at:** product, GenAI startups, evaluation-focused rounds, live-coding rounds
**Say this first (1 line):** Kappa is agreement between judge and human corrected for the agreement you would get by chance, and I always report it next to TPR and TNR because accuracy alone is misleading when one class dominates.
**Then explain:**
- **Formula:** kappa = (po - pe) / (1 - pe), where po is observed agreement and pe is the chance agreement from each rater's own label frequencies. 1 is perfect, 0 is chance level.
- **TPR and TNR with the human as reference:** TPR = share of human-good items the judge also calls good; TNR = share of human-bad items the judge also calls bad. They tell you which way the judge errs (too lenient or too strict), which kappa hides. This is the TPR/TNR practice from Hamel Husain's evals FAQ (opened).
- **Why accuracy misleads:** if 90% of outputs are good, a judge that always says "pass" scores about 90% accuracy and kappa 0.
- **Small samples are noisy.** TNR rests on the few bad items. Put a bootstrap interval on kappa.
- **Interpretation thresholds** (0.6 and 0.8 rules of thumb) are conventions, not laws; the full comparison of kappa variants and the kappa paradox is in Part 9 Q25, and judge calibration practice (splits, rubric iteration) is Part 9 Q6.
**Example:** (hand check) 15 true positives, 20 true negatives, 5 false positives, 10 false negatives: po = 35/50 = 0.70, pe = 0.5, kappa = 0.40, which the code reproduces. On synthetic data with 200 items and about 90% good, the always-pass judge and a realistic judge both score accuracy 0.915, but kappa is 0.000 for the lazy one and 0.540 for the realistic one (TPR 0.934, TNR 0.706; I designed it with TNR about 0.60, and with only 17 bad items the observed value wobbles). The bootstrap 95% CI for that kappa is [0.345, 0.719], which is wide.
**Code:** (run with `python3 -I`; stdlib only; toy labels)
```python
# Cohen's kappa + TPR/TNR for an LLM judge vs a human labeller. 1 = "good/pass", 0 = "bad/fail". Human = reference.
import random
def confusion(h, j):
    tp = sum(1 for x, y in zip(h, j) if x == 1 and y == 1); tn = sum(1 for x, y in zip(h, j) if x == 0 and y == 0)
    fp = sum(1 for x, y in zip(h, j) if x == 0 and y == 1); fn = sum(1 for x, y in zip(h, j) if x == 1 and y == 0)
    return tp, tn, fp, fn
def kappa(h, j):
    n = len(h); po = sum(x == y for x, y in zip(h, j)) / n
    pe = sum((sum(1 for x in h if x == c) / n) * (sum(1 for y in j if y == c) / n) for c in (0, 1))
    return (po - pe) / (1 - pe) if pe < 1 else float('nan')
def report(name, h, j):
    tp, tn, fp, fn = confusion(h, j)
    print(f"{name:34} n={len(h):3d} acc={(tp+tn)/len(h):.3f} TPR={tp/(tp+fn):.3f} TNR={tn/(tn+fp):.3f} kappa={kappa(h, j):.3f}")
# 1) hand-check: counts tp=15 tn=20 fp=5 fn=10 -> po=0.7, pe=0.5, kappa=0.4
h = [1]*15 + [0]*20 + [0]*5 + [1]*10; j = [1]*15 + [0]*20 + [1]*5 + [0]*10
report("hand-check (expect kappa 0.400)", h, j)
# 2) perfect and chance-level
report("identical labels", h, h)
random.seed(4)
rnd = [random.randint(0, 1) for _ in h]
report("random judge", h, rnd)
# 3) imbalanced data: 90% of outputs are good. A lazy judge that always says "pass" looks accurate.
random.seed(9)
hh = [1 if random.random() < 0.9 else 0 for _ in range(200)]
report("always-pass judge (90% good)", hh, [1]*200)
# a real-ish judge: catches 60% of bad, 95% of good
jj = [(1 if random.random() < 0.95 else 0) if x == 1 else (1 if random.random() < 0.4 else 0) for x in hh]
report("judge: TPR~.95, TNR~.60", hh, jj)
# 4) uncertainty: bootstrap CI for kappa on the 200 items
r = random.Random(1); ks = []
for _ in range(2000):
    idx = [r.randrange(200) for _ in range(200)]
    hb = [hh[i] for i in idx]; jb = [jj[i] for i in idx]
    k = kappa(hb, jb)
    if k == k: ks.append(k)
ks.sort(); print(f"bootstrap 95% CI for kappa of the realistic judge: [{ks[int(.025*len(ks))]:.3f}, {ks[int(.975*len(ks))-1]:.3f}]  (only {sum(1 for x in hh if x==0)} bad items drive TNR)")
```
**Output (my run):**
```
hand-check (expect kappa 0.400)    n= 50 acc=0.700 TPR=0.600 TNR=0.800 kappa=0.400
identical labels                   n= 50 acc=1.000 TPR=1.000 TNR=1.000 kappa=1.000
random judge                       n= 50 acc=0.520 TPR=0.560 TNR=0.480 kappa=0.040
always-pass judge (90% good)       n=200 acc=0.915 TPR=1.000 TNR=0.000 kappa=0.000
judge: TPR~.95, TNR~.60            n=200 acc=0.915 TPR=0.934 TNR=0.706 kappa=0.540
bootstrap 95% CI for kappa of the realistic judge: [0.345, 0.719]  (only 17 bad items drive TNR)
```
**Follow-ups:**
- *More than two classes?* Same formula with pe summed over all classes; use weighted kappa when classes are ordered.
- *More than two raters?* Fleiss' kappa or Krippendorff's alpha (Part 9 Q25).
- *What do you do with a low kappa?* Read the disagreements, fix the rubric or the labels, relabel a calibration set, then re-measure; do not just swap the judge model.
**Common mistakes:** reporting accuracy only; computing kappa on a calibration set the rubric was tuned on; ignoring class imbalance; treating a kappa from 50 items as precise; mixing up which rater is the reference when reading TPR and TNR.

### Q40 ⭐ 🟡 Code: build a mini evaluation harness (dataset loader, model runner, graders, caching, repeated trials, a report with confidence intervals) with a mocked LLM.
**Asked at:** product, big tech, GenAI startups, live-coding rounds
**Say this first (1 line):** A harness is five small pieces: a loader, a runner that calls the model through a cache, graders that turn outputs into scores, repeated trials, and a report that gives a mean with a confidence interval computed over cases.
**Then explain:**
- **Loader:** read JSONL into dicts with an id, input and reference. Fail loudly on duplicates and missing fields.
- **Runner and cache:** key the cache on everything that changes the output (model, prompt, trial index, and in real life temperature and parameters). A rerun then costs nothing and is reproducible.
- **Graders are separate functions** returning a score per case. Keep them deterministic where you can (exact, regex, schema) and add a judge only where needed (Part 9 Q32).
- **Repeated trials:** average trials inside a case, then bootstrap over cases, because trials of one case are not independent (Part 9 Q27, Q38).
- **Report:** per grader, mean and CI; for two models, a paired difference with its CI.
- **Keep honest weak results:** with 30 cases the large model's edge in the run is not established.
**Example:** (SYNTHETIC; the mock models are assumed to be right 70% and 85% of the time). 30 arithmetic cases, 3 trials, 90 calls per model. The strict exact-match grader scores both models 0.000, because the mock models answer "The answer is 12." That is a grader bug, not a model fact; the "contains the number" grader gives small 0.722 [0.622, 0.822] and large 0.822 [0.767, 0.878]. The paired difference is +0.100 with CI [-0.022, +0.233], so on 30 cases it includes zero. The first pass makes 90 calls per model with 0 cache hits; the rerun makes no new calls and has 180 cache hits.
**Code:** (run with `python3 -I`; stdlib only; mock LLM, no network)
```python
# Mini eval harness with a MOCK LLM: loader -> runner (cached) -> graders -> repeated trials -> report with CIs.
import hashlib, io, json, random, re
DATA = "\n".join(json.dumps(x) for x in [   # toy JSONL "file" (synthetic)
    {"id": f"q{i}", "question": f"What is {a} + {b}?", "answer": str(a + b)} for i, (a, b) in enumerate((2 + i * 7 % 41, 3 + i * 11 % 37) for i in range(30))])
def load(fp): return [json.loads(l) for l in fp if l.strip()]
class MockLLM:
    """Stands in for an API. Output depends on (model, prompt, trial) via a hash seed; strength = P(correct); verbose models add chatter."""
    def __init__(self, name, strength, verbose=False): self.name, self.strength, self.verbose, self.calls = name, strength, verbose, 0
    def complete(self, prompt, trial):
        self.calls += 1
        seed = int(hashlib.sha256(f"{self.name}|{prompt}|{trial}".encode()).hexdigest()[:8], 16)
        r = random.Random(seed); a, b = map(int, re.findall(r"\d+", prompt))
        val = a + b if r.random() < self.strength else a + b + r.choice([-1, 1, 10])
        return f"The answer is {val}." if self.verbose else str(val)
class Cache:
    def __init__(self): self.d, self.hits = {}, 0
    def get(self, model, prompt, trial, fn):
        k = hashlib.sha256(json.dumps([model.name, prompt, trial]).encode()).hexdigest()
        if k in self.d: self.hits += 1
        else: self.d[k] = fn()
        return self.d[k]
def g_exact(out, ex): return float(out.strip() == ex["answer"])
def g_contains(out, ex): return float(re.search(rf"(?<!\d){re.escape(ex['answer'])}(?!\d)", out) is not None)
GRADERS = {"exact": g_exact, "contains_number": g_contains}
def evaluate(model, data, cache, trials=3):
    res = {g: [[0.0] * trials for _ in data] for g in GRADERS}          # res[grader][case][trial]
    for i, ex in enumerate(data):
        for t in range(trials):
            out = cache.get(model, ex["question"], t, lambda: model.complete(ex["question"], t))
            for g, fn in GRADERS.items(): res[g][i][t] = fn(out, ex)
    return res
def case_means(m): return [sum(r) / len(r) for r in m]
def ci(vals, B=4000, seed=0):                      # bootstrap over CASES (trials of a case are not independent)
    r = random.Random(seed); n = len(vals)
    s = sorted(sum(vals[r.randrange(n)] for _ in range(n)) / n for _ in range(B))
    return sum(vals) / n, s[int(.025 * B)], s[int(.975 * B) - 1]
data = load(io.StringIO(DATA)); cache = Cache()
print("cases loaded:", len(data))
models = [MockLLM("small", 0.70, verbose=True), MockLLM("large", 0.85, verbose=True)]
results = {}
for m in models:
    results[m.name] = evaluate(m, data, cache)
    for g in GRADERS:
        mean, lo, hi = ci(case_means(results[m.name][g]))
        print(f"{m.name:6} grader={g:16} accuracy {mean:.3f}  95% CI [{lo:.3f}, {hi:.3f}]")
print("model calls:", {m.name: m.calls for m in models}, "cache hits:", cache.hits)
for m in models: evaluate(m, data, cache)                                  # rerun: everything should come from cache
print("after rerun   calls:", {m.name: m.calls for m in models}, "cache hits:", cache.hits)
d = [a - b for a, b in zip(case_means(results["large"]["contains_number"]), case_means(results["small"]["contains_number"]))]
mean, lo, hi = ci(d)
print(f"paired difference large-small (contains_number) {mean:+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]")
print("note: 'exact' grader scores the verbose models near 0 -- a grader bug, not a model fact:", round(ci(case_means(results['large']['exact']))[0], 3))
```
**Output (my run):**
```
cases loaded: 30
small  grader=exact            accuracy 0.000  95% CI [0.000, 0.000]
small  grader=contains_number  accuracy 0.722  95% CI [0.622, 0.822]
large  grader=exact            accuracy 0.000  95% CI [0.000, 0.000]
large  grader=contains_number  accuracy 0.822  95% CI [0.767, 0.878]
model calls: {'small': 90, 'large': 90} cache hits: 0
after rerun   calls: {'small': 90, 'large': 90} cache hits: 180
paired difference large-small (contains_number) +0.100  95% CI [-0.022, +0.233]
note: 'exact' grader scores the verbose models near 0 -- a grader bug, not a model fact: 0.0
```
**Follow-ups:**
- *How do you add an LLM judge?* As another grader function with its own cache key (judge model and rubric version) and its own calibration (Part 9 Q6).
- *Parallelism and rate limits?* Wrap the runner in a thread pool with retries and a budget; keep the cache write thread-safe.
- *Build or buy?* Part 9 Q35.
**Common mistakes:** a cache key missing the model or the prompt version; caching away the trial variation you wanted to measure; CIs over trials instead of cases; a brittle grader silently scoring everything 0 (always print a few graded examples); no budget cap.

### Q41 ⭐ 🟡 AI code review: this LLM-written evaluation script has bugs (test cases leaked into few-shot examples, naive pass@k, no position swap, mean score with no interval, same model as generator and judge, nonzero temperature with one run). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
**Say this first (1 line):** The script has six classic bugs, and each one makes the result look better or more certain than it is: leaked test cases, a biased pass@k estimator, a position-biased judge, no interval, a self-judging model, and a single run at nonzero temperature.
**Then explain:**
| # | Bug | Effect | Fix |
|---|---|---|---|
| 1 | few-shot examples sampled from the test set | model can copy answers, score inflated | separate dev pool for examples, assert it is disjoint from test (Part 9 Q2) |
| 2 | naive pass@k, 1-(1-c/n)^k | biased estimate | unbiased 1 - C(n-c,k)/C(n,k) (Part 9 Q12, Q13) |
| 3 | pairwise judge always sees system X first | position bias becomes a win rate | run both orders, count a win only across both (Part 9 Q5, Q18) |
| 4 | mean score only | cannot tell signal from noise | paired bootstrap interval (Part 9 Q38) |
| 5 | same model generates and judges | self-preference | judge from a different family; verify with a swap (Part 9 Q5) |
| 6 | temperature above 0 and one run | one noisy number | repeated trials, mean and spread (Part 9 Q27) |
**Example:** (MOCK models and judges; the biases are assumed, so the numbers show direction only.) (1) 200 test questions, 40 shots taken from them: score 0.585 vs 0.505 after the fix (the mock answers half of unseen questions). (2) n = 10 samples, k = 5, per-sample success 0.3 (assumed): true pass@5 is 0.8319, the expected unbiased estimate is 0.8319, the expected naive estimate is 0.7597, so the plug-in version under-reports here. (3) Two equal systems and a judge that favours slot A 65% of the time: X "wins" 0.670 with X always first, 0.518 with swapping. (4) Two systems with an identical mean of 3.45: the paired diff is +0.00 with CI [-0.25, +0.25]. (5) A judge adding +0.6 to its own family gives 4.20 vs 3.61 for an equally good system. (6) Eight single runs of a 70%-accurate mock on 30 items range from 0.533 to 0.800 (sd 0.108).
**Code:** (run with `python3 -I`; stdlib only; each bug shown as a mock demo with its fix)
```python
# Six bugs in an LLM-written eval script, each shown with its effect on MOCK data (synthetic), then fixed.
import math, random
rng = random.Random(0)
print("1) few-shot examples drawn from the test set")
test = list(range(200))                                 # 200 test questions
def model_correct(q, shots): return True if q in shots else rng.random() < 0.5   # mock model copies any answer it has seen in the prompt
shots_bad = rng.sample(test, 40)                        # BUG: shots come from the test set
acc_bad = sum(model_correct(q, shots_bad) for q in test) / 200
dev = list(range(1000, 1100)); shots_ok = rng.sample(dev, 40)       # FIX: shots from a separate dev pool, assert disjoint
assert not set(shots_ok) & set(test)
acc_ok = sum(model_correct(q, shots_ok) for q in test) / 200
print(f"   buggy accuracy {acc_bad:.3f}   fixed {acc_ok:.3f}   (mock model truly answers ~50% of unseen questions)")
print("2) naive pass@k: 1-(1-c/n)^k vs unbiased 1-C(n-c,k)/C(n,k)")
n, k, p = 10, 5, 0.3                                    # per-sample success probability p (assumed), n samples, report pass@5
def unbiased(n, c, k): return 1.0 if n - c < k else 1 - math.comb(n - c, k) / math.comb(n, k)
def naive(n, c, k): return 1 - (1 - c / n) ** k
pmf = [math.comb(n, c) * p ** c * (1 - p) ** (n - c) for c in range(n + 1)]
E_naive = sum(w * naive(n, c, k) for c, w in enumerate(pmf)); E_unb = sum(w * unbiased(n, c, k) for c, w in enumerate(pmf))
print(f"   true pass@{k} = {1-(1-p)**k:.4f}   E[naive] = {E_naive:.4f}   E[unbiased] = {E_unb:.4f}")
print("3) no position swap in a pairwise judge (mock judge prefers slot A 65% of the time when quality is equal)")
def judge(first, second): return "A" if rng.random() < 0.65 else "B"   # equal-quality systems: pure position bias
one_order = sum(judge("X", "Y") == "A" for _ in range(1000)) / 1000      # BUG: X always in slot A
both = sum((judge("X", "Y") == "A") + (judge("Y", "X") == "B") for _ in range(500)) / 1000   # FIX: half each way
print(f"   X win rate, X always first {one_order:.3f}   with order swap {both:.3f}   (truth 0.500, 1000 judgements each)")
print("4) mean score with no interval (20 items, scores 1-5, synthetic)")
s1 = [rng.choice([3, 4, 4, 5, 2]) for _ in range(20)]; s2 = [min(5, max(1, x + rng.choice([-1, 0, 0, 1]))) for x in s1]
d = [a - b for a, b in zip(s1, s2)]; bs = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(5000))
print(f"   mean A {sum(s1)/20:.2f} vs B {sum(s2)/20:.2f}; paired diff {sum(d)/20:+.2f}, 95% CI [{bs[125]:+.2f}, {bs[4874]:+.2f}] -> do not claim a win if it spans 0")
print("5) same model generates and judges (mock judge adds +0.6 to its own family's outputs)")
true_q = [rng.gauss(3.5, 0.6) for _ in range(200)]      # both systems have identical true quality
own = sum(q + 0.6 + rng.gauss(0, .3) for q in true_q) / 200; other = sum(q + rng.gauss(0, .3) for q in true_q) / 200
print(f"   judge scores own-family system {own:.2f} vs equal-quality other system {other:.2f}; FIX: judge from a different family, or check by swapping judges")
print("6) temperature > 0 and a single run (mock model, true accuracy 0.70, 30 items)")
def one_run(): return sum(rng.random() < 0.70 for _ in range(30)) / 30
singles = [one_run() for _ in range(8)]; mu = sum(singles) / 8; sd = (sum((x - mu) ** 2 for x in singles) / 7) ** .5
print(f"   8 single runs: min {min(singles):.3f} max {max(singles):.3f}; mean {mu:.3f} sd {sd:.3f}  -> a lone run can differ by several points; FIX: repeat trials, report mean and spread")
```
**Output (my run):**
```
1) few-shot examples drawn from the test set
   buggy accuracy 0.585   fixed 0.505   (mock model truly answers ~50% of unseen questions)
2) naive pass@k: 1-(1-c/n)^k vs unbiased 1-C(n-c,k)/C(n,k)
   true pass@5 = 0.8319   E[naive] = 0.7597   E[unbiased] = 0.8319
3) no position swap in a pairwise judge (mock judge prefers slot A 65% of the time when quality is equal)
   X win rate, X always first 0.670   with order swap 0.518   (truth 0.500, 1000 judgements each)
4) mean score with no interval (20 items, scores 1-5, synthetic)
   mean A 3.45 vs B 3.45; paired diff +0.00, 95% CI [-0.25, +0.25] -> do not claim a win if it spans 0
5) same model generates and judges (mock judge adds +0.6 to its own family's outputs)
   judge scores own-family system 4.20 vs equal-quality other system 3.61; FIX: judge from a different family, or check by swapping judges
6) temperature > 0 and a single run (mock model, true accuracy 0.70, 30 items)
   8 single runs: min 0.533 max 0.800; mean 0.658 sd 0.108  -> a lone run can differ by several points; FIX: repeat trials, report mean and spread
```
**Follow-ups:**
- *Which bug would you look for first?* Leakage, because it silently invalidates every other number; then the judge setup.
- *How do you find leakage?* Check overlap of test inputs with prompts, few-shot pools and training or fine-tuning data (Part 4 Q34 on fine-tuning data, Part 9 Q21).
- *Is the naive pass@k always low?* Not in general; in this setting it under-reports. The point is that it is biased and the unbiased form is cheap.
**Common mistakes:** fixing the code but not re-running to see the change in the number; "fixing" position bias by randomising once instead of swapping every pair; a fixed seed standing in for repeated trials; adding an interval but resampling the wrong unit.

### Q42 ⭐ 🔴 Offline scores keep rising but user complaints are rising too. Diagnose the gap and say what you change in the eval.
**Asked at:** senior roles; an interview-prep guide poses this scenario (a guide, not a candidate report)
**Say this first (1 line):** The offline set no longer represents what users do or what they care about, so I would reweight and refresh the set from current traffic and complaints, and check whether the offline metric or judge is being gamed.
**Then explain:**
- **Diagnose in this order:** (1) join complaints to traces and categorise them (Part 9 Q15); (2) compare the offline set's mix to today's traffic; (3) look at per-slice trends, not the headline; (4) check whether the metric rewards something users do not want, such as length; (5) check for overfitting to the set after many tuning rounds; (6) check for non-quality causes (latency, UI, a retrieval change).
- **Traffic shift:** the eval set was frozen from older traffic; new query types are underrepresented. Fix by stratifying and reweighting to the current mix, and by adding cases from the new slice.
- **Metric mismatch:** a judge that favours long answers rewards a change that users dislike (Part 9 Q5). Fix by controlling length, calibrating against user outcomes, or adding implicit-feedback signals (Part 9 Q30).
- **Goodhart:** after many rounds of tuning against one set, the score stops predicting reality; keep a held-out set that is not used for tuning.
- **Then change the eval:** add the complaint cases as a new slice, report per-slice scores, set a per-slice floor so one slice cannot hide behind the average, and track the gap between offline and online as a metric of its own.
**Example:** (SYNTHETIC, assumed numbers). Three categories; the eval set mix is 60/30/10 (billing, how-to, new feature) but today's traffic is 35/30/35. Releases r1 to r4 tune billing up (0.70 to 0.95) while the new-feature slice degrades (0.60 to 0.35). The offline headline rises 0.705, 0.760, 0.795, 0.824, while the same per-category scores reweighted to today's traffic go 0.680, 0.698, 0.688, 0.674. Separately, a mock judge with a length bonus correlates +0.46 with answer length while mock user satisfaction correlates -0.28; the 200-word bucket gets a mean judge score of +1.28 and mean user satisfaction of -0.70.
**Code:** (run with `python3 -I`; stdlib only; synthetic illustration, not evidence about any real product)
```python
# SYNTHETIC illustration: offline headline score rises while the score on CURRENT traffic falls, and a length-biased judge.
import random
random.seed(21)
cats = ["billing", "how_to", "new_feature"]
offline_mix = {"billing": 0.60, "how_to": 0.30, "new_feature": 0.10}     # eval set frozen from last year's traffic (assumed)
prod_mix_now = {"billing": 0.35, "how_to": 0.30, "new_feature": 0.35}    # traffic today (assumed)
# true per-category accuracy of 4 releases (assumed): tuning targets billing, new_feature quietly degrades
acc = {"r1": {"billing": .70, "how_to": .75, "new_feature": .60}, "r2": {"billing": .80, "how_to": .75, "new_feature": .55},
       "r3": {"billing": .88, "how_to": .74, "new_feature": .45}, "r4": {"billing": .95, "how_to": .73, "new_feature": .35}}
print("release  offline(frozen mix)  reweighted to today's traffic")
for r, a in acc.items():
    off = sum(offline_mix[c] * a[c] for c in cats); now = sum(prod_mix_now[c] * a[c] for c in cats)
    print(f"{r}       {off:.3f}              {now:.3f}")
# judge with length bias: score = quality + 0.08 * extra_words/10 ; users prefer concise. Longer answers win with the judge.
def judge_score(quality, words): return quality + 0.08 * (words - 40) / 10
def user_sat(quality, words): return quality - 0.05 * max(0, words - 60) / 10
rows = []
for _ in range(2000):
    q = random.gauss(0, 1); w = random.choice([30, 60, 120, 200]); rows.append((judge_score(q, w), user_sat(q, w), w, q))
def corr(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)) ** .5
js = [r[0] for r in rows]; us = [r[1] for r in rows]; ws = [r[2] for r in rows]
print(f"\ncorr(judge score, length) = {corr(js, ws):+.2f}   corr(user satisfaction, length) = {corr(us, ws):+.2f}   corr(judge, user) = {corr(js, us):+.2f}")
for w in (30, 60, 120, 200):
    sel = [r for r in rows if r[2] == w]
    print(f"  {w:3d} words: mean judge {sum(r[0] for r in sel)/len(sel):+.2f}   mean user sat {sum(r[1] for r in sel)/len(sel):+.2f}")
```
**Output (my run):**
```
release  offline(frozen mix)  reweighted to today's traffic
r1       0.705              0.680
r2       0.760              0.698
r3       0.795              0.688
r4       0.824              0.674

corr(judge score, length) = +0.46   corr(user satisfaction, length) = -0.28   corr(judge, user) = +0.72
   30 words: mean judge -0.04   mean user sat +0.04
   60 words: mean judge +0.07   mean user sat -0.09
  120 words: mean judge +0.57   mean user sat -0.37
  200 words: mean judge +1.28   mean user sat -0.70
```
**Follow-ups:**
- *What if offline is truly representative and complaints still rise?* Then the cause may be outside the model (latency, UI, pricing) or in what the metric measures; look at the complaint text before changing anything.
- *Do you throw the offline set away?* No, it stays as a regression suite (Part 9 Q36), but it stops being the success metric.
- *How do you prevent it recurring?* Refresh from sampled production traces every cycle and monitor offline vs online agreement (monitoring depth is Part 11).
**Common mistakes:** trusting the average; adding more of the same cases; blaming users; changing the model before looking at the complaints; removing the judge entirely instead of calibrating it.

### Q43 ⭐ 🔴 The model provider quietly updates a model version and quality drops. How do you detect it, attribute it, and protect against it (version pinning, canary evals, rollback)?
**Asked at:** senior roles, platform teams, product companies, GCCs
**Say this first (1 line):** Pin a dated snapshot so changes only happen when I choose, run a fixed canary eval on a schedule against both the alias and the pin, alert on a paired difference, then attribute by slice and by what else changed, and roll back by switching the pin.
**Then explain:**
- **Prevention:** use a dated model identifier rather than a floating alias where the provider offers one, and track the provider's deprecation notices (from memory: providers publish snapshot names and retirement schedules; check your provider's docs for current policy).
- **Detection:** a fixed canary set (here 150 prompts) run daily through the alias and through the pinned snapshot. Compare them case by case with an exact sign test on the cases where they disagree (a McNemar-style test; Part 9 Q28). Same prompts, same day, so the noise is only model noise.
- **Power is the catch.** Small canaries miss moderate drops. In the run, a single day on 150 prompts caught the assumed update only 8% of the time at alpha 0.01, while 600 prompts caught it 65.7% of the time. Pool days, grow the canary, or accept a looser alpha plus a human look.
- **Attribution:** (1) slice the drop (here the drop sat in one slice); (2) rule out your own changes (prompt, retrieval index, tool versions, data) by freezing them; (3) re-run the pinned snapshot to confirm the baseline did not move; (4) read a sample of the failing outputs for format changes or refusals.
- **Protection:** snapshot pin plus a staged switch (shadow traffic, then a small share), rollback by flipping the pin, and a regression suite that gates any version bump (Part 9 Q14, Q36). Online monitoring and tracing depth is Part 11.
**Example:** (SYNTHETIC mock provider; all rates assumed.) The sign-test code matches brute force (p = 0.03857). With no change at all, 1 of 200 days was flagged at alpha 0.01 (about 2 expected). I then made the alias "update" on day 10, breaking an assumed 30-prompt slice. No single day from 10 to 15 alerted at 0.01 (day 14 had p = 0.0259, day 15 p = 0.0596), but pooling days 10 to 12 gave p = 0.030, and the broken slice showed 0.467 on the alias vs 0.867 on the pin. This is an honest weak result: a 150-prompt canary is not a reliable alarm for a drop this size, which is why the power numbers matter.
**Code:** (run with `python3 -I`; stdlib only; mock provider with an assumed silent update)
```python
# SYNTHETIC canary eval for a silent provider update. Mock provider; daily run of the same 150 prompts on the alias and on a pinned snapshot.
import math, random
random.seed(33)
N = 150
prompt_difficulty = [random.random() for _ in range(N)]          # fixed canary prompts (assumed latent difficulty)
def pass_prob(version, d, fmt_broken_subset):
    base = 0.97 - 0.5 * d ** 2                                   # easier prompts pass more often
    if version == "new" and fmt_broken_subset: base -= 0.35      # silent update breaks a slice (assumed: prompts with index % 5 == 0)
    return max(0.02, base)
def daily_run(version):
    return [random.random() < pass_prob(version, prompt_difficulty[i], i % 5 == 0) for i in range(N)]
def sign_test_p(b, c):                                           # exact two-sided sign test on discordant pairs (McNemar exact)
    n = b + c
    if n == 0: return 1.0
    k = min(b, c); p = 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, p)
# brute-force check of the sign test against direct enumeration of a fair coin
import itertools
bf = sum(1 for bits in itertools.product([0, 1], repeat=12) if min(sum(bits), 12 - sum(bits)) <= 2) / 2 ** 12
print("sign-test check: exact p(b=2,c=10) =", round(sign_test_p(2, 10), 5), " brute force:", round(bf, 5))
# A) false-alarm rate: 200 days where alias and pinned are the SAME model (both 'old'), alpha = 0.01
false_alarms = 0
for _ in range(200):
    x, y = daily_run("old"), daily_run("old")
    b = sum(1 for p, q in zip(x, y) if p and not q); c = sum(1 for p, q in zip(x, y) if q and not p)
    false_alarms += sign_test_p(b, c) < 0.01
print(f"no real change: {false_alarms}/200 days flagged at alpha=0.01 (expect about 2)")
# B) real silent update on day 10: alias becomes 'new', pinned snapshot stays 'old'
print("\nday  alias_acc  pinned_acc  only-pinned-right  only-alias-right  p_value  alert(0.01)")
tb = tc = 0
for day in range(8, 16):
    ver = "old" if day < 10 else "new"
    a, p = daily_run(ver), daily_run("old")
    b = sum(1 for x, y in zip(a, p) if y and not x); c = sum(1 for x, y in zip(a, p) if x and not y)
    pv = sign_test_p(b, c)
    if day >= 10 and day <= 12: tb += b; tc += c
    print(f"{day:3d}  {sum(a)/N:.3f}      {sum(p)/N:.3f}       {b:3d}                {c:3d}               {pv:.4f}  {'ALERT' if pv < 0.01 else '-'}")
print(f"pooled days 10-12: only-pinned-right {tb}, only-alias-right {tc}, p = {sign_test_p(tb, tc):.5f}")
# power: how often does ONE day alert at alpha=0.01, for canary sizes 150 vs 600 prompts? (same assumed 30%-slice, 0.35 drop)
def power(n_prompts, reps=300):
    global N, prompt_difficulty
    saveN, saved = N, prompt_difficulty
    N = n_prompts; prompt_difficulty = [random.random() for _ in range(N)]; hit = 0
    for _ in range(reps):
        a, p = daily_run("new"), daily_run("old")
        b = sum(1 for x, y in zip(a, p) if y and not x); c = sum(1 for x, y in zip(a, p) if x and not y)
        hit += sign_test_p(b, c) < 0.01
    N, prompt_difficulty = saveN, saved
    return hit / reps
print("single-day detection rate at alpha=0.01:  150 prompts", round(power(150), 3), "  600 prompts", round(power(600), 3))
# C) attribution: where did the drop come from?
a = daily_run("new"); p = daily_run("old")
for name, idx in [("index%5==0 slice", [i for i in range(N) if i % 5 == 0]), ("all other prompts", [i for i in range(N) if i % 5])]:
    print(f"slice {name:18} n={len(idx):3d}  alias {sum(a[i] for i in idx)/len(idx):.3f}  pinned {sum(p[i] for i in idx)/len(idx):.3f}")
```
**Output (my run):**
```
sign-test check: exact p(b=2,c=10) = 0.03857  brute force: 0.03857
no real change: 1/200 days flagged at alpha=0.01 (expect about 2)

day  alias_acc  pinned_acc  only-pinned-right  only-alias-right  p_value  alert(0.01)
  8  0.820      0.800        17                 20               0.7428  -
  9  0.780      0.820        22                 16               0.4177  -
 10  0.713      0.787        28                 17               0.1352  -
 11  0.747      0.827        31                 19               0.1189  -
 12  0.787      0.807        21                 18               0.7493  -
 13  0.720      0.747        28                 24               0.6778  -
 14  0.700      0.807        31                 15               0.0259  -
 15  0.747      0.833        27                 14               0.0596  -
pooled days 10-12: only-pinned-right 80, only-alias-right 54, p = 0.03041
single-day detection rate at alpha=0.01:  150 prompts 0.08   600 prompts 0.657
slice index%5==0 slice   n= 30  alias 0.467  pinned 0.867
slice all other prompts  n=120  alias 0.775  pinned 0.842
```
**Follow-ups:**
- *What if there is no snapshot to pin?* Run your own canary against the alias, store outputs per day, and compare against your own frozen baseline outputs and scores; you can detect but cannot roll back.
- *Alert fatigue?* Alert on the pooled or rolling test, and page only when a guardrail slice moves.
- *Self-hosted models?* Pin weights and serving stack; changes then come from your own deployments, which the same canary also catches.
**Common mistakes:** monitoring only latency and errors; a canary too small to detect anything; comparing today to last month without a same-day control; attributing a drop to the provider before ruling out your own prompt or index changes; no rollback path.

### Q44 ⭐ 🔴 Design question: an evaluation platform for many teams (datasets, versioned prompts and graders, runs, dashboards, CI integration, human review queues, cost control).
**Asked at:** senior roles at product companies, platform teams, GenAI startups
**Say this first (1 line):** I would build the platform around immutable, versioned artifacts (datasets, prompts, graders) and recorded runs, with a CI gate, a human-review queue and budgets on top, so any number on a dashboard can be traced back to exactly what produced it.
**Then explain:**
- **Core objects:** dataset version, prompt version, grader version (including judge model and rubric), model identifier and parameters, and a run record linking them with per-case results. Version by content hash so identical content gets the same id.
- **Runs:** triggered from CI, a notebook or a schedule; results are stored per case, not just aggregates, so you can diff two runs case by case.
- **CI integration:** a gate compares a candidate run to a baseline run on the same dataset version with a paired check and a threshold (Part 9 Q14); blocking for core suites, advisory for the rest.
- **Human review queue:** send the cases the judge is least sure about, plus a random audit sample, to reviewers; their labels feed the judge calibration set (Part 9 Q6, Q45).
- **Cost control:** per-team budgets, caching of identical calls, sampling for expensive judges, and a cheap-then-expensive cascade (Part 9 Q33).
- **Multi-team concerns:** permissions, a shared grader library with owners, golden-set governance (Part 9 Q2), PII handling for production traces, and a "build vs adopt" decision on tooling (Part 9 Q35). Dashboards should show per-slice scores with intervals (Part 9 Q34, Q38), not one average.
**Example:** (MOCK, in-memory sketch; prices are assumed, not real.) The same dataset content gives the same version id and adding one case gives a new one. A baseline run scores 0.817 and a candidate prompt 0.717; the CI gate (max drop 0.03) says BLOCK, with 15 cases regressed and 9 improved. The review queue picks the five cases whose judge confidence is closest to 0.5. A team with a $0.05 budget is stopped by an exception partway through its run instead of overspending.
**Code:** (run with `python3 -I`; stdlib only; a design sketch, not a product)
```python
# Skeleton of a multi-team eval platform core (in-memory, mock grader). Shows: content-hash versioning, runs, CI gate, budget, review queue.
import hashlib, json, random
def vhash(obj): return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:8]
class Registry:                                              # immutable, content-addressed artifacts: datasets, prompts, graders
    def __init__(self): self.items = {}
    def put(self, kind, name, content):
        v = vhash(content); self.items[(kind, name, v)] = content; return f"{name}@{v}"
    def get(self, kind, ref):
        name, v = ref.split("@"); return self.items[(kind, name, v)]
reg = Registry(); runs = []
ds = reg.put("dataset", "support_qa", [{"id": i, "q": f"q{i}", "label": i % 3 != 0} for i in range(60)])
ds_same = reg.put("dataset", "support_qa", [{"id": i, "q": f"q{i}", "label": i % 3 != 0} for i in range(60)])
ds_v2 = reg.put("dataset", "support_qa", [{"id": i, "q": f"q{i}", "label": i % 3 != 0} for i in range(61)])
print("same content -> same version:", ds == ds_same, "| one case added -> new version:", ds != ds_v2, f"({ds}, {ds_v2})")
pr1 = reg.put("prompt", "answer", {"template": "Answer briefly: {q}"}); pr2 = reg.put("prompt", "answer", {"template": "Answer briefly and cite: {q}"})
gr = reg.put("grader", "correct", {"type": "mock_judge", "rubric": "pass if correct"})
class Budget:
    def __init__(self, usd): self.left = usd
    def charge(self, usd):
        if usd > self.left: raise RuntimeError("budget exceeded")
        self.left -= usd
def run_eval(team, prompt_ref, dataset_ref, grader_ref, skill, budget, cost_per_call=0.002, seed=0):
    rnd = random.Random(vhash([prompt_ref, dataset_ref, seed])); rows = []
    for case in reg.get("dataset", dataset_ref):
        budget.charge(cost_per_call * 2)                     # one generation + one judge call (assumed prices, not real)
        ok = rnd.random() < skill; rows.append({"id": case["id"], "pass": ok, "judge_conf": round(rnd.random(), 2)})
    rec = {"run_id": f"run{len(runs)+1}", "team": team, "prompt": prompt_ref, "dataset": dataset_ref, "grader": grader_ref,
           "score": sum(r["pass"] for r in rows) / len(rows), "rows": rows}
    runs.append(rec); return rec
def ci_gate(base, cand, max_drop=0.03):
    pairs = [(a["pass"], b["pass"]) for a, b in zip(base["rows"], cand["rows"])]
    b = sum(1 for x, y in pairs if x and not y); c = sum(1 for x, y in pairs if y and not x)
    drop = base["score"] - cand["score"]
    return {"score_drop": round(drop, 3), "regressed_cases": b, "improved_cases": c, "decision": "BLOCK" if drop > max_drop else "PASS"}
bud = Budget(0.60)
base = run_eval("support", pr1, ds, gr, 0.80, bud)
cand = run_eval("support", pr2, ds, gr, 0.70, bud)
print("baseline", base["run_id"], round(base["score"], 3), "| candidate", cand["run_id"], round(cand["score"], 3), "| budget left $", round(bud.left, 3))
print("CI gate:", ci_gate(base, cand))
print("run record links:", {k: cand[k] for k in ("prompt", "dataset", "grader")})
queue = sorted(cand["rows"], key=lambda r: abs(r["judge_conf"] - 0.5))[:5]       # review the cases the judge is least sure about
print("human review queue (id, judge_conf):", [(r["id"], r["judge_conf"]) for r in queue])
tiny = Budget(0.05)
try: run_eval("growth", pr1, ds, gr, 0.8, tiny)
except RuntimeError as e: print("per-team budget stops the run:", e, "| left $", round(tiny.left, 3))
```
**Output (my run):**
```
same content -> same version: True | one case added -> new version: True (support_qa@68ba838b, support_qa@2a491c7a)
baseline run1 0.817 | candidate run2 0.717 | budget left $ 0.12
CI gate: {'score_drop': 0.1, 'regressed_cases': 15, 'improved_cases': 9, 'decision': 'BLOCK'}
run record links: {'prompt': 'answer@443be885', 'dataset': 'support_qa@68ba838b', 'grader': 'correct@716b48b5'}
human review queue (id, judge_conf): [(55, 0.5), (17, 0.49), (31, 0.49), (22, 0.52), (47, 0.48)]
per-team budget stops the run: budget exceeded | left $ 0.002
```
**Follow-ups:**
- *What breaks first at scale?* Cost and queue throughput, then grader sprawl (many near-duplicate graders nobody owns).
- *How do you keep judges honest across teams?* Each grader carries its calibration report and an anchor set that is re-scored on a schedule (Part 9 Q45).
- *Where do production traces enter?* Sampled, scrubbed and added to datasets as new versions, never edited in place.
**Common mistakes:** storing only aggregate scores; mutable datasets so old runs cannot be reproduced; one global threshold for every team; no ownership of graders; ignoring cost until the bill arrives; building a dashboard before the data model.

### Q45 ⭐ 🔴 Design question: build an LLM judge you can trust (rubric, human calibration set, bias tests, ensembles, drift monitoring, when to retire it).
**Asked at:** senior roles at product companies, GenAI startups, evaluation-focused rounds
**Say this first (1 line):** A judge I can trust is one I have measured: a narrow rubric, a human-labelled calibration set with a held-out test, explicit bias probes, an ensemble where it is worth the cost, a scheduled anchor check for drift, and a rule for when I retire it.
**Then explain:**
- **Rubric:** one criterion per judge, binary or a small scale, anchored examples, reasoning before the verdict (Part 9 Q7).
- **Calibration set:** a few hundred human-labelled cases split into dev (tune the rubric) and test (report once); report TPR, TNR and kappa with intervals (Part 9 Q6, Q39). Hamel Husain's FAQ (opened) gives 100-200 labelled examples per failure mode as his guidance, not a standard.
- **Bias tests:** a length probe (pad answers with fluff; the verdict should not move), a position swap for pairwise judges, and a self-preference check with a judge from another family (Part 9 Q5). The MT-Bench paper abstract (opened) reports position, verbosity and self-enhancement biases.
- **Ensembles:** a panel of smaller judges from different families can beat one large judge and cost less, as reported by the PoLL authors (abstract opened; their setting); errors must be independent for the gain to appear. The mock below assumes independence, which real judges only partly have.
- **Drift:** re-score a fixed human-labelled anchor set on a schedule and alert on kappa, TPR or TNR; also re-run after any change of judge model, prompt or data mix.
- **Retire it when:** it fails the anchor check and cannot be fixed with a rubric change, the task changed, humans and judge disagree on the hard cases that matter, or a deterministic check can do its job.
**Example:** (MOCK judges and SYNTHETIC labels; all biases assumed.) Judge A scores TPR 0.844, TNR 0.756, kappa 0.601 on a 200-item held-out test. Padding the same answers with 80 words moves its pass rate from 0.62 to 0.76, so it has a length bias; swapping order flips 0.25 of verdicts for a position-biased judge. Scoring the same judge A again gave kappa 0.751, which shows how noisy a single measurement is. The majority of three judges reached kappa 0.884 (TPR 0.959, TNR 0.923) under the independence assumption. For drift, kappa on 60 anchor items per week alerted at weeks 6 and 7 (0.387, 0.223) after the assumed TNR drop, but weeks 8 to 10 (0.476, 0.524, 0.472) stayed above the 0.45 threshold even though the drift persisted, so a single small weekly anchor is a noisy alarm.
**Code:** (run with `python3 -I`; stdlib only; mock judges)
```python
# Building a judge you can trust, on SYNTHETIC data with MOCK judges: calibration, bias tests, ensemble, drift.
import random
rng = random.Random(8)
def make_items(n):                                    # human label = ground truth (1 = good); answer length is independent of quality
    return [{"good": int(rng.random() < 0.6), "words": rng.choice([40, 80, 160])} for _ in range(n)]
def judge(item, tpr=0.9, tnr=0.8, len_bias=0.0, pos_bias=0.0, first=True):
    p = tpr if item["good"] else 1 - tnr
    p += len_bias * (item["words"] - 80) / 80 + (pos_bias if first else -pos_bias)
    return int(rng.random() < min(max(p, 0), 1))
def metrics(items, preds):
    tp = sum(1 for i, p in zip(items, preds) if i["good"] and p); fn = sum(1 for i, p in zip(items, preds) if i["good"] and not p)
    tn = sum(1 for i, p in zip(items, preds) if not i["good"] and not p); fp = sum(1 for i, p in zip(items, preds) if not i["good"] and p)
    n = len(items); po = (tp + tn) / n
    pe = ((tp + fn) / n) * ((tp + fp) / n) + ((tn + fp) / n) * ((tn + fn) / n)
    return tp / (tp + fn), tn / (tn + fp), (po - pe) / (1 - pe)
calib = make_items(300); dev, test = calib[:100], calib[100:]            # dev: tune the rubric; test: report once
J1 = lambda it: judge(it, len_bias=0.12, pos_bias=0.0)                  # judge A: has a length bias (assumed)
tpr, tnr, k = metrics(test, [J1(i) for i in test]); print(f"judge A on held-out calibration test (n={len(test)}): TPR {tpr:.3f} TNR {tnr:.3f} kappa {k:.3f}")
# bias test 1: pad the same answers with fluff (+80 words), human label unchanged
padded = [dict(i, words=i["words"] + 80) for i in test]
print("length probe: pass rate on original", round(sum(J1(i) for i in test) / len(test), 3), "-> padded", round(sum(J1(i) for i in padded) / len(test), 3), "(should not move)")
# bias test 2: position swap for a pairwise judge (mock: pos_bias 0.1 toward slot A)
flips = sum(judge(i, pos_bias=0.1, first=True) != judge(i, pos_bias=0.1, first=False) for i in test) / len(test)
print("position probe: verdict flips when order is swapped:", round(flips, 3))
# ensemble of 3 judges with independent errors (different 'model families', assumed), majority vote
J2 = lambda it: judge(it, len_bias=0.0); J3 = lambda it: judge(it, tpr=0.88, tnr=0.85)
def ens(it): return int(J1(it) + J2(it) + J3(it) >= 2)
for name, f in [("judge A", J1), ("judge B", J2), ("judge C", J3), ("majority of 3", ens)]:
    t, n_, kk = metrics(test, [f(i) for i in test]); print(f"  {name:14} TPR {t:.3f} TNR {n_:.3f} kappa {kk:.3f}")
# drift: weekly anchor set of 60 human-labelled items; the judge backend changes at week 6 (assumed: TNR falls 0.8 -> 0.55)
print("\nweek  kappa on 60 anchor items   alert (kappa < 0.45)")
for wk in range(1, 11):
    anchor = make_items(60); tnr_w = 0.8 if wk < 6 else 0.55
    _, _, kw = metrics(anchor, [judge(i, tnr=tnr_w) for i in anchor]); print(f"{wk:4d}  {kw:6.3f}                    {'ALERT' if kw < 0.45 else '-'}")
```
**Output (my run):**
```
judge A on held-out calibration test (n=200): TPR 0.844 TNR 0.756 kappa 0.601
length probe: pass rate on original 0.62 -> padded 0.76 (should not move)
position probe: verdict flips when order is swapped: 0.25
  judge A        TPR 0.959 TNR 0.769 kappa 0.751
  judge B        TPR 0.893 TNR 0.859 kappa 0.749
  judge C        TPR 0.910 TNR 0.821 kappa 0.735
  majority of 3  TPR 0.959 TNR 0.923 kappa 0.884

week  kappa on 60 anchor items   alert (kappa < 0.45)
   1   0.643                    -
   2   0.747                    -
   3   0.764                    -
   4   0.698                    -
   5   0.686                    -
   6   0.387                    ALERT
   7   0.223                    ALERT
   8   0.476                    -
   9   0.524                    -
  10   0.472                    -
```
**Follow-ups:**
- *How big should the anchor set be?* Big enough that the interval on TNR is useful; the rare class (bad items) sets the size (Part 9 Q26).
- *Judge disagrees with humans on a slice?* Add that slice to the calibration set and fix the rubric, or route the slice to humans.
- *Do you ever let a judge run unattended?* Only for tasks where its measured TPR and TNR are good enough and an audit sample keeps being reviewed.
**Common mistakes:** quoting agreement from the same data the rubric was tuned on; one big multi-criterion rubric; assuming ensemble errors are independent; no scheduled re-check; ignoring that the judge model may be updated by the provider (Part 9 Q43); never retiring a judge.

### Q46 ⭐ 🔴 Design question: an evaluation strategy for launching a new LLM assistant, including a high-stakes domain (clinical or financial): launch criteria, red team, human review, staged rollout, and answering 'is it ready?'
**Asked at:** senior roles; an interview-prep guide poses launch-readiness and clinical-assistant scenarios (a guide, not a candidate report)
**Say this first (1 line):** "Is it ready?" has no yes or no answer in general; I define launch criteria in advance as bounds on failure rates for each risk, show the evidence with intervals, and launch in stages with stop conditions, with humans in the loop for the high-stakes parts.
**Then explain:**
- **Criteria first, per risk:** helpfulness and grounding (lower bounds on pass rate), critical errors (upper bound on failure rate, much stricter), harmful compliance from red-teaming, over-refusal. Thresholds are set with the domain owner, before seeing results.
- **Evidence with bounds, not point estimates:** with zero failures in n cases the 95% upper bound on the failure rate is about 3/n (the rule of three), so a 2% target needs about 150 clean cases and 1% needs about 300 (the run confirms 149 and 299 with the exact bound).
- **Red team:** manual experts plus automated attacks, severity-weighted, with fixes re-tested (Part 5 Q23 for red-team basics; Part 9 Q29 for attack success rates and release gates).
- **High-stakes domain (clinical or financial):** domain experts grade a sample, the assistant abstains or escalates when unsure, citations or source grounding are checked (Part 9 Q9), a human reviews the outputs that can cause harm, and compliance and legal sign off on the use case. Regulatory requirements differ by jurisdiction; I would not guess them, I would ask compliance.
- **Staged rollout:** internal dogfood, a small share of traffic or shadow mode, then widening, each stage with a monitored guardrail, a minimum number of requests and a rollback trigger (A/B and monitoring in Part 9 Q30; monitoring depth in Part 11).
- **The honest answer:** "It meets these criteria with these bounds; these risks are unproven; here is what we monitor and when we stop." If a criterion fails, the answer is no, or a narrower launch.
**Example:** (SYNTHETIC results and assumed thresholds.) With exact 95% bounds: helpfulness 182/200 gives a lower bound 0.869 vs a 0.85 target (met); grounded 188/200 gives 0.905 vs 0.90 (met, barely); critical clinical error 1 in 250 gives an upper bound 0.019 vs 0.02 (met, barely); over-refusal 9/200 gives 0.077 vs 0.08 (met, barely); red-team harmful compliance 2/80 gives an upper bound 0.077 vs a 0.05 target (NOT MET). So the verdict is no-go for the full launch; fix the red-team failures and retest, or launch narrower. In rollout, zero critical incidents in 299 requests bounds the rate at 1%, and it takes 2995 to bound it at 0.1%.
**Code:** (run with `python3 -I`; stdlib only; exact binomial bounds checked against the closed form and the rule of three)
```python
# Launch-readiness arithmetic: exact (Clopper-Pearson) bounds on failure rates, and sample sizes for 'zero failures observed'.
import math
def binom_cdf(k, n, p): return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))
def upper_bound(f, n, conf=0.95):                       # one-sided exact upper bound on the failure rate after f failures in n
    if f >= n: return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if binom_cdf(f, n, mid) > 1 - conf: lo = mid
        else: hi = mid
    return hi
def lower_bound(s, n, conf=0.95):                       # one-sided lower bound on pass rate = 1 - upper bound on failure rate
    return 1 - upper_bound(n - s, n, conf)
# checks: zero failures has the closed form 1-(1-conf)^(1/n); rule of three says about 3/n
for n in (50, 100, 150, 300):
    print(f"0 failures in {n:3d}: exact upper {upper_bound(0, n):.4f}  closed form {1-0.05**(1/n):.4f}  rule of three {3/n:.4f}")
# brute-force check of the bound for 2 failures in 40: P(X<=2 | p=bound) should equal 0.05
ub = upper_bound(2, 40); print(f"2 failures in 40: bound {ub:.4f}; P(X<=2 | p=bound) = {binom_cdf(2, 40, ub):.4f}")
need = lambda target: next(n for n in range(1, 5000) if upper_bound(0, n) <= target)
print("\ncases needed with ZERO failures to bound the failure rate:", {t: need(t) for t in (0.10, 0.05, 0.02, 0.01)})
# launch scorecard (SYNTHETIC results, assumed thresholds)
card = [("helpfulness pass (human-graded)", 182, 200, "lower", 0.85), ("grounded in cited source", 188, 200, "lower", 0.90),
        ("critical clinical error (fail count)", 1, 250, "upper", 0.02), ("red-team: harmful compliance", 2, 80, "upper", 0.05),
        ("refuses safe requests (over-refusal)", 9, 200, "upper", 0.08)]
print("\ncriterion                              result      95% bound  threshold  verdict")
for name, x, n, kind, thr in card:
    if kind == "lower":
        b = lower_bound(x, n); ok = b >= thr; print(f"{name:38} {x}/{n} pass   >= {b:.3f}   >= {thr:.2f}     {'MET' if ok else 'NOT MET'}")
    else:
        b = upper_bound(x, n); ok = b <= thr; print(f"{name:38} {x}/{n} fail   <= {b:.3f}   <= {thr:.2f}     {'MET' if ok else 'NOT MET'}")
# staged rollout: if zero critical incidents are seen at each stage, how many requests until the 95% upper bound <= 1%?
print("\nrequests with zero critical incidents needed to bound incident rate <= 1%:", need(0.01), "; <= 0.1%:", need(0.001))
```
**Output (my run):**
```
0 failures in  50: exact upper 0.0582  closed form 0.0582  rule of three 0.0600
0 failures in 100: exact upper 0.0295  closed form 0.0295  rule of three 0.0300
0 failures in 150: exact upper 0.0198  closed form 0.0198  rule of three 0.0200
0 failures in 300: exact upper 0.0099  closed form 0.0099  rule of three 0.0100
2 failures in 40: bound 0.1492; P(X<=2 | p=bound) = 0.0500

cases needed with ZERO failures to bound the failure rate: {0.1: 29, 0.05: 59, 0.02: 149, 0.01: 299}

criterion                              result      95% bound  threshold  verdict
helpfulness pass (human-graded)        182/200 pass   >= 0.869   >= 0.85     MET
grounded in cited source               188/200 pass   >= 0.905   >= 0.90     MET
critical clinical error (fail count)   1/250 fail   <= 0.019   <= 0.02     MET
red-team: harmful compliance           2/80 fail   <= 0.077   <= 0.05     NOT MET
refuses safe requests (over-refusal)   9/200 fail   <= 0.077   <= 0.08     MET

requests with zero critical incidents needed to bound incident rate <= 1%: 299 ; <= 0.1%: 2995
```
**Follow-ups:**
- *What if the thresholds are met by a hair?* Treat it as "not yet proven": grow the sample or stage the launch more cautiously.
- *Who decides?* The product and risk owners, using the evidence; the eval team's job is to make the evidence honest.
- *After launch?* Keep sampling production traces for human review and re-run the red team on every significant change.
**Common mistakes:** thresholds picked after seeing the results; a point estimate with no interval; averaging a critical failure away inside a high overall score; skipping a human review path in a clinical or financial setting; treating launch as the end of evaluation; claiming compliance without asking the compliance team.

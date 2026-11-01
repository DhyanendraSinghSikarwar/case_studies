### Q13 ⭐⭐⭐ 🟡 Code: implement the unbiased pass@k estimator (n samples, c correct) from scratch, check it against brute force, and aggregate it over problems.
**Asked at:** product, big tech, live-coding rounds
**Say this first (1 line):** pass@k = 1 - C(n-c, k) / C(n, k): the chance that a random k-subset of my n samples contains at least one correct one, averaged over problems.

**Then explain:** (concepts are in Q12; this answer is the implementation)
- **Formula:** draw n samples per problem (n >= k), count c correct. pass@k = 1 - C(n-c, k) / C(n, k). If fewer than k samples are wrong (n-c < k), every k-subset has a correct one, so it is 1.0.
- **Stable form:** C(n-c, k) / C(n, k) = product over i from n-c+1 to n of (1 - k/i). No huge binomials, no overflow for n = 200. The Codex paper's reference code is written this way (from memory, check the paper body, which was not opened in this research).
- **Aggregate:** compute per problem, then average over problems. Never average c and n first.
- **Why plug-in is biased:** the tempting estimate 1 - (1 - c/n)^k treats c/n as the true rate. The estimator is nonlinear in c/n, so noise in c does not average out. The code computes the exact expectation over c ~ Binomial(n, p): the unbiased estimator gives the truth, the plug-in is low.
- **pass^k (all k succeed)** is C(c, k) / C(n, k); same brute-force check applies.

**Example:** one problem, n = 10 samples, c = 4 correct. pass@1 = 4/10 = 0.4. pass@5 = 1 - C(6,5)/C(10,5) = 1 - 6/252 = 0.976. pass^3 = C(4,3)/C(10,3) = 4/120 = 0.033. Same problem, three very different answers depending on what "success" means (see the run: values match these hand calculations).

**Code:** (pure stdlib; brute force enumerates every k-subset; toy synthetic (n, c) pairs)
```python
# pass@k from scratch: n samples per problem, c of them correct.
from itertools import combinations
from math import comb, prod

def pass_at_k(n, c, k):
    """Unbiased estimator: 1 - C(n-c, k) / C(n, k), in the stable product form."""
    if not 1 <= k <= n:
        raise ValueError("need 1 <= k <= n")
    if n - c < k:                      # fewer than k wrong samples: every k-subset has a correct one
        return 1.0
    return 1.0 - prod(1.0 - k / i for i in range(n - c + 1, n + 1))

def pass_hat_k(n, c, k):
    """pass^k: probability that k samples drawn without replacement are ALL correct."""
    return comb(c, k) / comb(n, k)

def brute_force(n, c, k, all_k=False):
    """Enumerate every k-subset of the n samples (first c are the correct ones)."""
    good = hits = 0
    for subset in combinations(range(n), k):
        n_ok = sum(1 for i in subset if i < c)
        hits += (n_ok == k) if all_k else (n_ok >= 1)
        good += 1
    return hits / good

# 1) check against brute force over every (n, c, k) with n <= 8
worst = 0.0
for n in range(1, 9):
    for c in range(0, n + 1):
        for k in range(1, n + 1):
            worst = max(worst,
                        abs(pass_at_k(n, c, k) - brute_force(n, c, k)),
                        abs(pass_hat_k(n, c, k) - brute_force(n, c, k, all_k=True)))
print("max |closed form - brute force| over all n<=8:", worst)

# 2) aggregate over problems: (n, c) per problem (toy numbers, synthetic)
problems = {"p1": (10, 10), "p2": (10, 4), "p3": (10, 1), "p4": (10, 0)}
for k in (1, 5, 10):
    vals = [pass_at_k(n, c, k) for n, c in problems.values()]
    print(f"k={k:2d} per-problem", [round(v, 3) for v in vals], "mean pass@k =", round(sum(vals) / len(vals), 4))
print("pass^3 per problem:", [round(pass_hat_k(n, c, 3), 3) for n, c in problems.values()])

# 3) why plug-in 1-(1-c/n)^k is biased: exact expectation over c ~ Binomial(n, p)
p, n, k = 0.2, 5, 3
truth = 1 - (1 - p) ** k
e_unb = sum(comb(n, c) * p**c * (1 - p) ** (n - c) * pass_at_k(n, c, k) for c in range(n + 1))
e_plug = sum(comb(n, c) * p**c * (1 - p) ** (n - c) * (1 - (1 - c / n) ** k) for c in range(n + 1))
print(f"true pass@{k} at p={p}: {truth:.4f} | E[unbiased] = {e_unb:.4f} | E[plug-in] = {e_plug:.4f}")
```
**Output (my run):**
```
max |closed form - brute force| over all n<=8: 1.1102230246251565e-16
k= 1 per-problem [1.0, 0.4, 0.1, 0.0] mean pass@k = 0.375
k= 5 per-problem [1.0, 0.976, 0.5, 0.0] mean pass@k = 0.619
k=10 per-problem [1.0, 1.0, 1.0, 0.0] mean pass@k = 0.75
pass^3 per problem: [1.0, 0.033, 0.0, 0.0]
true pass@3 at p=0.2: 0.4880 | E[unbiased] = 0.4880 | E[plug-in] = 0.4150
```
Reading it: the closed form matches brute force to floating-point error for every n up to 8. The mean over the four toy problems rises from 0.375 (pass@1) to 0.75 (pass@10); the last problem (c = 0) never improves, because no amount of sampling helps if the model cannot do it. The plug-in estimate was 0.4150 against a true 0.4880 (synthetic p = 0.2, n = 5, k = 3).

**Follow-ups:**
- *What if n = k?* Then pass@k is 1 if c >= 1 else 0: just "did any sample pass", which is noisy. Use n larger than k.
- *What n do I need?* Larger n gives a lower-variance estimate; the Codex paper used a few hundred samples per problem for large k (from memory, check). Reported results from the abstract: 28.8% single-sample and 70.2% with 100 samples per problem (reported by the authors, HumanEval, Codex).
- *Confidence interval?* Bootstrap over problems (Q38), because problems, not samples, are the unit of analysis.

**Common mistakes:** the plug-in formula; computing with `math.comb` on big n (slow and overflow-prone in other languages); averaging c and n across problems; sampling k only once and calling it pass@k (high variance); mixing pass@k with pass^k.

### Q14 ⭐⭐⭐ 🟡 How do you do regression testing and CI gates for prompt or model changes (tiered suites, thresholds, flaky results, blocking vs advisory checks)?
**Asked at:** product, GenAI startups, GCC, platform teams; interview-prep guides describe CI release gates (guides, not candidate reports)
**Say this first (1 line):** I treat a prompt or model change like a code change: run a tiered eval suite in CI, block on hard failures and statistically clear regressions, and only warn on noisy or soft signals.

**Then explain:**
- **Tiers:** (1) a small smoke set with deterministic checks that runs on every commit (schema valid, no banned content, critical cases); (2) a fuller suite with a judge on each pull request or nightly; (3) the expensive human or large-judge runs before release. Cheap and fast first (a common pattern in eval guides; the tiering idea comes from vendor and prep blogs, not a standard).
- **Blocking vs advisory:** block on critical-case failures and on a regression whose confidence interval excludes zero; make everything else advisory (visible in the PR, not red). Too many blocking checks teach the team to ignore or bypass the gate.
- **Flakiness:** LLM outputs vary, so one run per case gives false alarms. Repeat each case (3 runs here), compare per case, and use a paired bootstrap over cases for the aggregate change. Fix the flakiest cases or move them to advisory.
- **Thresholds:** a fixed "-3 points" rule needs a noise estimate. One guide's example uses a 3% regression gate (seen in a search snippet, treated as an example, not a rule); calibrate yours from A/A runs (same prompt twice).
- **Pin everything:** model version, temperature, prompts, judge version and dataset version, otherwise a red build cannot be reproduced (see Q43).

**Example:** synthetic suite: 100 cases (10 critical), 3 runs each. Rerunning the same model 200 times, a naive single-run rule "block if the score drops by more than 2 points" blocked 74 times. A CI-aware rule blocked 5 times. With a real regression planted (30 cases at 60% of their old pass probability) the mean dropped 0.133 and the CI excluded zero, so it blocked.

**Code:** (mock model with per-case pass probabilities; every probability is an assumed synthetic input)
```python
# Toy CI gate for a prompt change. The "model" is a mock: each case has a pass probability per run.
import numpy as np

rng = np.random.default_rng(0)
N, R = 100, 3                                   # 100 cases, 3 repeated runs each (synthetic)
tier = np.where(np.arange(N) < 10, "critical", "general")
p_old = np.concatenate([np.full(10, 0.99), rng.choice([0.97, 0.7, 0.3], size=90, p=[0.7, 0.2, 0.1])])

def run(p, rng):                                # returns N x R matrix of 0/1 outcomes
    return (rng.random((N, R)) < p[:, None]).astype(int)

def paired_bootstrap(diff_per_case, rng, B=1000):
    idx = rng.integers(0, len(diff_per_case), size=(B, len(diff_per_case)))
    means = diff_per_case[idx].mean(axis=1)
    return np.percentile(means, [2.5, 97.5])

def gate(old, new, rng, margin=0.03):
    d = new.mean(axis=1) - old.mean(axis=1)     # per-case pass rate change (paired)
    crit = tier == "critical"
    if (new[crit].mean(axis=1) < 0.5).any():
        return "BLOCK (critical case fails most runs)"
    lo, hi = paired_bootstrap(d, rng)
    if hi < 0 and d.mean() < -margin:
        return f"BLOCK (drop {d.mean():+.3f}, 95% CI [{lo:+.3f}, {hi:+.3f}] excludes 0)"
    if d.mean() < -margin:
        return f"ADVISORY (drop {d.mean():+.3f} but CI [{lo:+.3f}, {hi:+.3f}] includes 0)"
    return f"PASS (change {d.mean():+.3f})"

# Same prompt re-run: how often does a naive single-run "drop > 2 points" gate cry wolf?
trials, naive_false = 200, 0
smart_false = 0
for t in range(trials):
    r = np.random.default_rng(1000 + t)
    a, b = run(p_old, r)[:, :1], run(p_old, r)[:, :1]          # one run each, identical model
    naive_false += (b.mean() - a.mean()) < -0.02
    a3, b3 = run(p_old, r), run(p_old, r)
    smart_false += gate(a3, b3, r).startswith("BLOCK")
print(f"identical model, {trials} CI runs: naive single-run gate blocked {naive_false}, CI-aware gate blocked {smart_false}")

old = run(p_old, rng)
p_bad = p_old.copy(); p_bad[10:40] *= 0.6        # real regression on 30 general cases
p_noise = p_old.copy(); p_noise[10:20] -= 0.1    # tiny change on 10 cases
p_crit = p_old.copy(); p_crit[:2] = 0.1          # two critical cases break, rest identical
for name, p in [("identical", p_old), ("small change", p_noise), ("real regression", p_bad), ("critical broken", p_crit)]:
    print(f"{name:16s} ->", gate(old, run(p, rng), rng))
```
**Output (my run):**
```
identical model, 200 CI runs: naive single-run gate blocked 74, CI-aware gate blocked 5
identical        -> PASS (change +0.023)
small change     -> PASS (change +0.013)
real regression  -> BLOCK (drop -0.133, 95% CI [-0.203, -0.070] excludes 0)
critical broken  -> BLOCK (critical case fails most runs)
```
Honest reading: "identical" showed a +0.023 change from pure noise, which is why a point-estimate gate misfires. With 100 cases the CI-aware gate only catches large drops; it will miss a true 1-2 point regression (Q26 covers how many cases you need).

**Follow-ups:**
- *Should the judge be in the gate?* Only a validated judge (Q6), pinned, with its own regression check; otherwise a judge update looks like a model regression.
- *Where do new cases come from?* Production failures (Q15), added after each incident.
- *Agent or multi-step flows?* See Part 8 Q39 and Q51 for trajectory and non-deterministic suites.

**Common mistakes:** one run per case; a hard threshold with no noise estimate; making every check blocking; letting the model, prompt and judge change at the same time; running the full suite on every commit and then skipping it because it is slow and expensive.

### Q15 ⭐⭐⭐ 🟡 How do you do error analysis on an LLM product (read traces, open coding, group into a failure taxonomy, count, prioritise) and turn the findings into evals?
**Asked at:** product, GenAI startups, evaluation-focused rounds, senior roles
**Say this first (1 line):** read real traces, write a free-text note on what went wrong in each, group the notes into a small failure taxonomy, count them, fix the biggest cheap category first, and turn each category into a test.

**Then explain:**
- **Sample and read:** pull real traces (not synthetic), look at the whole trace including tool calls and retrieved context. A practitioner guide (Hamel Husain's FAQ, opened) suggests about 100 traces as a start and reading until no new failure types appear (his guidance, not a standard).
- **Open coding:** one short note per failing trace, in plain words ("quotes old refund window"). Do not start from a fixed list; you will miss the product's own failures.
- **Axial coding:** merge notes into 5-10 categories. Keep a "none/other" bucket; revisit when it grows.
- **Count and prioritise:** counts show frequency, not importance; weigh by user harm and by fix cost. The code uses count / cost, an assumed heuristic.
- **Turn into evals:** a deterministic check where possible (code beats judge), a binary judge for the fuzzy ones, validated on human labels (Q6, Q7).

**Example:** 40 synthetic failing traces coded into 5 categories. Stale knowledge is the largest bucket (11, 28%), yet fabricated identifiers (10, 25%) come first by count/cost because the fix is cheap (require ids to come from tool output). The check at the end catches the fake order id in the second toy answer.

**Code:** (stdlib only; traces and fix costs are synthetic, assumed)
```python
# Toy error analysis: open codes -> failure taxonomy -> counts -> priority -> eval checks. All traces SYNTHETIC.
from collections import Counter

# step 1-2: reviewer's open-coding notes on 40 failing traces (one note per trace), then grouped (axial coding)
taxonomy = {
    "quotes old refund window": "stale knowledge",
    "cites 2022 policy": "stale knowledge",
    "ignored date filter": "retrieval filter",
    "searched wrong product line": "retrieval filter",
    "made up order id": "fabricated identifier",
    "invented ticket number": "fabricated identifier",
    "tool timeout then guessed": "tool error not handled",
    "too apologetic, no answer": "tone / no answer",
}
notes = (["quotes old refund window"] * 7 + ["cites 2022 policy"] * 4 + ["ignored date filter"] * 6
         + ["searched wrong product line"] * 3 + ["made up order id"] * 8 + ["invented ticket number"] * 2
         + ["tool timeout then guessed"] * 6 + ["too apologetic, no answer"] * 4)
cats = Counter(taxonomy[n] for n in notes)
print("traces coded:", len(notes))
fix_cost = {"stale knowledge": 2, "retrieval filter": 1, "fabricated identifier": 1, "tool error not handled": 2, "tone / no answer": 3}
print(f"{'category':24s}{'count':>6s}{'share':>8s}{'cost(1-3)':>11s}{'priority=count/cost':>21s}")
rows = sorted(cats.items(), key=lambda kv: -kv[1] / fix_cost[kv[0]])
for cat, cnt in rows:
    print(f"{cat:24s}{cnt:6d}{cnt/len(notes):8.0%}{fix_cost[cat]:11d}{cnt/fix_cost[cat]:21.1f}")

# step 3: turn the top category into a deterministic eval (no judge needed)
import re
def no_fabricated_order_id(answer, tool_results):
    ids = re.findall(r"\bORD-\d{4}\b", answer)
    return all(i in tool_results for i in ids)           # every quoted id must appear in a tool result

cases = [("Your order ORD-1234 ships Monday.", "order ORD-1234 found"),
         ("Order ORD-9999 is delayed.", "order ORD-1234 found"),
         ("I could not find an order.", "no orders")]
print("fabricated-id check:", [no_fabricated_order_id(a, t) for a, t in cases])
```
**Output (my run):**
```
traces coded: 40
category                 count   share  cost(1-3)  priority=count/cost
fabricated identifier       10     25%          1                 10.0
retrieval filter             9     22%          1                  9.0
stale knowledge             11     28%          2                  5.5
tool error not handled       6     15%          2                  3.0
tone / no answer             4     10%          3                  1.3
fabricated-id check: [True, False, True]
```
**Follow-ups:**
- *How many traces?* Until new notes stop adding categories; the 100 above is a starting point from one practitioner, not a rule.
- *Who codes?* Ideally a domain expert; two people on a subset, with kappa (Q25), if the categories are contested.
- *How does this relate to a golden set?* The failures become cases in it (Q2).

**Common mistakes:** starting from generic metrics (helpfulness, toxicity) instead of reading traces; asking an LLM to invent the taxonomy without reading anything; prioritising by count only; one giant "bad answer" category; never turning the findings into automated tests.

### Q16 ⭐⭐ 🟡 Context precision and context recall in depth: how are they computed, what do they need (reference answer or labelled chunks), why is precision rank-aware, and how do you read the four combinations of high and low?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** context precision asks "are the relevant chunks ranked near the top?" and context recall asks "did the retrieved chunks contain everything needed for the reference answer?"; read them together.

**Then explain:**
- **Context recall (Ragas docs, opened in this run):** the reference answer is split into claims and each is checked against the retrieved context: supported claims / total claims. It always needs a reference. Non-LLM and ID-based variants compare retrieved contexts or ids with labelled reference contexts directly.
- **Context precision (Ragas docs, opened earlier):** rank-aware. Take precision@k at each rank k where the chunk is relevant and average those values. Plain precision ignores order; this one rewards putting good chunks first.
- **What you need:** a reference answer for the claim-based recall, or labelled gold chunks/ids for the ID-based one. Relevance per chunk comes from an LLM judge or labels.
- **Reading the four cells:** high P / high R fine. High P / low R: what you retrieved is good but you retrieve too little (raise k, better recall). Low P / high R: all the needed facts are there, buried in noise (re-rank, reduce k). Low P / low R: retrieval is broken.
- **Limits:** claim-based recall is judge-dependent (a mock substring judge below); both need a reference, so they fit offline sets, not production.

**Example:** same three chunks, relevant ones at ranks (1,1,0), (1,0,1), (0,1,1): plain precision is 0.667 for all three, rank-aware is 1.000, 0.833, 0.583.

**Code:** (mock keyword judge; toy chunks and reference; hand-checked assert inside)
```python
# Context precision (rank-aware) and context recall (claim-based and ID-based) on toy data.
def context_precision(rels):
    """Ragas-style: mean of precision@k taken only at ranks k where the chunk is relevant."""
    if not any(rels):
        return 0.0
    hits, total = 0, 0.0
    for k, r in enumerate(rels, start=1):
        if r:
            hits += 1
            total += hits / k
    return total / hits

def plain_precision(rels):                      # not rank-aware
    return sum(rels) / len(rels)

# check against a hand-computed value: relevant at ranks 2 and 3 of 3 -> (1/2 + 2/3) / 2 = 0.5833
assert abs(context_precision([0, 1, 1]) - (1/2 + 2/3) / 2) < 1e-12
for rels in ([1, 1, 0], [1, 0, 1], [0, 1, 1]):
    print(f"relevance by rank {rels}: plain precision {plain_precision(rels):.3f}, rank-aware {context_precision(rels):.3f}")

def mock_supports(claim_keywords, chunks):      # mock judge: a claim is supported if all its keywords appear in some chunk
    return any(all(w in ch for w in claim_keywords) for ch in chunks)

def claim_recall(reference_claims, chunks):
    return sum(mock_supports(c, chunks) for c in reference_claims) / len(reference_claims)

def id_recall(gold_ids, retrieved_ids):
    return len(set(gold_ids) & set(retrieved_ids)) / len(set(gold_ids))

# reference answer (toy): "Refunds take 5 days. Cards only. Not for sale items."
claims = [("5 days",), ("cards",), ("sale items", "not")]
chunks = {"A": "refunds take 5 days to arrive", "B": "refunds go to cards only", "C": "sale items are not refundable",
          "X": "our office is in Pune", "Y": "holiday list for 2024"}
gold = ["A", "B", "C"]
scenarios = {
    "high P, high R": ["A", "B", "C"],
    "high P, low R":  ["A"],
    "low P, high R":  ["X", "Y", "A", "B", "C"],
    "low P, low R":   ["X", "Y", "A"],
}
print(f"{'scenario':16s}{'precision':>10s}{'recall(claims)':>16s}{'recall(ids)':>13s}")
for name, ids in scenarios.items():
    rels = [1 if i in gold else 0 for i in ids]
    print(f"{name:16s}{context_precision(rels):10.3f}{claim_recall(claims, [chunks[i] for i in ids]):16.3f}{id_recall(gold, ids):13.3f}")
```
**Output (my run):**
```
relevance by rank [1, 1, 0]: plain precision 0.667, rank-aware 1.000
relevance by rank [1, 0, 1]: plain precision 0.667, rank-aware 0.833
relevance by rank [0, 1, 1]: plain precision 0.667, rank-aware 0.583
scenario         precision  recall(claims)  recall(ids)
high P, high R       1.000           1.000        1.000
high P, low R        1.000           0.333        0.333
low P, high R        0.478           1.000        1.000
low P, low R         0.333           0.333        0.333
```
The low-P/high-R scenario scores 0.478: relevant chunks sit at ranks 3-5 (1/3, 2/4, 3/5 averaged).

**Follow-ups:**
- *Why not just recall@k?* It is the retrieval-metrics view from Part 6 Q10; the Ragas variants need no chunk labels because an LLM judges relevance.
- *Does high precision mean a good answer?* No: generation can still ignore the context (Q8).

**Common mistakes:** calling the metric "precision@k" (it is rank-aware and averaged only over relevant ranks); reading recall as "did the answer include everything" (it is about the context, not the answer); trusting an LLM relevance judge without checking it on a labelled sample.

### Q17 ⭐⭐ 🟡 A RAG assistant is wrong a third of the time and you only have logs. How do you separate retrieval failures from generation failures, handle unanswerable questions, and decide what to fix first?
**Asked at:** product, GenAI startups, GCC; an interview-prep guide poses this scenario (a guide, not a candidate report)
**Say this first (1 line):** from logs I first label a sample of failures by whether the right evidence was retrieved, then whether the question was answerable, and fix whichever bucket is largest and cheapest.

**Then explain:**
- **Decision tree per failed log:** (1) Was the question answerable from the corpus at all? If not, the right behaviour is abstain. (2) If yes, was a gold chunk in the retrieved top-k? No: retrieval failure. (3) Yes, but the answer is wrong or unfaithful: generation failure (Q8).
- **No labels yet:** review a random sample of failures by hand (about 80 here; a size I chose, not a standard); use an LLM judge only after validating it (Q6).
- **Unanswerable questions:** track abstention rate and "answered when it should not" separately; they look like generation errors but come from missing content or missing instructions.
- **What to fix first:** the biggest bucket, weighted by fix cost. Retrieval miss: chunking, query rewriting, hybrid search. Generation error: prompt, model. Unanswerable: abstention rule and threshold.
- **Link:** the same split as Part 6 Q10 and Q39 (retrieval and generation evaluated separately).

**Example (synthetic, assumed rates):** 300 logs, 33.0% wrong. True split: 57 retrieval misses (58% of failures), 18 generation errors (18%), 24 answered-unanswerable (24%). A reviewed sample of 80 failures gave 55%, 19%, 26%: close, so retrieval comes first.

**Code:** (simulated logs: 85% answerable, 75% retrieval hit, other probabilities assumed)
```python
# Separating retrieval from generation failures from logs. Everything here is SYNTHETIC (assumed rates).
import numpy as np
from collections import Counter

rng = np.random.default_rng(7)
N = 300
logs = []
for i in range(N):
    answerable = rng.random() < 0.85
    if answerable:
        hit = rng.random() < 0.75                       # gold chunk in the top-k?
        correct = rng.random() < (0.90 if hit else 0.10)
        abstained = (not correct) and rng.random() < 0.2
        bucket = "ok" if correct else ("retrieval miss" if not hit else "generation error")
        if abstained and not hit: bucket = "retrieval miss"
    else:
        hit = False
        abstained = rng.random() < 0.4
        correct = abstained
        bucket = "ok" if correct else "answered unanswerable"
    logs.append(dict(answerable=answerable, hit=hit, correct=correct, bucket=bucket))

true_counts = Counter(l["bucket"] for l in logs)
wrong = sum(v for k, v in true_counts.items() if k != "ok")
print(f"wrong overall: {wrong}/{N} = {wrong/N:.1%}")
for k in ("retrieval miss", "generation error", "answered unanswerable"):
    print(f"  {k:22s}{true_counts[k]:4d}  ({true_counts[k]/wrong:.0%} of failures)")

# Reviewer labels a random sample of 80 FAILED logs (open the trace: was the gold chunk in the top-k? answerable at all?)
failed = [l for l in logs if l["bucket"] != "ok"]
sample = [failed[i] for i in rng.choice(len(failed), size=80, replace=False)]
sc = Counter(l["bucket"] for l in sample)
print("reviewed sample of 80 failures:", {k: f"{v/80:.0%}" for k, v in sc.most_common()})
print("rule: fix the biggest bucket first (retrieval miss -> chunking, query rewriting, hybrid search; "
      "generation error -> prompt/model; unanswerable -> abstention instruction + threshold)")
```
**Output (my run):**
```
wrong overall: 99/300 = 33.0%
  retrieval miss          57  (58% of failures)
  generation error        18  (18% of failures)
  answered unanswerable   24  (24% of failures)
reviewed sample of 80 failures: {'retrieval miss': '55%', 'answered unanswerable': '26%', 'generation error': '19%'}
rule: fix the biggest bucket first (retrieval miss -> chunking, query rewriting, hybrid search; generation error -> prompt/model; unanswerable -> abstention instruction + threshold)
```
**Follow-ups:**
- *Retrieved the gold chunk but the answer is wrong?* Generation or context-use problem; check position of the chunk and context length.
- *Wrong a third of the time, is that high?* Depends on stakes; the point is the breakdown, not the rate.
- *Sample size?* The 80-failure sample gives each bucket share about plus or minus 10 points; enough to rank buckets here, not to quote percentages precisely.

**Common mistakes:** fixing the prompt first by default; mixing unanswerable questions into the retrieval-failure bucket; judging retrieval by answer correctness (the model can be right from memory); treating logs without labels as ground truth.

### Q18 ⭐⭐ 🟡 How do you run pairwise comparisons properly (swap order, ties, win rate with a confidence interval, which judge, when pairwise beats absolute scores)?
**Asked at:** product, GenAI startups, evaluation-focused rounds
**Say this first (1 line):** show each pair in both orders, count a win only when the verdict survives the swap, report ties, and give the win rate with a confidence interval over prompts.

**Then explain:**
- **Swap order:** judges favour a position (Q5; the MT-Bench paper measured it, see Q19). Run (A,B) and (B,A); the same answer winning twice is a win, a flip is a tie (the MT-Bench mitigation, as returned by a fetch of the paper, check).
- **Ties:** keep them, and count them half when you compute a win rate, or report W/T/L. Dropping ties inflates the gap.
- **Interval:** the unit is the prompt, so bootstrap over prompts (or a Wilson interval on non-tie wins). Below, bootstrap and the closed-form standard error agree.
- **Which judge:** a stronger or different-family judge than the systems; validated against human labels on a sample (Q6); not one of the two systems (self-preference, Q5).
- **Pairwise vs absolute:** pairwise is easier for both humans and judges and more sensitive to small differences; absolute scores are needed for thresholds, trends over time and CI gates. Pairwise cost grows with the number of systems.

**Example (synthetic judge with an assumed position bias):** 200 prompts. Always showing the new answer first gives a 67.5% win rate. After the swap check: 68 wins, 52 losses, 80 ties (40% flipped), win rate 0.540, 95% CI [0.487, 0.593], which includes 0.5: not clearly better. The true share of prompts where new is better was 0.55.

**Code:** (mock judge with assumed bias; numpy only)
```python
# Pairwise comparison with a mock judge that has position bias. All numbers synthetic.
import numpy as np
rng = np.random.default_rng(3)
N = 200
gap = rng.normal(0.15, 1.0, N)               # true quality gap new - old per prompt (new slightly better, assumed)
POS_BIAS = 0.8                                # judge's logit boost for whichever answer is shown first (assumed)

def judge_prefers_first(first_minus_second):  # mock judge: 1 if the first-shown answer wins
    p = 1 / (1 + np.exp(-(2.0 * first_minus_second + POS_BIAS)))
    return (rng.random(first_minus_second.shape) < p).astype(int)

# Naive: new answer always shown first
naive_win = judge_prefers_first(gap)
# Proper: judge twice, swapping order; win only if the same answer wins both times, else tie
new_first = judge_prefers_first(gap)                 # 1 = new wins
old_first = 1 - judge_prefers_first(-gap)            # 1 = new wins (first-shown was old)
wins = (new_first == 1) & (old_first == 1)
losses = (new_first == 0) & (old_first == 0)
ties = ~(wins | losses)
score = wins + 0.5 * ties                            # per-prompt score in {0, 0.5, 1}
print(f"naive (new always first): win rate {naive_win.mean():.3f}")
print(f"swap-checked: wins {wins.sum()}, losses {losses.sum()}, ties {ties.sum()} (tie = order flipped the verdict: {ties.mean():.0%})")
print(f"swap-checked win rate (ties count half): {score.mean():.3f}")

B = rng.integers(0, N, size=(5000, N))
boot = score[B].mean(axis=1)
lo, hi = np.percentile(boot, [2.5, 97.5])
se_formula = score.std(ddof=1) / np.sqrt(N)          # closed form for a mean
print(f"bootstrap 95% CI [{lo:.3f}, {hi:.3f}]; normal approx [{score.mean()-1.96*se_formula:.3f}, {score.mean()+1.96*se_formula:.3f}]")
print("true share of prompts where new is better:", round((gap > 0).mean(), 3))
```
**Output (my run):**
```
naive (new always first): win rate 0.675
swap-checked: wins 68, losses 52, ties 80 (tie = order flipped the verdict: 40%)
swap-checked win rate (ties count half): 0.540
bootstrap 95% CI [0.487, 0.593]; normal approx [0.486, 0.594]
true share of prompts where new is better: 0.55
```
**Follow-ups:**
- *How many prompts?* The CI half-width here is about 0.05 at 200; Q26 gives the sample-size calculation.
- *Many systems?* Fit Bradley-Terry instead of raw win rates (Q20, Q37).

**Common mistakes:** one fixed order; discarding ties; no interval; letting one of the systems judge itself; reading a win rate of 0.54 as "better".

### Q19 ⭐⭐ 🟡 What did the MT-Bench and Chatbot Arena paper (Judging LLM-as-a-Judge) report: the biases, the agreement with humans, what MT-Bench is, and what does the agreement claim not show?
**Asked at:** product, GenAI startups, research-leaning teams
**Say this first (1 line):** the paper (Zheng et al., 2023) introduced MT-Bench, a set of 80 two-turn questions, and Chatbot Arena as the human reference, and reported that a strong judge (GPT-4) agrees with humans about as often as humans agree with each other; it also measured judge biases, and agreement does not show the judge is right on the cases that matter.

**Then explain:**
- **Numbers below are the authors' reported results**, read from a fetch of the arXiv HTML (the fetch tool summarises the page, so verify exact figures in the paper). The abstract was opened earlier: over 80% agreement, about human-human level.
- **MT-Bench:** 80 questions, 8 categories, 2 turns each. Human data: about 3K expert votes from 58 labelers; Arena: about 30K votes collected over one month, with 3K sampled for the agreement analysis.
- **Biases:** position bias (consistency under swapped order with the default prompt: GPT-4 65.0%, GPT-3.5 46.2%, Claude-v1 23.8%); verbosity (on a repetitive-list attack, Claude-v1 and GPT-3.5 failed 91.3% of 23 answers, GPT-4 8.7%); self-enhancement (GPT-4 favoured itself by about 10 points, Claude-v1 by about 25, GPT-3.5 not at all, but the authors say the data cannot settle it); limited ability to grade math and reasoning.
- **Mitigations the paper tried:** swap positions; chain-of-thought; reference-guided grading (math failures: 14 of 20 default, 6 of 20 with chain-of-thought, 3 of 20 with a reference); few-shot examples (GPT-4 consistency 65.0% to 77.5%).
- **Agreement:** MT-Bench first turn, GPT-4 vs human 66% (setup S1) and 85% (S2), human-human 63% and 81%. From memory (check): S1 counts ties as a label, S2 excludes ties, which is why S2 is higher.
- **What it does not show:** (a) agreement is an average, subsets can be bad; (b) the questions are a small, general chat set, not your task; (c) the authors stress helpfulness and largely leave safety aside; (d) agreement with a crowd or experts is not accuracy; (e) judges and humans can share the same bias (for example towards length).

**Example (synthetic, not the paper's data):** a toy judge matches humans 69.4% on non-tie pairs overall, yet agrees only 27.1% where the longer answer is the worse one, 90.2% elsewhere. A headline agreement number hides this; slice by length difference.

**Code:** (simulated humans and judge; every rate is assumed)
```python
# What an "agreement with humans" number can hide. Synthetic judge and humans (assumed rates), not the paper's data.
import numpy as np
rng = np.random.default_rng(11)
N = 1000
# human label: 'A', 'B' or 'tie'
human = rng.choice(["A", "B", "tie"], size=N, p=[0.4, 0.4, 0.2])
length_mismatch = rng.random(N) < 0.3                 # 30% of items: the longer answer is the WORSE one (assumed)
judge = []
for h, lm in zip(human, length_mismatch):
    if h == "tie":
        judge.append(rng.choice(["A", "B", "tie"], p=[0.35, 0.35, 0.30]))
    elif lm and rng.random() < 0.7:                   # judge is lured by the longer (worse) answer 70% of the time
        judge.append("B" if h == "A" else "A")
    else:
        judge.append(h if rng.random() < 0.9 else ("B" if h == "A" else "A"))
judge = np.array(judge)
agree = judge == human
print(f"agreement counting ties as a label (3-way): {agree.mean():.3f}")
no_tie = (human != "tie") & (judge != "tie")
print(f"agreement on non-tie pairs only:            {agree[no_tie].mean():.3f}  (n={no_tie.sum()})")
nt = human != "tie"
print(f"  ... on items where longer = better/equal: {agree[nt & ~length_mismatch].mean():.3f}")
print(f"  ... on items where longer = worse:        {agree[nt & length_mismatch].mean():.3f}")
```
**Output (my run):**
```
agreement counting ties as a label (3-way): 0.627
agreement on non-tie pairs only:            0.694  (n=818)
  ... on items where longer = better/equal: 0.902
  ... on items where longer = worse:        0.271
```
Note also the tie effect: 3-way agreement 0.627 versus 0.694 on non-tie pairs, so always ask how ties were treated.

**Follow-ups:**
- *Is 85% good?* Compare with human-human on the same setup, which the paper does; also look at chance level (kappa, Q6).
- *So can I trust a judge?* Validate on my own labelled sample before relying on it (Q6, Q45).

**Common mistakes:** quoting "80% agreement" without the setting and tie handling; treating MT-Bench scores as a product eval; saying the paper proved self-preference (the authors said the data was not enough); forgetting safety is outside the paper's scope.

### Q20 ⭐⭐ 🟡 How does Chatbot Arena turn pairwise human votes into a ranking (Elo vs Bradley-Terry, confidence intervals, style control), and what are its blind spots?
**Asked at:** product, GenAI startups, research-leaning teams
**Say this first (1 line):** Arena collects pairwise human votes and fits a Bradley-Terry model, which gives order-independent ratings with bootstrap confidence intervals; style control adds covariates such as answer length so verbose models are not rewarded for length alone.

**Then explain:**
- **Elo vs Bradley-Terry:** Elo updates ratings one battle at a time, so the result depends on the order of battles. Bradley-Terry fits all battles at once by maximum likelihood (logistic model of win probability on the skill difference). LMSYS's blog described moving from online Elo to Bradley-Terry for more stable ratings and tighter intervals (a search snippet, blog not opened; the paper abstract, opened, mentions statistical methods for ranking over 240K votes). Full code is Q37.
- **Confidence intervals:** bootstrap the battles, refit, take percentiles; rankings with overlapping intervals are effectively tied.
- **Style control:** add features like length difference to the logistic regression so the model skill is estimated holding style fixed. That Arena uses it, and exactly how, is from a snippet; check the live methodology page.
- **Blind spots:** voters are self-selected users with their own prompts, not your users; preferences reward style and length; short single-turn chat dominates, so coding agents or long tasks are under-represented; votes tell which answer was liked, not which was correct; sampling and model-release patterns affect who is compared with whom (from memory, check).

**Example (synthetic battles, 4,000):** true skills A 0.0, B 0.5, C 0.2 (logit), voters like longer answers (true length coefficient 0.8), C is much longer. Plain BT puts C at +0.93 [+0.83, +1.00], first. With a length covariate C falls to +0.19 [+0.06, +0.29] and B is first at +0.43; the recovered length coefficient is +0.79. Elo on shuffles of the same battles moved by 97-169 rating points per model.

**Code:** (numpy only; Newton's method logistic fit; all strengths and the length taste are assumed)
```python
# Arena-style ranking: Bradley-Terry by Newton's method, bootstrap CIs, a style (length) control, and Elo order sensitivity.
import numpy as np
rng = np.random.default_rng(5)
M, names = 3, ["Model-A", "Model-B", "Model-C"]
skill = np.array([0.0, 0.5, 0.2])         # TRUE skill (logit scale, assumed)
mean_len = np.array([0.0, 0.0, 1.0])      # Model-C writes much longer answers on average (assumed)
GAMMA = 0.8                               # voters' true taste for the longer answer (assumed)

n = 4000
i = rng.integers(0, M, n); j = (i + rng.integers(1, M, n)) % M
length = mean_len[:, None] + rng.normal(0, 0.5, (M, n))   # length score of each model's answer in each battle (assumed)
dlen = length[i, np.arange(n)] - length[j, np.arange(n)]
z = skill[i] - skill[j] + GAMMA * dlen
y = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(float)   # 1 if i wins (no ties in this toy)

def design(i, j, style):
    X = np.zeros((len(i), M - 1 + (1 if style else 0)))
    for r, (a, b) in enumerate(zip(i, j)):
        if a > 0: X[r, a - 1] += 1
        if b > 0: X[r, b - 1] -= 1
        if style: X[r, -1] = dlen[r]
    return X

def fit(X, y, iters=25, l2=1e-4):
    beta = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ beta))
        g = X.T @ (y - p) - l2 * beta
        H = (X * (p * (1 - p))[:, None]).T @ X + l2 * np.eye(len(beta))
        beta += np.linalg.solve(H, g)
    return beta

for style in (False, True):
    X = design(i, j, style)
    b = fit(X, y)
    sk = np.concatenate([[0.0], b[:M - 1]])
    boots = []
    for _ in range(100):
        idx = rng.integers(0, n, n)
        bb = fit(X[idx], y[idx]); boots.append(np.concatenate([[0.0], bb[:M - 1]]))
    lo, hi = np.percentile(boots, [2.5, 97.5], axis=0)
    print("style control" if style else "plain BT     ", {nm: f"{s:+.2f} [{l:+.2f},{h:+.2f}]" for nm, s, l, h in zip(names, sk, lo, hi)},
          f"| length coef {b[-1]:+.2f}" if style else "")
print("true skills vs A:", dict(zip(names, skill.tolist())), "true length taste:", GAMMA)

# Elo: same battles, different order -> different final ratings (Q37 builds this out in full)
def elo(order, K=32):
    r = np.full(M, 1000.0)
    for t in order:
        a, b = i[t], j[t]
        ea = 1 / (1 + 10 ** ((r[b] - r[a]) / 400))
        r[a] += K * (y[t] - ea); r[b] -= K * (y[t] - ea)
    return r
runs = np.array([elo(rng.permutation(n)) for _ in range(20)])
print("Elo over 20 shuffles of the same battles, min-max range per model:", dict(zip(names, (runs.max(0) - runs.min(0)).round(0).tolist())))
```
**Output (my run):**
```
plain BT      {'Model-A': '+0.00 [+0.00,+0.00]', 'Model-B': '+0.41 [+0.31,+0.50]', 'Model-C': '+0.93 [+0.83,+1.00]'} 
style control {'Model-A': '+0.00 [+0.00,+0.00]', 'Model-B': '+0.43 [+0.34,+0.54]', 'Model-C': '+0.19 [+0.06,+0.29]'} | length coef +0.79
true skills vs A: {'Model-A': 0.0, 'Model-B': 0.5, 'Model-C': 0.2} true length taste: 0.8
Elo over 20 shuffles of the same battles, min-max range per model: {'Model-A': 169.0, 'Model-B': 97.0, 'Model-C': 161.0}
```
**Follow-ups:**
- *Why not raw win rate?* It depends on who each model happened to face; BT adjusts for opponents.
- *Ties?* Treated as half a win each, or dropped, depending on implementation (check the current method).
- *Can style control remove all bias?* Only the style features you include.

**Common mistakes:** quoting Elo as if order did not matter; ignoring intervals; reading Arena rank as "best for my task"; unidentified style control (needs per-battle length variation; with one verbose model and a fixed length difference it cannot be separated from skill).

### Q21 ⭐⭐ 🟡 Benchmark contamination and saturation: how do you detect leakage, what do held-out, dynamic or refreshed benchmarks do (LiveCodeBench-style), and how should you read a leaderboard?
**Asked at:** product, GenAI startups, research-leaning teams; see also Part 2 Q30 on decontamination
**Say this first (1 line):** contamination means test items leaked into training data, so scores overstate ability; I check with overlap tests and perturbation tests, prefer fresh or held-out benchmarks, and read leaderboards as a screen, not a verdict.

**Then explain:**
- **Detect, method 1: n-gram overlap** between benchmark items and the training corpus. Needs corpus access, and misses paraphrase (see the run: 0 of 10 paraphrased items flagged).
- **Method 2: perturbation.** Re-ask with changed numbers or reworded options; a model that memorised drops sharply. Needs no corpus.
- **Method 3: probing the model.** An opened paper (arXiv 2311.09783, abstract) reports that some commercial models can fill in masked MMLU options (exact match 52% for ChatGPT, 57% for GPT-4, authors' claim in their setting).
- **Dynamic benchmarks:** LiveCodeBench keeps adding new contest problems with dates, so you can score only problems released after a model's training cutoff (abstract opened: 400 problems from May 2023 to May 2024 at that time; reports possible overfitting on HumanEval and MBPP).
- **Saturation:** when top models cluster near the ceiling, the benchmark no longer separates them; MMLU-Pro (abstract opened) reports accuracy drops of 16-33% versus MMLU, authors' claim.
- **Reading a leaderboard:** check the evaluation setup (the Hugging Face post, opened, shows one model scoring 0.637, 0.488 and 0.636 on MMLU in three implementations), date versus training cutoff, whether the weights are open, and whether your task resembles the benchmark. See Part 2 Q30 for decontaminating pretraining data.

**Example (synthetic):** 100 items, 30 verbatim in the corpus, 10 paraphrased in it, 60 clean. The 8-gram check flags 30, 0 and 0. A memorising mock model scores 1.00 on both leaked groups, 0.45 on clean items. With fresh numbers the leaked groups fall to 0.03 and 0.00, while clean items stay at 0.40: that gap exposes the paraphrased leak the n-gram check missed.

**Code:** (pure stdlib; pseudo-word templated questions; the "model" is a lookup plus coin flips)
```python
# Contamination: n-gram overlap detector vs a perturbation test. Benchmark, corpus and "model" are all SYNTHETIC.
import random
rng = random.Random(4)
WORDS = [f"w{k}" for k in range(300)]                 # pseudo-words so items do not share long phrases by accident

def make_item(i):
    w1, w2, w3, w4 = rng.sample(WORDS, 4); a, b = rng.randint(12, 99), rng.randint(12, 99)
    return dict(id=i, parts=(w1, w2, w3, w4, a, b), ans=a + b)

def text(parts, swap=False):
    w1, w2, w3, w4, a, b = parts
    if swap: a, w3, b, w4 = b, w4, a, w3              # paraphrase: the two clauses come in the other order
    return f"{w1} sells {a} {w2} on {w3} and {b} {w2} on {w4} how many {w2} were sold in total"

bench = [make_item(i) for i in range(100)]
kind = {i: ("verbatim" if i < 30 else "paraphrased" if i < 40 else "clean") for i in range(100)}
corpus = [f"filler document number {k} about cooking travel and music " * 3 for k in range(200)]
for it in bench:
    if kind[it["id"]] == "verbatim":    corpus.append(text(it["parts"]) + f" the answer is {it['ans']}")
    if kind[it["id"]] == "paraphrased": corpus.append(text(it["parts"], swap=True) + f" the answer is {it['ans']}")

def ngrams(t, n=8):
    w = t.split(); return {" ".join(w[i:i+n]) for i in range(len(w) - n + 1)}
corpus_grams = set().union(*(ngrams(d) for d in corpus))
for k in ("verbatim", "paraphrased", "clean"):
    ids = [i for i in kind if kind[i] == k]
    hit = sum(bool(ngrams(text(bench[i]["parts"])) & corpus_grams) for i in ids)
    print(f"{k:12s} items {len(ids):3d}: flagged by 8-gram overlap {hit:3d}")

memorised = {i for i in kind if kind[i] != "clean"}   # the mock model saw both verbatim and paraphrased items
def model(item_id, solve_prob=0.5):
    if item_id in memorised:
        return bench[item_id]["ans"]                  # recalls the stored answer, whatever the question now says
    return None                                       # None = tries to solve; handled by caller

def accuracy(ids, fresh_numbers):
    ok = 0
    for i in ids:
        parts = list(bench[i]["parts"])
        if fresh_numbers: parts[4], parts[5] = rng.randint(12, 99), rng.randint(12, 99)
        truth = parts[4] + parts[5]
        out = model(i)
        ok += (out == truth) if out is not None else (rng.random() < 0.5)
    return ok / len(ids)

for k in ("verbatim", "paraphrased", "clean"):
    ids = [i for i in kind if kind[i] == k]
    print(f"{k:12s} accuracy original {accuracy(ids, False):.2f} | with fresh numbers {accuracy(ids, True):.2f}")
```
**Output (my run):**
```
verbatim     items  30: flagged by 8-gram overlap  30
paraphrased  items  10: flagged by 8-gram overlap   0
clean        items  60: flagged by 8-gram overlap   0
verbatim     accuracy original 1.00 | with fresh numbers 0.03
paraphrased  accuracy original 1.00 | with fresh numbers 0.00
clean        accuracy original 0.45 | with fresh numbers 0.40
```
**Follow-ups:**
- *Can I prove a model was not trained on a benchmark?* No, only gather evidence.
- *Private test sets?* Help, but you must trust the host and rotation.
- *Is a held-out split enough?* Only if it is truly unseen by training and by prompt tuning (Q2).

**Common mistakes:** trusting a 0-overlap result as clean; comparing models with different shot counts or prompts; ignoring the training cutoff on dynamic benchmarks; treating saturation as "model is solved".

### Q22 ⭐⭐ 🟡 What do code benchmarks measure and miss (HumanEval and MBPP functional tests, SWE-bench and SWE-bench Verified), and how can weak tests or saturation mislead you?
**Asked at:** product, big tech, code-model teams
**Say this first (1 line):** HumanEval and MBPP measure whether a short function passes unit tests, SWE-bench measures whether a patch fixes a real repository issue; all of them measure only what the tests check, so weak tests and saturation make scores look better than the model is.

**Then explain:**
- **HumanEval / MBPP:** functional correctness from a docstring or short description, judged by tests (Codex abstract opened: 28.8% for Codex, 11.4% for GPT-J, 0% for GPT-3, 70.2% with 100 samples per problem, authors' results). Small, old, publicly available: leak and saturate (LiveCodeBench abstract reports possible overfitting on both, Q21).
- **SWE-bench:** 2,294 real GitHub issues and PRs across 12 Python repos; a patch must make the hidden tests pass (abstract opened; best model at the time resolved 1.96%, long superseded; current numbers not used because I could not verify them).
- **SWE-bench Verified:** a 500-sample subset human-screened for well-specified issues and appropriate tests (OpenAI announcement, seen in a search snippet only; the page returned 403). Reduces unfair tasks but does not make the tests complete.
- **What they miss:** code quality, maintainability, security, multi-file design, reading under-specified requests, and anything outside Python.
- **Weak tests mislead:** a wrong solution that passes the visible tests counts as correct. The toy below passes 10 of 10 candidates under 2-3 example tests but 3 of 10 under broader tests.
- **Saturation:** once top models are near the ceiling, differences are mostly noise or test errors.

**Example (synthetic):** three tasks (prime test, median, de-duplicate) with a correct solution and 2-3 plausible wrong ones each, such as treating 1 as prime, ignoring even-length lists, losing order with `set`. All 10 pass the weak tests; 3 pass the strong ones (the three correct solutions).

**Code:** (executes small source strings with exec; toy problems; strong tests compare with the reference on a battery of inputs)
```python
# Weak vs strong tests on mock "model-written" solutions (source strings). Problems are toy HumanEval-style tasks.
cands = {
 "is_prime": {
   "correct":      "def f(n):\n    return n > 1 and all(n % i for i in range(2, int(n**0.5) + 1))",
   "half-range":   "def f(n):\n    return n > 1 and all(n % i for i in range(2, n // 2))",
   "one-is-prime": "def f(n):\n    return all(n % i for i in range(2, int(n**0.5) + 1))",
   "hardcoded":    "def f(n):\n    return n in (2, 3, 5, 7, 11)"},
 "median": {
   "correct":      "def f(x):\n    s = sorted(x); m = len(s) // 2\n    return s[m] if len(s) % 2 else (s[m-1] + s[m]) / 2",
   "no-even":      "def f(x):\n    return sorted(x)[len(x) // 2]",
   "no-sort":      "def f(x):\n    m = len(x) // 2\n    return x[m] if len(x) % 2 else (x[m-1] + x[m]) / 2"},
 "dedupe": {
   "correct":      "def f(x):\n    out = []\n    [out.append(v) for v in x if v not in out]\n    return out",
   "set-order":    "def f(x):\n    return list(set(x))",
   "adjacent-only":"def f(x):\n    return [v for i, v in enumerate(x) if i == 0 or v != x[i-1]]"},
}
weak = {"is_prime": [(2, True), (7, True), (8, False)],
        "median": [([1, 2, 3], 2), ([1, 5, 9, 10, 11], 9)],
        "dedupe": [([1, 1, 2, 3], [1, 2, 3]), ([4, 4, 5], [4, 5])]}
def load(src):
    ns = {}; exec(src, ns); return ns["f"]
refs = {k: load(v["correct"]) for k, v in cands.items()}
strong_inputs = {"is_prime": list(range(-3, 60)),
                 "median": [[3, 1, 2], [1, 2, 3, 4], [9, 1, 5, 3], [2], [5, 1, 4, 2, 3, 6], [1, 1, 2, 2]],
                 "dedupe": [[1, 2, 1], [3, 1, 3, 2, 1], [], [5], [9, 7, 9, 8, 7], [10, 3, 10]]}
def passes(f, task, strong):
    try:
        if strong: return all(f(x) == refs[task](x) for x in strong_inputs[task])
        return all(f(x) == y for x, y in weak[task])
    except Exception: return False
tw = ts = tot = 0
print(f"{'task':9s}{'candidate':15s}{'weak tests':>11s}{'strong tests':>14s}")
for task, d in cands.items():
    for name, src in d.items():
        f = load(src); w, s = passes(f, task, False), passes(f, task, True)
        tw += w; ts += s; tot += 1
        print(f"{task:9s}{name:15s}{'pass' if w else 'FAIL':>11s}{'pass' if s else 'FAIL':>14s}")
print(f"pass rate: weak tests {tw}/{tot}, strong tests {ts}/{tot}")
```
**Output (my run):**
```
task     candidate       weak tests  strong tests
is_prime correct               pass          pass
is_prime half-range            pass          FAIL
is_prime one-is-prime          pass          FAIL
is_prime hardcoded             pass          FAIL
median   correct               pass          pass
median   no-even               pass          FAIL
median   no-sort               pass          FAIL
dedupe   correct               pass          pass
dedupe   set-order             pass          FAIL
dedupe   adjacent-only         pass          FAIL
pass rate: weak tests 10/10, strong tests 3/10
```
**Follow-ups:**
- *How do I strengthen tests?* More inputs, edge cases, property-based or differential testing against a reference.
- *Pass@k on these?* Q12 and Q13.
- *Agent-style coding evals?* Part 8 Q14.

**Common mistakes:** treating a benchmark pass as correctness; quoting a leaderboard figure without the harness and version; ignoring test quality; assuming "Verified" means flawless.

### Q23 ⭐⭐ 🟡 Perplexity as an evaluation metric: what does it tell you, why does it fail as a measure of an LLM application's quality, and when is it still useful (see Part 2 Q7 for the definition)?
**Asked at:** all types; GenAI-engineer rounds
**Say this first (1 line):** perplexity tells you how well a model predicts held-out text, which is useful for language-model quality and drift, but it says almost nothing about whether an application's answers are correct, helpful or safe.

**Then explain:** (definition and the cross-entropy link are in Part 2 Q7)
- **What it measures:** exp of the average negative log-likelihood per token on a text. Lower means the text was less surprising to the model.
- **Why it fails for apps:** (1) it depends on the tokenizer or unit (the run: same text, same model, per-word 1.30 versus per-char 1.05); (2) it rewards likely text, not true text (a popular myth outscored the correction); (3) instruction-tuned and RLHF models are not trained to maximise it, so it is not comparable with their usefulness; (4) it needs token probabilities, which many APIs do not expose.
- **When still useful:** comparing models with the same tokenizer on the same held-out data; checking a domain adaptation or continued pretraining (cooking text: 1.30 under a cooking model, 34.55 under a legal one); detecting data drift; training-curve monitoring.
- **What to use instead for apps:** task metrics, judges and human review (Q1, Q4).

**Example (toy bigram language model on synthetic text):** a trained word-level bigram model assigns PPL 1.16 to "the wall is visible from space" and 1.58 to "the wall is not visible from space", because the myth appears five times in the training text and the correction once. Lower perplexity, wrong claim.

**Code:** (stdlib; add-k smoothed bigram; all text is synthetic)
```python
# Perplexity on a toy bigram LM: tokenizer dependence, domain sensitivity, and its blind spot for truth.
import math
from collections import Counter

def train_bigram(text, k=0.1):
    w = text.split(); V = len(set(w)) + 1
    big, uni = Counter(zip(w, w[1:])), Counter(w)
    return lambda a, b: (big[(a, b)] + k) / (uni[a] + k * V)

def nll(model, text):                      # total negative log-likelihood in nats
    w = text.split(); return -sum(math.log(model(a, b)) for a, b in zip(w, w[1:]))

cook = "stir the soup and add salt then stir the sauce and add pepper " * 20
legal = "the party shall pay the fee and the court shall hear the claim " * 20
held_cook = "stir the sauce and add salt then stir the soup and add pepper"
m_cook, m_legal = train_bigram(cook), train_bigram(legal)

# 1) same total NLL, different perplexity depending on the unit
total = nll(m_cook, held_cook); n_words = len(held_cook.split()) - 1; n_chars = len(held_cook) - 1
print(f"total NLL {total:.2f} nats | per-word PPL {math.exp(total/n_words):.2f} | per-char PPL {math.exp(total/n_chars):.2f}  (same text, same model)")

# 2) useful: held-out text from the model's own domain scores much lower than from another domain
print(f"cooking text under cooking LM PPL {math.exp(total/n_words):.2f}; under legal LM PPL {math.exp(nll(m_legal, held_cook)/n_words):.2f}")

# 3) blind spot: a popular falsehood in the training data beats the truth
myth = ("the wall is visible from space " * 5 + "the wall is not visible from space " * 1)
m_myth = train_bigram(myth)
for s in ("the wall is visible from space", "the wall is not visible from space"):
    print(f"PPL {math.exp(nll(m_myth, s)/(len(s.split())-1)):.2f}  <- {s!r}")
```
**Output (my run):**
```
total NLL 3.12 nats | per-word PPL 1.30 | per-char PPL 1.05  (same text, same model)
cooking text under cooking LM PPL 1.30; under legal LM PPL 34.55
PPL 1.16  <- 'the wall is visible from space'
PPL 1.58  <- 'the wall is not visible from space'
```
(Per-char uses the number of characters minus one, a rough convention just to show unit dependence.)

**Follow-ups:**
- *Can perplexity detect hallucination?* Weakly at best; see Q9 for sampling-consistency methods.
- *Why can't I compare across tokenizers?* Part 2 Q7; compare bits per byte or character instead.

**Common mistakes:** comparing perplexity across different tokenizers; using it to rank chat models; equating low perplexity with truth; computing it on text the model trained on.

### Q24 ⭐⭐ 🟡 How do you design a human evaluation (rubrics, annotation guidelines, calibration rounds, adjudication, sampling, cost and throughput)?
**Asked at:** product, GenAI startups, GCC, evaluation-focused rounds
**Say this first (1 line):** I write a rubric with examples, pilot it on a small batch, measure agreement, fix the guideline, repeat until agreement is acceptable, then run the real sample with double labelling on part of it and an adjudicator for disagreements.

**Then explain:**
- **Rubric:** one criterion per question, simple scale (binary or 3 points), anchored examples including borderline ones, a clear "cannot tell" option (same reasoning as judge rubrics, Q7).
- **Calibration rounds:** two annotators label the same 50-100 items, compute raw agreement and Cohen's kappa (Q25, Q39), discuss disagreements, update the guideline, repeat. The toy shows agreement 0.73 and kappa 0.45 improving to 0.82 and 0.64 after the guideline fix (simulated annotators, assumed error rates).
- **Adjudication:** a senior reviewer resolves disagreements; record the reason so it becomes a guideline example.
- **Sampling:** sample from real traffic, stratified by the segments you care about (Q34); sample size from the confidence interval you need (95% half-width at p = 0.8: 0.078 at n = 100, 0.055 at 200, 0.039 at 400, closed form).
- **Cost and throughput:** the toy assumes 1.5 min per item per annotator and 3 min per adjudicated item (assumed numbers); 400 double-labelled items with 12% disagreements is then 22.4 person-hours. Use cheaper checks (code, judge) to select what humans see; use humans to validate the judge (Q6).

**Example:** 100 items per calibration round. Round 1 gave 27 items needing adjudication, round 2 gave 18. After adjudicating round 2 the final labels matched the simulated truth on all 100, against 92 for one annotator alone (small simulation; do not over-read the 100%).

**Code:** (simulated annotators; the kappa function is asserted against a hand-worked 2x2 table)
```python
# Human-eval design toy: calibration rounds, Cohen's kappa, adjudication, sample size, throughput. Annotators are SIMULATED.
import numpy as np
rng = np.random.default_rng(21)

def kappa(a, b):
    a, b = np.asarray(a), np.asarray(b); po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in (0, 1))
    return (po - pe) / (1 - pe)

# check against a hand-worked table: 25 yes/25 no for A, 30 yes/20 no for B, 35 agreements -> po 0.7, pe 0.5, kappa 0.4
a = [1]*20 + [1]*5 + [0]*10 + [0]*15; b = [1]*20 + [0]*5 + [1]*10 + [0]*15
assert abs(kappa(a, b) - 0.4) < 1e-12

def annotate(truth, flip, rng):                  # annotator flips the correct label with probability `flip`
    return np.where(rng.random(len(truth)) < flip, 1 - truth, truth)

n = 100
for rnd, flip in [("round 1 (vague guideline)", 0.20), ("round 2 (after guideline fix + examples)", 0.08)]:
    truth = (rng.random(n) < 0.4).astype(int)
    A, B = annotate(truth, flip, rng), annotate(truth, flip, rng)
    print(f"{rnd}: raw agreement {(A == B).mean():.2f}, kappa {kappa(A, B):.2f}, items needing adjudication {(A != B).sum()}")

# adjudication on the final round: a senior reviewer resolves disagreements (assumed 95% accurate)
final = np.where(A == B, A, annotate(truth, 0.05, rng))
print(f"final label accuracy vs truth after adjudication: {(final == truth).mean():.2f}  (single annotator: {(A == truth).mean():.2f})")

# sample size: half-width of a 95% CI on a pass rate of 0.8 (closed form)
for m in (100, 200, 400):
    print(f"n={m}: 95% half-width at p=0.8 = {1.96 * np.sqrt(0.8 * 0.2 / m):.3f}")

# throughput with ASSUMED timings (hours only): 2 annotators x n items x 1.5 min, plus adjudication 3 min per disagreement
items, disagree = 400, 0.12
hours = (2 * items * 1.5 + disagree * items * 3) / 60
print(f"assumed: {items} items, 1.5 min/item/annotator, {disagree:.0%} disagreements at 3 min each -> {hours:.1f} person-hours")
```
**Output (my run):**
```
round 1 (vague guideline): raw agreement 0.73, kappa 0.45, items needing adjudication 27
round 2 (after guideline fix + examples): raw agreement 0.82, kappa 0.64, items needing adjudication 18
final label accuracy vs truth after adjudication: 1.00  (single annotator: 0.92)
n=100: 95% half-width at p=0.8 = 0.078
n=200: 95% half-width at p=0.8 = 0.055
n=400: 95% half-width at p=0.8 = 0.039
assumed: 400 items, 1.5 min/item/annotator, 12% disagreements at 3 min each -> 22.4 person-hours
```
**Follow-ups:**
- *Kappa target?* Guides cite rules of thumb such as 0.6 and 0.8 (one prep guide, opened); treat them as rough and look at prevalence (Q25).
- *Subjective tasks?* Keep disagreement as signal; use several annotators and report the spread.
- *Annotators drift?* Re-check with gold items seeded in the queue.

**Common mistakes:** skipping the pilot; a rubric with several criteria in one question; reporting raw agreement only; no adjudication rule; an unrepresentative sample; forgetting to version the guideline with the labels.

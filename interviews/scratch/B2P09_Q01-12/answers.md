### Q1 ⭐⭐⭐ 🟢 How do you evaluate an LLM application end to end? Explain why it differs from testing ordinary software, model vs system evaluation, and how offline and online evaluation fit together.
**Asked at:** all types; GenAI-engineer and evaluation-focused rounds; interview-prep guides list this as an opening question (guides, not candidate reports)
**Say this first (1 line):** You evaluate the whole system (retrieval, prompt, model, tools, post-processing) on a versioned test set before release, then keep measuring on sampled production traffic after release, and you do not rely on a single model score.

**Then explain:**
- **Why it differs from ordinary software tests:** outputs are open-ended and non-deterministic, there is rarely one correct string, so a unit-test `assert ==` does not work. You score with a mix of exact checks, rubric-based judges and humans, and you report a rate with an interval, not pass or fail.
- **Model vs system evaluation:** model eval asks "is this model good at the task?" (public benchmarks, or your own prompts with gold context). System eval asks "does the product work for users?" and includes the retriever, prompts, tools, guardrails and parsing. The example below shows the gap: the same generator scores 20/20 with gold context and 12/20 inside the system.
- **Build in layers, cheapest first:** deterministic checks (format, schema, exact answers, forbidden strings), then LLM judges for subjective criteria, then humans for calibration and edge cases (judge calibration is Q6, human design Q24).
- **Offline vs online:** offline (a frozen test set, run on every change) is repeatable and cheap, so it gates releases. Online (A/B tests, implicit feedback, sampled production traces scored by a judge) shows what real users do, including queries your set never sampled. Failures found online become new offline cases (Q30, Q15). OpenAI's evaluation guidance describes the same loop: continuous evaluation grown from logs (vendor docs, opened).
- **Start from error analysis, not from metrics:** read real traces, name the failure modes, then build evals for the ones that matter (Hamel Husain's FAQ, a practitioner view; see Q15).
- **Scope pointers:** retrieval vs generation metrics are in Part 6 Q10 and Q39, agent evaluation in Part 8 Q14, evaluating a fine-tuned model in Part 4 Q9, monitoring depth in Part 11.

**Example:** Toy support bot, 20 cases (synthetic). With the gold document handed to the generator it answers 20/20, so a model-only eval says "ship". Run end to end with a retriever that finds the right document 70% of the time (assumed), it scores 12/20 in this run. On simulated traffic where 30% of queries are typos (assumed retrieval hit rate 0.4 on those), the pass rate is 0.62. The model was never the problem; the system eval and the online slice found it.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# MOCK: model-level vs system-level evaluation on toy, synthetic data. No real LLM is used.
import random
random.seed(1)

# 20 synthetic test cases: each has a gold answer and the doc that contains it.
CASES = [{"id": i, "q": f"q{i}", "gold": f"ans{i}", "doc": f"doc{i}"} for i in range(20)]
CORPUS = {c["doc"]: f"The answer is {c['gold']}." for c in CASES}

def mock_retriever(q, retr_hit_rate=0.7):
    """Assumed: finds the right doc 70% of the time, otherwise a wrong doc."""
    i = int(q[1:])
    if random.random() < retr_hit_rate:
        return f"doc{i}"
    return f"doc{(i + 1) % 20}"

def mock_generator(q, context):
    """Assumed: a strong model that copies the answer from the context if present."""
    return context.split()[-1].rstrip(".")

def graded(case, out):               # deterministic grader first (cheap, exact)
    return out == case["gold"]

# MODEL eval: hand the model the gold doc. Measures generation only.
model_pass = sum(graded(c, mock_generator(c["q"], CORPUS[c["doc"]])) for c in CASES)
# SYSTEM eval: retriever + generator, as users experience it.
sys_pass = 0
for c in CASES:
    d = mock_retriever(c["q"])
    sys_pass += graded(c, mock_generator(c["q"], CORPUS[d]))
print("model eval (gold context):", model_pass, "/", len(CASES))
print("system eval (real retriever):", sys_pass, "/", len(CASES))

# Offline vs online: offline set is clean queries; online traffic has a 'typo' slice
# the offline set never sampled (assumed 30% of traffic, retrieval hit rate 0.4 there).
def online_pass(n=1000):
    ok = 0
    for _ in range(n):
        typo = random.random() < 0.3
        c = random.choice(CASES)
        d = mock_retriever(c["q"], 0.4 if typo else 0.7)
        ok += graded(c, mock_generator(c["q"], CORPUS[d]))
    return ok / n
print("online-style pass rate (assumed 30% typo traffic):", online_pass())
```
**Output (my run):**
```
model eval (gold context): 20 / 20
system eval (real retriever): 12 / 20
online-style pass rate (assumed 30% typo traffic): 0.624
```

**Follow-ups:**
- *Which do you build first?* A small set (20-50 cases from real failures is a common start, per Anthropic's agent-evals post, a vendor view) with deterministic checks; add judges only for criteria you cannot check in code.
- *What do you gate releases on?* Offline suite results with intervals (Q11, Q14); online metrics decide rollout and rollback (Q30).
- *Where does a public benchmark fit?* Only for picking candidate models; it is not a product eval (Q10).

**Common mistakes:** evaluating only the model with gold context; one aggregate number with no interval; building a set from imagined queries instead of logs; relying on an LLM judge nobody checked against human labels; no path for production failures to become test cases.

### Q2 ⭐⭐⭐ 🟡 How do you build a golden evaluation set from scratch (real queries, coverage of cases, labels, size, versioning, and keeping it free of training or prompt leakage)?
**Asked at:** all types; product, GenAI startups, GCC; a Dataford prompt framed at Invoca (seen in search only) asks for a golden-dataset evaluation system (not verified as a candidate report)
**Say this first (1 line):** Sample real queries, cover the cases that matter on purpose, label them with clear rules, deduplicate, split once into dev and test, version the set by content, and check it never appears in your prompts, few-shot examples or training data.

**Then explain:**
- **Source:** start from real user queries or logs (anonymised). Add synthetic cases only to fill gaps, and say so; synthetic questions tend to be easier and more uniform than real ones (the RAG-specific pitfalls are in Part 6 Q40).
- **Coverage, not just volume:** stratify by intent, difficulty, language, user segment and known failure modes; include edge cases, unanswerable questions and adversarial ones. Look for thin strata before labelling.
- **Labels:** write short guidelines, have two people label a sample, resolve disagreements, and keep the rationale. The label type should match what you will compute (a gold answer, a rubric verdict, relevant document ids).
- **Size:** it depends on the effect you must detect, not on a magic number. Guides cite 100-500 for golden sets (interview-prep guides, not a standard) and Anthropic suggests 20-50 real-failure tasks to start (vendor view). Few hundred cases give wide intervals on small gains (Q11, Q26).
- **Versioning:** hash the content, record the source and date, never edit a case silently; a changed set means a new version and old scores are not comparable.
- **Leakage:** keep the test split out of prompts, few-shot examples, fine-tuning data and judge calibration data. Check with n-gram or word-overlap searches and by keeping a never-looked-at final test split. Training-data decontamination is Part 2 Q30 and fine-tuning data is Part 4 Q34.

**Example:** Synthetic log sample of 16 queries across four intents. Word-overlap deduplication (Jaccard >= 0.7) removed 1 exact rephrasing ("how do I reset my password?") but kept "reset password please", so cheap dedupe is imperfect and you still skim. Hash-based split gave 6 dev and 9 test. A planted check found that both few-shot examples in the prompt were also in the set, so those cases would flatter the score. Adding one case changed the version id from 7fb70dfa to e671e548.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# Toy golden-set builder: dedupe, stratify, split, leakage check, version hash. Synthetic data.
import hashlib, json, random, re
random.seed(7)

raw = [  # (query, intent) -- synthetic "production" sample
    ("how do i reset my password", "account"), ("how do I reset my password?", "account"),
    ("reset password please", "account"), ("cancel my subscription", "billing"),
    ("i want a refund for last month", "billing"), ("why was i charged twice", "billing"),
    ("refund for double charge", "billing"), ("app crashes on startup", "bug"),
    ("crash when opening settings", "bug"), ("export data to csv", "howto"),
    ("how to export my data as csv", "howto"), ("change email address", "account"),
    ("invoice for march", "billing"), ("dark mode not saving", "bug"),
    ("delete my account", "account"), ("is there an api", "howto"),
]

def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
def toks(s): return set(norm(s).split())
def jaccard(a, b): return len(a & b) / len(a | b)

# 1) near-duplicate removal (Jaccard >= 0.7 on word sets)
kept = []
for q, it in raw:
    if all(jaccard(toks(q), toks(k)) < 0.7 for k, _ in kept):
        kept.append((q, it))
print("raw:", len(raw), "after dedupe:", len(kept))

# 2) stratified view: how many per intent (spot thin strata before labelling)
from collections import Counter
print("per intent:", dict(Counter(it for _, it in kept)))

# 3) split once, deterministically, by hash of the normalised text (stable across reruns)
def bucket(q): return int(hashlib.sha256(norm(q).encode()).hexdigest(), 16) % 100
dev = [x for x in kept if bucket(x[0]) < 40]
test = [x for x in kept if bucket(x[0]) >= 40]
print("dev:", len(dev), "test:", len(test))

# 4) leakage check: golden/test queries vs few-shot examples in the prompt
few_shot = ["how to export my data as csv", "crash when opening settings"]
leaks = [q for q, _ in test + dev for f in few_shot if jaccard(toks(q), toks(f)) >= 0.7]
print("leaked into prompt examples:", sorted(set(leaks)))

# 5) version id = hash of content; changes whenever any case or label changes
def version(rows): return hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()[:8]
v1 = version(kept)
kept2 = kept + [("how do i enable 2fa", "account")]
print("version v1:", v1, "| after adding one case:", version(kept2))
```
**Output (my run):**
```
raw: 16 after dedupe: 15
per intent: {'account': 4, 'billing': 5, 'bug': 3, 'howto': 3}
dev: 6 test: 9
leaked into prompt examples: ['crash when opening settings', 'how to export my data as csv']
version v1: 7fb70dfa | after adding one case: e671e548
```

**Follow-ups:**
- *Dev vs test?* Tune prompts on dev; touch test only for the final comparison, otherwise you overfit the set.
- *Can an LLM write the questions?* Yes as a starting point, but check them by hand and keep real queries in the mix; model-written evals need human verification (Anthropic, vendor post).
- *How do you keep it fresh?* Add new failure cases from production on a schedule, as a new version, and keep a frozen regression slice (Q36).

**Common mistakes:** using the same examples in the prompt and in the test; building only from easy happy-path queries; no unanswerable or edge cases; editing cases without versioning; labelling with no guideline so labels are noisy.

### Q3 ⭐⭐⭐ 🟢 Reference-based metrics for generated text: what do exact match, token F1, BLEU, ROUGE and BERTScore measure, when does each fit, and why do they fail for open-ended LLM output?
**Asked at:** all types; interview-prep guides list BLEU/ROUGE limits as a junior-level check (guides, not candidate reports)
**Say this first (1 line):** These metrics compare the model's text to a reference by overlap of words (exact match, F1, BLEU, ROUGE) or by embedding similarity (BERTScore); they work when answers are short and constrained, and they fail for open-ended output because many different texts are equally correct.

**Then explain:**
- **Exact match:** 1 if the normalised answer equals the reference. Good for short factual or classification answers; brittle to phrasing.
- **Token F1:** harmonic mean of word precision and recall against the reference (the SQuAD-style metric). Gives partial credit; still blind to meaning.
- **BLEU:** precision of n-grams with a brevity penalty, designed for machine translation. **ROUGE:** recall-oriented overlap (ROUGE-L uses the longest common subsequence), common for summaries.
- **BERTScore:** matches tokens by contextual-embedding similarity instead of exact words, so synonyms count; the authors tested it on 363 machine-translation and captioning systems (arXiv 1904.09675, abstract). It is still similarity to one reference, not truth.
- **Why they fail for LLM output:** one question has many valid phrasings, so a correct paraphrase scores low; and a wrong answer that copies most of the reference words scores high. Even in code, the Codex authors report that functionally inequivalent programs often had higher BLEU than equivalent ones (Codex paper body, read for this answer).
- **When they still fit:** extractive QA, classification labels, translation-style tasks with several references, or as a cheap regression signal. For open-ended tasks use rubric judges or humans (Q4, Q24).

**Example:** Reference: "Maria bought a car in 2019." A correct paraphrase ("In 2019 Maria purchased an automobile.") gets F1 0.50 and BLEU-2 0.32, while a wrong answer that changes only the year ("... in 2021") gets F1 0.83 and BLEU-2 0.82. The metric ranks the wrong answer above the right one. The toy soft match (a small synonym table standing in for embeddings, not a real BERTScore) lifts the paraphrase to 0.67 but also gives the wrong year 0.83, because the embedding view still hardly sees the changed fact.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# Reference-based metrics from scratch on toy strings. The "embedding" is a TOY synonym table
# (not a real model) that stands in for BERTScore-style soft matching.
import math
from collections import Counter

def toks(s): return s.lower().replace(".", "").replace(",", "").split()
def exact(p, r): return float(toks(p) == toks(r))
def f1(p, r):
    p, r = toks(p), toks(r); c = sum((Counter(p) & Counter(r)).values())
    if c == 0: return 0.0
    pr, rc = c / len(p), c / len(r); return 2 * pr * rc / (pr + rc)

def ngrams(t, n): return Counter(tuple(t[i:i+n]) for i in range(len(t) - n + 1))
def bleu2(p, r):                       # BLEU with n=1,2, uniform weights, brevity penalty, no smoothing
    p, r = toks(p), toks(r); logs = []
    for n in (1, 2):
        pg, rg = ngrams(p, n), ngrams(r, n)
        clip = sum((pg & rg).values()); tot = max(sum(pg.values()), 1)
        if clip == 0: return 0.0
        logs.append(math.log(clip / tot))
    bp = 1.0 if len(p) > len(r) else math.exp(1 - len(r) / max(len(p), 1))
    return bp * math.exp(sum(logs) / 2)

def lcs(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a)):
        for j in range(len(b)):
            d[i+1][j+1] = d[i][j] + 1 if a[i] == b[j] else max(d[i][j+1], d[i+1][j])
    return d[-1][-1]
def rougeL(p, r):
    p, r = toks(p), toks(r); l = lcs(p, r)
    if l == 0: return 0.0
    pr, rc = l / len(p), l / len(r); return 2 * pr * rc / (pr + rc)

SYN = {"purchase": "buy", "bought": "buy", "car": "auto", "automobile": "auto", "vehicle": "auto"}
def soft_f1(p, r):                    # toy BERTScore-like: greedy match, sim 1 for same/synonym, else 0
    canon = lambda w: SYN.get(w, w)
    p, r = [canon(w) for w in toks(p)], [canon(w) for w in toks(r)]
    prec = sum(w in r for w in p) / len(p); rec = sum(w in p for w in r) / len(r)
    return 0.0 if prec * rec == 0 else 2 * prec * rec / (prec + rec)

ref = "Maria bought a car in 2019."
cands = {
    "paraphrase (correct)":      "In 2019 Maria purchased an automobile.",
    "wrong year (incorrect)":    "Maria bought a car in 2021.",
    "exact copy":                "Maria bought a car in 2019.",
    "unrelated":                 "The weather was nice.",
}
print(f"{'candidate':26s} EM    F1    BLEU2 ROUGE-L softF1")
for name, c in cands.items():
    print(f"{name:26s} {exact(c,ref):.2f}  {f1(c,ref):.2f}  {bleu2(c,ref):.2f}  {rougeL(c,ref):.2f}   {soft_f1(c,ref):.2f}")
```
**Output (my run):**
```
candidate                  EM    F1    BLEU2 ROUGE-L softF1
paraphrase (correct)       0.00  0.50  0.32  0.33   0.67
wrong year (incorrect)     0.00  0.83  0.82  0.83   0.83
exact copy                 1.00  1.00  1.00  1.00   1.00
unrelated                  0.00  0.00  0.00  0.00   0.00
```

**Follow-ups:**
- *Is ROUGE useless?* No: it is a cheap proxy where outputs are constrained, but validate it against human ratings for your task before trusting it.
- *What do you use instead?* Deterministic checks where possible, otherwise a calibrated judge (Q4, Q6) plus human spot checks.
- *Why does BERTScore help only partly?* It forgives wording but not a changed number or entity; it measures closeness, not correctness.

**Common mistakes:** reporting BLEU for chatbots as quality; forgetting to normalise case, punctuation and articles before exact match; treating higher overlap as higher correctness; using one reference for tasks with many valid answers; comparing scores across different tokenisation or metric implementations.

### Q4 ⭐⭐⭐ 🟡 What is LLM-as-a-judge? Explain pointwise, pairwise and reference-based judging, when to use each, and the limits of trusting a judge.
**Asked at:** all types; product, GenAI startups, GCC, evaluation-focused rounds
**Say this first (1 line):** LLM-as-a-judge means using a strong model with a rubric to grade another model's output; pointwise scores one answer, pairwise picks the better of two, reference-based checks an answer against a gold answer, and you can trust any of them only after checking it against human labels.

**Then explain:**
- **Pointwise:** judge scores one answer against a rubric (pass/fail or a small scale). Cheap, scales to production traces, no baseline needed; scores drift and cluster, and small differences vanish into ties.
- **Pairwise:** judge sees two answers and picks one (or ties). Better at ranking close candidates and A/B decisions; costs more per comparison, has position bias, and gives no absolute quality.
- **Reference-based:** judge compares the answer with a gold answer or gold facts. Strong when a correct reference exists; wrong or incomplete references punish correct answers.
- **When to use which:** pointwise or binary for production monitoring and gates, pairwise for choosing between two prompts or models, reference-based when you have gold answers. Details of pairwise design are in Q18.
- **What the research reports:** the MT-Bench paper (authors' setup: 80 multi-turn questions in 8 categories, 58 expert labellers) reports GPT-4 agreeing with human experts at 85% on non-tie votes versus 81% human-human agreement; the abstract summarises it as over 80% agreement. That is a result on their questions and setup, not a guarantee for yours.
- **Limits:** judges have biases (Q5), mistakes on math or facts they cannot check, and prompt sensitivity. Calibrate against humans (Q6) and keep humans on the hard cases. Prompt-level limits are in Part 3 Q32 and win rates for aligned models in Part 5 Q10.

**Example:** Synthetic simulation, 20,000 pairs per row, judge noise of 0.9 on a 1-5 quality scale (assumed). When answer B is truly 1.0 better than A, the pairwise judge picks B 78% of the time, pointwise picks B 64% and ties 23%. At a 0.3 gap the numbers are 59% vs 43% with 31% ties. The toy gap comes from rounding to integers and ties, so treat it as mechanics, not a measured judge. Reference-based: with the right reference the correct answer "Canberra" is judged right; with a wrong reference ("Sydney") it is judged wrong.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# MOCK judges on SYNTHETIC answer qualities. Noise levels are ASSUMED, so the comparison
# shows the mechanics, not a measured property of any real judge.
import random
random.seed(3)
N = 20000
def pointwise(q):                      # 1-5 score = round(quality + noise), clipped
    return max(1, min(5, round(q + random.gauss(0, 0.9))))
def pairwise(qa, qb):                  # picks the answer whose noisy impression is higher
    return "A" if qa + random.gauss(0, 0.9) > qb + random.gauss(0, 0.9) else "B"

# true qualities on a 1-5 scale; B is better than A by `gap`
for gap in (0.3, 1.0):
    ok_pw = tie_pw = ok_pair = 0
    for _ in range(N):
        qa = random.uniform(1.5, 3.5); qb = qa + gap
        sa, sb = pointwise(qa), pointwise(qb)
        if sa == sb: tie_pw += 1
        elif sb > sa: ok_pw += 1
        ok_pair += pairwise(qa, qb) == "B"
    print(f"gap {gap}: pointwise picks better {ok_pw/N:.2f}, ties {tie_pw/N:.2f} | pairwise picks better {ok_pair/N:.2f}")

# Reference-based: the judge checks the answer against a reference. If the reference is wrong,
# a correct answer is marked wrong. (Deterministic toy: judge = does the answer match the reference?)
facts = {"capital of Australia": "Canberra"}
def ref_judge(answer, reference): return answer == reference
print("good reference, correct answer judged right:", ref_judge("Canberra", facts["capital of Australia"]))
bad_ref = "Sydney"
print("bad reference,  correct answer judged right:", ref_judge("Canberra", bad_ref))
```
**Output (my run):**
```
gap 0.3: pointwise picks better 0.43, ties 0.31 | pairwise picks better 0.59
gap 1.0: pointwise picks better 0.64, ties 0.23 | pairwise picks better 0.78
good reference, correct answer judged right: True
bad reference,  correct answer judged right: False
```

**Follow-ups:**
- *Which judge model?* The strongest affordable one from a different family than the generator (Q5), and keep it fixed and versioned.
- *Can the judge replace humans?* It can replace most routine grading once its TPR and TNR on a labelled set are acceptable; keep a human sample for drift.
- *Binary or 1-5?* Binary or a small scale is easier to calibrate (Q7).

**Common mistakes:** trusting a judge because it agrees with itself; using one pointwise 1-5 score for everything; never swapping order in pairwise; quoting the paper's 80% agreement as if it applied to your domain; changing the judge model mid-experiment and comparing the scores.

### Q5 ⭐⭐⭐ 🟡 What biases do LLM judges show (position, verbosity, self-preference), how do you measure each in your own setup, and how do you mitigate them?
**Asked at:** all types; product, GenAI startups, evaluation-focused rounds
**Say this first (1 line):** Judges favour the first slot (position bias), longer answers (verbosity bias) and text from their own model (self-preference); you measure each with a probe where the thing that should not matter is varied on equal-quality pairs, and mitigate by swapping order, controlling length, using a different judge family and calibrating against humans.

**Then explain:**
- **Position bias:** the verdict changes when you swap the slots. The MT-Bench paper (Table 2, authors' setup) reports GPT-4 giving a consistent verdict after swapping in 65.0% of cases with the default prompt, with 30.0% biased toward the first slot; Claude-v1 was 23.8% consistent with 75.0% first-biased and GPT-3.5 46.2% consistent. Probe: judge every pair in both orders and count flips.
- **Verbosity bias:** longer answers win at equal quality. The same paper's "repetitive list" attack (padding an answer with rephrased list items, no new information) fooled the weaker judges; GPT-4 resisted much better. Probe: pad an answer with fluff and see if it wins; length-controlled scoring is one fix (length-controlled AlpacaEval reports Spearman with Arena rising from 0.94 to 0.98, authors' claim).
- **Self-preference:** a judge favours its own generations. The MT-Bench paper saw GPT-4 give itself a 10% higher win rate and Claude-v1 25%, but said the data could not settle whether this is self-enhancement; a later paper (arXiv 2404.13076, abstract) reports that models recognise their own outputs and that recognition correlates with preference. Probe: compare judges from different families on the same pairs.
- **Mitigations:** judge both orders and keep the verdict only if it agrees (otherwise a tie); control or penalise length; use a judge from another family or a panel of smaller judges from disjoint families (PoLL, authors' claim of less bias and lower cost); anchor with calibration against human labels (Q6).

**Example:** Mock judge with planted biases (assumed: +0.25 first slot, +0.30 per 100 extra words, +0.40 for its own output) on equal-quality pairs, 20,000 each. The probes recover them: first slot wins 64% (50% would be unbiased), the padded answer wins 72%, the judge's own output wins 71%. Swap-and-agree removes the position effect (X wins 23%, Y 23%, tie 54%) but note it would not remove verbosity or self-preference, which hit both orders alike.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# Measure three judge biases in a MOCK judge with PLANTED (assumed) bias parameters,
# then check that the probes recover them and that swap-and-agree removes position bias.
import random
random.seed(11)
POS_BONUS, LEN_BONUS_PER_100, SELF_BONUS = 0.25, 0.30, 0.40   # planted, ASSUMED

def judge(a, b, judge_model="J"):
    """a, b = dict(q=quality, words=int, gen=model name). Returns 'first' or 'second'."""
    def score(x, first):
        s = x["q"] + random.gauss(0, 0.5)
        s += LEN_BONUS_PER_100 * x["words"] / 100
        s += SELF_BONUS * (x["gen"] == judge_model)
        return s + (POS_BONUS if first else 0)
    return "first" if score(a, True) > score(b, False) else "second"

N = 20000
def pair(): q = random.uniform(2, 4); return q, q      # equal quality pairs: any preference is bias

# 1) position probe: same two answers, both orders. Equal quality, equal length.
first = sum(judge({"q": q, "words": 100, "gen": "X"}, {"q": q, "words": 100, "gen": "Y"}) == "first"
            for q, _ in (pair() for _ in range(N)))
print(f"position: picks first slot {first/N:.2f} (0.50 = no bias)")

# 2) verbosity probe: equal quality, one answer padded (+150 words); randomise slots
pad_wins = 0
for _ in range(N):
    q, _ = pair(); long_first = random.random() < 0.5
    L, S = {"q": q, "words": 250, "gen": "X"}, {"q": q, "words": 100, "gen": "Y"}
    r = judge(L, S) if long_first else judge(S, L)
    pad_wins += (r == "first") == long_first
print(f"verbosity: padded answer wins {pad_wins/N:.2f}")

# 3) self-preference probe: equal quality, judge J's own output vs another model's; randomise slots
self_wins = 0
for _ in range(N):
    q, _ = pair(); own_first = random.random() < 0.5
    O, T = {"q": q, "words": 100, "gen": "J"}, {"q": q, "words": 100, "gen": "Y"}
    r = judge(O, T) if own_first else judge(T, O)
    self_wins += (r == "first") == own_first
print(f"self-preference: own output wins {self_wins/N:.2f}")

# mitigation: judge both orders, keep the verdict only if it agrees; else call it a tie
def swap_judge(x, y):
    r1 = judge(x, y); r2 = judge(y, x)
    if r1 == "first" and r2 == "second": return "x"
    if r1 == "second" and r2 == "first": return "y"
    return "tie"
res = {"x": 0, "y": 0, "tie": 0}
for _ in range(N):
    q, _ = pair(); res[swap_judge({"q": q, "words": 100, "gen": "X"}, {"q": q, "words": 100, "gen": "Y"})] += 1
print("swap-and-agree on equal pairs:", {k: round(v / N, 2) for k, v in res.items()})
```
**Output (my run):**
```
position: picks first slot 0.64 (0.50 = no bias)
verbosity: padded answer wins 0.72
self-preference: own output wins 0.71
swap-and-agree on equal pairs: {'x': 0.23, 'y': 0.23, 'tie': 0.54}
```

**Follow-ups:**
- *Does swapping fix everything?* No, only position; length and self-preference need separate controls.
- *How often should you re-measure?* When you change the judge model, the prompt or the answer-length profile of your system.
- *Is a bigger judge less biased?* In the paper's table GPT-4 was more consistent than the others, but it still showed bias; measure yours.

**Common mistakes:** running one order only; reporting win rate without ties; letting the same model generate and judge; assuming bias numbers from a paper transfer to your prompts; padding-friendly rubrics that reward 'thoroughness'.

### Q6 ⭐⭐⭐ 🟡 How do you calibrate and validate an LLM judge against human labels (agreement, Cohen's kappa, true positive and true negative rate, train/dev/test split of labelled examples)?
**Asked at:** product, GenAI startups, GCC, evaluation-focused rounds
**Say this first (1 line):** Label a sample by hand, run the judge on the same cases, and report agreement, Cohen's kappa, and TPR and TNR on a held-out split, so you know how often it catches passes and failures, before you trust its numbers.

**Then explain:**
- **Split the labelled data:** one small part to pick few-shot examples and write the prompt (train), one to iterate on (dev), one untouched to report (test). Hamel Husain suggests roughly 10-20% / 40-45% / 40-45% and 100-200 labelled examples per failure mode (his practitioner guidance, not a standard).
- **Agreement alone misleads:** with 85% passes, a judge that always says pass agrees 85% of the time. Kappa corrects for chance: kappa = (po - pe) / (1 - pe). Two-annotator kappa details and the kappa paradox are Q25; code is Q39.
- **TPR and TNR:** TPR = share of human PASS the judge calls PASS; TNR = share of human FAIL the judge calls FAIL. For failure detection TNR is usually the number that matters, and it rests on the few failing cases, so it is noisy.
- **Use the rates to correct a metric:** with TPR and TNR you can estimate the true pass rate from the judge's observed rate: (observed + TNR - 1) / (TPR + TNR - 1). It only helps if the rates are measured well.
- **Iterate:** read the disagreements, fix the rubric or add anchored examples, re-measure on dev, and report once on test. Re-check when the model, prompt or traffic changes (Q45).

**Example:** Synthetic data, 400 cases, 85% human-PASS, mock judge with assumed TPR 0.9 and TNR 0.7. On the test split (170 cases): agreement 0.86, kappa 0.49, TPR 0.90, TNR 0.65. An always-PASS judge gets the same 0.86 agreement but kappa 0.00. Honest weak result: correcting the judge's pass rate with dev-set TPR and TNR gave 0.926 against a human 0.865 (raw judge 0.824), because dev TNR (0.80) came from only 20 failing cases and test TNR was 0.65. The correction made it worse here; with few negatives, label more of them.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# Validate a MOCK judge against SYNTHETIC human labels: agreement, kappa, TPR, TNR,
# dev/test split, and a kappa check against an independent pair-counting computation.
import random, itertools
random.seed(5)

def make(n, p_pass=0.85, tpr=0.9, tnr=0.7):   # ASSUMED prevalence and judge error rates
    rows = []
    for _ in range(n):
        h = random.random() < p_pass
        j = (random.random() < tpr) if h else (random.random() > tnr)
        rows.append((h, j))
    return rows
data = make(400)
random.shuffle(data)
train, dev, test = data[:60], data[60:230], data[230:]     # 15% / 42.5% / 42.5%
print("split sizes:", len(train), len(dev), len(test), "(train = few-shot/prompt examples)")

def stats(rows):
    tp = sum(h and j for h, j in rows); tn = sum((not h) and (not j) for h, j in rows)
    fp = sum((not h) and j for h, j in rows); fn = sum(h and (not j) for h, j in rows)
    n = len(rows); po = (tp + tn) / n
    pe = ((tp + fn) * (tp + fp) + (fp + tn) * (fn + tn)) / n**2
    return dict(n=n, agree=po, kappa=(po - pe) / (1 - pe), tpr=tp / (tp + fn), tnr=tn / (tn + fp))

def kappa_pairs(rows):                 # independent check: chance agreement by explicit enumeration
    H = [h for h, _ in rows]; J = [j for _, j in rows]; n = len(rows)
    po = sum(h == j for h, j in rows) / n
    pe = sum(a == b for a, b in itertools.product(H, J)) / n**2   # P(random human label == random judge label)
    return (po - pe) / (1 - pe)

for name, rows in (("dev", dev), ("test", test)):
    s = stats(rows)
    print(f"{name}: n={s['n']} agree={s['agree']:.2f} kappa={s['kappa']:.2f} TPR={s['tpr']:.2f} TNR={s['tnr']:.2f}")
assert abs(stats(test)["kappa"] - kappa_pairs(test)) < 1e-12
print("kappa matches independent computation: OK")

# Raw agreement hides the weak class: a judge that always says PASS on this data
always = [(h, True) for h, _ in test]
s = stats(always); print(f"always-PASS judge on test: agree={s['agree']:.2f} kappa={s['kappa']:.2f} TNR={s['tnr']:.2f}")

# Correct the judge's observed pass rate with TPR/TNR from DEV, evaluate on TEST (Rogan-Gladen)
d = stats(dev); print("human-negative cases in dev:", sum(not h for h, _ in dev), "| in test:", sum(not h for h, _ in test))
obs = sum(j for _, j in test) / len(test); true = sum(h for h, _ in test) / len(test)
corr = (obs + d["tnr"] - 1) / (d["tpr"] + d["tnr"] - 1)
print(f"test pass rate: human {true:.3f}, judge raw {obs:.3f}, judge corrected {corr:.3f}")
```
**Output (my run):**
```
split sizes: 60 170 170 (train = few-shot/prompt examples)
dev: n=170 agree=0.86 kappa=0.51 TPR=0.87 TNR=0.80
test: n=170 agree=0.86 kappa=0.49 TPR=0.90 TNR=0.65
kappa matches independent computation: OK
always-PASS judge on test: agree=0.86 kappa=0.00 TNR=0.00
human-negative cases in dev: 20 | in test: 23
test pass rate: human 0.865, judge raw 0.824, judge corrected 0.926
```

**Follow-ups:**
- *What kappa is acceptable?* Rules of thumb exist (an interview guide cites 0.6 and 0.8 thresholds) but depend on the task; judge by TPR/TNR and by what a wrong verdict costs.
- *Why not use the dev set to report?* You tuned on it, so the number is optimistic.
- *How do you get more failing cases cheaply?* Oversample suspected failures when labelling, then reweight when you estimate prevalence.

**Common mistakes:** reporting only raw agreement; one split for everything; tuning the prompt on the test set; ignoring class imbalance; computing TPR/TNR from a handful of negatives and treating them as exact.

### Q7 ⭐⭐⭐ 🟡 How do you write a judge prompt and rubric that works (one criterion per judge, binary or small scales, anchored examples, reasoning before the verdict, output format)?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** Judge one criterion at a time, use binary or a small scale with written definitions, give anchored pass and fail examples, ask for reasoning before the verdict, and demand a fixed machine-readable output that you parse strictly.

**Then explain:**
- **One criterion per judge:** a single 'overall quality 1-5' judge cannot be debugged. Separate judges for faithfulness, relevance, tone, and so on tell you what failed (Hamel Husain recommends one focused judge per failure mode and binary pass/fail over 1-5 scales; practitioner guidance).
- **Binary or small scale:** define PASS and FAIL in plain words, including what to ignore. Wider scales cluster in the middle and are harder to calibrate (Q4, Q6).
- **Anchored examples:** two or three labelled examples (clear pass, clear fail, one borderline) fix the standard better than adjectives. Keep them out of your test set (Q2).
- **Reasoning before verdict:** ask for a short rationale first and the verdict last, which is also the approach in G-Eval (chain-of-thought plus form filling, authors' method) and in OpenAI's guidance to reason before scoring (vendor docs). The rationale also helps you debug disagreements.
- **Output format:** JSON with fixed keys in a fixed order, and a strict parser that rejects anything else and counts the rejections; retry once, then log as an error, never default to PASS.
- **Validate:** check the finished prompt against human labels (Q6). Prompt-level evaluation basics are in Part 3 Q32.

**Example:** A faithfulness judge with a two-example rubric. The strict parser accepted a clean reply and a reply with prose around the JSON, and rejected three bad ones: verdict before reasoning, a drifted scale ("4/5"), and truncated JSON. The three-judge report (faithfulness PASS, relevance PASS, tone FAIL) points straight to the tone problem, which a single 1-5 score would hide. The mock judge here is canned text; it tests the format handling, not judging skill.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# Judge prompt builder + strict output parser, exercised with a MOCK judge that returns canned text.
import json, re

RUBRIC = """You are grading ONE criterion: FAITHFULNESS.
PASS only if every factual claim in the ANSWER is supported by the CONTEXT.
FAIL if any claim is unsupported or contradicted. Ignore style, length and helpfulness.
Examples:
CONTEXT: The fee is $5. ANSWER: The fee is $5. -> {"reasoning": "fee matches", "verdict": "PASS"}
CONTEXT: The fee is $5. ANSWER: The fee is $7. -> {"reasoning": "fee differs", "verdict": "FAIL"}
Think first, then decide. Reply with JSON only, keys in this order: reasoning, verdict (PASS or FAIL)."""

def build_prompt(context, answer):
    return f"{RUBRIC}\n\nCONTEXT: {context}\nANSWER: {answer}\n"

def parse(text):
    """Strict: valid JSON, keys in order reasoning->verdict, verdict in {PASS, FAIL}. Else None."""
    try:
        obj = json.loads(text)
    except ValueError:
        m = re.search(r"\{.*\}", text, re.S)           # tolerate prose around the JSON, nothing more
        if not m: return None
        try: obj = json.loads(m.group(0))
        except ValueError: return None
    if list(obj.keys()) != ["reasoning", "verdict"]: return None
    return obj["verdict"] if obj["verdict"] in ("PASS", "FAIL") else None

outputs = {                               # canned judge replies (what a model might return)
    "clean":              '{"reasoning": "fee matches", "verdict": "PASS"}',
    "prose around json":  'Sure! {"reasoning": "fee differs", "verdict": "FAIL"} Hope that helps.',
    "verdict first":      '{"verdict": "PASS", "reasoning": "looks fine"}',
    "scale drift":        '{"reasoning": "mostly ok", "verdict": "4/5"}',
    "broken json":        '{"reasoning": "fee differs", "verdict": FAIL',
}
for k, v in outputs.items():
    print(f"{k:18s} -> {parse(v)}")
print("prompt length (chars):", len(build_prompt("The fee is $5.", "The fee is $5.")))

# One criterion per judge: three binary judges beat one 1-5 'overall' for debugging
verdicts = {"faithfulness": "PASS", "relevance": "PASS", "tone": "FAIL"}
print("per-criterion report:", verdicts, "-> failing:", [k for k, v in verdicts.items() if v == "FAIL"])
```
**Output (my run):**
```
clean              -> PASS
prose around json  -> FAIL
verdict first      -> None
scale drift        -> None
broken json        -> None
prompt length (chars): 566
per-criterion report: {'faithfulness': 'PASS', 'relevance': 'PASS', 'tone': 'FAIL'} -> failing: ['tone']
```

**Follow-ups:**
- *Should the judge see the reference?* Only if the criterion needs it (correctness); for faithfulness give the context.
- *What about temperature?* Use temperature 0 and a pinned model version, and still expect small variation (Q27).
- *How many examples?* Enough to anchor the edge cases; more can bias the judge toward the examples' style.

**Common mistakes:** a rubric with several criteria mixed together; verdict before reasoning; 1-10 scales with no definitions; examples copied from the test set; defaulting unparseable outputs to PASS; not versioning the judge prompt.

### Q8 ⭐⭐⭐ 🟡 RAGAS-style generation metrics in depth: how are faithfulness and answer relevance computed, what do they miss, and why can faithfulness be 0.9 while users still complain?
**Asked at:** product, GenAI startups, GCC; interview-prep guides pose the 0.9-faithfulness-but-complaints scenario (guides, not candidate reports)
**Say this first (1 line):** Ragas faithfulness is the share of claims in the answer that the retrieved context supports, and answer relevance is how close the questions regenerated from the answer are to the original question; neither checks that the answer is correct or complete, which is how faithfulness can be 0.9 while users still complain.

**Then explain:**
- **Faithfulness:** an LLM splits the answer into claims, checks each against the retrieved context, and the score is supported claims divided by total claims. The Ragas docs' example: a claim set where 1 of 2 is supported scores 0.5 (official docs, opened).
- **Answer (response) relevancy:** an LLM generates questions from the answer (default 3), and the score is the mean cosine similarity between each generated question's embedding and the original question's. The docs state it does not check factuality.
- **What they miss:** (1) faithful to wrong or stale context: a correct summary of the wrong document scores 1.0; (2) incompleteness: leaving out half the answer keeps relevance high; (3) retrieval failure: nothing here checks that the right chunks were fetched (Q16); (4) the verifier's own errors; (5) averaging: a mean hides a tail of bad answers.
- **Why 0.9 with complaints:** the metric asks 'is what you said supported?' not 'did you solve the problem?' Pair it with correctness or resolution labels, context metrics, and error analysis of complaints (Q15, Q17).
- **Scope:** the overview of generation metrics is in Part 6 Q39; here the point is how they break. The Ragas page for context recall was not opened for this answer.

**Example:** Toy implementation (word overlap standing in for the LLM verdicts, bag-of-words cosine standing in for embeddings): the Einstein-style case gives 0.5, matching the docs' pattern. An answer faithful to a stale document (14 days, current policy 30) scores 1.0. Synthetic 10-answer set (assumed numbers): mean faithfulness 0.9, human-judged resolved rate 0.6, and 2 of the 8 perfectly faithful answers were not resolved. Relevance of an on-topic but partial answer is 0.69; an off-topic answer scores 0.0.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# RAGAS-style metrics from scratch with MOCK components (word-overlap 'entailment', bag-of-words
# 'embedding'). Real Ragas uses an LLM for claim extraction and verdicts and a real embedding model.
import math, re
from collections import Counter

def words(s): return re.findall(r"[a-z0-9$]+", s.lower())
def supported(claim, context):                 # mock verdict: all content words appear in context
    stop = {"the", "is", "a", "of", "in", "to", "and"}
    cw = [w for w in words(claim) if w not in stop]
    return all(w in set(words(context)) for w in cw)

def faithfulness(claims, context):             # supported claims / total claims
    return sum(supported(c, context) for c in claims) / len(claims)

def cos(a, b):
    a, b = Counter(words(a)), Counter(words(b))
    dot = sum(a[w] * b[w] for w in a)
    return dot / (math.sqrt(sum(v*v for v in a.values())) * math.sqrt(sum(v*v for v in b.values())) or 1)

def answer_relevance(question, generated_questions):   # mean cosine(question, questions generated from the answer)
    return sum(cos(question, g) for g in generated_questions) / len(generated_questions)

ctx = "Einstein was born in Germany. The refund window is 30 days."
print("faithfulness, Einstein-style (1 of 2 claims supported):",
      faithfulness(["Einstein was born in Germany", "Einstein was born on 20 March 1879"], ctx))

# Faithful but wrong: the retriever returned an OLD policy; the answer is faithful to it.
stale = "The refund window is 14 days."
print("faithful to a stale doc:", faithfulness(["The refund window is 14 days"], stale), "(current policy: 30 days)")

# Faithful but incomplete: answers only restate one safe fact; relevance sees on-topic questions.
q = "What is the refund window and how do I request a refund?"
print("answer relevance, on-topic but partial answer:",
      round(answer_relevance(q, ["What is the refund window?", "How long is the refund window?"]), 2))
print("answer relevance, off-topic answer:",
      round(answer_relevance(q, ["Where was Einstein born?"]), 2))

# Mean 0.9 can still hide complaints: 10 SYNTHETIC answers (all numbers assumed)
faith    = [1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0.5]   # per-answer faithfulness (supported claims / claims)
resolved = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0]       # human: was the user's problem solved?
print("mean faithfulness:", round(sum(faith) / 10, 2), "| resolved rate:", sum(resolved) / 10)
print("answers with faithfulness 1.0 that were NOT resolved:",
      sum(1 for f, r in zip(faith, resolved) if f == 1 and r == 0), "of", sum(1 for f in faith if f == 1))
```
**Output (my run):**
```
faithfulness, Einstein-style (1 of 2 claims supported): 0.5
faithful to a stale doc: 1.0 (current policy: 30 days)
answer relevance, on-topic but partial answer: 0.69
answer relevance, off-topic answer: 0.0
mean faithfulness: 0.9 | resolved rate: 0.6
answers with faithfulness 1.0 that were NOT resolved: 2 of 8
```

**Follow-ups:**
- *Reference-free or with reference?* Faithfulness and response relevancy need no gold answer; correctness needs one.
- *Is faithfulness the same as hallucination rate?* Close but not equal: it is relative to the context, not to the world (Q9).
- *How do you debug a low score?* Read the unsupported claims; check whether retrieval or generation caused them (Q17).

**Common mistakes:** reading faithfulness as correctness; averaging without looking at the tail; ignoring that the verifier is an LLM that can be wrong; using relevance to judge completeness; treating one tool's metric name as a standard across libraries.

### Q9 ⭐⭐⭐ 🟡 How do you detect hallucinations and measure groundedness (claim decomposition plus entailment checks, citation verification, sampling-consistency checks, abstention rate), and what are the limits of each?
**Asked at:** all types; product, GenAI startups, GCC
**Say this first (1 line):** Hallucination checks split the answer into claims and test each against sources (entailment), verify that cited passages really support their claims, sample several answers and look for disagreement, and track how often the system abstains; each has blind spots, so combine them with human review.

**Then explain:**
- **Claim decomposition plus entailment:** extract atomic claims, then ask an NLI model or LLM whether the source entails each. Output: share of grounded claims and the list of unsupported ones. Limits: decomposition errors, subtle numbers, and the checker's own mistakes; it checks against the source, not the world.
- **Citation verification:** check that each cited passage exists and supports the sentence that cites it. Catches fake and misattached citations; does not catch uncited claims.
- **Sampling consistency (SelfCheckGPT-style):** sample several answers and flag claims they disagree on, with no source needed (SelfCheckGPT, tested on GPT-3 WikiBio passages, abstract). Limit: a model can be consistently wrong, so agreement is not truth.
- **Abstention rate:** on unanswerable questions, how often the system says it does not know (and how often it wrongly abstains on answerable ones). A system that never abstains will hallucinate on them.
- **Connect to metrics:** faithfulness in Q8 is the claim-level version of the first check; context quality is Q16; separating retrieval from generation failures is Q17.

**Example:** Synthetic source about a company. Four claims: 3 grounded, the invented "900 employees" flagged, grounded-claim rate 0.75. A citation check confirms the first two citations and fails the third. Sampling: an unsure mock model gave 400, 400, 400, 150, 900 (agreement 0.6, majority happens to be right); a confidently wrong mock gave 900 five times (agreement 1.0, truth 400), which is the case consistency checks miss. Abstention on 4 unanswerable cases: 1 of 4 = 0.25.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# Hallucination checks on a MOCK knowledge setting (synthetic). Lexical 'entailment' stands in for an NLI model/LLM.
import random, re
random.seed(2)
SOURCE = "Acme was founded in 1998 in Pune. Its CEO is Rao. It has 400 employees."
def words(s): return set(re.findall(r"[a-z0-9]+", s.lower()))
def entailed(claim, src=SOURCE): return words(claim) <= words(src) | {"is", "was", "the", "a", "it"}

answer_claims = ["Acme was founded in 1998", "Acme was founded in Pune", "Acme has 900 employees", "Its CEO is Rao"]
flags = [entailed(c) for c in answer_claims]
print("claim decomposition + entailment:", list(zip(answer_claims, flags)))
print("grounded-claim rate:", sum(flags) / len(flags))

# citation verification: each claim cites a sentence index; check the cited sentence supports it
sentences = [s.strip() for s in SOURCE.split(".") if s.strip()]
cites = [(answer_claims[0], 0), (answer_claims[3], 1), (answer_claims[2], 2)]
for c, i in cites:
    print(f"citation [{i}] supports '{c}':", entailed(c, sentences[i]))

# sampling consistency (SelfCheck-style): sample 5 answers to 'how many employees?' from a mock model
def mock_sampler(kind):
    if kind == "unsure":   return random.choice(["400", "900", "150", "1200", "60"])
    if kind == "confident_wrong": return "900"     # consistently wrong
for kind in ("unsure", "confident_wrong"):
    s = [mock_sampler(kind) for _ in range(5)]
    top = max(set(s), key=s.count)
    print(f"{kind:16s} samples={s} agreement={s.count(top)/5:.1f} answer={top} (truth 400)")

# abstention rate on unanswerable questions (synthetic 10 cases, 4 unanswerable)
unanswerable = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
abstained    = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
ab_rate = sum(a for a, u in zip(abstained, unanswerable) if u) / sum(unanswerable)
print("abstention on unanswerable:", ab_rate, "| false abstention on answerable:",
      sum(a for a, u in zip(abstained, unanswerable) if not u) / unanswerable.count(0))
```
**Output (my run):**
```
claim decomposition + entailment: [('Acme was founded in 1998', True), ('Acme was founded in Pune', True), ('Acme has 900 employees', False), ('Its CEO is Rao', True)]
grounded-claim rate: 0.75
citation [0] supports 'Acme was founded in 1998': True
citation [1] supports 'Its CEO is Rao': True
citation [2] supports 'Acme has 900 employees': False
unsure           samples=['400', '400', '400', '150', '900'] agreement=0.6 answer=400 (truth 400)
confident_wrong  samples=['900', '900', '900', '900', '900'] agreement=1.0 answer=900 (truth 400)
abstention on unanswerable: 0.25 | false abstention on answerable: 0.0
```

**Follow-ups:**
- *Which one first?* Claim-level entailment against retrieved context, plus abstention on a labelled unanswerable set.
- *Black-box vs white-box?* Sampling checks work through an API; token-probability methods need logits.
- *How do you validate the detector?* Same way as any judge: human labels, TPR and TNR (Q6).

**Common mistakes:** treating consistency as correctness; checking the answer against itself; ignoring abstention; verifying only citation format and not content; trusting a detector never calibrated on your domain.

### Q10 ⭐⭐⭐ 🟡 Public benchmarks (MMLU, HumanEval, SWE-bench, MT-Bench, Chatbot Arena): what does each measure, and why is a benchmark score not a product evaluation?
**Asked at:** all types; interview-prep guides list benchmark knowledge at junior level (guides, not candidate reports)
**Say this first (1 line):** Public benchmarks measure narrow, standardised abilities (knowledge, small coding functions, repository bug fixes, multi-turn chat quality, human preference), so they are useful for shortlisting models but a score says little about your users, your data or your system.

**Then explain:**
- **MMLU:** 57 multiple-choice subject tasks testing knowledge; at publication most models were near chance and the largest GPT-3 about 20 points above (paper abstract). MMLU-Pro made it harder with 10 options and cleaner questions; the authors report accuracy drops of 16% to 33% and lower prompt sensitivity (authors' claim).
- **HumanEval:** 164 hand-written Python problems with an average of 7.7 unit tests each, scored by functional correctness (Codex paper). It tests small function writing, not software engineering (Q22).
- **SWE-bench:** 2,294 problems from real GitHub issues in 12 Python repos, scored by whether the patch passes the repository's tests; in the original paper the best model resolved 1.96% (abstract, long superseded). Current scores and Verified-subset figures change; check the live leaderboard.
- **MT-Bench:** 80 multi-turn questions across 8 categories, scored by an LLM judge. **Chatbot Arena:** crowdsourced pairwise human votes ranked statistically; the Arena paper cites over 240K votes at the time (details in Q19, Q20).
- **Why it is not a product eval:** different task mix, different prompts and data, contamination and saturation (Q21), implementation sensitivity, and no system effects. Hugging Face reported llama-65b at 0.637, 0.488 and 0.636 on MMLU from three implementations at that time (vendor blog), and Anthropic notes small format changes shift accuracy by about 5% (vendor post).
- **How to use:** shortlist models, then run your own golden set (Q2) on your system.

**Example:** Two synthetic models with assumed per-task pass rates. On a benchmark mix of 70% math MCQs and 30% code, model X wins 0.84 vs 0.77. On a product mix (60% support chat, 30% extraction, 10% code) model Y wins 0.805 vs 0.64. Format sensitivity: a mock multiple-choice model that knows half the answers (assumed) and guesses with a bias to option A scores 0.702 when the gold answer is always A and 0.627 when the gold slot is random.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# Why a benchmark score is not a product eval: two toy demonstrations on SYNTHETIC models.
import random
random.seed(4)

# 1) Ranking flips when the task mix changes. Skill = pass rate per task type (ASSUMED numbers).
skills = {"model_X": {"math_mcq": 0.90, "code": 0.70, "support_chat": 0.60, "extraction": 0.70},
          "model_Y": {"math_mcq": 0.80, "code": 0.70, "support_chat": 0.80, "extraction": 0.85}}
bench_mix   = {"math_mcq": 0.7, "code": 0.3, "support_chat": 0.0, "extraction": 0.0}   # what the benchmark tests
product_mix = {"math_mcq": 0.0, "code": 0.1, "support_chat": 0.6, "extraction": 0.3}   # what our users do
for name, mix in (("benchmark mix", bench_mix), ("product mix", product_mix)):
    sc = {m: sum(mix[t] * v for t, v in s.items()) for m, s in skills.items()}
    print(f"{name:14s}", {m: round(v, 3) for m, v in sc.items()}, "winner:", max(sc, key=sc.get))

# 2) Format sensitivity: a mock multiple-choice model that knows 50% of answers (assumed) and
#    otherwise guesses with a bias toward letter A (assumed 40% A, 20% each other).
def run(correct_slot_fn, n=20000):
    ok = 0
    for _ in range(n):
        gold = correct_slot_fn()
        if random.random() < 0.5: pick = gold
        else: pick = random.choices("ABCD", [0.4, 0.2, 0.2, 0.2])[0]
        ok += pick == gold
    return ok / n
print("accuracy, gold always listed as A:", round(run(lambda: "A"), 3))
print("accuracy, gold in random slot    :", round(run(lambda: random.choice("ABCD")), 3))
```
**Output (my run):**
```
benchmark mix  {'model_X': 0.84, 'model_Y': 0.77} winner: model_X
product mix    {'model_X': 0.64, 'model_Y': 0.805} winner: model_Y
accuracy, gold always listed as A: 0.702
accuracy, gold in random slot    : 0.627
```

**Follow-ups:**
- *Which benchmark is closest to a product?* Whichever shares your task and data; none replace your own eval.
- *Why do different tools report different MMLU numbers?* Prompt format, answer extraction and few-shot setup differ.
- *Is Arena a product eval?* It measures broad human preference on its users' prompts, not your task (Q20).

**Common mistakes:** picking a model by leaderboard rank alone; comparing numbers from different harnesses; assuming a high benchmark score means no regression on your task; quoting scores without the setting; ignoring contamination.

### Q11 ⭐⭐⭐ 🟡 Your new prompt scores 82% and the old one 80% on 200 test cases. Is it better? Cover confidence intervals, paired comparison, and how much to trust small differences.
**Asked at:** product, GenAI startups, evaluation-focused rounds, senior roles
**Say this first (1 line):** Not on this evidence: 82% vs 80% on 200 cases is a 4-case difference, the intervals overlap heavily, and even a paired test on the same cases usually cannot call it unless the two prompts almost never disagree.

**Then explain:**
- **Interval for each score:** a Wilson 95% interval for 164/200 is about 0.761 to 0.867 and for 160/200 about 0.739 to 0.850, so they overlap a lot. Report a rate with an interval, not a bare number (Miller's 'Adding error bars to evals' frames evals as samples from a super-population; abstract).
- **Use the pairing:** both prompts ran on the same cases, so compare per case. Only discordant cases matter: b = new right and old wrong, c = old right and new wrong. A net +4 can come from 4 vs 0 or 34 vs 30.
- **Test:** exact McNemar test (binomial on b and c) or a paired bootstrap of the difference. The unpaired z-test ignores the pairing and is the wrong tool here (Q28; bootstrap code is Q38).
- **Trust small differences?** Little. Also repeated runs add noise (Q27), many comparisons add false positives (Q28), and sample size sets what you can detect (Q26).
- **Practical answer:** say you cannot conclude it is better; check the discordant cases, enlarge the set, or decide on other grounds (cost, latency, qualitative review).

**Example:** Numbers from the run. Unpaired z = 0.51, p = 0.61. With the same +4 net wins: b=4, c=0 gives McNemar p = 0.125; b=6, c=2 gives 0.289; b=14, c=10 gives 0.541; b=34, c=30 gives 0.708. Even a 4-vs-0 result is not significant at 0.05. The paired bootstrap CI for 4-vs-0 came out (+0.005, +0.040), which excludes zero while exact McNemar says p = 0.125; with so few discordant cases the percentile bootstrap is too optimistic, so prefer the exact test there. Simulated power for a true +2 point gain (assumed 7% new-only wins, 5% old-only) at n = 200 was only 0.08.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# Is 82% vs 80% on 200 cases a real gain? Wilson CI, unpaired z, exact McNemar, paired bootstrap.
import math, random
from math import comb
random.seed(8)

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = p + z*z/(2*n)
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return (c - h) / d, (c + h) / d
print("old 160/200 Wilson 95%:", tuple(round(x, 3) for x in wilson(160, 200)))
print("new 164/200 Wilson 95%:", tuple(round(x, 3) for x in wilson(164, 200)))

# unpaired two-proportion z-test (ignores that both prompts saw the same cases)
p1, p2 = 160/200, 164/200; pp = (160+164)/400
z = (p2 - p1) / math.sqrt(pp*(1-pp)*(2/200)); pval = math.erfc(abs(z)/math.sqrt(2))
print(f"unpaired z={z:.2f}, p={pval:.2f}")

def mcnemar_exact(b, c):               # two-sided exact binomial on discordant pairs, p0 = 0.5
    d = b + c; k = min(b, c)
    return min(1.0, 2 * sum(comb(d, i) for i in range(k + 1)) / 2**d)
def mcnemar_brute(b, c):               # enumerate all 2^d sign patterns
    d = b + c; k = min(b, c); tail = 0
    for mask in range(2**d):
        ones = bin(mask).count("1")
        if min(ones, d - ones) <= k: tail += 1
    return tail / 2**d
for b, c in ((4, 0), (6, 2), (7, 3)):
    assert abs(mcnemar_exact(b, c) - mcnemar_brute(b, c)) < 1e-12
print("exact McNemar matches brute-force enumeration: OK")

def paired_boot(b, c, n=200, reps=4000):          # cases where new wins = b, old wins = c
    diffs = [0]*(n-b-c) + [1]*b + [-1]*c
    out = sorted(sum(random.choice(diffs) for _ in range(n)) / n for _ in range(reps))
    return out[int(.025*reps)], out[int(.975*reps)]
print("same +4 net wins, different overlap (b = new-only wins, c = old-only wins):")
for b, c in ((4, 0), (6, 2), (14, 10), (34, 30)):
    lo, hi = paired_boot(b, c)
    print(f"  b={b:2d} c={c:2d} discordant={b+c:2d} McNemar p={mcnemar_exact(b, c):.3f} paired-bootstrap 95% CI for diff=({lo:+.3f}, {hi:+.3f})")

# power: true rates new-only win 7%, old-only win 5% (assumed), n=200, exact McNemar at p<0.05
def power(n=200, pb=0.07, pc=0.05, reps=3000):
    hit = 0
    for _ in range(reps):
        b = c = 0
        for _ in range(n):
            r = random.random()
            if r < pb: b += 1
            elif r < pb + pc: c += 1
        hit += (b + c > 0) and mcnemar_exact(b, c) < 0.05
    return hit / reps
print("simulated power to detect a true +2 point gain with n=200:", round(power(), 2))
```
**Output (my run):**
```
old 160/200 Wilson 95%: (0.739, 0.85)
new 164/200 Wilson 95%: (0.761, 0.867)
unpaired z=0.51, p=0.61
exact McNemar matches brute-force enumeration: OK
same +4 net wins, different overlap (b = new-only wins, c = old-only wins):
  b= 4 c= 0 discordant= 4 McNemar p=0.125 paired-bootstrap 95% CI for diff=(+0.005, +0.040)
  b= 6 c= 2 discordant= 8 McNemar p=0.289 paired-bootstrap 95% CI for diff=(-0.005, +0.050)
  b=14 c=10 discordant=24 McNemar p=0.541 paired-bootstrap 95% CI for diff=(-0.025, +0.070)
  b=34 c=30 discordant=64 McNemar p=0.708 paired-bootstrap 95% CI for diff=(-0.055, +0.100)
simulated power to detect a true +2 point gain with n=200: 0.08
```

**Follow-ups:**
- *How many cases do you need?* Roughly, enough discordant cases to see the effect; see Q26.
- *What if the real gain is 2 points?* Then 200 cases will miss it most of the time, as the power simulation shows.
- *Can you just rerun?* Reruns reduce run noise but not case-sampling noise (Q27).

**Common mistakes:** comparing two intervals by eye for overlap; using an unpaired test on paired data; declaring a winner from a 2-point gap; running many variants and keeping the best (selection bias, Q28); ignoring run-to-run randomness.

### Q12 ⭐⭐⭐ 🟡 What is pass@k? Explain the unbiased estimator from the Codex paper, why naive 'best of k' reporting is biased, and how pass@k differs from pass^k (all k succeed).
**Asked at:** product, big tech, code-model and evaluation-focused rounds; an interview guide lists implementing pass@k as a senior-level exercise (a guide, not a candidate report)
**Say this first (1 line):** pass@k is the probability that at least one of k sampled solutions passes the tests; the unbiased estimator draws n >= k samples, counts c correct, and computes 1 - C(n-c, k) / C(n, k) per problem, then averages across problems.

**Then explain:**
- **Definition and estimator:** the Codex paper defines pass@k as the expectation over problems of 1 - C(n-c, k)/C(n, k), and used n = 200 samples with k <= 100 (paper body, read for this answer). The estimate is exact for the probability that a random size-k subset of your n samples contains a pass, which is unbiased for the true pass@k.
- **Why not generate exactly k and count?** That works but is noisy; many samples and the formula give a lower-variance estimate for every k at once. The stable code multiplies terms instead of computing huge binomials.
- **The biased shortcut:** estimating pass@k as 1 - (1 - p_hat)^k with the empirical pass@1 is biased. The paper says it consistently underestimates and the gap does not fully close even for n > 5k (Appendix A and Figure 13). Another meaning of 'best of k' bias: if you pick the best sample using the tests and report it as pass@1, you reported pass@k under the wrong name; pass@k is only honest when you say k and the tests are the selector, which is not available in a product.
- **pass^k (all k succeed):** the probability that every one of k trials passes, about p^k for independent trials, estimated by C(c, k)/C(n, k). It is the reliability view. Anthropic's agent-evals post gives 75% per trial as about 42% pass^3 (vendor post). pass@k rises with k, pass^k falls.
- **Reported results:** the Codex abstract reports 28.8% solved with a single sample and 70.2% with 100 samples per problem (authors' setting, HumanEval). Implementation is Q13; agent use is Part 8 Q51.

**Example:** Problem with n = 10 samples, c = 3 correct: pass@1 = 0.300 and pass@5 = 0.917. Bias, exact expectation over c for true p = 0.3, n = 10, k = 5: true pass@5 = 0.8319; the unbiased estimator averages 0.8319; the naive 1 - (1 - p_hat)^5 averages 0.7597. A per-trial success of 0.75 gives pass@3 = 0.984 but pass^3 = 0.422. Across three synthetic problems with (n, c) = (10, 10), (10, 7), (10, 2): mean pass@3 = 0.842, mean pass^3 = 0.431.

**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)
```python
# pass@k: Codex-paper unbiased estimator, brute-force check, bias of 1-(1-p_hat)^k, and pass^k.
import itertools, random
from math import comb
import numpy as np
random.seed(0)

def pass_at_k(n, c, k):                # numerically stable form (the Codex paper's Figure 3 script has this shape)
    if n - c < k: return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))
def pass_at_k_closed(n, c, k): return 1.0 - comb(n - c, k) / comb(n, k)
def pass_at_k_brute(n, c, k):          # average over every size-k subset of the n samples
    labels = [1]*c + [0]*(n - c)
    subs = list(itertools.combinations(range(n), k))
    return sum(any(labels[i] for i in s) for s in subs) / len(subs)

worst = 0
for n in range(1, 9):
    for c in range(n + 1):
        for k in range(1, n + 1):
            a, b, d = pass_at_k(n, c, k), pass_at_k_closed(n, c, k), pass_at_k_brute(n, c, k)
            worst = max(worst, abs(a - b), abs(a - d))
print("max abs diff, stable vs closed vs brute force (all n<=8):", f"{worst:.1e}")
print("n=10, c=3: pass@1 =", round(pass_at_k(10, 3, 1), 3), "pass@5 =", round(pass_at_k(10, 3, 5), 3))

# Bias: a problem whose TRUE per-sample pass rate is p. Draw n samples, estimate pass@k two ways.
p, n, k = 0.3, 10, 5
true = 1 - (1 - p)**k
pmf = [comb(n, c) * p**c * (1 - p)**(n - c) for c in range(n + 1)]
e_unb = sum(w * pass_at_k(n, c, k) for c, w in enumerate(pmf))
e_naive = sum(w * (1 - (1 - c / n)**k) for c, w in enumerate(pmf))
print(f"true pass@{k} = {true:.4f} | E[unbiased] = {e_unb:.4f} | E[1-(1-p_hat)^k] = {e_naive:.4f} (exact expectation over c)")

# pass@k vs pass^k on one problem with per-sample success 0.75, k=3 (independent trials assumed)
q = 0.75
print(f"per-trial {q}: pass@3 = {1-(1-q)**3:.3f}, pass^3 = {q**3:.3f}")
# pass^k estimator from n samples, c correct: C(c,k)/C(n,k); and an aggregate over 3 toy problems
def pass_hat_k(n, c, k): return comb(c, k) / comb(n, k)
problems = [(10, 10), (10, 7), (10, 2)]      # (n, c) -- synthetic
for k in (1, 3):
    print(f"k={k}: mean pass@k = {np.mean([pass_at_k(n, c, k) for n, c in problems]):.3f}"
          f" | mean pass^k = {np.mean([pass_hat_k(n, c, k) for n, c in problems]):.3f}")
```
**Output (my run):**
```
max abs diff, stable vs closed vs brute force (all n<=8): 1.1e-16
n=10, c=3: pass@1 = 0.3 pass@5 = 0.917
true pass@5 = 0.8319 | E[unbiased] = 0.8319 | E[1-(1-p_hat)^k] = 0.7597 (exact expectation over c)
per-trial 0.75: pass@3 = 0.984, pass^3 = 0.422
k=1: mean pass@k = 0.633 | mean pass^k = 0.633
k=3: mean pass@k = 0.842 | mean pass^k = 0.431
```

**Follow-ups:**
- *Which should a product report?* If the user sees one answer, pass@1 or pass^k; pass@k only when a verifier picks among k.
- *Does pass@k assume independent samples?* The estimator assumes the n samples are drawn independently from the model; temperature and sampling must allow that.
- *HumanEval is small; how do you report uncertainty?* Bootstrap over problems (Q38).

**Common mistakes:** using 1 - (1 - p_hat)^k; reporting pass@100 as if it were what users get; computing the binomials directly and overflowing; using n = k so the estimate is noisy; mixing pass@k and pass^k.

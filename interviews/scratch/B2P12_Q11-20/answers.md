### Q11 ⭐⭐⭐ 🟡 Demo to production: a prototype RAG or agent demo impresses stakeholders. List what changes before launch (data and permissions, evaluation set and quality bar, latency and cost at real volume, abuse and injection, fallbacks, monitoring, ownership), and how do you present 'what could go wrong' and a go or no-go criterion? (Part 9 Q46 is an evaluation strategy for launch; this question is the whole readiness review.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
**Say this first (1 line):** A demo proves the happy path works once; launch readiness means the unhappy paths (other users' data, real queries, real volume, attackers, outages) have been measured against criteria we wrote down before looking, with a named owner and a rollback.

**Then explain:**
- **What changes between demo and launch (one line each, each a pointer to the part that owns it):**
  - *Data and permissions:* the demo used one friendly corpus and one user; production needs per-user ACLs enforced at retrieval, ingestion freshness and deletion (Part 6 Q15, Q17, Q42; Part 11 Q26).
  - *Evaluation:* 20 hand-picked questions become a golden set sampled from real intended users, with a pre-agreed quality bar and a CI gate (Part 9 Q2, Q14; the launch-time evaluation strategy is Part 9 Q46).
  - *Latency and cost at real volume:* measure p95, not the average, and multiply per-request cost by launch volume (Part 6 Q31, Q32; Part 10 Q3, Q13; budgets per tenant in Part 11 Q16).
  - *Abuse and injection:* red-team, the lethal-trifecta review, guardrail layers, no write tools without approval (Part 11 Q9, Q28, Q40; Part 5 Q8; Part 8 Q24).
  - *Fallbacks:* timeouts, retries, circuit breaker, a degraded mode that still answers or says "I don't know" (Part 11 Q15; Part 6 Q27; this part's Q20).
  - *Monitoring and ownership:* traces, sampled quality scoring, alerts, an on-call owner, a content owner, a rollback switch, staged rollout (Part 11 Q2, Q6; Part 9 Q30).
- **How to present "what could go wrong":** a short risk table, not a speech. Columns: failure, who is hurt, how likely (a measured rate with an interval, or "unknown"), how we detect it, what limits the damage, owner. Sort by severity times likelihood and say plainly which rows are still "unknown".
- **Go/no-go criterion:** write thresholds before the final eval run, and use the lower confidence bound for quality (a pass rate on 200 samples is a range, not a point). Split criteria into hard blockers (any cross-user data leak, injection that triggers a write action) and soft targets (quality, p95, cost per day).
- **Zero failures does not prove zero risk:** 0 leaks in 60 red-team attempts still leaves an upper bound near 6 per cent (the code below). More attempts, or a lower bar for the claim, are the only fixes.
- **Staged launch is part of the decision:** go for 5 per cent of users with auto-rollback triggers is a different decision from go for everyone (Part 11 Q6).

**Example:** Synthetic numbers (labelled in the code): the demo set passes 19 of 20 (0.95). A sample of 200 real-style queries passes 172 (0.86, Wilson 95% interval 0.805 to 0.901). The bar was "lower bound at least 0.80": passes, barely. Red team: 0 leaks in 60 attempts, but the 95% upper bound is 0.0602 against an agreed limit of 0.06, so that row fails and the decision is NO-GO. The fix is not to argue about the threshold; it is to run more attack cases (or narrow the claim) and re-decide. p95 latency (4.56 s, assumed lognormal sample) and daily cost (0.012 per request times 40,000 requests = 480, assumed) both pass.

**Code:** (mocked/toy inputs only; run with `python3 -I`)
```python
# Launch-readiness gate for a RAG demo. ALL inputs are SYNTHETIC or ASSUMED (labelled); no real model, no network.
import math, random

def wilson(k, n, z=1.96):
    """Wilson score interval for a proportion k/n."""
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

# --- check the closed form: at each bound, (p_hat - p)/sqrt(p(1-p)/n) must equal +-z
k, n = 172, 200
lo, hi = wilson(k, n)
for b in (lo, hi):
    zscore = (k / n - b) / math.sqrt(b * (1 - b) / n)
    assert abs(abs(zscore) - 1.96) < 1e-9, zscore

# --- SYNTHETIC evidence a team might hold the week before launch
demo_set = (19, 20)         # 20 hand-picked demo questions: 19 pass
real_sample = (172, 200)    # 200 real-style queries sampled from the intended users: 172 pass
redteam = (0, 60)           # 60 injection/ACL-leak attempts: 0 leaks (a leak is a failure)
acl_leaks = 0               # cross-user documents seen in 500 permission-test queries

# --- ASSUMED latency sample (lognormal, synthetic) and ASSUMED per-request cost
rng = random.Random(7)
lat = sorted(rng.lognormvariate(math.log(2.2), 0.45) for _ in range(2000))   # seconds
p95 = lat[int(0.95 * len(lat)) - 1]
COST_PER_REQ = 0.012        # ASSUMED currency units per request
REQS_PER_DAY = 40_000       # ASSUMED launch volume
daily_cost = COST_PER_REQ * REQS_PER_DAY

CRITERIA = {                # the go/no-go contract, agreed BEFORE the review
    "quality_lower_bound_min": 0.80,
    "max_acl_leaks": 0,
    "max_redteam_leaks_upper95": 0.06,
    "p95_latency_s_max": 6.0,
    "daily_cost_max": 600.0,
}

def gate(c):
    lo_q, hi_q = wilson(*real_sample)
    lo_r, hi_r = wilson(*redteam)
    checks = [
        ("quality (Wilson lower bound on real sample)", lo_q >= c["quality_lower_bound_min"], f"{lo_q:.3f} vs >= {c['quality_lower_bound_min']}"),
        ("ACL leaks in permission tests", acl_leaks <= c["max_acl_leaks"], f"{acl_leaks} vs <= {c['max_acl_leaks']}"),
        ("red-team leak rate (95% upper bound)", hi_r <= c["max_redteam_leaks_upper95"], f"{hi_r:.4f} vs <= {c['max_redteam_leaks_upper95']}"),
        ("p95 latency", p95 <= c["p95_latency_s_max"], f"{p95:.2f}s vs <= {c['p95_latency_s_max']}s"),
        ("daily cost at launch volume", daily_cost <= c["daily_cost_max"], f"{daily_cost:.0f} vs <= {c['daily_cost_max']:.0f}"),
    ]
    return all(ok for _, ok, _ in checks), checks

print("demo set pass rate:   %.2f (n=%d)" % (demo_set[0] / demo_set[1], demo_set[1]))
print("real sample pass rate: %.2f (n=%d), 95%% Wilson interval %.3f-%.3f" % (real_sample[0] / real_sample[1], real_sample[1], lo, hi))
ok, checks = gate(CRITERIA)
for name, passed, detail in checks:
    print(("PASS " if passed else "FAIL ") + name + ": " + detail)
print("DECISION:", "GO" if ok else "NO-GO")

# test: a tighter quality bar flips the decision, and a single ACL leak always blocks
strict = dict(CRITERIA, quality_lower_bound_min=0.85)
assert gate(strict)[0] is False
acl_leaks = 1
assert gate(CRITERIA)[0] is False
print("tests passed: strict bar -> NO-GO; one ACL leak -> NO-GO")
```
**Output (my run):**
```text
demo set pass rate:   0.95 (n=20)
real sample pass rate: 0.86 (n=200), 95% Wilson interval 0.805-0.901
PASS quality (Wilson lower bound on real sample): 0.805 vs >= 0.8
PASS ACL leaks in permission tests: 0 vs <= 0
FAIL red-team leak rate (95% upper bound): 0.0602 vs <= 0.06
PASS p95 latency: 4.56s vs <= 6.0s
PASS daily cost at launch volume: 480 vs <= 600
DECISION: NO-GO
tests passed: strict bar -> NO-GO; one ACL leak -> NO-GO
```
The gate is a function of data and a criteria dict, so changing a threshold or adding one ACL leak flips the decision in a test, which is the point: the contract is executable. The demo-versus-real gap (0.95 versus 0.86) is also the usual story.

**Follow-ups:**
- *Who signs off?* Product owner for quality and scope, security for the blocker rows, an on-call engineer for operability. Name them in the table; a risk without an owner is a risk nobody mitigates.
- *What if the quality bar is missed by a little?* Launch narrower (fewer intents, or human review on low-confidence answers) rather than relaxing the bar, and say which slice you excluded.
- *What goes in the first week after launch?* Heavier sampling of traces, a daily look at refusals, thumbs-down and escalations, and a pre-agreed rollback trigger (Part 11 Q6).

**Common mistakes:**
- Presenting the demo pass rate as the quality estimate; testing on questions the builders wrote.
- Setting thresholds after seeing the results.
- Reporting averages (latency, quality) with no tail or interval.
- Treating security as a late checklist item instead of a blocker row with an owner.
- No rollback path, so "go" is irreversible.


### Q12 ⭐⭐⭐ 🔴 Design a multilingual assistant for Indian users (Hindi, English, Hinglish and a few regional languages, text and voice): language detection and code-mixed input, tokenizer cost, embedding and retrieval across languages, answering language and script, translation vs native generation, ASR errors on code-mixed audio, safety and tone, and per-language evaluation so averages do not hide weak languages. (Part 2 Q17, Part 6 Q35 and Part 9 Q34 cover the pieces; ASR error figures differ widely by vendor and test set.)
**Asked at:** BFSI and fintech GenAI teams, GCCs and product companies (company-type tag from guides and regulator material, not a candidate report)
**Say this first (1 line):** Detect language and script per message (not per user), keep one multilingual retrieval index with metadata, answer in the language and script the user used, and judge quality per language with intervals because the average will hide the weak ones.

**Then explain:**
- **Language and script detection:** code-mixed input is common (Hindi in Roman script, Hindi in Devanagari, English words inside either). Detect script by Unicode block (cheap, exact) and language by a trained classifier with a confidence; route low-confidence cases to a safe default plus a clarifying turn. A word-list heuristic is a toy: the code shows it missing a short code-mixed message.
- **Tokenizer cost:** non-Latin scripts usually cost more tokens per word, which means more money, more latency and less usable context (Part 2 Q17). In the code, UTF-8 bytes per word is only a worst-case proxy (5.4 for the English line versus 11.8 for the Hindi line), not a real tokenizer; measure your own tokenizer on a sample of your own traffic.
- **Retrieval across languages:** a multilingual embedding model lets a Hindi query hit an English document; alternatively translate the query to the corpus language, or keep per-language indexes (Part 6 Q35). Use hybrid search (Part 7 Q2): BM25 helps on product names and numbers, which stay in Latin script. Test the choice per language, not overall.
- **Answer language and script:** reply in the language and script the user wrote in, unless a stored preference says otherwise. Romanised Hindi in, romanised Hindi out; this is a product rule, written down as code so it can be tested.
- **Translate vs generate natively:** translating the final answer is easy to build but can garble numbers, names and domain terms; native generation reads better but is less reliable in weaker languages. Keep numbers, product names and legal terms copied verbatim from the source, and check them after generation.
- **Voice (ASR) on code-mixed audio:** transcripts mix scripts and spellings (the same word in Devanagari or Roman). Normalise script and spelling before scoring: in the toy run, raw WER is 1.0 for an identical sentence written in the other script, 0.0 after normalisation, and 0.25 for a genuinely inserted word. Published Hinglish WER ranges are vendor figures on different test sets; I do not use any here. Read back key entities (amounts, account digits) before acting.
- **Safety and tone:** safety classifiers and refusal behaviour are weaker in lower-resource languages, so red-team in each supported language (Part 11 Q28); use the register users expect (respectful "aap" forms in Hindi, for example; this is a language-style point, ask native reviewers).
- **Per-language evaluation:** report each language with an interval and a floor, and mark slices as OK, WEAK or UNDERPOWERED (Part 9 Q34). A language with 20 test cases cannot be called fine or broken.

**Example:** A user types "mera balance kitna hai" in Roman script. Script detection says Latin letters; the lexicon says romanised Hindi (4 of 4 words are in the list); the policy answers in Roman-script Hinglish. Retrieval embeds the query with a multilingual model against English FAQ chunks. The answer shows the balance from a tool call (a number, not generated text). The same sentence in Devanagari takes the Devanagari path. Evaluation (synthetic counts, labelled): English 188/200, Hindi 172/200, Hinglish 70/100, Tamil 36/60, Bengali 9/20. The micro average is 0.819 and the traffic-weighted 0.834, which looks acceptable, while Tamil (95% interval 0.47 to 0.71) and Bengali (0.26 to 0.66) are below a 0.75 floor and Hinglish (0.60 to 0.78) is too uncertain to call.

**Code:** (mocked/toy inputs only; run with `python3 -I`)
```python
# Multilingual assistant pieces: script/language routing, token-cost proxy, ASR scoring, per-language gate.
# ALL data are SYNTHETIC toys; the cost proxy is UTF-8 bytes, NOT a real tokenizer (see Part 2 Q17 for real tokenizers).
import math, unicodedata

# ---- 1. script and code-mix detection --------------------------------------------------------
ROMAN_HINDI = {"mera", "meri", "kitna", "kitni", "hai", "kya", "kaise", "karna", "paisa", "nahi", "bhejo", "balance", "chahiye", "mujhe", "ka", "ki", "ko"}
def script_of(ch):
    if "DEVANAGARI" in unicodedata.name(ch, ""): return "deva"
    if ch.isascii() and ch.isalpha(): return "latin"
    return None
def profile(text):
    counts = {"deva": 0, "latin": 0}
    for ch in text:
        s = script_of(ch)
        if s: counts[s] += 1
    words = [w.strip("?.,!").lower() for w in text.split()]
    roman_hits = sum(w in ROMAN_HINDI for w in words)
    total = max(1, counts["deva"] + counts["latin"])
    if counts["deva"] and counts["latin"]: label = "mixed-script"
    elif counts["deva"]: label = "hindi-devanagari"
    elif roman_hits >= 2 and roman_hits / max(1, len(words)) >= 0.4: label = "romanised-hindi/hinglish"
    else: label = "english-or-other"
    return label, round(counts["deva"] / total, 2)

def reply_script(user_text):
    """Policy: answer in the language AND script the user wrote in, unless the profile has a stored preference."""
    label, _ = profile(user_text)
    return {"hindi-devanagari": "hindi in Devanagari", "mixed-script": "match dominant script",
            "romanised-hindi/hinglish": "hinglish in Roman script", "english-or-other": "english"}[label]

samples = ["What is my account balance?", "मेरा बैलेंस कितना है?", "mera balance kitna hai", "mera balance कितना hai?"]
for s in samples: print(profile(s), "->", reply_script(s), "|", s)
assert profile("mera balance kitna hai")[0] == "romanised-hindi/hinglish"
assert profile("What is my account balance?")[0] == "english-or-other"
# honest weakness: short romanised input with one hint word is not caught
print("weak case:", profile("send paisa to Ravi"), "(a lexicon heuristic misses short code-mixed text; use a trained detector and confidence)")

# ---- 2. token-cost proxy: UTF-8 bytes per word ------------------------------------------------
pair = ("What is my account balance?", "मेरा खाता शेष कितना है?")
for t in pair:
    b = len(t.encode()); w = len(t.split())
    print(f"{b:3d} bytes, {w} words, {b / w:.1f} bytes/word | {t}")
print("note: byte-level fallback is the WORST case; real tokenizers vary, measure yours on a sample of your own traffic")

# ---- 3. ASR scoring: WER is meaningless until script and spelling are normalised ---------------
def wer(ref, hyp):
    r, h = ref.split(), hyp.split()
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = d[j]
            d[j] = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev = cur
    return d[len(h)] / len(r)
assert wer("a b c", "a b c") == 0 and wer("a b c", "a x c") == 1 / 3 and wer("a b", "a b c d") == 1.0
TRANSLIT = {"मेरा": "mera", "बैलेंस": "balance", "कितना": "kitna", "है": "hai"}   # toy 4-word map
def norm(s): return " ".join(TRANSLIT.get(w, w).lower() for w in s.split())
ref = "mera balance kitna hai"
hyp = "मेरा बैलेंस कितना है"          # same words, ASR wrote Devanagari
print("raw WER:", wer(ref, hyp), "| after script normalisation:", wer(norm(ref), norm(hyp)))
hyp2 = "mera balance kitna hai kya"
print("real error (inserted word) WER:", wer(norm(ref), norm(hyp2)))

# ---- 4. per-language gate: averages hide the weak language -------------------------------------
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
# SYNTHETIC eval counts: (language, correct, n). Traffic share is also SYNTHETIC.
EVAL = [("english", 188, 200, 0.45), ("hindi", 172, 200, 0.25), ("hinglish", 70, 100, 0.20), ("tamil", 36, 60, 0.07), ("bengali", 9, 20, 0.03)]
micro = sum(c for _, c, _, _ in EVAL) / sum(n for _, _, n, _ in EVAL)
weighted = sum(c / n * s for _, c, n, s in EVAL)
print(f"micro-average {micro:.3f}, traffic-weighted {weighted:.3f}")
FLOOR = 0.75
for lang, c, n, share in EVAL:
    lo, hi = wilson(c, n)
    status = "OK" if lo >= FLOOR else ("WEAK" if hi < FLOOR else "UNDERPOWERED")
    print(f"{lang:9s} {c}/{n} = {c/n:.2f}  95% CI {lo:.2f}-{hi:.2f}  -> {status}")
```
**Output (my run):**
```text
('english-or-other', 0.0) -> english | What is my account balance?
('hindi-devanagari', 1.0) -> hindi in Devanagari | मेरा बैलेंस कितना है?
('romanised-hindi/hinglish', 0.0) -> hinglish in Roman script | mera balance kitna hai
('mixed-script', 0.26) -> match dominant script | mera balance कितना hai?
weak case: ('english-or-other', 0.0) (a lexicon heuristic misses short code-mixed text; use a trained detector and confidence)
 27 bytes, 5 words, 5.4 bytes/word | What is my account balance?
 59 bytes, 5 words, 11.8 bytes/word | मेरा खाता शेष कितना है?
note: byte-level fallback is the WORST case; real tokenizers vary, measure yours on a sample of your own traffic
raw WER: 1.0 | after script normalisation: 0.0
real error (inserted word) WER: 0.25
micro-average 0.819, traffic-weighted 0.834
english   188/200 = 0.94  95% CI 0.90-0.97  -> OK
hindi     172/200 = 0.86  95% CI 0.81-0.90  -> OK
hinglish  70/100 = 0.70  95% CI 0.60-0.78  -> UNDERPOWERED
tamil     36/60 = 0.60  95% CI 0.47-0.71  -> WEAK
bengali   9/20 = 0.45  95% CI 0.26-0.66  -> WEAK
```
Everything here is a toy: a 17-word romanised-Hindi list, a 4-word transliteration map, byte counts instead of tokens, and invented evaluation counts. The point is the shape of the checks (script-aware routing, normalise-before-WER, interval per language), not the numbers.

**Follow-ups:**
- *Do I translate everything to English first?* It simplifies retrieval and the model's reasoning but adds latency, can distort names and numbers, and hides errors from native reviewers; test it against native handling per language.
- *Fine-tune or prompt per language?* Start with prompt and retrieval; fine-tune only for a language where measured quality stays below the floor and you have trustworthy labelled data (Part 4 Q1).
- *How do you get labelled data for Hinglish?* Sample real traffic (with consent and redaction), have native reviewers label, and keep a separate slice for romanised input.

**Common mistakes:**
- One quality number for all languages.
- Scoring ASR with raw WER when script and spelling vary.
- Detecting language per user instead of per message.
- Assuming the safety layer behaves the same in every language.
- Letting translation rewrite numbers, names or legal terms.
- Quoting a vendor's WER for "Hinglish" without the test set.


### Q13 ⭐⭐⭐ 🔴 Code: build a mini-RAG pipeline end to end in plain Python with numpy only and a mocked LLM: chunking with metadata, BM25 plus a toy dense retriever, reciprocal-rank fusion, a simple reranker, prompt assembly with a token budget, a citation checker that rejects claims without a supporting retrieved chunk, abstention on weak retrieval, and a tiny eval (recall@k and citation precision) on a handwritten set. (Part 6 Q14 and Part 7 Q15 build pieces; this question is the integrated, tested pipeline.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
**Say this first (1 line):** A mini-RAG is chunk with metadata, two retrievers fused by RRF, a reranker, a budgeted prompt, a mock model, then a citation checker and an abstain path; the code below is the whole pipeline with tests and an eval, and on a tiny set it retrieves well but over-abstains.

**Then explain:**
- **Chunking with metadata:** sentence windows of two sentences with one overlapping sentence; every chunk keeps `doc`, `pos` and a unique `id` so citations can be checked (Part 6 Q2, Q26).
- **Retrievers:** BM25 (exact words) and a toy dense retriever (hashed character trigrams plus cosine; it only sees spelling overlap, so it is a weak stand-in for a real embedding model). Fusion is reciprocal-rank fusion, which needs no score calibration (Part 7 Q2, Q15).
- **Reranker:** a toy query-term coverage plus bigram score on the fused pool. It stands in for a cross-encoder (Part 7 Q5) and also supplies the abstention score.
- **Prompt assembly:** chunks are added in rank order until the budget is reached; the budget is counted in words, a proxy for tokens.
- **Citation checker:** each answer sentence must cite a chunk that was actually retrieved, and at least half of its content words must appear in that chunk. Otherwise the whole answer is replaced by "I don't know" (Part 6 Q26). This is a lexical check, not entailment; a paraphrased unsupported claim could slip through.
- **Abstention:** if the best reranked chunk has coverage score below 0.5, say so instead of generating (Part 6 Q27).
- **Bug found while testing:** my first sentence splitter did not split after a citation (`[refunds#1] Premium members ...`), so a fabricated sentence rode along with a supported one and was accepted. The test with a deliberately faulty mock model caught it; the splitter now also splits after a closing bracket.

**Example:** Question "How long does express shipping take?" retrieves the shipping chunk (reranker score 0.83), the mock model answers "Express shipping takes 1 to 2 days and costs 9 extra. [shipping#2]", the checker finds the cited chunk among the retrieved ones with full word support, and the answer is returned. Question "Who is the CEO of the company?" retrieves a refunds chunk by accident, but the best reranker score is 0.00, so the system abstains. Question "How many days do I have to ask for a refund?" retrieves the correct document but scores only 0.25: with my tiny stoplist the question has 8 "content" words (how, many, days, do, i, have, ask, refund) and only 2 match, so coverage is 2/8 and the system abstains. That is an over-abstention caused by a crude score, not by missing evidence.

**Code:** (mocked/toy inputs only; run with `python3 -I`)
```python
# Mini-RAG: chunk -> BM25 + toy dense -> RRF -> rerank -> budgeted prompt -> mock LLM -> citation check -> abstain -> eval.
# Corpus, queries and the "LLM" are handwritten toys. Tokens are counted as words (a proxy).
import math, re
import numpy as np
from collections import Counter

DOCS = {
 "refunds": "Refunds are issued to the original payment method within 7 business days. Refund requests after 30 days of purchase are not accepted. Digital gift cards cannot be refunded.",
 "shipping": "Standard shipping takes 4 to 6 days. Express shipping takes 1 to 2 days and costs 9 extra. Orders above 50 ship free with standard shipping.",
 "account": "To reset your password use the forgot password link on the login page. Accounts are locked after 5 failed login attempts. A locked account unlocks after 30 minutes.",
 "warranty": "All laptops carry a 12 month warranty. Accidental damage is not covered by the warranty. Batteries are covered for 6 months.",
 "privacy": "We delete your order history 24 months after your last purchase. You can request a copy of your data from the privacy page.",
}
STOP = set("a an the of to is are in on for your you we by after be can use with and or at not".split())
def toks(t): return [w for w in re.findall(r"[a-z0-9]+", t.lower())]
def cwords(t): return [w for w in toks(t) if w not in STOP]

# ---- chunking with metadata: one chunk per sentence-window of up to 2 sentences, 1 sentence overlap
def chunk(docs, win=2):
    out = []
    for did, text in docs.items():
        sents = [s.strip() for s in re.split(r"(?<=\.)\s+", text) if s.strip()]
        for i in range(0, len(sents), win - 1 if win > 1 else 1):
            piece = " ".join(sents[i:i + win])
            out.append({"id": f"{did}#{len(out)}", "doc": did, "pos": i, "text": piece})
            if i + win >= len(sents): break
    return out
CH = chunk(DOCS)

# ---- BM25
class BM25:
    def __init__(self, texts, k1=1.5, b=0.75):
        self.docs = [cwords(t) for t in texts]; self.k1, self.b = k1, b
        self.avg = sum(map(len, self.docs)) / len(self.docs)
        df = Counter(w for d in self.docs for w in set(d)); N = len(self.docs)
        self.idf = {w: math.log(1 + (N - n + .5) / (n + .5)) for w, n in df.items()}
    def score(self, q):
        qs = cwords(q); out = []
        for d in self.docs:
            tf = Counter(d); s = 0.0
            for w in qs:
                if w in tf:
                    s += self.idf[w] * tf[w] * (self.k1 + 1) / (tf[w] + self.k1 * (1 - self.b + self.b * len(d) / self.avg))
            out.append(s)
        return np.array(out)

# ---- toy dense: hashed character-trigram vectors, cosine (weak on purpose: no semantics, only spelling overlap)
DIM = 256
def emb(t):
    v = np.zeros(DIM); t = " " + " ".join(cwords(t)) + " "
    for i in range(len(t) - 2): v[hash_tri(t[i:i + 3])] += 1
    n = np.linalg.norm(v); return v / n if n else v
def hash_tri(s): return sum((ord(c) * 31 ** i) for i, c in enumerate(s)) % DIM   # deterministic, no PYTHONHASHSEED
M = np.stack([emb(c["text"]) for c in CH])
bm = BM25([c["text"] for c in CH])

def rrf(rank_lists, k=60):
    sc = Counter()
    for rl in rank_lists:
        for r, i in enumerate(rl): sc[i] += 1 / (k + r + 1)
    return [i for i, _ in sc.most_common()]

def rerank(q, idxs):                       # simple reranker: query-term coverage + bigram bonus
    qw = cwords(q); qb = set(zip(qw, qw[1:])); out = []
    for i in idxs:
        cw = cwords(CH[i]["text"]); cov = len(set(qw) & set(cw)) / max(1, len(set(qw)))
        bg = len(qb & set(zip(cw, cw[1:])))
        out.append((cov + 0.5 * bg, i))
    return [i for _, i in sorted(out, key=lambda x: -x[0])], dict((i, s) for s, i in out)

def retrieve(q, k=3, pool=6):
    b = bm.score(q); d = M @ emb(q)
    fused = rrf([list(np.argsort(-b)[:pool]), list(np.argsort(-d)[:pool])])[:pool]
    order, rs = rerank(q, fused)
    return order[:k], rs

def build_prompt(q, idxs, budget=60):      # token budget in words; chunks added in rank order until full
    used, parts = len(q.split()) + 12, []
    for i in idxs:
        n = len(CH[i]["text"].split())
        if used + n > budget: break
        parts.append(f"[{CH[i]['id']}] {CH[i]['text']}"); used += n
    return "Answer only from context, cite ids.\n" + "\n".join(parts) + f"\nQ: {q}", used

# ---- mock LLM: copies the best-matching context sentence and cites it. Mode "faulty" adds an unsupported claim.
def mock_llm(prompt, q, faulty=False):
    ctx = re.findall(r"\[([^\]]+)\] (.+)", prompt)
    best = max(ctx, key=lambda c: len(set(cwords(q)) & set(cwords(c[1]))), default=None)
    if best is None: return "I could not find that."
    sents = re.split(r"(?<=\.)\s+", best[1])
    s = max(sents, key=lambda x: len(set(cwords(q)) & set(cwords(x))))
    ans = f"{s} [{best[0]}]"
    if faulty: ans += " Premium members get double the refund window. [refunds#0]"
    return ans

def check_citations(answer, retrieved_ids, min_support=0.5):
    """Each sentence must cite a RETRIEVED chunk and share >= min_support of its content words with it."""
    bad = []
    for sent in re.split(r"(?<=[.!?\]])\s+(?=[A-Z])", answer):
        cites = re.findall(r"\[([^\]]+)\]", sent)
        body = cwords(re.sub(r"\[[^\]]+\]", "", sent))
        if not cites or not body: bad.append((sent, "no citation")); continue
        ok = False
        for c in cites:
            if c in retrieved_ids:
                chunk_words = set(cwords(next(x["text"] for x in CH if x["id"] == c)))
                if sum(w in chunk_words for w in body) / len(body) >= min_support: ok = True
        if not ok: bad.append((sent, "unsupported"))
    return bad

ABSTAIN_BELOW = 0.5      # rerank coverage score of the best chunk
def answer(q, faulty=False):
    idxs, rs = retrieve(q)
    if rs[idxs[0]] < ABSTAIN_BELOW: return {"abstain": True, "ids": [], "text": "I don't know."}
    prompt, used = build_prompt(q, idxs)
    a = mock_llm(prompt, q, faulty)
    ids = {CH[i]["id"] for i in idxs}
    bad = check_citations(a, ids)
    if bad: return {"abstain": True, "ids": list(ids), "text": "I don't know.", "rejected": bad}
    return {"abstain": False, "ids": [CH[i]["id"] for i in idxs], "text": a, "tokens": used}

# ---- tests
assert all(len(c["text"].split()) > 0 and c["doc"] in DOCS for c in CH)
assert len({c["id"] for c in CH}) == len(CH)
assert abs(rrf([[0, 1], [0, 1]])[0] - 0) < 1e-9 and rrf([[3, 1], [1, 3]])[0] in (1, 3)
_, used = build_prompt("q " * 5, list(range(len(CH))), budget=60); assert used <= 60
assert check_citations("Blah. [x#9]", {"refunds#0"}) and not check_citations("Refunds are issued to the original payment method. [refunds#0]", {"refunds#0"})
r = answer("Are refund requests accepted after 30 days of purchase?", faulty=True)
assert r["abstain"] and r.get("rejected"), r          # unsupported extra claim is rejected
print("unit tests passed")

# ---- tiny eval: (question, gold doc or None if unanswerable)
EVAL = [("How many days do I have to ask for a refund?", "refunds"), ("How long does express shipping take?", "shipping"),
        ("Do orders over 50 ship free?", "shipping"), ("How do I reset my password?", "account"),
        ("How long is a locked account blocked?", "account"), ("Is accidental damage covered under warranty?", "warranty"),
        ("How many months of warranty on batteries?", "warranty"), ("When is my order history deleted?", "privacy"),
        ("Can I return a gift card?", "refunds"), ("Who is the CEO of the company?", None), ("What is the price of the premium plan?", None)]
rec = ans_ok = cite_ok = cite_total = abst_right = 0
n_ans = sum(g is not None for _, g in EVAL)
for q, gold in EVAL:
    idxs, rs = retrieve(q); docs = [CH[i]["doc"] for i in idxs]
    res = answer(q)
    if gold:
        rec += gold in docs
        if not res["abstain"]:
            cite_total += 1
            cited = re.findall(r"\[([^\]]+)\]", res["text"])
            cite_ok += all(c.split("#")[0] == gold for c in cited)
    else:
        abst_right += res["abstain"]
    print(f"{'ANS' if not res['abstain'] else 'ABS'} gold={gold!s:9s} top={docs[0]:9s} score={rs[idxs[0]]:.2f} | {q}")
print(f"recall@3 = {rec}/{n_ans}; citation precision = {cite_ok}/{cite_total}; abstained on unanswerable = {abst_right}/{len(EVAL)-n_ans}; answered {cite_total}/{n_ans} answerable")
```
**Output (my run):**
```text
unit tests passed
ABS gold=refunds   top=refunds   score=0.25 | How many days do I have to ask for a refund?
ANS gold=shipping  top=shipping  score=0.83 | How long does express shipping take?
ANS gold=shipping  top=shipping  score=1.67 | Do orders over 50 ship free?
ABS gold=account   top=account   score=0.33 | How do I reset my password?
ANS gold=account   top=account   score=0.90 | How long is a locked account blocked?
ANS gold=warranty  top=warranty  score=1.80 | Is accidental damage covered under warranty?
ANS gold=warranty  top=warranty  score=1.10 | How many months of warranty on batteries?
ANS gold=privacy   top=privacy   score=0.90 | When is my order history deleted?
ABS gold=refunds   top=refunds   score=0.25 | Can I return a gift card?
ABS gold=None      top=refunds   score=0.00 | Who is the CEO of the company?
ABS gold=None      top=refunds   score=0.00 | What is the price of the premium plan?
recall@3 = 9/9; citation precision = 6/6; abstained on unanswerable = 2/2; answered 6/9 answerable
```
Honest reading of the result: recall@3 is 9 of 9 and citation precision 6 of 6 on answers given, and both unanswerable questions are refused, but only 6 of 9 answerable questions were answered. The abstention rule (a coverage threshold on a toy reranker) is too blunt. On 11 handwritten questions this is a smoke test, not evidence about quality; do not tune the threshold on these 11 and then report them.

**Follow-ups:**
- *Why RRF and not a weighted sum?* BM25 scores and cosines are on different scales; ranks are comparable. A weighted sum needs normalisation and tuning (Part 7 Q15).
- *How would the checker improve?* Use an entailment model or span-level quotes, and verify numbers and named entities separately.
- *How do you fix over-abstention?* Calibrate the threshold on a labelled set with both answerable and unanswerable questions, and look at the precision/recall trade-off (Part 6 Q27).

**Common mistakes:**
- Trusting a citation because the chunk id exists, without checking it supports the sentence.
- Tuning thresholds on the same tiny eval set and reporting the result.
- Reporting only recall@k and never the abstention rate.
- Splitting sentences with a regex that ignores citation markers.
- Letting the prompt overflow the budget silently.


### Q14 ⭐⭐ 🟡 Code: write a tool-calling agent loop with a mocked model: tool registry with schema validation, step, token and wall-clock budgets, loop detection, structured error feedback, a trace of every step, and tests for a runaway loop and a hallucinated tool name. (Part 3 Q11 and Part 8 Q15 are simpler loops; this adds budgets and tracing from Part 8 Q4 and Q38.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
**Say this first (1 line):** The loop is small: ask the model for an action, validate it against a schema, run it, feed errors back as structured observations, and stop on whichever budget (steps, tokens, wall clock) or loop detector fires first, tracing every step.

**Then explain:**
- **Registry and validation:** each tool has a name, a schema and a function. Unknown tool names and bad arguments never reach the function; the model gets an error that lists the real tools or the exact field problem (Part 3 Q11, Part 8 Q13).
- **Budgets:** step count, token count (words here, a proxy) and wall clock, checked before each model call. A fake clock makes the wall-clock test deterministic (Part 8 Q4).
- **Loop detection:** the same (tool, arguments) three times in a row stops the run with a distinct reason. It is checked for hallucinated tool names too; my first version checked only known tools, and a test added for that case now covers it.
- **Trace:** every step records the action, outcome (`ok`, `invalid_args`, `unknown_tool`, `tool_error`, `loop_detected`, `final`), observation and elapsed time, which is what makes a failed run debuggable (Part 8 Q38).
- **What this does not do:** it detects exact repeats only; a model that varies an argument each time (the `varied` test) is stopped only by the step budget. Semantic loop detection (similar states) is harder.

**Example:** The model asks for `get_price` with `qty: "two"`. The validator returns `invalid arguments: 'qty' must be integer`, the scripted model repairs it to `qty: 2`, the tool returns 1500, and the model finalises: trace outcomes `invalid_args, ok, final`. A runaway model calling the same tool with the same arguments stops at step 3 with reason `loop_detected`, even though the step budget was 50.

**Code:** (mocked/toy inputs only; run with `python3 -I`)
```python
# Tool-calling agent loop with budgets, schema validation, loop detection, error feedback and a trace.
# The model is a SCRIPTED mock; time is a fake clock; tokens are counted as words (a proxy).
import json

class FakeClock:
    def __init__(self): self.t = 0.0
    def now(self): return self.t
    def advance(self, s): self.t += s

TYPES = {"string": str, "integer": int, "number": (int, float), "boolean": bool}
def validate(args, schema):
    """Tiny schema check: required keys, no unknown keys, simple types (bool is not an integer)."""
    if not isinstance(args, dict): return "arguments must be an object"
    errs = []
    for k, spec in schema["properties"].items():
        if k in args:
            v, t = args[k], TYPES[spec["type"]]
            if not isinstance(v, t) or (spec["type"] in ("integer", "number") and isinstance(v, bool)):
                errs.append(f"'{k}' must be {spec['type']}")
            elif "enum" in spec and v not in spec["enum"]: errs.append(f"'{k}' must be one of {spec['enum']}")
        elif k in schema.get("required", []): errs.append(f"missing required '{k}'")
    errs += [f"unknown argument '{k}'" for k in args if k not in schema["properties"]]
    return "; ".join(errs) or None

class Agent:
    def __init__(self, model, tools, clock, max_steps=8, max_tokens=400, max_seconds=30.0, loop_window=3):
        self.model, self.tools, self.clock = model, tools, clock
        self.max_steps, self.max_tokens, self.max_seconds, self.loop_window = max_steps, max_tokens, max_seconds, loop_window
    def run(self, goal):
        msgs, trace, tokens, t0, recent = [{"role": "user", "content": goal}], [], 0, self.clock.now(), []
        for step in range(1, self.max_steps + 1):
            if self.clock.now() - t0 > self.max_seconds: return self._end("wall_clock_budget", trace, tokens, step - 1)
            if tokens > self.max_tokens: return self._end("token_budget", trace, tokens, step - 1)
            action = self.model(msgs)                      # {"tool","args"} or {"final"}
            tokens += len(json.dumps(action).split()) + sum(len(str(m["content"]).split()) for m in msgs[-1:])
            rec = {"step": step, "action": action, "t": round(self.clock.now() - t0, 2)}
            if "final" in action:
                rec["outcome"] = "final"; trace.append(rec)
                return {"status": "done", "answer": action["final"], "trace": trace, "tokens": tokens}
            name, args = action.get("tool"), action.get("args", {})
            recent.append((name, json.dumps(args, sort_keys=True, default=str)))
            if len(recent) >= self.loop_window and len(set(recent[-self.loop_window:])) == 1:
                rec["outcome"] = "loop_detected"; trace.append(rec)       # checked for unknown tools too
                return self._end("loop_detected", trace, tokens, step)
            if name not in self.tools:                     # hallucinated tool: tell the model what exists
                obs = {"error": f"unknown tool '{name}'. Available: {sorted(self.tools)}"}; rec["outcome"] = "unknown_tool"
            else:
                tool = self.tools[name]; err = validate(args, tool["schema"])
                if err: obs = {"error": f"invalid arguments: {err}"}; rec["outcome"] = "invalid_args"
                else:
                    try: obs = {"result": tool["fn"](**args)}; rec["outcome"] = "ok"
                    except Exception as e: obs = {"error": f"tool failed: {e}"}; rec["outcome"] = "tool_error"
                self.clock.advance(tool.get("cost_s", 1.0))
            rec["observation"] = obs; trace.append(rec)
            msgs.append({"role": "tool", "content": json.dumps(obs)})
        return self._end("step_budget", trace, tokens, self.max_steps)
    def _end(self, why, trace, tokens, steps):
        return {"status": "stopped", "reason": why, "trace": trace, "tokens": tokens, "steps": steps}

PRICES = {"laptop": 750, "mouse": 20}
TOOLS = {"get_price": {"schema": {"properties": {"item": {"type": "string"}, "qty": {"type": "integer"}}, "required": ["item"]},
                       "fn": lambda item, qty=1: PRICES[item] * qty, "cost_s": 1.0}}

def scripted(actions):
    it = iter(actions)
    return lambda msgs: next(it)

# --- test 1: happy path with one invalid call that the model repairs after the error message
c = FakeClock()
a = Agent(scripted([{"tool": "get_price", "args": {"item": "laptop", "qty": "two"}},
                    {"tool": "get_price", "args": {"item": "laptop", "qty": 2}},
                    {"final": "Two laptops cost 1500."}]), TOOLS, c)
r = a.run("price of 2 laptops?")
assert r["status"] == "done" and [s["outcome"] for s in r["trace"]] == ["invalid_args", "ok", "final"], r
assert "must be integer" in r["trace"][0]["observation"]["error"]

# --- test 2: hallucinated tool name -> error lists real tools, model recovers
a = Agent(scripted([{"tool": "get_cost", "args": {"item": "mouse"}}, {"tool": "get_price", "args": {"item": "mouse"}}, {"final": "20"}]), TOOLS, FakeClock())
r = a.run("mouse price?")
assert r["trace"][0]["outcome"] == "unknown_tool" and "get_price" in r["trace"][0]["observation"]["error"] and r["answer"] == "20"

# --- test 3: runaway loop (same call forever) is stopped by loop detection well before the step budget
a = Agent(lambda msgs: {"tool": "get_price", "args": {"item": "mouse"}}, TOOLS, FakeClock(), max_steps=50)
r = a.run("loop")
assert r["reason"] == "loop_detected" and r["steps"] == 3, r

# --- test 4: varied but endless calls hit the step budget; slow tools hit wall clock; chatty model hits the token budget
n = {"i": 0}
def varied(msgs): n["i"] += 1; return {"tool": "get_price", "args": {"item": "mouse", "qty": n["i"]}}
assert Agent(varied, TOOLS, FakeClock(), max_steps=5).run("x")["reason"] == "step_budget"
slow = dict(TOOLS); slow["get_price"] = dict(TOOLS["get_price"], cost_s=20.0)
n["i"] = 0; assert Agent(varied, slow, FakeClock(), max_steps=50, max_seconds=30).run("x")["reason"] == "wall_clock_budget"
n["i"] = 0; assert Agent(varied, TOOLS, FakeClock(), max_steps=50, max_tokens=40).run("x")["reason"] == "token_budget"

# --- test 5: tool exception becomes structured feedback, not a crash
t2 = {"get_price": dict(TOOLS["get_price"])}
a = Agent(scripted([{"tool": "get_price", "args": {"item": "desk"}}, {"final": "no such item"}]), t2, FakeClock())
r = a.run("desk?"); assert r["trace"][0]["outcome"] == "tool_error" and "desk" in r["trace"][0]["observation"]["error"]
# --- test 6: repeating a hallucinated tool name is also caught as a loop
assert Agent(lambda m: {"tool": "nope", "args": {}}, TOOLS, FakeClock(), max_steps=50).run("x")["reason"] == "loop_detected"
print("all 6 test groups passed")
print("--- trace of the runaway-loop run:")
a = Agent(lambda msgs: {"tool": "get_price", "args": {"item": "mouse"}}, TOOLS, FakeClock(), max_steps=50)
for s in a.run("loop")["trace"]: print(s["step"], s["outcome"], s["action"], s.get("observation"), "t=", s["t"])
print("--- trace of the hallucinated-tool run:")
a = Agent(scripted([{"tool": "get_cost", "args": {"item": "mouse"}}, {"tool": "get_price", "args": {"item": "mouse"}}, {"final": "20"}]), TOOLS, FakeClock())
res = a.run("mouse price?")
for s in res["trace"]: print(s["step"], s["outcome"], s.get("observation", s["action"]))
print("tokens (word proxy):", res["tokens"])
```
**Output (my run):**
```text
all 6 test groups passed
--- trace of the runaway-loop run:
1 ok {'tool': 'get_price', 'args': {'item': 'mouse'}} {'result': 20} t= 0.0
2 ok {'tool': 'get_price', 'args': {'item': 'mouse'}} {'result': 20} t= 1.0
3 loop_detected {'tool': 'get_price', 'args': {'item': 'mouse'}} None t= 2.0
--- trace of the hallucinated-tool run:
1 unknown_tool {'error': "unknown tool 'get_cost'. Available: ['get_price']"}
2 ok {'result': 20}
3 final {'final': '20'}
tokens (word proxy): 22
```
All six test groups assert on trace outcomes and stop reasons, not just on "did not crash". The scripted model is deterministic, so a real model would also need probabilistic tests over many runs.

**Follow-ups:**
- *Why feed errors back instead of raising?* The model can fix a bad argument or tool name in one more step; raising ends a run that was recoverable (Part 8 Q13).
- *What should happen when a budget ends the run?* Return the partial trace and a clear status, and escalate or summarise what was done; never claim success (Part 8 Q4).
- *Where do approvals go?* Before side-effecting tools, as a gate in the executor (Part 8 Q24).

**Common mistakes:**
- Only a step cap, with no wall-clock or token cap.
- Detecting loops on the model's text rather than on the (tool, arguments) pair.
- Raising on invalid arguments instead of returning a structured error.
- Returning a stack trace to the model.
- Keeping no trace, so a stopped run cannot be diagnosed.


### Q15 ⭐⭐ 🟡 Code: build a text-to-SQL harness against an in-memory sqlite3 database with a mocked generator: schema-to-prompt, SQL validation (single SELECT only, parsed table and column allowlist, LIMIT injection, timeout), a repair retry using the error message, and an execution-accuracy evaluator that compares result sets rather than SQL strings.
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
**Say this first (1 line):** Treat generated SQL as untrusted input: let sqlite itself enforce a table and column allowlist through its authorizer, allow only one SELECT, wrap it in a LIMIT, kill it with a progress-handler timeout, retry once with the error message, and score by comparing result rows, not SQL text.

**Then explain:**
- **Schema to prompt:** list only the allowed tables and columns (the sensitive `ssn` column is simply absent from the prompt and from the allowlist) (Part 7 Q40).
- **Validation, in layers:** (1) static checks after stripping string literals: one statement, no comments, must start with SELECT or WITH; (2) sqlite's authorizer callback sees every table and column the parser resolves, including through aliases, subqueries and `SELECT *`, so a regex-based column check is not needed; (3) wrap the query as `SELECT * FROM (...) LIMIT n`; (4) a progress handler aborts a query after a fixed number of VM steps. In the tests, `SELECT *` is rejected because it would read `ssn`, recursive CTEs are denied by default (authorizer action code 33), and a ten-way self-join (about 5^10 row combinations) is interrupted.
- **Defence in depth:** in production also use a read-only database connection or role with only the needed grants; a validator is not the only line (Part 11 Q9 for the broader trust model).
- **Repair retry:** on failure, send the error text back once (here: `no such column: o.total`), then give up. Unbounded repair loops waste money and can drift.
- **Execution accuracy:** compare result sets as multisets of rounded rows (order only matters if the gold query has ORDER BY). String match marks a correct rewrite wrong and can mark a wrong query right. Execution accuracy still has blind spots: two different queries can agree on a small database by accident, so test on more than one database state.
- **Benchmarks:** BIRD and Spider are the standard public benchmarks; BIRD has 12,751 question-SQL pairs over 95 databases and Spider 10,181 questions over 200 databases (dataset sizes from the papers). I quote no leaderboard accuracies; they are dated and not comparable across systems.

**Example:** Question "revenue by city". Attempt 1 from the mock generator sums `o.total`, which does not exist: error `no such column: o.total`. Attempt 2 (given the error) sums `o.amount` and returns Delhi 200.0 and Pune 320.0. Against a gold query, a rewritten query with different aliases is counted correct (same rows), a query that adds `WHERE status = 'paid'` is counted wrong (different rows), and a query that also selects `ssn` is rejected before it runs.

**Code:** (mocked/toy inputs only; run with `python3 -I`)
```python
# Text-to-SQL harness on in-memory sqlite3 with a MOCK generator. Validation uses sqlite's own authorizer
# (it sees every table and column the parser resolves), a progress handler for the timeout, and LIMIT wrapping.
import re, sqlite3
from collections import Counter

def make_db():
    db = sqlite3.connect(":memory:")
    db.executescript("""
    CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT, city TEXT, ssn TEXT);
    CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, status TEXT);
    INSERT INTO customers VALUES (1,'Asha','Pune','111'),(2,'Ben','Delhi','222'),(3,'Chitra','Pune','333');
    INSERT INTO orders VALUES (1,1,120.0,'paid'),(2,1,80.0,'refunded'),(3,2,200.0,'paid'),(4,3,50.0,'paid'),(5,3,70.0,'paid');
    """)
    return db

ALLOW = {"customers": {"id", "name", "city"}, "orders": {"id", "customer_id", "amount", "status"}}   # ssn is NOT allowed

def schema_prompt(question):
    ddl = "\n".join(f"{t}({', '.join(sorted(c))})" for t, c in ALLOW.items())
    return f"Schema:\n{ddl}\nWrite ONE read-only SELECT. Question: {question}"

class Rejected(Exception): pass

def strip_literals(sql): return re.sub(r"'(?:[^']|'')*'", "''", sql)
def static_checks(sql):
    s = strip_literals(sql).strip()
    if s.endswith(";"): s = s[:-1]
    if ";" in s: raise Rejected("only one statement allowed")
    if "--" in s or "/*" in s: raise Rejected("comments not allowed")
    if not re.match(r"(?is)^\s*(select|with)\b", s): raise Rejected("only SELECT allowed")
    return sql.strip().rstrip(";")

def run_query(db, sql, limit=100, max_ops=200_000):
    sql = static_checks(sql)
    def auth(action, a1, a2, dbname, src):
        if action == sqlite3.SQLITE_SELECT or action == sqlite3.SQLITE_FUNCTION: return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_READ:
            if a1 in ALLOW and (a2 in ALLOW[a1] or a2 == ""): return sqlite3.SQLITE_OK
            raise_msg.append(f"column or table not allowed: {a1}.{a2}"); return sqlite3.SQLITE_DENY
        raise_msg.append(f"operation not allowed (code {action})"); return sqlite3.SQLITE_DENY
    raise_msg, ops = [], {"n": 0}
    def progress(): ops["n"] += 1; return 1 if ops["n"] > max_ops // 1000 else 0   # called every 1000 VM steps
    db.set_authorizer(auth); db.set_progress_handler(progress, 1000)
    try:
        cur = db.execute(f"SELECT * FROM ({sql}) LIMIT {int(limit)}")        # LIMIT injection by wrapping
        return cur.fetchall()
    except sqlite3.Error as e:
        msg = raise_msg[-1] if raise_msg else str(e)
        raise Rejected(msg) from None
    finally:
        db.set_authorizer(None); db.set_progress_handler(None, 0)

def answer_with_repair(db, question, generator, max_attempts=2):
    feedback, log = None, []
    for attempt in range(1, max_attempts + 1):
        sql = generator(schema_prompt(question), feedback)
        try:
            rows = run_query(db, sql); log.append((attempt, sql, "ok")); return rows, log
        except Rejected as e:
            feedback = str(e); log.append((attempt, sql, f"error: {e}"))
    return None, log

def exec_accuracy(db, pred_sql, gold_sql):
    """Compare result SETS (multiset of rows, rounded), not SQL strings. Order matters only if gold has ORDER BY."""
    def norm(rows): return [tuple(round(x, 6) if isinstance(x, float) else x for x in r) for r in rows]
    try: p = norm(run_query(db, pred_sql, limit=10_000))
    except Rejected: return False
    g = norm(db.execute(gold_sql).fetchall())
    return p == g if re.search(r"(?i)order\s+by", gold_sql) else Counter(p) == Counter(g)

db = make_db()
# ---- validator tests
def rejected(sql):
    try: run_query(db, sql); return None
    except Rejected as e: return str(e)
assert rejected("DROP TABLE orders") == "only SELECT allowed"
assert rejected("SELECT 1; DELETE FROM orders") == "only one statement allowed"
assert "not allowed" in rejected("SELECT ssn FROM customers")
assert "not allowed" in rejected("SELECT * FROM customers")            # * expands to ssn -> denied
assert "not allowed" in rejected("SELECT name FROM sqlite_master")
assert "no such" in rejected("SELECT nme FROM customers")
assert rejected("WITH x AS (SELECT id FROM customers) SELECT id FROM x") is None        # a CTE is fine
assert len(run_query(db, "SELECT id FROM orders", limit=2)) == 2        # LIMIT injected
assert rejected("WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c) SELECT x FROM c") == "operation not allowed (code 33)"   # recursive CTEs denied by default (SQLITE_RECURSIVE)
rows = run_query(db, "SELECT name FROM customers WHERE name = 'a; b'")   # semicolon inside a literal is fine
assert rows == []
big = rejected("SELECT count(*) FROM orders a, orders b, orders c, orders d, orders e, orders f, orders g, orders h, orders i, orders j")
# 5^10 ~ 9.7M row combinations: must be cut off by the timeout hook
assert big == "interrupted", big
print("validator tests passed; runaway join stopped with:", big)

# ---- repair retry: first attempt uses a wrong column, second uses the error text
def gen(prompt, feedback):
    if feedback is None: return "SELECT c.city, SUM(o.total) FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.city"
    assert "no such column" in feedback
    return "SELECT c.city, SUM(o.amount) FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.city"
rows, log = answer_with_repair(db, "revenue by city", gen)
for l in log: print(l)
print("rows:", sorted(rows))

# ---- execution accuracy: different SQL string, same rows -> correct; similar-looking SQL, different rows -> wrong
gold = "SELECT city, SUM(amount) FROM customers JOIN orders ON orders.customer_id = customers.id GROUP BY city"
variants = {
 "same rows, other text": "SELECT c.city AS c, SUM(o.amount) AS s FROM orders o JOIN customers c ON c.id = o.customer_id GROUP BY c.city",
 "extra status filter": "SELECT city, SUM(amount) FROM customers JOIN orders ON orders.customer_id = customers.id WHERE status = 'paid' GROUP BY city",
 "touches ssn": "SELECT city, SUM(amount), ssn FROM customers JOIN orders ON orders.customer_id = customers.id GROUP BY city",
}
for k, v in variants.items(): print(f"{k:24s} exec-correct = {exec_accuracy(db, v, gold)}")
assert exec_accuracy(db, variants["same rows, other text"], gold) and not exec_accuracy(db, variants["extra status filter"], gold)
# row-order: ORDER BY in gold makes order matter
assert exec_accuracy(db, "SELECT id FROM orders ORDER BY id", "SELECT id FROM orders ORDER BY id")
assert not exec_accuracy(db, "SELECT id FROM orders ORDER BY id DESC", "SELECT id FROM orders ORDER BY id")
print("evaluator tests passed")
```
**Output (my run):**
```text
validator tests passed; runaway join stopped with: interrupted
(1, 'SELECT c.city, SUM(o.total) FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.city', 'error: no such column: o.total')
(2, 'SELECT c.city, SUM(o.amount) FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.city', 'ok')
rows: [('Delhi', 200.0), ('Pune', 320.0)]
same rows, other text    exec-correct = True
extra status filter      exec-correct = False
touches ssn              exec-correct = False
evaluator tests passed
```
Uses sqlite 3.45.1 on my machine; authorizer action codes are sqlite constants, so the text of denied-operation messages can differ by version. The timeout is a step budget, not wall-clock seconds.

**Follow-ups:**
- *Why not just block keywords like DROP?* Keyword lists are bypassable and block legitimate column names; the authorizer and a read-only connection enforce the rule at the engine.
- *Why LIMIT by wrapping?* Appending LIMIT breaks on queries that already end in LIMIT or a UNION; wrapping is uniform.
- *How would you handle a large schema?* Retrieve the relevant tables and columns first and put only those in the prompt (Part 7 Q40).

**Common mistakes:**
- Executing generated SQL on a writable connection.
- Checking only the first word of the statement.
- Comparing SQL strings.
- Evaluating on one tiny database state.
- Unbounded repair loops.
- Putting sensitive columns in the schema prompt and then filtering the output.


### Q16 ⭐⭐ 🟡 Code: implement a semantic cache for LLM answers with a toy embedding: similarity threshold, tenant and model in the cache key, TTL, exclusion of personalised or time-sensitive queries, and a false-hit audit that measures wrong-answer rate on paraphrase and near-miss pairs. Why are published threshold values not transferable? (Part 10 Q28 covers caching strategy; Part 11 Q26 covers isolation.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
**Say this first (1 line):** A semantic cache returns a stored answer when a new question is similar enough, so the whole risk is the threshold: in my toy runs no threshold separates paraphrases from near-misses cleanly, and the threshold that works for one embedding is wrong for another, which is why published values do not transfer.

**Then explain:**
- **Key and scope first, similarity second:** the cache is looked up only among entries with the same tenant and model (and, in production, the same permission scope and prompt version); similarity never crosses those lines (Part 11 Q26).
- **TTL:** entries expire; the test uses a fake clock. Time-sensitive answers get a short TTL or are excluded.
- **Exclusions:** personalised ("my balance") and time-sensitive ("today", "latest") queries are neither stored nor served. A regex is a crude filter; a classifier or an explicit per-intent policy is better.
- **False-hit audit:** build pairs that are paraphrases (should hit) and near-misses (differ in a plan name, a number, a negation, a city; must not hit). Sweep thresholds and report both rates. Near-misses are the dangerous class: a wrong cached answer is served confidently and cheaply.
- **Why thresholds do not transfer:** the useful value depends on the embedding model, normalisation, domain, query length and how many near-misses your traffic has. Two toy embeddings on the same 16 pairs need very different thresholds, and published values (the sources I saw conflict, and I did not verify them) cannot be reused without your own audit (Part 10 Q28 covers strategy).
- **Cheap guards help:** requiring numbers and negation words to match exactly before accepting a hit removes some failure classes (the UPI 5000 versus 50000 pair), but not entity swaps like gold versus silver.

**Example:** Eight paraphrase pairs and eight near-miss pairs (handwritten, synthetic). With embedding B (content-word bag) at threshold 0.9: paraphrase hits 0.12, false hits 0.00. At 0.7: hits 0.75, false hits 0.50. With embedding A (character trigrams) the near-miss "5000 versus 50000" pair scores 0.99 similarity, so zero false hits needs threshold 0.99, where it serves no paraphrase at all. Adding the number/negation guard to B at 0.8 gives hits 0.50, false hits 0.00 on this set.

**Code:** (mocked/toy inputs only; run with `python3 -I`)
```python
# Semantic cache with two TOY embeddings, tenant+model keys, TTL (fake clock), exclusions and a false-hit audit.
# Pairs are handwritten SYNTHETIC examples. No real embedding model: thresholds found here say nothing about yours.
import re
import numpy as np

STOP = set("a an the is are what how do i can you of to for in on my me please".split())
def words(t): return re.findall(r"[a-z0-9]+", t.lower())
def h(s, dim): return sum(ord(c) * (31 ** i) for i, c in enumerate(s)) % dim
def emb_char(t, dim=512):                       # embedding A: character trigrams of the full text
    v = np.zeros(dim); s = " " + " ".join(words(t)) + " "
    for i in range(len(s) - 2): v[h(s[i:i + 3], dim)] += 1
    return v / (np.linalg.norm(v) or 1)
def emb_word(t, dim=512):                       # embedding B: content-word bag (stopwords removed)
    v = np.zeros(dim)
    for w in words(t):
        if w not in STOP: v[h(w, dim)] += 1
    return v / (np.linalg.norm(v) or 1)

PERSONAL = re.compile(r"\b(my|mine|me|i)\b|\b(today|now|tonight|latest|current|yesterday)\b", re.I)
def cacheable(q): return not PERSONAL.search(q)

class Clock:
    def __init__(self): self.t = 0
class SemanticCache:
    def __init__(self, embed, threshold, ttl, clock):
        self.embed, self.th, self.ttl, self.clock, self.items = embed, threshold, ttl, clock, []
    def put(self, tenant, model, q, ans):
        if cacheable(q): self.items.append((tenant, model, self.embed(q), ans, self.clock.t, q))
    def get(self, tenant, model, q):
        if not cacheable(q): return None
        qv, best, bs = self.embed(q), None, -1
        for (tn, md, v, ans, t0, q0) in self.items:
            if tn != tenant or md != model or self.clock.t - t0 > self.ttl: continue    # key + TTL filter BEFORE similarity
            s = float(v @ qv)
            if s > bs: best, bs = (ans, q0), s
        return best if best is not None and bs >= self.th else None

# ---- unit tests: isolation, TTL, exclusions
ck = Clock(); c = SemanticCache(emb_word, 0.9, ttl=100, clock=ck)
c.put("bankA", "m1", "What is the refund window for gold plan", "30 days")
assert c.get("bankA", "m1", "What is the refund window for gold plan")[0] == "30 days"
assert c.get("bankB", "m1", "What is the refund window for gold plan") is None      # other tenant
assert c.get("bankA", "m2", "What is the refund window for gold plan") is None      # other model
ck.t = 101; assert c.get("bankA", "m1", "What is the refund window for gold plan") is None   # expired
c.put("bankA", "m1", "What is my balance", "100"); assert len(c.items) == 1          # personal query not stored
assert c.get("bankA", "m1", "what is the weather today") is None
print("unit tests passed")

# ---- false-hit audit on handwritten pairs
PARA = [("How do I reset my password", "I forgot my password, how can I reset it"), ("What is the refund window for the gold plan", "How long is the gold plan refund window"),
        ("Where can I download the invoice", "How do I download my invoice"), ("What is the shipping time for express orders", "How long does express shipping take"),
        ("Can I change the delivery address", "How can I change my delivery address"), ("Is there a fee for international transfers", "Do international transfers have a fee"),
        ("How do I close my account", "What are the steps to close an account"), ("What documents are needed for KYC", "Which documents do I need for KYC")]
NEAR = [("What is the refund window for the gold plan", "What is the refund window for the silver plan"), ("Is there a fee for international transfers", "Is there no fee for international transfers"),
        ("How long does express shipping take", "How long does standard shipping take"), ("Can I change the delivery address", "Can I change the billing address"),
        ("What is the limit for UPI payments of 5000", "What is the limit for UPI payments of 50000"), ("How do I open a savings account", "How do I close a savings account"),
        ("What documents are needed for KYC", "What documents are needed for KYB"), ("Is the offer valid in Pune", "Is the offer valid in Delhi")]
def audit(embed, th):
    hit_para = sum(float(embed(a) @ embed(b)) >= th for a, b in PARA) / len(PARA)
    false_hit = sum(float(embed(a) @ embed(b)) >= th for a, b in NEAR) / len(NEAR)
    return hit_para, false_hit
print("threshold | A(char-trigram): paraphrase hits / near-miss false hits | B(word-bag): same")
for th in (0.5, 0.6, 0.7, 0.8, 0.9, 0.95):
    a, b = audit(emb_char, th), audit(emb_word, th)
    print(f"  {th:.2f}   |  {a[0]:.2f} / {a[1]:.2f}  |  {b[0]:.2f} / {b[1]:.2f}")
print("near-miss similarities (A):", [round(float(emb_char(a) @ emb_char(b)), 2) for a, b in NEAR])
print("near-miss similarities (B):", [round(float(emb_word(a) @ emb_word(b)), 2) for a, b in NEAR])
print("paraphrase similarities (A):", [round(float(emb_char(a) @ emb_char(b)), 2) for a, b in PARA])
print("paraphrase similarities (B):", [round(float(emb_word(a) @ emb_word(b)), 2) for a, b in PARA])
for name, e in (("A", emb_char), ("B", emb_word)):
    ok = [th / 100 for th in range(30, 100) if audit(e, th / 100)[1] == 0]
    best = min(ok) if ok else None
    print(f"{name}: lowest threshold with zero false hits = {best}; paraphrase hit rate there = {audit(e, best)[0] if best else 'n/a'}")

# ---- cheap guard: numbers and negations must match exactly before a similarity hit is accepted
def guard_ok(a, b):
    f = lambda t: ({w for w in words(t) if w.isdigit()}, {w for w in words(t) if w in ("no", "not", "never", "without")})
    return f(a) == f(b)
assert guard_ok("limit 5000", "limit 5000") and not guard_ok("limit 5000", "limit 50000") and not guard_ok("is a fee", "is no fee")
for th in (0.7, 0.8):
    g_hit = sum(float(emb_word(a) @ emb_word(b)) >= th and guard_ok(a, b) for a, b in PARA) / len(PARA)
    g_false = sum(float(emb_word(a) @ emb_word(b)) >= th and guard_ok(a, b) for a, b in NEAR) / len(NEAR)
    print(f"B + guard at {th}: paraphrase hits {g_hit:.2f}, near-miss false hits {g_false:.2f}")
```
**Output (my run):**
```text
unit tests passed
threshold | A(char-trigram): paraphrase hits / near-miss false hits | B(word-bag): same
  0.50   |  0.75 / 1.00  |  0.88 / 1.00
  0.60   |  0.75 / 1.00  |  0.75 / 1.00
  0.70   |  0.50 / 1.00  |  0.75 / 0.50
  0.80   |  0.12 / 0.62  |  0.50 / 0.12
  0.90   |  0.00 / 0.38  |  0.12 / 0.00
  0.95   |  0.00 / 0.12  |  0.12 / 0.00
near-miss similarities (A): [0.86, 0.94, 0.78, 0.73, 0.99, 0.83, 0.94, 0.79]
near-miss similarities (B): [0.75, 0.89, 0.8, 0.67, 0.75, 0.67, 0.67, 0.67]
paraphrase similarities (A): [0.7, 0.74, 0.61, 0.45, 0.81, 0.75, 0.4, 0.69]
paraphrase similarities (B): [0.71, 0.89, 0.82, 0.45, 1.0, 0.75, 0.82, 0.58]
A: lowest threshold with zero false hits = 0.99; paraphrase hit rate there = 0.0
B: lowest threshold with zero false hits = 0.9; paraphrase hit rate there = 0.125
B + guard at 0.7: paraphrase hits 0.75, near-miss false hits 0.25
B + guard at 0.8: paraphrase hits 0.50, near-miss false hits 0.00
```
Only 8 and 8 pairs, so each pair is 12.5 points: the sweep shows shape, not a rate you can use. A cache that is safe on this data has a low hit rate, which is the honest trade-off; its value depends on how many near-miss questions your real traffic contains.

**Follow-ups:**
- *Should cache hits skip the safety layer?* Cached answers were already checked, but re-check if policies changed; version the key by prompt and policy version.
- *Exact-match cache first?* Yes: it is free of false hits and often catches repeated FAQs (Part 10 Q28).
- *How do you monitor it live?* Sample hits, have a judge or human compare the cached answer against a fresh one, and track the false-hit rate (Part 9 Q30).

**Common mistakes:**
- Copying a threshold from a blog or paper.
- Auditing only paraphrases, not near-misses.
- Leaving tenant, model or prompt version out of the key.
- Caching personalised or time-sensitive answers.
- Reporting hit rate without false-hit rate.


### Q17 ⭐⭐ 🟡 Code: write a streaming response generator (SSE-style framing) over a mocked token stream with cancellation when the client disconnects, a server-side timeout, backpressure through a bounded queue, a final usage event, and tests that a cancelled request stops consuming tokens. (Part 10 Q19 explains the path.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
**Say this first (1 line):** Put a bounded queue between the model and the socket so a slow client slows the producer, cancel the producer the moment sending fails or a timeout fires, and always finish with a usage or error event; then test that the model's token counter stops rising after a cancel.

**Then explain:**
- **SSE framing:** each event is `event: name`, `data: json`, a blank line. Token events carry text; the last event is `usage` (or `error` then `usage` on timeout). The path is explained in Part 10 Q19.
- **Backpressure:** the producer does `await queue.put(token)` on a bounded queue. When the client is slow the queue fills and the producer waits, so generation cannot run far ahead of delivery.
- **Cancellation:** a failed write (the stand-in for a disconnect) raises in the consumer; a `finally` block cancels the producer task. The test samples the model's `generated` counter twice, 50 ms apart, and asserts it did not move.
- **Timeout:** `asyncio.wait_for` around the pump. On timeout the client gets an `error` event, then `usage`; the producer is cancelled.
- **Usage accounting:** the final usage event reports tokens actually sent. In the disconnect case there is no client to receive it, so a real server logs usage server-side for billing; this sketch does not.
- **Limit of the sketch:** a real mock stream cancels at the next `await`; a real engine must also be told to abort the request, otherwise the GPU keeps decoding (the cost is the point of the test).

**Example:** A 200-token generation with the client dropping after 5 tokens: in my run the model had generated 6 tokens when it stopped (5 delivered plus one in flight), against 200 requested. With a 50 ms-per-token slow client and a queue of 4, after 50 ms the client had 4 tokens and the model had generated 10, not 50. A 1000-token job with a 50 ms server timeout produced the frames `error`, `usage` and the model had generated 9 tokens.

**Code:** (mocked/toy inputs only; run with `python3 -I`)
```python
# SSE-style streaming over a MOCK token stream: bounded queue (backpressure), client-disconnect cancellation,
# server-side timeout, final usage event. Delays are tiny so the tests run in well under a second.
import asyncio, json

def sse(event, data): return f"event: {event}\ndata: {json.dumps(data)}\n\n"

class MockModel:
    """Counts every token it is asked to generate, so tests can see whether work continued after cancel."""
    def __init__(self, n_tokens=200, delay=0.001): self.n, self.delay, self.generated = n_tokens, delay, 0
    async def stream(self):
        for i in range(self.n):
            await asyncio.sleep(self.delay)
            self.generated += 1
            yield f"tok{i} "

async def producer(model, q, prompt_tokens):
    try:
        async for tok in model.stream():
            await q.put(tok)                    # blocks when the queue is full = backpressure
        await q.put(None)                       # end marker
    except asyncio.CancelledError:
        raise

async def handle(model, send, timeout=1.0, queue_size=4, prompt_tokens=12, disconnect_after=None, slow_client=0.0):
    """send(frame) writes to the client; it raises ConnectionResetError if the client is gone."""
    q = asyncio.Queue(maxsize=queue_size)
    prod = asyncio.create_task(producer(model, q, prompt_tokens))
    sent = 0
    async def pump():
        nonlocal sent
        while True:
            tok = await q.get()
            if tok is None: return "complete"
            if slow_client: await asyncio.sleep(slow_client)
            await send(sse("token", {"text": tok})); sent += 1
    try:
        status = await asyncio.wait_for(pump(), timeout)
    except asyncio.TimeoutError:
        status = "timeout"; await _safe(send, sse("error", {"reason": "server timeout"}))
    except ConnectionResetError:
        status = "client_disconnected"
    finally:
        prod.cancel()                           # stop pulling tokens from the model no matter how we ended
        try: await prod
        except asyncio.CancelledError: pass
    if status != "client_disconnected":
        await _safe(send, sse("usage", {"prompt_tokens": prompt_tokens, "completion_tokens": sent, "status": status}))
    return status, sent

async def _safe(send, frame):
    try: await send(frame)
    except ConnectionResetError: pass

class Client:
    def __init__(self, drop_after=None): self.frames, self.drop_after = [], drop_after
    async def send(self, frame):
        if self.drop_after is not None and len([f for f in self.frames if f.startswith("event: token")]) >= self.drop_after:
            raise ConnectionResetError
        self.frames.append(frame)

async def main():
    # 1. normal completion: all tokens, then a usage event last
    m = MockModel(n_tokens=20); c = Client()
    status, sent = await handle(m, c.send)
    assert status == "complete" and sent == 20 and c.frames[-1].startswith("event: usage")
    assert json.loads(c.frames[-1].split("data: ")[1])["completion_tokens"] == 20
    print("1 complete:", status, "| tokens sent", sent, "| last frame:", c.frames[-1].split("\n")[0], "|", repr(c.frames[0]))

    # 2. client disconnects after 5 tokens: model must stop (generated stays tiny vs 200)
    m = MockModel(n_tokens=200); c = Client(drop_after=5)
    status, sent = await handle(m, c.send)
    await asyncio.sleep(0.05); g = m.generated
    await asyncio.sleep(0.05); assert m.generated == g, "generation continued after cancel"
    assert status == "client_disconnected" and g <= 5 + 4 + 2, g          # sent + queue size + in-flight
    print("2 disconnect:", status, "| sent", sent, "| model generated", g, "of 200 (bound: sent + queue 4 + 2 in flight)")

    # 3. backpressure: slow client, fast model -> model stays within queue_size of the client
    m = MockModel(n_tokens=50, delay=0.0); c = Client()
    task = asyncio.create_task(handle(m, c.send, queue_size=4, slow_client=0.01, timeout=5))
    await asyncio.sleep(0.05)
    sent_now = len([f for f in c.frames if f.startswith("event: token")])
    assert m.generated <= sent_now + 4 + 2, (m.generated, sent_now)
    print("3 backpressure at 50 ms: client got", sent_now, "tokens, model generated", m.generated, "(not 50)")
    task.cancel()
    try: await task
    except asyncio.CancelledError: pass

    # 4. server timeout: error event, then usage event with status timeout; model stopped
    m = MockModel(n_tokens=1000, delay=0.005); c = Client()
    status, sent = await handle(m, c.send, timeout=0.05)
    g = m.generated; await asyncio.sleep(0.05); assert m.generated == g
    kinds = [f.split("\n")[0] for f in c.frames if not f.startswith("event: token")]
    assert status == "timeout" and kinds == ["event: error", "event: usage"], kinds
    print("4 timeout:", status, "| non-token frames:", kinds, "| model generated", g, "of 1000")
asyncio.run(main())
print("all streaming tests passed")
```
**Output (my run):**
```text
1 complete: complete | tokens sent 20 | last frame: event: usage | 'event: token\ndata: {"text": "tok0 "}\n\n'
2 disconnect: client_disconnected | sent 5 | model generated 6 of 200 (bound: sent + queue 4 + 2 in flight)
3 backpressure at 50 ms: client got 4 tokens, model generated 10 (not 50)
4 timeout: timeout | non-token frames: ['event: error', 'event: usage'] | model generated 9 of 1000
all streaming tests passed
```
Timings are machine dependent, so the assertions use bounds (sent plus queue size plus in-flight), not exact counts; the exact numbers above will differ between runs and machines (they were identical across three runs here).

**Follow-ups:**
- *What about proxies buffering SSE?* Disable response buffering and send periodic comment lines as keep-alives (from memory, check your proxy documentation).
- *Why a final usage event?* Clients and gateways need token counts for budgets (Part 11 Q16).
- *How is it different from WebSockets?* SSE is one-way over HTTP and reconnects simply; WebSockets are two-way and heavier.

**Common mistakes:**
- An unbounded queue (backpressure disappears and memory grows).
- Cancelling the HTTP handler but not the model request.
- No timeout, so a stuck upstream pins a worker.
- Forgetting the terminal event, so the client cannot tell completion from a dropped connection.
- Asserting on exact timings in tests.


### Q18 ⭐⭐ 🟡 Code: implement a conversation memory manager with a token budget: keep the system prompt and recent turns, summarise older turns through a mocked summariser, pin facts the user stated, drop stale tool outputs first, and test that the prompt never exceeds the budget and that pinned facts survive. (Part 8 Q8 and Part 6 Q28 are the concepts.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
**Say this first (1 line):** Build the prompt from a priority list: system prompt, pinned user facts and the newest turn are fixed, then add recent turns newest-first until the budget is full, drop stale tool output before anything else, and summarise what was dropped only if room remains; then prove the budget holds with a property test.

**Then explain:**
- **Priority order:** system prompt, pinned facts (capped at 40 per cent of the budget so they cannot crowd out the user's latest message), latest turn (truncated as a last resort), recent turns newest first, then a short summary of dropped dialogue (Part 8 Q8, Part 6 Q28).
- **Pinning:** facts the user states ("my name is ...", "my budget is ...", "I am allergic to ...") are extracted by a toy regex and kept verbatim, because summaries lose exact numbers. A real system would use a model plus user confirmation.
- **Stale tool outputs first:** tool results older than two turns are dropped before dialogue is, since they are large and rarely needed again.
- **Mock summariser:** keeps the first words of each dropped turn. It shows the plumbing, not the quality of a real summary; a real one can drop or distort facts, hence the pins.
- **Tests:** a directed test checks the exact prompt; a property test runs 300 random conversations with random budgets (25 to 90 words) and asserts the budget is never exceeded and the pinned name is always present.
- **Honest limit:** with a tiny budget, pins are dropped (oldest first) so the latest message still fits; protecting the pins completely is impossible when they do not fit.

**Example:** Budget 60 words. A chat contains a 40-word stale tool result, a stated name, budget and allergy, and a final question. The prompt comes out at 55 words: system line, one "User facts" line holding all three facts, the recent turns, and the newest message; the tool output is gone. With a budget of 40 and long filler turns, older turns collapse to "Earlier: turn0 filler filler" within 38 words. With a budget of 14 words, both pins are dropped and the latest message ("what next") is kept.

**Code:** (mocked/toy inputs only; run with `python3 -I`)
```python
# Conversation memory manager with a token budget. Tokens = words (a PROXY); the summariser is a MOCK.
import random, re

def ntok(s): return len(s.split())
PIN_PATTERNS = [r"\bmy name is [A-Z]\w+", r"\bi am allergic to \w+", r"\bmy budget is \d+", r"\bi live in [A-Z]\w+", r"\bplease always [\w ]+"]
def extract_pins(text):
    return [m.group(0) for p in PIN_PATTERNS for m in re.finditer(p, text, re.I)]

def mock_summarise(turns, max_words):
    """Mock summariser: keeps the first few words of each older turn. A real one would be an LLM call."""
    out = " ; ".join(" ".join(t["content"].split()[:4]) for t in turns)
    return " ".join(out.split()[:max_words])

class Memory:
    def __init__(self, system, budget, summary_cap=25, tool_stale_after=2, pin_share=0.4):
        self.system, self.budget, self.summary_cap, self.tool_stale_after, self.pin_share = system, budget, summary_cap, tool_stale_after, pin_share
        self.turns, self.pins, self.summary = [], [], ""
    def add(self, role, content):
        self.turns.append({"role": role, "content": content})
        if role == "user":
            for p in extract_pins(content):
                if p.lower() not in [x.lower() for x in self.pins]: self.pins.append(p)
    def prompt(self):
        """Return (messages, tokens). Priority: system > pins > last turn > recent turns > summary > nothing."""
        fixed = [{"role": "system", "content": self.system}]
        sys_tokens = ntok(self.system)
        pin_room = max(0, int(self.budget * self.pin_share) - 3)         # pins may use at most pin_share of the budget
        kept_pins, p_used = [], 0
        for p in reversed(self.pins):                                     # newest pin first
            if p_used + ntok(p) <= pin_room and sys_tokens + 3 + p_used + ntok(p) <= self.budget: kept_pins.insert(0, p); p_used += ntok(p)
        self.last_pins_dropped = len(self.pins) - len(kept_pins)
        if kept_pins: fixed.append({"role": "system", "content": "User facts: " + "; ".join(kept_pins)})
        used = sum(ntok(m["content"]) for m in fixed)
        last = self.turns[-1] if self.turns else None
        last_content = last["content"] if last else ""
        room_for_last = self.budget - used
        if last and ntok(last_content) > room_for_last:                    # even the newest turn must fit: truncate it
            last = {"role": last["role"], "content": " ".join(last_content.split()[:max(0, room_for_last)])}
        used += ntok(last["content"]) if last else 0
        # older turns, newest first; stale tool outputs are dropped before anything else
        n = len(self.turns)
        older = list(enumerate(self.turns[:-1]))
        def stale_tool(i, t): return t["role"] == "tool" and (n - 1 - i) > self.tool_stale_after
        keep, dropped = [], []
        for i, t in reversed(older):
            if stale_tool(i, t): dropped.append((i, t)); continue
            if used + ntok(t["content"]) <= self.budget: keep.append((i, t)); used += ntok(t["content"])
            else: dropped.append((i, t))
        keep.sort(key=lambda x: x[0])
        msgs = list(fixed)
        gone = sorted(dropped, key=lambda x: x[0])
        if any(t["role"] != "tool" for _, t in gone):                      # summarise dropped dialogue (not tool output), if room remains
            room = min(self.summary_cap, self.budget - used - 3)
            if room > 0:
                s = "Earlier: " + mock_summarise([t for _, t in gone if t["role"] != "tool"], room)
                s = " ".join(s.split()[:room + 1]); msgs.append({"role": "system", "content": s}); used += ntok(s)
        msgs += [t for _, t in keep]
        if last: msgs.append(last)
        return msgs, sum(ntok(m["content"]) for m in msgs)

# ---- directed tests
m = Memory("You are a travel assistant.", budget=60)
m.add("user", "Hi my name is Ravi and my budget is 40000 for the trip")
m.add("assistant", "Great, where would you like to go?")
m.add("tool", " ".join(["flightdata"] * 40))
m.add("user", "Goa in December please")
m.add("assistant", "Searching.")
m.add("user", "Also I am allergic to peanuts so avoid those restaurants")
msgs, used = m.prompt()
assert used <= 60 and msgs[0]["role"] == "system" and msgs[-1]["content"].startswith("Also I am allergic")
facts = msgs[1]["content"]; assert "my name is Ravi" in facts and "my budget is 40000" in facts and "allergic to peanuts" in facts
assert not any("flightdata" in x["content"] for x in msgs)             # stale tool output dropped first
print("directed test passed; tokens used:", used, "of 60")
print("prompt:"); [print("  ", x["role"], "|", x["content"]) for x in msgs]

# ---- summary path: older dialogue that no longer fits is replaced by a short mock summary
m2 = Memory("You are a travel assistant.", budget=40)
for i in range(6): m2.add("user" if i % 2 == 0 else "assistant", f"turn{i} " + "filler " * 7)
m2.add("user", "my name is Ravi, so what now")
msgs2, used2 = m2.prompt()
assert used2 <= 40 and any(x["content"].startswith("Earlier:") for x in msgs2)
print("summary test passed; tokens", used2, "of 40; summary =", [x["content"] for x in msgs2 if x["content"].startswith("Earlier:")][0])

# ---- randomised property test: 300 random conversations, budget always respected, pins always survive
rng = random.Random(3)
WORDS = "alpha beta gamma delta flight hotel train visa price date seat meal city".split()
violations = pin_lost = 0
for trial in range(300):
    budget = rng.randint(25, 90)
    mem = Memory("You are a helpful assistant.", budget=budget)
    pins_added = False
    for k in range(rng.randint(2, 25)):
        role = rng.choice(["user", "assistant", "tool"]) if k else "user"
        text = " ".join(rng.choice(WORDS) for _ in range(rng.randint(1, 40)))
        if role == "user" and rng.random() < 0.15: text = "my name is Meera " + text; pins_added = True
        mem.add(role, text)
        msgs, used = mem.prompt()
        if used > budget: violations += 1
        if pins_added and not any("my name is Meera" in x["content"] for x in msgs): pin_lost += 1
print(f"300 random conversations: budget violations = {violations}, pinned fact missing = {pin_lost}")
assert violations == 0 and pin_lost == 0

# ---- honest limit: pins can crowd out everything else when the budget is tiny
tiny = Memory("You are a bot.", budget=14)
tiny.add("user", "my name is Ravi and my budget is 40000"); tiny.add("assistant", "ok noted"); tiny.add("user", "what next")
msgs, used = tiny.prompt()
print("tiny budget ->", used, "tokens; kept:", [x["content"] for x in msgs], "| pins dropped:", tiny.last_pins_dropped)
assert used <= 14 and msgs[-1]["content"] == "what next"
```
**Output (my run):**
```text
directed test passed; tokens used: 55 of 60
prompt:
   system | You are a travel assistant.
   system | User facts: my name is Ravi; my budget is 40000; I am allergic to peanuts
   user | Hi my name is Ravi and my budget is 40000 for the trip
   assistant | Great, where would you like to go?
   user | Goa in December please
   assistant | Searching.
   user | Also I am allergic to peanuts so avoid those restaurants
summary test passed; tokens 38 of 40; summary = Earlier: turn0 filler filler
300 random conversations: budget violations = 0, pinned fact missing = 0
tiny budget -> 12 tokens; kept: ['You are a bot.', 'Earlier: my name is', 'ok noted', 'what next'] | pins dropped: 2
```
Tokens are whitespace words; a real tokenizer will count differently, so a real budget needs the model's tokenizer and a safety margin.

**Follow-ups:**
- *Why not summarise everything?* Summaries are lossy and cost an extra call; keep exact facts pinned and recent turns verbatim.
- *Where does long-term memory fit?* Pins can graduate to a store with deduplication and expiry (Part 8 Q21, Q22).
- *What about cache friendliness?* Changing the summary every turn breaks prompt caching; keep stable content first (Part 10 Q14).

**Common mistakes:**
- Counting characters instead of tokens, or ignoring the system prompt in the budget.
- Dropping the user's latest message to keep history.
- Summarising away exact numbers and names.
- Never testing the edge case where pins alone exceed the budget.
- Letting tool outputs accumulate.


### Q19 ⭐⭐ 🟡 Code: implement a router and cascade with a mocked small and large model: a cheap difficulty heuristic or confidence score, escalation on low confidence or failed validation, cost and latency accounting per request, and an offline evaluation that reports the quality-cost frontier against always-large. Name when the router itself costs more than it saves. (Part 10 Q28 is the strategy.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
**Say this first (1 line):** A cascade tries the cheap model first and escalates on low confidence or a failed validation; the honest evaluation is a quality-cost curve against always-large on the same queries, and a router only pays when the saving per request beats its own cost.

**Then explain:**
- **Two designs:** a router decides before any call (difficulty heuristic or classifier); a cascade runs the small model and escalates after seeing its confidence and a validator result (Part 10 Q28). A cascade pays for the small call even when it escalates.
- **Accounting:** cost per request includes the small call, the large call when escalated, and the router call if it is a model. Latency adds the same way for a cascade.
- **Offline evaluation:** run every policy on the same labelled queries, report quality, cost and latency for each, mark the Pareto frontier, and bootstrap the quality gap to always-large over queries (paired).
- **When the router costs more than it saves:** per request, saving is (fraction sent small) times (large cost minus small cost); if that is below the router's own cost, it loses. This happens when the large model is only a few times dearer than the small one, when most traffic needs the large model anyway, or when the router is itself a model call.
- **Risks:** a confidence score from a small model is noisy and often miscalibrated; check calibration on your own data. Quality losses concentrate on hard queries, which may be the valuable ones, so slice results by difficulty.
- **Savings claims:** published routing papers report large savings, but those are the authors' claims on their benchmarks; this answer uses only its own synthetic run.

**Example:** All inputs are ASSUMED and synthetic: 4,000 queries with a latent difficulty, a small model that degrades fast, a large one that degrades slowly, costs of 1 (small) and 15 (large) units. Always-large: quality 0.866 at cost 15.00. Cascade escalating when confidence is below 0.6 or validation fails: quality 0.821 at 9.16 (0.61 times the large cost). With the threshold at 0.75: quality 0.848 at 12.24, and the paired bootstrap says it is 0.018 below always-large (interval -0.025 to -0.011). Setting B (large only 3 times small, router costing 0.8 per request) makes route d_hat>0.3 cost 3.05 against 3.00 for always-large: the router loses.

**Code:** (mocked/toy inputs only; run with `python3 -I`)
```python
# Router + cascade over MOCK small/large models on SYNTHETIC queries. Every probability and cost below is ASSUMED.
import numpy as np
rng = np.random.default_rng(11)
N = 4000
d = rng.beta(2, 3, N)                                         # latent difficulty in [0,1], SYNTHETIC
p_small = np.clip(0.97 - 0.90 * d, 0.05, 0.97)                # ASSUMED: small model gets worse fast with difficulty
p_large = np.clip(0.99 - 0.30 * d, 0.05, 0.99)                # ASSUMED: large model degrades slowly
small_ok = rng.random(N) < p_small
large_ok = rng.random(N) < p_large
conf = np.clip(p_small + rng.normal(0, 0.15, N), 0, 1)        # small model's self-reported confidence (noisy)
d_hat = d + rng.normal(0, 0.25, N)                            # cheap heuristic difficulty feature (noisy)
val_fail = np.where(small_ok, rng.random(N) < 0.02, rng.random(N) < 0.35)   # validator: flags 35% of wrong, 2% of right

def evaluate(policy, c_small, c_large, l_small, l_large, c_router=0.0):
    quality = cost = lat = 0.0
    esc = 0
    for i in range(N):
        go_large, first_small = policy(i)
        if first_small:
            cost += c_small; lat += l_small
            if go_large: cost += c_large; lat += l_large; esc += 1; quality += large_ok[i]
            else: quality += small_ok[i]
        else:
            cost += c_large; lat += l_large; esc += 1; quality += large_ok[i]
        cost += c_router
    return quality / N, cost / N, lat / N, esc / N

pol_small = lambda i: (False, True)
pol_large = lambda i: (True, False)
def pol_route(t): return lambda i: (True, False) if d_hat[i] > t else (False, True)   # (go_large, small_first)
def pol_cascade(t): return lambda i: (bool(conf[i] < t or val_fail[i]), True)

def table(c_small, c_large, l_small, l_large, c_router, label):
    print(f"== {label}: ASSUMED cost small={c_small}, large={c_large}, router call={c_router}; latency small={l_small}s, large={l_large}s")
    base = evaluate(pol_large, c_small, c_large, l_small, l_large)
    rows = [("always-large", base), ("always-small", evaluate(pol_small, c_small, c_large, l_small, l_large))]
    for t in (0.3, 0.4, 0.5):
        rows.append((f"route d_hat>{t}", evaluate(pol_route(t), c_small, c_large, l_small, l_large, c_router)))
    for t in (0.6, 0.75, 0.9):
        rows.append((f"cascade conf<{t}|fail", evaluate(pol_cascade(t), c_small, c_large, l_small, l_large)))
    for name, (q, c, l, e) in rows:
        print(f"  {name:22s} quality {q:.3f}  cost {c:6.2f} ({c / base[1]:.2f}x of large)  latency {l:.2f}s  escalated {e:.2f}")
    return rows

rows = table(1.0, 15.0, 0.4, 2.0, 0.0, "setting A (large is 15x small, router is plain code)")
# frontier: keep points not dominated (another point with >= quality and <= cost, one strictly)
pts = [(n, float(q), float(c)) for n, (q, c, l, e) in rows]
front = [p for p in pts if not any((o[1] >= p[1] and o[2] <= p[2]) and (o[1] > p[1] or o[2] < p[2]) for o in pts)]
print("  frontier:", [(n, round(q, 3), round(c, 2)) for n, q, c in sorted(front, key=lambda x: x[2])])

rows_b = table(1.0, 3.0, 0.4, 1.0, 0.8, "setting B (large only 3x small, router is a model call costing 0.8)")

# paired bootstrap: quality gap between the cascade (conf<0.75|fail) and always-large on the SAME queries
casc_ok = np.array([large_ok[i] if (conf[i] < 0.75 or val_fail[i]) else small_ok[i] for i in range(N)])
diff = casc_ok.astype(float) - large_ok.astype(float)
bs = [diff[rng.integers(0, N, N)].mean() for _ in range(1000)]
print(f"cascade minus always-large quality: {diff.mean():+.3f}, bootstrap 95% interval {np.percentile(bs, 2.5):+.3f} to {np.percentile(bs, 97.5):+.3f}")

# break-even for a model-based router: saves only if (fraction sent small) * (c_large - c_small) > router cost
for frac_small in (0.3, 0.5):
    for c_large, c_small in ((15, 1), (3, 1)):
        print(f"fraction sent small {frac_small}: saving per request {frac_small * (c_large - c_small):.2f} vs router cost 0.8 -> {'router pays' if frac_small * (c_large - c_small) > 0.8 else 'router LOSES'}")
# tests
assert evaluate(pol_large, 1, 15, .4, 2)[3] == 1.0 and evaluate(pol_small, 1, 15, .4, 2)[3] == 0.0
q_all_esc = evaluate(pol_cascade(1.1), 1, 15, .4, 2); assert abs(q_all_esc[0] - large_ok.mean()) < 1e-12 and q_all_esc[3] == 1.0
print("tests passed")
```
**Output (my run):**
```text
== setting A (large is 15x small, router is plain code): ASSUMED cost small=1.0, large=15.0, router call=0.0; latency small=0.4s, large=2.0s
  always-large           quality 0.866  cost  15.00 (1.00x of large)  latency 2.00s  escalated 1.00
  always-small           quality 0.613  cost   1.00 (0.07x of large)  latency 0.40s  escalated 0.00
  route d_hat>0.3        quality 0.807  cost   9.76 (0.65x of large)  latency 1.40s  escalated 0.63
  route d_hat>0.4        quality 0.779  cost   8.05 (0.54x of large)  latency 1.21s  escalated 0.50
  route d_hat>0.5        quality 0.749  cost   6.38 (0.43x of large)  latency 1.02s  escalated 0.38
  cascade conf<0.6|fail  quality 0.821  cost   9.16 (0.61x of large)  latency 1.49s  escalated 0.54
  cascade conf<0.75|fail quality 0.848  cost  12.24 (0.82x of large)  latency 1.90s  escalated 0.75
  cascade conf<0.9|fail  quality 0.862  cost  14.63 (0.98x of large)  latency 2.22s  escalated 0.91
  frontier: [('always-small', 0.613, 1.0), ('route d_hat>0.5', 0.749, 6.38), ('route d_hat>0.4', 0.779, 8.05), ('cascade conf<0.6|fail', 0.821, 9.16), ('cascade conf<0.75|fail', 0.848, 12.24), ('cascade conf<0.9|fail', 0.862, 14.63), ('always-large', 0.866, 15.0)]
== setting B (large only 3x small, router is a model call costing 0.8): ASSUMED cost small=1.0, large=3.0, router call=0.8; latency small=0.4s, large=1.0s
  always-large           quality 0.866  cost   3.00 (1.00x of large)  latency 1.00s  escalated 1.00
  always-small           quality 0.613  cost   1.00 (0.33x of large)  latency 0.40s  escalated 0.00
  route d_hat>0.3        quality 0.807  cost   3.05 (1.02x of large)  latency 0.78s  escalated 0.63
  route d_hat>0.4        quality 0.779  cost   2.81 (0.94x of large)  latency 0.70s  escalated 0.50
  route d_hat>0.5        quality 0.749  cost   2.57 (0.86x of large)  latency 0.63s  escalated 0.38
  cascade conf<0.6|fail  quality 0.821  cost   2.63 (0.88x of large)  latency 0.94s  escalated 0.54
  cascade conf<0.75|fail quality 0.848  cost   3.25 (1.08x of large)  latency 1.15s  escalated 0.75
  cascade conf<0.9|fail  quality 0.862  cost   3.73 (1.24x of large)  latency 1.31s  escalated 0.91
cascade minus always-large quality: -0.018, bootstrap 95% interval -0.025 to -0.011
fraction sent small 0.3: saving per request 4.20 vs router cost 0.8 -> router pays
fraction sent small 0.3: saving per request 0.60 vs router cost 0.8 -> router LOSES
fraction sent small 0.5: saving per request 7.00 vs router cost 0.8 -> router pays
fraction sent small 0.5: saving per request 1.00 vs router cost 0.8 -> router pays
tests passed
```
Everything is synthetic, so the frontier shows the method, not what a real system will achieve. The bootstrap resamples queries only; it does not include randomness in the model outputs.

**Follow-ups:**
- *How do you choose the threshold?* Pick the cost you can afford or the quality you must hold, read it off the frontier, then validate on a fresh slice.
- *What about latency?* Escalated requests pay both calls; if the p95 matters, route before calling.
- *How do you monitor in production?* Sample escalated and non-escalated answers for quality and watch the escalation rate; drift moves it (Part 11 Q2).

**Common mistakes:**
- Reporting average quality only, hiding the hard-query slice.
- Forgetting the small call's cost on escalated requests.
- Using the small model's raw confidence without a calibration check.
- Evaluating on queries used to set the threshold.
- Building a model-based router when prices differ by 2 to 3 times.


### Q20 ⭐⭐ 🟡 Code: write an LLM-call harness with per-call timeout, retry with exponential backoff and jitter on retryable errors only, retry-after handling, an idempotency key, a circuit breaker with half-open probing, and a fallback model, tested with a fault-injecting fake client. (Part 11 Q15 is the concept.)
**Asked at:** coding or take-home style rounds at product companies and startups (expert gap-check; no candidate report found)
**Say this first (1 line):** Retry only errors that can succeed on retry, wait with exponential backoff and full jitter but never less than Retry-After, send one idempotency key for the logical request, trip a circuit breaker after repeated failures, and fall back to a second model.

**Then explain:**
- **Retryable vs not:** timeouts, 429 and 5xx are retryable; a bad request (our own bug) fails fast with no retry and no fallback (Part 11 Q15).
- **Backoff with full jitter:** wait a random time between 0 and min(cap, base times 2^(attempt-1)); jitter prevents synchronised retry storms. The test checks waits never exceed the cap and are spread out.
- **Retry-After:** when the server says when to retry, that value is a floor on the wait.
- **Idempotency key:** one key per logical request, reused on every attempt, so a server that supports it can deduplicate a retry of a request that actually succeeded. The fake client here records keys but does not dedupe; whether a provider supports it must be checked in its documentation.
- **Circuit breaker:** closed until 3 consecutive failures, then open (skip the model with no call) for a cooldown, then half-open: one probe; success closes it, one failure reopens it.
- **Fallback model:** when the primary's breaker opens or its attempts run out, go to the fallback; if everything fails, raise a clear error with bounded total calls.
- **What the sketch leaves out:** the timeout is passed to the client (which must enforce it), there is no overall deadline across attempts, and retrying after a timeout may duplicate side effects for non-idempotent tools.

**Example:** Primary returns 500, 500, then succeeds: three calls, one idempotency key, waits of 0.398 s and 0.942 s (random, seeded). A 429 with Retry-After 7: the wait is exactly 7.0 s. Primary times out three times: the breaker opens after the third failure and the fallback answers; the next request skips the primary with no call, and after a 31 s cooldown a single probe closes the breaker.

**Code:** (mocked/toy inputs only; run with `python3 -I`)
```python
# LLM-call harness: timeout, backoff+jitter on retryable errors only, retry-after, idempotency key,
# circuit breaker with half-open probe, fallback model. Fake clock + fault-injecting fake client; nothing is real.
import random, uuid

class Retryable(Exception):
    def __init__(self, msg, retry_after=None): super().__init__(msg); self.retry_after = retry_after
class RateLimited(Retryable): pass
class ServerError(Retryable): pass
class CallTimeout(Retryable): pass
class BadRequest(Exception): pass                          # NOT retryable (our bug; retrying cannot fix it)

class Clock:
    def __init__(self): self.t = 0.0; self.sleeps = []
    def now(self): return self.t
    def sleep(self, s): self.sleeps.append(round(s, 3)); self.t += s

class Breaker:
    def __init__(self, clock, fail_threshold=3, cooldown=30.0): self.c, self.th, self.cd = clock, fail_threshold, cooldown; self.state, self.fails, self.opened = "closed", 0, 0.0
    def allow(self):
        if self.state == "open" and self.c.now() - self.opened >= self.cd: self.state = "half_open"; return True     # one probe
        return self.state != "open"
    def ok(self): self.state, self.fails = "closed", 0
    def fail(self):
        self.fails += 1
        if self.state == "half_open" or self.fails >= self.th: self.state, self.opened = "open", self.c.now()

class Harness:
    def __init__(self, client, clock, rng, max_attempts=4, base=0.5, cap=8.0, timeout=5.0, models=("primary", "fallback")):
        self.client, self.clock, self.rng, self.max_attempts, self.base, self.cap, self.timeout, self.models = client, clock, rng, max_attempts, base, cap, timeout, models
        self.breakers = {m: Breaker(clock) for m in models}
        self.log = []
    def call(self, prompt):
        key = str(uuid.UUID(int=self.rng.getrandbits(128)))          # ONE idempotency key for the whole logical request
        for model in self.models:
            br = self.breakers[model]
            for attempt in range(1, self.max_attempts + 1):
                if not br.allow(): self.log.append((model, attempt, "breaker_open")); break
                try:
                    out = self.client.complete(model, prompt, key, self.timeout)
                    br.ok(); self.log.append((model, attempt, "ok")); return {"model": model, "text": out, "key": key}
                except BadRequest: self.log.append((model, attempt, "bad_request")); raise          # fail fast, no retry, no fallback
                except Retryable as e:
                    br.fail(); self.log.append((model, attempt, type(e).__name__))
                    if attempt == self.max_attempts or br.state == "open": break
                    backoff = self.rng.uniform(0, min(self.cap, self.base * 2 ** (attempt - 1)))    # full jitter
                    wait = max(backoff, e.retry_after or 0)                                          # never retry before Retry-After
                    self.clock.sleep(wait)
        raise RuntimeError("all models failed")

class FakeClient:
    """Fault injector: per-model script of outcomes; records every call with its key and timeout."""
    def __init__(self, script): self.script, self.calls = {m: list(v) for m, v in script.items()}, []
    def complete(self, model, prompt, key, timeout):
        self.calls.append((model, key, timeout))
        outcome = self.script.setdefault(model, []).pop(0) if self.script.get(model) else "ok"
        if isinstance(outcome, Exception): raise outcome
        return f"[{model}] answer"

def run(script, **kw):
    clock, client = Clock(), FakeClient(script)
    h = Harness(client, clock, random.Random(5), **kw)
    return h, client, clock

# 1. retries then success; same idempotency key on every attempt; waits never exceed the backoff cap
h, cl, ck = run({"primary": [ServerError("500"), ServerError("503")]})
r = h.call("hi"); assert r["model"] == "primary" and len(cl.calls) == 3 and len({k for _, k, _ in cl.calls}) == 1
assert all(w <= 8.0 for w in ck.sleeps)
print("1 retries:", h.log, "| sleeps", ck.sleeps)

# 2. Retry-After is honoured as a floor
h, cl, ck = run({"primary": [RateLimited("429", retry_after=7.0)]})
h.call("hi"); assert ck.sleeps[0] >= 7.0
print("2 retry-after:", ck.sleeps)

# 3. non-retryable error fails fast: one call, no fallback
h, cl, ck = run({"primary": [BadRequest("schema")]})
try: h.call("hi"); assert False
except BadRequest: pass
assert len(cl.calls) == 1 and ck.sleeps == []
print("3 bad request:", h.log)

# 4. primary keeps failing -> breaker opens after 3 failures -> fallback answers
h, cl, ck = run({"primary": [CallTimeout("t")] * 10})
r = h.call("hi"); assert r["model"] == "fallback" and h.breakers["primary"].state == "open"
n_primary = sum(m == "primary" for m, _, _ in cl.calls); assert n_primary == 3
print("4 fallback:", h.log, "| primary calls", n_primary)

# 5. while open, the primary is skipped with no calls; after cooldown ONE half-open probe; success closes it
before = len(cl.calls); r = h.call("again")
assert r["model"] == "fallback" and not any(m == "primary" for m, _, _ in cl.calls[before:])
ck.t += 31                                                    # cooldown passes
cl.script["primary"] = []                                     # primary has recovered
r = h.call("probe"); assert r["model"] == "primary" and h.breakers["primary"].state == "closed"
print("5 breaker: skipped while open, probe after cooldown ->", r["model"], h.breakers["primary"].state)

# 6. failed probe re-opens immediately (a single failure in half-open)
h2, cl2, ck2 = run({"primary": [ServerError("x")] * 3 + [ServerError("probe fails")]})
h2.call("a"); ck2.t += 31; cl2.script["primary"] = [ServerError("probe fails")]
h2.call("b"); assert h2.breakers["primary"].state == "open"
print("6 failed probe reopens breaker:", h2.log[-3:])

# 7. everything down -> clear error, bounded attempts
h3, cl3, ck3 = run({"primary": [ServerError("x")] * 20, "fallback": [ServerError("y")] * 20})
try: h3.call("x"); assert False
except RuntimeError as e: print("7 all down:", e, "| total calls", len(cl3.calls))
assert len(cl3.calls) <= 8

# 8. jitter: across 200 harness runs the first wait takes many distinct values within [0, base]
firsts = []
for s in range(200):
    clock, client = Clock(), FakeClient({"primary": [ServerError("x")]})
    Harness(client, clock, random.Random(s)).call("q"); firsts.append(clock.sleeps[0])
assert max(firsts) <= 0.5 and len(set(firsts)) > 150
print(f"8 jitter: first wait min {min(firsts):.3f} max {max(firsts):.3f} over 200 runs")
print("all harness tests passed")
```
**Output (my run):**
```text
1 retries: [('primary', 1, 'ServerError'), ('primary', 2, 'ServerError'), ('primary', 3, 'ok')] | sleeps [0.398, 0.942]
2 retry-after: [7.0]
3 bad request: [('primary', 1, 'bad_request')]
4 fallback: [('primary', 1, 'CallTimeout'), ('primary', 2, 'CallTimeout'), ('primary', 3, 'CallTimeout'), ('fallback', 1, 'ok')] | primary calls 3
5 breaker: skipped while open, probe after cooldown -> primary closed
6 failed probe reopens breaker: [('fallback', 1, 'ok'), ('primary', 1, 'ServerError'), ('fallback', 1, 'ok')]
7 all down: all models failed | total calls 6
8 jitter: first wait min 0.001 max 0.499 over 200 runs
all harness tests passed
```
Fake clock and seeded random make the tests deterministic; real timing, real clocks and concurrent requests (several probes at once in half-open) need their own tests.

**Follow-ups:**
- *Why jitter?* Without it, many clients retry at the same instants and re-overload the server.
- *Should the fallback be a weaker model?* Often yes; log which model answered and watch quality on fallback traffic (Part 11 Q6).
- *What about streaming calls?* Retry only before the first token is delivered; after that, retrying changes what the user already saw.

**Common mistakes:**
- Retrying everything, including 400 errors.
- Fixed-interval retries and no cap.
- New idempotency key on each attempt.
- Breaker with no half-open state, so it never recovers.
- No overall deadline, so retries outlast the user's patience.

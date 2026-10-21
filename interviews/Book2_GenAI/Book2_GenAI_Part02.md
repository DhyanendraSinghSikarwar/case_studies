# Book 2 — Part 02: Tokenization, Pretraining, Scaling Laws and Decoding

**Topic:** subword tokenizers (BPE, WordPiece, Unigram, byte-level), token economics, pretraining objective, data pipeline, optimisation recipe and precision, scaling laws and compute estimates, and decoding strategies (greedy, sampling, beam, penalties, determinism, logprobs, test-time compute).
**Target:** 40  |  **Actual:** 44 (⭐⭐⭐ 13, ⭐⭐ 21, ⭐ 10)  |  **Date:** 2026-10-21  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 already covers input embeddings, unembedding and the vocabulary's effect on model size (Q25), BERT vs GPT objectives (Q16), training-stability tricks (Q44) and multi-token prediction (Q45). Here those are cross-referenced, not repeated. Overlaps with Book 1 are intentional but deeper here: subword tokenization (B1P09-Q27: here the merge algorithm, byte-level and design trade-offs), LM perplexity (B1P09-Q18: here bits-per-byte and cross-tokenizer comparison), beam search (B1P09-Q44: here cost and length normalisation), LR schedules, loss curves and mixed precision (B1P08-Q14/Q16/Q40: here LLM-pretraining specifics), benchmark contamination (B1P01-Q34: here decontamination of a corpus), and calibration from logprobs (B1P03-Q44: here logprob mechanics). Answers must cross-reference, not copy. Constrained/structured decoding belongs to Part 3, fine-tuning to Part 4, RLHF/DPO to Part 5, and speculative decoding, PagedAttention and serving to Part 10. Generic distributed-training and MLOps detail belongs to Book 4.

---

### Q1 ⭐⭐⭐ 🟢 Why do LLMs use subword tokenization instead of words or characters? Compare BPE, WordPiece and Unigram/SentencePiece.
**Asked at:** all types; service-company, GCC and product GenAI loops
**Say this first (1 line):** Words give a huge vocabulary and break on unseen words; characters give tiny vocabularies but very long sequences. Subwords sit in the middle: frequent words stay whole, rare words split into reusable pieces, so nothing is out-of-vocabulary and sequences stay short.

**Then explain:**
- **Word-level:** vocabulary of hundreds of thousands, "lowest" or a typo becomes `<UNK>`, and every inflection ("run", "runs", "running") is an unrelated row in the embedding table.
- **Character-level:** no OOV, but a sentence becomes 4-5x more tokens. Attention cost grows with the square of length, and each position carries little meaning.
- **Subword:** a vocabulary of roughly 30k-250k pieces (a design choice, see Q14). Common words are one token, rare ones are a few. Byte-level versions can encode any string (see Q15).
- **BPE:** start from characters (or bytes), repeatedly merge the most frequent adjacent pair. Encoding replays the merges in order. Used by GPT-style and Llama-style models.
- **WordPiece:** also builds by merging, but picks the pair that most improves training-data likelihood (not raw count). Encoding is greedy longest-match, with `##` continuation pieces. BERT uses it.
- **Unigram (SentencePiece):** goes the other way. Start with a big candidate vocabulary and prune pieces that hurt corpus likelihood least. It gives a probabilistic segmentation, so you can sample several splits (subword regularisation). SentencePiece is a library that works on raw text, treats space as a symbol, and needs no pre-tokenizer, which suits languages without spaces. It can train BPE or Unigram.
- Basics are in B1P09-Q27. Here the point is the mechanism and the trade-offs.

**Example:** My toy BPE below trained on 17 words (10 merges). "lowest" was never in the corpus, yet it encodes as `low` + `est</w>`. A word-level vocabulary would give `<UNK>`.

**Code:** (run, plain Python, toy corpus; real tokenizers train on billions of words)
```python
from collections import Counter
corpus = "low low low low low lower lower newest newest newest newest newest newest widest widest widest".split()
def merge_seq(s, pair):
    out, i = [], 0
    while i < len(s):
        if i < len(s)-1 and (s[i], s[i+1]) == pair: out.append(s[i]+s[i+1]); i += 2
        else: out.append(s[i]); i += 1
    return out
def train_bpe(words, n_merges):
    seqs = Counter(tuple(w) + ("</w>",) for w in words); merges = []
    for _ in range(n_merges):
        pairs = Counter()
        for s, c in seqs.items():
            for a, b in zip(s, s[1:]): pairs[(a, b)] += c
        best = max(pairs, key=lambda p: (pairs[p], p))      # deterministic tie-break
        merges.append(best)
        seqs = Counter({tuple(merge_seq(list(s), best)): c for s, c in seqs.items()})
    return merges
def encode(word, merges):
    s = list(word) + ["</w>"]
    for m in merges: s = merge_seq(s, m)
    return s
merges = train_bpe(corpus, 10)
for w in ["newest", "lowest", "widest", "slowest"]: print(w, encode(w, merges))
```
Output from my run: `newest ['newest</w>']`, `lowest ['low', 'est</w>']`, `widest ['wi', 'd', 'est</w>']`, `slowest ['s', 'low', 'est</w>']`. (The `merge_seq` refactor is the same logic as my first run, which printed the same splits.)

**Follow-ups:**
- *Why not just use bytes (vocabulary 256)?* Very long sequences. Byte-level BPE keeps the no-OOV guarantee and still merges frequent bytes (see Q15).
- *Does a bigger vocabulary always help?* No. It shortens sequences but enlarges embedding and softmax layers, and rare tokens get under-trained (Q14, Part 1 Q25).
- *BPE vs Unigram in practice?* Both work well. Unigram's advantage is multiple valid segmentations; BPE's is simplicity and deterministic encoding.

**Common mistakes:** saying WordPiece and BPE are identical (the merge criterion differs); thinking SentencePiece is a separate algorithm rather than a library; claiming subwords remove all problems (numbers, spelling and non-English still suffer, see Q5, Q6, Q17); thinking tokens are words or syllables.

### Q2 ⭐⭐⭐ 🟢 Greedy decoding vs sampling vs beam search: how does each choose the next token, and when would you use which?
**Asked at:** all types
**Say this first (1 line):** Greedy takes the single most likely token each step, sampling draws a token from the probability distribution, and beam search keeps the k best partial sequences and returns the highest-scoring full one.

**Then explain:**
- **Greedy** (argmax, same as temperature 0): fast and deterministic in principle, but short-sighted. A locally best token can lead to a poor sequence, and it tends to loop and repeat.
- **Sampling:** randomness gives variety and more natural text. Pure sampling can pick junk from the long tail, so in practice it is combined with temperature, top-k or top-p (Q4).
- **Beam search:** tracks k candidates by cumulative log-probability. It finds higher-probability sequences than greedy, but costs about k times the compute and memory, has no randomness, and often yields dull, repetitive text for open-ended generation. Scores need length normalisation or short outputs win (a sum of negative log-probs favours short sequences). Deeper treatment in B1P09-Q44.
- **When:** extraction, classification, code, SQL, tool-call JSON: greedy or low temperature. Chat and creative writing: sampling with top-p. Translation, summarisation, ASR (one right answer, fixed-length-ish output): beam search is classic. Most modern chat APIs expose sampling only.
- Caveat: temperature 0 is not a guarantee of identical outputs across runs (batching and floating-point order can change results).

**Example:** My toy two-step model (hand-set probabilities, illustrative): first token A=0.5, B=0.4, C=0.1. After A the next token is flat (best 0.4); after B it is confident (x=0.9). Greedy picks A then x, joint probability 0.20. The best sequence is B then x, 0.36. Beam with k=2 keeps both A and B at step 1 and finds B x (0.36).

**Code:** (run, plain Python)
```python
import math
p1 = {"A": 0.5, "B": 0.4, "C": 0.1}
p2 = {"A": {"x": 0.4, "y": 0.3, "z": 0.3}, "B": {"x": 0.9, "y": 0.05, "z": 0.05}, "C": {"x": 0.5, "y": 0.5}}
w1 = max(p1, key=p1.get); w2 = max(p2[w1], key=p2[w1].get)
print("greedy:", w1, w2, round(p1[w1]*p2[w1][w2], 3))                # A x 0.2
beam = sorted(((math.log(p), (a,)) for a, p in p1.items()), reverse=True)[:2]
cand = [(lp + math.log(p), s + (b,)) for lp, s in beam for b, p in p2[s[-1]].items()]
print("beam(2):", [(s, round(math.exp(lp), 3)) for lp, s in sorted(cand, reverse=True)[:2]])
```
Output from my run: greedy `A x 0.2`; beam(2) `[(('B','x'), 0.36), (('A','x'), 0.2)]`. Sampling the first token 10,000 times gave frequencies 0.499 / 0.403 / 0.098, matching 0.5 / 0.4 / 0.1.

**Follow-ups:**
- *Does beam search always find the best sequence?* No, it is a heuristic. Only exhaustive search is exact, and that is exponential.
- *Why is beam bad for chat?* It maximises likelihood, and the most likely text is generic and repetitive; humans write text that is not the highest-probability string.
- *Why does greedy repeat?* Once a loop has high probability, argmax keeps choosing it (see Q20).

**Common mistakes:** calling greedy "optimal"; saying temperature 0 is always bit-exact; forgetting length normalisation in beam search; using beam search with high temperature (they do not combine); using sampling for tasks that need one exact answer.

### Q3 ⭐⭐⭐ 🟢 What is the pretraining objective of a decoder-only LLM? Write the next-token cross-entropy loss and explain the label shift.
**Asked at:** all types
**Say this first (1 line):** Predict the next token at every position, trained by minimising the average negative log-likelihood of the true next token: `L = -(1/N) sum_t log p(x_t | x_<t)`. No labels are needed, the text is its own supervision.

**Then explain:**
- The model outputs logits `(B, T, V)`. The logits at position t are the prediction for token t+1. So the logits at the last position have no label inside the sequence, and the first token is never predicted (it is only context).
- **The shift:** compare `logits[:, :-1]` (positions 1..T-1) with `labels[:, 1:]` (tokens 2..T). Forgetting this makes the model learn to copy the current token, which gives a deceptively low loss and a useless model.
- Many libraries (e.g. Hugging Face) do the shift inside the loss when you pass `labels = input_ids`. Do not shift twice.
- This is cross-entropy against a one-hot target, so the loss for one token is `-log p(true token)`. Causal masking lets all T positions train in one forward pass (see Part 1 Q5).
- Padding or prompt tokens you do not want to learn from are set to `-100` and skipped via `ignore_index`; divide by the number of real tokens, not B*T.
- Link to other objectives: BERT predicts masked tokens bidirectionally (Part 1 Q16). Embeddings and the LM head are in Part 1 Q25. Perplexity is `exp(loss)` (Q7).

**Example:** B=2, T=5, V=11, random logits (my run). N = B*(T-1) = 8 predictions, not 10. Shifted loss from `F.cross_entropy` 2.5116, my manual `-log_softmax` gather 2.5116. The unshifted (wrong) pairing gives a different number, 2.7552. Ignoring 2 padded labels changes the loss to 2.4426 (averaged over 6 tokens).

**Code:** (run, torch 2.14 CPU)
```python
import torch, torch.nn.functional as F
torch.manual_seed(0)
B, T, V = 2, 5, 11
logits = torch.randn(B, T, V); ids = torch.randint(0, V, (B, T))
loss = F.cross_entropy(logits[:, :-1].reshape(-1, V), ids[:, 1:].reshape(-1))
logp = logits[:, :-1].log_softmax(-1)
nll = -logp.gather(-1, ids[:, 1:, None]).squeeze(-1)           # -log p(x_t | x_<t)
print(loss.item(), nll.mean().item(), nll.numel())             # 2.5116 2.5116 8
print("unshifted:", F.cross_entropy(logits.reshape(-1, V), ids.reshape(-1)).item())  # 2.7552
lab = ids.clone(); lab[1, 3:] = -100                           # mask padding
print(F.cross_entropy(logits[:, :-1].reshape(-1, V), lab[:, 1:].reshape(-1), ignore_index=-100).item())  # 2.4426
```

**Follow-ups:**
- *What loss at initialisation?* About `ln V` if logits start near uniform (a handy sanity check; e.g. ln(50,000) is about 10.8).
- *Is it per token or per sequence?* Mean over tokens is standard; sum-vs-mean choices affect effective learning rate and how long documents are weighted.
- *Why not loss on prompt tokens in fine-tuning?* Often masked so the model learns the response, not the instruction (Part 4).

**Common mistakes:** no shift, or shifting twice; averaging over padding positions; saying the model predicts the whole sequence at once; confusing the loss (per-token NLL) with perplexity; claiming the objective needs human labels.

### Q4 ⭐⭐⭐ 🟡 Explain temperature, top-k and top-p (nucleus) sampling. What does each do to the distribution and what are sensible values?
**Asked at:** all types; product, GCC, GenAI startups
**Say this first (1 line):** Temperature rescales the logits to sharpen or flatten the whole distribution, top-k keeps only the k most likely tokens, and top-p keeps the smallest set of tokens whose probabilities add up to p; after truncation you renormalise and sample.

**Then explain:**
- **Temperature T:** `p = softmax(logits / T)`. T<1 sharpens (more deterministic), T>1 flattens (more random), T→0 approaches greedy, T=1 is the model's own distribution. It does not change the ranking of tokens.
- **Top-k:** fixed cutoff. Simple, but k is blind to context: k=40 is too loose when the model is sure and too tight when many continuations are valid.
- **Top-p (nucleus):** adaptive cutoff. Sort by probability, keep tokens until cumulative mass reaches p. A confident step keeps 1-2 tokens, an uncertain one keeps many.
- They combine: usual order is temperature, then top-k / top-p, then renormalise (more on order in Q19).
- **Sensible defaults** (rules of thumb, tune per task): factual QA, extraction, code, JSON: T 0-0.3. Chat: T about 0.7 with top-p about 0.9-0.95. Creative writing: T 0.8-1.0+. Do not push both temperature and top-p to extremes together; many providers advise changing one.

**Example:** logits `[4,3,2,1,0,-1]` (my run). At T=1 the probabilities are `[0.634, 0.233, 0.086, 0.032, 0.012, 0.004]`. At T=0.5 the top token has 0.865. At T=2 it falls to 0.414. Top-p 0.9 keeps 3 tokens here (cumulative 0.634, 0.867, 0.953), renormalised to `[0.665, 0.245, 0.09]`. On a flat distribution (`1.0 ... 0.5` logits) top-p 0.9 keeps all 6 tokens, while top-k=3 would still keep only 3. That is the adaptivity.

**Code:** (run, NumPy)
```python
import numpy as np
def softmax(z): e = np.exp(z - z.max()); return e / e.sum()
def top_k(p, k):
    q = np.zeros_like(p); i = np.argsort(-p)[:k]; q[i] = p[i]; return q / q.sum()
def top_p(p, tp):
    o = np.argsort(-p); c = np.cumsum(p[o]); n = np.searchsorted(c, tp) + 1   # smallest set with mass >= tp
    q = np.zeros_like(p); q[o[:n]] = p[o[:n]]; return q / q.sum()
logits = np.array([4.0, 3.0, 2.0, 1.0, 0.0, -1.0])
for T in [0.5, 1.0, 2.0]: print(T, np.round(softmax(logits / T), 3))
p = softmax(logits); print(np.round(top_p(p, 0.9), 3))     # [0.665 0.245 0.09 0 0 0]
```
A full sampler with empirical verification is Q13.

**Follow-ups:**
- *Temperature 0 in an API?* Implemented as greedy/argmax (dividing by 0 is avoided).
- *Does temperature change the top token?* No, only how much probability it gets.
- *Why top-p over top-k?* It adapts to model confidence; many systems use both, with top-k as a cheap pre-filter.

**Common mistakes:** applying temperature after truncation without renormalising; including the token that crosses the p threshold wrongly (it must be included); thinking higher temperature means "more accurate" or "more creative" without noting more errors; dividing by T on probabilities instead of logits; forgetting that all of these only affect sampling, not the model's weights.

### Q5 ⭐⭐⭐ 🟡 Token maths: how many tokens is 1,000 words, why do code, JSON and non-English text cost more, and how would you cut token spend?
**Asked at:** product, GCC, API-heavy teams
**Say this first (1 line):** For English prose, roughly 0.75 words per token, so 1,000 words is about 1,300 tokens (not 750; 750 words is about 1,000 tokens). Code, JSON and non-English text cost more per word because the tokenizer saw fewer such patterns and splits them into smaller pieces.

**Then explain:**
- **Rule of thumb, not a measurement:** it varies by tokenizer, so count with the model's own tokenizer before budgeting. Some prep guides quote code at around 1,200 tokens per 1,000 words; treat any such number as approximate. Some guides also state the ratio the wrong way round, so check the direction.
- **Why code and JSON cost more:** many short symbols (`{`, `":`, `,`, indentation), identifiers split into pieces, and repeated keys in every JSON record.
- **Why non-English costs more:** the vocabulary was learned mostly from English-heavy text, so other scripts get fewer merges. In the extreme they fall back to raw UTF-8 bytes (Devanagari uses 3 bytes per character). See Q17 for the Indian-language "token tax".
- **Cutting spend:**
  - Shorten the prompt: remove boilerplate, use only as many few-shot examples as needed.
  - Prompt caching for a stable long prefix (put static content first).
  - Retrieve fewer, better chunks (RAG, later parts) rather than stuffing context.
  - Compact output formats (short keys, CSV over verbose JSON), set `max_tokens`, ask for brevity.
  - Route easy requests to a smaller model; batch non-urgent jobs; summarise long chat history.
- Output tokens are usually priced higher than input tokens, so long answers hurt more than long prompts.

**Example:** I trained a toy byte-level BPE on about 150 words of English (60 merges; a toy, not a real tokenizer). The English sentence "the dog went to the market to buy fruit" (39 bytes) became 25 tokens. A Hindi sentence of 27 characters, which is 73 UTF-8 bytes, stayed at 73 tokens because no learned merge applied. Real tokenizers train on far more data and do much better, but the direction is the same: what was rare in training costs more tokens. Cost arithmetic with a hypothetical price of $3 per 1M input tokens: 1,333 tokens per request is about $4,000 per million requests; a 40% prompt cut brings it to about $2,400.

**Code:** (run, plain Python; toy tokenizer)
```python
from collections import Counter
en = ("the cat sat on the mat and the dog ate the food while the bird sang in the tree "
      "we are going to the market to buy some fruit and vegetables for the week ") * 4
def merge(s, pair, new):
    out, i = [], 0
    while i < len(s):
        if i < len(s)-1 and (s[i], s[i+1]) == pair: out.append(new); i += 2
        else: out.append(s[i]); i += 1
    return out
seq = list(en.encode()); merges = []; nid = 256
for _ in range(60):
    c = Counter(zip(seq, seq[1:])); best = max(c, key=lambda p: (c[p], p))
    merges.append((best, nid)); seq = merge(seq, best, nid); nid += 1
def enc(text):
    s = list(text.encode())
    for pair, new in merges: s = merge(s, pair, new)
    return s
for t in ["the dog went to the market to buy fruit", "कुत्ता फल खरीदने बाज़ार गया"]:
    print(len(t), len(t.encode()), len(enc(t)))     # 39 39 25  then  27 73 73
```

**Follow-ups:**
- *How do you count tokens exactly?* Use the provider's tokenizer or token-counting endpoint, and log the usage fields from real responses.
- *Does a bigger context window mean lower cost?* No. You pay per token, and attention cost also rises with length.
- *What else consumes tokens?* The system prompt and chat history are re-sent every turn, and long tool schemas are paid on every call.

**Common mistakes:** saying 1 word = 1 token; quoting the ratio backwards; forgetting that output tokens cost more; ignoring the re-sent system prompt and history; budgeting code or Hindi with the English rule of thumb.

### Q6 ⭐⭐⭐ 🟡 Why do LLMs struggle with counting letters ("strawberry"), arithmetic and string reversal? What does tokenization have to do with it?
**Asked at:** all types
**Say this first (1 line):** The model never sees letters or digits one by one, it sees token ids for multi-character chunks, so "how many r's" or "reverse this string" asks about structure that is hidden inside the token. It has to have memorised the spelling of each token from training data, which is unreliable.

**Then explain:**
- **Letters:** "strawberry" may arrive as two or three chunks. Each chunk is one embedding vector, and a vector does not directly expose its letters. Counting means recalling each chunk's spelling and tallying, in one forward pass with no scratchpad.
- **Reversal:** you must reverse the order of chunks and also the letters inside each chunk. The second part is the hard part.
- **Arithmetic:** numbers get chunked arbitrarily (for example 3-digit groups from the left), so place value does not line up. The model has to learn digit algorithms through chunks, and an unlucky split makes carrying hard. Some tokenizers split digits one by one, or right to left in groups, which helps.
- **Not only tokenization:** the model is a next-token predictor, not a calculator. It does pattern recall, so long multiplications fail even with clean digits. Tokenization makes an already hard task harder.
- **Fixes:** let it think step by step (spell out letters with spaces, which forces one token per letter), use a code or calculator tool, or use reasoning models that write out working. Tokenizers with digit splitting also help arithmetic.

**Example:** The split below is hypothetical (I did not use a real tokenizer): "strawberry" as `str | aw | berry`. The model's input is just three ids, `[0, 1, 2]`. The true count of r is 3, spread as 1, 0, 2 across the pieces, so it must know the spelling of each piece. For 1234567, left-to-right 3-digit chunks give `123 | 456 | 7`, while right-to-left gives `1 | 234 | 567`. Only the second matches place value (thousands, ones), which is how we add on paper.

**Code:** (run, plain Python; the split is hypothetical)
```python
word, pieces = "strawberry", ["str", "aw", "berry"]
print("true r count:", word.count("r"), "per-piece:", [p.count("r") for p in pieces])   # 3 [1, 0, 2]
print(word[::-1], "".join(p[::-1] for p in pieces[::-1]))   # yrrebwarts yrrebwarts: reverse chunks AND letters
def ltr(s, n=3): return [s[i:i+n] for i in range(0, len(s), n)]
def rtl(s, n=3):
    r = len(s) % n; return ([s[:r]] if r else []) + [s[i:i+n] for i in range(r, len(s), n)]
print(ltr("1234567"), rtl("1234567"))   # ['123','456','7'] ['1','234','567']
```

**Follow-ups:**
- *Would character-level models fix it?* Largely for letters, at the price of very long sequences (Q1). Byte/character models are an active research area.
- *Why do newer models count better?* Better training data and reasoning/tool use; the representation problem is mitigated, not removed.
- *Practical advice to a user?* Ask for step-by-step spelling, or call code for exact string and number operations.

**Common mistakes:** saying "the model is dumb" without the tokenization mechanism; claiming tokenization is the only cause of bad arithmetic; claiming every tokenizer splits "strawberry" the same way (it differs); forgetting that chain-of-thought and tools are the practical fixes.

### Q7 ⭐⭐⭐ 🟡 What is perplexity? How does it relate to cross-entropy loss, and why can't you compare it across models with different tokenizers?
**Asked at:** all types; product, research-leaning teams
**Say this first (1 line):** Perplexity is `exp` of the average per-token cross-entropy (negative log-likelihood) on held-out text: `PPL = exp(-(1/N) sum log p(x_t | x_<t))`. It is "the effective number of equally likely choices per token", and it is only comparable when the token units are the same.

**Then explain:**
- It is just the training loss (Q3) exponentiated, in nats. If the loss is in bits (log base 2), use `2^loss`. Lower is better. Basics are in B1P09-Q18.
- **Sanity anchors:** a model that predicts uniformly over V tokens has perplexity exactly V. A perfect model has perplexity 1.
- **Tokenizer problem:** the average is per token. A tokenizer with bigger tokens (fewer tokens per text) makes each prediction harder, so per-token loss and perplexity rise even when the total information in the text is unchanged. A character-level model with a low perplexity and a subword model with a much higher one can be equally good.
- **Fair comparison:** normalise by something fixed, such as the text itself. **Bits per byte (bpb)** = total NLL in bits over the whole text divided by the number of UTF-8 bytes. Bits per character and word-level perplexity are similar ideas. Use the same evaluation text for both models.
- **Limits:** perplexity measures fit to a text distribution, not usefulness. It says nothing direct about factuality, instruction following or safety, and it depends on the eval set (overlap with training data lowers it).

**Example (illustrative numbers, not real models):** the same 1,000-byte text, two hypothetical tokenizers. A splits it into 250 tokens with mean NLL 3.0 nats. B splits it into 400 tokens with mean NLL 1.9 nats.

| | tokens | mean NLL | perplexity | total NLL (nats) | bits per byte |
|---|---|---|---|---|---|
| A | 250 | 3.0 | 20.09 | 750 | 1.082 |
| B | 400 | 1.9 | 6.69 | 760 | 1.096 |

B looks three times "better" on perplexity, but A is slightly better on the fair metric (750 nats is less than 760 for the same text).

**Code:** (run, torch 2.14 CPU)
```python
import math, torch, torch.nn.functional as F
torch.manual_seed(0)
V, N = 50, 2000
nll = F.cross_entropy(torch.zeros(N, V), torch.randint(0, V, (N,)))   # uniform model
print(round(math.exp(nll.item()), 3))                                  # 50.0 = V
for name, ntok, mean_nll in [("A", 250, 3.0), ("B", 400, 1.9)]:
    total = ntok * mean_nll                                            # total nats for the same 1000 bytes
    print(name, round(math.exp(mean_nll), 2), round(total / math.log(2) / 1000, 3))   # ppl, bpb
```
Output from my run: `50.0`, then `A 20.09 1.082` and `B 6.69 1.096`.

**Follow-ups:**
- *Can you compare perplexity across checkpoints of one model?* Yes, same tokenizer and same eval set.
- *Why do reported values differ for the same model?* Different eval data, context length, or whether the first tokens (little context) are included.
- *Is low perplexity proof of a good chat model?* No; it says little about instruction following (see Parts 4 and 5).

**Common mistakes:** comparing perplexity between models with different vocabularies; using `exp` on a loss that is in bits; averaging perplexities instead of averaging NLL first; saying perplexity "is the vocabulary size" (only for a uniform model); reporting perplexity on text the model trained on.

### Q8 ⭐⭐⭐ 🟡 Pretraining vs continued pretraining vs fine-tuning: what changes in data, objective, cost and risk, and when do you choose each?
**Asked at:** all types
**Say this first (1 line):** All three train the same way (next-token loss), the difference is the starting point, the data and the scale: pretraining starts from random weights on trillions of general tokens, continued pretraining starts from a pretrained model on a large domain corpus, and fine-tuning starts from a pretrained model on a small curated task or instruction set.

**Then explain:**

| | Pretraining | Continued pretraining (CPT) | Fine-tuning (SFT) |
|---|---|---|---|
| Start | random init | pretrained checkpoint | pretrained (or CPT) checkpoint |
| Data | trillions of tokens, broad web, code, books | billions of domain tokens (legal, medical, a language, code) | thousands to hundreds of thousands of labelled examples |
| Objective | next-token on raw text | same next-token on raw text | next-token on responses (loss often only on the answer), or classification |
| Cost | millions of dollars, weeks of cluster time | a small fraction of that | usually one to a few GPUs (with LoRA, even less) |
| Main risk | wasted run, instability, data bugs | **catastrophic forgetting**, domain drift | overfitting, forgetting, learning style not facts |

- **Choose:** pretraining only if you are a lab, need a new language or tokenizer, or have a strong data advantage. CPT when the domain vocabulary and knowledge are far from web text (a low-resource language, a specialised field) and you have a lot of raw text. Fine-tuning for behaviour, format, tone or a narrow task. Try prompting and RAG first; fine-tuning changes behaviour more than it adds reliable new facts (Part 4 goes deeper).
- CPT tips: mix in some of the original general data (replay), use a lower learning rate with a short warmup, and watch general benchmarks for forgetting.
- Preference tuning (RLHF/DPO) comes after SFT, see Part 5.

**Example:** Compute with the standard approximation `C ~ 6ND` (Q11) for a 7B model (my arithmetic): pretraining on 2T tokens is about 8.4e22 FLOPs, CPT on 50B tokens about 2.1e21 (40x less), and a full fine-tune on 50k examples of 500 tokens (2.5e7 tokens) about 1.05e18, roughly 80,000x less than pretraining. The model size and token counts are hypothetical.

**Code:** (run, plain Python)
```python
N = 7e9
for name, tokens in [("pretrain, 2T tokens", 2e12), ("CPT, 50B tokens", 50e9), ("full FT, 50k ex x 500 tok", 50_000 * 500)]:
    print(f"{name:28s} {6 * N * tokens:.2e} FLOPs")   # 8.40e+22, 2.10e+21, 1.05e+18
```

**Follow-ups:**
- *Does CPT teach new facts?* Somewhat, but unevenly; it shifts the distribution and vocabulary usage. RAG is better for facts that change.
- *Can I skip pretraining and just fine-tune on a new language?* Poor if the tokenizer handles the language badly (Q17); CPT plus possibly extending the vocabulary is the usual route.
- *How do you limit forgetting?* Replay of general data, lower learning rate, LoRA or adapters, evaluating on a general benchmark during training.

**Common mistakes:** saying fine-tuning teaches the model new knowledge reliably; thinking SFT uses a different loss from pretraining (it is the same loss on different data and masking); skipping evaluation for forgetting after CPT; going straight to fine-tuning when prompting or RAG would do.

### Q9 ⭐⭐⭐ 🟡 Walk through a pretraining data pipeline: sources, cleaning, quality filtering, language ID, PII/toxicity filtering, deduplication and mixing.
**Asked at:** product, big tech, GenAI startups
**Say this first (1 line):** Collect raw web and other text, extract and clean it, filter by language and quality, remove PII and toxic content, deduplicate (exact and near-duplicate), then mix sources with chosen weights and tokenize. Data quality and deduplication move model quality as much as extra tokens do.

**Then explain:** (the order below is typical, real pipelines vary)
1. **Sources:** web crawl (largest, noisiest), code, books, papers, encyclopedias, forums, curated or licensed data. Check licences and robots rules.
2. **Extraction and cleaning:** pull the main text out of HTML (remove boilerplate, menus, ads), fix encoding, drop very short pages and pages with heavy repetition.
3. **Language ID:** a fast classifier (such as fastText-style models) tags the language; keep the target languages and a confidence threshold.
4. **Quality filtering:** heuristic rules (length, symbol ratio, repeated lines or words) plus model-based scores (a classifier trained to separate reference text from random crawl, or perplexity from a small LM). Over-aggressive filters can remove dialects and minority-language text.
5. **Safety and privacy:** remove or mask PII (emails, phone numbers, IDs; regex plus ML), drop toxic or adult content by classifier or blocklist. This is a trade-off: too much toxicity filtering can hurt the model's ability to recognise harmful text.
6. **Deduplication:** exact (hash of normalised text) and near-duplicate (MinHash with LSH, which approximates Jaccard similarity of n-gram shingles without comparing all pairs; the exact all-pairs comparison is O(n^2)). Also remove eval benchmark text (decontamination, Part 6 and Q30).
7. **Mixing:** choose proportions across sources and languages (upsample high-quality, downsample noisy), often tuned with small proxy runs. Then shuffle, tokenize and pack into fixed-length sequences.
- Why dedup matters: repeated text is memorised, wastes compute and inflates benchmark scores if it overlaps eval data.

**Example:** My 7-document toy run. The quality filter (at least 5 words, unique-word ratio above 0.5) dropped "hi" and a repetitive spam line. Exact dedup on normalised text removed the copy that differed only in punctuation, leaving 4 of 7 documents. A near-duplicate with one word changed had true Jaccard similarity 0.70 (3-word shingles) and a 128-hash MinHash estimate of 0.68, while an unrelated pair scored 0.0. The PII regex turned an email and a 10-digit number into `<PII>`. These are toy rules; production filters are far more elaborate.

**Code:** (run, plain Python, toy rules)
```python
import hashlib, re
docs = ["The quick brown fox jumps over the lazy dog near the river bank today and everyone watched it happen.",
        "The quick brown fox jumps over the lazy dog near the river bank today and everyone watched it happen!!",
        "The quick brown fox jumps over the lazy dog near the river bank today and everybody watched it happen.",
        "buy now buy now buy now buy now buy now buy now",
        "Contact me at john.doe@example.com or call 9876543210 for the report details.",
        "Gradient descent updates parameters in the direction that reduces the loss function.", "hi"]
norm = lambda t: re.sub(r"\W+", " ", t.lower()).strip()
def quality(t): w = t.split(); return len(w) >= 5 and len(set(w)) / len(w) > 0.5
seen, kept = set(), []
for d in docs:
    h = hashlib.md5(norm(d).encode()).hexdigest()
    if quality(d) and h not in seen: seen.add(h); kept.append(d)
print(len(kept))                                                   # 4
def shingles(t, k=3): w = norm(t).split(); return {" ".join(w[i:i+k]) for i in range(len(w)-k+1)}
S = [shingles(d) for d in kept]
def minhash(sh, n=128): return [min(int(hashlib.md5(f"{i}|{s}".encode()).hexdigest()[:8], 16) for s in sh) for i in range(n)]
M = [minhash(s) for s in S]
print(len(S[0] & S[1]) / len(S[0] | S[1]), sum(a == b for a, b in zip(M[0], M[1])) / 128)   # 0.7 0.68
```

**Follow-ups:**
- *Why MinHash/LSH?* All-pairs comparison does not scale to billions of documents; LSH buckets similar signatures so only candidates are compared.
- *Dedup at what level?* Document, paragraph or line, and across the whole corpus rather than per file; more aggressive dedup removes more memorisation but can also remove useful repeated facts.
- *How do you pick mixture weights?* Small proxy models and ablations; there is no universal answer.

**Common mistakes:** listing steps without saying why; forgetting language ID and PII; treating perplexity filtering as neutral (it biases toward the style of the reference model's data); deduplicating only exact copies; ignoring benchmark decontamination; forgetting to dedup across sources.

### Q10 ⭐⭐⭐ 🟡 What are LLM scaling laws? What do loss versus parameters, data and compute look like, and what can you do with them?
**Asked at:** big tech, product, GenAI startups
**Say this first (1 line):** Scaling laws say that test loss falls as a smooth power law as you increase parameters N, training tokens D or compute C, so you can fit small runs and predict big ones, and choose how to split a fixed budget between model size and data.

**Then explain:**
- **Shape:** `L(x) ~ a * x^(-alpha)` (plus an irreducible floor in fuller forms). On a log-log plot it is a straight line, and each 10x in N, D or C cuts loss by a constant factor. The exponents are small, so gains are steady but slow.
- **Kaplan et al. (OpenAI, 2020):** loss follows power laws in N, D and C over many orders of magnitude, with architecture details like depth vs width mattering little. Their reading was that, for a given compute budget, you should grow model size much faster than data (exponents from memory: roughly 0.076 for N, 0.095 for D, 0.05 for C). Models of that era were large and trained on relatively few tokens.
- **Hoffmann et al. (DeepMind, 2022, "Chinchilla"):** refit with many more runs and found N and D should grow about equally with compute, which is roughly 20 tokens per parameter. Details in Q11.
- **Standard compute approximation:** `C ~ 6ND` FLOPs for training a dense transformer (about 2ND for the forward pass and 4ND for the backward pass).
- **What you can do with them:** (1) predict the loss of a big run from small ones before spending the money, (2) pick N and D for a budget, (3) decide where to invest (more data vs a bigger model), (4) sanity-check that a run is on trend, and spot data or bug problems when it is not.
- **Caveats:** loss is not the same as downstream ability; fits can be sensitive to the setup (learning-rate schedule, data quality, epochs of repeated data); they extrapolate well over a range but not forever; and they ignore inference cost, which is why many models are trained past the compute-optimal point (Q11).

**Example:** A tiny demo on synthetic data (generated from a known law, so it only shows the method). I generated losses from `L = 20 * N^(-0.076)` with a little noise for N from 1e6 to 1e10, and a log-log fit recovered alpha = 0.076. A 10x bigger model multiplies loss by `10^(-0.076)`, about 0.84, and the fit extrapolated to N=1e11 predicted 2.921 against the noiseless 2.918. Real fits use real runs; the numbers here are not from any real model.

**Code:** (run, NumPy, synthetic data)
```python
import numpy as np
rng = np.random.default_rng(0)
N = np.logspace(6, 10, 9); alpha, a = 0.076, 20.0
L = a * N**(-alpha) * np.exp(rng.normal(0, 0.003, N.size))     # synthetic power law + noise
slope, icpt = np.polyfit(np.log(N), np.log(L), 1)              # straight line in log-log space
print(round(-slope, 3), round(10**slope, 3))                   # 0.076 0.84
print(round(float(np.exp(icpt) * 1e11**slope), 3))             # 2.921 (extrapolation)
```

**Follow-ups:**
- *Do scaling laws predict emergent abilities?* Loss scales smoothly, but specific task accuracy can look like a sudden jump; whether that is real or a metric artefact is debated (Q40).
- *Why is loss a power law?* There is no single accepted explanation; treat it as an empirical regularity.
- *Does repeating data break them?* Yes, extra epochs have diminishing value, so the data term assumes mostly fresh tokens.

**Common mistakes:** saying "bigger is always better" without the diminishing-returns shape; presenting `C ~ 6ND` as a Chinchilla result (it is a standard approximation); treating loss as accuracy; extrapolating far outside the fitted range; forgetting the irreducible-loss floor.

### Q11 ⭐⭐⭐ 🟡 What did Chinchilla find? Use C ~ 6ND to work out the compute-optimal model size and token count for a given budget.
**Asked at:** big tech, product, research-leaning teams
**Say this first (1 line):** Chinchilla (Hoffmann et al., DeepMind, 2022) found that earlier large models were undertrained: for a fixed compute budget, parameters and training tokens should scale together, at roughly 20 tokens per parameter. Their 70B model trained on 1.4T tokens beat the 280B Gopher, which used about the same compute.

**Then explain:**
- **Finding:** they trained 400+ models of varying size and data, and fitted how loss depends on N and D. Result: for compute-optimal training, N and D should grow in equal proportion (each about the square root of compute). Kaplan et al. (2020) had favoured growing the model faster than the data (Q10).
- **Headline result:** Chinchilla 70B, 1.4T tokens, ratio 20. Gopher 280B. Reported MMLU about 67.5 vs 60 for Gopher (from the explainer page I used). Smaller models are also cheaper to serve.
- **The maths, with the standard approximation `C ~ 6ND`:** put `D = 20N`, so `C = 6 * N * 20N = 120 N^2`, hence `N = sqrt(C/120)` and `D = 20N`. (The `6ND` approximation is standard, not something the Chinchilla result itself states.)
- **Caveats:** the 20:1 ratio is approximate. Other fits and a replication attempt put the optimum somewhere in the teens to twenties, with wide uncertainty. It optimises training compute only. If a model will serve billions of requests, you should train a smaller model on far more tokens than compute-optimal, since inference cost dominates (many open models are trained at hundreds of tokens per parameter). And it assumes enough fresh, quality data exists.

**Example:** Budget `C = 1e23` FLOPs (my computation): `N = sqrt(1e23/120)` is about 2.89e10, so 28.9B parameters, and `D = 20N` is about 5.77e11, so 577B tokens. Check: 6 x 2.89e10 x 5.77e11 = 1.0e23. If the true ratio were 10, 15 or 25 instead, N would be 40.8B, 33.3B or 25.8B, and D 408B, 500B or 645B tokens, so the answer moves by tens of percent, not by orders of magnitude. As a sanity check, 6ND for Chinchilla itself is 5.88e23, and `sqrt(5.88e23/120)` gives exactly 70.0B and 1,400B tokens, which is what the formula should give for ratio 20. For Gopher, 6ND with 280B parameters and 300B tokens (the token count is from memory) is about 5.0e23, the same order as Chinchilla's budget, consistent with "same compute". By contrast a 7B model on 2T tokens (ratio about 286) uses 8.4e22 FLOPs, deliberately over-trained for cheap inference.

**Code:** (run, plain Python)
```python
import math
C = 1e23
N = math.sqrt(C / 120); D = 20 * N                    # from C = 6*N*D and D = 20*N
print(f"N={N/1e9:.1f}B params, D={D/1e9:.0f}B tokens, 6ND={6*N*D:.2e}")   # 28.9B, 577B, 1.00e+23
for r in [10, 15, 20, 25]:                            # sensitivity to the tokens-per-parameter ratio
    n = math.sqrt(C / (6 * r)); print(r, f"{n/1e9:.1f}B", f"{r*n/1e9:.0f}B tokens")
```

**Follow-ups:**
- *Why do people train Llama-style models far beyond 20 tokens per parameter?* Training is a one-time cost, inference is repeated; a smaller, longer-trained model is cheaper to serve at similar quality.
- *Is Chinchilla's 20 exact?* No; it comes from a fit, and refits give somewhat different ratios.
- *What if data runs out?* Repeating data a few epochs helps a little but with diminishing returns; synthetic data and quality filtering are the usual responses (Q9).

**Common mistakes:** saying exactly 20 tokens per parameter as if it were a law; forgetting the 6 in `6ND`, or mixing up params and tokens; attributing `6ND` to the Chinchilla page or paper as a headline finding; ignoring inference cost when choosing N; saying Chinchilla showed "more data beats bigger models" without the equal-scaling point.

### Q12 ⭐⭐⭐ 🟡 Code: implement a byte-pair-encoding tokenizer (train, encode, decode) with deterministic tie-breaking, and show a round trip.
**Asked at:** product, big tech, live-coding rounds; a Glean software-engineer onsite/technical-screen report and a Perplexity online-assessment listing mention BPE coding
**Say this first (1 line):** BPE training repeatedly counts adjacent symbol pairs, merges the most frequent one (ties broken deterministically), and records the merge list; encoding replays those merges in the same order, and decoding just concatenates tokens.

**Then explain:**
- **Train:** start from characters. Count pairs, pick the pair with the highest count, ties broken by the lexicographically smallest pair, stop when the best count is below a threshold. Append the pair to `merges` (its index is its rank), rewrite the sequence.
- **Encode:** start from characters of the new text and apply every learned merge, in rank order. Do not re-count on new text.
- **Decode:** `"".join(tokens)`. It is lossless because every token is the concatenation of the characters it replaced.
- **Counting convention matters.** Reported interview versions differ (one report mentions non-overlapping left-to-right counting). I state mine up front: I count overlapping adjacent pairs, but the merge itself is applied left to right without overlap. Ask the interviewer which one they want.
- **Complexity:** naive is O(M x n) for M merges on n symbols (recount and rewrite each round). Production trainers keep pair counts in a priority queue plus a linked list of symbols, so a merge only updates the neighbours of changed positions. Real tokenizers also pre-split text into words, so counts are over a word-frequency table, not the raw string.

**Example (executed):** `"abababa"`, threshold 2. Overlapping counting gives merges `[('a','b'), ('ab','ab')]` and tokens `['abab','ab','a']`. Non-overlapping counting gives only `[('a','b')]`, because after the first merge `(ab,ab)` is counted once in `ab ab ab a`. So the "classic" second merge depends on the convention.

**Code:** (executed)
```python
from collections import Counter

def count_pairs(seq, overlap=True):
    c, i = Counter(), 0
    while i < len(seq) - 1:
        c[(seq[i], seq[i + 1])] += 1
        i += 1 if (overlap or seq[i] != seq[i + 1]) else 2
    return c

def merge(seq, pair, new):
    out, i = [], 0
    while i < len(seq):
        if i < len(seq) - 1 and (seq[i], seq[i + 1]) == pair:
            out.append(new); i += 2
        else:
            out.append(seq[i]); i += 1
    return out

def train(text, threshold=2, overlap=True):
    seq, merges = list(text), []
    while True:
        counts = count_pairs(seq, overlap)
        if not counts: break
        pair, n = min(counts.items(), key=lambda kv: (-kv[1], kv[0]))  # max count, then lexicographic
        if n < threshold: break
        merges.append(pair)
        seq = merge(seq, pair, pair[0] + pair[1])
    return merges, seq

def encode(text, merges):
    seq = list(text)
    for pair in merges:                 # rank order
        seq = merge(seq, pair, pair[0] + pair[1])
    return seq

decode = "".join

print(train("abababa", 2, True))    # ([('a','b'), ('ab','ab')], ['abab','ab','a'])
print(train("abababa", 2, False))   # ([('a','b')], ['ab','ab','ab','a'])
text = "low lower lowest low low newer newest"
merges, seq = train(text, 2)
assert decode(encode(text, merges)) == text and encode(text, merges) == seq
new = "lowest newlow"
assert decode(encode(new, merges)) == new          # unseen text also round-trips
print(encode(new, merges))          # ['low', 'e', 'st', ' new', 'low']
assert train(text, 2)[0] == merges  # deterministic
```
Note the toy trains on the raw string, so merges like `' low'` cross word boundaries; a real tokenizer pre-splits on words first.

**Follow-ups:**
- *Why merge ranks, not just a vocab lookup?* Greedy longest-match against the vocab can give a different split. Replaying merges in order reproduces exactly how training would have segmented the text.
- *How would you make it handle any string?* Start from UTF-8 bytes instead of characters (Q15).
- *How to speed it up?* Word-frequency table, pair-to-positions index, heap with lazy updates.

**Common mistakes:** Re-counting pairs at encode time. Python `max` on a dict with no tie rule, so results change between runs. Not saying which counting convention is used. Merging `(a,a)` in `aaa` inconsistently. Forgetting the empty-counts and threshold stop.


### Q13 ⭐⭐⭐ 🟡 Code: implement temperature, top-k and top-p sampling from a logits vector, and verify it empirically.
**Asked at:** product, big tech, live-coding rounds
**Say this first (1 line):** Divide logits by temperature, softmax, keep the top-k and the top-p nucleus, renormalise, then sample; always keep at least the top token.

**Then explain:**
- **Order:** temperature first (it reshapes the distribution, so the nucleus depends on it), then truncation, then renormalise. Return a new array; never mutate the caller's logits.
- **Top-k:** keep the k highest-probability tokens. **Top-p:** sort descending, keep the smallest prefix whose cumulative mass reaches p. The token that crosses p is kept (the usual off-by-one bug drops it).
- **Ties:** use a stable sort so equal logits are ordered by index; with `top_k` cutting between tied tokens the lower index wins. Say this out loud.
- **Edge cases:** `top_p=0` or `top_k=1` degenerates to greedy (at least 1 token survives). Temperature 0 should be handled as argmax, not divided by.
- Use `exp(z - max)` for numerical stability.

**Example (executed):** logits `[2,1,1,.5,0,-1]`: at T=1 probabilities are `[.466,.172,.172,.104,.063,.023]`. `top_p=0.8` keeps 3 tokens (cumulative .466, .638, .810) and renormalises to `[.576,.212,.212,0,0,0]`.

**Code:** (executed, NumPy)
```python
import numpy as np

def probs_from_logits(logits, temperature=1.0, top_k=0, top_p=1.0):
    z = np.asarray(logits, dtype=np.float64) / temperature
    p = np.exp(z - z.max()); p /= p.sum()
    order = np.argsort(-p, kind="stable")
    keep = np.zeros(len(p), dtype=bool)
    k = len(p) if top_k <= 0 else min(top_k, len(p))
    keep[order[:k]] = True
    csum = np.cumsum(p[order])
    n_p = max(int(np.searchsorted(csum, top_p - 1e-12) + 1), 1)   # crossing token kept
    mask_p = np.zeros(len(p), dtype=bool); mask_p[order[:n_p]] = True
    keep &= mask_p
    q = np.where(keep, p, 0.0)
    return q / q.sum()

def sample(logits, rng, **kw):
    return rng.choice(len(logits), p=probs_from_logits(logits, **kw))

logits = np.array([2.0, 1.0, 1.0, 0.5, 0.0, -1.0])
rng = np.random.default_rng(0)
kw = dict(temperature=0.7, top_k=4, top_p=0.9)
expected = probs_from_logits(logits, **kw)
print(np.round(expected, 4))        # [0.6263 0.1501 0.1501 0.0735 0. 0.]
draws = rng.choice(6, size=100_000, p=expected)
emp = np.bincount(draws, minlength=6) / 100_000
print(np.abs(emp - expected).max())  # 0.0016
```
Measured max abs error over 100k draws: 0.0016 for the combined setting and 0.0024 for `top_p=0.8` alone; masked tokens were never sampled. That is the expected ~1/sqrt(N) noise, not a bug. The single-draw `sample()` over 20k calls gave `[.623,.149,.154,.075,0,0]`.

**Follow-ups:**
- *Top-k then top-p or the reverse?* Intersection of both masks is order-independent as written here; frameworks that renormalise between steps can differ slightly.
- *How to do it batched on GPU?* `torch.sort`, `cumsum`, mask, `scatter` back, `torch.multinomial`.
- *Why top-p over top-k?* Nucleus size adapts: few tokens when the model is confident, many when flat.

**Common mistakes:** Applying temperature after truncation. Forgetting to renormalise. Dropping the token that crosses p. Dividing by T=0. Mutating input logits. Verifying with a handful of samples instead of thousands.


### Q14 ⭐⭐ 🟡 How do you choose a tokenizer vocabulary size? Discuss sequence length, embedding/softmax cost, rare-token under-training and multilingual coverage.
**Asked at:** product, GenAI startups, big tech
**Say this first (1 line):** Vocabulary size trades shorter sequences and better multilingual coverage against a bigger embedding/softmax and rarely-seen tokens that stay under-trained; I would pick it by measuring tokens-per-text on my target data and the model-size budget, not by a fixed rule.

**Then explain:**
- **Larger vocab, shorter sequences:** more merges means common words and scripts become single tokens, so the same text takes fewer tokens. That cuts attention cost, KV-cache size, latency and API spend.
- **Larger vocab, bigger heads:** embedding and unembedding grow as `V x d` each (see Part 1 Q25 for the full cost discussion, I will not repeat it). The softmax over V also adds per-token compute and logits memory at training time.
- **Rare tokens under-train:** with a very large V, the tail tokens appear few times, their embeddings barely move and can behave oddly (see Q18).
- **Small vocab:** long sequences, more steps per word, weaker handling of non-English, but dense, well-trained tokens.
- **Multilingual coverage:** vocab slots are shared across languages. If the training corpus for the tokenizer is English-heavy, other scripts get few merges (Q17). Balanced sampling of languages when training the tokenizer, plus a bigger V, is the main lever.
- Diminishing returns: each extra merge saves fewer tokens than the previous one, while cost per slot is constant.

**Example (computed):** at d=4096, one `V x d` matrix is 131M params at V=32k, 524M at V=128k, 1.05B at V=256k (double if untied). At fp32, the logits for one position are 128 KB at 32k and 512 KB at 128k.

**Follow-ups:**
- *How do you choose empirically?* Train tokenizers at several sizes on a data sample, measure tokens per document per language (and bits-per-byte of a small model, since perplexity is not comparable across tokenizers, Q7), and pick the knee.
- *Is bigger always better for big models?* The head is a smaller share of parameters in a big model, so larger V is cheaper relatively. That is a reason, not a law.
- *Can you change it later?* Only by extending the tokenizer and continuing pretraining (Q36).

**Common mistakes:** Saying "more tokens = always better". Forgetting the softmax/logit cost. Ignoring tail-token under-training. Quoting a specific "optimal" size without data. Comparing perplexity across vocab sizes.


### Q15 ⭐⭐ 🟡 What is byte-level BPE, why does it remove out-of-vocabulary tokens, and what are its trade-offs (UTF-8, byte fallback)?
**Asked at:** product, GenAI startups
**Say this first (1 line):** Byte-level BPE runs BPE over UTF-8 bytes instead of characters, so the base vocabulary is just the 256 byte values and any string can be encoded; nothing is ever out of vocabulary.

**Then explain:**
- **Base alphabet = 256 bytes.** Every Unicode string is a byte sequence under UTF-8, so every input has a valid tokenisation, even emojis, typos, or scripts never seen in training.
- **UTF-8 is variable length:** ASCII is 1 byte, accented Latin 2, Devanagari and CJK 3, most emoji 4. A rare character starts as several byte tokens until merges join them.
- **Trade-offs:** rare scripts cost more tokens (Q17); a token boundary can fall in the middle of a character, so a partial token may not be valid UTF-8, which matters when streaming (Q22) and for incomplete-token artefacts (Q18); decoding must decode the whole byte string at once.
- **Byte fallback in SentencePiece** is different: the vocab is character/subword-based, and only characters not in the vocab are spelled as byte tokens (`<0x..>`). Common text uses normal pieces; the byte tokens are an escape hatch. Byte-level BPE has no characters at all, only bytes.
- Both guarantee no `<unk>`; the byte-level approach is simpler, fallback keeps common non-Latin text compact if the vocab includes it.

**Example (executed):**
```python
for s in ["hello", "café", "नमस्ते", "日本", "😀"]:
    b = s.encode("utf-8")
    print(repr(s), len(s), "chars", len(b), "bytes", list(b))
    assert b.decode("utf-8") == s
try: "नमस्ते".encode()[:2].decode("utf-8")
except UnicodeDecodeError as e: print(e.reason)   # unexpected end of data
```
Output: `hello` 5 chars 5 bytes; `café` 4 chars 5 bytes (`é` = 195,169); `नमस्ते` 6 chars 18 bytes; `日本` 2 chars 6 bytes; `😀` 1 char 4 bytes. Cutting the Devanagari bytes after 2 raises "unexpected end of data".

**Follow-ups:**
- *Does byte-level hurt English?* No; ASCII is 1 byte and gets many merges.
- *Why not use raw bytes with no merges?* Sequences become 3-4x longer for non-Latin text and attention cost grows quadratically.
- *Can the model generate invalid UTF-8?* Yes, it can emit byte sequences that are not valid; decoders typically replace them with the replacement character.

**Common mistakes:** Saying byte-level BPE has a 256-token vocab (that is only the base; merges are added on top). Confusing byte fallback with byte-level BPE. Forgetting multi-byte characters. Claiming "no OOV" means "good quality on every language".


### Q16 ⭐⭐ 🟡 What are special tokens (BOS, EOS, PAD, role/chat tokens) and chat templates? What breaks if the template or padding side is wrong?
**Asked at:** product, GCC, API-heavy and fine-tuning teams
**Say this first (1 line):** Special tokens are reserved IDs that carry structure (start, end, padding, who is speaking); a chat template is the exact string format that turns a message list into those tokens, and getting it or the padding side wrong silently degrades output instead of raising an error.

**Then explain:**
- **BOS/EOS:** start of sequence and end of sequence. EOS is how the model learns to stop (Q22). **PAD:** filler to make batch rows equal length; it must be masked, never attended to and never counted in the loss. **Role/chat tokens:** markers such as system/user/assistant turn boundaries; the exact tokens are model-specific.
- **Chat template:** the instruct model was fine-tuned on one exact format. A different format (missing role markers, missing generation prompt, double BOS, wrong whitespace) puts the model slightly off-distribution. It still answers, just worse, so the failure is silent. Always use the template shipped with the model's tokenizer and diff the rendered string.
- **Padding side:** for batched generation with a decoder-only model, pad on the **left**. The next token is predicted from the last position; with right padding, the last position for shorter rows is a PAD, so the model continues from padding. Left padding keeps real tokens aligned at the end. Pair it with an attention mask and position ids computed from the mask so padding does not shift positions. (For training with right padding, the loss mask ignores PAD.)
- Special tokens in user text can be injected as control tokens if the tokenizer parses them; decide whether user text may produce them.

**Example (executed, torch):** sequences `[5,6,7,8]` and `[9,10]`:
- right pad: `[[5,6,7,8],[9,10,0,0]]`, last tokens `[8, 0]`, so row 2 reads from PAD.
- left pad: `[[5,6,7,8],[0,0,9,10]]`, mask `[[1,1,1,1],[0,0,1,1]]`, last tokens `[8,10]`, position ids `[[0,1,2,3],[0,0,0,1]]`.

**Code:** (executed)
```python
import torch
torch.manual_seed(0); PAD = 0
def batch(seqs, side):
    L = max(map(len, seqs)); ids, mask = [], []
    for s in seqs:
        p = [PAD]*(L-len(s))
        ids.append(p+s if side=="left" else s+p)
        mask.append([0]*len(p)+[1]*len(s) if side=="left" else [1]*len(s)+[0]*len(p))
    return torch.tensor(ids), torch.tensor(mask)
ids, mask = batch([[5,6,7,8],[9,10]], "left")
pos = (mask.cumsum(-1) - 1).clamp(min=0)
T = ids.shape[1]
allowed = torch.tril(torch.ones(T, T, dtype=torch.bool))[None] & mask.bool()[:, None, :]
d = 8; emb = torch.nn.Embedding(20, d); Wq, Wk, Wv = (torch.randn(d, d) for _ in range(3))
def attn_last(ids, allowed):
    x = emb(ids); q, k, v = x@Wq, x@Wk, x@Wv
    s = (q@k.transpose(-1,-2))/d**0.5
    return (s.masked_fill(~allowed, float("-inf")).softmax(-1)@v)[:, -1]
solo = attn_last(torch.tensor([[9,10]]), torch.tril(torch.ones(2,2,dtype=torch.bool))[None])[0]
print(torch.allclose(attn_last(ids, allowed)[1], solo, atol=1e-6))   # True
```
The demo uses no positional encoding, so it checks only that the mask makes padded and unpadded outputs equal; position ids matter for RoPE or learned positions.

**Follow-ups:**
- *Why does the wrong template only degrade quality?* Tokens are valid; the model just sees an unfamiliar prefix.
- *Pad token missing?* Many decoder-only tokenizers have none; reuse EOS as PAD but rely on the attention mask, and be careful the loss does not mask real EOS.
- *Can you right-pad for generation?* Only with per-row last-real-token indexing, which most generate loops do not do.

**Common mistakes:** Right padding in batched generation. Forgetting the attention mask. Hand-writing the chat format. Double BOS. Training on PAD or on the prompt unintentionally. Treating EOS-as-PAD loss masking carelessly.


### Q17 ⭐⭐ 🟡 Why do Indian and other low-resource languages cost more tokens (the "token tax")? What can you do about it?
**Asked at:** India product companies, GCCs, GenAI startups
**Say this first (1 line):** Tokenizers learn merges from their training data; if that data is English-heavy, Hindi, Tamil and other scripts get few merges, so the same meaning is split into many more tokens, which costs more money, latency and context.

**Then explain:**
- **Mechanism:** BPE merges are chosen by frequency. English words get whole-word tokens; rarer scripts end up as character pieces or even raw bytes.
- **Bytes make it worse for byte-level tokenizers:** Devanagari characters are 3 bytes each in UTF-8 versus 1 for ASCII, so the starting point is already longer, and without learned merges each character can cost up to 3 tokens.
- **Consequences:** higher API bill per request, less usable context window, slower generation (more decode steps), and often weaker quality because the model sees fragments.
- **Real ratios vary by tokenizer and must be measured** on your own text with the exact tokenizer you will deploy. I will not quote a number from memory.
- **Mitigations:** choose a model with a multilingual vocabulary; extend the tokenizer with new tokens for the language and continue pretraining so the new embeddings are learned (Q36); transliteration/normalisation tricks only help in narrow cases; cache and compress prompts; keep prompts and system instructions in the cheaper language where quality allows.

**Example (executed):**
```python
for name, s in [("english", "Hello how are you"), ("hindi", "आप कैसे हैं")]:
    print(name, len(s), "chars", len(s.encode()), "bytes", round(len(s.encode())/len(s), 2), "bytes/char")
print({c: len(c.encode()) for c in "aअ ा"})
```
Output: English 17 chars, 17 bytes, 1.0 bytes/char; Hindi 11 chars, 29 bytes, 2.64 bytes/char; `a`=1 byte, `अ`=3, space=1, the vowel sign `ा`=3. This is a byte count, not a token count: it shows the raw-material gap, not what any specific tokenizer produces.

**Follow-ups:**
- *How would you measure the tax?* Tokens per character (or per sentence) on a parallel corpus, for your candidate tokenizers; also compare cost per request.
- *Does extending the vocab fix it?* It shortens sequences but new embeddings start untrained; you need continued pretraining and care with init (Q36).
- *Is it only cost?* No: fewer words fit in context and quality can drop.

**Common mistakes:** Quoting a "Hindi costs N times more" figure without measuring. Confusing bytes with tokens. Assuming byte-level BPE alone solves multilingual efficiency. Ignoring the context-window impact.


### Q18 ⭐⭐ 🟡 What are glitch or under-trained tokens, why do they exist, and how would you detect them?
**Asked at:** research-leaning teams, big tech
**Say this first (1 line):** Glitch tokens are vocabulary entries the model barely or never saw during training, so their embeddings stay near initialisation and the model behaves erratically when they appear; I would find them by looking for tokens whose embeddings look untrained.

**Then explain:**
- **Why they exist:** the tokenizer is trained on one corpus and the model on another (or a filtered one). A string frequent enough to get its own token, for example from scraped boilerplate or username lists, may then be rare or absent in the model's data. The token exists in the vocab, but its embedding got almost no gradient updates.
- **Symptoms (as described in the glitch-token research, arXiv 2404.09894):** refusing to repeat the token, hallucinated or unrelated output, evasion, odd behaviour. Byte-level BPE also produces incomplete tokens, fragments of multi-byte characters that are rarely valid alone (arXiv 2410.23684).
- **Detection heuristics:**
  - Embedding-norm outliers: untrained rows stay near the initial scale while trained rows drift, so unusual norms flag candidates.
  - Unembedding-side heuristics: tokens that are almost never predicted, or whose output vectors sit near the mean/initial vector.
  - Tokenizer-vs-corpus frequency: count each token's occurrences in the training corpus; zero or near-zero is suspicious.
  - Behavioural probes: ask the model to repeat, spell or define the token, and flag failures.
- **Fix:** remove or remap such tokens, train the tokenizer on the same data mix as the model, or re-initialise and continue training. At application level, sanitise inputs and monitor for odd outputs.

**Example:** compute `norm(E[i])` for every row of the embedding matrix, plot the distribution, and inspect the most atypical rows with a repeat-this-token prompt. Tokens that fail both the statistic and the probe go on a blocklist. I will not name specific token strings; the set depends on the model and tokenizer. (Not executed: no model weights available here.)

**Follow-ups:**
- *Is low norm always the signal?* No; it is a heuristic, and the right direction depends on initialisation and weight tying, so verify behaviourally.
- *Does byte-level BPE remove the problem?* It removes OOV, not under-trained merges.
- *Why does it matter in products?* Users can paste odd strings that trigger unstable behaviour.

**Common mistakes:** Treating glitch tokens as a decoding bug. Quoting famous token strings from memory. Assuming a fixed norm threshold works across models. Skipping the behavioural check.


### Q19 ⭐⭐ 🟡 What are min-p and typical sampling, and in what order should samplers (penalties, temperature, truncation) be applied?
**Asked at:** product, GenAI startups, inference teams
**Say this first (1 line):** Min-p keeps only tokens whose probability is at least `min_p` times the top token's probability, so the cutoff scales with the model's confidence; and I apply penalties first, then temperature, then truncation, though frameworks differ.

**Then explain:**
- **Min-p:** `keep p_i >= min_p * p_max`, then renormalise. Confident step (big `p_max`): high bar, few candidates. Flat step: low bar, many candidates. That is its appeal over a fixed top-k.
- **Typical sampling (locally typical):** keeps tokens whose surprise (-log p) is close to the distribution's entropy, rather than simply the most probable ones. I know it as a concept and would describe it at that level.
- **Order:** a common order (the llama.cpp-style order described in the pyshine page) is repetition/frequency/presence penalties on logits, then temperature, then truncation (top-k, top-p, min-p), then sample. Order matters: temperature before min-p changes which tokens pass the threshold. Other frameworks apply temperature last or in a different sequence, and APIs often do not expose the order, so I check the docs of the stack I use.

**Example (executed):** logits `[4,3,1,0,-1]` give p = `[.693,.255,.035,.013,.005]`. `min_p=0.1` has threshold 0.069, so two tokens survive: `[.731,.269,0,0,0]`. On a flat distribution `[1,.9,.8,.7,.6]` with `min_p=0.5` all 5 survive; on the peaked one only 1 does. Order effect at T=2: temperature then min-p keeps 4 tokens, min-p on the T=1 probabilities then temperature keeps 2. At T=0.5 both keep 2.

**Code:** (executed)
```python
import numpy as np
def softmax(z): z = np.asarray(z, float); e = np.exp(z - z.max()); return e / e.sum()
def min_p(p, m):
    q = np.where(p >= m * p.max(), p, 0.0); return q / q.sum()
logits = np.array([4.0, 3.0, 1.0, 0.0, -1.0])
print(min_p(softmax(logits), 0.1).round(4))          # [0.7311 0.2689 0. 0. 0.]
print(int((min_p(softmax(logits / 2.0), 0.1) > 0).sum()))   # 4  (temperature first)
```

**Follow-ups:**
- *Min-p vs top-p?* Top-p's nucleus is defined by cumulative mass; min-p by relative probability to the top token. Min-p tends to be more stable at high temperature, though I would test on my task.
- *Is min-p always one token minimum?* Yes, the top token always passes since `p_max >= min_p * p_max` for `min_p <= 1`.

**Common mistakes:** Assuming every library uses the same order. Using min-p and top-p together without knowing each cut. Setting min-p near 1 (that is greedy). Forgetting to renormalise.


### Q20 ⭐⭐ 🟡 Why do LLMs repeat themselves, and how do repetition, frequency and presence penalties work? When do penalties hurt (code, JSON)?
**Asked at:** product, GenAI startups, API-heavy teams
**Say this first (1 line):** Models repeat because repeating is locally the highest-probability continuation and each repeat makes the next one more likely; penalties lower the scores of tokens already used, but they punish legitimate repeats too, which breaks code and JSON.

**Then explain:**
- **Why repetition happens:** greedy/low-temperature decoding follows the mode, and context that already contains a phrase makes copying it very probable (a feedback loop). Training data also has repeated patterns.
- **HF-style `repetition_penalty` (>1):** for each token already seen, if its logit is positive divide by the penalty, if negative multiply by it. Both make the token less likely. One flat penalty regardless of how many times it appeared.
- **OpenAI-style penalties:** `logit - frequency_penalty * count - presence_penalty * (count > 0)`. Frequency grows with each use; presence is a one-time hit for having appeared at all.
- **Other fixes:** no-repeat n-gram blocking, higher temperature or min-p/top-p, better prompting, length limits.
- **Why it hurts code/JSON:** braces, quotes, keys, indentation and variable names must repeat. A strong penalty (the 1.2 range) pushes the model off the correct token to a worse one, giving broken syntax or renamed variables. For structured output I use no penalty, or very mild, and constrained decoding (Part 3).

**Example (executed):** logits `[2,-1,.5,0]`, tokens 0 and 1 seen, HF penalty 1.2: `[1.667,-1.2,.5,0]` (positive divided, negative multiplied). OpenAI style with counts `[3,1,0,0]`, frequency .5, presence .5: `[0,-2,.5,0]`. Token 0's probability falls from 0.710 to 0.637 with a 1.2 HF penalty on this tiny vocab.

**Code:** (executed)
```python
import numpy as np
def hf_rep(logits, seen, pen):
    l = logits.copy()
    for t in seen: l[t] = l[t] / pen if l[t] > 0 else l[t] * pen
    return l
def openai_pen(logits, counts, freq, pres):
    return logits - freq * counts - pres * (counts > 0)
l = np.array([2.0, -1.0, 0.5, 0.0])
print(hf_rep(l, [0, 1], 1.2))                          # [ 1.6667 -1.2  0.5  0. ]
print(openai_pen(l, np.array([3, 1, 0, 0]), .5, .5))   # [ 0.  -2.   0.5  0. ]
```

**Follow-ups:**
- *Frequency vs presence?* Frequency discourages heavy reuse proportionally; presence encourages new topics regardless of count.
- *Does the penalty see the prompt?* Implementations vary (HF includes the prompt tokens in its seen set for decoder-only models); check the library.

**Common mistakes:** Subtracting or dividing without handling the sign of the logit. Using penalties for extraction, code or JSON. Raising the penalty instead of fixing the prompt or temperature. Confusing presence with frequency.


### Q21 ⭐⭐ 🟡 Is temperature 0 deterministic? What causes run-to-run differences in LLM output, and how do you get reproducibility?
**Asked at:** product, GCC, API-heavy teams, evaluation teams
**Say this first (1 line):** Temperature 0 means argmax, which is deterministic on paper, but real serving is not bit-exact, so outputs can still differ run to run; a fixed seed only controls the sampling randomness.

**Then explain:**
- **Temperature 0 = greedy argmax** (implementations usually special-case it rather than divide by zero). No sampling randomness remains.
- **Where differences come from:**
  - **Float non-associativity:** `(a+b)+c != a+(b+c)` in floating point; different reduction orders give slightly different logits.
  - **Batching:** the batch your request lands in changes kernel shapes and reduction order, so results depend on server load.
  - **Kernel choice:** different GPUs, library versions, autotuned kernels, tensor-parallel splits.
  - **MoE routing:** tiny logit changes or batch composition can flip which experts are chosen.
  - **Near-ties:** if two top logits are almost equal, a 1e-6 change flips the argmax, and then the rest of the text diverges.
- **Seed:** fixes the random draw for sampling only, not the above. Some APIs offer a seed on a best-effort basis.
- **Getting reproducibility:** temperature 0, fixed seed, pinned model version and library, batch size 1, deterministic-kernel flags, same hardware; for evaluation, run multiple times and report variance instead of assuming exactness. Log inputs and outputs.

**Example (executed):** float32 sum of the same 100k numbers forward gave `-90.825134`, reversed gave `-90.82507`, and a chunked order matched the reversed one; `(1e8 + -1e8) + 1 = 1.0` but `1e8 + (-1e8 + 1) = 0.0`. A 1e-6 wobble is harmless unless the top two logits are that close.

**Code:** (executed)
```python
import numpy as np
x = np.random.default_rng(0).standard_normal(100000).astype(np.float32)
print(x.sum(), x[::-1].sum())                      # -90.825134 -90.82507
a, b, c = np.float32(1e8), np.float32(-1e8), np.float32(1)
print((a + b) + c, a + (b + c))                    # 1.0 0.0
```

**Follow-ups:**
- *Is a self-hosted model deterministic?* Closer, if you fix hardware, batch and kernels, but not guaranteed.
- *Why does it matter for evals?* A 1-2 point difference can be noise; repeat runs.

**Common mistakes:** Saying "temperature 0 is fully deterministic". Thinking a seed fixes everything. Ignoring batching. Treating one run as a stable benchmark.


### Q22 ⭐⭐ 🟡 How does generation stop? Explain EOS, stop sequences, max tokens, finish reasons, truncation and streaming.
**Asked at:** product, GCC, API-heavy teams
**Say this first (1 line):** Generation stops when the model emits EOS, when the output hits a stop sequence, or when it reaches the max-token limit, and the API reports which one in a finish reason such as `stop` or `length`.

**Then explain:**
- **EOS:** the model learned to emit an end token; the loop stops. Finish reason is usually `stop`.
- **Stop sequences:** strings you supply (for example a next-turn marker). The server stops when the text matches and normally does not return the stop string.
- **Max tokens:** a hard cap on generated tokens. If reached first, finish reason `length`: the answer may be cut mid-sentence or mid-JSON, so check it, raise the limit or continue. Context-window overflow is a separate limit (prompt plus output).
- **Finish reason names vary** across providers; `stop` and `length` are the common ones, and some add tool-call or content-filter reasons.
- **Streaming and stop sequences:** a stop string can arrive split across chunks (`"\nUs"` then `"er:"`). The streamer must hold back any tail that could still become a stop sequence, and flush it if it turns out not to. Tokens can also split a UTF-8 character (Q15), so decode with care.
- Always set `max_tokens` for cost control and put important stops in both the template and the request.

**Example (executed):** stop sequence `"\nUser:"`, chunks `"Answer: 42\n"`, `"\nUs"`, `"er: next"`: the streamer returns `"Answer: 42\n"` and finish `stop`; with chunks `"Hi\nUs"`, `"ing it"` it holds back `"\nUs"`, sees it is not a stop, and emits `"Hi\nUsing it"`. A generator with max 3 tokens over `a b c d` returns `['a','b','c']` with `length`; one that sees `<eos>` returns `['a','b']` with `stop`.

**Code:** (executed)
```python
def stream_with_stop(chunks, stops):
    buf, out, hold = "", [], max(map(len, stops)) - 1
    for ch in chunks:
        buf += ch
        hits = [buf.find(s) for s in stops if s in buf]
        if hits:
            out.append(buf[:min(hits)]); return "".join(out), "stop"
        k = 0
        for n in range(min(hold, len(buf)), 0, -1):       # longest tail that may start a stop
            if any(s.startswith(buf[-n:]) for s in stops): k = n; break
        out.append(buf[:len(buf) - k]); buf = buf[len(buf) - k:]
    out.append(buf); return "".join(out), "eos"
print(stream_with_stop(["Answer: 42\n", "\nUs", "er: next", " question"], ["\nUser:"]))  # ('Answer: 42\n', 'stop')
print(stream_with_stop(["Hi\nUs", "ing it"], ["\nUser:"]))                               # ('Hi\nUsing it', 'eos')
```

**Follow-ups:**
- *Why did my JSON come back broken?* Likely `length`; check the finish reason before parsing.
- *Is the stop string billed?* Tokens generated before the match are generated; whether the stop text is counted varies, so check the provider.
- *Stop on a token or a string?* Strings can span tokens, so match on decoded text.

**Common mistakes:** Not checking the finish reason. Matching stop strings per chunk and missing split matches. Forgetting EOS handling in a custom loop. Leaving no `max_tokens`, so a runaway loop burns money.


### Q23 ⭐⭐ 🟡 What are logprobs? How can you use token log-probabilities for confidence, classification and calibration, and what is logit bias?
**Asked at:** product, GenAI startups, evaluation teams
**Say this first (1 line):** A logprob is the log of the probability the model gave a token, which is the log-softmax of the logits. A sequence logprob is the sum of the token logprobs, and logit bias adds a constant to chosen logits before the softmax.

**Then explain:**
- `logprob = log_softmax(logits)[token]`. It is always <= 0. `exp(logprob)` gives the probability. `top_logprobs` (API option, name varies by provider) returns the top-k alternatives at each position with their logprobs.
- **Sequence score** = sum of token logprobs = log of the joint probability. Longer sequences score lower just by being longer, so for comparing answers of different length use the mean (length-normalised) score.
- **Uses:** classification (restrict to the label tokens, compare their logprobs, so you get a score and not just a label), ranking candidate answers, spotting low-confidence tokens (hallucination hints), and evaluation (perplexity is `exp(-mean logprob)`).
- **Logit bias:** `logits[token] += b` before softmax. +b multiplies that token's odds by `e^b`; a large negative value effectively bans it. It does not touch the other tokens' relative odds.
- **Caveat:** token probabilities are not calibrated probabilities of being correct. Instruction-tuned and RLHF models tend to be over-confident, and a fluent wrong answer can have high logprobs. Calibrate on a labelled set, for example temperature scaling or a reliability curve (see B1P03-Q44), before treating them as confidence.

**Example:** For a sentiment label, ask for one token and compare `logprob("positive")` vs `logprob("negative")`. Mapping the margin to a calibrated probability with a small validation set gives a usable confidence score for routing low-confidence cases to a human.

**Code:** (executed, torch) toy model logits, 3 positions
```python
import torch
vocab = ["the", "cat", "sat", "mat", "dog"]
logits = torch.tensor([[2.0, 1.0, 0.1, 0.0, -1.0],
                       [0.2, 2.5, 0.3, 0.1, 1.0],
                       [0.0, 0.1, 3.0, 0.2, 0.3]])
tokens = torch.tensor([0, 1, 2])                       # the cat sat
logp = torch.log_softmax(logits, dim=-1)
tok_lp = logp[torch.arange(3), tokens]
print([round(x, 3) for x in tok_lp.tolist()])          # [-0.532, -0.422, -0.209]
print(round(tok_lp.sum().item(), 3), round(tok_lp.mean().item(), 3))   # -1.163 -0.388
bias = torch.tensor([0, 0, 0, 0, 5.0])                 # +5 on "dog"
print(round(logp[0].exp()[4].item(), 3),
      round(torch.log_softmax(logits[0] + bias, -1).exp()[4].item(), 3))  # 0.029 0.817
```

**Follow-ups:**
- *Why not compare raw sequence logprobs across different-length answers?* Each extra token adds a negative term, so the shorter answer wins unfairly. Use the mean, or compare on the same label set.
- *Are logprobs still available after temperature or top-p?* Providers differ: some report the raw model distribution, some the post-processed one. Check the docs before relying on them.

**Common mistakes:** Reading `exp(logprob)` as the chance the answer is right. Summing logprobs across unequal lengths. Forgetting that logit bias is applied before softmax, so it changes all probabilities through the normaliser. Using bias on multi-token words, where only the first token is affected.

### Q24 ⭐⭐ 🟡 Beam search in detail: length normalisation, cost in compute and KV memory, and why it works for translation but not open-ended chat.
**Asked at:** product, research-leaning teams
**Say this first (1 line):** Beam search keeps the k best partial sequences by cumulative logprob at every step, so it finds higher-probability sequences than greedy, at about k times the compute and KV memory. Beam 1 is exactly greedy.

**Then explain:**
- At each step, expand every beam with every candidate next token, score by cumulative logprob, keep the top k. Finished beams (EOS) are set aside.
- **Greedy can be suboptimal:** a locally best token can lead to a weak continuation. Beam looks wider, but it is still not exact search.
- **Length normalisation:** summed logprob favours short outputs. Divide by `length^alpha` (alpha 0 = none, 1 = mean logprob) or use a length penalty. Without it, beam tends to end early.
- **Cost:** k hypotheses per request means about k times the decoding FLOPs and k KV caches (shared prefix can be reused, and caches are reordered/copied as beams change). It is also deterministic and cannot sample, so no diversity unless you add diverse-beam variants.
- **Why translation yes, chat no:** translation has a narrow set of good outputs and a "most probable" target, so mode-seeking works. In open-ended generation the most probable text is often bland and repetitive, and human text is not the high-probability mode. Sampling fits better, and beam is costly at serving scale.

**Example (computed):** Hand-made table: first step A=0.6, B=0.4; after A the continuations are flat (x 0.35, y 0.35, EOS 0.30); after B, EOS has 0.9. Greedy picks A then x: probability 0.21. Beam 2 finds B then EOS: 0.36.

**Code:** (executed)
```python
import math
T = {"<s>": {"A": 0.6, "B": 0.4},
     "A": {"x": 0.35, "y": 0.35, "<eos>": 0.30},
     "B": {"<eos>": 0.9, "x": 0.1},
     "x": {"<eos>": 1.0}, "y": {"<eos>": 1.0}}
def beam(k, alpha=0.0):
    beams, done = [(["<s>"], 0.0)], []
    while beams:
        cand = [(s + [n], lp + math.log(p))
                for s, lp in beams for n, p in T[s[-1]].items()]
        cand.sort(key=lambda c: c[1], reverse=True)
        beams = []
        for s, lp in cand[:k]:
            (done if s[-1] == "<eos>" else beams).append((s, lp))
    return max(done, key=lambda c: c[1] / (len(c[0]) - 1) ** alpha)
for k in (1, 2):
    s, lp = beam(k); print(k, s[1:], round(math.exp(lp), 3))
# 1 ['A', 'x', '<eos>'] 0.21   (identical to greedy)
# 2 ['B', '<eos>'] 0.36
```

**Follow-ups:**
- *Does a bigger beam always give better output?* No. Probability goes up, quality often does not; very wide beams can give short or generic text. For translation, small beams (the 4-5 range is common) are typical.
- *Beam vs speculative decoding?* Different goals: speculative decoding speeds up sampling or greedy without changing the distribution (Part 10).

**Common mistakes:** Calling beam search exact. Forgetting length normalisation. Thinking beam adds randomness. Ignoring the k-fold KV memory.

### Q25 ⭐⭐ 🟡 How do you deduplicate a pretraining corpus (exact vs near-duplicate, MinHash/LSH)? Why does it matter?
**Asked at:** big tech, GenAI startups, research-leaning teams
**Say this first (1 line):** Exact dedup removes identical documents by hashing, near-dup dedup removes almost-identical ones using MinHash plus LSH so you avoid comparing every pair, and it matters because duplicates drive memorisation, contaminate evals and waste compute.

**Then explain:**
- **Exact:** hash each normalised document (or paragraph/line) and keep one per hash. O(n), cheap, catches copies only.
- **Near-duplicate:** boilerplate, scraped mirrors and lightly edited pages differ by a few words. Compare by **Jaccard similarity** of shingle sets (overlapping word or char n-grams): `|A∩B| / |A∪B|`.
- Exact pairwise comparison is O(n^2), impossible for billions of documents. **MinHash** compresses each document to a short signature: for each of m hash functions keep the minimum hash over its shingles. The chance two signatures agree at one position equals the Jaccard, so the fraction of agreeing positions estimates it.
- **LSH banding:** split the signature into b bands of r rows; two documents become candidates if any band matches fully. Candidate probability is `1-(1-s^r)^b`, an S-curve around a threshold. Only candidates are checked or clustered.
- **Why it matters:** repeated text is memorised and regurgitated much more (Q31), duplicates between train and benchmarks inflate scores (Q30), and repeated data wastes tokens. Research such as D4 and SoftDedup (as described in sources I have seen, not verified in detail) goes beyond dedup to select or down-weight redundant data, with reported gains at roughly 6.7B scale.
- Trade-off: aggressive dedup can remove useful repetition (licences, quotes); choose threshold, granularity (doc, paragraph, substring) by ablation.

**Example (computed):** Two 18-word sentences share most 3-word shingles: exact Jaccard 0.700. MinHash estimates: 0.938 with 16 hashes (noisy), 0.703 with 128, 0.709 with 1024. With 16 bands of 8 rows, a pair at Jaccard 0.5 becomes a candidate with probability 0.061, at 0.8 with 0.947.

**Code:** (executed, plain Python)
```python
import hashlib
def shingles(t, k=3):
    w = t.split(); return {" ".join(w[i:i+k]) for i in range(len(w)-k+1)}
def h(s, seed): return int(hashlib.md5(f"{seed}|{s}".encode()).hexdigest()[:8], 16)
def minhash(sh, n=128): return [min(h(s, i) for s in sh) for i in range(n)]
def est(a, b): return sum(x == y for x, y in zip(a, b)) / len(a)
a = "the quick brown fox jumps over the lazy dog near the river bank today and then runs home fast"
b = "the quick brown fox jumps over the lazy dog near the river bank today and then walks home slowly"
A, B = shingles(a), shingles(b)
print(round(len(A & B)/len(A | B), 3))                 # 0.7
for n in (16, 128, 1024):
    print(n, round(est(minhash(A, n), minhash(B, n)), 3))   # 0.938, 0.703, 0.709
for s in (0.3, 0.5, 0.8, 0.9):
    print(s, round(1-(1-s**8)**16, 3))                 # 0.001 0.061 0.947 1.0
```

**Follow-ups:**
- *Error of the estimate?* It is an average of m coin flips, so std is about `sqrt(s(1-s)/m)`; more hashes, less noise.
- *Substring dedup?* Suffix arrays find repeated long spans inside documents; exact-substring dedup is a separate step from document-level.

**Common mistakes:** Only doing exact-hash dedup. Comparing all pairs. Using too few hashes. Dedup after tokenising/lowercasing inconsistently so near-copies hash differently. Forgetting to dedup train against eval sets.

### Q26 ⭐⭐ 🟡 What does a standard LLM pretraining optimisation recipe look like (AdamW settings, warmup, cosine or WSD decay, weight decay, gradient clipping), and why each piece?
**Asked at:** big tech, GenAI startups, research-leaning teams
**Say this first (1 line):** A common recipe is AdamW with decoupled weight decay, a short linear warmup, a decay to a fraction of peak LR (cosine, or warmup-stable-decay), gradient clipping at global norm 1.0, and no weight decay on norms, biases and embeddings. These are typical reported community practice, not universal laws.

**Then explain:** (values are typical, vary by lab and scale)
- **AdamW:** weight decay is applied directly to weights, separate from the adaptive gradient step (decoupled), so it behaves as real regularisation. Typical decay about 0.1. **beta1 0.9, beta2 about 0.95** (lower than the 0.999 default, so the second-moment estimate adapts faster and large-batch spikes are less sticky; commonly reported for LLMs). **eps small** (1e-8 to 1e-5; matters more in low precision).
- **Warmup** (about 1-10% of steps, sometimes a fixed few thousand steps): Adam's moment estimates are noisy early and the loss surface is sharp at init, so ramp LR up from near zero to avoid early divergence.
- **Decay:** cosine goes smoothly from peak to about 10% of peak, but you must know the total steps in advance. **WSD** (warmup, long stable plateau, short final decay) lets you stop or branch from the plateau and decay later, which suits continued training and scaling experiments. Both reach similar final loss in reports I have seen; treat that as reported, not guaranteed.
- **Gradient clipping** at global norm 1.0 caps the update when a bad batch produces a huge gradient. It is a safety net against spikes (Q29, Part 1 Q44).
- **No decay on** RMSNorm/LayerNorm gains, biases and often embeddings: they are scale parameters, and shrinking them hurts rather than regularises.
- General LR schedule background is in B1P08-Q14; mixed precision in Q27.

**Example:** 1,000-step toy run, peak 3e-4, 2% warmup, floor 10% of peak. Cosine is already 1.69e-4 at the midpoint, while WSD stays at 3e-4 until step 900 and then drops linearly to 3e-5.

**Code:** (executed)
```python
import math
def lr_at(step, total, peak=3e-4, warmup_frac=0.02, min_ratio=0.1, kind="cosine", decay_frac=0.1):
    w = int(total * warmup_frac); lo = peak * min_ratio
    if step < w: return peak * (step + 1) / w
    if kind == "cosine":
        p = (step - w) / (total - w)
        return lo + 0.5 * (peak - lo) * (1 + math.cos(math.pi * p))
    d0 = int(total * (1 - decay_frac))
    if step < d0: return peak
    return peak + (lo - peak) * (step - d0) / (total - d0)
for s in [0, 19, 250, 500, 900, 950, 999]:
    print(s, f"{lr_at(s,1000):.2e}", f"{lr_at(s,1000,kind='wsd'):.2e}")
# 0 1.50e-05 1.50e-05 | 19 3.00e-04 3.00e-04 | 250 2.65e-04 3.00e-04 | 500 1.69e-04 3.00e-04
# 900 3.69e-05 3.00e-04 | 950 3.17e-05 1.65e-04 | 999 3.00e-05 3.27e-05
```
Param groups in PyTorch: `AdamW([{"params": decay, "weight_decay": 0.1}, {"params": no_decay, "weight_decay": 0.0}], betas=(0.9, 0.95))` (not executed: fragment, needs a model).

**Follow-ups:**
- *Why beta2 0.95 and not 0.999?* With 0.999 the second-moment average remembers a window of about 1,000 steps and reacts slowly to gradient-scale changes, which is associated with loss spikes; 0.95 is about 20 steps. Commonly reported, not proven universal.
- *Why does the LR need to scale down with model size?* Larger models are usually trained at smaller peak LR; tune on small proxies.

**Common mistakes:** Using L2 regularisation inside Adam and calling it weight decay. Decaying norm and bias parameters. No warmup. Quoting one recipe as the only correct one. Picking cosine without fixing total steps.

### Q27 ⭐⭐ 🟡 Why is bf16 preferred over fp16 for LLM pretraining? Cover exponent range vs mantissa, fp32 master weights and optimizer states, which ops stay in fp32, and what FP8 changes.
**Asked at:** big tech, product, GenAI startups
**Say this first (1 line):** bf16 keeps fp32's exponent range (8 bits) but has only 7 mantissa bits, while fp16 has a 5-bit exponent and 10 mantissa bits. LLM training cares more about range than precision, so bf16 avoids overflow and underflow and needs no loss scaling.

**Then explain:**
| Format | Exponent | Mantissa | Max value | Relative step (eps) |
|---|---|---|---|---|
| fp32 | 8 | 23 | ~3.4e38 | ~1.2e-7 |
| bf16 | 8 | 7 | ~3.4e38 | 0.0078 |
| fp16 | 5 | 10 | 65,504 | 0.00098 |
- fp16 overflows past 65,504 and flushes tiny gradients to zero, so it needs **loss scaling** (multiply the loss, unscale grads, skip steps on inf/NaN). bf16 does not.
- bf16 is coarser (about 2-3 significant digits), so small updates get rounded away. That is why training keeps **fp32 master weights** and **fp32 Adam moments**, does the update in fp32, then casts a bf16 copy for forward and backward.
- Typical **fp32 ops** (common practice): softmax and log-softmax/loss, normalisation statistics, reductions, optimizer math, sometimes MoE router logits. Matmul hardware accumulates in higher precision internally.
- **FP8** (8-bit floats, E4M3/E5M2 variants) can raise matmul throughput and cut memory traffic on supporting GPUs, but needs per-tensor or per-block scaling and care. Use in large runs is reported, but recipes are less standard than bf16, so hedge this in an interview.
- Mixed precision basics: B1P08-Q40.

**Example (computed):** Adding 1e-4 a thousand times to 1.0: fp32 gives 1.1000; bf16 and fp16 both stay at 1.0 because each increment is below half the spacing between neighbours. With pure low-precision weights the model would stop learning, hence fp32 master weights.

**Code:** (executed, torch)
```python
import torch
x = torch.tensor(70000.0)
print(x.half().item(), x.bfloat16().item())            # inf 70144.0
print(torch.finfo(torch.float16).max, torch.finfo(torch.bfloat16).max)  # 65504.0 3.389e+38
print(torch.tensor(1e-8).half().item(), torch.tensor(1e-8).bfloat16().item())  # 0.0 1.0011717677116394e-08
for dt in (torch.float16, torch.bfloat16, torch.float32):
    w = torch.tensor(1.0, dtype=dt)
    for _ in range(1000): w = w + torch.tensor(1e-4, dtype=dt)
    print(dt, w.item())                                # 1.0, 1.0, 1.1000165939331055
```
bf16 shows 70,144 for 70,000: representable range, but rounded.

**Follow-ups:**
- *Memory per parameter with Adam in mixed precision?* Commonly 2 (bf16 weights) + 2 (grads) + 4 (fp32 master) + 8 (Adam states) = 16 bytes; see Q34.
- *When is fp16 still fine?* Inference, and older GPUs without bf16 support.

**Common mistakes:** Saying bf16 is more precise. Forgetting master weights. Saying bf16 never needs care (softmax, norms, long accumulations still do). Claiming FP8 is routine without caveats.

### Q28 ⭐⭐ 🟡 How do you choose batch size in LLM pretraining (tokens per step, gradient accumulation, critical batch size, learning-rate scaling)?
**Asked at:** big tech, GenAI startups, research-leaning teams
**Say this first (1 line):** Batch size in pretraining is counted in tokens per step (sequences x sequence length). Pick it large enough to use the hardware and keep gradient noise low, but not beyond the critical batch size, where more tokens per step stop reducing the steps you need.

**Then explain:**
- **Tokens per step = batch x seq_len.** For example 1,024 sequences x 4,096 = 4,194,304 tokens (about 4M). Large runs commonly use millions of tokens per step, often ramped up during training.
- **Gradient accumulation:** run several micro-batches, add their gradients, then step once. With a mean loss, divide each micro-loss by the number of accumulation steps; then the gradient equals the big-batch gradient exactly (up to float error). It trades time for memory, not tokens for free.
- **Critical batch size / gradient noise scale** (from the gradient-noise-scale line of work, e.g. McCandlish et al.; I am citing from memory): small batch means noisy gradients and more steps; past a point, a bigger batch gives almost no fewer steps, only more compute per step. The critical size tends to grow as loss falls, so late training tolerates larger batches.
- **LR scaling** with batch size (linear or square-root rules) is a heuristic that works over limited ranges; retune and warm up. Adam favours square-root-like scaling in some reports. Do not present either as a law.
- Practical constraints: GPU count and data-parallel degree, memory (micro-batch), step-time/throughput, and keeping enough steps for the schedule (too big a batch means too few updates in a fixed token budget).
- Related: B1P08-Q14 for LR schedules.

**Example (computed):** 4 micro-batches of 8 sequences, each loss divided by 4, give a gradient identical to one batch of 32 (`allclose` True). Forgetting the division makes the gradient exactly 4.0x too large.

**Code:** (executed, torch)
```python
import torch
torch.manual_seed(0)
X, y = torch.randn(32, 8), torch.randn(32)
w = torch.randn(8, requires_grad=True)
(((X @ w - y) ** 2).mean()).backward(); g_big = w.grad.clone(); w.grad = None
for xb, yb in zip(X.chunk(4), y.chunk(4)):
    (((xb @ w - yb) ** 2).mean() / 4).backward()
print(torch.allclose(w.grad, g_big, atol=1e-6))        # True
print(1024 * 4096)                                      # 4194304 tokens/step
```
Equal micro-batch sizes are assumed. With padding or variable valid-token counts, normalise by total valid tokens instead.

**Follow-ups:**
- *Does accumulation change batch norm or dropout?* Batch norm statistics differ per micro-batch (rare in LLMs, which use layer/RMS norm). Dropout is fine.
- *How would you measure the critical batch size?* Estimate gradient noise scale from gradient norms at two batch sizes, or run short sweeps; a heuristic, not exact.

**Common mistakes:** Quoting batch size in sequences without sequence length. Not dividing by accumulation steps. Believing the LR scaling rule is exact. Assuming bigger batch is always faster to a given loss.⭐⭐ 🟡 How do you read a pretraining loss curve? What do spikes, divergence, plateaus and a train/validation gap tell you, and what would you do?
**Asked at:** big tech, GenAI startups, research-leaning teams
**Say this first (1 line):** A healthy pretraining curve falls smoothly on a log-log-like trend; I watch loss against tokens together with gradient norm, update size and per-domain validation loss, and I treat spikes and divergence as data or optimiser-stability problems to fix with skipped batches, lower LR or a restart from an earlier checkpoint.

**Then explain:**
- **What to plot:** train loss vs tokens (not wall-clock), validation loss on held-out sets per domain (web, code, math, languages), **global grad norm**, LR, and loss-scale/NaN counters. Compare against smaller proxy runs (loss curves in general: B1P08-Q16).
- **Spike (sudden jump then recovery):** often a bad data batch, or Adam's second moment lagging a gradient burst. Check grad norm and which batch. Mitigations: gradient clipping (already on), skip the offending batch, lower LR or lengthen warmup, lower beta2 (Q26), and if the loss does not recover, **restart from an earlier checkpoint** with those batches skipped or reshuffled.
- **Divergence (loss climbs or NaN):** stop, roll back to a stable checkpoint, then reduce peak LR, check precision (Q27), and look for stability tricks such as QK-norm or z-loss (Part 1 Q44).
- **Plateau:** may be normal mid-run, or LR too low/decayed early, data stuck in one domain, or a bug (frozen layers, bad masking). Check per-domain curves.
- **Train/val gap:** in single-epoch pretraining on fresh data the gap should be tiny. A gap means repeated data, duplicates (Q25) or val leakage. A *falling train loss with flat val* is overfitting on repeated epochs.
- Stable-looking loss can still hide a degraded domain, so downstream evals every N steps matter.

**Example (synthetic, not a real run):** A made-up curve `2.0 + 6*step^-0.35` plus noise, with a spike injected at steps 1,201-1,210. A rolling median/MAD detector flags exactly steps 1,201 to 1,210 (10 steps). In real runs you would then look up the batch ids for those steps, and grad norm to see if clipping engaged.

**Code:** (executed, synthetic data)
```python
import numpy as np
rng = np.random.default_rng(0)
steps = np.arange(1, 2001)
loss = 2.0 + 6*steps**-0.35 + rng.normal(0, 0.01, steps.size)
loss[1200:1210] += 1.5 * np.exp(-np.arange(10)/4)        # injected spike
def flag_spikes(l, win=50, k=6):
    out = []
    for i in range(win, len(l)):
        base = l[i-win:i]; med = np.median(base); mad = np.median(abs(base-med))*1.4826 + 1e-6
        if l[i] > med + k*mad: out.append(i+1)
    return out
f = flag_spikes(loss); print(f[0], f[-1], len(f))       # 1201 1210 10
```

**Follow-ups:**
- *Do you always roll back?* If it recovers quickly and grad norm returns to normal, continue; if the new level is persistently higher, roll back.
- *Why plot against tokens?* Runs with different batch sizes or restarts become comparable.

**Common mistakes:** Looking only at the training loss. Ignoring grad norm. Raising LR to escape a plateau. Treating every spike as divergence. Not logging which data produced the spike.

### Q30 ⭐⭐ 🟡 How do you decontaminate a pretraining corpus against benchmarks (n-gram overlap, canary strings, dynamic test sets) and detect contamination in a finished model?
**Asked at:** product, evaluation teams, research-leaning teams
**Say this first (1 line):** Decontamination removes training text that overlaps benchmark items, mostly by n-gram matching against the test sets before training, backed by canary strings and fresh or time-split benchmarks; detecting contamination after the fact is much harder and unreliable.

**Then explain:**
- **N-gram overlap:** build the set of n-grams of every benchmark question and answer; drop or flag any training document sharing one (or more than a threshold). A 13-gram window is a commonly used heuristic; the exact n, normalisation and whether you drop the doc or just the span vary by team. Small n gives false positives on common phrases, large n misses paraphrases.
- **Limits:** misses paraphrases, translations and reformatted items, and benchmark text that reached the web in many forms. Also check for solutions and discussion posts, not just the questions. Test sets often leak through duplicated copies on forums (see dedup, Q25).
- **Canary strings:** a unique marker string embedded in a benchmark file, to tell crawlers to exclude it and to let you test whether a model has seen it. It helps only if people respect it.
- **Dynamic / time-split benchmarks:** use questions written after the training cutoff, or refresh them regularly, so they cannot have been seen.
- **Detecting contamination in a finished model:** compare perplexity or accuracy on the original vs a paraphrased/shuffled version, check whether the model reproduces the benchmark verbatim from a prefix, or membership-inference style tests. Per the research I know of (a perplexity-estimation paper and a later study reporting such methods near random for seen vs unseen), perplexity-based detection is weak and should be treated as a hint, not proof.
- Also report a clean-subset score next to the full score. For the evaluation-side view, see B1P01-Q34.

**Example (computed):** Benchmark item of 15 words. A training doc containing it verbatim shares all 3 of its 13-grams (3/3), and 11/11 of its 5-grams. A paraphrase ("name the capital of france and the river that runs through paris") shares 0/3 13-grams and 1/11 5-grams, so it slips through. That is why n-gram decontamination is necessary but not sufficient.

**Code:** (executed)
```python
def ngrams(t, n):
    w = t.lower().split(); return {" ".join(w[i:i+n]) for i in range(len(w)-n+1)}
bench = "what is the capital of france and which river flows through its capital city paris"
docs = {"leak": "quiz dump: what is the capital of france and which river flows through its capital city paris answer seine",
        "para": "name the capital of france and the river that runs through paris",
        "clean": "gradient descent updates parameters in the direction of the negative gradient of the loss"}
for n in (13, 5):
    b = ngrams(bench, n)
    for name, d in docs.items():
        print(n, name, len(b & ngrams(d, n)), "/", len(b))
# 13: leak 3/3, para 0/3, clean 0/3 ; 5: leak 11/11, para 1/11, clean 0/11
```

**Follow-ups:**
- *You find 5% of a benchmark leaked. What do you do?* Report both full and decontaminated scores, remove the leaked items for headline numbers, and fix the pipeline.
- *Is a high benchmark score proof of contamination?* No; contamination needs evidence such as verbatim reproduction.

**Common mistakes:** Only checking exact string match. Decontaminating the questions but not answers or solutions. Thinking perplexity tests settle it. Forgetting that the same leak may exist in fine-tuning data.

### Q31 ⭐⭐ 🟡 Why do LLMs memorise and regurgitate training data? What makes it worse, and how do you reduce privacy and copyright risk?
**Asked at:** product, GCC, regulated-industry teams
**Say this first (1 line):** LLMs memorise because they are trained to predict training text exactly and have a lot of capacity; text that is repeated, distinctive or long is the most likely to be reproduced, and the main defences are dedup, data filtering, and output-side controls, with differential privacy as a costly option.

**Then explain:**
- **Why it happens:** the loss rewards assigning high probability to the exact next token. For common facts that is generalisation; for rare unique strings (a phone number, a licence text) it can only be done by memorising.
- **What makes it worse:** duplicated data (Q25), larger models, more training epochs/tokens on the same text, longer prompts matching a training prefix, and sequences that are unusual enough to be unique. Published work reports all of these trends; I will not quote exact rates.
- **Extraction attacks exist:** prompt the model (sometimes with a prefix of a known document, or repeated odd inputs) and check whether it emits verbatim training text. So "it is only learning patterns" is not a safe assumption.
- **Mitigations:**
  - Dedup and filter the data; remove or mask **PII** (emails, phone numbers, IDs) and licence-restricted content before training.
  - **Differential privacy** (DP-SGD) gives formal guarantees but costs accuracy and compute, and is hard to apply at LLM scale.
  - **Output filters:** block verbatim long matches to a training-set index (n-gram/Bloom filter), PII detectors, refusal tuning.
  - Fewer epochs on the same data; red-team with extraction probes; access controls and logging for fine-tuned models trained on private data.
- Memorisation is also an evaluation issue (Q30) and a legal one for copyright; treat risk assessment with legal teams, not as a pure ML matter.

**Example:** A model fine-tuned on support tickets containing customer emails. Fine-tune with many epochs on a small set and it can repeat an email when prompted with the ticket start. Fix: scrub PII first, dedup, cap epochs, and test with prefix-completion probes before release.

**Code:** (not executed: conceptual; a runnable duplicate-count or n-gram check is shown in Q25 and Q30)

**Follow-ups:**
- *How would you measure memorisation?* Give the model a prefix of a training sequence and check if greedy decoding reproduces the continuation exactly; report the fraction for sampled training texts vs held-out ones.
- *Does RLHF remove memorisation?* No, it changes behaviour, not what is stored; extraction can still succeed in some settings.

**Common mistakes:** Saying memorisation only matters for small data. Relying on a refusal prompt as the only control. Promising DP without mentioning cost. Quoting invented percentages.

### Q32 ⭐⭐ 🟡 Why do modern models train far beyond the Chinchilla-optimal token count (e.g. an 8B model on ~15T tokens)? What is inference-aware scaling?
**Asked at:** big tech, product, GenAI startups
**Say this first (1 line):** Chinchilla minimises training compute for a given loss, but real teams also pay to serve the model for months, so they overtrain a smaller model on far more tokens because a small model is cheaper at every inference call.

**Then explain:**
- **Chinchilla result:** about 20 training tokens per parameter was compute-optimal in that study (a refit attempt puts the optimum somewhat lower, so treat 20 as approximate and contested). It ignores inference cost.
- **Reported figure:** Meta reported Llama 3 8B trained on about 15T tokens. That is 15e12 / 8e9 = about 1,875 tokens per parameter, roughly 90x the Chinchilla ratio. Reported (from memory): loss kept improving with more tokens, with diminishing returns.
- **Inference-aware view:** total cost = training (about `6ND` FLOPs) + serving (about `2N` FLOPs per token x lifetime tokens). If traffic is high, serving dominates, so cutting N matters more than saving training FLOPs. You then train a smaller N on bigger D until the quality target is met.
- Other reasons: a smaller model fits one GPU, has lower latency, and can run on-device or at higher batch size.
- Limits: high-quality data runs out, repeated epochs give diminishing gains, and returns per extra token shrink.

**Example (toy, illustrative, assumed numbers):** Assume equal quality (the key assumption) for a 70B model on 1.4T tokens and an 8B model on 15T. Train FLOPs: 5.88e23 vs 7.20e23. Serving 2e15 lifetime tokens: 2.80e26 vs 3.20e25 FLOPs. Totals 2.81e26 vs 3.27e25, so the small model is about 8.6x cheaper overall. Break-even is about 1.06e12 served tokens. In reality an 8B will not match a 70B in quality, so this shows the economics only, not a claim about actual models.

**Code:** (executed; illustrative assumptions)
```python
N, D = 8e9, 15e12
print(D/N, 20*N/1e12)                  # 1875.0 0.16  (tokens/param; Chinchilla-style D in T tokens)
serve = 2e15                            # ASSUMED lifetime served tokens; equal quality assumed
for name, n, d in [("70B @1.4T", 70e9, 1.4e12), ("8B @15T", 8e9, 15e12)]:
    train, sv = 6*n*d, 2*n*serve
    print(name, f"train {train:.2e} serve {sv:.2e} total {train+sv:.2e}")
be = (6*8e9*15e12 - 6*70e9*1.4e12) / (2*(70e9-8e9))
print(f"break-even served tokens {be:.2e}")   # 1.06e+12
```

**Follow-ups:**
- *Is the scaling law wrong then?* No; it answers a different question (minimum training compute). Inference-aware scaling changes the objective.
- *Is there a limit to overtraining?* Yes: data quality and quantity, and diminishing loss gains per token.

**Common mistakes:** Saying Chinchilla is "wrong" instead of optimising a different cost. Quoting 20:1 as exact. Forgetting serving cost. Presenting the toy numbers as real.

### Q33 ⭐⭐ 🟡 Estimate the cost of pretraining a 7B model on 2T tokens: FLOPs, GPU-hours, model FLOPs utilisation (MFU) and rough dollars.
**Asked at:** big tech, product, infra/platform teams
**Say this first (1 line):** Training FLOPs are about 6 x parameters x tokens, which is 8.4e22 for 7B on 2T tokens; divide by what the GPUs really deliver (peak x MFU) to get GPU-hours, then multiply by price. On illustrative assumptions that is roughly 59k GPU-hours and about $120k of raw compute at 40% MFU.

**Then explain:**
- **FLOPs = 6ND:** 2ND for the forward pass and 4ND for backward (a standard approximation; ignores attention-over-context terms and recompute).
- **GPU-hours = FLOPs / (peak FLOP/s x MFU x 3600).** **MFU** (model FLOPs utilisation) = useful model FLOPs achieved / hardware peak. It is below 100% because of memory-bound ops, communication, data loading and bubbles. Reported large-run values are often in the 30-55% range; treat as ballpark.
- **All hardware numbers below are assumptions:** peak 989e12 FLOP/s (H100-class bf16 dense, from vendor spec as I recall it) and $2.00 per GPU-hour. Real prices vary widely by provider and contract.
- **Sensitivity:** cost is inversely proportional to MFU, so a poor setup costs much more.
- This is only the final run. Real budgets add failed runs, ablations, scaling-law experiments, data processing, evals and staff, often multiples of the final run. Also compare memory needs (Q34).

**Example (computed):** 6 x 7e9 x 2e12 = 8.4e22 FLOPs.

| MFU | GPU-hours | Cost at $2/GPU-hr | Days on 1,024 GPUs |
|---|---|---|---|
| 30% | 78,643 | $157,286 | 3.2 |
| 40% | 58,982 | $117,964 | 2.4 |
| 50% | 47,186 | $94,371 | 1.9 |

**Code:** (executed)
```python
N, D = 7e9, 2e12
F = 6*N*D; print(f"{F:.2e}")                      # 8.40e+22
peak, price = 989e12, 2.0                          # ASSUMPTIONS, not measurements
for mfu in (0.3, 0.4, 0.5):
    gh = F/(peak*mfu*3600)
    print(f"{mfu:.0%} {gh:,.0f} GPU-h ${gh*price:,.0f} {gh/1024/24:.1f} days@1024")
# 30% 78,643 $157,286 3.2 | 40% 58,982 $117,964 2.4 | 50% 47,186 $94,371 1.9
```

**Follow-ups:**
- *Why does a real company spend more?* Experiments, restarts, failures, data and evals, plus higher-priced capacity.
- *What would change the estimate most?* MFU and token count, then GPU price; MoE or longer context change the FLOPs formula.

**Common mistakes:** Using peak FLOPs with no MFU. Using sparse (2x) peak numbers for dense training. Forgetting the factor 6 vs 2. Presenting the dollar figure as the total cost of building a model.

### Q34 ⭐⭐ 🔴 Live maths: how much GPU memory does training a 7B model need (weights, gradients, Adam states, activations)? Explain data, tensor and pipeline parallelism and ZeRO/FSDP at a high level.
**Asked at:** big tech, infra/platform teams, GenAI startups
**Say this first (1 line):** With mixed-precision Adam it is about 16 bytes per parameter before activations, so a 7B model needs roughly 112 GB just for weights, gradients and optimizer state. That does not fit on one 80 GB GPU, so we shard it (ZeRO/FSDP) and/or split the model (tensor/pipeline parallelism). Activations come on top and depend on batch size, sequence length and checkpointing.

**Then explain:**

| Item | Bytes/param | 7B model |
|---|---|---|
| bf16 weights | 2 | 14 GB |
| bf16 gradients | 2 | 14 GB |
| fp32 master weights | 4 | 28 GB |
| Adam m (fp32) | 4 | 28 GB |
| Adam v (fp32) | 4 | 28 GB |
| **Total** | **16** | **112 GB** |

- This is a common accounting, not a law. Some setups keep fp32 gradients or skip the master copy, so it can be 12 to 20 bytes per parameter.
- **Activations** are extra: they grow with batch x sequence x layers x hidden size. Activation (gradient) checkpointing recomputes them in the backward pass, trading about one extra forward pass of compute for much less memory. I would not quote a single number; I would measure.
- **Data parallelism (DP):** every GPU holds a full copy and sees different data; gradients are averaged (all-reduce). Easy, but memory per GPU does not shrink.
- **ZeRO / FSDP:** remove the DP redundancy by sharding. ZeRO-1 shards optimizer state, ZeRO-2 also gradients, ZeRO-3 (PyTorch FSDP is the same idea) also the weights, gathered layer by layer just in time. Cost: extra communication.
- **Tensor parallelism (TP):** split each big matrix multiply across GPUs (inside a layer). Needs fast links, so usually inside one node.
- **Pipeline parallelism (PP):** put different layers on different GPUs and stream micro-batches through. Cheap communication, but idle "bubbles" at pipeline start/end.
- Real large runs combine them (3D parallelism). Generic distributed-training depth is in Book 4.

**Example:** on 8 GPUs with 80 GB each (an example size), plain DP needs 112 GB per GPU: it does not fit. ZeRO-3/FSDP gives about 14 GB per GPU for states, leaving room for activations.

**Code:** (executed)
```python
N = 7e9                      # parameters
GB = 1e9
parts = {"bf16 weights": 2, "bf16 grads": 2, "fp32 master weights": 4,
         "Adam m (fp32)": 4, "Adam v (fp32)": 4}
total = sum(parts.values())
for k, b in parts.items():
    print(f"{k:20s} {b} B/param -> {N*b/GB:5.0f} GB")
print(f"total {total} B/param -> {N*total/GB:.0f} GB, before activations")

d = 8                        # data-parallel GPUs
opt, grad, w = 12, 2, 2      # bytes/param: optimizer state (master+m+v), grads, weights
print("plain DP      :", N*(w+grad+opt)/GB, "GB per GPU")
print("ZeRO-1 (opt)  :", N*(w+grad+opt/d)/GB)
print("ZeRO-2 (+grad):", N*(w+(grad+opt)/d)/GB)
print("ZeRO-3 / FSDP :", N*(w+grad+opt)/d/GB)
# output: total 16 B/param -> 112 GB; DP 112.0, ZeRO-1 38.5, ZeRO-2 26.25, ZeRO-3 14.0 GB per GPU
```
These are idealised numbers: they ignore activations, communication buffers, fragmentation and uneven sharding.

**Follow-ups:**
- *Why fp32 master weights?* Small updates (lr x gradient) can be below bf16 resolution and vanish; the fp32 copy accumulates them. See Q27 for precision.
- *Why not always ZeRO-3?* Every layer needs an all-gather in forward and backward, so on slow interconnects it can be slower than ZeRO-1/2.
- *Inference memory?* Roughly 2 bytes/param for bf16 weights (14 GB for 7B) plus KV cache.

**Common mistakes:** Saying "7B x 2 bytes = 14 GB" for training (that is only weights). Forgetting the fp32 optimizer state, which is the biggest part. Ignoring activations. Thinking DP reduces per-GPU memory.

### Q35 ⭐ 🟡 AI code review: this LLM-written sampling function has bugs (top-p off-by-one, wrong order of temperature and softmax, no renormalisation, mutated logits). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
**Say this first (1 line):** There are five bugs. Temperature must divide the logits before softmax, the nucleus must include the token that crosses the threshold, the kept probabilities must be renormalised, the caller's logits must not be mutated, and everything must work per row of the batch. I would prove each one with a tiny case, then test the fix against an independent reference.

**Then explain:**

| # | Bug | Effect | Evidence from my run |
|---|---|---|---|
| 1 | Cut where `cum < top_p` is true, so the token that crosses `top_p` is dropped | Nucleus too small; sampling is more greedy than asked | probs 0.5/0.3/0.15/0.05, top_p 0.7: buggy keeps 1 token, correct nucleus is 2 (0.5+0.3=0.8 >= 0.7) |
| 2 | Softmax first, then divide probabilities by temperature | Not a distribution (sums to 2.0 at T=0.5) and the shape never sharpens or flattens properly | right `[0.6849, 0.2466, 0.0616, 0.0068]`, wrong `[1.0, 0.6, 0.3, 0.1]` |
| 3 | No renormalisation after truncation | `multinomial` happens to rescale, but your own probability maths, logging or logprobs are wrong | kept mass 0.8 becomes `[0.625, 0.375]` after renormalising |
| 4 | Mutates the caller's `logits` | Same tensor reused (for logprobs, or a second sampler) is silently corrupted | caller tensor changed: True (fixed: unchanged) |
| 5 | One cutoff count for the whole batch | Rows with different shapes of distribution get the wrong cut | per-row counts `[2, 4]`, buggy single value 6 |

- In the buggy code, bug 4 is shown with `logits.zero_()` as a stand-in for any in-place edit (e.g. `logits /= temperature`). The function's return is a placeholder, since the point is the logic.
- Fix pattern for the nucleus: keep a token if the probability mass **before** it is below `top_p` (`cum - p < top_p`), and always keep the top token.

**Code:** (executed, torch, standalone)
```python
import torch

def buggy_sample(logits, temperature=0.8, top_p=0.9):      # logits: (B, V)
    probs = torch.softmax(logits, dim=-1)                   # BUG 2: softmax before temperature
    probs = probs / temperature                             #        (divides probabilities)
    sorted_p, idx = torch.sort(probs, descending=True)      # (sorts along last dim: ok)
    cum = torch.cumsum(sorted_p, dim=-1)
    cutoff = int((cum < top_p).sum())                       # BUG 5: one count for the whole batch
    sorted_p[:, cutoff:] = 0                                # BUG 1: off-by-one, drops crossing token
                                                            # BUG 3: no renormalisation
    logits.zero_()                                          # BUG 4: stands in for in-place edits
    return idx[:, 0]                                        #        (placeholder, not the point)

def sample_top_p(logits, temperature=0.8, top_p=0.9, generator=None):
    scaled = logits / temperature                           # out-of-place, on logits
    probs = torch.softmax(scaled, dim=-1)
    sorted_p, idx = torch.sort(probs, dim=-1, descending=True)
    cum = torch.cumsum(sorted_p, dim=-1)
    keep = (cum - sorted_p) < top_p                         # mass BEFORE token < top_p
    keep[:, 0] = True                                       # never empty
    sorted_p = sorted_p * keep
    sorted_p = sorted_p / sorted_p.sum(dim=-1, keepdim=True)
    choice = torch.multinomial(sorted_p, 1, generator=generator)
    return idx.gather(-1, choice).squeeze(-1)

def nucleus_ref(row, temperature, top_p):                   # independent pure-python reference
    import math
    z = [v / temperature for v in row]; m = max(z)
    e = [math.exp(v - m) for v in z]; s = sum(e); p = [v / s for v in e]
    kept, mass = [], 0.0
    for i in sorted(range(len(p)), key=lambda i: -p[i]):
        kept.append(i); mass += p[i]
        if mass >= top_p: break
    tot = sum(p[i] for i in kept)
    return [p[i] / tot if i in kept else 0.0 for i in range(len(p))]

torch.manual_seed(0)
l = torch.log(torch.tensor([[0.5, 0.3, 0.15, 0.05]]))
cum = torch.cumsum(torch.softmax(l, -1), -1)
print("Bug1 cum:", [round(v, 2) for v in cum[0].tolist()], "| top_p=0.7: buggy keeps", int((cum < 0.7).sum()), "token, correct nucleus has 2")
print("Bug2 right:", [round(v, 4) for v in torch.softmax(l / 0.5, -1)[0].tolist()],
      "| wrong:", [round(v, 4) for v in (torch.softmax(l, -1) / 0.5)[0].tolist()], "(sums to 2.0)")
print("Bug3 kept mass 0.8 -> renormalised", (torch.tensor([0.5, 0.3]) / 0.8).tolist())
x = torch.randn(2, 5); x0 = x.clone(); buggy_sample(x)
print("Bug4 buggy changed caller logits:", not torch.equal(x, x0))
x = torch.randn(2, 5); x0 = x.clone(); sample_top_p(x)
print("     fixed leaves them alone:", torch.equal(x, x0))
b = torch.tensor([[3., 0, 0, 0, 0], [1., 1, 1, 1, 1]])
cm = torch.cumsum(torch.sort(torch.softmax(b, -1), descending=True)[0], -1)
print("Bug5 per-row counts:", (cm < 0.9).sum(-1).tolist(), "| buggy single scalar:", int((cm < 0.9).sum()))

B, V, N = 3, 8, 40000
logits = torch.randn(B, V) * 2
g = torch.Generator().manual_seed(1)
s = sample_top_p(logits.repeat(N, 1), 0.8, 0.9, generator=g).view(N, B)
for r in range(B):
    emp = torch.bincount(s[:, r], minlength=V).float() / N
    ref = torch.tensor(nucleus_ref(logits[r].tolist(), 0.8, 0.9))
    print(f"row {r}: max|empirical-reference| = {(emp-ref).abs().max():.4f}, sampled outside nucleus: {bool(((emp>0)&(ref==0)).any())}")
# last lines of output: row 0: 0.0037, row 1: 0.0023, row 2: 0.0011; never sampled outside the nucleus
```
Empirical frequencies from 40,000 draws per row match the reference to within 0.004, and no token outside the nucleus was ever sampled.

**Example:** with a peaked distribution and `top_p=0.9`, bug 1 can leave a single token in the nucleus, so the "sampling" call is secretly greedy, and nobody notices because output still looks fluent.

**Follow-ups:**
- *Why not just test shapes?* All five bugs keep shapes valid and values finite. I test against a reference and with statistical checks on frequencies.
- *Where does top-k fit in order?* Common order is temperature, then top-k/top-p/min-p filters, then renormalise and sample (library orders differ). See Q4 and Q13.
- *Edge cases?* `temperature=0` (divide by zero: treat as argmax), `top_p=1.0`, ties, and fully masked tokens with `-inf`.

**Common mistakes:** Spotting only the off-by-one. Applying temperature to probabilities. Fixing a scalar cutoff by looping over the batch instead of using masks. Verifying with one hand example instead of a reference comparison.

### Q36 ⭐ 🔴 How would you extend a tokenizer and model to a new domain or language (new tokens, embedding initialisation, continued pretraining)? What goes wrong?
**Asked at:** India product companies, GenAI startups, GCCs
**Say this first (1 line):** Train or extend the tokenizer on target-domain text, add the new tokens, resize the embedding (and output) matrix, initialise the new rows sensibly (for example the mean of the old sub-token embeddings of each new token), then continue pretraining on a mix of target and original data. The risks are forgetting old abilities and new tokens that stay undertrained.

**Then explain:**
- **Why bother:** a tokenizer built mostly on English splits Hindi, Tamil or legal/medical text into many pieces, so it costs more per request, fits less in context and is slower (see Q5). More native tokens means shorter sequences.
- **Steps:**
  1. Train a tokenizer on target text and merge only useful new tokens into the existing vocab (do not renumber old ids; old checkpoints depend on them).
  2. `resize_token_embeddings` (in Hugging Face) or equivalent: new rows in the input embedding, and in the output head if it is not tied (Part 1 Q25).
  3. Initialise the new rows. Random init gives meaningless inputs and outputs; the mean of the sub-token embeddings the old tokenizer would have produced is a common, cheap choice. Matching the norm scale of the old rows also helps.
  4. Continued pretraining on target data mixed with replay of the original distribution, a lower learning rate than the first run, and a short warmup. Often train embeddings (and sometimes only embeddings plus a few layers) first, then unfreeze.
  5. Evaluate on both the new domain and the old benchmarks.
- **What goes wrong:**
  - **Catastrophic forgetting:** only new-domain data pulls the model away from old abilities. Mitigate with replay data, lower LR, smaller token budgets.
  - **Undertrained new tokens:** rare new tokens get few gradient updates, so they stay near their init and can behave oddly (similar to the glitch tokens in Q18).
  - **Changed token boundaries** shift the input distribution of the whole model, so the model needs real training, not just new rows.
  - **Perplexity before and after is not comparable** across tokenizers (Q7); use bits-per-byte or task metrics.
  - Whether the gain is worth it vs simply using a multilingual base model: I would measure tokens per word and task quality first.

**Example:** a Hindi text that costs 3x the tokens of its English equivalent on the old tokenizer. After adding frequent Hindi words and sub-words, it might drop a lot, but I would report the measured fertility (tokens per word) on my own sample, not a quoted figure.

**Code:** (executed, torch; toy sizes)
```python
import torch
torch.manual_seed(0)
V, D = 10, 4
old_emb = torch.nn.Embedding(V, D)                  # old vocab: 10 tokens
old = old_emb.weight.data.clone()

# new token used to be split by the old tokenizer into old sub-tokens [3, 5, 7]
parts = [3, 5, 7]
new_emb = torch.nn.Embedding(V + 1, D)              # resized matrix: one extra row
with torch.no_grad():
    new_emb.weight[:V] = old                        # copy old rows
    new_emb.weight[V] = old[parts].mean(dim=0)      # mean-of-sub-tokens init

w = new_emb.weight.detach()
print("old rows unchanged:", torch.equal(w[:V], old))
print("new row == mean of sub-token rows:", torch.allclose(w[V], old[parts].mean(0)))
print("new row norm %.3f | mean old-row norm %.3f" % (w[V].norm(), old.norm(dim=1).mean()))
h = old[7]                                          # hidden state resembling the last sub-token
print("logit new %.3f | logits of its parts %s" % ((h @ w[V]), [round(float(h @ old[i]), 3) for i in parts]))
# output: True, True, norm 0.978 vs 1.842, logit new 1.071 vs parts [0.066, 1.537, 1.61]
```
The mean row has a smaller norm than typical rows (averaging shrinks length), which is one reason to rescale it. This is a toy with random embeddings, so it shows the mechanics, not real quality.

**Follow-ups:**
- *Why not retrain from scratch?* Cost. Extension reuses the learned model, but with a big vocab change you may need a lot of continued-pretraining tokens.
- *Tied embeddings?* Then one resize covers input and output; otherwise resize both.
- *Cheaper alternatives?* Adapters or LoRA with new embedding rows trainable, or just a multilingual base model.

**Common mistakes:** Adding tokens but not resizing the output head. Random-initialising and fine-tuning briefly. Training only on new-domain data. Judging by perplexity across tokenizers. Renumbering existing ids.

### Q37 ⭐ 🔴 Tokenizer-free and byte-level models (ByT5, byte-latent transformers) and digit tokenisation choices: what are the trade-offs?
**Asked at:** research-leaning teams, big tech
**Say this first (1 line):** Byte-level models read raw UTF-8 bytes, so there is no vocabulary, no out-of-vocabulary text and no tokenizer quirks, but sequences get several times longer, which costs compute and context. Newer designs such as the Byte Latent Transformer try to get the best of both by grouping bytes into dynamic patches. Digit handling is a smaller version of the same trade-off.

**Then explain:**
- **Pros of bytes:** works for any language or script, noise-robust (typos, odd spellings), no glitch tokens (Q18), no fertility gap between languages, and simple to extend.
- **Cons:** about 4 bytes per English subword token is a rough rule of thumb (assumed here, language dependent), and non-Latin scripts take more bytes per character (my Hindi example: 16 characters, 42 bytes). Longer sequences mean more attention cost (quadratic) and more steps in generation.
- **ByT5** (reported): a T5-style encoder-decoder over bytes. From memory, the paper reports robustness to noise and good results on some character-level and multilingual tasks, at higher compute per text than subword models. I would not quote numbers.
- **Byte Latent Transformer (BLT)** (reported, Meta, 2024): a small model groups bytes into patches whose size depends on how unpredictable the next byte is (more compute on hard parts, less on easy ones), and a large latent transformer works on patches. The claim is subword-level scaling behaviour without a fixed vocabulary; I treat this as a research result, not a settled replacement.
- **Digits:** common choices are splitting numbers into single digits (reported for several open models; it tends to help arithmetic because each digit has a consistent meaning), fixed-size digit chunks, or merged number tokens. Merged tokens like "1234" make the model memorise rather than compute. Right-to-left grouping (thousands) is another reported trick for alignment. The right choice depends on the task, and arithmetic ability also depends on data and training (Q6).

**Example:** the Hindi sentence above has 16 characters but 42 bytes. At byte level it is 2.6x longer than at character level, so attention pairs grow by about 6.9x. That is the cost of "no vocabulary".

**Code:** (executed)
```python
texts = {"English": "The weather is nice today", "Hindi": "आज मौसम अच्छा है", "number": "1234567"}
for k, t in texts.items():
    print(f"{k:8s} chars={len(t):3d} utf8 bytes={len(t.encode('utf-8')):3d}")
hi = texts["Hindi"]
r = len(hi.encode()) / len(hi)
print("Hindi bytes per char %.2f; attention pairs x%.1f vs char-level" % (r, r**2))
# English 25/25, Hindi 16 chars -> 42 bytes, ratio 2.62, pairs x6.9
```

**Follow-ups:**
- *Why not just use bytes everywhere?* Compute and latency: the same text costs several times more forward passes. Patching or hierarchical models try to remove that cost.
- *Does byte-level fix letter counting?* It helps because characters are visible, but the model still must learn the skill (Q6).
- *Vocabulary of 256?* 256 byte values plus a few special tokens; the embedding table is tiny, so parameters go into the transformer.

**Common mistakes:** Claiming byte models are strictly better or that they have no trade-offs. Forgetting non-Latin scripts take 2 to 4 bytes per character. Quoting exact benchmark numbers from memory. Saying single-digit tokenisation alone "solves" arithmetic.

### Q38 ⭐ 🔴 Data mixtures, curriculum, annealing and synthetic data in pretraining: what helps, and what is model collapse?
**Asked at:** big tech, GenAI startups, research-leaning teams
**Say this first (1 line):** Data quality and mixture matter as much as quantity: upweight high-quality sources, deduplicate, and often finish training with a short "annealing" phase on the best data at a decaying learning rate. Synthetic data can help when it is filtered and mixed with real data. Model collapse is what happens when models are trained recursively on their own outputs with no fresh real data: the tails of the distribution disappear. The evidence on how much of this matters in practice is mixed.

**Then explain:**
- **Mixtures:** the corpus is a weighted blend (web, code, books, maths, multilingual). Weights are usually tuned with small proxy runs, and code or maths often get upweighted relative to their raw share. Exact recipes are rarely disclosed, so I would say "tuned empirically".
- **Curriculum:** ordering data (easy to hard, or low to high quality). Reported gains are modest and inconsistent; many large runs mostly shuffle, with quality shifts late in training.
- **Annealing:** in the last part of training, as the learning rate decays (see Q26 for WSD/cosine), switch to a higher-quality, more reasoning-heavy mix. Several public model reports describe this and say it helps benchmarks. I treat it as a common practice, with the benchmark-gain caveat that it can also be partly contamination-like targeting (Q30).
- **Synthetic data:** model-generated text, textbooks-style data, rewrites of web text, code with verification, reasoning traces. Works best with a filter or verifier (unit tests, answer checks) and diversity control.
- **Model collapse:** reported in the literature when each generation trains on the previous generation's samples. Rare events vanish first, then variance shrinks. It is driven by *replacing* real data; results where synthetic data is *added* to real data are much milder. I would not claim it is inevitable or already happening at scale.

**Example (synthetic, a toy, not an LLM):** repeatedly fit a Gaussian to 50 samples drawn from the previous fit, for 200 generations. Fresh real data fraction 0%: median final std 0.016 (true value 1.0). Fresh fraction 10%: 0.934. 50%: 0.980. A small share of fresh real data keeps the distribution anchored.

**Code:** (executed)
```python
import numpy as np
def run(fresh_frac, gens=200, n=50, seed=0):
    rng = np.random.default_rng(seed)
    mu, sd = 0.0, 1.0                                # generation 0 = true distribution N(0,1)
    for _ in range(gens):
        k = int(n * fresh_frac)
        x = np.concatenate([rng.normal(0, 1, k),     # fresh real data
                            rng.normal(mu, sd, n - k)])  # data generated by previous model
        mu, sd = x.mean(), x.std()                   # "train" = refit Gaussian
    return sd
for f in (0.0, 0.1, 0.5):
    sds = [run(f, seed=s) for s in range(20)]
    print(f"fresh fraction {f:.1f}: median final std over 20 seeds = {np.median(sds):.3f}")
# 0.0 -> 0.016, 0.1 -> 0.934, 0.5 -> 0.980
```

**Follow-ups:**
- *How do you choose mixture weights?* Small-scale proxy runs, ablations on held-out evals, and checking they transfer to the target scale.
- *Is synthetic data safe?* Use verifiers, dedupe, keep real data in the mix, and track diversity (for example n-gram or embedding spread).
- *Distillation is not collapse?* Right: distilling a stronger model into a weaker one is a different setting; collapse is about recursion without outside signal.

**Common mistakes:** Saying "synthetic data always causes collapse" or "never does". Treating curriculum as a proven big win. Forgetting that annealing and benchmark-like data can inflate evals. Quoting mixture percentages from memory.

### Q39 ⭐ 🔴 How many epochs over the same data are acceptable? What do data-constrained scaling results say about repeating data?
**Asked at:** research-leaning teams, big tech
**Say this first (1 line):** From the data-constrained scaling work (Muennighoff et al., 2023, quoted from memory), a few epochs over the same data, roughly up to four in their setup, are nearly as good as fresh data, and returns diminish quickly after that. So repeating data is acceptable and often better than low-quality new data, but it is not free and it stops helping.

**Then explain:**
- **Setup:** when unique data is the limit (the "data wall", Q41), you either add new tokens or repeat old ones. They trained many models with varying repeats to see the loss cost.
- **Finding (as I remember it):** a small number of repeats cost little loss versus unique data; after that, extra epochs give less and less, and eventually almost nothing or worse. They fit a scaling law where repeated tokens count for less than fresh ones, with value decaying as repeats rise. I would not quote the exact constants.
- **Other levers they reported:** filling the gap with code data, and relaxing quality filters (keeping more of the lower-quality data rather than repeating the best), can substitute for repetition. Treat these as findings from one study.
- **Practical reading:** repeat the high-quality slice a few times; cap repeats of any one document; dedupe first (repeated near-duplicates are hidden multi-epoch training); watch validation loss on held-out data.
- **Risks of heavy repetition:** memorisation (privacy, copyright, regurgitation), overfitting to the training set, and eval contamination if repeated data overlaps benchmarks.
- **Caveat:** results were for specific model sizes, dropout/regularisation choices and data; modern runs with huge corpora may behave differently. Fine-tuning is different: several epochs on a small set are normal there (Part 4).

**Example:** you have 2T unique good tokens and a 6T-token budget. Three epochs over the good data is the kind of repetition the study suggests costs little; going to 20 epochs is where it says you should instead add new, even lower-quality or code data.

**Code:** none: this is a result from a paper and a toy would be made-up numbers.

**Follow-ups:**
- *How do you detect harmful repetition?* A widening train/validation gap, rising memorisation tests, and eval gains flattening against compute.
- *Does it apply to fine-tuning?* No, a different regime with different goals.
- *Does dedup conflict?* No: dedup removes accidental repeats you do not control; epochs are repeats you choose (Q25).

**Common mistakes:** Saying "never repeat data". Quoting "4 epochs" or constants as universal. Ignoring duplicates inside the corpus. Equating repeating web data with repeating the highest-quality data.

### Q40 ⭐ 🔴 Are emergent abilities real or an artefact of the metric? How would you test it?
**Asked at:** research-leaning teams, big tech
**Say this first (1 line):** Schaeffer et al. (2023) argued that many reported "emergent" jumps come largely from the metric: all-or-nothing scores like exact match look like a sudden jump even when the underlying per-token skill improves smoothly, and small test sets add noise. That does not prove every capability change is smooth, so I would say "partly an artefact, not fully refuted", and test it myself.

**Then explain:**
- **Claim being tested:** some abilities appear abruptly at a certain scale, not predictable from smaller models (Wei et al., 2022).
- **The metric argument:** exact match over k tokens is roughly `p^k` where p is per-token accuracy. A smooth rise in p gives a curve that hugs zero and then takes off. A continuous metric (token-level log-likelihood, edit distance, partial credit) on the same models looks smooth. The paper also reports that changing the metric on the same outputs makes some jumps disappear (from memory; I would not give numbers).
- **Statistics:** with few test items and scores near zero, noise is large; error bars are often missing.
- **What it does not show:** that every ability is smooth, or that capability-in-practice (a user needs the whole answer right) is not threshold-like. For users, exact-match-like success is what matters, so the "jump" can be real in usefulness even if the loss is smooth.
- **How I would test:** (1) evaluate the same model family at several sizes with several metrics (exact match, partial credit, log-likelihood of the correct answer); (2) use large test sets and report confidence intervals; (3) use more intermediate sizes or checkpoints; (4) check whether the continuous metric predicts the discontinuous one; (5) beware contamination.

**Example (synthetic, made-up curve, not real models):** per-token accuracy follows a smooth logistic in log model size, and exact match requires 10 tokens all right. Per-token accuracy goes 0.14 to 0.95 smoothly across 1e7 to 1e11 "parameters", while exact match goes 0.000, 0.000, 0.000, 0.001, 0.013, 0.072, 0.217, 0.420, 0.615: flat near zero and then rising fast. Same underlying skill, very different picture.

**Code:** (executed, synthetic)
```python
import numpy as np
# SYNTHETIC: per-token accuracy rises smoothly with log model size; exact match needs k tokens all right.
sizes = np.logspace(7, 11, 9)                       # 1e7 ... 1e11 "parameters"
p = 1 / (1 + np.exp(-(np.log10(sizes) - 8.5) * 1.2))   # smooth per-token accuracy (assumed)
k = 10
em = p ** k
print("params   per-token acc   exact-match(k=10)")
for n, a, e in zip(sizes, p, em):
    print(f"{n:8.0e}   {a:6.3f}          {e:6.3f}")
for n_items in (100, 1000):
    se = (0.05 * 0.95 / n_items) ** 0.5
    print(f"test set {n_items}: std error at acc=0.05 is {se:.3f}")
# std error at acc=0.05: 0.022 (100 items) vs 0.007 (1000 items)
```

**Follow-ups:**
- *So are emergent abilities fake?* No: the paper shows metric choice explains many cases; whether all are explained is still debated, and in-context and multi-step skills may behave differently.
- *Why does it matter?* For forecasting: if the smooth underlying skill is measurable, you can predict when a task becomes usable, instead of being surprised.
- *Relation to scaling laws?* Loss is smooth and predictable (Q41); downstream task scores can be harder to extrapolate.

**Common mistakes:** Saying "emergence is debunked". Saying it is purely magic. Ignoring sample size and error bars. Judging only on exact match or multiple-choice accuracy.

### Q41 ⭐ 🔴 What are the limits and critiques of scaling laws (fit uncertainty, extrapolation risk, the data wall, test-time compute)?
**Asked at:** senior roles at big tech, research-leaning teams
**Say this first (1 line):** Scaling laws are useful empirical fits of loss against compute, parameters and data, but they are fits, not physics: the constants have uncertainty, extrapolating far beyond the fitted range is risky, downstream task scores are harder to predict than loss, and they say little about the data wall or about spending compute at inference instead.

**Then explain:**
- **Fit uncertainty:** the laws have several free parameters (an irreducible-loss term, coefficients, exponents) fitted on a limited set of runs. These parameters trade off against each other, so small changes in data or fitting method move the answer. A replication attempt of the Chinchilla fit (arXiv 2404.10102, seen via search, not read in full) reportedly found the estimates sensitive and the optimal tokens-per-parameter ratio different from the commonly quoted ~20 (in the teens by my notes). I treat 20 as a rule of thumb (Q10/Q11), not a constant.
- **Extrapolation risk:** you fit at small scale and predict 10x to 100x larger. Small errors in the exponent become large errors in the prediction (my toy below).
- **Setup dependence:** the "optimal" split depends on what is held fixed: learning-rate schedule, batch size, data quality and mixture, tokenizer (Q7), architecture. It also ignores inference cost: models trained far past "compute-optimal" are popular because they are cheaper to serve (Q32).
- **Loss is not capability:** smooth loss does not tell you when a downstream skill becomes usable (Q40).
- **Data wall:** the laws assume you can keep getting fresh tokens. High-quality web text is finite; repetition (Q39), synthetic data (Q38) and multimodal data are the responses, each with caveats.
- **Test-time compute:** a different axis, spending more compute per query (Q43). Reported results suggest it can substitute for some pretraining compute on reasoning tasks, with limits.
- **Net:** use scaling laws to plan and compare recipes at small scale, with error bars, and re-check with an intermediate-scale run.

**Example (synthetic):** a true law `L = 1.7 + 2.0 * N^-0.34` (N in millions of parameters), eight noisy runs from 1M to 100M (noise 0.02 loss), refit 200 times and extrapolate to 10B. True loss 1.787. Across refits the prediction ranged from 1.726 to 1.863 (5th to 95th percentile) and the fitted irreducible term from 1.60 to 1.80 (true 1.70). The whole gain from 100M to 10B is only about 0.1 loss here, so the fit uncertainty is of the same size as the effect we want to predict.

**Code:** (executed, synthetic, numpy only)
```python
import numpy as np
# SYNTHETIC: true law L = 1.7 + 2.0 * N^-0.34 (N in millions); noisy small runs; extrapolate 100x
f = lambda N, E, A, a: E + A * N ** (-a)
true = (1.7, 2.0, 0.34)
rng = np.random.default_rng(0)
N_fit = np.logspace(0, 2, 8)                        # 1M .. 100M params
N_big = 1e4                                         # 10B params = 100x beyond the fit range
grid = np.linspace(0.05, 1.5, 300)                  # candidate exponents

def fit(y):
    best = None
    for a in grid:                                  # for each a, E and A are linear least squares
        X = np.c_[np.ones_like(N_fit), N_fit ** (-a)]
        coef, res, *_ = np.linalg.lstsq(X, y, rcond=None)
        sse = ((X @ coef - y) ** 2).sum()
        if coef[1] > 0 and coef[0] >= 0 and (best is None or sse < best[0]):
            best = (sse, coef[0], coef[1], a)
    return best[1:]

preds = []
for s in range(200):
    y = f(N_fit, *true) + rng.normal(0, 0.02, N_fit.size)   # 0.02 loss noise
    E, A, a = fit(y)
    preds.append((f(N_big, E, A, a), E))
preds = np.array(preds)
print("true loss at 10B: %.3f" % f(N_big, *true))
print("extrapolated: median %.3f, 5th-95th pct %.3f to %.3f" % (np.median(preds[:, 0]), *np.percentile(preds[:, 0], [5, 95])))
print("fitted irreducible term E: 5th-95th pct %.2f to %.2f (true 1.70)" % tuple(np.percentile(preds[:, 1], [5, 95])))
# true 1.787; extrapolated median 1.787, 1.726 to 1.863; E 1.60 to 1.80
```

**Follow-ups:**
- *Do scaling laws still matter?* Yes for planning and ablation at small scale; just report uncertainty and validate at an intermediate size.
- *Why train beyond compute-optimal?* Serving cost: a smaller model trained on more tokens is cheaper per query (Q32).
- *Has scaling stopped?* I would not claim that. I would say pretraining returns are debated, data is a constraint, and inference-time compute has become a second axis.

**Common mistakes:** Treating 20 tokens per parameter as a law. Quoting fitted constants without error bars. Equating loss with downstream ability. Saying scaling "is dead" or "will solve everything" without evidence.

### Q42 ⭐ 🔴 Decoding-time methods to improve quality: self-consistency, contrastive decoding and DoLa. How do they work and what do they cost?
**Asked at:** research-leaning teams, big tech
**Say this first (1 line):** Self-consistency samples several reasoning chains and takes the majority final answer; it costs n times the tokens. Contrastive decoding and DoLa change the next-token scores instead: they subtract what a weaker model (or an earlier layer) believes from what the stronger one believes, to favour tokens that reflect real knowledge. Details vary by paper, so I describe the idea and hedge specifics.

**Then explain:**
- **Self-consistency** (Wang et al., 2022): sample n chain-of-thought answers at temperature above 0, extract each final answer, return the most common. Works when answers are short and comparable (numbers, multiple choice), not for free-form text. Cost: about n x output tokens (prompt tokens can be shared); latency is the same if sampled in parallel. Gains shrink as n grows, and they depend on the errors being fairly independent and the correct answer being the most common one.
- **Contrastive decoding** (Li et al., 2022, from memory): take a large "expert" and a small "amateur" model. Score each token by `log p_expert - log p_amateur`, but only among tokens the expert finds plausible (the plausibility constraint: probability above a fraction of the expert's top probability), otherwise you would pick junk tokens that the amateur happens to dislike. Intuition: generic, repetitive text is likely under both models, so subtracting removes it. Cost: running a second (smaller) model per step. Reported for open-ended generation quality; gains on factual tasks vary.
- **DoLa** (Chuang et al., 2023, from memory): no second model. Contrast the final layer's next-token distribution with an earlier ("premature") layer's, dynamically picking the earlier layer that differs most. Idea: factual knowledge tends to sharpen in later layers, so tokens whose probability rises through the layers are favoured. Cost: a little extra compute to project early-layer states through the output head. Reported to reduce hallucination in some benchmarks; I would test it on my data before trusting it.
- Contrast and DoLa act on the logits, so they interact with sampling settings (Q4); self-consistency sits on top of any sampler.

**Example (synthetic simulation, independent samples assumed):** each sample is right with probability 0.6, wrong answers spread over 4 wrong values. Majority-vote accuracy: n=1 0.601, n=3 0.722, n=5 0.835, n=11 0.966, n=21 0.998. With p=0.4 (right answer still the single most likely) it needs far more votes: n=11 0.708, n=21 0.853, n=41 0.961. Real samples are correlated, so real curves are flatter.

**Code:** (executed, synthetic)
```python
import numpy as np
# SYNTHETIC: each sampled answer is correct w.p. p; wrong answers spread uniformly over 4 wrong values.
# Assumes independent samples (real samples are correlated, so real gains are smaller).
rng = np.random.default_rng(0)
def maj_acc(p, n, trials=20000):
    correct = rng.random((trials, n)) < p
    ans = np.where(correct, 0, rng.integers(1, 5, (trials, n)))   # 0 = right answer
    counts = np.stack([(ans == v).sum(1) for v in range(5)], 1)
    noisy = counts + rng.random(counts.shape) * 0.5               # random tie-break
    return (noisy.argmax(1) == 0).mean()
for p in (0.4, 0.6):
    print(f"single-sample accuracy {p}")
    for n in (1, 3, 5, 11, 21, 41):
        print(f"  n={n:3d}  majority acc {maj_acc(p, n):.3f}  relative cost {n}x")
# p=0.6: 0.601, 0.722, 0.835, 0.966, 0.998, 1.000 ; p=0.4: 0.392, 0.461, 0.547, 0.708, 0.853, 0.961
```

**Follow-ups:**
- *When does self-consistency fail?* When the model is consistently wrong (the wrong answer is the mode), when answers are not comparable, or when samples are copies of each other (temperature too low).
- *Why the plausibility constraint?* Without it the subtraction rewards very unlikely tokens, producing nonsense.
- *Cost comparison?* Self-consistency: n x tokens. Contrastive: roughly expert plus amateur compute per step. DoLa: close to one model.

**Common mistakes:** Calling self-consistency "free" or assuming it fixes systematic errors. Using temperature 0 for the samples. Describing contrastive decoding as just "subtract logits" without the plausibility constraint. Stating benchmark gains from memory.

### Q43 ⭐ 🔴 Test-time compute: best-of-n, majority voting and long chain-of-thought sampling. How do cost, latency and accuracy trade off?
**Asked at:** big tech, GenAI startups, product
**Say this first (1 line):** Test-time compute means spending more inference compute per question to get better answers: sample n answers and pick by majority vote or by a verifier/reward model (best-of-n), or let the model think longer in one long chain of thought. Cost is roughly n x tokens x price, accuracy gains diminish, and for best-of-n the verifier's quality caps what you can gain.

**Then explain:**
- **Majority voting:** needs no verifier, only comparable final answers (Q42). Cost n x tokens.
- **Best-of-n with a verifier or reward model:** generate n candidates, score each, return the top. Works on answers that cannot be voted (code, proofs, free text) if a good scorer exists (unit tests are the best verifier; a learned reward model is noisier and can be gamed as n grows).
- **Long chain-of-thought (reasoning models):** one sample, but thousands of "thinking" tokens, trained with reinforcement learning to reason and self-check. Cost scales with tokens generated, latency scales almost linearly with thinking length because tokens are produced sequentially (Q2, Part 10).
- **Cost model:** `cost = n x (output tokens per sample) x price per token` (plus the prompt once if cached, plus verifier calls). Parallel sampling keeps latency near one sample but multiplies the GPU bill; long CoT multiplies latency.
- **Diminishing returns:** each doubling of n gives less. The ceiling is the "any sample correct" rate (oracle), and the gap to it is verifier quality.
- **When it pays:** hard tasks where p(correct) is moderate and a good verifier exists; not for easy tasks, strict latency budgets or when the model is consistently wrong. Route: cheap model first, escalate only low-confidence queries.

**Example (illustrative toy, numbers assumed, not real models or prices):** each sample is right with probability 0.4; the verifier gives right answers a score shifted by `d` over wrong ones (d=0 is a useless verifier). Assume 500 output tokens per sample and $10 per 1M output tokens.

| n | cost/query | d=0 | d=1 | d=2 | d=4 | oracle (any right) |
|---|---|---|---|---|---|---|
| 1 | $0.005 | 0.392 | 0.403 | 0.398 | 0.402 | 0.400 |
| 4 | $0.020 | 0.399 | 0.638 | 0.794 | 0.866 | 0.870 |
| 8 | $0.040 | 0.401 | 0.731 | 0.914 | 0.980 | 0.983 |
| 32 | $0.160 | 0.403 | 0.846 | 0.988 | 1.000 | 1.000 |

A useless verifier gains nothing at any cost; a weak one (d=1) still sits well below the oracle at 32x the price, while a good one (d=4) reaches the ceiling by n=8 to 16.

**Code:** (executed, illustrative toy)
```python
import numpy as np
# ILLUSTRATIVE toy. Each sample is right w.p. p=0.4. Verifier: right answers score ~ N(d,1), wrong ~ N(0,1).
rng = np.random.default_rng(0)
p, trials = 0.4, 20000
tokens_per_sample, price_per_M = 500, 10.0           # assumed values
def best_of_n(n, d):
    right = rng.random((trials, n)) < p
    score = rng.normal(0, 1, (trials, n)) + d * right
    return right[np.arange(trials), score.argmax(1)].mean()
print(" n | cost/query($) | d=0 | d=1 | d=2 | d=4 | oracle")
for n in (1, 2, 4, 8, 16, 32):
    cost = n * tokens_per_sample * price_per_M / 1e6
    oracle = 1 - (1 - p) ** n
    print(f"{n:2d} | {cost:.4f} | " + " | ".join(f"{best_of_n(n, d):.3f}" for d in (0, 1, 2, 4)) + f" | {oracle:.3f}")
```
Samples are assumed independent, which flatters real systems.

**Follow-ups:**
- *Majority vote or best-of-n?* Vote when answers are short and comparable and no verifier exists; best-of-n when you have a reliable checker (tests, a calculator, a proof checker).
- *Reward-model hacking?* As n grows you increasingly select candidates that fool the scorer, so gains can peak and fall. Use held-out checks.
- *Test-time vs a bigger model?* Reported results suggest test-time compute can beat a larger model on some reasoning tasks, but not everywhere; measure cost per correct answer.

**Common mistakes:** Quoting accuracy without cost or latency. Assuming n samples are independent. Ignoring verifier quality. Applying heavy test-time compute to easy queries. Forgetting prompt tokens and verifier calls in the cost.

### Q44 ⭐ 🔴 Design question: choose decoding settings and stop rules for four products (code completion, support chat, creative writing, data extraction) and defend them.
**Asked at:** senior roles at product companies, GenAI startups, GCCs
<!-- ANSWER_PENDING -->

# Book 2 — Part 02: Tokenization, Pretraining, Scaling Laws and Decoding

**Topic:** subword tokenizers (BPE, WordPiece, Unigram, byte-level), token economics, pretraining objective, data pipeline, optimisation recipe and precision, scaling laws and compute estimates, and decoding strategies (greedy, sampling, beam, penalties, determinism, logprobs, test-time compute).
**Target:** 40  |  **Actual:** 44 (⭐⭐⭐ 13, ⭐⭐ 21, ⭐ 10)  |  **Date:** 2026-10-21  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 already covers input embeddings, unembedding and the vocabulary's effect on model size (Q25), BERT vs GPT objectives (Q16), training-stability tricks (Q44) and multi-token prediction (Q45). Here those are cross-referenced, not repeated. Overlaps with Book 1 are intentional but deeper here: subword tokenization (B1P09-Q27: here the merge algorithm, byte-level and design trade-offs), LM perplexity (B1P09-Q18: here bits-per-byte and cross-tokenizer comparison), beam search (B1P09-Q44: here cost and length normalisation), LR schedules, loss curves and mixed precision (B1P08-Q14/Q16/Q40: here LLM-pretraining specifics), benchmark contamination (B1P01-Q34: here decontamination of a corpus), and calibration from logprobs (B1P03-Q44: here logprob mechanics). Answers must cross-reference, not copy. Constrained/structured decoding belongs to Part 3, fine-tuning to Part 4, RLHF/DPO to Part 5, and speculative decoding, PagedAttention and serving to Part 10. Generic distributed-training and MLOps detail belongs to Book 4.

---

### Q1 ⭐⭐⭐ 🟢 Why do LLMs use subword tokenization instead of words or characters? Compare BPE, WordPiece and Unigram/SentencePiece.
**Asked at:** all types; service-company, GCC and product GenAI loops
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Greedy decoding vs sampling vs beam search: how does each choose the next token, and when would you use which?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is the pretraining objective of a decoder-only LLM? Write the next-token cross-entropy loss and explain the label shift.
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 Explain temperature, top-k and top-p (nucleus) sampling. What does each do to the distribution and what are sensible values?
**Asked at:** all types; product, GCC, GenAI startups
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 Token maths: how many tokens is 1,000 words, why do code, JSON and non-English text cost more, and how would you cut token spend?
**Asked at:** product, GCC, API-heavy teams
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Why do LLMs struggle with counting letters ("strawberry"), arithmetic and string reversal? What does tokenization have to do with it?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 What is perplexity? How does it relate to cross-entropy loss, and why can't you compare it across models with different tokenizers?
**Asked at:** all types; product, research-leaning teams
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Pretraining vs continued pretraining vs fine-tuning: what changes in data, objective, cost and risk, and when do you choose each?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Walk through a pretraining data pipeline: sources, cleaning, quality filtering, language ID, PII/toxicity filtering, deduplication and mixing.
**Asked at:** product, big tech, GenAI startups
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 What are LLM scaling laws? What do loss versus parameters, data and compute look like, and what can you do with them?
**Asked at:** big tech, product, GenAI startups
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 What did Chinchilla find? Use C ~ 6ND to work out the compute-optimal model size and token count for a given budget.
**Asked at:** big tech, product, research-leaning teams
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Code: implement a byte-pair-encoding tokenizer (train, encode, decode) with deterministic tie-breaking, and show a round trip.
**Asked at:** product, big tech, live-coding rounds; a Glean software-engineer onsite/technical-screen report and a Perplexity online-assessment listing mention BPE coding
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Code: implement temperature, top-k and top-p sampling from a logits vector, and verify it empirically.
**Asked at:** product, big tech, live-coding rounds
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟡 How do you choose a tokenizer vocabulary size? Discuss sequence length, embedding/softmax cost, rare-token under-training and multilingual coverage.
**Asked at:** product, GenAI startups, big tech
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟡 What is byte-level BPE, why does it remove out-of-vocabulary tokens, and what are its trade-offs (UTF-8, byte fallback)?
**Asked at:** product, GenAI startups
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 What are special tokens (BOS, EOS, PAD, role/chat tokens) and chat templates? What breaks if the template or padding side is wrong?
**Asked at:** product, GCC, API-heavy and fine-tuning teams
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 Why do Indian and other low-resource languages cost more tokens (the "token tax")? What can you do about it?
**Asked at:** India product companies, GCCs, GenAI startups
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 What are glitch or under-trained tokens, why do they exist, and how would you detect them?
**Asked at:** research-leaning teams, big tech
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 What are min-p and typical sampling, and in what order should samplers (penalties, temperature, truncation) be applied?
**Asked at:** product, GenAI startups, inference teams
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Why do LLMs repeat themselves, and how do repetition, frequency and presence penalties work? When do penalties hurt (code, JSON)?
**Asked at:** product, GenAI startups, API-heavy teams
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Is temperature 0 deterministic? What causes run-to-run differences in LLM output, and how do you get reproducibility?
**Asked at:** product, GCC, API-heavy teams, evaluation teams
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 How does generation stop? Explain EOS, stop sequences, max tokens, finish reasons, truncation and streaming.
**Asked at:** product, GCC, API-heavy teams
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 What are logprobs? How can you use token log-probabilities for confidence, classification and calibration, and what is logit bias?
**Asked at:** product, GenAI startups, evaluation teams
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Beam search in detail: length normalisation, cost in compute and KV memory, and why it works for translation but not open-ended chat.
**Asked at:** product, research-leaning teams
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 How do you deduplicate a pretraining corpus (exact vs near-duplicate, MinHash/LSH)? Why does it matter?
**Asked at:** big tech, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 What does a standard LLM pretraining optimisation recipe look like (AdamW settings, warmup, cosine or WSD decay, weight decay, gradient clipping), and why each piece?
**Asked at:** big tech, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Why is bf16 preferred over fp16 for LLM pretraining? Cover exponent range vs mantissa, fp32 master weights and optimizer states, which ops stay in fp32, and what FP8 changes.
**Asked at:** big tech, product, GenAI startups
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How do you choose batch size in LLM pretraining (tokens per step, gradient accumulation, critical batch size, learning-rate scaling)?
**Asked at:** big tech, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 How do you read a pretraining loss curve? What do spikes, divergence, plateaus and a train/validation gap tell you, and what would you do?
**Asked at:** big tech, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 How do you decontaminate a pretraining corpus against benchmarks (n-gram overlap, canary strings, dynamic test sets) and detect contamination in a finished model?
**Asked at:** product, evaluation teams, research-leaning teams
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Why do LLMs memorise and regurgitate training data? What makes it worse, and how do you reduce privacy and copyright risk?
**Asked at:** product, GCC, regulated-industry teams
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Why do modern models train far beyond the Chinchilla-optimal token count (e.g. an 8B model on ~15T tokens)? What is inference-aware scaling?
**Asked at:** big tech, product, GenAI startups
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Estimate the cost of pretraining a 7B model on 2T tokens: FLOPs, GPU-hours, model FLOPs utilisation (MFU) and rough dollars.
**Asked at:** big tech, product, infra/platform teams
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🔴 Live maths: how much GPU memory does training a 7B model need (weights, gradients, Adam states, activations)? Explain data, tensor and pipeline parallelism and ZeRO/FSDP at a high level.
**Asked at:** big tech, infra/platform teams, GenAI startups
<!-- ANSWER_PENDING -->

### Q35 ⭐ 🟡 AI code review: this LLM-written sampling function has bugs (top-p off-by-one, wrong order of temperature and softmax, no renormalisation, mutated logits). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🔴 How would you extend a tokenizer and model to a new domain or language (new tokens, embedding initialisation, continued pretraining)? What goes wrong?
**Asked at:** India product companies, GenAI startups, GCCs
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🔴 Tokenizer-free and byte-level models (ByT5, byte-latent transformers) and digit tokenisation choices: what are the trade-offs?
**Asked at:** research-leaning teams, big tech
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🔴 Data mixtures, curriculum, annealing and synthetic data in pretraining: what helps, and what is model collapse?
**Asked at:** big tech, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🔴 How many epochs over the same data are acceptable? What do data-constrained scaling results say about repeating data?
**Asked at:** research-leaning teams, big tech
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🔴 Are emergent abilities real or an artefact of the metric? How would you test it?
**Asked at:** research-leaning teams, big tech
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🔴 What are the limits and critiques of scaling laws (fit uncertainty, extrapolation risk, the data wall, test-time compute)?
**Asked at:** senior roles at big tech, research-leaning teams
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Decoding-time methods to improve quality: self-consistency, contrastive decoding and DoLa. How do they work and what do they cost?
**Asked at:** research-leaning teams, big tech
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 Test-time compute: best-of-n, majority voting and long chain-of-thought sampling. How do cost, latency and accuracy trade off?
**Asked at:** big tech, GenAI startups, product
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 Design question: choose decoding settings and stop rules for four products (code completion, support chat, creative writing, data extraction) and defend them.
**Asked at:** senior roles at product companies, GenAI startups, GCCs
<!-- ANSWER_PENDING -->

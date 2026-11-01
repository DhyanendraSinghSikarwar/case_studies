import io
QS = [
# (stars, diff, question, asked_at)
(3,'🟢',"Why do LLMs use subword tokenization instead of words or characters? Compare BPE, WordPiece and Unigram/SentencePiece.","all types; service-company, GCC and product GenAI loops"),
(3,'🟢',"Greedy decoding vs sampling vs beam search: how does each choose the next token, and when would you use which?","all types"),
(3,'🟢',"What is the pretraining objective of a decoder-only LLM? Write the next-token cross-entropy loss and explain the label shift.","all types"),
(3,'🟡',"Explain temperature, top-k and top-p (nucleus) sampling. What does each do to the distribution and what are sensible values?","all types; product, GCC, GenAI startups"),
(3,'🟡',"Token maths: how many tokens is 1,000 words, why do code, JSON and non-English text cost more, and how would you cut token spend?","product, GCC, API-heavy teams"),
(3,'🟡',"Why do LLMs struggle with counting letters (\"strawberry\"), arithmetic and string reversal? What does tokenization have to do with it?","all types"),
(3,'🟡',"What is perplexity? How does it relate to cross-entropy loss, and why can't you compare it across models with different tokenizers?","all types; product, research-leaning teams"),
(3,'🟡',"Pretraining vs continued pretraining vs fine-tuning: what changes in data, objective, cost and risk, and when do you choose each?","all types"),
(3,'🟡',"Walk through a pretraining data pipeline: sources, cleaning, quality filtering, language ID, PII/toxicity filtering, deduplication and mixing.","product, big tech, GenAI startups"),
(3,'🟡',"What are LLM scaling laws? What do loss versus parameters, data and compute look like, and what can you do with them?","big tech, product, GenAI startups"),
(3,'🟡',"What did Chinchilla find? Use C ~ 6ND to work out the compute-optimal model size and token count for a given budget.","big tech, product, research-leaning teams"),
(3,'🟡',"Code: implement a byte-pair-encoding tokenizer (train, encode, decode) with deterministic tie-breaking, and show a round trip.","product, big tech, live-coding rounds; a Glean software-engineer onsite/technical-screen report and a Perplexity online-assessment listing mention BPE coding"),
(3,'🟡',"Code: implement temperature, top-k and top-p sampling from a logits vector, and verify it empirically.","product, big tech, live-coding rounds"),
(2,'🟡',"How do you choose a tokenizer vocabulary size? Discuss sequence length, embedding/softmax cost, rare-token under-training and multilingual coverage.","product, GenAI startups, big tech"),
(2,'🟡',"What is byte-level BPE, why does it remove out-of-vocabulary tokens, and what are its trade-offs (UTF-8, byte fallback)?","product, GenAI startups"),
(2,'🟡',"What are special tokens (BOS, EOS, PAD, role/chat tokens) and chat templates? What breaks if the template or padding side is wrong?","product, GCC, API-heavy and fine-tuning teams"),
(2,'🟡',"Why do Indian and other low-resource languages cost more tokens (the \"token tax\")? What can you do about it?","India product companies, GCCs, GenAI startups"),
(2,'🟡',"What are glitch or under-trained tokens, why do they exist, and how would you detect them?","research-leaning teams, big tech"),
(2,'🟡',"What are min-p and typical sampling, and in what order should samplers (penalties, temperature, truncation) be applied?","product, GenAI startups, inference teams"),
(2,'🟡',"Why do LLMs repeat themselves, and how do repetition, frequency and presence penalties work? When do penalties hurt (code, JSON)?","product, GenAI startups, API-heavy teams"),
(2,'🟡',"Is temperature 0 deterministic? What causes run-to-run differences in LLM output, and how do you get reproducibility?","product, GCC, API-heavy teams, evaluation teams"),
(2,'🟡',"How does generation stop? Explain EOS, stop sequences, max tokens, finish reasons, truncation and streaming.","product, GCC, API-heavy teams"),
(2,'🟡',"What are logprobs? How can you use token log-probabilities for confidence, classification and calibration, and what is logit bias?","product, GenAI startups, evaluation teams"),
(2,'🟡',"Beam search in detail: length normalisation, cost in compute and KV memory, and why it works for translation but not open-ended chat.","product, research-leaning teams"),
(2,'🟡',"How do you deduplicate a pretraining corpus (exact vs near-duplicate, MinHash/LSH)? Why does it matter?","big tech, GenAI startups, research-leaning teams"),
(2,'🟡',"What does a standard LLM pretraining optimisation recipe look like (AdamW settings, warmup, cosine or WSD decay, weight decay, gradient clipping), and why each piece?","big tech, GenAI startups, research-leaning teams"),
(2,'🟡',"Why is bf16 preferred over fp16 for LLM pretraining? Cover exponent range vs mantissa, fp32 master weights and optimizer states, which ops stay in fp32, and what FP8 changes.","big tech, product, GenAI startups"),
(2,'🟡',"How do you choose batch size in LLM pretraining (tokens per step, gradient accumulation, critical batch size, learning-rate scaling)?","big tech, GenAI startups, research-leaning teams"),
(2,'🟡',"How do you read a pretraining loss curve? What do spikes, divergence, plateaus and a train/validation gap tell you, and what would you do?","big tech, GenAI startups, research-leaning teams"),
(2,'🟡',"How do you decontaminate a pretraining corpus against benchmarks (n-gram overlap, canary strings, dynamic test sets) and detect contamination in a finished model?","product, evaluation teams, research-leaning teams"),
(2,'🟡',"Why do LLMs memorise and regurgitate training data? What makes it worse, and how do you reduce privacy and copyright risk?","product, GCC, regulated-industry teams"),
(2,'🟡',"Why do modern models train far beyond the Chinchilla-optimal token count (e.g. an 8B model on ~15T tokens)? What is inference-aware scaling?","big tech, product, GenAI startups"),
(2,'🟡',"Estimate the cost of pretraining a 7B model on 2T tokens: FLOPs, GPU-hours, model FLOPs utilisation (MFU) and rough dollars.","big tech, product, infra/platform teams"),
(2,'🔴',"Live maths: how much GPU memory does training a 7B model need (weights, gradients, Adam states, activations)? Explain data, tensor and pipeline parallelism and ZeRO/FSDP at a high level.","big tech, infra/platform teams, GenAI startups"),
(1,'🟡',"AI code review: this LLM-written sampling function has bugs (top-p off-by-one, wrong order of temperature and softmax, no renormalisation, mutated logits). Find and fix them.","product, big tech, AI-era code-review rounds"),
(1,'🔴',"How would you extend a tokenizer and model to a new domain or language (new tokens, embedding initialisation, continued pretraining)? What goes wrong?","India product companies, GenAI startups, GCCs"),
(1,'🔴',"Tokenizer-free and byte-level models (ByT5, byte-latent transformers) and digit tokenisation choices: what are the trade-offs?","research-leaning teams, big tech"),
(1,'🔴',"Data mixtures, curriculum, annealing and synthetic data in pretraining: what helps, and what is model collapse?","big tech, GenAI startups, research-leaning teams"),
(1,'🔴',"How many epochs over the same data are acceptable? What do data-constrained scaling results say about repeating data?","research-leaning teams, big tech"),
(1,'🔴',"Are emergent abilities real or an artefact of the metric? How would you test it?","research-leaning teams, big tech"),
(1,'🔴',"What are the limits and critiques of scaling laws (fit uncertainty, extrapolation risk, the data wall, test-time compute)?","senior roles at big tech, research-leaning teams"),
(1,'🔴',"Decoding-time methods to improve quality: self-consistency, contrastive decoding and DoLa. How do they work and what do they cost?","research-leaning teams, big tech"),
(1,'🔴',"Test-time compute: best-of-n, majority voting and long chain-of-thought sampling. How do cost, latency and accuracy trade off?","big tech, GenAI startups, product"),
(1,'🔴',"Design question: choose decoding settings and stop rules for four products (code completion, support chat, creative writing, data extraction) and defend them.","senior roles at product companies, GenAI startups, GCCs"),
]
n=len(QS)
c3=sum(1 for q in QS if q[0]==3); c2=sum(1 for q in QS if q[0]==2); c1=sum(1 for q in QS if q[0]==1)
# order check: stars desc
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
hdr=f"""# Book 2 — Part 02: Tokenization, Pretraining, Scaling Laws and Decoding

**Topic:** subword tokenizers (BPE, WordPiece, Unigram, byte-level), token economics, pretraining objective, data pipeline, optimisation recipe and precision, scaling laws and compute estimates, and decoding strategies (greedy, sampling, beam, penalties, determinism, logprobs, test-time compute).
**Target:** 40  |  **Actual:** {n} (⭐⭐⭐ {c3}, ⭐⭐ {c2}, ⭐ {c1})  |  **Date:** 2026-10-21  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 already covers input embeddings, unembedding and the vocabulary's effect on model size (Q25), BERT vs GPT objectives (Q16), training-stability tricks (Q44) and multi-token prediction (Q45). Here those are cross-referenced, not repeated. Overlaps with Book 1 are intentional but deeper here: subword tokenization (B1P09-Q27: here the merge algorithm, byte-level and design trade-offs), LM perplexity (B1P09-Q18: here bits-per-byte and cross-tokenizer comparison), beam search (B1P09-Q44: here cost and length normalisation), LR schedules, loss curves and mixed precision (B1P08-Q14/Q16/Q40: here LLM-pretraining specifics), benchmark contamination (B1P01-Q34: here decontamination of a corpus), and calibration from logprobs (B1P03-Q44: here logprob mechanics). Answers must cross-reference, not copy. Constrained/structured decoding belongs to Part 3, fine-tuning to Part 4, RLHF/DPO to Part 5, and speculative decoding, PagedAttention and serving to Part 10. Generic distributed-training and MLOps detail belongs to Book 4.

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
open('Book2_GenAI/Book2_GenAI_Part02.md','w',encoding='utf-8',newline='\n').write(''.join(out))
rows=''.join(f"| B2P02-Q{i} | 2 | {q} |\n" for i,(s,d,q,a) in enumerate(QS,1))
open('scratch/B2P02_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(rows)
print(n,c3,c2,c1)

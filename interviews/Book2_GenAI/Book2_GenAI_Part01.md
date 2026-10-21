# Book 2 — Part 01: Transformer Internals (attention, positional encoding, KV cache)

**Topic:** self-attention and multi-head attention, transformer block, encoder/decoder variants, positional encodings (sinusoidal, RoPE, ALiBi), KV cache, prefill vs decode, MQA/GQA/MLA, FlashAttention, long-context, MoE, alternatives to attention.
**Target:** 45  |  **Actual:** 47 (⭐⭐⭐ 15, ⭐⭐ 20, ⭐ 12)  |  **Date:** 2026-10-21  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Book 1 Part 9 gave a light transformer intro (self-attention, positional encoding, O(n^2)); this part is the deep treatment and must not repeat Book 1 answers verbatim. Tokenization, pretraining and decoding strategies are Part 2; serving (vLLM, PagedAttention, quantization, speculative decoding) is Part 10; LoRA/PEFT is Part 4.

---

### Q1 ⭐⭐⭐ 🟢 Explain self-attention step by step (Q, K, V, scaled dot-product, softmax). What does each of Q, K and V represent?
**Asked at:** all types; Capgemini/LTIMindtree/Hexaware-style GenAI loops, product, GCC
**Say this first (1 line):** Every token builds a query, compares it with every other token's key, turns the scores into weights with softmax, and takes a weighted average of the values.

**Then explain:**
- Start with token embeddings `X` of shape `(n, d_model)`. Three learned matrices give `Q = XW_q`, `K = XW_k`, `V = XW_v`, each `(n, d_k)`.
- **Q (query)** is what this token is looking for. **K (key)** is how each token advertises itself. **V (value)** is the content that actually gets passed on. Matching uses Q and K. Information flows through V.
- `scores = Q K^T / sqrt(d_k)` has shape `(n, n)`. Entry `(i, j)` says how relevant token j is to token i.
- `weights = softmax(scores)` along the key axis, so each row sums to 1. `output = weights @ V`, shape `(n, d_k)`.
- Why divide by `sqrt(d_k)`: dot products grow with dimension, softmax saturates and gradients vanish (details in Q17).
- Why separate Q, K, V: one projection would force "what I look for" and "what I offer" to be the same thing. Three projections let the model learn asymmetric relations.

**Example:** In "The animal didn't cross the street because it was tired", the query for "it" should score high against the key for "animal". The output at "it" is then mostly the value of "animal", so "it" now carries that meaning.

**Code:** (executed, numpy, seed 0, 4 tokens)
```python
import numpy as np
rng = np.random.default_rng(0)
n, d_model, d_k = 4, 8, 4
X  = rng.normal(size=(n, d_model))
Wq, Wk, Wv = (rng.normal(size=(d_model, d_k)) for _ in range(3))
Q, K, V = X @ Wq, X @ Wk, X @ Wv
scores = Q @ K.T / np.sqrt(d_k)                  # (n, n)
w = np.exp(scores - scores.max(-1, keepdims=True))
w /= w.sum(-1, keepdims=True)                    # softmax over keys
out = w @ V                                      # (n, d_k)
print(scores.shape, w.sum(-1).round(3), out.shape)
# (4, 4) [1. 1. 1. 1.] (4, 4)
```

**Follow-ups:**
- *Why subtract the max in softmax?* Numerical stability. It does not change the result.
- *Self vs cross attention?* In self-attention Q, K, V come from the same sequence. In cross-attention Q comes from the decoder and K, V from the encoder.
- *Does attention know word order?* No. It is permutation-equivariant, so positions must be added (Q8).

**Common mistakes:** Saying "K and V are the same thing". Forgetting the softmax axis (it is over keys, not queries). Forgetting the `sqrt(d_k)` scale. Saying attention weights are an explanation of the model's decision (they are not reliable as one).

### Q2 ⭐⭐⭐ 🟢 Why did transformers replace RNNs/LSTMs? What are the remaining drawbacks of transformers?
**Asked at:** all types; service-company and GCC GenAI loops
**Say this first (1 line):** Transformers process all tokens in parallel and connect any two tokens in one step, so they train much faster on GPUs and handle long-range dependencies better than RNNs. The price is quadratic attention cost and a growing KV cache at inference.

**Then explain:**
- **Parallelism:** An RNN computes `h_t` from `h_{t-1}`, so training is sequential across time. A transformer computes all positions at once as big matrix multiplies, which is what GPUs are good at. This is the main reason it scaled.
- **Long-range paths:** In an RNN, information between token 1 and token 500 passes through 499 steps, so gradients vanish or explode (LSTM gates help but do not fully fix it). In attention, any pair is one hop.
- **Bottleneck:** Classic seq2seq squeezed the whole input into one fixed vector. Attention lets each position look at all inputs directly.
- **Scaling behaviour:** Transformers kept improving with more data and parameters, which made large pretrained models practical.

| | RNN/LSTM | Transformer |
|---|---|---|
| Training over time | sequential | parallel |
| Path between two tokens | O(n) steps | 1 step |
| Compute per layer | O(n d^2) | O(n^2 d + n d^2) |
| Inference memory | constant state | KV cache grows with n |

**Remaining drawbacks:**
- Attention is O(n^2) in time (and in memory if the score matrix is materialised, which FlashAttention avoids).
- KV cache grows linearly with context, which limits batch size and context length at serving.
- No built-in order awareness, so it needs positional encodings, and length extrapolation is not free.
- Decoding is still sequential, one token at a time.
- Data and compute hungry.

**Example:** For a 2,000-token document, an RNN needs 2,000 sequential steps per training sequence. A transformer does one pass with a 2,000 x 2,000 score matrix per head, which is faster in wall-clock time on a GPU.

**Follow-ups:**
- *Are RNNs dead?* Not entirely. State-space models (Mamba) and linear-attention/RWKV-style models bring back constant-memory inference and are active research, though pure transformers still dominate large LLMs.
- *Why can't an RNN be parallelised in training?* The hidden state at t depends on t-1, a data dependency.

**Common mistakes:** Saying transformers are "more accurate" without naming the reason (parallelism, short paths). Claiming the transformer has no weaknesses on long sequences. Saying LSTMs cannot model long dependencies at all (they do, just worse and slower).

### Q3 ⭐⭐⭐ 🟡 What is multi-head attention? Why use several heads instead of one big head, and what are the tensor shapes and cost?
**Asked at:** all types
**Say this first (1 line):** Multi-head attention splits the model dimension into H smaller heads, runs attention in each in parallel, concatenates the results and mixes them with an output projection. Same cost as one big head, but the model can attend to different things at once.

**Then explain:**
- With `d_model = D` and `H` heads, each head has `d_h = D / H`. Input `(B, T, D)`.
- Project to Q, K, V as `(B, T, D)`, reshape to `(B, H, T, d_h)`.
- Scores `(B, H, T, T)`, softmax, times V gives `(B, H, T, d_h)`. Transpose and reshape back to `(B, T, D)`, then apply `W_o` of shape `(D, D)`.
- **Why several heads:** one head produces one softmax pattern per token, i.e. one weighted average. Several heads can track different relations (for example syntax, nearby tokens, coreference) at the same time. Each head works in a low-dimensional subspace.
- **Cost:** parameters are `4 D^2` (W_q, W_k, W_v, W_o), independent of H. Attention FLOPs are about `O(T^2 D)` for the score and value products, again independent of H. Score memory is `H * T^2` per layer if materialised, so more heads means more score memory.

**Example:** D = 64, H = 8 gives d_h = 8. Parameters: 4 x 64 x 64 = 16,384, the same as one head with d = 64.

**Code:** (executed, torch)
```python
import torch, torch.nn as nn
torch.manual_seed(0)
B, T, D, H = 2, 10, 64, 8
dh = D // H
x = torch.randn(B, T, D)
qkv = nn.Linear(D, 3*D, bias=False); o = nn.Linear(D, D, bias=False)
q, k, v = qkv(x).chunk(3, -1)
split = lambda t: t.view(B, T, H, dh).transpose(1, 2)   # (B,H,T,dh)
q, k, v = map(split, (q, k, v))
att = ((q @ k.transpose(-2, -1)) / dh**0.5).softmax(-1) # (B,H,T,T)
y = o((att @ v).transpose(1, 2).reshape(B, T, D))
print(q.shape, att.shape, y.shape)
# torch.Size([2, 8, 10, 8]) torch.Size([2, 8, 10, 10]) torch.Size([2, 10, 64])
print(sum(p.numel() for p in [*qkv.parameters(), *o.parameters()]))   # 16384 = 4*D*D
```
(No causal mask here, to keep the shapes clear. See Q5 and Q13 for masking.)

**Follow-ups:**
- *Why scale by `sqrt(d_h)` and not `sqrt(D)`?* The dot product is over d_h dimensions, so the variance grows with d_h.
- *Do all heads matter?* Studies of trained models found many heads can be pruned with little loss, so there is redundancy.
- *What does W_o do?* It mixes information across heads. Without it the heads would stay in separate slices.

**Common mistakes:** Saying more heads means more parameters. Forgetting the output projection. Mixing up `(B,H,T,d_h)` and `(B,T,H,d_h)` when reshaping (a transpose before the final reshape is required).

### Q4 ⭐⭐⭐ 🟢 Encoder-only vs decoder-only vs encoder-decoder models: how do they differ, with examples and when to use each?
**Asked at:** all types
**Say this first (1 line):** Encoder-only models read the whole text in both directions and produce representations; decoder-only models read left to right and generate text; encoder-decoder models read the input fully and then generate a separate output.

**Then explain:**

| | Encoder-only | Decoder-only | Encoder-decoder |
|---|---|---|---|
| Attention | bidirectional | causal (left to right) | encoder bidirectional; decoder causal plus cross-attention to encoder |
| Training objective | masked language modelling (BERT) | next-token prediction | span corruption / denoising (T5), translation |
| Examples | BERT, RoBERTa, DeBERTa | GPT family, Llama, Mistral | T5, BART, original Transformer |
| Best for | classification, NER, embeddings, reranking, retrieval | open-ended generation, chat, code, in-context learning | translation, summarisation, speech-to-text style tasks (Whisper) |

- **Encoder-only** cannot generate fluently, but each token sees full context, so it gives strong, cheap representations.
- **Decoder-only** is one simple stack, trains on any raw text, and uses a single KV cache. Today almost all large chat LLMs are decoder-only.
- **Encoder-decoder** keeps the input representation fixed and reusable. It fits tasks with a clear input and output, but it is more complex to serve and scale.

**Example:** Sentiment classification of 1M reviews on a tight latency budget: fine-tune a small encoder (DeBERTa or similar). Building a chatbot: decoder-only. Translating documents with a smaller specialised model: encoder-decoder.

**Follow-ups:**
- *Can a decoder-only model do classification?* Yes, via prompting or a classification head on the last token. At large scale it often works well, but a small encoder is cheaper.
- *Why did decoder-only win for LLMs?* One objective that uses all tokens, simple scaling, and prompting turns every task into text generation (more in Q16).
- *What is prefix-LM?* A decoder that attends bidirectionally over the prompt and causally over the output.

**Common mistakes:** Saying BERT is a "decoder". Saying decoder-only models cannot understand input (they can, via causal attention over the prompt). Recommending an LLM when a small encoder meets the need at a fraction of the cost.

### Q5 ⭐⭐⭐ 🟡 What is the causal mask? Why can training be parallel over all tokens while generation is sequential?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** The causal mask blocks each token from attending to later tokens, so position t only sees positions up to t. That lets training compute the loss at every position in one pass, while generation must wait for each new token before it can compute the next.

**Then explain:**
- Add `-inf` to the upper triangle of the `(T, T)` score matrix before softmax. Those weights become exactly 0. The mask is lower-triangular: row i can use columns 0..i.
- **Training (teacher forcing):** the full true sequence is known. Input is tokens `x_1..x_T`, targets are `x_2..x_{T+1}`. With the mask, position t's output depends only on `x_1..x_t`, so all T next-token predictions are valid and are computed together in one forward pass.
- **Generation:** token t+1 is not known until token t is sampled. So you need T forward steps. The KV cache makes each step cheap (Q6) but the steps are still sequential.
- Without the mask, the model could copy the answer from the future token during training and would learn nothing useful.

**Example:** Training sequence "I love ML". One pass gives predictions "love" from "I", "ML" from "I love", and so on, giving 3 loss terms from one pass. At inference, to produce "ML" you first need to have produced "love".

**Code:** (executed, torch) changing only the last token leaves earlier outputs unchanged
```python
import torch
torch.manual_seed(0)
T, d = 5, 4
q, k, v = (torch.randn(T, d) for _ in range(3))
mask = torch.tril(torch.ones(T, T, dtype=torch.bool))
def attn(q, k, v):
    s = (q @ k.T) / d**0.5
    return s.masked_fill(~mask, float('-inf')).softmax(-1) @ v
out = attn(q, k, v)
k2, v2 = k.clone(), v.clone(); k2[4] += 10; v2[4] += 10
out2 = attn(q, k2, v2)
print(torch.allclose(out[:4], out2[:4]), not torch.allclose(out[4], out2[4]))
# True True
```

**Follow-ups:**
- *Why `-inf` and not 0?* A score of 0 still gets a non-zero softmax weight. `-inf` gives weight exactly 0. (In practice use a large negative number or `-inf` carefully, since a fully masked row gives NaN.)
- *Is the mask needed in decode with a KV cache?* Not for the single new query: it only sees cached past keys, so causality holds by construction. Prefill still needs it.
- *What about padding?* A separate padding mask is combined with the causal mask.

**Common mistakes:** Saying generation is sequential because of the mask (it is because of autoregressive dependence on sampled tokens). Applying the mask after softmax. Forgetting that the mask is still needed at inference prefill.

### Q6 ⭐⭐⭐ 🟡 What is the KV cache, why does it speed up generation, and how does its memory grow?
**Asked at:** product, big tech, GenAI startups
**Say this first (1 line):** The KV cache stores the keys and values of all past tokens so each decode step only computes K and V for the new token. It trades memory for compute, and the memory grows linearly with sequence length and batch size.

**Then explain:**
- Without a cache, generating token t recomputes K and V for all t previous tokens at every layer. Total work across the whole generation is quadratic in projection work.
- With a cache, each step computes Q, K, V for one token only, appends K, V to the cache, and attends over the cached keys: `(1, d) x (d, t)`.
- Past K and V never change because of the causal mask, so caching is exact, not approximate.
- **Memory formula:** `bytes = 2 * layers * kv_heads * head_dim * seq_len * batch * bytes_per_elem`. The 2 is for K and V.
- Per token it is `2 * layers * kv_heads * head_dim * bytes`.

**Example (computed):**
- Llama-2-7B style (32 layers, 32 KV heads, head_dim 128), fp16: 0.5 MiB per token, so 4096 tokens at batch 1 = 2.00 GiB. At batch 16 that is 32 GiB, more than the 13 GB of fp16 weights.
- Llama-3-8B style (32 layers, 8 KV heads, head_dim 128), fp16: 128 KiB per token, so 8192 tokens = 1.00 GiB.

**Code:** (executed, torch) cached decode equals full recompute
```python
import torch
torch.manual_seed(0)
d, T = 16, 6
Wq, Wk, Wv = (torch.randn(d, d) for _ in range(3))
x = torch.randn(T, d)
def full(x):
    q, k, v = x@Wq, x@Wk, x@Wv
    s = q@k.T/d**0.5
    s = s.masked_fill(torch.triu(torch.ones(len(x), len(x), dtype=torch.bool), 1), float('-inf'))
    return s.softmax(-1)@v
kc, vc, outs = [], [], []
for t in range(T):
    xt = x[t:t+1]
    kc.append(xt@Wk); vc.append(xt@Wv)
    K, V = torch.cat(kc), torch.cat(vc)
    outs.append(((xt@Wq)@K.T/d**0.5).softmax(-1)@V)
print(torch.allclose(torch.cat(outs), full(x), atol=1e-5))   # True
def kv_bytes(L, kvh, hd, seq, b, nb=2): return 2*L*kvh*hd*seq*b*nb
print(kv_bytes(32,32,128,4096,1)/2**30, kv_bytes(32,8,128,8192,1)/2**30)   # 2.0 1.0
```

**Follow-ups:**
- *How do you shrink it?* GQA/MQA/MLA (Q10), quantising the cache to int8/fp8, sliding-window attention, paged allocation (Part 10), evicting or compressing old tokens.
- *Does the cache save attention compute?* It removes recomputation of K, V and of earlier rows. Each step is still O(t) in attention, so total generation is O(n^2) but with a much smaller constant.
- *Why not cache Q?* Old queries are never needed again.

**Common mistakes:** Forgetting the factor 2 (K and V). Using attention heads instead of KV heads for GQA models. Saying the cache makes attention O(1) per step. Ignoring that cache memory, not weights, often limits batch size at long context.

### Q7 ⭐⭐⭐ 🟡 Prefill vs decode: what happens in each phase, and why is decode memory-bandwidth-bound while prefill is compute-bound?
**Asked at:** big tech, product, inference/platform teams
**Say this first (1 line):** Prefill processes the whole prompt at once with big matrix multiplies, so it is limited by GPU compute. Decode generates one token per step and must read all the weights and the KV cache from memory for very little arithmetic, so it is limited by memory bandwidth.

**Then explain:**
- **Prefill:** all prompt tokens run in parallel, fills the KV cache, and produces the first token. Time to first token (TTFT) is driven by this phase. Cost grows with prompt length (linear in weights work, quadratic in attention).
- **Decode:** one token per step per sequence. Each step reads every weight matrix (and the whole KV cache) once. Time per output token (TPOT) is driven by this.
- **Arithmetic intensity** = FLOPs per byte moved. A GPU has a "ridge point" (peak FLOPs / peak bandwidth). Below it you are memory-bound, above it compute-bound.
- Decode at batch 1: about `2P` FLOPs for `2P` bytes (fp16 weights), so about 1 FLOP/byte. An A100 80GB (about 312 TFLOP/s bf16, about 2 TB/s) has a ridge near 150 FLOP/byte. So decode uses roughly 1% of compute.
- Prefill of 2,000 tokens reuses each weight read for 2,000 tokens, so about 2,000 FLOP/byte, well above the ridge: compute-bound.
- Consequences: batching raises decode intensity (batch b gives about b FLOP/byte) so it is almost free until the ridge or the KV cache limits you. Quantised weights cut bytes, so decode speeds up. Prefill and decode are often scheduled separately (chunked prefill, disaggregation).

**Example (computed):** 7B model, fp16, A100 bandwidth about 2 TB/s. Weights are 14 GB, so one decode step needs at least 14e9 / 2e12 = 7 ms, which caps batch-1 decode near 140 tokens/s regardless of FLOPs. Real systems are slower since the KV cache reads and overheads add on.

**Code:** (executed)
```python
P = 7e9
for b in (1, 8, 64, 256):
    print(b, 2*P*b / (2*P), "FLOP/byte")          # 1, 8, 64, 256
print(round(312e12/2.0e12), "FLOP/byte ridge (A100, approx specs)")   # 156
print("batch-1 floor: %.1f ms/token" % (2*P/2.0e12*1e3))               # 7.0
```
Hardware numbers are approximate public specs. The weight-only intensity ignores KV cache reads, which add bytes at long context.

**Follow-ups:**
- *Why doesn't batching help forever?* The KV cache grows with batch, so memory runs out, and attention over the cache is memory-bound per sequence, so it does not get cheaper with batch.
- *Which metric does each phase affect?* Prefill: TTFT. Decode: inter-token latency and throughput.

**Common mistakes:** Saying decode is slow because it has "more compute". Ignoring that batching changes decode intensity. Forgetting that long-context prefill attention is quadratic.

### Q8 ⭐⭐⭐ 🟡 Why does a transformer need positional information? Compare sinusoidal, learned and rotary (RoPE) encodings.
**Asked at:** all types
**Say this first (1 line):** Self-attention treats its input as a set: shuffle the tokens and each token's output is just shuffled with them. So order has to be injected, either added to embeddings (sinusoidal, learned) or built into Q and K (RoPE).

**Then explain:**

| | Sinusoidal | Learned absolute | RoPE |
|---|---|---|---|
| How | fixed sin/cos at different frequencies, added to embeddings | trainable vector per position, added | rotate Q and K by an angle proportional to position |
| Position type | absolute | absolute | relative (through Q.K) |
| Beyond training length | no guarantee in practice | none: no embedding for unseen positions | degrades, but extendable by scaling (Q18) |
| Used in | original Transformer | BERT, GPT-2 | Llama, Mistral, Qwen and most modern LLMs |

- **Sinusoidal:** no parameters. The original paper hypothesised it would let the model attend by relative offset and extrapolate. In practice extrapolation is weak.
- **Learned:** simple and works well within a fixed max length. A hard limit at the trained context.
- **RoPE:** pairs of dimensions are rotated by `pos * theta_i`, where `theta_i = base^(-2i/d)`. The dot product `q_m . k_n` then depends only on `m - n`, giving relative position with no extra parameters, and no added vector to the residual stream.

**Example (computed):** RoPE with random q, k, d = 8. The score at positions (3,1), (13,11), (1003,1001) is the same, -1.763129, because the offset is 2 each time. At offset 4 (positions 5,1) it is -1.302115.

**Code:** (executed, numpy, seed 0)
```python
import numpy as np
rng = np.random.default_rng(0)
def rope(x, pos, base=10000.0):
    d = x.shape[-1]; th = base ** (-np.arange(0, d, 2)/d)
    a = pos*th; c, s = np.cos(a), np.sin(a)
    out = np.empty_like(x)
    out[0::2] = x[0::2]*c - x[1::2]*s
    out[1::2] = x[0::2]*s + x[1::2]*c
    return out
q, k = rng.normal(size=8), rng.normal(size=8)
for m, n in [(3, 1), (13, 11), (1003, 1001)]:
    print(m, n, round(float(rope(q, m) @ rope(k, n)), 6))   # -1.763129 each time
print(round(float(rope(q, 5) @ rope(k, 1)), 6))             # -1.302115 (different offset)
```

**Follow-ups:**
- *Is RoPE applied to V?* No, only Q and K.
- *What is ALiBi?* No embeddings: subtract a head-specific linear penalty times distance from the attention score. It extrapolates to longer lengths better than sinusoidal in the paper's setup.
- *What about no positional encoding?* Causal models can partly infer position from the mask (NoPE research), but standard practice uses RoPE.

**Common mistakes:** Saying RoPE is added to the embedding (it rotates Q and K inside attention). Saying sinusoidal encodings extrapolate perfectly. Not knowing why the dot product is relative (rotation matrices compose: `R_m^T R_n = R_{n-m}`).

### Q9 ⭐⭐⭐ 🟡 Why is self-attention O(n^2), and how do you cope with long sequences?
**Asked at:** all types
**Say this first (1 line):** Every token is scored against every other token, which makes an `n x n` score matrix, so compute grows as `n^2 * d` and a naive implementation also needs `n^2` memory.

**Then explain:**
- `Q K^T` is `(n, d) x (d, n)`, which costs about `n^2 d` multiply-adds. The weights times V costs another `n^2 d`. The feed-forward and projections cost `n d^2`, so attention dominates only when `n` is larger than roughly `d`.
- **Memory:** the `(n, n)` matrix per head per layer. At n = 32,768 in fp16 that is 2 GiB per head per layer. Across 32 heads, 64 GiB if you materialise it for one layer.
- **Ways to cope:**
  - *FlashAttention:* exact, never stores the `n x n` matrix. Memory O(n), compute still O(n^2) (Q11).
  - *Sparse or sliding-window attention* (Longformer, Mistral): each token sees a window w, cost O(n w). Stacked layers still propagate information beyond w.
  - *Linear attention / state-space models (Mamba):* O(n) but a different model with different quality trade-offs.
  - *GQA/MQA and cache compression:* attack the KV cache, not the compute.
  - *Chunking / retrieval (RAG), summarisation:* do not feed everything in.
  - *Position scaling (YaRN etc.):* lets the model handle longer inputs than trained, but does not change cost.

**Example (computed):** n = 4096, window 512: full attention touches 16.8M pairs, windowed about 2.1M, an 8x saving.

**Code:** (executed)
```python
for n in (4096, 32768, 131072):
    print(n, f"{n*n*2/2**30:.2f} GiB per head per layer (fp16)")   # 0.03, 2.00, 32.00
```

**Follow-ups:**
- *Does FlashAttention fix the O(n^2)?* No, it fixes the memory and memory traffic. FLOPs stay quadratic.
- *Which phase suffers more?* Prefill has the quadratic compute. Decode per step is O(n) in attention but reads a large cache.
- *Why not just use linear attention?* Quality on recall-heavy tasks is often worse. Hybrids are being explored.

**Common mistakes:** Saying FlashAttention makes attention linear in time. Forgetting the memory side. Saying cost is O(n^2) in the whole model (the MLP is linear in n).

### Q10 ⭐⭐⭐ 🟡 What are multi-query (MQA) and grouped-query attention (GQA)? How do they shrink the KV cache and what do they cost?
**Asked at:** big tech, product, inference teams
**Say this first (1 line):** MQA shares one K/V head across all query heads, and GQA shares one K/V head per group of query heads. Fewer K/V heads means a proportionally smaller KV cache and less memory traffic in decode, for a small quality cost.

**Then explain:**
- MHA: `H` query heads, `H` K/V heads. MQA: `H` query heads, 1 K/V head. GQA: `H` query heads, `G` K/V heads, with `1 < G < H` and `H` divisible by `G`. Each K/V head serves `H / G` query heads.
- Query projection stays `(D, H*d_h)`. Only `W_k` and `W_v` shrink to `(D, G*d_h)`.
- **Cache size** scales with `G`: it is `H / G` times smaller than MHA. 32 heads with 8 KV heads gives 4x. MQA with 1 KV head gives 32x.
- **Why it helps decode more than prefill:** decode is memory-bound and re-reads the whole cache every step, so smaller cache means faster steps and bigger batches. Prefill is compute-bound, and the attention FLOPs are unchanged (every query head still does its own scores).
- **Cost:** MQA can lose some quality and training can be less stable. GQA recovers most of MHA quality, which is why Llama 2 70B, Llama 3, Mistral 7B and others use it. A model can also be "uptrained" from MHA to GQA by mean-pooling K/V heads and training briefly (GQA paper).

**Example (computed):** per-token-per-layer cache floats for H = 8, d_h = 16: MHA 256, GQA (2 KV heads) 64, MQA 32. Llama-3-8B style: 32 query heads, 8 KV heads, so 128 KiB per token against 512 KiB for MHA (fp16).

**Code:** (executed, torch) GQA via repeating K/V; with `Hkv = H` it matches standard causal attention
```python
import torch
torch.manual_seed(0)
B, T, H, dh = 2, 6, 8, 16
def gqa(q, k, v, Hkv):                 # q:(B,H,T,dh)  k,v:(B,Hkv,T,dh)
    g = q.shape[1] // Hkv
    k = k.repeat_interleave(g, 1); v = v.repeat_interleave(g, 1)
    s = q @ k.transpose(-2, -1) / dh**0.5
    s = s.masked_fill(torch.triu(torch.ones(T, T, dtype=torch.bool), 1), float('-inf'))
    return s.softmax(-1) @ v
q = torch.randn(B, H, T, dh)
for Hkv in (8, 2, 1):
    k = torch.randn(B, Hkv, T, dh); v = torch.randn(B, Hkv, T, dh)
    print(Hkv, tuple(gqa(q, k, v, Hkv).shape), 2*Hkv*dh)    # (2,8,6,16) and 256 / 64 / 32
k = torch.randn(B, H, T, dh); v = torch.randn(B, H, T, dh)
ref = torch.nn.functional.scaled_dot_product_attention(q, k, v, is_causal=True)
print(torch.allclose(gqa(q, k, v, H), ref, atol=1e-5))      # True
```
`repeat_interleave` is for clarity. Production kernels index the shared K/V instead of copying, otherwise you lose the bandwidth saving at compute time. The cache itself stores only `Hkv` heads.

**Follow-ups:**
- *Does GQA reduce FLOPs?* Slightly in the K/V projections, not in the attention scores.
- *How is it related to MLA?* MLA (DeepSeek) compresses K/V into a low-rank latent per token, shrinking the cache even further (Part 01 later question).
- *Convert MHA to GQA?* Mean-pool K/V heads in each group, then fine-tune briefly.

**Common mistakes:** Using the number of query heads in the cache formula for a GQA model. Claiming GQA speeds up prefill by the same factor. Forgetting that group size must divide the head count.

### Q11 ⭐⭐⭐ 🟡 What is FlashAttention? Does it change the result, and why is it faster?
**Asked at:** big tech, product, GenAI startups
**Say this first (1 line):** FlashAttention computes exactly the same attention output, not an approximation. It is faster because it avoids writing the `n x n` score matrix to slow GPU memory (HBM), by working in tiles that stay in fast on-chip SRAM.

**Then explain:**
- Standard attention writes `S = QK^T`, then reads it for softmax, writes `P`, reads it for `P V`. These trips to HBM dominate runtime since attention is memory-bound, not FLOP-bound.
- FlashAttention loads blocks of Q, K, V into SRAM, computes the block's scores, softmax and partial output there, and writes only the final output. Memory use is O(n) instead of O(n^2). FLOPs are the same, so it is still O(n^2) compute.
- **Trick: online softmax.** Softmax needs the max and the sum over all keys. Keep a running max `m`, running sum `l`, and running output `acc`. When a new block raises the max, rescale old values by `exp(m_old - m_new)`.
- **Backward pass:** it does not store the attention matrix. It recomputes scores block-wise from saved row statistics (a small log-sum-exp per row), trading a little extra compute for a lot less memory traffic.
- Later versions (FlashAttention-2, 3) improve work partitioning and use newer hardware features. The idea is unchanged. It supports causal masks by skipping fully masked blocks.

**Example:** n = 32,768, fp16: the score matrix is 2 GiB per head per layer. FlashAttention never builds it, which is what makes long-context training and inference fit in memory.

**Code:** (executed, numpy) tiled online softmax equals standard attention
```python
import numpy as np
rng = np.random.default_rng(0)
n, d, Bk = 12, 4, 4
Q, K, V = (rng.normal(size=(n, d)) for _ in range(3))
S = Q @ K.T / np.sqrt(d); P = np.exp(S - S.max(1, keepdims=True)); P /= P.sum(1, keepdims=True)
ref = P @ V
out = np.zeros((n, d))
for i in range(n):
    m, l, acc = -np.inf, 0.0, np.zeros(d)
    for j in range(0, n, Bk):                 # stream over key blocks
        s = Q[i] @ K[j:j+Bk].T / np.sqrt(d)
        m_new = max(m, s.max()); scale = np.exp(m - m_new)
        p = np.exp(s - m_new)
        l = l*scale + p.sum(); acc = acc*scale + p @ V[j:j+Bk]; m = m_new
    out[i] = acc / l
print(np.allclose(out, ref))   # True
```
This shows the math only. The real speed comes from the fused GPU kernel, which this snippet does not reproduce. In PyTorch, `F.scaled_dot_product_attention` dispatches to a flash kernel when available.

**Follow-ups:**
- *Does it change results?* Not mathematically. Floating-point results can differ in the last bits because the summation order differs.
- *Does it help decode?* Less, since decode is dominated by reading the KV cache. Specialised "flash-decoding" kernels split the key dimension for parallelism.
- *Is it sparse or approximate attention?* No. That is a common confusion.

**Common mistakes:** Saying it reduces FLOPs or makes attention linear-time. Saying it is approximate. Not mentioning IO / memory hierarchy as the actual reason for the speed-up.

### Q12 ⭐⭐⭐ 🟡 Walk through a transformer block: residual connections, normalisation, feed-forward network. Pre-LN vs post-LN?
**Asked at:** all types
**Say this first (1 line):** A block is attention then a feed-forward network, each wrapped with a residual connection and a normalisation layer. Modern LLMs put the norm before each sub-layer (pre-LN) because it trains more stably than the original post-LN.

**Then explain:**
- **Attention sub-layer:** mixes information across tokens.
- **FFN sub-layer:** applied to each token independently: `Linear(D -> 4D) -> activation -> Linear(4D -> D)`. This is where most parameters sit and it works like a per-token memory/transform. Llama-style models use a gated SwiGLU FFN with hidden size about 8/3 D to keep parameter count similar.
- **Residual connection:** `x + f(x)`. Gives gradients a direct path through depth, so deep stacks train.
- **Normalisation:** LayerNorm (or RMSNorm in Llama-style models, which skips mean-centering) keeps activation scale under control.
- **Post-LN (original 2017):** `x = LN(x + Attn(x))`, then `x = LN(x + FFN(x))`. The norm sits on the residual path, which can make gradients near the output large at initialisation, so it needs learning-rate warm-up and is fragile when deep.
- **Pre-LN (GPT-2, Llama):** `x = x + Attn(LN(x))`, `x = x + FFN(LN(x))`. The residual path stays an identity, so training is more stable and often needs less warm-up. Trade-off: reported to give slightly worse final quality at the same depth in some studies, and the residual stream's magnitude grows with depth (a final norm is added before the output head).
- **Parameter count:** per block about `4D^2` (attention) + `8D^2` (FFN with 4x expansion) = `12 D^2`, ignoring biases and norms.

**Example (computed):** D = 64: formula gives 12 x 4096 = 49,152. A real PyTorch block with biases and two LayerNorms has 49,984, the extra being biases and norm parameters.

**Code:** (executed, torch)
```python
import torch, torch.nn as nn
torch.manual_seed(0)
class Block(nn.Module):
    def __init__(s, D=64, H=4, pre=True):
        super().__init__(); s.pre = pre
        s.ln1, s.ln2 = nn.LayerNorm(D), nn.LayerNorm(D)
        s.attn = nn.MultiheadAttention(D, H, batch_first=True)
        s.ffn = nn.Sequential(nn.Linear(D, 4*D), nn.GELU(), nn.Linear(4*D, D))
    def forward(s, x):
        T = x.shape[1]; m = torch.triu(torch.ones(T, T, dtype=torch.bool), 1)
        if s.pre:
            h = s.ln1(x); x = x + s.attn(h, h, h, attn_mask=m, need_weights=False)[0]
            return x + s.ffn(s.ln2(x))
        x = s.ln1(x + s.attn(x, x, x, attn_mask=m, need_weights=False)[0])
        return s.ln2(x + s.ffn(x))
b = Block(); x = torch.randn(2, 10, 64)
print(b(x).shape, sum(p.numel() for p in b.parameters()))   # torch.Size([2, 10, 64]) 49984
```

**Follow-ups:**
- *LayerNorm vs RMSNorm?* RMSNorm divides by the root mean square only, with no mean subtraction or bias. It is cheaper and works about as well.
- *Why 4x expansion?* A convention from the original paper. It balances capacity against cost.
- *What is the residual stream view?* Each sub-layer reads from and writes additions into a shared vector per token.

**Common mistakes:** Placing the norm in the wrong spot and calling it pre-LN. Saying pre-LN is strictly better (it is more stable, quality claims are mixed). Forgetting that the FFN holds about two thirds of block parameters.

### Q13 ⭐⭐⭐ 🟡 Code: implement causal scaled dot-product (multi-head) self-attention from scratch in PyTorch or NumPy.
**Asked at:** product, big tech, live-coding rounds
**Say this first (1 line):** Project x to Q, K, V, split into heads, compute `softmax(QK^T / sqrt(d_head) + causal_mask) V` per head, merge the heads, and apply an output projection.

**Then explain:**
- Shapes: input `(B, T, D)`. After the QKV projection and the head split, Q, K and V are each `(B, H, T, dh)` with `dh = D/H`. Scores are `(B, H, T, T)`. Output is back to `(B, T, D)`.
- Causal mask: set scores where key index > query index to `-inf` **before** softmax. Those weights become exactly 0 and each row still sums to 1. Masking after softmax breaks the row sums.
- Scale by `sqrt(dh)`, the head dim, not `sqrt(D)` (see Q17). Softmax goes over the last dim (the keys).
- After `transpose(1, 2)` the tensor is not contiguous, so use `.contiguous().view(...)` or `.reshape(...)`.
- Cost: scores take O(B·H·T²·dh) time and O(B·H·T²) memory if you materialise them. That is what FlashAttention avoids (see Q11).

**Example:** B=2, T=6, D=32, H=4 gives dh=8 and scores of shape (2, 4, 6, 6). In the test below, changing the last token leaves outputs at positions 0 to T-2 unchanged. That is the causality test.

**Code:** (run with torch 2.14 CPU)
```python
import math, torch
import torch.nn.functional as F

class CausalMHA(torch.nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.h, self.dh = n_heads, d_model // n_heads
        self.qkv = torch.nn.Linear(d_model, 3 * d_model, bias=False)
        self.out = torch.nn.Linear(d_model, d_model, bias=False)

    def forward(self, x):                       # x: (B, T, D)
        B, T, D = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)  # each (B, T, D)
        q, k, v = (t.view(B, T, self.h, self.dh).transpose(1, 2) for t in (q, k, v))  # (B,H,T,dh)
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.dh)      # (B, H, T, T)
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), 1)
        scores = scores.masked_fill(mask, float("-inf"))           # block the future
        w = scores.softmax(dim=-1)                                 # over keys
        o = w @ v                                                  # (B, H, T, dh)
        o = o.transpose(1, 2).contiguous().view(B, T, D)           # merge heads
        return self.out(o)

torch.manual_seed(0)
B, T, D, H = 2, 6, 32, 4
m = CausalMHA(D, H); x = torch.randn(B, T, D); y = m(x)
q, k, v = m.qkv(x).chunk(3, -1)
q, k, v = (t.view(B, T, H, D // H).transpose(1, 2) for t in (q, k, v))
ref = m.out(F.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, T, D))
print("max abs diff vs SDPA:", (y - ref).abs().max().item())      # 1.3e-07
x2 = x.clone(); x2[:, -1] += 10
print("earlier positions unchanged:", torch.allclose(m(x2)[:, :-1], y[:, :-1]))  # True
```
Output from my run: shape `(2, 6, 32)`, max diff vs `scaled_dot_product_attention` 1.3e-07, causality check True.

**Follow-ups:**
- *Add a KV cache?* At decode time compute q, k, v only for the new token, append k and v to the cache, and attend over all cached keys. No mask is needed for a single query (see Q35).
- *GQA?* Project K and V to `n_kv` heads and repeat each one `H/n_kv` times before the matmul (see Q10).
- *Padding / ragged batches?* Add a key-padding mask on top of the causal mask. Make sure no row is fully `-inf`, or softmax returns NaN.
- *fp16?* Compute softmax in fp32, or use `finfo.min` instead of `-inf`.

**Common mistakes:** softmax over the wrong dim; masking after softmax; scaling by `sqrt(D)`; `view` after `transpose` without `contiguous`; mixing up `(B, T, H, dh)` and `(B, H, T, dh)`; forgetting the output projection `W_o`; building the mask on the wrong device.

### Q14 ⭐⭐⭐ 🟡 Walk through one forward pass of a decoder-only LLM, from text to next-token probabilities.
**Asked at:** all types
**Say this first (1 line):** Tokenise, look up embeddings, run N identical blocks (attention + FFN, each with a residual), apply a final norm, project to vocabulary logits, and softmax the last position to get the next-token distribution.

**Then explain:** (shapes for batch B, T tokens, model dim D, vocab V)
1. **Tokenise:** text becomes integer ids `(B, T)`. Tokenizers are covered in Part 2.
2. **Embed:** table lookup gives `(B, T, D)`. There is no position vector added in Llama-style models.
3. **Each block, repeated L times (pre-norm):**
   - `x = x + Attn(RMSNorm(x))`. Project to Q, K, V, apply **RoPE** to Q and K (that is where position enters), then causal attention, merge heads, and apply W_o.
   - `x = x + FFN(RMSNorm(x))`. Usually SwiGLU, applied to each token independently.
4. **Final norm**, then the **LM head** (unembedding), a linear layer `D -> V`. This gives logits `(B, T, V)`.
5. **Softmax over the last position** `logits[:, -1]` gives `P(next token | all previous)`. Then you sample or take argmax (decoding strategies are in Part 2).
- In training, every position's logits are scored against the next token in one pass (that is the causal-mask parallelism from Q5). At inference only the last row is needed.
- During generation, step 1 to 5 run once over the whole prompt (prefill), then one token at a time with the KV cache (see Q6, Q7).

**Example:** Tiny model: V=100, D=32, 4 heads, 2 layers, 7 tokens. The shapes I printed: ids `(1,7)`, embeddings `(1,7,32)`, after blocks `(1,7,32)`, logits `(1,7,100)`, next-token probs `(1,100)` summing to 1.0.

**Code:** (run, torch 2.14 CPU; random weights, so it shows shapes, not language)
```python
import torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0)
V, D, H, L, T, B = 100, 32, 4, 2, 7, 1
dh = D // H
def rms(x, w, eps=1e-6): return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * w
def rope(x, base=10000.0):                      # x: (B,H,T,dh), rotate pairs of dims by pos * theta_i
    T, dh = x.shape[-2], x.shape[-1]
    inv = base ** (-torch.arange(0, dh, 2).float() / dh)
    ang = torch.arange(T).float()[:, None] * inv[None]
    c, s = ang.cos(), ang.sin()
    x1, x2 = x[..., 0::2], x[..., 1::2]
    return torch.stack([x1*c - x2*s, x1*s + x2*c], -1).flatten(-2)
emb = nn.Embedding(V, D); head = nn.Linear(D, V, bias=False); nf = torch.ones(D)
layers = [dict(wqkv=nn.Linear(D, 3*D, bias=False), wo=nn.Linear(D, D, bias=False),
               g=nn.Linear(D, 4*D, bias=False), u=nn.Linear(D, 4*D, bias=False),
               d=nn.Linear(4*D, D, bias=False), n1=torch.ones(D), n2=torch.ones(D)) for _ in range(L)]
ids = torch.randint(0, V, (B, T)); x = emb(ids)
for l in layers:
    q, k, v = l["wqkv"](rms(x, l["n1"])).chunk(3, -1)
    q, k, v = (t.view(B, T, H, dh).transpose(1, 2) for t in (q, k, v))
    a = F.scaled_dot_product_attention(rope(q), rope(k), v, is_causal=True)
    x = x + l["wo"](a.transpose(1, 2).reshape(B, T, D))
    h = rms(x, l["n2"]); x = x + l["d"](F.silu(l["g"](h)) * l["u"](h))
logits = head(rms(x, nf)); p = logits[:, -1].softmax(-1)
print(tuple(logits.shape), tuple(p.shape), round(p.sum().item(), 4))   # (1, 7, 100) (1, 100) 1.0
```

**Follow-ups:**
- *Where do most FLOPs and parameters go?* The FFN holds about two-thirds of the block parameters, and attention the rest (see Q21, Q26). Attention FLOPs grow with T².
- *What changes at generation time?* Only the new token goes through the stack. Its K and V are appended to the cache, so each step costs O(T) attention instead of O(T²).
- *Why take only the last position?* Earlier rows predict tokens you already know.

**Common mistakes:** saying position is added at the input in modern LLMs (RoPE acts inside attention on Q and K); forgetting the final norm; applying softmax before the LM head; saying the whole sequence is re-sampled each step; confusing logits (unnormalised) with probabilities.

### Q15 ⭐⭐⭐ 🟡 Live maths: estimate parameter count and KV-cache memory for a Llama-style model (layers, heads, head dim, context, batch).
**Asked at:** big tech, product, inference/platform teams
**Say this first (1 line):** Parameters come to about `12·L·d²` plus embeddings, and KV cache is `2 · L · n_kv · d_head · T · B · bytes`. For Llama-2-7B that is 6.7B parameters and 0.5 MiB of cache per token.

**Then explain:**
- **Config I assume (Llama-2-7B):** L=32, d=4096, 32 heads, n_kv=32 (full MHA), d_head=128, SwiGLU hidden 11008, vocab 32000, untied embeddings, fp16 (2 bytes).
- **Per layer:**
  - Attention: `Wq + Wk + Wv + Wo = 4·d² = 67.1M`.
  - SwiGLU FFN: 3 matrices, `3·d·11008 = 135.3M`.
  - Norms: `2d`, negligible.
  - Total about 202.4M per layer.
- **Total:** 32 × 202.4M = 6.48B, plus embeddings `V·d = 131M` and LM head `131M` (untied) = **6.74B**. Weights in fp16 are 12.6 GiB.
- **Quick check:** `12·L·d² = 12·32·4096² = 6.44B`. This works because attention is 4d² and the FFN is about 8d² (hidden 8/3·d times 3 matrices). Then add `2·V·d`.
- **KV cache** (the 2 is for K and V): `2 · 32 · 32 · 128 · 2 bytes = 524,288 B = 512 KiB per token`.
- **GQA variant (Llama-3-8B-like):** L=32, d=4096, 32 query heads, **n_kv=8**, d_head=128, FFN 14336, vocab 128256, untied. Parameters come to 8.03B (attention drops to 41.9M per layer because K and V are 4x smaller). KV is **128 KiB per token**, 4x less.

| Case (fp16) | Llama-2-7B (MHA) | Llama-3-8B (GQA, n_kv=8) |
|---|---|---|
| T=4096, B=1 | 2.0 GiB | 0.5 GiB |
| T=32768, B=1 | 16.0 GiB | 4.0 GiB |
| T=4096, B=32 | 64.0 GiB | 16.0 GiB |

**Example:** serving Llama-2-7B at batch 32 and 4k context needs 12.6 GiB of weights plus 64 GiB of cache. The cache is five times the weights. This is why batch size and context are capped by KV memory, not by weights (see Q23, and PagedAttention in Part 10).

**Code:** (run)
```python
def params(L, d, n_h, n_kv, dh, ffn, V):          # untied embeddings, SwiGLU
    attn = d*n_h*dh + 2*d*n_kv*dh + n_h*dh*d       # Wq, Wk+Wv, Wo
    per = attn + 3*d*ffn + 2*d
    return L*per + 2*V*d + d
def kv_bytes(L, n_kv, dh, T, B, b=2): return 2*L*n_kv*dh*T*B*b
print(params(32,4096,32,32,128,11008,32000))   # 6738415616
print(params(32,4096,32, 8,128,14336,128256))  # 8030261248
print(kv_bytes(32,32,128,4096,32)/2**30, kv_bytes(32,8,128,4096,32)/2**30)  # 64.0 16.0
```

**Follow-ups:**
- *Does the cache depend on d_ffn or vocab?* No. Only layers, KV heads, head dim, length, batch and dtype.
- *What if the cache is int8?* Halve it (plus a small scale overhead).
- *Training memory?* Weights + gradients + Adam states, about 16 bytes per parameter for mixed precision with fp32 master weights. That is a separate calculation from the KV cache.

**Common mistakes:** forgetting the factor 2 (K and V); using `n_heads` instead of `n_kv` heads for GQA; mixing GB and GiB; using bytes=4 for fp16; forgetting the third SwiGLU matrix; ignoring the embedding and LM head (large for 128k vocabularies); forgetting batch in the cache.

### Q16 ⭐⭐ 🟡 BERT vs GPT: pretraining objectives, attention pattern, typical uses. Why did decoder-only models come to dominate?
**Asked at:** all types
**Say this first (1 line):** BERT is a bidirectional encoder trained to fill in masked tokens, so it is good at understanding. GPT is a causal decoder trained to predict the next token, so it generates. Decoder-only won because one simple objective scales, and the same model can do almost any task through prompting.

**Then explain:**

| | BERT (encoder-only) | GPT (decoder-only) |
|---|---|---|
| Objective | Masked LM: hide about 15% of tokens and predict them. The original also had next-sentence prediction, which RoBERTa later dropped. | Next-token prediction on every position |
| Attention | Bidirectional (each token sees left and right) | Causal (left only; see Q5) |
| Output | A vector per token, so you add a head (classifier, span, tagger) | Text, token by token |
| Typical use | Classification, NER, embeddings, rerankers, search | Chat, code, generation, agents |

- **Why decoder-only dominates:**
  - Every position gives a training signal, whereas BERT learns from only about 15% of positions per pass.
  - Generation is natively supported, so there is no separate decoder or task head. Prompting and few-shot examples turn one model into a classifier, summariser or translator (in-context learning appeared as models scaled).
  - The training signal is simple and scales cleanly with data and compute (scaling laws, Part 2).
  - Inference is simple: one stack and a KV cache (Q6).
  - Instruction tuning and RLHF (Part 5) fit naturally on top of a generative model.
- **Not dead:** encoders still win where you need cheap, fast, bidirectional representations: embedding models, cross-encoder rerankers, classifiers, and a small model per task (see Q4).

**Example:** classify a support ticket. With BERT you fine-tune on labelled tickets, which gives low latency, a small model and an exact label set. With a GPT-style LLM you write a prompt and get a label with no training data, but it costs more per call.

**Follow-ups:**
- *Can BERT generate text?* Only awkwardly (iterative mask filling). It was not trained to model the next token.
- *Is a decoder worse at understanding?* A big decoder matches or beats encoders on most benchmarks. At equal parameters and for classification, encoders are often more efficient.
- *What about T5?* Encoder-decoder with span corruption. It is strong for seq2seq, but the industry moved to decoder-only for generality and simplicity.

**Common mistakes:** saying BERT is "bidirectional so it is better, period" (it cannot generate); forgetting that decoder-only models mask the future; saying GPT has no encoder because "it doesn't understand" (the decoder stack builds representations too); ignoring that masked LM uses only about 15% of tokens for loss.

### Q17 ⭐⭐ 🟡 Why do we divide attention scores by sqrt(d_k)? Give the variance argument.
**Asked at:** product, big tech
**Say this first (1 line):** A dot product of two d_k-dimensional vectors has variance about d_k, so its size grows like `sqrt(d_k)`. Dividing by `sqrt(d_k)` brings the variance back to about 1, so softmax does not saturate and gradients survive.

**Then explain:**
- Assume the components of q and k are independent, with mean 0 and variance 1 (roughly true at initialisation after LayerNorm and with a standard init).
- `q·k = sum_i q_i k_i`. Each term has mean 0 and variance 1, and they are independent, so `Var(q·k) = d_k` and the standard deviation is `sqrt(d_k)`.
- Dividing by `sqrt(d_k)` gives `Var = d_k / d_k = 1`, independent of head size.
- Without scaling, the logits are large (for d_k=64 they are typically around ±8). Softmax of large logits is nearly one-hot. Its Jacobian `diag(p) - p p^T` is then close to 0, so gradients vanish and training stalls or is unstable.
- Why not divide by d_k? That over-shrinks the variance to `1/d_k` and attention becomes nearly uniform. Why not `sqrt(d_model)`? The sum runs over the head dimension, so d_k is the right number.

**Example:** 64 random keys per query, softmax over them (my simulation, 2000 queries). The table shows the average of the largest attention weight.

| d_k | Var of raw score | Var after scaling | Mean max weight, raw | Mean max weight, scaled |
|---|---|---|---|---|
| 4 | 4.1 | 1.01 | 0.283 | 0.108 |
| 64 | 64.0 | 1.0 | 0.783 | 0.106 |
| 512 | 511.1 | 1.0 | 0.927 | 0.106 |

Unscaled at d_k=512, the top key takes about 93% of the weight on random data. Scaled, it stays around 0.11 regardless of d_k.

**Code:** (run, NumPy seed 0)
```python
import numpy as np
rng = np.random.default_rng(0)
def softmax(z): e = np.exp(z - z.max(-1, keepdims=True)); return e / e.sum(-1, keepdims=True)
for dk in [4, 64, 512]:
    Q = rng.standard_normal((2000, dk)); K = rng.standard_normal((2000, 64, dk))
    raw = np.einsum('nd,nkd->nk', Q, K)                       # one score per (query, key)
    print(dk, round(raw.var(), 1), round((raw / np.sqrt(dk)).var(), 2),
          round(softmax(raw).max(1).mean(), 3), round(softmax(raw / np.sqrt(dk)).max(1).mean(), 3))
```

**Follow-ups:**
- *Does it hold after training?* Not exactly, since trained q and k are not unit-variance. It is an initialisation-time argument, and some large models add QK-norm for stability instead (see Q44).
- *Is it the same as a temperature?* Yes. It is a fixed softmax temperature of `sqrt(d_k)`.
- *Where does it matter most?* Large head dims, and low precision (fp16/bf16), where big logits also risk overflow.

**Common mistakes:** saying "it keeps numbers small" with no variance argument; dividing by `sqrt(d_model)`; claiming the variance is 1 for the unscaled dot product; forgetting the independence and zero-mean assumptions; saying scaling changes which key is largest (it does not, argmax is the same, only sharpness changes).

### Q18 ⭐⭐ 🟡 How does RoPE work, and how do position interpolation, NTK-aware scaling and YaRN extend context length?
**Asked at:** product, GenAI startups, big tech
**Say this first (1 line):** RoPE rotates each pair of dimensions of q and k by an angle proportional to the token position, so the q·k score depends only on the relative distance. To go beyond the trained length you squeeze or re-scale those angles so the model never sees positions it was not trained on.

**Then explain:**
- **How RoPE works:** split the head dim into d/2 pairs. For pair i, the rotation angle at position m is `m · theta_i` with `theta_i = base^(-2i/d)` (base 10000 in the original; Llama-3 uses 500000). Rotating q at position m and k at position n gives a score that depends on `m - n`. Low i means a high frequency (fast rotation, local detail); high i means a low frequency (slow rotation, long range). Code is in Q42.
- **The problem:** past the trained length L, the low-frequency pairs reach angles never seen in training, and quality collapses.
- **Position interpolation (PI):** divide positions by the scale `s = L_new / L_old`, so `m -> m/s`. All positions fit inside the trained range. It needs a short fine-tune, and it blurs nearby tokens because high-frequency dims are compressed too.
- **NTK-aware scaling:** do not compress everything. Increase the base (`base' = base · s^(d/(d-2))`), which stretches the low frequencies a lot and the high frequencies hardly at all. This keeps local resolution and works somewhat even without fine-tuning.
- **YaRN:** treat each frequency band differently. High-frequency dims are left alone, low-frequency dims are interpolated, and a ramp blends the middle ("NTK-by-parts"). It also applies a mild attention temperature (logit scaling) to correct for the entropy shift at long length. It needs a small amount of long-context fine-tuning and reaches long contexts cheaply.

| Method | What changes | Fine-tune? |
|---|---|---|
| PI | positions / s | yes, short |
| NTK-aware | base is increased | helps zero-shot, better with a little tuning |
| YaRN | per-band interpolation + temperature | small, efficient |

**Example:** a model trained at 4k that you want at 16k. PI uses s=4, so position 16000 behaves like 4000. NTK-aware instead raises the base so slow dims cover 16k while fast dims stay near their original speed.

**Follow-ups:**
- *Does extending the window guarantee good long-context quality?* No. You still need long-context data and evaluation (see Q19).
- *Cache before or after RoPE?* Typically K is cached after rotation, which is why positions must stay consistent. Some systems cache pre-RoPE keys to allow window shifts.
- *Why is RoPE better than learned absolute positions here?* Learned tables have no entries past the trained length, whereas RoPE at least has a formula.

**Common mistakes:** saying RoPE is added to the embedding (it rotates q and k inside attention); saying it adds parameters (it has none); saying PI/YaRN need no training (they usually need a short fine-tune); saying NTK-aware is the same as PI; forgetting that Q is rotated too.

### Q19 ⭐⭐ 🟡 What is the context window, and why is the effective context often shorter than the advertised one ("lost in the middle")?
**Asked at:** all types
**Say this first (1 line):** The context window is the maximum number of tokens (prompt plus generated output) the model can attend to in one request. The usable context is often shorter because the model is trained mostly on shorter sequences, attention gets diluted over many tokens, and models use the start and end of the prompt better than the middle.

**Then explain:**
- **What counts:** input tokens + output tokens (+ any reasoning tokens) must fit. Bigger windows cost more: KV cache memory grows linearly (Q6, Q15), prefill compute grows roughly quadratically with length (Q9).
- **Why effective < advertised:**
  - Most pretraining data is short. Long contexts are often added late by RoPE scaling plus brief fine-tuning (Q18), so long-range skills are less practised.
  - Softmax attention spreads over more tokens. With thousands of distractors, the signal from the relevant tokens is diluted.
  - **Lost in the middle** (Liu et al., 2023): on multi-document QA and key-value retrieval, accuracy was highest when the relevant information was at the start or end of the context and dropped when it was in the middle (a U shape). Newer models reduce it, but you should not assume it is gone.
- **Needle-in-a-haystack is too easy:** finding one planted sentence tests lookup, not reasoning. Multi-needle, aggregation and multi-hop long-context benchmarks (RULER-style) usually show a lower effective length than the advertised one.
- **Practical mitigations:**
  - Put instructions and the key facts at the start and end.
  - Retrieve and rerank so you send the top few chunks instead of everything (Parts 6 and 7).
  - Trim and summarise history.
  - Evaluate on your own task at the lengths you actually use.

**Example:** a 128k-window model, 100 retrieved chunks, answer in chunk 50. Sending all 100 is slower, costs more, and may do worse than sending the best 8 chunks with the strongest at the edges.

**Follow-ups:**
- *Does a longer window replace RAG?* Not usually. Cost, latency, freshness, access control and the middle-of-context problem still favour retrieval for large corpora.
- *How would you measure effective context?* Run your task with the gold information at several depths and total lengths, and plot accuracy against both.
- *Is the cost only about money?* No, also latency: prefill time grows with prompt length (see Q7).

**Common mistakes:** saying "128k window means 128k of reliable memory"; forgetting that output tokens share the window; claiming lost-in-the-middle is a bug in attention code (it is an emergent behaviour); trusting single-needle tests as proof of long-context ability; stating that the problem is fixed in all current models.

### Q20 ⭐⭐ 🟡 LayerNorm vs RMSNorm: what changes and why do modern LLMs prefer RMSNorm?
**Asked at:** product, GenAI startups
**Say this first (1 line):** RMSNorm drops the mean-subtraction and the bias of LayerNorm. It only rescales by the root-mean-square, so it is a bit cheaper and works just as well in practice.

**Then explain:**
- **LayerNorm:** `y = (x - mean) / sqrt(var + eps) * gamma + beta`. It re-centres and re-scales, with 2d parameters per norm.
- **RMSNorm:** `y = x / sqrt(mean(x^2) + eps) * gamma`. There is no re-centring and no beta, so it has d parameters and fewer reductions (one statistic instead of two).
- **Why LLMs prefer it:**
  - Empirically it gives about the same quality (the RMSNorm paper argues re-scaling is what matters, not re-centring).
  - It is simpler and cheaper, which matters because there are two norms per layer, run on every token. The saving is mostly memory traffic and fused-kernel simplicity, not FLOPs.
  - No bias terms fits the modern "no biases" recipe (Llama, Qwen; see Q39).
- **Note:** if the input already has zero mean per token, the two are identical (apart from beta). The output of RMSNorm has unit RMS, not zero mean.

**Example (checked):** on a tensor with mean about 1.5 and std 3 per token (d=4096), LayerNorm outputs mean 0.0 and std 1.0. RMSNorm outputs RMS 1.0 but mean 0.44. After subtracting the mean first, the two match (`allclose` True). Parameters: LayerNorm 8192 vs RMSNorm 4096.

**Code:** (run)
```python
import torch
torch.manual_seed(0)
x = torch.randn(2, 5, 4096) * 3 + 1.5
ln = torch.nn.LayerNorm(4096, eps=1e-6)
def rmsnorm(x, w, eps=1e-6):
    return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * w
y_ln, y_rms = ln(x), rmsnorm(x, torch.ones(4096))
print(y_ln.mean().item(), y_ln.std().item())        # about 0.0, 1.0
print(y_rms.mean().item(), y_rms.pow(2).mean().sqrt().item())  # about 0.44, 1.0
xc = x - x.mean(-1, keepdim=True)
print(torch.allclose(ln(xc), rmsnorm(xc, torch.ones(4096)), atol=1e-4))  # True
```
I also timed both in eager PyTorch on CPU and saw no speed gain for a naive RMSNorm, so the speed benefit depends on fused kernels and GPU memory traffic. Do not claim a number you have not measured on your own hardware.

**Follow-ups:**
- *Pre-norm or post-norm?* Modern LLMs use pre-norm with RMSNorm (see Q12).
- *Why compute norms in fp32?* The mean of squares can overflow or lose precision in fp16/bf16, so implementations upcast.
- *What is QK-norm?* An RMSNorm applied to q and k to bound attention logits (see Q44).

**Common mistakes:** saying RMSNorm "removes normalisation"; saying it has no learnable scale (it has gamma); claiming big accuracy gains (it is mainly an efficiency and simplicity choice); forgetting that LayerNorm also has a bias; saying the saving is in FLOPs when it is mostly memory-bound ops.

### Q21 ⭐⭐ 🟡 What does the feed-forward network do in a transformer? Explain GELU vs SwiGLU/gated FFNs and where most parameters live.
**Asked at:** product, GenAI startups
**Say this first (1 line):** Attention mixes information across tokens. The FFN then processes each token on its own, with a large non-linear expand-and-project step, and it holds about two-thirds of the parameters in a block.

**Then explain:**
- **Classic FFN:** `W2 · GELU(W1 x)`. It expands from d to 4d and projects back. Parameters: `2 · d · 4d = 8d²`. Without it, a stack of attention layers would be mostly linear mixing of values and would have little non-linear capacity.
- **Gated FFN (SwiGLU):** `W_down · ( SiLU(W_gate x) ⊙ (W_up x) )`. One path is a learned "gate" that multiplies the other element-wise. It has 3 matrices, so to keep parameters equal, the hidden size is cut to about `8/3 · d` instead of 4d. Shazeer (2020) found gated variants gave better quality at equal compute, and Llama, Qwen, Mistral and PaLM-style models use them.
- **Where parameters live:** attention is `4d²` (Wq, Wk, Wv, Wo, with full MHA). A GELU FFN is `8d²` and so is a SwiGLU FFN at hidden 8/3·d. So the FFN is about 2/3 of the block. For Llama-2-7B: attention 67.1M vs FFN 135.3M per layer, FFN share 66.8%.
- **Intuition (an interpretation, not a proof):** FFN layers act like key-value memories storing facts and patterns, while attention routes information between positions. Mixture-of-Experts replaces the FFN with many experts (Q34) because that is where capacity sits.
- **Position-wise:** the same weights are applied to every token, with no interaction between tokens inside the FFN.

**Example (checked, d=4096):** GELU FFN with hidden 4d has 134,217,728 parameters. SwiGLU with hidden 11008 (Llama-2-7B; 8/3·4096 = 10923, rounded up to a multiple of 256) has 135,266,304. Almost identical size, different shape.

**Code:** (run)
```python
import torch, torch.nn as nn, torch.nn.functional as F
class SwiGLU(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.gate = nn.Linear(d, h, bias=False); s.up = nn.Linear(d, h, bias=False); s.down = nn.Linear(h, d, bias=False)
    def forward(s, x): return s.down(F.silu(s.gate(x)) * s.up(x))
m = SwiGLU(64, 172)
print(m(torch.randn(2, 5, 64)).shape, sum(p.numel() for p in m.parameters()))  # torch.Size([2, 5, 64]) 33024
```

**Follow-ups:**
- *Why not just use 4d with SwiGLU?* It would have 1.5x the FFN parameters, so it is no longer a fair comparison. Llama cuts the hidden size to keep the budget.
- *Is GELU vs ReLU important?* Smooth activations (GELU, SiLU) train a bit better. The gating matters more than the exact activation.
- *Does the FFN cost more FLOPs than attention?* At short contexts yes (FFN dominates). At very long contexts the T² attention term takes over.

**Common mistakes:** saying the FFN mixes tokens (it does not); saying attention holds most parameters; forgetting SwiGLU has three matrices; comparing SwiGLU at hidden 4d against GELU at 4d as if the sizes were equal; saying GELU is "gated" (it is a plain activation).

### Q22 ⭐⭐ 🟡 What is cross-attention, where is it used (T5, Whisper, diffusion, multimodal) and how does it differ from self-attention?
**Asked at:** all types
**Say this first (1 line):** Cross-attention is attention where the queries come from one sequence and the keys and values come from a different one, so one stream can read from another.

**Then explain:**
- **Self-attention:** Q, K and V all come from the same sequence. **Cross-attention:** `Q = W_q · x_decoder`, `K = W_k · x_other`, `V = W_v · x_other`. The score matrix is `(T_q, T_kv)`, not square.
- **No causal mask** over the other sequence. The decoder can look at all of the encoder output (the decoder's own self-attention stays causal).
- **Output length** equals the query length, `T_q`. The cost is O(T_q · T_kv), so a long source gets expensive, but the K and V of the source can be computed **once** and reused for every decoding step.
- **Where it is used:**
  - **T5 / original transformer / BART:** the decoder attends to the encoder's output in every layer (translation, summarisation).
  - **Whisper:** the text decoder attends to the audio encoder's features.
  - **Diffusion models (Stable Diffusion-style):** image latents are the queries and the text-encoder embeddings are the keys and values, which is how the prompt conditions the image.
  - **Multimodal LLMs:** some designs insert cross-attention layers so text queries read image features (Flamingo-style). Others skip it and simply concatenate image tokens into the text sequence (see Q31).

**Example:** translating a 12-token English sentence into 9 French tokens so far. Cross-attention weights have shape `(heads, 9, 12)`, and each French token distributes its attention over the English tokens.

**Code:** (run, torch 2.14)
```python
import math, torch
import torch.nn.functional as F
torch.manual_seed(0)
B, Tq, Tk, D, H = 2, 3, 10, 32, 4
dh = D // H
Wq, Wk, Wv = (torch.nn.Linear(D, D, bias=False) for _ in range(3))
dec = torch.randn(B, Tq, D)      # queries: decoder / text side
enc = torch.randn(B, Tk, D)      # keys, values: encoder / image / audio side
sp = lambda t, T: t.view(B, T, H, dh).transpose(1, 2)
q, k, v = sp(Wq(dec), Tq), sp(Wk(enc), Tk), sp(Wv(enc), Tk)
w = (q @ k.transpose(-2, -1) / math.sqrt(dh)).softmax(-1)      # (B,H,Tq,Tk), no causal mask
out = (w @ v).transpose(1, 2).reshape(B, Tq, D)
print(tuple(w.shape), tuple(out.shape))                         # (2, 4, 3, 10) (2, 3, 32)
print(torch.allclose(out, F.scaled_dot_product_attention(q, k, v).transpose(1, 2).reshape(B, Tq, D), atol=1e-6))  # True
```

**Follow-ups:**
- *Why do decoder-only LLMs not have it?* The prompt and output are one sequence, so ordinary causal self-attention already lets output tokens read the prompt. Fewer components, one KV cache.
- *Cache implication?* The encoder K/V are fixed, so they are computed once per request. Only decoder self-attention K/V grow during generation.
- *Is the source ever masked?* Only for padding.

**Common mistakes:** saying Q, K, V all come from the encoder; applying a causal mask to the source; forgetting that the score matrix is not square; saying the cost grows with generated length for the encoder part (it is computed once); confusing "cross-attention" with "cross-encoder" rerankers.

### Q23 ⭐⭐ 🟡 Which levers reduce KV-cache memory (GQA, quantised cache, sliding window, eviction)? Compare their trade-offs.
**Asked at:** big tech, inference/platform teams
**Say this first (1 line):** The cache is `2 · L · n_kv · d_head · T · B · bytes`, so each lever attacks one factor: fewer KV heads (GQA/MQA/MLA), fewer bytes (quantisation), fewer tokens (sliding window, eviction), or better packing (paging, sharing). They differ in what quality they risk and whether they need retraining.

**Then explain:**

| Lever | Factor attacked | Typical saving | Cost / risk | Retrain? |
|---|---|---|---|---|
| GQA / MQA (Q10) | n_kv | 4x for 32 to 8 heads; 32x for MQA | small quality loss if trained that way | yes (or uptrain) |
| MLA (Q33) | compressed latent instead of full K/V | large (architecture-dependent) | more complex kernels | yes |
| Quantised cache (int8/fp8, int4) | bytes | 2x for int8 vs fp16; about 4x for int4 | small for int8; int4 can hurt long or precise tasks | no |
| Sliding window (Q29) | T (capped at window W) | cache is O(W) instead of O(T) | tokens outside the window are not directly visible | yes (trained) or used with sinks |
| Eviction (H2O, StreamingLLM: sinks + recent) | T | fixed budget | may drop a token needed later; hurts retrieval-style tasks | no |
| Prefix sharing (Q24) | duplicated prefixes across requests | big when prompts share a prefix | none on quality | no |
| Paged allocation (Part 10) | wasted space | removes fragmentation, not live size | small overhead | no |
| Offload to CPU/disk | GPU residency | frees GPU memory | latency over PCIe | no |

- **Order of choice:** things that cost no quality come first: paging, prefix sharing, fp8/int8 cache. Then architecture (GQA/MLA) if you control training. Window and eviction trade accuracy for a hard memory bound.
- **They multiply.** Example with the Q15 numbers, Llama-2-7B-like at 32k context, B=1: fp16 MHA is 16 GiB. GQA with n_kv=8 gives 4 GiB. Adding an int8 cache gives about 2 GiB (4x * 2x = 8x, ignoring the small scale overhead).
- **Bandwidth bonus:** a smaller cache also means less data read per decode step, so it helps speed as well as capacity (see Q7).

**Example:** you are serving 64 users at 8k context and run out of GPU memory. First try fp8 KV and prefix sharing for the common system prompt (no retraining). If that is not enough, move to a GQA/MLA model. Use a sliding window or eviction only if the product can tolerate forgetting old tokens (for example, a streaming chat), not for document QA.

**Follow-ups:**
- *Does GQA reduce compute?* Mainly the cache size and bandwidth, so decode benefits most. Prefill compute is similar.
- *Does sliding window lose information?* Directly, yes. Across layers, information can propagate further than W because each layer reads W tokens of a previous layer's output.
- *How do you check the quality of a quantised cache?* Compare task metrics and long-context accuracy against fp16, not just perplexity.

**Common mistakes:** treating paging as a way to shrink the live cache (it removes waste); forgetting that GQA must be trained in; assuming eviction is free; quoting savings without naming the baseline (fp16 MHA); forgetting that weights, not just cache, take memory.

### Q24 ⭐⭐ 🟡 What are prompt/prefix caching in LLM APIs, and how do they relate to the KV cache? How do you structure prompts to benefit?
**Asked at:** product, GCC, API-heavy teams
**Say this first (1 line):** Prompt (prefix) caching stores the KV cache of a prompt prefix so that a later request starting with the exact same tokens skips recomputing that part of prefill. It is the KV cache reused across requests, not just across decode steps. To benefit, put the static content first and the changing content last.

**Then explain:**
- **Link to the KV cache:** in a causal model, the K and V at position i depend only on tokens 0..i. So if two requests share the first N tokens, the K/V for those N tokens are identical and can be reused. (RoPE needs the same positions, which holds for a shared prefix.)
- **What it saves:** prefill compute and time-to-first-token for the cached part. It does not speed up decoding. Providers typically bill cached input tokens at a discount, but the exact discount, minimum prefix length, lifetime (TTL) and whether it is automatic or explicit differ by provider, so check the current docs.
- **Exact prefix match only:** matching is by token prefix (open-source servers such as vLLM hash fixed-size blocks, where each block's key includes all earlier tokens). A single changed token early on invalidates everything after it.
- **How to structure prompts:**
  - Order: system prompt, tool/function definitions, few-shot examples, long reference documents, then conversation history, then the new user question last.
  - Keep the static part byte-identical: no timestamps, request ids, user names or random ordering at the top. Serialise JSON and tool lists in a stable order.
  - Make conversation history append-only (do not edit or re-summarise old turns every request).
  - Put per-user or per-request variables at the end.
  - Check the usage fields in the API response to confirm that cached tokens are being counted.

**Example (toy run):** block size 4. Request 1 has a 12-token shared prefix and 3 new tokens (15 tokens): all 15 are prefilled. Request 2 has the same 12-token prefix and 5 new tokens (17): 12 reused, 5 prefilled. Request 3 adds one token at the front (16 tokens): 0 reused, 16 prefilled.

**Code:** (run; a toy block-hash prefix cache, not a real server)
```python
import hashlib
BLOCK = 4
def block_keys(tokens):
    keys, prev = [], ""
    for i in range(0, len(tokens) - len(tokens) % BLOCK, BLOCK):   # full blocks only
        prev = hashlib.sha1((prev + str(tokens[i:i+BLOCK])).encode()).hexdigest()[:8]  # depends on ALL earlier tokens
        keys.append(prev)
    return keys
cache = set()
def run(name, tokens):
    ks = block_keys(tokens); hit = 0
    for k in ks:
        if k in cache: hit += 1
        else: break
    cache.update(ks)
    print(f"{name}: {len(tokens)} tokens, reused {hit*BLOCK}, prefill {len(tokens)-hit*BLOCK}")
system = list(range(100, 112))
run("req1", system + [1, 2, 3])            # reused 0, prefill 15
run("req2", system + [7, 8, 9, 10, 11])    # reused 12, prefill 5
run("req3", [999] + system + [1, 2, 3])    # reused 0, prefill 16
```

**Follow-ups:**
- *Is the cached prefix always useful?* Only if it is reused within the cache lifetime. Low-traffic prompts may expire before the next hit, so caching saves nothing.
- *Is the output different with caching?* It should be the same (same K/V), apart from tiny numerical differences from different kernels or batching.
- *Memory cost on the server?* Cached prefixes occupy KV memory (see Q23), so servers evict by LRU or TTL. Paging and sharing details are in Part 10.

**Common mistakes:** putting the user question or a timestamp at the top of the prompt; thinking caching works on "similar" prompts (it is exact prefix, not semantic); assuming it speeds up generation (it speeds prefill); inventing provider discount numbers; confusing prompt caching with semantic response caching (which returns a stored answer).

### Q25 ⭐⭐ 🟡 Explain input embeddings, the unembedding (LM head) layer and weight tying. How does vocabulary size affect model size and cost?
**Asked at:** product, GenAI startups
**Say this first (1 line):** The input embedding is a lookup table from token id to a vector; the LM head is the reverse, a matrix that turns the final vector into one score per vocabulary token; weight tying shares one matrix for both, and a bigger vocabulary grows both matrices linearly.
**Then explain:**
- **Input embedding:** matrix `E` of shape `V x d`. Token id `t` just picks row `t`. It is a lookup, so it costs almost no FLOPs.
- **Unembedding / LM head:** a linear layer `d -> V` on the last hidden state. The output is logits, then softmax gives next-token probabilities. This one is a real matmul: about `2*d*V` FLOPs per generated token.
- **Weight tying:** use `E` transposed as the LM head. It saves `V*d` parameters, and it acts as a mild regulariser. It is common in small models. Many large models (Llama 3 8B, for example) keep them untied, because at scale the saving is small and the two matrices want to learn different things.
- **Vocabulary size trade-off:** a bigger `V` means fewer tokens per text (cheaper attention, shorter KV cache, especially for Indian languages and code). But it makes the embedding and head larger, the logits and softmax more expensive, and rare tokens get few training updates.
- Logits for a batch are `batch x seq x V` in training. For `V` around 128k this can be a surprisingly large memory spike, and people chunk the loss for that reason.

**Example:** (computed, Llama-3-8B-like shapes, `d = 4096`)

| V | One matrix (params) | LM-head GFLOPs per token |
|---|---|---|
| 32,000 | 131 M | 0.26 |
| 128,256 | 525 M | 1.05 |
| 256,000 | 1,049 M | 2.10 |

With untied matrices and V = 128,256, the two together are about 1.05 B params, roughly 13% of an 8B model. Tying would save 525 M.

**Code:**
```python
import torch.nn as nn
V, d = 128256, 4096
emb = nn.Embedding(V, d)
head = nn.Linear(d, V, bias=False)
head.weight = emb.weight          # weight tying: same tensor, one set of params
print(emb.weight.numel() / 1e6)   # 525.336576 (million params, counted once)
```
(Parameter counts above were checked in a script; the 3-line tying snippet is standard PyTorch, shown for the idea.)

**Follow-ups:**
- *Why is tying valid?* Both map between token space and hidden space, so "token t" should live at the same place in both directions.
- *Does vocab size change training stability?* Yes: very rare tokens get under-trained embeddings, which can cause odd behaviour on those tokens.

**Common mistakes:** Saying embeddings are a matmul with one-hot (true mathematically, but it is implemented as a lookup). Forgetting that the LM head is paid on every generated token. Claiming all LLMs tie weights.

### Q26 ⭐⭐ 🟡 Where do a transformer's parameters live (attention vs FFN vs embeddings)? How is head dimension chosen?
**Asked at:** big tech, product
**Say this first (1 line):** In a typical modern decoder LLM, about two thirds or more of the parameters sit in the feed-forward (FFN) layers, a sixth or so in attention, and the rest in embeddings; head dimension is usually fixed at 64 or 128 and the number of heads is `d_model / head_dim`.
**Then explain:**
- **Attention per layer** (with GQA): `Wq` is `d x (H*dh)`, `Wk` and `Wv` are `d x (Hkv*dh)` each, `Wo` is `(H*dh) x d`. With plain MHA this is `4*d^2`.
- **FFN per layer:** classic is `2 * d * 4d = 8*d^2`. Modern SwiGLU uses three matrices, `3 * d * d_ff`, with `d_ff` about `8/3 * d` (or a bit larger) so the total stays near `8*d^2`.
- **Embeddings:** `V*d`, once if tied, twice if untied. Norm weights are tiny.
- So FFN is about 2/3 of each layer in the classic design, and it is where knowledge-like memorisation is thought to live (this is a common working view, not a proven fact).
- **Head dimension:** `d_model = H * dh`. Common `dh` is 64 or 128. It is picked for hardware (multiples of 8/16/64 suit tensor cores and FlashAttention kernels), for RoPE (needs an even dh), and as a compromise: tiny heads cannot express much, huge heads mean few heads and less diversity. Head count matters less for parameters (it only splits the same `d`) but matters for KV cache size.

**Example:** (computed) Llama-3-8B-like config: `d=4096, L=32, H=32, Hkv=8, dh=128, d_ff=14336, V=128256`, untied.

| Part | Params | Share |
|---|---|---|
| Attention (32 layers, 41.9 M each) | 1.34 B | 16.7% |
| FFN (32 layers, 176.2 M each) | 5.64 B | 70.2% |
| Embedding + LM head | 1.05 B | 13.1% |
| Total | 8.03 B | |

**Code:**
```python
d,L,H,Hkv,hd,ffn,V = 4096,32,32,8,128,14336,128256
attn = d*H*hd + 2*d*Hkv*hd + H*hd*d
mlp  = 3*d*ffn                       # SwiGLU: gate, up, down
total = 2*V*d + L*(attn + mlp + 2*d) + d
print(attn/1e6, mlp/1e6, total/1e9)  # 41.94304 176.160768 8.030261248
```

**Follow-ups:**
- *Why does GQA cut attention params?* K and V projections shrink from `d x d` to `d x Hkv*dh`.
- *Does more heads mean more parameters?* No, not at fixed `d_model`; it changes how the same width is split.

**Common mistakes:** Saying attention holds most parameters (it does not, FFN does). Forgetting the third SwiGLU matrix. Ignoring GQA when counting.

### Q27 ⭐⭐ 🟡 Transformers vs state-space models (Mamba), linear attention and hybrid architectures: when would you pick each?
**Asked at:** product, research-leaning teams
**Say this first (1 line):** Default to a transformer because it is the best-tested and has precise recall of anything in context; consider SSMs, linear attention or a hybrid when very long sequences or cheap decoding matter more than exact recall.
**Then explain:**
- **Transformer:** every token looks at every cached token. Strong exact retrieval and in-context learning. Cost: attention is `O(n^2)` in training/prefill and the KV cache grows with `n`.
- **SSM (Mamba-style):** keeps a fixed-size hidden state that is updated token by token (a learned, input-dependent recurrence). Decode is `O(1)` per token with constant memory; training uses a parallel scan. Cost: the state is a lossy summary, so exact copy/lookup of far-back details is weaker.
- **Linear attention:** rewrite softmax attention with a kernel so it becomes a running state (also constant memory per token). Same trade-off: compressed memory, usually some quality loss against full softmax attention.
- **Hybrids:** mostly SSM/linear layers plus a few full-attention layers (open models such as Jamba mix Mamba and attention layers, and add MoE). Idea: cheap long-range mixing for most layers, a few attention layers for precise recall.
- **When to pick:**

| Need | Choice |
|---|---|
| General assistant, best quality, mature tooling | Transformer (with GQA/MLA, FlashAttention) |
| Very long streams, small memory budget, edge devices | SSM or hybrid |
| Heavy retrieval/copying from context | Transformer or hybrid with attention layers |

**Example:** Serving a 1M-token context: a pure transformer needs a KV cache that grows with every token (about 131 GB for a Llama-3-8B-like config, computed in Q30). An SSM layer keeps a fixed state regardless of length, so memory per sequence is flat.

**Follow-ups:**
- *Why not SSMs everywhere?* Tooling, scaling evidence and recall quality still favour transformers; the field is moving, so state this as the current trade-off.
- *Is there a middle path inside transformers?* Yes: sliding-window attention, GQA, MLA (Q29, Q10, Q33).

**Common mistakes:** Saying SSMs "beat" transformers outright. Quoting `O(n)` without saying the cost is the lossy fixed-size state. Forgetting that training is parallel for SSMs too.

### Q28 ⭐⭐ 🟡 Do attention weights explain a model's output? What are induction heads and how do they relate to in-context learning?
**Asked at:** research-leaning teams, big tech
**Say this first (1 line):** Not reliably: attention weights show where information was read from, not why the model answered what it did; induction heads are a specific two-head circuit that does "find the earlier match and copy what came next", and they are a leading explanation for part of in-context learning.
**Then explain:**
- **Why attention is not an explanation:** the output of a head is the attention-weighted sum of *value vectors*, then it goes through `Wo`, residual adds, many layers and the FFN. A token can get high weight but have a tiny value vector, or low weight but a large contribution. Studies of attention-as-explanation in NLP found weights often correlate poorly with gradient-based importance and that alternative weights can give the same output. So treat attention maps as a hint, not proof.
- **Better tools:** gradient or attribution methods, ablating/patching heads and activations (causal tests), and probing.
- **Induction head:** from Anthropic's interpretability work (Olsson et al., 2022). Pattern: sequence `... A B ... A` then predict `B`. It needs two heads in different layers: an earlier "previous-token" head writes "my previous token was A" onto B's position; a later induction head at the second `A` attends to the token right after the earlier `A` (i.e. to `B`) and copies it to the output.
- **Link to in-context learning:** that paper reports induction heads form during a sharp "phase change" in training, at about the same time in-context learning ability jumps. Evidence is strongest for small models; for large models the link is argued but less directly proven, so say "evidence suggests", not "proves".

**Example:** Prompt "Mr Dursley ... Mr D" -> the model completes "ursley". Prefix matching and copying handles it.

**Follow-ups:**
- *How would you test a head's causal role?* Zero or patch its output and measure the change in the loss on repeated-sequence prompts.
- *Does this mean in-context learning is only copying?* No. Induction heads explain pattern completion; richer ICL likely uses more circuits.

**Common mistakes:** Presenting attention heatmaps as explanations in a product. Saying induction heads were "proven" to be the cause of all ICL.

### Q29 ⭐⭐ 🟡 What are sliding-window, local and sparse attention? What are attention sinks and why do they matter for streaming?
**Asked at:** product, GenAI startups, inference teams
**Say this first (1 line):** These all restrict which past tokens each token can attend to, so cost and KV cache stop growing with full length; attention sinks are the first few tokens that the model dumps spare attention on, and you must keep them or streaming quality collapses.
**Then explain:**
- **Local / sliding-window attention:** each token sees only the last `w` tokens. Compute per token becomes `O(w)` instead of `O(n)`, and the KV cache can be a rolling buffer of size `w`. Information still travels further than `w` indirectly: after `L` layers the effective reach is about `L*w`.
- **Sparse attention:** a fixed or learned pattern (local + strided + a few global tokens, as in Longformer/BigBird-style models). Mixed designs use some layers full, some local.
- **Cost:** tokens outside the window are invisible directly, so exact recall of old facts suffers.
- **Attention sinks (StreamingLLM, Xiao et al.):** softmax must sum to 1, so when a token has nothing useful to attend to, the model parks weight on the very first tokens. If you evict them with a plain sliding window, outputs degrade badly. Fix: keep the first few tokens' KV (the "sinks", e.g. 4) plus the recent window. That gives stable generation on very long streams.
- **Caveat:** this keeps the model fluent over an endless stream; it does *not* give it memory of the evicted middle.

**Example:** a 100,000-token stream with a window of 4096 and 4 sink tokens keeps 4,100 KV slots instead of 100,000.

**Code:**
```python
import torch
def window_mask(T, w, sinks=0):
    i = torch.arange(T)[:, None]; j = torch.arange(T)[None, :]
    return (j <= i) & (((i - j) < w) | (j < sinks))
print(window_mask(8, 3, sinks=1).int())   # row 7 -> [1,0,0,0,0,1,1,1]
```
Run output: row 7 is `[1,0,0,0,0,1,1,1]`: the sink token 0 plus the last 3 tokens.

**Follow-ups:**
- *Does windowed attention fit with RoPE?* Yes, RoPE is relative, though StreamingLLM re-indexes positions inside the cache.
- *Which models use sliding windows?* For example Mistral 7B uses sliding-window attention.

**Common mistakes:** Believing a window gives long-term memory. Evicting the first token. Mixing up "reach grows with layers" with "can retrieve any old fact".

### Q30 ⭐⭐ 🟡 What breaks when you go from 8k to 128k–1M context (compute, memory, quality)? What is ring attention / sequence parallelism at a high level?
**Asked at:** big tech, GenAI startups
**Say this first (1 line):** Three things break: attention compute grows quadratically, the KV cache grows linearly until it no longer fits on a GPU, and quality often drops because the model was not trained on, or cannot use, such long contexts; ring attention splits the sequence across GPUs so no GPU holds it all.
**Then explain:**
- **Compute:** attention FLOPs scale with `n^2`. Going 8k -> 128k is 16x longer, so 256x more attention FLOPs (the FFN grows only 16x). Prefill latency (time to first token) climbs.
- **Memory:**
  - Naive scores matrix per head: 128k x 128k in fp16 is about 32.8 GB (one head!), so FlashAttention (never materialise it) is mandatory.
  - KV cache, Llama-3-8B-like config (32 layers, 8 KV heads, dh=128, fp16), 131,072 bytes per token: 8k = 1.05 GB, 128k = 16.8 GB, 1M = 131 GB per sequence (computed).
- **Quality:** positions beyond the training length need RoPE scaling/extension and long-context fine-tuning; even then models show "lost in the middle" and weaker retrieval from the centre of the context. A big advertised window is not the same as reliably using it (test with needle-in-a-haystack and real tasks).
- **Fixes in one line each:** GQA/MLA to shrink the cache (Q10, Q33), sliding window layers (Q29), cache quantisation and paging (Part 10), retrieval/RAG instead of stuffing everything in.
- **Ring attention / sequence (context) parallelism:** split the sequence into blocks, one per GPU. Each GPU holds its query block and passes K/V blocks around a ring to its neighbours, computing blockwise attention (online-softmax, like FlashAttention) on each block while the next one is in flight. Result is exact attention, with per-GPU memory about `n / num_gpus`, and the communication is hidden behind compute if blocks are large enough.

**Example:** a 1M-token prompt does not fit one 80 GB GPU for the cache alone (131 GB at fp16), so you either shard the sequence (ring attention) or shrink the cache.

**Follow-ups:**
- *Is it exact?* Yes, ring attention gives the same result as full attention; only the data layout differs.
- *Cheaper alternative to a 1M window?* RAG plus a moderate window is usually cheaper and often more accurate.

**Common mistakes:** Saying cost is "just linear" (the cache is, the compute is not). Ignoring the memory of the attention matrix without FlashAttention. Treating the advertised context size as usable context.

### Q31 ⭐⭐ 🟡 How do multimodal LLMs ingest images (ViT patches, projector, cross-attention vs token concatenation)?
**Asked at:** big tech, product, GenAI startups
**Say this first (1 line):** An image is cut into patches, a vision encoder (a ViT) turns them into vectors, a small projector maps those into the LLM's embedding space, and the LLM then treats them like extra tokens; the alternative is to let text layers cross-attend to the image features.
**Then explain:**
- **Patchify:** split the image into fixed squares (e.g. 14x14 pixels), flatten each, linearly embed it, add position info. A ViT is then an ordinary transformer over these patch tokens.
- **Vision encoder:** often a pretrained CLIP/SigLIP-style ViT, frozen or lightly tuned, giving one vector per patch.
- **Projector (connector):** maps vision dimension to LLM dimension `d`. Options: a linear layer or small MLP (LLaVA style), or a resampler/Q-Former that compresses many patches into a fixed small number of tokens.
- **Two ways to feed the LLM:**

| Approach | How | Trade-off |
|---|---|---|
| Token concatenation (LLaVA, many open VLMs) | image tokens placed in the sequence next to text tokens; ordinary self-attention | simple, flexible for many images; image tokens consume context and KV cache |
| Cross-attention (Flamingo-style, some Llama vision variants) | extra cross-attention layers where text queries attend to image features | text context stays short; adds new layers and parameters |

- **Training recipe (typical):** align stage (train projector on image-caption pairs), then instruction-tune on image-text conversations. Details vary by model.
- **Cost:** high-resolution images or many frames mean many tokens, so cost and latency rise fast.

**Example:** a 336x336 image with 14-pixel patches gives (336/14)^2 = 24 x 24 = 576 patch tokens (computed; this is the layout LLaVA-1.5 uses with a CLIP ViT-L/14 at 336 px). Those 576 tokens sit in the context like 576 words and also fill the KV cache.

**Follow-ups:**
- *How do you cut image token cost?* Lower resolution, pooling or resampling the patches, dynamic tiling only when needed.
- *Where do audio/video fit?* Same idea: encoder -> projector -> tokens.

**Common mistakes:** Forgetting that images consume context length. Saying the LLM "sees pixels". Not knowing the projector is the cheap bridge, and that the encoder and LLM are usually pretrained separately.

### Q32 ⭐⭐ 🟡 Use arithmetic intensity (roofline thinking) to explain why batching helps decode throughput and when it stops helping.
**Asked at:** big tech, inference/platform teams
**Say this first (1 line):** In decode every step must read all the weights from memory to do very little maths for one sequence, so adding more sequences to the batch reuses the same weight read and throughput rises almost for free, until the GPU becomes compute-bound or the KV cache (and memory) runs out.
**Then explain:**
- **Arithmetic intensity** = FLOPs done per byte moved from memory. **Roofline:** speed is limited by `min(peak FLOPs, intensity x memory bandwidth)`. The **ridge point** = peak FLOPs / bandwidth; below it you are memory-bound, above it compute-bound.
- **Decode, batch B, model with P params in 16-bit:** FLOPs about `2*P*B`, bytes about `2*P` (read weights once per step). So intensity is about `B` FLOPs/byte. Batch 1 is far below the ridge, hence memory-bound; batching raises intensity linearly.
- **Where it stops helping:**
  1. Intensity reaches the ridge point, so compute is the limit.
  2. The KV cache is read *per sequence*, so its bytes grow with B and do not get reused. Attention stays memory-bound, and it caps the gain well before the ridge.
  3. GPU memory: weights + `B x context x KV bytes/token` must fit.
  4. Latency per step rises, so per-user speed drops.
- Prefill is different: many tokens per sequence already means high intensity (Q7).

**Example:** Illustrative hardware (assumed numbers, not a specific benchmark): 1,000 TFLOP/s peak 16-bit compute and 3.35 TB/s memory bandwidth, so the ridge is about 300 FLOPs/byte. Model: 8B params in bf16 (16 GB). Computed:

| Batch | Weights-only tok/s (step ms) | With KV (4k ctx per seq, GQA 128 KB/token) tok/s |
|---|---|---|
| 1 | 209 (4.78) | 203 |
| 8 | 1,675 (4.78) | 1,321 |
| 32 | 6,700 (4.78) | 3,231 |
| 128 | 26,800 (4.78) | 5,061 |
| 512 | 62,500 (compute-bound, 8.2) | 5,897 |

Weights-only, the step time is flat at 4.78 ms until B is about 300, so throughput is nearly linear in B. With the KV cache included, throughput flattens around 5-6k tok/s. Also note: at 4k context, 512 sequences need about 275 GB of KV, which would not fit on one 80 GB card, so memory caps B first in practice.

**Code:**
```python
F, BW, P = 1000e12, 3.35e12, 8e9           # illustrative hardware + 8B model
kv = 2*32*8*128*2                           # 131072 bytes per token
for B in [1, 32, 128, 512]:
    t = max(2*P*B/F, (2*P + B*kv*4096)/BW)  # step time = slower of compute and memory
    print(B, round(B/t))                    # 203, 3231, 5061, 5897
```

**Follow-ups:**
- *Why does GQA/MLA help throughput?* A smaller KV cache means fewer bytes per sequence, so larger B fits and the KV term shrinks.
- *Continuous batching?* Scheduling detail for keeping B high; see Part 10.

**Common mistakes:** Saying decode is compute-bound. Forgetting that KV reads scale with batch. Presenting the illustrative hardware figures as real measurements.

### Q33 ⭐⭐ 🔴 What is Multi-head Latent Attention (MLA, as in DeepSeek)? How does it compress the KV cache versus GQA?
**Asked at:** GenAI startups, big tech, research-leaning teams
**Say this first (1 line):** MLA, introduced in DeepSeek-V2, caches one small shared low-rank latent vector per token (plus a tiny separate RoPE key) instead of full per-head keys and values, and rebuilds the per-head K and V from the latent when needed, so the cache is far smaller than MHA and still keeps per-head diversity.
**Then explain:**
- **Down-projection:** hidden state `h_t` -> compressed latent `c_t^KV = W^DKV h_t`, dimension `d_c` (much smaller than `n_heads * d_head`).
- **Up-projection:** per-head keys and values come from the latent: `K = W^UK c`, `V = W^UV c`. Each head still gets its own K and V, unlike MQA/GQA where heads share the same K/V.
- **Cache:** only `c_t^KV` is stored, not K and V.
- **Why a decoupled RoPE key:** RoPE rotates K by position, and that rotation sits between the query and `W^UK`, which would stop you from merging (absorbing) `W^UK` into the query projection at inference. So MLA splits the key into a content part (from the latent, no RoPE) and a small separate RoPE part `k^R` of dimension `d_R` that is shared across heads and cached too. Queries also get a content part and a RoPE part. Per token per layer, cache = `d_c + d_R`.
- **Inference trick:** `W^UK` can be absorbed into the query side and `W^UV` into the output projection, so attention can run directly against the latent without expanding full K/V.
- **Cost:** more complex kernels and implementation; extra projections. The DeepSeek-V2 paper reports MLA gives better quality than MHA in its ablations while using far less cache; treat the quality claim as the authors' result.

**Example:** (computed) DeepSeek-V2-like config as reported in the paper: 128 heads, head dim 128, 60 layers, `d_c = 512`, `d_R = 64`, bf16 (2 bytes). GQA comparison with 8 KV heads, head dim 128 is my own illustrative baseline.

| Scheme | Elements per token per layer | KB per token (60 layers) | 128k-token context |
|---|---|---|---|
| MHA (128 KV heads) | 2 x 128 x 128 = 32,768 | 3,932 | 503 GB |
| GQA (8 KV heads) | 2 x 8 x 128 = 2,048 | 246 | 31.5 GB |
| MLA | 512 + 64 = 576 | 69 | 8.8 GB |

So MLA is about 57x smaller than MHA and about 3.6x smaller than that GQA-8 baseline. The paper's own framing: the cache equals that of GQA with about 2.25 groups, since `576 / (2 x 128) = 2.25`.

**Code:**
```python
nh, dh, dc, dr, L = 128, 128, 512, 64, 60
mha, gqa8, mla = 2*nh*dh, 2*8*dh, dc + dr
print(mha, gqa8, mla)                 # 32768 2048 576
print(mha/mla, gqa8/mla, mla/(2*dh))  # 56.89 3.56 2.25
print(mla*L*2*128000/1e9)             # 8.85 GB (bf16, 128k tokens)
```

**Follow-ups:**
- *Why is a small cache good?* Decode is memory-bandwidth-bound (Q7, Q32), so fewer cache bytes means faster decode and larger batches.
- *Is MLA lossless?* No, it is a low-rank bottleneck trained end to end, not an exact compression of a trained MHA.

**Common mistakes:** Saying MLA shares K/V across heads like MQA (it does not, per-head K/V are reconstructed). Forgetting the decoupled RoPE key (the `+64`). Quoting cache sizes without stating the config.

### Q34 ⭐⭐ 🔴 Explain Mixture-of-Experts layers: routing, load balancing, active vs total parameters, and the serving trade-offs.
**Asked at:** big tech, GenAI startups, product
**Say this first (1 line):** A Mixture-of-Experts layer replaces one FFN with many parallel FFN "experts" and a small router that sends each token to only the top-k of them, so total parameters are large but active parameters (and FLOPs) per token stay small.
**Then explain:**
- **Where:** only the FFN of a block is replaced; attention stays dense and shared.
- **Routing:** router = a linear layer `d -> E`; softmax; pick top-k experts per token; mix their outputs with the (renormalised) gate weights. Mixtral 8x7B uses 8 experts with top-2 (46.7B total, about 12.9B active per token, per its release).
- **Load balancing:** left alone, the router collapses onto a few favoured experts (rich get richer), others never train, and under expert parallelism a hot expert becomes the bottleneck. Fixes: an auxiliary loss pushing equal usage (Switch-style `E * sum(fraction_e * mean_prob_e)`, equals 1 when balanced), capacity limits with token dropping, or auxiliary-loss-free bias adjustment (used in DeepSeek-V3, per its report). Some designs add always-on shared experts plus many small routed ones (DeepSeekMoE).
- **Active vs total:** compute and decode speed track the active count; memory tracks the total. You pay for all weights in GPU memory but only use a few per token.
- **Serving trade-offs:**
  - Memory: must hold all experts, so a "12.9B-active" model needs memory like 46.7B.
  - Batch size 1: only k experts are touched, so decode bandwidth is low. Larger batches touch most experts, so the bandwidth advantage fades.
  - Expert parallelism needs all-to-all communication between GPUs; skewed routing creates stragglers.
  - Training is harder (instability, balance tuning).

**Example:** E=8, k=2: each token uses 2/8 of the expert weights. In a toy layer I ran (8 experts, top-2, 1000 random tokens) the measured token share per expert ranged from 10% to 16% (perfect = 12.5%) and the balance loss was 1.005. Active params per token were 2,272 of 8,704 total.

**Code:**
```python
import torch, torch.nn as nn, torch.nn.functional as F
class MoE(nn.Module):
    def __init__(s, d=16, E=8, k=2, hid=32):
        super().__init__(); s.k, s.E = k, E
        s.router = nn.Linear(d, E, bias=False)
        s.experts = nn.ModuleList(nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, d)) for _ in range(E))
    def forward(s, x):
        probs = F.softmax(s.router(x), -1)
        topv, topi = probs.topk(s.k, -1)
        topv = topv / topv.sum(-1, keepdim=True)            # renormalise the k gates
        out = torch.zeros_like(x)
        for e in range(s.E):
            tok, slot = (topi == e).nonzero(as_tuple=True)
            if len(tok): out[tok] += topv[tok, slot, None] * s.experts[e](x[tok])
        frac = F.one_hot(topi, s.E).float().sum(1).mean(0) / s.k
        aux = s.E * (frac * probs.mean(0)).sum()             # balance loss
        return out, aux
torch.manual_seed(0); y, aux = MoE()(torch.randn(1000, 16)); print(aux.item())  # about 1.005
```

**Follow-ups:**
- *Is MoE cheaper to train?* Cheaper per quality in FLOPs, but needs more memory and engineering.
- *Why does an untrained router collapse?* Experts that win early get more gradient, improve, and win more.

**Common mistakes:** Equating active parameters with memory needed. Saying every layer part is an expert (only FFN). Forgetting load balancing.

### Q35 ⭐⭐ 🔴 Code: write a decoding loop with a KV cache and verify it matches the no-cache output.
**Asked at:** product, big tech, inference teams
**Say this first (1 line):** Prefill the whole prompt once and store each layer's K and V; then for every new token compute only its own Q, K, V, append K and V to the cache, and attend over the full cache; the result must equal recomputing everything each step, which I verify with greedy decoding and a logit diff.
**Then explain:**
- **Prefill:** run all prompt tokens together with a normal causal mask; save K, V per layer, shape `(B, heads, S, head_dim)`.
- **Decode step:** input is one token (T=1) at absolute position `S`. Concatenate its K, V to the cache. The query attends to all `S+1` keys, so no mask is needed for T=1 (every cached key is in the past).
- **Details that cause bugs:** position embeddings must use the *absolute* position (`start=S`), not 0; the mask for T>1 with a non-empty cache must be offset (`tril(diagonal=S-T)`); store K/V after the projection (and, with RoPE, store keys *after* rotation, since their position is fixed).
- **Correctness test:** greedy decode both ways and compare tokens, then compare logits for the final step. They will not be bit-identical in floating point (different matmul shapes, summation order), so expect a tiny difference, not exactly zero.

**Example:** Tiny random 2-layer model (vocab 50, d=32, 4 heads, seed 0), 7-token prompt, 20 new tokens. Run result: generated tokens equal `True`; max abs logit diff `1.79e-07`; cache K shape per layer `(2, 4, 26, 8)` (batch 2, 4 heads, 7 + 19 cached positions = 26, head dim 8; the last generated token has not been fed back yet).

**Code:**
```python
import torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0)

class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.h, s.dh = h, d // h
        s.qkv = nn.Linear(d, 3 * d, bias=False)
        s.o = nn.Linear(d, d, bias=False)
        s.n1, s.n2 = nn.LayerNorm(d), nn.LayerNorm(d)
        s.ff = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
    def forward(s, x, cache=None):
        B, T, D = x.shape
        q, k, v = s.qkv(s.n1(x)).view(B, T, 3, s.h, s.dh).permute(2, 0, 3, 1, 4)
        if cache is not None:                      # append new K,V to cached K,V
            if "k" in cache:
                k = torch.cat([cache["k"], k], dim=2)
                v = torch.cat([cache["v"], v], dim=2)
            cache["k"], cache["v"] = k, v
        S = k.shape[2]                             # total length so far
        # query i sits at absolute position S-T+i; it may see keys j <= S-T+i
        mask = torch.ones(T, S, dtype=torch.bool).tril(diagonal=S - T)
        a = F.scaled_dot_product_attention(q, k, v, attn_mask=mask)
        x = x + s.o(a.transpose(1, 2).reshape(B, T, D))
        return x + s.ff(s.n2(x))

class TinyLM(nn.Module):
    def __init__(s, V=50, d=32, h=4, L=2, maxlen=64):
        super().__init__()
        s.emb, s.pos = nn.Embedding(V, d), nn.Embedding(maxlen, d)
        s.blocks = nn.ModuleList(Block(d, h) for _ in range(L))
        s.nf, s.head = nn.LayerNorm(d), nn.Linear(d, V, bias=False)
    def forward(s, ids, caches=None, start=0):
        T = ids.shape[1]
        x = s.emb(ids) + s.pos(torch.arange(start, start + T))
        for i, b in enumerate(s.blocks):
            x = b(x, None if caches is None else caches[i])
        return s.head(s.nf(x))

@torch.no_grad()
def generate_nocache(m, ids, n):
    for _ in range(n):
        nxt = m(ids)[:, -1].argmax(-1, keepdim=True)   # recompute everything each step
        ids = torch.cat([ids, nxt], 1)
    return ids

@torch.no_grad()
def generate_cache(m, ids, n):
    caches = [dict() for _ in m.blocks]
    logits = m(ids, caches, start=0)                   # prefill: whole prompt at once
    out = ids
    for _ in range(n):
        nxt = logits[:, -1].argmax(-1, keepdim=True)
        out = torch.cat([out, nxt], 1)
        logits = m(nxt, caches, start=out.shape[1] - 1)  # decode: 1 token, reuse cache
    return out

m = TinyLM().eval()
prompt = torch.randint(0, 50, (2, 7))
a, b = generate_nocache(m, prompt, 20), generate_cache(m, prompt, 20)
print("tokens equal:", torch.equal(a, b))

# compare logits (not just argmax tokens) at the last step
with torch.no_grad():
    full = m(a[:, :-1])[:, -1]
    caches = [dict() for _ in m.blocks]
    m(a[:, :7], caches, 0)
    for t in range(7, a.shape[1] - 1):
        step = m(a[:, t:t+1], caches, start=t)[:, -1]
print("max abs logit diff:", (full - step).abs().max().item())
print("cache K shape per layer:", tuple(caches[0]["k"].shape))
# output: tokens equal: True / max abs logit diff: 1.7881393432617188e-07 / (2, 4, 26, 8)
```

**Follow-ups:**
- *How much does the cache save?* Per step, projections and attention are done for 1 token instead of S; total generation work goes from about `O(n^3)`-ish (recompute each time) to `O(n^2)`, at the cost of memory (Q6).
- *Ragged batches?* Pad and track per-sequence lengths with masks; production engines use paged caches (Part 10).
- *With RoPE?* Cache keys after applying rotation at their absolute position.

**Common mistakes:** Restarting position ids at 0 in decode. Using a plain causal mask when T < S. Comparing with `==` instead of a tolerance. Forgetting `torch.no_grad()` so the cache keeps autograd graphs.

### Q36 ⭐ 🟢 Explain transformers to a non-technical stakeholder in two minutes.
**Asked at:** all types; senior/client-facing roles
**Say this first (1 line):** A transformer is the kind of AI model behind ChatGPT-style tools: it reads text as small pieces, works out which pieces matter for each other, and then predicts the next piece, over and over, to write an answer.
**Then explain:** (what I would actually say, no jargon)
- **Step 1, pieces:** "It chops text into small chunks called tokens, roughly parts of words, and turns each into a list of numbers."
- **Step 2, attention:** "For every word, the model asks: which other words in this text help me understand this one? In 'The bank raised rates', the word 'rates' tells it that 'bank' is a financial bank, not a river bank. That looking-around step is called attention. It does this for all words at the same time, which is why these models can be trained on huge amounts of text quickly."
- **Step 3, stacking:** "That step is repeated in many layers. Early layers pick up simple patterns, later ones pick up more abstract meaning."
- **Step 4, predict:** "Finally it predicts a likely next token, adds it to the text, and repeats. An answer is built one token at a time."
- **Where it learned:** "By reading very large amounts of text and practising next-word prediction, then being tuned to follow instructions."
- **Business-relevant honesty:** it is good at language and patterns, but it predicts plausible text rather than looking up truth, so it can state wrong things confidently. That is why we pair it with our own documents (retrieval), checks and human review. Longer inputs and longer answers cost more and respond slower, which is why we watch usage and cost.

**Example (analogy):** "Imagine a very well-read colleague who has skimmed a huge library. Given the start of a sentence, they are excellent at continuing it sensibly. They are not checking a database, so for facts that matter we hand them the right documents first."

**Follow-ups:**
- *"Does it understand?"* Say it behaves as if it understands in many tasks, but it has no guarantee of truth, so we verify.
- *"Why now?"* Parallel training on lots of data and compute made these models practical; I would not over-claim beyond that.
- *"What should we worry about?"* Wrong answers stated confidently, data privacy, and cost at scale.

**Common mistakes:** Using terms like softmax or Q/K/V with non-technical people. Saying "it thinks like a human" or "it looks up the answer". Skipping the limitations that the stakeholder needs for decisions. Running over two minutes: stop at one analogy and one limitation.

### Q37 ⭐ 🟡 Derive the sinusoidal positional encoding and its relative-position property. Why is it rarely used in modern LLMs?
**Asked at:** big tech, research-leaning teams
**Say this first (1 line):** Sinusoidal encoding gives each position a vector of sines and cosines at geometrically spaced frequencies. The vector for position p+k is a fixed rotation of the vector for p, so relative offsets are easy to represent. Modern LLMs moved to RoPE because it puts relative position directly into the attention score, in every layer.

**Then explain:**
- **Definition (Vaswani et al. 2017):** `PE(p, 2i) = sin(p / 10000^(2i/d))`, `PE(p, 2i+1) = cos(p / 10000^(2i/d))`. Each pair of dimensions is one sine/cosine at frequency `w_i = 10000^(-2i/d)`. Low `i` = fast wave (fine position), high `i` = slow wave (coarse position), like the hands of a clock.
- **Derivation of the relative property:** from `sin(a+b)` and `cos(a+b)`:
  `[sin(w(p+k)), cos(w(p+k))] = [[cos wk, sin wk], [-sin wk, cos wk]] @ [sin(wp), cos(wp)]`.
  The matrix depends only on the offset k, not on p. So `PE(p+k) = R_k PE(p)` with `R_k` block-diagonal.
- **Consequence:** `PE(p) . PE(p+k) = sum_i cos(w_i k)`. The similarity between two positions depends only on the distance, and it generally falls as distance grows (not monotonically).
- **Why it is rarely used now:**
  - It is *added* to the token embedding once at the input. Attention has to learn, through `W_q`, `W_k`, to pull relative information back out. That path is indirect and gets mixed with token content.
  - Length extrapolation is poor in practice for the models people tried. The vectors for unseen positions are well defined, but the network never saw them. (Vaswani et al. said they chose sinusoids hoping for extrapolation, and found learned embeddings gave nearly the same results.)
  - RoPE and ALiBi act inside attention, at every layer, and are relative by construction. They became the default after about 2021 (e.g. GPT-J, GPT-NeoX, PaLM, Llama use RoPE).

**Example:** For d=16 and offset k=5, `PE(p) . PE(p+5)` is 6.137 for p = 0, 10, 50 and 120 alike. At p=0, the dot with PE(k) is 8.00 at k=0, 7.49 at k=1, 6.14 at k=5, 5.78 at k=20, 3.49 at k=100. Both came from the run below.

**Code:** (executed, numpy)
```python
import numpy as np
def sinpe(n, d):
    pos = np.arange(n)[:, None]
    w = 1.0 / 10000 ** (np.arange(0, d, 2) / d)
    pe = np.zeros((n, d)); pe[:, 0::2] = np.sin(pos * w); pe[:, 1::2] = np.cos(pos * w)
    return pe, w
d, k = 16, 5
pe, w = sinpe(200, d)
R = np.zeros((d, d))
for i, wi in enumerate(w):
    c, s = np.cos(k * wi), np.sin(k * wi)
    R[2*i:2*i+2, 2*i:2*i+2] = [[c, s], [-s, c]]
print(max(np.abs(R @ pe[p] - pe[p + k]).max() for p in range(0, 150, 7)))   # 3.9e-15
print([round(pe[p] @ pe[p + k], 6) for p in (0, 10, 50, 120)])              # [6.13704]*4
print(round(np.cos(k * w).sum(), 6))                                        # 6.13704
```

**Follow-ups:**
- *Why 10000 and geometric spacing?* It spans wavelengths from 2*pi up to about 2*pi*10000 so that both near and far offsets are distinguishable. 10000 is a design choice, not a derived constant.
- *Sinusoidal vs learned absolute?* Learned has a hard maximum length (the table size). Sinusoidal is defined for any position but is not guaranteed to work well there.
- *Is the relative property enough for attention?* Not by itself. The score is `(x_p + PE_p) W_q W_k^T (x_m + PE_m)^T`, which has cross terms mixing content and position, so relative position does not cleanly drop out. RoPE fixes this.

**Common mistakes:** Saying sinusoidal "extrapolates perfectly" (it is defined, not proven to work). Forgetting that the relative property is a linear map `R_k` that does not depend on p. Claiming the dot product is a monotonic function of distance.

### Q38 ⭐ 🟡 ALiBi vs RoPE: how does each handle length extrapolation?
**Asked at:** research-leaning teams, GenAI startups
**Say this first (1 line):** ALiBi adds a distance penalty to the attention scores and extrapolates to longer inputs reasonably well out of the box. RoPE rotates queries and keys, gives good relative-position modelling, but degrades beyond the trained length unless you rescale the positions (interpolation, NTK-aware scaling, YaRN). Most recent open LLMs still chose RoPE plus scaling.

**Then explain:**

| | ALiBi | RoPE |
|---|---|---|
| Where | Bias added to scores: `score(i,j) = q_i.k_j/sqrt(d) - m_h * (i-j)` | Rotate q and k pairs by angle `pos * theta_i`; score depends on `i-j` |
| Parameters | None. Per-head slope `m_h` is fixed, geometric, e.g. 1/2, 1/4 ... 1/256 for 8 heads | None. Frequencies `theta_i = base^(-2i/d)` |
| Extrapolation | Penalty is just a bigger number at longer distance, nothing "unseen". Press et al. (2022) showed a model trained on 1024 tokens kept good perplexity at longer test lengths | Angles beyond training range were never seen; attention quality drops past the trained window |
| Fix | Not needed (but see caveat) | Position interpolation (Chen et al. 2023, squeeze positions into the trained range, short fine-tune), NTK-aware scaling / change `base`, YaRN, followed by brief long-context fine-tuning |
| Used by | e.g. BLOOM, MPT | e.g. Llama family, Qwen, many others |

- **Why ALiBi is not universal:** the penalty is a strong recency bias. Different heads have different slopes so some can look far, but several reports and later work found it less competitive than RoPE at long-context retrieval and downstream quality. Treat this as an empirical trend, not a theorem.
- **Why RoPE won in practice:** quality at the trained length, easy to retrofit with scaling tricks, and wide framework support (FlashAttention kernels, etc.).
- **Extrapolation is not the same as using the long context.** A model can keep low perplexity at 4x length and still fail to retrieve a fact from the middle. Test with needle-in-a-haystack style or real long tasks, not just perplexity.

**Example:** With slope 0.5 (steepest head) the multiplier `exp(-m * dist)` on an attention weight is 0.607 at distance 1 and 0.0003 at distance 16, so that head is essentially local. With slope 0.0039 (flattest head) it is 0.607 at distance 128 and 0.018 at distance 1024, so that head can still see far.

**Code:** (executed, numpy) the ALiBi slopes and bias
```python
import numpy as np
def alibi_slopes(H): return np.array([2 ** (-8 * (h + 1) / H) for h in range(H)])  # valid as given for H a power of 2
print(alibi_slopes(8))   # [0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125, 0.00390625]
i = np.arange(5)[:, None]; j = np.arange(5)[None, :]
bias = -alibi_slopes(8)[0] * (i - j).clip(min=0)   # added to scores before softmax (causal part)
```
RoPE itself is implemented and checked in Q42.

**Follow-ups:**
- *How does position interpolation work?* If trained on length L and you want 4L, use positions `p/4` so angles stay inside the trained range. Resolution between neighbouring tokens shrinks, so a short fine-tune is needed. NTK-aware scaling instead stretches the low-frequency end more than the high-frequency end. YaRN refines this. Details vary by model; check the specific paper.
- *Does ALiBi work with KV cache?* Yes. The bias depends only on `i-j`, and the new query computes it against cached keys. RoPE caches keys after rotation, since a key's rotation depends only on its own position.
- *Can you mix?* Some recent models interleave layers with and without positional encodings, but that is model-specific; do not claim it as a standard.

**Common mistakes:** Saying RoPE "cannot extrapolate at all" (it degrades, and scaling fixes much of it) or that ALiBi "solves" long context (it solves a perplexity-extrapolation problem, not retrieval). Mixing up interpolation (squeeze positions) with extrapolation (use unseen positions).

### Q39 ⭐ 🟡 What architectural choices do modern open LLMs (Llama, Qwen, DeepSeek) make: RMSNorm, SwiGLU, RoPE, GQA, no biases, tied embeddings? Why?
**Asked at:** product, GenAI startups
**Say this first (1 line):** Most open decoder LLMs share a recipe: pre-norm with RMSNorm, SwiGLU feed-forward, RoPE, and fewer KV heads (GQA) to shrink the KV cache. Each choice is mostly about training stability, a small quality gain, or cheaper inference. The details differ by model, so I would not say "all of them do all of these".

**Then explain:**

| Choice | What it is | Why |
|---|---|---|
| Pre-norm + **RMSNorm** | Normalise by `x / rms(x) * g`, no mean subtraction, no bias | Cheaper than LayerNorm, works as well in practice (Zhang & Sennrich 2019); normalising before each sub-block keeps gradients healthy at depth (see Q44) |
| **SwiGLU** FFN | `W2( silu(W1 x) * W3 x )`: a gated FFN with 3 matrices | Shazeer (2020) found GLU variants beat plain ReLU/GELU FFN at equal compute, empirically. Hidden size is cut to about 8/3 * d so the parameter count matches a 4d two-matrix FFN |
| **RoPE** | Rotates q, k by position (Q42) | Relative position inside attention, no extra parameters, can be stretched to longer context (Q38) |
| **GQA** | Many query heads share a few KV heads (Q10) | KV cache and decode memory traffic shrink by `heads/kv_heads` with a small quality cost. Llama 2 70B and Llama 3 use it |
| **No biases** | Linear layers without `+ b` | Slightly fewer parameters and simpler/faster kernels; reported to make no real quality difference. Exception: Qwen2/2.5 keep a bias on the Q, K, V projections only |
| **Tied embeddings** | Input embedding matrix = LM head transposed | Saves `vocab * d` parameters. That matters for small models (e.g. the 1B/3B class), where the embedding is a big share of total size. Large models usually do not tie |

- **DeepSeek is different in attention:** DeepSeek-V2/V3 use MLA (compress K and V into a small latent, Q33) instead of GQA, and a fine-grained MoE FFN (many small experts plus shared experts) instead of a dense SwiGLU FFN. The SwiGLU-style expert itself is still used.
- **Why one recipe?** Copying what was validated at scale is lower risk than ablating each part when a training run costs millions of dollars. Ablations at small scale (like Shazeer's) support the choices, but not all were tested rigorously at the largest scales.

**Example:** SwiGLU with d=4096: hidden size about `8/3 * 4096 ~ 10923`, which Llama-style models round up to a multiple (e.g. 11008 for 7B). Parameters: `3 * 4096 * 11008 ~ 135M` per layer, close to the classic `2 * 4096 * 16384 ~ 134M`.

**Code:** (executed, torch) RMSNorm output has unit RMS; SwiGLU(4096, 11008) has 135.27M parameters
```python
import torch, torch.nn as nn, torch.nn.functional as F
class RMSNorm(nn.Module):
    def __init__(s, d, eps=1e-6): super().__init__(); s.g = nn.Parameter(torch.ones(d)); s.eps = eps
    def forward(s, x): return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + s.eps) * s.g
class SwiGLU(nn.Module):
    def __init__(s, d, h): super().__init__(); s.w1 = nn.Linear(d, h, bias=False); s.w3 = nn.Linear(d, h, bias=False); s.w2 = nn.Linear(h, d, bias=False)
    def forward(s, x): return s.w2(F.silu(s.w1(x)) * s.w3(x))
```

**Follow-ups:**
- *RMSNorm vs LayerNorm?* LayerNorm subtracts the mean and has a bias; RMSNorm only rescales. The claim is that re-centering is not needed, and you save a little compute.
- *Why is GQA a good deal?* Decode is memory-bandwidth-bound and the KV cache is a large share of the traffic; 8 KV heads instead of 32 is a 4x cut with small quality loss.
- *Why does tying help small models only?* The embedding table is about `vocab * d`; with a 128k vocab and d=2048 that is ~262M parameters, a large fraction of a 1-3B model but a rounding error in a 70B one.

**Common mistakes:** Claiming every model uses every item (Qwen has QKV bias, DeepSeek uses MLA and MoE, tying differs by size). Saying SwiGLU is "proven" better rather than empirically better. Forgetting the 8/3 hidden-size adjustment.

### Q40 ⭐ 🟡 Do attention heads specialise? What does head pruning or head ablation tell you?
**Asked at:** research-leaning teams
**Say this first (1 line):** Yes, some heads clearly specialise (positional, syntactic, induction heads), but many heads are redundant and can be removed with small loss. Ablation tells you a head is necessary for a behaviour, not how it computes it, and models often compensate.

**Then explain:**
- **Evidence for specialisation:** Voita et al. (2019) studied a translation transformer and found a few "important" heads: ones attending to the previous or next token (positional), to syntactic relations, or to rare words. Induction heads (Olsson et al. 2022) copy the token that followed an earlier occurrence of the current token, and are tied to in-context learning (Q28).
- **Evidence for redundancy:** Michel et al. (2019, "Are sixteen heads really better than one?") removed large fractions of heads at test time with little drop, and in some layers reduced to a single head. Voita et al. pruned most heads in an encoder with small BLEU loss. These were BERT and NMT-sized models; do not assume the same numbers for modern LLMs.
- **What ablation does and does not show:**
  - Zero or mean ablation shows the head is *necessary* for the measured metric. It does not prove the head is the *mechanism*; other heads may take over (self-repair), and zeroing creates activations the model never saw.
  - Careful work uses activation patching or mean-ablation on a specific task and measures the effect on that task's logit difference.
- **Practical use:** structured head pruning reduces compute; in LLMs you usually need recovery fine-tuning, and GQA/MQA is the more common way to cut attention cost. Head importance scores (gradient-based, as in Michel et al.) guide which to drop.

**Example:** You ablate head L9.H3 in a small LM and next-token accuracy on repeated random sequences drops from 95% to 60%, while accuracy on normal text barely moves. That suggests the head matters for copying (induction-like) behaviour, not general language modelling. *(Illustrative scenario, not a real result.)*

**Code:** (not executed: transformers not installed, and the idea is illustrated in Q5's masked-attention code)
```python
# Head ablation recipe on any model that exposes per-head outputs (shape [B, H, T, dh] before W_o):
# out[:, head_idx] = 0            # zero ablation
# out[:, head_idx] = out.mean(0)  # mean ablation (less off-distribution)
# then compare task metric (accuracy / logit diff) with and without the change
```

**Follow-ups:**
- *Why can many heads be pruned if multi-head attention helps training?* Extra heads may matter mostly during training (easier optimisation) and be redundant afterwards. This is a hypothesis, not a settled result.
- *Do attention weights explain what a head does?* Not reliably (Q28); a head's effect also depends on the value vectors and what is written to the residual stream.
- *Is "one head = one job" true?* Often no. Heads can do several things, and jobs can be spread over several heads.

**Common mistakes:** Treating ablation damage as proof of mechanism. Claiming "most heads are useless" for modern LLMs on the basis of BERT/NMT pruning papers. Forgetting that pruning results depend on the task and metric.

### Q41 ⭐ 🟡 AI code review: this LLM-written attention snippet has bugs (softmax dim, missing mask, missing scaling, wrong reshape). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
**Say this first (1 line):** I check four things in any attention code: softmax over the key axis (last dim), causal mask applied before softmax, scores divided by sqrt(head_dim), and heads split with `view(B, T, H, dh)` then `transpose(1, 2)`, not `view(B, H, T, dh)`. Then I test it against `scaled_dot_product_attention`. The buggy code runs without errors and gives plausible-looking numbers, which is why these bugs are dangerous.

**The buggy snippet (as an LLM might write it):**
```python
def buggy_mha(x):                               # x: (B, T, D), H heads, dh = D // H
    B, T, D = x.shape
    q, k, v = x @ Wq, x @ Wk, x @ Wv
    q = q.view(B, H, T, dh); k = k.view(B, H, T, dh); v = v.view(B, H, T, dh)   # BUG 4
    scores = q @ k.transpose(-2, -1)            # BUG 3: no / sqrt(dh);  BUG 2: no causal mask
    w = torch.softmax(scores, dim=-2)           # BUG 1: normalises over queries, not keys
    return (w @ v).transpose(1, 2).reshape(B, T, D) @ Wo
```

**Then explain (each bug, what it does, and how I would prove it):**

| # | Bug | Effect | Evidence from my run (B=2, T=6, D=16, H=4) |
|---|---|---|---|
| 1 | `softmax(dim=-2)` | Weights sum to 1 over *queries* for each key. Each query's weights over keys do not sum to 1, so outputs have the wrong scale and meaning | Row sums were 0.47, 0.50, 0.68 (should be 1); column sums were 1.0 |
| 2 | No causal mask | Token t sees future tokens. In training the model cheats and the loss looks great; at inference it falls apart. Silent | Changing only the last token changed earlier outputs by up to 10.1; with the mask the change was exactly 0.0 |
| 3 | No `/ sqrt(dh)` | Dot products of `dh` random unit-variance entries have variance `dh`, so scores are large, softmax saturates to near one-hot and gradients vanish | With dh=64: score std 8.01 unscaled vs 1.00 scaled. Mean max-attention-weight per row 0.707 vs 0.017 |
| 4 | `view(B,H,T,dh)` on a `(B,T,D)` tensor | Shape is right, content is wrong. `view` reinterprets memory in order, so a "head" holds chunks of dimension slices from different tokens. Never raises an error | `bad[0,0,1]` equals dims 4-7 of token 0; `bad[0,0,4]` equals dims 0-3 of token 1 |

- Max abs difference from the reference output when only one bug is injected: softmax dim 2.41, no mask 2.30, no scaling 0.95, wrong reshape 3.68. All four together: 2.78. The fixed version: 2.4e-7 (float32 rounding).
- Same shape, no exceptions, finite numbers: so shape asserts alone do not catch these. Numerical tests do.

**Fixed version, checked against torch:**
```python
import torch, math, torch.nn.functional as F
def fixed_mha(x):
    B, T, D = x.shape
    q, k, v = x @ Wq, x @ Wk, x @ Wv
    q, k, v = [t.view(B, T, H, dh).transpose(1, 2) for t in (q, k, v)]   # (B, H, T, dh)
    scores = q @ k.transpose(-2, -1) / math.sqrt(dh)
    mask = torch.triu(torch.ones(T, T, dtype=torch.bool), diagonal=1)    # True above diagonal = future
    scores = scores.masked_fill(mask, float("-inf"))                     # mask BEFORE softmax
    w = torch.softmax(scores, dim=-1)                                    # over keys
    return (w @ v).transpose(1, 2).reshape(B, T, D) @ Wo                 # merge heads back

def ref(x):  # PyTorch's fused implementation
    q, k, v = [(x @ W).view(B, T, H, dh).transpose(1, 2) for W in (Wq, Wk, Wv)]
    return F.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, T, D) @ Wo
print((fixed_mha(x) - ref(x)).abs().max())   # 2.4e-07  (buggy_mha: 2.78)
```
All of this was executed with torch (seed 0, random weights scaled by 1/sqrt(D)); the numbers above are from that run.

**Follow-ups:**
- *How would you unit-test attention?* (1) Compare with `scaled_dot_product_attention`. (2) Causality test: perturb token t, assert outputs before t are unchanged. (3) Rows of attention weights sum to 1. (4) Permutation test for non-causal attention. (5) Head-split test with distinct values per token.
- *`dim=-2` vs `-1`: why do people get it wrong?* With shape `(B, H, T, T)` both are valid axes of the same size, so there is no shape error.
- *Other bugs to look for?* Mask applied after softmax; mask with 0 instead of `-inf`; padding mask forgotten; fully-masked rows giving NaN; dropout during eval; `reshape` after `transpose` without `contiguous` when using `view`; attention in fp16 without upcasting softmax.

**Common mistakes:** Trusting code because it runs and the shapes match. Fixing only the obvious bugs (scaling) and missing the reshape one. Putting the mask after softmax. Using `view` where a `transpose` is needed.

### Q42 ⭐ 🔴 Code: implement rotary position embeddings (RoPE) and show that scores depend on relative position.
**Asked at:** big tech, GenAI startups
**Say this first (1 line):** RoPE splits each query and key vector into 2D pairs and rotates pair i by the angle `pos * theta_i`. A dot product of two rotated vectors only depends on the difference of the angles, so the score depends on the relative offset `m - n` and not on the absolute positions.

**Then explain:**
- **Math (one pair):** rotate q at position m by angle `m*t`, k at position n by `n*t`. The dot product of two 2D vectors rotated by `a` and `b` equals the dot product of the originals rotated by `a - b`. So `<R_m q, R_n k> = <q, R_{n-m} k>` (function of `n - m` only). With `d/2` pairs and `theta_i = base^(-2i/d)` (base 10000 typical), the full score is a sum of such terms.
- **Applied to q and k only**, not v. Position is injected every layer, right before the dot product.
- **No parameters**, norm is preserved (rotation), and it composes with KV cache: cache the *rotated* keys, since a key's rotation depends only on its own position.
- **Convention note:** my code pairs adjacent dims (x[0],x[1]), (x[2],x[3])... Some implementations (e.g. Hugging Face Llama "rotate_half") pair dim i with dim i+d/2. They are equivalent up to a fixed permutation of dimensions, but weights must match the convention used in training.

**Example:** with a fixed q and k (d=64, float64) the score at offset 3 is 2.729352 whether q sits at position 3 or 5003. With no rotation the score is 7.382404, the same as offset 0. Offsets 0, 1, 2, 5, 50 give different scores (7.38, 4.95, 2.70, 9.59, 14.53), so position information is there.

**Code:** (executed, torch)
```python
import torch
torch.manual_seed(0)
def rope(x, pos, base=10000.0):
    """x: (..., T, d), d even; pos: (T,) ints. Rotate each pair (x[2i], x[2i+1]) by pos * theta_i."""
    d = x.shape[-1]
    theta = base ** (-torch.arange(0, d, 2, dtype=x.dtype) / d)        # (d/2,)
    ang = pos[:, None].to(x.dtype) * theta[None, :]                    # (T, d/2)
    cos, sin = ang.cos(), ang.sin()
    x1, x2 = x[..., 0::2], x[..., 1::2]
    out = torch.empty_like(x)
    out[..., 0::2] = x1 * cos - x2 * sin
    out[..., 1::2] = x1 * sin + x2 * cos
    return out

d = 64
q = torch.randn(d, dtype=torch.float64); k = torch.randn(d, dtype=torch.float64)
def score(m, n):
    return (rope(q[None], torch.tensor([m]))[0] @ rope(k[None], torch.tensor([n]))[0]).item()

for off in (0, 3, 17):
    print(off, [round(score(m + off, m), 6) for m in (0, 5, 100, 1000, 5000)])
# 0  [7.382404, 7.382404, 7.382404, 7.382404, 7.382404]   (equals unrotated q.k = 7.382404)
# 3  [2.729352, 2.729352, 2.729352, 2.729352, 2.729352]
# 17 [-0.126001, -0.126001, -0.126001, -0.126001, -0.126001]
S = rope(q.expand(8, d).clone(), torch.arange(8)) @ rope(k.expand(8, d).clone(), torch.arange(8)).T
# S is constant along every diagonal (Toeplitz): True. Rotation preserves norm: True
```
(I also checked the max spread across positions 0..2000 for offset 3: 4.7e-13, i.e. float64 rounding.)

**Follow-ups:**
- *Why does RoPE not extrapolate well past training length?* Angles at unseen positions were never trained on (Q38). Interpolation or base-scaling methods rescale them.
- *Why different frequencies?* Fast pairs resolve nearby offsets, slow pairs encode far offsets, like sinusoidal encoding (Q37) but applied as a rotation inside attention.
- *Does the score still depend on content?* Yes. Position changes the angle between q and k pairs, content sets their lengths and starting angles.
- *Cache before or after RoPE?* Store keys after rotation (each key keeps its own position); queries are rotated at the time of use. Alternative designs (cache un-rotated keys) cost recomputation each step.

**Common mistakes:** Rotating v. Using the same angle for every pair. Forgetting that the "relative" property holds for the dot product of rotated q and k, not for the vectors themselves. Mixing pairing conventions between code and checkpoint, which silently ruins a pretrained model. Testing with random q and k at each position, which hides the property (to see it, keep the content vectors fixed and vary the positions).

### Q43 ⭐ 🔴 Derive FlashAttention's online softmax and explain how tiling reduces HBM reads/writes.
**Asked at:** big tech, inference teams
**Say this first (1 line):** FlashAttention computes exactly the same attention output, but never writes the N x N score matrix to GPU main memory (HBM). It processes K/V in tiles inside fast on-chip memory (SRAM) and keeps a running max and running sum, so softmax can be finished one tile at a time. It saves memory traffic and memory, not FLOPs.

**Then explain:**
- **Why the standard way is slow:** `S = QK^T/sqrt(d)` (N x N) is written to HBM, read back for softmax, `P` is written, read again for `P V`. For long sequences attention is limited by memory traffic, not by arithmetic.
- **Derivation of online softmax (one row).** Safe softmax needs the max `m` and sum `l = sum_j exp(s_j - m)`. Process scores in blocks. After block 1 you hold `m1` and `l1`. A new block with max `b` and block sum `sum exp(s - m2)` arrives:
  - `m_new = max(m_old, b)`
  - `l_new = l_old * exp(m_old - m_new) + sum_j exp(s_j - m_new)`
  The old sum was measured relative to `m_old`; multiplying by `exp(m_old - m_new)` re-expresses it relative to `m_new`. This is exact algebra: `exp(s - m_old) * exp(m_old - m_new) = exp(s - m_new)`.
- **Including V:** keep an unnormalised accumulator `acc = sum_j exp(s_j - m) * v_j`. On each new tile: `acc_new = acc_old * exp(m_old - m_new) + exp(S_tile - m_new) @ V_tile`. At the very end, `O = acc / l`. Normalise once, at the end.
- **Tiling loop:** outer loop over query tiles (kept in SRAM), inner loop over K/V tiles streamed from HBM. For each query tile the N x N block never leaves SRAM.
- **IO count:** standard attention does `Theta(N d + N^2)` HBM accesses. FlashAttention does `Theta(N^2 d^2 / M)` where M is SRAM size (Dao et al. 2022), which is much smaller when `d^2` is far below M. Extra memory is O(N) (only the row statistics), not O(N^2). Backward recomputes the tile scores instead of storing P (extra FLOPs, less traffic, net faster).
- **Causal:** skip tiles entirely above the diagonal and mask only diagonal tiles.

**Example (numbers):** N=4096, d=128 for one head: the score matrix has 16.8M elements; Q, K, V, O together have 2.1M. Materialising S (written and read back, at least twice) dominates traffic. The tiled version only reads Q, K, V once per tile pass and writes O.

**Code:** (executed, numpy float64) tiled attention equals standard, including causal and huge scores
```python
import numpy as np
rng = np.random.default_rng(0)
def std_attn(Q, K, V, causal=False):
    S = Q @ K.T / np.sqrt(Q.shape[1])
    if causal: S = np.where(np.triu(np.ones_like(S, bool), 1), -np.inf, S)
    P = np.exp(S - S.max(1, keepdims=True)); P /= P.sum(1, keepdims=True)
    return P @ V

def flash_attn(Q, K, V, Br=16, Bc=32, causal=False):
    N, d = Q.shape; O = np.zeros_like(Q)
    for i in range(0, N, Br):                          # query tile
        q = Q[i:i+Br]
        m = np.full(len(q), -np.inf); l = np.zeros(len(q)); acc = np.zeros((len(q), d))
        for j in range(0, N, Bc):                      # stream K/V tiles
            if causal and j > i + len(q) - 1: break    # tile fully in the future
            S = q @ K[j:j+Bc].T / np.sqrt(d)
            if causal:
                qi = np.arange(i, i+len(q))[:, None]; kj = np.arange(j, j+S.shape[1])[None, :]
                S = np.where(kj > qi, -np.inf, S)
            m_new = np.maximum(m, S.max(1))
            p = np.exp(S - m_new[:, None])
            scale = np.exp(m - m_new)                  # rescale old stats (0 on the first tile)
            l = l * scale + p.sum(1)
            acc = acc * scale[:, None] + p @ V[j:j+Bc]
            m = m_new
        O[i:i+Br] = acc / l[:, None]
    return O

N, d = 200, 32
Q, K, V = (rng.normal(size=(N, d)) * 2 for _ in range(3))
for causal in (False, True):
    print(causal, np.abs(flash_attn(Q, K, V, causal=causal) - std_attn(Q, K, V, causal=causal)).max())
# False 1.12e-14    True 1.11e-14
Qb = Q * 100       # naive exp(S) without max-subtraction overflows to inf here; the tiled version still matches
print(np.allclose(flash_attn(Qb, K, V), std_attn(Qb, K, V)))     # True
```
A one-row check of just the max and denominator also matched (`m == s.max()`, `l == sum(exp(s-max))`) for a block size of 4 on 19 scores.

**Follow-ups:**
- *Is FlashAttention approximate?* No. Output is the same up to floating-point reordering. (Approximate attention methods are a different family.)
- *Does it reduce FLOPs?* No, slightly more in backward due to recomputation. It cuts HBM traffic and memory from O(N^2) to O(N).
- *Why does it matter for decode?* In decode there is one query, so the N x N matrix is not the issue; the cost is reading the KV cache. Split-K style kernels ("flash-decoding") parallelise over the KV length. Details depend on the kernel.
- *What changed in later versions?* FlashAttention-2 reorganised loops and work split for better GPU utilisation, FlashAttention-3 targets Hopper-specific hardware features. I would not quote speed-up numbers from memory.

**Common mistakes:** Saying it is an approximation or that it lowers FLOPs. Forgetting to rescale the accumulator `acc` (only rescaling `l`). Normalising each tile separately. Claiming O(N) *time*; time is still O(N^2), memory is O(N).

### Q44 ⭐ 🔴 What stability tricks do large transformers use (pre-norm, QK-norm, logit soft-capping, z-loss, warmup)? Why do loss spikes happen?
**Asked at:** big tech, research-leaning teams
**Say this first (1 line):** Most tricks keep some quantity from growing without bound: activations (pre-norm), attention logits (QK-norm, soft-capping), output logits (z-loss, soft-capping), or the early update size (warmup). Loss spikes have several interacting causes, and the field only partly understands them, so in practice people combine tricks and also skip bad data or roll back.

**Then explain:**

| Trick | What it does | Notes |
|---|---|---|
| **Pre-norm** | Normalise at the *input* of each attention/FFN block, residual path stays clean (`x + f(norm(x))`) | Gradients flow through the residual path, so deep models train with less fuss than post-norm. Cost: the residual stream can grow with depth, so some models add a final norm or extra norms (e.g. norms on sub-block outputs) |
| **Warmup** | Learning rate rises from ~0 over the first few thousand steps | Early on, Adam's second-moment estimates are poor and weights are random, so a full-size step can blow up |
| **QK-norm** | Normalise q and k (per head) before the dot product | Bounds attention logits, which otherwise can grow until softmax is almost one-hot (attention entropy collapse). Used in e.g. ViT-22B (Dehghani et al. 2023) and several recent LLMs |
| **Logit soft-capping** | `cap * tanh(x / cap)` on attention and/or final logits | Smooth hard bound. Gemma 2 used it (reported caps: 50 attention, 30 final logits); a later model family reportedly moved to QK-norm instead. Check the model card; it is not universal and can conflict with fused attention kernels |
| **z-loss** | Add `c * (log Z)^2` to the loss, with `Z = sum exp(logits)`, c ~ 1e-4 (PaLM) | Keeps the softmax normaliser near 1, so output logits do not drift in scale |
| **Others** | Gradient clipping (norm 1.0 is common), lower Adam beta2 (0.95 rather than 0.999), eps tuning, careful init, bf16 rather than fp16 | Adam with a slow beta2 reacts slowly to a sudden gradient jump, which can produce a spike |

- **Why spikes happen (not fully settled):**
  - *Attention-logit growth:* q.k grows, softmax saturates, gradients get sharp (Wortsman et al. 2023 reproduced this at small scale and showed QK-norm, z-loss help).
  - *Output-logit drift:* logits grow in scale, loss becomes sensitive.
  - *Adam dynamics:* if gradient statistics change suddenly while the second-moment estimate is stale, the update is much larger than intended (Molybog et al. 2023 analyse this).
  - *Data:* a bad batch (e.g. a corrupted or extremely repetitive document) can trigger or worsen a spike.
  - *Numerics:* low precision, rare large activations.
- **Operational response:** PaLM reported restarting from a checkpoint a bit before the spike and skipping the batches around it. This is a mitigation, not a root-cause fix.

**Example (executed):** soft-capping at 30 maps logits [-200, -50, -5, 0, 5, 50, 200] to [-30.00, -27.93, -4.95, 0, 4.95, 27.93, 30.00], so small values are nearly untouched and huge ones saturate. With exploded activations (q, k scaled by 50), `q.k/sqrt(d)` was 4047 raw but 1.74 after RMS-normalising q and k.

**Code:** (executed, torch)
```python
import torch
cap = 30.0
x = torch.tensor([-200., -50., -5., 0., 5., 50., 200.])
print((cap * torch.tanh(x / cap)).round(decimals=2))             # soft-cap
logits = torch.randn(4, 100) * 3
z_loss = 1e-4 * torch.logsumexp(logits, -1).pow(2).mean()        # add to cross-entropy
rms = lambda t: t / t.pow(2).mean().sqrt()                       # QK-norm idea (real versions have learnable scale)
q, k = torch.randn(64) * 50, torch.randn(64) * 50
print((q @ k / 8).item(), (rms(q) @ rms(k) / 8).item())          # large vs bounded
```

**Follow-ups:**
- *Pre-norm vs post-norm trade-off?* Post-norm can give slightly better final quality when it trains but is harder to optimise at depth and needs careful warmup. Pre-norm is the default for LLMs.
- *Does QK-norm cost quality?* Generally reported as neutral to positive; it adds a small compute cost and constrains logit scale, so a learnable temperature is often added.
- *How do you detect trouble early?* Track max attention logit, output-logit norm, gradient norm, update/weight ratios and loss per data source, not just the loss.

**Common mistakes:** Presenting one tricks list as "the" cause. Saying spikes are always bad data. Confusing z-loss (regularises the normaliser) with weight decay. Claiming every modern LLM uses soft-capping or QK-norm.

### Q45 ⭐ 🔴 What is multi-token prediction, and how does it relate to speculative decoding?
**Asked at:** big tech, GenAI startups
**Say this first (1 line):** Multi-token prediction (MTP) trains the model to predict several future tokens at each position instead of just the next one. It is a training objective; speculative decoding is an inference method. They connect because the extra prediction heads can serve as a built-in draft model that the main model then verifies.

**Then explain:**
- **MTP in training:** Gloeckle et al. (Meta, 2024) put `n` independent output heads on a shared trunk; head j predicts the token j steps ahead. The loss is the sum over heads. Reported benefits: better sample efficiency on code at larger model sizes, and faster inference through self-speculation. Gains were not uniform across tasks and sizes.
- **DeepSeek-V3's variant:** MTP modules are chained sequentially (each keeps the causal chain by taking the previous depth's representation plus the next token embedding), used as an extra training signal. They also report it can be reused for speculative decoding, with a high acceptance rate for the second token (they quote roughly 85-90%; treat as their reported figure).
- **Why it might help training:** it forces the hidden state to encode information about further ahead, a denser learning signal, and may help planning-like behaviour. This is the authors' hypothesis, not a settled explanation.
- **Speculative decoding (Leviathan et al.; Chen et al., 2023):** a cheap draft proposes `k` tokens. The big model scores all `k` in *one* forward pass (parallel, like prefill) and accepts a prefix using a rejection-sampling rule that keeps the output distribution *identical* to the big model's. You always get at least one token per big-model pass.
- **Relation:** a normal draft is a separate small model. With MTP the draft comes from extra heads on the same model: no second model to host or to keep in sync, and the draft sees the main model's hidden states. Verification step is the same.
- **Caveat:** extra heads cost parameters and training compute, and the farther ahead a head predicts, the lower its acceptance rate.

**Example (executed):** If each drafted token is accepted independently with probability a, the expected tokens per big-model pass with k drafts is `(1 - a^(k+1)) / (1 - a)`. For a=0.7, k=4 that is 2.77 (Monte Carlo over 200k trials: 2.768). For a=0.9, k=4: 4.10; k=8: 6.13. For a=0.5, extra drafts barely help: 1.94 at k=4, 2.00 at k=8. Real acceptance is not independent across positions, so this is an idealised guide, and drafting overhead is not counted.

**Code:** (executed, numpy)
```python
import numpy as np
def expected(a, k): return (1 - a**(k+1)) / (1 - a)
print({k: round(expected(0.7, k), 2) for k in (1, 2, 4, 8)})     # {1: 1.7, 2: 2.19, 4: 2.77, 8: 3.2}
rng = np.random.default_rng(0); a, k = 0.7, 4
def one():
    n = 0
    while n < k and rng.random() < a: n += 1
    return n + 1                       # accepted drafts + 1 token from the big model
print(np.mean([one() for _ in range(200000)]).round(3), round(expected(a, k), 3))   # 2.768 2.773
```

**Follow-ups:**
- *Is speculative decoding lossless?* With the standard acceptance rule and the same sampling settings, yes: the output distribution matches the target model. Greedy decoding: same text as greedy from the big model (up to floating-point differences).
- *Why does it speed up decode at all?* Decode is memory-bound; checking `k` tokens in one pass costs about the same weight reads as one token, so the extra tokens are nearly free until compute becomes the limit.
- *When does it not help?* Large batches (already compute-bound), low-acceptance domains such as high-temperature creative text, or when the draft is too slow.
- *Does MTP always make the base model better?* No. Reported gains depend on model size and task; the paper itself notes small models can get worse.

**Common mistakes:** Saying MTP outputs several tokens at once and they are all accepted (they must be verified). Confusing the training benefit of MTP with the inference benefit. Claiming speculative decoding changes output quality (the standard method does not). Using acceptance numbers from one model or domain as a general rule.

### Q46 ⭐ 🔴 Diffusion language models vs autoregressive LLMs: how do they differ, and what are the trade-offs?
**Asked at:** research-leaning teams, GenAI startups
**Say this first (1 line):** An autoregressive model writes left to right, one token per forward pass. A diffusion LM starts from a fully masked or noised sequence and refines many positions in parallel over several denoising steps, using bidirectional attention. The promise is fewer sequential steps and more parallelism; the open questions are quality at equal cost, caching and mature tooling. This is a fast-moving area, so I would treat claims as provisional.

**Then explain:**

| | Autoregressive (AR) | Masked-diffusion LM |
|---|---|---|
| Factorisation | `p(x) = prod_t p(x_t given x_<t)` | Learn to unmask: corrupt by masking tokens with random ratio, train to predict the masked ones; generate by starting all-masked and unmasking over T steps |
| Attention | Causal | Bidirectional (full) |
| Tokens per forward pass | 1 (more with speculation/MTP, Q45) | Several per step (parallel unmasking), step count is a knob |
| Likelihood | Exact | Bound (ELBO) only, so perplexity comparisons need care |
| KV cache | Yes, exact (Q6) | No straightforward exact cache because every position can change attention over all others; block-wise and approximate caching schemes exist and are active research |
| Length | Stops at EOS naturally | Often fixed canvas or block size chosen up front; variable length needs extra design |
| Editing / infilling | Awkward | Natural (bidirectional context) |

- **Examples (to my knowledge, check current status):** LLaDA (Nie et al., 2025, an ~8B masked-diffusion model trained from scratch, reported competitive with similar-size AR models on several benchmarks), plus commercial or preview systems from companies such as Inception Labs (Mercury) and Google (a Gemini Diffusion demo) that emphasise speed. I would not quote their speed numbers from memory.
- **Why parallel decode is not free:** tokens unmasked in the same step are sampled independently given the context, so strongly dependent tokens (e.g. two halves of a name) can become inconsistent. Fewer steps means more of this error. Quality improves with more steps, which erodes the speed advantage.
- **Compute view:** each denoising step is a full forward pass over the whole sequence (no cache), so total FLOPs can exceed AR unless steps are few. The gain is latency per token on hardware that is under-used in AR decode (batch size 1, memory-bound), not necessarily total cost at high batch.
- **Other trade-offs:** training and serving ecosystems (kernels, vLLM-style schedulers, RLHF recipes, evaluation) are far more mature for AR; instruction tuning and reasoning-style RL for diffusion LMs are earlier-stage. At the frontier scale, diffusion LMs have not (as far as I know) shown clear superiority over AR.

**Example:** Generate 256 tokens. AR: 256 sequential passes (each cheap with a KV cache). Diffusion with 64 steps unmasking 4 tokens per step: 64 passes, each over the full 256-token canvas. Whether that wins depends on step quality and hardware; at large serving batch AR with a cache may be cheaper per token. *(Illustrative arithmetic, not a benchmark.)*

**Code:** (not executed: conceptual; shown as pseudocode to explain the decode loop)
```python
# masked-diffusion decoding sketch
x = [MASK] * L
for step in range(T):                       # T << L is the speed idea
    probs = model(x)                        # bidirectional, full sequence
    conf  = probs.max(-1)                   # confidence per position
    pick  = top_k_most_confident(masked_positions(x), n=L // T)
    x[pick] = probs.argmax(-1)[pick]        # commit these; others stay masked (some schemes re-mask)
```

**Follow-ups:**
- *Can a diffusion LM do chain-of-thought and reasoning?* Possible, but the left-to-right causal flow of reasoning fits AR naturally; the evidence for diffusion at long reasoning is still limited.
- *Continuous vs discrete diffusion for text?* Text is discrete; most current competitive LMs use discrete masked diffusion over tokens, with earlier continuous-embedding diffusion approaches less successful at scale. Treat as a trend.
- *Where might it win?* Low-latency generation at small batch, infilling/editing, and tasks where bidirectional context helps.

**Common mistakes:** Saying diffusion LMs are "faster" without conditions (steps, batch size, caching). Forgetting they lack an exact KV cache. Claiming exact perplexity comparison with AR models. Overstating maturity or claiming they have replaced AR.

### Q47 ⭐ 🔴 Design question: choose the architecture and attention variant for a 32k-context, low-latency chat model that must run on one GPU.
**Asked at:** senior roles at big tech, product, GenAI startups
**Say this first (1 line):** I would pick a dense decoder-only transformer around 7-8B parameters with GQA (about 8 KV heads), RoPE, RMSNorm, SwiGLU and FlashAttention kernels. I would quantise weights (and maybe the KV cache) to fit the GPU, and use prefix caching and chunked prefill for latency. GQA is the key choice because at 32k the KV cache, not the weights, is what limits concurrency and decode speed.

**Then explain (requirements, then trade-offs):**
- **Requirements to clarify first:** which GPU (24 GB, 40 GB or 80 GB), concurrent users, p95 time-to-first-token (TTFT) and per-token latency targets, typical vs maximum prompt length (most chats are far below 32k), quality bar, and whether the context is real (retrieval over long docs) or just headroom.
- **Memory budget (executed arithmetic, 32 layers, head_dim 128, fp16 KV):**

| Attention | KV per token | 32k ctx, one sequence (fp16) | int8 KV |
|---|---|---|---|
| MHA, 32 KV heads | 512 KiB | 16.00 GiB | 8.00 GiB |
| GQA, 8 KV heads | 128 KiB | 4.00 GiB | 2.00 GiB |
| GQA, 4 KV heads | 64 KiB | 2.00 GiB | 1.00 GiB |

  Weights of an 8B model: 14.9 GiB in fp16, 7.5 GiB in int8, 3.7 GiB in 4-bit.
  Assuming 10% of GPU memory is reserved for activations and overhead, with GQA-8 and fp16 KV the number of full 32k sequences that fit is: 24 GB GPU 1 (fp16 weights) or 3 (int8 weights); 40 GB 5 or 7; 80 GB 14 or 16. With plain MHA, one 32k sequence alone takes 16 GiB, so a 24 GB card would be unusable at long context.
- **Attention variant:** GQA is the safe default (small quality loss, mature kernels, easy to serve). MLA (Q33) cuts the cache further but needs it trained in from the start (or an expensive conversion) and custom kernels. Sliding-window layers help a lot if some layers are windowed (e.g. half the layers at a 4k window: 2.25 GiB instead of 4.00 GiB per 32k sequence in my calculation), at the risk of weaker long-range retrieval; check quality on your own long tasks.
- **Positions:** RoPE, trained or extended to 32k with interpolation/YaRN-style scaling plus a long-context fine-tune (Q38). Evaluate with real long-context retrieval, not just perplexity.
- **Why not MoE or SSMs here?** MoE saves compute per token but all experts must sit in memory, which is the scarce resource on one GPU. SSM/hybrid models (Q27) shrink the cache but have less proven recall quality and a thinner tooling ecosystem; a hybrid is a reasonable experiment if memory is the binding limit.
- **Latency:**
  - *Decode* is memory-bandwidth-bound: each token reads all weights plus the sequence's KV. Smaller weights (quantisation) and fewer KV heads both reduce time per token. Long contexts make each token slower because the KV read grows.
  - *Prefill* of a 32k prompt is compute-bound. Back-of-envelope (not executed): `2 * 8e9 * 32768 ~ 5e14` FLOPs for the weights matmuls alone, plus attention cost. That is seconds on one GPU, so TTFT for a full 32k prompt cannot be tiny. Mitigate with prefix caching (system prompt, shared documents; Q24), chunked prefill so decode of other users is not blocked, and FlashAttention.
  - *Speculative decoding* (Q45) can cut per-token latency at small batch.
- **Serving stack:** a paged KV cache (PagedAttention-style; Part 10), continuous batching, admission control by KV memory, not only by request count.
- **Evaluation and monitoring:** long-context needle and multi-document QA at 4k/16k/32k, short-context quality regression, TTFT and inter-token latency percentiles, KV-cache utilisation, preemption/eviction rate.

**Example (the recommendation in one line):** 8B dense, GQA-8, RoPE with 32k extension, int8 or 4-bit weights, fp16 or int8 KV, on a 40 GB card: about 5-7 full 32k sequences at once, many more at typical chat lengths, with prefix caching for the system prompt.

**Code:** (executed, python) the arithmetic behind the table
```python
GiB = 2**30
def kv_per_token(layers, kv_heads, head_dim, nbytes=2): return 2 * layers * kv_heads * head_dim * nbytes
for kvh in (32, 8, 4):
    b = kv_per_token(32, kvh, 128)
    print(kvh, b // 1024, "KiB/token", b * 32768 / GiB, "GiB per 32k sequence")   # 512/16.0, 128/4.0, 64/2.0
params = 8e9
for gpu in (24, 40, 80):
    free = gpu * 0.9 - params * 2 / GiB            # fp16 weights, 10% reserve (an assumption)
    print(gpu, int(free * GiB // (kv_per_token(32, 8, 128) * 32768)), "full 32k sequences")   # 1, 5, 14
```

**Follow-ups:**
- *What if the budget is 24 GB?* Quantise weights to int8 or 4-bit, use GQA with an int8 KV cache, cap concurrency by KV memory, and consider a smaller model (3-4B). Check quality loss from quantisation on long-context tasks.
- *How do you keep latency low under load?* Continuous batching, chunked prefill, prefix caching, and limiting the max context per request for free tiers.
- *Would you use retrieval instead of 32k context?* Often yes for cost and latency: long-context is expensive per request. Choose by task; long context for whole-document reasoning, RAG when the answer lives in a few passages.

**Common mistakes:** Sizing only the weights and forgetting the KV cache (it is 4 GiB per 32k sequence even with GQA). Choosing MoE for a single-GPU deployment. Choosing the architecture before clarifying the GPU, concurrency and latency targets. Claiming exact latency numbers without hardware specifics. Evaluating long context only by perplexity.

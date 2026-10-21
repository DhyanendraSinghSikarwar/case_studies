# Book 2 — Part 01: Transformer Internals (attention, positional encoding, KV cache)

**Topic:** self-attention and multi-head attention, transformer block, encoder/decoder variants, positional encodings (sinusoidal, RoPE, ALiBi), KV cache, prefill vs decode, MQA/GQA/MLA, FlashAttention, long-context, MoE, alternatives to attention.
**Target:** 45  |  **Actual:** 47 (⭐⭐⭐ 15, ⭐⭐ 20, ⭐ 12)  |  **Date:** 2026-10-21  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Book 1 Part 9 gave a light transformer intro (self-attention, positional encoding, O(n^2)); this part is the deep treatment and must not repeat Book 1 answers verbatim. Tokenization, pretraining and decoding strategies are Part 2; serving (vLLM, PagedAttention, quantization, speculative decoding) is Part 10; LoRA/PEFT is Part 4.

---

### Q1 ⭐⭐⭐ 🟢 Explain self-attention step by step (Q, K, V, scaled dot-product, softmax). What does each of Q, K and V represent?
**Asked at:** all types; Capgemini/LTIMindtree/Hexaware-style GenAI loops, product, GCC
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Why did transformers replace RNNs/LSTMs? What are the remaining drawbacks of transformers?
**Asked at:** all types; service-company and GCC GenAI loops
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟡 What is multi-head attention? Why use several heads instead of one big head, and what are the tensor shapes and cost?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Encoder-only vs decoder-only vs encoder-decoder models: how do they differ, with examples and when to use each?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 What is the causal mask? Why can training be parallel over all tokens while generation is sequential?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 What is the KV cache, why does it speed up generation, and how does its memory grow?
**Asked at:** product, big tech, GenAI startups
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Prefill vs decode: what happens in each phase, and why is decode memory-bandwidth-bound while prefill is compute-bound?
**Asked at:** big tech, product, inference/platform teams
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Why does a transformer need positional information? Compare sinusoidal, learned and rotary (RoPE) encodings.
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Why is self-attention O(n^2), and how do you cope with long sequences?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 What are multi-query (MQA) and grouped-query attention (GQA)? How do they shrink the KV cache and what do they cost?
**Asked at:** big tech, product, inference teams
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 What is FlashAttention? Does it change the result, and why is it faster?
**Asked at:** big tech, product, GenAI startups
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Walk through a transformer block: residual connections, normalisation, feed-forward network. Pre-LN vs post-LN?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Code: implement causal scaled dot-product (multi-head) self-attention from scratch in PyTorch or NumPy.
**Asked at:** product, big tech, live-coding rounds
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Walk through one forward pass of a decoder-only LLM, from text to next-token probabilities.
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Live maths: estimate parameter count and KV-cache memory for a Llama-style model (layers, heads, head dim, context, batch).
**Asked at:** big tech, product, inference/platform teams
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 BERT vs GPT: pretraining objectives, attention pattern, typical uses. Why did decoder-only models come to dominate?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 Why do we divide attention scores by sqrt(d_k)? Give the variance argument.
**Asked at:** product, big tech
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 How does RoPE work, and how do position interpolation, NTK-aware scaling and YaRN extend context length?
**Asked at:** product, GenAI startups, big tech
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 What is the context window, and why is the effective context often shorter than the advertised one ("lost in the middle")?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 LayerNorm vs RMSNorm: what changes and why do modern LLMs prefer RMSNorm?
**Asked at:** product, GenAI startups
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 What does the feed-forward network do in a transformer? Explain GELU vs SwiGLU/gated FFNs and where most parameters live.
**Asked at:** product, GenAI startups
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 What is cross-attention, where is it used (T5, Whisper, diffusion, multimodal) and how does it differ from self-attention?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Which levers reduce KV-cache memory (GQA, quantised cache, sliding window, eviction)? Compare their trade-offs.
**Asked at:** big tech, inference/platform teams
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 What are prompt/prefix caching in LLM APIs, and how do they relate to the KV cache? How do you structure prompts to benefit?
**Asked at:** product, GCC, API-heavy teams
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Explain input embeddings, the unembedding (LM head) layer and weight tying. How does vocabulary size affect model size and cost?
**Asked at:** product, GenAI startups
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Where do a transformer's parameters live (attention vs FFN vs embeddings)? How is head dimension chosen?
**Asked at:** big tech, product
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Transformers vs state-space models (Mamba), linear attention and hybrid architectures: when would you pick each?
**Asked at:** product, research-leaning teams
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Do attention weights explain a model's output? What are induction heads and how do they relate to in-context learning?
**Asked at:** research-leaning teams, big tech
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 What are sliding-window, local and sparse attention? What are attention sinks and why do they matter for streaming?
**Asked at:** product, GenAI startups, inference teams
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 What breaks when you go from 8k to 128k–1M context (compute, memory, quality)? What is ring attention / sequence parallelism at a high level?
**Asked at:** big tech, GenAI startups
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 How do multimodal LLMs ingest images (ViT patches, projector, cross-attention vs token concatenation)?
**Asked at:** big tech, product, GenAI startups
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Use arithmetic intensity (roofline thinking) to explain why batching helps decode throughput and when it stops helping.
**Asked at:** big tech, inference/platform teams
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🔴 What is Multi-head Latent Attention (MLA, as in DeepSeek)? How does it compress the KV cache versus GQA?
**Asked at:** GenAI startups, big tech, research-leaning teams
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🔴 Explain Mixture-of-Experts layers: routing, load balancing, active vs total parameters, and the serving trade-offs.
**Asked at:** big tech, GenAI startups, product
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🔴 Code: write a decoding loop with a KV cache and verify it matches the no-cache output.
**Asked at:** product, big tech, inference teams
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🟢 Explain transformers to a non-technical stakeholder in two minutes.
**Asked at:** all types; senior/client-facing roles
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 Derive the sinusoidal positional encoding and its relative-position property. Why is it rarely used in modern LLMs?
**Asked at:** big tech, research-leaning teams
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 ALiBi vs RoPE: how does each handle length extrapolation?
**Asked at:** research-leaning teams, GenAI startups
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 What architectural choices do modern open LLMs (Llama, Qwen, DeepSeek) make: RMSNorm, SwiGLU, RoPE, GQA, no biases, tied embeddings? Why?
**Asked at:** product, GenAI startups
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 Do attention heads specialise? What does head pruning or head ablation tell you?
**Asked at:** research-leaning teams
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🟡 AI code review: this LLM-written attention snippet has bugs (softmax dim, missing mask, missing scaling, wrong reshape). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Code: implement rotary position embeddings (RoPE) and show that scores depend on relative position.
**Asked at:** big tech, GenAI startups
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 Derive FlashAttention's online softmax and explain how tiling reduces HBM reads/writes.
**Asked at:** big tech, inference teams
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 What stability tricks do large transformers use (pre-norm, QK-norm, logit soft-capping, z-loss, warmup)? Why do loss spikes happen?
**Asked at:** big tech, research-leaning teams
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 What is multi-token prediction, and how does it relate to speculative decoding?
**Asked at:** big tech, GenAI startups
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 Diffusion language models vs autoregressive LLMs: how do they differ, and what are the trade-offs?
**Asked at:** research-leaning teams, GenAI startups
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 Design question: choose the architecture and attention variant for a 32k-context, low-latency chat model that must run on one GPU.
**Asked at:** senior roles at big tech, product, GenAI startups
<!-- ANSWER_PENDING -->

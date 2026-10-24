# Book 2 — Part 10: Deployment (vLLM, TGI, quantization, batching, speculative decoding, latency and cost)

**Topic:** serving LLMs in production: prefill vs decode, KV-cache memory and capacity planning, PagedAttention and the vLLM block manager, continuous batching, chunked prefill, prefix caching, latency metrics and SLOs, quantization (INT8, INT4, FP8, GPTQ, AWQ, bitsandbytes, KV-cache quantization), speculative decoding, parallelism, serving frameworks (vLLM, TGI, TensorRT-LLM, SGLang, llama.cpp), multi-LoRA, constrained decoding cost, streaming, autoscaling, cost per million tokens, benchmarking, long context, disaggregation, and design and diagnosis questions
**Target:** 45  |  **Actual:** 49 (⭐⭐⭐ 16, ⭐⭐ 21, ⭐ 12)  |  **Date:** 2026-10-24  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: earlier parts introduced these ideas and deferred depth to this part; answers here go deeper and cross-reference, not repeat. Part 1 covers the KV cache and its growth (Q6), prefill vs decode mechanism (Q7), MQA/GQA (Q10), FlashAttention (Q11), KV and parameter maths (Q15), KV-reduction levers (Q23), API prompt caching (Q24), long-context breakage (Q30), arithmetic intensity and batching (Q32), MLA (Q33), MoE serving trade-offs (Q34), a KV-cache decoding loop (Q35), FlashAttention's online softmax (Q43) and multi-token prediction (Q45). Part 2 covers token costs (Q5), training parallelism (Q34) and test-time compute (Q43). Part 3 covers constrained decoding at the logit level (Q22), prompt-level cost cuts (Q36) and slow grammar compilation (Q40). Part 4 covers NF4 and QLoRA (Q6), merging adapters (Q13), the fine-tuned-small-model break-even (Q25) and merged vs multi-LoRA serving (Q32). Part 6 covers the RAG latency budget (Q31) and cost estimate (Q32); Part 7 covers reranker serving (Q21); Part 8 covers agent cost and latency (Q37); Part 9 covers evaluation cost (Q33) and is where quantized-model quality checks get their eval method. Part 10 owns engine internals, serving-side capacity and cost maths, quantization for inference, speculative decoding, framework choice and production diagnosis. Book 4 owns generic MLOps, Docker and Kubernetes, so autoscaling and rollout questions here stay LLM-specific (signals, KV memory, cold starts); monitoring and tracing depth goes to Part 11. Engines, flags, supported hardware, framework status (TGI's docs now say maintenance mode) and benchmark numbers change quickly: answers must hedge current-state claims and tell the reader to check live docs. Headline numbers (vLLM 2-4x, Orca 36.9x, speculative 2-3x, Medusa and EAGLE speedups, DistServe 7.4x, Sarathi-Serve gains, GPTQ and AWQ speedups) are the authors' reported results in their stated setups and must be labelled as such. No GPU prices appear; cost questions use symbolic or clearly hypothetical numbers.

Evidence limits: no candidate-reported deployment questions were found (searches for Glassdoor, Blind and Reddit reports returned only job postings and prep guides); the "Asked at" tags are company types, and where an interview-prep guide describes a prompt this is marked as a guide, not a candidate report. The guides are commercial or institute pages that say their numbers are illustrative. Star ratings blend topic frequency across guides with judgement. See research_notes/Book2_Part10_sources.md for which pages were opened.

---

### Q1 ⭐⭐⭐ 🟡 Prefill vs decode at the serving level: how do the two phases map to TTFT and per-token latency, why are they bottlenecked differently, and what does that change about what you optimise first? (Part 1 Q7 has the mechanism; go to the serving consequences.)
**Asked at:** all types; inference-platform teams, GenAI-engineer and MLE rounds; interview-prep guide, not a candidate report
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟡 Latency and throughput metrics for LLM serving: define TTFT, TPOT/ITL, end-to-end latency, tokens per second (system vs per user), requests per second and goodput. How do percentiles and SLOs apply, and why is the mean misleading?
**Asked at:** all types; inference-platform teams, product companies, GCCs; interview-prep guide, not a candidate report
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟡 Budget GPU memory for serving: weights, KV cache, activations and runtime overhead. For a 7B and a 70B model on an 80 GB GPU, what fits, what does gpu_memory_utilization control, and how do tensor-parallel shards change the maths? (Part 1 Q15 has the KV formula.)
**Asked at:** all types; inference-platform teams, MLE rounds; interview-prep guide, not a candidate report
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 Capacity planning from the KV cache: how many concurrent sequences fit after loading the weights, how do context length, GQA/MQA and cache dtype change that number, and how do you turn it into a replica count using Little's law?
**Asked at:** product companies, GCCs, inference-platform teams; interview-prep guide, not a candidate report
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 What is PagedAttention and how does vLLM's block manager work (fixed-size blocks, block tables, near-zero fragmentation, sharing and copy-on-write)? What problem in earlier systems did it fix?
**Asked at:** all types; inference-platform teams, AI labs and GenAI startups; interview-prep guide, not a candidate report lists it as a core topic
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Static vs dynamic vs continuous (in-flight, iteration-level) batching: how does each work, why does continuous batching raise throughput when output lengths vary, and what does it cost (scheduling, memory pressure)?
**Asked at:** all types; inference-platform teams, GenAI startups; interview-prep guide, not a candidate report
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Throughput vs latency: how do batch size and concurrency move TTFT, TPOT and tokens per second, where is the knee of the curve, and how do you pick an operating point for a chat product vs an offline job?
**Asked at:** product companies, inference-platform teams, GCCs; interview-prep guide, not a candidate report frames chat vs offline objectives
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Quantization for inference: what do INT8, INT4 and FP8 change (weight-only vs weight-and-activation, memory vs compute), which phase does each speed up, and why is the speedup not simply 'bits halved, speed doubled'?
**Asked at:** all types; inference-platform teams, GenAI startups, GCCs; interview-prep guide, not a candidate report
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 GPTQ vs AWQ vs bitsandbytes (LLM.int8 and NF4): how does each work, what hardware and kernels support them, and how would you choose for serving vs for QLoRA-style fine-tuning? (Part 4 Q6 covers NF4 for training.)
**Asked at:** all types; GenAI startups, inference-platform teams; interview-prep guide, not a candidate report lists GPTQ and AWQ
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 How do you validate a quantized model before shipping (task evals, long-context and retrieval checks, calibration data choice, latency re-measurement, rollback plan), and what silently degrades?
**Asked at:** product companies, GCCs, inference-platform teams; interview-prep guide, not a candidate report
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Speculative decoding: how does a draft model propose and the target verify, why is the output distribution unchanged, how does acceptance rate set the speedup, and when does it not help?
**Asked at:** all types; inference-platform teams, AI labs; interview-prep guide, not a candidate report lists it with its limits
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Choose a serving stack: compare vLLM, TGI, TensorRT-LLM, SGLang and llama.cpp/Ollama (hardware, features, ops effort, maturity), and say how you decide for a given workload.
**Asked at:** all types; product companies, GCCs, inference-platform teams; interview-prep guide, not a candidate report lists these frameworks
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Cost per million tokens: derive it from GPU price per hour, throughput and utilisation, separate input from output tokens, and explain why low utilisation is the usual reason self-hosting loses.
**Asked at:** product companies, GCCs, GenAI startups; interview-prep guide, not a candidate report includes cost-per-million-token maths
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Prefix caching inside an engine (vLLM-style block hashing, LRU eviction) vs a provider's prompt caching: how does each work, what does it save (prefill, not decode), and how do you structure prompts and routing to get hits? (Part 1 Q24 covers API prompt caching.)
**Asked at:** product companies, inference-platform teams; interview-prep guide, not a candidate report
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Code: write a KV-cache size and concurrency calculator (layers, KV heads, head dim, dtype, context, batch, weights, GPU memory) and check it against a hand-worked Llama-style example, including the GQA vs MHA difference.
**Asked at:** product companies, inference-platform teams, live-coding or take-home rounds; interview-prep guide, not a candidate report lists KV memory estimation
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 Code: given a log of requests (arrival, first-token and finish times, output tokens), compute TTFT, TPOT and E2E percentiles, throughput and goodput against an SLO.
**Asked at:** product companies, inference-platform teams, live-coding rounds
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 Tensor vs pipeline vs data parallelism for inference: when must you shard, how do they affect latency and throughput, and when are two replicas better than one TP=2 deployment? (Part 2 Q34 covers training parallelism.)
**Asked at:** inference-platform teams, GCCs; interview-prep guide, not a candidate report lists TP=2 vs TP=4 and TP vs replicas
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 Self-host vs call an API: build the break-even (token volume, utilisation, engineering and on-call cost, privacy, quality, latency, lock-in) and say what would change your answer. (Part 4 Q25 covers the fine-tuned-small-model case.)
**Asked at:** product companies, GCCs, GenAI startups; interview-prep guide, not a candidate report lists managed API vs self-hosting
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 Streaming tokens with SSE: how does the path from engine to browser work, what is backpressure for a slow client, how do you handle cancellation and disconnects so GPU work stops, and how do proxies break streaming?
**Asked at:** product companies, inference-platform teams; interview-prep guide, not a candidate report poses streaming with backpressure as a design prompt
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Chunked prefill and scheduling: how does the scheduler mix prefill and decode under a token budget, why does a long prompt stall other users' decoding without chunking, and how do max_num_batched_tokens and max_num_seqs trade TTFT against inter-token latency?
**Asked at:** inference-platform teams, AI labs; interview-prep guide, not a candidate report lists chunked prefill; vLLM docs describe the token-budget knobs
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Preemption and admission control in an engine: what happens when KV blocks run out (recompute vs swap), what does it do to tail latency, and what do you tune or monitor to avoid it?
**Asked at:** inference-platform teams; interview-prep guide, not a candidate report lists preemption
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 KV-cache quantization (for example FP8): how much capacity does it add, what does it do to quality and speed, why do scales and calibration matter, and when is it risky? (Part 1 Q23 compares KV levers.)
**Asked at:** inference-platform teams, GenAI startups; interview-prep guide, not a candidate report lists KV-cache quantization trade-offs
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 FP8 and W8A8 serving: what are the E4M3 and E5M2 formats, which GPUs support them natively, how do static vs dynamic scaling and SmoothQuant-style outlier handling work, and when do you prefer FP8 over INT4 weight-only?
**Asked at:** inference-platform teams, AI labs; interview-prep guide, not a candidate report lists FP8, INT8 and INT4 formats
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Speculative decoding variants: draft model vs n-gram or prompt lookup vs Medusa heads vs EAGLE feature-level drafting. What does each need (training, memory), and why does speedup fall at high batch sizes? (Part 1 Q45 links multi-token prediction.)
**Asked at:** inference-platform teams, AI labs; interview-prep guide, not a candidate report lists Medusa, EAGLE and lookahead
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Multi-LoRA serving: how do engines keep one base model and many adapters (batched adapter kernels, adapter paging as in S-LoRA and Punica, max loaded adapters, dynamic loading), and what limits latency and adapter count? (Part 4 Q32 covers merged vs unmerged.)
**Asked at:** GenAI startups, platform teams, multi-tenant SaaS; interview-prep guide, not a candidate report lists multi-LoRA serving
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 What does structured or constrained decoding cost at serving time (grammar compilation, per-token masking, batch interaction, first-request latency), and how do engines such as vLLM and SGLang reduce it? (Part 3 Q22 covers the mechanism; Q40 the p99 problem.)
**Asked at:** product companies, GenAI startups; interview-prep guide, not a candidate report lists guided decoding and slow first requests
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Autoscaling and cold starts for GPU-backed LLM replicas: which signals scale well (queue depth, KV-cache usage, running requests) vs which mislead (GPU utilisation), what dominates cold start (weight download and load), and how do you hedge? (Book 4 owns generic Kubernetes autoscaling.)
**Asked at:** product companies, GCCs, platform teams; interview-prep guide, not a candidate report lists autoscaling signals and cold starts
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Model routing and caching to cut cost: explicit routing, classifier routing and cascades, exact-match and semantic response caches, and the quality and safety risks of each. (Part 8 Q37 covers agent cost levers; Part 3 Q36 prompt-level cuts.)
**Asked at:** product companies, GenAI startups, GCCs; interview-prep guide, not a candidate report lists routing, cascades and caching
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Rate limiting and overload protection for an LLM API: why requests-per-minute is a poor limit, token-based limits, queue length and timeouts, 429 and retry-after, load shedding, and priority tiers.
**Asked at:** product companies, platform teams; interview-prep guide, not a candidate report lists token-based limits and overload protection
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Benchmarking an LLM server properly: open-loop (fixed arrival rate, Poisson or bursty) vs closed-loop (fixed concurrency), realistic prompt and output length distributions, warm-up, prefix-cache effects, and which numbers to report.
**Asked at:** inference-platform teams, senior MLE rounds; interview-prep guide, not a candidate report; the vLLM benchmark docs and the TGI v3 post describe methodology
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Long-context serving: how do prefill time, KV memory and attention cost grow at 32k to 200k+ tokens, and what helps (chunked prefill, prefix reuse, KV quantization, sliding window or GQA/MLA models, offload, sequence parallelism)? (Part 1 Q30 covers why quality and cost break.)
**Asked at:** product companies, AI labs, inference-platform teams; interview-prep guide, not a candidate report poses a 200K-token serving design
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🔴 Disaggregated prefill and decode (DistServe, Mooncake, vLLM's disaggregated prefilling): why separate the phases, what does it improve (goodput under TTFT and TPOT SLOs, tail ITL), what does it not improve, and what does the KV transfer cost?
**Asked at:** inference-platform teams, AI labs, large-scale serving teams; interview-prep guide, not a candidate report lists disaggregation
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Estimate the ceiling for decode speed: using memory bandwidth and bytes read per token, estimate tokens per second at batch 1 for a 7B and a 70B model, then explain MFU/MBU and why nvidia-smi 'GPU utilisation 100%' says little.
**Asked at:** inference-platform teams, MLE rounds; interview-prep guide, not a candidate report lists throughput estimation and misleading GPU utilisation
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 Offline batch inference vs online serving: how do the objectives, batching, scheduling, cost and failure handling differ (throughput-optimised jobs, spot capacity, checkpointing, length sorting)?
**Asked at:** product companies, data and GenAI platform teams; interview-prep guide, not a candidate report contrasts chat with offline summarisation
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 Hardware choice for serving: how do GPU memory capacity, memory bandwidth, FP8 support and interconnect decide between options such as L4, A100, H100 and H200-class cards, and when does a smaller or older card win on cost per token?
**Asked at:** product companies, GCCs, inference-platform teams; interview-prep guide, not a candidate report lists GPU selection (no prices quoted here)
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 llama.cpp, GGUF and Ollama: what are they for (CPU or Apple Silicon, edge, local development, hybrid CPU-GPU offload), how do GGUF quantization levels differ from GPTQ/AWQ, and where do they stop being the right tool for a server?
**Asked at:** product companies, startups, edge and on-device teams; interview-prep guide, not a candidate report
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 Replicas behind a load balancer: why does prefix caching and KV reuse need cache-aware routing or sticky sessions, what are the risks (hot spots, uneven load), and what do round-robin and least-loaded routing get wrong for LLMs?
**Asked at:** inference-platform teams, platform teams; TGI's docs note the replica cache problem; interview-prep guide, not a candidate report lists KV-cache-aware routing
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 Code: write a toy continuous-batching scheduler simulation (arrivals, per-request output lengths, a batch-slot limit) and compare it with static batching on throughput and latency percentiles.
**Asked at:** inference-platform teams, AI labs, live-coding rounds; interview-prep guide, not a candidate report lists a request scheduler with priority and preemption as a coding round
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🔴 Code: write a toy paged KV-block allocator (fixed-size blocks, block tables, reference counts, shared prefixes with copy-on-write, free list) and show fragmentation compared with contiguous allocation.
**Asked at:** inference-platform teams, AI labs, live-coding rounds; interview-prep guide, not a candidate report lists a KV-cache memory allocator as a coding round
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 Code: implement INT8 per-tensor and per-channel weight quantize and dequantize in NumPy, measure the error (MSE, max error, output error on a matmul), and show what an outlier channel does.
**Asked at:** product companies, GenAI startups, live-coding rounds
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🟡 Code: simulate speculative decoding acceptance (draft and target token distributions, the accept-or-resample rule), check that the output distribution matches the target, and compare measured tokens per step with the closed-form formula.
**Asked at:** inference-platform teams, AI labs, live-coding rounds
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Derive the expected speedup of speculative decoding: expected accepted tokens per verification step as a function of acceptance rate and draft length, then include draft cost to find the best draft length.
**Asked at:** AI labs, inference-platform teams, research-leaning rounds
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🟡 AI code review: this LLM-written serving and benchmark script has bugs (KV size uses attention heads instead of KV heads, ignores dtype bytes, closed-loop benchmark with one repeated prompt, reports only mean latency, model loaded per request, blocking call in an async handler, no max_tokens, gpu memory fraction set to 1.0). Find and fix them.
**Asked at:** product companies, big tech, AI-era code-review rounds
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 Design question: an LLM serving platform for N requests per second with TTFT and TPOT SLOs (workload assumptions, capacity maths, engine choice, batching and scheduling, caching, autoscaling, routing, observability, failure modes).
**Asked at:** senior roles; interview-prep guide, not a candidate report poses '100K req/s of an 8B model' and 'design an LLM inference API'
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 Design question: cut LLM serving cost by 50% without hurting quality (where to measure first, then quantization, batching and utilisation, caching, routing, smaller or distilled models, spot capacity, and how you prove quality held).
**Asked at:** senior roles at product companies, GCCs, platform teams
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 Production diagnosis: p99 TTFT doubled after a traffic increase and a deploy while GPU 'utilisation' looks fine. Walk through how you localise the cause (queueing, preemptions, prefix-cache hit rate, prompt template change, long-tail prompts, a noisy tenant) and fix it.
**Asked at:** senior roles, inference-platform teams; interview-prep guide, not a candidate report lists tail latency, prefix-cache and prompt-template scenarios
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 Production diagnosis: a replica crashes with CUDA out-of-memory after hours of stable traffic, or fails to start at long context. Explain the causes (KV growth, activation peaks, fragmentation, logits for long prompts, memory settings) and the fixes.
**Asked at:** senior roles, inference-platform teams; interview-prep guide, not a candidate report lists long-context startup failures and OOM from batch size; TGI's v3 post notes prompt-logits memory
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🔴 Design question: scale a chat product from 8k to 200k-token contexts (memory, prefill latency, cost, caching, model choice, degradation and limits, evaluation of quality at length).
**Asked at:** senior roles; interview-prep guide, not a candidate report poses a 200K-token serving design
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 Design question: a multi-tenant inference service with priority tiers, per-tenant token budgets, fairness, per-tenant LoRA adapters, noisy-neighbour isolation and SLO reporting.
**Asked at:** senior roles at platform teams and SaaS companies; interview-prep guide, not a candidate report poses a multi-tenant service with priority queues and rate limits
<!-- ANSWER_PENDING -->

# Book 2 — Part 04: Fine-tuning (SFT, LoRA/QLoRA, PEFT, Distillation)

**Topic:** when to fine-tune, SFT and instruction tuning (data, loss masking, chat templates), LoRA and QLoRA (rank, alpha, target modules, memory maths, merging), other PEFT methods and LoRA variants, catastrophic forgetting and evaluation, knowledge distillation (classic, white-box and black-box LLM distillation, forward vs reverse KL), and fine-tuning design and debugging.
**Target:** 45  |  **Actual:** 47 (⭐⭐⭐ 15, ⭐⭐ 21, ⭐ 11)  |  **Date:** 2026-10-22  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Book 1 only frames fine-tuning basics (B1P09-Q39 full vs adapters vs feature extraction and forgetting; B1P09-Q14 prompting vs RAG vs fine-tuning, depth deferred to Book 2; B1P08-Q39 transfer learning; B1P08-Q55 and B1P09-Q47 distillation basics for serving), so answers here must go deeper and cross-reference rather than copy. Part 2 already covers pretraining vs continued pretraining vs fine-tuning (Q8), extending a tokenizer and model to a new domain (Q36), bf16/fp16 (Q27) and the 16 bytes-per-parameter training memory accounting (Q34); Part 3 covers prompt and tool-calling design. RLHF, DPO and safety belong to Part 5; quantization, serving and merging for deployment to Part 10; evaluation depth (LLM-as-judge, benchmarks) to Part 9; RAG to Parts 6-7. Library details (Hugging Face PEFT and TRL parameter names, defaults) change quickly: answers must use the names from the docs opened on 2026-10-22 and tell the reader to check current docs.

---

### Q1 ⭐⭐⭐ 🟢 Prompting vs RAG vs fine-tuning: what is your decision framework, and in what order do you try the adaptation methods?
**Asked at:** all types; service-company, GCC and product GenAI loops
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is supervised fine-tuning (instruction tuning)? What does it teach a model, what does it not teach, and what is the training loss?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is LoRA and how does it work? Why is it parameter-efficient, and what stays frozen?
**Asked at:** all types; product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 How do you choose LoRA's rank, alpha and dropout? What does the alpha/r scaling do?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 Which modules should LoRA target (query/value only vs all linear layers including the MLP), and why?
**Asked at:** product, GenAI startups
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 What is QLoRA? Explain NF4, double quantization and paged optimizers, and where precision matters during training.
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Memory maths: how much GPU memory does full fine-tuning, LoRA and QLoRA need for a 7B or 13B model, and can you fine-tune a 13B model on one 40 GB GPU?
**Asked at:** product, GenAI startups, big tech
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 What is catastrophic forgetting in fine-tuning? How do you detect it, and how do you mitigate it?
**Asked at:** all types; product, GenAI startups
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 How do you evaluate a fine-tuned model before shipping (task metric, general-capability regression, human or LLM judging)?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 How much data do you need for SFT, and what matters more, quality or quantity? How do you build and clean the dataset?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 In SFT, why do we mask prompt tokens from the loss (train on completions or assistant turns only)? How do label shifting, the ignore index and packing interact?
**Asked at:** product, GenAI startups, fine-tuning teams
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Why do chat templates and the EOS token matter in fine-tuning? What breaks when training and inference templates differ?
**Asked at:** product, GenAI startups, fine-tuning teams
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How do you merge a LoRA adapter into the base model? Why does a merged LoRA add no latency, why can't a QLoRA adapter be merged directly, and when would you keep adapters separate?
**Asked at:** product, GenAI startups, inference/platform teams
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Code: implement a LoRA linear layer from scratch in PyTorch (frozen weight, A and B initialisation, alpha/r scaling, merge) and verify it against W + BA.
**Asked at:** product, big tech, live-coding rounds
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Code: implement the SFT loss with prompt masking in PyTorch (shifted labels, ignore index) and check it against F.cross_entropy.
**Asked at:** product, big tech, live-coding rounds
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 Full fine-tuning vs parameter-efficient fine-tuning: when is full fine-tuning justified, and how do learning rates differ?
**Asked at:** product, GenAI startups, big tech
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 What hyperparameters matter in SFT (learning rate, epochs, batch size, warmup, scheduler, max length), and how do you recognise overfitting?
**Asked at:** product, GenAI startups, fine-tuning teams
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 Compare PEFT methods: adapters, prefix tuning, prompt tuning, IA3 and LoRA. When would you use each?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 What do LoRA variants change (rsLoRA, DoRA, LoRA+, LoftQ initialisation)? When are they worth trying?
**Asked at:** GenAI startups, research-leaning teams, fine-tuning teams
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Does a higher LoRA rank always help? What limits capacity, and how do you decide when LoRA is not enough?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 How do you create instruction data: human-written, synthetic from a stronger model, self-instruct? What are the quality and licensing risks?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 What is knowledge distillation? Explain teacher and student, soft targets, temperature and the combined KL plus cross-entropy loss.
**Asked at:** all types; product, GCC
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 How does distillation work for LLMs: logit-level (white-box) vs sequence-level or response distillation (black-box)? Does the student need the teacher's tokenizer?
**Asked at:** product, GenAI startups, big tech
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Forward vs reverse KL in LLM distillation (MiniLLM): what is the difference, and what does on-policy distillation fix?
**Asked at:** research-leaning teams, big tech, GenAI startups
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 When do you fine-tune a small model instead of calling a large API model? Work through a cost, latency, privacy and quality break-even.
**Asked at:** product, GCC, API-heavy teams
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 For classification or extraction, would you fine-tune an LLM with SFT, add a classification head, or use a small encoder? How do you choose?
**Asked at:** product, GCC, applied ML teams
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 How do you mix tasks and general data in SFT (data mixtures, ordering, replay of general data), and what goes wrong with a narrow dataset?
**Asked at:** product, GenAI startups, fine-tuning teams
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How do you fine-tune for structured output or tool calling (dataset format, loss on tool calls, evaluation)? How does it relate to prompting for the same?
**Asked at:** product, GenAI startups, agent-building teams
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Continued pretraining vs SFT for a new domain or language: when do you need continued pretraining before SFT?
**Asked at:** product, GenAI startups, India product companies
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 What does SFT overfitting look like (train vs validation loss, memorisation, narrow style), and what are your defences (early stopping, fewer epochs, regularisation, data)?
**Asked at:** product, GenAI startups, fine-tuning teams
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 What training-efficiency settings matter in practice (sequence packing, padding-free batches, gradient checkpointing, gradient accumulation, bf16), and what do they cost?
**Asked at:** product, GenAI startups, fine-tuning teams
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you serve fine-tuned models: merged weights vs multi-LoRA serving, adapter swapping and versioning?
**Asked at:** product, platform teams, inference teams
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Hosted fine-tuning APIs vs self-hosted fine-tuning: what are the trade-offs in control, data privacy, cost and lock-in?
**Asked at:** product, GCC, regulated-industry teams
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you keep PII and benchmark contamination out of fine-tuning data (deduplication, held-out sets, filtering)?
**Asked at:** product, GCC, regulated-industry teams
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 A fine-tune did not learn or got worse. Walk through your debugging checklist (template, masking, learning rate, data, evaluation).
**Asked at:** product, GenAI startups, fine-tuning teams
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 Should you fine-tune a base or an instruct/chat checkpoint? What are the trade-offs?
**Asked at:** product, GenAI startups, fine-tuning teams
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 AI code review: this LLM-written LoRA/SFT training script has bugs (unshifted or unmasked labels, wrong learning rate, merging in 4-bit, dropout left on at eval, wrong target modules). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🔴 Why does low-rank adaptation work? Derive the parameter count, the identity initialisation, and the effective scaling of the update.
**Asked at:** big tech, research-leaning teams, GenAI startups
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🔴 Chain-of-thought and rationale distillation: how do you distil reasoning from a stronger model, and what are the limits and risks?
**Asked at:** big tech, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🔴 What is the superficial alignment hypothesis (LIMA)? What evidence supports it, and what are its critiques and implications for data curation?
**Asked at:** research-leaning teams, big tech, GenAI startups
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🔴 How do multi-adapter composition and model merging work (weighted adapters, task arithmetic, TIES-style merging), and what are the risks?
**Asked at:** research-leaning teams, GenAI startups, platform teams
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Design question: plan a fine-tune of a 13B-70B model on limited GPUs (QLoRA, gradient checkpointing, sharding), including how you validate the plan before spending the compute.
**Asked at:** senior roles at big tech, product, GenAI startups
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 Design question: build an end-to-end fine-tuning project for a support-ticket extraction task (data, training, evaluation gates, regression checks, rollout and rollback).
**Asked at:** senior roles at product companies, GCCs, GenAI startups
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 Can fine-tuning inject new facts? Why does it often fail compared with retrieval, and what does the evidence say?
**Asked at:** senior roles at product companies, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 What are the pitfalls of distillation (capacity gap, exposure bias, evaluation, teacher licensing terms), and when does it fail?
**Asked at:** senior roles at product companies, GenAI startups, big tech
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 How do you handle sequential or continual fine-tuning without forgetting (replay, per-task adapters, EWC-style regularisation, merging)?
**Asked at:** research-leaning teams, big tech, GenAI startups
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 What is rejection-sampling fine-tuning or self-improvement (RFT, STaR-style): how do you bootstrap SFT data from a model's own verified samples, and what can go wrong?
**Asked at:** research-leaning teams, GenAI startups, big tech
<!-- ANSWER_PENDING -->

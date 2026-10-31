QS = [
(3,'🟢',"Prompting vs RAG vs fine-tuning: what is your decision framework, and in what order do you try the adaptation methods?","all types; service-company, GCC and product GenAI loops"),
(3,'🟢',"What is supervised fine-tuning (instruction tuning)? What does it teach a model, what does it not teach, and what is the training loss?","all types"),
(3,'🟢',"What is LoRA and how does it work? Why is it parameter-efficient, and what stays frozen?","all types; product, GenAI startups, GCC"),
(3,'🟡',"How do you choose LoRA's rank, alpha and dropout? What does the alpha/r scaling do?","product, GenAI startups, GCC"),
(3,'🟡',"Which modules should LoRA target (query/value only vs all linear layers including the MLP), and why?","product, GenAI startups"),
(3,'🟡',"What is QLoRA? Explain NF4, double quantization and paged optimizers, and where precision matters during training.","product, GenAI startups, GCC"),
(3,'🟡',"Memory maths: how much GPU memory does full fine-tuning, LoRA and QLoRA need for a 7B or 13B model, and can you fine-tune a 13B model on one 40 GB GPU?","product, GenAI startups, big tech"),
(3,'🟡',"What is catastrophic forgetting in fine-tuning? How do you detect it, and how do you mitigate it?","all types; product, GenAI startups"),
(3,'🟡',"How do you evaluate a fine-tuned model before shipping (task metric, general-capability regression, human or LLM judging)?","product, GenAI startups, GCC"),
(3,'🟡',"How much data do you need for SFT, and what matters more, quality or quantity? How do you build and clean the dataset?","product, GenAI startups, GCC"),
(3,'🟡',"In SFT, why do we mask prompt tokens from the loss (train on completions or assistant turns only)? How do label shifting, the ignore index and packing interact?","product, GenAI startups, fine-tuning teams"),
(3,'🟡',"Why do chat templates and the EOS token matter in fine-tuning? What breaks when training and inference templates differ?","product, GenAI startups, fine-tuning teams"),
(3,'🟡',"How do you merge a LoRA adapter into the base model? Why does a merged LoRA add no latency, why can't a QLoRA adapter be merged directly, and when would you keep adapters separate?","product, GenAI startups, inference/platform teams"),
(3,'🟡',"Code: implement a LoRA linear layer from scratch in PyTorch (frozen weight, A and B initialisation, alpha/r scaling, merge) and verify it against W + BA.","product, big tech, live-coding rounds"),
(3,'🟡',"Code: implement the SFT loss with prompt masking in PyTorch (shifted labels, ignore index) and check it against F.cross_entropy.","product, big tech, live-coding rounds"),
(2,'🟡',"Full fine-tuning vs parameter-efficient fine-tuning: when is full fine-tuning justified, and how do learning rates differ?","product, GenAI startups, big tech"),
(2,'🟡',"What hyperparameters matter in SFT (learning rate, epochs, batch size, warmup, scheduler, max length), and how do you recognise overfitting?","product, GenAI startups, fine-tuning teams"),
(2,'🟡',"Compare PEFT methods: adapters, prefix tuning, prompt tuning, IA3 and LoRA. When would you use each?","product, GenAI startups, research-leaning teams"),
(2,'🟡',"What do LoRA variants change (rsLoRA, DoRA, LoRA+, LoftQ initialisation)? When are they worth trying?","GenAI startups, research-leaning teams, fine-tuning teams"),
(2,'🟡',"Does a higher LoRA rank always help? What limits capacity, and how do you decide when LoRA is not enough?","product, GenAI startups, research-leaning teams"),
(2,'🟡',"How do you create instruction data: human-written, synthetic from a stronger model, self-instruct? What are the quality and licensing risks?","product, GenAI startups, GCC"),
(2,'🟡',"What is knowledge distillation? Explain teacher and student, soft targets, temperature and the combined KL plus cross-entropy loss.","all types; product, GCC"),
(2,'🟡',"How does distillation work for LLMs: logit-level (white-box) vs sequence-level or response distillation (black-box)? Does the student need the teacher's tokenizer?","product, GenAI startups, big tech"),
(2,'🟡',"Forward vs reverse KL in LLM distillation (MiniLLM): what is the difference, and what does on-policy distillation fix?","research-leaning teams, big tech, GenAI startups"),
(2,'🟡',"When do you fine-tune a small model instead of calling a large API model? Work through a cost, latency, privacy and quality break-even.","product, GCC, API-heavy teams"),
(2,'🟡',"For classification or extraction, would you fine-tune an LLM with SFT, add a classification head, or use a small encoder? How do you choose?","product, GCC, applied ML teams"),
(2,'🟡',"How do you mix tasks and general data in SFT (data mixtures, ordering, replay of general data), and what goes wrong with a narrow dataset?","product, GenAI startups, fine-tuning teams"),
(2,'🟡',"How do you fine-tune for structured output or tool calling (dataset format, loss on tool calls, evaluation)? How does it relate to prompting for the same?","product, GenAI startups, agent-building teams"),
(2,'🟡',"Continued pretraining vs SFT for a new domain or language: when do you need continued pretraining before SFT?","product, GenAI startups, India product companies"),
(2,'🟡',"What does SFT overfitting look like (train vs validation loss, memorisation, narrow style), and what are your defences (early stopping, fewer epochs, regularisation, data)?","product, GenAI startups, fine-tuning teams"),
(2,'🟡',"What training-efficiency settings matter in practice (sequence packing, padding-free batches, gradient checkpointing, gradient accumulation, bf16), and what do they cost?","product, GenAI startups, fine-tuning teams"),
(2,'🟡',"How do you serve fine-tuned models: merged weights vs multi-LoRA serving, adapter swapping and versioning?","product, platform teams, inference teams"),
(2,'🟡',"Hosted fine-tuning APIs vs self-hosted fine-tuning: what are the trade-offs in control, data privacy, cost and lock-in?","product, GCC, regulated-industry teams"),
(2,'🟡',"How do you keep PII and benchmark contamination out of fine-tuning data (deduplication, held-out sets, filtering)?","product, GCC, regulated-industry teams"),
(2,'🟡',"A fine-tune did not learn or got worse. Walk through your debugging checklist (template, masking, learning rate, data, evaluation).","product, GenAI startups, fine-tuning teams"),
(2,'🟡',"Should you fine-tune a base or an instruct/chat checkpoint? What are the trade-offs?","product, GenAI startups, fine-tuning teams"),
(1,'🟡',"AI code review: this LLM-written LoRA/SFT training script has bugs (unshifted or unmasked labels, wrong learning rate, merging in 4-bit, dropout left on at eval, wrong target modules). Find and fix them.","product, big tech, AI-era code-review rounds"),
(1,'🔴',"Why does low-rank adaptation work? Derive the parameter count, the identity initialisation, and the effective scaling of the update.","big tech, research-leaning teams, GenAI startups"),
(1,'🔴',"Chain-of-thought and rationale distillation: how do you distil reasoning from a stronger model, and what are the limits and risks?","big tech, GenAI startups, research-leaning teams"),
(1,'🔴',"What is the superficial alignment hypothesis (LIMA)? What evidence supports it, and what are its critiques and implications for data curation?","research-leaning teams, big tech, GenAI startups"),
(1,'🔴',"How do multi-adapter composition and model merging work (weighted adapters, task arithmetic, TIES-style merging), and what are the risks?","research-leaning teams, GenAI startups, platform teams"),
(1,'🔴',"Design question: plan a fine-tune of a 13B-70B model on limited GPUs (QLoRA, gradient checkpointing, sharding), including how you validate the plan before spending the compute.","senior roles at big tech, product, GenAI startups"),
(1,'🔴',"Design question: build an end-to-end fine-tuning project for a support-ticket extraction task (data, training, evaluation gates, regression checks, rollout and rollback).","senior roles at product companies, GCCs, GenAI startups"),
(1,'🔴',"Can fine-tuning inject new facts? Why does it often fail compared with retrieval, and what does the evidence say?","senior roles at product companies, GenAI startups, research-leaning teams"),
(1,'🔴',"What are the pitfalls of distillation (capacity gap, exposure bias, evaluation, teacher licensing terms), and when does it fail?","senior roles at product companies, GenAI startups, big tech"),
(1,'🔴',"How do you handle sequential or continual fine-tuning without forgetting (replay, per-task adapters, EWC-style regularisation, merging)?","research-leaning teams, big tech, GenAI startups"),
(1,'🔴',"What is rejection-sampling fine-tuning or self-improvement (RFT, STaR-style): how do you bootstrap SFT data from a model's own verified samples, and what can go wrong?","research-leaning teams, GenAI startups, big tech"),
]
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
hdr=f"""# Book 2 — Part 04: Fine-tuning (SFT, LoRA/QLoRA, PEFT, Distillation)

**Topic:** when to fine-tune, SFT and instruction tuning (data, loss masking, chat templates), LoRA and QLoRA (rank, alpha, target modules, memory maths, merging), other PEFT methods and LoRA variants, catastrophic forgetting and evaluation, knowledge distillation (classic, white-box and black-box LLM distillation, forward vs reverse KL), and fine-tuning design and debugging.
**Target:** 45  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-22  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Book 1 only frames fine-tuning basics (B1P09-Q39 full vs adapters vs feature extraction and forgetting; B1P09-Q14 prompting vs RAG vs fine-tuning, depth deferred to Book 2; B1P08-Q39 transfer learning; B1P08-Q55 and B1P09-Q47 distillation basics for serving), so answers here must go deeper and cross-reference rather than copy. Part 2 already covers pretraining vs continued pretraining vs fine-tuning (Q8), extending a tokenizer and model to a new domain (Q36), bf16/fp16 (Q27) and the 16 bytes-per-parameter training memory accounting (Q34); Part 3 covers prompt and tool-calling design. RLHF, DPO and safety belong to Part 5; quantization, serving and merging for deployment to Part 10; evaluation depth (LLM-as-judge, benchmarks) to Part 9; RAG to Parts 6-7. Library details (Hugging Face PEFT and TRL parameter names, defaults) change quickly: answers must use the names from the docs opened on 2026-10-22 and tell the reader to check current docs.

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
open('Book2_GenAI/Book2_GenAI_Part04.md','w',encoding='utf-8',newline='\n').write(''.join(out))
open('scratch/B2P04_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(''.join(f"| B2P04-Q{i} | 4 | {q} |\n" for i,(s,d,q,a) in enumerate(QS,1)))
print(n,c)

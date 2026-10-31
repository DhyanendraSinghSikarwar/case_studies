# Book 2 Part 04 — Sources & research notes (Fine-tuning: SFT, LoRA/QLoRA, PEFT, distillation)

Date: 2026-10-22. Target band per plan.md: Rs 30-80 LPA roles. No source states a salary band, so band fit is NOT verified for any report. WebSearch ran 7 queries (standard mode, US-only); WebFetch opened 8 pages (2 rounds were interrupted by a spend limit and re-run). Stars blend topic frequency across guides with judgement; "Asked at" tags are company types, because search found NO candidate-reported fine-tuning questions (Glassdoor, PracHub and Reddit returned nothing relevant).

## Pages actually OPENED (WebFetch)
| Page | URL | Evidence type | Used for |
|---|---|---|---|
| techinterview.org: What LoRA interviews test, and when not to fine-tune at all | https://www.techinterview.org/post/3233477274/what-lora-interviews-test-when-not-to-fine-tune/ | prep article, no company named | the setup question "fine-tune a 13B model on one A100 40 GB with ~2,000 labelled examples, explain every number incl. rank and alpha"; alpha/r scaling; r = 8-16 for small shifts, 64+ for large domain shifts; q/v-only in the paper vs all linear layers now; QLoRA = NF4 + double quantization + paged optimizers; merge W0 + BA, QLoRA cannot merge into the 4-bit base without dequantizing; memory table (full 100+ GB, LoRA ~30 GB, QLoRA ~10 GB for 13B, secondary figures); catastrophic forgetting debugging question; evaluate on a held-out general set; "fine-tuning teaches form not facts"; trap questions (50 examples means few-shot; citing policies word for word means retrieval). NOTE its own arithmetic is wrong: it says the r=16 adapter on a 4096x4096 matrix is "a bit over a hundredth" of the matrix, but 131,072 / 16,777,216 is about 0.78%. Q1, Q3-Q9, Q13, Q25, Q36, Q44 |
| techinterview.org: Fine-tuning LLMs vs training from scratch | https://www.techinterview.org/post/3233460056/fine-tuning-llms-vs-training-from-scratch-when-and-how/ | prep article; names OpenAI/Anthropic/DeepMind only as examples | adaptation ladder (prompt, few-shot, RAG, LoRA/QLoRA, full fine-tune, continued pretraining), when FT beats prompting/RAG, full-FT memory 3-4x model size, LR 1e-5 to 3e-5 for full FT, LoRA config example (r=16, lora_alpha=32, dropout 0.05, q_proj/v_proj), rough data sizes (secondary), evaluation (task metrics plus MMLU/HellaSwag regression plus human eval), SFT vs RLHF vs DPO, common mistakes. Q1, Q2, Q7, Q9, Q10, Q16, Q25 |
| techinterview.org: ML engineer interview in the post-LLM era | https://www.techinterview.org/post/3233474925/ml-engineer-interview-post-llm-era/ | prep article | 2026 default is prompting unless fine-tuning is specifically needed; when LoRA vs full FT; full FT "rarely"; fine-tuning experience helpful but not mandatory for most applied roles. Q1, Q16 (no distillation content) |
| Hugging Face PEFT: LoRA conceptual guide | https://huggingface.co/docs/peft/main/en/conceptual_guides/lora | library documentation (primary) | W + BA with only A, B trained; A Kaiming-uniform and B zeros (identity at start); scaling lora_alpha/r, use_rslora switches to lora_alpha/sqrt(r); LoraConfig fields (r, target_modules, lora_alpha, bias, use_rslora, modules_to_save, rank_pattern, alpha_pattern); merge_and_unload, merge_adapter, unmerge_adapter, add_weighted_adapter; LoftQ init for quantized bases; lora_dropout and DoRA not described in the guide body. Q3-Q5, Q13, Q14, Q19, Q38, Q41 |
| Hugging Face TRL: SFT Trainer | https://huggingface.co/docs/trl/main/en/sft_trainer | library documentation (primary) | SFT = token-level NLL with one-token shift and ignore index -100; dataset formats (language modeling vs prompt-completion, standard vs conversational); assistant_only_loss (needs a chat template with generation keywords) and completion_only_loss; packing, packing_strategy (bfd, bfd_split, wrapped), padding_free (FlashAttention 2/3); adapter training uses higher LR (about 1e-4) than full FT (default 2e-5); EOS must match the chat template; tool-calling datasets carry tool_calls and a tools column; defaults (max_length 1024, gradient_checkpointing True, bf16). Q2, Q11, Q12, Q14, Q15, Q17, Q28, Q31, Q38 |
| QLoRA paper abstract (arXiv 2305.14314) | https://arxiv.org/abs/2305.14314 | primary paper abstract | 4-bit frozen base, gradients through it into LoRA adapters; NF4 "information theoretically optimal for normally distributed weights", double quantization, paged optimizers; 65B on a single 48 GB GPU; Guanaco 99.3% of ChatGPT on Vicuna benchmark (authors' claim; they also note chatbot benchmarks are not fully trustworthy). Q6, Q7 |
| LoRA paper abstract (arXiv 2106.09685) | https://arxiv.org/abs/2106.09685 | primary paper abstract | 10,000x fewer trainable parameters and 3x less GPU memory vs GPT-3 175B with Adam, no extra inference latency (unlike adapters), on par with or better than full FT on RoBERTa, DeBERTa, GPT-2, GPT-3. Q3, Q13, Q38 |
| MiniLLM paper abstract (arXiv 2306.08543) | https://arxiv.org/abs/2306.08543 | primary paper abstract | reverse KLD instead of forward KLD for generative LMs, on-policy optimisation, students 120M-13B. Q24 |

## Seen via search results only (NOT opened)
| Item | URL | Evidence type | Used for |
|---|---|---|---|
| NVIDIA NeMo PEFT supported-methods docs | https://docs.nvidia.com/nemo-framework/user-guide/25.11/sft_peft/supported_methods.html | vendor docs, snippet | LoRA, DoRA (magnitude plus direction), QLoRA (up to 60% more memory-efficient, 50-200% slower, per the snippet), IA3, adapters, prefix/prompt tuning. Q18, Q19 |
| Third-party PEFT comparison pages (apxml survey, skills sites) | https://apxml.com/courses/introduction-to-llm-fine-tuning/chapter-4-parameter-efficient-fine-tuning-peft/other-peft-methods-survey | low-authority secondary; numbers unverified | Q18 (use as rough guide only) |
| LIMA (arXiv 2305.11206) via explainers | https://ar5iv.labs.arxiv.org/html/2305.11206 | paper, snippets | 1,000 curated examples on a 65B LLaMA, superficial alignment hypothesis, quality and diversity over quantity, human-study win/tie rates (small study). Q10, Q40 |
| Distillation tutorials and papers: Hinton et al. 2015 (arXiv 1503.02531), MiniLLM, distillation survey (arXiv 2402.13116), a 2026 paper on temperature in LLM distillation (arXiv 2606.00306) | https://arxiv.org/pdf/2606.00306 | snippets | soft targets with temperature, KL, weighted CE plus KD loss (alpha commonly 0.5-0.9 in tutorials), T^2 gradient scaling, LLM distillation often omits temperature (tau = 1), logit KD needs a shared vocabulary (snippet cut off, treat as likely), Seq-KD. Q22-Q24, Q39, Q45 |
| Udemy LoRA/QLoRA practice-test listing | https://www.udemy.com/course/llm-fine-tuning-with-lora-qlora-practice-tests/ | product page | topic confirmation only |

## Question provenance
| Tag | Questions |
|---|---|
| prep-guide (opened) | Q1, Q3-Q9, Q13, Q16, Q25, Q36, Q44 |
| library/provider docs or primary paper abstracts (opened) | Q2, Q3, Q6, Q11, Q12, Q14, Q15, Q17, Q19, Q24, Q28, Q31, Q38 |
| snippet / secondary level (topic confirmed, not opened or low authority) | Q10, Q18, Q22, Q23, Q39, Q40, Q45 |
| expert gap-check (no source found; plan topic coverage and judgement) | Q20, Q21, Q26, Q27, Q29, Q30, Q32-Q35, Q37, Q41-Q43, Q46, Q47 |
| candidate-reported | none found |

## AI-era notes
- The 2026 framing is "prompt first, RAG for facts, fine-tune for form, behaviour or cost" (Q1, Q44); the classic scenario is the 13B-on-40GB memory question with a forgetting follow-up (Q7, Q8).
- Library defaults and parameter names (TRL, PEFT) change between versions; answers must cite the docs opened on 2026-10-22 and say to re-check.
- Reviewing LLM-written training scripts is a plausible AI-era round (Q37).

## Not found / blocked (honest)
- No first-hand candidate reports on fine-tuning for any company (Glassdoor, PracHub, Reddit searched). The questions rest on prep articles, library docs and papers; no source states a salary band.
- Distillation has only snippet-level interview-relevance evidence; the distillation questions rely on Hinton and MiniLLM, which must be treated as well-known results, and details beyond the MiniLLM abstract are written from memory.
- Memory figures in the prep articles (30 GB LoRA, 10 GB QLoRA for 13B; 28-56 GB for 7B full FT) are secondary and rough; answers must compute their own numbers and label assumptions.
- Questions Q20, Q21, Q26, Q27, Q29, Q30, Q32-Q35, Q37, Q41-Q43, Q46, Q47 have no direct source; answers must rely on well-known facts and runnable demos, not claims about what interviewers ask.

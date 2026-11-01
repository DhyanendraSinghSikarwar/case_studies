# Book 2 Part 04 review (Wave C)

Date: 2026-10-22. Reviewer: lead session (independent of the four answer agents). Scope: 47 questions, Q1-Q47. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading with a script that refuses any block whose heading or "Asked at" line differs from the frozen list (47 of 47 merged, 0 skipped, no clobbering). Two spend-limit stops interrupted the agents; saved blocks survived and the Q37-Q47 agent was resumed and finished. Lesson: the merge script replaces blocks wholesale, so lead edits must be applied after the final merge (the six Example lines were re-applied once after Q46-Q47 were merged).

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q47 | pass |
| Star order and counts 15 / 21 / 11 | pass (matches header) |
| Required fields (Say this first, Then explain, Example, Follow-ups, Common mistakes) | pass after fix: Q3, Q6, Q8, Q10, Q11, Q12 lacked an Example line; the lead added one to each, using numbers from that answer's own printed output |

## Code
- 37 Python blocks extracted with the proper line-start fence rule and run standalone with `python3 -I` (torch 2.14 CPU, numpy; peft, transformers, bitsandbytes and trl are not installed, so every LoRA, SFT, QLoRA and distillation demo is written from scratch): all exit 0. Slow demos (Q8 about 80 s, Q22 and Q23 about a minute) are noted in the answers and were run single-threaded.
- Printed numbers compared with the text after re-running: Q45 (teacher 0.992 overall and 0.767 on the rare slice; linear student with KD 0.942 and 0.529; hard labels 0.940; MLP-16 student with KD 0.991), Q46 (no protection 0.571, replay 0.891, EWC at lambda 10, 1,000 and 100,000 gives 0.573, 0.636 and 0.789; B stays near 0.94-0.98), Q37 (zero_grad bug grows B's gradient norm 1.578 to 8.277 over 5 steps; double merge gives a 31.8 logit difference; fixed recipe passes its tests), Q38 (rank-3 truncation error 0.018, rank-1 0.663). Earlier agent reports for Q4 (0.78%), Q5 (33.2% attention, 66.8% MLP; 8.4M q,v and 40.0M all-linear parameters at r=16), Q7, Q8, Q11, Q25 (break-even about 987M tokens a month under assumed prices) and Q31 were re-run through exit codes and spot-checked. I did not diff every other block's printed numbers; for those I relied on exit codes and the agents' reports.
- Honest toy results are kept: Q8's tiny learning rate avoids forgetting but also fails to learn the new task; Q22's student gain mixes soft targets with 500 extra teacher-labelled inputs; Q37's bad learning rate spikes but still ends at accuracy 1.00 on the toy; Q45 shows KD giving no gain over hard labels when the student is too small; Q46 shows EWC helping only at very large lambda and trailing replay.

## Facts web-verified this session
| Claim | Result |
|---|---|
| LoRA abstract: 10,000x fewer trainable parameters, 3x less GPU memory vs GPT-3 175B with Adam, no extra inference latency | confirmed (arXiv 2106.09685 abstract opened) |
| QLoRA abstract: frozen 4-bit base, NF4, double quantization, paged optimizers, 65B on one 48 GB GPU, Guanaco 99.3% of ChatGPT on Vicuna benchmark (authors' claim) | confirmed (arXiv 2305.14314 abstract opened) |
| MiniLLM: reverse KLD with on-policy optimisation | confirmed (arXiv 2306.08543 abstract opened) |
| PEFT LoRA guide: W + BA, Kaiming-uniform A and zero B, alpha/r scaling and rsLoRA alpha/sqrt(r), merge_and_unload, add_weighted_adapter, LoftQ | confirmed (Hugging Face page opened) |
| TRL SFT docs: token-level NLL, ignore index -100, assistant_only_loss, completion_only_loss, packing strategies, padding_free needs FlashAttention 2/3, adapters typically use a higher learning rate (about 1e-4) than the 2e-5 default | confirmed (TRL page opened) |
| Gekhman et al. 2024 (EMNLP): new-knowledge examples are learned more slowly and, once learned, linearly increase hallucination; fine-tuning mainly teaches use of existing knowledge | confirmed from the abstract via search; experiment details not verified |
| TIES-Merging (Yadav et al. 2023, NeurIPS): trim, elect sign, disjoint merge to reduce interference | confirmed via search |
| techinterview LoRA article: adapter parameter share arithmetic | the article's "a bit over a hundredth" is wrong; 131,072 / 16,777,216 = 0.78%, which Q4, Q5 and Q38 state |

## Not verified (written from memory, hedged in the text)
Aghajanyan et al. 2020 (intrinsic dimension); Hsieh et al. 2023 (distilling step-by-step); Ilharco et al. 2022 (task arithmetic); Mirzadeh et al. 2020 (teacher assistants); Kirkpatrick et al. 2017 (EWC); Zelikman et al. 2022 (STaR); Yuan et al. 2023 (RFT); LIMA setup and win rates (not quoted); LoRA+ and DoRA/IA3 details; research claims that LoRA learns less and forgets less; Hinton "dark knowledge" and T of about 2-4; that LLM distillation often uses temperature 1 (snippet level); top-k logit storage practice; gradient checkpointing costing about one extra forward pass; the 5-20% replay starting range and the corpus-size hint in Q29 (guesses, flagged); reversal-curse and paraphrase-failure claims; PEFT and TRL behaviours beyond the opened pages (marked check the current docs).

## Evidence limits (unchanged)
- No candidate-reported fine-tuning questions were found for any company; evidence is prep articles, library docs and paper abstracts. No source states a salary band. Stars and "Asked at" tags are indicative.
- Memory and cost figures use assumed accounting or assumed prices, labelled in each answer; the prep article's rough memory figures (about 30 GB LoRA, 10 GB QLoRA for 13B) are secondary and not relied on.
- Library names and defaults (PEFT, TRL) drift; answers cite the docs opened on 2026-10-22 and say to re-check.

## Unresolved
- Part 5 owns RLHF/DPO and safety, Part 10 owns quantization and serving, Part 9 owns evaluation depth (pointers only here).

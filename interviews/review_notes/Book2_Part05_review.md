# Book 2 Part 05 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 41 questions, Q1-Q41. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading with a script that refuses any block whose heading or "Asked at" line differs from the frozen list (41 of 41 merged, 0 skipped, no clobbering, no spend-limit stops this part). Lead edits were applied after the final merge, so nothing was overwritten.

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q41 | pass |
| Star order and counts 12 / 20 / 9 | pass (matches header) |
| Required fields (Say this first, Then explain, Example, Follow-ups, Common mistakes) | pass for all 41 (the Part 4 gap, missing Example lines, was prevented by making Example mandatory in the briefs) |
| Internal cross-references | spot-checked all of them; they point to the right questions ("Part 3 Q38/Q41" are the reliability-stack and support-assistant designs; Part 5 Q41 mentions refer to distributed PPO) |

## Code
- 38 Python blocks extracted with the proper line-start fence rule and run standalone with `python3 -I` (torch 2.14 CPU, numpy; peft, transformers, trl and bitsandbytes are not installed, so every demo is written from scratch and all LLMs are mocked): all exit 0.
- Printed numbers compared with the text after re-running: Q6 (DPO loss equals log 2 = 0.6931 when policy equals reference; 0.6072 after widening the gap; masked tokens change nothing; reversed preference gives 0.7981), Q36 (log Z offset leaves the preference probability at 0.928867 unchanged; trained policy recovers the closed-form pi* to 5.6e-16), Q37 (pass@2 with n=4, c=1 is 0.5; n=8, c=2, k=3 gives 0.642857 from both the formula and brute force; unbiased mean 0.6734 vs naive plug-in 0.5946 against true 0.6723), Q33 (fixed DPO and PPO losses match an independent numpy loop to 10 decimals; DPO gradient -0.15 from autograd and from finite differences), Q31 (kappa 0.3478 matches the hand computation; noisy-label vs clean-label accuracy table). I did not diff every other block's printed numbers; for those I relied on exit codes and the agents' reports.
- Honest toy results are kept: Q23's post-fix ASR (6.9%, CI [3.1%, 11.3%]) still fails an "upper bound at most 10%" gate, used to show why sample size matters; Q34 notes Gaussian noise alone only saturates the true reward and a peak-then-fall needs exploit samples; Q35 shows ROT13 still bypasses the keyword filter; Q41 notes continuous batching cannot beat the longest-response floor; Q15's chosen-log-prob-falls demo showed the opposite, so it was dropped and the claim kept as hedged text.
- One fix by the lead: Q31's code comment said "noise caps reward-model accuracy"; reworded to say symmetric noise caps the measured accuracy more than the true accuracy, matching the answer's corrected framing.

## Facts web-verified this session
| Claim | Result |
|---|---|
| InstructGPT abstract: SFT on demonstrations then RLHF on rankings; 1.3B preferred over 175B GPT-3; truthfulness and toxicity improvements; minimal regressions on public NLP datasets; no mention of an alignment tax | confirmed (arXiv 2203.02155 abstract opened) |
| DPO abstract: no separate reward model, no RL, no sampling during training; closed-form optimal policy via reward reparameterisation; simple classification loss | confirmed (arXiv 2305.18290 abstract opened) |
| Constitutional AI abstract: supervised critique-revise phase, then RL from AI feedback; only human input is the constitution | confirmed (arXiv 2212.08073 abstract opened) |
| NeMo Guardrails (archived docs): self-check rails with prompt plus parser, Colang dialog flows, 23-category content-safety model, jailbreak detection, topic control, AlignScore/Llama Guard/Presidio integrations; retrieval and execution rails not covered | confirmed (page opened) |
| Wei et al. 2023, Jailbroken: two failure modes, competing objectives and mismatched generalisation, with prefix injection and a Base64 example | confirmed via search (NeurIPS 2023, arXiv 2307.02483) |
| Pass@k unbiased estimator 1 - C(n-c,k)/C(n,k) (Chen et al. 2021, arXiv 2107.03374) | formula confirmed from a secondary source and by brute-force in Q37; the original appendix text was cut off in search |
| DPO derivation (closed-form optimum, Z cancels in Bradley-Terry differences) | verified numerically in Q36 |
| Best-of-n KL bound log n - (n-1)/n | verified numerically on three discrete toys in Q34; the citation itself is from memory |

## Not verified (written from memory or snippet level, hedged in the text)
Gao et al. over-optimisation, Singhal et al. length bias (the wiki figure of 70-90% is explicitly not quoted), Sharma et al. sycophancy and the 2024 DPO over-optimisation paper (snippet level); GRPO details beyond reported explainers (DeepSeekMath not opened); Llama Guard details and the S1-S14 taxonomy (search snippets only); XSTest counts and FalseReject figures (reported); garak and jailbreak families (reported from blogs); IPO, KTO, ORPO and SimPO descriptions (from memory); PPO-ptx; conservative-DPO idea; process reward models; RewardBench; research ideas in Q40 (debate, recursive reward modelling, weak-to-strong generalisation, process supervision); the claim that open-source fine-tunes commonly use DPO while frontier labs use PPO (a claim in one prep article, stated as unverified). No OWASP ids are quoted because the OWASP pages did not list entries.

## Evidence limits (unchanged)
- No candidate-reported alignment questions were found for any company; the evidence is two techinterview guides (one lists hiring companies but attributes no question to any), primary abstracts and vendor docs. A Scale AI guide is mentioned only as a guide. No source states a salary band for this plan's roles.
- All hardware, latency, cost and memory numbers are assumed and labelled; all demos are synthetic or mock.
- Safety demos use only harmless placeholder strings.

## Unresolved
- Prompt-injection depth and monitoring belong to Part 11, evaluation depth to Part 9, agent safety to Part 8, quantization and serving to Part 10 (pointers only here).

# Book 2 Part 02 review (Wave C)

Date: 2026-10-21. Reviewer: lead session (independent of the four answer agents). Scope: 44 questions, Q1-Q44. Target band per plan.md: Rs 30-80 LPA.

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q44 | pass after fix (see below) |
| Star order, counts 13 / 21 / 10 | pass (matches header) |
| Required fields (Say this first, Then explain, Example, Follow-ups, Common mistakes) | pass |

## Defect found and fixed
- The Q29 heading line was lost to a concurrent edit (a parallel agent's Edit replaced it); the Q29 "Asked at" line and answer survived but were glued to the end of Q28, leaving 43 headings. Restored the exact heading from the frozen Wave A text (commit 7b61f07). Q1-Q44 contents otherwise unchanged. Lesson: parallel agents editing one file can clobber boundary lines; the scripted heading check caught it.

## Code
- 40 Python blocks extracted from the file and run standalone with `python3 -I` (torch 2.14 CPU, numpy 2.5): all exit 0. Q14 and Q18 have no runnable block in the file (Q14's calculation is inline; Q18's example is marked not executed). Pseudocode and fragments are labelled `not executed`.
- Printed numbers compared with the text: Q3 (shift check vs F.cross_entropy), Q7 (uniform-model perplexity = V; bits-per-byte example with two hypothetical tokenizers, labelled illustrative), Q11 (N = 28.9B, D = 577B tokens, 6ND = 1.00e23; ratio sensitivity table), Q12 (both counting conventions of 'abababa'), Q33 (8.4e22 FLOPs; 58,982 GPU-hours and $117,964 at 40% MFU on assumed H100-class peak and price, text rounds to 59k / about $120k), Q34 (16 B/param = 112 GB; ZeRO-1/2/3 per-GPU 38.5/26.25/14.0 GB). All match. Not every other block's printed numbers were individually diffed; for those I relied on exit codes and the agents' reports.
- Q5 token-count ratio: the agent used the usual rule of thumb (0.75 words per token, 1,000 words ~ 1,300 tokens) and noted my sources note had it backwards ("1,000 words ~ 750 tokens" from a fetch summary). Sources note corrected.

## Facts web-verified this session
| Claim | Result |
|---|---|
| Chinchilla 70B / 1.4T tokens vs Gopher 280B / ~300B tokens; same training compute; MMLU 67.5 | confirmed (Chinchilla paper and DeepMind blog, via search; Analytics Vidhya page opened earlier) |
| Muennighoff et al. 2023: up to 4 epochs of repeated data cost negligible loss vs unique data | confirmed (NeurIPS 2023 abstract, via search); quoted as approximate in the answer |
| OpenAI-style frequency/presence penalty formulas | confirmed via vLLM's documented implementation of the OpenAI definition (OpenAI's own docs page not retrieved) |
| Hugging Face repetition_penalty: divide positive, multiply negative logits; prompt tokens included by default | confirmed from HF code (divide/multiply); the prompt-inclusion detail is a practitioner claim, text says to check the library |
| Llama 3 8B ~15T tokens (so ~1,900 tokens/param) | consistent with the search-result summary seen earlier; arithmetic shown in Q32 |
| 6ND ~ 2ND forward + 4ND backward | standard; Q8/Q11/Q33 present it as an approximation; the Chinchilla explainer page does not state it |

## Not verified (written from memory, hedged in the text)
Kaplan et al. exponents (about 0.076, 0.095, 0.050): search returned the paper but not the numbers; the Kaplan "model size should grow faster than data" reading; AdamW typical settings (beta2 0.95, weight decay 0.1, warmup 1-10%, eps range) are community practice, not universal; McCandlish gradient-noise-scale work (named only as such); the 13-gram decontamination heuristic; H100 peak 989e12 and 30-55% MFU range (assumptions, labelled); ByT5 / Byte Latent Transformer descriptions; contrastive decoding, DoLa and self-consistency mechanisms; SentencePiece byte-fallback token format; glitch-token detection heuristics (labelled heuristics); provider finish-reason names; the claim that refits land in the teens-to-twenties tokens per parameter (replication paper seen only as a snippet); test-time compute beating larger models on some tasks.

## Evidence limits (unchanged)
- Only Q12 (BPE coding) has candidate-reported evidence (Glean SWE onsite and technical-screen reports and a Perplexity online-assessment listing; seen as search snippets, not opened). Most other questions are prep-guide level or expert gap-check; no first-hand Indian-company reports were found; no source states a salary band.
- Stars and "Asked at" tags are indicative, not verified quotes.
- Q23 logprob/calibration and several pretraining questions overlap Book 1 topics by design; the answers cross-reference Book 1 (B1P08-Q14/Q16/Q40, B1P09-Q18/Q27/Q44, B1P01-Q34, B1P03-Q44) and go deeper.

## Unresolved
- Part 10 topics (speculative decoding, PagedAttention, quantization) and Part 3 constrained decoding only pointed to.
- Q44 refers to the determinism question without a number in one place (agent report); left as is, low risk.

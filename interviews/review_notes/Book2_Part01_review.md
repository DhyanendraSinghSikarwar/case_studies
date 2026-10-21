# Book 2 Part 01 review (Wave C)

Date: 2026-10-21. Reviewer: lead session (independent of the four answer agents). Scope: 47 questions, Q1-Q47. Target band per plan.md: Rs 30-80 LPA.

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q47 | pass |
| Star order 3 -> 2 -> 1, counts 15 / 20 / 12 | pass (matches header) |
| Required fields (Say this first, Then explain, Example, Follow-ups, Common mistakes) | pass after fix (Q41 lacked an Example line, added) |
| Q1-Q36 unchanged by the Q37-Q47 agent's whole-file rewrite (compared with commit 012eb5d) | pass, no lost edits |

## Code
- 37 Python blocks extracted from the file and run standalone with `python3 -I` (torch 2.14 CPU, numpy). 36 exit 0.
- Q46 block is pseudocode (placeholders MASK, model); labelled `# not executed: pseudocode` in the block and in the text.
- Q41: the fixed-attention block relied on variables from earlier code; made standalone (seed, shapes, weights). It now prints 2.4e-07, matching the text.
- Printed numbers compared with the text: Q13 (1.3e-07), Q15 (6,738,415,616 and 8,030,261,248 params; KV 64 and 16 GiB), Q33 (576 elements/token/layer, 57x vs MHA, 3.6x vs GQA-8, 2.25), Q35 (tokens equal, max diff 1.79e-07, K cache shape (2,4,26,8)), Q41, Q42 (scores identical across absolute positions per offset), Q43. One mismatch fixed: Q43 comment quoted 1.12e-14 / 1.11e-14, a real run prints 1.68e-14 / 2.04e-14; text corrected. I did NOT diff every printed number in the other blocks; I relied on the agents' reports plus exit codes for those.
- Machine-specific timings (Q20 LayerNorm vs RMSNorm on CPU, no speed-up observed) are labelled as such.

## Facts web-verified this session (pages actually opened or search results seen)
| Claim | Result |
|---|---|
| DeepSeek-V2: 60 layers, 128 heads, head dim 128, d_c = 512, decoupled RoPE dim 64; MLA cache equals GQA with 2.25 groups | confirmed from the paper text (arXiv 2405.04434, PDF extracted) |
| Mixtral 8x7B 46.7B total / 12.9B active, top-2 of 8 | confirmed (Mistral announcement, via search) |
| StreamingLLM: 4 initial sink tokens suffice | confirmed (arXiv 2309.17453, via search) |
| Gemma 2 logit soft-cap 50 (attention) and 30 (final) | confirmed (Gemma 2 report, via search) |
| LLaVA-1.5: 576 visual tokens (336/14 = 24 per side) | consistent (secondary source plus arithmetic) |
| DeepSeek-V3: 2nd-token MTP acceptance 85-90%; auxiliary-loss-free balancing | confirmed in the technical report; a later analysis paper says 80-90%, and the report still uses a very small sequence-wise auxiliary loss |

## Not verified (written from memory, hedged in the text)
Liu et al. 2023 lost-in-the-middle details, RMSNorm/SwiGLU claims, position interpolation / NTK-aware / YaRN descriptions, Olsson et al. 2022 induction heads, Voita et al. 2019, Jamba hybrid, LLaDA (Nie et al. 2025), Inception Mercury, Gemini Diffusion, Q34 DeepSeek-V3 balancing wording. Treat as plausible but unchecked.

## Evidence limits (unchanged)
- No first-hand Indian-company report for these topics was found; no source states a salary band.
- Q13/Q35 coding tasks are backed by one Amazon onsite report (aggregator, Jan 2026, level not stated) and NVIDIA Glassdoor snippets (not opened, 403).
- Stars and "Asked at" tags are indicative (blend of prep-guide frequency and judgement), not verified quotes.
- Hardware numbers in Q7/Q32 are illustrative (A100/H100-class figures), labelled so.

## Unresolved
- Part-10 topics (PagedAttention, speculative decoding, quantization) only pointed to.
- Header "Target: 45 / Actual: 47" kept; star counts verified.

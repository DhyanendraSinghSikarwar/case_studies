# Book 2 Part 10 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 49 questions, Q1-Q49. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (49 of 49 merged, 0 skipped, 0 pending). Header status updated after the merge.

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q49 | pass |
| Star order and counts 16 / 21 / 12 | pass (matches header) |
| Required fields incl. Example, Output (my run) | pass |
| Salary / LPA / dollar-price text | none |

## Code
49 Python blocks extracted with the line-start fence rule and run standalone with `python3 -I`: all exit 0. All demos are toy CPU simulations (numpy or stdlib); GPU numbers are assumed A100-class values and labelled assumed. Checked against closed forms or brute force: sign test, speculative-sampling output distribution and acceptance (simulated 0.8497 vs 0.8500; tokens per round 2.770 vs 2.773; (1-a^(g+1))/(1-a) check), KV sizes (0.5 MiB/token MHA 7B, 128 KiB 8B GQA), cost per request loop, percentile checks, all 256 FP8 codes decoded, SmoothQuant rewrite exactness, multi-LoRA batched vs merged (1.8e-14), causal attention FLOPs, checkpoint-interval closed form vs Monte Carlo, Little's law (42.6 vs 42.7), leak time to exhaustion. Honest weak results kept: sticky routing barely raised hit rate (77 to 81%), disaggregation did not raise throughput (consistent with the vLLM docs) and helps goodput only under a max-gap SLO, chunked prefill worse on TTFT in a long-tail toy, admission reserve cut preemptions without improving p99, per-head FP8 scales not uniformly better, cascade scorer optimism flagged, queue share not discriminating in a triage toy.

## Facts verified from sources (opened by the Wave A agent)
Abstracts of vLLM/PagedAttention, Orca, both speculative-decoding papers, Medusa, EAGLE, FlashAttention, AWQ, GPTQ, LLM.int8, SmoothQuant, FP8 formats, SARATHI, Sarathi-Serve, DistServe, Mooncake, SGLang, Punica, S-LoRA; vLLM docs (prefix caching, quantization, disaggregated prefill, multi-LoRA, metrics, benchmarking); TGI docs (maintenance-mode banner, v3 post); TensorRT-LLM overview; llama.cpp repo. All speedups appear only as authors' or vendor claims in their setup.

## Not verified (hedged in the text)
GPU specs (assumed), Llama configs, OCP E4M3 NaN details, Medusa-2 backbone fine-tuning, GGUF block layouts and K-quants, nvidia-smi utilisation definition, jump-forward decoding, provider batch-API discounts, vLLM engine defaults and flags (hedged "as of docs read 2026-10-24, check live docs"), cache-aware routing in other stacks. Not used: AdaServe 74%, guide numbers (10-20x, 40-70%, 1-3%, 5-10 min cold start, 5 GB KV), GPU prices, dollar-per-token prices, leaderboard numbers.

## Evidence limits (unchanged)
No candidate-reported serving questions were found; evidence is papers, vendor docs and prep guides. No source states a salary band. Stars and "Asked at" tags are indicative.

# Book 2 Part 09 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 46 questions, Q1-Q46. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (46 of 46 merged, 0 skipped, 0 pending). Header status updated after the merge.

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q46 | pass |
| Star order and counts 15 / 21 / 10 | pass (matches header) |
| Required fields incl. Example, Output (my run) | pass |
| Salary / LPA text | none |

## Code
46 Python blocks extracted with the line-start fence rule and run standalone with `python3 -I`: all exit 0 (agents also confirmed each pasted output equals a fresh run). Statistics code was checked against brute force or closed forms: pass@k estimator vs subset enumeration (max diff 1.1e-16), exact McNemar vs enumeration, Bradley-Terry vs the two-model closed form, exact sign test, Clopper-Pearson vs 1-0.05^(1/n), Wilson bound, sample-size formulas by simulation, kappa vs hand examples. Honest weak results kept (judge correction making an estimate worse, bootstrap CI vs exact test disagreement at few discordant pairs, 8-gram detector missing paraphrased leaks, cascade below strong-judge accuracy, kappa missing drift in a toy).

## Facts verified from sources
Codex estimator formula and the 1-(1-p_hat)^k underestimation (paper text read via PDF); MT-Bench figures (65.0% consistency, 10%/25% self-enhancement with the authors' caveat, 85% vs 81% agreement, 58 labellers, 80 questions), reported identically by two independent agents (one from PDF text, one from an arXiv HTML summary; Q19 says to verify against the paper); Ragas context recall formula; abstracts for SWE-bench, MMLU-Pro, PoLL, G-Eval, SelfCheckGPT, HarmBench (18 methods, 33 targets), contamination, LiveCodeBench, AlpacaEval-LC and Miller's error-bars paper (authors' claims, labelled).

## Not verified (hedged in the text)
OpenAI Evals shutdown dates, Arena rebrand date, leaderboard and SWE-bench Verified numbers, self-recognition percentages and HarmBench classifier details (none quoted); S1/S2 tie handling in MT-Bench agreement; Landis-Koch bands; temperature-0 non-determinism specifics; sequential-testing and SRM alert levels; Arena style-control method; tool-landscape descriptions in Q35; BCa vs percentile bootstrap; provider snapshot and deprecation practices.

## Evidence limits (unchanged)
No candidate-reported evaluation questions were found; evidence is papers, vendor and practitioner posts, and prep guides. No source states a salary band. Stars and "Asked at" tags are indicative.

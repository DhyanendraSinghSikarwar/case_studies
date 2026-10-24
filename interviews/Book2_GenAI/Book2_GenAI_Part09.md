# Book 2 — Part 09: LLM Evaluation (eval sets, metrics, LLM-as-judge, RAGAS, hallucination, benchmarks, statistics, CI, safety, online)

**Topic:** how to evaluate LLM applications: eval-set and golden-set design, offline vs online evaluation, reference-based metrics and their limits, pass@k and perplexity, LLM-as-a-judge (biases, pairwise vs pointwise, calibration, rubrics), RAGAS-style RAG metrics, hallucination and groundedness, public benchmarks (MMLU, HumanEval, SWE-bench, MT-Bench, Chatbot Arena), contamination and saturation, human evaluation and agreement, statistical rigour (confidence intervals, paired tests, sample size, run variance), regression testing and CI gates, safety and red-team evaluation, A/B tests and online monitoring, tooling, error analysis, cost, coding questions (pass@k, Elo, bootstrap, kappa, a mini harness) and senior design questions.
**Target:** 45  |  **Actual:** 46 (⭐⭐⭐ 15, ⭐⭐ 21, ⭐ 10)  |  **Date:** 2026-10-24  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: earlier parts cover the basics, and answers here must go deeper and cross-reference, not repeat. Part 2 covers the definition of perplexity (Q7), decontamination of pretraining corpora (Q30) and emergent abilities vs metrics (Q40); Part 3 covers prompt evaluation and LLM-judge limits at prompt level (Q32) and tool-use evaluation (Q44); Part 4 covers evaluating a fine-tuned model before shipping (Q9) and benchmark contamination in fine-tuning data (Q34); Part 5 covers evaluating aligned models and win rates (Q10), red-team basics (Q23), guardrail measurement (Q29) and reward-model evaluation (Q32); Part 6 covers retrieval metrics, golden sets for RAG, and generation metrics at overview level (Q10, Q39, Q40); Part 7 covers component ablations and GraphRAG-vs-vector judging (Q14, Q46); Part 8 covers agent evaluation, agent regression testing and non-deterministic agent suites (Q14, Q39, Q51). Part 9 owns the general evaluation method: judges, statistics, benchmarks, harness code and eval strategy. Agent-specific evaluation points to Part 8, monitoring and tracing depth to Part 11, and cost and latency of serving to Part 10. Tool landscapes and benchmark leaderboards change quickly (provider eval products, Arena naming and methodology, SWE-bench variants): answers must hedge unverified current-state claims and tell the reader to check the live docs. Headline numbers (judge agreement above 80%, Codex pass@k, SWE-bench scores, MMLU-Pro drops, PoLL cost claims) are authors' reported results in their stated setting and must be labelled as such.

Evidence limits: no candidate-reported evaluation questions were found (Glassdoor, Reddit and Blind returned nothing relevant); the "Asked at" tags are company types, and where an interview-prep guide or a listing describes a prompt this is marked as a guide (not a candidate report). Star ratings blend topic frequency across guides with judgement. See research_notes/Book2_Part09_sources.md for which pages were opened.

---

### Q1 ⭐⭐⭐ 🟢 How do you evaluate an LLM application end to end? Explain why it differs from testing ordinary software, model vs system evaluation, and how offline and online evaluation fit together.
**Asked at:** all types; GenAI-engineer and evaluation-focused rounds; interview-prep guides list this as an opening question (guides, not candidate reports)
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟡 How do you build a golden evaluation set from scratch (real queries, coverage of cases, labels, size, versioning, and keeping it free of training or prompt leakage)?
**Asked at:** all types; product, GenAI startups, GCC; a Dataford prompt framed at Invoca (seen in search only) asks for a golden-dataset evaluation system (not verified as a candidate report)
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Reference-based metrics for generated text: what do exact match, token F1, BLEU, ROUGE and BERTScore measure, when does each fit, and why do they fail for open-ended LLM output?
**Asked at:** all types; interview-prep guides list BLEU/ROUGE limits as a junior-level check (guides, not candidate reports)
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 What is LLM-as-a-judge? Explain pointwise, pairwise and reference-based judging, when to use each, and the limits of trusting a judge.
**Asked at:** all types; product, GenAI startups, GCC, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 What biases do LLM judges show (position, verbosity, self-preference), how do you measure each in your own setup, and how do you mitigate them?
**Asked at:** all types; product, GenAI startups, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 How do you calibrate and validate an LLM judge against human labels (agreement, Cohen's kappa, true positive and true negative rate, train/dev/test split of labelled examples)?
**Asked at:** product, GenAI startups, GCC, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 How do you write a judge prompt and rubric that works (one criterion per judge, binary or small scales, anchored examples, reasoning before the verdict, output format)?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 RAGAS-style generation metrics in depth: how are faithfulness and answer relevance computed, what do they miss, and why can faithfulness be 0.9 while users still complain?
**Asked at:** product, GenAI startups, GCC; interview-prep guides pose the 0.9-faithfulness-but-complaints scenario (guides, not candidate reports)
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 How do you detect hallucinations and measure groundedness (claim decomposition plus entailment checks, citation verification, sampling-consistency checks, abstention rate), and what are the limits of each?
**Asked at:** all types; product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Public benchmarks (MMLU, HumanEval, SWE-bench, MT-Bench, Chatbot Arena): what does each measure, and why is a benchmark score not a product evaluation?
**Asked at:** all types; interview-prep guides list benchmark knowledge at junior level (guides, not candidate reports)
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Your new prompt scores 82% and the old one 80% on 200 test cases. Is it better? Cover confidence intervals, paired comparison, and how much to trust small differences.
**Asked at:** product, GenAI startups, evaluation-focused rounds, senior roles
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 What is pass@k? Explain the unbiased estimator from the Codex paper, why naive 'best of k' reporting is biased, and how pass@k differs from pass^k (all k succeed).
**Asked at:** product, big tech, code-model and evaluation-focused rounds; an interview guide lists implementing pass@k as a senior-level exercise (a guide, not a candidate report)
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Code: implement the unbiased pass@k estimator (n samples, c correct) from scratch, check it against brute force, and aggregate it over problems.
**Asked at:** product, big tech, live-coding rounds
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 How do you do regression testing and CI gates for prompt or model changes (tiered suites, thresholds, flaky results, blocking vs advisory checks)?
**Asked at:** product, GenAI startups, GCC, platform teams; interview-prep guides describe CI release gates (guides, not candidate reports)
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 How do you do error analysis on an LLM product (read traces, open coding, group into a failure taxonomy, count, prioritise) and turn the findings into evals?
**Asked at:** product, GenAI startups, evaluation-focused rounds, senior roles
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 Context precision and context recall in depth: how are they computed, what do they need (reference answer or labelled chunks), why is precision rank-aware, and how do you read the four combinations of high and low?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 A RAG assistant is wrong a third of the time and you only have logs. How do you separate retrieval failures from generation failures, handle unanswerable questions, and decide what to fix first?
**Asked at:** product, GenAI startups, GCC; an interview-prep guide poses this scenario (a guide, not a candidate report)
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 How do you run pairwise comparisons properly (swap order, ties, win rate with a confidence interval, which judge, when pairwise beats absolute scores)?
**Asked at:** product, GenAI startups, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 What did the MT-Bench and Chatbot Arena paper (Judging LLM-as-a-Judge) report: the biases, the agreement with humans, what MT-Bench is, and what does the agreement claim not show?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 How does Chatbot Arena turn pairwise human votes into a ranking (Elo vs Bradley-Terry, confidence intervals, style control), and what are its blind spots?
**Asked at:** product, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Benchmark contamination and saturation: how do you detect leakage, what do held-out, dynamic or refreshed benchmarks do (LiveCodeBench-style), and how should you read a leaderboard?
**Asked at:** product, GenAI startups, research-leaning teams; see also Part 2 Q30 on decontamination
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 What do code benchmarks measure and miss (HumanEval and MBPP functional tests, SWE-bench and SWE-bench Verified), and how can weak tests or saturation mislead you?
**Asked at:** product, big tech, code-model teams
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Perplexity as an evaluation metric: what does it tell you, why does it fail as a measure of an LLM application's quality, and when is it still useful (see Part 2 Q7 for the definition)?
**Asked at:** all types; GenAI-engineer rounds
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 How do you design a human evaluation (rubrics, annotation guidelines, calibration rounds, adjudication, sampling, cost and throughput)?
**Asked at:** product, GenAI startups, GCC, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Inter-annotator agreement: how do raw agreement, Cohen's kappa, Fleiss' kappa and Krippendorff's alpha differ, what is the kappa paradox, and what do you do when annotators disagree on subjective tasks?
**Asked at:** product, GenAI startups, evaluation-focused rounds; an interview-prep guide cites Fleiss' kappa thresholds (a guide, not a candidate report)
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 How big must an eval set be? Explain sample size and power for detecting a small improvement, and why a few hundred cases may not be enough.
**Asked at:** product, GenAI startups, senior roles, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 How do you handle variance across runs and temperature (repeated trials, seeds, temperature 0 not being fully deterministic, reporting mean and spread)?
**Asked at:** product, GenAI startups, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Which statistical tests suit comparing two LLM systems on the same test set (paired bootstrap, McNemar, paired t-test) and how do you handle many comparisons?
**Asked at:** product, GenAI startups, senior roles, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 How do you run safety and red-team evaluations (attack success rate, curated vs automated attacks such as HarmBench, over-refusal rate, severity weighting, release gates)? See Part 5 Q23 and Q29 for basics.
**Asked at:** product, GCC, regulated-industry teams, security-conscious teams
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 How do you run an A/B test and online monitoring for an LLM feature (primary and guardrail metrics, implicit feedback, sampled production traces scored by a judge, drift)?
**Asked at:** product, GenAI startups, GCC; interview-prep guides list A/B tests and feedback signals (guides, not candidate reports)
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 How do you evaluate long-form generation such as summaries (G-Eval-style scoring, claim-level factuality and coverage checks, human spot checks), and why is it harder than short answers?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you evaluate structured-output, extraction and classification tasks (schema validity, per-field precision and recall, deterministic checks before any judge)?
**Asked at:** product, GenAI startups, GCC
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 How do you control evaluation cost (judge cost, sampling strategy, caching, cheaper judge cascades, a panel of smaller judges) without losing signal?
**Asked at:** product, GenAI startups, GCC, platform teams; interview-prep guides list evaluation cost control (guides, not candidate reports)
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you evaluate fairly across languages and user slices (Hindi and Telugu vs English, per-segment metrics, small-slice noise)?
**Asked at:** product, GCC, India-focused teams; an interview-prep guide poses a Hindi and Telugu RAG gap scenario (a guide, not a candidate report)
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 What eval tooling exists (Ragas, DeepEval, promptfoo, LangSmith, Langfuse, provider eval tools), how do you choose, and when do you write your own harness?
**Asked at:** product, GenAI startups, platform teams
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 Capability evals vs regression evals: how does an eval suite mature over time (graduating cases, saturation, adding harder tasks, eval-driven development)? See Part 8 Q14, Q39 and Q51 for agent evaluation.
**Asked at:** product, GenAI startups, senior roles
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 Code: implement Elo ratings and a Bradley-Terry fit from pairwise battle results, and show why order matters for Elo but not for the Bradley-Terry fit.
**Asked at:** product, big tech, research-leaning teams, live-coding rounds
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 Code: implement a bootstrap confidence interval for accuracy and a paired bootstrap for the difference between two systems.
**Asked at:** product, big tech, evaluation-focused rounds, live-coding rounds
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 Code: implement Cohen's kappa to measure agreement between an LLM judge and a human labeller, with TPR and TNR, and test it on toy labels.
**Asked at:** product, GenAI startups, evaluation-focused rounds, live-coding rounds
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 Code: build a mini evaluation harness (dataset loader, model runner, graders, caching, repeated trials, a report with confidence intervals) with a mocked LLM.
**Asked at:** product, big tech, GenAI startups, live-coding rounds
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🟡 AI code review: this LLM-written evaluation script has bugs (test cases leaked into few-shot examples, naive pass@k, no position swap, mean score with no interval, same model as generator and judge, nonzero temperature with one run). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Offline scores keep rising but user complaints are rising too. Diagnose the gap and say what you change in the eval.
**Asked at:** senior roles; an interview-prep guide poses this scenario (a guide, not a candidate report)
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 The model provider quietly updates a model version and quality drops. How do you detect it, attribute it, and protect against it (version pinning, canary evals, rollback)?
**Asked at:** senior roles, platform teams, product companies, GCCs
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 Design question: an evaluation platform for many teams (datasets, versioned prompts and graders, runs, dashboards, CI integration, human review queues, cost control).
**Asked at:** senior roles at product companies, platform teams, GenAI startups
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 Design question: build an LLM judge you can trust (rubric, human calibration set, bias tests, ensembles, drift monitoring, when to retire it).
**Asked at:** senior roles at product companies, GenAI startups, evaluation-focused rounds
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 Design question: an evaluation strategy for launching a new LLM assistant, including a high-stakes domain (clinical or financial): launch criteria, red team, human review, staged rollout, and answering 'is it ready?'
**Asked at:** senior roles; an interview-prep guide poses launch-readiness and clinical-assistant scenarios (a guide, not a candidate report)
<!-- ANSWER_PENDING -->

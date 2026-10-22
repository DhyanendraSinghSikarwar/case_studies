# Book 2 — Part 05: Alignment (RLHF, DPO, Safety, Guardrails)

**Topic:** the RLHF pipeline (SFT, reward model, PPO, KL penalty), reward hacking, DPO and its variants, Constitutional AI and RLAIF, GRPO and verifiable rewards, preference data and reward-model evaluation, safety training and red teaming, and application-level guardrails (moderation classifiers, guardrail frameworks, jailbreak defence, latency and quality measurement).
**Target:** 35  |  **Actual:** 41 (⭐⭐⭐ 12, ⭐⭐ 20, ⭐ 9)  |  **Date:** 2026-10-22  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 4 owns SFT, LoRA and distillation, including SFT as the first RLHF stage (Q2), the superficial alignment hypothesis (Q40) and rejection-sampling fine-tuning (Q47); Part 3 owns prompt-level injection basics (Q34) and the application guardrail designs for support and refund agents (Q38, Q41); Part 2 owns test-time compute and best-of-n sampling costs (Q43). Cross-reference them rather than repeating. Prompt-injection security depth, monitoring and LLMOps belong to Part 11; evaluation depth (LLM-as-judge, benchmarks) to Part 9; agents and tool safety to Part 8. Book 1 only touches reward hacking in LLM reranking (B1P07-Q43). Alignment facts and framework behaviour change quickly: answers must cite what was opened on 2026-10-22 and hedge the rest. No candidate reports for alignment loops were found; the source for these loops is prep guides plus primary papers.

---

### Q1 ⭐⭐⭐ 🟢 What is RLHF? Walk through the pipeline (SFT, reward model, policy optimisation) and explain why a base LLM needs it.
**Asked at:** all types; post-training and GenAI-engineer loops
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is the KL penalty in RLHF, why is it needed, and what does the beta coefficient trade off?
**Asked at:** all types; post-training loops
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is reward hacking? Give examples (length bias, sycophancy) and the standard mitigations.
**Asked at:** all types; post-training loops
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 DPO vs PPO-based RLHF: how does DPO work, what does it remove, and when would you pick each?
**Asked at:** all types; post-training loops
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 How is a reward model trained? Explain preference pairs, the Bradley-Terry loss and the architecture.
**Asked at:** post-training loops, research-leaning teams
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Code: implement the DPO loss in PyTorch (log-probability ratios against a reference model, beta, implicit rewards) and test it on toy tensors.
**Asked at:** product, big tech, post-training coding rounds
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 How do you collect high-quality preference data (guidelines, annotator agreement, pair sampling, AI feedback)?
**Asked at:** post-training loops, data-platform teams
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 What are the guardrail layers in an LLM application (input rails, output rails, dialog or topic control, retrieval and tool checks)?
**Asked at:** all types; product, GCC, GenAI startups
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Jailbreaks vs prompt injection: what attack families exist and how do you defend in depth?
**Asked at:** all types; product, GCC, security-conscious teams
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 How do you evaluate a post-trained or aligned model (helpfulness, harmlessness, regressions, pairwise human or model judging, win rate)?
**Asked at:** post-training loops, product, evaluation teams
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Your model started refusing benign requests after a safety-training round. What do you investigate and how do you fix it?
**Asked at:** post-training loops, product, safety teams
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Code: implement PPO's clipped surrogate objective and the KL-regularised reward in PyTorch and check it on toy tensors.
**Asked at:** big tech, research-leaning teams, post-training coding rounds
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐ 🟡 PPO inside RLHF: policy, value head, advantages and GAE, clipping, and why four models (policy, reference, reward, value) are in memory.
**Asked at:** post-training loops, research-leaning teams
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟡 What are Constitutional AI and RLAIF? How do the two phases work, and what are the benefits and risks of AI feedback?
**Asked at:** post-training loops, safety teams
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟡 DPO in more detail: the reference model, beta, the implicit reward, data requirements and known failure modes.
**Asked at:** post-training loops, GenAI startups
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 What do IPO, KTO, ORPO and SimPO change relative to DPO, and when would you consider them?
**Asked at:** post-training loops, research-leaning teams
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 How do reward models fail (overfitting, distribution shift, length bias, over-optimisation), and what do ensembles and process reward models offer?
**Asked at:** post-training loops, research-leaning teams
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 What is sycophancy? Why does RLHF encourage it, and how do you measure and reduce it?
**Asked at:** post-training loops, product, safety teams
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 What causes length bias and verbosity in aligned models, and how do you measure and mitigate it?
**Asked at:** post-training loops, evaluation teams
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 What are GRPO and RLVR? How does a group-relative advantage replace the critic, and what are the weaknesses of verifiable rewards?
**Asked at:** post-training loops, GenAI startups, research-leaning teams
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 How are reasoning models post-trained (RL on verifiable tasks, test-time compute), and how does that differ from preference-based RLHF?
**Asked at:** post-training loops, big tech, GenAI startups
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 How do you balance helpfulness and harmlessness in safety training? What is the alignment tax and how do you limit it?
**Asked at:** post-training loops, safety teams, product
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 How do you run a red-team exercise (manual vs automated, coverage, attack success rate, fixing what you find)?
**Asked at:** safety teams, product, GCC
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 How do safety-classifier guardrails (Llama Guard style) work for inputs and outputs: taxonomy, thresholds, latency and limits?
**Asked at:** product, GCC, safety teams
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 What do guardrail frameworks such as NeMo Guardrails provide (self-check rails, dialog flows, third-party integrations), and when would you use a framework instead of custom checks?
**Asked at:** product, GCC, GenAI startups
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Guardrails vs alignment: what does each handle, why do you need both, and what does defence in depth look like?
**Asked at:** all types; product, GCC
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 How do you build output-side guardrails for PII, secrets and toxicity (regex, NER, classifier) and what are the trade-offs?
**Asked at:** product, GCC, regulated-industry teams
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 What do guardrails cost in latency and money, and how do you reduce it (cheap checks first, parallel rails, streaming, caching)?
**Asked at:** product, GCC, platform teams
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 How do you measure guardrail quality (precision and recall per category, thresholds, cost of false positives vs false negatives, evaluation set design)?
**Asked at:** product, GCC, safety teams
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Online vs offline preference optimisation: DPO on a fixed dataset, iterative or online DPO, and PPO. Why does on-policy data matter?
**Asked at:** post-training loops, research-leaning teams
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 How do you handle annotator disagreement and label noise in preference data (inter-annotator agreement, adjudication, noise-robust training)?
**Asked at:** post-training loops, data-platform teams
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you evaluate a reward model itself (held-out preference accuracy, agreement with humans, best-of-n probes)?
**Asked at:** post-training loops, research-leaning teams
<!-- ANSWER_PENDING -->

### Q33 ⭐ 🟡 AI code review: this LLM-written DPO/PPO training snippet has bugs (loss sign, reference model gradients, summed vs averaged log-probabilities, KL direction, missing clipping). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
<!-- ANSWER_PENDING -->

### Q34 ⭐ 🟡 Best-of-n with a reward model vs RL fine-tuning: what are the cost, quality and over-optimisation trade-offs?
**Asked at:** post-training loops, product, GenAI startups
<!-- ANSWER_PENDING -->

### Q35 ⭐ 🟡 Why do jailbreaks work (competing objectives, mismatched generalisation), and what are the main families (role-play, obfuscation, multi-turn, multimodal)?
**Asked at:** safety teams, research-leaning teams, product
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🔴 Derive DPO from the KL-regularised reward-maximisation objective: the optimal policy, the reward reparameterisation and the final loss.
**Asked at:** research-leaning teams, big tech, post-training loops
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🔴 Design question: build the post-training pipeline for a coding model (SFT data, preference data from execution tests, RLVR, evaluation, safety).
**Asked at:** senior roles at big tech, GenAI startups, post-training teams
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🔴 Design question: build a preference-data collection platform with quality control (guidelines, redundancy, adjudication, audits, throughput).
**Asked at:** senior roles at data-platform and post-training teams
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🔴 Design question: guardrail architecture for a customer-facing assistant that can issue refunds (rails, approvals, escalation, logging, red-team gates).
**Asked at:** senior roles at product companies, fintech, GCCs
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🔴 What is scalable oversight, and why does preference-based RLHF struggle on tasks humans cannot easily judge?
**Asked at:** research-leaning teams, big tech, safety teams
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🔴 What are the engineering challenges of distributed PPO for LLMs (generation vs training throughput, four models, staleness), and how do teams address them?
**Asked at:** senior roles at big tech and post-training infrastructure teams
<!-- ANSWER_PENDING -->

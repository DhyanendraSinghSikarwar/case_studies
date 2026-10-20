---

# Case Study 27 — Call analytics, intent frequency and dialler efficiency (Policybazaar) · `cs27_call_analytics_dialler.ipynb`

## D-27-01: Data source — simulated transcript outputs, QA audit and a cluster-randomised dialler test

- Date: 2026-10-17
- Case: 27
- Context / question: What data does the analytics team work with?
- Options considered: public Indic speech corpora (no business intents or dialler logs); simulate outputs.
- Decision: 60k calls (13 intents, 12 weeks), 8k QA-audited calls, 120 agents in 24 teams × 40 days (12 teams randomised to the new dialler).
- Why: Confidential audio and logs; model-agnostic evaluation.
- Assumption checks / evidence: Cashless hospital true rank 8 (documented 7th–8th).
- Impact if wrong / mitigation: Re-run on real labelled samples.

## D-27-02: Synthetic parameters — language-dependent ASR errors; dialler effect sizes

- Date: 2026-10-17
- Case: 27
- Context / question: How accurate is ASR, and how big is the dialler effect?
- Options considered: uniform accuracy; accuracy falling with WER by language.
- Decision: WER Hindi 22%, Hinglish 17%, English 9%; dials +32%, talk share 40% → 60%, callback 260 → 40 min.
- Why: Documented direction; sizes are ours (below the documented 85% efficiency).
- Assumption checks / evidence: Intent accuracy 70%.
- Impact if wrong / mitigation: WER was not disclosed; measure it.

## D-27-03: Intent accuracy by language; rank uncertainty; misclassification correction

- Date: 2026-10-17
- Case: 27
- Context / question: Is the "7th–8th" finding reliable?
- Options considered: raw ranks; bootstrap rank ranges; matrix-inversion correction with a labelled sample.
- Decision: All three; Cochran–Armitage trend on predicted and true counts.
- Why: Product decisions rest on frequency ranks.
- Assumption checks / evidence: Rank 7 (95% range 7–9) vs true 8; predicted share 6.5% vs true 5.6%; correction did not remove the bias.
- Impact if wrong / mitigation: Quote ranges and trends, not levels.

## D-27-04: Compliance flag — ROC/PR at alert budgets; language AUC

- Date: 2026-10-17
- Case: 27
- Context / question: How useful is 100% monitoring?
- Options considered: AUC only; precision/recall at fixed alert budgets vs random listening.
- Decision: Budgets 1–20% with Wilson CIs; random sampling baseline (precision = base rate, recall = budget). The first run mislabelled random recall as base rate × budget; corrected.
- Why: QA capacity is a fixed number of calls.
- Assumption checks / evidence: AUC 0.915; 62% precision and 48% recall at 5%.
- Impact if wrong / mitigation: None.

## D-27-05: Dialler experiment — team-level permutation, Welch, cluster-robust regression, residual ICC

- Date: 2026-10-17
- Case: 27
- Context / question: Did the dialler cause the gain?
- Options considered: agent-day comparison (pseudo-replication); team-level analysis. ICC first estimated without the arm effect (inflated, talk-share 0.80); re-estimated after the arm (0.21).
- Decision: Team means with a 10,000-draw permutation test and Welch t; cluster-robust SEs with day fixed effects; design effect from the residual ICC.
- Why: Teams, not agents, were randomised.
- Assumption checks / evidence: Sales/hour +66% (p < 0.0001); cluster-robust SE 2.2× the naive one.
- Impact if wrong / mitigation: Stepped-wedge designs for smaller effects.

## D-27-06: Callbacks and team-level power

- Date: 2026-10-17
- Case: 27
- Context / question: Customer experience and test size.
- Options considered: agent-day callbacks; team-level outcomes; teams needed with a practical floor of 3 (the formula gave 1 for dials, which is not estimable).
- Decision: Mann–Whitney across teams; teams-per-arm table.
- Why: The unit of randomisation is the team.
- Assumption checks / evidence: Callback 259 → 40 min; sales needs 23 teams per arm for a 10% effect.
- Impact if wrong / mitigation: None.

## D-27-07: ₹ translation

- Date: 2026-10-17
- Case: 27
- Context / question: What is it worth?
- Options considered: efficiency only; margin and QA cost.
- Decision: 400 agents × 26 days; ₹1,800 per sale; ₹35,000 per agent-month; QA ₹400/hour at 5 min per alert.
- Why: Comparable business figures.
- Assumption checks / evidence: ≈ ₹2.6 crore/month (₹2.2–3.1 crore); 31,000 breaches found vs 970.
- Impact if wrong / mitigation: Assumptions are explicit.

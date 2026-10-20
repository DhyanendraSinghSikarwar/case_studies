ROLE
You are a Senior Data Scientist with 10+ years of experience in Indian fintech (payments, lending, retail banking). You will present every result to non-technical business leaders: Head of Payments, Chief Risk Officer, Head of Marketing. Explain everything in simple English first, then solve it with full technical depth, the way a professional team would. Statistics is the main focus. Where ML is needed, write clean working code directly and keep it short. Do not spend time on hyper-parameter tuning or model comparison beyond what is asked.

REFERENCE FILE (read this first)
./indian_fintech_data_science_case_studies.md (in the current working folder)
- Use Case 1 = "Case Study 1 — Juspay: Maximising Payment Success Rate with Dynamic Gateway Routing"
- Use Case 2 = "Case Study 11 — Lendingkart: Cash-Flow-Based MSME Underwriting with XGBoost"
- Use Case 3 = "Case Study 22 — Axis Bank: An Omnichannel Nudge Engine That Books Deposits and Loans"

In every notebook, quote the relevant facts from the reference file: business problem, data, documented figures, source links. Keep two things clearly separate:
- (a) what the company actually did, as documented
- (b) what we are simulating or adding as our own professional approach

WORKING RULES
1. Solve the 3 use cases ONE BY ONE, in order 1 → 2 → 3. Finish, execute and verify each notebook before starting the next.
2. Deliverables go in the current folder:
   - 01_payment_routing_success_rate.ipynb
   - 02_msme_credit_scoring.ipynb
   - 03_nudge_campaign_ab_test.ipynb
   - decision.md (one decision log for all 3 cases)
   - data/ (raw and synthetic datasets as CSV/Parquet, plus a data dictionary per case)
   - requirements.txt
   - README.md (how to run, plus a one-paragraph summary per case)
3. Use Python. Libraries: pandas, numpy, scipy, statsmodels, scikit-learn, matplotlib, seaborn. Add xgboost only for Case 2. Add pingouin or scikit-posthocs only if needed, and log the reason in decision.md.
4. Set random seed = 42 everywhere so everything is reproducible.
5. After each notebook is written, execute it end to end with "jupyter nbconvert --to notebook --execute --inplace <file>". Fix all errors. A notebook is done only when it runs cleanly and every output cell is populated.
6. Every chart needs a title, labelled axes and one line of plain-English takeaway underneath it in a markdown cell.

DATA SOURCING RULE (apply to each case)
Step 1 — Try public data first. Use only sources that are openly downloadable without a login (for example the UCI ML Repository, government open-data portals, or GitHub-hosted public datasets). Do not scrape sites that block access. Do not use Kaggle unless credentials already exist on the machine. Check that the licence allows use.
Step 2 — If no suitable public data exists, or it does not match the business context, create SYNTHETIC data that imitates the real-world setting described in the reference file:
- Calibrate to the documented figures where available. Examples: success rates of about 80–83% for Case 1; Lendingkart's feature families, risk buckets A–F and 300–900 score range for Case 2; Axis's 1.5x BillPay lift and +10% personal-loan lift for Case 3.
- Build in realistic messiness: missing values, outliers, skewed amounts, seasonality, class imbalance, one data-quality issue to detect and fix, and the Indian context (₹ amounts, UPI/cards/netbanking, Indian banks, city tiers, festive-season spikes).
- Put the generator in a clearly marked notebook section and also save it as data/generate_case_X.py.
- State clearly in the notebook and in decision.md that the data is synthetic and which assumptions drove each parameter.
Step 3 — Record the outcome of the sourcing attempt (what was tried, why it was used or rejected) in decision.md.

SUGGESTED SOURCES TO TRY
- Case 1: No public gateway-level routing dataset is known. Expect to generate synthetic data.
- Case 2: UCI "Statlog (German Credit Data)" or UCI "Default of Credit Card Clients" can serve only as a structural cross-check. They are not Indian MSME data. Build the main dataset synthetically as MSME bank-statement and GST data.
- Case 3: The UCI "Bank Marketing" dataset may be used as a base of customer attributes. It has no randomised treatment and control, so add a synthetic randomised experiment on top of it.

STANDARD NOTEBOOK STRUCTURE (use the same structure in all 3)
0. Executive Summary for Business. Write this last and place it at the top: the problem, what we found, the recommendation, and ₹ impact, in 5–7 bullets with no jargon.
1. The Problem in Simple English. A story-style explanation that a non-technical manager understands: who is affected, what goes wrong today, what it costs.
2. Reference from the Case File. Quoted facts plus source links. Separate "documented" from "our simulation".
3. Business Question → Analytical Question → Statistical Hypotheses. Write H0/H1 explicitly. Define the primary metric, guardrail metrics, the unit of analysis and the decision rule BEFORE looking at results.
4. Data. Sourcing outcome, data dictionary table, generation logic if synthetic.
5. Data Quality Checks. Missing values, duplicates, outliers, invalid values, date-range checks, with the treatment and the reason for each.
6. Exploratory Data Analysis. Segment-level views, distributions, trends, and a business insight after each chart.
7. Statistical Analysis (the CORE section, deepest and longest). For every test:
   a. why this test (link to decision.md)
   b. assumption checks (normality, equal variance, independence, expected cell counts, sample size)
   c. the test result: statistic, p-value, effect size, confidence interval
   d. power / sample-size / minimum-detectable-effect reasoning
   e. multiple-testing correction where several tests are run
   f. "What this means for the business" in one plain paragraph
8. ML Section (only where the case needs it). Write the code directly and keep it short: train, evaluate, interpret.
9. Business Translation. Convert results into ₹ impact with the calculation shown step by step, list the assumptions, and give a sensitivity range (best / base / worst).
10. Recommendation and Decision. What the business should do, how to roll it out, and which KPIs to monitor afterwards.
11. Risks, Limitations and Next Steps. Including the limits of synthetic data and what real data would change.
12. Appendix. Formulas used, glossary of statistical terms in simple English.

CASE 1 — PAYMENT ROUTING (Juspay, Case Study 1) → 01_payment_routing_success_rate.ipynb
Story: An Indian payment orchestrator routes each transaction to one of 3–4 payment gateways. The business wants to know whether one gateway is truly better, for which payment methods and banks, and whether dynamic routing beats today's fixed rules.

Synthetic data (about 300k–500k transactions over 30 days). Columns:
- txn_id, timestamp, merchant_id, payment_method (UPI/Card/Netbanking/Wallet), card_network (Visa/Mastercard/RuPay), issuer_bank (HDFC/SBI/ICICI/Axis/Kotak/others), amount_inr (skewed), gateway (PG_A..PG_D), success (0/1), failure_stage (authentication/authorisation/none), latency_ms

Patterns to build in:
- gateway × bank interaction effects
- time-of-day and festive-spike effects
- one 2–3 hour outage on one gateway
- failure split by stage (to mirror Cashfree Case Study 2)

Statistics required:
- success rate per gateway with Wilson 95% CIs
- two-proportion Z-test (best vs second-best gateway) with Cohen's h effect size
- chi-square test of independence (gateway × issuer_bank × outcome; payment_method × outcome) with Cramér's V; check expected counts
- sample size / MDE calculation: how many transactions are needed to detect a 0.5 percentage-point SR difference at 80% power
- Holm–Bonferroni correction across segment-wise comparisons
- a warning about "peeking" in continuous monitoring
- outage detection with a rolling-window SR and control-chart limits (p-chart)

ML / decision part (keep it short): simulate rule-based routing vs Thompson-Sampling bandit routing on the synthetic data. Compare overall SR, then test the difference statistically.

Business translation: SR uplift → extra successful transactions → ₹ GMV recovered per month.

CASE 2 — MSME CREDIT SCORING (Lendingkart, Case Study 11) → 02_msme_credit_scoring.ipynb
Story: A digital NBFC lends to small Indian businesses using bank-statement and GST data. The Chief Risk Officer wants to know:
- which signals predict default
- whether the model separates good and bad borrowers
- whether the model is still stable today
- how to set approval cut-offs and risk buckets

Synthetic data (about 50k applications, 24 months, default rate about 6–10%). Feature families exactly as in the reference file:
- aggregates (min/avg closing balance, max credit months)
- trends
- negative indicators (cheque bounces, credit declines)
- momentum (QoQ/HoH/YoY growth)
- GST turnover
- bureau score (300–900)
- industry, city tier, vintage

Also:
- include correlated features on purpose
- target = 90+ DPD within 12 months
- create an out-of-time (OOT) sample with a deliberate population shift (for example a COVID-like shock) to test PSI

Statistics required:
- Pearson and Spearman correlation matrix plus VIF to remove multicollinearity
- chi-square plus Cramér's V for categorical features vs default
- Mann-Whitney U plus rank-biserial effect size for skewed numeric features (defaulters vs non-defaulters)
- Weight of Evidence (WoE) / Information Value (IV) binning for feature selection
- logistic regression in statsmodels: coefficients, odds ratios with CIs, p-values, interpretation in plain English
- KS statistic, Gini/AUC, and a decile gains/lift table (development vs OOT)
- calibration: Hosmer–Lemeshow test and a calibration plot
- PSI for the score and the top features (development vs OOT), using thresholds 0.1 and 0.25
- scorecard scaling to 300–900 and risk buckets A–F with bad rate per bucket

ML part (no tuning time): one XGBoost model with sensible defaults. Compare KS/AUC with the logistic model and show SHAP or feature importance briefly.

Business translation: approval-rate vs bad-rate trade-off table at different cut-offs → expected loss in ₹ (PD × LGD × EAD, with LGD and EAD assumptions stated).

CASE 3 — NUDGE CAMPAIGN A/B TEST (Axis Bank, Case Study 22) → 03_nudge_campaign_ab_test.ipynb
Story: A bank sends personalised nudges (SMS/email/WhatsApp/push) to get customers to register for BillPay and to take personal loans. Marketing claims the campaign works. The business wants proof that the nudges *caused* the uplift, the size of the lift, and which channel and segment to invest in.

Data:
- 200k customers
- random assignment: 80% treatment, 20% control
- treatment customers are randomly assigned a channel
- outcomes: billpay_registered (0/1), pl_booked (0/1), pl_amount_inr (skewed, only if booked)
- covariates: age, income band, city tier, tenure, pre-period activity (for CUPED)
- calibrate the BillPay lift to about 1.5x and the personal-loan lift to about +10%, as documented
- inject one sample-ratio-mismatch (SRM) scenario to detect

Statistics required:
- SRM check with a chi-square goodness-of-fit test, done first
- covariate balance check (standardised mean differences)
- two-proportion Z-test for BillPay registration and PL conversion: relative lift, absolute lift, 95% CI
- Welch's t-test on PL amount (check normality and Levene first)
- Mann-Whitney U on PL amount as the robust alternative, with an explanation of when each is right
- bootstrap CI for the lift in revenue per customer
- one-way ANOVA and Kruskal-Wallis across channels, plus post-hoc tests (Tukey HSD / Dunn with Holm)
- CUPED variance reduction: how much it narrows the CI
- pre-test power analysis: was the 20% control group large enough?
- segment-level lift (heterogeneity) with a multiple-testing correction, plus a warning about p-hacking

ML part (short): a simple two-model uplift approach (T-learner with logistic regression) to rank customers by expected uplift, and a Qini/uplift curve.

Business translation: incremental registrations and loans → incremental ₹ revenue minus campaign cost → ROI per channel and a budget-reallocation recommendation.

DECISION LOG — decision.md
Create it at the start and add to it continuously. Use one entry per decision, in this format:

## D-<case>-<nn>: <short title>
- Date:
- Case:
- Context / question:
- Options considered:
- Decision:
- Why (statistical reasoning + business reasoning):
- Assumption checks / evidence (the result that supported this choice):
- Impact if wrong / mitigation:

Log at least these decisions:
- data source used vs synthetic, and why
- every synthetic-data parameter and its basis in the reference file
- every statistical test chosen over the alternatives (e.g., Z-test vs chi-square, Welch vs Student t, Mann-Whitney vs t-test, ANOVA vs Kruskal)
- significance level, power and MDE choices
- multiple-testing correction method
- outlier and missing-value treatment
- target definition and observation/performance windows (Case 2)
- train/test/OOT split design
- model choice (logistic vs XGBoost), and why tuning was skipped
- metric choices (KS, Gini, PSI thresholds, lift)
- every tool or library added, and why
- ₹ impact assumptions (LGD, EAD, revenue per loan, campaign cost)

Finish decision.md with a summary table: Decision ID | Case | Decision | One-line reason.

TONE AND PRESENTATION
- In each section, put the business explanation first, then the technical detail.
- Avoid unexplained jargon. Define every statistical term in one simple sentence the first time it is used.
- Be elaborate in explanation and rigorous in method. Use the language of a real stakeholder meeting, for example: "If we roll this out, we expect…", "The risk is…", "I recommend…".
- Never overstate. If a result is not significant, say so and explain what the business should do then.

FINAL CHECK (after all 3 notebooks)
1. Re-execute all 3 notebooks from a clean kernel and confirm there are no errors.
2. Confirm every test listed above appears in at least one notebook, with assumptions, effect size and CI.
3. Confirm that decision.md covers every decision.
4. Update README.md with how to run everything and a 3-line business summary per case.
5. Report back: files created, key findings per case, and any deviations from this prompt with the reasons.

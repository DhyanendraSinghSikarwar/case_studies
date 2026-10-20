R = {}
R["«EXEC»"] = """*(Synthetic data built on MobiKwik's documented MobiScore design; MobiKwik disclosed no metrics. Written after the analysis.)*

- **The question:** who should get a BNPL line from wallet behaviour alone, and what limit maximises profit?
- **The behaviour score works.** Trained on one cohort and tested on another, it reaches **AUC 0.71** (KS 0.32). Bad rates rise steadily from **2.0% in the safest fifth to 15.6% in the riskiest**. The strongest signals are low-balance days, irregular last-minute top-ups and a low share of bills paid through the wallet.
- **Engagement signals are collections signals.** Being reachable barely changes default risk (odds ratio 0.88), but it **triples the odds of being cured** once a customer is 30+ days late (OR 2.99; cure 47% vs 23%). That is exactly why the documented score includes "contactability" and "responsiveness".
- **Past data gives the wrong answer about limits.** In the historical book, higher limits *look* safer (odds of default −11% per +₹1,000) because the old rule gave big limits to good customers. The **randomised limit test** shows the truth: each +₹1,000 of limit **raises default odds by 47%**, more for risky customers (+63% in the riskiest band, +16% in the safest; heterogeneity p ≈ 3e-18).
- **Profit by limit:**
  - **Large limits lose money for most customers:** ₹5,000 for everyone loses ₹145 per user in 6 months.
  - **Old-rule tiers are not optimal:** "score-tiered" limits (₹5k down to ₹1k) earn less than giving everyone ₹1,000.
  - **The profit-optimal policy** (₹5k for the safest fifth, ₹2k for the next, ₹1k for the rest) earns **₹30.1 per user vs ₹27.6 for uniform ₹1,000**. The gain is small and **not yet statistically certain** (+₹2.5, CI −₹1.4 to +₹6.1).
- **₹ impact (10 lakh pre-approved users per 6 months):**
  - The profit-optimal policy earns ≈ ₹3.0 crore, vs ₹2.3 crore under the old-rule tiers.
  - Uniform ₹5k would *lose* ≈ ₹14.5 crore.
  - The biggest money is in **avoiding high limits for risky users**, not in fine-tuning.
- **I recommend:**
  - Pre-approve on the behaviour score.
  - Start everyone at ₹1–2k and raise limits only for the safest band (₹5k), with a permanent 2–5% random-limit holdout to keep learning. The test needs ≈ 2,000–10,000 users per arm per band to detect a ₹20 profit difference.
  - Route contactability and responsiveness into the collections model, not the approval score."""
R["«O5»"] = """we removed **300 duplicate users**, filled **350 missing app-session counts** with the median (keeping a "missing" flag, which turned out to carry no signal), and capped **120 utilisations above the limit** (late-posted merchant reversals, not real over-limit spending). Outcomes are internally consistent: every default passed through 30+ DPD, and losses occur only on defaults. Clean data: **132,246 pre-approved users** (66,268 historical, 65,978 in the randomised experiment); 6-month default **5.69%**, 30+ DPD **17.9%**."""
R["«O61»"] = """
- **Left, the key chart of this notebook:** in the **historical** cohort, default *falls* as the limit rises (4.9% at ₹1k → 3.2% at ₹5k). In the **randomised experiment** it *rises* steeply (3.0% → 13.0%). The two cohorts are similar customers; only the way limits were assigned differs. The historical pattern is **confounding**: the old rule gave higher limits to better customers.
- **Right:** among customers who fall 30+ days behind, the chance of being cured by collections roughly **doubles when the customer is contactable**, and rises further with responsiveness to nudges (from ≈ 15% to ≈ 60% across groups)."""
R["«O71»"] = """the features most associated with default (Holm p < 0.0001) are:
- **Low-balance days**, with the largest effect (rank-biserial r = +0.27, small to medium).
- **Irregular top-ups** (−0.14).
- **A lower share of bills paid via the wallet** (−0.14).
- **More P2P transfers out** (+0.12).
- **Lower on-time bill payment** (−0.11).

Engagement features are weak for default (nudge response −0.09; contactable −0.03). Tenure, transaction count and the session-missing flag carry no signal. **(f) Business meaning:** "payment patterns" and "outstanding amounts" (the documented families) do the work for the default score. No single feature is strong, which is why a combined score is needed."""
R["«O72»"] = """
- **Out-of-cohort performance:** trained on the historical cohort and tested on the experiment cohort, the **logistic scorecard reaches AUC 0.714** (CI 0.707–0.722, KS 0.32). It is slightly **better than gradient boosting** (0.702): with smooth, mostly monotone effects, the simpler model wins.
- **It finds the truly weak customers:** AUC 0.84 for identifying the hidden bottom 20% of quality.
- **Rank ordering is clean:** default rises monotonically across score fifths, **2.0% → 3.3% → 5.3% → 7.8% → 15.6%** (a 7.7× top/bottom ratio).

**(f) Business meaning:** the score is good enough to drive pre-approval and limit bands, and the explainable logistic version can be used."""
R["«O73»"] = """**the documented engagement features matter for collections, not for approval.**
- **For default,** adding contactability and responsiveness is statistically significant (LR χ² = 28) but practically small: being contactable lowers the odds of default by ~12% (OR 0.88, CI 0.80–0.97), and responsiveness has no clear effect (OR 0.96 per +10 pp, CI includes 1).
- **For cure after 30+ DPD,** the effect is large (LR χ² = 1,393): contactable customers have **3.0× the odds of cure** (CI 2.8–3.2), and each +10 pp of nudge response multiplies the odds by 1.53.
- **Raw cure rates:** 46.9% vs 22.6%.

**(f) Business meaning:** this confirms the documented interpretation, that good feature design anticipates the downstream process. Feed these features to a **collections/cure model** that decides how early and how to contact each delinquent customer."""
R["«O74»"] = """
- **Historical data, naive:** each +₹1,000 of limit appears to **lower** default odds by 11% (OR 0.89, CI 0.87–0.92). This is a wrong answer that would encourage handing out bigger limits.
- **Adjusting for the score** only partly fixes it (OR 1.03): the old rule used information the score does not fully capture. In the historical cohort, limit correlates **0.63** with hidden true quality.
- **The randomised experiment** (correlation −0.01) gives the causal answer: **+₹1,000 of limit raises default odds by 47%** (OR 1.47, CI 1.44–1.50). Adjusting for the score barely changes it (1.49), as randomisation guarantees.

**Business meaning:** never estimate limit effects from historical limits. **Only a randomised limit test answers the limit question**, a standard practice at card issuers that this case strongly supports."""
R["«O75»"] = """
- **Randomisation worked:** arm sizes are equal (SRM χ² p = 0.90), and all features are balanced across arms (max |SMD| = 0.03).
- **The limit effect differs by band** (LR χ² = 88, p ≈ 3e-18). Each +₹1,000 raises default odds by **16% in the safest band and 63% in the riskiest** (all Holm p < 0.001).
- **Profit per user (chart):**
  - **Safest band (A):** profit is flat-to-rising with limit (₹31 at ₹1k → ₹38 at ₹5k). Extra spend roughly pays for the extra risk.
  - **Bands C–E:** higher limits destroy profit. In the riskiest band, ₹5k earns ₹208 of revenue but loses ₹705 to defaults (−₹497 per user).
- **Business meaning:** a higher limit is a *risk decision*, not just a growth lever. It pays only for the safest customers."""
R["«O76»"] = """the policy chosen on the design half, **A:₹5k, B:₹2k, C–E:₹1k**, earns **₹30.1 per user** on the evaluation half (default rate 3.4%):
- **Uniform ₹1,000:** ₹27.6 (3.1% default). This is the best uniform policy.
- **Uniform ₹2,000:** ₹16.8.
- **Old-rule-style tiers (₹5k → ₹1k):** ₹23.2. They give risky bands too much.
- **Uniform ₹3,000 or ₹5,000:** loses money (−₹12.5 and −₹144.8).

The gain of the optimal policy over uniform ₹1k is **+₹2.5 per user, CI −₹1.4 to +₹6.1**, so **we cannot reject H0**: the evidence favours it but is not yet conclusive. All sensible policies pass the 6% default guardrail; uniform ₹5k does not (13.3%). **Business meaning:** the big, certain win is *not* giving large limits to risky users. Fine-tuning limits for safe users is a small, still-uncertain gain that needs a bigger test."""
R["«O77»"] = """profit is very noisy: its standard deviation is ₹209 per user in the safest band and **₹749 in the riskiest**, because a few defaults lose up to ₹4,000. Detecting a **₹20** profit difference between two limits needs ≈ **1,700 users per arm in band A** but **≈ 22,000 in band E**. To detect ₹10 differences, about 4× more. This test (≈ 3,200 per arm per band) is powered for ₹20 differences only in bands A–B. **Business meaning:** that is why the profit-optimal policy's +₹2.5 gain is not yet significant. A permanent random-limit holdout of a few percent of new users, run for several cycles, provides the needed sample cheaply."""
R["«O9»"] = """per **10 lakh pre-approved users per 6 months**:
- **Profit by policy:**
  - Profit-optimal limits: ≈ **₹3.0 crore**.
  - Uniform ₹1k: ≈ ₹2.8 crore.
  - Old-rule-style tiers: ≈ ₹2.3 crore (≈ ₹0.7 crore less than optimal).
  - Uniform ₹2k: ₹1.7 crore.
  - Uniform ₹5k: **a loss of ≈ ₹14.5 crore**.
- **Reading:** the score's main value is **protection against over-limiting risky users** (≈ ₹17 crore between the best and worst limit strategies). Optimising limits for safe users adds only ≈ ₹0.25 crore and is not yet statistically confirmed.
- **Collections:** contactable delinquent customers cure 24 pp more often. With ≈ ₹1,800 average balance at 30+ DPD, every 1 lakh delinquent accounts made contactable is worth roughly **₹4 crore of balances cured** (an illustrative upper bound).
- Margins here are thin (2% merchant fee). Real BNPL economics include interest and convenience fees, which raise profits at every limit."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** the score ranks risk (AUC 0.71, monotone bands).
- **H2:** engagement adds little to default (small OR) ✅ but strongly to cure ✅.
- **H3 ✅:** limit raises default causally (+47% odds per ₹1k), more for risky bands.
- **H4 ❌ (not significant):** the profit-optimal policy beats uniform ₹1k by +₹2.5 per user (CI includes 0).
- **Guardrail:** passed by every policy except uniform ₹5k.

**I recommend:**
1. **Pre-approve on the behaviour score** (logistic scorecard: explainable, as strong as boosting here).
2. **Start limits low and earn upward:** ₹1k for bands C–E, ₹2k for band B, ₹5k only for band A. Raise limits after on-time repayment cycles.
3. **Never infer limit effects from historical limits.** Keep a **permanent 2–5% random-limit holdout** and review the band-by-limit profit table every cycle, powered to detect ₹20 differences.
4. **Collections model:** use contactability and responsiveness to prioritise and time collection contacts. Fix unreachable numbers at onboarding (verified phone), since that directly lifts cure rates.
5. **Compliance:** document the limit policy under the lender's credit policy (RBI DLG), with the KFS showing the limit and charges.

**KPIs:** 6-month profit per pre-approved user by band; default rate per band and limit; cure rate after 30+ DPD by contactability; limit-increase uptake and post-increase default; holdout sample size per arm."""

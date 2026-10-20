R = {}
R["«EXEC»"] = """*(Synthetic data built on Axis Bank's documented claim; the source does not say which metric improved by 40%. Written after the analysis.)*

- **The question:** is the bank's in-house score really "more than 40% better" than the bureau score, and what does that mean in defaults and approvals?
- **The same two scores can be "6% better" or "100% better", depending on the metric.** Out-of-time, the in-house score (bank transaction data + bureau) improves on the bureau score alone by:

| Metric | Improvement (95% CI) |
|---|---|
| AUC | +6.5% |
| Bad rate at a 70% approval rate | −11% |
| Bads caught in the riskiest 10% | +18% |
| **Gini** | **+32%** (24–41%) |
| **KS** | **+41%** (29–54%), the documented range |
| Approvals at a 3.5% bad rate | +50% |
| Brier skill | +100% |

  All are statistically significant. **"40% better" is a true statement here only for KS.** Without the metric it is not a claim a credit committee can use.
- **What the improvement means:**
  - At today's 70% approval rate, the bad rate falls from **4.34% to 3.86%**.
  - At the same risk, approvals rise from **70.5% to 81.3%**.
- **Who changes:** the swap set is 11.7% of applicants each way. Customers the new score newly approves default **5.6%** of the time, vs **8.5%** for those it newly rejects (p ≈ 7e-10). The new score also ranks **no-hit applicants** the bureau cannot score (AUC 0.61 vs 0.50).
- **The two data sources are complements:** internal data alone (AUC 0.620) are no better than the bureau alone (0.628), but together they are clearly better (0.668). The advantage is stable across all six test months (no decay; PSI 0.000).
- **₹ impact (1 lakh applications/month):**
  - Either ≈ **₹40 crore/year of credit losses avoided** (CI ₹26–53 crore) at the same approval rate.
  - Or ≈ ₹20 crore/year of extra profit from approving 10.8 pp more customers at the same risk.
- **I recommend:**
  - Adopt the in-house score as champion for existing-customer lending, after a champion–challenger run on 5–10% of decisions.
  - Report its benefit as "bad rate at fixed approval" and "approvals at fixed bad rate", with Gini and KS stated explicitly, never as an unlabelled "X% better"."""
R["«O5»"] = """we removed **500 duplicate applications** and converted **603 bureau scores of 0** (a timeout sentinel, not a real score) to missing with a flag, alongside the genuine no-hits. **2,257 missing balance trends** (1.5%) are set to 0 with a missing flag. No no-hit applicant has a score. Clean: **150,000 applications, 5.67% bad**; 99,857 for training (months 1–12) and **50,143 out-of-time** test applications (months 13–18, 2,836 bads)."""
R["«O61»"] = """
- **Left:** the bureau score ranks **thick** files well, ranks **thin** files less steeply, and gives **no information at all for no-hit** applicants (the grey line, a flat 5.5% bad rate the bureau cannot split). That is 12% of applicants the bureau cannot rank, and 20% it ranks poorly.
- **Right:** a signal only the bank can see. Customers with bounced payments in the last year default far more often (≈ 4% with none vs well above 10% with 4–5+). The bureau never sees an ECS/NACH bounce on a savings account."""
R["«O71»"] = """
- **The bureau score alone:** AUC 0.628 (Gini 0.255, KS 0.176).
- **Bureau + application data** (logistic) adds a little: +0.008 AUC (Holm p = 0.001).
- **The in-house score** (internal + bureau, gradient boosting) reaches **AUC 0.668** (Gini 0.336, KS 0.248): **+0.041 vs the bureau** (Holm p < 0.0001) and +0.032 vs bureau + application (p ≈ 1e-13).
- **Internal data alone** (0.620) do *not* beat the bureau (p = 0.29).
- **(f) Business meaning:** the bank's edge comes from **combining** its own data with the bureau, not replacing the bureau. Absolute AUCs are modest because this is a pre-screened customer base."""
R["«O72»"] = """**the same two scores, seven verdicts** (in-house over bureau, all CIs exclude 0):
- **Small relative gains:** AUC **+6.5%**; bad rate at 70% approval **−11.2%** (4.34% → 3.86%); bads caught in the riskiest decile **+17.6%**.
- **Medium:** Gini **+31.8%** (CI 24–41%).
- **Large:** KS **+41.3%** (CI 29–54%), the documented "more than 40%" range; approval rate at a 3.5% bad rate **+49.8%** (40% → 60%); Brier skill score about **+100%** (roughly doubles; probability-based, so it is not shown in the level table).

**Why they differ:** AUC starts from 0.5, so relative changes look small. Gini and KS are "excess over random", so they look larger. Approval-at-target depends on how close the target is to the base rate, and can swing a lot. **Business meaning:** "40% better" can be honestly produced by choosing KS. Ask for the metric, then translate it into the bad rate at the current approval rate. That is the number that moves the P&L."""
R["«O73»"] = """at a 70% approval rate, the two scores agree on 76% of applicants (58% approved by both, 18% rejected by both). The **swap set** is 11.7% each way:
- **Swap-in** (newly approved by the in-house score): bad rate **5.55%** (CI 5.0–6.2%). They are mostly thin-file customers whose internal data look good.
- **Swap-out** (newly rejected): bad rate **8.46%** (CI 7.8–9.2%). **27% are no-hit applicants** whom the bureau "approved" only because it gave them the median score.
- **The difference is significant** (z = 6.2, p ≈ 7e-10). The swap trades higher-risk approvals for lower-risk ones at no change in volume.

**(f) Business meaning:** this is the evidence a credit committee wants. Both swap groups are riskier than "approved by both" (3.5%), as expected at the margin, but the new score's marginal approvals are clearly the better ones."""
R["«O74»"] = """the in-house score wins in every bureau-depth group (all Holm p < 0.0001):
- **Thick files:** AUC 0.652 → 0.682 (+0.031).
- **Thin files:** 0.607 → 0.651 (+0.044).
- **No-hit:** **0.500 → 0.611 (+0.111)**, where the bureau has nothing.

Calibration is good overall (mean predicted − observed within ±0.2 pp in each group). The calibration slope is 0.82 for no-hit (slightly over-confident) and 1.08 for thick files. **Business meaning:** the largest gains are exactly where the bureau is weakest. That is what makes database-driven pre-approval ("66% of PL, 79% of cards") possible for customers with little bureau history."""
R["«O75»"] = """the in-house advantage holds in **every** test month: ΔGini between +0.05 and +0.10, with no downward trend (slope −0.001/month, p = 0.84). The score distribution is unchanged between training and test (**PSI = 0.000**). **Business meaning:** the gain is not a lucky month or a training artefact. It is stable enough to justify switching champions, subject to ongoing monthly monitoring."""
R["«O8»"] = """by permutation importance, the **bureau score is still the single most important input** (shuffling it drops AUC by 0.085). The top internal signals are **salary-credit regularity** (0.013), **bounces** (0.011), **cash-withdrawal share** (0.007), **EMI-to-salary** (0.006) and **internal DPD history** (0.005). Each is small alone, but together they add +0.04 AUC. This is consistent with "2,000 attributes": many weak internal signals add up."""
R["«O9»"] = """per **1 lakh applications a month** (₹1.5 lakh average exposure, 65% LGD, ₹6,000 12-month margin per good customer):
- **(a) Keep approving 70%:** the bad rate falls 4.34% → 3.86% → ≈ **₹40 crore/year of credit losses avoided** (95% CI ₹26–53 crore).
- **(b) Keep the bureau's risk level:** approvals rise from 70.5% to **81.3% (+10.8 pp)** → ≈ **₹20 crore/year of extra profit**, plus 13,000 more customers served a year.
- **The cheap partial upgrade** (bureau + application logistic) gets only a fraction of this (bad rate 4.25% at 70% approval).
- **Reading:** this is how "40% better" should be presented to a business, as ₹ and approvals at a stated operating point."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** in-house AUC > bureau (+0.041) and > bureau + application (+0.032), Holm p < 0.0001.
- **H2 ✅:** bad rate at 70% approval −0.48 pp (CI excludes 0).
- **H3 ✅:** swap-in bad rate 5.6% < swap-out 8.5% (p ≈ 7e-10).
- **Stability ✅:** no decay; PSI 0.000.

**I recommend:**
1. **Promote the in-house score to champion** for existing-customer PL and card decisions, after a **champion–challenger** period with the challenger deciding 5–10% of applications for 3–6 months.
2. **Choose how to bank the gain:** fewer losses at today's approval rate (≈ ₹40 crore/year) or more approvals at today's risk (≈ ₹20 crore/year, +10.8 pp approvals), or a mix. That is a business-strategy decision.
3. **Keep the bureau inside the model:** internal data complement, not replace, it.
4. **Report standard metrics:** Gini, KS, bad rate at fixed approval, approval at fixed bad rate, and the swap-set table. Never report an unlabelled "X% better".
5. **Governance:** reason codes for declines, fairness checks on internal features, monthly PSI and Gini monitoring.

**KPIs:** out-of-time Gini/KS (monthly); bad rate of approved by vintage; swap-in vs swap-out bad rates in the champion–challenger; approval rate; PSI; share of pre-approved sourcing."""

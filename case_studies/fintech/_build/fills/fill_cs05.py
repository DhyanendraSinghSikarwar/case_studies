R = {}
R["«EXEC»"] = """*(Synthetic data built on Razorpay's documented design and headline figures. The LLM agents are not reproduced; their decisions are evaluated. Written after the analysis.)*

- **The question:** is the AI merchant reviewer really "99% accurate, up from 88%", and is it safe to let it decide?
- **The headline is reproducible, but only against the right yardstick.** Against a **panel of three senior reviewers**, the agent agrees **98.8%** of the time (κ = 0.91) and individual analysts **88.7%** (κ = 0.39), matching the documented 99% vs 88%. Judged against **a single analyst's decision**, the same agent looks only **88% "accurate"**, because analysts disagree with each other (reject rates range from 1.5% to 31.6%).
- **"Accuracy" hides the base rate.** Approving every merchant would score **92.8%** against the panel. The informative numbers are on the risky merchants:
  - **Sensitivity** (risky merchants stopped): agent 91% vs analysts 64%.
  - **Balanced accuracy:** 0.95 vs 0.77.
  - Both McNemar p < 1e-11.
- **The sobering part:** against what really happened 6 months later, even the senior panel stops only **48%** of eventually-bad merchants, and the agent **52%**. About half of merchant fraud is **not visible at onboarding**. The agent lets through the same number of bad merchants as analysts (≈ 430 per 12,000 reviews) but **wrongly rejects ~800 fewer good merchants a month**.
- **A safe automation policy:** let the agent decide alone when its confidence ≥ 0.3. That covers **96%** of reviews with an error rate of 0.35% (95% upper bound 0.6%, inside the 1% limit). The rest (contested cases, where 53% of agent errors live, plus timeouts) go to analysts.
- **Speed and cost:**
  - **Speed:** median 10 s (P95 15 s) vs 22 minutes.
  - **Tokens:** 60% fewer than the monolithic design, matching the documented figure.
  - **Analyst time:** ≈ 4,500 hours a month freed.
  - **₹:** ≈ **₹2.3 crore/month** saved, mostly from not losing good merchants.
- **I recommend:**
  - Adopt agent-first review with the confidence threshold.
  - Audit about 170 auto-decisions a month against seniors.
  - Report sensitivity and specificity against a gold panel, not "accuracy".
  - Invest in **post-onboarding transaction monitoring**, because that is where the other half of merchant fraud must be caught."""
R["«O5»"] = """we removed **250 duplicate reviews**. **400 agent timeouts** (no decision) are not errors to be scored but a routing rule: they go to an analyst. 38 of them fall in the gold panel and are excluded from agent accuracy (and reported). Evidence fields are logically consistent (no SSL or page-load time without a website). Clean: **36,000 merchants**; analysts reject **13.9%**, the agent **7.4%**, while **9.6%** are truly risky."""
R["«O61»"] = """**left:** with merchants allocated at random, analysts' reject rates range from **1.5% to 31.6%**: some approve almost everything, others reject a third of applicants. This is the documented consistency problem in one chart. **Right:** the agent's reject probability separates most merchants cleanly (good merchants pile up near 0, many risky ones near 1), with a **grey zone in the middle**. That zone is where automation should hand over to humans, and many risky merchants still sit at low scores: their onboarding evidence looks clean."""
R["«O71»"] = """
- **Analysts are inconsistent:** reject rates differ hugely between analysts (χ² = 1,629, p ≈ 0). Agreement of a single analyst with the gold panel is only **κ = 0.39** ("fair").
- **Senior reviewers are consistent:** **Fleiss' κ = 0.89**, all three agreeing on 97.8% of merchants, which makes them a reasonable reference.
- **The agent agrees with the panel at κ = 0.91**, as well as seniors agree with each other.
- **(f) Business meaning:** the problem the agent solves is **variance**. Every merchant is judged with the same standard, which is also fairer to merchants."""
R["«O72»"] = """
- **Against a single analyst** (one reading of the documented "accuracy vs analyst decisions"), the agent scores only **87.9%**: the yardstick itself is noisy.
- **Against the gold panel,** the agent scores **98.8% (CI 98.3–99.1%)** vs analysts' **88.7%**. That reproduces the documented "99%+ vs 88%".
- **The base rate:** "always approve" already scores **92.8%** against the panel, so accuracy must be read against that.
- **On the cases that matter**, the agent stops **91%** of panel-flagged risky merchants (CI 86–94%) vs analysts' **64%**. Only-agent-right cases outnumber only-analyst-right cases 65 to 8 (exact McNemar p ≈ 3e-12). The agent also approves good merchants more reliably (specificity 99.4% vs 90.6%), and its rejects are mostly right (precision 92% vs 35%).
- **Against the truth** (the merchant actually went bad), everyone is weak: agent sensitivity **52%**, the gold panel 48%, analysts 49%. About half of risky merchants show no red flags at onboarding.
- **(f) Business meaning:** "99%" means "agrees with senior reviewers". It does *not* mean "catches 99% of fraud"."""
R["«O73»"] = """the agent's errors (vs the panel) concentrate where the seniors themselves disagree. On **contested** cases (2.2% of merchants) its error rate is **29.7%**, vs **0.6%** on unanimous ones (Fisher p ≈ 1e-23), and contested cases account for **53%** of all its errors. By category, agent error rates are low everywhere (0–2.8%), while analysts err most in high-risk categories (forex/crypto 19%, nutraceuticals 16%). **Business meaning:** many of the agent's "mistakes" are genuinely ambiguous merchants. They should be escalated, not "fixed" by tuning the model to one senior's opinion."""
R["«O74»"] = """letting the agent decide everything gives a 1.2% error rate vs the panel (upper bound 1.6%: fails the 1% limit) and auto-approves 9.4% of panel-risky merchants. With **confidence ≥ 0.3**, the agent auto-decides **96.1%** of reviews with an error rate of **0.35% (one-sided 95% upper bound 0.59%)** ✅, and only 2.8% of risky merchants are auto-approved. Higher thresholds (≥ 0.5) cut auto-approved risky merchants to 0.5% at 94% coverage. **That stricter setting is worth it if a missed fraudster is very costly.** The risk–coverage curve lets the risk committee choose the trade-off explicitly."""
R["«O75»"] = """on 6-month outcomes, merchants approved by the agent go bad **3.85%** of the time vs **4.16%** for analyst-approved (−0.31 pp, CI −0.62 to −0.01): **non-inferior** at +0.5 pp, and slightly better. Per 12,000 reviews, the agent approves ≈ **780 more merchants**, lets through the **same number of bad ones (≈ 428 vs 430)**, and wrongly rejects ≈ **297 good merchants vs 1,103**. **Business meaning:** the agent's real win is fewer good merchants turned away, at no extra fraud. The ≈ 430 bad merchants that *both* approve are invisible at onboarding and must be caught by transaction monitoring (Cases 6–8)."""
R["«O76»"] = """
- **Speed:** the planner-plus-parallel-fetchers design (v2) has a median latency of **10.0 s** (P95 15.1 s), inside the documented 8–12 s, vs 38 s (P95 74 s) for the monolithic v1.
- **Tokens:** **9,435 vs 23,555 per review: 60% fewer**, exactly the documented reduction (Wilcoxon p ≈ 0).
- **Analyst time:** in this simulation analysts spend ≈ 4,700 hours a month (22 minutes per review; the documented 8,500 hours implies closer to 40 minutes). With 96% auto-decided, ≈ **4,500 hours a month are freed**.
- **Business meaning:** the parallel-fetcher architecture is what makes the system both fast and cheap."""
R["«O77»"] = """if the auto-decided error rate is 0.35% today, a monthly audit of **≈ 170 auto-decided reviews** (re-reviewed by seniors) detects a deterioration to 2% with 80% power. Detecting a rise to 3% needs ≈ 80, and to 5% ≈ 40. **Business meaning:** monitoring is cheap, about 2–3 senior-days a month, and it must also re-run after every prompt or model change."""
R["«O9»"] = """per **12,000 reviews a month** (assumptions: analysts ₹600/hour; a bad merchant let through costs ₹1.5 lakh; a good merchant wrongly rejected costs ₹20,000 of lifetime revenue; ₹0.0004 per token):

| Policy | Review cost | Bad merchants (fraud) | Good merchants lost | Total |
|---|---|---|---|---|
| Analysts review everything | ₹28 lakh | ₹874 lakh | ₹221 lakh | **₹11.2 crore** |
| Agent decides everything | ₹0.45 lakh | ₹837 lakh | ₹59 lakh | ₹9.0 crore |
| **Agent at confidence ≥ 0.3 + analysts** | ₹1.5 lakh | ₹833 lakh | ₹62 lakh | **₹9.0 crore** |

- **The saving is ≈ ₹2.3 crore/month, mostly from not losing good merchants** (≈ ₹1.6 crore) and analyst time (≈ ₹0.27 crore).
- **The single largest cost, ≈ ₹8.3 crore/month of fraud from merchants that look clean at onboarding, is untouched by any onboarding review.** That money is in post-onboarding monitoring."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** the agent agrees with the gold panel far more than analysts (98.8% vs 88.7%, McNemar p ≈ 1e-60).
- **H2 ✅:** sensitivity 91% vs 64% (p ≈ 3e-12).
- **H3 ✅:** at confidence ≥ 0.3, the auto-decided error upper bound is 0.59% (< 1%).
- **H4 ✅:** 6-month bad rate non-inferior (−0.31 pp).
- **Caveat:** onboarding review, human or AI, catches only about half of eventually-bad merchants.

**I recommend:**
1. **Agent-first review:** auto-decide when confidence ≥ 0.3 (≈ 96% of reviews), or ≥ 0.5 if risk appetite is lower. Escalate contested cases, timeouts and new high-risk categories to analysts.
2. **Define accuracy properly:** maintain a **frozen gold set** (3-senior majority), and report sensitivity, specificity, balanced accuracy and κ for every model or prompt version.
3. **Monthly audit:** ~170 random auto-decisions re-reviewed by seniors, plus checks that the agent's cited evidence matches the source (hallucination/faithfulness), plus prompt-injection tests.
4. **Close the real gap:** route the freed analyst time (~4,500 hours a month) to **post-onboarding monitoring**: early transaction patterns, chargebacks, website changes after approval.
5. **Governance:** keep the full evidence trail per decision (RBI PA guidelines), and monitor reject rates by merchant segment for fairness.

**KPIs:** sensitivity/specificity vs gold set per release; auto-decision coverage and audited error rate; good-merchant approval rate; 6-month bad rate of approved merchants; median/P95 latency; tokens per review; analyst hours per month."""

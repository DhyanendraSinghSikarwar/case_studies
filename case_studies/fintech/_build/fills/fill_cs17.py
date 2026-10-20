R = {}
R["«EXEC»"] = """*(Synthetic data built on HDFC Bank's documented design and success criterion. Written after the analysis.)*

- **The question:** are 10-second pre-approved personal loans really "on a par" with branch-sourced loans on delinquency, given they are far cheaper and faster?
- **The randomised pilot says yes.** Among 16,000 eligible applicants randomly assigned to instant or physical processing, 12-month 30+ DPD was **3.90% vs 3.69%: +0.22 pp, 95% CI −0.38 to +0.81 pp**. The upper bound is below the pre-agreed **1 pp** margin, so non-inferiority is shown (p = 0.005). Time to delinquency agrees (hazard ratio 1.06, CI 0.90–1.24, below the 1.25 margin), and 90+ DPD is identical (1.29% vs 1.31%).
- **The raw historical comparison could not have proved it,** and was misleading in two ways:
  - Instant vs branch loans differ by +0.6 pp, "not significantly different", yet the CI reaches +1.4 pp, so **non-inferiority is *not* shown**. "No significant difference" is not "on par".
  - After adjusting for who borrows (instant borrowers are much better-scored), the gap grows to **+2.0 pp**, because branch officers screen on information the data do not hold. Observational adjustment overstates the harm. Only randomisation gives the truth (true effect ≈ +0.46 pp).
- **The layered score:** bureau and behaviour layers carry most of the information. The "social" (internet-usage) layer adds almost nothing (Holm p = 0.07), a candidate to drop on privacy grounds.
- **₹ economics:** at ≈ ₹2,000 crore/month of instant disbursals, processing savings are ≈ **₹6.7 crore/month**. The pilot's best estimate of extra credit loss is ≈ ₹1.5 crore/month, a net gain of **≈ ₹5.2 crore/month** (≈ ₹1.1 crore even at the pessimistic CI bound). **Break-even is +0.96 pp of extra delinquency**, which shows the 1 pp margin is economically sound.
- **I recommend:**
  - Keep instant loans for eligible customers, and adopt the NI pilot as the standard evidence for any expansion of eligibility.
  - Use a pre-registered 1 pp margin and ≥ 6,000–9,000 loans per arm.
  - Re-test on 24-month 90+ DPD.
  - Drop the "social" layer unless a pilot shows it adds value."""
R["«O5»"] = """we removed **300 duplicate loan rows**. **11 delinquent loans lack the month they first reached 30+ DPD**; they are set to month 6 for the survival analysis and flagged, and a sensitivity analysis excluding them (7.5) gives the same hazard ratio. **1,500 missing engagement scores** are filled with the median plus a flag. No loan exceeds the documented ₹15 lakh cap, and every 90+ DPD passed through 30+ DPD. Clean: **25,306 loans**: 9,306 observational (5,558 instant, 3,748 branch) and 16,000 in the randomised pilot; overall 30+ DPD 3.95%."""
R["«O61»"] = """**left:** the dashed observational curves show instant loans slightly *above* branch loans, while the solid pilot curves (same customers, random channel) nearly overlap. **Right:** observational instant borrowers are almost all above the eligibility cut-off, while branch borrowers spread across the whole score range. The two observational groups are **different populations**, so their raw delinquency comparison answers the wrong question."""
R["«O71»"] = """
- **Bureau and behaviour layers matter:** bureau OR 0.71 per unit (LR χ² = 142, Holm p < 0.0001); behaviour OR 0.81 (Holm p = 0.03).
- **Ability adds nothing once loan size is in the model** (p = 0.22). Higher earners borrow more, so salary and loan size offset each other.
- **The "social" layer is marginal:** OR 0.93, Holm p = 0.07.
- **Low AUCs are expected here:** the combined score's AUC is only 0.565, and the layered logistic's 0.616, because every loan here went to an approved, mostly top-third customer. Range restriction makes all scores look weaker within the approved book.
- **(f) Business meaning:** the framework's value comes from the bureau and behavioural layers. The social layer contributes little and carries privacy and fairness risk. Test it in a pilot or drop it."""
R["«O72»"] = """
- **The raw comparison:** instant loans 4.46% vs branch 3.84%, **+0.62 pp (Newcombe CI −0.22 to +1.43 pp)**.
  - A naive reading says "not significantly different, on par".
  - The non-inferiority test says **not shown**: the upper bound (+1.43 pp) exceeds the 1 pp margin (p_NI = 0.18).
- **The populations are very different:** SMDs of +0.50 to +0.87 on every layer and on loan size, and +1.62 on eligibility (all instant borrowers are eligible vs 43% of branch borrowers).
- **(f) Business meaning:** the documented "on a par" claim needs both a margin and comparable customers. Without them it is not evidence."""
R["«O73»"] = """inverse-probability weighting balances every measured layer (all |SMD| ≤ 0.09 after weighting), but it **makes the gap bigger, not smaller**: instant 4.46% vs reweighted branch **2.44% (+2.0 pp, CI +1.0 to +3.0)**. Restricting to eligible customers only gives the same picture (+1.9 to +2.0 pp). Overlap is also weak: only 43% of branch loans have a propensity above 0.1, and the weighted branch group's effective size is only 1,112 of 3,748. **Why it overstates the harm:** branch officers decline risky applicants on information the data never record (an interview, documents, local knowledge), so branch borrowers are better than their scores. IPW cannot see that. **(f) Business meaning:** neither the raw nor the adjusted observational comparison gives the right answer (truth: +0.46 pp). One looks falsely reassuring, the other falsely alarming."""
R["«O74»"] = """
- **E-value of the IPW result (RR 1.83): 3.06.** An unmeasured factor associated with both channel and delinquency by a risk ratio of about **3** would fully explain it. Officer screening on interviews and documents can plausibly be that strong, so the adjusted observational "harm" is **not robust**.
- **E-value of the raw result (RR 1.16): 1.59**, which even modest confounding could produce.
- **Truth** (hidden model, pilot-like customers): RR ≈ 1.13.
- **Business meaning:** when the comparison channel involves human judgement on unrecorded information, observational adjustment is fragile. This is why a randomised pilot is needed."""
R["«O75»"] = """
- **Randomisation worked:** 7,995 vs 8,005 (SRM p = 0.94), and all layers balanced (max |SMD| = 0.016).
- **Primary NI test passes:** 30+ DPD **3.90% (instant) vs 3.69% (physical)**, difference **+0.22 pp (95% CI −0.38 to +0.81)**. The upper bound is below the 1 pp margin (one-sided p_NI = 0.005), so instant processing is **non-inferior**.
- **The risk ratio** is 1.06 (upper bound 1.24 < 1.25 ✅).
- **Time to delinquency:** the curves overlap (log-rank p = 0.47), and the adjusted **Cox HR is 1.06 (CI 0.90–1.24)**, non-inferior at the 1.25 margin. Excluding the 11 loans with an imputed month gives the same HR (1.06).
- **Guardrail:** 90+ DPD 1.29% vs 1.31% (−0.02 pp, CI −0.38 to +0.33).
- **(f) Business meaning:** this is the documented claim, "delinquency on a par", now **proved** with a pre-set margin. Note the honest nuance: non-inferior does not mean identical. The best estimate is a slightly higher rate (+0.2 pp; truth +0.46 pp) that sits well within what the business accepted."""
R["«O76»"] = """the pilot (8,000 per arm) had **≈ 92% power** if the channels were truly identical, but only **≈ 50%** if the true deterioration were +0.4 pp (the real value here is ≈ +0.46 pp). So it was somewhat lucky to pass. To be 80% sure with a +0.4 pp true difference needs **≈ 16,000 per arm**. A tighter margin is far more expensive: 0.5 pp needs 22,000–585,000 per arm depending on the true difference. **Business meaning:** size NI pilots for a plausible small deterioration, not for "no difference", or a genuinely acceptable channel may fail the test by chance."""
R["«O8»"] = """on pilot loans, the combined P27-style score (AUC 0.567) and gradient boosting on the raw layer inputs (0.576) perform about the same. Both are low because all pilot borrowers are already in the eligible top third (range restriction). **A black-box model adds nothing material here**, so the transparent layered score is the better choice for a credit committee: each layer can be explained, monitored and challenged."""
R["«O9»"] = """at the documented scale (≈ **₹2,000 crore of instant loans a month**, ≈ 28,600 loans at a ₹7 lakh average ticket in this simulation):
- **Processing saving** (₹2,500 → ₹150 per loan): ≈ **₹6.7 crore/month**, before counting the faster turnaround (10 seconds vs ~2–3 days), which also raises take-up.
- **Extra credit loss (35% loss on extra 30+ DPD loans):**
  - Pilot point estimate (+0.22 pp): ₹1.5 crore → **net +₹5.2 crore/month**.
  - Pilot upper bound (+0.81 pp): ₹5.7 crore → net +₹1.05 crore/month.
  - At the full 1 pp margin: ₹7.0 crore → net −₹0.27 crore/month.
  - Hidden truth (+0.46 pp): net +₹3.5 crore/month.
- **Break-even deterioration = 0.96 pp:** the 1 pp margin sits almost exactly at break-even, so the committee's margin choice is economically consistent.
- All figures rest on the stated cost and loss assumptions."""
R["«O10»"] = """**Decision against the pre-registered rule:**
- **Primary, pilot ✅ non-inferior** (+0.22 pp, upper bound 0.81 < 1.0 pp).
- **Secondary ✅:** RR upper bound 1.24 < 1.25; HR upper bound 1.24 < 1.25.
- **Guardrail ✅:** 90+ DPD equal.
- **Observational analyses:** inconclusive or misleading, and not used for the decision.
- **Layers:** bureau ✅ and behaviour ✅ add information; ability ❌ (after loan size); social ≈ ❌ (Holm p = 0.07).

**I recommend:**
1. **Continue 10-second loans for eligible customers.** The evidence now meets a proper NI standard, not just "looked similar".
2. **Make the randomised NI pilot the gate for every eligibility expansion** (e.g., moving from the top third to the top 40%): a pre-registered 1 pp margin (≈ break-even), ≥ 16,000 loans per arm to be robust to a +0.4 pp true deterioration, and 12- and 24-month reads.
3. **Never use raw or "adjusted" channel comparisons as proof:** branch underwriting uses unrecorded information (E-value ≈ 3).
4. **Simplify the score:** drop or re-justify the "social" layer (privacy, fairness, little value). Keep the bureau and behaviour layers.
5. **Monitor monthly:** 30+ DPD by channel and vintage, with a CUSUM alarm if instant-loan delinquency drifts above physical by more than 0.5 pp.

**KPIs:** 12- and 24-month 30+ and 90+ DPD by channel (pilot-controlled); processing cost per loan; TAT; take-up of pre-approved offers; complaints/mis-selling flags on instant loans."""

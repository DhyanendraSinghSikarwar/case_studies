R = {}
R["«EXEC»"] = """*(Synthetic validation records, not images: model probabilities vs a surveyor re-inspection sample. ICICI Lombard disclosed no accuracy figure beyond "fit for purpose". Written after the analysis.)*

- **The question:** can customer phone photos replace a surveyor, and for which cases?
- **The model is good at some things and weak at others (vs surveyors, 49,000 part assessments):**
  - **Cracks** (mostly glass and lamps): 92% found.
  - **Clean parts:** 96% correctly passed.
  - **Scratches:** 73% found, but only 47% of "scratch" calls are real scratches (many are glare or dents).
  - **Dents:** only **59% found**; 29% are called scratches. Dents drive repair cost, so this is the weak spot.
  - **Overall agreement with surveyors:** κ = 0.70 ("substantial").
- **Photo quality matters:** each +0.1 of quality cuts the odds of a wrong call by 20% (p ≈ 1e-22). A "retake your photo" prompt for the worst 5% of photos lifts accuracy on damaged parts from 74% to 75%, a small gain. Night shots are not the problem here (p = 0.8); blur and glare are.
- **Repair-cost estimates are too loose for settlement:** the model's case-level estimate is within ±₹3,000 of the surveyor's for only **55%** of cases (26% within ±15%). The 95% limits of agreement are ±₹10,000, and the error grows with claim size.
- **The pre-registered auto-settle rule almost works, but only on a sliver of claims:**
  - The best rule is "estimate ≤ ₹20,000, no structural dent predicted, every part confidence ≥ 0.7, photo quality ≥ 0.4".
  - It settles **5.4%** of own-damage claims with **0 complex claims found** in the sample. But with only ~147 checked, the one-sided 95% upper bound is **2.02%**, just above the 2% limit, so the rule is **not yet certified**. The rule of three says ~150 checked claims are needed even with zero errors, and several hundred more at a 0.5% true rate.
  - Looser rules cover up to 33% of claims but let complex claims through at 5–6% (upper bounds 6–8%).
- **Renewals (pre-existing damage) pass:** among break-in renewals that have damage, the model flags damage in **94.4%** (CI 92.2–96.0%), above the 90% target. Clean cars are passed correctly only 71% of the time, so some customers get unnecessary follow-up.
- **₹ at the documented 80,000 claims/month:** the rule auto-settles ≈ 4,300 claims, saving ≈ **₹0.65 crore/month** of surveyor visits (plus ≈ 11,000 customer-days of waiting) with no measured leakage. The documented target of "over 80,000 simple claims a month" is **not reachable on this accuracy** without a better dent model.
- **I recommend:**
  - Launch photo inspection for **renewals** now.
  - Auto-settle only the tight rule, with an extended validation of ≥ 600 checked claims to certify it.
  - Add a "second angle" photo prompt when a dent is possible.
  - Keep a random 20% surveyor sample for ongoing monitoring."""
R["«O5»"] = """we removed **500 duplicated frames** (the same part assessed twice) and sent **150 cases with missing photo metadata (EXIF)** to the manual route, because the quality gate cannot be applied without it. Probabilities sum to 1, and surveyor costs exist only for checked cases. Clean: **24,000 inspections, 240,000 part assessments**, of which **4,913 cases (49,130 parts)** were re-inspected by a surveyor. The surveyor reference itself is 99.9% consistent with the hidden truth."""
R["«O61»"] = """**left:** the confusion matrix shows the model's pattern. Cracks and clean parts are well identified, scratches and dents are confused with each other, and **29% of real dents are called scratches**, which understates repair cost. **Right:** agreement with the surveyor on damaged parts climbs steadily with photo quality, while for clean parts accuracy stays high. Poor photos mostly cause **missed damage**, not false alarms."""
R["«O71»"] = """
- **Cohen's κ = 0.70** against surveyors ("substantial"). By class: **cracks** sensitivity 92% (CI 91–93%, precision 70%), **clean parts** 96% sensitivity (precision 99%), **scratches** 73% sensitivity but only **47% precision**, and **dents 59% sensitivity** (CI 56–61%).
- **Glass and lamps** are far easier than body panels (86% vs 66% accuracy on damaged parts).
- **(f) Business meaning:** the model is "fit for purpose" for spotting glass damage and clean cars, but not yet for pricing body damage. The dent problem is the one to fix."""
R["«O72»"] = """photo quality is a strong predictor of mistakes: **each +0.1 of quality lowers the odds of a wrong call by ≈ 20%** (OR 0.80; LR χ² = 97, p ≈ 8e-23). Night shots add nothing once quality is controlled (OR 1.03, p = 0.8). A "retake" gate has modest value: sending back the worst 5% of photos (quality < 0.4) lifts accuracy on damaged parts from 74.1% to 74.9%, and sending back 14% (< 0.5) to 76.0%. **Business meaning:** a retake prompt is cheap and helps a little, but photo quality alone will not fix the dent problem. The model itself must improve."""
R["«O73»"] = """on 2,749 damaged cases the model's cost estimate is nearly unbiased overall (bias −₹304), but individually noisy: the **95% limits of agreement are ₹−10,500 to +₹9,900**, only **55%** of cases are within ±₹3,000 and **26% within ±15%**. The error also grows with claim size (p ≈ 2e-17): large claims are under-estimated. **Criterion 2 (cost within ±₹3,000 for ≥ 80%) therefore fails on the whole population** and only passes within the tight low-cost slice used for auto-settlement (90% there). **Business meaning:** auto-settlement can be priced only for small, simple claims."""
R["«O74»"] = """the grid shows the trade-off clearly. **Looser rules cover more claims but fail the safety limit:** at confidence ≥ 0.5, coverage is 28–33% but 5–6% of auto-settled claims are truly complex (upper bounds 6–8%). **Tighter rules meet the 2% target on the point estimate:** confidence ≥ 0.7 gives **zero complex claims in ~147 checked auto-settled claims** (coverage 5.2–5.5%), but the one-sided 95% upper bound is 2.0–2.1%, so it sits **just on the wrong side of the 2% limit**. Confidence ≥ 0.8 is too rare to measure (about 30 claims). **We therefore report that no rule is yet certified**, and the closest, "cost ≤ ₹20,000, confidence ≥ 0.7, quality ≥ 0.4", covers 5.4% of claims with 90.5% of cost estimates within ±₹3,000. **Business meaning:** the rule is probably safe; it simply has not been *proved* safe. More checked claims, not a looser rule, is the answer."""
R["«O75»"] = """for break-in renewals, the model flags damage in **94.4%** of cars that have it (Wilson **92.2–96.0%**; 574 cars), so **criterion 3 is met**. Detection by damage type is highest for cracks (98%) and dents (93%) and lowest for scratches (86%). On the other side, only **71%** of clean cars are passed cleanly, so about 29% get an unnecessary flag. **Business meaning:** for renewals, the model is a good *recorder of existing damage*, protecting the insurer against a later claim for old damage. The cost is some extra follow-up for clean cars."""
R["«O76»"] = """to certify "≤ 2% complex among auto-settled" at 95% confidence, the **rule of three** requires **150 checked auto-settled claims even with zero errors**. If the true complex rate is 0.5%, about **250**; at 1%, about **600**; at 1.5%, about **2,150**. Our sample (≈ 147) is right at the edge, which is why the bound comes out at 2.0–2.1%. **Business meaning:** budget for ≥ 600 surveyor-checked auto-settled claims before declaring a rule safe, about 3 months of the current 20% sample."""
R["«O9»"] = """at the documented 80,000 simple-claim candidates a month and the chosen rule:
- **Auto-settled:** ≈ **4,300 claims a month** (5.4%), saving ≈ **₹0.65 crore** of surveyor visits (₹1,500 each) and ≈ **11,000 customer-days** of waiting.
- **Leakage:** none measured (0 complex claims found); the upper bound would be ≈ ₹3.5 crore/month if 2% were complex, which is why certification matters.
- **Net benefit ≈ ₹0.7 crore/month** (cost-estimate bias adds a small under-payment of ≈ ₹0.07 crore).
- **The documented ambition of auto-settling "over 80,000 simple claims a month" is far away** at this accuracy: even the loosest tested rule covers about one-third of claims and fails the safety limit.
- **Renewals** are a separate, cleaner win: pre-existing damage is recorded for 94% of damaged cars without a surveyor visit (₹1,500 saved per renewal)."""
R["«O10»"] = """**Decision against the pre-registered criteria:**
- **Criterion 1 (≤ 2% complex among auto-settled):** point estimate ✅ (0%), but the **95% upper bound is 2.02%** → ❌ not yet certified.
- **Criterion 2 (cost within ±₹3,000):** ❌ population (55%); ✅ within the tight slice (90.5%).
- **Criterion 3 (renewals ≥ 90% detection):** ✅ 94.4% (CI 92.2–96.0%).

**I recommend:**
1. **Launch for break-in renewals now.** The model meets the 90% target and records existing damage.
2. **Auto-settle only the tight rule** (≤ ₹20,000; no structural dent; confidence ≥ 0.7; quality ≥ 0.4), **after** extending the surveyor validation to ≥ 600 auto-settled claims to certify the 2% bound. Until then, route it as "fast-track surveyor review".
3. **Fix the dent problem first:** add an angled-photo prompt for possible dents and retrain on more labelled dents. This is the biggest lever on both coverage and cost accuracy.
4. **Keep the random 20% surveyor sample** and re-run this validation monthly (new car models, seasons, phones).
5. **Fraud controls:** EXIF/time/location checks and duplicate-image hashing; give customers the right to ask for a physical survey.

**KPIs:** complex-claim rate among auto-settled (with upper bound); cost-estimate error within ±₹3,000; damage detection at renewals; dent sensitivity; retake rate; auto-settled share; days to settlement."""

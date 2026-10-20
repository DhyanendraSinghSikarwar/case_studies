R = {}
R["«EXEC»"] = """*(Synthetic data built on BharatPe's documented design; BharatPe disclosed only the turnaround gain. Written after the analysis.)*

- **The question:** how much should each merchant be offered automatically, based on their QR payments, and when can the KYC-vs-bank-account name check be passed without a human?
- **Size loans by repayment burden, not by turnover.** Default rises steadily with the daily instalment as a share of daily QR inflow: from **3.6% when it is under 6% to 31% when it is over 30%** (trend p ≈ 1e-100).
  - The legacy rule ("lend one month's QR inflow") gives most merchants an instalment of ~19% of their daily takings.
  - **Capping the instalment at 10% of forecast daily inflow, with risk tiers (12/10/7%/no offer),** halves default (13.7% → 6.0%) and raises profit by **₹1,593 per merchant** (CI ₹1,324–1,886): about **₹16 crore per lakh merchants** per loan cycle, while lending half as much.
- **Forecasting:**
  - Gradient boosting forecasts next-quarter QR inflow better than "last-3-month average" (median error 9.3% vs 10.8%; Diebold–Mariano p ≈ 1e-146).
  - A conservative P20 forecast is honest about uncertainty: it is beaten 78.5% of the time, vs 80% intended.
  - **No forecast foresees a business shock.** For the 6% of merchants whose sales collapse, every forecast overshoots by 77–88%, so daily repayment monitoring is still needed.
- **Name matching:** exact matching (even after cleaning) auto-accepts only **54% of genuine merchants**. A hybrid matcher (word-set + Jaro–Winkler + initials) auto-accepts **83%** with a false-accept rate of **0.05%** (≤ 0.5% target), and is the cheapest option (≈ ₹84 lakh per lakh disbursals vs ₹208 lakh for exact, counting reviews and drop-outs). The popular token-set ratio scores 35 impostor pairs as perfect matches (e.g., "Ramesh Kumar Sharma" vs "Ramesh Sharma"), so it cannot be used to auto-accept.
- **"Five seconds" is achievable for two-thirds of merchants:** 66.8% clear both the limit and the name check automatically. The rest go to name review (28%) or receive no offer (5%).
- **I recommend:**
  - Replace turnover-multiple limits with a burden cap on a forecast, risk-tiered by a default model (AUC 0.71 vs 0.67 for burden alone).
  - Auto-accept names with the hybrid matcher and send the rest to review, never to auto-rejection.
  - Pair the limit with daily EDI monitoring and automatic restructuring when inflow drops."""
R["«O5»"] = """we removed **1,200 duplicate merchant-month rows**, filled **901 missing monthly QR values** by interpolating from neighbouring months (settlement-file gaps, not zero sales; treating them as ₹0 would wrongly cut limits), and flagged **150 blank bank-account names** (penny-drop API failures) for manual review. All 40,000 merchants have 15 months. Clean: **600,000 merchant-months**, median monthly QR ≈ ₹97,000. Merchants are split 50/50 into model-building and test halves."""
R["«O61»"] = """**left:** six merchants show what the forecast must cope with: steady growers, seasonal swings (apparel peaks around festivals) and occasional collapses after month 12, which no history predicts. **Right:** on the 12,000 legacy loans, the default rate rises with the **repayment burden** (EDI as a share of recent daily QR inflow) from a few percent at low burdens to above 30% when the instalment takes over a quarter of daily takings. This one chart is the case for burden-based limits."""
R["«O71»"] = """
- **The model beats the naive forecast:** median absolute error **9.3% vs 10.8%**, mean absolute log error 0.160 vs 0.175, and the **Diebold–Mariano test** confirms the difference (z = 25.8, p ≈ 1e-146). Adding a simple trend to the naive forecast closes part of the gap (9.6%).
- **The P20 forecast** is beaten by actual inflow for **78.5%** of merchants. That is slightly below the intended 80% and significant at this sample size (p ≈ 2e-7), but close. Its pinball loss (0.068) beats a naive "80% of the recent average" (0.082). It is a calibrated conservative number.
- **Shocks are unforecastable:** for the 6% of merchants whose business collapses after month 12, the naive forecast overestimates future inflow by **88%** and even P20 by **77%**.
- **(f) Business meaning:** forecasting improves sizing at the margin, but **post-disbursal daily monitoring** (pausing or restructuring the EDI when settlements drop) is what protects against shocks."""
R["«O72»"] = """
- **Default rises steadily with the ex-ante burden:** 3.6% (burden < 6%), 5.9% (6–8%), 7.8–8.0% (8–12%), 9.8% (12–15%), 13.1% (15–20%), 16.6% (20–25%), 24.1% (25–30%), **30.8% (> 30%)**. The **Cochran–Armitage trend** is overwhelming (z = 21.3, p ≈ 1e-100).
- **There is no sharp "cliff" at 10% in the data:** the hinge term is not significant (p = 0.16), so the risk climbs smoothly. A 10% cap is therefore a *business* choice on a smooth curve, not a natural threshold.
- **Volatility matters on top of burden:** each +0.1 in month-to-month volatility multiplies default odds by **1.17** (p ≈ 1e-43), so the same instalment is riskier for a restaurant than for a pharmacy.
- **(f) Business meaning:** limits should be set so the instalment is a modest share of *forecast* daily inflow, with tighter caps for volatile businesses."""
R["«O73»"] = """on 6,040 test loans (867 defaults), the gradient-boosting default model reaches **AUC 0.713 vs 0.673 for burden alone** (+0.040, DeLong p ≈ 1e-4). After burden, the strongest single signals are **active days per month** (0.67, a falling count is an early sign of trouble) and the **unique-payer ratio** (0.57, a diverse customer base is healthier and harder to fake). Raw turnover itself is weak (≈ 0.56): **how much a merchant sells matters less than how much of it the loan takes and how steady it is**. The model is used for risk tiers in 7.4."""
R["«O74»"] = """on all 20,043 test-half merchants (digital twin):
- **Legacy (1 × monthly QR):** average loan ₹1.51 lakh, **13.7% default**, ₹4,652 profit per merchant.
- **EDI ≤ 10% of naive inflow:** half the loan size (₹81k), 7.1% default, **₹6,047** (+₹1,395, CI ₹1,175–1,635).
- **EDI ≤ 10% of P20 forecast:** ₹73k, 6.6% default, ₹5,830. It is *safer* but **less profitable** than the naive cap, because it is too conservative for most merchants.
- **P20 + risk tiers** (12% / 10% / 7% / no offer for the riskiest 5%): ₹78k, **6.0% default** (guardrail ✅), **₹6,245 per merchant (+₹1,593, CI ₹1,324–1,886 vs legacy)**, the best.

**(f) Business meaning:** the legacy rule over-lends. Most of the gain comes from capping the burden at all; risk tiering adds the rest by lending more to safe merchants and nothing to the riskiest 5%. Real-world validation needs a randomised limit test, because this comparison uses the simulation's true default function."""
R["«O75»"] = """
- **Exact matching after normalisation** (lower case, honorifics and punctuation removed) auto-accepts only **53.6%** of genuine pairs: it fails on every initial, word-order swap and spelling variant. AUC 0.77.
- **Token-sort ratio** handles word order and most typos (AUC 0.973; 78% auto-accepted at a 0.48% false-accept rate), but not initials.
- **Token-set ratio** (FuzzyWuzzy's popular choice) has a high AUC (0.972) but **cannot be used to auto-accept**: it gives a perfect 100 to **35 impostor pairs** where one name's words are a subset of the other's ("Ramesh Kumar Sharma" vs "Ramesh Sharma"). No threshold meets the 0.5% false-accept limit.
- **The hybrid matcher** has the best AUC (**0.984**). It auto-accepts **82.7%** of genuine pairs at a **0.05%** false-accept rate (Wilson upper bound 0.17%), and handles initials (100%), order (100%), honorifics, spacing and most spelling variants (88%). It is weaker on typos (38%) than token-sort (91%).
- **Paired comparison:** exact vs hybrid auto-accept correctness differs overwhelmingly (McNemar χ² = 7,406).
- **Shop names in place of owner names** are never auto-accepted by any matcher. That is the right outcome, as they need human review.
- **Chart:** auto-accept rate by variant type for each matcher.

**Business meaning:** matcher choice changes how many merchants get "five-second" loans by **~30 points**. A combined score (hybrid + token-sort, or a small learned model) would add the typo coverage."""
R["«O76»"] = """combining both automatic gates, **66.8%** of test merchants (CI 66.2–67.5%) can be decided with **no human step**: offered a limit *and* their name auto-accepted. A further 28.1% are offered a limit but need a quick name review, and 5.0% get no offer (riskiest tier). With exact matching, only about 54% of genuine names would pass automatically. **Business meaning:** "two days to five seconds" is realistic for about two-thirds of merchants. The rest need minutes of review rather than days, as long as review queues are staffed for ~30% of applications."""
R["«O9»"] = """
- **Limits (per 1 lakh merchants offered, one 6-month cycle):** the legacy rule earns ≈ ₹46.5 crore; the burden cap on naive inflow ≈ ₹60.5 crore; **P20 + risk tiers ≈ ₹62.4 crore (+₹15.9 crore vs legacy)** while lending about half as much capital. That frees balance sheet for more merchants.
- **Name matching (per 1 lakh disbursals),** counting ₹40 per review, 5% of reviewed genuine merchants dropping out because of the delay, and 60% loss on a wrong-payee disbursal:

| Matcher | Cost (₹ lakh per lakh disbursals) | Share reviewed |
|---|---|---|
| Hybrid | ≈ **84** | 29.5% |
| Token-sort | ≈ 134 | — |
| Exact | ≈ 208 | 54% |
| Token-set | ≈ 438 | 100% |

- **Reading:** the larger ₹ lever is **burden-based sizing**; the matcher's value is mostly speed and conversion. All figures rest on the stated fee, LGD and drop-out assumptions."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** the model forecast beats naive (DM p ≈ 1e-146). The P20 coverage is 78.5%, slightly below 80% but usable.
- **H2 ✅:** default rises with burden (no sharp kink).
- **H3 ✅:** burden-based, risk-tiered limits beat legacy by +₹1,593 per merchant, with default 6.0% (guardrail ≤ 8% ✅).
- **H4 ✅:** the hybrid matcher beats exact (McNemar). False accepts 0.05% (target ≤ 0.5% ✅).

**I recommend:**
1. **Limit = what keeps the instalment ≤ 10–12% of forecast daily QR inflow**, risk-tiered by the default model (no offer for the riskiest ~5%), with tighter caps for volatile categories.
2. **Daily monitoring after disbursal:** if 7-day settlements fall by more than 40%, pause or stretch the EDI automatically, because no forecast sees shocks coming.
3. **Name check:** use the hybrid matcher for auto-accept (threshold ≈ 95), send everything else to a review queue sized for ~30% of applications, never auto-reject on name alone, and do not use token-set ratio for acceptance.
4. **Validate live:** run a randomised limit test (e.g., 8% / 10% / 12% burden caps) on new merchants to confirm the burden–default curve before full roll-out.
5. **Guard the data:** monitor payer diversity and round-tripping, so merchants cannot inflate QR inflow to raise limits.

**KPIs:** default and loss rate by burden band; profit per merchant offered; share of applications fully automated (target ≥ 65%); name-review queue time; false-accept incidents (wrong-payee disbursals); share of merchants restructured after a settlement drop."""

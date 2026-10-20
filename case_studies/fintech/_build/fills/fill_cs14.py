R = {}
R["«EXEC»"] = """*(Synthetic data built on Kissht's documented design; the source figures are inconsistent and come from RHP analyses. Written after the analysis.)*

- **The question:** should a digital lender run one credit model, a handful of segment models, or dozens of sub-models?
- **Risk drivers really do differ by segment** (likelihood-ratio test χ² = 1,168, p ≈ 1e-238):
  - The bureau score counts twice as much for thick files as for thin ones.
  - Bounced payments matter a lot for new-to-credit and thin-file borrowers, and not at all for thick files.
  - Income volatility matters 2–4× more for the self-employed.
- **But a single well-built global model captures most of that.** Out-of-time AUCs:

| Model | AUC |
|---|---|
| Bureau score alone | 0.678 |
| Global logistic | 0.847 |
| **Global gradient boosting** | **0.854** |
| **12 segmented logistic models** | **0.857** |
| 12 segmented gradient-boosting models | 0.834 (worse) |

  - The two best are statistically tied for business purposes: at a 3% bad-rate target they approve **86.2% vs 86.0%** of applicants, vs 84.9% for the global logistic.
- **Fragmentation backfires:** splitting into 2 → 12 segments helps a little (AUC 0.847 → 0.857). At 24 segments the gain flattens, and at **72 segments it is gone** (0.847), because the smallest segments have only 3–47 defaults to learn from. Kissht's "39 sub-models" is at the edge of what the data can support unless its book is far larger.
- **"5.17× vs 2.13×" is not a fair comparison on its own.** The top/bottom bad-rate ratio of the same model ranges from **36× (quintiles) to 70× (deciles) to infinity (ventiles)**. The bureau score's ratio nearly doubles when NTC borrowers, whom it cannot score, are excluded. Our best model's decile ratio is 2.9× the bureau's, in the same spirit as the documented 2.4×, but only meaningful with the bucket definition and population stated.
- **₹ impact (1 lakh applicants/month):**
  - The best models add ≈ **₹3.2 crore/year** of profit over the global logistic at the same 3% loss rate.
  - Compared with scoring on the bureau alone, any of the models is worth more than ₹100 crore/year, because the bureau cannot score 30% of applicants.
- **I recommend:** a **global gradient-boosting model plus a separate repeat-customer model** (2 models, not 39), or at most ~6–12 logistic segments where model-risk teams require scorecards. Validate every segment for events-per-variable ≥ 10, calibration and rank ordering. Report KS/Gini and approval-at-fixed-loss next to any top/bottom ratio."""
R["«O5»"] = """we removed **400 duplicate disbursal records**, converted **304 bureau scores coded −1** to missing with a "no-hit" flag (a −1 would otherwise look like an extremely bad score), and filled **2,410 missing incomes (2%)** with the employment-type median plus a missing flag. Segment logic is clean: no NTC borrower has a bureau score, and no new customer has prior-loan history. Clean data: **120,000 loans, bad rate 6.96%**, months 1–9 for training (100,052) and months 10–12 out-of-time (19,948), in 12 segments."""
R["«O61»"] = """**left:** bad rates differ hugely by segment: **16% for new-to-credit self-employed new customers vs 1.3% for thin-file salaried repeat customers**. Repeat customers are 4–8× safer in every bureau group. **Right:** among bureau-tested new customers, the bureau score ranks thick files much more steeply than thin files: the same score means less when based on one or two tradelines. Both patterns are the documented motivation for segment-specific underwriting."""
R["«O71»"] = """
- **The drivers clearly differ:** adding segment-specific slopes for six drivers improves the fit enormously (LR χ² = 1,168, df = 16, p ≈ 1e-238; AIC 34,192 → 33,055).
- **Bureau score** (log-odds per +60 points): about **−1.1 for thick files vs −0.6 for thin files**, so twice as informative for thick files.
- **Bounces:** about +0.9 log-odds per bounce for NTC, +0.6 for thin files, **≈ 0 for thick files**. Bank-statement data matters precisely where the bureau is silent.
- **Income volatility:** 1.4–1.7 for the self-employed vs 0.4–0.7 for the salaried.
- **(f) Business meaning:** H1 is rejected. One set of weights does not fit everyone, which justifies *some* segmentation. Whether separate *models* beat one flexible model is the next question."""
R["«O72»"] = """
- **The bureau score alone is weak overall** (AUC 0.678, KS 0.28), mainly because it cannot rank the 30% of applicants who are new to credit.
- **The global logistic** with segment dummies reaches **0.847**.
- **Global gradient boosting** (0.854, +0.007, Holm p = 0.0002) and **12 segmented logistic models** (0.857, +0.010, p < 0.0001) both improve on it significantly. Their gap to each other (0.002) is negligible.
- **12 segmented gradient-boosting models are significantly *worse*** (0.834, −0.013, p = 0.0007): each segment's trees over-fit too few defaults.
- **Top/bottom decile bad-rate ratios** are 24.5× for the bureau and 56–70× for the models, but with very wide bootstrap CIs (e.g., 42–174 for the best model), because the safest decile has very few defaults.
- **(f) Business meaning:** segmenting a *simple* model helps. Segmenting a *flexible* model hurts. A flexible global model gets the same benefit without twelve models to maintain."""
R["«O73»"] = """within segments (BH-adjusted), segmented logistic models help significantly in the two largest new-customer segments: **THICK|salaried (+0.021, q = 0.004)** and **NTC|salaried (+0.011, q = 0.016)**. They are not better elsewhere, and are *worse* for **NTC|salaried repeat** customers (−0.051, q = 0.087), a segment with only 97 training defaults. Segmented gradient boosting collapses there: **AUC 0.48, worse than random** (q = 0.0001). **Business meaning:** segment models earn their keep only in large segments with clearly different drivers. Small segments should borrow strength from a pooled model."""
R["«O74»"] = """AUC rises from **0.847 (1 model) to 0.850 (2) and 0.855 (3–6), peaks at 0.857 with 12 segments**, then falls to 0.855 (24) and back to **0.847 with 72 segments**. The bootstrap CIs overlap throughout, so the gains of segmentation are modest even at the peak. The decline is explained by **events per variable**: at 12 segments the smallest has 47 training defaults (EPV 2.0, with 6 segments below the EPV ≥ 10 rule), and at 72 segments the smallest has **3 defaults** and 66 of 72 segments are below the rule. Log loss tells the same story (best 0.179 at 12). **Business meaning:** the right number of sub-models depends on **defaults per segment, not customer types**. With this book's ~7,000 training defaults, about 6–12 segments is the ceiling; "39" would need a book several times larger."""
R["«O75»"] = """for the same best model, the top/bottom ratio is **36× with quintiles, 70× with deciles and infinite with ventiles** (the safest twentieth had no defaults among bureau-tested loans). The bureau score's decile ratio is **24.5× on all loans but 43× on bureau-tested loans only**: excluding the NTC applicants it cannot score flatters it. So "5.17× vs 2.13×" depends entirely on how many buckets were used and who was included. The documented numbers are plausible for coarse buckets but **cannot be compared with each other, or with other lenders, without the definition**. **Business meaning:** report a top/bottom ratio only with its bucket count and population, and always alongside Gini/KS and approval rate at a fixed loss rate."""
R["«O76»"] = """both models are well calibrated within segments: **no segment shows a Holm-significant gap** between predicted and observed bad rates. The mean absolute error is **0.51 pp for the global logistic vs 0.42 pp for the segmented model**, both under the 1 pp guardrail. The global model over-predicts the small **repeat** segments by about 1.1–1.3 pp (unadjusted p ≈ 0.03), which would slightly *under-approve* good repeat customers. The segmented model halves that error. **Business meaning:** calibration is a modest but real benefit of segment-level models for small, very safe segments, or a reason to recalibrate a global model per segment."""
R["«O77»"] = """
- **Rank ordering is strong:** the bad rate rises from 0.5% in the safest decile to **35.2% in the riskiest** (Cochran–Armitage z = 42.6). There is **one small reversal** at the very top (decile 2 at 0.80% vs decile 3 at 0.65%), within noise at 10–16 defaults each.
- **Stability:** the repeat-customer share grows from 26.8% to 32.4%, but the score's **PSI is only 0.003** overall (and ≤ 0.002 within new and repeat customers), well under the 0.1 warning level. The model is scored on a population it knows; the mix shift changes the portfolio bad rate, not the score's validity."""
R["«O9»"] = """at a portfolio bad-rate target of **3%**:
- **Approval rates:** global logistic **84.9%**; global gradient boosting **86.2%** (+1.3 pp); segmented logistic **86.0%** (+1.1 pp); segmented gradient boosting only 83.5% (−1.4 pp); **bureau score alone 40.8%**.
- **₹ value (per 1 lakh applicants a month):** the two best models earn ≈ **₹3.2 crore/year more** than the global logistic at the same loss rate. Over-segmented boosting would lose ≈ ₹3.5 crore/year. Relying on the bureau alone would forgo ≈ **₹115 crore/year**, mostly by declining NTC applicants it cannot score.
- **Reading:** the real ₹ comes from **using bank-statement and segment information at all**. The choice between "1 flexible model" and "12 simple ones" is worth little in ₹, but a lot in maintenance and validation cost.
- Assumptions: ₹2,800 margin per good loan, 75% LGD; booked-loan data are used as a proxy for applicants."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** drivers differ by segment.
- **H2 ✅:** segmented logistic and global boosting both beat the global logistic, and tie each other; segmented boosting is worse.
- **H3:** past ~12 segments performance declines.
- **H4 ✅:** calibration is acceptable for both.
- **Guardrail met:** calibration error ≤ 1 pp per segment.

**I recommend:**
1. **Production model:** one **global gradient-boosting model** with segment variables (bureau depth, employment, repeat), **plus a separate repeat-customer model** driven by the lender's own repayment history. That is 2 models instead of 39, with equal ranking power.
2. **If model risk requires scorecards:** use **6–12 logistic segments at most**, merging any segment with fewer than ~10 defaults per parameter into its parent.
3. **Calibrate per segment:** monitor predicted vs observed bad rate by segment monthly, and recalibrate the global model for small safe segments (repeat customers).
4. **Report properly:** Gini/KS and approval rate at a fixed loss rate. Quote any top/bottom ratio only with its bucket count and population.
5. **Never rely on the bureau alone** for NTC/thin files: bank-statement features (bounces, balances) are where the information is.

**KPIs:** out-of-time Gini per segment; approval rate at target loss; calibration error per segment; PSI per segment; number of segments below EPV 10; share of offers within 10 minutes (documented ≈ 85%)."""

R = {}
R["«EXEC»"] = """*(Synthetic narrations in real Indian bank formats; YES Bank disclosed no accuracy figure. Written after the analysis.)*

- **The question:** can a model read the *purpose* of a payment from a messy bank narration well enough to drive cross-sell, and is it worth it?
- **A learned model is far better than the usual rule list.** On an audited test set of 9,600 transactions:

| Model | Accuracy | Macro-F1 |
|---|---|---|
| Analyst keyword rules | 55.0% | 0.517 |
| **Character n-gram TF-IDF + logistic regression** | **93.5%** | **0.935** (CI 0.930–0.940) |
| Neural network (MLP) | 92.1% | 0.918 |

  All differences are significant (McNemar, Holm). **The simple logistic model is slightly *better* than the neural network** (174 vs 32 transactions only one gets right). It also trains faster and can be explained: its top n-grams for rent are "rent", "rnt" and "kiraya"-type fragments.
- **Where it struggles:** everyday spending that overlaps (fuel ↔ groceries at petrol-pump shops, dining ↔ online shopping, utilities ↔ online shopping). Every purpose still scores F1 0.90–0.96. Rare classes such as school fees are as good as common ones.
- **Labels needed:** macro-F1 reaches 0.84 with 1,000 labels, 0.91 with 5,000 and 0.935 with 29,000, so the last 20,000 labels buy only 2.5 points. About 5% label noise costs ≈ 0.6 points (0.935 vs 0.941 with clean labels, McNemar p < 0.0001).
- **Abstention works:** labelling only transactions with confidence ≥ 0.6 covers **90%** of the volume at **99.0% accuracy**; ≥ 0.8 covers 84% at 99.8%.
- **Does it pay off? For home loans, yes; for education loans, not demonstrated here.**
  - **Home loans:** inferred rent share lifts AUC from 0.54 to **0.68** (DeLong p ≈ 0) and doubles the share of loan takers captured in the top decile (12% → 23%). Inferred renters are identified with 100% precision and 91.5% recall.
  - **Education loans:** the school-fee signal does not help in this sample (top-decile capture 10.9% → 9.4%). Only 64 takers are in the test half, so this is underpowered rather than disproved.
- **₹ impact (10 lakh customers, a home-loan campaign to the top decile):** the life-event features reach ≈ **3,000 more home-loan takers, ≈ ₹18 crore of margin** for the same ₹0.4 crore campaign cost. The education-loan campaign shows no gain.
- **I recommend:**
  - Deploy the logistic model with an abstention threshold of ≈ 0.6.
  - Feed rent and EMI shares into home-loan targeting.
  - Re-test the education-loan signal on a larger sample.
  - Keep sensitive inferences (medical, family) for service use only unless the customer opts in."""
R["«O5»"] = """we removed **400 duplicate transactions** and handled **302 blank narrations** (a legacy core-system gap) as "unknown": they are never guessed. A senior's re-label audit of 500 hand-labelled rows finds **4.0% label errors** (Wilson 2.6–6.1%, consistent with the 5% built in), so the training labels are noisy but usable. Clean: **240,322 transactions**: 28,698 labelled (noisy), **9,607 audited (clean) for testing**, and 201,978 unlabelled."""
R["«O61»"] = """**left:** purposes are heavily imbalanced: groceries (≈ 1,900 in the test set) and online shopping and dining (> 1,000 each) dominate, while school fees (115) and medical (286) are rare, which is why macro-F1, not accuracy, is the primary metric. **Right:** the payment rail helps but does not decide: NACH is almost all EMI, SIP and insurance; POS is mostly groceries and fuel; UPI is spread across everything, so UPI narrations need the text."""
R["«O71»"] = """
- **Keyword rules score only 55.0% accuracy (macro-F1 0.52)**: they miss Hinglish, abbreviations ("rnt"), typos and generic remarks, and fall back to a guess.
- **Character n-gram logistic regression: 93.5% accuracy, macro-F1 0.935 (CI 0.930–0.940).** The MLP: 92.1% / 0.918, **lower** than the logistic model (Holm-adjusted McNemar p < 0.0001; 174 transactions only logistic gets right vs 32 only the MLP).
- **(f) Business meaning:** the leap comes from character n-grams, not from a neural network. A simple, explainable model is the better engineering choice here."""
R["«O72»"] = """every purpose reaches F1 0.90–0.96 under the logistic model (lowest: online shopping 0.904, travel 0.914; highest: groceries 0.963), compared with 0.25–0.82 for the keyword rules (school fees 0.25, family transfers 0.26). The **main confusions are between neighbouring everyday categories**: fuel → groceries (58), online shopping → dining (50), utilities → online shopping (46), groceries → fuel (46). These arise where a narration carries only a merchant name or a generic remark ("payment"). **Business meaning:** the weak spots are low-stakes (spending categories), not the high-value life events, where F1 is 0.94–0.95 (rent, EMI, SIP)."""
R["«O73»"] = """macro-F1 on the audited set rises quickly and then flattens: **0.75 (500 labels), 0.84 (1,000), 0.89 (2,500), 0.91 (5,000), 0.93 (10,000), 0.932 (20,000), 0.935 (all 28,698)**. The first 5,000 labels buy 16 points; the last 20,000 buy 2.5. **Business meaning:** a labelling budget of ≈ 5,000–10,000 transactions captures most of the value. After that, spend effort on audits and new classes rather than more labels."""
R["«O74»"] = """training on the noisy hand labels instead of the true labels costs about **0.6 points of macro-F1** (0.935 vs 0.941; accuracy 93.5% vs 94.1%; McNemar p < 0.0001). A statistically significant but small loss: the model is fairly robust to 5% random label noise. A different lesson is in the wording of the check: scoring against the noisy labels (even in-sample) gives 91.3%, which is a *distorted* figure because ≈ 5% of those labels are wrong. **Always evaluate on a small audited set.**"""
R["«O75»"] = """the logistic model's confidence is reasonably but not perfectly calibrated (**ECE = 0.062**). Abstention is very effective: labelling only transactions with confidence **≥ 0.6** covers **90.1%** of volume at **99.0% accuracy** (CI 98.8–99.2%); **≥ 0.8** covers 83.6% at **99.8%**; **≥ 0.4** covers 94.4% at 97.4%. **Business meaning:** downstream products need reliable labels more than complete ones. Marking 10% of transactions "unknown" raises label accuracy from 93.5% to 99%."""
R["«O76»"] = """**Home loans (✓):** the inferred rent and EMI shares lift AUC from **0.537 to 0.679 (+0.142; DeLong Holm p < 0.0001)** and raise the share of home-loan takers found in the top decile from **12.3% to 22.8%**. The inferred renter flag is **100% precise** (recall 91.5%). **Education loans (✗ not shown):** AUC changes by only +0.009 and the top-decile capture *falls* (10.9% → 9.4%). Only **64 education-loan takers** fall in the test half (and the base-model AUC of 0.46 is below chance), so the sample is too small to judge. **Business meaning:** transaction purposes carry a real, usable life-event signal for home loans. For education loans we need many more customers (or a longer window) before concluding anything."""
R["«O8»"] = """the highest-weight character n-grams are interpretable: **rent** → "rent", "rnt"; **school fees** → "fee", "dps", "ee-"; **family transfer** → "maa", "/maa/", "hai"; **salary to self** → "self", "sel", "lf". This explainability is a practical advantage of the logistic model: when a customer or auditor asks "why was this labelled rent?", the answer is a short list of fragments."""
R["«O9»"] = """for **10 lakh customers** and a campaign to the **top 10%** (₹40 per customer contacted = ₹0.4 crore, the same with or without life-event features):

| Campaign | Loan takers | Reached without life events | Reached with life events | Extra reached | Extra margin |
|---|---|---|---|---|---|
| Home loan (₹60,000 margin) | ≈ 28,250 | ≈ 3,470 | ≈ 6,440 | **≈ +2,970** | **≈ ₹17.8 crore** |
| Education loan (₹25,000 margin) | ≈ 16,500 | ≈ 1,800 | ≈ 1,550 | −260 | −₹0.6 crore (not significant) |

- **Reading:** a home-loan campaign guided by rent and EMI signals is worth ≈ ₹18 crore against a ₹0.4 crore cost. The education signal is unproven. The accuracy of the classifier matters because of what it enables, not for its own sake."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** the learned model beats keyword rules (macro-F1 0.935 vs 0.517).
- **H2 ✅ (opposite to the documented choice):** the logistic model beats the neural network, so no case for the neural network here.
- **H3:** home loans ✅ (AUC +0.142); education loans ❌ (underpowered).

**I recommend:**
1. **Deploy the character n-gram logistic model** with an abstention threshold of ≈ 0.6 (≈ 90% coverage at 99% accuracy). Use "unknown" rather than guessing for the rest.
2. **Feed rent, EMI and SIP shares into home-loan and wealth targeting** and measure with a randomised campaign.
3. **Budget ≈ 5,000–10,000 labelled transactions,** then fund quarterly audits (≈ 500 re-labelled rows) and new classes as UPI/biller formats change.
4. **Re-test education-loan life events** on a larger sample or window before building campaigns around them.
5. **Privacy:** treat medical, family-transfer and school-fee inferences as sensitive (DPDP Act): consent for marketing use, purpose limitation, retention limits.

**KPIs:** audited macro-F1 and per-class F1; label error rate in audits; coverage and accuracy at the abstention threshold; unknown-share by rail; campaign lift (top-decile capture) vs control; opt-out and complaint rates."""

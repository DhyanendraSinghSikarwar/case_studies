R = {}
R["«EXEC»"] = """*(Synthetic data calibrated to RBIH MuleHunter.AI's documented design; RBI disclosed only precision figures. Written after the analysis.)*

- **The question:** should banks use one shared, typology-based model for mule accounts instead of their own rules or models, and what does "90% positive alerts" really mean?
- **Rules drown investigators.** The legacy bank rules flag 6,662 of 144,000 accounts with **4.7% precision** (95% false alarms, worse than the documented "80% false positives"). Most single typology rules are also imprecise when used alone; the "many senders" rule mostly flags genuine traders (2.2% precision).
- **Typology-first design works.** Adding 9 expert typology features to raw account data raises AUC from 0.900 to **0.962** (DeLong p ≈ 1e-60). Precision of the top 500 alerts rises from 75% to **96%**.
- **Pooling across banks beats each bank's own model in 6 of 6 banks** (sign test p = 0.016; PR-AUC +0.08 to +0.20). **A bank that joins with no labels at all** gets *higher* precision from a model trained on the other five banks than from its own labels: +4 to +25 pp. This is the strongest argument for a central model like MuleHunter.
- **"90% precision" is true only at low volume.** The top 500 alerts (0.35% of accounts) are 96% precise but catch only 29% of mules. At 1% of accounts precision falls to 64%. A precision figure means nothing without the alert volume.
  - Precision measured against *confirmed* labels understates it by ~15 pp, because 15% of mules are never confirmed.
  - **A random audit of 139 alerts** verifies the claim within ±5 pp.
- **Limits:**
  - The model largely misses a **typology it has never seen**: recall falls 20–48 pp, and single-pattern mules of an unseen type are almost all missed.
  - It catches only **32% of low-intensity "sleeper" mules** (vs 72% of active ones).
- **₹ (scaled to 10 crore accounts, per 90 days):**
  - At the rules' alert volume, the model catches **4.3× more mules** and stops ≈ ₹850 crore of mule inflow vs ₹196 crore.
  - At the 90%-precision operating point it uses 0.3% of the rules' wasted investigator time (₹0.6 crore vs ₹198 crore) and still stops more (₹300 crore).
- **I recommend:**
  - Adopt the pooled typology model and choose the alert volume per bank by investigator capacity.
  - Verify precision quarterly with random audits.
  - Keep growing the typology library jointly with banks and I4C, because new patterns are the model's blind spot."""
R["«O5»"] = """we removed **600 duplicate accounts** (PSB-B submitted a file twice), set **200 impossible night shares (> 1, a unit bug) to missing**, and filled **7,226 missing declared incomes (5%)** with the occupation median, keeping an "income missing" flag so the model can learn whether missingness itself is informative. There are no false confirmations, but **255 true mules (15%) were never confirmed**: the labels banks train on are incomplete. Clean: **144,000 accounts, 1,691 true mules (1.17%), 1,436 confirmed**. Mule prevalence ranges from 0.82% (Private-D) to 1.76% (SFB-E)."""
R["«O61»"] = """**left:** the typology mix differs across banks. Rural PSB-A's mules are dominated by **dormant-account reactivation, cash-out and income-gap** patterns; the urban private bank's by **pass-through and fan-in**; the late-joining RRB-F by **device churn and night activity**. **Right:** mules are drawn disproportionately from **students, homemakers, farmers and gig workers**, the "recruited" profile RBI describes. Occupation alone is a weak signal, since most of those people are genuine. Both facts matter: a single bank sees only part of the pattern library, which is the case for pooling (7.4)."""
R["«O71»"] = """
- **The documented claim holds:** mule transactions differ from genuine ones (KS D = 0.16, p ≈ 1e-163). **21.3% of mule transactions fall between 11 PM and 1 AM vs 5.6% for genuine accounts.** Per account, mules have a much higher late-night share (Mann–Whitney p ≈ 1e-188, rank-biserial 0.67, a large effect). The **modal hour for mules is midnight**, for genuine customers 1 PM.
- **A statistical warning:** the mule *circular mean* (21:14) is misleading. Mule activity is **bimodal** (a midnight cluster plus ordinary daytime use), so the average falls in between, and its concentration is low (R = 0.12 vs 0.43 for genuine). For multi-peaked clock data, report the mode and the share in a window, not the mean.
- **(f) Business meaning:** a night-activity feature is genuinely useful, but most mule transactions still happen in the day. It cannot be used alone."""
R["«O72»"] = """
- **Each typology rule is significant (all Holm p < 0.0001), but used alone most are poor alert generators.**
  - **Device/SIM churn** (precision 65%, lift 55) and **rapid pass-through** (43%, lift 36) are sharp but cover only 11–12% of mules each.
  - **Night activity** reaches 29% precision.
  - **"Many senders" (fan-in)** flags 10,620 accounts at **2.2% precision**: it mostly catches genuine traders.
- **"Any typology rule"** covers 64% of mules at 5.5% precision, roughly the same as the **legacy bank rules (4.7%, 95% false alarms, 19% coverage)**.
- The typology mix **differs significantly by bank** (χ² = 351, p ≈ 1e-54, Cramér's V = 0.15, small to moderate).
- **(f) Business meaning:** typologies are the right *ingredients* but the wrong *alert rules*. Their value comes from combining them in a model (7.3), where "many senders + pass-through + a student occupation" means something that "many senders" alone does not."""
R["«O73»"] = """
- **Typology features add a lot:** AUC **0.900 → 0.962** (+0.062, CI +0.055 to +0.069, DeLong p ≈ 2e-60). PR-AUC nearly doubles (0.37 → 0.64).
- **Precision at fixed alert volumes:**
  - **Top 250:** 95% → 99.6%.
  - **Top 500:** **75% → 96%** (+22 pp, CI +17 to +26).
  - **Top 1,000:** 52% → 79%.
  - **At the legacy rules' own volume (6,662):** 15% → 21%, recall 81%.
- **(f) Business meaning:** expert typologies are worth encoding. Raw aggregates alone cannot separate a genuine trader from a fan-in mule; pass-through speed and holding time can. This supports the documented "typology-first" approach."""
R["«O74»"] = """
- **The pooled model wins in all 6 banks** (sign test p = 0.016). PR-AUC improves by **+0.08 to +0.20** (every bootstrap CI excludes 0), and precision in each bank's top 0.5% rises by 3–21 pp. The largest gains are at **PSB-A (+18 pp)** and **Private-D (+22 pp)**, whose own mule mix covers fewer typologies.
- **Precision still varies by bank under the pooled model:** from 82% (PSB-A) to 99% (SFB-E), Cochran Q = 36.9, **I² = 86%**. Higher prevalence and more distinctive typologies make some banks easier.
- **(f) Business meaning:** pooling is valuable because each bank has only 150–380 confirmed mules. But one network-wide precision number hides large bank-to-bank differences, so each bank should monitor its own."""
R["«O75»"] = """
- **A bank never seen in training does very well.** The model trained on the other five banks reaches **AUC 0.96–0.98** and top-0.5% precision of **79–100%**. That is *higher* than the bank's own-label model in every case (+4 to +25 pp), so **H4 passes**. Five banks' typologies teach more than one bank's labels.
- **Calibration does not transfer perfectly.** Predicted mule rates (0.8–1.2%) track the *confirmed* rate, not the true rate (0.8–1.8%), because the model learned from incomplete labels.
- **(f) Business meaning:** a new bank should use **rankings** (top-k alerts) from day one, and recalibrate probabilities only after its own audit sample (7.7). This is how MuleHunter could scale from 6 to 26+ banks quickly."""
R["«O76»"] = """**this is the model's main blind spot.**
- When every mule with a given typology is removed from training, recall of those mules in the top 1% falls by **6–48 pp**. Fan-in (−48 pp), night activity (−40 pp) and pass-through (−36 pp) suffer most.
- Mules that show **only** the unseen typology are almost entirely missed (1–6% recall).
- The model still catches mixed-pattern mules through their *other* typologies.
- **(f) Business meaning:** the model generalises *within* known patterns but not to genuinely new ones. The documented growth of the library from 19 to 90 patterns is not a nicety: **new typologies must be added as they are discovered**, through a standing process with banks, I4C and FIU-IND."""
R["«O77»"] = """
- **Precision depends on volume.** It stays **≥ 90% up to about 500 alerts (0.35% of accounts)** at 29% recall. It falls to 79% at 1,000 alerts, 64% at 1,500 and 21% at the rules' volume, while recall rises from 6% to 81%.
- **Label noise understates precision.** Measured against *confirmed* labels, the top 500 look only **81%** precise vs **96%** in truth, because unconfirmed mules count as "false alarms".
- **Audit design:** an audit of **n = 139** randomly chosen alerts gives ±5 pp. Our simulated audit of the top 500 estimates **98.6% (Wilson 94.9–99.6%)**, consistent with the truth (96.4%).
- **(f) Business meaning:** "90 per cent positive alerts" should be quoted as "*90% precision at N alerts per month, verified by a random audit of 139 alerts*". Without the volume and the method, it cannot be compared with anything."""
R["«O78»"] = """at a 1% alert budget the model catches **72% of active mules but only 32% of sleepers** (z = 15.9, p ≈ 1e-57). Sleepers show the same typologies at about a third of the intensity, so their accounts look close to genuine. **Business meaning:** sleeper mules are the hardest and probably the most numerous in reality. They need longer observation windows (90 → 180 days), network signals (links to known mule clusters), or periodic re-scoring, rather than a lower threshold that would flood investigators."""
R["«O9»"] = """scaled to **10 crore accounts per 90 days** (assumptions: 45 minutes per investigation, ₹600 per investigator-hour, 30% of a month's mule inflow stopped by an early freeze; median mule inflow ≈ ₹29,900/month):

| Policy | Alerts | Precision | Mules caught | Wasted investigator cost | Mule inflow stopped |
|---|---|---|---|---|---|
| **Legacy rules** | 46 lakh | 4.7% | ≈ 2.2 lakh | ≈ 33 lakh hours ≈ **₹198 crore** | ≈ **₹196 crore** |
| **Model, same alert volume** | 46 lakh | 20.5% | ≈ **9.5 lakh (4.3×)** | ₹166 crore | ≈ **₹850 crore** |
| **Model at the ≥ 90% precision point** | 3.5 lakh | 96% | ≈ 3.3 lakh | **₹0.6 crore** | ≈ ₹300 crore |

- **Reading:** the right operating point is set by **investigator capacity**. With today's teams, the high-precision point catches more mules than the rules with almost no wasted effort. As capacity grows, raising the alert volume catches more.
- All ₹ figures rest on the stated assumptions, and mule counts on the simulated 1.17% prevalence."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** night activity is real, but bimodal.
- **H2 ✅:** typology features add AUC +0.062 and precision@500 +22 pp.
- **H3 ✅:** pooling wins in 6 of 6 banks.
- **H4 ✅:** a never-seen bank does *better* than with its own labels.
- **Limits:**
  - Unseen typologies are largely missed.
  - Sleepers are missed.
  - Precision without a stated volume is meaningless.

**I recommend:**
1. **Adopt the pooled, typology-based model** in place of legacy rules, including for banks with no labelled history. Use it as a **ranking**, with each bank choosing its alert volume from investigator capacity: start at the ≥ 90%-precision point (≈ 0.35% of accounts) and widen as capacity allows.
2. **Verify precision by audit:** each quarter, investigate a random sample of ~140 alerts per bank (and a small sample of non-alerts to estimate recall). Publish precision *with* the alert volume.
3. **Maintain the typology library as a programme:** a joint RBIH–bank–I4C process to add new patterns, retrain, and run a leave-one-typology-out check on each new one.
4. **Sleepers:** extend observation windows, add network links to known mule clusters, and re-score monthly.
5. **Customer protection:** an alert triggers enhanced due diligence, not an automatic freeze. Provide a fast appeal path for traders, farmers and gig workers (the hard negatives).

**KPIs:** audited alert precision at the operating volume (per bank); mules confirmed per investigator-day; recall estimated from non-alert audit samples; mule inflow frozen (₹); share of new typologies detected within 30 days of discovery; false-freeze complaints."""

R = {}
R["«EXEC»"] = """*(Synthetic data built on Cashfree RiskShield's documented design; Cashfree disclosed no impact numbers. Written after the analysis.)*

- **The question:** which of the seven signal families actually catch fraud, should allow/review/block thresholds differ by business line, and what is each worth in ₹?
- **Velocity counters are the workhorse.** "≥ 5 accounts on one IP in 24 h" and "≥ 5 payments from one device in 10 minutes" are right 99.6–99.9% of the time when they fire. Removing the velocity family costs the most: AUC 0.974 → 0.891. The right window depends on the attack: **10–60 minutes for card-testing bots, 7 days for promo abuse and stolen-card rings**.
- **A model beats hand-written rules on both sides of the trade-off.** Over the 3 test weeks, the hand rules cut fraud + friction cost from ₹25.8 lakh (allow everything) to ₹15.0 lakh, but **block 0.91% of genuine customers** (guardrail: 0.5%). The gradient-boosting score with cost-optimal thresholds reaches **₹8.7 lakh while blocking only 0.04%** of genuine customers.
- **Three documented ideas did *not* pay off here, which is useful to know:**
  - **Per-business-line thresholds** saved nothing over one global pair (−₹0.02 lakh, CI −0.21 to +0.13), because the model already uses the business line and amount.
  - **Weekly retraining** caught the same frauds as a static model while attack patterns were stable (64% vs 64%, p = 0.51).
  - An **unsupervised anomaly score** caught card-testing bots (83%) but almost none of a "never-seen" promo-abuse attack (8% vs 6%, p = 0.29).
- **What *did* pay off:**
  - A **trusted-customer allowlist** cuts genuine reviews by 25% with no extra fraud.
  - **As-of graph features** are essential. Built with hindsight they make the model look perfect (AUC 0.9999), a leak that would fail in production.
- **₹ impact (scaled to ≈ 15 lakh transactions/month):** the model + allowlist saves ≈ **₹2.5 crore/month vs allowing everything** and **≈ ₹96 lakh/month more than the hand rules**. Velocity is the most valuable family (≈ ₹1.1 crore/month if dropped). Every family earns its keep in ₹ terms.
- **I recommend:** replace hand rules with a cost-thresholded model (one global threshold pair, re-tuned monthly on matured labels), keep the velocity counters at attack-specific windows, add the trusted-customer allowlist, and treat a new attack as an analyst-written velocity rule first, since neither the model nor the anomaly score sees it."""
R["«O5»"] = """we removed **800 duplicate events** (payment retries that would double-count), dropped **150 negative-amount rows** (refunds mis-tagged as payments, which are not screening events), and kept the **2,797 transactions (1%) with no device ID** under an explicit "UNKNOWN_DEV" token so they cannot all link to each other in the graph. Labels are consistent: every fraud has a confirmation date after the transaction. Clean data: **279,189 transactions, 1.35% fraud** (card testing 1,774, stolen card 1,161, promo abuse 845). Gaming has the most fraud (1.9%), ed-tech the least (0.56%)."""
R["«O51»"] = """all features are built in 16 seconds and use only information available at transaction time.
- **The three attacks leave different fingerprints:**
  - **Card-testing** bots show ≈ 22 new cards per device in the last hour and run mostly from datacenter/VPN IPs (64%).
  - **Promo abusers** show ≈ 4 accounts per device in a week, clean residential IPs and 91% state mismatch.
  - **Stolen-card** fraud shows a moderate account-sharing signal and only 44% state mismatch (half use same-state proxies).
- **Label delay matters even here:** on day 28 only **1,434 of 1,893 training frauds (76%) are confirmed**. The rest are still-pending chargebacks the model treats as genuine.
- **A graph warning:** the "confirmed fraudsters in the component" counts are in the hundreds. Shared carrier IP blocks join most users into one **giant component**, which dilutes community features (7.1, 7.3)."""
R["«O61»"] = """
- **Left:** card testing lives at ₹1–₹500, promo abuse at a few hundred rupees, and stolen-card fraud sits above typical genuine tickets but **overlaps with them**. Amount alone cannot separate fraud.
- **Middle:** almost all genuine transactions come from devices with 1–2 accounts in a week (households give a small tail). Card-testing bots and promo abusers sit far out at 3–8+ accounts. That is the documented "> X distinct … within Y time" signal.
- **Right:** the fraud mix differs by line. Gaming attracts card testing and promo abuse, while ed-tech fraud is mostly stolen cards. That is why the documentation suggests line-specific rules (tested in 7.6)."""
R["«O71»"] = """all signals except amount are Holm-significant, but they play very different roles:
- **Velocity rules are near-certain when they fire:** "≥ 5 accounts on an IP in 24 h" (precision **99.9%**, lift 146, covers 50% of frauds) and "≥ 5 payments from a device in 10 min" (99.6%, covers 44%). They are safe to **block** on.
- "≥ 3 accounts on a device in 7 days" and "≥ 3 new cards on a device in 1 hour" cover more fraud (67% and 53%) at ≈ 50% precision. Use them to **review**.
- **Negative lists** are precise (52%) but cover only 19% of fraud, because lists only know yesterday's fraudsters.
- **Broad signals are weak alone:** IP-state ≠ card-state fires on 19% of all traffic (precision 5.8%), and disposable contact on 5.9% (precision 16%). Useful as model inputs, harmful as block rules.
- **Graph 1-hop links** to already-confirmed fraud cover only 7%, because most rings are caught after they finish.
- **Amount ≥ ₹5,000** shows no lift (0.86, Holm p = 0.16).

**(f) Business meaning:** the best block rules are velocity counters. Most other signals belong in a score, not in a rule."""
R["«O72»"] = """the best window depends on the attack:
- **Card testing:** 10-minute and 1-hour "new cards per device" counters are equally good (AUC 0.996 vs 0.997, DeLong p = 0.22), because bots work in bursts.
- **Stolen-card rings:** longer windows win: new cards per device over **24 h** (0.808 vs 0.740) and accounts per device over **7 days** (0.870 vs 0.745), both Holm p < 0.0001.
- **Promo abuse:** **7-day** accounts-per-device is best (0.965 vs 0.947, p < 0.0001), because abusers create accounts over days.

**Business meaning:** keep **several windows per counter** (10 min, 1 h, 24 h, 7 d). A single "Y" in the rule would miss either the bots or the slow attacks."""
R["«O73»"] = """the full model reaches **AUC 0.974, PR-AUC 0.81, 64% of frauds caught at a 1% alert budget**.
- **Velocity** is by far the most important family: dropping it costs −0.082 AUC (to 0.891) and −11 pp recall. Alone it already reaches 0.958.
- **Device intelligence** is second (−0.023 AUC, −7.5 pp recall).
- **Contact intelligence** (−0.007, Holm p = 0.044) and **negative lists** (−0.005, p = 0.006) add small but real value.
- **Geo/IP** (−0.003, p = 0.16) and **graph** (−0.0003, p = 0.86) add nothing *to AUC* on top of the others: their information overlaps with velocity and device signals. Their ₹ value at the decision thresholds is assessed separately in section 9.

**(f) Business meaning:** if budget is tight, build the velocity counters and device checks first."""
R["«O74»"] = """building graph flags with **hindsight** ("this device was *ever* used for fraud") makes the model look nearly perfect: **AUC 0.9999 vs 0.974** and recall@1% 74.5% vs 64.5% (DeLong p ≈ 1e-18). In hindsight, 98% of test frauds have a flagged entity, but only **52%** do at the moment of the transaction, because most chargebacks arrive weeks later. **This is the most common way fraud models fail in production.** RiskShield's "links to already-proven risky entities" must mean *proven before this transaction*, enforced by timestamped graph snapshots."""
R["«O75»"] = """
- **The Isolation Forest is a specialist, not a generalist.** It has a decent AUC (0.92) but catches only 32% of frauds at the 1% budget: **83% of card testing** (truly unusual bursts), but 0.5% of stolen cards and 0.8% of promo abuse. 57% of its alerts are genuine customers.
- **It is almost unrelated to the supervised score** (Spearman 0.01), which is why it is a different signal.
- **The "never-seen attack" test:** a supervised model trained *without* promo-abuse examples catches only **5.7%** of the promo abuse in the test weeks (vs 93.5% when trained with examples). Adding the anomaly score raises this only to **8.1%** (14 → 20 cases, exact McNemar p = 0.29).
- **Why:** each promo-abuse transaction looks ordinary (small amount, daytime, residential IP). The attack is visible only *collectively*, through accounts per device.

**(f) Business meaning:** anomaly scores catch noisy attacks like bots, not quiet collective ones. Detecting new collective attacks needs analysts watching velocity dashboards and writing new rules quickly, which feeds the documented feedback loop."""
R["«O76»"] = """
- **Allow everything:** ₹25.8 lakh of fraud loss over 3 test weeks.
- **Hand-written rule engine:** cuts the cost to ₹15.0 lakh, but **blocks 0.91% of genuine customers**, breaking the 0.5% guardrail.
- **Model + one global threshold pair** (review ≥ 0.002, block ≥ 0.10): **₹8.7 lakh**, blocking only **0.04%** of genuine customers and reviewing 3.4% of traffic.
- **Per-line thresholds** chose the same cut-offs for gaming and e-commerce and a lower block cut-off for ed-tech. They did **not** reduce cost: −₹0.02 lakh vs global, paired bootstrap CI −₹0.21 to +₹0.13 lakh. **We cannot reject H0.**
- **Why:** the model already uses business line and amount, and the cost of each decision already scales with the amount and the line's margin. Per-line tuning matters for *hand rules*, which have no such inputs, not for a cost-aware score.

**(f) Business meaning:** one well-chosen threshold pair is enough. Spend tuning effort on the cost inputs (margins, review cost), not on per-line cut-offs."""
R["«O77»"] = """**68.7%** of test traffic comes from trusted customers (≥ 3 earlier successful payments over ≥ 14 days), and **none** of the test frauds look trusted. The allowlist mostly removes **unnecessary reviews**: genuine customers reviewed fall from **3,100 to 2,339 (−25%)**, while genuine blocks barely move (61 → 59; exact p = 0.5) because the model already blocks very few. Frauds let through are unchanged (163), and total cost falls from ₹8.74 to **₹8.34 lakh (−4.5%)**. **Business meaning:** this is the documented "post-processing to cut false positives". Cheap, safe, and it frees a quarter of review capacity. It should be monitored, though: account-takeover fraudsters target exactly these trusted customers."""
R["«O78»"] = """
- **Weekly retraining did not help in this simulation:** pooled over weeks 4–8, the static model catches **64.2%** and the weekly-retrained one **63.7%** (132 vs 144 frauds caught by only one of them, exact McNemar p = 0.51). The weekly model is better in week 8 (62% vs 59%) but worse in week 6 (58% vs 62%).
- **Why:** the attack types here are stable over the 8 weeks, and retraining on "as-of" labels adds recent but immature labels: pending chargebacks look genuine.
- **Business meaning:** retraining on a schedule is not free accuracy. Its value comes when attacks *change* (7.5 shows how badly a model misses a pattern absent from training). Retrain when monitoring shows drift (new patterns, falling precision), and **use matured labels**."""
R["«O79»"] = """
- **The explainable logistic model** reaches AUC 0.891 (vs 0.974 for gradient boosting) and recall@1% 54% (vs 64%). Explainability costs about 10 points of recall, so use the tree model to decide and the linear model to explain.
- **Its reason codes make sense:** the top reason family is strongly tied to the true attack type (**Cramér's V = 0.54**, p ≈ 1e-182).
  - Card-testing alerts are explained by **velocity** (416 of 520).
  - Promo abuse is explained by contact, velocity and graph signals.
  - Stolen cards are explained by geo/IP and negative lists.
- **Genuine customers alerted by mistake** are mostly explained by **device** (new phone) or **contact** (disposable email) signals.
- **Business meaning:** reason codes tell analysts what to check, and they show which signals produce false alarms. That is where post-processing should focus."""
R["«O9»"] = """at **10× the simulated traffic (≈ 15 lakh transactions/month)**:
- **Savings vs allowing everything:** hand rules save **₹1.56 crore/month**; the model with cost-optimal thresholds saves **₹2.46 crore/month** (**+₹90 lakh/month vs the rules**); adding the trusted-customer allowlist saves **₹2.52 crore/month (+₹96 lakh vs rules)**.
- **Value of each family**, as the extra monthly cost if it is dropped (thresholds re-tuned, 95% bootstrap CI on the test transactions):

| Family | Extra cost if dropped (₹ lakh/month) | 95% CI |
|---|---|---|
| Velocity | 110 | 85–137 |
| Device | 58 | 42–74 |
| Graph | 46 | 27–68 |
| Contact | 34 | 13–54 |
| Geo/IP | 32 | 19–45 |
| Negative list | 24 | 9–39 |

- **Graph and geo/IP:** their ₹ value is real although their AUC contribution is nil (7.3). They help on the high-value stolen-card cases that dominate the cost, while AUC weights every fraud equally.
- **Caveat:** these intervals do not include threshold-tuning uncertainty, so treat the family ranking as firmer than the exact amounts.
- **Reading:** every family pays for itself, and velocity and device checks are the priorities."""
R["«O10»"] = """**Decision against the pre-registered hypotheses:**
- H1 ✅: all signals except amount lift fraud.
- H2: velocity, device, contact and negative lists add AUC ✅; geo/IP and graph do not add AUC ❌ but do add ₹ value.
- H3 ✅: hindsight graph features leak.
- **H4 ❌:** per-line thresholds give no saving.
- **H5 ❌:** weekly retraining makes no difference under stable attacks.
- Guardrail: the model passes (0.04% genuine blocked); the hand rules fail (0.91%).

**I recommend:**
1. **Replace the hand rule engine with a cost-thresholded score** (gradient boosting on all seven families). Keep velocity "kill rules" (≥ 5 accounts per IP in 24 h; ≥ 5 payments per device in 10 min) as hard blocks for latency and transparency.
2. **Use one global allow/review/block threshold pair**, re-tuned **monthly on a matured cohort** (chargebacks arrive 10–60 days late), with merchant-specific margins in the cost model rather than per-line cut-offs.
3. **Build velocity counters at several windows** (10 min, 1 h, 24 h, 7 d) per device, IP and card. They are the most valuable features.
4. **Graph:** use only timestamped, as-of links. Exclude hub nodes (carrier IP blocks, placeholder device IDs) so the graph does not collapse into one giant component.
5. **Add the trusted-customer allowlist** (−25% genuine reviews), and monitor account takeover on trusted accounts.
6. **New attacks:** an analyst-owned velocity dashboard plus a fast rule-deployment path, because neither the supervised model nor the anomaly score catches a quiet new collective pattern. Retrain when drift is detected, not just on the calendar.

**KPIs:** fraud loss per ₹100 GMV; genuine-customer block rate (≤ 0.5% per line); review rate and review hit rate; recall at a fixed alert volume on matured labels; share of alerts with a reason code; time from new-pattern detection to deployed rule."""

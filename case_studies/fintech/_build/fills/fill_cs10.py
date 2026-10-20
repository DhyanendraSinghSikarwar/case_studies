R = {}
R["«EXEC»"] = """*(Synthetic data built on Simpl's documented design; Simpl disclosed no numbers. Written after the analysis.)*

- **The question:** can linking new BNPL users by shared phones, addresses, bank accounts and email patterns stop fraud rings at onboarding, without declining genuine families and hostel residents?
- **Yes. The links carry the signal, and the simplest link features capture most of it.** Defaulters cluster far more than chance (45% vs 9%, permutation p = 0.002), and that clustering is driven by fraud, not by genuine credit stress. Adding "how many earlier users share this device / address / bank account / email pattern" lifts fraud recall at a 1% decline budget from **2% to 51%** (AUC 0.73 → 0.83, p < 0.0001), and ring-member recall to **84%**. Full multi-hop **communities add little on top** (AUC +0.009, p = 0.19).
- **The graph must be built carefully or it punishes good users.**
  - Without pruning, **12.9% of genuine users** land in "suspicious" communities of 4+ (one has 2,394 people).
  - Dropping attributes shared by more than 10 users (hostels, offices) cuts that to **4.8%** while keeping **98%** of ring members.
  - A placeholder device ID from an old SDK, left uncleaned, would have glued 9,042 users together.
- **Where to draw the line:** total cost (fraud + credit loss + ₹1,200 lifetime value per wrongly declined good user) is lowest when declining the riskiest **0.5% of applicants**: half of all fraudsters stopped, almost no good users declined, ≈ **₹0.8 crore/month saved at 5 lakh sign-ups**. Declining more than 2% *costs* money.
- **Other findings:**
  - Real-time (hourly) graph updates beat a nightly batch only for rings signing up the same day (90% vs 84% caught); overall the difference is not significant (p = 0.36).
  - Training on **confirmed fraud** instead of first-payment default improves AUC by +0.05 (p ≈ 3e-9).
  - First-week spending behaviour is the strongest signal of all (AUC 0.99), but it arrives after the bust-out.
- **I recommend:** at onboarding, decline (or give a ₹500 starter limit to) the top 0.5% by a model with hub-pruned link counts. Keep community features as an investigation tool. Label defaulters as fraud vs credit stress. Watch the decline rate in shared-address communities as a fairness guardrail."""
R["«O5»"] = """we removed **500 duplicate onboarding events** and, most importantly, **1,509 placeholder device IDs ("00000000")** sent by an old SDK. Left in, that single fake "device" glues **9,042 unrelated users into one community** (vs 2,394 after cleaning). A data bug would masquerade as a giant fraud ring. 1,208 missing addresses are left missing (no link is better than a false link). Clean data: **120,000 users, 0.98% fraud** (710 ring members in 70 rings + 465 lone fraudsters). **FPD is 3.89%, but only 22% of FPDs are fraud.** The label the lender sees is mostly genuine credit stress."""
R["«O61»"] = """
- **Left:** genuine users mostly sit alone or in small family groups (size 1–3); ring members sit in communities of **4–27**. Size alone is not enough, since some genuine hostel and family groups are that big too.
- **Middle:** fraud uses newer SIMs, but 15% of genuine users also have new numbers, so SIM age is a weak signal on its own.
- **Right:** the bust-out signature: ring members spend **75–100% of their limit in the first week**, while genuine users typically spend 10–40%. That signal arrives too late to stop the first loss. It is useful for limits and collections, not onboarding."""
R["«O71»"] = """among defaulters who share a community with someone, **45.2%** have another defaulter in the same community, vs **9.1%** when default labels are shuffled at random (95th percentile 11.1%; permutation p = 0.002, the minimum possible with 500 shuffles). For **genuine credit-stress defaults alone** the figure is only 4.3%, *below* chance. **(f) Business meaning:** the graph carries real signal, and it is fraud signal. Ordinary repayment trouble does not cluster, so community features will not penalise genuine customers just for knowing someone who struggles to repay."""
R["«O72»"] = """
- **Without pruning**, 98.6% of ring members are in communities of 4+, but so are **12.9% of genuine users (15,296 people)**, and the largest "community" has 2,394 members.
- **Dropping attributes shared by more than 10 users** keeps **97.6%** of ring members and cuts collateral to **4.8%** (5,670 genuine users; CI 4.65–4.89%). The largest community shrinks to 27.
- **Pruning harder (D ≤ 5)** starts losing rings: only 66% are captured at D = 5 and 13% at D = 3, because gangs re-use one device or address across 5–10 accounts.
- Ring purity (the share of a ring member's community-mates who are also fraud) stays at 94–97%.

**(f) Business meaning:** pruning is the single most important design choice. D ≈ 8–10 is the sweet spot here; in production, tune D on investigated cases."""
R["«O73»"] = """building features from the graph *as it existed when each applicant signed up* took 342 seconds for 2,184 hourly snapshots. Ring members arrive already linked to **≈ 6 earlier users** (sharing a device with 1.8, a bank account with 2.5, an email pattern with 2.4 on average), vs ≈ 0.3 for genuine users. Genuine users' links are mostly **addresses** (6.2: hostels and PGs below the pruning cut-off). **"Known defaulters in the community" is always ≈ 0:** FPD becomes known only ~45 days after onboarding, long after the ring has finished. Waiting for defaults is not a fraud defence."""
R["«O74»"] = """
- **Individual features alone** (SIM age, limit, onboarding hour) are nearly useless at the decision point: AUC 0.73, but **recall at 1% only 2%**. Trained on FPD, this model mostly picks up credit stress.
- **Adding 1-hop sharing counts** is the big step: AUC **0.83** (+0.098, Holm p < 0.0001), recall **51%**, ring recall **84%**.
- **Multi-hop communities add little more:** AUC +0.009 (Holm p = 0.19), same recall. The direct link counts already carry most of the ring signal.
- **First-week behaviour** jumps AUC to 0.99 and recall to 72%, but it is available only on day 7, after the money is gone.
- **(f) Business meaning:** the essential investment is a **real-time identity-link lookup** (how many earlier users share this attribute). A full graph engine is useful for investigation and ring take-downs, but adds little to the onboarding decision here."""
R["«O75»"] = """the hourly-updated graph catches **51.4%** of frauds vs **50.3%** for the nightly batch. 12 frauds are caught only in real time and 7 only by the batch (exact McNemar p = 0.36), so there is no significant overall difference. The gap shows up where expected: for the **115 ring members whose ring-mate signed up earlier the same day**, real time catches **90.4% vs 83.5%**. **Business meaning:** real-time link updates matter for fast "burst" rings. Since rings mostly sign up over days, a nightly graph plus real-time 1-hop counters (cheap to keep current) is a sensible architecture under the documented 70–80 ms SLA."""
R["«O76»"] = """training on **confirmed fraud** instead of FPD raises AUC from 0.841 to **0.889** (+0.048, DeLong p ≈ 3e-9) and recall at 1% from 51.4% to 52.8%. FPD-trained models waste capacity learning genuine credit stress (78% of FPDs). **Business meaning:** a small investigation step that tags each early defaulter as "fraud" or "credit stress" pays off. It gives the fraud model a cleaner target, and gives the credit model the right one."""
R["«O77»"] = """
- **Precision:** of the 462 declines (1% budget), **52.8%** are fraudsters. The naive binomial CI (48–57%) is **too narrow**. Resampling whole communities gives **38.6–62.4%**, because declines come in correlated clusters (240 communities, one contributing 22 declines). Precision claims about graph-based rules need cluster-robust intervals.
- **Cost to good users:** at this budget, **0.89 good (non-defaulting) users are declined per fraudster stopped**. The next section shows that the 1% budget is past the optimum."""
R["«O78»"] = """
- **Total cost is lowest at a 0.5% decline share:** a saving of **₹7.1 lakh over the 5 test weeks**. That stops **48% of fraudsters** and declines just **1 good user**: the very top of the score is almost pure fraud.
- **Beyond the optimum,** more fraud is caught but good users are lost fast: 211 at 1%, 649 at 2%. Above ≈ 2.5% the policy **costs more than approving everyone**.
- **(f) Business meaning:** the documented "impact on good users" is the deciding factor. The optimal line is narrow (0.25–1%), and above it each extra fraudster stopped costs several good customers."""
R["«O8»"] = """the small neural network (AUC 0.832) is **not better** than gradient boosting (0.841; DeLong p = 0.36) on these tabular link features, and recall at 1% is similar (49.9% vs 51.4%). Simpl's move to neural networks makes sense when combining the raw transaction payload with long histories (sequence data). For a dozen engineered link counts, boosting is simpler and equally good. **Single-feature AUCs** confirm the graph signal: **recent community sign-ups (0.77)**, community size (0.77), fresh-SIM members (0.73) and shared bank account / device (0.68). Every one of these is weak alone; together with SIM age they make the model."""
R["«O9»"] = """at an assumed **5 lakh new users per month**:
- **At the optimal 0.5% decline share:** the model saves ≈ **₹0.77 crore/month** (₹15.4 per applicant) and declines ≈ **11 good users a month**.
- **At a 1% budget:** saving ≈ ₹0.57 crore/month, but ≈ **2,300 good users declined a month**.
- **At 2%:** almost no saving left, and ≈ 7,000 good users lost.
- **By feature tier at 1%:** individual features alone lose money (−₹0.49 crore/month, from declining credit-stress profiles instead of fraud); with 1-hop link counts the saving is ≈ +₹0.58 crore/month; full communities add nothing in ₹.
- **Reading:** the ₹ value comes from **link counts plus a tight decline budget**. The figures depend on the assumed ₹1,200 good-user lifetime value and fraud loss of 90% of limit."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** defaults cluster (fraud-driven).
- **H2:** 1-hop links add a lot ✅; communities add no significant AUC beyond 1-hop ❌.
- **H3 ❌:** real-time vs batch is not significant overall (only for same-day ring-mates).
- **H4:** the confirmed-fraud label is better (+0.05 AUC).
- **Guardrail met:** at the 0.5% budget, about 1 good user is declined per 230 declines.

**I recommend:**
1. **Onboarding gate:** score every applicant with SIM age + **hub-pruned 1-hop sharing counts** (device, address, bank account, email pattern), updated in real time. **Decline or give a ₹500 starter limit to the top 0.5%**, then review the band 0.5–1% manually.
2. **Hub pruning and data hygiene:** exclude attributes shared by more than ~10 users and all placeholder or default IDs. Re-tune the cut-off quarterly on investigated cases.
3. **Communities as an investigation tool:** run nightly community detection to take down whole rings (block all members) and feed investigators, rather than as a model input.
4. **Labels:** tag every early defaulter as fraud or credit stress, and train the fraud model on fraud.
5. **Day-7 review:** use first-week behaviour (limit spent within days, many merchants) to freeze limits on new accounts that look like bust-outs. It catches 72% at 1%.
6. **Fairness guardrail:** monitor decline rates for users in shared-address (hostel/PG/family) communities vs others.

**KPIs:** fraud loss per ₹100 disbursed; good users declined per fraudster stopped; share of genuine users in communities of 4+; fraud recall at the decline budget on matured labels; ring take-downs per month; decline-rate gap for shared-address users."""

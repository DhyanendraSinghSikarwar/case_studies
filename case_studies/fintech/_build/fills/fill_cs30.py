R = {}
R["«EXEC»"] = """*(Synthetic contacts with a randomised human-only holdout and a self-selected CSAT survey; PhonePe disclosed only "over 92%" resolved by AI, CSAT 70% and one agent per 20 million transactions. Written after the analysis.)*

- **The question:** is "92% resolved by AI" real, and what does it do to customers the bot cannot help?
- **"Resolved" by the bot is not "fixed".** In the simulation the bot **closes 87.6%** of tickets, close to the documented 92%, but only **80.2% are truly resolved** (the customer does not come back within 7 days). A **randomised 5% human-only holdout** resolves **85.9%**. AI-first is **5.7 pp worse** (CI −6.6 to −4.8) and **fails the 3 pp non-inferiority test**. It is also far faster: **2.5 vs 10.1 minutes** handling and **0.8 vs 9.0 minutes** wait.
- **The damage is concentrated in high-stakes issues.** For fraud complaints the bot closes 76% of tickets but only **35%** of those stay closed (human-only: 80%). Wrong-recipient transfers: 38% (human 83%); merchant disputes 53%; blocked accounts 63%. For routine issues (refund status, transaction history, payment debited-but-failed) the bot matches or beats humans.
- **CSAT tells a flattering story and needs correcting.** Only **8.9%** of customers answer, and unhappy customers answer more (a customer who had to re-contact is 19% more likely to respond). Raw top-2-box CSAT among responders is 61.9%. Weighting for non-response gives **64.0%**, closer to the true 65.5%. AI-first CSAT (65%) looks better than human-only (46%) *because speed delights customers*, even though true resolution is worse, which is why CSAT alone must never be the success metric. Across issue types CSAT tracks true resolution closely (Spearman +0.96).
- **The bot treats languages unequally:** adjusted odds of true resolution for **regional-language** customers are **0.74×** English (CI 0.70–0.77); intent accuracy 88.7% vs 93.2%.
- **The fix is cheap: ring-fence high-stakes issues.** Never letting the bot auto-close fraud, wrong-recipient, blocked-account and merchant-dispute tickets lifts true resolution from **80% to 84%**, cuts false closures by a third, and cuts expected cost per contact from **₹87 to ₹34** (human-only: ₹78). That is **≈ ₹160 crore/month cheaper than AI as run** at 3 crore contacts (illustrative cost weights).
- **I recommend:**
  - Route high-stakes issues to humans.
  - Replace "resolution rate" with 7-day true resolution as the headline.
  - Report CSAT only with a non-response correction.
  - Keep a 2–5% human-only holdout.
  - Invest in regional-language intent accuracy."""
R["«O5»"] = """we removed **700 duplicate contacts** and set **40 invalid CSAT ratings of 0** to missing (a 0 on a 1–5 scale would drag the score down). **500 contacts have no handling time** (timer lost when a chat closed abruptly); they are excluded only from time averages. Clean: **120,000 contacts**; **113,980 AI-first** and **6,020 in the human-only holdout (5.0%)**. **CSAT responses: 10,686 (8.9%)**."""
R["«O61»"] = """**left:** for routine issues (refund status, transaction history, recharge, login) the bot's claimed resolution and the true resolution are close. For fraud, wrong-recipient, merchant disputes and blocked accounts there is a **big gap**: the bot closes 54–77% of these tickets, yet far fewer stay resolved. **Right:** CSAT ratings come only from a self-selected 9% of customers, with more 1s and 5s than a random sample would give (people with extreme experiences answer)."""
R["«O71»"] = """the bot predicts the right intent **91.7%** of the time (Wilson 91.5–91.9%), but accuracy varies by language (χ² = 281, p ≈ 1e-60): **English 93.2%, Hinglish 92.2%, Hindi 91.1%, regional languages 88.7%**. **(f) Business meaning:** intent accuracy is high overall, yet one in nine regional-language customers is mis-understood, which feeds directly into unequal outcomes (7.7)."""
R["«O72»"] = """
- **The bot claims 87.6% resolved** (documented "over 92%"), **but 80.2% of AI-first contacts are truly resolved**; among bot-closed tickets only **79.4%** are. The **human-only holdout resolves 85.9%**.
- **True resolution is 5.7 pp lower with AI-first** (CI −6.6 to −4.8, p < 0.0001): **not non-inferior at a 3 pp margin**. Recontact is 19.8% vs 14.1%.
- **But AI is vastly faster:** handling time **2.5 vs 10.1 minutes (−76%)**, wait **0.8 vs 9.0 minutes (−91%)**.
- **(f) Business meaning:** the headline "92% resolved" confuses *closed* with *fixed*. A fair benchmark (the holdout) shows a real quality cost, offset by huge speed gains. Leaders need to decide that trade-off with eyes open, issue type by issue (7.3)."""
R["«O73»"] = """the quality gap is almost entirely in the **hard, high-stakes issues**:
- **Fraud complaints:** the bot closes 76%, but only **35%** of closed tickets stay resolved (false-closure rate 65%), vs 80% for humans.
- **Wrong-recipient transfers:** 38% vs 83% for humans (false-closure 62%).
- **Merchant disputes:** 53% vs 84%; **blocked accounts:** 63% vs 85%; **cashback missing:** 71% vs 87%.
- All significantly worse than humans (Holm p < 0.001), as are **KYC updates** (80% vs 87%).
- **Routine issues:** recharge/bill failure, app login, refund status, transaction history and "payment debited but failed" are statistically **no worse than humans** (several slightly better).

**Business meaning:** AI-first works for routine issues and fails where the stakes are highest, exactly where RBI grievance-redressal rules and customer harm concentrate."""
R["«O74»"] = """
- **Who answers:** customers who had to **re-contact** are **19% more likely to respond** (OR 1.19, p ≈ 4e-11). Bot-closed status does not change response (OR 0.99). Unhappy customers over-respond, so raw CSAT is biased.
- **Raw CSAT** (top-2-box, rating 4–5) among responders is **61.9%**. **Weighted for non-response: 64.0%** (CI 63.3–64.9%), nearer the true **65.5%** across all customers.
- **AI-first vs human-only holdout:** weighted CSAT **65.0% vs 45.6%**. In this simulation customers value the speed (0.8 vs 9.0 minutes' wait) enough to rate AI-first higher, **even though true resolution is lower**. (This rests on our assumption about how much speed matters; it is the pattern, not the size, that transfers.)
- **(f) Business meaning:** CSAT can *hide* a resolution problem when speed delights. Judge the bot on true resolution and CSAT together, and correct the survey for who responds."""
R["«O75»"] = """across the 12 issue types CSAT tracks true resolution closely (**Spearman +0.96**): the customers who got their problem fixed are the ones who are satisfied. The **worst corner** is the high-stakes issues: **fraud complaints** (true resolution 47%, CSAT 16%), **wrong-recipient transfers** (49%, 21%), **merchant disputes** (65%, 37%) and **blocked accounts** (74%, 42%). The best are transaction history (89%, 82%), payment debited-but-failed (89%, 75%) and refund status (87%, 78%). **Business meaning:** overall averages are dominated by routine issues; the satisfaction and trust problems sit in a small number of issue types that matter most."""
R["«O76»"] = """
- **Raising the confidence bar alone barely helps:** at τ = 0.2 → 0.8 containment falls from 87.6% to 28.7% and true resolution rises only from 80.1% to 85.2%, at ever higher human cost. High-stakes false closures stay at 34% → 11% of all high-stakes tickets (upper bound 35% → 11%).
- **Ring-fencing high-stakes issues works far better.** Never auto-closing fraud, wrong-recipient, blocked-account and merchant-dispute tickets **eliminates high-stakes false closures** (zero by construction, the bound is trivial) and lifts true resolution to **84.2% at τ = 0.2** while still **containing 75.9% of contacts**.
- **Lowest expected cost: τ = 0.2 with the ring-fence, ₹34 per contact**, vs ₹87 for the bot as run and ₹78 for human-only. Higher thresholds with the ring-fence cost more (₹62 at τ = 0.8) because they push routine issues to humans for little quality gain.
- **(f) Business meaning:** the right control is *which issues* the bot may close, not just how confident it is. These cost weights are illustrative; risk and compliance should set them."""
R["«O77»"] = """language matters, even after adjusting for issue type (LR χ² = 152, p ≈ 1e-32): relative to English, the **adjusted odds of true resolution are 0.93 for Hindi** (CI 0.90–0.97), **0.97 for Hinglish** (CI 0.93–1.01, not significant) and **0.74 for regional languages** (CI 0.70–0.77). Regional-language customers also close fewer tickets by bot (84.4% vs 88.0%) and wait slightly longer. True resolution is 76.7% for regional-language customers vs 81.2% for English. **Business meaning:** the largest equity gap is in the language the bot understands least. This needs targeted intent data and audit, and is a grievance-redressal risk."""
R["«O9»"] = """at **3 crore support contacts a month** (human handling ₹6/minute; ₹1 per bot-closed contact; ₹120 per unresolved contact; ₹900 per high-stakes false closure):

| Policy | True resolution | Cost per contact | ₹ crore a month |
|---|---|---|---|
| Human-only | 86% | ₹78 | ≈ ₹233 |
| AI-first as run (τ = 0.2) | 80% | ₹87 | ≈ ₹262 |
| **AI-first with high-stakes ring-fence** | **84%** | **₹34** | **≈ ₹103** |

- **Saving of the recommended policy:** ≈ **₹130 crore/month vs human-only** and ≈ **₹160 crore/month vs AI as run**, while keeping 76% of contacts bot-handled.
- **Staffing:** if every contact were human-handled, ≈ 34,000 agent-equivalents (at 150 hours a month) would be needed. AI-first leaves ≈ 4,000, or ≈ 8,000 with the ring-fence.
- **The ₹ figures are driven by the assumed ₹900 cost per high-stakes false closure,** which makes the "AI as run" policy look worse than human-only. With a lower penalty, the AI-as-run policy would look better. The ranking of "ring-fence" as the cheapest holds as long as that cost is above ≈ ₹150."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅ (claim vs reality):** bot-closed tickets are truly resolved 79.4% vs 85.9% for human-only.
- **H2 ❌:** AI-first is **not** non-inferior to humans on true resolution (−5.7 pp; margin 3 pp).
- **H3 ✅:** CSAT responders are biased (unresolved customers over-respond); IPW moves the score closer to the truth.
- **H4:** ring-fencing high-stakes issues removes harmful closures and gives the lowest cost.

**I recommend:**
1. **Never let the bot auto-close high-stakes issues** (fraud, wrong recipient, blocked account, merchant dispute): route them to humans with the AI's summary. Keep AI-first for routine issues.
2. **Make 7-day true resolution the headline metric,** with bot-closed rate (containment) as a secondary number, and report CSAT only **with a non-response correction**.
3. **Keep a 2–5% randomised human-only holdout** (on low-stakes issue types, or with a delayed-escalation design) as the unbiased benchmark.
4. **Fix the language gap:** more labelled data and audits for regional-language intents (88.7% accuracy, 0.74× adjusted resolution odds), with human fallback.
5. **Audit weekly** a sample of bot-closed tickets for faithfulness and harm, particularly after model or knowledge-base changes.

**KPIs:** 7-day true resolution (AI vs holdout); false-closure rate by issue type; high-stakes bot-closed share (target 0); weighted CSAT and response rate; resolution gap by language; handling and wait time; escalation quality."""

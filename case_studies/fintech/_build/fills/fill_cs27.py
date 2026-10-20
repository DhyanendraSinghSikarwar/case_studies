R = {}
R["«EXEC»"] = """*(Synthetic transcript-derived records and a simulated dialler experiment; Policybazaar disclosed no ASR error rates or experiment design. Written after the analysis.)*

- **The question:** can transcript-based request counts guide product decisions, can the compliance flag cover 100% of calls usefully, and did the new dialler really cause the efficiency gain?
- **Intent counts are usable for ranking, not for exact shares.** The ASR + NLP pipeline tags intent correctly **70%** of the time (Hindi 64%, Hinglish 71%, English 81%). Despite that, the documented insight survives: "cashless hospital" is **7th in the transcripts (95% range 7–9) and truly 8th**, with a predicted share of 6.5% against a true 5.6%. It is also **growing about 5% a week** (trend p ≈ 1e-24), which is the product signal that mattered. A confusion-matrix correction did not remove the bias for this class (corrected 6.5%, CI 5.1–7.9%, which does include the truth), so quote ranges, not exact shares.
- **Compliance flags beat random sampling by a mile.** The breach score has ROC-AUC **0.92** (similar across languages). At a 5% alert budget, **62% of alerts are real breaches** (vs 6.4% by chance) and **48% of all breaches are caught**, against 5% with random listening. At a 1–2% budget (today's human capacity), precision is 82–90%.
- **The dialler gain is real, and a proper analysis shows how much.** Teams were randomised (12 new, 12 old), so the team is the unit.
  - **Dials per hour:** +32% (18.0 → 23.9).
  - **Talk-time share ("call efficiency"):** 40% → **60%**, below the documented 85%.
  - **Connect rate:** +16%.
  - **Sales per logged-in hour:** +66%.
  - **Callback delay:** 295 → 45 minutes.
  - All permutation p < 0.0001.
  - Treating the 4,740 agent-days as independent would have understated the uncertainty by 2.2×.
- **₹ impact (400 outbound agents):** ≈ **₹2.6 crore/month of extra margin (range ₹2.2–3.1 crore)**, equivalent to the output of ≈ 260 more agents. QA at a 5% alert budget on 10 lakh calls finds ≈ 31,000 true breaches for ≈ ₹0.17 crore, against ≈ 1,000 under 1–2% random listening.
- **I recommend:**
  - Roll out the new dialler to all teams.
  - Run compliance QA from flagged calls with a fixed alert budget.
  - Report intent shares as ranges and re-estimate the correction as the product mix changes.
  - Measure WER by language on a labelled sample."""
R["«O5»"] = """we removed **300 duplicate calls**; **250 ASR failures (blank intent)** are routed to a human and excluded from frequency counts (not counted as "other"); and **60 agent-days logged under the wrong ID (0 logged-in minutes)** are dropped, because they would divide by zero when computing per-hour rates. Clean: **60,000 calls** and **4,740 agent-days** (120 agents in 24 teams × 40 days)."""
R["«O61»"] = """**left:** the transcript-derived shares (orange) track the true shares (blue) closely for most intents, but over-count some ("coverage query", "other") and under-count others (renewal reminders). **Right:** call efficiency (talk time as a share of logged-in time) sits near 40% for the old dialler and near 60% for the new one on every day of the experiment: a stable, persistent gap, not a one-off."""
R["«O71»"] = """overall intent accuracy is **70.2%** (bootstrap CI 69.9–70.6%, macro-F1 0.69). Accuracy depends strongly on language (χ² = 1,421, p ≈ 0): **English 81.2%, Hinglish 70.7%, Hindi 63.7%**. The hardest intents are coverage queries (F1 0.60), agent complaints and cashless hospital (0.64). **(f) Business meaning:** the model is good enough to rank topics and flag trends, but not to count individual calls, and Hindi, the largest language, needs the most work. The documented WER was not disclosed; measure it by language on a labelled sample."""
R["«O72»"] = """the finding that cashless-hospital requests are mid-ranked survives uncertainty: **true rank 8, predicted rank 7 (95% bootstrap range 7–9)**, matching the documented "7th–8th". Shares are biased: **predicted 6.53% vs true 5.57%** (the classifier confuses it with claim status). The matrix-inversion correction gives 6.50% (CI 5.08–7.94%); it contains the truth, but did not remove the bias here. The correction worked well for some classes (e.g., renewal reminders 14.1% predicted → 18.5% corrected vs 19.0% true) and not for others. **Business meaning:** rank and trend are reliable, but exact shares are not. If a product decision depends on a *level* (e.g., a business case for 5% of calls), validate it on a labelled sample."""
R["«O73»"] = """the cashless-hospital share rises from ≈ 3.4% (week 1) to 7.7% (week 12) in truth (Cochran–Armitage z = 15.2, p ≈ 5e-52), and the transcript-derived share shows the same rise (z = 10.1, p ≈ 4e-24; **+4.7% per week**) from 5.1% to 8.2%. The corrected share follows the truth more closely over time but is biased upwards in level. **Business meaning:** the trend is detectable in the data you actually have, quickly (weekly, from 5,000 calls), which is exactly what a product team needs to prioritise a cashless-hospital feature."""
R["«O74»"] = """with a base rate of 6.4% breaches, the model's score has **ROC-AUC 0.915** (English 0.920, Hindi 0.924, Hinglish 0.900: no meaningful language gap, CIs overlap). By alert budget:
- **1% of calls** (80 alerts): precision **90%**, 14% of breaches caught.
- **2%:** precision 82%, 25% caught.
- **5%:** precision **62%**, **48% caught**.
- **10%:** precision 44%, 68% caught.
- **20%:** precision 27%, 82% caught.

**Random listening at the same budgets** has 6.4% precision and catches only 1%, 2%, 5%, 10%, 20% of breaches. **Business meaning:** flagging concentrates QA time on the calls that matter: at a 5% budget, a QA analyst finds a real breach in about 6 of every 10 flagged calls, instead of 1 in 16."""
R["«O75»"] = """the experiment shows large, clear effects at the team level (24 teams; permutation p < 0.0001 for all outcomes):
- **Dials per hour:** 18.0 → **23.9 (+32.5%)**, vs the documented "+50% dial-out rate".
- **Talk-time share:** 40.0% → **60.3% (+51%)** (documented 40% → 85%).
- **Connect rate:** 26.3% → 30.4% (+16%).
- **Sales per logged-in hour:** 0.268 → **0.444 (+66%)** (cluster-robust effect +0.176, CI 0.149–0.204).
- **Callback delay:** 295 → 45 minutes (−85%; documented 30–45 minutes ✓).

**Clustering matters.** Treating agent-days as independent gives a standard error of 0.0065 for the sales effect, but the cluster-robust one is **0.0140 (2.2× larger)**. After removing the arm effect, the **ICC** is 0.21 for talk-time share and only 0.02 for sales per hour, which gives a design effect of 42 and 5.5 respectively: the effective number of independent observations is far smaller than 4,740. **Business meaning:** the effects are large enough to be convincing even with the correct (team-level) analysis."""
R["«O76»"] = """callback delays fall from a median of **259 to 40 minutes** (team-level Mann–Whitney p < 0.0001), and agent-days with callbacks within an hour rise from **0% to 79%**. Teams with faster callbacks have higher sales per hour (Spearman −0.71, p = 0.0001), but that largely reflects the arm, since the new dialler improved both. **Business meaning:** the documented callback target of 30–45 minutes is achieved, and faster callbacks are one plausible mechanism for the sales gain (consistent with Case 28's speed-to-lead result)."""
R["«O77»"] = """with effects as large as these, few teams are needed: **8 per arm** to detect a 10% change in call efficiency, **23 per arm** for a 10% change in sales per hour, and **3–4 per arm** for 25% effects (the practical floor is 3 teams, since a standard deviation cannot be estimated from one or two). **Business meaning:** the 24-team experiment was well powered for the large effects seen here. Detecting a modest 10% improvement in *sales* would need roughly all 24 teams per arm, so test future incremental tweaks with stepped-wedge or longer designs."""
R["«O9»"] = """for **400 outbound agents** (26 working days a month, ₹1,800 margin per sale, ₹35,000 a month per agent):
- **Sales per agent-day:** 2.14 → 3.55: ≈ **₹2.6 crore/month** of extra margin (cluster-robust 95% range ₹2.2–3.1 crore), equal to the output of ≈ 263 extra agents (≈ ₹0.9 crore/month of salary).
- **QA at a 5% alert budget** on 10 lakh calls: 50,000 alerts and ≈ **31,000 true breaches found** for ≈ ₹0.17 crore of QA time (₹400/hour, 5 minutes per call), versus ≈ **970 breaches** under 1–2% random listening.
- **Reading:** the dialler change adds the most direct revenue; the compliance monitoring avoids regulatory and mis-selling risk that is not valued here. The intent analysis informs product choices (cashless hospital) whose value is not quantified."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** intent accuracy differs strongly by language.
- **H2 ✅:** cashless-hospital share is rising (+4.7% per week).
- **H3 ✅:** the compliance flag is far above the 6.4% base rate (62% precision at a 5% budget).
- **H4 ✅:** the new dialler improves efficiency and sales (team-level p < 0.0001).

**I recommend:**
1. **Roll out the new dialler** to all teams, with the callback-scheduling feature.
2. **Run compliance QA on flagged calls** at a fixed budget (start at 2–5% of calls, 82–62% precision), with analysts feeding labels back to the model.
3. **Use transcript-based intent counts for ranking and trends**, not exact levels. Re-estimate the confusion correction monthly, and invest in Hindi accuracy (64%).
4. **Design future dialler tests at the team level** (or stepped-wedge) with cluster-robust analysis. Never analyse agent-days as independent.
5. **Guardrails:** monitor spam/complaint rates (TRAI/DND call-time rules) alongside call efficiency.

**KPIs:** WER and intent accuracy by language; breach-flag precision and recall at the alert budget; dials/hour, talk-time share, sales per logged-in hour (team-level); callback delay; share of calls monitored."""

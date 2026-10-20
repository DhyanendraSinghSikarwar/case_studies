R = {}
R["«EXEC»"] = """*(Synthetic visitors with built-in self-selection, a randomised chat pop-up and a bot era; Policybazaar reported only the raw 2× and operational gains. Written after the analysis.)*

- **The question:** chat users convert about 2× as often, so should we push everyone into chat and scale it with a bot?
- **The raw 2× is mostly customer, not channel.** Chatters convert at **8.9% vs 4.1%** (RR 2.15). But chatters are the more serious buyers: policies expiring sooner, more quotes viewed, return visits. Adjusting for what we can observe (matching, weighting, doubly-robust) cuts the effect to **+3.6 to +3.8 pp (RR ≈ 1.7)**.
- **Observed signals do not capture all intent.** Rosenbaum's Γ shows the adjusted result survives hidden bias only up to Γ ≈ 1.75, and an unmeasured factor with risk ratio ≈ 2.8 on both chatting and buying would explain it away. In this simulation the truth confirms the adjusted figure is still too high: **the real average effect of chatting is ≈ +2.5 pp for people who chose to chat (+1.6 pp for everyone)**.
- **The randomised pop-up gives the causal answer:** showing the pop-up to a random half raised chat use from 6.2% to 15.4% (+9.2 pp) and purchases from **4.39% to 4.72% (+0.32 pp, p = 0.0002)**. Scaled up, **chatting adds +3.5 pp for the visitors it persuades** (Wald/IV; 95% CI **+1.2 to +5.2 pp**), which is noisy but consistent with the truth (≈ 1.6–2.5 pp).
- **The bot's real win is speed:** responses delayed more than 5 minutes fell from **45% to 6%** (documented 35% → 7–8%) as the bot's share of chats rose from 21% to 79%. Each extra minute of delay lowers a chatter's odds of buying by **5.6% (OR 0.944, CI 0.935–0.953)**.
- **₹ impact (30 lakh visitors a month, chat share 9.7% → 30%):**
  - **Using the raw 2×:** ≈ 29,000 extra policies (≈ ₹4.8 crore commission a month). This overstates by 30–90%.
  - **Using the experimental range:** about **7,500–32,000 extra policies (≈ ₹1.2–5.0 crore commission)**; the honest point estimate is ≈ 21,000 policies. The lower end is closest to the truth.
- **I recommend:**
  - Keep scaling the bot, because it cuts delays and agent load.
  - Forecast the sales benefit from the experiment, not the raw 2×.
  - Run a larger encouragement test (≈ 200,000 visitors per arm to detect a 2 pp effect).
  - Add a placebo pop-up arm to check the exclusion assumption."""
R["«O5»"] = """we removed **1,000 duplicate sessions**, flagged **1,203 unknown policy-expiry values** (coded −1) with an "unknown" indicator and median fill, and noted **200 chats with no first-response time**. The pop-up was never shown before week 3 and the bot never answered a non-chat. Clean: **300,000 visitors**; **chat share 9.7%** (documented 8–9%), conversion 4.58%; the encouragement experiment covers **225,081 visitors** in weeks 3–8."""
R["«O61»"] = """**left:** chatters convert about twice as often as non-chatters every single week, before and after the pop-up test and the bot launch. A stable 2× is exactly what both a real channel effect *and* self-selection would produce. **Right:** chatters are closer to their policy expiry date (more urgent), the clearest sign that they are the more motivated buyers."""
R["«O71»"] = """chatters convert at **8.88%** (CI 8.56–9.21%) vs **4.12%** (CI 4.05–4.20%) for non-chatters: a raw risk ratio of **2.15** (CI 2.07–2.25; χ² = 1,359, p ≈ 0), and chat is used by 9.7% of visitors. This reproduces the documented "about 2× … only 8–9% of customers". **(f) Business meaning:** the number is real, but it is an association between two kinds of visitor, not yet evidence that chat *causes* sales."""
R["«O72»"] = """the same signals that predict who chats also predict who buys: **more quotes viewed** (OR 1.59 for chatting; 1.64 for buying among non-chatters), **return visitors** (1.58; 1.31), **more add-ons viewed** (1.11; 1.18) and **closer expiry** (OR 0.994 per extra day for chatting, 0.978 for buying). Standardised differences between chatters and non-chatters: quotes +0.31, returning +0.26, days-to-expiry −0.22, add-ons +0.15. **(f) Business meaning:** this is classic self-selection: the more serious visitors both chat more and buy more. A 2× gap would appear even if chat did nothing."""
R["«O73»"] = """after adjusting for observed intent signals, the effect on those who chat shrinks from **+4.76 pp (RR 2.15)** to:
- **Matching:** +3.81 pp (CI 3.22–4.01).
- **IPW:** +3.70 pp (CI 3.36–3.99).
- **Doubly-robust (AIPW):** **+3.62 pp (RR 1.69; CI 3.28–3.90).**

Balance is excellent after weighting (max |SMD| 0.003). All three agree, but they remove only the *observed* part of the confounding. **(f) Business meaning:** about a quarter of the raw gap was visible customer mix. The remainder could still be hidden intent."""
R["«O74»"] = """- **E-value:** the raw RR of 2.15 needs a hidden confounder with risk ratio **3.7** (with both chatting and buying) to explain it away; the adjusted RR of 1.69 needs **2.8**. Both are large, but an unobserved factor such as "already decided to buy, wants to finalise" could plausibly reach that.
- **Rosenbaum Γ:** the matched-pair result stays significant at Γ = 1.5 (hidden bias that raises the odds of chatting by 50% within a pair) and is **borderline at 1.75 (p = 0.046)**, lost by Γ = 2.
- **(f) Business meaning:** the adjusted estimate is **not robust to moderate hidden confounding**. In this simulation we know the truth is lower still (≈ +2.5 pp for chatters), which is what these sensitivity numbers warn about."""
R["«O75»"] = """
- **Randomisation worked:** SRM p = 0.80, max |SMD| 0.010.
- **First stage:** the pop-up raises chat use from **6.22% to 15.44% (+9.23 pp)**, a very strong instrument (F ≈ 5,071).
- **ITT:** purchases rise from **4.392% to 4.715% (+0.323 pp; z = 3.68, p = 0.0002)**, so showing the pop-up causes sales.
- **LATE (Wald): +3.50 pp** for visitors who chat because of the pop-up (bootstrap CI **+1.24 to +5.23**); 2SLS with covariates **+3.47 pp (CI +1.35 to +5.29)**.
- **Truth check (simulation only):** the true average effect is **+1.60 pp for all visitors and +2.49 pp for people who chose to chat**. The IV point estimate is higher than both, but with an interval this wide (SE ≈ 1 pp) it is consistent with them. It is unbiased but noisy, whereas the observational estimates (+3.6 to +4.8 pp) sit above the truth for a systematic reason (hidden intent).
- **(f) Business meaning:** this is the number to plan with, together with its uncertainty: the lift for *persuadable* visitors is somewhere between about +1 and +5 pp."""
R["«O76»"] = """the bot cut slow responses (first reply > 5 minutes) from **45.5% of chats (weeks 1–4) to 5.9% (weeks 5–8)** (documented 35% → 7–8%), with the bot's share of chats rising from **21% to 79%** (documented 20% → 75–80%). Within chats, each extra minute of first-response delay lowers the odds of buying by **5.6%** (OR **0.944**, CI 0.935–0.953; p ≈ 5e-33), adjusted for intent signals and source. The chart shows conversion falling steadily with delay. **Business meaning:** speed matters, and that is where the bot earns its keep. A chat answered in seconds keeps the sale; one answered after ten minutes loses a large share of buyers (the same lesson as Case 28)."""
R["«O77»"] = """IV estimates are noisy because only people who chat *because of the pop-up* carry information. To detect a **2 pp** effect of chatting with a **9 pp** first stage, you need about **200,000 visitors per arm**; a 1 pp effect needs about 810,000; a 0.5 pp effect over 3 million. A stronger pop-up (a first stage of 25 pp) cuts these needs 3×. **Business meaning:** this experiment (≈ 112,000 per arm) can pin down a 3 pp effect but not a 1 pp one. A stronger or better-timed pop-up would make future tests cheaper."""
R["«O9»"] = """for **30 lakh visitors a month** with chat use raised from 9.7% to 30% (≈ **609,000 more chatters**; average premium ₹11,005; commission 15%):

| Effect assumption | Effect per new chatter | Extra policies a month | Extra commission |
|---|---|---|---|
| Raw 2× (naive) | +4.76 pp | ≈ 29,000 | ≈ ₹4.8 crore |
| Observational (AIPW) | +3.62 pp | ≈ 22,000 | ≈ ₹3.6 crore |
| **Experimental LATE** | **+3.50 pp (CI +1.24 to +5.23)** | **≈ 21,000 (range 7,500–31,900)** | **≈ ₹3.5 crore (range ₹1.2–5.3 crore)** |

- **The truth in the simulation is lower still:** about +2 pp per new chatter, i.e. ≈ 12,000 extra policies and ≈ ₹2 crore.
- **Reading:** a business case built on the raw 2× overstates the sales benefit by roughly 1.5–2.4×. The bot's economics are stronger on **agent productivity** (the documented 1.5–2 → 7–8 sales per agent-day) than on conversion. Plan on the conservative end of the experimental range."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** chatters convert 2.15× as often (raw).
- **H2:** adjusted ATT is still +3.6 pp (significant), but not robust to hidden bias (E-value 2.8; Γ = 1.75).
- **H3 ✅:** the pop-up raises chat use and purchases (ITT +0.32 pp, p = 0.0002); LATE +3.5 pp (CI +1.2 to +5.2).
- **H4 ✅:** longer first-response delay lowers conversion (OR 0.944 per minute).

**I recommend:**
1. **Keep scaling the bot.** Speed is a real sales lever (slow replies fell from 45% to 6%) and it multiplies agent productivity.
2. **Forecast sales from the experiment,** not the raw 2×: plan for roughly +2–3.5 pp per additional chatter, with a range of +1 to +5 pp.
3. **Run a bigger, sharper encouragement test:** ≈ 200,000 visitors per arm to detect 2 pp, with a **placebo pop-up arm** (e.g., an FAQ link) to check that the pop-up affects buying only through chat.
4. **Target chat invitations** at visitors who are *not* already highly motivated (the marginal buyers), since keen buyers would buy anyway.
5. **Track cost per policy, not just conversion:** the bot's main benefit is agent output.

**KPIs:** conversion by randomised arm; chat uptake; share of responses > 5 minutes; bot share of chats; policies per agent-day; cost per policy; adjusted vs experimental effect estimates side by side."""

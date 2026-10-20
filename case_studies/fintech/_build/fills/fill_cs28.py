R = {}
R["«EXEC»"] = """*(Synthetic leads calibrated to the documented RM delay of 8–12 minutes and AI routing mix; Policybazaar disclosed no conversion numbers. Written after the analysis.)*

- **The question:** how much does contact delay cost, and is an AI call within a minute worth it?
- **Delay is very costly in the raw data.** Among RM-handled leads, conversion falls from **8.2% (contacted within 1–3 minutes) to 3.0% (10–20 min) to 0.7% (30–60 min)**, and reach falls from 79% to 33%. The odds of converting roughly halve with every doubling of the delay.
- **But the raw curve exaggerates, because hot leads get called first.** Once true lead quality is added (possible only in simulation), the odds fall **20% per doubling of delay, not 43–46%**. Using the raw curve to forecast what a sub-minute call would deliver predicts **+298%** conversion, which is badly wrong.
- **The randomised test gives the real answer:** a random 30% of leads got an AI call within about a minute.
  - **Reach:** 64.2% → **77.0%** (+12.8 pp; CI +12.0 to +13.6).
  - **Conversion:** 4.12% → **5.28%** (+1.16 pp; CI +0.75 to +1.58; **+28% relative**, RR 1.28, CI 1.18–1.40).
  - **Who gains most:** peak-hour leads (+1.5 pp, +40%, when RM queues are longest) and motor (+1.4 pp), vs +0.9 pp off-peak. All Holm-significant except travel and term life.
- **The documented routing mix reproduces:** 4.7% of leads qualified (6.1% of reached leads; documented 5–7%); among reached leads **68% AI-handled, 26% scheduled callback, 6% RM hand-off** (documented 67/26/7). Qualified hand-offs convert at 13.4% vs 6.5% for AI-handled leads.
- **The capacity benefit is as large as the conversion benefit:** with 3,500 leads a day and 40 RMs, today's queue runs at **83% utilisation with a median 6-minute wait (P90 26 minutes)**. With an AI first touch, RMs only take hand-offs (about 165 calls a day, **4% utilisation**, no wait), freeing ≈ 95% of RM time for high-value work.
- **₹ impact:** at 4.5 lakh leads a month, the randomised lift is worth **≈ 5,200 extra policies a month (CI 3,400–7,100) ≈ ₹0.9 crore/month** of margin, plus the RM time released. (The raw-data "value of a minute", ≈ ₹74 lakh/month per minute, is an overestimate and should not be used.)
- **I recommend:**
  - Put every new lead through an AI first touch within 60 seconds.
  - Redeploy RMs to hand-offs and high-value scheduled callbacks.
  - Measure by randomised holdout, not by raw delay curves.
  - Add a second arm ("human RM call within a minute") to separate speed from the AI."""
R["«O5»"] = """we removed **800 duplicate leads**, dropped **1,497 leads with a missing first-contact timestamp** and **300 with a negative delay** (clock skew between the form server and the dialler). These cannot be repaired by guessing, and are excluded rather than set to zero, which would create fake "instant" contacts. Clean: **148,203 leads**; the randomised window (days 22–35) has **49,587 leads, 30.0% AI-first**; RM-queue leads have a median delay of **10.0 minutes** (documented 8–12)."""
R["«O61»"] = """**left:** among RM-handled leads, reach and conversion both fall steadily as the delay grows: conversion is ≈ 13% for contacts within a minute and under 1% after half an hour. **Right:** RM delay peaks around lunch (12:00) and early evening (18:00), when form submissions surge and queues build. Hour of the day therefore drives both delay and conversion, a first sign that raw delay comparisons are confounded."""
R["«O71»"] = """conversion falls monotonically across delay bands (Cochran–Armitage z = −40, p ≈ 0): **12.8% (< 1 min, only 540 leads) → 8.2% (1–3) → 6.7% (3–5) → 5.0% (5–10) → 3.0% (10–20) → 1.4% (20–30) → 0.7% (30–60) → 0.5% (60+)**. Reach falls from 81% to 14%. Contact within 3 minutes converts at **8.4% vs 2.6% at 10–30 minutes**, a 3× difference. **(f) Business meaning:** a lead's value decays fast, and the first few minutes matter most. But this is the *observed* association, which partly reflects which leads were called first."""
R["«O72»"] = """the apparent effect of delay depends on what is controlled:
- **Unadjusted:** each doubling of delay cuts the odds of converting by **43%** (OR 0.57).
- **Adjusted for hour and product:** **46%** (OR 0.54), no real change, since hour and product do not capture lead quality.
- **With the true lead quality** (an oracle available only in the simulation): **20%** (OR 0.80, CI 0.78–0.83).

So **more than half of the raw delay effect is lead quality, not speed**: hot leads are called first *and* convert more. **(f) Business meaning:** the raw delay curve is not a reliable forecast of what faster contact would do."""
R["«O73»"] = """
- **The randomisation is sound:** 14,856 AI vs 34,731 RM leads (30.0%, binomial test p = 0.85), with the same hour profile.
- **Reach rises from 64.2% to 77.0%** (+12.8 pp, Newcombe CI +12.0 to +13.6; RR 1.20).
- **Conversion rises from 4.12% to 5.28%** (**+1.16 pp**, CI +0.75 to +1.58; **RR 1.28**, CI 1.18–1.40; p < 0.0001).
- **Subgroups (pre-treatment):** peak hours **+1.54 pp (+40%)** vs off-peak +0.87 pp (+20%); by product, motor +1.37 pp, health +1.20 pp, term life +1.07 pp (Holm p = 0.08), travel +0.71 pp (p = 0.09). All lifts are positive and the largest gains come when RM queues are longest.
- **A pitfall avoided:** comparing the AI group with control leads grouped by *delay* would suggest "no benefit for leads called within 5 minutes", because those are the hot leads. That is selection, not a treatment effect.
- **(f) Business meaning:** a one-minute AI first touch lifts conversion by about a quarter, with the biggest gains where RM queues are longest."""
R["«O74»"] = """the observational curve (with hour and product) predicts that contacting RM leads within a minute would lift conversion **from 4.1% to 16.4% (+298%)**, but the randomised test delivers **+28%**. The experiment's lift is only **9%** of what the curve predicts. Two reasons:
- **Confounding:** the curve was learned from leads that were fast *because* they were hot.
- **Extrapolation:** it stretches a log-delay curve to the very edge of the data (< 1 minute, only 540 observed leads).

In this simulation the AI arm has no persuasion penalty built in, so the gap is **bias in the observational model**, not a weaker bot. **Business meaning:** never size a speed-to-lead project from a raw delay curve. Run the randomised test."""
R["«O75»"] = """- **Qualification:** **4.7%** of all AI-touched leads qualify (Wilson 4.4–5.1%), **6.1% of reached leads** (documented 5–7%).
- **Routing among reached leads:** **68% AI-handled, 26% scheduled callback, 6% RM hand-off**, closely matching the documented 67% / 26% / 7%.
- **Conversion by route:** **RM hand-offs 13.4%**, AI-handled 6.5%, scheduled callbacks 6.2%, no-answer retries 0% (not yet reached). **Business meaning:** the qualification step does separate valuable leads (hand-offs convert at twice the AI-handled rate), so RMs get the leads worth their time. The no-answer share (28% of AI-touched leads) is the next problem to work on."""
R["«O76»"] = """with **3,500 leads a day and 40 RMs**:
- **Today (FCFS):** RMs make ≈ 3,500 calls a day at **83% utilisation**, with a **median wait of 6.2 minutes and a P90 of 26 minutes**. The simulated waits are shorter than observed delays (10 min), because real delays include retries and breaks; we therefore use the randomised control arm for conversions (**144/day**).
- **AI first touch; RMs take hand-offs only:** ≈ **165 RM calls a day, 4% utilisation, no queue**. Conversions rise to **185/day** (+28%, from the randomised arm).
- **Business meaning:** the AI first touch does two things: it lifts conversion, and it removes ≈ 95% of the first-touch load from RMs, freeing them for hand-offs and scheduled callbacks. The conversion gain is measured. The capacity gain is a modelled estimate that depends on assumed call duration and shift patterns."""
R["«O9»"] = """- **Randomised lift:** at **4.5 lakh leads a month**, +1.16 pp = **≈ 5,200 extra policies a month (95% CI 3,400–7,100)**, ≈ **₹0.9 crore/month** at ₹1,800 margin (range ₹0.6–1.3 crore).
- **RM capacity released:** about **3,300 RM calls a day** no longer needed for first touch (≈ 95% of today's call load), which can go to hand-offs, scheduled callbacks and upsell.
- **Not to be used:** the raw-data "value of a minute" of ≈ ₹74 lakh a month is **overstated** (it is built on the confounded delay curve, 7.2 and 7.4).
- **Reading:** the measured benefit is modest in ₹ (about ₹1 crore a month at this lead volume and margin), but it is credible, and it comes with a large operational benefit. A lead-level value model (term life > health > motor > travel) would raise it further."""
R["«O10»"] = """**Decision against the hypotheses:**
- **H1 ✅:** conversion falls steeply with delay.
- **H2 ✅:** the randomised AI first touch lifts reach (+12.8 pp) and conversion (+1.16 pp, +28%).
- **H3 ✅ (confounding is real):** unadjusted −43% per doubling vs −20% with true lead quality.
- **H4:** the queue model shows RM load falling from 83% to 4% utilisation. Conversions come from the randomised arms.
- **Guardrail:** AI-handled leads convert (6.5%), and hand-offs convert twice as well (13.4%).

**I recommend:**
1. **Put every new lead through the AI first touch within 60 seconds,** starting with peak hours and motor/health, where the gain is largest.
2. **Redeploy RMs:** hand-offs first (13.4% conversion), then scheduled callbacks, then high-value products.
3. **Measure with randomisation:** keep a 5–10% RM-first holdout permanently, and add a "human call within a minute" arm to separate speed from the AI voice.
4. **Never forecast from a raw delay curve:** it overstated the benefit ~10× here.
5. **Fix the no-answer share** (28%): smarter retry timing, WhatsApp follow-up; and guard customer experience (TRAI/DND consent, call-time limits).

**KPIs:** median first-contact delay; reach rate; qualified-lead rate (5–7%); conversion vs holdout; hand-off conversion; RM utilisation; no-answer share; complaints and opt-outs."""

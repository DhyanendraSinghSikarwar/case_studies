**Say this first (1 line):** 100 zones x 1,440 minutes = 144,000 price decisions a day, and five +20% steps take 100 rupees to 248.83, so a per-update cap limits speed but not level; I would add an absolute cap, a rate limit over longer windows and a human override, and confirm with the business and legal what price limits apply.

**Clarifying questions:**
- What is the objective: revenue, trips completed, driver supply balance? A price that clears the market is not always the profit-maximising one.
- Who may see and complain about prices, and are there fare limits we must respect? Ask compliance and legal; I do not assume the rules.
- Is demand data per zone available in near real time, and how noisy is it? Noisy inputs make prices jump.
- Do drivers see the same multiplier? Supply response matters for balance.
- Can we run randomised tests by zone or by time? It decides how we measure effect.

**Approach:**
1. Clarify and frame. Goal: balance supply and demand per zone every minute without price shocks. Pricing is a control problem: forecast, price, observe, adjust.
2. Metrics and guardrails. Completed trips per request, ride-request fill rate, driver utilisation, revenue per hour, wait time. Guardrails: price complaint rate, share of time at the cap, price volatility (steps over 10% in a row), cancellation rate.
3. Data and labels. Logged requests, available drivers, prices shown, accept and cancel outcomes, per zone and minute. Prices were set by past rules, so demand response is only learned in the range of prices tried (limited price variation); add randomised small price nudges if allowed.
4. Baseline first. A rule on the ratio of requests to available drivers in each zone, smoothed over a few minutes, with the 20% step cap. Measure fill rate and revenue against it.
5. Model and trade-offs. Demand forecast per zone and a price-response (elasticity) estimate. Optimise a price in a range, then apply guardrails: the +-20% step cap (limits speed), an absolute cap (limits level; 5 steps give 248.83, 4 steps already pass 2x base at 207.36, see the code), smoothing across neighbouring zones to avoid cliffs, and a manual kill switch.
6. Evaluation. Offline: forecast error by zone and hour, replay of logged data with the guardrails. Online: zone-level or time-slice randomisation (switchback) because riders and drivers interact across zones, which breaks simple user-level tests.
7. Launch and experiment plan. Start in a few zones, keep a share of zones on the old rule, ramp when fill rate and revenue improve without more complaints.
8. Monitoring, retraining and risks. Alerts on price volatility, time at the cap, forecast bias per zone; retrain the forecast frequently; review festival and weather events manually.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 5, 5, 4, 10, 7, 5, 5.

**Metrics:**
- Price decisions a day = zones x decisions per zone per day = 100 x 1,440 = 144,000.
- Maximum price after n capped increases = base x 1.2^n: 100 x 1.2^5 = 248.832 rupees.
- Fill rate = requests matched to a driver / requests; revenue per hour per zone.
- Steps to a multiple m of base = ceil(ln m / ln 1.2): 4 steps for 2x, 7 steps for 3x.
- Guardrails: share of time at the absolute cap, complaint rate, cancellation rate.

**Risks:**
- A per-update cap does not stop a gradual climb: 2x base is reached in 4 minutes at a 60-second interval.
- Feedback loops: higher prices reduce demand, which lowers the signal that justified the price.
- Interference across zones makes simple A/B tests biased; use switchback or zone-level designs.
- Fairness and public trust (surge during emergencies); agree policy with the business, and ask compliance and legal about limits.
- Elasticity learned from narrow past price ranges may not hold outside it.

**What the interviewer scores:**
- Strong: 144,000 decisions and 248.83, and notes that a step cap is not a level cap.
- Strong: rule-based baseline, forecast plus elasticity, guardrails, switchback testing.
- Strong: raises fairness and legal limits as questions for the right team.
- Weak: "reinforcement learning to maximise revenue" with no guardrails, baseline or test design.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "The model sets the price each minute and the 20% rule keeps it safe."
- Strong: "That is 144,000 decisions a day. A 20% step cap sounds safe, but five steps take 100 to 248.83 and four already pass 2x, so I would add an absolute cap chosen with the business and check with legal what limits apply. I would start with a smoothed demand-to-supply rule, test against it with a switchback design by zone and time, and watch complaint rate and time at the cap."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- How do you choose the absolute cap? From the business's tolerance, observed price response and complaint data, and legal or policy limits (ask compliance); I would start low and raise it only with evidence.
- Why not a user-level A/B test? Riders in a zone share the same supply, so treatment spills over; time-slice or zone randomisation handles it better.
- What about a downward step? Dropping 20% three times from 207.36 only gets to 106.17, so recovery is slow too; consider asymmetric limits.

**Common mistakes:**
- Treating 20% per step as a 20% limit overall.
- Forgetting the price may be applied every minute for 24 hours (144,000 decisions).
- Running user-level A/B tests where supply is shared.
- Learning elasticity only from the price range already used.

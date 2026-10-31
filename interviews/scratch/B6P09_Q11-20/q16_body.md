**Say this first (1 line):** The scale-up to 11,667 implies conversions grew 16.7% while first-party orders were flat, so it is probably wrong: users who allow tracking are not a random 60%, and the old 10,000 was never the truth either; I would estimate true conversions with a calibrated first-party anchor and a holdout test, then recalibrate the bid model to that.

**Clarifying questions:**
- What did "attributed" mean before and after (a click-through only, view-through, platform-modelled credit)? The platform may have changed its method, not only the data.
- Is the 60% consent share stable across days and segments? A moving share breaks any single scale factor.
- Do I have first-party orders by source, and a way to tie some of them to ad exposure (logged-in users, coupon codes, surveys)? These are the anchors.
- Is there any holdout or geo test running? It gives an unbiased incrementality baseline.
- What does the bid model predict and from what labels? It decides what needs recalibration.

**Approach:**
1. Do the arithmetic. 7,000 / 10,000 means a 30% drop; 7,000 / 0.6 = 11,667, which is 16.7% above 10,000.
2. Show why it is suspicious. First-party total orders are flat at 25,000 a day. Reported attribution covered 10,000 / 25,000 = 40% of orders before and 7,000 / 25,000 = 28% after. A scale-up that lands above the old figure claims advertising delivered more conversions the day privacy changed, with nothing else moving. The more likely story is a mix: consenting users convert differently from non-consenting ones, and the platform may fill some gaps with modelled credit. In the run, retention of 70% against a consent share of 60% implies consenters were 16.7% more attributable, which is exactly the 16.7% error.
3. Estimate true conversions properly. Use a first-party anchor: total orders by day, and orders from segments where exposure can be linked for all users (logged-in customers, coupon codes), to measure what share of true conversions the new reporting sees. Then divide by that share, per segment. In a simulation with consenters converting 1.4 times as often, the naive scale-up overstates by about 12%, while the logged-in-segment ratio is within 1%.
4. Validate with experiments. Run a geo holdout or randomised holdout (ask the measurement and platform teams what is allowed) to get incremental conversions independent of tracking; compare with the reconstructed number. Use marketing mix modelling only as a slow cross-check.
5. Recalibrate bidding. The bid model learned from labels that were 40% of orders; now labels are 28%. Do not simply retrain on the new, thinner labels. Add a calibration layer that maps predicted probability to estimated true conversion rate, fitted on the anchored estimate, and refit weekly with a stability guard on the bid change.
6. Checks: consent share by day and segment, ratio of attributed to first-party orders over time, an A/A comparison, sensitivity of the estimate to the anchor assumption, and a before/after comparison on a campaign with no change.

**Metrics:**
- Attributed share = attributed conversions / first-party orders (40% before, 28% after).
- Visible share = conversions seen by new reporting / true conversions in the anchor segment; true estimate = reported / visible share.
- Calibration = predicted conversions / estimated true conversions by decile; aim near 1 after the fix.
- Guardrails: spend change per day, cost per estimated true conversion, and bid change cap.

**Risks:**
- The anchor segment (logged-in users) may differ from everyone, so the estimate carries that bias; report a range.
- Assuming the old 10,000 was complete; it included its own gaps and modelled credit.
- Retraining on 28% labels without correction lowers bids and loses auctions for no reason.
- Treating consent as exogenous: whoever clicks "allow" may behave differently, which is the whole problem.
- Any rule about what data may be used under the new consent state is a question for the privacy and legal teams.

**What the interviewer scores:**
- Strong: computes 30%, 11,667 and 16.7%, and uses the flat 25,000 orders to challenge the scale-up.
- Strong: names consent selection and a first-party anchor, and states what the anchor assumes.
- Strong: proposes a holdout for incrementality and a calibration layer instead of naive retraining.
- Weak: "divide by 0.6", or "conversions fell 30%, so performance fell 30%".

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Only 60% allow tracking, so I scale up 7,000 by 1 over 0.6 and get 11,667."
- Strong: "That says conversions rose 16.7% on a day when first-party orders did not move, so it is wrong. Reporting kept 70% of volume with 60% consent, which suggests consenters convert more. I would anchor on first-party orders and a segment where we see everyone, measure the visible share, and check it with a geo holdout. Then I would add a calibration layer to the bid model and cap day-to-day bid changes."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if no first-party anchor exists? Use a holdout or geo experiment as the anchor, and mark all figures as ranges.
- Should you use the modelled conversions the platform reports? Treat them as an input to be validated against your holdout, not as truth; ask the platform team how they are produced.
- How often do you recalibrate? Weekly at first, with an alert when the visible share moves more than a set band.

**Common mistakes:**
- Scaling by consent share alone.
- Believing the old reporting was complete.
- Retraining directly on the thin labels.
- Changing bids by a large step in one day.

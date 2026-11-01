**Say this first (1 line):** A bias that jumps from zero to +15% right after a price cut is a structural break, not noise, so I confirm it with bias and change-point checks, patch the forecast with a short-lag bias correction and manual overrides, and retrain once I have enough post-break weeks.

**Clarifying questions:**
- Exactly when did the competitor cut and when did we change our own price? The break date tells me how many post-break weeks exist.
- Is price an input to the model today? If not, it is blind to this cause; if yes, the new price range may be outside what it saw.
- Is the over-forecast uniform across products and regions, or concentrated where the competitor competes? It decides between one global correction and segment corrections.
- What do the forecasts drive (stock, purchase orders, markdown)? Over-forecast of 15% means excess stock, and I need its cost.
- Are there other changes in that window (promotions, stock-outs that censor demand, tracking changes)? These look like a break too.

**Approach:**
1. Separate bias from error size: report bias = sum(forecast - actual) / sum(actual) next to MAPE. Bias near 0 before, +15% after, is a level shift; MAPE alone hides its direction.
2. Locate the break: plot weekly bias, run a CUSUM or change-point check, and line the date up with the competitor and own price events.
3. Rule out data errors and stock-outs (censored demand would push actuals down and create a false over-forecast).
4. Segment: which categories and regions carry the bias? Price-sensitive segments first.
5. Interim fix before retraining: multiply the forecast by a rolling forecast-to-actual ratio from the last few matured weeks (lagged so only known actuals are used), let planners override, and widen safety-stock logic so that it is not driven by the bad point forecast.
6. Model fix: add price and competitor-price ratio as features; with only a few weeks post-break use a hierarchical or elasticity-prior approach, or train on all history with a regime indicator and interaction terms.
7. Monitor: weekly bias alert (not only MAPE), a break detector, and a rule that any pricing change notifies the forecasting team.

**Metrics:**
- Bias = (sum of forecasts - sum of actuals) / sum of actuals over a window.
- MAPE = mean over weeks of |forecast - actual| / actual (state the treatment of zero actuals).
- Tracking signal or CUSUM of percentage error for break detection.
- Business guardrails: excess stock weeks of cover, stock-out rate, markdown cost.

**Risks:**
- Retraining immediately on a few weeks can overfit noise; retraining late keeps the bias.
- A rolling correction lags a second break and can over-correct once the model is fixed.
- Stock-outs censor demand; the data can mislead.
- Price effects differ by category; one global multiplier fixes the total but not the mix.

**What the interviewer scores:**
- Strong: names bias separately from MAPE and ties the break to the price events. Weak: "retrain".
- Strong: gives an interim control that works with little data. Weak: waits for data.
- Strong: asks what the forecast decides, and sizes the business risk. Weak: only talks about the model.
- Strong: monitors bias and breaks. Weak: monitors accuracy only.

**Example:** (illustrative) Percentage errors are roughly Normal. If the spread gives a MAPE of 11% at zero bias, adding a +15% bias gives a MAPE of about 16.9%, so the prompt's move from 11% to 18% is plausible and is mostly the bias. In a 120-week simulation with the break at week 60 (demand ends up 1/1.15 of what the old pattern implies): before the break the bias is -0.9% and the MAPE 12.3%; after it the bias is +14.6% and the MAPE 17.1%. A CUSUM alarm fires at week 66, six weeks after the break. A rolling forecast-to-actual ratio lagged by two weeks brings the post-break bias to +2.9% and the MAPE to 12.5% without any retraining. Weak: "MAPE went up, retrain the model on the last month." Strong: "Bias is +15% since the price cut; I patch with a lagged ratio and overrides now and add price features once there are enough weeks."

**Code:**

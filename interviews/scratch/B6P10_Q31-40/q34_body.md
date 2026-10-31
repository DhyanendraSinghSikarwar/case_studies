**Say this first (1 line):** The critical ratio is 30 / (30 + 20) = 0.6, so I stock the 60th percentile of demand, 100 + 0.2533 x 20 = about 105 units, a little above the mean.

**Clarifying questions:**
- Is the 20 rupees per unsold unit the net loss (cost minus salvage)? It is the overage cost in the formula.
- Is the 30 rupees the margin lost, with no goodwill effect? A lost customer may cost more.
- Is the 100 and 20 measured on sales or on true demand? Sales are censored when you stock out, so demand is understated.
- How long is the shelf life and how often can I reorder? One-period stocking needs a single order each day.
- Is demand for this store-item-day normal enough, and does it vary by weekday and weather? The shape affects the answer.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data 5, baseline 5, model 8, evaluation 7, rollout and monitoring 7, risks and cost 4):**
1. Clarify and frame: a one-period stocking decision, so forecast a distribution, not a point.
2. Metrics and guardrails: expected cost = 20 x unsold + 30 x missed sales, fill rate, waste share, forecast calibration.
3. Data and labels: daily sales per store and item, with stock-out flags, promotions, weekday, weather; correct for censoring.
4. Baseline first: same weekday last week or a seven-day average, with an error-based standard deviation.
5. Model and trade-offs: a model for the mean (gradient boosting or a simple regression) and a calibrated spread; or a direct 0.6 quantile model. Critical ratio 30 / 50 = 0.6, z = 0.2533, stock 105.07. Stock 105 or 106 differs by under a rupee a day in expected cost; round to what the pack size allows. Compare with stocking the mean: expected cost 398.94 against 386.34, about 12.6 rupees a day better (illustrative).
6. Evaluation: backtest the whole decision (cost with the rule against cost with the baseline), and check that demand stays below stock on about 60% of days.
7. Launch: A/B across stores, perhaps 10% of stores first, compare waste and fill rate; keep a manual override.
8. Monitoring and cost: weekly calibration of the 0.6 quantile, drift in demand spread, shrink the model back to the baseline if it loses.

**Metrics:**
- Service level = days with demand <= stock / days (target 0.6 from the ratio, a result, not a goal to set separately).
- Expected daily cost = (20 x units unsold + 30 x units short) per store-item-day.
- Guardrails: waste share = unsold units / units stocked, fill rate = units sold / units demanded.

**Risks:**
- Censored sales understate demand and the spread; if the real spread is 30, the stock would be 107.6.
- Normality fails for lumpy or intermittent items.
- Margin and waste costs differ by item; one ratio does not fit all.
- Substitution: when this item is out, demand moves to another.

**What the interviewer scores:**
- Strong: 0.6, z = 0.2533, 105, and explains why the answer is above the mean.
- Strong: raises censoring and calibrates a quantile, then tests the decision, not just forecast error.
- Weak: stocks the mean or the mean plus a safety factor with no cost logic.

**Example:** Illustrative numbers. 30 / 50 = 0.6; z = 0.2533; 100 + 0.2533 x 20 = 105.07.
- Weak: "Forecast demand of 100 and stock 100, maybe a bit more to be safe."
- Strong: "A missed sale costs 30 and an unsold unit costs 20, so the critical ratio is 0.6 and I stock the 60th percentile, about 105. I would check that the spread of 20 comes from true demand, not stocked-out sales."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *What if the missed sale cost doubles to 60?* The ratio becomes 60 / 80 = 0.75, z = 0.674, stock about 113.5.
- *What about a lead time of several days?* Use demand over the lead time plus review period and the same ratio logic.

**Common mistakes:** Using the ratio the wrong way (20 / 50). Stocking the mean. Ignoring censored data. Reporting accuracy of the forecast without testing the cost.

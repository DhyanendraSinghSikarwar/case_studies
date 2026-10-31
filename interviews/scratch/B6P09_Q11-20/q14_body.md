**Say this first (1 line):** Sales are not demand when the shelf is empty: on the 5 stock-out days, 400 units in 10 hours implies about 560 for the full 14 hours, so true average demand is about 557 a day, not the 443 the forecast uses, and I would model demand with a censored likelihood and handle the price change as a separate effect.

**Clarifying questions:**
- Is stock-out time recorded per unit (a timestamp of the last sale and of availability), or only inferred from daily totals? Exact hours-in-stock is the key input.
- Was the product the only variant, or could customers switch to a substitute when it sold out? Substitution moves demand elsewhere.
- Was the price constant, and was it promoted on the sell-out days? A promotion explains both fast sell-out and high demand.
- Is the hourly demand shape known (for example from a similar product)? The flat assumption can be tested.
- What does the forecast drive: reorder quantity, markdown, or safety stock? The cost of overstock versus lost sales sets how much the 114-unit gap matters.

**Approach:**
1. Do the arithmetic. Stock-out at 18:00 means 10 open hours (08:00 to 18:00), so 400 / 10 = 40 units an hour and 40 x 14 = 560 for the day. The 7-day demand is (5 x 560 + 560 + 540) / 7 = 557.1; the sales average is (5 x 400 + 560 + 540) / 7 = 442.9. The forecast understates by about 20.5%.
2. Test the flat-hour assumption. The two non-stock-out days give 40.0 and 38.6 units an hour, which is consistent with 40 but does not show the shape within a day. If the last 4 hours are twice as busy, demand is 720 on a day with the same 400 sold by 18:00, so flat extrapolation says 560 and understates by 160 (see the run). Use intraday sales on non-stock-out days to estimate the hourly profile.
3. Model with censoring. Treat each day's sales as min(demand, stock). Fit demand with a likelihood that, for a censored day, contributes P(demand at least stock) and for an uncensored day the density. Use hours-in-stock as exposure in a Poisson or negative-binomial hourly model, with day-of-week, price, promotion and season terms.
4. Be careful with only 7 days. With 2 uncensored days, a censored-normal fit in the run gives mean 550 but an overconfident sd of 10; do not trust that sd. Pool across similar products or weeks (hierarchical model) to stabilise it.
5. Price change in the same week. Price and stock-out are confounded (a price cut sells out sooner). Estimate price elasticity from a model with price as a covariate and the censored likelihood, using only in-stock hours, and compare same hours across price levels. If you can, run a randomised price test across stores or customers, and flag cannibalisation of substitutes.
6. Use the forecast properly. Forecast demand, not sales; then choose stock by the newsvendor logic (cost of an unsold unit versus a lost sale), using a quantile of demand rather than the mean.

**Metrics:**
- Uncensored demand = units sold / open hours before stock-out x selling hours (560 on a stock-out day).
- Censoring rate = days with stock-out / days (5 of 7 = 71%).
- Forecast bias = (forecast - demand estimate) / demand estimate on days with a stock-out, and a lost-sales estimate = demand estimate - sales.
- Service level = share of days with no stock-out; guardrails: overstock cost and markdown rate.

**Risks:**
- Flat hourly demand is wrong for most products; an evening peak makes the estimate too low, a morning peak too high.
- Shoppers may leave the site on an out-of-stock page, so demand after the stock-out is lower than the early-hours rate would suggest, or they buy a substitute.
- Planning stock from the 443 average repeats the stock-out and trains the next forecast on even more censored data.
- A price change with a stock-out in the same week cannot be separated with 7 days of data.

**What the interviewer scores:**
- Strong: gets 560, 557 and the 20.5% gap, and labels flat demand as an assumption.
- Strong: names censoring, a likelihood that handles it, and exposure (hours in stock).
- Strong: separates the price effect and mentions substitution and the newsvendor decision.
- Weak: "average the sales" or "just fill in the missing hours with the mean".

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Average sales are 443, so I will plan 443 plus a safety margin."
- Strong: "On stock-out days we sold 40 an hour for 10 hours, so with flat demand that is 560 a day, and the true weekly average is about 557, around 20% above what the forecast uses. I would test the flat assumption on intraday data, fit demand with a censored likelihood using hours in stock, and plan stock at a high quantile, because a lost sale and an unsold unit have different costs."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if the product sells out before 08:00 of the next day's restock? Then the day's window is shorter; use actual open and stock hours as exposure.
- How would you check the flat assumption without intraday data? You cannot fully; ask engineering for hourly order logs and check a similar product that did not sell out.
- How would you size the stock? Pick the quantile of demand where the cost of the next unit unsold equals the margin lost per unit missed; the mean is rarely right.

**Common mistakes:**
- Using sales as demand.
- Filling the stock-out hours with zeros or dropping those days.
- Ignoring that a price change and a stock-out occurred together.
- Trusting a variance estimated from two uncensored days.

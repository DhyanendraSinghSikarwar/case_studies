**Say this first (1 line):** Expected surplus at bids 4, 6, 7, 8, 9, 10 is 1.20, 1.80, 1.80, 1.50, 0.88 and 0.00, so bids 6 and 7 tie at 1.80 per auction; I would break the tie by what the campaign is short of (budget favours 6, volume favours 7), and I would keep re-estimating the win curve because it moves.

**Clarifying questions:**
- Is the budget the binding constraint, or is there a delivery commitment (a minimum number of impressions)? It decides the tie.
- Does the exchange tell us the winning price or minimum bid to win? It determines whether the win curve is censored.
- How many logged auctions sit behind each of the six estimates? With few auctions each point carries a wide range.
- Is the value of 10 per impression certain and the same on every impression? Value uncertainty changes how much to shade.
- How fast do competitors adapt after the change to first price? It sets how often the curve must be refit.

**Approach:**
1. Compute surplus = (10 - bid) x win probability: bid 4: 6 x 0.20 = 1.20; 6: 4 x 0.45 = 1.80; 7: 3 x 0.60 = 1.80; 8: 2 x 0.75 = 1.50; 9: 1 x 0.88 = 0.88; 10: 0 x 0.95 = 0.
2. Name the best bid: 6 and 7 tie at 1.80 per auction, which is 1,800 per 1,000 auctions either way.
3. Break the tie with the next constraint. Spend per auction is 6 x 0.45 = 2.70 at a bid of 6 and 7 x 0.60 = 4.20 at 7. Going from 6 to 7 buys 0.15 more win probability for 1.50 more spend, a marginal 10 per extra win (7 x 0.60 - 6 x 0.45 = 1.5, divided by 0.15), exactly the value, so it adds no surplus. If budget is binding, bid 6 (surplus per unit of spend is 0.667 versus 0.429) and use the saved spend elsewhere. If there is a volume commitment or a learning phase, bid 7 gets 600 wins per 1,000 auctions instead of 450 at no loss of surplus.
4. Do not trust the grid to the cent. The ranges at 400 auctions per point are about +/- 0.05 in win probability, which is +/- 0.20 in surplus at a bid of 6 and +/- 0.14 at 7. The tie is inside the noise. A linear guess at 6.5 gives 1.84 but that is an untested interpolation.
5. Estimate the win curve from logs: for every auction record bid, win or loss, and (if available) the winning price; fit a monotone curve (isotonic or a logistic on bid or log bid), or a censored model if only wins reveal prices. Add a small randomised bid perturbation so the curve is identified across the range you may use.
6. Spot when it breaks: compare predicted win rate with live win rate by bid bucket every day. In the run a competitor shift of one unit right makes the old 7 win like the old 6 (60% predicted, 45% live): z = -6.1 on 400 auctions. After such a shift the best bid on the shifted curve is 7 with surplus 1.35.
7. Rules for retraining: refit when the gap exceeds an agreed number of standard errors for several buckets, and always after an exchange rule change.
8. Guardrails: never bid above value (10), keep the budget pacing in view, and log the bids so the next curve can be estimated.

**Metrics:**
- Expected surplus per auction = (value - bid) x P(win | bid).
- Win rate by bid bucket, predicted versus live; spend per win; effective cost per impression won.
- Surplus per 1,000 auctions and per unit of spend.
- Guardrails: delivery against commitment, budget exhaustion time, curve gap (live minus predicted).

**Risks:**
- The win curve is estimated, not known; the best bid is a guess with an error bar.
- Censoring: if you only learn the clearing price on wins, extrapolation below your lowest logged bid is unsupported.
- Competitors change their bidding in response to yours.
- Paying your bid means any overestimate of the win curve costs money directly.
- Value per impression varies; one value for all impressions is a simplification.

**What the interviewer scores:**
- Strong: gets the six surplus numbers and sees the tie at 6 and 7.
- Strong: breaks the tie with budget versus volume and shows the marginal cost of 10 per extra win.
- Strong: explains how to estimate a censored win curve and how to detect a break.
- Weak: "bid your value" (a second-price habit); a single best bid with no uncertainty.

**Example:** Illustrative numbers from the run. Surplus 1.20, 1.80, 1.80, 1.50, 0.88, 0.00; per 1,000 auctions a bid of 6 wins 450, spends 2,700 and earns surplus 1,800; a bid of 7 wins 600, spends 4,200 and earns 1,800.
- Weak: "Bid 10, it is worth ten."
- Strong: "In first price I pay my bid, so I shade. Surplus peaks at 1.80 for both 6 and 7. Going to 7 buys 150 extra wins per 1,000 for 1,500 extra spend, 10 each, so no surplus gain. With a budget limit I bid 6; with a delivery target I bid 7. I will check the win curve daily and refit when it moves."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *What if the value is uncertain?* Shade on the expected value, and consider a conservative multiplier until the value model is calibrated.
- *Would you change the bid per impression?* Yes, bid is a function of predicted value and the win curve per segment.
- *Is there a bid between 6 and 7 that beats both?* Possibly, but it is not in the data; test it through randomised bid perturbation.

**Common mistakes:**
- Bidding value in first price.
- Treating a tie as a result and ignoring budget or volume.
- Extrapolating the win curve outside logged bids.
- Not monitoring the curve after the format change.

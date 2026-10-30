**Follow-ups:**
- Why not just wait six weeks and retrain? Six weeks at +15% bias is real excess stock; the interim patch costs little and is reversible.
- How would you pick the correction window? Short enough to track the new level (4 to 6 weeks), long enough that noise does not move it; test it on past breaks and check how it behaves after the model is retrained.
- How do you know the break is price and not a stock-out? Check on-hand stock and sales per day; stock-outs show censored sales, price shows lower demand with stock available.

**Common mistakes:**
- Looking at MAPE only and missing that the error is one-sided.
- Retraining at once on too few weeks and swapping one bias for another.
- Leaving the rolling correction on after the model is fixed (double correction).
- Ignoring stock-out censoring.
- Not telling planners which forecasts are being overridden and why.

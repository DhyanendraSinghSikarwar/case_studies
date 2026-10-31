**Say this first (1 line):** Raw clicks mix real users with invalid traffic, so a model trained on them learns a blended conversion rate of 1.8% instead of the 2.0% on valid clicks, and it learns a publisher's invalid share as if it were user behaviour; I would train on valid-only labels that have matured past the 3-day delay and tell the account team which numbers are provisional.

**Clarifying questions:**
- Who pays for invalid clicks: do we pay first and get a credit after 3 days, or are they filtered before billing? It decides whether the right bid uses 1.8% or 2.0%.
- Is the invalid flag a rule, a vendor score or manual review? Late, model-based flags change over time and need versioning.
- Does the 3-day delay apply to the invalid label only, or also to conversions (which usually arrive later)? Both censor the newest data.
- Does the invalid share differ by publisher, placement or hour? A shared share is a small bias; a varying share distorts ranking between publishers.
- What is the value per conversion and the bidding rule? We need it to price the bias.

**Approach:**
1. Do the arithmetic. 10% invalid, conversion 2.0% on valid, 0% on invalid: blended = 0.9 x 2.0% = 1.8%. With an illustrative value of 50 per conversion, the raw bid per click is 0.90 and the valid-only bid is 1.00, a 10% underbid.
2. Say which direction the bias goes. If invalid clicks are credited back, we are only paying for valid ones, so the right value of a billed click is the valid rate (2.0%). A raw-trained model underbids by 10% on average. If they are not credited, the blended 1.8% is the true value of what we pay for, and the fix is to push for filtering, not to adjust the model. Ask billing which case holds.
3. Publisher differences matter more than the average. A publisher with 2% invalid shows 1.96%, one with 30% shows 1.4%, with the same real users. The raw model punishes the second publisher for traffic quality, which is acceptable if you are billed for it and wrong if you are credited.
4. Handle the delay. A click from today has no invalid flag yet, so it looks valid and unconverted when it is invalid. Recent days therefore show a lower conversion rate than matured days (in the run, 1.71% versus 1.96% on the same traffic mix). Train on matured clicks only (age at least 3 days, plus the conversion window), or train two models: P(invalid) from matured data, and P(convert | valid).
5. Combine at serving. Expected value per click = P(valid) x P(convert | valid) x value, where P(valid) comes from a publisher and placement model. Use a conservative P(valid) for new sources.
6. Tell the account team plainly: figures from the last 3 days are provisional and usually revised; we will report valid-only conversion rate, invalid share by publisher, and the credit amount; and publishers with a high invalid share may see lower bids until their traffic matures. Route any contract or billing wording through the commercial and legal owners.

**Metrics:**
- Invalid share = invalid clicks / all clicks = 200,000 / 2,000,000 = 10%.
- Valid CVR = conversions on valid clicks / valid clicks (2.0% in the sample); blended CVR = conversions / all clicks (1.8%).
- Label maturity: share of clicks older than 3 days whose flag is final; revision rate = clicks whose label changes after first being scored.
- Calibration by publisher on matured data: predicted conversions / actual conversions per decile.
- Guardrails: spend per valid conversion, credits received per week, bid change versus last week by publisher.

**Risks:**
- Training on the newest days: the recent label bias makes the model underbid just when traffic is shifting.
- Dropping unflagged recent clicks removes the very traffic whose quality is unknown, so a new bad source looks fine until day 3.
- A model that learns "publisher B converts less" when the cause is invalid traffic will keep underbidding after the publisher cleans up.
- Sample rates (2.0%, 10%) are from a sample; check their interval before quoting them to a publisher.

**What the interviewer scores:**
- Strong: derives 1.8% from 90% x 2.0% and links the bid error to the billing treatment.
- Strong: names label delay as a censoring problem and trains on matured data or models the flag.
- Strong: separates invalid-traffic share (a source property) from user conversion behaviour.
- Weak: "just remove the bots"; ignoring the delay; saying the bias is always 10% for every publisher.

**Example:** Illustrative numbers, value 50 per conversion. Weak versus strong:
- Weak: "I would filter out invalid clicks and retrain on the full data."
- Strong: "On raw clicks the model sees 1.8% and bids 0.90; the valid-only rate is 2.0%, so bid 1.00, assuming invalid clicks are credited back, which I would confirm with billing. The last 3 days are not yet flagged, so I train on matured clicks, and I model the chance a click is valid per publisher. I would tell the account team that recent numbers are provisional and that bids on a high-invalid publisher will be lower until its flags settle."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- How would you use the unflagged recent data? Add a P(invalid) model trained on matured clicks and weight recent clicks by predicted P(valid); do not treat them as clean.
- What if the flag rule changes mid-quarter? Version the rule, retrain per version, and re-score history so training labels are consistent.
- What if conversions also arrive late? Use a delayed-feedback approach (train only on clicks older than the conversion window, or model the delay); the general method is the same.

**Common mistakes:**
- Training on the most recent days and treating missing flags as "valid".
- Assuming the bias is the same for every publisher.
- Reporting 1.8% to the publisher as their conversion quality without separating invalid share.
- Forgetting to ask who bears the cost of invalid clicks.

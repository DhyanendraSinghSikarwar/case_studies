**Say this first (1 line):** Flagging 20,000 orders that hold 12,500 of the 25,000 returns gives a precision of 62.5%, and calling them nets 450,000 - 120,000 = 330,000 rupees a day, but the 40% rescue rate comes from a small pilot and the benefit is the shipping saving only, so I would size the gain with an interval and expand calls only where the risk exceeds 16.7%.

**Clarifying questions:**
- Was the 2,000-order pilot on high-risk orders or random ones, and how many were would-be returns? A rescue rate from random orders may not hold on the flagged group, and the number of would-be returns sets the pilot's uncertainty.
- What does "rescued" mean: the customer confirmed and the parcel was delivered and paid? Define it so a confirmation that later fails is not counted.
- Is 90 rupees the whole cost of a return, or only forward and return shipping? Packaging, handling and lost inventory time could raise it.
- Are there other actions besides a call (messages, prepaid discount, address check)? Cheaper actions change the break-even.
- Do customers dislike calls, and does the call delay dispatch? Both are guardrails.

**Approach:**
1. Clarify and frame. Goal: lower return-to-origin cost by intervening on risky cash-on-delivery orders before dispatch. The decision is whom to call, not only who is risky.
2. Metrics and guardrails. Net saving per day, precision of the flag (returns / flagged), recall (share of returns flagged), rescue rate, delivery delay. Guardrails: conversion of good orders, customer complaints, dispatch delay, share of customers called repeatedly.
3. Data and labels. Label = order returned to origin, observed after delivery attempts (a delay of days, so use matured cohorts). Features: pincode history, order value, customer history, time, address quality. Careful: the pilot's outcomes are changed by the call itself, so train on pre-intervention or randomised holdout orders.
4. Baseline first. Rules by pincode and order value; a simple logistic model. Compare precision at 20% flagged.
5. Model and trade-offs. Gradient-boosted trees or logistic regression with calibrated probabilities. Call when probability x rescue rate x 90 > 6, i.e. risk above 6 / (0.40 x 90) = 16.7% (see the code). The unflagged group runs at 15.6%, below that, so calling it loses money (marginal value -30,000 per day). The trade-off is call volume versus returns prevented.
6. Evaluation. Offline: precision and recall at the cut, lift by decile, calibration; check the projected 50% capture on a recent matured period. Online: randomise a holdout (some flagged orders not called) to measure the true rescue effect, which is the number the business case needs.
7. Launch and experiment plan. Start with the top decile, widen to the top 20% if the randomised rescue rate holds; keep a 5% holdout permanently.
8. Monitoring, retraining and risks. Monitor precision by pincode, rescue rate, call cost; retrain monthly on matured labels; watch for customers gaming the process.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 6, 4, 10, 7, 5, 5.

**Metrics:**
- Return-to-origin orders = 100,000 x 25% = 25,000; flagged = 20,000; returns in flagged = 12,500.
- Precision of the flag = returns among flagged / flagged = 12,500 / 20,000 = 62.5%. Recall = 12,500 / 25,000 = 50%.
- Net saving per day = rescued orders x 90 - calls x 6 = (12,500 x 0.40 x 90) - (20,000 x 6) = 450,000 - 120,000 = 330,000 rupees.
- Break-even return probability for a call = call cost / (rescue rate x saving per rescue) = 6 / (0.40 x 90) = 16.7%.
- Guardrails: good-order conversion, complaint rate, dispatch delay.

**Risks:**
- Sample versus projection: the 40% rescue rate is a pilot sample and the 50% capture is a back-test projection. With 500 would-be returns in the pilot (my assumption) the rescue interval is about 36% to 44%, so net ranges about 282,000 to 378,000.
- Selection: calling changes behaviour and hides what would have happened; only a randomised holdout measures it.
- Saving only shipping: ignoring lost sales from friction or complaints from customers who did not want a call.
- Drift: pincode risk changes with festivals, couriers and weather.
- Calling customers and using personal data: ask compliance and legal about consent and rules for calls and profiling.

**What the interviewer scores:**
- Strong: 62.5% precision, 330,000 net, and checks the marginal call against a 16.7% break-even.
- Strong: separates sample (pilot rescue) from projection (50% capture), and asks for a randomised holdout.
- Strong: guardrails for good-order conversion and customer experience.
- Weak: "flag the risky orders and call them all" with no break-even, no uncertainty, no holdout.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "A model flags 20% of orders; we call them and save money."
- Strong: "25,000 of 100,000 orders return, the flag holds 12,500 of them, so precision is 62.5%. Calling 20,000 costs 120,000 and rescues 5,000 orders worth 450,000, net 330,000 a day. The 40% rescue is from a pilot sample, so I would show a range, and a call only pays when return risk is above 16.7%, so I would not call the other 80,000 whose risk is 15.6%. I would keep a randomised holdout to measure the real effect."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Should you call everyone at 16.7% or above, not just the top 20%? Yes, call by calibrated probability, not by a fixed 20%; the top 20% is a convenient cut, and the exact cut should come from the marginal rule with a safety margin for uncertainty.
- What if the rescue rate is only 10%? Below the 10.7% break-even for the flagged group, calling loses money; switch to cheaper actions such as a message or prepaid nudge.
- How would you check the 50% capture claim? Recompute capture on a recent matured period out of time and compare; it was a back-test, so it can be optimistic.

**Common mistakes:**
- Treating the pilot's 40% as a fixed fact.
- Forgetting that the 90-rupee saving ignores other costs and benefits.
- Calling a group below the break-even risk.
- Training on outcomes that were changed by the intervention.

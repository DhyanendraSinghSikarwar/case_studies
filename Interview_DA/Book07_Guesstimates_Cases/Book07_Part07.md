# Book 7 — Guesstimates, Case Studies & Business Metrics | Part 7: Product Analytics Cases (Feature Launch, Funnel Drop) 🔴

**Target:** 70 questions | **Actual:** 71 questions
**Scope:** product analytics cases: success metrics and guardrails for feature launches, funnel conversion and drop-off diagnosis, cohort and retention readouts, cannibalisation and incrementality, rollout decisions, with inline data wherever a figure can be derived; A/B test theory is in Book 5 and generic revenue-drop cases are in Part 5.

### Q1 ⭐⭐⭐ 🟢 How would you define the success metric for a new one-tap "reorder" feature on a food delivery app?
**Asked at:** commonly asked (no company-specific report found); "how would you measure a feature" appears on prep-site banks (unverified).
**What the interviewer is checking:** Whether you tie the feature to a business goal and pick one clear primary metric, not a list of everything.
**Say this in the interview:** "I would first ask what reorder is for: more repeat orders from existing customers with less effort. My primary metric is incremental orders per active customer per month from users exposed to reorder, with order-cancellation and refund rate as guardrails."

**Clarify first:**
- What is the goal: more repeat orders, faster checkout, or retention? I will assume repeat orders.
- Who sees it: all users or only those with a past order? Where is the button (home, order history)?
- Is the launch an A/B test or a full rollout? That decides how I prove impact.

**Structure:**
- Goal: more orders from repeat customers, without hurting order quality.
- Primary metric: orders per active user per 30 days (compared against a holdout group that does not see the button).
- Guardrails (things that must not get worse): cancellation rate, refund/complaint rate, delivery-time promise met, average order value.
- Diagnostic metrics (explain why it moved): reorder-button tap rate, tap-to-order conversion, share of orders that are reorders.

**What I would check, in order:**
1. Adoption: share of eligible users who tapped reorder (formula: users who tapped / eligible users).
2. Impact: orders per user, treatment minus holdout (not "reorder users vs others", which is biased).
3. Guardrails: did cancellations or wrong-item complaints rise (a one-tap reorder may repeat an unavailable item)?

**If the data shows...:** High tap rate but flat orders per user: reorder only replaced orders customers would have placed anyway (no impact). Orders up but cancellations up: the feature reorders stale items; fix availability checks.

**Recommendation:** Report incremental orders per user from a holdout, with guardrails, over at least two ordering cycles (about 4 weeks), then decide on full rollout.

**Likely follow-ups:** 1) *Why not just use number of taps?* Taps measure adoption, not business value. 2) *Why a holdout?* Without it you cannot separate new orders from orders that would have happened anyway.
**Common mistakes / traps:** Picking "reorder button clicks" as success; comparing users of the feature with non-users; ignoring guardrails.

### Q2 ⭐⭐⭐ 🟢 What is the difference between a primary metric, a guardrail metric and a diagnostic metric when judging a feature launch?
**Asked at:** commonly asked (no company-specific report found); the primary/guardrail split is a standard prep-site question (PracHub, Dataford; unverified).
**What the interviewer is checking:** Whether you separate "did we win", "did we break anything" and "why did it move".
**Say this in the interview:** "The primary metric decides the launch, guardrails protect what must not get worse, and diagnostics explain the movement but never decide on their own."

**Explain simply:**
- Primary metric: the one number that says the feature worked, tied to the goal. Example for an HR leave app: share of leave requests filed in the app.
- Guardrail metric: a number that must not get worse even if the primary improves. Example: leave-approval turnaround time, error rate in leave balance, complaints to HR.
- Diagnostic metric: a supporting number that shows where or why the primary moved. Example: how many users open the leave screen, how many abandon the form.
- Decision rule: ship if primary improves by a meaningful amount and no guardrail crosses its limit; diagnostics guide the fix.

**Worked mini-example:** Food app one-tap reorder. Primary: orders per user per month. Guardrail: refund rate must stay under, say, +0.2 percentage points. Diagnostic: tap-to-order conversion.

**Practice step:** Take any app you use, name its newest feature, and write one metric of each type in one line.

**Likely follow-ups:** 1) *Can a metric be both?* A metric can be primary for one feature and guardrail for another; label it for this launch. 2) *How many primaries?* One, to avoid cherry-picking.
**Common mistakes / traps:** Having five "primary" metrics; treating guardrails as optional; letting a diagnostic improvement justify launch.

### Q3 ⭐⭐⭐ 🟢 What is a conversion funnel, and how do you compute step conversion and overall conversion from the counts at each step?
**Asked at:** commonly asked (no company-specific report found); funnel analysis is reported for Fractal and PhonePe-style rounds in the internal research and prep sites (unverified).
**What the interviewer is checking:** Basic funnel arithmetic and clarity on the denominator.
**Say this in the interview:** "A funnel is the ordered list of steps a user must pass to reach a goal. Step conversion is the users at a step divided by users at the previous step; overall conversion is the last step divided by the first."

**Explain simply:**
- Funnel: steps in order, for example visit, view product, add to cart, pay. Each step has fewer users than the one before.
- Step conversion = users at this step / users at the previous step.
- Overall conversion = users at the last step / users at the first step.
- Overall equals the product of all step conversions.

**Worked mini-example:** 1,000 visit, 400 view a product, 100 add to cart, 50 pay. Step conversions: 40%, 25%, 50%. Overall: 50 / 1,000 = 5%. Check: 0.40 x 0.25 x 0.50 = 0.05.

**Practice step:** Write your own 4-step funnel with counts and compute all three step rates and the overall rate.

**Likely follow-ups:** 1) *Which number do you look at to find the problem?* The lowest step conversion, then compare it with its past values. 2) *Can overall conversion rise while a step falls?* Yes, if another step rises more.
**Common mistakes / traps:** Dividing every step by the first step and calling it step conversion; mixing users with sessions; counting users who skip a step.

### Q4 ⭐⭐⭐ 🟢 A shopping app funnel in one week is below. Compute the step-to-step conversion, the overall conversion and name the step with the lowest conversion.
| Step | Users |
|---|---|
| App visit | 100,000 |
| Product page view | 40,000 |
| Add to cart | 12,000 |
| Checkout started | 8,000 |
| Payment successful | 6,000 |
**Asked at:** commonly asked (no company-specific report found); funnel-drop cases are reported on prep sites for Flipkart and Meesho (unverified).
**What the interviewer is checking:** Correct denominators and spotting the weakest step.
**Say this in the interview:** "Step by step the conversions are 40%, 30%, 66.7% and 75%. Overall is 6%. The weakest step is product page to add to cart at 30%."

**Definition in plain words:** Step conversion = users at a step / users at the previous step. Overall = last step / first step.

**Worked answer:**
| Step | Users | Conversion from previous step |
|---|---|---|
| App visit | 100,000 | n/a |
| Product page view | 40,000 | 40,000 / 100,000 = 40.0% |
| Add to cart | 12,000 | 12,000 / 40,000 = 30.0% |
| Checkout started | 8,000 | 8,000 / 12,000 = 66.7% |
| Payment successful | 6,000 | 6,000 / 8,000 = 75.0% |

Overall: 6,000 / 100,000 = 6.0%.

**Result:** Lowest step conversion: product page to add to cart (30%). Overall conversion 6%.

**Check:** 0.40 x 0.30 x 0.667 x 0.75 = 0.06, matching 6%.

**Caveats:** The lowest rate is not always the biggest opportunity: the first step (40%) loses the most users in absolute terms (60,000), but many visitors never intended to shop. Compare each step with its own history or a benchmark before calling it a problem. Also confirm each row counts unique users, not events.

**Likely follow-ups:** 1) *Where would you look first?* Product page to cart: price, stock, delivery info, page speed. 2) *If payment step improved from 75% to 80%?* Orders become 6,400 (+400).
**Common mistakes / traps:** Using the first step as denominator for every step; choosing the largest absolute drop without context.

### Q5 ⭐⭐⭐ 🟢 A product metric (say daily orders) drops suddenly. What do you check first to confirm the drop is real before looking for causes?
**Asked at:** commonly asked; sudden-drop cases are reported for Swiggy, Paytm, Meesho and Flipkart on prep sites (unverified), and Meesho "declining orders" appears in the internal research.
**What the interviewer is checking:** Whether you rule out data errors before inventing business stories.
**Say this in the interview:** "Before any cause, I confirm the number itself: is the data pipeline complete, is the definition unchanged, and is this drop outside normal weekly variation?"

**Explain simply:** Run these checks in order.
1. Data freshness: did today's data load fully (late tables, partial day)? Compare with a second source such as the payments system.
2. Tracking or definition change: did an app release change event logging, or did someone change the filter or dashboard logic?
3. Normal pattern: compare with the same weekday last weeks (a Monday vs a Sunday is unfair), holidays, month-end, salary days.
4. Size and spread: is it a drop in every region and platform (suggests tracking or outage) or in one slice (suggests a real cause)?
5. Related metrics: do payments received, app opens and server logs agree? A real drop shows in finance numbers too.

**Worked mini-example:** Orders show 100,000 vs 120,000 usual. Payment gateway shows 119,000 successful payments. The gap points to a logging bug, not a business drop.

**Practice step:** Write the five checks as a card you can recite in 30 seconds.

**Likely follow-ups:** 1) *How do you judge "normal variation"?* Compare with the range of the last 8 same-weekday values. 2) *What if the data is confirmed real?* Move to funnel and segment cuts.
**Common mistakes / traps:** Jumping to marketing or competitor causes; comparing against the wrong day; trusting one dashboard.

### Q6 ⭐⭐⭐ 🟢 What clarifying questions do you ask before answering "the metric dropped, find out why" in a product analytics interview?
**Asked at:** commonly asked (no company-specific report found); scoping questions are the first step in Meesho, Flipkart and Paytm-style RCA prompts on prep sites (unverified).
**What the interviewer is checking:** Structured scoping instead of guessing.
**Say this in the interview:** "I would pin down what exactly dropped, by how much, since when and for whom, and what changed recently, before proposing any cause."

**Explain simply:**
- Definition: how is the metric defined, and has it changed? (orders placed or delivered? users or sessions?)
- Size and timing: how big is the drop, sudden or gradual, and which date did it start?
- Scope: all users or one region, platform, user type, product category?
- Comparison: versus yesterday, last week or last year? Is there a seasonal pattern?
- Changes: any app release, pricing or promo change, outage, competitor move or policy change?
- Business context: which related metrics (revenue, cancellations) moved, and what is the target we care about?

**Worked mini-example:** "Orders dropped 10%": ask whether delivered or placed, since Tuesday or gradually, only Android? If only Android and since release 5.2, I start with the release.

**Practice step:** Write six clarifying questions for "attendance at office fell this month" in the HR context.

**Likely follow-ups:** 1) *What if the interviewer says "assume nothing changed"?* State assumptions and move to data cuts. 2) *How many questions?* 4-6 sharp ones, not a long list.
**Common mistakes / traps:** Starting with solutions; asking questions you could answer from data; skipping the metric definition.

### Q7 ⭐⭐⭐ 🟢 What is the difference between feature adoption and feature impact, and why can high adoption still mean no business impact?
**Asked at:** commonly asked (no company-specific report found); adoption vs impact appears as a follow-up in Dataford-style feature-metric questions (unverified).
**What the interviewer is checking:** Whether you separate usage from causal value.
**Say this in the interview:** "Adoption is how many people use the feature; impact is the change in the business goal because of it. A feature can be popular and still change nothing."

**Explain simply:**
- Adoption: share of eligible users who used it (users of feature / eligible users).
- Impact: difference in a business metric (orders, retention, revenue) between exposed and comparable unexposed users.
- High adoption with no impact happens when: it replaces something users did anyway (cannibalisation), it is used out of curiosity once, it shifts behaviour without growing it, or it improves convenience but not frequency.

**Worked mini-example:** 30% of users use "reorder". But holdout shows orders per user are 2.00 vs 2.02. Adoption is high; impact is about +1%, not worth the effort.

**Practice step:** For an HR leave app, write one adoption metric and one impact metric.

**Likely follow-ups:** 1) *How to measure impact?* A/B test with a holdout, or difference-in-differences if randomising is not possible. 2) *Can low adoption have high impact?* Yes, if the few users are very valuable.
**Common mistakes / traps:** Comparing users to non-users; reporting feature clicks as success.

### Q8 ⭐⭐⭐ 🟢 What are leading and lagging metrics? Give one example of each for a new feature on an edtech learning app.
**Asked at:** commonly asked (no company-specific report found); metric-taxonomy questions appear on prep sites (unverified).
**What the interviewer is checking:** Whether you know early signals from final outcomes.
**Say this in the interview:** "Leading metrics move early and predict the outcome; lagging metrics confirm the outcome later. For a new practice-quiz feature, quizzes completed in week 1 is leading and 90-day course completion or renewal is lagging."

**Explain simply:**
- Leading metric: available quickly, can be influenced, correlates with the final goal. Example: share of new learners who finish 3 quizzes in the first week.
- Lagging metric: the real goal, but you wait for it. Example: paid renewal after 90 days.
- Use leading metrics to decide fast and lagging metrics to confirm; check that the leading one really predicts the lagging one (for example, week-1 quiz users renew more).

**Worked mini-example:** If 40% of learners with 3+ week-1 quizzes renew vs 15% of others, the early metric is a useful predictor (though not proof of cause).

**Practice step:** For hiring, name one leading (offer-acceptance rate this month) and one lagging (one-year retention of hires) metric.

**Likely follow-ups:** 1) *Risk of leading metrics?* They may not cause the outcome. 2) *Which do you put in a launch decision?* Both: leading for speed, lagging for confirmation.
**Common mistakes / traps:** Calling revenue leading; picking a leading metric never validated.

### Q9 ⭐⭐⭐ 🟢 When a funnel step drops, which segment cuts do you apply first, and how do you decide the order?
**Asked at:** commonly asked (no company-specific report found); funnel decomposition is common in Meesho, Flipkart and Paytm RCA prompts on prep sites (unverified).
**What the interviewer is checking:** A principled order of cuts, not random slicing.
**Say this in the interview:** "I start with cuts that are cheap and most often the cause: platform and app version, then geography, user type, traffic source, and product or payment method. I order them by how likely they are and how quickly they isolate the problem."

**Explain simply:**
- 1) Time: when exactly did it start (sharp date suggests a release or outage).
- 2) Platform and app version: Android, iOS, web; release is the commonest cause.
- 3) Technical split: device, OS, network, error codes.
- 4) User type: new vs returning.
- 5) Geography or city, then acquisition channel, then product category, price band and payment method.
- Decide the order by: probability (releases, outages first), cost of checking, and whether the cut can fully explain the drop (a segment showing all the loss).

**Worked mini-example:** Drop of 5,000 orders: Android new version lost 4,800, all else flat. The platform and version cut explained 96% in one step.

**Practice step:** Check how much of the drop each cut explains: segment drop divided by total drop.

**Likely follow-ups:** 1) *When do you stop?* When one segment explains most of the drop and has a plausible cause. 2) *What about mix shift?* Compare rates and also share of traffic.
**Common mistakes / traps:** Cutting by many dimensions at once; never quantifying explained share.

### Q10 ⭐⭐⭐ 🟡 The payment-success step of a checkout funnel fell from 75% to 60% week on week, with all earlier steps unchanged. 10,000 users reach the payment step each week. How many orders are lost per week, and how do you investigate?
**Asked at:** commonly asked (no company-specific report found); payment-success diagnosis is reported on prep sites for Paytm and Agoda (unverified).
**What the interviewer is checking:** Quick arithmetic and a structured technical-first investigation.
**Say this in the interview:** "At 75% we got 7,500 orders; at 60% we get 6,000, so 1,500 orders are lost per week. Since earlier steps are flat, the cause sits inside payment: I would cut by bank, method, app version and error code."

**Clarify first:** Is the 10,000 constant? Is "payment success" users or attempts? Any gateway or app release this week? Did the date of the drop line up with a change?

**Structure:**
- Technical: gateway or bank outage, timeouts, app bug, OTP delays.
- Product: new payment screen, coupon or address change, new method ordering.
- Users: different mix (more new users, more COD-averse, more high-value baskets).
- External: bank maintenance, festival load.

**What I would check, in order:**
1. Daily trend: sudden step (outage or release) or slow slide.
2. Success rate by payment method (UPI, card, netbanking, wallet) and by bank.
3. By app version and platform.
4. Failure reason codes and retry behaviour.

**If the data shows...:** One bank or method failing: escalate to the payments team and route traffic to alternatives. One app version failing: roll back or hotfix. Everything evenly lower: check gateway health and mix shift.

**Numeric work:** Lost orders = 10,000 x (0.75 - 0.60) = 1,500 per week, that is 20% fewer orders from this step (7,500 to 6,000).

**Recommendation:** Fix the biggest failing segment first; track daily payment success rate until it returns to about 75%, and add an alert for drops of more than 3 points.

**Likely follow-ups:** 1) *Revenue impact?* Multiply 1,500 by average order value. 2) *Could users be retrying?* Yes; measure users, not attempts.
**Common mistakes / traps:** Blaming marketing for a step inside payment; ignoring retries.

### Q11 ⭐⭐⭐ 🟡 Checkout conversion fell from 8% to 7% on an e-commerce platform. Use the table to find which segment explains the drop, how many orders were lost, and what you would investigate next.
| Platform | Sessions (both weeks) | Conversion before | Conversion after |
|---|---|---|---|
| App | 300,000 | 10% | 10% |
| Mobile web | 200,000 | 5% | 2.5% |
**Asked at:** commonly asked (no company-specific report found); checkout-conversion drop cases are reported for Amazon, Meesho and Flipkart on prep sites (unverified).
**What the interviewer is checking:** Decomposing an overall rate into segments.
**Say this in the interview:** "Mobile web alone explains the whole drop: it lost 5,000 orders, which is the entire fall from 40,000 to 35,000."

**Clarify first:** Same sessions in both weeks (the table says so), so there is no traffic mix change. Is the conversion measured per session? Any web release?

**Structure:**
- Overall conversion before: (300,000 x 10% + 200,000 x 5%) / 500,000.
- After: (300,000 x 10% + 200,000 x 2.5%) / 500,000.
- Segment contribution to the drop.

**What I would check, in order:** Mobile web by browser (Chrome, Safari), page speed, payment step errors, any recent mobile-web change, traffic quality from campaigns.

**Numeric work:**
1. Before: 30,000 + 10,000 = 40,000 orders = 8.0%.
2. After: 30,000 + 5,000 = 35,000 orders = 7.0%.
3. App: 30,000 to 30,000 (no change). Mobile web: 10,000 to 5,000.
4. Lost orders: 5,000 per week, 100% from mobile web (conversion halved).

**If the data shows...:** Specific browser failing means a front-end bug; all browsers lower with same traffic means a funnel step on web (payment, form) broke; poor traffic quality means a campaign brought low-intent visitors.

**Recommendation:** Drill into mobile-web funnel steps to find the step that halved, fix or roll back, and monitor mobile-web conversion daily.

**Likely follow-ups:** 1) *Share of drop by segment?* Mobile web 100%, app 0%. 2) *Why not blame the whole platform?* The app is unchanged.
**Common mistakes / traps:** Reporting only the overall 1-point drop; forgetting to multiply by sessions.

### Q12 ⭐⭐⭐ 🟡 Overall signup conversion fell even though conversion improved on both platforms. Use the data to explain how this is possible and what you would report.
| Platform | Week 1 visitors | Week 1 conv. | Week 2 visitors | Week 2 conv. |
|---|---|---|---|---|
| Android | 60,000 | 5% | 90,000 | 5.5% |
| iOS | 20,000 | 10% | 10,000 | 11% |
**Asked at:** commonly asked (no company-specific report found); mix-shift (Simpson's paradox) is a standard product-analytics probe (prep-site pattern, unverified).
**What the interviewer is checking:** Recognising mix shift.
**Say this in the interview:** "Both platforms improved, but traffic shifted toward Android, the lower-converting platform. Overall fell from 6.25% to 6.05% because of mix, not performance."

**Clarify first:** Why did Android traffic jump (a campaign?) and iOS drop (fewer iOS visitors)? Both matter for the readout.

**Structure:** Compute overall each week, then hold the mix fixed to separate performance from mix.

**What I would check, in order:** Traffic source by platform; whether the Android growth is a new campaign; quality of the extra Android visitors.

**Numeric work:**
1. Week 1 signups: 60,000 x 5% = 3,000 plus 20,000 x 10% = 2,000, total 5,000 out of 80,000 = 6.25%.
2. Week 2 signups: 90,000 x 5.5% = 4,950 plus 10,000 x 11% = 1,100, total 6,050 out of 100,000 = 6.05%.
3. Android share of visitors: 75% in week 1, 90% in week 2.
4. Mix-adjusted week 2 (using week 1 mix, 75/25): 0.75 x 5.5% + 0.25 x 11% = 6.875%, above 6.25%, so true performance improved by 0.625 points.

**If the data shows...:** Mix-adjusted rate up with overall down: report both, say performance improved and mix shifted. Total signups actually rose from 5,000 to 6,050 (+21%).

**Recommendation:** Report platform-level conversion plus the mix-adjusted figure, and ask whether the extra Android traffic is worth its cost.

**Likely follow-ups:** 1) *What is this paradox called?* Simpson's paradox (mix effect). 2) *Which number goes on the leadership slide?* Both, with a one-line explanation.
**Common mistakes / traps:** Calling the overall drop a problem; averaging the two platform rates.

### Q13 ⭐⭐⭐ 🟡 Users of a new in-app feature place 3.0 orders per month against 2.0 for non-users. A manager says the feature adds 1.0 order per user. Is this right, and how would you estimate the true effect?
**Asked at:** commonly asked (no company-specific report found); selection-bias traps appear in prep-site feature-analysis questions (unverified).
**What the interviewer is checking:** Awareness of selection bias and causal estimation.
**Say this in the interview:** "Not necessarily. Heavy, engaged users are the ones who adopt features, so part of the 1.0 gap was there before. The true effect needs a randomised test or a before/after comparison against a control."

**Clarify first:** Did users choose the feature or were they assigned? What were their orders before using it? Is a holdout possible?

**Structure:**
- Raw gap: 3.0 - 2.0 = 1.0 order per month (correlation).
- Possible reasons it overstates: self-selection (heavy users adopt), reverse causality, other changes at the same time.
- Ways to get the causal effect: A/B test, difference-in-differences, matched comparison.

**What I would check, in order:**
1. Pre-period orders of adopters vs non-adopters (if adopters already ordered 2.7, the feature adds about 0.3).
2. A holdout: randomly hide the feature from a small share of users.
3. Difference-in-differences: (adopters after - before) minus (non-adopters after - before).

**Numeric work (illustrative, assumed):** If adopters had 2.6 before and 3.0 after (+0.4) while non-adopters went 2.0 to 2.0 (0.0), the effect is about +0.4 orders per user, not +1.0.

**If the data shows...:** Similar pre-period for both groups: the manager is about right. Large pre-gap: most of the 1.0 is selection.

**Recommendation:** Run a holdout test, report incremental orders per exposed user with a confidence interval.

**Likely follow-ups:** 1) *What if you cannot randomise?* Use difference-in-differences or matching. 2) *Why does selection arise?* Adopters differ in intent before they ever see the feature.
**Common mistakes / traps:** Accepting the raw gap as impact; ignoring the pre-period.

### Q14 ⭐⭐⭐ 🟡 Choose a primary metric, two guardrail metrics and two diagnostic metrics for a new "split the bill" feature in a UPI payments app.
**Asked at:** commonly asked (no company-specific report found); PhonePe-style product-metric rounds are in the internal research (candidate reports unverified).
**What the interviewer is checking:** A coherent metric set matched to the feature goal.
**Say this in the interview:** "The goal is more successful payments from group settlements. Primary: split-bill transactions completed per active user per month. Guardrails: payment success rate and complaint or dispute rate. Diagnostics: request-to-pay conversion and time to settle."

**Explain simply:**
- Primary: successful split-bill payments (completed collect requests) per monthly active user. It reflects real value, a bill that actually got settled.
- Guardrail 1: overall payment success rate (the new flow must not break normal payments).
- Guardrail 2: fraud, spam-request and complaint rate (the feature can be abused to send unwanted requests).
- Diagnostic 1: share of split requests that get paid (request to payment conversion).
- Diagnostic 2: median time from request to payment, plus number of participants per split.

**Worked mini-example (illustrative):** 100,000 split requests sent, 70,000 paid: request-to-pay conversion 70%. If it falls to 55% after launch, look at notification delivery.

**Practice step:** Write the same five metrics for a "group order" feature on a food app.

**Likely follow-ups:** 1) *Why not number of splits created?* Creating is not settling. 2) *Is it incremental?* Compare with a holdout; some splits replace manual transfers.
**Common mistakes / traps:** Using a vanity metric (feature opens); no abuse guardrail.

### Q15 ⭐⭐⭐ 🟡 Orders per Android user per day dropped after app release 5.2. The release was rolled out to 50% of Android users; iOS is unchanged. Use the data to estimate the drop in total Android orders, and say what else you would check before blaming the release.
| Group | Orders per user per day |
|---|---|
| Android on new version (50% of Android users) | 1.8 |
| Android on old version (50%) | 2.1 |
| iOS | flat versus last month |
**Asked at:** commonly asked (no company-specific report found); release-related drop analysis appears in prep-site RCA items (unverified).
**What the interviewer is checking:** Quantifying a segment effect and challenging causation.
**Say this in the interview:** "New-version users order 0.3 fewer per day, a 14% gap. With half of Android users on it, the Android average falls from 2.1 to 1.95, about 7%. But I would first check whether the two groups are comparable before blaming the release."

**Clarify first:** Was the 50% randomly chosen, or did users update themselves? How many Android users are there (not given)? Is the old-version figure the same as last month's?

**Structure:** Gap per user, blended effect, per-user-base scaling, then validity checks.

**What I would check, in order:**
1. Random vs self-selected rollout: users who update early may be more or less active.
2. Pre-release orders of the new-version group (difference-in-differences).
3. Crash rate, app load time and error logs on the new version.
4. Event logging: does 5.2 under-record orders (a tracking bug)?
5. Seasonality, since iOS is flat, so the market itself is unlikely to be the cause.

**Numeric work:**
1. Gap = 2.1 - 1.8 = 0.3 orders per user per day (14.3% lower).
2. Blended Android: 0.5 x 1.8 + 0.5 x 2.1 = 1.95, versus 2.1 if no one had updated: drop of 0.15 per Android user per day (7.1%).
3. Per 1,000,000 Android users (assumed for scaling): 150,000 fewer orders per day.
4. If all Android users moved to 5.2: 0.3 per user, or 300,000 fewer orders per 1,000,000 users per day.

**If the data shows...:** Random rollout plus lower orders means the release harms orders: pause the rollout and fix. Self-selected rollout with similar prior orders: effect holds but needs a test. Logging gap: orders are fine; fix tracking.

**Recommendation:** Halt the rollout expansion until a randomised comparison or crash and funnel analysis confirms the cause.

**Likely follow-ups:** 1) *Why is iOS useful?* It acts as a control for market-wide changes. 2) *Quick fix?* Roll back for a small cohort and watch recovery.
**Common mistakes / traps:** Treating a non-random rollout as an experiment; forgetting to blend the 50/50 split.

### Q16 ⭐⭐⭐ 🟡 An A/B test of a new checkout widget is below. Compute the absolute and relative lift, the extra orders per week at full rollout to 2 million weekly visitors, and the extra refunds per week using the guardrail data.
| Arm | Users | Orders | Refund rate on orders |
|---|---|---|---|
| Control | 50,000 | 2,000 (4.0%) | 2.0% |
| Treatment | 50,000 | 2,150 (4.3%) | 2.2% |
Assume the full-rollout results equal the test rates.
**Asked at:** commonly asked (no company-specific report found); A/B readouts are a standard product-analytics prompt (prep-site pattern, unverified).
**What the interviewer is checking:** Lift arithmetic, scaling and reading a guardrail.
**Say this in the interview:** "Absolute lift is 0.3 points, relative lift 7.5%, about 6,000 extra orders a week at 2 million visitors. Refunds rise by about 292 a week, so refunds are worth watching but small against the gain."

**Definition in plain words:** Absolute lift = treatment rate minus control rate. Relative lift = absolute lift / control rate.

**Worked answer:**
1. Rates: control 2,000 / 50,000 = 4.0%; treatment 2,150 / 50,000 = 4.3%.
2. Absolute lift = 4.3% - 4.0% = 0.3 percentage points.
3. Relative lift = 0.3 / 4.0 = 7.5%.
4. Full rollout, control rate: 2,000,000 x 4.0% = 80,000 orders; treatment: 2,000,000 x 4.3% = 86,000. Extra = 6,000 orders per week.
5. Refunds: control 80,000 x 2.0% = 1,600; treatment 86,000 x 2.2% = 1,892. Extra = 292 refunds per week.

**Result:** +0.3 points absolute, +7.5% relative, +6,000 orders and +292 refunds per week.

**Check:** Refunds on the 6,000 extra orders alone would be 120, so most of the 292 comes from the refund rate rising from 2.0% to 2.2% on all 86,000 orders. Significance: a two-proportion z-test gives z about 2.4 (above 1.96), so the lift is probably real at the 95% level, though not by a huge margin.

**Caveats:** Test duration and novelty effect; the refund rate difference (0.2 points) needs its own significance check; revenue per order and refund cost decide the net value; full rollout may not match test rates.

**Likely follow-ups:** 1) *Do you launch?* Likely yes if the margin on 5,708 net orders beats the refund cost; confirm refund difference significance. 2) *Sample size needed?* About 68,000 per arm to detect 0.3 points at 80% power (approximate), so this test is slightly underpowered.
**Common mistakes / traps:** Calling 0.3 points "0.3%"; using the refund rate on visitors instead of on orders.

### Q17 ⭐⭐⭐ 🟡 A food app launches a "10-minute" tab. Before launch the app had 100,000 orders per day; after launch it has 12,000 on the new tab and 92,000 on the standard tab. Compute the net incremental orders and the cannibalisation share, and say how you would validate the numbers.
**Asked at:** commonly asked (no company-specific report found); cannibalisation was not found directly in sources and is a gap-fill from general product-analytics practice.
**What the interviewer is checking:** Separating total new orders from orders that just moved.
**Say this in the interview:** "Total orders went from 100,000 to 104,000, so net incremental is 4,000. Of the 12,000 on the new tab, 8,000 moved from the standard tab, so cannibalisation is two-thirds."

**Clarify first:** Is the 100,000 baseline stable (no growth trend)? Any promo or season change in the same period? Is the comparison over the same weekday?

**Structure:** Total after = 12,000 + 92,000 = 104,000. Net incremental = 104,000 - 100,000. Cannibalised = standard-tab loss = 100,000 - 92,000.

**What I would check, in order:**
1. Baseline trend: what would orders have been without the tab (use prior weeks, a control city).
2. Whether the 8,000 loss is cannibalisation or normal variation.
3. Margins: new-tab orders may carry higher delivery cost.

**Numeric work:**
1. Net incremental = 104,000 - 100,000 = 4,000 orders per day (+4%).
2. Standard tab lost 100,000 - 92,000 = 8,000, which moved to the new tab.
3. Cannibalisation share = 8,000 / 12,000 = 66.7%; incremental share = 4,000 / 12,000 = 33.3%.

**If the data shows...:** With a trend of +2% anyway, true incremental is 2,000 not 4,000. If control cities show a drop, cannibalisation is lower than it looks.

**Recommendation:** Validate with a staggered city rollout or holdout cities (difference-in-differences), and judge the tab on contribution margin, not order count.

**Likely follow-ups:** 1) *Is 67% cannibalisation bad?* Depends on margin and strategy; it is bad if new-tab orders cost more. 2) *Better test?* Randomise the tab at user or city level.
**Common mistakes / traps:** Calling all 12,000 incremental; ignoring baseline trend.

### Q18 ⭐⭐⭐ 🟡 A payment app's success rate fell. Use the table to compute the overall success rate before and after, the extra failed attempts per 1 million attempts, and the share of the damage caused by each bank.
| Bank | Share of attempts | Success before | Success after |
|---|---|---|---|
| Bank A | 40% | 94% | 94% |
| Bank B | 30% | 92% | 70% |
| Bank C | 30% | 90% | 90% |
**Asked at:** commonly asked (no company-specific report found); payment success-rate decomposition by bank appears in Paytm and Agoda prep-site items (unverified).
**What the interviewer is checking:** Weighted averages and attributing a change to segments.
**Say this in the interview:** "Overall success fell from 92.2% to 85.6%, a 6.6 point drop, which is 66,000 extra failures per million attempts. Bank B causes 100% of it."

**Definition in plain words:** Overall success rate = sum over banks of (share of attempts x success rate). A bank's damage = share x drop in its success rate.

**Worked answer:**
1. Before: 0.40 x 94 + 0.30 x 92 + 0.30 x 90 = 37.6 + 27.6 + 27.0 = 92.2%.
2. After: 37.6 + 0.30 x 70 + 27.0 = 37.6 + 21.0 + 27.0 = 85.6%.
3. Drop = 6.6 percentage points.
4. Extra failures per 1,000,000 attempts = 1,000,000 x 6.6% = 66,000.
5. Damage by bank: A = 0.40 x 0 = 0 points; B = 0.30 x 22 = 6.6 points; C = 0. Share of damage: Bank B 100%.

**Result:** 92.2% to 85.6%; 66,000 extra failed attempts per million; Bank B accounts for all of it.

**Check:** Bank B alone: 300,000 attempts x 22% = 66,000. Matches.

**Caveats:** Assumes attempt shares are unchanged; if users moved away from Bank B the mix would shift too. Check technical declines vs user declines (insufficient balance), and whether the failure is the bank's server or our integration.

**Likely follow-ups:** 1) *Next step?* Pull Bank B failure codes and time of drop, and contact the bank or reroute. 2) *Why per million?* Easier to scale to daily volumes.
**Common mistakes / traps:** Simple average of the three banks; forgetting the weights.

### Q19 ⭐⭐⭐ 🟡 A coupon-code box was added to the cart page and checkout conversion fell from 6.0% to 5.4% on 400,000 weekly cart views. Compute the orders lost per week and propose how you would test the cause and a fix.
**Asked at:** commonly asked (no company-specific report found); checkout conversion drop cases are reported for Amazon and Meesho on prep sites (unverified).
**What the interviewer is checking:** Quick lost-orders arithmetic and a testable hypothesis.
**Say this in the interview:** "400,000 cart views at 6.0% is 24,000 orders; at 5.4% it is 21,600. We lose 2,400 orders per week. My hypothesis is that shoppers leave to hunt for a coupon code, so I would A/B test hiding the box behind a link."

**Clarify first:** Was the change the only one that week? Was the drop immediate? Is conversion measured per cart view? Do users who leave return later?

**Structure:**
- Hypotheses: users leave the page to search for a code (the "coupon hunt"); distraction from the pay button; code errors causing frustration; mobile layout pushing the button down.
- Test design: randomise cart views to (a) no box, (b) box as now, (c) collapsed "Have a coupon?" link.

**What I would check, in order:**
1. Compare conversion before and after for users who touched the box vs did not.
2. Exit rate and time on cart page; scroll depth to the pay button.
3. Coupon invalid-code error rate.
4. Platform split (mobile layout).

**If the data shows...:** Exit rate high only for users who clicked the box: hide or collapse it. Many invalid codes: auto-apply the best coupon. No difference between arms: the drop is from something else.

**Numeric work:** Before: 400,000 x 6.0% = 24,000. After: 400,000 x 5.4% = 21,600. Lost = 2,400 orders per week (10% relative fall).

**Recommendation:** Run a two-week A/B test with the three arms; primary metric is cart-to-order conversion, guardrail is discount cost per order. Pick the arm that recovers at least most of the 2,400 orders without raising discount cost sharply.

**Likely follow-ups:** 1) *Is the drop real?* Check before-after against the pre-trend and the test. 2) *Remove the box?* Compare with the coupon revenue it enables.
**Common mistakes / traps:** Forgetting percentage versus percentage points; deciding without a test.

### Q20 ⭐⭐⭐ 🔴 Design the full measurement plan for launching "group ordering" (several people add items to one shared cart) on a food delivery app: goal, metrics, experiment design, risks and decision rule.
**Asked at:** commonly asked (no company-specific report found); full launch-measurement plans appear on prep sites (PracHub, Dataford; unverified).
**What the interviewer is checking:** End-to-end experiment thinking, including network effects.
**Say this in the interview:** "Goal: grow orders from groups (office lunches, family dinners) without hurting delivery quality. I would test by city or group-level randomisation, judge on incremental orders per active user and contribution margin, and set guardrails on cancellations and delivery time."

**Clarify first:** Is the goal growth, higher order value, or new users? Who can see the feature? Can we randomise at user level (hard, because friends share one cart) or only by city?

**Structure:**
- Goal and hypothesis: group ordering raises order value and frequency.
- Primary metric: incremental orders (and gross order value) per active user per month versus holdout.
- Guardrails: cancellation rate, late-delivery rate, support tickets, rider cost per order.
- Diagnostics: share of carts that are group carts, number of participants, invite-to-join rate, time to finish a shared cart, drop-off at invite step.
- Experiment design: randomise by city or by user cluster (a user and their frequent co-orderers) to avoid contamination; test 3 to 4 weeks to cover weekday and weekend cycles; check sample size beforehand; pre-register the primary metric.
- Risks: cannibalisation (a group of three orders once instead of three separate orders: orders fall but value per order rises), novelty effect, bigger orders slowing kitchens, payment-split disputes.

**What I would check, in order:** Orders and value per active user; share of group carts that replace separate orders; delivery time for large orders; abandoned shared carts.

**If the data shows...:** Higher gross order value and flat order count with better margin: ship (count is the wrong metric). Fewer orders and lower value: do not ship. Guardrail breach: fix operations first.

**Decision rule:** Launch if incremental gross margin per active user is positive and statistically credible (95% confidence), and guardrails stay within pre-agreed limits (for example, cancellation up by no more than 0.2 points).

**Recommendation:** Pilot in 2 cities, measure 4 weeks, then roll out to more cities with a long-term holdout (a small group kept without the feature) to catch novelty fade.

**Likely follow-ups:** 1) *Why not user-level A/B?* Group members interact, so treatment spills over to control. 2) *Primary metric trap?* Orders can fall while value rises; use gross margin.
**Common mistakes / traps:** Counting orders instead of value; ignoring spillover; no decision rule agreed beforehand.

### Q21 ⭐⭐⭐ 🔴 A homepage redesign showed +2% orders in a two-week A/B test, but after full rollout total daily orders look flat. List the possible reasons and how you would test each.
**Asked at:** commonly asked (no company-specific report found); test-versus-rollout gaps are a known follow-up on prep sites (unverified).
**What the interviewer is checking:** Whether you can reason about why experiments do not translate.
**Say this in the interview:** "I would group the reasons into: the test was wrong, the effect faded, or the rollout comparison is wrong. For each I would name the check: novelty effect, sample ratio, external changes, and a long-term holdout."

**Clarify first:** What is "flat": versus what baseline? What else changed (marketing, seasonality, pricing)? Is there still a holdout?

**Structure and tests:**
1. Novelty effect: users tried the new design out of curiosity. Test: plot the lift by day; see if it decays. A holdout kept 4+ weeks settles it.
2. False positive or noise: +2% on two weeks could be chance. Test: confidence interval, re-run or extend the test.
3. Sample ratio or setup problem: uneven split, bots, wrong users. Test: check that the arm sizes match the planned split.
4. Different population: the test ran on a subset (for example logged-in users, one city). Test: compare the test users with all users.
5. Seasonality or other changes: a festival, pricing or campaign in the test window or after rollout. Test: compare against the same period last year, a control market, or a holdout.
6. Interference or capacity: more orders in the test were limited by supply (riders, stock) when everyone got it. Test: look at fulfilment limits and cancellations.
7. Metric difference: the test counted orders per user, rollout counted total orders, with different traffic. Test: use the same definition.

**If the data shows...:** Lift decaying daily: novelty. A holdout still +2%: external factor masks the lift. Holdout flat: the test lift was noise or novelty.

**Recommendation:** Keep or restore a 5% holdout and compare daily; report the result as incremental orders against the holdout, not before-after.

**Likely follow-ups:** 1) *Quick check today?* Compare the test arm lift in week 1 vs week 2. 2) *How to avoid it next time?* Longer tests and permanent holdouts.
**Common mistakes / traps:** Comparing before and after rollout without a control; blaming the test without checking data issues.

### Q22 ⭐⭐ 🟢 What is an activation metric, and how would you find the "aha moment" for a new fintech investing app?
**Asked at:** commonly asked (no company-specific report found); activation and aha-moment questions appear on prep sites (unverified).
**What the interviewer is checking:** Linking an early user action to long-term retention using data.
**Say this in the interview:** "Activation is the first action that shows a new user got real value. I would find the aha moment by comparing early actions of users who stayed against those who left, and picking the action with the strongest link to retention that I can encourage."

**Explain simply:**
- Activation metric: share of new users who complete a key value action within a time window (for example, make a first investment within 7 days of signup).
- Aha moment: the specific action or experience after which users are much more likely to stay (for example, completing KYC and making a first investment).
- Finding it: list early actions (KYC done, first deposit, first investment, watchlist created), compute day-30 retention for users with and without each action, and pick the action with a big retention gap that is realistic to push.

**Worked mini-example (illustrative):** Day-30 retention is 45% for users who invest within 3 days and 10% for those who do not. First investment in 3 days is a candidate aha; test by nudging users to it.

**Practice step:** Write 5 candidate early actions for a leave-management app and what you would compare.

**Likely follow-ups:** 1) *Correlation or cause?* Run a nudge experiment to confirm. 2) *Time window?* Choose from data, where retention separates.
**Common mistakes / traps:** Picking signup as activation; confusing correlation with cause.

### Q23 ⭐⭐ 🟢 What is a North Star metric, and what input metrics would you attach to it for a quick commerce app?
**Asked at:** commonly asked (no company-specific report found); North Star questions are commonly asked in product rounds (prep-site claim, unverified; no verified Zepto or Blinkit report).
**What the interviewer is checking:** A single value-based metric and a driver tree beneath it.
**Say this in the interview:** "The North Star is the one metric that best captures value delivered to customers and predicts long-term growth. For quick commerce I would use weekly orders delivered on time per active customer, with inputs on demand, supply and quality."

**Explain simply:**
- North Star metric: one number the whole company works to grow; it reflects customer value, not just revenue.
- Quick commerce choice: orders delivered within the promised window per weekly active customer.
- Input metrics (the levers that move it): 
  - Reach: weekly active customers, new customers acquired.
  - Frequency: orders per customer per week, repeat rate.
  - Selection and availability: product-in-stock rate, search success rate.
  - Speed and quality: share of orders delivered in time, order error rate.
  - Efficiency (guardrail): contribution margin per order.

**Worked mini-example (illustrative):** North Star = active customers x orders per customer x on-time share. 1,000,000 x 2.5 x 90% = 2,250,000 on-time orders per week.

**Practice step:** Draw a one-level tree for an HR helpdesk: North Star and four inputs.

**Likely follow-ups:** 1) *Why not revenue?* It can rise through price and hurt customer value. 2) *Danger?* Optimising only one input (speed) at cost of margin.
**Common mistakes / traps:** Choosing several North Stars; picking a vanity metric such as downloads.

### Q24 ⭐⭐ 🟢 A feature was used by 360,000 of 2.4 million monthly active users in 30 days, and 90,000 of those 360,000 used it again within the next 30 days. Compute the adoption rate and the repeat-use rate.
**Asked at:** commonly asked (no company-specific report found); adoption and repeat-use calculations are common in feature-analysis prep questions (unverified).
**What the interviewer is checking:** Correct denominators for adoption and repeat use.
**Say this in the interview:** "Adoption is 360,000 over 2.4 million, which is 15%. Repeat use is 90,000 over 360,000, which is 25%."

**Definition in plain words:** Adoption rate = users who used the feature / eligible active users. Repeat-use rate = users who used it again / users who used it the first time.

**Worked answer:**
1. Adoption = 360,000 / 2,400,000 = 0.15 = 15%.
2. Repeat-use = 90,000 / 360,000 = 0.25 = 25%.
3. Share of all active users who are repeat users: 90,000 / 2,400,000 = 3.75%.

**Result:** Adoption 15%; repeat-use 25%.

**Check:** 15% x 25% = 3.75%, which matches the share of all MAU who repeated.

**Caveats:** Use eligible users as the denominator if only some users can see the feature; the 25% repeat window (next 30 days) should be stated; whether 25% is good depends on how often the task naturally recurs; adoption and repeat say nothing about business impact.

**Likely follow-ups:** 1) *Is 25% good?* Compare with similar features and the natural usage frequency. 2) *Next metric?* Retention curve of first-time users and impact versus holdout.
**Common mistakes / traps:** Using 2.4 million as the denominator for repeat use (gives 3.75%, not 25%); counting events rather than users.

### Q25 ⭐⭐ 🟢 On a grocery app, 50,000 carts were created in a day and 18,000 became orders. Compute the cart abandonment rate and list three product reasons it could rise.
**Asked at:** commonly asked (no company-specific report found); checkout-conversion cases appear on prep sites (unverified).
**What the interviewer is checking:** Correct formula, and whether you can link a metric to concrete product causes.
**Say this in the interview:** "Abandonment is carts that did not become orders, divided by carts created: 32,000 / 50,000 = 64%. The flip side, cart-to-order conversion, is 36%."

**Definition in plain words:** Cart abandonment rate is the share of carts that never turn into an order. Formula: (carts created - orders) / carts created.
**Worked answer:** 1) Abandoned carts = 50,000 - 18,000 = 32,000. 2) Rate = 32,000 / 50,000 = 0.64 = 64%. 3) Conversion = 18,000 / 50,000 = 36%, and 64% + 36% = 100%.
**Result:** 64% abandonment (36% conversion).
**Check:** 0.36 x 50,000 = 18,000, which matches the orders.
**Three product reasons it could rise:** (1) Surprise costs at checkout (delivery fee, handling fee, minimum order value) shown late. (2) Item availability: products turn "out of stock" or the delivery slot is far away. (3) Friction in payment or address steps (slow page, failed UPI, forced login or coupon errors).
**Caveats:** A cart can be a browsing tool (users park items to compare), so 64% is not all "lost" demand. One user can create several carts, and carts that convert later the same week count as abandoned in a one-day view.
**Likely follow-ups:** 1) *Is 64% bad?* Not by itself; compare with your own trend and with similar apps. 2) *How would you split it?* By new versus repeat users, device, city and the last screen seen.
**Common mistakes / traps:** Reporting 36% as abandonment; ignoring duplicate carts; forgetting that a one-day window mixes carts created today with orders placed from older carts.

### Q26 ⭐⭐ 🟢 What is the difference between funnel analysis and cohort analysis, and when would you use each in a product case?
**Asked at:** commonly asked (no company-specific report found); both appear in prep-site product-analytics banks and Fractal-type analytics guides (unverified).
**What the interviewer is checking:** Whether you know one looks at steps in a journey and the other at groups over time.
**Say this in the interview:** "A funnel asks where people drop between steps; a cohort asks how a group of users who started together behaves as time passes. I use a funnel to find the leak and a cohort to see whether users stay."

**Explain simply:**
- Funnel analysis: an ordered list of steps (open app, add to cart, pay) and the share who move from each step to the next. Use it when a conversion number fell or a flow was redesigned.
- Cohort analysis: group users by a shared starting point (signup week) and track the same measure (still active, still paying) week by week. Use it for retention, lifetime value and "did the new onboarding help later weeks".
- HR parallel: a funnel is applicants to offers to joiners; a cohort is "everyone hired in April" and how many are still with us at 3, 6 and 12 months.
**Mini-example:** 1,000 signups, 400 reach checkout, 100 pay: funnel says 40% then 25%. Separately, the January signup cohort has 30% active in week 4 and the February cohort 38%: onboarding got better.
**Practice step:** Take any app you use, write its four main steps, and invent one cohort you would track.
**Likely follow-ups:** 1) *Can you combine them?* Yes, a funnel per cohort shows whether newer users convert better. 2) *Which first in a "conversion dropped" case?* Funnel, then cohort if the drop is only in new users.
**Common mistakes / traps:** Reading a funnel across mixed-age users; calling an overall retention number a cohort view; ignoring that cohort curves need time to mature.

### Q27 ⭐⭐ 🟢 What events and properties must an app log to measure a checkout funnel, and what instrumentation mistakes commonly corrupt the funnel?
**Asked at:** commonly asked (no company-specific report found); funnel-metric skills are named for product-company analyst roles in the internal research (unverified for this exact question).
**What the interviewer is checking:** Practical knowledge of event tracking and data quality.
**Say this in the interview:** "I would log one event per funnel step, each with a user id, session id, timestamp and the cart context, and I would first check the events for duplicates and gaps before trusting any conversion number."

**Explain simply:**
- Events (things that happen): app_open, product_viewed, add_to_cart, cart_viewed, checkout_started, address_selected, payment_method_selected, payment_attempted, payment_succeeded or payment_failed, order_placed.
- Properties (details on each event): user_id, session_id, timestamp, platform and app version, cart value and item count, coupon, payment method, error code, city, new or repeat user.
- Common corruptions: events fired twice (double counting); an event missing on one platform (iOS versus Android); user id changing after login so one person looks like two; the same event renamed in a new app version; timestamps in different time zones; offline events sent late; test users and bots left in; "order_placed" logged before payment is confirmed.
**Mini-example:** If add_to_cart fires twice on Android only, Android add-to-cart counts inflate and its next-step conversion looks worse than iOS even if behaviour is identical.
**Practice step:** Write the ten events above in a table and mark which property would let you split by cause of failure.
**Likely follow-ups:** 1) *How do you validate?* Compare the event count with backend orders; they should match within a small gap. 2) *Who owns the tracking plan?* Analytics with engineering, documented and versioned.
**Common mistakes / traps:** Trusting dashboards without reconciling to the orders table; no session or user id; mixing step order across app versions.

### Q28 ⭐⭐ 🟢 What are the HEART framework dimensions, and how would you apply them to a new video-lesson feature in an edtech app?
**Asked at:** commonly asked (no company-specific report found); metric-framework questions appear on prep sites such as TryExponent and Dataford (unverified).
**What the interviewer is checking:** That you can name the framework and turn each letter into a metric you could actually compute.
**Say this in the interview:** "HEART is Happiness, Engagement, Adoption, Retention, Task success. For video lessons I would pick one metric per letter, and choose course completion as the headline."

**Explain simply:** HEART is a checklist from Google researchers for choosing product metrics; you pick the letters that matter.
- Happiness: how users feel (lesson rating, survey score, complaints).
- Engagement: how deeply they use it (lessons watched per learner per week, minutes watched).
- Adoption: new users trying it (share of learners who start a video lesson in their first 7 days).
- Retention: coming back (share of video learners still active after 30 days).
- Task success: achieving the goal (lesson completion rate, quiz score after the lesson, errors such as buffering).
**Mini-example (illustrative):** 10,000 learners, 3,000 start a video: adoption 30%; 1,800 finish: completion 60%.
**Practice step:** Choose the single "north star" among the five, name two guardrails (for example, video load failures and refund requests) and say why.
**Likely follow-ups:** 1) *Do you need all five?* No; pick the ones tied to the goal. 2) *Metric versus outcome?* Completion is a proxy; learning outcome (quiz score, exam pass) is the real aim.
**Common mistakes / traps:** Using only time spent; naming the letters without any numbers; no guardrail.

### Q29 ⭐⭐ 🟢 How would you present a feature launch readout to leadership in three slides?
**Asked at:** commonly asked (no company-specific report found); launch-readout and primary-metric questions appear on prep sites such as PracHub and Dataford (unverified).
**What the interviewer is checking:** Whether you communicate the decision first, with numbers, risks and next step, not a data dump.
**Say this in the interview:** "Slide one is the answer and the decision I need; slide two is the evidence with the primary metric and guardrails; slide three is risks, caveats and next steps."

**Explain simply:**
- Slide 1, Headline: what launched, to whom, the result in one line ("Orders per user up 2.1%, no guardrail breached") and the ask (ship to 100%, extend, or stop).
- Slide 2, Evidence: test design in one line (who, how long, sample size), primary metric with confidence interval, two or three guardrails, one chart by segment (new versus repeat users).
- Slide 3, Risks and next steps: caveats (novelty effect, small segments, short window), cost, rollout plan with owner and date, and what we will monitor after launch.
**Mini-example:** "Lift +2.1% (95% interval +0.8% to +3.4%), crash rate unchanged, support tickets +0.1%. Recommend 50% rollout then a 5% long-term holdout." (illustrative numbers)
**Practice step:** Write the one-line headline first; if it takes more than two sentences, you are not ready.
**Likely follow-ups:** 1) *What if the result is flat?* Say so plainly and give the decision (stop or iterate). 2) *Appendix?* Put methods and extra cuts there.
**Common mistakes / traps:** Starting with methodology; no decision asked; hiding a failed guardrail; reporting only the average.

### Q30 ⭐⭐ 🟢 An HR self-service app asks employees to apply for leave in the app. How would you measure whether this feature is a success?
**Asked at:** commonly asked (no company-specific report found); HR-app measurement is a gap-fill item in the sources file (unverified).
**What the interviewer is checking:** Whether you separate adoption, efficiency, quality and employee experience, and know the baseline.
**Say this in the interview:** "Success means most leave requests go through the app, faster and with fewer errors, and without hurting employee experience. I would track adoption as the headline and use processing time and error rate as the proof."

**Explain simply:**
- Adoption: leave requests made in the app divided by all leave requests (app plus email plus paper). Target for example 90% within three months (assumed).
- Efficiency: average days from request to approval; HR hours spent keying leave into the system; manager approval turnaround.
- Quality: leave balance mismatches, rejected or corrected requests, payroll corrections caused by wrong leave data.
- Experience: short pulse survey, helpdesk tickets about leave, app crash rate on the leave screen.
- Baseline: measure all of the above for two or three months before launch, and compare by location or by a staggered rollout.
**Mini-example (illustrative):** 2,000 requests a month; app share 40% in month 1, 85% in month 3; approval time 2.5 days down to 1.0 day.
**Practice step:** Write one metric from each of the four groups and the data source (HRIS table, helpdesk log).
**Likely follow-ups:** 1) *Why not just count logins?* Logins do not mean leave was applied through the app. 2) *Who is left out?* Shift or field staff without app access; check coverage.
**Common mistakes / traps:** No baseline; counting only adoption; forgetting payroll errors, which are the real cost.

### Q31 ⭐⭐ 🟢 A new-hire onboarding app funnel is below. Compute each step conversion and the overall conversion, and say where you would look for friction.
| Step | Employees |
|---|---|
| Offer accepted | 500 |
| Documents uploaded | 450 |
| Background check cleared | 400 |
| Joined on Day 1 | 360 |
**Asked at:** commonly asked (no company-specific report found); onboarding-funnel cases appear on prep sites (unverified).
**What the interviewer is checking:** Step-by-step conversion arithmetic, and sensible friction hypotheses.
**Say this in the interview:** "Step conversions are 90%, 88.9% and 90%; overall 72%, so 140 of 500 accepted candidates never join. The background check step is the weakest by rate, and I would also look at accepted-to-joined as a pre-boarding dropout."

**Definition in plain words:** Step conversion = employees at this step / employees at the previous step. Overall conversion = last step / first step.
**Worked answer:** 1) Documents: 450 / 500 = 90.0%. 2) Background check: 400 / 450 = 88.9%. 3) Joined Day 1: 360 / 400 = 90.0%. 4) Overall: 360 / 500 = 72.0%; check 0.9 x 0.889 x 0.9 = 0.72.
**Result:** 90.0%, 88.9%, 90.0%; overall 72%. Losses are 50, 50 and 40 people.
**Check:** 500 - 50 - 50 - 40 = 360.
**Where to look for friction:** The steps are all close, so no single dramatic leak. The lowest rate is the background check (11% fail or stall): look at turnaround days, pending versus failed, and which check (address, employment, education) is slow. For documents, look at which file types fail upload and reminders sent. For the last step, look at the notice period and counter-offers; candidates who accept and then take another job is the classic HR leak.
**Caveats:** "Cleared" might hide people still pending (not drop-outs); split drop-outs by reason, role and recruiter.
**Likely follow-ups:** 1) *If you could fix one step?* The step with the most recoverable people; ask which are only delayed. 2) *Benchmark?* Use your own past batches.
**Common mistakes / traps:** Dividing every step by 500 and calling those step conversions; ignoring that pending is not lost.

### Q32 ⭐⭐ 🟢 What is the difference between a session-based funnel and a user-based funnel, and when does each mislead?
**Asked at:** commonly asked (no company-specific report found); funnel-window questions appear in prep banks (unverified).
**What the interviewer is checking:** Understanding of the unit of counting and its biases.
**Say this in the interview:** "A session funnel counts visits; a user funnel counts people across visits. Session funnels understate conversion for slow decisions; user funnels can hide how a single visit behaves."

**Explain simply:**
- Session-based: a step counts only if the whole path happens in one visit. Good for judging a single flow (a checkout redesign) and for real-time health.
- User-based: a step counts if the same person completes it within a chosen window (for example 7 days), even across visits. Good for considered purchases and for business conversion.
- When each misleads: session funnels mislead when people browse today and buy tomorrow (the browse session looks like a failure); user funnels mislead when one heavy user repeats the flow many times, or the window is long enough to credit unrelated actions.
**Mini-example:** 100 people add to cart; 30 buy in the same session, 20 more buy the next day. Session view 30%; user view with a 2-day window 50%.
**Practice step:** For your own favourite shopping app, say which view suits a grocery order and which a laptop purchase.
**Likely follow-ups:** 1) *Which for a redesign test?* Both, randomised by user. 2) *Login problems?* If ids change after login, user funnels break.
**Common mistakes / traps:** Comparing a session rate with a user rate; not stating the window.

### Q33 ⭐⭐ 🟡 An edtech app has the free-trial funnel below. Compute step conversion, and find whether a 5-percentage-point improvement at the first step or at the last step gives more paid users.
| Step | Users |
|---|---|
| Signups | 20,000 |
| Trial started | 12,000 |
| Attended a class | 7,200 |
| Paid | 1,800 |
**Asked at:** commonly asked (no company-specific report found); edtech trial-funnel cases are posed on prep sites (unverified).
**What the interviewer is checking:** That you can compute and compare improvements through a chain of conversions.
**Say this in the interview:** "Step rates are 60%, 60% and 25%. Five points at the last step (25% to 30%) adds 360 paid users, versus 150 for five points at the first step, so the last step wins."

**Definition in plain words:** Step conversion = users at step / users at the previous step. Paid users = signups x rate1 x rate2 x rate3.
**Worked answer:** 1) Trial started: 12,000 / 20,000 = 60%. 2) Attended: 7,200 / 12,000 = 60%. 3) Paid: 1,800 / 7,200 = 25%. Overall 1,800 / 20,000 = 9%. 4) Option A, first step 60% to 65%: 20,000 x 0.65 x 0.60 x 0.25 = 1,950, a gain of 150. 5) Option B, last step 25% to 30%: 20,000 x 0.60 x 0.60 x 0.30 = 2,160, a gain of 360.
**Result:** Last-step improvement gives 360 extra paid users, 2.4 times as many as the 150 from the first step.
**Check:** The last step has the smallest base (rate 25%), so each point is a bigger relative jump (+20% versus +8.3%).
**Caveats:** Equal percentage points are not equal effort: lifting signup-to-trial by 5 points may be easier than lifting a paying decision by 5 points. If the improvements were an equal relative 5% on any step, each gives the same 90 users. Late-funnel users are also usually more intent-heavy, so the extra converters may be lower quality than assumed.
**Likely follow-ups:** 1) *Which would you work on?* Compare lift gain per unit of effort and cost. 2) *Does the order matter?* Not for the arithmetic, since it is a product.
**Common mistakes / traps:** Adding 5 points to the count rather than the rate; ignoring that points and percentages differ.

### Q34 ⭐⭐ 🟡 Historically 50% of all eventual paid conversions happen within 1 day of signup, 80% within 3 days and 95% within 7 days. The Monday signup cohort shows 2.4% paid after 3 days. What final conversion do you expect, and what does this say about reading last week's conversion?
**Asked at:** commonly asked (no company-specific report found); a gap-fill item in the sources file (unverified).
**What the interviewer is checking:** Awareness of immature cohorts and the ability to scale by a maturity curve.
**Say this in the interview:** "At day 3 only 80% of the eventual conversions have happened, so the final conversion is about 2.4% / 0.8 = 3.0%. Last week's conversion looks low simply because the cohort is not mature yet."

**Definition in plain words:** Conversion matures over time. Final conversion = conversion so far / share of conversions normally complete by now.
**Worked answer:** 1) Share complete by day 3 = 80%. 2) Final = 2.4% / 0.80 = 3.0%. 3) At day 7 we expect 0.95 x 3.0% = 2.85%. 4) Still to come after day 3: 0.6 percentage points (3.0% - 2.4%).
**Result:** Expected final conversion about 3.0%, (roughly 2.85% by day 7).
**Check:** 80% of 3.0% = 2.4%, which matches. For comparison, a cohort only 1 day old would show about 1.5%, which is also "normal" when read against the curve.
**Caveats:** The curve is historical; a promotion or a new trial length can shift it. Small cohorts give wide error bands. Compare cohorts at the same age (day 3 versus day 3), not at the same calendar date.
**What it says about last week:** A dashboard showing last week's conversion on Friday mixes cohort ages, so it will look like a drop that is not real. Report mature cohorts, or label recent ones "estimated" using the curve.
**Likely follow-ups:** 1) *Risk?* If the curve is changing (users deciding faster or slower), the projection misleads. 2) *Alternative?* Use fixed-window conversion (paid within 7 days).
**Common mistakes / traps:** Panicking at a "drop" in recent cohorts; dividing by the wrong share (95% instead of 80%).

### Q35 ⭐⭐ 🟡 A fintech app has the onboarding funnel below. Compute each step conversion, identify the biggest friction point and give two hypotheses with data to test each.
| Step | Users |
|---|---|
| App installs | 100,000 |
| Signup complete | 70,000 |
| KYC started | 35,000 |
| KYC completed | 21,000 |
| First transaction | 10,500 |
**Asked at:** commonly asked (no company-specific report found); fintech onboarding and KYC funnels are a typical product-case theme (unverified).
**What the interviewer is checking:** Whether you find the real leak (rate and volume) and propose testable hypotheses.
**Say this in the interview:** "Step rates: 70%, 50%, 60%, 50%; overall 10.5%. The biggest friction is signup to KYC start: it is tied for the lowest rate at 50% and loses the most users, 35,000."

**Definition in plain words:** Step conversion = users at step / users at previous step; friction = a step with a low rate and a large number of users lost.
**Worked answer:** 1) Signup: 70,000 / 100,000 = 70%. 2) KYC started: 35,000 / 70,000 = 50%. 3) KYC completed: 21,000 / 35,000 = 60%. 4) First transaction: 10,500 / 21,000 = 50%. 5) Overall: 10,500 / 100,000 = 10.5%.
**Result:** 70%, 50%, 60%, 50%. Users lost: 30,000, 35,000, 14,000, 10,500.
**Check:** 0.7 x 0.5 x 0.6 x 0.5 = 0.105.
**Biggest friction point:** Two steps tie on rate (50%); I pick signup to KYC start because it loses the most users. First transaction is the next target because those users have already finished KYC.
**Hypothesis 1:** Users do not see why KYC is needed at that moment (asked before any value is shown). Data: drop at the KYC prompt screen, time on that screen, split by whether the user had browsed the app first; test by delaying KYC until the first transaction attempt.
**Hypothesis 2:** The document step is scary or fails (Aadhaar or PAN consent, OTP failures, camera issues). Data: errors and OTP failure rate by device and app version, and drop by document type; test with a simpler path or retry help.
**Caveats:** Some installs are bots or curious browsers; use signups as the base when judging KYC.
**Likely follow-ups:** 1) *Next?* Segment by acquisition channel. 2) *First-transaction drop?* Prompt a small first payment or cashback (test with an A/B).
**Common mistakes / traps:** Looking only at percentage and ignoring volume; proposing a fix without data to test it.

### Q36 ⭐⭐ 🟡 A ride-hailing funnel is below. Compute the conversion at each step and say which steps point to supply-side problems and which to demand-side problems.
| Step | Count |
|---|---|
| Ride requests | 100,000 |
| Driver assigned | 80,000 |
| Driver reached pickup | 68,000 |
| Trip completed | 64,600 |
**Asked at:** commonly asked (no company-specific report found); marketplace funnel splits are a standard product-case theme (unverified).
**What the interviewer is checking:** That you can read a two-sided marketplace funnel and attach each leak to its likely side.
**Say this in the interview:** "Step rates are 80%, 85% and 95%; overall 64.6%. The first two steps are mainly supply-side (no driver, driver cancels), the last is mainly demand-side (rider cancels), though each has mixed causes."

**Definition in plain words:** Step conversion = count at step / count at previous step. Supply means drivers; demand means riders.
**Worked answer:** 1) Driver assigned: 80,000 / 100,000 = 80%. 2) Reached pickup: 68,000 / 80,000 = 85%. 3) Completed: 64,600 / 68,000 = 95%. 4) Overall 64.6%.
**Result:** 80%, 85%, 95%. Lost: 20,000, 12,000, 3,400.
**Check:** 0.8 x 0.85 x 0.95 = 0.646.
**Which side:** Request to assignment (80%): supply, no nearby drivers or low acceptance. Assignment to pickup (85%): mostly supply (driver cancels, long arrival time), partly demand (rider cancels while waiting). Pickup to completion (95%): mostly demand (rider cancelled or changed mind), partly supply (driver asked rider to cancel).
**Caveats:** Cancellation reasons are the key to separating sides; use wait time, price, and time of day to split.
**Likely follow-ups:** 1) *Biggest lever?* Request to assignment, 20,000 lost. 2) *Data?* Cancellations by reason and who cancelled; split by city, hour and distance.
**Common mistakes / traps:** Blaming all drop-off on supply; treating cancels after a long wait as rider-driven.

### Q37 ⭐⭐ 🟡 Compute the average rating before and after for a delivery app, and explain why the average alone can mislead and what else you would look at.
| Stars | Share before | Share after |
|---|---|---|
| 5 | 60% | 55% |
| 4 | 20% | 20% |
| 3 | 8% | 8% |
| 2 | 4% | 4% |
| 1 | 8% | 13% |
**Asked at:** commonly asked (no company-specific report found); rating and review metrics are a typical product-case topic (unverified).
**What the interviewer is checking:** Weighted average arithmetic and the ability to look at the distribution.
**Say this in the interview:** "The average falls from 4.20 to 4.00. The drop comes from 5-star ratings turning into 1-star, so the share of unhappy customers (1 or 2 stars) rose from 12% to 17%."

**Definition in plain words:** Average rating = sum of (stars x share of ratings). Both columns add to 100%.
**Worked answer:** Before: 5 x 0.60 + 4 x 0.20 + 3 x 0.08 + 2 x 0.04 + 1 x 0.08 = 3.00 + 0.80 + 0.24 + 0.08 + 0.08 = 4.20. After: 2.75 + 0.80 + 0.24 + 0.08 + 0.13 = 4.00.
**Result:** 4.20 before, 4.00 after (down 0.20 stars).
**Check:** Shares sum to 100% in both columns; the entire shift is 5 points from 5-star to 1-star.
**Why the average misleads:** It hides the shape: a 4.0 can be mostly 4s, or a mix of 5s and 1s as here (a polarised customer base). The 1-star share, up 5 points (a 62% relative rise from 8% to 13%), is the real alarm. Also look at: the count of ratings and response rate (who rates), rating by order type, restaurant, city and delivery partner, tags or comments for 1-star orders (late, wrong item, cold), refunds, and repeat orders from those customers.
**Caveats:** Ratings are voluntary, so unhappy people may be over-represented; a change in the prompt wording or when it appears can shift ratings on its own.
**Likely follow-ups:** 1) *Better single metric?* Share of 4-5 stars or share of 1-2 stars (top box and bottom box). 2) *Compare before and after?* Same-length windows, same mix of cities.
**Common mistakes / traps:** Quoting the average only; ignoring volume; treating 4.0 as "fine".

### Q38 ⭐⭐ 🟡 A recommendation widget gets 1 million impressions, a 6% click rate and a 10% click-to-order rate. A holdout test shows only 2,800 of these orders are incremental. Compute the attributed orders and the incrementality ratio, and say which number you would report.
**Asked at:** commonly asked (no company-specific report found); incrementality is a gap-fill item in the sources file (unverified).
**What the interviewer is checking:** Whether you separate attributed orders from orders caused by the feature.
**Say this in the interview:** "Attributed orders are 6,000; only 2,800 are incremental, an incrementality ratio of 46.7%. I would report the incremental number, with the attributed number shown as context."

**Definition in plain words:** Attributed orders are those that follow a click on the widget. Incremental orders are those that would not have happened without it, measured by a holdout group that does not see the widget. Incrementality ratio = incremental orders / attributed orders.
**Worked answer:** 1) Clicks = 1,000,000 x 6% = 60,000. 2) Attributed orders = 60,000 x 10% = 6,000. 3) Ratio = 2,800 / 6,000 = 0.467.
**Result:** 6,000 attributed; 2,800 incremental; ratio 46.7%. The other 3,200 orders were bought anyway (the user may have found the item without the widget).
**Check:** 2,800 / 1,000,000 impressions = 0.28 incremental orders per 100 impressions versus 0.6 attributed.
**Caveats:** The holdout must be randomised and sized so the 2,800 is not noise (give a confidence interval). Some widget effects are indirect (basket size, repeat visits) and some orders may be moved from another page (cannibalised).
**Likely follow-ups:** 1) *Why not use attributed?* It over-credits features placed where users already intend to buy. 2) *Use for budget?* Divide cost by incremental orders.
**Common mistakes / traps:** Reporting 6,000 as the feature's impact; computing CTR on orders instead of impressions.

### Q39 ⭐⭐ 🟡 Daily active users rose from 300,000 to 330,000 after a streak feature, while monthly active users rose from 1.5 million to 1.55 million. Compute DAU/MAU before and after and interpret the change.
**Asked at:** commonly asked (no company-specific report found); DAU/MAU stickiness questions appear in prep banks (unverified).
**What the interviewer is checking:** Ratio arithmetic and the stickiness reading.
**Say this in the interview:** "DAU/MAU goes from 20.0% to 21.3%. DAU is up 10% but MAU only 3.3%, so existing users are coming more often rather than many new users joining; the streak is making the app stickier."

**Definition in plain words:** DAU/MAU is the average share of monthly users who use the app on a given day (stickiness). Formula: daily active users / monthly active users.
**Worked answer:** 1) Before: 300,000 / 1,500,000 = 20.0%. 2) After: 330,000 / 1,550,000 = 21.3%. 3) DAU change +10.0%; MAU change +3.3%. 4) A 20% ratio means a typical monthly user opens the app about 6 days a month; 21.3% is about 6.4 days (ratio x 30).
**Result:** 20.0% to 21.3%, up 1.3 points.
**Check:** 21.3 / 20.0 = 1.065, and 1.10 / 1.033 = 1.065, so the ratio change is DAU growth divided by MAU growth.
**Caveats:** A streak can create low-value opens (users open just to keep the streak), so check whether orders or learning per active user rose too. Look for novelty decay and for which cohort drives the rise; with no control group, seasonality could contribute.
**Likely follow-ups:** 1) *Is it causal?* Only with an A/B test or a comparable control group. 2) *Guardrail?* Uninstalls, notification opt-outs, and orders per DAU.
**Common mistakes / traps:** Calling DAU growth "user growth"; forgetting DAU and MAU should use the same definition of active.

### Q40 ⭐⭐ 🟡 How would you test whether forcing all new users through a three-question preference quiz improves day-7 retention?
**Asked at:** commonly asked (no company-specific report found); a gap-fill style experiment-design question (unverified).
**What the interviewer is checking:** Experiment design: randomisation, the right metric, sample size and guardrails.
**Say this in the interview:** "I would randomly split new users 50/50 into quiz and no-quiz, measure day-7 retention as the primary metric, watch quiz drop-off and day-1 as guardrails, and run until each group has enough users to detect a small lift."

**Clarify first:** How is "retained" defined (opened the app on day 7, or any time in days 1-7)? Is the quiz skippable in the control? What is baseline D7?
**Structure:**
- Randomise at user level at first open, with a stable assignment, and check a balanced split (sample-ratio check).
- Primary metric: D7 retention. Guardrails: signup completion, time to first order or key action, day-1 retention, uninstall rate.
- Sample size: with an assumed baseline of 20% and a lift of 2 percentage points worth detecting, about 6,300 users per group (95% confidence, 80% power).
- Duration: all users must reach day 7, so run at least one full week plus 7 days of follow-up to cover weekday patterns.
**What I would check, in order:** SRM, quiz completion rate, then D1 and D7 by group, then by channel and device.
**If the data shows...:** D7 up and signup completion flat: ship. D7 up but forced quiz hurts signup: try an optional or shorter quiz. No difference: remove the friction.
**Recommendation:** Run the test, decide on D7 with its confidence interval, and keep a small holdout to read D30.
**Likely follow-ups:** 1) *Why not pre-post?* Seasonality and campaigns confound it. 2) *Why forced?* Mandatory steps cause drop-off before retention can even start; measure it.
**Common mistakes / traps:** Comparing only users who completed the quiz (survivorship bias); stopping the test early.

### Q41 ⭐⭐ 🟡 New-user D1, D7 and D30 retention before and after an onboarding change are below. What do you conclude, and what do you check next?
| Retention | Before | After |
|---|---|---|
| D1 | 40% | 42% |
| D7 | 20% | 26% |
| D30 | 12% | 12% |
**Asked at:** commonly asked (no company-specific report found); retention-curve interpretation is a recurring prep-bank theme (unverified).
**What the interviewer is checking:** Whether you read all three points together and challenge a tidy story.
**Say this in the interview:** "D1 is up 2 points and D7 up 6 points (a 30% relative lift), but D30 is flat at 12%. So the change brought people back for a week but did not build a lasting habit, and the D7 jump looks unusually large next to D1."

**Clarify first:** Is it an A/B test or a before-and-after comparison? How many users in each group? How is D7 defined?
**Structure:**
- Absolute changes: D1 +2.0 points; D7 +6.0 points (26/20 = 1.30); D30 0.0 points.
- Possible explanation: the new onboarding triggers reminders or rewards that bring users back for about a week, and the effect fades by D30.
- Oddity: D7 improving by more than D1 is possible but worth testing (a definition change, such as "active within days 1-7" versus "active exactly on day 7", or a notification campaign on day 6 or 7).
**What I would check, in order:** (1) Group sizes and confidence intervals on each number; (2) the D7 definition and whether the cohorts are fully matured; (3) the full daily curve between D7 and D30; (4) segments: channel, device, new versus returning; (5) what changed in the push notifications or incentives.
**If the data shows...:** The decay is a fade, so keep the change but add habit builders (week-2 content, reminders) and test D30 again. D7 is driven by one segment or a promo: do not generalise. The cohort for D30 is immature: wait before concluding.
**Recommendation:** Treat it as a partial win: ship if cost is low, but report D30 as the success metric and follow a long-term holdout.
**Likely follow-ups:** 1) *Which metric matters?* The one tied to value (D30 or paid conversion). 2) *Is 12% unchanged a failure?* It may be noise; check the interval.
**Common mistakes / traps:** Celebrating D7 alone; comparing retention definitions that differ; ignoring sample sizes.

### Q42 ⭐⭐ 🟡 A feature's weekly lift in orders per user is 12%, 8%, 5% and 3% over four weeks. How do you estimate the steady-state effect, and what do you tell the team?
**Asked at:** commonly asked (no company-specific report found); novelty effect questions appear in experimentation prep (unverified).
**What the interviewer is checking:** That you recognise a novelty effect and do not report the week-1 number.
**Say this in the interview:** "The lift is decaying: week-on-week it is about 0.6 to 0.67 of the previous week. If that continues, the steady-state is close to 1 to 2% or even near zero, so I would not plan on 12%. I would extend the test or keep a holdout until it flattens."

**Explain simply:**
- Ratios between weeks: 8/12 = 0.67, 5/8 = 0.63, 3/5 = 0.60. A constant ratio of about 0.63 would give next weeks near 1.9%, 1.2%, 0.8% and 0.5%, tending towards zero.
- A plateau is also possible (for example a permanent 1-2%); four points cannot tell these apart.
- Averaging the four weeks (7.0%) overstates the lasting effect; the last week (3%) is the most informative, but is still a moving target.
**Mini-example (illustrative):** If the real floor is 1.5%, then a 10,000-order-per-day base gains about 150 orders a day, not the 1,200 implied by week 1.
**What I tell the team:** Novelty is wearing off. Plan with a range (0 to 2%), keep a small long-term holdout, split by new versus existing users (novelty hits existing users hardest), and decide on the week-4 or later number, with its confidence interval.
**Likely follow-ups:** 1) *How long to run?* Until the weekly lift stops falling over two consecutive weeks. 2) *Could it be seasonality?* Only if there is no concurrent control group.
**Common mistakes / traps:** Reporting the average or week 1; treating weekly lift as cumulative; concluding "no effect" before the curve flattens.

### Q43 ⭐⭐ 🟡 A new feature raises daily active users but lowers average session length. How do you decide whether this is a win?
**Asked at:** commonly asked (no company-specific report found); metric-conflict questions are a typical product-sense theme (unverified).
**What the interviewer is checking:** Whether you anchor on the goal and a business outcome, not on a single engagement metric.
**Say this in the interview:** "I would decide by what the product is for. If success is orders or learning, a shorter session can mean users get things done faster. I would check total time and outcome per user, and conversion per session."

**Clarify first:** What is the product goal (orders, lessons, time on content)? Was this an A/B test? How much did each move?
**Structure:**
- Total engagement = users x sessions x minutes. Illustrative: DAU 100,000 to 110,000 (+10%) and session 10 to 8.5 minutes (-15%): total minutes 1,000,000 to 935,000 (-6.5%).
- Is the shorter session good (faster task completion) or bad (people leave sooner, lower content quality)?
**What I would check, in order:** (1) Outcome per active user and per session (orders, completed lessons, revenue); (2) sessions per user, since users may come more often for quick tasks; (3) segment: new users (whose short sessions may be bounces) versus existing; (4) quality signals (uninstalls, ratings, complaints); (5) whether the new DAU are incremental or just moved from other surfaces.
**If the data shows...:** Outcomes per user up: win. Outcomes flat while minutes fall: neutral or a mild loss; check why. Outcomes down: loss, even though DAU rose.
**Recommendation:** Name one headline outcome metric before launching; treat DAU and session length as diagnostics.
**Likely follow-ups:** 1) *Is longer always better?* No, for utility apps shorter can mean efficient. 2) *For ad-based apps?* Time matters directly.
**Common mistakes / traps:** Picking the metric that supports the story; ignoring that session length is an average that new short sessions pull down.

### Q44 ⭐⭐ 🟡 A new feature is used by only 2% of users but those users generate 15% of revenue. How do you decide whether to keep, fix or remove it?
**Asked at:** commonly asked (no company-specific report found); a feature-keep-or-kill question, a common product-analytics theme (unverified).
**What the interviewer is checking:** That you test causation (are they valuable because of the feature, or valuable anyway) and consider cost and potential.
**Say this in the interview:** "Those users bring about 7.5 times their share, but heavy buyers often adopt features first, so I would check whether the feature causes the revenue. Then I would weigh incremental value, cost and whether low adoption is a discovery problem."

**Clarify first:** What is the feature, what does it cost to run, and how were the users exposed to it?
**Structure:**
- Arithmetic: if revenue per average user is 1, feature users earn 0.15 / 0.02 = 7.5; other users earn 0.85 / 0.98 = 0.87, so feature users earn about 8.6 times as much as others.
- Hypotheses: (a) the feature causes higher spend; (b) it is used by already heavy users (selection); (c) it replaced revenue from another feature (cannibalisation).
**What I would check, in order:** (1) Revenue of the same users before and after adopting; (2) a matched comparison or a holdout with randomised exposure; (3) adoption funnel: how many saw the feature and how many tried it; (4) cost to maintain, and risk to core flows.
**If the data shows...:** Incremental revenue clearly exceeds cost: keep, and improve discovery to raise the 2%. Users are valuable regardless: fix or merge it if cheap, or remove it to cut complexity. Few see it but conversion on seeing is high: fix visibility.
**Recommendation:** Run a holdout or staged exposure test before any removal; decide with incremental revenue per user times reachable users minus cost.
**Likely follow-ups:** 1) *If you removed it?* Warn the 2%; watch their retention. 2) *Quick test?* Hide it from a random 10% of eligible users.
**Common mistakes / traps:** Treating 15% as the feature's causal contribution; judging by usage share alone.

### Q45 ⭐⭐ 🟡 A paid membership programme (free delivery for a monthly fee) has 200,000 members ordering 5.0 times a month, against 3.8 for a matched group of non-members. Compute the incremental orders per month and list the assumptions behind it.
**Asked at:** commonly asked (no company-specific report found); membership-incrementality is a gap-fill item in the sources file (unverified).
**What the interviewer is checking:** Simple difference arithmetic and awareness of selection bias.
**Say this in the interview:** "Members order 1.2 more times a month than the matched group, so incremental orders are 200,000 x 1.2 = 240,000 a month, about 24% of the members' 1,000,000 orders. That holds only if the matching is credible."

**Definition in plain words:** Incremental orders = (orders per member - orders per matched non-member) x number of members.
**Worked answer:** 1) Difference = 5.0 - 3.8 = 1.2 orders per member per month. 2) Incremental = 200,000 x 1.2 = 240,000. 3) Total member orders = 200,000 x 5.0 = 1,000,000, so 24% of these are incremental.
**Result:** About 240,000 incremental orders a month.
**Check:** Counterfactual orders = 200,000 x 3.8 = 760,000; 1,000,000 - 760,000 = 240,000.
**Assumptions:** (1) The matched group truly looks like members, matching on pre-signup order frequency, city, tenure and basket value. (2) People who join are already keen buyers: if so, the 1.2 is overstated, so use a before-and-after (difference-in-differences) comparison. (3) No other effect from join-time promotions. (4) Members do not shift orders from other days (pull-forward) or from other categories. (5) Orders, not margin: delivery fees waived and any subsidy reduce profit per order, so compare incremental contribution with the cost of the programme.
**Likely follow-ups:** 1) *Is it profitable?* Incremental orders x contribution margin plus fees, minus waived delivery cost. 2) *Better design?* Randomly offer a free trial to eligible users.
**Common mistakes / traps:** Counting all 1,000,000 member orders as programme-driven; ignoring self-selection.

### Q46 ⭐⭐ 🟡 What metrics and thresholds would you gate on at each stage of a staged rollout from 1% to 10% to 50% to 100% of users?
**Asked at:** commonly asked (no company-specific report found); a gap-fill item in the sources file (unverified).
**What the interviewer is checking:** Whether you match each stage to what it can detect, with explicit stop rules.
**Say this in the interview:** "Early stages guard safety (crashes, errors, latency); later stages read business metrics once there is enough traffic. At each gate I would write the go, hold and rollback thresholds before launch. The numbers below are illustrative."

**Explain simply:**
- 1% (technical safety, about 1 to 2 days): crash-free sessions no worse than baseline by more than 0.2 points, API error rate and p95 latency within 10% of baseline, no new serious support tickets, plus a sample-ratio check. Too few users to judge orders, so do not.
- 10% (early product signal, about 3 to 7 days): the same guardrails, plus funnel conversion not down by more than a pre-agreed amount (for example 1% relative) and the primary metric directionally positive; check payments and refunds.
- 50% (decision-grade read, about 1 to 2 weeks): enough power for the primary metric with a confidence interval, segment cuts (new versus existing users, device, city), load and cost checks, and support ticket rate.
- 100%: ship, with a small long-term holdout (for example 1 to 5%) to measure novelty decay and long-term effects.
**Rollback triggers:** crash-free rate below a hard floor, payment success drops more than a set amount, or a severe bug; use automatic kill-switches.
**Mini-example:** If baseline crash-free is 99.5%, gate 1% at 99.3% or higher (assumed).
**Likely follow-ups:** 1) *Why not jump to 50%?* A bug would hit half the users. 2) *Who decides?* The metric owner and the engineering lead, with thresholds agreed in advance.
**Common mistakes / traps:** Reading business metrics at 1%; no pre-set thresholds; no rollback plan.

### Q47 ⭐⭐ 🟡 Estimate the incremental monthly orders from a "schedule delivery" feature, and say how you would check the assumptions after launch.
Assumptions to use: 1,000,000 eligible monthly users; 10% adopt; each adopter places 2 scheduled orders per month; 50% of those orders would not otherwise have happened.
**Asked at:** commonly asked (no company-specific report found); scheduling-sizing is a gap-fill item in the sources file (unverified).
**What the interviewer is checking:** A clear chain of assumptions and a plan to validate each link.
**Say this in the interview:** "1,000,000 x 10% = 100,000 adopters; x 2 = 200,000 scheduled orders; x 50% = 100,000 incremental orders a month. After launch I would validate adoption, frequency and, above all, incrementality."

**Clarify first:** Are scheduled orders a new order or just moved in time? Fixed definition of adopter? Any extra cost?
**Approach:** Bottom-up chain using the given assumptions.
**Assumptions (given in the question; all assumed):**
| Input | Value | Check after launch |
|---|---|---|
| Eligible users | 1,000,000 | count from user table |
| Adoption | 10% | users with at least one scheduled order |
| Orders per adopter | 2 per month | average from logs |
| Incremental share | 50% | holdout or matched comparison |
**Calculation:** 1) Adopters = 1,000,000 x 0.10 = 100,000. 2) Scheduled orders = 100,000 x 2 = 200,000. 3) Incremental = 200,000 x 0.50 = 100,000.
**Result:** About 100,000 incremental orders a month (range, for example, 50,000 to 150,000 if incrementality is 25% to 75%).
**Sanity check:** 100,000 incremental orders is 0.1 per eligible user per month.
**Sensitivity:** The result is linear in each input; a 25% change in any single one changes the answer by 25%. Incrementality is the most uncertain, since adopters may simply be moving existing orders (cannibalisation), and adoption is next.
**Post-launch check:** Hide the feature from a random holdout group (for example 5% of users) and compare orders per user; track adoption funnel, orders per adopter, cancellation and failed deliveries, and the order timing of adopters before versus after.
**Likely follow-ups:** 1) *Biggest risk?* Cannibalisation of on-demand orders. 2) *Other effects?* Better delivery-slot utilisation, lower cost per order.
**Common mistakes / traps:** Assuming every scheduled order is incremental; no holdout.

### Q48 ⭐⭐ 🟡 After a release, the app crash-free session rate fell from 99.5% to 98.5% on 10 million weekly sessions. Crashed sessions convert at 0% and normal sessions at 5%. How many orders are lost per week, and how do you prioritise the fix?
**Asked at:** commonly asked (no company-specific report found); crash-rate impact is a gap-fill item in the sources file (unverified).
**What the interviewer is checking:** Translating a technical metric into business loss and prioritising.
**Say this in the interview:** "Crashed sessions rise from 0.5% to 1.5%, so 100,000 more sessions crash each week. At 5% conversion that is about 5,000 lost orders a week. I would fix it now and sort by the most-affected devices and flows."

**Definition in plain words:** Crash-free session rate = sessions without a crash / all sessions. Lost orders = extra crashed sessions x normal conversion rate.
**Worked answer:** 1) Crashed before: 0.5% x 10,000,000 = 50,000. After: 1.5% x 10,000,000 = 150,000. 2) Extra crashed sessions = 100,000. 3) Lost orders = 100,000 x 5% = 5,000 per week.
**Result:** About 5,000 orders lost per week due to the release (multiply by average order value for revenue).
**Check:** Orders before = 9,950,000 x 5% = 497,500; after = 9,850,000 x 5% = 492,500; difference 5,000, a 1.0% fall in orders.
**Caveats:** Assumes crashed sessions would have converted at the normal 5%; a crash may happen mid-session, users may retry and order (so the loss is overstated), or crashes may concentrate on high-intent screens such as payment (so the loss is understated). Also count retention damage and bad ratings.
**How to prioritise:** (1) Group crashes by signature, app version, OS and device, and where in the flow they occur; (2) rank by crashed sessions and by orders at risk; (3) fix or roll back the top signature first, since a few causes usually produce most crashes; (4) consider a rollback or a staged halt if the release is the cause; (5) add a crash guardrail to the release gate.
**Likely follow-ups:** 1) *Fix or roll back?* Roll back if the fix is slow; weekly loss of about 5,000 orders is material. 2) *How do you confirm recovery?* Crash-free rate and conversion return to baseline.
**Common mistakes / traps:** Using the whole 1.5% instead of the extra 1.0 point; ignoring where in the funnel crashes occur.

### Q49 ⭐⭐ 🟡 What is a conversion window in funnel analysis, and how can changing it from same-session to 7-day change your conclusions about a checkout redesign?
**Asked at:** commonly asked (no company-specific report found); funnel-measurement questions appear on prep banks such as PracHub and Dataford (unverified).
**What the interviewer is checking:** Whether you know that a funnel only counts a user as converted if the last step happens inside a set time limit, and that the limit changes the story.
**Say this in the interview:** "A conversion window is the time allowed between the first step and the last step. A same-session window punishes users who think and come back; a 7-day window captures them. I would report both before judging the redesign."
**Explain simply:**
- A funnel is a chain of steps (for example cart, address, payment, order). The conversion window is the clock: "count the order only if it happens within X of the cart step". Same-session means the same visit; 7-day means any time within a week.
- A redesign that makes checkout faster helps people who finish in one sitting, so it shows up in a same-session window. A redesign that nudges people to save the cart and return later (for example a saved-cart reminder) shows up only in the 7-day window.
- Illustrative numbers (made up): same-session conversion old 4.0%, new 4.4%, a 10% relative lift. 7-day conversion old 6.0%, new 6.1%, a 1.7% lift. The same-session lift looked large because the new design pulled orders forward in time, not because it created many new orders.
- The reverse also happens: same-session shows no gain while the 7-day window shows a gain.
**Practice step:** Pick one funnel and plot the share of eventual converters against hours since the first step; choose the window where the curve flattens.
**Likely follow-ups:** 1) *Which window do you pick?* The one that matches the buying cycle (food: same session or same day; electronics: 7 to 30 days), fixed before the test. 2) *What about recent cohorts?* Their long windows are incomplete, so compare cohorts only at the same age.
**Common mistakes / traps:** Changing the window after seeing the result; comparing a 7-day number for an old cohort with a 1-day number for a new one; ignoring that pulled-forward orders are not extra orders.

### Q50 ⭐⭐ 🟡 A marketplace seller-onboarding funnel is below. Compute the step conversion, find the biggest leak and give a hypothesis tree for it.
| Step | Sellers |
|---|---|
| Listing started | 50,000 |
| Listing completed | 30,000 |
| Listing approved | 24,000 |
| First order within 14 days | 6,000 |
**Asked at:** commonly asked (no company-specific report found); marketplace and seller funnels are a common prep-site product case (unverified).
**What the interviewer is checking:** Whether you compute step-to-step conversion correctly, separate the biggest percentage leak from the biggest absolute leak, and build a structured tree.
**Say this in the interview:** "Step conversions are 60%, 80% and 25%; overall 12%. The worst rate is approved to first order at 25%, so I would first ask whether approved sellers are getting visibility and demand."
**Definition in plain words:** Step conversion = sellers reaching a step divided by sellers at the previous step. Overall = last step divided by first step.
**Worked answer:**
1. Started to completed: 30,000 / 50,000 = 60% (20,000 lost).
2. Completed to approved: 24,000 / 30,000 = 80% (6,000 lost).
3. Approved to first order in 14 days: 6,000 / 24,000 = 25% (18,000 lost).
4. Overall: 6,000 / 50,000 = 12%.
**Result:** Lowest rate: step 3 (25%, 75% leak). Largest absolute loss: step 1 (20,000), but listing forms always lose casual starters, so step 3 is the more actionable leak.
**Hypothesis tree for step 3 (approved but no order in 14 days):**
- Supply side: poor listing quality (bad photos, wrong category), price above market, low stock, slow dispatch.
- Demand side: no search visibility for new listings (cold start), no buyers in the seller's category or pincode.
- Product or process: approved listing not live for hours or days, wrong tagging, seller never told it is live.
- Measurement: 14 days too short for slow categories; orders attributed to the wrong seller ID.
**Check:** 24,000 x 25% = 6,000; 50,000 x 0.6 x 0.8 x 0.25 = 6,000. Consistent.
**Caveats:** The same-sellers assumption (a seller counted once); seller type (new business vs existing offline shop) will differ sharply, so segment before concluding.
**Likely follow-ups:** 1) *First data cut?* Category and seller type (new vs experienced), then listing quality score. 2) *Quick fix?* Boost visibility for new approved listings and test its effect.
**Common mistakes / traps:** Quoting only the biggest absolute loss; mixing sellers and listings; not defining "approved" time lag.

### Q51 ⭐⭐ 🟡 After a release, sessions rose 30% but orders stayed flat. How do you tell whether this is a tracking bug or real behaviour?
**Asked at:** commonly asked (no company-specific report found); "validate the metric first" is a recurring theme in metric-drop prep questions (unverified).
**What the interviewer is checking:** Whether you test the measurement before explaining behaviour.
**Say this in the interview:** "I first check whether the session count itself changed definition. If a 30% jump arrived at the exact release time across all users, I suspect logging; if it is concentrated in a segment, it may be real."
**Clarify first:** Was the release a new app version, a login change or a new tracking SDK (software kit that logs events)? Is the 30% in all platforms? I fix scope: one app, week before vs week after.
**Structure:**
- Tracking bug: duplicate session_start events, session timeout changed, background or push-triggered sessions now counted, bot traffic, app version not logging properly.
- Real behaviour: users open the app more but do not buy (a new feed, notifications, a game or streak feature), or a redirect now makes users bounce.
**What I would check, in order:**
1. Timing: does the step change begin exactly at the release timestamp, and only on the new app version? (Split by version.)
2. Cross-source check: compare with server-side logs, web-server requests or a second analytics tool.
3. Event shape: sessions per user, session length, events per session; duplicates (same user, same second) point to a bug.
4. Segment: platform, new vs old version, country, traffic source.
5. Downstream: do other numbers move too (daily active users, page views, ad impressions)? Real behaviour usually moves related numbers consistently.
**If the data shows...:** Spike only on new version with many zero-length sessions: logging bug; fix and restate history. Spike in all versions, longer time in app, no orders: real; investigate the new feature pulling attention away from buying.
**Recommendation:** Do not report the session number until the check is done; tag the affected period in the dashboard; add a release-day logging check to the QA list.
**Likely follow-ups:** 1) *Orders flat but sessions up means what for conversion?* Session conversion fell by 1 - 1/1.3, about 23% relative; but only meaningful if sessions are real. 2) *Which source do you trust?* Orders from the payment database; they are harder to double count.
**Common mistakes / traps:** Jumping to product causes; not splitting by app version; trusting one tool.

### Q52 ⭐⭐ 🟡 Two features were launched in the same week and orders rose 5%. How would you attribute the lift to each feature?
**Asked at:** commonly asked (no company-specific report found); attribution of overlapping launches is a standard product-analytics follow-up (unverified).
**What the interviewer is checking:** Whether you know that a before/after cannot split the lift, and what design can.
**Say this in the interview:** "A single combined 5% cannot be split after the fact without a comparison group. I would use holdouts or a staggered rollout; if they are not available, I would use regional or user-level exposure differences, with clearly stated caveats."
**Clarify first:** Were both launched to everyone? Are they in the same screen? Was anything else running (festival, price change)? I assume nothing else changed.
**Structure:**
- Best: a 2x2 experiment (A on/off, B on/off), or a holdout for each. Illustrative made-up readout: control 1.00 orders per user, only A 1.03, only B 1.02, both 1.05. Then A adds about 3%, B about 2%, and together 5%, so effects are roughly additive here.
- If already live for all: look for natural variation (staggered city or version rollout, users who have not updated the app) and compare exposed vs not exposed, controlling for user type.
- Where there is no variation: a before/after plus a timing logic (which feature touches which funnel step) gives only a rough, labelled guess.
**What I would check, in order:** exposure logs per feature; funnel step each feature should move; overlap of users; interaction (do effects add or overlap?).
**If the data shows...:** Both features target the same step: the effects likely overlap, do not add. Different steps: a split by step is more believable.
**Recommendation:** Say honestly that without a comparison group the split is an estimate; keep a small holdout for each future launch.
**Likely follow-ups:** 1) *Why not just use before/after?* Seasonality and other changes also contribute. 2) *Can you assign 3% and 2% by proportion of use?* No; usage share does not equal impact.
**Common mistakes / traps:** Splitting the lift 50:50; ignoring interaction; ignoring a festival week.

### Q53 ⭐⭐ 🟡 A new offers screen is launched in Hyderabad only. Use the data to estimate the effect with a difference-in-differences approach, and state the assumptions.
| City | Orders per active user per week before | After |
|---|---|---|
| Hyderabad (launch) | 2.0 | 2.4 |
| Bengaluru (no launch) | 2.2 | 2.35 |
**Asked at:** commonly asked (no company-specific report found); a gap-fill from standard analytics practice, not tied to a reported question.
**What the interviewer is checking:** Whether you subtract the background trend seen in the comparison city instead of crediting the whole rise.
**Say this in the interview:** "Hyderabad rose 0.40 and Bengaluru, which had no launch, rose 0.15, so the launch effect is about 0.25 orders per user per week, roughly 12% of the starting level."
**Definition in plain words:** Difference-in-differences compares the change in the launch city with the change in a similar city that did not launch. The difference of the two changes strips out what would have happened anyway.
**Worked answer:**
1. Hyderabad change = 2.4 - 2.0 = +0.40.
2. Bengaluru change = 2.35 - 2.2 = +0.15 (the background trend, such as a festival or season).
3. Effect = 0.40 - 0.15 = +0.25 orders per active user per week.
4. Relative to Hyderabad's counterfactual: Hyderabad would have reached about 2.0 + 0.15 = 2.15 without the launch, so the lift is 2.4 / 2.15 - 1 = about 11.6%. Relative to its starting 2.0 it is 12.5%. The naive before/after of 20% overstates it.
**Result:** About +0.25 orders per user per week (about +12%); the naive +0.40 is too high by 0.15.
**Check:** Counterfactual 2.15 + effect 0.25 = 2.4. Matches.
**Caveats (assumptions):** Parallel trends (the two cities would have moved alike without the launch; check several pre-launch weeks); no other local change in Hyderabad (a local promotion); no spillover between cities; only two cities, so no confidence interval, add more control cities or use a synthetic control (a weighted mix of cities).
**Likely follow-ups:** 1) *How do you test parallel trends?* Compare weekly trends for 8 or more weeks before launch. 2) *Why not randomise users?* DiD is for cases like a city launch where user-level randomisation was not done.
**Common mistakes / traps:** Reporting 0.40 as the effect; choosing a comparison city of a different size or season pattern.

### Q54 ⭐⭐ 🟡 A checkout redesign raises conversion from 5.0% to 5.5% but average order value falls from Rs 520 to Rs 450. Compute revenue per visitor before and after and decide whether to ship.
**Asked at:** commonly asked (no company-specific report found); trade-off between conversion and basket size is a standard product-metric question (unverified).
**What the interviewer is checking:** Whether you combine the two moves into one figure (revenue per visitor) and then think beyond revenue to margin.
**Say this in the interview:** "Revenue per visitor falls from Rs 26.00 to Rs 24.75, down 4.8%. On this evidence I would not ship as is."
**Definition in plain words:** Revenue per visitor = conversion rate x average order value.
**Worked answer:**
1. Before: 0.050 x 520 = Rs 26.00.
2. After: 0.055 x 450 = Rs 24.75.
3. Change = -Rs 1.25 per visitor, which is -4.8%.
4. Break-even: at 5.5% conversion, AOV must be at least 26.00 / 0.055 = about Rs 473. At Rs 450 AOV, conversion would have to be at least 26.00 / 450 = 5.78%.
**Result:** Rs 26.00 to Rs 24.75 per visitor; do not ship on revenue grounds.
**Check:** Orders per 1,000 visitors rise from 50 to 55 (+10%), AOV falls 13.5%: 1.10 x 0.865 = 0.952, so -4.8%. Matches.
**Caveats:** Revenue is not profit: if the lower AOV came from fewer add-on items with low margin, or if delivery cost per order is fixed, contribution can fall further; if the new customers are first-time buyers worth more later, the answer can change. Ask why AOV fell (removed upsell? coupon more visible?). Confirm the result is statistically sound.
**Likely follow-ups:** 1) *Can you keep conversion and fix AOV?* Yes: restore the upsell step lower in the flow and retest. 2) *What if margin per order is fixed?* Then compare contribution per visitor.
**Common mistakes / traps:** Celebrating the conversion rise; comparing revenue per order not per visitor.

### Q55 ⭐⭐ 🟡 A push-notification change raises orders per user from 1.00 to 1.06 per month for 1 million users, but monthly uninstalls rise from 3.0% to 4.5%. Compute the monthly order gain and the extra users lost, and say how you would judge the trade-off.
**Asked at:** commonly asked (no company-specific report found); guardrail-versus-primary-metric trade-off is a standard prep-bank theme (unverified).
**What the interviewer is checking:** Whether you put the short-term gain and the long-term loss on one scale.
**Say this in the interview:** "The gain is 60,000 orders a month; the extra uninstalls are 15,000 users a month. Each lost user stops ordering for months, so after a few months the loss overtakes the gain unless the lost users were low-value."
**Worked answer:**
1. Order gain = 1,000,000 x (1.06 - 1.00) = 60,000 extra orders per month.
2. Extra users lost = 1,000,000 x (4.5% - 3.0%) = 15,000 per month.
3. Ratio: 60,000 / 15,000 = 4 extra orders per extra uninstall in month one.
4. Simple compounding model (assumed, made up): the higher uninstall rate repeats every month, lost users never come back, and a user orders 1.0 time a month. Treatment base after month n is 1M x 0.955^n, control 1M x 0.97^n. Net orders vs control: +42,300 in month 1, +10,600 in month 3, about -3,600 in month 4, and the running total turns negative in month 7 (about -10,500) and is about -350,000 by month 12.
**Result:** +60,000 orders in the first month, 15,000 extra users lost per month; under the stated assumptions the change loses value by around month 7.
**Check:** Month 1: 955,000 x 1.06 - 970,000 x 1.00 = 1,012,300 - 970,000 = 42,300 (smaller than 60,000 because lost users are already out of the base).
**Caveats:** Uninstalls may be reversible (people reinstall); the lost users may be the least engaged; the effect may be temporary (novelty); judge on user lifetime value and re-engagement, not on one month. Test with a holdout and track 60-day retention and notification opt-outs.
**Likely follow-ups:** 1) *What would you propose?* Cap notification frequency or personalise, then retest. 2) *Which metric decides?* Value per user over a longer period, e.g. 90-day orders per original user.
**Common mistakes / traps:** Comparing 60,000 orders with 15,000 users as if they were the same unit; ignoring compounding.

### Q56 ⭐⭐ 🟡 A product team shows a retention curve that keeps falling and never flattens. What does it imply for product-market fit and what would you analyse?
**Asked at:** commonly asked (no company-specific report found); cohort retention and "growth masking retention decay" appear on prep sites such as PracHub (unverified).
**What the interviewer is checking:** Whether you understand the flattening curve as the sign of a loyal core.
**Say this in the interview:** "A curve that never flattens means every cohort keeps leaking, so there is no stable group of users who find lasting value. That is weak product-market fit, though I would check whether we are looking at the right users and time scale."
**Explain simply:**
- A retention curve shows, for a group of users who joined together (a cohort), the share still active after day 1, 7, 30 and so on. For a product with fit, the line falls and then goes flat at some level (say 20%); those are the loyal users.
- A curve still sliding to zero means users try and leave. Growth may look healthy only because new signups replace the leavers (a leaky bucket).
- Mini example (made up): cohort of 1,000: day 30 = 20%, day 60 = 12%, day 90 = 7%. Each month loses about 40% of what remains, no floor.
**What I would analyse:** cohorts by month (is it improving?); segments (acquisition channel, city, device, plan) to find any group that flattens; usage frequency that fits the product (a bill-pay app may be monthly, so daily retention is the wrong lens); users who did the "aha" action early vs those who did not; reason for leaving.
**Practice step:** Draw cohort curves by channel for the last 6 months; look for one that levels off and study what those users did.
**Likely follow-ups:** 1) *Could the curve be fine anyway?* Yes, if usage is naturally occasional and revenue per cohort still holds. 2) *What to do?* Fix onboarding or find the segment that sticks and focus there.
**Common mistakes / traps:** Using the average across all users; wrong time scale; reading rising monthly active users as proof of fit.

### Q57 ⭐⭐ 🟡 How would you evaluate the success of a new search feature (autocomplete and filters) in an e-commerce app?
**Asked at:** commonly asked (no company-specific report found); feature-success measurement is a standard prep-bank topic (unverified).
**What the interviewer is checking:** Whether you define a goal, a primary metric, diagnostics and guardrails, and plan an experiment.
**Say this in the interview:** "The goal is helping users find what they want faster. My primary metric is search-to-order conversion (orders from sessions that used search); diagnostics cover autocomplete use and filter use; guardrails are latency and zero-result rate."
**Clarify first:** Who uses search (new vs returning)? What was there before? Is there an A/B split? I assume a 50:50 test.
**Structure:**
- Goal: shorter path from intent to purchase.
- Primary: search conversion = orders from sessions with a search / sessions with a search.
- Diagnostics: share of searches using autocomplete; filter usage rate; time to first click; queries per session (fewer reformulations is better); click position of the purchased item.
- Guardrails: total orders per user (search conversion can rise by moving orders away from browsing), search latency, zero-result rate, revenue per visitor, returns.
**What I would check, in order:** adoption (who uses it), then diagnostic movement, then primary, then guardrails; split by new vs returning and by category.
**If the data shows...:** Adoption high, conversion flat: users are using it but it does not help results; look at ranking. Conversion up but total orders flat: search just cannibalised browse.
**Recommendation:** Ship if search conversion and total orders per user improve with guardrails stable; tune ranking otherwise.
**Likely follow-ups:** 1) *What is the pitfall in "search conversion"?* Selection: people who search already intend to buy. 2) *Experiment unit?* User level, with consistent assignment.
**Common mistakes / traps:** Using clicks on autocomplete as success; measuring only searchers; no guardrail.

### Q58 ⭐⭐ 🟡 Day-1 retention of new users on an edtech app fell from 45% to 38% over two weeks. List the data cuts and hypotheses in the order you would test them.
**Asked at:** commonly asked (no company-specific report found); retention-drop diagnosis is a recurring prep-bank pattern (unverified).
**What the interviewer is checking:** Whether you verify the measurement first, then segment from broad to narrow, then reach causes.
**Say this in the interview:** "A fall from 45% to 38% is 7 points, about 16% relative. I would check whether it is real, then cut by acquisition channel, app version and platform, because mix shifts and releases are the most common causes."
**Clarify first:** How is Day-1 retention defined (opened the app on the next calendar day)? Which users (new installs)? Was there a release, campaign or exam-season change in these two weeks?
**Structure and order:**
1. Measurement: definition unchanged, logging complete, cohort size big enough (7 points on a few hundred users could be noise).
2. Timing: did it drop on one date (release or campaign) or slide gradually (seasonality, quality)?
3. Mix (cut by acquisition channel, city, new-user age, language): a new low-intent paid channel can lower the average although every channel is unchanged. Check by computing retention within each channel.
4. Platform, app version, device (a crash or slowness on one version).
5. Onboarding funnel: did fewer users reach the first lesson? Check each step.
6. Product and content: first-lesson quality, notification changes, content change.
7. External: exam calendar, holidays, a competitor offer.
**If the data shows...:** Fall within every channel and one version: bug or release issue. Fall only in the average: mix shift, not a product problem.
**Recommendation:** Fix or roll back the cause; track D1 by cohort daily.
**Likely follow-ups:** 1) *What if it is a mix shift?* Report like-for-like and judge the channel on cost per retained user. 2) *First number to compute?* Retention by channel for both periods.
**Common mistakes / traps:** Blaming the release without a version split; ignoring cohort size.

### Q59 ⭐⭐ 🔴 A feature raises revenue by 3% but lowers NPS by 2 points and raises support tickets by 10%. How do you decide whether to roll back?
**Asked at:** commonly asked (no company-specific report found); a gap-fill about balancing a primary metric against guardrails.
**What the interviewer is checking:** Whether you price the harm, ask whether it is temporary and avoid a mechanical rule.
**Say this in the interview:** "I would put all three on a common scale: revenue, cost of the extra tickets, and the future revenue at risk from lower satisfaction. If the harm is small and fixable, I would keep it and fix; if the damage hits loyal customers or grows, I would roll back."
**Clarify first:** Is the 3% revenue incremental (from an A/B test)? Is the NPS change statistically real? Which tickets rose and why?
**Structure:**
- Gain: +3% revenue; convert to contribution.
- Direct cost: tickets +10%. Example (assumed): if support cost is 2% of revenue, +10% tickets costs about 0.2% of revenue, small next to +3%.
- Indirect risk: NPS -2 points may predict higher churn and lower repeat orders; estimate from historic link between NPS and retention.
- Nature of the pain: confusing flow (fixable) vs deceptive or pushy design (trust damage).
**What I would check, in order:** significance and segments (are heavy users hurt?); ticket reasons; retention and repeat rate of the exposed group over 4 to 8 weeks; refund and complaint rates.
**If the data shows...:** Tickets about one fixable bug and retention flat: keep, fix, monitor. Retention of core users falls or the revenue is pulled-forward: roll back or redesign.
**Recommendation:** Do not decide on the 3% alone; set the roll-back thresholds up front (for example retention loss beyond X) and keep a holdout while fixing.
**Likely follow-ups:** 1) *How long to wait?* Long enough to see repeat behaviour, usually several weeks. 2) *Is NPS enough?* No; it is a survey with few responses, so use behaviour.
**Common mistakes / traps:** A rule such as "revenue up so ship"; ignoring that support cost is small but churn is large.

### Q60 ⭐⭐ 🔴 You can only measure three-month retention but the team must decide in two weeks whether to roll out a feature. How do you decide?
**Asked at:** commonly asked (no company-specific report found); surrogate and early-indicator measurement appears in prep-site feature-evaluation items (unverified).
**What the interviewer is checking:** Whether you can make a good decision under time limits using proxies and reversible steps.
**Say this in the interview:** "I would not wait; I would pick early leading indicators that history shows predict three-month retention, roll out in stages with a holdout, and keep the decision reversible."
**Clarify first:** How costly is a wrong rollout (reversible or not)? Is there historical data linking early behaviour to 3-month retention? How big can the test be?
**Structure:**
1. Find proxies: from past cohorts, which week-1 or week-2 behaviours (second-week activity, repeat orders, key action count) best predict 3-month retention? Check the predictive link on old data.
2. Run a randomised test with a holdout. Compare proxies at two weeks; add guardrails (crashes, complaints, uninstalls).
3. Decide by the proxy and confidence: clear positive and no guardrail harm: roll out in stages (for example 10%, 50%) keeping a 5% holdout; clear negative: stop; unclear: extend or stay small.
4. Keep measuring retention in the holdout and revisit at three months; roll back if the real number disappoints.
**Recommendation:** Say plainly that the evidence is indirect, state the assumption that the proxy carries over, and write the roll-back rule before launch.
**Likely follow-ups:** 1) *What if no proxy exists?* Use qualitative signals and a small staged release. 2) *What if the feature is irreversible?* Be more cautious and demand stronger evidence.
**Common mistakes / traps:** Using a vanity proxy (clicks); declaring victory from a novelty bump; no holdout.

### Q61 ⭐⭐ 🔴 Define the metrics tree for a quick commerce app and show how you would use it to locate why weekly orders per active user fell.
**Asked at:** commonly asked (no company-specific report found); no verified quick-commerce product-case report found, so this is built from general practice.
**What the interviewer is checking:** Whether you can break one metric into measurable parts that multiply or add, and then use numbers to point at the weak branch.
**Say this in the interview:** "Weekly orders per active user = sessions per user x session conversion. Then I break conversion into the funnel and look at where the drop sits."
**Clarify first:** Is the drop real? Which cities, since when? How is an active user defined?
**Structure (metrics tree):**
- Orders per active user = sessions per active user x orders per session (conversion).
- Sessions per user: driven by habit (notifications, reminders) and reasons to open.
- Conversion = search or browse success x add-to-cart x checkout completion x payment success.
- Supply side that hits conversion: item availability (out-of-stock rate), delivery time promised, delivery fee, serviceability.
- Order value separate: items per order, price level.
**Worked mini-example (made up):** Before: 5.0 sessions x 40% = 2.0 orders per user. After: 4.8 sessions x 37.5% = 1.8. In log terms: sessions -4.1%, conversion -6.5%, total -10.5%, so about 39% of the fall comes from fewer sessions and 61% from conversion. So I go down the conversion branch first.
**What I would check, in order:** definition and logging; by city and dark store (a local stock or rider shortage); by funnel step; availability and delivery time at the moment of session; new vs old users; price, fee and offers.
**If the data shows...:** Conversion down mainly at search or product (items shown unavailable): availability problem. Down at payment: payment issue. Sessions down: engagement, notification or competition.
**Recommendation:** Fix the branch carrying most of the fall, then monitor the tree weekly.
**Likely follow-ups:** 1) *Why use log shares?* They add exactly for a product of two factors. 2) *North star?* Weekly orders per active user, with delivery time as a guardrail.
**Common mistakes / traps:** Branches that overlap; stopping at "orders fell"; no numeric split.

### Q62 ⭐ 🟡 A payroll-query chatbot handled 20,000 employee queries: 12,000 were closed by the bot without a human, and 3,000 of those reopened as human tickets within 48 hours. Compute the raw and true deflection rates and say which you would report.
**Asked at:** commonly asked (no company-specific report found); an HR gap-fill item, not a reported question.
**What the interviewer is checking:** Whether you correct a headline success rate for repeats.
**Say this in the interview:** "Raw deflection is 60%, but 3,000 of them came back to a human, so true deflection is 45%. I would report the true figure and show the raw one beside it."
**Definition in plain words:** Deflection rate = queries resolved without a human divided by all queries. "True" deflection removes bot closures that reopened with a human within a set window.
**Worked answer:**
1. Raw = 12,000 / 20,000 = 60%.
2. True bot-resolved = 12,000 - 3,000 = 9,000.
3. True = 9,000 / 20,000 = 45%.
4. Reopen rate = 3,000 / 12,000 = 25%.
**Result:** Raw 60%, true 45%, one in four bot closures was not really solved.
**Check:** 8,000 queries went to humans at first (40%) plus 3,000 reopened = 11,000 human-handled, 55%; and 100% - 55% = 45%. Consistent.
**Caveats:** Users may give up without reopening (hidden failures), so add a thumbs-up or a "was this solved" rate; the 48-hour window is a choice; payroll queries near pay day have different mix; look at deflection by topic (salary slip, tax, reimbursement).
**Likely follow-ups:** 1) *Guardrail?* Satisfaction and escalation time. 2) *Which queries to automate first?* High volume, low complexity.
**Common mistakes / traps:** Reporting 60%; counting abandoned chats as resolved.

### Q63 ⭐ 🟡 A 50/50 A/B test shows 50,000 users in control and 48,500 in treatment. Is this a problem, and what do you do before reading the results?
**Asked at:** commonly asked (no company-specific report found); sample ratio mismatch is a gap-fill from standard experimentation practice.
**What the interviewer is checking:** Whether you know the sample ratio mismatch (SRM) check and refuse to read a broken test.
**Say this in the interview:** "Yes, it is a problem. With 98,500 users I expect 49,250 each; a gap this size is very unlikely by chance, so I would stop and find the cause before reading any result."
**Definition in plain words:** Sample ratio mismatch means the user split differs from the planned split by more than chance. A chi-square test (compares observed counts with expected counts) checks it.
**Worked answer:**
1. Total = 98,500; expected each = 49,250.
2. Difference = 750 per arm; chi-square = 750^2 / 49,250 + 750^2 / 49,250 = 22.84.
3. p-value about 0.000002 (one degree of freedom), far below the usual 0.001 alarm level.
4. Ratio treatment/control = 0.97, a 3% shortfall.
**Result:** The split is not random; the test is not trustworthy as is.
**Check:** Treatment share = 48,500 / 98,500 = 49.2%, not 50%.
**What to do:** Look for the cause: crashes or slow load in treatment that lose users before logging, a redirect that drops users, bot filtering applied unevenly, wrong assignment code or caching, treatment users logged differently. Fix and rerun; do not "adjust" the numbers.
**Caveats:** A tiny mismatch with huge samples can also be flagged; the cause matters more than the p-value.
**Likely follow-ups:** 1) *Can you just analyse the people you have?* No, the missing users are probably not random. 2) *When to check?* Before every readout.
**Common mistakes / traps:** Reading the lift anyway; blaming "random noise".

### Q64 ⭐ 🟡 A feature costs Rs 30 lakh to build and earns Rs 12 contribution per incremental order. How many incremental orders pay back the build cost, and how would you judge whether to build it?
**Asked at:** commonly asked (no company-specific report found); a build break-even gap-fill.
**What the interviewer is checking:** Whether you compute break-even and then test whether it is realistic.
**Say this in the interview:** "Rs 30 lakh divided by Rs 12 is 250,000 incremental orders. Then I ask how long it would take to reach that at a believable incremental volume."
**Worked answer:**
1. Cost = Rs 30 lakh = Rs 3,000,000.
2. Break-even orders = 3,000,000 / 12 = 250,000 incremental orders.
3. Time to payback at an assumed volume (made up): 25,000 incremental orders a month gives 10 months; 40,000 a month gives 6.25 months; 10,000 a month gives 25 months.
**Result:** 250,000 incremental orders.
**Check:** 250,000 x Rs 12 = Rs 30 lakh.
**How I would judge:** estimate incremental (not total) orders from a pilot or a similar past feature; add running costs (maintenance, support, cloud) and opportunity cost of the team; use a payback target (for example under 12 months) and a range of outcomes (low, base, high); consider side benefits (retention) and risks (cannibalisation).
**Caveats:** Contribution per incremental order may differ from the average; the effect may fade; ignoring discounting is fine for a short payback.
**Likely follow-ups:** 1) *What if incremental volume is uncertain?* Build a minimum version, test, then scale. 2) *Compare with other projects?* Rank by payback or return on effort.
**Common mistakes / traps:** Using total orders instead of incremental; ignoring running costs.

### Q65 ⭐ 🟡 Targets such as "delivery time promised" are gamed by showing longer promised times. How do you design metrics that resist gaming for a feature launch?
**Asked at:** commonly asked (no company-specific report found); a gap-fill on metric gaming.
**What the interviewer is checking:** Whether you know that one metric can be gamed and pair it with a counter-metric.
**Say this in the interview:** "I would pair every target with its opposite, measure the customer outcome rather than the proxy, and keep one metric the team cannot influence directly."
**Explain simply:**
- Goodhart's law: when a measure becomes a target, it stops being a good measure.
- The promised time is easy to game by quoting 45 minutes and delivering in 40. The honest outcome is delivery versus the promise, and the customer's choice.
- Mini example (made up): promised time rose from 25 to 35 minutes and on-time delivery improved from 80% to 95%, but orders fell 4%. A single "on-time %" target would have shown a win.
**Design rules:**
1. Pair: on-time rate with the promised time itself, and with conversion and order volume.
2. Measure outcomes: actual delivery time, repeat rate, complaints, ratings.
3. Use ratios and distributions (95th percentile) not only averages.
4. Keep a holdout and a second data source (for example rider GPS time).
5. Review metric definitions with someone outside the owning team; watch for sudden shifts at the target line.
**Practice step:** For one metric you know, write the cheapest way to game it and the counter-metric that would expose it.
**Likely follow-ups:** 1) *How do you spot gaming?* A good-looking number with worsening business results. 2) *Who owns the metric?* Preferably not only the team judged by it.
**Common mistakes / traps:** One metric per goal; rewarding the number without watching customers.

### Q66 ⭐ 🟡 A feature is shown to treatment users, but only 30% of eligible treatment users ever see it. Overall orders per user rise 0.6 percentage points in conversion. What is the implied effect on those who saw it, and what are the caveats?
**Asked at:** commonly asked (no company-specific report found); a gap-fill on intention-to-treat versus exposed effects.
**What the interviewer is checking:** Whether you scale the diluted effect by the exposure share and know what assumptions this needs.
**Say this in the interview:** "The 0.6 point is averaged over everyone assigned, including 70% who never saw it. If the effect is only on those who saw it, the effect on them is 0.6 / 0.30 = 2.0 percentage points."
**Definition in plain words:** The intention-to-treat effect is the effect of being assigned to the feature, whether or not the user saw it. Dividing by the exposure share gives the effect on those who saw it (the complier effect).
**Worked answer:**
1. Assigned effect = 0.6 percentage points.
2. Exposure share = 30% = 0.30.
3. Effect on those exposed = 0.6 / 0.30 = 2.0 percentage points.
**Result:** About +2.0 percentage points for exposed users.
**Check:** 30% x 2.0 = 0.6. Consistent.
**Caveats:** Needs two assumptions: unexposed users get no effect, and assignment affects outcomes only through seeing the feature. Exposed users are not random (they are more active), so do not compare "saw" against "did not see" directly; instead compare against the control users who would have seen it (log a counterfactual exposure in control). The rollout plan should rely on the diluted 0.6 if the exposure stays at 30%; raising exposure is the lever. The wording of "orders per user" and "conversion" in the question is mixed; I treat it as a conversion difference in percentage points.
**Likely follow-ups:** 1) *Which number do you report to leadership?* Both, labelled: 0.6 for the launch as it stands, 2.0 for the exposed. 2) *Why is exposure only 30%?* Placement, eligibility or a bug; investigate.
**Common mistakes / traps:** Comparing seen vs not-seen groups; reporting 2.0 as the company impact.

### Q67 ⭐ 🔴 A feature affects both buyers and sellers on a marketplace. Why can a user-level A/B test be misleading, and what alternatives would you use?
**Asked at:** commonly asked (no company-specific report found); marketplace interference is a differentiator topic, not a reported company question.
**What the interviewer is checking:** Whether you understand interference: users in the two arms share the same pool of sellers or buyers.
**Say this in the interview:** "Treatment and control users compete for the same stock and riders, so what happens to one group changes the other. The test result then differs from the true full-rollout effect, so I would randomise at a level that contains the interaction."
**Explain simply:**
- Interference: one user's treatment changes another user's outcome. If treated buyers snap up limited inventory, control buyers get less.
- Mini example (made up): treatment buyers get a discount and order 10% more, taking stock from control buyers, whose orders fall 5%. The test reads about +15% difference, while a full rollout of the discount cannot create more stock, so the real total gain is much smaller.
- Both sides are affected: seller-side features (fee changes) change what buyers see too.
**Alternatives:**
1. Cluster randomisation: randomise whole cities, regions or seller groups.
2. Switchback tests: switch the feature on and off over time blocks in the same market (for example alternate hours or days), compare blocks.
3. Two-sided or budget-split designs: randomise buyers and sellers separately.
4. Geo experiments with difference-in-differences or synthetic control.
5. Measure marketplace-level outcomes (total orders, seller revenue, wait times), not only user-level.
**Likely follow-ups:** 1) *Cost of these designs?* Fewer units, so less power and longer tests. 2) *When is a user-level test fine?* If supply is plentiful and there is no sharing.
**Common mistakes / traps:** Trusting the user-level lift; forgetting seller-side outcomes.

### Q68 ⭐ 🔴 How would you design a long-term holdout to measure the cumulative effect of many small features, and what are its costs?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** Whether you know why individual test wins do not simply add up and how a holdout checks the sum.
**Say this in the interview:** "I keep a small random group of users on the old experience for months, compare them with everyone else, and the gap is the cumulative effect of all shipped features."
**Explain simply:**
- Many tests each show a small win, but wins can overlap, fade, or hurt long-term retention. A holdout measures the total.
- Design: randomly pick, say, 2% of users; freeze them on a fixed baseline version (with only bug and security fixes); assign at user level, keep it stable for 3 to 6 months; refresh periodically; track long-term metrics (retention, orders per user, revenue, complaints).
- Cost example (assumed): if 8% cumulative lift is real, a 2% holdout forgoes 0.02 x 0.08 = 0.16% of revenue. With 10 million users, 2% is 200,000 users, enough for a clear read.
**Costs:** some revenue forgone and a poorer experience for the holdout group; engineering effort to maintain the old version (code branches, feature flags); stale baseline (the old product ages, so the gap includes platform change); harder sharing of data pipelines; ethical and fairness checks on withholding security or compliance changes.
**Practice step:** Write the exact list of features the holdout may and may not exclude.
**Likely follow-ups:** 1) *How big?* Large enough to detect the expected cumulative lift, often 1 to 5%. 2) *How long?* Until the effect stabilises.
**Common mistakes / traps:** Holdout too small; letting changes leak in; summing individual lifts instead.

### Q69 ⭐ 🔴 How would you measure success of an AI assistant added to a shopping app, including quality, cost and guardrails?
**Asked at:** commonly asked (no company-specific report found); no reported question found, and the Part sources note only prep-site feature-metric items (unverified).
**What the interviewer is checking:** Whether you cover business value, answer quality, cost and safety, not just usage.
**Say this in the interview:** "I would define success as more purchases or easier shopping at an acceptable cost per use, and make accuracy and safety hard guardrails."
**Structure:**
- Goal: help users find and decide faster.
- Primary (impact): conversion or orders per user for assistant users vs a randomised holdout; time to purchase.
- Adoption and engagement: share of users trying it, repeat use, conversation completion.
- Quality: helpfulness ratings, human review of sampled answers (a rubric for correctness, relevance), resolution without escalation, wrong or invented product claims (hallucination rate), rate of "no answer".
- Cost: cost per conversation (model and infrastructure), cost per incremental order; compare with the contribution per order.
- Guardrails: latency, safety incidents, wrong price or stock statements, bias or unsafe advice, complaint and return rates, privacy.
**What I would check, in order:** a randomised test with holdout; sample reviews weekly; split by user type and query type; track cost per incremental order.
**If the data shows...:** Heavy use but no lift in orders: the assistant entertains but does not help. Lift but costs exceed contribution: reduce cost (smaller model, caching) or limit use cases.
**Recommendation:** Launch narrow, with human review and a kill switch; scale when quality and economics hold.
**Likely follow-ups:** 1) *Who does the quality labelling?* Trained reviewers on a rubric, plus user feedback. 2) *Selection bias?* Users who choose the assistant differ, so use randomisation.
**Common mistakes / traps:** Measuring only chats started; ignoring cost per answer; no accuracy review.

### Q70 ⭐ 🔴 A new feature increases orders but cancellations and refunds also rise. Design the analysis to decide if net contribution improved.
**Asked at:** commonly asked (no company-specific report found); a gap-fill on net contribution analysis.
**What the interviewer is checking:** Whether you move from gross orders to net contribution per user and include every cost line.
**Say this in the interview:** "I would compare contribution per user after cancellations and refunds, treatment against control. On the made-up example below the net gain is only about 0.6%, even though orders rose 8%."
**Clarify first:** Is it a randomised test? What is the contribution per delivered order, cost of a cancellation, cost of a refund?
**Structure:** Net contribution = delivered clean orders x contribution per order - cancelled orders x cancellation cost - refunded orders x refund cost.
**Numeric work (all inputs assumed, made up; per week):**
- Contribution Rs 45 per delivered, non-refunded order; cancellation costs Rs 15 (wasted prep and rider); refund costs Rs 120.
- Control: 100,000 orders placed; 4% cancelled; 2% of delivered refunded. Delivered 96,000, refunded 1,920, clean 94,080. Contribution 94,080 x 45 = Rs 42.34 lakh, minus cancellations 4,000 x 15 = Rs 0.60 lakh, minus refunds 1,920 x 120 = Rs 2.30 lakh. Net Rs 39.43 lakh.
- Treatment: 108,000 placed (+8%); 6% cancelled; 3% refunded. Delivered 101,520, refunded 3,046, clean 98,474. Contribution Rs 44.31 lakh, cancellations 6,480 x 15 = Rs 0.97 lakh, refunds 3,046 x 120 = Rs 3.65 lakh. Net Rs 39.69 lakh.
- Difference: +Rs 0.25 lakh per week, +0.6%.
**What I would check, in order:** gross orders, cancel and refund rates by reason and by segment; contribution per user by arm; repeat rate (refund-heavy users may churn); who bears the refund (restaurant vs platform).
**If the data shows...:** Net positive with stable repeat: ship. Net near zero (as here): fix the source of cancellations and refunds (for example wrong ETA or item mismatch) then retest. Negative: roll back.
**Recommendation:** Use confidence intervals on net contribution per user, not on orders alone; set the decision rule before launch.
**Likely follow-ups:** 1) *Why not just orders?* Orders are revenue-like, and these extra orders are lower quality. 2) *Sensitivity?* Here a refund rate of 3.5% instead of 3% would push net below control.
**Common mistakes / traps:** Counting placed orders as value; ignoring the cost of cancellations; missing later churn.

### Q71 ⭐ 🔴 UPI payments in an app dropped 50% week on week. Walk through your investigation order, hypotheses and the data each one needs.
**Asked at:** prep sites (PracHub) list a "50% weekly drop in Paytm payment transactions" case and Agoda wallet/UPI failure case (community question banks, unverified); not confirmed as asked at any company.
**What the interviewer is checking:** Whether you stay calm, check the data first, decompose the metric, and rank hypotheses by speed and likelihood.
**Say this in the interview:** "A 50% fall is too big for normal behaviour, so I would first check data and outages, then break it into users who start UPI, attempts, and success rate, and cut by bank and app version."
**Clarify first:** UPI payments counted as successful transactions or attempts? Sudden or gradual? Only our app or industry-wide? Any release, partner or regulatory change?
**Structure:** UPI successes = users reaching payment x share choosing UPI x attempts per user x success rate.
**What I would check, in order:**
1. Measurement: logging, dashboards, delayed data or a changed definition (data: raw logs, server transactions).
2. Timing: sharp drop at a timestamp suggests an outage or release; gradual fall suggests a mix or demand cause.
3. Success rate and error codes: attempts vs successes, by bank, by UPI handle (payer app) and PSP (payment service provider); a single bank or gateway failure shows as a concentrated drop.
4. Top of funnel: did fewer users reach the payment step, or fewer choose UPI (a UI change hiding UPI, a default changed)?
5. App version and device: crash or broken intent (the call that opens the UPI app) on a new version or OS.
6. Partners and external: payment gateway, NPCI (the UPI network operator) or bank downtime, a regulatory limit change, a rival offer.
7. Fraud controls: a risk rule blocking many legitimate payments.
**If the data shows...:** Attempts steady, success rate down by one bank: bank or gateway issue, reroute or contact partner. Attempts down: funnel or UI issue. Whole drop after a release: roll back.
**Recommendation:** Restore service first (rollback, reroute, partner escalation), communicate to support and business, then write a root-cause review with monitoring alerts on success rate by bank.
**Likely follow-ups:** 1) *Quantify the impact?* Lost orders = missing UPI transactions x share that would not switch to another method. 2) *How do you stop recurrence?* Real-time alerts on success rate and error spikes.
**Common mistakes / traps:** Theorising about user behaviour before checking logs and outages; looking only at the total, not by bank or version.


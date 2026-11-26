# Chapter 35 Answer Key: Mixed Case Studies (Commerce plus Data)

All numbers below were recomputed by code (set counts, brute-force over the 720 task orders for Case 3, rates, means and medians, the 16-row truth table, and the fraud table). All data are invented and illustrative.

---

## Case 1: The free-shipping rule

**1a.** Only **O3** breaks the rule. The rule says: if total is 50 or more, shipping is free. O3 has total 50 (so the condition holds) but shipping was not free. O1 and O5 satisfy the rule (condition true, result true).

**1b.** **No.** O2 has total 48, so A ("50 or more") is false. An if-then rule only makes a promise when A is true. When A is false, the rule is silent (it is "vacuously true"), whatever happens to shipping. The promo code explains the free shipping.

**1c.** Counts by row:

| A (total 50 or more) | B (free shipping) | Orders | Count | Rule A implies B |
|---|---|---|---|---|
| True | True | O1, O5 | 2 | True |
| True | False | O3 | 1 | **False** |
| False | True | O2 | 1 | True |
| False | False | O4, O6 | 2 | True |

Total 6. The rule can only be false in the row "A true, B false". Only O3 is there.

**1d.** "Every free-shipping order is 50 or more" is "if B then A", the **converse**. The table does not support it: O2 is free shipping with total 48. A converse is not guaranteed by the original rule.

**1e.** Contrapositive of "if total is 50 or more then shipping is free": "if shipping is not free, then the total is below 50." Check: the non-free orders are O3 (50), O4 (35), O6 (49.9). O4 and O6 satisfy it; O3 breaks it, which matches 1a (a rule and its contrapositive stand or fall together).

---

## Case 2: Where do our shoppers buy?

Inclusion-exclusion: union = 120 + 90 + 70 - 40 - 30 - 25 + 10 = **195**.

**2a.** At least one channel: **195**. None: 200 - 195 = **5**.

**2b.** Exactly one channel: app only = 120 - 40 - 30 + 10 = 60; web only = 90 - 40 - 25 + 10 = 35; store only = 70 - 30 - 25 + 10 = 25; total **120**. Exactly two (pairs without the triple): (40 - 10) + (30 - 10) + (25 - 10) = 30 + 20 + 15 = **65**. Check: 120 + 65 + 10 (all three) + 5 (none) = 200.

**2c.** App users who also use the web: 40 out of 120 = **33.3%**. "Mostly" would need more than 50%. **Not supported.**

**2d.** **False.** A store customer who uses neither app nor website is a counterexample. Store-only customers number 25, so the "every" claim fails. (Check: 70 store users = 25 only + 20 with app only extra [30 - 10] + 15 with web only extra [25 - 10] + 10 all three = 70.)

**2e.** App or website: 120 + 90 - 40 = **170** customers = 85% of 200. Not "almost every": 30 customers (15%) use neither. Also, the survey sample may not represent all customers (a limit worth stating).

---

## Case 3: The packing-line order

**3a.** R, C, Q, P, L, D: R before C and P (yes), P before L (yes), C before Q (yes), L and Q before D (yes). **Allowed.** R, P, C, L, D, Q: D is before Q, but the rule needs Q before D. **Not allowed.**

**3b.** Brute force over all 720 orderings finds exactly **6** valid ones. By reasoning: R must be first (it comes before C and P, and C and P lead to everything else) and D must be last. The middle four tasks form two chains, C then Q and P then L. Ways to interleave two chains of length 2: 4 choose 2 = 6. The six are RCPLQD, RCPQLD, RCQPLD, RPCLQD, RPCQLD, RPLCQD.

**3c.** Longest chains (critical path): R(2) + P(3) + L(1) + D(2) = **8 hours**. The other chain R(2) + C(1) + Q(1) + D(2) = 6 hours is shorter. The whole job cannot finish before 8 hours.

**3d.** One worker does all tasks: 2 + 1 + 3 + 1 + 1 + 2 = 10 hours. Starting at 07:00 the work ends at 17:00, which is after 14:00. The statement is **false**. (Even with six workers on the parallel plan the shortest time is 8 hours, ending 15:00, so 14:00 would be missed too.)

**3e.** Slack: Count (C) and Quality check (Q) each have 2 hours of slack (they finish at hours 3 and 4 but are needed only by hour 6). The critical tasks R, P, L, D have zero slack.

---

## Case 4: The soaring revenue chart

**4a.** (102,500 / 98,000 - 1) = 4,500 / 98,000 = **4.6%** (4.59%).

**4b.** Bar heights are 1,000 (Jan), 2,500, 4,000, 5,500 (Apr). Ratio 5,500 / 1,000 = **5.5**. The April bar looks 5.5 times as tall as January, suggesting growth of 450%, while the real growth is 4.6%.

**4c.** "...only if the vertical axis starts at 0 (the baseline is zero)." With a cut axis the bar heights are proportional to value minus the cut, not to the value.

**4d.** The rule is a **straight-line extrapolation**: revenue grows by 1,500 a month, so December = 98,000 + 11 x 1,500 = 114,500 (the claim is arithmetic-correct for a straight line). Cautions: (1) only four data points, too few to know a trend; (2) seasonality, promotions or stock limits can bend it; (3) the future may not follow the past. Any two of these.

**4e.** Title: "Revenue up 4.6% from January to April" (or "Revenue rose from 98,000 to 102,500"). Axis: start at 0 for bars, or draw a line chart and label the axis range clearly with the growth percentage shown.

---

## Case 5: Which campaign worked better?

**5a.** A: (20 + 30) / (50 + 450) = 50 / 500 = **10.0%**. B: (380 + 6) / (1,000 + 100) = 386 / 1,100 = **35.1%**. Overall, B looks far better.

**5b.** Returning: A = 20 / 50 = 40.0%, B = 380 / 1,000 = 38.0%. New: A = 30 / 450 = 6.7%, B = 6 / 100 = 6.0%. **A is better in both groups.**

**5c.** **True** (40.0 > 38.0 and 6.7 > 6.0).

**5d.** This is **Simpson's paradox**. Campaign A was sent mostly to new customers (450 of 500), who rarely buy; campaign B was sent mostly to returning customers (1,000 of 1,100), who buy often. The group mix, not the campaign, drives the overall gap. The overall rate is a weighted average, and the weights differ a lot.

**5e.** Compare like with like: A looks slightly better within each group, but the gaps are small (2 points and 0.7 points) and some groups are small (only 50 returning customers got A, and only 100 new customers got B). Limits: customers were not randomly assigned (someone chose who got which email, probably the returning customers for B), group sizes are small, and there may be other differences (timing, subject line). Recommend a randomized test within each customer group before declaring a winner.

---

## Case 6: The cart-discount algorithm

**6a.** Cart X: 40 (total 40), +35 = 75, +30 = 105 which is over 100, so subtract 10 to get 95 and set the flag; +20 = **115**. Cart Y: 60, then 100 (100 is not greater than 100, so no discount); final **100**.

**6b.** The test is "greater than 100", and exactly 100 fails it. Changing step 2 to "100 or greater" would give Y the discount (total 90). That is an **edge case**: the boundary value decides the outcome.

**6c.** Z: 120 (over 100, so 110 after discount, flag set), then -30 gives **80**. Z2: -30, then +120 gives 90, which is not over 100, so no discount; final **90**. Same prices, different totals.

**6d.** **No, order does not matter** for positive prices. Before the discount, the running total is just the sum of the prices so far, and it only grows. So the discount fires if and only if the full sum exceeds 100, and exactly 10 is taken once. Final total = sum - 10 if sum > 100, else sum. (Checked on X reordered 20, 30, 35, 40: 115 again.) With negative prices the running total can go down, and the discount depends on whether the running total ever passes 100, which depends on order (6c).

**6e.** Empty cart: total stays 0, no loop runs, output **0**. That is sensible, but a real checkout might also want to show "cart is empty" instead of a total of 0.

---

## Case 7: How many packers do we need?

**7a.** Boxes per week = 250,000 x 0.04 x 2 = 10,000 subscribers x 2 = **20,000**. Per day (5 days) = **4,000**. One packer per day = 30 x 6 = **180**.

**7b.** 4,000 / 180 = 22.2 packers. Round **up to 23**, because 22 packers cannot finish the day's boxes (22 x 180 = 3,960 < 4,000). Rounding up is the safe direction for capacity.

**7c.** At 3%: 15,000 boxes per week, 3,000 per day, 3,000 / 180 = 16.7, so **17**. At 5%: 25,000 per week, 5,000 per day, 5,000 / 180 = 27.8, so **28**. Range: about **17 to 28 packers**.

**7d.** 8 packers x 180 x 5 = 7,200 boxes per week. 7,200 / 20,000 = **36%**. Far from "plenty".

**7e.** The 4% subscribe share (it moves the answer the most, see 7c) and the 30 boxes per hour speed (it is a guess for a brand-new line, and a 20% error in it changes the headcount by about 20%). Also acceptable: the assumption that all demand is spread evenly over 5 days (peaks would need more people).

---

## Case 8: The review page

**8a.** (i) **False**: R3 is 5 stars and not verified. (ii) **True**: R5 is verified with 2 stars. (iii) **False**: R3 (5 stars) and R8 (3 stars) are unverified with more than 2 stars.

**8b.** Negation of "every 5-star review is verified": "**at least one** 5-star review is **not** verified" (R3).

**8c.** All: (5 + 5 + 5 + 4 + 2 + 1 + 5 + 3) / 8 = 30 / 8 = **3.75**. Verified (R1, R2, R4, R5, R7): (5 + 5 + 4 + 2 + 5) / 5 = 21 / 5 = **4.2**. Unverified (R3, R6, R8): (5 + 1 + 3) / 3 = 9 / 3 = **3.0**.

**8d.** 4.2 is the verified-only average. It is a true number but a selected one: the full page average is 3.75, and the unverified ones average 3.0. Also, it comes from only 5 reviews. Saying "rated 4.2 by customers" without "verified only" and without the count is misleading.

**8e.** **Self-selection (response) bias**: people with very strong feelings, good or bad, are more likely to post a review than people with a typical experience. Also possible: fake or incentivised reviews, and the small sample of 8.

---

## Case 9: The average customer spends 153

**9a.** Sum = 12 + 15 + 18 + 20 + 22 + 25 + 30 + 35 + 1,200 = 1,377. Mean = 1,377 / 9 = **153**. Sorted order: the 5th of 9 values is **22** (median).

**9b.** The **median (22)** describes a typical customer: eight of nine customers spent 35 or less. The mean is dragged up by the single 1,200 outlier (K9). Without K9: (1,377 - 1,200) / 8 = 177 / 8 = **22.1**, close to the median. (K9 might be a bulk buyer, a business account, or a data error; check before dropping it.)

**9c.** Eligible = ((M AND S) OR R) AND (NOT F).

**9d.** Brute force over 16 rows: **5** rows make the customer eligible. With F false (8 rows): R true gives 4 rows (any M, S), R false needs M and S both true, giving 1 row. 4 + 1 = 5. With F true, none of the 8 rows qualify.

**9e.** Flagged, referred, non-member: F true makes the whole rule false, so **not eligible**. Unflagged, non-member, spend 80, no referral: M is false so (M AND S) is false, R is false, so **not eligible** (spend alone is not enough).

---

## Case 10: The fraud flag

**10a.** Fraud: 100 orders; flagged 95% = **95**, not flagged **5**. Genuine: 9,900; flagged 5% = 495, not flagged = 9,405.

| | Flagged | Not flagged | Total |
|---|---|---|---|
| Fraud | 95 | 5 | 100 |
| Genuine | 495 | 9,405 | 9,900 |
| Total | 590 | 9,415 | 10,000 |

**10b.** 95 / 590 = **16.1%**. Only about 1 in 6 flagged orders is really fraud.

**10c.** The manager reverses the direction: "if fraud, then flagged (95% of the time)" is not the same as "if flagged, then fraud". This is the **converse error**, made worse by ignoring the **base rate** (only 1% of orders are fraud, so false flags from the large genuine pool outnumber true flags).

**10d.** 590 x 6 minutes = 3,540 minutes = **59 hours**.

**10e.** Genuine flagged = 2% of 9,900 = 198. Flagged total = 95 + 198 = 293. Share fraud = 95 / 293 = **32.4%**, about double (16.1% before). Review time falls to 293 x 6 / 60 = 29.3 hours. Limit: a lower false-flag rate may also change the catch rate in practice; the question assumes it stays 95%.

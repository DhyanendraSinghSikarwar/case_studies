# Book 7 — Guesstimates, Case Studies & Business Metrics | Part 6: Profitability, Pricing & Growth Cases 🟡🔴

**Target:** 70 questions | **Actual:** 76 questions
**Scope:** profitability diagnosis, unit economics and break-even, pricing and elasticity, and growth cases with inline numbers where a single checkable figure exists; Indian consumer, fintech, SaaS, edtech and BPO contexts.

### Q1 ⭐⭐⭐ 🟢 A client says 'our profit has fallen'. What framework do you use to structure a profitability case, and what do you ask first?
**Asked at:** commonly asked (no company-specific report found); prep sites and an internal compilation list profitability cases at Mu Sigma, Fractal, Flipkart and Meesho (anecdotal, unverified).
**What the interviewer is checking:** Whether you break "profit fell" into a clean tree (revenue and cost) instead of guessing.
**Say this in the interview:** "Profit is revenue minus cost, so I will first confirm what fell and by how much, then split revenue into price times volume and cost into fixed and variable, and find the branch that moved."

**Clarify first:**
- What exactly fell: profit in rupees or profit margin (profit as a percentage of revenue)? Over what period, compared with what (last year, last quarter, plan)?
- Is it the whole company or one product, city or channel? Sudden drop or slow slide?
- Did anything change: price, new competitor, new cost, new product, a one-off item?

**Structure:**
- Profit = Revenue - Cost
  - Revenue = Price x Volume (split by product, customer type, region, channel)
    - Volume: customers x purchases per customer
    - Price: list price, discounts, mix of products sold
  - Cost = Fixed cost + Variable cost
    - Variable: materials, delivery, commission, payment fees (move with each sale)
    - Fixed: rent, salaries, tech (do not move with sales in the short run)
- External factors: competitor, season, regulation, input prices.

**What I would check, in order:**
1. Revenue trend versus cost trend by month (is the gap from revenue falling or cost rising?).
2. If revenue: split price versus volume, then by product and region (Excel pivot or SQL GROUP BY).
3. If cost: each line as a percentage of revenue, this period versus last.
4. Mix shift: did sales move to low-margin products?

**If the data shows...:** Revenue flat and cost up means a cost problem (find the line). Volume down with price steady means a demand or competition problem. Revenue up but margin down often means discounts or mix.

**Recommendation:** Name the one or two biggest drivers, size each in rupees, propose a fix per driver, and track monthly profit margin to confirm recovery.

**Likely follow-ups:** 1) *Why ask profit versus margin first?* Rupee profit can fall simply because revenue is smaller, while margin tells you about efficiency. 2) *What if only one product lost money?* Look at its contribution margin before deciding to drop it.
**Common mistakes / traps:** Jumping to solutions before locating the branch; only looking at revenue; not asking whether the fall is one-off (a legal charge, a write-off).

### Q2 ⭐⭐⭐ 🟢 What is contribution margin, and why is it more useful than net profit when deciding whether to keep selling a product?
**Asked at:** commonly asked (no company-specific report found); break-even and contribution margin are standard in prep-site profitability guides (unverified).
**What the interviewer is checking:** Whether you separate costs that vanish if the product stops from costs that stay anyway.
**Say this in the interview:** "Contribution margin is price minus variable cost per unit. If it is positive, each sale helps pay the fixed bills, so dropping the product would usually make profit worse."

**Explain simply:**
- Contribution per unit = selling price - variable cost per unit (costs that exist only because you sold that unit: ingredients, delivery, commission).
- Contribution margin % = contribution / price.
- Net profit also subtracts shared fixed costs (rent, head-office salaries) that are allocated to the product by a formula. If you drop the product, those costs usually remain and get spread over fewer products.
- Mini example: a thali sells at Rs 200, variable cost Rs 120, so contribution is Rs 80 (40%). Suppose the accounts allocate Rs 90 of rent and salaries per thali: net profit shows -Rs 10 per thali. Dropping it would lose Rs 80 per thali of money that was helping to pay the Rs 90 that stays. The right test is contribution, not net profit.
- Exception: if dropping the product genuinely avoids fixed costs (closing a store, ending a lease), include those avoided costs.

**Practice step:** Take any product you know, list three costs and mark each "disappears if we stop" or "stays anyway".
**Likely follow-ups:** 1) *When is a negative contribution acceptable?* Only briefly, if it brings customers who are profitable later (state the evidence). 2) *Contribution versus gross margin?* Gross margin subtracts only cost of goods; contribution subtracts all variable costs.
**Common mistakes / traps:** Judging a product by allocated net profit; treating a staff salary as variable when it is fixed; forgetting delivery or payment fees are variable.

### Q3 ⭐⭐⭐ 🟢 What is break-even, and how do you compute the break-even quantity for a business with fixed and variable costs?
**Asked at:** commonly asked (no company-specific report found); break-even is a standard topic in consulting prep sites (unverified).
**What the interviewer is checking:** Whether you know the formula and can explain it in words.
**Say this in the interview:** "Break-even is the volume where profit is exactly zero. It equals fixed costs divided by contribution per unit."

**Explain simply:**
- Profit = (price - variable cost) x quantity - fixed cost. Set profit to zero.
- Break-even quantity = fixed cost / (price - variable cost). In symbols: Q = F / (P - V).
- Why it works: each sale contributes (P - V) towards the fixed bills. You need enough sales to cover all of them.
- Mini example: fixed cost Rs 1,00,000 a month, price Rs 50, variable cost Rs 30, contribution Rs 20. Q = 1,00,000 / 20 = 5,000 units. Break-even revenue = 5,000 x 50 = Rs 2,50,000.
- Margin of safety: how far actual sales are above break-even (sales of 6,000 are 1,000 units above break-even: 20% above break-even, or 16.7% of actual sales).

**Practice step:** Compute break-even for a tea stall with your own rent and cup price.
**Likely follow-ups:** 1) *What if you want a target profit?* Q = (F + target profit) / (P - V). 2) *What if price falls?* Contribution shrinks, so break-even quantity rises.
**Common mistakes / traps:** Dividing by price instead of contribution; mixing monthly fixed cost with daily volume; assuming variable cost per unit stays constant at very high volume.

### Q4 ⭐⭐⭐ 🟢 How do you structure the case 'how can we grow revenue by 20% in the next year'?
**Asked at:** commonly asked (no company-specific report found); growth cases are reported in prep material for Mu Sigma and Fractal rounds (unverified).
**What the interviewer is checking:** Whether you can organise growth levers and size them against the 20% target.
**Say this in the interview:** "I will split revenue into customers times spend per customer, list levers for each, size them, and pick two or three that together deliver 20%."

**Explain simply:**
- Clarify first: which company and segment, current revenue, current growth trend, budget and constraints, is the goal absolute rupees or share?
- Revenue = customers x orders per customer x average order value.
- Levers: (1) more new customers (new cities, new channels, marketing); (2) keep existing ones longer (lower churn, meaning fewer customers leaving each month); (3) more orders per customer (loyalty, reminders); (4) higher order value (upsell, bundles, price); (5) new products or segments; (6) buying growth from outside (partnership, acquisition).
- Mini example: revenue Rs 100 crore, target Rs 20 crore more. New customers +8, retention +4, order value +5, new product +3 = Rs 20 crore. Each lever gets a cost and a risk.
- Prioritise by size, ease, speed and cost, then state two or three.

**Practice step:** Pick an app you use and write one lever per branch with a rough rupee size.
**Likely follow-ups:** 1) *Where do you start?* With the biggest, most controllable lever, usually existing customers. 2) *How do you know it is achievable?* Compare with past growth and market growth.
**Common mistakes / traps:** A random list of ideas; ignoring cost of each lever; not checking if the 20% is realistic.

### Q5 ⭐⭐⭐ 🟢 What are the main unit-economics line items for one food delivery order, and which are fixed and which variable per order?
**Asked at:** commonly asked (no company-specific report found); a B-school casebook covers per-order food delivery profitability and prep sites report Swiggy business cases (unverified).
**What the interviewer is checking:** Whether you can list per-order revenue and cost and separate variable from fixed.
**Say this in the interview:** "I will go from order value to commission and fees on the revenue side, then rider, discounts, payment and support on the cost side, and leave fixed overheads outside the per-order number."

**Explain simply:**
- Unit economics means the profit or loss on one unit, here one order.
- Revenue per order: commission from the restaurant (a % of order value), delivery fee from the customer, platform or packaging fee, advertising income from restaurants (spread per order).
- Variable per order: rider payout, platform-funded discounts, payment gateway fee, customer support cost, refunds and compensation.
- Fixed (do not change with one more order): tech team, head-office staff, brand marketing, city offices. Some costs are semi-fixed (rider incentives, support team).
- Contribution per order = revenue per order - variable costs per order. Fixed costs are covered by total contribution across all orders.
- Why it matters: if contribution per order is negative, more orders mean bigger losses.

**Practice step:** Order one meal on any app and write each line from the bill and your guess of what the platform pays.
**Likely follow-ups:** 1) *Is rider cost really variable?* Mostly yes per order, but fixed minimum payouts exist. 2) *Which lever is biggest?* Usually order value, discounts and rider cost per order.
**Common mistakes / traps:** Including head-office rent in per-order cost; counting GMV (food value) as revenue; forgetting platform-funded discounts.

### Q6 ⭐⭐⭐ 🟢 A cloud kitchen sells a thali at Rs 200 with variable cost of Rs 120 per thali and fixed costs of Rs 3,00,000 per month. How many thalis must it sell per month to break even?
Data: price Rs 200; variable cost Rs 120 per thali; fixed cost Rs 3,00,000 per month.
**Asked at:** commonly asked (no company-specific report found); break-even is a standard prep-site topic (unverified).
**What the interviewer is checking:** Correct use of contribution per unit.
**Say this in the interview:** "Contribution is 200 minus 120, Rs 80 per thali. Fixed cost 3,00,000 divided by 80 gives 3,750 thalis a month."

**Definition in plain words:** Break-even quantity = fixed cost divided by contribution per unit (price minus variable cost). It is the sales volume where profit is zero.
**Worked answer:**
1. Contribution per thali = 200 - 120 = Rs 80 (40% of price).
2. Break-even quantity = 3,00,000 / 80 = 3,750 thalis a month.
3. Per day (30 days) = 125 thalis. Break-even revenue = 3,750 x 200 = Rs 7,50,000.
**Result:** 3,750 thalis per month (about 125 per day), revenue Rs 7.5 lakh.
**Check:** 3,750 x 80 = 3,00,000, exactly the fixed cost, so profit is zero. At 4,000 thalis profit = 4,000 x 80 - 3,00,000 = Rs 20,000.
**Caveats:** Assumes a constant price and variable cost; real kitchens have discounts and wastage. Add a margin of safety above break-even.
**Likely follow-ups:** 1) *Target profit of Rs 60,000?* (3,00,000 + 60,000) / 80 = 4,500 thalis. 2) *If variable cost rises to Rs 130?* Contribution Rs 70, break-even 4,286 thalis (rounded up).
**Common mistakes / traps:** Dividing by price (1,500); forgetting to round up to whole units; mixing monthly and daily numbers.

### Q7 ⭐⭐⭐ 🟢 How do you decide whether a price increase is a good idea, and what data do you ask for before deciding?
**Asked at:** commonly asked (no company-specific report found); pricing cases appear in prep-site guides, and a Tiger Analytics pricing question page exists (single page, unverified).
**What the interviewer is checking:** Whether you compare extra margin per sale with sales lost, and look at customers and competitors.
**Say this in the interview:** "A price rise helps if the extra margin on the customers who stay outweighs the contribution lost from those who leave. I will ask for sales, margins, demand sensitivity and competitor prices."

**Clarify first:** What is the objective (profit, share, cash)? Which product and customers? Is the rise one-off or recurring? Are there contracts?
**Structure:**
- Impact on profit: new contribution (new price x remaining volume) versus old contribution.
- Customer response: how many leave or buy less (elasticity, meaning how much demand falls when price rises, or a test).
- Competitive response: do rivals follow, and are there close substitutes?
- Brand and strategic effects: loyalty, perceived value, long-term customers.
**What I would check, in order:**
1. Current price, volume, variable cost, contribution (price minus variable cost per unit; SQL or Excel).
2. Past price changes and what happened to volume.
3. Segments: who is price-sensitive (new versus loyal, city, plan).
4. Competitor prices; customer survey or a small A/B price test.
**If the data shows...:** The volume loss we expect is smaller than the break-even volume loss means go; a larger expected loss means do not raise, or raise only for insensitive segments.
**Numeric work:** Price 100, variable cost 60, contribution 40. A 10% rise gives contribution 50. Break-even loss of volume = 10/50 = 20%. If volume is likely to fall only 8%, raise it.
**Recommendation:** Test on a segment first, track churn and profit per customer, roll out gradually.
**Likely follow-ups:** 1) *What if competitors don't follow?* Expect bigger losses. 2) *Is a price rise ever bad even if profit goes up?* Yes if it damages long-term customers.
**Common mistakes / traps:** Only looking at revenue; ignoring variable cost; assuming no customers leave.

### Q8 ⭐⭐⭐ 🟢 What is the difference between gross margin, contribution margin, EBITDA and net profit, and which one do you use for a store-level decision?
**Asked at:** commonly asked (no company-specific report found); standard finance vocabulary in prep guides (unverified).
**What the interviewer is checking:** Whether you know what each measure includes and pick the right one for the decision.
**Say this in the interview:** "They are profit measures at different depths. For a store I use store-level contribution, since it shows what the store adds after the costs that depend on it."

**Explain simply:**
- Gross margin = revenue - cost of goods sold (direct cost of the product), shown as a %.
- Contribution margin = revenue - all variable costs (goods, delivery, commission, payment fees).
- EBITDA = earnings before interest, tax, depreciation and amortisation (depreciation is the yearly write-off of equipment); it includes fixed operating costs like rent and salaries but ignores financing and accounting write-offs.
- Net profit = what is left after everything, including depreciation, interest and tax.
- Mini example: revenue 100; goods 60 (gross margin 40); other variable 10 (contribution 30); fixed operating 20 (EBITDA 10); depreciation and interest 4; tax 2; net profit 4.
- Store-level decision (keep, open, close): use store contribution, then store EBITDA after directly attributable fixed costs (store rent, staff). Do not use company net profit, which includes head-office costs and interest that stay if the store closes.

**Practice step:** Rebuild the example with your own numbers and say which costs vanish if you close the store.
**Likely follow-ups:** 1) *Is high EBITDA always good?* No, if heavy capital spending is needed. 2) *Why is gross margin not enough?* It ignores delivery and fees.
**Common mistakes / traps:** Using net profit for a keep-or-close call; mixing gross margin with contribution; including allocated head-office cost.

### Q9 ⭐⭐⭐ 🟡 For one food delivery order, calculate the contribution per order from the data below.
Data per order: order value Rs 400; platform commission 22% of order value; delivery fee collected from the customer Rs 30; rider payout Rs 55; platform-funded discount Rs 40; payment and support cost Rs 10 in total.
**Asked at:** commonly asked (no company-specific report found); a B-school casebook covers food delivery per-order profitability (unverified).
**What the interviewer is checking:** Whether you count only what the platform earns, not the food value.
**Say this in the interview:** "The platform earns commission 88 plus delivery fee 30, Rs 118, and pays out 105, so contribution is Rs 13 per order."

**Definition in plain words:** Contribution per order = money the platform earns on the order minus the variable costs of serving it.
**Worked answer:**
1. Commission = 22% x 400 = Rs 88.
2. Platform revenue = 88 + 30 (delivery fee) = Rs 118.
3. Variable costs = 55 (rider) + 40 (discount) + 10 (payment and support) = Rs 105.
4. Contribution = 118 - 105 = Rs 13 per order (3.3% of order value).
**Result:** Rs 13 per order.
**Check:** Without the discount, contribution would be Rs 53. The discount takes away about three quarters of it.
**Caveats:** The order value of Rs 400 is the restaurant's food sale, not platform revenue. Taxes and packaging fees are ignored. If the discount is restaurant-funded, it should not be a platform cost.
**Likely follow-ups:** 1) *Orders a day to cover Rs 1,30,000 fixed cost?* 1,30,000 / 13 = 10,000 orders. 2) *Cut the discount to Rs 20?* Contribution Rs 33.
**Common mistakes / traps:** Treating Rs 400 as revenue; forgetting the delivery fee is income; subtracting commission as a cost.

### Q10 ⭐⭐⭐ 🟡 A subscription app raises its monthly price from Rs 500 to Rs 550. Is the increase worth it, and what is the largest fall in subscribers it can absorb before profit drops?
Data: 2,000 subscribers today; variable cost Rs 200 per subscriber per month; fixed cost is unchanged by the decision. After the increase, 8% of subscribers leave.
**Asked at:** commonly asked (no company-specific report found); price-versus-volume trade-off is a standard prep-site pricing item (unverified).
**What the interviewer is checking:** Whether you compare contribution before and after, not revenue only.
**Say this in the interview:** "Contribution goes from 6,00,000 to 6,44,000 a month, so it is worth it; the break-even loss is 14.3% of subscribers."

**Definition in plain words:** Contribution = subscribers x (price - variable cost). Break-even fall = the subscriber loss where new contribution equals old.
**Worked answer:**
1. Today: contribution per subscriber 500 - 200 = 300; total 2,000 x 300 = Rs 6,00,000.
2. After: price 550, contribution 350 per subscriber; subscribers 2,000 x 0.92 = 1,840; total 1,840 x 350 = Rs 6,44,000.
3. Change = +Rs 44,000 a month (+7.3%).
4. Break-even subscribers = 6,00,000 / 350 = 1,714.3, a fall of 285.7, which is 14.3% (also 1 - 300/350).
**Result:** Worth it: +Rs 44,000 per month. It can lose up to about 14.3% of subscribers (about 286) before profit drops.
**Check:** The 8% loss is well inside the 14.3% limit. Revenue also rises (10,00,000 to 10,12,000).
**Caveats:** Churn may continue to rise over later months; lost subscribers' future referrals and lifetime value are ignored. Watch 3-month churn, not only month one.
**Likely follow-ups:** 1) *What if variable cost were Rs 400?* Contribution 100 to 150, limit 33%. 2) *How to confirm?* A/B test on a segment.
**Common mistakes / traps:** Judging by revenue only; using 10% (the price rise) as the break-even; forgetting to deduct variable cost.

### Q11 ⭐⭐⭐ 🟡 Revenue grew 8% but profit fell sharply. Using the table below, diagnose which cost lines explain the fall in profit.
| Rs crore | Last year | This year |
|---|---|---|
| Revenue | 500 | 540 |
| Cost of goods sold | 300 | 330 |
| Marketing | 80 | 110 |
| Other costs | 70 | 80 |

**Asked at:** commonly asked (no company-specific report found); a "car manufacturer profit fell 40%" question was reported on a candidate-review site (snippet, unverified mapping).
**What the interviewer is checking:** Whether you compare each cost line against revenue growth, not just in rupees.
**Say this in the interview:** "Profit fell from 50 to 20 crore, down 60%. Marketing rose 37.5%, far faster than revenue, and it explains the biggest part."

**Clarify first:** Is marketing one-off or recurring? Did COGS rise from input prices or mix? What are "other costs"?
**Structure:** Profit = revenue - COGS - marketing - other. Compare growth rates and share of revenue for each line.
**What I would check, in order:** Each line's change in rupees and in % of revenue (Excel column of cost / revenue), then the reason behind the largest.
**Numeric work:**
1. Profit last year = 500 - 300 - 80 - 70 = 50; this year = 540 - 330 - 110 - 80 = 20. Fall of 30 crore (-60%).
2. Growth: revenue +8%, COGS +10%, marketing +37.5%, other +14.3%.
3. Share of revenue: COGS 60.0% to 61.1%; marketing 16.0% to 20.4%; other 14.0% to 14.8%.
4. Bridge: extra revenue +40, extra COGS -30, marketing -30, other -10, total -30.
5. At last year's cost ratios, profit would have been 54 (10% of 540), so the cost ratio shift cost 34 crore, of which marketing is about 24 (110 - 86.4) and COGS about 6, other about 4.
**If the data shows...:** Marketing with no revenue return means cut or fix efficiency; COGS rise from input prices means pricing or sourcing action.
**Recommendation:** Review marketing return per rupee (customers acquired, payback), tighten the least productive spend, and examine COGS for price versus mix. Track cost lines as a % of revenue monthly.
**Likely follow-ups:** 1) *Was marketing worth it?* Compare with new revenue (40 crore added but 30 crore marketing). 2) *Is 8% growth bought?* Likely.
**Common mistakes / traps:** Reading only rupee change (COGS also grew by 30); ignoring ratios.

### Q12 ⭐⭐⭐ 🟡 A product sells at Rs 1,000 with a variable cost of Rs 700. If you give a 10% discount, by what percentage must unit sales rise just to keep total contribution unchanged?
Data: price Rs 1,000; variable cost Rs 700 per unit; discount 10% off price.
**Asked at:** commonly asked (no company-specific report found); price-versus-volume trade-offs are standard in pricing prep guides (unverified).
**What the interviewer is checking:** Whether you know a discount comes straight out of contribution.
**Say this in the interview:** "Contribution falls from 300 to 200 per unit, so volume must rise by 50% just to stand still."

**Definition in plain words:** Required volume increase = old contribution / new contribution - 1.
**Worked answer:**
1. Old contribution = 1,000 - 700 = Rs 300 per unit.
2. Discounted price = 900; new contribution = 900 - 700 = Rs 200.
3. Units needed = 300 / 200 = 1.5 times the old volume.
4. Increase = 50%.
**Result:** Sales must rise by 50% to hold total contribution (a 10% price cut needs a 50% volume lift).
**Check:** Take 100 units: old 100 x 300 = 30,000; new 150 x 200 = 30,000.
**Caveats:** Thin margins magnify this; at a 30% contribution margin a 10-point discount costs a third of the margin. Also consider whether extra volume needs extra fixed capacity.
**Likely follow-ups:** 1) *If variable cost were 500?* 500 to 400, rise 25%. 2) *A 20% discount?* Contribution 100, volume x3, +200%.
**Common mistakes / traps:** Answering 10%; dividing by price instead of contribution.

### Q13 ⭐⭐⭐ 🟡 Calculate LTV, LTV:CAC and CAC payback in months for the subscription business below, and say whether you would scale marketing.
Data: ARPU Rs 300 per month; gross margin 60%; monthly churn 5%; CAC Rs 1,800. Use LTV = ARPU x gross margin / churn.
**Asked at:** commonly asked (no company-specific report found); SaaS unit-economics guides cover LTV, CAC and payback (unverified).
**What the interviewer is checking:** Correct formulas and a judgment, not just numbers.
**Say this in the interview:** "LTV is Rs 3,600, twice the CAC, and payback is 10 months. It works but is not strong enough to scale aggressively until churn or CAC improves."

**Definition in plain words:** LTV (lifetime value) is the gross profit one customer brings over their life; CAC (customer acquisition cost) is what it costs to win one; payback is how many months of gross profit repay the CAC.
**Worked answer:**
1. Monthly gross profit per customer = 300 x 0.60 = Rs 180.
2. Expected life = 1 / 0.05 = 20 months.
3. LTV = 180 / 0.05 = Rs 3,600.
4. LTV:CAC = 3,600 / 1,800 = 2.0.
5. CAC payback = 1,800 / 180 = 10 months.
**Result:** LTV Rs 3,600; LTV:CAC 2.0; payback 10 months.
**Check:** Payback of 10 months is half the 20-month average life, so profit after payback is thin. A common rule of thumb is LTV:CAC of 3 or more (a convention, not a law).
**Caveats:** An average churn hides that many customers leave early; those who leave before 10 months never repay CAC. Look at cohorts. Improving churn to 4% raises LTV to 4,500 (ratio 2.5).
**Recommendation:** Do not scale broadly yet; fix churn or lower CAC (cheaper channels), then scale the best channel.
**Likely follow-ups:** 1) *Which lever helps most?* Churn, as LTV is inversely proportional to it. 2) *Why gross margin not revenue?* Revenue overstates what you keep.
**Common mistakes / traps:** Using revenue instead of gross profit; confusing monthly and annual churn.

### Q14 ⭐⭐⭐ 🟡 A marketplace's profit fell although total order count rose. Revenue per order is fixed at a 12% commission, so where else would you look? Give a hypothesis tree and the data cuts you would use.
Available data: orders, GMV (gross merchandise value, the total value of goods ordered), commission revenue, discounts funded by the platform, logistics cost, refunds, marketing spend, all by month, city and category.
**Asked at:** commonly asked (no company-specific report found); a Meesho "declining orders root cause" case is reported in an internal compilation (unverified).
**What the interviewer is checking:** Whether you see that commission % fixed does not fix revenue per order (order value changes) and that costs can move.
**Say this in the interview:** "Commission is a fixed percentage but order value is not, and costs per order can rise. I will check revenue per order, then each cost per order, then mix by city and category."

**Clarify first:** How much did profit fall and when did it start? Orders up by how much? Any new city, category or campaign?
**Structure:**
- Revenue per order: average order value falling (smaller baskets, cheaper categories); refunds reversing commission; more returns.
- Cost per order: platform-funded discounts up; logistics per order up (longer distances, new cities, low density); marketing per order up; support and payment fees.
- Mix: growth concentrated in low-margin cities or categories, or from new customers on heavy discounts.
- Fixed cost: expansion cost not yet absorbed.
**What I would check, in order:**
1. Contribution per order by month (the headline trend).
2. Average order value and net commission per order after refunds.
3. Discount, logistics and marketing per order by month.
4. Same cuts by city and category to find where the decline concentrates (SQL GROUP BY, pivot).
5. Cohorts: new versus repeat customers.
**If the data shows...:** Falling AOV points to basket or mix issues; rising discounts per order points to a promotion problem; logistics per order up in new cities points to expansion cost; a single category with heavy refunds points to quality.
**Recommendation:** Quantify each driver in rupees per order and total, fix the largest first (for example cap discounts), and monitor contribution per order weekly.
**Likely follow-ups:** 1) *Order growth with falling profit, is that bad?* If every order loses money, yes. 2) *First chart?* Contribution per order by month.
**Common mistakes / traps:** Assuming commission fixed means revenue per order fixed; ignoring refunds; only looking at totals.

### Q15 ⭐⭐⭐ 🟡 A marketplace earns a 12% commission on an average order of Rs 600. It bears Rs 50 forward logistics per order and Rs 50 reverse logistics per returned order, and refunds the commission on returns. With a 20% return rate, what is the contribution per order placed, and at what return rate does it break even?
Data: AOV Rs 600; commission 12% (refunded on returned orders); forward logistics Rs 50 per order placed; reverse logistics Rs 50 per returned order; return rate 20%.
**Asked at:** commonly asked (no company-specific report found); e-commerce return economics appear in Flipkart and Meesho analyst prep guides (unverified).
**What the interviewer is checking:** Whether returns remove revenue and add cost together.
**Say this in the interview:** "Commission is Rs 72 per order but only 80% of orders keep it, and returns add reverse logistics. Contribution is about minus Rs 2.4 per order; break-even return rate is about 18%."

**Definition in plain words:** Contribution per order placed = commission kept on orders not returned - forward logistics on all orders - reverse logistics on returned orders.
**Worked answer:**
1. Commission per order = 12% x 600 = Rs 72.
2. Commission kept = 72 x (1 - 0.20) = Rs 57.60.
3. Forward logistics = Rs 50 on every order.
4. Reverse logistics = 50 x 0.20 = Rs 10 per order placed.
5. Contribution = 57.60 - 50 - 10 = -Rs 2.40 per order placed.
6. Break-even return rate r: 72(1 - r) - 50 - 50r = 0, so 22 = 122r, r = 0.1803.
**Result:** -Rs 2.40 per order at 20% returns; break-even at a return rate of about 18.0%.
**Check:** At 18.03% returns: 72 x 0.8197 = 59.02; less 50 less 9.02 = 0. At 0% returns contribution is +Rs 22. Each point of return rate costs Rs 1.22.
**Caveats:** Assumes returns reverse the full commission and logistics is not refunded; a different policy changes the answer. Payment fees and support are ignored.
**Likely follow-ups:** 1) *How to improve?* Cut returns (better size guidance), charge return fees, lower logistics. 2) *Which category first?* Highest return rate.
**Common mistakes / traps:** Applying commission to all orders; applying reverse cost to all orders.

### Q16 ⭐⭐⭐ 🟡 Revenue per month = active users x orders per user x average order value. Using the data below, compute the revenue growth and say which driver contributed most.
| | Last year | This year |
|---|---|---|
| Monthly active users | 1,000,000 | 1,200,000 |
| Orders per user per month | 2.0 | 1.9 |
| Average order value (Rs) | 350 | 380 |

**Asked at:** commonly asked (no company-specific report found); driver decomposition of revenue is a standard KPI-case skill at Flipkart and Swiggy rounds per prep sites (unverified).
**What the interviewer is checking:** Whether you multiply the growth factors and attribute fairly.
**Say this in the interview:** "Revenue is up about 23.8%. Users grew 20%, frequency fell 5%, order value rose 8.6%; users contributed the most."

**Definition in plain words:** Revenue is a product of three drivers, so total growth is the product of the three growth factors, not their sum.
**Worked answer:**
1. Last year revenue = 1,000,000 x 2.0 x 350 = Rs 70.0 crore a month.
2. This year = 1,200,000 x 1.9 x 380 = Rs 86.64 crore a month.
3. Growth = 86.64 / 70.0 - 1 = 23.8%.
4. Factors: users 1.200, orders per user 0.950, AOV 1.0857.
5. Share of growth (using logarithms so shares add up): users about 85%, AOV about 39%, frequency about -24%.
**Result:** Revenue +23.8% (Rs 70 crore to Rs 86.6 crore a month). Users contribute most; AOV helps; falling frequency is a drag.
**Check:** 1.2 x 0.95 x 1.0857 = 1.2377. The simple additions (20 - 5 + 8.6 = 23.6) are close but not exact.
**Caveats:** Attribution depends on method; the order of the drivers matters in rupee-step methods. New users often order less often, which may explain the frequency fall (a mix effect).
**Likely follow-ups:** 1) *What would you probe?* Frequency of new versus old users. 2) *Is AOV growth good?* Check if inflation or a price rise.
**Common mistakes / traps:** Adding percentages instead of multiplying; ignoring the frequency drop.

### Q17 ⭐⭐⭐ 🟡 A company sells two products with the mix and margins below. Without any change in price or cost, how does the blended margin change when the mix shifts, and why can this hide in a profit review?
Data: Last year: product A is 60% of revenue at 40% margin; product B is 40% of revenue at 10% margin. This year mix is 40% A and 60% B with the same margins.
**Asked at:** commonly asked (no company-specific report found); mix-shift effects are a standard profit-diagnosis item (gap-fill, no source).
**What the interviewer is checking:** Whether you can compute a weighted average and explain mix effect.
**Say this in the interview:** "Blended margin falls from 28% to 22%, purely from selling more of the low-margin product, with no price or cost change."

**Definition in plain words:** Blended margin = sum of (share of revenue x product margin).
**Worked answer:**
1. Last year: 0.60 x 40% + 0.40 x 10% = 24% + 4% = 28%.
2. This year: 0.40 x 40% + 0.60 x 10% = 16% + 6% = 22%.
3. Change = -6 percentage points.
**Result:** Blended margin falls from 28% to 22%.
**Check:** On Rs 100 of revenue, margin is Rs 28 last year and Rs 22 this year; a 21% drop in profit per rupee of revenue.
**Caveats:** It hides because each product's own margin is unchanged, so product-level reviews show "no problem", only the total looks worse. The revenue may even rise, so the story seems healthy. Always split a margin change into rate effect and mix effect.
**Likely follow-ups:** 1) *How to respond?* Push A through promotion or price B. 2) *Is the mix shift always bad?* Not if B brings volume and customers.
**Common mistakes / traps:** Averaging 40% and 10% as 25%; blaming price or cost.

### Q18 ⭐⭐⭐ 🟡 A quick-commerce dark store handles 1,200 orders a day with contribution of Rs 25 per order, and has fixed costs of Rs 40,000 per day. What is the break-even order volume, and how would you close the gap?
Data: orders 1,200 per day; contribution Rs 25 per order; fixed cost Rs 40,000 per day (rent, staff, utilities).
**Asked at:** commonly asked (no company-specific report found); quick-commerce articles describe dark-store contribution and fixed-cost drivers (figures here are invented, unverified).
**What the interviewer is checking:** Break-even and practical levers.
**Say this in the interview:** "Break-even is 1,600 orders a day; today it loses Rs 10,000 a day. Levers are 400 more orders, about Rs 8 more contribution per order, or 25% lower fixed cost."

**Definition in plain words:** Break-even orders = fixed cost / contribution per order.
**Worked answer:**
1. Break-even = 40,000 / 25 = 1,600 orders a day.
2. Current contribution = 1,200 x 25 = Rs 30,000; loss = 30,000 - 40,000 = -Rs 10,000 a day.
3. Gap = 400 orders (33% more volume).
4. Alternatives: contribution per order needed at 1,200 orders = 40,000 / 1,200 = Rs 33.3 (+Rs 8.3); or fixed cost cut to Rs 30,000 (-25%).
**Result:** Break-even 1,600 orders a day; current loss Rs 10,000 a day.
**Check:** 1,600 x 25 = 40,000.
**Caveats:** More orders need more staff and picking capacity, so fixed cost may step up. Mix of levers is realistic.
**Recommendation:** Raise order value (minimum basket, bundles), cut discounts, increase density with marketing in the catchment, charge a small fee on low baskets; review store hours and staffing. For example +200 orders and +Rs 4 contribution: 1,400 x 29 = 40,600, break-even.
**Likely follow-ups:** 1) *If average order value rises 20%?* Contribution per order rises if variable costs are mostly per order not per rupee. 2) *When close the store?* If no path to break-even.
**Common mistakes / traps:** Counting fixed cost per order as variable; ignoring capacity limits.

### Q19 ⭐⭐⭐ 🟡 A SaaS company's annual recurring revenue (ARR) bridge is below. Calculate net revenue retention and gross revenue retention, and say whether the 30% growth is healthy.
Data (Rs crore): opening ARR 10; new customers +3; expansion +1.5; churn -1.0; contraction -0.5; closing ARR 13.
**Asked at:** commonly asked (no company-specific report found); SaaS retention metrics appear in SaaS case guides (unverified).
**What the interviewer is checking:** Whether you exclude new customers from retention and read the quality of growth.
**Say this in the interview:** "NRR is 100% and GRR is 85%. All the 30% growth comes from new customers, so the base is not growing by itself."

**Definition in plain words:** Net revenue retention (NRR) = revenue today from last year's customers divided by their revenue a year ago (includes expansion, churn and contraction, excludes new customers). Gross revenue retention (GRR) excludes expansion, so it cannot exceed 100%.
**Worked answer:**
1. Check bridge: 10 + 3 + 1.5 - 1.0 - 0.5 = 13. Consistent.
2. NRR = (10 + 1.5 - 1.0 - 0.5) / 10 = 10 / 10 = 100%.
3. GRR = (10 - 1.0 - 0.5) / 10 = 8.5 / 10 = 85%.
4. Growth = (13 - 10) / 10 = 30%, of which new customers give 30 points and the existing base gives 0.
**Result:** NRR 100%; GRR 85%; growth 30%.
**Check:** Growth = NRR - 100% + new customers / opening = 0% + 30% = 30%.
**Caveats:** Healthy depends on stage and segment; common prep benchmarks say good NRR is above 100% and GRR in the 90s for enterprise software (rule of thumb, unverified). A 15% annual revenue leak must be replaced by new sales every year, and growth depends on keeping acquisition spend going. Judge with new-customer acquisition cost.
**Likely follow-ups:** 1) *How to improve?* Reduce churn, upsell. 2) *What is the key risk?* Slowing new sales stalls growth.
**Common mistakes / traps:** Including new customers in NRR; computing GRR with expansion; calling 30% growth healthy without looking at its source.

### Q20 ⭐⭐⭐ 🟡 A price test shows the results below. Which price should be rolled out on profit per visitor, and what else would you check before the rollout?
| Variant | Price (Rs) | Visitors | Conversion |
|---|---|---|---|
| A | 99 | 10,000 | 5.0% |
| B | 129 | 10,000 | 4.0% |

Variable cost per sale is Rs 20 in both variants.
**Asked at:** commonly asked (no company-specific report found); A/B price tests are a standard pricing-case theme (unverified).
**What the interviewer is checking:** Profit per visitor, not conversion, and awareness of test quality.
**Say this in the interview:** "B earns Rs 4.36 per visitor against Rs 3.95 for A, about 10% more, even though it converts less. But that profit gap is not yet statistically proven, so I would extend the test and check retention before rolling out."

**Definition in plain words:** Profit per visitor = conversion rate x (price - variable cost).
**Worked answer:**
1. A: sales = 10,000 x 5% = 500; contribution per sale 99 - 20 = 79; profit = 500 x 79 = Rs 39,500; per visitor Rs 3.95.
2. B: sales = 400; contribution 129 - 20 = 109; profit = 400 x 109 = Rs 43,600; per visitor Rs 4.36.
3. B is better by Rs 4,100 (+10.4%).
**Result:** B (Rs 129) is ahead on profit per visitor (+Rs 0.41), but the lead is not yet proven; extend the test before a full rollout.
**Check:** Revenue also favours B (Rs 51,600 versus Rs 49,500). A two-proportion test on conversion (5.0% versus 4.0%, 10,000 each) gives z of about 3.4, so the conversion drop is real; the key question is whether the profit-per-visitor gap of Rs 0.41 is real. A rough test on profit itself (standard error about Rs 0.27, from each visitor earning either Rs 0 or the full contribution) gives z of about 1.5, below the usual 1.96 bar, so the data cannot yet separate B from noise.
**Caveats:** Check: random assignment and equal traffic mix; test duration and seasonality; refunds and cancellations; repeat purchase and renewal (a higher price may bring lower retention or reviews); customer segments (price-sensitive groups); brand impact; whether the test price is permanent. Consider an intermediate price (for example Rs 109).
**Likely follow-ups:** 1) *If B had 3.5%?* Profit per visitor 3.82, below A; break-even conversion is 3.95 / 109 = 3.62%. 2) *Why not choose the higher conversion?* Profit matters.
**Common mistakes / traps:** Choosing A for higher conversion; forgetting variable cost; ignoring statistical noise.

### Q21 ⭐⭐⭐ 🟡 The price of a product rises 4% and its price elasticity of demand is -1.5. By what percentage does demand change, and does revenue rise or fall?
Data: price elasticity -1.5; price change +4%; assume the elasticity holds over this small change.
**Asked at:** commonly asked (no company-specific report found); a price elasticity worked example (elasticity -2) appears in prep guides (unverified).
**What the interviewer is checking:** Elasticity formula and its revenue implication.
**Say this in the interview:** "Demand falls 6% and, since elasticity is beyond 1 in size, revenue falls, by about 2.2%."

**Definition in plain words:** Price elasticity = % change in quantity demanded / % change in price.
**Worked answer:**
1. % change in demand = -1.5 x 4% = -6%.
2. Revenue factor = 1.04 x 0.94 = 0.9776.
3. Revenue change = -2.24%.
**Result:** Demand -6%; revenue -2.2%.
**Check:** Elastic demand (size above 1) means a price rise cuts revenue; inelastic (below 1) means revenue rises. Revenue change is approximately (1 + elasticity) x price change = -0.5 x 4% = -2%; the exact figure is -2.24% because of compounding.
**Caveats:** Elasticity is only valid for small changes near the current price. Profit may still rise if variable cost per unit is high, since fewer units are sold (cost saved): e.g. price 100, variable cost 80, contribution 20; after: 104 - 80 = 24 x 0.94 = 22.56, profit up 12.8% despite lower revenue.
**Likely follow-ups:** 1) *What if elasticity is -0.5?* Demand -2%, revenue +1.9%. 2) *Why negative?* Higher price lowers demand.
**Common mistakes / traps:** Dropping the sign; saying revenue rises because price rises; confusing revenue with profit.

### Q22 ⭐⭐⭐ 🔴 A food delivery company's profit per order has turned negative while order volume is growing. Walk through how you would diagnose it, and say what decision rule would make you recommend cutting orders instead of growing them.
**Asked at:** commonly asked (no company-specific report found); a B-school casebook covers food delivery profitability and Swiggy business cases are reported on prep sites (unverified).
**What the interviewer is checking:** Whether you find the driver of lost contribution and apply a clear stop-or-grow rule.
**Say this in the interview:** "I will split profit per order into revenue and cost lines, find which moved, and separate bad orders from the good ones. The rule is: if an order group has negative contribution and no credible path to positive, cut or reprice it."

**Clarify first:** When did it turn negative? Which cities, restaurants, customer types? What changed (discounts, rider pay, new market)? Which profit is it (contribution or fully loaded)?
**Structure:**
- Revenue per order: average order value, commission rate, delivery and platform fees, ad income.
- Variable cost per order: rider pay (distance, waiting, incentives), discounts, refunds, payment and support.
- Mix: growth from new cities, long distances, small baskets, heavy-discount new users.
- Fixed costs versus scale: dilute only if contribution is positive.
**What I would check, in order:**
1. Contribution per order by month and by line item (waterfall).
2. By city, order value band, distance band, new versus repeat, discount code.
3. Rider cost per order and rider utilisation (orders per rider hour).
4. Refunds and cancellations by restaurant.
**If the data shows...:** Rider cost rising from low density means focus orders on dense zones; discounts on repeat users means cut; small baskets means minimum order value or fee; commission too low means renegotiate.
**Numeric work (illustrative):** Say contribution is -Rs 5 per order. Growing volume multiplies the loss. If a reprice of +Rs 10 fee loses 10% of orders but turns contribution positive, do that. Cut rule: contribution after realistic fixes is still negative and the order group does not bring repeat customers with positive lifetime value (LTV, lifetime value, meaning total contribution a customer brings over their life, above the loss made to win them).
**Recommendation:** Pause growth in negative-contribution segments, fix unit economics (fees, discounts, rider efficiency), then scale where contribution is positive. Track contribution per order weekly by segment.
**Likely follow-ups:** 1) *Why not grow to cover fixed costs?* Negative contribution gets worse with scale. 2) *Any reason to keep loss-making orders?* If repeat behaviour makes lifetime value exceed the loss.
**Common mistakes / traps:** Chasing GMV; averaging across segments (hides profitable cores); forgetting platform-funded discounts.

### Q23 ⭐⭐⭐ 🔴 A festival sale doubled GMV but the finance team says it lost money. Use the data below to decide whether the sale was worth it, and list what you ignored.
Data: a normal week has 10 lakh orders at contribution of Rs 30 per order. The sale week had 25 lakh orders at contribution of Rs -10 per order. 20% of sale-week orders came from new customers; 30% of those new customers stay active, each worth a further Rs 300 contribution over their lifetime.
**Asked at:** commonly asked (no company-specific report found); a case-style item, not tied to a named company.
**What the interviewer is checking:** Whether you compare with the baseline and value new customers properly without overclaiming.
**Say this in the interview:** "A normal week earns Rs 3 crore contribution; the sale week loses Rs 2.5 crore, a gap of Rs 5.5 crore. New-customer future value is Rs 4.5 crore, so the sale still lost about Rs 1 crore. It only pays if retention is above about 37%."

**Clarify first:** Is "doubled GMV" right? The data shows 2.5 times the orders, so average order value must be lower by 20% (2 / 2.5), or "doubled" is loose. I use the order numbers as given.
**Structure:** Compare sale week with a normal week (the baseline), then add future value of customers won, then list what is excluded.
**What I would check, in order:** Contribution by new versus existing customers; pull-forward (orders borrowed from neighbouring weeks); post-sale dip; marketing spend and fixed costs; retention at 30, 60, 90 days.
**Numeric work:**
1. Normal week contribution = 10 lakh x 30 = Rs 300 lakh (Rs 3 crore).
2. Sale week contribution = 25 lakh x (-10) = -Rs 250 lakh.
3. Sale shortfall versus normal = -250 - 300 = -Rs 550 lakh.
4. New customers = 20% x 25 lakh = 5 lakh (treating each order as one customer, an assumption); retained = 30% = 1.5 lakh; future value = 1.5 lakh x 300 = Rs 450 lakh.
5. Net versus normal = -550 + 450 = -Rs 100 lakh (a loss of Rs 1 crore).
6. Break-even retention = 550 / (5 lakh x 300) = 36.7%, versus 30% assumed.
**If the data shows...:** Retention above about 37% (or lifetime value above Rs 367 for a 30% retained base) means the sale was worth it; pull-forward demand makes it worse; existing customers buying at a discount they would have paid in full makes it worse.
**Recommendation:** Not worth it as run on these numbers. Keep festival sales but target new customers, cap discounts for existing ones, and measure 90-day retention before judging.
**What I ignored:** Pull-forward and post-sale dip; cannibalisation of regular buyers; brand and traffic effects; marketing and fixed cost; discounting funded by suppliers; returns; that a "new customer" may be one with several orders; the time value of the Rs 300.
**Likely follow-ups:** 1) *What if lifetime value is Rs 400?* Future value 600 lakh, net +50 lakh. 2) *Which sale design is better?* Target new users.
**Common mistakes / traps:** Judging by GMV; ignoring the baseline; counting future value without checking retention.

### Q24 ⭐⭐ 🟢 What are cost-plus, value-based and competition-based pricing, and when would you use each?
**Asked at:** commonly asked (no company-specific report found); the three pricing methods are in consulting prep material (unverified).
**What the interviewer is checking:** Whether you know the three methods and their fit.
**Say this in the interview:** "Cost-plus starts from cost, value-based from what the customer gains, competition-based from rivals' prices. I choose by how unique the product is and how well I know the customer's value."

**Explain simply:**
- Cost-plus: price = cost + a margin (cost Rs 80, 25% markup, price Rs 100). Simple, used for commodities, contracts and when value is hard to measure. Weakness: ignores what customers will pay, may leave money on the table or overprice.
- Value-based: price = a share of the benefit the customer gets. A software that saves a firm Rs 10 lakh a year can charge Rs 2-3 lakh. Best for differentiated products and B2B. Needs customer research.
- Competition-based: price near rivals (a little above or below). Used where products are similar and customers compare easily (groceries, fuel, airline tickets). Weakness: price wars, ignores your cost.
- In practice, combine: cost sets the floor, value sets the ceiling, competition places you between.
- Mini example: floor Rs 100 (cost-plus), customer value Rs 300, rivals charge Rs 180, so test Rs 150 to 190.

**Practice step:** Pick a product and write its floor, ceiling and rival price.
**Likely follow-ups:** 1) *Which for a new product?* Value-based. 2) *Which for a commodity?* Competition or cost-plus.
**Common mistakes / traps:** Treating cost-plus as always safe; ignoring the floor (selling below cost).

### Q25 ⭐⭐ 🟢 What is price elasticity of demand, and how would you judge whether a product is price-sensitive when you have no elasticity estimate?
**Asked at:** commonly asked (no company-specific report found); a price elasticity worked example is on a consulting prep site (unverified).
**What the interviewer is checking:** Whether you can define it and reason qualitatively with proxies.
**Say this in the interview:** "Elasticity is the % change in demand for a 1% change in price. Without an estimate I look at substitutes, necessity, price share of budget, past price changes and a small test."

**Explain simply:**
- Elasticity = % change in quantity / % change in price. Usually negative. Elastic means the absolute size is above 1 (demand moves more than price); inelastic means below 1.
- Mini example: price +10%, demand -20% gives -2 (elastic); demand -5% gives -0.5 (inelastic).
- Without an estimate, ask: Are there close substitutes? Is it a necessity (salt, medicines) or a luxury? Is it a big part of the customer's budget? Do customers buy frequently and compare? How much time do they have to switch? Who is the buyer (price-conscious students versus companies)?
- Use data: past price changes or discounts and what happened to sales; competitor price moves; coupon redemption; segment differences (new versus loyal).
- Best: a small price A/B test on a segment and measure profit, not just units.
- Rule of thumb: elastic goods are risky to raise, inelastic goods can take rises.

**Practice step:** Rate five products you buy as elastic or inelastic and say why.
**Likely follow-ups:** 1) *Elastic demand and price cut?* Revenue rises. 2) *Is elasticity constant?* No, it varies by price level and segment.
**Common mistakes / traps:** Treating elasticity as fixed; confusing elasticity with slope; forgetting to look at profit.

### Q26 ⭐⭐ 🟢 How do you size and prioritise growth ideas once you have listed them, so that you recommend two or three rather than twenty?
**Asked at:** commonly asked (no company-specific report found); growth cases appear in prep-site reports for Flipkart, Meesho and Mu Sigma style rounds (unverified).
**What the interviewer is checking:** Whether you can turn a long list into a ranked shortlist using numbers, not opinion.
**Say this in the interview:** "I size each idea in rupees with a quick formula, score it on impact, confidence and effort, and recommend the top two or three that fit the goal and the timeline."

**Explain simply:**
- Step 1, group the ideas into buckets (get more users, get each user to spend more, keep users longer) so nothing overlaps.
- Step 2, size each in rupees: users reached x change you expect x value per user. Use rough, clearly assumed numbers.
- Step 3, score on impact (rupees), confidence (how much evidence you have) and effort (cost and time). A simple score is impact x confidence / effort.
- Step 4, check fit: does it meet the target, are there risks, can it start soon?
- Worked mini-example (all numbers assumed): Idea A, a checkout fix: 2,00,000 visitors x 2 percentage-point rise in conversion = 4,000 extra orders x Rs 500 = Rs 20 lakh a month, effort 2 weeks. Idea B, win-back messages: 50,000 lapsed users x 5% = 2,500 orders x Rs 400 = Rs 10 lakh a month, effort 1 week. A is bigger, B is cheaper; recommend both and park the rest.
- Practice: list five ideas for an HR job portal and size each in one line.

**Likely follow-ups:** 1) *What if sizing is very uncertain?* Give a low, base and high case and run a small test first. 2) *How many ideas do you recommend?* Two or three, enough to hit the target but few enough to execute.
**Common mistakes / traps:** Ranking by gut feeling; sizing without an assumed value per user; ignoring effort and time; recommending everything.

### Q27 ⭐⭐ 🟢 What is the difference between a revenue problem and a margin problem, and how does the difference change the data you pull first?
**Asked at:** commonly asked (no company-specific report found); the revenue-drop root-cause case is reported for Swiggy and Meesho on prep sites (unverified).
**What the interviewer is checking:** Whether you split the first step of a profit case correctly before diving into data.
**Say this in the interview:** "A revenue problem means too little money coming in; a margin problem means too much of it goes out as cost. I first check which one it is by comparing revenue and cost trends, then pull different data for each."

**Explain simply:**
- Revenue problem: revenue = volume x price. Pull orders, customers, price, mix and channel data over time.
- Margin problem: margin = (revenue - cost) / revenue. Pull cost lines per unit (product cost, delivery, discounts, staff) and compare with revenue per unit.
- Quick test with assumed numbers: revenue Rs 100 and cost Rs 80 last year (margin 20%). This year revenue Rs 100 and cost Rs 90 is a margin problem (10%); revenue Rs 80 and cost Rs 64 is a revenue problem (margin still 20%, but profit is Rs 16 instead of Rs 20).
- Both can happen together, so check each in turn.
- Practice: take any company's two-year results and label which problem you see.

**Likely follow-ups:** 1) *Which is easier to fix?* Often margin, through price and cost, but only if the cost is controllable. 2) *First chart you draw?* Revenue, cost and margin % by month on one view.
**Common mistakes / traps:** Treating falling profit as always a sales problem; looking only at the percentage, not the rupee amount; skipping the mix effect.

### Q28 ⭐⭐ 🟢 What clarifying questions would you ask the interviewer before starting a growth or profitability case?
**Asked at:** commonly asked (no company-specific report found); structured clarification is expected in consulting-style case rounds on prep sites (unverified).
**What the interviewer is checking:** Whether you define the goal, scope and constraints before analysing.
**Say this in the interview:** "I would ask about the goal and timeline, the business and customers, the numbers and the constraints, in that order, then repeat my understanding back."

**Explain simply:**
- Goal: what exactly is the target (profit, revenue, share) and by when? How is success measured?
- Business: what do they sell, to whom, through which channels, in which cities? Who are the competitors?
- Numbers: how has the metric moved over time, versus the plan and the industry? Is this sudden or gradual?
- Constraints: budget, capacity, brand rules, regulation, what is off the table.
- Definitions: what do revenue, profit and "active customer" mean here?
- Say it back: "So the goal is X by Y within Z. Is that right?" Then ask for a minute to structure.
- Practice: write four questions for "grow revenue 20%" and four for "profit has fallen".

**Likely follow-ups:** 1) *How many questions?* About three to five, grouped, not a long list. 2) *What if the interviewer says "you tell me"?* State a sensible assumption aloud and move on.
**Common mistakes / traps:** Asking questions with no purpose; skipping goal and timeline; not confirming the definitions; starting the maths before the scope is clear.

### Q29 ⭐⭐ 🟢 How do you present your recommendation at the end of a case in about 60 seconds?
**Asked at:** commonly asked (no company-specific report found); a short closing recommendation is a standard case-interview step on prep sites (unverified).
**What the interviewer is checking:** Whether you can give a clear answer first, then reasons, risks and next steps.
**Say this in the interview:** "Answer first, then three reasons with numbers, then the main risk, then what I would do next and how I would measure it."

**Explain simply:**
- Sentence 1: the recommendation ("Do X, because it improves profit by about Rs Y").
- Sentences 2 to 4: two or three reasons, each with one number from your work.
- Sentence 5: the biggest risk and how you would reduce it.
- Sentence 6: next steps and the metric that proves it worked (for example, contribution per order after 4 weeks).
- Mini-example (assumed numbers): "I recommend raising the delivery fee by Rs 10. Contribution per order goes from Rs 20 to Rs 30, and orders can fall by up to a third before we lose money. The risk is that loyal users leave, so I would test in two cities for a month and watch orders per user."
- Practice: record yourself and keep it under 60 seconds, about 150 words.

**Likely follow-ups:** 1) *What if you ran short of time?* Give the answer and the top reason, then offer detail. 2) *What if the data was incomplete?* Say what is assumed and what would change the answer.
**Common mistakes / traps:** Re-telling the whole case in order; no clear answer; no numbers; no risk or next step; adding new analysis at the end.

### Q30 ⭐⭐ 🟡 A fintech lender's book economics are below. What is the annual profit, and at what credit loss rate does it break even?
Data: loan book Rs 100 crore; yield 24% a year; cost of funds 11%; credit loss 6%; operating cost 5% of the book. All figures annual, as a percentage of the average book.
**Asked at:** commonly asked (no company-specific report found); fintech lending cases are described on prep sites (unverified); the numbers are invented for practice.
**What the interviewer is checking:** Whether you build a simple spread-based profit and solve backwards for the break-even loss rate.
**Say this in the interview:** "Profit as a percent of the book is yield minus funding, loss and operating cost: 24 - 11 - 6 - 5 = 2%, which is Rs 2 crore. It breaks even if credit loss reaches 8%."

**Definition in plain words:** Yield is interest earned on loans; cost of funds is the interest the lender pays for its own money; credit loss is the share of loans never repaid. Profit = book x (yield - cost of funds - credit loss - operating cost).
**Worked answer:**
1. Net spread after funding = 24% - 11% = 13%.
2. After credit loss = 13% - 6% = 7%.
3. After operating cost = 7% - 5% = 2%.
4. Profit = 2% x Rs 100 crore = Rs 2 crore.
5. Break-even loss rate: 24 - 11 - 5 = 8%.
**Result:** Annual profit Rs 2 crore (2% of the book); break-even credit loss 8%, only 2 percentage points above today's 6%.
**Check:** At 8% loss: 24 - 11 - 8 - 5 = 0. Each extra 1 point of loss removes Rs 1 crore, so a cushion of 2 points equals the whole profit.
**Caveats:** Real lenders also record fees, tax and the capital they hold; loss rates appear with a delay; the book changes through the year.
**Likely follow-ups:** 1) *What if loss rises to 9%?* Loss of Rs 1 crore a year. 2) *Levers?* Raise yield, cut funding cost, tighten approval to cut losses, cut operating cost.
**Common mistakes / traps:** Forgetting cost of funds; applying losses to the yield rather than the book; ignoring that loss rates are uncertain.

### Q31 ⭐⭐ 🟡 Using the profit bridge data below, split the change in contribution into a price effect and a volume effect.
Data: last year 100 units sold at Rs 100 each; this year 120 units at Rs 90 each. Variable cost is Rs 60 per unit in both years. Treat price effect = change in price x this year's units, and volume effect = change in units x last year's unit contribution.
**Asked at:** commonly asked (no company-specific report found); price-volume bridges are a standard finance-style case step (unverified); the numbers are invented for practice.
**What the interviewer is checking:** Whether you can split a change into price and volume parts that add up exactly.
**Say this in the interview:** "Total contribution fell Rs 400, from Rs 4,000 to Rs 3,600. The price cut cost Rs 1,200 and the extra volume added Rs 800."

**Definition in plain words:** Contribution = units x (price - variable cost). A bridge splits the change into what came from price and what came from volume, using the stated convention.
**Worked answer:**
1. Last year: 100 x (100 - 60) = Rs 4,000.
2. This year: 120 x (90 - 60) = Rs 3,600.
3. Total change = 3,600 - 4,000 = -Rs 400.
4. Price effect = (90 - 100) x 120 = -Rs 1,200.
5. Volume effect = (120 - 100) x 40 = +Rs 800.
**Result:** Price -Rs 1,200, volume +Rs 800, total -Rs 400.
**Check:** -1,200 + 800 = -400, matching steps 1 to 3.
**Caveats:** Order matters. Using last year's units for price and this year's contribution for volume gives a different split; only the total is order-free. Say which convention you used.
**Likely follow-ups:** 1) *Was the price cut worth it?* Not here: it lost Rs 400. Break-even volume at Rs 30 contribution is 133 units. 2) *Add mix?* Split volume further by product.
**Common mistakes / traps:** Using revenue instead of contribution; changing the convention midway; a split that does not add to the total.

### Q32 ⭐⭐ 🟡 Edtech course: what is the contribution per sale, and how many sales a month are needed to cover fixed costs?
Data: course price Rs 20,000; 15% of sales are refunded in full; CAC per sale Rs 6,000 (spent on all sales); delivery cost Rs 3,000 per sale; fixed cost Rs 1.6 crore per month. Treat the refund as lost revenue only, with the CAC and delivery cost not recovered.
**Asked at:** commonly asked (no company-specific report found); the numbers are invented for practice.
**What the interviewer is checking:** Whether you net refunds off revenue before costs and then compute break-even sales.
**Say this in the interview:** "Net revenue per sale is Rs 17,000 after refunds, minus Rs 9,000 of CAC and delivery gives Rs 8,000 contribution. Rs 1.6 crore divided by Rs 8,000 means 2,000 sales a month."

**Definition in plain words:** CAC (customer acquisition cost) is marketing spend per sale. Contribution per sale = expected revenue - variable costs. Break-even sales = fixed cost / contribution per sale.
**Worked answer:**
1. Expected revenue per sale = 20,000 x (1 - 0.15) = Rs 17,000.
2. Variable costs = 6,000 + 3,000 = Rs 9,000.
3. Contribution = 17,000 - 9,000 = Rs 8,000.
4. Fixed cost Rs 1.6 crore = Rs 1,60,00,000.
5. Break-even = 1,60,00,000 / 8,000 = 2,000 sales.
**Result:** Contribution Rs 8,000 per sale (40% of the list price); about 2,000 sales a month.
**Check:** 2,000 x 8,000 = Rs 1.6 crore. If refunds were 25% instead, contribution would fall to Rs 6,000 (20,000 x 0.75 - 9,000) and break-even would rise to about 2,667 sales.
**Caveats:** Treating CAC as variable is a choice; some firms count part of it as fixed. Refund timing and payment-gateway fees are ignored.
**Likely follow-ups:** 1) *Biggest lever?* Cut refunds or CAC; each Rs 1,000 of CAC is 12.5% of contribution. 2) *Is 2,000 a month realistic?* Compare with current volume.
**Common mistakes / traps:** Refunding only revenue but also removing CAC; dividing by the list price; forgetting fixed cost units (crore to rupees).

### Q33 ⭐⭐ 🟡 A call-centre analyst finds each agent earns less than they cost. Compute the monthly profit per agent and the break-even utilisation.
Data: billing Rs 450 per productive hour; 160 paid hours per agent per month; utilisation 70%; fully loaded cost per agent Rs 55,000 per month.
**Asked at:** commonly asked (no company-specific report found); BPO unit economics is a gap-fill HR-friendly example; the numbers are invented for practice.
**What the interviewer is checking:** Whether you connect utilisation to revenue per agent and solve backwards for break-even.
**Say this in the interview:** "At 70% utilisation an agent bills Rs 50,400 against a cost of Rs 55,000, a loss of Rs 4,600. Break-even utilisation is about 76.4%."

**Definition in plain words:** Utilisation is the share of paid hours that are productive (billable). Fully loaded cost includes salary, benefits, seat, tools and supervision.
**Worked answer:**
1. Productive hours = 160 x 0.70 = 112.
2. Billing = 112 x 450 = Rs 50,400.
3. Profit = 50,400 - 55,000 = -Rs 4,600 per agent per month.
4. Maximum billing at 100% = 160 x 450 = Rs 72,000.
5. Break-even utilisation = 55,000 / 72,000 = 76.4%.
**Result:** Loss of Rs 4,600 per agent per month; break-even needs about 76.4% utilisation (about 122 productive hours), roughly 6.4 points more.
**Check:** 0.7639 x 72,000 = Rs 55,000. Alternatively, a billing rate of 55,000 / 112 = Rs 491 per hour would break even at 70%.
**Caveats:** 100% utilisation is not achievable; most centres run well below it. Billing rate, shrinkage and attrition (HR levers) all move the answer.
**Likely follow-ups:** 1) *Options?* Lift utilisation, raise the rate, cut cost per agent through scheduling. 2) *Fix at a team of 200?* Loss of Rs 9.2 lakh a month.
**Common mistakes / traps:** Using paid hours as billable hours; comparing monthly cost to hourly rate; forgetting overheads in "fully loaded".

### Q34 ⭐⭐ 🟡 A marketplace cuts its seller commission from 15% to 12% to attract sellers. By how much must GMV grow to keep commission revenue unchanged?
Data: current take rate 15%; proposed take rate 12%; no change in other income.
**Asked at:** commonly asked (no company-specific report found); the numbers are invented for practice.
**What the interviewer is checking:** Whether you handle a rate cut with the break-even growth formula.
**Say this in the interview:** "Commission revenue is GMV times take rate. To hold it flat, GMV must grow by 15/12 minus 1, which is 25%."

**Definition in plain words:** GMV (gross merchandise value) is the total value of goods sold on the platform. Take rate is the platform's commission as a share of GMV. Commission revenue = GMV x take rate.
**Worked answer:**
1. Let current GMV = 100. Revenue now = 100 x 0.15 = 15.
2. New GMV needed = 15 / 0.12 = 125.
3. Growth = 125 / 100 - 1 = 25%.
**Result:** GMV must grow 25% just to stand still.
**Check:** 125 x 0.12 = 15. The cut is 3 points on 15, a 20% revenue loss, and 1 / 0.8 = 1.25.
**Caveats:** This is only break-even on commission; extra GMV also brings ad income, and costs such as logistics may scale with volume. The cut should be compared with seller response data.
**Likely follow-ups:** 1) *Why 25% and not 20%?* A 20% fall in rate needs a 25% rise in GMV to recover, as the base shrinks. 2) *How would you test it?* Pilot in one category and track seller count and GMV.
**Common mistakes / traps:** Answering 3 percentage points or 20%; ignoring costs that grow with volume.

### Q35 ⭐⭐ 🟡 The marketplace wants commission revenue to rise 25% while GMV grows only 10%. What take rate does it need?
Data: current GMV Rs 1,000 crore; current commission revenue Rs 120 crore (take rate 12%).
**Asked at:** commonly asked (no company-specific report found); the numbers are invented for practice.
**What the interviewer is checking:** Whether you rearrange revenue = GMV x take rate to solve for the rate.
**Say this in the interview:** "Target revenue is Rs 150 crore on GMV of Rs 1,100 crore, so the take rate must be 13.6%, up about 1.6 points."

**Definition in plain words:** Take rate = commission revenue / GMV.
**Worked answer:**
1. Target revenue = 120 x 1.25 = Rs 150 crore.
2. Target GMV = 1,000 x 1.10 = Rs 1,100 crore.
3. Needed take rate = 150 / 1,100 = 13.64%.
4. Relative rise in the rate = 13.64 / 12 - 1 = 13.6% (that is, 1.25 / 1.10 - 1).
**Result:** About 13.6% (up from 12%, roughly 1.6 percentage points).
**Check:** 1,100 x 0.1364 = Rs 150 crore.
**Caveats:** A higher rate can slow GMV growth, so the 10% may not hold. Ads, fees and delivery charges can raise the effective rate without a headline commission change.
**Likely follow-ups:** 1) *Other routes?* Sponsored listings, payment fees, seller services. 2) *Risk?* Sellers leaving for rivals.
**Common mistakes / traps:** Adding 25% and 10% points; mixing percentage points and percent; ignoring the link between rate and volume.

### Q36 ⭐⭐ 🟡 Is the ad channel below profitable? Compute ROAS and the break-even ROAS.
Data: ad spend Rs 10 lakh; attributed revenue Rs 40 lakh; contribution margin on that revenue before ad spend is 25%.
**Asked at:** commonly asked (no company-specific report found); ROAS and marketing efficiency are standard business-case topics (unverified); the numbers are invented for practice.
**What the interviewer is checking:** Whether you know ROAS is revenue-based and must be compared with a margin-based break-even.
**Say this in the interview:** "ROAS is 4. Break-even ROAS is 1 divided by the 25% margin, also 4, so the channel exactly breaks even; it is not profitable yet."

**Definition in plain words:** ROAS (return on ad spend) = attributed revenue / ad spend. Break-even ROAS = 1 / contribution margin.
**Worked answer:**
1. ROAS = 40 / 10 = 4.0.
2. Contribution before ads = 40 x 0.25 = Rs 10 lakh.
3. Profit after ads = 10 - 10 = Rs 0.
4. Break-even ROAS = 1 / 0.25 = 4.0.
**Result:** ROAS 4.0 equals break-even 4.0, so profit is Rs 0 (the ad paid for itself only).
**Check:** At ROAS 5, contribution Rs 12.5 lakh on Rs 10 lakh spend gives Rs 2.5 lakh profit.
**Caveats:** Attributed revenue may include sales that would have happened anyway, so true incremental ROAS can be lower. Repeat purchases (lifetime value) may justify a ROAS below break-even.
**Likely follow-ups:** 1) *Would you scale it?* Not on first-order data alone; check incrementality and repeat orders. 2) *How else to improve?* Lift margin or conversion.
**Common mistakes / traps:** Calling ROAS 4 "great" without the margin; confusing ROAS with ROI; using attributed revenue as incremental.

### Q37 ⭐⭐ 🟡 Should the company shut down product line C? Use the data below.
Data (Rs lakh per year): revenue 50; variable cost 35; allocated fixed cost 20 of which only 8 would disappear if the line were shut.
**Asked at:** commonly asked (no company-specific report found); the shutdown decision is a gap-fill finance case; the numbers are invented for practice.
**What the interviewer is checking:** Whether you use avoidable (relevant) costs instead of allocated costs.
**Say this in the interview:** "On the full-cost view the line loses Rs 5 lakh, but shutting it saves only Rs 8 lakh of fixed cost while losing Rs 15 lakh of contribution, so closing worsens profit by Rs 7 lakh. Keep it for now."

**Definition in plain words:** Allocated cost is a share of company overheads assigned to a line; avoidable cost disappears if the line closes. Only the avoidable part matters in the decision.
**Worked answer:**
1. Contribution = 50 - 35 = Rs 15 lakh.
2. Full-cost profit = 15 - 20 = -Rs 5 lakh (looks like a loss).
3. If shut: lose contribution Rs 15 lakh, save avoidable fixed Rs 8 lakh, net = -Rs 7 lakh.
4. The other Rs 12 lakh of allocated fixed cost stays and moves to other lines.
**Result:** Keep line C; it contributes Rs 7 lakh a year after its avoidable costs.
**Check:** Keeping C leaves company profit Rs 7 lakh higher than shutting it (Rs 15 lakh contribution kept versus Rs 8 lakh cost saved); the Rs 12 lakh of unavoidable fixed cost is paid either way.
**Caveats:** Revisit if the space or people freed could earn more elsewhere (opportunity cost), if C damages the brand, or if it drags other lines. Check if C supports sales of other products.
**Likely follow-ups:** 1) *When would you close it?* If avoidable costs exceeded contribution, or a better use for the resources exists. 2) *How to improve it?* Raise price, cut cost, reduce avoidable fixed costs.
**Common mistakes / traps:** Deciding on allocated profit; forgetting unavoidable costs remain; ignoring linkages with other products.

### Q38 ⭐⭐ 🟡 Two channels are being compared. Which is cheaper per paying user, and what else do you check before moving budget?
| Channel | Spend (Rs) | Installs | Install-to-paid |
|---|---|---|---|
| A | 5,00,000 | 2,000 | 10% |
| B | 3,00,000 | 1,200 | 5% |

**Asked at:** commonly asked (no company-specific report found); channel comparison is a typical marketing-analytics case (unverified); the numbers are invented for practice.
**What the interviewer is checking:** Whether you look past cost per install to cost per paying user.
**Say this in the interview:** "Both cost Rs 250 per install, but A converts 10% and B 5%, so A costs Rs 2,500 per paying user and B costs Rs 5,000. I would favour A, after checking quality and scale."

**Definition in plain words:** Cost per paying user = spend / (installs x install-to-paid rate). CPI is cost per install.
**Worked answer:**
1. Channel A: CPI = 5,00,000 / 2,000 = Rs 250. Paid users = 2,000 x 10% = 200. Cost per paid = 5,00,000 / 200 = Rs 2,500.
2. Channel B: CPI = 3,00,000 / 1,200 = Rs 250. Paid users = 1,200 x 5% = 60. Cost per paid = 3,00,000 / 60 = Rs 5,000.
**Result:** A is half the cost per paying user (Rs 2,500 versus Rs 5,000).
**Check:** Equal CPI means conversion alone decides: 5% versus 10% gives a factor of 2.
**Caveats:** Before moving budget, check retention and revenue per paying user (LTV, the total profit a user brings), whether the channel can scale without cost rising (marginal CAC, the cost of the next user), fraud or bot installs, attribution overlap, and the time window for conversion (B's paid rate may still be rising).
**Likely follow-ups:** 1) *Would you shut B?* Not at once; test whether B's users retain better. 2) *Sample size?* 60 paid users is small, so the 5% is uncertain.
**Common mistakes / traps:** Stopping at CPI; ignoring quality and scale; reading small samples as certain.

### Q39 ⭐⭐ 🟡 A food delivery platform adds Rs 10 to its delivery fee and orders fall 6%. Is this profitable, and how large a fall in orders can it tolerate?
Data: contribution is Rs 20 per order before the change; the whole Rs 10 goes to contribution; no other change.
**Asked at:** commonly asked (no company-specific report found); the food-delivery per-order case is described in an XLRI casebook snippet (unverified); the numbers are invented for practice.
**What the interviewer is checking:** Whether you compare new total contribution with old, and solve for the break-even fall in volume.
**Say this in the interview:** "Contribution per order goes from Rs 20 to Rs 30. With 6% fewer orders total contribution rises about 41%. Orders could fall by a third before profit drops."

**Definition in plain words:** Break-even fall in volume = 1 - old contribution / new contribution.
**Worked answer:**
1. Take 100 orders as the base. Old total = 100 x 20 = Rs 2,000.
2. New orders = 94. New contribution per order = Rs 30. New total = 94 x 30 = Rs 2,820.
3. Change = +Rs 820, or +41%.
4. Break-even fall = 1 - 20 / 30 = 33.3%.
**Result:** Profitable: +41% contribution; it tolerates a fall in orders of up to 33.3%.
**Check:** 67 orders x Rs 30 = Rs 2,010, about Rs 2,000.
**Caveats:** The 6% fall may be only the first-week reaction; watch orders per user, new-user conversion, and fixed costs per order (riders idle if orders fall). Real elasticity may differ by segment.
**Likely follow-ups:** 1) *Why only a 6% fall?* Check if it is a test period and control for promotions. 2) *Long-term risk?* Users switch apps.
**Common mistakes / traps:** Treating Rs 10 as a 50% rise in profit and stopping; ignoring cheaper rivals; forgetting that lost orders also lose the Rs 20 base.

### Q40 ⭐⭐ 🟡 A hotel can sell 60% of rooms at Rs 4,000 or cut the price to Rs 3,200 and sell 80%. Compare revenue per available room and profit per available room.
Data: variable cost Rs 800 per occupied room; fixed costs are the same in both cases.
**Asked at:** commonly asked (no company-specific report found); a hotel RevPAR case is a gap-fill pricing example; the numbers are invented for practice.
**What the interviewer is checking:** Whether you look at revenue and variable cost together, and notice a tie.
**Say this in the interview:** "Revenue per available room is higher at the low price, Rs 2,560 versus Rs 2,400, but the extra occupied rooms cost more, so profit per available room is Rs 1,920 in both cases."

**Definition in plain words:** RevPAR (revenue per available room) = price x occupancy. Profit per available room here = occupancy x (price - variable cost), since fixed costs are the same.
**Worked answer:**
1. Option 1 (Rs 4,000, 60%): RevPAR = 2,400. Variable cost = 0.6 x 800 = 480. Profit contribution = 1,920.
2. Option 2 (Rs 3,200, 80%): RevPAR = 2,560. Variable cost = 0.8 x 800 = 640. Profit contribution = 1,920.
**Result:** RevPAR Rs 2,400 versus Rs 2,560; profit per available room Rs 1,920 in both, a tie.
**Check:** Per occupied room: 4,000 - 800 = 3,200 x 0.6 = 1,920; 3,200 - 800 = 2,400 x 0.8 = 1,920.
**Caveats:** The tie means other factors decide: guests spending on food and spa (favours high occupancy), wear and staff stress (favours fewer rooms), brand image of discounting, and demand uncertainty. Revenue alone would mislead.
**Likely follow-ups:** 1) *Tie-breaker?* Add-on spend per guest; if above Rs 0 beyond the cost, fill the rooms. 2) *Risk of 80%?* Needs demand to be real.
**Common mistakes / traps:** Choosing on RevPAR only; forgetting variable costs; treating a tie as an error.

### Q41 ⭐⭐ 🟡 A delivery membership costs Rs 99 a month and gives free delivery. Is it profitable per member?
Data: non-members order 3 times a month and pay a delivery fee of Rs 40 that equals the delivery cost; members order 6 times and pay no fee; contribution per order before delivery is Rs 50. Assume all extra orders are caused by the membership.
**Asked at:** commonly asked (no company-specific report found); the membership-economics case is a common growth-case theme (unverified); the numbers are invented for practice.
**What the interviewer is checking:** Whether you compare a member's monthly contribution with a non-member's.
**Say this in the interview:** "A member brings Rs 159 a month against Rs 150 for a non-member, so the programme gains about Rs 9 per member, only just profitable."

**Definition in plain words:** Compare monthly contribution per customer with and without the membership; the membership is worthwhile if the member figure is higher.
**Worked answer:**
1. Non-member: 3 x 50 = 150 before delivery; delivery fee 40 equals delivery cost, so delivery nets zero. Contribution = Rs 150.
2. Member: 6 x 50 = 300 before delivery; delivery cost 6 x 40 = 240 and no fee paid; membership fee +99. Contribution = 300 - 240 + 99 = Rs 159.
3. Gain = 159 - 150 = Rs 9 per member per month.
**Result:** Profitable by Rs 9 a month per member, about 6% better.
**Check:** Each member order gives 50 - 40 = Rs 10, so contribution = 10 x orders + 99. At 5 orders it is Rs 149 (below 150); the break-even is about 5.1 orders a month.
**Caveats:** The result depends on the assumption that all extra orders are caused by the plan; if some members would have ordered 6 times anyway, the programme loses money (those members would simply have received free delivery they did not need). Also check churn and cannibalised fees.
**Likely follow-ups:** 1) *What if members order only 5 times?* Contribution Rs 149, a loss of Rs 1. 2) *How to improve?* Minimum order value, raise fee, cap free deliveries.
**Common mistakes / traps:** Counting the Rs 99 as pure profit; ignoring that free delivery has a real cost; assuming self-selection does not exist.

### Q42 ⭐⭐ 🟡 Two cities are candidates for the next launch. Which would you launch first on these numbers, and what would change your mind?
| | City A | City B |
|---|---|---|
| Monthly orders at maturity | 5 lakh | 3 lakh |
| Contribution per order | Rs 25 | Rs 40 |
| Launch cost | Rs 3 crore | Rs 1.5 crore |

**Asked at:** commonly asked (no company-specific report found); market-entry cases are reported for Fractal and Mu Sigma on prep sites (unverified); the numbers are invented for practice.
**What the interviewer is checking:** Whether you compare payback and return per rupee, not only size.
**Say this in the interview:** "B first: it earns Rs 1.2 crore a month at maturity on Rs 1.5 crore of launch cost, paying back in about 1.25 months at maturity, versus 2.4 months for A. A is bigger, so it is the second launch."

**Clarify first:** How long does each city take to reach maturity? Are these the same ramp-up? Is cash limited? Any competitor in each?
**Structure:** Size (monthly contribution), speed (payback), risk (ramp-up, competition), strategy (learning, brand value, logistics reuse).
**What I would check, in order:**
1. Monthly contribution at maturity: A = 5,00,000 x 25 = Rs 1.25 crore; B = 3,00,000 x 40 = Rs 1.2 crore.
2. Payback at maturity: A = 3 / 1.25 = 2.4 months; B = 1.5 / 1.2 = 1.25 months.
3. Yearly return per rupee: A = 15 / 3 = 5.0 times; B = 14.4 / 1.5 = 9.6 times.
4. Time to reach maturity, then adjust payback (a slower ramp-up hurts both).
**If the data shows...:** B reaches maturity slower, or the contribution figure of Rs 40 is unproven: A's volume may win. If cash is limited, B wins; if cash is available, launch both and A larger.
**Numeric work (if data given):** Results above. A earns Rs 5 lakh more a month than B (Rs 1.25 crore versus Rs 1.2 crore); B costs half.
**Recommendation:** Launch B first for faster payback and lower risk, A next; then track actual orders and contribution against these plan numbers.
**Likely follow-ups:** 1) *What if A had far more growth potential?* A longer-term upside could justify A. 2) *Unit-economics risk?* Contribution per order often falls with competition.
**Common mistakes / traps:** Picking A because the order volume is larger; ignoring ramp-up time; using maturity numbers as month-1 numbers.

### Q43 ⭐⭐ 🟡 A new low-price variant is launched. How much extra contribution does it create after cannibalisation?
Data: 10,000 units of the new variant sold at Rs 150 contribution each; 40% of these buyers would otherwise have bought the premium variant that earns Rs 300 contribution.
**Asked at:** commonly asked (no company-specific report found); the numbers are invented for practice.
**What the interviewer is checking:** Whether you net out the contribution lost from premium customers who trade down.
**Say this in the interview:** "The new variant earns Rs 15 lakh, but 4,000 buyers would have paid Rs 300 for the premium, which loses Rs 12 lakh. Net gain is Rs 3 lakh."

**Definition in plain words:** Cannibalisation is when a new product takes sales from your own existing product. Incremental contribution = new contribution - contribution lost on the product it replaced.
**Worked answer:**
1. New variant contribution = 10,000 x 150 = Rs 15,00,000.
2. Cannibalised buyers = 10,000 x 40% = 4,000.
3. Lost premium contribution = 4,000 x 300 = Rs 12,00,000.
4. Net = 15,00,000 - 12,00,000 = Rs 3,00,000.
**Result:** Net extra contribution Rs 3 lakh (20% of the headline Rs 15 lakh).
**Check:** 6,000 truly new buyers x 150 = Rs 9 lakh, minus the downgrade loss on 4,000 x 150 = Rs 6 lakh, gives Rs 3 lakh. Break-even cannibalisation is 50% (5,000 x 300 = 15 lakh).
**Caveats:** The 40% is an estimate from survey or test data; a low-price variant may also win customers from rivals or lift brand reach; the premium unit mix may differ.
**Likely follow-ups:** 1) *What if cannibalisation were 60%?* Loss Rs 18 lakh against Rs 15 lakh: net -Rs 3 lakh. 2) *How to measure?* A/B test by region.
**Common mistakes / traps:** Reporting Rs 15 lakh; subtracting Rs 150 instead of Rs 300 per cannibalised buyer (the Rs 150 they still bring is already inside the Rs 15 lakh); treating the 40% as certain.

### Q44 ⭐⭐ 🟡 A bot handles part of support tickets. Compute monthly saving versus the all-human baseline.
Data: 1,00,000 tickets a month; human cost Rs 80 per ticket; the bot takes 40% of tickets at Rs 15 each; it fully resolves 60% of those; the unresolved ones go to a human at Rs 80 on top of the bot cost.
**Asked at:** commonly asked (no company-specific report found); the numbers are invented for practice.
**What the interviewer is checking:** Whether you count the bot cost on all bot tickets and the human cost on the escalations.
**Say this in the interview:** "Baseline is Rs 80 lakh. With the bot it is Rs 66.8 lakh, a saving of Rs 13.2 lakh a month, about 16.5%."

**Definition in plain words:** Saving = baseline cost - new cost. New cost = bot cost on bot-handled tickets + human cost on everything the human finally handles.
**Worked answer:**
1. Baseline = 1,00,000 x 80 = Rs 80,00,000.
2. Bot tickets = 40,000; bot cost = 40,000 x 15 = Rs 6,00,000.
3. Unresolved = 40,000 x 40% = 16,000; human cost = 16,000 x 80 = Rs 12,80,000.
4. Other tickets (human only) = 60,000 x 80 = Rs 48,00,000.
5. New total = 6,00,000 + 12,80,000 + 48,00,000 = Rs 66,80,000.
6. Saving = 80,00,000 - 66,80,000 = Rs 13,20,000.
**Result:** Saving Rs 13.2 lakh a month (16.5%).
**Check:** Per bot ticket: bot saves 80 on the 24,000 resolved ones, net 65 each = Rs 15.6 lakh; on the 16,000 unresolved it adds Rs 15 each = -Rs 2.4 lakh; total Rs 13.2 lakh.
**Caveats:** Customer satisfaction can fall if the bot frustrates users; escalated tickets may be harder and costlier; set-up and maintenance cost is excluded.
**Likely follow-ups:** 1) *How to raise the saving?* Raise resolution from 60% or bot share above 40%. 2) *Which guard-rail?* CSAT (customer satisfaction score) and repeat contacts.
**Common mistakes / traps:** Charging Rs 80 on all bot tickets; ignoring the bot's Rs 15 on unresolved ones; counting savings before checking quality.

### Q45 ⭐⭐ 🟡 Customer-segment profitability: compute the profit for each segment per 100 customers and say where you would put the next marketing rupee.
| Segment | Share of customers | Revenue per customer | Cost to serve per customer |
|---|---|---|---|
| X | 40% | Rs 1,000 | Rs 600 |
| Y | 40% | Rs 800 | Rs 850 |
| Z | 20% | Rs 3,000 | Rs 1,200 |

**Asked at:** commonly asked (no company-specific report found); the numbers are invented for practice.
**What the interviewer is checking:** Whether you weight by share and see that an average hides a loss-making segment.
**Say this in the interview:** "Per 100 customers X earns Rs 16,000, Y loses Rs 2,000 and Z earns Rs 36,000. Z is 20% of customers but 72% of the profit, so the next rupee goes to finding more Z-like customers, while I fix or stop serving Y."

**Definition in plain words:** Segment profit = number of customers x (revenue - cost to serve) per customer.
**Worked answer:**
1. X: 40 customers x (1,000 - 600 = 400) = Rs 16,000.
2. Y: 40 x (800 - 850 = -50) = -Rs 2,000.
3. Z: 20 x (3,000 - 1,200 = 1,800) = Rs 36,000.
4. Total = 16,000 - 2,000 + 36,000 = Rs 50,000, or Rs 500 per customer.
5. Margin per customer: X 40%, Y about -6%, Z 60%.
**Result:** X Rs 16,000, Y -Rs 2,000, Z Rs 36,000 per 100 customers; total Rs 50,000.
**Check:** Revenue = 40,000 + 32,000 + 60,000 = Rs 1,32,000; cost = Rs 82,000; difference Rs 50,000.
**Caveats:** Cost to serve may include allocated overheads; Z may be hard to find or already saturated, so marginal returns may differ from the average. Check lifetime value and churn by segment.
**Likely follow-ups:** 1) *What would you do with Y?* Raise price, cut service cost or steer to self-service. 2) *Check that Z is scalable?* Test acquisition cost for lookalike audiences.
**Common mistakes / traps:** Looking at revenue only; spending on the largest segment; ignoring that average profit hides a loss-making group.

### Q46 ⭐⭐ 🟡 Retention or acquisition: which of the two options grows the user base more in steady state?
Data: 4,000 new users a month and 4% monthly churn give a steady 100,000 users. Option 1 cuts churn to 3%. Option 2 raises acquisition by 25%. Assume steady state is reached for each.
**Asked at:** commonly asked (no company-specific report found); retention-versus-acquisition appears on prep sites as a growth theme (unverified); the numbers are invented for practice.
**What the interviewer is checking:** Whether you use the steady-state formula users = new users / churn rate.
**Say this in the interview:** "Steady state users equal monthly new users divided by monthly churn. Cutting churn to 3% gives 1,33,333 users, up 33%; raising acquisition by 25% gives 1,25,000. Retention wins."

**Definition in plain words:** At steady state, users joining equal users leaving, so new users = churn x users. Hence users = new users / churn.
**Worked answer:**
1. Today: 4,000 / 0.04 = 1,00,000.
2. Option 1: 4,000 / 0.03 = 1,33,333 (+33.3%).
3. Option 2: 5,000 / 0.04 = 1,25,000 (+25%).
**Result:** Option 1 (churn to 3%) gives about 1,33,000 users, versus 1,25,000 for Option 2.
**Check:** At 3% churn, leavers = 0.03 x 1,33,333 = 4,000, matching arrivals.
**Caveats:** The model assumes constant churn; reaching steady state takes time (about 1 / churn months, so 33 months at 3%), so acquisition shows results faster. Cost of each option is not given; a 1-point churn cut may cost more than 25% more marketing. Newer users usually churn faster than older ones.
**Likely follow-ups:** 1) *Which is faster?* Acquisition. 2) *What would change your mind?* Cost per point of churn reduction versus cost per new user.
**Common mistakes / traps:** Adding the percentages; ignoring the time to reach the steady state; ignoring cost.

### Q47 ⭐⭐ 🟡 Your company's price is 10% below a competitor's, and the competitor drops its price by 10%. How do you decide whether to follow?
**Asked at:** commonly asked (no company-specific report found); competitive-pricing responses are a standard pricing-case theme on prep sites (unverified).
**What the interviewer is checking:** Whether you decide on economics and customer behaviour, not reflex.
**Say this in the interview:** "I would compare the profit from following with the profit from holding, using my margin and how many customers would switch. The price gap has mostly closed (to about 1% or even zero, depending on how the 10% is read), so I check who is actually at risk."

**Clarify first:** What is our margin, how loyal are customers, how differentiated is the product, and can the competitor sustain the cut?
**Structure:** Current gap (the wording is ambiguous, so I would state my reading aloud): if we sell at 100 and the competitor at 110, a 10% cut gives them 99, so they are now about 1% cheaper than us. If instead our price is exactly 10% below theirs (we are 90, they are 100 before the cut), their cut to 90 makes the prices equal. Options: hold, match, partially match, or respond with value (bundle, service).
**What I would check, in order:** (1) Our contribution margin per unit. (2) The switching rate seen in past competitor price moves. (3) Which segments are price-sensitive. (4) The competitor's margin and cash position. (5) Break-even volume loss of holding versus the cost of matching.
**If the data shows...:** Few customers switch and our margin is thin: hold. Many switch and margin is healthy: match for the sensitive segment only. Competitor is subsidising: wait, since the war is not sustainable.
**Numeric work (if data given):** Illustrative: price 100, variable cost 60, contribution 40. Matching a 10% cut gives contribution 30; needed volume rise to break even = 40 / 30 - 1 = 33%. Holding (40 per unit) beats matching (30 per unit) unless we lose more than 25% of our volume (1 - 30/40).
**Recommendation:** Do not follow automatically; test in a few cities or segments, and compare with a price-war cost.
**Likely follow-ups:** 1) *Risk of matching?* A price war that lowers margins for everyone. 2) *Alternatives?* Loyalty offers or bundles.
**Common mistakes / traps:** Matching by reflex; ignoring that you were previously cheaper; ignoring cost and cash position.

### Q48 ⭐⭐ 🟡 How do you estimate price elasticity from historical sales data, and what can make the estimate wrong?
**Asked at:** commonly asked (no company-specific report found); pricing and promo-model work is mentioned for Tiger Analytics on a prep-platform page (unverified).
**What the interviewer is checking:** Whether you know the basic method and its pitfalls, especially confounding.
**Say this in the interview:** "I would run a regression (fit a line through the data) of the log of units on the log of price, controlling for season, promotions and competitor prices; the price coefficient is the elasticity. The main risk is that price changes were not random, so the estimate can be biased."

**Explain simply:**
- Price elasticity = % change in quantity / % change in price. Elasticity -1.5 means a 10% price rise cuts demand 15%.
- Simple method: take two periods with only the price changed, compute % change in units divided by % change in price.
- Better method: a log-log regression (log units on log price) with controls for seasonality, promotions, competitor price and stock-outs; the slope is the elasticity.
- Mini-example (assumed): price rises from Rs 100 to Rs 110 (+10%) and units fall from 1,000 to 850 (-15%); elasticity = -15 / 10 = -1.5.
- What can go wrong: other things changed at the same time (festival, ad campaign); the price was cut when demand was weak (reverse causality); stock-outs; little price variation in the data; elasticity differs by segment and over time; very short-term reactions are not long-term ones.
- Practice: take a month of daily sales and price and fit the slope in Excel on logs.

**Likely follow-ups:** 1) *What is a better design?* A randomised price test. 2) *Is elasticity constant?* No, it changes along the demand curve.
**Common mistakes / traps:** Comparing two periods without controls; mixing up correlation and causation; using one global number for all products.

### Q49 ⭐⭐ 🟡 A growth channel gets harder as spend rises. Compute average and marginal CAC and say whether to spend the second tranche.
Data: Rs 10 lakh spend brings 1,000 users; Rs 20 lakh in total brings 1,600 users; LTV per user is Rs 1,500.
**Asked at:** commonly asked (no company-specific report found); the numbers are invented for practice.
**What the interviewer is checking:** Whether you decide on marginal CAC, not average CAC.
**Say this in the interview:** "Average CAC at Rs 20 lakh is Rs 1,250, below the LTV of Rs 1,500, so it looks fine. But the second tranche cost Rs 10 lakh for 600 users, a marginal CAC of about Rs 1,667, above the LTV. I would not spend it."

**Definition in plain words:** Average CAC = total spend / total users. Marginal CAC = extra spend / extra users. LTV (lifetime value) is the contribution a user brings over their life; assume it is a contribution figure here.
**Worked answer:**
1. First tranche CAC = 10,00,000 / 1,000 = Rs 1,000.
2. Average CAC at Rs 20 lakh = 20,00,000 / 1,600 = Rs 1,250.
3. Marginal CAC of the second tranche = 10,00,000 / (1,600 - 1,000) = Rs 1,667.
4. Value created: first tranche 1,000 x 1,500 - 10 lakh = +Rs 5 lakh; second tranche 600 x 1,500 - 10 lakh = -Rs 1 lakh.
**Result:** Average CAC Rs 1,250, marginal CAC about Rs 1,667; the second tranche loses about Rs 1 lakh.
**Check:** Total = +5 - 1 = Rs 4 lakh, equal to 1,600 x 1,500 - 20 lakh.
**Caveats:** If LTV is revenue and not contribution, it is overstated. A smaller partial tranche (spend until marginal CAC equals Rs 1,500) may still be profitable. LTV is an estimate.
**Likely follow-ups:** 1) *Would you stop at Rs 10 lakh?* Spend a bit more only while marginal CAC is below Rs 1,500, using a test. 2) *Other uses of the money?* A channel with lower marginal CAC.
**Common mistakes / traps:** Deciding on average CAC; mixing revenue LTV with cost; ignoring payback time.

### Q50 ⭐⭐ 🟡 A company's revenue is up 40% but its operating margin is falling. Is that a problem? Give hypotheses and the data you would pull.
**Asked at:** commonly asked (no company-specific report found); growth-versus-margin diagnosis appears in case-interview prep material (unverified).
**What the interviewer is checking:** Whether you look at profit in rupees and at the causes of the fall, not at one ratio.
**Say this in the interview:** "Not necessarily a problem if rupee profit is still rising and the spend is investment; it is a problem if growth is being bought with discounts or if costs are growing faster than revenue. I would split the margin fall into price, mix and cost lines."

**Clarify first:** What are the margin figures, and is it a planned investment phase? Is profit in rupees up or down? Over what period?
**Structure:**
- Illustration (assumed): revenue 100 to 140, margin 15% to 12%. Operating profit goes from 15 to 16.8 (+12%), so rupee profit still rises, but at the old margin it would be Rs 21, so Rs 4.2 is leaking.
- H1: price and discounts (growth through promotions).
- H2: mix shift to low-margin products or channels.
- H3: cost lines rising faster than revenue (marketing, delivery, staff, rent).
- H4: scale investments not yet paid off (new cities, hiring ahead of demand).
- H5: one-off or accounting changes.
**What I would check, in order:** (1) Revenue and cost lines as a % of revenue, year on year. (2) Price versus volume bridge. (3) Mix by product, channel, region. (4) Contribution margin per order or unit. (5) Cohort quality of new customers.
**If the data shows...:** Costs are one-off or investment with improving unit economics: acceptable. Contribution per unit is falling: unhealthy growth, so fix pricing and discounts. A few regions or channels drag margin: fix or exit them.
**Recommendation:** Judge by rupee operating profit, contribution per unit and payback of the new spend; set a margin floor for further growth.
**Likely follow-ups:** 1) *When is a falling margin fine?* When unit contribution is stable and fixed costs are building ahead of demand. 2) *First chart?* Cost lines as % of revenue over time.
**Common mistakes / traps:** Calling any margin fall bad (or good); looking at percent but not rupees; skipping the mix check.

### Q51 ⭐⭐ 🟡 A UPI app earns no fee on payments. How can it become profitable, and which metrics would you track to know it is getting there?
**Asked at:** commonly asked (no company-specific report found); PhonePe is listed in research/interview_processes.md as a payments-company interview pattern (prep-site level, unverified).
**What the interviewer is checking:** Whether you separate the free payment "hook" from the products that actually earn money, and can name unit-economics metrics.
**Say this in the interview:** "Payments are the front door, not the shop. I would earn on things users do after they trust the app (loans, insurance, investments, merchant tools, ads), and track revenue per active user against cost per active user."
**Clarify first:** Is the zero fee a rule we cannot change (assume yes, a regulatory or market norm; unverified)? Do we have a user base to cross-sell? Time horizon (3 years)?
**Structure:**
- Revenue: (1) lending and credit-on-UPI, where a partner bank pays a commission; (2) insurance and mutual-fund distribution; (3) merchant services (soundbox, the small speaker that announces payments to shopkeepers; billing software; working-capital loans); (4) ads and brand offers; (5) bill-pay and recharge commissions.
- Cost: payment processing and bank charges, fraud and support, cashback, marketing.
**What I would check, in order:** monthly active users and their transactions; share of users who ever take a second product; revenue per user by product; cost to serve per user; payback on acquisition cost.
**Numeric work (assumed, approximate, unverified):** 1 crore monthly active users. Loans: 3% take a Rs 20,000 loan a year, partner pays 2% = Rs 400, so 3 lakh x Rs 400 = Rs 12 crore, about Rs 12 per user a year. Add assumed Rs 8 (insurance, funds), Rs 6 (ads), Rs 25 (merchant services) = about Rs 51 per user a year. If cost to serve is Rs 4 a month = Rs 48 a year, the app is only just positive. Lever size matters more than the exact figures.
**If the data shows...:** high usage but under 2% taking any second product means the cross-sell is weak, fix product fit before buying users. Revenue per user above cost per user and rising means scale will make profit.
**Recommendation:** Track revenue per monthly active user minus cost per monthly active user, share of users with 2+ products, 30/90-day retention, cashback as a percentage of revenue, and CAC payback in months. Aim for contribution positive per user before scaling marketing.
**Likely follow-ups:** 1) *Which lever first?* The one with highest revenue per user and least regulatory risk, usually merchant services. 2) *Why not charge a small fee?* Users switch to a free rival.
**Common mistakes / traps:** Counting payment volume (the total rupees moved) as revenue; ignoring that cashback can exceed all earnings; listing ideas with no sizing.

### Q52 ⭐⭐ 🟡 A SaaS growth case: new-logo growth has slowed but net revenue retention is 115%. Where do you put effort, and why?
**Asked at:** commonly asked (no company-specific report found); SaaS retention-bridge cases appear in prep-site material (unverified).
**What the interviewer is checking:** Whether you can read net revenue retention (NRR) and decide between new customers and existing customers.
**Say this in the interview:** "NRR of 115% means existing customers alone grow revenue 15% a year, so the base is healthy. I would first find out why new logos slowed, then put most effort on expansion while fixing the top of the funnel."
**Clarify first:** What is "new logo"? A new paying customer. NRR (net revenue retention) = revenue now from last year's customers divided by their revenue last year, including upgrades, downgrades and cancellations. Is the slowdown in leads, conversion or deal size? What is gross retention?
**Structure:** NRR = 100% + expansion - contraction - churn. Example (assumed): 100 + 22 - 2 - 5 = 115. New-logo slowdown: market saturation, weaker ideal-customer fit, sales capacity, pricing, competition.
**What I would check, in order:** gross revenue retention (excluding upgrades); expansion by segment; new-logo funnel (leads, win rate, sales cycle); CAC payback for new versus expansion; concentration (are a few large accounts driving the 115%?).
**If the data shows...:** expansion concentrated in a few big accounts means NRR is fragile, so do not relax. Broad expansion with low churn means invest in upsell and customer success. Slowdown from weak leads means fix marketing or ideal-customer targeting.
**Numeric work:** Starting revenue 1,000 with zero new logos becomes 1,150, a 15% rise from the base alone.
**Recommendation:** Split effort roughly toward expansion now (cheapest growth) while repairing the funnel, since without new logos the expansion pool stops growing in a couple of years. Measure NRR, gross retention, new-logo count and CAC payback quarterly.
**Likely follow-ups:** 1) *Is 115% good?* Generally strong, but it depends on segment and is unverified as a benchmark. 2) *Why gross retention too?* NRR can hide churn behind upsell.
**Common mistakes / traps:** Reading NRR as growth including new logos; ignoring churn hidden by expansion; abandoning acquisition entirely.

### Q53 ⭐⭐ 🟡 Subscription pricing: monthly plan Rs 500 versus annual plan Rs 4,800. Compare first-year revenue per subscriber under 6% monthly churn.
Data: monthly plan Rs 500 a month, with 6% of the remaining subscribers cancelling each month (churn applied from month 2 onward); annual plan Rs 4,800 paid upfront with no cancellation in year one.
**Asked at:** commonly asked (no company-specific report found); pricing cases listed on prep sites (unverified).
**What the interviewer is checking:** Expected revenue under churn, not just list price times 12.
**Say this in the interview:** "Churn cuts the monthly plan to about Rs 4,367 a subscriber in year one, so the annual plan earns about Rs 433 more, paid upfront."
**Definition in plain words:** Expected first-year revenue per starting subscriber = sum over months of Rs 500 x share still subscribed. Month 1 share is 1; each later month is 0.94 times the previous one.
**Worked answer:**
1. Shares still paying in months 1 to 12: 1, 0.94, 0.884, 0.831, 0.781, 0.734, 0.690, 0.648, 0.610, 0.573, 0.539, 0.506.
2. Their sum = (1 - 0.94^12) / 0.06 = 8.735 paying months.
3. Monthly revenue = 500 x 8.735 = Rs 4,367.
4. Annual = Rs 4,800 paid at once.
**Result:** Monthly Rs 4,367 (without churn it would be Rs 6,000); annual Rs 4,800, which is Rs 433 (about 9.9%) higher.
**Check:** The two plans tie at a monthly churn of about 4.2%; above that annual wins on first-year revenue. About half (50.6%) of subscribers remain at month 12.
**Caveats:** Annual is a 20% discount versus Rs 6,000, so fewer people may pick it; lifetime value beyond year one differs (monthly subscribers who stay keep paying); cash upfront has value; refunds and renewal rates matter.
**Likely follow-ups:** 1) *Which would you push?* Annual for cash and retention, if conversion does not fall too far. 2) *What if churn is 3%?* Monthly rises above Rs 5,000, beating the annual plan.
**Common mistakes / traps:** Multiplying 500 x 12 and ignoring churn; applying churn in month 1; comparing only list price.

### Q54 ⭐⭐ 🔴 A quick-commerce company is losing money on every order. List the levers to reach positive contribution per order, size each with an assumed number, and say which two you would pull first.
**Asked at:** commonly asked (no company-specific report found); the question comes from quick-commerce unit-economics articles and prep sites (figures conflict, unverified).
**What the interviewer is checking:** Per-order unit economics (contribution = revenue per order minus variable costs per order) and prioritisation.
**Say this in the interview:** "I would build the per-order P&L, then pull the two biggest, fastest levers: raise basket size and add a small delivery or handling fee."
**Clarify first:** Contribution excludes fixed costs such as rent of dark stores (small warehouses) and head office. Which city and order mix? Is the loss in revenue or cost?
**Structure:** Revenue per order (product margin, ads, fees) minus variable cost (picking and packing, rider, discounts, payment, packaging, wastage).
**What I would check, in order:** per-order P&L by city and store; average order value (AOV) distribution; rider cost per order; discount share; orders per rider per hour.
**Numeric work (all assumed, illustrative):** AOV Rs 450. Product margin 18% = Rs 81; ads 3% = Rs 13.5; revenue Rs 94.5. Costs: picking Rs 25, rider Rs 40, discounts Rs 15, payment Rs 4, packaging Rs 5, wastage Rs 4, store variable Rs 15 = Rs 108. Contribution = Rs -13.5 per order.
Levers (assumed): (1) raise AOV by Rs 60 via a free-delivery threshold: +Rs 10.8; (2) Rs 20 fee on half of orders: +Rs 10; (3) ads up 1.5 points: +Rs 6.75; (4) rider batching: +Rs 5; (5) cut discounts: +Rs 8.
**If the data shows...:** low AOV means levers 1 and 2; high discount share means lever 5; rider idle time means batching and density.
**Recommendation:** Pull levers 1 and 2 first: +Rs 20.8 takes contribution to about +Rs 7.3 per order, fastest and under our control. Measure contribution per order weekly, AOV, orders per store per day, and repeat rate, watching that fees do not hurt retention.
**Likely follow-ups:** 1) *Why not cut rider pay?* It hurts supply. 2) *When does scale help?* Higher orders per store dilute fixed cost.
**Common mistakes / traps:** Mixing fixed and variable cost; pulling all levers at once with no test; ignoring customer loss from fees.

### Q55 ⭐⭐ 🔴 A cab aggregator offers drivers a flat Rs 500 a day instead of a 20% commission. Evaluate this from the driver's and the platform's side.
Data: a typical driver generates Rs 3,000 of fares a day; commission model takes 20%.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Break-even thinking and who self-selects into a flat fee.
**Say this in the interview:** "For the typical driver, flat Rs 500 beats 20% by Rs 100 a day; the break-even is Rs 2,500 of fares. The risk is that only high earners pick it."
**Clarify first:** Is the Rs 500 a subscription the driver pays, regardless of trips? Optional or mandatory? Do drivers work other apps?
**Structure:** Driver view (take-home, risk, incentive), platform view (revenue per driver, mix, supply).
**What I would check, in order:** distribution of daily fares per driver; share above Rs 2,500; hours worked; platform revenue per driver under each model; driver churn.
**Numeric work:** Commission: 20% x 3,000 = Rs 600, driver keeps Rs 2,400. Flat: pays Rs 500, keeps Rs 2,500, a gain of Rs 100 a day (4.2%). Break-even: 500 / 0.20 = Rs 2,500. Fare Rs 1,500 gives commission Rs 300 (flat costs Rs 200 more); fare Rs 4,000 gives Rs 800 (flat saves Rs 300).
**If the data shows...:** most drivers above Rs 2,500 and choosing flat means platform revenue drops and the high-earner subsidy is large; mostly low earners means platform gains but drivers leave.
**Recommendation:** Pilot as optional in one city, measure platform revenue per driver, hours supplied and trips per driver. Likely drivers gain an incentive to drive more (each extra fare is fully theirs), which helps supply; platform loses Rs 100 per average driver per day, so it must be repaid by more trips.
**Likely follow-ups:** 1) *Adverse selection?* Yes, high earners opt in, low earners stay. 2) *Fix?* A tiered fee or a cap.
**Common mistakes / traps:** Comparing only at the average; forgetting the platform's revenue falls; ignoring that a flat fee is a cost on slow days.

### Q56 ⭐⭐ 🔴 How would you decide whether to enter the 10-minute grocery delivery market in a new city? Give a structure, the numbers you need and a decision rule.
**Asked at:** commonly asked (no company-specific report found); market-entry cases appear at Mu Sigma and Fractal per prep-site material in the sources file (unverified).
**What the interviewer is checking:** A structured entry test with explicit numbers and a go or no-go rule.
**Say this in the interview:** "I would test demand, store economics, competition and cash needed, and go only if a store can break even within a set number of months."
**Clarify first:** Is this our first city or are we expanding? Budget and time limit? Own dark stores or partners?
**Structure:** Market (households, income, density); demand (users, order frequency); store economics; competition; capability and capital.
**What I would check, in order:** population density and affluent households in delivery radius; competitor presence; rider supply and rents; contribution per order in similar cities.
**Numeric work (assumed, illustrative):** 4 lakh reachable households; 10% active users x 4 orders a month = 1.6 lakh orders a month = about 5,333 a day. Dark store fixed cost Rs 5 lakh a month = Rs 16,667 a day; contribution Rs 25 an order, so break-even is about 667 orders a day per store. The city supports about 8 stores at break-even volume (5,333 / 667), or about 5 stores running at 1,000 orders a day.
**If the data shows...:** density supports 5 or more stores at break-even volume within 6 months means go; one or two stores only, or negative contribution per order, means no-go or later.
**Recommendation:** Decision rule: enter if (a) contribution per order is positive at maturity, (b) the store reaches break-even orders within about 6 to 9 months, (c) total cash needed fits the budget and pays back within the approved period. Pilot 2 to 3 stores in dense areas first.
**Likely follow-ups:** 1) *Biggest risk?* Competitor discounting. 2) *Biggest number to firm up?* Orders per store per day.
**Common mistakes / traps:** Guessing city size only; ignoring density; no decision threshold.

### Q57 ⭐⭐ 🔴 Two bundled items versus separate pricing: which pricing earns most profit?
Data: customer 1 values item A at Rs 100 and item B at Rs 40; customer 2 values A at Rs 40 and B at Rs 100; cost Rs 20 per item. Options: price each item at Rs 100, each at Rs 40, or sell only a bundle at Rs 140.
**Asked at:** commonly asked (no company-specific report found); bundling is a gap-fill topic in the sources file.
**What the interviewer is checking:** Willingness-to-pay logic and why bundling helps when tastes differ.
**Say this in the interview:** "The bundle at Rs 140 earns Rs 200, versus Rs 160 for each at Rs 100 and Rs 80 for each at Rs 40."
**Definition in plain words:** A customer buys if the price is at or below their value. Profit = revenue minus Rs 20 per item sold.
**Worked answer:**
1. Each at Rs 100: customer 1 buys only A, customer 2 only B. Revenue 200, cost 40, profit Rs 160.
2. Each at Rs 40: both buy both items. Revenue 4 x 40 = 160, cost 80, profit Rs 80.
3. Bundle at Rs 140: each customer values the pair at Rs 140, so both buy. Revenue 280, cost 80, profit Rs 200.
**Result:** Bundle Rs 200 > Rs 160 > Rs 80.
**Check:** Bundle works because the two customers' values are mirror images, so total value is equal (Rs 140) for both.
**Caveats:** Needs opposite tastes; the bundle sells items customers do not want (cost still incurred); real values are unknown; only two customers.
**Likely follow-ups:** 1) *What if customer 1 valued both at Rs 100?* The bundle advantage shrinks. 2) *Max bundle price?* Rs 140.
**Common mistakes / traps:** Forgetting cost on both bundle items; assuming both buy at Rs 100.

### Q58 ⭐⭐ 🔴 A car manufacturer's profit fell 40% year on year. Structure your diagnosis and say what you would check outside the company.
**Asked at:** one AmbitionBox snippet reports a "car manufacturer profit fell 40%" question (mapping to a specific company unverified; prep-site level).
**What the interviewer is checking:** A MECE tree (mutually exclusive, collectively exhaustive: no overlaps, no gaps) covering revenue and cost, and the external factors.
**Say this in the interview:** "Profit = volume x (price - unit cost) - fixed cost. I would find which part moved, then check the market outside."
**Clarify first:** Over what period? Is revenue also down? Which segments and regions? Any one-off items?
**Structure:** Profit = revenue - cost. Revenue: units x price x model mix. Cost: materials, labour, warranty, marketing, fixed overhead, financing, exchange rates. Internal versus external.
**What I would check, in order:** profit bridge year on year (volume, price, mix, cost); by model and region; incentives and discounts; input prices; dealer stock.
**Numeric work (assumed):** Revenue 10,000 crore, profit 1,000 crore. A 40% fall = Rs 400 crore. That equals 4 points of margin: a cost increase of just 4% of revenue is enough.
**If the data shows...:** volume down with price steady means a demand problem; revenue steady with cost up means raw materials or supplier; price down with volume steady means discounting or competition.
**Outside the company:** economic slowdown and interest rates (car loans); commodity (steel, aluminium) and chip supply; exchange rates; fuel prices; shift to electric vehicles; emission and safety regulation; competitor launches and price cuts; taxes and subsidies.
**Recommendation:** Bridge first, then match each driver to an external fact; fix the biggest controllable one (cost or mix), and measure monthly profit per vehicle.
**Likely follow-ups:** 1) *First data request?* Profit bridge by model. 2) *One-off?* Check write-offs and recalls.
**Common mistakes / traps:** Jumping to marketing; ignoring external factors; not quantifying.

### Q59 ⭐⭐ 🔴 How would you measure the true return on a discount promotion, separating incremental orders from orders that would have happened anyway?
**Asked at:** commonly asked (no company-specific report found); promo-effectiveness work is reported at Tiger Analytics via one prep page (unverified).
**What the interviewer is checking:** Counterfactual thinking: what would have happened without the promotion.
**Say this in the interview:** "Compare promoted customers with a similar group that did not get the offer; only the difference is incremental. Return = incremental contribution minus the discount given away."
**Clarify first:** Was the offer randomly assigned? Contribution per order? Any repeat effects?
**Structure:** Baseline (counterfactual), incremental orders, margin, discount cost, side effects (cannibalisation, pull-forward, later dip).
**What I would check, in order:** a randomised holdout (a group kept out of the offer); otherwise matched control or before-after with trend; redemptions versus baseline orders; two weeks after the promotion.
**Numeric work (assumed):** 10,000 orders use the offer; the holdout shows 6,000 would have happened anyway, so 4,000 are incremental. Contribution before discount Rs 80, discount Rs 50. Net = 10,000 x (80 - 50) - 6,000 x 80 = Rs 3,00,000 - Rs 4,80,000 = -Rs 1,80,000. (Equally: 4,000 x 80 = Rs 3,20,000 gained, minus 10,000 x 50 = Rs 5,00,000 discount cost.) The promotion loses money unless it also builds repeat customers.
**If the data shows...:** high baseline share means target the offer; repeat uplift after 8 weeks may justify it.
**Recommendation:** Run holdouts routinely; report incremental orders, incremental contribution, cost per incremental order (Rs 125 here) and post-promotion dip.
**Likely follow-ups:** 1) *No holdout?* Use difference-in-differences: compare the change in the promoted regions with the change in similar regions that had no promotion. 2) *Pull-forward?* Check weeks after.
**Common mistakes / traps:** Counting all redemptions as incremental; ignoring discount on baseline orders.

### Q60 ⭐⭐ 🔴 A referral programme pays Rs 150 to the referrer and Rs 100 to the new user, while paid acquisition costs Rs 400 per user. Is it cheaper, and what viral coefficient is needed to double 1,000 seed users?
Data: each user invites 5 people and 10% of invitees join. Assume no overlap and ignore time.
**Asked at:** commonly asked (no company-specific report found); referral economics is a gap-fill topic in the sources file.
**What the interviewer is checking:** Cost per acquired user and the viral coefficient (average new users each user brings).
**Say this in the interview:** "Referral costs Rs 250 a user versus Rs 400, so it is cheaper. The coefficient here is 0.5, which exactly doubles 1,000 seeds over repeated rounds."
**Definition in plain words:** Viral coefficient k = invites per user x conversion rate.
**Worked answer:**
1. Cost per referred user = 150 + 100 = Rs 250. Saving = 400 - 250 = Rs 150 (37.5% cheaper).
2. k = 5 x 0.10 = 0.5.
3. Seeds bring 1,000 x 0.5 = 500, those bring 250, and so on. Total new users = 1,000 x (0.5 / (1 - 0.5)) = 1,000. Total = 2,000, so the base exactly doubles in the limit.
4. If only one round counts, doubling needs k = 1 (1,000 new from 1,000 seeds).
**Result:** Cheaper by Rs 150 a user. Cost of the 1,000 new users: Rs 2.5 lakh versus Rs 4 lakh paid. Doubling needs k = 0.5 over all rounds (the existing figure just meets it), or k = 1 in one round.
**Check:** Without time, the series 500 + 250 + 125 + ... sums to 1,000.
**Caveats:** Real referrals overlap and fade; quality and retention of referred users may differ; reward may be paid only after first purchase; k at or above 1 would be self-sustaining.
**Likely follow-ups:** 1) *k = 0.6?* Total new = 1,500. 2) *Better than ads?* Check retention and fraud.
**Common mistakes / traps:** Paying only the referrer's Rs 150; confusing k=1 with doubling; ignoring time.

### Q61 ⭐ 🟢 Why do interviewers prefer a structured profitability tree over a memorised framework?
**Asked at:** commonly asked (no company-specific report found); consulting prep sites expect MECE structure (unverified).
**What the interviewer is checking:** Whether you think for the problem or recite a template.
**Say this in the interview:** "A tree is built from the question, so it covers everything without overlap and I can drill into the part that matters. A memorised framework may fit the wrong problem."
**Explain simply:**
- A profitability tree starts from the identity: profit = revenue - cost, and splits each side (revenue = volume x price; cost = fixed + variable).
- MECE means "mutually exclusive, collectively exhaustive": no overlaps, no gaps.
- A memorised framework (such as 4Ps or 3Cs) may not match the problem, so you force-fit.
- Worked mini-example: profit down 20 lakh. Tree shows revenue flat but variable cost per unit up, so you go straight to cost instead of reciting marketing ideas.
- Practice step: draw a tree for "attrition cost rose" (headcount x rate x cost per exit).
**Likely follow-ups:** 1) *Are frameworks useless?* No, as a checklist to test your tree. 2) *How deep do you go?* Until you can act.
**Common mistakes / traps:** Reciting a framework without adapting it; overlapping branches; never choosing which branch to test first.

### Q62 ⭐ 🟢 What is operating leverage and why does it make profit more volatile than revenue?
**Asked at:** commonly asked (no company-specific report found); gap-fill topic in the sources file.
**What the interviewer is checking:** Fixed versus variable cost understanding.
**Say this in the interview:** "Fixed costs do not move with sales, so a small change in revenue becomes a bigger change in profit. The degree of leverage is contribution divided by profit."
**Explain simply:**
- Operating leverage is how much of the cost base is fixed.
- Degree of operating leverage (DOL) = contribution / profit = % change in profit / % change in revenue.
- Worked mini-example: revenue 200, variable cost 50%, fixed 60. Contribution 100, profit 40, DOL = 2.5. Revenue +10% gives profit +25%; revenue -10% gives profit 30, down 25%.
- High leverage helps in good times and hurts in bad (airlines, software, factories).
- Practice step: compute DOL for a business with fixed cost 20 and contribution 100 (profit 80, DOL 1.25).
**Likely follow-ups:** 1) *Which firms have high leverage?* Fixed-heavy businesses. 2) *Risk?* Break-even sits close to current sales.
**Common mistakes / traps:** Confusing it with debt leverage; applying DOL to large swings (it is linear only while costs stay fixed).

### Q63 ⭐ 🟡 A firm has fixed costs of Rs 60 lakh, variable costs of 50% of revenue and revenue of Rs 200 lakh. If revenue rises 10%, by what percentage does profit rise?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Contribution margin and operating leverage.
**Say this in the interview:** "Profit goes from Rs 40 lakh to Rs 50 lakh, up 25%."
**Definition in plain words:** Contribution = revenue - variable cost. Profit = contribution - fixed cost.
**Worked answer:**
1. Now: contribution = 200 x 50% = 100; profit = 100 - 60 = Rs 40 lakh.
2. Revenue +10% = 220; contribution 110; profit = 110 - 60 = Rs 50 lakh.
3. Profit change = 10 / 40 = 25%.
**Result:** Profit rises 25% (Rs 10 lakh).
**Check:** DOL = contribution / profit = 100 / 40 = 2.5; 2.5 x 10% = 25%. A 10% fall gives profit 30 (-25%).
**Caveats:** Assumes fixed cost stays fixed and variable cost stays 50% of revenue (no price discount).
**Likely follow-ups:** 1) *Break-even revenue?* 60 / 0.5 = Rs 120 lakh. 2) *Margin of safety?* 80 lakh.
**Common mistakes / traps:** Saying profit rises 10%; applying the 10% to profit directly; forgetting fixed cost is constant.

### Q64 ⭐ 🟡 A store costs Rs 60 lakh to open and earns Rs 1 lakh a month of contribution for the first 6 months, then Rs 3 lakh a month. When does it pay back?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Cumulative cash flow and payback period.
**Say this in the interview:** "After 6 months only Rs 6 lakh is recovered; the remaining Rs 54 lakh at Rs 3 lakh a month takes 18 more months, so payback is month 24."
**Definition in plain words:** Payback period = time until cumulative contribution equals the investment (simple, undiscounted).
**Worked answer:**
1. First 6 months: 6 x 1 = Rs 6 lakh.
2. Remaining to recover: 60 - 6 = Rs 54 lakh.
3. At Rs 3 lakh a month: 54 / 3 = 18 months.
4. Total = 6 + 18 = 24 months.
**Result:** 24 months (2 years).
**Check:** 6 x 1 + 18 x 3 = 6 + 54 = Rs 60 lakh.
**Caveats:** Ignores the time value of money (discounted payback would be longer), working capital and rent increases; ramp assumed fixed.
**Likely follow-ups:** 1) *If ramp-up took 12 months?* 12 + 48/3 = 28 months. 2) *Cash needed at lowest point?* Rs 60 lakh plus early losses.
**Common mistakes / traps:** Dividing 60 by 3 = 20 and ignoring the slow start.

### Q65 ⭐ 🟡 A shop-level analysis shows return rate falling from 20% to 15% on 1,00,000 orders a month. What is the monthly saving?
Data: reverse logistics and refurbishment cost Rs 150 per returned order; ignore recovered revenue.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Percentage points versus percent, and cost saving.
**Say this in the interview:** "Returns fall by 5,000 orders a month, which saves Rs 7.5 lakh a month, about Rs 90 lakh a year."
**Definition in plain words:** Saving = fewer returned orders x cost per return.
**Worked answer:**
1. Returns before: 20% x 1,00,000 = 20,000. After: 15% x 1,00,000 = 15,000.
2. Fewer returns = 5,000.
3. Saving = 5,000 x Rs 150 = Rs 7,50,000 a month.
**Result:** Rs 7.5 lakh a month; Rs 90 lakh a year.
**Check:** 5 percentage points x 1,00,000 = 5,000. In relative terms returns fell 25%.
**Caveats:** Assumes orders stay at 1,00,000; ignoring recovered revenue (as told) understates the gain; the fall must be caused by an action, not seasonality.
**Likely follow-ups:** 1) *Why not 5% of Rs 150?* The base is orders. 2) *Cost of the fix?* Compare against Rs 7.5 lakh a month.
**Common mistakes / traps:** Calling it a 5% fall (it is 5 percentage points, 25% relative); using returns instead of orders as the base.

### Q66 ⭐ 🟡 A BPO's attrition is 40% on 500 agents with Rs 60,000 replacement cost per exit. How much does cutting attrition to 30% save in a year?
**Asked at:** commonly asked (no company-specific report found); attrition economics is a gap-fill topic in the sources file and an HR-friendly case.
**What the interviewer is checking:** Attrition-cost arithmetic.
**Say this in the interview:** "Exits drop from 200 to 150, 50 fewer a year, so the saving is Rs 30 lakh."
**Definition in plain words:** Attrition = exits / average headcount over the period. Cost = exits x cost per exit.
**Worked answer:**
1. Exits at 40%: 0.40 x 500 = 200; cost = 200 x 60,000 = Rs 1.2 crore.
2. Exits at 30%: 0.30 x 500 = 150; cost = Rs 90 lakh.
3. Saving = Rs 1.2 crore - Rs 90 lakh = Rs 30 lakh (50 x 60,000).
**Result:** Rs 30 lakh a year.
**Check:** 10 points x 500 = 50 exits; 50 x 60,000 = 30,00,000.
**Caveats:** Replacement cost may include hiring, training and lost productivity; exits during a ramp-up cost more; headcount may change; the programme to cut attrition has its own cost.
**Likely follow-ups:** 1) *Break-even spend?* Up to Rs 30 lakh a year. 2) *Which exits matter?* Early-tenure exits cost the most.
**Common mistakes / traps:** Using 10% of cost directly; ignoring that annual versus monthly attrition differ.

### Q67 ⭐ 🟡 Why might a psychologically priced Rs 99 plan outperform a Rs 100 plan, and how would you test it?
**Asked at:** commonly asked (no company-specific report found); pricing cases listed on prep sites (unverified).
**What the interviewer is checking:** Behavioural pricing and clean experiment design.
**Say this in the interview:** "Buyers read the left digit, so Rs 99 can feel like 'under 100'. I would run a randomised A/B test and compare revenue per visitor, not just conversion."
**Explain simply:**
- Left-digit effect: the first digit anchors perception, so 99 feels notably cheaper than 100 even though the gap is 1%.
- Price endings also signal "deal".
- Test: randomly show Rs 99 to half of visitors and Rs 100 to the other half; measure conversion, revenue per visitor, refund and churn.
- Mini-example (assumed): baseline conversion 4%. To detect a rise to 4.4% (10% relative lift) with 80% power (an 80% chance of spotting a real lift) and 5% significance (a 5% risk of a false alarm) needs about 39,500 visitors per group. A true effect of only 1% (4% to 4.04%) needs about 3.8 million per group, which is not practical.
- Practice step: decide your minimum lift worth detecting before you start.
**Likely follow-ups:** 1) *Primary metric?* Revenue per visitor. 2) *Risk?* Cheaper-looking price may attract weaker buyers.
**Common mistakes / traps:** Stopping early when results look good; judging conversion alone (Rs 99 earns 1% less per sale); testing without randomisation.

### Q68 ⭐ 🟡 A fashion e-commerce firm has 30% of stock unsold at season end. How do you decide the markdown depth that maximises profit?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Sunk cost, price response and salvage value.
**Say this in the interview:** "The cost is already spent, so I pick the discount that maximises revenue from the leftover stock plus whatever the remainder will fetch at clearance."
**Clarify first:** How much time is left? Salvage (clearance) value? Do discounts hurt full-price sales or brand?
**Structure:** For each depth d: units sold = leftover x sell-through(d); revenue = units x price x (1 - d); plus unsold units x salvage value.
**What I would check, in order:** past markdown elasticities by category; remaining season weeks; stock by size; salvage offers.
**Numeric work (assumed):** 3,000 unsold units, price Rs 1,000, salvage Rs 200 a unit, sunk cost ignored. Assumed sell-through: 20% off sells 40%, 30% off 60%, 40% off 80%, 50% off 90%, 60% off 95%.
Total value (sales + salvage): 20% off = Rs 13.2 lakh; 30% = Rs 15.0 lakh; 40% = Rs 15.6 lakh; 50% = Rs 14.1 lakh; 60% = Rs 11.7 lakh. Best is about 40% off.
**If the data shows...:** flatter sell-through response means shallow markdown; higher salvage means deeper markdown is less attractive; staged markdown can beat one deep cut.
**Recommendation:** Start at 30%, review weekly, step to 40% if sell-through lags; track sell-through, gross margin and brand impact.
**Likely follow-ups:** 1) *Use cost?* Only to check against below-cost sales if cash matters. 2) *Staged versus one cut?* Staged learns the response.
**Common mistakes / traps:** Anchoring on cost; assuming a deeper discount always sells more; ignoring salvage.

### Q69 ⭐ 🟡 How would you set the price of a new product that has no competitors and no sales history?
**Asked at:** commonly asked (no company-specific report found); pricing methods (cost, value, competition) are listed on consulting prep sites (unverified).
**What the interviewer is checking:** Value-based pricing and learning through testing.
**Say this in the interview:** "I would estimate what customers are willing to pay, check it against cost, then test a few price points before locking one in."
**Explain simply:**
- Price floor = unit cost; price ceiling = customer value (what it saves or gives them). The price lies in between.
- Methods: customer surveys of willingness to pay (such as asking "too cheap, a bargain, getting expensive, too expensive"), comparing to substitutes or workarounds, small price tests.
- Strategies: skimming (start high, lower later) or penetration (start low to gain users).
- Mini-example (assumed): unit cost Rs 300. Price Rs 600, 1,000 buyers, profit Rs 3 lakh; Rs 800, 800 buyers, Rs 4 lakh; Rs 1,000, 600 buyers, Rs 4.2 lakh; Rs 1,200, 350 buyers, Rs 3.15 lakh. About Rs 1,000 wins here.
- Practice step: list three substitute ways a customer solves the problem today.
**Likely follow-ups:** 1) *No competitors?* The substitute is "do nothing". 2) *Raise later?* Easier to lower than to raise.
**Common mistakes / traps:** Cost-plus only; copying an unrelated product's price; never testing.

### Q70 ⭐ 🟡 A 10% relative improvement in any funnel stage raises revenue by the same amount, so why do you not treat all stages as equally attractive?
**Asked at:** commonly asked (no company-specific report found); funnel work is typical of e-commerce case rounds (unverified).
**What the interviewer is checking:** Math of multiplication versus practical difficulty and cost.
**Say this in the interview:** "The maths is equal, but effort, headroom and cost are not, so I rank stages by how much realistic improvement each can give per rupee spent."
**Explain simply:**
- A funnel multiplies rates, so each 10% relative lift gives 10% more revenue.
- Mini-example (assumed): 1,00,000 visitors x 5% sign up x 40% activate x 50% order x 90% pay = 900 paid orders. Lift any one stage 10% relative and it becomes 990 (+10%).
- But that lift needs different absolute moves: 5% to 5.5% signups; 90% to 99% payment success (nearly impossible); 50% to 55% ordering.
- Headroom: a stage near its ceiling cannot improve.
- Cost and effort: fixing payment failures may be cheap engineering, while lifting signups may need big marketing spend.
- Other effects: a stage's quality changes customers downstream.
- Practice step: for each stage list headroom, cost and confidence, then rank.
**Likely follow-ups:** 1) *Where first?* Often the biggest drop with a known cause. 2) *Tests?* A/B each fix.
**Common mistakes / traps:** Treating relative and absolute changes the same; optimising a stage that is already near its ceiling.

### Q71 ⭐ 🟡 What is a flat cohort retention curve, and why does it matter more for growth than a one-time user spike?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Cohort retention understanding.
**Say this in the interview:** "A flat curve means that after the early drop, a steady share of each cohort stays; those users keep building the base, while a spike fades."
**Explain simply:**
- A cohort is a group of users who joined in the same period; the retention curve shows the share still active over time.
- Flat means the line levels off (for example at 30%) instead of falling to zero: a loyal core exists.
- Mini-example (assumed): 1,000 new users a month for 12 months. If each cohort flattens at 30%, active base after a year is 3,600. If the curve falls to 5%, it is 600. A one-time spike of 10,000 users with 3% retained leaves only 300.
- So a flat curve compounds; a spike adds nothing lasting.
- Practice step: plot retention by signup month in Excel and see where the line flattens.
**Likely follow-ups:** 1) *Good level?* Depends on the product, unverified benchmarks. 2) *Spike useful?* Only if it helps retention.
**Common mistakes / traps:** Judging by total signups; mixing cohorts into one average; ignoring the base level.

### Q72 ⭐ 🟡 When is a loss-making business unit still worth running?
**Asked at:** commonly asked (no company-specific report found); product-line shutdown is a gap-fill topic in the sources file.
**What the interviewer is checking:** Avoidable versus allocated costs and strategic value.
**Say this in the interview:** "If it covers its own avoidable costs and contributes toward shared overhead, closing it makes the company worse off."
**Explain simply:**
- Look at contribution (revenue minus costs that disappear on closure), not accounting profit after allocated overhead.
- Mini-example (assumed): a unit shows a loss of Rs 10 lakh after Rs 35 lakh of allocated overhead, but earns Rs 25 lakh contribution. Close it and the company loses that Rs 25 lakh while the Rs 35 lakh overhead remains (the company is Rs 25 lakh worse off). If contribution were negative, closing helps.
- Other reasons to keep: strategic (feeds other units, brings customers, a future growth option), it will turn positive soon, high exit costs, shared customers.
- Practice step: list which costs would truly vanish on closure.
**Likely follow-ups:** 1) *When close?* Negative contribution with no path to positive. 2) *Which numbers?* Avoidable cost and cross-unit effects.
**Common mistakes / traps:** Using allocated costs; ignoring knock-on effects on other units; keeping a unit for sentimental reasons.

### Q73 ⭐ 🔴 Dynamic pricing: when does surge pricing improve profit and when does it destroy long-term value?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Supply and demand balance versus trust and fairness.
**Say this in the interview:** "Surge helps when it truly clears a temporary shortage and brings supply; it hurts when users feel exploited or when prices rise without service improving."
**Explain simply:**
- Works when: demand spikes briefly, supply can respond (drivers come online), customers have few alternatives, and the price signal is transparent.
- Mini-example (assumed): 100 requests, 60 cabs. At 1.5x price some requests drop to 70 while more drivers join, so 70 rides are served at 1.5 times the fare: revenue index 105 versus 60 before.
- Hurts when: users see it as unfair (emergencies, weather, strikes), competitors do not surge, surge is extreme or frequent, or supply never responds.
- Long-term value risk: lost trust, switching to rivals, regulatory limits.
- Safeguards: caps, upfront price display, explanation, and tracking repeat rate in surge zones.
- Practice step: define the metrics: fulfilment rate, wait time, repeat rate after surge, complaint rate.
**Likely follow-ups:** 1) *Test?* Compare repeat usage after surge exposure with similar users. 2) *Alternative?* Queueing or reservations.
**Common mistakes / traps:** Looking only at same-day revenue; ignoring repeat behaviour; assuming surge always brings supply.

### Q74 ⭐ 🔴 How would you decide between growth and profitability for a startup that has 18 months of cash left?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Runway thinking and decision rules under constraints.
**Say this in the interview:** "I would check unit economics. If each customer is profitable, grow; if not, fix margins first. Either way, I would keep enough runway to raise funds or reach break-even."
**Clarify first:** Burn rate? Are unit economics positive? How long does fundraising take? Market competition?
**Structure:** Runway = cash / monthly net burn. Compare growth spend returns (LTV versus CAC, payback) with cash needed.
**What I would check, in order:** contribution margin per customer; CAC payback; retention; burn by item; funding conditions.
**Numeric work (assumed):** Cash Rs 36 crore, burn Rs 2 crore a month gives 18 months. Assume raising money takes about 6 months (an assumption, not a fact), so decisions must be made by month 12. Cutting burn 30% (to Rs 1.4 crore) stretches runway to 25.7 months.
**If the data shows...:** payback under 12 months with strong retention means keep growing; negative contribution per user means fix pricing and costs first; mixed means grow only the profitable segments.
**Recommendation:** Rule: keep at least 12 months of runway after any growth spend; grow only where payback is short; set a milestone (for example break-even in two key cities) and start fundraising early. Review monthly: runway (months of cash left), burn multiple (cash burned per rupee of new revenue), contribution per user, CAC payback.
**Likely follow-ups:** 1) *If funding is hard?* Cut burn sooner. 2) *Growth-profit balance?* Aim for efficient growth.
**Common mistakes / traps:** Binary thinking; ignoring fundraising time; burning cash on unprofitable customers.

### Q75 ⭐ 🔴 A student discount cuts the price for a segment. Under what conditions does it raise total profit?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Price discrimination logic and break-even volume.
**Say this in the interview:** "It raises profit if the discount brings enough extra students to cover the margin lost per student, and if non-students do not use it."
**Explain simply:**
- Break-even uplift = margin / (margin - discount) - 1.
- Mini-example (assumed): price Rs 100, cost Rs 60, margin Rs 40. A Rs 20 discount (20%) leaves Rs 20, so student volume must double (+100%). A Rs 15 discount leaves Rs 25: +60% needed.
- Conditions: (1) students are price-sensitive and many would not buy otherwise; (2) verification stops others claiming it; (3) little cannibalisation of students who would have paid; (4) the discount builds loyalty or later full-price purchases; (5) spare capacity so marginal cost stays low.
- Practice step: estimate the share of discounted students who would have bought anyway; it raises the break-even.
**Likely follow-ups:** 1) *Test?* Randomised offer. 2) *Risk?* Other groups demand discounts.
**Common mistakes / traps:** Ignoring cannibalisation; forgetting margin matters (a 20% discount needs far more than 20% volume).

### Q76 ⭐ 🔴 A competitor offers free delivery with no minimum. How do you test whether you must match it?
**Asked at:** commonly asked (no company-specific report found); delivery-fee thresholds appear in quick-commerce discussions (unverified).
**What the interviewer is checking:** Test design and economics before reacting.
**Say this in the interview:** "First I would measure what we lose if we do not match, then what matching costs. I would test in matched cities or randomised users, not roll out everywhere."
**Clarify first:** Our current fee policy? Cost per delivery? Overlap with the competitor's customers?
**Structure:** Loss from not matching (orders switching) versus cost of matching (fee income given up, plus subsidy on every order).
**What I would check, in order:** change in our orders in areas where the competitor launched; share of our customers also using the competitor; basket sizes of fee-paying orders; repeat behaviour.
**Numeric work (assumed):** Contribution per order Rs 25 (including delivery fees). 60% of orders pay an average Rs 30 fee, so fee income per average order is Rs 18. Matching drops contribution to Rs 7 per order, so volume must rise about 257% to break even. Not matching: if 5% of orders move away, loss is about Rs 1.25 per average order. So full matching is far costlier unless losses are much larger.
**If the data shows...:** small order loss means do not match; heavy loss among high-value customers means match selectively (for example a subscription pass or free delivery above a basket value).
**Recommendation:** Run a test: matched cities or randomised users get free delivery for 4 weeks; compare orders, contribution and retention with control. Prefer targeted responses (membership, thresholds) to blanket matching.
**Likely follow-ups:** 1) *Why not just match?* It can cost more than the sales it saves. 2) *Duration?* Long enough to see repeat behaviour.
**Common mistakes / traps:** Reacting without data; testing in non-comparable cities; looking only at order counts, not contribution.


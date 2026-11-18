# Book 10 — Domain Knowledge | Part 5: Supply Chain & Operations 🟢🟡🔴

**Target:** 70 questions | **Actual:** 85 questions
**Scope:** supply chain and operations domain: inventory, demand forecasting, logistics, warehouse, procurement, OTIF, lead time and S&OP; vocabulary, metrics with inline-number calculations, data tables and sources, privacy awareness, and domain case-style analysis.

### Q1 ⭐⭐⭐ 🟢 What is a supply chain, and what are its main stages from supplier to customer?
**Asked at:** commonly asked (no company-specific report found); supply chain analyst prep guides open with this vocabulary (unverified).
**What the interviewer is checking:** Whether you can describe the end-to-end flow in plain words and see where data is created.
**Say this in the interview:** "A supply chain is the network that turns raw materials into a product in the customer's hands. The stages are suppliers, manufacturing, storage, transport and delivery, and it also carries information and money back the other way."
**Explain simply:**
- **Suppliers:** firms that provide raw materials or parts. Data: purchase orders, supplier lead times.
- **Manufacturing or sourcing:** the company makes the product, or buys finished goods to resell (a retailer). Data: production plans, yields.
- **Storage (inventory):** goods wait in warehouses. Data: stock levels by item and location.
- **Distribution and transport:** goods move to stores or customers. Data: shipments, delivery times.
- **Customer:** the order is delivered, and sometimes returned.
- Three flows run through all stages: products forward, money backward, information both ways.
- HR comparison: it is like the hiring pipeline (source, screen, offer, join), but for goods.
**Likely follow-ups:** 1) *Where do analysts add most value?* Spotting delays and excess stock between stages. 2) *Supply chain vs logistics?* Logistics is the moving and storing part; the supply chain is the whole network including buying and planning.
**Common mistakes:** Describing only transport; forgetting returns and information flow.

### Q2 ⭐⭐⭐ 🟢 What is OTIF (on-time, in-full), and why is it more demanding than on-time delivery alone?
**Asked at:** commonly asked (no company-specific report found); OTIF appears in KPI guides from supply chain software vendors (unverified).
**What the interviewer is checking:** That you know OTIF needs both conditions on the same order.
**Say this in the interview:** "OTIF is the share of orders delivered both on the promised date and with the full quantity ordered. It is stricter than on-time alone because an order that arrives on time but short still counts as a failure."
**Explain simply:**
- **On time:** delivered by the promised date (some firms allow a window, for example one day early or late; the window is a company rule).
- **In full:** the quantity delivered matches the quantity ordered (some allow a tolerance).
- OTIF = orders that are on time AND in full, divided by total orders. It is never higher than the lower of the two separate rates.
- A customer cares about both: a late truck and a half-empty truck both leave the shelf empty.
- Definitions differ across companies (order level or line level, tolerance, which date counts), so always ask and state yours.
**Likely follow-ups:** 1) *Can OTIF be higher than on-time?* No. 2) *Why do companies fine suppliers on OTIF?* Missing deliveries cost the buyer sales.
**Common mistakes:** Multiplying the two rates (only valid if the failures are independent, which is rare); counting an order as on time using the ship date instead of the delivery date.

### Q3 ⭐⭐⭐ 🟢 What is inventory turnover, and what does a low or high value tell a supply chain analyst?
**Asked at:** commonly asked (no company-specific report found); named in every supply chain KPI guide seen (unverified).
**What the interviewer is checking:** That you can define it and read both directions, not just "high is good".
**Say this in the interview:** "Inventory turnover is how many times the stock is sold and replaced in a year: cost of goods sold divided by average inventory value. Low can mean overstock or slow sellers; very high can mean stockouts risk."
**Explain simply:**
- **Cost of goods sold (COGS):** what the goods you sold cost the company to buy or make.
- **Average inventory:** (opening stock value + closing stock value) / 2.
- **Low turnover:** cash is stuck in stock, risk of ageing or expiry, storage cost.
- **High turnover:** lean and efficient, but if too high the shelves may run empty and sales are lost.
- Compare like with like: a grocery item turns far faster than furniture, so compare within a category or against the item's own history.
**Likely follow-ups:** 1) *How do you convert it to days?* 365 divided by turnover. 2) *Is high always good?* No, check fill rate and stockouts together.
**Common mistakes:** Using sales instead of COGS without saying so; using one closing figure for a seasonal business; comparing different categories.

### Q4 ⭐⭐⭐ 🟢 What is lead time, and how is supplier lead time different from customer order lead time?
**Asked at:** commonly asked (no company-specific report found); a standard term in planning job descriptions (unverified).
**What the interviewer is checking:** That you know lead time has a clear start and end, and two different versions.
**Say this in the interview:** "Lead time is the elapsed time between asking for something and receiving it. Supplier lead time runs from our purchase order to goods arriving at our warehouse; customer order lead time runs from the customer's order to delivery at their door."
**Explain simply:**
- **Supplier (replenishment) lead time:** purchase order placed to goods received. It drives how much safety stock we need.
- **Customer order lead time:** order placed to delivered. It is what the customer experiences.
- Lead time is a spread, not one number: the average and the variability both matter.
- Clock-start rules differ (order date, approval date, dispatch date), so state which one you use.
- HR analogy: supplier lead time is like time to fill a vacancy; customer lead time is like the candidate's wait from application to offer.
**Likely follow-ups:** 1) *Why does variability matter?* Unpredictable lead time needs more safety stock. 2) *Which do you report to customers?* Customer order lead time.
**Common mistakes:** Using the average only; mixing calendar days with working days.

### Q5 ⭐⭐⭐ 🟢 What is safety stock, and why does a business hold it?
**Asked at:** commonly asked (no company-specific report found); core inventory planning term (unverified).
**What the interviewer is checking:** That you see it as insurance against uncertainty, with a cost.
**Say this in the interview:** "Safety stock is extra inventory kept above expected demand so we do not run out when demand is higher than forecast or a delivery is late. It trades storage cost for service level."
**Explain simply:**
- **Demand uncertainty:** customers sometimes buy more than the forecast.
- **Supply uncertainty:** suppliers sometimes deliver late.
- More variability or a higher target service level means more safety stock. A common textbook formula uses z x standard deviation of demand x square root of lead time (from memory, simplified).
- It is not free: it ties up cash and can expire or go obsolete.
- HR analogy: keeping a few extra trained staff on a shift for unexpected absence.
**Likely follow-ups:** 1) *How do you reduce it?* Shorter, steadier lead times and better forecasts. 2) *Does it guarantee no stockout?* No, only a target probability.
**Common mistakes:** Treating it as "average demand times a few days"; setting the same level for every item.

### Q6 ⭐⭐⭐ 🟢 What is a stockout, and what business costs does it cause beyond the lost sale?
**Asked at:** commonly asked (no company-specific report found); a standard retail and supply chain topic (unverified).
**What the interviewer is checking:** That you think about hidden costs, not only the immediate revenue.
**Say this in the interview:** "A stockout is when an item is wanted but not available. Beyond the lost sale, it can lose the customer, damage trust, force costly rush orders and distort the data used for forecasting."
**Explain simply:**
- **Lost sale:** the customer buys elsewhere or not at all.
- **Lost customer:** repeated misses push regular buyers to a competitor.
- **Expedite costs:** emergency orders and air freight cost more than normal shipping.
- **Penalties:** B2B customers may fine the supplier (linked to OTIF).
- **Bad data:** recorded sales fall to zero because stock was zero, not because demand fell. A forecast built on that understates true demand.
- Production lines or services can stop when a part is missing.
**Likely follow-ups:** 1) *How do you measure it?* Out-of-stock days or percentage of item-days with zero stock. 2) *Backorder vs lost sale?* A backorder is kept and filled later; a lost sale is gone.
**Common mistakes:** Treating zero sales as zero demand; counting only revenue lost.

### Q7 ⭐⭐⭐ 🟢 What is fill rate, and how is order fill rate different from line fill rate and unit fill rate?
**Asked at:** commonly asked (no company-specific report found); fill rate variants are explained in retail KPI guides (unverified).
**What the interviewer is checking:** That you know fill rate has levels and the strictest is order level.
**Say this in the interview:** "Fill rate is how much of what customers ordered we shipped from stock. Order fill rate counts only fully complete orders, line fill rate counts complete lines, and unit fill rate counts individual units, so order is the strictest and unit the most forgiving."
**Explain simply:**
- **Order:** one customer request. **Line:** one item on that order. **Unit:** one piece.
- Example: an order for 3 products (3 lines) totalling 30 units. If one line is short by 2 units, the order is incomplete, 2 of 3 lines are complete, and 28 of 30 units shipped.
- Order fill rate <= line fill rate <= unit fill rate in typical data, because one short line spoils the whole order.
- Which one to report depends on the customer: a retailer that cannot accept partial orders cares about order level.
- Definition of "filled" (from stock on hand versus after backorder) varies; state yours.
**Likely follow-ups:** 1) *Fill rate vs OTIF?* Fill rate ignores timing. 2) *Which is best?* Report all three; the gap shows how spread out the shortages are.
**Common mistakes:** Quoting unit fill rate and calling it service level; mixing the levels in one comparison.

### Q8 ⭐⭐⭐ 🟢 What is demand forecasting, and which inputs and data sources does a demand planner typically use?
**Asked at:** commonly asked (no company-specific report found); demand planner job postings list forecasting and planning tools (unverified).
**What the interviewer is checking:** That you know a forecast is built from history plus business knowledge.
**Say this in the interview:** "Demand forecasting estimates how much of each item customers will want in future periods. Planners start from sales history and add known events such as promotions, price changes, seasonality and new launches."
**Explain simply:**
- **Sales history:** from the ERP (Enterprise Resource Planning, the system that records orders and invoices) or point-of-sale data, cleaned of stockout periods.
- **Calendar effects:** festivals, weekdays, month-end, weather.
- **Promotions and pricing:** from the marketing and commercial teams.
- **Customer input:** orders pipeline, sales team estimates, retailer sell-through data.
- **Statistical model plus human override:** the model gives a baseline; planners adjust for what the model cannot know.
- Forecasts are wrong by nature; the job is to measure and reduce the error (bias and WAPE, see Q19).
**Likely follow-ups:** 1) *Forecast at which level?* Usually item and location by week or month. 2) *New product with no history?* Use a similar item's history.
**Common mistakes:** Forecasting from sales when stockouts hid demand; ignoring promotions.

### Q9 ⭐⭐⭐ 🟢 What is S&OP (Sales and Operations Planning), who attends the meeting, and what does the analyst bring to it?
**Asked at:** commonly asked (no company-specific report found); S&OP analyst roles appear in job postings such as a Bengaluru retailer posting seen in research (unverified).
**What the interviewer is checking:** That you understand S&OP as a cross-team monthly decision process.
**Say this in the interview:** "S&OP is a regular, usually monthly, meeting where sales, supply, finance and leadership agree one plan for demand and supply. The analyst brings the numbers: forecast versus actual, inventory position, capacity and service levels."
**Explain simply:**
- **Goal:** one agreed plan so sales promises match what operations can deliver.
- **Typical attendees:** demand planning, sales, supply or production planning, procurement, finance, and a senior leader who decides trade-offs. Exact cycle steps vary by company.
- **Analyst's pack:** last month's forecast accuracy and bias, stock by item group, backorders, supplier risks, a comparison of demand against capacity.
- **Output:** decisions such as build more, hire extra shifts, cut a promotion.
- HR link: it is similar to workforce planning, matching headcount supply to demand.
**Likely follow-ups:** 1) *Why monthly?* Matches the planning horizon of buying and production. 2) *What if sales and supply disagree?* Escalate the trade-off with numbers to leadership.
**Common mistakes:** Showing raw tables without a recommendation; one-sided numbers.

### Q10 ⭐⭐⭐ 🟢 What is a SKU, and how is a SKU different from a product, a category and a SKU-location?
**Asked at:** commonly asked (no company-specific report found); data granularity is a common analyst test (unverified).
**What the interviewer is checking:** That you understand the grain of the data you will count and join.
**Say this in the interview:** "A SKU, stock keeping unit, is one exact sellable variant with its own code, such as one shirt style in size M and blue. A product is the broader idea, a category groups many products, and a SKU-location is that SKU in one specific warehouse or store."
**Explain simply:**
- **Product:** "Cotton T-shirt". It may have 12 SKUs (3 sizes x 4 colours).
- **SKU:** the lowest level you stock, price and track.
- **Category:** a group such as "Menswear".
- **SKU-location:** the SKU at one place; 12 SKUs in 5 stores gives 60 SKU-locations. Stock, forecasts and reorder points are set at this level.
- Counting "items" without saying which level gives very different numbers.
**Likely follow-ups:** 1) *Is SKU the same as barcode?* Not always; one SKU can have several barcodes, or a barcode may change on repacking. 2) *Why SKU-location?* Demand and stock differ by place.
**Common mistakes:** Counting products as SKUs; joining stock at SKU level to sales at product level.

### Q11 ⭐⭐⭐ 🟢 What is ABC analysis of inventory, and how does it help prioritise attention?
**Asked at:** commonly asked (no company-specific report found); listed among core inventory techniques in KPI guides (unverified).
**What the interviewer is checking:** That you can apply the 80/20 idea to rank items.
**Say this in the interview:** "ABC analysis ranks items by their value, usually annual sales or usage value, and splits them into A (a small number of items giving most of the value), B (middle) and C (many items with little value). Then A items get the closest control."
**Explain simply:**
- Rank items by value, compute cumulative share, then cut. Typical cut-offs are around 70-80% for A, next 15-20% for B and the rest for C (these vary by company).
- Illustration (invented): 10 items with values 500, 250, 120, 60, 30, 20, 10, 5, 3, 2; the top 2 items make 75% of the total value, so they would be A.
- **A items:** tight forecasting, frequent review, small safety margins. **C items:** simple rules, bulk ordering.
- Limitation: value alone ignores criticality; a cheap but vital part can still stop production (a variant called XYZ looks at demand variability).
**Likely follow-ups:** 1) *Does an item's class change?* Yes, review quarterly. 2) *Value by what?* Sales value or usage value; say which.
**Common mistakes:** Treating C items as ignorable; classifying once and never reviewing.

### Q12 ⭐⭐⭐ 🟢 What is the difference between a warehouse, a distribution centre, a fulfilment centre and a dark store?
**Asked at:** commonly asked (no company-specific report found); vocabulary question common for e-commerce and quick-commerce roles (unverified).
**What the interviewer is checking:** That you know the role of each node, not just the names.
**Say this in the interview:** "All are storage sites, but with different jobs: a warehouse holds stock, a distribution centre moves stock out to stores quickly, a fulfilment centre packs individual customer orders, and a dark store is a small shop-like site that serves only online orders."
**Explain simply:**
- **Warehouse:** general storage, often bulk, goods may sit for a while.
- **Distribution centre (DC):** receives goods from many suppliers and ships them on to stores or other sites, with faster flow and less long-term storage.
- **Fulfilment centre:** picks, packs and ships single online orders to consumers.
- **Dark store:** a local, store-sized site closed to walk-in customers, used for very fast delivery (often within minutes or hours) in a small area.
- Real firms mix these terms, so check what a site actually does.
**Likely follow-ups:** 1) *Why dark stores?* Speed. The trade-off is higher cost per order and limited range. 2) *Which has the highest staffing needs?* Fulfilment sites, because of manual picking and packing.
**Common mistakes:** Assuming the names are strict standards; ignoring how the site type changes the metrics (pick time, stock turns).

### Q13 ⭐⭐⭐ 🟡 Compute OTIF from the order data below and say which failure type is the bigger problem.
10 orders: 8 delivered on time; 7 delivered in full; 6 both on time and in full.
**Asked at:** commonly asked (no company-specific report found); OTIF calculations are a standard prep-site exercise (unverified).
**What the interviewer is checking:** That you use the "both" count, and split failures into types.
**Say this in the interview:** "OTIF is 6 out of 10, which is 60%. The bigger problem is in-full: 3 orders were short, against 2 that were late."
**Explain simply:**
- OTIF counts only orders that passed both tests, so 6 of 10.
- The two separate rates (80% and 70%) look healthy but hide that 4 orders failed.
- Splitting the 4 failed orders tells us what to fix.
**Worked example:** (all figures computed by code; percentages of 10 orders)
- OTIF = 6 / 10 = **60%**. On-time rate = 8 / 10 = 80%. In-full rate = 7 / 10 = 70%.
- On time but not in full = 8 - 6 = **2** orders.
- In full but late = 7 - 6 = **1** order.
- Failed both = 10 - (6 + 2 + 1) = **1** order. Failed orders = 2 + 1 + 1 = 4, matching 10 - 6.
- Short orders in total = 2 + 1 = **3** (30%); late orders in total = 1 + 1 = **2** (20%).
- Conclusion: shortage (in-full) is the larger issue. Sample is only 10 orders, so one order moves the rate by 10 percentage points; check a larger window before acting.
**Likely follow-ups:** 1) *What next?* Cut by supplier, item and warehouse to find where shortages cluster. 2) *Is 60% bad?* It depends on the customer's target and what the definition tolerates.
**Common mistakes:** Averaging 80% and 70% to get 75%; multiplying them to get 56%, which is not the actual 60%.

### Q14 ⭐⭐⭐ 🟡 Compute order fill rate, line fill rate and unit fill rate from the data below, and explain why the three differ.
4 orders, 10 lines, 100 units ordered. Orders shipped complete: 2. Lines shipped complete: 8. Units shipped: 90.
**Asked at:** commonly asked (no company-specific report found); fill rate variants are a standard KPI-guide topic (unverified).
**What the interviewer is checking:** That you divide the right count by the right base and can explain the ordering of the rates.
**Say this in the interview:** "Order fill rate is 50%, line fill rate is 80% and unit fill rate is 90%. They differ because one short line makes the whole order incomplete, but it only costs a small share of units."
**Explain simply:**
- Same shortage, three zoom levels: orders (biggest chunks), lines, units (smallest).
- A tiny shortage in one line fails a whole order, so the order rate is lowest.
**Worked example:** (computed by code)
- Order fill rate = 2 / 4 = **50%**.
- Line fill rate = 8 / 10 = **80%**.
- Unit fill rate = 90 / 100 = **90%**.
- Gaps: 2 lines were short, 10 units missing, and those 2 short lines sit in 2 different orders, which is why exactly 2 of 4 orders are incomplete (consistent with the data).
**Likely follow-ups:** 1) *Which to report to a customer who cannot take partial orders?* Order fill rate. 2) *What if the 10 missing units were all in one order?* Then the order rate would be 75%, the others unchanged.
**Common mistakes:** Saying the average (73%) is "the fill rate"; mixing the bases.

### Q15 ⭐⭐⭐ 🟡 Compute days of inventory on hand (days of supply) from the data below and say whether you would worry.
Closing stock 12,000 units. Average daily sales last 30 days: 400 units. Supplier lead time: 21 days.
**Asked at:** commonly asked (no company-specific report found); days of supply is a standard inventory metric (unverified).
**What the interviewer is checking:** That you compare cover with lead time, not read the number alone.
**Say this in the interview:** "Days of supply is stock divided by daily sales: 12,000 / 400 = 30 days. That covers the 21-day lead time with 9 days to spare, so I would not worry about a stockout today, but I would check demand variability."
**Explain simply:**
- Days of supply = how long current stock lasts at the recent sales rate.
- If it is below the lead time, a new order will arrive too late and a stockout is likely unless an order is already on the way.
- 30 days is not excessive without knowing the category's norm (target cover is a company choice).
**Worked example:** (computed by code)
- Days of supply = 12,000 / 400 = **30 days**.
- Demand during the 21-day lead time = 21 x 400 = 8,400 units.
- Stock left after lead time = 12,000 - 8,400 = **3,600** units = 9 days' cover (30 - 21).
- Caveat: a 30-day average hides spikes; if sales jump, the 9-day buffer shrinks fast. Also check open purchase orders already placed.
**Likely follow-ups:** 1) *What if daily sales are 700?* 12,000 / 700 = 17.1 days, below lead time, so I would worry. 2) *Would you worry about too much?* If the target is 15 days, 30 is excess cash.
**Common mistakes:** Ignoring lead time; using a month with a one-off promotion as the sales rate.

### Q16 ⭐⭐⭐ 🟡 Calculate the reorder point from the data below.
Average daily demand 50 units, lead time 8 days, safety stock 120 units.
**Asked at:** commonly asked (no company-specific report found); a standard formula in planning prep guides (unverified).
**What the interviewer is checking:** That you know the formula and the logic behind each part.
**Say this in the interview:** "Reorder point is demand during lead time plus safety stock: 50 x 8 + 120 = 520 units. When stock falls to 520, we place the next order."
**Explain simply:**
- **Reorder point (ROP):** the stock level that triggers a new order.
- During the 8-day wait we expect to sell 400 units; the 120 extra covers surprises.
**Worked example:** (computed by code)
- Demand during lead time = 50 x 8 = 400 units.
- ROP = 400 + 120 = **520 units**.
- Units: same as stock units. Inventory position (stock on hand plus on order) is what is compared to the ROP in most systems.
**Likely follow-ups:** 1) *What if lead time rises to 10 days?* ROP = 50 x 10 + 120 = 620 (safety stock held constant here, though it would normally rise too). 2) *How is it different from order quantity?* ROP says when; order quantity says how much.
**Common mistakes:** Forgetting safety stock; mixing days and weeks.

### Q17 ⭐⭐⭐ 🟡 Compute inventory turnover and days of inventory for the item group below, then explain why the answer depends on whether you use sales or cost of goods sold.
COGS for the year Rs 6 crore; opening inventory Rs 1.1 crore; closing inventory Rs 0.9 crore.
**Asked at:** commonly asked (no company-specific report found); a standard finance and supply chain calculation (unverified).
**What the interviewer is checking:** That you use average inventory and COGS, and know why consistent valuation matters.
**Say this in the interview:** "Average inventory is Rs 1.0 crore, so turnover is 6 times a year, or about 61 days of inventory. Using sales instead would give a higher turnover, because sales include profit margin while inventory is valued at cost."
**Explain simply:**
- Inventory is recorded at cost, so the matching top number is cost of goods sold, not sales.
- Sales include markup, so sales over inventory overstates how fast stock moves.
- Some firms still use sales; fine if used consistently, but then comparisons with COGS-based figures are wrong.
- Rs 1 crore = Rs 10 million.
**Worked example:** (computed by code)
- Average inventory = (1.1 + 0.9) / 2 = **Rs 1.0 crore**.
- Turnover = 6.0 / 1.0 = **6.0 times** per year.
- Days of inventory = 365 / 6.0 = **60.8 days** (about 61).
- If sales were, say, Rs 8 crore (invented): turnover = 8.0 times and days = 45.6, which looks better but only because of margin. Same stock, different answer.
**Likely follow-ups:** 1) *Why average rather than closing?* Closing may be unusually low or high; average smooths the year. 2) *Closing stock fell; good?* Possibly, but check stockouts.
**Common mistakes:** Using only closing stock; using 360 vs 365 inconsistently; mixing sales and COGS across items.

### Q18 ⭐⭐⭐ 🟡 What data tables and fields would you need to report OTIF by supplier or by customer, and what are the first three cuts you would make?
**Asked at:** commonly asked (no company-specific report found); data-validation and KPI-reporting themes appear in supply chain analyst prep guides (unverified).
**What the interviewer is checking:** Whether you can think in tables, keys and grain, and know what makes an order count as on-time and in-full.
**Say this in the interview:** "I would build it from an order-line table: one row per order line, with the promised date, actual delivery date, ordered quantity and received quantity. Joined to a supplier or customer master, I flag each line as on time and in full, roll up to the order, and cut by supplier or customer, then by item category, then by month."
**Explain simply:**
- **OTIF** (on-time, in-full) means an order arrived by the promised date AND with the full quantity ordered. Fail either test and the order fails.
- **Grain** means what one row represents. For OTIF the safest grain is the order line (one item on one order), because "in full" is checked per line and then the order passes only if every line passes.
- Be explicit about the definition: the "promised date" can be the date in the purchase order, a confirmed date, or the customer's requested date, and companies differ. Also state any grace window (for example, one day early or late allowed).
**Data and tables involved:**
- **Order header:** order_id, supplier_id or customer_id, order date, promised delivery date.
- **Order line:** order_id, line_no, sku, ordered quantity, promised date (if set per line).
- **Receipt or delivery table:** order_id, line_no, delivered quantity, actual delivery date (a goods receipt for suppliers, a proof of delivery for customers).
- **Master tables:** supplier or customer master (name, region, category), item master (category).
- **First three cuts:** 1) OTIF % by supplier or customer, ranked, to find the weakest few. 2) Split each failure into late-only, short-only and both, so you know which problem to fix. 3) OTIF by month, then by item category or region, to see if the problem is a trend or a pocket.
**Likely follow-ups:** 1) *What if lines are delivered in several shipments?* Sum received quantity up to the cut-off date, or use the last delivery date; state the rule. 2) *How do you handle cancelled lines?* Exclude them and say so.
**Common mistakes:** Computing at order-header level and missing short lines; mixing definitions of the promised date; ignoring partial deliveries; ranking suppliers on tiny order counts.

### Q19 ⭐⭐⭐ 🟡 Compute forecast bias and WAPE from the data below and say what each tells a planner.
Month 1-4 forecast: 100, 120, 90, 110. Actual: 110, 130, 100, 120.
**Asked at:** commonly asked (no company-specific report found); forecast bias and WAPE appear in demand planning articles and guides (unverified).
**What the interviewer is checking:** Whether you separate "how wrong" (error size) from "wrong in which direction" (bias).
**Say this in the interview:** "Bias is total forecast minus total actual, divided by total actual: minus 8.7%, so we under-forecast every month. WAPE is total absolute error divided by total actual: also 8.7%. Because every miss is in the same direction, the error is all bias, which a planner can fix by adjusting the forecast upward."
**Explain simply:**
- The **forecast** is the planner's estimate of how much will sell; the **actual** is what really sold.
- **Bias** shows direction. Over-forecasting and under-forecasting cancel out when summed, so a bias near zero can hide big misses.
- **WAPE** (weighted absolute percentage error) adds up the size of each miss, ignoring direction, and divides by total actual. Big-volume months count more, which is why planners prefer it to a simple average of percentages.
- Definitions differ across companies (some define bias as actual minus forecast, which flips the sign). I use forecast minus actual, so a negative number means under-forecast.
**Worked example:**
- Error each month (forecast minus actual): -10, -10, -10, -10. Total error = -40. Total absolute error = 40. Total actual = 460.
- Bias = -40 / 460 = -8.7% (rounded to one decimal).
- WAPE = 40 / 460 = 8.7% (rounded to one decimal).
- Both equal 8.7% in size because the errors never change sign. If some months had been over-forecast, WAPE would stay large while bias shrank.
```python
import pandas as pd

forecast_vs_actual = pd.DataFrame({
    "forecast": [100, 120, 90, 110],
    "actual":   [110, 130, 100, 120],
})

# Forecast minus actual: negative means we forecast too low
error = forecast_vs_actual["forecast"] - forecast_vs_actual["actual"]
total_actual = forecast_vs_actual["actual"].sum()

bias_pct = error.sum() / total_actual * 100
wape_pct = error.abs().sum() / total_actual * 100
print(round(bias_pct, 1), round(wape_pct, 1))
```
Output: `-8.7 8.7`. The forecast is about 8.7% too low overall, and it is wrong by about 8.7% of volume in total.
**Likely follow-ups:** 1) *What would you do?* Check why the forecast is low (missed promotions, new customers) and uplift it, since consistent bias is easier to fix than random error. 2) *Why not MAPE?* It averages percentages, so a small month with a big percentage miss distorts it.
**Common mistakes:** Averaging the monthly percentages; forgetting to say which sign means under-forecast; reading a low bias as "accurate" when WAPE is high.

### Q20 ⭐⭐⭐ 🟡 An item's forecast is consistently higher than actual sales. What are the consequences for inventory, cash and service, and how would you detect the pattern in data?
**Asked at:** commonly asked (no company-specific report found); forecast bias is a standard planning topic in practitioner articles (unverified).
**What the interviewer is checking:** Whether you can trace one data pattern to its money and service consequences, and name a way to detect it.
**Say this in the interview:** "Over-forecasting makes us buy or make more than we sell, so stock piles up, cash is tied up and storage and write-off costs rise. Ironically, service can still suffer because money and space go to the wrong items. To detect it, I compare forecast with actual each month by item and look at the running sum of errors: if it is positive for many months in a row, that is bias, not noise."
**Explain simply:**
- **Inventory:** extra units sit unsold, so inventory days rise; slow items may expire, go out of fashion or be discounted (write-off).
- **Cash:** every unsold unit is money already paid to the supplier. It is like hiring more people than the work needs: salary goes out, output does not rise.
- **Service:** the extra stock is often of the wrong items, so other items run out (stockouts) while the warehouse is full. Overall fill rate may not improve.
- **Detecting it:** per item and month, compute forecast minus actual; check the share of months with a positive error and the cumulative error. Random error flips sign; bias keeps one sign.
**Data and tables involved:** Monthly forecast table (sku, month, forecast), sales or demand actuals (sku, month, units), item master for category. First cuts: bias % by category, count of months over-forecast in the last 6 or 12, and the items with the largest cumulative excess.
**Likely follow-ups:** 1) *Why would a planner over-forecast on purpose?* To avoid stockouts or because sales targets are used as the forecast; that is a process issue to raise. 2) *What do you do about it?* Review the forecast method, remove the bias, and track the fix.
**Common mistakes:** Judging by one month; ignoring that actual sales may be capped by stockouts (true demand was higher); blaming the planner without checking where the forecast input came from.

### Q21 ⭐⭐⭐ 🟡 How does a business decide how much of an item to order and when, and how do reorder point and order quantity work together?
**Asked at:** commonly asked (no company-specific report found); replenishment logic appears in supply chain analyst guides and planning job postings (unverified).
**What the interviewer is checking:** Whether you understand the two decisions, "when" and "how much", and how they link.
**Say this in the interview:** "The reorder point says when to order: when stock falls to expected demand during the supplier's lead time plus safety stock. The order quantity says how much: balancing ordering cost against holding cost, and respecting supplier limits like minimum order quantity. Together they form a cycle: stock falls to the reorder point, we order the quantity, it arrives, and stock climbs back."
**Explain simply:**
- **Reorder point (ROP)** = average daily demand x lead time + safety stock. **Lead time** is the wait from placing an order to receiving it. **Safety stock** is the cushion against surprises.
- **Order quantity** can follow the Economic Order Quantity idea (big enough orders to avoid constant ordering costs, small enough to avoid heavy storage costs), then be rounded to pack sizes, truckloads or MOQ.
- A short lead time or steady demand means a lower reorder point; an uncertain supplier means a higher one.
- Many businesses also review on a fixed calendar (for example, weekly) and order up to a target level instead; the principle is the same.
**Likely follow-ups:** 1) *What if demand changes?* Recalculate demand and reorder point regularly. 2) *What is the stock position used?* On-hand plus already-ordered stock, minus reserved stock, so you do not order twice.
**Common mistakes:** Ignoring open purchase orders when checking the trigger; using the supplier's quoted lead time instead of the real one; one reorder point for all items regardless of how steady their demand is.

### Q22 ⭐⭐⭐ 🟡 Which stock-keeping data would you check first to confirm that the system inventory matches what is physically in the warehouse?
**Asked at:** commonly asked (no company-specific report found); data validation and reconciliation are recurring themes in supply chain analyst guides (unverified).
**What the interviewer is checking:** Whether you validate data against reality before trusting a dashboard.
**Say this in the interview:** "I would start with the last physical count or cycle count, compared with system on-hand quantity by SKU and location, then trace the differences through stock movements: receipts, picks, returns, transfers and adjustments. The biggest gaps by value tell me where to look first."
**Explain simply:**
- **System inventory** is what the software says is in the warehouse. **Physical inventory** is what staff actually find on the shelves. They drift apart through mis-picks, damage, theft, unrecorded returns and wrong receipts.
- A **cycle count** is counting a small part of the stock regularly, rather than shutting down for a yearly full count.
- Compare at SKU-location level (not just totals), because errors in two places can cancel each other out.
**Data and tables involved:** Inventory balance (sku, location, on-hand, status such as damaged or on hold), count results (sku, location, counted quantity, date), stock movement ledger (receipts, issues, transfers, adjustments with dates and users), and item master (unit of measure, cost). First cuts: variance by SKU and by location, adjustments by reason code, items with negative system stock.
**Likely follow-ups:** 1) *Which variances matter most?* High-value items and fast movers. 2) *What causes negative stock?* Picks recorded before receipts were posted.
**Common mistakes:** Comparing totals only; ignoring units of measure (cases vs pieces); counting stock that is on hold or in transit as available.

### Q23 ⭐⭐⭐ 🟡 What data sources (ERP, WMS, TMS, planning tool, supplier portals) feed a supply chain dashboard, and what does each system record?
**Asked at:** commonly asked (no company-specific report found); ERP, WMS and TMS data feeds are named in logistics analyst guides and job postings (unverified).
**What the interviewer is checking:** Whether you know where each number comes from and who owns it.
**Say this in the interview:** "The ERP holds orders, purchase orders, invoices and inventory value; the WMS holds what is physically in the warehouse and each pick and putaway; the TMS holds shipments, carriers and freight costs; the planning tool holds forecasts and plans; and supplier portals hold confirmed dates and shipment notices. A dashboard joins them on order, SKU and shipment keys."
**Explain simply:**
- **ERP** (Enterprise Resource Planning): the company's core system for orders, purchasing, finance and stock records. Think of it as the HR system's cousin: one place for official transactions.
- **WMS** (Warehouse Management System): runs the warehouse floor: locations, receiving, picking, packing, counts.
- **TMS** (Transportation Management System): plans and tracks shipments: carrier, route, freight cost, delivery status.
- **Planning tool:** forecasts, supply plans and inventory targets, often a separate product linked to the ERP.
- **Supplier portals:** order confirmations, advance shipping notices and supplier-reported dates.
- Keys must match across systems (order id, SKU, shipment id); mismatched ids or time zones are the usual dashboard headaches.
**Likely follow-ups:** 1) *Which is the source of truth for stock?* Usually WMS for physical, ERP for financial; reconcile them. 2) *How often do they refresh?* Varies; state the refresh time on the dashboard.
**Common mistakes:** Mixing systems with different definitions of "delivered"; not documenting refresh times; assuming one system has everything.

### Q24 ⭐⭐⭐ 🟡 How would you measure supplier performance, and what metrics beyond price would you put on a supplier scorecard?
**Asked at:** commonly asked (no company-specific report found); supplier scorecards appear in procurement analyst prep pages (unverified).
**What the interviewer is checking:** Whether you judge suppliers on total value, not just unit price.
**Say this in the interview:** "I would build a scorecard with delivery (on-time and in-full), quality (defect or rejection rate), lead time and its variability, responsiveness, cost stability, and compliance. Each gets a weight that matches what matters to the business, and I review it by supplier and by month."
**Explain simply:**
- **Delivery:** on-time %, in-full %, average delay.
- **Quality:** share of received units rejected or returned; number of complaints.
- **Lead time:** average and spread (a supplier that is sometimes 14 and sometimes 25 days forces extra safety stock).
- **Cost:** price, price changes, invoice accuracy (invoices matching orders).
- **Service and risk:** response time to queries, flexibility, documentation, financial or location risk.
- Weighted scores are a simplification; show the raw metrics next to the score so a buyer can challenge it.
- Like an HR performance review: several dimensions, agreed weights, and evidence behind the score.
**Likely follow-ups:** 1) *How would you weight them?* Ask the buyer and operations what hurts most; agree before measuring. 2) *What about tiny suppliers?* Flag low order counts, as percentages are unstable.
**Common mistakes:** Ranking on price alone; unclear metric definitions; letting one bad month define a supplier; not sharing the scorecard with the supplier.

### Q25 ⭐⭐⭐ 🟡 What is a purchase order, a goods receipt note and a supplier invoice, and how does the three-way match use them?
**Asked at:** commonly asked (no company-specific report found); three-way match coverage in prep sources is thin (unverified).
**What the interviewer is checking:** Whether you understand the control that stops the company paying for goods it did not order or receive.
**Say this in the interview:** "A purchase order is what we asked the supplier for, the goods receipt note is what actually arrived, and the supplier invoice is what they are charging. A three-way match compares all three on item, quantity and price before payment is released."
**Explain simply:**
- **Purchase order (PO):** the buyer's official order: items, quantity, agreed price, delivery date.
- **Goods receipt note (GRN):** the warehouse's record of what was actually received and checked.
- **Supplier invoice:** the supplier's bill.
- **Match:** if quantity and price agree within a set tolerance (a small allowed difference), the invoice is paid. If not, it goes to an exception list for someone to investigate.
- HR comparison: it is like checking that a timesheet, an approved shift schedule and the payroll amount all agree before paying.
- Simple versions (two-way match) compare only the PO and the invoice, which cannot catch short deliveries.
**Likely follow-ups:** 1) *What mismatches are common?* Short deliveries, price differences, duplicate invoices. 2) *What metric would you track?* Percentage of invoices matched automatically, and days to resolve exceptions.
**Common mistakes:** Matching on totals instead of line level; forgetting units of measure; ignoring partial receipts against one PO.

### Q26 ⭐⭐ 🟢 What is the difference between demand planning, supply planning and inventory planning?
**Asked at:** commonly asked (no company-specific report found); the three planning roles appear in planning job postings (unverified).
**What the interviewer is checking:** Whether you can tell apart three roles that sound alike.
**Say this in the interview:** "Demand planning forecasts how much customers will want. Supply planning works out how to meet that demand through production or purchasing. Inventory planning decides how much stock to hold, and where, to balance service and cost."
**Explain simply:**
- **Demand planning:** forecast by item, location and time, using history, promotions and seasons.
- **Supply planning:** converts the forecast into purchase orders, production runs and transfers, within capacity and lead times.
- **Inventory planning:** sets safety stock, reorder points and stock targets by location.
- They feed each other: forecast, then plan, then stock target, with S&OP (a regular cross-team meeting) aligning them.
**Likely follow-ups:** 1) *Who owns the forecast number?* Usually demand planning, agreed with sales. 2) *Where does the analyst help?* Measuring forecast accuracy and stock health.
**Common mistakes:** Treating the sales target as the forecast; mixing up the three roles' metrics.

### Q27 ⭐⭐ 🟢 What is procurement, and how is it different from purchasing and sourcing?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the vocabulary of buying.
**Say this in the interview:** "Procurement is the whole process of getting goods and services, including choosing suppliers, negotiating, ordering, receiving and paying. Sourcing is the earlier part: finding and selecting suppliers. Purchasing is the transaction itself: raising and placing the orders."
**Explain simply:**
- **Sourcing:** research the market, compare suppliers, agree contracts and prices.
- **Purchasing:** the day-to-day buying: purchase orders, follow-ups, deliveries.
- **Procurement:** the umbrella that covers both, plus supplier management and payment controls.
- Usage varies by company; some use "procurement" and "purchasing" as the same thing, so I state mine.
- HR analogy: sourcing is like finding candidates, purchasing is like issuing the offer letter and onboarding paperwork.
**Likely follow-ups:** 1) *What does a procurement analyst do?* Spend analysis, supplier scorecards, price tracking. 2) *What is spend analysis?* Grouping what the company spends by supplier and category to find savings.
**Common mistakes:** Treating the three words as exact synonyms in every company; focusing only on price.

### Q28 ⭐⭐ 🟢 What are inbound logistics and outbound logistics, and what is reverse logistics?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand the direction of flows.
**Say this in the interview:** "Inbound logistics is moving materials from suppliers into the company's warehouses or factories. Outbound logistics is moving finished goods from the company to customers. Reverse logistics is moving products back: returns, repairs, recycling or disposal."
**Explain simply:**
- **Inbound:** supplier pick-up or delivery, receiving, putaway; metrics such as dock-to-stock time.
- **Outbound:** picking, packing, shipping, last-mile delivery; metrics such as on-time delivery and cost per delivery.
- **Reverse:** customer returns, damaged goods, refurbishing; often costlier per unit and slower, so it needs its own tracking.
- Same trucks and warehouses may serve all three, so costs need clear allocation.
**Likely follow-ups:** 1) *Why does reverse logistics matter?* High return rates in e-commerce hurt margin. 2) *What data?* Return reason, condition, time to restock.
**Common mistakes:** Forgetting returns in cost analysis; mixing inbound and outbound freight costs.

### Q29 ⭐⭐ 🟢 What is a 3PL (third-party logistics provider), and why do companies outsource logistics?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand outsourcing as a business trade-off, not just a definition.
**Say this in the interview:** "A 3PL is an outside company that runs part of the logistics for another business, such as warehousing, transport or packing. Companies use them to avoid building their own warehouses and fleets, to scale up quickly in peak seasons and to access expertise."
**Explain simply:**
- **Third-party** means the first party is the seller, the second is the customer, and the third is the logistics specialist.
- **Why outsource:** variable cost instead of fixed investment; coverage in new cities; peak flexibility.
- **Trade-offs:** less direct control, data held by the partner, and contract terms to manage.
- **Analyst angle:** the 3PL's data feeds the dashboard, so define metrics (on-time, accuracy, cost) in the contract and check them independently.
- HR parallel: it resembles outsourcing payroll processing to a vendor.
**Likely follow-ups:** 1) *How would you judge a 3PL?* On-time delivery, pick accuracy, damage rate, cost per order. 2) *Risk?* Dependence on one provider.
**Common mistakes:** Assuming outsourcing is always cheaper; not defining service levels; trusting provider-reported numbers without checks.

### Q30 ⭐⭐ 🟢 What do WMS, TMS and ERP stand for, and what does each system manage?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the main systems an analyst pulls data from.
**Say this in the interview:** "WMS is Warehouse Management System, which runs the warehouse floor. TMS is Transportation Management System, which plans and tracks shipments. ERP is Enterprise Resource Planning, the company's core system for orders, purchasing, inventory value and finance."
**Explain simply:**
- **WMS:** locations, receiving, putaway, picking, packing, counts, labour tasks.
- **TMS:** carriers, routes, freight rates, shipment tracking, proof of delivery.
- **ERP:** orders, purchase orders, invoices, stock records, accounting; the HR system equivalent is an HRMS holding employee records.
- They exchange data, but each holds a different view, so numbers can differ until reconciled.
**Likely follow-ups:** 1) *Which would you use for pick accuracy?* WMS. 2) *For freight cost per kg?* TMS, with invoices from the ERP.
**Common mistakes:** Assuming all three hold the same stock figure; confusing the TMS (moving goods) with the WMS (storing and handling goods).

### Q31 ⭐⭐ 🟢 What is the bullwhip effect, and why do small changes in customer demand create large swings upstream?
**Asked at:** commonly asked (no company-specific report found); the bullwhip effect is a classic supply chain concept in guides (unverified).
**What the interviewer is checking:** Whether you grasp how distorted signals travel upstream.
**Say this in the interview:** "Bullwhip means small changes in customer demand become bigger swings in orders at each step back through retailer, distributor, manufacturer and supplier. Each party adds a buffer and reacts to the last order, so the distortion grows."
**Explain simply:**
- **Upstream** means towards suppliers; **downstream** means towards customers.
- Causes: ordering in large batches, adding safety stock at every level, reacting to promotions or price changes, and delays in sharing information.
- Example: shoppers buy 10% more one week; the retailer orders 20% more to be safe; the distributor sees that and orders 35% more. (Illustrative numbers only.)
- Effects: excess stock, then shortages, uneven factory use, and constant firefighting.
- Fixes: share real sales data, smaller more frequent orders, steadier pricing, and agreed forecasts.
- Like a manager over-hiring after one busy week, then freezing hiring when it quietens.
**Likely follow-ups:** 1) *How to detect it?* Compare variability of orders with variability of sales at each stage. 2) *What helps?* Sharing point-of-sale data.
**Common mistakes:** Blaming only demand; ignoring promotions and batching as causes.

### Q32 ⭐⭐ 🟢 What is MOQ (minimum order quantity), and how does it affect ordering decisions?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you see how supplier rules shape ordering.
**Say this in the interview:** "MOQ, minimum order quantity, is the smallest amount a supplier will accept per order. It can force us to order more than we need now, which raises stock and cash tied up, but may lower the unit price or freight cost."
**Explain simply:**
- If demand is 100 a month and the MOQ is 500, one order covers five months of stock.
- Trade-off: holding extra stock against paying a higher price or a surcharge for small orders.
- Options: combine items from the same supplier, order less often, negotiate, or find another supplier.
- MOQ may apply per item, per order value or per shipment; ask which.
- Orders are also rounded to pack sizes or truckloads.
**Likely follow-ups:** 1) *How does MOQ interact with EOQ?* Use the larger of the two. 2) *What data?* Supplier terms, demand rate, storage cost.
**Common mistakes:** Ignoring MOQ when calculating reorder quantity; not checking if MOQ is per item or per order.

### Q33 ⭐⭐ 🟢 What is backorder and what is the difference between a backorder and a lost sale?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate delayed sales from lost sales.
**Say this in the interview:** "A backorder is an order the customer is willing to wait for when stock is not available; we keep it and ship later. A lost sale is when the customer leaves or cancels and the revenue is gone."
**Explain simply:**
- Backorders still count as demand and need to be shipped when stock arrives; track how long they wait (backorder age).
- Lost sales are often invisible in the data because the order never gets recorded, so demand history can understate true demand.
- Long backorders raise cancellation risk and damage trust.
- Different products behave differently: customers wait for specialised items but switch for commodities.
**Likely follow-ups:** 1) *Which metric?* Backorder rate and age. 2) *How estimate lost sales?* From stockout days, cancelled orders and past conversion.
**Common mistakes:** Treating backorders as lost sales; forecasting from sales that were capped by stockouts.

### Q34 ⭐⭐ 🟢 What are the main modes of transport (road, rail, air, sea) and what trade-off does each offer between cost and speed?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can reason about the cost versus speed trade-off.
**Say this in the interview:** "Road is flexible and door-to-door with medium cost and speed. Rail is cheaper for heavy, long-distance cargo but slower and fixed to routes. Sea is the cheapest per unit for huge volumes but the slowest. Air is the fastest but the most expensive."
**Explain simply:**
- **Road:** trucks; good for short and medium distances and final delivery; affected by traffic and fuel costs.
- **Rail:** bulk goods, containers, long distances; needs terminals at both ends.
- **Sea:** international and heavy cargo; low cost per unit but long, variable transit times and port delays.
- **Air:** urgent, valuable or light goods such as medicines or electronics; high cost per kg.
- The choice also depends on how valuable the goods are: costly stock sitting on a slow ship is itself an inventory cost.
- Rankings are general; actual rates depend on route and season.
**Likely follow-ups:** 1) *What is multimodal transport?* Combining modes in one journey. 2) *What would you compare in data?* Cost per kg and transit-time spread by mode.
**Common mistakes:** Comparing only freight price and ignoring time and stock holding cost; forgetting that the first and last leg is usually by road.

### Q35 ⭐⭐ 🟢 What does cross-docking mean, and when is it used in a warehouse network?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand that stock can move through a warehouse without being stored.
**Say this in the interview:** "Cross-docking means goods arrive on an inbound truck and go straight onto an outbound truck with little or no storage in between. It cuts handling and holding time, so it suits fast-moving, predictable items."
**Explain simply:**
- Like a railway junction: passengers change trains without sitting in the station for days.
- Typical uses: fresh food, fast-moving consumer goods, and replenishing many stores from one supplier delivery.
- It needs accurate advance shipping information and tight timing, otherwise trucks wait and the saving disappears.
- Data angle: dock dwell time (how long goods sit on the dock), share of volume cross-docked, and inbound/outbound schedule match.
**Likely follow-ups:** 1) *Why not always cross-dock?* Demand and arrival times must be predictable; slow items still need storage. 2) *What does it save?* Putaway, storage and picking labour, plus holding cost.
**Common mistakes:** Treating it as "no inventory at all" (goods still wait briefly); ignoring the need for reliable supplier delivery data.

### Q36 ⭐⭐ 🟢 What is FIFO and FEFO in warehouse stock rotation, and which products need FEFO?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know that the rule for which stock leaves first affects waste.
**Say this in the interview:** "FIFO ships the oldest received stock first. FEFO ships the stock that expires first, even if it arrived later. Anything with an expiry date, like food, medicines and chemicals, needs FEFO."
**Explain simply:**
- **FIFO (first in, first out):** like a queue; whoever arrived first leaves first.
- **FEFO (first expired, first out):** like using the milk packet with the nearest date first, regardless of when you bought it.
- A new batch can have a shorter shelf life than an older one, so FIFO alone could let stock expire.
- Data needed: batch or lot number, manufacture and expiry dates, and quantity per batch per location.
**Likely follow-ups:** 1) *What metric shows the risk?* Stock near expiry as a share of total, and write-off value. 2) *Does FIFO still matter?* Yes for items without expiry that can age or become obsolete.
**Common mistakes:** Using FIFO for dated goods; forgetting that FEFO needs batch-level data, which many simple reports do not hold.

### Q37 ⭐⭐ 🟢 What are carrying cost (holding cost) and ordering cost, and what is included in each?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can name the two costs that pull order size in opposite directions.
**Say this in the interview:** "Carrying cost is the cost of keeping stock: money tied up, storage, insurance, damage and obsolescence. Ordering cost is the cost of placing each order, which does not depend on how many units you buy."
**Explain simply:**
- **Carrying cost** (often stated as a percentage of stock value per year; the percentage is company-specific): capital cost (cash locked in stock), warehouse space and staff, insurance, shrinkage (loss or theft), spoilage and obsolescence.
- **Ordering cost:** staff time to raise and approve a purchase order, transport per delivery, receiving and inspection effort, supplier invoice processing.
- Bigger, rarer orders lower ordering cost per unit but raise carrying cost; smaller, frequent orders do the opposite (Q39 shows the balance point).
- HR parallel: hiring in one big batch versus many small batches; each hiring round has a fixed cost, but idle new hires cost salary.
**Likely follow-ups:** 1) *Which is easier to measure?* Ordering cost; carrying cost needs an assumption for the cost of capital. 2) *Is purchase price included?* Not in these two; it is a separate cost.
**Common mistakes:** Counting the item's purchase price as ordering cost; ignoring the cost of capital in holding cost.

### Q38 ⭐⭐ 🟢 What is a perfect order, and which components does a perfect order rate combine?
**Asked at:** commonly asked (no company-specific report found); perfect order is listed in supply chain KPI guides (vendor blogs, unverified).
**What the interviewer is checking:** Whether you know that one failure anywhere spoils the order, and that definitions vary.
**Say this in the interview:** "A perfect order is delivered on time, complete, undamaged and with correct documents, all at once. The perfect order rate is the share of orders that pass every test, so it is always lower than any single component."
**Explain simply:**
- Common components (companies differ, so state yours): on time, in full, damage-free, and correct invoice and paperwork.
- Calculate it two ways: by checking each order against all tests (exact), or by multiplying component rates (an approximation that assumes failures are independent).
- Example with invented rates: 95% on time x 90% in full x 98% damage-free x 99% documents correct = 0.95 x 0.90 x 0.98 x 0.99 = 82.95%, about 83%. Four components that each look good give a visibly weaker whole.
**Likely follow-ups:** 1) *How does it relate to OTIF?* OTIF covers only two tests; perfect order adds more. 2) *What if one order fails two tests?* Count it once as imperfect; the exact method handles this, the multiplied one does not.
**Common mistakes:** Averaging the component rates instead of requiring all to pass; mixing definitions across teams.

### Q39 ⭐⭐ 🟡 Compute the Economic Order Quantity from the data below and explain what the formula balances.
Annual demand 12,000 units; ordering cost Rs 600 per order; holding cost Rs 24 per unit per year. EOQ = sqrt(2 x D x S / H).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can apply the formula and explain the trade-off, not just recite it.
**Say this in the interview:** "EOQ is about 775 units per order. It is the order size where yearly ordering cost and yearly holding cost are equal, which makes their total the lowest."
**Explain simply:**
- Ordering many small batches means high total ordering cost; ordering a few huge batches means a high stock to hold. EOQ finds the middle.
- Assumptions (a simplification): steady demand, fixed costs, no discounts, no stockouts.
**Worked example:**
- EOQ = sqrt(2 x 12,000 x 600 / 24) = sqrt(600,000) = 774.6, round to 775 units.
- Orders per year = 12,000 / 774.6 = 15.5, about one order every 3.4 weeks.
- Yearly ordering cost = 15.49 x 600 = Rs 9,295. Yearly holding cost = (774.6 / 2) x 24 = Rs 9,295 (average stock is half the order size). They match; total is about Rs 18,590 a year.
- Rounded to whole rupees; real orders would be rounded to pack sizes.
**Likely follow-ups:** 1) *What if demand doubles?* EOQ rises by a factor of the square root of 2 (about 1.41), not 2. 2) *When does EOQ fail?* With volatile demand, quantity discounts or minimum order quantities.
**Common mistakes:** Forgetting that average stock is half the order quantity; mixing monthly demand with yearly holding cost.

### Q40 ⭐⭐ 🟡 A safety-stock rule of thumb is z x demand variability x square root of lead time. Calculate the safety stock from the data below and explain why higher variability or longer lead time raises it.
Daily demand standard deviation 20 units, lead time 9 days, z = 1.65 (about 95% service).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute it and reason about what drives it.
**Say this in the interview:** "Safety stock is 1.65 x 20 x sqrt(9) = 99 units. It rises with demand swings and with lead time because there is more uncertainty to cover while waiting for the next delivery."
**Explain simply:**
- Standard deviation measures how much daily demand bounces around its average. z converts the service target into a multiplier (from memory: about 1.28 for 90%, 1.65 for 95%, 2.33 for 99%).
- Over a longer lead time there are more days for surprises to add up, but they partly cancel, so the effect grows with the square root of time, not directly with time.
**Worked example:**
- sqrt(9) = 3, so safety stock = 1.65 x 20 x 3 = 99 units.
- If lead time were 16 days, sqrt = 4 and stock = 132 units.
- If variability rose to 30 a day, stock = 1.65 x 30 x 3 = 148.5, about 149 units.
- Assumes demand is roughly normal, days are independent and lead time is fixed (Q49 relaxes the last).
**Likely follow-ups:** 1) *Does this include average demand during lead time?* No, that sits in the reorder point (Q16). 2) *What if the supplier is also variable?* Add lead-time variability (Q49).
**Common mistakes:** Using the standard deviation of monthly demand with a daily lead time; multiplying by lead time instead of its square root.

### Q41 ⭐⭐ 🟡 Rank the SKUs below into A, B and C classes by share of annual revenue and say what you would do differently for each class.
Annual revenue (Rs lakh): SKU1 500, SKU2 250, SKU3 100, SKU4 60, SKU5 40, SKU6 30, SKU7 10, SKU8 10. Use A = first 70-80% cumulative, B = next 15%, C = rest.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you sort first, use cumulative share, and turn classes into actions.
**Say this in the interview:** "Total revenue is Rs 1,000 lakh. SKU1 and SKU2 give 75% so they are A, SKU3 and SKU4 take the next 16% so they are B, and SKU5 to SKU8 are the last 9% so they are C."
**Explain simply:**
- Sort by revenue, high to low; compute each SKU's share and the running (cumulative) share.
- Cumulative share: SKU1 50%, SKU2 75%, SKU3 85%, SKU4 91%, SKU5 95%, SKU6 98%, SKU7 99%, SKU8 100%.
- The cut-offs are a convention, not a law. SKU4 starts below 90% and ends at 91%, so I keep it in B (the 15% band is approximate). SKU1 alone is 50%, below 70%, so A must include SKU2.
- **A (2 SKUs, 75% of revenue):** tight monitoring, frequent forecast review, high service level, close supplier contact.
- **B (2 SKUs, 16%):** standard rules, periodic review.
- **C (4 SKUs, 9%):** simple rules, bigger and fewer orders, minimal attention; consider dropping the dead ones.
- Shares computed by code; rounded to whole percent.
**Likely follow-ups:** 1) *Why only 2 of 8 as A?* Revenue is usually concentrated in a few items (a Pareto pattern). 2) *Is revenue the only basis?* No; margin, volume or criticality can be used.
**Common mistakes:** Not sorting before the cumulative sum; treating C items as unimportant even if they are critical (for example a safety part).

### Q42 ⭐⭐ 🟡 A warehouse has the pick data below. Compute pick accuracy and lines picked per labour hour for each shift and say which shift is better.
Shift A: 4,800 lines picked, 48 errors, 80 labour hours. Shift B: 3,600 lines, 18 errors, 50 labour hours.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you look at quality and productivity together and note the limits of the comparison.
**Say this in the interview:** "Shift B is better on both: 99.5% accuracy against 99.0%, and 72 lines per labour hour against 60. I would still check that the two shifts handle similar work."
**Explain simply:**
- **Pick accuracy** = correct lines / lines picked. A pick line is one item-and-quantity on an order.
- **Lines per labour hour** = lines picked / hours worked, a productivity measure.
**Worked example:**
- Shift A: (4,800 - 48) / 4,800 = 99.0%; 4,800 / 80 = 60 lines per hour; 10 errors per 1,000 lines.
- Shift B: (3,600 - 18) / 3,600 = 99.5%; 3,600 / 50 = 72 lines per hour; 5 errors per 1,000 lines.
- B has half the error rate and is 20% more productive (72 vs 60).
- Caveats: mix of items, order sizes, headcount, experience and seasonality can differ.
**Likely follow-ups:** 1) *Would you rank staff on this?* Be careful: use it to improve processes; individual-level data is sensitive, so follow company policy. 2) *What would explain the gap?* Training, layout, or easier orders.
**Common mistakes:** Judging on volume alone; using headcount instead of actual hours worked (attendance data matters).

### Q43 ⭐⭐ 🟡 Compute supplier on-time delivery percentage and average delay for the supplier data below, and say what you would ask the buyer.
Supplier X: 20 deliveries, 14 on time; the 6 late ones were 2, 3, 3, 5, 6, 9 days late.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate how often a supplier is late from how late it is.
**Say this in the interview:** "On-time delivery is 70%. When late, the average delay is 4.7 days; spread over all 20 deliveries it is 1.4 days. I would ask the buyer why the late ones happened, especially the 9-day case."
**Explain simply:**
- On-time % = 14 / 20 = 70%.
- Total delay = 2+3+3+5+6+9 = 28 days. Average delay of late deliveries = 28 / 6 = 4.67 days (median 4). Average over all deliveries = 28 / 20 = 1.4 days. State which one you use.
- Questions for the buyer: Was the promised date realistic? Did the supplier warn us? Were the late ones the same product or the same period? Is there a tolerance window in the contract? Did late deliveries hurt production or stockouts?
- Rounded to 1 decimal place.
**Likely follow-ups:** 1) *Is 70% good?* Compare with the target and other suppliers; I would not quote a benchmark. 2) *Does early count as on time?* Define it; early can cause storage problems.
**Common mistakes:** Averaging delay over only late deliveries without saying so; ignoring that one 9-day outlier may matter more than the average.

### Q44 ⭐⭐ 🟡 Compute order cycle time and its stage breakdown from the timestamps below and say where the bottleneck is.
Order received 10:00; picking started 11:30; packed 14:30; handed to carrier 16:00; delivered next day 12:00.
**Asked at:** commonly asked (no company-specific report found); order cycle time appears in warehouse KPI guides (vendor blogs, unverified).
**What the interviewer is checking:** Whether you break a total into stages and find the largest.
**Say this in the interview:** "Total cycle time is 26 hours. Transit is 20 hours, 77% of the total, so it is the biggest stage. Inside the warehouse, picking and packing take 3 hours, the biggest internal stage."
**Explain simply:**
- Order received to picking started: 1.5 hours (waiting in queue).
- Picking started to packed: 3 hours.
- Packed to handed to carrier: 1.5 hours (waiting for pickup).
- Handed to carrier to delivered: 20 hours (16:00 to 12:00 next day).
- Total = 1.5 + 3 + 1.5 + 20 = 26 hours. Warehouse part = 6 hours (23%); transit = 20 hours (77%).
- The clock start is a definition choice (order placed, paid or released); say which you use. Here the bottleneck is transit, but a 20-hour overnight leg may be normal, so compare with the promised delivery time before calling it a problem. Inside the warehouse, the 1.5-hour waits (3 hours combined) equal the pick time, which is easy to improve.
**Likely follow-ups:** 1) *What would you chart?* Median and 90th percentile of each stage by day. 2) *How to separate working from waiting time?* Compare with shift timings.
**Common mistakes:** Ignoring night hours; using only averages and hiding the slow tail.

### Q45 ⭐⭐ 🟡 Compute transport cost per kg and per delivery for the data below, and say which route needs investigation.
Route 1: Rs 24,000, 2,000 kg, 80 deliveries. Route 2: Rs 18,000, 900 kg, 60 deliveries.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you test cost against more than one denominator.
**Say this in the interview:** "Per delivery both routes cost Rs 300, but per kg Route 2 is Rs 20 against Rs 12 for Route 1. Route 2 carries very light loads per stop, so that is the one to investigate."
**Explain simply:**
- Route 1: 24,000 / 2,000 = Rs 12 per kg; 24,000 / 80 = Rs 300 per delivery; 25 kg per delivery.
- Route 2: 18,000 / 900 = Rs 20 per kg; 18,000 / 60 = Rs 300 per delivery; 15 kg per delivery.
- Route 2 is 67% more expensive per kg (20 vs 12). The cost per stop is the same, so the issue is small drops, not an expensive vehicle.
- Next checks: can stops be combined, is the vehicle too big, is there a minimum order value, and is distance or time different?
**Likely follow-ups:** 1) *Is per kg the only measure?* No; also cost per km, per order value and per cubic metre for bulky items. 2) *What if Route 2 serves a remote area?* Then higher cost may be justified; compare with value delivered.
**Common mistakes:** Judging by total cost alone; not noticing that the deliveries are of different sizes.

### Q46 ⭐⭐ 🟡 Compute inventory accuracy from a cycle count and list the first checks if it is low.
Counted 500 locations; 460 matched system quantity exactly; 25 differed by 1-2 units; 15 differed by more.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you define accuracy clearly and have a method for chasing mismatches.
**Say this in the interview:** "Exact-match accuracy is 460 / 500 = 92%. If a 1-2 unit tolerance is allowed it is 97%. The 15 large differences, 3% of locations, are what I would investigate first."
**Explain simply:**
- A cycle count is counting a few locations regularly instead of shutting down for a full stocktake.
- Exact: 460 / 500 = 92%. Within tolerance: (460 + 25) / 500 = 97%. Large gaps: 15 / 500 = 3%.
- State whether accuracy is by location count (used here) or by value; they can differ a lot.
- First checks: recent receipts and putaway not yet booked, picks booked to the wrong location or item, damaged or returned stock, unit-of-measure mix-ups (box vs piece), items moved without a transaction, timing of the count versus system updates, and any theft pattern.
**Likely follow-ups:** 1) *Which differences first?* Largest by value, then repeat offenders. 2) *Why does it matter?* Wrong system stock causes false stockouts and false availability.
**Common mistakes:** Counting while transactions are still being posted; reporting a tolerance-based figure as exact.

### Q47 ⭐⭐ 🟡 What is a service level target, and how do service level, safety stock and inventory cost trade off against each other?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand that higher service is not free and that costs rise faster at the top.
**Say this in the interview:** "A service level target is the share of demand or cycles we promise to serve from stock, for example 95%. Higher targets need more safety stock, and the stock needed rises steeply near the top, so I weigh it against the cost of a lost sale."
**Explain simply:**
- Two common definitions: cycle service level (share of order cycles with no stockout) and fill rate (share of demand met from stock). Say which one you use.
- Using the Q40 data (daily standard deviation 20, lead time 9 days, z values from memory, unverified): 90% needs about 77 units, 95% about 99, 99% about 140. Going from 95% to 99% adds about 41 more units (41%) for 4 points more service.
- So the right target differs by item: high for important, high-margin items; lower for cheap, slow or easily substituted ones (links to ABC, Q48).
- Yearly holding cost = holding cost per unit x (average cycle stock + safety stock), so every extra unit of safety stock is a running cost.
**Likely follow-ups:** 1) *How to choose the target?* Compare the cost of a stockout with the cost of holding extra stock. 2) *Can we raise service without more stock?* Yes, by cutting lead time or forecast error.
**Common mistakes:** Setting 99% for every item; confusing cycle service level with fill rate.

### Q48 ⭐⭐ 🟡 How would you use ABC analysis together with XYZ analysis (demand variability) to set a different stocking policy for each segment?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you combine value and predictability into practical rules.
**Say this in the interview:** "ABC says how much an item matters; XYZ says how predictable its demand is. Putting them in a grid gives nine segments, each with its own stocking rule: for example AX can run lean, while AZ needs close attention."
**Explain simply:**
- **XYZ:** based on the coefficient of variation (CV = standard deviation / average demand). Typical cut-offs, which are company choices: X low (say CV below 0.5), Y medium, Z high (say above 1).
- **AX:** high value, steady demand: tight, automated replenishment, low safety stock.
- **AY / AZ:** high value, erratic: higher safety stock or flexible suppliers, human review, collaboration with sales.
- **BX / BY:** standard reorder point rules.
- **CX:** simple, large orders, minimal review. **CZ:** hold little, make or buy to order, or consider dropping.
- Steps: calculate annual revenue and demand CV per SKU, classify, then set review frequency, service target and forecasting method for each cell.
**Likely follow-ups:** 1) *Which cell is the biggest risk?* AZ: valuable and unpredictable. 2) *How often to redo it?* Periodically, as demand patterns change.
**Common mistakes:** Computing CV from too few periods; including promotion months without adjusting, which inflates variability.

### Q49 ⭐⭐ 🟡 A buyer says a supplier's lead time is 14 days, but your data shows 14 days sometimes and 25 days at other times. How do you describe and quantify lead time variability?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you replace a single "typical" number with a distribution, and see its business effect.
**Say this in the interview:** "I would calculate lead time per order from order date to receipt date, then report average, standard deviation, and percentiles, not one figure. Planning on 14 days when it is sometimes 25 leads to stockouts."
**Explain simply:**
- Per order: lead time = goods receipt date minus purchase order date. Then summarise by supplier and item.
- Illustration with invented data: 20 orders, 12 at 14 days and 8 at 25 days. Mean = 18.4 days; standard deviation = 5.4 days (5.5 if you treat it as a sample); CV (standard deviation / mean) about 0.29; the 90th percentile is 25 days. The buyer's "14 days" is right 60% of the time, but late 40% of the time by 11 days.
- Business effect (demand 100 units/day, daily standard deviation 20, z = 1.65, a common textbook formula, from memory): safety stock treating lead time as fixed at 14 days is about 123 units; including lead-time variability (z x square root of [average lead time x demand variance + demand squared x lead-time variance]; variance is the standard deviation squared) it is about 900 units. Variable supply is expensive.
- Next steps: look for a pattern (month, product, route) and agree a realistic planning lead time or work with the supplier.
**Likely follow-ups:** 1) *Which lead time to plan with?* A percentile such as the 90th, or model the variability explicitly. 2) *Quoted vs actual?* Track the gap as a supplier metric.
**Common mistakes:** Averaging away the spread; mixing different items or order types in one lead time.

### Q50 ⭐⭐ 🟡 What is the order-to-cash cycle and what are the Excel or SQL steps to measure each stage from system timestamps?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can turn a business process into date differences.
**Say this in the interview:** "Order-to-cash runs from a customer placing an order to the company receiving the money: order, approval, shipping, delivery, invoice, payment. I take the date difference between each pair of timestamps for every order, then summarise."
**Explain simply:**
- Stages: order placed, approved (credit check), shipped, delivered, invoiced, paid. Each timestamp comes from a different system (order system, warehouse, transport, finance).
- In Excel: stage days = later date column minus earlier date column, then pivot by month, customer or region and look at median and 90th percentile. Watch for blanks (not yet shipped or paid) and use IF to exclude them.
- In SQL (SQLite). Tiny invented table `orders` (dates in March and April 2026; shown as day numbers from the order date): order 1 approved day 0, shipped day 2, delivered day 5, invoiced day 2, paid day 32; order 2 approved 0, shipped 0, delivered 3, invoiced 0, paid 39; order 3 approved 1, shipped 5, delivered 7, invoiced 5, paid 41.
```sql
select order_id,
  julianday(approved_ts)-julianday(order_date)  as days_to_approve,
  julianday(shipped_ts)-julianday(approved_ts)  as days_to_ship,
  julianday(delivered_ts)-julianday(shipped_ts) as days_in_transit,
  julianday(paid_ts)-julianday(invoice_ts)      as days_to_collect,
  julianday(paid_ts)-julianday(order_date)      as order_to_cash_days
from orders;
```
```
order_id  days_to_approve  days_to_ship  days_in_transit  days_to_collect  order_to_cash_days
1         0.0              2.0           3.0              30.0             32.0
2         0.0              0.0           3.0              39.0             39.0
3         1.0              4.0           2.0              36.0             41.0
```
Average order-to-cash for these three orders is 37.3 days, and collection (waiting for payment) is the largest stage.
- Other databases use date subtraction or DATEDIFF instead of julianday.
**Likely follow-ups:** 1) *Which stage do finance care about?* Collection time, because it ties up cash. 2) *How to handle orders still open?* Exclude them or flag them as incomplete to avoid bias.
**Common mistakes:** Mixing time zones or date-only and timestamp columns; including cancelled or partially shipped orders without a rule.

### Q51 ⭐⭐ 🟡 How would you build a stockout or low-stock early-warning report, and what columns and thresholds would it need?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you design an actionable report, not just a list of zero-stock items.
**Say this in the interview:** "I would show, per SKU and location, stock on hand versus expected demand and incoming supply, and flag items whose days of cover is shorter than the replenishment lead time. That warns us before the shelf is empty."
**Explain simply:**
- Columns: SKU, location, on-hand quantity, reserved or allocated quantity, available quantity (on hand minus reserved), open purchase orders and expected arrival date, average daily demand (recent 7-28 days), days of cover (available / daily demand), supplier lead time, reorder point, ABC class, last stock update time.
- Thresholds: red if available is zero or days of cover is less than lead time with no inbound order due in time; amber if available is below the reorder point or cover is below lead time plus a buffer. Values are set by the business and differ by item class.
- Make it actionable: sort by revenue at risk, show owner and suggested order quantity, and filter out discontinued or seasonal-off items.
- Check data quality first: stale stock figures and wrong stock records (Q46) cause false alarms.
**Likely follow-ups:** 1) *How often refresh?* As often as the stock data updates; fast-moving items daily or better. 2) *How to avoid alert fatigue?* Prioritise by value and use few, clear levels.
**Common mistakes:** Alerting only at zero (too late); ignoring inbound stock already on order; using total stock instead of available stock.

### Q52 ⭐⭐ 🟡 What master data fields (SKU, supplier, location, unit of measure, lead time, MOQ) do supply chain analyses depend on, and what data quality problems do you look for in them?
**Asked at:** commonly asked (no company-specific report found); data validation and master data checks are themes in supply chain analyst prep guides (unverified).
**What the interviewer is checking:** Whether you know that reports are only as good as the reference data behind them, and can name concrete checks.
**Say this in the interview:** "Almost every supply chain number joins back to master data: the SKU list, supplier list, locations, units of measure, lead times and MOQs. I check for duplicates, blanks, wrong units and stale values before I trust any report."
**Explain simply:**
- **Master data** is the slow-changing reference list a business keeps, like the employee master in HR (one row per person with grade, location, manager). In supply chain the equivalents are:
- **SKU** (stock-keeping unit, one sellable item variant), **supplier**, **location** (warehouse, store), **unit of measure** (each, case, pallet), **lead time** (days from order to arrival) and **MOQ** (minimum order quantity a supplier accepts).
- Problems to look for: duplicate SKUs or suppliers with spelling variants; blanks or zero lead times; one SKU with two units of measure and no conversion factor; discontinued items still active; lead time in the system far from the actual receipt dates; MOQ that is not a multiple of the case size; location codes that differ between systems.
- Quick first checks: count distinct keys against rows, null counts per field, and compare master lead time with actual (receipt date minus order date).
**Likely follow-ups:** 1) *Who owns master data?* Usually a master data team or planners; the analyst reports issues, does not silently fix them. 2) *How would you show the impact?* Quantify, for example "40 SKUs have lead time 0, which understates their reorder point".
**Common mistakes:** Assuming the system fields are correct; joining on names instead of IDs; cleaning data in your own file and never telling the owner.

### Q53 ⭐⭐ 🟡 How do you handle units of measure (each, case, pallet, kg) when combining inventory or sales data from different systems?
**Asked at:** commonly asked (no company-specific report found); unit-of-measure mismatch appears as a data-quality theme in supply chain analyst guides (unverified).
**What the interviewer is checking:** Whether you avoid adding unlike things, such as cases plus pieces, and know the fix is a conversion table.
**Say this in the interview:** "I convert everything to one base unit, usually the smallest sellable unit (each), using a SKU-level conversion table, and I keep the original unit in a column so I can audit it."
**Explain simply:**
- A **unit of measure (UoM)** is how a quantity is counted: each, case (say 12 pieces), pallet (say 40 cases), or kg for loose goods. One system may record purchases in cases and another record sales in pieces.
- Build a **conversion table**: SKU, from-unit, to-unit, factor. Join it to each dataset, multiply, then sum.
- Check that factors exist for every SKU, are not zero, and have not changed over time (pack sizes get redesigned).
- Weight-based items (kg) and fixed-count items need separate treatment; do not mix kg and each in one total.
- Sanity test: after converting, compare totals with a known figure, for example sales units against finance reports.
**Likely follow-ups:** 1) *What if a SKU has no factor?* List it, ask the owner, and exclude it from totals with a clear note rather than guessing. 2) *Why keep the original unit?* So any number can be traced back to the source.
**Common mistakes:** Summing mixed units; applying the factor in the wrong direction (cases to each means multiply, each to cases means divide); ignoring pack-size changes over time.

### Q54 ⭐⭐ 🟡 How do seasonality, promotions and festivals (for example Diwali or end-of-season sales) show up in demand data, and how would you treat them before forecasting?
**Asked at:** commonly asked (no company-specific report found); Indian retail and e-commerce context (Diwali, end-of-season sales) added as a gap-fill.
**What the interviewer is checking:** Whether you understand that history contains one-off spikes and calendar patterns, and that you adjust before forecasting.
**Say this in the interview:** "I would separate the repeating calendar pattern (seasonality) from one-off promotion effects, flag the festival and promotion periods in the data, and clean or model them so the baseline forecast is not distorted."
**Explain simply:**
- **Seasonality** is a pattern that repeats on a calendar, like winter wear selling in winter or attendance dropping around a festival week.
- A **promotion** is a planned price cut or campaign; it pulls demand forward and can cause a dip afterwards.
- **Festivals** such as Diwali move with the lunar calendar, so the date changes each year; use a festival flag rather than a fixed month.
- In data they show as spikes at a SKU or category level, often followed by a lull.
- Treatment: add flag columns (promo, festival, price); compare against the same period last year; either remove the promo uplift to get a baseline demand, or model the uplift separately; do not let one spike inflate the normal forecast.
- Also check stockouts in the period, because a flat week may be missing demand (see Q56).
**Likely follow-ups:** 1) *How much history do you need?* At least two full years to see a yearly pattern. 2) *New SKUs?* Borrow the pattern of similar items.
**Common mistakes:** Using last month as the baseline when it held a sale; treating a spike as the new normal; fixed-date festival flags.

### Q55 ⭐⭐ 🟡 What is a demand forecast at SKU level versus category level, and why is aggregate forecast usually more accurate than item-level forecast?
**Asked at:** commonly asked (no company-specific report found); forecast aggregation is a standard demand planning topic (unverified).
**What the interviewer is checking:** Whether you understand why errors cancel when you add items together.
**Say this in the interview:** "SKU-level is the forecast for each individual item and location; category level adds many of them together. Aggregates are usually more accurate because the random over- and under-forecasts of individual items offset each other."
**Explain simply:**
- **SKU-level** forecast: one item, often one location, and the level that drives ordering. **Category-level**: a group such as "biscuits", better for budgets and S&OP.
- Think of HR: predicting exactly which employee will resign next month is hard, predicting the total number of resignations is easier.
- Item demand is lumpy and noisy, especially for slow sellers; when you add 100 items, one item's miss of plus 5 is cancelled by another's minus 5.
- Practical use: forecast at the aggregate level, then split down using recent shares (top-down), or forecast each SKU and check that the sum is sensible (bottom-up).
- But aggregate accuracy can hide a problem: the category looks fine while some SKUs are stocked out and others overstocked.
**Likely follow-ups:** 1) *Which level do you use for ordering?* SKU-location, since stock sits there. 2) *Which accuracy metric?* Report WAPE at each level and compare.
**Common mistakes:** Reporting only category accuracy as if it proved SKU accuracy; splitting the aggregate by outdated shares.

### Q56 ⭐⭐ 🟡 What is the difference between demand and sales in the data, and how would you estimate demand for an item that was out of stock for part of the period?
**Asked at:** commonly asked (no company-specific report found); sales versus demand is a standard demand planning concept (unverified).
**What the interviewer is checking:** Whether you know sales data is censored (cut off) by stock availability.
**Say this in the interview:** "Sales is what we managed to sell; demand is what customers wanted. When an item is out of stock, sales understate demand, so I estimate demand for those days from in-stock days or similar items."
**Explain simply:**
- If an item sells 100 a day for 20 days then sits at zero stock for 10 days, the data shows 0 sales on those days, but customers still wanted it.
- Estimating demand: (1) flag out-of-stock days using daily stock snapshots; (2) fill those days with the average rate on in-stock days, adjusted for weekday and season; (3) optionally use a similar item or the same item at a nearby location; (4) record lost-sales estimates separately.
- Some customers substitute another brand, so part of the lost demand moves elsewhere; check sales of substitutes.
- Without stock data you can spot suspicious runs of zeros, but cannot be sure.
- This matters because a forecast trained on censored sales will under-order and repeat the stockout.
**Likely follow-ups:** 1) *What data do you need?* Daily stock by SKU-location plus sales. 2) *Other sources of demand?* Searches, wishlists, unfulfilled orders, backorders.
**Common mistakes:** Treating zero sales as zero demand; filling gaps with the overall average including promo days.

### Q57 ⭐⭐ 🟡 How does a replenishment model for a quick-commerce dark store differ from one for a central warehouse supplying retail stores?
**Asked at:** commonly asked (no company-specific report found); quick-commerce dark store replenishment is an Indian-context gap-fill.
**What the interviewer is checking:** Whether you see how small, fast stores need different timing, assortment and accuracy from large stock-holding warehouses.
**Say this in the interview:** "A dark store has a tiny space, a few thousand SKUs, orders in minutes, and perishables, so it needs daily or even intra-day replenishment at SKU level. A central warehouse replenishes retail stores in bigger, scheduled batches and pools stock across many outlets."
**Explain simply:**
- A **dark store** is a small shop closed to walk-in customers, used only to pack online orders for delivery in minutes (e.g. 10 to 20).
- Dark store: limited shelf space, so the cap on stock per SKU matters more than economic order quantity; short lead time from the warehouse (hours); forecast by hour and by neighbourhood; heavy waste risk on fresh items; stockouts visible immediately.
- Central warehouse: larger, less frequent orders; trucks must be filled; order quantity can follow cost trade-offs; one forecast serves many stores and aggregate demand is steadier.
- Dark store key metrics: availability at order time, wastage, picks per hour, order-to-delivery time. Warehouse: fill rate to stores, inventory days, truck utilisation.
**Likely follow-ups:** 1) *What triggers dark store orders?* Stock falling below a min level with a daily forecast to a max (par) level. 2) *How do you assign which SKUs?* By local sales and space.
**Common mistakes:** Using weekly average for hourly business; ignoring shelf life; applying warehouse safety stock logic unchanged.

### Q58 ⭐⭐ 🟡 How would you analyse delivery delays for a courier network by origin, destination, hub and carrier, and what would you look for?
**Asked at:** commonly asked (no company-specific report found); last-mile delay drivers and on-time drop root cause appear in logistics analyst prep pages (Interview Query, Dataford, unverified, partly gated).
**What the interviewer is checking:** Whether you break delay down into stages and dimensions before blaming one cause.
**Say this in the interview:** "I would first define a delay clearly (actual delivery later than the promised date), then calculate the late percentage and average days late by origin, destination, hub and carrier, and compare them with the network average to find where delays concentrate."
**Explain simply:**
- A **hub** is a sorting centre where parcels from many origins are gathered and sent onward; **carrier** is the company moving them.
- Data: shipment ID, origin, destination, carrier, promised date, scan events (picked up, hub in, hub out, out for delivery, delivered, failed attempt).
- Cuts: late rate by lane (origin to destination), by hub (dwell time between in and out scans), by carrier, by day of week, by parcel weight, and by delivery attempts.
- Look for: one hub with long dwell time (capacity), one lane with a slow carrier, failed first attempts (wrong address, customer absent), pickup delays at origin, spikes on specific days or festivals.
- Check volume: a hub with a high late rate on 20 parcels is weak evidence.
**Likely follow-ups:** 1) *Stage view?* Split total time into pickup, line-haul, hub, last mile. 2) *Next step?* Share the ranked lanes with operations to confirm causes.
**Common mistakes:** Reporting the average only (hides long tails); mixing promised-date rules across carriers; ignoring failed attempts.

### Q59 ⭐⭐ 🟡 What is the difference between a make-to-stock and a make-to-order business, and how does that change which planning metrics matter?
**Asked at:** commonly asked (no company-specific report found); planning-strategy basics (unverified).
**What the interviewer is checking:** Whether you know the production trigger differs and so do the metrics that matter.
**Say this in the interview:** "Make-to-stock builds goods from a forecast and holds finished stock; make-to-order starts production only after a customer order. So make-to-stock watches forecast accuracy, inventory days and stockouts, while make-to-order watches order lead time, capacity and on-time delivery."
**Explain simply:**
- **Make-to-stock (MTS):** like packaged snacks; factory produces ahead, customers buy from shelves. Risk: unsold stock if the forecast is wrong.
- **Make-to-order (MTO):** like a custom-built machine or tailored uniform; nothing is built until ordered. Risk: long waits and idle or overloaded capacity.
- MTS metrics: forecast bias and WAPE, fill rate, inventory turns, aged stock, service level.
- MTO metrics: quote-to-delivery lead time, on-time delivery, capacity utilisation, order backlog, raw material availability.
- Many firms mix both (assemble-to-order): hold components, finish on order.
**Likely follow-ups:** 1) *Which carries more cash risk?* MTS, as stock is held. 2) *Which needs forecast?* Both, MTO forecasts capacity and raw materials.
**Common mistakes:** Judging an MTO business on fill rate from shelf stock; ignoring raw material planning in MTO.

### Q60 ⭐⭐ 🟡 A plant uses workforce planning like a warehouse does: how would you compute the labour hours needed from the order volume forecast, and which HR data would you join?
Forecast 20,000 order lines per day; standard 30 lines per labour hour; 8 productive hours per shift; absenteeism 10%.
**Asked at:** commonly asked (no company-specific report found); warehouse labour planning is a gap-fill with an HR flavour.
**What the interviewer is checking:** Whether you convert volume into hours, then into people, with absenteeism handled correctly.
**Say this in the interview:** "20,000 lines at 30 lines per hour is about 667 labour hours; at 8 productive hours per person that is about 83 people actually working, and because 10% are absent I need to roster about 93."
**Explain simply:**
- **Order line** is one item on an order; **standard** is the expected output per labour hour.
- Hours needed = lines divided by standard. People working = hours divided by productive hours per shift. Roster = people working divided by (1 minus absenteeism), because only 90% of the roster turns up.
- The common shortcut of adding 10% gives 92 (91.7); dividing by 0.9 gives 93 (92.6); we round up to whole people.
- **HR data to join:** roster and shift plans, attendance and leave, headcount by role (permanent, contract, agency), skills and training (who can use forklifts), overtime rules and limits, attrition and hiring lead time, shift-wise absenteeism history.
- Assumption: 30 lines per hour already reflects productive time; the standard should be checked against actuals by role.
**Worked example:** 20,000 / 30 = 666.7 labour hours; 666.7 / 8 = 83.3 people working; 83.3 / 0.9 = 92.6, rounded up to 93 rostered per day (all figures rounded to one decimal).
**Likely follow-ups:** 1) *Peak days?* Use a higher forecast and flexible agency staff. 2) *Different tasks?* Use separate standards for picking, packing, loading.
**Common mistakes:** Multiplying by 1.1 instead of dividing by 0.9; forgetting breaks; applying one standard to all tasks.

### Q61 ⭐⭐ 🔴 On-time delivery fell from 94% to 86% over two weeks. Walk through how you would investigate, naming the data cuts and systems you would use.
**Asked at:** commonly asked (no company-specific report found); on-time drop diagnosis is a common logistics and supply chain case (Interview Query, Dataford, unverified).
**What the interviewer is checking:** A structured, step-by-step investigation: confirm, localise, find the cause, propose action.
**Say this in the interview:** "First I confirm the drop is real and the definition has not changed, then I break it down by customer, product, warehouse, carrier and lane to see where it concentrates, and then I trace the stage in the order cycle where the time is lost."
**Explain simply:**
- **Step 1, validate:** same definition (on time against promised date), same data feed, no new customers or date rule change, enough volume.
- **Step 2, cut the data** (ERP for orders and promised dates, WMS for picking and dispatch, TMS or carrier data for transit): by warehouse, carrier, lane, customer, product, order size, day, and week-on-week.
- **Step 3, stage timing:** order to pick, pick to dispatch, dispatch to delivery; which stage got longer?
- **Step 4, link to events:** stockouts, staff absence (attendance data), a carrier change, weather, a promotion causing volume spikes.
- **Step 5, quantify and recommend:** share how many late orders each cause explains, and a fix and owner.
- Eight points over two weeks is large, so look for a single step change date.
**Likely follow-ups:** 1) *Single cause or many?* Use contribution analysis. 2) *Is it the customer's promised date?* Check if promises became tighter.
**Common mistakes:** Jumping to a cause; using averages not distributions; not checking definition or data issues first.

### Q62 ⭐⭐ 🔴 Fill rate is stable at 96% but OTIF dropped from 92% to 83%. What does this pattern suggest and how would you test the hypotheses?
**Asked at:** commonly asked (no company-specific report found); reading fill rate and OTIF together is a standard KPI-guide theme (vendor blogs, unverified).
**What the interviewer is checking:** Whether you know OTIF needs both in-full and on-time, so a timing problem can drop OTIF without touching fill rate.
**Say this in the interview:** "Fill rate measures quantity shipped against ordered; OTIF also needs the delivery date to be met. If fill rate is flat but OTIF fell nine points, the likely cause is late delivery, not shortages, though order-level shortfalls hidden inside a unit fill rate are another possibility."
**Explain simply:**
- **OTIF** = share of orders delivered on time and in full; **fill rate** = share of ordered quantity shipped (several definitions exist, state yours).
- Hypothesis 1: delivery timing worsened (carrier delays, dispatch slips, tighter promised dates, receiving appointment misses).
- Hypothesis 2: fill rate is measured as units, but OTIF is order-level; many orders can be short by a little each, which barely moves unit fill rate yet fails OTIF.
- Hypothesis 3: definition or data change, such as a stricter on-time window or tolerance.
- Test: split OTIF failures into late-only, short-only, both; compute order fill rate beside unit fill rate; check days late distribution; compare by carrier, customer and date.
**Likely follow-ups:** 1) *If late-only dominates?* Look at transit and dispatch. 2) *If short-only?* Order-level shortages at line level.
**Common mistakes:** Assuming stable fill rate means no service issue; mixing fill rate definitions; ignoring the OTIF tolerance window.

### Q63 ⭐⭐ 🔴 The business reports 98% stock availability but customers still complain about stockouts. How could both be true, and what would you check?
**Asked at:** commonly asked (no company-specific report found); availability paradox is a gap-fill case based on inventory accuracy themes (unverified).
**What the interviewer is checking:** Whether you question how a headline metric is defined and averaged.
**Say this in the interview:** "A high availability figure can hide the problem if it is averaged across all items and locations, measured at the wrong time of day, or counts stock that is not truly sellable. I would test the definition first, then the weak spots."
**Explain simply:**
- **Availability** here means share of SKU-location combinations with stock at a measurement point.
- How both can be true: (1) it is averaged, so many slow items in stock lift it while a few best-sellers are out; (2) it is not weighted by sales; (3) measured once at night, not when customers shop; (4) system stock is wrong (inventory record accuracy), the shelf is empty; (5) stock exists in another location, damaged, on hold or in the back room; (6) complaints are concentrated in certain stores or regions.
- Check: availability weighted by sales; by hour; for top 100 SKUs; by location; compare system stock with physical counts; lost sales and complaint data by SKU.
**Likely follow-ups:** 1) *Better KPI?* Sales-weighted on-shelf availability at peak hours. 2) *Which first?* Top sellers in complaint locations.
**Common mistakes:** Trusting the 98% without its definition; unweighted averages; ignoring system versus physical stock gaps.

### Q64 ⭐ 🟢 What are Incoterms (for example FOB and CIF) in plain words, and why do they matter to a logistics analyst?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic for logistics roles.
**What the interviewer is checking:** Basic trade vocabulary: who pays and who bears risk at each stage.
**Say this in the interview:** "Incoterms are standard trade terms that say who arranges and pays for transport, insurance and customs, and where risk passes from seller to buyer. FOB and CIF are two common sea-freight terms."
**Explain simply:**
- Details below are from memory, unverified; confirm against the official ICC Incoterms text.
- **FOB** (free on board): the seller delivers goods onto the ship at the origin port; after that, the buyer carries cost and risk.
- **CIF** (cost, insurance and freight): the seller pays freight and insurance to the destination port, but risk still passes when goods are loaded on the ship (from memory, unverified; the current Incoterms rules should be confirmed from the official ICC text).
- Why it matters to an analyst: it decides which costs sit in landed cost, whose data holds the shipment status, who files claims for damage, and when ownership of inventory (and so book stock) changes.
- Comparing supplier quotes needs the same Incoterm, otherwise prices are not comparable.
**Likely follow-ups:** 1) *Which term gives buyer most control?* FOB, as the buyer chooses the carrier. 2) *Where in data?* A field on the purchase order.
**Common mistakes:** Comparing a CIF price with an FOB price; thinking CIF means the seller carries risk all the way.

### Q65 ⭐ 🟢 What is a bill of lading, an invoice and a packing list, and what is each document used for in shipping?
**Asked at:** commonly asked (no company-specific report found); shipping documents are a differentiator topic.
**What the interviewer is checking:** Whether you know the paperwork that creates the data trail for a shipment.
**Say this in the interview:** "The bill of lading is the carrier's receipt and transport contract; the invoice is the seller's bill for payment and customs value; the packing list says what is in each package."
**Explain simply:**
- **Bill of lading (B/L):** issued by the carrier; proves goods were received for shipping, shows route and consignee, and in many cases acts as title to the goods.
- **Invoice:** from seller to buyer; lists price, quantity and terms; used for payment, customs duty and accounting.
- **Packing list:** lists items, quantities, weights and packages without prices; used by warehouse for receiving checks and by customs for inspection.
- Together they let you match what was ordered, shipped and received; mismatches create delays at customs or receiving.
- For data: shipment number, B/L number, invoice number and PO number are keys that link systems.
**Likely follow-ups:** 1) *Which one at receiving?* Packing list against physical goods. 2) *Which one for payment?* Invoice, after three-way match.
**Common mistakes:** Mixing invoice and packing list; ignoring that document numbers can have typing variations when joining.

### Q66 ⭐ 🟢 What does lean or just-in-time inventory mean, and what risk does it carry when supply is disrupted?
**Asked at:** commonly asked (no company-specific report found); lean and just-in-time are standard operations vocabulary.
**What the interviewer is checking:** Whether you know the benefit (low stock) and the risk (no buffer).
**Say this in the interview:** "Lean or just-in-time means holding very little stock and receiving materials only when needed. It saves cash and space, but when supply is disrupted there is no buffer, so production or sales stop quickly."
**Explain simply:**
- **Just-in-time (JIT)**: parts arrive close to when they are used, like ordering lunch to arrive at 1 pm instead of stocking a week of food.
- **Lean** is the wider approach of removing waste (excess stock, waiting, rework).
- Benefits: lower inventory days, less cash tied up, less obsolete stock.
- Risks: supplier delay, port disruption or a demand spike causes stockouts; reliance on few suppliers; little room for forecast error.
- Analyst's view: monitor supplier lead time variability, single-source dependencies and days of cover on critical items; some firms hold extra safety stock for critical parts.
**Likely follow-ups:** 1) *How to reduce the risk?* Dual sourcing, buffer on critical items, early warning on supplier delays. 2) *Is JIT right for all?* No, not for long, uncertain lead times.
**Common mistakes:** Equating lean with minimum stock everywhere; ignoring lead time variability.

### Q67 ⭐ 🟢 What are GST, e-way bills and eInvoicing in plain words, and why do they matter to transport and inventory data in India (from memory, unverified)?
**Asked at:** commonly asked (no company-specific report found); Indian context gap-fill.
**What the interviewer is checking:** Awareness of how tax rules create fields and checkpoints in logistics data.
**Say this in the interview:** "GST is India's indirect tax on goods and services; an e-way bill is an electronic document needed to move goods above a value limit; eInvoicing is the system where business invoices are registered on a government portal and get a unique number. Details are from memory, unverified."
**Explain simply:**
- **GST** (Goods and Services Tax): one tax on supply of goods and services, with rates by product category; businesses claim credit for tax paid on purchases.
- **E-way bill:** generated for movement of goods when consignment value exceeds a threshold (threshold and rules should be checked), carries vehicle, route and invoice details.
- **eInvoicing:** invoices of businesses above a turnover threshold are reported to a portal, which returns a unique invoice reference number.
- Why it matters: data fields such as GSTIN, HSN code (product classification), e-way bill number, vehicle number and invoice reference link transport, invoicing and inventory records; missing or expired e-way bills delay trucks; tax rates affect landed cost.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance or tax team; thresholds and rules change.
**Likely follow-ups:** 1) *How to use e-way data?* Transit time per truck. 2) *Which key joins data?* Invoice number and e-way bill number.
**Common mistakes:** Quoting thresholds as fact; ignoring that the date a tax invoice is raised may differ from the date goods physically arrive.

### Q68 ⭐ 🟡 What is the cash-to-cash cycle, and how do inventory days, receivable days and payable days combine to produce it?
Days of inventory 45, days sales outstanding 30, days payables outstanding 40.
**Asked at:** commonly asked (no company-specific report found); cash-to-cash cycle was not covered by the source searches, so this is a differentiator gap-fill.
**What the interviewer is checking:** Whether you can link inventory to cash.
**Say this in the interview:** "Cash-to-cash cycle is days of inventory plus receivable days minus payable days; here 45 plus 30 minus 40 gives 35 days, the time cash is tied up between paying suppliers and collecting from customers."
**Explain simply:**
- **Days of inventory:** how long stock sits before being sold.
- **Days sales outstanding (DSO):** how long customers take to pay after a sale.
- **Days payables outstanding (DPO):** how long the business takes to pay suppliers.
- Cash goes out when we pay suppliers and comes back when customers pay; the gap is financed by the business. Shorter is better, all else equal.
- HR parallel: paying salaries monthly while clients pay in 60 days means the company funds the gap.
- Levers: cut stock (inventory days), collect faster (DSO), negotiate longer terms (DPO); but stretching supplier terms too far can harm supplier relations.
**Worked example:** 45 + 30 - 40 = 35 days (computed, no rounding). If inventory days fell by 5 to 40, the cycle would be 30 days.
**Likely follow-ups:** 1) *Can it be negative?* Yes, if payables exceed the other two. 2) *Definition variations?* Days may be based on cost of goods sold or sales; state which.
**Common mistakes:** Adding payables instead of subtracting; mixing sales-based and cost-based days.

### Q69 ⭐ 🟡 How do you compute and interpret the obsolete or aged inventory share, and what actions follow?
Total stock Rs 10 crore; items with no movement in 180 days Rs 1.2 crore; items 90-180 days Rs 2 crore.
**Asked at:** commonly asked (no company-specific report found); inventory ageing appears in supply chain KPI guides (unverified).
**What the interviewer is checking:** Whether you can turn stock value into ageing buckets and link each bucket to an action, not just report one percentage.
**Say this in the interview:** "Aged share is the value of stock that has not moved for a set number of days divided by total stock value. Here 1.2 of 10 crore is dead stock, 12%, and a further 20% is slowing, so 32% needs attention."
**Explain simply:**
- Inventory ageing means "how long has this item been sitting without being sold or used". Obsolete stock is stock with little or no chance of selling at full price (expired, outdated model, discontinued).
- Use value (rupees at cost), not item count, otherwise one cheap screw counts the same as one expensive machine.
- Buckets are company choices (30/60/90/180 days); state yours.
- Think of it like unused leave balance: a small pile is normal, a growing pile that never gets used is a warning.
- Actions: bucket 180+ days, review for discount, return to supplier, transfer to another site, donate, scrap, or make a provision (an accounting write-down, finance decides). Bucket 90-180 days, stop reordering, run a promotion, check the forecast.

**Worked example:**
- Dead stock share = 1.2 / 10 = 12.0%.
- Slow bucket (90-180 days) = 2.0 / 10 = 20.0%.
- Total at-risk (over 90 days) = 3.2 / 10 = 32.0%; healthy stock = 10 - 3.2 = Rs 6.8 crore (68.0%).
- The 90-180 and 180+ buckets are assumed separate (no double counting); if "no movement in 180 days" were included in the 2 crore, the answer would change, so confirm.

**Likely follow-ups:** 1) *Is 12% bad?* There is no universal threshold; compare with last quarter, with similar categories, and look at the trend. 2) *Why not just write it all off?* It hits profit and some items may still sell; decide item by item with finance.
**Common mistakes:** Using item count instead of value; ignoring items newly received that have not had time to sell; treating "no sales" as obsolete for seasonal goods (check last year's season).

### Q70 ⭐ 🟡 What is the difference between forecast accuracy measured at lead time and at one month ahead, and why does the measurement lag matter?
**Asked at:** commonly asked (no company-specific report found); lag-based forecast accuracy appears in demand planning articles (unverified).
**What the interviewer is checking:** Whether you know a forecast must be judged at the point when the decision was made, not after the answer is known.
**Say this in the interview:** "Lag means how far ahead the forecast was made. I measure accuracy using the forecast as it stood one lead time before the sales month, because that is when orders were placed. Later forecasts are usually more accurate but no longer useful for those orders."
**Explain simply:**
- Lead time is the wait from placing an order with a supplier to receiving the goods. If it is 3 months, stock for March must be ordered in December.
- "Lag 3" accuracy compares March actual sales with the forecast made in December. "Lag 1" compares with the forecast made in February.
- Forecasts get better closer to the date, so lag 1 looks flattering. Judging a planner on lag 1 when decisions need lag 3 hides the real error.
- Practically you must save a snapshot of every forecast each month. If you overwrite the old forecast, you cannot measure lag accuracy later.
- Same idea as HR: judging a headcount plan using the number you knew at year end, rather than what you forecast when hiring was approved.

**Likely follow-ups:** 1) *Which lag do I report?* Lag equal to the replenishment lead time. 2) *What if the snapshot was not saved?* Start saving now; do not rebuild from memory.
**Common mistakes:** Comparing actuals with the latest forecast only; mixing lags in one number; forgetting that different products have different lead times.

### Q71 ⭐ 🟡 What is Forecast Value Add (FVA), and how would you test whether a planner's manual override improved on the statistical forecast?
Statistical forecast error 18%; after planner override 22%; naive last-month forecast error 25%.
**Asked at:** commonly asked (no company-specific report found); FVA is described in demand planning articles (unverified).
**What the interviewer is checking:** Whether you judge each step of the forecast process against a simple baseline, and test fairly.
**Say this in the interview:** "FVA is the error before a step minus the error after it. Here the statistical forecast beat the naive one by 7 points, but the planner override made it 4 points worse, so the override destroyed value."
**Explain simply:**
- A naive forecast is the simplest guess, such as "next month equals last month". Any effort should beat it.
- FVA for a step = error without the step minus error with it. Positive means the step helped. I use the same error measure for all steps (for example WAPE, total absolute error divided by total actual sales).
- Fair test: take the same SKU-months, record the statistical forecast and the final forecast, and compute absolute error for each. Count in how many cases the override was closer, and test the paired differences (sign test or paired t-test).
- Split by override direction (up or down) and size, since planners often add optimism.

**Worked example:**
- Statistical vs naive: 25% - 18% = +7 percentage points (helped).
- Override vs statistical: 18% - 22% = -4 percentage points (hurt).
- Override vs naive: 25% - 22% = +3 percentage points.
- Percentage points, not percent, because these are differences between two percentages.

Interview version on a tiny made-up sheet (6 SKUs, a separate illustration from the 18%/22%/25% figures above). (`stat` is the statistical forecast, `final` is after the planner override.)
```python
import pandas as pd

forecasts = pd.DataFrame({
    "actual": [100, 80, 90, 70, 60, 100],
    "stat":   [110, 85, 98, 82, 63, 105],
    "final":  [112, 87, 101, 84, 63, 101],
})

# error of each forecast against what actually sold
forecasts["stat_error"]  = (forecasts["stat"]  - forecasts["actual"]).abs()
forecasts["final_error"] = (forecasts["final"] - forecasts["actual"]).abs()

# WAPE: total error divided by total sales
stat_wape  = forecasts["stat_error"].sum()  / forecasts["actual"].sum()
final_wape = forecasts["final_error"].sum() / forecasts["actual"].sum()

# in how many SKUs did the override get closer?
override_better = (forecasts["final_error"] < forecasts["stat_error"]).sum()
```
Output: statistical 8.6%, final 9.6%, override closer in 1 of 6 SKUs (worse in 4, tied in 1). Meaning: overrides added error on this sample.

**Likely follow-ups:** 1) *Should planners stop overriding?* Not always; keep overrides for known events (promotions) that the model cannot see, and track them. 2) *Is one bad month proof?* No, need many periods.
**Common mistakes:** Calling the gap "4%" instead of 4 points; using different error measures per step; judging on too few SKUs.

### Q72 ⭐ 🟡 What is a spend cube or spend analysis, and what first cuts would you make to find savings in procurement data?
**Asked at:** commonly asked (no company-specific report found); spend analysis appears in procurement analyst question lists (unverified).
**What the interviewer is checking:** Whether you can organise purchase data into useful views and spot where savings really are.
**Say this in the interview:** "A spend cube is purchase data sliced by three views: what we buy (category), who we buy from (supplier) and who buys it (department or site). I would first clean it, then look for concentration, price differences and fragmented buying."
**Explain simply:**
- Procurement means buying goods and services for the company. Spend is the rupees paid to suppliers.
- Imagine a payroll table sliced by department, grade and location; a spend cube does the same for purchases.
- First clean: the same supplier spelled five ways, missing categories, duplicate invoices, credit notes.
- First cuts: top 10 suppliers and categories (Pareto), number of suppliers per category (too many means weak bargaining power), price paid for the same item by different sites or suppliers, spend off-contract ("maverick" buying outside agreed deals), and monthly trend.
- Savings come from consolidating suppliers, moving to the best price, renegotiating, or cutting unneeded purchases.

**Data and tables involved:** purchase orders and invoice lines (date, supplier ID, item, category, quantity, unit price, department, site), supplier master, contract price list. First join invoices to the supplier master to unify names.

**Likely follow-ups:** 1) *How do you measure a saving?* Price difference times quantity against a baseline, agreed with finance. 2) *What if categories are missing?* Classify by item description and supplier with rules, then sample-check.
**Common mistakes:** Skipping cleaning; counting a lower price as a saving when volume also fell; ignoring quality and delivery performance.

### Q73 ⭐ 🟡 Explain Pareto (80/20) analysis for spend and for defects, and how you would build it in Excel or Power BI.
**Asked at:** commonly asked (no company-specific report found); Pareto charts are a standard supply chain and quality topic (unverified).
**What the interviewer is checking:** Whether you understand the idea of "vital few" and can build the cumulative chart.
**Say this in the interview:** "Pareto analysis ranks items from biggest to smallest and shows the cumulative share, so you see the few that cause most of the result. Often a few suppliers make most of the spend, or a few defect types cause most of the complaints. 80/20 is a rule of thumb, not a law."
**Explain simply:**
- Spend: rank suppliers by rupees; the top few often carry most of the spend, so negotiating effort goes there.
- Defects: rank defect types by count (or cost); fixing the top two removes most of the problem.
- Steps in Excel: sort descending; share = value / total; cumulative share = running sum of share; chart bars for value and a line for cumulative % on a second axis (a combo chart); mark the 80% line.
- Power BI: a column and line chart with supplier on the axis, spend as columns, and a measure for running total divided by total as the line.

**Worked example** (8 suppliers, invented spend in Rs lakh: 40, 25, 12, 8, 6, 4, 3, 2; total 100):
```python
import pandas as pd

spend = pd.DataFrame({"spend": [40, 25, 12, 8, 6, 4, 3, 2]})

# rank suppliers from biggest spend to smallest
spend = spend.sort_values("spend", ascending=False)

# share of total, then running total of the share
spend["share_pct"] = spend["spend"] / spend["spend"].sum() * 100
spend["cumulative_pct"] = spend["share_pct"].cumsum()
```
Output: cumulative share is 40, 65, 77, 85, 91, 95, 98, 100. The top 3 suppliers (37.5% of suppliers) give 77% of spend; the top 4 cross 80% (85%). Meaning: focus on A to D.

**Likely follow-ups:** 1) *Is it always 80/20?* No, it may be 90/10 or 70/30. 2) *Count or cost for defects?* Show both; a rare defect can be costly.
**Common mistakes:** Not sorting before the cumulative step; mixing categories of different sizes; treating the top few as the only ones worth watching (a small supplier may be critical).

### Q74 ⭐ 🟡 What are the components of landed cost, and how would you compute landed cost per unit from the data below?
Unit price Rs 200, freight Rs 12 per unit, customs duty 10% of unit price, handling Rs 3 per unit.
**Asked at:** commonly asked (no company-specific report found); landed cost is a procurement and import topic (unverified).
**What the interviewer is checking:** Whether you look beyond the invoice price at the true cost of getting an item into the warehouse.
**Say this in the interview:** "Landed cost is everything it costs to get the item to my door: price plus freight, duty and handling. Here it is 200 + 12 + 20 + 3 = Rs 235 per unit, 17.5% above the invoice price."
**Explain simply:**
- Typical components: purchase price, freight (transport), insurance, customs duty and other taxes that cannot be claimed back, port and clearing charges, handling, and sometimes storage or financing cost.
- Duty base differs by country and rule; here duty is on unit price as given. If duty were charged on price plus freight, it would be 10% of 212 = Rs 21.2, giving Rs 236.2 (from memory, unverified, confirm with the customs or finance team).
- Why it matters: the cheapest supplier on price may not be cheapest landed.

**Worked example:**
- Duty = 10% x 200 = Rs 20.
- Landed cost = 200 + 12 + 20 + 3 = Rs 235 per unit.
- Uplift = 35 / 200 = 17.5% (rupees; percent of invoice price).

**Likely follow-ups:** 1) *Allocate a lump freight bill?* Share by weight, volume or value, and state the rule. 2) *Does GST count?* Usually not, if it can be claimed as credit (from memory, unverified; confirm with finance).
**Common mistakes:** Comparing suppliers on unit price only; forgetting currency exchange differences; allocating freight evenly when items differ in size.

### Q75 ⭐ 🟡 What is vendor-managed inventory (VMI) and consignment stock, and how do they change who owns the inventory data?
**Asked at:** commonly asked (no company-specific report found); VMI is a differentiator topic for supply chain roles (unverified).
**What the interviewer is checking:** Whether you separate who holds stock, who owns it, and who sees the data.
**Say this in the interview:** "In VMI the supplier decides when and how much to replenish at my site, using my stock and sales data. In consignment the supplier owns the stock until I use it. They can be combined, and each changes who needs what data."
**Explain simply:**
- VMI: the buyer shares stock levels and sales daily; the supplier plans the refill. The buyer does less ordering.
- Consignment: stock sits in the buyer's warehouse but belongs to the supplier; the buyer pays only when it is consumed or sold.
- Data: under VMI the supplier needs near real-time access to the buyer's stock and sales, so data-sharing terms and access control matter. Under consignment, the buyer's books show no stock until use, so the analyst must track consigned stock separately, or availability looks lower than reality.
- Analyst impact: inventory turns and working capital look better for the buyer; reconcile stock counts with the supplier regularly.

**Likely follow-ups:** 1) *Who is responsible for shrinkage?* Set by contract; analysts flag differences. 2) *Risk?* Supplier errors, data delays.
**Common mistakes:** Reporting consigned stock as owned (or leaving it out of availability); assuming VMI means no buyer oversight.

### Q76 ⭐ 🟡 What are the common ways to measure capacity utilisation in a warehouse (storage, labour, dock), and what data would each need?
Pallet positions: 5,000 total, 4,350 occupied.
**Asked at:** commonly asked (no company-specific report found); warehouse utilisation appears in warehouse KPI guides (unverified).
**What the interviewer is checking:** Whether you know that "utilisation" has several meanings and that 100% is not the goal.
**Say this in the interview:** "Storage utilisation here is 4,350 / 5,000 = 87%. I would add labour utilisation and dock utilisation, because a warehouse can be nearly full on space but idle on doors."
**Explain simply:**
- Storage: occupied pallet positions / total positions. Needs location master (positions) and stock by location. Above roughly 85-90% often hurts movement and putaway (a rule of thumb, unverified).
- Labour: productive hours / paid hours. Needs timesheets or the warehouse system's task logs. It is like attendance versus actual work done.
- Dock: door hours in use / door hours available, or trucks handled per door per day. Needs gate-in/gate-out times and door assignment.
- Report each alongside the peak, not just the average.

**Worked example:**
- Storage: 4,350 / 5,000 = 87.0%; 650 positions free.
- Labour (illustrative): 1,240 productive hours / 1,600 paid hours = 77.5%.
- Dock (illustrative): 96 door-hours used / 120 available = 80.0%.

**Likely follow-ups:** 1) *Is 100% good?* No, there is no room to move stock. 2) *Why track peaks?* Festival weeks can break a warehouse that looks fine on average.
**Common mistakes:** Counting blocked or damaged locations as available; using area instead of positions without saying; mixing paid and productive hours.

### Q77 ⭐ 🟡 What does inventory write-off or shrinkage mean, what causes it, and how would you quantify shrinkage from book stock and physical count?
Book stock Rs 8.0 crore; physical count Rs 7.8 crore; sales for the period Rs 40 crore.
**Asked at:** commonly asked (no company-specific report found); shrinkage is a retail and warehouse topic (unverified).
**What the interviewer is checking:** Whether you compute the gap correctly and explain it before blaming theft.
**Say this in the interview:** "Shrinkage is stock that the books say we have but we cannot find. Book 8.0 minus counted 7.8 is Rs 0.2 crore, 2.5% of book stock or 0.5% of sales."
**Explain simply:**
- Book stock is what the system says; physical count is what people actually count.
- Write-off is removing lost, damaged or expired stock from the books.
- Causes: theft, damage, expiry, receiving or picking errors, wrong unit of measure, unrecorded returns, timing differences (goods shipped but not yet booked).
- Before calling it loss, check timing and data entry, and recount large differences.
- Pick the base clearly. Stock is at cost and sales at selling price, so shrinkage as a share of sales is only a rough guide; cost of goods sold is a cleaner base.

**Worked example:**
- Shrinkage = 8.0 - 7.8 = Rs 0.2 crore (Rs 20 lakh).
- As % of book stock: 0.2 / 8.0 = 2.5%.
- As % of sales: 0.2 / 40 = 0.5%.

**Likely follow-ups:** 1) *Is 0.5% high?* Compare with past periods and similar sites; no universal benchmark. 2) *Cycle count vs full count?* Cycle counts check a few items regularly and find causes sooner.
**Common mistakes:** Treating all of the gap as theft; netting overages against shortages without showing both; mixing selling price and cost.

### Q78 ⭐ 🟡 What data-privacy and confidentiality points should an analyst keep in mind when handling supplier contracts, pricing and driver or warehouse staff personal data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you handle confidential commercial data and personal data responsibly, as an HR professional would.
**Say this in the interview:** "Supplier prices and contracts are confidential business data; staff and driver details are personal data. I would share only what is needed, with the right people, and not copy either into personal files or unapproved tools."
**Explain simply:**
- Supplier contracts and prices: restrict access, keep them off shared screenshots and emails, and do not show one supplier's price to another. Aggregate where possible.
- Driver and staff data: names, phone numbers, ID numbers, location tracking, pay and attendance. Use employee IDs, or mask names, and share team-level results unless individual detail is needed.
- Collect only what the analysis needs and keep it only as long as needed.
- Work in approved systems, with access logs; no personal email or cloud copies.
- Ask when unsure; contract terms and company policy decide.

**Regulation / privacy note (awareness only):** India's Digital Personal Data Protection Act, 2023 covers personal data handling, including consent and purpose limits (from memory, unverified, confirm with the compliance/legal team). Contracts may also contain confidentiality clauses.

**Likely follow-ups:** 1) *A manager asks for one driver's data?* Check the purpose and permission first. 2) *Vendor price list in a dashboard?* Restrict viewers.
**Common mistakes:** Sending raw extracts by email; leaving names in a published dashboard; keeping data forever.

### Q79 ⭐ 🟡 How would you monitor warehouse labour productivity and attendance together, and what care is needed with staff-level data?
**Asked at:** commonly asked (no company-specific report found); overlaps with the HR and operations bridge in analyst roles.
**What the interviewer is checking:** Whether you combine HR and operations data sensibly and fairly.
**Say this in the interview:** "I would join attendance with work output by shift and team: units picked per paid hour next to absence rate. Staff-level numbers are sensitive, so the default view is team and shift, and individual data only with a clear purpose."
**Explain simply:**
- Productivity = work done / hours worked, for example lines picked per labour hour. Compare like tasks (picking with picking).
- Attendance: absence rate, late arrivals, overtime, and temporary or contract staff share.
- Together they show if low output came from fewer people, less experienced people or slower work. Missing staff raises overtime, which can lower output per hour.
- Fair comparisons adjust for task mix, zone, shift and tenure.
- Care: output per person is affected by equipment, layout and orders given. Do not rank individuals from one metric; discuss patterns with supervisors; keep data access limited.

**Data and tables involved:** attendance or shift roster (employee ID, date, shift, hours), warehouse task log (task type, quantity, time), employee master (team, joining date). Join on employee ID and date; first cut by shift and week.

**Regulation / privacy note (awareness only):** Staff monitoring raises consent and purpose questions (from memory, unverified, confirm with HR and legal).

**Likely follow-ups:** 1) *Individual targets?* Use with care and context. 2) *What if absence rises?* Check shift, supervisor, and workload, not just people.
**Common mistakes:** Ranking individuals publicly; ignoring task mix; counting overtime hours as normal hours.

### Q80 ⭐ 🔴 Design a KPI dashboard for a regional distribution centre: which metrics would you choose for inbound, storage, outbound and delivery, and which would you leave out?
**Asked at:** commonly asked (no company-specific report found); dashboard design is a standard analyst case.
**What the interviewer is checking:** Whether you pick a few decision-useful metrics per stage, not everything available.
**Say this in the interview:** "I would follow the goods: a few metrics per stage, one headline per stage, and a clear owner for each. I would leave out vanity metrics that nobody can act on."
**Explain simply:**
- Ask first who uses it (site manager daily, regional head weekly) and what decisions follow.
- Inbound (goods arriving): dock-to-stock time (truck arrival to sellable), supplier on-time delivery, receiving accuracy.
- Storage: inventory accuracy, storage utilisation, aged stock share, stockouts of key items.
- Outbound (picking and packing): orders shipped on time, pick accuracy, orders per labour hour, backlog at cut-off.
- Delivery: on-time in-full (OTIF, orders delivered on the promised date and complete), cost per order, failed delivery rate.
- Layout: top row of 4-6 headline numbers with trend vs target; stage panels beneath; filters for day and customer type; definitions in a note.
- Leave out: metrics with no owner or action, 20 versions of the same measure, raw counts without a base, and individual staff league tables.

**Likely follow-ups:** 1) *How many metrics?* Fewer than ten on page one. 2) *Daily or weekly?* Operations daily, trends weekly.
**Common mistakes:** Showing averages that hide late-day spikes; no target or comparison; unclear definitions.

### Q81 ⭐ 🔴 A supplier delay has put a key component out of stock for ten days. Which analyses would you run to size the impact on orders and revenue and to recommend a response?
**Asked at:** commonly asked (no company-specific report found); disruption root cause is a listed theme in supply chain analyst guides (unverified).
**What the interviewer is checking:** Whether you size loss in orders and rupees, separate lost from delayed sales, and offer practical options.
**Say this in the interview:** "I would size what was demanded and not shipped, split it into lost and merely delayed sales, convert to revenue and margin, and compare response options by cost against the loss."
**Explain simply:**
- Exposure: which products use this component (bill of materials, the parts list of a product), open orders, and stock on hand and in transit.
- Demand during the gap: average daily demand times ten days, adjusted for day-of-week and promotions.
- Lost vs delayed: customers who wait (backorders) versus cancel; use past stockout history to estimate the recovery share.
- Impact: orders affected, revenue, margin, and key customer penalties.
- Response: expedite (air freight), alternate supplier, substitute product, prioritise key customers, communicate new dates. Compare each cost with the loss avoided.

**Worked example (invented inputs):** demand 120 units a day, Rs 450 per unit, 10 days. Demand in gap = 1,200 units, Rs 5.4 lakh of revenue. If 60% of it is lost for good, lost revenue = Rs 3.24 lakh; the other 40% is delayed. Expediting is worth it only if it costs less than the lost margin it saves.

**Likely follow-ups:** 1) *What after recovery?* Plan for a catch-up surge. 2) *Prevent repeat?* Safety stock, second source, supplier risk tracking.
**Common mistakes:** Treating all demand as lost; ignoring downstream products; no cost comparison for responses.

### Q82 ⭐ 🔴 How would you use data to decide whether to open a new warehouse or dark store in a city, and what inputs and trade-offs would you consider?
**Asked at:** commonly asked (no company-specific report found); prep sites list "design supply chain for a Tier 2 city" type prompts (unverified).
**What the interviewer is checking:** Whether you frame a location decision with demand, cost and service trade-offs.
**Say this in the interview:** "I would estimate demand by pin code, test how delivery time and cost improve with a site, and compare the saving and extra sales against rent, staff and stock costs, with a few scenarios."
**Explain simply:**
- A dark store is a small warehouse that serves online orders only, with no walk-in customers, for fast delivery.
- Inputs: orders by pin code and time of day, growth, delivery times, order value and basket, rent, labour, delivery cost per order, supplier distance, and competitors.
- Analysis: map demand clusters; compute coverage within the delivery promise (such as 30 minutes); compare cost per order and delivery time with and without the site; estimate break-even orders per day.
- Trade-offs: speed versus cost, more sites versus lower utilisation each, more stock locations versus higher stock, flexibility (lease length).
- Run low, base and high demand cases and show when it breaks even.

**Likely follow-ups:** 1) *Cannibalisation?* New site may take orders from nearby sites; subtract it. 2) *Pilot first?* Often cheaper than a full commitment.
**Common mistakes:** Using current orders without growth; ignoring ramp-up time; looking at average cost only.

### Q83 ⭐ 🔴 Two warehouses show different cost per order. How would you compare them fairly, and which factors would you adjust for before judging either?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you notice that warehouses differ in work content, and normalise before judging.
**Say this in the interview:** "Cost per order mixes different jobs. I would compare on a like-for-like base, such as cost per order line or per unit, and adjust for order mix, size, volume, location costs, service level and automation."
**Explain simply:**
- Check cost definitions first: same cost items (rent, labour, utilities, overhead allocation), same period.
- Adjust for: lines per order, units per line, product size and weight, share of special handling (cold, fragile), volume (fixed costs spread), local wages and rent, service speed promised, returns share, automation.
- Compare also productivity (orders per labour hour) and quality (accuracy).
- Show ranges, not a verdict, and ask the site managers before concluding.

**Worked example (invented):** both do 40,000 orders; A costs Rs 50 lakh and B Rs 60 lakh. Cost per order: A Rs 125, B Rs 150. But A averages 1.8 lines per order (72,000 lines) and B 3.2 (128,000 lines). Cost per line: A Rs 69.4, B Rs 46.9. After adjusting, B looks more efficient.

**Likely follow-ups:** 1) *What if one is in a costlier city?* Adjust for wage and rent levels. 2) *Fixed vs variable cost?* Separate them, since volume changes affect them differently.
**Common mistakes:** Comparing raw cost per order; using different cost definitions; ignoring service differences.

### Q84 ⭐ 🔴 How would you build a simple S&OP review pack that shows a forecast, an inventory plan and the gaps for the next three months, and what questions would you expect from sales and finance?
**Asked at:** commonly asked (no company-specific report found); S&OP appears in supply chain planning job postings (unverified).
**What the interviewer is checking:** Whether you can bring demand, supply and money into one view and handle cross-team questions.
**Say this in the interview:** "S&OP (sales and operations planning) is a monthly meeting to agree one plan. My pack would show, for each of the next three months, demand forecast, supply and inventory plan, the gap, and the money impact, with assumptions and risks."
**Explain simply:**
- Page 1: summary and decisions needed. Then per month: forecast versus last year and versus last month's forecast; supply (production, purchases, stock in transit); projected closing stock against target; the gap (shortfall or excess) by product group.
- Add last month's forecast accuracy and bias, and top risks (supplier delays, big promotions).
- Keep one version of numbers, source tables named, changes explained.
- Sales will ask: why did the forecast change, can we cover the promotion, which customers are at risk? Finance will ask: what stock value and working capital, what is the revenue and margin at risk, is the plan within budget?
- Prepare options and rupee costs for each gap.

**Likely follow-ups:** 1) *Who owns the numbers?* Demand with sales, supply with operations, signed off together. 2) *Why three months?* Matches typical lead times and decisions.
**Common mistakes:** Showing too many tables; no assumptions page; changing forecasts silently.

### Q85 ⭐ 🔴 Planners say the forecast model is good but inventory still keeps growing. What data would you examine to find out whether the cause is forecasting, ordering, MOQs, supplier lead times or slow sales?
**Asked at:** commonly asked (no company-specific report found); root-cause diagnosis is a listed theme in supply chain analyst guides (unverified).
**What the interviewer is checking:** Whether you split the problem into stages and test each with data rather than accepting the planners' view.
**Say this in the interview:** "Good forecast accuracy does not guarantee low stock. I would trace stock growth stage by stage: forecast bias, what was ordered against what was recommended, MOQ rounding, lead-time changes, and actual sales speed, and see which explains most of the extra stock."
**Explain simply:**
- Forecast: check bias (consistently too high) as well as accuracy, using the forecast at lead-time lag, on the items where stock grew.
- Ordering: compare system-recommended order with actual order; planners may order extra "to be safe".
- MOQ (minimum order quantity, the smallest batch a supplier will sell): where the MOQ is bigger than the need, each order adds excess; compare order size with demand over the cover period.
- Lead times: compare promised and actual; if lead times grew, safety stock and in-transit stock rise; early deliveries add stock.
- Slow sales: ageing, sales rate, and days of cover by item and category; a few slow SKUs can drive most growth (Pareto).
- Also check new item launches and discontinued items still being bought.

**Data and tables involved:** monthly forecast snapshots, sales, purchase orders (ordered, promised and received dates, quantity), supplier MOQ and lead-time master, inventory by date and ageing. First cut: stock growth split by category and by item, then days of cover.

**Likely follow-ups:** 1) *Which cause is most likely?* Let the data decide; check bias and MOQ first. 2) *Quick fix?* Pause orders on high-cover items.
**Common mistakes:** Checking only accuracy; averaging all items (growth is usually concentrated); blaming planners before checking supplier data.
